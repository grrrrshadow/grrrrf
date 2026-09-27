# -*- coding: utf-8 -*-
# Balic Sergeje: z fotek (render_sergej.py) udela spritesheet a cely GRF v yaglu.
#   python3 pack_sergej.py <orig|bryle> <adresar s fotkami> <vystupni adresar>
# Fotky: <adresar>/<orig|bryle>_zeleny a _cerveny, v kazdem d0-d8.png, vlastnik_d1/3/5/7.png, kotvy.json.
#
# Lokomotiva je 3 clanky jako CZTR 770: hlava, stred (8 osmin), zad.
#   orig : 2 + 8 + 2 = 12 osmin (CZTR meritko, ~12,2 px/m v zin4)
#   bryle: 3 + 8 + 3 = 14 osmin (o 20 % vetsi sprity, 14,64 px/m)
# Na sikme koleji (smery 0,2,4,6) kresli celou lokomotivu stred, hlava a zad jsou prazdne.
# Na rovne koleji (1,3,5,7) si kazdy clanek kresli svuj kus podle barevneho pruchodu.
#
# Posuny: hra kresli sprite na RemapCoords(poloha + bounds.origin + bounds.offset), viz
# Train::UpdateDeltaXY (train_cmd.cpp) a AddSortableSpriteToDraw (viewport.cpp). Kotva spritu
# tedy neni poloha vozidla; tady se to dopocita, aby bod na koleji pod stredem clanku padl
# presne na polohu clanku.
import os, sys, json
import numpy as np
from PIL import Image

VARIANTA, FOTKY, VYSTUP = sys.argv[1], sys.argv[2], sys.argv[3]
DELKY = {"orig": (2, 8, 2), "bryle": (3, 8, 3)}[VARIANTA]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hra import ROVNE, KROK, remap, kotva_hry, odstupy

N_HLAVA, N_ZAD = odstupy(DELKY)
# Rucni doladeni podle hry: sever o 3 px doprava (hrac 27. 9.: "severni smer sprity lehce doprava",
# jih ne). CZTR ma stred lokomotivy v severnim pohledu 2,5 px vpravo od kotvy u vsech 364 sad.
KOREKCE = {0: (3, 0)}

def rozdel(d, fotka, vlastnik, predni):
    """Pixely fotky -> clanek (0 hlava, 1 stred, 2 zad) podle barevneho pruchodu."""
    a = np.array(fotka); v = np.array(vlastnik).astype(int)
    lab = np.full(a.shape[:2], -1, int)
    ma = v[..., 3] > 0
    k = np.argmax(v[..., :3], axis=2)              # 0 = plus konec (R), 1 = stred (G), 2 = minus konec (B)
    konec = {0: "plus", 2: "minus"}
    for kk in (0, 1, 2):
        sel = ma & (k == kk)
        if kk == 1: lab[sel] = 1
        else: lab[sel] = 0 if konec[kk] == predni else 2
    # vyhlazene okraje siluety, ktere v ostrem pruchodu nejsou: nejblizsi soused
    potreba = (a[..., 3] > 0) & (lab < 0)
    for _ in range(12):
        if not potreba.any(): break
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            sh = np.roll(np.roll(lab, dy, 0), dx, 1)
            vyplnit = potreba & (sh >= 0)
            lab[vyplnit] = sh[vyplnit]
            potreba = (a[..., 3] > 0) & (lab < 0)
    kusy = []
    for c in range(3):
        k_ = a.copy(); k_[lab != c] = 0
        kusy.append(Image.fromarray(k_))
    return kusy

def orez(im):
    bb = im.getbbox()
    if bb is None: return None, (0, 0)
    return im.crop(bb), (bb[0], bb[1])

