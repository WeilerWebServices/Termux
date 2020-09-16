"""
==========================================================================================
backup.py:
  automatic backup/restore subsystem (part of the mergeall system [2.0])

Summary:

Make backup copies of all files and directories in the TO directory that will
be destructively replaced or deleted in-place during a mergeall run.  These 
items' prior versions in the TO tree are saved in the automatically-created 
__bkp__ folder at the top of the TO archive, with their full directory paths.
Backups are not synchronized across trees, but are automatically pruned by age 
when their number exceeds a limit.  This option makes mergeall generally safer,
as unwanted or failed changes can be later undone by restoring backup copies.

2.1 extends this model to support complete rollback of a prior run, by merging
a backup subfolder to an archive root.  It augments backups to also record files
added in a __bkp__\subfolder\__added__.txt file, and runs a special merge mode
which does not delete unique items in TO, but does delete all items in TO that
are listed in the backup's __added__.txt file (which is itself removed from TO
after the merge).  The net effect restores the TO tree's prior state, as long
as the restore run is made before any additional changes in TO.

Details:

Because a given item name may appear at multiple places in the archive tree,
replaced and deleted items are backed up in folders of this form (the mergeall
log gives a more linear list of changed items):

    TO-archive-root\__bkp__\date-time\full-archive-path-less-root\filename

Items in the __bkp__ folder are local to the TO archive copy, and save items changed in
that copy only.  Backup folders are not propagated to other archive copies by mergeall:
unlike normal archive items, they are not synchronized across trees.  Hence any changes
in __bkp__ folders are not themselves backed up.  Backup subfolders in __bkp__ are,
however, automatically pruned by age when their number exceeds a limit (changeable
in the code below).  This allows changes from any of multiple mergeall runs to be
selected for restores, if needed.

Any errors while writing a backup copy of an item causes the replacement or deletion
of that item to be skipped, as the operation is unsafe.  The item will register as
a difference on the next mergeall run, if not resolved manually.

Note that users can make arbitrary changes to their __bkp__ folders (including deleting
them altogether), as they are not synchronized and are created automatically whenever
needed.  For instance, if the default pruning limit results in too much space being
taken by __bkp__, you may delete portions of it freely.

Also note that __bkp__ folders may register differences in diffall.py runs.  As each
run has its own uniquely-named subfolders, these will usually be few, and can generally
be ignored.  Per-run folders' content differences may be useful, however, to compare and
analyze backup copies from different runs; run diffall on the subfolders themselves.

Purpose:

Though this option makes mergeall runs safer in general, it was primarily intended as an
automatic guard against propagating corrupted files across multiple archive copies, and
an better alternative to manual backup copies or multiple archive stores cycled by date
manually.  Merges generally works without issue if all but one archive copy are treated
as read-only; however, unwanted or incorrect changes may spread though archive copies
if changes are made in an archive copy and then synched back to the main copy.  In such
cases, the original's versions of files may be quickly lost, if not backed up.

By backing up items to be changed in each TO copy automatically and retaining multiple
runs' backups, bad copies can generally be undone easily by taking the most recent
backup's versions, without falling back to potentially much older full archive copies.
Backup folders also serve as a record of the most recent mergeall runs against a tree.

------------------------------------------------------------------------------------------

More about __bkp__ folders:

Stores __bkp__ folder at top of TO archive so it doesn't become disjoint from it, but
does not include __bkp__ in the mergeall synchronization -- its contents are local to
the TO archive, and not copied to/from other copies automatically.  This is so, because:

1) Propagating backups between copies in round-robin trips between three (or more)
devices seems potentially very confusing, and device source would be unclear.

2) Synchronizing would delete copes on TO not also on FROM, thereby limiting TO
from having more than one backup, in one-way propagation use cases.

3) Automatic backup pruning wouldn't be possible, as it violates the principle that
changes in the archive must all be disjoint during a single mergeall run.  If __bkp__
was included in the synchronization process, it's not impossible that one of its folders
on the TO archive would be both pruned by the backup system here and deleted due to an
absence in the FROM archive -- regardless of the timing, the second deletion attempt
would fail with an exception.

More about disjoint changes:

More generally, mergeall works at all only because its updates are mutually exclusive,
and disjoint (a given name can appear in just one change category).  Its changes are
limited to these items, in this order:

  a) Same-named files (replaced in TO)
  b) Unique files and directories in TO (deleted from TO)
  c) Unique files and directories in FROM (copied to TO)
  d) Same-named file/directory type mismatches between TO and FROM (replaced in TO)

Once any item is classified and changed in one of these categories, it is not
further inspected or altered.  Hence, each change in the TO tree is limited to
its TO tree location, and cannot be impacted by, or appear as part of, any other
changes category, regardless of the timing of changes made.  Order does matter for
renames on case-insensitive machines like Windows, but are sound as long as deletes
occur before adds (see mergeall.py's mergetrees() docstring for more details).

Backups rely on the fact that the change sets are disjoint: a file can be saved
for only one category (a, b, or d), and new copies (c) are never saved and thus
cannot overwrite saves for deletions, even for mixed-case differences on Windows.

Synchronizing the __bkp__ tree between archives would violate this disjointedness rule,
however, because automatic backup subfolder prunes may delete an item also scheduled for
deletion in category (b).  This is true even though all differences are detected before
the changes phase begins, and only removing __bkp__ items from the set of backed-up
items does not circumvent this; synchronization changes may still intersect with prunes.

Therefore, top-level __bkp__ folders are removed from the set of synchronized items
in the archives, and an archive copy retains only backups from mergeall runs where
it served the role of TO archive.  Backups can be manually copied into normal archive
folders to propagate them to other archive copies if desired, but their management
then becomes a user task; only items in the special-cased __bkp__ folders are
automatically pruned when their items count limit is exceeded.

------------------------------------------------------------------------------------------

General implementation notes:

Caveat: backup paths may be too long in some cases on some platforms.  The original file's
full archive path is recreated and required, because the same name may appear in more
than one place in the tree (and filenames created by concatenating path parts seem more
likely to exceed platform length limits).  

Does not store a single '.bkp' alongside original: would need to special-case to avoid
.bkp.bkp... accumulation, and a '.bkp' may be a valid to-be-archived user file name.

Uses copy instead of move (rename): need to retain original if code here fails, and also
want to retain the original's mod times in the copy.  os.rename also proved unreliable
on Windows, especially across devices.

All errors return with an exception: caller handles. In mergeall, the backup exception
here causes the removal or deletion to be skipped, as the operation is then unsafe.

Backs up files replaced or deleted, but does not backup new files added, as these
would be just redundant copies of new data.

Backup folder are excluded from the synchronization process by removing only top-level
__bkp__ items from os.listdir results in the comparisons procedure.  This proved more
reliable than os.rename moves to/from a temporary folder (see unused code ahead).

TBD: should backups be stored outside the archive itself?  Originally placed in __bkp__
at root of archive, and synchronized so that prior versions are not stored on just one
device only (which may fail).  The downside of this is that, when this option is used,
backups can accumulate quickly, and deletes are removed from the archive's actual folders
but linger on the device taking up space.  Could backup replaced files only, but that's
less secure.

     RESOLVED: later opted to store __bkp__ in the TO archive for association, but
     not synchronize it across other archive copies.  This was required, because
     prunes violated the disjoint updates rule which is the logical basis of mergeall.

TBD: should backups be pruned?  Currently, this is automatic, lest old backups
accumulate.  The downside of this is that the user may not want old backups removed.
As an alternative, the end user could be expected to manage backups, and could also be
expected to select the backups folder.  This would be flexible, but complicates the
command line and GUI with another directory choice, and deleting backup folders manually
seems a substantial extra admin task.

    RESOLVED: backups are stored in the automatically-created __bkp__ at the top of the
    TO archives, and are automatically pruned by age after N (default 10) copies have
    accumulated.  Given that __bkp__ is now local to each archive copy, this policy
    allows ample backup retention -- any of the last N runs can be unwound if needed.
    Users may also manually delete large backup folders before they are pruned for space.

TBD: __bkp__ folders will register differences in diffall.py runs for their top-level
per-run folders.  These can be simply ignored in reports.  diffall could skip __bkp__,
like mergeall, but this seems too tight a dependency between the two programs to enforce.

==========================================================================================
"""

