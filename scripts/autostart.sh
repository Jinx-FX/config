#!/bin/bash

# /bin/bash ~/scripts/dwm-status.sh &
# /bin/bash ~/scripts/wp-autochange.sh &

nm-applet &
xflux -l 104E 30N
# redshift &
fcitx &
# picom -o 0.95 -i 0.88 --detect-rounded-corners --vsync --blur-background-fixed -f -D 5 -c -b
picom -b

/bin/bash ~/scripts/setxmodmap.sh &
/bin/bash ~/scripts/wp-change.sh &

# mate-power-manager &
# alsa-utils &

# ~/scripts/autostart_wait.sh &

