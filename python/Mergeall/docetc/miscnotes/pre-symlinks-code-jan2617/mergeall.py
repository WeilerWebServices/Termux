#!/usr/bin/python
# Python 3.X is recommended for Unicode filenames, 3.5+ is recommended for speed
r"""
================================================================================
mergeall.py:
  main file-processing script (part of the mergeall system)

A folder tree-merge utility, and a supplemental example for books PP4E/LP5E.
Makes a destination folder the same as a source folder quickly.  This script
is run automatically by the GUI and console launchers provided, and may be run
directly by manual command lines.  See UserGuide.html for usage, license, and
author details.  See docetc/MoreDocs/Revisions.html for all version history.
  
  *WARNING*: Depending on your command-line options or interactive inputs,
  this script may irrevocably change the content of the directory tree
  named in its "dirto" argument in-place as needed to make it the same as
  "dirfrom".  Do not run it against a tree you care about unless you fully
  understand its operation.  A backup copy of "dirto" tree is recommended.

  Update: The 2.0+ "-backup" option makes automatic copies of items replaced
  or deleted in "dirto" to mitigate some data loss risk, and 2.1's "-restore"
  can rollback a run with backups immediately after the run.  Still, these
  should not be considered foolproof, given the many ways that storage devices
  may fail.  Though designed to be useful and robust, this script and its
  launchers are provided as is, without warranties of any kind.  By using
  this system, you accept all responsibility for any actions it takes.

--------------------------------------------------------------------------------

USAGE:
  [py[thon]] mergeall.py dirfrom dirto
                [-report] [-auto]
                [-peek] [-verify]
                [-backup] [-restore] [-quiet]
                [-skipcruft]

Where:
  dirfrom    => source tree pathname       (this tree is never changed)
  dirto      => destination tree pathname  (-auto changes this tree to == dirfrom)
  -report    => report differences only and stop, making no changes
  -auto      => update dirto for differences automatically without asking
  -peek      => check N start/stop bytes too when comparing same-named files
  -verify    => at end, run diffall.py to check update results (or rerun with -report)
  -backup    => backup files and dirs in dirto that will be replaced or deleted [2.0]
  -restore   => run mergeall to restore/rollback changes from a prior backup [2.1]
  -quiet     => suppress per-file backing-up log messages (show just one) [2.4]
  -skipcruft => ignore cruft (a.k.a. metadata) files/dirs in both FROM and TO [3.0]

  Main usage modes:
      if "-report": report differences only
      elif "-auto": report and resolve differences automatically
      else:         report and interact to resolve differences selectively
  
  See UserGuide.html usage note for Windows pathname syntax of devices and
  network drives used for dirfrom and dirto.  See backup.py and Whitepaper.html
  for more on the automatic backups and restore features added in releases 2.0
  and 2.1; "-backup" and "-restore" apply to "-auto" and [not "-report"] only,
  but this isn't error-checked here.  "-peek" is used by comparisons, and hence
  applies to all update modes.  "-quiet" applies only if "-backup" is used,
  and "-skipcruft" applies to all 3 run modes: "-report", "-auto", and neither.


SYNOPSIS: Synchronize "dirto" in-place to be the same as "dirfrom".

Merges directory tree (folder) "dirfrom" into directory tree "dirto" quickly,
by updating "dirto" in-place for just the items that differ between the trees.
This is useful for quick backups and managing multiple tree copies, and can
serve in some contexts as a manual alternative to cloud-based storage.

This Python 3.X/2.X command-line script performs one-way synchronization of
directory trees.  It may be run to update for all differences automatically
(if "-auto"); report differences only (if "-report"); or update differing
items selectively per console user interaction (if no "-auto" or "-report").

Differing items include both unique items and changed files.  Unique items
are found by tree content.  Changed files are normally detected by checking
just file modification-times and sizes.  The script may also inspect the
first and last bytes of files as an option (if "-peek"); can spawn a full
byte-wise comparison as a post-merge step (if "-verify"); can backup items
before they are destructively changed or removed (if "-backup"); can rollback
changes made by a prior run with backups (if "-restore"); and can skip
platform-specific metadata files and dirs in both trees (if "-skipcruft").

When allowed to perform updates, this script writes to "dirto" only the items
that are unique or changed in "dirfrom", and deletes items unique to "dirto".
The net effect synchronizes "dirto" to be the same as "dirfrom" quickly,
without changing "dirfrom" in any way, and without requiring complete tree
copies or full content compares.

New in [3.0]: If "-skipcruft" is passed, mergeall will skip platform-specific
cruft (metadata) files and dirs defined by patterns in mergeall_configs.py,
in both the FROM and TO trees.  Hence, they will not be reported, and in update
modes will never be copied to, deleted from, or replaced in the TO tree.  Cruft
is also skipped by cpall's copytree(), used here for bulk copies of FROM folders
to TO (but not for backup copies in backup.py).  When mergeall's "-skipcruft" is
used, FROM and TO will be the same after a merge, except for their unique cruft
files.  Platform-specific cruft is retained on the creating platform, but not
propagated to other copies and computers.  This is one way to deal with hidden
files generated by some operating systems (notably, Macs).  The related script
"nuke-cruft-files.py" here provides an alternative brute-force and more manual
solution.  See that script and mergeall_configs.py for more details.


PURPOSE

This script allows multiple local tree copies to synchronize their changes,
either to and from a common base, or between each other directly.  It was
written as an alternative to PP4E's cpall and diffall, and to avoid:

1) Long-running full copies and compares of large trees.  Such backups over
   USB 2.0 to flashdrives or other devices can take hours (the target use case
   was 50G, 30K files, 1700 dirs--photos, music, books, and everything else).
   
2) Relying on the semantics and interaction requirements of platform specific
   merges (e.g., drag-and-drop, cut-and-paste, swipe-and-pray).

3) Giving access to and control of important and private digital assets to
   cloud providers (and/or the NSA...).

Unlike brute-force copies, this script updates only for differences,
updates in-place, and allows selective updates via its interactive mode.
Unlike a typical Unix "cp -r" merge, this script copies to dirto only
differing items in dirfrom, and prunes unique items in dirto.  The net
effect allows typical mergeall runs to finish in roughly 1 minute.


USAGE PATTERNS

For trees with Unicode filenames, first run this (see explanation ahead):
    set PYTHONIOENCODING=utf8

--Quick check for differences only:
    mergeall.py [dir-path-1] [dir-path-2] -report  

--Quick check for differences only, slightly slower (for reads), save results:
    mergeall.py [dir-path-1] [dir-path-2] -peek -report > saveoutput
    notepad saveoutput
    
--Upload changes from working copy to common copy (backup/network drive?), automatic:
    mergeall.py [working-dir-path] [common-dir-path] -auto -backup > saveoutput
    notepad saveoutput
    
--Download changes from common copy to other (flashdrive?), interactive/selective:
    mergeall.py [common-dir-path] [other-dir-path] -backup

--Download changes from common copy to other, no change backups (trust devices):
    mergeall.py [common-dir-path] [other-dir-path] -auto 

--Synchronize changes to other work copies directly, automatic, no peek reads:
    mergeall.py [working-copy1-path] [working-copy2-path] -auto -backup

--Synchronize changes to other work copies directly, skipping all cruft files:
    mergeall.py [working-copy1-path] [working-copy2-path] -auto -backup -skipcruft

--Verify results after a merge:
    mergeall.py [dir-path-1] [dir-path-2] -report  (quicker, not byte-by-byte)
    diffall.py  [dir-path-1] [dir-path-2]          (slower, but more thorough)
    mergeall.py [dir-path-1] [dir-path-2] -verify  (runs diffall auto at end)
    diffall.py  [dir-path-1] [dir-path-2] -recent  (compare recent changes only)

--Rollback changes from an immediately preceding run with backups:
    mergeall.py archiveroot\__bkp__\dateyymmdd-timehhmmss archiveroot -auto -restore
    mergeall.py archiveroot\__bkp__\dateyymmdd-timehhmmss archiveroot -restore  

--------------------------------------------------------------------------------

OPERATION

This script's behavior consists of three phases, run in series:


1) COMPARISON PHASE

It first reports differences between dirfrom and dirto.  These include:

  --Unique items by name in either tree (both files and directories)
  --Same-named items that appear as file in one tree and directory in the other
  --Differing same-named files
  
The latter by default is detected by checking just the files' modification
date/times, and sizes.  If "-peek" is used, the detection also compares just
the first and last 10 bytes of each file (or < 10 for very small files).
This makes it slightly slower, but not nearly as slow as full content reads.

This is not 100% accurate, but suffices for tree merges, and yields a much
quicker comparison than the byte-for-byte scans of diffall (whose output
is also too terse to parse and use here in any event).

[Version 2.2 speeds the comparison phase with scandir() when using Python 3.5+
or a PyPI install: see Revisions.html.]

[Version 3.0's "-skipcruft" ignores cruft files in both TO and FROM during this
phase, so they are not reported, copied, deleted, or replaced; see above.]


2) RESOLUTION PHASE

If directed to do so, the script then resolves all the differences in dirto,
such that dirto is made the same as dirfrom, but dirfrom is unchanged.
That is, dirto becomes a "mirror" of dirfrom, by the following updates,
run in the following order ("items" means both files and directories):

  a) Differing same-named files are copied from dirfrom to dirto
  b) Unique items in dirto are removed from dirto
  c) Unique items in dirfrom are copied to dirto
  d) Mixed-mode same-named items are replaced in dirto by their dirfrom version

As these updates are fully disjoint (a name can appear in only one category),
they cannot interfere with each other's correctness, though order matters for
renames on case-insensitive platforms like Windows (deletes must precede adds).

The command-line "-auto" option directs the script to perform all these updates
automatically.  Otherwise, the user is asked for confirmation of each update
interactively, and may run updates selectively.  Updates change dirto in-place,
but impact differing items only, and this yields a much quicker backup than the
full tree copies of cpall (or drag-and-drops or other).

Mixed-mode items are replaced in dirto only if they are a file/dir or dir/file
mix; other mixed-mode cases and unknown-mode uniques are ignored (and may include
FIFOs on some platforms, but not Unix symlinks which are always copied instead of
followed as of 3.0: see TBD ahead).

All file errors during resolution are caught and reported, and do not end the
script; scan its results for "**Error".  This error message pattern is used both
for top-level file errors here, as well as for file error messages during the
recursive folder copy in cpall.copyfile(), and errors during the comparison phase
(which terminate the run before updates).  Any resolution failures skipped also
register as differences on the next run.

As of version 2.0, prior versions of items (both files and directories) replaced
or removed during the resolution process are automatically backed-up to the TO
archive's __bkp__ folder, if the new "-backup" flag is used.  See TBD 3 ahead.

As of version 2.1, resolution can also be run in "-restore" mode to rollback
changes made by a prior run with backups enabled.  This mode merges from
backup to archive root, omitting step (b) above, and removing items added by
the prior run's step (c).


3) VERIFICATION PHASE

If "-verify" is used, also runs a byte-for-byte diffall.py comparison as a post
step, to verify results.  The diffall summary appears at end of its output, and
should show "No diffs found." at the end if the merge was successful; search
this output for "*DIFFER" and "*UNIQUE" strings for further diff details.

Note that you can generally skip the (possibly very) slow -verify diffall step,
and simply rerun with -report to view any lingering diffs; this report differs
in form and semantics, but contains the same data.  In practice, diffall may be
better run rarely and by separate command lines, than as part of each mergeall.


MORE DETAILS

See test\expected-output-3.0 for recent logs with example commands and output.
See examples\{Logs, _older\other\mergeall-run.txt} for example commands and output.

This script runs on Python 3.X and 2.X.  It should be platform neutral, but
has been tested only on Windows to date.  [Update: this system has now also been
verified to work on Linux for basic file types, per release 1.5 notes in Revisions.html.]
[Update: 3.X is recommended for Unicode filenames, and 3.5 for speed; see Revisions.html.]

TIP: set environment variable PYTHONIOENCODING=utf8 (or other) in your shell or
Control Panel if you receive Unicode errors when scripts like mergeall.py attempt 
to print non-ASCII filenames on your platform.  This manual setting isn't required
for the GUI launcher, as it automatically sets and propagates this variable to its
mergeall.py subprocess, and does not route text to a console (only to a GUI and a
logfile).  However, this setting may be required for both the console launcher,
and mergeall.py run directly from a command line -- because both print filenames to
the console, visiting any file with a non-ASCII name may otherwise abort these 
scripts, especially in 3.X. 

Reuses some PP4E book examples: diffall.py logic, and cpall.py file and dir tree
copiers, though the latter required extension to call shutil.copystat() to also copy
file modification times after file content, so that files are the same when later
compared again here (see 2.X caveat ahead).  shutil.copy2() would work too, but
PP4E code reuse was a goal.  Also added __future__ imports of print_function for
2.X in cpall and diffall; these are 2.X compatible with this insert.  [[1.7.1]:
also extended cpall's file error message text slightly to match that here.]

--------------------------------------------------------------------------------

CAVEAT 1: file timestamp dependence

As is, this script relies on the integrity of file modification times (a.k.a.
"modtimes").  It's not impossible that these may be skewed by some devices to
which a backup is written.  If this occurs, the worst this can do is cause a
file to be spuriously classified as a difference, and harmlessly written over
its identical copy in dirto.

If this is problematic, though, edit the comparefiles() function's modtimes
logic.  In the worst cases, this function could be changed to abandon file
modtimes, and use some sort of checksums, or read/compare full file contents
instead (see the file matching logic in diffall.comparetrees() for pointers).
Even full reads would likely still be quicker than a full tree copy, though,
as most devices today read much faster than they write. 

  UPDATE: FAT 2-second issue

  Version 1.3 was patched to allow for the FAT32 file system's 2-second
  file modification time granularity, else files stored on the more accurate
  NTFS file system always mismatch by modtimes and are classified as diffs.
  
  Prior to the fix, the same file on NTFS and FAT32 could register a bogus
  mismatch: NTFS on hard drives gives fractional second accuracy on Windows,
  but FAT32 on USB flashdrives always truncates file modtime fractional parts,
  and usually rounds up to the next multiple of 1 or 2 -- even immediately
  after a mergeall or drag-and-drop copy from NTFS (c:) to FAT32 (e:):

  >>> os.path.getmtime(r'c:\MY-STUFF\__more__\Memos\tablet-issues.txt')
  1393450444.1208856
  >>> os.path.getmtime(r'e:\MY-STUFF\__more__\Memos\tablet-issues.txt')
  1393450446.0
  
  >>> os.path.getmtime(r'c:\MY-STUFF\__more__\calendar\trips.ics')
  1393428663.0284016
  >>> os.path.getmtime(r'e:\MY-STUFF\__more__\calendar\trips.ics')
  1393428664.0

  It is possible to work around this by copying from FAT32 back to NTFS
  redundantly (after copying from NTFS to FAT32), by rerunning with swapped
  to/from roles to make time just stamps the same, but that was inconvenient.
  The fix allows for a match if times are +/- 2 seconds, which may miss some
  very unusual diffs, but compares without modtimes based on limited reads or
  checksums will be slower.

  UPDATE: FAT DST rollover issue
  
  Version 1.4's Revisions.html notes describe an issue regarding FAT32 filesystem
  modtimes being off by 1 hour (versus NTFS and exFAT) after daylight savings
  time (DST) has been automatically adjusted.  This is a well-known Windows
  issue with no easy fix; the best solution seems to be to disable your DST
  auto-adjust on Windows and adjust your time/clock manually when needed;
  the next best solutions may be to either allow timestamp-based backup tools
  like mergeall to rewrite your full archive twice a year (not ideal, but rare),
  or keep two FAT archive copies--one used when DST is in effect, and one used
  when it is not (which also automatically promotes long-term backups).  See
  UsrGuide.html for other workaround ideas.  NEW: see also the workaround script
  fix-fat-dst-modtimes.py, added in version 2.0.

  UPDATE: Excel (and others?) may change content but not modtime

  It's been observed that Excel (and possibly others?) can sometimes change
  file content bytes without updating file size or modification time.  This
  happens on Windows, and occurs even if a file is simply opened and closed.
  The result is that diffall.py's full content bytes comparison detects and
  reports the difference, but mergeall.py's time/size metadata (and optional
  limited 'peek' bytes) comparison does not.  This seems to happen only for
  metadata that's almost certainly harmless and unimportant, but there is no
  known fix for mergeall, short of manually replacing files that report diffs
  in a byte-wise diffall.py run.  For an illustration of this in Python, see:
      examples\issues\excel-covert-changes-issue.txt
  
  UPDATE: Linux/Windows NTFS cross-platform merge DST issue
  
  On Linux, when comparing trees on mounted Windows NTFS volumes to trees
  on Linux volumes, there may be an issue related or similar to the FAT
  DST rollover issue described above, which skews some NTFS mod times by an
  hour (and hence generates spurious mergeall differences).  The best solution
  so far is to simply synch once to remove the differences.  See release 1.5's
  second "Linux Usage Note" in Revisions.html for more details, and the following
  file for a demo of this issue in Python:
      examples\issues\linux-ntfs-dst-issue.txt
      
----

CAVEAT 2: one-way versus two-way synchronization

This script is a one-way merge and prune.  It assumes there is just 1 "golden"
base version of a tree that all other copies are made to mirror, either by merging
changes to and from a common base copy, or by merging to other copies directly.
Changes in a local copy may be uploaded to and from the base copy(s) quickly,
but all bets are off if the same file is changed in multiple trees before
synchronizing them with the base.

If this won't suffice, run with just -report to see differences and resolve
manually, or run without -auto to resolve items on a case-by-case basis by
interactive input.  A more peer-level and bi-direction automatic union merge
mode would fail to allow for renames and deletes, and multiple edited copies
probably encroach on the domain of full source control systems in general.

  UPDATE: It is possible to use this one-way merge to perform peer-level and
  two-way synchronizations after all, by simply running _twice_ in interactive
  and selective mode, with swapped to/from roles -- choose one tree's diffs
  on the first run, and the other's on the second.  For more details on this
  process, see file Whitepaper.html in this system's docetc/MoreDocs folder.

----

CAVEAT 3: 2.X compatibility and file modtimes

This was coded to also work on Python 2.X, but requires os.stat_float_times(False)
to work on 2.X.  This call forces file modtimes to be truncated integers instead
of floats (losing second fractions, irrelevant here).  This works around a bug
in Python 2.7's shutil.copystat(), which copies file modtimes with a different
precision than that in the original file (a low exponent digit differs):

  >>> import os
  >>> os.path.getmtime(r'test\test1\f1.txt')  # original file
  1391819917.6508296
  >>> os.path.getmtime(r'test\test2\f1.txt')  # copy, modtime differs if made in 2.X
  1391819917.650829                           # (but same as original if made in 3.X)

This in turn makes all future comparisons register a difference here.  By
truncating modtime return values to ints on both 3.X and 2.X, the code here
is portable and works on both 3.X and 2.X as is.

The os.stat_float_times() call is today marked as "deprecated in 3.3"; if it's
ever removed from 3.X, the call here will automatically be replaced with a manual
truncation of os.path.getmtime() results.  This may be a simpler solution in
any event, and avoids storing truncated modtimes in file copies made in 2.X (only).

  UPDATE: note that truncating fractional parts of mod times is not enough to
  address the 2-second granularity of the FAT32 file system, described earlier,
  even if the truncated times are pushed out to disk (they seem to be in 2.X).

----

CAVEAT 4: directory removals may fail on Windows due to pending deletes [2.0]

On Windows, deletes may sometimes not be finalized immediately -- they are left
still pending after the delete call returns (perhaps due to other activities).
This is lethal to shutil.rmtree, because directories cannot be removed until
after all their contents are removed.  Version 2.0 adds a workaround that waits
temporarily, retrying shutil.rmtree's os.rmdir directory removal calls that fail.
The operation can still fail, however, leaving log messages, and a difference to
be resolved on the next run: harmless, but less than ideal.  This is very rare
(and may warrant additional research); see Revisions.html for more details.

  UPDATE: [3.0] experimented with - but did not use - code that extends the
  shutil.rmtree error handler to first try to correct read-only items and
  rerun the failed operation, before trying the preceding workaround.
  Read-only failures seem an oddly-common issue on windows, but permisssions
  should be changed by users only.  See backup.py for this disabled code.

--------------------------------------------------------------------------------

TBD 1: symlinks? [RESOLVED]

This code may need some honing on platforms with symlinks and other esoteric
filesystem entries.  As is, these may be skipped in both trees: uniques and mixes
both process only files and dirs (per Python's libs), and report other types skipped.
Skipped and unreadable items don't terminate the script, but could return as
unresolved differences in future runs.  However, this depends on the semantics
of Python's os.isfile()/isdir() results, which may follow symlinks on some platforms
(uddate: both return _True_ for Unix symlinks).  See Python's manuals and test on
your machine; this script has been used on only Windows to date.

  UPDATE: per Revisions.html's release 1.5 notes, the GUI/console launchers and
  main script are now known to run well on Linux for basic file/directory trees,
  though further testing of more exotic file types is still pending.

  UPDATE: version [3.0] finally resolved this point as part of its Mac OS X port.
  For Unix symbolic links to both files and dirs, mergeall now always copies the
  link itself, instead of following it.  Else, archives with intra-archive links
  will wind up with multiple copies of the linked data.  Assumes symlinks are
  relative, or else they may not work on a different machine.

  Windows symlinks are complex and remain untested and TBD; they should work with
  the code here as is if the target of the link exists.  Also note that FIFO files
  are False for _both_ isfile() and isdir() (and stat analogy), so they won't be
  copied here unintentionally.  For more background details, see this session log:
      docetc/miscnotes/demo-3.0-unix-symlinks.txt.
  
----

TBD 2: remaining Unicode issues? [ADDRESSED]

This script may need to address Unicode filenames on some platforms, perhaps by using
already-encoded bytes filenames in os.listdir().

  UPDATE: in version 1.2, encoding of streams in the processes spawned by the
  GUI and console launchers are forced to agree with subprocess.Popen decoding,
  by setting the inherited PYTHONIOENCODING shell variable; this handles filenames
  in those streams, but does not address all filename contexts.

  UPDATE: in version 1.4, this was patched again to force the mergeall subproc
  to print in UTF8, use binary-mode stream reads for Popen, and manually decode
  per UTF8 in launchers after the read; this allows both mergeall and Popen to
  handle Unicode filenames in messages.

  UPDATE: in version 1.6, the GUI launcher was patched for rare 2.X decoding errors
  for non-ASCII characters in filenames.  See the GUI launcher's code file for details.
  Note that this patch applies only to the GUI launcher's display: PYTHONIOENCODING 
  must still be set manually in your system shell when running script mergeall.py 
  directly from a command line, if it may ever process and thus print non-ASCII 
  filenames, especially in 3.X.

  UPDATE: for version 1.7, Revisions.html includes a Usage Note about different folder
  names being treated the same by Windows if they are the same after Unicode
  accents are dropped.  See Revisions.html's version history for details/workaround.
  =>
    REUPDATE: release 1.7.1 updated this note to clarify that this problem occurs
    only on FAT32 filesystems (of the sort used by USB flash drives), and only if
    a non-accented name is copied before an accented and otherwise equivalent name.
    No automatic workaround is yet known, but this is a very rare and unusual event;
    manually merge folders or manually copy in the desired order if this occurs.
  
----

TBD 3: auto backups? [RESOLVED]

An auto-backup copy feature is half-coded here, but was not implemented (it's not
clear if this is desirable, and not clear how/when to dispose of the backups).
Backup your trees manually first if you don't trust or want this script's results.

  UPDATE: version 2.0 adds automatic update of changed items, via the mergeall
  "-backup" argument, and corresponding widgets and prompts in the GUI and console
  launchers, respectively.  Changed items include files and folders replaced or
  deleted in-place.  New items copied to TO are not updated, as this is not a
  destructive change.  Backups are kept in per-run folders in a top-level __bkp__
  folder, and pruned automatically.  This makes mergeall generally safer: if needed,
  files may be restored from any of the latest mergeall run backups in the __bkp__
  of any archive copy.  See Revisions.html, backups.py, and Whitepaper.html
  for more details.

  UPDATE: version 2.1 further extended this model to support automatic rollback of
  all changes made by a prior run with backups enabled, including new items added.
  It restores replacements and removals, and removes additions.  A new file
  __bkp__/__added__.txt logs additions.  See the same sources for more details.

----

TBD 4: drop the copystat() hack? [RESOLVED]

The cpall.copyfile()/copytree() examples from PP4E were extended here to call
shutil.copystat() to copy modtimes too, but this was done in an unusual way
(a.k.a. "monkeypatching").  This works, and reuses book examples intact, but
copyfile() could be changed in-place to do this as an option.

  UPDATE: Done -- version 2.0 changed cpall.copyfile in-place to call copystat
  by default; original code retained in quotes below as an example (and lesson).

----

TBD 5: counters? [RESOLVED]

Some counts/statistics may be useful additions to the report.

  UPDATE: Done -- version 2.0 adds counts for both comparison and
  resolution phases, and displays at the run's end.  [Update: 2.2
  now also displays runtimes for each mergeall phase.]

--------------------------------------------------------------------------------

PSEUDOCODE (original design):

For differences (by modtime, size, or limited content tests),
reports only if "-report"; else at each common directory in
the two directory trees:

  For differing same-named files:
      if -auto, copies dirfrom file to dirto
      else asks if should use dirto or dirfrom version, or ignore
          if use dirto,   takes no action
          if use dirfrom, copies dirfrom file to dirto 

  For unique files in dirfrom:
      if -auto, copies dirfrom file to dirto
      else asks if should do auto action, else ignore
  For unique files in dirto:
      if -auto, deletes dirto file
      else asks if should do auto action, else ignore
      
  For unique dirs in dirfrom:
      if -auto, copies dirfrom tree to dirto
      else asks if should do auto action, else ignore
  For unique dirs in dirto:
      if -auto, deletes dirto tree
      else asks if should do auto action, else ignore

  For same-named items that are both file and dir (rare):
      if -auto or (ask user if should use dirfrom version)
          if dirfrom is a dir
              deletes dirto file, copies dirfrom tree to dirto
          if dirfrom is a file
              deletes dirto tree, copies dirfrom file to dirto
          else
              ignore: the names may be something else (fifos?, not symlinks) 
      else takes no action

There naturally are alternative algorithms (e.g., resoution might just
delete item in TO (file or dir) and then copy item on FROM (dir or file),
but they may lead to redundnt steps and less-intuitive action reporting.
================================================================================
"""

