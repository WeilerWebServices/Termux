#!/usr/bin/python
r"""
================================================================================
fixeoln-all.py (Python 3.X or 2.X)

Convert all text files in a directory tree to Unix or DOS end-of-line format.
Files are changed in place, if any of their end-lines must be converted. 
See also "fixeoln.py" for code applied by this script to each file in the tree.

Copyright: 2017 by M. Lutz (learning-python.com).
Latest update: June 2017 - skip symlinks and fifos, add iffext.
License: provided freely, but with no warranties of any kind.

Usage:    
        [python] fixeoln-all.py (tounix|todos) rootdir encoding?

Examples: 
        python fixeoln-all.py tounix /Stuff/websites              # Unix
        python3 docetc/fixeoln-all.py todos . utf8                # Unix
        py -3 docetc\fixeoln-all.py tounix ..\uploaddir latin1    # Windows

See also: 
        global-variable switches for report-only mode, messages, prunes

Converts end-line character sequences in all text files in the folder tree
whose pathname is provided, to the target end-line format ("tounix" or "todos"),
changing all the subject files in-place.  In all text files, lines are changed
as needed to end with "\n" for "tounix" and "\r\n" for todos.

Uses the provided Unicode encoding for all files in the tree.  Its default is
utf8, though latin1 may work better for some trees: run in debug=True mode
first to see which files might fail to decode, or run again with another
encoding after failures to pick up files skipped on errors (you can also run
"fixeoln.py" on individual failed files).  Detects text files with Python's
mimetypes module, instead of hardcoded extensions - see the next section.

--------------------------------------------------------------------------------
PRIMER - this script also uses Python's mimetypes to identify text files:

>>> from mimetypes import guess_type, add_type
 
>>> guess_type('spam.txt'), guess_type('spam.py'), guess_type('spam.pyw')
(('text/plain', None), ('text/plain', None), ('text/plain', None))

>>> guess_type('spam.html'), guess_type('spam.css'), guess_type('spam.xml')
(('text/html', None), ('text/css', None), ('text/xml', None))

>>> guess_type('spam.TXT'), guess_type('spam.Py'), guess_type('spam.HTM')
(('text/plain', None), ('text/plain', None), ('text/html', None))

>>> guess_type('C:\\somedir\\spam.txt'), guess_type('/Users/you/spam.html')
(('text/plain', None), ('text/html', None))
 
>>> guess_type('spam.png'), guess_type('spam.xls'), guess_type('spam.xxx')
(('image/png', None), ('application/vnd.ms-excel', None), (None, None))
 
>>> guess_type('spam.zip'), guess_type('spam.tgz')
(('application/x-zip-compressed', None), ('application/x-tar', 'gzip'))

>>> add_type('text/x-python', '.pyw')
>>> guess_type('spam.py'), guess_type('spam.pyw')
(('text/plain', None), ('text/x-python', None))

--------------------------------------------------------------------------------
EXAMPLE (with function args tracelevel=0, debug=True):

c:\...\pymailgui\Release\docetc> fixeoln-all.py tounix ..\..\..\mergeall latin1
Using mode=tounix, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:   606
        Unchanged:   285
        Failures:      0
        Empties:     215

c:\...\pymailgui\Release\docetc> fixeoln-all.py todos ..\..\..\mergeall latin1
Using mode=todos, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:    88
        Unchanged:   803
        Failures:      0
        Empties:     215

These two runs show that 18 files in the rootdir have mixed DOS/Unix endlines,
or contain no end-line characters at all:
    tounix: 285 already-unix or empty - 215 empty = 70  already-unix only 
    todos:  803 already-dos  or empty - 215 empty = 588 already-dos only
    88  todos converted  - 70 unix only => 18 mixed or no-end-line
    606 tounix converted - 588 dos only => 18 mixed or no-end-line

--------------------------------------------------------------------------------
EXAMPLE (with function args tracelevel=0, debug=False):

The following runs further reveal two files with no end-line characters at all:

c:\...\pymailgui\Release\docetc> fixeoln-all.py tounix ..\..\..\mergeall latin1
Using mode=tounix, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:   674
        Unchanged:   217
        Failures:      0
        Empties:     215

c:\...\pymailgui\Release\docetc> fixeoln-all.py tounix ..\..\..\mergeall latin1
Using mode=tounix, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:     0
        Unchanged:   891
        Failures:      0
        Empties:     215

c:\...\pymailgui\Release\docetc> fixeoln-all.py todos ..\..\..\mergeall latin1
Using mode=todos, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:   674
        Unchanged:   217
        Failures:      0
        Empties:     215

c:\...\pymailgui\Release\docetc> fixeoln-all.py todos ..\..\..\mergeall latin1
Using mode=todos, rootdir=..\..\..\mergeall, encoding=latin1

--SUMMARY--
Visited 891 files:
        Converted:     0
        Unchanged:   891
        Failures:      0
        Empties:     215

And here they are (files with missing end-lines)...

>>> import os
>>> for (dir, subs, files) in os.walk(r'..\..\..\mergeall'):
...     for file in files:
...         if file.endswith(('.txt', '.py', '.html')):
...             text = open(os.path.join(dir, file), 'r', encoding='latin1').read()
...             if len(text) > 0 and '\n' not in text: print(dir, file)
...
..\..\..\mergeall\_older-examples-webonly\issues README.txt
..\..\..\mergeall\_private_ announce-2.2.txt
>>>
>>> open(r'..\..\..\mergeall\_older-examples-webonly\issues\README.txt', 'rb').read()
b"Demos of some outstanding issues described in mergeall's docs."
>>> open(r'..\..\..\mergeall\_private_\announce-2.2.txt', 'rb').read()
b'moved to top-level Docs folder'
================================================================================
"""

