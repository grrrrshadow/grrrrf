# -*- coding: utf-8 -*-
# Skladaci pole po dlazdicich (hrac 3. 10.): "pole marihuana, brambor, budou modularni skladana. zaklad je jedno policko
# bez kytky, dlazdice se bude opakovat. takhle prvni druhej a ctvrtej radek pet stejnych dlazdic a treti radek bude
# ctyri dlazdice cesty, opet stejne dlazdice a pata dlazdice bude bouda na konci cesty. tu boudu muzes zas prilozit jako
# kytky, das patou dlazdici jen cestu a prilozime boudu. takhle bude mit pole tri faze, bez kytek, s malyma kytkama a se
# vzrostlymi smrcky marihuany", "budem prikladat holky na marihuanove pole", "to same bramborove pole, uplne stejny na
# mensi plose, prikladat kytky. musime setrit Mb"; holky na bramborove pole zatim ne.
#
# Kazdy obrazek je jedno policko, vsechny maji stejny ram a stejne rohy:
# - zaklady (neprusvitne presne v kosoctverci policka): pole marihuany (zem se zahony), pole brambor (hrebeny), cesta
#   (trava a polni cesta podel x);
# - prikladaci vrstvy (jinde pruhledne, nic nepresahuje pod predni hrany policka, jen nahoru): bouda (kulna a nadrze na
#   konci cesty vedle ni, na trave u severozapadniho okraje), male a vzrostle kytky (i se stinem na zem), holky u okraju
#   cesty, holky pri praci u kytek na dlazdici pole (prace_*, zvlast pro male a vzrostle kytky, viz nize).
# Cesta prostredkem pole (hrac: "takhle bude cesta prostredkem pole, vzor je overlaping titles z toho grf", "normalne tam
# bude tvoje nynejsi cesta a pod ni postavim silnici pro auta, proto potrebuju aby ta cesta v marihuanovy plantazi byla
# overlaping, ze tam je obrazek ale muzu pod obrazkem stavet"): obrazek cesty je plny, ve hre se kresli jako prekryvajici
# obrazek pres silnici (jako ISR/DWE-style Objects II: placata budova vetsi nez dlazdice nebo posunuta pres vedlejsi
# policko; hrac: "jedno policko zaberou a druhe jen nakresli ale zustane volne"), silnici a zastavku si pod nim hrac
# postavi sam. Holky (hrac: "holky prikladej jen po stranach u kraje dlazdic cesty polem") stoji jen u severozapadniho
# nebo jihovychodniho okraje dlazdice cesty, ne uprostred, kde jezdi auta.
# Navaznost: zem a zahony jsou periodicke s periodou policka (sum zeme z periodickeho obrazku, zahony a hrebeny podel x
# pres cele policko a dal), rostliny stoji v kazdem policku na stejnych mistech. Stin na zem je ve vrstve kytek i od
# rostlin sousednich policek (ty stin vrhaji, ale nejsou videt), takze stiny na hranach policek navazuji.
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, policko x 0 az T, y 0 az T. Kamera jako u aut
# a budov (30 st. shora, azimut 45 st., 12,2 px/m ve 4x), svetlo a slabe stiny jako u sochy.
#   [ZIN=8] [SAMPLES=128] POLE=marihuana|brambory python3 render_dlazdice.py <vystupni adresar>
#   JEN=mari_zaklad,cesta,... jen nektere obrazky
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image

VYSTUP = sys.argv[-1]
os.makedirs(VYSTUP, exist_ok=True)
ZIN = int(os.environ.get("ZIN", "4"))
S4 = ZIN // 4
PX_M = 12.2 * ZIN / 4
T = 256 / (math.sqrt(2) * 12.2)                # policko 14,84 m (256 px ve 4x)
POLE = os.environ.get("POLE", "marihuana")
JEN = set(filter(None, os.environ.get("JEN", "").split(",")))
K = 2.0                                        # holky dvakrat vetsi jako u sochy, chatky a u aut
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM4, SEVER4 = (264, 200), (132, 64)           # ram a severni roh policka ve 4x (64 px nad nim na rostliny)
RAM, SEVER = (RAM4[0] * S4, RAM4[1] * S4), (SEVER4[0] * S4, SEVER4[1] * S4)

def B(x, y, z=0.0):
    """souradnice hry (m) -> Blender"""
    return Vector((y, -x, z))

# ---------------------------------------------------------------- scena, svetlo jako socha
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False
scene.cycles.samples = int(os.environ.get("SAMPLES", "128")); scene.cycles.filter_width = 1.5
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.render.resolution_x, scene.render.resolution_y = RAM; scene.render.resolution_percentage = 100
world = bpy.data.worlds.new("World"); scene.world = world; world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment'); wo = nt.nodes.new('ShaderNodeOutputWorld')
env.image = bpy.data.images.load(HDRI)
nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.9"))

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

