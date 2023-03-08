#!/usr/bin/env bash

#nix-shell /home/bzizou/git/fablab/bmso/allsky_cam/default.nix --run "/home/bzizou/git/fablab/bmso/allsky_cam/bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 60 -G -10 -u http://192.168.1.205:81/stream -t 'http://192.168.1.205/cm?cmnd=Status%208'"
nix-shell /home/bzizou/git/fablab/bmso/allsky_cam/default.nix --run "/home/bzizou/git/fablab/bmso/allsky_cam/bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 10 -G -10 -u http://192.168.1.205:80"
