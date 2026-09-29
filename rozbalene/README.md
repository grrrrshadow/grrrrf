# Rozbalené cizí sady (jen text)

Výpisy yaglu bez obrázků a zvuků (`yagl -d -n`, viz `yagl/POSTUP.md`). Slouží ke čtení: co který vůz
vozí, jaké kódy nákladů sada zná, jak jsou napsané callbacky. Zpátky do GRF se z nich složit nedá.

| složka | sada | GRF | md5 | odkud |
|---|---|---|---|---|
| `cztr-wagons-cargo-1.1.0/` | CZTR Wagons-Cargo 1.1.0 | `CZTR_Wagons_cargo.grf` | 51428bd34dd430467423562cafcb61ec | release `par`, `cztr.zip` |
| `gets-0.7/` | GETS German Extrazoom Trainset 0.7 | `gets0.7.grf` | 00fd0b19f81b0d30fb3c187e827c64b6 | BaNaNaS 53410808 |
| `gets-alpine-0.3.1/` | GETS: Alpine Addon 0.3.1 | `gets_alpine_0.3.1.grf` | 6df3adfa09d57769cf4a721bcd045fcc | BaNaNaS 53411c1c |
| `firs-5.2.0/` | FIRS Industry Replacement Set 5.2.0 | `firs.grf` | df3c0e7f1cb3f1fdcac37dd22a1b0885 | release `par4`, `zip4.zip` |
| `axis-2.3.1/` | AXIS eXtreme Industry Set 2.3.1 | `axis_2.3.1.grf` | 8458a68b07293fe482ded5aa3b253e3c | BaNaNaS 4a4b8808 (hráčova hra, save v3s2) |
| `apollo-1.0/` | Apollo Rocket Industry Set 1.0 | `apollo.grf` | 133d9f2bebb49f187515faf7b13356bb | BaNaNaS 454e1501 (hráčova hra, save v3s2) |
| `auztown-commercial-14/` | AuzTown Commercial Industries 14 | `AuzTownSetInd-v14-2022-02-21.grf` | a155714d8a75ef84616ea813994434e1 | BaNaNaS 47473337 (hráčova hra, save v3s2) |
| `beach-as-industry-1.2.0/` | Beach as Industry 1.2.0 | `beach_ind.grf` | b29c04d41ae17e1477cbde5651eb98ea | BaNaNaS 54540202 (hráčova hra, save v3s2) |
| `czis-3.2.1/` | CZIS 3.2.1 | `czis.grf` | 2c7b622cf502529bf13d1a160306f92f | BaNaNaS 4d471002 (hráčova hra, save v3s2) |
| `xis-0.6.2/` | XIS Extreme Industry Set 0.6.2 | `xis.grf` | 63dc8fb4423a643de87d70b06cccd3cf | BaNaNaS 4a448807 (hráčova hra, save v3s2) |
| `gist-0.21.15/` | GIST German Industries Set 0.21.15 | `german_industries.grf` | 2b1fbabb629efa8d93db9988a764d605 | BaNaNaS 55440100 (hráčova hra, save v3s2) |
| `housing-as-industries-0.1.1/` | Housing as Industries 0.1.1 | `housingind_0.1.1.grf` | 70b125abda6dd89fc1260792807191c5 | BaNaNaS 4a448850 (hráčova hra, save v3s2) |
| `caribbean-2.7/` | Industries of the Caribbean 2.7 | `industries_of_the_caribbean.grf` | c3dae8e922e8486c1cf0bf8ccdd127ba | BaNaNaS 54543230 (hráčova hra, save v3s2) |
| `open-industries-temperate-0.4.3/` | Open Industries: Temperate 0.4.3 | `open_industries_temperate.grf` | 4bebbf2bcbaeeb1cf4574c455f83f45d | BaNaNaS 4f495431 (hráčova hra, save v3s2) |
| `wr-tourist-set-1.1.0/` | WR Tourist Set 1.1.0 | `wannaroo-tourist-set.grf` | de2dc28ca46c6f6f32bad7b7b8ef5ebc | BaNaNaS 6a647202 (hráčova hra, save v3s2) |

Licence (podle BaNaNaS a přiložených `license.txt`):

