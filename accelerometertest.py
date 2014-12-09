from adxl345 import ADXL345
import time

adxl345 = ADXL345()

count = 1

xsum = 0.0
ysum = 0.0
zsum = 0.0

minx = miny = minz = 100
maxx = maxy = maxz = -100


while 1:    
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

	if count == 100:
		count = 1
		xavg = xsum / 100.0
		yavg = ysum / 100.0
		zavg = zsum / 100.0
		
		xavg = round(xavg, 2)
		yavg = round(yavg, 2)
		zavg = round(zavg, 2)
		minx = round(minx, 2)
		miny = round(miny, 2)
		minz = round(minz, 2)
		maxx = round(maxx, 2)
		maxy = round(maxy, 2)
		maxz = round(maxz, 2)

		print "x = " + str(xavg) + "\tmin: " + str(minx) + "\tmax: " + str(maxx)
		print "y = " + str(yavg) + "\tmin: " + str(miny) + "\tmax: " + str(maxy)
		print "z = " + str(zavg) + "\tmin: " + str(minz) + "\tmax: " + str(maxz)
		print
		
		xsum = ysum = zsum = 0

	time.sleep(0.1)	
