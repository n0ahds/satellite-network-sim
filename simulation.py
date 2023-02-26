#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : simulation.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
#   FUNCTIONS :
#       Satellite.Satellite()
#       Satellite.draw()
#       Satellite.update_position()
#       Satellite.get_position()
#       GroundStation.GroundStation()
#       GroundStation.draw()
#       GroundStation.get_position()
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
#   0.0.2a      2023.01.09  Noah            Basic simulation of LEO satellite constellation.
#   0.0.2b      2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
#   0.0.2c      2023.01.21  Noah/Ranul      Added distortion to LEO satellite orbit to better represent Mercator Projection.
#   0.1.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
#   0.1.1a      2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
#

from math import sin, pi, radians, asin
import pygame

from constants import *


class LEOSatellite:
    def __init__(self, delay=0):
        self.x = 0
        self.y = 0
        self.radius = 5
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour):
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self):
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = (pygame.time.get_ticks() / (WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT) + self.delay) / TIME_TO_COMPLETE_ORBIT * -cos(WINDOW_WIDTH)
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value
        self.x = self.time % WINDOW_WIDTH
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = int(AMPLITUDE * sin(2 * pi * LEO_FREQUENCY * self.time + radians(self.phase))) + WINDOW_HEIGHT / 2

    def get_position(self):
        return (self.x, self.y) # Return position pair for current satellite


class GroundStation:
    def __init__(self, x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2):
        self.x = x
        self.y = y
        self.radius = 7.5

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def get_position(self):
        return (self.x, self.y)


class MEOSatellite:
    def __init__(self, delay=0):
        self.x = 0
        self.y = 0
        self.radius = 7.5
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour):
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self):
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = (pygame.time.get_ticks() / (WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT * 2) + self.delay) / TIME_TO_COMPLETE_ORBIT * -cos(WINDOW_WIDTH)
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value
        self.x = self.time % WINDOW_WIDTH
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = int(AMPLITUDE * sin(2 * pi * MEO_FREQUENCY * self.time + radians(self.phase))) + WINDOW_HEIGHT / 2

    def get_position(self):
        return (self.x, self.y) # Return position pair for current satellite