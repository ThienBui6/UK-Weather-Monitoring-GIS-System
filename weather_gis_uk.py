# weather_gis_uk.py
import os
import requests
import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import folium

# ---------------------------
# Data Acquisition Module
# ---------------------------

def fetch_weather_data(api_key):
    """Fetch real-time weather data from OpenWeatherMap API"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': 'UK',
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def load_geography_data():
    """Load UK geographical features"""
    geography = {
        'elevation': rasterio.open('uk_elevation.tif').read(1),
        'coast_distance': rasterio.open('uk_coast_distance.tif').read(1),
        'urban_areas': rasterio.open('uk_urban_areas.tif').read(1)
    }
    return geography

# ---------------------------
# Data Processing Module
# ---------------------------

def process_weather_data(raw_data, geography):
    """Integrate weather data with geographical features"""
    processed = {
        'temperature': normalize_data(raw_data['main']['temp'], -10, 35),
        'humidity': normalize_data(raw_data['main']['humidity'], 0, 100),
        'precipitation': normalize_data(raw_data.get('rain', {}).get('1h', 0), 0, 50),
        'elevation': normalize_data(geography['elevation']),
        'coast_proximity': normalize_data(geography['coast_distance']),
        'urbanization': normalize_data(geography['urban_areas'])
    }
    return processed

def normalize_data(data, min_val=None, max_val=None):
    """Normalize data to 0-1 scale"""
    if min_val is None: min_val = np.nanmin(data)
    if max_val is None: max_val = np.nanmax(data)
    return (data - min_val) / (max_val - min_val)

# ---------------------------
# Visualization Module
# ---------------------------

def create_weather_map(weather_data, output_file='uk_weather_map.html'):
    """Create interactive Leaflet map with weather layers"""
    base_map = folium.Map(location=[54.5, -2.5], zoom_start=6)
    
    # Temperature layer
    folium.raster_layers.ImageOverlay(
        image=weather_data['temperature'],
        bounds=[[49.9, -8.6], [58.6, 1.8]],
        colormap=LinearSegmentedColormap.from_list('temp', ['blue', 'yellow', 'red']),
        opacity=0.6,
        name='Temperature'
    ).add_to(base_map)

    # Precipitation layer
    folium.raster_layers.ImageOverlay(
        image=weather_data['precipitation'],
        bounds=[[49.9, -8.6], [58.6, 1.8]],
        colormap=LinearSegmentedColormap.from_list('rain', ['white', 'darkblue']),
        opacity=0.5,
        name='Precipitation'
    ).add_to(base_map)

    folium.LayerControl().add_to(base_map)
    base_map.save(output_file)
    return output_file

# ---------------------------
# Main Workflow
# ---------------------------

def main(api_key):
    # Data pipeline
    raw_weather = fetch_weather_data(api_key)
    geography = load_geography_data()
    processed_data = process_weather_data(raw_weather, geography)
    
    # Create visualization
    map_file = create_weather_map(processed_data)
    
    print(f"Weather map generated: {map_file}")

if __name__ == "__main__":
    API_KEY = 'your_openweathermap_api_key'
    main(API_KEY)