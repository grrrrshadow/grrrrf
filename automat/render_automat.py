# -*- coding: utf-8 -*-
# Automat na marihuanu na 1 policko (hrac 1. 10. s fotkami CBD MAT: "jeste udelej 1x1 policko automat na marihuanu
# s lavickou a kerickem krovi"). Vlastni model, kamera, meritko a svetlo jako gymnazium (gymnazium/render_gymnazium.py):
# ortho 30 st. shora, 12,2 px/m v zin4, slunce zleva shora se silnejsimi stiny jako u Tatry, stin na travu na 55 %.
# Automat podle fotek: tmave seda skrin, prosklena dvirka s regaly, vpravo zeleny pruh s placenim, dole vydejni
# klapka se zelenym stitkem PULL, bok polepeny zelenou folii s listy konopi, paprsky a bilym napisem CBD MAT.
# Skupina je ctverec (hrac: "to mas obdelnicek, neco jako 2x1 policko", "lavicku postav pred automat, otoc ji
# sedadlem k automatu a mas ctverec"): automat vzadu, lavicka pred nim sedadlem k nemu, ker vedle, dlazba 4 x 4 m
# s obrubnikem. Hrac: "2x vetsi jo, dame do rohu policka a zbytek policka krovi", "vedle lavicky dej odpadkovy kos
# a odpadky rozhazene po zemi": skupina je v severnim rohu policka (MERITKO, vychozi 2), zbytek zarostly divokym
# neudrzovanym krovim stejne zvetsenym, mezi nim plevel.
#   python3 render_automat.py <vystup.png>
#   POSTAVY=1: druhy obrazek do animace s divkami (postavy/), pak sloucit postavy/animace.py s automat_zin4.png
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu policka.
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image, ImageDraw, ImageFont

VYSTUP = sys.argv[-1]
ZIN = int(os.environ.get("ZIN", "4"))         # priblizeni: 4 (zin4, 12,2 px/m, 384 px) nebo 8 (zin8 jen nase hra: 24,4 px/m, 768 px, stejny zaber)
PX_M = 12.2 * ZIN / 4
RAM = 384 * ZIN // 4
K = float(os.environ.get("MERITKO", "2"))
T = 256 / (math.sqrt(2) * 12.2)               # policko 14,84 m (256 px ve 4x)
C = T / 2                                       # stred policka
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
PISMO = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEX = os.path.splitext(VYSTUP)[0] + "_tex"
os.makedirs(TEX, exist_ok=True)

# ---------------------------------------------------------------- obrazky na automat (polep boku a predek)
def list_konopi(d, cx, cy, delka, uhel, barva):
    """list konopi: sedm listku do vejire, prostredni nejdelsi, kazdy kopinaty se zubatym okrajem"""
    for rel, dl in ((0, 1.0), (-27, 0.86), (27, 0.86), (-54, 0.66), (54, 0.66), (-82, 0.42), (82, 0.42)):
        a = math.radians(uhel + rel); L = delka * dl; w = L * 0.13
        osa = (math.cos(a), math.sin(a)); kolmo = (-osa[1], osa[0])
        body = []
        for i in range(13):                       # jedna strana od spicky ke stopce, zoubky
            t = i / 12; s = math.sin(math.pi * t) ** 0.8 * w * (1.15 if i % 2 else 0.85)
            body.append((cx + osa[0] * L * (1 - t) + kolmo[0] * s, cy + osa[1] * L * (1 - t) + kolmo[1] * s))
        for i in range(12, -1, -1):
            t = i / 12; s = math.sin(math.pi * t) ** 0.8 * w * (1.15 if i % 2 else 0.85)
            body.append((cx + osa[0] * L * (1 - t) - kolmo[0] * s, cy + osa[1] * L * (1 - t) - kolmo[1] * s))
        d.polygon(body, fill=barva)
    a = math.radians(uhel + 180)
    d.line([(cx, cy), (cx + math.cos(a) * delka * 0.35, cy + math.sin(a) * delka * 0.35)], fill=barva, width=max(2, int(delka * 0.03)))

