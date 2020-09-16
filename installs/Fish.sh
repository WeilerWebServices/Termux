#!/system/bin/sh

# Fish Install
# ============

echo "FISH is a smart and user-friendly command line shell for macOS, Linux, and the rest of the family."

echo "The FISH shell init files are ~/.fish, $PREFIX/etc/fish/config.fish and more. See `man fish` and `info fish` for more information."

echo "Oh-My-Fish of fish shell working without any known issue in termux, you can install it with official manual in the repository here. Run"

omf

echo "to get some help installing plugin and theme."

echo "Fisherman is a fish-shell plugin manager."

sleep 20s

curl -L https://get.oh-my.fish > install fish install --path=~/.local/share/omf --config=~/.config/omf

echo "You can install Oh My Fish with Git"

git clone https://github.com/oh-my-fish/oh-my-fish

cd oh-my-fish

bin/install --offline # with a tarball

curl -L https://get.oh-my.fish > install

fish install --offline=omf.tar.gz

echo "Run install --help for a complete list of install options you can customize."

echo "Install a plugin. fisher z"

echo "Install several plugins concurrently. fisher fzf edc/bass omf/thefuck omf/theme-bobthefish"

echo "Install a specific branch. fisher edc/bass:master"
sleep 20s

echo "Install a specific tag. fisher edc/bass@1.2.0"

echo "Install a gist. fisher https://gist.github.com/username/1f40e1c6e0551b2666b2"

echo "Install a local plugin. fisher ~/path/to/my_plugin Edit your fishfile and run fisher to commit changes, e.g. install missing plugins. $EDITOR ~/.config/fish/fishfile fisher"

echo "Show everything you've installed. fisher ls @ my_plugin # a local plugin"
sleep 20d

bobthefish # current theme

bass fzf thefuck z 

echo Show everything available to install. fisher ls-remote

echo Show additional information about plugins: fisher ls-remote --format="%name(%stars): %info [%url]\n"
sleep 2

echo Update everything.
fisher up

echo Update specific plugins. fisher up bass z fzf

echo Remove plugins. fisher rm thefuck

echo Remove all the plugins. fisher ls | fisher rm

echo Done
