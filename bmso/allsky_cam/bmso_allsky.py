#!/usr/bin/env python3
import cv2
import urllib.request
import numpy as np
from optparse import OptionParser

# Default camera stream url
stream = urllib.request.urlopen('http://192.168.1.204:81/stream')

# Options parsing
parser = OptionParser()
parser.add_option("-u", "--url",
                  dest="url", default="",
                  help="Camera stream url")
parser.add_option("-c", "--create_dark", action="store_true",
                  dest="dark",
                  help="Create a master dark stacking n_darks dark frames. Don't forget to cover the lens!")
parser.add_option("-d", "--dark",
                  dest="dark_path", default="/tmp/bmso_allsky_dark.tif",
                  help="Path of the dark image")
parser.add_option("-n", "--n_darks",
                  dest="n_darks", default="20",
                  help="Number of dark frames to stack")

(options, args) = parser.parse_args()


if options.url != "":
  stream = urllib.request.urlopen(options.url)
n_dark_frames = int(options.n_darks)

# Main
bytes = bytes()
f=0
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        f=f+1
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        if options.dark and f == 1:
            master_dark=i/n_dark_frames
        cv2.imshow('i', i)
        if options.dark:
            master_dark+=i/n_dark_frames
        if cv2.waitKey(1) == 27 or (options.dark == True and f==n_dark_frames):
            if options.dark:
                master_dark = master_dark.astype(np.uint8)
                cv2.imwrite(options.dark_path,master_dark)
            exit(0)
