#!/usr/bin/env python3
# Nova verze GRF VW T1, Skoda 1203 a TAZ (grf_id MAX\x08), z rozbaleneho VWT1-S1203-clanky-oba-na-stred:
#  1. prekladova tabulka 221 kodu: za FREE pripsano 125 kodu ze vzoru (prekladova-tabulka-vzor.yagl) v jeho poradi,
#     stara cisla plati
#  2. naklady podle hrace 30. 9.: VW T1 je vzor pro dodavky, bedna zvlast, valniky podle barvy kupy, lide 2 / 5 / 8
#  3. novy valnik 0x8A se zelenou kupou marihuany (kupa brambor z 0x88 prebarvena, plna i nakladaci)
#  4. neviditelny clanek: cumak delky 1 + auto delky 8, zadni naraznik uz se nepripojuje (poradi kresleni, CUMAK.md;
#     verze 1 mela cumak 2, hrac 30. 9.: "je tam velka mezera", rozestup v kolone 9 misto 10)
#  5. skutecne udaje: rok uvedeni, vykon, max. rychlost, vaha (Pajda karavan 130 km/h a lepsi motor podle hrace)
#  6. (verze 2) TAZ 1203 bus, bus zahradka a tri dodavky 0x8B-0x8F: kopie TAZ 1500 se svetlejsim lakem, od 1973
#  7. (verze 3) roky: vyroba = auto maji vsichni, rok predtim prototyp na zkousku (hra ho nabidne jedne firme
#     na rok); TAZ 1203 se zahradkou az od 1981
#  8. (verze 4) fialova TAZ 1900 D dodavka 0x98 s naftovym motorem VW 1,9 (kopie modre dodavky TAZ 1500)
#  9. (verze 5) divky u otevrenych dveri busu a Pajdy na zastavce (vrstvy za autem a pred autem, holky-u-aut/),
#     novy kod BRAM (nase brambory) na konci tabulky: valnik brambor misto BEAN, k tomu vsude, kde jsou TATO;
#     v popisu GRF autori 3D modelu (Rabatin.B, divky)
# 10. (verze 6) podle vypisu prumyslu (hrac 1. 10.): kovy pod plachtou (plachta a plachta seda), odpad (TRSH, WSTE,
#     RCYC) na valniku s kamennou kupou; cennosti, zlato a diamanty dvanacttrojky nevozi (pojede na ne Avia VB),
#     tekutiny vozi sudy V3S a cisterny Tater
# Pouziti: python3 stavba_vwt1.py <vstup.yagl> <list.png> <zelena.pkl> <kody.json> <slozka sprites> <jmeno>
#   vznikne <slozka sprites>/<jmeno>.yagl, list novych spritu a <slozka sprites>/../<jmeno>-souhrn.json
import json, os, pickle, re, sys
import numpy as np
from PIL import Image

VSTUP, LIST, ZELENA, KODY, VYSTUP, JMENO = sys.argv[1:7]
t = open(VSTUP, encoding="utf-8").read()
kody = json.load(open(KODY, encoding="utf-8"))
TABULKA = kody["grf"] + kody["nove"]                   # 96 hracovych (do FREE) + 125 ze vzoru + BRAM = 222
assert TABULKA[0x5F] == "FREE" and len(TABULKA) == 222 and len(TABULKA) == len(set(TABULKA)) + 1  # CERA je 2x
assert TABULKA[-1] == "BRAM"                           # (verze 5) novy kod na konci, stara cisla plati
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
              "MILK", "EOIL", "SALT", "KAOL", "QLME", "SASH", "FERT", "CBLK", "PLNT",
              "BRAM"]                                  # (verze 5) nase brambory: VW T1, dodavky a plachty jako TATO
VALNIKY = {0x83: ["WOOD", "TWOD"], 0x84: ["COAL", "COKE", "MNO2"],
           0x85: ["CLAY", "PEAT", "BIOM", "AORE", "IORE", "CORE", "COCO"],
           0x86: ["SAND", "SULP", "GRAI", "WHEA", "MAIZ", "CERE"],
           0x87: ["GRVL", "LIME", "SLAG", "SCMT", "SCRP", "NKOR", "PORE", "POTA", "PHOS",
                  "TRSH", "WSTE", "RCYC"],     # (verze 6) odpad na sede kupe (hrac: "odpad bude ta seda kupa na valniku")
           0x88: ["TATO", "BRAM", "CASS", "SGBT"], 0x8A: ["MARI", "HOPS"]}   # zeleny: i chmel (hrac 30. 9.)
