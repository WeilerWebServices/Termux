#===============================================================================
# Test ziptools by zipping, unzipping, and comparing to originals zipped.
# Formerly in ziptools.ziptols.py, before it was moved to a subpackage.
# Python 3.X doesn't very well support files that are both script+module.
#===============================================================================

import sys, os

from ziptools import createzipfile, extractzipfile   # main tools
from ziptools import cruft_skip_keep                 # default cruft patterns
from ziptools import tryrmtree                       # pre-extract utility

if __name__ == '__main__':
    """
    Self-test, run in script's folder (and edit me: your context may vary).
    Makes a zip file, unzips it, and compares results to original data.
    See zip-create.py, zip-extract.py, zip-list.py for command-line clients.
    """
        
    def announce(*args):
        print('\n\n****', *args, '****\n')

    #----------------------------------------------------------------
    # configure test run parameters
    #----------------------------------------------------------------

    # map test to test subdir names
    skipcruft = len(sys.argv) > 1    # any cmdline arg?
    platform  = sys.platform         # win32, darwin, or linux
    
    cruftsubdir = 'skipcruft' if skipcruft else 'withcruft'
    platsubdir  = dict(win32='Windows', darwin='MacOSX', linux='Linux')[platform]

    # make+use folder here to create and extract a zipfile
    testsubdir = os.path.join('selftest', platsubdir, cruftsubdir)
    if not os.path.exists(testsubdir):              # selftest\Windows\withcruft
        os.makedirs(testsubdir)                     # selftest/MacOSX/skipcruft
    zipto = os.path.join(testsubdir, 'ziptest.zip') # plus the zip file target

    # use test data dirs in '..' parent [**EDIT ME**]
    origin  = '..'
    folders = ['test1', 'test2']                    # i.e., [../test1, ../test2]
    sources = [(origin + os.sep + folder) for folder in folders]

    #----------------------------------------------------------------
    # zip original source dirs to subdir file
    #----------------------------------------------------------------
    
    announce('CREATING')
    if not skipcruft:                     # any cmdline arg? use cruft patts
        createzipfile(zipto, sources)     # else keep cruft: use {} default
    else:
        createzipfile(zipto, sources, cruftpatts=cruft_skip_keep)    

    #----------------------------------------------------------------
    # unzip subdir file to subdir dirs, cleaning first if needed
    #----------------------------------------------------------------
    
    announce('EXTRACTING')
    for folder in folders:
        tryrmtree(os.path.join(testsubdir, folder))     # clean extract targets
    extractzipfile(zipto, testsubdir)                   # extract in testsubdir 

    #----------------------------------------------------------------
    # compare zipped+unzipped subdir dirs to original source dirs
    #----------------------------------------------------------------

    # use mergeall's diff and merge for validation [EDIT ME]
    mergeallpath = os.path.join('..', '..', 'mergeall.py')
    diffallpath  = os.path.join('..', '..', 'diffall.py')

    # compare structure + file modtimes
    for folder in folders:
        announce('COMPARING MODTIMES:', folder)
        pipe = os.popen('%s %s %s %s -report' %
                        (sys.executable, mergeallpath,
                         os.path.join(origin, folder),
                         os.path.join(testsubdir, folder)))
        for line in pipe: 
            print(line, end='')

    # compare by full-file content
    for folder in folders:
        announce('COMPARING CONTENT:', folder)
        pipe = os.popen('%s %s %s %s' %
                        (sys.executable, diffallpath,
                         os.path.join(origin, folder),
                         os.path.join(testsubdir, folder)))
        for line in pipe: 
            print(line, end='')

    if sys.platform.startswith('win'):
        if sys.version[0] == '2':
            input = raw_input 
        input('Press Enter to exit.')  # stay up if clicked
