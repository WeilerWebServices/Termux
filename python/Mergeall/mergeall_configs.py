"""
================================================================================
mergeall_configs.py:
  user configurable settings (part of the mergeall system)

Edit this file to customize GUI appearance and various behavior options.
This file contains settings that are unlikely to vary per mergeall run.
Other per-run options are set in the GUI or command-line arguments.
Names here that are used by mergeall and others are all uppercase.

NOTE: Be careful with edits here.  mergeall and its launchers will generally
ignore errors in this file and fall back on using all defaults, but such errors
are reported on the console only (if there is one).  It's recommended to import
this file to check for errors, and retain a copy of its shipped version.
================================================================================
"""
import sys   # e.g., if sys.platform.startswith(('win', 'darwin', 'linux'))

# for platform-specific choices
RunningOnMac     = sys.platform.startswith('darwin')       # all OS (X)
RunningOnWindows = sys.platform.startswith('win')          # all Windows
RunningOnLinux   = sys.platform.startswith('linux')        # all Linux



#===============================================================================
# [2.2] BACKUPS LIMIT: keep up to this many backup folders in each archive
# copy's __bkp__ folder; after this limit is reached, backups are pruned
# by age, oldest first.  The value means # runs with backups enabled.
# Only changed items are stored in backups, so backups are normally small,
# and backup folders are created only if a run produces items to record.
#===============================================================================

MAXBACKUPS = 25         # was 10, then 15 (uses very little space in practice)



#===============================================================================
# [3.0] TEXT AREA HEIGHT: initial height (in number lines) of the scrolled
# mergeall messages area of the GUI.  This can still grow/shrink later with
# the mergeall window: it has top priority for resizing when the user resizes
# the window.  Setting this to None uses Tk's default, which is 24 lines.
#===============================================================================

if RunningOnMac:
    TEXTAREAHEIGHT = 25                       # use more screen space on Mac
else:
    TEXTAREAHEIGHT = 18                       # formerly used Tk's default 24



#===============================================================================
# [3.0] TEXT AREA WIDTH: initial width (in number characters) of the scrolled
# mergeall messages area of the GUI.  This can still grow/shrink later with the
# mergeall window: it has top priority for resizing on user resize actions.
# Making this larger also expands the control-widget area above the text area. 
# Setting this to None uses Tk's default, which is 80 characters, with wrapping.
# View the output in your popup text editor after the run for richer options.
#===============================================================================

if RunningOnMac:
    TEXTAREAWIDTH = 110                       # control fonts larger on Mac
elif RunningOnWindows:
    TEXTAREAWIDTH = 90                        # default seems narrow on Windows
elif RunningOnLinux:
    TEXTAREAWIDTH = 100                       # None = use Tk's default 80



#===============================================================================
# [3.0] TEXT AREA FONT: font of scrolled messages text in GUI, None=Tk default.
# For custom fonts, use a tuple ('family', size, 'style style...'), where
# style is any mix of 'normal' or 'bold', 'italic' or 'roman', 'underline',
# etc., and both size and style can be omitted but size must appear second.
# The default style is 'normal' and 'roman'.  Size may be positive for points
# and negative for pixels, and defaults to 0 if omitted (the font's default).
# A 'family size style style...' string works for fonts too if the family name
# has no spaces, else use the tuple form (e.g., for family 'courier new').
#===============================================================================

# per platform?
if RunningOnMac:                             # special-case fonts for Mac OS X
    textfont = ('menlo', 11, 'normal')       # a nice Mac monospace (or monaco)  

elif RunningOnWindows:                       # output font - monospace is best
    textfont = ('consolas', 11, 'normal')    # consolas isn't monospace on Linux

elif RunningOnLinux:                         # inconsolata isn't mono on Windows
    textfont = ('inconsolata', 9, 'normal')  # courier works on all, but duller

TEXTAREAFONT = textfont    # None = use Tk default for platform



#===============================================================================
# [3.0] TEXT AREA COLOR: color(s) of scrolled messages text in GUI.  This is
# especially useful on the Mac, where both controls and text area are white by
# default: color sets it off better than a border.  A string means background
# only (foreground is black); a tuple means (background, foreground); and None
# uses Tk default for platform.  Each color is either a color-name or "#RRGGBB"
# hex-value string.  Use light colors if background only (e.g., wheat, ivory).
# See docetc/Tools/pickcolor.py for a simple #RRGGBB color-string chooser GUI.
# Caveat: color can vary by platform and machine, and YMMV; set as you prefer.
#===============================================================================

# per platform?
if RunningOnMac:                             # default=all white  
    textcolor = '#ededed'                    # use a light grey to offset

