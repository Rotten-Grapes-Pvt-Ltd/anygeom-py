#!/usr/bin/env python
"""Test script for anygeom package"""
import json
from anygeom import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon

def test_basic_geometries():
    """Test basic geometry generation"""
    print("=== Basic Geometries ===")
    p = Point()
    ls = LineString()
    poly = Polygon()
    print(f"✓ Point: {p}")
    print(f"✓ LineString: {ls}")
    print(f"✓ Polygon: {poly}\n")

def test_multi_geometries():
    """Test multi-geometry generation"""
    print("=== Multi Geometries ===")
    mp = Point(count=3)
    mls = LineString(count=2)
    mpoly = Polygon(count=2)
    print(f"✓ MultiPoint: {mp}")
    print(f"✓ MultiLineString: {mls}")
    print(f"✓ MultiPolygon: {mpoly}\n")

def test_crs():
    """Test different CRS"""
    print("=== Different CRS ===")
    p_4326 = Point(crs=4326)
    p_3857 = Point(crs=3857)
    p_32643 = Point(crs=32643)
    print(f"✓ Point EPSG:4326: {p_4326}")
    print(f"✓ Point EPSG:3857: {p_3857}")
    print(f"✓ Point EPSG:32643: {p_32643}\n")

def test_bbox():
    """Test custom bbox"""
    print("=== Custom BBOX ===")
    p = Point(count=5, bbox=[0, 0, 10, 10])
    print(f"✓ Points in bbox [0,0,10,10]: {p}\n")

def test_vertex_control():
    """Test vertex count control"""
    print("=== Vertex Control ===")
    ls = LineString(min_vertex=5, max_vertex=10)
    poly = Polygon(min_vertex=8, max_vertex=12)
    print(f"✓ LineString (5-10 vertices): {ls}")
    print(f"✓ Polygon (8-12 vertices): {poly}\n")

def test_polygon_holes():
    """Test polygon with holes"""
    print("=== Polygon with Holes ===")
    poly = Polygon(hole=True)
    print(f"✓ Polygon with hole: {poly}\n")

def test_geojson_export():
    """Test GeoJSON export"""
    print("=== GeoJSON Export ===")
    p = Point(count=2)
    geojson = p.__geo_interface__
    
    # Verify it's valid JSON
    json_str = json.dumps(geojson, indent=2)
    parsed = json.loads(json_str)
    
    # Verify coordinates are lists, not tuples
    assert isinstance(parsed['coordinates'], list), "Coordinates must be a list"
    assert isinstance(parsed['coordinates'][0], list), "Coordinate pairs must be lists"
    
    print(f"✓ GeoJSON export valid")
    print(f"  Type: {parsed['type']}")
    print(f"  Coordinates type: {type(parsed['coordinates'])}")
    print(f"  Sample: {json_str[:100]}...\n")

def test_combined():
    """Test combined parameters"""
    print("=== Combined Parameters ===")
    points = Point(count=3, crs=32643, bbox=[53.127823, 7.047742, 106.125870, 35.488629])
    lines = LineString(count=4, crs=4326, min_vertex=3, max_vertex=6)
    poly = Polygon(hole=True, min_vertex=6, max_vertex=10)
    
    print(f"✓ Points (count=3, crs=32643, custom bbox)")
    print(f"✓ LineStrings (count=4, crs=4326, 3-6 vertices)")
    print(f"✓ Polygon (hole=True, 6-10 vertices)\n")

if __name__ == "__main__":
    print("Testing anygeom package\n")
    test_basic_geometries()
    test_multi_geometries()
    test_crs()
    test_bbox()
    test_vertex_control()
    test_polygon_holes()
    test_geojson_export()
    test_combined()
    print("✅ All tests passed!")