#
# CODE STARTS HERE
#

from __future__ import print_function         # Py 2.X compatibility
import os, sys, pprint, shutil                # shutil has rmtree (and copystat)
if sys.version[0] == '2': input = raw_input   # Py 2.X compatibility

# reuse PP4E book examples
from diffall import intersect                 # in both a and b, retains order
from dirdiff import difference                # in a but not b, retains order
from cpall   import copyfile, copytree        # copy utils, with own trace/trys

# [2.0/2.1] automatic backups/restores extensions
import backup                                 # save change/deleted files/dirs in TO 

# [3.0] support long pathnames on Windows
from fixlongpaths import OPEN                 # or 'as open', but too obscure 

# [3.0] filter out system metadata files
from skipcruft import filterCruftNames, filterCruftDirentrys   

traceLevel = 1  #2=more, 0=less
def trace(level, *args, **kargs):
    if level <= traceLevel: print(*args, **kargs)



# use ints for modtimes (losing fractions of a second), not floats;
# else shutil.copystat() values differ in copied files in Py 2.X (only);
# stat_float_times deprecated in Py 3.3: if gone, simply trucate modtimes

if hasattr(os, 'stat_float_times'):           # use while it lasts?
    os.stat_float_times(False)                # 2.X compatibility (fix)
else:
    orig_getmtime = os.path.getmtime
    os.path.getmtime = lambda path: int(orig_getmtime(path))