from __future__ import print_function          # Python 2.X compatibility
import mimetypes, os, sys, fixeoln             # fixeoln lives in same dir

# switches (beyond those on cmd line)
Debug  = False                                 # print results only? 
Trace  = 0                                     # show filenames?
Iffext = None                                  # visit files with this ext only?

# pyw not in module's table, though may be in other sources
mimetypes.add_type('text/x-python', '.pyw')


def isMimeMainType(guessresult, checktype='text'):
    """
    ------------------------------------------------------------
    this should probably have been included in mimetypes...
    ------------------------------------------------------------
    """
    (mimetype, encoding) = guessresult
    return (encoding == None and                     # not a zip, etc?
            mimetype != None and                     # a known ext type?
            mimetype.split('/')[0] == checktype)     # ok: check main type


def walkAndConvert(rootpath, mode, encoding, 
                       iffext=Iffext, tracelevel=Trace, debug=Debug):
    """
    ------------------------------------------------------------
    convert all text files in a tree, per files' MIME types, 
    and using mode=todos/tounix and encoding=Unicode type;
    tracelevel: 0=none, 1=converted, 2=converted+unchanged;
    debug: if True, print results but do not update any files;
    ------------------------------------------------------------
    """
    numvisited = numconverted = numunchanged = numfailed = numempties = 0
    for (dirhere, subshere, fileshere) in os.walk(rootpath):
        for filename in fileshere:

            if iffext and not filename.endswith(iffext):
                # skip files not of interest
                continue

            filepath = os.path.join(dirhere, filename)
            if os.path.islink(filepath) or (not os.path.isfile(filepath)):
                # skip symlinks and fifos (etc)
                print('\tNonfile:', filepath)
                continue
  
            guessresult = mimetypes.guess_type(filename)
            if isMimeMainType(guessresult, 'text'):
                # an uncompressed text file, per its extension
                numvisited += 1
                if os.path.getsize(filepath) == 0:
                    numempties += 1   # these are never changed
                try:
                    # try to convert this file
                    changed = fixeoln.convertEndlines(mode, filepath, encoding,
                                                      reraise=True, debug=debug)
                except Exception as Why:
                    # bad Unicode, permission: fixeoln shows error
                    numfailed += 1
                else:
                    # file was changed or skipped
                    if changed:
                        numconverted += 1
                        if tracelevel > 0:
                            print('Converted:', filepath)
                    else:
                        numunchanged += 1
                        if tracelevel > 1:
                            print('\tUnchanged:', filepath)

    return (numvisited, numconverted, numunchanged, numfailed, numempties)


if __name__ == '__main__':
    #
    # main logic
    #
    errmsg = 'Required arguments missing: ["todos"|"tounix"] rootdir encoding?'
    assert (len(sys.argv) >= 3 and sys.argv[1] in ['todos', 'tounix']), errmsg

    mode, dirname = sys.argv[1:3]
    encoding = 'UTF-8' if len(sys.argv) < 4 else sys.argv[3]
    print('Using mode=%s, rootdir=%s, encoding=%s' % (mode, dirname, encoding))

    metrics = walkAndConvert(dirname, mode, encoding)
    summary = ('\n--SUMMARY--\n'
               'Visited %d files:'
                   '\n\tConverted: %5d'
                   '\n\tUnchanged: %5d'
                   '\n\tFailures:  %5d'
                   '\n\tEmpties:   %5d')
    print(summary % metrics)

