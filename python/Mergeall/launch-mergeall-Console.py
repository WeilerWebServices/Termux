#!/usr/bin/python
"""
================================================================================
launch-mergeall-Console.py:
  shell console launcher (part of the mergeall system)

Launch mergeall.py after inputting settings in console window (3.X and 2.X).
See also launch-mergeall-GUI.py for a GUI alternative to this console script.
The code here was experimental, and evolved with time; please pardon our dust.

Drag me out to a no-arguments shortcut on Windows to use hard-coded path
defaults in this script.  Or, pass 1 argument = name of path defaults file
in "launch-config" subdir of this directory, having from/to/log paths on
individual lines (though always asks about defaults anyhow).  Examples:

  launch-mergeall.py                                    (hardcoded defaults)
  launch-mergeall.py launch-configs\tablet-upload.txt   (tablet upload dflts)
  launch-mergeall.py launch-configs\tablet-download.txt (tablet download dflts)

TBD: see notes ahead on stdout stream input prompts and interactive mode;
until resolved, this precludes log files in interactive mergeall runs.

TBD: this is largely 2.X compatible, but may still have issues in stream
decoding for non-ASCII filenames.  This remains suggested exercise for now.

This script was patched in 1.6 for a Python 2.X Unicode issue described in the 
GUI launcher's file.  Still, because this script routes text to a console, you 
must generally set PYTHNIOENCODING in your shell for non-ASCII filenames, 
especially in 3.X; see UserGuide.html, docs/Whitepaper.html, and mergeall.py.

[2.0] This script was updated for the new '-backup' option added in release
2.0, though the GUI launcher is much more commonly used.  Unlike the GUI,
which does -report and -auto but no interactively-selected changes, arg
-backup here can apply to either -auto, or manual changes for [not -report].
Aso added note about new findings for spawnee interactive prompts issues.

[3.0] This script was updated for all the new modes, options, and porting
changes of this release, along with the GUI launcher.  See this version's
changes list in docs/Revisions.html for details.
================================================================================
"""

from __future__ import print_function         # 2.X
import sys, os, time, webbrowser, subprocess

# [3.0] for frozen app/exes, fix module+resource visibility (sys.path)
import fixfrozenpaths

RunningOnMac     = sys.platform.startswith('darwin')
RunningOnWindows = sys.platform.startswith('win')
RunningOnLinux   = sys.platform.startswith('linux')

if sys.version[0] == '2':                     # 2.X
    input = raw_input
    #import codecs
    #open = codecs.open    # [1.4] log binary mode from stream, not text files

# [1.4] how spawned mergeall subproc's text is written and decoded here
STREAM_ENCODE = 'utf8'

# [1.6] display version number initially
VERSION = 3.1
print('mergeall %.1f' % VERSION)

# [3.0] user configs: logfile editor popup only (no GUI here)
try:
    from mergeall_configs import LOGEDITORPOPUP
except Exception as why:
    LOGEDITORPOPUP = True   # default: show a saved logfile in text editor too


################################################################################
# initial defaults: change here, or via user input (use C:\... for main drive);
# logfile names include '-yymmdd-hhmmss' to make unique and retain old versions
################################################################################


test = True
if test:
    # default to shipped test dirs
    frompath = 'test' + os.sep + 'test1'            # [3.0] portable to Win+Unix
    topath   = 'test' + os.sep + 'test2'
    try:
        # try Windows user's desktop
        logpath = r'C:\Users\%s\Desktop' % os.environ['username']
        assert os.path.exists(logpath)
    except:
        try:
            # [3.0] try same on Linux and Mac OS X
            logpath = os.path.join(os.environ['HOME'], 'Desktop')
            assert os.path.exists(logpath)
        except:
            logpath = '<none>'
else:
    # old testing code: now unused 
    frompath = r'D:\YOUR-STUFF'                     # e.g., sd card in win81 tablet
    topath   = r'E:\YOUR-STUFF'                     # e.g., terabyte backup drive
    logpath  = frompath + r'\admin\mergeall-logs'   # creates a diff if in from/to!

