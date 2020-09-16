#!/usr/bin/python
r"""
================================================================================
nuke-cruft-files.py, part of the mergeall system [3.0]

Summary: Removes platform-specific metadata files and folders (a.k.a. "cruft")
         from an entire folder tree, before or after copying it for use on
         other platforms.  Mostly targets common Mac OS X files, but cruft
         patterns may also be general, and are configurable in code here.
         See also mergeall's "-skipcruft" alternative, which is designed
         to automatically keep cruft out of cross-platform archive copies. 

License: Provided freely, but with no warranties of any kind.
Caution: This script deletes files; always run it in list-only mode first. 
Author:  M. Lutz (learning-python.com), copyright December, 2016.
Runs on: Python 3.X and 2.X (but 3.X is recommended for Unicode filenames).
Content: Much of this file also documents the complex issue it addresses.

Usage: the tree's root path and other options are specified as either
command-line arguments, or interactive inputs prompted at the console.
Interactive mode is used when no command-line arguments are provided, and
runs are always verified interactively at the console before they proceed.
Report output may be ">"-piped to a file, as prompts display on stderr.
It is *strongly* recommended that users run in "-listonly" mode first,
to inspect files that will be deleted otherwise.

Command line:
    [python] nuke-cruft-files.py
                 [rootpath [-listonly] [-dotunders] [-alldots]]
                 [> savereport.txt]

Where:
    Default=remove all items matching "crufts" list patterns in tree rootpath.
    -listonly lists all matching cruft items, but does not delete them
    -dotunders adds all "._*" files to the matching crufts set (more aggressive)
    -alldots adds all ".*" files to the matching crufts set (most aggressive)
    Filenames matching the "keeps" list, and folders on pathnames matching the
    "prunes" list are skipped; configure these and "crufts" for your goals.

For rootpath:
    Use absolute or relative directory paths names.
    Use posix /... paths on Macs and Linux, or Drive:... paths on Windows.
    USB drives:   Mac=/Volumes/name, Linux=/media/username/name, Windows=D:\
    Fixed drives: Mac=/Users/username, Linux=/home/username, Windows=C:\Users

UPDATE: this script now also removes some Windows cruft files if present,
though its primary motivation is still files on Mac (the worst offender).
It has also been extended to remove cruft folders in addition to files.

UPDATE: the new "-skipcruft" option in mergeall and diffall (and cpall) can
be used as a less-manual and less-brute-force alternative to this script.  It
skips matching cruft files in both FROM and TO, which means these files will
not be reported as differences, and in mergeall's update modes will not be
copied to, deleted from, or replaced in the TO tree.  This allows Mac to retain
its cruft files, and Windows drives to omit them - intermediate drives won't
receive cruft files from FROM, and also won't cause them to be deleted on
target TO drives later.

UPDATE: this script's patterns also now support removal of Python bytecode
files.  Bytecode files are platform-specific; they always differ across
platforms, trigger recompiles if transferred to a different platform, and
are thus undesirable in cross-platform copies.  The bytecode pattern is
enabled by default here, as these files should normally be removed from
cross-platform external drives - the most likely target when running this
script.  Disable this pattern below to retain bytecode files when running
this script against a platform's local drives (else they'll be recompiled).
The default here matches "-skipcruft" which also skips bytecode files,
both in FROM (so they are not copied) and in TO (so they are not removed).

See UserGuide.html, mergeall_configs.py, and skipcruft.py for more details on
mergeall's "-skipcruft" alternative to this script.  You can still use this
script as a more brute-force solution, if you'd rather manage these files
explicitly and on demand.  This script also can be used to create an initial
cruft-free archive copy to transfer to other devices, and to clean folders
that are used on a Mac but are never the subject of a mergeall; Windows
network drives, for instance, grow cruft if accessed by and used on a Mac.

CAVEAT: unlike mergeall, diffall, and cpall, this script does not use FWP()
to handle too-long paths on Windows; terminate any long-path cruft manually.

--------------------------------------------------------------------------------

PREFACE:

Much of the following was written during the initial shock of seeing how
much "different" the Mac was, especially in regard to external drives.  Since
then, its author has gained more of an appreciation for the platform, and
mergeall's "-skipcruft" mode provides full interoperability for content shared
between Windows, Mac OS X, and Linux.  In fact, this script is only very rarely
needed, to clean up a network or external drive polluted with Mac cruft; upload
folders (programs and websites) changed on Mac are sometimes handled here,
but usually by the similar "-skipcruft" in the ziptools package scripts.

Of course, YMMV, and all that follows remains true, but the Mac cross-platform
story is not quite as dire as may be portrayed here.  Indeed, Windows seems
headed towards a world of advertising, subscriptions, clouds, and other ways
to exploit its customers, which should be larger concerns than managing cruft;
but that's a tale for another doc file.


THE ISSUE:

This program attempts to sanitize data sets (a.k.a. archives and folder trees)
that have been used on a Mac, before or after they are mirrored to Windows or
Linux machines.  The Mac adds numerous and normally-hidden ".*" metadata files
and folders to user data folders in-place, and many of these cannot be disabled.

For instance:

  -A ".DS_Store" file can be created in a folder just by the act of viewing
   it in Finder (often along with a "._.DS_Store" companion).

  -A ".TemporaryItems" folder can be generated just by moving files (also
   sometimes accompanied by a "._.TemporaryItems").

  -A ".Spotlight-V100" folder will appear in a volume's root by default,
   unless indexing has been disabled.

On non-Mac filesystem drives, the Mac can also generate so-called 'companion'
(a.k.a. AppleDouble resource fork) files that are named with a leading "._",
and augment real files (those without the "._") with attributes that are unique
to Mac usage or incompatible with other platforms' filesystems.  Some Mac
programs add these files for every file accessed on non-Mac drives, even if
they have minor or no role in the creating programs, and the non-"._" data fork
files are usable by themselves.  Companion files can even show up for files
viewed on a Mac, but never written there - opening or saving a simple text file
or image on a drive using a non-MAC filesystem, for instance, can suffice to
generate a "._" file alongside the actual data file.  (For more on these files
than space allows here, see https://en.wikipedia.org/wiki/Resource_fork.)

To be fair, other platforms may create some metadata cruft too.  For instance,
Windows can generate "~xxx" Office save files, "Thumbs.db" icon caches, and
"desktop.ini" view options; and Linux may make ".Trash-1000" saved-deletion
folders in USB drive roots.  Still, Mac is by far the worst offender in this
department - its myriad cruft reflect fundamental design choices. 


THE MAC-ONLY PERSPECTIVE:

These files have purposes, and are part of the Mac "ecosystem."  For example,
a ".DS_Store" may save folder view-option choices, ".Spotlight-V100" records
indexing that speeds search, and "._*" companion files store attributes on
non-Mac drives that Mac programs may employ.  They are an acceptable and
perhaps even desirable part of data sets for users who will never use their
data on any other platform, and should be included in backups and mirrors for
this audience.


THE OTHER-PLATFORMS PERSPECTIVE:

On the other hand, such files are useless noise on both Windows and Linux.  By
mirroring an archive to and from a Mac, it can sprout many ".*" files that are
pointless on these other machines.  And by using a non-Mac drive on a Mac, it
can grow a multitude of "._*" companion files that have no purpose outside Macs.
This happens to both drives inserted by USB, and drives accessed on a network. 
Put more colorfully, it's as if archives can come down with data herpes just by
associating with OS X (and indeed, this script was nearly named "Macicillin"!).

Despite these files' generally small sizes, this may not be acceptable to users
of other platforms.  Many such users view in-place hidden ".*" and "._*" files
as an overly-proprietary, if not antagonistic, scheme, especially given the
files' pervasiveness and mandatory nature.  To this crowd, things that make
sense only on a Mac belong only on the Mac.

This position is valid too.  Your data is your private, personal, and valuable
asset; it seems rude and unconscionable for an operating system to corrupt it
with a horde of hidden files, especially in the face of clear backlash from
paying customers.  This is equivalent to someone leaving sticky notes all over
your photograph collection; not only would they distract from your content,
they may have to be pulled out by you later with great care.

At a minimum, these files add deletion steps and processing complexities for
many Mac users.  For example, in mergeall's domain, Mac metadata files can be
so widespread and distracting as to make spotting actual data archive changes
difficult.  These files also require special handling when uploading web site
folders; a "._" companion file ending in a ".png," for instance, can easily
throw off image formatting and display tools.

Whatever their rationales, these files can be fairly seen as condescending to
many Apple customers; add special cases to a myriad of data processing tools;
and needlessly cloud the user experience on an otherwise admirable platform.
They have value on Macs and shouldn't be removed naively without cause; but
users of other platforms may have clear cause.


MORE DETAILS:

For more background on these files - as well as a stunningly rude attitude
towards users of other platforms - see this post by a purportedly former Apple
engineer (note the "former" in that; this doesn't necessarily reflect Apple!):

  http://lists.apple.com/archives/applescript-users/2006/Jun/msg00180.html

For another overview of these files, try a search or this thread:

  http://apple.stackexchange.com/questions/14980/
       why-are-dot-underscore-files-created-and-how-can-i-avoid-them

For background on "._*" companion files on non-Mac drives, check out:

  https://en.wikipedia.org/wiki/AppleSingle_and_AppleDouble_formats
  https://en.wikipedia.org/wiki/Resource_fork

Interestingly, ".DS_Store" files may also reflect a legacy OS X bug:

  http://arno.org/arnotify/2006/10/on-the-origins-of-ds_store/
  
Here, we'll note that this unusual scheme complicates data archiving tasks in
ways that other platforms do not, and perhaps needlessly so, but otherwise
leave further politics aside and address the issue.


THE FIX:

To support all audiences, mergeall always retains metadata files by default
(and now provides a "-skipcruft" mode and GUI toggle to skip them: see the
UPDATE in the first section above), but provides this script as a portable
way to delete these files in a single step when desired:

-Mac-only users need do nothing, as their metadata will be merged and retained.

-Users who predominantly work on Windows or Linux but wish to update their
 data sets on Macs too may run this script to clean up Mac cruft either before
 mirroring a data set to a transfer device with mergeall (run it as a pre-step
 on Mac), or after the data set has been mirrored to the other devices by
 mergeall (run it as a post-step on either Mac or Windows/Linux).

Either way, this script attempts to remove common hidden metadata files and
folders created by a Mac.  It does not try to remove special folders on a
volume (device) root, such as .Trashes, because some are useful, many won't
appear in data archive folders themselves, and a few trigger new system actions
on removal until restored; see ahead for hints on suppressing some of these
manually if desired.

As noted earlier, other platforms may also create metadata cruft, and some
of it is addressed here too.  Mac is clearly the biggest cruft exporter, but
the merit of its model remains in the eye of the beholder.

--------------------------------------------------------------------------------

MORE USE CASE DETAILS (or: Do you need to Care?)

There are two main use cases for mergeall:

    1) Backups: incrementally backing up data sets to archive devices
    2) Mirrors: echoing data sets to other machines using an intermediate device

When used only to do quick backups to an external device, mergeall users do
not generally need to care about platform divergence; Mac backups will include
Mac metadata, but are likely not intended for cross-platform use.

However, when using mergeall as a manual "cloud" system to mirror data sets
between computers with an intermediate transfer device, platform issues become 
a factor.  There are multiple mirroring uses cases that may include Mac machines:

    1) Users who will never use anything but multiple Macs
    2) Users of multiple platforms who will view data sets on Macs but never 
       update them there (read-only mode: Macs are mergeall's TO, but never FROM)
    3) Users of multiple platforms who will both view and update data sets
       on Macs (read/write mode: Macs are both mergeall's TO and FROM).

The last of the above is the only usage mode where metadata files can be an
issue.  In more detail, this yields the following decision-tree pseudocode:

If you do not copy your archives to a Mac:
    You do not need to run this script - you somehow get by without Macs.
    
If you use your archives on Macs only, whether for backups or mirrors:
    You do not need to run this script - archives include your Mac metadata.

If you use your archives on multiple platforms including a Mac:
    If you use Mac copies in read-only mode (for viewing, not updating):
        You do not need to run this script - the Mac is always TO target only.

    If you update an archive's files on a Mac, and copy it elsewhere (as FROM):

        If you do not care about Mac metadata files in your archives:
            You do not need to run this script - archives include Mac metadata.
            (You won't normally see these files on Macs and Linux, but will on
            Windows because its notion of "hidden" isn't a leading "." name.)
 
        If you do not want Mac metadata files to show up in your archives:
            *YOU CARE*
            Either use mergeall's "-skipcruft" option to ignore cruft files,
            or run this script in one of the following modes:
            -Before copying off the Mac (before it is a mergeall FROM)
                Run on the Mac itself, with the Mac's archive copy root
                (caution: this may remove metadata Mac programs use)
            -After copying off the Mac:
                Run on any platform, with the transfer device's archive root.
            -After copying off the Mac:
                Run on other platforms, with the platform's archive copy root.

IN OTHER WORDS, you need run this script only if all of the following are true:

    -You use your archive on a Mac and others
    -You change your archive's files on the Mac
    -You copy the archive from the Mac to other platforms
    -You don't want Mac metadata files in your archive

If so, run this script either before or after mergeall, to delete Mac metadata.
You can also run this just on copies on Windows and Linux machines, and retain 
metadata files on the transfer device (e.g., USB flash or SSD drives) for use on
Macs, as long as the transfer device is never the TO destination for a copy from
a non-Mac machine, as that will erase its metadata files (though see the UPDATE
ahead).  If you don't know what that means, read mergeall's UserGuide.html and
docetc/MoreDocs/Whitepaper.html.

The alternative to this script's extra step is to modify mergeall itself, to
skip Mac metadata files in FROM source and/or TO target trees, and allow this
to be enabled or disabled in the configs file.  Given that any of the use cases
outlined above seems just as valid as any other, a default in this scheme might
be rude.  Instead, multiplatform uses cases simply incur an extra script launch
when transferring from the Mac.  Multiple-platform users seem more likely to
care about and address this issue than those working on a single platform.

    UPDATE: as noted earlier, mergeall was eventually modified to skip cruft
    files in both FROM and TO when "-skipcruft" is used, and its GUI supports
    this mode with a new toggle.  Enabling this mode is an alternative to this
    script, though it is likely moot for users who never use Macs.  This new
    option also allows you to both avoid erasing metadata files in TO
    destinations if already present, and avoid copying them to TO if absent.

Caveat: if you transfer an archive from the Mac and strip its metadata with
this script for use on other platforms, transferring it back to the Mac later
will wipe out all archive metadata on the Mac (they won't be present in FROM,
and there is no way to skip these files in TO targets).  This is an unavoidable
consequence of Apple's proprietary design decision to store metadata in data
folders in-place - this puts metadata on a par with actual data, and subject
to the same data archiving constraints.  If you don't want to later erase
any accumulated Mac metadata, keep it in archives and do not run this script.

    UPDATE: the new "-skipcruft" mergeall/diffall option addresses this too, by
    ignoring cruft files in TO - they aren't erased on the Mac if not on FROM.

On the other hand: for a copy/paste from an external drive, Mac OS X's own
Finder (file explorer) did _not_ copy over dozens of names that start with a
"._" and are thus considered hidden - even though they originated on a Mac!
Hence, there may be no reason for you to retain these files either (and it
begs the question: should mergeall?; this remains a TBD).

    UPDATE: the new "-skipcruft" mergeall/diffall option mimics Finder (and
    some other tools) this way - it skips and hence doesn't copy cruft in FROM. 

Naturally, there are other cross-platform file issues which you may need to
address in a mixed-system environment (Windows' DST rollover timestamps,
Windows-versus-Unix line-end sequence differences, pathname constraints,
and so on).  These are beyond this script's scope; see fixlongpaths.py,
fix-fat-dst-modtimes.py, and frigcal's fixeoln.py for examples of other
platform-leveling tools -- and hope for a brighter future in which computer
vendors do not view proprietary lockdowns as valid business practice!

--------------------------------------------------------------------------------

HINTS FOR SUPPRESSING MAC METADATA FILES:

Note: this list is for reference only, and you may or may not want to do any
of the following; please research impacts before applying.

Show/hide hidden files (.*) in Finder ("ls -a" in a shell works too):
    defaults write com.apple.finder AppleShowAllFiles TRUE;killall Finder
    defaults write com.apple.finder AppleShowAllFiles FALSE;killall Finder
    (Note: "._*" files may still not be displayed; use "ls -a" in a shell)

Stop metadata on network volumes and USB drives (.DS_Store):
    defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
    defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true	

Stop metadata on internal drives, hard or SSD (.DS_Store):
    there appears to be no way to do this (and why?), but they can be removed;
    delete on any platform with: this script  
    -or-
    delete on Mac and perhaps elsewhere with: "dot_clean volumepath"
    (Note: this is more than a deletion: see "man dot_clean" on Mac,
    or fetch elsewhere for use on Windows)
    -or-
    delete on any Unix with: "find . -type f -name '*.DS_Store' -ls -delete"

Stop spotlight from indexing a volume (/.Spotlight-V100)
    create a ".metadata_never_index" file in a volume's root folder
    -or-
    System Preferences > Spotlight > Privacy > + to add a /Volumes device or folder
    (Note: drag your entire internal hard/SSD drive here to stop its indexing)
    -or-
    sudo mdutil -a -i off
    sudo mdutil -a -i on
    -or (?untested)-
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist
    sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist
        
Disable trash folder deletion saves for USB drives (/.Trashes)
    create a ".Trashes" file in Volume root, to prevent a folder of same name
    (Note: Linux creates a similar ".Trash-1000" folder on USB drive roots,
    whose deletion retentions can similarly be disabled by a same-named file.)

Disable .fseventsd writes on file system changes (/.fseventsd)
    create a ".fseventsd" folder in root folder, with a single file named "no_log"
    seems to be a no-op as fseventsd should be empty on eject, but avoids activity
    note that this item will probably reappear if simply deleted
	
Disable spotlight localization (/.localized? - cause and fix TBD):
    supposedly tells apps it's okay to display a folder's localized name (really?)
    System Preferences => Security & Privacy => Privacy => Location Services,
    "System Services", click "Details...", uncheck "Safari & Spotlight Suggestions"

A combo platter: to disable indexing, fsevetsd, trash on a USB stick:
    mdutil -i off /Volumes/yourUSBstick
    cd /Volumes/yourUSBstick
    rm -rf .{,_.}{fseventsd,Spotlight-V*,Trashes}
    mkdir .fseventsd
    touch .fseventsd/no_log .metadata_never_index .Trashes
    cd -

To disable "._*" companion files
    you can't, but you can remove them with this script or ignore them
    with mergeall's "-skipcruft" option; reformat your drive to use a Mac
    filesystem; or not use a non-Mac drive directly on a Mac.

================================================================================
"""

