#!/usr/bin/python
r"""
================================================================================
rollback.py:
    build and run a restore command line (part of the mergeall system)
    
Usage:
    [py[thon]] rollback.py [archiverootpath]

Rollbacks (a.k.a. restores) run by this script back out all changes made
during the most recent mergeall run with backups enabled.  See UserGuide.html,
and docetc/MoreDocs' Whitepaper.html and Revisions.html for background details
on mergeall 2.1+'s restores.

This simple convenience script, added in [2.1], finds the latest backup folder,
and builds and runs a mergeall.py automatic-updates restore-mode command line,
given just an archive's root path on the command line or interactively.  It
prints and prompts to stderr, so that the user may redirect mergeall's stdout
output (only) to a log file  via ">".  To rollback multiple merges on a device,
delete the most recent __bkp__ subfolder before each subsequent rollback.py run.
    
On Windows, run this from a Command Prompt or by file-icon clicks, not in IDLE
(which pops up a transient window for os.system).  On Mac OS X and Linux, run
this from a Terminal (or other) command line as usual.  Provide the pathname
of the root folder of the archive you wish to rollback, as argument or input.

EXAMPLES, on Unix, Windows, and either:

    ~/...$ python3 rollback.py /MY-STUFF  > savelog.txt
    C:...> py -3   rollback.py C:\MyStuff > savelog.txt
    ...... python  rollback.py   # input path when asked, and scroll output

A more realistic example:
    ~/Desktop$ py3 /MY-STUFF/Code/mergeall/rollback.py /Volumes/SSDT3/MY-STUFF
             > /Admin-Mergeall/ssdt3-500g/jan-31-17/rollback.txt

[3.0] The backup folder's __added__.txt file's paths are now made portable
in mergeall's code by translating any separator characters, so backups made
on Unix can be rolled back on Windows, and vice versa.

[3.0] Note: this script doesn't care about "-skipcruft" because rollbacks
reset the root to its prior state, regardless of whether cruft skipping was
enabled in the prior run or not.  Rollbacks put back whatever was destroyed.

[3.0] Note: there is also no reason to use "-quiet" here to minimize messages:
"-backup" isn't passed, so no backups are performed.  Manual restore command
lines may pass "-backup", but it's mostly moot (rollbacks can't be rolled back).

[3.0] Note: when this is frozen in the Mac app, all .py files are in Resources
but this is launched with a MacOS python executable that bundles everything used
by mergeall.py.  On Windows and Linux freezes, rollback and mergeall are both
standalone exes which embed all their own requirements.

[3.0] Especially for Windows, enhance the os.system() command lines to allow
for spaces in mergeall, python, and pathnames.  This isn't required for the
GUI and console launchers' spawns, because they both use subprocess.Popen()
command sequences that are auto-formatted as needed for Windows (by contrast,
PyEdit uses command strings that must be manually preformatted as needed).
================================================================================
"""
from __future__ import print_function          # Py 2.X
import os, sys, glob, shlex
if sys.version[0] == '2': input = raw_input    # Py 2.X

# [3.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')
RunningOnLinux   = sys.platform.startswith('linux')

def display(*args, **kargs):
    print(*args, file=sys.stderr, **kargs)

def prompt(message):
    display(message, end=' ')
    return input()
    
def error(message):
    display(message)
    display('Run cancelled.')
    
display('**Warning**\n\n'
    'This script builds and runs a command to automatically restore the tree,\n'
    'whose root path is given on the command line or interactively, to its\n'
    'state prior to its most recent mergeall synch.  It assumes that the tree\n'
    'has not been changed since this synch, and further assumes that the latest\n'
    'synch was run with backups enabled.  This rollback cannot be undone\n'
    'automatically.\n')

ans = prompt('Are you sure you want to do this (y=yes)?')
if ans.lower() not in ['y', 'yes']:
    prompt('Run cancelled.  Press Enter to exit.')
    sys.exit()

if len(sys.argv) == 2:
    rootfolder = sys.argv[1]                      # command-line arg
elif len(sys.argv) == 1:
    rootfolder = prompt('Archive root path?')     # interactive reply?
else:                       
    rootfolder = ''

if not rootfolder:
    error('Usage error: archive root path input missing or invalid.')
elif not os.path.isdir(rootfolder):
    error('Error: your archive root path is not a valid directory.')
else:
    try:
        bkproot = os.path.join(rootfolder, '__bkp__')      
        backups = glob.glob(os.path.join(bkproot, 'date*-time*'))
        if len(backups) == 0:
            error('Error: there are no backup folders in your archive.')
        else:
            backups.sort()
            bkpfolder = backups[-1]    # last=newest

            # [3.0] scripts not in os.getcwd() if run from a cmdline elsewhere, and 
            # __file__ may not work if running as a frozen PyInstaller executable;
            # use __file__ of this file for Mac apps, not module: it's in a zipfile;
            mypath = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute

            if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
                # pyinstaller exe [3.0]
                # run frozen executable directly, not script through python
                freezename = 'mergeall.exe' if RunningOnWindows else 'mergeall'
                frozenpath = os.path.join(mypath, freezename)
                
                if RunningOnWindows:
                    # allow for spaces: ""C:\Program Files\..." args"
                    cmdline = 'cmd /S /C ""%s" "%s" "%s" -auto -restore"'
                    cmdline %= (frozenpath, bkpfolder, rootfolder)
                else:
                    # allow for spaces: adds '...' plus nesteds if needed
                    cmdline = '%s %s %s -auto -restore'
                    cmdline %= tuple(shlex.quote(x)
                        for x in (frozenpath, bkpfolder, rootfolder))

            else:
                # py2app Mac app or source (original code)
                # run script though local or app python executable
                scriptpath = os.path.join(mypath, 'mergeall.py')
                
                if RunningOnWindows:
                    # allow for spaces: ""C:\Program Files\..." args"
                    cmdline = 'cmd /S /C ""%s" "%s" "%s" "%s" -auto -restore"'
                    cmdline %= (sys.executable, scriptpath, bkpfolder, rootfolder)

                else:
                    # allow for spaces: adds '...' plus nesteds if needed
                    cmdline = '%s %s %s %s -auto -restore'
                    cmdline %= tuple(shlex.quote(x)
                        for x in (sys.executable, scriptpath, bkpfolder, rootfolder))
                
            display('Running rollback command:\n....', cmdline)
            os.system(cmdline)
    except:
        error('Error: %s %s' % (sys.exc_info()[0], sys.exc_info()[1]))

prompt('Press Enter to exit.')   # stay open on Windows
