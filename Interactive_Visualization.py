import folium

m = folium.Map(location=[54.5, -2], zoom_start=6)
folium.Choropleth(
    geo_data= merged_data,
    data= merged_data,
    columns=['Region', 'Avg_Rainfall'],
    key_on='feature.properties.Region',
    fill_color='Blues',
    legend_name='Rainfall (mm)'
).add_to(m)
m.save('uk_rainfall_interactive.html')

# Example: Regional rainfall variability
rainfall_variability = merged_data.groupby('Region')['Rainfall'].std().sort_values(ascending=False)
print("Regions with highest rainfall variability:\n", rainfall_variability.head())