#
# CODE STARTS HERE
#

from __future__ import print_function
import sys, os, shutil
from fnmatch import fnmatch   # case-insensitive (but only on Windows!)

if sys.version[0] == '2':
    input = raw_input


#------------------------------------------------------------------------------
# FILENAME PATTERNS
#------------------------------------------------------------------------------
# Don't rm .Spotlight-V100, .Trashes, .fseventd unless immediately restored:
# may be in volume root only, and deletion may trigger actions they disable.
# Patterns here match as case-insensitive on Windows, but not on Mac or Linux.
# On Windows, use "C:\" to name a drive, not "C:", else 'prunes' apply to '.'.
# Disable the ".py[co]" pattern here to keep platform-specific Python bytecode
# on local drives, but keep it enabled to remove from cross-platform drives.
# CAVEAT: some patterns may subsume others - not checked or optimized here.
# SEE ALSO: the more-complete cruft patterns and docs in mergeall_configs.py.
#------------------------------------------------------------------------------

# Nuke these files (Mac), unless in keeps
dsstore   = '.DS_Store'           # these are pervasive
dsstore2  = '._.DS_Store'         # these appear occasionally
localized = '.localized'          # these are common
temporary = '.TemporaryItems'     # a folder left by moves/copies
trashed   = '.Trashes'            # delete retention - recycle bin
dotunders = '._*'                 # optional: more aggressive (AppleDoubles)
alldots   = '.*'                  # optional: most (too?) aggressive catchall

