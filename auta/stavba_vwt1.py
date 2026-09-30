#!/usr/bin/env python3
# Nova verze GRF VW T1, Skoda 1203 a TAZ (grf_id MAX\x08), z rozbaleneho VWT1-S1203-clanky-oba-na-stred:
#  1. prekladova tabulka 221 kodu: za FREE pripsano 125 kodu ze vzoru (prekladova-tabulka-vzor.yagl) v jeho poradi,
#     stara cisla plati
#  2. naklady podle hrace 30. 9.: VW T1 je vzor pro dodavky, bedna zvlast, valniky podle barvy kupy, lide 2 / 5 / 8
#  3. novy valnik 0x8A se zelenou kupou marihuany (kupa brambor z 0x88 prebarvena, plna i nakladaci)
#  4. neviditelny clanek: cumak delky 2 + auto delky 8, zadni naraznik uz se nepripojuje (poradi kresleni, CUMAK.md)
#  5. skutecne udaje: rok uvedeni, vykon, max. rychlost, vaha (Pajda karavan 130 km/h a lepsi motor podle hrace)
# Pouziti: python3 stavba_vwt1.py <vstup.yagl> <list.png> <zelena.pkl> <kody.json> <slozka sprites> <jmeno>
#   vznikne <slozka sprites>/<jmeno>.yagl, list se zelenou kupou a <slozka sprites>/../<jmeno>-souhrn.json
import json, os, pickle, re, sys
from PIL import Image

VSTUP, LIST, ZELENA, KODY, VYSTUP, JMENO = sys.argv[1:7]
t = open(VSTUP, encoding="utf-8").read()
kody = json.load(open(KODY, encoding="utf-8"))
TABULKA = kody["grf"] + kody["nove"]                   # 96 hracovych (do FREE) + 125 ze vzoru = 221
assert TABULKA[0x5F] == "FREE" and len(TABULKA) == 221 and len(TABULKA) == len(set(TABULKA)) + 1  # CERA je 2x
SLOT = {}
for i, k in enumerate(TABULKA):
    SLOT.setdefault(k, i)                              # CERA: prvni vyskyt 0x4B (0x5A zustava v seznamu VW T1)

# ---------------- naklady
LIDE = ["PASS", "TOUR", "OTI1", "OTI2", "STUD", "WORK", "PRIS", "YETI", "YETY", "PLAY"]   # vsichni lide v tabulce
LIDE_2 = ["PASS", "WORK", "PRIS", "YETI", "YETY"]      # dodavky, valniky, plachty: pasazeri, delnici, vezni
LIDE_BUS = ["PASS", "TOUR", "OTI1", "OTI2", "STUD", "WORK", "PRIS", "YETI", "YETY", "PLAY"]
LIDE_KARAVAN = ["PASS", "STUD"]                        # studentky a normalni cestujici (bez GRF prumyslu)
BEDNA = ["GOOD", "FMSP", "ENSP", "MNSP", "TOYS", "BATT", "HWAR", "VPTS", "MPTS", "PACK"]
NEZNAME = ["CRAN", "LFEQ", "SCPR", "STTP", "SWRP", "TIN_", "WDCH"]   # nevime co to je: pod plachtu
VW_PRIPSAT = ["FRVG", "MARI", "WINE", "BAKE", "FLOU", "OYST", "ENUM", "RSGR", "PCL_", "PRNT", "MPAR", "PPAR",
              "LEAT", "LETH", "PLAS", "PLST", "RUBR", "CHEM", "WORK", "PRIS", "YETI", "YETY",
              "MILK", "EOIL", "SALT", "KAOL", "QLME", "SASH", "FERT", "CBLK", "PLNT"]
