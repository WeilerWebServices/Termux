# WINDOWS

set-window-option -g automatic-rename on    # Rename window to reflect current program
set-option -g renumber-windows on                  # Renumber windows when a window is closed

# Allow the title bar to adapt to whatever host you connect to: https://wiki.archlinux.org/index.php/Tmux#Terminal_emulator_window_titles
set-option -g set-titles on

# set first window to index 1 (not 0) to map more to the keyboard layout...
set-option -g base-index 1
# confirm before killing a window or the server
bind-key k confirm kill-window
bind-key K confirm kill-server

set-window-option -g window-style "bg=$INACTIVE_BACKGROUND_COLOR"
set-window-option -ga window-style "fg=$INACTIVE_TEXT_COLOR"
set-window-option -g window-active-style "bg=$FOCUSED_BACKGROUND_COLOR"
set-window-option -ga window-active-style "fg=$FOCUSED_TEXT_COLOR"

# Firefox-like shortcuts for tabs/windows
bind-key -n C-t new-window -c '#{pane_current_path}'    # Ctrl+T: new window 
bind-key -n C-PPage previous-window                     # Ctrl+Page up ⯅
bind-key -n C-NPage next-window                         # Ctrl+Page down ⯆
# Tab Navigation: Alt+<NUMBER>
unbind M-0; bind-key -n M-0 select-window -t :0         # Alt+0: swtich to tab 0
unbind M-1; bind-key -n M-1 select-window -t :1         # Alt+1: swtich to tab 1
unbind M-2; bind-key -n M-2 select-window -t :2         # Alt+2: swtich to tab 2
unbind M-3; bind-key -n M-3 select-window -t :3         # Alt+3: swtich to tab 3
unbind M-4; bind-key -n M-4 select-window -t :4         # Alt+4: swtich to tab 4
unbind M-5; bind-key -n M-5 select-window -t :5         # Alt+5: swtich to tab 5
unbind M-6; bind-key -n M-6 select-window -t :6         # Alt+6: swtich to tab 6
unbind M-7; bind-key -n M-7 select-window -t :7         # Alt+7: swtich to tab 7
unbind M-8; bind-key -n M-8 select-window -t :8         # Alt+0: swtich to tab 0
unbind M-9; bind-key -n M-9 select-window -t :9         # Alt+9: swtich to tab 9
