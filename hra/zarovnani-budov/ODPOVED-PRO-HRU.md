# Odpověď pro hru (1. 10.)

Díky, zpráva je jasná.

- **JSON s rohy pozemku** budu dělat u každé budovy jako dosud. Socha Karla Máchy (`socha/`, 1 × 1, kamenná
  a bronzová) ho má.
- **Socha po stažení na 124/128 nepřečuhuje:** pod přední hranou ani do stran z ní nic neleží (změřeno na
  staženém obrázku). Jen okraj stínu přesahuje nejvýš o 1 px v přiblížení 4× s alfou 4 z 255, tedy neviditelně.
  Stín má socha jen 20 % černé (hráč chtěl mnohem méně stínů), automat a gymnázium 55 %.
- **Posunutý náhled byla moje chyba.** V náhledech jsem nepočítal s tím, že země v okruhu zkušební hry leží ve
  výšce 16, takže jsem všechno vkládal o 64 px (půl políčka) níž. Opraveno: náhledy gymnázia, automatu i sochy
  jsou nové a dělá je `hra/nahled_ve_hre.py` (výška země, stažení na 124/128 a severní roh +4 px jako u vás).
- **Objekty:** hráč je teď dělá. Přidám je do obrázků a hotové pošlu ve tvaru hry (`*_stazeny.png`, stažené na
  124/128 stejně jako vaše verze) s JSONem `"stazeny": true`.

## Animace sochy a licence (1. 10.)

Hráč: *„uděláme animaci, tahle socha bez objektů se bude střídat s obrázkem s objekty“* a *„licence střádat
a předat do forclaude“*.

- **Dva obrázky na sochu**, které se střídají: `socha/socha_kamen_zin4.png` a `socha/socha_kamen_postavy_zin4.png`,
  bronzová stejně (`socha_bronz_…`). Kamera, rohy pozemku i JSON jsou u obou stejné, liší se jen tam, kde jsou
  postavy (jinde jsou pixely shodné, takže to nebliká). Nic nepřečuhuje pod přední hranu ani do stran.
  Ukázka střídání ve fotce ze hry: `socha/animace_ve_hre.gif`.
- **Licence:** na obrázku s postavami je pět cizích modelů dívek (Sketchfab, CC BY 4.0). Autory, odkazy a hotový
  text uvedení pro hru máte v `AUTORI-MODELU.md` v oddílu „Postavy u sochy Karla Máchy“. Prosím vezměte ho do hry
  spolu s obrázky (do titulků nebo k licencím grafiky, jak to u vás je). Budovy samotné jsou vlastní modely.
- **Další na řadě:** automat a gymnázium, také s druhým obrázkem pro animaci. Udělám je stejně z 3D scény
  (ne vkládáním do staženého obrázku), takže to budou zase rendery 256 × 128 s rohy v JSONu bez `"stazeny"`.

## Socha znovu (1. 10. odpoledne)

Obrázky sochy jsou nové, oba páry (bez dívek a s dívkami, kamenná i bronzová): joint hoří (popel a kouř), kolem
dlažby je tmavě zelený pás keřů a jsou tam rostliny marihuany, velké vzadu za lavičkami až 5 m. Velké rostliny lezou
jen nahoru (nejvyšší pixel je 28 px od horního okraje obrázku po stažení), pod přední hranu ani do stran nic. Rohy
pozemku v JSONu zůstaly stejné. Text uvedení autorů v `AUTORI-MODELU.md` má nově i dvě rostliny marihuany.

## Zastávka, auta a brambory (1. 10. večer)

Rozhodnutí hráče, která se týkají hry:

- **Dívky na zastávce** (`zastavka/README.md`):
  - jsou tam **jen když na zastávce čekají cestující** (*„jo bude tam jen když budou cestující“*);
  - velikost 2× jako budovy;
  - podél X dvě (druhá je jen tmavovlasá College Girl), podél Y jedna;
  - obrázky a posuny od severního rohu dlaždice jsou v README.
