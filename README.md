# Maritime Route Optimization and Visualization

This project provides a tool for calculating and visualizing maritime routes between various ports and waypoints. The tool constructs a graph of port connections and uses the A* algorithm to find the shortest path between two ports, displaying the route on an interactive map. The project leverages the `NetworkX` library for graph representation, `geopy` for distance calculations, and `Folium` for map visualization.

## Features

- **Distance Calculations**: Supports both `haversine` and `geodesic` distance calculations.
- **Graph Construction**: Builds a weighted graph of port connections based on real geographic coordinates.
- **Shortest Path**: Uses the A* algorithm to find the shortest maritime route between two ports.
- **Interactive Map**: Visualizes the ports, connections, and shortest paths on an OpenStreetMap (OSM) using `Folium`.
- **Port and Waypoint Data**: Includes a set of predefined ports and waypoints with their geographic coordinates.

## Installation

### Prerequisites

Make sure you have Python 3.x installed. You will also need to install the following Python libraries:

```bash
pip install networkx geopy folium
