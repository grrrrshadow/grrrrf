# -*- coding: utf-8 -*-
# Skoda 706 RTO (linkovy KAR) jako vlastni model z primitiv v bpy: kvadr s loopy a subdivision surface (zaobleny
# trup), okna jako slupka trupu orezana kvadry (sklo sleduje zaobleni), dvere jako tmave linky, kola, mrizka,
# svetla, naraznik, zrcatka. Zadny cizi model: hrac 2. 10.: "to nemusi byt 3D model focenej, ty umis dobre kreslit".
# Rozmery (m, cs.wikipedia): delka 10,81, sirka 2,50, vyska 2,90-2,98, rozvor 5,45, previs vpredu 1,57 a vzadu 3,79,
# pneu 11.00-20 (prumer ~1,05). Celo je na +Y (jako V3S), zem z = 0, stred delky y = 0.
import bpy, bmesh, math
from mathutils import Vector, Matrix

L, W, H = 10.81, 2.50, 2.95
Y0, Y1 = -L / 2, L / 2
PREDNI = Y1 - 1.57                       # +3.835
ZADNI = Y0 + 3.79                        # -1.615
R_KOLA, SIRKA_KOLA = 0.525, 0.28
Z_SPODEK = 0.45                          # spodni hrana karoserie (sukne)
Z_PRUH = (1.38, 1.58)                    # sedy pruh pod okny; pod nim cervena, nad nim kremova
Z_OKNA = (1.76, 2.52)
# okna na boku (y od, y do): okno zadnich dveri, ctyri okna, okno prednich dveri, dve okna, ridic
DVERE_PREDNI = (1.495, 2.295)
DVERE_ZADNI = (-5.10, -4.40)
# kvadry oken se nesmi prekryvat (ani s celnim a zadnim sklem), jinak presny boolean vrati prazdno
OKNA_BOK = [(-4.95, -4.55), (-4.26, -2.96), (-2.82, -1.52), (-1.38, -0.08), (0.06, 1.36), (1.56, 2.24),
            (2.42, 3.22), (3.34, 4.08), (4.20, 4.42)]

NATERY = {
    # hrac: linkovy CSAD cerveno-kremovy; druhy modro-kremovy (mestsky / LUX)
    "cervena": {"spodek": (160, 24, 30), "pruh": (174, 176, 174), "vrsek": (248, 238, 206)},
    "modra": {"spodek": (28, 78, 168), "pruh": (248, 238, 206), "vrsek": (248, 238, 206)},
}

def srgb(c, a=1.0):
    return tuple((v / 255) ** 2.2 for v in c) + (a,)

def material(jm, rgb, drsnost=0.45, kov=0.0, emise=0.0):
    m = bpy.data.materials.new(jm); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(rgb)
    b.inputs["Roughness"].default_value = drsnost; b.inputs["Metallic"].default_value = kov
    if emise:
        b.inputs["Emission Color"].default_value = srgb(rgb); b.inputs["Emission Strength"].default_value = emise
    return m

def kvadr(jm, x0, x1, y0, y1, z0, z1, mat, scene):
    me = bpy.data.meshes.new(jm); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(x1 - x0, y1 - y0, z1 - z0), verts=bm.verts)
    bmesh.ops.translate(bm, vec=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), verts=bm.verts)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(jm, me); scene.collection.objects.link(o); o.data.materials.append(mat)
    return o

def valec(jm, osa, r, delka, stred, mat, scene, seg=48):
    me = bpy.data.meshes.new(jm); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=delka)
    if osa == "x": bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(90), 3, 'Y'), verts=bm.verts)
    if osa == "y": bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(90), 3, 'X'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=stred, verts=bm.verts)
    bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    o = bpy.data.objects.new(jm, me); scene.collection.objects.link(o); o.data.materials.append(mat)
    return o

