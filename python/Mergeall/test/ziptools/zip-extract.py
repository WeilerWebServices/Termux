#!/usr/bin/python
"""
=============================================================================
Command-line ziptools wrapper and client (for Python 3.X or 2.X).
Extract a zip file, with:

  <python> zip-extract.py [zipfile [unzipto] [-nofixlinks]]

Where:
  "zipfile" is the pathname of an existing zipfile (a ".zip" is appended to
  the end of this if missing)

  "unzipto" is the pathname of a possibly-existing folder where all unzipped
  items will be stored (the default is ".", the current working directory)

  "-nofixlinks", if used, prevents symbolic-link path separators from being
  adjusted for the local platform (else they are, to make links portable)

Arguments are input at console prompts if not listed on the command line.
The script's output lists for each item both zipfile (from) and extracted
(to) name, the latter after a "=>" on a new line. 

<python> is your platform's optional Python identifier string.  It may be 
"python", "python3", or an alias on Unix; and "python", "py -3", or "py" 
on Windows.  It can also be omitted on Windows (to use a default), and on 
Unix given executable permission for this script (e.g., post "chmod +x").
Some frozen app/executable packages may also omit <python>; see your docs.

The "unzipto" folder is created automatically if needed, but is cleaned
of its contents before the extract only if using interactive-prompts 
mode here and cleaning is confirmed.  Neither the base extract function 
nor non-interactive mode here do any such cleaning.  Remove the unzipto 
folder's contents manually if needed before running this script.

Caution: cleaning may not make sense for ".", the current working dir.
This case is verified with prompts in interactive mode only, but that 
is the only context in which auto-cleaning occurs.

Examples:
  python zip-extract.py                           # input args
  python zip-extract.py tests.zip                 # unzip to '.'
  python zip-extract.py download.zip dirpath      # unzip to other dir
  python zip-extract.py dev.zip  . -nofixlinks    # don't adjust links

ABOUT LINKS AND OTHER FILE TYPES:
  For symbolic links to both files and dirs, the ziptools package either
  zips links themselves (by default), or the items they refer to (upon
  request); this extract simply recreates whatever was added to the zip.
  FIFOs and other exotica are never zipped or unzipped.
 
  To make links more portable, path separators in link paths are automatically
  agjusted for the hosting platform by default (e.g., '/' becomes '\' on
  Windows); use "-nofixlinks" (which can appear anywhere on the command line)
  to suppress this if you are unzipping on one platform for use on another.
  See ziptools.py's main docstring for more details.

ABOUT TARGET PATHS:
  For extracts, the Python zipfile module underlying this script discards
  any special syntax in the archive's item names, including leading slashes,
  Windows drive and UNC network names, and ".." up-references.  The local
  symlink adder parrots the same behavior.

  Hence, paths that were either absolute, rooted in a drive or network, or
  parent-relative at zip time become relative to (and are created in) the
  "unzipto" path here.  Items zipped as "dir0", "/dir1", "C:\dir2", and
  "..\dir3" are extracted to "dir0", "dir1", "dir2", and "dir3" in "unzipto".

  Technically, zipfile's write() removes leading slashes and drive and
  network names (they won't be in the zipfile), and its extract() used
  here removes everything special, including "..".  Other zip tools may
  store anything in a zipfile, and may or may not be as forgiving about
  "..", but the -create and -extract scripts here work as a team.

  Note that all top-level items in the zipfile are extracted as top-level
  items in the "unzipto" folder.  A zipfile that contains just files will
  not create nested folders in "unzipto"; a zipfile with folders will.

ABOUT LARGE FILES:
  Python's zipfile - and hence ziptools - handles files > ZIP64's 2G
  size cutoff, both for zipping and unzipping.  UNIX "unzip" may not.
  See zip-create.py for more details.

CAVEAT: extracts here may not preserve UNIX permissions due to a Python 
zipfile bug; see extractzipfile() in ziptools/ziptools.py for more details.

See zip-create.py for usage details on the zip-creation companion script.
See ziptools/ziptools.py's docstring for more on this script's utility.
=============================================================================
"""

import ziptools, sys, os
if sys.version[0] == '2':
    input = raw_input                         # py 2.X compatibility

if len(sys.argv) >= 2:                        # 2 = script zipfile...
    interactive = False
    nofixlinks = False
    if '-nofixlinks' in sys.argv:             # anywhere in argv
        nofixlinks = True
        sys.argv.remove('-nofixlinks')
    assert len(sys.argv) >= 2, 'Too few arguments'
    zipfrom = sys.argv[1]
    zipfrom += '' if zipfrom[-4:].lower() == '.zip' else '.zip'
    unzipto = '.' if len(sys.argv) == 2 else sys.argv[2]

else:
    interactive = True
    zipfrom = input('Zip file to extract? ')
    zipfrom += '' if zipfrom[-4:].lower() == '.zip' else '.zip'
    unzipto = input('Folder to extract in (use . for here) ? ') or '.'
    nofixlinks = input('Do not localize symlinks (y=yes)? ').lower() == 'y'
    verify = input("About to UNZIP\n"
                      "\t%s,\n"
                      "\tto %s,\n"
                      "\t%socalizing any links\n"
                   "Confirm with 'y'? "
                   % (zipfrom, unzipto, 'not l' if nofixlinks else 'l'))
    if verify.lower() != 'y':
        input('Run cancelled.')
        sys.exit(0)

if not os.path.exists(unzipto):
    # no need to create here: zipfile.extract() does os.makedirs(unzipto)
    pass
else:
    # in interactive mode, offer to clean target folder (ziptools doesn't);
    # removing only items to be written requires scanning the zipfile: pass;
    if (interactive and
        input('Clean target folder first (yes=y)? ').lower() == 'y'):
        # okay, but really?
        if (unzipto in ['.', os.getcwd()] and
            input('Target = "." cwd - really clean (yes=y)? ').lower() != 'y'):
            # a very bad thing to do silently!
            pass
        else:
            # proceed with cleaning
            for item in os.listdir(unzipto):
                itempath = os.path.join(unzipto, item)
                if os.path.isfile(itempath) or os.path.islink(itempath):
                    os.remove(ziptools.FWP(itempath))
                elif os.path.isdir(itempath):
                    ziptools.tryrmtree(itempath)

# the zip bit
ziptools.extractzipfile(zipfrom, unzipto, nofixlinks)

if interactive and sys.platform.startswith('win'):
    input('Press Enter to exit.')     # stay up if clicked