from __future__ import print_function   # Py 2.X
import os, time, glob, shutil, sys, time, errno, stat  

import  mergeall    # for copyfile, copytree (from won't work here: recursive)
indent1 = '....'    # to distinguish messages here from main mergeall logic
indent2 = '____'    # rmdir retries: not just for pruning (also for uniqueto)


# [2.1] from configs file, unless absent or errors
try:
    from mergeall_configs import MAXBACKUPS 
except:
    MAXBACKUPS = 10   # keep up to this many backup folders in each archive copy's __bkp__

# [2.3] use UTF8 (or other) Unicode encoding for __added__.txt restore files in __bkp__,
# not platform default; these files contain filenames which may have arbitrary characters;
# 2.X's codecs.open files are always binary mode: must specialize line-ends here too;
ADDENC = 'utf-8'
if sys.version[0] == '3':
    unicode_open = open                         # what 3.X probably should have done?
    unicode_linesep = '\n'                      # 3.X text mode files expand \n as needed
else:
    import codecs
    unicode_open = codecs.open                  # 2.X compatibility (or use from...as...)
    unicode_linesep = os.linesep                # 2.X codecs always binary: no \n expansion

# make just 1 subfolder per run, on first file baked up;
# else may make 1 new subfolder for each second in run!
# now also used by noteadditions, to get run's subfolder:
# either backupitem or noteaddition may be called first;
datetimestamp = None

