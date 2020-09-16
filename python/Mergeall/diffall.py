#!/usr/bin/env python3
# Python 3.X and 2.X are both supported
# Python 3.X is recommended for trees with Unicode filenames
"""
################################################################################
Usage:
    [py[thon]] diffall.py dir1 dir2 [-recent [days=90]] [-skipcruft] [-u]
    
Recursive directory tree comparison: report unique files that exist in only
dir1 or dir2, report files (and symlinks) of the same name in dir1 and dir2
with differing contents, report instances of same name but different type in
dir1 and dir2, and do the same for all subdirectories of the same names in
and below dir1 and dir2.  

The net effect performs both a structural comparison of the dir1 and dir2 trees, 
and a byte-for-byte comparison of all their common files.  "-recent" limits
comparisons to files changed in the last N days; "-skipcruft" ignores system
hidden and metadata files; and "-u" unbuffers output for frozen apps/exes.
See the change log below for more on command-line arguments supported.

A summary of diffs appears at end of this script's output.  Redirect its output
to a file using ">" and search for "*DIFFER", "*UNIQUE", and "*MISSED" strings 
for further difference details following a run (per Sep-2016's update below).

In sum, diffall compares full, byte-by-byte file content to verify that files
are truly the same.  It does not compare file modification times, as these
are not relevant to content equivalence.  See mergeall for a quicker but
shallower alternative that checks modification times but not full content
to detect file changes that warrant synchronization.

--------------------------------------------------------------------------------
CHANGE LOG

New PP3E: limit reads to 1M for large files, catch same name=file/dir mixed
type cases.

New PP4E: avoid extra os.listdir() calls in dirdiff.comparedirs() by passing
results here along.

New March-2015, for mergeall 2.0: add "-recent [days]" limited comparisons
option to compare just files changed in last days (else compares all files),
plus simple stats at end of report.  Also for 2.0, added explicit file.close
calls, for use outside CPython; we don't care about catching exceptions here,
as any kill the script, and we're just reading in any event.

New Jan-2016: change incorrect "dirdiff" in usage message to "diffall".
Also print total diffall runtime for speed analysis and drive comparisons.
Caveat: may run quicker with os.scandir() instead of os.listdir() in Python
3.5+ (only!), but runtime is likely dominated by the exhaustive file reads
here, not listings; see mergeall.py for os.scandir() alternative in action.

New Sep-2016..Mar-2017 [3.0]:

0) Compare, but do not follow symbolic links (symlinks).  Otherwise, may
compare arbitarily-large items referenced by intra-archive links > once.
Coded as a pretest to avoid changing existing code, treats links to both
files and dirs the same, and compares their reference-path strings.

1) Changed difference labels slightly, so users can search the report for
uppercase '*UNIQUE' and '*DIFFER' (and the rare '*MISSED') to jump to
differences quickly.

2) Use mergeall's extended OPEN() to support long file pathnames on Windows.
UPDATE: the fixlongpaths module is now used in multiple places to support
long windows paths here, not just for open(); see FWP().

3) The new '-skipcruft' mode, also added to mergeall, skips system cruft files
in both folders so they do not register as differences (and clutter the report
to the point of near unusability on some platforms that rhyme with "Mac"!).
See mergeall_configs.py for more on cruft metadata; the implementation of
cruft skipping is shared with mergeall and cpall.

4) Recoded the diffall algorithm so that rare mixed-type differences are
detected _before_ recurring into any subdirs.  This way, any "*MISSED" log
messages appear in the subject folder's section - not arbitrarily far ahead
after all subfolders' sections.  As it was, these showed up in the last
subfolder's section of the report, and listed their dirs only in the summary.

Note that the diffall algorithm must still use multiple loops over items, in
order to report file comparisons (and now mixed-type cases) _before_ starting
a new report section for subdirectories' content.  This structure differs
from mergeall's single-loop data builder scheme, but is deliberate.

5) The algorithm was also optimized slightly, to avoid running os.path.join()
on an item more than once (though the gain is likely negligible versus file IO,
and the speed tradeoff for the added list operations was not determined).

6) Further optimized later to replace os.path.join(x, y) with x + os.sep + y;
join() seems complex and slow overkill in simple and known path+file cases,
especially on Windows (see Python's Lib\ntpath.py).

OPTIMIZATION RESULTS:

The prior 2 point's optimizations had NO significant effect on diffall
runtimes.  See file:
    test/expected-output-3.0/optimizations-3.0/diffall-results.txt
for typical speed test results.  In sum, a diffall for an 87G SSD folder with
59K files and 3.5K folders runs in roughly 4 minutes 20 seconds - in BOTH the
prior and new diffall code.  The optimized version here may shave very low
single-digit seconds in some runs, but this is trivial in a 4 minute task.
Caveat: timing tests were run on Windows; other platforms may or may not agree.

Further optimizations based on different codings or the os.scandir()
alternative to os.listdir() in Python 3.5+ used by mergeall are also likely
to be pointless (and os.scandir() may run _slower_ on Mac OS X).  As expected,
the vast majority of this script's time is spent reading files in full, not in
analysis of structure.  As another metric, the mergeall comparison phase for
this same test folder runs in just 7.2 seconds - versus 4 minutes for a
byte-for-byte diffall.  The latter is clearly too IO-bound to speed further
in code, which is why mergeall was developed in the first place!

Given these results, the cpall script was not optimized; its runtimes are
even _more_ IO-bound by the need to write files (and probably reach hours on
slow drives).  Faster devices seem a better bet for speeding such programs.

7) Support symlinks by comparing their linkpaths, not the items they refer to.
We care only if the links differ here, not that their referents are valid.

New Dec-2017 [3.1]: If a "-u" command-line arg is passed to this script or its 
frozen app/executables (not to Python), flush output lines as they are written. 
This makes prints unbuffered, useful when monitoring output with a Unix "tail".
################################################################################
"""