def napis(d, text, cx, cy, vyska, barva, obrys):
    f = ImageFont.truetype(PISMO, int(vyska))
    for dx in range(-4, 5, 2):
        for dy in range(-4, 5, 2):
            d.text((cx + dx + 5, cy + dy + 6), text, font=f, fill=obrys, anchor="mm")
    d.text((cx, cy), text, font=f, fill=barva, anchor="mm")

def obrazek_bok(cesta):
    W, H = 340, 732
    im = Image.new("RGB", (W, H), (92, 186, 50)); d = ImageDraw.Draw(im)
    sx, sy = W * 0.55, H * 0.56
    for k in range(28):                                                  # paprsky ze stredu
        if k % 2: continue
        a0, a1 = 2 * math.pi * k / 28, 2 * math.pi * (k + 1) / 28
        d.polygon([(sx, sy), (sx + 2000 * math.cos(a0), sy + 2000 * math.sin(a0)), (sx + 2000 * math.cos(a1), sy + 2000 * math.sin(a1))],
                  fill=(116, 204, 66))
    tmava, stredni = (30, 96, 32), (46, 120, 40)
    for cx, cy, dl, u, b in ((70, 90, 150, -60, tmava), (270, 150, 170, -120, tmava), (60, 400, 120, -100, stredni),
                             (290, 360, 100, -70, tmava), (90, 640, 170, -80, tmava), (270, 650, 150, -110, tmava),
                             (180, 260, 70, -95, stredni), (300, 560, 60, -60, stredni), (40, 250, 60, -40, stredni)):
        list_konopi(d, cx, cy, dl, u, b)
    pis = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pis)
    napis(dp, "CBD", W * 0.5, H * 0.47, 112, (246, 246, 244), (20, 60, 22))
    napis(dp, "MAT", W * 0.52, H * 0.62, 112, (246, 246, 244), (20, 60, 22))
    pis = pis.rotate(8, resample=Image.BICUBIC, center=(W * 0.5, H * 0.55))
    im.paste(pis, (0, 0), pis)
    im.save(cesta)

