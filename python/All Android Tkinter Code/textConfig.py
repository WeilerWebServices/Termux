"""
===================================================================================
textConfig.py: PyEdit (textEditor.py) configuration module.

#----------------------------------------------------------------------------------
# ANDROID version, Jan-Mar 2019 (see "# ANDROID" for changes)
#
# Recent changes:
# [Mar2819]: New start-folder setting for Android file-chooser dialog.
# [Feb2019]: Clarify Android tkinter font family and style constraints.
#---------------------------------------------------------------------------------- 

Edit the Python variable assignments below to customize PyEdit's appearance
and behavior for your preferences.  These settings are applied at startup
time; some can also be modified in the GUI itself (e.g., fonts and colors).

Color and font settings:

For colors:
  Use either a color-name string that Tk understands (e.g., 'navy'), or an
  RGB-value hex string (e.g., '#0000FF').  You can get custom RGB strings
  from the tools/pickcolor.py script, and PyEdit's Info dialog also reports
  colors you've set in the GUI itself.  Both can be used for cut-and-paste here.

For fonts:
  Use a 3-item tuple giving font family, size, and style (for example,
  ('menlo', 13, 'normal')).  The style part is a space-separated list that may
  include 'normal' or 'bold', and 'italic' or 'roman', and an omitted style 
  defaults to 'normal'.  Size may be positive for points, negative for pixels,
  or 0 for a default size, and omitting size is the same as 0 (the default).
  
  A string 'family size style...' also works if the family name has no spaces,
  but you can never omit size unless you also omit style (their order matters).
  See the Pick Font dialog's in-program help for more pointers.

Use in standalone and embedded roles:

This module is imported normally via the module search path.  Although the
version here is loaded and used when PyEdit is run standalone, this module
can also be redefined locally per client program, by creating a file of the
same name in the program's '.' home folder.  PyMailGUI, for example, embeds
PyEdit and provides its own version of textConfig.py that overrides this.

When redefined this way, the local file fully replaces this file - its settings
do not augment those here, unless that other file also imports the names here
(e.g., via "from *").  If a name is not set in the sole textConfig.py imported
(here or elsewhere), that name's in-program default is used.  If this module
is not on the search path at all, it will be skipped altogether, and all
names' in-program defaults will be applied.

More details:

1) As noted, all names here have presets in the program that are used if not
set in the sole textConfig.py file imported.  So, for example, if you don't
set color and font lists either here or in a client program's local version
of this file, the program code's presets will be used.

2) Exception: for ease of use (and because they're crucial), PyEdit's Unicode
behavior settings always come from this file, _not_ a client program's local
textConfig.py.  These are complex enough that they seem best set once here,
for all PyEdit roles.  See the end of this file for Unicode settings.

3) Caution: PyEdit is not currently forgiving about errors here.  Please edit
with care, and verify your changes before relying on them (e.g., import or
run this file to check for syntax; PyEdit's Run Code can be used for this).
Some errors may silently fail if you have no console window, and may even hang
the GUI (this is a to-be-improved, but low priority).
===================================================================================
"""

import sys   # for checking platform, version, etc.

# For platform-specific choices
RunningOnMac     = sys.platform.startswith('darwin')       # all OS (X)
RunningOnWindows = sys.platform.startswith('win')          # all Windows
RunningOnLinux   = sys.platform.startswith('linux')        # all Linux



#==================================================================================
# Basic Configurations: Initial Font, Color, Size
#
# Comment-out any setting in this section to accept Tk or program defaults.
# All of these are used for initial configuration only: you can change font
# and colors from GUI menus and resize the window interactively at any time.
#
# See also the font and color lists ahead for mutiple-choice options that can
# be cycled through on demand (and automatically for colors); the Run-Code
# font and color settings below for output-window settings; and the toolbar
# font settings up next for configuring controls.
#
# [3.0] The insertion cursor is now also set to the same color as foreground
# (fg) text, so its default black doesn't get lost in a dark background (bg).
# This does not require any additional settings in this file.
#==================================================================================

