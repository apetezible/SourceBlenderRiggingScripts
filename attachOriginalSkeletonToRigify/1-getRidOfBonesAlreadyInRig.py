#Put the original armature in the file then rescale and rotate. apply.
#Make a Layer in it with all the bones for easy access
#Remove all parenting with alt in edit mode
#Merge Armatures
#Select all bones in original layer

import bpy

DUPLICATE_SUFFIX = "_CTRL"

def mark_duplicate_bones_in_rig():
    # Expect exactly two armatures selected
    armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
    if len(armatures) != 2:
        print("Select exactly TWO armatures in Object Mode.")
        return

    arm_a, arm_b = armatures

    # Identify the RIG- armature
    if "RIG-" in arm_a.name and "RIG-" not in arm_b.name:
        rig = arm_a
        other = arm_b
    elif "RIG-" in arm_b.name and "RIG-" not in arm_a.name:
        rig = arm_b
        other = arm_a
    else:
        print("Exactly one armature must have 'RIG-' in its OBJECT name.")
        return

    rig_names = {bone.name for bone in rig.data.bones}
    other_names = {bone.name for bone in other.data.bones}

    # Find duplicated bone names
    duplicated_names = rig_names.intersection(other_names)
    if not duplicated_names:
        print("No duplicated bones found. Nothing to mark.")
        return

    print("==============================")
    print(f"Marking duplicated bones in RIG armature: {rig.name}")
    print(f"Reference armature: {other.name}")
    print(f"Bones to MARK: {len(duplicated_names)}")
    for name in sorted(duplicated_names):
        print(name)
    print("==============================")

    # Switch to Edit Mode on RIG armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    renamed = []
    for eb in rig.data.edit_bones:
        if eb.name in duplicated_names:
            # Avoid double-marking if script is run twice
            if not eb.name.endswith(DUPLICATE_SUFFIX):
                original_name = eb.name
                eb.name = original_name + DUPLICATE_SUFFIX
                renamed.append(eb.name)

    bpy.ops.object.mode_set(mode='OBJECT')

    print("==============================")
    print(f"Marked {len(renamed)} bones in '{rig.name}':")
    for name in renamed:
        print(name)
    print("==============================")

mark_duplicate_bones_in_rig()


