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
SATELLITE_MASS = 1250