def periodicky_sum(jmeno, n=512, beta=1.5, seed=1):
    """obrazek sumu, ktery navazuje sam na sebe (hrany do sebe): nahodne spektrum s utlumem 1/f^beta"""
    rng = np.random.default_rng(seed)
    f = np.fft.fft2(rng.standard_normal((n, n)))
    k = np.sqrt(np.fft.fftfreq(n)[:, None] ** 2 + np.fft.fftfreq(n)[None, :] ** 2)
    a = np.real(np.fft.ifft2(f * np.where(k > 0, 1.0 / np.maximum(k, 1.0 / n) ** beta, 0.0)))
    a = (a - a.min()) / (a.max() - a.min())
    img = bpy.data.images.new(jmeno, n, n, alpha=False, float_buffer=True)
    img.pixels.foreach_set(np.dstack([a, a, a, np.ones_like(a)]).astype(np.float32).ravel())
    img.colorspace_settings.name = 'Non-Color'
    return img
SUM = periodicky_sum("sum_zeme")

def mat(jmeno, rgb, drsnost=0.8, kov=0.0, sum_=0.0, opak=1):
    """material; sum_ = jak moc barvu meni periodicky sum (opak = kolikrat se sum na policko opakuje, cele cislo)"""
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if sum_:
        tc = t.nodes.new('ShaderNodeTexCoord'); mp = t.nodes.new('ShaderNodeMapping')
        mp.inputs["Scale"].default_value = (opak / T, opak / T, 1.0)
        t.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        ti = t.nodes.new('ShaderNodeTexImage'); ti.image = SUM; ti.extension = 'REPEAT'; ti.interpolation = 'Cubic'
        t.links.new(mp.outputs["Vector"], ti.inputs["Vector"])
        ramp = t.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = srgb(tuple(max(0, v * (1 - sum_)) for v in rgb))
        ramp.color_ramp.elements[1].color = srgb(tuple(min(255, v * (1 + sum_)) for v in rgb))
        t.links.new(ti.outputs["Color"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    m.diffuse_color = srgb(rgb)
    return m

M = {
    "zemina": mat("zemina", (98, 72, 50), 0.95, sum_=0.16),                 # brazda mezi zahony
    "zahon": mat("zahon", (118, 88, 60), 0.95, sum_=0.14, opak=2),          # nakypreny zahon, sussi a svetlejsi
    "trava": mat("trava", (92, 124, 58), 0.9, sum_=0.22),                    # mez u cesty
    "cesta": mat("cesta", (150, 128, 96), 0.95, sum_=0.12, opak=2),          # ujezdena polni cesta
    "kolej": mat("kolej", (118, 98, 72), 0.95, sum_=0.12, opak=3),
    "prkna": mat("prkna", (112, 82, 54), 0.85, sum_=0.15, opak=4),           # drevo kulny
    "plech": mat("plech", (128, 132, 134), 0.45, kov=0.5, sum_=0.08, opak=3),
    "tmava": mat("tmava", (40, 34, 28), 0.9),
    "sklo": mat("sklo", (40, 48, 58), 0.2),
    "nadrz": mat("nadrz", (226, 228, 224), 0.4),                              # IBC nadrz, bila
    "klec": mat("klec", (150, 152, 150), 0.4, kov=0.7),
    "paleta": mat("paleta", (176, 140, 96), 0.8),
    "nat": mat("nat", (58, 100, 40), 0.85, sum_=0.25, opak=12),              # nat brambor
    "nat2": mat("nat2", (78, 118, 48), 0.85, sum_=0.25, opak=12),
    "nat_mlada": mat("nat_mlada", (96, 140, 56), 0.85, sum_=0.2, opak=12),   # mlada nat, svetlejsi
    "kvet_b": mat("kvet_b", (240, 238, 228), 0.6), "kvet_f": mat("kvet_f", (184, 156, 214), 0.6),
}

SKUPINY = {}                                   # jmeno -> seznam objektu
def do_skupiny(jm, o):
    SKUPINY.setdefault(jm, []).append(o)
    return o
SITE = {}
def bm_pro(sk, m):
    if (sk, m.name) not in SITE: SITE[sk, m.name] = (m, bmesh.new())
    return SITE[sk, m.name][1]
def mnohostena(sk, m, body, steny):
    bm = bm_pro(sk, m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])
def kvadr(sk, m, x0, x1, y0, y1, z0, z1):
    b = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    mnohostena(sk, m, b, [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)])
