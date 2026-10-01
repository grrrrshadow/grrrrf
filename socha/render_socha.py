# -*- coding: utf-8 -*-
# Socha Karla Máchy na 1 policko (hrac 1. 10.: "udelej Karel Macha statue, policko 1x1 sochu uprostred, sedou
# z kamene a bronzovou, karel macha bude mit kapucu, vousy a obrovskyho dzonta v ruce, ruce bude mit od sebe jako by
# se chystal obejmout neco velkyho, okolo lavicky, male krovicko, odpadak, odpadky").
# Vlastni model, kamera, meritko, svetlo a stin jako automat (automat/render_automat.py), vsechno dvakrat vetsi
# (MERITKO 2) jako automat, at to k sobe sedi.
#   python3 render_socha.py <vystup.png>          SOCHA=kamen (sediva z kamene) nebo SOCHA=bronz
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu policka; skupina je
# navrzena ve skutecne velikosti kolem stredu policka C a zvetsi se K krat.
# Postava stoji na podstavci cela k divakovi (k jihu), aby roztazene ruce byly na obrazku vodorovne: mikina s kapuci
# na hlave, plnovous, ruce dopredu od sebe jako k objeti, v prave ruce obrovsky joint. Telo je kostra s modifikatorem
# Skin a vyhlazenim, takze je hladke jako tesane nebo lite.
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image

VYSTUP = sys.argv[-1]
PX_M = 12.2
RAM = 384
K = float(os.environ.get("MERITKO", "2"))
SOCHA = os.environ.get("SOCHA", "kamen")
T = 256 / (math.sqrt(2) * PX_M)               # policko 14,84 m
C = T / 2
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
PISMO = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- scena jako automat
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = int(os.environ.get("SAMPLES", "128"))
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
scene.world.cycles_visibility.shadow = True
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.35"))

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

def mat(jmeno, rgb, drsnost=0.8, kov=0.0, sum_=0.0, meritko=2.0):
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if sum_:
        tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = meritko; tex.inputs["Detail"].default_value = 6.0
        ramp = t.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = srgb(tuple(max(0, v * (1 - sum_)) for v in rgb))
        ramp.color_ramp.elements[1].color = srgb(tuple(min(255, v * (1 + sum_)) for v in rgb))
        t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    return m

def bronz():
    """bronz s patinou: kov, ve zlabech a dole zelenava patina (sum), vyleštěne misto se dela zvlast"""
    m = bpy.data.materials.new("bronz"); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = 6.0; tex.inputs["Detail"].default_value = 8.0
    ramp = t.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = srgb((112, 78, 44))
    ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = srgb((74, 122, 100))
    t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Metallic"].default_value = 0.85; b.inputs["Roughness"].default_value = 0.42
    return m

M = {
    "podstavec": mat("podstavec", (126, 124, 120), 0.85, sum_=0.12, meritko=14.0),       # zula
    "deska": mat("deska", (112, 80, 46), 0.4, kov=0.9),                                  # bronzova deska se jmenem
    "pismo": mat("pismo", (186, 150, 96), 0.3, kov=1.0),
    "dlazba": mat("dlazba", (176, 172, 164), 0.9, sum_=0.07, meritko=6.0),
    "spara": mat("spara", (136, 132, 124), 0.95),
    "obrubnik": mat("obrubnik", (150, 146, 138), 0.9, sum_=0.06, meritko=8.0),
    "lavicka": mat("lavicka", (138, 92, 52), 0.7),
    "kov": mat("kov", (52, 58, 54), 0.5, kov=0.5),
    "ker": mat("ker", (54, 98, 40), 0.9, sum_=0.32, meritko=9.0),
    "ker2": mat("ker2", (70, 108, 44), 0.9, sum_=0.3, meritko=9.0),
    "kos": mat("kos", (38, 70, 46), 0.5, kov=0.3),
    "cerna": mat("cerna", (14, 14, 14), 0.9),
}
M["socha"] = bronz() if SOCHA == "bronz" else mat("socha", (178, 176, 170), 0.9, sum_=0.08, meritko=10.0)
ODPAD = {"papir": [mat(f"papir{i}", c, 0.9) for i, c in enumerate([(236, 234, 226), (214, 206, 186), (200, 200, 204)])],
         "plech": [mat(f"plech{i}", c, 0.35, kov=0.6) for i, c in enumerate([(196, 30, 34), (190, 192, 196), (36, 80, 170), (40, 140, 60)])],
         "lahev": [mat(f"lahev{i}", c, 0.2) for i, c in enumerate([(160, 196, 214), (70, 140, 70), (120, 80, 40)])],
         "kelimek": [mat(f"kelimek{i}", c, 0.7) for i, c in enumerate([(240, 240, 236), (150, 100, 60)])],
         "sacek": [mat(f"sacek{i}", c, 0.6) for i, c in enumerate([(232, 232, 232), (60, 90, 170), (30, 30, 30)])],
         "balicek": [mat("balicek", (96, 200, 58), 0.5)]}

