#!/usr/bin/env python3
# Kdo by vezl naklad s danym kodem a tridami, podle pravidla hry (CalculateRefitMasks v newgrf.cpp):
#   1. tridy: naklad ma aspon jednu povolenou tridu vozu a zadnou zakazanou,
#   2. pak se pridaji kody ze seznamu "vzdy" (always_refittable_cargos),
#   3. nakonec se uberou kody ze seznamu "nikdy" (never_refittable_cargos), zakaz vyhrava.
#   python3 tools/kdo_veze.py <soubor.yagl> <KOD> [tridy]
# Tridy jako cislo (0x0210 = sypke + kryte) nebo slovy: sypke+kryte. Bez trid se hleda jen podle seznamu.
# Stara 32bitova maska (refit_cargo_types) se nepocita; skript varuje, kdyz ji nektery vuz ma nenulovou.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from naklady import nacti, TRIDY

cesta, kod = sys.argv[1], sys.argv[2]
arg = sys.argv[3] if len(sys.argv) > 3 else "0"
if re.fullmatch(r"(0x)?[0-9A-Fa-f]+", arg):
    CL = int(arg, 16)
else:
    podle_jmena = {v: b for b, v in TRIDY.items()}
    CL = sum(1 << podle_jmena[s] for s in arg.split("+"))

tab, jmena, vozy = nacti(cesta)
if kod not in tab.values():
    print(f"pozor: {kod} neni v prekladove tabulce, podle seznamu ho nevezme zadny vuz", file=sys.stderr)
ano = []
for vid, v in vozy.items():
    if "refittable_cargo_classes" not in v and "always_refittable_cargos" not in v: continue
    tridou = bool(CL & v.get("refittable_cargo_classes", 0)) and not CL & v.get("non_refittable_cargo_classes", 0)
    vezme = (tridou or kod in v.get("always_refittable_cargos", [])) and kod not in v.get("never_refittable_cargos", [])
    if vezme: ano.append(jmena.get(vid, f"0x{vid:04X}"))
ruzna = sorted({j for j in ano if j != "Invisible"})
print(f"{len(ano)} vozu, {len(ruzna)} ruznych jmen:")
print("; ".join(ruzna))
if re.search(r"refit_cargo_types: 0x0*[1-9A-F]", open(cesta, encoding="utf-8", errors="replace").read()):
    print("pozor: nektery vuz ma nenulovy refit_cargo_types, ten skript nepocita", file=sys.stderr)
