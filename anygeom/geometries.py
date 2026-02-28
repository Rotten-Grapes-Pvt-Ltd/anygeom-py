import random
import json
from typing import Optional, List, Tuple
from shapely import geometry
from shapely.geometry.base import BaseGeometry
from pyproj import Transformer

def _get_default_bbox(crs: int) -> List[float]:
    """Get appropriate default bbox for the given CRS"""
    if crs == 3857:  # Web Mercator has limited latitude range
        return [-180, -85, 180, 85]
    return [-180, -90, 180, 90]

def _validate_bbox(bbox: List[float]) -> None:
    """Validate bbox format and values"""
    if len(bbox) != 4:
        raise ValueError(f"bbox must have exactly 4 values [minx, miny, maxx, maxy], got {len(bbox)}")
    if bbox[0] >= bbox[2]:
        raise ValueError(f"bbox minx ({bbox[0]}) must be less than maxx ({bbox[2]})")
    if bbox[1] >= bbox[3]:
        raise ValueError(f"bbox miny ({bbox[1]}) must be less than maxy ({bbox[3]})")

def _transform_bbox(bbox: List[float], from_crs: int, to_crs: int) -> List[float]:
    transformer = Transformer.from_crs(f"EPSG:{from_crs}", f"EPSG:{to_crs}", always_xy=True)
    x1, y1 = transformer.transform(bbox[0], bbox[1])
    x2, y2 = transformer.transform(bbox[2], bbox[3])
    return [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]

def _random_point(bbox: List[float]) -> Tuple[float, float]:
    return (random.uniform(bbox[0], bbox[2]), random.uniform(bbox[1], bbox[3]))

def _to_geojson(geom: BaseGeometry) -> dict:
    """Convert shapely geometry to proper GeoJSON dict with lists instead of tuples"""
    return json.loads(json.dumps(geom.__geo_interface__))

def _to_feature(geom: BaseGeometry) -> dict:
    """Convert shapely geometry to GeoJSON Feature"""
    return {
        "type": "Feature",
        "properties": {},
        "geometry": _to_geojson(geom)
    }

class _GeometryWrapper:
    def __init__(self, geom: BaseGeometry):
        self._geom = geom
    
    def __getattr__(self, name):
        return getattr(self._geom, name)
    
    @property
    def __geo_interface__(self):
        return _to_feature(self._geom)
    
    def __repr__(self):
        return repr(self._geom)
    
    def __str__(self):
        return str(self._geom)

class _GeometryListWrapper:
    def __init__(self, geoms: List[BaseGeometry]):
        self._geoms = geoms
    
    def __getitem__(self, index):
        return _GeometryWrapper(self._geoms[index])
    
    def __len__(self):
        return len(self._geoms)
    
    def __iter__(self):
        return iter([_GeometryWrapper(g) for g in self._geoms])
    
    @property
    def __geo_interface__(self):
        return [_to_feature(g) for g in self._geoms]
    
    def __repr__(self):
        return f"[{', '.join(repr(g) for g in self._geoms)}]"
    
    def __str__(self):
        return f"[{', '.join(str(g) for g in self._geoms)}]"

class Point:
    def __new__(cls, count: int = 1, crs: int = 4326, bbox: Optional[List[float]] = None):
        if count < 1:
            raise ValueError(f"count must be at least 1, got {count}")
        
        bbox = bbox or _get_default_bbox(crs if bbox is None else 4326)
        _validate_bbox(bbox)
        if crs != 4326:
            bbox = _transform_bbox(bbox, 4326, crs)
        
        if count == 1:
            return _GeometryWrapper(geometry.Point(_random_point(bbox)))
        
        points = [geometry.Point(_random_point(bbox)) for _ in range(count)]
        return _GeometryListWrapper(points)

class MultiPoint:
    def __new__(cls, count: int = 2, crs: int = 4326, bbox: Optional[List[float]] = None):
        if count < 2:
            raise ValueError(f"count must be at least 2 for MultiPoint, got {count}")
        
        if bbox is None:
            bbox = _get_default_bbox(crs if bbox is None else 4326)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        else:
            _validate_bbox(bbox)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        
        points = [_random_point(bbox) for _ in range(count)]
        return _GeometryWrapper(geometry.MultiPoint(points))

