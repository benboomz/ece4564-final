'''import pygame

pygame.mixer.init()
pygame.mixer.music.load("alarm_beep.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue
'''

import time

time.ctime()
time = time.strftime('%m/%d/%y%l:%M %p') #11/30/14 5:34 PM
print time
