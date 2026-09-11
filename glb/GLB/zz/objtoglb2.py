# -*- coding: utf-8 -*-

import bpy
import os
import math

# --- CLEAN SCENE ---
bpy.ops.wm.read_factory_settings(use_empty=True)

base_dir = os.getcwd()

# --- FIND OBJ ---
obj_files = [f for f in os.listdir(base_dir) if f.lower().endswith(".obj")]
if not obj_files:
    raise Exception("No OBJ found")

obj_path = os.path.join(base_dir, obj_files[0])

# --- IMPORT OBJ ---
bpy.ops.wm.obj_import(filepath=obj_path)

# --- COLLECT MESHES ---
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not meshes:
    raise Exception("No meshes imported")

# --- CREATE ROOT EMPTY ---
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
root = bpy.context.object
root.name = "turntable_and_target"

# --- MOVE ORIGINS TO GEOMETRY + PARENT ---
bpy.ops.object.select_all(action='DESELECT')

for o in meshes:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    o.parent = root
    o.select_set(False)

# --- CENTER ROOT ---
bpy.context.view_layer.objects.active = root
bpy.ops.object.select_all(action='DESELECT')
root.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
root.location = (0,0,0)

# --- EXPORT GLB ---
glb_path = os.path.join(base_dir, "output.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    export_materials='EXPORT'
)

print("GLB exported:", glb_path)
