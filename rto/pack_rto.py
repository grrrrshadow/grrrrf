# -*- coding: utf-8 -*-
# Balic autobusu Skoda 706 RTO: z fotek (render_rto.py) udela spritesheety (zin4 i zin8) a cely GRF v yaglu.
#   python3 pack_rto.py <mala|velka> <adresar s fotkami> <vystupni adresar>
# Fotky: <adresar>/<mala|velka>_<nater>/d0-d7.png + kotvy.json a k nim <totez>_zin8 (ZIN=8, dvojnasobny ram).
# Autobus je dlouhy 10,81 m = 11,7 osmin v mericku CZTR (12,2 px/m), 14,05 osmin u BRYLI, a hra ma clanek nejvys 8/8:
# kupovane cislo je neviditelny cumak (mala 4/8, velka 7/8, viz auta/CUMAK.md), drzi jmeno, cenu a obrazek v nakupu,
# viditelny autobus je druhy clanek 8/8 (obrazek cele delky kotveny na zem pod stredem autobusu, jako velka vejtraska).
# Kotvy a pruh na silnici CZTR jsou stejne jako v pack_v3s.py. Jen cestujici (PASS), 41 mist (KAR 41+2 k sezeni).
import os, sys, json, math, re
import numpy as np
from PIL import Image

VEL, FOTKY, VYSTUP = sys.argv[1:4]
TU = os.path.dirname(os.path.abspath(__file__))
# Verze: kazde sestaveni pro hrace o jednu vys, je ve jmenu souboru i v Action14 (VRSN).
# 1 prvni autobus, cerveno-kremovy linkovy (KAR), zin4 i zin8
VERZE = 1
JMENO = {"mala": "Skoda_706_RTO", "velka": "Skoda_706_RTO_BRYLE"}[VEL] + f"-v{VERZE}"
GRF_ID = {"mala": "MAXf", "velka": "MAXg"}[VEL]
PNG32 = f"{JMENO}-32bpp-zin4.png"; PNG8 = f"{JMENO}-8bpp.png"; PNG32_8 = f"{JMENO}-32bpp-zin8.png"
NATERY = ["cervena"]
CUMAK = {"mala": 4, "velka": 7}[VEL]              # delka neviditelneho cumaku v osminach
KAPACITA = 41

# ---------------------------------------------------------------- kotvy (jako pack_v3s.py)
def kotva_zrcadlova(d):
    """kotva spritu proti bodu na zemi pod stredem auta, px zin4 (vodorovne, svisle), zrcadlove srovnana"""
    a = math.radians(45 * d)
    return 10.0 * math.sin(a), -20.8 - 0.7 * math.cos(a)

# Pruh na silnici CZTR (viz pack_v3s.py): hra vede auto v pruhu na 9 (SV, JV) nebo 5 (JZ, SZ) jednotkach dlazdice
# a kresli ho na poloha + (-2, -1) (SV, JZ) nebo (-1, -2) (JV, SZ). Stred pruhu CZTR RT14: podel X 10,2 a 6,33,
# podel Y 9,66 a 5,79. smer: (osa napric, pruh hry, posun kresleni napric, stred pruhu CZTR)
PRUH_CZTR = {1: ("y", 9, -1, 10.2), 3: ("x", 9, -1, 9.66), 5: ("y", 5, -1, 6.33), 7: ("x", 5, -1, 5.79)}
DOLADENI = {5: (2, 1)}                            # doladeni od hrace u vejtrasky (px zin4), platí pro vsechna auta

def posun_do_pruhu(d):
    """posun obrazku v px zin4 (vodorovne, svisle), aby zem pod stredem auta byla ve stredu pruhu CZTR"""
    if d % 2 == 0:
        a, b = posun_do_pruhu((d - 1) % 8), posun_do_pruhu((d + 1) % 8)
        return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    osa, pruh, kresli, stred = PRUH_CZTR[d]
    du, dv = kotva_zrcadlova(d)
    zx, zy = ((-dv) / 4 - (-du) / 8) / 2, ((-dv) / 4 + (-du) / 8) / 2
    o = stred - (pruh + kresli + (zx if osa == "x" else zy))
    sx, sy = (-8 * o, 4 * o) if osa == "x" else (8 * o, 4 * o)
    dx, dy = DOLADENI.get(d, (0, 0))
    return sx + dx, sy + dy

