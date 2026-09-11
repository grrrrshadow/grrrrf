# -*- coding: utf-8 -*-

import bpy
import os
import sys

BASE_DIR = os.getcwd()

# clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# find obj
obj_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".obj")]
if not obj_files:
    print("ERROR: no obj found")
    sys.exit(1)

obj_path = os.path.join(BASE_DIR, obj_files[0])
glb_path = os.path.splitext(obj_path)[0] + ".glb"

# import OBJ (Blender 4.3+)
bpy.ops.wm.obj_import(
    filepath=obj_path,
    forward_axis='NEGATIVE_Z',
    up_axis='Y'
)

# DO NOT TOUCH TRANSFORMS
# no rotation
# no parenting
# no origin change

# export GLB
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    export_materials='EXPORT',
    use_selection=False,
    export_apply=False
)

print("OK:", glb_path)