def obrazek_predek(cesta):
    W, H = 360, 732
    im = Image.new("RGB", (W, H), (66, 68, 70)); d = ImageDraw.Draw(im)
    gx0, gx1, gy0, gy1 = 0.05 * W, 0.67 * W, 0.04 * H, 0.66 * H
    d.rectangle([gx0 - 8, gy0 - 8, gx1 + 8, gy1 + 8], fill=(128, 130, 134))           # ram skla
    d.rectangle([gx0, gy0, gx1, gy1], fill=(22, 26, 32))                             # vnitrek
    rnd = random.Random(3)
    barvy = [(236, 236, 230), (90, 190, 60), (200, 200, 205), (30, 30, 30), (230, 140, 40), (60, 120, 200), (240, 240, 240)]
    police = 6
    for i in range(police):
        y1 = gy0 + (gy1 - gy0) * (i + 1) / police
        y0 = y1 - (gy1 - gy0) / police
        x = gx0 + 14
        while x < gx1 - 16:                                                  # baliky na polici
            w = rnd.randint(14, 26); h = rnd.randint(int((y1 - y0) * 0.45), int((y1 - y0) * 0.8))
            d.rectangle([x, y1 - 6 - h, x + w, y1 - 6], fill=rnd.choice(barvy))
            x += w + rnd.randint(3, 8)
        d.rectangle([gx0, y1 - 6, gx1, y1 - 1], fill=(176, 178, 184))              # police
    d.rectangle([gx0 + 3, gy0, gx0 + 7, gy1], fill=(250, 250, 255))                   # svetelny pas LED
    d.rectangle([gx0 + 16, gy0 + 10, gx0 + 64, gy0 + 40], fill=(236, 236, 236))       # nalepka POZOR
    d.rectangle([gx0 + 16, gy0 + 10, gx0 + 64, gy0 + 22], fill=(210, 30, 30))
    px0, px1 = 0.72 * W, 0.95 * W                                                    # zeleny pruh s placenim
    d.rectangle([px0, 0.05 * H, px1, 0.89 * H], fill=(96, 200, 58))
    d.rectangle([px0 + 14, 0.10 * H, px1 - 14, 0.16 * H], fill=(236, 240, 236))       # papir s cenikem
    d.rectangle([px0 + 10, 0.22 * H, px1 - 10, 0.29 * H], fill=(26, 26, 28))          # ctecka karet
    d.rectangle([px0 + 16, 0.32 * H, px1 - 16, 0.345 * H], fill=(40, 80, 230))        # displej
    for r in range(4):                                                               # klavesnice
        for s in range(3):
            x = px0 + 14 + s * 18; y = 0.40 * H + r * 18
            d.rectangle([x, y, x + 12, y + 12], fill=(170, 172, 176))
    d.rectangle([px0 + 22, 0.60 * H, px1 - 22, 0.66 * H], fill=(150, 152, 156))       # mince
    d.rectangle([px0 + 26, 0.72 * H, px1 - 26, 0.76 * H], fill=(30, 30, 32))
    d.rectangle([0.07 * W, 0.70 * H, 0.66 * W, 0.86 * H], fill=(52, 54, 56))           # vydejni klapka
    d.rectangle([0.17 * W, 0.735 * H, 0.56 * W, 0.825 * H], fill=(96, 200, 58))       # zeleny stitek PULL
    f = ImageFont.truetype(PISMO, 40)
    d.text((0.365 * W, 0.78 * H), "PULL", font=f, fill=(24, 60, 24), anchor="mm")
    d.rectangle([0, 0.9 * H, W, H], fill=(38, 38, 40))                               # sokl
    im.save(cesta)

obrazek_bok(os.path.join(TEX, "bok.png")); obrazek_predek(os.path.join(TEX, "predek.png"))

# ---------------------------------------------------------------- scena jako gymnazium
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

def mat(jmeno, rgb, drsnost=0.8, kov=0.0, sum_=0.0, meritko=2.0, obrazek=None):
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if obrazek:
        tx = t.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(obrazek); tx.interpolation = 'Cubic'
        t.links.new(tx.outputs["Color"], b.inputs["Base Color"])
    elif sum_:
        tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = meritko; tex.inputs["Detail"].default_value = 6.0
        ramp = t.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = srgb(tuple(max(0, v * (1 - sum_)) for v in rgb))
        ramp.color_ramp.elements[1].color = srgb(tuple(min(255, v * (1 + sum_)) for v in rgb))
        t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    return m

M = {
    "skrin": mat("skrin", (66, 68, 70), 0.45, kov=0.3),
    "bok": mat("bok", (0, 0, 0), 0.35, obrazek=os.path.join(TEX, "bok.png")),
    "predek": mat("predek", (0, 0, 0), 0.25, obrazek=os.path.join(TEX, "predek.png")),
    "dlazba": mat("dlazba", (182, 178, 170), 0.9, sum_=0.07, meritko=6.0),
    "spara": mat("spara", (140, 136, 128), 0.95),
    "obrubnik": mat("obrubnik", (150, 146, 138), 0.9, sum_=0.06, meritko=8.0),
    "lavicka": mat("lavicka", (138, 92, 52), 0.7),
    "kov": mat("kov", (52, 58, 54), 0.5, kov=0.5),
    "ker": mat("ker", (54, 98, 40), 0.9, sum_=0.32, meritko=9.0),
    "kos": mat("kos", (38, 70, 46), 0.5, kov=0.3),
    "cerna": mat("cerna", (14, 14, 14), 0.9),
}
# divoke krovi: nekolik zeleni (i zlutava a tmava), suche hnede, plevel
KRE = [mat(f"krovi{i}", c, 0.9, sum_=0.3, meritko=9.0) for i, c in
       enumerate([(54, 98, 40), (70, 108, 44), (44, 82, 36), (88, 112, 50), (62, 92, 46)])]