# cmd arg? => filename, having from/to/log defaults on separate lines
if len(sys.argv) > 1:
    defaults = open(sys.argv[1])
    frompath = defaults.readline().strip()     # assume okay, drop /n at end
    topath   = defaults.readline().strip() 
    logpath  = defaults.readline().strip()

datestamp   = time.strftime('date%y%m%d-time%H%M%S')
logfilepath = logpath + os.sep + 'mergeall-%s.txt' % (datestamp)


################################################################################
# interact to get settings
################################################################################


def yes(prompt, hint=' (y=yes): '):
    return input(prompt + hint).lower() in ['y', 'yes']

print('\nFROM path = "%s"' % frompath)
if not yes('use this?'):
    frompath = input('enter new FROM path: ')

print('\nTO path = "%s"' % topath)
if not yes('use this?'):
    topath = input('enter new TO path: ')

# script in same cwd here so no abs path needed, don't support -peek or -verify 
if yes('\nReport differences only?'):
    argmode = '-report'                         # report differences and stop
elif yes('Automatically resolve differences in TO (else asks)?'):
    argmode = '-auto'                           # run in-place updates to sync auto
else:
    argmode = ''                                # ask in console before each update

dolog = argmode and yes('\nSave output to log file too?')    # iff non-interactive
if dolog:
    print('Log file path = "%s"' % logfilepath)
    if not yes('use this?'):
       logfilepath = input('enter new Log file path: ')

# [2.0] new auto-backup option, applies to both -auto and manual changes here
dobkp = (argmode != '-report') and yes('\nBackup changes made in TO?')

# [2.4] quiet mode, omit per-file backup messages (show just one indicator)
if dobkp:
    doquiet = yes('Suppress per-file backup messages?')

# [3.0] skip system cruft files mode (all run modes)
# GUI's 3.0 "skip compare messages" moot here: console scroll is fast
docruft = yes('Skip system cruft files in both FROM and TO?')


################################################################################
# spawn mergeall, interact or capture output+errors
################################################################################

#-----------------------------------------------------------------------------
# TBD: interactive mode prompts issue (and cause for two spawn schemes below):
# subproc's stdin will inherit stdin here (the console) by default, but
# stream linebuffering in Python 3.X text mode may hide subproc's input()
# prompts till the next \n.  Binary mode streams can be unbuffered and may
# suffice for ascii prompts, but may fail for showing multibyte characters
# in Unicode filenames (if any are present in subject trees).  This seems
# to preclude catching stdout of interactive scripts in 3.X in general,
# and may be another Unicode "Catch22": input() prompts with no \n won't
# appear in intercepted subprocess streams until _after_ text is entered.
#
# Update:
# See also the "2.0 UPDATE" ahead.  Reading by bytes with unbufferred
# binary mode streams and stdout flushes works, but seems to preclude
# decoding Unicode to text for display -- individual bytes can't be decoded,
# there's no way to know when a non \n-terminated print string is complete,
# and eolns may be problematic, as their bytes may be part of other chars.
# stdin=sys.stdin is not needed: no-op, as descriptor inherited normally.
# Tools like PyExpect may not apply here: Python 3.X doesn't use C's IO lib. 
#-----------------------------------------------------------------------------


# verify: show settings, confirm run
argbkp = ' -backup' if dobkp else ''
if dobkp: argbkp += ' -quiet' if doquiet else ''   # [2.4]
argcruft = ' -skipcruft' if docruft else ''        # [3.0]

print('\nReady to run:')
print('\tcmd = "mergeall.py %s %s %s%s%s"' %
                 (frompath, topath, argmode, argbkp, argcruft))
print('\tlog = %s' %
                 ('"%s"' % logfilepath if dolog else '(none)'))

# not quite as descriptive as GUI, but suffices
if argmode in ['-auto', '']:
    print('\n*WARNING*: this may change your TO directory permanently and ')
    print('irrevocably, by adding, replacing, and deleting files and folders.\n')

if not yes('Proceed?'):                              
    input('Not run (press Enter to close)')   # keep console open on Windows
    sys.exit(0)


