import pygame
import time

with open("alarms.txt") as f:
	alarmlist = f.readlines()

alarmlist = sorted(alarmlist)

with open("alarms.txt", "w") as f:
	for alarms in alarmlist:
		f.write(alarms)

while 1:
	time.ctime()
	currenttime = time.strftime('%m/%d/%Y%l:%M %p') #11/30/14 5:34 PM
	print currenttime

	for alarms in alarmlist:
		if alarms.strip() == currenttime.strip():
			pygame.mixer.init()
			pygame.mixer.music.load("alarm_beep.wav")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				continue
			


	time.sleep(60)


