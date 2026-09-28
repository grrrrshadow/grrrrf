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

---

## 4. Marihuana u vozidel ze sad, která ji mají jménem (2026-09-28)

Hráč: *„vejtřaska nejde přestavět na marihuanu“*. Praga V3S (`v3s/`, GRF `MAXd` a `MAXe`) má
`MARI` v seznamu vždy povolených nákladů (vlastnost 24, `always_refittable_cargos`) jménem,
přes překladovou tabulku. Hra ji ale škrtne v `OfferMarijuanaToShipsAndAircraft()`
(`newgrf.cpp`, na vaší větvi `claude/github-connection-check-m6m898`):

```cpp
for (Engine *e : Engine::Iterate()) {
	if (e->GetDefaultCargoType() != marijuana) e->info.refit_mask.Reset(marijuana);
}
```

Komentář u ní říká *„no set's vehicle knows the cargo by name“*, jenže tahle už ano (a VW T1
a dvanácettrojky taky, mají `MARI` v tabulce). Pravidlo má zjevně chránit před uhelnými auty,
která berou náklad podle **třídy** (komentář cituje hráče: *„the lorries for marijuana are there,
the coal ones need not carry it“*). U V3S hráč marihuanu chce: *„hlavně ty napiš vejtřasce MARI“*,
*„to má fungovat ty kódy“*, *„MARI je ve hře zabudovaný“*. Ověřeno na vaší větvi v commitu
`18fb946` (28. 9. 12:27). Návrh: nechat marihuanu vozidlům, která ji mají v seznamu
**jménem**. `_gted` v tu chvíli ještě žije (volá se před `_gted.clear()` v `AfterLoadGRFs`):

```cpp
for (Engine *e : Engine::Iterate()) {
	if (e->GetDefaultCargoType() == marijuana) continue;
	if (_gted[e->index].ctt_include_mask.Test(marijuana)) continue;   // sada ji chce jménem
	e->info.refit_mask.Reset(marijuana);
}
```

U článkových aut (velká V3S má neviditelný čumák a auto jako druhý díl) mají oba díly stejný
seznam, takže podmínka projde u obou.

Grafiku pro to už máme: naložená V3S vozí zelenou kupičku, jakmile ji hra na `MARI` přestavět
nechá. Konopná vlákna (`FICR`) hra neškrtá, ta V3S vozí už teď.

### Plantáž: MARI i FICR, V3S obojí (hráč 28. 9.)

Hráč: *„napiš mu, že bude používat FICR i to druhý, co používá u plantáže marihuany, a ty budeš
taky používat obojí“*. Plantáž dává dva náklady: `MARI` (marihuana) a `FICR` (`CT_HEMP_FIBRE`,
„Konopná vlákna“). Jiný kód na vlákna hra nemá. Hráč chce, aby V3S vozila **obojí**:

- `FICR` vozí už dnes, hra ho neškrtá.
- `MARI` jí hra škrtá, viz návrh výš (nechat marihuanu vozidlům, která ji mají v seznamu jménem).

(`OLSD` jsou olejniny a vozy na `OLSD` zůstanou na olejniny. Hráč: *„OLSD budou na OLSD, to je olej“*.
Moje dřívější úvaha dát vláknům `OLSD` kvůli vagonům CZTR tím padá.)