# [2.0] these would work in interactive mode, and could pass to mergeall in
# -auto mode because it doesn't start interactive help() for non-tty, but
# catch path here to avoid displaying command-line doc from mergeall;

if not os.path.exists(frompath):
    input('**Bad FROM path: run cancelled (press Enter to close)')
    sys.exit(1)
if not os.path.exists(topath):
    input('**Bad TO path: run cancelled (press Enter to close)')
    sys.exit(1)


#-----------------------------------------------------------------------------
# [1.2] make subproc's streams encoding match Popen expectation (Win=cp1252);
# could instead use utf8 here, if binary streams + manual utf8 line decode;
# required only if PYTHONIOENCODING set in shell (mine is) -- Popen ignores
# this and uses locale, and has no direct way to name stream encoding (why??);
#
# import locale
# os.environ['PYTHONIOENCODING'] = locale.getpreferredencoding(False)  # inherited
#
# [1.4] Unicode stream encoding, take 2: need to use UTF8 for prints in mergeall
# subproc, and binary mode Popen reads + manual decoding here; Popen's locale
# encoding works for reading the stream, but not for prints within mergeall;
#-----------------------------------------------------------------------------

os.environ['PYTHONIOENCODING'] = STREAM_ENCODE      # inherited (moot in py3.6?)


#-----------------------------------------------------------------------------
# INTERACTIVE MODE SPAWN (not [-auto or -report]):
#
# no log, run in same console so tty streams are shared (else prompts can be
# problematic);  file path error prompts from mergeall work correctly in this
# mode, but pre-check to avoid displaying mergeall's command-line help [2.0];
#-----------------------------------------------------------------------------

# [3.0] data+scripts not in os.getcwd() if run from a cmdline elsewhere,
# and __file__ may not work if running as a frozen PyInstaller executable;
# use __file__ of this file for Mac apps, not module: it's in a zipfile;

launcherpath = fixfrozenpaths.fetchMyInstallDir(__file__)   # absolute

# [3.0] allow for frozen executables
if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
    # pyinstaller exe [3.0]
    freezename = 'mergeall.exe' if RunningOnWindows else 'mergeall'
    mergeallpath = os.path.join(launcherpath, freezename)
    mergeallspwn = [mergeallpath]
    cmdpath = mergeallpath
else:
    # py2app Mac app or source (original code)
    mergeallpath = os.path.join(launcherpath, 'mergeall.py')
    mergeallspwn = ['python', mergeallpath]
    cmdpath = sys.executable

if argmode == '':
    # former caveat: script not in os.getcwd() if run elsewhere (see gui)
    # assume args do not need to be manually quoted in the cmd sequence
    cmdseq = mergeallspwn + [frompath, topath]
    if dobkp:
        cmdseq += ['-backup']                 # [2.0] for interactive changes too
        if doquiet:
            cmdseq += ['-quiet']              # [2.4] ditto, but only if -backup
    if docruft:
        cmdseq += ['-skipcruft']              # [3.0] for '', -report, or -auto
    os.spawnv(os.P_WAIT, cmdpath, cmdseq)     # interact in this console
    input('Done (press Enter to close)')      # keep console open on Windows
    sys.exit(0) 


#-----------------------------------------------------------------------------
# NON-INTERACTIVE MODE SPAWN (-auto or -report):
#
# run command-line in separate process, read/show/save output;  requires more
# control over streams here than 3.X's os.popen/spawnv provide;  uses python
# -u so sub's stdout stream is unbufferred, and hence not delayed;  other
# Popen ideas explored...
#     universal_newlines=True,     # [1.2] text mode streams, auto decode
#     stdin=sys.stdin)             # provide sub's stdin here?: inherited
#
# [1.4] change: drop -u here, as it makes eolns \n in 2.X but \r\n in 3.X;
# UPDATE: '-u' unbuffered flag reinstated, else 10+ second output delay
# for some devices; this also requires linebreak mapping to handle the
# 2.X/3.X difference; see GUI launcher's 1.4 change log for more details.
#
# [2.0] UPDATE note: this spawning mode _does_ support interactive prompts,
# if stdout is unbuffered and binary, output is read by bytes instead of
# lines, and this process's own stdout is flushed after each character:
#
# while True:
#     byte = subproc.stdout.read(1)       
#     if not byte: break
#     sys.stdout.write(byte.decode())     # but to which scheme?
#     sys.stdout.flush()
#
# However, it's not clear that this can support multi-byte Unicode filename
# chracters in the output (what would the console do with their individual
# bytes?), and this may make it difficult to normalize 2.X/3.X endline
# characters, as their raw undecoded bytes may be part of another multibyte
# Unicode character.  Reading by bytes is also slower, though perhaps not
# significantly so to an interactive user.  Keep two spawn schemes for now.
#-----------------------------------------------------------------------------

