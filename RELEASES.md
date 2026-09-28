# Co je v releasech

Velké soubory do gitu nepatří, takže je hráč dává do releasů repa
`grrrrshadow/grrrrf`. Tohle je soupis, ať se příště nemusí hledat.
Stav k 2026-09-26. **Úplný seznam všech souborů**, i s obsahem tarů a md5
každého GRF, je v `INDEX-RELEASY.md` (generuje `tools/zipindex.py index`).
Tady je jen souhrn, k čemu co je.

Kódy na začátku jmen jsou GRF ID z BaNaNaS: `4d49....` je CZTR,
`4d65....` ECS.

---

## glb — GLB.zip, 156 MB

Modely a osvětlení pro render z Blenderu. Do gitu schválně ne, jsou
v `.gitignore`.

- `GLB/hdri/` — `sunset.hdr`, `overcast.exr`, `snow.exr` (6 až 71 MB)
- `GLB/bsg__shuttle_mk._iiix0cx60.glb`, `GLB/glbobj/Shuttle.glb` — raketoplán
- skripty `objtoglb*.py`, `materialyglb.py`, `glb3BBC.py` a další

## glb2 — newgrf.zip, 200 MB, 98 souborů

Hráčovy pracovní složky a hotové GRF.

| co | velikost |
|---|---|
| `cztrtruckset/` — pracovní složka truck setu, 50 souborů | 92,9 MB |
| `s1203modradodavka/` — pracovní složka dvanácettrojek, 37 souborů | 3,5 MB |
| `Real_Aircrafts_Betaf.grf` | 82,2 MB |
| `CZTR_Plane_set.grf` | 58,1 MB |
| `CZTR_Truck_SetBRYLE1.grf` — hráčův zvětšený build | 38,3 MB |
| `VWT1-S1203modradodavka.grf` | 4,1 MB |

V `cztrtruckset/` je i **`yagl.exe`, ta starší verze pro Windows**, co
balila chunkované sprity s chybou. A hráčovy skripty `barvy*.py`,
`posun*.py`, `bounding.py`, `cistic.py`, `analyza.py`.

## par — cztr.zip, 253 MB

| co | velikost |
|---|---|
| `4d490207-CZTR_Engines_Steam-1.0.2.tar` | 138 MB |
| `4d490104-CZTR_Rails-2.2.4.tar` | 20 MB |
| **`4d490213-CZTR_Wagons_Cargo-1.1.0.tar`** — nákladní vagony | 132 MB |

## par2 — zip2.zip, 23 MB

- `4d490203-CZTR_Truck_set-1.0.1.tar` — **oficiální** truck set, na porovnání

## par3 — zip3.zip, 592 MB

| co | velikost |
|---|---|
| `4d490101-CZTR_Road_set-2.3.1.tar` | 15 MB |
| `4d490209-CZTR_Engines_Diesel-1.1.0.tar` | 80 MB |
| `4d490212-CZTR_Wagons_Passengers-1.2.0.tar` — osobní vagony | 220 MB |
| `4d490210-CZTR_Engines_EMU-1.2.0.tar` | 91 MB |
| `4d490208-CZTR_Engines_Electric-1.2.0.tar` | 233 MB |
| `Real_Cars_1_5_1DECOUPLE.grf` | 15 MB |
| `nofences.grf` | 1 kB |
| `OpenTTD-YPS-Decouple.zip` — hráčův build hry | 11 MB |

## par4 — zip4.zip, 9,5 MB

Sady průmyslů a budov, 22 tarů:

- `55440100-GIST_German_Industries_Set-0.21.15`
- `54543230-Industries_of_the_Caribbean-2.7`
- `524a450b-Fixed_OpenGFX_Mars_Houses-1.1`
- `f1250009-FIRS_Industries_5-5.2.0` a `f1250007-FIRS_Industries_3-3.0.12`
- `4d471002-CZIS-3.2.1`
- `4a448807-XIS_Extreme_Industry_Set-0.6.2`
- `54540202-Beach_as_Industry-1.2.0`, `4a448850-Housing_as_Industries-0.1.1`
- `41533031-Swedish_Houses-1.1.2`, `43481001-Polish_Buildings_as_Objects-2.0`
- ECS: Basic vector II, Chemical vector II, Agricultural, Construction,
  Machinery, Basic, Town (dvě verze), Wood, ECSext 2.6, Industry Add-on

