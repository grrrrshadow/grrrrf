# Škoda 706 RTO: autobus z vlastního modelu

Hráč 2. 10. (zip s fotkami a videi RTO): *„zkus udělat škoda rto autobus, to nemusí být 3D model focenej, ty umíš
dobře kreslit.“* Žádný cizí model: autobus je nakreslený z primitiv ve skriptu (`model_rto.py`, bpy) podle fotek,
videí a rozměrů z Wikipedie, vyfocený stejnou kamerou jako vejtřaska a zabalený do vlastního GRF.

| GRF | `grf_id` | měřítko | délka auta | články |
|---|---|---|---|---|
| `grf/mala/Skoda_706_RTO-v1.grf` | `MAXf` | jako CZTR, 12,2 px/m (zin4), 24,4 (zin8) | 11,7 osminy | neviditelný čumák 4/8 + autobus 8/8, rozestup 12 |
| `grf/velka/Skoda_706_RTO_BRYLE-v1.grf` | `MAXg` | BRÝLE, o 20 % větší, 14,64 px/m | 14,05 osminy | čumák 7/8 + autobus 8/8, rozestup 15 |

Oba GRF a licence jsou i v `Skoda_706_RTO-v1.zip`. Každý sprite je v GRF ve dvou přiblíženích (`zin4` a `zin8`,
8× přesně dvojnásobné, jako u vejtrašky od v16 a Sergeje od v7).

## Autobus

Škoda 706 RTO, linkový (KAR), nátěr ČSAD: červený spodek, stříbrný pruh pod okny, krémový vršek a střecha.
Skutečné údaje (cs.wikipedia.org/wiki/Škoda_706_RTO): délka 10 810 mm, šířka 2 500, výška 2 900–2 980, rozvor 5 450,
převis vpředu 1 570 a vzadu 3 790, pneu 11.00-20, motor Škoda 706 RT 11,78 l, 117,6 kW (160 k) při 1 900 ot/min,
KAR 75 km/h a 41 + 2 míst k sezení, pohotovostní hmotnost 8 570–8 950 kg, Karosa Vysoké Mýto 1958–1972, 14 451 kusů.

| | id | nátěr | uvedení |
|---|---|---|---|
| Škoda 706 RTO | 0x0100 (čumák, kupované číslo) + 0x0110 (karoserie) | červeno-krémový ČSAD | 1958 |

V GRF: 75 km/h (`speed_2_kmh` 0x96), 160 k, 8,75 t, 41 cestujících (čumák 1 + karoserie 40, jen PASS, překladová
tabulka je hráčův vzor jako u vejtrašky), zvuk odjezdu starého autobusu hry, cena a provoz o něco vyšší než
vejtřaska. Popis v nákupu je jeden zelený řádek a „Model: vlastní kresba podle fotek“.

## Jak to vzniklo

1. **Předlohy:** hráčův zip (74 fotek a 5 videí, kontaktní archy a snímky z videí jen ve scratchpadu session),
   rozměry z Wikipedie; výkres autobusu na webu není (the-blueprints.com má jen nákladní 706 RT).
2. **Model** (`model_rto.py`): kvadr trupu rozřezaný rovinami (`bmesh.ops.bisect_plane`) na smyčky u hran a pod
   okny, pak subdivision surface (3 úrovně) dá zakulacené konce a střechu; čelo vypouklé a nahoře skloněné,
   střecha mírně klenutá. Materiály podle výšky plochy (spodek, pruh, vršek). Podběhy kol jsou válce odečtené od
   trupu. **Okna** jsou kopie trupu vysunutá o 12 mm (Displace) a oříznutá kvadry oken (Boolean INTERSECT, EXACT),
   takže sklo sleduje zaoblení včetně čelního skla přes rohy; kvadry oken se nesmí překrývat, jinak přesný boolean
   vrátí prázdno (stalo se, okna zmizela). Dveře jsou tmavé linky, kola válce s diskem, mřížka chladiče chrom
   s tmavými pruhy, kulatá světla, nárazníky, zrcátka, poklopy na střeše, štítek nad čelním sklem, tmavý podvozek.
   Celo je na +Y jako V3S, zem z = 0, střed délky y = 0.