# allow non-ascii filenames in my log file text: write chars as utf8:
# logfile = open(logfilepath, 'w', encoding=STREAM_ENCODE)
# [1.4] use binary mode from stream: 2.X codecs.open doesn't expand \n;

if dolog:
    try:
        logfile = open(logfilepath, 'wb')
    except:
        # [2.0] not exception text
        input('**Bad log-file path: run cancelled (press Enter to close)')
        sys.exit(1)

# former caveat: script not in os.getcwd() if run elsewhere (see gui)
extras = {}
if hasattr(sys, 'frozen') and (RunningOnWindows or RunningOnLinux):
    # pyinstaller exe [3.0]
    cmdseq = [mergeallpath, frompath, topath]
    if RunningOnWindows:
        # else spawn hangs unless launcher uses --console (with popup!)
        extras = dict(stdin=subprocess.DEVNULL)
else:
    # py2app Mac app or source (original code)
    cmdseq = [sys.executable, '-u', mergeallpath, frompath, topath]    # [1.4] need '-u'

if argmode:
    cmdseq.append(argmode)       # else fails if empty and not special-cased above (but is)
if dobkp:
    cmdseq.append('-backup')     # [2.0] not added for -report (but harmless if is)
if dobkp and doquiet:
    cmdseq.append('-quiet')      # [2.4] not added (or asked) unless -backup
if docruft:
    cmdseq.append('-skipcruft')  # [3.0] added (and asked) for both -report and -auto


# [1.5] shell should be True on Windows so that it uses filename associations,
# but False on Linux so that it doesn't just start a python" interactive shell;
# uses a command sequence (not string): args are auto-quoted by subprocess;
doshell = sys.platform.startswith('win') 

subproc = subprocess.Popen(
              cmdseq,                     # a string cmd may fail on Unix
              shell=doshell,              # [1.5] see note above, platform specific
              universal_newlines=False,   # [1.4] binary mode, manual decode/eoln
              stdout=subprocess.PIPE,     # capture sub's stdout here
              stderr=subprocess.STDOUT,   # route sub's stderr to its stdout
              **extras)

# read sub's output
# no need to thread this here (this is not a GUI: okay to block)

for binline in subproc.stdout:            # read stdout+stderr lines
    try:
        line = binline.decode(STREAM_ENCODE)       # [1.4] manual decode here, match subproc
    except UnicodeDecodeError:
        line = b'(UNDECODABLE LINE): ' + binline   # [1.6] 2.X fix--see details in GUI launcher
    print(line.rstrip())                           # scroll to console (assume can handle)
    
    if dolog:                                      # also save to log file; [1.4]: binary
        eoln = os.linesep.encode()                 # must be bytes in 3.X (no-op in 2.X)
        binline = binline.replace(b'\r\n', b'\n')  # [1.4]: got just \n from '-u' in 2.X only
        binline = binline.replace(b'\n', eoln)     # replaces are no-op in 3.X and unix 
        logfile.write(binline)

# mergeall exited: close/show log file if logging
if dolog:
    logfile.close()
    if LOGEDITORPOPUP:
        # [3.0] Mac OS X is pickier about file URLs
        if sys.platform.startswith('darwin'):
            logfilepath = 'file:' + os.path.abspath(logfilepath)
        webbrowser.open(logfilepath)   # popup, uses start=Notepad on Windows
    else:
        print('See log file in logs folder.')

input('Done (press Enter to close)')   # keep console open on Windows till Enter
