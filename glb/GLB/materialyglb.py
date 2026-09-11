# -*- coding: utf-8 -*-
import bpy
import os

# adresar skriptu / cwd
base_dir = os.getcwd()

# najdi prvni GLB
glb_files = [f for f in os.listdir(base_dir) if f.lower().endswith(".glb")]
if not glb_files:
    raise Exception("Nenalezen  .glb soubor")

glb_path = os.path.join(base_dir, glb_files[0])

# import GLB
bpy.ops.import_scene.gltf(filepath=glb_path)

print("\n=== SEZNAM MATERIaLu ===")
materials = set()

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                materials.add(slot.material.name)

for m in sorted(materials):
    print(m)

print(f"\nCelkem materialu: {len(materials)}")
