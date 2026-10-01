# V3S Vejtřaska: Praga V3S jako vlastní GRF

## Verze 13 (1. 10.): studentky na korbě

Hráč:
- *„dáme dvacet studentek na valník, který vozí STUD, bez plachty, dvacet asi je moc, to se nevejde“*;
- *„stejnou velikost dáme k autům, aby to ladilo se zastávkou“*;
- *„studentky na valník Tatra a V3S, nemusí jich být dvacet“*;
- *„STUD povolíme přestavbu na zelenou Tatru“*.

Co je nové:
- **Se studenty (STUD) stojí na korbě holky místo plachty.** Platí to pro obě vejtřasky, modrou i zelenou, a pro
  Tatru 148 a 138 na valníku.
  - Holky jsou College Girl, holka v tyrkysovém tílku a bělovlasá Galaxia z `postavy/`.
  - Stojí v řadách po dvou čelem ke kabině, každá trochu natočená, některé bokem ven.
  - Velikost je 2× jako dívky na zastávce: na vejtřasku se vejde 8 holek (4 řady), na Tatru 10 (5 řad).
  - Náklad `studentky` je v `render_v3s.py`. Tatra si stavitele nákladu bere odtud, kabinu má na druhé straně
    (`SMER_KABINY`).
  - Jako ostatní náklad je vidět od poloviny naložení.
  - Srovnání 2× a 1,5× (12 holek) je v `kontrola/studentky_2x_1_5x.png`, hráč nechal 2×.
- **Kapacita se nemění:** zelená vejtřaska 20, modrá a Tatry 3 (u velké čumák 1 a zbytek auto). Ostatní lidé jedou
  jako dřív: vojáci pod plachtou, v modré a v Tatře v kabině.
- **Tatra:** STUD má zelenou přestavbu navíc (`T_ZELENA_NAVIC`), v okně přestavby je „(zelená)“ se studentkami
  na vojenském valníku. U velké odpovídá na jména podtypů i čumák, jinak by je okno přestavby nevzalo.
- **V popisu GRF** přibyl řádek s autory holek „Students: kiemtruongkts, Rotmill, Tatenashi (Sketchfab), CC BY 4.0“
  a v `licence.txt` jejich modely s odkazy.
- Malá 6,68 MB (`49b3b1f5…`), velká 7,88 MB (`644b7dd6…`), balík `Praga_V3S_Tatra-v13.zip`. Rozbalit a znovu
  složit yaglem: malá bajt po bajtu stejná.
- **Ověřeno ve zkušební hře:**
  - **Fotka** `TEST_FOTO_SADA=studentky` (`tatra/nahledy/ve_hre_v13_studentky.png`): modrá a zelená vejtřaska,
    Tatra 148 a 138 i v zelené přestavbě, malá i velká.
  - **`testv3s`** pro `MAXd` i `MAXe`:
    - STUD: zelená 20, modrá a Tatry 3;
    - obrázek holek je stejný u vejtřasek a stejný u Tater;
    - Tatry mají podtypy „“ a „(zelená)“;
    - ostatní náklady beze změny proti verzi 12.
- **Ve hře zatím není průmysl se studenty** (hráč: *„ještě není build s průmyslem studentky, až to doděláme“*).

## Verze 12 (1. 10.): naše brambory BRAM, fazole v hnědých pytlích

Hráč: *„valník brambory, vem mu kód BEAN a dej mu kód BRAM, uděláme si svoje brambory a fazole dáme do hnědých
pytlů na kafe, v pytlích se ztratí i brambory BEAN“*.

- **Nový kód BRAM** na konci vzorové tabulky (`prekladova-tabulka-vzor.yagl`, slot 0xDC). Tabulka má 221 kódů, stará
  čísla platí.
  - Vozí ho všechny vejtřasky i Tatry, stejně jako TATO.
  - V okně přestavby je „(na kupě)“ se žlutou kupou brambor a „(v pytlích)“ v hnědých pytlích.
  - Modrá vejtřaska je s ním v odstínu B (zemědělství).
- **Fazole BEAN** jsou v hnědých pytlích jako káva, bez podtypů. Dřív měly kupu a pytle jako brambory, protože je CZIS
  má přejmenované na brambory.
- **Tatra:** zelená přestavba navíc je i u BRAM (`T_ZELENA_NAVIC`), u BEAN zůstala.
- Vojenská vozí 216 nákladů, modrá 209 (o jeden víc, BRAM).
- Malá 6,58 MB (`b97e2aea…`), velká 7,75 MB (`c05eee41…`), balík `Praga_V3S_Tatra-v12.zip`.
- Valník brambor z dodávek veze od jejich verze 5 také BRAM místo BEAN (`auta/NOVA-VERZE.md`).
- **Ověřeno ve zkušební hře.** Zkušební náklady `hra/zkusebni_naklady` mají od dneška i BRAM a BEAN.
  - **Fotka** `TEST_FOTO_SADA=brambory` (`tatra/nahledy/ve_hre_v12_brambory.png`):
    - modrá vejtřaska s BRAM na kupě a v pytlích, s fazolemi a s kávou v hnědých pytlích;
    - zelená vejtřaska s BRAM na kupě a s fazolemi;
    - Tatra 148 s BRAM na kupě a s fazolemi, Tatra 138 s BRAM v pytlích;
    - valník TAZ 1203 z dodávek v5 s kupou brambor.
  - **`testv3s`** pro `MAXd` i `MAXe`:
    - BRAM má u obou vejtřasek podtypy „(na kupě)“ a „(v pytlích)“, u Tater navíc obojí „zelená“;
    - BEAN je bez podtypu v hnědých pytlích (stejný obrázek jako BRAM v pytlích), u Tater i „(zelená)“;
    - ostatní náklady jako ve verzi 11: modrá umí 35 z 39 nákladů zkušební hry (chybí URAN, MLTR, BOOM a ROLA),
      zelená 37 (chybí TOYS a ROLA), Tatry 38 (chybí ROLA).

## Verze 11 (30. 9.): zelená Tatra schovaná pod normální, GRF jen pro naši hru

- **Zelená Tatra 148 a 138 zmizela z nákupu** (hráč: *„hlavně zmizí z menu nákupu ta vojenská 138 148 a schová
  se“*). V GRF zůstala (`0x0104`, `0x0105`, klima žádné), aby rozehrané hry jezdily dál. Zelená vejtřaska zůstává
  (*„zelenou v3s neschováme, ta prostě jezdila v civilu běžně“*).
