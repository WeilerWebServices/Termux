# Colours
git config --global color.status auto
git config --global color.branch auto
git config --global color.diff auto

# Short-hand aliases
git config --global alias.st status
git config --global alias.ci commit
git config --global alias.co checkout
git config --global alias.br branch

# Commit without a file (message-only commit)
git config --global alias.msg "commit --allow-empty -m"

# Amend the message of your last commit
git config --global alias.amend "commit --amend"

# Print a list of people next to the number of commits they have
git config --global alias.count "shortlog -sn"

# Undo the last commit, leaving your staging area the same as just before you committed
git config --global alias.undo "reset --soft HEAD^"

# Specify a .gitignore file which applies to every git repo (useful for things like Thumbs.db or .DS_Store)
git config --global core.excludesfile ~/.gitignore_global

# Display UTF-8 characters in filenames, if you're having problems seeing them
git config --global core.quotepath false

# Auto-corrects typos, with a short delay and a warning message (e.g. git cmomit)
git config --global help.autocorrect 1

# Remembers how you handled merging conflicts in a branch, for easier merging later
git config --global rerere.enabled 1