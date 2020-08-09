#!/system/bin/sh

# Heroku

apt-get install wget nano tar gzip nodejs -y

cd /sdcard/apps/

wget http://cli-assets.heroku.com/heroku-linux-arm.tar.gz -O heroku.tar.gz

tar -xvzf heroku.tar.gz -C heroku

mkdir -p /data/data/com.termux/files/usr/lib/heroku

mv -v heroku/heroku-cli-linux-x64.tar.gz/* /data/data/com.termux/files/usr/lib/heroku

ln -s /data/data/com.termux/files/usr/lib/heroku/bin/heroku /data/data/com.termux/files/usr/bin/heroku

echo Heroku will not work as its script is pointing to /usr/bin/env whereas our path on Termux differs.

echo To direct Heroku to the right path, first install nano (or your own favourite editor), then edit Heroku’s script:

cd /data/data/com.termux/files/usr/lib/heroku/bin/

echo #!/usr/bin/env bash

echo Change this line to:

echo

echo #!/data/data/com.termux/files/usr/bin/env bash

sleep 2

echo Now Heroku is not yet working, one more fix and we’ll be done.

echo The tarball file does contain a necessary node.js binary but it does not work in Termux. you will have to install it with the Linux environment and point Heroku to its path.

touch heroku

sleep 2

nano heroku

cd /data/data/com.termux/files/usr/lib/heroku/bin

mv node node.old

ln -s ../../../bin/node node

echo When asked, press any key (expect ‘q’) to open a web browser and login your Heroku account.

echo Done