SITE = {}
def bm_pro(m):
    if m.name not in SITE: SITE[m.name] = (m, bmesh.new())
    return SITE[m.name][1]

def B(x, y, z):
    """skupina -> Blender: navrzeno kolem stredu policka C ve skutecne velikosti, zvetseno K krat"""
    return Vector((C + (y - C) * K, -(C + (x - C) * K), z * K))

def kvadr(m, x0, x1, y0, y1, z0, z1):
    bm = bm_pro(m)
    v = [bm.verts.new(B(x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        bm.faces.new([v[i] for i in f])

def mnohostena(m, body, steny):
    bm = bm_pro(m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])

def valec(m, x, y, z0, z1, r, n=16):
    bm = bm_pro(m)
    dole = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z0)) for k in range(n)]
    nahore = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z1)) for k in range(n)]
    bm.faces.new(dole[::-1]); bm.faces.new(nahore)
    for k in range(n):
        bm.faces.new((dole[k], dole[(k + 1) % n], nahore[(k + 1) % n], nahore[k]))

# ---------------------------------------------------------------- dlazba, podstavec, lavicky, kos, kere, odpadky
# namesticko 5,6 x 5,6 m z dlazdic 50 cm s obrubnikem, kolem trava hry
D0, D1, OBR, Z_D = C - 2.8, C + 2.8, 0.15, 0.03
for (x0, x1, y0, y1) in ((D0, D1, D0, D0 + OBR), (D0, D1, D1 - OBR, D1), (D0, D0 + OBR, D0 + OBR, D1 - OBR), (D1 - OBR, D1, D0 + OBR, D1 - OBR)):
    kvadr(M["obrubnik"], x0, x1, y0, y1, 0.0, Z_D + 0.03)
kvadr(M["spara"], D0 + OBR, D1 - OBR, D0 + OBR, D1 - OBR, 0.0, Z_D - 0.004)
n_ = int(round((D1 - D0 - 2 * OBR) / 0.5)); kr = (D1 - D0 - 2 * OBR) / n_
for i in range(n_):
    for j in range(n_):
        x, y = D0 + OBR + kr * i, D0 + OBR + kr * j
        kvadr(M["dlazba"], x + 0.012, x + kr - 0.012, y + 0.012, y + kr - 0.012, 0.0, Z_D)

