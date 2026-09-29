# -*- coding: utf-8 -*-
# Foceni Tatry 148 (hans1240, "Tatra-148-AKT-3-3", CC BY 4.0) pro OpenTTD, stejne jako vejtraska (v3s/render_v3s.py):
# ortho kamera 30 stupnu nad obzorem, azimut 45 stupnu, HDRI snow.exr, 8 smeru ve stejnem meritku.
# Hrac 29. 9.: "hans1240 berem na tekutiny", "zkus jednu od Hanse, jak bude vypadat".
#   python3 render_t148.py <nater> <px_na_m> <vystup>        nater: oranzova (T148), cervena (T138)
# Model nema barvy ani textury (materialy bile a sede), barvy se davaji podle jmen materialu (BARVY).
import bpy, os, sys, math, json
from mathutils import Vector

TU = os.path.dirname(os.path.abspath(__file__))
NATER, PX_M, VYSTUP = sys.argv[-3], float(sys.argv[-2]), sys.argv[-1]
MODEL = os.environ.get("MODEL", os.path.join(TU, "model", "tatra-148-akt-3-3.glb"))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = 256
SAMPLES = int(os.environ.get("SAMPLES", "256"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
# jako u vejtrasky: uhly z render_sergej.py pocitaji s celem na -Y, Tatra ma kabinu na +Y, proto +180
ROTATION_ANGLES = [(u + 180.0) % 360 for u in (225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0)]

os.makedirs(VYSTUP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = SAMPLES
scene.cycles.filter_width = 1.5
scene.render.resolution_x = scene.render.resolution_y = RAM; scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
world = bpy.data.worlds.new("World"); scene.world = world; world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment'); wo = nt.nodes.new('ShaderNodeOutputWorld')
env.image = bpy.data.images.load(HDRI)
nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
scene.world.cycles_visibility.shadow = False

pred = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=MODEL)
nove = list(set(scene.objects) - pred)
koreny = [o for o in nove if o.parent is None]
meshe = [o for o in nove if o.type == 'MESH']

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

# ---------------------------------------------------------------- barvy podle materialu
# Materialy modelu (jmeno bez cisla na konci po teckce se nebere, kazdy ma svoje): bile plechy kabiny, dveri,
# cisterny a naraznik v barve nateru; sede kovove dily tmave sede; ram cerny; svetla podle barvy v modelu.
# hrac 29. 9.: "majaky pryc, zadna vojenska, oranzovy tatrovacky 148 a cerveny komunisticka cervena 138"
NATERY = {"oranzova": (224, 104, 24), "cervena": (176, 24, 20)}
LAK = NATERY[NATER]
BARVY = {
    "kabina.2": LAK, "kabina.3": LAK, "kabina.4": LAK, "kabina.9": LAK, "kabina.10": LAK, "kabina.11": LAK,
    "door_rf_ok.5": LAK, "AC.6": LAK, "otboynik.2": LAK, "primochki.1": LAK, "primochki.6": LAK, "wheel_rm.1": LAK,
    "kabina.6": (58, 58, 56), "kabina.7": (36, 36, 36), "kabina.8": (70, 70, 68), "kabina.13": (62, 62, 60),
    "door_rf_ok.4": (60, 60, 58), "AC.5": (66, 66, 62), "primochki.4": (60, 60, 58), "otboynik.3": (46, 46, 44),
    "otboynik.5": (46, 46, 44), "otboynik.6": (46, 46, 44),
    "rama.0": (22, 22, 22), "wheel_rm.2": (26, 26, 26), "primochki.2": (22, 22, 22),   # wheel_rm.2 pneumatiky, .1 disky
    "kabina.12": (150, 150, 146), "right_front_light.001": (150, 150, 146),   # stresni svetla hasicky, nesviti
    "salon.2": (44, 42, 40), "salon.3": (44, 42, 40), "salon.4": (44, 42, 40), "salon.5": (44, 42, 40), "salon.6": (44, 42, 40),
    "primochki.3": (150, 30, 20), "primochki.5": (30, 40, 26),
}
SVITI = {"right_front_light": (255, 255, 250), "left_front_light": (255, 255, 250),
         "right_rear_light": (200, 24, 16)}          # oba reflektory bile
SKRYT = {"kabina.15"}                                # modre majaky (hasicska cisterna), na tekutiny pryc
for m in bpy.data.materials:
    if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes: continue
    b = m.node_tree.nodes["Principled BSDF"]
    if m.name in BARVY:
        b.inputs["Base Color"].default_value = srgb(BARVY[m.name]); b.inputs["Roughness"].default_value = 0.6
    elif m.name in SVITI:
        b.inputs["Base Color"].default_value = srgb(SVITI[m.name])
        b.inputs["Emission Color"].default_value = srgb(SVITI[m.name]); b.inputs["Emission Strength"].default_value = 1.5
    elif m.name == "glass":
        b.inputs["Base Color"].default_value = (0.030, 0.040, 0.055, 1.0); b.inputs["Roughness"].default_value = 0.15
for o in meshe:
    if any(s.material and s.material.name in SKRYT for s in o.material_slots):
        o.hide_render = True
neznama = sorted({s.material.name for o in meshe for s in o.material_slots if s.material} - set(BARVY) - set(SVITI) - SKRYT - {"glass"})
print("materialy bez barvy:", neznama)

pts = [o.matrix_world @ v.co for o in meshe if not o.hide_render for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "delka", round(mx.y - mn.y, 2))

bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
for k in koreny:
    k.parent = gramofon; k.matrix_parent_inverse = gramofon.matrix_world.inverted()
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, flush=True)
print("hotovo")
