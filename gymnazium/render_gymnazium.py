# -*- coding: utf-8 -*-
# Divci gymnazium na 2 x 2 policka (hrac 1. 10.: "udelame budovu skoly, divci gymnazium, 2x2 policka, nizka budova,
# neco okolo budovy hriste park", "jenom obrazek a vedle ve forclaude to zabudujem do zakladniho prumyslu hry").
# Vlastni model, zadny cizi. Kamera jako u Tatry (tatra/render_sklapec.py): ortho, 30 st. shora, azimut 45 st.
# Svetlo od 3. 10. mekke jako u sochy (socha/render_socha.py, okoli 0,9, slunce 2 zleva shora, stin na travu 20 %),
# hrac: "to jsou stiny, davas hodne stinu, uz nefotime tatru 148". Do 3. 10. bylo jako u Tatry (okoli 0,35, slunce 5,
# stin 55 %), ale to delalo tmave kouty u schodu.
# Meritko 12,2 px/m jako vejtraska a Tatra v zin4, policko je pak 14,84 m a pozemek 29,7 x 29,7 m.
#   python3 render_gymnazium.py <vystup.png> [px_na_m]
#   POSTAVY=1: druhy obrazek do animace s divkami (postavy/), pak sloucit postavy/animace.py s gymnazium_zin4.png
#   ZIN=8: priblizeni 8x nasi hry (2. 10.): stejna scena a kamera, 24,4 px/m do 1440 x 1440 px, policko 512 px,
#   obrazek i rohy v JSONu jsou presne dvojnasobek 4x (hra to u spritu s vic urovnemi kontroluje)
# Souradnice v modelu jako ve hre: x k jihozapadu (na obrazku doleva dolu), y k jihovychodu (doprava dolu),
# z nahoru, pocatek v severnim rohu pozemku. Do Blenderu B(x, y, z) = (y, -x, z), kamera z jihu jako u aut.
import bpy, bmesh, os, sys, math, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

VYSTUP = sys.argv[-1] if sys.argv[-1].endswith(".png") else sys.argv[-2]
ZIN = int(os.environ.get("ZIN", "4"))          # 4 = zin4 (vychozi), 8 = zin8 (jen nase hra)
PX_M = (float(sys.argv[-1]) if not sys.argv[-1].endswith(".png") else 12.2) * ZIN / 4
RAM = 720 * ZIN // 4
T = 256 * ZIN / 4 / (math.sqrt(2) * PX_M)     # delka policka v metrech (v zin4 je policko 256 px siroke, v zin8 512)
P = 2 * T                                       # pozemek 2 x 2
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
SAMPLES = int(os.environ.get("SAMPLES", "128"))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = SAMPLES
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
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.9"))       # jako socha (do 3. 10. 0,35)


def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

def mat(jmeno, rgb, drsnost=0.8, kov=0.0, sum_=0.0, meritko=2.0):
    """material; sum_ = jak moc se barva meni sumem (omitka, tasky, travy), at plochy nejsou mrtve"""
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if sum_:
        tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = meritko
        tex.inputs["Detail"].default_value = 6.0
        ramp = t.nodes.new('ShaderNodeValToRGB')
        tmavsi = tuple(max(0, v * (1 - sum_)) for v in rgb); svetlejsi = tuple(min(255, v * (1 + sum_)) for v in rgb)
        ramp.color_ramp.elements[0].color = srgb(tmavsi); ramp.color_ramp.elements[1].color = srgb(svetlejsi)
        t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    return m

