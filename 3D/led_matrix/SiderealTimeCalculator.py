#Sidereal Time and Julian Date Calculator
#Revision history: Justine Haupt, v1.0 (11/23/17)
# Updated for localtime (Chambery), Bruno Bzeznik, 2025

#Only valid for dates between 1901 and 2099. Accurate to within 1.1s.

#References:
#http://aa.usno.navy.mil/faq/docs/JD_Formula.php
#http://aa.usno.navy.mil/faq/docs/GAST.php and

import datetime

Long = 5.933      #Longitude of location (Chambery)

#Calculate longitude in DegHHMM format for edification of user:
hemisphere = 'W'
if Long > 0:        #if the number is positive it's in the Eastern hemisphere
    hemisphere = 'E'
LongDeg = int(Long)
LongMin = (Long - int(Long))*60
LongSec = (LongMin - int(LongMin))*60
LongMin = int(LongMin)
LongSec = int(LongSec)

now = datetime.datetime.now(datetime.UTC);
TD=now.strftime("%m%d%y %H%M");

#split TD into individual variables for month, day, etc. and convert to floats:
MM = float(TD[0:2])
DD = float(TD[2:4])
YY = float(TD[4:6])
YY = YY+2000
hh = float(TD[7:9])
mm = float(TD[9:11])

#convert mm to fractional time:
mm = mm/60

#reformat UTC time as fractional hours:
UT = hh+mm

#calculate the Julian date:
JD = (367*YY) - int((7*(YY+int((MM+9)/12)))/4) + int((275*MM)/9) + DD + 1721013.5 + (UT/24)
#print('\nJulian Date: JD%s' %(JD))

#calculate the Greenwhich mean sidereal time:
GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
GMST = GMST % 24    #use modulo operator to convert to 24 hours
GMSTmm = (GMST - int(GMST))*60          #convert fraction hours to minutes
GMSTss = (GMSTmm - int(GMSTmm))*60      #convert fractional minutes to seconds
GMSThh = int(GMST)
GMSTmm = int(GMSTmm)
GMSTss = int(GMSTss)
#print('\nGreenwhich Mean Sidereal Time: %s:%s:%s' %(GMSThh, GMSTmm, GMSTss))

#Convert to the local sidereal time by adding the longitude (in hours) from the GMST.
#(Hours = Degrees/15, Degrees = Hours*15)
Long = Long/15      #Convert longitude to hours
LST = GMST+Long     #Fraction LST. If negative we want to add 24...
if LST < 0:
    LST = LST +24
LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
LSThh = int(LST)
LSTmm = int(LSTmm)
LSTss = int(LSTss)

print('%s:%s:%s' %(LSThh, LSTmm, LSTss))
