# -*- coding: utf-8 -*-
# Foceni M62 "Sergej" pro OpenTTD. Odvozeno z hracova glb3BBC.py (24. 1. 2026):
# stejna kamera (ortho, 30 stupnu nad obzorem, 45 stupnu azimut), stejne HDRI snow.exr
# bez stinu, stejny Cycles a stejne uhly otoceni. Pridano:
#   - meritko v px na metr misto ortho_scale (CZTR ma ~12,2 px/m v zin4)
#   - stlaceni podel osy na rovne koleji (smery 1,3,5,7): hra tam stavi vozidla
#     hustsi nez na sikme koleji (8 px na osminu proti 16 px), CZTR to dela stejne
#   - barevny pruchod: ktery pixel patri hlave, stredu a zadi (lokomotiva je 3 clanky)
#   - kotva (bod na koleji pod stredem lokomotivy) spoctena promitnutim, ne odhadem
#   - ZIN=8: obrazky 8x (zin8) pro nasi hru, dvojnasobne px/m i ram, zbytek stejny; do GRF jdou k 4x
#   - natier rzd: textury РЖД z par8 (nater.rzd), SMERY=1,3 vyfoti jen nektere smery (zkousky)
#   - rez (od v9 jen CSD, REZ=0 bez ni, REZ_LADENI=<maska> ukaze masku zelene misto barvy)
# Spousti se:  [ZIN=8] python3 render_sergej.py <natier: zeleny|cerveny|rzd> <px_na_m (4x)> <osmin: 12|14> <vystup>
import bpy, os, sys, math, json
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import nater

ZIN = int(os.environ.get("ZIN", "4"))
NATER, PX_M, OSMIN, VYSTUP = sys.argv[-4], float(sys.argv[-3]) * ZIN / 4, int(sys.argv[-2]), sys.argv[-1]
SMERY = [int(s) for s in os.environ.get("SMERY", "").split(",") if s]
MODEL = os.path.join(TU, "model", "diesel_locomotive_m62.glb")
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = 320 * ZIN // 4              # ctverec rendru v px (zin4: 320); lokomotiva se do nej vejde v obou meritkach
SAMPLES = int(os.environ.get("SAMPLES", "256"))
# poradi smeru jako vycet Direction ve hre: N, NE, E, SE, S, SW, W, NW, a 8 = obrazek do nakupu (W)
ROTATION_ANGLES = [225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0, 315.0]
ROVNE = (1, 3, 5, 7)              # smery po rovne koleji (na obrazovce sikmo)
STLACENI = 1 / math.sqrt(2)       # na rovne koleji je osmina 8 px vodorovne, na sikme 16 px
KROK = {0: (0, -8), 1: (8, -4), 2: (16, 0), 3: (8, 4), 4: (0, 8), 5: (-8, 4), 6: (-16, 0), 7: (-8, -4)}

os.makedirs(VYSTUP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = False
scene.cycles.samples = SAMPLES
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
scene.world.cycles_visibility.shadow = False       # jako v glb3BBC.py: bez stinu z HDRI

pred = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=MODEL)
nove = list(set(scene.objects) - pred)
koren = [o for o in nove if o.parent is None][0]
meshe = [o for o in [koren] + list(koren.children_recursive) if o.type == 'MESH']
pts = [o.matrix_world @ v.co for o in meshe for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
DELKA = mx.y - mn.y                                   # model lezi podel osy Y
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "delka", round(DELKA, 3))

PREBARVIT = {"zeleny": None, "cerveny": nater.cerveny, "rzd": nater.rzd}[NATER]
if PREBARVIT:
    for img in bpy.data.images:
        if img.name.startswith("Image_"):
            w, h = img.size
            px = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(px)
            px = px.reshape(h, w, 4)
            # Blender ma obrazky odspodu nahoru, nater pocita s radky shora
            rgb = (np.flipud(px[..., :3]) * 255 + 0.5).astype(np.uint8)
            nove = PREBARVIT(img.name, rgb)
            if nove is None: continue
            px[..., :3] = np.flipud(nove).astype(np.float32) / 255
            img.pixels.foreach_set(px.ravel()); img.update()
            print("prebarveno", img.name, (w, h))