def hreben(sk, m, y, x0, x1, sirka_dole, sirka_nahore, vyska):
    """zahon nebo hrebek podel x: lichobeznik od x0 do x1 se stredem v y"""
    d, h = sirka_dole / 2, sirka_nahore / 2
    b = [(x0, y - d, 0.0), (x0, y + d, 0.0), (x0, y + h, vyska), (x0, y - h, vyska),
         (x1, y - d, 0.0), (x1, y + d, 0.0), (x1, y + h, vyska), (x1, y - h, vyska)]
    mnohostena(sk, m, b, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 4, 7, 3), (1, 2, 6, 5), (3, 7, 6, 2)])
def site_do_sceny():
    for (sk, jm), (m, bm) in SITE.items():
        me = bpy.data.meshes.new(f"{sk}_{jm}"); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(f"{sk}_{jm}", me); scene.collection.objects.link(o); me.materials.append(m)
        do_skupiny(sk, o)
    SITE.clear()

# ---------------------------------------------------------------- zaklady: zem pres sousedni policka (vidi se jen stredni)
OD, DO = -T, 2 * T
Z_ZEM = 0.0
def zem(sk, m):
    kvadr(sk, m, OD, DO, OD, DO, -0.05, Z_ZEM)
# pole marihuany: 4 zahony na policko podel x (rady rostlin na nich), mezi nimi brazdy
RADY_M = [T / 8 + k * T / 4 for k in range(4)]
if POLE == "marihuana":
    zem("mari_zaklad", M["zemina"])
    for posun in (-T, 0.0, T):
        for y in RADY_M:
            hreben("mari_zaklad", M["zahon"], y + posun, OD, DO, 1.3, 0.8, 0.14)
# pole brambor: 20 hrebenu na policko podel x (rozestup T/20 = 0,74 m)
RADY_B = [T / 40 + k * T / 20 for k in range(20)]
HV = 0.22
if POLE == "brambory":
    zem("bram_zaklad", M["zemina"])
    for posun in (-T, 0.0, T):
        for y in RADY_B:
            hreben("bram_zaklad", M["zahon"], y + posun, OD, DO, 0.68, 0.26, HV)
