# Rostliny marihuany do obrázků budov

Z releasu `par6` (`zip6.zip`, složka `bar/`), všechny ze Sketchfabu pod CC BY 4.0. Autoři a text uvedení pro hru
jsou v `../AUTORI-MODELU.md`.

| soubor | model, autor | použití |
|---|---|---|
| `cannabis_plant.glb` | Cannabis Plant, streetpharmacy | vysoká štíhlá rostlina, u sochy velké vzadu, na plantáži (`pole/`) ve druhé fázi |
| `cannabis_sativa_plant.glb` | Cannabis Sativa plant, Zbrojmistrz | košatá, v souboru je i s květináčem (ten se zahodí), u sochy velké i malé, na plantáži v obou fázích |
| `small_cannabis_plant.glb` | Small Cannabis Plant, streetpharmacy | řídká mladá rostlinka s velkými listy; sama ve velikosti hry skoro není vidět, na plantáži v první fázi přes keř |

`rostliny.py`: načtení bez květináče, přebarvení listů na zelenou nákladu MARI (jas textury → přechod mezi
(48, 98, 10) a (94, 144, 26) jako kupka marihuany na V3S) a postavení více kusů se společnou sítí; když by
koruna byla širší než povolený poloměr, rostlina se do šířky zúží.

Jen jednotlivé soubory ze zipu se dají stáhnout bez celých 328 MB: přesměrování z GitHubu na podepsanou adresu
a pak HTTP Range na konec zipu (adresář) a na jednotlivé soubory.
