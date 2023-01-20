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

from math import sin, pi, radians, asin
import pygame

from constants import *


class Satellite:
    def __init__(self, delay=0):
        self.x = 0
        self.y = 0
        self.radius = 5
        self.colour = RED
        self.phase = 0
        self.delay = delay
        self.orbit_number = 0

        '''
        self.orbit = []

        self.distance_to_earth = 0

        self.x_velocity = 1
        self.y_velocity = 0
        '''

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
    
    def update_position(self):
        self.time = (pygame.time.get_ticks() + self.delay) / WINDOW_WIDTH * SATELLITE_SPEED   # Program counter.
        self.y = int(AMPLITUDE * sin(2 * pi * FREQUENCY * self.time + radians(self.phase))) + WINDOW_HEIGHT / 2    # Calculate the sinwave of for y-coordinate

        self.x = self.time % WINDOW_WIDTH    
    '''
    def draw(self, screen):
        x = self.x
        y = self.y

        if len(self.orbit) > 2:
            updated_points = []
            print(self.orbit)
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
    '''

class GroundStation:
    def __init__(self, x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2):
        self.x = x
        self.y = y
        self.radius = 7.5

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)