# try to prune just once per run, on first file backed up
pruned = False

# if -quiet, print backups message on first backup only [2.4]
firstbkpmsg = True



def makedirs_ifneeded(dirpath):
    """
    --------------------------------------------------------------------------------------
    [2.3] Run an os.makedirs() call portably on Python 3.X or 2.X to create any and all
    parts of a directory path as needed.  Only 3.X has the exists_ok flag to avoid an
    exception if a part already exists, and 2.X doesn't have 3.X's detailed exceptions.

    Note: Python's os.makedirs() in Lib\os.py is recursive, but probably doesn't need
    to be.  Because it scans a linear directory path, a simple loop should suffice, and
    yield simpler code (alas, "batteries included" means you get what's shipped in the
    box).  Recursion is really required only for arbitrary shapes, such as folder trees,
    and even then can be replaced with explicit stacks (see Learning Python 5E, p555-561).
    --------------------------------------------------------------------------------------
    """
    if sys.version[0] == '3':
        # python 3.X
        os.makedirs(dirpath, exist_ok=True)               # 'recursive' mkdir, as needed
    else:
        # python 2.X
        try:
            os.makedirs(dirpath)                          # 2.X has no exists_ok
        except OSError as E:                              # 2.X requires errno test
            import errno                                  # only need here on exc
            if E.errno != errno.EEXIST: raise             # reraise all others



