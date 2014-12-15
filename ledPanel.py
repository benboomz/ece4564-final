import RPi.GPIO as GPIO
import time
 
delay = 0.000001
 
GPIO.setmode(GPIO.BCM)
red1_pin = 17
green1_pin = 18
blue1_pin = 22
red2_pin = 23
green2_pin = 24
blue2_pin = 25
clock_pin = 3
a_pin = 7
b_pin = 8
c_pin = 9
latch_pin = 4
oe_pin = 2

#######################################
#digits
hrLeft = 1
hrRight = 1
minLeft = 1
minRight = 1

########################################
#sleep quality
bad = 1
ok = 3
good = 2
########################################
#hours
hr1 = bad
hr2 = bad
hr3 = bad
hr4 = bad
hr5 = bad
hr6 = bad
hr7 = bad
hr8 = bad
hr9 = bad
hr10 = bad
hr11 = bad
hr12 = bad

colortochange = 2

 
GPIO.setup(red1_pin, GPIO.OUT)
GPIO.setup(green1_pin, GPIO.OUT)
GPIO.setup(blue1_pin, GPIO.OUT)
GPIO.setup(red2_pin, GPIO.OUT)
GPIO.setup(green2_pin, GPIO.OUT)
GPIO.setup(blue2_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(a_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)
GPIO.setup(c_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(oe_pin, GPIO.OUT)
 
screen = [[0 for x in xrange(32)] for x in xrange(16)]
 
def clock():
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
 
def latch():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)
 
def bits_from_int(x):
    a_bit = x & 1
    b_bit = x & 2
    c_bit = x & 4
    return (a_bit, b_bit, c_bit)
 
def set_row(row):
    #time.sleep(delay)
    a_bit, b_bit, c_bit = bits_from_int(row)
    GPIO.output(a_pin, a_bit)
    GPIO.output(b_pin, b_bit)
    GPIO.output(c_pin, c_bit)
    #time.sleep(delay)
 
def set_color_top(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red1_pin, red)
    GPIO.output(green1_pin, green)
    GPIO.output(blue1_pin, blue)
    #time.sleep(delay)
 
def set_color_bottom(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red2_pin, red)
    GPIO.output(green2_pin, green)
    GPIO.output(blue2_pin, blue)
    #time.sleep(delay)
     
def refresh():
    for row in range(8):
        GPIO.output(oe_pin, 1)
        set_color_top(0)
        set_row(row)
        #time.sleep(delay)
        for col in range(32):
            set_color_top(screen[row][col])
            set_color_bottom(screen[row+8][col])
            clock()
        #GPIO.output(oe_pin, 0)
        latch()
        GPIO.output(oe_pin, 0)
        time.sleep(delay)
 
def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
            screen[y][x] = color
 
 
def set_pixel(x, y, color):
    screen[y][x] = color
 
#fill_rectangle(0, 0, 12, 12, 1)
#fill_rectangle(20, 4, 30, 15, 2)
#fill_rectangle(15, 0, 19, 7, 7)
##################################################################
#first digit

while True: 
	
	time.ctime()
	hour = time.strftime("%I")
	minute = time.strftime("%M")

	if hour < 10:
		hrLeft = 0
		hrRight = int(hour[1])
	else:
		hrLeft = int(hour[0])
		hrRight = int(hour[1])
	
	minLeft = int(minute[0])
	minRight = int(minute[1])
	
	print hrLeft, hrRight, minLeft, minRight	


	if(hrLeft == 1):
		fill_rectangle(25, 13, 31, 15, 0) # top -
		fill_rectangle(25, 9, 31, 11, 0) # mid -
		fill_rectangle(29, 9, 31, 15, 0) # left top |
		fill_rectangle(29, 5, 31, 11, 0) # bottom left |
		fill_rectangle(25, 5, 31, 7, 0) # bottom -
		fill_rectangle(25, 5, 27, 11, colortochange) # bottom right |
		fill_rectangle(25, 9, 27, 15, colortochange) # right top |
	elif(hrLeft == 0):
		fill_rectangle(25, 9, 31, 11, 0) # mid -
		fill_rectangle(25, 13, 31, 15, colortochange) # top -
		fill_rectangle(25, 9, 27, 15, colortochange) # right top |
		fill_rectangle(29, 9, 31, 15, colortochange) # left top |
		fill_rectangle(25, 5, 27, 11, colortochange) # bottom right |
		fill_rectangle(29, 5, 31, 11, colortochange) # bottom left |
		fill_rectangle(25, 5, 31, 7, colortochange) # bottom -
		
#fill_rectangle(27, 5, 29, 15, 1) #1
#fill_rectangle(25, 13, 31, 15, 1) # top -
#fill_rectangle(25, 9, 27, 15, 1) # right top |
#fill_rectangle(25, 9, 31, 11, 1) # mid -
#fill_rectangle(29, 9, 31, 15, 1) # left top |
#fill_rectangle(25, 5, 27, 11, 1) # bottom right |
#fill_rectangle(29, 5, 31, 11, 1) # bottom left |
#fill_rectangle(25, 5, 31, 7, 1) # bottom -

##################################################################

	if(hrRight == 1):
		fill_rectangle(18, 13, 24, 15, 0) # top -	
		fill_rectangle(18, 9, 24, 11, 0) # mid -
		fill_rectangle(22, 9, 24, 15, 0) # top left |
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		fill_rectangle(18, 5, 24, 7, 0) # bottom -
		
		fill_rectangle(18, 9, 20, 15, colortochange) # top right |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
	elif(hrRight == 2):	
		fill_rectangle(22, 9, 24, 15, 0) # top left |
		fill_rectangle(18, 5, 20, 11, 0) # bottom  right |
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # top right |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(22, 5, 24, 11, colortochange) # bottom left |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	elif(hrRight == 3):
		fill_rectangle(22, 9, 24, 15, 0) # top left |
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	elif(hrRight == 4):		
		fill_rectangle(18, 13, 24, 15, 0) # top -
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		fill_rectangle(18, 5, 24, 7, 0) # bottom -
		
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(22, 9, 24, 15, colortochange) # top left |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
	elif(hrRight == 5):		
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		fill_rectangle(18, 9, 20, 15, 0) # right top |
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(22, 9, 24, 15, colortochange) # top left |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -	
	elif(hrRight == 6):
		fill_rectangle(22, 9, 24, 15, 0) # top left |
	
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(22, 5, 24, 11, colortochange) # bottom left |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	elif(hrRight == 7):
		fill_rectangle(18, 9, 24, 11, 0) # mid -
		fill_rectangle(22, 9, 24, 15, 0) # top left |
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		fill_rectangle(18, 5, 24, 7, 0) # bottom -
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top 
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
	elif(hrRight == 8):
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(22, 9, 24, 15, colortochange) # top left |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(22, 5, 24, 11, colortochange) # bottom left |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	elif(hrRight == 9):
		fill_rectangle(22, 5, 24, 11, 0) # bottom left |
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(18, 9, 24, 11, colortochange) # mid -
		fill_rectangle(22, 9, 24, 15, colortochange) # top left |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	elif(hrRight == 0):
		fill_rectangle(18, 9, 24, 11, 0) # mid -
		
		fill_rectangle(18, 13, 24, 15, colortochange) # top -
		fill_rectangle(18, 9, 20, 15, colortochange) # right top |
		fill_rectangle(22, 9, 24, 15, colortochange) # top left |
		fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
		fill_rectangle(22, 5, 24, 11, colortochange) # bottom left |
		fill_rectangle(18, 5, 24, 7, colortochange) # bottom -
	
#2             x    y   x   y
#fill_rectangle(18, 13, 24, 15, colortochange) # top -
#fill_rectangle(18, 9, 20, 15, colortochange) # right top |
#fill_rectangle(18, 9, 24, 11, colortochange) # mid -
#fill_rectangle(22, 9, 24, 15, colortochange) # top left |
#fill_rectangle(18, 5, 20, 11, colortochange) # bottom  right |
#fill_rectangle(22, 5, 24, 11, colortochange) # bottom left |
#fill_rectangle(18, 5, 24, 7, colortochange) # bottom -

#dots
	fill_rectangle(15, 11, 17, 13, colortochange)
	fill_rectangle(15, 7, 17, 9, colortochange)

###################################################################
	if(minLeft == 1):
		fill_rectangle(8, 13, 14, 15, 0) # top -
		fill_rectangle(8, 9, 14, 11, 0) # mid -
		fill_rectangle(12, 9, 14, 15, 0) # left top |
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
		fill_rectangle(8, 5, 14, 7, 0) #bottom -
		
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
	elif(minLeft == 2):
		fill_rectangle(12, 9, 14, 15, 0) # left top |
		fill_rectangle(8, 5, 10, 11, 0) # bottom right |
		
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 5, 14, 11, colortochange) # bottom left |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 3):
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
		fill_rectangle(12, 9, 14, 15, 0) # left top |
		
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 4):
		fill_rectangle(8, 13, 14, 15, 0) # top -
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
		fill_rectangle(8, 5, 14, 7, 0) #bottom -	
		
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
	elif(minLeft == 5):
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
		fill_rectangle(8, 9, 10, 15, 0)  # right top |
		
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 6):
		fill_rectangle(8, 9, 10, 15, 0)  # right top |
		
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(12, 5, 14, 11, colortochange) # bottom left |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 7):

		fill_rectangle(12, 9, 14, 15, 0) # left top |
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
		fill_rectangle(8, 5, 14, 7, 0) #bottom -
		
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
	elif(minLeft == 8):
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(12, 5, 14, 11, colortochange) # bottom left |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 9):
		fill_rectangle(12, 5, 14, 11, 0) # bottom left |
	
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(8, 9, 14, 11, colortochange) # mid -
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	elif(minLeft == 0):
		fill_rectangle(8, 9, 14, 11, 0) # mid -
		
		fill_rectangle(8, 13, 14, 15, colortochange) # top -
		fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
		fill_rectangle(12, 9, 14, 15, colortochange) # left top |
		fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
		fill_rectangle(12, 5, 14, 11, colortochange) # bottom left |
		fill_rectangle(8, 5, 14, 7, colortochange) #bottom -
	
