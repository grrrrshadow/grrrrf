# Rozbalené cizí sady (jen text)

Výpisy yaglu bez obrázků a zvuků (`yagl -d -n`, viz `yagl/POSTUP.md`). Slouží ke čtení: co který vůz
vozí, jaké kódy nákladů sada zná, jak jsou napsané callbacky. Zpátky do GRF se z nich složit nedá.

| složka | sada | GRF | md5 | odkud |
|---|---|---|---|---|
| `cztr-wagons-cargo-1.1.0/` | CZTR Wagons-Cargo 1.1.0 | `CZTR_Wagons_cargo.grf` | 51428bd34dd430467423562cafcb61ec | release `par`, `cztr.zip` |
| `gets-0.7/` | GETS German Extrazoom Trainset 0.7 | `gets0.7.grf` | 00fd0b19f81b0d30fb3c187e827c64b6 | BaNaNaS 53410808 |
| `gets-alpine-0.3.1/` | GETS: Alpine Addon 0.3.1 | `gets_alpine_0.3.1.grf` | 6df3adfa09d57769cf4a721bcd045fcc | BaNaNaS 53411c1c |
| `firs-5.2.0/` | FIRS Industry Replacement Set 5.2.0 | `firs.grf` | df3c0e7f1cb3f1fdcac37dd22a1b0885 | release `par4`, `zip4.zip` |

Licence (podle BaNaNaS a přiložených `license.txt`):

| sada | autor | licence |
|---|---|---|
| CZTR Wagons-Cargo 1.1.0 | stefino_cz a Couda (CZTR team) | CC BY-SA 3.0 |
| GETS 0.7 a GETS Alpine Addon 0.3.1 | GarlicBread42 | GPL v2 |
| FIRS 5.2.0 | andythenorth | GPL v2 |

Výpisy jsou jen převedené do textu yaglem, obsah je beze změny. U CZTR ležel v rozbalené kopii jen
GRF. Jeho `license.txt` je stejný soubor CC BY-SA 3.0 (22 820 B), vzatý ze CZTR Engines Diesel 1.1.0.
Co z licencí plyne pro úpravy, je na konci.

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

### Doporučení: OLSD

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