# cesta: trava, polni cesta podel x uprostred policka, dve koleje a trava mezi nimi (jako na stare plantazi)
YT = T / 2
# cesta pro auta: ve hre jezdi ve dvou pruzich T/4 od stredu dlazdice (3,7 m), takze ujezdena cesta je 9,8 m siroka,
# v kazdem pruhu dve koleje od kol, uprostred pruh travy, po krajich trava 2,5 m (tam stoji holky)
C0, C1 = YT - 4.9, YT + 4.9
PRUHY = (YT - T / 4, YT + T / 4)
if POLE == "marihuana":
    zem("cesta", M["trava"])                   # klade se pres normalni silnici (prekryvajici dlazdice)
    kvadr("cesta", M["cesta"], OD, DO, C0, C1, 0.0, 0.01)
    for pr in PRUHY:
        for k in (-0.75, 0.75):
            kvadr("cesta", M["kolej"], OD, DO, pr + k - 0.24, pr + k + 0.24, 0.0, 0.013)
    kvadr("cesta", M["trava"], OD, DO, YT - 0.6, YT + 0.6, 0.0, 0.02)
    # bouda na konci cesty, vedle ni (hrac 3. 10.: "postavil jsi boudu do cesty na marihuanovy plantazi : ) tam budou
    # jezdit auta prece"): stoji na trave u severozapadniho okraje dlazdice (y do 2,5 m, cesta zacina na 2,52 m)
    # u severovychodniho konce (x maly), ujeta cesta i oba pruhy aut zustavaji volne. Drevena kulna s pultovou
    # plechovou strechou spadajici k ceste, dvere a okno na cestu (k jihovychodu), okno k jihozapadu; vedle ni
    # k jihozapadu tri IBC nadrze na vodu, take na trave. Severozapadni strana je za auty, auta ji ve hre prekresli
    # spravne (prekryvajici obrazek se kresli pod auty).
    KX0, KX1, KY0, KY1 = 0.6, 5.0, 0.2, 2.2
    ZK, ZK1 = 2.5, 3.1                             # stena u cesty a vzadu
    kvadr("bouda", M["prkna"], KX0, KX1, KY0, KY1, 0.0, ZK)
    mnohostena("bouda", M["prkna"], [(KX0, KY0, ZK), (KX1, KY0, ZK), (KX1, KY1, ZK), (KX0, KY1, ZK), (KX0, KY0, ZK1), (KX1, KY0, ZK1)],
               [(0, 1, 2, 3), (0, 4, 5, 1), (3, 2, 5, 4), (0, 3, 4), (1, 5, 2)])
    O = 0.25
    mnohostena("bouda", M["plech"], [(KX0 - O, KY0 - O, ZK1 + 0.08), (KX1 + O, KY0 - O, ZK1 + 0.08), (KX1 + O, KY1 + O, ZK - 0.12),
                                     (KX0 - O, KY1 + O, ZK - 0.12), (KX0 - O, KY0 - O, ZK1 + 0.14), (KX1 + O, KY0 - O, ZK1 + 0.14),
                                     (KX1 + O, KY1 + O, ZK - 0.06), (KX0 - O, KY1 + O, ZK - 0.06)],
               [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    for k in range(int((KX1 - KX0) / 0.22)):      # spary prken na stene u cesty
        x = KX0 + 0.22 * (k + 1)
        kvadr("bouda", M["tmava"], x - 0.012, x + 0.012, KY1, KY1 + 0.012, 0.05, ZK - 0.05)
    for k in range(int((KY1 - KY0) / 0.22)):      # a na jihozapadni stene
        y = KY0 + 0.22 * (k + 1)
        kvadr("bouda", M["tmava"], KX1, KX1 + 0.012, y - 0.012, y + 0.012, 0.05, ZK - 0.05)
    kvadr("bouda", M["tmava"], KX0 + 0.5, KX0 + 1.6, KY1, KY1 + 0.02, 0.0, 2.1)            # dvere na cestu
    kvadr("bouda", M["prkna"], KX0 + 0.55, KX0 + 1.55, KY1 + 0.02, KY1 + 0.05, 0.02, 2.05)
    kvadr("bouda", M["sklo"], KX0 + 2.5, KX0 + 3.5, KY1, KY1 + 0.02, 1.3, 2.0)              # okno na cestu
    kvadr("bouda", M["prkna"], KX0 + 2.45, KX0 + 3.55, KY1, KY1 + 0.05, 1.25, 1.3)
    kvadr("bouda", M["sklo"], KX1, KX1 + 0.02, KY0 + 0.5, KY0 + 1.5, 1.3, 2.0)              # okno k jihozapadu
    kvadr("bouda", M["prkna"], KX1, KX1 + 0.05, KY0 + 0.45, KY0 + 1.55, 1.25, 1.3)
    for i in range(3):
        nx0, ny0 = KX1 + 0.6 + 1.35 * i, 0.6
        kvadr("bouda", M["paleta"], nx0, nx0 + 1.2, ny0, ny0 + 1.0, 0.0, 0.15)
        kvadr("bouda", M["nadrz"], nx0 + 0.05, nx0 + 1.15, ny0 + 0.05, ny0 + 0.95, 0.15, 1.15)
        for t in (0.0, 0.33, 0.66, 1.0):
            kvadr("bouda", M["klec"], nx0 + 0.03 + 1.12 * t - 0.015, nx0 + 0.03 + 1.12 * t + 0.015, ny0 + 0.98, ny0 + 1.0, 0.15, 1.2)
            kvadr("bouda", M["klec"], nx0 + 1.18, nx0 + 1.2, ny0 + 0.03 + 0.92 * t - 0.015, ny0 + 0.03 + 0.92 * t + 0.015, 0.15, 1.2)
        for z in (0.55, 1.18):
            kvadr("bouda", M["klec"], nx0 + 1.18, nx0 + 1.2, ny0, ny0 + 1.0, z - 0.015, z + 0.015)
            kvadr("bouda", M["klec"], nx0, nx0 + 1.2, ny0 + 0.98, ny0 + 1.0, z - 0.015, z + 0.015)
        kvadr("bouda", M["tmava"], nx0 + 0.45, nx0 + 0.75, ny0 + 0.35, ny0 + 0.65, 1.15, 1.22)
site_do_sceny()
SOUSEDE = [(dx, dy) for dx in (-T, 0.0, T) for dy in (-T, 0.0, T)]

# ---------------------------------------------------------------- rostliny: v kazdem policku na stejnych mistech
if POLE == "marihuana":
    sys.path.insert(0, os.path.join(TU, "..", "rostliny"))
    import rostliny as RO
    # 4 rady na zahonech po 4 rostlinach, kazda rostlina ma sve nahodne posunuti a velikost (v kazdem policku stejne)
    rnd = random.Random(5)
    MISTA = []
    for yr in RADY_M:
        for j in range(4):
            MISTA.append((T / 8 + j * T / 4 + rnd.uniform(-0.2, 0.2), yr + rnd.uniform(-0.12, 0.12), rnd.random(),
                          rnd.uniform(0, 2 * math.pi), rnd.random()))
    # vzrostle: smrcky jako druha faze stare plantaze, 3,8 az 5 m, ctvrtina vysokych stihlych, barvy MARI jako u sochy
    VYSOKA = RO.nacti("cannabis_plant"); KOSATA = RO.nacti("cannabis_sativa_plant")
    KORUNA_V = 1.4
    # male: mlada rostlinka (small_cannabis_plant) 1,5 az 2,2 m, svetlejsi zelena mlade rostliny
    MLADA = RO.nacti("small_cannabis_plant")
    for m_ in {m for me in MLADA[0] for m in me.materials if m and m.use_nodes}:
        for n_ in m_.node_tree.nodes:
            if n_.type == 'VALTORGB':
                n_.color_ramp.elements[0].color = srgb((56, 112, 14))
                n_.color_ramp.elements[1].color = srgb((124, 172, 38)); n_.color_ramp.elements[1].position = 0.15
    KORUNA_M = 0.9
    for dx, dy in SOUSEDE:
        stred = dx == 0 and dy == 0
        for i, (x, y, t_, u_, d_) in enumerate(MISTA):
            pata = Matrix.Translation(B(x + dx, y + dy, -0.04))
            vys = 3.8 + 1.2 * t_
            druh = VYSOKA if d_ < 0.25 else KOSATA
            for o in RO.postav(druh[0], druh[1], pata, vys, KORUNA_V, u_, jmeno="vzrostla"):
                do_skupiny("mari_vzrostle" if stred else "mari_vzrostle_sousede", o)
            for o in RO.postav(MLADA[0], MLADA[1], pata, 1.5 + 0.7 * t_, KORUNA_M, u_ + 1.0, jmeno="mlada"):
                do_skupiny("mari_male" if stred else "mari_male_sousede", o)
    print("rostlin na policko", len(MISTA), flush=True)

if POLE == "brambory":
    def nat_brambor(seed, mlada):
        """trs nati jako na stare plantazi: lisky jako hrbolate koule do kopule; mlada nizsi, bez kvetu"""
        r_ = random.Random(seed); bm = bmesh.new()
        me = bpy.data.meshes.new(f"nat{seed}{'m' if mlada else ''}")
        for m in ((M["nat_mlada"], M["nat_mlada"]) if mlada else (M["nat"], M["nat2"])) + (M["kvet_b"], M["kvet_f"]):
            me.materials.append(m)
        vys = r_.uniform(0.2, 0.27) if mlada else r_.uniform(0.4, 0.52)
        pol = r_.uniform(0.12, 0.16) if mlada else r_.uniform(0.2, 0.26)
        for i in range(r_.randint(5, 7) if mlada else r_.randint(8, 11)):
            a = r_.random() * 2 * math.pi; d = pol * 0.75 * math.sqrt(r_.random())
            z = vys * (0.35 + 0.5 * (1 - d / pol) * r_.random() + 0.15)
            rr = r_.uniform(0.05, 0.08) if mlada else r_.uniform(0.08, 0.12)
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
        if not mlada and r_.random() < 0.3:
            mi = 2 if r_.random() < 0.75 else 3
            for i in range(r_.randint(2, 4)):
                a = r_.random() * 2 * math.pi; d = pol * 0.6 * math.sqrt(r_.random())
                nove = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035, matrix=Matrix.Translation((d * math.cos(a), d * math.sin(a), vys - 0.02)))["verts"]
                for f in {f for v in nove for f in v.link_faces}:
                    f.material_index = mi
        bm.to_mesh(me); bm.free()
        return me
    TRSY = {False: [nat_brambor(100 + i, False) for i in range(10)], True: [nat_brambor(200 + i, True) for i in range(10)]}
    rnd = random.Random(7)
    N_X = 42                                       # trsu na hrebeni na policko (po 0,35 m)
    MISTA = [(T / (2 * N_X) + j * T / N_X + rnd.uniform(-0.05, 0.05), yr + rnd.uniform(-0.04, 0.04), rnd.randrange(10),
              rnd.uniform(0, 2 * math.pi), rnd.uniform(0.85, 1.15)) for yr in RADY_B for j in range(N_X)]
    for dx, dy in SOUSEDE:
        stred = dx == 0 and dy == 0
        for mlada, sk in ((True, "bram_male"), (False, "bram_vzrostle")):
            for x, y, i_, u_, s_ in MISTA:
                o = bpy.data.objects.new("trs", TRSY[mlada][i_]); scene.collection.objects.link(o)
                o.location = B(x + dx, y + dy, HV - 0.03); o.rotation_euler[2] = u_; o.scale = (s_, s_, s_)
                do_skupiny(sk if stred else sk + "_sousede", o)
    print("trsu na policko", len(MISTA), flush=True)

# ---------------------------------------------------------------- holky (jen pole marihuany)
if POLE == "marihuana":
    sys.path.insert(0, os.path.join(TU, "..", "postavy"))
    import postavy as PO
    def do_sceny(meshe, gx, gy, gz, uhel, sk):
        """postava (objekty z nacti_stojici, celem k -y, chodidla v 0) do bodu hry, celem ve smeru uhel (jako chatka)"""
        PO.postav(meshe, Matrix.Translation(B(gx, gy, gz)) @ Matrix.Rotation(uhel, 4, 'Z') @ Matrix.Scale(K, 4))
        for o in meshe: do_skupiny(sk, o)
    # u okraju dlazdice cesty: u severozapadniho okraje (y maly) a u jihovychodniho (y velky), kazda strana zvlast;
    # stoji na trave u kraje (cesta od 2,5 m). Na dlazdici s boudou jen jihovychodni (bouda a nadrze stoji na trave
    # u severozapadniho okraje)
    do_sceny(PO.nacti_stojici("galaxia_anime_girl", 1.58, "ruce_dolu"), 4.2, 1.6, 0.0, math.radians(60), "holky_sz")
    do_sceny(PO.nacti_stojici("college_girl", 1.62, "ruce_dolu"), 10.4, 1.9, 0.0, math.radians(40), "holky_sz")
    do_sceny(PO.nacti_stojici("character_people_girl_001", 1.68), 9.2, T - 1.7, 0.0, math.radians(15), "holky_jv")
    do_sceny(PO.nacti_stojici("college_girl", 1.62, "ruce_dolu"), 12.6, T - 2.0, 0.0, math.radians(50), "holky_jv")
    # holky pri praci mezi kytkami (hrac 3. 10.: "na pole mam specialni pozy. soubory real, siting a punk tyhle at jsou
    # videt dobre mezi kytkama jak pracujou", "nasmeruj je celem ke kytce vzdy jako ze delaj na ty kytce, z ktery strany
    # delaj na kytce je jedno"): modely uz napozovane (release par10, zip9; v gitu nejsou, patri do postavy/par10/),
    # bez kostry, ve skutecne velikosti (punk je asi o petinu mensi, proto 1,17x). Kazda holka je vlastni vrstva na
    # dlazdici pole (MISTA jsou na vsech polickach stejna), kazda u jine kytky, takze jdou dat i vic na jedno policko.
    # Kytky stoji v mrizce po T/4 a kamera se diva sikmo pod 45 st.: mezi sloupci kytek jsou sikme pruhledy (y - x
    # o pul rozestupu od kytek). Holka sedi nebo kleci bokem ke kytce v pruhledu, takze je dobre videt a kytky ji
    # zakryvaji jen trochu (zvlast vrstva pro male a pro vzrostle kytky).
    S2 = math.sqrt(0.5)
    PRACE = {   # skupina: (model, vyska posazene postavy v m, kytka z MISTA, odstup od kytky v m, smer od holky ke kytce)
        "prace_real": ("par10/real_girl", 1.11, 5, 1.5, (S2, -S2)),                  # klecici, vpravo od kytky
        "prace_sedi": ("par10/girl_sitting", 1.043, 10, 1.35, (-S2, S2)),            # na bobku, vlevo od kytky
        "prace_punk": ("par10/teenage_punk_girl", 0.697 * 1.17, 7, 1.1, (S2, -S2)),  # sedi, nohy ke kytce, vpravo od ni
    }
    # dalsi holky vklece u kytek (hrac: "muzes pridat na pole dalsi takhle sedici, klecici u kytek", "colege nech na
    # ceste a ty ostatni na ceste taky, vem dalsi holky ze zipu"): z par10 pubg_girl a character_girl_16 kostrou
    # Mixamo i s rukama ke kytce, chill_girl ohnutim nohou v siti, rovne, s telefonem v rukou (pauza)
    KLECI = {"prace_pubg", "prace_char16", "prace_chill"}
    PRACE.update({
        "prace_pubg": ("par10/pubg_girl_pose_t", 1.62, 2, 1.6, (S2, -S2)),           # vpravo od kytky
        "prace_char16": ("par10/character_girl_16_fbx", 1.62, 13, 1.6, (-S2, S2)),   # vlevo od kytky
        "prace_chill": ("par10/chill_girl", 1.65, 11, 1.3, (S2, -S2)),               # vpravo od kytky, s telefonem
    })
    for sk, (model, vyska, kytka, odstup, (sx, sy)) in PRACE.items():
        kx, ky = MISTA[kytka][0], MISTA[kytka][1]
        meshe = PO.klecici(model, vyska, predklon=0.0 if sk == "prace_chill" else 28.0) if sk in KLECI else PO.nacti(model, vyska)
        do_sceny(meshe, kx - sx * odstup, ky - sy * odstup, 0.0, math.atan2(sy, sx), sk)

# ---------------------------------------------------------------- kamera, slunce, ram
stred = B(T / 2, T / 2, 0.0)
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); cil = bpy.context.object
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 100.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = cil
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * -0.25 + Vector((0, 0, 1.0))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "2.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()
cam.data.ortho_scale = max(RAM) / PX_M
bpy.context.view_layer.update()
q = cam.matrix_world.inverted() @ B(0, 0, 0)
roh4 = (q.x * 12.2, -q.y * 12.2)               # severni roh ve 4x proti stredu ramu, bez posunu kamery
dx4 = SEVER4[0] - (RAM4[0] / 2 + roh4[0]); dy4 = SEVER4[1] - (RAM4[1] / 2 + roh4[1])
cam.data.shift_x = -dx4 / max(RAM4); cam.data.shift_y = dy4 / max(RAM4)
bpy.context.view_layer.update()
def na_pixel(p):
    v = world_to_camera_view(scene, cam, p)
    return (v.x * RAM[0], (1 - v.y) * RAM[1])