# (verze 5) hrac 1. 10.: "valnik brambory, vem mu kod BEAN a dej mu kod BRAM, udelame si svoje brambory, a fazole dame
# do hnedych pytlu na kafe": BEAN uz na valniku brambor neni, v dodavkach a pod plachtou jede dal (jako kava JAVA)

# (verze 5) divky u otevrenych dveri na zastavce: busy a Pajda karavan (hrac 1. 10.), obrazky vrstev z holky-u-aut/
S_HOLKAMI = [0x82, 0x8B, 0x8C, 0x93, 0x94]
HOLKY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "holky-u-aut", "vrstvy")
HOLKY = json.load(open(os.path.join(HOLKY_DIR, "holky.json"), encoding="utf-8"))
assert all(len(HOLKY[d]) == 8 for d in ("za", "pred"))

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
# (verze 6) hrac 1. 10.: "kovy muzou byt pod plachtou": oceli a kovy, ktere dvanacttrojky dosud nevozily
KOVY = [k for k in ("STEL STAL STSH STBR STIG STPL STSL STSW STCB STST STWR STSE STBL STPP STTB PIPE RBAR ALUM IRON "
                    "ZINC NICK COBL CSTI FEAL METL COPR TINP RAMT FECR").split() if k in SLOT]
PLACHTA = sorted(set(DODAVKA) | set(cisla(NEZNAME)) | set(cisla(KOVY)))   # plachta: jako dodavka, nezname kody a kovy
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
    # TAZ 1203 bus a dodavky (od verze 2): naklady jako jejich TAZ 1500, udaje dvanacttrojky
    # (verze 3) se zahradkou az od 1981, bez zahradky od 1973 (hrac 30. 9.)
    0x8B: ("taz1203z", cisla(LIDE_BUS), 8, "PASS"), 0x8C: ("taz1203", cisla(LIDE_BUS), 8, "PASS"),
    0x8D: ("taz1203z", DODAVKA, 2, "MAIL"), 0x8E: ("taz1203z", S_BEDNOU, 2, "GOOD"), 0x8F: ("taz1203", DODAVKA, 2, "MAIL"),
    # (verze 4) fialova TAZ 1900 D (hrac 30. 9.: "udelame jeden fialovej TAZ 1,9D motor z Volkswagenu, asi z modry dodavky")
    0x98: ("taz1900d", DODAVKA, 2, "MAIL"),
}
TAZ1203_Z_1500 = {0x8B: (0x93, "zluta"), 0x8C: (0x94, "zluta"), 0x8D: (0x95, "modra"), 0x8E: (0x96, "modra"),
                  0x8F: (0x97, "modra")}
for v, (_, sez, _, vych) in AUTA.items():
    assert SLOT[vych] in sez, (hex(v), vych)
    assert SLOT["FREE"] not in sez

# ---------------- skutecne udaje (zdroje v souhrnu)
# vykon po 10 k (hra jinak neumi), vaha po 1/4 t, rychlost: vlastnost 0x08 po 0,5 km/h do 127 km/h, nad to 0x15 po 2 km/h
# Pajda karavan: 130 km/h podle hrace (dva svedci, Shell V-Power) a lepsi motor, 110 k, aby na 130 dojel i nalozeny;
# hra se nemeni, odpor vzduchu zustava vychozi (hra ho pocita z max. rychlosti)
# vyroba: od tohoto dne auto maji vsichni; hra ho rok predtim nabidne jedne firme na zkousku (prototyp), proto je
# datum uvedeni v GRF o rok driv (hrac 30. 9.: "prototyp na zkousku ve hre a pak vyroba")
UDAJE = {
    "vw":       dict(vyroba="1950/3/8",   vykon_k=25,  kmh=80,  vaha_kg=975),    # prototypy 1949
    "karavan":  dict(vyroba="1968/11/20", vykon_k=110, kmh=130, vaha_kg=1170),   # Vrchlabi
    "taz1203":  dict(vyroba="1973/4/1",   vykon_k=47,  kmh=90,  vaha_kg=1170),   # Trnava
    "taz1203z": dict(vyroba="1981/1/1",   vykon_k=47,  kmh=90,  vaha_kg=1170),   # se zahradkou (hrac)
    "taz1500":  dict(vyroba="1988/1/1",   vykon_k=57,  kmh=110, vaha_kg=1260),   # motor 1433 cm3
    "taz1900d": dict(vyroba="1996/1/1",   vykon_k=54,  kmh=110, vaha_kg=1260),   # VW 1,9 D 40 kW (cs Wikipedia)
}
for d in UDAJE.values():
    r, m, den = map(int, d["vyroba"].split("/"))
    d["uvedeni"] = f"{r - 1}/{m}/{den}"

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

