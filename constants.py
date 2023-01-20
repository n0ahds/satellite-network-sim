#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : constants.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
#   FUNCTIONS :
#       main()
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

# Window size
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
SCALE = 5
FPS = 60

# PyGame colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Astronomy
GRAVITATIONAL_CONSTANT = 6.67428e-11    # Nm^2 / kg^2
EARTH_MASS = 5.9722 * 10 ** 24  # kg
EARTH_RADIUS = 6.3781 * 10 ** 6 # m

# Starlink v2.0
ORBIT_HEIGHT = 500   
TIME_TO_COMPLETE_ORBIT = 108    # minutes (seconds for simulation) 
SATELLITE_MASS = 1250

# Sin wave data
FREQUENCY = 1 / (WINDOW_WIDTH / (1.3))  # Ensures a constellation that will never loop on itself. (frequency = 0.0007222222222222223)
AMPLITUDE = WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 10
SATELLITE_SPEED = WINDOW_WIDTH / TIME_TO_COMPLETE_ORBIT
MAX_SATELLITE_COUNT = 580