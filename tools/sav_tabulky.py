#!/usr/bin/env python3
# Cteni tabulkovych chunku ulozene hry OpenTTD (CH_TABLE / CH_SPARSE_TABLE) bez hry, i kdyz je
# ulozena novejsi verzi, nez umi moje zkusebni hra. Hlavicka tabulky rika jmena a typy poli.
#   sav_tabulky.py <hra.sav> <CHUNK> [pole,pole...]     vypise prvky chunku (napr. VEHS, ROTT, NGRF)
import lzma, sys, zlib, struct

def rozbal(cesta):
    d = open(cesta, "rb").read()
    fmt, telo = d[:4], d[8:]
    if fmt == b"OTTX": return lzma.decompress(telo)
    if fmt == b"OTTZ": return zlib.decompress(telo)
    if fmt == b"OTTN": return telo
    raise SystemExit(f"neznamy format {fmt}")

class Cteni:
    def __init__(s, d, i=0): s.d, s.i = d, i
    def b(s): v = s.d[s.i]; s.i += 1; return v
    def n(s, k): v = s.d[s.i:s.i + k]; s.i += k; return v
    def gamma(s):
        i = s.b()
        if i & 0x80 == 0: return i
        if i & 0x40 == 0: return ((i & 0x3F) << 8) | s.b()
        if i & 0x20 == 0: return ((i & 0x1F) << 16) | (s.b() << 8) | s.b()
        if i & 0x10 == 0: return ((i & 0x0F) << 24) | (s.b() << 16) | (s.b() << 8) | s.b()
        return (s.b() << 24) | (s.b() << 16) | (s.b() << 8) | s.b()

VELIKOST = {1: 1, 2: 1, 3: 2, 4: 2, 5: 4, 6: 4, 7: 8, 8: 8, 9: 2}
ZNAK = {1: ">b", 2: ">B", 3: ">h", 4: ">H", 5: ">i", 6: ">I", 7: ">q", 8: ">Q", 9: ">H"}

def hlavicka(c):
    pole = []
    while True:
        t = c.b()
        if t == 0: break
        jm = c.n(c.gamma()).decode("latin1")
        pole.append([t, jm, None])
    for p in pole:                                # podhlavicky struktur jdou za hlavickou, v poradi
        if p[0] & 0x0F == 11: p[2] = hlavicka(c)
    return pole

def hodnota(c, t, sub):
    zaklad = t & 0x0F
    if zaklad == 10: return c.n(c.gamma()).decode("latin1", "replace")
    if zaklad == 11: return prvek(c, sub)
    v = struct.unpack(ZNAK[zaklad], c.n(VELIKOST[zaklad]))[0]
    return v

def prvek(c, pole):
    out = {}
    for t, jm, sub in pole:
        if t & 0x10:
            k = c.gamma(); out[jm] = [hodnota(c, t, sub) for _ in range(k)]
        else:
            out[jm] = hodnota(c, t, sub)
    return out

def chunk(raw, jmeno):
    c = Cteni(raw)
    while c.i < len(raw):
        tag = c.n(4)
        if tag == b"\0\0\0\0": break
        m = c.b(); typ = m & 0x0F
        if typ in (3, 4):
            delka = c.gamma() - 1; zac = c.i
            pole = hlavicka(c); c.i = zac + delka
            prvky = []; index = 0
            while True:
                dl = c.gamma()
                if dl == 0: break
                konec = c.i + dl - 1
                if typ == 4: index = c.gamma()
                if tag.decode("latin1") == jmeno:
                    prvky.append((index, prvek(c, pole)))
                c.i = konec; index += 1
            if tag.decode("latin1") == jmeno: return pole, prvky
        elif typ == 0:                               # CH_RIFF
            dl = (c.b() << 16) | (c.b() << 8) | c.b()
            dl += (m >> 4) << 24
            c.i += dl
        else:                                        # stare CH_ARRAY / CH_SPARSE_ARRAY
            while True:
                dl = c.gamma()
                if dl == 0: break
                if typ == 2: c.gamma()
                c.i += dl - 1
    raise SystemExit(f"chunk {jmeno} neni")

if __name__ == "__main__":
    raw = rozbal(sys.argv[1])
    pole, prvky = chunk(raw, sys.argv[2])
    chci = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    print("pole:", [p[1] for p in pole])
    for i, p in prvky:
        print(i, {k: v for k, v in p.items() if chci is None or k in chci})