# Always nuke these filenames, minimally
crufts = [dsstore, dsstore2, localized, temporary]

# A few Windows cruft files too (hey, fair is fair)
crufts += ['[dD]esktop.ini',      # similar to Mac's .DS_Store: folder views
           'Thumbs.db',           # folder items icon cache file
           '~*']                  # catchall for temporary Office save files

# Any other platform-specific items to remove from archive copies
crufts += ['*.py[co]']            # del python bytecode on cross-platform drives

# Never nuke these: valid file or folder names (extend as desired)
keeps = ['.htaccess*', '.login', '.bash*', '.profile', '.svn']

# Never nuke these or their contents: folder pathnames (EDIT ME)
prunes = ['*%sziptools*selftest' % os.sep,           # ziptools retains cruft
          '*%smergeall*%stest[12]' % ((os.sep,)*2),  # mergeall tests use cruft
          '*%smac%sDRIVE-METADATA' % ((os.sep,)*2),  # keep volume root inserts
          '*%s_volume-root-start' % os.sep           # ditto
          ]


#------------------------------------------------------------------------------
# CONFIG RUN
#------------------------------------------------------------------------------

builtin_input = input   # still available here, 3.X or 2.X

def input(prompt):
    "prompt on stderr, so stdout report can be piped to a file"
    sys.stderr.write(prompt)
    return builtin_input()   # or sys.stdin.readline().rstrip()

