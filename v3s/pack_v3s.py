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
# 1 prvni vydani, 2 jmeno "V3S Praga" zlute bez "for", texty bez "communist", zelena kupka na MARI, pruhy CZTR, zvuk,
# 3 tmava leskla okna a bile reflektory, prikladaci naklady (vrstva nad autem, barva podle nakladu, klady, prkna),
# 4 naklady hracovym systemem (cela tabulka ze vzoru, vypsany seznam, bez trid), brambory zlute, cement sedy,
#   prikladaci plachta na vsechno, co neni kupka,
# 5 chemikalie v kanystrech pod plachtou (obe), radioaktivni naklad jen vojenska, hracky jen modra
VERZE = 5
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
        if bb is None:                             # naklad v tomhle smeru cely za bocnici
            out.append((Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0, 0)); continue
        out.append((foto.crop(bb), int(math.floor(bb[0] - (gx + du) + 0.5)), int(math.floor(bb[1] - (gy + dv) + 0.5))))
    return out

# ---------------------------------------------------------------- naklady
# Od verze 4 hracuv system (temata3.md, "Jak hrac dela GRF"; hrac 28. 9.: "ja chci abys pouzival muj system mapovani
# nakladu, at se v tom yaglu vyznam", "muj system je jasnej, vidis hned"):
#  - prekladova tabulka je cely hracuv vzor prekladova-tabulka-vzor.yagl, ve stejnem poradi a se stejnymi cisly
#    (MARI 0x92), kody vejtrasky, ktere ve vzoru nejsou (NAVIC), jdou za MARI;
#  - kazde auto ma vypsany seznam, co vozi (vlastnost 24, always_refittable_cargos), tridy nakladu 0 a seznam nikdy
#    povolenych prazdny, jako VW T1. Co v seznamu neni, auto nevozi, v zadne hre.
# Co vozi: vsechno z tabulky krome NEVOZI (hrac: "napis vsechno vozi", "co nevozi vyjmenuj krom tekutin", "alkohol
# vozime, pivo v base", "svarovaci material a jidlo nech, barvy nech, cistici prostredky taky nech, to neni tekuty ve
# flaskach, vojenske jidlo jo"). Marihuana (MARI) je v seznamu jmenem, jako v kazdem normalnim GRF.
NEVOZI = {                                         # nevozi ani jedna
    "OIL_": "ropa", "OILD": "ropa", "OILI": "ropa", "PETR": "benzín", "RFPR": "rafinované produkty",
    "FUEL": "zemní plyn", "CTAR": "dehet", "MILK": "mléko", "WATR": "voda", "EOIL": "jedlý olej", "MOLS": "melasa",
    "ACID": "kyselina", "LYE_": "louh", "CHLO": "chlor", "NH3_": "čpavek", "O2__": "kyslík",     # tekutiny a plyny
    "GLAS": "sklo", "ELTR": "elektřina", "GEAR": "přeřazení lokomotivy"}
JEN_VOJENSKA = {"FOOD": "potraviny", "BOOM": "výbušniny",   # modra je nevozi (hrac: "jidlo jenom vojensky",
                "URAN": "uran", "NUKF": "jaderné palivo",     # "vojenska explosives, modra ne", 29. 9.:
                "NUKW": "jaderný odpad"}                      # "vojenska radioaktivni veci, modra ne")