# podstavec ze zuly: schod, kvadr, rimsa; na prednich stenach bronzova deska se jmenem
Z_PODST = 1.4
kvadr(M["podstavec"], C - 0.85, C + 0.85, C - 0.85, C + 0.85, 0.0, 0.25)
kvadr(M["podstavec"], C - 0.6, C + 0.6, C - 0.6, C + 0.6, 0.25, 1.27)
kvadr(M["podstavec"], C - 0.7, C + 0.7, C - 0.7, C + 0.7, 1.27, Z_PODST)
for stena in ("x", "y"):                      # deska na jihozapadni (x) a jihovychodni (y) stene
    if stena == "x": kvadr(M["deska"], C + 0.6, C + 0.625, C - 0.36, C + 0.36, 0.56, 1.02)
    else: kvadr(M["deska"], C - 0.36, C + 0.36, C + 0.6, C + 0.625, 0.56, 1.02)
    bpy.ops.object.text_add(location=B(C + 0.63, C, 0.79) if stena == "x" else B(C, C + 0.63, 0.79),
                            rotation=(math.radians(90), 0, 0) if stena == "x" else (math.radians(90), 0, math.radians(90)))
    tx = bpy.context.object; tx.data.body = "KAREL\nMÁCHA"; tx.data.align_x = 'CENTER'; tx.data.align_y = 'CENTER'
    tx.data.font = bpy.data.fonts.load(PISMO); tx.data.size = 0.12 * K; tx.data.extrude = 0.004 * K
    tx.data.space_line = 0.9; tx.data.materials.append(M["pismo"])

def lavicka(x, y, uhel):
    """lavicka 1,6 m jako u automatu; uhel: kam se sedici diva (rad)"""
    c, s = math.cos(uhel), math.sin(uhel)
    def bod(u, v, z):
        return (x + u * -s + v * -c, y + u * c + v * -s, z)
    def kus(m, u0, u1, v0, v1, z0, z1):
        b = [bod(u, v, z) for z in (z0, z1) for v in (v0, v1) for u in (u0, u1)]
        mnohostena(m, b, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
    kus(M["lavicka"], -0.8, 0.8, -0.22, 0.22, 0.42, 0.47)
    kus(M["lavicka"], -0.8, 0.8, 0.2, 0.25, 0.5, 0.88)
    for u in (-0.65, 0.65):
        kus(M["kov"], u - 0.03, u + 0.03, -0.2, 0.22, 0.0, 0.42)
# tri lavicky cela k soše: za ni dve (sedadla k divakovi), vpravo vpredu jedna; vlevo vpredu volno na desku
R_LAV = 2.15
lavicka(C - R_LAV, C, 0.0)                    # severovychodni, diva se k jihozapadu na sochu
lavicka(C, C - R_LAV, math.pi / 2)            # severozapadni, diva se k jihovychodu
lavicka(C, C + R_LAV, -math.pi / 2)           # jihovychodni, diva se k severozapadu

# odpadkovy kos u prave zadni lavicky (v severnim rohu by ho zakryla socha), plny pres okraj
KOSX, KOSY = C - 2.15, C + 1.3
valec(M["kos"], KOSX, KOSY, 0.04, 0.76, 0.22)
valec(M["kov"], KOSX, KOSY, 0.74, 0.79, 0.24)
valec(M["cerna"], KOSX, KOSY, 0.79, 0.792, 0.19)

def ker(cx, cy, r, vyska, materialy, seed, chumacu=9, deleni=3):
    """hrbolaty ker z chumacu koul primo v siti se sumem jako u automatu"""
    rnd = random.Random(seed)
    for i in range(chumacu):
        a = rnd.random() * 2 * math.pi; d = r * 0.6 * math.sqrt(rnd.random())
        rr = r * (0.38 + 0.16 * rnd.random())
        zc = max(rr * 0.55, vyska * (0.45 + 0.5 * rnd.random()) * (1 - 0.4 * d / r) - rr * 0.3)
        stred_ = B(cx + d * math.cos(a), cy + d * math.sin(a), zc)
        bm = bm_pro(rnd.choice(materialy))
        nove_v = bmesh.ops.create_icosphere(bm, subdivisions=deleni, radius=rr * K, matrix=Matrix.Translation(stred_))["verts"]
        posun = Vector((rnd.random(), rnd.random(), rnd.random())) * 100
        for v in nove_v:
            smer = (v.co - stred_).normalized()
            n2 = noise.noise(v.co / (0.09 * K * 4) + posun) * 0.5 + noise.noise(v.co / (0.09 * K * 2) + posun) * 0.25
            v.co += smer * n2 * rr * 0.55 * K
        for f in {f for v in nove_v for f in v.link_faces}: f.smooth = True
# male krovicko v rozich policka mimo namesticko
OKR = C - (T / 2) / K                          # hrana policka v souradnicich skupiny
for i, (x, y) in enumerate(((OKR + 0.5, OKR + 0.5), (OKR + 0.5, 2 * C - OKR - 0.5), (2 * C - OKR - 0.5, OKR + 0.5),
                            (2 * C - OKR - 0.55, 2 * C - OKR - 0.55))):
    ker(x, y, 0.42, 0.7, [M["ker"], M["ker2"]], 40 + i, chumacu=8)

rnd_o = random.Random(11)
def odpadek(x, y, z0=0.0):
    """odpadek jako u automatu; jen na namesticku"""
    x = min(max(x, D0 + 0.12), D1 - 0.12); y = min(max(y, D0 + 0.12), D1 - 0.12)
    if z0 == 0.0 and abs(x - C) < 0.9 and abs(y - C) < 0.9:      # ne pod podstavec
        return
    druh = rnd_o.choices(["papir", "plech", "lahev", "kelimek", "sacek", "balicek"], [30, 18, 14, 10, 12, 16])[0]
    m = rnd_o.choice(ODPAD[druh]); uhel = rnd_o.random() * 2 * math.pi
    if druh in ("papir", "sacek"):
        r = 0.09 if druh == "papir" else 0.14
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r * K, location=B(x, y, z0 + r * 0.35))
        o = bpy.context.object; o.scale = (1.0, 0.8 + 0.4 * rnd_o.random(), 0.45 if druh == "papir" else 0.22)
        o.rotation_euler[2] = uhel
    elif druh == "balicek":
        bpy.ops.mesh.primitive_cube_add(size=1, location=B(x, y, z0 + 0.012)); o = bpy.context.object
        o.scale = (0.12 * K, 0.08 * K, 0.026 * K); o.rotation_euler[2] = uhel
    else:
        r, delka = {"plech": (0.04, 0.14), "lahev": (0.05, 0.28), "kelimek": (0.045, 0.1)}[druh]
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=r * K, depth=delka * K, location=B(x, y, z0 + r),
                                            rotation=(math.radians(90), 0, uhel))
        o = bpy.context.object
    o.data.materials.append(m)
