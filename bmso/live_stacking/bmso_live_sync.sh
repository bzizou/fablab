#/usr/bin/env bash

TELESCOPE_HOST=buzz
WATCH_DIR=/home/bzizou/Pictures
INCOMING_DIR=/home/bzizou/BMSO/live/incoming

while [ 1 ]
do
  file=`ssh $TELESCOPE_HOST inotifywait -q -e create -r $WATCH_DIR --format "%w%f"`
  if [ "$file" \!= "" ]
  then
	  scp $TELESCOPE_HOST:$file $INCOMING_DIR
  fi
  sleep 2
done
