# Pixelova kontrola fotky ze zkusebni hry (hra/README.md, testv3sfoto s TEST_FOTO_SADA=rto): ke kazdemu viditelnemu
# dilu autobusu z logu (V3SDIL, grf MAXf nebo MAXg, dil 0x0110) vezme sprite ze souhrnu balice a fotek (4x nebo 8x),
# polozi ho tam, kam ho kresli hra, a spocita presne shodne pixely; hleda i nejlepsi posun v okoli.
#   python3 kontrola_pixel.py <zin> <log> <fotka.png> <cislo fotky> <adresar fotek> <vystup_nahled.png>
import json, math, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
TU = os.path.dirname(os.path.abspath(__file__))
zin, log, fotka, cislo, FOTKY, vystup = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6]
m = zin // 4
t = open(log, encoding="utf-8", errors="replace").read()
vl, na = map(int, re.search(rf"V3SPOHLED: fotka {cislo} vlevo (-?\d+) nahore (-?\d+)", t).groups())
dily = []
for mm in re.finditer(rf"V3SDIL: fotka {cislo} vuz (\d+) grf (\S+) dil 0x([0-9A-F]+) x (\d+) y (\d+) z (\d+) smer (\d+) stav (\w+) delka (\d+) kresli (-?\d+) (-?\d+)", t):
    v, grf, dil, x, y, z, smer, stav, delka, kx, ky = mm.groups()
    if grf not in ("MAXf", "MAXg") or int(dil, 16) != 0x0110: continue
    dily.append((int(v), grf, int(x), int(y), int(z), int(smer), stav, int(delka), int(kx), int(ky)))
print("dilu autobusu v logu:", len(dily), "vlevo", vl, "nahore", na)
VEL = {"MAXf": "mala", "MAXg": "velka"}
sady = {}
for grf, vel in VEL.items():
    souhrn = [f for f in os.listdir(os.path.join(TU, "grf", vel)) if f.endswith("-souhrn.json")]
    if not souhrn: continue
    s = json.load(open(os.path.join(TU, "grf", vel, souhrn[0])))["sprity_zin8" if zin == 8 else "sprity"]["cervena"]
    adr = os.path.join(FOTKY, f"{vel}_cervena")
    out = []
    for d in range(8):
        w, h, xo, yo = s[d]
        foto = Image.open(os.path.join(adr, f"d{d}.png")).convert("RGBA"); bb = foto.getbbox()
        im = np.asarray(Image.open(os.path.join(adr + "_zin8", f"d{d}.png")).convert("RGBA").crop((2 * bb[0], 2 * bb[1], 2 * bb[2], 2 * bb[3]))).astype(int) if zin == 8 else np.asarray(foto.crop(bb)).astype(int)
        assert im.shape[1] == w and im.shape[0] == h, (vel, d, im.shape, w, h)
        out.append((im, xo, yo))
    sady[grf] = out
foto = np.asarray(Image.open(fotka).convert("RGB")).astype(int); H, W = foto.shape[:2]
r = 8 * m
vysl = []
for v, grf, x, y, z, smer, stav, delka, kx, ky in dily:
    if grf not in sady: print(f"vuz {v} {grf}: chybi souhrn"); continue
    vr, xo, yo = sady[grf][smer]; h, w = vr.shape[:2]; opak = vr[..., 3] == 255
    X, Y = 8 * m * (y + ky - x - kx) - vl * m // 2, 4 * m * (x + kx + y + ky - z) - na * m // 2
    best = None
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            x0, y0 = X + xo + dx, Y + yo + dy
            if x0 < 0 or y0 < 0 or x0 + w > W or y0 + h > H: continue
            kus = foto[y0:y0 + h, x0:x0 + w]
            n = int(((np.abs(kus - vr[..., :3]).max(-1) == 0) & opak).sum())
            if best is None or n > best[0]: best = (n, dx, dy, int(opak.sum()), x0, y0)
    if best is None: print(f"vuz {v} {grf} smer {smer}: mimo fotku"); continue
    n, dx, dy, celkem, x0, y0 = best
    vysl.append((v, grf, smer, n, celkem, dx, dy, x0, y0, w, h))
    print(f"vuz {v:2d} {grf} {VEL[grf]:5s} smer {smer} stav {stav:>2s}: presne {n:6d}/{celkem:6d} ({100*n/max(celkem,1):5.1f} %) posun ({dx},{dy})")
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
Z = 2 if zin == 4 else 1; ok = 10 * m
kusy = []
for v, grf, smer, n, celkem, dx, dy, x0, y0, w, h in vysl:
    im = Image.fromarray(foto[max(0, y0 - ok):y0 + h + ok, max(0, x0 - ok):x0 + w + ok].astype(np.uint8))
    kusy.append((f"{VEL[grf]} s{smer} {100*n/max(celkem,1):.0f}% ({dx},{dy})", im.resize((im.width * Z, im.height * Z), Image.NEAREST)))
if kusy:
    cw = max(im.width for _, im in kusy) + 8; ch = max(im.height for _, im in kusy) + 26
    cols = min(len(kusy), 4); rows = math.ceil(len(kusy) / cols)
    out = Image.new("RGB", (cols * cw + 8, rows * ch + 8), (40, 40, 40)); d = ImageDraw.Draw(out)
    for i, (pop, im) in enumerate(kusy):
        cx, cy = 8 + (i % cols) * cw, 8 + (i // cols) * ch
        d.text((cx, cy), pop, font=f, fill=(255, 255, 255)); out.paste(im, (cx, cy + 20))
    out.save(vystup); print("nahled", out.size)
if len(sys.argv) > 7: json.dump(vysl, open(sys.argv[7], "w"))
