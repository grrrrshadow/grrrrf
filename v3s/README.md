# V3S Vejtřaska: Praga V3S jako vlastní GRF

Hráč 28. 9.: *„udělej mi vejtřasku, zas uděláme velkou malou“*, *„vojenskou a modrou“*,
*„vojenská tam je, jen ji přebarvi na modro“*, *„komunistickou modrou“*.

| GRF | `grf_id` | měřítko | délka auta | kolona |
|---|---|---|---|---|
| `grf/mala/Praga_V3S-v3.grf` | `MAXd` | jako CZTR, 12,2 px/m (zin4) | 7,7 osminy, díl 8/8 | rozestup 8, jako CZTR |
| `grf/velka/Praga_V3S_BRYLE-v3.grf` | `MAXe` | BRÝLE, o 20 % větší, 14,64 px/m | 9,25 osminy, díl 8/8 | čumák 2/8, rozestup 10 |

Balík pro hráče je `Praga_V3S_Vejtraska-v3.zip`: oba GRF a `licence.txt` (licence, převzatý model,
reklama na ottd Decouple s odkazem na itch a „No donations allowed“). Starší verze (`-v1`, `-v2`)
zůstávají v repu.

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
  hráč: „hodně“), modrá 3 (kabina). Lidi dělá callback 0x15, jen pro PASS. U velké má callback 0x15
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

Hráč: *„VW T1 vozí všechno, tam se inspiruj“*, *„skoro všechno“*. Seznamem, bez tříd, jak to
hráč dělá (`temata3.md`, „Jak hráč dělá GRF“).

- **Základ:** seznam VW T1 (0x0082, 71 kódů s MARI), bez GLAS (*„stavební materiály všechny
  kódy kromě skla“*) a bez FOOD.
- **Přidáno:** šrot a ocel (SCMT STEL STAL STST STSE STSH METL a z FIRS Steeltown STIG STSL STBR
  STPL STSW), železný řetězec Steeltownu (IORE COAL COKE LIME QLME IRON SLAG FEAL CSTI VBOD PLNT),
  řepa SGBT, konopná vlákna FICR, stavební GRVL SAND.
- **Jen vojenská:** FOOD (*„jídlo jenom vojenský“*) a BOOM (*„vojenská explosives, modrá ne“*).
- Modrá 96 kódů, vojenská 98. Pivo, tabák, marihuana a cigára (BEER TBCO MARI CIGR) vozí obě.
- **Od verze 3 vozí všechno kromě tekutin** (hráč: *„napiš všechno vozí“*, *„co nevozí vyjmenuj krom
  tekutin“*, *„alkohol vozíme, pivo v báse“*): třídy nákladu všechny kromě tekutin (0x0040)
  a zvláštních (0x8000, auta na ROLU), k tomu seznam výš (i pivo, barvy, čistidla a svařovací
  materiál, které FIRS značí jako tekutiny), přidaná síra a kaučuk (obojí se vozí i pevné) a zakázané
  sklo, u modré i jídlo a výbušniny. Hra v okně nákupu píše krátce „vše kromě …“, jen když chybí
  nejvýš 7 nákladů (`ShowRefitOptionsList` ve `vehicle_gui.cpp`). Ve FIRS 5.2 Steeltown s náklady
  hry chybí vojenské 6 (kyselina, dehet, sklo, louh, marihuana, auta na ROLU), modré 8 (navíc jídlo
  a výbušniny), takže modrá tam ukáže dlouhý seznam; až hra pustí marihuanu, bude jich 7.
- **Náklad na korbě jako přikládací vrstva** (od verze 3, hráč: *„kupku přikládací, uděláme
  černou kupku uhlí a žlutou písek a všechny barvy a dřevo udělej“*), popsané níž. Marihuana je
  zelená kupka (ve verzi 2 celé auto s kupkou, hráč: *„udělej tam zelenou kupičku náklad“*).
  Hra ale MARI škrtá všem vozidlům kromě svých marihuanových náklaďáků (`OfferMarijuanaToShipsAndAircraft`),
  takže se na ni V3S zatím přestavět nedá; pro kolegu `PRO-HRU.md`, bod 4. Zkoušeno se zkušebním
  nákladem `hra/zkusebni_mari/`.
- Jména kódů z `naklady.md` a z FIRS 5.2 (`rozbalene/firs-5.2.0`), nic domyšleného. Neznámé
  labely z VW T1 (FARM LVPT HOPS ELEC NODC) zůstaly, jak je hráč má.
- Překladová tabulka: jen použité kódy v pořadí z `prekladova-tabulka-vzor.yagl`, co ve vzoru
  není, jde za MARI (98 položek).
- FIRS Steeltown má u všech 62 nákladů násobek kapacity 1 (vlastnost 1D), takže V3S vezme
  10 jednotek čehokoli. Ve hře bez FIRS má zboží násobek 2, tam vezme 10 zboží, ale 5 uhlí.

### Odstíny modré

Hráč: *„máme hodně nákladů, tak všechny modrý použijem, míchej to“*: C světloučká stavby,
D tmavá strojírenství, A zboží, B zemědělství. Grafika se volí v Action 3 podle nákladu.

| odstín | lak v texture | náklady |
|---|---|---|
| A | 30, 60, 130 | zboží a všechno, co není v B, C, D (i lidi a pošta, obrázek v nákupu) |
| B | 40, 62, 100 | TATO BEAN SGBT TBCO MARI FICR FMSP SEED OLSD LVST WOOL FRUT JAVA NUTS |
| C | 60, 90, 130 | CMNT BDMT BRCK CCPR CERA GRVL SAND LIME QLME RBAR STSW |
| D | 25, 45, 95 | ocel, šrot, ruda, uhlí, koks, železo, struska, motory, díly, stroje (40 kódů) |

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
   pak v `grf/<varianta>` `yagl -e Praga_V3S-v3.grf` (nebo `Praga_V3S_BRYLE-v3.grf`). Fotky
   nákladů: `render_v3s.py naklad_<KÓD>` pro každý kód z `VRSTVY`. Zvuky předem
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

## Náklad jako vrstva (verze 3)

Hra umí kreslit vozidlo z až čtyř obrázků přes sebe, když má vlastnost `miscellaneous_flags` bit 7
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
| GRVL kámen | šedá |
| SAND písek | žlutá, jemná |
| TATO brambory, SGBT cukrová řepa | hnědá a béžová, hrudkovitá |
| SEED osivo, BEAN fazole, NUTS ořechy, OLSD olejniny | zlatá, béžová, světle hnědá, tmavě hnědá |
| MARI marihuana | zelená |
| SULP síra | žlutá |
| WOOD dřevo | klády ve třech vrstvách, kůra a světlá čela |
| WDPR dřevařské výrobky | hranice prken |

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
(18 nákladů), dřevo v seznamu nákladů.
