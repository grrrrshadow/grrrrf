# -*- coding: utf-8 -*-
# Socha Karla Máchy na 1 policko (hrac 1. 10.: "udelej Karel Macha statue, policko 1x1 sochu uprostred, sedou
# z kamene a bronzovou, karel macha bude mit kapucu, vousy a obrovskyho dzonta v ruce, ruce bude mit od sebe jako by
# se chystal obejmout neco velkyho, okolo lavicky, male krovicko, odpadak, odpadky").
# Pak (hrac): "ruce trochu niz, ne podel tela, neco mezi tim, vousy po pupek dlouhy a jointa vic do trychtyre, sirsi na
# konci" a "mnohem mene stinu". Pak zhavy popel a kour z jointu, tmave zeleny pas keru kolem dlazby a rostliny
# marihuany (velke vzadu za lavickami, male vpredu, zelene jako naklad MARI; rostliny/rostliny.py).
# Vlastni model, kamera a meritko jako automat (automat/render_automat.py), vsechno dvakrat vetsi (MERITKO 2) jako
# automat, at to k sobe sedi. Slunce slabsi a okoli silnejsi nez u automatu, stin na travu jen 20 %.
#   python3 render_socha.py <vystup.png>          SOCHA=kamen (sediva z kamene) nebo SOCHA=bronz
#   POSTAVY=1: druhy obrazek do animace s divkami od hrace (postavy/), pak sloucit postavy/animace.py
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu policka; skupina je
# navrzena ve skutecne velikosti kolem stredu policka C a zvetsi se K krat.
# Postava stoji na podstavci cela k divakovi (k jihu), aby roztazene ruce byly na obrazku vodorovne: mikina s kapuci
# na hlave, plnovous po pupek, ruce od sebe jako k objeti, v prave ruce obrovsky joint jako trychtyr. Telo je kostra
# s modifikatorem Skin a vyhlazenim, takze je hladke jako tesane nebo lite.
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image

VYSTUP = sys.argv[-1]
ZIN = int(os.environ.get("ZIN", "4"))         # priblizeni: 4 (zin4, 12,2 px/m, 384 px) nebo 8 (zin8 jen nase hra: 24,4 px/m, 768 px, stejny zaber)
PX_M = 12.2 * ZIN / 4
RAM = 384 * ZIN // 4
K = float(os.environ.get("MERITKO", "2"))
SOCHA = os.environ.get("SOCHA", "kamen")
T = 256 / (math.sqrt(2) * 12.2)               # policko 14,84 m (256 px ve 4x)
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
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.9"))      # hrac: "mnohem mene stinu"

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
# vousy u kamenne hrube tesane, o kus tmavsi, jinak by se pri slabych stinech ztratily na mikine (bronz stejny)
M["vousy"] = M["socha"] if SOCHA == "bronz" else mat("vousy", (146, 144, 138), 0.95, sum_=0.16, meritko=40.0)
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
# tmave zeleny pas nizkych keru kolem dlazby az k hrane policka (hrac: "to krovi je stejnou barvou jako zem, zanika,
# neni videt. udelej tam tmavou zelenou okolo dlazby"). Chomacky primo v siti jako ker(), nahodne hustě vedle sebe;
# zadny nesmi presahnout hranu policka (dosah = polomer i s hrbolky), dovnitr kousek pres obrubnik.
M["ker_t1"] = mat("ker_t1", (26, 56, 22), 0.9, sum_=0.35, meritko=9.0)
M["ker_t2"] = mat("ker_t2", (36, 72, 30), 0.9, sum_=0.3, meritko=9.0)
M["ker_t3"] = mat("ker_t3", (31, 64, 25), 0.9, sum_=0.3, meritko=11.0)
POLE = T / 2 / K                                   # od stredu k hrane policka (skupina)
def pas_keru():
    rnd = random.Random(77)
    hotove = []
    for _ in range(9000):
        dx, dy = rnd.uniform(-POLE, POLE), rnd.uniform(-POLE, POLE)
        rr = rnd.uniform(0.13, 0.2)
        dosah = rr * 1.45
        mx = max(abs(dx), abs(dy))
        if mx + dosah > POLE - 0.04 or mx < 2.8 - 0.06:
            continue
        if any((dx - hx) ** 2 + (dy - hy) ** 2 < (0.55 * (rr + hr)) ** 2 for hx, hy, hr in hotove):
            continue
        hotove.append((dx, dy, rr))
    for i, (dx, dy, rr) in enumerate(hotove):
        zc = rr * 0.55 + rnd.uniform(0.0, 0.14)
        stred_ = B(C + dx, C + dy, zc)
        bm = bm_pro(rnd.choice([M["ker_t1"], M["ker_t2"], M["ker_t3"]]))
        nove_v = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=rr * K, matrix=Matrix.Translation(stred_))["verts"]
        posun = Vector((rnd.random(), rnd.random(), rnd.random())) * 100
        for v in nove_v:
            smer_ = (v.co - stred_).normalized()
            n2 = noise.noise(v.co / (0.09 * K * 4) + posun) * 0.5 + noise.noise(v.co / (0.09 * K * 2) + posun) * 0.25
            v.co += smer_ * n2 * rr * 0.55 * K
            if v.co.z < 0: v.co.z = 0.0
        for f in {f for v in nove_v for f in v.link_faces}: f.smooth = True
    print("pas keru:", len(hotove), "chomacku")
