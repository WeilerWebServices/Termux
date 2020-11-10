#!/bin/bash

_toggle_mouse() {
  old=$(tmux show -gv mouse)
  new=""

  if [[ "$old" == "on" ]]; then
    new="off"
  else
    new="on"
  fi

  tmux set-option -g mouse $new \; display "mouse: $new"
}

_toggle_mouse