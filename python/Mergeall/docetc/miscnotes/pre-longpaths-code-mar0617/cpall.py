#!/usr/bin/python
# Python 3.X is recommended for trees with Unicode filenames and symlinks
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
Symlinks are always copied, not followed, to avoid redundant data copies.
Fifos and any other exotic non-file/dir types are unsupported and skipped.

--------------------------------------------------------------------------------
CHANGE LOG

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

Unix symlinks: copy, don't follow (and FIFOs are skipped)
    For Unix symbolic links to both files and dirs, always copy the link
    itself, instead of following it (i.e., copy the link's path, not the item
    it refers to).  Otherwise, archives with intra-archive links will wind up
    with multiple copies of the linked data, for both mergeall copies and
    backups.  This policy assumes symlinks are both relative and intra-archive,
    else they may not work on a different machine.

    In mergeall, the symlinks extension was coded as pretests to minimize
    impacts to existing code, and relies implictly on the fact that cpfile()
    and cptree() here were also augmented to check for and copy links up-front,
    before attempting to copy actual items.  The code here also uses py 3.3+'s
    follow_links, if present, to copy extra stat info from/to links themselves.

    Windows symlinks work with this code too, but require admin permission,
    and the portability of symlink paths between Windows and Unix is poor.
    Also note that FIFO files are False for _both_ isfile() and isdir() (and
    similar os.stat/lstat tools), so they won't be copied here unintentionally.
    For more background details, see these session logs:
    
      docetc/miscnotes/demo-3.0-unix-symlinks.txt
      docetc/miscnotes/demo-3.0-windows-symlinks.txt.
    
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
    ---------------------------------------------------------------------------
    Copy extra metadata (e.g., modtime) from pathFrom to pathTo, in
    addition to the data itself.  Most of the action here happens in
    Python's shutil module, but must allow a spurious EINVL err #22
    in copystat() to pass for Mac OS X; see [3.0] updates above.

    Also use "follow_symlinks" to process links themselves, when both
    from and to are links (instead of fetching and setting info from
    and to link targets).  In shutil, this arg is ignored for non-link
    items, and is available and used in Py 3.3 and later only.  Windows'
    os.utime() used by shutil.copystat() doesn't support this arg either,
    but shutil simply makes utime a no-op that ignores the arg and does
    not copy link modtimes (which is irrelevant for mergeall compares). 
    ---------------------------------------------------------------------------
    """
    # links, not their targets
    if float(sys.version[:3]) < 3.3:           # [3.0] don't follow links
        follow = {}                            # not available in py 3.2-
    else:                                      # ignored for nonlinks
        follow = dict(follow_symlinks=False)

    # copy modtime, etc.
    try:
        shutil.copystat(pathFrom, pathTo, **follow)
    except OSError as why:
        if why.errno != errno.EINVAL:       # [3.0] ignore err 22 on Macs: moot
            raise                           # propagate all other errnos/excs  



def copylink(pathFrom, pathTo, copystat=True, verbose=1):
    """
    ---------------------------------------------------------------------------
    Copy a symbolic link instead of following it.  For links to both files
    and dirs, this copies the symlink itself (the pathname of its link) to
    a new symlink, instead of copying the data that the symlink refers to.
    See [3.0] updates above for more on this extension and its purpose.

    Removes item at target if it's a link, else symlink() fails when target
    exists - unlike file open().write().  All other existing target types
    must be removed by the caller (e.g., mergeall removes dirs and files,
    and only ever calls this with an existing pathTo for link+link diffs).
    
    On Windows, links are type-specific.  os.symlink() gets type from the
    target if it exists (in TO, not FROM), else type defaults to file link
    unless target_is_directory=True is passed.  We need to pass this here,
    because there are multiple ways we may copy the link _before_ the dir
    when resolving a folder in mergeall.  This argument reflects the target
    in FROM, is ignored on Unix as of Py 3.3, and isn't present in Py 2.X.
    ---------------------------------------------------------------------------
    """
    # caller handles all exceptions
    assert os.path.islink(pathFrom)
    if verbose > 0:
        print('propagating symlink', pathFrom)

    # windows dir-link arg
    if (os.path.isdir(pathFrom) and          # not suported in 2.X
        sys.platform.startswith('win') and   # not okay on unix till 3.3
        int(sys.version[0]) >= 3):
        dirarg = dict(target_is_directory=True)
    else:
        dirarg ={}
                      
    # remove current link                    # lexists: link, not its target
    if os.path.lexists(pathTo):              # else os.symlink() will fail
        os.remove(pathTo)                    # e.g., if modtime has changed

    # copy linkpath over 
    linkPath = os.readlink(pathFrom)         # the from link's pathname str
    os.symlink(linkPath, pathTo, **dirarg)   # store pathname as new link
    if copystat:
        copyinfo(pathFrom, pathTo)           # copy extras after content



def copyfile(pathFrom, pathTo, maxfileload=maxfileload, copystat=True):
    """
    ---------------------------------------------------------------------------
    Copy one file pathFrom to pathTo, byte for byte.
    Uses binary file modes to supress Unicode decode and endline transform.
    [2.0] Add copystat() call as default, to copy original's metadata too.
    [2.0] Recode for explicit close(); old: open(wb).write(open(rb).read()).
    [3.0] Use extended OPEN() to support long file pathnames on Windows.
    [3.0] Allow EINVL err #22 in copystat() to pass on Macs (see above).
    [3.0] For symlinks to files or dirs, copy the link instead of following it.
    ---------------------------------------------------------------------------
    """
    if os.path.islink(pathFrom):                     # [3.0]: link to file (or dir)
        copylink(pathFrom, pathTo, copystat)         # copy link, don't follow it
        return                                       # minimize nesting
    
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
        copyinfo(pathFrom, pathTo)                   # copy extras after content



def copytree(dirFrom, dirTo, verbose=0, strict=False, skipcruft=False):
    """
    ---------------------------------------------------------------------------
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

    [3.0] For symlinks to files or dirs, copy the link instead of following
    it.  The pretest here runs only at the top-level; nested links to dirs
    are grouped with simple files during the recursive traversal to avoid
    os.mkdir.  os.path.isfile()/isdir() both return True for real items and
    links to them.  Also recode logic to rule out FIFOs, which are neither
    isfile() nor isdir(); these are not counted as errors here - ok? (TBD).
    ---------------------------------------------------------------------------
    """
    if os.path.islink(dirFrom):           # [3.0]: link to dir (or file)
        copylink(dirFrom, dirTo)          # copy link, don't follow it
        return                            # minimize nesting

    fcount = dcount = 0
    itemsHere = os.listdir(dirFrom)
    if skipcruft:
        itemsHere = filterCruftNames(itemsHere)             # [3.0] ignore cruft

    for filename in itemsHere:                              # for files/dirs here
        pathFrom = os.path.join(dirFrom, filename)
        pathTo   = os.path.join(dirTo,   filename)          # extend both paths
        
        if os.path.isfile(pathFrom) or os.path.islink(pathFrom):
            # copy simple files, and links to files and dirs
            if verbose > 1: print('copying file', pathFrom, 'to', pathTo)
            try:
                copyfile(pathFrom, pathTo)                  # [3.0] file or link
                fcount += 1
            except:
                print('**Error copying', pathFrom, 'to', pathTo, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
                anyErrorsReported = True   # [3.0] flag for summary line
                if strict: raise           # [3.0] reraise, else continue

        elif os.path.isdir(pathFrom):
            # copy entire folders: actual dirs, not links to them
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

        else:
            # fifo, or other non-file item: punt
            print('**Unsupported file type not copied:', pathFrom)
            
    return (fcount, dcount)



def getargs():
    """
    ---------------------------------------------------------------------------
    Get and verify directory name arguments, returns default None on errors.
    ---------------------------------------------------------------------------
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
    ---------------------------------------------------------------------------
    Stand-alone/command-line mode.
    cpall is useful both standalone and as callable functions;
    see mergeall's use of the latter to compare files and trees;
    ---------------------------------------------------------------------------
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