M = {
    "fasada": mat("fasada", (226, 194, 124), 0.9, sum_=0.05, meritko=1.5),       # okrova omitka jako stare skoly
    "bila": mat("bila", (236, 232, 220), 0.8),                                   # rimsy, lizeny, ostenia
    "sokl": mat("sokl", (132, 126, 116), 0.9, sum_=0.08, meritko=4.0),
    "strecha": mat("strecha", (132, 58, 40), 0.8, sum_=0.12, meritko=3.0),      # palene tasky
    "komin": mat("komin", (146, 84, 62), 0.85, sum_=0.06),
    "sklo": mat("sklo", (26, 34, 44), 0.15),
    "dvere": mat("dvere", (84, 50, 28), 0.6),
    "napis": mat("napis", (60, 46, 26), 0.4, kov=0.6),
    "kurt": mat("kurt", (172, 76, 54), 0.9, sum_=0.04, meritko=6.0),            # cerveny umely povrch
    "cara": mat("cara", (236, 236, 230), 0.8),
    "dlazba": mat("dlazba", (178, 174, 164), 0.9, sum_=0.06, meritko=5.0),
    "sterk": mat("sterk", (198, 184, 150), 0.95, sum_=0.08, meritko=8.0),
    "plot": mat("plot", (50, 88, 38), 0.9, sum_=0.25, meritko=4.0),             # zivy plot
    "kmen": mat("kmen", (82, 64, 46), 0.9),
    "lavicka": mat("lavicka", (138, 92, 52), 0.7),
    "kov": mat("kov", (52, 58, 54), 0.5, kov=0.5),
    "deska": mat("deska", (238, 238, 236), 0.4),
    "obruc": mat("obruc", (222, 108, 30), 0.5),
    "zemina": mat("zemina", (92, 64, 42), 0.95),
    "lampa": mat("lampa", (244, 242, 232), 0.3),
    "v_bila": mat("v_bila", (240, 240, 240), 0.7), "v_cervena": mat("v_cervena", (200, 24, 34), 0.7),
    "v_modra": mat("v_modra", (20, 60, 150), 0.7),
}
# rady tasek: vodorovne pruhy po 16 cm vysky (na strese 28 st. je to 34 cm podel spadu), spodni hrana kazde rady tmavsi
_t = M["strecha"].node_tree; _b = _t.nodes["Principled BSDF"]
_vlna = _t.nodes.new('ShaderNodeTexWave'); _vlna.wave_type = 'BANDS'; _vlna.bands_direction = 'Z'; _vlna.wave_profile = 'SAW'
_souradnice = _t.nodes.new('ShaderNodeTexCoord'); _t.links.new(_souradnice.outputs["Object"], _vlna.inputs["Vector"])
_vlna.inputs["Scale"].default_value = 0.1 * math.pi / 0.164      # pruhy Z v Cycles: perioda 2 pi / (20 * scale)
_krivka = _t.nodes.new('ShaderNodeMapRange'); _krivka.inputs["From Min"].default_value = 0.0; _krivka.inputs["From Max"].default_value = 1.0
_krivka.inputs["To Min"].default_value = 0.80; _krivka.inputs["To Max"].default_value = 1.05
_t.links.new(_vlna.outputs["Fac"], _krivka.inputs["Value"])
_nasob = _t.nodes.new('ShaderNodeMix'); _nasob.data_type = 'RGBA'; _nasob.blend_type = 'MULTIPLY'; _nasob.inputs["Factor"].default_value = 1.0
_puv = _b.inputs["Base Color"].links[0].from_socket
_t.links.new(_puv, _nasob.inputs[6]); _t.links.new(_krivka.outputs["Result"], _nasob.inputs[7])
_t.links.new(_nasob.outputs[2], _b.inputs["Base Color"])
KORUNY = [mat(f"koruna{i}", c, 0.85, sum_=0.22, meritko=5.0)
          for i, c in enumerate([(62, 104, 44), (70, 112, 48), (56, 96, 42), (78, 116, 52)])]
KVETY = [mat(f"kvet{i}", c, 0.7) for i, c in enumerate([(210, 40, 50), (236, 196, 40), (226, 120, 160), (240, 240, 236)])]

# ---------------------------------------------------------------- stavebnice: kvadry po materialech do jedne site
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

def valec(m, x, y, z0, z1, r, n=12):
    body = [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z) for z in (z0, z1) for k in range(n)]
    steny = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    mnohostena(m, body, steny)

def mezikruzi(m, x, y, z0, z1, r0, r1, n=48):
    """kruh (r0 = 0) nebo mezikruzi jako placka"""
    bm = bm_pro(m)
    if r0 <= 0:
        valec(m, x, y, z0, z1, r1, n); return
    vn = [[bm.verts.new(B(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n), z)) for k in range(n)]
          for r, z in ((r0, z0), (r1, z0), (r0, z1), (r1, z1))]
    for k in range(n):
        k1 = (k + 1) % n
        bm.faces.new((vn[2][k], vn[3][k], vn[3][k1], vn[2][k1]))   # vrch
        bm.faces.new((vn[0][k], vn[0][k1], vn[1][k1], vn[1][k]))   # spodek
        bm.faces.new((vn[1][k], vn[1][k1], vn[3][k1], vn[3][k]))   # vnejsi
        bm.faces.new((vn[0][k], vn[2][k], vn[2][k1], vn[0][k1]))   # vnitrni

# ---------------------------------------------------------------- budova
X0, X1, Y0, Y1 = 1.8, 12.4, 3.0, 25.0            # hlavni hmota: hloubka 10,6 m, delka 22 m, prucelim k jihozapadu
ZS, ZP, ZPP, ZR = 0.7, 4.3, 7.9, 8.3            # sokl, patro, rimsa pod strechou, okap
YC = (Y0 + Y1) / 2
RIZ_Y0, RIZ_Y1, RIZ_X = YC - 3.2, YC + 3.2, X1 + 0.7   # stredni rizalit se vstupem
LIZ = 0.6                                        # sirka narozni lizeny

kvadr(M["fasada"], X0, X1, Y0, Y1, ZS, ZPP)
kvadr(M["sokl"], X0 - 0.06, X1 + 0.06, Y0 - 0.06, Y1 + 0.06, 0.0, ZS)
kvadr(M["bila"], X0 - 0.25, X1 + 0.25, Y0 - 0.25, Y1 + 0.25, ZPP, ZR)                # hlavni rimsa
kvadr(M["bila"], X0 - 0.08, X1 + 0.08, Y0 - 0.08, Y1 + 0.08, ZP - 0.1, ZP + 0.12)    # kordonova rimsa mezi patry
for yy in (Y0, Y1 - LIZ):                                                            # lizeny na rozich prucelim
    kvadr(M["bila"], X1, X1 + 0.06, yy, yy + LIZ, ZS, ZPP)
