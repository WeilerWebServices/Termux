#!/usr/bin/env python3
"""
============================================================================
Simple custom recursive ls: shows stucture and links, skips Unix hiddens.
Run as "ls.py <folder>" where <folder> is the root of the tree to list:

   /somedir$ /Code/ls.py test1
   ...test1
   ......dirlink => dir
   ......file
   ......filelink => file
   ......nestedfilelink => dir/nestedfile
   ......test1/dir
   .........nestedfile
============================================================================
"""

from __future__ import print_function   # Py 3.X or 2.X
import os, sys
unixhiddens = ('.', '._')

level = 0
for (here, subs, files) in os.walk(sys.argv[1]):
    indent = len(here.split(os.sep))
    print('.' * (indent*3), here, sep='')

    for s in subs:
        if s.startswith(unixhiddens):
            continue
        sp = os.path.join(here, s)
        if os.path.islink(sp):
            print('.' * ((indent+1)*3), s, ' => ', os.readlink(sp), sep='')

    for f in files:
        if f.startswith(unixhiddens):
            continue
        fp = os.path.join(here, f)
        if os.path.islink(fp):
            print('.' * ((indent+1)*3), f, ' => ', os.readlink(fp), sep='')
        else:
            print('.' * ((indent+1)*3), f, sep='')
