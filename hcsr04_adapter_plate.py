import FreeCAD as App
import Part

# ============================================================
# HC-SR04 MOUNTING ADAPTER PLATE
# Units: millimeters
# ============================================================

PLATE_WIDTH = 49.0
PLATE_HEIGHT = 27.0
PLATE_THICKNESS = 4.0

# HC-SR04 mounting pattern
HOLE_SPACING_X = 40.0
HOLE_SPACING_Y = 15.0

# M3 clearance
HOLE_DIAMETER = 3.4

# Small edge rounding
EDGE_RADIUS = 1.0

OUTPUT_FCSTD = "hcsr04_adapter_plate.FCStd"
OUTPUT_STEP = "hcsr04_adapter_plate.step"


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("HC_SR04_Adapter_Plate")
except:
    pass

doc = App.newDocument("HC_SR04_Adapter_Plate")


# ============================================================
# CREATE PLATE
# ============================================================

plate = Part.makeBox(
    PLATE_WIDTH,
    PLATE_THICKNESS,
    PLATE_HEIGHT
)


# ============================================================
# SENSOR HOLES
# ============================================================

center_x = PLATE_WIDTH / 2.0
center_z = PLATE_HEIGHT / 2.0

hole_x1 = center_x - HOLE_SPACING_X / 2.0
hole_x2 = center_x + HOLE_SPACING_X / 2.0

hole_z1 = center_z - HOLE_SPACING_Y / 2.0
hole_z2 = center_z + HOLE_SPACING_Y / 2.0

holes = [
    (hole_x1, hole_z1),
    (hole_x2, hole_z1),
    (hole_x1, hole_z2),
    (hole_x2, hole_z2)
]

for x, z in holes:

    cutter = Part.makeCylinder(
        HOLE_DIAMETER / 2.0,
        PLATE_THICKNESS + 2.0,
        App.Vector(x, -1, z),
        App.Vector(0, 1, 0)
    )

    plate = plate.cut(cutter)


# ============================================================
# CREATE FREECAD OBJECT
# ============================================================

obj = doc.addObject(
    "PartDesign::Feature",
    "HCSR04_Adapter_Plate"
)

obj.Label = "HC-SR04 M3 Adapter Plate"
obj.Shape = plate


# ============================================================
# DIMENSION PROPERTIES
# ============================================================

obj.addProperty(
    "App::PropertyLength",
    "PlateWidth",
    "Dimensions"
)
obj.PlateWidth = PLATE_WIDTH

obj.addProperty(
    "App::PropertyLength",
    "PlateHeight",
    "Dimensions"
)
obj.PlateHeight = PLATE_HEIGHT

obj.addProperty(
    "App::PropertyLength",
    "PlateThickness",
    "Dimensions"
)
obj.PlateThickness = PLATE_THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "HoleSpacingX",
    "HC-SR04"
)
obj.HoleSpacingX = HOLE_SPACING_X

obj.addProperty(
    "App::PropertyLength",
    "HoleSpacingY",
    "HC-SR04"
)
obj.HoleSpacingY = HOLE_SPACING_Y

obj.addProperty(
    "App::PropertyLength",
    "HoleDiameter",
    "Mounting"
)
obj.HoleDiameter = HOLE_DIAMETER


# ============================================================
# VISUAL SETTINGS
# ============================================================

obj.ViewObject.ShapeColor = (0.25, 0.65, 0.90)
obj.ViewObject.LineColor = (0.10, 0.10, 0.10)


# ============================================================
# SAVE
# ============================================================

doc.recompute()

doc.saveAs(OUTPUT_FCSTD)

Part.export(
    [obj],
    OUTPUT_STEP
)

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()

print("")
print("======================================")
print("HC-SR04 ADAPTER PLATE CREATED")
print("======================================")
print("Plate: %.1f x %.1f x %.1f mm"
      % (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS))
print("Hole spacing: %.1f x %.1f mm"
      % (HOLE_SPACING_X, HOLE_SPACING_Y))
print("Hole diameter: %.1f mm (M3 clearance)"
      % HOLE_DIAMETER)
print("")
print("Created:")
print(OUTPUT_FCSTD)
print(OUTPUT_STEP)
print("======================================")

