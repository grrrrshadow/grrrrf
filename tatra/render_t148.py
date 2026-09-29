# -*- coding: utf-8 -*-
# Foceni Tatry 148 (hans1240, "Tatra-148-AKT-3-3", CC BY 4.0) pro OpenTTD, stejne jako vejtraska (v3s/render_v3s.py):
# ortho kamera 30 stupnu nad obzorem, azimut 45 stupnu, HDRI snow.exr, 8 smeru ve stejnem meritku.
# Hrac 29. 9.: "hans1240 berem na tekutiny", "zkus jednu od Hanse, jak bude vypadat".
#   python3 render_t148.py <nater> <px_na_m> <vystup>        nater: oranzova (T148), cervena (T138)
# Model nema barvy ani textury (materialy bile a sede), barvy se davaji podle jmen materialu (BARVY).
import bpy, os, sys, math, json
from mathutils import Vector

TU = os.path.dirname(os.path.abspath(__file__))
NATER, PX_M, VYSTUP = sys.argv[-3], float(sys.argv[-2]), sys.argv[-1]
MODEL = os.environ.get("MODEL", os.path.join(TU, "model", "tatra-148-akt-3-3.glb"))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
RAM = 256
SAMPLES = int(os.environ.get("SAMPLES", "256"))
SMERY = [int(s) for s in os.environ.get("SMERY", "0,1,2,3,4,5,6,7").split(",")]
# jako u vejtrasky: uhly z render_sergej.py pocitaji s celem na -Y, Tatra ma kabinu na +Y, proto +180
ROTATION_ANGLES = [(u + 180.0) % 360 for u in (225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0)]

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

pred = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=MODEL)
nove = list(set(scene.objects) - pred)
koreny = [o for o in nove if o.parent is None]
meshe = [o for o in nove if o.type == 'MESH']

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

# ---------------------------------------------------------------- barvy podle materialu
# Materialy modelu (jmeno bez cisla na konci po teckce se nebere, kazdy ma svoje): bile plechy kabiny, dveri,
# cisterny a naraznik v barve nateru; sede kovove dily tmave sede; ram cerny; svetla podle barvy v modelu.
# hrac 29. 9.: "majaky pryc, zadna vojenska, oranzovy tatrovacky 148 a cerveny komunisticka cervena 138"
NATERY = {"oranzova": (224, 104, 24), "cervena": (176, 24, 20)}
LAK = NATERY[NATER]
BARVY = {
    "kabina.2": LAK, "kabina.3": LAK, "kabina.4": LAK, "kabina.9": LAK, "kabina.10": LAK, "kabina.11": LAK,
    "door_rf_ok.5": LAK, "AC.6": LAK, "otboynik.2": LAK, "primochki.1": LAK, "primochki.6": LAK, "wheel_rm.1": LAK,
    "kabina.6": (58, 58, 56), "kabina.7": (36, 36, 36), "kabina.8": (70, 70, 68), "kabina.13": (62, 62, 60),
    "door_rf_ok.4": (60, 60, 58), "AC.5": (66, 66, 62), "primochki.4": (60, 60, 58), "otboynik.3": (46, 46, 44),
    "otboynik.5": (46, 46, 44), "otboynik.6": (46, 46, 44),
    "rama.0": (22, 22, 22), "wheel_rm.2": (26, 26, 26), "primochki.2": (22, 22, 22),   # wheel_rm.2 pneumatiky, .1 disky
    "kabina.12": (150, 150, 146), "right_front_light.001": (150, 150, 146),   # stresni svetla hasicky, nesviti
    "salon.2": (44, 42, 40), "salon.3": (44, 42, 40), "salon.4": (44, 42, 40), "salon.5": (44, 42, 40), "salon.6": (44, 42, 40),
    "primochki.3": (150, 30, 20), "primochki.5": (30, 40, 26),
}
SVITI = {"right_front_light": (255, 255, 250), "left_front_light": (255, 255, 250),
         "right_rear_light": (200, 24, 16)}          # oba reflektory bile
SKRYT = {"kabina.15"}                                # modre majaky (hasicska cisterna), na tekutiny pryc
for m in bpy.data.materials:
    if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes: continue
    b = m.node_tree.nodes["Principled BSDF"]
    if m.name in BARVY:
        b.inputs["Base Color"].default_value = srgb(BARVY[m.name]); b.inputs["Roughness"].default_value = 0.6
    elif m.name in SVITI:
        b.inputs["Base Color"].default_value = srgb(SVITI[m.name])
        b.inputs["Emission Color"].default_value = srgb(SVITI[m.name]); b.inputs["Emission Strength"].default_value = 1.5
    elif m.name == "glass":
        b.inputs["Base Color"].default_value = (0.030, 0.040, 0.055, 1.0); b.inputs["Roughness"].default_value = 0.15
for o in meshe:
    if any(s.material and s.material.name in SKRYT for s in o.material_slots):
        o.hide_render = True
neznama = sorted({s.material.name for o in meshe for s in o.material_slots if s.material} - set(BARVY) - set(SVITI) - SKRYT - {"glass"})
print("materialy bez barvy:", neznama)

