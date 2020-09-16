# -*- coding: utf-8 -*-
r"""
======================================================================================
frigcal_configs.py: optional user-provided configuration settings.

#-------------------------------------------------------------------------------------
# ANDROID version, Jan-Apr 2019 (see "# ANDROID" for all changes).
# Recent changes (search on date string for settings changed):
# [Apr1219] Use smaller button/month font presets for smaller-phone fit. 
#-------------------------------------------------------------------------------------

Code simple Python assignments in this file to customize your frigcal's
appearance and behavior.  Your settings will be loaded at frigcal startup.
See frigcal_configs_base.py for the full set of options you can customize
by reassigning names here, along with their defaults and documentation.

DETAILS:

This file is shipped in UTF-8 Unicode and Windows or Unix end-line format;
see UserGuide.html's "Using the Program" => "Configurations File" section. 

In version 2.0+, EDIT THIS FILE for all user-defined customizations, instead
of changing the frigcal_configs_base.py base file in-place.  This file (not
the base) is imported by frigcal at startup, and imports "*" from the base
file initially to load preset "factory" defaults.  Any assignments you code
here will override (i.e., replace) the corresponding default assignments in
the base file automatically.

Your customizations here will also be immune to changes in the base file when
upgrading to new frigcal versions, as long as you save your version of this
file and restore it in the new version after installation.  Any errors in
this file are still reported by both GUI popup and console message as before.

See the frigcal_configs_base.py base file in this folder for setting examples,
settings available, and all settings documentation.  Coding note: the initial
"from *" here could be avoided by having the base file import this (instead
of vice versa), but per Python philosophy: Explicit Is Better Than Implicit. 
======================================================================================
"""
import sys, os  # for platform, etc.

# Load the base file's defaults first (don't delete this line!)
from frigcal_configs_base import *


# ----User-defined customizations of frigcal_configs_base.py follow----

# Code your assignments here; they'll be immune to base-file changes on upgrades


#=====================================================================================
# ANDROID changes section
#=====================================================================================


# ANDROID - use None=tkinter's or program's default fonts, to avoid crashes.
# Pydroid 3's tkinter crashes if font family != courier/helvetica/times or synonyms.
# Change to experiment with your own settings, and see frigcal_configs_base.py for ideas.
# Also set your icspath and imgpath for calendars and images located elsewhere.

daysfont = None               # text on month day-tiles: (family, size, style)
monthnamefont = None          # text of month name at top of window
daynamefont = None            # text of day names at top of window
controlsfont = None           # text on buttons and toggles
footerfont = None             # text in the footer panel
eventdialogfont = None        # text in event view/edit dialogs


# ANDROID [Apr1219] - preset smaller fonts to avoid truncation on smaller phones.
# Caveat: month abbreviation (or redesign) may be warranted for very small phones.
# The "mm/yy/dddd" input field size was also reduced, but is hardcoded in the script.
# Note: the controlsfont preset for buttons below actually is the None default on 
# some phones (e.g., Note 9), but is noticeably smaller on smaller devices (e.g., J7).

monthnamefont = ('times', 10, 'bold italic')    # thinner and shorter (on all tested)
controlsfont  = ('helvetica', 6, 'normal')      # smaller buttons (on smaller phones)

# ANDROID - preset event dialog font for readability (default is just 5 points),
# and preset the view/edit dialog's size for fit; tailor both for your usage.
# Note: eventdialogfont sets all text items' fonts; some differ for None=defaults.

eventdialogfont = ('courier', 6, 'normal')
eventdialogtextheight = 10    # number lines (None=default=5; Tk default=24)
eventdialogtextwidth  = 80    # number characters (None=Tk default=80, prior preset)


# ANDROID - put your custom calendars-folder path here (None = program's Calendars/).
# In order, these are: internal storage, SD card updatable, SD card read only, and the 
# default; yours will vary.  Also see month-images path ahead (and don't maximize).

#icspath = '/sdcard/MY-STUFF/Code/frigcal/Calendars'
#icspath = '/storage/6C2A-1618/Android/data/ru.iiec.pydroid3/MY-STUFF/Code/frigcal/Calendars'
#icspath = '/storage/6C2A-1618/Android/data/com.termux/MY-STUFF/Code/frigcal/Calendars'
icspath = None


# ANDROID - use single-tap/click mode on smartphones for easier operation, 
# and to avoid pointless keyboard popups on event clicks; change as desired.

#clickmode = 'mouse'          # double-press model, with inline summary edits
clickmode  = 'touch'          # single-press model


#=====================================================================================
# Original code follows
#=====================================================================================


"""
rootbg = '#A28264'     # removed the 3 quotes above and below to activate code
daysbg = 'wheat'       # basic settings include colors, fonts, etc.
"""


# Calendar files folder (else uses install folder's Calendars)
"""
if RunningOnMac:
    icspath = '/MY-STUFF/Code/frigcal/Calendars'        # outside app and source?
elif RunningOnWindows:
    icspath = r'C:\MY-STUFF\Code\frigcal\Calendars'     # outside exe and source?
elif RunningOnLinux:
    icspath = '/home/ubuntu-user/frigcal/Calendars'
"""


# Calendar files alternative: user guide's screenshots demo files, in install dir
"""
if RunningOnMac:
   #icspath = '/MY-STUFF/Code/frigcal/Calendars/2.0-examples/Screenshots-Demo-Calendars'
    icspath = '/Applications/Frigcal.app/Contents/Resources/Calendars/2.0-examples/Screenshots-Demo-Calendars'
elif RunningOnWindows:
   #icspath = r'C:\MY-STUFF\Code\frigcal\Calendars\2.0-examples\Screenshots-Demo-Calendars' 
    icspath = r'C:\Program Files\Frigcal\Calendars\2.0-examples\Screenshots-Demo-Calendars' 
elif RunningOnLinux:
   #icspath = '/home/ubuntu-user/My-Code/Frigcal/Calendars/2.0-examples/Screenshots-Demo-Calendars'
    icspath = '/home/ubuntu-user/Desktop/frigcal/Calendars/2.0-examples/Screenshots-Demo-Calendars'
"""


# Month images folder (else uses install folder's MonthImages)
"""
imgpath = 'MonthImages/AlternateMonthImages/DrawnImages1'.replace('/', os.sep)   # portable
"""


# And many more... see frigcal_configs_base.py