elif RunningOnWindows:                       # defaults: ctrls=grey, text=white
    textcolor = None                         # use the default unchanged
    
elif RunningOnLinux:                         # Linux: default is okay too
    textcolor = ('#000050', 'white')         # try custom (darkblue, white)

# "factory" setting: darkblue/white seems portable to all three
TEXTAREACOLOR = ('#000050', 'white') 



#===============================================================================
# [3.0] DEFAULT LOG-FILES FOLDER: where mergeall stores its log files, when
# they are enabled in the GUI.  If set to None (or set to an invalid pathname),
# this folder defaults to the user's Desktop, wherever that is located on the
# underlying platform.  Else, set this to the pathname of the folder where
# you want logs to appear (e.g., '/Admin-Mergeall', r'C:\Admin-Mergeall\Logs').
#
# This setting gives an initial choice only: regardless of its value, you can
# always Browse to a different folder in the GUI for any run.  Log files have
# names that give their creation date and time, and make them unique in a
# folder.  Note that merges might run slower if you save log files on the same
# external flash drive that is being updated (i.e., on mergeall TO's drive).
#===============================================================================

DEFAULTLOGDIR = None    # None=Desktop, else folder path (r'C:\Admin-Mergeall', ')



#===============================================================================
# [3.0] LOG-FILE EDITOR POPUP: if True, automatically open the log file used to
# save mergeall messages in a local text editor, when the mergeall run finishes.  
#
#   UPDATE: in the GUI launcher, the log-file popup can now be toggled on and
#   off per run in the GUI itself, and the setting here is used only as initial 
#   value for the toggle (it saves a single click if the toggle's default isn't 
#   to your liking).  However, this setting is still applied in the lesser-used 
#   console launcher as described by text below, which also provides context.
#
# The popup typically opens Notepad on Windows, TextEdit on Mac, and gedit on 
# Linux (it may also open the portable PyEdit, if you've associate it with text
# files).  The setting here works for both the GUI and console launchers, but 
# applies only when the user has elected to save messages to a log file in the 
# launcher.  Log-file saves are made regardless of this popup viewer setting.
#
# The editor popup is optional, because mergeall's messages are always viewable
# in the scrollable text area of the GUI launcher (and the console launcher's
# screen).  On the other hand, logs can be large for large trees, the GUI's
# display lacks the search tools of a full-blown text editor, and navigating to
# the log dir manually after runs can be tedious.  The editor popup has always
# been available; disabling it here was added in [3.0].  This _may_ be a per-run
# choice, but it didn't seem to merit another toggle in the already-busy GUI;
# more likely, users will either want the pop-up or not, for all their runs.
#===============================================================================

LOGEDITORPOPUP = True    # True=toggle on: show log file in a text editor too?



#===============================================================================
# [3.0] MAC SLIDE-DOWN DIALOGS: On Mac OS X (only), set to True to display
# folder browse dialogs as slide-down sheets instead of windows-y modal popups.
#===============================================================================

MACSLIDEDOWN = True      # if False, use popup window instead of sheet (YMMV)




#===============================================================================
# **NOTE** the rest of this file is advanced cruft filename patterns, which
# you probably don't want to modify unless you're sure about your changes.
#===============================================================================



