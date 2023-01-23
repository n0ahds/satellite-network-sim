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
#       PacketRouting.closest_nodes_to_endpoints()
#       PacketRouting.draw()
#       PacketRouting.dijskra_algorithm()
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

from math import dist
import pygame

from constants import *


class PacketRouting:
    def __init__(self, node_positions, endpoint_positions):
        self.node_positions = node_positions
        self.endpoint_positions = endpoint_positions
        self.MAX_REACHABILITY = 100
        #MAX_REACHABILITY = ORBIT_HEIGHT + (EARTH_RADIUS/1000 + EARTH_MESOSPHERE)
        self.nodes_endpoints_link = []
        self.edges = {}
        self.node_graph = {}
    
    def edges_between_nodes(self):
        self.edges = {}
        # Loop through all nodes
        for i in range(len(self.node_positions)):
            for j in range(len(self.node_positions)):
                if self.node_positions[i] != self.node_positions[j]:
                    distance_between_nodes = dist(self.node_positions[i], self.node_positions[j])
                    if distance_between_nodes <= self.MAX_REACHABILITY:
                        if (self.node_positions[j], self.node_positions[i]) not in self.edges:
                            self.edges[(self.node_positions[i], self.node_positions[j])] = distance_between_nodes
        # Return node edge dict
        return self.edges

    def closest_nodes_to_endpoints(self):
        self.nodes_endpoints_link = [] # Initialize coordinate pair list
        for endpoint in self.endpoint_positions:    # Find nearest node for each endpoint
            min_dist = float("inf") # Create initial float variable with infinity value
            
            for node in self.node_positions:    # Loop through each node to find nearest to endpoint
                distance_to_endpoint = dist(endpoint, node) # Get distance between node and endpoint
                
                if distance_to_endpoint < min_dist: # If distance is smaller than current nearest node,
                    min_dist = distance_to_endpoint # Set it as the new nearest node
                    endpoint_node = node    # Save node position
            
            self.nodes_endpoints_link.append((endpoint_node, endpoint))    # Add node and endpoint positions to list
        # Return nearest nodes for each endpoints
        return self.nodes_endpoints_link  

    def draw(self, screen, colour, points):
        pygame.draw.lines(screen, colour, False, points, 3)

    def dijskra_algorithm(self):
        # Add source node and destionation node
        self.closest_nodes_to_endpoints()
        src_node = self.nodes_endpoints_link[0][0]
        dst_node = self.nodes_endpoints_link[-1][0]
    
        # Create an adjancency graph for the edges of each node
        self.edges_between_nodes()
        adjancent_nodes = {v: {} for v in self.node_positions}
        for (u, v), w_uv in self.edges.items():
            adjancent_nodes[u][v] = w_uv
            adjancent_nodes[v][u] = w_uv

        node_path = []          # Initialize path
        shortest_distance = {}  # Temporary shortest distance node to node
        parent_node = {}        # Keep track of previous nodes traversed

        for node in adjancent_nodes:
            shortest_distance[node] = float("inf")
        shortest_distance[src_node] = 0
        
        while adjancent_nodes:
            minimum_distance_node = None
            for node in adjancent_nodes:
                if minimum_distance_node is None:
                    minimum_distance_node = node
                elif shortest_distance[node] < shortest_distance[minimum_distance_node]:
                    minimum_distance_node = node

            for child_node, distance in adjancent_nodes[minimum_distance_node].items():
                if distance + shortest_distance[minimum_distance_node] < shortest_distance[child_node]:
                    shortest_distance[child_node] = distance + shortest_distance[minimum_distance_node]
                    parent_node[child_node] = minimum_distance_node
            adjancent_nodes.pop(minimum_distance_node)
        
        current_node = dst_node
        while current_node != src_node:
            try:
                node_path.insert(0, current_node)
                current_node = parent_node[current_node]
            except KeyError:
                print("path is not reachable")
                break
        node_path.insert(0, src_node)

        #return shortest_distance[dst_node]  # Return shortest distance value
        return node_path    # Return node path of shortest distance