# gramofon (otaceni) -> natahovac (stlaceni podel osy modelu) -> model
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); natah = bpy.context.object
natah.parent = gramofon; natah.matrix_parent_inverse = gramofon.matrix_world.inverted()
koren.parent = natah; koren.matrix_parent_inverse = natah.matrix_world.inverted()
# ---------------------------------------------------------------- rez
# Hrac 2. 10.: "strechu sergeje udelame rezatou a podvozek taky, kola vsechno co je sedy dole bude taky rezaty ale ne jako
# strecha. dole tmavsi rez, od oleje, spinavy", "rez kde je sedy, na podvozek tmavy spinavy rez". V kazdem materialu se pred
# Base Color vlozi michani s rezi, rozhoduje vyska a sedost (nizka sytost barvy): strecha = sede plochy nad horni hranou
# boku (3,5 m, boky tela jsou 1,6 az 3,47 m) a v texture tela cela oblast strechy (radky 0-383 z 2048); podvozek = sede
# plochy pod spodni hranou boku (1,55 m): kola, podvozky, ram, nadrz, skrine, spojka. Lak (zelena, cervena, pruhy, sedy pas
# RZD na boku) se nemeni. Souradnice v prostoru natahovace (puvodni metry modelu od stredu), takze rez je u vsech smeru
# na stejnem miste. REZ=0 bez rzi.
# Od v9 (hrac 3. 10.): rez jen na CSD ("mezinarodni a masu jsi nemel delat rezate ... nech jak byly"), a strecha jen lehce
# jako stopy po vode: "pruhy na strese od boku k boku s epicentrem na vrchu strechy", "ten cernej velkej flek to muze byt
# rezaty a cary koroze z toho", vzor CZTR 810 Unifik Rez. Podvozek CSD zustava tmavy olejovy jako ve v8.
REZ = os.environ.get("REZ", "1") == "1" and NATER == "cerveny"
VYFUK_Y, VYFUK_X = (-2.96, -2.74), 0.46        # cerna skvrna na strese (otvor vyfuku), metry od stredu modelu
POL_SIRKY = 1.48                                # pul sirky strechy
Z_STRECHA, Z_PODVOZEK = 3.50, 1.55
BEZ_REZU = {"phong3", "phong4", "phong5", "phong9", "phong12"}   # kabina a strojovna za okny, sklo, zaluzie
TELO = {"phong1", "phong10"}                                       # textura tela (Image_0): strecha i podle radku textury

