# -*- coding: utf-8 -*-
# Chatka na 2 policka. Hrac 3. 10.: "okolo domku lavicky velke jak u sochy, neporadek, nizke smrcky marihuany misto plotu,
# sem tam dira. prikladaci holky stojici a pak prikladaci holky sedici. takze bude obrazek bez holek a dva s holkama
# prilozenejma. chci tam hlavne tu holku co stoji u kufru dvanacetrojky bus", "velikost 1 policko ... muze to byt pres
# dve policka nebo pres ctyri policka, to je jedno. ale holky prikladaci at usetrime Mb".
# Domek: "A little happy hut" od Tigrana Safaryana (Sketchfab, CC BY 4.0, model/a_little_happy_hut.glb). Holky jsou jako
# u sochy a u kufru 1203 dvakrat vetsi, domek je proto zvetseny tak, aby dvere (v modelu 76 jednotek) mely 3,35 m a holka
# (College Girl 3,24 m) prosla; tim zabere cele zadni policko, vpredu je druhe policko s dvorkem.
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu pozemku (2 policka podel x:
# x 0 az 2T, y 0 az T). Kamera, svetlo a slabe stiny jako u sochy (socha/render_socha.py).
#   [ZIN=8] [SAMPLES=128] python3 render_chatka.py <vystupni adresar>      -> chatka[_stojici|_sedici]_zin4.png + .json
#   NAHLED=1: rychly nahled cele sceny (Workbench) i s obema sadami holek do <adresar>/nahled*.png
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image

VYSTUP = sys.argv[-1]
ZIN = int(os.environ.get("ZIN", "4"))
PX_M = 12.2 * ZIN / 4
K = 2.0                                        # lavicky, holky, neporadek a rostliny dvakrat vetsi jako u sochy
T = 256 / (math.sqrt(2) * 12.2)                # policko 14,84 m (256 px ve 4x)
NAHLED = os.environ.get("NAHLED", "0") == "1"
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
DVERE_M, DVERE_J = 3.35, 76.0                  # vyska dveri v prizemi: chceme metry, v modelu jednotek
os.makedirs(VYSTUP, exist_ok=True)

def B(x, y, z=0.0):
    """souradnice hry (m) -> Blender"""
    return Vector((y, -x, z))

# ---------------------------------------------------------------- scena jako socha
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = int(os.environ.get("SAMPLES", "128"))
scene.cycles.filter_width = 1.5
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
world = bpy.data.worlds.new("World"); scene.world = world; world.use_nodes = True
nt = world.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment'); wo = nt.nodes.new('ShaderNodeOutputWorld')
env.image = bpy.data.images.load(HDRI)
nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
scene.world.cycles_visibility.shadow = True
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.9"))

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
    m.diffuse_color = srgb(rgb)
    return m

M = {
    "hlina": mat("hlina", (118, 96, 70), 0.95, sum_=0.18, meritko=3.0),        # uslapana zem na dvorku
    "lavicka": mat("lavicka", (138, 92, 52), 0.7),
    "kov": mat("kov", (52, 58, 54), 0.5, kov=0.5),
    "bedna": mat("bedna", (150, 112, 68), 0.85, sum_=0.12, meritko=6.0),
    "bedna_tm": mat("bedna_tm", (104, 76, 46), 0.85, sum_=0.12, meritko=6.0),
    "prkno": mat("prkno", (126, 98, 66), 0.85, sum_=0.15, meritko=8.0),
    "guma": mat("guma", (26, 26, 26), 0.9),
    "kyblik": mat("kyblik", (150, 156, 160), 0.35, kov=0.8),
    "cerna": mat("cerna", (14, 14, 14), 0.9),
}
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

def mnohostena(m, body, steny):
    bm = bm_pro(m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])

