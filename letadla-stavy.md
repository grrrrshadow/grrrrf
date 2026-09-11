# Letadla: jak poznat, v jaké je fázi letu

Ověřeno **ve zdrojácích hry** (`forclaude/openttd/src/`, jen čteno, nic
neměněno) a na skutečném setu `kaas_planes.grf`. 2026-09-11.

## Tři proměnné, které to řeší

| var | co vrací | kde v kódu |
|---|---|---|
| **`0xE2`** | **fáze pohybu** — hlavní věc | `MapAircraftMovementState()` |
| **`0xE6`** | akce pohybu — pozná **nakládání** | `MapAircraftMovementAction()` |
| **`0xB4`** | aktuální rychlost | `newgrf_engine.cpp`, `case 0x34` |
| `0x44` | výška nad stínem + typ letiště | „Aircraft info“ |

V kódu jsou to `case 0x62` a `case 0x66` uvnitř `switch (variable - 0x80)`,
takže skutečná čísla jsou **0xE2** a **0xE6**. `kaas_planes` používá
`0xE2` 18×, `0xB4` 3× a `0xE6` vůbec.

## Tabulka var 0xE2 — fáze pohybu

Sloupec *vrací* říká, jestli tu hodnotu OpenTTD vůbec kdy vrátí. Deset
hodnot z TTDPatche je mrtvých — **nemá smysl na ně větvit.**

| hod. | název | česky | fáze | vrací |
|---|---|---|---|---|
| 0 | `HANGAR` | v hangáru (dojel na místo) | hangár | **ano** |
| 1 | `TO_HANGAR` | pojíždí do hangáru | taxi | **ano** |
| 2 | `TO_PAD1` | stojí na stání 1 | terminál | **ano** |
| 3 | `TO_PAD2` | stojí na stání 2 | terminál | **ano** |
| 4 | `TO_PAD3` | stojí na stání 3 a výš | terminál | **ano** |
| 5 | `TO_ENTRY_2_AND_3` | — | — | ne |
| 6 | `TO_ENTRY_2_AND_3_AND_H` | pojíždí k stání 2/3+ | taxi | **ano** |
| 7 | `TO_JUNCTION` | pojíždí ke stání 1 / po ploše | taxi | **ano** |
| 8 | `LEAVE_RUNWAY` | — | — | ne |
| 9 | `TO_INWAY` | sjel z dráhy, pojíždí k terminálu | taxi | **ano** |
| 10 | `TO_RUNWAY` | — | — | ne |
| 11 | `TO_OUTWAY` | pojíždí na start dráhy | taxi | **ano** |
| 12 | `WAITING` | — | — | ne |
| 13 | `TAKEOFF` | rozjezd po dráze (vzlet) | VZLET | **ano** |
| 14 | `TO_TAKEOFF` | — | — | ne |
| 15 | `CLIMBING` | stoupání po odlepení | LET | **ano** |
| 16 | `FLIGHT_APPROACH` | let ve vyčkávacím okruhu nad letištěm | LET | **ano** |
| 17 | `UNUSED_0x11` | — | — | ne |
| 18 | `FLIGHT_TO_TOWER` | let na trati | LET | **ano** |
| 19 | `UNUSED_0x13` | — | — | ne |
| 20 | `FLIGHT_FINAL` | — | — | ne |
| 21 | `FLIGHT_DESCENT` | klesání na přistání (ve vzduchu) | PŘISTÁNÍ VZDUCH | **ano** |
| 22 | `BRAKING` | brzdí po dosednutí na dráze | PŘISTÁNÍ DRÁHA | **ano** |
| 23 | `HELI_TAKEOFF_AIRPORT` | vrtulník stoupá z letiště | heli | **ano** |
| 24 | `HELI_TO_TAKEOFF_AIRPORT` | — | — | ne |
| 25 | `HELI_LAND_AIRPORT` | vrtulník klesá na letiště | heli | **ano** |
| 26 | `HELI_TAKEOFF_HELIPORT` | vrtulník stoupá z heliportu | heli | **ano** |
| 27 | `HELI_TO_TAKEOFF_HELIPORT` | — | — | ne |
| 28 | `HELI_LAND_HELIPORT` | vrtulník klesá na heliport | heli | **ano** |

## Tvoje fáze → hodnoty 0xE2

| co chceš rozlišit | hodnoty |
|---|---|
| taxi po letišti | **1, 6, 7, 9, 11** |
| vzlet na dráze (rozjezd) | **13** |
| let (stoupání / trať / okruh) | **15, 16, 18** |
| přistání ve vzduchu (klesání) | **21** |
| přistání na dráze (brzdění) | **22** |
| stojí na terminálu | **2, 3, 4** |
| v hangáru | **0** |
| vrtulník | 23, 25, 26, 28 |

