# -*- coding: utf-8 -*-
# Foceni Skody 1203 (TAZ) valniku s plachtou pro OpenTTD. Model "Škoda 1203 ROL valník 1975" od Jiriho Novaka
# (Printables 1620425, CC0, release par9 zip8/skoda-1203-valnik-1975.stl): jeden kus pro 3D tisk bez barev, plachta
# je v nem. Barvy se davaji po plochach podle polohy (kabina, plachta, bocnice, podvozek, kola, svetla), okna jsou
# v modelu otevrena, sklo je konvexni obal kabiny nad parapetem o kousek zanoreny (jen celni, bocni a rohy).
# Kamera, HDRI a Cycles jako render_rto.py (ortho, 30 stupnu nad obzorem, snow.exr bez stinu, 8 smeru).
# Foti rovnou 8x (do GRF jde jen zin8, 4x a mensi si hra dopocita):
#   [SMERY=1,6] [RAM=512] [SAMPLES=256] [NAHLED=1] python3 render_1203.py <px_na_m v 8x> <vystup>
# Vystup: d0-d7.png (smery jako vycet Direction: N, NE, E, SE, S, SW, W, NW) a kotvy.json s promitnutym bodem na zemi
# pod stredem auta a pod stredem rozvoru. NAHLED=1 vyfoti misto smeru 4 pohledy s ploskymi barvami trid (kontrola).
import bpy, bmesh, os, sys, math, json
import numpy as np
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