VALNIKY = {0x83: ["WOOD", "TWOD"], 0x84: ["COAL", "COKE", "MNO2"],
           0x85: ["CLAY", "PEAT", "BIOM", "AORE", "IORE", "CORE", "COCO"],
           0x86: ["SAND", "SULP", "GRAI", "WHEA", "MAIZ", "CERE"],
           0x87: ["GRVL", "LIME", "SLAG", "SCMT", "SCRP", "NKOR", "PORE", "POTA", "PHOS"],
           0x88: ["TATO", "BEAN", "CASS", "SGBT"], 0x8A: ["MARI", "HOPS"]}   # zeleny: i chmel (hrac 30. 9.)

def cisla(seznam):
    return sorted({SLOT[k] for k in seznam})

def seznam_z_grf(vid):
    m = re.search(rf"^properties<RoadVehicles, 0x{vid:04X}>.*?always_refittable_cargos: \[([^\]]*)\]", t, re.M | re.S)
    return [int(x, 16) for x in m.group(1).split()]

vw = seznam_z_grf(0x80)
assert vw == seznam_z_grf(0x81), "VW T1 obe velikosti maji mit stejny seznam"
VW = sorted(set(vw) | set(cisla(VW_PRIPSAT)))          # hracuv seznam VW T1 + pripsane, vynechane zustava vynechane
BEDNA_C = set(cisla(BEDNA))
DODAVKA = [c for c in VW if c not in BEDNA_C]          # modre dodavky bez bedny: jako VW T1 bez veci z bedny
PLACHTA = sorted(set(DODAVKA) | set(cisla(NEZNAME)))   # plachta: jako dodavka a navic nezname kody
S_BEDNOU = sorted(BEDNA_C | set(cisla(LIDE_2)))        # dodavka bedna, plachta bedna, valnik bedna

# druh: skupina skutecnych udaju; naklady; lidi; vychozi naklad (s nim se auto koupi)
AUTA = {
    0x80: ("vw", VW, 2, "GOOD"), 0x81: ("vw", VW, 2, "GOOD"),
    0x82: ("karavan", cisla(["MARI", "CIGR", "TBCO", "BEER", "WINE"] + LIDE_KARAVAN), 5, "PASS"),
    **{v: ("taz1203", cisla(k + LIDE_2), 2, k[0]) for v, k in VALNIKY.items()},
    0x89: ("taz1203", S_BEDNOU, 2, "GOOD"),
    0x90: ("taz1203", S_BEDNOU, 2, "GOOD"), 0x91: ("taz1203", PLACHTA, 2, "MAIL"), 0x92: ("taz1203", PLACHTA, 2, "MAIL"),
    0x93: ("taz1500", cisla(LIDE_BUS), 8, "PASS"), 0x94: ("taz1500", cisla(LIDE_BUS), 8, "PASS"),
    0x95: ("taz1500", DODAVKA, 2, "MAIL"), 0x96: ("taz1500", S_BEDNOU, 2, "GOOD"), 0x97: ("taz1500", DODAVKA, 2, "MAIL"),
}
for v, (_, sez, _, vych) in AUTA.items():
    assert SLOT[vych] in sez, (hex(v), vych)
    assert SLOT["FREE"] not in sez

# ---------------- skutecne udaje (zdroje v souhrnu)
# vykon po 10 k (hra jinak neumi), vaha po 1/4 t, rychlost: vlastnost 0x08 po 0,5 km/h do 127 km/h, nad to 0x15 po 2 km/h
# Pajda karavan: 130 km/h podle hrace (dva svedci, Shell V-Power) a lepsi motor, 110 k, aby na 130 dojel i nalozeny;
# hra se nemeni, odpor vzduchu zustava vychozi (hra ho pocita z max. rychlosti)
UDAJE = {
    "vw":      dict(uvedeni="1950/3/8",   vykon_k=25,  kmh=80,  vaha_kg=975),
    "karavan": dict(uvedeni="1968/11/20", vykon_k=110, kmh=130, vaha_kg=1170),
    "taz1203": dict(uvedeni="1973/4/1",   vykon_k=47,  kmh=90,  vaha_kg=1170),
    "taz1500": dict(uvedeni="1988/1/1",   vykon_k=57,  kmh=110, vaha_kg=1260),
}

