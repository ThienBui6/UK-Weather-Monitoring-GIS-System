import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

# Load weather data (example: London temperature)
weather_df = pd.read_csv('london_temperature.csv')
weather_df['Date'] = pd.to_datetime(weather_df['Date'])  # Convert date column

# Load UK shapefile
uk_regions = gpd.read_file('uk_regions.geojson')
# Rename the column in weather_df if necessary
weather_df.rename(columns={'region_name': 'Region'}, inplace=True)

# Merge weather data with geographic data (e.g., by region name)
merged_data = uk_regions.merge(weather_df, on='Region')  # Ensure 'Region' exists in both DataFrames

# Plotting average temperature
fig, ax = plt.subplots(1, figsize=(12, 8))
merged_data.plot(column='Avg_Temperature', cmap='YlOrRd', legend=True, ax=ax)
plt.title('Average Temperature Across UK Regions (2023)')
plt.axis('off')
plt.savefig('uk_temperature_map.png')  # Ensure the directory exists

# Creating an interactive map for rainfall
m = folium.Map(location=[54.5, -2], zoom_start=6)
folium.Choropleth(
    geo_data=merged_data,
    data=merged_data,
    columns=['Region', 'Avg_Rainfall'],  # Ensure 'Avg_Rainfall' exists in merged_data
    key_on='feature.properties.Region',  # Ensure this matches your GeoJSON structure
    fill_color='Blues',
    legend_name='Rainfall (mm)'
).add_to(m)
m.save('uk_rainfall_interactive.html')  # Ensure the directory exists

# Example: Regional rainfall variability
rainfall_variability = merged_data.groupby('Region')['Rainfall'].std().sort_values(ascending=False)
print("Regions with highest rainfall variability:\n", rainfall_variability.head())
