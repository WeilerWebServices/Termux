r"""
==============================================================================
ziplongpaths.py:
   Work around Windows path-length limits (part of the ziptools system).

The code here was adapted (copied) from mergeall's fixlongpaths.py, as the
ziptools package is available both in mergeall and separately.  See mergeall's
fixlongpaths.py (http://learning-python.com/mergeall) for docs clipped here.
==============================================================================
"""

from __future__ import print_function   # py 2.x
import sys, os

TracePaths = False             # show expanded paths? (here or arg)

FileLimit  = 260 - 1           # 259 in Py, including 3 for drive, N for UNC
DirLimit   = FileLimit - 12    # 247 in Py, after reserving 12 for 8.3 name



def fixLongWindowsPath(pathname, force=False, limit=DirLimit, trace=TracePaths):
    """
    ------------------------------------------------------------------
    [3.0] Fix too-long paths on Windows (only) by prefixing as
    needed to invoke APIs that support extended-length paths.
    See this file's main docsting for more details on the fix.
    Call this before other Python file-path tools as required.
    Returns pathname either unaltered or with required expansion.
    
    Pass force=True to prefix on Windows regardless of length.
    This may be required to prefix pathnames on a just-in-case
    basis, for APIs like shutil.rmtree() and os.walk() that 
    recur into subfolders of unknown depth, and for libs that
    otherwise expand paths to unknown lengths (e.g., zipfile).

    This is given a "FWP" shorter synonym ahead for convenience:
    depending on your code it may wind up appearing at _every_
    stdlib file-tool call, but is a quick no-op where unneeded.
    ------------------------------------------------------------------
    """
    if not sys.platform.startswith('win'):
        # Mac, Linux, etc.: no worries
        return pathname
    else:
        abspathname = os.path.abspath(pathname)       # use abs len (see above)
        if len(abspathname) <= limit and not force:   # rel path len is moot
            # Windows path within limits: ok
            return pathname
        else:
            # Windows path too long: fix it
            pathname = abspathname                    # to absolute, and / => \
            extralenprefix = '\\\\?\\'                # i.e., \\?\ (or r'\\?'+'\\')
            if not pathname.startswith('\\\\'):       # i.e., \\   (or r'\\')
                # local drives: C:\
                pathname = extralenprefix + pathname  # C:\dir => \\?\C:\dir
            else:
                # network drives: \\...               # \\dev  => \\?\UNC\dev
                pathname = extralenprefix + 'UNC' + pathname[1:]
            if trace: print('Extended path =>', pathname[:60])
            return pathname



def unfixLongWindowsPath(pathname):
    """
    ------------------------------------------------------------------
    For contexts that require a just-in-case preemptive '\\?\'
    prefix (e.g., os.walk(), shutil.rmtree()), strip the prefix
    to restore the original pathname (mostly) when it is needed.
    
    May be required to get the normal folder name when using
    os.walk(); os.path.splitdrive() strips '\\?\' but also 'C:'.
    
    Note that this does NOT undo relative->absolute mapping:
    see os.path.isabs() and os.path.relpath() where required.
    ------------------------------------------------------------------
    """
    if not pathname.startswith('\\\\?\\'):      # never will on Mac, Linux
        return pathname                         # may or may not on Windows
    else:
        if pathname.startswith('\\\\?\\UNC'):
            return '\\' + pathname[7:]          # network: drop \\?\UNC, add \
        else:
            return pathname[4:]                 # local: drop \\?\ only



#---------------------------------------------------------------------
# Shorter synomyms for coding convenience
# FWP stands for "Fix Windows Paths" (officially...)
#---------------------------------------------------------------------

FWP      = fixLongWindowsPath      # generic: use most-inclusive limit (dirs)
FWP_dir  = FWP                     # or force dir-path or file/other limits
FWP_file = lambda *pargs, **kargs: FWP(*pargs, limit=FileLimit, **kargs)
UFWP     = unfixLongWindowsPath