# ---------------- nova auta: kopie celeho bloku auta (sady auta, skupina, vlastnosti cumaku, jmeno, ikona, auto,
# Action 3 auta, pruhledny cumak, switche, Action 3 cumaku), kazdy sprite s novym cislem, zmenene obrazky na novem listu
velky = np.array(Image.open(LIST).convert("RGBA"))
zel = pickle.load(open(ZELENA, "rb"))                  # {(sada, smer): (rgba, maska, sprite)}
dalsi_id = [max(int(x, 16) for x in re.findall(r"sprite_id<(0x[0-9A-F]+)>", t)) + 1]
LIST_NOVY = f"{JMENO}-nove-sprity.png"
bunky = []                                             # obrazky na novy list v poradi zapisu

def nove_id():
    i = dalsi_id[0]; dalsi_id[0] += 1
    return i

def prepis_sprity(z, obraz=None):
    """kazdy sprite dostane nove cislo; kdyz obraz(sada, smer, (w, h, xo, yo, soubor, x, y)) vrati obrazek, jde
    na novy list, jinak zustane obrazek z puvodniho listu"""
    sady = re.split(r"(?=    sprite_set // )", z)
    out = []
    for si, s in enumerate(sady):
        smer = [-1]
        def jeden(m):
            smer[0] += 1
            w, h, xo, yo, soubor, x, y = m.group(2, 3, 4, 5, 6, 7, 8)
            sp = (int(w), int(h), int(xo), int(yo), soubor, int(x), int(y))
            novy_obraz = obraz(si - 1, smer[0], sp) if obraz else None      # sady[0] je hlavicka zaznamu
            if novy_obraz is not None:
                assert novy_obraz.shape[:2] == (sp[1], sp[0])
                bunky.append(novy_obraz)
                soubor, x, y = LIST_NOVY, "{X%d}" % (len(bunky) - 1), "{Y%d}" % (len(bunky) - 1)
            return (f"sprite_id<0x{nove_id():08X}>\n        {{\n            [{w}, {h}, {xo}, {yo}], zin4, c32bpp | chunked, "
                    f"\"{soubor}\", [{x}, {y}];")
        out.append(re.sub(r"sprite_id<(0x[0-9A-F]+)>\n        \{\n            \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\], "
                          r"zin4, c32bpp \| chunked, \"([^\"]+)\", \[(\d+), (\d+)\];", jeden, s))
    return "".join(out)

def klonuj(zdroj, nos, jmeno, obraz_auta=None, obraz_ikony=None):
    """blok auta zdroj (13 zaznamu) jako nove auto nos s cumakem nos a autem nos + 0x20"""
    zc, nc = zdroj + 0x20, nos + 0x20
    i = najdi(rf"^properties<RoadVehicles, 0x{zdroj:04X}>")
    blok = zaznamy[i - 2:i + 11]
    assert "sprite_sets<" in blok[0] and blok[1].startswith("sprite_groups<RoadVehicles, 0xFF>")
    assert f"feature_ids: [ 0x{zdroj:04X} ]" in blok[12] and f"0x{zc:04X}" in blok[6]
    stare = re.search(r'"([^"]*)"', blok[3]).group(1)
    novy = list(blok)
    novy[0] = prepis_sprity(blok[0], obraz_auta)
    novy[2] = blok[2].replace(f"0x{zdroj:04X}", f"0x{nos:04X}")
    novy[3] = blok[3].replace(f"0x{zdroj:04X}", f"0x{nos:04X}").replace(f'"{stare}"', f'"{jmeno}"')
    novy[4] = prepis_sprity(blok[4], obraz_ikony)
    novy[6] = blok[6].replace(f"0x{zc:04X}", f"0x{nc:04X}")
    novy[7] = blok[7].replace(f"0x{zc:04X}", f"0x{nc:04X}")
    novy[8] = prepis_sprity(blok[8])                   # pruhledny cumak: stejny obrazek
    novy[10] = blok[10].replace(f"0x80{zc:02X}", f"0x80{nc:02X}")
    novy[12] = blok[12].replace(f"0x{zdroj:04X}", f"0x{nos:04X}")
    assert all(novy[n] != blok[n] for n in (2, 3, 6, 7, 10, 12)) and jmeno in novy[3]
    return novy

