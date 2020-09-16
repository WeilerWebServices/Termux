#!/usr/bin/python
"""
================================================================================
ziptools.py (part of the mergeall system [3.0]) [Python 3.X or 2.X]
Author:  M. Lutz (learning-python.com), copyright March, 2017
License: Provided freely but with no warranties of any kind.

Tools to create and extract zipfiles containing a set of files, folders, and
symbolic links.  All functions here are callable, but the main top-level entry
points are these two (see ahead for more on their arguments):

  createzipfile(zipname, [addnames],
                storedirs=True, cruftpatts={}, atlinks=False, trace=print)
                     
  extractzipfile(zipname, pathto='.',
                 nofixlinks=False, trace=print)

See also scripts zip-create.py and zip-extract.py for command-line clients,
and zipcruft.cruft_skip_keep for a default "cruftpatts" cruft-file definition. 

This mostly extends Python's zipfile module with top-level convenience tools
that add some important missing features:

 * For folders, adds the folder's entire tree to the zipfile automatically
 * For zipfile creation, filters out cruft (hidden metadata) files on request
 * For zipfile extracts, retains original modtimes for files, folders, links
 * For symlinks, adds/recreates the link itself to/from zipfiles, by default 

CRUFT HANDLING:

This script sidesteps other tools' issues with ".*" cruft files (metadata that
is normally hidden): by default, they are not silently/implicitly omitted in
zips here for completeness, but can be omitted by passing a filename-patterns
definition structure to the optional "cruftpatts" argument.

See zipcruft.py for pattern defaults to import and pass, and zipfile-create.py
for more background.  Most end-user zips should skip cruft files (see mergeall:
cruft can be a major issue on Mac OS X in data to be transferred elsewhere).

SYMLINKS SUPPORT:

This package also supports adding symlinks (symbolic links) to and extracting
them from zip archives, on both Unix and Windows with Python 3.X, but only on
Unix with Python 2.X.  Windows requires admin permissions and NTFS filesystem
destinations to create symlinks from a zip file; Unix does not.

The underlying Python zipfile module doesn't support symlinks directly today,
short of employing the very low-level magic used in ziptools_symlinks.py here,
and there is an open bug report to improve this:

    https://bugs.python.org/issue18595
    https://mail.python.org/pipermail/python-list/2005-June/322179.html
    https://duckduckgo.com/?q=python+zipfile+symlink

Symlinks customize messages with "~" characters in creation and "(Link)"
prefixes in extraction, because they are a special-enough case to call out in
logs, and may require special permission and handling to unzip and use on
Windows.  For example, link creation and extraction messages are as follows:

    Adding  link  ~folder test1/dirlink   # create message
    (Link) Extracted test1/dirlink        # extract message

By default, zipfile creation zips links themselves verbatim, not the items they
refer to.  Pass True to the "atlinks" function argument to instead follow links
and zip the items they refer to.  Unzipping restores whatever was zipped.

When links are copied verbatim, extracts adjust the text of a link's path to
use the hosting platform's separators - '\' for Windows and '/ for Unix.  This
provides some degree of link portability between Unix and Windows, but is
switchable with "nofixlinks" because it may not be desirable in all contexts
(e.g., when unzipping to a drive to be used elsewhere).  Symlinks will still
be nonportable if they contain other platform-specific syntax, such as Windows
drive letters or UNC paths, or use asbolute references to extra-archive items.

When "atlinks" is used to follow links and copy itens they refer to, recursive
links are detected on platforms and Pythons that support stat objects' st_ino
(a.k.a. indode) unique directory identifiers.  This includes all Unix contexts,
and Windows as of Python 3.2 (other contexts fails on path or memory errors).
Recursive links are copied themselves, verbatim, to avoid loops and errors.

Besides symlinks, FIFOs and other exotic items are always skipped and ignored.
================================================================================
"""