SUCHE = mat("suche", (122, 104, 62), 0.95, sum_=0.25, meritko=9.0)
PLEVEL = [mat("plevel0", (124, 140, 66), 0.95, sum_=0.25, meritko=12.0), mat("plevel1", (146, 136, 84), 0.95, sum_=0.25, meritko=12.0)]
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

OKRAJ = 0.3                                     # dlazba od severnich hran policka
PC = OKRAJ + 2.0 * K                            # stred dlazby (4 x 4 m krat K) v severnim rohu
def B(x, y, z):
    """skupina -> Blender: skupina je navrzena kolem stredu policka C, zvetsena K krat a posunuta do severniho rohu"""
    return Vector((PC + (y - C) * K, -(PC + (x - C) * K), z * K))

def Bp(x, y, z):
    """policko -> Blender bez zvetseni (divoke krovi)"""
    return Vector((y, -x, z))

def kvadr(m, x0, x1, y0, y1, z0, z1, pevne=False):
    """kvadr; pevne = na policku bez zvetseni (dlazba)"""
    bm = bm_pro(m); b_ = (lambda x, y, z: Vector((y, -x, z))) if pevne else B
    v = [bm.verts.new(b_(x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        bm.faces.new([v[i] for i in f])

def mnohostena(m, body, steny):
    bm = bm_pro(m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])

def obraz(m, rohy):
    """ctyruhelnik s obrazkem: rohy v poradi vlevo dole, vpravo dole, vpravo nahore, vlevo nahore (jak ho vidi divak)"""
    bm = bm_pro(m); uv = bm.loops.layers.uv.verify()
    f = bm.faces.new([bm.verts.new(B(*p)) for p in rohy])
    for smycka, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        smycka[uv].uv = (u, v)

# ---------------------------------------------------------------- automat, lavicka, ker, dlazba
AX0 = C - 1.45; AX1 = AX0 + 0.85                # predek k jihozapadu (+x), hloubka 85 cm
AY0 = C - 1.05; AY1 = AY0 + 0.9                  # sirka 90 cm, bok s polepem k jihovychodu (+y)
AZ0, AZ1 = 0.04, 1.83
kvadr(M["skrin"], AX0, AX1, AY0, AY1, AZ0, AZ1)
for xx in (AX0 + 0.06, AX1 - 0.1):                                            # nozicky
    for yy in (AY0 + 0.06, AY1 - 0.1):
        kvadr(M["kov"], xx, xx + 0.04, yy, yy + 0.04, 0.0, AZ0)
obraz(M["predek"], [(AX1 + 0.004, AY0, AZ0), (AX1 + 0.004, AY1, AZ0), (AX1 + 0.004, AY1, AZ1), (AX1 + 0.004, AY0, AZ1)])
obraz(M["bok"], [(AX1, AY1 + 0.004, AZ0), (AX0, AY1 + 0.004, AZ0), (AX0, AY1 + 0.004, AZ1), (AX1, AY1 + 0.004, AZ1)])

def lavicka(x, y, uhel):
    """lavicka 1,6 m jako u gymnazia; uhel: kam se sedici diva (rad)"""
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
lavicka(AX1 + 1.4, (AY0 + AY1) / 2, math.pi)                               # pred automatem, sedi se k nemu

# dlazba 4 x 4 m z betonovych dlazdic 50 cm se sparami, kolem obrubnik 15 cm, uprostred policka
D0, D1, OBR, Z_D = C - 2.0, C + 2.0, 0.15, 0.03
for (x0, x1, y0, y1) in ((D0, D1, D0, D0 + OBR), (D0, D1, D1 - OBR, D1), (D0, D0 + OBR, D0 + OBR, D1 - OBR), (D1 - OBR, D1, D0 + OBR, D1 - OBR)):
    kvadr(M["obrubnik"], x0, x1, y0, y1, 0.0, Z_D + 0.03)
kvadr(M["spara"], D0 + OBR, D1 - OBR, D0 + OBR, D1 - OBR, 0.0, Z_D - 0.004)
n_ = int(round((D1 - D0 - 2 * OBR) / 0.5)); kr = (D1 - D0 - 2 * OBR) / n_
for i in range(n_):
    for j in range(n_):
        x, y = D0 + OBR + kr * i, D0 + OBR + kr * j
        kvadr(M["dlazba"], x + 0.012, x + kr - 0.012, y + 0.012, y + kr - 0.012, 0.0, Z_D)

from mathutils import Matrix, noise
def ker(cx, cy, r, vyska, materialy, seed, v_policku=False, chumacu=9, deleni=3):
    """hrbolaty ker z chumacu koul: ve skupine (souradnice skupiny, zvetsi se K krat), nebo na policku (metry).
    Koule jdou rovnou do site materialu (bmesh) a hrbolky dela sum na vrcholech, ne objekt s modifikatorem na kazdou
    kouli: s divokym krovim je jich stovky a Blender by se s tolika objekty vlekl."""
    rnd = random.Random(seed)
    mapa, s = (Bp, 1.0) if v_policku else (B, K)
    for i in range(chumacu):
        a = rnd.random() * 2 * math.pi; d = r * 0.6 * math.sqrt(rnd.random())
        rr = r * (0.38 + 0.16 * rnd.random())
        zc = max(rr * 0.55, vyska * (0.45 + 0.5 * rnd.random()) * (1 - 0.4 * d / r) - rr * 0.3)
        stred_ = mapa(cx + d * math.cos(a), cy + d * math.sin(a), zc)
        bm = bm_pro(rnd.choice(materialy))
        nove_v = bmesh.ops.create_icosphere(bm, subdivisions=deleni, radius=rr * s, matrix=Matrix.Translation(stred_))["verts"]
        posun = Vector((rnd.random(), rnd.random(), rnd.random())) * 100
        for v in nove_v:                                   # hrbolky: sum podel normaly jako drive Clouds a Displace
            smer = (v.co - stred_).normalized()
            n_ = noise.noise(v.co / (0.09 * s * 4) + posun) * 0.5 + noise.noise(v.co / (0.09 * s * 2) + posun) * 0.25
            v.co += smer * n_ * rr * 0.55 * s
        for f in {f for v in nove_v for f in v.link_faces}: f.smooth = True

# kericek vpravo vedle automatu
ker(AX0 + 0.6, AY1 + 0.95, 0.6, 1.0, [M["ker"]], 5)

# odpadkovy kos vlevo vedle lavicky: zeleny plechovy valec s okrajem, plny az pres okraj
LX, LY = AX1 + 1.4, (AY0 + AY1) / 2                  # stred lavicky
KOSX, KOSY = LX, LY - 1.2
def valec(m, x, y, z0, z1, r, n=16):
    bm = bm_pro(m)
    dole = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z0)) for k in range(n)]
    nahore = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z1)) for k in range(n)]
    bm.faces.new(dole[::-1]); bm.faces.new(nahore)
    for k in range(n):
        bm.faces.new((dole[k], dole[(k + 1) % n], nahore[(k + 1) % n], nahore[k]))