def natier_sprity(adr):
    info = json.load(open(os.path.join(adr, "kotvy.json")))
    assert info["osmin"] == sum(DELKY), (info["osmin"], DELKY)
    sprity = {"hlava": [], "stred": [], "zad": [], "nakup": []}
    for d in range(8):
        s = info["smery"][str(d)]; kx, ky = s["kotva"]
        foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA")
        if d in ROVNE:
            vl = Image.open(os.path.join(adr, f"vlastnik_d{d}.png")).convert("RGBA")
            kusy = rozdel(d, foto, vl, s["predni"])
            posun = {"hlava": N_HLAVA, "stred": 0, "zad": -N_ZAD}
            for jm, kus, L in zip(("hlava", "stred", "zad"), kusy, DELKY):
                im, (cx, cy) = orez(kus)
                if im is None: sprity[jm].append(None); continue
                ax = kx + posun[jm] * KROK[d][0]; ay = ky + posun[jm] * KROK[d][1]
                rx, ry = remap(*kotva_hry(L, d))
                sprity[jm].append((im, int(round(cx - ax - rx)), int(round(cy - ay - ry))))
        else:
            im, (cx, cy) = orez(foto)
            rx, ry = remap(*kotva_hry(DELKY[1], d))
            kx_, ky_ = KOREKCE.get(d, (0, 0))
            sprity["stred"].append((im, int(round(cx - kx - rx)) + kx_, int(round(cy - ky - ry)) + ky_))
            sprity["hlava"].append(None); sprity["zad"].append(None)
    # obrazek do nakupu: pohled W (d8), posuny jako stred ve smeru W
    s = info["smery"]["8"]; kx, ky = s["kotva"]
    im, (cx, cy) = orez(Image.open(os.path.join(adr, "d8.png")).convert("RGBA"))
    rx, ry = remap(*kotva_hry(DELKY[1], 6))
    sprity["nakup"].append((im, int(round(cx - kx - rx)), int(round(cy - ky - ry))))
    return sprity

# ---------------------------------------------------------------- spritesheet
NATERY = ("zeleny", "cerveny")
vse = {n: natier_sprity(os.path.join(FOTKY, f"{VARIANTA}_{n}")) for n in NATERY}
JMENO = {"orig": "Sergej_M62", "bryle": "Sergej_M62_BRYLE"}[VARIANTA]
PNG32 = f"{JMENO}-32bpp-zin4.png"; PNG8 = f"{JMENO}-8bpp.png"
os.makedirs(os.path.join(VYSTUP, "sprites"), exist_ok=True)

ODST = 6
polozky = []                                    # (klic, obrazek)
for n in NATERY:
    for jm in ("hlava", "stred", "zad", "nakup"):
        for i, sp in enumerate(vse[n][jm]):
            if sp is not None: polozky.append(((n, jm, i), sp[0]))
SIRKA = 1024
x = y = ODST; radek = 0; pozice = {}
for klic, im in polozky:
    if x + im.width + ODST > SIRKA: x = ODST; y += radek + ODST; radek = 0
    pozice[klic] = (x, y); x += im.width + ODST; radek = max(radek, im.height)
PRAZDNY = (SIRKA - ODST - 1, ODST)              # 1x1 pruhledny pixel pro prazdne smery
vyska = y + radek + ODST
list32 = Image.new("RGBA", (SIRKA, vyska), (0, 0, 0, 0))
for klic, im in polozky: list32.alpha_composite(im, pozice[klic])
list32.save(os.path.join(VYSTUP, "sprites", PNG32))
list8 = Image.new("P", (16, 16), 0); list8.putpalette([0, 0, 255] + [0, 0, 0] * 255)
list8.save(os.path.join(VYSTUP, "sprites", PNG8))

