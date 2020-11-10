# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Other examples:
set -g @plugin 'tmux-plugins/tmux-net-speed'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'tmux-plugins/tmux-battery'
set -g @plugin 'tmux-plugins/tmux-open'

set-option -g @continuum-restore 'on'
set-option -g @continuum-save-interval '8'
set-option -g @resurrect-capture-pane-contents 'on'

# Install: Hit prefix + I to fetch the plugin and source it.
run '~/.tmux/plugins/tpm/tpm'