- **Oranžová 148 a červená 138 vozí i vojenské náklady a jsou s nimi celé zelené** (*„hráč koupí tatru na explosives
  a dostane zelenou“*): jídlo, výbušniny, uran, uranová ruda, jaderné palivo a odpad, vojenská technika. Jedou na
  vojenském valníku s obrázkem nákladu, nebo pod vojenskou plachtou. Nevozí jen sklo, elektřinu a přeřazení lokomotivy.
- **Zelená přestavba navíc**, v okně přestavby další podtyp „… (zelená)“: zvířata (prasátka, kravičky, ovečky), co
  roste na valníku (marihuana, seno, vlákna, marihuanové seno, ovoce, zrní), dřevo, cihly, stavebniny (cement, vápno,
  pytle), doutníky, tabák a alkohol. Cisterny Plzeň a Budvar zelenou variantu nemají (*„přestavby na pivovar Plzeň
  Budvar ne“*), sudy ano. Seznam je `T_ZELENA_NAVIC` v `tatra/grf_tatra.py`.
- **Řádek 3D** v popisu GRF jako u VW T1: `3D: hans1240 (Praga V3S, Tatra 148, Tatra 138), sketchfab.com/hans1240,
  CC BY 4.0`.
- **Jen pro naši hru.** Hráč: *„skupiny nákladů nechcem, máme náklady pěkně vypsaný na řádku“*, *„neuskromněný,
  využij nový rozsah čísel bloků“*. Každý náklad má u Tatry svoje bloky grafiky a normální Tatra jich potřebuje víc,
  než kolik jde zapsat jedním bajtem (malá 211, velká 189, bylo 176 volných). GRF se proto v Action 14 před hlavičkou
  ptá na `decouple_more_action2_ids` (dvoubajtová čísla bloků, hra od forclaude `682797f`,
  `hra/cisla-bloku/ZPRAVA-OD-HRY.md`) a na zámek `decouple_128_cargo`; hned za hlavičkou je zámek (Action 7 na bit 8
  proměnné 0x9D, jinak Action B): jinde se GRF vypne s hláškou *„Tento GRF patří ke hře OpenTTD decouple by Karel
  Mácha a jinde nefunguje.“* Zamčená je i vejtřaska, je ve stejném GRF. Náš yagl umí dvoubajtová čísla od téhož dne
  (`yagl/NASE-UPRAVY.md`, bod 4). Switche jdou od `0x10` do `0xBF` a pak od `0x100`, vrstvy nákladu zůstaly na
  `0xC0` až `0xFF`.
- Malá 6,58 MB (`dbd34c04…`), velká 7,74 MB (`22e454ea…`).
- **Ověřeno ve zkušební hře s dvoubajtovými čísly** (kolegova hra `c53e895` s mými zkušebními příkazy,
  `hra/ottd-zkusebni-c53e895-gfx.tar.xz`), `testv3s` pro `MAXd` i `MAXe` na všech 37 nákladech hry a všech podtypech:
  zelené Tatry nejdou koupit (malá i velká), oranžová a červená umí 36 z 37 (chybí jen `ROLA`, auta na vlaku),
  s uranem, vojenskou technikou a výbušninami jsou celé zelené, zelená přestavba navíc je u 14 nákladů, které
  zkušební hra má (LVST GRAI WOOD TATO CMNT BEER SGCN BRCK BDMT FRUT WINE HOPS FICR MARI), vždy stejná vrstva nákladu
  na zeleném valníku; pivo v cisterně Plzeň a Budvar bez zelené. Všechny čtyři Tatry stejně, zvuky jako u vejtřasky,
  vejtřaska beze změny. Po uložení a načtení hry stejný výsledek. Fotka okruhu: `tatra/nahledy/ve_hre_v11.png`.
  Ve staré zkušební hře bez těch vlastností se GRF vypne (Action 7 nepřeskočí, Action B fatální) a žádné auto
  z něj ve hře není. Rozbalit a znovu složit yaglem: malá bajt po bajtu stejná.

## Verze 10 (29. 9.): vejtřaska a Tatry v jednom GRF

- **Tatry 148 a 138 ve stejném GRF** (hráč: *„tak je dáme k vejtřaskám, ať ušetříme místo MB za zvukové soubory?“*,
  *„jo dobrý“*): zvuky jsou v GRF 3,1 MB ze 4,4 MB, takže každý soubor ušetří asi 3 MB. Soubory se jmenují
  `Praga_V3S_Tatra-v10.grf` (malá, `MAXd`) a `Praga_V3S_Tatra_BRYLE-v10.grf` (velká, `MAXe`), číslo GRF zůstalo,
  rozehrané hry s vejtřaskou poběží dál. Tatry balí `tatra/grf_tatra.py`, který `pack_v3s.py` spustí, když dostane
  čtvrtý argument s fotkami Tater: `python3 pack_v3s.py <mala|velka> <fotky vejtřasky> grf/<varianta> <fotky Tater>`.
  Popis Tater je v `tatra/README.md` (oddíl GRF).
- **Červenější cihly** (hráč: *„náklad cihly trochu červenější na příště“*).
- **Výjezd z depa bez startéru** (hráč: *„ustřihni starter ze zvuků, tu první vteřinu, možná dvě vteřiny, když ho
  pustím z depa“*): `zvuky/syntetizuj_zvuky.py` ořízne zvuk na začátku o 1,3 s (tak dlouho hraje startér), výjezd
  začíná, jak motor chytne, zatroubí a vyjede; 3,7 s místo 5 s. Ostatní zvuky se nezměnily (stejné md5).
- Malá 6,44 MB, velká 7,56 MB (verze 9 bez Tater 4,37 a 4,78 MB).
- **Ověřeno ve zkušební hře** (`testv3s` pro `MAXd` i `MAXe`, fotky okruhu): oranžová a červená Tatra nevozí uran
  a vojenskou techniku (umí 33 z 35), zelené je vezou (34 z 35, chybí hračky); uhlí jede na sklápěči, voda, ropa
  a kyselina v cisterně své barvy, pivo v sudech a přestavbou v cisterně Plzeň a Budvar, zvuky má Tatra stejné
  jako vejtřaska. Vejtřaska se chová jako ve verzi 9 (stejné kapacity, náklady, podtypy i počty vrstev). Tatry
  jezdí na okruhu ve správném pruhu.

