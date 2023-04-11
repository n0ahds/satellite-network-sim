""" PROJECT : Satellite Network Simulation

    FILENAME : constants.py

    FUNCTIONS :
        n/a

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
"""

# Window size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 960

# Frame rate of program
FPS = 50

# PyGame colours
WHITE = (255, 255, 255)
DARK_GRAY = (105, 105, 105)
BLACK = (0, 0, 0)
RED = (247, 37, 133)
ORANGE = (252, 132, 3)
GREEN = (110, 235, 38)
BLUE = (89, 108, 217)
PURPLE = (139, 0, 139)

LEO_COLOUR = (105, 55, 2)
MEO_COLOUR = (55, 105, 2)
GROUND_STATION_COLOUR = (247, 37, 133)
LINE_COLOUR = (50, 50, 50)


#NOTE: Simulation variables

# Determine how many levels of congestion there is in the simulation.
CONGESTION_COMPLEXITY = 10
# Sets the density of rows and columns in the congestion grid.
CONGESTION_GRID_DENSITY = 30
# How frequent the congestion map generates a new heatmap.
HEAT_MAP_REFRESH = 2

# How many LEO and MEO satellites are in orbit.
MAX_LEO_SATELLITE_COUNT = 500
MAX_MEO_SATELLITE_COUNT = 125

# How far LEO and MEO satellites can reach other satellites.
LEO_MAX_REACHABILITY = 75
MEO_MAX_REACHABILITY = 250  

# How fast the satellites move (will alter orbit).
SIMULATION_SPEED_MULTIPLIER = 1/500

# How fast each layer moves compare to each other.
LEO_SPEED = 1
MEO_SPEED = 0.5


#NOTE: Sin wave data

LEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.08333333333333333333333333333333))
MEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.14285714285714285714285714285714))
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10   # Amplitude for LEO satellite orbit path


#NOTE: Satellite positions

# Orbit height for LEO and MEO satellites (km)
LEO_ORBIT_HEIGHT = 45
MEO_ORBIT_HEIGHT = 450
