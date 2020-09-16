QUICK LOOK:

To see mergeall in action, open the BASIC-TESTS-*.html files in this
folder for the platform(s) you wish to study.  These use non-GUI mode;
see ../../screenshots for mergeall's GUI which runs similar commands.

DETAILS:

This folder contains the output of mergeall and diffall test runs.
All tests were run in and give the expected output of the latest 
mergeall release at test time - version 3.0.  Contents:

  BASIC-TESTS-*.html:
      is the formatted output of the basic test sequence in ../README.txt
  /more-tests-*
      records individual steps of a comprehensive mergeall/diffall test series
  /optimizations-3.0 
      holds timing results for mergeall and diffall optimizations in 3.0
  /nuke-cruft-files 
      has example results for the 3.0 utility script of the same name

The "*" in the above stands for a platform's abbreviated name.  For
example, "Windows" results are run on Windows, and "MacOSX" on Mac OS X. 
Where available, these test's results are given for multiple platforms.  

Apart from pathnames and one embedded screenshot, the Mac OS X and Linux 
tests here are largely the same, as they were run from a Bash Unix shell.
Windows Command Prompt usage differs from Unix in only minor details.

Late-breaking changes, incorporated in most of the outputs here: 

1) The rollback.py script now uses absolute instead of relative paths 
   for the spawned mergeall.py script's name (as do all launchers).
2) There were minor changes to mergeall restore-message format.
3) Mac no longer uses the Python 3.5+ scandir optimization and hence
   doesn't print its opening message (it's actually slower on Macs).
4) Windows and Linux now longer use the Python 3.5+ scandir optimization
   either, as an os.lstat() recoding proved as fast on these platforms.

The BASIC-TESTS-*.hmtl reflect all these; older results here may not.
