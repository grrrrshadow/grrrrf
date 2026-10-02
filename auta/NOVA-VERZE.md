# Nová verze VW T1, Škody 1203 a TAZ (30. 9.)

| verze | soubor | md5 | co přinesla |
|---|---|---|---|
| 1 | `dodavky_BRYLE_v1.grf` | `8ea92f1db2a1a9eeddd56856409989e4` | náklady, zelený valník, čumák 2 + auto 8, skutečné údaje |
| 2 | `dodavky_BRYLE_v2.grf` | `012303618c0e34e225621d9c6ce62343` | TAZ 1203 bus a dodávky, čumák 1 (menší mezera v koloně) |
| 3 | `dodavky_BRYLE_v3.grf` | `aa348bbae9aaf135405355cb8e882dc5` | roky: prototyp na zkoušku rok před výrobou, zahrádky TAZ 1203 od 1981 |
| 4 | `dodavky_BRYLE_v4.grf` | `56d1797382f742dbf43831627bbf53c6` | fialová TAZ 1900 D dodávka s naftovým motorem VW |
| 5 | `dodavky_BRYLE_v5.grf` | `94b3f4ea2dec56f6c3132ffa383ee780` | holky u otevřených dveří busů a Pajdy na zastávce, kód BRAM, autoři 3D v popisu |
| 6 | `dodavky_BRYLE_v6.grf` | `4571e1e71efd6c0fc4fe25cc6c4e3f81` | kovy pod plachtou, odpad na valníku s kamennou kupou |
| 7 | `dodavky_BRYLE_v7.grf` | `2e602ee7273fb785eb94ae106940b9c5` | holky u dveří i v přiblížení 8× naší hry (`zin8`), 1024 vzorků |
| 8 | `dodavky_BRYLE_v8.grf` | `6891ebf5cce0495b83f0da8dc86d5e9e` | holky u dveří jen v 8×, ve směru na severovýchod o kousek výš (chyběla bota) |

- grf_id `MAX\x08`, jméno v seznamu GRF ve hře zůstává zatím staré (hráč: „ve jménu GRF v seznamu GRF ve hře to
  zatím nech“).
- Až budou auta hotová, zamkne se podle `hra/zamek-128-nakladu/ZPRAVA-OD-HRY.md`: zámek `decouple_128_cargo` a hře
  jméno souboru a GRF ID. Další verze bude `dodavky_BRYLE_v9`.
- Základ je poslední vydané `VWT1-S1203-clanky-oba-na-stred.grf`, rozbalené yaglem a upravené skriptem
  `stavba_vwt1.py`.

## Verze 8 (2. 10.): holky jen v 8×, směr na severovýchod výš

Hráč k v7 (hrál ji v 8×, v nastavení hry musel přepnout 4× na 8×):
- *„zbytečný dávat do GRF obrázky 4× a 8×, to nemusíš, jenom 8× stačí“*;
- *„severovýchodní směr zvednem holku trochu vejš, protože jí chybí bota. Levá bota není vidět, ale pravá bota je
  vidět, tak nevím, čím to je“*.

- **Holky mají v GRF jen `zin8`.** Ve 4× si hra obrázek udělá z 8× sama (vynechá každý druhý pixel), je o něco hrubší
  než vlastní fotka 4× ve v7, v 8× je to stejné. GRF je tím jen pro naši hru: jiná hra řádek `zin8` přeskočí a sprite
  nemá nic.
- **Čím to je:** chodník zastávky CZTR je sprite s vlastní krabicí blíž k divákovi než auto, hra ho kreslí až po
  autě (holky jsou vrstvy auta) a překryje, co z holek leží na něm: boty. Levá bota ležela celá na chodníku, pravá
  stála na jeho hraně. Změřeno ve zkušební hře pixel po pixelu (`holky-u-aut/bota.png`): holce u kufru hra schovala
  až 8 px (8×). Ve směru 3 holku u kufru zakrývá prosklený přístřešek, to je jiná věc a zůstává.
- **Směr 1 (na severovýchod):** holka B u kufru o 6 px (4×) výš, holka A u předních dveří o 8 px výš (stojí o 0,3
  jednotky hlouběji v chodníku, podle téže hrany by přišla o 10 px; s 11 px ale koukala hlavou nad střechu
  přístřešku CZTR, tak jen 8, špičky bot tam může ztratit, v tomhle směru je stejně pod přístřeškem). Ostatní směry
  beze změny. Ověřeno ve hře: holce B zůstaly obě boty celé.