valec(M["kos"], KOSX, KOSY, 0.04, 0.76, 0.22)
valec(M["kov"], KOSX, KOSY, 0.74, 0.79, 0.24)
valec(M["cerna"], KOSX, KOSY, 0.79, 0.792, 0.19)

# odpadky: papiry, plechovky, PET lahve, kelimky, sacky a zelene balicky z automatu, nejvic kolem kose a pod lavickou
rnd_o = random.Random(11)
def odpadek(x, y, z0=0.0):
    x = min(max(x, D0 + 0.12), D1 + 0.5); y = min(max(y, D0 + 0.12), D1 + 0.5)    # jen na dlazbe a u ni, ne za policko
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
for i in range(22):                                                              # kolem kose
    odpadek(KOSX + rnd_o.gauss(0, 0.5), KOSY + rnd_o.gauss(0, 0.5))
for i in range(5):                                                               # pres okraj kose
    a = rnd_o.random() * 2 * math.pi
    odpadek(KOSX + 0.1 * math.cos(a), KOSY + 0.1 * math.sin(a), 0.79)
for i in range(12):                                                              # pod lavickou a pred ni
    odpadek(LX + rnd_o.uniform(-0.6, 0.6), LY + rnd_o.uniform(-0.85, 0.85))
for i in range(25):                                                              # po cele dlazbe
    odpadek(rnd_o.uniform(D0 + 0.25, D1 - 0.25), rnd_o.uniform(D0 + 0.25, D1 - 0.25))