## Verze 9 (29. 9.)

- **Vojenskou techniku** (`MLTR`) vozí jen zelená (hráč: *„mltr jen zelená“*). Kódy z nevydaného průmyslu CZTR
  podle vagónů a hráče: `FLOU` mouka, `LETH` kůže, `MLTR` vojenská technika, `UORE` uranová ruda (jen zelená už
  od verze 8). `FREE` není náklad, je to hráčova značka ve VW T1, kde skončil; vejtřaska ho nevozí.
- Neznámé kódy (11) zůstávají ve vzoru a jedou pod výchozí plachtou (hráč: *„musíme kódy evidovat, i když
  nevíme, co to je, dáme neutrální grafiku plachty“*).
- Grafika jako ve verzi 8. Malá 4,37 MB, velká 4,78 MB.
- **Ověřeno ve zkušební hře** (zkušební náklady navíc `MLTR`): modrá vojenskou techniku nevozí (umí 33 z 35,
  chybí uran a vojenská technika), zelená ji veze pod olivovou plachtou (34 z 35, chybí hračky).

## Verze 8 (29. 9.)

- **Vzorová tabulka 220 kódů** (hráč: *„budem muset aktualizovat vzorovou tabulku, já si ji pak stáhnu od tebe“*):
  prvních 147 beze změny na stejných číslech, za MARI kódy z VW T1, FIRS 5.2 a CHEM (jako dosud), kódy ze sad
  v hráčově hře (save `v3s2`, `naklady.md`), víno `WINE` a kódy, které znají jen vagóny. Vejtřaska bere celý vzor,
  vlastní kódy navíc už nemá. Chmel je `HOPS` (hráč: *„hops, tak to je náš kód“*).
- **Lidé:** navíc studenti `STUD`, vězni `PRIS`, kvalifikovaní dělníci `WORK` a hráči `PLAY` (Temporal8 Real
  Industries), zelená 20 pod plachtou, modrá 3 v kabině. Turisté jsou ve hře dva kódy, `TOUR` a `OTI2`, oba vozí.
- **Jen zelená:** navíc jaderný odpad `NWST` a uranová ruda `UORE` (hráč: *„odpad jaderný vojenská jenom, všechno
  co je uran jenom zelená“*).
- **Náklad na korbě**, co je nové:

  | náklad | obrázek |
  |---|---|
  | BRCK cihly | podtypy: červené, šedé (o kus větší) cihly na paletách |
  | BDMT stavební materiál | podtypy: červené cihly, šedé cihly, bílé pytle |
  | TATO BEAN brambory | podtypy: kupa brambor, hnědé pytle (hráč: *„já brambory ještě neviděl“*) |
  | FRUT FRVG ovoce | pestrá kupa jablíček (hráč: *„ovoce krásný je“*) |
  | BEER alkohol | podtypy: rum (dřevěné sudy), pivo Plzeň (bílé sudy), pivo Budvar (šedá plachta) |
  | WINE víno | dřevěné sudy jako rum |
  | HOPS chmel | marihuanové seno |
  | kyseliny a plyny z AXIS a GIST | červené sudy; NAPH a LUBR jako ropa, COCO (měděný koncentrát) kupa měděné rudy |

- **Velikost:** malá 4,37 MB, velká 4,78 MB.
- **Ověřeno ve zkušební hře** (`testv3s`, zkušební náklady navíc BRCK BDMT FRUT STUD WINE HOPS): každý náklad
  i podtyp má svůj obrázek a jméno v obou dílech, studenti 20 a 3, modrá nevozí uran, zelená hračky.
  Fotka ze hry: `kontrola/hra_naklady_v8.png`.

## Verze 7 (29. 9.)

- **Nákup:** zeleně „for ottd Decouple by Karel Mácha“, pod tím „Model: hans1240 (Sketchfab), CC BY 4.0“
  (hráč: *„napíšem zeleně for, for ottd decouple by karel macha. A kde máš autora objektu, toho tam
  napíšem“*). Dva krátké řádky, okno nákupu se nezvětší.
- **Náklad na korbě**, co je nové (hráč: *„žádný modrý náklad, auta jsou modrý“*):

  | náklad | obrázek |
  |---|---|
  | CMNT SALT SUGR RSGR WOOL BDMT KAOL QLME SASH (cement, sůl, cukr, vlna, stavební materiál, kaolín, nehašené vápno, soda) | bílé pytle jako ve verzi 5, náhodně naházené, černá čára kolem každého (hráč: *„tam černou linku kolem pytle … slévaly se do sebe“*) |
  | JAVA káva | hnědé pytle |
  | GOOD FMSP ENSP WELD (zboží, zemědělské a strojírenské zásoby, svařovací materiál) | bedny |
  | GRAI WHEA MAIZ CERE obilí | žlutá kupka jako písek |
  | CORE měděná ruda | zelenošedá kupka |
  | AORE NKOR PORE MNO2 URAN ostatní rudy | kupky: bauxit jako železná ruda, niklová jako struska, pyritová jako štěrk, mangan a uran jako koks |
  | CLAY jíl | okrově hnědá kupka |
  | SGCN cukrová třtina | vlákna (obrázek přadných plodin) |
  | WATR MILK EOIL MOLS voda, mléko, olej, melasa | bílé sudy místo modrých |
  | FICR přadné plodiny | tři podtypy: vlákna, marihuanové seno (zelené), seno (žlutší) |

  Kupka nehašeného vápna je pryč, vápno jede v pytlích. Pod plachtou dál plasty, mouka, hnojivo a saze.
- **Černá čára kolem pytlů** dělá `render_v3s.py` (`OBRYSY`): druhý render, kde má každý pytel svou barvu,
  z něj pixely na hranách pytlů, ty se ve fotce ztmaví (`temata3.md`). Při oddálení se čára rozpadne na
  tečky, hra zmenšuje sprity výběrem pixelů.
- **Velikost:** malá 4,27 MB, velká 4,66 MB.
- **Ověřeno ve zkušební hře** (`testv3s` obě velikosti, zkušební náklady rozšířené o JAVA CLAY SGCN KAOL):
  každý náklad se přestaví a naložený ukáže svůj obrázek (cement a kaolín stejné bílé pytle, káva hnědé,
  jíl svou kupku, třtina vlákna), podtypy vláken i dobytka mají jména a obrázky v obou dílech, modrá nevozí
  uran, zelená hračky, modrá je v nákupu první. Fotka ze hry: `kontrola/hra_naklady_v7.png`.

