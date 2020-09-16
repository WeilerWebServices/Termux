#!/system/bin/sh

# Oh-My-Termux Install
# ====================

pkg install -y libcurl git zsh curl wget

bash -c "$(curl -fsSL https://git.io/oh-my-termux)"
