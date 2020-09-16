Mergeall — Backup and Mirror Your Stuff Your Way

Fetch: 
    From "http://learning-python.com/mergeall.html" download and unzip:

    - Mergeall.app.zip (Mac app)
    - Mergeall-64bit.zip or Mergeall-32bit.zip (Windows executable)
    - Mergeall.zip (Linux executable)
    - Mergeall-source.zip (source code)

    See Package Usage Basics below for more install details.

Start:
    To launch the program, run the unzipped folder or its file:

    - Mergeall.app (Mac app) 
    - launch-mergeall-GUI.exe (Windows executable)
    - launch-mergeall-GUI (Linux executable)  
    - launch-mergeall-GUI.pyw (source code)

    See Package Usage Basics below for more run details.

Docs:
    Open UserGuide.html in a web browser for the main user guide.
    Select 'Help' in the GUI to view that document in any distribution. 

Configs:
    Edit mergeall_configs.py to customize mergeall's appearance and behavior.

Backups:
    When backups are enabled, mergeall saves all files deleted or changed by
    a run in the __bkp__ folder of the "TO" destination.  See UserGuide.html.

Tools:
    mergeall is coded in Python, and uses tkinter/Tk for its GUI.  
    Mac frozen apps are built with py2app; others use PyInstaller.  

Versions:
    3.0, Jun-2017: major release - GUI redesign, Mac OS, cruft, app/exes
    3.1, Dec-2017: minor upgrade - folder modtimes, Linux flushes, "-u"
    See docetc/MoreDocs/Revisions.html for all versions and changes.

Upgrades:
    To install a new version of mergeall in the future, save and restore
    any customizations you've made in mergeall_configs.py.

Screenshots:
    See UserGuide.html or folder docetc/docimgs for GUI samples.

------------------------------------------------------------------------------

Package Usage Basics

mergeall is available as full source code, a Mac app, and executables
for Windows and Linux.  Source code is the ultimate in portability,
but apps and executables integrate better with your computer's GUI,
do not require any additional install steps, and are immune to 
future changes in the Python programming language they use.

The following sections give the fundamentals of each format's usage:

    - Mac OS App Package
    - Windows Executable Packages
    - Linux Executable Package
    - Source-Code Package

------------------------------------------------------------------------------