- **Holky u dveří aut** jsou hotové v GRF dodávek (`auta/dodavky_BRYLE_v5.grf`) a ve hře se nic měnit nemusí:
  - kreslí je samo GRF jako další obrázek přes auto (sprite stack), když auto na zastávce nakládá;
  - týká se TAZ 1203 a TAZ 1500 busů a Pajdy karavanu;
  - popis je v `holky-u-aut/README.md`.

  Na původních zastávkách hry je u bližšího pruhu schová zadní stěna přístřešku. Hráč to tak chce nechat (*„radši
  předělám původní zastávku než holky“*).
- **Nový náklad BRAM** (naše brambory, hráč: *„uděláme si svoje brambory“*):
  - kód je na konci vzorové tabulky (`prekladova-tabulka-vzor.yagl`, slot 0xDC);
  - vozí ho V3S a Tatry v12 (kupa a pytle), valník brambor a dodávky v5;
  - fazole BEAN jsou nově v hnědých pytlích.

  Aby BRAM ve hře existoval, musí ho nadefinovat průmysl (Action 0 feature 0B, label BRAM).

## Automat a gymnázium s holkami (1. 10. večer)

Hráč: *„spawnem holky kolem školy a automatu“*. Jsou to druhé obrázky do animace jako u sochy:

| budova | bez holek (to, co už máte) | s holkami (nový) |
|---|---|---|
| automat | `automat/automat_zin4.png` | `automat/automat_postavy_zin4.png` |
| gymnázium | `gymnazium/gymnazium_zin4.png` | `gymnazium/gymnazium_postavy_zin4.png` |

- **Obrázky bez holek se nezměnily.** Nové jsou ze stejné scény, stejně velké (384 × 384 a 720 × 720) a rohy v JSONu
  mají stejné. Jsou to zase rendery s políčkem 256 × 128, bez `"stazeny"`, takže je `openttd_gymnazium.py` stáhne
  a rozkrájí stejně jako první.
- **Liší se jen tam, kde jsou holky**, jejich stíny a u školy pár odlesků v oknech. Jinde jsou pixely shodné, takže
  při střídání nic nebliká.
- **Nic nepřečuhuje:** pod přední hrany ani do stran nic nepřibylo (změřeno: mimo kosočtverec pozemku jsou stejné
  pixely jako bez holek).
- **U gymnázia se mění jen pruhy `w` (hřiště) a `s`.** Pruh `e` je v obou obrázcích stejný.
- **Holky:** u automatu tři, dvakrát větší jako automat. U školy sedm ve skutečné velikosti jako budova. Kde jsou, je
  v README obou budov. Ukázka střídání ve fotce ze hry: `gymnazium/animace_ve_hre.gif` (0,9 s na snímek, jen
  náhled, rychlost ve hře je na vás).
- **Licence:** v `AUTORI-MODELU.md` je nový oddíl „Postavy u automatu a gymnázia“ s hotovým textem uvedení pro hru
  (čtyři dívky ze Sketchfabu, CC BY 4.0). Prosím vezměte ho do hry spolu s obrázky.
- **Váš náklad STUD** (`efec273`): studentky na korbě V3S a Tater v13 hledají náklad podle štítku STUD, takže by se
  měly ukázat i s vaším nákladem. Ve hře s průmyslem to ještě vyzkoušené není, hráč to projede, až bude build hotový.

## Marihuanová plantáž a políčko brambor (1. 10. večer)

Hráč: *„uděláme pole marihuany 4x5 a políčko brambor 3x3“*, *„obrázek nahradí marihuanovou plantáž“*, *„to bude
první fáze růstu na marihuanovým poli a druhá fáze udělej ty špičatý smrčky vysoký“*, u brambor *„to stačí tenhle
jeden obrázek bez fází růstu“*. Obrázky jsou v `pole/`, popis v `pole/README.md`.

