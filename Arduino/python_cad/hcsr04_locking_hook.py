import FreeCAD as App
import Part

# ============================================================
# HC-SR04 SLIDING LOCKING HOOK
# Designed for the existing 4 mm thick L-bracket
# Units: mm
# ============================================================

# ---------------- BRACKET ----------------
BRACKET_THICKNESS = 4.0

# Clearance between hook and bracket
CLEARANCE = 0.35

# ---------------- HOOK ----------------
HOOK_WIDTH = 12.0
HOOK_LENGTH = 24.0
HOOK_THICKNESS = 4.0

# Depth of the hook that catches the bracket
CATCH_DEPTH = 5.0

# ---------------- LOCKING TAB ----------------
TAB_WIDTH = 8.0
TAB_LENGTH = 12.0
TAB_THICKNESS = 3.0

# Clearance for sliding
SLIDE_CLEARANCE = 0.4

# ---------------- PRINT ----------------
# Slightly rounded/softened locking nose
NOSE_LENGTH = 4.0


# ============================================================
# NEW DOCUMENT
# ============================================================

try:
    App.closeDocument("HC_SR04_Locking_Hook")
except:
    pass

doc = App.newDocument("HC_SR04_Locking_Hook")


# ============================================================
# MAIN SLIDING HOOK
#
# The bracket slides into the channel underneath.
# ============================================================

# Main body
body = Part.makeBox(
    HOOK_WIDTH,
    HOOK_LENGTH,
    HOOK_THICKNESS
)


# ============================================================
# CREATE CHANNEL FOR 4 MM BRACKET
# ============================================================

channel_width = HOOK_WIDTH
channel_depth = BRACKET_THICKNESS + CLEARANCE

channel = Part.makeBox(
    channel_width,
    HOOK_LENGTH - CATCH_DEPTH,
    channel_depth
)

# Put channel underneath the body
channel.translate(
    App.Vector(
        0,
        CATCH_DEPTH,
        -CLEARANCE
    )
)

body = body.cut(channel)


# ============================================================
# FRONT CATCH
#
# This section remains solid and catches the edge of the
# L-bracket.
# ============================================================

catch = Part.makeBox(
    HOOK_WIDTH,
    CATCH_DEPTH,
    HOOK_THICKNESS + BRACKET_THICKNESS
)

catch.translate(
    App.Vector(
        0,
        0,
        -BRACKET_THICKNESS
    )
)

body = body.fuse(catch)


# ============================================================
# LOCKING TAB
# ============================================================

tab = Part.makeBox(
    TAB_WIDTH,
    TAB_LENGTH,
    TAB_THICKNESS
)

tab_x = (HOOK_WIDTH - TAB_WIDTH) / 2.0

tab.translate(
    App.Vector(
        tab_x,
        HOOK_LENGTH - TAB_LENGTH,
        HOOK_THICKNESS
    )
)

body = body.fuse(tab)


# ============================================================
# LOCKING NOSE
#
# Angled-ish retaining block at end of tab.
# ============================================================

nose = Part.makeBox(
    TAB_WIDTH,
    NOSE_LENGTH,
    TAB_THICKNESS + 2.0
)

nose.translate(
    App.Vector(
        tab_x,
        HOOK_LENGTH - NOSE_LENGTH,
        HOOK_THICKNESS
    )
)

body = body.fuse(nose)


# ============================================================
# RELIEF CUT
#
# Makes the locking tab slightly flexible.
# ============================================================

relief_width = TAB_WIDTH + 2.0
relief_length = TAB_LENGTH - 2.0

relief = Part.makeBox(
    relief_width,
    relief_length,
    TAB_THICKNESS
)

relief.translate(
    App.Vector(
        tab_x - 1.0,
        HOOK_LENGTH - TAB_LENGTH + 2.0,
        HOOK_THICKNESS
    )
)

# Don't cut completely through the tab.
# Leave a small flexible section.

# body = body.cut(relief)


# ============================================================
# CREATE OBJECT
# ============================================================

obj = doc.addObject(
    "PartDesign::Feature",
    "HCSR04_Locking_Hook"
)

obj.Label = "HC-SR04 L-Bracket Locking Hook"
obj.Shape = body


# ============================================================
# DIMENSION PROPERTIES
# ============================================================

obj.addProperty(
    "App::PropertyLength",
    "BracketThickness",
    "Dimensions"
)
obj.BracketThickness = BRACKET_THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "Clearance",
    "Dimensions"
)
obj.Clearance = CLEARANCE

obj.addProperty(
    "App::PropertyLength",
    "HookWidth",
    "Dimensions"
)
obj.HookWidth = HOOK_WIDTH

obj.addProperty(
    "App::PropertyLength",
    "HookLength",
    "Dimensions"
)
obj.HookLength = HOOK_LENGTH

obj.addProperty(
    "App::PropertyLength",
    "HookThickness",
    "Dimensions"
)
obj.HookThickness = HOOK_THICKNESS

obj.addProperty(
    "App::PropertyLength",
    "CatchDepth",
    "Dimensions"
)
obj.CatchDepth = CATCH_DEPTH


# ============================================================
# COLOR
# ============================================================

obj.ViewObject.ShapeColor = (0.90, 0.55, 0.10)
obj.ViewObject.LineColor = (0.15, 0.15, 0.15)


# ============================================================
# SAVE
# ============================================================

doc.recompute()

doc.saveAs(
    "hcsr04_locking_hook.FCStd"
)

Part.export(
    [obj],
    "hcsr04_locking_hook.step"
)


# ============================================================
# DISPLAY
# ============================================================

Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()


print("")
print("==============================================")
print("HC-SR04 LOCKING HOOK CREATED")
print("==============================================")
print("")
print("Designed for:")
print("  4 mm L-bracket")
print("")
print("Clearance:")
print("  %.2f mm" % CLEARANCE)
print("")
print("Hook size:")
print("  %.1f x %.1f x %.1f mm"
      % (
          HOOK_WIDTH,
          HOOK_LENGTH,
          HOOK_THICKNESS
      ))
print("")
print("Created:")
print("  hcsr04_locking_hook.FCStd")
print("  hcsr04_locking_hook.step")
print("")
print("==============================================")