def kotva_konvence(d):
    du, dv = kotva_zrcadlova(d)
    sx, sy = posun_do_pruhu(d)
    return du - sx, dv - sy

vse8 = {}
def nacti_sadu(nater):
    """8 smeru (obrazek, xo, yo) z fotek 4x a do vse8 totez z fotek 8x (orez 2 x ramecek 4x, posun 2x)"""
    adr = os.path.join(FOTKY, f"{VEL}_{nater}")
    info = json.load(open(os.path.join(adr, "kotvy.json")))
    info8 = json.load(open(os.path.join(adr + "_zin8", "kotvy.json")))
    assert info8["zin"] == 8 and info8["ram"] == 2 * info["ram"], (adr, info8["zin"], info8["ram"], info["ram"])
    out, out8 = [], []
    for d in range(8):
        gx, gy = info["smery"][str(d)]["zem_stred"]
        du, dv = kotva_konvence(d)
        foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA")
        bb = foto.getbbox()
        xo, yo = int(math.floor(bb[0] - (gx + du) + 0.5)), int(math.floor(bb[1] - (gy + dv) + 0.5))
        out.append((foto.crop(bb), xo, yo))
        foto8 = Image.open(os.path.join(adr + "_zin8", f"d{d}.png")).convert("RGBA")
        assert foto8.size == (2 * foto.width, 2 * foto.height), (nater, d, foto.size, foto8.size)
        out8.append((foto8.crop((2 * bb[0], 2 * bb[1], 2 * bb[2], 2 * bb[3])), 2 * xo, 2 * yo))
    vse8[nater] = out8
    return out

vse = {n: nacti_sadu(n) for n in NATERY}

# ---------------------------------------------------------------- prekladova tabulka: hracuv vzor (jako V3S)
vzor = open(os.path.join(TU, "..", "prekladova-tabulka-vzor.yagl"), encoding="utf-8").read()
blok = vzor[vzor.index("properties<GlobalSettings"):vzor.index("\n}\n")]
PORADI, POZNAMKA, ODDIL = [], {}, {}
for _r in blok.split("\n"):
    _m = re.match(r'\s+cargo_translation_table: "([^"]{4})";\s*//\s*(.*?)\s*$', _r)
    if _m:
        PORADI.append(_m.group(1)); POZNAMKA[_m.group(1)] = _m.group(2)
    elif _r.strip().startswith("// ----"):
        ODDIL[len(PORADI)] = _r.strip()
TABULKA = PORADI
INDEX = {k: i for i, k in enumerate(TABULKA)}
assert "PASS" in INDEX, "ve vzoru chybi PASS"

# ---------------------------------------------------------------- listy
ODST = 6; SIRKA = 1024
polozky = [((n, i), vse[n][i][0]) for n in NATERY for i in range(8)]
def rozmisti(polozky, sirka):
    x = y = ODST; radek = 0; poz = {}
    for klic, im in polozky:
        if x + im.width + ODST > sirka: x = ODST; y += radek + ODST; radek = 0
        poz[klic] = (x, y); x += im.width + ODST; radek = max(radek, im.height)
    return poz, y + radek + ODST
