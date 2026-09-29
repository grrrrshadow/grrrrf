# -*- coding: utf-8 -*-
# Nahled sklapece T148 S1 (hans1240 "Tatra-148", Sketchfab). Jmena dilu (KorbaS1, TG_POLOOSA, TG_T148, PneuP) jsou
# stejna jako v modu Tatry 148 pro Farming Simulator od EmikMODelStudio, takze je to nejspis jeho model.
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
     "blinkr": mat("blinkr", (255, 170, 60), 0.3, 0.0, 0.8), "mrizka": mat("mrizka", (14, 14, 14), 0.8),
     "napis": mat("napis", (200, 16, 16), 0.35)}
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

# Mrizka chladice (hrac 29. 9.: "musime zlepsit chladic mrizku, ted tam neni zadnej"). Model ma na masce jen hladkou
# plochu (predni strana y = -0,48, x +-0,54, z 0,995 az 1,53, stitek na napis z 1,29 az 1,35). Skutecna T148 ma
# 3 sloupce x 6 rad vodorovnych otvoru, dve rady nad napisem TATRA a ctyri pod nim, dole o kus sirsi. Otvory jsou
# o neco vyssi nez ve skutecnosti, aby mrizka byla ve hre videt i v malem.
MRIZKA = os.environ.get("MRIZKA", "148")
if MRIZKA == "148":
    YM, RADY, VOTVOR, MEZ = -0.480, [1.468, 1.402, 1.262, 1.196, 1.130, 1.064], 0.044, 0.028
    for zc in RADY:
        pol = 0.330 + (0.362 - 0.330) * (RADY[0] - zc) / (RADY[0] - RADY[-1])       # polovina sirky rady
        w = (2 * pol - 2 * MEZ) / 3
        for k in range(3):
            x0 = -pol + k * (w + MEZ)
            kvadr(M["mrizka"], x0, x0 + w, YM - 0.006, YM + 0.004, zc - VOTVOR / 2, zc + VOTVOR / 2)
    bpy.ops.object.text_add(location=(0, YM - 0.004, 1.320), rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = "TATRA"; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
    t.data.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    t.data.size = 0.080; t.data.extrude = 0.002; t.data.materials.append(M["napis"])
    t.parent = koren; t.matrix_parent_inverse = koren.matrix_world.inverted()

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

meshe = [o for o in scene.objects if o.type == 'MESH']
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
