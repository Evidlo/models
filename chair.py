#!/usr/bin/env python3
# Endcaps for binoculars

import cadquery as cq
from cadquery.vis import show


result = (
    cq.Workplane('front')
    .circle(15).extrude(50)
    .faces(">Z")
    .circle(25).extrude(10)
    .faces(">Z")
    .circle(20).extrude(50)
    .faces(">Z")
    .fillet(10)
)

# Render the solid
show(result)
cq.exporters.export(result, 'chair.stl')
cq.exporters.export(result, 'chair.step')