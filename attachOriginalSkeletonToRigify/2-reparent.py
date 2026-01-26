#Select bones in pose mode ALREADY MERGED
#Switch to edit mode
#Run and check console
#tweak
import bpy

CTRL_SUFFIX = "_CTRL"
DEF_PREFIX = "DEF-"

def reparent_selected_bones():
    # Must be in Edit Mode with bones selected
    if bpy.context.mode != 'EDIT_ARMATURE':
        print("Switch to Edit Mode and select bones before running.")
        return

    arm = bpy.context.object
    ebones = arm.data.edit_bones

    selected = [b for b in ebones if b.select]
    if not selected:
        print("No bones selected.")
        return

    reparented = []

    for eb in selected:
        def_name = DEF_PREFIX + eb.name
        ctrl_name = eb.name + CTRL_SUFFIX

        if def_name in ebones:
            eb.parent = ebones[def_name]
            reparented.append((eb.name, def_name))
        elif ctrl_name in ebones:
            eb.parent = ebones[ctrl_name]
            reparented.append((eb.name, ctrl_name))
        else:
            print(f"No DEF- or _CTRL match found for {eb.name}")

    print("==============================")
    print(f"Reparented {len(reparented)} bones in '{arm.name}':")
    for child, parent in reparented:
        print(f"{child} → {parent}")
    print("==============================")

reparent_selected_bones()


