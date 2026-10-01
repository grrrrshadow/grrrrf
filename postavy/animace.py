#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Druhy obrazek do animace (budova s postavami) sloucit s prvnim (bez postav) tak, aby se lisily jen tam, kde
# postavy a jejich stiny opravdu jsou. Kazdy render ma trochu jiny sum a pri strídani by jinak blikala cela budova.
#   python3 animace.py <bez_postav.png> <s_postavami.png> <vystup.png>
# Zmena = pixel se lisi o vic nez 6 (z 255) a aspon 3 jeho sousede taky; maska se rozsiri o 2 px a zmekci, mimo ni
# se vezme obrazek bez postav. JSON s rohy pozemku se zkopiruje od obrazku s postavami.
import json, os, shutil, sys
import numpy as np
from PIL import Image, ImageFilter

PRAH = 6


def sloucit(bez, s, vystup):
    a = np.asarray(Image.open(bez).convert("RGBA")).astype(float)
    b = np.asarray(Image.open(s).convert("RGBA")).astype(float)
    d = np.abs(a - b).max(axis=2)
    zmena = d > PRAH
    sousedu = np.asarray(Image.fromarray((zmena * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(1))).astype(float) / 255 * 9
    jadro = Image.fromarray(((zmena & (sousedu >= 3)) * 255).astype(np.uint8))
    maska = jadro.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
    w = np.asarray(maska).astype(float)[..., None] / 255
    c = a * (1 - w) + b * w
    Image.fromarray(np.clip(c + 0.5, 0, 255).astype(np.uint8), "RGBA").save(vystup)
    j = os.path.splitext(s)[0] + ".json"
    if os.path.exists(j):
        shutil.copyfile(j, os.path.splitext(vystup)[0] + ".json")
    mimo = int(((d > 4) & (w[..., 0] < 0.01)).sum())
    print(vystup, "maska", int((w[..., 0] > 0.01).sum()), "px, sum mimo masku zahozen u", mimo, "px")


if __name__ == "__main__":
    sloucit(*sys.argv[1:4])
