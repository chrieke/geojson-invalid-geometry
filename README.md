# invalid-geometries

Explanation and examples GeoJSONs of invalid geometry issues (holes, self-intersection etc.).
Whenever you encounter an "invalid geometry" issue, this repo will help you deal with it.
This repository also addresses issues outside the GeoJSON specification, which might be specific 
to certain tools or APIs when using GeoJSON input data.

For a general introduction to GeoJSON see Tom MacRight's excellent article
["More than you ever wanted to know about GeoJSON"](https://macwright.com/2015/03/23/geojson-second-bite.html)



## Self-intersection
A very common problem, one or multiple parts of the geometry overlap another part of itself. Often found 
in complex geometry shapes, or after geometry operations without careful cleanup, raster-to-vector operations etc.
With small intersections, often easy to fix with a simple `.buffer(0)` operation. This dissolves the overlapping
area. However, if not being careful, this might lead to unintended changes of the geometry, especially common with larger
self-intersections, as it could lead to significant parts of the geometry being removed.

## Polygon specific, also applies to Multipolygons
### Polygon holes

### Polygon vertices
    ### Polygon less than four nodes
    ### Polygon first last node not the same
    ### Polygon duplicate nodes+vertices 
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

### Multipolygon specific
## Multipolygon but just one Polygong
   Works in most cases, but some tools complain


### Line specific
## Fewer than two points
## Zero-length lines: a line has no length

## Multiline specific
### ??? Multi-line strings with intersecting lines: two or more lines in a multi-line string intersect with each other


## All types
### Geometries with incorrect data types: for example, a polygon is defined as a line string

## Coordinate reference system issues
The GeoJSON specification defines all geojson as being in WGS84 with latitude / longitude decimal coordinates. 
Thus, the CRS does not need to be specified in the GeoJSON, there is only a single correct one. However, the  
However, some tools (e.g. QGIS) do not respect this and export GeoJSONs with a different CRS. This can cause issues when you try to use the GeoJSON in a different tool (e.g. Leaflet). The following examples show how to fix this.


### Polygon 3D coordinates (elevation)
    This is valid, but some apis/tools have issues with it.
### More than three coordinates
"Before the current specification was released, GeoJSON allowed the storage of more than 3 coordinates per position, and sometimes people would use that to store time, heart rate, and so on. This wasn’t well supported in GeoJSON tools, and is forbidden by the new specification. https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1"




odds:
Floating-point precision errors: due to the limitations of floating-point arithmetic, some geometries may have small errors in their coordinates