## Verze 6 (29. 9.)

Jen popis v nákupu (callback 0x23): jediný zelený řádek „ottd Decouple by Karel Mácha“. Okno nákupu se
roztahuje podle popisu vybraného auta; dlouhý text verze 5 ho zvětšil a tlačítko „Koupit vozidlo“ vyjelo
z obrazovky, ostatní auta to nedělají (hráč: *„ten zelenej text musí pryč … ottd decouple by karel macha
se vejde“*, *„zelený jen ottd decouple by karel macha“*, *„to hýbalo s velikostí okna a ostatní to nedělali
a schovalo to čudlík koupit“*). Věty o vagónku, motoru, socialismu a zásobách armády zůstaly v popisu GRF
a v licenci. Grafika a náklady jako ve verzi 5.

## Verze 5 (29. 9.) v kostce

Co je jinak proti verzi 4 (podrobnosti v oddílech níž, starší text popisuje verzi 4, kde se liší, platí tohle):

- **Jména:** „Praga V3S Vejtřaska (zelená)“ a „(modrá)“ (hráč: *„vůbec slova army a military … až na konec“*).
  V nákupu je modrá nad zelenou: hra řadí auta jedné sady podle místního čísla a vlastnost 20
  (`sort_purchase_list`) u modré ji přesune **před** zelenou (`CommitVehicleListOrderChanges`). Modrá je
  i v GRF první (hráč: *„musíš mít v GRF nejdřív sprity modrý“*), na pořadí v nákupu to vliv nemá.
- **Co vozí:** všechno z tabulky kromě skla, elektřiny a GEAR. Tekutiny v barevných sudech (hráč: *„prostě
  udělej i tekutiny, barevný sudy a je to“*), chemikálie (`CHEM`, nový kód za MARI, 0xAB) pod plachtou.
  Jen zelená: jídlo, výbušniny a radioaktivní (URAN NUKF NUKW). Jen modrá: hračky. Zelená 168 kódů, modrá 164.
- **Náklad na korbě** (vrstvy, jeden obrázek pro víc nákladů):

  | náklad | obrázek |
  |---|---|
  | sypký (uhlí, ruda, písek s bramborami, kámen …) | kupka v barvě nákladu jako ve verzi 4 |
  | WOOD, TWOD / WDPR | klády / prkna |
  | CMNT cement | pytle (hráč: *„si říkal, že cement dáš do pytlů“*) |
  | GOOD zboží | dřevěné bedny |
  | BEER alkohol | dřevěné sudy |
  | OIL_ OILD OILI PETR RFPR ropa a benzín | modrá černé sudy, zelená šedá plachta (hráč: *„vojenská šedá plachta všechny benzíny, ropu“*) |
  | CTAR dehet | černé sudy |
  | WATR MILK EOIL MOLS voda, mléko, olej, melasa | modré sudy |
  | ACID LYE_ CHLO NH3_ O2__ FUEL chemie a plyny | červené sudy |
  | FICR přadné plodiny | naložené seno (hráč: *„místo plachty seno“*) |
  | LVST dobytek | prasátka, kravičky (česká strakatá) nebo ovečky, podle přestavby |
  | všechno ostatní | plachta (zelená olivová, modrá žlutá, ocel a strojírenství šedá a šedobílá) |

- **Dobytek má tři podtypy** (hráč: *„může se jmenovat V3S prasátka … a na pozadí poběží kód dobytek
  normálně“*, *„další jméno V3S dobytek a kravičky, po přestavbě“*, *„ovce tam jsou“*): v okně přestavby
  „Dobytek (prasátka)“, „(kravičky)“, „(ovečky)“. Callback 0x19 (bit 0x20 masky callbacků u obou dílů)
  vrací text D003 až D005 podle podtypu (proměnná 0xF2, `cargo_subtype`), 0x400 = konec seznamu. Hra
  bere jen podtypy, které vrátí všechny díly, proto má čumák velké stejný callback. Obrázek na korbě
  vybírá switch na 0xF2.
- **Texty:** popis GRF „Carries everything and rides on railway wagons“, půl motoru Tatry 111, bez měřítka
  CZTR (u malé „original size“), zeleně „for ottd Decouple by Karel Mácha“, socialismus, na konci věta
  o zelených ze zásob armády. V nákupu totéž česky.
- **Velikost:** malá 4,18 MB (auta 0,34, náklady 0,54, plachty 0,11, zvuk 3,15), velká 4,53 MB.
- **Ověřeno ve zkušební hře** (`testv3s`, zkušební náklady `hra/zkusebni_naklady/`): každý náklad se
  přestaví a naložený ukáže svůj obrázek, podtypy dobytka mají jména a obrázky v obou dílech, modrá
  nevozí uran, zelená hračky, modrá je v nákupu první. Fotka ze hry: `kontrola/hra_naklady_v5.png`.

Hráč 28. 9.: *„udělej mi vejtřasku, zas uděláme velkou malou“*, *„vojenskou a modrou“*,
*„vojenská tam je, jen ji přebarvi na modro“*, *„komunistickou modrou“*.

| GRF | `grf_id` | měřítko | délka auta | kolona |
|---|---|---|---|---|
| `grf/mala/Praga_V3S_Tatra-v13.grf` | `MAXd` | jako CZTR, 12,2 px/m (zin4) | 7,7 osminy, díl 8/8 | rozestup 8, jako CZTR |
| `grf/velka/Praga_V3S_Tatra_BRYLE-v13.grf` | `MAXe` | BRÝLE, o 20 % větší, 14,64 px/m | 9,25 osminy, díl 8/8 | čumák 2/8, rozestup 10 |

Balík pro hráče je `Praga_V3S_Tatra-v13.zip`: oba GRF a `licence.txt` (licence, převzatý model,
reklama na ottd Decouple s odkazem na itch a „No donations allowed“). Starší balíky
(`Praga_V3S_Vejtraska-v1` až `-v9`, `Praga_V3S_Tatra-v10` až `-v12`) zůstávají v repu.

## Jméno a popis v seznamu GRF