Mac OS App Package

    The Mac OS (f.k.a. OS X) app runs only on Mac systems, but requires 
    no Python install and better supports the Mac user experience.

    To install:
        Fetch file "Mergeall.app.zip", unzip it by a double-click (or other), 
        and drag the resulting Mergeall.app to your /Applications folder in 
        Finder to access it from Launchpad.  You can also move Mergeall.app 
        and create aliases to it anywhere else on your computer.
    
    To Run:
        Click "Mergeall.app" to start the program (or run the app any other way).
        Running Mergeall.app automatically launches mergeall's GUI launcher,
        the same as running the source-code package's launch-mergeall-GUI.pyw.
        From the GUI, configure and run mergeall to propagate your content.

        Clicking mergeall's app icon or Dock entry while the program is running 
        automatically deiconifies (unhides) its main window, and always lifts
        it above other windows on screen (handy to locate it in a busy session).
        Double-click the app and single-click the Dock to make this work.

    Files:
        Your mergeall_configs.py file is located inside the unzipped app's 
        folder, at path:
        
            Mergeall.app/Contents/Resources

        Navigate to this nested folder in Finder by a right-click on 
        Mergeall.app and Show Package Contents (or use "ls" in Terminal).
        Your UserGuide.html is in the same folder, but can also be 
        accessed by the program's "Help" button.

    Scripts:
        All mergeall scripts are frozen executables in the app's folder:
        
            Mergeall.app/Content/MacOS
        
        The scripts have no ".py" extension in this format, but otherwise run 
        exactly as documented.  No separate Python install is required to run 
        these from command lines in Terminal.  For example, if you've drug the
        unzipped folder to your /Applications, the following work in Terminal:

        CPALL:
          /Applications/Mergeall.app/Contents/MacOS/cpall dirFrom dirTo -skipcruft

        DIFFALL:
          /Applications/Mergeall.app/Contents/MacOS/diffall dir1 dir2 -skipcruft
          /Applications/Mergeall.app/Contents/MacOS/diffall dir1 dir2 -skipcruft -u > log.txt

        MERGEALL:
          /Applications/Mergeall.app/Contents/MacOS/mergeall dirFrom dirTo -report
          /Applications/Mergeall.app/Contents/MacOS/mergeall dirFrom dirTo -auto -backup -skipcruft

        LAUNCHERS:
          /Applications/Mergeall.app/Contents/MacOS/launch-mergeall-Console 
          /Applications/Mergeall.app/Contents/MacOS/launch-mergeall-GUI  (the same as an app click)

        OTHER:
          /Applications/Mergeall.app/Contents/MacOS/rollback
          /Applications/Mergeall.app/Contents/MacOS/fix-fat-dst-modtimes folder -add
          /Applications/Mergeall.app/Contents/MacOS/nuke-cruft-files -help

        Note that source-code versions of these scripts are also included in
        the app's Contents/Resources folder for their documentation, but will
        not generally run in this form and location; use the frozen executables
        in Contents/MacOS instead. 

    Versions: 
        The Mac OS app was built on Mac OS (a.k.a. OS X) version 10.11 El Capitan,
        as a Mac universal binary.  It has been verified to run on this as well 
        as Mac OS 10.12 Sierra and 10.13 High Sierra, and is expected to work on 
        later Mac OS versions too.  Support for earlier versions of Mac OS remains
        to be verified (feedback is welcome).

    Known issues:
        Due to limitations in the underlying Tk toolkit, emojis are replaced 
        for display only; see the user guide for details.

        Due to a flaw in the underlying Tk toolkit, closed windows may leave
        zombie items in Dock menus; these can be safely ignored.  See also 
        http://learning-python.com/post-release-updates.html#appexpose.

------------------------------------------------------------------------------

Windows Executable Packages

    The Windows executables run only on Windows systems, but require
    no Python install and better support the Windows user interface.

    To install:
        Fetch file "Mergeall-64bit.zip" or "Mergeall-32bit.zip" and unzip 
        it on your computer (see Versions below for the difference).  
        Copy the unzipped folder to C:\Program Files or elsewhere to 
        save it.  Make Desktop shortcuts to the unzipped folder's 
        executable (per the next section) for quick access as desired.

    To Run:
        Click on the unzipped folder's "launch-mergeall-GUI.exe" file to run.  
        This automatically starts mergeall's GUI launcher, the same as 
        running the source-code package's script launch-mergeall-GUI.pyw.
        From the GUI, configure and run mergeall to propagate your content.
        File "launch-mergeall-console.exe" runs the lesser-used console interface.

    Files:
        Your UserGuide.html, mergeall_configs.py, and utility-script exes are 
        are all located at the top level of the same folder as the main ".exe"
        executable (the folder created by unzipping the download).

    Scripts:
        mergeall's extra utility scripts in this package are all provided as
        executables that have a ".exe" extension instead of a ".py" and can be 
        run without a local Python install, but otherwise work the same.  For 
        example, the source package's diffall.py and rollback.py become ".exe"
        executables in this package (the ".exe" in these is usually optional):

            Mergeall-64bit\diffall.exe folder1 folder2 -skipcruft
            Mergeall-64bit\rollback.exe
       
        Scripts' ".py" source files are also included for their in-file 
        documentation, but some may not run in this form; use their .exes.
        See the Mac app's documentation above for more utility scripts.        

    Versions: 
        The Windows executable comes in both 64- and 32-bit forms, as denoted
        by its zipfile names.  The former works only on 64-bit systems; the 
        latter works more broadly but may run slower on 64-bit systems.  The
        64-bit executable was built on Windows 7, and the 32-bit version on 
        Windows 8, but both have been verified to run on Windows 7, 8, and 10.

    Known issues: 
        Startups may be briefly delayed due to PyInstaller folder extracts.  
        Use the source-code package if this is problematic on slower machines.

        Due to limitations in the underlying Tk toolkit, emojis are replaced 
        for display only; see the user guide for details.

