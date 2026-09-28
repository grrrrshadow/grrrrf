# -*- coding: utf-8 -*-
# Balic Pragy V3S "vejtrasky": z fotek (render_v3s.py) udela spritesheet a GRF v yaglu.
#   python3 pack_v3s.py <mala|velka> <adresar s fotkami> <vystupni adresar>
# Fotky: <adresar>/<mala|velka>_<nater>/d0-d7.png a kotvy.json, nater = vojenska, modra_A .. modra_D.
#
#   mala : meritko CZTR, 12,2 px/m (zin4). Auto ma 7,7 osminy, vejde se do jednoho mista v kolone (8).
#   velka: BRYLE, o 20 % vetsi, 14,64 px/m, 9,25 osminy. Aby se v kolone neprekryvala, je pred ni
#          neviditelny cumak delky 2 (rozestup 8 + 2 = 10, viz auta/CUMAK.md). Kupovane cislo je cumak,
#          drzi jmeno, cenu a obrazek v nakupu; auto je druhy clanek. Clankova auta berou jen
#          pruchozi zastavky (hra: STR_ERROR_NO_STOP_ARTICULATED_VEHICLE).
#
# Kotva spritu (bod -xoffs, -yoffs, ktery hra polozi na RemapCoords(poloha + bounds.origin + bounds.offset)):
# konvence VW T1 orig size (temata3.md, "Konvence VW T1 origsize"; hrac: "podle linky mezi koly"),
# zrcadlove srovnana (hrac 28. 9.: "a zrcadlova verifikace stredu"): kotva proti bodu na zemi pod
# stredem auta je vodorovne 10,0 * sin a, svisle -20,8 - 0,7 * cos a, a = 45 st. * smer. Casti, ktere
# nebyly zrcadlove (konstanta -5 px a 3,8 * cos a), jsou pryc: sever a jih maji kotvu na ose,
# dvojice SV/SZ, V/Z a JV/JZ jsou zrcadla. Stred auta = pul delky (V3S ma za zadni napravou dlouhou
# korbu, stred rozvoru je o metr blize k celu, auto by pak v zastavce a na vagonu stalo o metr dozadu).
# K tomu posun napric silnici do stredu pruhu CZTR (posun_do_pruhu), od verze 2: pruhy hry nesedi na
# cary CZTR stejne ve vsech smerech, JV jezdil po krajnici a JZ po prostredni care (hrac 28. 9.).
import os, sys, json, math, re
from PIL import Image

VEL, FOTKY, VYSTUP = sys.argv[1], sys.argv[2], sys.argv[3]
TU = os.path.dirname(os.path.abspath(__file__))
CUMAK = {"mala": 0, "velka": 2}[VEL]           # delka neviditelneho cumaku v osminach, 0 = bez cumaku

# Verze: kazde sestaveni pro hrace o jednu vys, je ve jmenu souboru i v Action14 (VRSN).
# 1 prvni vydani, 2 jmeno "V3S Praga" zlute bez "for", texty bez "communist", zelena kupka na MARI
VERZE = 2
JMENO = {"mala": "Praga_V3S", "velka": "Praga_V3S_BRYLE"}[VEL] + f"-v{VERZE}"
GRF_ID = {"mala": "MAXd", "velka": "MAXe"}[VEL]
PNG32 = f"{JMENO}-32bpp-zin4.png"; PNG8 = f"{JMENO}-8bpp.png"

def kotva_zrcadlova(d):
    """kotva spritu proti bodu na zemi pod stredem auta, px zin4 (vodorovne, svisle), zrcadlove srovnana"""
    a = math.radians(45 * d)
    return 10.0 * math.sin(a), -20.8 - 0.7 * math.cos(a)

