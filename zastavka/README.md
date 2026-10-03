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
- **Velikost: 2×, jako budovy** (hráč: *„vemem tu větší variantu holky“*). Je skoro tak vysoká jako střecha
  přístřešku; 1,5× je v ukázkách pro srovnání.

**Druhá dívka jen u silnice podél X** (hráč: *„podél X se vejde do jižního rohu dlaždice druhá, jiná holka, zády
otočená. Podél Y asi ne, naproti na zastávku se nevejde“*, *„úplně do rohu“*):

| silnice | bod | čelem k | posun od severního rohu, 4× | 1× | kreslit po |
|---|---|---|---|---|---|
| podél X | x 15, y 15 (jižní roh, blízký okraj) | silnici, k severozápadu (260 st), k divákovi zády | (0, 120) | (0, 30) | blízkém přístřešku `X_E` |

- **Originál:** stojí na konci blízkého přístřešku před sloupkem. **CZTR:** na konci chodníku, přístřešek je až
  na druhém konci.
- **Která:** jen tmavovlasá dívka v tmavé sukni (College Girl), hráč: *„jen tmavovlasá“*. Zezadu je na světlém
  chodníku vidět, bělovlasá (Galaxia) na něm skoro splývá (`druha_divka_srovnani.png`).
- Slabý stín u nohou může přesáhnout přední hranu dlaždice o pár pixelů.

## Rozhodnuto (hráč 1. 10.)

- **Dívky jsou na zastávce, jen když tam čekají cestující** (*„jo bude tam jen když budou cestující“*).
- **Velikost 2×** (*„vemem tu verzi 2x velkou“*). Stejně velké budou i dívky u aut (*„stejnou velikost dáme
  k autům, aby to ladilo se zastávkou“*), viz `holky-u-aut/`.
- **Podél Y je jen jedna** (*„na Y není místo naproti, to je škoda“*).
- Podél X tedy dvě: dívka v tyrkysovém tílku na vzdáleném okraji a tmavovlasá zády v jižním rohu.

## Soubory

| soubor | co to je |
|---|---|
| `vysledek_2x.png` | **výsledek:** obě zastávky s dívkami ve 2×, podél X dvě (druhá tmavovlasá v jižním rohu zády), podél Y jedna |
| `zastavky_4x.png` | obě zastávky (originál OpenGFX a CZTR), silnice podél X i Y, ze hry v přiblížení 4× |
| `zastavky_mrizka.png` | totéž zvětšené 2× s mřížkou dlaždice po 2/16 a rohy N, W, E, S |
| `divka_na_zastavce_k1.5.png`, `divka_na_zastavce_k2.png` | ukázka: dívka vložená na místo do obou zastávek, 1,5× a 2× |
| `divky_na_zastavce_k1.5.png`, `divky_na_zastavce_k2.png` | obě dívky: podél X dvě, podél Y jedna |
| `druha_divka_srovnani.png` | druhá dívka v jižním rohu: bělovlasá a tmavovlasá vedle sebe |
| `divka2_co_k*_s260.png`, `divka2_ga_k*_s260.png` (+ `.json`) | druhá dívka sama zády (College Girl, Galaxia), ruce podél těla |
| `divka_k*_s90.png`, `divka_k*_s0.png` (+ `.json`) | dívka sama (Character People Girl 001, stojí), čelem k jihovýchodu a k jihozápadu, 160 × 160 px, 4×, chodidla přesně uprostřed |
| `divka_k2_s90_zin8.png`, `divka_k2_s0_zin8.png`, `divka2_co_k2_s260_zin8.png` (+ `.json`) | tytéž tři dívky, které hra používá, v přiblížení 8× (jen naše hra, `zin8`): 320 × 320 px, 24,4 px/m, 1024 vzorků, chodidla přesně uprostřed (160, 160), přesně dvojnásobek 4× |

Fotky zastávek: zkušební hra s příkazem `testzastavky` (`hra/zkusebni-prikazy-c53e895.patch`), mapa `-G 11`,
OpenGFX, jednou bez GRF a jednou s celou sadou CZTR silnic (z releasu `par3`), výška země 8. Fotka dívky:
`postavy/fotka_postavy.py` (`POSTAVA`, `POZA`, `SMER`, `MERITKO`), kamera a světlo jako u budov.

