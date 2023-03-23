#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : constants.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
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

# Window size
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
SCALE = 5
FPS = 15
SIMULATION_SPEED_MULTIPLIER = 5

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
#LEO_COLOUR = (100, 100, 100)
#MEO_COLOUR = (25, 25, 25)
GROUND_STATION_COLOUR = (247, 37, 133)
LINE_COLOUR = (50, 50, 50)

# Simulation variables
CONGESTION_COMPLEXITY = 10   # Determine how many levels of congestion there is in the simulation
CONGESTION_GRID_DENSITY = 30    # Sets the density of rows and columns in the congestion grid
HEAT_MAP_REFRESH = 30
LEO_MAX_REACHABILITY = 75
MEO_MAX_REACHABILITY = 250

# Sin wave data
LEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.3))  # Ensures a constellation that will never loop on itself. (frequency = 0.0007222222222222223)
MEO_FREQUENCY = 1 / (WINDOW_WIDTH / (0.3))
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10   # Amplitude for LEO satellite orbit path
MAX_LEO_SATELLITE_COUNT = 600
MAX_MEO_SATELLITE_COUNT = 110
TIME_TO_COMPLETE_ORBIT = 6

# Satellite positions
LEO_ORBIT_HEIGHT = 45
MEO_ORBIT_HEIGHT = 450