#3             x   y   x   y
#fill_rectangle(8, 13, 14, 15, colortochange) # top -
#fill_rectangle(8, 9, 10, 15, colortochange)  # right top |
#fill_rectangle(8, 9, 14, 11, colortochange) # mid -
#fill_rectangle(12, 9, 14, 15, colortochange) # left top |
#fill_rectangle(8, 5, 10, 11, colortochange) # bottom right |
#fill_rectangle(12, 5, 14, 11, colortochange) # bottom left |
#fill_rectangle(8, 5, 14, 7, colortochange) #bottom -

####################################################################

	if(minRight == 1):
		fill_rectangle(1, 13, 7, 15, 0) # top
		
		fill_rectangle(1, 9, 7, 11, 0) # mid
		fill_rectangle(5, 9, 7, 15, 0) # top left | 
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
		fill_rectangle(1, 5, 7, 7, 0) # bottom -
		
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
	elif(minRight == 2):
		fill_rectangle(5, 9, 7, 15, 0) # top left | 
		fill_rectangle(1, 5, 3, 11, 0) # bottom right |
		
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 5, 7, 11, colortochange) # bottom left |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	elif(minRight == 3):
		fill_rectangle(5, 9, 7, 15, 0) # top left | 
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
	
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |	
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	elif(minRight == 4):
		fill_rectangle(1, 13, 7, 15, 0) # top
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
		fill_rectangle(1, 5, 7, 7, 0) # bottom -
		
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
	elif(minRight == 5):
		fill_rectangle(1, 9, 3, 15, 0) # top right |
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
		
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	elif(minRight == 6):
		fill_rectangle(1, 9, 3, 15, 0) # top right |
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
		fill_rectangle(5, 5, 7, 11, colortochange) # bottom left |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	elif(minRight == 7):
		fill_rectangle(1, 9, 7, 11, 0) # mid
		fill_rectangle(5, 9, 7, 15, 0) # top left |
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
		fill_rectangle(1, 5, 7, 7, 0) # bottom -
		
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
	elif(minRight == 8):
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
		fill_rectangle(5, 5, 7, 11, colortochange) # bottom left |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -	
	elif(minRight == 9):
		fill_rectangle(5, 5, 7, 11, 0) # bottom left |
		
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(1, 9, 7, 11, colortochange) # mid
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	elif(minRight == 0):
		fill_rectangle(1, 9, 7, 11, 0) # mid
		
		fill_rectangle(1, 13, 7, 15, colortochange) # top
		fill_rectangle(1, 9, 3, 15, colortochange) # top right |
		fill_rectangle(5, 9, 7, 15, colortochange) # top left | 
		fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
		fill_rectangle(5, 5, 7, 11, colortochange) # bottom left |
		fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
	
