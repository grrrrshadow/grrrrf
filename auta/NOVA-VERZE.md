# Nová verze VW T1, Škody 1203 a TAZ (30. 9.)

Vydáno hráči 30. 9. jako **`dodavky_BRYLE_v1.grf`** (grf_id `MAX\x08`, md5 `8ea92f1db2a1a9eeddd56856409989e4`).
Jméno v seznamu GRF ve hře zůstává zatím staré (hráč: „ve jménu GRF v seznamu GRF ve hře to zatím nech“).
Až budou auta hotová, zamkne se podle `hra/zamek-128-nakladu/ZPRAVA-OD-HRY.md`: zámek `decouple_128_cargo`
a hře jméno souboru a GRF ID. Další verze bude `dodavky_BRYLE_v2`.
Základ je poslední vydané `VWT1-S1203-clanky-oba-na-stred.grf`, rozbalené yaglem a upravené skriptem
`stavba_vwt1.py`.

## Co se změnilo

1. **Překladová tabulka:** za `FREE` je připsáno 125 kódů ze vzoru (`prekladova-tabulka-vzor.yagl`) v jeho
   pořadí, sloty 0x60–0xDC. Celkem 221 kódů. Hráčova čísla 0x00–0x5F zůstala.
2. **Náklady** podle hráče (níž).
3. **Nový valník 0x8A „TAZ 1203 valnik zelena marihuana“:** kupa brambor z valníku 0x88 přebarvená herní
   zelenou marihuany (paleta 0x52–0x57). Zelená je plná kupa i malá kupa při nakládání. Okno kabiny zůstalo
   červené. Ikona v nákupu je stejná jako u ostatních valníků. Skript `zelena_kupa.py`, náhled
   `nahled_zelena_kupa.png`.
4. **Čumák 2 + auto 8:**
   - čumák má `shorten_vehicle 0x06`, auto `0x00`;
   - článkovací switch vrací jen auto, zadní nárazník 0x00C0 se už nepřipojuje. Jeho definice zůstala kvůli
     rozehraným hrám.

   Rozestup v koloně zůstává 10. Pořadí kreslení je správně (`poradi_nova_verze.png`, níž).
5. **Skutečné údaje:** rok uvedení, výkon, max. rychlost a váha (níž).

## Náklady

- **VW T1 (obě velikosti):** hráčův seznam, vynechané zůstalo vynechané. Připsáno:
  - ovoce a zelenina, marihuana, víno, mouka (BAKE, FLOU), ústřice;
  - potravinářská aditiva, surový cukr, balíky, tiskoviny;
  - kovové a plastové díly, kůže (LEAT, LETH), plasty (PLAS, PLST), kaučuk, chemikálie;
  - dělníci a vězni (WORK, PRIS, YETI, YETY);
  - k tomu mléko, jedlý olej, sůl, kaolín, pálené vápno, soda, hnojivo, saze a stroje (hráč 30. 9.: „bod 1 jo,
    pod plachtu a do dodávky jde skoro všechno“).
- **Věci z bedny:** zboží, zemědělské, strojírenské a výrobní zásoby, hračky, baterie, železářské zboží, díly
  vozidel, strojní součásti a obaly.
- **Modrá dodávka a modrá dodávka zahrádka:** jako VW T1 bez věcí z bedny.
- **Dodávka bedna, plachta bedna, valník bedna:** jen věci z bedny.
- **Plachta a plachta šedá:** jako dodávka a navíc neznámé kódy (CRAN LFEQ SCPR STTP SWRP TIN_ WDCH).
- **Valníky podle barvy kupy:**
  - dřevo: WOOD, TWOD;
  - uhlí: COAL, COKE, MNO2;
  - jíl: CLAY, PEAT, BIOM, AORE, IORE, CORE, COCO;
  - písek: SAND, SULP, GRAI, WHEA, MAIZ, CERE;
  - kámen: GRVL, LIME, SLAG, SCMT, SCRP, NKOR, PORE, POTA, PHOS;
  - brambory: TATO, BEAN, CASS, SGBT;
  - zelený: MARI, HOPS.

  Všech 17 kódů sklápěčky Tatry vezou valníky, každý na tom s kupou své barvy.
- **Lidé:**
  - dodávky, valníky, plachty a VW T1: PASS, WORK, PRIS, YETI, YETY, 2 lidi;
  - bus (oba): PASS, TOUR, OTI1, OTI2, STUD, WORK, PRIS, YETI, YETY, PLAY, 8 lidí;
  - Pajda karavan: MARI (uvnitř, bez zelené), CIGR, TBCO, BEER, WINE a z lidí STUD a PASS, 5 lidí. PASS je tam,
    aby jezdil i bez GRF průmyslu se studenty.

Celé seznamy jsou v `vwt1-nova-souhrn.json`.

## Kapacita a výchozí náklad

- Oba díly mají v GRF kapacitu 1 a zapnutý nový výpočet kapacity (`miscellaneous_flags` 0x20). Kapacita tak
  nezávisí na výchozím nákladu:
  - sypké a většina nákladů 2, jako dřív;
  - zboží a pošta 4, dřív 5.
