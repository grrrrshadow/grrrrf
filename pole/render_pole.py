# -*- coding: utf-8 -*-
# Pole marihuany a policko brambor (hrac 1. 10.: "udelame pole marihuany 4x5 a policko brambor 3x3", "vem si objekty
# kytek na to pole marihuany, obrazek nahradi marihuanovou plantaz").
# - Marihuana: obrazek pro marihuanovou plantaz hry. Ta je ted ovocna plantaz zakladni grafiky, ktera pestuje marihuanu
#   (forclaude industry_cmd.cpp SetupMarijuanaPlantation, rozlozeni _tile_table_fruit_plantation_0: x 0 az 4, y 0 az 3),
#   proto 5 policek k jihozapadu a 4 k jihovychodu. Rostliny jsou modely od sochy (rostliny/rostliny.py), zelene jako
#   naklad MARI, 3,6 az 5 m (hrac u sochy: "kytky rostou 5 metru vysoko"), v radach na zahonech, uprostred polni cesta,
#   na jejim severovychodnim konci kulna a nadrze na vodu.
# - Brambory: 3 x 3, pro naklad BRAM (nase brambory). Hrebeny s natí, jihozapadni cast uz sklizena: hole hrebeny
#   s bramborami na zemi, kupa brambor, pytle a bedny.
# Jen obrazky jako gymnazium a automat, do hry je zabuduje session hry ve forclaude. Kamera, meritko a svetlo jako
# gymnazium (gymnazium/render_gymnazium.py): ortho 30 st. shora, 12,2 px/m v zin4 (policko 14,84 m), skutecna velikost,
# stin na travu 55 %. Pod polem je zemina az skoro k hranam pozemku, uplne na kraji (25 cm) je pruhledne, tam je trava hry.
#   POLE=marihuana python3 render_pole.py <vystup.png>
#   POLE=brambory  python3 render_pole.py <vystup.png>
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu pozemku.
# Obrazek: severni roh pozemku na celem pixelu (delitelnem 4 kvuli 8bpp ve hre), 32 px do stran a dolu, 96 px nahoru.
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image

VYSTUP = sys.argv[-1]
POLE = os.environ.get("POLE", "marihuana")
FAZE = int(os.environ.get("FAZE", "1"))         # faze rustu marihuany: 1 kere, 2 vysoke spicate (brambory jen jeden obrazek)
PX_M = 12.2
T = 256 / (math.sqrt(2) * PX_M)               # policko 14,84 m
NX, NY = (5, 4) if POLE == "marihuana" else (3, 3)
PX, PY = NX * T, NY * T
OKRAJ, NAD = 32, 96
W = (NX + NY) * 128 + 2 * OKRAJ
H = (NX + NY) * 64 + NAD + OKRAJ
SEVER = (OKRAJ + NX * 128, NAD)
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = int(os.environ.get("SAMPLES", "128"))
scene.cycles.filter_width = 1.5
scene.render.resolution_x, scene.render.resolution_y = W, H; scene.render.resolution_percentage = 100
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
    """material; sum_ = jak moc se barva meni sumem (zemina, drevo), at plochy nejsou mrtve"""
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if sum_:
        tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = meritko
        tex.inputs["Detail"].default_value = 6.0
        ramp = t.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = srgb(tuple(max(0, v * (1 - sum_)) for v in rgb))
        ramp.color_ramp.elements[1].color = srgb(tuple(min(255, v * (1 + sum_)) for v in rgb))
        t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    return m

