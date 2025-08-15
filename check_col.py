import geopandas as gpd

# Load your GeoJSON file
gdf = gpd.read_file("data/DWA Waterbodies Ph1 for Karnataka.geojson")

# Print column names
print(gdf.columns)