# Pruh na silnici CZTR (hrac 28. 9.: "zarovnej to znova na silnici cztr", "nemuze jezdit kolem po prostredni
# care", "odstup jako od krajnice, par pixelu", "tak neco zkus mezi tim"). Hra vede auto v pruhu na 9 (SV, JV)
# nebo 5 (JZ, SZ) jednotkach dlazdice a kresli ho na poloha + (-2, -1) (SV, JZ) nebo (-1, -2) (JV, SZ).
# Stred pruhu mezi bilou krajnici a prostredni carou, zmereny na spritech CZTR RT14 "1. trida - venkov"
# (hra/cztr_silnice): silnice podel X (SV, JZ) 10,2 a 6,33, silnice podel Y (JV, SZ) 9,66 a 5,79.
# smer: (osa napric, pruh hry, posun kresleni napric, stred pruhu CZTR)
PRUH_CZTR = {1: ("y", 9, -1, 10.2), 3: ("x", 9, -1, 9.66), 5: ("y", 5, -1, 6.33), 7: ("x", 5, -1, 5.79)}
# Doladeni od hrace podle nahledu, px zin4 (vodorovne, svisle). Hrac 28. 9.: "velka jihozapad malicko
# na jihovychod pixelik, mala jihozapad taky" (jihovychod je na obrazovce doprava dolu, 2 : 1).
DOLADENI = {5: (2, 1)}

def posun_do_pruhu(d):
    """posun obrazku v px zin4 (vodorovne, svisle), aby zem pod stredem auta byla ve stredu pruhu CZTR"""
    if d % 2 == 0:
        # S, V, J, Z jsou jen v zatackach: napul mezi sousednimi smery
        a, b = posun_do_pruhu((d - 1) % 8), posun_do_pruhu((d + 1) % 8)
        return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    osa, pruh, kresli, stred = PRUH_CZTR[d]
    du, dv = kotva_zrcadlova(d)
    # zem pod stredem auta je na obrazovce (-du, -dv) od kotvy; na mape x je (-8, 4) px, y je (8, 4) px (zin4)
    zx, zy = ((-dv) / 4 - (-du) / 8) / 2, ((-dv) / 4 + (-du) / 8) / 2
    o = stred - (pruh + kresli + (zx if osa == "x" else zy))      # o kolik jednotek napric posunout
    sx, sy = (-8 * o, 4 * o) if osa == "x" else (8 * o, 4 * o)
    dx, dy = DOLADENI.get(d, (0, 0))
    return sx + dx, sy + dy

def kotva_konvence(d):
    """kotva spritu proti bodu na zemi pod stredem auta, px zin4 (vodorovne, svisle): zrcadlova, posunuta do pruhu"""
    du, dv = kotva_zrcadlova(d)
    sx, sy = posun_do_pruhu(d)
    return du - sx, dv - sy

def nacti_sadu(nater):
    adr = os.path.join(FOTKY, f"{VEL}_{nater}")
    info = json.load(open(os.path.join(adr, "kotvy.json")))
    out = []
    for d in range(8):
        gx, gy = info["smery"][str(d)]["zem_stred"]
        du, dv = kotva_konvence(d)
        foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA")
        bb = foto.getbbox()
        out.append((foto.crop(bb), int(math.floor(bb[0] - (gx + du) + 0.5)), int(math.floor(bb[1] - (gy + dv) + 0.5))))
    return out

# ---------------------------------------------------------------- naklady
# Hrac 28. 9.: "vwt1 vozi vsechno, tam se inspiruj", "skoro vsechno". Zaklad je seznam VW T1 (0x0082, s MARI),
# bez skla ("stavebni materialy vsechny kody krome skla") a bez jidla (jidlo jen vojenska).
VW_T1 = ("PASS BEER MAIL GOOD BDMT ENSP FOOD FARM FMSP FRUT LVPT DYES PACK HOPS TEXT GLAS VPTS WDPR WOOL FISH "
         "PAPR SUGR NUTS JAVA MNSP COAT TYRE PIPE STWR STCB CMNT VENG POWR CIGR TBCO COLA BEAN FURN MPTS TATO "
         "BATT ELEC NODC TOYS FZDR SWET CTCD SOAP MEAT SEED OLSD CHSE CERA BUBL TOFF CCPR HWAR BRCK STBL FOCA "
         "PPWK RBAR SEAL STPP STTB TYCO WELD SESP LVST PUMP MARI").split()
BEZ = {"GLAS", "FOOD"}
# Pridano podle hrace: srot, ocel, motory, cely zelezny retezec Steeltownu (FIRS 5.2), repa, konopna vlakna,
# stavebni materialy. Kody z naklady.md nebo z FIRS 5.2 (rozbalene/firs-5.2.0).
PRIDANO = ("SCMT STEL STAL STST STSE STSH METL STIG STSL STBR STPL STSW "      # srot a ocel
           "IORE COAL COKE LIME QLME IRON SLAG FEAL CSTI VBOD PLNT "           # zelezny retezec Steeltown
           "SGBT FICR "                                                       # repa, konopna vlakna
           "GRVL SAND").split()                                               # stavebni
