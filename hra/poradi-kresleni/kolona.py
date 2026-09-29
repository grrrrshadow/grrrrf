# Vystrihne zacpu po radach z fotek pred a po oprave: python3 kolona.py <osa x|y> <vystup> <adresar>
# V adresari ceka kolona_{pred,oprava}_{x,y}.log a .png (vypis a fotka testpruhy ... kolona).
import re, sys
from PIL import Image, ImageDraw
osa, out, P = sys.argv[1], sys.argv[2], sys.argv[3]
def rady(verze):
    t = open(f"{P}/kolona_{verze}_{osa}.log", encoding="utf-8", errors="replace").read()
    L, T = map(int, re.search(r"V3SPOHLED: fotka 0 vlevo (-?\d+) nahore (-?\d+)", t).groups())
    body = {}
    for m in re.finditer(r"V3SDIL: fotka 0 vuz \d+ grf \S+ dil 0x[0-9A-F]+ x (-?\d+) y (-?\d+) z (-?\d+) smer \d+ stav \S+ delka \d+ kresli (-?\d+) (-?\d+)", t):
        x, y, z, kx, ky = map(int, m.groups())
        napric = (y if osa == "x" else x) // 16
        body.setdefault(napric, []).append((8 * (y + ky - x - kx) - L, 4 * (x + kx + y + ky - z) - T))
    im = Image.open(f"{P}/kolona_{verze}_{osa}.png").convert("RGB")
    vysl = []
    for napric in sorted(body):
        xs = [p[0] for p in body[napric]]; ys = [p[1] for p in body[napric]]
        vysl.append(im.crop((min(xs) - 70, min(ys) - 110, max(xs) + 70, max(ys) + 40)))
    return vysl
pred, po = rady("pred"), rady("oprava")
W = max(c.width for c in pred + po); H = sum(c.height + 34 for c in pred + po)
plocha = Image.new("RGB", (W, H), (20, 20, 20)); kr = ImageDraw.Draw(plocha)
yy = 0
for i, (a, b) in enumerate(zip(pred, po)):
    for c, jm in ((a, "PRED opravou"), (b, "PO oprave")):
        kr.text((10, yy + 10), f"rada {i + 1}: {jm}", fill=(255, 255, 255)); plocha.paste(c, (0, yy + 34)); yy += c.height + 34
plocha.save(out); print(plocha.size, [c.size for c in pred])
