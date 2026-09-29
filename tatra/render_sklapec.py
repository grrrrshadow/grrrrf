# -*- coding: utf-8 -*-
# Nahled sklapece T148 S1 (hans1240 "Tatra-148", Sketchfab, CC BY 4.0).
# Hrac 29. 9. rozhodl: bereme podle licence, kterou hans1240 uvadi (CC BY), model jako predlohu, auto je ve hre
# asi 120 x 60 px. Kamera a smery jako vejtraska (render_v3s.py), svetlo silnejsi zleva shora (SVETLO).
# Hrac 29. 9.: "co vozime kupy a pytle by slo asi na tuhle". KUPA=GRVL|SAND|COAL nasype do korby kupu.
#   python3 render_sklapec.py <oranzova|cervena> <px_na_m> <ram_px> <vystup>
import bpy, os, sys, math
import numpy as np
from mathutils import Vector
NATER, PX_M, RAM, VYSTUP = sys.argv[-4], float(sys.argv[-3]), int(sys.argv[-2]), sys.argv[-1]
TU = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(TU, "model", "tatra-148.glb")
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
SAMPLES = int(os.environ.get("SAMPLES", "128"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
ROTATION_ANGLES = [225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0]    # celo na -Y jako vejtraska
os.makedirs(VYSTUP, exist_ok=True)
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
# Svetlo (hrac 29. 9.: "lepe osvetlit, at vynikne zaobleni kolem mrizky chladice smerem ke kabine, asi vic stinu"):
# SVETLO=slunce zapne stiny od okoli (zakouti a zaobleni ztmavnou) a prida slunce zleva shora, pevne vuci kamere,
# takze je ve vsech 8 smerech stejne. SVETLO=okoli je puvodni ploche svetlo jako u vejtrasky.
SVETLO = os.environ.get("SVETLO", "slunce")
scene.world.cycles_visibility.shadow = SVETLO == "slunce"
if SVETLO == "slunce":
    bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.35"))

bpy.ops.import_scene.gltf(filepath=MODEL)
koren = [o for o in scene.objects if o.parent is None][0]
koren.scale = (0.01, 0.01, 0.01)                     # model je v centimetrech
bpy.context.view_layer.update()
meshe = [o for o in scene.objects if o.type == 'MESH']

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)
def mat(jmeno, rgb, drsnost=0.6, kov=0.0, sviti=0.0):
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = srgb(rgb)
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if sviti:
        b.inputs["Emission Color"].default_value = srgb(rgb); b.inputs["Emission Strength"].default_value = sviti
    return m
NATERY = {"oranzova": (224, 104, 24), "cervena": (176, 24, 20)}
M = {"lak": mat("lak", NATERY[NATER]), "ram": mat("ram", (22, 22, 22)), "naprava": mat("naprava", (40, 40, 38)),
     "podvozek": mat("podvozek", (58, 58, 56)), "pneu": mat("pneu", (26, 26, 26), 0.85),
     "sklo": mat("sklo", (8, 10, 14), 0.15), "zrcatko": mat("zrcatko", (30, 36, 44), 0.1, 0.8),
     "zadni": mat("zadni", (150, 26, 18), 0.4, 0.0, 0.6), "svetlo": mat("svetlo", (255, 255, 250), 0.2, 0.0, 1.5),
     "blinkr": mat("blinkr", (255, 170, 60), 0.3, 0.0, 0.8), "mrizka": mat("mrizka", (14, 14, 14), 0.8)}
if SVETLO == "slunce":
    M["lak"].node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = float(os.environ.get("LESK", "0.42"))
def obarvi(o, m):
    o.data.materials.clear(); o.data.materials.append(m)
for o in meshe:
    n = o.name
    if n.startswith(("Kabina", "KorbaS1", "Kolo")): obarvi(o, M["lak"])
    elif n.startswith("Pneu"): obarvi(o, M["pneu"])
    elif n.startswith("RamTk"): obarvi(o, M["ram"])
    elif n.startswith("TG_POLOOSA"): obarvi(o, M["naprava"])
    elif n.startswith("TG_T148"): obarvi(o, M["podvozek"])
    elif n.startswith("ZS"): obarvi(o, M["zadni"])
    else: print("bez barvy", n)
# Korba (hrac 29. 9.: "pripravime valnik, pro plny valnik plachta a cisterna na tekutiny"): KORBA=sklapec je korba
# S1 z modelu, valnik / plachta / cisterna ji schovaji a postavi svoji nastavbu (nize), zadna necha jen podvozek.
KORBA = os.environ.get("KORBA", "sklapec")
if KORBA != "sklapec":
    for o in meshe:
        if o.name.startswith("KorbaS1"): o.hide_render = True

# skla: kabina je jeden kus i se skly, rozdelit na samostatne kusy a skla najit podle polohy a velikosti (metry)
kab = [o for o in meshe if o.name.startswith("Kabina")][0]
bpy.ops.object.select_all(action='DESELECT'); kab.select_set(True); bpy.context.view_layer.objects.active = kab
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
kusy = [o for o in scene.objects if o.type == 'MESH' and o.name.startswith("Kabina")]
def je_sklo(mn, mx, plocha):
    ax0, ax1 = min(abs(mn.x), abs(mx.x)), max(abs(mn.x), abs(mx.x)); jedna_strana = mn.x * mx.x > 0
    if mn.y >= 0.75 and mx.y <= 1.45 and mn.z >= 1.75 and mx.z <= 2.36 and plocha >= 0.8: return "sklo"         # celni sklo
    if jedna_strana and ax0 >= 1.0 and ax1 <= 1.09 and mn.y >= 1.1 and mx.y <= 2.02 and mn.z >= 1.69 and mx.z <= 2.27 and plocha >= 0.2:
        return "sklo"                                                                                             # okna ve dverich
    if mn.y >= 2.19 and mx.y <= 2.24 and mn.z >= 1.95 and mx.z <= 2.23 and plocha >= 0.05: return "sklo"       # zadni okno
    if jedna_strana and ax0 >= 1.25 and ax1 <= 1.43 and mn.z >= 1.65 and mx.z <= 2.01 and 0.02 <= plocha < 0.05:
        return "zrcatko"
    if jedna_strana and mx.y < -0.25 and 0.75 <= ax0 and ax1 <= 1.05 and mn.z >= 0.88 and mx.z <= 1.15 and 0.02 <= plocha <= 0.05:
        return "svetlo"                                                                                           # reflektory v blatnicich
    if jedna_strana and mn.y >= -0.27 and mx.y <= -0.24 and 0.8 <= ax0 and ax1 <= 1.06 and mn.z >= 1.2 and mx.z <= 1.4 and plocha >= 0.02:
        return "blinkr"                                                                                           # smerovky na blatnicich
    return None
pocet = {}
for o in kusy:
    P = [o.matrix_world @ v.co for v in o.data.vertices]
    mn = Vector((min(q.x for q in P), min(q.y for q in P), min(q.z for q in P)))
    mx = Vector((max(q.x for q in P), max(q.y for q in P), max(q.z for q in P)))
    s = o.matrix_world.to_scale()[0]
    plocha = sum(p.area for p in o.data.polygons) * s * s
    k = je_sklo(mn, mx, plocha)
    if k:
        obarvi(o, M[k]); pocet[k] = pocet.get(k, 0) + 1
print("skla", pocet)

def kvadr(m, x0, x1, y0, y1, z0, z1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object; o.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    b = o.modifiers.new("hrana", 'BEVEL'); b.width = min(0.006, min(x1 - x0, y1 - y0, z1 - z0) / 3); b.segments = 2
    o.data.materials.append(m); o.parent = koren; o.matrix_parent_inverse = koren.matrix_world.inverted()
    return o

# Mrizka chladice (hrac 29. 9.: "musime zlepsit chladic mrizku, ted tam neni zadnej"; k fotkam skutecne T148:
# "tam ma byt napis tatra a nakonec to splyne s temi mrizkami", "tam udelej mrizku vsude a je to jak napis").
# Model ma na masce jen hladkou plochu: predni strana y = -0,477, x +-0,54, z 0,995 az 1,53, okraj masky o 1 cm
# vpredu. Skutecna T148 ma uprostred masky mrizku 7 rad: 2 rady otvoru, napis TATRA pres pul mrizky, 4 rady otvoru,
# 3 sloupce (prostredni o kus sirsi) a po stranach masky 3 vodorovna zebra. Nahore uprostred ma skutecna plech,
# tady jsou otvory vsude. Pismena jsou tmava jako otvory, v malem je z napisu dalsi rada mrizky.
MRIZKA = os.environ.get("MRIZKA", "148")
if MRIZKA == "148":
    YM, VOTVOR, PUL, DELIC = -0.477, 0.045, 0.378, 0.022
    RADY, ZNAPIS = [1.472, 1.404, 1.256, 1.188, 1.120, 1.052], 1.330
    a_ = (2 * PUL - 2 * DELIC) / 3.15; c_ = 1.15 * a_
    SLOUPCE = [(-PUL, -PUL + a_), (-PUL + a_ + DELIC, PUL - a_ - DELIC), (PUL - a_, PUL)]
    for zc in RADY:
        for x0, x1 in SLOUPCE:
            kvadr(M["mrizka"], x0, x1, YM - 0.004, YM + 0.004, zc - VOTVOR / 2, zc + VOTVOR / 2)
    for str_ in (-1, 1):                                                   # zebra po stranach masky
        for zc in (1.35, 1.24, 1.13):
            x0, x1 = sorted((str_ * 0.400, str_ * 0.515))
            kvadr(M["mrizka"], x0, x1, YM - 0.003, YM + 0.003, zc - 0.006, zc + 0.006)
    bpy.ops.object.text_add(location=(0, YM - 0.006, ZNAPIS), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = "TATRA"; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
    t.data.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    t.data.size = 0.08; t.data.extrude = 0.002; t.data.materials.append(M["mrizka"])
    bpy.context.view_layer.update()
    t.scale = (0.39 / t.dimensions.x, 0.062 / t.dimensions.y, 1.0)          # napis 39 cm siroky, 6,2 cm vysoky
    bpy.context.view_layer.update()
    t.parent = koren; t.matrix_parent_inverse = koren.matrix_world.inverted()

elif MRIZKA == "138":
    # Mrizka T138 (hrac 29. 9.: "a co 138?", "barva je dobra, mrizku zkus trochu zlepsit"; podle jeho videa
    # skutecne T138 a ctyr fotek T138): ovalny otvor, nahore sirsi a zaobleny, dole plossi, za nim tma.
    # V nem 15 svislych lamel do vejire (sbihaji se k bodu pod mrizkou, uprostred svisle, na krajich 32 stupnu,
    # dole skoro u sebe, nahore se krajni ohybaji jeste vic ven). Lamely v barve auta
    # (ZEBRA=bila jako na nekterych fotkach). Nad otvorem ovalny chromovy stitek s cervenym napisem TATRA.
    # Jinak je 138 stejna jako 148.
    import bmesh
    # Hrac k 2. verzi: "to pulkulaty trochu vys a vetsi a ztrati se to. 148 je hranata a mrizka nepasuje, dej mrizku
    # vys a opticky se lip spoji do hranate 148", pak "tahle ovalna je asi dobra". Oval zustava, je vetsi (92 x 44 cm)
    # a vys, vrchol oblouku 2 cm pod horni hranou hladke plochy masky 148 (z 1,528), takze nejsou videt dva oblouky
    # nad sebou. Stitek je nad mrizkou na hornim pasku masky.
    YM, ZC, A_, BH, BD = -0.477, 1.235, 0.46, 0.27, 0.17
    obrys = []
    for k in range(144):
        u = 2 * math.pi * k / 144; cu, su = math.cos(u), math.sin(u)
        if su >= 0:                                                            # horni pul: plossi oblouk
            x = A_ * math.copysign(abs(cu) ** (2 / 2.5), cu); z = ZC + BH * abs(su) ** (2 / 2.5)
        else:                                                                  # dolni pul: uzsi a plossi
            x = A_ * math.copysign(abs(cu) ** (2 / 3.0), cu) * (1 - 0.12 * abs(su)); z = ZC - BD * abs(su) ** (2 / 3.5)
        obrys.append((x, z))
    bm = bmesh.new(); vs = [bm.verts.new((x, YM - 0.002, z)) for x, z in obrys]; bm.faces.new(vs)
    me = bpy.data.meshes.new("otvor138"); bm.to_mesh(me); bm.free()
    # hrac: "cernou pod lamely": za lamelami ciste cerna bez odlesku, at je mrizka v malem videt
    M["cerna"] = mat("cerna", (0, 0, 0), 1.0); M["cerna"].node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.0
    ot = bpy.data.objects.new("otvor138", me); scene.collection.objects.link(ot); ot.data.materials.append(M["cerna"])
    ot.parent = koren; ot.matrix_parent_inverse = koren.matrix_world.inverted()
    def v_obrysu(px, pz, dx, dz):                                             # kde paprsek vstupuje a vystupuje z otvoru
        ts = []
        for (x0, z0), (x1, z1) in zip(obrys, obrys[1:] + obrys[:1]):
            ex, ez = x1 - x0, z1 - z0; det = dx * (-ez) - dz * (-ex)
            if abs(det) < 1e-12: continue
            t = ((x0 - px) * (-ez) - (z0 - pz) * (-ex)) / det; w = (dx * (z0 - pz) - dz * (x0 - px)) / det
            if 0 <= w <= 1 and t > 0: ts.append(t)
        return min(ts), max(ts)
    # hrac: "jen trochu zvyraznit, at na malinky fotce je trochu videt, nemusi to byt presny" (LAMEL, SIRKA)
    # 9 sirsich lamel misto 15 (jako na fotkach): v herni velikosti jsou videt svisle prouzky, 15 uzkych splyne v tmu
    UHEL, LAMEL, SIRKA = 32.0, int(os.environ.get("LAMEL", "9")), float(os.environ.get("SIRKA", "0.065"))
    ZP = ZC - (A_ - 0.035) / math.tan(math.radians(UHEL))                    # kam se lamely sbihaji
    m_lam = M["lak"] if os.environ.get("ZEBRA", "lak") == "lak" else mat("lamely", (232, 230, 220), 0.4)
    OHYB = 0.10                                                                # jak moc se krajni lamely nahore ohnou ven
    for i in range(LAMEL):
        th = math.radians(-UHEL + 2 * UHEL * i / (LAMEL - 1)); dx, dz = math.sin(th), math.cos(th)
        nx, nz = math.copysign(1.0, th) * math.cos(th), -math.copysign(1.0, th) * math.sin(th)   # kolmo ven
        t0, t1 = v_obrysu(0.0, ZP, dx, dz); t0 += 0.01; t1 -= 0.014
        ohyb = OHYB * abs(th) / math.radians(UHEL)
        bm = bmesh.new(); rady = []
        for j in range(13):
            f = j / 12; t = t0 + (t1 - t0) * f; o_ = ohyb * f * f * (t1 - t0)
            cx, cz = t * dx + o_ * nx, ZP + t * dz + o_ * nz
            tx, tz = dx + 2 * ohyb * f * nx, dz + 2 * ohyb * f * nz; dl = math.hypot(tx, tz); px, pz = tz / dl, -tx / dl
            rady.append([bm.verts.new((cx + q * SIRKA / 2 * px, YM - 0.012, cz + q * SIRKA / 2 * pz)) for q in (-1, 1)])
        for r0, r1 in zip(rady, rady[1:]):
            bm.faces.new((r0[0], r0[1], r1[1], r1[0]))
        me = bpy.data.meshes.new("lamela"); bm.to_mesh(me); bm.free()
        la = bpy.data.objects.new("lamela", me); scene.collection.objects.link(la)
        so = la.modifiers.new("tloustka", 'SOLIDIFY'); so.thickness = 0.012; so.offset = 0
        bv = la.modifiers.new("hrana", 'BEVEL'); bv.width = 0.004; bv.segments = 2
        la.data.materials.append(m_lam)
        for f_ in me.polygons: f_.use_smooth = True
        la.parent = koren; la.matrix_parent_inverse = koren.matrix_world.inverted()
    M["chrom"] = mat("chrom", (196, 196, 190), 0.25, 0.9)
    # stitek na hornim pasku masky (y -0,486, z 1,53 az 1,57) a kousek na kapote, skloneny dozadu jako kapota
    ZST, YST, SKLON = 1.565, -0.490, math.radians(90 - 18)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.0, depth=0.006, location=(0, YST, ZST),
                                        rotation=(SKLON, 0, 0))
    st_ = bpy.context.object; st_.scale = (0.16, 0.03, 1.0); st_.data.materials.append(M["chrom"])
    st_.parent = koren; st_.matrix_parent_inverse = koren.matrix_world.inverted()
    M["napis"] = mat("napis", (200, 16, 16), 0.35)
    bpy.ops.object.text_add(location=(0, YST - 0.0045 * math.sin(SKLON), ZST + 0.0045 * math.cos(SKLON)), rotation=(SKLON, 0, 0))
    t = bpy.context.object; t.data.body = "TATRA"; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
    t.data.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    t.data.size = 0.08; t.data.extrude = 0.002; t.data.materials.append(M["napis"])
    bpy.context.view_layer.update()
    t.scale = (0.25 / t.dimensions.x, 0.036 / t.dimensions.y, 1.0)
    bpy.context.view_layer.update()
    t.parent = koren; t.matrix_parent_inverse = koren.matrix_world.inverted()

# ---------------------------------------------------------------- nastavby misto korby S1
# Podvozek bez korby (namereno, vycniva.py): pomocny ram x +-0,35 az 0,50 nahore z 1,18 od y 2,16 do 6,37, za kabinou
# (kabina konci y 2,24) rezervni kolo a schranka az do z 2,3 v y 2,2 az 2,6, dily sklapeni do z 1,30 v y 3,6 az 5,3
# (schovaji se pod podlahu). Nastavby proto zacinaji az za rezervou na y 2,70 a konci na y 7,00 jako korba S1.
def mat_sum(jmeno, tmava, svetla, drsnost, meritko=18.0, vlny=False):
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    n_ = m.node_tree.nodes; l_ = m.node_tree.links; b = n_["Principled BSDF"]
    if vlny:                                                               # prkna podel auta (spary po 15 cm)
        tx = n_.new("ShaderNodeTexWave"); tx.wave_type = 'BANDS'; tx.bands_direction = 'X'
        tx.inputs["Scale"].default_value = 3.3; tx.inputs["Distortion"].default_value = 1.5
        sou = n_.new("ShaderNodeTexCoord"); l_.new(sou.outputs["Object"], tx.inputs["Vector"])
    else:
        tx = n_.new("ShaderNodeTexNoise"); tx.inputs["Scale"].default_value = meritko; tx.inputs["Detail"].default_value = 6.0
    ra = n_.new("ShaderNodeValToRGB"); ra.color_ramp.elements[0].color = srgb(tmava); ra.color_ramp.elements[1].color = srgb(svetla)
    l_.new(tx.outputs["Fac"] if "Fac" in tx.outputs else tx.outputs[0], ra.inputs["Fac"]); l_.new(ra.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = drsnost
    return m
Y0N, Y1N = 2.70, 7.00                                                      # nastavba od / do
if KORBA in ("valnik", "plachta"):
    # Valnik (hrac 29. 9.: "pripravime valnik"): drevena podlaha z 1,36 na pricnicich, sklopne ocelove bocnice
    # 0,6 m v barve auta se dvema prolisy, na kazde strane dva dily s klanici uprostred, zadni celo stejne,
    # predni celo 1,0 m a nad nim mrizka proti nakladu do kabiny.
    ZP_, XV, BOK = 1.36, 1.24, 0.60
    m_prkna = mat_sum("prkna", (96, 66, 40), (142, 104, 66), 0.85, vlny=True)
    m_klanice = mat("klanice", (40, 40, 38), 0.5)
    y = Y0N + 0.10
    while y < Y1N - 0.05:                                                  # pricniky pod podlahou
        kvadr(M["ram"], -XV + 0.04, XV - 0.04, y - 0.04, y + 0.04, 1.19, ZP_ - 0.05); y += 0.55
    kvadr(m_prkna, -XV + 0.05, XV - 0.05, Y0N + 0.05, Y1N - 0.05, ZP_ - 0.05, ZP_)          # podlaha
    for str_ in (-1, 1):                                                   # obvodovy ram podlahy
        x0, x1 = sorted((str_ * (XV - 0.06), str_ * XV)); kvadr(M["lak"], x0, x1, Y0N, Y1N, ZP_ - 0.12, ZP_)
    for yy in (Y0N, Y1N - 0.06):
        kvadr(M["lak"], -XV, XV, yy, yy + 0.06, ZP_ - 0.12, ZP_)
    YD = (Y0N + 0.05 + Y1N) / 2                                            # deleni bocnice (klanice)
    for str_ in (-1, 1):
        for ya, yb in ((Y0N + 0.05, YD - 0.02), (YD + 0.02, Y1N)):
            x0, x1 = sorted((str_ * (XV - 0.035), str_ * XV))
            kvadr(M["lak"], x0, x1, ya, yb, ZP_, ZP_ + BOK)                    # dil bocnice
            x0, x1 = sorted((str_ * XV, str_ * (XV + 0.012)))
            for zp in (ZP_ + 0.17, ZP_ + 0.40):                                  # prolisy
                kvadr(M["lak"], x0, x1, ya + 0.06, yb - 0.06, zp, zp + 0.05)
            x0, x1 = sorted((str_ * (XV - 0.04), str_ * (XV + 0.012)))
            kvadr(M["lak"], x0, x1, ya, yb, ZP_ + BOK - 0.035, ZP_ + BOK)      # horni lem
            for yz in (ya + 0.25, (ya + yb) / 2, yb - 0.25):                     # panty dole
                x0, x1 = sorted((str_ * XV, str_ * (XV + 0.02))); kvadr(m_klanice, x0, x1, yz - 0.05, yz + 0.05, ZP_ - 0.03, ZP_ + 0.03)
        x0, x1 = sorted((str_ * (XV - 0.02), str_ * (XV + 0.03)))
        for yk in (Y0N + 0.03, YD, Y1N - 0.03):                                # klanice
            kvadr(m_klanice, x0, x1, yk - 0.035, yk + 0.035, ZP_ - 0.10, ZP_ + BOK + 0.02)
    kvadr(M["lak"], -XV, XV, Y1N - 0.035, Y1N, ZP_, ZP_ + BOK)                  # zadni celo
    for zp in (ZP_ + 0.17, ZP_ + 0.40):
        kvadr(M["lak"], -XV + 0.08, XV - 0.08, Y1N, Y1N + 0.012, zp, zp + 0.05)
    kvadr(M["lak"], -XV, XV, Y1N - 0.04, Y1N + 0.012, ZP_ + BOK - 0.035, ZP_ + BOK)
    CELO = 1.00
    kvadr(M["lak"], -XV, XV, Y0N, Y0N + 0.04, ZP_, ZP_ + CELO)                  # predni celo
    for zp in (ZP_ + 0.20, ZP_ + 0.50, ZP_ + 0.80):
        kvadr(M["lak"], -XV + 0.08, XV - 0.08, Y0N - 0.012, Y0N, zp, zp + 0.05)
    for xm in (-XV + 0.02, -0.42, 0.0, 0.42, XV - 0.02):                        # mrizka nad celem
        kvadr(m_klanice, xm - 0.02, xm + 0.02, Y0N, Y0N + 0.04, ZP_ + CELO, ZP_ + CELO + 0.30)
    kvadr(m_klanice, -XV, XV, Y0N, Y0N + 0.04, ZP_ + CELO + 0.27, ZP_ + CELO + 0.31)
    print("valnik: podlaha z", ZP_, "y", Y0N, "az", Y1N, "bocnice", BOK)
if KORBA == "plachta":
    # Plachta na plny valnik (hrac 29. 9.: "pro plny valnik plachta"), jako u vejtrasky: boky svisle kousek pres
    # bocnice, strecha 1,6 m nad podlahou (z 2,96), podelne hrany zaoblene jako oblouky, vpredu u cela a vzadu rovne.
    PLACHTY = {"seda": ((86, 88, 86), (136, 138, 134)), "zluta": ((168, 136, 36), (224, 190, 74)),
               "sedobila": ((168, 168, 160), (222, 222, 214)), "rezna": ((170, 160, 128), (220, 212, 178))}
    tm_, sv_ = PLACHTY[os.environ.get("PLACHTA", "seda")]
    m_pl = mat_sum("plachta", tm_, sv_, 0.95, 7.0); nt_ = m_pl.node_tree; bs_ = nt_.nodes["Principled BSDF"]
    vr = nt_.nodes.new("ShaderNodeTexNoise"); vr.inputs["Scale"].default_value = 3.0; vr.inputs["Detail"].default_value = 4.0
    hb = nt_.nodes.new("ShaderNodeBump"); hb.inputs["Strength"].default_value = 0.25
    nt_.links.new(vr.outputs["Fac"], hb.inputs["Height"]); nt_.links.new(hb.outputs["Normal"], bs_.inputs["Normal"])
    X_, Z0_, Z1_, R_ = XV + 0.02, ZP_ + BOK - 0.12, ZP_ + 1.60, 0.30
    profil = [(-X_, Z0_)]
    for k in range(9):
        a_ = math.radians(180 - 90 * k / 8); profil.append((-X_ + R_ + R_ * math.cos(a_), Z1_ - R_ + R_ * math.sin(a_)))
    for k in range(9):
        a_ = math.radians(90 - 90 * k / 8); profil.append((X_ - R_ + R_ * math.cos(a_), Z1_ - R_ + R_ * math.sin(a_)))
    profil.append((X_, Z0_))
    import bmesh
    bm = bmesh.new()
    pr_ = [bm.verts.new((x, Y0N + 0.045, z)) for x, z in profil]; za_ = [bm.verts.new((x, Y1N + 0.02, z)) for x, z in profil]
    for i in range(len(profil) - 1):
        bm.faces.new((za_[i], za_[i + 1], pr_[i + 1], pr_[i]))
    bm.faces.new(pr_[::-1]); bm.faces.new(za_); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("plachta"); bm.to_mesh(me); bm.free()
    pl = bpy.data.objects.new("plachta", me); scene.collection.objects.link(pl); pl.data.materials.append(m_pl)
    pl.parent = koren; pl.matrix_parent_inverse = koren.matrix_world.inverted()

if KORBA == "cisterna":
    # Cisterna na tekutiny (hrac 29. 9.: "cisterna na tekutiny"; hasicska z modelu AKT mela nahore hrb). Vlastni,
    # hladka: ovalny prurez 2,30 x 1,45 m (superelipsa), vydute dna, delka 4,3 m od y 2,76 do 7,02, dno z 1,30 na trech
    # sedlech na pomocnem ramu, dve obruce, dva nizke prulezy nahore (zadny hrb), vzadu vypust a zebrik, nad zadnimi
    # koly blatniky. Asi 11 m3.
    import bmesh
    m_klanice = mat("klanice", (40, 40, 38), 0.5)
    A_, B_, N_, ZC_ = 1.15, 0.725, 2.4, 1.30 + 0.725
    Y0T, Y1T, HL = 2.76, 7.02, 0.16                                        # od, do, hloubka dna
    def prurez(f, zvetseni=1.0, n=48):
        body = []
        for k in range(n):
            u = 2 * math.pi * k / n; cu, su = math.cos(u), math.sin(u)
            body.append((A_ * f * zvetseni * math.copysign(abs(cu) ** (2 / N_), cu), ZC_ + B_ * f * zvetseni * math.copysign(abs(su) ** (2 / N_), su)))
        return body
    L_ = Y1T - Y0T; kroky = [HL * (1 - math.cos(math.pi / 2 * k / 10)) for k in range(11)]
    usek = [0.0] + kroky[1:] + [L_ / 2] + [L_ - d for d in reversed(kroky)][:-1] + [L_]
    usek = sorted(set(round(u, 5) for u in usek))
    bm = bmesh.new(); kruhy = []
    for u in usek:
        d = min(u, L_ - u); f = math.sqrt(max(0.0, 1 - ((HL - d) / HL) ** 2)) if d < HL else 1.0
        f = max(f, 0.03); kruhy.append([bm.verts.new((x, Y0T + u, z)) for x, z in prurez(f)])
    for r0, r1 in zip(kruhy, kruhy[1:]):
        for i in range(len(r0)):
            j = (i + 1) % len(r0); bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
    bm.faces.new(kruhy[0][::-1]); bm.faces.new(kruhy[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("cisterna"); bm.to_mesh(me); bm.free()
    for f_ in me.polygons: f_.use_smooth = True
    ci = bpy.data.objects.new("cisterna", me); scene.collection.objects.link(ci); ci.data.materials.append(M["lak"])
    ci.parent = koren; ci.matrix_parent_inverse = koren.matrix_world.inverted()
    for yo in (Y0T + 1.25, Y1T - 1.25):                                     # obruce
        bm = bmesh.new(); r0 = [bm.verts.new((x, yo - 0.03, z)) for x, z in prurez(1.0, 1.012)]
        r1 = [bm.verts.new((x, yo + 0.03, z)) for x, z in prurez(1.0, 1.012)]
        for i in range(len(r0)):
            j = (i + 1) % len(r0); bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
        me = bpy.data.meshes.new("obruc"); bm.to_mesh(me); bm.free()
        for f_ in me.polygons: f_.use_smooth = True
        ob_ = bpy.data.objects.new("obruc", me); scene.collection.objects.link(ob_); ob_.data.materials.append(M["lak"])
        ob_.parent = koren; ob_.matrix_parent_inverse = koren.matrix_world.inverted()
    for ys in (Y0T + 0.45, (Y0T + Y1T) / 2, Y1T - 0.45):                    # sedla
        kvadr(M["ram"], -0.56, 0.56, ys - 0.07, ys + 0.07, 1.18, 1.36)
    ZV = ZC_ + B_
    for yp in (Y0T + 1.0, Y1T - 1.0):                                       # prulezy nahore, nizke
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.24, depth=0.12, location=(0, yp, ZV + 0.03))
        d_ = bpy.context.object; d_.data.materials.append(M["lak"]); bpy.ops.object.shade_smooth()
        d_.parent = koren; d_.matrix_parent_inverse = koren.matrix_world.inverted()
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.26, depth=0.03, location=(0, yp, ZV + 0.10))
        v_ = bpy.context.object; v_.data.materials.append(m_klanice); bpy.ops.object.shade_smooth()
        v_.parent = koren; v_.matrix_parent_inverse = koren.matrix_world.inverted()
    kvadr(m_klanice, -0.16, 0.16, Y1T - 0.10, Y1T + 0.08, 1.12, 1.32)       # vypust vzadu
    for xz in (-0.62, -0.34):                                               # zebrik vzadu vlevo
        kvadr(m_klanice, xz - 0.015, xz + 0.015, Y1T + 0.02, Y1T + 0.05, 0.95, ZV - 0.05)
    zz = 1.05
    while zz < ZV - 0.1:
        kvadr(m_klanice, -0.62, -0.34, Y1T + 0.02, Y1T + 0.05, zz, zz + 0.025); zz += 0.25
    for str_ in (-1, 1):                                                    # blatniky nad zadnimi koly
        x0, x1 = sorted((str_ * 0.64, str_ * 1.30)); kvadr(M["ram"], x0, x1, 3.60, 6.20, 1.11, 1.14)
        x0, x1 = sorted((str_ * 1.27, str_ * 1.30)); kvadr(M["ram"], x0, x1, 3.60, 6.20, 1.00, 1.14)
    print("cisterna: y", Y0T, "az", Y1T, "dno z 1.30 vrch z", round(ZV, 2))

# naklad na ukazku: kupa jako u vejtrasky (render_v3s.py kupka), korba S1 namerena paprsky (rez.py):
# podlaha z 1,46 (u bocnic zaoblena nahoru, vzadu od y 5,9 stoupa na 1,66), bocnice x +-1,13, nahore z 2,39 az 2,61,
# predni celo y 2,75, zadni celo y 6,75 nahore z 2,59.
KUPA = os.environ.get("KUPA")
NAKLAD = {"GRVL": ((112, 109, 105), (172, 167, 160), 0.85, 1.2, 24), "SAND": ((184, 148, 88), (226, 196, 132), 0.95, 0.7, 14),
          "COAL": ((16, 16, 18), (58, 58, 62), 0.45, 1.3, 26)}
if KUPA:
    import bmesh, random
    tm, sv, drs, hrubost, mer = NAKLAD[KUPA]
    mk = bpy.data.materials.new("kupa"); mk.use_nodes = True
    n_ = mk.node_tree.nodes; l_ = mk.node_tree.links; bs = n_["Principled BSDF"]
    sum_ = n_.new("ShaderNodeTexNoise"); sum_.inputs["Scale"].default_value = mer; sum_.inputs["Detail"].default_value = 6.0
    ra = n_.new("ShaderNodeValToRGB"); ra.color_ramp.elements[0].color = srgb(tm); ra.color_ramp.elements[1].color = srgb(sv)
    l_.new(sum_.outputs["Fac"], ra.inputs["Fac"]); l_.new(ra.outputs["Color"], bs.inputs["Base Color"]); bs.inputs["Roughness"].default_value = drs
    # hrac 29. 9.: "kupicku vetsi o 20 % na vysku, celou kupicku vys". Kupa ted korbu vyplni az tesne pod okraj bocnic
    # (DNO_KUPY, okraj kupy je schovany za bocnicemi a celem) a nad bocnice kouka o 20 % vys a cela o 0,2 m vys nez
    # na prvnim nahledu: vrchol 2,83 -> 3,07 m. Kdyz byla kupa na podlaze a jen vysoka, vypadala v korbe jako vejce.
    KX, KY0, KY1 = 1.135, 2.77, 6.73
    DNO_KUPY = float(os.environ.get("DNO_KUPY", "2.28")); VRCH_KUPY = float(os.environ.get("VRCH_KUPY", "3.07"))
    random.seed(7); B = (KY1 - KY0) / 2; YS = (KY0 + KY1) / 2
    bm = bmesh.new(); NX, NY = 40, 80; vrch = {}
    hr = [[random.uniform(-1, 1) for _ in range(NY // 4 + 2)] for _ in range(NX // 4 + 2)]
    for i in range(NX + 1):
        for j in range(NY + 1):
            x = -KX + 2 * KX * i / NX; y = YS - B + 2 * B * j / NY
            sk = max(0.0, 1 - (abs(x) / KX) ** 2.2 - (abs(y - YS) / B) ** 2.2)
            hrudka = hr[i // 4][j // 4] * 0.035 * max(0.0, hrubost - 0.7) * sk
            z = DNO_KUPY + (VRCH_KUPY - DNO_KUPY) * sk ** 0.6 + (random.uniform(-0.04, 0.04) * sk * hrubost if sk > 0 else 0) + hrudka - 0.02
            vrch[i, j] = bm.verts.new((x, y, z))
    for i in range(NX):
        for j in range(NY):
            bm.faces.new((vrch[i, j], vrch[i + 1, j], vrch[i + 1, j + 1], vrch[i, j + 1]))
    me = bpy.data.meshes.new("kupa"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    ob = bpy.data.objects.new("kupa", me); scene.collection.objects.link(ob); ob.data.materials.append(mk)
    ob.parent = koren; ob.matrix_parent_inverse = koren.matrix_world.inverted()

meshe = [o for o in scene.objects if o.type == 'MESH' and not o.hide_render]
pts = [o.matrix_world @ v.co for o in meshe for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "delka", round(mx.y - mn.y, 2))
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
koren.parent = gramofon; koren.matrix_parent_inverse = gramofon.matrix_world.inverted()
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon
if SVETLO == "slunce":
    # odkud sviti: zleva (z pohledu kamery) a shora, trochu zezadu, at jsou boky kapoty a korby do kamery tmavsi.
    # Vyzkouseno 29. 9. (okoli 0,75/0,5/0,45/0,35, slunce 3/4/4,5/5): nejlip vynikne zaobleni kapoty pri 0,35 a 5.
    ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
    odkud = (vlevo * 1.0 + ke_kamere * float(os.environ.get("ZEPREDU", "-0.25")) + Vector((0, 0, float(os.environ.get("SHORA", "1.0"))))).normalized()
    bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
    sl.data.energy = float(os.environ.get("SLUNCE", "5.0")); sl.data.angle = math.radians(6)
    sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, flush=True)
print("hotovo")
