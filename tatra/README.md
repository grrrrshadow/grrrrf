# Tatra 148 a 138 (rozdělaná, 29. 9.)

Hráč 29. 9.: *„my budem dělat dvě velký original size 148 a 138 a dvě malý 148 a 138. 138 vyrobíme přiložením
spritu chladiče na 148, to je jen z některých směrů, ušetříme spoustu místa MB“*, *„hans1240 berem na tekutiny.
A nádrž pak dáme pryč a dáme tam korbu na náklad, pak plachtu a kupy náklady jako u V3S“*, *„majáky pryč, žádná
vojenská, oranžový tatrovácky 148 a červený komunistická červená 138“*.

- **Model:** Tatra-148-AKT-3-3 od hans1240 (https://sketchfab.com/3d-models/tatra-148-akt-3-3-fd33c6c21dd54539b1fa449be41300ec),
  CC BY 4.0, release `par6` (`zip6/bar/tatra-148-akt-3-3.glb`), zkopírovat do `model/` (v gitu není). Cisterna
  (díly `AC`) na tekutiny, 9,25 m. Model nemá barvy ani textury, barvy dává `render_t148.py` podle jmen materiálů.
  Pneumatiky jsou `wheel_rm.2`, disky `wheel_rm.1`. Modré majáky (`kabina.15`) jsou schované, střešní světla nesvítí.
- **Nátěr:** 148 tatrovácká oranžová, 138 komunistická červená (`NATERY`).
- **Mřížka chladiče:** model má na masce jen hladkou plochu. Namodelovat mřížku 148 i 138; 138 podle hráčova
  videa skutečné T 138 (velký zaoblený otvor, nahoře širší, svislá zahnutá žebra do vějíře, nad ním červené TATRA).
- **Fotky:** `python3 render_t148.py <oranzova|cervena> <px_na_m> <výstup>`, kamera a HDRI jako vejtřaska.
- **Korba místo cisterny** (hráč: *„cisterna je fakt pro hasiče, tam z cisterny nahoře kouká takovej hrb. Jak bysme
  udělali korbu na náklad?“*, *„můžem vzít korbu z jiného auta“*): `KORBA=valnik` nebo `KORBA=sklapec` schová cisternu
  (díly `AC_` kromě blatníků `AC_kabina.3`, příčníku a tažného zařízení) a postaví korbu z kvádrů na rám: podlaha
  z = 0,32 m, y −5,00 až 1,05 m, x ±1,24 m. Valník má bočnice 0,55 m (náklady na něm jsou vidět jako u vejtřasky),
  sklápěč S1 ocelové bočnice 1,0 m se žebry a štítek nad kabinou. Hráč chce spíš přebarvování hrou (jeden obrázek
  pro 148 i 138).
- **Sklápěč S1 od hans1240** (`model/tatra-148.glb`, hráč ho poslal 29. 9.: *„co vozíme kupy a pytle, by šlo asi na
  tuhle“*): 7,54 m dlouhý, v centimetrech, kabina na −Y jako vejtřaska (bez +180). Náhled dělá
  `python3 render_sklapec.py <oranzova|cervena> <px_na_m> <rám_px> <výstup>`: nabarví po dílech (kabina, korba
  a disky lak, `RamTk` černý, `TG_POLOOSA` a `TG_T148` tmavé, `Pneu*` pneumatiky), kabinu (jeden kus i se skly)
  rozdělí na samostatné kusy a skla, zrcátka, reflektory a blinkry najde podle polohy a velikosti.
  Korba S1 změřená paprsky: podlaha z = 1,46 m (u bočnic zaoblená nahoru, vzadu od y 5,9 stoupá na 1,66),
  bočnice x ±1,13, nahoře z 2,39 až 2,61, přední čelo y 2,75, štítek nad kabinou y 1,25 až 2,5.
  `KUPA=GRVL|SAND|COAL` nasype kupu jako u vejtřasky (kupa vyplní korbu až pod okraj bočnic, viz Kupa níže). Pytle: bočnice jsou metr vysoké, pytle by byly vidět jen shora, musely by se skládat nad bočnice.
- **Licence:** hráč 29. 9. rozhodl, že modely od hans1240 bereme podle licence, kterou uvádí (CC BY), jako předlohu,
  auto je ve hře asi 120 × 60 px (`AUTORI-MODELU.md`, oddíl „Pozor na modely od hans1240“).
  Cisternu na tekutiny uděláme vlastní na podvozku sklápěče (bez hasičského hrbu).
- **Mřížka chladiče 148** (hráč 29. 9.: *„musíme zlepšit chladič mřížku, teď tam není žádnej“*): model má na masce
  jen hladkou plochu (y −0,48, x ±0,54, z 0,995 až 1,53). `render_sklapec.py` na ni dá mřížku podle hráčových fotek
  skutečné T148: 6 řad × 3 sloupce tmavých otvorů všude (hráč: *„tam udělej mřížku všude a je to jak nápis“*;
  skutečná má nahoře uprostřed plech), uprostřed tmavý nápis TATRA přes půl mřížky (39 × 6,2 cm, v malém z něj
  je další řada mřížky) a po stranách masky 3 žebra. Otvory 4,5 cm, aby byla mřížka ve hře vidět i v malém.
  `MRIZKA=zadna` ji vypne.
- **Mřížka chladiče 138** (hráč 29. 9.: *„jo to máš mřížku 148 a co 138?“*, *„barva je dobrá, mřížku zkus trochu
  zlepšit“*): `MRIZKA=138` dá místo mřížky 148 mřížku podle hráčova videa a čtyř fotek skutečné T138: oválný otvor
  92 × 44 cm (x ±0,46, z 1,065 až 1,505, nahoře širší a zaoblený, dole plošší), za ním čistá černá, v něm 9 širokých
  lamel (6,5 cm) v barvě auta do vějíře (sbíhají se k bodu pod mřížkou, uprostřed svisle, na krajích 32°, krajní
  nahoře ohnuté ještě víc ven), nad mřížkou na horním pásku masky oválný chromový štítek s červeným TATRA,
  skloněný dozadu jako kapota. `ZEBRA=bila` dá bílé lamely jako na některých fotkách, `LAMEL` a `SIRKA` mění počet
  a šířku lamel. Jinak je 138 stejná jako 148, nátěr `cervena` (hráč: *„barva je dobrá“*). Na fotkách mají 138
  často blatníky a nárazník v jiné barvě (bílé, krémové).
  Jak se k tomu došlo: první mřížka přes celou masku byla moc široká. Druhá (84 × 41 cm, 13 úzkých lamel) seděla
  na hranaté masce 148 jako druhý oblouk. Hráč: *„to půlkulatý trochu výš a větší a ztratí se to … dej mřížku výš
  a opticky se líp spojí do hranaté 148“*, *„tahle oválná je asi dobrá“*. Takže ovál zůstal, je větší a vrchol má
  2 cm pod horní hranou masky. Pak *„jen trochu zvýraznit, ať na malinký fotce je trochu vidět, nemusí to být
  přesný“* a *„černou pod lamely“*: 15 úzkých lamel v herní velikosti splynulo do tmavé skvrny, 9 širokých na
  černé dává svislé proužky.
- **Světlo** (hráč: *„lépe osvětlit, ať vynikne zaoblení kolem mřížky chladiče směrem ke kabině, asi víc stínu“*):
  `SVETLO=slunce` (výchozí) zapne stíny od okolí a přidá slunce zleva shora, pevné vůči kameře (auto se točí,
  světlo ne), okolí slabší (`OKOLI` 0,35, `SLUNCE` 5, `ZEPREDU` −0,25) a lak lesklejší (`LESK` 0,42).
  `SVETLO=okoli` je původní ploché světlo jako u vejtřasky.
- **Kupa** (hráč: *„kupičku větší o 20 % na výšku, celou kupičku výš“*): korbu vyplní až těsně pod okraj bočnic
  (`DNO_KUPY` 2,28 m) a vrchol je na 3,07 m místo 2,83 (nad bočnice kouká o 20 % víc a celá o 0,2 m výš).
- **Nástavby** (hráč 29. 9.: *„co dál? připravíme valník, pro plný valník plachta a cisterna na tekutiny?“*):
  `KORBA=sklapec` (výchozí) je korba S1 z modelu, `valnik`, `plachta` a `cisterna` ji schovají a postaví svoji,
  `zadna` nechá jen podvozek. Podvozek bez korby: pomocný rám nahoře z 1,18 (y 2,16 až 6,37), za kabinou rezervní
  kolo a schránka do z 2,3 (y 2,2 až 2,6), díly sklápění do z 1,30 zmizí pod podlahou. Nástavby jsou od y 2,70 do 7,00.
  - **Valník** (hráč: *„jo je to dobrej valník“*): dřevěná podlaha z 1,36 na příčnících, sklopné ocelové bočnice
    0,6 m v barvě auta se dvěma prolisy, na každé straně dva díly, klanice, panty, zadní čelo stejné, přední čelo
    1,0 m a nad ním mřížka proti nákladu do kabiny.
  - **Plachta** na plný valník (jako u vejtřasky): boky kousek přes bočnice, střecha 1,6 m nad podlahou (z 2,96),
    podélné hrany zaoblené. Barva `PLACHTA=seda|zluta|sedobila|rezna` (vojenská ne, hráč: *„žádná vojenská“*).
  - **Cisterna** na tekutiny: vlastní, hladká, bez hasičského hrbu. Oválný průřez 2,30 × 1,45 m, vyduté dna,
    y 2,76 až 7,02, dno z 1,30 na třech sedlech, dvě obruče, dva nízké průlezy, vzadu výpust a žebřík, blatníky
    nad zadními koly. Asi 11 m³.
- **Náhledy v repu** (`nahledy/`, hráči mizí obrázky v aplikaci): `sklapec148.png`, `mrizka138.png`, `nastavby.png`.
- **Barvy nástaveb** (hráč 29. 9.): *„bočnice udělej hnědou, prkna, to jsou hnědé dřevěné boky valníku a nad nimi
  plachta, u 138 i 148“*, *„chtělo by to tři barvy cisterny modrou, bílou a žlutou, jenom tu cisternu na autě jinou
  barvou“*, *„celooranžový a celočervený valník a cisternu nebudem používat, jen sklápěčka může být celooranžová
  a celočervená“*.
  - Valník: bočnice, zadní a přední čelo z vodorovných hnědých prken s mezerami (bočnice a zadní čelo tři prkna,
    přední pět), kování a klanice tmavé, rám podlahy černý. V barvě auta je jen kabina.
  - Cisterna: `CISTERNA=modra|bila|zluta|cerna` (nádrž, obruče a průlezy), kabina v barvě auta. Co v které (hráč:
    *„žlutá chemie, modrá voda, mlíko, olej a bílá benzín, asi na ropu musíme udělat černou tmavou“*): modrá voda,
    mléko a olej, bílá benzín, žlutá chemie, černá ropa. Přiřazení kódů nákladů se udělá při skládání GRF.
  - Sklápěč zůstává celý v barvě auta (148 oranžová, 138 červená).
- **Zelená vojenská Tatra** (hráč: *„na ty věci, co vozí jenom zelená vejtřaska, uděláme zelenou Tatru 138 a 148
  valník a valník plachta, pro uranový věci, military, explosives“*): nátěr `vojenska` olivový jako vojenská
  vejtřaska (80, 74, 48), valník s hnědými bočnicemi a vojenská olivová plachta (výchozí pro `vojenska`).
  Světla na blatnících (hráč: *„vojenskou kolem blinkrů na zeleno taky, u červené a oranžové to nebude vidět, tam
  je to dobrý“*): u zelené je štítek skříňky v barvě auta a oranžové jen sklíčko (11 × 6 cm), u oranžové a červené
  zůstává oranžový celý štítek. Pak *„tu zelenou jsi dobarvil dobře, udělej tak oranžovou a červenou“*: štítek je
  u všech v barvě auta, oranžové je jen sklíčko. Náhled `nahledy/blinkry.png`.
- **Náklady** (hráč: *„náklady bude mít jako vejtřaska, jen tekutiny budou v cisterně“*). `render_sklapec.py` bere
  stavitele nákladu přímo z `v3s/render_v3s.py` (oddíl od „naklad na korbe“ po `NAKLAD_KOD`, spuštěný s rozměry korby
  Tatry), takže pytle, bedny, sudy, cihly, zvířata, seno, klády, prkna, brambory, ovoce a barvy kup jsou stejné jako
  u vejtřasky a vejtřaska se tím nemění. Černé obrysy pytlů taky z vejtřasky (konec skriptu, `OBRYSY`).
  - `NAKLAD=<kód>` je vrstva jako u vejtřasky (auto neviditelné, jen zakrývá náklad), `KUPA=<kód>` totéž i s autem na
    ukázku. Kamera má pro všechny nástavby a náklady stejný střed (podvozek s kabinou bez korby S1), vrstva sedí přesně.
  - **Co na čem pojede** (hráč 29. 9.): *„kupy rudy na sklápěč, kupy zemědělských plodin na valník“*, *„minerály, uhlí
    sklápěč, a valník ocel hotovou a výrobky z oceli pod plachtu“*, *„valník ovoce, řepa, beans, zvířátka, marihuanu,
    marihuanové seno, seno, vlákna, co roste, to na valník“*. Tedy sklápěč: rudy, uhlí a ostatní nerosty; valník: co
    roste, zvířata, kusový náklad; valník s plachtou: ocel a výrobky z oceli (a co u vejtřasky jede pod plachtou);
    cisterna: tekutiny. Kódy se přiřadí při skládání GRF.
  - **Pivo** (hráč: *„pivo uděláme sudy a taky livery i cisterny, Plzeň bílou a Budvar modrou, v Čechách vozí pivo
    cisterny do hospod, teď už moc ne, ale tenkrát jo“*): sudy na valníku a přestavby Plzeň (bílá cisterna) a Budvar
    (modrá cisterna).
  - **Kupa na valníku** (hráč: *„trochu tu kupu rozsypej, je to jak bochník chleba, rozsypej to jako když zadrncá“*,
    *„kupa nevadila ve sklápěčce, ale na valníku to vypadá nepřirozeně“*): korba plná skoro po okraj bočnic a nad tím
    tři nízké nepravidelné hrbolky (0,30 až 0,42 m), povrch zvlněný. Pak *„ve valníku jsi to hezky rozsypal, takhle
    to udělej i ve sklápěčce“*: sklápěč je taky rozsypaný (plný po 2,33 m, hrbolky 0,45 až 0,60 m, aby nad vysokým
    horním lemem korby koukaly asi jako na valníku). Obojí dělá `rozsypana_kupa()`.
  - Přehled všech nákladů: `nahledy/naklady.png`.
- Náhled barev: `nahledy/barvy.png`.

## GRF (verze 10 spolu s vejtřaskou, 29. 9.)

Hráč: *„teď je to opravdu hezký, tak můžem udělat GRF“*, *„tak je dáme k vejtřaskám, ať ušetříme místo MB za zvukové
soubory?“*, *„dáme zvlášť obrázky pro přesné barvy“*, *„jo zvuk je dobrej“*.

1. **Fotky:** `python3 fotky_tatra.py <adresář> [auta|valnik|sklapec]` pustí `render_sklapec.py` pro obě velikosti
   (malá 12,2 px/m, velká 14,64 px/m, jako vejtřaska), dva rendery naraz, hotové přeskočí. Auta: 148 oranžová a 138
   červená se sklápěčem, valníkem a cisternou ve čtyřech barvách, zelená 148 a 138 s valníkem; vrstvy: všechny obrázky
   nákladu vejtřasky na valníku (kupy rozsypané, pytle, bedny, sudy, dřevo, zvířata, seno, plachty vojenská, šedá,
   šedobílá) a kupy nerostů na sklápěči. U každé fotky `kotvy.json` jako u vejtřasky.
2. **Balení:** `v3s/pack_v3s.py <mala|velka> <fotky vejtřasky> v3s/grf/<varianta> <fotky Tater>` spustí
   `grf_tatra.py` (Tatry do stejného GRF), pak `yagl -e`. Balič bez čtvrtého argumentu dělá GRF jen s vejtřaskou.
   `TATRA_NANECISTO=1` doplní chybějící fotky prázdnými (zkouška baliče, než doběhnou rendery).
3. **Auta v GRF:** Tatra 148 (`0x0102`, od 1969, 15 jednotek, 212 k), Tatra 138 (`0x0103`, od 1959, 12, 180 k),
   Tatra 148 a 138 zelená (`0x0104`, `0x0105`). 71 km/h, lidé 3 v kabině, u zelené 20 pod plachtou. Velká má jako
   vejtřaska neviditelný čumák 2 (viditelné auto `0x0112` až `0x0115`), malá je bez čumáku (Tatra je 8,2 osminy,
   o kousek delší než místo v koloně).
4. **Nástavba podle nákladu** (oranžová a červená): tekutiny cisterna (modrá voda, mléko, olej, melasa; bílá benzín
   a rafinované produkty; žlutá chemie a plyny; černá ropa a dehet), nerosty sklápěč (uhlí, koks, rudy, vápenec,
   struska, šrot, štěrk, písek, jíl, síra), obrazy nákladů vejtřasky na valníku (co roste, zvířata, pytle, bedny,
   sudy s alkoholem, cihly, dřevo), ocel a strojírenství pod šedou plachtou, ostatní pod šedobílou, lidé prázdný
   valník. Pivo má podtypy sudy, Plzeň (bílá cisterna) a Budvar (modrá cisterna). Zelená vozí jako zelená vejtřaska
   (i uran, vojenskou techniku a výbušniny), valník s obrázky vejtřasky, ostatní pod vojenskou plachtou.
5. **Zkouška:** `testv3s` ve zkušební hře (`hra/`) vypíše Tatry jako vejtřasku; fotka na okruhu
   `TEST_FOTO_SADA=tatra` a `testv3sfoto` (seznam `nakupy_tatra` v `console_cmds.cpp`).
6. **Vydáno ve verzi 10** (balík `v3s/Praga_V3S_Tatra-v10.zip`, oba GRF a licence). Ve zkušební hře:
   oranžová a červená nevozí uran a vojenskou techniku (33 z 35), zelené je vezou (34 z 35, chybí hračky), uhlí na
   sklápěči, voda, ropa a kyselina v cisterně své barvy, pivo v sudech a přestavbou v cisterně Plzeň a Budvar,
   zvuky jako vejtřaska. Tatry na okruhu: `nahledy/ve_hre_v10.png`.
7. **Verze 11: zelená schovaná pod normální** (hráč 30. 9.: *„zelenou tatru 138 148 schováme pod normální 138 148.
   hráč koupí tatru na explosives a dostane zelenou“*, *„hlavně zmizí z menu nákupu ta vojenská 138 148 a schová
   se“*). Zelené `0x0104` a `0x0105` nejdou koupit (klima žádné), v GRF zůstaly kvůli rozehraným hrám. Oranžová a
   červená vozí všechno kromě skla, elektřiny a přeřazení lokomotivy; s vojenským nákladem (`JEN_VOJENSKA`: jídlo,
   výbušniny, uran, uranová ruda, jaderné palivo a odpad, vojenská technika) jsou celé zelené. Zelená přestavba
   navíc (`T_ZELENA_NAVIC`, další podtyp „… (zelená)“) u zvířat, co roste, dřeva, cihel, stavebnin, doutníků,
   tabáku a alkoholu; cisterny Plzeň a Budvar ji nemají (*„přestavby na pivovar Plzeň Budvar ne“*). Hráč: *„skupiny
   nákladů nechcem, máme náklady pěkně vypsaný na řádku“*, takže každý náklad má svoje bloky grafiky; normální Tatra
   jich potřebuje víc než 255 (malá 211), GRF proto používá dvoubajtová čísla bloků naší hry
   (`hra/cisla-bloku/ZPRAVA-OD-HRY.md`) a je zamčený pro ottd Decouple. Switche jdou od `0x10` do `0xBF` a pak od
   `0x100`, vrstvy nákladu zůstávají na `0xC0` až `0xFF`.
