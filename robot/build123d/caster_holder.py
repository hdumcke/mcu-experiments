from build123d import *

outer_radius = 16.0 / 2
inner_radius = 13.0 / 2
hight = 20.6

screw_support_plate = 3.0
screw_hole = 2.0

with BuildPart() as holder:
    with BuildSketch() as holder_sk:
        Circle(outer_radius)
        Circle(inner_radius, mode=Mode.SUBTRACT)
    extrude(amount=hight)
    with BuildSketch(holder.faces().sort_by().first) as inner_sk:
        Circle(outer_radius)
        Circle(screw_hole, mode=Mode.SUBTRACT)
    extrude(amount=-screw_support_plate)

#holder.part.export_stl('caster-holder.stl')