pas_keru()

# rostliny marihuany, zelene jako naklad MARI (hrac: "odstinem je odlis od krovi", "odstin zelene z nakladu mari"):
# velke na severovychodni a severozapadni strane za lavickami a v rohu mezi nimi (hrac: "kytky rostou 5 metru vysoko,
# na severovychodni a severozapadni strane muzou byt kytky marihuany velky jako socha", "dopredu maly, velky sv a sz
# dozadu za lavicky"), male vpredu v pasu keru. Koruna velkych nejvys 0,9 m od kmene, at nesaha na operadla, malych
# 0,38 m, at nepresahnou predni hranu policka.
sys.path.insert(0, os.path.join(TU, "..", "rostliny"))
import rostliny as RO
VYSOKA = RO.nacti("cannabis_plant"); KOSATA = RO.nacti("cannabis_sativa_plant")       # mala ridka (small_cannabis_plant) neni videt
for dx, dy, vys, druh, ot in ((-3.35, -3.35, 5.0, VYSOKA, 0.4),                                  # roh mezi lavickami
                              (-0.65, -3.4, 4.4, KOSATA, 3.0), (0.65, -3.4, 4.7, VYSOKA, 4.1),   # za severozapadni
                              (-3.4, -0.65, 4.6, VYSOKA, 2.2), (-3.4, 0.65, 4.3, KOSATA, 1.3)):  # za severovychodni
    RO.postav(druh[0], druh[1], Matrix.Translation(B(C + dx, C + dy, 0)), vys * K, 0.9 * K, ot)
for dx, dy, vys, ot in ((3.28, -2.3, 1.35, 0.3), (3.28, -1.0, 1.2, 2.0), (3.28, 2.3, 1.4, 4.4),          # jihozapadni strana
                        (-2.3, 3.28, 1.4, 1.1), (-1.0, 3.28, 1.25, 3.3), (2.3, 3.28, 1.3, 5.2)):          # jihovychodni
    RO.postav(KOSATA[0], KOSATA[1], Matrix.Translation(B(C + dx, C + dy, 0)), vys * K, 0.38 * K, ot)   # mala kosata

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
    # ruce od sebe jako k objeti neceho velkeho, ale niz (hrac: "ne podel tela, neco mezi tim"): nadlokti sikmo dolu
    # do stran a malo dopredu, predlokti dopredu a ven, dlane ve vysce hrudi
    "rameno_p": (0.23, 0, 1.43), "loket_p": (0.446, 0.075, 1.235), "zapesti_p": (0.611, 0.281, 1.29), "ruka_p": (0.667, 0.37, 1.323),
    "rameno_l": (-0.23, 0, 1.43), "loket_l": (-0.446, 0.075, 1.235), "zapesti_l": (-0.611, 0.281, 1.29), "ruka_l": (-0.667, 0.37, 1.323),
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
def loft(jmeno, kruhy, konec=None, deleni=1):
    """sit z kruhu bodu (vsechny stejne dlouhe) spojenych pasy; prvni kruh zavre stena, posledni stena nebo spicka konec"""
    bm = bmesh.new()
    vk = [[bm.verts.new(p) for p in k] for k in kruhy]
    n = len(vk[0])
    for a, b in zip(vk, vk[1:]):
        for k in range(n):
            bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    bm.faces.new(vk[0])
    if konec is None:
        bm.faces.new(vk[-1])
    else:
        v = bm.verts.new(konec)
        for k in range(n):
            bm.faces.new((vk[-1][k], vk[-1][(k + 1) % n], v))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    m_ = bpy.data.meshes.new(jmeno); bm.to_mesh(m_); bm.free()
    o = bpy.data.objects.new(jmeno, m_); scene.collection.objects.link(o)
    sub = o.modifiers.new("hladke", 'SUBSURF'); sub.levels = sub.render_levels = deleni
    pridej(o)
    return o

