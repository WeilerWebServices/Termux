*Note: this file's shortcut hints are largely superseded by more recent launchers*

1) See launch-mergeall-GUI.pyw for a basic but portable tkinter desktop GUI that
inputs settings and launches mergeall.py automatically.  You can drag just this file
out to your Desktop for quick launches; it was written after (and, for -report and 
-auto modes, somewhat obviates) both the console and shortcut options described in 
the rest of this file.

2) See launch-mergeall-Console.py for a more portable script that inputs settings 
interactively, and may be drug out to a single Desktop icon on Windows (and other).
This scrip additionally supports selective update mode.

For both of the above, laucher-configs\mergeall-desktop-icon.ico can be used as the
shortcut's icon.

----

WINDOWS USERS: if you want to avoid command lines, you can make clickable shortcuts on your
desktop (or elsewhere) that launch this script automatically in a Command Prompt window, to 
report only, or run upload/download syncs.  Here's how (see "cmd /?" for more details):

1) Set PYTHONIOENCODING=utf8, in Control Panel -> System -> Advanced -> Environment variables 
(so this is made global and persistent; it may be needed if you have Unicode filenames in your trees).

2) On the desktop, right-click to make 3 New shortcuts to file "C:\Windows\System32\cmd.exe"
(or wherever the cmd.exe Command Prompt executable is on your machine: search C: if needed).

3) Name/rename the shortcuts as desired
(names used in this example, where tb is a drive: "sync report", "sync to tb", "sync from tb").

4) Open their Properties (right-click) and set their "Target:" field to the following
(your folder/machine names will vary, and your drive letters may vary: in this example,
D is the source SD card and E is the backup drive; use C for your main drive if that's
where a subject folder lives):

--for shortcut name: sync report
  C:\Windows\System32\cmd.exe /K "D:\MY-STUFF\Code\mergeall\mergeall.py D:\MY-STUFF E:\MY-STUFF -report"

--for shortcut name: sync to tb
  C:\Windows\System32\cmd.exe /K "D:\MY-STUFF\Code\mergeall\mergeall.py D:\MY-STUFF E:\MY-STUFF -auto > D:\MY-STUFF\admin\mergeall-moses-tbdrive.txt && notepad D:\MY-STUFF\admin\mergeall-moses-tbdrive.txt"

--for shortcut name: sync from tb
  C:\Windows\System32\cmd.exe /K "D:\MY-STUFF\Code\mergeall\mergeall.py E:\MY-STUFF D:\MY-STUFF -auto > D:\MY-STUFF\admin\mergeall-tbdrive-moses.txt && notepad D:\MY-STUFF\admin\mergeall-tbdrive-moses.txt"

If this works, you have 3 shortcuts that run mergeall to report, upload, and download when clicked;
all 3 keep the console window open on exit for viewing results, though the latter 2 send all results 
to a text file which is opened automatically on exit (the first simply scrolls results as they appear).
These are a temporary convenience, unless/until a GUI appears.