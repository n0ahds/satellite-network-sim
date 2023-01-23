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
#

from math import cos


# Window size
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
SCALE = 5
FPS = 60

# PyGame colours
WHITE = (255, 255, 255)
RED = (230, 57, 70)
ORANGE = (247, 127, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Astronomy
GRAVITATIONAL_CONSTANT = 6.67428e-11    # Nm^2 / kg^2
EARTH_MASS = 5.9722 * 10**24    # kg
EARTH_RADIUS = 6.3781 * 10**6   # m
EARTH_MESOSPHERE = 85   # km

# Starlink v2.0
ORBIT_HEIGHT = 550   
TIME_TO_COMPLETE_ORBIT = 108    # minutes (seconds for simulation) 
SATELLITE_MASS = 1250

# Sin wave data
FREQUENCY = 1 / (WINDOW_WIDTH / (1.3))  # Ensures a constellation that will never loop on itself. (frequency = 0.0007222222222222223)
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10
SATELLITE_SPEED = WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT * cos(WINDOW_WIDTH)
MAX_SATELLITE_COUNT = 540