# sums for comparison and resolution phases (reusable coding) [2.0]
class Totals:
    """
    a collection of named sums that display nicely;
    each sum is an attribute of the instance object;
    """
    def __init__(self, *sums):
        for name in sums:
            setattr(self, name, 0)
    def __str__(self):
        return ', '.join(('%s: %d' % kvpair)
                         for kvpair in sorted(self.__dict__.items()))

class MultipleTotals:
    """
    a collection of named Totals that display nicely;
    each Total is an attribute of the instance object;
    """
    def __init__(self, kinds, sums):
        for name in kinds:
            setattr(self, name, Totals(*sums))
    def __str__(self):
        maxlen = max(len(k) for k in self.__dict__.keys())
        return '\n'.join(('%s => %s' % (k.ljust(maxlen), v))
                         for k, v in sorted(self.__dict__.items()))

# e.g., countcompare.files, countresolve.files.replaced 
countcompare = Totals('files', 'folders')
countresolve = MultipleTotals(('files', 'folders'), ('replaced', 'deleted', 'created'))

# [3.0] for summary indicator line; global because too many parameters already
import cpall                # errors in copytree()
anyErrorsReported = False   # errors printed here




"""..................................................................
RIP: This following was blatantly-evil monkeypatching: instead,
changed cpall.copyfile in-place to call copystat by default [2.0];

# must copy file _and_ its modtime, else always differs here;
# this is a bit of a hack, but reuses book examples intact

import cpall
cpall_copyfile = cpall.copyfile        # save original

def copyfile(pathfrom, pathto):
    cpall_copyfile(pathfrom, pathto)   # copies file content
    shutil.copystat(pathfrom, pathto)  # extend with modtime step

cpall.copyfile = copyfile              # reset for cpall.copytree
copytree = cpall.copytree              # ...which runs copyfile here
....................................................................."""


    
################################################################################
# analyze trees: Python 3.4 and earlier => use portable os.listdir() names
################################################################################