# ANDROID - disabled due to font crashes, preset below (but experiment as desired)
"""
# Initial main-text font                 # ('family', size, 'style...'?)
font = ('courier', 12, 'bold')           # default for all platforms

# Customize per platform?
if RunningOnMac:                         # specialize, else tiny [3.0]
    font = ('menlo', 13, 'normal')       # also mono on Mac: monaco, courier/15

elif RunningOnWindows:                   # size was 9, then 12
    font = ('consolas', 13, 'normal')    # also mono on Windows: courier (new)

elif RunningOnLinux:                     # if differs from default
    font = ('inconsolata', 11, 'normal') # also mono on Linux: 'courier new'
"""

# Initial background/foreground colors   # default=colorlist[0] (see ahead)
bg = 'beige'                             # colorname or #RRGGBB hexstr
fg = 'black'                             # e.g., 'powder blue', '#690f96'


# Initial text-area size: lines, chars
if RunningOnMac:
    height = 34                          # Use the space on Macs (not 35...)
    width  = 90                          # can resize after open arbitrarily  

elif RunningOnWindows:
    height = 28                          # Tk default=24 lines (if not set)
    width  = 90                          # Tk default=80 characters (if not set)

elif RunningOnLinux:
    height = 30                          # toolbar now uses smaller labels
    width  = 90                          # no need to make wider to accommodate

# ANDROID - smaller/safe font and sizes (fonts: courier, helvetica, or times)
font = ('courier', 8, 'normal')
height = 10
width = 15



#==================================================================================
# ANDROID [Mar2819]: starting folder for Open and Save file-chooser dialogs.
#
# Choose and edit one of the options below; the last setting wins.  Respectively,
# the options illustrated by the example settings below refer to:
#
# - Internal storage
# - Removable media (whose xs mean the drive's ID)
# - The default, selected by None
#
# The default for None is the "/storage/emulated/0" internal-storage root, which
# is the same as "/sdcard" except that it allows navigating up to a removable 
# drive (though the trip is unfortunately one way in Android Tk's file dialog).  
# If the setting does not work, dialogs start at Pydroid 3's app-private $HOME 
# folder in "/data/data".
#
# Later dialog opens still pick up from the last folder you selected as before,
# but this setting avoids a tedious initial navigation up and down to your possibly
# nested content folder, from the nested app-private folder of the Pydroid 3 app.
#==================================================================================

filechooserstart = '/sdcard/MY-STUFF'
filechooserstart = '/storage/xxxx-xxxx/Android/data/ru.iiec.pydroid3/MY-STUFF'
filechooserstart = None



#==================================================================================
# [3.0] Toolbar: layout and font
#
# Choose a font for the quick-access buttons at the bottom of edit windows.
# These are redundant with menus and their accelerator-key combos, but may 
# be useless nonetheless, especially if your input is limited on a tablet.
#
# You can also now choose a fixed toolbar-layout scheme (so buttons are always
# in the same position) or a variable scheme where space between button groups
# grows and shrinks with the window.  The latter keeps more on screen (default).
#==================================================================================


# Font for button row at bottom
toolbarFont = None                            # None = system default font
                                              # or ('family', size, 'style...'?)

# ANDROID - disabled due to font crashes (but experiment as desired)
"""
# Customize per platform?
if RunningOnMac:
    toolbarFont = ('tahoma', 12, 'normal')    # or None, monaco, menlo, courier

elif RunningOnWindows:
    toolbarFont = ('consolas', 9, 'bold')     # or tahoma, 'segoe ui', arial

elif RunningOnLinux:
    toolbarFont = ('inconsolata', 10)         # now labels (buttons render hugely)
"""

# Spacers in toolbar do not expand?           # True=buttons stay in same place
toolbarFixedLayout = False                    # False=spacers expand with window



#==================================================================================
# [3.0] Run Code: Font and Color
#
# If not None, the following font setting is used only for output text in 
# the window displayed for Run-Code's Capture mode.  The default font is a
# reasonable fixed-width, so this is optional.  See above for example fonts.
#
# The code's output-text color can be configured here too, but it is not by
# default - its lack of color suffices to make it distinct from edit windows.
# But your mileage may vary: a unique color scheme may work well here.
#==================================================================================


