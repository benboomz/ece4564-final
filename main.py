import pygame

pygame.mixer.init()
pygame.mixer.music.load("alarm_beep.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue
