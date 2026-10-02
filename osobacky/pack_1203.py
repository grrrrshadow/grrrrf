# -*- coding: utf-8 -*-
# Balic osobacku, zatim TAZ 1203 plachta: z fotek 8x (render_1203.py) udela spritesheet a cely GRF v yaglu.
#   python3 pack_1203.py <adresar s fotkami> <vystupni adresar>
# Fotky: <adresar>/<orig|zmensena>/d0-d7.png + kotvy.json (zin 8).
# Hrac 2. 10.: "grf musi byt bez 4x spritu, jenom 8x pouzijem. udelame orig size a zmenseny do jednoho grf." Proto:
# - kazdy sprite je jen zin8 (a 1x1 paletova atrapa pro 8bpp blitter jako u ostatnich GRF), 4x a mensi si hra dopocita
#   (od afed76d 4x prumerem 2x2 vazenym alfou); posuny a rozmery 8x jsou suda cisla, aby 4x vyslo na cely pixel;
# - oba vozy v jednom GRF: orig size jako 1203 z VW T1 (17,71 px/m ve 4x, rozvor 42,5 px) a zmensena jako mala
#   vejtraska (CZTR, 12,2 px/m ve 4x). Auto je 4,81 m = 7,56 osmin (orig) a 5,2 osmin (zmensena), obe jeden dil 8/8.
# Kotvy a pruh na silnici CZTR jako pack_v3s.py / pack_rto.py (prepocet 4x -> 8x je krat 2).
# Naklady, kapacita a udaje jako TAZ 1203 plachta 0x91 z dodavek (auta/NOVA-VERZE.md): 121 kodu, vychozi posta,
# kapacita 2 s novym nasobenim (sypke 2, zbozi a posta 4), lide callbackem 0x15 jen 2 (sedi v kabine).
import os, sys, json, math, re
import numpy as np
from PIL import Image

FOTKY, VYSTUP = sys.argv[1:3]
TU = os.path.dirname(os.path.abspath(__file__))
# Verze: kazde sestaveni pro hrace o jednu vys, je ve jmenu souboru i v Action14 (VRSN).
# 1 TAZ 1203 plachta, orig size a zmensena, jen zin8
VERZE = 1
JMENO = f"Osobacky-v{VERZE}"
GRF_ID = "MAXh"
PNG32_8 = f"{JMENO}-32bpp-zin8.png"; PNG8 = f"{JMENO}-8bpp.png"
VELIKOSTI = ["orig", "zmensena"]
ID = {"orig": 0x0100, "zmensena": 0x0101}
NAZEV = {"orig": "TAZ 1203 plachta", "zmensena": "TAZ 1203 plachta zmenšená"}
VARIANTA = {"orig": "{gold}orig size", "zmensena": "{lt-blue}zmenšená, jako malá vejtřaska"}
TEXT = {"orig": 0x01, "zmensena": 0x02}
UVEDENI = "1972/4/1"                               # vyroba v Trnave od 1. 4. 1973, rok predtim na zkousku (dodavky)
LIDE = ["PASS", "WORK", "PRIS", "YETI", "YETY"]
KAPACITA_LIDE = 2


# ---------------------------------------------------------------- kotvy (jako pack_v3s.py, px zin4)
def kotva_zrcadlova(d):
    """kotva spritu proti bodu na zemi pod stredem auta, px zin4 (vodorovne, svisle), zrcadlove srovnana"""
    a = math.radians(45 * d)
    return 10.0 * math.sin(a), -20.8 - 0.7 * math.cos(a)

# Pruh na silnici CZTR (viz pack_v3s.py): hra vede auto v pruhu na 9 (SV, JV) nebo 5 (JZ, SZ) jednotkach dlazdice
# a kresli ho na poloha + (-2, -1) (SV, JZ) nebo (-1, -2) (JV, SZ). Stred pruhu CZTR RT14: podel X 10,2 a 6,33,
# podel Y 9,66 a 5,79. smer: (osa napric, pruh hry, posun kresleni napric, stred pruhu CZTR)
PRUH_CZTR = {1: ("y", 9, -1, 10.2), 3: ("x", 9, -1, 9.66), 5: ("y", 5, -1, 6.33), 7: ("x", 5, -1, 5.79)}
DOLADENI = {5: (2, 1)}                            # doladeni od hrace u vejtrasky (px zin4), plati pro vsechna auta

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


