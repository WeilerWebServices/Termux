"""
================================================================================
scandir_defunct.py:
   Python 3.5+ os.scandir() comparison-phase optimization, no longer used [3.0].

The comparison-phase variant code here, added in 2.2, formerly was some 2X
faster (or better) on Windows and Linux, but also 2X slower on Mac OS X.  This
meant that both variants were maintained and tested redundantly -- a major task.
  
Near the end of the 3.0 project, the non-scandir() variant was optimized to use
os.lstat() stat objects instead of os.path.*() calls, initially for new symlink
support.  This reduced the non-scandir() speed hit on Windows to 50%: runtimes
for a 60k-file archive were 10 seconds with scandir(), and 15 seconds without.

However, a final step of this recoding to avoid all extra stat calls made the
non-scandir() variant as fast as -- or slightly faster than -- this scandir()
variant on Windows too (at ~10 seconds).  This made the code here obsolete.
See ./docetc/miscnotes/3.0-mergeall-comparison-times-Windows.txt for timings.

On Mac OS X, this recoding to eliminate extra stats calls only improved the
non-scandir() performance.  For the same 60k-file archive, runtime fell from
9 seconds for the code here; to 4.5 seconds for the initial non-scandir()
variant; to just 3.8 seconds for the final non-scandir() variant.

See ./docetc/miscnotes/3.0-mergeall-comparison-times.txt for timing results.
These times are slightly better when mergeall is run directly outside the
GUI launcher (for reasons TBD: the launcher's UTF8 stdout encoding or -u?):

  # scandir() version on Mac
  $ py3 ../mergeall.py /MY-STUFF /MY-STUFF -skipcruft -report | grep 'Phase'
  Phase runtime: 8.64699007209856

  # non-scandir() version on Mac
  $ py3 ../mergeall.py /MY-STUFF /MY-STUFF -skipcruft -report | grep 'Phase'
  Phase runtime: 3.5263971380190924

Hence, this file's code will no longer be used, maintained, or tested, but
is retained here indefinitely for reference and historical context only,
and to recreate the relative speed results that led to its demise.

The final lesson here seems to be that os.scandir() can speed programs on
Windows and Linux (though not Mac OS X) which use many os.path.*() calls.
But it is no faster, and may even be slower, than code which uses explicit
os.stat()/lstat() calls and objects.  Given that both the scandir() and stat
schemes require similar changes or special coding, os.scandir() seems no
better, and worse on Mac.  Using stat objects yields code that is arguably
more cluttered visually than os.path.*(), but also a huge performance win.
================================================================================
"""

#
# this code is exec()d instead of imported to avoid recursion
#

# both should be False, except for testing
USETHISCODE = False   # <= change to 1/True to enable comparison variant here
FORCEONMAC  = False   # <= change to 1/True to use on Mac, despite slowness


################################################################################
# COMPARISON PHASE: analyze trees
# Python 3.5 and later version => use faster os.scandir() objects [2.2]
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
#
# UPDATE: these results were seen before the os.lstat() recoding above,
# after which the os.scandir() verison is still 2X *slower* on Macs -- 9~10
# secs vs 4~5 for an archive that grew to 65K files since the prior timings.
# Using python.org's Python 3.5 pm Mac OS X 10.11, only run-time differs:
#
#   /Admin-Mergeall/kingston-savagex256g/feb-2-17$ diff \
#           noopt1--mergeall-date170202-time091326.txt \
#           opt2--mergeall-date170202-time092217.txt 
#   0a1
#   > Using Python 3.5+ os.scandir() optimized variant.
#   4053c4054
#   < Phase runtime: 5.286043012980372
#   ---
#   > Phase runtime: 10.12333482701797
#
# With 3.0 code, the scandir() varient is still 50% to 2X *faster* on Windows.
#
# [3.0] FINAL UPDATE: this scandir() variant is no longer faster on Windows,
# making this code moot; see this file's main dosctring for the full verdict.
#
# Don't use float(sys.version[:3]) >= 3.5; scandir() can be a separate install.
#-------------------------------------------------------------------------------

if not hasattr(os, 'scandir'):          # older Pythons (2.7+): no os.scandir
    try:
        import scandir                  # check for PyPI package install
        os.scandir = scandir.scandir    # store in os, and assume same API
    except:
        pass                            # punt: use Py 3.4- (now all) verions


