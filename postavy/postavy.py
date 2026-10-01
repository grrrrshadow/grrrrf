# -*- coding: utf-8 -*-
# Postavy z modelu hrace (zip7: dívky ze Sketchfabu, CC-BY-4.0, autori v LICENCE.md) pro druhe obrazky budov
# do animace: nacteni GLB, poza (sed na lavicce, chuze, objeti) a postaveni do sceny. Pouziva render_socha.py.
#
# Kazda postava se nejdriv udela staticka: sit ve svetovych souradnicich, chodidla v z 0, stred chodidel v x 0
# y 0, celem k -y, vyska v metrech. Modely s kostrou se napred napozuji kostmi a poza se zapece do site, modely
# bez kostry (stoji jako socha) se ohnou primo v siti: kazdy bod dostane vahy trupu, stehna a lytka podle vysky
# (hladky prechod kolem kycle a kolena), stehno se otoci kolem osy kycle, lytko jeste kolem kolena.
import bpy, math, os
import numpy as np
from mathutils import Vector, Matrix

TU = os.path.dirname(os.path.abspath(__file__))


def _vrcholy(o):
    a = np.zeros(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", a)
    return a.reshape(-1, 3)


def _zapis(o, v):
    o.data.vertices.foreach_set("co", np.ascontiguousarray(v, dtype=np.float64).ravel()); o.data.update()


def _zapec(objekty):
    """vsechny meshe -> staticke site ve svetovych souradnicich (i s pozou kostry), bez rodicu a modifikatoru"""
    dg = bpy.context.evaluated_depsgraph_get()
    meshe = []
    for o in objekty:
        if o.type != 'MESH':
            continue
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=False, depsgraph=dg)
        me.transform(o.matrix_world)
        n = bpy.data.objects.new(o.name + "_s", me)
        bpy.context.scene.collection.objects.link(n)
        meshe.append(n)
    for o in objekty:
        bpy.data.objects.remove(o, do_unlink=True)
    return meshe


def _rozmery(objekty, pozice=True):
    """vyska a stred chodidel (z vyhodnocenych siti, i s kostrou)"""
    dg = bpy.context.evaluated_depsgraph_get()
    P = []
    for o in objekty:
        if o.type != 'MESH':
            continue
        e = o.evaluated_get(dg); m = e.to_mesh()
        a = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get("co", a); a = a.reshape(-1, 3)
        W = np.array(o.matrix_world); P.append(a @ W[:3, :3].T + W[:3, 3]); e.to_mesh_clear()
    P = np.vstack(P)
    z0, z1 = P[:, 2].min(), P[:, 2].max()
    nohy = P[P[:, 2] - z0 < 0.05 * (z1 - z0)]
    return z1 - z0, Vector((nohy[:, 0].mean(), nohy[:, 1].mean(), z0))