def nacti_sadu(vel):
    """8 smeru (obrazek, xo, yo) v 8x: posun i rozmery suda cisla, orez s pruhlednym okrajem do sudych rozmeru"""
    adr = os.path.join(FOTKY, vel)
    info = json.load(open(os.path.join(adr, "kotvy.json")))
    assert info["zin"] == 8, (adr, info["zin"])
    out = []
    for d in range(8):
        gx, gy = info["smery"][str(d)]["zem_stred"]
        du, dv = kotva_konvence(d)
        ax, ay = gx + 2 * du, gy + 2 * dv            # kotva (poloha auta ve hre) v pixelech fotky 8x
        foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA")
        bb = foto.getbbox()
        xo, yo = 2 * math.floor((bb[0] - ax) / 2), 2 * math.floor((bb[1] - ay) / 2)
        L, T = int(round(ax + xo)), int(round(ay + yo))
        assert L <= bb[0] and T <= bb[1], (vel, d, L, T, bb)
        w, h = bb[2] - L, bb[3] - T
        w += w % 2; h += h % 2
        sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sprite.alpha_composite(foto.crop((L, T, min(L + w, foto.width), min(T + h, foto.height))), (0, 0))
        assert xo % 2 == 0 and yo % 2 == 0 and w % 2 == 0 and h % 2 == 0
        out.append((sprite, xo, yo))
    return out

vse = {v: nacti_sadu(v) for v in VELIKOSTI}

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
NAKLADY = list(dict.fromkeys(json.load(open(os.path.join(TU, "plachta_naklady.json")))))
chybi = [k for k in NAKLADY if k not in INDEX]
assert not chybi, f"ve vzoru chybi {chybi}"

# ---------------------------------------------------------------- list (jen 8x) a paletova atrapa
ODST = 6; SIRKA = 1024
polozky = [((v, i), vse[v][i][0]) for v in VELIKOSTI for i in range(8)]
def rozmisti(polozky, sirka):
    x = y = ODST; radek = 0; poz = {}
    for klic, im in polozky:
        if x + im.width + ODST > sirka: x = ODST; y += radek + ODST; radek = 0
        poz[klic] = (x, y); x += im.width + ODST; radek = max(radek, im.height)
    return poz, y + radek + ODST
pozice, vyska = rozmisti(polozky, SIRKA)
os.makedirs(os.path.join(VYSTUP, "sprites"), exist_ok=True)
list32 = Image.new("RGBA", (SIRKA, vyska), (0, 0, 0, 0))
for klic, im in polozky: list32.alpha_composite(im, pozice[klic])
list32.save(os.path.join(VYSTUP, "sprites", PNG32_8))
list8 = Image.new("P", (16, 16), 0); list8.putpalette([0, 0, 255] + [0, 0, 0] * 255)
list8.save(os.path.join(VYSTUP, "sprites", PNG8))

# ---------------------------------------------------------------- yagl
sid = [1]
def sprite(vel, i):
    """sprite auta: jen zin8 (a 1x1 paletova atrapa)"""
    im, xo, yo = vse[vel][i]; px, py = pozice[(vel, i)]
    out = [f"        sprite_id<0x{sid[0]:08X}>", "        {", f'            [1, 1, 0, 0], normal, c8bpp, "{PNG8}", [4, 4];',
           f'            [{im.width}, {im.height}, {xo}, {yo}], zin8, c32bpp | chunked, "{PNG32_8}", [{px}, {py}];', "        }"]
    sid[0] += 1
    return out

ITCH = "https://karel-macha.itch.io/openttd-decouple-by-karel-macha"
DECOUPLE = "ottd Decouple by Karel Macha"
POPIS = {v: "{green}for " + DECOUPLE + "{black}{new-line}" + VARIANTA[v] + "{black}{new-line}"
            "Model: {gold}Jiří Novák (Printables), CC0" for v in VELIKOSTI}
