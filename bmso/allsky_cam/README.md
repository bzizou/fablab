Example:
--------

# With Arduino IDE (no temp sensor for now):
```
nix-shell
./bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 10 -G -10 -u http://192.168.1.205:80
```

# With Tasmota firmware (temp sensor, but long exposure not really working):
```
nix-shell
./bmso_allsky.py -S /home/bzizou/Pictures/BMSO_all_sky -s 30 -G -10 -u http://192.168.1.205:81/stream -t "http://192.168.1.205/cm?cmnd=Status%208"
```