# Output font for all platforms
runcodefont = None                              # a font, or None=system default

# ANDROID - disabled due to font crashes (but experiment as desired)
"""
# Customize per platform?
if RunningOnMac:                                # or menlo for tighter lines?
    runcodefont = ('monaco', 12, 'normal')      # default=monaco 11 normal

elif RunningOnWindows:                          # or courier, other?
    runcodefont = ('consolas', 12, 'normal')    # default=courier 10 normal

elif RunningOnLinux:                            # or same as Windows?
    runcodefont = ('inconsolata', 11, 'normal') # consolas not mono on Linux
"""

# Color of code output: background/foreground 
runcodebg = None   # or 'black'?                # None = white/black default
runcodefg = None   # or 'green2'?               # else color 'name' or '#RRGGBB'



#==================================================================================
# Find (Simple Version) is Case-Insensitive? [Legacy Switch]
#
# [3.0] Note: the case-insensitivity ('a'='A') setting applies to Find searches
# within a single window's text, but not to Grep searches in external files.
# This makes Grep more specific in order to minimize the number of matches.
#
# [3.0] This is now for the simple Find dialog (and its accelerators) only.
# Both the Change (find/change) and Grep (external files search) dialogs
# now have GUI toggles to select case, which start as case-insensitive.
#==================================================================================


# Find is case insensitive?
caseinsens = True                        # default=1/True (on) if not set



#==================================================================================
# [3.0] Color and Font Lists
#
# Set the following two names to the types of values shown to override preset
# color and font lists that are cycled through when the GUI's menu options
# "Tools->Font List" (F1) and "Tools->Color List" (F3) are selected - the next
# item in the list is always applied.  The toolbar's "Color" and "Font" buttons
# cycle through these choices too, and the colorlist setting here will also be
# used automatically by the color-cycling feature described in the next section.
#
# You can list any number of items in each of the lists below, per syntax shown.
# For colors, fg=foreground and bg=background, and settings may be Tk color
# names or '#RRGGBB' hex-value strings (see tools/pickcolor.py for the latter).
# If you also set "bg" and "fg" above, they will be used for the first window.
#
# These settings are mostly a convenience.  While you can always select fonts
# and colors in the GUI's Tools menu at the start of each session, the lists
# here are a more permanent way to access your favorite font and color choices.
# If they are not set here (or in a client program's local textConfig.py file),
# both lists default to their in-program presets in code (in textEditor.py).
#==================================================================================


# _Not_ setting these means you'll use the presets assigned in the program.
# Remove the """ quotes above and below and edit to enable these overrides.
# ANDROID: courier, helvetica/arial, or times fonts only (courier: no italic/bold). 


"""
colorlist = [dict(fg='black',   bg='beige'),      # or {'fg': xxx, 'bg': yyy}
             dict(fg='green2',  bg='black'),      # color name or #RRGGBB hex
             dict(fg='white',   bg='#173166'),    # as many as you wish
             dict(fg='#00ffff', bg='#3b3b3b')     # picks next each time
             ]

fontlist = [('courier',  11, 'normal'),           # ('family', size, 'style...')
            ('arial',    12, 'bold italic'),      # as many as you wish
            ('times',    18, 'bold'),             # picks next each time
            ('consolas', 13, 'normal'),           # Win (inconsolata on Linux)
            ('monaco',   14, 'normal')            # Mac (also fixed: 'menlo')
            ]
"""



#==================================================================================
# [3.0] Automatic Color Cycling
#
# If the following variable is True, PyEdit automatically sets the foreground
# and background color of each new edit window after the first to the next
# color in the color list.
#
# The color list is the "colorlist" setting (or its preset default) described
# in the preceding section.  Its colors can be applied manually by the Tools
# Menu's Color List (F3) menu option.  The setting here, if True, applies the
# list's colors to windows automatically when they are opened, to make each
# distinct in a session.  For example, each new Popup window opened and Grep
# match clicked will display a different color scheme from the list.  On Mac,
# each click to the app or its Dock entry when already open does likewise.
#
# Note that this setting applies both to top-level (popup) windows that are
# opened by Popup (Cmd/Ctrl-p), Clone, and other programs, and to embedded
# component windows of the sort used in PyMailGUI View/Write windows; disable
# it in a client program's textConfig.py if this proves too distracting.  In
# PyMailGUI, for example, fixed per-account color schemes may be preferred.
#==================================================================================


