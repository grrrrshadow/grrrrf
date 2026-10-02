# Sergej: M62 jako vlastní GRF

Tři lokomotivy M62 v jednom GRF, ve dvou velikostech, každý sprite v přiblížení 4× i 8×:

| GRF | `grf_id` | měřítko | délka | kolej |
|---|---|---|---|---|
| `grf/orig/M62_Sergej-v7.grf` | `MAXb` | jako CZTR, 12,2 px/m (zin4), 24,4 px/m (zin8) | 12/8 (2 + 8 + 2) | na koleje CZTR |
| `grf/bryle/M62_Sergej_BRYLE-v7.grf` | `MAXc` | o 20 % větší, 14,64 px/m (zin4), 29,28 px/m (zin8) | 14/8 (3 + 8 + 3) | na původní koleje hry |

Obě mají `track_type 0`, tedy štítek `RAIL`. Na něm jezdí i lokomotivy a vagony CZTR (v jejich
převodní tabulce je `RAIL` na indexu 1) a všechny koleje CZTR Rails (RA01–RA13, ELRL, ER01–08)
mají `RAIL` mezi kompatibilními a napájenými. Takže jezdí obě všude, liší se velikostí.

## Jméno a popis v seznamu GRF

Hráč: *„červeně uděláme M62 Sergej a zbytek zeleně for ottd Decouple by Karel Macha“* (verze 6),
*„brýle má svoji barvu a cztr měřítko má svoji barvu“*. Na konci symbol vláčku v barvě varianty,
jako u hráčových sad (CZTR Truck set BRYLE, VW T1, m62 v `par5`).

    {red}M62 Sergej{green} for ottd Decouple by Karel Macha {gold}{train}       (měřítko CZTR)
    {red}M62 Sergej{green} for ottd Decouple by Karel Macha {lt-blue}{train}    (BRÝLE)

BRÝLE má `{lt-blue}` jako „Magnificated“ v truck setu, měřítko CZTR `{gold}` jako symboly ve VW T1
(to je v měřítku CZTR). Stejnou barvu má ve variantě i řádek s popisem velikosti a symboly v popisu.

Popis (Action08) jde v hráčově pořadí: `{red}M62 Sergej{green}  {train}`, zelený řádek se symboly,
řádek varianty v její barvě, `{orange}` informace (lokomotivy, 3D model, zvuky) a nakonec zeleně
`ottd decouple by Karel Mácha`, odkaz na itch a licence.

Soubory se jmenují `M62_Sergej-v7.grf` a `M62_Sergej_BRYLE-v7.grf`, aby šly v seznamu najít podle jména.
Číslo verze (hráč: *„piš tam verzi do jména souboru grf“*) je `VERZE` v `pack_sergej.py`, stejné
číslo jde do Action14 (`VRSN`) a hra ho ukáže v okně GRF. Každé sestavení pro hráče o jedna výš:
1 první sprity, 2 sever o 3 px, 3 přezdívky a licence, 4 troubení, 5 motor podle rychlosti a barevné
jméno, 6 jméno „M62 Sergej“ červeně a zbytek zeleně, 7 třetí lokomotiva Maša РЖД a všechno v 4× i 8×. `MINV` je 1,
takže nová verze smí v uložené hře nahradit kteroukoli starší.

## Lokomotivy

| | id | nátěr | uvedení |
|---|---|---|---|
| M62 Tamtam tajgy | 0x0100 (+ články 0x0101, 0x0102) | původní zelený | 1965 |
| Sergej ČSD | 0x0110 (+ články 0x0111, 0x0112) | ČSD červená, žlutý pruh kus pod čelním oknem | 1966 |
| Maša РЖД | 0x0120 (+ články 0x0121, 0x0122) | červeno-šedý РЖД s logem, textury z modelu Leafia dev. (par8) | 2003 (vznik РЖД, 1. 10. 2003) |

Parametry všech: 100 km/h, 1971 hp (1470 kW), 116 t, tažná síla 0x4F, trakce diesel, provoz
jako diesel (0x4C36), cena a provoz jako CZTR 775 se stejným výkonem, k dispozici do konce hry.
Popis v nákupním okně je callback 0x23 (texty D001 až D003), znění podle hráče; u Maši azbukou РЖД a Маша
(hráč 2. 10.: *„červenej je rusko azbukou ržd, to bude maša. do popisu k nákupu azbukou ržd a maša azbukou“*).
Maša má zvuky zelené (motor bez tlumiče).

