# -*- coding: utf-8 -*-
# Jak hra kresli vlak, prepsano ze zdrojaku OpenTTD (forclaude/openttd/src, jen cteno):
#   landscape.h      RemapCoords: x_obr = (y - x) * 2 * ZOOM_BASE, y_obr = (y + x - z) * ZOOM_BASE, ZOOM_BASE = 4 (zin4)
#   vehicle.cpp      DoDrawVehicle -> AddSortableSpriteToDraw(sprite, x_pos, y_pos, z_pos, bounds)
#   viewport.cpp     sprite se kresli na RemapCoords(poloha + bounds.origin + bounds.offset)
#   train_cmd.cpp    Train::UpdateDeltaXY nastavuje bounds podle smeru a delky clanku
#   train.h          Train::CalcNextVehicleOffset: rozestup clanku = L_a / 2 + (L_b + 1) / 2
import re, os
from PIL import Image

ROVNE = (1, 3, 5, 7)                              # NE, SE, SW, NW: po rovne koleji, na obrazovce sikmo
# jednotkovy krok ve svete pro smer jizdy (vycet Direction: N, NE, E, SE, S, SW, W, NW)
SMER = {0: (-1, -1), 1: (-1, 0), 2: (-1, 1), 3: (0, 1), 4: (1, 1), 5: (1, 0), 6: (1, -1), 7: (0, -1)}

def remap(x, y, z=0):
    """RemapCoords v zin4."""
    return ((y - x) * 2 * 4, (y + x - z) * 4)

KROK = {d: remap(*SMER[d]) for d in SMER}         # posun na obrazovce o jednu osminu ve smeru jizdy

def kotva_hry(L, d):
    """bounds.origin + bounds.offset z Train::UpdateDeltaXY pro nepreklopeny clanek delky L (osmin)."""
    if d not in ROVNE:
        hs = (8 - L) // 2
        sx, sy = {0: (-1, -1), 2: (-1, 1), 4: (1, 1), 6: (1, -1)}[d]
        return (-1 - hs * sx, -1 - hs * sy)
    if d == 1: return (-((L + 1) // 2) + 1, -1)
    if d == 7: return (-1, -((L + 1) // 2) + 1)
    if d == 5: return (-(L // 2) + 1 - (8 - L), -1)
    return (-1, -(L // 2) + 1 - (8 - L))           # d == 3

def odstupy(delky):
    """O kolik osmin je hlava pred stredem a zad za stredem."""
    h, s, z = delky
    return h // 2 + (s + 1) // 2, s // 2 + (z + 1) // 2

def nacti_sady(adresar, yagl, zin=4):
    """Sady spritu z (rozbaleneho) yaglu v poradi, kazda jako seznam (w, h, xoffs, yoffs, png, x, y) podle zoomu
    zin (4 nebo 8); sprite bez radku toho zoomu (prazdne smery maji jen zin4) je None."""
    text = open(os.path.join(adresar, yagl)).read()
    vzor = re.compile(r"\[(\d+), (\d+), (-?\d+), (-?\d+)\], zin" + str(zin) + r", [^\"]*\"([^\"]+)\", \[(\d+), (\d+)\]")
    sady = []
    for rec in re.findall(r"sprite_sets<Trains[^>]*>.*?\n\}", text, re.S):
        for blok in re.split(r"\n    sprite_set", rec)[1:]:
            sada = []
            for sp in re.split(r"sprite_id<", blok)[1:]:
                m = vzor.search(sp)
                sada.append(tuple(int(v) if i != 4 else v for i, v in enumerate(m.groups())) if m else None)
            sady.append(sada)
    return sady

_listy = {}
def obrazek(adresar, sp):
    if sp is None: return Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0, 0
    w, h, xo, yo, png, x, y = sp
    klic = os.path.join(adresar, png)
    if klic not in _listy: _listy[klic] = Image.open(klic).convert("RGBA")
    return _listy[klic].crop((x, y, x + w, y + h)), xo, yo
