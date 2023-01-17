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

from simulation import Satellite
from constants import *


def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Satellite Orbit")
    
    bg = pygame.image.load("worldmap_light.png").convert()
    bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

    orbit = []

    for i in range(0, 100):
        orbit.append(Satellite(0, 0, 5, RED))


    running = True
    while running:
        clock.tick(fps)
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            # 'X' Button
            if event.type == pygame.QUIT:
                running = False
                continue

        for satellite in orbit:
            satellite.draw(screen)
            satellite.update_position()

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()


if __name__ == '__main__':
    main()