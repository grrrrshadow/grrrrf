# Mapa: kde co je

Stav k 26. 9. 2026 (večer). Když něco přibude nebo se přesune, patří to sem.

## Tohle repo (`grrrrf`), GRF a sprity

| kde | co tam je |
|---|---|
| `auta/` | Škoda / TAZ / VW (dvanácettrojky): hotové GRF s neviditelnými nárazníky (vpředu, vzadu, oba), skripty na čištění a zarovnání. Celá historie a zadání parametru „Pevnost nárazníku“ je v `CUMAK.md`. |
| `cztr/` | CZTR truck set, tvůj zvětšený build BRYLE1: přebalený, s rozestupy, vyčištěný, s články. Popis v `README.md`. |
| `sergej/` | Vlastní GRF lokomotivy M62: zelená „M62 Tamtam tajgy“ a červená „Sergej ČSD“, v měřítku CZTR i BRÝLE +20 %. Skripty na nátěr, focení, balení a kontroly, popis v `README.md`. |
| `vagony-mari/` | Zelená ploška MARI na St z CZTR Wagons - Cargo 1.1.0: sprity, zápis v yaglu, náhled. |
| `shuttle/`, `shuttletest/` | Raketoplán jako GRF, druhý je diagnostický build. |
| `glb/` | Focení z Blenderu. `GLB/` jsou skripty (modely a HDRI jsou jen v releasu `glb`), `render-test/` vyfocený raketoplán po fázích letu. |
| `sbirka-grf/` | ITL Houses 2.3, bez nich spadne Industries of the Caribbean. |
| `yagl/` | Náš upravený yagl. Zdroj `yagl-main/`, jak přeložit je v `POSTUP.md`, co jsme na něm změnili v `NASE-UPRAVY.md`. |
| `tools/zipindex.py` | Hledání v zipech v releasech a vytažení jednoho souboru bez stažení celého zipu. |
| `RELEASES.md` | Souhrn releasů: co je v kterém zipu a k čemu. |
| `INDEX-RELEASY.md` | Úplný index releasů, každý soubor, i obsah tarů, u GRF md5 a jméno. Generuje `tools/zipindex.py index`. |
| `PRO-HRU.md` | Vzkaz kolegovi, co dělá hru (rozestupy, délka vozidla, klikací box, články). |
| `temata3.md` | Moje poznámky a poučení. |
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
