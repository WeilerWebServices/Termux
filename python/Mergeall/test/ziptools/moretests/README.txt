The tests here demonstrate ziptool's support for zipping
and unzipping symlinks on Unix and Windows, and long 
pathnames on Windows.  These are relatively rare in user
content, but are fully supported by ziptools if present.
Another folder gives examples of zipping files, not dirs.

test-symlinks/
	Illustrates symlink support, including advanced 
	features such as creation-time "-atlinks" link 
	following and recursive link detection.  These 
	tests were run on Unix (Mac OS X), but are expected
	to work the same way elsewhere.

	Note: this folder was originally one level higher
	in this package, so some paths (e.g., to scripts) in 
        examples may be one level shorter than they are today.

test-windows-longpaths-symlinks/
	On Windows, exercises both symlinks and Windows
	long-pathname support.  This folder is a direct 
	copy of the same-named folder in the mergeall package,
	and tests both mergeall and ziptools (their symlink 
	and path support are strongly related).

test-simple-files/
	Demos zipping individual files instead of folders, 
        with and without Unix-like shell "*" expansions.