colorCycling = True      # True=next color for each window, False=disabled



#==================================================================================
# [3.0] Grep Search: Matches List Font and Spawn Mode
#
# The font here is used in the Grep-matches selection list.  A None invokes
# the platform default, which may be too small from some users on some Windows.
#
# You can also define the spawn mode for Grep; change this to an alternative
# if the Grep option in Tools crashes.  You'll generally want to leave this as
# is.  The preset attempts to workaround a thread bug in Python 3.5/Tk 8.6,
# and has significant performance advantages.  It's available here jst in case
# the preset is problematic on a given platform (or threading's story improves).
#==================================================================================


# Matches-list font
grepMatchesFont = None     # None=default, or ('family', size, 'style...'?)

# ANDROID - disabled due to font crashes (but experiment as desired)
"""
# Customize per platform?
if RunningOnMac:
    grepMatchesFont = None  # default is nice

elif RunningOnWindows:
    grepMatchesFont = ('consolas', 12, 'normal')      # else too small

elif RunningOnLinux:
    grepMatchesFont = ('inconsolata', 10, 'normal')   # else too small
"""

# Use process or threads? (for gurus only)
grepSpawnMode = 'multiprocessing'   # multiprocessing, _thread, or threading 
grepSpawnMode = '_thread'           # ANDROID - multiprocessing fails, use threads code



#==================================================================================
# [3.0] Auto-Save Folder and Timing Control
#
# If autoSaveToFolder in the following is set to None (or not assigned) in the
# imported textConfig module, no auto-save is performed.
#
# Otherwise, every 5 minutes (by default), PyEdit auto-saves the text content
# of each changed and unsaved top-level or embedded-component window , to files
# in the folder to whose full path-name autoSaveToFolder is assigned here.
# These saved files serve as emergency recovery copies, and are automatically
# deleted by PyEdit after 7 days (by default) to minimize clutter and space.
#
# Important: auto-save DOES NOT overwrite the actual file(s) being edited
# in-place, but merely saves copies of changed and unsaved edit windows'
# content to a separate folder.  This feature is intended as a last resort
# for recovery from outright program crashes or unintended operator mistakes.
#
# Auto-save applies to all top-level windows in PyEdit, and to both top-level 
# popups and embedded components of View/Write windows in PyMailGUI.  In all
# roles, only changed windows' content is auto-saved (not text only viewed).
#
# FOLDER SETTING:
#
# The preset value below auto-saves files to a specially-named (but not hidden)
# folder in the running program's current working directory.  This is normally
# PyEdit's source directory, but not when PyEdit is being used as a tool by
# another program (e.g., changes in PyMailGUI appear in PyMailGUI's own source
# folder).  Users may change this to auto-save to any folder on their computer.
# Use a folder name with a leading "." if you prefer that this folder be hidden
# (e.g., so it is not copied by data archive/mirror programs such as mergeall).
# The auto-save folder is created automatically if it does not yet exist.
#
# TIMING SETTINGS:
#
# The preset values below run auto-save every 5 minutes, and prune saved files
# that have not been rewritten in one week's time.  You can change these values
# (e.g., to auto-save more or less often), but these defaults generally suffice:
# 5 minutes is frequent (and roughly the time it takes to compose no more than
# one decently-sized paragraph), and catastrophic data loss (e.g., due to a
# crash) will usually be known immediately.  If you prefer to auto-save but not
# auto-prune saved files, set the retention value to a very high number.  As a
# rule, the auto-save folder stores temporary copies, and is self-cleaning to
# minimize its clutter and size; save files in the GUI for long-term storage.
#
# FILENAMES:
#
# Auto-saves use either a known filename, or a generated name for nameless
# windows (i.e., text not opened from a file, and not yet saved to one).
# Both adopt naming patterns to make files unique in the auto-save folder.
#
# For known filenames, the auto-save's name is of form "ffff--AT--dddd",
# where "ffff" is the base filename, and "dddd" is the directory where "fff"
# is located, with slashes changed to underscores.  The directory part (or as
# much of it as will fit in a filename) is added to make same-named files
# unique if edited in the same or different PyEdit sessions.  Rename to
# delete the  directory after "--AT" if you are restoring from the save.
#
# For nameless windows (new text that has not yet been saved), the auto-save's
# name is of of form "_nameless-N-M.txt", where N is a nameless-edits sequence
# number that is unique within a session, and M is a process id that is unique
# across multiple PyEdit sessions running on your computer.  If you need to
# recover nameless text, it may help to also sort the auto-save folder by
# modtime, so you can focus on recent saves.
#
# UNICODE ENCODING:
#
# In all cases, auto-saves always encode all saved files per the general
# UTF-8 Unicode encoding scheme.  This handles all text, but convert saved
# files to different encodings if required for your use cases.
#==================================================================================