GRF_JMENO = "{yellow}Osobáčky{green} ottd Decouple by Karel Macha {gold}{truck}"
POPIS_GRF = ("{green}Osobáčky: TAZ 1203 plachta {gold}{truck}{new-line}"
             "{orange}3D: Jiří Novák (Printables, Škoda 1203 ROL valník 1975), CC0{new-line}"
             "{gold}orig size {lt-blue}and smaller in one GRF{new-line}"
             "{orange}Sprites only in 8x zoom, the game makes the smaller zooms itself.{new-line}"
             "{orange}The little Czechoslovak cab-over from Vrchlabí, built in Trnava by TAZ from 1973: a pickup with "
             "a mustard tarp, 47 hp, 90 km/h. Carries mail, goods, food and almost everything else under the tarp, "
             "two people ride in the cab.{new-line}"
             "{new-line}"
             "{green}for ottd Decouple by Karel Mácha {gold}{truck}{new-line}"
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
for v in VELIKOSTI: Y.append(f'    /* 0xD0{TEXT[v]:02X} */ "{POPIS[v]}";')
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
dalsi = [0x10]
def nove():
    dalsi[0] += 1; return dalsi[0] - 1

for v in VELIKOSTI:
    eid = ID[v]
    Y += [f"properties<RoadVehicles, 0x{eid:04X}> // Action00 ({NAZEV[v]})", "{", "    {",
          "        climate_availability: Temperate | Arctic | Tropical | Toyland;",
          f"        long_introduction_date: date({UVEDENI});", "        model_life_years: 255;",
          "        vehicle_life_years: 255;", "        reliability_decay_speed: 20;",
          "        refittable_cargo_classes: 0x0000;", "        non_refittable_cargo_classes: 0x0000;",
          "        refit_cargo_types: 0x00000000;",
          "        always_refittable_cargos: [ " + " ".join(f"0x{INDEX[k]:02X}" for k in NAKLADY) + " ];",
          "        never_refittable_cargos: [ ];",
          f"        cargo_type: 0x{INDEX['MAIL']:02X};", "        loading_speed: 0x05;", "        refit_cost: 0x00;",
          "        sprite_id: 0xFF;",
          "        miscellaneous_flags: 0x60;",        # nove nasobeni kapacity (0x20) a bez koure pri poruse (0x40)
          "        cargo_capacity: 0x02;",
          "        shorten_vehicle: 0x00;",
          "        speed_2_kmh: 0xB4;",                # 90 km/h
          "        power_10_hp: 0x05;",                # 47 k (35 kW), ve hre 50 k
          "        weight_quarter_tons: 0x05;",        # 1 170 kg, ve hre 1,25 t
          "        cost_factor: 0x05;", "        running_cost_factor: 0x05;", "        running_cost_base: 0x00000000;",
          "        sound_effect_type: 0x17;",
          "        callback_flags_mask: 0x08;",        # kapacita (callback 0x15)
          "    }", "}", f"strings<RoadVehicles, default, 0x{eid:04X}> // Action04", "{",
          f'    /* 0x{eid:04X} */ "{NAZEV[v]}";', "}"]
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01: auto (8 smeru)", "{", "    sprite_set // 0x0000 auto", "    {"]
    for i in range(8): Y += sprite(v, i)
    Y += ["    }", "}"]
    g_auto = nove()
    Y += [f"sprite_groups<RoadVehicles, 0x{g_auto:02X}> // Action02 basic, auto", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, obrazek do nakupu (smer W)", "{", "    sprite_set // 0x0000 nakup", "    {"]
    Y += sprite(v, 6)
    Y += ["    }", "}"]
    g_nakup = nove()
    Y += [f"sprite_groups<RoadVehicles, 0x{g_nakup:02X}> // Action02 basic, nakup", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    s_lide, s_nakup = nove(), nove()
    Y += sw(s_lide, f"lide: kapacita {KAPACITA_LIDE} (callback 0x15), jinak obrazek", CALLBACK,
            [(0x15, 0x8000 | KAPACITA_LIDE)], g_auto)
    Y += sw(s_nakup, "nakup: popis (callback 0x23), jinak obrazek", CALLBACK, [(0x23, 0x8000 | TEXT[v])], g_nakup)
    Y += action3(eid, g_auto, [(INDEX[k], s_lide) for k in LIDE] + [(0xFF, s_nakup)])

open(os.path.join(VYSTUP, "sprites", f"{JMENO}.yagl"), "w", encoding="utf-8").write("\n".join(Y) + "\n")
lic = open(os.path.join(TU, "licence.txt"), encoding="utf-8").read()
open(os.path.join(VYSTUP, "license.txt"), "w", encoding="utf-8").write(lic)
souhrn = {"sprity_zin8": {v: [[im.width, im.height, xo, yo] for im, xo, yo in vse[v]] for v in VELIKOSTI},
          "naklady": NAKLADY, "lide": LIDE}
json.dump(souhrn, open(os.path.join(VYSTUP, f"{JMENO}-souhrn.json"), "w"), indent=1)
print(JMENO, "spritu", sid[0] - 1, "list 8x", list32.size, "naklady", len(NAKLADY))
