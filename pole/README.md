# Pole marihuany a políčko brambor

Hráč 1. 10.:
- *„uděláme pole marihuany 4x5 a políčko brambor 3x3“*;
- *„vem si objekty kytek na to pole marihuany, obrázek nahradí marihuanovou plantáž“*;
- *„jo dobrý, to bude první fáze růstu na marihuanovým poli a druhá fáze udělej ty špičatý smrčky vysoký“*;
- *„jo to vypadá dobře ty brambory, to stačí tenhle jeden obrázek bez fází růstu“*.

Jsou to jen obrázky jako u gymnázia a automatu, do hry je zabuduje session hry ve forclaude. Skript
`render_pole.py` je postaví v Blenderu a vyfotí.

- **Kamera, měřítko a světlo jako gymnázium:** 12,2 px/m v přiblížení 4×, políčko 14,84 m, skutečná velikost.
- **Stín** na trávu je na 55 %.

## Marihuanová plantáž (5 × 4 políčka)

- **Místo plantáže hry:** plantáž je ve hře teď ovocná plantáž základní grafiky, která pěstuje marihuanu (forclaude,
  `SetupMarijuanaPlantation()` v `industry_cmd.cpp`). Má jediné rozložení: 5 políček k jihozápadu (x 0 až 4) a 4
  k jihovýchodu (y 0 až 3). Obrázek je přesně na ně.
- **Řady rostlin** stojí na záhonech podél x, mezi nimi jsou brázdy.
- **Polní cesta** vede uprostřed od severovýchodní hrany k jihozápadní. Na jejím severovýchodním konci je dřevěná
  kůlna s plechovou střechou a tři nádrže na vodu.
- **Dvě fáze růstu**, rostliny jsou v obou na stejných místech:
  1. `pole_marihuany_faze1_zin4.png`: košaté zakulacené keře 2,6 až 3,4 m, světle zelené, z keřů trčí velké dlanité
     listy;
  2. `pole_marihuany_faze2_zin4.png`: vysoké špičaté rostliny 3,8 až 5 m („smrčky“), tmavší zelená nákladu MARI jako
     u sochy, čtvrtina z nich štíhlá.
- **Rostliny jsou modely od sochy** (`rostliny/`).
  - V první fázi je to Cannabis Sativa plant se zkráceným vrškem (jako zaštípnuté konopí). Přes ni je mladá rostlinka
    Small Cannabis Plant, jejíž velké listy trčí z keře ven: podle nich se konopí pozná.
  - Ve druhé fázi je to Cannabis Sativa plant a Cannabis Plant, jak jsou.
  - Proč takhle: z dálky vypadaly původní rostliny jako smrčky, proto je první fáze přetvarovaná. Hráči se smrčky
    líbily na druhou fázi.

## Políčko brambor (3 × 3)

Je pro náklad BRAM (naše brambory), ve hře by to byl nový průmysl. Jeden obrázek bez fází.

- **Hřebeny** jsou po 0,75 m podél y. Na nich roste nízká zelená nať 0,4 až 0,5 m, část kvete bíle a fialově.
  Nať je vlastní model: trsy lístků jako hrbolaté kuličky.
- **Sklizený pruh:** jihozápadních 9 m jsou holé hřebeny s bramborami na zemi.
- **U jižního rohu** je kupa brambor, pytle na paletě (4, 3 a 2 na sobě) a tři stojící, k tomu bedny s bramborami.

## Pro hru

- **Rohy pozemku** jsou v JSONu (`rohy`). Severní roh je vždy na celém pixelu dělitelném 4. Dál JSON uvádí `policek`
  ([x, y]) a `obrazek` ([šířka, výška]).
- **Průhlednost:** pole je neprůhledné, jen úplně na kraji (25 cm od hran pozemku) je průhledno a je vidět tráva hry.
- **Nic nepřečuhuje** pod přední hrany ani do stran. Rostliny jsou celé uvnitř pozemku, jen nahoru můžou. Změřeno:
  mimo kosočtverec je jen pár pixelů okraje stínu s alfou nejvýš 8 z 255.
