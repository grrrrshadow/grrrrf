# -*- coding: utf-8 -*-
import bpy
import os

print("--- Kontrola objektu na negativni skalu a zrcadlove transformace ---")

# Cesta k GLB souboru
base_dir = os.path.dirname(bpy.data.filepath)
if not base_dir:
    base_dir = os.getcwd()

glb_files = [f for f in os.listdir(base_dir) if f.lower().endswith('.glb')]
if not glb_files:
    raise Exception("Chyba: V adresari nebyl nalezen zadny GLB soubor.")

glb_path = os.path.join(base_dir, glb_files[0])
print(f"Importuji GLB: {glb_path}")

# Vymazani scény (pro test)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import GLB
bpy.ops.import_scene.gltf(filepath=glb_path)

# Projdeme vsechny objekty v scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        scale = obj.scale
        rot = obj.rotation_euler
        neg_scale = any(s < 0 for s in scale)
        print(f"Objekt '{obj.name}': skala={scale}, rotace={rot}, negativni_skala={neg_scale}")
