# -*- coding: utf-8 -*-
# Foceni M62 "Sergej" pro OpenTTD. Odvozeno z hracova glb3BBC.py (24. 1. 2026):
# stejna kamera (ortho, 30 stupnu nad obzorem, 45 stupnu azimut), stejne HDRI snow.exr
# bez stinu, stejny Cycles a stejne uhly otoceni. Pridano:
#   - meritko v px na metr misto ortho_scale (CZTR ma ~12,2 px/m v zin4)
#   - stlaceni podel osy na rovne koleji (smery 1,3,5,7): hra tam stavi vozidla
#     hustsi nez na sikme koleji (8 px na osminu proti 16 px), CZTR to dela stejne
#   - barevny pruchod: ktery pixel patri hlave, stredu a zadi (lokomotiva je 3 clanky)
#   - kotva (bod na koleji pod stredem lokomotivy) spoctena promitnutim, ne odhadem
# Spousti se:  python3 render_sergej.py <natier: zeleny|cerveny> <px_na_m> <osmin: 12|14> <vystup>
import bpy, os, sys, math, json
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import nater

NATER, PX_M, OSMIN, VYSTUP = sys.argv[-4], float(sys.argv[-3]), int(sys.argv[-2]), sys.argv[-1]
MODEL = os.path.join(TU, "model", "diesel_locomotive_m62.glb")
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = 320                         # ctverec rendru v px (zin4); lokomotiva se do nej vejde v obou meritkach
SAMPLES = int(os.environ.get("SAMPLES", "256"))
# poradi smeru jako vycet Direction ve hre: N, NE, E, SE, S, SW, W, NW, a 8 = obrazek do nakupu (W)
ROTATION_ANGLES = [225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0, 315.0]
ROVNE = (1, 3, 5, 7)              # smery po rovne koleji (na obrazovce sikmo)
STLACENI = 1 / math.sqrt(2)       # na rovne koleji je osmina 8 px vodorovne, na sikme 16 px
KROK = {0: (0, -8), 1: (8, -4), 2: (16, 0), 3: (8, 4), 4: (0, 8), 5: (-8, 4), 6: (-16, 0), 7: (-8, -4)}

os.makedirs(VYSTUP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = False
scene.cycles.samples = SAMPLES
scene.render.resolution_x = scene.render.resolution_y = RAM
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True

world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment'); wo = nt.nodes.new('ShaderNodeOutputWorld')
env.image = bpy.data.images.load(HDRI)
nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
scene.world.cycles_visibility.shadow = False       # jako v glb3BBC.py: bez stinu z HDRI

pred = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=MODEL)
nove = list(set(scene.objects) - pred)
koren = [o for o in nove if o.parent is None][0]
meshe = [o for o in [koren] + list(koren.children_recursive) if o.type == 'MESH']
pts = [o.matrix_world @ v.co for o in meshe for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
DELKA = mx.y - mn.y                                   # model lezi podel osy Y
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "delka", round(DELKA, 3))

if NATER == "cerveny":
    for img in bpy.data.images:
        if img.name in ("Image_0", "Image_6", "Image_8"):
            w, h = img.size
            px = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(px)
            px = px.reshape(h, w, 4)
            # Blender ma obrazky odspodu nahoru, nater pocita s radky shora
            rgb = (np.flipud(px[..., :3]) * 255 + 0.5).astype(np.uint8)
            nove_rgb = np.flipud(nater.cerveny(img.name, rgb)).astype(np.float32) / 255
            px[..., :3] = nove_rgb
            img.pixels.foreach_set(px.ravel()); img.update()
            print("prebarveno", img.name)