from __future__ import print_function         # py 2.X
import os, sys, time, shutil
from zipfile import ZipFile, ZIP_DEFLATED     # stdlib base support
from fnmatch import fnmatchcase               # non-case-mapping version

# default cruft-file patterns, import here for importers
try:
    from zipcruft import cruft_skip_keep
except ImportError:
    from .zipcruft import cruft_skip_keep     # if pkg used elsewhere in py3.X

# a major workaround: split this narly code off to a module...
try:
    from zipsymlinks import addSymlink, isSymlink, extractSymlink
except ImportError:
    from .zipsymlinks import addSymlink, isSymlink, extractSymlink   # ditto
   

#===============================================================================

def tryrmtree(folder, trace=print):
    """
    Utility: remove a folder by pathname if needed before unzipping to it.
    Python's shutil.rmtree() can sometimes fail on Windows with a "directory
    not empty" error, even though the dir _is_ empty when inspected after
    the error, and running again usually fixes the problem (deletes the
    folder successfully).  Bizarre, yes?  See the rmtreeworkaround() onerror
    handler in mergeall's backup.py for explanations and fixes.  rmtree()
    can also fail on read-only files, but this is likely intended by users.
    """

    if os.path.exists(folder):
        trace('Removing', folder)
        try:
            if os.path.islink(folder):
                os.remove(folder)
            else:
                shutil.rmtree(folder)
        except Exception as why:
            print('shutil.rmtree (or os.remove) failed:', why)
            input('Try running again, and press Enter to exit.')
            sys.exit(1)


#===============================================================================

def isCruft(filename, cruftpatts):
    """
    Identify cruft by matching a file or folder basename "filename", to
    the patterns in dict "cruftpatts", using the fnmatch stdib module.
    Returns True if filename is a cruft item, which means it matches any
    pattern on "skip" list, and does not match any pattern on "keep" list,
    either of which can be empty to produce False results from any().
    
    No files are cruft if the entire patterns dict is empty (the default).
    See createzipfile() ahead for more on the "cruftpatts" dictionary.
    """
    return (cruftpatts
            and
            any(fnmatchcase(filename, patt) for patt in cruftpatts['skip'])
            and not
            any(fnmatchcase(filename, patt) for patt in cruftpatts['keep']))


#===============================================================================

def isRecursiveLink(dirpath):
    """
    Use inodes to identify each part of path leading to a link,
    on platforms that support inodes.  All Unix/Posix do, though
    Windows Python doesn't until till 3.2 - if absent, allow
    other error to occur (there are not many more options here;
    on all Windows, os.path.realpath() is just os.path.abspath()).
    
    This is linearly slow in the length of paths to dir links,
    but links are exceedingly rare, "atlinks" use in ziptools
    may be rarer, and recursive links are arguably invalid data.
    Recursion may be better than os.walk when path history is
    required, though this incurs overheads only if needed as is.
    """
    trace = lambda * args: None                 # or print to watch

    # called iff atlinks: following links
    if (not os.path.islink(dirpath) or          # dir item not a link?
        os.stat(os.getcwd()).st_ino == 0):      # platform has no inodes?
        return False                            # moot, or hope for best 
    else:
        # collect inode ids for each path extension except last
        inodes = []
        path = []
        parts = dirpath.split(os.sep)[:-1]      # all but link at end
        while parts:
            trace(path, parts)
            path    += [parts[0]]               # add next path part
            parts    = parts[1:]                # expand, fetch inode
            thisext  = os.sep.join(path)
            thispath = os.path.abspath(thisext)
            inodes.append(os.stat(thispath).st_ino)

        # recursive if points to item with same inode as any item in path               
        linkpath = os.path.abspath(dirpath)
        trace(inodes, os.stat(linkpath).st_ino)
        return os.stat(linkpath).st_ino in inodes


