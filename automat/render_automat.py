# -*- coding: utf-8 -*-
# Automat na marihuanu na 1 policko (hrac 1. 10. s fotkami CBD MAT: "jeste udelej 1x1 policko automat na marihuanu
# s lavickou a kerickem krovi"). Vlastni model, kamera, meritko a svetlo jako gymnazium (gymnazium/render_gymnazium.py):
# ortho 30 st. shora, 12,2 px/m v zin4, slunce zleva shora se silnejsimi stiny jako u Tatry, stin na travu na 55 %.
# Automat podle fotek: tmave seda skrin, prosklena dvirka s regaly, vpravo zeleny pruh s placenim, dole vydejni
# klapka se zelenym stitkem PULL, bok polepeny zelenou folii s listy konopi, paprsky a bilym napisem CBD MAT.
# Skupina je ctverec (hrac: "to mas obdelnicek, neco jako 2x1 policko", "lavicku postav pred automat, otoc ji
# sedadlem k automatu a mas ctverec"): automat vzadu, lavicka pred nim sedadlem k nemu, ker vedle, dlazba 4 x 4 m
# s obrubnikem uprostred policka. MERITKO=2 zvetsi celou skupinu i s dlazbou kolem stredu policka.
#   python3 render_automat.py <vystup.png>
# Souradnice jako ve hre: x k jihozapadu, y k jihovychodu, z nahoru, pocatek v severnim rohu policka.
import bpy, bmesh, os, sys, math, json, random
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image, ImageDraw, ImageFont

VYSTUP = sys.argv[-1]
PX_M = 12.2
RAM = 384
K = float(os.environ.get("MERITKO", "1"))
T = 256 / (math.sqrt(2) * PX_M)               # policko 14,84 m
C = T / 2                                       # stred policka
TU = os.path.dirname(os.path.abspath(__file__))
HDRI = os.path.join(TU, "..", "glb", "GLB", "hdri", "snow.exr")
PISMO = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEX = os.path.splitext(VYSTUP)[0] + "_tex"
os.makedirs(TEX, exist_ok=True)

# ---------------------------------------------------------------- obrazky na automat (polep boku a predek)
def list_konopi(d, cx, cy, delka, uhel, barva):
    """list konopi: sedm listku do vejire, prostredni nejdelsi, kazdy kopinaty se zubatym okrajem"""
    for rel, dl in ((0, 1.0), (-27, 0.86), (27, 0.86), (-54, 0.66), (54, 0.66), (-82, 0.42), (82, 0.42)):
        a = math.radians(uhel + rel); L = delka * dl; w = L * 0.13
        osa = (math.cos(a), math.sin(a)); kolmo = (-osa[1], osa[0])
        body = []
        for i in range(13):                       # jedna strana od spicky ke stopce, zoubky
            t = i / 12; s = math.sin(math.pi * t) ** 0.8 * w * (1.15 if i % 2 else 0.85)
            body.append((cx + osa[0] * L * (1 - t) + kolmo[0] * s, cy + osa[1] * L * (1 - t) + kolmo[1] * s))
        for i in range(12, -1, -1):
            t = i / 12; s = math.sin(math.pi * t) ** 0.8 * w * (1.15 if i % 2 else 0.85)
            body.append((cx + osa[0] * L * (1 - t) - kolmo[0] * s, cy + osa[1] * L * (1 - t) - kolmo[1] * s))
        d.polygon(body, fill=barva)
    a = math.radians(uhel + 180)
    d.line([(cx, cy), (cx + math.cos(a) * delka * 0.35, cy + math.sin(a) * delka * 0.35)], fill=barva, width=max(2, int(delka * 0.03)))

def napis(d, text, cx, cy, vyska, barva, obrys):
    f = ImageFont.truetype(PISMO, int(vyska))
    for dx in range(-4, 5, 2):
        for dy in range(-4, 5, 2):
            d.text((cx + dx + 5, cy + dy + 6), text, font=f, fill=obrys, anchor="mm")
    d.text((cx, cy), text, font=f, fill=barva, anchor="mm")

