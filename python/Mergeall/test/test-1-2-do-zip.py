#!/usr/bin/python
"""
Precoded test-files zip.
Don't skip any cruft here: it's deliberate in the test folders.
Or, run a ziptools/zip-create.py command with os.system.
"""
import sys
from ziptools import ziptools
if sys.version[0] == '2':
    input = raw_input

# os.remove('test-1-2.zip') not required: zipfile opens it in 'wb' mode
    
if input("About to ZIP: confirm with 'y'? ").lower() != 'y':
    print('Run cancelled')
else:
    # not used: cruftdflt = ziptools.cruft_skip_keep
    ziptools.createzipfile('test-1-2.zip', ['test1', 'test2'])

if sys.platform.startswith('win'):
    input('Press Enter to exit.')     # stay up if clicked
