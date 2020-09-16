This folder contains the output of mergeall and diffall test runs,
with outputs saved as individual files.  This folder's test were 
all run on Windows; see '..' for the same results on other platforms.


MERGEALL TEST SEQUENCE:

  This folder records 14 mergeall runs made against the test1 and test2 
  folders in the top-level /test folder.  These runs were made in sequence: 
  the initial characters in each run's logfile gives its relative step number.  
  For example, file "4-*.txt" is the output of step #4.  Filename labels:

    -"report"    denotes a report-only run
    -"UPDATE"    designates an automatic-update run
    -"skipcruft" used "-skipcruft" mode to ignore hidden/metadata files
    -"withcruft" did not use "-skipcruft" to ignore cruft files

  The test1 and test2 test folders were reset to their original state 
  before each UPDATE run, using the script /test/test-1-2-do-unzip.py.
  Specifically, resets were performed before steps #1, #6, #9, and #12.

  mergeall tests were run in the GUI launcher with logging enabled to 
  save run output here (and logfile names were expanded with prefixes
  afer runs).  mergeall tests can also be run as direct command lines
  with output piped to a logfile, but this does not also test the GUI:

     python3 ../mergeall.py test1 test2 -auto -backup -skipcruft > logfile   

  On Windows:
    c:\...\mergeall\test> py -3 ..\mergeall.py test1 test2 
                  -auto -backup -skipcruft
                  > expected-output-3.0\more-tests\1-report-xxx-mergeall.txt

  See ../BASIC-TESTS.html for command-line test examples.

DIFFALL RUNS:

  The output of diffall runs made along the way are also saved here:
  step numbers in their filenames denote the mergeall testing step 
  at which they were run.  For instance, files "diffall-4*" are the 
  output of diffalls run at step #4 in the mergeall test sequence.

  diffall runs were launched in the console, with piped output:

    python3 ../diffall.py test1 test2 -skipcruft > logfile

  On Windows:
    c:\...\mergeall\test> py -3 ..\diffall.py test1 test2 
                  -skipcruft
                  > expected-output-3.0\more-tests\diffall-xxx.txt


WHAT THE TESTS SIMULATE:

  In general terms, the non-cruft files in test1 and test2 exercise 
  all update types performed by mergeall: file and folder replacements,
  additions, and deletions in TO; based on timestamps, file sizes, and
  tree structure.

  In terms of system cruft files, test1 and test2 contain common Mac and
  Windows files, respectively.  For example, test1 includes the notorious
  ".DS_Store" Mac files, and test2 has a dreaded Windows "Thumbs.db".

  Thus, the merges from test1 to test2 at steps #3 and #6 roughly simulate
  Mac-to-Windows merges, and steps #9 and #12's "backwards" merge from 
  test2 to test1 simulate Windows-to-Mac merges.

  In either case, using the "-skipcruft" mode for updates makes results the
  same as in prior versions: the test folders differ only in their unique 
  cruft files, which are also omitted for "-skipcruft" reports and diffalls.

 
TO CRUFT OR NOT TO CRUFT:

  Despite these tests, you don't necessarily want to use "-skipcruft" if 
  you work on only one platform, and may not care about cruft files from 
  multiple platforms accumulating alongside your content.  These files are
  generally small, and serve roles where recognized.  

  If you are one of the many people who do care, however, this mode allows
  cross-platform data archives to be kept clear of files that have meaning 
  and serve generally-limited roles on just one platform.