def obrazek_bok(cesta):
    W, H = 340, 732
    im = Image.new("RGB", (W, H), (92, 186, 50)); d = ImageDraw.Draw(im)
    sx, sy = W * 0.55, H * 0.56
    for k in range(28):                                                  # paprsky ze stredu
        if k % 2: continue
        a0, a1 = 2 * math.pi * k / 28, 2 * math.pi * (k + 1) / 28
        d.polygon([(sx, sy), (sx + 2000 * math.cos(a0), sy + 2000 * math.sin(a0)), (sx + 2000 * math.cos(a1), sy + 2000 * math.sin(a1))],
                  fill=(116, 204, 66))
    tmava, stredni = (30, 96, 32), (46, 120, 40)
    for cx, cy, dl, u, b in ((70, 90, 150, -60, tmava), (270, 150, 170, -120, tmava), (60, 400, 120, -100, stredni),
                             (290, 360, 100, -70, tmava), (90, 640, 170, -80, tmava), (270, 650, 150, -110, tmava),
                             (180, 260, 70, -95, stredni), (300, 560, 60, -60, stredni), (40, 250, 60, -40, stredni)):
        list_konopi(d, cx, cy, dl, u, b)
    pis = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pis)
    napis(dp, "CBD", W * 0.5, H * 0.47, 112, (246, 246, 244), (20, 60, 22))
    napis(dp, "MAT", W * 0.52, H * 0.62, 112, (246, 246, 244), (20, 60, 22))
    pis = pis.rotate(8, resample=Image.BICUBIC, center=(W * 0.5, H * 0.55))
    im.paste(pis, (0, 0), pis)
    im.save(cesta)

def obrazek_predek(cesta):
    W, H = 360, 732
    im = Image.new("RGB", (W, H), (66, 68, 70)); d = ImageDraw.Draw(im)
    gx0, gx1, gy0, gy1 = 0.05 * W, 0.67 * W, 0.04 * H, 0.66 * H
    d.rectangle([gx0 - 8, gy0 - 8, gx1 + 8, gy1 + 8], fill=(128, 130, 134))           # ram skla
    d.rectangle([gx0, gy0, gx1, gy1], fill=(22, 26, 32))                             # vnitrek
    rnd = random.Random(3)
    barvy = [(236, 236, 230), (90, 190, 60), (200, 200, 205), (30, 30, 30), (230, 140, 40), (60, 120, 200), (240, 240, 240)]
    police = 6
    for i in range(police):
        y1 = gy0 + (gy1 - gy0) * (i + 1) / police
        y0 = y1 - (gy1 - gy0) / police
        x = gx0 + 14
        while x < gx1 - 16:                                                  # baliky na polici
            w = rnd.randint(14, 26); h = rnd.randint(int((y1 - y0) * 0.45), int((y1 - y0) * 0.8))
            d.rectangle([x, y1 - 6 - h, x + w, y1 - 6], fill=rnd.choice(barvy))
            x += w + rnd.randint(3, 8)
        d.rectangle([gx0, y1 - 6, gx1, y1 - 1], fill=(176, 178, 184))              # police
    d.rectangle([gx0 + 3, gy0, gx0 + 7, gy1], fill=(250, 250, 255))                   # svetelny pas LED
    d.rectangle([gx0 + 16, gy0 + 10, gx0 + 64, gy0 + 40], fill=(236, 236, 236))       # nalepka POZOR
    d.rectangle([gx0 + 16, gy0 + 10, gx0 + 64, gy0 + 22], fill=(210, 30, 30))
    px0, px1 = 0.72 * W, 0.95 * W                                                    # zeleny pruh s placenim
    d.rectangle([px0, 0.05 * H, px1, 0.89 * H], fill=(96, 200, 58))
    d.rectangle([px0 + 14, 0.10 * H, px1 - 14, 0.16 * H], fill=(236, 240, 236))       # papir s cenikem
    d.rectangle([px0 + 10, 0.22 * H, px1 - 10, 0.29 * H], fill=(26, 26, 28))          # ctecka karet
    d.rectangle([px0 + 16, 0.32 * H, px1 - 16, 0.345 * H], fill=(40, 80, 230))        # displej
    for r in range(4):                                                               # klavesnice
        for s in range(3):
            x = px0 + 14 + s * 18; y = 0.40 * H + r * 18
            d.rectangle([x, y, x + 12, y + 12], fill=(170, 172, 176))
    d.rectangle([px0 + 22, 0.60 * H, px1 - 22, 0.66 * H], fill=(150, 152, 156))       # mince
    d.rectangle([px0 + 26, 0.72 * H, px1 - 26, 0.76 * H], fill=(30, 30, 32))
    d.rectangle([0.07 * W, 0.70 * H, 0.66 * W, 0.86 * H], fill=(52, 54, 56))           # vydejni klapka
    d.rectangle([0.17 * W, 0.735 * H, 0.56 * W, 0.825 * H], fill=(96, 200, 58))       # zeleny stitek PULL
    f = ImageFont.truetype(PISMO, 40)
    d.text((0.365 * W, 0.78 * H), "PULL", font=f, fill=(24, 60, 24), anchor="mm")
    d.rectangle([0, 0.9 * H, W, H], fill=(38, 38, 40))                               # sokl
    im.save(cesta)

