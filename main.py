import networkx as nx
import math
from geopy.distance import geodesic
import folium
import requests
import json
import os

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
        "WP14": (13.765, 74.293),
        "WP15": (12.419, 74.695),
        "WP16": (25.812,56.876),
        "WP17": (24.015,63.720),
        "WP18": (12.376,46.796),
        "WP19": (6.179,51.231),
        "WP20": (-0.570,46.538),
        "WP21": (16.683,64.216),
        "WP22": (12.001,67.907),
        "WP23": (10.060,59.470),
        "WP24": (4.132,60.876),
        "WP25": (22.916,70.242)
    }

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

def getGraph():
   return {
    "Malindi": ["WP1","WP2","WP20","WP21","WP24","WP23","Kochi","New Mangalore","WP14","WP13","Mormugaiort","Mumbai"],
    "Lamu": ["WP1", "WP2","WP20","WP24","Kochi"],
    "Kismayo": ["WP2", "WP19","WP20","WP24","WP23","WP15","New Mangalore","WP14","Mormugaiort","WP22","Magadishu"],
    "Magadishu": ["WP20","WP2","Kismayo","WP24","WP23","WP22","Kochi","WP15","WP14","New Mangalore"],
    "Bosaso": ["Aden","Mukalla","WP18","WP6","Salalah"],
    "Berbera": ["Aden","WP18","Mukalla"],
    "Aden": ["WP6","WP18","Berbera","Bosaso","WP5","Socotra"],
    "Mukalla": ["WP6", "WP5","Bosaso","Berbera","Socotra","WP4","WP21","WP22","WP14","Mumbai","Mormugaiort","Kochi","WP15","New Mangalore"],
    "Nishtun": ["WP5", "WP7","Salalah","Socotra","WP21","WP22","WP23","WP13","WP14","Mumbai","Mormugaiort","Kochi","WP15","New Mangalore"],
    "Salalah": ["WP4","WP5","WP6","Socotra","Bosaso","WP22","WP23"],
    "Sultan": ["WP9","WP16","Chabahar","WP17","WP10","WP11","WP12","Mumbai"],
    "Duqm": ["WP8","WP21","WP12","Mumbai","WP13","Mormugaiort","WP22","WP14","WP15","New Mangalore","Kochi"],
    "Bandar Abbas": ["WP16","Sultan"],
    "Chabahar": ["WP9", "WP17","WP8","WP10","WP12","WP21","Mumbai","WP13","Mormugaiort","WP22","WP14","WP15","New Mangalore","Kochi"],
    "Socotra": ["WP5","WP6","Nishtun","Salalah","WP7","WP21","WP22","WP8","WP17","WP10","WP12","Mumbai","WP13","Mormugaiort","WP22","WP14","WP15","New Mangalore"],
    "Kandla": ["WP25"],
    "Mumbai": ["WP21", "WP12","WP22","WP23","WP24","Malindi","Mukalla","Nishtun","Sultan","Chabahar","Socotra"],
    "Mormugaiort": ["WP12","WP21","WP22","WP23","WP14","Malindi","Kismayo","Mukalla","Nishtun","Duqm","Chabahar","Socotra"],
    "New Mangalore": ["WP14","WP15","WP21","WP22","WP23","WP24","WP12","Malindi","Kismayo","Magadishu","Mukalla","Nishtun","Duqm","Chabahar","Socotra"],
    "Kochi": ["WP15","WP21","WP22","WP23","WP12","WP19","WP20","Malindi","Lamu","Magadishu","Mukalla","Nishtun","Duqm","Chabahar"],

    # Waypoint connections
    "WP1": ["WP2", "Malindi", "Lamu","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP2": ["WP1", "WP19", "Kismayo","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort","Magadishu"],
    "WP3": ["WP4","WP5","WP19","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP4": ["WP3", "WP5","WP6","Mukalla","WP19","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP5": ["WP4", "WP6", "Nishtun","Socotra","WP7","Bosaso","WP18","Aden","WP21","WP10","WP12","Mumbai","WP13","WP14","New Mangalore","Mormugaiort"],
    "WP6": ["WP5", "Aden", "Mukalla","Aden","WP18","Mukalla","Bosaso","WP5","WP4","WP7","Salalah","WP12","WP21","Mumbai","WP13","Mormugaiort","WP10"],
    "WP7": ["WP5", "Salalah", "WP6","Bosaso","WP18","Berbera","WP21","WP22","WP23","WP24","WP8","WP10","Wp12","WP9","WP17","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP8": ["WP9", "WP7", "Chabahar","WP17","WP10","WP12","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP9": ["WP8", "WP10", "Sultan","Chabahar","WP16","WP17","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP10": ["WP9", "WP11","WP12","WP21","WP22","WP23","WP24","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP11": ["WP10", "WP25"],
    "WP12": ["WP10", "WP13", "Mumbai","WP17","WP9","Chabahar","Sultan","WP8","Duqm","WP7","WP21","WP22","WP23","WP24","Mumbai","WP13","WP14","WP15","Kochi","New Mangalore","Mormugaiort"],
    "WP13": ["WP12", "WP14", "Mormugaiort","Mumbai","WP10","WP17","WP9","Chabahar","WP8","Duqm","WP7","WP3","WP19","WP14","WP15","WP21","WP22","WP23","WP24"],
    "WP14": ["WP13", "WP15", "New Mangalore","Mormugaiort","WP21","WP22","WP23","WP24","Malindi","Lamu","WP1","WP2"],
    "WP15": ["WP14", "Kochi","New Mangalore","WP13","WP21","WP22","WP23","WP24","WP17","WP9","Chabahar","WP7","WP8","Duqm","Socotra","WP3","WP4","WP19","WP20","Malindi","Lamu"],
    "WP16": ["WP9", "WP17", "Bandar Abbas", "Chabahar","Sultan","WP12","Mumbai"],
    "WP17": ["WP16", "WP21","WP10","WP12","WP9","WP8","Mumbai","WP13","Mormugaiort","WP22","WP14","WP15","New Mangalore","Kochi","WP23","WP24"],
    "WP18": ["WP6", "Socotra","Aden","Berbera","Mukalla","WP5","WP21","WP12","Mumbai","WP10"],
    "WP19": ["WP3", "WP20", "Kismayo", "Magadishu","WP4","WP21","WP1","Malindu","Lamu","WP22","WP23","WP24","Mumbai","WP13","Mormugaiort","WP14","WP15","New Mangalore","Kochi"],
    "WP20": ["WP19", "WP4", "Magadishu","Kismayo","Lamu","WP1","Malindi","Lamu","Mumbai","WP13","Mormugaiort","WP22","WP14","WP15","New Mangalore","Kochi","WP23","WP24"],
    "WP21": ["WP17", "WP22","WP10","WP12","Mumbai","WP13","Mormugaiort","WP14","WP15","New Mangalore","Kochi","WP23","WP24","WP20","WP19","WP3","WP4","Socotra","WP5","WP6","WP18","Nishtun","Mukalla","WP7","WP8","Duqm","WP9","Chabahar"],
    "WP22": ["WP17", "WP21","WP10","WP12","Mumbai","WP13","Mormugaiort","WP14","WP15","New Mangalore","Kochi","WP23","WP24","WP20","WP19","WP3","WP4","Socotra","WP2","Nishtun","Mukalla","WP7","WP8","Duqm","WP9","Chabahar"],
    "WP23": ["WP17", "WP22","WP10","WP12","Mumbai","WP13","Mormugaiort","WP14","WP15","New Mangalore","Kochi","WP21","WP24","WP20","WP19","WP3","WP4","WP6","WP18","Nishtun","WP7","WP8","Duqm","WP9","Chabahar"],
    "WP24": ["WP17", "WP22","WP10","WP12","Mumbai","WP13","Mormugaiort","WP14","WP15","New Mangalore","Kochi","WP23","WP21","WP20","WP19","WP3","WP4","WP5","WP6","WP18","Mukalla","WP7","WP8","Duqm","WP9","Chabahar","WP1","Malindi","Lamu"],
    "WP25": ["Kandla","WP11"]
    }

def constructPositionedGraph(portData, graph, method='geodesic'):
    G = nx.Graph()
    for port, (lat, lon) in portData.items():
        G.add_node(port, pos=(lat, lon))
    
    for port1, neighbors in graph.items():
        for port2 in neighbors:
            if port1 in portData and port2 in portData:
                distance = calculateDistance(
                    portData[port1][0], portData[port1][1], 
                    portData[port2][0], portData[port2][1], method)
                G.add_edge(port1, port2, weight=distance)
    
    return G

# Caching weather data
CACHE_FILE = 'weather_cache.json'

def load_weather_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_weather_cache(data):
    with open(CACHE_FILE, 'w') as file:
        json.dump(data, file)

def fetch_weather_data(lat, lon, api_key):
    cache = load_weather_cache()
    key = f"{lat},{lon}"
    
    if key in cache:
        print(f"Using cached weather data for {key}")
        return cache[key]

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # Get temperature in Celsius
    }
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        print(f"Weather data fetched for {key}: {json.dumps(weather_data, indent=2)}")
        
        if 'weather' not in weather_data:
            print(f"Error: 'weather' key not found in the API response for {key}.")
            return {}
        
        cache[key] = weather_data
        save_weather_cache(cache)
        
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {key}: {e}")
        return {}
    except KeyError as e:
        print(f"Data format error for {key}: {e}")
        return {}

def assess_weather_risk(weather_data):
    if not weather_data or 'weather' not in weather_data or not weather_data['weather']:
        print("Error: Missing or empty 'weather' key in data.")
        return 0
    
    try:
        storm_severity = weather_data['weather'][0]['main']
        risk_mapping = {
            'Clear': 0,
            'Clouds': 1,
            'Rain': 2,
            'Drizzle': 2,
            'Thunderstorm': 3,
            'Snow': 3
        }
        risk = risk_mapping.get(storm_severity, 0)
        return risk
    except KeyError as e:
        print(f"Key error while assessing weather risk: {e}")
        return 0
    except IndexError as e:
        print(f"Index error while accessing weather data: {e}")
        return 0

def is_unsafe(weather_data):
    """
    Determines if a location is unsafe based on the weather data.
    This function returns True if the weather conditions are unsafe.
    """
    if not weather_data or 'weather' not in weather_data or 'main' not in weather_data:
        return False  # If there's no valid data, assume it's safe.

    # Extract relevant weather details
    weather_description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind'].get('speed', 0)

    # Define conditions for unsafe weather (you can adjust these thresholds)
    if 'storm' in weather_description or 'thunderstorm' in weather_description:
        return True
    if 'rain' in weather_description and wind_speed > 10:  # Heavy rain and strong winds
        return True
    if wind_speed > 20:  # High wind speeds alone
        return True

    return False  # Safe otherwise

def displayWeatherMarkersOnMap(folium_map, portData, api_key):
    for port, (lat, lon) in portData.items():
        weather_data = fetch_weather_data(lat, lon, api_key)
        
        if not weather_data or 'weather' not in weather_data:
            print(f"Weather data missing for port {port} at ({lat}, {lon})")
            continue
        
        try:
            weather_description = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            wind_speed = weather_data['wind'].get('speed', 0)
        except KeyError as e:
            print(f"Key error while accessing weather data for {port}: {e}")
            continue

        # Determine the color of the marker based on weather conditions
        if is_unsafe(weather_data):
            color = 'red'  # Mark unsafe locations in red
            folium.Circle(
                location=[lat, lon],
                radius=50000,  # Adjust the radius based on the unsafe area
                color='red',
                fill=True,
                fill_opacity=0.3
            ).add_to(folium_map)
        else:
            # Match weather description to available color options for safe locations
            if 'rain' in weather_description:
                color = 'blue'
            elif 'clear' in weather_description:
                color = 'orange'
            elif 'cloud' in weather_description:
                color = 'gray'
            else:
                color = 'green'  # Use green for safe, unknown conditions
        
        # Add the marker to the map
        folium.Marker(
            location=[lat, lon],
            popup=f"{port}\nWeather: {weather_description}\nTemp: {temp:.1f}°C\nWind: {wind_speed:.1f} m/s",
            icon=folium.Icon(color=color)
        ).add_to(folium_map)

def draw_route_on_map(folium_map, path, portData):
    # Define a color for the route
    route_color = 'blue'
    
    # Add the route to the map
    folium.PolyLine(
        locations=[(portData[port][0], portData[port][1]) for port in path],
        color=route_color,
        weight=5,
        opacity=0.8
    ).add_to(folium_map)

def find_shortest_path_with_weather_risk(graph, start, end, portData, api_key):
    # Ensure that the start and end nodes are in the graph
    if start not in graph or end not in graph:
        print("Error: Start or end port not found in the graph.")
        return [], float('inf')

    # Adjust edge weights based on weather risk
    for u, v, data in graph.edges(data=True):
        lat1, lon1 = portData[u]
        lat2, lon2 = portData[v]
        weather_data_u = fetch_weather_data(lat1, lon1, api_key)
        weather_data_v = fetch_weather_data(lat2, lon2, api_key)

        risk_u = assess_weather_risk(weather_data_u)
        risk_v = assess_weather_risk(weather_data_v)

        # Adjust the distance by adding risk weight (modify weight if needed)
        risk_weight = 0.5 * (risk_u + risk_v)
        graph[u][v]['weight'] += risk_weight
    
    try:
        # Find the shortest path using A* algorithm
        path = nx.astar_path(graph, start, end, weight='weight')
        path_length = nx.path_weight(graph, path, weight='weight')
        return path, path_length
    except nx.NetworkXNoPath:
        print("No path found between the given ports.")
        return [], float('inf')
    except nx.NodeNotFound as e:
        print(f"Error: {e}")
        return [], float('inf')

def main():
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    portData = getPortData()
    graph = getGraph()
    G = constructPositionedGraph(portData, graph)

    # Example start and end ports
    start_port = 'Kochi'
    end_port = 'Kandla'

    # Find shortest path considering weather risk
    path, path_length = find_shortest_path_with_weather_risk(G, start_port, end_port, portData, api_key)

    # Display results
    print(f"Shortest path: {path}")
    print(f"Path length: {path_length:.2f} km")

    # Create a map centered around the first port
    if path:
        map_center = portData[path[0]]
        folium_map = folium.Map(location=[map_center[0], map_center[1]], zoom_start=6)
        displayWeatherMarkersOnMap(folium_map, portData, api_key)
        draw_route_on_map(folium_map, path, portData)
        folium_map.save('route_map.html')
        print("Map has been saved to route_map.html")

if __name__ == "__main__":
    main()