def isRecursiveLink0(dirpath, visited):
    """
    ABANDONED, UNUSED: realpath() cannot be used portably,
    because it is just abspath() on Windows Python (but why?).
    
    Trap recursive links to own parent dir, but allow multiple
    non-recursive link visits.  The logic here is as follows:
    If we've reached a link that leads to a path we've already
    reached from a link AND we formerly reached that path from
    a link located at a path that is a prefix of the new link's
    path, then the new link must be recursive.  No, really...
    Catches link at visit #2, but avoids overhead for non-links.
    """
    # called iff atlinks: following links
    if not os.path.islink(dirpath):
        # skip non-links
        return False                                      # don't note path
    else:
        # check links history
        realpath = os.path.realpath(dirpath)              # dereference, abs
        #print('\t', dirpath, '\n\t', realpath, sep='')
        if (realpath in visited and
            any(dirpath.startswith(prior) for prior in visited[realpath])):
            return True          
        else:
            # record this link's visit
            visited[realpath] = visited.get(realpath, []) # add first or next
            visited[realpath].append(dirpath)
            return False


#===============================================================================

def addEntireDir(rootdirname,      # pathname of directory to add
                 zipfile,          # open zipfile.Zipfile object to add to 
                 storedirs=True,   # record dirs explicitly in zipfile?
                 cruftpatts={},    # cruft files skip/keep, or {}=do not skip
                 atlinks=False,    # zip items referenced instead of links?
                 trace=print):     # trace message router (or lambda *x: None)
    """
    Add the full folder at rootdirname to zipfile by adding all its parts.
    Python's zipfile module has extractall(), but nothing like an addall().
    
    Note that the walker's files list is really all non-dirs (which
    may include non-file items that should likely be excluded on some
    platforms), and non-link subdirs are always reached by the walker.
    Dir links are returned in subdir list, but not followed by default.

    Dirs (a.k.a. folders) don't always need to be written to the
    zipfile themselves, because extracts add all of a file's dirs if
    needed (with os.makedirs(), in Python's zipfile module).  Really,
    zipfiles don't have folders per se - just individual items with
    pathnames and metadata.

    However, dirs MUST be added to the zipfile themselves to either:
    1) Retain folders that are empty in the original.
    2) Retain the original modtimes of folders (see extract below).

    When added directly, the zipfile records folders as zero-length
    items with a trailing "/", and recreates the folder on extracts
    as needed.  Disable folder writes with "storedirs" if this proves
    incompatible with other tools (but it works fine with WinZip).

    If atlinks=True, copies items links reference not links themselves,
    and steps into subdirs referenced by links; else, copies links and
    doesn't folow them.  For links to dirs, os.walk yields the name of
    the link (not the dir it references), and this is the name under
    which the linked subdir is stored in the zip (hence, dirs can be
    present in multiple tree locations).  For example, if link 'python'
    reference dir 'python3', the latter is stored under the former name.

    Also traps recursive link paths to avoid running into memory errors
    or path limits, by using stat object st_ino unique identifiers to
    discern loops from valid dir repeats.  For more details on links in
    os.walk(), see docetc/symlinks/demo*.txt
    """      

    # walker follows dir links iff atlinks
    treewalker = os.walk(rootdirname, followlinks=atlinks)
    
    for (dirhere, subdirshere, fileshere) in treewalker:
            
        # handle this dir
        if storedirs and dirhere != '.':
            trace('Adding folder', dirhere)
            zipfile.write(dirhere)                            # add folders too

        # handle subdirs here
        for subname in subdirshere.copy():
            if isCruft(subname, cruftpatts):                  # skip cruft dirs
                trace('--Skipped cruft dir', subname)
                subdirshere.remove(subname)                   # prune the walk

            else:
                dirpath = os.path.join(dirhere, subname)
                if atlinks and isRecursiveLink(dirpath):      # link to parent?
                    trace('Recursive link copied', dirpath)
                    addSymlink(dirpath, zipfile)              # copy link instead
                    subdirshere.remove(subname)               # prune the walk

                elif os.path.islink(dirpath) and not atlinks: # walk won't follow
                    trace('Adding  link  ~folder', dirpath)   # but add link path
                    addSymlink(dirpath, zipfile)

                else: # non-link dir or following links
                    pass                                      # follow the link

        # handle non-dirs here
        for filename in fileshere:
            if isCruft(filename, cruftpatts):                 # skip cruft files
                trace('--Skipped cruft file', filename)

            else:
                filepath = os.path.join(dirhere, filename)
                if os.path.islink(filepath) and not atlinks:  # add link paths
                    trace('Adding  link  ~file', filepath)    # else follow links
                    addSymlink(filepath, zipfile)

                elif os.path.isfile(filepath):                # add files/paths
                    trace('Adding  file ', filepath)
                    zipfile.write(filepath)

                else: # fifo, etc.                            # skip oddities
                    trace('--Skipped unknown type:', filepath)


