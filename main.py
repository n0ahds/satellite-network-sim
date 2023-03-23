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
#   AUTHOR(S) : Noah F. A. Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
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
#   0.1.1       2023.01.22  Noah            Allows to run multiple endpoint pairs at once (not recommended).
#   0.2.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
#   0.3.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
#


import pygame
from pygame.locals import *
import sys
import numpy as np

from simulation import LEOSatellite, MEOSatellite, GroundStation, Congestion
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
        orbit_constellation_meo.append(MEOSatellite(delay=i * WINDOW_WIDTH * (MAX_LEO_SATELLITE_COUNT / MAX_MEO_SATELLITE_COUNT) / SIMULATION_SPEED_MULTIPLIER))
    
    endpoints.append(GroundStation(x=300, y=275))
    endpoints.append(GroundStation(x=1475, y=615))

    #endpoints.append(GroundStation(x=485, y=295))
    #endpoints.append(GroundStation(x=1000, y=500))

    #endpoints.append(GroundStation(x=370, y=295))
    #endpoints.append(GroundStation(x=300, y=245))

    #endpoints.append(GroundStation(x=870, y=240))
    #endpoints.append(GroundStation(x=1475, y=600))

    #endpoints.append(GroundStation(x=610, y=600))
    #endpoints.append(GroundStation(x=500, y=480))

    #endpoints.append(GroundStation(x=1250, y=240))
    #endpoints.append(GroundStation(x=1600, y=450))

    congestion = Congestion()
    congestion_map = congestion.generate_congestion_heatmap(grid_density=CONGESTION_GRID_DENSITY)

    loop_counter = 0    # Counts the amount of times we looped through the main program loop
    running = True
    while running:

        # Pygame settings
        clock.tick(FPS)
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            # 'X' Button
            if event.type == pygame.QUIT:
                running = False
                continue
        
        # Main code
        loop_counter += 1

        if loop_counter % HEAT_MAP_REFRESH == 0:
            congestion_map = congestion.generate_congestion_heatmap(grid_density=CONGESTION_GRID_DENSITY)
        
        real_time_LEO_satellite_positions = []
        for satellite in orbit_constellation_leo:
            satellite.update_position()
            real_time_LEO_satellite_positions.append(satellite.get_3D_position())

        real_time_MEO_satellite_positions = []
        for satellite in orbit_constellation_meo:
            satellite.update_position()
            real_time_MEO_satellite_positions.append(satellite.get_3D_position())

        endpoint_positions = []
        for ground_station in endpoints:
            endpoint_positions.append(ground_station.get_3D_position())

        # Draw the heat map to visualize the congestion
        for (cell_top_left_points, cell_bottom_right_points), congestion_level in congestion_map.items():
            cell = pygame.Surface((congestion.cell_size, congestion.cell_size), pygame.SRCALPHA)
            (30 * congestion_level)
            cell.fill((155, int(255 - np.interp(np.exp(np.interp(congestion_level, [1, 5], [0, 1])), [np.exp(0), np.exp(1)], [65, 254])), 120, 80))
            screen.blit(cell, cell_top_left_points)

        # Drawing visuals for endpoints
        for ground_station in endpoints:
            ground_station.draw(screen, GROUND_STATION_COLOUR)

        # Loops through each pair of endpoints
        for i in range(0, len(endpoint_positions), 2):
            packet_routing = PacketRouting(
                LEO_node_positions=real_time_LEO_satellite_positions,
                MEO_node_positions=real_time_MEO_satellite_positions,
                endpoint_positions=endpoint_positions[i:i+2],
                congestion_map=congestion_map
            )

            closest_LEO_nodes_to_endpoints = packet_routing.closest_LEO_nodes_to_endpoints()
            shortest_path = packet_routing.dijskra_algorithm()
            # Drawing visuals for satellite links
            for j in range(1, len(shortest_path)):
                packet_routing.draw(screen, LINE_COLOUR, (shortest_path[j], shortest_path[j-1]))
            # Drawing visuals for endpoint links
            for point_pair in closest_LEO_nodes_to_endpoints:
                packet_routing.draw(screen, LINE_COLOUR, point_pair)
            
            # Show number of hops
            font = pygame.font.Font(None, 28)
            hops_text = font.render(f"Number of hops: {len(shortest_path) + 1}", True, BLACK)
            screen.blit(hops_text, (50, 50))

        # Drawing visuals for satellites
        for satellite in orbit_constellation_leo:
            if satellite.get_3D_position() in shortest_path:
                satellite.draw(screen, ORANGE)
            else:
                satellite.draw(screen, LEO_COLOUR)
        
        # Drawing visuals for satellites
        for satellite in orbit_constellation_meo:
            if satellite.get_3D_position() in shortest_path:
                satellite.draw(screen, GREEN)
            else:
                satellite.draw(screen, MEO_COLOUR)

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