JEN_VOJENSKA = ["FOOD", "BOOM"]                   # jidlo a vybusniny jen vojenska
NAKLADY = {"modra": [k for k in VW_T1 if k not in BEZ] + [k for k in PRIDANO if k not in VW_T1]}
NAKLADY["vojenska"] = NAKLADY["modra"] + JEN_VOJENSKA
for _n in NAKLADY:
    assert len(NAKLADY[_n]) == len(set(NAKLADY[_n])), _n

# Odstin modre podle nakladu (hrac: "staveni C, cement a stavebni; tmava strojirenstvi D, A zbozi,
# B zemedelstvi"). Co neni v B, C ani D, je A.
ODSTIN = {}
for k in "TATO BEAN SGBT TBCO MARI FICR FMSP SEED OLSD LVST WOOL FRUT JAVA NUTS".split(): ODSTIN[k] = "B"
for k in "CMNT BDMT BRCK CCPR CERA GRVL SAND LIME QLME RBAR STSW".split(): ODSTIN[k] = "C"
for k in ("SCMT STEL STAL STST STSE STSH STWR STCB METL STIG STSL STBR STPL STBL STPP STTB PIPE IORE COAL COKE "
          "IRON SLAG FEAL CSTI FOCA VBOD VENG VPTS TYRE TYCO PLNT POWR MPTS ENSP MNSP HWAR PUMP SEAL PPWK WELD").split():
    ODSTIN[k] = "D"
assert all(k in NAKLADY["modra"] for k in ODSTIN), [k for k in ODSTIN if k not in NAKLADY["modra"]]

# prekladova tabulka: poradi z hracova vzoru (prekladova-tabulka-vzor.yagl), co ve vzoru neni, jde za MARI
vzor = open(os.path.join(TU, "..", "prekladova-tabulka-vzor.yagl"), encoding="utf-8").read()
blok = vzor[vzor.index("properties<GlobalSettings"):vzor.index("\n}\n")]
PORADI = re.findall(r'^\s+cargo_translation_table: "([^"]{4})";', blok, re.M)
assert len(PORADI) == 147 and PORADI[-1] == "MARI", len(PORADI)
_pouzite = set(NAKLADY["vojenska"])
TABULKA = [k for k in PORADI if k in _pouzite] + [k for k in NAKLADY["vojenska"] if k not in PORADI]
INDEX = {k: i for i, k in enumerate(TABULKA)}

KAPACITA = 10                                      # jednotek beznych nakladu
LIDI = {"modra": 3, "vojenska": 20}                # hrac: "modra 3 osoby, vojenska nevim, hodne"

# ---------------------------------------------------------------- sprity a list
SADY = {"vojenska": ["vojenska"], "modra": ["modra_A", "modra_B", "modra_C", "modra_D"]}
# naložena marihuanou: zelena kupka na korbe (hrac 28. 9.: "udelej tam zelenou kupicku naklad"),
# u modre v odstinu B jako ostatni zemedelske naklady
KUPKA = {"vojenska": ("vojenska", "vojenska_kupka"), "modra": ("modra_B", "modra_B_kupka")}
vse = {nat: nacti_sadu(nat) for v in SADY.values() for nat in v}
vse.update({k[1]: nacti_sadu(k[1]) for k in KUPKA.values()})
os.makedirs(os.path.join(VYSTUP, "sprites"), exist_ok=True)
ODST = 6; SIRKA = 1024
polozky = [((nat, i), vse[nat][i][0]) for nat in vse for i in range(8)]
x = y = ODST; radek = 0; pozice = {}
for klic, im in polozky:
    if x + im.width + ODST > SIRKA: x = ODST; y += radek + ODST; radek = 0
    pozice[klic] = (x, y); x += im.width + ODST; radek = max(radek, im.height)