- Hráč: *„radši změním originál zastávku než holky“* (původní zastávka hry holky u bližšího pruhu schová přístřeškem),
  to je na straně hry.
- Složení jako v7, jen `dodavky_BRYLE_v8`. Pozor při zkoušení: hra si při ukončení přepíše řádek v `[newgrf]` na
  `4D415808|<md5>|…` a podle GRF ID a md5 pak klidně vezme starší soubor ze složky (`hra/README.md`); md5 je u v7 i v8
  stejné (`EA3B7428…`, počítá se jen z akcí, ne z obrázků), starší verze proto ze složky pryč.

## Verze 7 (2. 10.): holky u dveří v přiblížení 8×

Kolega dal hře přiblížení 8× (forclaude `51428e5`, `ZoomLevel::In8x` před původním 4×, v GRF kód zoomu 6). Hráč:
*„potřebujem udělat yagl pro zinc zoom a zkusíme to na dvanácttrojkách na přikládacích studentkách, dáme maximum
detailu, jsou to maličký obrázky, které jen přikládáme“*.

- **yagl umí `zin8`** (`yagl/NASE-UPRAVY.md`, oddíl 5): v jednom `sprite_id` stojí řádek `zin4` a pod ním `zin8`
  s obrázkem přesně dvojnásobným (šířka, výška i posun od kotvy; hra to u víc úrovní jednoho spritu vyžaduje).
  Jiná hra kód 6 přeskočí, GRF jí jde dál.
- **Holky u dveří mají obě úrovně.** Fotky 8× (`holky-u-aut/foto/*_z8.png`) jsou na 24,4 px/m místo 12,2 a mají
  1024 vzorků místo 64 (šest fotek za 3 minuty). Vrstvy 4× zůstaly pixel po pixelu jako ve v6, vrstvy 8× jsou
  jejich přesný dvojnásobek (`holky-u-aut/README.md`). Prázdné směry mají 8 × 8 průhledných pixelů.
- **Ostatní sprity mají dál jen 4×**, hra si je v 8× zdvojí sama. Auta, náklady, texty: beze změny (souhrn
  `vwt1-nova-souhrn.json` stejný jako ve v6).
- Náhled `holky-u-aut/nahled_8x.png`: vlevo 4× (zvětšeno 3×), vpravo 8× (auto zdvojené, holky z fotek 8×,
  zvětšeno 1,5×).
- **Ověřeno ve zkušební hře z `51428e5`** (`hra/README.md`, třetí zkušební hra): `testholky` s `setting
  gui.zoom_min 0` fotí v 8×, holky jsou z vrstev 8×; se `zoom_min 1` (4×) stejný obrázek jako v6.
- Složení jako dřív, jen `dodavky_BRYLE_v7` a nový yagl; rozbalení zpět dá 16 řádků `zin8` a vlastní list
  `dodavky_BRYLE_v7-32bpp-zin8-0.png`.

## Verze 6 (1. 10. večer): kovy pod plachtou, odpad na kupě

Podle výpisu průmyslu ze dvou her hráče (všechny kódy už ve vzorové tabulce jsou, chyběl jen zvláštní náklad hry ROLA,
ten do tabulky nepatří). Hráč k tomu, co dvanácttrojky nevozily:
- *„kovy můžou být pod plachtou“*: plachta a plachta šedá (0x91, 0x92) nově vozí 22 kovů a ocelí: ocel (STEL),
  ocelové slitiny, plechy, pláty, tyče, ingoty, bramy, profily, konstrukční, uhlíková a nerezová ocel, hliník, surové
  železo, zinek, nikl, kobalt, měď, kov, litina, feroslitiny, ferochrom, bílý plech a vzácné kovy;
- *„odpad bude ta šedá kupa na valníku V3S, Tatra, TAZ“*: valník s kamennou kupou (0x87) nově vozí odpadky (TRSH),
  odpad (WSTE) a recyklovatelný odpad (RCYC);
- *„nemůžem dát cennosti, zlato, diamanty do dvanácttrojek, uděláme pak na to auto pěkný, Avia VB“*: cennosti, zlato
  a diamanty dvanácttrojky dál nevozí;
- *„tekutiny máme sudy a cisterny, to půjde“*: tekutiny vozí sudy vejtřasky a cisterny Tater, dvanácttrojky ne;
- vozidla, těžká vozidla a karoserie se do dvanácttrojky nevejdou.