| obrázek | políček (x × y) | velikost | rohy: sever, východ, západ, jih |
|---|---|---|---|
| `pole/pole_marihuany_faze1_zin4.png` | 5 × 4 | 1216 × 704 | (672, 96), (1184, 352), (32, 416), (544, 672) |
| `pole/pole_marihuany_faze2_zin4.png` | 5 × 4 | 1216 × 704 | stejné |
| `pole/pole_brambor_zin4.png` | 3 × 3 | 832 × 512 | (416, 96), (800, 288), (32, 288), (416, 480) |

- **Plantáž je na rozložení vaší plantáže**, tedy ovocné plantáže základní grafiky (`_tile_table_fruit_plantation_0`:
  x 0 až 4, y 0 až 3). Hráč chce, aby obrázek nahradil její grafiku.
- **Dvě fáze růstu plantáže:** keře, pak vysoké špičaté rostliny. Rostliny stojí v obou fázích na stejných místech,
  kůlna, cesta a záhony jsou stejné. Jak fáze použít (třeba jako růst polí u farmy), je na vás.
- **Brambory** jsou obrázek pro průmysl s nákladem BRAM (ten zatím ve hře není, viz výš).
- **Jako gymnázium:** rendery s políčkem 256 × 128, bez `"stazeny"`, severní roh na celém pixelu dělitelném 4. JSON
  má navíc `policek` a `obrazek` (šířka, výška), protože obrázky nejsou čtvercové.
- **Země:** pole je neprůhledné (zemina, záhony, cesta). Jen 25 cm u hran pozemku je průhledno, tam bude tráva hry.
- **Nic nepřečuhuje** pod přední hrany ani do stran, rostliny jsou celé uvnitř pozemku a lezou jen nahoru. Změřeno:
  mimo kosočtverec pozemku je jen pár pixelů okraje stínu s alfou nejvýš 8 z 255, tedy neviditelně.
- **Licence:** rostliny na plantáži jsou modely ze Sketchfabu (CC BY 4.0). Text uvedení je v `AUTORI-MODELU.md`
  v oddílu „Rostliny na marihuanové plantáži“. Brambory jsou celé vlastní.

## K opravě políčka, škola znovu, zlato dvakrát (1. 10. noc)

- **Políčko 256 × 128:** díky za opravu. `hra/nahled_ve_hre.py` už nestahuje, výška země a severní roh +4 px zůstaly.
  Náhledy gymnázia, automatu, sochy a polí jsou udělané znovu.
- **Gymnázium, oba obrázky znovu.** Hráč: *„škola zvětšit studentky, zvětšíme i lavičky, dveře do školy jsou velké
  dost“*.
  - Holky i všech šest laviček jsou 1,5× větší než budova. Holka měří 2,43 až 2,52 m, dveře mají 2,55 m.
  - Změnily se `gymnazium/gymnazium_zin4.png` (větší lavičky) i `gymnazium/gymnazium_postavy_zin4.png`. Prosím
    rozkrájet znovu.
  - Rohy v JSONu jsou stejné a nic nepřečuhuje.
- **Zlato je ve hře dvakrát se stejným kódem GOLD** (oba výpisy `prum` od hráče):
  - slot 10 je zlato ECS Town vector, slot 117 vlastní zlato hry (zlatý důl a banka hry);
  - GRF ho podle kódu najde jen jednou, tedy zlato ECS;
  - naše V3S a Tatry od v14 berou i druhé zlato přes třídu cennosti, jiné GRF (vlaky a podobně) ho nevezmou.

  Podle komentáře v `newgrf_act0_cargo.cpp` si má sada zlato hry vzít za své. U ECS Town vector to nevyšlo, možná
  proto, že zlato má v pevném slotu. Hráč: *„to zlato dvakrát“*. Jen dávám vědět, ve hře nic neměníme.
- **ROLA do vzorové tabulky nedáváme.** Hráč: *„rola je speciální náklad, to nedávej do tabulky“*. Jinak má tabulka
  všechny kódy z obou her.
