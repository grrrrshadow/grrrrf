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