M = {
    "zemina": mat("zemina", (98, 72, 50), 0.95, sum_=0.12, meritko=3.0),        # brazda mezi zahony
    "zahon": mat("zahon", (118, 88, 60), 0.95, sum_=0.12, meritko=4.0),         # nakypreny zahon, sussi a svetlejsi
    "cesta": mat("cesta", (150, 128, 96), 0.95, sum_=0.1, meritko=2.0),         # ujezdena polni cesta
    "kolej": mat("kolej", (118, 98, 72), 0.95, sum_=0.1, meritko=3.0),
    "trava": mat("trava", (92, 124, 58), 0.9, sum_=0.2, meritko=6.0),
    "prkna": mat("prkna", (112, 82, 54), 0.85, sum_=0.15, meritko=1.5),        # drevo kulny
    "plech": mat("plech", (128, 132, 134), 0.45, kov=0.5, sum_=0.08, meritko=2.0),
    "tmava": mat("tmava", (40, 34, 28), 0.9),
    "sklo": mat("sklo", (40, 48, 58), 0.2),
    "nadrz": mat("nadrz", (226, 228, 224), 0.4),                                # IBC nadrz, bila
    "klec": mat("klec", (150, 152, 150), 0.4, kov=0.7),
    "paleta": mat("paleta", (176, 140, 96), 0.8),
    "brambora": mat("brambora", (206, 172, 112), 0.75, sum_=0.12, meritko=30.0),
    "pytel": mat("pytel", (150, 112, 70), 0.9, sum_=0.15, meritko=20.0),       # jutovy pytel jako na V3S
    "bedna": mat("bedna", (168, 132, 88), 0.8, sum_=0.12, meritko=8.0),
    "nat": mat("nat", (58, 100, 40), 0.85, sum_=0.25, meritko=14.0),           # nat brambor
    "nat2": mat("nat2", (78, 118, 48), 0.85, sum_=0.25, meritko=14.0),
    "kvet_b": mat("kvet_b", (240, 238, 228), 0.6), "kvet_f": mat("kvet_f", (184, 156, 214), 0.6),
}

