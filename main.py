import networkx as nx
import math
from geopy.distance import geodesic
import folium
import requests
import time

# Sample port data (replace with actual data)
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

# Construct the graph using the provided connections
def getGraph():
    return {
        "Malindi": ["WP1", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP1": ["Lamu", "WP10", "WP2", "Mormugaiort"],
        "Lamu": ["WP2", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP2": ["Kismayo", "Magadishu", "WP3", "WP10", "Mormugaiort"],
        "Kismayo": ["Magadishu", "WP3", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "Magadishu": ["WP3", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP3": ["WP4", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort"],
        "WP4": ["WP5", "Kochi", "New Mangalore", "Mumbai", "WP10", "Mormugaiort", "WP6"],
        "Bosaso": ["Berbera", "Aden", "Mukalla", "Nishtun", "Salalah", "WP6"],
        "Berbera": ["WP6", "Aden", "Mukalla", "Nishtun"],
        "WP5": ["WP6", "Socotra", "Salalah", "Nishtun"],
        "Aden": ["Mukalla", "WP6"],
        "Nishtun": ["Socotra", "WP6", "WP10", "Mumbai", "Mormugaiort"],
        "Salalah": ["WP6", "WP5", "WP7", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort", "Socotra"],
        "WP7": ["WP5", "WP6", "WP8", "WP10", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort", "Duqm"],
        "Duqm": ["WP8", "WP10", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort"],
        "WP8": ["WP9", "WP10", "Sultan", "Kochi", "New Mangalore", "Mumbai", "Mormugaiort"],
        "WP9": ["Chabahar", "Sultan", "Bandar Abbas", "WP10"],
        "Sultan": ["Chabahar", "Bandar Abbas"],
        "WP10": ["WP11", "WP12"],
        "WP11": ["Kandla"],
        "WP12": ["Mumbai", "WP13", "WP14"],
        "Mumbai": ["WP13", "Mormugaiort", "Chabahar", "Kochi", "New Mangalore"],
        "WP13": ["Mormugaiort", "WP14"],
        "WP14": ["Mormugaiort", "Kochi"],
        "Chabahar": ["Mumbai", "Kochi", "New Mangalore", "Mormugaiort"],
        "Mormugaiort": ["Mumbai", "Chabahar", "New Mangalore", "Kochi"],
        "New Mangalore": ["Mumbai", "Mormugaiort", "Kochi", "Chabahar"],
        "Kochi": ["Mumbai", "Mormugaiort", "New Mangalore", "Chabahar"]
    }

# Function to construct the graph with distances
def constructPositionedGraphOptimized(portData, graph, method='geodesic'):
    G = nx.Graph()
    for port in portData.keys():
        G.add_node(port, pos=portData[port])
    
    for port1, neighbors in graph.items():
        for port2 in neighbors:
            if port1 in portData and port2 in portData:
                distance = calculateDistance(
                    portData[port1][0], portData[port1][1], 
                    portData[port2][0], portData[port2][1], method)
                G.add_edge(port1, port2, weight=distance)
    
    return G

# Function to fetch weather data
def fetch_weather_data(lat, lon, api_key):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    return response.json()

# Functions to assess various risks
def assess_weather_risk(weather_data):
    storm_severity = weather_data['weather'][0]['main']
    wind_speed = weather_data['wind']['speed']

    if storm_severity == "Thunderstorm":
        return 0.5
    elif wind_speed > 20:
        return 0.3
    else:
        return 0.1

def assess_traffic_risk(maritime_data):
    # Simplified risk assessment for demonstration purposes
    traffic_density = maritime_data.get('density', 0)
    if traffic_density > 50:
        return 0.5
    elif traffic_density > 20:
        return 0.3
    else:
        return 0.1

# A* algorithm for shortest path with heuristic and risk consideration
def astarShortestPath(graph, start, end, api_key):
    def heuristic(u, v):
        pos_u = graph.nodes[u]['pos']
        pos_v = graph.nodes[v]['pos']
        return calculateDistance(pos_u[0], pos_u[1], pos_v[0], pos_v[1])
    
    def modified_weight(u, v, data):
        pos_u = graph.nodes[u]['pos']
        pos_v = graph.nodes[v]['pos']
        base_weight = data['weight']
        
        # Fetch weather data for both nodes
        weather_u = fetch_weather_data(pos_u[0], pos_u[1], api_key)
        weather_v = fetch_weather_data(pos_v[0], pos_v[1], api_key)
        
        # Assess risk based on weather
        weather_risk_u = assess_weather_risk(weather_u)
        weather_risk_v = assess_weather_risk(weather_v)
        
        # Simplified combined risk factor
        risk_factor = (weather_risk_u + weather_risk_v) / 2
        
        return base_weight * (1 + risk_factor)

    try:
        shortest_path = nx.astar_path(graph, start, end, heuristic=heuristic, weight=modified_weight)
        return shortest_path
    except nx.NetworkXNoPath:
        return None

# Function to display the shortest path on the map
def displayWeatherMarkersOnMap(folium_map, portData, api_key):
    """ Add weather markers for each port to the map. """
    for port, (lat, lon) in portData.items():
        weather_data = fetch_weather_data(lat, lon, api_key)
        weather_description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        
        # Choose marker color based on weather
        if 'rain' in weather_description:
            color = 'blue'
        elif 'clear' in weather_description:
            color = 'yellow'
        elif 'cloud' in weather_description:
            color = 'gray'
        elif 'storm' in weather_description:
            color = 'red'
        else:
            color = 'green'
        
        folium.Marker(
            location=[lat, lon],
            popup=f"{port}\nWeather: {weather_description}\nTemp: {temp:.1f}°C",
            icon=folium.Icon(color=color)
        ).add_to(folium_map)

def displayShortestPathOnOSM(graph, shortest_path, api_key):
    folium_map = folium.Map(location=[0, 0], zoom_start=2)
    
    for i in range(len(shortest_path) - 1):
        start = shortest_path[i]
        end = shortest_path[i + 1]
        folium.PolyLine(
            locations=[graph.nodes[start]['pos'], graph.nodes[end]['pos']],
            color='blue',
            weight=2.5,
            opacity=1
        ).add_to(folium_map)
    
    # Add weather markers to the map
    portData = getPortData()
    displayWeatherMarkersOnMap(folium_map, portData, api_key)
    
    folium_map.save("shortest_path_map_with_weather.html")
    print("Shortest path map with weather saved as 'shortest_path_map_with_weather.html'.")

def main():
    portData = getPortData()
    
    # Filter out waypoints (those that start with "WP") and only show actual ports
    available_ports = [port for port in portData.keys() if not port.startswith("WP")]
    print("Available ports:", ", ".join(available_ports))
    
    start_port = input("Enter the starting port: ").strip()
    end_port = input("Enter the destination port: ").strip()
    
    if start_port not in portData or end_port not in portData:
        print("Invalid port entered. Please ensure both ports exist.")
        return
    
    method = input("Enter distance calculation method ('haversine' or 'geodesic'): ").lower()
    if method not in ['haversine', 'geodesic']:
        print("Invalid method. Defaulting to 'geodesic'.")
        method = 'geodesic'
    
    # Construct the graph with the chosen distance calculation method
    graph = constructPositionedGraphOptimized(portData, getGraph(), method)
    
    # Fetch your API key from environment variables or securely
    api_key = "7d4fe998e8796d76e06167b04ca6057c"
    
    # Calculate the shortest path using A*
    shortestPath = astarShortestPath(graph, start_port, end_port, api_key)
    if shortestPath:
        print("Shortest path:", shortestPath)
        # Display the shortest path on the map with weather
        displayShortestPathOnOSM(graph, shortestPath, api_key)
    else:
        print(f"No valid path found between {start_port} and {end_port}.")

if __name__ == "__main__":
    main()