def trup_mesh(jm, mats):
    """kvadr trupu s loopy (bisect) a subdivision; materialy podle vysky: spodek, pruh, vrsek"""
    me = bpy.data.meshes.new(jm); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(W, L, H - Z_SPODEK), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, (H + Z_SPODEK) / 2), verts=bm.verts)
    rezy = ([("x", v) for v in (-W / 2 + 0.6, 0.0, W / 2 - 0.6)] +
            [("y", v) for v in (Y0 + 0.85, Y0 + 1.8, 0.0, Y1 - 1.8, Y1 - 1.15)] +
            [("z", v) for v in (Z_SPODEK + 0.08, Z_PRUH[0], Z_PRUH[1], H - 0.52)])
    for osa, v in rezy:
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        no = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[osa]
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector(no) * v, plane_no=no, dist=1e-5)
    # vypoukle celo a zad, celni sklo mirne sklonene dozadu, mirne klenuta strecha
    for v in bm.verts:
        stred = abs(v.co.x) < 1e-4; kraj = abs(v.co.x) > W / 2 - 0.01
        if abs(v.co.y - Y1) < 1e-4:
            v.co.y += 0.30 if stred else (0.14 if not kraj else 0.0)
            if v.co.z > Z_PRUH[1]: v.co.y -= 0.12 * (v.co.z - Z_PRUH[1]) / (H - Z_PRUH[1])
        if abs(v.co.y - Y0) < 1e-4: v.co.y -= 0.15 if stred else (0.07 if not kraj else 0.0)
        if abs(v.co.z - H) < 1e-4: v.co.z += 0.08 if stred else (0.04 if not kraj else 0.0)
    bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
        z = me.vertices[f.vertices[0]].co.z; zc = sum(me.vertices[i].co.z for i in f.vertices) / len(f.vertices)
        f.material_index = 0 if zc < Z_PRUH[0] else (1 if zc < Z_PRUH[1] else 2)
    for m in mats: me.materials.append(m)
    return me

def subsurf(o, urovne=3):
    m = o.modifiers.new("sub", 'SUBSURF'); m.levels = urovne; m.render_levels = urovne
    return m