def display(*pargs, **kargs):
    "messages on stderr, so stdout report can be piped to a file"
    print(*pargs, file=sys.stderr, **kargs)   # order matters in 3.3 (not 3.5)

def yesreply(prompt):
    return input(prompt)[:1].lower() == 'y'

def usageexit():
    display('Usage: [python] nuke-cruft-files.py '
                '[rootpath [-listonly] [-dotunders] [-alldots]] '
                '[> savereport.txt]')
    input('Not run - press Enter to exit.')
    sys.exit(1)

if '-help' in sys.argv:
    usageexit()

if len(sys.argv) == 1:
    # interactive
    rootpath = input('Data set (archive) tree root path? ')
    listonly = yesreply('List matching cruft files only? ')
    if yesreply('Match all "%s" files too (more aggressive)? ' % dotunders):
       crufts.append(dotunders)
    if yesreply('Match all "%s" files too (most aggressive)? ' % alldots):
       crufts.append(alldots)       
else:
    # command args
    rootpath = sys.argv[1]
    listonly = '-listonly' in sys.argv[2:]
    if '-dotunders' in sys.argv[2:]:
        crufts.append(dotunders)
    if '-alldots' in sys.argv[2:]:
        crufts.append(alldots)

if not os.path.isdir(rootpath):
    display('Invalid root path: "%s".' % rootpath)
    usageexit()


