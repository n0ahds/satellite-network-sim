""" PROJECT : Satellite Network Simulation

    FILENAME : simulation.py

    FUNCTIONS :
        LEOSatellite.__init__()
        LEOSatellite.draw()
        LEOSatellite.update_position()
        LEOSatellite.get_2D_position()
        LEOSatellite.get_3D_position()
        MEOSatellite.__init__()
        MEOSatellite.draw()
        MEOSatellite.update_position()
        MEOSatellite.get_2D_position()
        MEOSatellite.get_3D_position()
        GroundStation.__init__()
        GroundStation.draw()
        GroundStation.get_2D_position()
        GroundStation.get_3D_position()
        Congestion.__init__()
        Congestion.initialize_heatmap()
        Congestion.generate_congestion_heatmap()
        Congestion.refresh_congestion_heatmap()

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
"""

from math import sin, pi, radians

import pygame
import numpy as np

from constants import *


class LEOSatellite:
    def __init__(self, delay=0) -> None:
        self.x = delay
        self.y = 0
        self.z = LEO_ORBIT_HEIGHT
        self.radius = 5
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour) -> None:
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self) -> None:
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = pygame.time.get_ticks() * LEO_SPEED * SIMULATION_SPEED_MULTIPLIER + self.delay
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = LEO_AMPLITUDE * sin(2 * pi * LEO_FREQUENCY * self.time + radians(self.phase)) + WINDOW_HEIGHT / 2
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value        
        self.x = self.time % WINDOW_WIDTH

    def get_2D_position(self) -> tuple[float, float]:
        return (self.x, self.y) # Return 2D position pair for current satellite
    
    def get_3D_position(self) -> tuple[float, float, int]:
        return (self.x, self.y, self.z) # Return 3D position pair for current satellite


class MEOSatellite:
    def __init__(self, delay=0) -> None:
        self.x = delay
        self.y = 0
        self.z = MEO_ORBIT_HEIGHT
        self.radius = 6
        self.phase = 0
        self.delay = delay

    def draw(self, screen, colour) -> None:
        # Draw a red circle to represent satellite position
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update_position(self) -> None:
        # Get program tickrate/clockspeed to calculate our positional values
        self.time = pygame.time.get_ticks() * MEO_SPEED * SIMULATION_SPEED_MULTIPLIER + self.delay
        # Utilize the sinwave formula to get y-coordinate, using an offset of 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen
        self.y = AMPLITUDE * sin(2 * pi * MEO_FREQUENCY * self.time + radians(self.phase)) + WINDOW_HEIGHT / 2
        # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to get a prevent x-coordinate from going over WINDOW_WIDTH value        
        self.x = self.time % WINDOW_WIDTH

    def get_2D_position(self) -> tuple[float, float]:
        return (self.x, self.y) # Return 2D position pair for current satellite
    
    def get_3D_position(self) -> tuple[float, float, int]:
        return (self.x, self.y, self.z) # Return 3D position pair for current satellite


class GroundStation:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.z = 0
        self.radius = 7.5

    def draw(self, screen, colour) -> None:
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def get_2D_position(self) -> tuple[float, float]:
        return (self.x, self.y) # Return 2D position pair for current ground station
    
    def get_3D_position(self) -> tuple[float, float, int]:
        return (self.x, self.y, self.z) # Return 3D position pair for current ground station


class Congestion:
    def __init__(self) -> None:
        self. cell_size = 0
        self.column_num = 0
        self.row_num = 0
        self.grid_density = 0
        self.congestion_map = {}

    def initialize_heatmap(self) -> None:
        # Input sanitization
        if not isinstance(self.grid_density, int):
            raise TypeError("'density' must be an integer")
        if self.grid_density <= 0:
            raise TypeError("'density' must be above 0")
        
        # Get the aspect ration of the program window.
        aspect_ratio = WINDOW_WIDTH / WINDOW_HEIGHT
        # Get the pixel size of the cells.
        self.cell_size = WINDOW_WIDTH / aspect_ratio / self.grid_density
        # Get the number of columns and rows for our cell grid.
        self.column_num = int(WINDOW_WIDTH / self.cell_size)
        self.row_num = int(WINDOW_HEIGHT / self.cell_size)
    
    def generate_congestion_heatmap(self, grid_density=10) -> dict:
        self.grid_density = grid_density
        self.initialize_heatmap()
        self.congestion_map = {}
        # Go through each cell in the grid
        for col in range(self.column_num):
            for row in range(self.row_num):
                # Ensure that we don't create unnecessary cells where satellites won't travel.
                if (row * self.cell_size) < (WINDOW_HEIGHT / 2 - AMPLITUDE) or (row * self.cell_size) >= (WINDOW_HEIGHT / 2 + AMPLITUDE):
                    continue
                else:
                    scale = 1.0
                    size = self.column_num * self.row_num
                    random_numbers = np.random.exponential(scale, size)
                    # Scale the values to be within the desired range
                    random_numbers = random_numbers / np.max(random_numbers) * CONGESTION_COMPLEXITY + 1
                    # Round the values to the nearest integer
                    random_numbers = np.round(random_numbers)
                    # Assign the first random number in the list to the congestion map cell
                    self.congestion_map[((col*self.cell_size, row*self.cell_size), ((col+1)*self.cell_size, (row+1)*self.cell_size))] = random_numbers[0]
                    # Remove that number out of the list
                    random_numbers = random_numbers[1:]

        return self.congestion_map
    
    def refresh_congestion_heatmap(self) -> dict:
        # Change up to 2% of all cells inside the heatmap.
        cells_to_change = np.random.randint(0, int(self.column_num * self.row_num / 50))

        # Select the row and cells and modift them
        for i in range(cells_to_change):
            row_to_change = np.random.randint(1, self.row_num) - 1
            col_to_change = np.random.randint(1, self.column_num) - 1

            # Makes sure that the select cell is within 
            if not ((row_to_change * self.cell_size) < (WINDOW_HEIGHT / 2 - AMPLITUDE) or (row_to_change * self.cell_size) >= (WINDOW_HEIGHT / 2 + AMPLITUDE)):
                # The chosen cell in the grid
                scale = 1.0
                size = self.column_num * self.row_num
                random_numbers = np.random.exponential(scale, size)
                # Scale the values to be within the desired range
                random_numbers = random_numbers / np.max(random_numbers) * CONGESTION_COMPLEXITY + 1
                # Round the values to the nearest integer
                random_numbers = np.round(random_numbers)
                # Assign the first random number in the list to the congestion map cell
                self.congestion_map[((col_to_change*self.cell_size, row_to_change*self.cell_size), ((col_to_change+1)*self.cell_size, (row_to_change+1)*self.cell_size))] = \
                    random_numbers[np.random.randint(0, len(random_numbers))]

        return self.congestion_map