for i in range(20):
    odpadek(KOSX + rnd_o.gauss(0, 0.5), KOSY + rnd_o.gauss(0, 0.5))
for i in range(5):
    a = rnd_o.random() * 2 * math.pi
    odpadek(KOSX + 0.1 * math.cos(a), KOSY + 0.1 * math.sin(a), 0.79)
for x, y in ((C - R_LAV, C), (C, C - R_LAV), (C, C + R_LAV)):          # u lavicek
    for i in range(6):
        odpadek(x + rnd_o.uniform(-0.6, 0.6), y + rnd_o.uniform(-0.6, 0.6))
for i in range(18):
    odpadek(rnd_o.uniform(D0 + 0.2, D1 - 0.2), rnd_o.uniform(D0 + 0.2, D1 - 0.2))

for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)

# ---------------------------------------------------------------- socha
# V mistnich souradnicich postavy (metry, clovek 1,8 m): x doprava (z pohledu postavy), y dopredu, z nahoru, chodidla
# v nule. Koren se pak postavi na podstavec, otoci celem k jihu a zvetsi (postava 2,3 m, pak K krat).
VYSKA_POSTAVY = 2.3
koren = bpy.data.objects.new("socha", None); scene.collection.objects.link(koren)

def pridej(o):
    o.parent = koren; o.data.materials.append(M["socha"])
    for p in o.data.polygons: p.use_smooth = True

