# -*- coding: utf-8 -*-
# Rostliny marihuany ze Sketchfabu (z release par6, CC BY 4.0, autori v AUTORI-MODELU.md) pro obrazky budov:
# nacteni bez kvetinace, prebarveni na zelenou nakladu MARI (jako kupka marihuany na V3S, v3s/render_v3s.py) a
# postaveni do sceny vic kusu se spolecnou siti. Pouziva socha/render_socha.py.
import bpy, math, os
import numpy as np
from mathutils import Matrix, Vector

TU = os.path.dirname(os.path.abspath(__file__))
MARI = ((48, 98, 10), (94, 144, 26))                # tmava a svetla zelena kupky MARI


def _srgb(c):
    return tuple((v / 255) ** 2.2 for v in c) + (1.0,)


def prebarvi_mari(m):
    """barva listu z textury -> jas -> prechod mezi tmavou a svetlou zelenou MARI; pruhlednost listu zustava"""
    t = m.node_tree
    b = next((n for n in t.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:
        return
    vstup = b.inputs["Base Color"]
    if not vstup.is_linked:
        vstup.default_value = _srgb(MARI[0]); return
    zdroj = vstup.links[0].from_socket
    bw = t.nodes.new('ShaderNodeRGBToBW'); t.links.new(zdroj, bw.inputs[0])
    ramp = t.nodes.new('ShaderNodeValToRGB')
    # textury listu jsou tmave (jas do 0,25), at nevyjdou jako jedle: svetla MARI uz od jasu 0,2
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = _srgb(MARI[0])
    ramp.color_ramp.elements[1].position = 0.2; ramp.color_ramp.elements[1].color = _srgb(MARI[1])
    t.links.new(bw.outputs[0], ramp.inputs[0]); t.links.new(ramp.outputs[0], vstup)


def nacti(jmeno):
    """GLB -> seznam siti v jednotkach modelu: pata kmene v 0 0 0, vyska 1. Kvetinac (material bucket) pryc.
    Vrati (site, nejvetsi polomer koruny k vysce)."""
    pred = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(TU, jmeno + ".glb"))
    nove = [o for o in bpy.data.objects if o not in pred]
    site = []
    for o in nove:
        if o.type == 'MESH' and not any(s.material and "bucket" in s.material.name for s in o.material_slots):
            me = o.data.copy(); me.transform(o.matrix_world); site.append(me)
    for o in nove:
        bpy.data.objects.remove(o, do_unlink=True)
    P = np.vstack([np.array([v.co[:] for v in me.vertices]) for me in site])
    z0, z1 = P[:, 2].min(), P[:, 2].max(); H = z1 - z0
    pata = P[P[:, 2] - z0 < 0.03 * H][:, :2].mean(axis=0)
    T = Matrix.Scale(1 / H, 4) @ Matrix.Translation((-pata[0], -pata[1], -z0))
    for me in site:
        me.transform(T)
        for s in me.materials:
            if s is not None and s.use_nodes:
                prebarvi_mari(s)
    P = np.vstack([np.array([v.co[:] for v in me.vertices]) for me in site])
    return site, float(np.sqrt(P[:, 0] ** 2 + P[:, 1] ** 2).max())


def postav(site, polomer_k_vysce, matice_paty, vyska, polomer_max, otoceni, jmeno="konopi"):
    """jedna rostlina: pata v matice_paty (Blender), vyska a nejvetsi polomer koruny v jednotkach sceny;
    kdyz by koruna byla sirsi, rostlina se do sirky zuzi (stihla jako venkovni sativa)"""
    sirka = min(vyska, polomer_max / polomer_k_vysce)
    M = matice_paty @ Matrix.Rotation(otoceni, 4, 'Z') @ Matrix.Diagonal((sirka, sirka, vyska, 1.0))
    objekty = []
    for i, me in enumerate(site):
        o = bpy.data.objects.new(f"{jmeno}_{i}", me)
        bpy.context.scene.collection.objects.link(o)
        o.matrix_world = M
        objekty.append(o)
    return objekty