# Main setting: where to save files          # relative to '.' if no folder path 
autoSaveToFolder = '__pyedit-autosaves__'    # or pathame, or None=no auto-saves


# Timing settings
autoSaveMinsTillRun  = 5    # number minutes between auto-saves (5 == 1 para)
autoSaveDaysRetained = 7    # number days until auto-saved files are deleted



#==================================================================================
# [3.0] Run Code: Python Interpreter and Import Paths
#
# Users just getting started with Python coding can likely get by with this 
# section's defaults, which support editing and running most Python programs.
# Read on if you need access to your locally-installed libraries or Pythons.
#
# When launching a Python script with the Tools=>Run Code option, the default
# Python used for your code is that used to run PyEdit.  This is either:
#
# 1) The locally-installed Python used to run PyEdit.  This is always the case
# for source-code distributions of PyEdit, as well as Run Code's Click modes.
# Source-code PyEdit must be run with an installed Python, and Click modes run
# code with a Python you've associated with files or types on your computer.
#
# 2) A minimal version, with all Python standard libraries "baked in" but no
# builtin access to any extension libraries installed locally.  This is the case
# for frozen app and executable distributions, which require no Python install:
# your libraries aren't in the freeze, and a local Python can't be assumed. 
#
# You can override these defaults by setting variables below:
#
# RunCode_PYTHONEXECUTABLE:
#
#   To force PyEdit to run your code with a Python interpreter that you've
#   installed locally in Console and Capture modes, set the first variable below
#   to the full pathname of the installed Python executable you wish to use.
#   In most contexts this also adds the chosen Python's standard library folders 
#   to the sys.path import path automatically, so these do not require setup.
#
#   The executable setting works for any Python -- including a Python 2.X, even
#   though PyEdit itself runs on 3.X.  Python 2.X code generally runs in Pyedit,
#   including any "from __future__ import X" statements.  This means your code
#   can choose to use either Python 3.X or 2.X prints as usual.
#
#   Note that this setting is not required if you wish to experiment with basic
#   code in frozen PyEdits (which include the full Python standard library), or
#   use modules saved in the same directory as the script being run (which is
#   always on sys.path).  Edit this setting to use a specific Python, or enable
#   any locally-installed packages (path settings below can also do the latter).
#
#   Hint: to get your local Python's path for pasting here: run "import sys"
#   and then "sys.executable" at any ">>>" prompt.
#
# RunCode_PYTHONPATH_APPENDS/PREPENDS:
#
#   To force PyEdit to extend the module import path to include your local
#   development folders or extension installs in Capture mode, add your local
#   folders to the append and/or prepend lists of pathnames assigned to the
#   variables below.  Appends are added to the end of the import path, prepends
#   are added to the front, and in both cases multiple items are added in the
#   same left-to-right order as that in your lists here.  Prepends may work 
#   better in some cases (e.g., for same-named modules in multiple folders).
#
#   Note that these settings are not required for your main script's folder,
#   which is always on the path.  They are also not normally not required to use
#   standard library modules if you set a Python executable's path; sys.path is
#   then configured to see standard folders automatically by the Python run.
#
#   Also note that your normal PYTHONPATH environment variable may work for
#   setting import paths in Console and Capture modes too, but on some platforms
#   requires that PyEdit itself be launched from a console command line instead
#   of by clicks (e.g., for Mac OS X apps).  Use the import-path settings here
#   if needed to configure your path to import from local folders.
#
# In all cases, PyEdit ignores pathnames set here that do not exist or refer to
# invalid types, and falls back on its defaults.
#
# WHEN THESE SETTINGS ARE NEEDED:
#
# 1) You generally do _not_ need to set any of this section's three names
# when running PyEdit's source-code version, as you will control the version
# of Python (and its libs) used to start PyEdit, and hence run your own code.
# You may still want to set your Python, though, to test edited code with a
# different version than that required to run PyEdit itself.
#
# 2) You probably _do_ need to set Python executable and/or module-import paths
# if you wish to access any locally-installed third-party libraries in code run
# by a frozen PyEdit app or executable.  Your local Python's site-packages
# folder is unknown to the frozen PyEdit's bundled Python.  Setting a Python
# executable also makes its site-packages folder automatically importable.
#
# 3) The only _required_ setting here is Python executable for Console mode,
# when using frozen PyEdits on Windows or Linux (no stand-alone Python ships).
# Frozen Pyedits _may_ also also require a locally-installed Python executable's
# path in order to run some programs that start other Python programs in 
# Capture mode; see README.txt and docetc/examples/RunCode-examples/spawner.py.
# Settings are optional in other cases, and depend on your goals.
# 
# CAVEAT: 
#
# These settings work, but running alternative Pythons is a complex business.
# Some third-party packages may manipulate import paths in unusual ways that
# may throw off Run Code imports on some platforms, even with the settings here.
# As a worst-case fallback, use the source-code version of PyEdit if frozen 
# PyEdits refuse to use your local Python or allow imports of your local libs.
#
# See the Run Code dialog's in-program Help for more Run Code usage details.
# See the examples below the settings here for more ideas and inspiration.
#==================================================================================