def zesvetli(a, barva, sytost=0.72, jas=1.10, pridat=0.04):
    """svetlejsi lak: jen syte body v odstinu laku (bus zluta 40-62 stupnu, dodavky modra 190-225), v HSV mene
    sytosti a vic jasu; tmave stiny a okna se skoro nehnou, sedacky, kufry, kola a naklad zustanou"""
    lo, hi = {"zluta": (40, 62), "modra": (190, 225)}[barva]
    f = a.astype(float) / 255
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b); d = np.where(mx - mn == 0, 1, mx - mn)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx == 0, 0, (mx - mn) / np.where(mx == 0, 1, mx))
    m = (a[..., 3] > 0) & (h >= lo) & (h <= hi) & (s > 0.25)
    s2, v2 = s * sytost, np.minimum(1.0, mx * jas + pridat)
    hh = (h / 60) % 6; i = np.floor(hh).astype(int); fr = hh - i
    p, q, tt = v2 * (1 - s2), v2 * (1 - s2 * fr), v2 * (1 - s2 * (1 - fr))
    rgb = np.stack([np.choose(i, [v2, q, p, p, tt, v2]), np.choose(i, [tt, v2, v2, q, p, p]),
                    np.choose(i, [p, p, tt, v2, v2, q])], -1) * 255
    out = a.copy()
    out[..., :3][m] = np.round(rgb[m]).clip(0, 255).astype(np.uint8)
    return out

# valnik 0x8A: sada 0 prazdny valnik (stejny obrazek), 1 plna a 2 nakladani se zelenou kupou; ikona stejna
def zelena(sada, smer, sp):
    if sada not in (1, 2):
        return None
    rgba, _, zsp = zel[(sada, smer)]
    assert (zsp["w"], zsp["h"], zsp["xo"], zsp["yo"]) == sp[:4]
    return rgba
novy = klonuj(0x88, 0x8A, "TAZ 1203 valnik zelena marihuana", zelena)
i89 = najdi(r"^properties<RoadVehicles, 0x0089>")
zaznamy[i89 + 11:i89 + 11] = novy                      # hned za valnik bedna
assert zaznamy[i89 + 10].startswith("feature_graphics") and "0x0089" in zaznamy[i89 + 10]

# TAZ 1203 bus a dodavky (hrac 30. 9.: TAZ 1500 jsou az od 1988, tak i TAZ 1203, busy svetlejsi zlutou, dodavky
# svetlejsi modrou): kopie TAZ 1500, vsechny sady i ikona se svetlejsim lakem
def svetly(barva):
    def obraz(sada, smer, sp):
        w, h, xo, yo, soubor, x, y = sp
        assert soubor == os.path.basename(LIST)
        return zesvetli(velky[y:y + h, x:x + w], barva)
    return obraz
nove = []
for nos, (zdroj, barva) in TAZ1203_Z_1500.items():
    jm = re.search(rf'/\* 0x{zdroj:04X} \*/ "([^"]*)"', t).group(1).replace("TAZ 1500", "TAZ 1203")
    nove += klonuj(zdroj, nos, jm, svetly(barva), svetly(barva))
# fialova TAZ 1900 D: kopie modre dodavky TAZ 1500 bez zahradky, modry lak otoceny na fialovou
def fialova(a, cil=285):
    """fialovy lak: syte body modre (odstin 190-225 stupnu) otocene o (cil - 205) stupnu, sytost a jas zustanou"""
    f = a.astype(float) / 255
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b); d = np.where(mx - mn == 0, 1, mx - mn)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx == 0, 0, (mx - mn) / np.where(mx == 0, 1, mx))
    m = (a[..., 3] > 0) & (h >= 190) & (h <= 225) & (s > 0.25)
    hh = ((h + cil - 205) % 360 / 60) % 6; i = np.floor(hh).astype(int); fr = hh - i
    p, q, tt = mx * (1 - s), mx * (1 - s * fr), mx * (1 - s * (1 - fr))
    rgb = np.stack([np.choose(i, [mx, q, p, p, tt, mx]), np.choose(i, [tt, mx, mx, q, p, p]),
                    np.choose(i, [p, p, tt, mx, mx, q])], -1) * 255
    out = a.copy()
    out[..., :3][m] = np.round(rgb[m]).clip(0, 255).astype(np.uint8)
    return out
