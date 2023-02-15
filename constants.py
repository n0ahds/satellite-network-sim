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

from math import cos


# Window size
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
SCALE = 5
FPS = 2
SIMULATION_SPEED_MULTIPLIER = 1

# PyGame colours
WHITE = (255, 255, 255)
ORANGE = (247, 127, 0)
RED = (247, 37, 133)
YELLOW = (255, 214, 112)
GREEN = (66, 171, 52)

# Sin wave data
FREQUENCY = 1 / (WINDOW_WIDTH / (1.3))  # Ensures a constellation that will never loop on itself. (frequency = 0.0007222222222222223)
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10   # Amplitude for LEO satellite orbit path
MAX_LEO_SATELLITE_COUNT = 600
TIME_TO_COMPLETE_ORBIT = 60