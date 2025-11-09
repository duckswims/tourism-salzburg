# Salzburg Bus Routes Visualization

A comprehensive Python tool for visualizing and analyzing regional bus routes in the Salzburg Pinzgau district, Austria. This project extracts data from OpenStreetMap to create detailed maps showing bus routes, stops, villages, and nearby accommodations for lines 660, 670, and 673.

![Salzburg Bus Routes](salzburg_bus_routes_detailed.png)

## Features

### 🗺️ Interactive Visualizations
- **Detailed route maps** showing the complete geographic layout of three major bus lines
- **Color-coded routes** for easy identification:
  - Bus 660 (Red): Zell am See ↔ Kaprun
  - Bus 670 (Cyan): Zell am See ↔ Krimml
  - Bus 673 (Gold): Wald im Pinzgau ↔ Königsleiten

### 📍 Comprehensive Data Extraction
- **Bus stops**: All stops along each route with GPS coordinates and names
- **Villages**: Villages served by each route, color-coded by bus line
- **Hotels & Accommodations**: Hotels, guest houses, and hostels near the routes
- **Route geometry**: Complete geographic path data from OpenStreetMap

### 📊 Dual Visualization System
1. **Geographic Map**: Large-scale map (40x30 inches) showing:
   - Route lines (thick, color-coded)
   - Bus stops (colored circles)
   - Villages (colored triangles with labels)
   - Hotels (brown squares)
   
2. **Villages by Route Chart**: Scatter plot showing which villages are served by which routes

### 📋 Detailed Reports
Console output includes:
- Complete list of bus stops for each route
- Villages organized by bus line
- Hotel information (names, ratings, contact details)
- Summary statistics

## Bus Routes Covered

| Route | Name | Description |
|-------|------|-------------|
| **660** | Zell am See ↔ Kaprun | Connects Zell am See with Kaprun and Kitzsteinhorn |
| **670** | Zell am See ↔ Krimml | Long route through Uttendorf, Mittersill, Neukirchen, Wald to Krimml |
| **673** | Wald/Pzg ↔ Königsleiten | Mountain route from Wald im Pinzgau through Krimml to Königsleiten |

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Libraries
```bash
pip install requests matplotlib
```

### Optional (for enhanced features)
```bash
pip install pillow  # For better image handling
```

## Usage

### Basic Usage
```bash
python salzburg_bus_routes.py
```

### What the Script Does
1. **Fetches route data** from OpenStreetMap via Overpass API
2. **Extracts coordinates** for all route segments
3. **Identifies bus stops** along each route
4. **Finds villages** near each route
5. **Locates hotels** and accommodations in the area
6. **Generates visualizations**:
   - Main detailed map
   - Villages by route chart
7. **Prints detailed reports** to console

### Output Files
The script generates the following files:
- `salzburg_bus_routes_detailed.png` - Main geographic map
- `salzburg_villages_by_route_chart.png` - Villages by route scatter plot

## Data Sources

