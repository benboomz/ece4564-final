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

	if count == 10:
		count = 1
		xavg = xsum / 10.0
		yavg = ysum / 10.0
		zavg = zsum / 10.0
		
		print "x = " + str(xavg) + "\tmin: " + str(minx) + "\tmax: " + str(maxx)
		print "y = " + str(yavg) + "\tmin: " + str(miny) + "\tmax: " + str(maxy)
		print "z = " + str(zavg) + "\tmin: " + str(minz) + "\tmax: " + str(maxz)
		print
		
		xsum = ysum = zsum = 0

	time.sleep(0.1)	