- **V3S a Tatry v14** (`v3s/Praga_V3S_Tatra-v14.zip`), hra nic měnit nemusí:
  - se STUD studentky za jízdy sedí na lavicích, při nakládání stojí;
  - zlato vozí jen zelené (pod plachtou);
  - cennosti a diamanty nevozí žádné, hráč na ně udělá Avii VB;
  - odpad jede na šedé kupě.
- **Dodávky v6** (`auta/dodavky_BRYLE_v6.grf`): kovy pod plachtou, odpad na valníku s kamennou kupou.

## Gymnázium: černá místa u schodů a stromy (2. 10. večer)

Hráč podle fotky z vaší hry: *„schody jsou dobře napasované, chybí jim bok a dlažba na konci. ta černá místa“* a
*„dva stromy vedle budovy maj vysoko koruny nad kmenem, je to tyčka ze země, mezera a koruna“*.

- **Krájení je v pořádku**, chyba byla v našem obrázku: plochy přes sebe ve stejné rovině vyšly v renderu černé (bok
  schodů a pruh dlažby před nimi). Opraveno v modelu, stromy mají kmen až do koruny.
- **Změnily se všechny čtyři obrázky:** `gymnazium/gymnazium_zin4.png`, `gymnazium/gymnazium_postavy_zin4.png`,
  `gymnazium/gymnazium_zin8.png`, `gymnazium/gymnazium_postavy_zin8.png`. Prosím rozkrájet znovu (4× i 8×).
- Rohy v JSONu jsou stejné, velikost obrázků taky, 8× je přesně dvojnásobek 4×. Holky jsou na stejných místech.

## Chatka s přikládacími holkami (3. 10.)

Hráč: *„okolo domku lavičky velké jak u sochy, nepořádek, nízké smrčky marihuany místo plotu, sem tam díra. přikládací
holky stojící a pak přikádací holky sedící. takže bude obrázek bez holek a dva s holkama přiloženejma“*, *„velikost
1 políčko … muže to být přes dvě políčka nebo přes čtyři políčka, to je jedno. ale holky přikládací ať ušetříme Mb“*.
Obrázky jsou v `chatka/`, popis v `chatka/README.md`.

| obrázek | co to je | velikost 4× (8×) |
|---|---|---|
| `chatka/chatka_zin4.png`, `chatka/chatka_zin8.png` | chatka bez holek | 400 × 360 (800 × 720) |
| `chatka/chatka_stojici_zin4.png`, `…_zin8.png` | přikládací vrstva: stojící holky | stejná |
| `chatka/chatka_sedici_zin4.png`, `…_zin8.png` | přikládací vrstva: sedící holky | stejná |

- **Pozemek 2 × 1 políčko:** 2 políčka podél x, 1 podél y. Zadní políčko (u severního rohu) je domek, přední dvorek.
  JSON má `policek: [2, 1]`.
- **Rohy ve 4×:** sever (264, 160), východ (392, 224), západ (8, 288), jih (136, 352); v 8× přesně dvojnásobek.
  Render 2 : 1, políčko 256 × 128, severní roh na celém pixelu dělitelném 4, bez `"stazeny"`, jako gymnázium a pole.
- **Přikládací vrstvy:** stejná velikost a rohy jako obrázek bez holek, jinde průhledné. Co holky zakrývá domek,
  lavička nebo rostlina, je už vyříznuté, takže se vrstva kreslí jen navrch obrázku s domkem (rozkrájet ji stejně
  jako obrázek s domkem). Holky nemají stín. Kde holky ve vrstvě jsou, říká `holky_obdelnik` v JSONu (vlevo, nahoře,
  vpravo, dole), kdybyste chtěli vrstvu oříznout: ve 4× stojící [108, 209, 240, 300], sedící [75, 234, 219, 281].
  Holky jsou na dvorku (předním políčku), jedna stojící na zadním políčku před zdí domku.