- **Políčko 256 × 128:** render 2 : 1 sedí na dlaždice hry, jak je (hra ho podle opravy 1. 10. večer nestahuje).

| soubor | co to je | obrázek | rohy: sever, východ, západ, jih |
|---|---|---|---|
| `pole_marihuany_faze1_zin4.png` | plantáž, první fáze (keře) | 1216 × 704 | (672, 96), (1184, 352), (32, 416), (544, 672) |
| `pole_marihuany_faze2_zin4.png` | plantáž, druhá fáze (smrčky) | 1216 × 704 | stejné |
| `pole_brambor_zin4.png` | políčko brambor | 832 × 512 | (416, 96), (800, 288), (32, 288), (416, 480) |
| `animace_ve_hre.gif` | obě pole ve fotce ze hry, plantáž střídá první a druhou fázi | | |

Složit znovu:
- `POLE=marihuana FAZE=1 python3 render_pole.py <výstup.png>`, druhá fáze `FAZE=2`;
- `POLE=brambory python3 render_pole.py <výstup.png>`.

Je to 128 vzorků, `SAMPLES=16` na zkoušku. Rostliny se nastavují proměnnými:
- první fáze: `RADA` a `ROZESTUP` (rozestup řad a rostlin), `VYSKA_OD` a `VYSKA_DO`, `KORUNA_OD` a `KORUNA`
  (poloměr keře), `SVETLA` a `TMAVA` (barvy), `MLADA_K` a `MLADA_S` (rostlinka s listy);
- druhá fáze: `VYSKA2_OD` a `VYSKA2_DO`, `KORUNA2`, `VYSOKYCH2`.

Náhled ve hře: `hra/nahled_ve_hre.py` s plantáží na `@41,13` a bramborami na `@47,13` (uvnitř okruhu), jednou
s první a jednou s druhou fází, a oba snímky do GIFu se společnou paletou.

## Skládací pole po dlaždicích (3. 10.)

Hráč: *„pole marihuana, brambor, budou modulární skládáná. základ je jedno políčko bez kytky, dlaždice se bude
opakovat. takhle první druhej a čtvrtej řádek pět stejných dlaždic a třetí řádek bude čtyři dlaždice cesty, opět
stejné dlaždice a pátá dlaždice bude bouda na konci cesty. tu boudu můžeš zas přiložit jako kytky … takhle bude mít
pole tři fáze, bez kytek, s malýma kytkama a se vzrostlými smrčky marihuany“*, *„budem přikládat holky na marihuanové
pole. když nepřijedou holky hodně dlouho tak tam nic neporoste“*, *„to samé bramborové pole, uplně stejný na menší
ploše, přikládat kytky. musime šetřit Mb“*. Holky na bramborové pole zatím ne.

Staré obrázky výš (celá plantáž 5 × 4 a brambory 3 × 3 v jednom kuse) byly jen ve 4×, v 8× je hra zvětšovala, proto
bylo listí rozmazané. Nové dlaždice jsou ve 4× i 8×.

**Každý obrázek je jedno políčko** se stejným rámem: ve 4× 264 × 200 px, rohy sever (132, 64), východ (260, 128),
západ (4, 128), jih (132, 192); v 8× 528 × 400 px a všechno dvakrát. Nad severním rohem je 64 px (4×) na rostliny.

