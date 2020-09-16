#!/usr/bin/python
r"""
================================================================================
fixeoln.py (Python 3.X or 2.X)

Convert end-line sequences in one file to Unix or DOS format as needed.
The file is changed in place, if any of its end-lines must be converted. 
See also "fixeoln-all.py" to convert all text files in a directory tree.

Copyright: 2001, 2006, 2016, 2017 by M. Lutz (learning-python.com).
License: provided freely, but with no warranties of any kind.
Adapted from the book "Programming Python", 2nd and 3rd Editions, with
changes here to remove Unicode limitations, and add 3.X/2.X portability.

Usage: 
        [python] fixeoln.py (tounix|todos) filename encoding?

Examples: 
        python fixeoln.py tounix /Stuff/websites/index.html     # Unix
        python3 docetc/fixeoln.py todos somefile.py utf8        # Unix
        py -3 docetc\fixeoln.py tounix ..\somefile.txt latin1   # Windows

Converts end-line character sequences in the single text file whose pathname and
Unicode encoding are given on the command line, to the target end-line format
("tounix" or "todos"), changing the subject file in-place.  Lines are changed
as needed to end with "\n" for "tounix" and "\r\n" for todos.  This script:

1) Works for files of _any_ Unicode encoding types, but requires the file's
encoding name (as known to Python) to be passed in on the command line as an
extra argument for some types (e.g., UTF-16).  The encoding argument defaults
to UTF-8 if omitted, which handles ASCII too, but not necessarily Latin-1.
Run again with another encoding name (e.g., "latin1") if a UTF-8 conversion
fails.  Encoding names "utf8", "utf16", and "utf32" all retain Unicode BOMs
in the file; "utf8" does not add one if none are present, but "utf-8-sig" does.

2) May be run on either Windows or Unix, to convert to either Windows or Unix
end-lines (DOS is synonymous with Windows here).  It is roughly a Python-coded,
Unicode-aware, and portable alternative to dos2unix + unix2dos Linux commands.

3) Changes end-lines only if necessary: lines and files that are already in
the target format are left unchanged.  Hence:

  a) It is harmless to convert a file more than once, because already-correct
     lines are ignored.

  b) Files with mixed end-line sequences are handled properly, because only
     lines not in the target format are converted.

  c) Files that either are empty, have text but no end-line characters,
     or have only end-line characters in the target format are unchanged.

Mixed end-lines are common when editing DOS-format files in some Unix editors,
such as TextEdit on Mac OS X, and display oddly in some editors (e.g., Notepad,
but not Wordpad or PyEdit) unless converted to a uniform and recognized format.

USAGE EXAMPLE AND NOTES:

See file "fixeoln-test.txt" in this script's docetc folder for a usage example.
To inspect the result interactively: open('filename', 'rb').read()[:500].
To try this script on different encoding types, see and run "unicodemod.py".
To apply this to many files: use a Unix find, or Python os.walk() or glob
[update: use the newer "fixeoln-all.py" to apply to all text files in a tree].

SEE ALSO:

File "fixeoln-old-bytes.py" in this script's docetc folder is an earlier variant
that used bytes files and processing and did not require an encoding name, but
failed for files saved in Unicode encodings that do not map end-line characters
to single bytes or may falsely produce their ASCII values algorithmically.
Also see the tree-wide script "fixeoln-all.py" as noted above.

CODING NOTES:

1) To handle all encodings well, this script uses text file modes and Unicode
strings (str in 3.X); equates open() to codecs.open() in 2.X; and passes to
open() both a Unicode encoding name possibly given by the user, and argument
newline='' in 3.X only to suppress end-line translations (codecs.open() never
translates end-lines, and always uses binary mode regardless of its mode
argument).  Text file mode is especially important, to avoid having to detect
encoded end-line character bytes in any Unicode encoding.

2) This script also explicitly closes both input and output files.  This is
not necessary when run by itself (there is just one of each, closed on script
exit), and isn't required when run by CPython (which auto-closes open file
objects during garbage collection when their last reference is removed).
But explicit closes were added for use by the fixeoln-all.py script (that
may convert many files) and other Python implementations (with different GC).

CAVEATS/TBDs:

1) This script keeps the file's entire content in memory, and may fail for
very large files; to do better, write lines as they are read to a temp file.

2) 2.X's codecs.open() is also available in 3.X, and could be used portably
here instead of tailoring code per Python version (but this is illustrative).

3) This script changes the file in-place without first writing to a temporary
and moving it, because encoding errors are likely to happen during input
before the output rewrite is attempted, and permission errors will preclude
erasing the prior content.  This reasoning is to be verified with use.
================================================================================
"""

