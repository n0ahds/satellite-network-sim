""" PROJECT : Satellite Network Simulation

    FILENAME : visuals.py

    DESCRIPTION :
        Simulate a network of satellite nodes to compare performance 
        compared to regular ground nodes.

    FUNCTIONS :
        draw_entity()
        draw_line()

    NOTES :
        - ...

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

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

import pygame
import numpy as np

import settings
from entities import LEOSatellite, MEOSatellite, GroundStation, Congestion


def draw_entity(
        screen: pygame.display,
        entity: LEOSatellite | MEOSatellite | GroundStation,
        colour: tuple[int, int, int] = None,
) -> None:
    if colour is not None:
        pygame.draw.circle(screen, colour, (entity.x, entity.y), entity.width)
    else:
        pygame.draw.circle(screen, entity.colour,
                           (entity.x, entity.y), entity.width)


def draw_line(
        screen: pygame.display,
        points: tuple[tuple, tuple],
        colour: tuple[int, int, int] = settings.BLACK
) -> None:
    pygame.draw.lines(screen, colour, False, [
                      point[0:2] for point in points], 2)


def draw_congestion(screen: pygame.display, congestion: Congestion) -> None:
    # Draw the heat map to visualize the congestion
    for (cell_top_left_points, cell_bottom_right_points), congestion_level in congestion.congestion_map.items():
        cell = pygame.Surface(
            (congestion.cell_size, congestion.cell_size), pygame.SRCALPHA)
        (30 * congestion_level)
        cell.fill((225, int(255 - np.interp(np.exp(np.interp(congestion_level,
                  [1, 5], [0, 1])), [np.exp(0), np.exp(1)], [65, 254])), 64, 80))
        screen.blit(cell, cell_top_left_points)