def backupitem(pathto, toroot, dobackup, quiet):
    """
    ----------------------------------------------------------------------------------------
    If enabled by command-line (or by proxy via GUI toggle or console reply), make a backup
    copy of items (files and directories) in the TO tree before they are destructively
    replaced or deleted in-place.  This includes a:

    1) File in the TO tree that is about to be replaced by a newer same-named file in the FROM tree.
    2) File or directory in the TO tree that is about to be deleted due to absence in the FROM tree.
    3) File or directory in TO about to be replaced due to a dir/file type mismatch in the FROM tree.

    Unique files in FROM copied to TO are not backed up, as this is not a destructive action.
    pathto is where the item to be destroyed resides; toroot is the top of the archive in
    the TO tree, where the backup will be stored in a __bkp__ subfolder under pathto's tail.
    No longer needed, because __bkp__ not synched: "if pathto.startswith(bkproot): return".
    Either this or noteaddition may be called first: prune + timestamp if not yet done.

    [3.0] use newly-added 'strict' arg to copytree() to force it to propagate its first
    file exception to here, instead of printing an error message and continuing.  We need
    to pass the eception to this function's caller, so the item's update is cancelled if
    its backup fails.  Else, we might delete a TO folder without backing up parts of it!
    [3.0] don't use copytree()'s new 'skipcruft' here: backing up data already in TO tree.
    ----------------------------------------------------------------------------------------
    """
    global firstbkpmsg
    
    if not dobackup:
        return  # avoid nesting

    assert pathto.startswith(toroot)       # sanity check: changed file must be in TO tree
    todir, tofile = '?', '?'               # initialize for early exceptions
    
    try:    
        # prune old backups the first time through here (or noteaddition)
        try:
            prunebkpdirs(toroot)
        except:
            print(indent1 + 'prune failed, but backups and mergeall continued')
            print(indent1 + '%s %s' % (sys.exc_info()[0], sys.exc_info()[1]))

        # make run's subfolder timestamp first time here (or noteaddition)
        datetimestamp = makeruntimestamp()
        
        # verify or create the backup-to path in the TO copy
        bkproot = os.path.join(toroot, '__bkp__')                   # toroot is cmdargs.dirto
        todir, tofile = os.path.split(pathto)
        archtail = todir[(len(toroot) + len(os.sep)):]              # remove prefix=cmdargs.dirto
        bkppath = os.path.join(bkproot, datetimestamp, archtail)
        makedirs_ifneeded(bkppath)                                  # 'recursive' mkdir, as needed

        # copy file or dir over to backup copy 
        copytopath = os.path.join(bkppath, tofile)
        if not quiet:
            print(indent1 + 'backing up %s to %s' % (tofile, copytopath))
        elif firstbkpmsg:
            # [2.4] suppress per-file messages (superfluous?), but indicate backups mode once
            allbkpsroot = os.path.join(bkproot, datetimestamp)
            print(indent1 + 'backing up all items to %s' % allbkpsroot)    # [3.0] not bkppath!
            firstbkpmsg = False
        
        if os.path.isfile(pathto):
            mergeall.copyfile(pathto, copytopath)                 # this never catches excs
            
        elif os.path.isdir(pathto):
            os.mkdir(copytopath)
            mergeall.copytree(pathto, copytopath, strict=True)    # [3.0] fail on any except

        else:
            assert False, ('unknown file type: ' + pathto)             

    except:
        print(indent1 + '**Error backing up %s in %s' % (tofile, todir))
        raise   # reraise: handle in caller - cancel update, as it would be destructive



def makeruntimestamp():
    """
    ---------------------------------------------------------------------------------------
    Make the run's unique timestamp, to be used for its subfolder name in the TO tree's
    __bkp__ backups folder.  Factored to here, as this may be triggered by either backitem
    or noteaddition, either of which may be called first during a mergeall run.
    ---------------------------------------------------------------------------------------
    """
    global datetimestamp
    
    if not datetimestamp:
        datetimestamp = time.strftime('date%y%m%d-time%H%M%S')  # backup's unique top dir name
    return datetimestamp



def prunebkpdirs(toroot, maxbackups=MAXBACKUPS):
    """
    ---------------------------------------------------------------------------------------
    On first backup in session, auto-delete the oldest backup dir(s) in the TO archive
    if needed, keeping just the most recent N.  Most of this was adapted from the frigcal
    GUI's backup system.  TBD: this could be left to user, but seems likely to accumulate.
    Caller handles any exceptions here: this pre-merge step shouldn't be fatal - proceed.

    [3.0] Recoded to skip a failed directory and continue the prune to process other
    folders, instead of ending the prune at the first failure.  Else, this may miss
    folders in the unlikely event that a failure of a more recent backup folder (e.g.,
    permissions) prevents the prune from reaching earlier backups later on the list...
    which can only ever happen if the #backups has been reduced in the configs file.
    Users must address the failure to allow the failing folder to be pruned eventually.
    Callers are still notified with an exception, but details will be displayed here.
    ---------------------------------------------------------------------------------------
    """
    global pruned
    
    if pruned:
        return
    else:
        pruned = True
        bkproot = os.path.join(toroot, '__bkp__')
        if os.path.exists(bkproot):
            
            backuppatt  = 'date*-time*'
            currbackups = glob.glob(os.path.join(bkproot, backuppatt))
            currbackups.sort(reverse=True)
            prunes = currbackups[(maxbackups - 1):]              # earliest last, via names sort

            anyfailed = False
            for prunee in prunes:                                # globs have full paths
                print(indent1 + 'pruning', prunee)               # normally 0 or 1, unless failed
                try:
                    shutil.rmtree(prunee, onerror=rmtreeworkaround)
                except Exception:
                    anyfailed = True
                    print(indent1 + 'this prunee failed, but pruning continued')
                    print(indent1 + '%s %s' % (sys.exc_info()[0], sys.exc_info()[1]))                    

            assert not anyfailed, 'Some prunes had errors'       # [3.0] notify caller of excs



