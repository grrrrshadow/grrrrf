# Pro kolegu, co dělá hru

Tohle je vzkaz z druhé strany, od grafiky a GRF. Děláme sady
silničních vozidel, CZTR truck set a sadu Škoda / TAZ / VW, a narazili
jsme na tři věci, které z GRF ovlivnit nejdou. Všechny tři jsou
v `src/roadveh_cmd.cpp`. Čísla níž jsou z aktuálního masteru, na
vaší větvi to prosím ověřte.

---

## 1. Odstup v koloně. Tohle je ta nejdůležitější.

```cpp
static constexpr DirectionIndexArray<int8_t> dist_x{-4, -8, -4, -1, 4, 8, 4, 1};
static constexpr DirectionIndexArray<int8_t> dist_y{-4, -1, 4, 8, 4, 1, -4, -8};
```

Ve `FindClosestBlockingRoadVeh`. Auto zastaví, když by se jeho střed
dostal blíž než **8 jednotek** ke středu auta před ním. `cached_veh_length`
se v té funkci nevyskytuje vůbec, takže na délce vozidla to nezávisí.

Dlaždice má 16 jednotek, takže auta v koloně stojí vždycky přesně půl
dlaždice od sebe. A protože plná délka vozidla je taky 8, auto na plnou
délku stojí přesně na doraz, mezera je nulová.

**Co by pomohlo:** kdyby ten odstup šel ovlivnit, ideálně z NewGRF,
třeba vlastností vozidla nebo aspoň herním nastavením. Dnes se to dá
obejít jenom tím, že se z každého auta udělá článkovaná souprava
s neviditelnými nárazníky. Funguje to, ale je to drahé (viz níž).

---

## 2. Jemnost délky vozidla

```cpp
uint length = VEHICLE_LENGTH;                          // 8
length -= Clamp(veh_len, 0, VEHICLE_LENGTH - 1);       // veh_len = shorten_vehicle
```

V `GetRoadVehLength`. Délka je celý počet osmin dlaždice, 1 až 8.

Z toho plyne, že **nejmenší možný díl je osmina dlaždice** a že rozestupy
se dají stavět jen po krocích 12,5 %. Hráč chtěl 20 % a to mezi ty kroky
nepadne, nejblíž je 12,5 % a 25 %.

**Co by pomohlo:** kdyby se počítalo po šestnáctinách, kroky by byly po
6,25 %. Chtělo by to ale i dohodu, jak se ten bajt v GRF čte, dneska je
po osminách.

---

## 3. Klikací box

`RoadVehicle::UpdateDeltaXY`. Podél jízdy je rozměr `cached_veh_length`,
napříč silnicí 3 a na výšku 6, a ty dvě jsou natvrdo.

Klikací box je tedy přesně délka vozidla. To je spojené s bodem 1:
jakmile se kvůli rozestupu zkrátí viditelné auto, zmenší se i box,
kterým se dá do auta trefit myší.

---

## Co jsme zatím udělali a co to stojí

Z každého auta je článkovaná souprava s neviditelnými nárazníky.
Rozestup mezi dvěma auty vychází na `délka auta + 8 + délka čumáku`,
protože díly soupravy se pouštějí z depa po délce toho **předního**
a blokuje kterýkoliv díl cizí soupravy.

| sestava čumák, auto, ocas | rozestup | proti 8 | klikací box auta |
|---|---|---|---|
| bez nárazníků | 8 | 0 % | 8 |
| 1, 8 | 9 | +12,5 % | 8 |
| 1, 1, 1 | 10 | +25,0 % | **1** |
| 1, 2, 1 | 11 | +37,5 % | 2 |

Daň je vidět v posledním sloupci. A ještě jedna, která nás překvapila:
**článek se připojuje jedině při koupi**, volá se to v
`CmdBuildRoadVehicle` a nikde jinde. Auta, která už ve hře jezdí, ho
nedostanou, takže po změně GRF je potřeba koupit nová.

---

## Co je a co není v GRF

Kompletní seznam vlastností silničních vozidel v
`src/newgrf/newgrf_act0_roadvehs.cpp` jde po 0x2A a **žádná z nich se
odstupu ani klikacího boxu netýká**. Proto to nejde vyřešit u nás.

Když by k něčemu z toho vznikla nová vlastnost nebo callback, rádi to
z GRF strany nasadíme a otestujeme na obou sadách.

---

## Pozor: naše silniční vozidla už nejsou jednodílná

Tohle je důležité pro cokoliv, co s autem na silnici manipuluje, tedy
i pro nakládání aut na vlak. Kvůli rozestupům je z **každého
kupovaného auta článkovaná souprava**:

| sada | kupovaných | dílů na soupravu |
|---|---|---|
| Škoda / TAZ / VW | 18 | 2 nebo 3 |
| CZTR truck set | 26 | 2, u 11 z nich 3 (mají přívěs) |

Sestava je `neviditelný nárazník vepředu`, `viditelné auto`, volitelně
`neviditelný nárazník vzadu`. Nárazníky mají osminu dlaždice a kreslí
se jako prázdný sprit.

Z toho plyne pár věcí, které můžou překvapit:

1. **Kupované číslo je ten neviditelný nárazník**, ne auto. Drží jméno,
   cenu i ikonu v nákupu. Viditelné auto je až druhý díl.
2. **Kapacita je rozdělená mezi díly.** U dvanácettrojek nese nárazník
   jednu jednotku a auto zbytek, protože motor s nulovou kapacitou
   přijde o nabídku nákladů. Součet sedí na původní hodnotu.
3. **Grafika podle druhu nákladu sedí na viditelném dílu**, ne na
   kupovaném čísle. U CZTR je takových mapování 129.
4. Kdo bere auto ze silnice, musí vzít **celou soupravu**, ne jeden
   `Vehicle`. Viditelné auto samo o sobě je jen prostřední díl.

Jestli by vám to u nakládání překáželo, dá se to z naší strany
přestavět, jen to chce vědět dopředu, jakou podobu potřebujete.