JEN_MODRA = {"TOYS": "hračky"}                               # vojenska je nevozi (hrac 29. 9.: "vojenska ne hracky")
# Kody vejtrasky, ktere ve vzoru nejsou: nezname labely ze seznamu VW T1 (naklady.md, "Labely, ktere v zadne tabulce
# nejsou"; hrac je ma, tak zustaly) a FIRS 5.2 Steeltown (naklady.md). Jdou do tabulky za MARI.
NAVIC = {
    "FARM": "? (z VW T1, význam neznámý)", "LVPT": "? (z VW T1, význam neznámý)", "HOPS": "? (z VW T1, význam neznámý)",
    "ELEC": "? (z VW T1, význam neznámý)", "NODC": "? (z VW T1, význam neznámý)",
    "CCPR": "betonové výrobky  [Concrete Products]", "HWAR": "železářské zboží  [Hardware]",
    "STBL": "předvalky  [Billets & Blooms]", "FOCA": "výkovky a odlitky  [Forgings & Castings]",
    "PPWK": "nádrže a potrubí  [Storage Tanks & Pipework]", "RBAR": "betonářská ocel  [Rebar]",
    "SEAL": "těsnění, hadice a řemeny  [Seals, Hoses & Belts]", "STPP": "ocelové trubky  [Steel Pipe]",
    "STTB": "ocelové trubky, tenkostěnné  [Steel Tube]", "TYCO": "kord do pneumatik  [Tyre Cord]",
    "WELD": "svařovací materiál  [Welding Consumables]", "PUMP": "čerpadla a ventily  [Pumps & Valves]",
    "STIG": "ocelové ingoty  [Steel Ingots]", "STSL": "bramy  [Steel Slab]", "STBR": "tyčová ocel  [Merchant Bar]",
    "STPL": "ocelový plech  [Steel Plate]", "STSW": "konstrukční ocel  [Structural Steel]",
    "FEAL": "feroslitiny  [Ferroalloys]", "PLNT": "stroje a zařízení  [Plant & Machinery]",
    # od verze 5 (hrac 29. 9.: "budem vozit i chemikalie, to je dulezity v prumyslu. plachta jako ze veze chemikalie
    # v kanystrech pod plachtou"); FIRS ho ma v ekonomikach 0, 3 a 4
    "CHEM": "chemikálie  [Chemicals] (FIRS), vejtřaska je veze v kanystrech pod plachtou"}

# prekladova tabulka: cely hracuv vzor (i s jeho poznamkami a nadpisy oddilu), za MARI kody NAVIC
vzor = open(os.path.join(TU, "..", "prekladova-tabulka-vzor.yagl"), encoding="utf-8").read()
blok = vzor[vzor.index("properties<GlobalSettings"):vzor.index("\n}\n")]
PORADI, POZNAMKA, ODDIL = [], {}, {}
for _r in blok.split("\n"):
    _m = re.match(r'\s+cargo_translation_table: "([^"]{4})";\s*//\s*(.*?)\s*$', _r)
    if _m:
        PORADI.append(_m.group(1)); POZNAMKA[_m.group(1)] = _m.group(2)
    elif _r.strip().startswith("// ----"):
        ODDIL[len(PORADI)] = _r.strip()
assert len(PORADI) == 147 and PORADI.index("MARI") == 0x92, len(PORADI)
assert not set(NAVIC) & set(PORADI), set(NAVIC) & set(PORADI)
ODDIL[len(PORADI)] = "// ---- NAVÍC PRO VEJTŘASKU — ve vzoru nejsou ----"
POZNAMKA.update(NAVIC)
TABULKA = PORADI + list(NAVIC)
INDEX = {k: i for i, k in enumerate(TABULKA)}
assert all(k in INDEX for k in list(NEVOZI) + list(JEN_VOJENSKA) + list(JEN_MODRA))
NAKLADY = {"vojenska": [k for k in TABULKA if k not in NEVOZI and k not in JEN_MODRA],
           "modra": [k for k in TABULKA if k not in NEVOZI and k not in JEN_VOJENSKA]}
# lide: cestujici, turiste, delnici; kapacitu jim dava callback 0x15 (vojenska 20, modra 3)
LIDE = ["PASS", "TOUR", "OTI1", "OTI2", "YETI", "YETY"]

# Odstin modre podle nakladu (hrac: "staveni C, cement a stavebni; tmava strojirenstvi D, A zbozi,
# B zemedelstvi"). Co neni v B, C ani D, je A. Od verze 4 i naklady, ktere prisly s celou tabulkou
# (obili a plodiny B, jil a kaolin C, rudy a kovy D).
ODSTIN = {}
for k in ("TATO BEAN SGBT TBCO MARI FICR FMSP SEED OLSD LVST WOOL FRUT JAVA NUTS WOOD "
          "GRAI WHEA MAIZ CERE FRVG SGCN CASS TWOD FERT").split(): ODSTIN[k] = "B"
for k in "CMNT BDMT BRCK CCPR CERA GRVL SAND LIME QLME RBAR STSW CLAY KAOL".split(): ODSTIN[k] = "C"
for k in ("SCMT STEL STAL STST STSE STSH STWR STCB METL STIG STSL STBR STPL STBL STPP STTB PIPE IORE COAL COKE "
          "IRON SLAG FEAL CSTI FOCA VBOD VENG VPTS TYRE TYCO PLNT POWR MPTS ENSP MNSP HWAR PUMP SEAL PPWK WELD "
          "SULP RUBR AORE CORE NKOR PORE COPR ZINC NICK ALUM COBL MNO2 FECR SCRP VEHI").split():
    ODSTIN[k] = "D"
