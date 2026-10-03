# -*- coding: utf-8 -*-
# Tatry 148 a 138 ve spolecnem GRF s vejtraskou (hrac 29. 9.: "tak je dame k vejtraskam, at usetrime misto MB za zvukove
# soubory?" -> zvuky jsou v GRF jen jednou). Tenhle soubor spousti v3s/pack_v3s.py ve svem jmennem prostoru (exec),
# takze pouziva jeho pomocniky (sw, action3, sprite, sid, INDEX, NAKLADY, VRSTVA, PODTYPY, zvukovy_retez, CUMAK, ...):
#   tatra_nacti()  pred sestavenim spritesheetu: fotky Tater do vse (fotky z tatra/fotky_tatra.py, argument 4 baliče)
#   tatra_texty()  retezce Tater (popis v nakupu, jmena podtypu) za retezci vejtrasky
#   tatra_yagl()   za auty vejtrasky: vrstvy nakladu Tatry, ctyri Tatry (vlastnosti, grafika, callbacky)
#
# Hrac 29. 9. (tatra/README.md): 148 oranzova a 138 cervena, kazda se svymi obrazky ("dame zvlast obrazky pro presne
# barvy"); nastavba podle nakladu: "mineraly, uhli sklapec", "co roste, to na valnik", "valnik ocel hotovou a vyrobky
# z oceli pod plachtu", tekutiny v cisterne ("zluta chemie, modra voda, mliko, olej a bila benzin, asi na ropu musime
# udelat cernou tmavou"), pivo v sudech a prestavbou v cisterne ("Plzen bilou a Budvar modrou"). Zelena 148 a 138
# ("na ty veci, ktere vozi jenom zelena vejtraska, udelame zelenou tatru 138 a 148 valnik a valnik plachta, pro uranovy
# veci, military, explosives") ma jen valnik a vozi jako zelena vejtraska.

T_AUTA = ["T148", "T138", "T148z", "T138z"]
T_ID = {"T148": 0x0102, "T138": 0x0103, "T148z": 0x0104, "T138z": 0x0105}        # kupovane cislo (u velke cumak)
T_ID_AUTO = {k: v + 0x10 for k, v in T_ID.items()}                                  # u velke viditelne auto
T_NAZEV = {"T148": "Tatra 148", "T138": "Tatra 138", "T148z": "Tatra 148 (zelená)", "T138z": "Tatra 138 (zelená)"}
T_MODEL = {"T148": "T148", "T138": "T138", "T148z": "T148", "T138z": "T138"}
T_ZELENA = {"T148z", "T138z"}
# Uvedeni: T 138 se vyrabela od roku 1959, T 148 od roku 1969 (obe do 1982, resp. 1969)
T_UVEDENI = {"T148": "1969/1/1", "T138": "1959/1/1", "T148z": "1969/1/1", "T138z": "1959/1/1"}
T_KAPACITA = {"T148": 15, "T138": 12, "T148z": 15, "T138z": 12}                  # vejtraska 10
T_LIDI = {"T148": 3, "T138": 3, "T148z": 20, "T138z": 20}                          # jako vejtraska: v kabine / na korbe
T_VYKON = {"T148": 0x15, "T138": 0x12}             # 212 k (T2-928-1), 180 k (T 928-1), v 10 k
T_HMOTNOST = {"T148": 0x29, "T138": 0x24}          # 10,25 t a 9 t, ve ctvrttunach

# Sklapec: kupy nerostu (obrazek kupy na sklapeci); uran a uranova ruda jen zelena
T_SKLAPEC = {k: k for k in "COAL COKE IORE LIME SLAG SCMT GRVL SAND CLAY CORE SULP".split()}
T_SKLAPEC.update({"AORE": "IORE", "NKOR": "SLAG", "PORE": "GRVL", "MNO2": "COKE", "COCO": "CORE", "SCRP": "SCMT"})
# Cisterna: barva podle tekutiny
T_CISTERNA = {}
for _c, _k in (("modra", "WATR MILK EOIL MOLS"),                                   # voda, mleko, jedly olej, melasa
               ("bila", "PETR RFPR NAPH LUBR"),                                    # benzin a rafinovane produkty
               ("zluta", "ACID LYE_ CHLO NH3_ O2__ FUEL ACET HYAC PHAC SUAC MEOH C2H4 C3H6 H2__ N7__ N2__"),  # chemie, plyny
               ("cerna", "OIL_ OILD OILI CTAR")):                                  # ropa a dehet
    T_CISTERNA.update({k: _c for k in _k.split()})