# Use this Python (and its libs) instead of default
RunCode_PYTHONEXECUTABLE = None              # None=use default, else 'pathname'


# Append all these to sys.path's tail for imports
RunCode_PYTHONPATH_APPENDS = []              # list of pathname strings to add


# Prepend all these to sys.path's front for imports
RunCode_PYTHONPATH_PREPENDS = []             # list of pathname strings to add



#-------------------------------------------------------------------------------
# EXAMPLES - remove triple-quote lines above and below a choice and edit.
#-------------------------------------------------------------------------------


# Using a specific Python 3.X exe for frozen app/exe distributions or source
r"""
if RunningOnMac:
    RunCode_PYTHONEXECUTABLE = \
        '/usr/local/bin/python3'        # python.org's 3.X (see also Homebrew)
        #or: '/Library/Frameworks/Python.framework/Versions/3.5/bin/python3'

elif RunningOnWindows:
    RunCode_PYTHONEXECUTABLE = \
        r'C:\Users\*YOURNAME*\AppData\Local\Programs\Python\Python35\python.exe'

elif RunningOnLinux:
    RunCode_PYTHONEXECUTABLE = \
        '/usr/bin/python3'
"""


# Running Python 2.X code in PyEdit, with 2.X or 3.X prints (yes, it works!)
r"""
if RunningOnMac:
    RunCode_PYTHONEXECUTABLE = \
        '/usr/bin/python'               # Python 2.X (Mac's default)
        #or: '/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7'

elif RunningOnWindows:
    RunCode_PYTHONEXECUTABLE = \
        r'C:\Python27\python.exe'       # ditto on Windows

elif RunningOnLinux:
    RunCode_PYTHONEXECUTABLE = \
        '/usr/bin/python'               # likewise on Linux
"""