KOSTI = {
    "panev": (0, 0, 0.98), "bricho": (0, 0.01, 1.15), "hrud": (0, 0, 1.33), "krk": (0, 0, 1.50),
    "kycel_p": (0.10, 0, 0.93), "koleno_p": (0.12, 0.04, 0.52), "kotnik_p": (0.13, 0, 0.10), "spicka_p": (0.15, 0.18, 0.05),
    "kycel_l": (-0.10, 0, 0.93), "koleno_l": (-0.12, 0.04, 0.52), "kotnik_l": (-0.13, 0, 0.10), "spicka_l": (-0.15, 0.18, 0.05),
    # ruce od sebe dopredu jako k objeti neceho velkeho: nadlokti do stran a malo dopredu, predlokti dopredu a ven
    "rameno_p": (0.23, 0, 1.43), "loket_p": (0.50, 0.16, 1.46), "zapesti_p": (0.62, 0.40, 1.58), "ruka_p": (0.64, 0.52, 1.63),
    "rameno_l": (-0.23, 0, 1.43), "loket_l": (-0.50, 0.16, 1.46), "zapesti_l": (-0.62, 0.40, 1.58), "ruka_l": (-0.64, 0.52, 1.63),
}
HRANY = [("panev", "bricho"), ("bricho", "hrud"), ("hrud", "krk")]
for s in ("p", "l"):
    HRANY += [("panev", f"kycel_{s}"), (f"kycel_{s}", f"koleno_{s}"), (f"koleno_{s}", f"kotnik_{s}"), (f"kotnik_{s}", f"spicka_{s}"),
              ("hrud", f"rameno_{s}"), (f"rameno_{s}", f"loket_{s}"), (f"loket_{s}", f"zapesti_{s}"), (f"zapesti_{s}", f"ruka_{s}")]
POLOMERY = {"panev": (0.2, 0.15), "bricho": (0.22, 0.16), "hrud": (0.25, 0.16), "krk": (0.08, 0.08),       # volna mikina, pomnik
            "kycel": (0.12, 0.12), "koleno": (0.095, 0.095), "kotnik": (0.075, 0.075), "spicka": (0.07, 0.05),    # kalhoty, boty
            "rameno": (0.1, 0.1), "loket": (0.09, 0.09), "zapesti": (0.07, 0.07), "ruka": (0.072, 0.038)}
jmena = list(KOSTI)
me = bpy.data.meshes.new("telo"); me.from_pydata([KOSTI[j] for j in jmena], [(jmena.index(a), jmena.index(b)) for a, b in HRANY], [])
telo = bpy.data.objects.new("telo", me); scene.collection.objects.link(telo)
bpy.context.view_layer.objects.active = telo; telo.select_set(True)
bpy.ops.object.modifier_add(type='SKIN')
telo.modifiers[-1].use_smooth_shade = True
for i, j in enumerate(jmena):
    me.skin_vertices[0].data[i].radius = POLOMERY.get(j, POLOMERY.get(j.split("_")[0], (0.08, 0.08)))
    me.skin_vertices[0].data[i].use_root = (j == "panev")
sub = telo.modifiers.new("hladke", 'SUBSURF'); sub.levels = sub.render_levels = 2
pridej(telo)

def elipsoid(jmeno, stred, polomery, rez=None):
    """elipsoid (rez: funkce bodu, ktere body vyhodit, napr. otvor kapuce)"""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=20, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * polomery[0] + stred[0], v.co.y * polomery[1] + stred[1], v.co.z * polomery[2] + stred[2]))
    if rez:
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if rez(v.co)], context='VERTS')
    m_ = bpy.data.meshes.new(jmeno); bm.to_mesh(m_); bm.free()
    o = bpy.data.objects.new(jmeno, m_); scene.collection.objects.link(o)
    pridej(o)
    return o

HLAVA = (0, 0.0, 1.64)
elipsoid("hlava", HLAVA, (0.112, 0.118, 0.128))
elipsoid("nos", (0, 0.115, 1.63), (0.02, 0.034, 0.032))
# kapuce: velka hluboka skorepina kolem hlavy az na ramena, oblicej v ni zapadly, vpredu otvor a pod bradou
def otvor_kapuce(p):
    return (p.y > 0.03 and (p.x / 0.1) ** 2 + ((p.z - 1.61) / 0.13) ** 2 < 1.0) or (p.y > 0.05 and p.z < 1.5)
