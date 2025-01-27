#!/usr/bin/env bash
curl "https://newsapi.org/v2/top-headlines?apiKey=4fd864944586438ab3a7b16cd0060001&sources=associated-press" |jq ".articles[] |.title" > /home/bzizou/led_matrix/news_.txt 2>/dev/null
declare -i c=`wc -l /home/bzizou/led_matrix/news_.txt |awk '{print $1}'`
if [ $? -eq 0 -a $c -gt 0 ]
then
  mv -f /home/bzizou/led_matrix/news_.txt /home/bzizou/led_matrix/news.txt
fi