def postav(scene, nater="cervena"):
    """Postavi autobus do sceny. Vraci (objekty, {'celo': y, 'zad': y, 'napravy': [y...]})."""
    b = NATERY[nater]
    m_spodek = material("lak_spodek", b["spodek"], 0.35)
    m_pruh = material("lak_pruh", b["pruh"], 0.4, 0.15)
    m_vrsek = material("lak_vrsek", b["vrsek"], 0.35)
    m_chrom = material("chrom", (205, 205, 205), 0.22, 1.0)
    m_sklo = material("sklo", (14, 22, 32), 0.08)
    m_guma = material("guma", (26, 26, 26), 0.85)
    m_disk = material("disk", (150, 150, 148), 0.4, 0.6)
    m_tma = material("tma", (18, 18, 18), 0.6)
    m_svetlo = material("svetlo", (245, 243, 230), 0.15, 0.0, 0.6)
    m_zadni = material("zadni_svetlo", (200, 20, 20), 0.2, 0.0, 0.8)
    m_podvozek = material("podvozek", (40, 40, 40), 0.8)
    m_strecha = material("strecha_poklop", (228, 217, 188), 0.5)
    objs = []
    # trup
    me = trup_mesh("trup", (m_spodek, m_pruh, m_vrsek))
    trup = bpy.data.objects.new("trup", me); scene.collection.objects.link(trup); subsurf(trup)
    # podbehy kol: valce odectene od trupu
    podbehy = bpy.data.meshes.new("podbehy"); bm = bmesh.new()
    for yy in (PREDNI, ZADNI):
        for sx in (-1, 1):
            bmesh.ops.create_cone(bm, cap_ends=True, segments=40, radius1=0.63, radius2=0.63, depth=0.75,
                                  matrix=Matrix.Translation((sx * 0.95, yy, R_KOLA)) @ Matrix.Rotation(math.radians(90), 4, 'Y'))
    bm.to_mesh(podbehy); bm.free()
    o_podbehy = bpy.data.objects.new("podbehy", podbehy); scene.collection.objects.link(o_podbehy); o_podbehy.hide_render = True
    bo = trup.modifiers.new("podbehy", 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = o_podbehy; bo.solver = 'EXACT'
    objs.append(trup)
    # okna: slupka trupu (displace 12 mm) orezana kvadry oken
    okna = bpy.data.meshes.new("okna_rez"); bm = bmesh.new()
    def box(x0, x1, y0, y1, z0, z1):
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)) @
                              Matrix.Diagonal((x1 - x0, y1 - y0, z1 - z0, 1.0)))
    for y0, y1 in OKNA_BOK:
        for sx in (-1, 1):
            box(sx * (W / 2 - 0.3), sx * (W / 2 + 0.3), y0, y1, Z_OKNA[0], Z_OKNA[1])
    box(-1.36, -0.04, Y1 - 0.88, Y1 + 0.6, 1.68, 2.62)                              # celni sklo, dve tabule, pres rohy
    box(0.04, 1.36, Y1 - 0.88, Y1 + 0.6, 1.68, 2.62)
    box(-0.98, -0.05, Y0 - 0.5, Y0 + 0.35, Z_OKNA[0], Z_OKNA[1] - 0.04)               # zadni okno, dve tabule
    box(0.05, 0.98, Y0 - 0.5, Y0 + 0.35, Z_OKNA[0], Z_OKNA[1] - 0.04)
    box(-0.45, 0.45, Y0 - 0.5, Y0 + 0.4, 2.62, 2.84)                                 # male okenko nad zadnim oknem
    bm.to_mesh(okna); bm.free()
    o_rez = bpy.data.objects.new("okna_rez", okna); scene.collection.objects.link(o_rez); o_rez.hide_render = True
    slupka = bpy.data.objects.new("okna", me.copy()); scene.collection.objects.link(slupka)
    for i in range(len(slupka.data.materials)): slupka.data.materials[i] = m_sklo
    subsurf(slupka)
    d = slupka.modifiers.new("ven", 'DISPLACE'); d.strength = 0.012; d.mid_level = 0.0; d.direction = 'NORMAL'
    bo = slupka.modifiers.new("okna", 'BOOLEAN'); bo.operation = 'INTERSECT'; bo.object = o_rez; bo.solver = 'EXACT'
    objs.append(slupka)
    # dvere: tmave linky (predni dvoukridle vpravo i vlevo? jen vpravo ve smeru jizdy = +X), zadni jednokridle
    for (y0, y1), kridla in ((DVERE_PREDNI, 2), (DVERE_ZADNI, 1)):
        hrany = [y0 + (y1 - y0) * k / kridla for k in range(kridla + 1)]
        for yy in hrany:
            objs.append(kvadr("dvere", W / 2 - 0.05, W / 2 + 0.016, yy - 0.012, yy + 0.012, Z_SPODEK + 0.1, Z_OKNA[1] + 0.03, m_tma, scene))
    # kola a podvozek
    for yy in (PREDNI, ZADNI):
        for sx in (-1, 1):
            sirka = SIRKA_KOLA if yy == PREDNI else 0.6
            xs = sx * (1.22 - sirka / 2)
            objs.append(valec("kolo", "x", R_KOLA, sirka, (xs, yy, R_KOLA), m_guma, scene))
            objs.append(valec("disk", "x", 0.25, 0.03, (sx * 1.225, yy, R_KOLA), m_disk, scene, 32))
    objs.append(kvadr("podvozek", -1.05, 1.05, Y0 + 0.25, Y1 - 0.25, 0.22, Z_SPODEK + 0.02, m_podvozek, scene))
    # celo: mrizka chladice s pruhy, svetla, naraznik, zrcatka, stitek nad celnim sklem
    yc = Y1 + 0.2
    objs.append(kvadr("mrizka", -0.62, 0.62, yc - 0.1, yc + 0.07, 0.80, 1.32, m_chrom, scene))
    for i in range(6):
        z = 0.845 + i * 0.085
        objs.append(kvadr("mrizka_pruh", -0.58, 0.58, yc - 0.1, yc + 0.085, z, z + 0.034, m_tma, scene))
    for sx in (-1, 1):
        objs.append(valec("svetlo", "y", 0.14, 0.12, (sx * 0.88, Y1 + 0.12, 0.98), m_svetlo, scene, 32))
        objs.append(valec("svetlo_ramek", "y", 0.16, 0.08, (sx * 0.88, Y1 + 0.09, 0.98), m_chrom, scene, 32))
        objs.append(kvadr("zrcatko_tyc", sx * (W / 2 - 0.05), sx * (W / 2 + 0.22), Y1 - 0.62, Y1 - 0.60, 2.08, 2.10, m_tma, scene))
        objs.append(kvadr("zrcatko", sx * (W / 2 + 0.17), sx * (W / 2 + 0.23), Y1 - 0.66, Y1 - 0.56, 1.98, 2.20, m_chrom, scene))
        objs.append(valec("zadni_svetlo", "y", 0.07, 0.08, (sx * 0.95, Y0 - 0.1, 1.05), m_zadni, scene, 24))
        objs.append(kvadr("naraznik_zadni", sx * 0.35, sx * 1.15, Y0 - 0.16, Y0 - 0.02, 0.46, 0.60, m_chrom, scene))
    objs.append(kvadr("naraznik", -1.15, 1.15, Y1 + 0.18, Y1 + 0.32, 0.46, 0.60, m_chrom, scene))
    objs.append(kvadr("stitek", -1.1, 1.1, Y1 - 0.02, Y1 + 0.30, 2.64, 2.71, m_vrsek, scene))
    objs.append(kvadr("poklop", -0.42, 0.42, 2.2, 3.1, H + 0.045, H + 0.075, m_strecha, scene))
    objs.append(kvadr("poklop", -0.42, 0.42, -2.6, -1.7, H + 0.045, H + 0.075, m_strecha, scene))
    for o in objs:
        for p in o.data.polygons:
            if o.name.startswith(("trup", "okna", "kolo", "disk", "svetlo", "zadni_svetlo")): p.use_smooth = True
    return objs, {"celo": Y1 + 0.32, "zad": Y0 - 0.16, "napravy": [PREDNI, ZADNI], "sirka": W, "vyska": H + 0.075}