# gramofon (otaceni) -> natahovac (stlaceni podel osy modelu) -> model
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); natah = bpy.context.object
natah.parent = gramofon; natah.matrix_parent_inverse = gramofon.matrix_world.inverted()
koren.parent = natah; koren.matrix_parent_inverse = natah.matrix_world.inverted()
body = {}
for jm, co in (("kotva", (stred.x, stred.y, mn.z)), ("plus", (stred.x, mx.y, mn.z)), ("minus", (stred.x, mn.y, mn.z)),
               ("vrsek", (stred.x, stred.y, mx.z))):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=co); e = bpy.context.object
    e.parent = natah; e.matrix_parent_inverse = natah.matrix_world.inverted(); body[jm] = e

ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon

# material pro barevny pruchod: podle souradnice Y v prostoru natahovace (= puvodni metry modelu)
POLOVINA_STREDU = (DELKA / 2) * (4.0 / (OSMIN / 2.0))      # stredni clanek ma 8 osmin z OSMIN
m = bpy.data.materials.new("vlastnik"); m.use_nodes = True
mt = m.node_tree
for n in list(mt.nodes): mt.nodes.remove(n)
tc = mt.nodes.new('ShaderNodeTexCoord'); tc.object = natah
sep = mt.nodes.new('ShaderNodeSeparateXYZ'); mt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
gt = mt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = POLOVINA_STREDU
lt = mt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = -POLOVINA_STREDU
mt.links.new(sep.outputs['Y'], gt.inputs[0]); mt.links.new(sep.outputs['Y'], lt.inputs[0])
mid = mt.nodes.new('ShaderNodeMath'); mid.operation = 'SUBTRACT'; mid.inputs[0].default_value = 1.0
add = mt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
mt.links.new(gt.outputs[0], add.inputs[0]); mt.links.new(lt.outputs[0], add.inputs[1]); mt.links.new(add.outputs[0], mid.inputs[1])
comb = mt.nodes.new('ShaderNodeCombineColor')
mt.links.new(gt.outputs[0], comb.inputs[0]); mt.links.new(mid.outputs[0], comb.inputs[1]); mt.links.new(lt.outputs[0], comb.inputs[2])
em = mt.nodes.new('ShaderNodeEmission'); mt.links.new(comb.outputs[0], em.inputs['Color'])
out = mt.nodes.new('ShaderNodeOutputMaterial'); mt.links.new(em.outputs[0], out.inputs['Surface'])

def na_pixel(obj):
    bpy.context.view_layer.update()
    p = world_to_camera_view(scene, cam, obj.matrix_world.translation)
    return (p.x * RAM, (1 - p.y) * RAM)

info = {"nater": NATER, "px_m": PX_M, "osmin": OSMIN, "ram": RAM, "delka_m": DELKA, "smery": {}}
for d, uhel in enumerate(ROTATION_ANGLES):
    gramofon.rotation_euler[2] = math.radians(uhel)
    natah.scale = (1, STLACENI, 1) if d in ROVNE else (1, 1, 1)
    bpy.context.view_layer.update()
    kot = na_pixel(body["kotva"]); plus = na_pixel(body["plus"]); minus = na_pixel(body["minus"])
    kx, ky = KROK[d % 8]
    predni = "plus" if (plus[0] - minus[0]) * kx + (plus[1] - minus[1]) * ky > 0 else "minus"
    info["smery"][d] = {"kotva": kot, "plus": plus, "minus": minus, "predni": predni}
    scene.view_layers[0].material_override = None
    scene.cycles.samples = SAMPLES; scene.cycles.filter_width = 1.5
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    if d in ROVNE:
        scene.view_layers[0].material_override = m
        scene.cycles.samples = 1; scene.cycles.filter_width = 0.01
        scene.render.filepath = os.path.join(VYSTUP, f"vlastnik_d{d}.png")
        bpy.ops.render.render(write_still=True)
    print("smer", d, "kotva", [round(v, 1) for v in kot], "predni konec", predni, flush=True)
scene.view_layers[0].material_override = None
json.dump(info, open(os.path.join(VYSTUP, "kotvy.json"), "w"), indent=1)
print("hotovo")
