# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

if [ -t 1 ]; then
exec zsh
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

eval ``keychain --eval --agents ssh id_rsa

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\][\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n $ '
else
    PS1='${debian_chroot:+($debian_chroot)}\w\n $ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias l='ls =Aph --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
export DOCKER_HOST=tcp://localhost:2375
export DOCKER_HOST=tcp://localhost:2375

# ALIAS # 
alias cd.='cd ..'
alias cd..='cd ../..'
alias cd...='cd ../../..'
alias l='ls -Aph --color=auto'
alias r='rm -rf'
alias g='git clone'
alias gs='git status'
alias gd='git diff'
alias gdc='git diff --cached'
alias gpl='git pull'
alias gup='git pull --rebase'
alias gp='git push'
alias gc='git commit -a'
alias gc!='git commit -v --amend'
alias gca!='git commit -a --amend'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcm='git checkout master'
alias gr='git remote'
alias grv='git remote -v'
alias grmv='git remote rename'
alias grrm='git remote remove'
alias grset='git remote set-url'
alias grup='git remote update'
alias grbi='git rebase -i'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'
alias gb='git branch'
alias gba='git branch -a'
alias gcount='git shortlog -sn'
alias gcl='git config --list'
alias gcp='git cherry-pick'
alias gl='git log --pretty -n 2 --stat'
alias gl1='git log --pretty=oneline -n 2 --stat'
alias gl2='git log --graph --oneline --decorate --all'
alias gs='git status -u'
alias ga='git add -A'
alias gm='git merge'
alias grh='git reset HEAD'
alias grhh='git reset HEAD --hard'
alias gclean='git reset --hard && git clean -dfx'
alias gwc='git whatchanged -p --abbrev-commit --pretty=medium'
alias gf='git ls-files | grep'
alias gpoat='git push origin --all && git push origin --tags'
alias gmt='git mergetool --no-prompt'
alias gg='git gui citool'
alias gga='git gui citool --amend'
alias gk='gitk --all --branches'
alias gsts='git stash show --text'
alias gsta='git stash'
alias gstp='git stash pop'
alias gstd='git stash drop'
alias grt='cd $(git rev-parse --show-toplevel || echo ".")'
alias git-svn-dcommit-push='git svn dcommit && git push github master:svntrunk'
alias gsr='git svn rebase'
alias gsd='git svn dcommit'
alias diff='diff --color=auto'
alias dmesg='dmesg --color=auto'
alias tree='tree -C'
alias dir='dir --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias ip='ip -c'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color'
alias cower='cower --color=auto'
alias mc='mc -b'
alias mocp='mocp -T blackwhite' . ~/scripts/bash_private.sh
alias gwip='git add -A; git ls-files --deleted -z | xargs -r0 git rm; git commit -m "--wip--"'
alias gunwip='git log -n 1 | grep -q -c "\-\-wip\-\-" && git reset HEAD~1'
alias gignore='git update-index --assume-unchanged'
alias gunignore='git update-index --no-assume-unchanged'
alias gignored='git ls-files -v | grep "^[[:lower:]]"'
alias ggpull='git pull origin $(current_branch)'
alias ggpur='git pull --rebase origin \n$(current_branch)'
alias ggpush='git push origin \n$(current_branch)'
alias ggpnp='git pull origin \n$(current_branch) && git push origin\n $(current_branch)'
alias dir='dir --color=always'
alias vdir='vdir --color=always'
alias grep='grep --color=always'
alias fgrep='fgrep --color=always'
alias egrep='egrep --color=always'
alias c='cat'
alias py='python3'
alias tree='tree -C'
alias mocp='mocp -T blackwhite'
alias mk='mkdir'
alias wpthl='wp theme list'
alias wppll='wp plugin list'
alias cmesg='git diff --name-only'
alias gstore='git config credential.helper store'
alias gl='git log --pretty -n 2 --stat --decorate --all'
alias la="!git config -l | grep alias | cut -c 7-"
alias a='add'
alias ca='commit -a --verbose'
alias ga="!git add -A && git add ."
alias gac='!git add -A && git commit -m'
alias gau='git add --update'
alias gbd='git branch --delete '
alias gc='git commit -m'
alias gcf='git commit --fixup'
alias gcob='git checkout -b'
alias gcom='git checkout master'
alias gcos='git checkout staging'
alias gcod='git checkout develop'
alias gd="git diff -- . ':!*.min.js' ':!*.min.css' ':!*.min-rtl.css'"
alias gda='git diff HEAD'
alias gi='git init'
alias glg='git log --graph --oneline --decorate --all'
alias gld='git log --pretty=format:"%h %ad %s" --date=short --all'
alias gm='git merge --no-ff'
alias gma='git merge --abort'
alias gmc='git merge --continue'
alias gpu='git pull origin'
alias gpr='git pull --rebase'
alias gpp='git push origin'
alias gr='git rebase'
alias gss='git status --short'
alias gst='git stash'
alias gsta='git stash apply'
alias gstl='git stash list'
alias gsts='git stash save'
alias grr='grunt release'
alias grm='grunt minify'
alias pb='phpcs'
alias pbf='phpcbf'
alias hist='history'
alias df="df -h | gawk '{print \$2,\$3,\$4,\$5,\$6}' OFS='\t'"
alias n='nano'
alias less='less -SR'
alias x='exit'
alias notepad="/mnt/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe"
alias pn="/mnt/g/Code/Editor/Programmer's Notepad/pn.exe"
alias np="/mnt/g/Code/Editor/Notepad++/notepad++.exe"
alias cpy='clip.exe'
alias lsr='ls -ahCFR --color=tty'
alias yt='youtube-dl'
alias mp4='youtube-dl mp4 -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
alias mp3='youtube-dl -cit --extract-audio --audio-format mp3 'bestaudio[ext=mp3]/best[ext=mp3]/best'
alias mocp="mocp; mocp -x"
alias clear_cache="sudo paccache -rk0"
alias gpfw="python ~/GitHub/gopro_fw_dl/gopro-fw-dl.py"
alias inotify_increase="echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl --system"
alias fixadb="sudo adb kill-server && sudo adb devices"
alias dmenu_fixed="dmenu_run -fn '-xos4-terminus-medium-r-*-*-14-*' -h 26"
alias cleanphoto="exiftool -all= $*"
alias mv='mv -v'
alias cp='cp -R'
alias meld="'/mnt/g/Code/Editor/MeldPortable' -multiInst -notabbar -nosession -noPlugin"
alias python='/mnt/g/Code/Editor/Python/python.exe'
alias py='/mnt/g/Code/Editor/Python/python.exe'
alias h='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias ~='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias gh='cd /mnt/g/Code/GitHub/ && ls =Aph --color=auto'
alias res='cd /mnt/g/Code/GitHub/WeilerWebServices/Resources/ && ls =Aph --color=auto'
alias wws='cd /mnt/g/Code/GitHub/WeilerWebServices/ && ls =Aph --color=auto'
alias nw='cd /mnt/g/Code/GitHub/NateWeiler && ls =Aph --color=auto'
alias d='cd /mnt/c/Users/natew/Desktop/ && ls =Aph --color=auto'
alias dow='cd /mnt/c/Users/natew/Downloads/ && ls =Aph --color=auto'
alias gedit='stfu gedit'
alias gimp='stfu gimp'
alias chrome='stfu chrome'
alias docker_start='systemctl start docker'
alias docker_debian='docker run -it debian /bin/bash'
alias docker_psh='docker run -it microsoft/powershell'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color=auto'
alias cower='cower --color=auto'
alias msf='./me.sh'
alias p='python3'
alias p3='python3'
alias c='cp -f /sdcard/DCIM/.bashrc $HOME'
alias ip='curl ifconfig.me'
alias ifc='ifconfig wlan0'
alias pu='pkg update -y && pkg upgrade -y'
alias au='apt update -y && apt upgrade -y'
alias uu='au && pu'
alias n='nano'
alias ch='chmod +x'
alias dark='DarkFly'
alias t='Twrp'
alias kali='cd $HOME ./start-kali.sh'
alias ubuntu='cd $HOME ./start-ubuntu.sh'
alias debian='cd $HOME ./start-debian.sh'
alias tool='Tool-X'
alias ip='curl ifconfig.me'
alias hiddeneye='cd $HOME/HiddenEye python3 HiddenEye.py'
alias shell='cd $HOME/shellphish bash shellphish.sh'
alias lazy='cd $HOME/Lazymux python3 lazymux.py'
alias py='python3'
alias py2='python2'
alias py3='python3'
alias python='python3'
alias h='cd ~'
alias webserver='python3 -m http.server 8080'
Nate-Desktop% l
5.0.93.tar.gz  .local/               .sudo_as_admin_successful
.bash/         metasploit.sh         Termux-speak/
.bash_history  .motd_shown           .wget-hsts
.bash_logout   msfvenom              .zcompdump
.bashrc        .oh-my-zsh/           .zcompdump-Nate-Desktop-5.8
.cache/        powerlevel10k/        .zsh_history
.cargo/        .profile              .zshrc
database.yml   .rustup/              .zshrc.pre-oh-my-zsh
.keychain/     .shell.pre-oh-my-zsh
.landscape/    .ssh/
Nate-Desktop% n .bashrc
Nate-Desktop% nano .bash_aliases
Nate-Desktop% source .bash_aliases
/home/hacker/.oh-my-zsh/oh-my-zsh.sh:source:125: no such file or directory: /home/hacker/.oh-my-zsh/themes/powerlevel10k.zsh-theme
/home/hacker/.zshrc:source:287: no such file or directory: /data/data/com.termux/files/home/.zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
Nate-Desktop% cat .bashrc
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

if [ -t 1 ]; then
exec zsh
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

eval ``keychain --eval --agents ssh id_rsa

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\][\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n $ '
else
    PS1='${debian_chroot:+($debian_chroot)}\w\n $ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias l='ls =Aph --color=auto'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'

# Add an "alert" alias for long running commands.  Use like so:
   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
export DOCKER_HOST=tcp://localhost:2375
export DOCKER_HOST=tcp://localhost:2375

# ALIAS # 
alias cd.='cd ..'
alias cd..='cd ../..'
alias cd...='cd ../../..'
alias l='ls -Aph --color=auto'
alias r='rm -rf'
alias g='git clone'
alias gs='git status'
alias gd='git diff'
alias gdc='git diff --cached'
alias gpl='git pull'
alias gup='git pull --rebase'
alias gp='git push'
alias gc='git commit -a'
alias gc!='git commit -v --amend'
alias gca!='git commit -a --amend'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcm='git checkout master'
alias gr='git remote'
alias grv='git remote -v'
alias grmv='git remote rename'
alias grrm='git remote remove'
alias grset='git remote set-url'
alias grup='git remote update'
alias grbi='git rebase -i'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'
alias gb='git branch'
alias gba='git branch -a'
alias gcount='git shortlog -sn'
alias gcl='git config --list'
alias gcp='git cherry-pick'
alias gl='git log --pretty -n 2 --stat'
alias gl1='git log --pretty=oneline -n 2 --stat'
alias gl2='git log --graph --oneline --decorate --all'
alias gs='git status -u'
alias ga='git add -A'
alias gm='git merge'
alias grh='git reset HEAD'
alias grhh='git reset HEAD --hard'
alias gclean='git reset --hard && git clean -dfx'
alias gwc='git whatchanged -p --abbrev-commit --pretty=medium'
alias gf='git ls-files | grep'
alias gpoat='git push origin --all && git push origin --tags'
alias gmt='git mergetool --no-prompt'
alias gg='git gui citool'
alias gga='git gui citool --amend'
alias gk='gitk --all --branches'
alias gsts='git stash show --text'
alias gsta='git stash'
alias gstp='git stash pop'
alias gstd='git stash drop'
alias grt='cd $(git rev-parse --show-toplevel || echo ".")'
alias git-svn-dcommit-push='git svn dcommit && git push github master:svntrunk'
alias gsr='git svn rebase'
alias gsd='git svn dcommit'
alias diff='diff --color=auto'
alias dmesg='dmesg --color=auto'
alias tree='tree -C'
alias dir='dir --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias ip='ip -c'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color'
alias cower='cower --color=auto'
alias mc='mc -b'
alias mocp='mocp -T blackwhite' . ~/scripts/bash_private.sh
alias gwip='git add -A; git ls-files --deleted -z | xargs -r0 git rm; git commit -m "--wip--"'
alias gunwip='git log -n 1 | grep -q -c "\-\-wip\-\-" && git reset HEAD~1'
alias gignore='git update-index --assume-unchanged'
alias gunignore='git update-index --no-assume-unchanged'
alias gignored='git ls-files -v | grep "^[[:lower:]]"'
alias ggpull='git pull origin $(current_branch)'
alias ggpur='git pull --rebase origin \n$(current_branch)'
alias ggpush='git push origin \n$(current_branch)'
alias ggpnp='git pull origin \n$(current_branch) && git push origin\n $(current_branch)'
alias dir='dir --color=always'
alias vdir='vdir --color=always'
alias grep='grep --color=always'
alias fgrep='fgrep --color=always'
alias egrep='egrep --color=always'
alias c='cat'
alias py='python3'
alias tree='tree -C'
alias mocp='mocp -T blackwhite'
alias mk='mkdir'
alias wpthl='wp theme list'
alias wppll='wp plugin list'
alias cmesg='git diff --name-only'
alias gstore='git config credential.helper store'
alias gl='git log --pretty -n 2 --stat --decorate --all'
alias la="!git config -l | grep alias | cut -c 7-"
alias a='add'
alias ca='commit -a --verbose'
alias ga="!git add -A && git add ."
alias gac='!git add -A && git commit -m'
alias gau='git add --update'
alias gbd='git branch --delete '
alias gc='git commit -m'
alias gcf='git commit --fixup'
alias gcob='git checkout -b'
alias gcom='git checkout master'
alias gcos='git checkout staging'
alias gcod='git checkout develop'
alias gd="git diff -- . ':!*.min.js' ':!*.min.css' ':!*.min-rtl.css'"
alias gda='git diff HEAD'
alias gi='git init'
alias glg='git log --graph --oneline --decorate --all'
alias gld='git log --pretty=format:"%h %ad %s" --date=short --all'
alias gm='git merge --no-ff'
alias gma='git merge --abort'
alias gmc='git merge --continue'
alias gpu='git pull origin'
alias gpr='git pull --rebase'
alias gpp='git push origin'
alias gr='git rebase'
alias gss='git status --short'
alias gst='git stash'
alias gsta='git stash apply'
alias gstl='git stash list'
alias gsts='git stash save'
alias grr='grunt release'
alias grm='grunt minify'
alias pb='phpcs'
alias pbf='phpcbf'
alias hist='history'
alias df="df -h | gawk '{print \$2,\$3,\$4,\$5,\$6}' OFS='\t'"
alias n='nano'
alias less='less -SR'
alias x='exit'
alias notepad="/mnt/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe"
alias pn="/mnt/g/Code/Editor/Programmer's Notepad/pn.exe"
alias np="/mnt/g/Code/Editor/Notepad++/notepad++.exe"
alias cpy='clip.exe'
alias lsr='ls -ahCFR --color=tty'
alias yt='youtube-dl'
alias mp4='youtube-dl mp4 -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
alias mp3='youtube-dl -cit --extract-audio --audio-format mp3 'bestaudio[ext=mp3]/best[ext=mp3]/best'
alias mocp="mocp; mocp -x"
alias clear_cache="sudo paccache -rk0"
alias gpfw="python ~/GitHub/gopro_fw_dl/gopro-fw-dl.py"
alias inotify_increase="echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl --system"
alias fixadb="sudo adb kill-server && sudo adb devices"
alias dmenu_fixed="dmenu_run -fn '-xos4-terminus-medium-r-*-*-14-*' -h 26"
alias cleanphoto="exiftool -all= $*"
alias mv='mv -v'
alias cp='cp -R'
alias meld="'/mnt/g/Code/Editor/MeldPortable' -multiInst -notabbar -nosession -noPlugin"
alias python='/mnt/g/Code/Editor/Python/python.exe'
alias py='/mnt/g/Code/Editor/Python/python.exe'
alias h='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias ~='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias gh='cd /mnt/g/Code/GitHub/ && ls =Aph --color=auto'
alias res='cd /mnt/g/Code/GitHub/WeilerWebServices/Resources/ && ls =Aph --color=auto'
alias wws='cd /mnt/g/Code/GitHub/WeilerWebServices/ && ls =Aph --color=auto'
alias nw='cd /mnt/g/Code/GitHub/NateWeiler && ls =Aph --color=auto'
alias d='cd /mnt/c/Users/natew/Desktop/ && ls =Aph --color=auto'
alias dow='cd /mnt/c/Users/natew/Downloads/ && ls =Aph --color=auto'
alias gedit='stfu gedit'
alias gimp='stfu gimp'
alias chrome='stfu chrome'
alias docker_start='systemctl start docker'
alias docker_debian='docker run -it debian /bin/bash'
alias docker_psh='docker run -it microsoft/powershell'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color=auto'
alias cower='cower --color=auto'
alias msf='./me.sh'
alias p='python3'
alias p3='python3'
alias c='cp -f /sdcard/DCIM/.bashrc $HOME'
alias ip='curl ifconfig.me'
alias ifc='ifconfig wlan0'
alias pu='pkg update -y && pkg upgrade -y'
alias au='apt update -y && apt upgrade -y'
alias uu='au && pu'
alias n='nano'
alias ch='chmod +x'
alias dark='DarkFly'
alias t='Twrp'
alias kali='cd $HOME ./start-kali.sh'
alias ubuntu='cd $HOME ./start-ubuntu.sh'
alias debian='cd $HOME ./start-debian.sh'
alias tool='Tool-X'
alias ip='curl ifconfig.me'
alias hiddeneye='cd $HOME/HiddenEye python3 HiddenEye.py'
alias shell='cd $HOME/shellphish bash shellphish.sh'
alias lazy='cd $HOME/Lazymux python3 lazymux.py'
alias py='python3'
alias py2='python2'
alias py3='python3'
alias python='python3'
alias h='cd ~'
alias webserver='python3 -m http.server 8080'# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

if [ -t 1 ]; then
exec zsh
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

eval ``keychain --eval --agents ssh id_rsa

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\][\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n $ '
else
    PS1='${debian_chroot:+($debian_chroot)}\w\n $ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias l='ls =Aph --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
export DOCKER_HOST=tcp://localhost:2375
export DOCKER_HOST=tcp://localhost:2375

# ALIAS # 
alias cd.='cd ..'
alias cd..='cd ../..'
alias cd...='cd ../../..'
alias l='ls -Aph --color=auto'
alias r='rm -rf'
alias g='git clone'
alias gs='git status'
alias gd='git diff'
alias gdc='git diff --cached'
alias gpl='git pull'
alias gup='git pull --rebase'
alias gp='git push'
alias gc='git commit -a'
alias gc!='git commit -v --amend'
alias gca!='git commit -a --amend'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcm='git checkout master'
alias gr='git remote'
alias grv='git remote -v'
alias grmv='git remote rename'
alias grrm='git remote remove'
alias grset='git remote set-url'
alias grup='git remote update'
alias grbi='git rebase -i'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'
alias gb='git branch'
alias gba='git branch -a'
alias gcount='git shortlog -sn'
alias gcl='git config --list'
alias gcp='git cherry-pick'
alias gl='git log --pretty -n 2 --stat'
alias gl1='git log --pretty=oneline -n 2 --stat'
alias gl2='git log --graph --oneline --decorate --all'
alias gs='git status -u'
alias ga='git add -A'
alias gm='git merge'
alias grh='git reset HEAD'
alias grhh='git reset HEAD --hard'
alias gclean='git reset --hard && git clean -dfx'
alias gwc='git whatchanged -p --abbrev-commit --pretty=medium'
alias gf='git ls-files | grep'
alias gpoat='git push origin --all && git push origin --tags'
alias gmt='git mergetool --no-prompt'
alias gg='git gui citool'
alias gga='git gui citool --amend'
alias gk='gitk --all --branches'
alias gsts='git stash show --text'
alias gsta='git stash'
alias gstp='git stash pop'
alias gstd='git stash drop'
alias grt='cd $(git rev-parse --show-toplevel || echo ".")'
alias git-svn-dcommit-push='git svn dcommit && git push github master:svntrunk'
alias gsr='git svn rebase'
alias gsd='git svn dcommit'
alias diff='diff --color=auto'
alias dmesg='dmesg --color=auto'
alias tree='tree -C'
alias dir='dir --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias ip='ip -c'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color'
alias cower='cower --color=auto'
alias mc='mc -b'
alias mocp='mocp -T blackwhite' . ~/scripts/bash_private.sh
alias gwip='git add -A; git ls-files --deleted -z | xargs -r0 git rm; git commit -m "--wip--"'
alias gunwip='git log -n 1 | grep -q -c "\-\-wip\-\-" && git reset HEAD~1'
alias gignore='git update-index --assume-unchanged'
alias gunignore='git update-index --no-assume-unchanged'
alias gignored='git ls-files -v | grep "^[[:lower:]]"'
alias ggpull='git pull origin $(current_branch)'
alias ggpur='git pull --rebase origin \n$(current_branch)'
alias ggpush='git push origin \n$(current_branch)'
alias ggpnp='git pull origin \n$(current_branch) && git push origin\n $(current_branch)'
alias dir='dir --color=always'
alias vdir='vdir --color=always'
alias grep='grep --color=always'
alias fgrep='fgrep --color=always'
alias egrep='egrep --color=always'
alias c='cat'
alias py='python3'
alias tree='tree -C'
alias mocp='mocp -T blackwhite'
alias mk='mkdir'
alias wpthl='wp theme list'
alias wppll='wp plugin list'
alias cmesg='git diff --name-only'
alias gstore='git config credential.helper store'
alias gl='git log --pretty -n 2 --stat --decorate --all'
alias la="!git config -l | grep alias | cut -c 7-"
alias a='add'
alias ca='commit -a --verbose'
alias ga="!git add -A && git add ."
alias gac='!git add -A && git commit -m'
alias gau='git add --update'
alias gbd='git branch --delete '
alias gc='git commit -m'
alias gcf='git commit --fixup'
alias gcob='git checkout -b'
alias gcom='git checkout master'
alias gcos='git checkout staging'
alias gcod='git checkout develop'
alias gd="git diff -- . ':!*.min.js' ':!*.min.css' ':!*.min-rtl.css'"
alias gda='git diff HEAD'
alias gi='git init'
alias glg='git log --graph --oneline --decorate --all'
alias gld='git log --pretty=format:"%h %ad %s" --date=short --all'
alias gm='git merge --no-ff'
alias gma='git merge --abort'
alias gmc='git merge --continue'
alias gpu='git pull origin'
alias gpr='git pull --rebase'
alias gpp='git push origin'
alias gr='git rebase'
alias gss='git status --short'
alias gst='git stash'
alias gsta='git stash apply'
alias gstl='git stash list'
alias gsts='git stash save'
alias grr='grunt release'
alias grm='grunt minify'
alias pb='phpcs'
alias pbf='phpcbf'
alias hist='history'
alias df="df -h | gawk '{print \$2,\$3,\$4,\$5,\$6}' OFS='\t'"
alias n='nano'
alias less='less -SR'
alias x='exit'
alias notepad="/mnt/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe"
alias pn="/mnt/g/Code/Editor/Programmer's Notepad/pn.exe"
alias np="/mnt/g/Code/Editor/Notepad++/notepad++.exe"
alias cpy='clip.exe'
alias lsr='ls -ahCFR --color=tty'
alias yt='youtube-dl'
alias mp4='youtube-dl mp4 -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
alias mp3='youtube-dl -cit --extract-audio --audio-format mp3 'bestaudio[ext=mp3]/best[ext=mp3]/best'
alias mocp="mocp; mocp -x"
alias clear_cache="sudo paccache -rk0"
alias gpfw="python ~/GitHub/gopro_fw_dl/gopro-fw-dl.py"
alias inotify_increase="echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl --system"
alias fixadb="sudo adb kill-server && sudo adb devices"
alias dmenu_fixed="dmenu_run -fn '-xos4-terminus-medium-r-*-*-14-*' -h 26"
alias cleanphoto="exiftool -all= $*"
alias mv='mv -v'
alias cp='cp -R'
alias meld="'/mnt/g/Code/Editor/MeldPortable' -multiInst -notabbar -nosession -noPlugin"
alias python='/mnt/g/Code/Editor/Python/python.exe'
alias py='/mnt/g/Code/Editor/Python/python.exe'
alias h='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias ~='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias gh='cd /mnt/g/Code/GitHub/ && ls =Aph --color=auto'
alias res='cd /mnt/g/Code/GitHub/WeilerWebServices/Resources/ && ls =Aph --color=auto'
alias wws='cd /mnt/g/Code/GitHub/WeilerWebServices/ && ls =Aph --color=auto'
alias nw='cd /mnt/g/Code/GitHub/NateWeiler && ls =Aph --color=auto'
alias d='cd /mnt/c/Users/natew/Desktop/ && ls =Aph --color=auto'
alias dow='cd /mnt/c/Users/natew/Downloads/ && ls =Aph --color=auto'
alias gedit='stfu gedit'
alias gimp='stfu gimp'
alias chrome='stfu chrome'
alias docker_start='systemctl start docker'
alias docker_debian='docker run -it debian /bin/bash'
alias docker_psh='docker run -it microsoft/powershell'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color=auto'
alias cower='cower --color=auto'
alias msf='./me.sh'
alias p='python3'
alias p3='python3'
alias c='cp -f /sdcard/DCIM/.bashrc $HOME'
alias ip='curl ifconfig.me'
alias ifc='ifconfig wlan0'
alias pu='pkg update -y && pkg upgrade -y'
alias au='apt update -y && apt upgrade -y'
alias uu='au && pu'
alias n='nano'
alias ch='chmod +x'
alias dark='DarkFly'
alias t='Twrp'
alias kali='cd $HOME ./start-kali.sh'
alias ubuntu='cd $HOME ./start-ubuntu.sh'
alias debian='cd $HOME ./start-debian.sh'
alias tool='Tool-X'
alias ip='curl ifconfig.me'
alias hiddeneye='cd $HOME/HiddenEye python3 HiddenEye.py'
alias shell='cd $HOME/shellphish bash shellphish.sh'
alias lazy='cd $HOME/Lazymux python3 lazymux.py'
alias py='python3'
alias py2='python2'
alias py3='python3'
alias python='python3'
alias h='cd ~'
alias webserver='python3 -m http.server 8080'
Nate-Desktop% l
5.0.93.tar.gz  .local/               .sudo_as_admin_successful
.bash/         metasploit.sh         Termux-speak/
.bash_history  .motd_shown           .wget-hsts
.bash_logout   msfvenom              .zcompdump
.bashrc        .oh-my-zsh/           .zcompdump-Nate-Desktop-5.8
.cache/        powerlevel10k/        .zsh_history
.cargo/        .profile              .zshrc
database.yml   .rustup/              .zshrc.pre-oh-my-zsh
.keychain/     .shell.pre-oh-my-zsh
.landscape/    .ssh/
Nate-Desktop% n .bashrc
Nate-Desktop% nano .bash_aliases
Nate-Desktop% source .bash_aliases
/home/hacker/.oh-my-zsh/oh-my-zsh.sh:source:125: no such file or directory: /home/hacker/.oh-my-zsh/themes/powerlevel10k.zsh-theme
/home/hacker/.zshrc:source:287: no such file or directory: /data/data/com.termux/files/home/.zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
Nate-Desktop% cat .bashrc
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

if [ -t 1 ]; then
exec zsh
fi

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

eval ``keychain --eval --agents ssh id_rsa

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\][\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n $ '
else
    PS1='${debian_chroot:+($debian_chroot)}\w\n $ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias l='ls =Aph --color=auto'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'

# Add an "alert" alias for long running commands.  Use like so:
   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
export DOCKER_HOST=tcp://localhost:2375
export DOCKER_HOST=tcp://localhost:2375

# ALIAS # 
alias cd.='cd ..'
alias cd..='cd ../..'
alias cd...='cd ../../..'
alias l='ls -Aph --color=auto'
alias r='rm -rf'
alias g='git clone'
alias gs='git status'
alias gd='git diff'
alias gdc='git diff --cached'
alias gpl='git pull'
alias gup='git pull --rebase'
alias gp='git push'
alias gc='git commit -a'
alias gc!='git commit -v --amend'
alias gca!='git commit -a --amend'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcm='git checkout master'
alias gr='git remote'
alias grv='git remote -v'
alias grmv='git remote rename'
alias grrm='git remote remove'
alias grset='git remote set-url'
alias grup='git remote update'
alias grbi='git rebase -i'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'
alias gb='git branch'
alias gba='git branch -a'
alias gcount='git shortlog -sn'
alias gcl='git config --list'
alias gcp='git cherry-pick'
alias gl='git log --pretty -n 2 --stat'
alias gl1='git log --pretty=oneline -n 2 --stat'
alias gl2='git log --graph --oneline --decorate --all'
alias gs='git status -u'
alias ga='git add -A'
alias gm='git merge'
alias grh='git reset HEAD'
alias grhh='git reset HEAD --hard'
alias gclean='git reset --hard && git clean -dfx'
alias gwc='git whatchanged -p --abbrev-commit --pretty=medium'
alias gf='git ls-files | grep'
alias gpoat='git push origin --all && git push origin --tags'
alias gmt='git mergetool --no-prompt'
alias gg='git gui citool'
alias gga='git gui citool --amend'
alias gk='gitk --all --branches'
alias gsts='git stash show --text'
alias gsta='git stash'
alias gstp='git stash pop'
alias gstd='git stash drop'
alias grt='cd $(git rev-parse --show-toplevel || echo ".")'
alias git-svn-dcommit-push='git svn dcommit && git push github master:svntrunk'
alias gsr='git svn rebase'
alias gsd='git svn dcommit'
alias diff='diff --color=auto'
alias dmesg='dmesg --color=auto'
alias tree='tree -C'
alias dir='dir --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias ip='ip -c'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color'
alias cower='cower --color=auto'
alias mc='mc -b'
alias mocp='mocp -T blackwhite' . ~/scripts/bash_private.sh
alias gwip='git add -A; git ls-files --deleted -z | xargs -r0 git rm; git commit -m "--wip--"'
alias gunwip='git log -n 1 | grep -q -c "\-\-wip\-\-" && git reset HEAD~1'
alias gignore='git update-index --assume-unchanged'
alias gunignore='git update-index --no-assume-unchanged'
alias gignored='git ls-files -v | grep "^[[:lower:]]"'
alias ggpull='git pull origin $(current_branch)'
alias ggpur='git pull --rebase origin \n$(current_branch)'
alias ggpush='git push origin \n$(current_branch)'
alias ggpnp='git pull origin \n$(current_branch) && git push origin\n $(current_branch)'
alias dir='dir --color=always'
alias vdir='vdir --color=always'
alias grep='grep --color=always'
alias fgrep='fgrep --color=always'
alias egrep='egrep --color=always'
alias c='cat'
alias py='python3'
alias tree='tree -C'
alias mocp='mocp -T blackwhite'
alias mk='mkdir'
alias wpthl='wp theme list'
alias wppll='wp plugin list'
alias cmesg='git diff --name-only'
alias gstore='git config credential.helper store'
alias gl='git log --pretty -n 2 --stat --decorate --all'
alias la="!git config -l | grep alias | cut -c 7-"
alias a='add'
alias ca='commit -a --verbose'
alias ga="!git add -A && git add ."
alias gac='!git add -A && git commit -m'
alias gau='git add --update'
alias gbd='git branch --delete '
alias gc='git commit -m'
alias gcf='git commit --fixup'
alias gcob='git checkout -b'
alias gcom='git checkout master'
alias gcos='git checkout staging'
alias gcod='git checkout develop'
alias gd="git diff -- . ':!*.min.js' ':!*.min.css' ':!*.min-rtl.css'"
alias gda='git diff HEAD'
alias gi='git init'
alias glg='git log --graph --oneline --decorate --all'
alias gld='git log --pretty=format:"%h %ad %s" --date=short --all'
alias gm='git merge --no-ff'
alias gma='git merge --abort'
alias gmc='git merge --continue'
alias gpu='git pull origin'
alias gpr='git pull --rebase'
alias gpp='git push origin'
alias gr='git rebase'
alias gss='git status --short'
alias gst='git stash'
alias gsta='git stash apply'
alias gstl='git stash list'
alias gsts='git stash save'
alias grr='grunt release'
alias grm='grunt minify'
alias pb='phpcs'
alias pbf='phpcbf'
alias hist='history'
alias df="df -h | gawk '{print \$2,\$3,\$4,\$5,\$6}' OFS='\t'"
alias n='nano'
alias less='less -SR'
alias x='exit'
alias notepad="/mnt/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe"
alias pn="/mnt/g/Code/Editor/Programmer's Notepad/pn.exe"
alias np="/mnt/g/Code/Editor/Notepad++/notepad++.exe"
alias cpy='clip.exe'
alias lsr='ls -ahCFR --color=tty'
alias yt='youtube-dl'
alias mp4='youtube-dl mp4 -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
alias mp3='youtube-dl -cit --extract-audio --audio-format mp3 'bestaudio[ext=mp3]/best[ext=mp3]/best'
alias mocp="mocp; mocp -x"
alias clear_cache="sudo paccache -rk0"
alias gpfw="python ~/GitHub/gopro_fw_dl/gopro-fw-dl.py"
alias inotify_increase="echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl --system"
alias fixadb="sudo adb kill-server && sudo adb devices"
alias dmenu_fixed="dmenu_run -fn '-xos4-terminus-medium-r-*-*-14-*' -h 26"
alias cleanphoto="exiftool -all= $*"
alias mv='mv -v'
alias cp='cp -R'
alias meld="'/mnt/g/Code/Editor/MeldPortable' -multiInst -notabbar -nosession -noPlugin"
alias python='/mnt/g/Code/Editor/Python/python.exe'
alias py='/mnt/g/Code/Editor/Python/python.exe'
alias h='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias ~='cd /mnt/c/Users/natew && ls =Aph --color=auto'
alias gh='cd /mnt/g/Code/GitHub/ && ls =Aph --color=auto'
alias res='cd /mnt/g/Code/GitHub/WeilerWebServices/Resources/ && ls =Aph --color=auto'
alias wws='cd /mnt/g/Code/GitHub/WeilerWebServices/ && ls =Aph --color=auto'
alias nw='cd /mnt/g/Code/GitHub/NateWeiler && ls =Aph --color=auto'
alias d='cd /mnt/c/Users/natew/Desktop/ && ls =Aph --color=auto'
alias dow='cd /mnt/c/Users/natew/Downloads/ && ls =Aph --color=auto'
alias gedit='stfu gedit'
alias gimp='stfu gimp'
alias chrome='stfu chrome'
alias docker_start='systemctl start docker'
alias docker_debian='docker run -it debian /bin/bash'
alias docker_psh='docker run -it microsoft/powershell'
alias pcregrep='pcregrep --color=auto'
alias vdir='vdir --color=auto'
alias watch='watch --color=auto'
alias cower='cower --color=auto'
alias msf='./me.sh'
alias p='python3'
alias p3='python3'
alias c='cp -f /sdcard/DCIM/.bashrc $HOME'
alias ip='curl ifconfig.me'
alias ifc='ifconfig wlan0'
alias pu='pkg update -y && pkg upgrade -y'
alias au='apt update -y && apt upgrade -y'
alias uu='au && pu'
alias n='nano'
alias ch='chmod +x'
alias dark='DarkFly'
alias t='Twrp'
alias kali='cd $HOME ./start-kali.sh'
alias ubuntu='cd $HOME ./start-ubuntu.sh'
alias debian='cd $HOME ./start-debian.sh'
alias tool='Tool-X'
alias ip='curl ifconfig.me'
alias hiddeneye='cd $HOME/HiddenEye python3 HiddenEye.py'
alias shell='cd $HOME/shellphish bash shellphish.sh'
alias lazy='cd $HOME/Lazymux python3 lazymux.py'
alias py='python3'
alias py2='python2'
alias py3='python3'
alias python='python3'
alias h='cd ~'
alias webserver='python3 -m http.server 8080'