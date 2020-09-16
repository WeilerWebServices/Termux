#!/system/bin/sh

# Oh My Fish Install
# ==================

curl -L https://get.oh-my.fish > install
fish install --path=~/.local/share/omf --config=~/.config/omf

# Install with Git
# ================

git clone https://github.com/oh-my-fish/oh-my-fish

cd oh-my-fish

bin/install --offline # with a tarball

curl -L https://get.oh-my.fish > install

fish install --offline=omf.tar.gz
