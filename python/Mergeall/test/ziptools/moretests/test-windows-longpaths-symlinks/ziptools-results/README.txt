This folder chronicles tests run on Windows.  The tests unzipped and
rezipped the xfer*.zip file here, which holds both symlinks and long 
Windows paths.  Tests were run in Admin mode; this is required for 
creating Windows symlinks, but not for long paths. 

See the RESULTS folder for the outputs of COMMANDS.txt commands run.

Unzip TEST-FOLDERS.zip on your machine with ziptools to recreate the
result folders (their unzipped symlinks won't survive mergeall or other
transfers to or from Unix on non-NTFS drives).

ziptools supports both long paths and symlinks on Windows, and
provides a way to transfer symlinks portably between patforms.

mergeall supports long paths on Windows, and symlinks on Windows 
and Unix (but not between them).