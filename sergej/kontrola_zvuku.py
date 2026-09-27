# -*- coding: utf-8 -*-
# Kontrola zvuku: z rozbaleneho GRF (yagl -d) projde callback 0x33 tak, jak ho vola hra, tik po tiku:
# stani, rozjezd na 100 km/h, jizda, brzdeni, stani. Kazdych 16 tiku (tick_counter vozidla) prijde
# udalost 7 (jede) nebo 8 (stoji nebo brzdi), var 0x0A je citac tiku hry (16 bitu). Hlida, ze kousky
# motoru jdou presne po perioda_tiku, ze pasmo sedi na rychlost a co udela odjezd, tunel a porucha.
#   python3 kontrola_zvuku.py <rozbaleny adresar sprites> <jmeno.yagl> [zvuky.json]
import sys, os, re, json

SD, YG = sys.argv[1], sys.argv[2]
ZJ = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "zvuky", "zvuky.json")
text = open(os.path.join(SD, YG) if not os.path.isabs(YG) and not os.path.exists(YG) else YG, encoding="utf-8", errors="replace").read()

# Action11: vlastni zvuky od 0x49 v poradi souboru
blok = text[text.index("sound_effects"):]
blok = blok[:blok.index("\n}")]
ZVUKY = {0x49 + i: os.path.basename(f) for i, f in enumerate(re.findall(r'binary\("([^"]+)"\)', blok))}

# switche: id -> (vyraz, [(od, do, cil)], default)
SW = {}
for m in re.finditer(r"switch<Trains, 0x([0-9A-Fa-f]+), (\w+)>[^\n]*\n\{(.*?)\n\}", text, re.S):
    telo = m.group(3)
    vyraz = re.search(r"expression:\s*\{(.*?)\};", telo, re.S).group(1)
    rozsahy = []
    for r in re.finditer(r"0x([0-9A-Fa-f]+)(?:\.\.0x([0-9A-Fa-f]+))?:\s*0x([0-9A-Fa-f]+);", re.search(r"ranges:\s*\{(.*?)\};", telo, re.S).group(1)):
        od = int(r.group(1), 16); rozsahy.append((od, int(r.group(2), 16) if r.group(2) else od, int(r.group(3), 16)))
    SW[int(m.group(1), 16)] = ([v.strip() for v in vyraz.split(";") if v.strip()], rozsahy,
                               int(re.search(r"default:\s*0x([0-9A-Fa-f]+);", telo).group(1), 16))
# Action03: hlava lokomotivy -> prvni switch
HLAVA = {}
for m in re.finditer(r"feature_graphics<Trains>.*?default_set_id: 0x([0-9A-Fa-f]+);.*?feature_ids: \[ 0x([0-9A-Fa-f]+) \]", text, re.S):
    HLAVA[int(m.group(2), 16)] = int(m.group(1), 16)

def spocti(vyraz, prom):
    v = {}
    for radek in vyraz:
        m = re.fullmatch(r"(value\d) = variable\[0x([0-9A-Fa-f]+)\] & 0x([0-9A-Fa-f]+)(?: ([/%]) 0x([0-9A-Fa-f]+))?", radek)
        if m:
            x = prom[int(m.group(2), 16)] & int(m.group(3), 16)
            if m.group(4): x = x // int(m.group(5), 16) if m.group(4) == "/" else x % int(m.group(5), 16)
            v[m.group(1)] = x; continue
        m = re.fullmatch(r"(value\d) = UnsignedMod\((value\d), (value\d)\)", radek)
        if m: v[m.group(1)] = v[m.group(2)] % v[m.group(3)]; continue
        raise ValueError("neznamy vyraz: " + radek)
    return v["value1"]

