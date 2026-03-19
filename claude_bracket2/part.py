import cadquery as cq
import cadquery_png_plugin.plugin

# ─── Dimensions ───────────────────────────────────────────────────────────────
W    = 20    # total width  (X), mm
D    = 20    # total depth  (Y), mm
H    = 20    # total height (Z), mm
arm  = 10    # arm width,        mm

# ─── Hole parameters ──────────────────────────────────────────────────────────
hole_d   = 3.0   # drill diameter,        mm
csk_d    = 6.0   # countersink diameter,  mm
csk_ang  = 120   # countersink included angle, degrees

# ─── Base L-shape ─────────────────────────────────────────────────────────────
# Cross-section in X-Y plane, extruded in +Z.
# Notch removed from the "back-right" quadrant: X∈[arm,W], Y∈[arm,D]
#
#   Y
#   ↑
#   D ┌────┐
#     │    │  ← left column only (X:0..arm, Y:arm..D)
#  arm├────┼──────────┐
#     │               │  ← bottom row (X:0..W, Y:0..arm)
#   0 └───────────────┘
#     0   arm         W → X

bracket = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(W,   0)
    .lineTo(W,   arm)
    .lineTo(arm, arm)
    .lineTo(arm, D)
    .lineTo(0,   D)
    .close()
    .extrude(H)
)

# ─── Front-face holes (Y=0 face, drilled in +Y direction) ────────────────────
# Both visible as circles in the front view; countersinks on outside (front) face.
# Positions centred in the left column arm (X=arm/2=5), at Z=5 and Z=15.
#
# CadQuery's "<Y" face workplane: origin at bbox centre of face = (W/2, 0, H/2)
# = (10, 0, 10).  pushPoints offsets are (local_x, local_z) → (ΔX, ΔZ).
bracket = (
    bracket
    .faces("<Y")                        # front face at Y=0
    .workplane()
    .pushPoints([(-5, 5), (-5, -5)])    # (5,15) and (5,5) in world X,Z
    .cskHole(hole_d, csk_d, csk_ang)   # through-hole + countersink on this face
)

# ─── Right-face hole (X=W face, drilled in -X direction) ─────────────────────
# Visible as circle in the right view; countersink on outside (right) face.
# Centred in the right arm: Y = arm/2 = 5,  Z = H/2 = 10.
#
# ">X" face workplane origin at bbox centre = (W, arm/2, H/2) = (20, 5, 10).
# The right-arm face spans Y:[0,arm] × Z:[0,H].  Centre is already (5,10).
bracket = (
    bracket
    .faces(">X")                        # right face at X=W
    .workplane()
    .pushPoints([(0, 0)])               # already at face centre
    .cskHole(hole_d, csk_d, csk_ang)
)

# ─── Export STL ───────────────────────────────────────────────────────────────
cq.exporters.export(bracket, "part.stl")
print("Exported part.stl")

# ─── Validation renders ───────────────────────────────────────────────────────
assy = cq.Assembly()
assy.add(bracket, color=cq.Color(0.6, 0.7, 0.9))

for view in ("front", "front-top-right", "front-bottom-left", "top", "right"):
    opts = {
        "width": 600, "height": 600,
        "color_theme": "default",
        "view": view,
        "zoom": 1.2,
    }
    assy.exportPNG(options=opts, file_path=f"part_{view}.png")
    print(f"Rendered part_{view}.png")
