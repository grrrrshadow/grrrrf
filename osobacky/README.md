# Osobáčky: GRF malých aut, zatím TAZ 1203 plachta

Hráč 2. 10. (release `par9`, `zip8.zip`): *„uděláme grf osobáčky, skusime jako první 1203 plachta, je to taky test
buildu, grf musí být bez 4x spritů, jenom 8x použijem. uděláme orig size a zmenšený do jednoho grf. jsou tam fotky
taky.“*

| GRF | `grf_id` | auta | sprity |
|---|---|---|---|
| `grf/Osobacky-v1.grf` | `MAXh` | TAZ 1203 plachta (orig size, `0x0100`) a TAZ 1203 plachta zmenšená (`0x0101`) | jen 8× (`zin8`), 4× a menší si hra dopočítá |

GRF a licence jsou i v `Osobacky-v1.zip`. GRF má 384 kB (md5 `1bfb31a9e7478f5adafa23b4168da97c`).

## Auto

- **Model:** „Škoda 1203 ROL valník 1975“ od Jiřího Nováka, https://www.printables.com/model/1620425-skoda-1203-rol-valnik-1975 ,
  licence **CC0** (volné dílo, ověřeno přes API Printables). V releasu `par9` je jako `zip8/skoda-1203-valnik-1975.stl`
  (49 MB); do `model/` se jen kopíruje, v gitu není. Je to model pro 3D tisk: jeden kus bez barev, plachta je v něm,
  okna jsou otevřená a uvnitř jsou sedačky a volant. Fotky v `par9` (valníček, ROL s černou plachtou, Kladno
  s modrou plachtou) jsou předloha.
- **Rozměry:** podle rozvoru 2,40 m vychází délka 4,81 m, šířka 2,24 m se zrcátky a výška s plachtou 2,46 m.
- **Barvy jako stará TAZ 1203 plachta z VW T1** (dodávky): vybledle červená kabina a bočnice, hořčicová plachta,
  bílé disky s chromovou poklicí, černé nárazníky, zrcátka a stěrače, tmavý podvozek, kulatá světla s chromovým
  rámečkem, oranžové blinkry, tmavá maska.
- **Jak se barví:** barva se dává každé ploše modelu podle její polohy (kabina před zadní stěnou, plachta nad hranou
  bočnic, bočnice, podvozek pod korbou, kola podle vzdálenosti od osy kola, světla a maska na čele). Zrcátka jsou
  v modelu zvlášť, takže jdou poznat. Sklo je obal kabiny nad parapetem, o kousek zanořený (čelní, boční a rohy),
  proto okna nejsou průhledná do kabiny.
- **Údaje jako stará plachta** (`auta/NOVA-VERZE.md`): uvedení 1. 4. 1972 (rok zkoušky před výrobou v Trnavě od 1973),
  90 km/h, 50 k, 1,25 t, zvuk jako stará plachta. Náklady stejné jako TAZ 1203 plachta v dodávkách (121 kódů,
  `plachta_naklady.json`, výchozí pošta), překladová tabulka je hráčův vzor. Kapacita: pošta a zboží 4, sypké 2,
  lidé 2 (sedí v kabině, callback 0x15).

## Dvě velikosti v jednom GRF

- **orig size** jako dosavadní 1203 z VW T1 (rozvor 42,5 px ve 4×, tedy 17,71 px/m, v 8× 35,42 px/m). Auto má 7,56 osmin.
- **zmenšená** jako malá vejtřaska a malé RTO (CZTR, 12,2 px/m ve 4×, v 8× 24,4 px/m). Auto má 5,2 osmin.
- Obě jsou jeden díl 8/8, v koloně stojí po 8 jako malá vejtřaska. Kotvy a posun do pruhu silnice CZTR jsou stejné
  jako u vejtřasky.
- Jiné měřítko (třeba „zmenšená“ jako BRÝLE, 14,64 px/m) je jedno číslo při focení.

## Jen 8× (test buildu)

- Každý sprite je v GRF jen v 8× (`zin8`) a k tomu 1×1 paletová atrapa pro 8bpp blitter jako u ostatních GRF. 4× tam
  není žádné.
- Hra od forclaude `afed76d` udělá 4× z 8× průměrem každého bloku 2×2 váženým alfou (hráč: *„alfa vážené průměrování
  jen když nebude v grf dostupný 4x“*), menší úrovně výběrem pixelu.
- Posuny a rozměry 8× jsou sudá čísla, aby 4× vyšlo na celý pixel.

## Ve zkušební hře

- Zkušební hra z `51428e5` se `spritecache.cpp` z `afed76d` (`hra/README.md`), `testv3sfoto 1500 RT14 2 300`
  s `TEST_FOTO_SADA=osobacky`: obě velikosti s poštou, zbožím a lidmi a jednou s uhlím, jednou v 8× a jednou ve 4×.
- Hra načetla všech 18 spritů jen v 8× (výpis `ZIN8: sprite … zoom 6`, ani jeden „ma 8x i 4x“).
- **Pixelová kontrola** (`kontrola_pixel.py`):
  - v 8× sedí všech 14 aut na dvou fotkách na 100 % s posunem (0,0), jen u jednoho chybí 1 pixel pod jiným autem;
  - ve 4× skript zmenší sprite 8× stejně jako hra a porovná: 13 ze 14 aut na 100 %, jedno na 83 %, protože ho zčásti
    zakrývá původní náklaďák hry. Tím je ověřené i dopočítání 4× ve hře.
- Kapacity ve hře: pošta 4, zboží 4, lidé 2. Uhlí pod plachtu nejde, jako u staré plachty.
- Výřezy z fotek: `kontrola/hra_8x_v1.png` (8×) a `kontrola/hra_4x_v1.png` (4× dopočítané hrou).

## Jak to složit

1. `cp <par9>/zip8/skoda-1203-valnik-1975.stl model/`
2. `python3 render_1203.py 35.42 <fotky>/orig` a `python3 render_1203.py 24.4 <fotky>/zmensena` (každé asi minuta).
   `NAHLED=1` vyfotí čtyři pohledy s plochými barvami dílů na kontrolu barvení.
3. `python3 pack_1203.py <fotky> grf`, pak v `grf/`: `yagl -e Osobacky-v1.grf sprites`.