Od verze 2 (hráč 28. 9.: *„ve jménu vynech for, jen žlutě V3S Praga, zeleně ottd Decouple by Karel
Macha“*): `{yellow}V3S Praga{green} ottd Decouple by Karel Macha` a na konci symbol náklaďáku
(`{truck}`) v barvě varianty, měřítko CZTR `{gold}`, BRÝLE `{lt-blue}`. Popis: žluté jméno, zelený
řádek se symboly, řádek varianty v její barvě, `{orange}` informace, model a zvuk, nakonec zeleně
ottd decouple, itch a licence. V textech není „communist“ (hráč: *„nepiš tam comunist blue“*).

## Auta

| | kupované číslo | viditelné auto (jen velká) | nátěr |
|---|---|---|---|
| Praga V3S Vejtřaska (vojenská) | 0x0100 | 0x0110 | model beze změny, olivová |
| Praga V3S Vejtřaska (modrá) | 0x0101 | 0x0111 | modrá, 4 odstíny podle nákladu |

- Uvedení **20. 2. 1952**, první funkční prototyp V3S (Praha-Vysočany). Hra dá v ten den prototyp
  jedné firmě na zkoušku, všem o rok později, jako sériová výroba od dubna 1953. Hra k datu přičte
  náhodně až 511 dní, když hra nezačala dřív než dva roky předtím.
- 60 km/h, 100 k (Tatra 912), 5,5 t, kapacita 10 jednotek. Lidé: vojenská 20 (vojáci na korbě,
  hráč: „hodně“), modrá 3 (kabina). Lidi dělá callback 0x15, pro PASS a od verze 4 i pro turisty
  a dělníky (TOUR OTI1 OTI2 YETI YETY). U velké má callback 0x15
  i čumák (vrátí 1): hra by jeho 1 zboží přepočetla násobkem na 2 lidi a velká ve verzi 1 vezla 21 a 4.
- Vlastní zvuk (níž), cena a provoz mezi Avií A31 a Tatrou 815 z CZTR.
- Na trhu do konce hry (`model_life_years 255`).

### Velká: neviditelný čumák

Stejně jako `CZTR_Truck_SetBRYLE1-clanek.grf` a dvanácettrojky (`auta/CUMAK.md`): kupované číslo
je neviditelný čumák délky 2, drží jméno, cenu a obrázek v nákupu, viditelné auto je druhý článek
délky 8. Rozestup v koloně je 8 + 2 = 10 osmin, auto má 9,25, mezera 0,75 osminy.
Čumák veze 1 jednotku (motor s nulovou kapacitou by přišel o nabídku nákladů), auto zbytek,
u lidí 1 + 2 a 1 + 19. Oba díly mají stejný seznam nákladů. Rychlost, výkon a hmotnost čte hra
jen z čumáku (`RoadVehUpdateCache`, `GetWeight`).

**Článková auta berou jen průjezdné zastávky** (hra: `STR_ERROR_NO_STOP_ARTICULATED_VEHICLE`).
Malá čumák nemá, do zálivu zajede.

## Náklady

Od verze 4 hráčovým systémem (`temata3.md`, „Jak hráč dělá GRF“; hráč: *„já chci, abys používal můj
systém mapování nákladů, ať se v tom yaglu vyznám“*, *„můj systém je jasnej, vidíš hned“*):

- **Překladová tabulka** je celý hráčův vzor `prekladova-tabulka-vzor.yagl` ve stejném pořadí a se
  stejnými čísly (MARI 0x92), i s jeho poznámkami a nadpisy oddílů. Kódy vejtřasky, které ve vzoru
  nejsou, jdou za MARI (0x93 až 0xAA): neznámé labely ze seznamu VW T1 (FARM LVPT HOPS ELEC NODC,
  hráč je má, tak zůstaly) a náklady FIRS 5.2 Steeltown (třeba STIG STSL STBR STPL STSW FEAL PLNT).
  Celkem 171 položek.
- **U každého auta vypsaný seznam, co vozí** (`always_refittable_cargos`), třídy nákladu 0, seznam
  nikdy povolených prázdný, jako VW T1. Nad seznamem je v yaglu poznámka, co auto nevozí. Co
  v seznamu není, auto nevozí v žádné hře.
- **Vozí všechno z tabulky kromě** (hráč: *„napiš všechno vozí“*, *„co nevozí vyjmenuj krom
  tekutin“*, *„alkohol vozíme, pivo v báse“*, *„svařovací materiál a jídlo nech, barvy nech, čisticí
  prostředky taky nech, to není tekutý, ve flaškách“*): tekutin a plynů (OIL_ OILD OILI PETR RFPR FUEL
  CTAR MILK WATR EOIL MOLS ACID LYE_ CHLO NH3_ O2__), skla (GLAS), elektřiny (ELTR) a přeřazení
  lokomotivy (GEAR, není to náklad). Modrá navíc nevozí jídlo a výbušniny (FOOD BOOM, hráč: *„jídlo
  jenom vojenský“*, *„vojenská explosives, modrá ne“*). Vojenská 152 kódů, modrá 150.
- **Marihuana** (MARI, 0x92) je v seznamu jménem, jako v každém normálním GRF (hráč: *„ty děláš
  normální GRF s kódem MARI“*), a má zelenou kupku. Hráčova hra ji do 28. 9. škrtala všem vozidlům
  kromě svých marihuanových náklaďáků; od kolegova commitu `f3f7e7e` (29. 9.) si ji nechá každá sada,
  která má `MARI` v překladové tabulce (`GrfNamesCargo` v `OfferMarijuanaToShipsAndAircraft`), stejně
  jako `ROLA`. Hráč: *„bude to fungovat normálně na kód MARI, standardně všem GRF, mezinárodní wiki
  značka, jako ROLA, my jsme to zavedli“*.
  Moje zkušební hra to pravidlo nemá a vejtřaska se v ní na MARI přestaví (`hra/zkusebni_mari/`).
- Řádek „Lze přestavět na“ v nákupu píše hra sama. Od kolegovy úpravy (`forclaude`, commit `fcbf5c6`,
  29. 9., `GetRefitOptionsString` ve `vehicle_gui.cpp`): všechno → „Všechny druhy nákladu“, chybí nejvýš
  7 → „Všechny kromě …“, jinak víc než 7 → „Skoro všechno vozí“, do 7 nákladů je vyjmenuje. Náklad pro
  auta na vagonech (ROLA) se autu, které auta nevozí, nepočítá jako chybějící. Spočítáno pro verzi 4
  a FIRS 5.2 s vlastními náklady hry (ještě se škrtanou marihuanou): Steeltown „Skoro všechno vozí“ (vojenské
  chybí 8: ACID CHLO CTAR GLAS LYE_ MARI N7__ O2__), ostatní ekonomiky „Všechny kromě …“ (2 až 7,
  tekutiny, sklo, marihuana, u modré jídlo a výbušniny). FIRS má i tekutiny CHEM a N7__, které ve vzoru
  tabulky nejsou; vejtřaska je nevozí, protože v seznamu nejsou.
