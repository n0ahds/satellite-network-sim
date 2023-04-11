""" PROJECT : Satellite Network Simulation

    FILENAME : settings.py

    DESCRIPTION :
        This module simulates a simple satellite network using Python and pygame. 
        It allows users to create and configure a network of LEO and MEO satellites 
        and ground stations, simulate packet routing, and visualize the network state 
        over time.

    FUNCTIONS :
        n/a

    NOTES :
        - ...

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

    CHANGES :
        - ...

    VERSION     DATE        WHO             DETAILS
    0.1.0       2022.11.26  Noah            Creation of project.
    0.2.0       2023.01.09  Noah            Basic simulation of LEO satellite constellation.
    0.2.1       2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
    0.2.2       2023.01.21  Noah/Ranul      Added some distortion to LEO satellite orbit to better represent Mercator Projection.
    0.3.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
    0.3.1       2023.01.22  Noah            Allows to run multiple endpoint (ground station) pairs at once (not recommended).
    0.4.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
    0.5.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
    1.0.0       2023.04.07  Noah            Rewrote the program for efficiency and better dynamic adjustments.
"""

# Window size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 960
RESOLUTION = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Frame rate of program
FPS = 50

# PyGame colours
WHITE = (255, 255, 255)
DARK_GRAY = (105, 105, 105)
BLACK = (0, 0, 0)
RED = (247, 37, 133)
BLUE = (89, 108, 217)
PURPLE = (139, 0, 139)

LEO_INACTIVE_COLOUR = (105, 55, 2)  # Dark orange.
LEO_ACTIVE_COLOUR = (252, 132, 3)  # Orange.
MEO_INACTIVE_COLOUR = (55, 105, 2)  # Dark green.
MEO_ACTIVE_COLOUR = (110, 235, 38)  # Lime green.
GROUND_STATION_COLOUR = (247, 37, 133)  # Hot pink.
LINK_COLOUR = (50, 50, 50)  # Dark gray.

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
MEO_MAX_REACHABILITY = 225

# How fast the satellites move (will alter orbit).
SIMULATION_SPEED_MULTIPLIER = 1/500

# How fast each layer moves compare to each other.
LEO_SPEED = 1
MEO_SPEED = 0.5

# Sin wave data.
LEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.08333333333333333333333333333333))  # 1/12
MEO_FREQUENCY = 1 / (WINDOW_WIDTH / (1.14285714285714285714285714285714))  # 1/7
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10

# Orbit height for LEO and MEO satellites (km).
LEO_ORBIT_HEIGHT = 45
MEO_ORBIT_HEIGHT = 450

# Satellite size on screen (pixels).
LEO_WIDTH = 5
MEO_WIDTH = 6
GROUND_STATION_WIDTH = 7.5
LINK_WIDTH = 2