for i in range(10):                                                              # zafoukane do krovi u dlazby
    if rnd_o.random() < 0.5: odpadek(D1 + rnd_o.uniform(0.0, 0.5), rnd_o.uniform(D0, D1))
    else: odpadek(rnd_o.uniform(D0, D1), D1 + rnd_o.uniform(0.0, 0.5))

# divoke neudrzovane krovi na zbytku policka (metry na policku, stejne zvetsene jako skupina), u dlazby nizsi,
# at lavicka a automat zustanou videt; v mezerach plevel
D_KRAJ = OKRAJ + 4.0 * K                              # jizni a vychodni hrana dlazby na policku
rnd_k = random.Random(21)
kere = []
for pokus in range(4000):
    r = K * rnd_k.uniform(0.45, 0.95)
    x, y = rnd_k.uniform(0.15 + r, T - 0.15 - r), rnd_k.uniform(0.15 + r, T - 0.15 - r)
    if x - r < D_KRAJ + 0.25 and y - r < D_KRAJ + 0.25:                            # na dlazbe ne
        continue
    if any(math.hypot(x - a, y - b) < 0.72 * (r + c) for a, b, c, _ in kere):
        continue
    u_dlazby = math.hypot(max(x - D_KRAJ, 0), max(y - D_KRAJ, 0)) - r          # mezera mezi kerem a dlazbou
    vyska = K * rnd_k.uniform(0.75, 1.6)
    if u_dlazby < 2.2 * K: vyska = min(vyska, K * 0.6 + 0.3 * u_dlazby)                 # u dlazby nizsi
    kere.append((x, y, r, vyska))
for i, (x, y, r, vyska) in enumerate(kere):
    mats = rnd_k.sample(KRE, 2) + ([SUCHE] if rnd_k.random() < 0.3 else [])
    ker(x, y, r, vyska, mats, 100 + i, v_policku=True, chumacu=rnd_k.randint(7, 12))
plevel, trsy = 0, []
for pokus in range(1500):
    x, y = rnd_k.uniform(0.4, T - 0.4), rnd_k.uniform(0.4, T - 0.4)
    if x < D_KRAJ + 0.15 and y < D_KRAJ + 0.15:
        continue
    if any(math.hypot(x - a, y - b) < c * 0.95 for a, b, c, _ in kere):
        continue
    r = K * rnd_k.uniform(0.18, 0.3)
    if any(math.hypot(x - a, y - b) < 1.6 * (r + c) for a, b, c in trsy):
        continue
    trsy.append((x, y, r))
    ker(x, y, r, r * 1.6, PLEVEL + [SUCHE], 500 + plevel, v_policku=True, chumacu=4, deleni=2)
    plevel += 1
print("kru", len(kere), "plevele", plevel)

