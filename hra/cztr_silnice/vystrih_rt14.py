# -*- coding: utf-8 -*-
# Vystrizek z CZTR Road set 2.3.1 pro zkusebni hru (hrac 28. 9.: "vystrihni sprity CZTR silnice 1. trida
# venkov, to bys hned videl; priprav si CZTR silnici jen 1. trida venkov, bohate staci").
# Bere jen povrch silnice RT14 "1. trida - venkov" (Record #196, sada 0, 19 spritu, v Action3 typ 0x02 = ground).
# Zastavky, depo, most a kurzory zustanou vychozi. Aby po ni smela bezna auta (typ ROAD), pridava RT14
# do "powered" seznamu ROAD, jako to dela cela sada (bity se k existujicim pricitaji).
#   python3 vystrih_rt14.py <rozbaleny CZTR_Road_set sprites/> <vystup>
# Pak ve <vystup>: yagl -e CZTR_silnice_RT14.grf
import os, re, sys
from PIL import Image

ZDROJ, VYSTUP = sys.argv[1], sys.argv[2]
text = open(os.path.join(ZDROJ, "CZTR_Road_set.yagl"), encoding="utf-8").read()
rec = text.split("// Record #196\n", 1)[1].split("// Record #197", 1)[0]
sada0 = re.split(r"\n    sprite_set", rec)[1]
sprity = re.findall(r"sprite_id<0x[0-9A-F]+>\s*\{(.*?)\n        \}", sada0, re.S)
assert len(sprity) == 19, len(sprity)
# kontrola, ze RT14 je opravdu 0x000D a ze Action3 bere ground ze skupiny z Record #197
assert 'roadtype_label: "RT14"' in text.split("// Record #195\n", 1)[1].split("// Record #196", 1)[0]
assert "0x02: 0x00F7;" in text.split("// Record #198\n", 1)[1].split("// Record #199", 1)[0]

RADEK = re.compile(r'\[(\d+), (\d+), (-?\d+), (-?\d+)\], (\w+), ([\w |]+), "([^"]+)", \[(\d+), (\d+)\];')
listy, novy = {}, {}
def zdroj(f):
    if f not in listy: listy[f] = Image.open(os.path.join(ZDROJ, f))
    return listy[f]
polozky = {}                                        # (zoom, hloubka) -> [(obrazek, klic)]
radky = []
for i, sp in enumerate(sprity):
    for m in RADEK.finditer(sp):
        w, h, xo, yo, zoom, hl, f, x, y = m.groups()
        w, h, x, y = int(w), int(h), int(x), int(y)
        im = zdroj(f).crop((x, y, x + w, y + h))
        polozky.setdefault((zoom, hl.strip()), []).append((im, (i, zoom)))
        radky.append((i, zoom, hl.strip(), w, h, int(xo), int(yo)))
os.makedirs(os.path.join(VYSTUP, "sprites"), exist_ok=True)
pozice, soubor = {}, {}
for (zoom, hl), seznam in polozky.items():
    jm = f"CZTR_silnice_RT14-{'8bpp' if '8bpp' in hl else '32bpp'}-{zoom}.png"
    x, y, radek, sirka = 4, 4, 0, 2048
    for im, k in seznam:
        if x + im.width + 4 > sirka: x = 4; y += radek + 4; radek = 0
        pozice[k] = (x, y); x += im.width + 4; radek = max(radek, im.height)
    mod = seznam[0][0].mode
    list_ = Image.new(mod, (sirka, y + radek + 4)) if mod != "P" else Image.new("P", (sirka, y + radek + 4), 0)
    if mod == "P": list_.putpalette(seznam[0][0].getpalette())
    for im, k in seznam: list_.paste(im, pozice[k])
    list_.save(os.path.join(VYSTUP, "sprites", jm))
    for _, k in seznam: soubor[k] = jm

Y = ['yagl_version: "";', "grf_format: Container2;",
     "grf // Action08", "{", '    grf_id: "MAXr";', "    version: GRF8;",
     '    name: "CZTR silnice 1. třída - venkov (výstřižek pro zkoušky)";',
     '    description: "Jen povrch silnice RT14 z CZTR Road set 2.3.1, CZTR team, CC BY-SA 3.0. Vystřiženo pro zkušební hru, '
     'zastávky, depo a most jsou výchozí.";', "}",
     "strings<RoadTypes, default, 0xDC00*> // Action04", "{", '    /* 0xDC00 */ " [ - ] 1. třída - venkov";', "}",
     "properties<RoadTypes, 0x0000> // Action00, bezna silnice smi na RT14", "{", "    // instance_id: 0x0000", "    {",
     '        roadtype_label: "ROAD";', '        powered_roadtypes: [ "RT14" ];', "    }", "}",
     "properties<RoadTypes, 0x0001> // Action00, RT14 jako v CZTR Road set 2.3.1 (Record #195)", "{", "    // instance_id: 0x0001", "    {",
     '        roadtype_label: "RT14";', "        introduction_date: date(1970/1/1);",
     "        road_type_name_id: 0xDC00;", "        toolbar_caption_id: 0xDC00;", "        dropdown_text_id: 0xDC00;",
     "        window_caption_id: 0xDC00;", "        autoreplace_text_id: 0xDC00;", "        new_engine_text_id: 0xDC00;",
     '        powered_roadtypes: [ "ROAD" ];', "        sort_order: 0x10;", "        construction_costs: 0x000F;",
     "        maintenance_cost_factor: 0x000F;", "        roadtype_flags: 0x04;", "        speed_limit: 0x00C8;", "    }", "}",
     "sprite_sets<RoadTypes, 0x0000> // Action01, povrch RT14 (CZTR Record #196, sada 0)", "{", "    sprite_set // 0x0000", "    {"]
sid = 1
for i in range(19):
    Y += [f"        sprite_id<0x{sid:08X}>", "        {"]
    for (j, zoom, hl, w, h, xo, yo) in radky:
        if j != i: continue
        px, py = pozice[(i, zoom)]
        Y.append(f'            [{w}, {h}, {xo}, {yo}], {zoom}, {hl}, "{soubor[(i, zoom)]}", [{px}, {py}];')
    Y += ["        }"]; sid += 1
Y += ["    }", "}",
      "sprite_groups<RoadTypes, 0xF7> // Action02 basic", "{", "    primary_spritesets: [ 0x0000 ];", "}",
      "feature_graphics<RoadTypes> // Action03", "{", "    livery_override: false;", "    default_set_id: 0x00F7;",
      "    feature_ids: [ 0x0001 ];", "    cargo_types:", "    {", "        0x02: 0x00F7;", "    };", "}"]
open(os.path.join(VYSTUP, "sprites", "CZTR_silnice_RT14.yagl"), "w").write("\n".join(Y) + "\n")
print("spritu", len(sprity), "listy", {k: len(v) for k, v in polozky.items()})