#------------------------------------------------------------------------------
# VERIFY RUN
#------------------------------------------------------------------------------

def pp(alist):
    "layout lists and nested paths nicely; pprint doesn't handle this case"
    if len(str(alist)) <= 85:
        # avoid repr for paths, else '\\' on Win
        return '[' + ', '.join("'%s'" % x for x in alist) + ']'
    else:
        # show one item per line, at indent '\t\t'
        return '[\n\t\t' + ',\n\t\t'.join("'%s'" % x for x in alist) + '\n\t\t]'
    
display('About to run in %s mode' %
            ('LIST ONLY' if listonly else 'REMOVE FILES'))
display('\tOn root "%s"\n\tFinding %s\n\tKeeping %s\n\tPruning %s' %
            (rootpath, pp(crufts), pp(keeps), pp(prunes)))

if not yesreply('Continue? '):
    display('Run cancelled - no changes made.')
    input('Press Enter to exit.')
    sys.exit(1)


#------------------------------------------------------------------------------
# WALK THE ROOT'S TREE
#------------------------------------------------------------------------------
# List or remove matches in "crufts" that are not also in "keeps",
# pruning (skipping) dirs in "prune" along the way.  Also prunes dirs
# as they are removed, so doesn't try to remove subdirs after dirs.
# TBD: should 'inxcruft' record/report matches by name or by pattern?
# TBD: would folder/file counts be useful here (as is: run mergeall)?
# TBD: Python 2.X fails for non-ASCII filenames in os.path.isfile().
#------------------------------------------------------------------------------