def fialovy(sada, smer, sp):
    w, h, xo, yo, soubor, x, y = sp
    assert soubor == os.path.basename(LIST)
    return fialova(velky[y:y + h, x:x + w])
nove += klonuj(0x97, 0x98, "TAZ 1900 D dodavka", fialovy, fialovy)
i_c0 = najdi(r"^properties<RoadVehicles, 0x00C0>")
zaznamy[i_c0:i_c0] = nove                              # pred zadni naraznik, za TAZ 1500

# (verze 5) divky u otevrenych dveri: jedna Action 1 se dvema sadami (0 za autem, 1 pred autem, 8 smeru, prazdne smery
# pruhledne 4 x 4) a skupiny 0xE0 (za) a 0xE3 (pred): za jizdy vysledek callbacku (hra nekresli nic), pri nakladani
# na zastavce divky. Stoji pred blokem prvniho auta, jejich cisla skupin zadne auto nepouziva, takze plati pro vsechny.
r = ["sprite_sets<RoadVehicles, 0x0000> // Action01, divky u otevrenych dveri: 0 za autem, 1 pred autem", "{"]
for si, druh in enumerate(("za", "pred")):
    r += [f"    sprite_set // 0x{si:04X} divky {druh} autem", "    {"]
    for p in HOLKY[druh]:
        a = np.array(Image.open(os.path.join(HOLKY_DIR, p["soubor"])).convert("RGBA"))
        w, h, xo, yo = p["w"], p["h"], p["xo"], p["yo"]
        if a[..., 3].max() == 0:                       # prazdny smer: pruhledny 4 x 4 jako cumak
            a, w, h, xo, yo = np.zeros((4, 4, 4), np.uint8), 4, 4, -2, -2
        assert a.shape[:2] == (h, w)
        bunky.append(a)
        n = len(bunky) - 1
        r += [f"        sprite_id<0x{nove_id():08X}>", "        {",
              f"            [{w}, {h}, {xo}, {yo}], zin4, c32bpp | chunked, \"{LIST_NOVY}\", [{{X{n}}}, {{Y{n}}}];",
              "        }"]
    r += ["    }"]
r += ["}"]
for gid, si, druh in ((0xE0, 0, "za"), (0xE3, 1, "pred")):
    r += [f"sprite_groups<RoadVehicles, 0x{gid:02X}> // Action02 basic, divky {druh} autem: za jizdy nic, na zastavce divky",
          "{", "    primary_spritesets: [ 0x8000 ];", f"    secondary_spritesets: [ 0x{si:04X} ];", "}"]
i80 = najdi(r"^properties<RoadVehicles, 0x0080>")
assert zaznamy[i80 - 2].startswith("sprite_sets<")
zaznamy[i80 - 2:i80 - 2] = ["\n".join(r)]
assert not re.search(r"^(sprite_groups|switch)<RoadVehicles, 0xE[0-3]", "\n".join(zaznamy[i80 - 1:]), re.M)

# (verze 5) autori 3D modelu v popisu GRF: Skoda 1203 Rabatin.B (hracuv listek), divky u dveri (AUTORI-MODELU.md)
i_grf = najdi(r"^grf // Action08")
assert zaznamy[i_grf].count("3D: renderatnight {new-line}") == 1
zaznamy[i_grf] = zaznamy[i_grf].replace(
    "3D: renderatnight {new-line}",
    "3D: renderatnight, Rabatin.B {new-line}{orange} Girls: kiemtruongkts, Rotmill (CC BY 4.0) {new-line}")

# novy list: rady zleva doprava, mezera 2 px
SIRKA_LISTU, pozice, x, y, vyska_rady = 1024, [], 0, 0, 0
for a in bunky:
    h, w = a.shape[:2]
    if x + w + 4 > SIRKA_LISTU:
        x, y, vyska_rady = 0, y + vyska_rady + 4, 0
    pozice.append((x + 2, y + 2))
    x, vyska_rady = x + w + 4, max(vyska_rady, h)
list_novy = Image.new("RGBA", (SIRKA_LISTU, y + vyska_rady + 4), (0, 0, 0, 0))
for (px, py), a in zip(pozice, bunky):
    list_novy.paste(Image.fromarray(a, "RGBA"), (px, py))
