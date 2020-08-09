#!/system/bin/sh

# Oh-My-Termux

pkg install -y git zsh curl wget

clear

if [ -d "$HOME/.termux" ]; then
 mv $HOME/.termux $HOME/.termux.bak
fi

curl -fsLo $HOME/.termux/colors.properties --create-dirs https://cdn.jsdelivr.net/gh/4679/oh-my-termux@master/.termux/colors.properties

curl -fsLo $HOME/.termux/font.ttf --create-dirs https://cdn.jsdelivr.net/gh/4679/oh-my-termux@master/.termux/font.ttf

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>! ~/.zshrccp $HOME/.oh-my-zsh/templates/zshrc.zsh-template $HOME/.zshrc

sed -i 's/ZSH_THEME="~/powerlevel10k/powerlevel10k.zsh-theme"/' $HOME/.zshrc

chsh -s zsh

termux-setup-storage

echo "Done! Please restart Termux."