#===============================================================================

def createzipfile(zipname,          # pathname of new zipfile to create
                  addnames,         # sequence of pathnames of items to add
                  storedirs=True,   # record dirs explicitly in zipfile?
                  cruftpatts={},    # cruft files skip/keep, or {}=do not skip
                  atlinks=False,    # zip items referenced instead of links?
                  trace=print):     # trace message router (or lambda *x: None)
    """
    Make a zipfile at path "zipname" and add to it all folders and files
    in "addnames".  Pass "trace=(lambda *args: None)" for silent operation.
    See function addEntireDir() above for details on "storedirs" (its
    default is normally desired), and ahead here for "cruftpatts" (its
    default means all cruft files and folders are included in the zip).
    
    This always uses ZIP_DEFLATED, the usual zip compression scheme
    (ZIP_STORED is uncompressed).  Python's base zipfile module used
    here supports Unicode filenames automatically (encoded per UTF8).

    By default, all files and folders are added to the zip.  This is by
    design, because this code was written as a workaround for WinZip's
    silent file omissions.  As an option, though, this function will
    instead skip normally-hidden cruft files and folders (e.g., ".*")
    much like mergeall, so they are not added to zips used to upload
    websites or otherwise distribute or transfer programs and data.  To
    enable cruft skipping, pass to cruftpatts a dictionary of this form:
    
        {'skip': ['pattern', ...],
         'keep': ['pattern', ...]}

    to define fnmatch filename patterns for both items to be skipped, and
    items to be kept despite matching a skip pattern (e.g., ".htaccess").
    If no dictionary is passed, all items are added to the zip; if either
    list is empty, it fails to match any file.  See zipcruft.py for more
    details, and customizable presets to import and pass to cruftpatts.

    Also by default, if symbolic links are present, they are added to the
    zip themselves - not the items they reference.  Pass atlinks=True to
    instead follow links and zip the items they reference.  This also 
    traps recursive links if atlinks=True, where inodes are supported.
    """

    trace('Zipping', addnames, 'to', zipname)
    if cruftpatts:
        trace('Cruft patterns:', cruftpatts)
        
    zipfile = ZipFile(zipname, mode='w', compression=ZIP_DEFLATED)
    for addname in addnames:
        if (addname not in ['.', '..'] and
            isCruft(os.path.basename(addname), cruftpatts)):
            print('--Skipped cruft item', addname)

        elif os.path.islink(addname) and not atlinks:
            trace('Adding  link  ~item', filepath)
            addSymlink(addname, zipfile) 

        elif os.path.isfile(addname):
            trace('Adding  file ', addname)
            zipfile.write(addname)

        elif os.path.isdir(addname):
            addEntireDir(addname, zipfile,
                         storedirs, cruftpatts, atlinks, trace)

        else: # fifo, etc.
            trace('--Skipped unknown type:', addname)
            
    zipfile.close()


#===============================================================================