#-------------------------------------------------------------------------------
# [3.0] CRUFT FILENAME PATTERNS:
#
# --See skipcruft.py for the code that uses the patterns defined here--
#
# The following settings are used by mergeall, diffall, and cpall for their
# "-skipcruft" modes (including cpall's copytree(), called from mergeall).
# When this argument is used in diffall or mergeall's "-report" mode, cruft
# (a.k.a. metadata) files will not register as differences.  When used in
# mergeall's "-auto" automatic (or "" selective) updates mode, cruft files:
#
#    -Are not copied from the FROM folder to TO, if absent in TO
#    -Are not deleted from the TO folder, if absent in FROM
#    -Are not replaced in the TO folder, if different in FROM
#
# In other words, cruft files are ignored if they have been newly added,
# removed, or changed in FROM since the last run.  They will not be copied
# to, deleted from, or replaced in TO.
#
# This both allows platform-specific files to remain on the creating platform,
# and prevents them from being propagated to other copies or computers.  In
# cpall, "-skipcruft" has the same role as for mergeall's FROM: cruft in the
# source is not copied to the destination.
#
# This an alternative to running the nuke-cruft-files.py script before
# or after a merge, or any other time a brute-force cleanup is in order.
# See that file for more background; Mac was initial motivation for this
# mode, but the patterns here also rule out other platform's cruft, as well
# as other files that vary per platform (e.g., Python bytecode: see ahead).
#
# HOW CRUFT-SKIPPING WORKS - MERGEALL EXAMPLES:
#
# The following narrates representative mergeall "-skipcruft" run results.
# In this, "[..] -> [..]" denotes mergeall FROM -> TO folders (roles assumed
# by a Drive1 and Drive2 here) and "=> [..]" gives the resulting TO folder.
# 
# 1) [A, B, C] -> [A, D] => [A, C]
#
#    If Drive1 has files [A, B, C] and Drive2 has files [A, D]
#        where on Drive1: B is cruft, A has changed, C is new, and D removed
#    Then a merge from Drive1 to Drive2 leaves Drive2 with files [A, C]
#        after skipping cruft B on Drive1, replacing common A on Drive2,
#        copying unique C to Drive2, and removing unique D from Drive2.
#    *Drive1's cruft B is skipped in FROM and not copied.
#
# 2) [A, C] -> [A, B, C] => [A, B, C]
#
#    Later merging from Drive2 [A, C] back to Drive1 [A, B, C] skips and
#    retains Drive1 cruft B, leaving it [A, B, C] with the latest A and C.
#    *Drive1's cruft B is skipped in TO and not removed.
#
# 3) [A, D, E] -> [A, B, C] => [A, B, D]
#
#    If Drive2 later changes to [A, D, E] where E is its own cruft file, and
#    Drive1 is still [A, B, C], then a merge from Drive2 to Drive1 makes
#    Drive1 [A, B, D], after skipping crufts E in Drive2 and B in Drive1,
#    pruning unique C, copying unique D, and synchronizing common A.
#    *Drive2's cruft E is skipped in FROM and not copied.
#    *Drive1'a cruft B is skipped in TO and not removed.
#
# In all 3 cases, the two drives are the same after the mergeall, except for
# their own unique cruft files.
#
# If "-skipcruft" was NOT used in the examples above, all cruft files would
# be treated like any other file - they would be copied to TO in #1, deleted
# from TO in #2, and both copied to and deleted from TO in #3:
#
# 1) [A, B, C] -> [A, D] => [A, B, C]
# 2) [A, C] -> [A, B, C] => [A, C]
# 3) [A, D, E] -> [A, B, C] => [A, D, E]
# 
# IN MORE CONCRETE TERMS:
#
# This allows Mac to retain its cruft files and Windows drives to omit them,
# and vice versa.  In particular, intermediate drives (e.g., USB or network
# drives) won't receive any cruft files when used as TO, and also won't cause
# them to be deleted on target computers (e.g., Macs) by omission when later
# used as FROM.  The net effect: what belongs only on Mac and Windows will
# stay only on Mac and Windows.  This option can also be used to keep other
# platform-specific items out of archive copies, including Python bytecode.  
#
# HOW TO CODE PATTERNS:
#
# Use filename patterns here compatible with Python's fnmatch module:
#    https://docs.python.org/3/library/fnmatch.html
#
# Patterns are configurable here, because the set shipped may be incomplete
# or overly-aggressive for some use cases; tweak as desired.  diffall also
# uses these settings to skip cruft files so they don't expand its report,
# and cpall uses them to avoid copying cruft much like some file explorers.
# Changes here are picked up by all these programs automatically.
#
# CASE SENSITIVITY:
#
# By default, cruft pattern matching is always case-insensitive ("Desktop.ini"
# matches "desktop.ini") on all platforms, unless you set CRUFTCASENEUTRAL
# below to False - in which case matches are case-insensitive on Windows, but
# not on Mac or Linux.  While case normally matters on Unix systems, they
# still need to detect varying-case Windows cruft, and it's unlikely that
# Unix cruft is not cruft if its case differs (a ".Trash" by any other case
# is probably still just garbage).  If this is ever problematic, use False
# and code your Windows patterns to cover all valid cases ("[dD]esktop.ini").
#
# NOTES AND OPEN ISSUES:
#
# 1) EFFICIENCY: Some patterns here may subsume others, making the others
#    pointless matches (this is not checked or optimized away, but see #2).
#    As is, cruft-skipping adds just 2-3 seconds to mergeall's comparison
#    for very large archives (87G and 58k-files compare in 11 secs versus 8).
#
# 2) GENERALITY: Would it be better to just skip all ".*" files than look for
#    specific names here?  They're treated as hidden on Unix, but not always.
#    Enable the ".*" pattern below if this proves to be a valid scheme.
#
#    UPDATE: as shipped, ".*" is now used below instead of specific "." names,
#    because the list of dot files was beginning to grow too long to manage.
#    A single ".*" also matches quicker than a list of dot-prefixed names.
#    Change the 'mac_cruft' list setting below for your use cases if required,
#    or add valid dot files to the KEEP list to treat them as normal items.
#    Note that ".*" includes "._*" AppleDouble resource-fork companion files
#    that appear on non-Mac filesystem drives only, but can accumulate fast.
#
# 3) OTHER CRUFT: Python ".pyc"/".pyo" bytecode files were added to the crufts
#    list preset because they vary per platform and always trigger differences.
#    Moreover, because bytecode is platform-specific, copying across machines
#    means it has to be recreated after each copy - a minor but unnecessary
#    performance hit.  Omitting bytecode from archive copies is harmless,
#    because it is regenerated automatically on each platform as needed.
#    The preset default here omits bytecode files both in FROM (so they are
#    not copied) and in TO (so they are not removed).  Extend this as needed.
#    
#    An argument could be made for also skipping platform-specific executables
#    and binaries as cruft (e.g., ".exe", ".o"), but they are not automatically
#    regenerated, and some may be desirable to keep in archives (e.g., utility
#    programs).  In general, "-skipcruft" is intended for items that _both_
#    vary per platform and are undesirable in cross-platform content copies.
#-------------------------------------------------------------------------------


