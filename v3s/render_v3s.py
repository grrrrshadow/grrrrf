# -*- coding: utf-8 -*-
# Foceni Pragy V3S pro OpenTTD (silnicni vozidlo). Kamera, HDRI a Cycles jako render_sergej.py
# (z hracova glb3BBC.py): ortho, 30 stupnu nad obzorem, azimut 45 stupnu, snow.exr bez stinu.
# Silnicni vozidla se na rovne silnici nestlacuji (jedna osmina = 1 jednotka mapy ve vsech smerech jizdy),
# takze vsech 8 smeru je ve stejnem meritku.
#   python3 render_v3s.py <vojenska|modra_A|modra_B|modra_C|modra_D>[_kupka] <px_na_m> <vystup>
# Vystup: d0-d7.png (smery jako vycet Direction: N, NE, E, SE, S, SW, W, NW) a kotvy.json, kde je pro kazdy
# smer promitnuty bod na zemi pod stredem auta (pul delky, pul sirky) a pod stredem rozvoru.
import bpy, os, sys, math, json
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import nater_v3s

NATER, PX_M, VYSTUP = sys.argv[-3], float(sys.argv[-2]), sys.argv[-1]
MODEL = os.path.join(TU, "model", "praga-v3s.glb")
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = 256                         # ctverec rendru v px (zin4)
SAMPLES = int(os.environ.get("SAMPLES", "256"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
# Uhly z render_sergej.py pocitaji s celem modelu na -Y. V3S ma kabinu na +Y, proto +180.
ROTATION_ANGLES = [(u + 180.0) % 360 for u in (225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0)]
# posun na obrazovce pri jizde o jednotku ve smeru d (RemapCoords, zin4): cim musi auto koukat
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

pred = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=MODEL)
nove = list(set(scene.objects) - pred)
koreny = [o for o in nove if o.parent is None]
meshe = [o for o in nove if o.type == 'MESH']
pts = [o.matrix_world @ v.co for o in meshe for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
# napravy: stredy kol (predni jedna naprava, zadni tandem)
ys = []
for o in meshe:
    if o.name.startswith("wheel") and "koloint02" in o.name:
        p = [o.matrix_world @ v.co for v in o.data.vertices]
        ys.append(round((min(q.y for q in p) + max(q.y for q in p)) / 2, 2))
ys = sorted(set(ys))
predni_naprava = max(ys); zadni = [y for y in ys if y < 0]
stred_rozvoru = (predni_naprava + sum(zadni) / len(zadni)) / 2
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "napravy", ys,
      "stred delky", round(stred.y, 3), "stred rozvoru", round(stred_rozvoru, 3))

KUPKA = NATER.endswith("_kupka")                  # zelena kupka marihuany na korbe (hrac 28. 9.)
NATER_LAK = NATER[:-len("_kupka")] if KUPKA else NATER
if NATER_LAK.startswith("modra_"):
    obr = {img.name: img for img in bpy.data.images}
    def cti(img):
        w, h = img.size
        px = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(px)
        px = px.reshape(h, w, 4)
        return px, (np.flipud(px[..., :3]) * 255 + 0.5).astype(np.uint8)   # Blender ma radky odspodu
    _, kab = cti(obr["Image_1"])
    print("jas laku", round(nater_v3s.nastav_ref(kab), 1))
    for jm in ("Image_0", "Image_1", "Image_2"):
        img = obr[jm]; px, rgb = cti(img)
        px[..., :3] = np.flipud(nater_v3s.modra(jm, rgb, NATER_LAK[-1])).astype(np.float32) / 255
        img.pixels.foreach_set(px.ravel()); img.update()
        print("prebarveno", jm)

if KUPKA:
    # Korba (namereno paprsky, korba.py): podlaha z = 0,264, uvnitr x +-1,095, y -3,842 az 0,163,
    # podel boku lavice nahore z = 0,604. Kupka: hromada uprostred, spicka 0,78 m nad podlahou.
    import bmesh, random
    random.seed(7)
    PODLAHA, A, Y0, Y1, VYSKA = 0.264, 1.0, -3.80, 0.12, 0.78
    B = (Y1 - Y0) / 2; YS = (Y0 + Y1) / 2
    bm = bmesh.new()
    NX, NY = 40, 80
    vrch = {}
    for i in range(NX + 1):
        for j in range(NY + 1):
            x = -A + 2 * A * i / NX; y = YS - B + 2 * B * j / NY
            s = max(0.0, 1 - (abs(x) / A) ** 2.2 - (abs(y - YS) / B) ** 2.2)
            z = PODLAHA + VYSKA * s ** 0.6 + (random.uniform(-0.04, 0.04) * s if s > 0 else 0) - 0.02
            vrch[i, j] = bm.verts.new((x, y, z))
    for i in range(NX):
        for j in range(NY):
            bm.faces.new((vrch[i, j], vrch[i + 1, j], vrch[i + 1, j + 1], vrch[i, j + 1]))
    me = bpy.data.meshes.new("kupka"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    kupka = bpy.data.objects.new("kupka", me); scene.collection.objects.link(kupka)
    mat = bpy.data.materials.new("marihuana"); mat.use_nodes = True
    mn_ = mat.node_tree.nodes; ml = mat.node_tree.links
    bsdf = mn_["Principled BSDF"]
    sum_ = mn_.new("ShaderNodeTexNoise"); sum_.inputs["Scale"].default_value = 18.0; sum_.inputs["Detail"].default_value = 6.0
    rampa = mn_.new("ShaderNodeValToRGB")
    # zelen jako herni marihuana (vagony-mari: prumer 90, 137, 22 v sRGB)
    rampa.color_ramp.elements[0].color = (0.045, 0.12, 0.004, 1)     # tmave listi
    rampa.color_ramp.elements[1].color = (0.11, 0.27, 0.010, 1)      # svetle listi
    ml.new(sum_.outputs["Fac"], rampa.inputs["Fac"]); ml.new(rampa.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.85
    kupka.data.materials.append(mat)
    koreny = koreny + [kupka]
    print("kupka", round(PODLAHA + VYSKA, 3), "m nahore")

bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
for k in koreny:
    k.parent = gramofon; k.matrix_parent_inverse = gramofon.matrix_world.inverted()
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

info = {"nater": NATER, "px_m": PX_M, "ram": RAM, "delka_m": mx.y - mn.y, "stred_delky_y": stred.y,
        "stred_rozvoru_y": stred_rozvoru, "napravy_y": ys, "smery": {}}
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    b = {jm: na_pixel(e) for jm, e in body.items()}
    kx, ky = KROK[d]
    dopredu = (b["celo"][0] - b["zad"][0]) * kx + (b["celo"][1] - b["zad"][1]) * ky
    assert dopredu > 0, f"smer {d}: kabina nemiri po smeru jizdy"
    info["smery"][d] = b
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, "zem pod stredem", [round(v, 2) for v in b["zem_stred"]], flush=True)
json.dump(info, open(os.path.join(VYSTUP, "kotvy.json"), "w"), indent=1)
print("hotovo")
