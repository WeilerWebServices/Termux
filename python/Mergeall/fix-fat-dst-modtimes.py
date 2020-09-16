#!/usr/bin/python
r"""
=============================================================================
fix-fat-dst-modtimes.py:
    adjust file modification times (part of the mergeall system [2.0])
    
Usage:
    [py[thon]] 
        fix-fat-dst-modtimes.py folderpath (-add | -sub) [numhours=1]

Examples:
    fix-fat-dst-modtimes.py D:\MY-STUFF -add   # add 1 hour to all (Windows)
    fix-fat-dst-modtimes.py /MY-STUFF -sub 8   # sub 8 hours from all (Unix)

This script runs under Python 3.X or 2.X (3.X may handle Unicode best).
(Note: you may avoid having to use this script to adjust file modtimes
after DST rollovers by formatting external drives as exFAT; see ahead.)

For FAT32 drives on Windows (e.g., USB flashdrives), fix modification
time 1-hour skew versus NTFS and others (e.g., harddives) at Daylight 
Savings Time (DST) rollovers.  Add ("-add") or subtract ("-sub") 1 hour
by default to the modification times of all files (but not folders) in 
the entire "folderpath" directory tree.  Adjust timestamps by multiple
hours (instead of the default 1) if an integer is passed for "numhours".

This script changes modtimes only - it does not rewrite any data in files,
and hence runs much quicker than a full recopy.  It suffices to put the 
directory tree's files back in synch with an NTFS or other non-FAT 
filesystem copy, according to mergeall's timestamp+size comparisons.

Run this with the root path of your FAT device's archive copy at
DST rollovers, after determining whether you must -add or -sub 1 hour
on the FAT drive's times (versus a same file's modtimes on your other
drives: right-click to Properties for any FAT/NTFS file pair to see).
This can also be run on a non-FAT drive's copy if more convenient.

This works, but is a manual process (you must run this script from a
command line, after inspecting file properties on both drives), and
is perhaps easy to forget (in which case, mergeall may overwrite 
every file on the FAT drive at DST rollover, in auto-updates mode).

Common alternatives to this script:

1) RECOMMENDED: Formatting external drives as exFAT (instead of FAT32)
   avoids DST timestamp issues altogether on both Windows and Mac OS X,
   though Linux exFAT extensions require a third-party install and may
   not support timezone-based changes as fully.  This solution was
   verified to work on all 3 platforms at the March, 2017 DST switch.

2) Turning off automatic DST adjustment on all Windows machines may
   suffice for Windows users, but this won't apply to other platforms.

3) Use 2 USB FAT drives: one when DST is active, and one when it is
   not, though this may doubles your external drive needs.

4) Formatting external drives in other UTC-based filesystems (e.g.,
   NTFS, HFS, ext) avoids DST issues too, though these are not
   universally supported across platforms, and may impact performance.

See mergeall's UserGuide.html and docs/Whitepaper.html for more 
background on the timestamp issue this script addresses.  See also
examples/Logs/fix-fat-dst for logs and its README for more on usage.

[3.0] Added optional "numhours" for adjusting timestamps by multiple
hours in a single run; it defaults to 1 hour, which works as before,
and addresses this script's primary goal of DST-rollover adjustment.

[3.0] Skips symbolic links, if present.  mergeall compares these by
content only, so modtime is moot (os.utime's follow_symlinks=False
is available in 3.3+ only, and wouldn't apply to other Pys anyhow).

[3.0] Note: this script does not skip cruft metadata files (e.g.,
Mac ".DS_Store"), but mergeall does (along with diffall, cpall, and
ziptools), so this is harmless.  It impacts only file counts here.

[3.0] Caveat: unlike mergeall, diffall, and cpall, this script does
not use FWP() to handle too-long Windows paths; adjust any manually.

[3.1] Caveat: this was fixed to run under Python 2.X again (where 
os.utime() takes no keyword args), but ignores modtimes on links and 
folders (Mergeall 3.0 does links, and 3.1 propagates folder times).
=============================================================================
"""

from __future__ import print_function  # Py 2.X
import sys, os

argv = sys.argv
if (len(argv) not in [3, 4] or
    not os.path.exists(argv[1]) or
    not os.path.isdir(argv[1]) or
    argv[2] not in ['-add', '-sub'] or
    (len(argv) == 4 and not argv[3].isdigit()) 
   ):
    print('Usage: [py[thon]] '
            'fix-fat-dst-modtimes.py folderpath (-add | -sub) [numhours=1])')
    sys.exit(1)

folder, action = argv[1], argv[2]
hoursecs   = 60 * 60
numhours   = 1 if len(argv) == 3 else int(argv[3])
secshours  = hoursecs * numhours
secschange = +secshours if action == '-add' else -secshours


# Fix files
print('Running...')
fcount = 0
for (thisdir, dirshere, fileshere) in os.walk(folder):
    for filename in fileshere:
        filepath = os.path.join(thisdir, filename)
        if os.path.islink(filepath):
            continue # compared by content only (still?)

        curacctime = os.path.getatime(filepath)
        curmodtime = os.path.getmtime(filepath)
        newmodtime = curmodtime + secschange

        try:
            os.utime(filepath, (curacctime, newmodtime))     # [3.1] py2.X has no times=
        except:
            print('Skipped file: error changing modtime in [%s]' % filepath)
            print('\t', sys.exc_info()[0], sys.exc_info()[1])
        else:
            print('Adjusted file:', filepath)
            fcount += 1


# Report stats
print('Done: %d file modtimes adjusted %s by %d hour%s' %
           (fcount, 
            'up' if action == '-add' else 'down', 
            numhours, 
            '' if numhours == 1 else 's'))