def noteaddition(pathto, toroot, dobackup):
    """
    --------------------------------------------------------------------------------------
    [2.1] Log unique FROM items (files and dirs) added to the TO tree in a text file,
    with 1 file path (relative to the TO tree's root) per line.  The logged items are
    stored in file: toroot\__bkp__\subfolder\__added__.txt.  This allows additions to be
    automatically removed by "-restore" as part of a later run to perform a complete
    rollback.  The adds file also serves as run documentation, in addition to logfiles.
    Either this or backupitem may be called first: prune + timestamp if not yet done.
    --------------------------------------------------------------------------------------
    """
    if not dobackup:
        return  # avoid nesting

    try:
        # prune old backups the first time through here (or backupitem)
        try:
            prunebkpdirs(toroot)
        except:
            print(indent1 + 'prune failed, but note-add and mergeall continued')
            print(indent1 + '%s %s' % (sys.exc_info()[0], sys.exc_info()[1]))

        # make run's subfolder timestamp first time here (or backupitem)
        datetimestamp = makeruntimestamp()

        # build and make the adds file's path 
        addsname = '__added__.txt'
        bkproot = os.path.join(toroot, '__bkp__')                    # toroot is cmdargs.dirto
        runroot = os.path.join(bkproot, datetimestamp)               # bkp subfolder for this run
        addspath = os.path.join(runroot, addsname)                   # adds file in run's subfolder
        makedirs_ifneeded(runroot)                                   # 'recursive' mkdir, as needed

        # write copied item's relative path to adds file
        # [2.3] use utf8 for filenames, not platform default
        archtail = pathto[(len(toroot) + len(os.sep)):]              # remove prefix=cmdargs.dirto
        addsfile = unicode_open(addspath, encoding=ADDENC, mode='a') # add to end of file
        try:                                                         # OLD: use default encoding in 3.X
            addsfile.write(archtail + unicode_linesep)               # 3.X expands \n, 2.X does not 
        finally:
            addsfile.close()

    except:
        # do NOT reraise: no need to cancel the update, as adds are non-destructive
        print('**Error noting add of %s' % pathto)
        
    else:
        # don't issue a trace mesage here, as it seems gratuitous in the logs (?)
        # print(indent1 + 'noted addition in TO of', archtail)
        pass



def removeprioradds(fromroot, toroot):
    """
    --------------------------------------------------------------------------------------
    [2.1] Remove items listed in fromroot's __added__.txt file from toroot tree, if
    __added__.txt and the listed files are present, as part of a complete rollback from
    backups.  This is a pre-merge step: order matters for renames on Windows (must delete
    and then add, else delete may remove different cased name).

    Assumes fromroot is a __bkp__ subfolder (or at least has an __added__.txt),
    but does not fail if not -- in all cases, ignore exceptions here.  The user may have
    deleted __added__.txt to back out removals+replacements only (not adds), and may have
    created a custom __added__.txt elsewhere in another tree to be merged.

    We need to care about closing the file on exceptions; this is now a pre-merge step.
    The __bkp__ folder's __added__.txt will be copied over to the TO root by the normal
    merge; it's deleted manually later, rather than skipping the name during the merge.

    CAVEAT: because noteaddition() records added items using the path syntax of the
    platform on which the prior mergeall ran, it's not possible to remove prior
    additions on a different platform having incompatible path syntax without editing
    either the additions file or the code here.  A file added on Windows, for example,
    will be noted with "\" in its path, which likely won't work in a restore on Linux.
    This could be addressed by always using "/" in additions file paths and running
    os.path.normpath() to convert to "\" on Windows only, but this seems a rare use case. 
    As is, restores with additions should be run on the same platform as the prior merge.
    --------------------------------------------------------------------------------------
    """
    addsname = '__added__.txt'
    addspath = os.path.join(fromroot, addsname)
    numfilesdel = numdirsdel = 0
    if os.path.exists(addspath) and os.path.isfile(addspath):
        # [2.3] use utf8, not platform default
        addsfile = unicode_open(addspath, encoding=ADDENC)  # propagate open() exceptions: cancel merge
        try:                                                # OLD: adds file uses default encoding in 3.X
            while True:                                     # decodes can fail - catch via while, not for
                try:
                    line = addsfile.readline()
                except:
                    print('**Error: restore cannot read added file name: file retained')
                    print(sys.exc_info()[0], sys.exc_info()[1])
                    continue
                else:
                    if not line: break  # eof

                delname = line.rstrip()
                delpath = os.path.join(toroot, delname)
                if os.path.isfile(delpath):
                    try:
                        os.remove(delpath)
                    except:
                        print('**Error: restore cannot delete file, retained:', delpath)
                        print(sys.exc_info()[0], sys.exc_info()[1])
                    else:
                        numfilesdel += 1
                        print(indent1 + 'restore removed file:', delpath)

                elif os.path.isdir(delpath):
                    try:
                        shutil.rmtree(delpath, onerror=rmtreeworkaround)
                    except:
                        print('**Error: restore cannot delete dir, retained:', delpath)
                        print(sys.exc_info()[0], sys.exc_info()[1])
                    else:
                        numdirsdel += 1
                        print(indent1 + 'restore removed dir:', delpath)

                else:
                    print('**Error: restore skipped missing or unknown type file:', delpath)
        except:
            print('**Error during prior adds removal')    # others? don't reraise: do merge
            print(sys.exc_info()[0], sys.exc_info()[1])
        finally:
            addsfile.close()                              # close, except or not (non-CPython)
    return (numfilesdel, numdirsdel)                      # sums: add to merge's delete counts



