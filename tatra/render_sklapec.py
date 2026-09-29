# -*- coding: utf-8 -*-
# Nahled sklapece T148 S1 (hans1240 "Tatra-148", Sketchfab). Jmena dilu (KorbaS1, TG_POLOOSA, TG_T148, PneuP) jsou
# stejna jako v modu Tatry 148 pro Farming Simulator od EmikMODelStudio, takze je to nejspis jeho model.
# Jen na ukazku hraci, do GRF az se svolenim autora. Kamera, HDRI a smery jako vejtraska (render_v3s.py).
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
scene.world.cycles_visibility.shadow = False

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
     "blinkr": mat("blinkr", (255, 170, 60), 0.3, 0.0, 0.8)}
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

# naklad na ukazku: kupa jako u vejtrasky (render_v3s.py kupka), korba S1 namerena paprsky (rez.py):
# podlaha z 1,46 (u bocnic zaoblena nahoru, vzadu od y 5,9 stoupa na 1,66), bocnice x +-1,13, nahore z 2,39 az 2,61,
# predni celo y 2,75. Okraj kupy drzet nad podlahou, jinak vykukuje pod korbou.
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
    PODLAHA, KX, KY0, KY1, VYSKA = 1.46, 1.08, 2.85, 6.60, 1.30
    random.seed(7); B = (KY1 - KY0) / 2; YS = (KY0 + KY1) / 2
    bm = bmesh.new(); NX, NY = 40, 80; vrch = {}
    hr = [[random.uniform(-1, 1) for _ in range(NY // 4 + 2)] for _ in range(NX // 4 + 2)]
    for i in range(NX + 1):
        for j in range(NY + 1):
            x = -KX + 2 * KX * i / NX; y = YS - B + 2 * B * j / NY
            sk = max(0.0, 1 - (abs(x) / KX) ** 2.2 - (abs(y - YS) / B) ** 2.2)
            hrudka = hr[i // 4][j // 4] * 0.035 * max(0.0, hrubost - 0.7) * sk
            z = PODLAHA + 0.07 + max(0.0, y - 5.9) * 0.34 + VYSKA * sk ** 0.6 + (random.uniform(-0.04, 0.04) * sk * hrubost if sk > 0 else 0) + hrudka - 0.02
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
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, flush=True)
print("hotovo")