from __future__ import print_function     # added: Py 2.X compatibility

# [3.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

import os, time, sys, dirdiff
from sys import argv

# [3.0] filter out metadata files
from skipcruft import filterCruftNames 

# [3.0] fix too-long paths on Windows 
from fixlongpaths import FWP

# [3.1] autofush print lines if "-u"
from autoflush import setFlushedOuput

blocksize = 1024 * 1024                   # up to 1M per read
numdir = numfile = numskip = 0            # [2.0] a few stats

# [jan16] python/platform-specific current time (secs)
gettime = (time.perf_counter if hasattr(time, 'perf_counter') else
          (time.clock if sys.platform.startswith('win') else time.time)) 



def intersect(seq1, seq2):
    """
    ---------------------------------------------------------------------------
    Return all items in both seq1 and seq2;
    a set(seq1) & set(seq2) would work too, but sets are randomly 
    ordered, so any platform-dependent directory order would be lost
    ---------------------------------------------------------------------------
    """
    return [item for item in seq1 if item in seq2]



def recentlychanged(path1, path2, numdays=90):
    """
    ---------------------------------------------------------------------------
    [mergeall 2.0] return True if either path1 or path2 was modified
    in last "days" days (default 90, if not passed, or not listed in the
    command-line).  This is really days-worth-of-seconds, but close enough.
    In large achives, most files will not have been changed recently, so
    this test can speed limited comparisons.  Library calls used here:
    ---------------------------------------------------------------------------
    >>> t1 = os.path.getmtime('python')
    >>> t2 = time.time()
    >>> t1, t2
    (1390862766.9136598, 1426117651.752781)
    >>> time.ctime(t1), time.ctime(t2)
    ('Mon Jan 27 14:46:06 2014', 'Wed Mar 11 15:47:31 2015')
    ---------------------------------------------------------------------------
    """
    modtime1 = os.path.getmtime(FWP(path1))      # in seconds since epoch 
    modtime2 = os.path.getmtime(FWP(path2))      # float in 3.X, int in 2.X?
    nowtime  = time.time()
    secsback = numdays * (24 * 60 * 60)
    return (modtime1 > nowtime - secsback) or (modtime2 > nowtime - secsback)


    
