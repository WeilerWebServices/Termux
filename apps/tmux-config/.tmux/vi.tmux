# VI Configuration

set-option -g status-keys vi

# Vim-style copy/paste
set-window-option -g mode-keys vi

# Allow mouse interaction
bind m run "bash $HOME/.tmux/toggle-mouse.sh"
set -g mouse on
bind [ copy-mode  # enable vi copy-mode

unbind -T copy-mode-vi MouseDragEnd1Pane  # keep copy mode active after mouse up (see https://github.com/tmux/tmux/issues/140)
bind -T root MouseDown2Pane run -b "xclip -o | tmux load-buffer - && tmux paste-buffer -s ' '"
set -g @yank_action 'copy-pipe' # keep selection after mouse-up

# copy selection using [Enter]
unbind Enter; bind -T copy-mode-vi Enter send-keys -X copy-pipe-and-cancel 'xclip -in -selection clipboard'