Ostatní auta beze změny (srovnání seznamů v5 a v6 po rozbalení). Ověřeno ve zkušební hře: GRF se načte, `testv3s`
s `TEST_RV_GRF=MAX\x08` projde všechna auta bez chyby.

## Verze 5 (1. 10.): holky u dveří, brambory BRAM

- **Holky u otevřených dveří**, když auto nakládá na zastávce:
  - auta: TAZ 1203 bus a bus zahrádka, TAZ 1500 bus a bus zahrádka, Škoda 1203 Pajda karavan;
  - holky stojí na straně k chodníku, jedna u předních dveří, druhá z boku u kufru;
  - jsou ve 2× jako dívky na zastávce a bez stínu.

  Je to samostatná vrstva přes auto (a ve dvou směrech pod autem), obrázky a rozmístění jsou v `holky-u-aut/`.
  Viditelné auto má navíc bit 7 ve `miscellaneous_flags` (vrstvy), skupiny `0xE0` a `0xE3` a switche `0xE1` a `0xE2`
  (`holky-u-aut/README.md`).
- **Nový kód BRAM** (hráč: *„valník brambory, vem mu kód BEAN a dej mu kód BRAM, uděláme si svoje brambory, a fazole
  dáme do hnědých pytlů na kafe“*):
  - v překladové tabulce je na konci, slot 0xDD, tabulka má 222 kódů a stará čísla platí;
  - valník brambor (0x88) veze TATO, BRAM, CASS a SGBT, BEAN už ne;
  - BRAM vezou i VW T1, modré dodávky a plachty, všude, kde jsou TATO;
  - fazole BEAN jedou v dodávkách a pod plachtou jako dosud, hnědé pytle jsou na V3S a Tatrách.
- **Popis GRF:** k „3D: renderatnight“ přibyl Rabatin.B (Škoda 1203, z hráčova lístku) a řádek s autory holek
  „Girls: kiemtruongkts, Rotmill (CC BY 4.0)“ (`AUTORI-MODELU.md`).
- **Kontrola:** rozbalená v5 proti rozbalené v4 se liší jen o:
  - popis a překladovou tabulku;
  - tři nové záznamy s holkami;
  - seznamy nákladů aut s BRAM;
  - u pěti aut s holkami vlastnosti viditelného dílu, jeho switche a Action 3.

  Všechny sady spritů aut jsou beze změny.
- **Zkouška ve hře:**
  - příkaz `testholky` pro TAZ 1203 bus, Pajdu a TAZ 1500 bus na CZTR silnicích a pro TAZ 1203 bus na původních;
  - všechna auta zastavila ve všech čtyřech směrech a holky jsou na místě (`holky-u-aut/ve_hre.png`);
  - za jízdy holky nejsou.

## Verze 4 (30. 9.): fialová TAZ 1900 D

- **Nové auto 0x98 „TAZ 1900 D dodavka“:** kopie modré dodávky TAZ 1500 bez zahrádky (0x97). Modrý lak (syté
  body v odstínu 190–225°) je otočený na fialovou, odstín 285°, sytost a jas zůstaly. Hráč dostal na výběr tři
  odstíny (275, 285, 295) v náhledu `nahled_taz1900d_fialova.png`, vzal jsem prostřední.
- **Údaje:**
  - motor VW 1,9 l diesel, 40 kW (54 k), max. 110 km/h (česká Wikipedia, u fotky mikrobusu TAZ 1900 roky 1998–99);
  - motor VW 1,9 l v řadě od roku 1996 (Škoda Storyboard), proto výroba 1996 a zkouška od 1995;
  - ve hře 50 k, na rovině jede nejvýš asi 95 km/h (silnější motor hráč nechce);
  - náklady jako modrá dodávka bez bedny, 2 lidi, výchozí pošta.
- **Zkouška:**
  - hra od 1994: TAZ 1900 D není, od 1997 je;
  - čumák má délku 1, auto 8, lidé 1 + 1, pošta 2 + 2;
  - zpětné rozbalení se shoduje;
  - proti verzi 3 v yaglu jen přibyl blok nového auta.

## Verze 3 (30. 9.): roky