class LineString:
    def __new__(cls, count: int = 1, crs: int = 4326, bbox: Optional[List[float]] = None, 
                min_vertex: int = 2, max_vertex: int = 5):
        if min_vertex > max_vertex:
            raise ValueError(f"min_vertex ({min_vertex}) cannot be greater than max_vertex ({max_vertex})")
        if min_vertex < 2:
            raise ValueError(f"min_vertex must be at least 2 for LineString, got {min_vertex}")
        
        bbox_provided = bbox is not None
        bbox = bbox or _get_default_bbox(crs)
        if bbox_provided:
            _validate_bbox(bbox)
        if crs != 4326 and bbox_provided:
            bbox = _transform_bbox(bbox, 4326, crs)
        elif crs != 4326:
            bbox = _transform_bbox(bbox, 4326, crs)
        
        if count == 1:
            n_vertices = random.randint(min_vertex, max_vertex)
            coords = [_random_point(bbox) for _ in range(n_vertices)]
            return _GeometryWrapper(geometry.LineString(coords))
        
        lines = []
        for _ in range(count):
            n_vertices = random.randint(min_vertex, max_vertex)
            coords = [_random_point(bbox) for _ in range(n_vertices)]
            lines.append(geometry.LineString(coords))
        return _GeometryListWrapper(lines)

class MultiLineString:
    def __new__(cls, count: int = 2, crs: int = 4326, bbox: Optional[List[float]] = None,
                min_vertex: int = 2, max_vertex: int = 5):
        if count < 2:
            raise ValueError(f"count must be at least 2 for MultiLineString, got {count}")
        if min_vertex > max_vertex:
            raise ValueError(f"min_vertex ({min_vertex}) cannot be greater than max_vertex ({max_vertex})")
        if min_vertex < 2:
            raise ValueError(f"min_vertex must be at least 2 for LineString, got {min_vertex}")
        
        if bbox is None:
            bbox = _get_default_bbox(crs)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        else:
            _validate_bbox(bbox)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        
        lines = []
        for _ in range(count):
            n_vertices = random.randint(min_vertex, max_vertex)
            coords = [_random_point(bbox) for _ in range(n_vertices)]
            lines.append(coords)
        return _GeometryWrapper(geometry.MultiLineString(lines))

