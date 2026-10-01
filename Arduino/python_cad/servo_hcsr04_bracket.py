import FreeCAD as App
import Part
import math

# ============================================================
# HC-SR04 / SERVO L-BRACKET
# All dimensions are in millimeters
# ============================================================

# ---------- MAIN BRACKET ----------
BRACKET_WIDTH       = 49.0     # left-right width of sensor plate
VERTICAL_HEIGHT     = 27.0     # height of vertical plate
BASE_DEPTH          = 30.0     # distance from vertical plate to front
THICKNESS            = 4.0

# ---------- HC-SR04 ----------
# Common HC-SR04 board is approximately 45 x 20 mm
SENSOR_HOLE_SPACING_X = 40.0
SENSOR_HOLE_SPACING_Y = 15.0
SENSOR_HOLE_DIAMETER  = 2.6

# Distance from bottom edge of vertical plate to lower
# row of sensor mounting holes
SENSOR_HOLE_BOTTOM = 6.0

# ---------- SERVO HORN ----------
# Your servo arm is approximately 34 mm long x 4 mm wide
SERVO_HORN_LENGTH = 34.0
SERVO_HORN_WIDTH  = 4.0

SERVO_CENTER_HOLE_DIAMETER = 3.2
SERVO_HOLE_DIAMETER        = 2.2

# Hole spacing along servo horn.
# The first small hole is 5 mm from the center,
# followed by 5 mm increments.
SERVO_HOLE_POSITIONS = [-15, -10, -5, 5, 10, 15]

# ---------- GUSSETS ----------
GUSSET_HEIGHT = 16.0
GUSSET_LENGTH = 18.0
GUSSET_THICKNESS = 4.0

# ---------- OUTPUT ----------
OUTPUT_FCSTD = "servo_hcsr04_L_bracket.FCStd"
OUTPUT_STEP  = "servo_hcsr04_L_bracket.step"


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("HC_SR04_Servo_L_Bracket")
except:
    pass

doc = App.newDocument("HC_SR04_Servo_L_Bracket")


# ============================================================
# VERTICAL SENSOR PLATE
# ============================================================

vertical = Part.makeBox(
    BRACKET_WIDTH,
    THICKNESS,
    VERTICAL_HEIGHT
)

# Put vertical plate at Y=0.
# X = left/right
# Y = front/back
# Z = vertical


# ============================================================
# BASE PLATE
# ============================================================

base = Part.makeBox(
    BRACKET_WIDTH,
    BASE_DEPTH,
    THICKNESS
)

# Base begins at Y=0.
# Vertical plate occupies Y=0 to THICKNESS.


# ============================================================
# JOIN THE TWO PLATES
# ============================================================

bracket = vertical.fuse(base)


# ============================================================
# HC-SR04 MOUNTING HOLES
# ============================================================

sensor_center_x = BRACKET_WIDTH / 2.0

left_x  = sensor_center_x - SENSOR_HOLE_SPACING_X / 2.0
right_x = sensor_center_x + SENSOR_HOLE_SPACING_X / 2.0

bottom_z = SENSOR_HOLE_BOTTOM
top_z    = bottom_z + SENSOR_HOLE_SPACING_Y

sensor_hole_locations = [
    (left_x, bottom_z),
    (right_x, bottom_z),
    (left_x, top_z),
    (right_x, top_z)
]

for x, z in sensor_hole_locations:

    # Cylinder through vertical plate
    hole = Part.makeCylinder(
        SENSOR_HOLE_DIAMETER / 2.0,
        THICKNESS + 2,
        App.Vector(x, -1, z),
        App.Vector(0, 1, 0)
    )

    bracket = bracket.cut(hole)


# ============================================================
# SERVO HORN MOUNTING HOLES
# ============================================================

# Servo horn runs along X direction on the base.
servo_center_x = BRACKET_WIDTH / 2.0
servo_center_y = BASE_DEPTH / 2.0

# Central servo screw
center_hole = Part.makeCylinder(
    SERVO_CENTER_HOLE_DIAMETER / 2.0,
    THICKNESS + 2,
    App.Vector(servo_center_x, servo_center_y, -1),
    App.Vector(0, 0, 1)
)

bracket = bracket.cut(center_hole)


# Small holes along servo arm
for offset in SERVO_HOLE_POSITIONS:

    x = servo_center_x + offset

    # Keep holes inside bracket
    if x > 2 and x < BRACKET_WIDTH - 2:

        hole = Part.makeCylinder(
            SERVO_HOLE_DIAMETER / 2.0,
            THICKNESS + 2,
            App.Vector(x, servo_center_y, -1),
            App.Vector(0, 0, 1)
        )

        bracket = bracket.cut(hole)


# ============================================================
# OPTIONAL SERVO HORN RECESS
# ============================================================

# This shallow recess lets the 34 x 4 mm servo arm sit
# more securely on the base.

RECESS_DEPTH = 1.0

recess = Part.makeBox(
    SERVO_HORN_LENGTH,
    SERVO_HORN_WIDTH,
    RECESS_DEPTH
)

recess_x = servo_center_x - SERVO_HORN_LENGTH / 2.0
recess_y = servo_center_y - SERVO_HORN_WIDTH / 2.0