TU = os.path.dirname(os.path.abspath(__file__))
PX_M, VYSTUP = float(sys.argv[-2]), sys.argv[-1]
STL = os.environ.get("STL", os.path.join(TU, "model", "skoda-1203-valnik-1975.stl"))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = int(os.environ.get("RAM", "512"))
SAMPLES = int(os.environ.get("SAMPLES", "256"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
NAHLED = os.environ.get("NAHLED", "0") == "1"
# uhly z render_sergej.py pocitaji s celem modelu na -Y; auto ma celo na +Y (po otoceni o 180), proto +180 jako V3S
ROTATION_ANGLES = [(u + 180.0) % 360 for u in (225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0)]
KROK = {0: (0, -8), 1: (8, -4), 2: (16, 0), 3: (8, 4), 4: (0, 8), 5: (-8, 4), 6: (-16, 0), 7: (-8, -4)}

# ---------------------------------------------------------------- rozmery modelu (jednotky STL, celo na -Y, z nahoru)
ROZVOR_M = 2.40                                   # Skoda 1203: rozvor 2 400 mm
KOLA_Y, KOLO_Z = (-26.75, 23.10), -18.45          # stredy kol (bocni pohled), zem z = -25.56
R_PNEU, R_DISK, R_POKLICE = 7.4, 4.6, 2.45        # pneumatika do 7,1 (+ rezerva), disk, chromova poklice
Y_KABINA = -16.0                                  # za timhle je korba (zadni stena kabiny -16,6, plachta -15,5)
Z_BOCNICE = (-8.6, -2.75)                         # bocnice korby; nad nimi plachta, pod nimi podvozek
Z_PLACHTA_NAD_KABINOU = 15.75                     # strecha kabiny 15,6, cela plachty nad ni do y -16,8


def srgb(c, a=1.0):
    return tuple((v / 255) ** 2.2 for v in c) + (a,)


def material(jm, rgb, drsnost=0.45, kov=0.0):
    m = bpy.data.materials.new(jm); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(rgb)
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    m.diffuse_color = srgb(rgb)                   # pro nahled ve Workbench
    return m


# tridy ploch: (jmeno, barva sRGB, drsnost, kov)
TRIDY = [
    ("lak", (206, 86, 80), 0.38, 0.0),            # TAZ cervena, vyjde jako stara plachta z VW T1 (178,87,81)
    ("plachta", (184, 172, 60), 0.92, 0.0),        # horcicova, vyjde jako stara plachta (167,152,57)
    ("podvozek", (40, 38, 36), 0.80, 0.0),
    ("cerna", (22, 22, 22), 0.50, 0.0),           # narazniky, zrcatka, sterace, tesneni
    ("pneu", (28, 28, 28), 0.90, 0.0),
    ("disk", (214, 214, 208), 0.45, 0.0),         # bile disky jako u stare plachty
    ("chrom", (205, 205, 205), 0.18, 1.0),
    ("sklo_svetla", (232, 232, 222), 0.10, 0.0),
    ("oranzova", (232, 122, 24), 0.30, 0.0),
    ("mriz", (30, 30, 30), 0.60, 0.0),
    ("zadni_svetla", (176, 22, 20), 0.30, 0.0),
    ("sklo", (18, 22, 27), 0.04, 0.0),
]
I = {t[0]: k for k, t in enumerate(TRIDY)}


def tridy_ploch(c, zrcatka):
    """trida kazde plochy podle stredu plochy c (jednotky STL)"""
    x, y, z = c[:, 0], c[:, 1], c[:, 2]
    ax = np.abs(x)
    T = np.full(len(c), I["lak"], np.int32)
    plachta = ((y > Y_KABINA) & (z > Z_BOCNICE[1])) | ((y > -17.6) & (z > Z_PLACHTA_NAD_KABINOU))
    korba = (y > Y_KABINA) & ~plachta
    kabina = ~plachta & ~korba
    T[plachta] = I["plachta"]
    T[korba & (z <= Z_BOCNICE[0])] = I["podvozek"]
    T[kabina & (z < -15.6)] = I["podvozek"]
    T[kabina & (y < -43.0) & (z < -13.3) & (z > -18.8)] = I["cerna"]                  # predni naraznik
    celo = kabina & (y < -46.5)
    T[celo & (ax < 9.3) & (z > -10.6) & (z < -5.4)] = I["mriz"]
    for sx in (-1, 1):
        d = np.hypot(x - sx * 12.1, z + 7.9)
        T[celo & (d < 2.55)] = I["chrom"]
        T[celo & (d < 2.0)] = I["sklo_svetla"]
        T[celo & (np.hypot(x - sx * 15.1, z + 12.6) < 0.9)] = I["oranzova"]
    # sterace a tesneni celniho skla: tesne pred sklonenou rovinou celniho skla
    yws = -44.8 + (z - 4.0) * (5.3 / 10.5)
    T[kabina & (ax < 16.5) & (z > 3.6) & (z < 14.9) & (y < yws + 0.8) & (y > yws - 1.5)] = I["cerna"]
    T[(y > 44.0) & (ax > 11.5) & (ax < 18.5) & (z > -13.8) & (z < -11.2)] = I["zadni_svetla"]
    T[zrcatka] = I["cerna"]
    for yc in KOLA_Y:                                                                  # kola nakonec, prebiji vse
        r = np.hypot(y - yc, z - KOLO_Z)
        w = (ax > 11.5) & (ax < 17.8) & (r < R_PNEU)
        T[w] = I["pneu"]; T[w & (r < R_DISK)] = I["disk"]; T[w & (r < R_POKLICE)] = I["chrom"]
    return T


def postav(scene):
    bpy.ops.wm.stl_import(filepath=STL)
    o = bpy.context.selected_objects[0]; o.name = "skoda1203"; me = o.data
    nv, nf = len(me.vertices), len(me.polygons)
    co = np.empty(nv * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    tri = np.empty(nf * 3, np.int32); me.polygons.foreach_get("vertices", tri); tri = tri.reshape(-1, 3)
    # souvisle kusy: hlavni kus a dve zrcatka (union-find pres hrany, vektorove)
    a = np.concatenate([tri[:, 0], tri[:, 1]]); b = np.concatenate([tri[:, 1], tri[:, 2]])
    lab = np.arange(nv)
    for _ in range(400):
        m = np.minimum(lab[a], lab[b]); nl = lab.copy()
        np.minimum.at(nl, a, m); np.minimum.at(nl, b, m); nl = nl[nl]
        if (nl == lab).all(): break
        lab = nl
    u, cnt = np.unique(lab, return_counts=True)
    hlavni = u[np.argmax(cnt)]
    zrcatka_v = lab != hlavni
    zrcatka_f = zrcatka_v[tri[:, 0]]
    print("kusu", len(u), "zrcatka ploch", int(zrcatka_f.sum()), flush=True)
    stredy = co[tri].mean(axis=1)
    T = tridy_ploch(stredy, zrcatka_f)
    for jm, rgb, dr, kov in TRIDY:
        me.materials.append(material(jm, rgb, dr, kov))
    me.polygons.foreach_set("material_index", T)
    me.update()
    print("plochy podle trid:", {TRIDY[k][0]: int((T == k).sum()) for k in range(len(TRIDY))}, flush=True)

    # sklo: konvexni obal kabiny nad parapetem bez zrcatek, bez vnitrku celniho skla (sterace) a bez strechy
    yws = -44.8 + (co[:, 2] - 4.0) * (5.3 / 10.5)
    vnitrek_cela = (np.abs(co[:, 0]) < 15.0) & (co[:, 2] > 4.6) & (co[:, 2] < 13.9) & (co[:, 1] < yws + 2.0)
    sel = (~zrcatka_v) & (co[:, 1] < -16.8) & (co[:, 2] > 2.8) & (co[:, 2] < 15.8) & (np.abs(co[:, 0]) < 20.0) & ~vnitrek_cela
    bm = bmesh.new()
    for p in co[sel]: bm.verts.new(p)
    res = bmesh.ops.convex_hull(bm, input=bm.verts)
    for g in res["geom_interior"] + res["geom_unused"]:
        if isinstance(g, bmesh.types.BMVert) and g.is_valid and not g.link_faces: bm.verts.remove(g)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    pryc = [f for f in bm.faces if f.normal.z > 0.6 or f.normal.z < -0.6 or f.normal.y > 0.5]
    bmesh.ops.delete(bm, geom=pryc, context='FACES')
    bm.normal_update()
    for v in bm.verts: v.co -= v.normal * 0.12
    sme = bpy.data.meshes.new("sklo"); bm.to_mesh(sme); bm.free()
    sklo = bpy.data.objects.new("sklo", sme); scene.collection.objects.link(sklo)
    sme.materials.append(me.materials[I["sklo"]])
    sklo.parent = o
    print("sklo ploch", len(sme.polygons), flush=True)

    # do metru: celo na +Y (otoceni o 180), zem z = 0, stred delky y = 0
    s = ROZVOR_M / (KOLA_Y[1] - KOLA_Y[0])
    mn, mx = co.min(0), co.max(0)
    c0 = Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]))
    o.matrix_world = Matrix.Rotation(math.pi, 4, 'Z') @ Matrix.Scale(s, 4) @ Matrix.Translation(-c0)
    model = {"sirka": float(mx[0] - mn[0]) * s, "delka": float(mx[1] - mn[1]) * s, "vyska": float(mx[2] - mn[2]) * s,
             "napravy": [float(-(yk - c0.y) * s) for yk in KOLA_Y], "meritko_m_na_jednotku": s}
    model["celo"], model["zad"] = model["delka"] / 2, -model["delka"] / 2
    return [o, sklo], model


