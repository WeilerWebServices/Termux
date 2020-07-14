# Dropbear

echo Dropbear does not provide SFTP server.

echo Starting and stopping Dropbear server

echo Same as for OpenSSH, you will need to execute it's binary manually. Also, unlike OpenSSH, Dropbear does not use a configuration file but only command line arguments.

echo Server is running in background, both password and public key authentication available. To achieve this, just type in console:

dropbear

echo If you need only public key authentication, do this instead:

dropbear -s

echo Also, server can be started in foreground. For this purpose use a parameter `-F`:

dropbear -F

echo Server started in foreground can be stopped by just Ctrl-C key combination. If it is in the background, then you can use a `pkill`:

echo pkill dropbear

echo Setting up password authentication

echo Same as for OpenSSH, password authentication is enabled by default.

echo Everything you have to do, is:

echo 1. Make sure that everything is up to date and dropbear is installed:

apt update && apt upgrade -y

pkg update && pkg upgrade -y pkg install dropbear

echo 2. Set password by executing command passwd.

echo 3. Start dropbear server. You can execute either just dropbear to start it in background or dropbear -F to start it in the foreground.

echo Setting up public key authentication

echo Same as for OpenSSH, you can put your keys by using ssh-copy-id. But if you consider to setup a public key authentication from Termux to something else, it is worth to mention some important differences between OpenSSH and Dropbear.

echo 1. Dropbear uses a different command for generating keys. Example of generating RSA key (2048 bit):

dropbearkey -t rsa -f id_rsa -s 2048

echo 2. Public key should be obtained manually. To do this, you have to use 'dropbearkey' again, but in different way:

dropbearkey -f id_rsa -y

echo 3. Dropbear and OpenSSH uses a different key formats. To use a Dropbear's key in OpenSSH, you will have to convert it:

dropbearconvert dropbear openssh ./id_rsa ./id_rsa_openssh

echo This procedure can be done vice versa to obtain a key in Dropbear's format:

dropbearconvert openssh dropbear ./id_rsa_openssh ./id_rsa_dropbear

echo Using the SFTP

echo Package OpenSSH provides a tool for accessing remote hosts over SFTP. This will allow you to work with files in same way as via FTP but with better security.

echo Connecting to Termux (sshd listening on port 8022):

echo sftp -P 8022 192.168.1.20

echo Connecting to somewhere else (sshd listening on standard port):

echo sftp sftp.example.com

echo However, to use command line SFTP client you should know some basic commands:

cd PATH - change current directory to `PATH`.

echo get REMOTE [LOCAL] - download file `REMOTE` and rename it as `LOCAL` (optional).

echo mkdir PATH - create directory `PATH`.

echo ls [PATH] - list files in directory `PATH`. If no argument, files in current directory will be listed.

echo put LOCAL [REMOTE] - Upload file `LOCAL` and rename it as `REMOTE` (optional).

echo rm FILE - Delete file `FILE`.

echo This is not a complete list of SFTP commands. To view all available commands, consider to view man page (man sftp) or view short help in interactive SFTP session by issuing command `help`.