# ---------------------------------------------------------------- yagl
sid = [1]                                       # sprite_id od 1, nula se pri rozbaleni ztraci
def sprite(sp, klic):
    out = [f"        sprite_id<0x{sid[0]:08X}>", "        {",
           f'            [1, 1, 0, 0], normal, c8bpp, "{PNG8}", [4, 4];']
    if sp is None:
        out.append(f'            [1, 1, 0, 0], zin4, c32bpp, "{PNG32}", [{PRAZDNY[0]}, {PRAZDNY[1]}];')
    else:
        im, xo, yo = sp; px, py = pozice[klic]
        out.append(f'            [{im.width}, {im.height}, {xo}, {yo}], zin4, c32bpp | chunked, "{PNG32}", [{px}, {py}];')
    out.append("        }"); sid[0] += 1
    return out

ID = {"zeleny": 0x0100, "cerveny": 0x0110}      # hlava; stred +1, zad +2
TEXT = {"zeleny": 0x01, "cerveny": 0x02}        # D001, D002
NAZEV = {"zeleny": "M62 Tamtam tajgy", "cerveny": "Sergej ČSD"}
UVEDENI = {"zeleny": "1965/1/1", "cerveny": "1966/1/1"}
TECH = ("Motor: {gold}14D40, dvanáctiválcový dvoutakt{black}{new-line}"
        "Uspořádání: {gold}Co'Co'{black}{new-line}Délka: {gold}17,55 m{black}{new-line}")
POPIS = {
    "zeleny": ("Určení: {gold}nákladní a osobní vlaky{black}{new-line}Výrobce: {gold}Luhansk{black}{new-line}" + TECH +
               "{lt-green}Mezinárodní M62. Dvoutakt z německé ponorky. Jezdila v Německu (NDR) jako Taigatrommel, "
               "tamtam tajgy, v Polsku, Maďarsku i Československu.{black}{new-line}Model: {gold}Chicken cutlet (Sketchfab), CC BY 4.0"),
    "cerveny": ("Určení: {gold}nákladní a osobní vlaky{black}{new-line}" + TECH +
                "{lt-green}ČSD T 679.1, od roku 1988 řada 781, přezdívaná Sergej. Dvoutakt z německé ponorky, "
                "vyrobený v Rusku.{black}{new-line}Model: {gold}Chicken cutlet (Sketchfab), CC BY 4.0"),
}
# Zvuky (Action11 + callback 0x33): zvuky/<natier>_start.wav a zvuky/<natier>_tunel.wav, pokud existuji.
# Vlastni zvuky GRF se cisluji od 0x49 v poradi Action11. Udalosti (var 0x10): 1 = rozjezd, 2 = tunel.
ZVUKY_ADR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zvuky")
ZVUKY = []                                        # (natier, udalost, soubor)
for n in NATERY:
    for udalost, jm in ((1, "start"), (2, "tunel")):
        f = os.path.join(ZVUKY_ADR, f"{n}_{jm}.wav")
        if os.path.exists(f): ZVUKY.append((n, udalost, f))
CISLO_ZVUKU = {(n, u): 0x49 + i for i, (n, u, _) in enumerate(ZVUKY)}

GRF_ID = {"orig": "MAXb", "bryle": "MAXc"}[VARIANTA]
GRF_JMENO = {"orig": "Sergej M62", "bryle": "Sergej M62 BRÝLE +20 %"}[VARIANTA]
POPIS_GRF = {"orig": "M62 Tamtam tajgy a Sergej ČSD, měřítko CZTR, 12/8 dlaždice.",
             "bryle": "M62 Tamtam tajgy a Sergej ČSD, o 20 % větší (BRÝLE), 14/8 dlaždice."}[VARIANTA]