#4             x  y  x   y
#fill_rectangle(1, 13, 7, 15, colortochange) # top
#fill_rectangle(1, 9, 3, 15, colortochange) # top right |
#fill_rectangle(1, 9, 7, 11, colortochange) # mid
#fill_rectangle(5, 9, 7, 15, 3)# top left | 
#fill_rectangle(1, 5, 3, 11, colortochange) # bottom right |
#fill_rectangle(5, 5, 7, 11, colortochange) # bottom left |
#fill_rectangle(1, 5, 7, 7, colortochange) # bottom -
################################################################


	fill_rectangle(20, 0, 32, 1, hr1)
	fill_rectangle(20, 0, 31, 1, hr2)
	fill_rectangle(20, 0, 30, 1, hr3)
	fill_rectangle(20, 0, 29, 1, hr4)
	fill_rectangle(20, 0, 28, 1, hr5)
	fill_rectangle(20, 0, 27, 1, hr6)
	fill_rectangle(20, 0, 26, 1, hr7)
	fill_rectangle(20, 0, 25, 1, hr8)
	fill_rectangle(20, 0, 24, 1, hr9)
	fill_rectangle(20, 0, 23, 1, hr10)
	fill_rectangle(20, 0, 22, 1, hr11)
	fill_rectangle(20, 0, 21, 1, hr12)

	
	counter = 0
	while counter != 30:	
		refresh()
		counter = counter + 1