def extractzipfile(zipname,            # pathname of zipfile to extract from
                   pathto='.',         # pathname of folder to extract to
                   nofixlinks=False,   # do not translate symlink separators? 
                   trace=print):       # trace router (or lambda *x: None)
    """
    Unzip an entire zipfile at zipname to pathto, which is created if
    it doesn't exist.  Note that compression is passed for writing, but 
    is auto-detected for reading here.  Pass "trace=(lambda *args: None)"
    for silent operation.  This does no cruft-file skipping, as it is
    assumed to operate in tandem with the zip creation tools here; see
    mergeall's nuke-cruft-files.py to remove cruft in other tools' zips.

    At least through 3.5, Python's zipfile library module does record
    the original files' modification times in zipfiles it creates, but
    does NOT retain files' original modification time when extracting:
    their modification times are set to unzip time.  This is clearly a
    bug, which will hopefully be addressed soon (a similar issue for
    permissions is posted).

    The workaround here manually propagates the files' original mod
    times in the zip as a post-extract step.  It's more code than an
    extractall(pathto), but this version works, and allows extracted
    files to be listed individually.
    
    See this file's main dosctring for details on symlink support here;
    links and their paths are made portable between Unix and Windows by
    translating their path separators to the hosting platform's scheme.
    but "nofixlinks can be used to suppress path separator replacement.

    SUBTLETY: Py docs suggest that os.utime() doesn't work for folders'
    modtime on Windows, but it does.  Still, a simple extract would
    change all non-empty folders' modtimes to the unzip time, just by
    virtue of writing files into those folders.  This isn't an issue for
    mergeall: only files compare by modtime, and dirs are just structural.
    The issue is avoided here, though, by resetting folder modtimes to
    their original values in the zipfile AFTER all files have been written.

    The net effect: assuming the zip records folders as individual items
    (see create above), this preserves original modtimes for BOTH files
    and folders across zips, unlike some other zip tools.  Cut-and-paste,
    drag-and-drop, and xcopy can also change folder modtimes on Windows,
    so be sure to zip folders that have not been copied this way if you
    wish to test this script's folder modtime retention.

    ALSO SUBTLE: the written-to "pathname" returned by zipfile.extract()
    may not be just os.path.join(pathto, filename).  extract() also removes
    any leading slashes, Windows drive and UNC network names, and ".." 
    up-references in "filename" before appending it to "pathto", to ensure
    that the item is stored relative to "pathto" regardless of any absolute,
    drive- or server-rooted, or parent-relative names in the zipfile's items.
    zipfile.write() drops all but "..", which zipfile.extract() discards.
    The local extractSymlink() behaves like zipfile.extract() in this regard.
    """

    trace('Unzipping from', zipname, 'to', pathto)
    dirtimes = []
    
    zipfile = ZipFile(zipname, mode='r')
    for zipinfo in zipfile.infolist():                    # all items in zip

        if isSymlink(zipinfo):
            # read/save link path
            trace('(Link)', end=' ')
            pathname = extractSymlink(zipinfo, pathto, zipfile, nofixlinks)
        else:
            # create file or dir
            pathname = zipfile.extract(zipinfo, pathto) 

        filename = zipinfo.filename                       # item's path in zip            
        trace('Extracted %s\n\t\t=> %s' % (filename, pathname))

        # propagate mod time to files, links (and dirs on some platforms)
        origtime = zipinfo.date_time                      # zip's 6-tuple
        datetime = time.mktime(origtime + (0, 0, -1))     # 9-tuple=>float

        if os.path.islink(pathname):
            # reset mtime of link itself where supported
            # but not on Windows or Py3.2-: keep now time
            if (hasattr(os, 'supports_follow_symlinks') and
                os.utime in os.supports_follow_symlinks):
                os.utime(pathname, (datetime, datetime), follow_symlinks=False)

        elif os.path.isfile(pathname):
            # reset (non-link) file mtime now
            os.utime(pathname, (datetime, datetime))      # dest time = src time   

        elif os.path.isdir(pathname):
            # defer (non-link) dir till after add files
            dirtimes.append((pathname, datetime))         # where supported

        else:
            assert False, 'Unknown type extracted'        # should never happen

    # reset (non-link) dir modtimes now, post file adds
    for (pathname, datetime) in dirtimes:
        try:
            os.utime(pathname, (datetime, datetime))      # reset dir mtime now
        except:
            trace('Error settting directory times')       # ok on Windows/Unix

    zipfile.close()