- **Kdy která vrstva**, je na vás a na hráči (třeba stojící, když přijíždí bus, sedící jindy). Hráč chce hlavně holku
  od kufru 1203 busu: *„když ji povezem tak tam pak musí být někde“*. Ta je v obou vrstvách (College Girl).
- **Nic nepřečuhuje:** vrstvy nemají mimo pozemek ani pixel, obrázek s domkem jen okraj stínu s alfou nejvýš 9 z 255.
- **Licence:** domek „A little happy hut“ (Tigran Safaryan) a holky a rostliny ze Sketchfabu, vše CC BY 4.0. Text
  uvedení je v `AUTORI-MODELU.md` v oddílu „Chatka“. Prosím vezměte ho do hry spolu s obrázky.

## Gymnázium: méně stínů (3. 10.)

Hráč: *„to jsou stíny, dáváš hodně stínů, už nefotíme tatru 148.“* Gymnázium bylo nasvícené jako Tatra (silné stíny),
teď je měkce jako socha (stín na trávu 20 % místo 55 %, tmavé kouty u schodů zmizely).

- **Změnily se zase všechny čtyři obrázky:** `gymnazium/gymnazium_zin4.png`, `gymnazium/gymnazium_postavy_zin4.png`,
  `gymnazium/gymnazium_zin8.png`, `gymnazium/gymnazium_postavy_zin8.png`. Prosím rozkrájet znovu (4× i 8×).
- Rohy v JSONu, velikost obrázků i místa holek jsou stejné, 8× je přesně dvojnásobek 4×.

## Chatka: třetí stojící holka a otočená Galaxia (3. 10.)

Hráč: *„otoč tu holku čelem vzad. na západní lavičce“*, *„ještě jednu mužeš dát na obrázek kde stojí na druhé políčko
k domku za severovýchodní lavičku ke dveřím domku“*, *„před popínavý rostliny na zdi ji postav“*.

- **Změnily se jen vrstvy s holkami:** `chatka/chatka_stojici_zin4.png`, `chatka/chatka_stojici_zin8.png`,
  `chatka/chatka_sedici_zin4.png`, `chatka/chatka_sedici_zin8.png` (a jejich `holky_obdelnik` v JSONu). Obrázek
  s domkem je bit po bitu stejný, rohy i velikost taky.
- Ve stojící vrstvě přibyla Galaxia na zadním políčku před zdí domku (popínavé rostliny vpravo od dveří), v sedící
  vrstvě sedí Galaxia na západní lavičce čelem k dvorku (předtím seděla čelem k opěradlu).

## Chatka: menší domek s kytkami, jiné rohy (3. 10.)

Hráč: *„teď zmenši domek a na ušetřeném místě vysázej kytky okolo. za domek kytky nesázej, domek i s holkou u dveří
posunem směrem od lavičky na ušetřené místo. ke zdi dej jinou ne tu colege, dej tam tu co chodí na jihozapadu“*.

- **Změnilo se všech šest obrázků chatky** (`chatka/chatka_zin4.png`, `chatka_stojici_zin4.png`,
  `chatka_sedici_zin4.png` a totéž `_zin8`). Prosím rozkrájet znovu.
- **Obrázek je nižší a rohy jsou jinde:** 400 × 320 (8× 800 × 640), rohy ve 4× sever (264, 120), východ (392, 184),
  západ (8, 248), jih (136, 312), v 8× dvojnásobek. Pozemek je pořád 2 × 1 políčko, jen domek je menší.
- Domek je zmenšený na tři čtvrtiny a stojí v severním rohu zadního políčka, kolem něj vpředu jsou rostliny
  marihuany. U zdi domku stojí holka v tyrkysovém tílku (Character Girl), Galaxia je místo ní u branky.
- `holky_obdelnik` ve 4×: stojící [110, 150, 245, 259], sedící [75, 194, 219, 241]. Nic nepřečuhuje.
