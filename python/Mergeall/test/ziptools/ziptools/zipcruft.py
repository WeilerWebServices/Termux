"""
===========================================================================
zipcruft.py: define default cruft file/folder name patterns

This module is used by both zip-create.py and ziptools.py.
See the former for more on cruft processing in general.

Defines default files and folders to be skipped for "-skipcruft"
in the create script, and a default which can be imported and
passed by other clients to utilities in ziptools.  Edit as needed,
either here, in the create script, or in other clients.

These are case-sensitive patterns that will be matched per
Python's fnmatch module against each file and folder's base
name (not an entire pathname).  See fnmatch for pattern details.
===========================================================================
"""

# skip all files and folders matching these
cruft_skip = [
    '.*',                # UNIX hidden files, Mac companion files
    '[dD]esktop.ini',    # Windows appearance
    'Thumbs.db',         # Windows caches
    '~*',                # Office temp files
    '$*',                # Windows recycle bin
    '*.py[co]'           # Python bytecode
    ]

# never skip any matching these, even if they match a skip pattern
cruft_keep = [
    '.htaccess'          # Apache website config files
    ]

# pass the pair as a dict to ziptools.createzipfile() if desired 
cruft_skip_keep = {'skip': cruft_skip,
                   'keep': cruft_keep}
