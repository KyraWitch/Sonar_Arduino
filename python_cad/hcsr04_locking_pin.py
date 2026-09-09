import FreeCAD as App
import Part

# ============================================================
# HC-SR04 / L-BRACKET PUSH-IN LOCKING PIN
# Print 4 copies
# Units: mm
# ============================================================

# Existing bracket / sensor hole
HOLE_DIAMETER = 2.6

# Pin shaft
PIN_DIAMETER = 2.35
PIN_LENGTH = 7.0

# Head
HEAD_DIAMETER = 5.5
HEAD_THICKNESS = 1.5

# Retaining barb
BARB_DIAMETER = 3.2
BARB_LENGTH = 1.5

# Small gap between barb and pin shaft
BARB_BASE_DIAMETER = 2.0


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("HCSR04_Locking_Pin")
except:
    pass

doc = App.newDocument("HCSR04_Locking_Pin")


# ============================================================
# PIN SHAFT
# ============================================================

shaft = Part.makeCylinder(
    PIN_DIAMETER / 2.0,
    PIN_LENGTH,
    App.Vector(0, 0, 0),
    App.Vector(0, 0, 1)
)


# ============================================================
# LARGE HEAD
# ============================================================

head = Part.makeCylinder(
    HEAD_DIAMETER / 2.0,
    HEAD_THICKNESS,
    App.Vector(0, 0, -HEAD_THICKNESS),
    App.Vector(0, 0, 1)
)


# ============================================================
# RETAINING BARB
#
# Tapered section that flexes while being pushed through
# the mounting hole, then catches on the rear side.
# ============================================================

# Narrow neck
neck = Part.makeCylinder(
    BARB_BASE_DIAMETER / 2.0,
    0.7,
    App.Vector(0, 0, PIN_LENGTH),
    App.Vector(0, 0, 1)
)

# Cone-shaped retaining barb
barb = Part.makeCone(
    PIN_DIAMETER / 2.0,
    BARB_DIAMETER / 2.0,
    BARB_LENGTH,
    App.Vector(0, 0, PIN_LENGTH + 0.5),
    App.Vector(0, 0, 1)
)


# ============================================================
# TIP
# ============================================================

tip = Part.makeCone(
    BARB_DIAMETER / 2.0,
    1.0,
    1.2,
    App.Vector(
        0,
        0,
        PIN_LENGTH + 0.5 + BARB_LENGTH
    ),
    App.Vector(0, 0, 1)
)


# ============================================================
# COMBINE
# ============================================================

pin = shaft.fuse(head)
pin = pin.fuse(neck)
pin = pin.fuse(barb)
pin = pin.fuse(tip)


# ============================================================
# CREATE FREECAD OBJECT
# ============================================================

obj = doc.addObject(
    "PartDesign::Feature",
    "HCSR04_Locking_Pin"
)

obj.Label = "HC-SR04 Push-In Locking Pin"
obj.Shape = pin


# ============================================================
# DIMENSION PROPERTIES
# ============================================================

obj.addProperty(
    "App::PropertyLength",
    "PinDiameter",
    "Dimensions"
)
obj.PinDiameter = PIN_DIAMETER

obj.addProperty(
    "App::PropertyLength",
    "PinLength",
    "Dimensions"
)
obj.PinLength = PIN_LENGTH

obj.addProperty(
    "App::PropertyLength",
    "HeadDiameter",
    "Dimensions"
)
obj.HeadDiameter = HEAD_DIAMETER

obj.addProperty(
    "App::PropertyLength",
    "HeadThickness",
    "Dimensions"
)
obj.HeadThickness = HEAD_THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "BarbDiameter",
    "Dimensions"
)
obj.BarbDiameter = BARB_DIAMETER

obj.addProperty(
    "App::PropertyLength",
    "BarbLength",
    "Dimensions"
)
obj.BarbLength = BARB_LENGTH


# ============================================================
# VISUAL
# ============================================================

obj.ViewObject.ShapeColor = (0.90, 0.60, 0.10)
obj.ViewObject.LineColor = (0.10, 0.10, 0.10)


# ============================================================
# SAVE
# ============================================================

doc.recompute()

doc.saveAs(
    "hcsr04_locking_pin.FCStd"
)

Part.export(
    [obj],
    "hcsr04_locking_pin.step"
)


# ============================================================
# DISPLAY
# ============================================================

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()


print("")
print("==============================================")
print("HC-SR04 LOCKING PIN CREATED")
print("==============================================")
print("")
print("Print 4 copies.")
print("")
print("Pin diameter: %.2f mm" % PIN_DIAMETER)
print("Pin length:   %.2f mm" % PIN_LENGTH)
print("Head:         %.2f mm" % HEAD_DIAMETER)
print("Barb:         %.2f mm" % BARB_DIAMETER)
print("")
print("Designed for approximately %.1f mm holes."
      % HOLE_DIAMETER)
print("")
print("Files created:")
print("  hcsr04_locking_pin.FCStd")
print("  hcsr04_locking_pin.step")
print("==============================================")