obrazek_bok(os.path.join(TEX, "bok.png")); obrazek_predek(os.path.join(TEX, "predek.png"))

# ---------------------------------------------------------------- scena jako gymnazium
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
scene.world.cycles_visibility.shadow = True
bg.inputs["Strength"].default_value = float(os.environ.get("OKOLI", "0.35"))

def srgb(c):
    return tuple(((v / 255) ** 2.2) for v in c) + (1.0,)

def mat(jmeno, rgb, drsnost=0.8, kov=0.0, sum_=0.0, meritko=2.0, obrazek=None):
    m = bpy.data.materials.new(jmeno); m.use_nodes = True
    t = m.node_tree; b = t.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if obrazek:
        tx = t.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(obrazek); tx.interpolation = 'Cubic'
        t.links.new(tx.outputs["Color"], b.inputs["Base Color"])
    elif sum_:
        tex = t.nodes.new('ShaderNodeTexNoise'); tex.inputs["Scale"].default_value = meritko; tex.inputs["Detail"].default_value = 6.0
        ramp = t.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = srgb(tuple(max(0, v * (1 - sum_)) for v in rgb))
        ramp.color_ramp.elements[1].color = srgb(tuple(min(255, v * (1 + sum_)) for v in rgb))
        t.links.new(tex.outputs["Fac"], ramp.inputs["Fac"]); t.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = srgb(rgb)
    return m

M = {
    "skrin": mat("skrin", (66, 68, 70), 0.45, kov=0.3),
    "bok": mat("bok", (0, 0, 0), 0.35, obrazek=os.path.join(TEX, "bok.png")),
    "predek": mat("predek", (0, 0, 0), 0.25, obrazek=os.path.join(TEX, "predek.png")),
    "dlazba": mat("dlazba", (182, 178, 170), 0.9, sum_=0.07, meritko=6.0),
    "spara": mat("spara", (140, 136, 128), 0.95),
    "obrubnik": mat("obrubnik", (150, 146, 138), 0.9, sum_=0.06, meritko=8.0),
    "lavicka": mat("lavicka", (138, 92, 52), 0.7),
    "kov": mat("kov", (52, 58, 54), 0.5, kov=0.5),
    "ker": mat("ker", (54, 98, 40), 0.9, sum_=0.32, meritko=9.0),
}

SITE = {}
def bm_pro(m):
    if m.name not in SITE: SITE[m.name] = (m, bmesh.new())
    return SITE[m.name][1]

def B(x, y, z):
    """policko -> Blender; skupina je kolem stredu policka zvetsena K krat"""
    return Vector((C + (y - C) * K, -(C + (x - C) * K), z * K))