ROHY = {"sever": na_pixel(B(0, 0)), "vychod": na_pixel(B(0, T)), "zapad": na_pixel(B(T, 0)), "jih": na_pixel(B(T, T))}
print("ram", RAM, "rohy", {k: tuple(round(c, 2) for c in v) for k, v in ROHY.items()}, flush=True)

# kosoctverec policka: pixel patri policku, kdyz v nem lezi jeho stred (hrany na stred pixelu nikdy nepadnou, takze
# sousedni policka se neprekryvaji a nemaji mezi sebou diru)
yy, xx = np.mgrid[0:RAM[1], 0:RAM[0]] + 0.5
KOSOCTVEREC = (np.abs(xx - SEVER[0]) / (128 * S4) + np.abs(yy - SEVER[1] - 64 * S4) / (64 * S4)) <= 1.0

VSE = [o for sk in SKUPINY.values() for o in sk]
def nastav(videt=(), chytac=(), drzi=(), jen_stin=(), bez_stinu=()):
    """co je videt; chytac stinu; zadrzene (zakryva, samo pruhledne); jen vrha stin; nevrha stin (skupiny)"""
    g = lambda jm: {o for s in jm for o in SKUPINY.get(s, [])}
    v, ch, dr, js, bs = g(videt), g(chytac), g(drzi), g(jen_stin), g(bez_stinu)
    for o in VSE:
        o.hide_render = o not in v
        o.is_shadow_catcher = o in ch
        o.is_holdout = o in dr
        o.visible_camera = o not in js
        o.visible_shadow = o not in bs