Y = ['yagl_version: "";', "grf_format: Container2;",
     "optional_info // Action14", "{", "    INFO: ", "    {",
     "        VRSN: [ 0x01 0x00 0x00 0x00 ];", "        MINV: [ 0x00 0x00 0x00 0x00 ];", "        NPAR: [ 0x00 ];",
     "        PALS: [ 0x44 ];", "        BLTR: [ 0x33 ];", "    }", "}",
     "grf // Action08", "{", f'    grf_id: "{GRF_ID}";', "    version: GRF8;", f'    name: "{GRF_JMENO}";',
     f'    description: "{POPIS_GRF}{{new-line}}Model: Diesel locomotive M62, Chicken cutlet (sketchfab.com/Chicken_Cutlet), CC BY 4.0{{new-line}}GRF: Karel Mácha";', "}",
     "strings<Trains, default, 0xD001*> // Action04, popisy v nakupnim okne", "{"]
for n in NATERY:
    Y.append(f'    /* 0xD0{TEXT[n]:02X} */ "{POPIS[n]}";')
Y.append("}")
if ZVUKY:
    import shutil
    Y += ["sound_effects // Action11, vlastni zvuky od 0x49", "{"]
    for n, u, f in ZVUKY:
        shutil.copy(f, os.path.join(VYSTUP, "sprites", os.path.basename(f)))
        Y += [f"    sprite_id<0x{sid[0]:08X}>", "    {", f'        binary("sprites/{os.path.basename(f)}");', "    }"]
        sid[0] += 1
    Y += ["}"]

