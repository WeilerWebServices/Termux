"""
==========================================================================
PyGadgets user-configurations file

# ANDROID version, Jan 2019 (see "# ANDROID" for changes)

Set variables available in this Python-code file to customize the 
appearance of both PyGadgets itself and any of the gadgets it launches.
Settings here override any defaults used by the individual gadgets.

For COLORS:
    Use either a color name (e.g., 'skyblue') or a RGB color hexstring 
    '#RRGGBB' (e.g., '#74c3e8').  Run the included pickcolor.py script's 
    simple GUI to select a color's RGB string for use in this file.

For FONTS:
    Use a 3-item tuple of the form (family, size, style), where family
    is the font-family name string (e.g., 'courier new'), size is the 
    size of the font (e.g., 14), and style is an optional string of 
    space-separated options (e.g., 'bold italic').  Using None instead
    of the tuple means the system default font is used.

    Technically, a font's style part is a space-separated list that may
    include 'normal' or 'bold', and 'italic' or 'roman', and an omitted 
    style defaults to 'normal'.  Size may be positive for points, negative
    for pixels, or 0 for a default size, and omitting size is the same as
    0 (the default).  Font may also be a string 'family size style...' 
    if the family name has no spaces, but tuples are generally simpler.

For SIZES:
    Use either None for default size, or string 'NxM' where N and M are
    numbers that give width and height, respectively (e.g., '280x300').

For PATHNAMES:
    File and folder pathnames can use "/" for directory separators on all 
    platforms (including Windows), and may be relative to "." or absolute.

Caution: an error in the code here will likely prevent PyGadgets from
launching.  Save a backup copy, and check your syntax with a Python 
interactive-prompt import or other techniques.  Each gadget's config
set is a class to make names unique; mind their nested indentation.
==========================================================================
"""

import sys, os, tkinter

# for platform-specific settings
RunningOnMac     = sys.platform.startswith('darwin')    # all Max OS (X)
RunningOnWindows = sys.platform.startswith('win')       # all Windows
RunningOnLinux   = sys.platform.startswith('linux')     # all Linux

# for Python- or Tk-specific choices
PyVersion = float(sys.version[:3])       # '3.5.0 ...' => 3.5
TkVersion = tkinter.TkVersion            # 8.5 or 8.6 (Win Py 3.4+=Tk 8.6)



##########################################################################
# Configurations for PyGadgets toolbar itself (not its gadgets)
##########################################################################

if RunningOnMac:
    InitialSize = '365x30'     # size on open (WidthxHeight)
else:
    InitialSize = None         # None means system default

BgColor = 'beige'              # toolbar background (name or RGB)
FgColor = 'black'              # toolbar foreground (button text)

Font = None                    # None means system default

# ANDROID - disabled due to some font crashes (experiment as desired)
"""
if RunningOnMac:
    Font = ('menlo', 14, 'italic')
elif RunningOnWindows:
    Font = ('consolas', 12, 'italic bold') 
elif RunningOnLinux:
    Font = ('inconsolata', 12, 'italic bold')
"""


##########################################################################
# PyCalc configurations
##########################################################################

class PyCalcConfig:

    #---------------------------------------------------------------------
    # Basic settings.
    #---------------------------------------------------------------------
 
    if RunningOnMac:
        InitialSize = '300x350'        # size of window on open, WxH
    elif RunningOnWindows:
        InitialSize = '400x500'        # Windows looks better larger
    elif RunningOnLinux:
        InitialSize = '350x400'        # None = default for GUI content

    BgColor = 'skyblue'                # operand button foreground, background
    FgColor = 'black'                  # colors reversed for operator buttons

    #---------------------------------------------------------------------
    # Button, display, and cmd popup font.
    #---------------------------------------------------------------------

    Font = ('courier', 16, 'bold')     # default (or per platform, below) 

    # ANDROID - disabled due to some font crashes (experiment as desired)
    """
    if RunningOnMac:                  
        Font = ('menlo', 16, 'bold')
    elif RunningOnWindows:
        Font = ('consolas', 15, 'bold') 
    elif RunningOnLinux:
        Font = ('inconsolata', 15, 'bold')
    """

    #---------------------------------------------------------------------
    # Calc history popup settings.
    #---------------------------------------------------------------------

    HistBgColor = 'beige'

    if RunningOnMac:     
        HistFont = ('courier', 15, 'normal') 
    else:
        HistFont = ('courier', 13, 'bold')



