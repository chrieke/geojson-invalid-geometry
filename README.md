# invalid-geometry

List of invalid GeoJSON geometry issues (self-intersection etc.) with example files

Ever encountered an "invalid geometry" error? Even if a GeoJSON technically [conforms](https://github.com/tmcw/awesome-geojson#validation) to the 
[GeoJSON specification](https://www.rfc-editor.org/rfc/rfc7946), using it with certain tools or APIs might still cause 
issues. This is a list of common issues and how to fix them. If the issue relates to the GeoJSON specification it is indicated 
with a link to the relevant section.

For a general introduction to GeoJSON, the different geometry types and how they are constructed, see Tom MacRight's excellent article 
["More than you ever wanted to know about GeoJSON"](https://macwright.com/2015/03/23/geojson-second-bite.html)

Notes
"Positions" are coordinate pairs, here used interchangebly with "nodes" and "vertices" (singular "vertex").


## Polygon
### Does not comply with right-hand rule [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
A Polygon's exterior ring must have counterclockwise winding order, the inner ring must be clockwise. This is a common 
issue when manually creating polygons or converting from other formats.

### Less than four nodes [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
The exterior or inner ring of a polygon must be a closed LineString with four or more positions.

### First and last node not equivalent [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
The first and last position of a polygons exterior or inner ring must be the same. Also referred to as un-closed polygon or ring.

### Has duplicate nodes [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
The requirement for equivalent first and last positions (see above) results in that no two other positions of the 
exterior or interior ring can be the same, as then the start/endpoint of the ring could not be identified.

### Self-intersection
    A very common problem, one or multiple parts of the geometry overlap another part of itself. Often found 
    in complex geometry shapes, or after geometry operations without careful cleanup, raster-to-vector operations etc.
    With small intersections, often easy to fix with a simple `.buffer(0)` operation. This dissolves the overlapping
    area. However, if not being careful, this might lead to unintended changes of the geometry, especially common with larger
    self-intersections, as it could lead to significant parts of the geometry being removed.

### Has holes
    A Polygon is allowed to have any amount of holes. But many tools/apis don't accept polygons with holes.
    The holes can be removed by removing the polygon's inner ring coordinates.

### ??? Sliver polygon (Polygon)
    A narrow polygon that is not supposed to exist due to small gaps in the input data.
### ??? Has self-touching rings (Polygon)
    a polygon has rings that touch but not at a common point. makes sense.
### ??? Inner ring intersects outer ring? (Polygon)


### Line / MultiLine
## Zero-length lines (Line)
    a line has no length
### ??? Multi-line strings with intersecting lines (Multiline)
    two or more lines in a multi-line string intersect with each other
### two line strings in a multi-line string overlap (Multiline)
    ??? Should be valid? 


## All Geometries
### More than three coordinates in a node
A [position](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1) must consist of either two coordinates (order `[longitude, latitude]`) or three coordinates 
(`[longitude, latitude, elevation]`). Altitude/Elevation is optional. In early versions of the GeoJSON specification, more than
three coordinates were allowed, e.g. storing additional information like time etc. Doing this may now lead to errors 
or the additional values being ignored. The additional information must now be stored separately in the properties of the feature.

### Disconnected geometries (All Geometries)
    a geometry object has disconnected parts and is not a multipolygon.
### Multi-Geometry, but just one geometry (All Multigeometries)
    Works in most cases, but some tools complain
### Incorrect geometry data types (All Geometries)
    for example, a polygon is defined as a line string
### Coordinate reference system issues [spec](https://www.rfc-editor.org/rfc/rfc7946#section-4)
The GeoJSON specification defines all GeoJSON as being in the [WGS84](https://de.wikipedia.org/wiki/World_Geodetic_System_1984) 
coordinate reference system (CRS) with latitude / longitude decimal coordinates. Thus, the CRS does not need to be 
specified in the GeoJSON. In older GeoJSON specifications you could define alternative crs, however this can lead to 
interoparability issues with some tools/APIs if they ignore the crs definition and assume WGS84.

### "3D coordinates" not accepted
    As above, a vertex coordinates are defined as `[longitude, latitude, elevation]`. However, some tools/APIs actually even have 
    issues with the elevation coordinates ("3D coordinates") and only accept the longitude and latitude pair.

### Excessive coordinate precision
Allthough not mandatory, the GeoJSON specification [recommends](https://www.rfc-editor.org/rfc/rfc7946#section-11.2) 
a coordinate precision of 6 decimal places. Using more than 6 decimal places may lead to issues with some tools/APIs and 
unncessarily increase the file size (6 decimal places corresponds to about 10cm of a GPS).

### Geometry crosses the antimeridian [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.9)
A Polygon or LineString that extends across the 180th meridian can lead to interoparability issues, and instead 
should be cut in two as a MultiPolygon or MultiLineString. 
Also see ["The 180th Meridian"](https://macwright.com/2016/09/26/the-180th-meridian.html) by Tom MacWright.

### Invalid bounding box coordinate order [spec](https://www.rfc-editor.org/rfc/rfc7946#section-3)
A `bbox` may be defined (but is not required) in the GeoJSON object to summarize the geometries on the Geometries, 
Features, or FeatureCollections level. If it is defined, the bbox coordinate order must conform to `[west, south, east, north]`.






### Not wrapped in a feature collection
    The Geojson standard actually allows not wrapping geometry objects in a featurecollection. A single point geometry or a single feature is still a valid GeojSON.
    it is still a valid geojson. However, some tools might expect a FeatureCollection.
    Also see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html
### Feature has no geometry
    Also valid, see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html






