# PANES

# set first pane to index 1 (not 0) to map more to the keyboard layout...
set-option -g pane-base-index 1

# confirm before killing a window or the server
bind-key q kill-pane


# Automatic layouting: https://wiki.archlinux.org/index.php/Tmux#Automatic_layouting
bind -n M-c kill-pane \; select-layout
bind -n M-n split-window \; select-layout

# Pane splitting
unbind "%";   bind | split-window -h -c '#{pane_current_path}'    # split vertically
unbind '"'; bind - split-window -v -c '#{pane_current_path}'    # split horizontally 

# Pane switching with Alt+arrow
bind -n M-Left select-pane -L   # Alt+⯇
bind -n M-Right select-pane -R  # Alt+⯈
bind -n M-Up select-pane -U     # Alt+⯅
bind -n M-Down select-pane -D   # Alt+⯆

# Default pane style
set-option -g pane-border-style "bg=$INACTIVE_BACKGROUND_COLOR"
set-option -ga pane-border-style "fg=$INACTIVE_TEXT_COLOR"
# Active pane style
set-option -g pane-active-border-style "bg=$FOCUSED_BACKGROUND_COLOR"
set-option -ga pane-active-border-style "fg=$ACTIVE_BORDER_COLOR"