def zrezivet(mat):
    nt = mat.node_tree; N = nt.nodes; Lk = nt.links
    bsdf = [n for n in N if n.type == 'BSDF_PRINCIPLED'][0]
    def soket(vstup):
        if vstup.is_linked: return vstup.links[0].from_socket
        v = N.new("ShaderNodeValue") if not hasattr(vstup.default_value, "__len__") else N.new("ShaderNodeRGB")
        v.outputs[0].default_value = vstup.default_value
        return v.outputs[0]
    def mapa(vstup, a, b, c, d):
        m = N.new("ShaderNodeMapRange"); m.interpolation_type = 'SMOOTHSTEP'; m.clamp = True
        Lk.new(vstup, m.inputs["Value"])
        for jm, v in (("From Min", a), ("From Max", b), ("To Min", c), ("To Max", d)): m.inputs[jm].default_value = v
        return m.outputs["Result"]
    def mat_(op, a, b=None, hodnota=None):
        m = N.new("ShaderNodeMath"); m.operation = op; m.use_clamp = op in ('MULTIPLY', 'ADD', 'MAXIMUM')
        Lk.new(a, m.inputs[0])
        if b is not None: Lk.new(b, m.inputs[1])
        else: m.inputs[1].default_value = hodnota
        return m.outputs[0]
    def sum_(vektor, meritko, detail, posun):
        s = N.new("ShaderNodeTexNoise"); s.inputs["Scale"].default_value = meritko; s.inputs["Detail"].default_value = detail
        s.inputs["Roughness"].default_value = 0.62
        p = N.new("ShaderNodeVectorMath"); p.operation = 'ADD'; p.inputs[1].default_value = posun
        Lk.new(vektor, p.inputs[0]); Lk.new(p.outputs[0], s.inputs["Vector"])
        return s.outputs["Fac"]
    def rampa(fac, body):
        r = N.new("ShaderNodeValToRGB"); cr = r.color_ramp
        for i, (poz, c) in enumerate(body):
            e = cr.elements[i] if i < 2 else cr.elements.new(poz)
            e.position = poz; e.color = tuple((v / 255) ** 2.2 for v in c) + (1.0,)
        Lk.new(fac, r.inputs["Fac"])
        return r.outputs["Color"]
    barva = soket(bsdf.inputs["Base Color"])
    tc = N.new("ShaderNodeTexCoord"); tc.object = natah
    xyz = N.new("ShaderNodeSeparateXYZ"); Lk.new(tc.outputs["Object"], xyz.inputs[0])
    z = xyz.outputs["Z"]; zs = stred.z
    hsv = N.new("ShaderNodeSeparateColor"); hsv.mode = 'HSV'; Lk.new(barva, hsv.inputs[0])
    sedost = mapa(hsv.outputs[1], 0.16, 0.30, 1.0, 0.0)
    nad = mapa(z, Z_STRECHA - zs - 0.02, Z_STRECHA - zs + 0.02, 0.0, 1.0)
    pod = mapa(z, Z_PODVOZEK - zs - 0.03, Z_PODVOZEK - zs + 0.03, 1.0, 0.0)
    if mat.name in TELO:
        uv = N.new("ShaderNodeSeparateXYZ"); Lk.new(tc.outputs["UV"], uv.inputs[0])
        v = uv.outputs["Y"]                                               # Blender: v odspodu, radek shora = 1 - v
        strecha_uv = mapa(v, 1 - 390 / 2048, 1 - 380 / 2048, 0.0, 1.0)   # radky 0-383: strecha
        mimo_cela = mapa(v, 1 - 1540 / 2048, 1 - 1530 / 2048, 0.0, 1.0)  # radky 1536+: cela (okna, svetla) bez rzi
        nad = mat_('MAXIMUM', strecha_uv, mat_('MULTIPLY', nad, mimo_cela))
        pod = mat_('MULTIPLY', pod, mimo_cela)
    strecha = mat_('MULTIPLY', nad, sedost); dole = mat_('MULTIPLY', pod, sedost)
    p = tc.outputs["Object"]
    x = xyz.outputs["X"]; y = xyz.outputs["Y"]
    def vek(meritko, posun):                                          # protazene souradnice pro sum
        m = N.new("ShaderNodeVectorMath"); m.operation = 'MULTIPLY'; m.inputs[1].default_value = meritko; Lk.new(p, m.inputs[0])
        s = N.new("ShaderNodeVectorMath"); s.operation = 'ADD'; s.inputs[1].default_value = posun; Lk.new(m.outputs[0], s.inputs[0])
        return s.outputs[0]
    def sum2(v, detail, zkresleni=0.0):
        s = N.new("ShaderNodeTexNoise"); s.inputs["Scale"].default_value = 1.0; s.inputs["Detail"].default_value = detail
        s.inputs["Roughness"].default_value = 0.6; s.inputs["Distortion"].default_value = zkresleni
        Lk.new(v, s.inputs["Vector"]); return s.outputs["Fac"]
    # strecha (v9): stopy po vode. a = jak daleko od hrebene (0 nahore uprostred, 1 na okraji strechy)
    a = mapa(mat_('ABSOLUTE', x, hodnota=0.0), 0.0, POL_SIRKY, 0.0, 1.0)
    # struzky napric strechou: sum protazeny podel delky (11x hustsi podel Y nez napric), tenke pruhy od hrebene k bokum
    struzka = mapa(sum2(vek((0.25, 4.6, 0.25), (2.3, 0.7, 5.1)), 2.0, 0.3), 0.52, 0.62, 0.0, 1.0)
    # kazda struzka jinak dlouha: dosah od hrebene dolu (podil pul sirky), nahore silnejsi nez dole
    dosah = mapa(sum2(vek((0.0, 2.1, 0.0), (7.7, 3.3, 1.9)), 1.0), 0.35, 0.65, 0.30, 1.05)
    konec = mapa(mat_('SUBTRACT', dosah, a), -0.04, 0.10, 0.0, 1.0)
    vrch = mapa(a, 0.0, 1.0, 1.0, 0.5)
    f_str = mat_('MULTIPLY', mat_('MULTIPLY', struzka, konec), mat_('MULTIPLY', vrch, None, 0.70))
    # na hrebeni, kde voda stoji, lehky nadech rzi v ostruvcich
    hreben = mat_('MULTIPLY', mapa(a, 0.05, 0.40, 1.0, 0.0), mapa(sum2(vek((1.6, 1.3, 1.6), (4.4, 9.9, 2.2)), 3.0), 0.42, 0.68, 0.0, 0.45))
    # cerna skvrna (vyfuk): sama rezava, kolem ni rezavy lem a z ni hustsi struzky az k okrajum strechy
    vy0, vy1 = VYFUK_Y
    dy = mat_('MAXIMUM', mat_('SUBTRACT', mat_('ABSOLUTE', mat_('SUBTRACT', y, None, (vy0 + vy1) / 2), hodnota=0.0), None, (vy1 - vy0) / 2), None, 0.0)
    dx = mat_('MAXIMUM', mat_('SUBTRACT', mat_('ABSOLUTE', x, hodnota=0.0), None, VYFUK_X), None, 0.0)
    vzd = N.new("ShaderNodeVectorMath"); vzd.operation = 'LENGTH'
    kom = N.new("ShaderNodeCombineXYZ"); Lk.new(dx, kom.inputs[0]); Lk.new(dy, kom.inputs[1]); Lk.new(kom.outputs[0], vzd.inputs[0])
    vzd = vzd.outputs["Value"]
    skvrna = mat_('MULTIPLY', mapa(vzd, 0.0, 0.03, 1.0, 0.0), mapa(sum2(vek((6.0, 6.0, 6.0), (1.2, 8.8, 3.4)), 4.0), 0.30, 0.60, 0.55, 0.85))
    lem = mat_('MULTIPLY', mapa(vzd, 0.02, 0.35, 0.6, 0.0), mapa(sum2(vek((4.0, 4.0, 4.0), (6.1, 2.2, 7.3)), 4.0), 0.40, 0.65, 0.0, 1.0))
    pas_vyfuku = mapa(dy, 0.0, 0.55, 1.0, 0.0)                     # u vyfuku struzky hustsi a az dolu
    struzka2 = mapa(sum2(vek((0.25, 4.6, 0.25), (2.3, 0.7, 5.1)), 2.0, 0.3), 0.47, 0.58, 0.0, 1.0)
    f_vyf = mat_('MULTIPLY', mat_('MULTIPLY', struzka2, pas_vyfuku), mapa(a, 0.0, 1.0, 0.75, 0.45))
    rez_celkem = mat_('MAXIMUM', mat_('MAXIMUM', f_str, hreben), mat_('MAXIMUM', mat_('MAXIMUM', skvrna, lem), f_vyf))
    f_s = mat_('MULTIPLY', strecha, rez_celkem)
    LADENI = os.environ.get("REZ_LADENI", "")
    if LADENI:                                                        # ladeni: maska misto barvy (zelena = rez)
        ukaz = {"str": f_str, "hreben": hreben, "skvrna": skvrna, "lem": lem, "vyf": f_vyf, "strecha": strecha, "vse": f_s,
                "struzka": struzka, "konec": konec, "a": a}[LADENI]
        mx_ = N.new("ShaderNodeMix"); mx_.data_type = 'RGBA'; Lk.new(ukaz, mx_.inputs["Factor"])
        mx_.inputs["A"].default_value = (0.05, 0.05, 0.05, 1); mx_.inputs["B"].default_value = (0.0, 1.0, 0.0, 1)
        Lk.new(mx_.outputs["Result"], bsdf.inputs["Base Color"]); return
    # barva rzi: rezave hneda az oranzova, kresba textury (spary, spina) zustava
    rez_s = rampa(sum_(p, 3.0, 6.0, (3.1, 7.7, 1.3)), [(0.30, (96, 50, 28)), (0.50, (132, 70, 36)), (0.68, (158, 88, 44)), (0.85, (120, 74, 48))])
    det_s = N.new("ShaderNodeMath"); det_s.operation = 'MULTIPLY_ADD'; Lk.new(hsv.outputs[2], det_s.inputs[0])
    det_s.inputs[1].default_value = 0.75; det_s.inputs[2].default_value = 0.42
    rez_s_d = N.new("ShaderNodeMix"); rez_s_d.data_type = 'RGBA'; rez_s_d.blend_type = 'MULTIPLY'; rez_s_d.inputs["Factor"].default_value = 1.0
    Lk.new(rez_s, rez_s_d.inputs["A"]); Lk.new(det_s.outputs[0], rez_s_d.inputs["B"])
    # podvozek: tmavy spinavy rez od oleje: skoro cerna hneda, misty rezava, mista vyprahleho prachu
    rez_d = rampa(sum_(p, 2.6, 6.0, (5.3, 1.1, 9.4)), [(0.28, (26, 22, 19)), (0.48, (52, 35, 24)), (0.68, (86, 52, 30)), (0.86, (64, 54, 44))])
    det_d = N.new("ShaderNodeMath"); det_d.operation = 'MULTIPLY_ADD'; Lk.new(hsv.outputs[2], det_d.inputs[0])
    det_d.inputs[1].default_value = 0.6; det_d.inputs[2].default_value = 0.55
    rez_d_d = N.new("ShaderNodeMix"); rez_d_d.data_type = 'RGBA'; rez_d_d.blend_type = 'MULTIPLY'; rez_d_d.inputs["Factor"].default_value = 1.0
    Lk.new(rez_d, rez_d_d.inputs["A"]); Lk.new(det_d.outputs[0], rez_d_d.inputs["B"])
    f_d = mat_('MULTIPLY', dole, None, 0.93)
    m1 = N.new("ShaderNodeMix"); m1.data_type = 'RGBA'; Lk.new(f_s, m1.inputs["Factor"]); Lk.new(barva, m1.inputs["A"]); Lk.new(rez_s_d.outputs["Result"], m1.inputs["B"])
    m2 = N.new("ShaderNodeMix"); m2.data_type = 'RGBA'; Lk.new(f_d, m2.inputs["Factor"]); Lk.new(m1.outputs["Result"], m2.inputs["A"]); Lk.new(rez_d_d.outputs["Result"], m2.inputs["B"])
    Lk.new(m2.outputs["Result"], bsdf.inputs["Base Color"])
    # rez je matny a neni kov
    oba = mat_('ADD', f_s, f_d)
    for jm, cil in (("Roughness", 0.9), ("Metallic", 0.0)):
        zdroj = soket(bsdf.inputs[jm])
        m = N.new("ShaderNodeMix"); m.data_type = 'FLOAT'; Lk.new(oba, m.inputs["Factor"]); Lk.new(zdroj, m.inputs["A"])
        m.inputs["B"].default_value = cil; Lk.new(m.outputs["Result"], bsdf.inputs[jm])

