#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : main.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
#   FUNCTIONS :
#       main()
# 
#   NOTES :
#       - ...
# 
#   AUTHOR(S) : Noah Arcand Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
#
#   CHANGES :
#       - ...
# 
#   VERSION     DATE        WHO             DETAILS
#   0.0.1a      2022.11.26  Noah            Creation of project.
#

import pygame
from pygame.locals import *
import math
import sys

from simulation import Satellite, GroundStation
from constants import *


def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Satellite Orbit")
    
    bg = pygame.image.load("worldmap_light.png").convert()
    bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

    orbit = []
    army_base = []

    for i in range(0, MAX_SATELLITE_COUNT):
        orbit.append(Satellite(delay=i*WINDOW_WIDTH*2))

    army_base.append(GroundStation(x=525, y=250))
    army_base.append(GroundStation(x=1475, y=600))

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            # 'X' Button
            if event.type == pygame.QUIT:
                running = False
                continue

        for satellite in orbit:
            satellite.draw(screen)
            satellite.update_position()

        for ground_station in army_base:
            ground_station.draw(screen)

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()


if __name__ == '__main__':
    main()