Pozor na dvě místa, kde by se dalo splést:

- **`13 TAKEOFF` je rozjezd po dráze**, ne „chce vzlétnout“. Pojíždění
  na start dráhy je `11 TO_OUTWAY`.
- **`22 BRAKING` je brzdění na dráze po dosednutí.** Jakmile sjede
  z dráhy, přepne na `9 TO_INWAY` — to je zpátky taxi.

## Nakládání: na tohle 0xE2 nestačí

`0xE2` u stojícího letadla vrátí `2/3/4` bez ohledu na to, jestli
zrovna nakládá, nebo jen stojí. Rozdíl zná jen **`0xE6`**, protože
se v kódu ptá na `current_order.IsType(OT_LOADING)`:

| hod. | název | česky |
|---|---|---|
| 0 | `IN_HANGAR` | stojí v hangáru |
| 1 | `ON_PAD1` | NAKLÁDÁ na stání 1 |
| 2 | `ON_PAD2` | NAKLÁDÁ na stání 2 |
| 3 | `ON_PAD3` | NAKLÁDÁ na stání 3+ |
| 4 | `HANGAR_TO_PAD1` | z hangáru na stání 1 |
| 5 | `HANGAR_TO_PAD2` | z hangáru na stání 2 |
| 6 | `HANGAR_TO_PAD3` | z hangáru na stání 3+ |
| 7 | `LANDING_TO_PAD1` | na stání 1, ale NEnakládá |
| 8 | `LANDING_TO_PAD2` | na stání 2, ale NEnakládá |
| 9 | `LANDING_TO_PAD3` | na stání 3+, ale NEnakládá |
| 10 | `PAD1_TO_HANGAR` | ze stání 1 do hangáru |
| 11 | `PAD2_TO_HANGAR` | ze stání 2 do hangáru |
| 12 | `PAD3_TO_HANGAR` | ze stání 3+ do hangáru |
| 13 | `PAD1_TO_TAKEOFF` | ze stání na vzlet |
| 14 | `PAD2_TO_TAKEOFF` | (hra nevrací) |
| 15 | `PAD3_TO_TAKEOFF` | (hra nevrací) |
| 16 | `HANGAR_TO_TAKEOFF` | (hra nevrací) |
| 17 | `LANDING_TO_HANGAR` | dojíždí do hangáru |
| 18 | `IN_FLIGHT` | letí |

Čili: **nakládá/vykládá ⟺ `0xE6` je 1, 2 nebo 3.** Jinak jen stojí.

## Jak to dělá kaas_planes

Rozebráno přímo z jeho GRF. Používá `0xE2` s maskou `0xFF` a větví
takhle (nejčastější vzor):

```
  0 .. 14   -> sada A   (na zemi: hangár, taxi, rozjezd)
  15        -> sada B   (stoupání)
  16,18,20  -> sada C   (let)
  21        -> sada D   (klesání)
```

Prakticky je to podvozek venku/zataženo. **Větev na `20 FLIGHT_FINAL`
je zbytečná** — OpenTTD tu hodnotu nikdy nevrátí. Totéž jeho větve na
`24` a `27` u vrtulníků.

Rychlost řeší zvlášť: `0xB4` maskuje na 16 bitů, násobí `0x3939`,
dělí `0x1000` (operátory `0A` = násobení, `06` = dělení) a pak větví
jedním prahem — u jednoho letadla na 60, u jiného na 90. Takže
**každý typ může mít práh vlastní.**

## Úhly a směry

Hra vybírá sprite jako `směr + základ` (`Aircraft::GetImage`), kde
směr je `Direction` z `direction_type.h`:

```
  0 N    1 NE    2 E    3 SE    4 S    5 SW    6 W    7 NW
```

Takže osm spritů musí jít v tomhle pořadí. **Pro auta i letadla
stejně** — je to společný `Direction`, ne něco zvlášť pro letadla.

K úhlům v `glb3BBC.py`: seznam pro auta je
`[0, 315, 270, 225, 180, 135, 90, 45]`, aktivní je
`[225, 180, 135, 90, 45, 0, 315, 270]`. Spočítáno: **je to tentýž
seznam, jen posunutý o 3 pozice (135°)**, krok je u obou −45°.
Pořadí směrů je tedy shodné, liší se jen o kolik je model v GLB
natočený. Devátý úhel navíc je sprite do depa.

Z toho plyne: **u nového modelu se neladí pořadí, jen počáteční
posun.** Vyrenderovat, podívat se, který obrázek je čelní pohled,
a seznam o tolik pozic pootočit.