PRAZDNY = (SIRKA - ODST - 1, ODST)                 # 1x1 pruhledny pixel pro neviditelny cumak
list32 = Image.new("RGBA", (SIRKA, y + radek + ODST), (0, 0, 0, 0))
for klic, im in polozky: list32.alpha_composite(im, pozice[klic])
list32.save(os.path.join(VYSTUP, "sprites", PNG32))
list8 = Image.new("P", (16, 16), 0); list8.putpalette([0, 0, 255] + [0, 0, 0] * 255)
list8.save(os.path.join(VYSTUP, "sprites", PNG8))

sid = [1]
def sprite(nat=None, i=None):
    out = [f"        sprite_id<0x{sid[0]:08X}>", "        {",
           f'            [1, 1, 0, 0], normal, c8bpp, "{PNG8}", [4, 4];']
    if nat is None:
        out.append(f'            [1, 1, 0, 0], zin4, c32bpp, "{PNG32}", [{PRAZDNY[0]}, {PRAZDNY[1]}];')
    else:
        im, xo, yo = vse[nat][i]; px, py = pozice[(nat, i)]
        out.append(f'            [{im.width}, {im.height}, {xo}, {yo}], zin4, c32bpp | chunked, "{PNG32}", [{px}, {py}];')
    out.append("        }"); sid[0] += 1
    return out

# ---------------------------------------------------------------- texty
ITCH = "https://karel-macha.itch.io/openttd-decouple-by-karel-macha"
DECOUPLE = "ottd Decouple by Karel Mácha"
PODPIS = "{new-line}{green}" + DECOUPLE + "{new-line}" + ITCH
NAZEV = {"vojenska": "Praga V3S Vejtřaska (vojenská)", "modra": "Praga V3S Vejtřaska (modrá)"}
UVEDENI = "1952/2/20"                              # prvni funkcni prototyp V3S, Praha-Vysocany 20. 2. 1952
TECH = ("Výrobce: {gold}Praga, od 1964 Avia{black}{new-line}"
        "Motor: {gold}Tatra 912, řadový šestiválec 7,4 l{black}{new-line}"
        "Uspořádání: {gold}6×6{black}{new-line}Nosnost: {gold}5 t na silnici, 3 t v terénu{black}{new-line}"
        "Délka: {gold}6,91 m{black}{new-line}Model: {gold}hans1240 (Sketchfab), CC BY 4.0")
POPIS = {
    "vojenska": ("{lt-green}Praga V3S, vejtřaska. Vojenský valník 6×6, vozí vojáky na korbě, jídlo, výbušniny "
                 "a skoro všechno ostatní." + PODPIS + "{black}{new-line}" + TECH),
    "modra": ("{lt-green}Praga V3S, vejtřaska. Civilní modrý valník, odstín podle nákladu: "
              "světlá stavby, tmavá strojírenství, zemědělství a zboží. V kabině tři lidi, na korbě skoro všechno."
              + PODPIS + "{black}{new-line}" + TECH),
}
TEXT = {"vojenska": 0x01, "modra": 0x02}           # D001, D002
ZVUKY_ADR = os.path.join(TU, "zvuky")               # umely zvuk motoru (zvuky/syntetizuj_zvuky.py)
_zj = os.path.join(ZVUKY_ADR, "zvuky.json")
ZV = json.load(open(_zj)) if os.path.exists(_zj) else {}
BARVA = {"mala": "{gold}", "velka": "{lt-blue}"}[VEL]
# hrac 28. 9.: "ve jmenu vynech for, jen zlute V3S Praga, zelene ottd Decouple by Karel Macha";
# symbol nakladaku v barve varianty na konci zustal (rozlisuje malou a velkou, jako Sergej)
GRF_JMENO = "{yellow}V3S Praga{green} ottd Decouple by Karel Macha " + BARVA + "{truck}"
VARIANTA_POPIS = {"mala": "CZTR scale, 12.2 px/m, one road vehicle slot (8/8)",
                  "velka": "BRÝLE, magnified +20 %, 14.64 px/m, invisible front bumper keeps the queue "
                           "spacing (articulated: drive-through stops only)"}[VEL]
