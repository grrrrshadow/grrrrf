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

# Okna (hrac 28. 9.: "ta modra, to vubec nesedi sedy okna, zkus jim udelat lepsi okna", "svetla bile bily"):
# material skla ma model nepruhledny a matny (drsnost 0,9), v jeho texture Image_3 jsou skla sede s prachem
# a v pravem dolnim rohu svetla (reflektor, odrazka, blinkr, zadni svetlo). OKNA=puvodni nechava model, jinak
# se skla prebarvi na tmavou barvu OKNA_BARVA, material je leskly (OKNA_DRSNOST) a reflektor sviti bile.
OKNA = os.environ.get("OKNA", "tmave")
if OKNA != "puvodni":
    img = {i.name: i for i in bpy.data.images}["Image_3"]
    w, h = img.size
    px = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(px); px = px.reshape(h, w, 4)
    yy, xx = np.mgrid[0:h, 0:w]
    yy = h - 1 - yy                                   # Blender ma radky odspodu, masky jsou v souradnicich obrazku
    svetla = (xx >= 283 * w // 512) & (yy >= 395 * h // 512)
    reflektor = ((xx - 322 * w / 512) ** 2 + (yy - 458 * h / 512) ** 2) <= (38 * w / 512) ** 2
    barva = np.array([float(c) for c in os.environ.get("OKNA_BARVA", "0.030,0.040,0.055").split(",")], np.float32)
    jas = px[..., :3].mean(axis=2, keepdims=True)
    sklo = ~svetla
    # tmave sklo, prach po okrajich (tmavsi mista textury) zustane naznaceny
    px[..., :3] = np.where(sklo[..., None], barva * (0.6 + 0.8 * jas), px[..., :3])
    px[..., :3] = np.where(reflektor[..., None], np.clip(px[..., :3] * 0.3 + 0.85, 0, 1), px[..., :3])
    img.pixels.foreach_set(px.ravel()); img.update()
    mat = bpy.data.materials["v3s_glass__da__spec"]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = float(os.environ.get("OKNA_DRSNOST", "0.15"))
    # reflektor sviti: emise jen tam, kde je v texture skoro bila (maska pres barvu)
    if os.environ.get("SVETLA", "bile") == "bile":
        nt = mat.node_tree
        tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tex.outputs["Color"], sep.inputs["Color"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.80; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        ramp.color_ramp.elements[1].position = 0.90; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        nt.links.new(sep.outputs["Blue"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = float(os.environ.get("SVETLA_SILA", "1.5"))
    print("okna", OKNA, "barva", barva, "drsnost", bsdf.inputs["Roughness"].default_value)

# ---------------------------------------------------------------- naklad na korbe
# Korba (namereno paprsky, korba.py): podlaha z = 0,264, uvnitr x +-1,095, y -3,842 az 0,163,
# podel boku lavice nahore z = 0,604.
PODLAHA, KX, KY0, KY1 = 0.264, 1.0, -3.80, 0.12
def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

def material(jmeno, tmava, svetla, drsnost, meritko=18.0):
    mat = bpy.data.materials.new(jmeno); mat.use_nodes = True
    n_ = mat.node_tree.nodes; l_ = mat.node_tree.links
    bsdf = n_["Principled BSDF"]
    sum_ = n_.new("ShaderNodeTexNoise"); sum_.inputs["Scale"].default_value = meritko; sum_.inputs["Detail"].default_value = 6.0
    rampa = n_.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].color = tmava; rampa.color_ramp.elements[1].color = svetla
    l_.new(sum_.outputs["Fac"], rampa.inputs["Fac"]); l_.new(rampa.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = drsnost
    return mat

def kupka(mat, hrubost=1.0, seed=7, vyska=0.78):
    """hromada uprostred korby, spicka 'vyska' m nad podlahou; hrubost = velikost hrudek"""
    import bmesh, random
    random.seed(seed)
    B = (KY1 - KY0) / 2; YS = (KY0 + KY1) / 2
    bm = bmesh.new(); NX, NY = 40, 80; vrch = {}
    hr = [[random.uniform(-1, 1) for _ in range(NY // 4 + 2)] for _ in range(NX // 4 + 2)]
    for i in range(NX + 1):
        for j in range(NY + 1):
            x = -KX + 2 * KX * i / NX; y = YS - B + 2 * B * j / NY
            s = max(0.0, 1 - (abs(x) / KX) ** 2.2 - (abs(y - YS) / B) ** 2.2)
            hrudka = hr[i // 4][j // 4] * 0.035 * max(0.0, hrubost - 0.7) * s
            z = PODLAHA + vyska * s ** 0.6 + (random.uniform(-0.04, 0.04) * s * hrubost if s > 0 else 0) + hrudka - 0.02
            vrch[i, j] = bm.verts.new((x, y, z))
    for i in range(NX):
        for j in range(NY):
            bm.faces.new((vrch[i, j], vrch[i + 1, j], vrch[i + 1, j + 1], vrch[i, j + 1]))
    me = bpy.data.meshes.new("kupka"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    ob = bpy.data.objects.new("kupka", me); scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return [ob]

def klady(seed=11):
    """klady podel korby: tri vrstvy, kura a svetla cela"""
    import random
    random.seed(seed)
    kura = material("kura", srgb((62, 45, 32)), srgb((112, 82, 56)), 0.9, 30.0)
    celo = material("celo", srgb((170, 135, 90)), srgb((215, 180, 125)), 0.8, 60.0)
    obs = []
    for vrstva, pocet in ((0, 5), (1, 4), (2, 3)):
        r = 0.17
        for k in range(pocet):
            x = (k - (pocet - 1) / 2) * 2 * r * 1.02
            z = PODLAHA + r + vrstva * r * 1.72
            dl = (KY1 - KY0) * random.uniform(0.9, 1.0)
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r * random.uniform(0.88, 1.05), depth=dl,
                                                location=(x, (KY0 + KY1) / 2 + random.uniform(-0.05, 0.05), z), rotation=(math.radians(90), 0, 0))
            o = bpy.context.object; o.data.materials.append(kura); o.data.materials.append(celo)
            for f in o.data.polygons:
                if abs(f.normal.z) > 0.9: f.material_index = 1      # cela valce (normala v souradnicich valce)
            obs.append(o)
    return obs

def prkna(seed=13):
    """hranice prken podel korby"""
    import random
    random.seed(seed)
    mat = material("prkna", srgb((165, 128, 84)), srgb((208, 172, 122)), 0.85, 40.0)
    obs = []
    for vrstva in range(10):                        # asi 0,5 m, aby bylo prkna videt i ze strany
        for k in range(8):
            w = 0.24; x = -KX + w / 2 + k * (2 * KX - w) / 7
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, (KY0 + KY1) / 2 + random.uniform(-0.03, 0.03),
                                                              PODLAHA + 0.025 + vrstva * 0.052))
            o = bpy.context.object; o.scale = (w * 0.96, (KY1 - KY0) * 0.97, 0.048)
            o.data.materials.append(mat); obs.append(o)
    return obs

# Naklady jako prikladaci vrstva (hrac 28. 9.: "kupku prikladaci, udelame cernou kupku uhli a zlutou pisek a vsechny
# barvy a drevo udelej"): nater "naklad_<KOD>" nafoti jen naklad, auto je neviditelne, ale zakryva, co je za
# bocnicemi (holdout). Stejna vrstva pak jde na vojenskou i vsechny odstiny modre.
#   kod: (tmava sRGB, svetla sRGB, drsnost povrchu, hrubost hrudek, meritko sumu)
NAKLAD = {
    "COAL": ((16, 16, 18), (58, 58, 62), 0.45, 1.3, 26), "COKE": ((48, 48, 50), (98, 95, 92), 0.8, 1.3, 26),
    "IORE": ((92, 44, 30), (152, 86, 60), 0.85, 1.2, 22), "LIME": ((158, 158, 148), (214, 214, 204), 0.9, 1.0, 20),
    "QLME": ((204, 204, 197), (242, 242, 236), 0.95, 0.8, 16), "SLAG": ((58, 54, 50), (110, 102, 95), 0.85, 1.2, 22),
    "SCMT": ((78, 54, 40), (150, 104, 74), 0.6, 1.5, 30), "GRVL": ((112, 109, 105), (172, 167, 160), 0.85, 1.2, 24),
    "SAND": ((184, 148, 88), (226, 196, 132), 0.95, 0.7, 14), "TATO": ((118, 84, 50), (176, 136, 90), 0.8, 1.6, 34),
    "SGBT": ((188, 168, 138), (232, 216, 186), 0.8, 1.6, 30), "SEED": ((158, 118, 58), (212, 172, 96), 0.9, 0.7, 16),
    "OLSD": ((44, 34, 27), (92, 72, 52), 0.7, 0.7, 16), "BEAN": ((172, 148, 98), (222, 196, 146), 0.8, 0.9, 20),
    "NUTS": ((118, 78, 44), (176, 126, 80), 0.8, 1.2, 24), "MARI": ((48, 98, 10), (94, 144, 26), 0.85, 1.0, 18),
    "SULP": ((196, 164, 28), (240, 214, 72), 0.85, 0.9, 18),      # sira pevna, zluta (FIRS ji ma jako tekutinu)
}
NAKLAD_KOD = NATER[len("naklad_"):] if NATER.startswith("naklad_") else None
if NAKLAD_KOD:
    for o in nove: o.is_holdout = True
    if NAKLAD_KOD == "WOOD": nalozeno = klady()
    elif NAKLAD_KOD == "WDPR": nalozeno = prkna()
    else:
        tm, sv, dr, hrub, mer = NAKLAD[NAKLAD_KOD]
        nalozeno = kupka(material("naklad", srgb(tm), srgb(sv), dr, mer), hrubost=hrub)
    koreny = koreny + nalozeno
    print("naklad", NAKLAD_KOD, "objektu", len(nalozeno))
elif KUPKA:
    # stara cela auta s kupkou marihuany (verze 2); od verze 3 je kupka prikladaci vrstva naklad_MARI
    mat = material("marihuana", (0.045, 0.12, 0.004, 1), (0.11, 0.27, 0.010, 1), 0.85)
    koreny = koreny + kupka(mat)
    print("kupka", round(PODLAHA + 0.78, 3), "m nahore")

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
