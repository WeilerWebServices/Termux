"""
=================================================================================
Implementation of symlinks for the ziptools package.

Moved here because this is fairly gross code - and should not
be required of clients of Python's zipfile module: fix, please!

ziptools zips and unzips symlinks portably on Windows and Unix, subject
to the constaints of each platform and Python's libraries.  Symlinks path
separators are not portable between Windows and Unix, but link path are
auto-adjusted here for the hosting platform's syntax unless "nofixlinks".
See ziptools.py's main docstring for more symlinks documentation.

Caveat: symlinks are not supported on Windows in Python 2.X (3.2- is marginal).
Caveat: Windows requires admin permission to write symlinks (use right-clicks).
Caveat: Windows supports symlinks only on NTFS filesystem drives (not exFAT/FAT).
Caveat: symlinks are not present in Windows until Vista (XP is right out).
=================================================================================
"""
import os, sys, time
import zipfile as zipfilemodule   # versus the passed zipfile object


#===============================================================================

"""
ABOUT THE "MAGIC" BITMASK

Magic = type + permission + DOS is-dir flag?
    >>> code = 0xA1ED0000
    >>> code
    2716663808
    >>> bin(code)
    '0b10100001111011010000000000000000'

Type = symlink (0o12/0xA=symlink 0o10/0x8=file, 0o04/0x4=dir) [=stat() bits]
    >>> bin(code & 0xF0000000)
    '0b10100000000000000000000000000000'
    >>> bin(code >> 28)
    '0b1010'
    >>> hex(code >> 28)
    '0xa'
    >>> oct(code >> 28)
    '0o12'

Permission = 0o755 [rwx + r-x + r-x]
    >>> bin((code & 0b00000001111111110000000000000000) >> 16)
    '0b111101101'
    >>> bin((code >> 16) & 0o777)
    '0b111101101'

DOS (Windows) is-dir bit
    >>> code |= 0x10 
    >>> bin(code)
    '0b10100001111011010000000000010000'
    >>> code & 0x10
    16
    >>> code = 0xA1ED0000
    >>> code & 0x10
    0

Full format:
    TTTTsstrwxrwxrwx0000000000ADVSHR
    ^^^^____________________________ file type, per sys/stat.h (BSD)
        ^^^_________________________ setuid, setgid, sticky
           ^^^^^^^^^________________ permissions, per unix style
                    ^^^^^^^^________ Unused (apparently)
                            ^^^^^^^^ DOS attribute bits: bit 0x10 = is-dir

Discussion:
    http://unix.stackexchange.com/questions/14705/
        the-zip-formats-external-file-attribute
    http://stackoverflow.com/questions/434641/  
        how-do-i-set-permissions-attributes-
        on-a-file-in-a-zip-file-using-pythons-zip/6297838#6297838
"""

SYMLINK_TYPE  = 0xA
SYMLINK_PERM  = 0o755
SYMLINK_ISDIR = 0x10
SYMLINK_MAGIC = (SYMLINK_TYPE << 28) | (SYMLINK_PERM << 16)

assert SYMLINK_MAGIC == 0xA1ED0000, 'Bit math is askew'    


#===============================================================================

def addSymlink(filepath, zipfile):
    """
    Create: add a symlink (to a file or dir) to the archive.

    This adds the symlink itself, not the file or directory it refers to, and
    uses low-level tools to add its link-path string.  Python's zipfile module
    does not support symlinks directly: see https://bugs.python.org/issue18595.
    Use atlinks=True in ziptools.py caller to instead add items links refer to.

    Windows requires administrator permission and NTFS to create symlinks, 
    and a special argument to denote directory links if dirs don't exist: the
    dir-link bit set here is used by extracts to know to pass the argument.

    Note: the ZipInfo constructor sets create_system and compress_type (plus
    a few others), so their assignment code here is not required but harmless.
    Note: os.path normpath() can change meaning of a path that with symlinks,
    but it is used here on the path of the link itself, not the link-path text.
    """
    assert os.path.islink(filepath)
    linkpath = os.readlink(filepath)                # str of link itself
    
    # 0 is windows, 3 is unix (e.g., mac, linux) [and 1 is Amiga!]
    createsystem = 0 if sys.platform.startswith('win') else 3 

    # else time defaults in zipfile to Jan 1, 1980
    linkstat = os.lstat(filepath)                   # stat of link itself
    origtime = linkstat.st_mtime                    # mtime of link itself
    ziptime  = time.localtime(origtime)[0:6]        # first 6 tuple items

    # zip mandates '/' separators in the zipfile
    zippath = os.path.splitdrive(filepath)[1]       # drop Windows drive, unc
    zippath = os.path.normpath(zippath)             # drop '.', double slash...
    zippath = zippath.lstrip(os.sep)                # drop leading slash(es)
    zippath = zippath.replace(os.sep, '/')          # no-op if unix or simple
   
    newinfo = zipfilemodule.ZipInfo()               # new zip entry's info
    newinfo.filename      = zippath
    newinfo.date_time     = ziptime
    newinfo.create_system = createsystem            # woefully undocumented
    newinfo.compress_type = zipfile.compression     # use the file's default
    newinfo.external_attr = SYMLINK_MAGIC           # type plus permissions

    if os.path.isdir(filepath):                     # symlink to dir?
        newinfo.external_attr |= SYMLINK_ISDIR      # DOS directory-link flag

    zipfile.writestr(newinfo, linkpath)             # add to the new zipfile


