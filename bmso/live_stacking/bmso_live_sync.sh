#/usr/bin/env bash

TELESCOPE_HOST=buzz
WATCH_DIR=/home/bzizou/Pictures
INCOMING_DIR=/home/bzizou/BMSO/live/incomming/

echo "Watching $TELESCOPE_HOST:$WATCH_DIR"
echo "Incoming directory: $INCOMING_DIR"

while [ 1 ]
do
  file=`ssh $TELESCOPE_HOST inotifywait -q -e create -r $WATCH_DIR --format "%w%f"`
  if [ "$file" \!= "" ]
  then
	  echo "Getting file $TELESCOPE_HOST:$file ..."
	  scp $TELESCOPE_HOST:$file $INCOMING_DIR
  fi
  sleep 2
done