def kupa_mat():
    """kupa brambor: hrbolky po bramborach (Voronoi, asi 11 cm) s tmavymi sparami mezi nimi, ne jako pisek"""
    m = bpy.data.materials.new("kupa_brambor"); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.8
    sou = t.nodes.new('ShaderNodeTexCoord')
    vor = t.nodes.new('ShaderNodeTexVoronoi'); vor.feature = 'DISTANCE_TO_EDGE'; vor.inputs["Scale"].default_value = 9.0
    t.links.new(sou.outputs["Object"], vor.inputs["Vector"])
    ramp = t.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = srgb((70, 48, 26))
    ramp.color_ramp.elements[1].position = 0.18; ramp.color_ramp.elements[1].color = srgb((200, 162, 102))
    t.links.new(vor.outputs["Distance"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = t.nodes.new('ShaderNodeBump'); bump.inputs["Strength"].default_value = 0.8; bump.inputs["Distance"].default_value = 0.05
    t.links.new(vor.outputs["Distance"], bump.inputs["Height"]); t.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m
M["kupa"] = kupa_mat()

SITE = {}
def bm_pro(m):
    if m.name not in SITE: SITE[m.name] = (m, bmesh.new())
    return SITE[m.name][1]

def B(x, y, z):
    return Vector((y, -x, z))

def kvadr(m, x0, x1, y0, y1, z0, z1):
    bm = bm_pro(m)
    v = [bm.verts.new(B(x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        bm.faces.new([v[i] for i in f])

def mnohostena(m, body, steny):
    bm = bm_pro(m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])

def hreben(m, osa, a0, a1, b, sirka_dole, sirka_nahore, vyska, z0):
    """zahon nebo hrebek: lichobeznik podel osy ('x' nebo 'y') od a0 do a1, stred v b"""
    d, h = sirka_dole / 2, sirka_nahore / 2
    prurez = [(-d, z0), (d, z0), (h, z0 + vyska), (-h, z0 + vyska)]
    if osa == 'x':
        body = [(a, b + u, z) for a in (a0, a1) for u, z in prurez]
    else:
        body = [(b + u, a, z) for a in (a0, a1) for u, z in prurez]
    mnohostena(m, body, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)])

Z_ZEM = 0.035
ZEM0 = 0.25                                       # zemina od hran pozemku
rnd = random.Random(5)

if POLE == "marihuana":
    sys.path.insert(0, os.path.join(TU, "..", "rostliny"))
    import rostliny as RO
    # polni cesta podel x uprostred (od severovychodni hrany k jihozapadni), dve koleje a trava mezi nimi
    YT = PY / 2
    C0, C1 = YT - 1.7, YT + 1.7
    kvadr(M["zemina"], ZEM0, PX - ZEM0, ZEM0, PY - ZEM0, 0.0, Z_ZEM)
    kvadr(M["cesta"], ZEM0, PX - ZEM0, C0, C1, 0.0, Z_ZEM + 0.01)
    for k in (-0.75, 0.75):
        kvadr(M["kolej"], ZEM0, PX - ZEM0, YT + k - 0.22, YT + k + 0.22, 0.0, Z_ZEM + 0.013)
    kvadr(M["trava"], ZEM0, PX - ZEM0, YT - 0.4, YT + 0.4, 0.0, Z_ZEM + 0.02)
    # kulna u severovychodniho konce cesty, za ni (k jihovychodu): drevena, pultova plechova strecha, dvere k jihozapadu
    KX0, KX1, KY0, KY1 = 0.9, 5.3, C1 + 0.6, C1 + 4.6
    ZK, ZK1 = 2.5, 3.1
    kvadr(M["prkna"], KX0, KX1, KY0, KY1, 0.0, ZK)
    mnohostena(M["prkna"], [(KX0, KY0, ZK), (KX1, KY0, ZK), (KX1, KY1, ZK), (KX0, KY1, ZK), (KX0, KY0, ZK1), (KX0, KY1, ZK1)],
               [(0, 1, 2, 3), (0, 4, 1), (3, 2, 5), (0, 3, 5, 4)])                     # stity pod pultovou strechou
    O = 0.3
    mnohostena(M["plech"], [(KX0 - O, KY0 - O, ZK1 + 0.08), (KX0 - O, KY1 + O, ZK1 + 0.08), (KX1 + O, KY1 + O, ZK - 0.12),
                            (KX1 + O, KY0 - O, ZK - 0.12), (KX0 - O, KY0 - O, ZK1 + 0.14), (KX0 - O, KY1 + O, ZK1 + 0.14),
                            (KX1 + O, KY1 + O, ZK - 0.06), (KX1 + O, KY0 - O, ZK - 0.06)],
               [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    for k in range(int((KY1 - KY0) / 0.22)):                                          # spary mezi prkny na stene k divakovi
        y = KY0 + 0.22 * (k + 1)
        kvadr(M["tmava"], KX1, KX1 + 0.012, y - 0.012, y + 0.012, 0.05, ZK - 0.05)
    kvadr(M["tmava"], KX1, KX1 + 0.02, KY0 + 0.5, KY0 + 1.6, 0.0, 2.1)                # dvere k jihozapadu
    kvadr(M["prkna"], KX1 + 0.02, KX1 + 0.05, KY0 + 0.55, KY0 + 1.55, 0.02, 2.05)
    kvadr(M["sklo"], KX0 + 1.4, KX0 + 2.6, KY1, KY1 + 0.02, 1.3, 2.0)                 # okno k jihovychodu
    kvadr(M["prkna"], KX0 + 1.35, KX0 + 2.65, KY1, KY1 + 0.05, 1.25, 1.3)
    # tri IBC nadrze na vodu na paletach vedle kulny, k ceste
    for i in range(3):
        nx0, ny0 = KX1 + 0.6, KY0 + 0.1 + 1.25 * i
        kvadr(M["paleta"], nx0, nx0 + 1.2, ny0, ny0 + 1.0, 0.0, 0.15)
        kvadr(M["nadrz"], nx0 + 0.05, nx0 + 1.15, ny0 + 0.05, ny0 + 0.95, 0.15, 1.15)
        for t in (0.0, 0.33, 0.66, 1.0):                                              # klec: svisle a vodorovne trubky
            kvadr(M["klec"], nx0 + 0.03 + 1.12 * t - 0.015, nx0 + 0.03 + 1.12 * t + 0.015, ny0 + 0.98, ny0 + 1.0, 0.15, 1.2)
            kvadr(M["klec"], nx0 + 1.18, nx0 + 1.2, ny0 + 0.03 + 0.92 * t - 0.015, ny0 + 0.03 + 0.92 * t + 0.015, 0.15, 1.2)
        for z in (0.55, 1.18):
            kvadr(M["klec"], nx0 + 1.18, nx0 + 1.2, ny0, ny0 + 1.0, z - 0.015, z + 0.015)
            kvadr(M["klec"], nx0, nx0 + 1.2, ny0 + 0.98, ny0 + 1.0, z - 0.015, z + 0.015)
        kvadr(M["tmava"], nx0 + 0.45, nx0 + 0.75, ny0 + 0.35, ny0 + 0.65, 1.15, 1.22)  # vicko
    VOLNO = [(KX0 - 0.6, KX1 + 2.4, KY0 - 0.3, KY1 + 0.6)]                            # tady rostliny nejsou
    # rady rostlin podel x na zahonech, z obou stran cesty
    # Rostliny jako u sochy, ale z dalky (45 px) byly kosata sativa i vysoka stihla rostlina jako smrcky: model sativy je
    # kuzel z pater listu. Proto sativa se zkracenym vrskem (jako zastipnute konopi), zakulaceny ker, a pres ni mlada
    # rostlinka (small_cannabis_plant) stejne velka, jejiz velke dlanite listy trci z keře ven: podle nich je to konopi.
    # Vysoka stihla rostlina tu neni. Barvy: zive rostliny na slunci svetlejsi a zlutejsi nez susena kupka MARI
    # (rostliny/rostliny.py), prechod tmava -> svetla uz od jasu SVETLA_OD. Pata 0,2 m v zahonu, at neni videt holy stonek.
    RADA, ROZESTUP = float(os.environ.get("RADA", "4.2")), float(os.environ.get("ROZESTUP", "3.3"))
    V0, V1 = float(os.environ.get("VYSKA_OD", "2.6")), float(os.environ.get("VYSKA_DO", "3.4"))
    K0, KORUNA = float(os.environ.get("KORUNA_OD", "1.45")), float(os.environ.get("KORUNA", "1.75"))   # polomer koruny
    KRAJ = KORUNA + 0.7                                                                # kmen od hran pozemku (i listy)
    TMAVA, SVETLA = (tuple(int(c) for c in os.environ.get(n, d).split(",")) for n, d in (("TMAVA", "56,112,14"), ("SVETLA", "124,172,38")))
    SVETLA_OD = float(os.environ.get("SVETLA_OD", "0.15"))
    sativa = RO.nacti("cannabis_sativa_plant")[0][0]; mlada, mlada_pomer = RO.nacti("small_cannabis_plant"); mlada = mlada[0]
    # Faze 2 (hrac: "druha faze udelej ty spicaty smrcky vysoky"): na stejnych mistech puvodni spicata sativa
    # a ctvrtina vysokych stihlych, 3,8 az 5 m, zuzene na KORUNA2, v barvach MARI jako u sochy (bez zesvetleni).
    V0_2, V1_2 = float(os.environ.get("VYSKA2_OD", "3.8")), float(os.environ.get("VYSKA2_DO", "5.0"))
    KORUNA2, VYSOKYCH2 = float(os.environ.get("KORUNA2", "1.4")), float(os.environ.get("VYSOKYCH2", "0.25"))
    if FAZE == 2:
        VYSOKA = RO.nacti("cannabis_plant"); KOSATA = (sativa, RO.nacti("cannabis_sativa_plant")[1])
        rnd2 = random.Random(13)                                                       # jen druh ve fazi 2, mista stejna
    for m_ in (sativa.materials[:] + mlada.materials[:] if FAZE == 1 else []):
        for n_ in (m_.node_tree.nodes if m_ and m_.use_nodes else []):
            if n_.type == 'VALTORGB':
                n_.color_ramp.elements[0].color = srgb(TMAVA)
                n_.color_ramp.elements[1].color = srgb(SVETLA); n_.color_ramp.elements[1].position = SVETLA_OD

    def ker(od, stlac, rozsir):
        """kopie sativy: nad vyskou od (podil) stlacena na stlac a rozsirena az o rozsir; vyska zase 1.
        Vrati (sit, polomer koruny k vysce)."""
        me = sativa.copy()
        v = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", v); v = v.reshape(-1, 3)
        z = v[:, 2].copy()
        nad = np.clip((z - od) / (1 - od), 0, 1)
        k = np.where(z > od, 1 + rozsir * np.sin(nad * math.pi / 2), 1.0)
        v[:, 0] *= k; v[:, 1] *= k
        v[:, 2] = np.where(z > od, od + (z - od) * stlac, z)
        v[:, 2] /= v[:, 2].max()
        me.vertices.foreach_set("co", v.ravel()); me.update()
        return me, float(np.sqrt(v[:, 0] ** 2 + v[:, 1] ** 2).max())
    KERE = [ker(0.4, 0.4, 0.0), ker(0.45, 0.45, 0.1)]
    MLADA_K = float(os.environ.get("MLADA_K", "0.85"))                                 # mlada rostlinka k vysce keře
    MLADA_S = float(os.environ.get("MLADA_S", "1.2"))                                  # a k jeho sirce: listy trci ven
    rady = []
    y = KRAJ
    while y < C0 - KORUNA - 0.2:
        rady.append(y); y += RADA
    rady = [r + (C0 - KORUNA - 0.2 - rady[-1]) / 2 for r in rady]                     # srovnat k ceste i k hrane
    y = C1 + KORUNA + 0.2; rady2 = []
    while y < PY - KRAJ:
        rady2.append(y); y += RADA
    rady2 = [r + (PY - KRAJ - rady2[-1]) / 2 for r in rady2]
    pocet = 0
    for yr in rady + rady2:
        hreben(M["zahon"], 'x', ZEM0 + 0.4, PX - ZEM0 - 0.4, yr, 1.3, 0.8, 0.14, 0.0)
        x = KRAJ + rnd.uniform(0, 0.4)
        while x < PX - KRAJ:
            xx, yy = x + rnd.uniform(-0.15, 0.15), yr + rnd.uniform(-0.12, 0.12)
            x += ROZESTUP * rnd.uniform(0.92, 1.08)
            if any(a0 - KORUNA < xx < a1 + KORUNA and b0 - KORUNA < yy < b1 + KORUNA for a0, a1, b0, b1 in VOLNO):
                continue
            if rnd.random() < 0.03:                                                    # tu a tam chybi
                continue
            vlna = 0.5 + 0.5 * noise.noise(Vector((xx / 9.0, yy / 9.0, 0.5)))           # sousedni rostliny podobne vysoke
            # nahodna cisla v obou fazich stejne a ve stejnem poradi, at jsou rostliny na stejnych mistech
            t_ = min(1.0, max(0.0, 0.6 * vlna + 0.4 * rnd.random()))
            j_ = rnd.uniform(-0.2, 0.2); kr = rnd.choice(KERE); u1 = rnd.uniform(0, 2 * math.pi); u2 = rnd.uniform(0, 2 * math.pi)
            pata = Matrix.Translation(B(xx, yy, -0.08))
            if FAZE == 1:
                vys = V0 + (V1 - V0) * t_; pol = K0 + (KORUNA - K0) * min(1.0, max(0.0, t_ + j_))
                me, pomer = kr
                sirka = pol / pomer                                                     # ker sirsi nez vysoky
                o = bpy.data.objects.new("konopi", me); scene.collection.objects.link(o)
                o.matrix_world = pata @ Matrix.Rotation(u1, 4, 'Z') @ Matrix.Diagonal((sirka, sirka, vys, 1.0))
                v2 = vys * MLADA_K; s2 = min(pol * MLADA_S, KORUNA + 0.25) / mlada_pomer
                o = bpy.data.objects.new("listy", mlada); scene.collection.objects.link(o)
                o.matrix_world = pata @ Matrix.Rotation(u2, 4, 'Z') @ Matrix.Diagonal((s2, s2, v2, 1.0))
            else:
                vys = V0_2 + (V1_2 - V0_2) * t_
                druh = VYSOKA if rnd2.random() < VYSOKYCH2 else KOSATA
                sirka = min(vys, KORUNA2 / druh[1])                                     # spicata, koruna nejvys KORUNA2
                for me in (druh[0] if isinstance(druh[0], list) else [druh[0]]):
                    o = bpy.data.objects.new("konopi", me); scene.collection.objects.link(o)
                    o.matrix_world = pata @ Matrix.Rotation(u1, 4, 'Z') @ Matrix.Diagonal((sirka, sirka, vys, 1.0))
            pocet += 1
    print("faze", FAZE, "rad", len(rady) + len(rady2), "rostlin", pocet)

else:
    # hrebeny brambor podel y (na obrazku doprava dolu), na nich nat; jihozapadni cast sklizena
    # (hrac: "jo to vypada dobre ty brambory, to staci tenhle jeden obrazek bez fazi rustu")
    kvadr(M["zemina"], ZEM0, PX - ZEM0, ZEM0, PY - ZEM0, 0.0, Z_ZEM)
    ROZ, HV = 0.75, 0.22                                                               # rozestup a vyska hrebenu
    SKLIZENO = PX - float(os.environ.get("SKLIZENO", "9.0"))                           # od tohohle x uz sklizeno
    Y0, Y1 = 0.9, PY - 0.9
    def nat_brambor(seed):
        """jeden trs nati: lisky jako hrbolate koule do kopule, u nekterych kvety; jedna sit, materialy podle ploch"""
        r_ = random.Random(seed); bm = bmesh.new()
        me = bpy.data.meshes.new(f"nat{seed}")
        for m in (M["nat"], M["nat2"], M["kvet_b"], M["kvet_f"]): me.materials.append(m)
        vys = r_.uniform(0.4, 0.52); pol = r_.uniform(0.2, 0.26)                     # uzsi nez hrebeny: brazdy videt
        for i in range(r_.randint(8, 11)):
            a = r_.random() * 2 * math.pi; d = pol * 0.75 * math.sqrt(r_.random())
            z = vys * (0.35 + 0.5 * (1 - d / pol) * r_.random() + 0.15)
            rr = r_.uniform(0.08, 0.12)
            stred_ = Vector((d * math.cos(a), d * math.sin(a), min(z, vys - rr * 0.6)))
            nove = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=rr, matrix=Matrix.Translation(stred_))["verts"]
            posun = Vector((r_.random(), r_.random(), r_.random())) * 50
            for v in nove:
                smer = (v.co - stred_).normalized()
                v.co += smer * noise.noise(v.co / 0.06 + posun) * rr * 0.5
                v.co.z = stred_.z + (v.co.z - stred_.z) * 0.75
            mi = r_.choice((0, 1))
            for f in {f for v in nove for f in v.link_faces}:
                f.material_index = mi; f.smooth = True
        if r_.random() < 0.3:                                                           # kvete: hlavne bile, nekdy fialove
            mi = 2 if r_.random() < 0.75 else 3
            for i in range(r_.randint(2, 4)):
                a = r_.random() * 2 * math.pi; d = pol * 0.6 * math.sqrt(r_.random())
                nove = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035, matrix=Matrix.Translation((d * math.cos(a), d * math.sin(a), vys - 0.02)))["verts"]
                for f in {f for v in nove for f in v.link_faces}:
                    f.material_index = mi
        bm.to_mesh(me); bm.free()
        return me
    TRSY = [nat_brambor(100 + i) for i in range(10)]
    x = 1.0; hrebenu = trsu = 0; hrebeny_x = []
    while x < PX - 1.0:
        hrebeny_x.append(x); x += ROZ
    hrebeny_x = [h + (PX - 1.0 - hrebeny_x[-1]) / 2 for h in hrebeny_x]
    kolekce = bpy.data.collections.new("nat"); scene.collection.children.link(kolekce)
    for xh in hrebeny_x:
        sklizeny = xh > SKLIZENO
        hreben(M["zahon"], 'y', Y0, Y1, xh, 0.68, 0.26, HV, 0.0)
        hrebenu += 1
        if sklizeny:
            continue
        y = Y0 + 0.3 + rnd.uniform(0, 0.15)
        while y < Y1 - 0.3:
            o = bpy.data.objects.new("trs", rnd.choice(TRSY)); kolekce.objects.link(o)
            o.location = B(xh + rnd.uniform(-0.04, 0.04), y, HV - 0.03)
            o.rotation_euler[2] = rnd.uniform(0, 2 * math.pi)
            s = rnd.uniform(0.85, 1.15); o.scale = (s, s, s * rnd.uniform(0.9, 1.1))
            y += rnd.uniform(0.3, 0.4); trsu += 1
    # sklizena cast: brambory na hrebenech a mezi nimi (vic na hrebenech, kde se vyoraly)
    me_b = bpy.data.meshes.new("brambora"); bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.055); bm.to_mesh(me_b); bm.free(); me_b.materials.append(M["brambora"])
    kus = 0
    for xh in hrebeny_x:
        if xh <= SKLIZENO:
            continue
        for i in range(int((Y1 - Y0) * 3.0)):
            y = rnd.uniform(Y0 + 0.2, Y1 - 0.2); na_hrebeni = rnd.random() < 0.7
            xx = xh + (rnd.uniform(-0.12, 0.12) if na_hrebeni else rnd.choice((-1, 1)) * rnd.uniform(0.3, 0.4))
            o = bpy.data.objects.new("brambora", me_b); kolekce.objects.link(o)
            o.location = B(xx, y, (HV - 0.02 if na_hrebeni else Z_ZEM + 0.02))
            o.scale = (rnd.uniform(0.8, 1.3), rnd.uniform(0.7, 1.0), rnd.uniform(0.6, 0.8)); o.rotation_euler[2] = rnd.uniform(0, 6.3)
            kus += 1
    # kupa brambor, pytle a bedny na sklizene casti u jihovychodni strany
    KUX, KUY = PX - 4.2, PY - 5.2
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1.0, location=B(KUX, KUY, 0.0))
    RKX, RKY = 1.45, 1.7                                                               # polomery kupy podel x a y
    kupa = bpy.context.object; kupa.scale = (RKY, RKX, 0.95); kupa.data.materials.append(M["kupa"])
    bpy.context.view_layer.update()
    for v in kupa.data.vertices:                                                       # hrbolata, dole srovnana na zem
        if v.co.z < 0: v.co.z = 0.0
        v.co += v.normal * 0.06 * noise.noise(v.co * 7.0)
    for p in kupa.data.polygons: p.use_smooth = True
    for i in range(160):                                                               # jednotlive brambory po povrchu kupy
        a = rnd.random() * 2 * math.pi; t = math.sqrt(rnd.random())
        x_, y_ = RKX * t * math.cos(a), RKY * t * math.sin(a)
        z_ = 0.95 * math.sqrt(max(0.0, 1 - t * t))
        o = bpy.data.objects.new("brambora", me_b); kolekce.objects.link(o)
        o.location = B(KUX + x_, KUY + y_, z_ + 0.01)
        o.scale = (rnd.uniform(0.9, 1.4), rnd.uniform(0.8, 1.1), rnd.uniform(0.7, 0.9)); o.rotation_euler[2] = rnd.uniform(0, 6.3)
    def pytel(x, y, z, uhel, lezi=True):
        """jutovy pytel: lezici (0,75 x 0,45 x 0,28 m) nebo stojici zavazany"""
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=B(x, y, z + (0.14 if lezi else 0.32)))
        o = bpy.context.object
        o.scale = (0.22, 0.37, 0.15) if lezi else (0.24, 0.18, 0.33)                   # Blender x = hra y
        o.rotation_euler[2] = uhel; o.data.materials.append(M["pytel"])
        for p in o.data.polygons: p.use_smooth = True
        if not lezi:
            bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.09, radius2=0.03, depth=0.14, location=B(x, y, z + 0.69))
            bpy.context.object.data.materials.append(M["pytel"])
    PYX, PYY = PX - 2.3, PY - 8.6                                                     # paleta s pytli
    kvadr(M["paleta"], PYX - 0.6, PYX + 0.6, PYY - 1.0, PYY + 1.0, 0.0, 0.14)
    for vrstva, kusu in enumerate((4, 3, 2)):
        for i in range(kusu):
            pytel(PYX + rnd.uniform(-0.05, 0.05), PYY + (i - (kusu - 1) / 2) * 0.46, 0.14 + 0.24 * vrstva, rnd.uniform(-0.08, 0.08))
    for i, (x, y) in enumerate(((PX - 2.2, PY - 6.9), (PX - 2.75, PY - 6.6), (PX - 3.1, PY - 9.9))):
        pytel(x, y, 0.0, rnd.uniform(0, 3), lezi=False)
    def bedna(x, y, z, uhel):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=B(x, y, z + 0.16)); o = bpy.context.object
        o.scale = (0.6, 0.4, 0.32); o.rotation_euler[2] = uhel; o.data.materials.append(M["bedna"])
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=B(x, y, z + 0.3)); v = bpy.context.object        # brambory v bedne
        v.scale = (0.54, 0.34, 0.06); v.rotation_euler[2] = uhel; v.data.materials.append(M["brambora"])
    for i in range(3):
        for j in range(2):
            for k in range(2 if (i + j) % 2 else 3):
                bedna(PX - 6.6 + 0.66 * i, PY - 2.4 + 0.46 * j, 0.33 * k, 0.0)
    print("hrebenu", hrebenu, "trsu nate", trsu, "brambor na zemi", kus)