# Valnik s plachtou: ocel a strojirenstvi (odstin D u vejtrasky) pod sedou, ostatni pod sedobilou
T_PLACHTA = {"oranzova": ("plachta_sedobila", "plachta_seda"), "zelena": ("plachta_vojenska", "plachta_seda")}
# Podtypy: [(telo, obrazek nakladu nebo None, jmeno)]; telo valnik, sklapec nebo cisterna_<barva>
T_PODTYPY = {k: [("valnik", obr, jm) for obr, jm in v] for k, v in PODTYPY.items()}
T_PODTYPY_ORANZ = dict(T_PODTYPY)
T_PODTYPY_ORANZ["BEER"] = [("valnik", "BEER", " (sudy)"), ("cisterna_bila", None, " (pivo Plzeň, cisterna)"),
                           ("cisterna_modra", None, " (pivo Budvar, cisterna)")]

# Od verze 11 (hrac 30. 9.): "zelenou tatru 138 148 schovame pod normalni 138 148. hrac koupi tatru na explosives
# a dostane zelenou", "hlavne zmizi z menu nakupu ta vojenska 138 148 a schova se". Zelene Tatry v nakupu nejsou
# (klima zadne), jejich cisla a grafika zustavaji kvuli rozehranym hram. Normalni 148 a 138 vozi i to, co dosud vozila
# jen zelena, a s tim jsou cele zelene (vojensky valnik te Tatry a vrstva nakladu jako u zelene).
T_SKRYTE = T_ZELENA
T_JEN_ZELENA = list(JEN_VOJENSKA)
T_NAKLADY_NORMALNI = [k for k in TABULKA if k not in NEVOZI]
# "par zelenych nechame jako prestavbu navic": zelena jako dalsi podtyp nakladu (okno prestavby) u dobytka, kup toho,
# co roste ("marihuana, seno, vlakna, marihuanove seno, ovoce, zrni, armada pomahala zemedelcum pri sklizni"), dreva,
# cihel a stavebnin ("cement, vapno, pytle") a u toho, co si vojaci uzijou ("cigara, tabak, alkohol"); "prestavby na
# pivovar Plzen Budvar ne" (cisterny zelenou variantu nemaji)
T_ZELENA_NAVIC = ("LVST "                                                           # prasatka, kravicky, ovecky
                  "MARI HOPS FICR SGCN FRUT FRVG GRAI WHEA MAIZ CERE TATO BRAM BEAN SGBT SEED OLSD NUTS "   # co roste
                  "WOOD TWOD BRCK BDMT CMNT QLME "                                  # drevo, cihly, stavebniny
                  "CIGR TBCO BEER WINE "                                            # doutniky, tabak, alkohol
                  "STUD").split()             # od verze 13 studentky (hrac 1. 10.: "stud povolime prestavbu na zelenou Tatru")

def t_normalni_obrazek(k, zelena_varianta):
    """(telo, obrazek na valniku) nakladu k bez podtypu u normalni Tatry, nebo jeho zelena varianta"""
    if k in VRSTVA and not VRSTVA[k].startswith("sudy_"):
        return ("valnik_zelena" if zelena_varianta else "valnik"), VRSTVA[k]
    pl = T_PLACHTA["zelena" if zelena_varianta else "oranzova"]
    return ("valnik_zelena" if zelena_varianta else "valnik"), pl[1] if ODSTIN.get(k) == "D" else pl[0]

def t_zeleny_podtyp(telo, obr, jm):
    """zelena varianta podtypu: vojensky valnik se stejnym nakladem, plachta vojenska misto sedobile"""
    if obr == T_PLACHTA["oranzova"][0]: obr = T_PLACHTA["zelena"][0]
    return ("valnik_zelena", obr, (jm[:-1] + ", zelená)") if jm else " (zelená)")

for _k in T_ZELENA_NAVIC:
    assert _k in INDEX and _k in T_NAKLADY_NORMALNI, _k
    _zaklad = T_PODTYPY_ORANZ.get(_k) or [t_normalni_obrazek(_k, False) + ("",)]
    T_PODTYPY_ORANZ[_k] = list(_zaklad) + [t_zeleny_podtyp(*p) for p in _zaklad if not p[0].startswith("cisterna_")]

