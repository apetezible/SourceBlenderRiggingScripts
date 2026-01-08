#Select SFM armature last

import bpy

# Ensure Object Mode
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

# Get selected armatures
armatures = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

if len(armatures) != 2:
    raise RuntimeError(
        "Select exactly TWO armatures.\n"
        "Active armature = receiver\n"
        "Other armature = source"
    )

target_arm = bpy.context.active_object
source_arm = armatures[0] if armatures[1] == target_arm else armatures[1]

print(f"\nReceiver armature: {target_arm.name}")
print(f"Source armature:   {source_arm.name}")

missing = []

# Pose Mode required for constraints
bpy.context.view_layer.objects.active = target_arm
bpy.ops.object.mode_set(mode='POSE')

for pbone in target_arm.pose.bones:
    name = pbone.name

    if name not in source_arm.pose.bones:
        missing.append(name)
        continue

    # Optional: remove existing matching constraints
    for c in list(pbone.constraints):
        if c.target == source_arm and c.subtarget == name:
            if c.type in {'COPY_LOCATION', 'COPY_ROTATION', 'COPY_SCALE'}:
                pbone.constraints.remove(c)

    # Copy Location
    c_loc = pbone.constraints.new('COPY_LOCATION')
    c_loc.target = source_arm
    c_loc.subtarget = name

    # Copy Rotation
    c_rot = pbone.constraints.new('COPY_ROTATION')
    c_rot.target = source_arm
    c_rot.subtarget = name

    # Copy Scale (SPECIAL CAVEAT)
    c_scl = pbone.constraints.new('COPY_SCALE')
    c_scl.target = source_arm
    c_scl.subtarget = name

    c_scl.target_space = 'LOCAL'
    c_scl.owner_space  = 'WORLD'

    print(f"✓ Constrained {name}")

# Back to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

# Popup report
def draw(self, context):
    if not missing:
        self.layout.label(text="All bones constrained successfully!")
    else:
        self.layout.label(text=f"{len(missing)} bones had no matching source bone.")
        self.layout.label(text="Check the console for details.")

bpy.context.window_manager.popup_menu(
    draw,
    title="Constraint Report",
    icon='INFO'
)

print("\nBones without matching source bone:")
for b in missing:
    print(" -", b)

print("\nDone.")