Hráč: *„Škoda 1203 z Vrchlabí prototyp od roku 1963 na zkoušku ve hře a od roku 1968 výroba. TAZ je z Trnavy,
TAZ 1203 od 1973 … 1981 pusť zahrádky, ať mají radost, od 1973 bez zahrádek … U 1985 to je jedno, nech tvých 1988,
to může být prototyp na zkoušku 1985. Můj zdroj roku výroby je pochybný.“*

- **Jak to hra dělá:** v den uvedení nabídne auto jedné firmě na rok na zkoušku (prototyp) a za rok ho mají všichni.
  Proto je v GRF datum uvedení o rok dřív než výroba. Zkouška trvá ve hře vždycky rok, delší prototyp (1963 až 1968)
  zapsat nejde. Když hra začne až po datu uvedení, auto je hned pro všechny. A když začne víc než dva roky před ním,
  hra k datu přičte náhodně 0 až 511 dní.
- **Roky (výroba, zkouška rok předtím):**
  - VW T1: výroba 8. 3. 1950, prototyp 1949 (VW je opravdu stavěl v roce 1949);
  - Škoda 1203 Pajda karavan: výroba 20. 11. 1968 ve Vrchlabí, zkouška od listopadu 1967;
  - TAZ 1203 valníky, plachty, bus a dodávka bez zahrádky: výroba 1. 4. 1973 v Trnavě, zkouška od dubna 1972;
  - TAZ 1203 se zahrádkou (bus zahrádka 0x8B, dodávka zahrádka 0x8D, dodávka zahrádka bedna 0x8E): 1981, hráč;
  - TAZ 1500: výroba 1988, zkouška 1987.
- **Zdroje k hráčovým rokům:**
  - Škoda 1203: první prototypy typ 979 počátkem roku 1957, pět kusů do 1958, od 1959 typ 997, konečná podoba
    představena 14. 9. 1968, výroba od 20. 11. 1968 (Škoda Storyboard). Hráčův rok 1963 sedí:
    - prototypu 997 z roku 1961 se v závodě už říkalo 1203;
    - v letech 1962–1964 vznikla řada prototypů, na kterých je budoucí 1203 hned poznat;
    - v roce 1963 byl hotový prototyp valníku (kniha Jana Králíka).

    Zdroje: tipcars.com, denik.cz. Hra ale nabízí auto na zkoušku jen rok, zůstává tedy zkouška 1967 a výroba 1968.
  - TAZ 1500: anglická Wikipedia má 1985 (modernizace, motor 1433 cm³), Škoda Storyboard 1988. Nechán 1988.
- **Zkouška:**
  - hra od 1979: TAZ 1203 valníky, plachty, bus a dodávka bez zahrádky jsou, zahrádky a TAZ 1500 ne;
  - hra od 1985: i zahrádky, TAZ 1500 ne.

## Verze 2 (30. 9.)

- **TAZ 1203 bus a dodávky, nová auta 0x8B–0x8F.** TAZ 1500 (bus, bus zahrádka, tři modré dodávky) přijely až
  v roce 1988 a v hráčově hře ještě nebyly. Hráč: *„oni maj hranatý světla jako TAZ, tak z nich nemůžem udělat
  Škodu 1203. Je to datum uvedení, to jsi udělal dobře. Tak uděláme bus TAZ 1203, dva busy jen světlejší žlutou,
  a dodávku taky TAZ 1203, tři dodávky světlejší modrou.“* Proto vznikla nová auta:
  - bus zahrádka 0x8B a bus 0x8C, světlejší žlutá;
  - dodávka zahrádka 0x8D, dodávka zahrádka bedna 0x8E a dodávka 0x8F, světlejší modrá.

  Údaje mají jako ostatní TAZ 1203 (duben 1973, 47 k, 90 km/h) a náklady jako jejich TAZ 1500. TAZ 1500 zůstaly,
  od roku 1988.
- **Světlejší lak:** kopie spritů TAZ 1500, všechny sady (prázdný, plný, nakládání, prázdný na zastávce) i ikona.
  Zesvětlený je jen lak, tedy syté body v odstínu 40–62° (žlutá) nebo 190–225° (modrá). V HSV mají sytost × 0,72
  a jas × 1,10 + 0,04. Okna, kufry, sedačky, kola a náklad zůstaly (`nahled_taz1203_svetlejsi.png`: vlevo TAZ 1500,
  vpravo TAZ 1203).
- **Hráčova kontrola:** prošel každý obrázek, je to v pořádku. Známá vada z focení modelu: na zaplechovaných
  zadních oknech jsou šmouhy (model prosvítal), ve hře ale nejsou vidět.
