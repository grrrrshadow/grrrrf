# Mapa: kde co je

Stav k 28. 9. 2026. Když něco přibude nebo se přesune, patří to sem.

## Tohle repo (`grrrrf`), GRF a sprity

| kde | co tam je |
|---|---|
| `temata3.md` | **Moje poznámky a poučení, číst jako první.** Pravidla od hráče, co jsem se naučil a jak to hráč chce. |
| `auta/` | Škoda / TAZ / VW (dvanácettrojky): hotové GRF s neviditelnými nárazníky (vpředu, vzadu, oba), skripty na čištění a zarovnání. Celá historie a zadání parametru „Pevnost nárazníku“ je v `CUMAK.md`. |
| `cztr/` | CZTR truck set, tvůj zvětšený build BRYLE1: přebalený, s rozestupy, vyčištěný, s články. Popis v `README.md`. |
| `sergej/` | Vlastní GRF lokomotivy M62 („M62 Sergej, for ottd decouple by Karel Macha“): zelená „M62 Tamtam tajgy“ a červená „Sergej ČSD“, v měřítku CZTR i BRÝLE +20 %, motor hraje podle rychlosti. Skripty na nátěr, focení, zvuky (`zvuky/`), balení a kontroly, popis v `README.md`. |
| `v3s/` | Vlastní GRF Pragy V3S („Praga V3S Vejtřaska for ottd Decouple by Karel Macha“): vojenská a modrá (4 odstíny podle nákladu), malá v měřítku CZTR a velká BRÝLE s neviditelným čumákem. Skripty na nátěr, focení, balení, zrcadlovou kontrolu a srovnání s VW T1, balík `Praga_V3S_Vejtraska-v1.zip`, popis v `README.md`. |
| `hra/` | Moje zkušební hra s obrazem (kopie OpenTTD ze zdrojáků hry a moje zkušební příkazy `testv3s`, `testv3sfoto`), přeložená a zabalená, ať se nemusí stavět znova. V `cztr_silnice/` výstřižek silnice CZTR 1. třída – venkov, na které se fotí. Jak pustit a jak přeložit v `README.md`, postup focení v `temata3.md`. |
| `vagony-mari/` | Zelená ploška MARI na St z CZTR Wagons - Cargo 1.1.0: sprity, zápis v yaglu, náhled. |
| `shuttle/`, `shuttletest/` | Raketoplán jako GRF, druhý je diagnostický build. |
| `glb/` | Focení z Blenderu. `GLB/` jsou skripty (modely a HDRI jsou jen v releasu `glb`), `render-test/` vyfocený raketoplán po fázích letu. |
| `sbirka-grf/` | ITL Houses 2.3, bez nich spadne Industries of the Caribbean. |
| `yagl/` | Náš upravený yagl. Zdroj `yagl-main/`, jak přeložit je v `POSTUP.md`, co jsme na něm změnili v `NASE-UPRAVY.md`. |
| `tools/zipindex.py` | Hledání v zipech v releasech a vytažení jednoho souboru bez stažení celého zipu. |
| `tools/naklady.py` | Vypíše z rozbaleného yaglu vozy, jejich jména, třídy nákladu a seznamy kódů. |
| `tools/kdo_veze.py` | Řekne, které vozy by vzaly náklad s daným kódem a třídami, podle pravidla hry. |
| `rozbalene/` | Rozbalené yagly cizích sad jen jako text (`yagl -d -n`): CZTR Wagons-Cargo 1.1.0, GETS 0.7, GETS Alpine 0.3.1, FIRS 5.2.0. V `README.md` kódy pro rostlinná vlákna a proč OLSD. |
| `RELEASES.md` | Souhrn releasů: co je v kterém zipu a k čemu. |
| `INDEX-RELEASY.md` | Úplný index releasů, každý soubor, i obsah tarů, u GRF md5 a jméno. Generuje `tools/zipindex.py index`. |
| `AUTORI-MODELU.md` | Kdo udělal který 3D model a pod jakou licencí (z metadat glb), plus opis hráčova lístku s modely a autory. |
| `PRO-HRU.md` | Vzkaz kolegovi, co dělá hru (rozestupy, délka vozidla, klikací box, články). |
| `naklady.md`, `cargo-classes.md`, `prekladova-tabulka-vzor.yagl` | Slovník labelů nákladu, třídy nákladu, vzor překladové tabulky. |
| `letadla-stavy.md` | Jak GRF pozná fázi letu. |

## Jiná repa

| repo | co to je |
|---|---|
| `forclaude` | Hra (OpenTTD), dělá ji kolega. **Jen číst, nic tam nepsat.** Releasy: `newgrf` (CZTR Wagons cargo `.grf` a FIRS 3.0.12), `testsave` (savy a `openttd.cfg`). |
| `cota`, `ulzvu` | Android aplikace, s GRF nesouvisí. |
| `dete` | Prázdné. |

## Nástroje v kontejneru

- yagl: `yagl/yagl-main/build/yagl` (build se necommituje, přeloží se za půl minuty)
- Blender jako modul Pythonu: `bpy` 5.0.1 (render bez okna)
- Python: Pillow, numpy

## Kde je model M62

V releasu `par5` (`zip5/m62/diesel_locomotive_m62.glb`, originál `zip5/M62-1675.blend`).
Do `sergej/model/` se jen kopíruje, v gitu není.