### OpenStreetMap
All geographic data is sourced from [OpenStreetMap](https://www.openstreetmap.org) via the [Overpass API](https://overpass-api.de/):
- Route geometries from OSM relations
- Bus stop locations and names
- Village/town locations
- Hotel and accommodation data

### Route Relations
The script uses the following OSM relation IDs:
- **Bus 660**: Relations 1852094, 10587835
- **Bus 670**: Relations 1852115, 10599642
- **Bus 673**: Relation 10601324

## Customization

### Adjusting Map Size
Change the figure size in the code:
```python
fig, ax = plt.subplots(figsize=(40, 30))  # Width x Height in inches
```

### Modifying Colors
Edit the color scheme:
```python
bus_routes = {
    '660': {'color': '#FF0000'},  # Red
    '670': {'color': '#00FFFF'},  # Cyan
    '673': {'color': '#FFD700'}   # Gold
}
```

### Adding More Routes
Add new routes to the `bus_routes` dictionary:
```python
'680': {
    'relations': ['relation_id_1', 'relation_id_2'],
    'name': 'Bus 680: Route Name',
    'color': '#YOUR_COLOR'
}
```

## How It Works

### 1. Data Fetching
The script queries the Overpass API to retrieve:
- Complete route geometries (ways and nodes)
- Bus stop locations (nodes with `highway=bus_stop` or `public_transport` tags)
- Village locations (nodes with `place=village`)
- Hotel locations (nodes with `tourism=hotel/guest_house/hostel`)

### 2. Coordinate Extraction
- Processes OSM data to extract latitude/longitude coordinates
- Filters out non-route elements (platforms, buildings)
- Organizes data by route number

### 3. Visualization
- **Matplotlib** for creating high-resolution maps
- **Scatter plots** for stops, villages, and hotels
- **Line plots** for route paths
- **Annotations** for village names

### 4. Analysis
- Groups villages by route
- Calculates bounding boxes
- Generates summary statistics

## Example Output

### Console Output
```
======================================================================
Salzburg Bus Routes - Detailed Analysis
======================================================================

[Bus 660] Bus 660: Zell am See ↔ Kaprun
      Fetching relation 1852094...
      ✓ 45 segments, 28 stops
      Fetching villages for Bus 660...
      ✓ Found 5 villages
   → Total: 45 segments, 28 stops, 5 villages

======================================================================
Bus 660 - Stop Details
======================================================================
Total Stops: 28

  1. Zell am See Postplatz
     Location: 47.3262°N, 12.7926°E
  2. Zell am See Bahnhof
     Location: 47.3237°N, 12.7891°E
...

======================================================================
Villages Along Each Route
======================================================================

Bus 660: Zell am See ↔ Kaprun
----------------------------------------------------------------------
Total: 5 villages

  1. Bruck an der Großglocknerstraße
     Location: 47.2825°N, 12.8269°E
  2. Kaprun (pop: 3,054)
     Location: 47.2689°N, 12.7589°E
...
```

## Technical Details

### API Rate Limits
- Overpass API has usage limits - the script includes appropriate timeouts
- Default timeout: 90 seconds per query
- Requests are sequential to avoid overloading the API

### Performance
- Typical execution time: 2-5 minutes (depending on network speed)
- Data size: ~2-5 MB downloaded from OpenStreetMap
- Output image sizes: 20-40 MB (high resolution)

### Coordinate System
- Input: WGS84 (EPSG:4326) - latitude/longitude
- Output: Direct lat/lon plotting (no projection transformation)

## Troubleshooting

### Common Issues

**"No coordinates found"**
- Check internet connection
- Verify Overpass API is accessible
- Relations may have changed - check OSM for updated IDs

**"Timeout errors"**
- Increase timeout in query: `[timeout:120]`
- Retry the request
- Check Overpass API status

**"Module not found"**
- Install missing dependencies: `pip install requests matplotlib`

**"Map looks cluttered"**
- Increase figure size for better spacing
- Adjust marker sizes in the code
- Reduce font sizes for labels

## Contributing

Contributions are welcome! Here are ways to contribute:

### Adding Features
- Support for additional bus routes
- Export to different formats (PDF, SVG)
- Interactive web-based version
- Real-time schedule integration
- Elevation profiles for routes

### Improving Visualizations
- Different map styles
- Satellite/terrain backgrounds
- Animation of routes
- 3D terrain visualization

### Data Enhancements
- Include route schedules
- Add ticket pricing information
- Show seasonal variations
- Include accessibility information

## Data Accuracy

### Important Notes
- Data is sourced from OpenStreetMap, a crowdsourced database
- Accuracy depends on OSM contributor updates
- Bus routes and stops may change - always verify current information
- The visualization shows approximate paths between stops

### Data Freshness
This tool fetches real-time data from OpenStreetMap, so maps reflect the current state of OSM data at the time of execution.

## License

This project uses data from OpenStreetMap, which is licensed under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/).

### Attribution
Maps and data: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors

## Acknowledgments

- **OpenStreetMap**: For providing free, open geographic data
- **Overpass API**: For enabling efficient OSM data queries
- **Matplotlib**: For powerful visualization capabilities
- **Salzburger Verkehrsverbund**: For operating these bus routes

## Related Projects

- [OpenStreetMap](https://www.openstreetmap.org)
- [Overpass API](https://overpass-api.de/)
- [Salzburg Public Transport](https://salzburg-verkehr.at/)

## Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

## Roadmap

### Planned Features
- [ ] Interactive HTML map output
- [ ] Support for more bus routes
- [ ] Integration with real-time schedules
- [ ] Mobile-friendly web interface
- [ ] Route comparison tools
- [ ] Export to GPX format
- [ ] Multi-language support

## Version History

### v1.0.0 (Current)
- Initial release
- Support for routes 660, 670, 673
- Geographic map visualization
- Villages by route chart
- Detailed console reports
- Hotel and accommodation data

---

**Made with ❤️ for travelers in Salzburg, Austria 🇦🇹**