def comparetrees(dir1, dir2, diffs,
                 recent=False, numdays=0,
                 skipcruft=False,
                 verbose=False):
    """
    ---------------------------------------------------------------------------
    Compare all subdirectories and files in two directory trees;
    uses binary files to prevent Unicode decoding and endline transforms,
    as trees might contain arbitrary binary files as well as arbitrary text;
    may need bytes listdir arg for undecodable filenames on some platforms;
    
    [2.0] compare only files changed in last "numdays" days if "recent";
    [3.0] use OPEN to support long file pathnames on Windows (now defunct);
    [3.0] ignore system metadata files in dir1 and dir2 if skipcruft is True;
    [3.0] detect and report mixed-type diffs before processing any subdirs; 
    [3.0] optimized to avoid calling os.path.join() more than once per item;
    [3.0] optimized to use +os.sep+ instead of likely slower os.path.join();
    [3.0] handle symlinks explicitly by comparing their link paths directly;
    [3.0] fix long paths on Windows (only) with FWP(), but don't mod msgs;
    ---------------------------------------------------------------------------
    """
    global numdir, numfile, numskip   # [2.0]
    
    # compare file name lists (new report section)
    numdir += 1
    print('-' * 20)
    names1 = os.listdir(FWP(dir1))
    names2 = os.listdir(FWP(dir2))
    if skipcruft:
        # [3.0] ignore metadata files
        names1 = filterCruftNames(names1) 
        names2 = filterCruftNames(names2) 

    # detect and report unique items
    if not dirdiff.comparedirs(dir1, dir2, names1, names2):
        diffs.append('items UNIQUE at [%s] - [%s]' % (dir1, dir2))

    # get names common to both dirs
    print('Comparing contents')
    common = intersect(names1, names2)

    #----------------------------------------------------------------------
    # compare contents of files (and links) in common
    # report before any subdirs, and try this most-common case first
    #----------------------------------------------------------------------
    
    notfiles = []
    for name in common:
        path1 = dir1 + os.sep + name    # [3.0] avoid os.path.join
        path2 = dir2 + os.sep + name

        if os.path.islink(FWP(path1)) or os.path.islink(FWP(path2)):
            # [3.0] handle symlinks to files and dirs specially here
            if os.path.islink(FWP(path1)) and os.path.islink(FWP(path2)):
                # both are links: read
                numfile += 1
                link1 = os.readlink(FWP(path1))   # str path name
                link2 = os.readlink(FWP(path2))
                if link1 == link2:
                    if verbose: print(name, 'matches')
                else:
                    diffs.append('links DIFFER at [%s] - [%s]' % (path1, path2))
                    print('*DIFFER:', name)
            else:
                # only one link: mixed
                diffs.append('items MISSED at [%s] - [%s]: [%s]' % (dir1, dir2, name))
                print('*MISSED:', name)
        
        elif os.path.isfile(FWP(path1)) and os.path.isfile(FWP(path2)):
            # file+file: skip full reads if not recently changed 
            if recent and (not recentlychanged(path1, path2, numdays)):  # [2.0]
                numskip += 1                                             # [2.0]
                if verbose: print(name, 'skipped')
            else:
                numfile += 1
                file1 = open(FWP(path1), 'rb')  # [3.0]: long paths
                file2 = open(FWP(path2), 'rb')
                while True:
                    bytes1 = file1.read(blocksize)
                    bytes2 = file2.read(blocksize)
                    if (not bytes1) and (not bytes2):
                        if verbose: print(name, 'matches')
                        break
                    if bytes1 != bytes2:
                        diffs.append('files DIFFER at [%s] - [%s]' % (path1, path2))
                        print('*DIFFER:', name)
                        break
                file1.close()
                file2.close()  # [2.0]

        else:
            # pass others to next phase (non-link dirs, mixes, fifos)
            notfiles.append((name, path1, path2))

    #----------------------------------------------------------------------
    # detect same name but not both files or dirs (rare)
    # [3.0] report before subdirs, and use cached paths for speed
    #----------------------------------------------------------------------
    
    notmixed = []
    for (name, path1, path2) in notfiles:
        if not (os.path.isdir(FWP(path1)) and os.path.isdir(FWP(path2))):
            diffs.append('items MISSED at [%s] - [%s]: [%s]' % (dir1, dir2, name))
            print('*MISSED:', name)
        else:
            notmixed.append((path1, path2))

    #----------------------------------------------------------------------
    # recur to compare non-link directories in common (the rest)
    # each subdir starts a new report section for its own content
    #----------------------------------------------------------------------
    
    for (path1, path2) in notmixed:
        comparetrees(path1, path2, diffs,
                     recent, numdays, skipcruft, verbose)



