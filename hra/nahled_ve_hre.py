#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nahled budov ve fotce ze zkusebni hry (silnicni okruh s Tatrami, priblizeni 4x) s polohou jako ve hre:
# - zeme v okruhu lezi ve vysce 16 (dve urovne, auta tam maji z 16), dlazdice je proto o 4 * 16 = 64 px vys, nez
#   by byla dole. Tuhle vysku jsem driv vynechaval a vsechny nahledy byly o pul policka niz (u automatu pak krovi
#   lezlo na silnici, i kdyz ve hre nepresahuje).
# - policko ve hre ma 256 x 124 px (render 256 x 128), obrazek se proto svisle stahne na 124/128 jako ve hre.
# - severni roh rovne dlazdice lezi ve hre o 4 px vpravo od hranice pixelu, kam ho klade render.
# Posledni dve veci podle zpravy od hry (zarovnani-budov/ZPRAVA-OD-HRY.md, skript hry openttd_gymnazium.py).
#
#   python3 nahled_ve_hre.py <vystup.png> <obrazek.png>@<x>,<y>[=popisek] ... [--vyrez L,T,R,B] [--zvetsit N]
#
# x, y je severni dlazdice budovy. Rohy pozemku se ctou z JSONu vedle obrazku; "stazeny": true znamena, ze obrazek
# uz ma vysku hry a nestahuje se. Popisek se napise pod jizni roh pozemku. Vyrez je v pixelech fotky od severniho
# rohu prvni budovy (vychozi -330,-150,330,330), zvetseni bez vyhlazovani (vychozi 2).
# Dlazdice v okruhu: silnice vede po y = 12 a y = 18 (x 40 az 51) a po x = 40 a x = 51 (y 12 az 18), uvnitr je
# trava; napr. (44,17) je primo u silnice, (45,16) o policko dal.
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

TU = os.path.dirname(os.path.abspath(__file__))
FOTKA = os.path.join(TU, "fotka_okruh_v11.png")       # v3s_okruh_02.png ze zkousky v11, pohled vlevo -5440 nahore 2840
VLEVO, NAHORE, Z_ZEME = -5440, 2840, 16
SEVER_POSUN = 4
RENDER_VYSKA, HRA_VYSKA = 128, 124
PISMO = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def sever_dlazdice(x, y):
    """pixel fotky, kde lezi severni roh dlazdice (x, y) ve hre"""
    return 128 * (y - x) - VLEVO + SEVER_POSUN, 64 * (x + y) - 4 * Z_ZEME - NAHORE


def nacti(cesta):
    """obrazek ve vysce hry a rohy pozemku na nem"""
    im = Image.open(cesta).convert("RGBA")
    info = json.load(open(os.path.splitext(cesta)[0] + ".json"))
    rohy = {k: tuple(v) for k, v in info["rohy"].items()}
    if not info.get("stazeny"):
        k = HRA_VYSKA / RENDER_VYSKA
        im = im.resize((im.width, round(im.height * k)), Image.LANCZOS)
        rohy = {n: (v[0], v[1] * k) for n, v in rohy.items()}
    return im, rohy


def main(argv):
    vystup, budovy, vyrez, zvetsit = argv[0], [], (-330, -150, 330, 330), 2
    i = 1
    while i < len(argv):
        if argv[i] == "--vyrez":
            vyrez = tuple(int(v) for v in argv[i + 1].split(",")); i += 2; continue
        if argv[i] == "--zvetsit":
            zvetsit = int(argv[i + 1]); i += 2; continue
        cesta, _, zbytek = argv[i].partition("@")
        misto, _, popisek = zbytek.partition("=")
        budovy.append((cesta, tuple(int(v) for v in misto.split(",")), popisek)); i += 1
    fotka = Image.open(FOTKA).convert("RGBA")
    popisky = []
    for cesta, (x, y), popisek in budovy:
        im, rohy = nacti(cesta)
        sx, sy = sever_dlazdice(x, y)
        ox, oy = round(sx - rohy["sever"][0]), round(sy - rohy["sever"][1])
        fotka.alpha_composite(im, (ox, oy))
        if popisek:
            popisky.append((popisek, ox + rohy["jih"][0], oy + rohy["jih"][1]))
    x0, y0 = sever_dlazdice(*budovy[0][1])
    L, T = x0 + vyrez[0], y0 + vyrez[1]
    v = fotka.crop((L, T, x0 + vyrez[2], y0 + vyrez[3])).convert("RGB")
    v = v.resize((v.width * zvetsit, v.height * zvetsit), Image.NEAREST)
    d = ImageDraw.Draw(v); f = ImageFont.truetype(PISMO, 13 * zvetsit)
    for text, px, py in popisky:
        X, Y = (px - L) * zvetsit, (py - T) * zvetsit + 15 * zvetsit
        d.text((X + 2, Y + 2), text, font=f, fill=(0, 0, 0), anchor="mm"); d.text((X, Y), text, font=f, fill=(255, 255, 255), anchor="mm")
    v.save(vystup)
    print(vystup, v.size)


if __name__ == "__main__":
    main(sys.argv[1:])
