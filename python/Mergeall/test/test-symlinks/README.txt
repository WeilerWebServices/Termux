Self-contained tests to verify and demonstrate 3.0's symlink support.
Run on Mac OS X 10.11 and Python 3.5 (Windows symlinks require admin).
These tests also exercise and illustrate FIFO file skipping cases,
and reflect the final 3.0 versions of mergeall and difall.

See ./mergeall-diffall-results.txt for primary test commands and outputs.

See ./verify-results for comparison-phase variant validations, and their Mac timings.

See also ../ziptools/moretests/test-symlinks for similar symlink support new in
the related ziptools package.