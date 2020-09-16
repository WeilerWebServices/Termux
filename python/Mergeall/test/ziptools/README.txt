ziptools - wrap and extend Python's zipfile for common use

Version:  1.0, released June 2017 with the mergeall 3.0 package.
License:  provided freely, but with no warranties of any kind.
Author:   © M. Lutz (learning-python.com) 2017.
Run with: Python 3.X or 2.X, on Windows, Mac OS X, Linux, others.

Summary:

This package wraps Python's zipfile module for common use cases, and 
extends it with extra features including support for adding folders, 
modtime propagation, symlinks on Unix and Windows, cruft-file handling,
and long Windows paths.  It provides both:

  -Library tools for use in programs (module ziptools/ziptools.py)
  -Command-line scripts for general use (the zip-*.py files here)

Both foster flexible and portable content management using zipfiles.


===============================================================================
QUICKSTART
===============================================================================

In the following:
  - "py" is your installed Python's name (e.g., "py -3", "python3")
  - "mycontent" and "myunzipdir" may be relative or absolute pathnames
  - "myarchive.zip" may be located at a relative or absolute path
  - "/Code" is the folder in which you've unzipped the ziptools package

Command lines:
  $ py /Code/ziptools/zip-create.py myarchive.zip mycontent -skipcruft
        --store all of folder mycontent in new zipfile myarchive.zip

  $ py /Code/ziptools/zip-list.py myarchive.zip
        --list the contents of zipfile myarchive.zip

  $ py /Code/ziptools/zip-extract.py myarchive.zip myunzipdir
        --extract the contents of myarchive.zip to folder myunzipdir

  $ py /Code/ziptools/zip-create.py ../myarchive.zip * -skipcruft
        --store folder contents as top-level items, where "*" supported 

Gerenal formats:
  [python] zip-create.py [zipfile source [source...] [-skipcruft] [-atlinks]]
  [python] zip-extract.py [zipfile [unzipto] [-nofixlinks]]

Program library:
  $ export PYTHONPATH=/Code/ziptools
  $ py
  >>> import ziptools
  >>> cruftdflt = ziptools.cruft_skip_keep
  >>> ziptools.createzipfile('myarchive.zip', ['mycontent'], cruftpatts=cruftdflt)
  >>> ziptools.extractzipfile('myarchive.zip', pathto='myunzipdir')

Related tools:
  $ py /Code/mergeall/mergeall.py mycontent myunzipdir/mycontent -report -skipcruft 
  $ py /Code/mergeall/diffall.py  mycontent myunzipdir/mycontent -skipcruft
        --verify results, per http://learning-python.com/mergeall.html


===============================================================================
OVERVIEW
===============================================================================

Python's standard zipfile module does great low-level work, but this 
package adds both much-needed features and higher-level access points, 
and documents some largely-undocumented dark corners of Python's zipfile
along the way.  Among its features, ziptools:

  - Adds entire folder trees to zipfiles automatically 
  - Propagates original modtimes for files, folders, and links
  - Can either include or skip system "cruft" files on request
  - Supports symlinks to files and dirs on Unix and Windows
  - Supports long pathnames on Windows beyond its normal limits 

In brief:

Folders
   are added to zipfiles as a whole automatically with extra code,
   a sorely-missed feature of Python's standard module

Modtimes
   for all items are propagated to and from zipfiles, another glaring
   omission in Python's standard module.  This is crucial when used 
   with tools that rely on file timestamps (e.g., mergeall).

Cruft-file skipping
   can be used to avoid adding platform-specific metadata files to 
   cross-platform zipfile archives (e.g., ".DS_Store" Finder files 
   on Macs, and "Desktop.ini" files on Windows).  Cruft is identified 
   with either custom skip and keep filename patterns, or a provided 
   general-purpose default.  It can also be omitted or retained as
   desired, via the "-skipcruft" command-line switch and corresponding
   function argument; see zip-create.py and ziptools.py for details.