os.makedirs(VYSTUP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
objs, model = postav(scene)
mn = Vector((-model["sirka"] / 2, model["zad"], 0.0)); mx = Vector((model["sirka"] / 2, model["celo"], model["vyska"]))
stred = (mn + mx) / 2
stred_rozvoru = sum(model["napravy"]) / len(model["napravy"])
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "napravy", [round(n, 3) for n in model["napravy"]],
      "stred delky", round(stred.y, 3), "stred rozvoru", round(stred_rozvoru, 3), flush=True)

if NAHLED:
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'; scene.display.shading.color_type = 'MATERIAL'
    scene.display.shading.show_cavity = True
    scene.render.resolution_x, scene.render.resolution_y = 1200, 800
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scene.collection.objects.link(cam); scene.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 6.2
    for jm, (az, el) in {"bok": (90, 0), "sikmo_predek": (35, 25), "sikmo_zad": (215, 25), "predek": (0, 5)}.items():
        a, e = math.radians(az), math.radians(el)
        d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
        cam.location = stred + d * 30
        fwd = -d; right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
        cam.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
        scene.render.filepath = os.path.join(VYSTUP, f"nahled_{jm}.png")
        bpy.ops.render.render(write_still=True)
    sys.exit(0)

scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = False
scene.cycles.samples = SAMPLES
scene.cycles.filter_width = 1.5
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
scene.world.cycles_visibility.shadow = False

bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
for o in list(scene.objects):
    if o is gramofon or o.parent is not None: continue
    o.parent = gramofon; o.matrix_parent_inverse = gramofon.matrix_world.inverted()
body = {}
for jm, c in (("zem_stred", (stred.x, stred.y, mn.z)), ("zem_rozvor", (stred.x, stred_rozvoru, mn.z)),
              ("celo", (stred.x, mx.y, mn.z)), ("zad", (stred.x, mn.y, mn.z))):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=c); e = bpy.context.object
    e.parent = gramofon; e.matrix_parent_inverse = gramofon.matrix_world.inverted(); body[jm] = e

ax_ = math.radians(90 - 30.0); az_ = math.radians(45.0); DIST = 30.0
cam_pos = (stred.x + DIST * math.sin(ax_) * math.sin(az_), stred.y - DIST * math.sin(ax_) * math.cos(az_), stred.z + DIST * math.cos(ax_))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = gramofon


def na_pixel(obj):
    bpy.context.view_layer.update()
    p = world_to_camera_view(scene, cam, obj.matrix_world.translation)
    return (p.x * RAM, (1 - p.y) * RAM)


info = {"zin": 8, "px_m": PX_M, "ram": RAM, "delka_m": mx.y - mn.y, "sirka_m": model["sirka"], "vyska_m": model["vyska"],
        "stred_delky_y": stred.y, "stred_rozvoru_y": stred_rozvoru, "napravy_y": model["napravy"],
        "meritko_m_na_jednotku": model["meritko_m_na_jednotku"], "smery": {}}
for d in SMERY:
    gramofon.rotation_euler[2] = math.radians(ROTATION_ANGLES[d])
    bpy.context.view_layer.update()
    b = {jm: na_pixel(e) for jm, e in body.items()}
    kx, ky = KROK[d]
    dopredu = (b["celo"][0] - b["zad"][0]) * kx + (b["celo"][1] - b["zad"][1]) * ky
    assert dopredu > 0, f"smer {d}: celo nemiri po smeru jizdy"
    info["smery"][d] = b
    scene.render.filepath = os.path.join(VYSTUP, f"d{d}.png")
    bpy.ops.render.render(write_still=True)
    print("smer", d, "zem pod stredem", [round(v, 2) for v in b["zem_stred"]], flush=True)
json.dump(info, open(os.path.join(VYSTUP, "kotvy.json"), "w"), indent=1)
print("hotovo")
