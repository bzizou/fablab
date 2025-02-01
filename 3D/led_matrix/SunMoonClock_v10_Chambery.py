import urllib.request, json
import datetime, time

# Data Retrieved frm US Naval Observatory API
# https://aa.usno.navy.mil/data/RS_OneDay
# 
# Sun and Moon Data for One Day
# https://aa.usno.navy.mil/data/api#rstt
# https://aa.usno.navy.mil/api/rstt/oneday?date=DATE&coords=COORDS&tz=TZ
#           Info to be filled in   -->          ----        ------    --
# 
# Phases of the Moon for Sequence of Dates
# https://aa.usno.navy.mil/data/api#phase
# https://aa.usno.navy.mil/api/moon/phases/date?date=2024-06-27&nump=50
#           Info to be filler in   -->               ----------      --
#           Return nump number of entries starting from the date entered
# 
# 

########################################
#####    Latitude and Longitude    #####
########################################
# Define Latitude and Longitude for location
latlong_str = "45.566669,5.93333"        #Chambery, FR

########################################
#####          Time Zone           #####
########################################
# Define Time Zone and Daylight Savings
if time.localtime().tm_isdst == 1: timezone_str = "+2"      # Central Daylight Time
else: timezone_str = "+1"                                   # Central Standard Time

today_sunrise_str = ""
today_sunset_str = ""
today_moonrise_str = ""
today_moonset_str = ""
next_moonrise_str = ""
next_moonset_str = ""

########################################
#####       Get Today's Data       #####
########################################
#Get Today's Sun and Moon Rise and Set Data
cmd_str = "https://aa.usno.navy.mil/api/rstt/oneday?date=" + datetime.datetime.now().strftime('%Y-%m-%d') + "&coords=" + latlong_str + "&tz=" + timezone_str
#print(cmd_str)
with urllib.request.urlopen(cmd_str) as url:
    data = json.load(url)
#print(data)
# get today sunrise and sunset    
for info in data["properties"]["data"]["sundata"]:
    if info["phen"] == "Set":
        today_sunset_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]
    if info["phen"] == "Rise":
        today_sunrise_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]

for info in data["properties"]["data"]["moondata"]:
    if info["phen"] == "Set":
        today_moonset_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]
        #print(f'-----------Today Moon Set: {today_moonset_str}')
        if datetime.datetime.now() < datetime.datetime.now().replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
            next_moonset_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]
            #print(f'------------Next Moon Set: {next_moonset_str}')
    if info["phen"] == "Rise":
        today_moonrise_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]
        #print(f'----------Today Moon Rise: {today_moonrise_str}')
        if datetime.datetime.now() < datetime.datetime.now().replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
            next_moonrise_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + info["time"]
            #print(f'------------Next Moon Set: {next_moonset_str}')

########################################
#####     Get the Lunar Cycle      #####
########################################
# Lunar Cycle actually 29.5 days, but I am using a 28 day cycle (0-27) to make it easier
# and referencing off the nearest phase (new, quarter, full, quarter) to it will be close enough

# Get where we are in the lunar cycle
#    0 = New Moon
#    7 = First Quarter Moon
#   14 = Full Moon
#   21 = Last Quarter Moon
#   27 = Last day before New Moon

temp_data = data["properties"]["data"]["closestphase"]
#print(temp_data)
temp_str = f'{temp_data["year"]}-{temp_data["month"]}-{temp_data["day"]} {temp_data["time"]}'
nearest_phase_str = temp_str + " " + temp_data["phase"]
nearest_phase_dt = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M')

phase_day = -1
if temp_data["phase"] == "New Moon":
    phase_day = 28 - int((nearest_phase_dt - datetime.datetime.today()).days)
    if phase_day > 28: phase_day = phase_day - 28
    #print(f'phase_day: {phase_day}')
    #print(f' alt calc: {abs(int((nearest_phase_dt - datetime.datetime.today()).days))}')
    
if temp_data["phase"] == "Full Moon":
    phase_day = 14 - int((nearest_phase_dt - datetime.datetime.today()).days)

if temp_data["phase"] == "First Quarter":
    phase_day = 7 - int((nearest_phase_dt - datetime.datetime.today()).days)

if temp_data["phase"] == "Last Quarter":
    phase_day = 21 - int((nearest_phase_dt - datetime.datetime.today()).days)

# The report is nearest 

########################################
#####     Get Tomorrow's Data      #####
########################################
# If needed get the moon rise and set times for tomorrow
if next_moonrise_str == "" or next_moonset_str == "":
    #print('Continueing to look at tomorrow')
    cmd_str = "https://aa.usno.navy.mil/api/rstt/oneday?date=" + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + "&coords=" + latlong_str + "&tz=" + timezone_str
    #print(cmd_str)
    with urllib.request.urlopen(cmd_str) as url:
        data = json.load(url)
    #print(data)
    for info in data["properties"]["data"]["moondata"]:
        if info["phen"] == "Set" and next_moonset_str == "":
            if datetime.datetime.now() < (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
                next_moonset_str = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + " " + info["time"]
        if info["phen"] == "Rise" and next_moonrise_str == "":
            if datetime.datetime.now() < (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
                next_moonrise_str = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + " " + info["time"]

########################################
#####     Get Day After's Data     #####
########################################
# If needed get the moon rise and set times for the day after tomorrow
if next_moonrise_str == "" or next_moonset_str == "":
    #print('Continueing to look at the next day')
    cmd_str = "https://aa.usno.navy.mil/api/rstt/oneday?date=" + (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d') + "&coords=" + latlong_str + "&tz=" + timezone_str
    #print(today_link_cmd_str)
    with urllib.request.urlopen(cmd_str) as url:
        data = json.load(url)
    #print(data)
    for info in data["properties"]["data"]["moondata"]:
        if info["phen"] == "Set" and next_moonset_str == "":
            if datetime.datetime.now() < (datetime.datetime.now() + datetime.timedelta(days=2)).replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
                next_moonset_str = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d') + " " + info["time"]
        if info["phen"] == "Rise" and next_moonrise_str == "":
            if datetime.datetime.now() < (datetime.datetime.now() + datetime.timedelta(days=2)).replace(hour = int(info["time"][:2]), minute = int(info["time"][-2:])):
                next_moonrise_str = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d') + " " + info["time"]





########################################
#####        Output the data       #####
########################################
print(" Today's Sun Rise: " + today_sunrise_str)
print("  Today's Sun Set: " + today_sunset_str)
print("Today's Moon Rise: " + today_moonrise_str)
print(" Today's Moon Set: " + today_moonset_str)
print()
if datetime.datetime.strptime(next_moonrise_str, '%Y-%m-%d %H:%M' ) < datetime.datetime.strptime(next_moonset_str, '%Y-%m-%d %H:%M' ):
    print('   Next Moon Rise: ' + next_moonrise_str)
    print('    Next Moon Set: ' + next_moonset_str)
else:
    print('    Next Moon Set: ' + next_moonset_str)
    print('   Next Moon Rise: ' + next_moonrise_str)
print()
print(f'The nearest phase is {nearest_phase_str}')
print()
print(f'We are on day {phase_day} of the 29 day lunar cycle')






