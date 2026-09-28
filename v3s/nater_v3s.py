# -*- coding: utf-8 -*-
# Natery Pragy V3S. Vojenska = textury modelu beze zmeny. Modra ("komunisticka modra", hrac 28. 9.)
# = olivovy lak premalovany na modro se zachovanim stinu, spiny a rzi. Pneumatiky, sklo, svetla,
# cedulka PRAGA V3S a rez zustavaji. Modra ma ctyri odstiny podle nakladu (hrac: "vsechny modry
# pouzijem, michej to"): A zbozi, B zemedelstvi, C stavby (svetloucka), D strojirenstvi (tmava).
# Textury v modelu: Image_0 kola a vnitrek dveri, Image_1 kabina a podvozek, Image_2 korba a vnitrek,
# Image_3 sklo.
import numpy as np

# Cilova barva laku v texture (na fotce vyjde tmavsi a mekci, render ji ztlumi)
ODSTINY = {"A": (30, 60, 130), "B": (40, 62, 100), "C": (60, 90, 130), "D": (25, 45, 95)}

def _jas(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

def _hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return h, s, mx / 255

def _rampa(x, a, b):
    """0 pod a, 1 nad b, mezi tim plynule"""
    return np.clip((x - a) / (b - a), 0, 1)

def vaha_laku(a):
    """jak moc je pixel olivovy lak: odstin 36-80 st. (olivova, khaki), rez a hnede drevo (pod 30 st.) ne,
    jasne syte zlute (cedulka) ne"""
    h, s, v = _hsv(a)
    w = _rampa(h, 30, 38) * (1 - _rampa(h, 76, 86)) * _rampa(s, 0.06, 0.14) * _rampa(v, 0.02, 0.05)
    w *= 1 - (_rampa(v, 0.5, 0.6) * _rampa(s, 0.42, 0.5))
    return w

REF = {}

def nastav_ref(rgb_kabina):
    """referencni jas laku: median jasu cisteho laku na texture kabiny (Image_1)"""
    a = rgb_kabina.astype(float)
    REF["lak"] = float(np.median(_jas(a)[vaha_laku(a) > 0.9]))
    return REF["lak"]

def modra(nazev, rgb, odstin):
    """rgb: HxWx3 uint8 (radky shora). Vrati texturu v modrem nateru daneho odstinu (A-D)."""
    if nazev not in ("Image_0", "Image_1", "Image_2"):
        return rgb
    a = rgb.astype(float)
    w = vaha_laku(a)
    f = np.clip(_jas(a) / REF["lak"], 0.12, 2.2)[..., None]
    nove = np.clip(np.array(ODSTINY[odstin], float)[None, None, :] * f, 0, 255)
    out = a * (1 - w[..., None]) + nove * w[..., None]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)
