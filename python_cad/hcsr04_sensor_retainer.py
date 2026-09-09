import FreeCAD as App
import Part

# ============================================================
# HC-SR04 RETAINER FOR EXISTING L-BRACKET
# Units: mm
# ============================================================

# ---------- RETAINER ----------
RETAINER_WIDTH = 49.0
RETAINER_HEIGHT = 12.0
RETAINER_THICKNESS = 4.0

# Approximate HC-SR04 mounting-hole spacing
HOLE_SPACING = 45.0

# M3 clearance
HOLE_DIAMETER = 3.4

# Slot adjustment
SLOT_LENGTH = 2.0

# Small corner radius
CORNER_RADIUS = 1.0

# Output filenames
OUTPUT_FCSTD = "hcsr04_sensor_retainer.FCStd"
OUTPUT_STEP = "hcsr04_sensor_retainer.step"


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("HC_SR04_Sensor_Retainer")
except:
    pass

doc = App.newDocument("HC_SR04_Sensor_Retainer")


# ============================================================
# CREATE RETAINER
# ============================================================

plate = Part.makeBox(
    RETAINER_WIDTH,
    RETAINER_THICKNESS,
    RETAINER_HEIGHT
)


# ============================================================
# CREATE TWO SLOTTED M3 HOLES
# ============================================================

center_x = RETAINER_WIDTH / 2.0
center_z = RETAINER_HEIGHT / 2.0

left_x = center_x - HOLE_SPACING / 2.0
right_x = center_x + HOLE_SPACING / 2.0


def make_slot(x, z):
    """
    Creates a horizontal slot with M3 clearance.
    Slot length is added to the nominal hole diameter.
    """

    radius = HOLE_DIAMETER / 2.0

    # Half of additional slot travel
    travel = SLOT_LENGTH / 2.0

    # Center cylinders
    c1 = Part.makeCylinder(
        radius,
        RETAINER_THICKNESS + 2,
        App.Vector(x - travel, -1, z),
        App.Vector(0, 1, 0)
    )

    c2 = Part.makeCylinder(
        radius,
        RETAINER_THICKNESS + 2,
        App.Vector(x + travel, -1, z),
        App.Vector(0, 1, 0)
    )

    # Connecting rectangular section
    box = Part.makeBox(
        SLOT_LENGTH,
        RETAINER_THICKNESS + 2,
        HOLE_DIAMETER,
        App.Vector(x - travel, -1, z - radius)
    )

    return c1.fuse(c2).fuse(box)


# Cut left and right mounting slots
plate = plate.cut(
    make_slot(left_x, center_z)
)

plate = plate.cut(
    make_slot(right_x, center_z)
)


# ============================================================
# ADD SMALL TOP LIP
# ============================================================

# This lip sits against the top edge of the HC-SR04
# and helps prevent the board from shifting when the servo moves.

LIP_HEIGHT = 3.0
LIP_DEPTH = 2.0

lip = Part.makeBox(
    RETAINER_WIDTH,
    LIP_DEPTH,
    LIP_HEIGHT
)

lip.translate(
    App.Vector(
        0,
        RETAINER_THICKNESS,
        RETAINER_HEIGHT - LIP_HEIGHT
    )
)

plate = plate.fuse(lip)


# ============================================================
# CREATE FREECAD OBJECT
# ============================================================

obj = doc.addObject(
    "PartDesign::Feature",
    "HCSR04_Sensor_Retainer"
)

obj.Label = "HC-SR04 Sensor Retainer"
obj.Shape = plate


# ============================================================
# DIMENSION PROPERTIES
# ============================================================

obj.addProperty(
    "App::PropertyLength",
    "RetainerWidth",
    "Dimensions"
)
obj.RetainerWidth = RETAINER_WIDTH

obj.addProperty(
    "App::PropertyLength",
    "RetainerHeight",
    "Dimensions"
)
obj.RetainerHeight = RETAINER_HEIGHT

obj.addProperty(
    "App::PropertyLength",
    "RetainerThickness",
    "Dimensions"
)
obj.RetainerThickness = RETAINER_THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "HoleSpacing",
    "Mounting"
)
obj.HoleSpacing = HOLE_SPACING

obj.addProperty(
    "App::PropertyLength",
    "HoleDiameter",
    "Mounting"
)
obj.HoleDiameter = HOLE_DIAMETER

obj.addProperty(
    "App::PropertyLength",
    "SlotAdjustment",
    "Mounting"
)
obj.SlotAdjustment = SLOT_LENGTH


# ============================================================
# VISUAL SETTINGS
# ============================================================

obj.ViewObject.ShapeColor = (0.30, 0.70, 0.90)
obj.ViewObject.LineColor = (0.10, 0.10, 0.10)


# ============================================================
# SAVE FREECAD FILE
# ============================================================

doc.recompute()

doc.saveAs(OUTPUT_FCSTD)

# Export STEP
Part.export(
    [obj],
    OUTPUT_STEP
)


# ============================================================
# DISPLAY
# ============================================================

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()


print("")
print("==============================================")
print("HC-SR04 SENSOR RETAINER CREATED")
print("==============================================")
print("")
print("Retainer:")
print("%.1f x %.1f x %.1f mm"
      % (
          RETAINER_WIDTH,
          RETAINER_HEIGHT,
          RETAINER_THICKNESS
      ))

print("")
print("Mounting hole spacing: %.1f mm" % HOLE_SPACING)
print("Hole diameter: %.1f mm (M3 clearance)" % HOLE_DIAMETER)
print("Slot adjustment: %.1f mm" % SLOT_LENGTH)

print("")
print("Created files:")
print(OUTPUT_FCSTD)
print(OUTPUT_STEP)

print("")
print("Use two M3 screws to secure the retainer.")
print("==============================================")

