#!/usr/bin/python
"""
================================================================================
ziptools.py (part of the mergeall system [3.0]) [Python 3.X or 2.X]
Author:  M. Lutz (learning-python.com), copyright June 2017
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
All of these have additional documentation omitted here.

This ziptools package mostly extends Python's zipfile module with top-level
convenience tools that add some important missing features:

 * For folders, adds the folder's entire tree to the zipfile automatically
 * For zipfile creation, filters out cruft (hidden metadata) files on request
 * For zipfile extracts, retains original modtimes for files, folders, links
 * For symlinks, adds/recreates the link itself to/from zipfiles, by default
 * For Windows, supports long pathnames by lifting the normal length limit

CRUFT HANDLING:

This script sidesteps other tools' issues with ".*" cruft files (metadata that
is normally hidden): by default, they are not silently/implicitly omitted in
zips here for completeness, but can be omitted by passing a filename-patterns
definition structure to the optional "cruftpatts" argument.

See zipcruft.py for pattern defaults to import and pass, and zipfile-create.py
for more background.  Most end-user zips should skip cruft files (see mergeall:
cruft can be a major issue on Mac OS X in data to be transferred elsewhere).

WINDOWS LONG PATHS:

This program, like mergeall, supports pathnames that are not restriced to the
usual 260/248-character lenght limit on all versions Windows.  To lift the
limit, pathnames are automatically prefixed with '\\?\' as needed, both when
adding to and extracting from archives.  This allows archives created on
platforms without such limits to be unzipped and rezipped on Windows machines.

The \\?\-prefix magic is internal, and hidden from the user as much as possible.
It also makes paths absolute, but relative paths are still fully supported:
absolute paths are not propagated to the archive when creating, and impact
only output messages on Windows when extracting (where we strip the prefix
and try to map back to relative as needed to keep the messages coherent).

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

When "atlinks" is used to follow links and copy items they refer to, recursive
links are detected on platforms and Pythons that support stat objects' st_ino
(a.k.a. indode) unique directory identifiers.  This includes all Unix contexts,
and Windows as of Python 3.2 (other contexts fails on path or memory errors).
Recursive links are copied themselves, verbatim, to avoid loops and errors.

Besides symlinks, FIFOs and other exotic items are always skipped and ignored;
items with system state can't be transferred in a zipfile (or mergeall mirror).
================================================================================
"""


from __future__ import print_function         # py 2.X compatibility

import os, sys, time, shutil
from zipfile import ZipFile, ZIP_DEFLATED     # stdlib base support
from fnmatch import fnmatchcase               # non-case-mapping version

# nested package so same if used as main script or package in py3.X

# default cruft-file patterns, import here for importers (or {}=don't skip)
from .zipcruft import cruft_skip_keep

# major workaround to support links: split this narly code off to a module...
from .zipsymlinks import addSymlink, isSymlink, extractSymlink

# also major: fix any too-long Windows paths on archive adds and extracts
from .ziplongpaths import FWP, UFWP