def kvadr(m, x0, x1, y0, y1, z0, z1, pevne=False):
    """kvadr; pevne = na policku bez zvetseni (dlazba)"""
    bm = bm_pro(m); b_ = (lambda x, y, z: Vector((y, -x, z))) if pevne else B
    v = [bm.verts.new(b_(x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        bm.faces.new([v[i] for i in f])

def mnohostena(m, body, steny):
    bm = bm_pro(m)
    v = [bm.verts.new(B(*p)) for p in body]
    for f in steny: bm.faces.new([v[i] for i in f])

def obraz(m, rohy):
    """ctyruhelnik s obrazkem: rohy v poradi vlevo dole, vpravo dole, vpravo nahore, vlevo nahore (jak ho vidi divak)"""
    bm = bm_pro(m); uv = bm.loops.layers.uv.verify()
    f = bm.faces.new([bm.verts.new(B(*p)) for p in rohy])
    for smycka, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        smycka[uv].uv = (u, v)

# ---------------------------------------------------------------- automat, lavicka, ker, dlazba
AX0 = C - 1.45; AX1 = AX0 + 0.85                # predek k jihozapadu (+x), hloubka 85 cm
AY0 = C - 1.05; AY1 = AY0 + 0.9                  # sirka 90 cm, bok s polepem k jihovychodu (+y)
AZ0, AZ1 = 0.04, 1.83
kvadr(M["skrin"], AX0, AX1, AY0, AY1, AZ0, AZ1)
for xx in (AX0 + 0.06, AX1 - 0.1):                                            # nozicky
    for yy in (AY0 + 0.06, AY1 - 0.1):
        kvadr(M["kov"], xx, xx + 0.04, yy, yy + 0.04, 0.0, AZ0)
obraz(M["predek"], [(AX1 + 0.004, AY0, AZ0), (AX1 + 0.004, AY1, AZ0), (AX1 + 0.004, AY1, AZ1), (AX1 + 0.004, AY0, AZ1)])
obraz(M["bok"], [(AX1, AY1 + 0.004, AZ0), (AX0, AY1 + 0.004, AZ0), (AX0, AY1 + 0.004, AZ1), (AX1, AY1 + 0.004, AZ1)])

def lavicka(x, y, uhel):
    """lavicka 1,6 m jako u gymnazia; uhel: kam se sedici diva (rad)"""
    c, s = math.cos(uhel), math.sin(uhel)
    def bod(u, v, z):
        return (x + u * -s + v * -c, y + u * c + v * -s, z)
    def kus(m, u0, u1, v0, v1, z0, z1):
        b = [bod(u, v, z) for z in (z0, z1) for v in (v0, v1) for u in (u0, u1)]
        mnohostena(m, b, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)])
    kus(M["lavicka"], -0.8, 0.8, -0.22, 0.22, 0.42, 0.47)
    kus(M["lavicka"], -0.8, 0.8, 0.2, 0.25, 0.5, 0.88)
    for u in (-0.65, 0.65):
        kus(M["kov"], u - 0.03, u + 0.03, -0.2, 0.22, 0.0, 0.42)
lavicka(AX1 + 1.4, (AY0 + AY1) / 2, math.pi)                               # pred automatem, sedi se k nemu

# dlazba 4 x 4 m z betonovych dlazdic 50 cm se sparami, kolem obrubnik 15 cm, uprostred policka
D0, D1, OBR, Z_D = C - 2.0, C + 2.0, 0.15, 0.03
for (x0, x1, y0, y1) in ((D0, D1, D0, D0 + OBR), (D0, D1, D1 - OBR, D1), (D0, D0 + OBR, D0 + OBR, D1 - OBR), (D1 - OBR, D1, D0 + OBR, D1 - OBR)):
    kvadr(M["obrubnik"], x0, x1, y0, y1, 0.0, Z_D + 0.03)
kvadr(M["spara"], D0 + OBR, D1 - OBR, D0 + OBR, D1 - OBR, 0.0, Z_D - 0.004)
n_ = int(round((D1 - D0 - 2 * OBR) / 0.5)); kr = (D1 - D0 - 2 * OBR) / n_
for i in range(n_):
    for j in range(n_):
        x, y = D0 + OBR + kr * i, D0 + OBR + kr * j
        kvadr(M["dlazba"], x + 0.012, x + kr - 0.012, y + 0.012, y + kr - 0.012, 0.0, Z_D)

# kericek vpravo za automatem: par koul s hrbolky, mekce stinovany
rnd = random.Random(5)
KX, KY, KR = AX0 + 0.6, AY1 + 0.95, 0.6               # vpravo vedle automatu
for i in range(9):                                     # hrbolaty ker z mensich chumacu, ne hladka koule
    a = rnd.random() * 2 * math.pi; d = KR * 0.6 * math.sqrt(rnd.random())
    rr = KR * (0.38 + 0.16 * rnd.random())
    zc = KR * (0.45 + 0.5 * rnd.random()) * (1 - 0.4 * d / KR)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=rr * K, location=B(KX + d * math.cos(a), KY + d * math.sin(a), zc))
    o = bpy.context.object; o.data.materials.append(M["ker"])
    for p in o.data.polygons: p.use_smooth = True
    dm = o.modifiers.new("hrbol", 'DISPLACE'); tx = bpy.data.textures.new(f"ker{i}", 'CLOUDS'); tx.noise_scale = 0.09 * K
    dm.texture = tx; dm.strength = rr * 0.55 * K