| soubor (`dlazdice/…_zin4.png`, `…_zin8.png`, `.json`) | co to je |
|---|---|
| `mari_zaklad` | zem pole marihuany bez kytek: hlína, 4 záhony podél x |
| `bram_zaklad` | zem pole brambor bez natě: 20 hřebenů podél x |
| `cesta` | polní cesta podél x: ujetá hlína 9,8 m se dvěma pruhy kolejí, tráva po krajích 2,5 m |
| `mari_male` | přikládací: malé kytky (mladé rostliny 1,5 až 2,2 m) |
| `mari_vzrostle` | přikládací: vzrostlé smrčky 3,8 až 5 m (jako druhá fáze staré plantáže) |
| `bram_male`, `bram_vzrostle` | přikládací: mladá nať 0,2 až 0,27 m, vzrostlá nať 0,4 až 0,52 m, část kvete |
| `bouda` | přikládací: kůlna a tři nádrže na konci cesty (na dlaždici cesty, severovýchodní konec, dveře na cestu) |
| `holky_sz`, `holky_jv` | přikládací: dvě holky u severozápadního, nebo jihovýchodního okraje dlaždice cesty |

- **Zem** (`*_zaklad`, `cesta`) je neprůhledná přesně v kosočtverci políčka: pixel patří políčku, když v něm leží jeho
  střed. Sousední dlaždice se tak nepřekrývají a nemají mezi sebou díru.
- **Přikládací vrstvy** jsou jinde průhledné a nic z nich nepřečuhuje pod přední hrany políčka, jen nahoru. Kytky
  mají i svůj stín na zem (20 %).
- **Navazování:** záhony, hřebeny a cesta vedou podél x přes celé políčko, šum hlíny a trávy je z obrázku, který
  navazuje sám na sebe, a rostliny stojí v každém políčku na stejných místech. Opakované dlaždice tak nemají švy. Ve
  vrstvě kytek je i stín od rostlin sousedních políček.
- **Fáze:** 1 jen zem, 2 zem a `mari_male`, 3 zem a `mari_vzrostle` (brambory stejně).
- **Rozložení podle hráče:** plantáž 5 × 4, řádky y 0, 1 a 3 po pěti dlaždicích pole, řádek y 2 cesta: čtyři
  dlaždice cesty a na páté (na konci cesty, x 0) cesta s boudou. Brambory na náhledu 3 × 3: řádky y 0 a 2 pole,
  y 1 cesta s boudou na konci. Bouda a cesta jsou pro obě pole stejné.
- **Cesta jako překrývající dlaždice:** hráč: *„normálně tam bude tvoje nynější cesta a pod ní postavim silnici pro
  auta, proto potřebuju aby ta cesta v marihuanový plantáži byla overlaping, že tam je obrázek ale mužu pod obrázkem
  stavět“* a *„jedno poličko zaberou a druhé jen nakreslí ale zustane volné“*. Vzor je ISR/DWE-style Objects II
  (dirty, chujo, GPL v2): překrývající obrázek patří vedlejšímu políčku, je větší než dlaždice nebo posunutý a kreslí
  se jako placatá budova přes volné políčko, na kterém je silnice; auta a zastávka se kreslí nad ním. Obrázek cesty
  tedy přiloží hra k dlaždici pole vedle (zem pole je pod kytkami vždycky) posunutý o políčko přes řádek cesty.
  Zastávku si hráč postaví sám normálně na silnici.
- **Proč je cesta tak široká:** auta ve hře jezdí ve dvou pruzích čtvrt políčka od středu (3,7 m), ujetá cesta je
  proto 9,8 m široká a koleje jsou v pruzích. Holky (hráč: *„holky přikladej jen po stranách u kraje dlaždic cesty
  polem“*) stojí na trávě u kraje, ne v pruzích.
- **Velikost:** všechny dlaždice marihuany ve 4× mají dohromady asi 135 kB, v 8× asi 475 kB; brambory 140 a 455 kB.

Složit znovu: `POLE=marihuana python3 render_dlazdice.py <adresář>` (zem, cesta, bouda, kytky, holky) a
`POLE=brambory python3 render_dlazdice.py <adresář>`, 8× s `ZIN=8`; `JEN=mari_male,…` jen některé. Náhled celého
pole: `python3 slozit_pole.py <adresář dlaždic> 4 <výstup>` (`dlazdice/nahled/`).