if REZ:
    for mat in {s.material for o in meshe for s in o.material_slots if s.material}:
        if mat.name in BEZ_REZU or not mat.use_nodes: continue
        zrezivet(mat); print("rez", mat.name)

body = {}
for jm, co in (("kotva", (stred.x, stred.y, mn.z)), ("plus", (stred.x, mx.y, mn.z)), ("minus", (stred.x, mn.y, mn.z)),
               ("vrsek", (stred.x, stred.y, mx.z))):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=co); e = bpy.context.object
    e.parent = natah; e.matrix_parent_inverse = natah.matrix_world.inverted(); body[jm] = e

ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon

# material pro barevny pruchod: podle souradnice Y v prostoru natahovace (= puvodni metry modelu)
POLOVINA_STREDU = (DELKA / 2) * (4.0 / (OSMIN / 2.0))      # stredni clanek ma 8 osmin z OSMIN
m = bpy.data.materials.new("vlastnik"); m.use_nodes = True
mt = m.node_tree
for n in list(mt.nodes): mt.nodes.remove(n)
tc = mt.nodes.new('ShaderNodeTexCoord'); tc.object = natah
sep = mt.nodes.new('ShaderNodeSeparateXYZ'); mt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
gt = mt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = POLOVINA_STREDU
lt = mt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = -POLOVINA_STREDU
mt.links.new(sep.outputs['Y'], gt.inputs[0]); mt.links.new(sep.outputs['Y'], lt.inputs[0])
mid = mt.nodes.new('ShaderNodeMath'); mid.operation = 'SUBTRACT'; mid.inputs[0].default_value = 1.0
add = mt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
mt.links.new(gt.outputs[0], add.inputs[0]); mt.links.new(lt.outputs[0], add.inputs[1]); mt.links.new(add.outputs[0], mid.inputs[1])
comb = mt.nodes.new('ShaderNodeCombineColor')
mt.links.new(gt.outputs[0], comb.inputs[0]); mt.links.new(mid.outputs[0], comb.inputs[1]); mt.links.new(lt.outputs[0], comb.inputs[2])
em = mt.nodes.new('ShaderNodeEmission'); mt.links.new(comb.outputs[0], em.inputs['Color'])
out = mt.nodes.new('ShaderNodeOutputMaterial'); mt.links.new(em.outputs[0], out.inputs['Surface'])