for xx in (X0, X1 - LIZ):                                                            # a na bocnim prucelim
    kvadr(M["bila"], xx, xx + LIZ, Y1, Y1 + 0.06, ZS, ZPP)
# rizalit
kvadr(M["fasada"], X1, RIZ_X, RIZ_Y0, RIZ_Y1, ZS, ZPP)
kvadr(M["sokl"], X1 + 0.06, RIZ_X + 0.06, RIZ_Y0 - 0.06, RIZ_Y1 + 0.06, 0.0, ZS)       # navazuji na sokl a rimsy hlavni
kvadr(M["bila"], X1 + 0.25, RIZ_X + 0.25, RIZ_Y0 - 0.25, RIZ_Y1 + 0.25, ZPP, ZR)         # budovy (driv prekryv ve stejne
kvadr(M["bila"], X1 + 0.08, RIZ_X + 0.08, RIZ_Y0 - 0.08, RIZ_Y1 + 0.08, ZP - 0.1, ZP + 0.12)  # vysce = cerna linka)
for yy in (RIZ_Y0, RIZ_Y1 - 0.5):
    kvadr(M["bila"], RIZ_X, RIZ_X + 0.06, yy, yy + 0.5, ZS, ZPP)
# stit nad rizalitem (trojuhelnik v rovine prucelim) a v nem kulate okno
ZST = ZR + 1.9
mnohostena(M["bila"], [(RIZ_X + 0.25, RIZ_Y0 - 0.25, ZR), (RIZ_X + 0.25, RIZ_Y1 + 0.25, ZR), (RIZ_X + 0.25, YC, ZST + 0.1),
                       (RIZ_X - 0.1, RIZ_Y0 - 0.25, ZR), (RIZ_X - 0.1, RIZ_Y1 + 0.25, ZR), (RIZ_X - 0.1, YC, ZST + 0.1)],
           [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)])
mnohostena(M["fasada"], [(RIZ_X + 0.27, RIZ_Y0 + 0.35, ZR + 0.12), (RIZ_X + 0.27, RIZ_Y1 - 0.35, ZR + 0.12), (RIZ_X + 0.27, YC, ZST - 0.32),
                         (RIZ_X + 0.2, RIZ_Y0 + 0.35, ZR + 0.12), (RIZ_X + 0.2, RIZ_Y1 - 0.35, ZR + 0.12), (RIZ_X + 0.2, YC, ZST - 0.32)],
           [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)])
okulus = (ZR + ZST) / 2 - 0.05
# kulate okno ve stitu: bily prstenec a sklo, osa kolma na prucelim (rovina y-z)
def kruh_ve_stene(m, x, yc, zc, r0, r1, tl, n=32):
    bm = bm_pro(m)
    for i, (ra, rb) in enumerate(((r0, r1),)):
        vn = [[bm.verts.new(B(xx, yc + r * math.cos(2 * math.pi * k / n), zc + r * math.sin(2 * math.pi * k / n))) for k in range(n)]
              for r, xx in ((ra, x), (rb, x), (ra, x + tl), (rb, x + tl))]
        for k in range(n):
            k1 = (k + 1) % n
            bm.faces.new((vn[2][k], vn[2][k1], vn[3][k1], vn[3][k]))
            bm.faces.new((vn[0][k], vn[1][k], vn[1][k1], vn[0][k1]))
            bm.faces.new((vn[1][k], vn[3][k], vn[3][k1], vn[1][k1]))
            bm.faces.new((vn[0][k], vn[0][k1], vn[2][k1], vn[2][k]))
def kotouc_ve_stene(m, x, yc, zc, r, tl, n=32):
    body = [(xx, yc + r * math.cos(2 * math.pi * k / n), zc + r * math.sin(2 * math.pi * k / n)) for xx in (x, x + tl) for k in range(n)]
    steny = [tuple(range(n)), tuple(range(n, 2 * n))[::-1]] + [(k, n + k, n + (k + 1) % n, (k + 1) % n) for k in range(n)]
    mnohostena(m, body, steny)
kotouc_ve_stene(M["sklo"], RIZ_X + 0.27, YC, okulus, 0.42, 0.02)
kruh_ve_stene(M["bila"], RIZ_X + 0.27, YC, okulus, 0.42, 0.58, 0.06)