POPIS_GRF = ("{yellow}V3S Praga{green}  {truck} {new-line}"
             "{green}Praga V3S military, Praga V3S blue  " + BARVA + "{truck}  {truck}  {truck}{new-line}" +
             BARVA + VARIANTA_POPIS + "{new-line}"
             "{orange}Two 6×6 flatbed trucks that carry almost everything. Military: troops, food and explosives too. "
             "Blue: three people in the cab, the shade follows the cargo (building, engineering, farming, goods). "
             "Marijuana rides as a green heap. Prototype from 1952.{new-line}"
             "{orange}3D: Praga V3S, hans1240 (sketchfab.com/hans1240), CC BY 4.0{new-line}" +
             ("{orange}Sound: synthesized after the Tatra 912 engine, revs up when pulling away{new-line}" if ZV else "") +
             "{new-line}"
             "{green}ottd decouple by Karel Mácha " + BARVA + "{truck}{new-line}"
             "{green}" + ITCH + "{new-line}"
             "{green}GRF: Karel Mácha, licence CC BY 4.0")

# ---------------------------------------------------------------- yagl
Y = ['yagl_version: "";', "grf_format: Container2;",
     "optional_info // Action14", "{", "    INFO: ", "    {",
     f'        URL_: default, "{ITCH}";',
     f"        VRSN: [ 0x{VERZE:02X} 0x00 0x00 0x00 ];", "        MINV: [ 0x01 0x00 0x00 0x00 ];", "        NPAR: [ 0x00 ];",
     "        PALS: [ 0x44 ];", "        BLTR: [ 0x33 ];", "    }", "}",
     "grf // Action08", "{", f'    grf_id: "{GRF_ID}";', "    version: GRF8;", f'    name: "{GRF_JMENO}";',
     f'    description: "{POPIS_GRF}";', "}",
     "properties<GlobalSettings, 0x0000> // Action00, prekladova tabulka nakladu", "{"]
for i, k in enumerate(TABULKA):
    Y += [f"    // instance_id: 0x{i:04X}", "    {", f'        cargo_translation_table: "{k}";', "    }"]
Y += ["}", "strings<RoadVehicles, default, 0xD001*> // Action04, popisy v nakupnim okne", "{"]
for n in ("vojenska", "modra"):
    Y.append(f'    /* 0xD0{TEXT[n]:02X} */ "{POPIS[n]}";')
Y.append("}")

# ---------------------------------------------------------------- zvuk
# Umely zvuk motoru (zvuky/syntetizuj_zvuky.py, zvuky.json) pres Action11 a callback 0x33, jako Sergej
# (sergej/zvuky/README.md). Silnicni auto dostava udalosti (var 0x10): 1 = odjezd ze zastavky a z depa
# (StartRoadVehSound), 7 = kazdych 16 tiku v jizde, 8 = kazdych 16 tiku ve stani (vehicle.cpp), 3 = porucha.
# Vola se jen pro prvni dil (u velke cumak). Rychlost (var 0xB4) je u silnicnich aut v polovinach km/h.
# Bez zvuky.json se GRF zabali bez zvuku (odjezd pak hraje vychozi zvuk hry, vlastnost sound_effect_type).
SOUBORY = []                                      # jedinecne wav v poradi Action11, cisla od 0x49
def cislo_zvuku(f):
    if f not in SOUBORY: SOUBORY.append(f)
    return 0x49 + SOUBORY.index(f)
if ZV:
    import shutil
    cislo_zvuku(ZV["1"])
    for _p in ZV["jizda"]:
        for _f in _p["zvuky"]: cislo_zvuku(_f)
    for _f in ZV["stani"]: cislo_zvuku(_f)
    Y += ["sound_effects // Action11, vlastni zvuky od 0x49", "{"]
    for f in SOUBORY:
        shutil.copy(os.path.join(ZVUKY_ADR, f), os.path.join(VYSTUP, "sprites", f))
        Y += [f"    sprite_id<0x{sid[0]:08X}>", "    {", f'        binary("sprites/{f}");', "    }"]
        sid[0] += 1
    Y += ["}"]

def seznam(n):
    return "[ " + " ".join(f"0x{INDEX[k]:02X}" for k in NAKLADY[n]) + " ]"

def sw(cid, popis, vyraz, rozsahy, default):
    """switch v yaglu; rozsahy = [(hodnota, cil)] nebo [(od, do, cil)]"""
    r = [f"switch<RoadVehicles, 0x{cid:02X}, PrimaryDWord> // {popis}", "{", "    expression:", "    {"]
    r += ["        " + v for v in vyraz] + ["    };", "    ranges:", "    {"]
    for rz in rozsahy:
        od, do, cil = rz if len(rz) == 3 else (rz[0], rz[0], rz[1])
        r.append(f"        0x{od:08X}: 0x{cil:04X};" if od == do else f"        0x{od:08X}..0x{do:08X}: 0x{cil:04X};")
    r += ["    };", f"    default: 0x{default:04X};", "}"]
    return r

