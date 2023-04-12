""" PROJECT : Satellite Network Simulation

    FILENAME : positioning.py

    DESCRIPTION :
        This program simulates a simple satellite network using Python and pygame. 
        It allows users to create and configure a network of LEO and MEO satellites 
        and ground stations, simulate packet routing, and visualize the network state 
        over time.

    FUNCTIONS :
        update_position()
        get_2D_position()
        get_3D_position()
        closest_LEO_nodes_to_endpoints()
        get_edges_between_nodes()
        get_node_costs()
        initialize_heatmap()
        generate_congestion_heatmap()
        refresh_congestion_heatmap()

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

from math import sin, pi, radians, dist

import numpy as np
import pygame

import settings
from entities import LEOSatellite, MEOSatellite, GroundStation, Congestion


def update_position(satellite: LEOSatellite | MEOSatellite) -> None:
    """ This function updates the position of a satellite based on the program
        time and a predetermined orbit equation.
        
        :param satellite: An instance of LEOSatellite or MEOSatellite.
    """
    # Get program tickrate/clockspeed to calculate our positional values
    time = pygame.time.get_ticks() * satellite.speed * \
        settings.SIMULATION_SPEED_MULTIPLIER + satellite.delay

    # Utilize the sinwave formula to get y-coordinate, using an offset of
    # 'WINDOW_HEIGHT / 2' to center the y-coordinate on the screen.
    satellite.y = settings.AMPLITUDE * \
        sin(2 * pi * satellite.frequency * time +
            radians(satellite.phase)) + settings.WINDOW_HEIGHT / 2

    # Set the x-coordinate to be the time value with WINDOW_WIDTH modulus to
    # prevent x-coordinate from going over WINDOW_WIDTH value.
    satellite.x = time % settings.WINDOW_WIDTH


def get_2D_position(
    entity: LEOSatellite | MEOSatellite | GroundStation
) -> tuple[float, float]:
    """ This function returns the 2D position of an entity.

        :param entity: An instance of LEOSatellite, MEOSatellite or GroundStation.
        :return: A tuple representing the 2D position of the entity.
    """
    return (entity.x, entity.y)


def get_3D_position(
    entity: LEOSatellite | MEOSatellite | GroundStation
) -> tuple[float, float, int]:
    """ This function returns the 3D position of an entity.

        :param entity: An instance of LEOSatellite, MEOSatellite or GroundStation.
        :return: A tuple representing the 3D position of the entity.
    """
    return (entity.x, entity.y, entity.z)


def closest_leo_nodes_to_endpoints(
        leo_satellite_positions: list[tuple[float, float, int]],
        ground_station_positions: list[tuple[float, float, int]],
        node_cost: dict[tuple, float]
) -> list[tuple[tuple, tuple]]:
    """
        This function finds the closest LEO satellite node for each ground station
        endpoint, while considering the cost of the satellite node.

        :param leo_satellite_positions: A list of tuples representing the positions 
        of LEO satellites.
        :param ground_station_positions: A list of tuples representing the positions
        of ground stations.
        :param node_cost: A dictionary with keys as tuples representing the
        positions of LEO satellites and values as floats representing the
        cost of using that satellite.
        :return: A list of tuples where each tuple contains two tuples representing 
        the positions of the closest LEO satellite node andthe corresponding ground 
        station endpoint.
    """
    # Initialize coordinate pair list.
    leo_nodes_endpoints_link = []
    # Find nearest node for each endpoint.
    for endpoint in ground_station_positions:
        # Initial the minimum distance variable with infinity value.
        min_dist = float("inf")
        # Loop through each node to find nearest to endpoint.
        for node in leo_satellite_positions:
            # Get distance between node and endpoint.
            distance_to_endpoint = dist(endpoint, node)
            # If the node is a better fit than previously best fit node.
            if (distance_to_endpoint * node_cost[node] < min_dist) \
                    and distance_to_endpoint < settings.LEO_MAX_REACHABILITY:
                # Set it as the new nearest node and save its position.
                min_dist = distance_to_endpoint * node_cost[node]
                endpoint_node = node
        # Add node and endpoint positions to list
        leo_nodes_endpoints_link.append((endpoint_node, endpoint))
    # Return nearest nodes for each endpoints
    return leo_nodes_endpoints_link


def get_edges_between_nodes(
        all_satellite_positions: list[tuple[float, float, int]],
) -> dict[tuple[tuple, tuple], float]:
    """ Calculates the edges between nodes in a graph.

        This function takes in a list of tuples representing the positions of all 
        satellites and returns a dictionary of reachable edges between nodes with 
        their respective costs. The cost is calculated as the distance between the 
        two nodes, and differs if both nodes are in LEO orbit, MEO orbit, or
        seperate orbits.

        :param all_satellite_positions: A list of tuples representing the 
        positions of all satellites.
        :type all_satellite_positions: list[tuple[float, float, int]]
        :return: A dictionary of edges between nodes with their respective costs.
        :rtype: dict[tuple[tuple, tuple], float]
    """
    edges = {}
    # Iterate through all node positions.
    for i in range(len(all_satellite_positions)):
        # Iterate through all other node positions, not previously iterated in parent loop.
        for j in range(i+1, len(all_satellite_positions)):
            if all_satellite_positions[i] == all_satellite_positions[j]:
                # Skip if the two nodes are the sames
                continue

            # Calculate the distance between the two nodes.
            distance_between_nodes = dist(
                all_satellite_positions[i], all_satellite_positions[j])

            # Check if both nodes are in LEO orbit.
            if (all_satellite_positions[i][2] == settings.LEO_ORBIT_HEIGHT) and (
                    all_satellite_positions[j][2] == settings.LEO_ORBIT_HEIGHT):
                # Check if the distance is within reachability and the edge doesn't already exist.
                if (distance_between_nodes <= settings.LEO_MAX_REACHABILITY) and (
                        (all_satellite_positions[j], all_satellite_positions[i]) not in edges):
                    # Add the edge with a cost of twice the distance between the nodes.
                    edges[(all_satellite_positions[i], all_satellite_positions[j])
                          ] = distance_between_nodes * settings.LEO_LEO_HOP_COST

            # Check if both nodes are in MEO orbit
            elif (all_satellite_positions[i][2] == settings.MEO_ORBIT_HEIGHT) and (
                    all_satellite_positions[j][2] == settings.MEO_ORBIT_HEIGHT):
                # Check if the distance is within reachability and the edge doesn't already exist.
                if (distance_between_nodes <= settings.MEO_MAX_REACHABILITY) and (
                        (all_satellite_positions[j], all_satellite_positions[i]) not in edges):
                    # Add the edge with a cost equal to the distance between the nodes.
                    edges[(all_satellite_positions[i], all_satellite_positions[j])
                          ] = distance_between_nodes * settings.MEO_MEO_HOP_COST

            # If one node is in LEO orbit and the other is in MEO orbit.
            else:
                # Calculate the distance between the two nodes ignoring the z-coordinate.
                distance_between_nodes = dist(
                    all_satellite_positions[i][:-1], all_satellite_positions[j][:-1])
                # Check if the distance is within reachability and the edge doesn't already exist.
                if (distance_between_nodes <= settings.MEO_MAX_REACHABILITY) and (
                        (all_satellite_positions[j], all_satellite_positions[i]) not in edges):
                    # Include the z-coordinate in the distance metric.
                    distance_between_nodes = dist(
                        all_satellite_positions[i], all_satellite_positions[j])
                    # Add the edge with a cost of 2.5 times the distance between the nodes.
                    edges[(all_satellite_positions[i], all_satellite_positions[j])
                          ] = distance_between_nodes * settings.LEO_MEO_HOP_COST
    return edges


def get_node_costs(
        all_satellite_positions: list[tuple[float, float, int]],
        congestion_map: dict[tuple[tuple, tuple], int]
) -> dict[tuple, float]:
    """ Calculates the cost for each node based on its position and the 
        congestion level of the cell it is in.

        :param all_satellite_positions: A list of tuples representing the 
        positions of all nodes. Each tuple contains the x and y coordinates of 
        the node and its index.
        :param congestion_map: A dictionary representing the congestion map. The 
        keys are tuples representing the top left and bottom right points of each 
        cell. The values are integers representing the congestion level of each cell.
        :return: A dictionary where the keys are tuples representing the positions 
        of all nodes and the values are floats representing the cost for each node.
    """
    # Set the initial cost for each node to infinity.
    node_cost = {all_satellite_positions[i]: float(
        "inf") for i in range(len(all_satellite_positions))}
    # Iterate through all node positions.
    for i in range(len(all_satellite_positions)):
        # Iterate through all cells in the congestion map.
        for (cell_top_left_points, cell_bottom_right_points
             ), congestion_level in congestion_map.items():
            # Check if the current node is within the current cell.
            if cell_top_left_points[0] <= all_satellite_positions[i][0] <= cell_bottom_right_points[0] and \
                    cell_top_left_points[1] <= all_satellite_positions[i][1] <= cell_bottom_right_points[1]:
                # Update the cost of the node based on the congestion level of the cell.
                node_cost[all_satellite_positions[i]
                          ] = settings.WINDOW_HEIGHT / 2 * congestion_level
                break
    return node_cost


def initialize_heatmap(congestion: Congestion) -> None:
    """ Initializes the heatmap by calculating the cell size, number of 
        columns and rows for the cell grid based on the program window's 
        aspect ratio and the grid density.

        :param congestion: Congestion object with grid_density attribute.
        :type congestion: Congestion
        :raises TypeError: If congestion.grid_density is not an integer or if it is less than or equal to 0.
    """
    # Input sanitization
    if not isinstance(congestion.grid_density, int):
        raise TypeError("'density' must be an integer")
    if congestion.grid_density <= 0:
        raise TypeError("'density' must be above 0")

    # Get the aspect ration of the program window.
    aspect_ratio = settings.WINDOW_WIDTH / settings.WINDOW_HEIGHT
    # Get the pixel size of the cells.
    congestion.cell_size = settings.WINDOW_WIDTH / \
        aspect_ratio / congestion.grid_density
    # Get the number of columns and rows for our cell grid.
    congestion.column_num = int(settings.WINDOW_WIDTH / congestion.cell_size)
    congestion.row_num = int(settings.WINDOW_HEIGHT / congestion.cell_size)


def generate_congestion_heatmap(congestion) -> dict:
    """ Generates a congestion heatmap by assigning random congestion levels 
        to each cell in the grid.

        :param congestion: An instance of the Congestion class.
        :return: A dictionary representing the congestion map. The keys are 
        tuples representing the top left and bottom right points of each cell. 
        The values are integers representing the congestion level of each cell.
    """
    initialize_heatmap(congestion)
    # Go through each cell in the grid
    for col in range(congestion.column_num):
        for row in range(congestion.row_num):
            # Ensure that we don't create unnecessary cells where satellites won't travel.
            if (row * congestion.cell_size) < (settings.WINDOW_HEIGHT / 2 - settings.AMPLITUDE) or (
                    row * congestion.cell_size) >= (settings.WINDOW_HEIGHT / 2 + settings.AMPLITUDE):
                continue
            else:
                scale = 1.0
                size = congestion.column_num * congestion.row_num
                random_numbers = np.random.exponential(scale, size)
                # Scale the values to be within the desired range
                random_numbers = random_numbers / \
                    np.max(random_numbers) * settings.CONGESTION_COMPLEXITY + 1
                # Round the values to the nearest integer
                random_numbers = np.round(random_numbers)
                # Assign the first random number in the list to the congestion map cell
                congestion.congestion_map[((col*congestion.cell_size, row*congestion.cell_size), ((
                    col+1)*congestion.cell_size, (row+1)*congestion.cell_size))] = random_numbers[0]
                # Remove that number out of the list
                random_numbers = random_numbers[1:]

    return congestion.congestion_map


def refresh_congestion_heatmap(congestion: Congestion) -> dict:
    """ Refreshes the congestion heatmap by randomly changing the congestion 
        levels of up to 2% of all cells.

        :param congestion: An instance of the Congestion class.
        :return: A dictionary representing the updated congestion map. The keys 
        are tuples representing the top left and bottom right points of each cell. 
        The values are integers representing the congestion level of each cell.
    """
    # Change up to 2% of all cells inside the heatmap.
    cells_to_change = np.random.randint(
        0, int(congestion.column_num * congestion.row_num / 50))

    # Select the row and cells and modift them
    for i in range(cells_to_change):
        row_to_change = np.random.randint(1, congestion.row_num) - 1
        col_to_change = np.random.randint(1, congestion.column_num) - 1

        # Makes sure that the select cell is within
        if not ((row_to_change * congestion.cell_size) < (settings.WINDOW_HEIGHT / 2 - settings.AMPLITUDE) or (
                row_to_change * congestion.cell_size) >= (settings.WINDOW_HEIGHT / 2 + settings.AMPLITUDE)):
            # The chosen cell in the grid
            scale = 1.0
            size = congestion.column_num * congestion.row_num
            random_numbers = np.random.exponential(scale, size)
            # Scale the values to be within the desired range
            random_numbers = random_numbers / \
                np.max(random_numbers) * settings.CONGESTION_COMPLEXITY + 1
            # Round the values to the nearest integer
            random_numbers = np.round(random_numbers)
            # Assign the first random number in the list to the congestion map cell
            congestion.congestion_map[
                ((col_to_change*congestion.cell_size, row_to_change*congestion.cell_size),
                 ((col_to_change+1) * congestion.cell_size, (row_to_change+1)*congestion.cell_size))
            ] = random_numbers[np.random.randint(0, len(random_numbers))]

    return congestion.congestion_map
