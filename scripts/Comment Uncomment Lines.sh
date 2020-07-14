#!/bin/bash

# your target file
CONFIG=./config.txt

# comment target
comment() {
  sed -i '' "s/^$1/#$1/" $CONFIG
}

# comment target
uncomment() {
  echo $1
  sed -i '' "s/^#$1/$1/" $CONFIG
}


# Use it so:
uncomment enable_uart
comment arm_freq