""" PROJECT : Satellite Network Simulation

    FILENAME : routing.py

    DESCRIPTION :
        This program simulates a simple satellite network using Python and pygame. 
        It allows users to create and configure a network of LEO and MEO satellites 
        and ground stations, simulate packet routing, and visualize the network state 
        over time.

    FUNCTIONS :
        Algorithms.dijskra()

    NOTES :
        - ...

    AUTHOR(S) : Noah Da Silva    START DATE : 2022.11.26 (YYYY.MM.DD)

    CHANGES :
        - ...

    VERSION     DATE        WHO             DETAILS
    0.1.0       2022.11.26  Noah            Creation of project.
    0.2.0       2023.01.09  Noah            Basic simulation of LEO satellite constellation.
    0.2.1       2023.01.19  Noah            Advanced simulation of LEO satellite constellation.
    0.2.2       2023.01.21  Noah            Added some distortion to LEO satellite orbit to better represent Mercator Projection.
    0.3.0       2023.01.22  Noah            Added path from ground station to nearest satellite and shortest path algorithm.
    0.3.1       2023.01.22  Noah            Allows to run multiple endpoint (ground station) pairs at once (not recommended).
    0.4.0       2023.03.17  Noah            Added MEO satellite constellation into routing calculations.
    0.5.0       2023.03.22  Noah            Added load-balancing in form of a dynamic heatmap.
    1.0.0       2023.04.07  Noah            Rewrote the program for efficiency and better dynamic adjustments.
"""

class Algorithms:
    def dijskra(
            all_satellite_positions: list[tuple[float, float, int]],
            leo_nodes_endpoints_link: list[tuple[tuple, tuple]],
            node_cost: dict[tuple, float],
            edges: dict[tuple[tuple, tuple], float],
    ) -> tuple[list[tuple[float, float, int]], float]:
        """ This function applies Dijkstra's algorithm to find the shortest path
            between two nodes.

            :param all_satellite_positions: A list of tuples representing the
            positions of all satellites.
            :param leo_nodes_endpoints_link: A list of tuples where each tuple
            contains two tuples representing the positions of the closest LEO
            satellite node and the corresponding ground station endpoint.
            :param node_cost: A dictionary with keys as tuples representing the
            positions of Leo satellites and values as floats representing the cost
            of using that satellite.
            :param edges: A dictionary with keys as tuples representing pairs of
            connected nodes and values as floats representing the distance between
            those nodes.
            :return: A tuple containing a list of tuples representing the positions
            of nodes along the shortest path and a float representing the total
            distance along that path.
        """
        # Set the source node to the first LEO node
        src_node = leo_nodes_endpoints_link[0][0]
        # Set the destination node to the last LEO node
        dst_node = leo_nodes_endpoints_link[-1][0]

        # Initialize an adjacency graph
        adjancent_nodes = {v: {} for v in all_satellite_positions}

        # Iterate through all edges
        for (u, v), w_uv in edges.items():
            # Add edge from u to v with weight w_uv
            adjancent_nodes[u][v] = w_uv
            # Add edge from v to u with weight w_uv
            adjancent_nodes[v][u] = w_uv

        # Initialize path
        node_path = []
        # Temporary shortest distance node to node
        shortest_distance = {}
        # Keep track of previous nodes traversed
        parent_node = {}
        # Keep track of cumulative distance of path
        cumulative_distance = 0

        # Iterate through all nodes in the adjacency graph
        for node in adjancent_nodes:
            # Set shortest distance to infinity
            shortest_distance[node] = float("inf")
        # Set shortest distance of source node to 0
        shortest_distance[src_node] = 0

        # While there are still nodes in the adjacency graph
        while adjancent_nodes:
            # Initialize minimum distance node as None
            minimum_distance_node = None
            # Iterate through all nodes in the adjacency graph
            for node in adjancent_nodes:
                # If minimum distance node is None
                if minimum_distance_node is None:
                    # Set minimum distance node to current node
                    minimum_distance_node = node
                # If current node has shorter distance than minimum distance node
                elif shortest_distance[node] < shortest_distance[minimum_distance_node]:
                    # Set minimum distance node to current node
                    minimum_distance_node = node

            # Iterate through all child nodes of minimum distance node
            for child_node, distance in adjancent_nodes[minimum_distance_node].items():
                # If a shorter path is found to child node
                if distance + shortest_distance[minimum_distance_node] + node_cost[child_node] < shortest_distance[child_node]:
                    # Update shortest distance of child node
                    shortest_distance[child_node] = distance + \
                        shortest_distance[minimum_distance_node] + \
                        node_cost[child_node]
                    # Set parent of child node to minimum distance node
                    parent_node[child_node] = minimum_distance_node

            # Remove the current minimum distance node from the adjacency graph
            adjancent_nodes.pop(minimum_distance_node)

        # Initialize the current node to the destination node
        current_node = dst_node
        # Build the path from the destination node to the source node by following parent nodes
        while current_node != src_node:
            try:
                # Add the current node to the beginning of the path
                node_path.insert(0, current_node)
                # Update the total cost by adding the cost of moving from the current node to its parent
                cumulative_distance += shortest_distance[current_node] - \
                    shortest_distance[parent_node[current_node]]
                # Set the current node to its paren
                current_node = parent_node[current_node]
            except KeyError:
                print("path is not reachable")
                break
        # Add the source node to the beginning of the path
        node_path.insert(0, src_node)

        # Return node path of shortest distance, along with its distance
        return node_path, cumulative_distance