Doplnění: **Industries of the Caribbean 2.7 potřebuje ITL Houses.**
Bez nich skončí fatální chybou. Ty nejsou v releasu, ale přímo v repu
ve složce `sbirka-grf/`, viz tamní `README.md`.

---

## par5 — zip5.zip, 160 MB

Model a pracovní složky lokomotivy M62 („Sergej“):

- `M62-1675.blend` — model v Blenderu (23. 1. 2026), starší kopie v `zz/`
- `m62/diesel_locomotive_m62.glb` — převod do glb, **z něj se fotí** (`sergej/`)
- `m62/glb3BBC.py` (24. 1. 2026) — nejnovější fotící skript, z něj vychází `sergej/render_sergej.py`;
  starší `glb3B*.py` hráč označil za nefunkční
- `m62/diesel_locomotive_m62_0-8.png` — staré fotky (17 px/m, v bočním pohledu uříznuté)
- `m62/hdri/` — stejná HDRI jako v `glb`
- `vw3/`, `vw4/` — pokusy o balení (`pack*.py`, `m62.yagl`), `vw4/yagl.exe` stará verze
- textury v `zz/*.bmp`

---

## par6 — zip6.zip, 329 MB

Modely 3D (hlavně glb ze Sketchfabu), autoři a licence jsou v `AUTORI-MODELU.md`:

- **letadla od manilov.ap:** An-10, An-74, An-124, An-225, MiG-21, Jak-42, Tu-114, Tu-144, Tu-154, Tu-204
- **Buran a raketa:** `space_shuttle_buran.glb` (tashtego, **CC BY-NC 4.0**) a
  `energia_rocket_untextured.glb` (Soviet Model Magic, bez textur)
- **nákladní auta od hans1240:** Tatra 148 a 815, Praga V3S, ZiL-164 a 4514, Amur. Dále Ural
  (Thcyrax), Žuk (Pavlo_Holubov), Žuk valník (Shonan), Opel Movano (Fratzica)
- **přívěsy a karavany:** car trailer (DynamicSAV), small a large caravan (rhcreations)
- **sci-fi:** BSG lodě (3D Sci-Fi), Star Wars (LarsH.), Zeppelin (Miguel Adão)
- **konopí:** cannabis plant, small cannabis plant a fat joint (streetpharmacy), cannabis sativa
  (Zbrojmistrz)
- **ostatní:**
  - `aviafurgonvb/` je Avia do Cities: Skylines;
  - `gggg/` je Trabant v Cinema 4D;
  - FSO Warszawa jsou modely do GTA;
  - Tatra 148 je mod do FS25;
  - `v3s_praga.rar/.glb` je bez autora.

---

## Releasy v `forclaude` (hra, jen číst)

| tag | zip | co v něm je |
|---|---|---|
| `newgrf` | `newgrf.zip`, 156 MB | `CZTR_Wagons_cargo.grf` (1.0.0) a `f1250007-FIRS_Industries_3-3.0.12.tar` |
| `testsave` | `Download.zip`, 104 kB | `test 1.sav`, `testnew.sav`, `test1.txt`, `openttd.cfg` |

V `grrrrf` visí ještě prázdný koncept (draft) `par3` z 19. 9., nic v něm
není. Skutečný `par3` je ten druhý, se `zip3.zip`.

---

## Jak z nich dostat jeden soubor bez stahování celého zipu

```bash
python3 tools/zipindex.py list https://github.com/grrrrshadow/grrrrf/releases/download/par3/zip3.zip
python3 tools/zipindex.py get  https://github.com/grrrrshadow/grrrrf/releases/download/par3/zip3.zip Diesel diesel.tar
```

Stáhne se jen konec zipu (adresář) a pak jen rozsah toho jednoho souboru.
Nástroj sám pozná, jestli je soubor zkomprimovaný. **Zkomprimované
(deflate, metoda 8) jsou soubory ve všech zipech**, uložené bez komprese
jsou jen složky a pár prázdných souborů. Velikost zipu se bere z odpovědi
na `GET` s rozsahem, protože `HEAD` na odkaz ke stažení vrací 401.

Proxy tu potřebuje CA `/root/.ccr/ca-bundle.crt`.