- FIRS Steeltown má u všech nákladů násobek kapacity 1 (vlastnost 1D), takže V3S vezme 10 jednotek
  čehokoli. Ve hře bez FIRS má zboží násobek 2, tam vezme 10 zboží, ale 5 uhlí.

Verze 1 až 3 měly seznam z VW T1 s přidanými kódy, jen použité kódy v tabulce, a verze 3 k tomu
třídy nákladu (všechno kromě tekutin). S třídami ale nebylo vidět, co auto nevozí (hráč: *„ale
nevíš, co se nevozí“*).

### Odstíny modré

Hráč: *„máme hodně nákladů, tak všechny modrý použijem, míchej to“*: C světloučká stavby,
D tmavá strojírenství, A zboží, B zemědělství. Grafika se volí v Action 3 podle nákladu.

| odstín | lak v texture | náklady |
|---|---|---|
| A | 30, 60, 130 | zboží a všechno, co není v B, C, D (i lidi a pošta, obrázek v nákupu) |
| B | 40, 62, 100 | TATO BEAN SGBT TBCO MARI FICR FMSP SEED OLSD LVST WOOL FRUT JAVA NUTS WOOD, od verze 4 i GRAI WHEA MAIZ CERE FRVG SGCN CASS TWOD FERT |
| C | 60, 90, 130 | CMNT BDMT BRCK CCPR CERA GRVL SAND LIME QLME RBAR STSW, od verze 4 i CLAY KAOL |
| D | 25, 45, 95 | ocel, šrot, ruda, uhlí, koks, železo, struska, motory, díly, stroje, od verze 4 i rudy a kovy (AORE CORE NKOR PORE COPR ZINC NICK ALUM COBL MNO2 FECR URAN SCRP) a vozidla VEHI, 56 kódů |

## Kotva spritů

Konvence VW T1 orig size (`temata3.md`, hráč: *„podle linky mezi koly“*), **zrcadlově srovnaná**
(hráč: *„a zrcadlová verifikace středu“*). Kotva (bod −xoffs, −yoffs) je proti bodu na zemi pod
středem auta vodorovně `10,0 · sin a`, svisle `−20,8 − 0,7 · cos a`, a = 45° · směr. Z proložení
VW T1 zmizely části, které zrcadlové nejsou (konstanta −5 px a `3,8 · cos a`): sever a jih mají
kotvu na ose, SV–SZ, V–Z a JV–JZ jsou zrcadla. Pro S, J, V a Z je to přesně oprava, kterou už
dostaly dvanácettrojky (sever −1, jih −9, východ a západ −5). V jízdních směrech je V3S o 2 px
(SV, SZ) a o 8 px (JV, JZ) jinde než VW T1, protože ten v nich zrcadlový není (otevřené
v `auta/CUMAK.md`).

Střed auta je v půlce délky, ne v půlce rozvoru. V3S má za zadní nápravou dlouhou korbu, střed
rozvoru je o metr blíž k čelu, auto by pak v zastávce i na vagonu stálo o metr dozadu.

### Pruh na silnici CZTR (verze 2)

Hráč 28. 9.: *„jihovýchodní sprite doprava lehce od krajnice“*, *„zarovnej to znova na silnici CZTR“*,
*„nemůže jezdit kolem po prostřední čáře … odstup jako od krajnice, pár pixelů“*. Hra vede auto
v pruhu na 9 (SV, JV) nebo 5 (JZ, SZ) jednotkách dlaždice a kreslí ho na poloha + (−2, −1) (SV, JZ)
nebo (−1, −2) (JV, SZ). Se zrcadlovou kotvou vycházela zem pod středem auta napříč na 10,2 (SV),
11,0 (JV), 7,0 (JZ) a 6,2 (SZ), kdežto střed pruhu mezi bílou krajnicí a prostřední čárou CZTR RT14
(změřeno na spritech silnice) je 10,2, 9,66, 6,33 a 5,79. JV tak jezdil po krajnici a velká JZ po
prostřední čáře. `posun_do_pruhu` v `pack_v3s.py` posune obrázek napříč silnicí do středu pruhu
(JV o 10,6 px doprava a 5,3 nahoru, JZ o 5,2 doleva a 2,6 nahoru, SZ o 3,4 doprava, SV skoro nic),
směry v zatáčkách (S, V, J, Z) napůl mezi sousedy. K tomu hráčovo doladění podle náhledu: JZ o pixel
na jihovýchod (*„maličko pixelík“*, 2 a 1 px). Kola (vnější hrany zadních dvojmontáží, 2,17 m) mají
pak z obou stran odstup asi 3 px (velká) a 5 px (malá) při zin4. Zrcadlová kontrola platí pro
kotvu před posunem, pruhy hry zrcadlové nejsou.

Ověřeno ve zkušební hře na silnici CZTR RT14 ve všech osmi případech (dvě velikosti, čtyři směry):
`kontrola/hra_smery_v2.png`.

Kontroly na rozbaleném GRF (`yagl -d`):
- `kontrola_zrcadla.py`: zrcadlo spritu 8 − k položené podle offsetů na sprite k. Obě velikosti,
  všech 5 sad: sever a jih kotva na ose, dvojice odchylka **0 px**, shoda siluet 0,95 až 1,00.
- `kontrola_vw.py`: vedle VW T1 orig size na společném křížku. V bočním pohledu (vzdálenost od
  krajnice) má V3S linku kol 27 až 28 px pod kotvou, VW T1 27 a 28 px.

## Jak to vzniklo

1. **Model**: `praga-v3s.glb` z releasu `par6` (`zip6/bar/`), zkopírovat do `model/`. Autor
   **hans1240**, „Praga-V3S“, CC BY 4.0,
   https://sketchfab.com/3d-models/praga-v3s-5593b3ca44cb41adb5a1c6ecb81297d3
