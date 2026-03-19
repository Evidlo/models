# STL Generation from Drawing

@drawing.png contains a hand-drawn schematic of a part meant to be 3D printed.

- gray lines are dimension lines or text notes
- red lines represent drill locations
- black lines are the boundaries of the solid part

Use the various views of the part in the drawing to generate @part.py using Cadquery.  Output the final result to @part.stl

Validate your result by either inspecting the part programmatically, or by inspecting a png from different angles

Example Cadquery png plugin
``` python
import cadquery as cq
import cadquery_png_plugin.plugin  # This registers the plugin with CadQuery

# You can customize the render options through a dictionary
render_options = {"width": 600,  # width of the output image
                  "height": 600,  # height of the output image
                  "color_theme": "default",  # can also be black_and_white
                  "view": "front-top-right",  # front, top, front-bottom-left, etc
                  "zoom": 1.0  # zooms in and out on the center of the model
                  }

# Create a simple CadQuery assembly for an example export
box = cq.Workplane().box(10, 10, 10)
cyl = cq.Workplane().circle(2.5).extrude(5)
assy = cq.Assembly(box, color=cq.Color(1.0, 0.0, 0.0))
# assy.add(box, color=cq.Color(1.0, 0.0, 0.0))
assy.add(cyl, loc=cq.Location(0, 0, 5.0), color=cq.Color(0.0, 0.0, 1.0))

# Do the PNG export
assy.exportPNG(options=render_options, file_path="ouptput_file.png")
```

