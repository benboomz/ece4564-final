from adxl345 import ADXL345

adxl345 = ADXL345()

count = 1

xsum = ysum = zsum = 0.0

minx = miny = minz = 100
maxx = maxy = maxz = -100
print

with open('sleephistory.json', 'r+') as json_data:
    sleephistory = json.load(json_data)


while 1:    

    time.ctime()
    hour = time.strftime("%H")
    minute = time.strftime("%M")

    minutetrigger = 0
    if minute == "00":
        minutetrigger = 1
    else:
        minutetrigger = 0

    if hour > 22 or hour < 10:
        hourtrigger = 1

    # if it is between 10 pm and 10 am, and the minute is 00, start reading from accelerometer
    # the accelerometer will average the amount of movements from each axis for every hour
    while minutetrigger and hourtrigger:

        axes = adxl345.getAxes(True)
        
        x = axes['x']
        y = axes['y']
        z = axes['z']
        
        count = count + 1   
        xsum = xsum + x
        ysum = ysum + y
        zsum = zsum + z
            
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if z < minz:
            minz = z

        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
        if z > maxz:
            maxz = z

        #count = 600 is a minute
        # 36000 is an hour
        if count == 36000:
            count = 1
            xavg = xsum / 36000.0
            yavg = ysum / 36000.0
            zavg = zsum / 36000.0
            
            xavg = round(xavg, 2)
            yavg = round(yavg, 2)
            zavg = round(zavg, 2)
            minx = round(minx, 2)
            miny = round(miny, 2)
            minz = round(minz, 2)
            maxx = round(maxx, 2)
            maxy = round(maxy, 2)
            maxz = round(maxz, 2)
            
            rangex = maxx - minx
            rangey = maxy - miny
            rangez = maxz - minz

            avgrange = round((rangex+rangey+rangez)/3, 2)
            
            if avgrange > 0.50:
                sleepcolor =  "red"
                sleepquality = "awake"
            elif avgrange < 0.20:
                sleepcolor =  "green"
                sleepquality = "rem sleep"
            else:
                sleepcolor = "yellow"
                sleepquality = "light sleep"

            print "\t" + str(avgrange)
            print "\t" + str(rangex), str(rangey), str(rangez)
            print       

            sleephistory[date][minute+":00:00"] = sleepquality

            with open('sleephistory.json','w') as outfile:
                json.dump(sleephistory, outfile, indent=4)
    

            xsum = ysum = zsum = 0
            minx = miny = minz = 100
            maxx = maxy = maxz = -100

        if hour == 10:
            hourtrigger = 0

        time.sleep(0.1) 

        time.ctime()
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        date = time.strftime("%Y-%m-%d")

        minutetrigger = 0
        if minute == "00":
            minutetrigger = 1
        else:
            minutetrigger = 0

        if hour > 22 or hour < 10:
            hourtrigger = 1