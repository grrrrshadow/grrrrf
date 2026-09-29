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
    "CORE": ((62, 74, 58), (114, 128, 100), 0.85, 1.2, 22),       # medena ruda, zelenosede (hrac 29. 9.: "medena ruda kupa")
}
def plachta(barva):
    """Plachta pres korbu (hrac 29. 9.: "co neni kupka, nech grafiku prazdne. udelame prikladaci plachtu. grafika
    stovky aut plny jednou plachtou. kdyz pojede plna, prilozime plachtu", "jidlo plachta"). Model ma na korbe klanice
    s hornim madlem (z do 1,29, vne x +-1,114, y -3,845 az 0,187), plachta je pres ne: boky svisle od horni hrany
    bocnic (0,64) kousek dolu, strecha 2,92 m nad zemi (vyska V3S s plachtou, kabina 2,46 m), podelne hrany zaoblene
    jako oblouky, celo u cela korby (kabina zacina az na y 0,64) a zadni stena rovne."""
    import bmesh
    tm, sv = PLACHTY[barva]
    mat = material("plachta", srgb(tm), srgb(sv), 0.95, 7.0)
    nt_ = mat.node_tree; bsdf = nt_.nodes["Principled BSDF"]
    vrasky = nt_.nodes.new("ShaderNodeTexNoise"); vrasky.inputs["Scale"].default_value = 3.0
    vrasky.inputs["Detail"].default_value = 4.0
    hrbol = nt_.nodes.new("ShaderNodeBump"); hrbol.inputs["Strength"].default_value = 0.25
    nt_.links.new(vrasky.outputs["Fac"], hrbol.inputs["Height"]); nt_.links.new(hrbol.outputs["Normal"], bsdf.inputs["Normal"])
    X, Y0, Y1 = 1.15, -3.88, 0.21                      # tesne vne klanic a madla
    Z0, Z1, R = 0.56, 2.92 + mn.z, 0.32                # boky kousek pres bocnice, strecha, polomer oblouku
    profil = [(-X, Z0)]
    for k in range(9):                                 # levy oblouk
        a = math.radians(180 - 90 * k / 8); profil.append((-X + R + R * math.cos(a), Z1 - R + R * math.sin(a)))
    for k in range(9):                                 # pravy oblouk
        a = math.radians(90 - 90 * k / 8); profil.append((X - R + R * math.cos(a), Z1 - R + R * math.sin(a)))
    profil.append((X, Z0))
    bm = bmesh.new()
    predni = [bm.verts.new((x, Y1, z)) for x, z in profil]
    zadni = [bm.verts.new((x, Y0, z)) for x, z in profil]
    for i in range(len(profil) - 1):
        bm.faces.new((zadni[i], zadni[i + 1], predni[i + 1], predni[i]))
    bm.faces.new(predni[::-1]); bm.faces.new(zadni)    # celo a zadni stena
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("plachta"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("plachta", me); scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return [ob]

# Barvy plachty (hrac 29. 9.: "vojensky vojenskou plachtu, a sedou", "modry zlutou sedobilou plachtu"):
#   jmeno: (tmava sRGB, svetla sRGB)
PLACHTY = {"vojenska": ((58, 64, 40), (100, 106, 70)), "seda": ((86, 88, 86), (136, 138, 134)),
           "zluta": ((168, 136, 36), (224, 190, 74)), "sedobila": ((168, 168, 160), (222, 222, 214)),
           "rezna": ((170, 160, 128), (220, 212, 178))}

# ---------------------------------------------------------------- kusovy naklad (verze 5)
# Hrac 29. 9.: "si rikal, ze cement das do pytlu", "zbozi bedny, alkohol sudy", "zviratka, muze se jmenovat v3s
# prasatka, vozit grafiku s prasatkama a na pozadi pobezi kod dobytek normalne", "dalsi jmeno v3s dobytek a
# kravicky, po prestavbe", "rostlinna vlakna jako plnou sena, misto plachty seno".
def kvadr(mat, x, y, z, sx, sy, sz, rot=0.0, zaobleni=0.0):
    """kvadr se stredem (x, y, z) a rozmery sx, sy, sz (m), natoceny o rot (rad) kolem svisle osy, hrany zaoblene"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z), rotation=(0, 0, rot))
    o = bpy.context.object; o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if zaobleni > 0:
        b = o.modifiers.new("zaobleni", 'BEVEL'); b.width = zaobleni; b.segments = 3; b.limit_method = 'NONE'
    o.data.materials.append(mat)
    return o

def pytle(seed=17):
    """Pytle cementu (hrac 29. 9.: "cement uplne zrus a zacni znova pytle pekne, nic sediviho. bile pytle"): bile papirove
    pytle 50 kg (asi 60 x 40 x 14 cm), bricha naducana, ve vazbe jako na palete (vrstvy stridave podel a napric),
    pet vrstev, horni nedoskladana."""
    import bmesh, random
    random.seed(seed)
    mat = material("pytle", srgb((232, 230, 222)), srgb((252, 251, 247)), 0.9, 30.0)
    nt_ = mat.node_tree; bsdf = nt_.nodes["Principled BSDF"]
    papir = nt_.nodes.new("ShaderNodeTexNoise"); papir.inputs["Scale"].default_value = 45.0
    hrbol = nt_.nodes.new("ShaderNodeBump"); hrbol.inputs["Strength"].default_value = 0.15
    nt_.links.new(papir.outputs["Fac"], hrbol.inputs["Height"]); nt_.links.new(hrbol.outputs["Normal"], bsdf.inputs["Normal"])
    D, S, V = 0.60, 0.40, 0.14                     # delka, sirka, vyska pytle
    def pytel(x, y, z, podel, rot):
        """naducany pytel: kvadr s velkym zaoblenim, vrch a spodek vyboulene"""
        sx, sy = (S, D) if podel else (D, S)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z), rotation=(0, 0, rot))
        o = bpy.context.object; o.scale = (sx * 0.97, sy * 0.97, V)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        sub = o.modifiers.new("oblost", 'SUBSURF'); sub.levels = 2; sub.render_levels = 2
        o.data.materials.append(mat)
        return o
    obs = []
    dx, dy = 2 * KX - 0.06, KY1 - KY0 - 0.08       # vnitrek korby
    for vrstva in range(5):
        podel = vrstva % 2 == 0
        sx, sy = (S, D) if podel else (D, S)
        nx, ny = int(dx // sx), int(dy // sy)
        for i in range(nx):
            for j in range(ny):
                if vrstva == 4 and random.random() < 0.4: continue
                x = -KX + 0.03 + (dx - nx * sx) / 2 + (i + 0.5) * sx + random.uniform(-0.015, 0.015)
                y = KY0 + 0.04 + (dy - ny * sy) / 2 + (j + 0.5) * sy + random.uniform(-0.015, 0.015)
                obs.append(pytel(x, y, PODLAHA + V / 2 + vrstva * V * 0.92, podel, math.radians(random.uniform(-2, 2))))
    return obs

def bedny(seed=19):
    """dřevěné bedny se zbozim ve dvou vrstvach, horni nedoskladana"""
    import random
    random.seed(seed)
    svetla = material("bedny", srgb((156, 118, 74)), srgb((200, 162, 110)), 0.85, 10.0)
    tmava = material("bedny_tmave", srgb((120, 88, 52)), srgb((160, 124, 80)), 0.85, 10.0)
    obs = []
    for vrstva, (nx, ny, v, z0) in enumerate(((3, 5, 0.60, 0.0), (3, 4, 0.50, 0.60))):
        dx, dy = (2 * KX - 0.08) / nx, (KY1 - KY0 - 0.12) / ny
        for i in range(nx):
            for j in range(ny):
                if vrstva == 1 and random.random() < 0.3: continue
                sx, sy, sz = dx * random.uniform(0.86, 0.95), dy * random.uniform(0.84, 0.95), v * random.uniform(0.85, 1.0)
                x = -KX + 0.04 + (i + 0.5) * dx + random.uniform(-0.02, 0.02)
                y = KY0 + 0.06 + (j + 0.5) * dy + random.uniform(-0.02, 0.02)
                obs.append(kvadr(random.choice((svetla, svetla, tmava)), x, y, PODLAHA + z0 + sz / 2, sx, sy, sz,
                                 math.radians(random.uniform(-3, 3)), 0.015))
    return obs

# Sudy (hrac 29. 9.: "alkohol sudy", "vojenska seda plachta vsechny benziny, ropu, tak udelej sudy, jako ze veze.
# protoze ropa je v kazdy hre v zakladnim prumyslu, tak to musi nejak vozit", "vodu vozit v sudech, modry sudy
# a cerny sudy"): drevene pivni sudy s brichem, plechove sudy 200 l modre (voda) a cerne (ropa a benzin).
#   druh: (tmava sRGB, svetla sRGB, drsnost, polomer, vyska, bricho, vysky obruci)
SUDY = {"drevo": ((104, 66, 36), (150, 102, 60), 0.8, 0.27, 0.80, 0.12, (0.05, 0.89)),
        "bile": ((212, 210, 202), (246, 245, 240), 0.45, 0.29, 0.88, 0.0, (0.3, 0.64)),     # hrac: "zadne modre sudy,
                                                                                           # modre budou bile"
        "cerne": ((16, 16, 18), (46, 46, 50), 0.4, 0.29, 0.88, 0.0, (0.3, 0.64)),
        "cervene": ((132, 26, 20), (184, 48, 38), 0.45, 0.29, 0.88, 0.0, (0.3, 0.64))}   # hrac: "prostě udělej i tekutiny, barevný sudy"

def sudy(druh="drevo", seed=23):
    """sudy nastojato, tri rady po sesti; drevene s brichem a zeleznymi obrucemi, plechove rovne s dvema prolisy"""
    import bmesh, random
    random.seed(seed)
    tm, sv, dr, R, V, bricho, obruce = SUDY[druh]
    drevo = material("sudy_" + druh, srgb(tm), srgb(sv), dr, 16.0)
    zelezo = (material("obruce", srgb((34, 34, 36)), srgb((64, 64, 66)), 0.45, 30.0) if druh == "drevo" else
              material("prolisy_" + druh, srgb(tuple(int(c * 0.75) for c in tm)), srgb(tuple(int(c * 0.8) for c in sv)), dr, 16.0))
    K = 16
    vysky = sorted({0, 0.3, 0.5, 0.7, 1.0} | {o for o in obruce} | {o + 0.06 for o in obruce})
    obs = []
    for x in (-0.7, 0.0, 0.7):
        for j in range(6):
            y = KY0 + 0.4 + j * (KY1 - KY0 - 0.8) / 5
            bm = bmesh.new(); kruhy = []
            for h in vysky:
                r = R * (1 - bricho + bricho * math.sin(math.pi * h))
                if druh != "drevo" and any(o <= h <= o + 0.06 for o in obruce): r *= 1.03              # prolis
                kruhy.append([bm.verts.new((r * math.cos(2 * math.pi * k / K), r * math.sin(2 * math.pi * k / K), h * V))
                              for k in range(K)])
            for i in range(len(vysky) - 1):
                for k in range(K):
                    f = bm.faces.new((kruhy[i][k], kruhy[i][(k + 1) % K], kruhy[i + 1][(k + 1) % K], kruhy[i + 1][k]))
                    if any(abs(vysky[i] - o) < 1e-9 for o in obruce): f.material_index = 1      # obruce, prolisy
            bm.faces.new(kruhy[-1]); bm.faces.new(kruhy[0][::-1])
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new("sud"); bm.to_mesh(me); bm.free()
            o = bpy.data.objects.new("sud", me); scene.collection.objects.link(o)
            o.location = (x + random.uniform(-0.03, 0.03), y + random.uniform(-0.03, 0.03), PODLAHA)
            o.data.materials.append(drevo); o.data.materials.append(zelezo)
            obs.append(o)
    return obs

def material_strakaty(jmeno, bila, hneda, meritko=3.0):
    """strakata srst: skvrny (noise, ostry prah) hneda na bile"""
    mat = bpy.data.materials.new(jmeno); mat.use_nodes = True
    n_ = mat.node_tree.nodes; l_ = mat.node_tree.links
    bsdf = n_["Principled BSDF"]
    sum_ = n_.new("ShaderNodeTexNoise"); sum_.inputs["Scale"].default_value = meritko; sum_.inputs["Detail"].default_value = 2.0
    rampa = n_.new("ShaderNodeValToRGB"); rampa.color_ramp.interpolation = 'CONSTANT'
    rampa.color_ramp.elements[0].color = hneda
    rampa.color_ramp.elements[1].position = 0.5; rampa.color_ramp.elements[1].color = bila
    l_.new(sum_.outputs["Fac"], rampa.inputs["Fac"]); l_.new(rampa.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    return mat

def zvire_koren(x, y, a):
    """prazdny objekt, ke kteremu se prichyti dily zvirete v jeho vlastnich souradnicich (hlava na +y)"""
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(x, y, PODLAHA), rotation=(0, 0, a))
    return bpy.context.object

def dil(koren, o, mat):
    o.data.materials.append(mat); o.parent = koren          # matrix_parent_inverse zustava jednotkova
    return o

def prase(x, y, a, kuze, rypak):
    koren = zvire_koren(x, y, a)
    L, W, H, N = 0.48, 0.25, 0.24, 0.20                        # pul delky, pul sirky, pul vysky tela, nohy
    zt = N + H
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1, location=(0, 0, zt))
    t = dil(koren, bpy.context.object, kuze); t.scale = (W, L, H)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.16, location=(0, L + 0.05, zt + 0.05))
    dil(koren, bpy.context.object, kuze)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.07, depth=0.1, location=(0, L + 0.2, zt + 0.02),
                                        rotation=(math.radians(90), 0, 0))
    dil(koren, bpy.context.object, rypak)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.065, radius2=0.0, depth=0.12,
                                        location=(sx * 0.09, L + 0.02, zt + 0.19), rotation=(math.radians(-30), sx * math.radians(25), 0))
        dil(koren, bpy.context.object, kuze)
        for sy in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.05, depth=N + 0.06, location=(sx * W * 0.55, sy * L * 0.55, (N + 0.06) / 2))
            dil(koren, bpy.context.object, kuze)
    return koren

def prasata(seed=29):
    """prasatka (dobytek, podtyp 0): tri sloupce po trech, hlavou dopredu i dozadu"""
    import random
    random.seed(seed)
    kuze = material("prase", srgb((212, 148, 140)), srgb((240, 186, 178)), 0.7, 14.0)
    rypak = material("rypak", srgb((186, 106, 106)), srgb((208, 128, 126)), 0.6, 30.0)
    obs = []
    for x0 in (-0.7, 0.0, 0.7):
        for j in range(3):
            y = KY0 + 0.7 + j * (KY1 - KY0 - 1.4) / 2 + random.uniform(-0.08, 0.08)
            a = random.choice((0.0, math.pi)) + random.uniform(-0.25, 0.25)
            obs.append(prase(x0 + random.uniform(-0.05, 0.05), y, a, kuze, rypak))
    return obs

def krava(x, y, a, srst, tmava, rohy):
    koren = zvire_koren(x, y, a)
    L, W, H, N = 0.62, 0.26, 0.29, 0.46                        # jalovicka: telo 1,25 m, nohy 0,46 m
    zt = N + H
    dil(koren, kvadr(srst, 0, 0, zt, 2 * W, 2 * L, 2 * H, 0.0, 0.12), srst)    # kvadr uz material ma, dil ho jen prichyti
    koren_hlava = (0, L + 0.16, zt + 0.12)
    o = kvadr(srst, koren_hlava[0], koren_hlava[1], koren_hlava[2], 0.22, 0.40, 0.24, 0.0, 0.06)
    o.rotation_euler = (math.radians(-25), 0, 0); o.parent = koren
    o = kvadr(tmava, 0, L + 0.36, zt + 0.02, 0.17, 0.10, 0.14, 0.0, 0.03); o.parent = koren       # cumak
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, radius2=0.0, depth=0.12,
                                        location=(sx * 0.10, L + 0.12, zt + 0.28), rotation=(0, sx * math.radians(60), 0))
        dil(koren, bpy.context.object, rohy)
        o = kvadr(srst, sx * 0.15, L + 0.14, zt + 0.2, 0.12, 0.04, 0.07, 0.0, 0.01); o.parent = koren       # ucho
        for sy in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=N + 0.08, location=(sx * W * 0.6, sy * L * 0.7, (N + 0.08) / 2))
            dil(koren, bpy.context.object, srst)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.5, location=(0, -L - 0.02, zt - 0.1))
    dil(koren, bpy.context.object, tmava)                                                        # ocas
    return koren

def kravy(seed=37):
    """kravicky (dobytek, podtyp 1): ceska strakata, dve rady po dvou"""
    import random
    random.seed(seed)
    srst = material_strakaty("krava", srgb((236, 230, 220)), srgb((150, 72, 42)), 3.0)
    tmava = material("cumak", srgb((70, 50, 44)), srgb((100, 76, 66)), 0.6, 20.0)
    rohy = material("rohy", srgb((200, 190, 168)), srgb((230, 222, 200)), 0.5, 20.0)
    obs = []
    for x0 in (-0.5, 0.5):
        for j in range(2):
            y = KY0 + 1.0 + j * (KY1 - KY0 - 2.0) + random.uniform(-0.08, 0.08)
            a = random.choice((0.0, math.pi)) + random.uniform(-0.15, 0.15)
            obs.append(krava(x0 + random.uniform(-0.04, 0.04), y, a, srst, tmava, rohy))
    return obs

def ovce_kus(x, y, a, vlna, hlava):
    koren = zvire_koren(x, y, a)
    L, W, H, N = 0.42, 0.25, 0.24, 0.26                        # ovce: telo 0,85 m, huňaté, nohy 0,26 m
    zt = N + H
    bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=9, radius=1, location=(0, 0, zt))
    t = dil(koren, bpy.context.object, vlna); t.scale = (W, L, H)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=1, location=(0, L + 0.08, zt + 0.1))
    hl = dil(koren, bpy.context.object, hlava); hl.scale = (0.09, 0.14, 0.1)
    for sx in (-1, 1):
        o = kvadr(hlava, sx * 0.1, L + 0.04, zt + 0.16, 0.1, 0.03, 0.04, 0.0, 0.01); o.parent = koren      # ucho
        for sy in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.035, depth=N + 0.06, location=(sx * W * 0.5, sy * L * 0.55, (N + 0.06) / 2))
            dil(koren, bpy.context.object, hlava)
    return koren

def ovce(seed=53):
    """ovečky (dobytek, podtyp 2; hrac 29. 9.: "ovce tam jsou"): bila vlna, tmava hlava a nohy, tri sloupce po ctyrech"""
    import random
    random.seed(seed)
    vlna = material("vlna", srgb((206, 200, 184)), srgb((238, 234, 222)), 0.95, 40.0)
    nt_ = vlna.node_tree; bsdf = nt_.nodes["Principled BSDF"]
    kudrny = nt_.nodes.new("ShaderNodeTexNoise"); kudrny.inputs["Scale"].default_value = 60.0
    hrbol = nt_.nodes.new("ShaderNodeBump"); hrbol.inputs["Strength"].default_value = 0.8
    nt_.links.new(kudrny.outputs["Fac"], hrbol.inputs["Height"]); nt_.links.new(hrbol.outputs["Normal"], bsdf.inputs["Normal"])
    hlava = material("hlava_ovce", srgb((40, 34, 30)), srgb((70, 60, 54)), 0.7, 20.0)
    obs = []
    for x0 in (-0.7, 0.0, 0.7):
        for j in range(4):
            y = KY0 + 0.55 + j * (KY1 - KY0 - 1.1) / 3 + random.uniform(-0.06, 0.06)
            a = random.choice((0.0, math.pi)) + random.uniform(-0.3, 0.3)
            obs.append(ovce_kus(x0 + random.uniform(-0.05, 0.05), y, a, vlna, hlava))
    return obs

# Barvy sena (hrac 29. 9.: "rostlina vlakna livery jako ovecky prasatka. marihuanove seno zeleny z grafiky rostlina
# vlakna a seno taky jako rostlina vlakna ale zlutejsi"): stejna kupa, jina barva.
SENO = {"vlakna": ((168, 142, 72), (218, 196, 118)), "mari": ((66, 104, 26), (116, 156, 52)),
        "zlute": ((208, 176, 42), (250, 226, 96))}

def seno(barva="vlakna", seed=31):
    """naložené seno: kupa pres bocnice, nahore zakulacena, 1,65 m nad podlahou"""
    import bmesh, random
    random.seed(seed)
    tm, sv = SENO[barva]
    mat = material("seno_" + barva, srgb(tm), srgb(sv), 0.95, 70.0)
    nt_ = mat.node_tree; bsdf = nt_.nodes["Principled BSDF"]
    stebla = nt_.nodes.new("ShaderNodeTexNoise"); stebla.inputs["Scale"].default_value = 90.0
    stebla.inputs["Detail"].default_value = 8.0
    hrbol = nt_.nodes.new("ShaderNodeBump"); hrbol.inputs["Strength"].default_value = 0.6
    nt_.links.new(stebla.outputs["Fac"], hrbol.inputs["Height"]); nt_.links.new(hrbol.outputs["Normal"], bsdf.inputs["Normal"])
    X, Y0, Y1, V = KX + 0.12, KY0 - 0.05, KY1 + 0.03, 1.45
    B, YS = (Y1 - Y0) / 2, (Y0 + Y1) / 2
    bm = bmesh.new(); NX, NY = 30, 60; vrch = {}
    hr = [[random.uniform(-1, 1) for _ in range(NY // 5 + 2)] for _ in range(NX // 5 + 2)]      # hrboly po naloženi
    def hrbol(i, j):
        a, b = i / 5, j / 5; i0, j0 = int(a), int(b); fa, fb = a - i0, b - j0
        return ((hr[i0][j0] * (1 - fa) + hr[i0 + 1][j0] * fa) * (1 - fb) + (hr[i0][j0 + 1] * (1 - fa) + hr[i0 + 1][j0 + 1] * fa) * fb)
    for i in range(NX + 1):
        for j in range(NY + 1):
            x = -X + 2 * X * i / NX; y = YS - B + 2 * B * j / NY
            s = max(0.0, 1 - (abs(x) / X) ** 5 - (abs(y - YS) / B) ** 6)
            z = (PODLAHA + 0.2 + V * s ** 0.3 + 0.10 * hrbol(i, j) * s ** 0.5 +
                 (random.uniform(-0.03, 0.03) if s > 0 else 0.0))
            vrch[i, j] = bm.verts.new((x, y, z))
    for i in range(NX):
        for j in range(NY):
            bm.faces.new((vrch[i, j], vrch[i + 1, j], vrch[i + 1, j + 1], vrch[i, j + 1]))
    me = bpy.data.meshes.new("seno"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    ob = bpy.data.objects.new("seno", me); scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return [ob]

KUSOVE = {"CMNT": pytle, "GOOD": bedny, "BEER": sudy, "sudy_bile": lambda: sudy("bile", 41),
          "sudy_cerne": lambda: sudy("cerne", 43), "sudy_cervene": lambda: sudy("cervene", 47),
          "LVST": prasata, "kravy": kravy, "ovce": ovce, "FICR": seno,
          "seno_mari": lambda: seno("mari"), "seno_zlute": lambda: seno("zlute")}

NAKLAD_KOD = NATER[len("naklad_"):] if NATER.startswith("naklad_") else None
if NAKLAD_KOD:
    for o in nove: o.is_holdout = True
    if NAKLAD_KOD == "WOOD": nalozeno = klady()
    elif NAKLAD_KOD == "WDPR": nalozeno = prkna()
    elif NAKLAD_KOD.startswith("plachta_"): nalozeno = plachta(NAKLAD_KOD[len("plachta_"):])
    elif NAKLAD_KOD in KUSOVE: nalozeno = KUSOVE[NAKLAD_KOD]()
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