def render_do_pole(jm):
    cesta = os.path.join(VYSTUP, f"_{jm}.png")
    scene.render.filepath = cesta
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(cesta).convert("RGBA"), dtype=np.float64) / 255
    os.remove(cesta)
    return a

def uloz(a, jm, druh, popis):
    Image.fromarray((a * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(os.path.join(VYSTUP, f"{jm}_zin{ZIN}.png"))
    ys, xs = np.nonzero(a[..., 3] > 0.004)
    json.dump({"px_m": PX_M, "policko_m": T, "ram": list(RAM), "rohy": ROHY, "druh": druh, "popis": popis,
               "obsah": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None},
              open(os.path.join(VYSTUP, f"{jm}_zin{ZIN}.json"), "w"), indent=1)
    print("ulozeno", jm, flush=True)

STIN = float(os.environ.get("STIN", "0.2"))
def zaklad(zem_sk, jm, popis):
    """zaklad: neprusvitna zem presne v kosoctverci policka"""
    nastav(videt=[zem_sk])
    a = render_do_pole(jm)
    a[..., 3] = np.where(KOSOCTVEREC, 1.0, 0.0)
    a[..., :3] *= a[..., 3:4]
    uloz(a, jm, "zaklad", popis)

def vrstva_se_stinem(zem_sk, vrstva, sousede, jm, popis):
    """prikladaci vrstva s vlastnim stinem na zem: A se zemi jako chytacem stinu, B se zemi zadrzenou;
    stin = (A.a - B.a) / (1 - B.a) jen v kosoctverci policka, na STIN (20 %) jako u sochy"""
    nastav(videt=[zem_sk, vrstva] + sousede, chytac=[zem_sk], jen_stin=sousede)
    A = render_do_pole(jm + "_a")
    nastav(videt=[zem_sk, vrstva] + sousede, drzi=[zem_sk], jen_stin=sousede)
    Bp = render_do_pole(jm + "_b")
    aB = Bp[..., 3]
    aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN * KOSOCTVEREC
    alfa = aB + (1 - aB) * aS
    barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
    out = np.dstack([barva, alfa]); out[alfa < 0.004] = 0.0
    uloz(out, jm, "vrstva", popis)

def vrstva_holek(zem_sk, holky, zakryva, jm, popis):
    """holky bez stinu: co je pred nimi (zem, rostliny policka), je zadrzene a nevrha stin; alfa se omezi druhym
    pruchodem se samotnymi holkami (listy s pruhlednou texturou nechavaji v zadrzene scene slabe cerne obrysy)"""
    nastav(videt=[zem_sk, holky] + zakryva, drzi=[zem_sk] + zakryva, bez_stinu=zakryva)
    H = render_do_pole(jm + "_h")
    nastav(videt=[holky])
    G = render_do_pole(jm + "_g")
    H[..., 3] = np.minimum(H[..., 3], G[..., 3])
    H[H[..., 3] < 0.004] = 0.0
    uloz(H, jm, "vrstva", popis)

def vrstva_prace(zem_sk, holky, zakryva, jm, popis):
    """holka mezi kytkami se stinem na zem: kytky policka (zakryva) jsou zadrzene a nevrhaji stin (ten je ve vrstve
    kytek); A se zemi jako chytacem stinu, B se zemi zadrzenou, stin = (A.a - B.a) / (1 - B.a) jen v kosoctverci
    policka na STIN (20 %) jako u kytek; alfa holky omezena pruchodem s holkou samotnou (listy s pruhlednou texturou
    nechavaji v zadrzene scene slabe cerne obrysy)"""
    nastav(videt=[zem_sk, holky] + zakryva, chytac=[zem_sk], drzi=zakryva, bez_stinu=zakryva)
    A = render_do_pole(jm + "_a")
    nastav(videt=[zem_sk, holky] + zakryva, drzi=[zem_sk] + zakryva, bez_stinu=zakryva)
    Bp = render_do_pole(jm + "_b")
    nastav(videt=[holky])
    G = render_do_pole(jm + "_g")
    aB = np.minimum(Bp[..., 3], G[..., 3])
    aS = np.clip((A[..., 3] - Bp[..., 3]) / np.maximum(1 - Bp[..., 3], 1e-6), 0, 1) * STIN * KOSOCTVEREC
    alfa = aB + (1 - aB) * aS
    barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
    out = np.dstack([barva, alfa]); out[alfa < 0.004] = 0.0
    uloz(out, jm, "vrstva", popis)

def chci(jm):
    return not JEN or jm in JEN

if POLE == "marihuana":
    if chci("mari_zaklad"): zaklad("mari_zaklad", "mari_zaklad", "pole marihuany bez kytek: zem, 4 zahony podel x")
    if chci("cesta"): zaklad("cesta", "cesta", "polni cesta podel x s travou kolem; ve hre prekryvajici obrazek, pod nim silnice")
    if chci("bouda"): vrstva_se_stinem("cesta", "bouda", [], "bouda", "kulna a tri nadrze na konci cesty vedle ni, na trave u severozapadniho okraje dlazdice cesty; cesta volna")
    if chci("mari_male"):
        vrstva_se_stinem("mari_zaklad", "mari_male", ["mari_male_sousede"], "mari_male", "male kytky (mlade rostliny 1,5 az 2,2 m)")
    if chci("mari_vzrostle"):
        vrstva_se_stinem("mari_zaklad", "mari_vzrostle", ["mari_vzrostle_sousede"], "mari_vzrostle", "vzrostle smrcky 3,8 az 5 m")
    if chci("holky_sz"): vrstva_holek("cesta", "holky_sz", [], "holky_sz", "dve holky u severozapadniho okraje cesty (ne na dlazdici s boudou)")
    if chci("holky_jv"): vrstva_holek("cesta", "holky_jv", [], "holky_jv", "dve holky u jihovychodniho okraje cesty (i s boudou)")
    for sk in PRACE:
        for f, kytky in ((2, "mari_male"), (3, "mari_vzrostle")):
            if chci(f"{sk}_f{f}"):
                vrstva_prace("mari_zaklad", sk, [kytky], f"{sk}_f{f}",
                             f"holka pri praci u kytky ({PRACE[sk][0].split('/')[-1]}), zakryta {'malymi' if f == 2 else 'vzrostlymi'} kytkami policka, faze {f}")
if POLE == "brambory":
    if chci("bram_zaklad"): zaklad("bram_zaklad", "bram_zaklad", "pole brambor bez nate: zem, 20 hrebenu podel x")
    if chci("bram_male"): vrstva_se_stinem("bram_zaklad", "bram_male", ["bram_male_sousede"], "bram_male", "mlada nat 0,2 az 0,27 m")
    if chci("bram_vzrostle"):
        vrstva_se_stinem("bram_zaklad", "bram_vzrostle", ["bram_vzrostle_sousede"], "bram_vzrostle", "vzrostla nat 0,4 az 0,52 m, cast kvete")
print("hotovo", VYSTUP, flush=True)