def tatra_nacti():
    """fotky Tater do vse: auta a vrstvy nakladu (valnik Tv_, sklapec Ts_), kotvy jako u vejtrasky"""
    global T_OBR_V, T_OBR_S
    fotky = sys.argv[4]
    def sada(jm, zin8=False):
        """8 smeru (obrazek, xo, yo) z fotek 4x; se zin8 k tomu do vse8[klic] totez z fotek 8x (jako nacti_sadu vejtrasky)"""
        adr = os.path.join(fotky, f"{VEL}_{jm}")
        if os.environ.get("TATRA_NANECISTO") and not os.path.exists(os.path.join(adr, "kotvy.json")):
            return [(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0, 0)] * 8     # zkouska baliče, fotka jeste neni
        info = json.load(open(os.path.join(adr, "kotvy.json")))
        out, out8 = [], []
        for d in range(8):
            gx, gy = info["smery"][str(d)]["zem_stred"]
            du, dv = kotva_konvence(d)
            foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA")
            bb = foto.getbbox()
            if bb is None:
                out.append((Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0, 0)); out8.append((Image.new("RGBA", (2, 2), (0, 0, 0, 0)), 0, 0)); continue
            xo, yo = int(math.floor(bb[0] - (gx + du) + 0.5)), int(math.floor(bb[1] - (gy + dv) + 0.5))
            out.append((foto.crop(bb), xo, yo))
            if zin8:
                foto8 = Image.open(os.path.join(adr + "_zin8", f"d{d}.png")).convert("RGBA")
                assert foto8.size == (2 * foto.width, 2 * foto.height), (jm, d, foto.size, foto8.size)
                out8.append((foto8.crop((2 * bb[0], 2 * bb[1], 2 * bb[2], 2 * bb[3])), 2 * xo, 2 * yo))
        if zin8: sada.out8 = out8
        return out
    for m in ("T148", "T138"):
        for t in ["sklapec", "valnik"] + [f"cisterna_{c}" for c in ("modra", "bila", "zluta", "cerna")] + ["valnik_zelena"]:
            vse[f"{m}_{t}"] = sada(f"{m}_{t}")
    T_OBR_V = sorted({v for v in VRSTVA.values()} | {obr for p in T_PODTYPY.values() for _, obr, _ in p if obr}
                     | set(T_PLACHTA["oranzova"]) | set(T_PLACHTA["zelena"]) | {"BEER", "studentky_sedi"})   # od v14 sedici
    T_OBR_V = [o for o in T_OBR_V if not o.startswith("plachta_") or o in ("plachta_vojenska", "plachta_seda", "plachta_sedobila")]
    T_OBR_S = sorted(set(T_SKLAPEC.values()))
    for k in T_OBR_V:
        vse[f"Tv_{k}"] = sada(f"T_valnik_naklad_{k}", zin8=k in ZIN8)
        if k in ZIN8: vse8[f"Tv_{k}"] = sada.out8          # od verze 16: studentky i v 8x
    for k in T_OBR_S: vse[f"Ts_{k}"] = sada(f"T_sklapec_naklad_{k}")

def tatra_texty():
    """popisy v nakupu a jmena podtypu Tater, cisla za retezci vejtrasky (Y je jeste v bloku strings)"""
    global T_TEXT, T_TEXT_PODTYP
    t = max(max(v) for v in TEXT_PODTYP.values()) + 1
    # Action 4 unese nejvys 255 retezcu, dal novy blok. Jmena podtypu smi az do 0xD3FF (callback 0x19 vraci 0x000-0x3FF).
    zacatek = [min(TEXT.values())]                      # blok strings vejtrasky zacina 0xD001
    def text(s):
        nonlocal t
        if t - zacatek[0] == 255:
            zacatek[0] = t
            Y.extend(["}", f"strings<RoadVehicles, default, 0x{0xD000 + t:04X}*> // Action04, dalsi retezce Tater", "{"])
        Y.append(f'    /* 0x{0xD000 + t:04X} */ "{s}";'); t += 1
        return t - 1
    T_TEXT = {}
    for n in T_AUTA:
        T_TEXT[n] = text(f"{{green}}for {DECOUPLE}{{black}}{{new-line}}Model: {{gold}}hans1240 (Sketchfab), CC BY 4.0")
    T_TEXT_PODTYP = {}
    for k, p in T_PODTYPY_ORANZ.items():
        if k in PODTYPY and (p is T_PODTYPY[k] or [jm for _, _, jm in p] == [jm for _, jm in PODTYPY[k]]):
            T_TEXT_PODTYP[k] = TEXT_PODTYP[k]; continue                  # stejna jmena jako u vejtrasky
        T_TEXT_PODTYP[k] = [text(jm) for _, _, jm in p]
    assert t <= 0x400

