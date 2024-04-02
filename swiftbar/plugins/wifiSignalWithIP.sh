#!/bin/bash

# <xbar.title>Active WIFI Signal</xbar.title>
# <xbar.author>Bryan Stone</xbar.author>
# <xbar.author.github>aegixx</xbar.author.github>
# <xbar.desc>Displays currently connected WIFI Signal</xbar.desc>

# Themes copied from here: http://colorbrewer2.org/
# shellcheck disable=SC2034
# RED_GREEN_THEME=("#d73027" "#fc8d59" "#fee08b" "#ffffbf" "#d9ef8b" "#91cf60" "#1a9850")
# COLORS=("${RED_GREEN_THEME[@]}")

WIFIDATA=$(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I)
SSID=$(echo "$WIFIDATA" | awk '/ SSID/ {print substr($0, index($0, $2))}')
SIGNAL=$(echo "$WIFIDATA" | awk '/ agrCtlRSSI/ {print substr($0, index($0, $2))}')
NOISE=$(echo "$WIFIDATA" | awk '/ agrCtlNoise/ {print substr($0, index($0, $2))}')

SNR="$((SIGNAL - NOISE))"

# Signal Strength – 0dBm (strongest) and --100dBm (weakest). 
## -30 dBm  Amazing
## -50 dBm	Excellent
## -60 dBm	Good
## -67 dBm	Reliable
## -70 dBm	Okay
## -80 dBm	Not Good
## -90 dBm	Unusable
if (("$SIGNAL" >= -30)); then
    RATING="Amazing"
    # COLOR=${COLORS[6]}
elif (("$SIGNAL" >= -50)); then
    RATING="Excellent"
    # COLOR=${COLORS[5]}
elif (("$SIGNAL" >= -60)); then
    RATING="Good"
    # COLOR=${COLORS[4]}
elif (("$SIGNAL" >= -67)); then
    RATING="Reliable"
    # COLOR=${COLORS[3]}
elif (("$SIGNAL" >= -70)); then
    RATING="Okay"
    # COLOR=${COLORS[2]}
elif (("$SIGNAL" >= -80)); then
    RATING="Not Good"
    # COLOR=${COLORS[1]}
elif (("$SIGNAL" >= -90)); then
    RATING="Unusable"
    # COLOR=${COLORS[0]}
else
    RATING="Unknown"
    COLOR="#ccc"
fi

# Signal Quality - quality ~= 2* (dBm + 100)
## High quality: 90% ~= -55dBm
## Medium quality: 50% ~= -75dBm
## Low quality: 30% ~= -85dBm
## Unusable quality: 8% ~= -96dBm
QUALITY="$((2 * SNR))"
QUALITY="$((QUALITY < 100 ? QUALITY : 100))"

# Display local and external IP and allow copying it. This plugin will connect to icanhazip.com to determine external IP address.
#
# by Martin Braun (martin-braun.net)
#

# metadata
# <xbar.title>IPs</xbar.title>
# <xbar.version>v1.0.0</xbar.version>
# <xbar.author>Martin Braun</xbar.author>
# <xbar.author.github>martin-braun</xbar.author.github>
# <xbar.desc>Display local and external IP and allow copying it. This plugin will connect to icanhazip.com to determine external IP address.</xbar.desc>
# <xbar.image>https://i.imgur.com/8eSN3Hw.png</xbar.image>
# 获取本地IP地址
locip=`osascript -e "IPv4 address of (system info)"`
# 获取公网IP地址
pubip=`curl -4s icanhazip.com` > /dev/null

if [[ "$1" = 'copy' ]]; then 
  echo "$2" | tr -d '\n' | pbcopy
fi

echo "$SSID ${locip/192.168./..} | color=$COLOR"

echo "---"
echo "Signal: $SIGNAL dbM ($RATING)"
echo "Quality: $QUALITY% ($SNR dBm SNR)"
echo "---"
echo "Refresh... | refresh=true"

echo "---"
echo "Click on an IP to copy it | font=Tahoma-Bold"
echo "---"
echo "Local:    $locip | font=AndaleMono bash=$0 param1=copy param2=$locip terminal=false refresh=false"
echo "External: $pubip | font=AndaleMono bash=$0 param1=copy param2=$pubip terminal=false refresh=false"
