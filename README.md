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