Symlinks (symbolic links)
   are supported on both Unix and Windows.  By default, links are 
   copied verbatim, but clients may elect to copy referenced items 
   instead with the "-atlinks" switch and argument.  Highlights:

   - When links are copied verbatim, they are by default also made 
     portable between Unix and Windows by automatically adjusting link
     paths for the hosting platform's path separators: simply zip and
     unzip to transport symlinks across platforms.  The "-nofixlinks" 
     switch suppresses this adjustment when required.

   - When links are followed to copy items referenced with "-atlinks",
     recursive links are detected and copied verbatim to avoid loops, 
     on platforms that support inode-like identifiers.  Recursion 
     detection works on all Unix, and Windows Pythons 3.2+.

   See zip-create.py and ziptools.py for more on "-atlinks", and
   zip-extract.py and ziptools.py for more on "-nofixlinks".

Long pathnames on Windows
   are allowed to exceed the normal 260/248-character length limit on 
   that platform, by automatically prefixing paths with '\\?\' as needed
   when they are passed to the underlying Python zipfile module's tools.  

   No user action is required for this fix.  On all versions of Windows,
   it supports files and folders at long Windows paths both when adding 
   to and extracting from zip archives.  Among other things, this is  
   useful for unzipping and rezipping long-path items zipped on Unix.

Beyond its features, this package also provides free command-line zip 
and unzip programs that work portably on Windows, Mac OS X, Linux, and 
more; runs all its code on either Python 3.X or 2.X; and comes with 
complete and changeable Python source code.

See zip-create.py and zip-extract.py for more details omitted here, 
and ziptools/ziptools.py for lower-level implementation details.


===============================================================================
USAGE
===============================================================================

ziptools/ziptools.py is the main utility module, and the zip-*.py console
scripts wrap it for command-line use: creation, extraction, and listing.

All code in this package works under both Python 3.X and 2.X.

The test-case folders here:

  - selftest/
  - cmdtest/
  - moretests/ 

all give example usage and runs, and each script and module in this package
includes in-depth documentation strings with details omitted here for space.
See also mergeall's test/test-symlinks/ for similar symlink support and tests.

In general, items added to zip archives are recorded with the relative or 
absolute paths given, less any leading drive, UNC, and relative-path syntax.  
Items are later unzipped to these paths relative to an unzip target folder.  
See the create and extract scripts' docstrings for more path usage details.

Quick examples by usage mode:


PROGRAM MODE-------------------------------------------------------------------

See ziptools/ziptools.py for more on program usage.

  import ziptools
  ziptools.createzipfile(zipto, sources)
  ziptools.extractzipfile(zipfrom, unzipto)

  ziptools.createzipfile('test-1-2.zip', ['test1', 'test2'])
  ziptools.extractzipfile('test-1-2.zip', '.')

  from ziptools.zipcruft import cruft_skip_keep
  ziptools.createzipfile('website.zip', ['website'], cruftpatts=cruft_skip_keep)
  ziptools.extractzipfile('website.zip', '~/public_html')

  ziptools.createzipfile('devtree.zip', ['dev'])
  ziptools.extractzipfile('devtree.zip', '.')

  ziptools.extractzipfile('nonportable_devtree.zip', '.', nofixlinks=True)
  ziptools.createzipfile('filledintree.zip', ['skeleton'], atlinks=True)


COMMAND-LINE MODE--------------------------------------------------------------

See zip-create.py and zip-extract.py for more on command-line usage.

  # test folders
  c:\...\ziptools> zip-create.py cmdtest\ziptest.zip selftest\test1 selftest\test2
  c:\...\ziptools> zip-list.py cmdtest\ziptest.zip
  c:\...\ziptools> zip-extract.py cmdtest\ziptest.zip cmdtest\target

  # websites
  ~/webdir$ python3 code/zip-create.py -skipcruft ~/Desktop/website.zip .
  ~/webdir$ python2 code/zip-extract.py website.zip public_html 

  # distributions
  ~/pkgdir$ python3 code/zip-create.py program.zip programdir -skipcruft
  ~/pkgdir$ python3 code/zip-extract.py program.zip programdir

  # development
  ....work1$ python $TOOLS/zip-create.py devtree.zip dev -skipcruft
  ....work2$ python $TOOLS/zip-extract.py devtree.zip . 

  # special cases: populating from links, retaining link separators
  ....work1$ python $TOOLS/zip-create.py devtree.zip dev -skipcruft -atlinks
  ....work2$ python $TOOLS/zip-extract.py devtree.zip . -nofixlinks

  # shell pattern expansion (in shells that support it: Unix, etc.)
  ....dev$ python $TOOLS/zip-create.py allcode.zip a.py b.py c.py d.py 
  ....dev$ python $TOOLS/zip-create.py allcode.zip *.py 

  # use items in a folder as top-level items, not nested in their folder
  cd sourcedir
  ....dev$ python $TOOLS/zip-create.py ../allcode.zip * -skipcruft 
  cd destdir, copy allcode.zip
  ....dev$ python $TOOLS/zip-extract.py allcode.zip . 