# [3.0] the non-scandir() version using os.lstat() is now faster everywhere
if (USETHISCODE
    and hasattr(os, 'scandir')                   # skip if not available
    and (not sys.platform.startswith('darwin')   # [3.0] not on Mac: slower!
         or FORCEONMAC)
    ):
    """
    ------------------------------------------------------------------------
    [2.2] Custom comparison code using os.scandir() instead of os.listdir().

    SEE NON-SCANDIR() VERSIONS in mergeall.py for docs not repeated here.

    os.scandir() provides an object API (versus name lists), that can often
    eliminate system calls for attributes such as type, modtime, and size.
    This can speed mergeall's comparison phase by a factor of 5 to 10 on
    Windows.  This speedup is entirely due to os.scandir(), not 3.5 in
    general, and can shave dozens of seconds off total runtimes for larger
    archives (and more on slower devices).

    POSIX systems also run quicker, according to this Python 3.5 change's PEP,
    benchmark, and documentation.  [UPDATE: Not so! => os.scandir() is faster
    on Linux too, but SLOWER on Macs - 2X~3X slower in mergeall; see above.]

    This speeds up the comparison phase only, but this phase always runs and
    can dominate runtimes in typical runs on large archives with light changes.
    The resolution phase was not changed, because it normally visits just a
    handful of file paths (changed items only), and is bound by basic file
    write/delete speed; system calls are minor component of its time.

    Note: diffall.py might benefit from os.scandir() too for path names,
    but it's less likely, as that script doesn't fetch modtimes or sizes,
    and is bound by the time required to fully read all common files.

    Note: scandir() is also available in a scandir module for older Pythons,
    including 2.7, via a PyPI package.  If installed, the code here imports
    and uses it, and so should work with older Pythons too -- not just 3.5+.

    CODING TBD: factor-out differing parts to avoid some redundant code?
    As is, there are two versions to update and test for comparison changes.
    In fact there were -- for 3.0 optimizations, cruft-file skipping, and
    symlinks support.
    But:
      They seem too different in structure to factor well, and factoring
      may slow either or both versions, negating this extension's goal.
    And:
      We need both, because the optimized variant is FASTER on Windows and
      Linux, but SLOWER on Mac.  This speed matters: a single version would
      penalize one or two platforms for the comparison phase, which always
      runs regardless of the number of changes in the trees.  Tentative
      lesson: redundancy is sometimes warranted in the name of optimization.

    [3.0] FINAL STORY: in the end, the non-scandir() grew slightly quicker
    on Windows too, by using stat objects to avoid all os.path.*() calls.
    This made the scandir() 3.5+ optimized variant fully obsolete, and
    removed the coding and testing redundancy.  Consequently, this scandir()
    variant has been moved out of file and kept here for reference only,
    and will no longer be updated or tested in the future.  Good riddance!
    ------------------------------------------------------------------------
    """
    if __name__ == '__main__':  # else prints twice
        trace(0, 'Using Python 3.5+ os.scandir() optimized variant.')

    # this decrufter flavor is used only here now
    from skipcruft import filterCruftDirentrys



    def comparedirs(direntsfrom, direntsto, dirfrom, dirto, uniques):
        """
        [2.2] python 3.5+ custom version using faster os.scandir().
        Doesn't use set difference here, to maintain listing order.
        Note: dirfrom and dirto pathnames still used by resolver phase.
        See mergeall.py's non-scandir() version for docs on this function.
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



    def comparelinks(direntfrom, direntto, dirfrom, dirto, diffs):
        """
        [3.0] python 3.5+ custom version using faster(?) os.scandir().
        See mergeall.py's non-scandir() version for docs on this function.
        """
        name = direntfrom.name 

        # compare link path strs
        linkpathfrom = os.readlink(direntfrom.path)
        linkpathto   = os.readlink(direntto.path) 
        if linkpathfrom != linkpathto:
            diffs.append((name, dirfrom, dirto, 'linkpaths'))



    def comparefiles(direntfrom, direntto, dirfrom, dirto, diffs, dopeek=False, peekmax=10):
        """
        [2.2] python 3.5+ custom version using faster(?) os.scandir().
        Uses stat() objects for sizes+times, perhaps avoiding system calls.
        Note: dirfrom and dirto pathnames still used by resolver phase.
        See mergeall.py's non-scandir() version for docs on this function.
        """
        trace(2, 'files:', direntfrom.path, direntto.path)
        
        def modtimematch(statfrom, statto, allowance=2):      # [1.3] 2 seconds for FAT32
            time1 = int(statfrom.st_mtime)                    # [2.2] os.stat_result object
            time2 = int(statto.st_mtime)
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
        [2.2] python 3.5+ custom version using faster(?) os.scandir().
        Doesn't use set intersection here, to maintain listing order.
        See mergeall.py's non-scandir() version for docs on this function.
        """
        trace(2, '-' * 20)
        trace(1, 'comparing [%s] [%s]' % (dirfrom, dirto))
        
        def excludeskips(direntsfrom, direntsto, skip):     # [3.0] pre-skipcruft filter 
            if not skip:
                return
            for dirents in (direntsfrom, direntsto):
                matches = [dirent for dirent in dirents if dirent.name == skip]
                if matches:
                    assert len(matches) == 1
                    trace(1, 'excluding', matches[0].path)
                    dirents.remove(matches[0])
            
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
            nonlink = dict(follow_symlinks=False)  # [3.0] narrow is() results
            
            # 0) compare linkpaths of links in common [3.0]
            if direntfrom.is_symlink() and direntto.is_symlink():
                comparelinks(direntfrom, direntto, dirfrom, dirto, diffs)

            # 1) compare contents of (non-link) files in common
            elif direntfrom.is_file(**nonlink) and direntto.is_file(**nonlink):
                comparefiles(direntfrom, direntto, dirfrom, dirto, diffs, dopeek)
                               
            # 2) compare (non-link) subdirectories in common via recursion
            elif direntfrom.is_dir(**nonlink) and direntto.is_dir(**nonlink):
                comparetrees(direntfrom.path, direntto.path,
                             diffs, uniques, mixes, dopeek, skipcruft)

            # 3) same name but not both links, files, or dirs (mixed, fifos)
            else:
                mixes.append((direntfrom.name, dirfrom, dirto))

