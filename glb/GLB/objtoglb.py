# -*- coding: utf-8 -*-
import bpy
import os
import sys

# clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# working directory
base_dir = os.getcwd()

# find first OBJ
obj_file = None
for f in os.listdir(base_dir):
    if f.lower().endswith(".obj"):
        obj_file = f
        break

if not obj_file:
    raise Exception("No OBJ file found")

obj_path = os.path.join(base_dir, obj_file)

# import OBJ
bpy.ops.wm.obj_import(filepath=obj_path)

# ensure materials exist and keep names
for mat in bpy.data.materials:
    mat.use_nodes = True

# find root objects
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.material_slots:
        obj.select_set(True)
    else:
        obj.select_set(False)

# export GLB
out_glb = os.path.join(base_dir, os.path.splitext(obj_file)[0] + ".glb")

bpy.ops.export_scene.gltf(
    filepath=out_glb,
    export_format='GLB',
    export_materials='EXPORT',
    export_apply=True
)

print("DONE:", out_glb)
