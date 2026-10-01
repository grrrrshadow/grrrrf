# Holky u otevřených dveří aut na zastávce

Hráč 1. 10.:
- *„dáme holky kolem dvanácttrojky na zastávce, přikládací, aby to šlo rovnou na TAZ 1203, 1500 busy a Pajda karavan“*;
- *„stejnou velikost dáme k autům, aby to ladilo se zastávkou“*;
- *„když bude animace dvanácttrojek na zastávce, tak tam bude po celou dobu přiložená holka u těch otevřených dveří,
  může být i vzadu u dveří kufru, klidně dvě“*;
- *„nesmí vstoupit do vozovky ke kufru, aby nebyl konflikt s dalším autem, nesmí za bílou čáru silnice, jen z boku
  ke kufru a k předním dveřím“*;
- *„přikládací obrázky bys měl fotit fakt úplně bez stínu“*.

Je to v GRF dodávek od verze 5 (`auta/dodavky_BRYLE_v5.grf`, `auta/NOVA-VERZE.md`). Hra se nemění.

## Co je vidět

- **Kdy:** jen když auto nakládá na zastávce, tedy když má otevřené dveře (sada spritů „na zastávce“). Za jízdy, v depu,
  v seznamech ani v nákupu holky nejsou.
- **Auta:**
  - TAZ 1203 bus 0x8C a bus zahrádka 0x8B;
  - TAZ 1500 bus 0x94 a bus zahrádka 0x93;
  - Škoda 1203 Pajda karavan 0x82.

  Všechna mají stejnou karoserii a jsou zarovnaná na stejnou linku kol (`auta/README.md`), proto jim stačí jeden
  přikládací obrázek na směr.
- **Kde:** obě holky na pravé straně auta, k chodníku, za bílou čárou silnice. Nikdy za autem v jízdním pruhu ani
  přes střední čáru.
  - **A:** Character Girl s kabelkou u předních dveří.
  - **B:** tmavovlasá College Girl z boku u kufru.
- **Směry:**

  | auto jede na | holky |
  |---|---|
  | SV a JV (pravá strana k divákovi) | obě, před autem |
  | JZ (pravá strana odvrácená) | jen A, za autem u předních dveří, vykukuje u přídě |
  | SZ (pravá strana odvrácená) | jen B, za autem u kufru, vykukuje za zádí |

  Ve směrech JZ a SZ by druhá holka stála za střechou a koukala by jen hrudníkem, proto tam není.
- **Velikost 2×** jako dívky na zastávce a budovy. Auta jsou kreslená asi 1,45× (rozvor), takže holka je o něco vyšší
  než bus, stejně jako vedle zastávky.
- **Bez stínu.**
- **Na původních zastávkách hry** schová holky u bližšího pruhu zadní stěna přístřešku. S CZTR silnicemi jsou vidět.

## Jak je to v GRF

- **Obrázky:** hra kreslí auto z několika obrázků přes sebe (sprite stack, bit 7 vlastnosti `miscellaneous_flags`
  viditelného auta). Jsou to tři vrstvy:
  1. holky za autem;
  2. auto;
  3. holky před autem.
- **Skupiny `0xE0` (za autem) a `0xE3` (před autem):** za jízdy vracejí výsledek callbacku, takže hra nic nekreslí.
  Při nakládání vracejí obrázek holek. Hra (`ResolveReal`) bere jízdu a nakládání stejně jako u sady auta, holky jsou
  tedy přesně tehdy, kdy otevřené dveře.
- **Switch `0xE1`:**
  - číslo vrstvy čte z proměnné 0x10 (bity 8–15) a druh obrázku z bitů 0–7 (0 = na mapě);
  - u vrstvy 0 a 1 na mapě zapíše bit 31 do registru 0x100, takže hra chce další vrstvu;
  - jinde (depo, seznamy, nákup) kreslí jen auto.
- **Switch `0xE2`:** callbacky (kapacita a další) jdou rovnou na auto, vrstvy jen při kreslení.

## Soubory

| soubor | co to je |
|---|---|
| `holky_u_aut.py` | rozmístění holek (tabulka `MISTA`), fotky, skládání vrstev a náhled |
| `foto/` | fotky holek (`postavy/fotka_postavy.py`, kamera a světlo jako budovy, 2×, bez stínu, chodidla uprostřed) |
| `vrstvy/` | obrázky vrstev `za_<směr>.png`, `pred_<směr>.png` a `holky.json` s posuny od kotvy spritu; prázdné směry 1 × 1 |
| `nahled.png` | náhled na autech z GRF, všechny čtyři směry: TAZ 1203 bus, bus zahrádka, TAZ 1500 bus, Pajda |
| `ve_hre.png` | ze zkušební hry (`testholky`): auta čekají na zastávkách na plné naložení, CZTR i původní silnice |

## Postup

```bash
python3 holky_u_aut.py foto      # chybějící fotky holek
python3 holky_u_aut.py vrstvy    # obrázky vrstev a holky.json
python3 holky_u_aut.py nahled <rozbalený yagl dodávek> x nahled.png
# GRF: auta/NOVA-VERZE.md, stavba_vwt1.py bere vrstvy odsud
```

**Zkouška ve hře:**
- příkaz `testholky [tiků] [auto hex] [RTxx]` ze zkušební kopie hry (`hra/zkusebni-prikazy-c53e895.patch`) postaví
  křižovatku s depem a čtyřmi průjezdnými zastávkami;
- na každou zastávku pošle jedno auto s příkazem plně naložit a vyfotí to v přiblížení 4×;
- auta pak stojí ve všech čtyřech směrech.

**Měření polohy:** linka kol a bod mezi blízkými koly jsou změřené na TAZ 1203 busu (0x8C, sada na zastávce). Holky se
staví od něj (`a` dopředu, `c` ven od linky kol, v jednotkách délky hry). V první verzi stála holka u bližšího pruhu
chodidly na bílé čáře, proto je o půl jednotky dál.
