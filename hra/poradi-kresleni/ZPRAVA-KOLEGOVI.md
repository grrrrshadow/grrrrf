# Pro kolegu ze hry: auta na silnici SV–JZ se kreslí přes sebe

Od session GRF a spritů (`grrrrshadow/grrrrf`), 29. 9. večer. Hráč poslal fotky ze hry, požádal mě, ať to
prozkoumám v kódu, a tuhle zprávu ti nese on. Ve forclaude jsem nic neměnil, jen četl tvou větev
`claude/github-connection-check-m6m898` (9d23ceb).

## Co hráč vidí

Na silnici **SV–JZ** (osa X) se auto, které jede **na jihozápad v zadním pruhu**, při míjení kreslí **přes**
auto v předním pruhu, které jede na severovýchod. Na silnici SZ–JV (osa Y) se to neděje.

- Nejvíc to dělají dvanácttrojky a VW T1 z poslední verze GRF VW T1, `VWT1-S1203-clanky-oba-na-stred.grf`. Tam je
  každé auto souprava nárazník + auto + nárazník a **každý díl má délku 1** (`shorten_vehicle 0x07`, všech 37 dílů).
- Stejně ale přes ně leze i Tatra (délka 8), když jede na jihozápad a míjí dvanácttrojku (`hrac_snimek2_tatra.png`).
- Není to zarovnáním spritů. Dvanácttrojka na hráčově fotce 3 jede ve svém pruhu daleko od středu a přesto je nahoře
  (`hrac_snimek3_1203.png`).

## Proč

`RoadVehicle::UpdateDeltaXY()` (`roadveh_cmd.cpp`) dělá třídicí krabici dílu tak dlouhou, jak dlouhý je díl
(`gcache.cached_veh_length`), a posadí ji k jeho čelu. GRF VW T1 ale kreslí celé auto, asi 7 jednotek (1/16 dlaždice),
na díl dlouhý 1. Krabice auta je tedy dlouhá 1 a zbytek obrázku za ní visí. Ze zkoušky (`PRUHY: … box`): dvanácttrojka
`0x00B3` má krabici x 1085..1085, Tatra vedle ní 1073..1080.

Když se dvě auta míjejí na silnici podél X:

- auto v zadním pruhu (na jihozápad) je dál po ose x;
- auto v předním pruhu (na severovýchod) je dál po ose y.

Každé je tak „za“ tím druhým v jiné ose. `ViewportSortParentSprites` pro takovou dvojici nemá pravidlo, obě nechá
v pořadí, v jakém je hra přidala, a jihozápadní vyjde nahoře. Na silnici podél Y leží krabice míjejících se aut tak,
že zadní je za předním v obou osách, proto tam chyba není.

**Rola to není.** Zvednutí krabice (`CARRIED_BOX_LIFT`) platí jen pro auto na vagonu. `ViewportSortParentSprites` je
u tebe stejné jako ve vanilce a `UpdateDeltaXY()` se liší jen tím zvednutím.

## Ověřeno ve zkušební hře

Zkoušel jsem ve své zkušební kopii hry (60283b3). Třídění i `UpdateDeltaXY()` jsou tam stejné jako u tebe, kromě
zvednutí na vagonu. Scéna `testpruhy`: stojící auta proti sobě na třech rovných silnicích, po osmi dvojicích
s čely od sebe 0 až 14/16 dlaždice (celé míjení), a k tomu zácpa v obou pruzích. Výsledek je v `pred_po.png`:

1. **SV–JZ dnes:** ve všech míjeních 2–8/16 je nahoře zadní pruh.
2. **SV–JZ s opravou 1:** nahoře je vždy přední pruh.
3. **SZ–JV:** dnes i s opravou správně, beze změny.
4. a 5. **Zácpa v obou pruzích na SV–JZ:** dnes leze zadní pruh přes přední, s opravou ne.

## Oprava 1: krabice jako celé auto

Každý díl třídit krabicí celého auta (`VEHICLE_LENGTH`), ať je díl dlouhý jakkoli.

- **Obrázek se nehne.** Origin + offset vychází pro každou délku stejně (−2), mění se jen krabice, podle které se řadí.
- **Rolu to neovlivní.** `road_on_rail.cpp` krabici nečte (bere `ROAD_VEHICLE_NOSE` a délky dílů) a zvednutí na vagonu
  zůstává, jak je.
- **Kolony se nerozbijí.** Díly jedné soupravy se překrývají jako u vozidla délky 8, pořadí rozhodne součet souřadnic
  a vepředu je vždy ten blíž k divákovi.

## Oprava 2: posun obrázku z vagonu se nevynuluje

`Vehicle::draw_offs` nastavuje `road_on_rail.cpp` autu na vagonu každý tik. Když auto vystoupí (`TryLeaveTrain`,
`TryLeaveVessel` → `PlaceRoadVehicleAtStopEntrance`), nikdo ho nevynuluje, takže auto jezdí dál po silnici
s posunutým obrázkem.

- Při výchozí palubě (`_carried_z_offset` 4·ZOOM_BASE) a boku 0 je posun nula.
- Po `testpaluba` nebo `testbok` ale posun autu, které se vezlo, zůstane, dokud znovu nenastoupí.
- Na silnici se auto jinudy nevrací, ostatní místa ho mažou. Stačí proto vynulovat v `PlaceRoadVehicleAtStopEntrance`
  u čela i u přívěsů.

Na hráčových fotkách to podle mě není, ta dělá oprava 1. Je to ale chyba a hráč chce, ať ji víš.

## Patch

Soubor `oprava-poradi-kresleni.patch` vedle téhle zprávy (v `grrrrshadow/grrrrf`, `hra/poradi-kresleni/`). Obsahuje
obě opravy, mění jen `roadveh_cmd.cpp` a je udělaný proti tvé větvi na 9d23ceb (`patch -p1` v kořeni repa).
Tvou větev jsem s ním celou přeložil bez chyby a hra naběhla a odjela 500 tiků nové hry (bez obrazu).

Pusť prosím i svou baterii (`tests/rig`), ať je vidět, že se jinde nic nepohnulo. Já jsem zkoušel jen silnici
a zácpu, ne zastávky, mosty a Rolu.

## Dodatek 30. 9.

Hráč vyzkoušel čistou vanilku: dvanácttrojky a Tatry dělají totéž, CZTR truck ne. Je to tedy chování samotného
OpenTTD s naším GRF, ne tvé větve. Oprava jde udělat v GRF: dvanácttrojka s čumákem délky 2 a autem délky 8
(bez zadního nárazníku) se kreslí správně i ve vanilce (`clanky_srovnani.png`). Oprava 1 ve hře proto nutná není,
pomohla by jen sadám, které dělají totéž co my. Oprava 2 (`draw_offs` po vystoupení z vagonu) platí dál.
