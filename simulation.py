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
#       LEOSatellite.LEOSatellite()
#       LEOSatellite.draw()
#       LEOSatellite.update_position()
#       LEOSatellite.get_2D_position()
#       LEOSatellite.get_3D_position()
#       MEOSatellite.MEOSatellite()
#       MEOSatellite.draw()
#       MEOSatellite.update_position()
#       MEOSatellite.get_2D_position()
#       MEOSatellite.get_3D_position()
#       GroundStation.GroundStation()
#       GroundStation.draw()
#       GroundStation.get_2D_position()
#       GroundStation.get_3D_position()
#       Congestion.Congestion()
#       Congestion.generate_congestion_heatmap()
# 
#   NOTES :
#       - ...
# 
#   AUTHOR(S) : Noah F. A. Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
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
#   0.1.1       2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
#   0.2.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
#   0.3.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
#


from math import sin, pi, radians, cos
import pygame
import numpy as np

from constants import *


class LEOSatellite:
    def __init__(self, delay=0):
        self.x = 0
        self.y = 0
        self.z = LEO_ORBIT_HEIGHT
        self.radius = 5
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour):
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self):
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = ((pygame.time.get_ticks() / (WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT) + self.delay) / TIME_TO_COMPLETE_ORBIT * -cos(WINDOW_WIDTH)) * SIMULATION_SPEED_MULTIPLIER
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value
        self.x = self.time % WINDOW_WIDTH
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = int(AMPLITUDE * sin(2 * pi * LEO_FREQUENCY * self.time + radians(self.phase))) + WINDOW_HEIGHT / 2

    def get_2D_position(self):
        return (self.x, self.y) # Return 2D position pair for current satellite
    
    def get_3D_position(self):
        return (self.x, self.y, self.z) # Return 3D position pair for current satellite


class MEOSatellite:
    def __init__(self, delay=0):
        self.x = 0
        self.y = 0
        self.z = MEO_ORBIT_HEIGHT
        self.radius = 7.5
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour):
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self):
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = ((pygame.time.get_ticks() / (WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT * 2) + self.delay) / TIME_TO_COMPLETE_ORBIT * -cos(WINDOW_WIDTH)) * SIMULATION_SPEED_MULTIPLIER
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value
        self.x = self.time % WINDOW_WIDTH
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = int(AMPLITUDE * sin(2 * pi * MEO_FREQUENCY * self.time + radians(self.phase))) + WINDOW_HEIGHT / 2

    def get_2D_position(self):
        return (self.x, self.y) # Return 2D position pair for current satellite
    
    def get_3D_position(self):
        return (self.x, self.y, self.z) # Return 3D position pair for current satellite


class GroundStation:
    def __init__(self, x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2):
        self.x = x
        self.y = y
        self.z = 0
        self.radius = 7.5

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def get_2D_position(self):
        return (self.x, self.y) # Return 2D position pair for current ground station
    
    def get_3D_position(self):
        return (self.x, self.y, self.z) # Return 3D position pair for current ground station


class Congestion:
    def __init__(self):
        self. cell_size = 0

    def generate_congestion_heatmap(self, grid_density=10):
        # Input sanitization
        if not isinstance(grid_density, int):
            raise TypeError("'density' must be an integer")
        if grid_density <= 0:
            raise TypeError("'density' must be above 0")
        
        # Get the aspect ration of the program window.
        aspect_ratio = WINDOW_WIDTH / WINDOW_HEIGHT

        # Get the pixel size of the cells.
        self.cell_size = WINDOW_WIDTH / aspect_ratio / grid_density

        # Get the number of columns and rows for our cell grid.
        column_num = int(WINDOW_WIDTH / self.cell_size)
        row_num = int(WINDOW_HEIGHT / self.cell_size)
        
        congestion_map = {}
        # Go through each cell in the grid
        for col in range(column_num):
            for row in range(row_num):
                if (row * self.cell_size) < (WINDOW_HEIGHT / 2 - AMPLITUDE) or (row * self.cell_size) >= (WINDOW_HEIGHT / 2 + AMPLITUDE):
                    continue    # Ensures that we don't create unnecessary cells where satellites won't travel
                else:
                    scale = 1.0
                    size = column_num * row_num
                    random_numbers = np.random.exponential(scale, size)

                    # Scale the values to be within the desired range
                    random_numbers = random_numbers / np.max(random_numbers) * CONGESTION_COMPLEXITY + 1

                    # Round the values to the nearest integer
                    random_numbers = np.round(random_numbers)

                    # Assign the first random number in the list to the congestion map cell
                    congestion_map[((col*self.cell_size, row*self.cell_size), ((col+1)*self.cell_size, (row+1)*self.cell_size))] = random_numbers[0]
                    
                    random_numbers = random_numbers[1:]   # Remove that number out of the list

        return congestion_map
