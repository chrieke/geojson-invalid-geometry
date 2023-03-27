# invalid-geometries

Examples GeoJSONs and explanation of invalid geometry issues (self-intersection etc.). When you encounter an 
"invalid geometry" error, this is the right place. For a general introduction to GeoJSON and the different geometry
types, see Tom MacRight's excellent article 
["More than you ever wanted to know about GeoJSON"](https://macwright.com/2015/03/23/geojson-second-bite.html)

If geometries are valid according to the [GeoJSON specification](https://www.rfc-editor.org/rfc/rfc7946),
this doesn't automatically mean that every tool or API will accept it as input. Thus this repository also lists
common issues you might encounter when using GeoJSONs in specific tools or APIs.

## Polygon / MultiPolygon
### Self-intersection (Polygon)
    A very common problem, one or multiple parts of the geometry overlap another part of itself. Often found 
    in complex geometry shapes, or after geometry operations without careful cleanup, raster-to-vector operations etc.
    With small intersections, often easy to fix with a simple `.buffer(0)` operation. This dissolves the overlapping
    area. However, if not being careful, this might lead to unintended changes of the geometry, especially common with larger
    self-intersections, as it could lead to significant parts of the geometry being removed.
### Holes (Polygon)
    A Polygon is allowed to have zero, one or any amount of holes. But many tools/apis don't accept polygons with holes.
    The holes can be removed by removing the polygon's inner ring coordinates.
### Winding order (Polygon)
    A Polygon exterior ring should be clockwise (not counterclockwise). A Polygon inner ring should be counter-clockwise (not clockwise).
### Less than four nodes (Polygon)
### First and last node not the same (Polygon)
    The first and last vertices of a polygons exterior or inner ring must be the same. Also referred to as "non closed" polygon or "unclosed ring".
### Duplicate nodes (Polygon)
    If any two or more coordinates are the same (except the first and last coordinate which is mandatory to be the same). Counts for both the exterior and inetrior rings.
### ??? Sliver polygon (Polygon)
    A narrow polygon that is not supposed to exist due to small gaps in the input data.
### ??? Self-touching rings (Polygon)
    a polygon has rings that touch but not at a common point. makes sense.
### ??? Inner ring intersects outer ring? (Polygon)


### Line / MultiLine
## Fewer than two points (Line)
## Zero-length lines (Line)
    a line has no length
### ??? Multi-line strings with intersecting lines (Multiline)
    two or more lines in a multi-line string intersect with each other
### two line strings in a multi-line string overlap (Multiline)
    ??? Should be valid? 


## All Geometries
### More than three coordinates
    Only three coordinates are allowed per vertex `[longitude, latitude, elevation]` as defined in the current GeoJSON 
    [specification](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1). In earlier GeoJSON specifications, more than
    three coordinates were allowed, people stored property information like time, heard rate as another "coordinate" point. 
    Now, additional properties need to be stored in the feature's property field.
### Disconnected geometries (All Geometries)
    a geometry object has disconnected parts and is not a multipolygon.
### Multi-Geometry, but just one geometry (All Multigeometries)
    Works in most cases, but some tools complain
### Incorrect geometry data types (All Geometries)
    for example, a polygon is defined as a line string
### Coordinate reference system issues
    The GeoJSON specification defines all geojson as being in WGS84 with latitude / longitude decimal coordinates. 
    Thus, the CRS does not need to be specified in the GeoJSON, there is only a single correct one. Many tools disregard a defined crs.
    However, some tools (e.g. QGIS) do not respect this and export GeoJSONs with a different CRS. This can cause issues when you try to use the GeoJSON in a different tool (e.g. Leaflet). The following examples show how to fix this.
    Could also be that the defined crs does not match the coordinates
### "3D coordinates" not accepted
    As above, a vertex coordinates are defined as `[longitude, latitude, elevation]`. However, some tools/APIs actually even have 
    issues with the elevation coordinates ("3D coordinates") and only accept the longitude and latitude pair.
### ??? crossing the antimeridian or poles: polygon or linestring
    jumps the 180 meridian, see https://macwright.com/2015/03/23/geojson-second-bite.html
### ??? Floating-point precision errors (All Geometries)
    due to the limitations of floating-point arithmetic, some geometries may have small errors in their coordinates
### Has no bounding box (All geometries)
    Can have but doesnt require bounding bix
### Not wrapped in a feature collection
    The Geojson standard actually allows not wrapping geometry objects in a featurecollection. A single point geometry or a single feature is still a valid GeojSON.
    it is still a valid geojson. However,  many tools expect a featurecollection.
    Also see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html
### Feature has no geometry
    Also valid, see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html
### coincident coordinates
### ??? Invalid geometries due to degenerate geometry
    for example, a polygon has zero area or a line string has zero length, leading to invalid geometries