def nacti(jmeno, vyska, priprava=None, nechat=None, emise=None):
    """GLB -> staticke meshe (viz nahore). priprava(arm, objekty): pozovani kostry (dostane armaturu a jeji
    meshe; meritko a stred jsou zmerene uz pred pozou). nechat(o): ktere meshe nechat (jinak vsechny krome
    obrysu). emise: sila emise materialu (anime modely sviti samy, ve scene by byly vybledle)."""
    pred = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(TU, jmeno + ".glb"))
    nove = [o for o in bpy.data.objects if o not in pred]
    for o in list(nove):
        if o.type == 'MESH' and ("Outline" in o.name or (nechat is not None and not nechat(o))):
            nove.remove(o); bpy.data.objects.remove(o, do_unlink=True)
    arm = next((o for o in nove if o.type == 'ARMATURE'), None)
    if arm is not None and arm.animation_data and arm.animation_data.action:
        # poza z akce (u college_girl je klidova poloha kosti rozbita, spravna je az snimek akce) -> natrvalo
        bpy.context.scene.frame_set(0)
        zaloha = {pb.name: pb.matrix_basis.copy() for pb in arm.pose.bones}
        arm.animation_data.action = None
        for pb in arm.pose.bones:
            pb.matrix_basis = zaloha[pb.name]
    bpy.context.view_layer.update()
    H, stred = _rozmery(nove)
    if priprava is not None:
        priprava(arm, [o for o in nove if o.type == 'MESH'])
        bpy.context.view_layer.update()
    meshe = _zapec(nove)
    T = Matrix.Scale(vyska / H, 4) @ Matrix.Translation(-stred)
    for o in meshe:
        o.data.transform(T)
        if emise is not None:
            for s in o.material_slots:
                b = s.material and s.material.node_tree and next((n for n in s.material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if b:
                    b.inputs["Emission Strength"].default_value = emise
    return meshe


def otoc_kost(arm, jmeno, osa, uhel):
    """otoci kost kolem jeji hlavy o uhel kolem osy ve svetovych souradnicich (deti jdou s ni)"""
    bpy.context.view_layer.update()
    pb = arm.pose.bones[jmeno]
    osa_a = (arm.matrix_world.inverted().to_3x3() @ Vector(osa)).normalized()
    h = pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ Matrix.Rotation(uhel, 4, osa_a) @ Matrix.Translation(-h) @ pb.matrix
    bpy.context.view_layer.update()


def hlava_kosti(arm, jmeno):
    bpy.context.view_layer.update()
    return arm.matrix_world @ arm.pose.bones[jmeno].head


def _hladke(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _rot(otoceni):
    """(osa, uhel) nebo hotova matice 3x3"""
    if isinstance(otoceni, (Matrix, np.ndarray)):
        return np.array(otoceni)
    osa, uhel = otoceni
    return np.array(Matrix.Rotation(uhel, 3, Vector(osa)))


def _pod(z, hrana, sirka):
    """1 pod hranou, 0 nad ni, hladce v pasu +-sirka"""
    return 1.0 - _hladke((z - (hrana - sirka)) / (2 * sirka))


def ohni_nohy(meshe, vyska, z_kycel, z_koleno, nohy, sirka=0.025, x_noh=0.13):
    """Ohne nohy staticke postavy. nohy: [(x_stred, stehno, lytko), ...] pro pravou (x < 0) a levou (x > 0) nohu,
    stehno a lytko jsou otoceni (osa, uhel) nebo matice 3x3: stehno kolem kycle, lytko pak jeste kolem kolena. Vysky jsou podily
    vysky postavy. x_noh: body dal od stredu nohy nez tolik (podil vysky) patri trupu (ruce, taska)."""
    H = vyska
    vse = np.vstack([_vrcholy(o) for o in meshe])
    pas = vse[np.abs(vse[:, 2] - z_kycel * H) < 0.02 * H]
    for o in meshe:
        v = _vrcholy(o)
        z = v[:, 2]
        stehno_vse = _pod(z, z_kycel * H, sirka * H)
        lytko_vse = _pod(z, z_koleno * H, sirka * H)
        novy = v.copy()
        vahy_trup = np.ones(len(v))
        x_mez = (nohy[0][0] + nohy[1][0]) / 2 if len(nohy) == 2 else None
        for i, (xs, otoc_s, otoc_l) in enumerate(nohy):
            # ktera noha: podle x od stredu mezi nohama, hladce
            if x_mez is None:
                strana = np.ones(len(v))
            else:
                t = _hladke((v[:, 0] - x_mez) / (0.03 * H) + 0.5)
                strana = t if xs > x_mez else 1 - t
            blizko = 1 - _hladke((np.abs(v[:, 0] - xs) - x_noh * H) / (0.03 * H))
            m = strana * blizko
            ys = pas[np.abs(pas[:, 0] - xs) < 0.06 * H][:, 1].mean() if len(pas) else 0.0
            K = np.array([xs, ys, z_kycel * H])
            Rs = _rot(otoc_s)
            kol = np.array([xs, ys, z_koleno * H])
            kol2 = Rs @ (kol - K) + K
            Rl = _rot(otoc_l)
            v_s = (v - K) @ Rs.T + K
            v_l = ((v_s - kol2) @ Rl.T) + kol2
            w_l = m * lytko_vse
            w_s = m * (stehno_vse - lytko_vse)
            novy += w_s[:, None] * (v_s - v) + w_l[:, None] * (v_l - v)
            vahy_trup -= w_s + w_l
        _zapis(o, novy)


def rozmery_siti(meshe):
    vse = np.vstack([_vrcholy(o) for o in meshe])
    return vse.min(axis=0), vse.max(axis=0), vse


def postav(meshe, matice):
    """postavi postavu do sceny: matice (4x4 v Blenderu) prevede jeji souradnice do sceny"""
    for o in meshe:
        o.data.transform(matice)
        for p in o.data.polygons:
            p.use_smooth = p.use_smooth
    return meshe


def sed(meshe, vyska, z_kycel, z_koleno, nohy_x, sedak=0.47, sirka=0.025, x_noh=0.13):
    """Posadi stojici postavu bez kostry: stehna dopredu, lytka skoro svisle dolu (chodidla kousek pred kolena).
    Uhel stehen vybere tak, aby pri sedu na sedaku vysokem `sedak` (m) dosla chodidla na zem. Vrati bod sedu
    (stred mezi kycli v x a y, nejnizsi bod zadku pod nimi v z) a uhel stehen."""
    puvodni = [_vrcholy(o) for o in meshe]
    vse = np.vstack(puvodni)
    pas = vse[np.abs(vse[:, 2] - z_kycel * vyska) < 0.02 * vyska]
    y_kycel = pas[:, 1].mean()
    # body stehen a zadku (podle puvodni vysky, bez lytek a bot, bez rukou a tasky u boku): na nich se sedi
    stehna = ((vse[:, 2] > (z_koleno + 0.06) * vyska) & (vse[:, 2] < (z_kycel + 0.06) * vyska)
              & (np.abs(vse[:, 0] - np.mean(nohy_x)) < 0.1 * vyska))
    nejlepsi = None
    for st in range(-90, -57, 2):
        for o, v in zip(meshe, puvodni):
            _zapis(o, v)
        ohni_nohy(meshe, vyska, z_kycel, z_koleno,
                  [(x, ((1, 0, 0), math.radians(st)), ((1, 0, 0), math.radians(-st - 5))) for x in nohy_x], sirka, x_noh)
        lo, hi, vse = rozmery_siti(meshe)
        okolo = vse[stehna & (np.abs(vse[:, 1] - y_kycel) < 0.12 * vyska)]          # pod zadkem, ne u kolen
        z_sed = okolo[:, 2].min()
        chyba = abs((z_sed - lo[2]) - sedak)
        if nejlepsi is None or chyba < nejlepsi[0]:
            nejlepsi = (chyba, st, z_sed)
    chyba, st, z_sed = nejlepsi
    for o, v in zip(meshe, puvodni):
        _zapis(o, v)
    ohni_nohy(meshe, vyska, z_kycel, z_koleno,
              [(x, ((1, 0, 0), math.radians(st)), ((1, 0, 0), math.radians(-st - 5))) for x in nohy_x], sirka, x_noh)
    return Vector((float(np.mean(nohy_x)), float(y_kycel), float(z_sed))), st, chyba


def stredy_nohou(meshe, vyska, z=0.42):
    """x stredu prave a leve nohy (u chodidel) a v dane vysce (podil vysky)"""
    _, _, vse = rozmery_siti(meshe)
    ch = vse[vse[:, 2] < 0.05 * vyska]; m = np.median(ch[:, 0])
    k = vse[np.abs(vse[:, 2] - z * vyska) < 0.01 * vyska]; mk = np.median(k[:, 0])
    return [(k[k[:, 0] < mk][:, 0].mean(), ch[ch[:, 0] < m][:, 0].mean(), ch[ch[:, 0] < m][:, 2].mean()),
            (k[k[:, 0] >= mk][:, 0].mean(), ch[ch[:, 0] >= m][:, 0].mean(), ch[ch[:, 0] >= m][:, 2].mean())]


def bod_sedu(meshe, vyska, y_kycel):
    """nejnizsi bod zadku pod kyclemi (u postav posazenych kostrou)"""
    lo, hi, vse = rozmery_siti(meshe)
    okolo = vse[(np.abs(vse[:, 1] - y_kycel) < 0.1 * vyska) & (vse[:, 2] > lo[2] + 0.15 * vyska) & (np.abs(vse[:, 0]) < 0.1 * vyska)]
    return Vector((0.0, float(y_kycel), float(okolo[:, 2].min()))), float(okolo[:, 2].min() - lo[2])


def otoc_cast(meshe, vyska, z_od, pivot, otoceni, sirka=0.012):
    """Otoci horni cast staticke postavy (vse nad vyskou z_od, podil vysky; hladce v pasu +-sirka) kolem bodu
    pivot (m) o otoceni (osa, uhel) nebo matici 3x3. Na hlavu: z_od u krku, ruce musi byt niz."""
    R = _rot(otoceni)
    p = np.array(pivot, dtype=float)
    for o in meshe:
        v = _vrcholy(o)
        w = 1.0 - _pod(v[:, 2], z_od * vyska, sirka * vyska)
        nove = (v - p) @ R.T + p
        _zapis(o, v + w[:, None] * (nove - v))


# ---------------------------------------------------------------- divky stojici samotne (fotky na prilozeni, naklad)
def _kost(arm, zacatek):
    return next(b.name for b in arm.pose.bones if b.name.startswith(zacatek))


def ruce_dolu(arm, meshe):
    """modely v pozici T (galaxia): ruce podel tela, kousek dopredu, lokty mirne pokrcene"""
    for st in ("L", "R"):
        zn = 1 if st == "L" else -1
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_UpperArm"), (0, 1, 0), zn * math.radians(76))
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_UpperArm"), (1, 0, 0), math.radians(-6))
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_LowerArm"), (1, 0, 0), math.radians(-14))


def ruce_dolu_college(arm, meshe):
    """college_girl (pozice T ze snimku akce): ruce podel tela"""
    for st, zn in (("L", 1), ("R", -1)):
        otoc_kost(arm, _kost(arm, f"Shoulder_{st}_"), (0, 1, 0), zn * math.radians(76))
        otoc_kost(arm, _kost(arm, f"Shoulder_{st}_"), (1, 0, 0), math.radians(-6))
        otoc_kost(arm, _kost(arm, f"Elbow_{st}_"), (1, 0, 0), math.radians(-14))


def divka_a(o):
    """z college_girl jen prvni divka na kostre (ostatni tri pryc)"""
    if o.parent is None or o.parent.type != 'ARMATURE':
        return False
    dg = bpy.context.evaluated_depsgraph_get(); e = o.evaluated_get(dg); me_ = e.to_mesh()
    x = sum((o.matrix_world @ v.co).x for v in me_.vertices) / max(1, len(me_.vertices)); e.to_mesh_clear()
    return x < -1.0


def nacti_stojici(jmeno, vyska, poza="stoji"):
    """divka stojici (poza "stoji" jak je v modelu, "ruce_dolu" z pozice T) jako staticke meshe, chodidla v 0, celem k -y;
    u kazdeho modelu s jeho upravami (u college_girl jen prvni divka, u galaxie bez koule, anime bez emise)"""
    priprava = (ruce_dolu_college if "college" in jmeno else ruce_dolu) if poza == "ruce_dolu" else None
    nechat = (lambda o: "Icosphere" not in o.name) if "galaxia" in jmeno else divka_a if "college" in jmeno else None
    return nacti(jmeno, vyska, priprava=priprava, nechat=nechat, emise=0.0 if "anime" in jmeno else None)


# ---------------------------------------------------------------- divky sedici (na lavicky u budov, pozy jako u sochy)
def sed_galaxia(arm, meshe):
    """galaxia: sed kostrou, ruce podel tela a predlokti na stehna"""
    for st in ("L", "R"):
        zn = 1 if st == "L" else -1
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_UpperLeg"), (1, 0, 0), math.radians(-72))     # kolena niz, at dojde na zem
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_LowerLeg"), (1, 0, 0), math.radians(67))
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_UpperArm"), (0, 1, 0), zn * math.radians(72))
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_UpperArm"), (1, 0, 0), math.radians(-18))
        otoc_kost(arm, _kost(arm, f"J_Bip_{st}_LowerArm"), (1, 0, 0), math.radians(-55))


#: modely bez kostry, ktere sedi ohnutim nohou v siti: vyska, kycle a kolena (podil vysky)
SEDICI = {"character_people_girl_001": (1.68, 0.49, 0.28), "anime_girl": (1.6, 0.52, 0.285)}


def sedici(jmeno):
    """divka posazena na sedak 0,47 m jako u sochy: (meshe, kotva), kotva = bod sedu (stred mezi kycli, zadek dole);
    galaxia kostrou, ostatni ohnutim nohou (sed())"""
    if "galaxia" in jmeno:
        g = nacti(jmeno, 1.58, priprava=sed_galaxia, nechat=lambda o: "Icosphere" not in o.name)
        return g, bod_sedu(g, 1.58, 0.0)[0]
    vyska, z_kycel, z_koleno = SEDICI[jmeno]
    m = nacti(jmeno, vyska, emise=0.0 if "anime" in jmeno else None)
    nohy = stredy_nohou(m, vyska)
    kotva, _, _ = sed(m, vyska, z_kycel, z_koleno, [nohy[0][1], nohy[1][1]])
    return m, kotva