assert all(k in NAKLADY["modra"] for k in ODSTIN), [k for k in ODSTIN if k not in NAKLADY["modra"]]

KAPACITA = 10                                      # jednotek beznych nakladu
LIDI = {"modra": 3, "vojenska": 20}                # hrac: "modra 3 osoby, vojenska nevim, hodne"

# ---------------------------------------------------------------- sprity a list
SADY = {"vojenska": ["vojenska"], "modra": ["modra_A", "modra_B", "modra_C", "modra_D"]}
# Prikladaci naklady (hrac 28. 9.: "kupku prikladaci, udelame cernou kupku uhli a zlutou pisek a vsechny barvy a drevo
# udelej"): fotky render_v3s.py naklad_<KOD>, jen naklad, auto neviditelne, ale zakryva, co je za bocnicemi.
# Sypke naklady jako kupka v barve nakladu, drevo klady, drevarske vyrobky prkna. VRSTVY jsou obrazky, VRSTVA rika,
# ktery naklad jede s kterym obrazkem. Jeden obrazek pro vic nakladu stoji nula megabajtu navic (hrac 29. 9.:
# "jen kupicka je min mb", "pisek a brambory zluta, cement, sterk seda"): brambory (TATO, a BEAN, ktere ma CZIS
# prejmenovane na brambory) jedou se zlutou kupkou pisku, cement se sedou kupkou kamene, tropicke drevo s kladami,
# stary kod srotu SCRP se srotem.
VRSTVY = ["COAL", "COKE", "IORE", "LIME", "QLME", "SLAG", "SCMT", "GRVL", "SAND", "SGBT", "SEED", "OLSD", "NUTS",
          "MARI", "SULP", "WOOD", "WDPR"]
VRSTVA = {k: k for k in VRSTVY}
VRSTVA.update({"TATO": "SAND", "BEAN": "SAND", "CMNT": "GRVL", "TWOD": "WOOD", "SCRP": "SCMT"})
assert all(k in NAKLADY["modra"] for k in VRSTVA), [k for k in VRSTVA if k not in NAKLADY["modra"]]
# Plachta (hrac 29. 9.: "co neni kupka nech grafiku prazdne. udelame prikladaci plachtu. grafika stovky aut plny jednou
# plachtou. kdyz pojede plna, prilozime plachtu", "jidlo plachta", "vojensky vojenskou plachtu, a sedou", "modry zlutou
# sedobilou plachtu", "sedou dame u vojensky na ocelove retezce, strojirenstvi"): vsechno, co nejede jako kupka, jede
# nalozene pod plachtou (render_v3s.py naklad_plachta_<barva>). Vojenska olivova, ocel a strojirenstvi (odstin D) seda;
# modra zluta, ocel a strojirenstvi sedobila. Vojaci jedou pod plachtou, lide v modre sedi v kabine, ta plachtu nema.
PLACHTA = {"vojenska": ("plachta_vojenska", "plachta_seda"), "modra": ("plachta_zluta", "plachta_sedobila")}
OBRAZKY = VRSTVY + [p for v in PLACHTA.values() for p in v]
vse = {nat: nacti_sadu(nat) for v in SADY.values() for nat in v}
vse.update({f"naklad_{k}": nacti_sadu(f"naklad_{k}") for k in OBRAZKY})
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
# Hrac 29. 9.: "vubec slova army a military taky az na konec, ze tam teda je, nebo vubec ne, kdyz je to videt moc.
# to je hra, ale zelena je casta, castejsi nez modra, protoze je military, tak to tam vsude napis, v civilu jezdily
# rozprodane ze skladovych zasob armady": olivova je v textech zelena, armada jen na konci. (Jmena v kodu zustala.)
NAZEV = {"vojenska": "Praga V3S Vejtřaska (zelená)", "modra": "Praga V3S Vejtřaska (modrá)"}
ZELENA_CASTA = "Zelené byly nejčastější, v civilu jezdily vejtřasky rozprodané ze skladových zásob armády."
UVEDENI = "1952/2/20"                              # prvni funkcni prototyp V3S, Praha-Vysocany 20. 2. 1952
TECH = ("Výrobce: {gold}Praga, od 1964 Avia{black}{new-line}"
        "Motor: {gold}Tatra 912, řadový šestiválec 7,4 l{black}{new-line}"
        "Uspořádání: {gold}6×6{black}{new-line}Nosnost: {gold}5 t na silnici, 3 t v terénu{black}{new-line}"
        "Délka: {gold}6,91 m{black}{new-line}Model: {gold}hans1240 (Sketchfab), CC BY 4.0")
