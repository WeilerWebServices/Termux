QUICK LOOK:

To see mergeall in action, open the BASIC-TESTS-*.html files in folder
expected-output-3.0 folder for the platform(s) you wish to study.  See
also ../../screenshots for mergeall's GUI which runs similar commands.


DETAILS:

The two canned test folders here:

  -test1
  -test2

comprehensively exercise the updates performed by mergeall runs.  
Use them as FROM/TO subjects for experimenting with the system 
before running it live on your important data. 

The /expected-output-3.0 folder here has expected results for 
mergeall and diffall runs against these two test folders.  See 
its README.txt for more details.  This folder's BASIC-TESTS-*.html
provide a quick, readable look at mergeall and diffall in action.


TEST CONTENT:

Version 3.0 adds ".*" and other cruft (a.k.a. metadata) files in
the test folders here to simulate files added by various platforms:
test1 mimics Mac, and test2 Windows.  Run with "-skipcruft" (or the 
equivalent toggle or reply in the launchers) to ignore these in 
diffall reports, cpall copies, and mergeall reports and merges.

Version 3.0 also adds support for symlinks on both Unix and Windows, 
demonstrated in ./test-symlinks, as well as support for long 
pathnames on Windows that exceed its usual limits, exercised in 
./test-windows-longpaths-symlinks (the latter also test symlinks). 


SAVED TEST DIRS:

Zipfile test-1-2.zip contains the original test folders' content, 
if your copies becomes munged.  The scripts:

  -test-1-2-do-zip.py
  -test-1-2-do-unzip.py    <= run to restore

here can be run directly and with no arguments (e.g., by clicking) to 
zip and unzip the two test folders.  Use the latter (unzip) to restore
the originals before new tests.

It was necessary to code these with Python's zipfile module, as WinZip
discards the test's ".*" Mac files on Windows, with no apparent way to 
disable this except on Macs.  See the ziptools package here for zipfile 
utility functions used for resetting state before tests.  This package
is also a general zip/unzip utility, including command-line scripts
(see also its web page at http://learning-python.com/ziptools.html).


BASIC TESTS:

For a quick stress test, run the following command-lines in mergeall.py's 
top folder (the mergeall commands can be run from the GUI too, and Unix
users on Mac and Linux use "/" instead of "\" in paths): 

  cd test
  test-1-2-do-unzip.py                               # reset test folders
  cd ..

  (copy original test\test2 to a new private folder) # delete first if needed
  xcopy /E test\test2 _original_                     # use cp -r/-R on Unix
 
  mergeall.py test\test1 test\test2 -auto -backup    # synch, with backups
  mergeall.py test\test1 test\test2 -report          # verify now no diffs
  diffall.py test\test1 test\test2                   # verify byte by byte

  rollback.py test\test2                             # rollback last synch
  mergeall.py test\test2 _original_ -report          # verify same as original
  diffall.py test\test2 _original_                   # byte-wise content verify

Try the initial mergeall and diffall runs with and without "-skipcruft" 
and "-quiet" to see how they modify results: when merged with cruft 
skipping, verifies will report differences unless they also skip cruft.

You can view examples of these runs on various platforms in:

  expected-output-3.0\BASIC-TESTS-*.html


OTHER:

The test-symlinks folder hosts self-contained tests of 3.0's symlinks support,
and test-windows-longpaths-symlinks tests both symlinks and Windows long paths.
Older restore and rollback sessions: ..\older-examples-webonly\Logs\version-2.1.


NEW IN MERGEALL 3.1:

The new verify-changes-3.1 folder has assorted tests for Mergeall 3.1 changes.  
Its mergeall-3.1.zip shows how the folder modtimes in the test1 and test2 folders
here fared in Mergeall 3.0 and 3.1 - they were stamped with run time in 3.0,
but original modtimes are propagated in 3.1.  This is largely convenience;
folder modtimes aren't used by Mergeall, so they aren't critical to results 
(file and link modtimes are, but have always been propagated to new copies).
The diffs-3.1 folder also captures assorted differences in the 3.1 release.