# plnovous: lice a brada, knir a dlouhe vousy po pupek (hrac): od brady pres prsa a bricho do spicky. Vzadu lezi
# kousek zanorene na mikine (predek tela zmereny z modelu: y 0,09 u krku, 0,15 na bricho), vpredu pramenky.
VOUSY_OBJ = [elipsoid("vousy", (0, 0.07, 1.48), (0.105, 0.08, 0.15)), elipsoid("knir", (0, 0.11, 1.585), (0.055, 0.025, 0.02))]
def kruh_vousu(z, w, d, yc, n=48):
    body = []
    for k in range(n):
        a = 2 * math.pi * k / n
        pramen = 1 + 0.07 * math.cos(12 * a) * max(0.0, math.sin(a))
        body.append((w * math.cos(a) * pramen, yc + d * math.sin(a) * pramen, z))
    return body
# kruhy dlouhych vousu: (vyska, pulsirka, pulhloubka, stred y)
VOUSY = [(1.57, 0.085, 0.04, 0.095), (1.50, 0.105, 0.05, 0.125), (1.42, 0.11, 0.047, 0.147), (1.33, 0.102, 0.041, 0.158),
         (1.25, 0.09, 0.036, 0.164), (1.18, 0.072, 0.03, 0.166), (1.12, 0.048, 0.024, 0.162), (1.075, 0.022, 0.015, 0.152)]
VOUSY_OBJ.append(loft("vousy_dlouhe", [kruh_vousu(*v) for v in VOUSY], konec=(0, 0.149, 1.048), deleni=2))
for o in VOUSY_OBJ: o.data.materials[0] = M["vousy"]
elipsoid("kapsa", (0, 0.13, 1.0), (0.15, 0.028, 0.075))                      # klokani kapsa mikiny, kousek pod vousy

# obrovsky joint v prave ruce jako trychtyr (hrac: "zvyraznit trychtyrovitost, sirsi na konci"; rovny tlusty kuzel byl
# "americky typu fat"): u prstu tenky filtr, pak rovny kuzel az do sirokeho konce. Ten hori (hrac: "udelame na konci
# zhavej popel a dym z dzonta"): na useknutem okraji papiru je nizka kupka popela, mista na ni zhavi, a z ni stoupa kour.
ruka = Vector(KOSTI["ruka_p"])
smer = Vector((0.55, 0.2, 0.8)).normalized()
u_ = smer.orthogonal().normalized(); v_ = smer.cross(u_)
PROFIL = [(0.0, 0.016), (0.08, 0.018), (0.085, 0.022), (0.10, 0.022)]                       # (od konce v puse, polomer)
PROFIL += [(0.10 + 0.74 * i / 8, 0.022 + 0.11 * i / 8) for i in range(1, 9)]              # rozevira se az na 0,132
zac = ruka - smer * 0.06                                                                     # filtr mezi prsty
def kruh_j(s, r, n=24):
    return [zac + smer * s + (u_ * math.cos(2 * math.pi * k / n) + v_ * math.sin(2 * math.pi * k / n)) * r for k in range(n)]
loft("joint", [kruh_j(s, r) for s, r in PROFIL])                  # konec je rovny, zakryje ho popel