from __future__ import print_function   # 2.X compatibility
import os, sys, codecs
Debug = False

  
def convertEndlines(mode, fname, encoding, reraise=False, debug=Debug):
    """
    ----------------------------------------------------------------
    Convert end-lines in one file, in-place.
    if mode is tounix: change any and all \r\n => \n
    if mode is todos:  change any and all <non\r>\n => \r\n
    if reraise: propagate all exceptions to caller
    if debug: detect/report required changes but bon't update file
    ----------------------------------------------------------------
    """
    if not os.path.isfile(fname):                         
        print('Not a valid text file:', fname)     # skip directories                  
        return False                               # caller: skip symlinks, fifos

    #
    # open the file
    #
    try:     
        # decode text, but retain \r on Windows
        if sys.version.startswith('3'):
            file = open(fname, mode='r', encoding=encoding, newline='')
        else:
            file = codecs.open(fname, mode='r', encoding=encoding)

    except Exception as why:
        print('Error opening file %s: skipped (%s)' % (fname, why))
        if reraise:
            raise          # caller gets exc too
        else:
            return False   # end exc with report here

    #
    # read and convert
    #
    newlines = []
    changed  = False
    try:
        for line in file.readlines():                      # use text i/o modes,
            if mode == 'todos':                            # ignore bytes diffs
                if line[-1:] == '\n' and line[-2:-1] != '\r':
                    line = line[:-1] + '\r\n'
                    changed = True

            elif mode == 'tounix':                         # slices are scaled:
                if line[-2:] == '\r\n':                    # avoids IndexError
                    line = line[:-2] + '\n'
                    changed = True
            newlines.append(line)

    except Exception as why:
        print('Error reading file %s: skipped (%s)' % (fname, why))
        if reraise:        # encoding, permission
            raise          # caller gets exc too
        else:
            return False   # end exc with report here

    finally:
        file.close()       # always: fixeoln-all

    #
    # write if changed (and not debug)
    #
    if changed:
        file = None
        try:
            # re-encode text, but don't expand \n on Windows
            if debug:
                pass  # testing mode
            else:
                if sys.version.startswith('3'):
                    file = open(fname, mode='w', encoding=encoding, newline='')
                else:
                    file = codecs.open(fname, mode='w', encoding=encoding) 
                file.writelines(newlines)

        except IOError as why:
            print('Error writing to file %s: skipped (%s)' % (fname, why))
            if reraise:             # might be read-only
                raise               # caller gets exc too
            else: 
                return False        # end exc with report here

        finally:
            if file: file.close()   # always: fixeoln-all

    return changed   # tell caller know what we found



if __name__ == '__main__':
    # 
    # main logic
    #
    errmsg = 'Required arguments missing: ["todos"|"tounix"] filename encoding?'
    assert (len(sys.argv) >= 3 and sys.argv[1] in ['todos', 'tounix']), errmsg

    mode, fname = sys.argv[1:3]
    encoding = 'UTF-8' if len(sys.argv) < 4 else sys.argv[3]
    print('Using mode=%s, file=%s, encoding=%s' % (mode, fname, encoding))

    changed = convertEndlines(mode, fname, encoding)
    print('Converted' if changed else 'No changes to', sys.argv[2])
