#!/usr/bin/python
# Python 3.X is recommended for trees with Unicode filenames
"""
################################################################################
Usage:
    [py[thon]] cpall.py dirFrom dirTo [-skipcruft] [-v] [-vv]
    
Recursive copy of a directory tree.  Works like a "cp -rp dirFrom/* dirTo"
Unix command, and assumes that dirFrom and dirTo are both directories.
Was written to get around fatal error messages under Windows drag-and-drop
copies (the first bad file ends the entire copy operation immediately),
but also allows for coding more customized copy operations in Python.
The "-skipcruft" option ignores (does not copy) dirFrom cruft files, as
defined by patterns in mergeall_configs.py.  "-v" and "-vv" change the copy's
verbose level to 1 (dirs) and 2 (dirs+files), from its default 0 (neither).

--------------------------------------------------------------------------------

CHANGE LOG:

FOR MERGEALL 2.0:

Copy stat info too
    Add shutil.copystat option to copyfile, to copy over the original's
    modtime (and other metadata) in addition to content.  This replaces an
    older money-patching approach.  Also for 2.0, add explicit file.close()
    calls, for use outside CPython.

FOR MERGEALL 3.0:

Windows long paths:
    Use fixlongpaths.OPEN() for long Windows file pathnames.  This avoids
    exceptions and skips during updates. 

Exception propagation:
    Allow exceptions to be propagated to caller, instead of printing error
    messages and continuing.  Required for properly cancelling a corresponding
    update when a backup copy fails.

Cruft files
    Filter out (and hence do not copy) files with names matching system cruft
    files defined in mergeall_configs.py if mode "-skipcruft" is used.  This is 
    required here for files in unique FROM dirs whose content is not inspected
    by mergeall itself before a bulk (atomic) copy to TO.  Tree copies for
    backups do not need to filter this way: they only copy data that was already
    in the TO tree.   This copytree() mode can be used when called from other
    programs too, though the cruft definition file is somewhat mergeall-specific
    as coded.

Cruft command-line arg
    Since it's already supported in call mode, added the "-skipcruft"
    command-line option to this script too, for use when run standalone.
    When used, this ignores (does not copy) metadata files like some other
    cut/paste and drag-and-drop copiers, but it's a switchable option here.
    Also added "-v" and "-vv" arguments for verbosity control.

Any error flag
    Set a global boolean to indicate that errors were reported at any point
    during a mergeall run, for a mergeall summary line.  mergeall handles its
    own errors, but tree copies gobble them here.

Mac lib error workaround
    Ignore EINVAL error num 22 ("Invalid argument") if it is raised by
    Python's shutil.copystat().  On Mac OS X, shutil.copystat() can fail
    this way due to an error raised by Mac libraries when trying to copy
    extended attributes with chflags() from a file on a Mac filesystem drive
    (e.g, HFS+) to a file on a non-Mac filesystem drive (e.g., FAT32, exFAT).
    
    This error occurs after all content has been copied, and then only in the
    final copystat() step after it has copied times correctly, so it's safe
    to ignore here in this isolated context.  We could check to ensure that
    modtimes match too, but that seems overkill, and requires ranges for FAT.
    
    Python's shutil should probably ignore this error too, though it may be a
    Mac bug (it also occurs at the shell for a "cp -p" command, which seems
    to create the attribute nonetheless). For more details and examples,
    see docetc/miscnotes/mac-chflags-error22.txt.  This arose because Mac's
    TextEdit adds an extended attribute for encoding type to .txt files...

Unix symlinks: copy, don't follow (and FIFOs okay)
    For Unix symbolic links to both files and dirs: copy the link itself,
    instead of following it.  Else, archives with intra-archive links will
    wind up with multiple copies of the linked data.  Assumes symlinks are
    relative (or else they may not work on a different machine) and uses
    py 3.3+'s follow_links to copy extra stat info from/to links themselves.

    Windows symlinks are complex and remain untested and TBD; they should
    work with the code here as is if the link's target exists.  Also note
    that FIFO files are False for both isfile() and isdir() (and the analogous
    calls in os.stat/lstat()), so they won't be copied unintentionally here.
    For background details, see docetc/miscnotes/demo-3.0-unix-symlinks.txt.
    
################################################################################
"""

