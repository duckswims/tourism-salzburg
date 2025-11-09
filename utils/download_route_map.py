import json
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

# Load bus info from JSON
with open('bus_670_salzburg.json', 'r') as f:
    bus_info = json.load(f)

# Create GeoDataFrame for bus stops
points_geom = [Point(lon, lat) for lat, lon in bus_info['line']]
gdf_points = gpd.GeoDataFrame(geometry=points_geom, crs="EPSG:4326")

# Convert to Web Mercator for contextily basemap
gdf_points = gdf_points.to_crs(epsg=3857)

# Plot points with smaller size
fig, ax = plt.subplots(figsize=(15, 4))
gdf_points.plot(ax=ax, color='blue', markersize=10, alpha=.7)

# Add basemap (OpenStreetMap)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

ax.set_axis_off()
# plt.tight_layout()
plt.savefig("assets/bus_route.png", dpi=300)
plt.show()
