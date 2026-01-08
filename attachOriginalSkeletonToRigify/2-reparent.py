#Select bones in pose mode ALREADY MERGED
#Run and check console
#tweak

import bpy

DUPLICATE_PREFIX = "__DUPLICATE__"
DEF_PREFIX = "DEF-"

obj = bpy.context.object

if obj is None or obj.type != 'ARMATURE':
    raise RuntimeError("Select the Armature object first.")

# Must select bones in Pose Mode
sel_pose_bones = list(bpy.context.selected_pose_bones)
if not sel_pose_bones:
    raise RuntimeError("No pose bones selected. Select bones in Pose Mode first.")

orig_mode = bpy.context.mode
not_parented = []

try:
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = obj.data.edit_bones

    for pb in sel_pose_bones:
        name = pb.name
        src_eb = edit_bones.get(name)

        if not src_eb:
            not_parented.append(name)
            continue

        # --- 1) Try DEF- counterpart ---
        def_name = DEF_PREFIX + name
        def_eb = edit_bones.get(def_name)

        if def_eb:
            src_eb.parent = def_eb
            src_eb.use_connect = False
            print(f"[DEF] Parented {name} → {def_name}")
            continue

        # --- 2) Try __DUPLICATE__ fallback ---
        dup_name = DUPLICATE_PREFIX + name
        dup_eb = edit_bones.get(dup_name)

        if dup_eb and dup_eb.parent:
            src_eb.parent = dup_eb.parent
            src_eb.use_connect = False
            print(
                f"[DUP] Parented {name} → parent of {dup_name} "
                f"({dup_eb.parent.name})"
            )
            continue

        # --- 3) No valid target ---
        not_parented.append(name)

finally:
    # Restore previous mode safely
    try:
        bpy.ops.object.mode_set(mode=orig_mode)
    except Exception:
        bpy.ops.object.mode_set(mode='OBJECT')

# --- Summary ---
print("\n==============================")
if not_parented:
    print("Bones NOT reparented:")
    for n in not_parented:
        print(" -", n)
else:
    print("All selected bones reparented successfully.")
print("==============================")