# Case-insensitive matching means that "Desktop.ini" matches "desktop.ini".
# If True, cruft pattern matching is case-insensitive everywhere (Unix too).
# If False, it is case-insensitive on Windows only (and not on Mac or Linux).

CRUFTCASENEUTRAL = True  # True=case-insensitive matching, on all platforms


# Mac files+folder (for filesystem diffs, some are valid to retain for Mac use)

mac_cruft = [
    '.DS_Store',         # pervasive! - directory services, Finder view options
    '._.DS_Store',       # these appear occasionally too (non-Mac drives)
    '.localized',        # tells apps to display a folder's "localized" name 
    '.TemporaryItems',   # temporary data for filesystem moves/copies/etc
    '.Trashes',          # delete retention, if not disabled (root only?)
    '.Trash',            # ditto
    '.Spotlight-V100',   # spotlight indexing, if not disabled (root only?)
    '.fseventsd',        # file system events demon, if not disabled (root?)
    '.VolumeIcon.icns',  # for custom volume icons (supposedly)
    '.apDisk',           # shared folder information, not required
    '.iTunes*',          # assorted itunes metadata files (or retain on KEEP)
    '.com.apple.*',      # various uses: timemachine, etc (root only?)
    '._*'                # AppleDouble resource-fork companions, non-Mac drives:
    ]                    # ._* files, ._.* files, Office, text, images, etc.

# -OR- use this: '.*' is faster and may catch more, but may be too aggressive?
mac_cruft = [
    '.*'                 # use to treat all names with leading "." as cruft,
    ]                    # except for those matched by the KEEP list below


# Windows files+folder (not nearly as pervasive as Mac, but still proprietary)

windows_cruft = [
    'Thumbs.db',         # thumbnail cache to skip recreation
    'Desktop.ini',       # custom folder view settings, if any (= Mac .DS_Store)
    '$Recycle.bin',      # delete retention (= Mac .Trash)
    'System Volume *',   # system restore tool information
    'RECYCLER',          # same as $Recycle.bin, for NTFS
    '~*'                 # catchall for temporary Office save files 
    ]


# Linux files+folder (not much on this platform so far: expand as desired)

linux_cruft = [ 
    '.Trash-1000'        # delete retention (similar to Mac, Windows)
    ]


# Other platform-specific files+folders that should remain where created only

other_cruft = [
    '*.py[co]',          # python bytecode files: per-platform, auto-created
    ]                    # alternative: add '__pycache__' for python 3.2+


# ALWAYS SKIP THESE - unless also matched by an item in CRUFT_KEEP.
# These will not be copied from FROM or removed in TO (new adds or deletes).
# Could select by run's sys.platform, but that would be less flexible.

CRUFT_SKIP = mac_cruft + windows_cruft + linux_cruft + other_cruft    


# NEVER SKIP THESE - even if matched by the skip list: valid .* data files.
# These will always be copied from FROM and deleted in TO (on adds and removes).
# Currently, this list's names apply only if the ".*" cruft pattern is enabled.

CRUFT_KEEP = [
    '.htaccess*',        # apache website config files
    '.login',            # unix login settings, but unlikely in an archive?
    '.bash*',            # ditto, but for the bash shell (linux, mac)
    '.profile',          # various uses
    '.svn'               # source control system storage, unlikely in archive?
    ]                    # edit and expand me, if using the ".*" factory preset



# [end settings]
