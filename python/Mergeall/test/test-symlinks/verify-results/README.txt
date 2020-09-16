Verify that mergeall's comparison-phase variants with and without the 
3.5+ scandir() optimization produce the same results after 3.0 symlink 
support changes.   This also shows how the scandir() "optimized" version
runs more slowly on Mac OS X, the test host.

Diff results:

The diffs in results.txt here were run before deleting comparison-phase
and difference-report message sections (including comparison runtime).  
The only difference between the variants were the mode messages and 
timing results.  Hence, the two variants are identical in behavior.

Timing results:

The scandir() version is consistently 2X slower on Mac, even after 
3.0 optimizations are factored in.  To negate speedups due to caching,
all but one test were timed after an initial run to prime OS caches.
drive0, however, includes a non-scandir() initial-insert run's time 
as well: it is still quicker than the already-cached time for the 
scandir() variant.  The scandir() version once ran faster on Windows, 
but no more: per the next point.

Update - final:

The scandir() variant is no longer used on any platform, Windows and
Linux included, because a later os.lstat() recoding proved just as 
fast as scandir() on Windows and Linux, and slightly faster than before
on Mac.  Hence, the results here are of minor interest from a performance 
perspective, but are mostly an example of the testing overheads inherent
when maintaining multiple versions of code.  See scandir_defunct.py 
in the source-code folder for more details.
