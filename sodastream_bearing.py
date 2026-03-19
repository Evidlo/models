#!/usr/bin/env python3
# Endcaps for binoculars

import cadquery as cq
# Evan Widoski - 2025-12-12
# pillow block bearing for sodastream internals

from cadquery.vis import show

width = 20
height = 14
depth = 5
diam = 9


base = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(depth)
)

cutout = (
    cq.Workplane("XY")
    .center(0, diam/2-height/2 + 4)
    .circle(diam / 2)
    .extrude(depth)
)

result = base.cut(cutout)

# Render the solid
show(result)
cq.exporters.export(result, 'sodastream_bearing.stl')