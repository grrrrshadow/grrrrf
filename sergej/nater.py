# Nátěry M62: zelený (původní textura) a červený ČSD se žlutým pruhem pod čelním oknem.
# Pracuje přímo s obrázky textur z diesel_locomotive_m62.glb (Image_0, Image_6, Image_8).
import numpy as np

# Cílové barvy textury. Ladí se tak, aby na fotce vyšla barva brejlovce z CZTR
# (ČSD červená 132,31,31 a žlutá 154,123,20 na spritu), viz ladeni_barvy v render_sergej.py.
CERVENA = np.array([159, 18, 25], float)
ZLUTA = np.array([190, 174, 9], float)

def _jas(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

def maska_zelena(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    return (g >= r) & (g >= b) & (s > 0.2) & (mx > 20) & ((g - r) > 15)

def maska_losos(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 150) & (r - g > 45) & (g > 60) & (r - b > 55)

def maska_krem(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 160) & (g > 150) & (b > 100) & (np.abs(r - g) < 40)

def prebarvit(pole, cil, maska, ref_jas):
    """Barvy v masce na cilovou barvu, se zachovanim pomeru jasu (stiny, spina, spary)."""
    f = np.clip(_jas(pole) / ref_jas, 0.15, 1.8)[..., None]
    nove = np.clip(cil[None, None, :] * f, 0, 255)
    pole[maska] = nove[maska]

def cerveny(nazev, rgb):
    """rgb: pole HxWx3 (uint8) textury; vrati novou texturu v cervenem natiru."""
    a = rgb.astype(float)
    out = a.copy()
    h, w = a.shape[:2]
    y = np.arange(h)[:, None] * np.ones((1, w))
    zel = maska_zelena(a)
    if nazev in ("Image_0", "Image_6"):
        zel &= y >= 452                 # boky a cela; nahore je strecha a drobnosti, tam zelena neni
    ref = np.median(_jas(a)[zel]) if zel.any() else 1.0
    prebarvit(out, CERVENA, zel, ref)
    if nazev in ("Image_0", "Image_6"):
        los = maska_losos(a); krem = maska_krem(a)
        # boky (452-770): kremove linky do cervene, bok bude hladky jako u brejlovce
        bok = krem & (y >= 452) & (y < 770)
        if bok.any():
            prebarvit(out, CERVENA, bok, np.median(_jas(a)[bok]))
        # cela (770+). Textura je vzhuru nohama: okna jsou na radcich 953-1010, pod nimi
        # (ve skutecnosti) lososovy pruh 934-946, zelena mezera 918-933, kremova linka 906-915.
        # Zluty pruh: radky 918-934 pres celou natrenou sirku cela, kus od okna (hrac:
        # "pruh pod okno kus od okna", jako CZTR brejlovci). Mezi nim a oknem zustane cervena.
        x = np.arange(w)[None, :] * np.ones((h, 1))
        natrene = zel | los | krem
        pod_oknem = natrene & (y >= 918) & (y <= 934) & (x < 900)
        zbytek = (los | krem) & (y >= 770) & ~pod_oknem
        # okraje stareho lososoveho pruhu pod okny (vyhlazene, ruzove a svetle tecky)
        r_, g_, b_ = a[..., 0], a[..., 1], a[..., 2]
        okraje = (y >= 928) & (y <= 952) & (x < 900) & (r_ > 110) & (r_ > g_ + 12) & (r_ > b_ + 12)
        zbytek |= okraje & ~pod_oknem
        if zbytek.any():
            prebarvit(out, CERVENA, zbytek, np.median(_jas(a)[zbytek]))
        ref_pas = np.median(_jas(a)[pod_oknem & zel]) if (pod_oknem & zel).any() else 1.0
        f = np.clip(_jas(a) / ref_pas, 0.8, 1.15)[..., None]
        zl = np.clip(ZLUTA[None, None, :] * f, 0, 255)
        out[pod_oknem] = zl[pod_oknem]
    return np.clip(out, 0, 255).astype(np.uint8)