display('Walking root tree...')
numcruft = 0
inxcruft = {}
numremove = numfail = 0

for (dirhere, subshere, fileshere) in os.walk(rootpath, topdown=True):

    # nuke folders
    copysubshere = subshere[:]
    for subname in copysubshere:
        subpath = os.path.join(dirhere, subname)
        if any(fnmatch(subpath, pattern) for pattern in prunes):
            print('(Pruned folder)', subpath)
            subshere.remove(subname)  # skip content
        else:
            if any(fnmatch(subname, pattern) for pattern in crufts):
                if not any(fnmatch(subname, pattern) for pattern in keeps):
                    print('Cruft folder =>', subpath)
                    subshere.remove(subname)  # skip content
                    if not listonly:
                        try:
                            shutil.rmtree(subpath)
                        except Exception as why:
                            numfail += 1
                            print('**Error removing "%s" - skipped.' % subpath)
                            print('**Python exception: ', why)
                        else:
                            numremove += 1
                    numcruft += 1
                    inxcruft[subname] = inxcruft.get(subname, 0) + 1

    # nuke files
    for filename in fileshere:
        filepath = os.path.join(dirhere, filename)
        if os.path.islink(filepath) or not os.path.isfile(filepath):
            print('(Nonfile item) ', filepath)
        else:
            if any(fnmatch(filename, pattern) for pattern in crufts):
                if not any(fnmatch(filename, pattern) for pattern in keeps):
                    print('Cruft file =>  ', filepath)
                    if not listonly:
                        try:
                            os.remove(filepath)
                        except Exception as why:
                            numfail += 1
                            print('**Error removing "%s" - skipped.' % filepath)
                            print('**Python exception: ', why)
                        else:
                            numremove += 1
                    numcruft += 1
                    inxcruft[filename] = inxcruft.get(filename, 0) + 1


#------------------------------------------------------------------------------
# REPORT RESULTS
#------------------------------------------------------------------------------

print('-' * 40)
print('Summary: %d cruft items %s.' % (numcruft, 'found' if listonly else 'removed'))
print('Number items removed=%d, failed=%d' % (numremove, numfail))
print('Cruft item counts by name:')
if not inxcruft:
    print('[None]')
else:
    for key in sorted(inxcruft):
        print('  %04d => "%s"' % (inxcruft[key], key))
print('-' * 40)

if sys.platform.startswith('win') and sys.stdin.isatty(): 
    input('Finished - press Enter to exit.')  # stay open on Windows clicks   
