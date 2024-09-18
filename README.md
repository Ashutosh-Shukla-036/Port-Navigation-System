# Maritime Route Optimization and Visualization

## Overview

This project provides a tool for calculating and visualizing maritime routes between various ports and waypoints. It constructs a graph of port connections and uses the A* algorithm to find the shortest path between two ports. The route is then displayed on an interactive map. This project utilizes:
- **NetworkX** for graph representation.
- **Geopy** for distance calculations.
- **Folium** for map visualization.

## Features

- **Distance Calculations**: Supports both Haversine and Geodesic distance calculations.
- **Graph Construction**: Builds a weighted graph of port connections based on real geographic coordinates.
- **Shortest Path**: Uses the A* algorithm to find the shortest maritime route between two ports.
- **Interactive Map**: Visualizes the ports, connections, and shortest paths on an OpenStreetMap (OSM) using Folium.
- **Port and Waypoint Data**: Includes a set of predefined ports and waypoints with their geographic coordinates.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your system. You will also need to install the required Python libraries. You can do this using `pip`:

```bash
pip install networkx geopy folium

Usage
Run the Script: Execute the script to calculate the shortest path and visualize it:

bash
Copy code
python script.py
Replace script.py with the actual name of your script file.

View the Output:

The shortest path between the specified start and end ports will be printed to the console.
An HTML file named route_map.html will be generated, displaying the interactive map with ports, connections, and the shortest path.
Example
To find the shortest route between Port A and Port B, the tool will:

Compute distances between ports.
Build a graph based on port connections.
Apply the A* algorithm to find the shortest path.
Generate an interactive map highlighting the route.
