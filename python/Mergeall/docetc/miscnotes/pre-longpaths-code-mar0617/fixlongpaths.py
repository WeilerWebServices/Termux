r"""
==============================================================================
fixlongpaths.py:
    work around Windows path-length limits (part of the mergeall system [3.0])

On Windows, work around the normal 260-character pathname length limit,
by extending the built-in open() to prefix paths with '\\?\'.  This fix is
used by mergeall, diffall, and cpall to support long pathnames on Windows.
Also provide a path fixer that can be used in other file-tool contexts.

This is a direct add for local-drive paths:
   'C:\folder...' => '\\?\C:\folder...'
but requires a minor reformatting step for network-drive paths:
   '\\server\folder...' => '\\?\UNC\server\folder...'
Either way, this prefix lifts the pathname length limit to 32k characters,
with 255 characters generally allowed per path component.

Pathnames are also run through abspath() to ensure they are absolute here
as needed for path prefixing.  This call also changes any '/' to '\' which
is required in this scheme: unlike the normal Windows file API, the API
invoked by '\\?\' does not do this automatically.  abspath() incurs a
minor speed hit (which isabs() + .replace('/', '\\') might minimize), but
it is run only for rare too-long pathnames.  '/' may crop up in GUIs.

Long paths seem most common when saving web pages (titles become filenames!),
and they generate open() exceptions and other failures without this fix.
Note that the 260-character size limit on Windows includes 1 byte for NULL
and 3 for the 'C:\' drive name, so the content length limit is 256, and the
string length limit is actually 259 in Python before hitting the C libraries.

For more details on Windows path-limit madness, see:
    -> https://msdn.microsoft.com/en-us/library/aa365247.aspx#maxpath.
For a demo of the fix in action apart from the code here, see:
    -> docetc/miscnotes/demo-3.0-long-windows-paths-fix.txt.
See also this file's self-test code and its expected output below.

DISCUSSION:

This is a Windows-only fix, and addresses limits in the Windows API itself,
not in filesystems (e.g., long paths and devices that fail on Windows work on
Mac OS X).  All filesystems in common use, including exFAT, FAT, and NTFS
support fle pathnames up to 32K with 255-character components:

    https://msdn.microsoft.com/en-us/library/
        windows/desktop/ee681827(v=vs.85).aspx#limits

Also note that Windows 10 removes the 260-character path limit, but for
compatibility reasons this is provided only as an option that must be
explicitly enabled via registry settings or Group policy selections (and
is fully irrelevant to some 1G machines running older versions of Windows):

    https://msdn.microsoft.com/en-us/library/
          windows/desktop/aa365247(v=vs.85).aspx#maxpath

Other platforms fare better.  On Mac OS X, the total path limit is likely 1024
with 255 for each filename component, and on Linux these limits can be 4096 and
255, though these details can vary per both filesystem and system version.  In
any event, these platforms' limits are large enough to be safely ignored here.

TBD: should long paths also be prefixed in contexts other than open()?
If so, need to factor out path extension logic and use nearly everywhere,
which may be prohibitive.  However, files on too-long paths can be both
listed and removed without changing their pathnames, so this seems moot.

UPDATE: it's not moot -- os.lstat() fails and os.path.isfile() simply returns
False for files at long paths, unless these paths are also fixed (again, see
docetc/miscnotes/demo-3.0-long-windows-paths-fix.txt).  The fix is now applied
for these cases in mergeall too, though other cases may need to be patched as
uncovered.  In the process, the path-prefix logic was made a separate tool
for other contexts; the already-used OPEN is now just a minor extension. 
==============================================================================
"""

from __future__ import print_function
import sys, os
trace = False  # show expanded paths?


def fixLongWindowsPath(pathname, trace=False):
    """
    [3.0] Fix too-long paths on Windows (only) by prefixing as
    needed to invoke APIs that support extended-length paths.
    See this file's main docsting for more details on the fix.
    Call this before other Python file-path tools as needed.
    """
    if not sys.platform.startswith('win'):
        # Mac, Linux, etc.: no worries
        return pathname
    else:
        if len(pathname) <= 259:
            # Windows path within limits: ok
            return pathname
        else:
            # Windows path too long: fix it
            pathname = os.path.abspath(pathname)      # to absolute, and / => \
            extralenprefix = r'\\?' + '\\'            # i.e., \\?\, or '\\\\?\\'
            if not pathname.startswith('\\\\'):
                # local drives                        # C:\dir => \\?\C:\dir
                pathname = extralenprefix + pathname
            else:
                # network drives                      # \\dev => \\?\UNC\dev
                pathname = extralenprefix + 'UNC' + pathname[1:]
            if trace: print('Extended path =>', pathname[:60])
            return pathname


