#!/usr/bin/env python3
# Vypis vozu z rozbaleneho yaglu (staci yagl -d -n): id, jmeno, tridy nakladu a seznamy kodu
# (always_refittable_cargos a never_refittable_cargos prelozene pres cargo_translation_table).
#   python3 tools/naklady.py <soubor.yagl>                  vsechny vozy
#   python3 tools/naklady.py <soubor.yagl> FICR Uacs ...    jen vozy s kodem v seznamu nebo s kusem jmena
# Seznamy jsou tak, jak je GRF zapsal. Co vuz opravdu vezme (zakaz vyhrava), rika tools/kdo_veze.py.
import re, sys

TRIDY = {0: "cestujici", 1: "posta", 2: "expres", 3: "obrnene", 4: "sypke", 5: "kusove", 6: "kapaliny",
         7: "chlazene", 8: "nebezpecne", 9: "kryte", 10: "nadrozmerne", 11: "praskove", 12: "nesypatelne",
         13: "pitne", 14: "nepitne", 15: "specialni"}


def tridy(x):
    return "+".join(TRIDY[b] for b in range(16) if x >> b & 1) or "-"


def nacti(cesta):
    """vrati (tabulka index->kod, jmena id->text, vozy id->vlastnosti)"""
    t = open(cesta, encoding="utf-8", errors="replace").read()
    tab = {int(m.group(1), 16): m.group(2) for m in
           re.finditer(r"// instance_id: 0x([0-9A-F]+)\s*\{\s*cargo_translation_table: \"([^\"]*)\"", t)}
    jmena = {}
    for m in re.finditer(r"strings<Trains, default, 0x([0-9A-F]{4})>[^\n]*\n\{\s*/\* 0x[0-9A-F]{4} \*/ \"([^\"]*)\"", t):
        jmena.setdefault(int(m.group(1), 16), m.group(2).replace("{dq}", '"').strip())
    vozy = {}
    for m in re.finditer(r"properties<Trains, 0x([0-9A-F]{4})>.*?\n\}", t, re.S):
        blok = m.group(0); v = vozy.setdefault(int(m.group(1), 16), {})
        for k in ("always_refittable_cargos", "never_refittable_cargos"):
            a = re.search(k + r": \[([^\]]*)\]", blok)
            if a: v[k] = [tab.get(int(x, 16), f"#{x}") for x in a.group(1).split()]
        for k in ("refittable_cargo_classes", "non_refittable_cargo_classes"):
            a = re.search(k + r": (0x[0-9A-F]+);", blok)
            if a: v[k] = int(a.group(1), 16)
    return tab, jmena, vozy


if __name__ == "__main__":
    tab, jmena, vozy = nacti(sys.argv[1])
    hled = sys.argv[2:]
    n = 0
    for vid, v in vozy.items():
        if "always_refittable_cargos" not in v and "refittable_cargo_classes" not in v: continue
        jm = jmena.get(vid, "?")
        seznam = v.get("always_refittable_cargos", [])
        if hled and not (any(h in seznam for h in hled) or any(h.lower() in jm.lower() for h in hled)): continue
        n += 1
        krome = v.get("non_refittable_cargo_classes")
        nikdy = v.get("never_refittable_cargos")
        print(f"0x{vid:04X} {jm[:44]:44s} tridy {tridy(v.get('refittable_cargo_classes', 0))}"
              + (f" krome {tridy(krome)}" if krome else "") + f" | {' '.join(seznam)}"
              + (f" | nikdy {' '.join(nikdy)}" if nikdy else ""))
    print(f"-- {n} vozu, tabulka {len(tab)} kodu", file=sys.stderr)