def rychlost_ve_hre(vykon_hp, kmh, vaha_t, dilu=2):
    """nejvyssi rychlost na rovine pri realistickem zrychleni (vzorce z ground_vehicle.cpp: sila z vykonu, cep
    10/t, valivy odpor 75 * (128 + v) / 128 na tunu, vzduch 6 * odpor * v^2 / 1000, vychozi odpor 2048 / max.
    rychlost a k nemu 3 * odpor * dilu / 20)"""
    a = max(2048 // kmh, 1)
    c = a + (3 * a * dilu) // 20
    return max(v for v in range(1, kmh + 1)
               if vykon_hp * 746 * 18 / (5 * v) >= 10 * vaha_t + vaha_t * 75 * (128 + v) / 128 + 6 * c * v * v / 1000)

for d in UDAJE.values():
    d["vykon_10"] = (d["vykon_k"] + 5) // 10           # 25 -> 3, 47 -> 5, 57 -> 6, 110 -> 11
    d["vaha_q"] = round(d["vaha_kg"] / 250)            # 975 -> 4, 1170 -> 5, 1260 -> 5
    d["ve_hre_kmh"] = [rychlost_ve_hre(d["vykon_10"] * 10, d["kmh"], t_) for t_ in (d["vaha_q"] // 4, d["vaha_q"] // 4 + 1)]

# ---------------- zaznamy
zaznamy = re.split(r"\n(?=// Record #\d+\n)", t)
hlava, zaznamy = zaznamy[0], [z.split("\n", 1)[1] for z in zaznamy[1:]]   # bez radku "// Record #N"

def najdi(vzor):
    i = [n for n, z in enumerate(zaznamy) if re.search(vzor, z, re.M)]
    assert len(i) == 1, (vzor, i)
    return i[0]

def seznam(c):
    return "[ " + " ".join(f"0x{x:02X}" for x in c) + " ]" if c else "[ ]"

def nastav(z, jmeno, hodnota):
    """prepise radek vlastnosti, nebo ho prida na konec instance"""
    radek = f"        {jmeno}: {hodnota};"
    if re.search(rf"^        {jmeno}: [^\n]*;$", z, re.M):
        return re.sub(rf"^        {jmeno}: [^\n]*;$", lambda m: radek, z, count=1, flags=re.M)
    k = z.rindex("\n    }\n}")
    return z[:k] + "\n" + radek + z[k:]

def switch(sid, popis, vyraz, rozsahy, vychozi):
    r = [f"switch<RoadVehicles, 0x{sid:02X}, PrimaryDWord> // Action02 variable, {popis}", "{", "    expression:", "    {",
         f"        {vyraz}", "    };", "    ranges:", "    {"]
    r += [f"        0x{a:08X}: 0x{b:04X};" for a, b in rozsahy]
    return "\n".join(r + ["    };", f"    default: 0x{vychozi:04X};", "}"])

def akce3(eid, vychozi, naklady):
    r = ["feature_graphics<RoadVehicles> // Action03", "{", "    livery_override: false;",
         f"    default_set_id: 0x{vychozi:04X};", f"    feature_ids: [ 0x{eid:04X} ];", "    cargo_types:", "    {",
         "        // <cargo_type>: <cargo_id>;"]
    r += [f"        0x{a:02X}: 0x{b:04X};" for a, b in naklady]
    return "\n".join(r + ["    };", "}"])

# ---------------- novy valnik 0x8A: kopie bloku 0x88 (sady, vlastnosti, jmeno, ikona, auto, pruhledny cumak, switche)
zel = pickle.load(open(ZELENA, "rb"))                  # {(sada, smer): (rgba, maska, sprite)}
i88 = najdi(r"^properties<RoadVehicles, 0x0088>")
blok = [z for z in zaznamy[i88 - 2:i88 + 11]]
assert "sprite_sets<" in blok[0] and "0xFF>" in blok[1] and "feature_ids: [ 0x0088 ]" in blok[12]
dalsi_id = [max(int(x, 16) for x in re.findall(r"sprite_id<(0x[0-9A-F]+)>", t)) + 1]
LIST_ZEL = f"{JMENO}-zelena-kupa.png"
bunky = []                                             # (sada, smer) -> pozice na novem listu

def nove_id():
    i = dalsi_id[0]; dalsi_id[0] += 1
    return i

def prepis_sprity(z, zelena_sada=None):
    """kazdy sprite dostane nove cislo; u zelene sady i obrazek z noveho listu"""
    sady = re.split(r"(?=    sprite_set // )", z)
    out = []
    for si, s in enumerate(sady):
        smer = [-1]
        def jeden(m):
            smer[0] += 1
            w, h, xo, yo, soubor, x, y = m.group(2, 3, 4, 5, 6, 7, 8)
            sada = si - 1                              # sady[0] je hlavicka zaznamu
            if zelena_sada is not None and sada in zelena_sada:
                rgba, _, sp = zel[(sada, smer[0])]
                assert (sp["w"], sp["h"], sp["xo"], sp["yo"]) == (int(w), int(h), int(xo), int(yo))
                bunky.append(((sada, smer[0]), rgba))
                soubor, x, y = LIST_ZEL, "{X%d}" % (len(bunky) - 1), "{Y%d}" % (len(bunky) - 1)
            return (f"sprite_id<0x{nove_id():08X}>\n        {{\n            [{w}, {h}, {xo}, {yo}], zin4, c32bpp | chunked, "
                    f"\"{soubor}\", [{x}, {y}];")
        out.append(re.sub(r"sprite_id<(0x[0-9A-F]+)>\n        \{\n            \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\], "
                          r"zin4, c32bpp \| chunked, \"([^\"]+)\", \[(\d+), (\d+)\];", jeden, s))
    return "".join(out)

novy = list(blok)
novy[0] = prepis_sprity(blok[0], zelena_sada={1, 2})   # sada 0 prazdny valnik (stejny obrazek), 1 plna, 2 nakladani
novy[2] = blok[2].replace("0x0088", "0x008A")
novy[3] = blok[3].replace("0x0088", "0x008A").replace('"TAZ 1203 valnik zluta brambor"', '"TAZ 1203 valnik zelena marihuana"')
assert "zelena marihuana" in novy[3]
novy[4] = prepis_sprity(blok[4])                       # ikona (vsechny valniky maji stejnou prazdnou)
novy[6] = blok[6].replace("0x00A8", "0x00AA")
novy[7] = blok[7].replace("0x00A8", "0x00AA")
novy[8] = prepis_sprity(blok[8])                       # pruhledny cumak
novy[10] = blok[10].replace("0x80A8", "0x80AA")
novy[12] = blok[12].replace("0x0088", "0x008A")
i89 = najdi(r"^properties<RoadVehicles, 0x0089>")
zaznamy[i89 + 11:i89 + 11] = novy                      # hned za valnik bedna
assert zaznamy[i89 + 10].startswith("feature_graphics") and "0x0089" in zaznamy[i89 + 10]

# list se zelenou kupou: 8 sloupcu, mezera 2 px
sirka = max(a.shape[1] for _, a in bunky) + 4; vyska = max(a.shape[0] for _, a in bunky) + 4
list_zel = Image.new("RGBA", (8 * sirka, ((len(bunky) + 7) // 8) * vyska), (0, 0, 0, 0))
pozice = []
for n, (_, a) in enumerate(bunky):
    x, y = (n % 8) * sirka + 2, (n // 8) * vyska + 2
    list_zel.paste(Image.fromarray(a, "RGBA"), (x, y))
    pozice.append((x, y))
list_zel.save(os.path.join(VYSTUP, LIST_ZEL))
for z_i in range(len(zaznamy)):
    if "{X" in zaznamy[z_i]:
        zaznamy[z_i] = re.sub(r"\{X(\d+)\}", lambda m: str(pozice[int(m.group(1))][0]), zaznamy[z_i])
        zaznamy[z_i] = re.sub(r"\{Y(\d+)\}", lambda m: str(pozice[int(m.group(1))][1]), zaznamy[z_i])

# ---------------- prekladova tabulka
i_tab = najdi(r'cargo_translation_table: "PASS"')
stare = re.findall(r'cargo_translation_table: "([^"]+)"', zaznamy[i_tab])
assert stare == kody["grf"], "tabulka v GRF neni ta, ze ktere se pocitalo"
r = ["properties<GlobalSettings, 0x0000> // Action00", "{"]
for i, k in enumerate(TABULKA):
    r += [f"    // instance_id: 0x{i:04X}", "    {", f'        cargo_translation_table: "{k}";', "    }"]
zaznamy[i_tab] = "\n".join(r + ["}"])

# ---------------- kazde auto
souhrn = {"tabulka": TABULKA, "udaje": UDAJE, "auta": {}}
for nos in sorted(AUTA):
    druh, sez, lidi, vych = AUTA[nos]
    auto = nos + 0x20
    d = UDAJE[druh]
    i = najdi(rf"^properties<RoadVehicles, 0x{nos:04X}>")
    assert zaznamy[i - 1].startswith("sprite_groups<RoadVehicles, 0xFF>")
    assert zaznamy[i + 4].startswith(f"properties<RoadVehicles, 0x{auto:04X}>")
    assert zaznamy[i + 5].startswith("feature_graphics") and f"[ 0x{auto:04X} ]" in zaznamy[i + 5]
    assert zaznamy[i + 8].startswith("switch<RoadVehicles, 0xF0") and zaznamy[i + 9].startswith("switch<RoadVehicles, 0xF1")
    assert zaznamy[i + 10].startswith("feature_graphics") and f"[ 0x{nos:04X} ]" in zaznamy[i + 10]
    lide_c = [c for c in sez if TABULKA[c] in LIDE]
    vychozi_lide = vych in LIDE
    valnik = nos in VALNIKY or nos == 0x89
    # cumak: delka 2 (8 - 6), clanky a kapacita osob, novy vypocet kapacity (nezavisi na vychozim nakladu),
    # skutecne udaje
    z = zaznamy[i]
    for jm, h in [("shorten_vehicle", "0x06"), ("callback_flags_mask", "0x18"), ("miscellaneous_flags", "0x60"),
                  ("always_refittable_cargos", seznam(sez)), ("cargo_type", f"0x{SLOT[vych]:02X}"),
                  ("long_introduction_date", f"date({d['uvedeni']})"), ("power_10_hp", f"0x{d['vykon_10']:02X}"),
                  ("weight_quarter_tons", f"0x{d['vaha_q']:02X}"), ("cargo_capacity", "0x01")]:
        z = nastav(z, jm, h)
    if d["kmh"] * 2 <= 255:
        z = nastav(z, "speed_2_kmh", f"0x{d['kmh'] * 2:02X}")
    else:
        z = nastav(z, "speed_2_kmh", "0xFF")
        z = nastav(z, "speed_half_kmh", f"0x{d['kmh'] // 2:02X}")   # jednotka 2 km/h
    zaznamy[i] = z
    # viditelne auto: delka 8, kapacita osob callbackem
    z = zaznamy[i + 4]
    for jm, h in [("shorten_vehicle", "0x00"), ("callback_flags_mask", "0x08"), ("miscellaneous_flags", "0x60"),
                  ("always_refittable_cargos", seznam(sez)), ("cargo_type", f"0x{SLOT[vych]:02X}"),
                  ("cargo_capacity", "0x01")]:
        z = nastav(z, jm, h)
    zaznamy[i + 4] = z
    # lide na valniku sedi v kabine: prazdny valnik (sada 0), i pri nakladani
    if valnik:
        zaznamy[i - 1] += ("\nsprite_groups<RoadVehicles, 0xFD> // Action02 basic, lide: prazdny valnik\n{\n"
                           "    primary_spritesets: [ 0x0000 ];\n    secondary_spritesets: [ 0x0000 ];\n}")
    g_lide = 0xFD if valnik else 0xFF
    auto_sw = [switch(0xFC, f"auto s lidmi: kapacita {lidi - 1}", "value1 = variable[0x0C] & 0x0000FFFF;",
                      [(0x15, 0x8000 | (lidi - 1))], g_lide)]
    auto_a3 = [(c, 0xFC) for c in lide_c]
    if vychozi_lide:                                   # v nakupu je vychozi naklad lide: kapacita i tam
        auto_sw.append(switch(0xFB, f"auto v nakupu: kapacita {lidi - 1}", "value1 = variable[0x0C] & 0x0000FFFF;",
                              [(0x15, 0x8000 | (lidi - 1))], 0xFF))
        auto_a3.append((0xFF, 0xFB))
    zaznamy[i + 5] = "\n".join(auto_sw) + "\n" + akce3(auto, 0xFF, auto_a3)
    # cumak: clanek 1 = auto, dal nic (zadni naraznik 0x00C0 se nepripojuje, jeho definice zustava kvuli starym hram)
    assert f"0x00000002: 0x80C0;" in zaznamy[i + 8]
    zaznamy[i + 8] = zaznamy[i + 8].replace("        0x00000002: 0x80C0;\n", "")
    nakup = ([(0x15, 0x8001)] if vychozi_lide else []) + [(0x16, 0xF0)]
    zaznamy[i + 9] += "\n" + "\n".join([
        switch(0xF3, "cumak s lidmi: kapacita 1, clanky", "value1 = variable[0x0C] & 0x0000FFFF;",
               [(0x15, 0x8001), (0x16, 0xF0)], 0xF2),
        switch(0xF4, "cumak v nakupu: clanky" + (", kapacita 1" if vychozi_lide else "") + ", ikona",
               "value1 = variable[0x0C] & 0x0000FFFF;", nakup, 0xFE)])
    zaznamy[i + 10] = akce3(nos, 0xF1, [(c, 0xF3) for c in lide_c] + [(0xFF, 0xF4)])
    jm = re.search(r'"([^"]*)"', zaznamy[i + 1]).group(1)
    souhrn["auta"][f"0x{nos:02X}"] = {"jmeno": jm, "druh": druh, "lidi": lidi, "vychozi": vych,
                                      "naklady": [TABULKA[c] for c in sez]}
    print(f"0x{nos:02X} {jm:34s} {druh:8s} nakladu {len(sez):3d} lidi {lidi} vychozi {vych} lide {[TABULKA[c] for c in lide_c]}")

text = hlava + "".join(f"\n// Record #{n + 1}\n{z}" for n, z in enumerate(zaznamy))
if not text.endswith("\n"):
    text += "\n"
open(os.path.join(VYSTUP, f"{JMENO}.yagl"), "w", encoding="utf-8").write(text)
json.dump(souhrn, open(os.path.join(VYSTUP, "..", f"{JMENO}-souhrn.json"), "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("udaje (vykon/10 k, vaha/4 t, km/h, ve hre prazdne a +1 t)",
      {k: (v["vykon_10"], v["vaha_q"], v["kmh"], v["ve_hre_kmh"]) for k, v in UDAJE.items()})
print("zaznamu", len(zaznamy), "novych spritu", dalsi_id[0] - 0x408, "list", list_zel.size)
