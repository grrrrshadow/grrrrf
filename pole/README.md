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
- **Políčko 256 × 128:** obrázky nejsou stažené, hra je stáhne na 124/128 jako gymnázium.

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
