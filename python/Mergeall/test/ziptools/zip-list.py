#!/usr/bin/python
"""
====================================================================
Ziptools utility.  List the contents of a zipfile, with:

  <python> zip-list.py [zipfile]

The sole optional argument zipfile is the file to list; it is input
interactively if omitted, and a ".zip" is appended if missing.

<python> is your platform's Python identifier string (e.g., "python3"
or "python" on Unix; "python", "py -3", "py", or omitted on Windows). 

Python's zipfile does most of the work here, but this adds argument
prompting when the command line is empty.  This could also use
zipfile's __main__ interface, by running an os.system command line
of the form: python -m zipfile -l somefile.zip.
====================================================================
"""
import zipfile, sys
if sys.version[0] == '2':
    input = raw_input 

# import os
# os.system('%s -m zipfile -l %s' % (sys.executable, sys.argv[1]))

if len(sys.argv) == 2:
    interactive = False
    thezip = sys.argv[1]
else:
    interactive = True
    thezip = input('Zipfile to list? ')
thezip += '' if thezip[-4:].lower() == '.zip' else '.zip'

# the zip bit
zipfile.ZipFile(thezip, 'r').printdir()

if interactive and sys.platform.startswith('win'):
    input('Press Enter to exit.')     # stay up if clicked
