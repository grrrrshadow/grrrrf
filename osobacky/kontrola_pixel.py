# Pixelova kontrola fotky ze zkusebni hry (hra/README.md, testv3sfoto s TEST_FOTO_SADA=osobacky): ke kazdemu vozu
# z logu (V3SDIL, grf MAXh) vezme sprite z GRF (jen zin8) a polozi ho tam, kam ho kresli hra. Ve 4x ho nejdriv zmensi
# stejne jako hra od afed76d (prumer kazdeho bloku 2x2 vazeny alfou, alfa = prumer), takze se overuje i dopocitane 4x.
# Pocita presne shodne pixely (jen plne kryte), hleda i nejlepsi posun v okoli.
#   python3 kontrola_pixel.py <zin 8|4> <log> <fotka.png> <cislo fotky> <adresar grf> <vystup_nahled.png> [vysledky.json]
import json, math, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
zin, log, fotka, cislo, GRF, vystup = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6]
m = zin // 4
t = open(log, encoding="utf-8", errors="replace").read()
vl, na = map(int, re.search(rf"V3SPOHLED: fotka {cislo} vlevo (-?\d+) nahore (-?\d+)", t).groups())
dily = []
for mm in re.finditer(rf"V3SDIL: fotka {cislo} vuz (\d+) grf (\S+) dil 0x([0-9A-F]+) x (\d+) y (\d+) z (\d+) smer (\d+) stav (\w+) delka (\d+) kresli (-?\d+) (-?\d+)", t):
    v, grf, dil, x, y, z, smer, stav, delka, kx, ky = mm.groups()
    if grf != "MAXh": continue
    dily.append((int(v), int(dil, 16), int(x), int(y), int(z), int(smer), stav, int(delka), int(kx), int(ky)))
print("vozu MAXh v logu:", len(dily), "vlevo", vl, "nahore", na)

# sprity z yaglu: id 1-8 orig smery 0-7, 9 nakup, 10-17 zmensena, 18 nakup
yg = [f for f in os.listdir(os.path.join(GRF, "sprites")) if f.endswith(".yagl")][0]
radky = re.findall(r"\[(\d+), (\d+), (-?\d+), (-?\d+)\], zin8, c32bpp \| chunked, \"([^\"]+)\", \[(\d+), (\d+)\]",
                   open(os.path.join(GRF, "sprites", yg), encoding="utf-8").read())
listy = {}
def sprite8(k):
    w, h, xo, yo, png, px, py = radky[k]
    w, h, xo, yo, px, py = map(int, (w, h, xo, yo, px, py))
    if png not in listy: listy[png] = Image.open(os.path.join(GRF, "sprites", png)).convert("RGBA")
    return np.asarray(listy[png].crop((px, py, px + w, py + h))).astype(np.int64), xo, yo

def zmensi(im):
    """4x z 8x jako hra (spritecache.cpp ResizeSpriteOut od afed76d): barva = (sum c*a + suma/2) / suma, alfa = prumer"""
    h, w = im.shape[:2]
    H2, W2 = (h + 1) // 2, (w + 1) // 2
    out = np.zeros((H2, W2, 4), np.int64)
    for y in range(H2):
        for x in range(W2):
            blk = im[2 * y:2 * y + 2, 2 * x:2 * x + 2].reshape(-1, 4)
            a = blk[:, 3]; sa = a.sum()
            if sa == 0: continue
            out[y, x, :3] = (blk[:, :3] * a[:, None]).sum(0) * 1 + sa // 2
            out[y, x, :3] //= sa
            out[y, x, 3] = (sa + len(a) // 2) // len(a)
    return out

SADA = {0x0100: 0, 0x0101: 9}
JM = {0x0100: "orig", 0x0101: "zmensena"}
foto = np.asarray(Image.open(fotka).convert("RGB")).astype(np.int64); H, W = foto.shape[:2]
r = 6 * m
vysl = []
cache = {}
for v, dil, x, y, z, smer, stav, delka, kx, ky in dily:
    k = SADA[dil] + smer
    if k not in cache:
        im, xo, yo = sprite8(k)
        if zin == 4:
            assert xo % 2 == 0 and yo % 2 == 0, (k, xo, yo)
            im, xo, yo = zmensi(im), xo // 2, yo // 2
        cache[k] = (im, xo, yo)
    vr, xo, yo = cache[k]; h, w = vr.shape[:2]; opak = vr[..., 3] == 255
    X, Y = 8 * m * (y + ky - x - kx) - vl * m // 2, 4 * m * (x + kx + y + ky - z) - na * m // 2
    best = None
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            x0, y0 = X + xo + dx, Y + yo + dy
            if x0 < 0 or y0 < 0 or x0 + w > W or y0 + h > H: continue
            kus = foto[y0:y0 + h, x0:x0 + w]
            n = int(((np.abs(kus - vr[..., :3]).max(-1) == 0) & opak).sum())
            if best is None or n > best[0]: best = (n, dx, dy, int(opak.sum()), x0, y0)
    if best is None: print(f"vuz {v} {JM[dil]} smer {smer}: mimo fotku"); continue
    n, dx, dy, celkem, x0, y0 = best
    vysl.append((v, JM[dil], smer, n, celkem, dx, dy, x0, y0, w, h))
    print(f"vuz {v:2d} {JM[dil]:8s} smer {smer} stav {stav:>2s}: presne {n:6d}/{celkem:6d} ({100*n/max(celkem,1):5.1f} %) posun ({dx},{dy})")
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
Z = 2 if zin == 4 else 1; ok = 10 * m
kusy = []
for v, jm, smer, n, celkem, dx, dy, x0, y0, w, h in vysl:
    im = Image.fromarray(foto[max(0, y0 - ok):y0 + h + ok, max(0, x0 - ok):x0 + w + ok].astype(np.uint8))
    kusy.append((f"{jm} s{smer} {100*n/max(celkem,1):.0f}% ({dx},{dy})", im.resize((im.width * Z, im.height * Z), Image.NEAREST)))
if kusy:
    cw = max(im.width for _, im in kusy) + 8; ch = max(im.height for _, im in kusy) + 26
    cols = min(len(kusy), 4); rows = math.ceil(len(kusy) / cols)
    out = Image.new("RGB", (cols * cw + 8, rows * ch + 8), (40, 40, 40)); d = ImageDraw.Draw(out)
    for i, (pop, im) in enumerate(kusy):
        cx, cy = 8 + (i % cols) * cw, 8 + (i // cols) * ch
        d.text((cx, cy), pop, font=f, fill=(255, 255, 255)); out.paste(im, (cx, cy + 20))
    out.save(vystup); print("nahled", out.size)
if len(sys.argv) > 7: json.dump(vysl, open(sys.argv[7], "w"))
