# Vystrihne dvojice aut z fotky testpruhy: python3 vystrih.py <log> <fotka> <vystup> [zvetseni]
import re, sys
from PIL import Image, ImageDraw
log, foto, out = sys.argv[1:4]
zv = int(sys.argv[4]) if len(sys.argv) > 4 else 2
t = open(log, encoding="utf-8", errors="replace").read()
L, T = map(int, re.search(r"V3SPOHLED: fotka 0 vlevo (-?\d+) nahore (-?\d+)", t).groups())
dily = {}
for m in re.finditer(r"V3SDIL: fotka 0 vuz (\d+) grf \S+ dil 0x([0-9A-F]+) x (-?\d+) y (-?\d+) z (-?\d+) smer \d+ stav \S+ delka \d+ kresli (-?\d+) (-?\d+)", t):
    vuz, dil, x, y, z, kx, ky = m.groups()
    dily.setdefault(int(vuz), []).append((int(x) + int(kx), int(y) + int(ky), int(z)))
pary = {}
for m in re.finditer(r"PRUHY: rada (\d) par (\d) odstup (\d+) (zadni|predni) vuz (\d+)", t):
    r, k, d, kde, vuz = m.groups()
    pary.setdefault((int(r), int(k), int(d)), set()).add(int(vuz))
im = Image.open(foto).convert("RGB")
CW, CH = 260, 170
bunky = {}
for (r, k, d), vozy in sorted(pary.items()):
    body = [p for v in vozy for p in dily.get(v, [])]
    sx = sum(8 * (y - x) for x, y, z in body) / len(body) - L
    sy = sum(4 * (x + y - z) for x, y, z in body) / len(body) - T
    c = im.crop((int(sx - CW / 2), int(sy - CH / 2 - 20), int(sx + CW / 2), int(sy + CH / 2 - 20)))
    bunky[(r, k, d)] = c.resize((CW * zv, CH * zv), Image.LANCZOS)
rady = sorted({r for r, k, d in bunky}); sloupce = sorted({(k, d) for r, k, d in bunky})
W, H = CW * zv, CH * zv
mrizka = Image.new("RGB", (W * len(sloupce), (H + 30) * len(rady)), (20, 20, 20))
kr = ImageDraw.Draw(mrizka)
for i, r in enumerate(rady):
    for j, (k, d) in enumerate(sloupce):
        mrizka.paste(bunky[(r, k, d)], (j * W, i * (H + 30) + 30))
        kr.text((j * W + 8, i * (H + 30) + 8), f"rada {r + 1}, cela od sebe {d}/16 dlazdice", fill=(255, 255, 255))
mrizka.save(out)
print(mrizka.size)