list_novy.save(os.path.join(VYSTUP, LIST_NOVY))
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
    # cumak: delka 1 (8 - 7), clanky a kapacita osob, novy vypocet kapacity (nezavisi na vychozim nakladu),
    # skutecne udaje
    z = zaznamy[i]
    for jm, h in [("shorten_vehicle", "0x07"), ("callback_flags_mask", "0x18"), ("miscellaneous_flags", "0x60"),
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
    # viditelne auto: delka 8, kapacita osob callbackem; s divkami i vrstvy (sprite stack, bit 7)
    holky = nos in S_HOLKAMI
    z = zaznamy[i + 4]
    for jm, h in [("shorten_vehicle", "0x00"), ("callback_flags_mask", "0x08"),
                  ("miscellaneous_flags", "0xE0" if holky else "0x60"),
                  ("always_refittable_cargos", seznam(sez)), ("cargo_type", f"0x{SLOT[vych]:02X}"),
                  ("cargo_capacity", "0x01")]:
        z = nastav(z, jm, h)
    zaznamy[i + 4] = z
    # lide na valniku sedi v kabine: prazdny valnik (sada 0), i pri nakladani
    if valnik:
        zaznamy[i - 1] += ("\nsprite_groups<RoadVehicles, 0xFD> // Action02 basic, lide: prazdny valnik\n{\n"
                           "    primary_spritesets: [ 0x0000 ];\n    secondary_spritesets: [ 0x0000 ];\n}")
    # (verze 5) divky: kresleni na mape jde pres tri vrstvy (hra je kresli po sobe): 0 divky za autem, 1 auto,
    # 2 divky pred autem. Promenna 0x10: vrstva v bitech 8-15, druh obrazku v 0-7 (0 = na mape). U vrstvy 0 a 1 na mape
    # zapise switch bit 31 do registru 0x100 (hra pak chce dalsi vrstvu). Callbacky a obrazky mimo mapu (depo, seznamy,
    # nakup) jdou rovnou na auto. Divky jsou jen pri nakladani na zastavce, za jizdy skupiny 0xE0 a 0xE3 nic nekresli.
    holky_sw = []
    if holky:
        holky_sw = [switch(0xE1, "vrstvy: 0 divky za autem, 1 auto, 2 divky pred autem", "\n        ".join([
                        "value1 = variable[0x10] & 0x0000FEFF;",
                        "value2 = variable[0x1A] & 0x00000001;", "value1 = UnsignedMin(value1, value2);",
                        "value2 = variable[0x1A] & 0x00000001;", "value1 = BitwiseXor(value1, value2);",
                        "value2 = variable[0x1A] & 0x0000001F;", "value1 = ShiftLeft(value1, value2);",
                        "value2 = variable[0x1A] & 0x00000100;", "value1 = TempStore(value1, value2);",
                        "value2 = variable[0x10] & 0x0000FFFF;", "value1 = Assign(value1, value2);"]),
                        [(0x000, 0xE0), (0x100, 0xFF), (0x200, 0xE3)], 0xFF),
                    switch(0xE2, "kresleni (bez callbacku) pres vrstvy s divkami", "value1 = variable[0x0C] & 0x0000FFFF;",
                           [(0x00, 0xE1)], 0xFF)]
    g_auto = 0xE2 if holky else 0xFF
    g_lide = 0xFD if valnik else g_auto
    auto_sw = holky_sw + [switch(0xFC, f"auto s lidmi: kapacita {lidi - 1}", "value1 = variable[0x0C] & 0x0000FFFF;",
                                 [(0x15, 0x8000 | (lidi - 1))], g_lide)]
    auto_a3 = [(c, 0xFC) for c in lide_c]
    if vychozi_lide:                                   # v nakupu je vychozi naklad lide: kapacita i tam
        auto_sw.append(switch(0xFB, f"auto v nakupu: kapacita {lidi - 1}", "value1 = variable[0x0C] & 0x0000FFFF;",
                              [(0x15, 0x8000 | (lidi - 1))], 0xFF))
        auto_a3.append((0xFF, 0xFB))
    zaznamy[i + 5] = "\n".join(auto_sw) + "\n" + akce3(auto, g_auto, auto_a3)
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
print("zaznamu", len(zaznamy), "novych spritu", dalsi_id[0] - 0x408, "list", list_novy.size)