def dropaddsfile(toroot):
    """
    -------------------------------------------------------------------------------
    In "-restore" mode, as a post-merge step get rid of the __added__.txt that
    the normal merge may have copied over to TO's root.  This is a special
    case, but it's quicker to drop it forcibly from the root here than to check
    for it as a skipped filename at each tree level during the merge (though 
    the merge's code supports skipping __bkp__ at top, __added__.txt otherwise).
    -------------------------------------------------------------------------------
    """
    addsname = '__added__.txt'
    mergedaddspath = os.path.join(toroot, addsname)
    if os.path.exists(mergedaddspath):
        os.remove(mergedaddspath)
        return True
    else:
        return False   # don't adjust merge's counters or print message



def rmtreeworkaround(function, fullpath, exc_info):
    """
    ---------------------------------------------------------------------------------------
    Catch and try to recover from failures in Python's shutil.rmtree() folder
    removal tool, which calls this function automatically on all system errors.
    ---------------------------------------------------------------------------------------
    [2.0] PENDING DELETION FILURES:
    
    On Windows, deletes may be marked as pending, and not finalized atomically,
    leaving an item in place after the delete call returns.  This can cause
    rmtree (shutil or custom) operations to fail with a directory-not-empty
    error in rare cases, subject to devices and other activity on the machine.

    This seems a shortcoming (bug?) in shutil.rmtree for Windows, and may be
    improved in the future.  In fact, Python's own test system uses a custom
    rmtree with wait loops to avoid the issue.  Here, update failures are mostly
    harmless (leaving a difference to be resolved on the next run), and rare
    (seen on only 1 machine in 1 year's usage), but errors are better avoided.

    Short of low-level C API possibilities, the two solutions seem to be to move
    (os.rename) to a temp file and delete from there, or fall into a brief wait loop
    to watch for the file removal to be finalized.  The former is subject to some
    os.rename oddness (see ahead), and the latter is used in Python's own test system
    for rmtree calls.  Adopt the latter here -- this function is a callback on errors
    in shutil.rmtree(), which retries the rmdir in a wait but bounded loop.

    Note that this applies to, and is used by, _both_ backup folder removals here
    and general archive tree removals in mergeall.py for unique dirs in the TO
    tree; it's here because it was first observed during backup folder removals.
    The fix here copies Python's test system's wait timing technique of exponentially
    increasing delay times up to half a second.  Usually 0 or 1, but at most 10,
    retries are run, with delays from .001 to .512 seconds (to see how this is
    computed, run code [x = 0.001, while x < 1.0: print(x); x *= 2]).
    
    Caveats: Deletes that are only pending seem a curious property for a filesystem,
    and this fix feels hackish.  But this is harmless (it kicks in only on os.rmdir
    failures, adding a minor delay), and there's no budget for further research...
    Could watch for not empty (ENOTEMPTY) only, but other errors are not inconceivable.

    Related threads (though something more authoritative from Microsoft would be nice):
    http://stackoverflow.com/questions/3764072/c-win32-how-to-wait-for-a-pending-delete-to-complete
    http://bugs.python.org/issue19811

    Note: shutil.rmtree could also be replaced with the following (sans some Unix cruft):
        for (root, dirs, files) in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    but this doesn't fix the Windows pending-deletes issue, and may be less robust
    and portable than shutil's time-honed alternative.
    ---------------------------------------------------------------------------------------   
    [3.0] READ-ONLY PERMISSION FAILURES:
    
    As a different issue, rmtree operations can also fail due to read-only files in
    the tree.  To work around this, an onerror handler like the following can be used,
    which is portable to both Unix-en and Windows, and works like a Unix "rm -rf":

    import stat
    def onerror(func, path, exc_info):           # this is portable code 
        if not os.access(path, os.W_OK):         # read-only permission?
            os.chmod(path, stat.S_IWRITE)        # change to allow writes
            func(path)                           # and retry operation 
        else:
            raise

    This workaround was also incorporated into the general onerror handler below as
    a first step, before attempting the retry loop described above.  However, this
    code is currently DISABLED (via the False), because it makes no sense to override
    read-only permissions in this single context only (what about simple file deletes?),
    and the user may have marked an item read-only on purpose to protect it.  Instead,
    users are expected to fix their read-only permissions and run mergeall again.

    It can be argued that permission changes may be okay in this context, because
    users understand that mergeall intends to remove items, and read-only items will
    leave trash behind if not fixed.  Moreover, files on Windows are sometimes marked
    read-only without any user action (e.g., camera card copies), causing rmtree to
    fail unexpectedly.  This argument was rejected in the end, in favor of mergeall's
    overarching policy that your data is your property; read-only files should never
    be deleted without user intervention, even if this incurs extra manual steps.
    ---------------------------------------------------------------------------------------
    """

    # try to fix read-only errors first [3.0]
    if False:
        # PUNT: why in this context only?
        if (not os.access(fullpath, os.W_OK)
            and function in [os.rmdir, os.remove, os.unlink]):
            try:
                print(indent2 + 'fixing read-only on', fullpath)
                os.chmod(fullpath, stat.S_IWRITE)
                function(fullpath)
            except:
                pass    # fail: try other workaround below (or not? TBD)
            else:
                return  # okay: this fix worked, proceed with rmtree

    # then try this: Windows only, directory deletes only [2.0]
    if sys.platform.startswith('win') and function == os.rmdir:
        timeout = 0.001
        while timeout < 1.0:                     # 10 tries only, increasing delays
            print(indent2 + 'retrying rmdir')    # set off, but not just for pruning
            try:
                os.rmdir(fullpath)               # rerun the failed delete
            except os.error as exc:
                if exc.errno == errno.ENOENT:    # no such file (not empty=ENOTEMPTY) 
                    return                       # it's now gone: proceed with rmtree
                else:
                    time.sleep(timeout)          # wait for a fraction of second (.001=1 msec)
                    timeout *= 2                 # and try again, with longer delay
            else:
                return                           # it's now gone: proceed with rmtree

    raise  # all other cases, or wait loop end: reraise exception to kill rmtree caller




