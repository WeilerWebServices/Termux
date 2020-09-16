#!/usr/bin/python
"""
Precoded test-files unzip.
Extracts don't care about cruft: unzip everything in the zip.
Or, run a ziptools/zip-extract.py command with os.system.
"""
import sys
from ziptools import ziptools
if sys.version[0] == '2':
    input = raw_input 

# this script's rmtrees sometimes fail on Windows after a fresh copy
from ziptools.ziptools import tryrmtree

if input("About to UNZIP: confirm with 'y'? ").lower() != 'y':
    print('Run cancelled')
else:
    for folder in ['test1', 'test2']:         # ensure fresh start
        tryrmtree(folder)
    ziptools.extractzipfile('test-1-2.zip', '.')

if sys.platform.startswith('win'):
    input('Press Enter to exit.')             # stay up if clicked
