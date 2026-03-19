import cadquery as cq
import cadquery.selectors as sel
import math

# All dimensions in mm
W = 20.0   # width (X direction)
H = 20.0   # height of vertical plate (Z direction)
D = 10.0   # depth of horizontal leg (Y direction)
T = 2.5    # material thickness

hole_d = 3.0    # drill hole diameter
csk_d = 6.0     # countersink outer diameter
csk_angle = 120  # included angle in degrees

# Build L-bracket profile in YZ plane (Y=depth, Z=height), extrude W along X
# Profile corners: bottom-front → bottom-back → top-back of horiz leg →
#                  inner corner → top of vert plate (inner) → top-front
bracket = (
    cq.Workplane("YZ")
    .polyline([(0, 0), (D, 0), (D, T), (T, T), (T, H), (0, H)])
    .close()
    .extrude(W)
)

# Two countersunk holes in vertical plate (front face at Y=0)
# Face centroid is at (X=W/2=10, Z=H/2=10)
# Upper hole at Z=15mm (5mm from top):  local offset (0, +5)
# Lower hole at Z=5mm  (5mm from bottom): local offset (0, -5)
bracket = (
    bracket
    .faces("<Y")
    .workplane()
    .pushPoints([(0, 5), (0, -5)])
    .cskHole(hole_d, csk_d, csk_angle)
)

# One countersunk hole in horizontal plate (top face at Z=T=2.5)
# The exposed top surface spans Y=T..D, centroid at (X=10, Y=6.25)
# Place hole centered in the leg at Y=D/2=5, so offset (0, -1.25)
bracket = (
    bracket
    .faces(sel.NearestToPointSelector((W / 2, (T + D) / 2, T)))
    .workplane()
    .center(0, -1.25)
    .cskHole(hole_d, csk_d, csk_angle)
)

# Export STL
cq.exporters.export(bracket, "part.stl")
print("Exported part.stl")

# Render validation PNGs from multiple angles
import cadquery_png_plugin.plugin  # noqa: registers plugin

assy = cq.Assembly(bracket, color=cq.Color(0.8, 0.8, 0.9))

for view in ["front-top-right", "front", "top", "right"]:
    assy.exportPNG(
        options={"width": 800, "height": 800, "color_theme": "default",
                 "view": view, "zoom": 1.2},
        file_path=f"part_{view}.png",
    )
    print(f"Rendered part_{view}.png")

print("Done.")
