import cadquery as cq
import math

# All dimensions in mm
W = 20.0   # width (X direction)
H = 20.0   # height of vertical plate (Z direction)
D = 10.0   # depth of horizontal leg (Y direction)
T = 2.5    # material thickness

hole_r = 1.5    # 3mm drill radius
csk_r = 3.0     # 6mm countersink radius
csk_angle = 120  # included angle in degrees
# Countersink depth from half-angle geometry
csk_depth = (csk_r - hole_r) / math.tan(math.radians(csk_angle / 2))

# Build L-bracket: profile in YZ plane, extrude W along X
# Profile (Y=depth axis, Z=height axis):
#   (0,0) front-bottom → (D,0) back-bottom of horiz leg
#   → (D,T) back-top of horiz leg → (T,T) inner corner
#   → (T,H) inner top of vert plate → (0,H) front-top → close
bracket = (
    cq.Workplane("YZ")
    .polyline([(0, 0), (D, 0), (D, T), (T, T), (T, H), (0, H)])
    .close()
    .extrude(W)
)


def make_csk_cutter(cx, cy, cz, axis, depth, hole_r, csk_r, csk_depth):
    """
    Create a countersunk hole cutter as a unioned solid.
    axis: 'X', 'Y', or 'Z' — direction of drilling (inward)
    csk is on the entry face (opposite to drill direction).
    """
    # Through-hole cylinder
    if axis == 'Y':
        plane = "XZ"
        through = (cq.Workplane(plane)
                   .transformed(offset=cq.Vector(cx, cz, 0))
                   .circle(hole_r)
                   .extrude(depth))
        # Countersink frustum at Y=cy (entry face), expanding outward
        csk = (cq.Workplane(plane)
               .transformed(offset=cq.Vector(cx, cz, 0))
               .workplane(offset=-csk_depth)
               .circle(csk_r)
               .workplane(offset=csk_depth)
               .circle(hole_r)
               .loft())
        # The through cylinder starts at Y=cy and goes to Y=cy+depth
        # Shift to correct absolute position
        through = through.translate((0, cy, 0))
        csk = csk.translate((0, cy, 0))
    elif axis == 'Z':
        plane = "XY"
        # Drill from cz downward by depth
        through = (cq.Workplane(plane)
                   .transformed(offset=cq.Vector(cx, cy, cz))
                   .circle(hole_r)
                   .extrude(depth, both=False))
        through = through.translate((0, 0, -depth))
        # Countersink at cz (top), frustum from csk_r at cz to hole_r at cz-csk_depth
        csk = (cq.Workplane(plane)
               .transformed(offset=cq.Vector(cx, cy, cz - csk_depth))
               .circle(hole_r)
               .workplane(offset=csk_depth)
               .circle(csk_r)
               .loft())
    return through.union(csk)


# ── Vertical plate holes ──────────────────────────────────────────────────────
# Drilled in +Y direction (from front face Y=0 inward through thickness T)
# Hole 1: upper, centered at (X=W/2, Y=0..T, Z=H-5=15)
# Hole 2: lower, centered at (X=W/2, Y=0..T, Z=5)
for z_center in [H - 5.0, 5.0]:
    origin = cq.Vector(W / 2, 0, z_center)
    drill_dir = cq.Vector(0, 1, 0)  # +Y: front face → back face
    # Through-hole cylinder Y=0..T
    through_cyl = cq.CQ(cq.Solid.makeCylinder(hole_r, T, pnt=origin, dir=drill_dir))
    # Countersink frustum: large (csk_r) at Y=0, narrows to hole_r at Y=csk_depth
    csk_frustum = cq.CQ(cq.Solid.makeCone(csk_r, hole_r, csk_depth,
                                           pnt=origin, dir=drill_dir))
    bracket = bracket.cut(through_cyl).cut(csk_frustum)

# ── Horizontal plate hole ─────────────────────────────────────────────────────
# Drilled in -Z direction from top face Z=T, centered at (X=W/2, Y=D/2)
cx, cy = W / 2, D / 2
# Through cylinder from Z=T down to Z=0
through_cyl = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cx, cy, 0))
    .circle(hole_r)
    .extrude(T)
)
# Countersink at Z=T (top face): large radius at Z=T, small at Z=T-csk_depth
csk_frustum = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cx, cy, T - csk_depth))
    .circle(hole_r)
    .workplane(offset=csk_depth)
    .circle(csk_r)
    .loft()
)
bracket = bracket.cut(through_cyl).cut(csk_frustum)

# ── Export ────────────────────────────────────────────────────────────────────
cq.exporters.export(bracket, "part.stl")
print("Exported part.stl")

# ── Validation renders ────────────────────────────────────────────────────────
import cadquery_png_plugin.plugin  # noqa: registers plugin

assy = cq.Assembly(bracket, color=cq.Color(0.8, 0.8, 0.9))
for view in ["front-top-right", "front", "top", "right", "front-bottom-left"]:
    assy.exportPNG(
        options={"width": 800, "height": 800, "color_theme": "default",
                 "view": view, "zoom": 1.1},
        file_path=f"part_{view}.png",
    )
    print(f"Rendered part_{view}.png")

print("Done.")
