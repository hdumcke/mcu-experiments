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
screw_hole = 2.3
screw_pos_y = outer_length / 2 - screw_support_plate
screw_pos_x = outer_width / 2 + 2 * screw_hole

# %%
importer = Mesher()
cover_import = importer.read("Parkside_Battery_holder_4928652/files/adapter_cover.stl")[0]
with BuildPart() as plate:
    add(cover_import)
    with BuildSketch(plate.faces().sort_by(Axis.Z)[-1]) as plate_sk:
        Rectangle(outer_width + 2 * wall_thickness, outer_length)
        Rectangle(outer_width + 2 * wall_thickness, outer_length - 28.0, mode=Mode.SUBTRACT)
        with Locations((-65.0, 0.0)):
            Rectangle(90.0, outer_length - 28.0)
        fillet(plate_sk.vertices(), radius=2)
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
        with Locations((-105.0, 0.0)):
            Circle(screw_hole, mode=Mode.SUBTRACT)
        with Locations((-27.0, 0.0)):
            Rectangle(5.0, 5.0, mode=Mode.SUBTRACT)
    extrude(amount=-wall_thickness)
show(plate)
# %%
plate.part.export_stl('cover.stl')
