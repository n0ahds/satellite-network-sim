"""
    PROJECT : Satellite Network Simulation

    FILENAME : constants.py

    DESCRIPTION :
        Simulate a network of satellite nodes to compare performance 
        compared to regular ground nodes.

    FUNCTIONS :
        ...

    NOTES :
        - ...

    AUTHOR(S) : Noah F. A. Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

    CHANGES :
        - ...

    VERSION     DATE        WHO             DETAILS
    0.0.1a      2022.11.26  Noah            Creation of project.
    0.0.2a      2023.01.09  Noah            Basic simulation of LEO satellite constellation.
    0.0.2b      2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
    0.0.2c      2023.01.21  Noah/Ranul      Added distortion to LEO satellite orbit to better represent Mercator Projection.
    0.1.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
    0.1.1       2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
    0.2.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
    0.3.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
"""

# Window size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 960

# Frame rate of program
FPS = 5

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

CONGESTION_COMPLEXITY = 10   # Determine how many levels of congestion there is in the simulation
CONGESTION_GRID_DENSITY = 30    # Sets the density of rows and columns in the congestion grid
HEAT_MAP_REFRESH = 2    # How frequent the congestion map generates a new heatmap

# How many LEO and MEO satellites are in orbit
MAX_LEO_SATELLITE_COUNT = 500
MAX_MEO_SATELLITE_COUNT = 125

# How far LEO and MEO satellites can reach other satellites
LEO_MAX_REACHABILITY = 75
MEO_MAX_REACHABILITY = 250  

# How fast the satellites move (will alter orbit)
SIMULATION_SPEED_MULTIPLIER = 1/500


#NOTE: Sin wave data

LEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.08333333333333333333333333333333))
MEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.14285714285714285714285714285714))
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10   # Amplitude for LEO satellite orbit path


#NOTE: Satellite positions

# Orbit height for LEO and MEO satellites (km)
LEO_ORBIT_HEIGHT = 45
MEO_ORBIT_HEIGHT = 450
