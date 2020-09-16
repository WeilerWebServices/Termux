#!/usr/bin/python
"""
================================================================================
Usage: "python fixeoln-bytes.py [tounix|todos] filename"

**SEE ALSO fixeoln.py in this script's folder for a variant that solves
  this script's Unicode limitations, but also may require an encoding name.

Convert end-line character sequences in the single text file whose name is
given on the command line, to the target end-line format ("tounix" or "todos"),
changing the subject file in-place.  This script:

1) Works _only_ for files whose Unicode encoding maps end-line characters to
single bytes and cannot generate a false ASCII end-line byte algorithmically.
It works for files encoded per ASCII, Latin-1, and UTF-8, but not UTF-16.

2) May be run on either Windows or Unix, to convert to either Windows or Unix
end-lines (DOS is synonymous with Windows in this context).  It is roughly a
Python-coded and portable alternative to dos2unix + unix2dos Linux commands.

3) Changes end-lines only if necessary: lines and files that are already in
the target format are left unchanged.  It's harmless to convert a file > once,
and files with mixed end-line sequences are handled properly.

To inspect the result interactively: open('filename', 'rb').read()[:500].
To apply this to many files: use a Unix find, or Python os.walk() or glob.  

Adapted from the book "Programming Python", 2nd and 3rd Editions, with minor
edits, 3.X + 2.X conversion (for prints and bytes), and notes about Unicode
limitations.  Copyright M. Lutz (learning-python.com), 2001, 2006, 2016.
License: provided freely but with no warranties of any kind.

================================================================================

CODING NOTES: as coded, this script must use binary file open modes for this
to work on Windows, else the default text mode automatically deletes the \r
on reads, and adds an extra \r for each \n on writes.  If targeting only
end-lines for the running platform, this is much simpler: use

  open('rb') + read() + splitlines() + write(line + (b'\n' or b'\r\n').

The portable os.linesep, however, would require a Unicode encoding type.

================================================================================

MAJOR CAVEAT: this script naively assumes that '\r' and '\n' each occupy a
single byte in the subject file.  It will thus work for ASCII, UTF-8, and
Latin-1 files, but fail for files using wider Unicode encodings such as UTF-16.

More subtly, this script also assumes that the file's encoding won't produce
a byte of the same value as an end-line character "accidentally": all bytes with
these values are assumed to be part of end-line sequences.  This is the case
for ASCII and Latin-1 naturally, but also for UTF-8 by virtue of its encoding
algorithm (see other resources for details).

To handle all encodings well, this would have to be rewritten to use text file
mode; equate open() to codecs.open() in 2.X; and pass to open() both a Unicode
encoding name given by the user, and a newline='' argument in 3.X only to
suppress end-line translations to allow inspection (codecs never translates).

See fixeoln.py in this script's folder for a Unicode-aware variant of this
script that addresses this issue, but requires an encoding name or default.

================================================================================

PYTHON MAKES THIS MISTAKE TOO: Python's bytes.splitlines() makes the same
naive 1-byte assumption (this really should be supported only for Unicode str):

>>> 'spam\neggs\n'.splitlines()
['spam', 'eggs']

>>> 'spam\neggs\n'.encode('utf8')
b'spam\neggs\n'
>>> 'spam\neggs\n'.encode('utf8').splitlines()
[b'spam', b'eggs']
>>> 'spam\neggs\n'.encode('utf8').splitlines()[-1].decode('utf8')
'eggs'

>>> 'spam\neggs\n'.encode('utf16')
b'\xff\xfes\x00p\x00a\x00m\x00\n\x00e\x00g\x00g\x00s\x00\n\x00'
>>> 'spam\neggs\n'.encode('utf16').splitlines()
[b'\xff\xfes\x00p\x00a\x00m\x00', b'\x00e\x00g\x00g\x00s\x00', b'\x00']
>>> 'spam\neggs\n'.encode('utf16').splitlines()[-1].decode('utf16')
UnicodeDecodeError: 'utf-16-le' codec can't decode byte 0x00 in position 0: truncated data

>>> 'spam\neggs\n'.encode('utf-16-be')
b'\x00s\x00p\x00a\x00m\x00\n\x00e\x00g\x00g\x00s\x00\n'
>>> 'spam\neggs\n'.encode('utf-16-be').splitlines()
[b'\x00s\x00p\x00a\x00m\x00', b'\x00e\x00g\x00g\x00s\x00']
>>> 'spam\neggs\n'.encode('utf-16-be').splitlines()[-1].decode('utf-16-be')
UnicodeDecodeError: 'utf-16-be' codec can't decode byte 0x00 in position 8: truncated data

The correct way to line-split encoded UTF-16 text is to also encode the
end-line delimiter, using a UTF-16 encoding name that suppresses the byte
order marker; but if you must know the text's encoding anyhow, you may as
well use text mode files and str Unicode objects in the first place...:

>>> '\n'.encode('utf-16')
b'\xff\xfe\n\x00'
>>> '\n'.encode('utf-16-le')
b'\n\x00'

>>> 'spam\neggs\n'.encode('utf-16-le')
b's\x00p\x00a\x00m\x00\n\x00e\x00g\x00g\x00s\x00\n\x00'
>>> 'spam\neggs\n'.encode('utf-16-le').split('\n'.encode('utf-16-le'))
[b's\x00p\x00a\x00m\x00', b'e\x00g\x00g\x00s\x00', b'']
>>> 'spam\neggs\n'.encode('utf-16-le').split('\n'.encode('utf-16-le'))[-2].decode('utf-16-le')
'eggs'

================================================================================
"""

from __future__ import print_function   # runs on Python 3.X + 2.X

import os
listonly = False   # True=show file to be changed, don't rewrite
  
def convertEndlines(mode, fname):                        # convert one file
    if not os.path.isfile(fname):                        # todos:  \n   => \r\n 
        print('Not a text file', fname)                  # tounix: \r\n => \n
        return False                                     # skip directory names
     
    newlines = []
    changed  = 0 
    for line in open(fname, 'rb').readlines():           # use binary i/o modes:
        if mode == 'todos':                              # else \r lost on Win
            if line[-1:] == b'\n' and line[-2:-1] != b'\r':
                line = line[:-1] + b'\r\n'
                changed = 1
        elif mode == 'tounix':                           # slices are scaled:
            if line[-2:] == b'\r\n':                     # avoid IndexError
                line = line[:-2] + b'\n'
                changed = 1
        newlines.append(line)
     
    if changed:
        try:                                             # might be read-only
            print('Changing', fname)
            if not listonly: open(fname, 'wb').writelines(newlines) 
        except IOError as why:
            print('Error writing to file %s: skipped (%s)' % (fname, why))
    return changed

if __name__ == '__main__':
    import sys
    errmsg = 'Required arguments missing: ["todos"|"tounix"] filename'
    assert (len(sys.argv) == 3 and sys.argv[1] in ['todos', 'tounix']), errmsg
    changed = convertEndlines(sys.argv[1], sys.argv[2])
    print('Converted' if changed else 'No changes to', sys.argv[2])