def getargs():
    """
    ---------------------------------------------------------------------------
    [2.0] Args for command-line mode
    ---------------------------------------------------------------------------
    """
    try:
        extramsg = None
        recent, numdays = False, 90         # defaults
        skipcruft = False
        unbuffered = False
        
        dir1, dir2 = sys.argv[1:3]          # first 2 command-line args
        if not os.path.isdir(dir1):         # exists and is a dir [2.0] [3.0]
            extramsg = 'dir1 is invalid'
            assert False
        if not os.path.isdir(dir2):         # exists and is a dir [2.0] [3.0]
            extramsg = 'dir2 is invalid'    # was: assert os.path.isdir(dir2)
            assert False

        if '-skipcruft' in sys.argv:
            skipcruft = True                # [3.0] skip metadata files (any order)
            sys.argv.remove('-skipcruft')
        if '-u' in sys.argv:
            unbuffered = True               # [3.1] make output unbuffered in apps
            sys.argv.remove('-u')

        if len(argv) > 3:
            assert argv[3] == '-recent'     # [2.0] last N days only
            recent = True
            if len(argv) > 4: numdays = int(argv[4])   # listed else 90
    except:
        print('Usage: '
            '[py[thon]] diffall.py dir1 dir2 [-recent [days=90]] [-skipcruft] [-u]')
        if extramsg: print('Additional details:', extramsg)
        sys.exit(1)
    else:
        return (dir1, dir2, recent, numdays, skipcruft, unbuffered)



if __name__ == '__main__':
    """
    ---------------------------------------------------------------------------
    stand-alone/command-line mode;
    diffall isn't very useful otherwise, as it prints instead of returning,
    but its output might be parsed;  see also mergeall's variation on the
    comparisons run here, that builds explicit results data-structures;
    ---------------------------------------------------------------------------
    """
    dir1, dir2, recent, numdays, skipcruft, unbuffered = getargs()

    # [3.1] force unbuffered output (for apps/exes)?
    if unbuffered:
        setFlushedOuput()

    # walk, compare, change diffs in-place
    diffs = []
    starttime = gettime()                                  
    comparetrees(dir1, dir2, diffs, recent, numdays, skipcruft, True) 
    tottime = gettime() - starttime 

    # report time [jan6], stats [2.0]
    hours   = tottime // (60*60); tottime -= hours * (60*60)
    minutes = tottime //  60;     tottime -= minutes * 60
    print('=' * 80)
    print('Runtime hrs:mins:secs = %.0f:%.0f:%.2f'
                      % (hours, minutes, tottime))          
    print('Dirs checked %d, Files checked: %d, Files skipped: %d'
                      % (numdir, numfile, numskip))
    if skipcruft: print('System metadata (cruft) files were skipped')

    # report collected diffs list
    if not diffs:
        print('No diffs found.')
    else:
        print('Diffs found:', len(diffs))
        for diff in diffs: print('-', diff)
    print('End of report.')