def kvadr_otoceny(m, x, y, z0, z1, du, dv, uhel):
    """kvadr se stredem x y, rozmery du (podel smeru uhel) a dv (napric), od z0 do z1"""
    c, s = math.cos(uhel), math.sin(uhel)
    def bod(u, v, z): return (x + u * c - v * s, y + u * s + v * c, z)
    b = [bod(u, v, z) for z in (z0, z1) for v in (-dv / 2, dv / 2) for u in (-du / 2, du / 2)]
    mnohostena(m, b, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])

def valec(m, x, y, z0, z1, r, n=16):
    bm = bm_pro(m)
    dole = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z0)) for k in range(n)]
    nahore = [bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z1)) for k in range(n)]
    bm.faces.new(dole[::-1]); bm.faces.new(nahore)
    for k in range(n):
        bm.faces.new((dole[k], dole[(k + 1) % n], nahore[(k + 1) % n], nahore[k]))

# ---------------------------------------------------------------- domek
pred = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=os.path.join(TU, "model", "a_little_happy_hut.glb"))
domek = [o for o in bpy.data.objects if o not in pred]
koren_d = [o for o in domek if o.parent is None][0]
meshe_d = [o for o in domek if o.type == 'MESH']
bpy.context.view_layer.update()
P = np.vstack([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in meshe_d])
mn_d, mx_d = P.min(axis=0), P.max(axis=0)
S_D = DVERE_M / DVERE_J
stred_d = (mn_d + mx_d) / 2
# otoceni o 90 st: dvere (stena -x modelu) k jihozapadu na dvorek, schody (strana -y modelu) k jihovychodu k divakovi
obal = bpy.data.objects.new("domek", None); scene.collection.objects.link(obal)
koren_d.parent = obal
C_D = (T / 2, T / 2)                            # stred zadniho policka (x, y)
obal.matrix_world = (Matrix.Translation(B(C_D[0], C_D[1], -mn_d[2] * S_D)) @ Matrix.Rotation(math.radians(90), 4, 'Z') @
                     Matrix.Scale(S_D, 4) @ Matrix.Translation(Vector((-stred_d[0], -stred_d[1], 0.0))))
bpy.context.view_layer.update()
P = np.vstack([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in meshe_d])
# v souradnicich hry: x = -Blender y, y = Blender x
hx0, hx1, hy0, hy1 = -P[:, 1].max(), -P[:, 1].min(), P[:, 0].min(), P[:, 0].max()
print(f"domek: meritko {S_D:.5f} m/jednotku, x {hx0:.2f}..{hx1:.2f}, y {hy0:.2f}..{hy1:.2f}, vyska {P[:, 2].max():.2f} m", flush=True)
DOMEK = list(meshe_d)

# ---------------------------------------------------------------- dvorek: uslapana zem, lavicky, neporadek
X0 = T                                           # dvorek: x T az 2T, y 0 az T
# uslapana hlina: nepravidelna placka na dvorku (kolem lavicek, k dverim a k dire v plotu)
def placka(m, body, z=0.012):
    bm = bm_pro(m)
    v = [bm.verts.new(B(x, y, z)) for x, y in body]
    bm.faces.new(v)
rnd_z = random.Random(5)
obrys = []
for k in range(40):
    a = 2 * math.pi * k / 40
    r = 1.0 + 0.12 * math.sin(3 * a + 1.0) + 0.06 * rnd_z.uniform(-1, 1)
    obrys.append((X0 + T * 0.5 + math.cos(a) * T * 0.40 * r, T * 0.5 + math.sin(a) * T * 0.38 * r))
placka(M["hlina"], obrys)