pozice, vyska = rozmisti(polozky, SIRKA)
PRAZDNY = (SIRKA - ODST - 1, ODST)                 # 1x1 pruhledny pixel pro neviditelny cumak
os.makedirs(os.path.join(VYSTUP, "sprites"), exist_ok=True)
list32 = Image.new("RGBA", (SIRKA, vyska), (0, 0, 0, 0))
for klic, im in polozky: list32.alpha_composite(im, pozice[klic])
list32.save(os.path.join(VYSTUP, "sprites", PNG32))
list8 = Image.new("P", (16, 16), 0); list8.putpalette([0, 0, 255] + [0, 0, 0] * 255)
list8.save(os.path.join(VYSTUP, "sprites", PNG8))
polozky8 = [((n, i), vse8[n][i][0]) for n in NATERY for i in range(8)]
pozice8, vyska8 = rozmisti(polozky8, 2 * SIRKA)
list32_8 = Image.new("RGBA", (2 * SIRKA, vyska8), (0, 0, 0, 0))
for klic, im in polozky8: list32_8.alpha_composite(im, pozice8[klic])
list32_8.save(os.path.join(VYSTUP, "sprites", PNG32_8))

# ---------------------------------------------------------------- yagl
sid = [1]
def sprite(nat=None, i=None):
    """sprite autobusu (zin4 + zin8) nebo bez argumentu prazdny sprite cumaku"""
    out = [f"        sprite_id<0x{sid[0]:08X}>", "        {", f'            [1, 1, 0, 0], normal, c8bpp, "{PNG8}", [4, 4];']
    if nat is None:
        out.append(f'            [1, 1, 0, 0], zin4, c32bpp, "{PNG32}", [{PRAZDNY[0]}, {PRAZDNY[1]}];')
    else:
        im, xo, yo = vse[nat][i]; px, py = pozice[(nat, i)]
        out.append(f'            [{im.width}, {im.height}, {xo}, {yo}], zin4, c32bpp | chunked, "{PNG32}", [{px}, {py}];')
        im8, xo8, yo8 = vse8[nat][i]; px8, py8 = pozice8[(nat, i)]
        assert (im8.width, im8.height, xo8, yo8) == (2 * im.width, 2 * im.height, 2 * xo, 2 * yo), (nat, i)
        out.append(f'            [{im8.width}, {im8.height}, {xo8}, {yo8}], zin8, c32bpp | chunked, "{PNG32_8}", [{px8}, {py8}];')
    out.append("        }"); sid[0] += 1
    return out

ITCH = "https://karel-macha.itch.io/openttd-decouple-by-karel-macha"
DECOUPLE = "ottd Decouple by Karel Macha"
NAZEV = {"cervena": "Škoda 706 RTO"}
UVEDENI = "1958/1/1"                               # seriova vyroba od 1958 (prototypy 1956), do 1972
POPIS = {"cervena": "{green}for " + DECOUPLE + "{black}{new-line}Model: {gold}vlastní kresba podle fotek"}
TEXT = {"cervena": 0x01}
BARVA = {"mala": "{gold}", "velka": "{lt-blue}"}[VEL]
GRF_JMENO = "{yellow}Škoda 706 RTO{green} ottd Decouple by Karel Macha " + BARVA + "{bus}"
VARIANTA_POPIS = {"mala": "original size", "velka": ""}[VEL]
POPIS_GRF = ("{yellow}Škoda 706 RTO{green}  {bus} {new-line}"
             "{green}Škoda 706 RTO red and cream  " + BARVA + "{bus}{new-line}" +
             (BARVA + VARIANTA_POPIS + "{new-line}" if VARIANTA_POPIS else "") +
             "{orange}The Czechoslovak bus of the 1960s, built by Karosa in Vysoké Mýto from 1958 to 1972 (14 451 made). "
             "Rounded all-steel body on a Škoda 706 RT truck frame, 160 hp six-cylinder diesel, 75 km/h, 41 seats. "
             "Intercity ČSAD livery: red below, cream above, silver belt line.{new-line}"
             "{orange}3D: own model drawn from photographs, no third-party parts, sprites in 4x and 8x zoom{new-line}"
             "{new-line}"
             "{green}for ottd Decouple by Karel Mácha " + BARVA + "{bus}{new-line}"
             "{green}OpenTTD where trains couple and uncouple on the move{new-line}"
             "{green}" + ITCH + "{new-line}"
             "{green}GRF: Karel Mácha, licence CC BY 4.0")