def zvukovy_retez(cid):
    """switche pro callback 0x33 od id cid; vraci (radky, id prepinace udalosti, dalsi volne id)"""
    if not ZV: return [], None, cid
    P = ZV["perioda_tiku"]; r = []
    def vyber(popis, soubory):
        nonlocal cid
        k = len(soubory); mid = cid; cid += 1
        r.extend(sw(mid, popis, [f"value1 = variable[0x0A] & 0x0000FFFF / 0x{P:08X};", f"value2 = variable[0x1A] & 0x{k:08X};",
                                 "value1 = UnsignedMod(value1, value2);"],
                    [(i, 0x8000 | cislo_zvuku(f)) for i, f in enumerate(soubory)], 0x8000 | cislo_zvuku(soubory[0])))
        return mid
    pasma = [vyber(f"jizda, pasmo {i} (do {p['do_kmh']} km/h, {p['otacky']} ot./min)", p["zvuky"]) for i, p in enumerate(ZV["jizda"])]
    id_stani = vyber("stani, volnobeh", ZV["stani"])
    id_rychlost, id_brana_j, id_brana_s, id_udalost = cid, cid + 1, cid + 2, cid + 3
    cid += 4
    rozsahy, od = [], 0
    for i, p in enumerate(ZV["jizda"][:-1]):
        rozsahy.append((od, 2 * p["do_kmh"], pasma[i])); od = 2 * p["do_kmh"] + 1
    r.extend(sw(id_rychlost, "rychlost (var 0xB4, poloviny km/h) -> pasmo", ["value1 = variable[0xB4] & 0x0000FFFF;"],
                rozsahy, pasma[-1]))
    brana = [f"value1 = variable[0x0A] & 0x0000FFFF % 0x{P:08X};"]
    r.extend(sw(id_brana_j, f"jizda: jednou za {P} tiku", brana, [(0, 15, id_rychlost)], 0xFFFF))
    r.extend(sw(id_brana_s, f"stani: jednou za {P} tiku", brana, [(0, 15, id_stani)], 0xFFFF))
    r.extend(sw(id_udalost, "zvuky (callback 0x33): 1 odjezd (rozjezd), 7 jizda, 8 stani", ["value1 = variable[0x10] & 0x000000FF;"],
                [(1, 0x8000 | cislo_zvuku(ZV["1"])), (7, id_brana_j), (8, id_brana_s)],
                0x7FFF))   # ostatni udalosti: callback selze a hra pusti svuj zvuk (porucha); 0xFFFF by bylo ticho
    return r, id_udalost, cid

def action3(eid, default, naklady):
    """naklady: [(index v tabulce, id retezce)], 0xFF = nakup"""
    r = ["feature_graphics<RoadVehicles> // Action03", "{", "    livery_override: false;", f"    default_set_id: 0x{default:04X};",
         f"    feature_ids: [ 0x{eid:04X} ];", "    cargo_types:", "    {"]
    r += [f"        0x{c:02X}: 0x{g:04X};" for c, g in naklady]
    return r + ["    };", "}"]