2. **Nátěr** (`nater_v3s.py`): olivový lak (odstín 36–80°) na modrou se zachováním jasu, tedy stínů,
   špíny a prken. Rez, pneumatiky, sklo, světla a cedulka PRAGA V3S zůstávají.
3. **Focení** (`render_v3s.py`): kamera, HDRI a Cycles jako Sergej, 8 směrů ve stejném měřítku
   (silniční vozidla se na rovné silnici nestlačují), kabina natočená po směru jízdy (kontroluje se).
   `python3 render_v3s.py <vojenska|modra_A..D> <px_na_m> <výstup>`
4. **Balení** (`pack_v3s.py`): `python3 pack_v3s.py <mala|velka> <adresář fotek> grf/<mala|velka>`,
   pak v `grf/<varianta>` `yagl -e Praga_V3S-v4.grf` (nebo `Praga_V3S_BRYLE-v4.grf`). Fotky
   nákladů: `render_v3s.py naklad_<KÓD>` pro každý kód z `VRSTVY` a `naklad_plachta_<barva>` pro
   plachty (vojenska, seda, zluta, sedobila). Zvuky předem
   `python3 zvuky/syntetizuj_zvuky.py` (bez `zvuky/zvuky.json` se GRF zabalí bez zvuku).
5. **Zkouška ve hře** (`hra/`, moje kopie hry, ne forclaude): příkaz `testv3s` koupí každé auto
   z GRF, přestaví ho na náklady a vypíše články, délky, kapacity a sprity. Ověřeno: načte se bez
   chyby, velká čumák 2 + auto 8, malá 8, lidi 3 a 20, zboží 10, modrá má jiný sprite pro ocel,
   uhlí a rudu (D), dobytek (B) a zboží a poštu (A). Příkaz `testv3sfoto` nechá V3S jezdit po okruhu
   s původními náklaďáky hry a vyfotí to: V3S jedou ve stejném pruhu jako původní náklaďáky
   (`kontrola/hra_kolona.png`, `kontrola/hra_detail.png`). Malá těsně za velkou se překryje asi
   o půl osminy (velká je delší, čumák chrání jen její čelo), stane se jen při míchání velikostí.

Na silnici CZTR RT14 „1. třída – venkov“ (hráč: *„fotit s CZTR silnicí“*) jede V3S ve svém
pruhu mezi středovou přerušovanou čárou a krajnicí a nepřejíždí ani jednu (`kontrola/hra_cztr_silnice.png`).

Obrázky v `kontrola/`: `porovnani_vw.png` (srovnání s VW T1 na společném křížku), `vyber_modre.png`
(odstíny A až D, jak si je hráč vybral), `hra_*.png` (fotky ze zkušební hry), `hra_smery_v2.png`
(verze 2 na silnici CZTR, všechny směry).

## Okna a reflektory (verze 3)

Hráč: *„nemáš lepší okna? U vojenský mi to ani nevadí, ale ta modrá, to vůbec nesedí šedý okna“*,
*„světla bíle bílý“*. Materiál skla (`v3s_glass__da__spec`, textura `Image_3`) má model
neprůhledný a matný (drsnost 0,9) a skla v textuře šedá, pod světlou oblohou HDRI vycházela šedá
a placatá. `render_v3s.py` (proměnná `OKNA`, výchozí `tmave`) přebarví skla v textuře na tmavou
(0,030, 0,040, 0,055 lineárně), materiál dá lesklý (drsnost 0,15) a reflektor v téže textuře
(kruh v pravém dolním rohu, kde jsou i odrazka, blinkr a zadní světlo) zesvětlí a nechá svítit
(emise 1,5 tam, kde je textura skoro bílá). `OKNA=puvodni` vrátí model, jak byl. Hráč vybíral ze
čtyř variant (šedá, tmavá lesklá, tmavá matnější, modravá).

## Náklad jako vrstva (verze 3, plachta od verze 4)

Hra umí kreslit vozidlo z až osmi obrázků přes sebe, když má vlastnost `miscellaneous_flags` bit 7
(`SpriteStack`). Grafický řetěz se prochází pro každou vrstvu zvlášť, číslo vrstvy je v proměnné
0x10 (bity 8–15), a když má přijít další vrstva, zapíše GRF do dočasného registru 0x100 bit 31
(`GetCustomEngineSprite` v `newgrf_engine.cpp`; registry se před každou vrstvou nulují). Vrstva 0
je auto (u modré v odstínu podle nákladu), vrstva 1 náklad. Switch `vrstvy <kód>` spočítá
`(1 − vrstva) << 31`, uloží do registru 0x100 (`TempStore`) a podle vrstvy vybere auto nebo
náklad. Náklad je vidět od poloviny nákladu (hra bere sadu naklad · počet / kapacita).

Fotky nákladu: `render_v3s.py naklad_<KÓD>` nafotí jen náklad, auto je neviditelné, ale zakrývá,
co je za bočnicemi (`is_holdout`). Stejná vrstva pak jde na vojenskou i všechny odstíny modré,
v GRF je jednou (skupiny 0xC0 a dál), auto má switche od 0x10.

| náklad | vrstva |
|---|---|
| COAL uhlí | černá hromada, lesklejší |
| COKE koks, SLAG struska | tmavě šedá |
| IORE železná ruda, SCMT šrot | rezavě hnědá (šrot hrubší) |
| LIME vápenec, QLME pálené vápno | světle šedá, bílá |
| GRVL kámen | šedá (cement jel ve verzi 4 s ní, od verze 5 je pod plachtou, hráč: *„ten cement je venku, není v pytlích nebo pod plachtou“*) |
| SAND písek, TATO brambory, BEAN | žlutá, jemná (brambory od verze 4, hráč: *„písek a brambory žlutá“*; BEAN má CZIS přejmenované na brambory) |
| SGBT cukrová řepa | béžová, hrudkovitá |
| SEED osivo, NUTS ořechy, OLSD olejniny | zlatá, světle hnědá, tmavě hnědá |
| MARI marihuana | zelená |
| SULP síra | žlutá |
| WOOD dřevo, TWOD tropické dřevo | klády ve třech vrstvách, kůra a světlá čela |
| WDPR dřevařské výrobky | hranice prken |
| všechno ostatní | plachta (níž) |

