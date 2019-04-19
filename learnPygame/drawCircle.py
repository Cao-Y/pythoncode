import pygame
from pygame.locals import *
import sys
pygame.init()
screen = pygame.display.set_mode((600,500))

color = 255,255,0
position = 300,250
radius = 100
width = 10
while True:
    for event in pygame.event.get():
        if event.type in (QUIT,KEYDOWN):
            pygame.quit()
            sys.exit()
    pygame.draw.circle(screen, color, position, radius, width)
    pygame.display.update()