for n in NATERY:
    h = ID[n]; SP = vse[n]
    Y += [f"// ---------------- {NAZEV[n]}"]
    for jm, eid, L in (("hlava", h, DELKY[0]), ("stred", h + 1, DELKY[1]), ("zad", h + 2, DELKY[2])):
        p = [f"properties<Trains, 0x{eid:04X}> // Action00", "{", "    {",
             f"        long_introduction_date: date({UVEDENI[n]});", "        model_life_years: 255;",
             "        vehicle_life_years: 50;", "        reliability_decay_speed: 20;",
             "        track_type: 0;", "        sprite_id: 0xFD;", "        cargo_capacity: 0;",
             "        refit_cargo_types: 0x00000000;",
             f"        shorten_vehicle: 0x{8 - L:02X};"]
        if jm == "hlava":
            p += ["        climate_availability: Temperate | Arctic | Tropical | Toyland;",
                  "        speed_kmh: 100;", "        power: 1971;", "        weight_tons: 116;",
                  "        cost_factor: 0x34;", "        running_cost_factor: 0x4C;", "        running_cost_base: 0x00004C36;",
                  "        engine_traction_type: 0x08;", "        coeff_of_tractive_effort: 0x4F;",
                  "        coeff_of_air_drag: 0x14;", "        ai_engine_rank: 0x04;",
                  "        visual_effect: effect(DisableEffect, 0x00, Enable);",
                  f"        callback_flags_mask: 0x{0x10 | (0x80 if any(z[0] == n for z in ZVUKY) else 0):02X};"]
        elif jm == "stred":
            p += ["        visual_effect: effect(DieselFumes, 0x08, Enable);"]
        else:
            p += ["        visual_effect: effect(DisableEffect, 0x00, Enable);"]
        Y += p + ["    }", "}",
                  f"strings<Trains, default, 0x{eid:04X}> // Action04", "{",
                  f'    /* 0x{eid:04X} */ "{NAZEV[n] if jm == "hlava" else NAZEV[n] + " (článek)"}";', "}"]
    # Action01: 0 hlava, 1 stred, 2 zad (po osmi spritech); obrazek do nakupu ma vlastni Action01,
    # protoze vsechny sady v jednom Action01 musi mit stejny pocet spritu
    base = 0x10 if n == "zeleny" else 0x20
    Y += ["sprite_sets<Trains, 0x0000> // Action01", "{"]
    for si, jm in enumerate(("hlava", "stred", "zad")):
        Y += [f"    sprite_set // 0x{si:04X} {jm}", "    {"]
        for i, sp in enumerate(SP[jm]):
            Y += sprite(sp, (n, jm, i))
        Y += ["    }"]
    Y += ["}"]
    for si in range(3):
        Y += [f"sprite_groups<Trains, 0x{base + si:02X}> // Action02 basic", "{",
              f"    primary_spritesets: [ 0x{si:04X} ];", f"    secondary_spritesets: [ 0x{si:04X} ];", "}"]
    Y += ["sprite_sets<Trains, 0x0000> // Action01, obrazek do nakupu", "{", "    sprite_set // 0x0000 nakup", "    {"]
    Y += sprite(SP["nakup"][0], (n, "nakup", 0))
    Y += ["    }", "}",
          f"sprite_groups<Trains, 0x{base + 3:02X}> // Action02 basic", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    clan = base + 4; hl = base + 5; nak = base + 6
    Y += [f"switch<Trains, 0x{clan:02X}, PrimaryDWord> // clanky (callback 0x16)", "{",
          "    expression:", "    {", "        value1 = variable[0x10] & 0x000000FF;", "    };",
          "    ranges:", "    {", f"        0x00000001: 0x{0x8000 | (h + 1):04X};", f"        0x00000002: 0x{0x8000 | (h + 2):04X};",
          "    };", "    default: 0xFFFF;", "}",
          ] + ([f"switch<Trains, 0x{base + 7:02X}, PrimaryDWord> // zvuky (callback 0x33)", "{",
          "    expression:", "    {", "        value1 = variable[0x10] & 0x000000FF;", "    };",
          "    ranges:", "    {"] + [f"        0x{u:08X}: 0x{0x8000 | CISLO_ZVUKU[(n, u)]:04X};" for (nn, u, _) in ZVUKY if nn == n] +
          ["    };", "    default: 0xFFFF;", "}"] if any(z[0] == n for z in ZVUKY) else []) + [
          f"switch<Trains, 0x{hl:02X}, PrimaryDWord> // hlava: clanky, zvuky nebo grafika", "{",
          "    expression:", "    {", "        value1 = variable[0x0C] & 0x0000FFFF;", "    };",
          "    ranges:", "    {", f"        0x00000016: 0x{clan:04X};"] + ([f"        0x00000033: 0x{base + 7:04X};"] if any(z[0] == n for z in ZVUKY) else []) + [
          "    };", f"    default: 0x{base:04X};", "}",
          f"switch<Trains, 0x{nak:02X}, PrimaryDWord> // nakup: clanky, popis, obrazek", "{",
          "    expression:", "    {", "        value1 = variable[0x0C] & 0x0000FFFF;", "    };",
          "    ranges:", "    {", f"        0x00000016: 0x{clan:04X};", f"        0x00000023: 0x{0x8000 | TEXT[n]:04X};",
          "    };", f"    default: 0x{base + 3:04X};", "}",
          "feature_graphics<Trains> // Action03", "{", "    livery_override: false;", f"    default_set_id: 0x{hl:04X};",
          f"    feature_ids: [ 0x{h:04X} ];", "    cargo_types:", "    {", f"        0xFF: 0x{nak:04X};", "    };", "}"]
    for off, g in ((1, base + 1), (2, base + 2)):
        Y += ["feature_graphics<Trains> // Action03", "{", "    livery_override: false;", f"    default_set_id: 0x{g:04X};",
              f"    feature_ids: [ 0x{h + off:04X} ];", "    cargo_types:", "    {", "    };", "}"]

open(os.path.join(VYSTUP, "sprites", f"{JMENO}.yagl"), "w").write("\n".join(Y) + "\n")
souhrn = {n: {jm: [None if sp is None else [sp[0].width, sp[0].height, sp[1], sp[2]] for sp in vse[n][jm]] for jm in vse[n]} for n in NATERY}
json.dump(souhrn, open(os.path.join(VYSTUP, f"{JMENO}-sprity.json"), "w"), indent=1)
print(JMENO, "spritu", sid[0] - 1, "list", list32.size, "hlava pred stredem", N_HLAVA, "zad za stredem", N_ZAD)