- **Čumák délky 1** (`shorten_vehicle 0x07`) místo 2. Hráč: *„je tam velká mezera, to by nešlo menší neviditelný
  článek?“* V koloně je rozestup 8 + délka čumáku, tedy 9 místo 10. Mezi obrázky aut (dlouhými 7) zbydou 2 jednotky
  místo 3, jako u první verze s článkem vpředu (CUMAK.md). Menší to s článkem nejde, kratší než 1 díl být nemůže.
  Souprava je dlouhá 9, na Rolu stačí vagon 9.
- **Zkouška:**
  - V roce 1980 se dají koupit TAZ 1203 bus a dodávky, TAZ 1500 ne. V roce 1990 obojí.
  - Čumák má délku 1, auto 8.
  - Bus veze 1 + 7 lidí, dodávky 1 + 1 lidí a poštu i zboží 2 + 2.
  - Pořadí kreslení je správně ve všech 24 dvojicích (`poradi_verze2.png`: TAZ 1203 bus proti plachtě, Tatra proti
    TAZ 1203 dodávce, plachta proti Tatře).

## Co se změnilo ve verzi 1

1. **Překladová tabulka:** za `FREE` je připsáno 125 kódů ze vzoru (`prekladova-tabulka-vzor.yagl`) v jeho
   pořadí, sloty 0x60–0xDC. Celkem 221 kódů. Hráčova čísla 0x00–0x5F zůstala.
2. **Náklady** podle hráče (níž).
3. **Nový valník 0x8A „TAZ 1203 valnik zelena marihuana“:** kupa brambor z valníku 0x88 přebarvená herní
   zelenou marihuany (paleta 0x52–0x57). Zelená je plná kupa i malá kupa při nakládání. Okno kabiny zůstalo
   červené. Ikona v nákupu je stejná jako u ostatních valníků. Skript `zelena_kupa.py`, náhled
   `nahled_zelena_kupa.png`.
4. **Čumák 2 + auto 8** (ve verzi 2 čumák 1):
   - auto má `shorten_vehicle 0x00`;
   - článkovací switch vrací jen auto, zadní nárazník 0x00C0 se už nepřipojuje. Jeho definice zůstala kvůli
     rozehraným hrám.

   Pořadí kreslení je správně (`poradi_nova_verze.png`, níž).
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
- **Modré dodávky bez bedny (TAZ 1203 i TAZ 1500, se zahrádkou i bez):** jako VW T1 bez věcí z bedny.
- **Dodávka bedna (TAZ 1203 i TAZ 1500), plachta bedna, valník bedna:** jen věci z bedny.
- **Plachta a plachta šedá:** jako dodávka a navíc neznámé kódy (CRAN LFEQ SCPR STTP SWRP TIN_ WDCH), od verze 6 i kovy.
- **Valníky podle barvy kupy:**
  - dřevo: WOOD, TWOD;
  - uhlí: COAL, COKE, MNO2;
  - jíl: CLAY, PEAT, BIOM, AORE, IORE, CORE, COCO;
  - písek: SAND, SULP, GRAI, WHEA, MAIZ, CERE;
  - kámen: GRVL, LIME, SLAG, SCMT, SCRP, NKOR, PORE, POTA, PHOS, od verze 6 i odpad TRSH, WSTE, RCYC;
  - brambory: TATO, BEAN, CASS, SGBT;
  - zelený: MARI, HOPS.

  Všech 17 kódů sklápěčky Tatry vezou valníky, každý na tom s kupou své barvy.
- **Lidé:**
  - dodávky, valníky, plachty a VW T1: PASS, WORK, PRIS, YETI, YETY, 2 lidi;
  - busy (TAZ 1203 i TAZ 1500, se zahrádkou i bez): PASS, TOUR, OTI1, OTI2, STUD, WORK, PRIS, YETI, YETY, PLAY,
    8 lidí;
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
  - busy a Pajda: cestující.
- **Nákup:** switch pro nákup zná článkovací callback 0x16, takže nákup ukazuje celé auto. Dřív ukazoval jen
  čumák, s kapacitou 1.

## Skutečné údaje