Y = ['yagl_version: "";', "grf_format: Container2;",
     "optional_info // Action14", "{", "    INFO: ", "    {",
     f'        URL_: default, "{ITCH}";',
     f"        VRSN: [ 0x{VERZE:02X} 0x00 0x00 0x00 ];", "        MINV: [ 0x01 0x00 0x00 0x00 ];", "        NPAR: [ 0x00 ];",
     "        PALS: [ 0x44 ];", "        BLTR: [ 0x33 ];", "    }", "}",
     "grf // Action08", "{", f'    grf_id: "{GRF_ID}";', "    version: GRF8;", f'    name: "{GRF_JMENO}";',
     f'    description: "{POPIS_GRF}";', "}",
     "properties<GlobalSettings, 0x0000> // Action00, překladová tabulka nákladů: hráčův vzor prekladova-tabulka-vzor.yagl", "{"]
for i, k in enumerate(TABULKA):
    if i in ODDIL: Y.append("    " + ODDIL[i])
    Y += [f"    // instance_id: 0x{i:04X}", "    {", f'        cargo_translation_table: "{k}"; // {POZNAMKA[k]}', "    }"]
Y += ["}", "strings<RoadVehicles, default, 0xD001*> // Action04, popisy v nakupnim okne", "{"]
for n in NATERY: Y.append(f'    /* 0xD0{TEXT[n]:02X} */ "{POPIS[n]}";')
Y.append("}")

def sw(cid, popis, vyraz, rozsahy, default):
    r = [f"switch<RoadVehicles, 0x{cid:02X}, PrimaryDWord> // {popis}", "{", "    expression:", "    {"]
    r += ["        " + v for v in vyraz] + ["    };", "    ranges:", "    {"]
    for rz in rozsahy:
        od, do, cil = rz if len(rz) == 3 else (rz[0], rz[0], rz[1])
        r.append(f"        0x{od:08X}: 0x{cil:04X};" if od == do else f"        0x{od:08X}..0x{do:08X}: 0x{cil:04X};")
    r += ["    };", f"    default: 0x{default:04X};", "}"]
    return r

def action3(eid, default, naklady):
    r = ["feature_graphics<RoadVehicles> // Action03", "{", "    livery_override: false;", f"    default_set_id: 0x{default:04X};",
         f"    feature_ids: [ 0x{eid:04X} ];", "    cargo_types:", "    {"]
    r += [f"        0x{c:02X}: 0x{g:04X};" for c, g in naklady]
    return r + ["    };", "}"]

CALLBACK = ["value1 = variable[0x0C] & 0x0000FFFF;"]
ID = {"cervena": 0x0100}                           # kupovane cislo = cumak
ID_AUTO = {"cervena": 0x0110}                      # viditelny autobus, druhy clanek
dalsi = [0x10]
def nove():
    dalsi[0] += 1; return dalsi[0] - 1

