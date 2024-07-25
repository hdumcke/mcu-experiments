# %%
from build123d import *
from ocp_vscode import *

# %%
outer_length = 65.0
outer_width = 10.0
hight = 12.0
wall_thickness = 4.0
slot_length = 18.0

screw_support_plate = 5.0
screw_hole = 2.0
screw_pos_x = outer_length / 2 - screw_support_plate
screw_pos_y = outer_width / 2 + 2 * screw_hole

# %%
with BuildPart() as holder:
    with BuildSketch() as holder_sk:
        Rectangle(outer_length, outer_width + 2 * wall_thickness)
        fillet(holder_sk.vertices(), radius=2)
        with Locations((screw_pos_x, screw_pos_y)):
            Circle(screw_support_plate)
            Circle(screw_hole, mode=Mode.SUBTRACT)
        with Locations((screw_pos_x, -screw_pos_y)):
            Circle(screw_support_plate)
            Circle(screw_hole, mode=Mode.SUBTRACT)
        with Locations((-screw_pos_x, screw_pos_y)):
            Circle(screw_support_plate)
            Circle(screw_hole, mode=Mode.SUBTRACT)
        with Locations((-screw_pos_x, -screw_pos_y)):
            Circle(screw_support_plate)
            Circle(screw_hole, mode=Mode.SUBTRACT)
    extrude(amount=hight + wall_thickness)
    with BuildSketch(holder.faces().sort_by().last) as slot_sk:
        Rectangle(outer_length, outer_width)
        Rectangle(slot_length, outer_width + 2 * wall_thickness)
    extrude(amount=-hight, mode=Mode.SUBTRACT)
    with BuildSketch() as holder_sk:
        with Locations((0.0, (outer_width + wall_thickness) / 2)):
            Rectangle(slot_length, wall_thickness)
    extrude(amount=hight + wall_thickness)
show(holder)
# %%
holder.part.export_stl('motor-holder.stl')