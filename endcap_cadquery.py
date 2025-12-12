#!/usr/bin/env python3
# Endcaps for binoculars

import cadquery as cq
from cadquery.vis import show

base_height = 1
wall = 2
diam = 27.2
height = 5

result = (
    cq.Workplane('front')
    .circle((diam + wall)/2).extrude(base_height)
    .workplane().circle((diam + wall)/2).circle(diam/2).extrude(height)
)

# Render the solid
show(result)
cq.exporters.export(result, 'endcap_cadquery.stl')