"""Regenerate the two overview PNGs in repo_images/.

Run with `python repo_images/make_repo_images.py` (needs matplotlib and numpy).

Shapes are read from the actual files in examples/ so the pictures stay in sync
with the README's list of issues (same order as the README sections). A few
cells that have nothing to show geometrically (outside lat/lon boundary,
crosses anti-meridian, zero-length LineString) use a schematic shape instead.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
OUT = ROOT / "repo_images"

FONT = "Arial Rounded MT Bold"
TEXT_COLOR = "#111111"
EDGE = "#1a1a1a"
ACCENT = "#EE1C25"  # red used for the annotations (arrows, nodes)

# Palette taken from the previous versions of the images.
GREEN = "#6BAF6B"
PURPLE = "#8C6BBF"
GOLD = "#D9A400"
PINK = "#F4A7BB"
CYAN = "#23B5E8"
DARKRED = "#C0414B"
CRIMSON = "#E8194B"
TAN = "#C8BD9C"
LIME = "#A9C93A"
ORANGE = "#F5941F"
PLUM = "#8E5AA8"
BROWN = "#A97148"
STEEL = "#9CA9C4"
TEAL = "#4BAFA0"
SAND = "#E0B25E"

CELL_W = 9.2
ROW_H = 10.4
SHAPE_H = 6.0
LABEL_TOP = -0.9  # first label line, below the shape box
LINE_H = 1.15
FONT_SIZE = 15


def geometry(path):
    """Return the geometry of an example file, unwrapping a FeatureCollection."""
    data = json.loads((EXAMPLES / path).read_text())
    return data["features"][0]["geometry"] if "features" in data else data


def positions(path):
    """Return the raw positions of the first ring, with any z/m values kept."""
    ring = geometry(path)["coordinates"]
    while isinstance(ring[0][0], list):
        ring = ring[0]
    return ring


def rings(path):
    """Return the polygon/linestring rings of an example file as arrays."""
    coords = geometry(path)["coordinates"]
    # Normalize to a list of rings, based on nesting depth rather than on the
    # declared type (one example deliberately mislabels its type).
    depth, probe = 0, coords
    while isinstance(probe, list):
        depth += 1
        probe = probe[0]
    if depth == 2:  # LineString
        coords = [coords]
    elif depth == 4:  # MultiPolygon
        coords = coords[0]
    return [np.array([c[:2] for c in ring], dtype=float) for ring in coords]


def signed_area(ring):
    x, y = ring[:, 0], ring[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def fit(shapes, box_w, box_h, scale=1.0):
    """Scale/center a list of point arrays into a box, keeping the aspect."""
    allpts = np.vstack(shapes)
    lo, hi = allpts.min(axis=0), allpts.max(axis=0)
    span = np.maximum(hi - lo, 1e-12)
    f = min(box_w / span[0], box_h / span[1]) * scale
    center = (lo + hi) / 2
    return [(s - center) * f for s in shapes]


class Cell:
    """One shape + caption slot on the canvas."""

    def __init__(self, ax, col, row, label, box_w=8.6, box_h=SHAPE_H):
        self.ax = ax
        self.x = col * CELL_W
        self.y = -row * ROW_H
        self.label = label
        self.box_w = box_w
        self.box_h = box_h

    def place(self, shapes, scale=1.0):
        return [p + (self.x, self.y) for p in fit(shapes, self.box_w, self.box_h, scale)]

    def polygon(self, shapes, color, scale=1.0, lw=1.6):
        pts = self.place(shapes, scale)
        # Matplotlib fills compound paths by the nonzero winding rule, so an
        # inner ring only cuts a hole if it runs opposite to the exterior.
        # Some examples deliberately have the "wrong" winding order — flip the
        # inner rings for drawing only, the returned points stay as-is.
        drawn = [pts[0]] + [
            r[::-1] if np.sign(signed_area(r)) == np.sign(signed_area(pts[0])) else r
            for r in pts[1:]
        ]
        verts, codes = [], []
        for ring in drawn:
            verts.extend(ring)
            codes.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(ring) - 1))
        patch = PathPatch(
            MplPath(verts, codes),
            facecolor=color,
            edgecolor=EDGE,
            lw=lw,
            joinstyle="round",
        )
        self.ax.add_patch(patch)
        return pts

    def line(self, shapes, scale=1.0):
        pts = self.place(shapes, scale)
        for ring in pts:
            self.ax.plot(ring[:, 0], ring[:, 1], color=EDGE, lw=1.8)
        return pts

    def caption(self):
        for i, line in enumerate(self.label.split("\n")):
            self.ax.text(
                self.x,
                self.y + LABEL_TOP - self.box_h / 2 - i * LINE_H,
                line,
                ha="center",
                va="top",
                fontsize=FONT_SIZE,
                fontweight="bold",
                fontname=FONT,
                color=TEXT_COLOR,
            )

    def note(self, text, y=-2.85, size=12, color=ACCENT):
        """Small annotation between the shape and the caption."""
        self.ax.text(self.x, self.y + y, text, ha="center", va="top",
                     fontsize=size, fontweight="bold", fontname=FONT, color=color)

    def arrow(self, start, end, lw=3.0):
        """Arrow in cell-relative units (0,0 = cell center)."""
        self.ax.annotate(
            "",
            xy=(self.x + end[0], self.y + end[1]),
            xytext=(self.x + start[0], self.y + start[1]),
            arrowprops=dict(arrowstyle="-|>,head_width=0.32,head_length=0.7",
                            color=ACCENT, lw=lw, shrinkA=0, shrinkB=0),
        )

    def turn_arrow(self, center, radius, start_deg, sweep_deg):
        """Curved arrow showing a winding direction; sweep > 0 is counter-clockwise."""
        cx, cy = self.x + center[0], self.y + center[1]
        t = np.radians(np.linspace(start_deg, start_deg + sweep_deg, 80))
        arc = np.column_stack([cx + radius * np.cos(t), cy + radius * np.sin(t)])
        self.ax.plot(arc[:-3, 0], arc[:-3, 1], color=ACCENT, lw=2.6,
                     solid_capstyle="round", zorder=4)
        self.ax.annotate(
            "", xy=arc[-1], xytext=arc[-4],
            arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.62",
                            color=ACCENT, lw=2.6, shrinkA=0, shrinkB=0),
            zorder=4,
        )


def canvas(ncols, nrows, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_xlim(-CELL_W / 2, ncols * CELL_W - CELL_W / 2)
    ax.set_ylim(-(nrows - 1) * ROW_H - 6.2, 4.2)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / name, dpi=170, facecolor="white",
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("wrote", OUT / name)


# --------------------------------------------------------------------------
# 1) Invalid by GeoJSON specification
# --------------------------------------------------------------------------
def invalid_examples():
    fig, ax = canvas(5, 1, (15.5, 4.2))

    # Unclosed – the ring is drawn only along the coordinates that exist,
    # so the missing closing segment stays visible as a gap.
    c = Cell(ax, 0, 0, "Unclosed")
    ring = rings("invalid_geometries/invalid_unclosed.geojson")[0]
    pts = c.place([ring], scale=0.82)[0]
    ax.fill(pts[:, 0], pts[:, 1], color=GREEN, zorder=1)
    ax.plot(pts[:, 0], pts[:, 1], color=EDGE, lw=1.6, zorder=2)
    ax.scatter(pts[[0, -1], 0], pts[[0, -1], 1], s=42, color=ACCENT, zorder=3)
    c.caption()

    # Fewer than three unique nodes – collapses to a line.
    c = Cell(ax, 1, 0, "Fewer 3 unique nodes")
    c.line(rings("invalid_geometries/invalid_less_three_unique_nodes.geojson"),
           scale=0.85)
    c.caption()

    # Exterior ring not counter-clockwise.
    c = Cell(ax, 2, 0, "Exterior ring not\ncounter-clockwise")
    c.polygon(rings("invalid_geometries/invalid_exterior_not_ccw.geojson"),
              PURPLE, scale=0.9)
    # Curved arrow hugging the right edge, showing the ring's actual
    # (clockwise, i.e. wrong) direction.
    c.turn_arrow((0.0, 0.0), 3.8, 68, -130)
    c.caption()

    # Interior ring not clockwise – the hole is cut out, the curved arrow shows
    # the ring's actual (counter-clockwise, i.e. wrong) direction.
    c = Cell(ax, 3, 0, "Interior ring not\nclockwise")
    c.polygon(rings("invalid_geometries/invalid_interior_not_cw.geojson"),
              GOLD, scale=0.95)
    c.turn_arrow((-0.6, -0.75), 0.95, -30, 300)
    c.caption()

    # Incorrect geometry data type – a closed ring shape declared as a LineString.
    c = Cell(ax, 4, 0, "Incorrect geometry\ndata type")
    ring = rings("invalid_geometries/invalid_incorrect_geometry_data_type.geojson")[0]
    pts = c.polygon([ring], PINK, scale=0.78)[0]
    c.note('"type": "LineString"', y=pts[:, 1].min() - c.y - 0.75)
    c.caption()

    save(fig, "invalid_examples.png")


# --------------------------------------------------------------------------
# 2) Valid but problematic for some tools/APIs
# --------------------------------------------------------------------------
def valid_problematic():
    fig, ax = canvas(5, 3, (15.5, 11.0))

    # --- row 1 ---
    c = Cell(ax, 0, 0, "Has holes")
    c.polygon(rings("problematic_geometries/problematic_holes.geojson"), CYAN,
              scale=0.95)
    c.caption()

    # Self-intersection (small) – the crossing is a couple of pixels wide at the
    # top-left corner, so point at it.
    c = Cell(ax, 1, 0, "Self-intersection\n(small)")
    c.polygon(rings("problematic_geometries/problematic_self_intersection_small.geojson"),
              CRIMSON, scale=0.9)
    c.arrow((-4.5, 2.75), (-3.85, 1.62), lw=2.2)
    c.caption()

    c = Cell(ax, 2, 0, "Self-intersection\n(large)")
    c.polygon(rings("problematic_geometries/problematic_self_intersection_large.geojson"),
              TAN, scale=0.9)
    c.caption()

    # Inner and exterior rings cross – filling both rings as one compound path
    # would just paint the protruding part as a spike, so only the exterior is
    # filled, the hole is punched out (clipped to the exterior) and the inner
    # ring is stroked on top: outside the exterior it stays an open outline.
    c = Cell(ax, 3, 0, "Inner and exterior\nrings cross")
    ext, inner = c.place(
        rings("problematic_geometries/problematic_inner_and_exterior_ring_intersect.geojson"),
        scale=0.9,
    )
    ext_patch = PathPatch(MplPath(ext), facecolor=PINK, edgecolor="none", zorder=1)
    ax.add_patch(ext_patch)
    hole = PathPatch(MplPath(inner), facecolor="white", edgecolor="none", zorder=2)
    hole.set_clip_path(ext_patch)
    ax.add_patch(hole)
    ax.plot(inner[:, 0], inner[:, 1], color=EDGE, lw=1.6, zorder=3)
    ax.plot(ext[:, 0], ext[:, 1], color=EDGE, lw=1.6, zorder=4)
    c.caption()

    # Duplicate nodes – mark the repeated position.
    c = Cell(ax, 4, 0, "Duplicate nodes")
    ring = rings("problematic_geometries/problematic_duplicate_nodes.geojson")[0]
    pts = c.polygon([ring], DARKRED, scale=0.85)[0]
    ax.scatter(pts[[1, 2], 0], pts[[1, 2], 1], s=55, color=ACCENT, zorder=3)
    c.caption()

    # --- row 2 ---
    # Zero-length LineString – all positions identical, renders as one node.
    c = Cell(ax, 0, 1, "Zero-length\nLineString")
    ax.plot([c.x - 2.6, c.x + 2.6], [c.y, c.y], color=EDGE, lw=1.5,
            ls=(0, (3, 3)), alpha=0.4, zorder=1)
    ax.scatter([c.x], [c.y], s=320, color=TEAL, edgecolor=EDGE, lw=1.8, zorder=3)
    c.caption()

    # Excessive coordinate precision – the shape alone says nothing, so one of
    # its 14-decimal positions is spelled out next to the node it belongs to.
    c = Cell(ax, 1, 1, "Excessive coordinate\nprecision")
    precision_file = "problematic_geometries/problematic_excessive_coordinate_precision.geojson"
    pts = c.polygon(rings(precision_file), ORANGE, scale=0.62)[0]
    node = pts[0]
    ax.scatter(pts[:, 0], pts[:, 1], s=26, color=EDGE, zorder=3)
    ax.scatter([node[0]], [node[1]], s=70, color=ACCENT, zorder=4)
    lon, lat = positions(precision_file)[0][:2]
    c.note(f"{lon}, {lat}", y=node[1] - c.y - 0.6, size=10)
    c.caption()

    c = Cell(ax, 2, 1, "Excessive vertices")
    c.polygon(rings("problematic_geometries/problematic_excessive_vertices.geojson"),
              ACCENT, scale=0.85, lw=0.5)
    c.caption()

    # 3D / 4D – the extra values per position are the point, so show one.
    c = Cell(ax, 3, 1, "3D coordinates")
    file_3d = "problematic_geometries/problematic_3d_coordinates.geojson"
    c.polygon(rings(file_3d), PLUM, scale=0.7)
    c.note(str(positions(file_3d)[1]), size=11)
    c.caption()

    c = Cell(ax, 4, 1, "4D coordinates")
    file_4d = "problematic_geometries/problematic_4d_coordinates.geojson"
    c.polygon(rings(file_4d), BROWN, scale=0.7)
    c.note(str(positions(file_4d)[1]), size=11)
    c.caption()

    # --- row 3 ---
    # Outside lat/lon boundary – shown against the valid [-180,180]/[-90,90] box.
    # The shape is schematic, drawn to straddle the western edge of that box.
    c = Cell(ax, 0, 2, "Outside lat/lon\nboundary")
    world = np.array([[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]],
                     dtype=float)
    ring = np.array([[-262, -46], [-78, -58], [-70, 40], [-256, 50], [-262, -46]],
                    dtype=float)
    world_p, ring_p = c.place([world, ring], scale=0.85)
    wx0, wx1 = world_p[:, 0].min(), world_p[:, 0].max()
    wy0, wy1 = world_p[:, 1].min(), world_p[:, 1].max()
    ax.add_patch(Rectangle((wx0, wy0), wx1 - wx0, wy1 - wy0,
                           facecolor="none", edgecolor=EDGE, lw=1.3,
                           ls=(0, (4, 3)), alpha=0.55))
    ax.fill(ring_p[:, 0], ring_p[:, 1], color=SAND, alpha=0.95, zorder=2)
    ax.plot(ring_p[:, 0], ring_p[:, 1], color=EDGE, lw=1.6, zorder=2)
    # Without ticks the dashed box is just a box – name the edge the polygon
    # crosses, and say what the box is.
    for x, lon in ((wx0, "-180°"), (wx1, "180°")):
        ax.text(x, wy0 - 0.2, lon, ha="center", va="top", fontsize=10.5,
                fontweight="bold", fontname=FONT, color=EDGE, alpha=0.7)
    c.note("valid lon/lat range", y=wy0 - c.y - 1.2, size=11, color=EDGE)
    c.caption()

    # Crosses anti-meridian.
    c = Cell(ax, 1, 2, "Crosses\nanti-meridian")
    # The example is a rectangle spanning lon 177.9 -> -179.8, i.e. over the 180th
    # meridian; drawn here as a box straddling the dashed meridian line.
    ring = np.array([[-2.0, -1.0], [2.0, -1.0], [2.0, 1.0], [-2.0, 1.0], [-2.0, -1.0]])
    pts = c.place([ring], scale=0.75)[0]
    ax.fill(pts[:, 0], pts[:, 1], color=LIME, zorder=2)
    ax.plot(pts[:, 0], pts[:, 1], color=EDGE, lw=1.6, zorder=2)
    ax.plot([c.x, c.x], [c.y - 2.4, c.y + 2.4], color=ACCENT, lw=2.0,
            ls=(0, (4, 3)), zorder=3)
    ax.text(c.x, c.y + 2.6, "180°", ha="center", va="bottom", fontsize=12,
            fontweight="bold", fontname=FONT, color=ACCENT)
    c.caption()

    # Wrong bbox coordinate order – draw the bbox around the geometry and name
    # the order it was written in; the example has [south, west, north, east].
    c = Cell(ax, 2, 2, "Wrong bbox\ncoordinate order")
    pts = c.polygon(rings("problematic_geometries/problematic_wrong_bbox_coordinate_order.geojson"),
                    LIME, scale=0.62)[0]
    x0, x1 = pts[:, 0].min(), pts[:, 0].max()
    y0, y1 = pts[:, 1].min(), pts[:, 1].max()
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none",
                           edgecolor=ACCENT, lw=1.7, ls=(0, (4, 3)), zorder=3))
    for label, (lx, ly, ha, va) in {
        "north": (c.x, y1 + 0.18, "center", "bottom"),
        "west": (x0 - 0.25, c.y, "right", "center"),
        "south": (c.x, y0 - 0.18, "center", "top"),
        "east": (x1 + 0.25, c.y, "left", "center"),
    }.items():
        ax.text(lx, ly, label, ha=ha, va=va, fontsize=10.5, fontweight="bold",
                fontname=FONT, color=ACCENT)
    c.note("bbox: [south, west, north, east]", size=11)
    c.caption()

    # Multitype with one part – a lone Polygon that is declared a MultiPolygon.
    c = Cell(ax, 3, 2, "Multitype with just\none geometry")
    c.polygon(rings("problematic_geometries/problematic_multitype_geometry_with_just_one_geometry.geojson"),
              STEEL, scale=0.7)
    c.note('"type": "MultiPolygon"', size=11)
    c.caption()

    save(fig, "valid_problematic.png")


if __name__ == "__main__":
    invalid_examples()
    valid_problematic()