3. **Focení** (`render_rto.py`): kamera, HDRI a Cycles jako `v3s/render_v3s.py`, `kotvy.json` se zemí pod
   středem délky a pod středem rozvoru. `python3 render_rto.py cervena <px_na_m> <výstup>`, s `ZIN=8` fotky 8×
   (rám 512 px, dvojnásobné px/m) do `<výstup>_zin8`; `SMERY=1,6` a `RAM=...` na zkoušky.
4. **Balení** (`pack_rto.py`): `python3 pack_rto.py <mala|velka> <adresář fotek> grf/<mala|velka>`, pak
   `yagl -e Skoda_706_RTO-v1.grf sprites` (nebo `_BRYLE`). Kotvy a pruh na silnici CZTR jsou převzaté
   z `pack_v3s.py` (zrcadlová kotva, posun do pruhu, doladění hráče), obrázek celé délky je kotvený na zem pod
   středem autobusu a nese ho článek karoserie 8/8; čumák má prázdné sprity.
5. **Kontrola ve hře** (`kontrola_pixel.py`): zkušební hra z `51428e5` (`hra/README.md`), `testv3sfoto`
   s `TEST_FOTO_SADA=rto` koupí malý i velký autobus dvakrát na okruh, fotka v 8× i 4×, výpis `V3SDIL` dá polohu
   článku karoserie a skript spočítá přesně shodné pixely spritu.

## Co je na tom podstatné

- **Délka a články:** hra má článek nejvýš 8/8 a autobus má 11,7 (malá) nebo 14,05 (velká) osmin, proto kupované
  číslo je neviditelný čumák (4/8, 7/8) a karoserie druhý článek (`auta/CUMAK.md`). Rozestup v koloně = 8 + délka
  čumáku, mezera za autobusem 0,3 (malá) a 0,95 (velká) osminy. Obrázek je kotvený na střed autobusu, takže v koloně
  sedí; v zatáčce se karoserie otáčí o délku čumáku později než skutečné čelo, jako u CZTR BRÝLE.
- **Boolean okna:** přesný solver chce manifold vstupy bez překryvů; proto okna řidiče končí před čelním sklem a
  zadní okno před zadními dveřmi.

## Verze 1 ve hře (2. 10. 2026)

- Zkušební hra z `51428e5` (`hra/README.md`), `testv3sfoto 1500 RT14 2 300` se sadou `rto`: na okruh koupeny dva malé
  a dva velké autobusy a dva původní náklaďáky hry, dvě fotky v 8× (`gui.zoom_min 0`) a dvě ve 4×.
- `kontrola_pixel.py`: všech 16 článků karoserie (4 autobusy × 2 fotky × 2 přiblížení) sedí s posunem (0,0); shoda
  100 % u volně viditelných, u tří částečně zakrytých jiným autem v koloně 99, 83 a 54 %. Výřezy z fotek:
  `kontrola/hra_8x_v1.png`, `kontrola/hra_4x_v1.png`. Výpis hry `ZIN8: ReadSprite … ma 8x i 4x` u všech 9 spritů.
- GRF: `grf/mala/Skoda_706_RTO-v1.grf` 403 kB (md5 `f10327f3c4d9d1f4eee6022aa314135b`),
  `grf/velka/Skoda_706_RTO_BRYLE-v1.grf` 545 kB (md5 `4c14e3eafe3c88bc935c424565130839`); v každém 17 spritů
  (8 směrů autobusu se zin4 i zin8, 8 prázdných čumáku, 1 do nákupu). Sprite 4× je v malé 120 × 85 px (šikmo)
  a 140 × 48 px (podél), 8× dvojnásobný.
- Co by šlo dál: modro-krémový nátěr (městský, `NATERY["modra"]` v modelu už je), LUX se střešním nosičem a okny
  ve střeše, holky u dveří jako u dodávek.
