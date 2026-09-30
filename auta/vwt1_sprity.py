# Rozebere yagl VW T1: ke kazdemu vozidlu (properties 0x00XX) sady spritu, ktere tesne predchazeji (sprite_sets)
import re, sys, json
def rozeber(cesta):
    t = open(cesta, encoding="utf-8").read()
    zaznamy = re.split(r"\n(?=// Record #\d+\n)", t)
    vysl = []   # posloupnost: ("sady", [[sprite...]...]) nebo ("vlastnosti", id)
    for z in zaznamy:
        if re.search(r"^sprite_sets<RoadVehicles", z, re.M):
            sady = []
            for s in re.findall(r"sprite_set // 0x[0-9A-F]+\n\s*\{(.*?)\n    \}", z, re.S):
                sp = re.findall(r"sprite_id<(0x[0-9A-F]+)>\s*\{\s*\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\], zin4, [^,]+, \"([^\"]+)\", \[(\d+), (\d+)\];", s)
                sady.append([dict(id=a, w=int(w), h=int(h), xo=int(xo), yo=int(yo), soubor=f, x=int(x), y=int(y)) for a, w, h, xo, yo, f, x, y in sp])
            vysl.append(("sady", sady))
        m = re.search(r"^properties<RoadVehicles, (0x[0-9A-F]{4})>", z, re.M)
        if m: vysl.append(("vlastnosti", int(m.group(1), 16)))
    # sady tesne pred vlastnostmi patri tomu vozidlu (podle poradi v souboru)
    sady_vozidla = {}
    for i, (co, x) in enumerate(vysl):
        if co == "vlastnosti" and i > 0 and vysl[i - 1][0] == "sady":
            sady_vozidla[x] = vysl[i - 1][1]
    return sady_vozidla
if __name__ == "__main__":
    s = rozeber(sys.argv[1])
    for vid in sorted(s): print(f"{vid:04X}", [len(x) for x in s[vid]])