class Polygon:
    def __new__(cls, count: int = 1, crs: int = 4326, bbox: Optional[List[float]] = None,
                min_vertex: int = 3, max_vertex: int = 8, hole: bool = False):
        if min_vertex > max_vertex:
            raise ValueError(f"min_vertex ({min_vertex}) cannot be greater than max_vertex ({max_vertex})")
        if min_vertex < 3:
            raise ValueError(f"min_vertex must be at least 3 for Polygon, got {min_vertex}")
        
        bbox_provided = bbox is not None
        bbox = bbox or _get_default_bbox(crs)
        if bbox_provided:
            _validate_bbox(bbox)
        if crs != 4326 and bbox_provided:
            bbox = _transform_bbox(bbox, 4326, crs)
        elif crs != 4326:
            bbox = _transform_bbox(bbox, 4326, crs)
        
        if count == 1:
            n_vertices = random.randint(max(3, min_vertex), max_vertex)
            center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            radius = min(bbox[2] - bbox[0], bbox[3] - bbox[1]) / 4
            
            coords = []
            for i in range(n_vertices):
                angle = 2 * 3.14159 * i / n_vertices
                x = center[0] + radius * random.uniform(0.5, 1) * (1 if i % 2 else -1) * abs(random.gauss(0, 0.3))
                y = center[1] + radius * random.uniform(0.5, 1) * (1 if i % 2 else -1) * abs(random.gauss(0, 0.3))
                coords.append((center[0] + radius * random.uniform(0.7, 1.0) * (1 + 0.3 * random.random()) * (1 if angle < 3.14159 else -1),
                              center[1] + radius * random.uniform(0.7, 1.0) * (1 + 0.3 * random.random()) * (1 if (angle > 1.57 and angle < 4.71) else -1)))
            
            coords = sorted(coords, key=lambda p: (p[0] - center[0], p[1] - center[1]))
            coords.append(coords[0])
            
            holes = None
            if hole:
                hole_radius = radius * 0.4
                hole_coords = []
                for i in range(max(3, n_vertices // 2)):
                    angle = 2 * 3.14159 * i / max(3, n_vertices // 2)
                    hole_coords.append((center[0] + hole_radius * (1 + 0.2 * random.random()) * (1 if angle < 3.14159 else -1),
                                       center[1] + hole_radius * (1 + 0.2 * random.random()) * (1 if (angle > 1.57 and angle < 4.71) else -1)))
                hole_coords = sorted(hole_coords, key=lambda p: (p[0] - center[0], p[1] - center[1]))
                hole_coords.append(hole_coords[0])
                holes = [hole_coords]
            
            return _GeometryWrapper(geometry.Polygon(coords, holes=holes))
        
        polygons = []
        for _ in range(count):
            n_vertices = random.randint(max(3, min_vertex), max_vertex)
            center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            radius = min(bbox[2] - bbox[0], bbox[3] - bbox[1]) / 4
            
            coords = []
            for i in range(n_vertices):
                angle = 2 * 3.14159 * i / n_vertices
                x = center[0] + radius * random.uniform(0.5, 1) * (1 if i % 2 else -1) * abs(random.gauss(0, 0.3))
                y = center[1] + radius * random.uniform(0.5, 1) * (1 if i % 2 else -1) * abs(random.gauss(0, 0.3))
                coords.append((center[0] + radius * random.uniform(0.7, 1.0) * (1 + 0.3 * random.random()) * (1 if angle < 3.14159 else -1),
                              center[1] + radius * random.uniform(0.7, 1.0) * (1 + 0.3 * random.random()) * (1 if (angle > 1.57 and angle < 4.71) else -1)))
            
            coords = sorted(coords, key=lambda p: (p[0] - center[0], p[1] - center[1]))
            coords.append(coords[0])
            
            holes = None
            if hole:
                hole_radius = radius * 0.4
                hole_coords = []
                for i in range(max(3, n_vertices // 2)):
                    angle = 2 * 3.14159 * i / max(3, n_vertices // 2)
                    hole_coords.append((center[0] + hole_radius * (1 + 0.2 * random.random()) * (1 if angle < 3.14159 else -1),
                                       center[1] + hole_radius * (1 + 0.2 * random.random()) * (1 if (angle > 1.57 and angle < 4.71) else -1)))
                hole_coords = sorted(hole_coords, key=lambda p: (p[0] - center[0], p[1] - center[1]))
                hole_coords.append(hole_coords[0])
                holes = [hole_coords]
            
            polygons.append(geometry.Polygon(coords, holes=holes))
        return _GeometryListWrapper(polygons)

class MultiPolygon:
    def __new__(cls, count: int = 2, crs: int = 4326, bbox: Optional[List[float]] = None,
                min_vertex: int = 3, max_vertex: int = 8, hole: bool = False):
        if count < 2:
            raise ValueError(f"count must be at least 2 for MultiPolygon, got {count}")
        if min_vertex > max_vertex:
            raise ValueError(f"min_vertex ({min_vertex}) cannot be greater than max_vertex ({max_vertex})")
        if min_vertex < 3:
            raise ValueError(f"min_vertex must be at least 3 for Polygon, got {min_vertex}")
        
        if bbox is None:
            bbox = _get_default_bbox(crs)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        else:
            _validate_bbox(bbox)
            if crs != 4326:
                bbox = _transform_bbox(bbox, 4326, crs)
        
        polygons = []
        for _ in range(count):
            poly = Polygon(count=1, crs=4326, bbox=bbox, min_vertex=min_vertex, max_vertex=max_vertex, hole=hole)
            polygons.append(poly._geom)
        return _GeometryWrapper(geometry.MultiPolygon(polygons))

class Circle:
    def __new__(cls, count: int = 1, crs: int = 4326, bbox: Optional[List[float]] = None,
                radius: Optional[float] = None, num_points: int = 64):
        if count < 1:
            raise ValueError(f"count must be at least 1, got {count}")
        if num_points < 8:
            raise ValueError(f"num_points must be at least 8 for Circle, got {num_points}")
        
        bbox_provided = bbox is not None
        bbox = bbox or _get_default_bbox(crs)
        if bbox_provided:
            _validate_bbox(bbox)
        if crs != 4326 and bbox_provided:
            bbox = _transform_bbox(bbox, 4326, crs)
        elif crs != 4326:
            bbox = _transform_bbox(bbox, 4326, crs)
        
        if count == 1:
            center = _random_point(bbox)
            if radius is None:
                radius = min(bbox[2] - bbox[0], bbox[3] - bbox[1]) * random.uniform(0.05, 0.15)
            
            coords = []
            for i in range(num_points):
                angle = 2 * 3.14159265359 * i / num_points
                x = center[0] + radius * (1 if angle < 3.14159 else -1) * abs((angle % 3.14159) / 3.14159)
                y = center[1] + radius * (1 if (angle > 1.57 and angle < 4.71) else -1) * abs(((angle + 1.57) % 3.14159) / 3.14159)
                coords.append((center[0] + radius * (1 if angle < 3.14159 else -1),
                              center[1] + radius * (1 if (angle > 1.57 and angle < 4.71) else -1)))
            coords.append(coords[0])
            
            return _GeometryWrapper(geometry.Point(center).buffer(radius, resolution=num_points//4))
        
        circles = []
        for _ in range(count):
            center = _random_point(bbox)
            if radius is None:
                r = min(bbox[2] - bbox[0], bbox[3] - bbox[1]) * random.uniform(0.05, 0.15)
            else:
                r = radius
            circles.append(geometry.Point(center).buffer(r, resolution=num_points//4))
        return _GeometryListWrapper(circles)
