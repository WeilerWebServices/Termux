#!/system/bin/sh

# Make Termux terminal look Awesome
# =================================

echo "Color, Font, Style"

echo "Requirements-  curl tool"

apt update -y && apt upgrade -y
clear
apt install curl -

sh -c "$(curl -fsSL https://github.com/Cabbagec/termux-ohmyzsh/raw/master/install.sh)"

echo "wait for complete install and choose any option according to you."

echo "for Example:"

echo "type 0"

echo "and restart termux app"

echo "If you need Change color scheme then type"

echo "~/.termux/colors.sh"

echo "If you need Change font then type"

echo "~/.termux/fonts.sh"
