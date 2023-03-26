# invalid-geometries

Examples GeoJSONs and explanation of invalid geometry issues (self-intersection etc.). When you encounter an 
"invalid geometry" error, this is the right place. For a general introduction to GeoJSON instead see Tom MacRight's 
excellent article ["More than you ever wanted to know about GeoJSON"](https://macwright.com/2015/03/23/geojson-second-bite.html)

If geometries are valid according to the [GeoJSON specification](https://www.rfc-editor.org/rfc/rfc7946),
this doesn't automatically mean that every tool or API will accept it as input. Thus this repository also lists
common issues you might encounter when using GeoJSONs in specific tools or APIs.

## Self-intersection
A very common problem, one or multiple parts of the geometry overlap another part of itself. Often found 
in complex geometry shapes, or after geometry operations without careful cleanup, raster-to-vector operations etc.
With small intersections, often easy to fix with a simple `.buffer(0)` operation. This dissolves the overlapping
area. However, if not being careful, this might lead to unintended changes of the geometry, especially common with larger
self-intersections, as it could lead to significant parts of the geometry being removed.

## Polygon specific, also applies to Multipolygons
### Polygon holes
    Not invalid in the specification, a polygon can have any amount of holes + inner rings. But many tools/apis have issues with holes.

### Polygon vertices
    ### Polygon less than four nodes
    ### Polygon first last node not the same
    ### Polygon duplicate nodes+vertices (in exterior or inner rings)
    two or more vertices have the same coordinates (except for the last node, which must be the same as the first node)
    ### Polygon inner ring first&last node not same
        Same for exterior?
### Polygon winding order
    #### Polygon inner ring not clockwise winding
    ### Polygon exterior ring not counterclockwise winding
### ???Non-closed polygons: a polygon does not have a closed boundary
### ???Unclosed rings: a ring within a polygon does not close
### Disconnected geometries: a geometry object has disconnected parts and is not a multipolygon.
### ??? Invalid polygon due to a sliver: a narrow polygon that is not supposed to exist due to small gaps in the input data.
### ??? Invalid polygons due to self-touching rings: a polygon has rings that touch but not at a common point. makes sense.
### ??? Inner ring intersects outer ring?


### Multipolygon specific
## Multipolygon but just one Polygon/line etc
   Works in most cases, but some tools complain


### Line specific
## Fewer than two points
## Zero-length lines: a line has no length

## Multiline specific
### ??? Multi-line strings with intersecting lines: two or more lines in a multi-line string intersect with each other
### ??? Should be valid? two line strings in a multi-line string overlap

## All types
### Geometries with incorrect data types: for example, a polygon is defined as a line string

## Coordinate reference system issues
The GeoJSON specification defines all geojson as being in WGS84 with latitude / longitude decimal coordinates. 
Thus, the CRS does not need to be specified in the GeoJSON, there is only a single correct one. However, the  
However, some tools (e.g. QGIS) do not respect this and export GeoJSONs with a different CRS. This can cause issues when you try to use the GeoJSON in a different tool (e.g. Leaflet). The following examples show how to fix this.
Could also be that the defined crs does not match the coordinates


### More than three coordinates
Only three coordinates are allowed per vertex `[longitude, latitude, elevation]` as defined in the current GeoJSON 
[specification](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1). In earlier GeoJSON specifications, more than
three coordinates were allowed, people stored property information like time, heard rate as another "coordinate" point. 
Now, additional properties need to be stored in the feature's property field.

## "3D coordinates" not accepted
As above, a vertex coordinates are defined as `[longitude, latitude, elevation]`. However, some tools/APIs actually even have 
issues with the elevation coordinates ("3D coordinates") and only accept the longitude and latitude pair.

### ??? crossing the antimeridian or poles: polygon or linestring




odds:
Floating-point precision errors: due to the limitations of floating-point arithmetic, some geometries may have small errors in their coordinates



# Can have but doesnt require bounding bix



??? Invalid geometries due to incorrect feature types: for example, a point feature is defined as a polygon, or a line feature is defined as a point
coincident coordinates
??? Invalid geometries due to degenerate geometry: for example, a polygon has zero area or a line string has zero length, leading to invalid geometries