def tatra_yagl():
    global Y
    # vrstvy nakladu Tatry: sady a skupiny 0xC0 a dal (skupiny vejtrasky tam uz nikdo neodkazuje)
    obr = [("v", k) for k in T_OBR_V] + [("s", k) for k in T_OBR_S]
    Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, vrstvy nakladu Tatry (valnik Tv_, sklapec Ts_)", "{"]
    for si, (kde, k) in enumerate(obr):
        Y += [f"    sprite_set // 0x{si:04X} {'valnik' if kde == 'v' else 'sklapec'} {k}", "    {"]
        for i in range(8): Y += sprite(f"T{kde}_{k}", i)
        Y += ["    }"]
    i_nic = len(obr)
    Y += [f"    sprite_set // 0x{i_nic:04X} bez nakladu", "    {"]
    for i in range(8): Y += sprite()
    Y += ["    }", "}"]
    G_T = {}
    for si, (kde, k) in enumerate(obr):
        G_T[kde, k] = 0xC0 + si
        assert G_T[kde, k] <= 0xFF
        # primarni sady za jizdy, sekundarni pri nakladani: od verze 14 studentky za jizdy sedi, na zastavce stoji
        sj = obr.index(("v", "studentky_sedi")) if (kde, k) == ("v", "studentky") and ("v", "studentky_sedi") in obr else si
        Y += [f"sprite_groups<RoadVehicles, 0x{G_T[kde, k]:02X}> // Action02 basic, Tatra {kde} {k}: prazdno, naklad"
              + (", za jizdy sedi" if sj != si else ""), "{",
              f"    primary_spritesets: [ 0x{i_nic:04X} 0x{sj:04X} ];", f"    secondary_spritesets: {sady_na_zastavce(i_nic, si)};", "}"]   # od verze 17 na zastavce od 1. jednotky

    for n in T_AUTA:
        h = T_ID[n]; auto = T_ID_AUTO[n] if CUMAK else h
        m = T_MODEL[n]; zelena = n in T_ZELENA
        dalsi = [0x10]
        def nove():
            # od verze 11 dvoubajtova cisla bloku (dotaz decouple_more_action2_ids): switche preskoci vrstvy 0xC0-0xFF
            if dalsi[0] == 0xC0: dalsi[0] = 0x100
            i = dalsi[0]; dalsi[0] += 1
            assert i <= 0x7FFD, "hra unese cisla bloku jen do 0x7FFD"
            return i
        naklady = NAKLADY["vojenska"] if zelena else T_NAKLADY_NORMALNI
        kap_cumak = 1 if CUMAK else 0
        kap_auto = T_KAPACITA[n] - kap_cumak
        lidi_auto = T_LIDI[n] - kap_cumak
        Y += [f"// ---------------- {T_NAZEV[n]}"]
        dily = [(h, "cumak"), (auto, "auto")] if CUMAK else [(h, "auto")]
        for eid, co in dily:
            p = [f"properties<RoadVehicles, 0x{eid:04X}> // Action00 ({co})", "{", "    {",
                 f"        long_introduction_date: date({T_UVEDENI[n]});", "        model_life_years: 255;",
                 "        vehicle_life_years: 15;", "        reliability_decay_speed: 20;",
                 # od verze 14 u zlata i trida cennosti (0x0008) kvuli druhemu zlatu hry (kod GOLD dvakrat, tabulka
                 # najde jen prvni); co Tatra nevozi, je v never_refittable_cargos, at to trida neprida
                 f"        refittable_cargo_classes: 0x{0x0008 if 'GOLD' in naklady else 0:04X};",
                 "        non_refittable_cargo_classes: 0x0000;",
                 "        refit_cargo_types: 0x00000000;",
                 f"        // vozí všechno z tabulky kromě: "
                 f"{nevozi('vojenska') if zelena else ', '.join(f'{k} {v}' for k, v in NEVOZI.items())}",
                 f"        always_refittable_cargos: [ {' '.join(f'0x{INDEX[k]:02X}' for k in naklady)} ];",
                 f"        never_refittable_cargos: [ {' '.join(f'0x{INDEX[k]:02X}' for k in TABULKA if k not in naklady and k in INDEX)} ];",
                 f"        cargo_type: 0x{INDEX['GOOD']:02X};", "        loading_speed: 0x05;", "        refit_cost: 0x00;",
                 "        sprite_id: 0xFF;",
                 f"        miscellaneous_flags: 0x{0x80 if co == 'auto' else 0:02X};",
                 f"        cargo_capacity: 0x{(kap_cumak if co == 'cumak' else kap_auto):02X};",
                 f"        shorten_vehicle: 0x{(8 - CUMAK) if co == 'cumak' else 0:02X};"]
            if eid == h:
                p += ["        climate_availability: " +                              # zelena od verze 11 schovana
                      ("null;" if n in T_SKRYTE else "Temperate | Arctic | Tropical | Toyland;"),
                      "        speed_2_kmh: 0x8E;",                                   # 71 km/h
                      f"        power_10_hp: 0x{T_VYKON[m]:02X};",
                      f"        weight_quarter_tons: 0x{T_HMOTNOST[m]:02X};",
                      "        cost_factor: 0x60;", "        running_cost_factor: 0x3C;",
                      "        running_cost_base: 0x00004C48;",
                      "        sound_effect_type: 0x17;"]
            maska = 0x18 if co == "cumak" else 0x08
            maska |= 0x20
            if eid == h and ZV: maska |= 0x80
            p += [f"        callback_flags_mask: 0x{maska:02X};"]
            Y += p + ["    }", "}", f"strings<RoadVehicles, default, 0x{eid:04X}> // Action04", "{",
                      f'    /* 0x{eid:04X} */ "{T_NAZEV[n] if eid == h else T_NAZEV[n] + " (auto)"}";', "}"]
        # Action01: nastavby auta a prazdna sada pro cumak
        tela = ["valnik_zelena"] if zelena else (["valnik", "sklapec"] + [f"cisterna_{c}" for c in ("modra", "bila", "zluta", "cerna")]
                                                 + ["valnik_zelena"])        # od verze 11 i zelena (vojenske naklady)
        i_prazdny = len(tela)
        Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01", "{"]
        for si, t in enumerate(tela):
            Y += [f"    sprite_set // 0x{si:04X} {m}_{t}", "    {"]
            for i in range(8): Y += sprite(f"{m}_{t}", i)
            Y += ["    }"]
        Y += [f"    sprite_set // 0x{i_prazdny:04X} prazdny cumak", "    {"]
        for i in range(8): Y += sprite()
        Y += ["    }", "}"]
        g = {t: nove() for t in tela}
        g_prazdny = nove()
        for si, t in enumerate(tela):
            Y += [f"sprite_groups<RoadVehicles, 0x{g[t]:02X}> // Action02 basic, {m}_{t}", "{",
                  f"    primary_spritesets: [ 0x{si:04X} ];", f"    secondary_spritesets: [ 0x{si:04X} ];", "}"]
        Y += [f"sprite_groups<RoadVehicles, 0x{g_prazdny:02X}> // Action02 basic, prazdny cumak", "{",
              f"    primary_spritesets: [ 0x{i_prazdny:04X} ];", f"    secondary_spritesets: [ 0x{i_prazdny:04X} ];", "}"]
        g_nakup = nove()
        Y += ["sprite_sets<RoadVehicles, 0x0000> // Action01, obrazek do nakupu", "{", "    sprite_set // 0x0000 nakup", "    {"]
        Y += sprite(f"{m}_{tela[0]}", 6)
        Y += ["    }", "}", f"sprite_groups<RoadVehicles, 0x{g_nakup:02X}> // Action02 basic, nakup", "{",
              "    primary_spritesets: [ 0x0000 ];", "    secondary_spritesets: [ 0x0000 ];", "}"]
        s_clanky, s_lidi, s_nakup, s_cumak = nove(), nove(), nove(), nove()
        zvuk_radky, id_zvuk, dalsi[0] = zvukovy_retez(dalsi[0])
        assert dalsi[0] < 0xC0
        Y += zvuk_radky
        zvuk = [(0x33, id_zvuk)] if id_zvuk else []
        plachta = T_PLACHTA["zelena" if zelena else "oranzova"]

        def urci(k):
            """(telo, obrazek na valniku 'v' / sklapeci 's' nebo None) pro naklad k"""
            if zelena or k in T_JEN_ZELENA:           # od verze 11 veze normalni Tatra vojenske naklady zelena
                if k in VRSTVA: return "valnik_zelena", ("v", VRSTVA[k])
                zp = T_PLACHTA["zelena"]
                return "valnik_zelena", ("v", zp[1] if ODSTIN.get(k) == "D" else zp[0])
            if k in T_CISTERNA: return f"cisterna_{T_CISTERNA[k]}", None
            if k in T_SKLAPEC: return "sklapec", ("s", T_SKLAPEC[k])
            if k in VRSTVA and not VRSTVA[k].startswith("sudy_"): return "valnik", ("v", VRSTVA[k])
            if k in LIDE: return "valnik", None
            return "valnik", ("v", plachta[1] if ODSTIN.get(k) == "D" else plachta[0])
        vrstvy_sw = {}
        def cil(telo, ob):
            """graficky cil: nastavba telo a pres ni vrstva ob (nebo nic)"""
            if ob is None: return g[telo]
            if (telo, ob) not in vrstvy_sw:
                sv = nove(); vrstvy_sw[telo, ob] = sv
                Y.extend(sw(sv, f"vrstvy: {m}_{telo} a pres ni {ob[1]} ({'valnik' if ob[0] == 'v' else 'sklapec'})",
                            VRSTVY_VYRAZ, [(1, G_T[ob])], g[telo]))
            return vrstvy_sw[telo, ob]
        vychozi_g = cil(*urci("GOOD"))
        podtypy = T_PODTYPY if zelena else T_PODTYPY_ORANZ
        texty_podtypu = {k: TEXT_PODTYP[k] for k in PODTYPY} if zelena else T_TEXT_PODTYP
        s_podtyp_text, s_podtyp, s_obr_k = {}, {}, {}
        for k, pt in podtypy.items():
            if k not in naklady: continue
            s_podtyp_text[k] = nove()
            Y += sw(s_podtyp_text[k], f"{k} (callback 0x19): jmena podtypu, dal konec seznamu",
                    ["value1 = variable[0xF2] & 0x000000FF;"], [(i, 0x8000 | t) for i, t in enumerate(texty_podtypu[k])], 0x8400)
            s_obr = nove()
            def cil_podtypu(telo, o):
                if zelena: telo = "valnik_zelena"
                return cil(telo, ("v", o) if o else None)
            Y += sw(s_obr, f"{k}: obrazek podle podtypu (promenna 0xF2)", ["value1 = variable[0xF2] & 0x000000FF;"],
                    [(i, cil_podtypu(telo, o)) for i, (telo, o, jm) in enumerate(pt) if i > 0], cil_podtypu(pt[0][0], pt[0][1]))
            s_obr_k[k] = s_obr
            s_podtyp[k] = nove()
            Y += sw(s_podtyp[k], f"{k}: jmena podtypu (callback 0x19), jinak obrazek", CALLBACK, [(0x19, s_podtyp_text[k])], s_obr)
        g_lide = cil(*urci("PASS"))
        Y += sw(s_lidi, f"osoby: kapacita {'auta ' if CUMAK else ''}{lidi_auto}", CALLBACK,
                [(0x15, 0x8000 | lidi_auto)] + ([] if CUMAK else zvuk), g_lide)
        # od verze 13 studentky: kapacita jako osoby, holky na korbe misto prazdneho valniku, u normalni Tatry i zelena
        # prestavba (podtypy)
        s_stud = None
        if "STUD" in naklady:
            s_stud = nove()
            Y += sw(s_stud, f"studentky: kapacita {'auta ' if CUMAK else ''}{lidi_auto}, jmena podtypu, jinak holky na korbe",
                    CALLBACK, [(0x15, 0x8000 | lidi_auto)] + ([(0x19, s_podtyp_text["STUD"])] if "STUD" in s_podtyp_text else [])
                    + ([] if CUMAK else zvuk), s_obr_k.get("STUD") or cil(*urci("STUD")))
        popis_nakup = [(0x23, 0x8000 | T_TEXT[n])]
        if CUMAK:
            Y += sw(s_clanky, "clanky (callback 0x16): 1 = viditelne auto, dal nic", ["value1 = variable[0x10] & 0x000000FF;"],
                    [(1, 0x8000 | auto)], 0xFFFF)
            Y += sw(s_cumak, "cumak: clanky, zvuky, jinak prazdny sprite", CALLBACK, [(0x16, s_clanky)] + zvuk, g_prazdny)
            s_cumak_lidi = nove()
            Y += sw(s_cumak_lidi, "cumak, osoby: kapacita 1, clanky, zvuky", CALLBACK,
                    [(0x15, 0x8000 | kap_cumak), (0x16, s_clanky)] + zvuk, g_prazdny)
            Y += sw(s_nakup, "nakup: clanky, popis, obrazek", CALLBACK, [(0x16, s_clanky)] + popis_nakup, g_nakup)
            s_cumak_podtyp = {}
            for k in s_podtyp_text:
                s_cumak_podtyp[k] = nove()
                Y += sw(s_cumak_podtyp[k], f"cumak, {k}: clanky, jmena podtypu, zvuky", CALLBACK,
                        [(0x16, s_clanky), (0x19, s_podtyp_text[k])] + zvuk, g_prazdny)
            cumak_mapa = {INDEX[k]: s_cumak_lidi for k in LIDE if k in naklady}
            cumak_mapa.update({INDEX[k]: s_cumak_podtyp[k] for k in s_cumak_podtyp})
            if "STUD" in s_cumak_podtyp:              # studentky: kapacita cumaku 1 a jmena podtypu dohromady
                s_cumak_stud = nove()
                Y += sw(s_cumak_stud, "cumak, studentky: kapacita 1, clanky, jmena podtypu, zvuky", CALLBACK,
                        [(0x15, 0x8000 | kap_cumak), (0x16, s_clanky), (0x19, s_podtyp_text["STUD"])] + zvuk, g_prazdny)
                cumak_mapa[INDEX["STUD"]] = s_cumak_stud
            Y += action3(h, s_cumak, list(cumak_mapa.items()) + [(0xFF, s_nakup)])   # poradi jako drive
        else:
            Y += sw(s_nakup, "nakup: popis, obrazek", CALLBACK, popis_nakup, g_nakup)
        mapa = {}
        for k in naklady:
            c = (s_stud if k == "STUD" and s_stud else s_lidi) if k in LIDE else (s_podtyp[k] if k in s_podtyp else cil(*urci(k)))
            if c != vychozi_g: mapa[INDEX[k]] = c
        # od verze 14: druhe zlato hry (stejny kod GOLD jako zlato ECS, Action 3 ho tabulkou nenajde) jde na vychozi,
        # u Tatry bedny; proto vychozi nejdriv podle nakladu (promenna 0x47, spodni bajt je misto nakladu v nasi tabulce,
        # hra ho hleda podle kodu, takze plati i pro druhe zlato) na zlato: zelena Tatra s plachtou
        vychozi_cil = vychozi_g
        if "GOLD" in naklady:
            vychozi_cil = nove()
            Y += sw(vychozi_cil, "vychozi: i druhe zlato hry jako zlato (zelena s plachtou), jinak vychozi",
                    ["value1 = variable[0x47] & 0x000000FF;"], [(INDEX["GOLD"], cil(*urci("GOLD")))], vychozi_g)
        vychozi = vychozi_cil
        if not CUMAK and id_zvuk:
            obal = {}
            for c in [vychozi_cil] + sorted(set(mapa.values()) - {s_lidi, s_stud, vychozi_cil}):
                obal[c] = nove()
                Y += sw(obal[c], "zvuk, jinak grafika", CALLBACK, zvuk, c)
            mapa = {k: obal.get(v, v) for k, v in mapa.items()}
            vychozi = obal[vychozi_cil]
        s_davka = davka_switche(nove, g_prazdny)
        mapa, vychozi = obal_nakladani(nove, mapa, vychozi, s_davka)    # od verze 17 davka nakladani (callback 0x36)
        if not CUMAK:
            mapa[0xFF] = s_nakup
        Y += action3(auto, vychozi, sorted(mapa.items()))
        print(n, "switchu a skupin do", hex(dalsi[0] - 1))
