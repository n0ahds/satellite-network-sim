#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : main.py
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
#   0.0.2a      2023.01.09  Noah            Basic simulation of LEO satellite constellation.
#   0.0.2b      2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
#   0.0.2c      2023.01.21  Noah/Ranul      Added distortion to LEO satellite orbit to better represent Mercator Projection.
#   0.1.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
#   0.1.1a      2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
#

import pygame
from pygame.locals import *
import sys

from simulation import LEOSatellite, MEOSatellite, GroundStation
from routing import PacketRouting
from constants import *


def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Satellite Orbit")
    
    bg = pygame.image.load("worldmap_light.png").convert()
    bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

    orbit_constellation_leo = []
    orbit_constellation_meo = []
    endpoints = []

    for i in range(0, MAX_LEO_SATELLITE_COUNT):
        orbit_constellation_leo.append(LEOSatellite(delay=i * WINDOW_WIDTH))

    for i in range(0, MAX_MEO_SATELLITE_COUNT):
        orbit_constellation_meo.append(MEOSatellite(delay=i * WINDOW_WIDTH))

    endpoints.append(GroundStation(x=485, y=294))
    endpoints.append(GroundStation(x=1475, y=600))

    #endpoints.append(GroundStation(x=485, y=600))
    #endpoints.append(GroundStation(x=1475, y=300))

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            # 'X' Button
            if event.type == pygame.QUIT:
                running = False
                continue
        
        real_time_satellite_positions = []
        for satellite in orbit_constellation_leo:
            satellite.update_position()
            real_time_satellite_positions.append(satellite.get_position())

        endpoint_positions = []
        for ground_station in endpoints:
            endpoint_positions.append(ground_station.get_position())

        # Loops through each pair of endpoints
        for i in range(0, len(endpoint_positions), 2):
            packet_routing = PacketRouting(node_positions=real_time_satellite_positions, endpoint_positions=endpoint_positions[i:i+2])
            closest_nodes_to_endpoints = packet_routing.closest_nodes_to_endpoints()
            shortest_path = packet_routing.dijskra_algorithm()

            # Drawing visuals for satellite links
            for j in range(1, len(shortest_path)):
                packet_routing.draw(screen, ORANGE, (shortest_path[j], shortest_path[j-1]))
            # Drawing visuals for endpoint links
            for point_pair in closest_nodes_to_endpoints:
                packet_routing.draw(screen, GREEN, point_pair)

        # Drawing visuals for endpoints
        for ground_station in endpoints:
            ground_station.draw(screen, GREEN)
        # Drawing visuals for satellites
        for satellite in orbit_constellation_leo:
            satellite.draw(screen, RED)

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
