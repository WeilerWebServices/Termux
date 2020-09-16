#!/usr/bin/python
"""
==============================================================================
Command-line ziptools wrapper and client (for Python 3.X or 2.X).
Create a zip file, with:

  <python> zip-create.py [zipfile source [source...] [-skipcruft] [-atlinks]]

Where:  
  "zipfile" is the pathname of the new zipfile to be created (a ".zip"
  is appended to the end of this if missing)

  each "source" (one or more) is the relative or absolute pathname of a
  file, link, or folder to be added to the zipfile

  "-skipcruft", if passed, avoids adding hidden or platform-specific
  items to the zipfile (else, nothing is skipped, as described ahead)

  "-atlinks", if passed, adds items that any symlinks refer to instead
  of the symlinks themselves (else, links are always added verbatim)

Arguments are input at the console if not listed on the command line.
The script's output lists all files and folders added to the zipfile.
A "*" in a source expands into multiple sources in supporting shells. 

<python> is your platform's optional Python identifier string.  It may be 
"python", "python3", or an alias on Unix; and "python", "py -3", or "py" 
on Windows.  It can also be omitted on Windows (to use a default), and on 
Unix given executable permission for this script (e.g., post "chmod +x").
Some frozen app/executable packages may also omit <python>; see your docs.

Examples:
  python zip-create.py                                  # input args
  python zip-create.py tests.zip test1 test2 test3      # zip 3 dirs
  python zip-create.py -skipcruft upload.zip webdir     # skip cruft
  python zip-create.py newzip dir -skipcruft -atlinks   # follow links
  python zip-create.py allcode.zip *.py                 # unix, etc.
  python zip-create.py ../allcode.zip * -skipcruft      # items in dir 

ABOUT CRUFT SKIPPING:
  The optional "-skipcruft" argument can appear anywhere if used.  When
  used, it prevents normally-hidden system metadata files and folders
  from being included in the generated zipfile.  Cruft defaults to all
  items whose names start with a "." (the Unix convention), plus a handful
  of others as defined in the pattern lists imported from module file
  zipcruft.py; customize these lists here or in the module as desired.

  Most end-user zips should pass "-skipcruft" to enable cruft skipping.
  This functionality is especially useful on a Mac, to avoid common files
  like ".DS_Store" and "._somename" in zips used to distribute software
  or upload websites.  If "-skipcruft" is _not_ used, every file and
  folder named in a 'source' is included in the zipfile.  For more
  background on cruft, see the overview in mergeall's documentation
  usage pointers, at learning-python.com/mergeall/UserGuide.html.
  
  Note that cruft skipping is implemented in this create script and the
  ziptools function is uses, but not in the extract script or function.
  This is by design: the create/extract tools work together as a pair.
  To remove cruft after unzipping a file created by other tools, see
  mergeall's nuke-cruft-files.py script.

ABOUT LINKS AND OTHER FILE TYPES:
  By default the ziptools package zips and unzips symbolic links to both
  files and dirs themselves, not the items they refer to; use "-atlinks"
  (which also can appear anywhere) at creation time here to zip and unzip
  items that links refer to instead.  This package also always skips FIFOs
  and other exotica.  See ziptools.py for more details.

ABOUT SOURCE PATHS:
  This script allows source items to be named by either relative or absolute
  pathnames, and generally stores items in the zip file with the paths given.
  When extracted, items are stored at their recreated paths relative to an
  unzip target folder (see zip-extract.py for the extract side of this story).
  
  In more detail, this script does nothing itself about any absolute paths
  (e.g., "/dir"), relative  path up-references (e.g., "..\dir"), or drive
  and UNC network names on Windows (e.g.,"C:\", "\\server").  The Python
  zipfile module used here (and the local symlink adder that parrots it)
  strips any leading slashes and removes both drive and network names on
  archive writes, but other oddities, including "..", will be retained in
  the zip file's item names.

  Some zip tools may have issues with this (e.g., WinZip chokes on ".."),
  but the companion script "zip-extract.py" here will always remove all
  of these special-case syntaxes to make item extract paths relative
  to (and hence stored in) the unzip destination folder, regardless of
  their origin.  See that script for more details.

  Still, if you're going to use this script's output in other zip tools,
  for best results run it from the folder containing the items you wish
  to zip (or its parent), avoiding ".."-rooted paths:

     c:\> cd YOUR-STUFF
     c:\YOUR-STUFF> py -3 scriptpath\zip-create.py x y z

  The zipfile module's write() also allows an extra 'arcname' argument
  to give an archive (and hence extract) pathname for an item that differs
  from its filename, but it's not exposed for end-users here (it is used
  by ziptools, but only internally to distinguish local-file from archive
  paths as part of the  support for '\\?'-prefixed long paths on Windows).

  Python's os.path.commonpath() (available in 3.5 and later only) or other
  might be used to remove common path prefixes as an option if all items
  are known to be in the same path, but it is not employed here - the full
  paths listed on the command line are stored in the zipfile and will be
  recreated in later extracts relative to an extract target dir.

  For example, a file named as 'a/b/c/f.txt' is zipped and uzipped to
  an extract target folder E as 'E/a/b/c/f.txt', even if all other items
  zipped are in 'a', 'a/b', or 'a/b/c'.  Hence, if you wish to minimize
  common path prefixes in the zip, cd to a common folder of zip sources
  before running this script, if warranted in a given use case.

MORE ABOUT SOURCES: Unix "*"
  Also note that source arguments can include any number of folders, 
  files, or both.  Any Unix-style "*"s in sources are applied before 
  this script runs, and may expand to either file or folder names.  If 
  you list just simple files as sources and no folders (with or without
  any Unix "*" expansions), no folder nesting occurs in the created 
  zipfile or its extraction (the zipfile will be all top-level files). 
  If you list folders, they will be recreated in the extract.  See 
  test-simple-files/ in moretests/ for an example of file-only zips.

  Where "*" shell expansion is supported (e.g., Unix), you can also 
  include the entire contents of a folder as unnested top-level items 
  in the zip, by running a zip with a "*" source after a cd into the 
  subject dir, and using a zipfile target path outside the dir:

       cd dir; $TOOLS/zip-create.py ../allhere.zip * -skipcruft

  This avoids folder nesting on extracts for all items in the dir:
  the zipfile can be extracted directly in its files' destination,
  and items need not be moved or copied after the extract.

  By contrast, a source "dir/*" or "dir" will instead record items as
  nested in the zip, and extract the items within their dir folder. 
  This is better for multiple folders that may have same-named items, 
  and may be safer (an accidental unzip won't trash files in ".").

ABOUT LARGE FILES
  Python's zipfile - and hence ziptools - handles files > ZIP64's 2G
  size cutoff, both for creating and extracting.  Unfortunately, some 
  UNIX "unzip" command-line programs may fail or refuse to extract 
  zipfiles created here that are larger than this 2G cutoff.  Both the
  zip-extract.py script here and Finder clicks on Mac handle such files
  correctly, and other third-party unzippers may as well.  If none of 
  these are an option you may need to split your zip into halves/parts,
  though this is a last resort; if you can find or install any recent 
  Python 2.X or 3.X on the unzip host, it will generally suffice to 
  run ziptools' zip-extract.py for large files.

CAVEAT: this could support "*" expansion on Windows too, by running source
arguments through glob.glob(), though Windows can run Unix-like shells.
If required, write a launcher script that runs this script with os.system()
and send it the result of glob.glob() or os.listdir() run though ' '.join().

See zip-extract.py for usage details on the zip-extraction companion script.
See ziptools/ziptools.py's docstring for more on this script's utility.
==============================================================================
""" 

