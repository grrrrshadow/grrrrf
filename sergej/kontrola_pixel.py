# Pixelova kontrola fotky ze zkusebni hry (hra/README.md, prikaz testvlakfoto): ke kazdemu dilu lokomotivy z logu (V3SDIL, grf MAXb) vezme
# sprite z rozbaleneho GRF (4x nebo 8x podle fotky), polozi ho tam, kam ho kresli hra, a spocita presne shodne pixely;
# hleda i nejlepsi posun v okoli.
#   python3 kontrola_pixel.py <zin> <log> <fotka.png> <cislo fotky> <rozbaleny sprites> <jmeno.yagl> <vystup_nahled.png> [vysledky.json]
import json, math, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/user/grrrrf/sergej")
from hra import nacti_sady, obrazek
zin, log, fotka, cislo, SD, YG, vystup = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
m = zin // 4
t = open(log, encoding="utf-8", errors="replace").read()
vl, na = map(int, re.search(rf"V3SPOHLED: fotka {cislo} vlevo (-?\d+) nahore (-?\d+)", t).groups())
dily = []
for mm in re.finditer(rf"V3SDIL: fotka {cislo} vuz (\d+) grf (\S+) dil 0x([0-9A-F]+) x (\d+) y (\d+) z (\d+) smer (\d+) stav (\w+) delka (\d+) kresli (-?\d+) (-?\d+)", t):
    v, grf, dil, x, y, z, smer, stav, delka, kx, ky = mm.groups()
    if grf != "MAXb": continue
    dily.append((int(v), int(dil, 16), int(x), int(y), int(z), int(smer), stav, int(delka), int(kx), int(ky)))
print("dilu v logu:", len(dily), "vlevo", vl, "nahore", na)
sady = nacti_sady(SD, YG, zin)                   # nater*4 + (0 hlava, 1 stred, 2 zad, 3 nakup)
NATERY = {0x010: "zeleny", 0x011: "cerveny", 0x012: "rzd"}
foto = np.asarray(Image.open(fotka).convert("RGB")).astype(int); H, W = foto.shape[:2]
r = 6 * m
vysl = []
for v, dil, x, y, z, smer, stav, delka, kx, ky in dily:
    nat = NATERY[dil >> 4]; kus = dil & 0xF
    sp = sady[list(NATERY.values()).index(nat) * 4 + kus][smer]
    if sp is None:
        print(f"vuz {v} {nat} dil {kus} smer {smer}: prazdny sprite (ok)"); continue
    im, xo, yo = obrazek(SD, sp); vr = np.asarray(im).astype(int); h, w = vr.shape[:2]; opak = vr[..., 3] == 255
    X, Y = 8 * m * (y + ky - x - kx) - vl * m // 2, 4 * m * (x + kx + y + ky - z) - na * m // 2
    best = None
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            x0, y0 = X + xo + dx, Y + yo + dy
            if x0 < 0 or y0 < 0 or x0 + w > W or y0 + h > H: continue
            kus_f = foto[y0:y0 + h, x0:x0 + w]
            n = int(((np.abs(kus_f - vr[..., :3]).max(-1) == 0) & opak).sum())
            if best is None or n > best[0]: best = (n, dx, dy, int(opak.sum()), x0, y0)
    if best is None: print(f"vuz {v} {nat} dil {kus} smer {smer}: mimo fotku"); continue
    n, dx, dy, celkem, x0, y0 = best
    vysl.append((v, nat, kus, smer, n, celkem, dx, dy, x0, y0, w, h))
    print(f"vuz {v:2d} {nat:8s} dil {kus} smer {smer} stav {stav:>2s}: presne {n:6d}/{celkem:6d} ({100*n/max(celkem,1):5.1f} %) posun ({dx},{dy})")
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
Z = 2 if zin == 4 else 1; ok = 10 * m
kusy = []
for v, nat, kus, smer, n, celkem, dx, dy, x0, y0, w, h in vysl:
    im = Image.fromarray(foto[max(0, y0 - ok):y0 + h + ok, max(0, x0 - ok):x0 + w + ok].astype(np.uint8))
    kusy.append((f"{nat} dil {kus} s{smer} {100*n/max(celkem,1):.0f}% ({dx},{dy})", im.resize((im.width * Z, im.height * Z), Image.NEAREST)))
if kusy:
    cw = max(im.width for _, im in kusy) + 8; ch = max(im.height for _, im in kusy) + 26
    cols = min(len(kusy), 3); rows = math.ceil(len(kusy) / cols)
    out = Image.new("RGB", (cols * cw + 8, rows * ch + 8), (40, 40, 40)); d = ImageDraw.Draw(out)
    for i, (pop, im) in enumerate(kusy):
        cx, cy = 8 + (i % cols) * cw, 8 + (i // cols) * ch
        d.text((cx, cy), pop, font=f, fill=(255, 255, 255)); out.paste(im, (cx, cy + 20))
    out.save(vystup); print("nahled", out.size)
if len(sys.argv) > 8: json.dump(vysl, open(sys.argv[8], "w"))