def comparedirs(dirfrom, dirto, namesfrom, namesto, uniques):
    """
    -----------------------------------------------------------------------------
    Compare directory contents, but not actual files, changing uniques in-place.
    dirfrom is not needed for uniques['to'] here, but noted for reporting.
    
    This comparison is by filename text, without normalizing case on case
    insensitive platforms (e.g., Windows).  This is deliberate, so that
    file renames trigger a delete of the old followed by an add of the new
    when merged.  Normalizing case would trigger same-files for mixed case,
    not uniques, and wouldn't implement the rename.

    [2.0] moved listdir call here to comparetrees; no need to return lists.
    -----------------------------------------------------------------------------
    """
    countcompare.folders += 1
    uniquefrom = difference(namesfrom, namesto)
    uniqueto   = difference(namesto, namesfrom)
    if uniquefrom:
        uniques['from'].append((uniquefrom, dirfrom, dirto))
    if uniqueto:
        uniques['to'].append((uniqueto, dirfrom, dirto))



def comparefiles(name, dirfrom, dirto, diffs, dopeek=False, peekmax=10):
    """
    -----------------------------------------------------------------------------
    Compare same-named files by modtime and size, and possibly by start+stop
    bytes read (up to min file size) if dopeek, changing diffs in-place.
    Test are run in series until the first difference is found, or all have
    been tried.  This is not 100% accurate (and is subject to filesystem
    diffs), but avoids full reads, and is sufficient for synching large trees.

    Uses binary byte files to prevent Unicode decoding and endline transforms,
    as trees might contain arbitrary binary files as well as arbitrary text.
    Requires shutil.copystat() to also copy file modtimes, else copied files
    will still always differ here; see hack to reused copy utilities above.

    Update: version 1.3 allows for 2-second modtime granularity in FAT32 file
    system (as well as NTFS's fractional seconds), by using a +/- 2-second range
    test instead of !=.  Modtime timestamps are returned in seconds, possibly
    truncated.  See details in the CAVEATs section of this file's docstring.
    -----------------------------------------------------------------------------
    """
    def modtimematch(pathfrom, pathto, allowance=2):    # [1.3] 2 seconds for FAT32
        time1 = os.path.getmtime(pathfrom)
        time2 = os.path.getmtime(pathto)
        return time2 >= (time1 - allowance) and time2 <= (time1 + allowance)

    countcompare.files += 1     
    startdiffs = len(diffs)
    pathfrom   = dirfrom + os.sep + name                         # [3.0] not os.path.join
    pathto     = dirto   + os.sep + name
    
    if not modtimematch(pathfrom, pathto):                       # try modtime 1st
        diffs.append((name, dirfrom, dirto, 'modtime'))          # the easiest diff

    else:                                                        
        sizefrom = os.path.getsize(pathfrom)                     # try size next
        sizeto   = os.path.getsize(pathto)                       # unlikely case
        if sizefrom != sizeto:
            diffs.append((name, dirfrom, dirto, 'filesize'))
            
        elif dopeek:                                             # try start+stop bytes
            peeksize = min(peekmax, sizefrom // 2)               # scale peek to size/2
            filefrom = OPEN(pathfrom, 'rb')                      # sizefrom == sizeto
            fileto   = OPEN(pathto, 'rb')
            if filefrom.read(peeksize) != fileto.read(peeksize):
                diffs.append((name, dirfrom, dirto, 'startbytes')) 
            else:
                filefrom.seek(sizefrom - peeksize)
                fileto.seek(sizeto - peeksize)
                if filefrom.read(peeksize) != fileto.read(peeksize):
                    diffs.append((name, dirfrom, dirto, 'stopbytes'))
            filefrom.close()
            fileto.close()
    return len(diffs) == startdiffs    # true if did not differ, else extends 'diffs'



def comparetrees(dirfrom, dirto, diffs, uniques, mixes, dopeek, skipcruft, skip=None):
    """
    -------------------------------------------------------------------------
    Compare all subdirectories and files in two directory trees, noting
    differences in-place in diffs, uniques, and mixes, for later updates.
    TBD: Permission error exceptions here end this script; should they?
    
    [2.0] Added skip argument for __bkp__ at top of archives, and moved
    os.listdir calls from comparedirs to here to make removals possible.
    May need bytes listdir arg for undecodable filenames on some platforms.

    [3.0] Added skipcruft arument and code for the new "-skipcruft" option
    described near the top of this file, and in the UserGuide.html document.

    [3.0] Coding note: any exceptions during the comparison phase (e.g., for
    permission errors on listings here) are deliberately ignored, and allowed
    to terminate the run.  Else, error message in this phase's log would be 
    too easy to miss, and failed folders would go silently unprocessed.
    But these are now caught at the top-level and reported (see __main__).

    [3.0] Optimization: don't scan the 'common' list more than once, but
    recur into subdirs immediately (unlike diffall, there is no need to
    postpone subdirs recursion here, because we're building difference
    data structures to be used later).  This automatically avoids calling
    os.path.join() twice on each item name, and halves big-O complexity
    in both this and its 3.5+ optimized variant ahead.

    [3.0] Optimization: also replace os.path.join() calls here with +os.sep+.
    os.path.join() is complex and slow overkill for known path+file cases,
    expecially on Windows (see Python's Lib\ntpath.py).  Also replaced in
    comparefiles() above (the savings for passing paths instead is likely
    trivial).  This was not required in the 3.5+ os.scandir() variant.
 
    OPTIMIZATION RESULTS: the prior 2 changes reduced comparison-phase time
    for an 87G SSD tree with 59k files and 3.5k dirs from 19 to 14 seconds
    on Pythons 3.4 and older (which use os.listdir()), but did not impact
    a 7.2 second runtime on Pythons 3.5+ (which use an os.scandir() variant
    that fully accounts for its faster speed).  Thus, 5 seconds were shaved
    in Pythons 3.4-, but filesystem call overheads overshadow code here in
    the 3.5+ variant's case.  Moreover, nearly all of the 5 second 3.4- gain
    is due to reduced 'common' scans, not os.path.join() removal.  For a
    typical results set, see test/expected-output-3.0/optimizations-3.0/
    mergall-results.txt; its relative findings are immune to test variables.
    Caveat: tested on Windows only; os.scandir() is not used on Mac OS X.
    -------------------------------------------------------------------------
    """
    def excludeskips(dirfrom, dirto, namesfrom, namesto, skip):
        """
        Remove __bkp__ changes-backup folders at top-level only [2.0].
        Could use set difference, but want to retain filesystem order,
        or [name for name in nameslist if name != skip], but extra copies.
        Could be used to exclude other items too, but currently is not.
        
        Update: [3.0]'s later "-skipcruft" added a more general filter
        which might have included __bkp__ if it was available earlier,
        but __bkp__ is a mandatory pass and crufts are user-configurable
        (though we could have always inserted __bkp__ in mergeall's code);
        """
        if skip and skip in namesfrom:
            trace(1, 'excluding', os.path.join(dirfrom, skip))
            namesfrom.remove(skip)
        if skip and skip in namesto:
            trace(1, 'excluding', os.path.join(dirto, skip))
            namesto.remove(skip)

    trace(2, '-' * 20)
    trace(1, 'comparing [%s] [%s]' % (dirfrom, dirto))
        
    # get dir content lists here
    namesfrom  = os.listdir(dirfrom)                            # [1.7] or pass bytes?
    namesto    = os.listdir(dirto)                              # would impact much
    excludeskips(dirfrom, dirto, namesfrom, namesto, skip)

    # [3.0] filter out system metadata files and folders
    if skipcruft:
        namesfrom = filterCruftNames(namesfrom)
        namesto   = filterCruftNames(namesto)

    # compare dir file name lists to get uniques  
    comparedirs(dirfrom, dirto, namesfrom, namesto, uniques)

    # analyse names in common (same name and case)
    trace(2, 'comparing common names')
    common = intersect(namesfrom, namesto)
    
    for name in common:                            # scan common names just once [3.0]
        pathfrom = dirfrom + os.sep + name         # avoid os.path.join overkill [3.0]
        pathto   = dirto   + os.sep + name

        # 1) compare contents of files in common 
        if os.path.isfile(pathfrom) and os.path.isfile(pathto):
            comparefiles(name, dirfrom, dirto, diffs, dopeek)
                           
        # 2) compare subdirectories in common via recursion
        elif os.path.isdir(pathfrom) and os.path.isdir(pathto):
            comparetrees(pathfrom, pathto, diffs, uniques, mixes, dopeek, skipcruft)

        # 3) same name but not both files or dirs
        else:
            mixes.append((name, dirfrom, dirto))



################################################################################
# analyze trees: Python 3.5 and later => use faster os.scandir() objects [2.2]
################################################################################


#-------------------------------------------------------------------------------
# Use optimized variant if scandir() available _and_ faster for comparisons:
# Windows:
#    In mergeall, scandir is faster - 5X to 10X before 3.0 optimizations,
#    and 2X faster after: 7 sec vs 14 secs for a large 87G 58k-file archive. 
# Linux:
#    The scandir() variant is 2X faster on Linux post 3.0 optimizations:
#    30 secs vs 60 secs for the same large archive (on a slow test machine).
# Mac OS X:
#    [3.0] BUT the scandir() variant is 3X SLOWER on Mac OS X! - it takes
#    6 secs vs 2 secs for the same 87G 58K-file archive (on a fast machine),
#    with the 3.0 coding optimizations described above.  DON'T USE ON MACS.
# Not just: float(sys.version[:3]) >= 3.5; scandir() can be a separate install.
#-------------------------------------------------------------------------------

if not hasattr(os, 'scandir'):          # older Pythons (2.7+): no os.scandir
    try:
        import scandir                  # check for PyPI package install
        os.scandir = scandir.scandir    # store in os, and assume same API
    except:
        pass                            # punt: use Py 3.4- verions above

if (hasattr(os, 'scandir')                              
    and not sys.platform.startswith('darwin')):   # [3.0] not on Mac OS X: slow! 
    """
    ------------------------------------------------------------------------
    [2.2] Custom comparison code using os.scandir() instead of os.listdir().
    SEE ORIGINAL 3.4 AND EARLIER VERSIONS ABOVE for docs not repeated here.
    
    os.scandir() provides an object API (versus name lists), that can often
    eliminate system calls for attributes such as type, modtime, and size.
    This can speed mergeall's comparison phase by a factor of 5 to 10 on
    Windows.  This speedup is entirely due to os.scandir(), not 3.5 in
    general, and can shave dozens of seconds off total runtimes for larger
    archives (and more on slower devices).

    POSIX systems also run quicker, according to this Python 3.5 change's PEP,
    benchmark, and documentation.  [UPDATE: Not so! => os.scandir() is faster
    on Linux too, but SLOWER on Macs - 3X slower in mergeall; see above.]

    This speeds up the comparison phase only, but this phase can dominate
    runtimes in typical runs on large archives.  The resolution phase was
    not changed, because it normally visits just a handful of file paths
    (changed items only), and is bound by basic file write/delete speed.

    Note: diffall.py might benefit from os.scandir() too for path names,
    but it's less likely, as that script doesn't fetch modtimes or sizes,
    and is bound by the time required to fully read all common files.
    
    Note: scandir() is also available in a scandir module for older Pythons,
    including 2.7, via a PyPI package.  If installed, the code here imports
    and uses it, and so should work with older Pythons too -- not just 3.5+.

    TBD: factor-out differing parts better to avoid some redundant code?
    They seem too different in structure to factor well, and factoring
    may slow either or both versions, negating this extension's goal.
    ------------------------------------------------------------------------
    """
    if __name__ == '__main__':
        trace(0, 'Using Python 3.5+ os.scandir() optimized variant.')



    def comparedirs(direntsfrom, direntsto, dirfrom, dirto, uniques):
        """
        [2.2] python 3.5+ custom version using faster os.scandir().
        Doesn't use set difference here, to maintain listing order.
        Note: dirfrom and dirto pathnames still used by resolver phase.
        """
        trace(2, 'dirs:', dirfrom, dirto)

        countcompare.folders += 1
        uniquefrom = [df.name for df in direntsfrom
                          if df.name not in (dt.name for dt in direntsto)]
        uniqueto   = [dt.name for dt in direntsto
                          if dt.name not in (df.name for df in direntsfrom)]
        if uniquefrom:
            uniques['from'].append((uniquefrom, dirfrom, dirto))
        if uniqueto:
            uniques['to'].append((uniqueto, dirfrom, dirto))


    
    def comparefiles(direntfrom, direntto, dirfrom, dirto, diffs, dopeek=False, peekmax=10):
        """
        [2.2] python 3.5+ custom version using faster os.scandir().
        Uses stat() objects for sizes+times, perhaps avoiding sysytem calls.
        Note: dirfrom and dirto pathnames still used by resolver phase.
        """
        trace(2, 'files:', direntfrom.path, direntto.path)
        
        def modtimematch(statfrom, statto, allowance=2):      # [1.3] 2 seconds for FAT32
            time1 = statfrom.st_mtime                         # [2.2] os.stat_result object
            time2 = statto.st_mtime
            return time2 >= (time1 - allowance) and time2 <= (time1 + allowance)

        countcompare.files += 1     
        startdiffs = len(diffs)
        
        name     = direntfrom.name                                   # same name in from and to
        statfrom = direntfrom.stat()                                 # call stat() just once
        statto   = direntto.stat()
        
        if not modtimematch(statfrom, statto):                       # try modtime 1st
            diffs.append((name, dirfrom, dirto, 'modtime'))          # the easiest diff

        else:                                                        
            sizefrom = statfrom.st_size                              # try size next
            sizeto   = statto.st_size                                # unlikely case
            if sizefrom != sizeto:
                diffs.append((name, dirfrom, dirto, 'filesize'))
                
            elif dopeek:                                             # try start+stop bytes
                peeksize = min(peekmax, sizefrom // 2)               # scale peek to size/2
                filefrom = OPEN(direntfrom.path, 'rb')               # sizefrom == sizeto
                fileto   = OPEN(direntto.path, 'rb')
                if filefrom.read(peeksize) != fileto.read(peeksize):
                    diffs.append((name, dirfrom, dirto, 'startbytes')) 
                else:
                    filefrom.seek(sizefrom - peeksize)
                    fileto.seek(sizeto - peeksize)
                    if filefrom.read(peeksize) != fileto.read(peeksize):
                        diffs.append((name, dirfrom, dirto, 'stopbytes'))
                filefrom.close()
                fileto.close()
        return len(diffs) == startdiffs    # true if did not differ, else extends 'diffs'



    def comparetrees(dirfrom, dirto, diffs, uniques, mixes, dopeek, skipcruft, skip=None):
        """
        [2.2] python 3.5+ custom version using faster os.scandir().
        Doesn't use set intersection here, to maintain listing order.
        """
        trace(2, 'trees:', dirfrom, dirto)
        
        def excludeskips(direntsfrom, direntsto, skip):     # [3.0] pre-skipcruft filter 
            if not skip:
                return
            for dirents in (direntsfrom, direntsto):
                matches = [dirent for dirent in dirents if dirent.name == skip]
                if matches:
                    assert len(matches) == 1
                    trace(1, 'excluding', matches[0].path)
                    dirents.remove(matches[0])

        trace(2, '-' * 20)
        trace(1, 'comparing [%s] [%s]' % (dirfrom, dirto))
            
        # get dir content lists here                        # [2.2] os.DirEntry objects iterator
        direntsfrom = list(os.scandir(dirfrom))             # [2.2] need list() for multiple scans! 
        direntsto   = list(os.scandir(dirto))               # or pass bytes?--would impact much
        excludeskips(direntsfrom, direntsto, skip)

        # [3.0] filter out system metadata files and folders
        if skipcruft:
            direntsfrom = filterCruftDirentrys(direntsfrom)
            direntsto   = filterCruftDirentrys(direntsto)

        # compare dir file name lists to get uniques 
        comparedirs(direntsfrom, direntsto, dirfrom, dirto, uniques)

        # analyse names in common (same name and case)
        trace(2, 'comparing common names')
        common = [(df, dt) for df in direntsfrom
                               for dt in direntsto if df.name == dt.name]

        # scan common list just once [3.0]
        for (direntfrom, direntto) in common:

            # 1) compare contents of files in common
            if direntfrom.is_file() and direntto.is_file():
                comparefiles(direntfrom, direntto, dirfrom, dirto, diffs, dopeek)
                               
            # 2) compare subdirectories in common via recursion
            elif direntfrom.is_dir() and direntto.is_dir():
                comparetrees(direntfrom.path, direntto.path,
                             diffs, uniques, mixes, dopeek, skipcruft)

            # 3) same name but not both files or dirs
            else:
                mixes.append((direntfrom.name, dirfrom, dirto))  # same name in both



################################################################################
# reconcile trees
################################################################################


def mergetrees(diffs, uniques, mixes,
               doauto, dobackup, toroot, dorestore, fromroot, quiet, skipcruft):
    """
    ------------------------------------------------------------------------------
    Reconcile tree difference per rules given in script's docstring.
    A merge only: makes dirto same as dirfrom, without changing dirfrom.
    Because change sets are disjoint (the same item can appear in only
    one category) they cannot interfere with each other's operation or
    results (though order matters on case-insensitive machines: see ahead).
    Do dirto deletes first in case limited space on target device.

    ----
    Subtle thing: the order of steps here also matters for correctness.
    On case-insensitive machines like Windows, it's crucial to delete
    before adding, or else mixed-case renames won't work.

    Because folder contents are compared by name strings, renames result
    in a delete of the old name in TO, and an add in TO of the new name
    in FROM, regardless of the modtimes on either version.  This is as it
    must be to implement a rename; treating differing case versions as the
    same file name on Windows would avoid updating the file if its modtime
    matched, but would not rename it (as it should).

    However, it's crucial that we delete the old version in TO before
    adding the new (and similarly, delete the new before adding the old
    in "-restore" mode), or else a new add would be removed by a later
    old delete on Windows.  This is so, because a delete of any case will
    delete any other case.  If adds were first, deletes would negate them.

    Although the same is true for rewrites on Windows -- opening any case
    for output erases any other case -- this isn't an issue for replacements
    of same-named files for modtime differences, because this can only happen
    when case matches; case mismatches are always instead classified as unique
    items by the tree comparison, triggering a delete and add (in that order).
    By the same logic, mixed-mode updates are also safe on Windows, because
    this category can only arise if case matches during tree comparison,
    though this category also deletes before adding for space.

    Order is a non-issue on case-sensitive platforms like Linux, because
    mixed-case filenames yield distinct files: deletions and rewrites cannot
    impact a file whose name is differently-cased.
    ----
    
    [2.0] Backup mode: if dobackup, save files and dirs that will be
    destructively replaced or removed, to the TO archive's __bkp__ folder.
    Any exceptions during backups cause the change operation to be skipped.
    Dropped old ".bkp" prototype code; insufficient, must special-case;

    [2.1] Restore mode: backups also list added files in __bkp__/__added.txt__,
    and if dorestore, don't delete unique items in the TO tree, but do delete
    items listed in FROM's __added__.txt (first: order matters on Windows!).
    This allows complete rollback of a prior run by merging a __bkp__ subfolder
    to the archive root -- restoring all items replaced and removed, and removing
    all items added.  noteaddition() failures don't cancel copies here, as
    these are non-destructive updates.
    ------------------------------------------------------------------------------
    """
    
    # defs for brevity and uniformity
    join = os.path.join
    from backup import (      # also: handles recursive/circular import
        backupitem,           # save items to be replaced or deleted
        rmtreeworkaround,     # hack/fix for shutil.rmtree: see backup.py
        noteaddition,         # list files added for info and restores
        removeprioradds,      # if restoring, remove prior run's adds
        dropaddsfile,         # if restoring, delete merged-in adds file 
        indent1)              # same look-and-feel for related message here


    def askuser(prompt, query, filename):
        # ask console user (hook for future GUI?)
        print('\n' + prompt)
        domanual = input(query).lower() in ['yes', 'y', '1']
        if not domanual:
            print('no action taken for [%s]' % filename)
        return domanual
        
    def error(message, *args):
        # std message fmt + exception data? [[1.7.1] show message!]
        global anyErrorsReported
        anyErrorsReported = True   # [3.0] for summary line
        print('**Error', message, *args)
        trace(1, sys.exc_info()[0], sys.exc_info()[1])


    # [2.1] if restoring by merging backup to root, delete prior run's additions first;
    # order matters: must delete before add on Windows to back out mixed-case renames;
    if dorestore:
        totals = removeprioradds(fromroot, toroot)   # make counts match prior run
        countresolve.files.deleted, countresolve.folders.deleted = totals
        trace(1, indent1 + 'prior file/dir additions removed: %d/%d' % totals)


    # 1) For differing same-named files: Replace [after backup, if enabled]
    
    for (name, dirfrom, dirto, why) in diffs:
        pathfrom, pathto = join(dirfrom, name), join(dirto, name)
        if not doauto:
            prompt = '[%s] differs by %s in\n\tFROM dir [%s]\n\tTO dir   [%s]'
            prompt = prompt % (name, why, dirfrom, dirto)
            domanual = askuser(prompt, 'use FROM version?', name)

        if doauto or domanual:
            try:
                backupitem(pathto, toroot, dobackup, quiet)
                copyfile(pathfrom, pathto)   # content + modtime
            except:
                error('copying same file: skipped FROM', pathfrom)
            else:
                countresolve.files.replaced += 1
                trace(1, 'replaced same file, using FROM', pathfrom)


    # 2) For unique files and dirs in dirto: Delete [after backup?] (first: order matters!)
    
    for (uniqs, dirfrom, dirto) in uniques['to']:
        for name in uniqs:
            pathto = join(dirto, name)
            if dorestore:
                # [2.1] leave unchanged items as is
                trace(1, indent1 + 'retained unique item in TO tree: [%s]' % pathto)   
                continue
            
            if os.path.isfile(pathto):
                if not doauto:
                    prompt = '[%s] is unique file in\n\tTO dir [%s]' % (name, dirto)
                    domanual = askuser(prompt, 'delete from TO tree?', name)
                if doauto or domanual:
                    try:
                        backupitem(pathto, toroot, dobackup, quiet)
                        os.remove(pathto)
                    except:
                        error('removing TO file: skipped', pathto)
                    else:
                        countresolve.files.deleted += 1
                        trace(1, 'removed old TO file,', pathto)

            elif os.path.isdir(pathto):
                if not doauto:
                    prompt = '[%s] is unique dir in\n\tTO dir [%s]' % (name, dirto)
                    domanual = askuser(prompt, 'delete from TO tree?', name)
                if doauto or domanual:
                    try:
                        backupitem(pathto, toroot, dobackup, quiet)
                        shutil.rmtree(pathto, onerror=rmtreeworkaround)
                    except:
                        error('removing TO dir: skipped', pathto)
                    else:
                        countresolve.folders.deleted += 1
                        trace(1, 'removed old TO dir,', pathto)

            else: trace(1, 'ignored unknown type, TO:', pathto)


    # 3) For unique files and dirs in dirfrom: Copy [no backups required, but add note [2.1]]
    
    for (uniqs, dirfrom, dirto) in uniques['from']:
        for name in uniqs:
            pathfrom, pathto = join(dirfrom, name), join(dirto, name)            
            if os.path.isfile(pathfrom):
                if not doauto:
                    prompt = '[%s] is unique file in\n\tFROM dir [%s]' % (name, dirfrom)
                    domanual = askuser(prompt, 'copy to TO tree?', name)
                if doauto or domanual:
                    try:
                        noteaddition(pathto, toroot, dobackup)
                        copyfile(pathfrom, pathto)
                    except:
                        error('copying FROM file: skipped', pathfrom)
                    else:
                        countresolve.files.created += 1
                        trace(1, 'copied new FROM file,', pathfrom)

            elif os.path.isdir(pathfrom):
                if not doauto:
                    prompt = '[%s] is unique dir in\n\tFROM dir [%s]' % (name, dirfrom)
                    domanual = askuser(prompt, 'copy to TO tree?', name)
                if doauto or domanual:
                    try:
                        noteaddition(pathto, toroot, dobackup)
                        os.mkdir(pathto)
                        copytree(pathfrom, pathto, skipcruft=skipcruft)
                    except:
                        error('copying FROM dir: skipped', pathfrom)
                    else:
                        countresolve.folders.created += 1
                        trace(1, 'copied new FROM dir,', pathfrom)

            else: trace(1, 'ignored unknown type, FROM:', pathfrom)


    # 4) For same-named items that are both file and dir (rare): Delete+Copy [after backup?]

    for (name, dirfrom, dirto) in mixes:
        pathfrom, pathto = join(dirfrom, name), join(dirto, name)
        if os.path.isdir(pathfrom) and os.path.isfile(pathto):
            if not doauto:
                prompt = '[%s] is mixed dir/file in\n\tFROM dir [%s]\n\tTO dir   [%s]'
                prompt = prompt % (name, dirfrom, dirto)
                domanual = askuser(prompt, 'use FROM version dir?', name)
            if doauto or domanual:
                try:
                    backupitem(pathto, toroot, dobackup, quiet)
                    os.remove(pathto)
                    os.mkdir(pathto)
                    copytree(pathfrom, pathto, skipcruft=skipcruft)
                except:
                    error('replacing file with FROM dir: skipped', pathfrom)
                else:
                    countresolve.files.replaced += 1
                    trace(1, 'replaced file with dir, using FROM', pathfrom)

        elif os.path.isfile(pathfrom) and os.path.isdir(pathto):
            if not doauto:
                prompt = '[%s] is mixed file/dir in\n\tFROM dir [%s]\n\tTO dir   [%s]'
                prompt = prompt % (name, dirfrom, dirto)
                domanual = askuser(prompt, 'use FROM version file?', name)
            if doauto or domanual:
                try:
                    backupitem(pathto, toroot, dobackup, quiet)
                    shutil.rmtree(pathto, onerror=rmtreeworkaround)
                    copyfile(pathfrom, pathto)
                except:
                    error('replacing dir with FROM file: skipped', pathfrom)
                else:
                    countresolve.folders.replaced += 1
                    trace(1, 'replaced dir with file, using FROM', pathfrom)

        else: trace(1, 'ignored unknown types, FROM:', pathfrom, 'TO:', pathto)


    # [2.1] remove the __added__.txt file copied over by merge, if any;
    # this could be excluded during comparison, but quicker to special-case;
    if dorestore and dropaddsfile(toroot):
        countresolve.files.created -= 1    # make counts match prior run
        trace(1, indent1 + 'removed __added__.txt file from TO tree root')



################################################################################
# utilities
################################################################################


def getargs():
    """
    get command-line arguments, return False if any error
    [2.0] added new -backup switch here, and in both launchers;
    [2.0] do more error checking, catch and report bad paths;
    [2.1] added "-restore": merge __bkp__ to root, no deletes, trim adds;
    """
    
    def usageerror(message):
        print('**%s' % message)
        print('mergeall run cancelled.')
        print('Usage:\n'
                   '\t[py[thon]] mergeall.py dirfrom dirto\n'
                   '\t\t[-report] [-auto]\n'
                   '\t\t[-peek] [-verify]\n'
                   '\t\t[-backup] [-restore] [-quiet]\n'
                   '\t\t[-skipcruft]')
        
        if sys.stdin.isatty() and sys.stdout.isatty():
            if input('More?') in ['y', 'yes']:           # [2.0] for shell, not pipe
                help('mergeall')                         # never used by launchers

    class cmdargs: pass   # a set of attributes
    
    try:
        cmdargs.dirfrom = sys.argv[1]
        cmdargs.dirto   = sys.argv[2]
    except:
        usageerror('Missing dirfrom or dirto paths')
        return False
    else:
        if not os.path.exists(cmdargs.dirfrom):
            usageerror('Invalid dirfrom directory path')
            return False
        elif not os.path.exists(cmdargs.dirto):
            usageerror('Invalid dirto directory path')
            return False
        else:
            options = ['-report', '-peek', '-auto', '-verify',
                       '-backup', '-restore', '-quiet', '-skipcruft']
            for option in options:
                setattr(cmdargs, option[1:], False)               
            for option in sys.argv[3:]:
                if option in options:
                    setattr(cmdargs, option[1:], True)
                else:
                    usageerror('Bad command-line option: "%s"' % option)
                    return False
    return cmdargs  # this class is True



def reportdiffs(diffs, uniques, mixes, stream=sys.stdout):
    """
    report tree differences found to file/stream;
    [2.1] for consistency in logfiles, changed the order here to match that in
    which updates are run and summarized; order matters for renames on Windows
    (deletes must precede adds for mixed-case renames);
    """
    sepln = ('-' * 79) + '\n'
    print(sepln + 'SAMEFILE DIFFERENCES: (name, dirfrom, dirto, why)', file=stream)
    print('**These items will be replaced in dirto by automatic resolution**\n')  # [1.7]
    pprint.pprint(diffs, stream)

    print(sepln + 'UNIQUE ITEMS IN DIRTO: (names, dirfrom, dirto)', file=stream)
    print('**These items will be deleted from dirto by automatic resolution**\n')
    pprint.pprint(uniques['to'], stream)

    print(sepln + 'UNIQUE ITEMS IN DIRFROM: (names, dirfrom, dirto)', file=stream)
    print('**These items will be copied over to dirto by automatic resolution**\n')
    pprint.pprint(uniques['from'], stream)

    print(sepln + 'MIXED MODE NAMES: (name, dirfrom, dirto)', file=stream)
    print('**These items will be replaced in dirto by automatic resolution**\n')
    pprint.pprint(mixes, stream)



def summaryreport(diffs, uniques, mixes):
    """
    [2.0] show cmp/mod totals at end of run (only, else may be lost in text);
    also report len of difference lists, to summarize the difference report;
    counters are in global scope; diffs, uniques, mixes are too, but also passed;
    a dict comp works, but seems too complex: {key: sum(...) for key in uniques};
    [3.0] add errors-present indicator, to alert user to search for "**Error";
    this may not be 100% complete, but it's enough to handle most error cases;
    """
    global anyErrorsReported
    trace(1, '-' * 79, '\n*Summary')
    trace(1, 'Compared    =>', countcompare)
            
    numuniqueto    = sum(len(names) for (names, dirfrom, dirto) in uniques['to'])
    numuniquefrom  = sum(len(names) for (names, dirfrom, dirto) in uniques['from'])
    trace(1, 'Differences => '
             'samefile: %d, uniqueto: %d, uniquefrom: %d, mixedmode: %d' %
             (len(diffs), numuniqueto, numuniquefrom, len(mixes)))

    trace(1, 'Changed:\n' + str(countresolve))
    if anyErrorsReported or cpall.anyErrorsReported:   # [3.0]
        trace(1, '**There are error messages in the log file above: see "**Error"')
    trace(1, '-' * 79)
    trace(1, 'Finished.')    # add \n for GUI, else last line hidden after resizes [2.0]
                             # nevermind: new enable/disable "GO" model fixes this [3.0]


###############################################################################
# main logic
################################################################################


if __name__ == '__main__':
    import time
    gettime = (time.perf_counter if hasattr(time, 'perf_counter') else
              (time.clock if sys.platform.startswith('win') else time.time)) 
    
    cmdargs = getargs()
    if not cmdargs:
        sys.exit(1)


    # 1) collect differences phase
    trace(1, 'Starting.')
    trace(1, '-' * 79, '\n*Collecting tree differences')
    if cmdargs.skipcruft:
        trace(1, 'Skipping system cruft (metadata) files in both FROM and TO')

    diffs   = []                         
    uniques = {'from': [], 'to': []}     # lists/dict changed in-place by walker
    mixes   = []
    starttime = gettime()
    try:
        comparetrees(cmdargs.dirfrom, cmdargs.dirto,       # from/to roots
                     diffs, uniques, mixes,                # noted differences
                     cmdargs.peek,                         # file reads?
                     cmdargs.skipcruft,                    # exclude cruft files [3.0]
                     skip='__bkp__')                       # exclude top backups [2.0]

    except Exception as Why:
        # [3.0] friendlier message on comparison failure exits
        print('**Error during comparison phase\n'
              '...The mergeall run was terminated by a folder comparisons error,\n'
              '...to avoid a partial merge.  No data was changed.  Please resolve\n'
              '...the following Python exception before rerunning mergeall against\n'
              '...the same folders:')
        print(Why.__class__.__name__, Why)
        sys.exit(1)
    else:
        trace(1, 'Phase runtime:', gettime() - starttime)  # [2.2] time phases

    trace(1, '-' * 79, '\n*Reporting tree differences')
    reportdiffs(diffs, uniques, mixes)                     # handles own exceptions
    if cmdargs.report:
        # report and exit
        summaryreport(diffs, uniques, mixes)               # show totals [2.0]
        sys.exit(0)


    # 2) reconcile differences phase
    trace(1, '-' * 79, '\n*Resolving tree differences')
    if cmdargs.skipcruft:
        trace(1, 'Skipping system cruft (metadata) files in FROM folders')

    starttime = gettime()
    mergetrees(diffs, uniques, mixes,                      # noted differences
               cmdargs.auto,                               # make changes? else ask
               cmdargs.backup,  cmdargs.dirto,             # save items replaced/removed [2.0]
               cmdargs.restore, cmdargs.dirfrom,           # keep unique TO, undo adds [2.1]
               cmdargs.quiet,                              # suppress backing-up messages [2.4]
               cmdargs.skipcruft)                          # skip cruft files in copytree [3.0]
    trace(1, 'Phase runtime:', gettime() - starttime)      # [2.2] time phases
    
    if cmdargs.verify:
        # post verify step
        trace(1, '-' * 79 + '\n*Diffall run follows\n' + '-' * 79)
        starttime = gettime()
        cmd = os.popen('diffall.py %s %s' % (cmdargs.dirfrom, cmdargs.dirto))
        for line in cmd: print(line, end='')    # or save to a file?
        trace(1, 'Phase runtime:', gettime() - starttime)  # [2.2] time phases

    summaryreport(diffs, uniques, mixes)                   # show totals [2.0]