for n in NATERY:
    h = ID[n]; auto = ID_AUTO[n]
    kap_cumak = 1; kap_auto = KAPACITA - kap_cumak     # cumak nese jednoho (s nulou by nakup neukazal naklad)
    for eid, co in ((h, "cumak"), (auto, "auto")):
        p = [f"properties<RoadVehicles, 0x{eid:04X}> // Action00 ({co})", "{", "    {",
             f"        long_introduction_date: date({UVEDENI});", "        model_life_years: 255;",
             "        vehicle_life_years: 20;", "        reliability_decay_speed: 20;",
             "        refittable_cargo_classes: 0x0000;", "        non_refittable_cargo_classes: 0x0000;",
             "        refit_cargo_types: 0x00000000;",
             f"        always_refittable_cargos: [ 0x{INDEX['PASS']:02X} ];",   # jen cestujici
             "        never_refittable_cargos: [ ];",
             f"        cargo_type: 0x{INDEX['PASS']:02X};", "        loading_speed: 0x05;", "        refit_cost: 0x00;",
             "        sprite_id: 0xFF;", "        miscellaneous_flags: 0x00;",
             f"        cargo_capacity: 0x{(kap_cumak if co == 'cumak' else kap_auto):02X};",
             f"        shorten_vehicle: 0x{(8 - CUMAK) if co == 'cumak' else 0:02X};"]
        if co == "cumak":
            p += ["        climate_availability: Temperate | Arctic | Tropical | Toyland;",
                  "        speed_2_kmh: 0x96;",               # 75 km/h (KAR)
                  "        power_10_hp: 0x10;",               # 160 k (117,6 kW)
                  "        weight_quarter_tons: 0x23;",       # 8,75 t pohotovostni (8,57 az 8,95)
                  "        cost_factor: 0x50;", "        running_cost_factor: 0x30;",
                  "        running_cost_base: 0x00004C48;",
                  "        sound_effect_type: 0x1A;",         # odjezd stareho autobusu (SND_1C_DEPARTURE_OLD_BUS)
                  "        callback_flags_mask: 0x10;"]       # clanky (callback 0x16)
        else:
            p += ["        callback_flags_mask: 0x00;"]
        Y += p + ["    }", "}", f"strings<RoadVehicles, default, 0x{eid:04X}> // Action04", "{",
                  f'    /* 0x{eid:04X} */ "{NAZEV[n] if co == "cumak" else NAZEV[n] + " (karoserie)"}";', "}"]
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01: autobus (8 smeru) a prazdna sada pro cumak", "{",
          "    sprite_set // 0x0000 autobus", "    {"]
    for i in range(8): Y += sprite(n, i)
    Y += ["    }", "    sprite_set // 0x0001 prazdny cumak", "    {"]
    for i in range(8): Y += sprite()
    Y += ["    }", "}"]
    g_auto, g_prazdny = nove(), nove()
    Y += [f"sprite_groups<RoadVehicles, 0x{g_auto:02X}> // Action02 basic, autobus", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}",
          f"sprite_groups<RoadVehicles, 0x{g_prazdny:02X}> // Action02 basic, prazdny cumak", "{",
          "    primary_spritesets: [ 0x0001 ];", "    secondary_spritesets: [ 0x0001 ];", "}"]
    g_nakup = nove()
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, obrazek do nakupu (smer W)", "{", "    sprite_set // 0x0000 nakup", "    {"]
    Y += sprite(n, 6)
    Y += ["    }", "}", f"sprite_groups<RoadVehicles, 0x{g_nakup:02X}> // Action02 basic, nakup", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    s_clanky, s_cumak, s_nakup = nove(), nove(), nove()
    Y += sw(s_clanky, "clanky (callback 0x16): 1 = viditelny autobus, dal nic", ["value1 = variable[0x10] & 0x000000FF;"],
            [(1, 0x8000 | auto)], 0xFFFF)
    Y += sw(s_cumak, "cumak: clanky, jinak prazdny sprite", CALLBACK, [(0x16, s_clanky)], g_prazdny)
    Y += sw(s_nakup, "nakup: clanky, popis, obrazek", CALLBACK, [(0x16, s_clanky), (0x23, 0x8000 | TEXT[n])], g_nakup)
    Y += action3(h, s_cumak, [(0xFF, s_nakup)])
    Y += action3(auto, g_auto, [])

open(os.path.join(VYSTUP, "sprites", f"{JMENO}.yagl"), "w", encoding="utf-8").write("\n".join(Y) + "\n")
lic = open(os.path.join(TU, "licence.txt"), encoding="utf-8").read()
open(os.path.join(VYSTUP, "license.txt"), "w", encoding="utf-8").write(lic)
souhrn = {"sprity": {n: [[im.width, im.height, xo, yo] for im, xo, yo in vse[n]] for n in NATERY},
          "sprity_zin8": {n: [[im.width, im.height, xo, yo] for im, xo, yo in vse8[n]] for n in NATERY},
          "cumak": CUMAK, "kapacita": KAPACITA}
json.dump(souhrn, open(os.path.join(VYSTUP, f"{JMENO}-souhrn.json"), "w"), indent=1)
print(JMENO, "spritu", sid[0] - 1, "list 4x", list32.size, "list 8x", list32_8.size, "cumak", CUMAK)
