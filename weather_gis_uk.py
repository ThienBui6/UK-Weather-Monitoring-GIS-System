# weather_gis_uk.py
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
# Load weather data (example: London temperature)
weather_df = pd.read_csv('london_temperature.csv')
weather_df['Date'] = pd.to_datetime(weather_df['Date'])  # Convert date column

# Load UK shapefile
uk_regions = gpd.read_file('uk_regions.geojson')

# Merge weather data with geographic data (e.g., by region name)
merged_data = uk_regions.merge(weather_df, on='Region')


fig, ax = plt.subplots(1, figsize=(12, 8))
merged_data.plot(column='Avg_Temperature', cmap='YlOrRd', legend=True, ax=ax)
plt.title('Average Temperature Across UK Regions (2023)')
plt.axis('off')
plt.savefig('uk_temperature_map.png')