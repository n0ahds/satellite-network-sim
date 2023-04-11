""" PROJECT : Satellite Network Simulation

    FILENAME : main.py

    FUNCTIONS :
        main()

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)
"""

import sys

import pygame
import numpy as np

from simulation import LEOSatellite, MEOSatellite, GroundStation, Congestion
from routing import PacketRouting
from constants import *


def main() -> None:
    pygame.init()

    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
    pygame.display.set_caption("Satellite Orbit")
    
    bg = pygame.image.load("worldmap_light.png").convert()
    bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

    orbit_constellation_leo = []
    orbit_constellation_meo = []
    endpoints = []

    for i in range(0, MAX_LEO_SATELLITE_COUNT):
        orbit_constellation_leo.append(LEOSatellite(delay= WINDOW_WIDTH / MAX_LEO_SATELLITE_COUNT * i * 12 ))

    for i in range(0, MAX_MEO_SATELLITE_COUNT):
        orbit_constellation_meo.append(MEOSatellite(delay=i * WINDOW_WIDTH / MAX_MEO_SATELLITE_COUNT + i * 84))
    
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

    # Counts the amount of times we looped through the main program loop
    loop_counter = 0
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

        loop_counter += 1
        if loop_counter % HEAT_MAP_REFRESH == 0:
            congestion_map = congestion.refresh_congestion_heatmap()
        
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
            cell.fill((225, int(255 - np.interp(np.exp(np.interp(congestion_level, [1, 5], [0, 1])), [np.exp(0), np.exp(1)], [65, 254])), 64, 80))
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

            routing_results = packet_routing.dijskra_algorithm()
            shortest_path = routing_results[0]
            path_distance = routing_results[1]

            # Drawing visuals for satellite links
            for j in range(1, len(shortest_path)):
                packet_routing.draw(screen, LINE_COLOUR, (shortest_path[j], shortest_path[j-1]))
            # Drawing visuals for endpoint links
            for point_pair in closest_LEO_nodes_to_endpoints:
                packet_routing.draw(screen, LINE_COLOUR, point_pair)
            
            text_backdrop = pygame.draw.rect(screen, WHITE, pygame.Rect(45,45, 200,80))
            # Show number of hops
            font = pygame.font.Font(None, 28)
            hops_text = font.render(f"Number of hops: {len(shortest_path) + 1}", True, BLACK)
            screen.blit(hops_text, (50, 50))

            # Show path distance
            font = pygame.font.Font(None, 28)
            hops_text = font.render(f"Path cost: {path_distance:.2f}", True, BLACK)
            screen.blit(hops_text, (50, 75))

            # Show path distance
            font = pygame.font.Font(None, 28)
            hops_text = font.render(f"FPS: {clock.get_fps():.2f}", True, BLACK)
            screen.blit(hops_text, (50, 100))


        # Drawing visuals for satellites
        PATH_TO_DRAW = []
        for satellite in orbit_constellation_leo:
            if not satellite.get_3D_position() in shortest_path:
                satellite.draw(screen, LEO_COLOUR)
            else:
                PATH_TO_DRAW.append(satellite)
        
        for satellite in PATH_TO_DRAW:
            satellite.draw(screen, ORANGE)
        
        # Drawing visuals for satellites
        PATH_TO_DRAW = []
        for satellite in orbit_constellation_meo:
            if not satellite.get_3D_position() in shortest_path:
                satellite.draw(screen, MEO_COLOUR)
            else:
                PATH_TO_DRAW.append(satellite)
        
        for satellite in PATH_TO_DRAW:
            satellite.draw(screen, GREEN)

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
