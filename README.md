# anygeom-py

Python package to generate any kind of geospatial geometry

## Motivation

As a GIS developer, often times while working on projects, I need to test my functions with dummy geometries, currently, I go on sites like [geojson.io](https://geojson.io/) to generate geometries. But this process is time consuming, and more importantly I can only generate data in EPSG:4326. 
I need solution that can Generate Random Geometry based on

- Geometry Type
- Projection
- BBOX
- Count
- Multi/Single

as per my need.

## Installation

```bash
pip install anygeom-py
```

## Quick Start

```python
from anygeom import Point, LineString, Polygon, Circle

# Generate single point (returns GeoJSON Feature)
point = Point()

# Generate 3 random points in projection EPSG:32643, within given bbox
# Returns list of 3 GeoJSON Features
points = Point(count=3, crs=32643, bbox=[53.127823, 7.047742, 106.125870, 35.488629])

# Generate 4 random linestrings in projection EPSG:4326, each having 3 to 6 vertices
# Returns list of 4 GeoJSON Features
linestrings = LineString(count=4, crs=4326, min_vertex=3, max_vertex=6)

# Generate random polygon having 6 to 10 vertices with hole in it
# Returns single GeoJSON Feature
polygon = Polygon(hole=True, min_vertex=6, max_vertex=10)

# Generate random circle with custom radius
circle = Circle(radius=5, crs=4326)

# Generate multiple circles
circles = Circle(count=3, bbox=[0, 0, 10, 10])
```

## Features

- **Geometry Types**: Point, LineString, Polygon, Circle, MultiPoint, MultiLineString, MultiPolygon
- **CRS Support**: Any EPSG code (e.g., 4326, 3857, 32643)
- **Custom Bounding Box**: Define area for geometry generation
- **Vertex Control**: Set min/max vertices for LineStrings and Polygons
- **Polygon Holes**: Generate polygons with holes
- **Count Control**: Generate single or multiple geometries
- **GeoJSON Export**: Proper GeoJSON Feature format with list coordinates
- **Shapely Compatible**: All geometries are Shapely objects
- **Input Validation**: Clear error messages for invalid parameters

## Usage Examples

### Basic Geometry Generation

```python
from anygeom import Point, LineString, Polygon, Circle
import json

# Single geometry returns GeoJSON Feature
point = Point()
print(json.dumps(point.__geo_interface__, indent=2))
# Output:
# {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Point",
#     "coordinates": [34.62, 14.18]
#   }
# }

# Multiple geometries return list of Features
points = Point(count=3)
print(len(points))  # 3
print(points[0])    # Access individual features
```

### Working with Different CRS

```python
# Generate geometries in Web Mercator (EPSG:3857)
point_3857 = Point(crs=3857)

# Generate geometries in UTM Zone 43N (EPSG:32643)
points_utm = Point(count=5, crs=32643, bbox=[72.0, 12.0, 84.0, 30.0])
```

### Custom Bounding Box

```python
# Generate geometries within specific area
india_bbox = [68.1766, 7.9668, 97.4025, 35.4940]
points = Point(count=10, bbox=india_bbox)
lines = LineString(count=5, bbox=india_bbox, min_vertex=3, max_vertex=8)
```

### LineStrings with Vertex Control

```python
# Simple linestring with 2-5 vertices
line = LineString()

# Complex linestring with 10-20 vertices
complex_line = LineString(min_vertex=10, max_vertex=20)

# Multiple linestrings
lines = LineString(count=4, min_vertex=3, max_vertex=6)
```

### Polygons with Holes

```python
# Simple polygon
polygon = Polygon()

# Polygon with specific vertex count
polygon = Polygon(min_vertex=8, max_vertex=12)

# Polygon with hole
polygon_with_hole = Polygon(hole=True, min_vertex=6, max_vertex=10)

# Multiple polygons with holes
polygons = Polygon(count=3, hole=True)
```

### Circles

```python
# Circle with auto-calculated radius
circle = Circle()

# Circle with custom radius (in CRS units)
circle = Circle(radius=5, crs=4326)

# Circle in Web Mercator with radius in meters
circle_meters = Circle(radius=1000, crs=3857)

# Multiple circles
circles = Circle(count=5, bbox=[0, 0, 10, 10])

# Control circle smoothness
smooth_circle = Circle(num_points=128)  # More points = smoother circle
```

### Exporting as GeoJSON

```python
# Single geometry
point = Point()
geojson = point.__geo_interface__
# Returns: {"type": "Feature", "properties": {}, "geometry": {...}}

# Multiple geometries
points = Point(count=3)
geojson_list = points.__geo_interface__
# Returns: [{"type": "Feature", ...}, {"type": "Feature", ...}, ...]

# Save to file
import json
with open('points.geojson', 'w') as f:
    json.dump(geojson_list, f, indent=2)
```

### Using with Shapely

```python
from anygeom import Point, Polygon

# All geometries are Shapely-compatible
point = Point()
print(point.x, point.y)  # Access Shapely properties
print(point.buffer(1))   # Use Shapely methods

polygon = Polygon()
print(polygon.area)      # Calculate area
print(polygon.bounds)    # Get bounds
```

## API Reference

### Common Parameters

All geometry classes support these parameters:

- **count** (int): Number of geometries to generate (default: 1)
- **crs** (int): EPSG code for coordinate reference system (default: 4326)
- **bbox** (list): Bounding box as [minx, miny, maxx, maxy] (default: world bounds)

### Point

```python
Point(count=1, crs=4326, bbox=None)
```

Generates random point geometries.

### LineString

```python
LineString(count=1, crs=4326, bbox=None, min_vertex=2, max_vertex=5)
```

Generates random linestring geometries.

**Additional Parameters:**
- **min_vertex** (int): Minimum number of vertices (default: 2)
- **max_vertex** (int): Maximum number of vertices (default: 5)

### Polygon

```python
Polygon(count=1, crs=4326, bbox=None, min_vertex=3, max_vertex=8, hole=False)
```

Generates random polygon geometries.

**Additional Parameters:**
- **min_vertex** (int): Minimum number of vertices (default: 3)
- **max_vertex** (int): Maximum number of vertices (default: 8)
- **hole** (bool): Generate polygon with hole (default: False)

### Circle

```python
Circle(count=1, crs=4326, bbox=None, radius=None, num_points=64)
```

Generates circular polygon geometries.

**Additional Parameters:**
- **radius** (float): Circle radius in CRS units (default: auto-calculated from bbox)
- **num_points** (int): Number of points to approximate circle (default: 64)

### MultiPoint, MultiLineString, MultiPolygon

```python
MultiPoint(count=2, crs=4326, bbox=None)
MultiLineString(count=2, crs=4326, bbox=None, min_vertex=2, max_vertex=5)
MultiPolygon(count=2, crs=4326, bbox=None, min_vertex=3, max_vertex=8, hole=False)
```

Generates Multi* geometry types (single feature with multiple geometries).

## Output Format

### Single Geometry

When `count=1`, returns a single GeoJSON Feature:

```json
{
  "type": "Feature",
  "properties": {},
  "geometry": {
    "type": "Point",
    "coordinates": [34.62, 14.18]
  }
}
```

### Multiple Geometries

When `count>1`, returns a list of GeoJSON Features:

```json
[
  {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Point",
      "coordinates": [34.62, 14.18]
    }
  },
  {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Point",
      "coordinates": [37.27, 10.92]
    }
  }
]
```

## Error Handling

The package validates all inputs and provides clear error messages:

```python
# Invalid vertex range
LineString(min_vertex=40, max_vertex=6)
# ValueError: min_vertex (40) cannot be greater than max_vertex (6)

# Invalid bbox (minx > maxx)
Point(bbox=[83.77, 29.12, 72.81, 12.70])
# ValueError: bbox minx (83.77) must be less than maxx (72.81)

# Invalid count
Point(count=0)
# ValueError: count must be at least 1, got 0

# Invalid bbox format
Point(bbox=[0, 0, 10])
# ValueError: bbox must have exactly 4 values [minx, miny, maxx, maxy], got 3
```

## Dependencies

- **Python** >= 3.11
- **shapely** >= 2.1.2 - For geometry operations and GeoJSON export
- **pyproj** >= 3.7.2 - For coordinate reference system transformations

## Technical Details

### Architecture

The package uses a wrapper pattern to provide GeoJSON Feature output while maintaining Shapely compatibility:

- **_GeometryWrapper**: Wraps single Shapely geometries and returns GeoJSON Features
- **_GeometryListWrapper**: Wraps multiple geometries and returns list of Features
- All geometry classes use `__new__` to return appropriate wrapper types

### CRS Handling

- Default CRS is EPSG:4326 (WGS84)
- Bounding boxes are always provided in EPSG:4326 and transformed internally
- Special handling for EPSG:3857 (Web Mercator) with latitude limits (-85 to 85)
- Uses pyproj for accurate coordinate transformations

### GeoJSON Compliance

- Coordinates are proper Python lists (not tuples)
- All geometries wrapped in GeoJSON Feature format
- Compatible with standard GeoJSON tools and libraries
- Can be directly serialized to JSON

### Geometry Generation

- Points: Random coordinates within bbox
- LineStrings: Random vertices connected in sequence
- Polygons: Generated using center point and radius with random variations
- Circles: Created using Shapely's buffer operation for perfect circles
- All geometries respect the specified bounding box

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/anygeom-py.git
cd anygeom-py

# Install dependencies
poetry install

# Run tests
poetry run python test_anygeom.py

# Run examples
poetry run python example.py
```

### Building

```bash
# Build package
poetry build

# Install locally
pip install dist/anygeom_py-0.1.0-py3-none-any.whl
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for public methods
- Keep functions focused and minimal

### Testing

- Add tests for new features
- Ensure existing tests pass
- Test with different CRS codes
- Validate GeoJSON output format

## License

MIT License - see LICENSE file for details

## Author

Krishna Lodha (krishna@rottengrapes.tech)

## Links

- PyPI: https://pypi.org/project/anygeom-py/
- Repository: https://github.com/Rotten-Grapes-Pvt-Ltd/anygeom-py
- Issues: https://github.com/Rotten-Grapes-Pvt-Ltd/anygeom-py/issues