# okna: bile ostenie vystupuje 5 cm, sklo tesne nad zdi (stin ostenia na skle dela hloubku), poutce do T,
# parapet a nadokenni rimsa
def okno(prucelim, u, z0, z1, sirka=1.2):
    """prucelim: ('x', X) okno ve stene x = X (lice k +x), ('y', Y) ve stene y = Y (lice k +y); u stred podel steny"""
    osa, lic = prucelim
    def q(m, a0, a1, d0, d1, zz0, zz1):          # a = podel steny, d = od lice ven
        if osa == 'x': kvadr(m, lic + d0, lic + d1, a0, a1, zz0, zz1)
        else: kvadr(m, a0, a1, lic + d0, lic + d1, zz0, zz1)
    s2, o = sirka / 2, 0.14
    q(M["sklo"], u - s2, u + s2, 0.0, 0.015, z0, z1)
    q(M["bila"], u - s2 - o, u - s2, 0.0, 0.05, z0 - o, z1 + o)          # ostenie
    q(M["bila"], u + s2, u + s2 + o, 0.0, 0.05, z0 - o, z1 + o)
    q(M["bila"], u - s2, u + s2, 0.0, 0.05, z1, z1 + o)
    q(M["bila"], u - s2 - 0.05, u + s2 + 0.05, 0.0, 0.11, z0 - 0.1, z0)   # parapet
    q(M["bila"], u - s2 - 0.22, u + s2 + 0.22, 0.0, 0.12, z1 + o, z1 + o + 0.12)   # nadokenni rimsa
    q(M["bila"], u - 0.03, u + 0.03, 0.0, 0.03, z0, z1)                    # poutce
    zt = z0 + (z1 - z0) * 0.68
    q(M["bila"], u - s2, u + s2, 0.0, 0.032, zt - 0.03, zt + 0.03)          # o 2 mm pred poutcem (krizeni)

OKNA_Z = [(1.55, 3.55), (5.15, 7.15)]
for z0, z1 in OKNA_Z:
    for k in range(3):
        okno(('x', X1), Y0 + LIZ + 1.2 + 2.4 * k, z0, z1)          # levé křídlo
        okno(('x', X1), RIZ_Y1 + 1.2 + 2.4 * k, z0, z1)            # pravé křídlo
        okno(('y', Y1), X0 + LIZ + 1.57 + 3.13 * k, z0, z1)        # bocni prucelim k jihovychodu
    okno(('x', RIZ_X), RIZ_Y0 + 0.95, z0, z1, 1.0)                 # rizalit, okna vedle vstupu a v patre
    okno(('x', RIZ_X), RIZ_Y1 - 0.95, z0, z1, 1.0)
okno(('x', RIZ_X), YC, 5.15, 7.15, 1.0)
# vstup: dvoukridle dvere v portalu, nad nimi napis, pred nimi tri schody
kvadr(M["bila"], RIZ_X, RIZ_X + 0.1, YC - 1.25, YC + 1.25, ZS, 3.55)          # portal
kvadr(M["dvere"], RIZ_X + 0.1, RIZ_X + 0.13, YC - 0.95, YC + 0.95, ZS, 3.25)
kvadr(M["bila"], RIZ_X + 0.1, RIZ_X + 0.15, YC - 0.03, YC + 0.03, ZS, 3.24)
# Schody jako jeden hranol se schodovitym profilem (do 2. 10. tri kvadry pres sebe: jejich boky lezely v jedne rovine
# pres sebe a Cycles takove plochy kresli cerne, hrac: "schody chybi jim bok", "ta cerna mista"). Zadni stena 5 cm
# v soklu rizalitu, at nelezi v rovine jeho lice.
PROFIL = [(RIZ_X - 0.05, 0.0), (RIZ_X + 1.08, 0.0), (RIZ_X + 1.08, 0.23), (RIZ_X + 0.72, 0.23), (RIZ_X + 0.72, 0.46),
          (RIZ_X + 0.36, 0.46), (RIZ_X + 0.36, 0.69), (RIZ_X - 0.05, 0.69)]
_n = len(PROFIL)
mnohostena(M["sokl"], [(x, YC - 1.6, z) for x, z in PROFIL] + [(x, YC + 1.6, z) for x, z in PROFIL],
           [tuple(range(_n)), tuple(range(2 * _n - 1, _n - 1, -1))] + [(k, k + _n, (k + 1) % _n + _n, (k + 1) % _n) for k in range(_n)])
bpy.ops.object.text_add(location=B(RIZ_X + 0.07, YC, 3.92), rotation=(math.radians(90), 0, 0))
napis = bpy.context.object; napis.data.body = "DÍVČÍ GYMNÁZIUM"; napis.data.align_x = 'CENTER'; napis.data.align_y = 'CENTER'
napis.data.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
napis.data.size = 0.3; napis.data.extrude = 0.015; napis.data.materials.append(M["napis"])
bpy.context.view_layer.update()
napis.scale = (4.9 / napis.dimensions.x, 0.34 / napis.dimensions.y, 1.0)