def lavicka(x, y, uhel):
    """lavicka jako u sochy, 2x: sedak 0,47 m, delka 1,6 m (skutecne), uhel: kam se sedici diva"""
    c, s = math.cos(uhel), math.sin(uhel)
    def bod(u, v, z):
        return (x + (u * -s + v * -c) * K, y + (u * c + v * -s) * K, z * K)
    def kus(m, u0, u1, v0, v1, z0, z1):
        b = [bod(u, v, z) for z in (z0, z1) for v in (v0, v1) for u in (u0, u1)]
        mnohostena(m, b, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
    kus(M["lavicka"], -0.8, 0.8, -0.22, 0.22, 0.42, 0.47)
    kus(M["lavicka"], -0.8, 0.8, 0.2, 0.25, 0.5, 0.88)
    for u in (-0.65, 0.65):
        kus(M["kov"], u - 0.03, u + 0.03, -0.2, 0.22, 0.0, 0.42)
# dve lavicky vzadu na dvorku, sedici koukaji k divakovi: jedna u domku (cela k jihozapadu), druha u severozapadni
# hrany dvorku (cela k jihovychodu)
LAV_1 = (X0 + 1.6, 9.6, 0.0)                    # u domku vpravo od dveri, diva se k jihozapadu (+x)
LAV_2 = (X0 + 8.2, 1.6, math.pi / 2)            # u severozapadni hrany, diva se k jihovychodu (+y)
for l in (LAV_1, LAV_2):
    lavicka(*l)

# neporadek: bedny, pneumatika, kyblik, prkna, lahve a odpadky jako u sochy
kvadr_otoceny(M["bedna"], X0 + 3.2, 3.6, 0.0, 0.7, 1.1, 0.8, 0.3)                    # bedna
kvadr_otoceny(M["bedna_tm"], X0 + 3.4, 3.7, 0.7, 1.25, 0.9, 0.7, 0.9)                # druha na ni nakrivo
kvadr_otoceny(M["bedna"], X0 + 12.6, 12.9, 0.0, 0.6, 0.9, 1.0, 1.2)                  # prevrhla bedna u plotu
for k in range(4):                                                                    # hromada prken
    kvadr_otoceny(M["prkno"], X0 + 6.4 + 0.05 * k, 12.4 - 0.3 * k, 0.05 * k, 0.05 * k + 0.05, 2.6, 0.3, 0.15 + 0.08 * k)
bpy.ops.mesh.primitive_torus_add(major_radius=0.32 * K, minor_radius=0.11 * K, location=B(X0 + 11.4, 4.2, 0.11 * K))
pneu = bpy.context.object; pneu.data.materials.append(M["guma"])
bpy.ops.mesh.primitive_torus_add(major_radius=0.32 * K, minor_radius=0.11 * K, location=B(X0 + 11.5, 4.3, 0.33 * K))
pneu2 = bpy.context.object; pneu2.data.materials.append(M["guma"])
valec(M["kyblik"], X0 + 4.6, 10.9, 0.0, 0.32 * K, 0.15 * K)
valec(M["cerna"], X0 + 4.6, 10.9, 0.32 * K - 0.02, 0.32 * K + 0.002, 0.13 * K)

rnd_o = random.Random(11)
NEPORADEK = [pneu, pneu2]
def odpadek(x, y, z0=0.0):
    druh = rnd_o.choices(["papir", "plech", "lahev", "kelimek", "sacek", "balicek"], [26, 20, 22, 8, 12, 12])[0]
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
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=r * K, depth=delka * K, location=B(x, y, z0 + r * K),
                                            rotation=(math.radians(90), 0, uhel))
        o = bpy.context.object
    o.data.materials.append(m); NEPORADEK.append(o)
for i in range(70):                                                                   # po celem dvorku
    odpadek(rnd_o.uniform(X0 + 0.8, X0 + T - 0.8), rnd_o.uniform(0.8, T - 0.8))
for lx, ly, _ in (LAV_1, LAV_2):                                                      # pod lavickami a u nich
    for i in range(10):
        odpadek(lx + rnd_o.uniform(-1.4, 1.4), ly + rnd_o.uniform(-1.4, 1.4))
for i in range(8):                                                                    # lahve u beden
    odpadek(X0 + 3.3 + rnd_o.gauss(0, 0.6), 3.6 + rnd_o.gauss(0, 0.6))

for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)
    NEPORADEK.append(o)