## Jak to vzniklo

1. **Model**: `diesel_locomotive_m62.glb` v `model/` je od v7 z releasu `par8` (týž model jako v `par5`, jen
   textury 2048 px místo 1024, kvůli 8×). Autor je podle metadat glb **Chicken cutlet**
   (sketchfab.com/Chicken_Cutlet), „Diesel locomotive M62“, licence **CC BY 4.0**, takže musí být uvedený.
   (renderatnight dělal VW T1, ne tohle.) K němu `model/rzd_telo.png`, `rzd_zaluzie.png` a `rzd_spojka.png`:
   obrázky 1, 2 a 6 z `teplovoz-m62.glb` (par8, „Teplovoz-m62 РЖД“, **Leafia dev.**, sketchfab.com/Leaf_dev,
   CC BY 4.0). Ten model má stejné rozložení textur jako model od Chicken cutlet, ale hrubší síť, neprůhledná okna
   a vpředu vlevo pomačkaný plech; hráč: *„radši texturu z červenýho na zelenej, protože zelenej vypadá
   detailnější s okny“*. Oba glb z par8 se zkopírují do `model/` (adresář není v gitu) a `python3 vytahni_rzd.py`
   z `teplovoz-m62.glb` udělá ty tři png.
2. **Nátěr** (`nater.py`): červená verze přebarví textury `Image_0`, `Image_6`, `Image_8` z modelu.
   Zelený lak jde na ČSD červenou se zachováním stínů a špíny, krémové linky boků a sovětské pruhy na
   čele na červenou, žlutý pruh na řádky 918–934 textury čela (textura je vzhůru nohama; souřadnice jsou pro
   1024 px, u 2048 px se dělí měřítkem). Barvy doladěné tak, aby na fotce vyšla červená a žlutá brejlovce z CZTR
   dieselsetu (132, 31, 31 a 154, 123, 20), vyšlo 130, 37, 33 a 151, 118, 32 a o krok dál.
   Nátěr РЖД (`nater.rzd`) vymění `Image_0`, `Image_8` a `Image_2` za textury Leafia dev. a v překryvu
   `Image_6` (vrstva s průhledností, má zelené kusy těla) dá zeleným pixelům barvu těla РЖД ze stejného místa.
3. **Focení** (`render_sergej.py`): z hráčova `glb3BBC.py` z 24. 1. 2026, stejná kamera, HDRI a Cycles.
   `python3 render_sergej.py <zeleny|cerveny|rzd> <px_na_m> <osmin> <výstup>`; s `ZIN=8` fotí 8×
   (dvojnásobné px/m i rám 640 px) do adresáře `<výstup>_zin8`. `SMERY=1,8` vyfotí jen dané směry (zkoušky).
4. **Balení** (`pack_sergej.py`): `python3 pack_sergej.py <orig|bryle> <adresář fotek> grf/<orig|bryle>`,
   pak v `grf/<varianta>` spustit `yagl -e M62_Sergej-v7.grf` (nebo `M62_Sergej_BRYLE-v7.grf`).
   Chce fotky 4× (`<orig|bryle>_<nátěr>`) i 8× (`…_zin8`) všech tří nátěrů.
   Zvuky bere ze `zvuky/` (`zvuky.json`), připravuje je `zvuky/priprav_zvuky.py`, viz `zvuky/README.md`.
5. **Kontroly** na rozbaleném GRF (`yagl -d`), poslední argument 4 nebo 8 je zoom:
   - `kontrola_koleje.py` ho postaví na koleje v 8 směrech (obrázky v `kontrola/`, zvlášť 4× a 8×);
   - `kontrola_spoju.py` ověří, že kusy na rovné koleji dají přesně původní fotku (4× i 8×);
   - `kontrola_pixel.py` porovná fotku ze zkušební hry (`hra/README.md`, příkaz `testvlakfoto`, výpis `V3SDIL`)
     s rozbaleným GRF: každý článek položí tam, kam ho kreslí hra, a spočítá přesně shodné pixely (4× i 8×);
   - `kontrola_zvuku.py` projde callback 0x33 tik po tiku (stání, rozjezd, brzdění) a ověří
     troubení, pásma podle rychlosti a že kousky motoru jdou přesně po sobě.

