# shuttle.grf

Zkušební letadlo pro OpenTTD. Sprity vyrenderované z `glbobj/Shuttle.glb`
skriptem `glb/GLB/glb3letadlo.py`, GRF složený nástrojem `yagl`.

```
shuttle/
├── shuttle.grf                        ← hotový GRF, do OpenTTD
├── sprites/
│   ├── shuttle.yagl                   ← zdroj
│   └── shuttle-32bpp-zin4-0.png       ← spritesheet, 8 směrů
└── README.md
```

**Jméno drží pohromadě na třech místech**, jak má: soubor `shuttle.grf`,
skript `shuttle.yagl` a `name: "shuttle";` v Action08. Tak se to najde
v seznamu GRF ve hře.

## Přeložit znovu

```bash
cd shuttle
../yagl/yagl-main/build/yagl -e shuttle.grf sprites
```

## Co v něm je

| záznam | co dělá |
|---|---|
| Action08 | `grf_id: "GRSH"`, GRF8, jméno a popis |
| Action01 | **tři sady po 8 spritech**, `zin4` 32bpp |
| Action02 | tři základní skupiny + **přepínač na `0xE2`** |
| Action00 | vlastnosti letadla, instance `0x0029` |
| Action04 | jméno „Shuttle" |
| Action03 | napojení grafiky na letadlo |

Vlastnosti: 320 mph, 80 cestujících, 20 pošty, **od roku 2042**,
neomezený dolet, všechna klimata.

## !!! climate_availability !!!

**`climate_availability: null;` znamená ŽÁDNÉ klima, ne „všechna".**
Vozidlo se pak nikdy neobjeví v nákupním menu a hra na to nijak
neupozorní — GRF svítí v seznamu zeleně, bez chyby. Rozhoduje o tom
jediný řádek v `newgrf.cpp`:

```cpp
if (!e->info.climates.Test(_settings_game.game_creation.landscape)) continue;
```

Správně se to píše výčtem: `Temperate | Arctic | Tropical | Toyland`.

## Fáze letu

Tři sady spritů, přepíná se podle `0xE2`:

```
0x0F  = 15  CLIMBING        -> stoupani, cumak nahoru  (HILL_TILT -12)
0x15  = 21  FLIGHT_DESCENT  -> klesani,  cumak dolu    (HILL_TILT +12)
ostatni                     -> rovne                   (HILL_TILT   0)
```

Rovná sada slouží i pro vodorovný let (16, 18) — letadlo v něm opravdu
rovné je — a pro všechno na zemi.

## Co zatím NENÍ hotové

- **Žádný stín ani vrtule.**
- `grf_id: "GRSH"` jsem si vymyslel. Na ostrou verzi si vyber vlastní,
  ať se to nepere s cizím GRF.
- **Ve hře ověřeno (2026-09-12).** Letadlo je v depu, zvedá čumák při
  vzletu ve vzduchu a má ho lehce dolů při klesání na přistání.

## Poznámka k rychlosti

`speed_8_mph: 0x28` je 320 mph. Původně tu bylo `0x3C` (480 mph) a
snížení vzniklo z chybné diagnózy — myslel jsem si, že fáze stoupání
při vyšší rychlosti probleskne příliš rychle. **Není to pravda**, fáze
jsou vidět i při 480. Vrátit se dá jedním řádkem.