def zhavy_popel():
    """popel: tmave sedy a drsny; kde je sum vys, zhavi oranzove, a v zhavem cervene body (hrac: "cerveny body v tom
    zhavym"). Barvy svitu jsou syte a ne moc silne, jinak je prevod barev (AgX) vybeli do ruzova."""
    m = bpy.data.materials.new("zhavy_popel"); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 1.0
    tc = t.nodes.new('ShaderNodeTexCoord')
    sm = t.nodes.new('ShaderNodeTexNoise'); sm.inputs["Scale"].default_value = 40.0; sm.inputs["Detail"].default_value = 4.0
    t.links.new(tc.outputs["Object"], sm.inputs["Vector"])
    zar = t.nodes.new('ShaderNodeMapRange'); zar.inputs["From Min"].default_value = 0.40; zar.inputs["From Max"].default_value = 0.52
    t.links.new(sm.outputs["Fac"], zar.inputs["Value"])
    vor = t.nodes.new('ShaderNodeTexVoronoi'); vor.inputs["Scale"].default_value = 11.0           # body asi 2 px ve hre
    t.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    body = t.nodes.new('ShaderNodeMapRange'); body.inputs["From Min"].default_value = 0.22; body.inputs["From Max"].default_value = 0.38
    body.inputs["To Min"].default_value = 1.0; body.inputs["To Max"].default_value = 0.0
    t.links.new(vor.outputs["Distance"], body.inputs["Value"])
    # cervene body hlavne v zhavem: body * (0,4 + 0,6 * zar)
    zz = t.nodes.new('ShaderNodeMapRange'); zz.inputs["To Min"].default_value = 0.4; zz.inputs["To Max"].default_value = 1.0
    t.links.new(zar.outputs["Result"], zz.inputs["Value"])
    bz = t.nodes.new('ShaderNodeMath'); bz.operation = 'MULTIPLY'
    t.links.new(body.outputs["Result"], bz.inputs[0]); t.links.new(zz.outputs["Result"], bz.inputs[1])
    barva = t.nodes.new('ShaderNodeMix'); barva.data_type = 'RGBA'
    barva.inputs["A"].default_value = (1.0, 0.22, 0.0, 1.0); barva.inputs["B"].default_value = (1.0, 0.0, 0.0, 1.0)
    t.links.new(bz.outputs[0], barva.inputs["Factor"])
    t.links.new(barva.outputs["Result"], b.inputs["Emission Color"])
    s1 = t.nodes.new('ShaderNodeMath'); s1.operation = 'MULTIPLY'; s1.inputs[1].default_value = float(os.environ.get("ZAR", "1.3"))
    t.links.new(zar.outputs["Result"], s1.inputs[0])
    s2 = t.nodes.new('ShaderNodeMath'); s2.operation = 'MULTIPLY_ADD'; s2.inputs[1].default_value = 1.6
    t.links.new(bz.outputs[0], s2.inputs[0]); t.links.new(s1.outputs[0], s2.inputs[2])
    t.links.new(s2.outputs[0], b.inputs["Emission Strength"])
    zaklad = t.nodes.new('ShaderNodeMix'); zaklad.data_type = 'RGBA'
    zaklad.inputs["A"].default_value = srgb((56, 53, 50)); zaklad.inputs["B"].default_value = srgb((120, 10, 2))
    mx = t.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
    t.links.new(zar.outputs["Result"], mx.inputs[0]); t.links.new(bz.outputs[0], mx.inputs[1])
    t.links.new(mx.outputs[0], zaklad.inputs["Factor"]); t.links.new(zaklad.outputs["Result"], b.inputs["Base Color"])
    return m
popel = loft("popel", [kruh_j(0.836, 0.130), kruh_j(0.848, 0.125), kruh_j(0.858, 0.108), kruh_j(0.866, 0.078),
                       kruh_j(0.871, 0.042)], konec=zac + smer * 0.874)
popel.data.materials[0] = zhavy_popel()

