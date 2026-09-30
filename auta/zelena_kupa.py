# Zelena kupa marihuany: kupa brambor (valnik 0x88) prebarvena na herni zelenou marihuany (paleta 0x52-0x57)
# Kupa = body, ktere se lisi od tychz bodu u aspon 3 ze 4 jinych valniku (pisek, jil, uhli, kamen): karoserie
# a korba jsou u vsech stejne, lisi se jen kupa.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vwt1_sprity import rozeber
from PIL import Image
import numpy as np
Y = sys.argv[1]; LIST = sys.argv[2]; VZOR = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0x88
s = rozeber(Y)
list_ = np.array(Image.open(LIST).convert("RGBA")).astype(int)
OSTATNI = [v for v in (0x86, 0x85, 0x84, 0x87, 0x88) if v != VZOR]
RAMPA = np.array([(32, 80, 4), (48, 96, 4), (64, 112, 12), (84, 132, 20), (104, 148, 28), (128, 168, 44), (144, 184, 60)], float)
def vyrez(sp):
    return list_[sp["y"]:sp["y"] + sp["h"], sp["x"]:sp["x"] + sp["w"]]
def zelena(sada, smer):
    sp = s[VZOR][sada][smer]; a = vyrez(sp)
    lisi = np.zeros(a.shape[:2], int)
    for v in OSTATNI:
        spb = s[v][sada][smer]
        b = np.zeros_like(a)                     # b v ramu obrazku a, zarovnane podle posunu na obrazovce
        dx, dy = sp["xo"] - spb["xo"], sp["yo"] - spb["yo"]
        bb = vyrez(spb)
        for yy in range(a.shape[0]):
            y2 = yy + dy
            if 0 <= y2 < bb.shape[0]:
                x0, x1 = max(0, -dx), min(a.shape[1], bb.shape[1] - dx)
                if x1 > x0: b[yy, x0:x1] = bb[y2, x0 + dx:x1 + dx]
        lisi += (np.abs(a[..., :3] - b[..., :3]).sum(-1) > 40) | (np.abs(a[..., 3] - b[..., 3]) > 60)
    maska = (lisi >= len(OSTATNI) - 1) & (a[..., 3] > 0)
    # jen body v barve kupy brambor (odstin 25-60 stupnu): zrcadleni kupy v okne kabiny je cervene a zustane
    r, g, bl = a[..., 0] / 255.0, a[..., 1] / 255.0, a[..., 2] / 255.0
    mx, mn = np.maximum(np.maximum(r, g), bl), np.minimum(np.minimum(r, g), bl)
    d = np.where(mx - mn == 0, 1, mx - mn)
    h = np.where(mx == r, ((g - bl) / d) % 6, np.where(mx == g, (bl - r) / d + 2, (r - g) / d + 4)) * 60
    maska &= (h >= 25) & (h <= 60) & (mx - mn > 0.02)
    out = a.copy()
    if maska.any():
        L = (0.30 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2])
        lo, hi = np.percentile(L[maska], 3), np.percentile(L[maska], 97)
        t = np.clip((L - lo) / max(hi - lo, 1), 0, 1) * (len(RAMPA) - 1)
        i0 = np.floor(t).astype(int); i1 = np.minimum(i0 + 1, len(RAMPA) - 1); f = (t - i0)[..., None]
        barva = RAMPA[i0] * (1 - f) + RAMPA[i1] * f
        out[..., :3][maska] = np.round(barva[maska]).astype(int)
    return out.astype(np.uint8), maska, sp
if __name__ == "__main__":
    import pickle
    vysl = {(sada, smer): zelena(sada, smer) for sada in (1, 2) for smer in range(8)}
    pickle.dump({k: (v[0], v[1], v[2]) for k, v in vysl.items()}, open(sys.argv[4], "wb"))
    print("bodu kupy:", {k: int(v[1].sum()) for k, v in vysl.items()})
