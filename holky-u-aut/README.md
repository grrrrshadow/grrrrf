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

## Přiblížení 8× (2. 10.)

Kolega dal hře úroveň přiblížení 8× (`ZoomLevel::In8x`, v GRF kód zoomu 6, v yaglu `zin8`). Hráč: *„zkusíme to na
dvanácttrojkách na přikládacích studentkách, dáme maximum detailu, jsou to maličký obrázky, které jen přikládáme“*.
Od dodávek v7 mají holky u dveří dvě úrovně:

- **Fotky 8×** (`foto/*_z8.png`): 24,4 px/m místo 12,2, rám 240 px, 1024 vzorků místo 64. Stejná kamera, světlo
  a chodidla uprostřed, takže fotka 8× je dvojnásobek fotky 4× (`postavy/fotka_postavy.py`, proměnná `PX_M`).
- **Vrstvy 8×** (`vrstvy/*_z8.png`, v `holky.json` pod `zin8`): každá fotka 8× leží na dvojnásobku celočíselné polohy
  fotky 4× a rámeček je společný, takže vrstva 8× je přesně dvojnásobek vrstvy 4× (šířka, výška i posun). Hra to
  u víc úrovní jednoho spritu vyžaduje. Pixely 4× zůstaly jako ve v6, jen by se rámeček rozšířil, kdyby 8×
  přesahovalo (nepřesahuje).
- **V GRF** je v každém `sprite_id` holek řádek `zin4` i `zin8` (v7 a od v9). Verze 8 měla jen `zin8` (hráč: *„jenom
  8× stačí“*): ve 4× si hra obrázek dělá z 8× sama vynecháním každého druhého pixelu (`ResizeSpriteOut`) a je hrubší
  než vlastní fotka 4× (`ve_hre_4x_z_8x.png`), proto hráč rozhodl: *„budem používat sprity 4× ke spritům 8×, budem
  dávat oboje do GRF“*. Prázdné směry 4 × 4 a 8 × 8 průhledných.
- **Auta mají dál jen 4×**, v 8× je hra kreslí zdvojená; holky jsou v 8× ostré. Jiná hra řádek `zin8` přeskočí
  a kreslí 4×.
- **Směr 1 (auto jede na severovýchod) má holky o kousek výš** (v8, `MISTA`, pátá hodnota: A o 8 px, B o 6 px ve 4×).
  Hráč viděl, že holce u kufru chybí levá bota. Chodník zastávky CZTR je sprite s vlastní krabicí blíž k divákovi než
  auto, hra ho kreslí až po autě i s holkami a překryje z nich to, co leží na něm: boty (levá celá, pravá stála na
  hraně). Změřeno ve zkušební hře pixel po pixelu (`hra/README.md`, třetí hra): holce B schová až 8 px v 8×, holka A
  u předních dveří stojí o 0,3 jednotky hlouběji v chodníku, přišla by o víc (s 11 px by ale koukala nad střechu
  přístřešku, proto jen 8). Ve směru 3 holku u kufru zakrývá
  prosklený přístřešek (hráč: *„směr 3 je za tím průhledným sklem zastávky“*), to zůstává.
- Náhled `nahled_8x.png`: vlevo 4× (zvětšeno 3×), vpravo 8× (zvětšeno 1,5×, stejná velikost na obrazovce).
- Ve hře: `ve_hre_8x.png` a `ve_hre_8x_detail.png` ze zkušební hry z `51428e5` (`testholky` se `setting gui.zoom_min 0`,
  domov se sadou CZTR Road set, aby byly zastávky prosklené a holky vidět). Se `zoom_min 1` (4×) je fotka stejná
  jako s v6.

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
| `foto/` | fotky holek (`postavy/fotka_postavy.py`, kamera a světlo jako budovy, 2×, bez stínu, chodidla uprostřed); `*_z8.png` v 8× |
| `vrstvy/` | obrázky vrstev `za_<směr>.png`, `pred_<směr>.png` a `holky.json` s posuny od kotvy spritu; prázdné směry 1 × 1; `*_z8.png` v 8× (v JSONu `zin8`) |
| `nahled.png` | náhled na autech z GRF, všechny čtyři směry: TAZ 1203 bus, bus zahrádka, TAZ 1500 bus, Pajda |
| `nahled_8x.png` | TAZ 1203 bus ve směrech 1 a 3: vlevo 4×, vpravo 8× (v9) |
| `ve_hre.png` | ze zkušební hry (`testholky`): auta čekají na zastávkách na plné naložení, CZTR i původní silnice |
| `ve_hre_8x.png` | ze zkušební hry z `51428e5` (`testholky`, CZTR silnice a zastávky): vlevo 4× zdvojené, uprostřed 8× s v6 (holky zdvojené hrou), vpravo 8× s v9 (holky z fotek 8×, směr 1 zvednuté) |
| `ve_hre_8x_detail.png` | totéž zblízka, jen holky u busu ve směrech 1 a 3 |
| `bota.png` | proč chyběla bota: holka u kufru ve směru 1 ve v7 (boty pod chodníkem) a ve v8 (zvednutá), 8× |
| `ve_hre_4x_z_8x.png` | 4× ve hře: vlevo z v7 (vlastní fotka 4×), vpravo z v8 (hra si 4× dělá z 8× vynecháním každého druhého pixelu); proto od v9 oboje |

## Postup

```bash
python3 holky_u_aut.py foto      # chybějící fotky holek 4×
python3 holky_u_aut.py foto 8    # chybějící fotky holek 8× (1024 vzorků, 6 fotek za 3 minuty)
python3 holky_u_aut.py vrstvy    # obrázky vrstev 4× i 8× a holky.json
python3 holky_u_aut.py nahled <rozbalený yagl dodávek> x nahled.png      # 4×
python3 holky_u_aut.py nahled <rozbalený yagl dodávek> x nahled8.png 8   # 8×
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