# ---------------------------------------------------------------- plot z nizkych "smrcku" marihuany se sem tam dirou
sys.path.insert(0, os.path.join(TU, "..", "rostliny"))
import rostliny as RO
KOSATA = RO.nacti("cannabis_sativa_plant"); STIHLA = RO.nacti("cannabis_plant")
rnd_p = random.Random(23)
ROSTLINY = []
def rada(body_od, body_do, krok, vynechat):
    """rostliny v rade od-do po kroku, indexy ve `vynechat` jsou diry"""
    (xa, ya), (xb, yb) = body_od, body_do
    d = math.hypot(xb - xa, yb - ya); n = int(d // krok) + 1
    for i in range(n):
        if i in vynechat: continue
        t = (i + 0.5) / n
        x, y = xa + (xb - xa) * t + rnd_p.uniform(-0.12, 0.12), ya + (yb - ya) * t + rnd_p.uniform(-0.12, 0.12)
        vys = rnd_p.uniform(1.0, 1.3) * K                     # nizke smrcky: skutecne 1 az 1,3 m
        druh = KOSATA if rnd_p.random() < 0.7 else STIHLA
        ROSTLINY.extend(RO.postav(druh[0], druh[1], Matrix.Translation(B(x, y, 0)), vys, 0.42 * K, rnd_p.random() * 6.3))
OKRAJ = 1.0                                                   # stred rostliny od hrany pozemku (koruna 0,42*K = 0,84 m, posun 0,12)
# jihovychodni hrana celeho pozemku (vpredu vpravo), jihozapadni hrana dvorku (vpredu vlevo), severozapadni hrana dvorku
rada((OKRAJ + 0.4, T - OKRAJ), (2 * T - OKRAJ, T - OKRAJ), 1.45, {3, 11, 16})
rada((2 * T - OKRAJ, OKRAJ), (2 * T - OKRAJ, T - OKRAJ - 1.0), 1.45, {4, 5})          # siroka dira = branka k dverim
rada((X0 + 0.6, OKRAJ), (2 * T - OKRAJ - 1.0, OKRAJ), 1.45, {6})
print("rostlin v plotu:", len(ROSTLINY) // max(1, len(KOSATA[0])), flush=True)

# ---------------------------------------------------------------- holky (prikladaci vrstvy)
sys.path.insert(0, os.path.join(TU, "..", "postavy"))
import postavy as PO
def do_sceny(meshe, kotva, gx, gy, gz, uhel):
    """postava (celem k -y, kotva = jeji bod) do bodu hry gx gy gz, celem ve smeru uhel (rad, v rovine hry x y)"""
    # v Blenderu je smer hry (cos u, sin u) = (sin u, -cos u); postava kouka k -y Blenderu = smer hry 0, otocit o +u
    # (jako u sochy). Do 3. 10. tu bylo -u: sedici na lavicce celem k jihovychodu (Galaxia) sedela celem k operadlu,
    # hrac: "otoc tu holku celem vzad. na zapadni lavicce". Stojici maji uhly takove, aby staly jako predtim.
    M_ = Matrix.Translation(B(gx, gy, gz)) @ Matrix.Rotation(uhel, 4, 'Z') @ Matrix.Scale(K, 4) @ Matrix.Translation(-kotva)
    PO.postav(meshe, M_)
def na_lavicku(meshe, kotva, lav, u):
    x, y, uhel = lav
    c, s = math.cos(uhel), math.sin(uhel)
    v = 0.05
    do_sceny(meshe, kotva, x + (u * -s + v * -c) * K, y + (u * c + v * -s) * K, 0.47 * K, uhel)
STOJICI, SEDICI = [], []
# stojici: holka od kufru 1203 (College Girl, ruce podel tela) na dvorku, Character Girl s kabelkou prichazi brankou
cg = PO.nacti_stojici("college_girl", 1.62, "ruce_dolu")
do_sceny(cg, Vector((0, 0, 0)), X0 + 2.6, 6.2, 0.012, math.radians(-35)); STOJICI += cg
ch = PO.nacti_stojici("character_people_girl_001", 1.68)
do_sceny(ch, Vector((0, 0, 0)), X0 + 9.8, 7.4, 0.012, math.radians(-200)); STOJICI += ch     # = 160 st, ale cislo jako predtim
# treti stojici, hrac 3. 10.: "jeste jednu ... na druhe policko k domku za severovychodni lavicku ke dverim domku",
# "pred popinavy rostliny na zdi ji postav". Galaxia jako u automatu (ruce podel tela) na zadnim policku pred
# brectanem na jihozapadni zdi vpravo od dveri (zed x 10,58, brectan u zeme y 6,8 az 9,4), celem k dvorku
ga_st = PO.nacti_stojici("galaxia_anime_girl", 1.58, "ruce_dolu")
do_sceny(ga_st, Vector((0, 0, 0)), 11.5, 8.1, 0.0, math.radians(25)); STOJICI += ga_st
# sedici: College Girl a Character Girl na lavicce u domku, Galaxia na druhe (zapadni), vsechny celem od operadla
cg2, k2 = PO.sedici("college_girl"); na_lavicku(cg2, k2, LAV_1, -0.42); SEDICI += cg2
ch2, kc = PO.sedici("character_people_girl_001"); na_lavicku(ch2, kc, LAV_1, 0.4); SEDICI += ch2
ga, kg = PO.sedici("galaxia_anime_girl"); na_lavicku(ga, kg, LAV_2, 0.1); SEDICI += ga

# ---------------------------------------------------------------- chytac stinu, kamera, slunce
bpy.ops.mesh.primitive_plane_add(size=1, location=B(T, T / 2, 0.0))
zem = bpy.context.object; zem.scale = (T, 2 * T, 1); zem.is_shadow_catcher = True
stred = B(T, T / 2, 0.0)
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

# ram: sirka pres cely pozemek, vyska od vrchu domku po jizni roh; severni roh na celem pixelu delitelnem 4 (ve 4x)
SIRKA4 = 400; OKRAJ_NAHORE4 = 8
bpy.context.view_layer.update()
def mereni(body):
    """body (Blender) -> pixely 4x proti stredu ramu (x doprava, y dolu) bez posunu kamery"""
    m = cam.matrix_world.inverted()
    out = []
    for p in body:
        q = m @ p
        out.append((q.x * 12.2, -q.y * 12.2))
    return out
def body_objektu(objekty, krok=5):
    for o in objekty:
        a = np.zeros(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", a)
        W = o.matrix_world
        for v in a.reshape(-1, 3)[::krok]:
            yield W @ Vector(v)
vrch = min(y for _, y in mereni(list(body_objektu(DOMEK + STOJICI + ROSTLINY))))
roh = dict(zip(("sever", "vychod", "zapad", "jih"), mereni([B(0, 0), B(0, T), B(2 * T, 0), B(2 * T, T)])))
VYSKA4 = int(math.ceil((roh["jih"][1] - vrch + OKRAJ_NAHORE4 + 6) / 4.0)) * 4
# kde ma byt severni roh (4x): vodorovne stred ramu + jeho posun, svisle tak, aby vrch domku byl OKRAJ_NAHORE4 od kraje
sever4 = (SIRKA4 / 2 + roh["sever"][0], OKRAJ_NAHORE4 + (roh["sever"][1] - vrch))
cil4 = (round(sever4[0] / 4) * 4, round(sever4[1] / 4) * 4)
RAM_W, RAM_H = SIRKA4 * ZIN // 4, VYSKA4 * ZIN // 4
scene.render.resolution_x, scene.render.resolution_y = RAM_W, RAM_H; scene.render.resolution_percentage = 100
cam.data.ortho_scale = max(RAM_W, RAM_H) / PX_M
# posun kamery (v podilu delsi strany ramu): severni roh z (stred + roh) na cil
dx4 = cil4[0] - (SIRKA4 / 2 + roh["sever"][0]); dy4 = cil4[1] - (VYSKA4 / 2 + roh["sever"][1])
cam.data.shift_x = -dx4 / max(SIRKA4, VYSKA4); cam.data.shift_y = dy4 / max(SIRKA4, VYSKA4)
bpy.context.view_layer.update()
def na_pixel(p):
    q = world_to_camera_view(scene, cam, p)
    return (q.x * RAM_W, (1 - q.y) * RAM_H)
rohy = {"sever": na_pixel(B(0, 0)), "vychod": na_pixel(B(0, T)), "zapad": na_pixel(B(2 * T, 0)), "jih": na_pixel(B(2 * T, T))}
print("ram", RAM_W, RAM_H, "rohy", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()}, flush=True)

VSE_SCENA = DOMEK + NEPORADEK + ROSTLINY
def ukaz(holky_stojici, holky_sedici, scena_drzi=False):
    for o in STOJICI: o.hide_render = not holky_stojici
    for o in SEDICI: o.hide_render = not holky_sedici
    for o in VSE_SCENA: o.is_holdout = scena_drzi

if NAHLED:
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'; scene.display.shading.color_type = 'TEXTURE'
    zem.hide_render = True
    for jm, (st, se) in {"stojici": (True, False), "sedici": (False, True)}.items():
        ukaz(st, se)
        scene.render.filepath = os.path.join(VYSTUP, f"nahled_{jm}.png")
        bpy.ops.render.render(write_still=True)
    sys.exit(0)

def render_do_pole(cesta):
    scene.render.filepath = cesta
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(cesta).convert("RGBA"), dtype=np.float64) / 255
    os.remove(cesta)
    return a
def uloz(a, jmeno, navic=None):
    Image.fromarray((a * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(os.path.join(VYSTUP, jmeno + ".png"))
    d = {"px_m": PX_M, "policko_m": T, "policek": [2, 1], "meritko_postav": K, "ram": [RAM_W, RAM_H], "rohy": rohy}
    if navic: d.update(navic)
    json.dump(d, open(os.path.join(VYSTUP, jmeno + ".json"), "w"), indent=1)

# 1) bez holek: stin na travu 20 % jako u sochy
ukaz(False, False)
A = render_do_pole(os.path.join(VYSTUP, "_a.png"))
zem.hide_render = True
Bp = render_do_pole(os.path.join(VYSTUP, "_b.png"))
STIN = float(os.environ.get("STIN", "0.2"))
aB = Bp[..., 3]; aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN
alfa = aB + (1 - aB) * aS
barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
uloz(np.dstack([barva, alfa]), f"chatka_zin{ZIN}")
# 2) a 3) prikladaci holky: jen holky, scena je zadrzena (holdout: zakryje, co je za ni), bez chytace stinu = bez stinu.
# Listy rostlin (pruhledna textura) nechavaji v zadrzene scene slabe cerne obrysy (alfa do 10 %), proto se alfa omezi
# jeste druhym pruchodem se samotnymi holkami (scena skryta): kde holka neni, je vrstva pruhledna.
for jm, (st, se) in (("stojici", (True, False)), ("sedici", (False, True))):
    ukaz(st, se, scena_drzi=True)
    H = render_do_pole(os.path.join(VYSTUP, "_h.png"))
    for o in VSE_SCENA: o.hide_render = True
    G = render_do_pole(os.path.join(VYSTUP, "_g.png"))
    for o in VSE_SCENA: o.hide_render = False
    H[..., 3] = np.minimum(H[..., 3], G[..., 3])
    H[H[..., 3] < 0.004] = 0.0
    ys, xs = np.nonzero(H[..., 3] > 0.004)
    bb = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None
    uloz(H, f"chatka_{jm}_zin{ZIN}", {"holky_obdelnik": bb})
    print(jm, "obdelnik holek", bb, flush=True)
print("hotovo", VYSTUP)
