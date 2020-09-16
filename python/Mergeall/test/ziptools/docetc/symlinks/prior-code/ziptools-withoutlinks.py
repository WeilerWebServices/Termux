#!/usr/bin/python
"""
================================================================================
ziptools.py (part of the mergeall system [3.0]) [Python 3.X or 2.X]
Author:  M. Lutz (learning-python.com), copyright December, 2016
License: Provided freely but with no warranties of any kind.

Tools to create or extract a zipfile containing a set of files and folders.
This mostly extends Python's zipfile module with top-level convenience tools.
For folders, adds the folder's entire content to the zipfile automatically.
For zipfile creation, filters out cruft (hidden) files on request only.
For zipfile extracts, retains original medtimes for files and folders.

This script sidesteps other tools' issues with '.*' hidden metadata (a.k.a.
"cruft") files: they are not always silently/implicitly omitted in zips here,
but can be omitted by explicitly passing cruft filename pattern arguments.
See zipcruft.py for pattern defaults, and zipfile-create.py for background.

CAVEAT: this package does not currently support adding SYMLINKS (symbolic
links) to zip archives, or extracting them from zip archives.  Rather than
naively following links and zipping the items that they reference, though,
links are explicitly skipped in the creation calls here.  The underlying
Python zipfile module doesn't support symlinks today, short of employing
very low-level magic, and there is an open bug report to improve this:

    https://bugs.python.org/issue18595
    https://mail.python.org/pipermail/python-list/2005-June/322179.html
    https://duckduckgo.com/?q=python+zipfile+symlink

See also zipfile-create.py and zipfile-extract.py for command-line clients.
================================================================================
"""

from __future__ import print_function         # py 2.X
import os, sys, time, shutil
from zipfile import ZipFile, ZIP_DEFLATED     # stdlib base support
from fnmatch import fnmatchcase               # non-case-mapping version


#-------------------------------------------------------------------------------

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
            shutil.rmtree(folder)
        except Exception as why:
            print('shutil.rmtree failed:', why)
            input('Try running again, and press Enter to exit.')
            sys.exit(1)


#-------------------------------------------------------------------------------

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

            
#-------------------------------------------------------------------------------

def addentiredir(rootdirname, zipfile,
                 storedirs=True, trace=print, cruftpatts={}):
    """
    Add a full folder to zipfile by adding all its parts.  Python's
    zipfile module has an extractall(), but nothing like an addall().
    See createzipfile() for usage of the optional cruftpatts argument.
    
    Note that the walker's files list is really all non-dirs (which
    may include non-file items that should likely be excluded on some
    platforms), and non-link subdirs are always reached by the walker.

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

    See symlinks caveat above: this does not support links, but it
    also does not follow links and zip the items they reference.
    """

    for (dirhere, subshere, fileshere) in os.walk(rootdirname):
        if storedirs and dirhere != '.':
            trace('Adding folder', dirhere)
            zipfile.write(dirhere)                           # add folders too

        for subname in subshere.copy():
            if isCruft(subname, cruftpatts):                 # skip cruft dirs
                trace('--Skipped cruft dir', subname)
                subshere.remove(subname)                     # prune the walk
            else:
                dirpath = os.path.join(dirhere, subname)
                if os.path.islink(dirpath):                  # walk won't follow
                    trace('--Link ignored', dirpath)         # but record link?
            
        for filename in fileshere:
            if isCruft(filename, cruftpatts):                # skip cruft files
                trace('--Skipped cruft file', filename)
            else:
                filepath = os.path.join(dirhere, filename)
                if os.path.islink(filepath):                 # tbd: record link?
                    trace('--Link ignored', filepath)
                elif os.path.isfile(filepath):               # skip oddities
                    trace('Adding  file ', filepath)
                    zipfile.write(filepath)                  # add files/paths
                else: # fifo, etc.
                    trace('--Skipped unknown type:', filepath)


#-------------------------------------------------------------------------------