| sada | autor | licence |
|---|---|---|
| CZTR Wagons-Cargo 1.1.0 | stefino_cz a Couda (CZTR team) | CC BY-SA 3.0 |
| GETS 0.7 a GETS Alpine Addon 0.3.1 | GarlicBread42 | GPL v2 |
| FIRS 5.2.0 | andythenorth | GPL v2 |
| AXIS 2.3.1, XIS 0.6.2 a Housing as Industries 0.1.1 | EmperorJake | GPL v2 |
| Apollo Rocket Industry Set 1.0 | Erato | GPL v3 |
| AuzTown Commercial Industries 14 | kevinfields777 | GPL v2 |
| Beach as Industry 1.2.0 a Industries of the Caribbean 2.7 | 2TallTyler | GPL v3 |
| CZIS 3.2.1 | matematysek | GPL v2 |
| GIST 0.21.15 | UweDomaratius | GPL v2 |
| Open Industries: Temperate 0.4.3 | DuNeSliM | GPL v2 |
| WR Tourist Set 1.1.0 | jrook1445 | GPL v2 |

Výpisy jsou jen převedené do textu yaglem, obsah je beze změny. U CZTR ležel v rozbalené kopii jen
GRF. Jeho `license.txt` je stejný soubor CC BY-SA 3.0 (22 820 B), vzatý ze CZTR Engines Diesel 1.1.0.
Co z licencí plyne pro úpravy, je na konci.

### Sady z hráčovy hry (2026-09-29)

Hráč poslal uloženou hru `v3s2.sav` (hra 15.x, save 368) a ke kódům nákladů: *„si dej chybějící do repa, budem
s nimi dělat“*. V savu (kus `NGRF`) je 40 GRF; sady průmyslu a měst, které v repu ještě nebyly, jsem stáhl
z BaNaNaS a rozbalil tak jako ty výš (`yagl -d -n`). Odkaz na stažení je
`https://bananas-cdn.openttd.org/newgrf/<GRF ID>/<md5 ze savu>/<GRF ID>-<jméno>-<verze>.tar.gz` (jméno na konci si CDN nekontroluje,
rozhoduje md5 ze savu). Z rozbalených výpisů jsou kódy nákladů v `naklady.md` a ve vzorové tabulce.

Do repa jsem **nedal** sady, jejichž licence to nedovoluje; jejich kódy nákladů jsou jen v `naklady.md`:

| sada | autor | licence | proč ne |
|---|---|---|---|
| BSPI 2.13 (`42580002`) | Borg, kamnet | vlastní | „do not have permission to modify or distribute“ |
| ECS Town vector 1.2 (`4d656f91`) | George | CC BY-NC-ND 3.0 | bez úprav, výpis je úprava |
| Temporal8 Real Industries 32bpp beta 4.0.3 (`54454d39`) | Temporal8 | vlastní, `license.txt` prázdný | nevím, co dovoluje |

CZTR Wagons-Cargo **1.0.0**, kterou má hra kvůli FIRS 5, leží v repu hry jako `CZTR_Wagons_cargo.yagl`.
Tu tady nekopíruju, patří hře.

## Rostlinná vlákna a marihuana (2026-09-27)

Hráč: *„najdi lepší kód pro rostlinná vlákna, ať marihuanová vlákna vozí vagonky CZTR“*,
*„Uacs má vozit rostlinná vlákna“*.

### Jaký kód mají sady pro rostlinná vlákna

- **CZTR Wagons-Cargo 1.1.0:** FICR (Fibre crops, přadné plodiny) má v tabulce, ale **žádný vůz ho
  nevozí**. MARI v tabulce nemá vůbec.
- **GETS 0.7:** FICR. Vezou ho kryté vozy (G 02, G 10, Gl 11, Gbs, Gmhs, Hbis, Hbillns, Habbiins)
  a kontejnerové vozy (Lgjs, Sggmrs, Sgmmrs), celkem 33 vozů. Kryté výsypné vozy (Kkt, Tad, Tads,
  Tals) a vozy s víky (K) mají FICR v povolených i zakázaných zároveň. Zákaz vyhrává, takže ho nevezou.
- **GETS Alpine 0.3.1:** FICR, vozí ho jen krytý vůz RhB „Haik“.
- **FIRS 5.2.0:** přadné plodiny nemá. Zakládá 96 nákladů, FICR ani OLSD mezi nimi nejsou.

### Uacs v CZTR

- **1.1.0:** vůz 0x011E. Do roku 1981 se jmenuje „Raj (ČD)“, od 1982 „Uacs (ČSD, ČD, Private)“
  (callback podle roku výroby). Bere přesně tyhle kódy: LIME SALT CBLK OLSD POTA SULP QLME SASH CMNT
  CHEM. Předchůdce Paoj (0x0115) má totéž bez CHEM. Nic jiného nevezmou, třídy nákladu CZTR 1.1.0
  nepoužívá.
