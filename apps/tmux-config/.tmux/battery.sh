#!/bin/bash

BATTERY_FULL_FG="#b3ff99"   # light green
BATTERY_EMPTY_FG="#ffffff"  # light red
ICON_FULL_BATTERY="◼"
ICON_EMPTY_BATTERY="◻"
ICON_CHARGING_BATTERY="🔌"
ICON_DISCHARGING_BATTERY="↯"

function get_battery_status_icon() {
    discharging="$(grep --count --ignore discharging $battery/status)"

    if (( $discharging == 1 )); then 
        status_icon="$ICON_DISCHARGING_BATTERY"
    else 
        status_icon=$ICON_CHARGING_BATTERY
    fi

    echo "$status_icon"
}

function get_battery_bar_length() {
    columns=$(tmux -q display -p '#{client_width}' 2> /dev/null || echo 80)

    if (( $columns >= 80)); then
        bar_length=10
    else
        bar_length=5
    fi

    echo "$bar_length"
}

function get_battery_bar() {
    full=$(awk "BEGIN { printf \"%.0f\", $batter_charge / 100 * $battery_bar_length }")

    if (( "$full" > 0 )); then
        battery_bar="$battery_bar#[fg=$BATTERY_FULL_FG]$(printf "%0.s$ICON_FULL_BATTERY" $(seq 1 "$full"))"
    fi

    empty=$(( $battery_bar_length - $full))
    if (( "$empty" > 0 )); then
        battery_bar="$battery_bar#[fg=$BATTERY_EMPTY_FG]$(printf "%0.s$ICON_EMPTY_BATTERY" $(seq 1 "$empty"))"
        battery_bar="$battery_bar#[fg=$BATTERY_EMPTY_FG]"
    fi

    echo "$battery_bar"
}

_battery() {
    battery="$(find /sys/class/power_supply -maxdepth 1 -iname '*bat*')"
    batter_charge=$(<"$battery/capacity")

    if (("$batter_charge" == 0)); then
        tmux  set -ug '@battery_status'  \;\
        set -ug '@battery_bar'     \;\
        set -ug '@battery_percentage'
      return
    fi

    battery_status_icon="$(get_battery_status_icon)"
    battery_bar_length="$(get_battery_bar_length)"
    battery_bar="$(get_battery_bar)"

    tmux    set -g '@battery_status' $battery_status_icon \;\
            set -g '@battery_bar' "$battery_bar" \;\
            set -g '@battery_percentage' "$batter_charge"
}

_battery