# ---------------------------------------------------------------- korba misto cisterny
# Hrac 29. 9.: "cisterna je fakt pro hasice, tam z cisterny nahore kouka takovej hrb. Jak bysme udelali korbu na naklad,
# jak by to vypadalo?" KORBA=cisterna nechava model, valnik a sklapec schovaji cisternu (dily AC_ krome blatniku
# AC_kabina.3, pricniku AC_rama.0 a tazneho zarizeni AC_primochki.4) a postavi korbu z kvadru na ram.
KORBA = os.environ.get("KORBA", "cisterna")
if KORBA != "cisterna":
    for o in meshe:
        if o.name.startswith("AC_") and not o.name.startswith(("AC_kabina.3", "AC_rama.0", "AC_primochki.4")):
            o.hide_render = True
    def mat(jmeno, rgb, drsnost=0.6):
        m = bpy.data.materials.new(jmeno); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = srgb(rgb)
        b.inputs["Roughness"].default_value = drsnost
        return m
    m_lak = mat("korba_lak", LAK); m_tmava = mat("korba_tmava", (40, 40, 38)); m_podlaha = mat("korba_podlaha", (92, 74, 52), 0.85)
    def kvadr(m, x0, x1, y0, y1, z0, z1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        o = bpy.context.object; o.scale = (x1 - x0, y1 - y0, z1 - z0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        b = o.modifiers.new("hrana", 'BEVEL'); b.width = min(0.012, (min(x1 - x0, y1 - y0, z1 - z0)) / 3); b.segments = 2
        o.data.materials.append(m); koreny.append(o); meshe.append(o)
        return o
    # rozmery: kabina konci na y 1,20, ram nahore z 0,11, sirka auta +-1,25
    X, Y0, Y1, Z0 = 1.24, -5.00, 1.05, 0.12
    kvadr(m_tmava, -0.55, 0.55, Y0 + 0.1, Y1 - 0.05, Z0, Z0 + 0.12)             # pomocny ram pod podlahou
    kvadr(m_podlaha, -X, X, Y0, Y1, Z0 + 0.12, Z0 + 0.20)                        # podlaha
    ZP = Z0 + 0.20
    if KORBA == "valnik":
        V = 0.55                                                                  # bocnice valniku
        for s in (-1, 1):
            kvadr(m_lak, s * X - 0.03, s * X + 0.03, Y0, Y1, ZP, ZP + V)
            for k in range(3):                                                    # tri vodorovne prolisy
                z = ZP + 0.10 + k * 0.17
                kvadr(m_tmava, s * (X + 0.03) - 0.01, s * (X + 0.03) + 0.01, Y0 + 0.05, Y1 - 0.05, z, z + 0.03)
            for y in (Y0 + 2.0, Y0 + 4.0):                                        # svisle zamky mezi dily bocnice
                kvadr(m_tmava, s * (X + 0.03) - 0.015, s * (X + 0.03) + 0.015, y - 0.04, y + 0.04, ZP, ZP + V)
        kvadr(m_lak, -X, X, Y0 - 0.03, Y0 + 0.03, ZP, ZP + V)                     # zadni celo
        kvadr(m_lak, -X, X, Y1 - 0.03, Y1 + 0.03, ZP, ZP + 1.05)                  # predni celo, vyssi, chrani kabinu
        for x in (-0.8, -0.27, 0.27, 0.8):                                        # mrizka nad prednim celem
            kvadr(m_tmava, x - 0.02, x + 0.02, Y1 - 0.02, Y1 + 0.02, ZP + 1.05, ZP + 1.30)
        kvadr(m_tmava, -X, X, Y1 - 0.02, Y1 + 0.02, ZP + 1.28, ZP + 1.32)
    elif KORBA == "sklapec":
        V = 1.00                                                                  # vysoke ocelove bocnice S1
        for s in (-1, 1):
            kvadr(m_lak, s * X - 0.03, s * X + 0.03, Y0, Y1, ZP, ZP + V)
            kvadr(m_lak, s * (X + 0.02) - 0.03, s * (X + 0.02) + 0.03, Y0, Y1, ZP + V - 0.08, ZP + V)   # horni lem
            y = Y0 + 0.25
            while y < Y1 - 0.2:                                                   # svisla zebra
                kvadr(m_lak, s * (X + 0.05) - 0.025, s * (X + 0.05) + 0.025, y - 0.04, y + 0.04, ZP, ZP + V - 0.08)
                y += 0.62
        kvadr(m_lak, -X, X, Y0 - 0.03, Y0 + 0.03, ZP, ZP + V)                     # zadni celo
        kvadr(m_lak, -X, X, Y1 - 0.03, Y1 + 0.03, ZP, ZP + V + 0.35)              # predni celo
        kvadr(m_lak, -X, X, Y1 - 0.03, Y1 + 0.75, ZP + V + 0.30, ZP + V + 0.36)   # stitek nad kabinou
    print("korba", KORBA, "podlaha z", round(ZP, 2), "y", Y0, "az", Y1)

pts = [o.matrix_world @ v.co for o in meshe if not o.hide_render for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
stred = (mn + mx) / 2
print("model", tuple(round(c, 3) for c in mn), tuple(round(c, 3) for c in mx), "delka", round(mx.y - mn.y, 2))

bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); gramofon = bpy.context.object
for k in koreny:
    k.parent = gramofon; k.matrix_parent_inverse = gramofon.matrix_world.inverted()
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