Jeden obrázek slouží víc nákladům, obrázek navíc tedy nestojí žádné megabajty (hráč: *„já chci tu
kupičku přikládací, ať ušetříme megabajty na spritech celých aut, jen kupička je míň MB“*).
V GRF je 17 obrázků kupek a klád a 4 plachty, každý v 8 směrech. Malá (3,93 MB): auta 0,34 MB, kupky
a klády 0,29 MB, plachty 0,11 MB, zvuk 3,15 MB; velká (4,19 MB): auta 0,47, kupky 0,39, plachty 0,15,
zvuk 3,15 MB. Megabajty dělá hlavně zvuk.

### Plachta (verze 4)

Hráč: *„co není kupka, nech grafiku prázdné. Uděláme přikládací plachtu. Grafika stovky aut plný
jednou plachtou. Když pojede plná, přiložíme plachtu“*, *„jídlo plachta“*, *„vojenský vojenskou
plachtu, a šedou“*, *„modrý žlutou šedobílou plachtu“*, *„šedou dáme u vojenský na ocelové řetězce,
strojírenství“*, *„moc hezký plachty“*.

`render_v3s.py naklad_plachta_<barva>`: plátno přes korbu, boky svisle od horní hrany bočnic kousek
dolů, střecha 2,92 m nad zemí (výška V3S s plachtou, kabina má 2,46 m), podélné hrany zaoblené jako
oblouky. Model má na korbě klanice s horním madlem (do 1,29 m nad podlahou modelu), plachta je těsně
přes ně. Auto je při focení neviditelné, ale zakrývá, co je před plachtou (kabinu).

| auto | plachta | náklady |
|---|---|---|
| vojenská | olivová | všechno, co není kupka, kromě oceli a strojírenství; i vojáci |
| vojenská | šedá | ocel a strojírenství (odstín D) |
| modrá | žlutá | všechno, co není kupka, kromě oceli a strojírenství; lidé sedí v kabině, plachtu nemají |
| modrá | šedobílá | ocel a strojírenství (odstín D) |

Plachta je vidět od poloviny nákladu, stejně jako kupka. Ve zkušební hře: `kontrola/hra_naklady_v4.png`.

Dřevo (WOOD) vejtřaska ve verzi 2 nevozila, od verze 3 ho má obě auta (modrá v odstínu B).

## Zvuk (verze 2)

Hráč: *„to bude troubit a vrčet jak vejtřaska“*, *„musíš si poslechnout originál V3S jako vzor
a udělat umělý zvuk, jak se rozjíždí“*. Videa s V3S (YouTube, Facebook) nemají volnou licenci,
proto je zvuk umělý: `zvuky/syntetizuj_zvuky.py` ho skládá z toho, jak motor Tatra 912 funguje
(šest ran výfuku za dvě otáčky, klepání dieselu, ventilátor, dunění cyklu, mechanika rozvodu,
kvílení převodovky, drnčení kabiny a korby). Hráč pak poslal nahrávku V3S z inzerátu; ta posloužila
jen k rozboru (v repu ani v GRF není): vytúrování na 1880 ot./min, čáry po otáčky / 120 stejně silné
jako zapalovací (nestejné válce), pískání na 38,4, 60,8 a 91,2násobku otáček, průměrná barva po
třetinách oktávy. Podle toho je syntéza vyladěná (barva v průměru 1,2 dB od vzoru).

| událost (callback 0x33) | kdy | zvuk |
|---|---|---|
| 1, auto ještě schované v depu (var 0xB2 bit 0) | výjezd z depa | startér, motor chytne, klakson „tú-túú“ (dvoutónový 352 a 440 Hz jako Tatra 148), plyn |
| 1, jinak | odjezd ze zastávky | rozjezd: plyn, spojka, řev v jedničce do 1880 ot./min, přeřazení |
| 7 | za jízdy po 16 tících | kousek podle rychlosti (do 15, 30, 45, nad 45 km/h; var 0xB4 je v polovinách km/h), jeden za 112 tiků |
| 8 | ve stání | volnoběh |
| ostatní | porucha … | výchozí zvuk hry |

Hlasitost jako Sergej: jízda −10,5 až −9 LUFS, volnoběh −12, rozjezd a výjezd −7,5. U malé jde
callback přes Action 3 podle nákladu, tak každý cíl grafiky dostal obal „zvuk, jinak grafika“,
u velké stačí čumák. Hráč: *„od 0:26 super“*; na nízkých otáčkách vadily vysoké tóny (pískání,
ventilátor, cinkání plechů a zvonění filtru barvy), pod 700 ot./min je proto barva vyhlazená.
Ověřeno ve zkušební hře (`testv3s` vypíše, co callback vrátí): depo 0x4A, zastávka 0x49, pásma
podle rychlosti, stání, porucha výchozí, mimo takt ticho. `zvuky/poslech.mp3` hraje, jak to zní ve hře.

Verze (`VERZE` v `pack_v3s.py`, je ve jménu souboru i v Action14): 1 první vydání; 2 jméno „V3S Praga“
bez „for“, texty bez „communist“, zelená kupka na MARI, pruhy na silnici CZTR, umělý zvuk s klaksonem,
velká veze správně 20 a 3 lidi; 3 tmavá lesklá okna a bílé reflektory, náklad jako přikládací vrstva
(18 nákladů), dřevo v seznamu nákladů; 4 náklady hráčovým systémem (celá tabulka ze vzoru, vypsaný
seznam, bez tříd), brambory žluté, cement šedý, přikládací plachta na všechno, co není kupka; 5 tekutiny
v barevných sudech, chemikálie, pytle, bedny, sudy, seno, dobytek jako prasátka, kravičky nebo ovečky,
zelená místo vojenské, modrá v nákupu první, nové texty; 6 v nákupu jen zelený řádek ottd Decouple;
7 v nákupu „for ottd Decouple by Karel Mácha“ a autor modelu, bílé a hnědé pytle s černou čarou, bedny
i na zásoby, obilí, rudy a jíl jako kupky, bílé sudy místo modrých, podtypy přadných plodin;
8 vzorová tabulka 220 kódů, studenti, vězni a dělníci, cihly, brambory, ovoce, rum a piva, víno, chmel;
9 vojenská technika jen zelená, FREE mezi nevozí; 10 Tatry ve stejném GRF; 11 zelená Tatra schovaná, jen pro naši hru;
12 naše brambory BRAM (kupa a pytle), fazole BEAN v hnědých pytlích; 13 studentky na korbě.