from __future__ import print_function      # Added 2.X compatibility

import os, sys, shutil, errno
from fixlongpaths import OPEN              # [3.0] or 'as open', but too obscure 
from skipcruft import filterCruftNames     # [3.0] filter out metadata files

anyErrorsReported = False                  # [3.0] for summary-report indicator

maxfileload = 1000000                      # default file-copy size parameters
blksize = 1024 * 500



def copyinfo(pathFrom, pathTo):
    """
    Copy extra metadata (e.g., modtime) from pathFrom to pathTo, in
    addition to the data itself.  Most of the action here happens in
    Python's shutil module, but must allow a spurious EINVL err #22
    in copystat() to pass for Mac OS X; see [3.0] updates above.

    Also use follow_symlinks to process links themselves, when both
    from and to are links (instead of fetching and setting info from
    and to the link targets); this arg is available in py 3.3+ only.
    """
    if float(sys.version[:3]) < 3.3:                   # [3.0] don't follow
        follow = {}                                    # not available 3.2-
    else:
        follow = dict(follow_symlinks=False)

    try:
        shutil.copystat(pathFrom, pathTo, **follow)    # [2.0] copy modtime, etc
    except OSError as why:
        if why.errno != errno.EINVAL:       # [3.0] ignore err 22 on Macs: moot
            raise                           # propagate all other errnos/excs  



def copylink(pathFrom, pathTo, copystat=True):
    """
    Copy a symbolic link instead of following it.  For links to both files
    and dirs, this copies the symlink itself (the pathname of its link) to
    a new symlink, instead of copying the data that the symlink refers to.
    See [3.0] updates above for more on this extension and its purpose.
    """
    # caller handles all exceptions
    assert os.path.islink(pathFrom)

    if os.path.exists(pathTo):               # else os.symlink() will fail
        os.remove(pathTo)                    # e.g., if modtime has changed
        
    linkPath = os.readlink(pathFrom)         # from link's pathname str
    os.symlink(linkPath, pathTo)             # store pathname as new link
    if copystat:
        copyinfo(pathFrom, PathTo)           # copy extras after content



def copyfile(pathFrom, pathTo, maxfileload=maxfileload, copystat=True):
    """
    Copy one file pathFrom to pathTo, byte for byte.
    Uses binary file modes to supress Unicode decode and endline transform.
    [2.0] Add copystat() call as default, to copy original's metadata too
    [2.0] Recode for explicit close(); old: open(wb).write(open(rb).read())
    [3.0] Use extended OPEN() to support long file pathnames on Windows
    [3.0] Allow EINVL err #22 in copystat() to pass on Macs (see above)
    [3.0] Don't check to see if pathFrom is a real file here: assumes the
          caller won't pass symlinks if they are to be copied, not followed.
    """
    fileFrom = OPEN(pathFrom, 'rb')                  # need 'b' mode for both
    fileTo   = OPEN(pathTo,   'wb')                  # [2.0] open for explicit close
    try:
        if os.path.getsize(pathFrom) <= maxfileload:
            bytesFrom = fileFrom.read()              # read small files all at once
            fileTo.write(bytesFrom)
        else:                                        # read big files in chunks
            while True:
                bytesFrom = fileFrom.read(blksize)   # get one block, less at end
                if not bytesFrom: break              # empty after last chunk
                fileTo.write(bytesFrom)
    finally:
        fileTo.close()                               # [2.0] explicit for non-CPython
        fileFrom.close()                             # except or not (or with: eibti)

    if copystat:
        copyinfo(pathFrom, PathTo)                   # copy extras after content