- **Lidé callbackem 0x15:** čumák 1, auto zbytek, tedy 2, 5 a 8.
- **Lidé na valníku** sedí v kabině, valník se ukazuje prázdný i při nakládání (skupina 0xFD, jen sada 0).
- **Výchozí náklad** (s ním se auto koupí a ukáže v nákupu), dřív byli všude cestující:
  - valníky: svůj náklad;
  - VW T1 a bedny: zboží;
  - modré dodávky a plachty: pošta;
  - bus a Pajda: cestující.
- **Nákup:** switch pro nákup zná článkovací callback 0x16, takže nákup ukazuje celé auto. Dřív ukazoval jen
  čumák, s kapacitou 1.

## Skutečné údaje

| auto | uvedení | výkon | max. rychlost | váha | zdroj |
|---|---|---|---|---|---|
| VW T1 | 8. 3. 1950 | 25 k, ve hře 30 k | 80 km/h | 975 kg, ve hře 1 t | Wikipedia (T1), automobile.at |
| Škoda 1203 Pajda karavan | 20. 11. 1968 | 110 k (lepší motor, hráč) | 130 km/h (hráč) | 1 170 kg | Škoda Storyboard |
| TAZ 1203 valníky a plachty | 1. 4. 1973 (Trnava) | 47 k (35 kW), ve hře 50 k | 90 km/h | 1 170 kg | Škoda Storyboard |
| TAZ 1500 bus a dodávky | 1988 (motor 1433 cm³) | 57 k (42 kW), ve hře 60 k | 110 km/h | 1 260 kg | Škoda Storyboard, Wikipedia |

- **Jednotky ve hře:** výkon jde jen po 10 k, váha po čtvrt tuně.
- **Rychlost nad 127 km/h** zapisuje vlastnost 0x15 (`speed_half_kmh`, jednotka 2 km/h): Pajda 0x41 = 130 km/h.
- **Hra se nemění.** Odpor vzduchu zůstává výchozí, hra ho počítá z max. rychlosti. Při realistickém zrychlení
  proto na rovině jedou nejvýš:
  - VW T1 71 km/h;
  - TAZ 1203 89 km/h;
  - TAZ 1500 101 km/h;
  - Pajda 130 km/h, díky lepšímu motoru i naložený.

## Jak to složit

```bash
mkdir z && cd z
cp ../VWT1-S1203-clanky-oba-na-stred.grf . && yagl -d VWT1-S1203-clanky-oba-na-stred.grf
python3 ../zelena_kupa.py sprites/VWT1-S1203-clanky-oba-na-stred.yagl \
    sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png 0x88 zelena.pkl
mkdir -p novy/sprites
python3 ../stavba_vwt1.py sprites/VWT1-S1203-clanky-oba-na-stred.yagl \
    sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png zelena.pkl ../vwt1_kody.json novy/sprites VWT1-zkouska
cp sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png novy/sprites/
cd novy && yagl -e VWT1-zkouska.grf sprites
```

Ověřeno 30. 9.:

- postup dal bajt po bajtu stejné GRF (md5 `8ea92f1db2a1a9eeddd56856409989e4`);
- zpětné rozbalení se shoduje se sestaveným yaglem, liší se jen poznámky a rozmístění spritů na listu;
- původní GRF po rozbalení a novém složení vyjde beze změny.

## Zkouška ve hře (zkušební kopie hry, beze změn hry)

- **`testv3s`** (koupě a přestavby) na všech kupovatelných autech:
  - čumák má délku 2, auto 8, zadní nárazník už není;
  - lidé 1 + 1, 1 + 4 a 1 + 7;
  - zboží a pošta 2 + 2, ostatní 1 + 1;
  - lidé na valníku: prázdný obrázek;
  - uhlí, brambory, marihuana i chmel: plný obrázek, u zeleného valníku sprite se zelenou kupou;
  - bedna: bedna na korbě.

  Že nákup ukazuje celé auto, plyne z kódu hry (`GetNextArticulatedPart` volá callback 0x16 v nákupu). Zkouška
  to přímo neměří.
- **`testpruhy`** (osa X, stojící dvojice proti sobě, čela 0–14/16 dlaždice od sebe), `poradi_nova_verze.png`:
  1. bus proti plachtě šedé;
  2. Tatra 148 proti plachtě šedé;
  3. plachta proti Tatře.

  Nahoře je ve všech 24 dvojicích auto v předním pruhu, stejně jako u zkušebního čumáku 2 + auto 8 v CUMAK.md.

## Otevřené

- VW T1 a TAZ 1500 jedou při realistickém zrychlení pod skutečnou max. rychlostí. Silnější motor jako u Pajdy?
- Zámek a přesun k základní grafice hry, až budou auta hotová.
- Auta koupená v rozehrané hře před výměnou GRF si nechají zadní nárazník. Nově koupená už ho nemají.