## Přiblížení 8× a ruce (2. 10.)

Hráč: *„uděláme 8× holky čekající na zastávce, 4× jim zůstane a přidáme 8×“*. Tři dívky, které hra kreslí (podél X
tyrkysová `divka_k2_s90` a tmavovlasá zády `divka2_co_k2_s260`, podél Y `divka_k2_s0`), jsou vyfocené znovu
`postavy/fotka_postavy.py` s `PX_M=24.4 RAM=320 SAMPLES=1024`: stejná kamera, dvojnásobné rozlišení, obrázek 8× je
přesně dvojnásobek 4× i s chodidly uprostřed. Tmavovlasá College Girl má zároveň ve 4× i 8× ruce (dřív je otočení
ramen o 76° schovalo do trupu, teď 50°, `postavy/README.md`), `divka2_co_k2_s260.png` je proto znovu.

## Matylda na blízkém chodníku podél Y (3. 10.)

Hráč: *„matylda je na zastávku kde holka chybí směr jihovýchod asi? tam dame matyldu a původní zastávka ji schová,
se nic neskazí“*, pak k náhledu *„jo přesně tak jsem ji chtěl, ať vyhlíží : )“*.

- **Kde chyběla:** u silnice podél Y (severozápad–jihovýchod) byla jen jedna dívka, na vzdáleném okraji. Na blízkém
  okraji by ji originální přístřešek zakryl. Hráč chce, ať tam stojí: v originále ji přístřešek schová, na CZTR je
  vidět.
- **Matylda** (Matilda od nicolekeane, Sketchfab, release par10 `zip9/matilda.glb`, v `postavy/par10/`): holka
  z filmu Leon s mikádem, v hnědé bundě a s kytkou v květináči. **Licence CC BY-NC-SA 4.0:** nekomerčně (jako
  Buran) a obrázky s ní musí mít stejnou licenci a jméno autorky (`AUTORI-MODELU.md`).
- **Vyhlíží autobus:** stojí na kraji chodníku u silnice a kouká podél silnice k severozápadu (směr 270 st.), kytka
  v květináči je z pohledu hráče vidět. Velikost 2× jako ostatní dívky (skutečná výška 1,6 m), slabý stín jako na
  zastávce.

| silnice | bod (šestnáctiny) | čelem k | posun od severního rohu, 4× | 1× | 8× | kreslit |
|---|---|---|---|---|---|---|
| podél Y | x 13,4, y 5 (blízký okraj, kraj chodníku u silnice) | podél silnice k severozápadu (270 st.) | (−67,2, 73,6) | (−16,8, 18,4) | (−134,4, 147,2) | jako podřízený obrázek **vzdáleného** přístřešku `Y_E`, tedy před blízkým `Y_W` |

- **Originál:** blízký přístřešek `Y_W` se kreslí až po ní, jeho zadní stěna, lavička a střecha ji zakryjí. Jak moc
  přesně, ukáže až hra.
- **CZTR:** blízký skleněný přístřešek je u jižního rohu, Matylda stojí v severozápadní části na volném chodníku
  (`matylda_na_zastavce_cztr.png`). Chodník je součást obrázku `Y_W` a kreslí se po ní, může jí překrýt podrážky
  o pixel.
- **Podél Y jsou teď dvě:** vzdálená v tyrkysovém tílku (`divka_k2_s0`) a Matylda.

| soubor | co to je |
|---|---|
| `divka3_ma_k2_s270.png` (+ `.json`) | Matylda ve 4×, 160 × 160 px, chodidla přesně uprostřed (80, 80) |
| `divka3_ma_k2_s270_zin8.png` (+ `.json`) | totéž v 8× (jen naše hra, `zin8`), 320 × 320 px, chodidla (160, 160), přesně dvojnásobek 4× |
| `matylda_na_zastavce_cztr.png` | náhled: Matylda vložená do zastávky CZTR podél Y (z `vysledek_2x.png`, 2× zvětšené) |

Fotka: `POSTAVA=par10/matilda VYSKA=1.6 SMER=270 STIN=0.2 SAMPLES=256 python3 ../postavy/fotka_postavy.py
divka3_ma_k2_s270.png`, 8× s `PX_M=24.4 RAM=320 SAMPLES=1024`.