def copytree(dirFrom, dirTo, verbose=0, strict=False, skipcruft=False):
    """
    Copy contents of dirFrom and below to dirTo, return (files, dirs) counts.
    verbose: 1=print directories, 2=also print files, 0=print neither.
    May need to use bytes for dirnames if undecodable on other platforms.
    May need to do more file-type checking on Unix: skip links, fifos, etc.
    Py 3.5+ os.scandir() may help here, but time is dominated by file copies.

    [3.0] If strict, reraise and exit all recursive levels immediately on
    on any first exception here.  mergeall backup copies pass True to cancel
    the update or delete on a backup copy failure.  mergeall non-backup
    callers instead allow this to print a message and continue the copy.
    
    [3.0] If skipcruft, skip cruft files in dirFrom.  This was added for
    mergeall bulk copies of folders to the TO drive, but can also be used
    in other programs, and when run from a command line with "-skipcruft".

    [3.0] Copy, instead of following, any symbolic links to files and dirs
    along the way.  Else may wind up copying files and dirs more than once.
    Also recode logic to rule out FIFOs, which are neither isfile nor isdir.
    """
    fcount = dcount = 0
    itemsHere = os.listdir(dirFrom)
    if skipcruft:
        itemsHere = filterCruftNames(itemsHere)             # [3.0] ignore cruft

    for filename in itemsHere:                              # for files/dirs here
        pathFrom = os.path.join(dirFrom, filename)
        pathTo   = os.path.join(dirTo,   filename)          # extend both paths
        if not os.path.isdir(pathFrom):                     # copy simple files
            try:
                if verbose > 1: print('copying file', pathFrom, 'to', pathTo)
                copyfile(pathFrom, pathTo)
                fcount += 1
            except:
                print('**Error copying', pathFrom, 'to', pathTo, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
                anyErrorsReported = True   # [3.0] flag for summary line
                if strict: raise           # [3.0] reraise, else continue
        else:
            if verbose: print('copying dir ', pathFrom, 'to', pathTo)
            try:
                os.mkdir(pathTo)                            # make new subdir
                below = copytree(                           # recur into subdirs
                            pathFrom, pathTo,               # propagate excs up
                            verbose, strict, skipcruft)     
                fcount += below[0]                          # add subdir counts
                dcount += below[1]
                dcount += 1
            except:
                print('**Error creating', pathTo, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
                anyErrorsReported = True   # [3.0] flag for summary line
                if strict: raise           # [3.0] reraise, else continue
    return (fcount, dcount)



def getargs():
    """
    Get and verify directory name arguments, returns default None on errors.
    """
    try:
        dirFrom, dirTo = sys.argv[1], sys.argv[2]
        assert all(arg in ['-skipcruft', '-v', '-vv'] for arg in sys.argv[3:])
    except:
        print('Usage error: '
              '[py[thon]] cpall.py dirFrom dirTo [-skipcruft] [-v] [-vv]')
    else:
        skipcruft = '-skipcruft' in sys.argv
        verbose = 2 if '-vv' in sys.argv else (1 if '-v' in sys.argv else 0)
        if not os.path.isdir(dirFrom):
            print('Error: dirFrom is not a directory')
        elif not os.path.exists(dirTo):
            os.mkdir(dirTo)
            print('Note: dirTo was created')
            return (dirFrom, dirTo, skipcruft, verbose)
        else:
            print('Warning: dirTo already exists')
            if hasattr(os.path, 'samefile'):
                same = os.path.samefile(dirFrom, dirTo)
            else:
                same = os.path.abspath(dirFrom) == os.path.abspath(dirTo)
            if same:
                print('Error: dirFrom same as dirTo')
            else:
                return (dirFrom, dirTo, skipcruft, verbose)



if __name__ == '__main__':
    """
    Stand-alone/command-line mode.
    cpall is useful both standalone and as callable functions;
    see mergeall's use of the latter to compare files and trees;
    """
    # [oct16] python/platform-specific current time (secs)
    import time
    gettime = (time.perf_counter if hasattr(time, 'perf_counter') else
              (time.clock if sys.platform.startswith('win') else time.time)) 

    # parse args, run copy
    argstuple = getargs()
    if argstuple:
        dirFrom, dirTo, skipcruft, verbose = argstuple
        print('Copying...')
        
        starttime = gettime()
        fcount, dcount = copytree(dirFrom, dirTo,
                                  skipcruft=skipcruft, verbose=verbose)
        tottime = gettime() - starttime

        dcount += 1  # for the root
        print('Copied', fcount, 'files,', dcount, 'directories', end=' ')
        print('in', tottime, 'seconds')