# Adding a specific Python exe's install folders
# Usually optional: sys.path is normally setup automatically by the Python executable
r"""
if RunningOnMac:
    RunCode_PYTHONPATH_APPENDS = [
        '/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages'
        ]
        
elif RunningOnWindows:
    RunCode_PYTHONPATH_APPENDS = [
        r'C:\Users\*YOURNAME*\AppData\Local\Programs\Python\Python35\Lib\site-packages'
        ]

elif RunningOnLinux: pass  # edit me
"""


# Adding your local dev or lib folders for imports
# This works in contexts where the usual PYTHONPATH setting is not supported
r"""
if RunningOnMac:
    RunCode_PYTHONPATH_APPENDS  = ['/MY-STUFF/Code']            # tail, this order
    RunCode_PYTHONPATH_PREPENDS = ['/MY-STUFF/Code/ziptools']   # front, this order

elif RunningOnWindows:
    RunCode_PYTHONPATH_APPENDS  = [r'C:\MY-STUFF\Code']    
    RunCode_PYTHONPATH_PREPENDS = [r'C:\MY-STUFF\Code\ziptools']

elif RunningOnLinux: pass  # edit me
"""



#==================================================================================
# 2.1: Unicode Encoding Behavior and Types for File Opens and Saves
#
# --These are complex and installation-wide: change with care--
#
# PyEdit attempts the cases listed below in the order shown, until the first
# one that works; set all variables to false/empty/0 to use your platform's
# default (which is generally 'utf-8' on Windows, Mac OS X, and Linux, but may
# be 'utf-8', 'ascii', or 'latin-1' on some - see sys.getdefaultencoding()).
#
# These settings are always imported from *this file*, not a client program's
# local textConfig.py in '.'.  They are located here via sys.path if PyEdit
# is __main__, else by package relative imports (see textEditor.py).
#
# UNICODE POLICY NOTES:
#
# [3.0] As shipped, both Ask settings below are True, which triggers popup dialogs
# on both opens and saves to ask for encodings.  This is best from a correctness
# perspective, but the general (non-book) release's users might not know or care
# about Unicode, and will likely be editing only their files encoded per their
# platform's default.
#
# If you are in this non-book group, either accept the popups' prefilled defaults,
# or set the Ask settings below to False to skip the popups completely.  On most
# systems, the prefilled default is UTF-8, which also handles simple ASCII text.
#
# However, users who may be editing mixed Unicode file types (e.g., both UTF-8
# and UTF-16) should generally leave these settings as is, and enter an encoding
# name when asked.  Providing the correct encoding name avoids translation errors,
# some of which could pass silently if text is decodable by an incorrect scheme.
#
# OTHER IDEAS:
#
# [3.0] In retrospect, this might have tried a single setting and asked otherwise,
# or tried each of a set of common encodings until one worked or all failed, but
# these are error-prone models: some text may decode per a set or tried encoding,
# but only accidentally!  Guessing from content (as most web browsers do) could
# be tried too, but it's impossible to guess correctly in all cases; making
# encodings explicit seems a more deterministic and safer paradigm in the end.
#
# MISC NOTES:
#
# savesUseKnownEncoding values:
#     0=No, 1=Yes for Save only, 2=Yes for Save and SaveAs.
# For Opens, the Ask popup's prefilled value is:
#     opensEncoding -or- platform default.
# For Saves, the Ask popup's prefilled value is:
#     known encoding -or- savesEncoding -or- platform default.
#==================================================================================

                       # 1) try internally-known type first (e.g., email charset)
opensAskUser = True    # 2) <=if True, try user input next (prefilled with default)
opensEncoding = ''     # 3) <=if nonempty, try this encoding next: 'latin-1', etc.
                       # 4) try sys.getdefaultencoding() platform default next 
                       # 5) use binary mode bytes and Tk policy as the last resort

savesUseKnownEncoding = 1    # 1) <=if > 0, try known encoding from last open or save
savesAskUser = True          # 2) <=if True, try user input next (prefill with known?)
savesEncoding = ''           # 3) <=if nonempty, try this encoding next: 'utf-8', etc.
                             # 4) tries sys.getdefaultencoding() as a last resort


# [END USER SETTINGS]
