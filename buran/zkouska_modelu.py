# Zkusme fotky modelu z par6: kam miri cumak, jak vypadaji. Neni to finalni foceni.
#   python3 zkouska_modelu.py <model.glb> <skutecna delka v m nebo 0> <vystup.png>
import bpy, sys, math, os
from mathutils import Vector
MODEL, DELKA_M, OUT = sys.argv[-3], float(sys.argv[-2]), sys.argv[-1]
HDRI = "/home/user/grrrrf/glb/GLB/hdri/snow.exr"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.cycles.use_denoising = False
sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = 360
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True; nt = w.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment'); wo = nt.nodes.new('ShaderNodeOutputWorld')
env.image = bpy.data.images.load(HDRI); nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
bpy.ops.import_scene.gltf(filepath=MODEL)
meshe = [o for o in sc.objects if o.type == 'MESH']
pts = [o.matrix_world @ v.co for o in meshe for v in o.data.vertices]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
st = (mn + mx) / 2; roz = mx - mn
# kde je ocas: body v horni petine vysky, jejich prumerne Y
horni = [p for p in pts if p.z > mn.z + 0.8 * roz.z]
ocas_y = sum(p.y for p in horni) / max(1, len(horni))
print(f"MODEL {os.path.basename(MODEL)} rozmer {roz.x:.2f} {roz.y:.2f} {roz.z:.2f} stred {st.y:.2f} horni body prumer Y {ocas_y:.2f} -> ocas na {'+Y' if ocas_y > st.y else '-Y'}")
k = DELKA_M / roz.y if DELKA_M > 0 else 1.0
velikost = max(roz) * k
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = velikost * 1.25
fotky = []
for jm, az in (("z boku +X", 90), ("zepredu -Y", 0), ("hra 45", 45)):
    a = math.radians(az); e = math.radians(30)
    d = velikost * 3
    cam.location = (st.x + d * math.cos(e) * math.sin(a), st.y - d * math.cos(e) * math.cos(a), st.z + d * math.sin(e))
    cam.rotation_euler = (math.radians(90 - 30), 0, a)
    sc.render.filepath = OUT.replace(".png", f"_{az}.png")
    bpy.ops.render.render(write_still=True); fotky.append(sc.render.filepath)
print("FOTKY", fotky)
