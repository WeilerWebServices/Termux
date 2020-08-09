#!/system/bin/sh

# Setting up http server on android with termux

pkg install autoconf automake bison bzip2 clang cmake coreutils diffutils flex gawk git grep gzip libtool make patch perl sed silversearcher-ag tar  apache2 php php-apache -y

echo Installing and configuring apache2

echo In this and further steps you will need to acces the `/etc` folder, but in termux it is hidden in `/data/data/com.termux/files/usr/etc/`, so I suggest you to make link.

ln -s /data/data/com.termux/files/usr/etc/ ~/etc

echo You can configure it if you need in `~/etc/apache2/httpd.conf`.

echo Now you can run apache2 server by simple `httpd` (by default it will run on 127.0.0.1:8080).

echo According to archwiki page `libphp7.so` included with `php-apache` will only work with `mod_mpm_prefork`.

echo * In `~/etc/apache2/httpd.conf` comment following line:

echo LoadModule mpm_worker_module libexec/apache2/mod_mpm_worker.so

echo * Add following line in the start of section with LoadModule instructions

echo LoadModule mpm_prefork_module libexec/apache2/mod_mpm_prefork.so

echo To enable PHP, add these lines to `~/etc/apache2/httpd.conf`:

echo * Place this at the end of the LoadModule list:

nano ~/etc/apache2/httpd.conf

LoadModule php7_module libexec/apache2/libphp7.so

AddHandler php7-script .php


echo * Place this at the end of the Include list (this will be at the end of file):

mkdir etc/

mkdir etc/apache2/

mkdir etc/apache2/extra/

touch etc/apache2/extra/php7_module.conf

Include etc/apache2/extra/php7_module.conf

echo To test if php works:

echo * Create index.php file with arbitrary content

echo "<?php phpinfo();?>" > ~/../usr/share/apache2/default-site/htdocs/index.php

echo * Restart apache2 server

killall httpd; httpd

echo * Verify PHP output

curl 127.0.0.1:8080/index.php
