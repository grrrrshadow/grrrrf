# -*- coding: utf-8 -*-
# Foceni Skody 706 RTO pro OpenTTD (silnicni vozidlo) z vlastniho modelu (model_rto.py). Kamera, HDRI a Cycles jako
# render_v3s.py: ortho, 30 stupnu nad obzorem, azimut 45 stupnu, snow.exr bez stinu; silnicni vozidla se nestlacuji,
# vsech 8 smeru je ve stejnem meritku. ZIN=8 foti 8x (dvojnasobne px/m i ram), do GRF jde k 4x.
#   [ZIN=8] [SMERY=1,6] [RAM=..] python3 render_rto.py <cervena|modra> <px_na_m (4x)> <vystup>
# Vystup: d0-d7.png (smery jako vycet Direction: N, NE, E, SE, S, SW, W, NW) a kotvy.json s promitnutym bodem na zemi
# pod stredem auta (pul delky, pul sirky) a pod stredem rozvoru.
import bpy, os, sys, math, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import model_rto

NATER, PX_M, VYSTUP = sys.argv[-3], float(sys.argv[-2]), sys.argv[-1]
ZIN = int(os.environ.get("ZIN", "4"))
PX_M *= ZIN / 4
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = int(os.environ.get("RAM", str(256 * ZIN // 4)))
SAMPLES = int(os.environ.get("SAMPLES", "256"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
# uhly z render_sergej.py pocitaji s celem modelu na -Y; autobus ma celo na +Y, proto +180 (jako V3S)
ROTATION_ANGLES = [(u + 180.0) % 360 for u in (225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0)]
KROK = {0: (0, -8), 1: (8, -4), 2: (16, 0), 3: (8, 4), 4: (0, 8), 5: (-8, 4), 6: (-16, 0), 7: (-8, -4)}

os.makedirs(VYSTUP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = False
scene.cycles.samples = SAMPLES
scene.cycles.filter_width = 1.5
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
scene.world.cycles_visibility.shadow = False

objs, model = model_rto.postav(scene, NATER)
mn = Vector((-model["sirka"] / 2, model["zad"], 0.0)); mx = Vector((model["sirka"] / 2, model["celo"], model["vyska"]))
stred = (mn + mx) / 2
stred_rozvoru = sum(model["napravy"]) / len(model["napravy"])
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "napravy", model["napravy"],
      "stred delky", round(stred.y, 3), "stred rozvoru", round(stred_rozvoru, 3), flush=True)

bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
for o in list(scene.objects):
    if o is gramofon or o.parent is not None: continue
    o.parent = gramofon; o.matrix_parent_inverse = gramofon.matrix_world.inverted()
body = {}
for jm, co in (("zem_stred", (stred.x, stred.y, mn.z)), ("zem_rozvor", (stred.x, stred_rozvoru, mn.z)),
               ("celo", (stred.x, mx.y, mn.z)), ("zad", (stred.x, mn.y, mn.z))):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=co); e = bpy.context.object
    e.parent = gramofon; e.matrix_parent_inverse = gramofon.matrix_world.inverted(); body[jm] = e

ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon

def na_pixel(obj):
    bpy.context.view_layer.update()
    p = world_to_camera_view(scene, cam, obj.matrix_world.translation)
    return (p.x * RAM, (1 - p.y) * RAM)

info = {"nater": NATER, "zin": ZIN, "px_m": PX_M, "ram": RAM, "delka_m": mx.y - mn.y, "stred_delky_y": stred.y,
        "stred_rozvoru_y": stred_rozvoru, "napravy_y": model["napravy"], "smery": {}}
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    b = {jm: na_pixel(e) for jm, e in body.items()}
    kx, ky = KROK[d]
    dopredu = (b["celo"][0] - b["zad"][0]) * kx + (b["celo"][1] - b["zad"][1]) * ky
    assert dopredu > 0, f"smer {d}: celo nemiri po smeru jizdy"
    info["smery"][d] = b
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, "zem pod stredem", [round(v, 2) for v in b["zem_stred"]], flush=True)
json.dump(info, open(os.path.join(VYSTUP, "kotvy.json"), "w"), indent=1)
print("hotovo")