#===============================================================================

def isSymlink(zipinfo):
    """
    Extract: check the entry's type bits for symlink code.
    This is the upper 4 bit, and matches os.stat() codes.
    """
    return (zipinfo.external_attr >> 28) == SYMLINK_TYPE


#===============================================================================

def extractSymlink(zipinfo, pathto, zipfile, nofixlinks=False):
    """
    Extract: read the link path string, and make a new symlink.
    
    On Windows, this requires admin permission and an NTFS destination drive.
    On Unix, this generally works with any writable drive and normal permission.
    
    Uses target_is_directory on Windows if flagged as dir in zip bits: it's not
    impossible that the extract may reach a dir link before its dir target.

    Adjusts link path text for host's separators to make links portable across
    Windows and Unix, unless 'nofixlinks' (whihc is command arg -nofixlinks).
    This is switchable because it assumes the target is a drive to be used
    on this patform  - more likely here than for mergeall external drives.

    Caveat: some of this code mimics that in zipfile.ZipFile._extract_member(),
    but that library does not expose it for reuse here.  Some of this is also
    superfluous if we only unzip what we zip (e.g., Windows drive names won't
    be present and upper dirs will have been created), but that's not ensured. 
    
    TBD: should we also call os.chmod() with the zipinfo's permission bits?
    TBD: does the UTF8 decoding of the unzip pathname here suffice everywhere?
    """
    assert zipinfo.external_attr >> 28 == SYMLINK_TYPE
    
    zippath  = zipinfo.filename                       # pathname in the zip 
    linkpath = zipfile.read(zippath)                  # original link path str
    linkpath = linkpath.decode('utf8')                # must be same types

    # undo zip-mandated '/' separators on Windows
    zippath  = zippath.replace('/', os.sep)           # no-op if unix or simple

    # drop Win drive + unc, leading slashes, '.' and '..'
    zippath  = os.path.splitdrive(zippath)[1]
    zippath  = zippath.lstrip(os.sep)                 # if other programs' zip
    allparts = zippath.split(os.sep)
    okparts  = [p for p in allparts if p not in ('.', '..')]
    zippath  = os.sep.join(okparts)

    # where to store link now
    destpath = os.path.join(pathto, zippath)          # hosting machine path
    destpath = os.path.normpath(destpath)             # perhaps moot, but...

    # make leading dirs if needed
    upperdirs = os.path.dirname(destpath)
    if not os.path.exists(upperdirs):                 # don't fail if exists
        os.makedirs(upperdirs)                        # exists_ok in py 3.2+

    # adjust link separators for the local platform
    if not nofixlinks:
        linkpath = linkpath.replace('/', os.sep).replace('\\', os.sep)

    # test+remove link, not target
    if os.path.lexists(destpath):                     # else symlink() fails
        os.remove(destpath)

    # windows dir-link arg
    isdir = zipinfo.external_attr & SYMLINK_ISDIR
    if (isdir and                                     # not suported in 2.X
        sys.platform.startswith('win') and            # ignored on unix in 3.3+
        int(sys.version[0]) >= 3):                    # never required on unix 
        dirarg = dict(target_is_directory=True)
    else:
        dirarg ={}

    # make the link in dest (mtime: caller)
    os.symlink(linkpath, destpath, **dirarg)          # store new link in dest
    return destpath                                   # mtime is set in caller