def na_pixel(obj):
    bpy.context.view_layer.update()
    p = world_to_camera_view(scene, cam, obj.matrix_world.translation)
    return (p.x * RAM, (1 - p.y) * RAM)

info = {"nater": NATER, "zin": ZIN, "px_m": PX_M, "osmin": OSMIN, "ram": RAM, "delka_m": DELKA, "smery": {}}
for d, uhel in enumerate(ROTATION_ANGLES):
    if SMERY and d not in SMERY: continue
    gramofon.rotation_euler[2] = math.radians(uhel)
    natah.scale = (1, STLACENI, 1) if d in ROVNE else (1, 1, 1)
    bpy.context.view_layer.update()
    kot = na_pixel(body["kotva"]); plus = na_pixel(body["plus"]); minus = na_pixel(body["minus"])
    kx, ky = KROK[d % 8]
    predni = "plus" if (plus[0] - minus[0]) * kx + (plus[1] - minus[1]) * ky > 0 else "minus"
    info["smery"][d] = {"kotva": kot, "plus": plus, "minus": minus, "predni": predni}
    scene.view_layers[0].material_override = None
    scene.cycles.samples = SAMPLES; scene.cycles.filter_width = 1.5
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    if d in ROVNE:
        scene.view_layers[0].material_override = m
        scene.cycles.samples = 1; scene.cycles.filter_width = 0.01
        scene.render.filepath = os.path.join(VYSTUP, f"vlastnik_d{d}.png")
        bpy.ops.render.render(write_still=True)
    print("smer", d, "kotva", [round(v, 1) for v in kot], "predni konec", predni, flush=True)
scene.view_layers[0].material_override = None
json.dump(info, open(os.path.join(VYSTUP, "kotvy.json"), "w"), indent=1)
print("hotovo")
