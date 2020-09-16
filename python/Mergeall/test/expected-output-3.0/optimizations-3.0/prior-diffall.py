"""
################################################################################
Usage:
    [py[thon]] diffall.py dir1 dir2 [-recent [days=90]] [-skipcruft]
    
Recursive directory tree comparison: report unique files that exist in only
dir1 or dir2, report files of the same name in dir1 and dir2 with differing 
contents, report instances of same name but different type in dir1 and dir2,
and do the same for all subdirectories of the same names in and below dir1 
and dir2.  A summary of diffs appears at end of output, but search redirected
output for "*DIFFERS" and "*UNIQUE" strings for further details (per Sep-2016).

In sum, diffall compares full, byte-by-byte file content to verify that files
are truly the same.  It does not compare file modification times, as these
are not relevant to content equivalence.  See mergeall for a quicker but
shallower alternative that checks modification times but not full content
to detect file changes that warrant synchronization.

New: (3E) limit reads to 1M for large files, (3E) catch same name=file/dir,
(4E) avoid extra os.listdir() calls in dirdiff.comparedirs() by passing
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

New Sep-2016: changed difference labels slightly, so users can search the
report for uppercase '*UNIQUE' and '*DIFFERS' to jump to differences quickly.

New Sep-2016: use mergeall's extended OPEN() to support long file pathnames
on Windows.

New Sep-2016: the '-skipcruft' mode, also added to mergeall, skips system
cruft files in both folders so they do not register as differences (and
can clutter the report to the point of near unusability on some platforms
that rhyme with "Mac").  See mergeall_configs.py for more on cruft metadata.
################################################################################
"""

from __future__ import print_function     # ADDED: Py 2.X compatibility

import os, time, sys, dirdiff
from sys import argv
from fixlongpaths import OPEN             # [2.5] or 'as open', but too obscure 
from skipcruft import filterCruftNames    # [2.5] filter out metadata files

blocksize = 1024 * 1024                   # up to 1M per read
numdir = numfile = numskip = 0            # [2.0] a few sats

# [jan16] python/platform-specific current time (secs)
gettime = (time.perf_counter if hasattr(time, 'perf_counter') else
          (time.clock if sys.platform.startswith('win') else time.time)) 


def intersect(seq1, seq2):
    """
    Return all items in both seq1 and seq2;
    a set(seq1) & set(seq2) would work too, but sets are randomly 
    ordered, so any platform-dependent directory order would be lost
    """
    return [item for item in seq1 if item in seq2]


def recentlychanged(path1, path2, numdays=90):
    """
    [mergeall 2.0] return True if either path1 or path2 was modified
    in last "days" days (default 90, if not passed, or not listed in the
    command-line).  This is really days-worth-of-seconds, but close enough.
    In large achives, most files will not have been changed recently, so
    this test can speed limited comparisons.  Library calls used here:
    --------------------------------------------------------------------
    >>> t1 = os.path.getmtime('python')
    >>> t2 = time.time()
    >>> t1, t2
    (1390862766.9136598, 1426117651.752781)
    >>> time.ctime(t1), time.ctime(t2)
    ('Mon Jan 27 14:46:06 2014', 'Wed Mar 11 15:47:31 2015')
    --------------------------------------------------------------------
    """
    modtime1 = os.path.getmtime(path1)      # in seconds since epoch 
    modtime2 = os.path.getmtime(path2)      # float in 3.X, int in 2.X?
    nowtime  = time.time()
    secsback = numdays * (24 * 60 * 60)
    return (modtime1 > nowtime - secsback) or (modtime2 > nowtime - secsback)

    
def comparetrees(dir1, dir2, diffs,
                 recent=False, numdays=0,
                 skipcruft=False,
                 verbose=False):
    """
    Compare all subdirectories and files in two directory trees;
    uses binary files to prevent Unicode decoding and endline transforms,
    as trees might contain arbitrary binary files as well as arbitrary text;
    may need bytes listdir arg for undecodable filenames on some platforms;
    [2.0] compare only files changed in last "numdays" days if "recent";
    [2.5] ignore system metadata files in dir1 and dir2 if skipcruft is True;
    """
    global numdir, numfile, numskip   # [2.0]
    
    # compare file name lists
    numdir += 1
    print('-' * 20)
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    if skipcruft:
        # [2.5] ignore metadata files
        names1 = filterCruftNames(names1) 
        names2 = filterCruftNames(names2) 
        
    if not dirdiff.comparedirs(dir1, dir2, names1, names2):
        diffs.append('items UNIQUE at [%s] - [%s]' % (dir1, dir2))

    print('Comparing contents')
    common = intersect(names1, names2)
    missed = common[:]

    # compare contents of files in common
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            if recent and (not recentlychanged(path1, path2, numdays)):   # [2.0]
                numskip += 1                                              # [2.0]
                if verbose: print(name, 'skipped')
            else:
                numfile += 1
                file1 = OPEN(path1, 'rb')
                file2 = OPEN(path2, 'rb')
                while True:
                    bytes1 = file1.read(blocksize)
                    bytes2 = file2.read(blocksize)
                    if (not bytes1) and (not bytes2):
                        if verbose: print(name, 'matches')
                        break
                    if bytes1 != bytes2:
                        diffs.append('files DIFFER at [%s] - [%s]' % (path1, path2))
                        print('*DIFFERS:', name)
                        break
                file1.close()
                file2.close()  # [2.0]

    # recur to compare directories in common
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1, path2, diffs,
                         recent, numdays, skipcruft, verbose)

    # same name but not both files or dirs?
    for name in missed:
        diffs.append('items MISSED at [%s] - [%s]: [%s]' % (dir1, dir2, name))
        print('*MISSED:', name)


def getargs():
    "[2.0] Args for command-line mode"
    try:
        extramsg = None
        recent, numdays = False, 90         # defaults
        skipcruft = False
        
        dir1, dir2 = sys.argv[1:3]          # first 2 command-line args
        if not os.path.isdir(dir1):         # exists and is a dir [2.0] [2.5]
            extramsg = 'dir1 is invalid'
            assert False
        if not os.path.isdir(dir2):         # exists and is a dir [2.0] [2.5]
            extramsg = 'dir2 is invalid'    # was: assert os.path.isdir(dir2)
            assert False
        if '-skipcruft' in sys.argv:
            skipcruft = True                # [2.5] skip metadata files
            sys.argv.remove('-skipcruft')
        if len(argv) > 3:
            assert argv[3] == '-recent'     # [2.0] last N days only
            recent = True
            if len(argv) > 4: numdays = int(argv[4])   # listed else 90
    except:
        print('Usage: '
            '[py[thon]] diffall.py dir1 dir2 [-recent [days=90]] [-skipcruft]')
        if extramsg: print('Additional details:', extramsg)
        sys.exit(1)
    else:
        return (dir1, dir2, recent, numdays, skipcruft)


if __name__ == '__main__':
    dir1, dir2, recent, numdays, skipcruft = getargs()

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