kapuce = elipsoid("kapuce", (0, -0.035, 1.65), (0.17, 0.185, 0.23), otvor_kapuce)                # vyssi nad hlavou
sol = kapuce.modifiers.new("tloustka", 'SOLIDIFY'); sol.thickness = 0.016; sol.offset = -1.0
kapuce.modifiers.new("hladke", 'SUBSURF').levels = 1
# plnovous: brada, lice a knir
elipsoid("vousy", (0, 0.07, 1.48), (0.105, 0.08, 0.15))                      # plnovous az na prsa
elipsoid("knir", (0, 0.11, 1.585), (0.055, 0.025, 0.02))
elipsoid("kapsa", (0, 0.135, 1.08), (0.15, 0.028, 0.08))                     # klokani kapsa mikiny

# obrovsky joint v prave ruce: kuzel od prstu ven a nahoru, u prstu uzky, na konci siroky se zakroucenou spickou
ruka = Vector(KOSTI["ruka_p"])
smer = Vector((0.5, 0.35, 0.8)).normalized()
DELKA, R_UZKY, R_SIROKY = 0.8, 0.022, 0.065
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=R_UZKY, radius2=R_SIROKY, depth=DELKA)
bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=R_SIROKY * 0.95, radius2=0.004, depth=0.09,
                      matrix=Matrix.Translation((0, 0, DELKA / 2 + 0.045)))
rot = Vector((0, 0, 1)).rotation_difference(smer).to_matrix().to_4x4()
bmesh.ops.transform(bm, matrix=Matrix.Translation(ruka + smer * (DELKA / 2 - 0.08)) @ rot, verts=bm.verts)
m_ = bpy.data.meshes.new("joint"); bm.to_mesh(m_); bm.free()
joint = bpy.data.objects.new("joint", m_); scene.collection.objects.link(joint); pridej(joint)

koren.location = B(C, C, Z_PODST)
koren.rotation_euler = (0, 0, math.radians(-135))     # misto +y (dopredu) miri k jihu (na policku +x +y)
s_ = VYSKA_POSTAVY / 1.8 * K
koren.scale = (s_, s_, s_)

# chytac stinu pres policko
bpy.ops.mesh.primitive_plane_add(size=1, location=Vector((C, -C, 0.0)))
zem = bpy.context.object; zem.scale = (T, T, 1); zem.is_shadow_catcher = True

# ---------------------------------------------------------------- kamera a slunce jako automat
stred = Vector((C, -C, 0.0))
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); cil = bpy.context.object
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 60.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = cil
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * -0.25 + Vector((0, 0, 1.0))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "5.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def na_pixel(p):
    bpy.context.view_layer.update()
    q = world_to_camera_view(scene, cam, p)
    return (q.x * RAM, (1 - q.y) * RAM)
rohy = {"sever": na_pixel(Vector((0, 0, 0))), "vychod": na_pixel(Vector((T, 0, 0))),
        "zapad": na_pixel(Vector((0, -T, 0))), "jih": na_pixel(Vector((T, -T, 0)))}
print("rohy policka na obrazku", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()})

# stin na travu na 55 % jako automat
def render_do_pole():
    scene.render.filepath = os.path.splitext(VYSTUP)[0] + "_tmp.png"
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(scene.render.filepath).convert("RGBA"), dtype=np.float64) / 255
    os.remove(scene.render.filepath)
    return a
A = render_do_pole()
zem.hide_render = True
Bp = render_do_pole()
STIN = float(os.environ.get("STIN", "0.55"))
aB = Bp[..., 3]; aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN
alfa = aB + (1 - aB) * aS
barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
Image.fromarray((np.dstack([barva, alfa]) * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(VYSTUP)
json.dump({"px_m": PX_M, "policko_m": T, "meritko_skupiny": K, "socha": SOCHA, "ram": RAM, "rohy": rohy},
          open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
