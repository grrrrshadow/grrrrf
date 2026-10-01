# -*- coding: utf-8 -*-
# Fotka jedne postavy samotne (pruhledne pozadi, bez stinu) stejnou kamerou a svetlem jako budovy (socha), aby sla
# prilozit na obrazek budovy, zastavky, auta nebo nastupiste. Bod pod chodidly je presne uprostred obrazku a pise se do JSONu.
# Vychozi je bez stinu (hrac 1. 10.: "prikladaci obrazky bys mel fotit fakt uplne bez stinu"), tak jsou divky u aut.
# STIN > 0 prida slaby stin na zem: divky na zastavce jsou s STIN=0.2 (hrac: "neni to videt, na zastavce dobry").
#   python3 fotka_postavy.py <vystup.png>
# Promenne: POSTAVA (jmeno GLB v postavy/), POZA (stoji = jak je v modelu, sedi, ruce_dolu = z pozice T), SMER (stupne, kam se diva: 0 = k
# jihozapadu, 90 = k jihovychodu, jako u lavicek), MERITKO (2 jako budovy), VYSKA (m, skutecna), RAM (px), SAMPLES.
import bpy, os, sys, math, json
import numpy as np
from mathutils import Vector, Matrix
from PIL import Image

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import postavy as P

VYSTUP = sys.argv[-1]
PX_M = 12.2
K = float(os.environ.get("MERITKO", "2"))
RAM = int(os.environ.get("RAM", "160"))
JMENO = os.environ.get("POSTAVA", "character_people_girl_001")
POZA = os.environ.get("POZA", "stoji")
SMER = math.radians(float(os.environ.get("SMER", "90")))
VYSKA = float(os.environ.get("VYSKA", "1.68"))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.use_denoising = False; scene.cycles.samples = int(os.environ.get("SAMPLES", "128"))
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
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.9"))     # svetlo jako u sochy

def kost(arm, zacatek):
    return next(b.name for b in arm.pose.bones if b.name.startswith(zacatek))

def ruce_dolu(arm, meshe):
    """modely v pozici T (galaxia): ruce podel tela, kousek dopredu, lokty mirne pokrcene"""
    for st in ("L", "R"):
        zn = 1 if st == "L" else -1
        P.otoc_kost(arm, kost(arm, f"J_Bip_{st}_UpperArm"), (0, 1, 0), zn * math.radians(76))
        P.otoc_kost(arm, kost(arm, f"J_Bip_{st}_UpperArm"), (1, 0, 0), math.radians(-6))
        P.otoc_kost(arm, kost(arm, f"J_Bip_{st}_LowerArm"), (1, 0, 0), math.radians(-14))

def ruce_dolu_college(arm, meshe):
    """college_girl (pozice T ze snimku akce): ruce podel tela"""
    for st, zn in (("L", 1), ("R", -1)):
        P.otoc_kost(arm, kost(arm, f"Shoulder_{st}_"), (0, 1, 0), zn * math.radians(76))
        P.otoc_kost(arm, kost(arm, f"Shoulder_{st}_"), (1, 0, 0), math.radians(-6))
        P.otoc_kost(arm, kost(arm, f"Elbow_{st}_"), (1, 0, 0), math.radians(-14))

def divka_a(o):
    """z college_girl jen prvni divka na kostre (ostatni tri pryc)"""
    if o.parent is None or o.parent.type != 'ARMATURE':
        return False
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me_ = e.to_mesh()
    x = sum((o.matrix_world @ v.co).x for v in me_.vertices) / max(1, len(me_.vertices)); e.to_mesh_clear()
    return x < -1.0

priprava = (ruce_dolu_college if "college" in JMENO else ruce_dolu) if POZA == "ruce_dolu" else None
nechat = (lambda o: "Icosphere" not in o.name) if "galaxia" in JMENO else divka_a if "college" in JMENO else None
meshe = P.nacti(JMENO, VYSKA, priprava=priprava, nechat=nechat, emise=0.0 if "anime" in JMENO else None)
if POZA == "sedi":
    nohy = P.stredy_nohou(meshe, VYSKA)
    kotva, _, _ = P.sed(meshe, VYSKA, 0.49, 0.28, [nohy[0][1], nohy[1][1]])
    kotva = Vector((kotva.x, kotva.y, 0.0))
else:
    kotva = Vector((0.0, 0.0, 0.0))
# postava celem k -y; v Blenderu je smer skupiny (cos, sin) = (sin u, -cos u), tj. otoceni o u kolem z
M = Matrix.Rotation(SMER, 4, 'Z') @ Matrix.Scale(K, 4) @ Matrix.Translation(-kotva)
P.postav(meshe, M)

# chytac stinu kolem chodidel
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
zem = bpy.context.object; zem.scale = (8, 8, 1); zem.is_shadow_catcher = True

# kamera a slunce jako budovy: 30 st nad obzorem, od jihu (azimut 45 st), slunce zleva shora
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 60.0
cam_pos = (DIST * math.sin(ax) * math.sin(az), -DIST * math.sin(ax) * math.cos(az), DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
cam.rotation_euler = (-Vector(cam_pos)).to_track_quat('-Z', 'Y').to_euler()
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * -0.25 + Vector((0, 0, 1.0))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "2.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def render_do_pole():
    scene.render.filepath = os.path.splitext(VYSTUP)[0] + "_tmp.png"
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(scene.render.filepath).convert("RGBA"), dtype=np.float64) / 255
    os.remove(scene.render.filepath)
    return a
STIN = float(os.environ.get("STIN", "0"))
A = render_do_pole() if STIN > 0 else None
zem.hide_render = True
Bp = render_do_pole()
aB = Bp[..., 3]
aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN if STIN > 0 else np.zeros_like(aB)
alfa = aB + (1 - aB) * aS
barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
Image.fromarray((np.dstack([barva, alfa]) * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(VYSTUP)
json.dump({"postava": JMENO, "poza": POZA, "smer_st": math.degrees(SMER), "meritko": K, "px_m": PX_M, "ram": RAM,
           "chodidla": [RAM / 2, RAM / 2]}, open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