recess.translate(
    App.Vector(recess_x, recess_y, THICKNESS - RECESS_DEPTH)
)

# NOTE:
# Recess is intentionally NOT cut by default.
# This keeps the bracket stronger and allows different
# servo horns to sit on top of it.


# ============================================================
# GUSSETS
# ============================================================

# Create triangular side supports on both sides.

def make_gusset(x_position):

    # Triangle in Y-Z plane
    p1 = App.Vector(x_position, THICKNESS, THICKNESS)
    p2 = App.Vector(
        x_position,
        THICKNESS + GUSSET_LENGTH,
        THICKNESS
    )
    p3 = App.Vector(
        x_position,
        THICKNESS,
        THICKNESS + GUSSET_HEIGHT
    )

    wire = Part.makePolygon([p1, p2, p3, p1])
    face = Part.Face(wire)

    return face.extrude(
        App.Vector(GUSSET_THICKNESS, 0, 0)
    )


left_gusset = make_gusset(0)

right_gusset = make_gusset(
    BRACKET_WIDTH - GUSSET_THICKNESS
)

bracket = bracket.fuse(left_gusset)
bracket = bracket.fuse(right_gusset)


# ============================================================
# CREATE MAIN OBJECT
# ============================================================

obj = doc.addObject("PartDesign::Feature", "L_Bracket")
obj.Label = "HC-SR04 Servo L-Bracket"
obj.Shape = bracket


# ============================================================
# ADD DIMENSION INFORMATION
# ============================================================

obj.addProperty(
    "App::PropertyString",
    "Description",
    "Dimensions"
)

obj.Description = "HC-SR04 ultrasonic sensor servo L-bracket"

obj.addProperty(
    "App::PropertyLength",
    "BracketWidth",
    "Dimensions"
)
obj.BracketWidth = BRACKET_WIDTH

obj.addProperty(
    "App::PropertyLength",
    "VerticalHeight",
    "Dimensions"
)
obj.VerticalHeight = VERTICAL_HEIGHT

obj.addProperty(
    "App::PropertyLength",
    "BaseDepth",
    "Dimensions"
)
obj.BaseDepth = BASE_DEPTH

obj.addProperty(
    "App::PropertyLength",
    "Thickness",
    "Dimensions"
)
obj.Thickness = THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "SensorHoleSpacingX",
    "HC-SR04"
)
obj.SensorHoleSpacingX = SENSOR_HOLE_SPACING_X

obj.addProperty(
    "App::PropertyLength",
    "SensorHoleSpacingY",
    "HC-SR04"
)
obj.SensorHoleSpacingY = SENSOR_HOLE_SPACING_Y

obj.addProperty(
    "App::PropertyLength",
    "SensorHoleDiameter",
    "HC-SR04"
)
obj.SensorHoleDiameter = SENSOR_HOLE_DIAMETER

obj.addProperty(
    "App::PropertyLength",
    "ServoHornLength",
    "Servo"
)
obj.ServoHornLength = SERVO_HORN_LENGTH

obj.addProperty(
    "App::PropertyLength",
    "ServoHornWidth",
    "Servo"
)
obj.ServoHornWidth = SERVO_HORN_WIDTH


# ============================================================
# VISUAL SETTINGS
# ============================================================

obj.ViewObject.ShapeColor = (0.75, 0.75, 0.80)
obj.ViewObject.LineColor = (0.15, 0.15, 0.15)


# ============================================================
# ADD SENSOR HOLE MARKERS
# ============================================================

# These are construction/reference objects showing where
# the four HC-SR04 holes are located.

for i, (x, z) in enumerate(sensor_hole_locations):

    marker = doc.addObject(
        "PartDesign::Feature",
        "SensorHole_%d" % (i + 1)
    )

    marker.Label = "HC-SR04 Hole %d" % (i + 1)

    marker.Shape = Part.makeCylinder(
        SENSOR_HOLE_DIAMETER / 2.0,
        THICKNESS,
        App.Vector(x, 0, z),
        App.Vector(0, 1, 0)
    )

    marker.ViewObject.ShapeColor = (0.8, 0.2, 0.2)
    marker.ViewObject.Visibility = False


# ============================================================
# SAVE
# ============================================================

doc.recompute()

doc.saveAs(OUTPUT_FCSTD)

# Export STEP
Part.export([obj], OUTPUT_STEP)

print("")
print("==============================================")
print("HC-SR04 SERVO L-BRACKET CREATED")
print("==============================================")
print("FreeCAD file:")
print(OUTPUT_FCSTD)
print("")
print("STEP file:")
print(OUTPUT_STEP)
print("")
print("Bracket width:       %.1f mm" % BRACKET_WIDTH)
print("Vertical height:     %.1f mm" % VERTICAL_HEIGHT)
print("Base depth:          %.1f mm" % BASE_DEPTH)
print("Thickness:           %.1f mm" % THICKNESS)
print("")
print("HC-SR04 hole spacing:")
print("  X = %.1f mm" % SENSOR_HOLE_SPACING_X)
print("  Y = %.1f mm" % SENSOR_HOLE_SPACING_Y)
print("")
print("Servo horn:")
print("  Length = %.1f mm" % SERVO_HORN_LENGTH)
print("  Width  = %.1f mm" % SERVO_HORN_WIDTH)
print("==============================================")

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()