## Zoom 8× (zin8)

Od verze 7 má každý sprite dva řádky: `zin4` a `zin8` (kód zoomu 6, jen naše hra; hráč: *„budem dávat oboje do
grf“*). Obrázek 8× je přesně dvojnásobek obrázku 4×: fotka 8× (`ZIN=8`, rám 640 px, dvojnásobné px/m) se ořízne
dvojnásobným rámečkem obrázku 4× a posuny jsou dvojnásobné, balič si to u každého spritu ověří. Na rovné koleji se
fotka 8× dělí na články podle téže mapy jako 4× (zvětšené 2×), takže kusy 8× jsou přesně 2× kusy 4×; pixely
siluety 8× mimo dvojnásobný rámeček 4× balič spočítá (`pixelu 8x mimo ramecek 4x`), bývá jich pár na okraji.
Prázdné směry (hlava a záď na šikmé koleji) mají jen `zin4` 1×1. Hra 8× ukáže, když je v nastavení přiblížení 8×
(`gui.zoom_min 0`); v jiné hře (bez zin8) se řádek přeskočí a 4× se zvětší jako dřív.

## Verze 7 ve hře (2. 10. 2026)

- **Zkušební hra** z `51428e5` (`hra/README.md`, třetí hra) s novým příkazem `testvlakfoto`: tři rovné koleje
  podél osy X, na každé jedna lokomotiva (zelená, ČSD, Maša), osm fotek v 8× (`gui.zoom_min 0`) a osm ve 4×.
- **Pixelová kontrola** (`kontrola_pixel.py`): v obou přiblíženích sedí všech 9 článků (3 lokomotivy × hlava, střed,
  záď, směr JZ) na 100 % přesně s posunem (0,0). Výřezy z fotek: `kontrola/hra_8x_v7.png`, `kontrola/hra_4x_v7.png`.
  Výpis hry `ZIN8: ReadSprite … ma 8x i 4x` potvrzuje, že bere oba řádky a 8× je přesně dvojnásobné.
- **Spoje a koleje** (`kontrola_spoju.py`, `kontrola_koleje.py`) 4× i 8× u obou velikostí: spoje v pořádku (rozdíl
  nejvýš 1 ze zaokrouhlení), obrázky `kontrola/koleje_orig*.png`, `kontrola/koleje_bryle*.png`.
- **GRF:** `grf/orig/M62_Sergej-v7.grf` 10,8 MB (md5 `95241f0c9565c6002b0ab23a5772972b`),
  `grf/bryle/M62_Sergej_BRYLE-v7.grf` 12,2 MB (md5 `a6db68db41e3d5b525c997028c2f27ea`); v každém 75 obrázkových
  spritů (51 se zin4 i zin8, 24 prázdných jen zin4) a 54 zvuků, listy `-32bpp-zin4.png` a `-32bpp-zin8.png`.
  Oba GRF a licence jsou i v `M62_Sergej-v7.zip`.
- Maša РЖД má uvedení 1. 10. 2003 (vznik РЖД); kdo hraje dřív, ji v nákupu neuvidí. Zkušební hra ji na fotku
  zpřístupnila bez ohledu na datum.

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

## Zvuky

Podrobně v `zvuky/README.md`. Stručně:

- Troubí obě stejnou trumpetkou (alexdarek), při odjezdu, na „zahoukej“ u nádražního směrování
  a v tunelu.
- Motor hraje celou cestu. Každé 3 s (112 tiků) pustí další kousek podle rychlosti vlaku. Je šest
  pásem od 15 do 100 km/h a s rychlostí rostou otáčky, rytmus i řev: zelená −10 → −7 LUFS,
  ve stání volnoběh.
- Na plné rychlosti hraje tak nahlas jako nejhlasitější zvuk CZTR diesel setu, jenže pořád.
- Sergej ČSD má motor přes tlumič: hlubší a o 1,5 LU tišší.
- Porucha a ostatní události nechají výchozí zvuk hry.

Kopie wav v `grf/*/sprites/` do gitu nejdou (jsou v GRF i v `zvuky/`).