# kour: tenky pramen z popela rovnou nahoru, kousek se stacuje stranou od Karlovy hlavy (k jeho pravici, na obrazku
# doleva) a dozadu, smerem nahoru se rozsiruje a ridne. Objem s hustotou ze sumu (chomacky), zespodu hustsi.
P0 = zac + smer * 0.874
DYM_V = 0.85                                                       # jak vysoko (mistni jednotky postavy 1,8 m)
def dym_material():
    m = bpy.data.materials.new("dym"); m.use_nodes = True
    t = m.node_tree
    for n in list(t.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            t.nodes.remove(n)
    out = next(n for n in t.nodes if n.type == 'OUTPUT_MATERIAL')
    pv = t.nodes.new('ShaderNodeVolumePrincipled')
    pv.inputs["Color"].default_value = (0.93, 0.93, 0.95, 1.0); pv.inputs["Anisotropy"].default_value = 0.25
    pv.inputs["Absorption Color"].default_value = (0.75, 0.75, 0.77, 1.0)        # svetly kour, ne tmave sedy
    tc = t.nodes.new('ShaderNodeTexCoord')
    sep = t.nodes.new('ShaderNodeSeparateXYZ'); t.links.new(tc.outputs["Object"], sep.inputs[0])
    sm = t.nodes.new('ShaderNodeTexNoise'); sm.inputs["Scale"].default_value = 14.0; sm.inputs["Detail"].default_value = 3.0
    t.links.new(tc.outputs["Object"], sm.inputs["Vector"])
    chom = t.nodes.new('ShaderNodeMapRange'); chom.inputs["From Min"].default_value = 0.35; chom.inputs["From Max"].default_value = 0.62
    t.links.new(sm.outputs["Fac"], chom.inputs["Value"])
    vys = t.nodes.new('ShaderNodeMapRange')
    vys.inputs["From Min"].default_value = P0.z; vys.inputs["From Max"].default_value = P0.z + DYM_V
    vys.inputs["To Min"].default_value = 1.0; vys.inputs["To Max"].default_value = 0.0
    t.links.new(sep.outputs["Z"], vys.inputs["Value"])
    m1 = t.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
    t.links.new(chom.outputs["Result"], m1.inputs[0]); t.links.new(vys.outputs["Result"], m1.inputs[1])
    m2 = t.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'; m2.inputs[1].default_value = float(os.environ.get("DYM", "18.0"))
    t.links.new(m1.outputs[0], m2.inputs[0]); t.links.new(m2.outputs[0], pv.inputs["Density"])
    t.links.new(pv.outputs["Volume"], out.inputs["Volume"])
    return m
kruhy_dym = []
for i in range(22):
    tt = i / 21
    stred = P0 + Vector((0.18 * tt + 0.04 * math.sin(2 * math.pi * 1.3 * tt), -0.08 * tt, DYM_V * tt))
    r = 0.026 + 0.15 * tt ** 0.8
    kruhy_dym.append([stred + Vector((math.cos(2 * math.pi * k / 16), math.sin(2 * math.pi * k / 16), 0)) * r for k in range(16)])
dym = loft("dym", kruhy_dym)
dym.data.materials[0] = dym_material()

koren.location = B(C, C, Z_PODST)
koren.rotation_euler = (0, 0, math.radians(-135))     # misto +y (dopredu) miri k jihu (na policku +x +y)
s_ = VYSKA_POSTAVY / 1.8 * K
koren.scale = (s_, s_, s_)

# ---------------------------------------------------------------- postavy (druhy obrazek do animace, POSTAVY=1)
# Hrac: "bikini girl jako ze kraci tam, kde by byla ctvrta lavicka, college girl vyleze na sochu, obejme Karla a da
# mu pusu, na lavicky zbytek: dve na jednu lavicku, jednu na jednu a treti lavicka bude prazdna"; meritko k lavicce.
# Modely jsou v postavy/ (autori a licence v postavy/LICENCE.md), poza v postavy/postavy.py.
if os.environ.get("POSTAVY", "") == "1":
    sys.path.insert(0, os.path.join(TU, "..", "postavy"))
    import postavy as PO

    def do_sceny(meshe, kotva, gx, gy, gz, uhel):
        """postava (celem k -y, kotva = jeji bod, ktery ma stat v bode skupiny gx gy gz) celem ve smeru uhel"""
        M = Matrix.Translation(B(gx, gy, gz)) @ Matrix.Rotation(uhel, 4, 'Z') @ Matrix.Scale(K, 4) @ Matrix.Translation(-kotva)
        PO.postav(meshe, M)

    def na_lavicku(meshe, kotva, lavicka, u):
        """bod sedu na sedak lavicky (x, y, uhel) ve vzdalenosti u od jejiho stredu, zady k operadlu"""
        x, y, uhel = lavicka
        c, s = math.cos(uhel), math.sin(uhel)
        v = 0.05                                      # kousek dozadu k operadlu
        do_sceny(meshe, kotva, x + u * -s + v * -c, y + u * c + v * -s, 0.47, uhel)

    # divka v bikinach: krok (stehno vpred, vzad, koleno zadni nohy), kolik z rozkroku srovnat (vic = chodidlo na hranu),
    # posun k jihovychodu a smer chuze ve stupnich (45 = k divakovi, 90 = k jihovychodu)
    BK_VPRED, BK_VZAD, BK_KOLENO, BK_K = (float(os.environ.get(n, d)) for n, d in (("BK_VPRED", "-12"), ("BK_VZAD", "5"), ("BK_KOLENO", "6"), ("BK_K", "0.5")))
    BK_Y, BK_SMER = float(os.environ.get("BK_Y", "0.55")), float(os.environ.get("BK_SMER", "70"))
    LAV_SZ = (C, C - R_LAV, math.pi / 2)              # severozapadni (na obrazku vlevo nahore): dve divky
    LAV_SV = (C - R_LAV, C, 0.0)                      # severovychodni (vpravo nahore): jedna, jihovychodni prazdna

    def kost(arm, zacatek):
        return next(b.name for b in arm.pose.bones if b.name.startswith(zacatek))

    # galaxia: sed kostrou, ruce podel tela a predlokti na stehna
    def sed_kostra(arm, meshe):
        for st in ("L", "R"):
            zn = 1 if st == "L" else -1
            PO.otoc_kost(arm, kost(arm, f"J_Bip_{st}_UpperLeg"), (1, 0, 0), math.radians(-72))     # kolena niz, at dojde na zem
            PO.otoc_kost(arm, kost(arm, f"J_Bip_{st}_LowerLeg"), (1, 0, 0), math.radians(67))
            PO.otoc_kost(arm, kost(arm, f"J_Bip_{st}_UpperArm"), (0, 1, 0), zn * math.radians(72))
            PO.otoc_kost(arm, kost(arm, f"J_Bip_{st}_UpperArm"), (1, 0, 0), math.radians(-18))
            PO.otoc_kost(arm, kost(arm, f"J_Bip_{st}_LowerArm"), (1, 0, 0), math.radians(-55))
    g = PO.nacti("galaxia_anime_girl", 1.58, priprava=sed_kostra, nechat=lambda o: "Icosphere" not in o.name)
    kotva, pokles = PO.bod_sedu(g, 1.58, 0.0)
    print("galaxia: od zadku k chodidlum %.3f m (sedak 0,47)" % pokles)
    na_lavicku(g, kotva, LAV_SZ, -0.42)

    # character_people_girl_001: sedi vedle, ruku ve vlasech nechava
    ch = PO.nacti("character_people_girl_001", 1.68)
    nohy = PO.stredy_nohou(ch, 1.68)
    kotva, st, chyba = PO.sed(ch, 1.68, 0.49, 0.28, [nohy[0][1], nohy[1][1]])
    print("character: stehna %d st, chodidla mimo zem o %.3f m" % (st, chyba))
    na_lavicku(ch, kotva, LAV_SZ, 0.38)

    # anime_girl: sama na severovychodni lavicce (sviti sama, emisi pryc)
    an = PO.nacti("anime_girl", 1.6, emise=0.0)
    nohy = PO.stredy_nohou(an, 1.6)
    kotva, st, chyba = PO.sed(an, 1.6, 0.52, 0.285, [nohy[0][1], nohy[1][1]])
    print("anime: stehna %d st, chodidla mimo zem o %.3f m" % (st, chyba))
    na_lavicku(an, kotva, LAV_SV, 0.12)

    # girl_bikini: krok tam, kde by byla ctvrta lavicka, a kousek k jihovychodu (hrac: "at nema u hlavy nohu te holky
    # na lavicce"). Model stoji jako modelka (nohy od sebe, hlava zaklonena k nebi), proto: nohy k sobe pod kycle,
    # kratky klidny krok, hlava o 35 st dopredu a 15 st zpet nad ramena. Jde k vychodu-jihovychodu, ze strany je
    # krok videt (hrac: "zda se mi neprirozena, klidne ji nejak pootoc").
    bk = PO.nacti("girl_bikini", 1.66)
    (xr, xfr, zfr), (xl, xfl, zfl) = PO.stredy_nohou(bk, 1.66)
    odklon_r = math.atan2(xfr - xr, 0.42 * 1.66 - zfr); odklon_l = math.atan2(xfl - xl, 0.42 * 1.66 - zfl)
    PO.ohni_nohy(bk, 1.66, 0.50, 0.285,
                 [(xr, Matrix.Rotation(math.radians(BK_VPRED), 3, 'X') @ Matrix.Rotation(-BK_K * odklon_r, 3, 'Y'), ((1, 0, 0), math.radians(4))),
                  (xl, Matrix.Rotation(math.radians(BK_VZAD), 3, 'X') @ Matrix.Rotation(-BK_K * odklon_l, 3, 'Y'), ((1, 0, 0), math.radians(BK_KOLENO)))])
    PO.otoc_cast(bk, 1.66, 0.855, (-0.06 * 1.66, 0.02 * 1.66, 0.85 * 1.66),
                 Matrix.Rotation(math.radians(15), 3, 'Y') @ Matrix.Rotation(math.radians(35), 3, 'X'))
    lo, hi, _ = PO.rozmery_siti(bk)
    do_sceny(bk, Vector((0, 0, lo[2])), C + R_LAV, C + BK_Y, Z_D, math.radians(BK_SMER))

    # college_girl: na podstavci u Karla zleva zpredu, celem k nemu, objima ho (ruce dopredu, predlokti kolem nej)
    def divka_a(o):
        if o.parent is None or o.parent.type != 'ARMATURE':
            return False
        dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me_ = e.to_mesh()
        x = sum((o.matrix_world @ v.co).x for v in me_.vertices) / max(1, len(me_.vertices)); e.to_mesh_clear()
        return x < -1.0
    def objeti(arm, meshe):
        for st, zn in (("R", 1), ("L", -1)):
            ram = kost(arm, f"Shoulder_{st}_"); loket = kost(arm, f"Elbow_{st}_")
            PO.otoc_kost(arm, ram, (0, 0, 1), zn * math.radians(62))       # ruce dopredu a trochu od sebe
            PO.otoc_kost(arm, ram, (1, 0, 0), math.radians(-25))           # a nahoru k jeho hrudi
            PO.otoc_kost(arm, loket, (0, 0, 1), zn * math.radians(45))     # predlokti kolem nej
        PO.otoc_kost(arm, kost(arm, "Spine1_M_"), (1, 0, 0), math.radians(6))
        PO.otoc_kost(arm, kost(arm, "Head_M_"), (1, 0, 0), math.radians(-25))  # hlavu nahoru k nemu
    cg = PO.nacti("college_girl", 1.62, priprava=objeti, nechat=divka_a)
    # v mistnich souradnicich sochy (x doprava z pohledu Karla, y dopredu): vlevo zpredu, Karel je 2,3/1,8 vetsi
    k_ = VYSKA_POSTAVY / 1.8
    lx, ly = -0.30 * k_, 0.25 * k_
    vpravo, vpred = Vector((1, -1)) / math.sqrt(2), Vector((1, 1)) / math.sqrt(2)     # Karel celem k jihu
    gpos = vpravo * lx + vpred * ly
    smer = -(gpos.normalized())
    do_sceny(cg, Vector((0, 0, 0)), C + gpos.x, C + gpos.y, Z_PODST, math.atan2(smer.y, smer.x))

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
sl.data.energy = float(os.environ.get("SLUNCE", "2.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def na_pixel(p):
    bpy.context.view_layer.update()
    q = world_to_camera_view(scene, cam, p)
    return (q.x * RAM, (1 - q.y) * RAM)
rohy = {"sever": na_pixel(Vector((0, 0, 0))), "vychod": na_pixel(Vector((T, 0, 0))),
        "zapad": na_pixel(Vector((0, -T, 0))), "jih": na_pixel(Vector((T, -T, 0)))}
print("rohy policka na obrazku", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()})

# stin na travu jen na 20 % (automat ma 55 %), hrac chtel u sochy mnohem mene stinu
def render_do_pole():
    scene.render.filepath = os.path.splitext(VYSTUP)[0] + "_tmp.png"
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(scene.render.filepath).convert("RGBA"), dtype=np.float64) / 255
    os.remove(scene.render.filepath)
    return a
A = render_do_pole()
zem.hide_render = True
Bp = render_do_pole()
STIN = float(os.environ.get("STIN", "0.2"))
aB = Bp[..., 3]; aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN
alfa = aB + (1 - aB) * aS
barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
Image.fromarray((np.dstack([barva, alfa]) * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(VYSTUP)
json.dump({"px_m": PX_M, "policko_m": T, "meritko_skupiny": K, "socha": SOCHA, "ram": RAM, "rohy": rohy},
          open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
