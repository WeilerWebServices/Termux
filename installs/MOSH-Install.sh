#!/system/bin/sh
# MOSH

echo Mosh is a remote terminal application that allows roaming, supports intermittent connectivity, and provides intelligent local echo and line editing of user keystrokes.

echo Usage example

echo Important note: Mosh should be installed on both client and server side.

echo Connecting to remote host (sshd listening on standard port):

echo mosh user@ssh.example.com

echo Connecting to Termux (sshd listening on port 8022):

mosh --ssh="ssh -p 8022" 192.168.1.25
Rsync
echo Rsync is a tool for synchronizing files with remote hosts or local directories (or drives). For better experience of using rsync, make sure that package `openssh` (or `dropbear`) is installed.

echo Usage example

echo Sync your photos with PC:

rsync -av /sdcard/DCIM/ user@192.168.1.20:~/Pictures/Android/

echo Get photos from remote Android device:

rsync -av -e 'ssh -p 8022' 192.168.1.3:/sdcard/DCIM/ /sdcard/DCIM/

echo Sync local directories (e.g. from external sdcard to Termux home):

rsync -av /storage/0123-4567/myfiles ~/files

echo You may want to see man page (`man rsync`) to learn more about it's usage.
