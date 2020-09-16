#!/usr/bin/python
"simple limited-scope source-code line count script"

# py 2.X compatibility
from __future__ import print_function
import sys
if sys.version_info[0] == 2: input = raw_input

import os, glob, sys
tally = count = 0

extras = glob.glob('ziptools' + os.sep + '*.py')  # now nested package here
for fname in glob.glob('*.py*') + extras:         # files in this dir 
    if not fname.startswith(('__sloc',)):         # skip self, keep __init__
        fobj = open(fname)
        lcnt = len(fobj.readlines())
        tally += lcnt
        count += 1
        print(fname, '=>', lcnt)
        
print('Total sloc in %d files: %s' % (count, tally))
if sys.platform.startswith('win'):
    input('Press Enter')  # if clicked


"""
================================================================================
example output (current counts/manifest):

__init__.py => 1
selftest.py => 95
zip-create.py => 213
zip-extract.py => 146
zip-list.py => 39
ziptools/__init__.py => 3
ziptools/zipcruft.py => 36
ziptools/ziplongpaths.py => 98
ziptools/zipsymlinks.py => 245
ziptools/ziptools.py => 724
Total sloc in 10 files: 1600
================================================================================
"""