import ziptools, sys

# defaults: customize as desired
from ziptools import cruft_skip_keep         

if sys.version[0] == '2':
    input = raw_input                        # py 2.X compatibilty

if len(sys.argv) >= 3:                       # 3 = script zipto source...
    # command-line args
    interactive = False
    skipcruft = {}
    if '-skipcruft' in sys.argv:             # anywhere in argv
        skipcruft = cruft_skip_keep
        sys.argv.remove('-skipcruft')
    atlinks = False
    if '-atlinks' in sys.argv:               # anywhere in argv
        atlinks = True
        sys.argv.remove('-atlinks')
    assert len(sys.argv) >= 3, 'Too few arguments'
    zipto, sources = sys.argv[1], sys.argv[2:]
    zipto += '' if zipto[-4:].lower() == '.zip' else '.zip'
    
else:
    # else ask and verify at the console
    interactive = True
    zipto = input('Zip file to create? ')
    zipto += '' if zipto[-4:].lower() == '.zip' else '.zip'
    
    sources = input('Items to zip (comma-separated)? ')
    sources = [source.strip() for source in sources.split(',')]

    skipcruft = input('Skip cruft items (y=yes)? ').lower() == 'y'
    skipcruft = cruft_skip_keep if skipcruft else {}

    atlinks = input('Follow links to targets (y=yes)? ').lower() == 'y'

    verify = input("About to ZIP\n"
                      "\t%s,\n"
                      "\tto %s,\n"
                      "\t%s cruft,\n"
                      "\t%sfollowing links\n"
                   "Confirm with 'y'? "
            % (sources, zipto,
               'skipping' if skipcruft else 'keeping',
               '' if atlinks else 'not '))
    if verify.lower() != 'y':
        input('Run cancelled.')
        sys.exit(0)

# os.remove(zipto) not required: zipfile opens it in 'wb' mode

# the zip bit
ziptools.createzipfile(zipto, sources, cruftpatts=skipcruft, atlinks=atlinks)

if interactive and sys.platform.startswith('win'):
    input('Press Enter to exit.')     # stay up if clicked