POPIS = {
    "vojenska": ("{lt-green}Praga V3S, vejtřaska. Zelený valník 6×6. Všechno vozí kromě tekutin, skla "
                 "a hraček, 20 lidí na korbě. " + ZELENA_CASTA + PODPIS + "{black}{new-line}" + TECH),
    "modra": ("{lt-green}Praga V3S, vejtřaska. Civilní modrý valník, odstín podle nákladu. Všechno vozí kromě "
              "tekutin, skla, jídla, výbušnin a radioaktivních věcí, v kabině tři lidi. " + ZELENA_CASTA + PODPIS +
              "{black}{new-line}" + TECH),
}
TEXT = {"vojenska": 0x01, "modra": 0x02}           # D001, D002
ZVUKY_ADR = os.path.join(TU, "zvuky")               # umely zvuk motoru (zvuky/syntetizuj_zvuky.py)
_zj = os.path.join(ZVUKY_ADR, "zvuky.json")
ZV = json.load(open(_zj)) if os.path.exists(_zj) else {}
BARVA = {"mala": "{gold}", "velka": "{lt-blue}"}[VEL]
# hrac 28. 9.: "ve jmenu vynech for, jen zlute V3S Praga, zelene ottd Decouple by Karel Macha";
# symbol nakladaku v barve varianty na konci zustal (rozlisuje malou a velkou, jako Sergej)
GRF_JMENO = "{yellow}V3S Praga{green} ottd Decouple by Karel Macha " + BARVA + "{truck}"
# hrac 29. 9.: "nepis tam cztr scale, kdyz budes muset cztr, tak nekde na konci v rohu a radsi vubec. nejak se to
# jmenuje odborne, original size, a druhy radsi nepis vubec": mala "original size", velka bez radku
VARIANTA_POPIS = {"mala": "original size", "velka": ""}[VEL]
# Hrac 29. 9.: "ten zbytek, to ti rikam, nemenuj, co vozi, napis vsechno vozi a napis neco hezkyho o autu a neco
# duleziteho zelene for decouple by karel macha. to melo pul motoru tatry ne?": Tatra 912 je polovina vidlicoveho
# dvanactivalce Tatra 111 (stejny valec 110 x 130 mm, 14,8 l / 2 = 7,4 l).
POPIS_GRF = ("{yellow}V3S Praga{green}  {truck} {new-line}"
             "{green}Praga V3S green, Praga V3S blue  " + BARVA + "{truck}  {truck}  {truck}{new-line}" +
             (BARVA + VARIANTA_POPIS + "{new-line}" if VARIANTA_POPIS else "") +
             "{orange}Carries everything.{new-line}"
             "{orange}The legendary vejtřaska, the 6×6 workhorse of Czechoslovakia from 1953 to 1990. Its air-cooled Tatra 912 diesel is half of the Tatra 111 V12: an inline six of 7.4 litres. " +
             ("It roars when pulling away and leaves the depot with the starter and a two-tone horn. " if ZV else "") +
             "The load shows on the bed as a heap, logs or a tarp. The green one is the common one: in civilian "
             "life they drove trucks sold off from army stock.{new-line}"
             "{orange}3D: Praga V3S, hans1240 (sketchfab.com/hans1240), CC BY 4.0{new-line}"
             "{new-line}"
             "{green}for ottd Decouple by Karel Mácha " + BARVA + "{truck}{new-line}"
             "{green}OpenTTD where trains couple and uncouple on the move{new-line}"
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
     "properties<GlobalSettings, 0x0000> // Action00, překladová tabulka nákladů: hráčův vzor "
     "prekladova-tabulka-vzor.yagl, stejná čísla, za MARI kódy navíc", "{"]