#===============================================================================

 
def tryrmtree(folder, trace=print):
    """
    Utility: remove a folder by pathname if needed before unzipping to it.
    Optionally run by zip-extract.py in interactive mode, but not by the
    base extactzipfile() function here: manually clean targets as needed.

    Python's shutil.rmtree() can sometimes fail on Windows with a "directory
    not empty" error, even though the dir _is_ empty when inspected after
    the error, and running again usually fixes the problem (deletes the
    folder successfully).  Bizarre, yes?  See the rmtreeworkaround() onerror
    handler in mergeall's backup.py for explanations and fixes.  rmtree()
    can also fail on read-only files, but this is likely intended by users.
    """

    if os.path.exists(FWP(folder)):
        trace('Removing', folder)
        try:
            if os.path.islink(FWP(folder)):
                os.remove(FWP(folder))
            else:
                shutil.rmtree(FWP(folder, force=True))    # recurs: always \\?\
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
    may be rarer, and recursive links are arguably-invalid data.
    Recursion may be better than os.walk when path history is
    required, though this incurs overheads only if needed as is.
    
    dirpath does not have a \\?\ Windows long-path prefix here;
    FWP adds one and also calls abspath() redundantly - but only
    on Windows, and we need abspath() on other platforms too.
    """
    trace = lambda * args: None                 # or print to watch

    # called iff atlinks: following links
    if (not os.path.islink(FWP(dirpath)) or     # dir item not a link?
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
            inodes.append(os.stat(FWP(thispath)).st_ino)

        # recursive if points to item with same inode as any item in path               
        linkpath = os.path.abspath(dirpath)
        trace(inodes, os.stat(FWP(linkpath)).st_ino)
        return os.stat(FWP(linkpath)).st_ino in inodes


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


def addEntireDir(rootdirname,      # pathname of directory to add (rel or abs)
                 zipfile,          # open zipfile.Zipfile object to add to 
                 storedirs=True,   # record dirs explicitly in zipfile?
                 cruftpatts={},    # cruft files skip/keep, or {}=do not skip
                 atlinks=False,    # zip items referenced instead of links?
                 trace=print):     # trace message router (or lambda *x: None)
    """
    -----------------------------------------------------------------------
    Add the full folder at rootdirname to zipfile by adding all its parts.
    Python's zipfile module has extractall(), but nothing like an addall(). 
    See createzipfile() for more docs on some of this function's utility.

    ADDING DIRS: Dirs (a.k.a. folders) don't always need to be written to
    the zipfile themselves, because extracts add all of a file's dirs if
    needed (with os.makedirs(), in Python's zipfile module and the local
    zipsymlinks module).  Really, zipfiles don't have folders per se -
    just individual items with pathnames and metadata.

    However, dirs MUST be added to the zipfile themselves to either:
    1) Retain folders that are empty in the original.
    2) Retain the original modtimes of folders (see extract below).

    When added directly, the zipfile records folders as zero-length
    items with a trailing "/", and recreates the folder on extracts
    as needed.  Disable folder writes with "storedirs" if this proves
    incompatible with other tools (but it works fine with WinZip).

    Note that the os.walker's files list is really all non-dirs (which
    may include non-file items that should likely be excluded on some
    platforms), and non-link subdirs are always reached by the walker.
    Dir links are returned in subdir list, but not followed by default.
    [Update: per ahead, os.walk() was later replaced with an explicit 
    recursion, coding which visits directories more directly.]

    SYMLINKS: If atlinks=True, copies items links reference not links
    themselves, and steps into subdirs referenced by links; else, copies
    links and doesn't follow them.  For links to dirs, os.walk yields the
    name of the link (not the dir it references), and this is the name
    under which the linked subdir is stored in the zip (hence, dirs can be
    present in multiple tree locations).  For example, if link 'python'
    references dir 'python3', the latter is stored under the former name.
    [Update: the non-os.walk() recoding per below behaves this same way.]

    Also traps recursive link paths to avoid running into memory errors
    or path limits, by using stat object st_ino unique identifiers to
    discern loops from valid dir repeats, where inode ids are supported.
    For more on recursive links detection, see isRecursiveLink() above.
    For more details on links in os.walk(), see docetc/symlinks/demo*.txt.

    LONG PATHS: Windows long paths are handled by prefixing all file-tool
    call paths with '\\?' and maing them absolute, and passing these to
    zipfile and zipsymlink tools for us in file-tool calls.  Names without
    \\?\ or absolute mapping are passed for use in the archive itself; this
    is required to support relative paths in the archive itself -- if not
    passed, archive names are created from filenames by running filenames
    though os.path.splitdrive() which drops the \\?\, but this does not
    translate from absolute back to relative (when users pass relative).

    This also required replacing a former os.walk() coding with manual
    recursion.  os.walk() required the root to have a just-in-case FWP()
    prefix to support arbitrary depth; which made os.walk() yield dirs
    that were always \\?\-prefixed and absolute; which in turn made all
    paths absolute in the zip archive.  Supporting relative zip paths
    AND long-paths requires either manual recursion (used here) or an
    os.walk() coding with abs->rel mapping (which is possible, but may
    be preclusive: see the message display code in the extract ahead).

    Nit: the explicit-recursion recoding changes the order in which items
    are visited and added - it's now alphabetical per level on Mac OS X,
    instead of files-then-dirs (roughly).  This order is different but
    completely arbitrary: it impacts the order of messages output, but
    not the content or utility of the archive zipfile generated.  For
    the prior os.walk() variant, see ../docetc/longpaths/prior-code.

    Also nit: due to the non-recursive recoding, links that are invalid 
    (do not point to an existing file or dir) are now an explicit case
    here.  Specifically, links to both nonexistent items and non-file/dir
    items are added to the zipfile, despite their rareness, and even if 
    "-atlinks" follow-links mode is used and the referent cannot be added. 
    This is done in part because mergeall and cpall propagate such links
    too, but also because programs should never silently drop content for
    you: invalid links may have valid uses, and may refer to items present
    on another machine.  The former os.walk()-based version added such 
    links just because that call returns dirs and non-dirs, and invalid
    links appear in the latter. 

    Also also nit: more clearly a win, the new coding reports full paths 
    to cruft items; it's difficult to identify drops from basenames alone.
    See folder _algorithms here for alternative codings for this function.
    -----------------------------------------------------------------------
    """

    # 
    # handle this dir
    #
    if storedirs and rootdirname != '.':
        # add folders too
        trace('Adding folder', rootdirname)  
        zipfile.write(filename=FWP(rootdirname),         # for file tools
                      arcname=rootdirname)               # not \\?\ + abs

    # 
    # handle items here
    #
    for itemname in os.listdir(FWP(rootdirname)):        # list fixed win path
        itempath = os.path.join(rootdirname, itemname)   # extend provided path
        
        # 
        # handle subdirs (and links to them)
        #
        if os.path.isdir(FWP(itempath)):
            if isCruft(itemname, cruftpatts):            # match name, not path
                # skip cruft dirs
                trace('--Skipped cruft dir', itempath)

            elif atlinks:
                # following links
                if isRecursiveLink(itempath):
                    # links to a parent: copy dir link instead
                    trace('Recursive link copied', itempath)
                    addSymlink(filepath=FWP(itempath),         # for file tools
                               zippath=itempath,               # not \\?\ + abs
                               zipfile=zipfile)                # adds link path
                else:
                    # recur into dir or link
                    addEntireDir(itempath, zipfile,     
                                 storedirs, cruftpatts, atlinks, trace)                    

            else:
                # not following links
                if os.path.islink(FWP(itempath)):
                    # copy dir link
                    trace('Adding  link  ~folder', itempath)  
                    addSymlink(filepath=FWP(itempath),         # for file tools
                               zippath=itempath,               # name in archive
                               zipfile=zipfile)               
                else:
                    # recur into dir
                    addEntireDir(itempath, zipfile,     
                                 storedirs, cruftpatts, atlinks, trace)                    

        # 
        # handle files (and links to them)
        # 
        elif os.path.isfile(FWP(itempath)):
            if isCruft(itemname, cruftpatts):
                # skip cruft files
                trace('--Skipped cruft file', itempath)

            elif atlinks:
                # following links: follow? + add
                trace('Adding  file ', itempath)
                zipfile.write(filename=FWP(itempath),        # for file tools
                              arcname=itempath)              # not \\?\ + abs

            else:
                # not following links
                if os.path.islink(FWP(itempath)):
                    # copy file link
                    trace('Adding  link  ~file', itempath)   
                    addSymlink(filepath=FWP(itempath),       # for file tools
                               zippath=itempath,             # name in archive
                               zipfile=zipfile)

                else:
                    # add simple file
                    trace('Adding  file ', itempath)
                    zipfile.write(filename=FWP(itempath),    # for file tools
                                  arcname=itempath)          # name in archive

        #
        # handle non-file/dir links (to nonexistents or oddities)
        #
        elif os.path.islink(FWP(itempath)):
            if isCruft(itemname, cruftpatts):
                # skip cruft non-file/dir links
                trace('--Skipped cruft link', itempath)

            else:
                # copy link to other: atlinks or not
                trace('Adding  link  ~unknown', itempath)   
                addSymlink(filepath=FWP(itempath),           # for file tools
                           zippath=itempath,                 # name in archive
                           zipfile=zipfile)

        #
        # handle oddities (not links to them)
        #
        else:
            # ignore cruft: not adding this
            trace('--Skipped unknown type:', itempath)       # skip fifos, etc.



#===============================================================================


def createzipfile(zipname,          # pathname of new zipfile to create
                  addnames,         # sequence of pathnames of items to add
                  storedirs=True,   # record dirs explicitly in zipfile?
                  cruftpatts={},    # cruft files skip/keep, or {}=do not skip
                  atlinks=False,    # zip items referenced instead of links?
                  trace=print):     # trace message router (or lambda *x: None)
    """
    -----------------------------------------------------------------------
    Make a zipfile at path "zipname" and add to it all folders and files
    in "addnames".  Its relative or absolute pathnames are propagated to
    the zipfile, to be used as path suffix when extracting to a target dir.
    See extactzipfile(), ../zip-create.py, and ../zip-extract.py for more
    docs on the use of relative and absolute pathnames for zip sources.

    Pass "trace=(lambda *args: None)" for silent operation.  See function
    addEntireDir() above for details on "storedirs" (its default is normally
    desired), and ahead here for "cruftpatts" and "atlinks" (their defaults
    include all cruft files and folders in the zip, and copy links instead
    of the items they reference, respectively).
    
    This always uses ZIP_DEFLATED, the "usual" zip compression scheme,
    and the only one supported in Python 2.X (ZIP_STORED is uncompressed).
    Python's base zipfile module used here supports Unicode filenames 
    automatically (encoded per UTF8).

    CRUFT: By default, all files and folders are added to the zip.  This is
    by design, because this code was written as a workaround for WinZip's
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
    details, and customizable presets to import and pass to cruftpatts
    (the default is available as "cruft_skip_keep" from this module too).

    SYMLINKS: Also by default, if symbolic links are present, they are added
    to the zip themselves - not the items they reference.  Pass atlinks=True
    to instead follow links and zip the items they reference.  This also 
    traps recursive links if atlinks=True, where inodes are supported; see
    isRecursiveLink() above for more details.

    LARGE FILES: allowZip64=True supports files of size > 2G with ZIP64 
    extensions, that are supported unevenly in other tools, but work fine
    with the create and extract tools here.  It's True by default in 
    Python 3.4+ -- only; a False would prohibit large files altogether,
    which avoids "unzip" issues but precludes use in supporting tools.
    Per testing, some UNIX "unzip"s fail with large files made here, but
    both the extract here and Mac's Finder-click unzips handle them well.
    Split zips into smaller parts iff large files fail in your tools, and
    you cannot find or install a recent Python 2.X or 3.X to run ziptools.
    -----------------------------------------------------------------------
    """

    trace('Zipping', addnames, 'to', zipname)
    if cruftpatts:
        trace('Cruft patterns:', cruftpatts)

    zipfile = ZipFile(zipname, mode='w', compression=ZIP_DEFLATED, allowZip64=True)
    for addname in addnames:
        if (addname not in ['.', '..'] and
            isCruft(os.path.basename(addname), cruftpatts)):
            print('--Skipped cruft item', addname)

        elif os.path.islink(FWP(addname)) and not atlinks:
            trace('Adding  link  ~item', addname)
            addSymlink(filepath=FWP(addname), zippath=addname, zipfile=zipfile) 

        elif os.path.isfile(FWP(addname)):
            trace('Adding  file ', addname)
            zipfile.write(filename=FWP(addname), arcname=addname)

        elif os.path.isdir(FWP(addname)):
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
    -----------------------------------------------------------------------
    Unzip an entire zipfile at zipname to "pathto", which is created if
    it doesn't exist.  Items from the archive are stored under "pathto",
    using whatever subpaths with which they are recorded in the archive.
    
    Note that compression is passed for writing, but is auto-detected for
    reading here.  Pass "trace=(lambda *args: None)" for silent operation.
    This function does no cruft-file skipping, as it is assumed to operate
    in tandem with the zip creation tools here; see mergeall's script
    nuke-cruft-files.py to remove cruft in other tools' zips if needed.

    MODTIMES: At least through 3.5, Python's zipfile library module does
    record the original files' modification times in zipfiles it creates,
    but does NOT retain files' original modification time when extracting:
    their modification times are set to unzip time.  This is clearly a
    bug, which will hopefully be addressed soon (a similar issue for
    permissions has been posted - see ahead).

    The workaround here manually propagates the files' original mod
    times in the zip as a post-extract step.  It's more code than an
    extractall(pathto), but this version works, and allows extracted
    files to be listed individually.
    
    See this file's main docstring for details on symlink support here;
    links and their paths are made portable between Unix and Windows by
    translating their path separators to the hosting platform's scheme.
    but "nofixlinks can be used to suppress path separator replacement.

    FOLDER MODTIMES: Py docs suggest that os.utime() doesn't work for
    folders' modtime on Windows, but it does.  Still, a simple extract
    would change all non-empty folders' modtimes to the unzip time, just
    by virtue of writing files into those folders.  This isn't an issue for
    mergeall: only files compare by modtime, and dirs are just structural.
    The issue is avoided here, though, by resetting folder modtimes to
    their original values in the zipfile AFTER all files have been written.

    The net effect: assuming the zip records folders as individual items
    (see create above), this preserves original modtimes for BOTH files
    and folders across zips, unlike some other zip tools.  Cut-and-paste,
    drag-and-drop, and xcopy can also change folder modtimes on Windows,
    so be sure to zip folders that have not been copied this way if you
    wish to test this script's folder modtime retention.

    ABOUT SAVEPATH: The written-to "savepath" returned by zipfile.extract()
    may not be just os.path.join(pathto, filename).  extract() also removes
    any leading slashes, Windows drive and UNC network names, and ".." 
    up-references in "filename" before appending it to "pathto", to ensure
    that the item is stored relative to "pathto" regardless of any absolute,
    drive- or server-rooted, or parent-relative names in the zipfile's items.
    zipfile.write() drops all but "..", which zipfile.extract() discards.
    The local extractSymlink() behaves like zipfile.extract() in this regard.

    LONG PATHS: To support long pathnames on Windows, always prefixes the
    pathto target dir with '\\?\' on Windows (only), so that all file-tool
    calls in zipfile and zipsymlinks just work for too-long paths -- the
    length of paths joined to archive names is unknown here.  This internal
    transform is hidden from users in messages, by dropping the prefix and
    mapping pathto back to relative if was not given as absolute initially.

    MAC BUG FIX: there is a bizarre but real bug on Mac OS X (El Capitan 
    at least) that requires utime() to be run *twice* to set modtimes on 
    exFAT drive symlinks.  Details omitted here for space: see mergeall's 
    cpall.py script for background (http://learning-python.com/programs).
    In short, modtime is usually updated by the second call, not first:

      >>> p = os.readlink('tlink')
      >>> t = os.lstat('tlink').st_mtime
      >>> os.symlink(p, '/Volumes/EXT256-1/tlink2')
      >>> os.utime('/Volumes/EXT256-1/tlink2', (t, t), follow_symlinks=False)
      >>> os.utime('/Volumes/EXT256-1/tlink2', (t, t), follow_symlinks=False)

    This incurs a rarely-run and harmless extra call for non-exFAT drives.

    CAVEAT - PERMISSIONS: Python's zipfile module seems to preserve UNIX 
    permissions on creates (zips) but not extracts (unzips).  This is a 
    known bug; see: https://bugs.python.org/issue15795.  ziptools doesn't 
    try to work around this one because it would require a complete copy 
    and rewrite of zipfile's extract code, and may be subtle (e.g., UNIX 
    permissions cannot be applied if the zip host was not UNIX, but the 
    host-type code may not be set reliably or correctly).  

    A fix will hopefully appear in Python's zipfile soon, and be inherited
    here.  For now, on UNIX, restore permissions post extract, or try the 
    local unzip.  Of course, preserving executable permissions on items 
    extracted from zipfiles may also be a huge security risk, but that's 
    not much of an excuse: it's fine for zips that you create yourself.

    LARGE FILES: allowZip64=True supports files of size > 2G with ZIP64 
    extensions, that are supported unevenly in other tools, but work with
    the create and extract tools here.  It's True by default in Python 3.4+ 
    only, and seems unused when unzipping.  See createzipfile() for more.
    -----------------------------------------------------------------------
    """
    
    trace('Unzipping from', zipname, 'to', pathto)
    dirtimes = []


    def show(pathto):
        """
        For message-display only, and on Windows only, try to
        undo the \\?\ prefix and to-absolute mapping for paths.
        This may or may not be exactly what was given, but is
        better than always showing an absolute path in messages,
        and avoiding just-in-case FWP() means rewiting extract().
        """
        if sys.platform.startswith('win'):
            pathto = UFWP(pathto)                   # strip \\?\
            if pathtoWasRelative:
                pathto = os.path.relpath(pathto)    # relative to '.'
        return pathto


    # always prefix with \\?\ on Windows: joined-path lengths are unknown;
    # hence, on Windows 'savepath' result is also \\?\-prefixed and absolute;

    pathtoWasRelative = not os.path.isabs(pathto)   # user gave relative?
    pathto = FWP(pathto, force=True)                # add \\?\, make abs
    
    zipfile = ZipFile(zipname, mode='r', allowZip64=True)
    for zipinfo in zipfile.infolist():              # for all items in zip

        if isSymlink(zipinfo):
            # read/save link path
            trace('(Link)', end=' ')
            savepath = extractSymlink(zipinfo, pathto, zipfile, nofixlinks)
        else:
            # create file or dir
            savepath = zipfile.extract(zipinfo, pathto) 

        filename = zipinfo.filename                       # item's path in zip            
        trace('Extracted %s\n\t\t=> %s' % (filename, show(savepath)))

        # propagate mod time to files, links (and dirs on some platforms)
        origtime = zipinfo.date_time                      # zip's 6-tuple
        datetime = time.mktime(origtime + (0, 0, -1))     # 9-tuple=>float

        if os.path.islink(savepath):
            # reset mtime of link itself where supported
            # but not on Windows or Py3.2-: keep now time
            # and call twice on Mac for exFAT drives bug  

            if (hasattr(os, 'supports_follow_symlinks') and
                os.utime in os.supports_follow_symlinks):
                os.utime(savepath, (datetime, datetime), follow_symlinks=False)

                if sys.platform.startswith('darwin'):
                    os.utime(savepath, (datetime, datetime), follow_symlinks=False)

        elif os.path.isfile(savepath):
            # reset (non-link) file mtime now
            os.utime(savepath, (datetime, datetime))      # dest time = src time   

        elif os.path.isdir(savepath):
            # defer (non-link) dir till after add files
            dirtimes.append((savepath, datetime))         # where supported

        else:
            assert False, 'Unknown type extracted'        # should never happen

    # reset (non-link) dir modtimes now, post file adds
    for (savepath, datetime) in dirtimes:
        try:
            os.utime(savepath, (datetime, datetime))      # reset dir mtime now
        except:
            trace('Error settting directory times')       # ok on Windows/Unix

    zipfile.close()



#===============================================================================

# see ../selftest.py for former __main__ code cut here for new pkg structure

