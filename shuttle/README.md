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
| Action01 | jedna sada, 8 spritů, `zin4` 32bpp |
| Action02 | základní skupina spritů |
| Action00 | vlastnosti letadla, instance `0x0029` |
| Action04 | jméno „Shuttle" |
| Action03 | napojení grafiky na letadlo |

Vlastnosti: 480 mph, 80 cestujících, 20 pošty, **od roku 2042**,
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

## Co zatím NENÍ hotové

- **Žádné rozlišení fáze letu.** Sprity jsou pořád stejné, ať letadlo
  taxíruje, stoupá nebo klesá. Na to je proměnná `0xE2` — popsáno
  v `../letadla-stavy.md`.
- **Žádný stín ani vrtule.**
- `grf_id: "GRSH"` jsem si vymyslel. Na ostrou verzi si vyber vlastní,
  ať se to nepere s cizím GRF.
- **Ve hře zatím jen načtené.** Hráč potvrdil, že GRF je v seznamu
  grafik zeleně a bez chyby. Jestli je letadlo v depu vidět a jak
  vypadá za letu, se teprve ukáže.
