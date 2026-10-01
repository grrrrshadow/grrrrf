# Dívka na zastávce: místo pro originál i CZTR

Hráč 1. 10.: *„ukaž CZTR zastávku pro cestující a originál zastávku hry. Já je vedle sebe neuvidím ve hře, protože
CZTR nahradí originál. Jde o to, jestli najdem místo, kam tu holku postavit, aby to fungovalo na CZTR i originál
zastávce“*, *„zálivovou dělat nebudem“*. Tady se to promýšlí, do hry to dá kolega ve forclaude.

## Co na zastávce je

- **Průjezdná autobusová zastávka** má ve hře dva přístřešky v pásech u okrajů dlaždice: u silnice podél X
  v pásu y 0–3 (severozápadní okraj, od diváka za silnicí) a y 13–16 (jihovýchodní, blíž k divákovi), u silnice
  podél Y v pásu x 0–3 (severovýchodní, vzdálený) a x 13–16 (jihozápadní, blízký). Každý přístřešek je jeden obrázek
  s ohraničením 16 × 3 × 16 (hra: `table/station_land.h`, `_station_display_datas_0170` a `0171`, obrázky
  `SPR_BUS_STOP_DT_X_W/E` a `Y_W/E`). Silnice je mezi pásy.
- **Originál (OpenGFX):** v obou pásech přístřešek přes celou délku dlaždice, lavička vzadu, otevřený k silnici.
- **CZTR (CZTR Road set 2.3.1):** ty čtyři obrázky přepisuje (Action 5, RoadStops 0–3) a přepisuje i zálivové
  zastávky (Action A, obrázky 2692–2723). V každém pásu je chodník a skleněný přístřešek jen na jednom konci:
  na vzdáleném okraji u silnice podél X na západním konci (x 12–16), u silnice podél Y na severním (y 0–4).
  **CZTR přístřešky jsou jen 32bpp v přiblížení 4×**, v 8bpp jsou prázdné (1 × 1 px).

## Kam dívku postavit

**Na vzdálený okraj (od diváka za silnicí), do části, kde CZTR nemá přístřešek:**

| silnice | bod (šestnáctiny dlaždice) | čelem k | posun od severního rohu dlaždice, 4× | 1× |
|---|---|---|---|---|
| podél X (SV–JZ) | x 6,5, y 2,2 | silnici, k jihovýchodu | (−34,4, 34,8) | (−8,6, 8,7) |
| podél Y (SZ–JV) | x 2,2, y 11 | silnici, k jihozápadu | (70,4, 52,8) | (17,6, 13,2) |

- **Originál:** stojí pod střechou před lavičkou. **CZTR:** stojí na volném chodníku vedle skleněného přístřešku.
- **Blízký okraj nejde:** originální přístřešek je tam k divákovi zády, zadní stěna a lavička by ji zakryly.
- **Jak kreslit:** jako podřízený obrázek (child sprite) vzdáleného přístřešku, tedy `X_W` u silnice podél X
  a `Y_E` u silnice podél Y. Oba mají počátek ohraničení v severním rohu dlaždice, odtud jsou posuny v tabulce.
  Hra ji pak nakreslí hned po přístřešku, ať je originální nebo z CZTR. Je vždycky před ním a nemá vlastní
  ohraničení, které by se hádalo s přístřeškem nebo s autobusy.
- **Velikost:** 1,5× (budovy jsou 2×) sedí k přístřeškům i autobusům. Ve 2× je skoro tak vysoká jako střecha.

**Druhá dívka jen u silnice podél X** (hráč: *„podél X se vejde do jižního rohu dlaždice druhá, jiná holka, zády
otočená. Podél Y asi ne, naproti na zastávku se nevejde“*, *„úplně do rohu“*):

| silnice | bod | čelem k | posun od severního rohu, 4× | 1× | kreslit po |
|---|---|---|---|---|---|
| podél X | x 15, y 15 (jižní roh, blízký okraj) | silnici, k severozápadu (260 st), k divákovi zády | (0, 120) | (0, 30) | blízkém přístřešku `X_E` |

- **Originál:** stojí na konci blízkého přístřešku před sloupkem. **CZTR:** na konci chodníku, přístřešek je až
  na druhém konci.
- **Která:** tmavovlasá dívka v tmavé sukni (College Girl) je zezadu na světlém chodníku vidět. Bělovlasá
  (Galaxia) na něm skoro splývá (`druha_divka_srovnani.png`).
- Slabý stín u nohou může přesáhnout přední hranu dlaždice o pár pixelů.

## Soubory

| soubor | co to je |
|---|---|
| `zastavky_4x.png` | obě zastávky (originál OpenGFX a CZTR), silnice podél X i Y, ze hry v přiblížení 4× |
| `zastavky_mrizka.png` | totéž zvětšené 2× s mřížkou dlaždice po 2/16 a rohy N, W, E, S |
| `divka_na_zastavce_k1.5.png`, `divka_na_zastavce_k2.png` | ukázka: dívka vložená na místo do obou zastávek, 1,5× a 2× |
| `divky_na_zastavce_k1.5.png`, `divky_na_zastavce_k2.png` | obě dívky: podél X dvě, podél Y jedna |
| `druha_divka_srovnani.png` | druhá dívka v jižním rohu: bělovlasá a tmavovlasá vedle sebe |
| `divka2_co_k*_s260.png`, `divka2_ga_k*_s260.png` (+ `.json`) | druhá dívka sama zády (College Girl, Galaxia), ruce podél těla |
| `divka_k*_s90.png`, `divka_k*_s0.png` (+ `.json`) | dívka sama (Character People Girl 001, stojí), čelem k jihovýchodu a k jihozápadu, 160 × 160 px, 4×, chodidla přesně uprostřed |

Fotky zastávek: zkušební hra s příkazem `testzastavky` (`hra/zkusebni-prikazy-c53e895.patch`), mapa `-G 11`,
OpenGFX, jednou bez GRF a jednou s celou sadou CZTR silnic (z releasu `par3`), výška země 8. Fotka dívky:
`postavy/fotka_postavy.py` (`POSTAVA`, `POZA`, `SMER`, `MERITKO`), kamera a světlo jako u budov.
