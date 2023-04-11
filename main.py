""" PROJECT : Satellite Network Simulation

    FILENAME : main.py

    DESCRIPTION :
        Simulate a network of satellite nodes to compare performance 
        compared to regular ground nodes.

    FUNCTIONS :
        main()

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

import sys

import pygame
import numpy as np

import settings
from entities import LEOSatellite, MEOSatellite, GroundStation, Congestion
from positioning import update_position, get_2D_position, get_3D_position, \
    closest_leo_nodes_to_endpoints, get_edges_between_nodes, get_node_costs, \
    initialize_heatmap, generate_congestion_heatmap, refresh_congestion_heatmap
from visuals import draw_entity, draw_line, draw_congestion
from routing import Algorithms


def main() -> None:
    """Main program when pygame loop is located."""
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(settings.RESOLUTION)
    pygame.display.set_caption("Satellite Orbit")

    bg = pygame.image.load("worldmap_light.png").convert()
    bg = pygame.transform.scale(bg, settings.RESOLUTION)

    leo_orbit_constellation = [LEOSatellite(
        delay=settings.WINDOW_WIDTH / settings.MAX_LEO_SATELLITE_COUNT * i * 12
    ) for i in range(settings.MAX_LEO_SATELLITE_COUNT)]

    meo_orbit_constellation = [MEOSatellite(
        delay=settings.WINDOW_WIDTH / settings.MAX_MEO_SATELLITE_COUNT * i * 7
    ) for i in range(settings.MAX_MEO_SATELLITE_COUNT)]

    endpoints = [
        GroundStation(x=300, y=275),
        GroundStation(x=1475, y=615),
    ]

    congestion = Congestion()
    initialize_heatmap(congestion)
    generate_congestion_heatmap(congestion)

    font = pygame.font.Font(None, 28)

    # Counts the amount of times we loop through the main program loop.
    loop_counter = 0

    running = True
    while running:
        tick_speed = clock.tick(settings.FPS)
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            # 'X' button press.
            if event.type == pygame.QUIT:
                running = False
                continue

        loop_counter += 1
        if loop_counter % settings.HEAT_MAP_REFRESH == 0:
            congestion.congestion_map = refresh_congestion_heatmap(congestion)

        leo_satellite_positions = [update_position(satellite) or get_3D_position(
            satellite) for satellite in leo_orbit_constellation]

        meo_satellite_positions = [update_position(satellite) or get_3D_position(
            satellite) for satellite in meo_orbit_constellation]

        endpoint_positions = [get_3D_position(
            ground_station) for ground_station in endpoints]

        node_cost = get_node_costs(
            all_satellite_positions=leo_satellite_positions + meo_satellite_positions,
            congestion_map=congestion.congestion_map
        )
        edges = get_edges_between_nodes(
            all_satellite_positions=leo_satellite_positions + meo_satellite_positions
        )

        leo_nodes_endpoints_link = closest_leo_nodes_to_endpoints(
            leo_satellite_positions=leo_satellite_positions,
            ground_station_positions=endpoint_positions,
            node_cost=node_cost
        )

        routing_results = Algorithms.dijskra(
            all_satellite_positions=leo_satellite_positions + meo_satellite_positions,
            leo_nodes_endpoints_link=leo_nodes_endpoints_link,
            node_cost=node_cost,
            edges=edges
        )
        shortest_path = routing_results[0]
        path_distance = routing_results[1]

        # Draw the congestion heatmap.
        draw_congestion(screen, congestion)

        # Drawing visuals for endpoints.
        for ground_station in endpoints:
            draw_entity(screen, ground_station)

        # Drawing visuals for satellite links.
        for j in range(1, len(shortest_path)):
            draw_line(
                screen=screen,
                points=(shortest_path[j], shortest_path[j-1]),
                colour=settings.LINK_COLOUR
            )
        # Drawing visuals for endpoint links.
        for point_pair in leo_nodes_endpoints_link:
            draw_line(
                screen=screen,
                points=point_pair,
                colour=settings.LINK_COLOUR
            )

        pygame.draw.rect(screen, settings.WHITE, pygame.Rect(25, 25, 200, 80))
        # Show number of hops.
        screen.blit(font.render(
            f"Number of hops: {len(shortest_path) + 1}", True, settings.BLACK), (30, 30))
        # Show path distance.
        screen.blit(font.render(
            f"Path cost: {path_distance:.2f}", True, settings.BLACK), (30, 55))
        # Show fps.
        screen.blit(font.render(
            f"FPS: {clock.get_fps():.2f}", True, settings.BLACK), (30, 80))

        # Drawing visuals for LEO satellites.
        PATH_TO_DRAW = []
        for satellite in leo_orbit_constellation:
            if not get_3D_position(satellite) in shortest_path:
                draw_entity(
                    screen=screen,
                    entity=satellite,
                    colour=settings.LEO_INACTIVE_COLOUR
                )
            else:
                PATH_TO_DRAW.append(satellite)

        for satellite in PATH_TO_DRAW:
            draw_entity(
                screen=screen,
                entity=satellite,
                colour=settings.LEO_ACTIVE_COLOUR
            )

        # Drawing visuals for MEO satellites.
        PATH_TO_DRAW = []
        for satellite in meo_orbit_constellation:
            if not get_3D_position(satellite) in shortest_path:
                draw_entity(
                    screen=screen,
                    entity=satellite,
                    colour=settings.MEO_INACTIVE_COLOUR
                )
            else:
                PATH_TO_DRAW.append(satellite)

        for satellite in PATH_TO_DRAW:
            draw_entity(
                screen=screen,
                entity=satellite,
                colour=settings.MEO_ACTIVE_COLOUR
            )

        pygame.display.update()

    # Ensures PyGame closes correctly.
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