def callback(hlava, prom):
    """vrati ('zvuk', jmeno) / ('ticho', None) / ('selhal', None)"""
    cil = HLAVA[hlava]
    for _ in range(50):
        if cil == 0x7FFF: return ("selhal", None)            # GROUPID_CALLBACK_FAILED: hra pusti svuj zvuk
        if cil & 0x8000:
            vysl = cil & 0x7FFF
            if vysl in ZVUKY: return ("zvuk", ZVUKY[vysl])
            return ("ticho", None) if vysl >= 0x49 else ("zvuk", f"zakladni {vysl:#x}")
        if cil not in SW: return ("selhal", None)            # grafika misto vysledku = callback selhal
        vyraz, rozsahy, default = SW[cil]
        x = spocti(vyraz, prom)
        cil = next((c for od, do, c in rozsahy if od <= x <= do), default)
    raise RuntimeError("zacykleny retez")

ZV = json.load(open(ZJ))
chyby = 0
for natier, hlava in (("zeleny", 0x0100), ("cerveny", 0x0110)):
    if hlava not in HLAVA: continue
    z = ZV[natier]; P = z["perioda_tiku"]
    def pasmo(kmh):
        for i, p in enumerate(z["jizda"]):
            if p["do_kmh"] is None or kmh <= p["do_kmh"]: return i
    zak = lambda u, v=0: {0x0C: 0x33, 0x10: u, 0x0A: 0, 0xB4: v, 0x1A: 0xFFFFFFFF}
    print(f"== {natier} (0x{hlava:04X})")
    for u, popis in ((1, "odjezd a zahoukej"), (2, "tunel"), (3, "porucha"), (9, "nakladka")):
        print(f"   udalost {u} ({popis}): {callback(hlava, zak(u))}")
    # jizda tik po tiku; ruzne faze citace vozidla a hry, jednou i pres preteceni 16 bitu
    for t0, c0 in ((0, 0), (5, 1000), (11, 65536 - 3000)):
        prehrano = []                                         # (tik, kmh, soubor)
        TIKY = 20000
        for t in range(TIKY):
            s = t * 0.027
            kmh = 0 if s < 30 else min(100, (s - 30) * 1.7) if s < 450 else max(0, 100 - (s - 450) * 5)
            brzdi = 450 <= s
            if (t0 + t) % 16: continue
            u = 7 if kmh > 0 and not brzdi else 8
            p = zak(u, int(kmh)); p[0x0A] = (c0 + t) & 0xFFFF
            druh, f = callback(hlava, p)
            if druh == "zvuk": prehrano.append((t, int(kmh), f, u))
        odstupy = [b[0] - a[0] for a, b in zip(prehrano, prehrano[1:])]
        spatne_odstupy = [o for o in odstupy if o != P]
        spatne_pasmo = [(t, v, f) for t, v, f, u in prehrano if u == 7 and f not in z["jizda"][pasmo(v)]["zvuky"]]
        spatne_stani = [(t, f) for t, v, f, u in prehrano if u == 8 and f not in z["stani"]]
        print(f"   faze {t0:2d}/{c0:5d}: {len(prehrano)} kousku, odstupy {sorted(set(odstupy))} tiku"
              f"{' (jiny ' + str(spatne_odstupy) + ' pri preteceni citace)' if spatne_odstupy else ''}, "
              f"spatne pasmo {len(spatne_pasmo)}, spatny volnobeh {len(spatne_stani)}")
        # jeden jiny odstup smi byt jen pri preteceni citace hry (65536 neni nasobek periody)
        chyby += len(spatne_pasmo) + len(spatne_stani) + int(len(spatne_odstupy) > 1 or (bool(spatne_odstupy) and c0 < 60000))
        if t0 == 0:
            ukazka = {}
            for t, v, f, u in prehrano:
                klic = f.rsplit("_", 1)[0]
                if klic not in ukazka: ukazka[klic] = (round(t * 0.027, 1), v)
            print("   prvni kousek kazdeho druhu (s, km/h):", ", ".join(f"{k} {s}s/{v}" for k, (s, v) in ukazka.items()))
print("ZVUKY V PORADKU" if not chyby else f"CHYB: {chyby}")