def createzipfile(zipname, addnames,
                  storedirs=True, trace=print, cruftpatts={}):
    """
    Make a zipfile at path "zipname" and add to it all folders and files
    in "addnames".  Pass "trace=(lambda *args: None)" for silent operation.
    See function addentiredir() above for details on "storedirs" (its
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
    websites or otherwise distribute programs and data.  To enable cruft
    skipping, pass to cruftpatts a dictionary of this form:
    
        {'skip': ['pattern', ...],
         'keep': ['pattern', ...]}

    to define fnmatch filename patterns for both items to be skipped, and
    items to be kept despite matching a skip pattern (e.g., ".htaccess").
    If no dictionary is passed, all items are added to the zip; if either
    list is empty, it fails to match any file.  See zipcruft.py for more
    details, and importable and customizable presets to pass to cruftpatts.
    """

    trace('Zipping', addnames, 'to', zipname)
    if cruftpatts:
        trace('Cruft patterns:', cruftpatts)
        
    zipfile = ZipFile(zipname, mode='w', compression=ZIP_DEFLATED)
    for addname in addnames:
        if (addname not in ['.', '..'] and
            isCruft(os.path.basename(addname), cruftpatts)):
            print('--Skipped cruft item', addname)
        elif os.path.islink(addname):
            print('--Link ignored', addname)
        elif os.path.isfile(addname):
            trace('Adding  file ', addname)
            zipfile.write(addname)
        elif os.path.isdir(addname):
            addentiredir(addname, zipfile, storedirs, trace, cruftpatts)
        else: # fifo, etc.
            trace('--Skipped unknown type:', addname)
            
    zipfile.close()


#-------------------------------------------------------------------------------

def extractzipfile(zipname, pathto='.', trace=print):
    """
    Unzip an entire zipfile at zipname to pathto, which is created if
    it doesn't exist.  Note that compression is used for writing, but 
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

    SUBTLETY: Py docs suggest that os.utime() doesn't work for folders'
    modtime on Windows, but it does.  Still, a simple extract would
    change all non-empty folders' modtimes to the unzip time, just by
    virtue of writing files into those folders.  This isn't an issue for
    mergeall: only files compare by modtime, and dirs are just structural.
    The issue is avoided here, though, by resetting folder modtimes to
    their original values in the zipfile after all files have been written.

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

    See symlinks caveat above: this does not support extracting links,
    which would require low-level access with Python's current zipfile.
    """

    trace('Unzipping from', zipname, 'to', pathto)
    dirtimes = []
    
    zipfile = ZipFile(zipname, mode='r')
    for zipinfo in zipfile.infolist():                    # all items in zip

        # extract this file 
        filename = zipinfo.filename                       # item's path in zip
        pathname = zipfile.extract(zipinfo, pathto)       # create this file
        trace('Extracted %s\n\t\t=> %s' % (filename, pathname))

        # propagate mod time to files (and dirs on some platforms)
        origtime = zipinfo.date_time                      # zip's 6-tuple
        datetime = time.mktime(origtime + (0, 0, -1))     # 9-tuple=>float
        if os.path.isfile(pathname):
            os.utime(pathname, (datetime, datetime))      # reset file mtime now
        else:
            dirtimes.append((pathname, datetime))         # dir after add files

    # reset dir modtimes now, post file adds
    for (pathname, datetime) in dirtimes:
        os.utime(pathname, (datetime, datetime))          # reset dir mtime now

    zipfile.close()


#-------------------------------------------------------------------------------
  
if __name__ == '__main__':
    """
    Self-test, run in script's folder (and edit me: your context may vary).
    Makes a zip file, unzips it, and compares results to original data.
    See zipfile-create.py and zipfile-extract.py for command-line clients.
    """

    from zipcruft import cruft_skip_keep   # used if any command-line arg
    
    def announce(*args):
        print('\n\n****', *args, '****\n')

    # map test to test subdir names
    skipcruft = len(sys.argv) > 1    # any cmdline arg?
    platform  = sys.platform         # win32, darwin, or linux
    
    cruftsubdir = 'skipcruft' if skipcruft else 'withcruft'
    platsubdir  = dict(win32='Windows', darwin='MacOSX', linux='Linux')[platform]

    # make+use folder here to create and extract a zipfile  
    testsubdir = os.path.join('selftest', platsubdir, cruftsubdir)
    if not os.path.exists(testsubdir):
        os.makedirs(testsubdir)
    zipto = os.path.join(testsubdir, 'ziptest.zip')

    # use test data dirs in '..' parent [**EDIT ME**]
    origin  = '..'
    folders = ['test1', 'test2']
    sources = [(origin + os.sep + folder) for folder in folders]

    # zip original source dirs to subdir file
    announce('CREATING')
    if not skipcruft:                     # any cmdline arg? use cruft patts
        createzipfile(zipto, sources)     # else keep cruft: use {} default
    else:
        createzipfile(zipto, sources, cruftpatts=cruft_skip_keep)    

    # unzip subdir file to subdir dirs, cleaning first if needed
    announce('EXTRACTING')
    for folder in folders:
        tryrmtree(os.path.join(testsubdir, folder))
    extractzipfile(zipto, testsubdir)

    # use mergeall's diff and merge for validation [EDIT ME]
    diffallpath  = os.path.join('..', '..', 'diffall.py')
    mergeallpath = os.path.join('..', '..', 'mergeall.py')

    # compare zipped+unzipped subdir dirs to original source dirs
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