------------------------------------------------------------------------------

Linux Executable Package

    The Linux executable runs only on Linux systems, but requires no
    Python install and may better support the Linux user interface.

    To install:
        Fetch file "Mergeall.zip" and unzip it on your computer.  Copy the
        unzipped folder to your home, desktop, or other folder to make it 
        easy to access, and make desktop shortcuts to the executable as 
        desired.  

    To Run:
        Click on the unzipped folder's "launch-mergeall" file to run.  
        This automatically starts mergeall's GUI launcher, the same as 
        running the source-code package's script launch-mergeall-GUI.pyw.
        From the GUI, configure and run mergeall to propagate your content.
        File "launch-mergeall-console.exe" runs the lesser-used console interface.
 
    Files:
        Your UserGuide.html, mergeall_configs.py, and utility-script executables
        are all located at the top level of the same folder as the main 
        executable (the folder created by unzipping the download).

    Scripts:
        mergeall's extra utility scripts in this package are all provided as
        executables that have no extension instead of a ".py" and can be 
        run without a local Python install, but otherwise work the same.  
        For example, the source package's diffall.py and rollback.py become
        Linux executables in this package:

            Mergeall/diffall folder1 folder2 -skipcruft
            Mergeall/rollback

        Scripts' ".py" source files are also included for their in-file 
        documentation, but some may not run in this form; use the executables.
        See the Mac app's documentation above for more utility scripts.        

    Versions: 
        The sole Linux executable was built on Ubuntu Linux 16.04, on a 
        64-bit system.  It is known to work on this and other versions of 
        Ubuntu and is expected to work on some other distributions of Linux,
        but this is to be verified.  If it fails on your system, use the 
        source-code mergeall package.

    Known issues:
        Startups may be briefly delayed due to PyInstaller folder extracts.  
        Use the source-code package if this is problematic on slower machines.

        Due to limitations in the underlying Tk toolkit, emojis are replaced 
        for display only; see the user guide for details.

------------------------------------------------------------------------------

Source-Code Package 

    The source-code version of mergeall runs on all flavors of Mac, 
    Windows, and Linux, but requires a separately-installed Python.

    To Install:
        Fetch file "Mergeall-source.zip" and unzip it on your computer.
        Also fetch and install a usable Python 3.X if one is not already
        present.  On Mac and Linux, also install the tkinter/Tk toolkit 
        if needed.  See the user guide's "Platform Basics" for details.

    To Run:
        Run "launch-mergeall-GUI.pyw" in the unzipped folder to launch the 
        program, using any Python program-launching technique on your 
        platform: Windows icon clicks, IDLE, command lines, Mac Python 
        Launcher, etc.  You can also run the file from within PyEdit
        (see learning-python.com/pyedit).

    Files:
        Your UserGuide.html, mergeall_configs.py, and utility scripts 
        are all located in the same folder as the main scripts' file
        (the folder created by unzipping the download).

    Versions:
        Source code is platform-neutral and is not dependent on the 
        version of your operating system.  This package runs on all
        versions of Mac OS, Windows, and Linux in common use today.
        
        The source-code package does, however, require and assume a
        separately-installed Python on your computer: download one 
        for your platform from www.python.org/downloads if Python is 
        not already installed.  
 
        mergeall's source code has been verified to run on all Python 
        3.X through 3.5, and has no third-party install requirements.
        Later Python versions are expected to work too, but 3.5 is 
        the latest version verified.

    Known issues:
        Due to limitations in the underlying Tk toolkit, emojis are replaced 
        for display only; see the user guide for details.

        On Mac OS, closed windows may leave zombie items in Dock menus due 
        to a flaw in the underlying Tk toolkit; use Tk 8.6+ if possible.  See
        also http://learning-python.com/post-release-updates.html#appexpose.

------------------------------------------------------------------------------