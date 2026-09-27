# Zvuky Sergeje

| soubor | lokomotiva | událost | zdroj |
|---|---|---|---|
| `zeleny_start.wav` | M62 Tamtam tajgy | rozjezd ze stanice a „zahoukej“ u nádražního směrování | Freesound 698211, alexdarek, CC0, úsek 0:27–0:42 |

Hra pouští při „zahoukej“ u nádražního směrování stejný zvuk jako při odjezdu ze stanice
(`PlayLeaveStationSound`), v GRF je to událost 1 callbacku 0x33.

Zpracování (ffmpeg z `imageio-ffmpeg`): mono 44,1 kHz 16 bit, horní propust 35 Hz,
kompresor (práh −24 dB, poměr 4, dorovnání +10 dB), +10 dB, limiter 0,95, náběh 50 ms a doznění 200 ms.
Výsledek: průměr −10,4 dB, špičky −0,4 dB.

`zdroje.txt` se přepisuje do `license.txt` vedle GRF (řádky `cs:` a `en:`).
