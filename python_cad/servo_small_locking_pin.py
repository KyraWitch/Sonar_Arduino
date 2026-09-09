import FreeCAD as App
import Part

# ============================================================
# SERVO HORN SMALL-HOLE LOCKING PIN
# Print several copies as needed
# Units: mm
# ============================================================

# Small servo horn holes
HOLE_DIAMETER = 2.0

# Pin
PIN_DIAMETER = 1.75
PIN_LENGTH = 5.5

# Head
HEAD_DIAMETER = 4.0
HEAD_THICKNESS = 1.2

# Retaining barb
BARB_DIAMETER = 2.35
BARB_LENGTH = 1.2

# Tip
TIP_LENGTH = 1.0
TIP_DIAMETER = 1.0


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("Servo_Small_Locking_Pin")
except:
    pass

doc = App.newDocument("Servo_Small_Locking_Pin")


# ============================================================
# SHAFT
# ============================================================

shaft = Part.makeCylinder(
    PIN_DIAMETER / 2.0,
    PIN_LENGTH,
    App.Vector(0, 0, 0),
    App.Vector(0, 0, 1)
)


# ============================================================
# HEAD
# ============================================================

head = Part.makeCylinder(
    HEAD_DIAMETER / 2.0,
    HEAD_THICKNESS,
    App.Vector(0, 0, -HEAD_THICKNESS),
    App.Vector(0, 0, 1)
)


# ============================================================
# FLEXIBLE NECK
# ============================================================

neck = Part.makeCylinder(
    PIN_DIAMETER / 2.0,
    0.6,
    App.Vector(0, 0, PIN_LENGTH),
    App.Vector(0, 0, 1)
)


# ============================================================
# RETAINING BARB
# ============================================================

barb = Part.makeCone(
    PIN_DIAMETER / 2.0,
    BARB_DIAMETER / 2.0,
    BARB_LENGTH,
    App.Vector(0, 0, PIN_LENGTH + 0.6),
    App.Vector(0, 0, 1)
)


# ============================================================
# TAPERED TIP
# ============================================================

tip = Part.makeCone(
    BARB_DIAMETER / 2.0,
    TIP_DIAMETER / 2.0,
    TIP_LENGTH,
    App.Vector(
        0,
        0,
        PIN_LENGTH + 0.6 + BARB_LENGTH
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
# FREECAD OBJECT
# ============================================================

obj = doc.addObject(
    "PartDesign::Feature",
    "Servo_Small_Locking_Pin"
)

obj.Label = "Servo Horn Small Locking Pin"
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
    "servo_small_locking_pin.FCStd"
)

Part.export(
    [obj],
    "servo_small_locking_pin.step"
)


# ============================================================
# DISPLAY
# ============================================================

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()


print("")
print("==============================================")
print("SERVO SMALL LOCKING PIN CREATED")
print("==============================================")
print("")
print("Designed for approximately %.1f mm holes."
      % HOLE_DIAMETER)
print("")
print("Pin diameter: %.2f mm" % PIN_DIAMETER)
print("Pin length:   %.2f mm" % PIN_LENGTH)
print("Head:         %.2f mm" % HEAD_DIAMETER)
print("Barb:         %.2f mm" % BARB_DIAMETER)
print("")
print("Print several copies as required.")
print("")
print("Files created:")
print("  servo_small_locking_pin.FCStd")
print("  servo_small_locking_pin.step")
print("==============================================")