| auto | výroba (od verze 3 zkouška rok předtím) | výkon | max. rychlost | váha | zdroj |
|---|---|---|---|---|---|
| VW T1 | 8. 3. 1950 | 25 k, ve hře 30 k | 80 km/h | 975 kg, ve hře 1 t | Wikipedia (T1), automobile.at |
| Škoda 1203 Pajda karavan | 20. 11. 1968 | 110 k (lepší motor, hráč) | 130 km/h (hráč) | 1 170 kg | Škoda Storyboard |
| TAZ 1203 valníky, plachty, bus a dodávka bez zahrádky | 1. 4. 1973 (Trnava) | 47 k (35 kW), ve hře 50 k | 90 km/h | 1 170 kg | Škoda Storyboard |
| TAZ 1203 bus a dodávky se zahrádkou | 1981 (hráč) | 47 k (35 kW), ve hře 50 k | 90 km/h | 1 170 kg | Škoda Storyboard |
| TAZ 1500 bus a dodávky | 1988 (motor 1433 cm³) | 57 k (42 kW), ve hře 60 k | 110 km/h | 1 260 kg | Škoda Storyboard, Wikipedia |

- **Jednotky ve hře:** výkon jde jen po 10 k, váha po čtvrt tuně.
- **Rychlost nad 127 km/h** zapisuje vlastnost 0x15 (`speed_half_kmh`, jednotka 2 km/h): Pajda 0x41 = 130 km/h.
- **Hra se nemění.** Odpor vzduchu zůstává výchozí, hra ho počítá z max. rychlosti. Při realistickém zrychlení
  proto na rovině jedou nejvýš:
  - VW T1 71 km/h;
  - TAZ 1203 89 km/h;
  - TAZ 1500 101 km/h;
  - Pajda 130 km/h, díky lepšímu motoru i naložený.

  Hráč 30. 9.: „silnější motory ostatním nedávej“. VW T1, valníky, plachty, busy a dodávky mají skutečný motor.

## Jak to složit

```bash
mkdir z && cd z
cp ../VWT1-S1203-clanky-oba-na-stred.grf . && yagl -d VWT1-S1203-clanky-oba-na-stred.grf
python3 ../zelena_kupa.py sprites/VWT1-S1203-clanky-oba-na-stred.yagl \
    sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png 0x88 zelena.pkl
mkdir -p novy/sprites
python3 ../stavba_vwt1.py sprites/VWT1-S1203-clanky-oba-na-stred.yagl \
    sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png zelena.pkl ../vwt1_kody.json novy/sprites dodavky_BRYLE_v8
cp sprites/VWT1-S1203-clanky-oba-na-stred-32bpp-zin4-0.png novy/sprites/
cd novy && yagl -e dodavky_BRYLE_v8.grf sprites
```

Ověřeno 30. 9.:

- postup dal bajt po bajtu stejné GRF: každá verze skriptem ze své verze (v gitu u jejího commitu);
- zpětné rozbalení se shoduje se sestaveným yaglem, liší se jen poznámky a rozmístění spritů na listu;
- původní GRF po rozbalení a novém složení vyjde beze změny.

## Zkouška ve hře (zkušební kopie hry, beze změn hry)

- **`testv3s`** (koupě a přestavby) na všech kupovatelných autech, verze 1:
  - čumák má délku 2, auto 8, zadní nárazník už není;
  - lidé 1 + 1, 1 + 4 a 1 + 7;
  - zboží a pošta 2 + 2, ostatní 1 + 1;
  - lidé na valníku: prázdný obrázek;
  - uhlí, brambory, marihuana i chmel: plný obrázek, u zeleného valníku sprite se zelenou kupou;
  - bedna: bedna na korbě.

  Že nákup ukazuje celé auto, plyne z kódu hry (`GetNextArticulatedPart` volá callback 0x16 v nákupu). Zkouška
  to přímo neměří.
- **`testpruhy`** (osa X, stojící dvojice proti sobě, čela 0–14/16 dlaždice od sebe), verze 1,
  `poradi_nova_verze.png`:
  1. bus proti plachtě šedé;
  2. Tatra 148 proti plachtě šedé;
  3. plachta proti Tatře.

  Nahoře je ve všech 24 dvojicích auto v předním pruhu, stejně jako u zkušebního čumáku 2 + auto 8 v CUMAK.md.
- Verze 2: viz oddíl nahoře.

## Otevřené

- Zámek a přesun k základní grafice hry, až budou auta hotová.
- Auta koupená v rozehrané hře před výměnou GRF si nechají zadní nárazník. Nově koupená už ho nemají.
