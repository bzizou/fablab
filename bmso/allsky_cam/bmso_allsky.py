#!/usr/bin/env python3
import cv2
import urllib.request
import numpy as np
from optparse import OptionParser
import os
from datetime import datetime
import json

# Window name
window_name = "BMSO Allsky Cam"

# Default dark path
default_dark_path = os.environ.get('HOME')+"/.bmso_allsky_dark.npy"

# Options parsing
parser = OptionParser()
parser.add_option("-u", "--url",
                  dest="url", default="",
                  help="Camera stream url")
parser.add_option("-c", "--create_dark", action="store_true",
                  dest="dark",
                  help="Create a master dark stacking n_darks dark frames. Don't forget to cover the lens!")
parser.add_option("-d", "--dark",
                  dest="dark_path", default=default_dark_path,
                  help="Path of the dark image")
parser.add_option("-n", "--n_darks",
                  dest="n_darks", default="20",
                  help="Number of dark frames to stack")
parser.add_option("-s", "--stack_size",
                  dest="stack_size", default="20",
                  help="Number of frames to stack")
parser.add_option("-o", "--overstack",
                  dest="overstack", action="store_true",
                  help="Double the signal strenght by stacking two average-stacked frames")
parser.add_option("-S", "--store",
                  dest="store", default="",
                  help="Record and store the stacked pictures into the provide directory")
parser.add_option("-R", "--red",
                  dest="red", default="",
                  help="Value for Red balance (-255 to 255)")
parser.add_option("-G", "--green",
                  dest="green", default="",
                  help="Value for Green balance (-255 to 255)")
parser.add_option("-B", "--blue",
                  dest="blue", default="",
                  help="Value for Blue balance (-255 to 255)")
parser.add_option("-t", "--sensor_url",
                  dest="sensor_url", default="",
                  help="Get temperature from sensor (only bmp280 supported)")

(options, args) = parser.parse_args()

if options.url != "" :
  stream = urllib.request.urlopen(options.url)
else:
  # default stream url
  stream = urllib.request.urlopen('http://192.168.1.205:81/stream')
n_dark_frames = int(options.n_darks)
stack_size = int(options.stack_size)

# Load dark master if exists
dark_loaded=False
if os.path.exists(options.dark_path) and not options.dark:
  print("Loading master dark "+options.dark_path)
  #dark_i=cv2.imread(options.dark_path,-1)
  #dark_i = dark_i.astype(np.uint16)
  dark_i=np.load(options.dark_path)
  dark_loaded=True
if options.dark:
  print ("Don't forget to cover the camera for dark creation!")
  print ("Creating master dark...")
else:
  cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
  font = cv2.FONT_HERSHEY_SIMPLEX

init=0

# Initiate the store directory
if options.store != "" and not os.path.exists(options.store):
    os.mkdir(options.store)

# Main
bytes = bytes()
f=0
previous = False
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
        if not options.dark:
          # Dark subtraction
          if dark_loaded:
            i=i-dark_i
          # Normalization
          cv2.normalize(i2,i,0,65535,cv2.NORM_MINMAX)

        # Init
        if init == 0:
            width=i.shape[1]
            height=i.shape[0]
            print("Frame size: "+str(width)+"x"+str(height))
            if not options.dark:
              cv2.resizeWindow(window_name, width, height)
              img = np.zeros((height, width, 3), dtype = np.uint8)
              cv2.putText(img, "Stacking. Please, wait...", (100,100), font, 3, (0, 0, 255), 4, cv2.LINE_AA)
              cv2.imshow(window_name, img)
            init=1

        # Stacking 
        if options.dark:
            if f == 1:
                master_dark=i/n_dark_frames
            else:
              master_dark+=i/n_dark_frames
        else:
            print("Stacking...")
            if f == 1:
              stacked_i=i/stack_size
            else:
              stacked_i+=i/stack_size
            if f==stack_size:
                f=0
                # Convert back to 8 bits and display
                if options.overstack:
                  if previous:
                     print("Overstacking")
                     i=stacked_i
                     stacked_i=stacked_i+previous_stacked_i
                     previous_stacked_i=i
                  else:
                     previous_stacked_i=stacked_i
                     previous = True
                if options.red:
                    stacked_i[...,2]=cv2.add(stacked_i[...,2],int(options.red))
                if options.green:
                    stacked_i[...,1]=cv2.add(stacked_i[...,1],int(options.green))
                if options.blue:
                    stacked_i[...,0]=cv2.add(stacked_i[...,0],int(options.blue))
                stacked_8bits=stacked_i
                cv2.normalize(stacked_i,stacked_8bits,0,255,cv2.NORM_MINMAX)
                # Get temperature
                if options.sensor_url != "":
                  r = urllib.request.urlopen(options.sensor_url)
                  sensor=json.loads(r.read())
                  temp=str(sensor['StatusSNS']['BMP280']['Temperature'])
                  temp_unit=sensor['StatusSNS']['TempUnit']
                  pressure=str(sensor['StatusSNS']['BMP280']['Pressure'])
                  pressure_unit=sensor['StatusSNS']['PressureUnit']
                  sensor_string=temp+" "+temp_unit+"  "+pressure+" "+pressure_unit
                # Add OSD
                d=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                cv2.putText(stacked_8bits, window_name, (10,height-60), font, 1, (0, 0, 255), 4, cv2.LINE_AA)
                cv2.putText(stacked_8bits, d, (10,height-15), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                if options.sensor_url != "":
                  cv2.putText(stacked_8bits, sensor_string, (width-400,height-15), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                # Outputs
                if options.store != "":
                    filename=options.store+"/"+window_name+"-"+d+".jpg"
                    print("Saving frame to "+filename)
                    cv2.imwrite(filename, stacked_8bits.astype(np.uint8))
                print("Displaying...")
                cv2.imshow(window_name, stacked_8bits.astype(np.uint8))


        if cv2.waitKey(1) == 27 or (options.dark == True and f==n_dark_frames):
            if options.dark:
                #master_dark = master_dark.astype(np.uint16)
                #cv2.imwrite(options.dark_path,master_dark)
                np.save(options.dark_path,master_dark)
                print ("Master dark saved in "+options.dark_path)
            exit(0)
        if not options.dark and cv2.getWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE) < 0 :
            exit(0)