#===============================================================================

if __name__ == '__main__':
    """
    Self-test, run in script's folder (and edit me: your context may vary).
    Makes a zip file, unzips it, and compares results to original data.
    See zip-create.py, zip-extract.py, zip-list.py for command-line clients.
    """
    
    # default cruft-file patterns
    from zipcruft import cruft_skip_keep    # or a custom def, or {}=no skip
    
    def announce(*args):
        print('\n\n****', *args, '****\n')

    #----------------------------------------------------------------
    # configure test run parameters
    #----------------------------------------------------------------

    # map test to test subdir names
    skipcruft = len(sys.argv) > 1    # any cmdline arg?
    platform  = sys.platform         # win32, darwin, or linux
    
    cruftsubdir = 'skipcruft' if skipcruft else 'withcruft'
    platsubdir  = dict(win32='Windows', darwin='MacOSX', linux='Linux')[platform]

    # make+use folder here to create and extract a zipfile  
    testsubdir = os.path.join('selftest', platsubdir, cruftsubdir)
    if not os.path.exists(testsubdir):              # selftest\Windows\withcruft
        os.makedirs(testsubdir)                     # selftest/MacOSX/skipcruft
    zipto = os.path.join(testsubdir, 'ziptest.zip') # plus the zip file target

    # use test data dirs in '..' parent [**EDIT ME**]
    origin  = '..'
    folders = ['test1', 'test2']                    # i.e., [../test1, ../test2]
    sources = [(origin + os.sep + folder) for folder in folders]

    #----------------------------------------------------------------
    # zip original source dirs to subdir file
    #----------------------------------------------------------------
    
    announce('CREATING')
    if not skipcruft:                     # any cmdline arg? use cruft patts
        createzipfile(zipto, sources)     # else keep cruft: use {} default
    else:
        createzipfile(zipto, sources, cruftpatts=cruft_skip_keep)    

    #----------------------------------------------------------------
    # unzip subdir file to subdir dirs, cleaning first if needed
    #----------------------------------------------------------------
    
    announce('EXTRACTING')
    for folder in folders:
        tryrmtree(os.path.join(testsubdir, folder))     # clean extract targets
    extractzipfile(zipto, testsubdir)                   # extract in testsubdir 

    #----------------------------------------------------------------
    # compare zipped+unzipped subdir dirs to original source dirs
    #----------------------------------------------------------------

    # use mergeall's diff and merge for validation [EDIT ME]
    diffallpath  = os.path.join('..', '..', 'diffall.py')
    mergeallpath = os.path.join('..', '..', 'mergeall.py')
    
    for folder in folders:
        announce('COMPARING MODTIMES:', folder)
        pipe = os.popen('%s %s %s %s -report' %
                        (sys.executable, mergeallpath,
                         os.path.join(origin, folder),
                         os.path.join(testsubdir, folder)))
        for line in pipe: 
            print(line, end='')

    for folder in folders:
        announce('COMPARING CONTENT:', folder)
        pipe = os.popen('%s %s %s %s' %
                        (sys.executable, diffallpath,
                         os.path.join(origin, folder),
                         os.path.join(testsubdir, folder)))
        for line in pipe: 
            print(line, end='')

    if sys.platform.startswith('win'):
        if sys.version[0] == '2':
            input = raw_input 
        input('Press Enter to exit.')  # stay up if clicked