- **1.0.0 (hra):** vůz 0x00B1 „Uacs (ČSD,ČD)“ bere cokoli **sypkého** kromě výjimek (AORE CLAY
  COAL FERT FLOU FRUT GRAI GRVL HOPS IORE NITR SAND SCMT SGBT SLAG UORE URAN WDPR WSTE).

### Doporučení: OLSD (neplatí, hráč 28. 9.: *„OLSD budou na OLSD, to je olej“*)

Hráč to zamítl: vozy na `OLSD` zůstanou na olejniny. Hra od kolegy dává konopná vlákna jako `FICR`.
Níž je původní úvaha, jen pro záznam.


Z deseti kódů, které Uacs v 1.1.0 bere, je **OLSD (olejniny) jediný, který FIRS 5 nepoužívá**.
Ostatní (vápenec, sůl, saze, potaš, síra, pálené vápno, soda, cement, chemikálie) už FIRS 5 má
a marihuana by se s nimi tloukla. OLSD je navíc rostlinný náklad. MARI žádná z těch sad nezná.

Když marihuanová vlákna dostanou kód OLSD a třídu **sypké**:

- **CZTR 1.1.0:** Uacs/Raj a Paoj podle seznamu.
- **CZTR 1.0.0:** podle třídy 22 druhů vozů, mezi nimi Uacs i St.
- **GETS:** 48 vozů podle třídy: otevřené (Eanos, Eaos, Om, Omm, Oc), výsypné (Fad, Fads, Fals,
  Oot, Otm) a kontejnerové Bt. Kryté výsypné (Tals, Tads, Kkt) ne, ty mají OLSD zakázané.
- **Alpine:** 7 vozů podle třídy (RhB Fac, KFNB).

Jen „sypké“, bez „kryté“. S třídou kryté by v GETS zbylo 27 vozů, protože část otevřených vozů
kryté náklady zakazuje.

Druhá možnost je **FICR**, běžný kód pro vlákna: vezou ho kryté vozy GETS i Alpine. CZTR 1.1.0 ho
ale nevozí vůbec, museli bychom mu ho do Uacs dopsat (upravená CZTR sada, jako truck set Crippled).

Kód dává ten, kdo náklad zakládá (vlastnost 17 u nákladu). Vlastní GRF, které mají v tabulce MARI
(VW T1), by pak potřebovaly OLSD místo MARI.

## Jak hledat

```bash
python3 tools/naklady.py rozbalene/gets-0.7/gets0.7.yagl FICR Uacs     # vozy s kódem nebo jménem
python3 tools/kdo_veze.py rozbalene/gets-0.7/gets0.7.yagl OLSD sypke   # kdo by vzal náklad
```

`kdo_veze.py` počítá jako hra (`CalculateRefitMasks`): nejdřív třídy, pak se přidá seznam „vždy“
a nakonec se ubere seznam „nikdy“, zákaz vyhrává.

## Licence: co smíme (2026-09-27)

Hráč: *„koukni na licenci, jestli můžem“*.

**CZTR Wagons-Cargo, CC BY-SA 3.0:** smíme ji upravit i šířit, třeba přídavek, aby Uacs vozil
vlákna, nebo upravenou celou sadu. Podmínky:

1. uvést autory a sadu: CZTR Wagons-Cargo, stefino_cz a Couda (CZTR team);
2. přiložit licenci nebo odkaz https://creativecommons.org/licenses/by-sa/3.0/ ;
3. napsat, že a co jsme změnili (bod 3b);
4. úprava musí být zase pod CC BY-SA 3.0 nebo 4.0 a nesmí se přidat žádné další omezení (bod 4b);
5. nesmí to vypadat, že to autoři CZTR schválili.

**GETS, GETS Alpine, FIRS 5, GPL v2:** taky smíme upravit a šířit. Úprava musí zůstat pod GPL v2,
s vyznačenými změnami a datem, a k GRF patří zdroják (u nás yagl).

Pozor, CZTR sady nemají všechny stejnou licenci. Truck set a Tram set jsou GPL v2, Narrow gauge
CC BY 3.0, ostatní CC BY-SA 3.0. Vždycky se kouknout na konkrétní sadu (BaNaNaS, `license.txt`).