for i, k in enumerate(TABULKA):
    if i in ODDIL: Y.append("    " + ODDIL[i])
    Y += [f"    // instance_id: 0x{i:04X}", "    {", f'        cargo_translation_table: "{k}"; // {POZNAMKA[k]}', "    }"]
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
    if "1_depo" in ZV: cislo_zvuku(ZV["1_depo"])
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

def nevozi(n):
    """co auto nevozi, pro poznamku u seznamu"""
    nv = dict(NEVOZI, **(JEN_VOJENSKA if n == "modra" else JEN_MODRA))
    return ", ".join(f"{k} {v}" for k, v in nv.items())

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
    odjezd = 0x8000 | cislo_zvuku(ZV["1"])
    if "1_depo" in ZV:
        # vyjezd z depa: hra zvuk pousti, kdyz je auto jeste schovane v depu (vehstatus bit 0, var 0xB2),
        # u zastavky ne (roadveh_cmd.cpp, StartRoadVehSound); hrac: "vyjezd z depa motor s klaksonem"
        id_odjezd = cid; cid += 1
        r.extend(sw(id_odjezd, "odjezd: z depa startovani a klakson, ze zastavky rozjezd", ["value1 = variable[0xB2] & 0x00000001;"],
                    [(1, 0x8000 | cislo_zvuku(ZV["1_depo"]))], odjezd))
        odjezd = id_odjezd
    r.extend(sw(id_udalost, "zvuky (callback 0x33): 1 odjezd, 7 jizda, 8 stani", ["value1 = variable[0x10] & 0x000000FF;"],
                [(1, odjezd), (7, id_brana_j), (8, id_brana_s)],
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

# Prikladaci naklady: hra kresli auto z vic obrazku pres sebe (sprite stack, bit 7 vlastnosti miscellaneous_flags).
# Graficky retez prochazi pro kazdou vrstvu zvlast, cislo vrstvy je v promenne 0x10 (bity 8-15); kdyz ma prijit
# dalsi vrstva, zapise GRF do docasneho registru 0x100 bit 31 (newgrf_engine.cpp, GetCustomEngineSprite; registry
# se pred kazdou vrstvou nuluji). Vrstva 0 je auto, vrstva 1 naklad. Sady nakladu jsou spolecne pro obe auta
# (skupiny 0xC0 a dal), naklad je videt od poloviny nakladu (hra bere sadu naklad * pocet / kapacita).
G_VRSTVA = {}
if OBRAZKY:
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, prikladaci naklady a plachty (spolecne pro obe auta)", "{"]
    for si, k in enumerate(OBRAZKY):
        Y += [f"    sprite_set // 0x{si:04X} naklad {k}", "    {"]
        for i in range(8): Y += sprite(f"naklad_{k}", i)
        Y += ["    }"]
    i_nic = len(OBRAZKY)
    Y += [f"    sprite_set // 0x{i_nic:04X} bez nakladu", "    {"]
    for i in range(8): Y += sprite()
    Y += ["    }", "}"]
    for si, k in enumerate(OBRAZKY):
        G_VRSTVA[k] = 0xC0 + si
        Y += [f"sprite_groups<RoadVehicles, 0x{G_VRSTVA[k]:02X}> // Action02 basic, naklad {k}: prazdno, naklad", "{",
              f"    primary_spritesets: [ 0x{i_nic:04X} 0x{si:04X} ];",
              f"    secondary_spritesets: [ 0x{i_nic:04X} 0x{si:04X} ];", "}"]
VRSTVY_VYRAZ = ["value1 = variable[0x1A] & 0x00000001;", "value2 = variable[0x10] >> 8 & 0x000000FF;",
                "value1 = Subtraction(value1, value2);",                                          # 1 - vrstva
                "value2 = variable[0x1A] & 0x0000001F;", "value1 = ShiftLeft(value1, value2);",    # vrstva 0: bit 31
                "value2 = variable[0x1A] & 0x00000100;", "value1 = TempStore(value1, value2);",    # do registru 0x100
                "value2 = variable[0x10] >> 8 & 0x000000FF;", "value1 = Assign(value1, value2);"]  # vyber podle vrstvy

for n in ("vojenska", "modra"):
    h = ID[n]; auto = ID_AUTO[n] if CUMAK else h
    # cisla skupin a switchu: kazde auto znova od 0x10 (Action 3 predchoziho auta uz je hotova), naklady 0xC0 a dal
    dalsi = [0x10]
    def nove():
        i = dalsi[0]; dalsi[0] += 1
        assert i < 0xC0, "switche narazily na spolecne vrstvy nakladu"
        return i
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
             f"        // vozí všechno z tabulky kromě: {nevozi(n)}",
             f"        always_refittable_cargos: {seznam(n)};",
             "        never_refittable_cargos: [ ];",
             f"        cargo_type: 0x{INDEX['GOOD']:02X};", "        loading_speed: 0x05;", "        refit_cost: 0x00;",
             "        sprite_id: 0xFF;",
             f"        miscellaneous_flags: 0x{0x80 if (co == 'auto' and OBRAZKY) else 0:02X};",   # 0x80: vrstvy (sprite stack)
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
        maska = 0x18 if co == "cumak" else 0x08            # cumak: clanky (0x16) a lidi (0x15); auto: kapacita (0x15)
        if eid == h and ZV: maska |= 0x80                   # prvni dil: zvuky motoru (callback 0x33)
        p += [f"        callback_flags_mask: 0x{maska:02X};"]
        Y += p + ["    }", "}", f"strings<RoadVehicles, default, 0x{eid:04X}> // Action04", "{",
                  f'    /* 0x{eid:04X} */ "{NAZEV[n] if eid == h else NAZEV[n] + " (auto)"}";', "}"]
    # Action01: sady auta (8 smeru, u modre ctyri odstiny) a prazdna sada pro cumak
    sady = SADY[n]
    i_prazdny = len(sady)
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01", "{"]
    for si, nat in enumerate(sady):
        Y += [f"    sprite_set // 0x{si:04X} {nat}", "    {"]
        for i in range(8): Y += sprite(nat, i)
        Y += ["    }"]
    Y += [f"    sprite_set // 0x{i_prazdny:04X} prazdny cumak", "    {"]
    for i in range(8): Y += sprite()
    Y += ["    }", "}"]
    g = {nat: nove() for nat in sady}
    g_prazdny = nove()
    for si, nat in enumerate(sady):
        Y += [f"sprite_groups<RoadVehicles, 0x{g[nat]:02X}> // Action02 basic, {nat}", "{",
              f"    primary_spritesets: [ 0x{si:04X} ];", f"    secondary_spritesets: [ 0x{si:04X} ];", "}"]
    Y += [f"sprite_groups<RoadVehicles, 0x{g_prazdny:02X}> // Action02 basic, prazdny cumak", "{",
          f"    primary_spritesets: [ 0x{i_prazdny:04X} ];", f"    secondary_spritesets: [ 0x{i_prazdny:04X} ];", "}"]
    # obrazek do nakupu: smer W, u modre odstin A (vychozi naklad je zbozi)
    g_nakup = nove()
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, obrazek do nakupu", "{", "    sprite_set // 0x0000 nakup", "    {"]
    Y += sprite(sady[0], 6)
    Y += ["    }", "}", f"sprite_groups<RoadVehicles, 0x{g_nakup:02X}> // Action02 basic, nakup", "{",
          "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
    s_clanky, s_lidi, s_nakup, s_cumak = nove(), nove(), nove(), nove()
    zaklad = g[sady[0]]                            # vojenska, u modre odstin A
    zvuk_radky, id_zvuk, dalsi[0] = zvukovy_retez(dalsi[0])
    assert dalsi[0] < 0xC0
    Y += zvuk_radky
    zvuk = [(0x33, id_zvuk)] if id_zvuk else []
    # grafika viditelneho auta podle nakladu: auto (u modre v odstinu podle nakladu) a pres nej vrstva s kupkou nebo
    # plachtou; switch pro kazdou dvojici (obrazek, auto) jednou
    telo = lambda k: g["modra_" + ODSTIN.get(k, "A")] if n == "modra" else zaklad
    def obrazek(k):
        """obrazek nakladu k na korbe: kupka, jinak plachta; modra s lidmi nic (lide sedi v kabine)"""
        if k in VRSTVA: return VRSTVA[k]
        if n == "modra" and k in LIDE: return None
        return PLACHTA[n][1] if ODSTIN.get(k) == "D" else PLACHTA[n][0]
    vrstvy_sw = {}
    def grafika(k):
        obr, t = obrazek(k), telo(k)
        if obr is None: return t
        if (obr, t) not in vrstvy_sw:
            sv = nove(); vrstvy_sw[obr, t] = sv
            nat = [jm for jm, gg in g.items() if gg == t][0]
            Y.extend(sw(sv, f"vrstvy: {nat} a pres nej {obr} (vrstva 0 auto a dalsi vrstva, 1 naklad)", VRSTVY_VYRAZ,
                        [(1, G_VRSTVA[obr])], t))
        return vrstvy_sw[obr, t]
    vychozi_g = grafika("GOOD")                    # vychozi naklad zbozi: plachta (u modre odstin A)
    # osoby: callback 0x15 vrati kapacitu, jinak grafika (vojaci pod plachtou, modra bez plachty); u male i zvuk
    g_lide = grafika("PASS")
    Y += sw(s_lidi, f"osoby: kapacita {'auta ' if CUMAK else ''}{lidi_auto}", CALLBACK,
            [(0x15, 0x8000 | lidi_auto)] + ([] if CUMAK else zvuk), g_lide)
    popis_nakup = [(0x23, 0x8000 | TEXT[n])]
    if CUMAK:
        Y += sw(s_clanky, "clanky (callback 0x16): 1 = viditelne auto, dal nic", ["value1 = variable[0x10] & 0x000000FF;"],
                [(1, 0x8000 | auto)], 0xFFFF)
        Y += sw(s_cumak, "cumak: clanky, zvuky, jinak prazdny sprite", CALLBACK, [(0x16, s_clanky)] + zvuk, g_prazdny)
        # cumak s lidmi: kapacita 1 (hra by jeho 1 zbozi prepocetla nasobkem na 2 lidi, velka pak vezla 21 a 4)
        s_cumak_lidi = nove()
        Y += sw(s_cumak_lidi, "cumak, osoby: kapacita 1, clanky, zvuky", CALLBACK,
                [(0x15, 0x8000 | kap_cumak), (0x16, s_clanky)] + zvuk, g_prazdny)
        Y += sw(s_nakup, "nakup: clanky, popis, obrazek", CALLBACK, [(0x16, s_clanky)] + popis_nakup, g_nakup)
        Y += action3(h, s_cumak, [(INDEX[k], s_cumak_lidi) for k in LIDE] + [(0xFF, s_nakup)])
    else:
        Y += sw(s_nakup, "nakup: popis, obrazek", CALLBACK, popis_nakup, g_nakup)
    # viditelne auto: osoby pres kapacitni callback, ostatni naklady auto a vrstva; co jde na vychozi, v Action 3 neni
    mapa = {}
    for k in NAKLADY[n]:
        cil = s_lidi if k in LIDE else grafika(k)
        if cil != vychozi_g: mapa[INDEX[k]] = cil
    vychozi = vychozi_g
    if not CUMAK and id_zvuk:
        # mala: Action 3 vybira podle nakladu a callback 0x33 jde stejnou cestou, tak kazdy cil grafiky
        # dostane obal "zvuk, jinak grafika" (osoby uz zvuk maji v s_lidi)
        obal = {}
        for cil in [vychozi_g] + sorted(set(mapa.values()) - {s_lidi, vychozi_g}):
            obal[cil] = nove()
            Y += sw(obal[cil], "zvuk, jinak grafika", CALLBACK, zvuk, cil)
        mapa = {k: obal.get(v, v) for k, v in mapa.items()}
        vychozi = obal[vychozi_g]
    if not CUMAK:
        mapa[0xFF] = s_nakup
    Y += action3(auto, vychozi, sorted(mapa.items()))
    print(n, "switchu a skupin do", hex(dalsi[0] - 1))

open(os.path.join(VYSTUP, "sprites", f"{JMENO}.yagl"), "w").write("\n".join(Y) + "\n")
souhrn = {"tabulka": TABULKA, "naklady": NAKLADY, "odstin": ODSTIN, "vrstva": VRSTVA, "plachta": PLACHTA,
          "sprity": {nat: [[im.width, im.height, xo, yo] for im, xo, yo in vse[nat]] for nat in vse}}
json.dump(souhrn, open(os.path.join(VYSTUP, f"{JMENO}-souhrn.json"), "w"), indent=1, ensure_ascii=False)
print(JMENO, "spritu", sid[0] - 1, "list", list32.size, "tabulka", len(TABULKA), "nakladu",
      {n: len(v) for n, v in NAKLADY.items()}, "odstiny B/C/D", {o: sum(1 for v in ODSTIN.values() if v == o) for o in "BCD"})