'''
==============================================================================================
THE FOLLOWING FUNCTIONS ARE NO LONGER USED (but retained as examples and lessons)

Instead of the following, restructured mergeall's recursive comparison algorithm to
skip '__bkp__' items in the top-level os.listdir result only.

Testing in Python 3.X showed os.rename to be unreliable.  On Windows, it fails when
the directories are on different devices (e.g., a USB stick and C:, possibly due to
differing file systems).  It also generated unexplainable permission errors on one
Windows test machine, even when the source and destination were on the same file
system.  As recursive copies and deletes are slow, recoded comparisons to skip
the folders in pure Python code instead.  The shutil.move call tries os.rename and
falls back on copy+delete too, but it's prone to the same issues seen here.
==============================================================================================

import tempfile, stat


def excludebkpdirs(toroot, fromroot):
    """
    ---------------------------------------------------------------------------------------
    Remove both archive's __bkp__ dirs from consideration, before diffs detection begins.
    To avoid complicating and slowing (or rewriting) change detection, simply move
    (rename) these out to a temp dir, and restore them after change detection finishes.
    They will not register changes, and so won't be propagated to any other archives.
    
    This and restorebkpdirs are coded fairly defensively, as this requires system calls;
    os.rename has been seen to fail for a true temp dir on Windows due to permissions
    (for no readily apparent reason...), so resort to program's cwd as a fallback option.
    
    On Windows, the destination of os.rename cannot exist, even for dirs; use new subdirs.
    mkdtemp adds random 6-character sequences to dir name till unique; add pid to be sure.
    Caveat: this may run up against directory path-length limits on some platforms?
    ---------------------------------------------------------------------------------------
    """
    global tempdir, temptobkp, tempfrombkp
    tempdir = temptobkp = tempfrombkp = None
    exists, join = os.path.exists, os.path.join
    try:
        tobkp   = join(toroot, '__bkp__')
        frombkp = join(fromroot, '__bkp__')
        if exists(tobkp) or exists(frombkp):          
            try:
                tempdir = tempfile.mkdtemp(prefix='mergeall-', suffix=str(os.getpid()))
                if sys.platform.startswith('win'):
                    os.chmod(tempdir, stat.S_IWRITE)   # may require force writeable?
                open('temp.txt', 'w').write('try rename\n')
                try:
                    os.rename('temp.txt', join(tempdir, 'temp.txt'))
                except:
                    os.remove('temp.txt')
                    raise  # reraise
                else:
                    os.remove(join(tempdir, 'temp.txt'))
            except:
                print('using cwd as temp dir fallback')         # show sys.exc_info()[0,1]?
                print(sys.exc_info()[0], sys.exc_info()[1])
                tempdir = os.getcwd()                           # temp unusable; or os.curdir

            if exists(tobkp):
                print('excluding', tobkp)
                temptobkp = join(tempdir, 'to.__bkp__')
                os.rename(tobkp, temptobkp)                     # quick move, not copy

            if exists(frombkp):
                print('excluding', frombkp)
                tempfrombkp = join(tempdir, 'from.__bkp__')
                os.rename(frombkp, tempfrombkp)                 # either can exist or not
    except:
        print('Cannot move __bkp__ to temp: rerun after manually moving out of archive')
        assert False, 'mergeall changes cancelled'



def restorebkpdirs(toroot, fromroot):
    """
    ---------------------------------------------------------------------------------------
    Restore __bkp__ folders from temp dir, after diffs detection, and before changes begin.
    See excludebkpdirs above for more details.
    ---------------------------------------------------------------------------------------
    """
    global tempdir, temptobkp, tempfrombkp
    join = os.path.join
    try:
        if temptobkp:
            tobkp = join(toroot, '__bkp__')
            print('restoring', tobkp)
            os.rename(temptobkp, tobkp)
            
        if tempfrombkp:
            frombkp = join(fromroot, '__bkp__')
            print('restoring', frombkp)
            os.rename(tempfrombkp, frombkp)
    except:
        print('Cannot restore __bkp__ from temp, changes cancelled: restore from %s' % tempdir)
        assert False, 'mergeall changes cancelled'
    else:
        if tempdir != None and tempdir != os.getcwd():    # not if fallback to cwd!
            os.rmdir(tempdir)
    
    
    
def isbkpdir(path, archroot):
    """
    ---------------------------------------------------------------------------------------
    Original idea: Call this from mergeall to skip a TO or FROM __bkp__ path during diffs
    detection phase.  Because these are skipped, they won't trigger any changes in the
    changes phase.  This is required to avoid including __bkp__ in synchronization (see top
    docstring).  Later replaced with os.rename moves, which was later replaced with
    comparison recoding.
    ---------------------------------------------------------------------------------------
    """
    bkproot = os.path.join(archroot, '__bkp__')
    return os.path.normpath(path).startswith(os.path.normpath(bkproot))  # equate / and \; case?

    # that is...
    #return path[(len(archroot) + len(os.sep)):] == '__bkp__'
'''

    
