# Sergej: M62 jako vlastní GRF

Dvě lokomotivy M62 v jednom GRF, ve dvou velikostech:

| GRF | `grf_id` | měřítko | délka | kolej |
|---|---|---|---|---|
| `grf/orig/Sergej_M62.grf` | `MAXb` | jako CZTR, 12,2 px/m (zin4) | 12/8 (2 + 8 + 2) | na koleje CZTR |
| `grf/bryle/Sergej_M62_BRYLE.grf` | `MAXc` | o 20 % větší, 14,64 px/m | 14/8 (3 + 8 + 3) | na původní koleje hry |

Obě mají `track_type 0`, tedy štítek `RAIL`. Na něm jezdí i lokomotivy a vagony CZTR (v jejich
převodní tabulce je `RAIL` na indexu 1) a všechny koleje CZTR Rails (RA01–RA13, ELRL, ER01–08)
mají `RAIL` mezi kompatibilními a napájenými. Takže jezdí obě všude, liší se velikostí.

## Lokomotivy

| | id | nátěr | uvedení |
|---|---|---|---|
| M62 Tamtam tajgy | 0x0100 (+ články 0x0101, 0x0102) | původní zelený | 1965 |
| Sergej ČSD | 0x0110 (+ články 0x0111, 0x0112) | ČSD červená, žlutý pruh kus pod čelním oknem | 1966 |

Parametry obou: 100 km/h, 1971 hp (1470 kW), 116 t, tažná síla 0x4F, trakce diesel, provoz
jako diesel (0x4C36), cena a provoz jako CZTR 775 se stejným výkonem, k dispozici do konce hry.
Popis v nákupním okně je callback 0x23 (texty D001 a D002), znění podle hráče.

## Jak to vzniklo

1. **Model**: `diesel_locomotive_m62.glb` z releasu `par5` (autor renderatnight), zkopírovat do `model/`.
2. **Nátěr** (`nater.py`): červená verze přebarví textury `Image_0`, `Image_6`, `Image_8` z modelu.
   Zelený lak jde na ČSD červenou se zachováním stínů a špíny, krémové linky boků a sovětské pruhy na
   čele na červenou, žlutý pruh na řádky 918–934 textury čela (textura je vzhůru nohama).
   Barvy doladěné tak, aby na fotce vyšla červená a žlutá brejlovce z CZTR dieselsetu
   (132, 31, 31 a 154, 123, 20), vyšlo 130, 37, 33 a 151, 118, 32 a o krok dál.
3. **Focení** (`render_sergej.py`): z hráčova `glb3BBC.py` z 24. 1. 2026, stejná kamera, HDRI a Cycles.
   `python3 render_sergej.py <zeleny|cerveny> <px_na_m> <osmin> <výstup>`
4. **Balení** (`pack_sergej.py`): `python3 pack_sergej.py <orig|bryle> <adresář fotek> grf/<orig|bryle>`,
   pak v `grf/<varianta>` spustit `yagl -e Sergej_M62.grf` (nebo `Sergej_M62_BRYLE.grf`).
5. **Kontroly**: `kontrola_koleje.py` postaví rozbalený GRF na koleje v 8 směrech (obrázky v
   `kontrola/`), `kontrola_spoju.py` ověří, že kusy na rovné koleji dají přesně původní fotku.

## Co je na tom podstatné

- **Rovná a šikmá kolej mají jiné měřítko.** Hra na rovné koleji (směry 1, 3, 5, 7) posune vozidlo
  o osminu o 8 px (zin4), na šikmé (0, 2, 4, 6) o 16 px. Lokomotiva se proto na rovné koleji fotí
  podélně stlačená 1/√2. CZTR dělá totéž (u 770 vychází asi 0,68).
- **Tři články jako CZTR 770.** Na šikmé koleji kreslí celou lokomotivu prostřední článek, hlava a záď
  mají prázdný sprite. Na rovné si každý kreslí svůj kus. Který pixel patří kterému článku, určuje
  druhý průchod renderu, kde je model obarvený podle vzdálenosti od středu.
- **Kotva spritu není poloha vozidla.** Hra kreslí sprite na `RemapCoords(poloha + bounds.origin +
  bounds.offset)` z `Train::UpdateDeltaXY`. Pro prostřední článek je to 8 px nad polohou na šikmé
  koleji a (±16, −16) px na rovné, pro krátké články jinak. Posuny se počítají v `hra.py`
  tak, aby bod na koleji pod středem článku padl přesně na polohu článku.
- **Odstupy článků** jsou `L_a / 2 + (L_b + 1) / 2` (`CalcNextVehicleOffset`): u 2 + 8 + 2 je hlava
  5 osmin před středem a záď 5 za ním, u 3 + 8 + 3 hlava 5 a záď 6.