# valbova strecha: okap s presahem 0,5 m, sklon 28 st., hreben podel delky budovy
O_, SKLON = 0.5, math.radians(28)
ax0, ax1, ay0, ay1 = X0 - O_, X1 + O_, Y0 - O_, Y1 + O_
pul = (ax1 - ax0) / 2; zh = ZR + pul * math.tan(SKLON); xh = (ax0 + ax1) / 2
mnohostena(M["strecha"],
           [(ax0, ay0, ZR - 0.15), (ax1, ay0, ZR - 0.15), (ax1, ay1, ZR - 0.15), (ax0, ay1, ZR - 0.15),
            (ax0, ay0, ZR), (ax1, ay0, ZR), (ax1, ay1, ZR), (ax0, ay1, ZR),
            (xh, ay0 + pul, zh), (xh, ay1 - pul, zh)],
           [(0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
            (4, 5, 8), (5, 6, 9, 8), (6, 7, 9), (7, 4, 8, 9)])
# strecha rizalitu: sedlova od stitu az do hlavni strechy, hreben ve vysce stitu
rx0, rx1 = X1 - 3.4, RIZ_X + 0.18
mnohostena(M["strecha"],
           [(rx1, RIZ_Y0 - 0.45, ZR - 0.15), (rx1, RIZ_Y1 + 0.45, ZR - 0.15), (rx1, YC, ZST + 0.16),
            (rx0, RIZ_Y0 - 0.45, ZR - 0.15), (rx0, RIZ_Y1 + 0.45, ZR - 0.15), (rx0, YC, ZST + 0.16)],
           [(0, 2, 1), (3, 4, 5), (0, 3, 5, 2), (1, 2, 5, 4), (0, 1, 4, 3)])
for yy in (Y0 + 4.0, Y1 - 4.0):                                     # dva komíny na hrebeni
    kvadr(M["komin"], xh - 0.35, xh + 0.35, yy - 0.5, yy + 0.5, ZR + 1.0, zh + 0.9)
    kvadr(M["bila"], xh - 0.42, xh + 0.42, yy - 0.57, yy + 0.57, zh + 0.9, zh + 1.02)

# ---------------------------------------------------------------- okoli: predprostor, cesty, hriste, park
Z_ZEM = 0.035
kvadr(M["dlazba"], X1 + 0.06, X1 + 2.2, Y0 - 0.3, Y1 + 0.3, 0.0, Z_ZEM)            # dlazba podel prucelim
kvadr(M["dlazba"], X1 + 2.2, P, YC - 1.25, YC + 1.25, 0.0, Z_ZEM)             # hlavni cesta k plotu, navazuje na dlazbu
                                                                                 # podel prucelim (driv se prekryvaly: cerny pas)
# hriste: cerveny kurt s carami a dvema kosi (podel osy x)
KX0, KX1, KY0, KY1 = 15.2, 28.2, 1.6, 10.4
kvadr(M["kurt"], KX0, KX1, KY0, KY1, 0.0, Z_ZEM)
C, ZC_ = 0.08, Z_ZEM + 0.004
kx0, kx1, ky0, ky1 = KX0 + 0.5, KX1 - 0.5, KY0 + 0.5, KY1 - 0.5
# cary, ktere se krizi, kazda o 0,5 mm jinak vysoko (ve stejne vysce by krizeni bylo cerne)
for k, (a0, a1, b0, b1) in enumerate(((kx0, kx1, ky0, ky0 + C), (kx0, kx1, ky1 - C, ky1), (kx0, kx0 + C, ky0, ky1), (kx1 - C, kx1, ky0, ky1))):
    kvadr(M["cara"], a0, a1, b0, b1, 0.0, ZC_ + 0.0005 * (k // 2))
kxs, kys = (kx0 + kx1) / 2, (ky0 + ky1) / 2
kvadr(M["cara"], kxs - C / 2, kxs + C / 2, ky0, ky1, 0.0, ZC_ + 0.001)
mezikruzi(M["cara"], kxs, kys, 0.0, ZC_ + 0.0015, 1.5, 1.5 + C)
for kraj, smer in ((kx0, 1), (kx1, -1)):
    xa, xb = sorted((kraj, kraj + smer * 4.0))
    for (a0, a1, b0, b1) in ((xa, xb, kys - 2.0, kys - 2.0 + C), (xa, xb, kys + 2.0 - C, kys + 2.0)):
        kvadr(M["cara"], a0, a1, b0, b1, 0.0, ZC_ + 0.002)
    xr = kraj + smer * 4.0
    kvadr(M["cara"], xr - C / 2, xr + C / 2, kys - 2.0, kys + 2.0, 0.0, ZC_ + 0.0025)
    # kos: sloup za cárou, rameno, deska a obruc
    xs = kraj - smer * 0.35
    kvadr(M["kov"], xs - 0.06, xs + 0.06, kys - 0.06, kys + 0.06, 0.0, 3.3)
    xd = xs + smer * 0.9
    kvadr(M["kov"], min(xs, xd), max(xs, xd), kys - 0.05, kys + 0.05, 3.05, 3.15)
    kvadr(M["deska"], xd - 0.03, xd + 0.03, kys - 0.9, kys + 0.9, 2.85, 3.9)
    mezikruzi(M["obruc"], xd + smer * 0.25, kys, 3.03, 3.06, 0.2, 0.24, 24)
# park: kruhove namesticko s kvetinovym zahonem, lavicky, cesticky k hlavni ceste a ke druhemu plotu
PX_, PY_ = 21.6, 21.0
mezikruzi(M["sterk"], PX_, PY_, 0.0, Z_ZEM, 0.0, 3.3)
mezikruzi(M["zemina"], PX_, PY_, 0.0, Z_ZEM + 0.08, 0.0, 1.55)
import random
random.seed(7)
for i in range(70):                                                     # kvetiny v zahonu
    r = 1.45 * math.sqrt(random.random()); a = random.random() * 2 * math.pi
    x, y = PX_ + r * math.cos(a), PY_ + r * math.sin(a)
    kvadr(KVETY[i % len(KVETY)], x - 0.09, x + 0.09, y - 0.09, y + 0.09, Z_ZEM + 0.08, Z_ZEM + 0.08 + 0.12 + 0.12 * random.random())
kvadr(M["sterk"], PX_ - 0.6, PX_ + 0.6, YC + 1.25, PY_ - 3.1, 0.0, Z_ZEM - 0.002)    # o 2 mm nize nez namesticko,
kvadr(M["sterk"], PX_ - 0.6, PX_ + 0.6, PY_ + 3.1, P, 0.0, Z_ZEM - 0.002)            # do ktereho kus zajizdeji
# Holky a lavicky 1,5x vetsi nez budova (hrac 1. 10.: "skola zvetsit studentky, zvetsime i lavicky, dvere do skoly jsou
# velke dost, muzem zvetsit studentky"): holka 2,43 az 2,52 m, dvere 2,55 m, ve 2x (3,2 m) by uz dvermi neprosla.
K_LAV = float(os.environ.get("LAVICKY", "1.5"))
K_POSTAV = float(os.environ.get("POSTAVY_K", "1.5"))

def lavicka(x, y, uhel):
    """lavicka 1,6 m (krat K_LAV), sedak a operadlo ze dreva, nohy kov; uhel: kam se sedici diva (rad)"""
    c, s = math.cos(uhel), math.sin(uhel)
    def bod(u, v, z):                    # u podel lavicky, v dozadu (od pohledu sediciho)
        return (x + K_LAV * (u * -s + v * -c), y + K_LAV * (u * c + v * -s), K_LAV * z)
    def kus(m, u0, u1, v0, v1, z0, z1):
        b = [bod(u, v, z) for z in (z0, z1) for v in (v0, v1) for u in (u0, u1)]
        mnohostena(m, b, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
    kus(M["lavicka"], -0.8, 0.8, -0.22, 0.22, 0.42, 0.47)
    kus(M["lavicka"], -0.8, 0.8, 0.2, 0.25, 0.5, 0.88)
    for u in (-0.65, 0.65):
        kus(M["kov"], u - 0.03, u + 0.03, -0.2, 0.22, 0.0, 0.42)
for a in (45, 135, 225, 315):
    r = 2.75; aa = math.radians(a)
    lavicka(PX_ + r * math.cos(aa), PY_ + r * math.sin(aa), aa + math.pi)
lavicka(X1 + 1.6, Y0 + 2.5, 0.0); lavicka(X1 + 1.6, Y1 - 2.5, 0.0)
# lampy podel hlavni cesty, stozar s vlajkou u vstupu
for x, y in ((17.4, YC + 1.7), (24.6, YC + 1.7), (17.4, YC - 1.7), (24.6, YC - 1.7)):
    valec(M["kov"], x, y, 0.0, 3.4, 0.05, 8)
    mezikruzi(M["lampa"], x, y, 3.4, 3.75, 0.0, 0.16, 12)
valec(M["kov"], X1 + 1.5, YC - 4.6, 0.0, 7.6, 0.06, 8)
FX, FY0, FZ1 = X1 + 1.5, YC - 4.55, 7.45
FD, FV = 1.5, 1.0
mnohostena(M["v_bila"], [(FX, FY0, FZ1), (FX, FY0 + FD, FZ1), (FX, FY0 + FD, FZ1 - FV / 2), (FX, FY0, FZ1 - FV / 2)], [(0, 1, 2, 3)])
mnohostena(M["v_cervena"], [(FX + 0.002, FY0, FZ1 - FV / 2), (FX + 0.002, FY0 + FD, FZ1 - FV / 2), (FX + 0.002, FY0 + FD, FZ1 - FV), (FX + 0.002, FY0, FZ1 - FV)],
           [(0, 1, 2, 3)])
mnohostena(M["v_modra"], [(FX + 0.004, FY0, FZ1), (FX + 0.004, FY0 + FD / 2, FZ1 - FV / 2), (FX + 0.004, FY0, FZ1 - FV)], [(0, 1, 2)])
# zivy plot kolem pozemku s mezerami pro cesty
H_PL, PL0, PL1 = 0.8, 0.25, 0.85
def plot_x(x0, x1, y0, y1):
    if x1 - x0 > 0.2 and y1 - y0 > 0.2: kvadr(M["plot"], x0, x1, y0, y1, 0.0, H_PL)
plot_x(P - PL1, P - PL0, PL0, YC - 1.3); plot_x(P - PL1, P - PL0, YC + 1.3, P - PL0)        # jihozapadni strana
plot_x(PL0, PX_ - 0.65, P - PL1, P - PL0); plot_x(PX_ + 0.65, P - PL1, P - PL1, P - PL0)    # jihovychodni strana
plot_x(PL0, P - PL1, PL0, PL1)                                                             # severozapadni strana
plot_x(PL0, PL1, PL1, P - PL1)                                                             # severovychodni strana

# stromy: kmen a koruna z nekolika koul, stin od koruny dela hloubku. Kmen jde az doprostred koruny a spodni koule
# koruny sahaji k nemu (hrac 2. 10.: "dva stromy vedle budovy maji vysoko koruny nad kmenem, je to tycka ze zeme,
# mezera a koruna"; drive kmen koncil ve 45 % vysky a koruna zacinala az nad nim)
def strom(x, y, vyska, r, barva, seed, kmen=True):
    rnd = random.Random(seed)
    if kmen: valec(M["kmen"], x, y, 0.0, vyska - r * 1.05, 0.2, 8)
    obj_m = KORUNY[barva]
    for i in range(9 if kmen else 4):
        a = rnd.random() * 2 * math.pi; d = r * 0.55 * math.sqrt(rnd.random())
        cx, cy = x + d * math.cos(a), y + d * math.sin(a)
        cz = vyska - r * 1.1 + (rnd.random() - 0.5) * r * 0.6
        if kmen and i < 3:                                              # spodek koruny tesne nad kmenem
            cx, cy, cz = x + (cx - x) * 0.5, y + (cy - y) * 0.5, vyska - r * 1.7
        rr = r * (0.48 + 0.22 * rnd.random())
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=rr, location=B(cx, cy, cz))
        o = bpy.context.object; o.data.materials.append(obj_m)
        for p in o.data.polygons: p.use_smooth = True                 # koruna mekka, ne hranata
        d_ = o.modifiers.new("hrbol", 'DISPLACE'); tx = bpy.data.textures.new(f"t{seed}{i}", 'CLOUDS')
        tx.noise_scale = 0.35; d_.texture = tx; d_.strength = rr * 0.35
STROMY = [(4.2, 27.4, 8.0, 2.0, 0, 1), (10.8, 27.6, 7.0, 1.8, 1, 2), (27.3, 21.8, 6.5, 1.7, 2, 3)]
for s in STROMY: strom(*s)
for i, a in enumerate((15, 50, 130, 165, 200, 235, 305, 340)):         # kere kolem namesticka
    aa = math.radians(a); rr = 0.55 + 0.15 * (i % 3)
    strom(PX_ + 4.3 * math.cos(aa), PY_ + 4.3 * math.sin(aa), rr * 1.5, rr, i % 4, 20 + i, kmen=False)

# ---------------------------------------------------------------- site do sceny
for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
# ---------------------------------------------------------------- postavy (druhy obrazek do animace, POSTAVY=1)
# Hrac 1. 10.: "spawnem holky kolem skoly a automatu". Jako u sochy (socha/render_socha.py), ale ve skutecne velikosti
# jako budova a lavicky: na lavicce pred skolou Galaxia a Character Girl (jako u sochy), na zadni lavicce v parku
# celem k divakovi Anime Girl, po hlavni ceste jde k brane tmavovlasa (College Girl), pred schody si povidaji
# Character Girl a druha tmavovlasa a na hristi hazi na kos treti (College Girl ma skolni uniformu).
# Modely v postavy/ (autori v AUTORI-MODELU.md), pozy v postavy/postavy.py.
if os.environ.get("POSTAVY", "") == "1":
    sys.path.insert(0, os.path.join(TU, "..", "postavy"))
    import postavy as PO
    from mathutils import Matrix

    def do_sceny(meshe, kotva, gx, gy, gz, uhel):
        """postava (celem k -y, kotva = jeji bod, ktery ma stat v bode gx gy gz) celem ve smeru uhel"""
        PO.postav(meshe, Matrix.Translation(B(gx, gy, gz)) @ Matrix.Rotation(uhel, 4, 'Z') @ Matrix.Scale(K_POSTAV, 4)
                  @ Matrix.Translation(-kotva))

    def na_lavicku(meshe, kotva, lavicka_, u):
        """bod sedu na sedak lavicky (x, y, uhel) ve vzdalenosti u od jejiho stredu, zady k operadlu"""
        x, y, uhel = lavicka_
        c, s = math.cos(uhel), math.sin(uhel)
        u, v = u * K_LAV, 0.05 * K_LAV                # v: kousek dozadu k operadlu
        do_sceny(meshe, kotva, x + u * -s + v * -c, y + u * c + v * -s, 0.47 * K_LAV, uhel)

    LAV_SKOLA = (X1 + 1.6, Y1 - 2.5, 0.0)                                         # pred prucelim vpravo
    LAV_PARK = (PX_ + 2.75 * math.cos(math.radians(225)), PY_ + 2.75 * math.sin(math.radians(225)), math.radians(45))
    g, kotva = PO.sedici("galaxia_anime_girl"); na_lavicku(g, kotva, LAV_SKOLA, -0.4)
    ch, kotva = PO.sedici("character_people_girl_001"); na_lavicku(ch, kotva, LAV_SKOLA, 0.4)
    an, kotva = PO.sedici("anime_girl"); na_lavicku(an, kotva, LAV_PARK, 0.0)
    cg = PO.nacti_stojici("college_girl", 1.62, "ruce_dolu")
    do_sceny(cg, Vector((0, 0, 0)), 21.0, YC - 0.6, Z_ZEM, 0.0)                  # po hlavni ceste k brane
    # pred schody si dve povidaji, z profilu; od zvetseni 1,2 m od sebe a lampa na obrazku mezi nimi, ne pres ne
    ch2 = PO.nacti_stojici("character_people_girl_001", 1.68)
    do_sceny(ch2, Vector((0, 0, 0)), 15.4, 12.8, Z_ZEM, math.atan2(13.7 - 12.8, 14.6 - 15.4))
    cg2 = PO.nacti_stojici("college_girl", 1.62, "ruce_dolu")                   # tmava, na svetlych schodech
    do_sceny(cg2, Vector((0, 0, 0)), 14.6, 13.7, Z_ZEM, math.atan2(12.8 - 13.7, 15.4 - 14.6))   # bela Galaxia splyvala

    def strela(arm, meshe):
        """obe ruce z pozice T dopredu nahoru, jako kdyz hazi na kos"""
        for st, zn in (("R", 1), ("L", -1)):
            ram, loket = PO._kost(arm, f"Shoulder_{st}_"), PO._kost(arm, f"Elbow_{st}_")
            PO.otoc_kost(arm, ram, (0, 0, 1), zn * math.radians(78))
            PO.otoc_kost(arm, ram, (1, 0, 0), math.radians(-58))
            PO.otoc_kost(arm, loket, (1, 0, 0), math.radians(-25))
    hrac = PO.nacti("college_girl", 1.62, priprava=strela, nechat=PO.divka_a)
    OBRUC = (KX1 - 0.5 + 0.35 - 0.9 - 0.25, (KY0 + KY1) / 2)                      # obruc u jihozapadniho konce kurtu
    HX, HY = OBRUC[0] - 2.3, OBRUC[1] - 0.6
    do_sceny(hrac, Vector((0, 0, 0)), HX, HY, Z_ZEM, math.atan2(OBRUC[1] - HY, OBRUC[0] - HX))
    _, hi, vse = PO.rozmery_siti(hrac)
    ruce = vse[vse[:, 2] > hi[2] - 0.04]                                           # nejvys jsou ruce, mic nad nimi
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 * K_POSTAV, location=(ruce[:, 0].mean(), ruce[:, 1].mean(), hi[2] + 0.08 * K_POSTAV))
    mic = bpy.context.object; mic.data.materials.append(M["obruc"])
    for p_ in mic.data.polygons: p_.use_smooth = True

# chytac stinu pod pozemkem: pruhledny, jen stiny budovy a stromu na travu hry
bpy.ops.mesh.primitive_plane_add(size=1, location=B(P / 2, P / 2, 0.0))
zem = bpy.context.object; zem.scale = (P, P, 1); zem.is_shadow_catcher = True

# ---------------------------------------------------------------- kamera jako u Tatry, slunce jako u sochy
stred = B(P / 2, P / 2, 0.0)
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); cil = bpy.context.object
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 80.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = cil
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * float(os.environ.get("ZEPREDU", "-0.25")) + Vector((0, 0, float(os.environ.get("SHORA", "1.0"))))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "2.0")); sl.data.angle = math.radians(6)   # do 3. 10. 5,0
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def na_pixel(p):
    bpy.context.view_layer.update()
    q = world_to_camera_view(scene, cam, p)
    return (q.x * RAM, (1 - q.y) * RAM)
rohy = {"sever": na_pixel(B(0, 0, 0)), "vychod": na_pixel(B(0, P, 0)), "zapad": na_pixel(B(P, 0, 0)), "jih": na_pixel(B(P, P, 0))}
print("rohy pozemku na obrazku", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()})
# Stin na travu: chytac stinu ho dava tmavy. Druhy render bez chytace da jen predmety, rozdil je stin a ten jde do
# obrazku jen na STIN (20 % jako u sochy, do 3. 10. 55 %).
import numpy as np
from PIL import Image
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
json.dump({"px_m": PX_M, "policko_m": T, "ram": RAM, "rohy": rohy}, open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