# ---------------------------------------------------------------- site do sceny
for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
# chytac stinu pod pozemkem: stiny na travu hry na krajich
bpy.ops.mesh.primitive_plane_add(size=1, location=B(PX / 2, PY / 2, 0.0))
zem = bpy.context.object; zem.scale = (PY, PX, 1); zem.is_shadow_catcher = True

# ---------------------------------------------------------------- kamera a slunce jako gymnazium
# stred obrazku lezi SEVER + (W/2, H/2) - SEVER px od severniho rohu; na zemi je to bod (gx, gy):
# vodorovne (gy - gx) * s, svisle (gx + gy) * s / 2, kde s = PX_M / odmocnina 2
s_ = PX_M / math.sqrt(2)
dx, dy = W / 2 - SEVER[0], H / 2 - SEVER[1]
gx, gy = (dy / (s_ / 2) - dx / s_) / 2, (dy / (s_ / 2) + dx / s_) / 2
stred = B(gx, gy, 0.0)
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); cil = bpy.context.object
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 120.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(W, H) / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = cil
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * -0.25 + Vector((0, 0, 1.0))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "5.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def na_pixel(p):
    bpy.context.view_layer.update()
    q = world_to_camera_view(scene, cam, p)
    return (q.x * W, (1 - q.y) * H)
rohy = {"sever": na_pixel(B(0, 0, 0)), "vychod": na_pixel(B(0, PY, 0)), "zapad": na_pixel(B(PX, 0, 0)), "jih": na_pixel(B(PX, PY, 0))}
print("rohy pozemku na obrazku", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()})
assert abs(rohy["sever"][0] - SEVER[0]) < 0.01 and abs(rohy["sever"][1] - SEVER[1]) < 0.01, "severni roh neni tam, kde ma byt"

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
json.dump({"px_m": PX_M, "policko_m": T, "policek": [NX, NY], "obrazek": [W, H], "pole": POLE, "rohy": rohy},
          open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