##########################################################################
# PyClock configurations
##########################################################################

class PyClockConfig:

    #---------------------------------------------------------------------
    # Size is used only by analog display, which is always square (NxN):
    # it uses just the first dimension (width), so this can be '250x'.
    #---------------------------------------------------------------------
    
    if RunningOnMac:
        InitialSize = '250x250'    # size of analog clock on open
    else:
        InitialSize = '300x'       # larger on Windows and Linux

    #---------------------------------------------------------------------
    # Digital clock appearance.
    #---------------------------------------------------------------------

    DigitalFgColor = 'black'       # None=use FgColor (always uses BgColor)

    if RunningOnWindows:
        DigitalFont = ('consolas', 12, 'bold')   # Windows system fonts are tiny
    else:
        DigitalFont = ('system', 0, 'bold')      # None=default (so does system/0)

    #---------------------------------------------------------------------
    # Analog clock appearance.
    #---------------------------------------------------------------------

    BgColor = 'ivory'          # clock-face canvas
    FgColor = 'cyan'           # analog circle ticks (or #009090?)

    HhColor = 'brown'          # hour hand
    MhColor = 'tan'            # minute hand
    ShColor = 'blue'           # second hand

    CogColor = 'white'         # center point

    #---------------------------------------------------------------------
    # Pathname of image to use in middle of analog clock, or None to omit.
    #
    # For apps and executables, this can be nearly any image file type. 
    # For source code, this should be a GIF image file, unless your Python 
    # uses Tk 8.6+ (for PNGs) or you install Pillow (for most image types).
    # See README.txt's source-code package "Dependencies" for more details. 
    # Presize your images as needed to work with your InitialSize setting.
    #
    # MAC OS USERS: use a GIF or JPEG image, not PNG.  Due to a bug in the 
    # underlying Tk library, using a PNG image for the clock face on some
    # Macs can leak memory so badly as to kill the computer by the end of 
    # the day if the analog display is left open (oddly, the leak is much 
    # more rapid on Sierra than El Capitan).  Because of this, PyPhoto
    # will remind you if you try to use a PNG image, and substitute a GIF.
    #
    # ALSO ON MAC OS: despite the PNG fix, PyClock's memory usage may still
    # grow modestly over time.  To avoid memory growth, minimize PyClock 
    # to the Dock when it's not in use.  See README.txt for more details.
    # Memory growth has been observed only on Mac OS, not Windows or Linux,
    # and does not occur on Mac OS while the clock is minimized.
    #---------------------------------------------------------------------

    #PictureFile = None   # no image

    if RunningOnMac:
        PictureFile = '_PyClock/Clock/images/PyGadgets1024_128x128.gif'
    else:
        PictureFile = '_PyClock/Clock/images/PyGadgets1024_128x128.png'

    #---------------------------------------------------------------------
    # OR... PP4E's default clock config (remove both """ to use).
    # See also: clockStyles.py demo script in the source-code package.
    #---------------------------------------------------------------------
    """
    InitialSize = '200x200'
    BgColor = 'white'
    FgColor = 'brown'
    HhColor = 'black'
    MhColor = 'navy'
    ShColor = 'blue'
    CogColor = 'red'
    PictureFile = '_PyClock/Clock/images/PythonPowered.gif'    # '/' okay on Windows 
    """



##########################################################################
# PyPhoto configurations
##########################################################################