for jmeno, (m, bm) in SITE.items():
    me = bpy.data.meshes.new(jmeno); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jmeno, me); scene.collection.objects.link(o); me.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=1, location=Vector((C, -C, 0.0)))
zem = bpy.context.object; zem.scale = (T, T, 1); zem.is_shadow_catcher = True

# ---------------------------------------------------------------- kamera a slunce jako gymnazium a Tatra
stred = Vector((C, -C, 0.0))
bpy.ops.object.empty_add(type='PLAIN_AXES', location=stred); cil = bpy.context.object
ax = math.radians(90 - 30.0); az = math.radians(45.0); DIST = 60.0
cam_pos = (stred.x + DIST * math.sin(ax) * math.sin(az), stred.y - DIST * math.sin(ax) * math.cos(az), stred.z + DIST * math.cos(ax))
bpy.ops.object.camera_add(location=cam_pos); cam = bpy.context.object; scene.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = RAM / PX_M; cam.data.clip_start = 0.001; cam.data.clip_end = 1000
c = cam.constraints.new(type='TRACK_TO'); c.target = cil
ke_kamere = Vector((math.sin(az), -math.cos(az), 0.0)); vlevo = Vector((-math.cos(az), -math.sin(az), 0.0))
odkud = (vlevo * 1.0 + ke_kamere * -0.25 + Vector((0, 0, 1.0))).normalized()
bpy.ops.object.light_add(type='SUN'); sl = bpy.context.object
sl.data.energy = float(os.environ.get("SLUNCE", "5.0")); sl.data.angle = math.radians(6)
sl.rotation_euler = odkud.to_track_quat('Z', 'Y').to_euler()

def na_pixel(p):
    bpy.context.view_layer.update()
    q = world_to_camera_view(scene, cam, p)
    return (q.x * RAM, (1 - q.y) * RAM)
rohy = {"sever": na_pixel(Vector((0, 0, 0))), "vychod": na_pixel(Vector((T, 0, 0))),
        "zapad": na_pixel(Vector((0, -T, 0))), "jih": na_pixel(Vector((T, -T, 0)))}
print("rohy policka na obrazku", {k: tuple(round(c, 2) for c in v) for k, v in rohy.items()})

# stin na travu jen na 55 % jako u gymnazia: render s chytacem stinu a bez nej, rozdil je stin
def render_do_pole():
    scene.render.filepath = os.path.splitext(VYSTUP)[0] + "_tmp.png"
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(scene.render.filepath).convert("RGBA"), dtype=np.float64) / 255
    os.remove(scene.render.filepath)
    return a
A = render_do_pole()
zem.hide_render = True
Bp = render_do_pole()
STIN = float(os.environ.get("STIN", "0.55"))
aB = Bp[..., 3]; aS = np.clip((A[..., 3] - aB) / np.maximum(1 - aB, 1e-6), 0, 1) * STIN
alfa = aB + (1 - aB) * aS
barva = np.where(alfa[..., None] > 0, Bp[..., :3] * aB[..., None] / np.maximum(alfa[..., None], 1e-6), 0)
Image.fromarray((np.dstack([barva, alfa]) * 255 + 0.5).clip(0, 255).astype(np.uint8), "RGBA").save(VYSTUP)
json.dump({"px_m": PX_M, "policko_m": T, "meritko_skupiny": K, "ram": RAM, "rohy": rohy},
          open(os.path.splitext(VYSTUP)[0] + ".json", "w"), indent=1)
print("hotovo", VYSTUP)
