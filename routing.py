
#
#   PROJECT : Satellite Network Simulation
# 
#   FILENAME : routing.py
# 
#   DESCRIPTION :
#       Simulate a network of satellite nodes to compare performance 
#       compared to regular ground nodes.
# 
#   FUNCTIONS :
#       PacketRouting.PacketRouting()
#       PacketRouting.edges_between_nodes()
#       PacketRouting.closest_LEO_nodes_to_endpoints()
#       PacketRouting.draw()
#       PacketRouting.dijskra_algorithm()
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


from math import dist
import pygame

from constants import *


class PacketRouting:
    def __init__(self, LEO_node_positions, MEO_node_positions, endpoint_positions, congestion_map):
        self.LEO_node_positions = LEO_node_positions
        self.LEO_MAX_REACHABILITY = LEO_MAX_REACHABILITY

        self.MEO_node_positions = MEO_node_positions
        self.MEO_MAX_REACHABILITY = MEO_MAX_REACHABILITY
        
        self.node_positions = LEO_node_positions + MEO_node_positions
        self.endpoint_positions = endpoint_positions

        self.congestion_map = congestion_map
    
    # Generating all possible edges between satellites, as well as their distance (cost)
    def edges_between_nodes(self):
        self.edges = {}
        self.node_cost = {}

        for i in range(len(self.node_positions)):                   # Loop through all node positions
            self.node_cost[self.node_positions[i]] = float("inf")   # Set the initial cost for each node to infinity
            for j in range(i+1, len(self.node_positions)):          # Loop through all other node positions
                if self.node_positions[i] == self.node_positions[j]:
                    continue    # Skip if the two nodes are the same
                else:
                    # Calculate the distance between the two nodes
                    distance_between_nodes = dist(self.node_positions[i], self.node_positions[j])

                    # Check if both nodes are in LEO orbit
                    if (self.node_positions[i][2] == LEO_ORBIT_HEIGHT) and (self.node_positions[j][2] == LEO_ORBIT_HEIGHT):
                        # Check if the distance is within reachability and the edge doesn't already exist
                        if (distance_between_nodes <= self.LEO_MAX_REACHABILITY) and ((self.node_positions[j], self.node_positions[i]) not in self.edges):
                            # Add the edge with a cost of twice the distance between the nodes
                            self.edges[(self.node_positions[i], self.node_positions[j])] = distance_between_nodes * 2
                    
                    # Check if both nodes are in MEO orbit
                    elif (self.node_positions[i][2] == MEO_ORBIT_HEIGHT) and (self.node_positions[j][2] == MEO_ORBIT_HEIGHT):
                        # Check if the distance is within reachability and the edge doesn't already exist
                        if (distance_between_nodes <= self.MEO_MAX_REACHABILITY) and ((self.node_positions[j], self.node_positions[i]) not in self.edges):
                            # Add the edge with a cost equal to the distance between the nodes
                            self.edges[(self.node_positions[i], self.node_positions[j])] = distance_between_nodes * 1
                    
                    # If one node is in LEO orbit and the other is in MEO orbit
                    else:
                        # Calculate the distance between the two nodes ignoring the z-coordinate
                        distance_between_nodes = dist(self.node_positions[i][:-1], self.node_positions[j][:-1])
                        # Check if the distance is within reachability and the edge doesn't already exist
                        if (distance_between_nodes <= self.MEO_MAX_REACHABILITY) and ((self.node_positions[j], self.node_positions[i]) not in self.edges):
                            # Add the edge with a cost of 2.5 times the distance between the nodes
                            self.edges[(self.node_positions[i], self.node_positions[j])] = distance_between_nodes * 2.5

            # Loop through all cells in the congestion map
            for (cell_top_left_points, cell_bottom_right_points), congestion_level in self.congestion_map.items():
                # Check if the current node is within the current cell
                if cell_top_left_points[0] <= self.node_positions[i][0] <= cell_bottom_right_points[0] and cell_top_left_points[1] <= self.node_positions[i][1] <= cell_bottom_right_points[1]:
                    # Update the cost of the node based on the congestion level of the cell
                    self.node_cost[self.node_positions[i]] = distance_between_nodes * congestion_level - 1
                    break   # Exit the loop

        # Return node edge dict
        return self.edges, self.node_cost
    
    def closest_LEO_nodes_to_endpoints(self):
        self.LEO_nodes_endpoints_link = [] # Initialize coordinate pair list
        for endpoint in self.endpoint_positions:    # Find nearest node for each endpoint
            min_dist = float("inf") # Create initial float variable with infinity value
            
            for node in self.LEO_node_positions:    # Loop through each node to find nearest to endpoint
                distance_to_endpoint = dist(endpoint, node) # Get distance between node and endpoint
                
                for (cell_top_left_points, cell_bottom_right_points), congestion_level in self.congestion_map.items():
                    if cell_top_left_points[0] <= node[0] <= cell_bottom_right_points[0] and cell_top_left_points[1] <= node[1] <= cell_bottom_right_points[1]:
                        if distance_to_endpoint * congestion_level < min_dist: # If distance is smaller than current nearest node, including its congestion,
                            min_dist = distance_to_endpoint * congestion_level # Set it as the new nearest node
                            endpoint_node = node    # Save node position
                        break
            
            self.LEO_nodes_endpoints_link.append((endpoint_node, endpoint))    # Add node and endpoint positions to list
        # Return nearest nodes for each endpoints
        return self.LEO_nodes_endpoints_link

    def draw(self, screen, colour, points):
        pygame.draw.lines(screen, colour, False, [point[0:2] for point in points], 2)

    def dijskra_algorithm(self):
        self.closest_LEO_nodes_to_endpoints()           # Find the closest LEO nodes to the endpoints
        src_node = self.LEO_nodes_endpoints_link[0][0]  # Set the source node to the first LEO node
        dst_node = self.LEO_nodes_endpoints_link[-1][0] # Set the destination node to the last LEO node
    
        
        self.edges_between_nodes()  # Get the edges of each node
        adjancent_nodes = {v: {} for v in self.node_positions}  # Initialize an adjacency graph

        for (u, v), w_uv in self.edges.items(): # Iterate through all edges
            adjancent_nodes[u][v] = w_uv        # Add edge from u to v with weight w_uv
            adjancent_nodes[v][u] = w_uv        # Add edge from v to u with weight w_uv

        node_path = []          # Initialize path
        shortest_distance = {}  # Temporary shortest distance node to node
        parent_node = {}        # Keep track of previous nodes traversed
        cumulative_distance = 0 # Keep track of cumulative distance of path

        for node in adjancent_nodes:                # Iterate through all nodes in the adjacency graph
            shortest_distance[node] = float("inf")  # Set shortest distance to infinity
        shortest_distance[src_node] = 0             # Set shortest distance of source node to 0

        while adjancent_nodes:                      # While there are still nodes in the adjacency graph
            minimum_distance_node = None            # Initialize minimum distance node as None
            for node in adjancent_nodes:            # Iterate through all nodes in the adjacency graph
                if minimum_distance_node is None:   # If minimum distance node is None
                    minimum_distance_node = node    # Set minimum distance node to current node
                # If current node has shorter distance than minimum distance node
                elif shortest_distance[node] < shortest_distance[minimum_distance_node]:
                    minimum_distance_node = node    # Set minimum distance node to current node

            # Iterate through all child nodes of minimum distance node
            for child_node, distance in adjancent_nodes[minimum_distance_node].items():
                # If a shorter path is found to child node
                if distance + shortest_distance[minimum_distance_node] + self.node_cost[child_node] < shortest_distance[child_node]:
                     # Update shortest distance of child node
                    shortest_distance[child_node] = distance + shortest_distance[minimum_distance_node] + self.node_cost[child_node]
                    # Set parent of child node to minimum distance node
                    parent_node[child_node] = minimum_distance_node

            adjancent_nodes.pop(minimum_distance_node)  # Remove the current minimum distance node from the adjacency graph

        current_node = dst_node # Initialize the current node to the destination node

        # Build the path from the destination node to the source node by following parent nodes
        while current_node != src_node:
            try:
                # Add the current node to the beginning of the path
                node_path.insert(0, current_node)
                # Update the total cost by adding the cost of moving from the current node to its parent
                cumulative_distance += shortest_distance[current_node] - shortest_distance[parent_node[current_node]]
                # Set the current node to its paren
                current_node = parent_node[current_node]
            except KeyError:
                print("path is not reachable")
                break

        node_path.insert(0, src_node)   # Add the source node to the beginning of the path

        return node_path, cumulative_distance   # Return node path of shortest distance, along with its distance