for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)
# ---------------------------------------------------------------- postavy (druhy obrazek do animace, POSTAVY=1)
# Hrac 1. 10.: "spawnem holky kolem skoly a automatu". Jako u sochy (socha/render_socha.py) ve 2x jako skupina:
# tmavovlasa (College Girl) plati u automatu, Character Girl sedi na lavicce celem k automatu, Galaxia s nakupem
# odchazi po dlazbe k divakovi. Modely v postavy/ (autori v AUTORI-MODELU.md), pozy v postavy/postavy.py.
if os.environ.get("POSTAVY", "") == "1":
    sys.path.insert(0, os.path.join(TU, "..", "postavy"))
    import postavy as PO

    def do_sceny(meshe, kotva, gx, gy, gz, uhel):
        """postava (celem k -y, kotva = jeji bod, ktery ma stat v bode skupiny gx gy gz) celem ve smeru uhel"""
        PO.postav(meshe, Matrix.Translation(B(gx, gy, gz)) @ Matrix.Rotation(uhel, 4, 'Z') @ Matrix.Scale(K, 4) @ Matrix.Translation(-kotva))

    def na_lavicku(meshe, kotva, lavicka_, u):
        """bod sedu na sedak lavicky (x, y, uhel) ve vzdalenosti u od jejiho stredu, zady k operadlu"""
        x, y, uhel = lavicka_
        c, s = math.cos(uhel), math.sin(uhel)
        v = 0.05                                      # kousek dozadu k operadlu
        do_sceny(meshe, kotva, x + u * -s + v * -c, y + u * c + v * -s, 0.47, uhel)

    def placeni(arm, meshe):
        """leva ruka podel tela (jako ruce_dolu_college), prava z pozice T dopredu dolu a predlokti nahoru k ctecce karet"""
        PO.otoc_kost(arm, PO._kost(arm, "Shoulder_L_"), (0, 1, 0), math.radians(50))   # 76 davalo pazi do trupu (postavy.py, 2. 10.)
        PO.otoc_kost(arm, PO._kost(arm, "Shoulder_L_"), (1, 0, 0), math.radians(-6))
        PO.otoc_kost(arm, PO._kost(arm, "Elbow_L_"), (1, 0, 0), math.radians(-14))
        ram, loket = PO._kost(arm, "Shoulder_R_"), PO._kost(arm, "Elbow_R_")
        PO.otoc_kost(arm, ram, (0, 0, 1), math.radians(PL_DOPREDU))
        PO.otoc_kost(arm, ram, (1, 0, 0), math.radians(PL_DOLU))
        PO.otoc_kost(arm, loket, (1, 0, 0), math.radians(-PL_LOKET))
    PL_DOPREDU, PL_DOLU, PL_LOKET = (float(os.environ.get(n, d)) for n, d in (("PL_DOPREDU", "82"), ("PL_DOLU", "50"), ("PL_LOKET", "70")))
    cg = PO.nacti("college_girl", 1.62, priprava=placeni, nechat=PO.divka_a)
    do_sceny(cg, Vector((0, 0, 0)), AX1 + 0.5, AY1 - 0.32, Z_D, math.pi)      # u automatu, prava ruka u placeni

    ch, kotva = PO.sedici("character_people_girl_001")
    na_lavicku(ch, kotva, (LX, LY, math.pi), 0.3)                                # na lavicce blize ke kosi

    ga = PO.nacti_stojici("galaxia_anime_girl", 1.58, "ruce_dolu")
    do_sceny(ga, Vector((0, 0, 0)), C + 0.45, C + 1.5, Z_D, math.radians(40))  # vpravo vpredu, k divakovi

bpy.ops.mesh.primitive_plane_add(size=1, location=Vector((C, -C, 0.0)))
zem = bpy.context.object; zem.scale = (T, T, 1); zem.is_shadow_catcher = True

# ---------------------------------------------------------------- kamera a slunce jako gymnazium a Tatra
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

# stin na travu jen na 55 % jako u gymnazia: render s chytacem stinu a bez nej, rozdil je stin
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
json.dump({"px_m": PX_M, "policko_m": T, "meritko_skupiny": K, "ram": RAM, "rohy": rohy},
          open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