def OPEN(pathname, *pargs, **kargs):   # 3.X kwonly args not an option for trace
    """
    [3.0] Extend built-in open() to support long pathnames on Windows.
    To leverage, import and use this instead of the built-in open().
    Importing "as open" works but probably hides the magic too much.
    This was more before fixLongPath() was pulled out for other cases.
    """

    pathname = fixLongWindowsPath(pathname)
    if trace: print('opening', pathname[:70])
    return open(pathname, *pargs, **kargs)

    # original coding
    """
    if not sys.platform.startswith('win'):
        # Mac, Linux, etc.: no worries
        return open(pathname, *pargs, **kargs)
    else:
        if len(pathname) <= 259:
            # Windows nomal case: no worries
            return open(pathname, *pargs, **kargs)
        else:
            # long path on Windows
            pathname = os.path.abspath(pathname)     # absolute, and / => \
            extralenprefix = r'\\?' + '\\'           # i.e., \\?\ (or '\\\\?\\')
            if not pathname.startswith('\\\\'):
                # local drives: C:\
                pathname = extralenprefix + pathname
            else:
                # network drives: \\dev => UNC\dev
                pathname = extralenprefix + 'UNC' + pathname[1:]  
            if trace: print('opening', pathname[:70])
            return open(pathname, *pargs, **kargs)
    """


if __name__ == '__main__':
    # test1
    print('-'*20, 'test normal short paths: local drive')
    path = r'C:\Users\me\uni2.py'
    print('len=%d' % len(path), path[:60])
    f = open(path, 'r')
    print('bltin: ', f.readline().rstrip())
    f = OPEN(path, 'r')
    print('worked:', f.readline().rstrip())

    # test2
    print('-'*20, 'test normal short paths: network drive')
    path = r'\\readyshare.routerlogin.net\USB_Storage\.Trashes'
    print('len=%d' % len(path), path[:60])
    f = open(path, 'r')
    print('bltin: ', f.readline().rstrip())
    f = OPEN(path, 'r')
    print('worked:', f.readline().rstrip())

    # test3
    print('-'*20, 'test normal short paths: arguments')
    path = r'C:\Users\me\temp.txt'
    print('len=%d' % len(path), path[:60])
    f = OPEN(path, mode='w')
    f.write('new spam\n')
    f.close()
    f = OPEN(path)
    print('worked:', f.readline().rstrip())

    # test4
    print('-'*20, 'test rare long paths: local drive')
    path = (r'C:\Users\me'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678')
    path = path + '/' + 'EGGS01234567890123456789.txt'
    print('len=%d' % len(path), path[:60])
    
    try:
        f = open(path)
    except Exception as E:
        print('failed as expected\n', str(E)[:75])

    f = OPEN(path)
    print('worked:', f.read().rstrip())

    # test5
    print('-'*20, 'test rare long paths: network drive')
    path = (r'\\readyshare.routerlogin.net\USB_Storage\TransferMark'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\01234567890123456789012345678901234567890123456789'
                         r'\0123456789012345678901234567890123456789')
    path = path + '/' + 'EGGS01234567890123456789.txt'
    print('len=%d' % len(path), path[:60])
    
    try:
        f = open(path, 'w')
    except Exception as E:
        print('failed as expected\n', str(E)[:75])

    f = OPEN(path, 'w')
    f.write('network spam')
    f.close()
    print('worked:', OPEN(path).readline())



# Expected output when trace=True (your drives will vary):
r"""
-------------------- test normal short paths: local drive
len=21 C:\Users\me\uni2.py
bltin:  from tkinter import *  # 3.4, 3.5, 2.7 with Tkinter
worked: from tkinter import *  # 3.4, 3.5, 2.7 with Tkinter
-------------------- test normal short paths: network drive
len=49 \\readyshare.routerlogin.net\USB_Storage\.Trashes
bltin:  Suppress Mac trash retention for this drive.
worked: Suppress Mac trash retention for this drive.
-------------------- test normal short paths: arguments
len=22 C:\Users\me\temp.txt
worked: new spam
-------------------- test rare long paths: local drive
len=276 C:\Users\me\0123456789012345678901234567890123456789012345
failed as expected
 [Errno 2] No such file or directory: 'C:\\Users\\me\\01234567890123456789
opening \\?\C:\Users\me\01234567890123456789012345678901234567890123456789\0
worked: more spam
-------------------- test rare long paths: network drive
len=276 \\readyshare.routerlogin.net\USB_Storage\TransferMark\012345
failed as expected
 [Errno 2] No such file or directory: '\\\\readyshare.routerlogin.net\\USB_S
opening \\?\UNC\readyshare.routerlogin.net\USB_Storage\TransferMark\0123456789
opening \\?\UNC\readyshare.routerlogin.net\USB_Storage\TransferMark\0123456789
worked: network spam
"""
