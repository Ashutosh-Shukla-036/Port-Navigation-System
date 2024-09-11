import networkx as nx
import math
from geopy.distance import geodesic
import folium
import os
import webbrowser

# Distance calculation functions
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1Rad = math.radians(lat1)
    lon1Rad = math.radians(lon1)
    lat2Rad = math.radians(lat2)
    lon2Rad = math.radians(lon2)
    dLat = lat2Rad - lat1Rad
    dLon = lon2Rad - lon1Rad
    a = math.sin(dLat / 2)**2 + math.cos(lat1Rad) * math.cos(lat2Rad) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def geodesicDistance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

def calculateDistance(lat1, lon1, lat2, lon2, method='geodesic'):
    if method == 'haversine':
        return haversine(lat1, lon1, lat2, lon2)
    elif method == 'geodesic':
        return geodesicDistance(lat1, lon1, lat2, lon2)
    else:
        raise ValueError("Invalid method. Choose 'haversine' or 'geodesic'.")

# Static graph of port connections
def constructGraph():
    graph = {
        "Malindi": ["WP1", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP1": ["Lamu", "Kochi", "New Mangalore", "Mumbai", "WP10", "WP2", "Mormugaiort"],
        "Lamu": ["WP2", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP2": ["Kismayo", "Magadishu", "WP3", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "Kismayo": ["Magadishu", "WP3", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "Magadishu": ["WP3", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP3": ["WP4", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP4": ["WP5", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "Bosaso": ["Berbera", "Aden", "Mukalla", "Nishtun", "Salalah", "WP6"],
        "Berbera": ["WP6", "Aden", "Mukalla", "Nishtun"],
        "WP5": ["WP6", "Socotra", "Salalah", "Nishtun"],
        "Aden": ["Mukalla", "WP6"],
        "Nishtun": ["Socotra", "WP6", "WP10", "Mumbai", "Mormugaiort"],
        "Salalah": ["WP6", "WP5", "WP7", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort"],
        "WP7": ["WP5", "WP6", "WP8", "WP10", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort", "Duqm"],
        "Duqm": ["WP8", "WP10", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort"],
        "WP8": ["WP9", "WP10", "Sultan", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort"],
        "WP9": ["Chabahar", "Sultan", "Bandar Abbas", "WP10"],
        "Sultan": ["Chabahar", "Bandar Abbas"],
        "WP10": ["WP11", "WP12"],
        "WP11": ["Kandla"],
        "WP12": ["Mumbai", "WP13", "WP14"],
        "Mumbai": ["WP13", "Mormugaiort"],
        "WP13": ["Mormugaiort", "WP14"],
        "WP14": ["Mormugaiort", "Kochi"]
    }
    return graph

# Add the port and waypoint coordinates
def getPortData():
    return {
        "Malindi": (-3.216, 40.128),
        "Lamu": (-2.194, 40.933),
        "Kismayo": (-0.388, 42.542),
        "Magadishu": (2.022, 45.338),
        "Bosaso": (11.293, 49.179),
        "Berbera": (10.522, 44.992),
        "Aden": (12.810, 44.993),
        "Mukalla": (14.522, 49.147),
        "Nishtun": (15.819, 52.197),
        "Salalah": (16.953, 54.004),
        "Sultan": (23.627, 58.570),
        "Duqm": (19.674, 57.706),
        "Bandar Abbas": (27.169, 56.276),
        "Chabahar": (25.300, 60.595),
        "Socotra": (12.682, 54.079),
        "Kandla": (23.002, 70.218),
        "Mumbai": (18.948, 72.844),
        "Mormugaiort": (15.411, 73.799),
        "New Mangalore": (12.987, 74.812),
        "Kochi": (9.966, 76.271),
        "WP1": (-2.763, 40.640),
        "WP2": (-1.689, 41.759),
        "WP3": (8.898, 51.044),
        "WP4": (11.293, 52.545),
        "WP5": (12.739, 52.741),
        "WP6": (12.861, 50.867),
        "WP7": (17.204, 56.845),
        "WP8": (20.663, 60.051),
        "WP9": (23.334, 60.936),
        "WP10": (22.715, 68.485),
        "WP11": (22.586, 69.558),
        "WP12": (20.082, 69.355),
        "WP13": (17.225, 72.942),
        "WP14": (13.765, 74.293)
    }

# Optimized function to construct graph with distances stored in a dictionary
def constructPositionedGraphOptimized(portData, method='geodesic'):
    graph = nx.Graph()
    edge_weights = {}
    
    for port, coords in portData.items():
        graph.add_node(port, pos=coords)
    
    connections = constructGraph()
    
    for port, neighbors in connections.items():
        for neighbor in neighbors:
            if port in portData and neighbor in portData:
                if (port, neighbor) not in edge_weights and (neighbor, port) not in edge_weights:
                    lat1, lon1 = portData[port]
                    lat2, lon2 = portData[neighbor]
                    distance = calculateDistance(lat1, lon1, lat2, lon2, method)
                    edge_weights[(port, neighbor)] = distance
                    edge_weights[(neighbor, port)] = distance
    
    for (port, neighbor), distance in edge_weights.items():
        graph.add_edge(port, neighbor, weight=distance)
    
    return graph

# A* algorithm for shortest path
def heuristic(node1, node2, pos):
    lat1, lon1 = pos[node1]
    lat2, lon2 = pos[node2]
    return geodesicDistance(lat1, lon1, lat2, lon2)

def astarShortestPath(graph, start, end):
    pos = nx.get_node_attributes(graph, 'pos')
    try:
        shortestPath = nx.astar_path(graph, start, end, heuristic=lambda u, v: heuristic(u, v, pos), weight='weight')
        return shortestPath
    except nx.NetworkXNoPath:
        return None

# Function to display the shortest path on OSM
def displayShortestPathOnOSM(graph, shortestPath):
    if not shortestPath:
        print("No path found.")
        return
    
    pos = nx.get_node_attributes(graph, 'pos')
    routeMap = folium.Map(location=[0, 0], zoom_start=2)

    for port in shortestPath:
        lat, lon = pos[port]
        marker_color = 'red' if "WP" in port else 'blue'
        folium.Marker([lat, lon], popup=port, icon=folium.Icon(color=marker_color)).add_to(routeMap)
    
    for i in range(len(shortestPath) - 1):
        start = shortestPath[i]
        end = shortestPath[i + 1]
        start_lat, start_lon = pos[start]
        end_lat, end_lon = pos[end]
        folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color='blue').add_to(routeMap)
    
    routeMap.save("shortest_path_map.html")
    webbrowser.open("shortest_path_map.html")

# Function to display all ports and waypoints and their connections on OSM
def displayAllPortsOnOSM(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    allPortsMap = folium.Map(location=[0, 0], zoom_start=2)
    
    for port, (lat, lon) in pos.items():
        marker_color = 'red' if "WP" in port else 'blue'
        folium.Marker([lat, lon], popup=port, icon=folium.Icon(color=marker_color)).add_to(allPortsMap)
    
    allPortsMap.save("all_ports_map.html")
    webbrowser.open("all_ports_map.html")

# Function to display all valid connections and all ports/waypoints on the map
def displayAllConnectionsOnOSM(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    connectionsMap = folium.Map(location=[0, 0], zoom_start=2)
    
    # Add all ports and waypoints to the map
    for port, (lat, lon) in pos.items():
        marker_color = 'red' if "WP" in port else 'blue'
        folium.Marker([lat, lon], popup=port, icon=folium.Icon(color=marker_color)).add_to(connectionsMap)
    
    # Draw all valid connections (edges) between nodes
    for port1, port2 in graph.edges:
        lat1, lon1 = pos[port1]
        lat2, lon2 = pos[port2]
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color='green').add_to(connectionsMap)
    
    connectionsMap.save("all_connections_map.html")
    webbrowser.open("all_connections_map.html")

# Main function to run the program
def main():
    portData = getPortData()
    graph = constructPositionedGraphOptimized(portData)

    # Input validation
    start_port = input("Enter the starting port: ")
    end_port = input("Enter the destination port: ")
    
    if start_port not in portData or end_port not in portData:
        print("Invalid port entered. Please ensure both ports exist.")
        return
    
    method = input("Enter distance calculation method ('haversine' or 'geodesic'): ").lower()
    if method not in ['haversine', 'geodesic']:
        print("Invalid method. Defaulting to 'geodesic'.")
        method = 'geodesic'
    
    # Calculate the shortest path using A*
    shortestPath = astarShortestPath(graph, start_port, end_port)
    print("Shortest path:", shortestPath)
    
    if shortestPath:
        # Display the shortest path on the map
        displayShortestPathOnOSM(graph, shortestPath)
    
    # Display all valid connections on the map
    displayAllConnectionsOnOSM(graph)
    
    # Display all ports on the map
    displayAllPortsOnOSM(graph)

if __name__ == "__main__":
    main()
