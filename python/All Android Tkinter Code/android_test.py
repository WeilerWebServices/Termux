"""
=======================================================================
To predefine names for platform-specific code, place this file in your
source-code package folder, and add this statement to any code file:

    from _android_test import *

Then use the three 'Running*' names below in your platform-test 'if's.

Future goal: use this for integrating Android code changes into base 
files; changes should really be 'if' statements, not custom versions.
This awaits more end-user testing, and source-code package rereleases.

Note, however, that the changes required for Pydroid 3 are specific 
to Pydroid 3 only (e.g., the sys.executable hardcoding).  The ethics 
of changing the portable source-code package to support just a single
app on Android are dubious, especially when that app employs freemium 
advertising.  For now, Pydroid 3 is best supported by custom code.
=======================================================================
"""
import os, sys

def _runningOnAndroid():
    """
    -------------------------------------------------------------------
    Test if running on Android, GUI or not.  Python 3.X's sys.platform
    is 'linux' on Android: check env vars instead.  This is a heuristic
    (and feels like user-agent sniffing hacks in JavaScript), but works
    in both Termux and Pydroid 3.  The latter might also just catch an 
    import error for the Kivy module, but that won't work in some apps. 
    -------------------------------------------------------------------
    """
    return any(key for key in os.environ if key.startswith('ANDROID_'))

# Import the following from this module for platform-specific code.
# RunningOnAndroid and RunningOnLinux are _both_ True on Android: to
# differentiate, test RunningOnAndroid first or use RunningOnLinuxOnly.

RunningOnAndroid    = _runningOnAndroid()
RunningOnLinux      = sys.platform.startswith('linux')
RunningOnLinuxOnly  = RunningOnLinux and not RunningOnAndroid

if __name__ == '__main__':
    print('On Android:   ', RunningOnAndroid)    # test
    print('On Linux:     ', RunningOnLinux)
    print('On Linux Only:', RunningOnLinuxOnly)
