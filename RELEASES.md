# Co je v releasech

Velké soubory do gitu nepatří, takže je hráč dává do releasů repa
`grrrrshadow/grrrrf`. Tohle je soupis, ať se příště nemusí hledat.
Stav k 2026-09-25.

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

Sady průmyslů:

- `55440100-GIST_German_Industries_Set-0.21.15`
- `54543230-Industries_of_the_Caribbean-2.7`
- `524a450b-Fixed_OpenGFX_Mars_Houses-1.1`
- `f1250009-FIRS_Industries_5-5.2.0`
- `4d471002-CZIS-3.2.1`
- ECS: Basic vector II, Chemical vector II, Agricultural, Construction,
  Machinery, Basic, Town (dvě verze), Wood, ECSext 2.6, Industry Add-on

---

## Jak z nich dostat jeden soubor bez stahování celého zipu

`par3` má přes půl gigabajtu a většinou z něj stačí jeden tar. Zip má
na konci adresář, takže:

1. stáhnout jen posledních pár MB (`Range: bytes=...`) a najít záznam
   `PK\x05\x06`, z něj offset adresáře
2. projít záznamy `PK\x01\x02`, u hledaného vzít metodu, komprimovanou
   velikost a offset lokální hlavičky
3. stáhnout lokální hlavičku (30 B + jméno + extra), za ní začínají data
4. stáhnout jen ten rozsah

**Pozor na metodu.** `zip2` je uložený bez komprese (metoda 0), ale
`cztr.zip` v `par` má vagony **zkomprimované (metoda 8)**. To se pak musí
rozbalit přes `zlib.decompressobj(-15)`, jinak z toho `tar` hlásí, že to
není archiv.

Proxy tu potřebuje CA `/root/.ccr/ca-bundle.crt`.