INTERACTIVE MODE---------------------------------------------------------------

In the following, substitute "\" for all "/" when working on Windows.


  # EXTRACT an existing zipfile to ".", the current directory

  .../test-symlinks$ ...ziptools/zip-extract.py
  Zip file to extract? save-test1-test2.zip
  Folder to extract in (use . for here) ? .
  Do not localize symlinks (y=yes)? 
  About to UNZIP
	save-test1-test2.zip,
	to .,
	localizing any links
  Confirm with 'y'? y
  Clean target folder first (yes=y)? n
  Unzipping from save-test1-test2.zip to .
  Extracted test1/
		=> test1
  ...etc...


  # CREATE a new zipfile in a folder, from items in a folder

  .../ziptools$ zip-create.py
  Zip file to create? cmdtest/ziptest
  Items to zip (comma-separated)? selftest/test1,selftest/test2                   
  Skip cruft items (y=yes)? y
  Follow links to targets (y=yes)? n
  About to ZIP
	['selftest/test1', 'selftest/test2'],
	to cmdtest/ziptest.zip,
	skipping cruft,
	not following links
  Confirm with 'y'? y
  Zipping ['selftest/test1', 'selftest/test2'] to cmdtest/ziptest.zip
  Cruft patterns: {'skip': ['.*', '[dD]esktop.ini', 'Thumbs.db', '~*', '$*', '*.py[co]'], 'keep': ['.htaccess']}
  Adding folder selftest/test1
  --Skipped cruft file selftest/test1/.DS_Store
  ...etc...


  # EXTRACT the zipfile just created, to another folder

  ../ziptools$ py3 zip-extract.py 
  Zip file to extract? cmdtest/ziptest
  Folder to extract in (use . for here) ? cmdtest/target
  Do not localize symlinks (y=yes)? 
  About to UNZIP
	cmdtest/ziptest.zip,
	to cmdtest/target,
	localizing any links
  Confirm with 'y'? y
  Clean target folder first (yes=y)? y
  Removing cmdtest/target/selftest
  Unzipping from cmdtest/ziptest.zip to cmdtest/target
  Extracted selftest/test1/
		=> cmdtest/target/selftest/test1
  ...etc...


  # LIST the created zipfile's contents

  .../ziptools> zip-list.py
  Zipfile to list? cmdtest/ziptest.zip
  File Name                                             Modified             Size
  selftest/test1/                                2016-10-02 09:01:58            0
  selftest/test1/d1/                             2016-09-30 16:41:12            0
  selftest/test1/d1/fa1.txt                      2014-02-07 16:38:58            0
  selftest/test1/d3/                             2016-10-02 09:05:02            0
  selftest/test1/d3/.htaccess                    2015-03-31 16:55:44          271
  ...etc...

  
  # EXTRACT using absolute paths, on Unix and Windows

  /...$ py3 /Code/ziptools/zip-extract.py 
  Zip file to extract? /Users/blue/Desktop/website.zip
  Folder to extract in (use . for here) ? /Users/blue/Desktop/temp/website
  Do not localize symlinks (y=yes)? n
  About to UNZIP
	/Users/blue/Desktop/website.zip,
	to /Users/blue/Desktop/temp/website,
	localizing any links
  Confirm with 'y'? y
  ...etc...

  c:\...> py -3 C:\Code\ziptools\zip-extract.py 
  Zip file to extract? C:\Users\me\Desktop\website.zip
  Folder to extract in (use . for here) ? C:\Users\me\Desktop\temp\website
  Do not localize symlinks (y=yes)? n
  About to UNZIP
          C:\Users\me\Desktop\website.zip,
          to C:\Users\me\Desktop\temp\website,
          localizing any links
  Confirm with 'y'? y
  ...etc...