class PyPhotoConfig:

    #---------------------------------------------------------------------
    # Thumbnails directory-window size (None='500x400').
    #---------------------------------------------------------------------

    InitialSize = '630x500'                       # 'WidthxHeight' if set

    #---------------------------------------------------------------------
    # Open this folder first (None=choose in GUI).
    #---------------------------------------------------------------------

    InitialFolder = '_PyPhoto/PIL/images-mixed'   # mixed-size small examples
 
   #InitialFolder = '_PyPhoto/PIL/images-large'   # alternative examples set  
   #InitialFolder = '/MY-STUFF/Camera/DCIM'       # photos from a camera/card

    #---------------------------------------------------------------------
    # Max scaled image-view size (None=fit to screen size).
    #---------------------------------------------------------------------

    ViewSize = None                               # fit to display size

   #ViewSize = '800x600'                          # alternative smaller view
   #ViewSize = '400x300'                          # smaller still

    #---------------------------------------------------------------------
    # Forcibly disable image-change detection for large, static archives.
    #
    # Set this to True to prevent spurious thumbnail regenerations that
    # can occur in the rare event that modification times of your images
    # and thumbnails cache differ due to platform or filesystem skew.
    #
    # This should normally be False, so that a thumbnail is recreated 
    # whenever the corresponding image is changed.  Use True only if 
    # thumbnails are recreated even though images have not changed;
    # thumb creation is prohibitively slow; and images won't change.
    #
    # This applies to image-change testing only.  Thumbnails may still 
    # be added or deleted when images are added, deleted, or renamed, but
    # this is intended only for archives that are not expected to change.
    # When passed as a command-line argument, an empty string == False.
    #
    # This setting's False default need not be changed in typical usage.  
    # For example, PyPhoto photo archives and thumb caches work correctly 
    # without this change when used on a single platform, burned to BD-R 
    # discs, or transferred between Mac OS and Windows on exFAT drives.
    #---------------------------------------------------------------------

    NoThumbChanges = False    # skip modtime-based thumb regeneration?



##########################################################################
# PyToe configurations
##########################################################################

class PyToeConfig:

    #---------------------------------------------------------------------
    # If DemoMode=True, PyToe displays preconfigured boards of various
    # degrees, colors, and move modes (and ignores these settings below).
    # Otherwise, it shows one board using all settings in this section.
    #---------------------------------------------------------------------

    DemoMode = True                   # use preset boards/games?

    #---------------------------------------------------------------------
    # Non-DemoMode settings follow.
    #---------------------------------------------------------------------

    InitialSize = '250x250'           # 'WxH' size on open, or None=default

    BgColor = 'navy'                  # board background
    FgColor = 'white'                 # board foreground (marks)

    Font = ('courier', 50, 'bold')    # font of X/O marks on board

    #---------------------------------------------------------------------
    # Lesser-used options.
    #---------------------------------------------------------------------

    GoesFirst = 'user'     # first move: 'user' or 'machine'
    UserMark  = 'X'        # user's mark character: 'X' or 'O'
    Degree = 3             # N for NxN board (3 = tic-tac-toe)

    #---------------------------------------------------------------------
    # Mode is machine move-choice class name (i.e., machine skill-level).
    # Use Minimax, Expert2, Expert1, Smart, or Random (best to worst?).
    # Minimax is moves-lookahead search, Expert1/2 and Smart use scores.
    # Minimax is ideal, but for speed doesn't look deeply if Degree > 3.
    # Caveat: tic-tac-toe has patterns that always win, despite all AI.
    #---------------------------------------------------------------------

    Mode = 'Minimax' if Degree <= 3 else 'Expert2'

    #---------------------------------------------------------------------
    # OR... a 4-across game alternative (remove both """ to use).
    #---------------------------------------------------------------------
    """
    InitialSize = None
    BgColor = 'wheat'
    FgColor = 'black'
    Font = ('courier', 50, 'bold')
    GoesFirst = 'user'
    UserMark  = 'X'
    Degree = 4
    Mode = 'Expert2'
    """


#[end]