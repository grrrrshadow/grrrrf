# -*- coding: utf-8 -*-
# Textury natieru РЖД: z model/teplovoz-m62.glb (release par8, "Teplovoz-m62 РЖД", Leafia dev., CC BY 4.0) vytahne
# obrazky 1 (telo), 2 (zaluzie) a 6 (spojka) jako model/rzd_telo.png, rzd_zaluzie.png a rzd_spojka.png.
# Model ma stejne UV jako diesel_locomotive_m62.glb, nater.rzd je jen vymeni. Spousti se bez argumentu.
import io, json, os, struct
from PIL import Image

TU = os.path.dirname(os.path.abspath(__file__))
GLB = os.path.join(TU, "model", "teplovoz-m62.glb")
OBRAZKY = {1: "rzd_telo.png", 2: "rzd_zaluzie.png", 6: "rzd_spojka.png"}

with open(GLB, "rb") as h:
    magic, verze, delka = struct.unpack("<III", h.read(12))
    assert magic == 0x46546C67, "neni glb"
    delka_json, _ = struct.unpack("<II", h.read(8)); js = json.loads(h.read(delka_json))
    delka_bin, _ = struct.unpack("<II", h.read(8)); binarni = h.read(delka_bin)
extras = js.get("asset", {}).get("extras", {})
assert "Leafia" in extras.get("author", ""), extras
for i, jmeno in OBRAZKY.items():
    bv = js["bufferViews"][js["images"][i]["bufferView"]]; od = bv.get("byteOffset", 0)
    im = Image.open(io.BytesIO(binarni[od:od + bv["byteLength"]])).convert("RGB")
    im.save(os.path.join(TU, "model", jmeno), optimize=True)
    print(jmeno, im.size)
