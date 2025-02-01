#!/usr/bin/env bash

IP=192.168.1.194
LC_TIME=fr_FR.UTF-8
FORTUNES="./sentences.txt"
NEWS_FILE="./news.txt"

urlencode() {
    # urlencode <string>

    old_lc_collate=$LC_COLLATE
    LC_COLLATE=C

    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:$i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf '%s' "$c" ;;
            \') printf '%%27';;
            *) printf '%%%02X' "'$c" ;;
        esac
    done

    LC_COLLATE=$old_lc_collate
}

while [ 1 ]
do
  ### Title	
  curl http://$IP/mode/0 > /dev/null 2>&1
  curl http://$IP/speed/100 > /dev/null 2>&1
  URL=`urlencode "*** BZs's ARCADE ***"`
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 1

  ### Date
  DATE=`date +"%a %d %b %Y - %H:%M"`
  URL=`urlencode "$DATE"`
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/10 > /dev/null 2>&1
  curl http://$IP/speed/20 > /dev/null 2>&1
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 1
  curl http://$IP/mode/0 > /dev/null 2>&1
  sleep 5

  ### Moon
  TXT=`grep phase sunmoon.txt|awk '{print $7 " " $8 " " $9}'`
  URL=`urlencode "$TXT"`
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/7 > /dev/null 2>&1
  curl http://$IP/speed/10 > /dev/null 2>&1
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 0.3
  curl http://$IP/mode/0 > /dev/null 2>&1
  sleep 5

  ### Moon
  RISE=`egrep "Today.*Moon Rise" sunmoon.txt  |awk '{print $5}'`
  SET=`egrep "Today.*Moon Set" sunmoon.txt  |awk '{print $5}'`
  TXT="Moon times: $RISE - $SET"
  URL=`urlencode "$TXT"`
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/11 > /dev/null 2>&1
  curl http://$IP/speed/10 > /dev/null 2>&1
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 1
  curl http://$IP/mode/0 > /dev/null 2>&1
  sleep 5

  ### Sun
  RISE=`egrep "Today.*Sun Rise" sunmoon.txt  |awk '{print $5}'`
  SET=`egrep "Today.*Sun Set" sunmoon.txt  |awk '{print $5}'`
  TXT="Sun times: $RISE - $SET"
  URL=`urlencode "$TXT"`
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/11 > /dev/null 2>&1
  curl http://$IP/speed/10 > /dev/null 2>&1
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 1
  curl http://$IP/mode/0 > /dev/null 2>&1
  sleep 5
 
  ### Fortunes
  #curl http://$IP/text/ > /dev/null 2>&1
  #curl http://$IP/speed/20 > /dev/null 2>&1
  #curl http://$IP/mode/1 > /dev/null 2>&1
  #FORTUNE=`shuf $FORTUNES |head -1`
  #URL=`urlencode "$FORTUNE"`
  #curl http://$IP/text/$URL > /dev/null 2>&1
  #sleep 15

  ### News title
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/12 > /dev/null 2>&1
  curl http://$IP/speed/10 > /dev/null 2>&1
  URL=`urlencode "--- RANDOM TOP NEWS ---"`
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 1

  # News
  curl http://$IP/mode/0 > /dev/null 2>&1
  sleep 1
  curl http://$IP/text/ > /dev/null 2>&1
  curl http://$IP/mode/1 > /dev/null 2>&1
  curl http://$IP/speed/20 > /dev/null 2>&1
  NEWS=`shuf $NEWS_FILE |head -1|sed 's/"//g'`
  URL=`urlencode "$NEWS"`
  curl http://$IP/text/$URL > /dev/null 2>&1
  sleep 20

done

