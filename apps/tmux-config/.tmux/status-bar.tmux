set-option -g status on         # Enable status bar 
bind-key b set-option status    # Toggle status bar visibility

set-option -g status-style "bg=$FOCUSED_BACKGROUND_COLOR"
set-option -ga status-style "fg=$FOCUSED_TEXT_COLOR"

# Status bar left part
set-option -g status-right-length 10
set-option -g status-left "#{host}❯"
set-window-option -g status-left bg="$DEFAULT_BACKGROUND_COLOR"
set-window-option -g status-left fg="$ACTIVE_TEXT_COLOR"

# Window's Tab
set-window-option -g window-status-format '#{window_index}:#{window_name}'
set-window-option -g window-status-style fg="$DEFAULT_TEXT_COLOR"
set-window-option -g window-status-style bg="$DEFAULT_BACKGROUND_COLOR"

# Active Window's Tab
set-window-option -g window-status-current-format '[#{window_index}:#{window_name}]'
set-window-option -g window-status-current-style bg="$FOCUSED_BACKGROUND_COLOR"
set-window-option -g window-status-current-style fg="$FOCUSED_TEXT_COLOR"
set-window-option -g window-status-current-style "bold"

# Status bar right part
set-option -g @batt_charged_icon "$EMPTY"
set-option -g @batt_charging_icon "$TEXT_WARNING🗲$TEXT_RESET"  # 🗲⚡🔌▴↻↺
set-option -g @batt_attached_icon "$EMPTY"  #
set-option -g @batt_full_charge_icon "$EMPTY"
set-option -g @batt_high_charge_icon "$EMPTY"
set-option -g @batt_medium_charge_icon "$TEXT_WARNING💣$TEXT_RESET"
set-option -g @batt_low_charge_icon "$TEXT_DANGER💣$TEXT_RESET"  # '⬇⬆↯🔋'

set-option -g @net_speed_interfaces "wlp4s0"
set-option -g @download_speed_format "%10s"
set-option -g @upload_speed_format "%10s"
set-option -g @net_speed_format "D:%10s U:%10s"

set-option -g status-right-length 60
set-option -g status-right '⇣#{download_speed} ⇡#{upload_speed} | #{battery_icon}#{battery_percentage} #{battery_graph} | %a %d %b ⌚ %H:%M'