CALLBACK = ["value1 = variable[0x0C] & 0x0000FFFF;"]
ID = {"vojenska": 0x0100, "modra": 0x0101}         # kupovane cislo (u velke cumak)
ID_AUTO = {"vojenska": 0x0110, "modra": 0x0111}    # u velke viditelne auto, druhy clanek
for n in ("vojenska", "modra"):
    h = ID[n]; auto = ID_AUTO[n] if CUMAK else h
    base = {"vojenska": 0x10, "modra": 0x40}[n]
    kap_cumak = 1 if CUMAK else 0                  # cumak nese jednu jednotku (CUMAK.md: motor s nulovou
    kap_auto = KAPACITA - kap_cumak                #  kapacitou prijde o nabidku nakladu), auto zbytek
    lidi_auto = LIDI[n] - kap_cumak                # osoby: auto dostane zbytek callbackem 0x15
    Y += [f"// ---------------- {NAZEV[n]}"]
    dily = [(h, "cumak")] + [(auto, "auto")] if CUMAK else [(h, "auto")]
    for eid, co in dily:
        p = [f"properties<RoadVehicles, 0x{eid:04X}> // Action00 ({co})", "{", "    {",
             f"        long_introduction_date: date({UVEDENI});", "        model_life_years: 255;",
             "        vehicle_life_years: 15;", "        reliability_decay_speed: 20;",
             "        refittable_cargo_classes: 0x0000;", "        non_refittable_cargo_classes: 0x0000;",
             "        refit_cargo_types: 0x00000000;",
             f"        always_refittable_cargos: {seznam(n)};", "        never_refittable_cargos: [ ];",
             f"        cargo_type: 0x{INDEX['GOOD']:02X};", "        loading_speed: 0x05;", "        refit_cost: 0x00;",
             "        sprite_id: 0xFF;", "        miscellaneous_flags: 0x00;",
             f"        cargo_capacity: 0x{(kap_cumak if co == 'cumak' else kap_auto):02X};",
             f"        shorten_vehicle: 0x{(8 - CUMAK) if co == 'cumak' else 0:02X};"]
        if eid == h:
            p += ["        climate_availability: Temperate | Arctic | Tropical | Toyland;",
                  "        speed_2_kmh: 0x78;",               # 60 km/h
                  "        power_10_hp: 0x0A;",               # Tatra 912, kolem 100 k
                  "        weight_quarter_tons: 0x16;",       # 5,5 t (pohotovostni 5,47 t)
                  "        cost_factor: 0x40;", "        running_cost_factor: 0x2C;",
                  "        running_cost_base: 0x00004C48;",
                  "        sound_effect_type: 0x17;"]         # odjezd nakladaku (SND_19_DEPARTURE_OLD_RV_1)
        maska = 0x10 if co == "cumak" else 0x08            # cumak: clanky (0x16); auto: kapacita (0x15)
        if eid == h and ZV: maska |= 0x80                   # prvni dil: zvuky motoru (callback 0x33)
        p += [f"        callback_flags_mask: 0x{maska:02X};"]
        Y += p + ["    }", "}", f"strings<RoadVehicles, default, 0x{eid:04X}> // Action04", "{",
                  f'    /* 0x{eid:04X} */ "{NAZEV[n] if eid == h else NAZEV[n] + " (auto)"}";', "}"]
    # Action01: sady auta (8 smeru, u modre ctyri odstiny), auto se zelenou kupkou (marihuana)
    # a prazdna sada pro cumak
    sady = SADY[n]
    lak_mari, sada_kupka = KUPKA[n]
    i_kupka, i_prazdny = len(sady), len(sady) + 1
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01", "{"]
    for si, nat in enumerate(sady + [sada_kupka]):
        Y += [f"    sprite_set // 0x{si:04X} {nat}", "    {"]
        for i in range(8): Y += sprite(nat, i)
        Y += ["    }"]
    Y += [f"    sprite_set // 0x{i_prazdny:04X} prazdny cumak", "    {"]
    for i in range(8): Y += sprite()
    Y += ["    }", "}"]
    g = {nat: base + si for si, nat in enumerate(sady)}
    g_prazdny = base + len(sady)
    g_mari = base + len(sady) + 1
    for si, nat in enumerate(sady):
        Y += [f"sprite_groups<RoadVehicles, 0x{g[nat]:02X}> // Action02 basic, {nat}", "{",
              f"    primary_spritesets: [ 0x{si:04X} ];", f"    secondary_spritesets: [ 0x{si:04X} ];", "}"]
    Y += [f"sprite_groups<RoadVehicles, 0x{g_prazdny:02X}> // Action02 basic, prazdny cumak", "{",
          f"    primary_spritesets: [ 0x{i_prazdny:04X} ];", f"    secondary_spritesets: [ 0x{i_prazdny:04X} ];", "}"]
    # marihuana: prazdne auto, od poloviny nakladu kupka (hra bere sadu naklad * pocet / kapacita)
    i_lak = sady.index(lak_mari)
    Y += [f"sprite_groups<RoadVehicles, 0x{g_mari:02X}> // Action02 basic, marihuana: prazdne, kupka", "{",
          f"    primary_spritesets: [ 0x{i_lak:04X} 0x{i_kupka:04X} ];",
          f"    secondary_spritesets: [ 0x{i_lak:04X} 0x{i_kupka:04X} ];", "}"]
    # obrazek do nakupu: smer W, u modre odstin A (vychozi naklad je zbozi)
    g_nakup = base + 8
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, obrazek do nakupu", "{", "    sprite_set // 0x0000 nakup", "    {"]
    Y += sprite(sady[0], 6)
    Y += ["    }", "}", f"sprite_groups<RoadVehicles, 0x{g_nakup:02X}> // Action02 basic, nakup", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    s_clanky, s_lidi, s_nakup, s_cumak = base + 9, base + 10, base + 11, base + 12
    zaklad = g[sady[0]]                            # vojenska, u modre odstin A
    zvuk_radky, id_zvuk, volne = zvukovy_retez(base + 13)
    Y += zvuk_radky
    zvuk = [(0x33, id_zvuk)] if id_zvuk else []
    # osoby: callback 0x15 vrati kapacitu, jinak grafika (u modre odstin A); u male i zvuk
    Y += sw(s_lidi, f"osoby: kapacita {'auta ' if CUMAK else ''}{lidi_auto}", CALLBACK,
            [(0x15, 0x8000 | lidi_auto)] + ([] if CUMAK else zvuk), zaklad)
    popis_nakup = [(0x23, 0x8000 | TEXT[n])]
    if CUMAK:
        Y += sw(s_clanky, "clanky (callback 0x16): 1 = viditelne auto, dal nic", ["value1 = variable[0x10] & 0x000000FF;"],
                [(1, 0x8000 | auto)], 0xFFFF)
        Y += sw(s_cumak, "cumak: clanky, zvuky, jinak prazdny sprite", CALLBACK, [(0x16, s_clanky)] + zvuk, g_prazdny)
        Y += sw(s_nakup, "nakup: clanky, popis, obrazek", CALLBACK, [(0x16, s_clanky)] + popis_nakup, g_nakup)
        Y += action3(h, s_cumak, [(0xFF, s_nakup)])
    else:
        Y += sw(s_nakup, "nakup: popis, obrazek", CALLBACK, popis_nakup, g_nakup)
    # viditelne auto: odstin podle nakladu (jen modra), osoby pres kapacitni callback
    mapa = {INDEX["PASS"]: s_lidi}
    if n == "modra":
        mapa.update({INDEX[k]: g["modra_" + o] for k, o in ODSTIN.items() if o != "A"})
    mapa[INDEX["MARI"]] = g_mari                    # kupka (u modre v odstinu B)
    vychozi = zaklad
    if not CUMAK and id_zvuk:
        # mala: Action 3 vybira podle nakladu a callback 0x33 jde stejnou cestou, tak kazdy cil grafiky
        # dostane obal "zvuk, jinak grafika" (osoby uz zvuk maji v s_lidi)
        obal = {}
        for cil in [zaklad] + sorted(set(mapa.values()) - {s_lidi, zaklad}):
            obal[cil] = volne + len(obal)
            Y += sw(obal[cil], "zvuk, jinak grafika", CALLBACK, zvuk, cil)
        mapa = {k: obal.get(v, v) for k, v in mapa.items()}
        vychozi = obal[zaklad]
        assert volne + len(obal) <= base + 0x30, "switche se prekryvaji s dalsim autem"
    if not CUMAK:
        mapa[0xFF] = s_nakup
    Y += action3(auto, vychozi, sorted(mapa.items()))

open(os.path.join(VYSTUP, "sprites", f"{JMENO}.yagl"), "w").write("\n".join(Y) + "\n")
souhrn = {"tabulka": TABULKA, "naklady": NAKLADY, "odstin": ODSTIN,
          "sprity": {nat: [[im.width, im.height, xo, yo] for im, xo, yo in vse[nat]] for nat in vse}}
json.dump(souhrn, open(os.path.join(VYSTUP, f"{JMENO}-souhrn.json"), "w"), indent=1, ensure_ascii=False)
print(JMENO, "spritu", sid[0] - 1, "list", list32.size, "tabulka", len(TABULKA), "nakladu",
      {n: len(v) for n, v in NAKLADY.items()}, "odstiny B/C/D", {o: sum(1 for v in ODSTIN.values() if v == o) for o in "BCD"})
