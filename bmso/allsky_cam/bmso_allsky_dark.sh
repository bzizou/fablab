#!/usr/bin/env bash

nix-shell /home/bzizou/git/fablab/bmso/allsky_cam/default.nix --run "/home/bzizou/git/fablab/bmso/allsky_cam/bmso_allsky.py -c -G -10 -u http://192.168.1.205:80"
