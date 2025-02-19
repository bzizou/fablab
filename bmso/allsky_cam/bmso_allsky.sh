#!/usr/bin/env bash

export NIX_PATH=nixpkgs=/home/bzizou/.nix-defexpr/channels_root/nixos
#nix-shell /home/bzizou/git/fablab/bmso/allsky_cam/default.nix --run "/home/bzizou/git/fablab/bmso/allsky_cam/bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 10 -G -1 -R -20 -u http://192.168.1.205:80"
nix-shell /home/bzizou/git/fablab/bmso/allsky_cam/default.nix --run "/home/bzizou/git/fablab/bmso/allsky_cam/bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 6 -G -1 -R -20 -u http://192.168.1.205:80"
