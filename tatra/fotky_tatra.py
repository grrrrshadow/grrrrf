# -*- coding: utf-8 -*-
# Davka fotek Tatry pro GRF (render_sklapec.py), obe velikosti jako vejtraska: mala 12,2 px/m, velka 14,64 px/m.
#   python3 fotky_tatra.py <adresar fotek> [skupina ...]      skupiny: auta, valnik, sklapec (bez = vse)
# Kazda fotka je <adresar>/<mala|velka>_<jmeno>/d0-d7.png a kotvy.json. Hotove (s kotvy.json) se preskoci, takze
# davka jde pustit znova a dodela, co chybi. Bezi dva rendery naraz (4 jadra).
import os, sys, subprocess, concurrent.futures as cf

TU = os.path.dirname(os.path.abspath(__file__))
FOTKY = sys.argv[1]
SKUPINY = sys.argv[2:] or ["auta", "valnik", "sklapec"]
VELIKOSTI = {"mala": 12.2, "velka": 14.64}
SAMPLES = os.environ.get("SAMPLES", "128")

# Auta (hrac 29. 9.): 148 oranzova a 138 cervena se sklapecem, valnikem a cisternou ve ctyrech barvach (modra voda,
# mleko, olej; bila benzin; zluta chemie; cerna ropa), zelena 148 a 138 jen s valnikem (plachta je vrstva).
AUTA = {}
for nater, mrizka in (("oranzova", "148"), ("cervena", "138")):
    AUTA[f"T{mrizka}_sklapec"] = (nater, {"KORBA": "sklapec", "MRIZKA": mrizka})
    AUTA[f"T{mrizka}_valnik"] = (nater, {"KORBA": "valnik", "MRIZKA": mrizka})
    for c in ("modra", "bila", "zluta", "cerna"):
        AUTA[f"T{mrizka}_cisterna_{c}"] = (nater, {"KORBA": "cisterna", "CISTERNA": c, "MRIZKA": mrizka})
for mrizka in ("148", "138"):
    AUTA[f"T{mrizka}_valnik_zelena"] = ("vojenska", {"KORBA": "valnik", "MRIZKA": mrizka})

# Naklady na valniku: vsechny obrazky nakladu vejtrasky (kupy rozsypane po korbe, kusovy naklad, drevo) a plachty.
VALNIK = ["COAL", "COKE", "IORE", "LIME", "SLAG", "SCMT", "GRVL", "SAND", "SGBT", "SEED", "OLSD", "NUTS", "MARI", "SULP",
          "CORE", "CLAY", "WOOD", "WDPR", "CMNT", "pytle_hnede", "GOOD", "BEER", "LVST", "kravy", "ovce", "FICR",
          "seno_mari", "seno_zlute", "sudy_cerne", "sudy_bile", "sudy_cervene", "cihly_cervene", "cihly_sede",
          "brambory", "ovoce", "plachta_vojenska", "plachta_seda", "plachta_sedobila"]
# Kupy nerostu na sklapeci (hrac: "mineraly, uhli sklapec")
SKLAPEC = ["COAL", "COKE", "IORE", "LIME", "SLAG", "SCMT", "GRVL", "SAND", "CLAY", "CORE", "SULP"]

ULOHY = []
for vel, px in VELIKOSTI.items():
    if "auta" in SKUPINY:
        for jm, (nater, env) in AUTA.items():
            ULOHY.append((f"{vel}_{jm}", nater, px, env))
    if "valnik" in SKUPINY:
        for k in VALNIK:
            ULOHY.append((f"{vel}_T_valnik_naklad_{k}", "oranzova", px, {"KORBA": "valnik", "NAKLAD": k}))
    if "sklapec" in SKUPINY:
        for k in SKLAPEC:
            ULOHY.append((f"{vel}_T_sklapec_naklad_{k}", "oranzova", px, {"KORBA": "sklapec", "NAKLAD": k}))

# OBRACENE=1 bere ulohy od konce: druha davka vedle prvni doceli od druheho konce (hotove obe preskoci)
if os.environ.get("OBRACENE"): ULOHY.reverse()

def udelej(uloha):
    jm, nater, px, env = uloha
    out = os.path.join(FOTKY, jm)
    if os.path.exists(os.path.join(out, "kotvy.json")): return jm, "uz je"
    e = dict(os.environ, SAMPLES=SAMPLES, **env)
    with open(os.path.join(FOTKY, jm + ".log"), "w") as log:
        r = subprocess.run([sys.executable, os.path.join(TU, "render_sklapec.py"), nater, str(px), "256", out],
                           env=e, stdout=log, stderr=subprocess.STDOUT, cwd=TU)
    return jm, "OK" if r.returncode == 0 and os.path.exists(os.path.join(out, "kotvy.json")) else f"CHYBA {r.returncode}"

os.makedirs(FOTKY, exist_ok=True)
print("uloh", len(ULOHY), flush=True)
with cf.ThreadPoolExecutor(2) as ex:
    for i, (jm, stav) in enumerate(ex.map(udelej, ULOHY), 1):
        print(f"{i}/{len(ULOHY)} {jm}: {stav}", flush=True)
