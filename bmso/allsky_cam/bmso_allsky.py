#!/usr/bin/env python3
import cv2
import urllib.request
import numpy as np
from optparse import OptionParser
from os import path

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
                  dest="dark_path", default="/tmp/bmso_allsky_dark.npy",
                  help="Path of the dark image")
parser.add_option("-n", "--n_darks",
                  dest="n_darks", default="20",
                  help="Number of dark frames to stack")
parser.add_option("-s", "--stack_size",
                  dest="stack_size", default="20",
                  help="Number of frames to stack")

(options, args) = parser.parse_args()


if options.url != "":
  stream = urllib.request.urlopen(options.url)
n_dark_frames = int(options.n_darks)
stack_size = int(options.stack_size)

# Load dark master if exists
dark_loaded=False
if path.exists(options.dark_path) and not options.dark:
  print("Loading master dark "+options.dark_path)
  #dark_i=cv2.imread(options.dark_path,-1)
  #dark_i = dark_i.astype(np.uint16)
  dark_i=np.load(options.dark_path)
  dark_loaded=True
if options.dark:
  print ("Don't forget to cover the camera for dark creation!")
  print ("Creating master dark...")

# Main
bytes = bytes()
f=0
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        f=f+1

        # Decode image
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Convert to 16 bits image
        i2 = i.astype(np.uint16)
        cv2.normalize(i2,i,0,65535,cv2.NORM_MINMAX)

        # Stacking 
        if options.dark:
            if f == 1:
                master_dark=i/n_dark_frames
            else:
              master_dark+=i/n_dark_frames
        else:
            print("Stacking...")
            if dark_loaded:
                i=i-dark_i
            if f == 1:
              stacked_i=i/stack_size
            else:
              stacked_i+=i/stack_size
            if f==stack_size:
                f=0
                # Convert back to 8 bits and display
                stacked_8bits=stacked_i
                cv2.normalize(stacked_i,stacked_8bits,0,255,cv2.NORM_MINMAX)
                print("Displaying...")
                cv2.imshow('BMSO Allsky', stacked_8bits.astype(np.uint8))
        if cv2.waitKey(1) == 27 or (options.dark == True and f==n_dark_frames):
            if options.dark:
                #master_dark = master_dark.astype(np.uint16)
                #cv2.imwrite(options.dark_path,master_dark)
                np.save(options.dark_path,master_dark)
                print ("Master dark saved in "+options.dark_path)
            exit(0)
