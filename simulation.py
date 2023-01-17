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
#       ...
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

from math import atan2, sqrt, cos, sin
from copy import deepcopy
import pygame

from constants import *


class Satellite:   # 1 day
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour

        self.orbit = []
        self.distance_to_earth = 0

        self.x_velocity = 4
        self.y_velocity = 0

    def draw(self, screen):
        x = self.x
        y = self.y

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                updated_points.append((x, y))
            pygame.draw.lines(screen, self.colour, False, updated_points, 2)

        pygame.draw.circle(screen, self.colour, (x, y), self.radius)

    def attraction(self):
        gravitational_force = GRAVITATIONAL_CONSTANT * SATELLITE_MASS * EARTH_MASS / (EARTH_RADIUS + ORBIT_HEIGHT) ** 2
        theta = atan2(self.y, self.x)
        force_x = cos(theta) * gravitational_force
        force_y = sin(theta) * gravitational_force
        return force_x, force_y

    def update_position(self):
        total_fx = total_fy = 0
		
        fx, fy = self.attraction()
        total_fx += fx
        total_fy += fy

        self.x_velocity += total_fx / EARTH_MASS
        self.y_velocity += total_fy / EARTH_MASS

        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x > WINDOW_WIDTH:
            self.x -= WINDOW_WIDTH

        if self.y > WINDOW_HEIGHT:
            self.y -= WINDOW_HEIGHT

        self.orbit.append((self.x, self.y))