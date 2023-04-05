# ⚠️ invalid-geometry

**List of GeoJSON geometry issues with example files**

Ever encountered an *invalid geometry* error? Even if a GeoJSON conforms to the 
[GeoJSON specification](https://www.rfc-editor.org/rfc/rfc7946), some tools or APIs might have issues with it. 
This repo shows the common issues when handling GeoJSON geometries and how to fix them.
For a general introduction to GeoJSON see [here](https://macwright.com/2015/03/23/geojson-second-bite.html).

📝 means invalid by GeoJSON specification (links to the relevant section).

## Polygon

### Less than four nodes [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
A [Polygon's](https://macwright.com/2015/03/23/geojson-second-bite.html#polygons) exterior and inner ring (defines hole cutouts) 
must have four or more coordinate positions (also called nodes or vertices). In order to define an area (compared to a line) 
at least three positions are required, plus the first and last node must be the same to close the Polygon (see below).

### Unclosed Polygon [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
The first and last node of a polygons exterior or inner ring must be the same with identical values. This signifies the 
start and endpoint of a closed Polygon.

### Has duplicate nodes [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
From the closed Polygon requirement (see above), results that no two other positions of the 
exterior or interior ring can be the same, as then the start/endpoint of the ring could not be identified.

### Does not comply with right-hand rule [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.6)
A Polygon's exterior ring must have counterclockwise winding order, the inner ring (defines hole cutouts) must be clockwise. This is often overlooked when manually creating polygons or converting from other formats.
As an older specification version did not define the winding order, most tools will accept Polygons with invalid winding order,
but not all. To fix this see e.g. [geojson-rewind](https://github.com/mapbox/geojson-rewind).

### Has holes
A Polygon is allowed to have hole cutouts, this is a feature, not an issue. However, some APIs don't accept 
Polygon geometries with holes as input (e.g. some satellite data providers where the desired area is relevant for pricing).
The holes can be removed by removing the Polygon's [inner ring](https://macwright.com/2015/03/23/geojson-second-bite.html#polygons) coordinates.

### Self-intersection
Here one or multiple parts of the geometry overlap another part of itself. Often found in complex geometry shapes, 
after geometry operations without careful cleanup (buffer, raster-to-vector etc.).
A Polygon is allowed to have self-intersections, this is conform with the GeoJSON specification. However, it frequently 
causes issues in downstream applications thus is often rejected by APIs and tools.

A common approach for removing the self-intersections is applying a zero-buffer operation (e.g. `.buffer(0)` in shapely).
This dissolves the overlapping areas and usually is an okay solution for small, undesired self-intersections. 
However, especially for larger self-intersections this might lead to unintended changes of the geometry, as significant 
parts of the geometry could be removed by the operation. Here only a manual operation can fix the issue, by splitting of
the geometry into multiple parts, or adding/removing nodes.


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
### Coordinate reference system issues [📝](https://www.rfc-editor.org/rfc/rfc7946#section-4)
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

### Geometry crosses the antimeridian [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.9)
A Polygon or LineString that extends across the 180th meridian can lead to interoparability issues, and instead 
should be cut in two as a MultiPolygon or MultiLineString. 
Also see ["The 180th Meridian"](https://macwright.com/2016/09/26/the-180th-meridian.html) by Tom MacWright.

### Invalid bounding box coordinate order [📝](https://www.rfc-editor.org/rfc/rfc7946#section-3)
A `bbox` may be defined (but is not required) in the GeoJSON object to summarize the geometries on the Geometries, 
Features, or FeatureCollections level. If it is defined, the bbox coordinate order must conform to `[west, south, east, north]`.






### Not wrapped in a feature collection
    The Geojson standard actually allows not wrapping geometry objects in a featurecollection. A single point geometry or a single feature is still a valid GeojSON.
    it is still a valid geojson. However, some tools might expect a FeatureCollection.
    Also see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html
### Feature has no geometry
    Also valid, see https://macwright.com/2016/06/05/falsehoods-developers-believe-about-geojson.html



### ??? Sliver polygon (Polygon)
    A narrow polygon that is not supposed to exist due to small gaps in the input data.


### ??? Inner ring intersects or touches outer ring? (Polygon)