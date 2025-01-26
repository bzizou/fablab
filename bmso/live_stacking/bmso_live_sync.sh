#/usr/bin/env bash

TELESCOPE_HOST=buzz
WATCH_DIR=/home/bzizou/Pictures
INCOMING_DIR=/home/bzizou/BMSO/live/incomming


echo "Clearing directory: $INCOMING_DIR"
mv $INCOMING_DIR/* $INCOMING_DIR.save/

echo "Watching $TELESCOPE_HOST:$WATCH_DIR"

while [ 1 ]
do
  file=`ssh $TELESCOPE_HOST inotifywait -q -e create -r $WATCH_DIR --format "%w%f"`
  if [ "$file" \!= "" ]
  then
    echo "Getting file $TELESCOPE_HOST:$file ..."
    scp $TELESCOPE_HOST:$file /tmp
    f=`basename $file`
    mv /tmp/$f $INCOMING_DIR/
  else
    sleep 2
  fi
done
