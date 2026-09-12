# temata3.md — moje vlastní poznámky

Tenhle soubor je můj. Zakládám si ho v `grrrrshadow/grrrrf`, píšu si do něj
sám pravidla a poznámky, abych nic nezapomněl mezi sezeními. Není to
dokumentace projektu ani nic pro nikoho jiného — je to můj zápisník.

## Pravidla (zadal hráč 2026-09-11)

1. **`temata3.md` v `grrrrshadow/grrrrf` je můj soubor.** Sám si sem
   zapisuju pravidla i poznámky. Na moje téma.
2. **Celé `grrrrf` je jenom moje** (upřesněno 2026-09-11) — ne jen `main`.
   Můžu si v něm zakládat soubory i větve a pushovat přímo, nepotřebuju
   k tomu zvláštní větev ani se doptávat.
3. **Do ostatních repozitářů nelezu sám od sebe.** Číst je smím, ale až
   když mě tam hráč pošle. Ne že si sám vyrazím na průzkum, protože se mi
   to zrovna hodí.
4. **Export do ostatních repozitářů jen když o tom hráč ví.** Ne potichu.
5. **V ostatních repozitářích nic nepřepisovat, nemazat, needitovat.**
   Tohle platí bez výjimky.
6. **Mám sbírat informace nezbytné pro tvorbu** (zadáno 2026-09-11) —
   zdroje, které mi hráč dá, si mám otevřít a nastudovat, ne je jen
   odložit jako odkaz. Kde to nejde (viz Odkazy), musím to nahlas říct
   a domluvit náhradní cestu, ne to mlčky obejít ani předstírat,
   že jsem to četl.
7. **Fakta znát nazpaměť, ne je odvozovat** (zadáno 2026-09-11). U věcí
   jako zkratky nákladu chce hráč spolehlivost, ne chytrost: `PASS` je
   Passengers, tečka. Nehledat v tom vzory a nedovozovat, co tam není —
   od toho je opsaná tabulka v `naklady.md`.
8. **`forclaude` je jen ke čtení** (zadáno 2026-09-11). Je to zdroj
   pravdy o tom, jak se hra chová — čtu z něj, ale **nic v něm neměním,
   nekomituju, nepushuju.** Po každé práci s ním zkontrolovat, že
   `git status` je prázdný.

## Poznámky

### 2026-09-11 — založení

- `grrrrf` bylo prázdné repo, tenhle soubor je jeho první commit.
- Pracovní repo tohohle sezení je `grrrrshadow/forclaude`, tam mám
  přidělenou větev `claude/gracious-hamilton-t0ikke` (OpenTTD build,
  spojování/rozpojování vlaků za jízdy, odtah porouchaných).
  `grrrrf` je něco jiného — to je celé moje.
- Chyba, kterou jsem hned na začátku udělal a nechci ji opakovat:
  rozjel jsem se číst `ulzvu`, `cota` a `dete`, abych zjistil, jestli
  existují starší `temata.md`/`temata2.md`. Hráč mě zastavil — tam mě
  neposlal. Pravidlo 3 vzniklo přesně z tohohle.

## Odkazy

- **NewGRF CargoTypes** — https://newgrf-specs.tt-wiki.net/wiki/CargoTypes
  (dal mi ho hráč 2026-09-11). Specifikace typů nákladu pro NewGRF —
  patří k tomu, co v `forclaude` řeší `CZTR_Wagons_cargo.yagl`.
  **Stav: nepřečteno, host je zablokovaný.** Ověřeno dvakrát —
  `WebFetch` vrátí `EGRESS_BLOCKED` a `curl` skončí na
  `CONNECT tunnel failed, response 403`. To je 403 od egress proxy,
  tedy síťová politika prostředí, ne moje nastavení.

  **Důležité, ať to znovu nepletu:** tenhle blok nejde odemknout tím,
  že mi to hráč v chatu povolí. Jeho svolení mě opravňuje ten zdroj
  použít, ale díru do sítě neudělá. Povolení domény se dělá v nastavení
  network policy toho prostředí (Claude Code on the web —
  https://code.claude.com/docs/en/claude-code-on-the-web) a projeví se
  až v novém sezení. README proxy k tomu říká jasně: 403 nezkoušet
  dokola a neobcházet, jen nahlásit zablokovaný host.

  **Otevřeno 2026-09-11:** hráč doménu povolil a wiki je od té chvíle
  dostupná (HTTP 200). Stahuju si stránky syrově přes `?action=raw`,
  ne přes shrnutí — u specifikací chci přesná data, ne převyprávění.

  Kontrola: seznam v `naklady.md`, který jsem opsal z chatu, **sedí
  přesně proti originálu** — 146 ku 146, jediný rozdíl je wiki odkaz
  kolem popisu u `NHNO`.

  Ostatní náhradní cesty, kdyby bylo potřeba víc: hráč vloží další část,
  nebo si vezmu, co jde, z dosažitelných zdrojů (GitHub funguje —
  zdrojáky OpenTTD, NML apod.).

## Soubory v tomhle repu

- **`naklady.md`** — *tohle je ten hlavní.* Prostý slovník
  zkratka → náklad, všech 146, podle abecedy. `PASS` = Passengers a tak
  dál. Žádné odvozování, jen opsaná tabulka. Tohle mám umět neomylně.
- **`cargo-classes.md`** — rozbor čtyřmístných čísel (jsou to bitmasky
  tříd, ne pořadová čísla). Hráč k tomu 2026-09-11 řekl, že o tom nic neví
  a nechce, abych hledal souvislosti — takže je to jen odložená reference,
  ne něco, čím se má argumentovat. Přednost má slovník.
- **`prekladova-tabulka-vzor.yagl`** — vzorová překladová tabulka, 147
  slotů včetně našeho `MARI`. Neznámé labely dole jako `undefined`.
- **`letadla-stavy.md`** — jak u letadla poznat fázi letu. Proměnná
  `0xE2` = fáze, `0xE6` = nakládání, `0xB4` = rychlost. Je tam i pořadí
  směrů pro sprity.
- **`glb/`** — rozbalený `GLB.zip` z releasu `glb`: blenderový render
  modelů na sprity. Velké binárky (modely, HDRI) jsou gitignorované,
  leží v releasu.
## Jak povolit zablokovanou doménu (zjištěno 2026-09-11)

Nepovoluje se to v chatu ani na GitHubu. Je to nastavení **cloud
environmentu** na claude.ai. Postup podle dokumentace
(https://code.claude.com/docs/en/cloud-environments#network-access):

1. Otevřít environment k editaci (ikona mráčku na příslušné obrazovce
   Claude Code — vlastní osobní environment nemá zvláštní stránku
   v nastavení účtu).
2. V dialogu položka **Network access**. Má čtyři úrovně:
   **None** (nic), **Trusted** (výchozí — balíčkové registry, GitHub,
   cloud SDK), **Full** (cokoliv), **Custom** (vlastní seznam).
3. Zvolit **Custom** a do pole **Allowed domains** napsat doménu,
   jednu na řádek. `*.` na začátku bere všechny subdomény.
4. Zaškrtnout **„Also include default list of common package managers“**,
   jinak se seznamem nahradí i ty výchozí povolené domény.

Projeví se to v **novém sezení** — běžící VM už svou politiku má.

Důležité k tomu: GitHub jde vlastní proxy mimo tenhle allowlist, takže
o přístup k repozitářům se tímhle přijít nedá. Allowlist je taky per
environment, žádný organizační společný neexistuje.

Pro `newgrf-specs.tt-wiki.net` tedy: **Custom** + řádek
`newgrf-specs.tt-wiki.net` (nebo rovnou `*.tt-wiki.net`) + ponechat
výchozí seznam. Kdo nechce nic řešit, dá **Full**, ale to otevře všechno.

### Pozor: režim oprávnění NENÍ síťová politika (2026-09-11)

Hráč navrhl, ať si přístup na wiki zařídím sám přes nastavení
„Claude handles permission decisions“ (auto režim). Nejde to a je dobré
vědět proč, ať to znovu nezkouším:

- **Režim oprávnění** říká, jestli se musím ptát, než něco udělám.
  Týká se nástrojů, které mám — spustit příkaz, zapsat soubor, pushnout.
- **Síťová politika** říká, kam vůbec smí to VM ven. Vynucuje ji proxy
  venku za sandboxem. Žádný režim oprávnění ji nemění.

Takže ani ve full auto se na zablokovanou doménu nedostanu: nejde
o nepovolený nástroj, ale o nástroj, který **neexistuje**. Ověřeno
hledáním v nástrojích — nic na editaci environmentu ani allowlistu tam
není. Číst environmenty umím (`list_environments`), měnit ne.

**Tenhle účet má jediný environment: `Default`, `env_01GmZvt3ZwYvH9Tt9gJSSZkf`,
úroveň Trusted.** Trusted = balíčkové registry, GitHub, cloud SDK —
`tt-wiki.net` v tom není, proto to padá. Přepnout ho musí hráč ručně
v UI podle postupu výš. Já k tomu můžu leda dodat ten název.

### Které stránky wiki jsou k čemu (2026-09-11)

- `CargoTypes` — seznam labelů nákladu.
- `Action0/Cargos` — vlastnosti nákladu. **CargoClasses je 16, label 17.**
  Je tam i celá tabulka bitů tříd.
- `Action0/Global Settings` — **překladová tabulka je vlastnost 09**
  u feature 08. Je tam příklad zápisu v NFO.
- `Action0/Industries`, `Action0/Industry Tiles` — průmysl a jeho dlaždice.
- `CargoDefaultProps` — výchozí náklady podle klimatu.
- `Action3` — napojení grafiky na typy nákladu.

Stahovat přes `curl "...?action=raw"`. Stránky s lomítkem v názvu
(`Action0/Cargos`) přes `index.php` s `--data-urlencode title=...`,
protože `Action0Cargos` je jen redirect.

### Co z toho mění přístup k práci

1. **Třídy nákladu nejsou spolehlivý identifikátor.** Specifikace sama
   říká, že se liší mezi sety a v čase. Na konkrétní náklad se refituje
   **podle labelu**, ne podle tříd.
2. **Label se nepřejmenovává.** Měnit ho bez moc dobrého důvodu je podle
   specifikace špatná praxe.
3. **FIRS, AXIS, ITI, Sunshine Trains a Iron Horse mají vlastní schéma
   tříd (FRAX)**, tahle tabulka pro ně neplatí.

## Jak hráč dělá GRF (zadáno 2026-09-11)

**U každého vozidla si ručně vypisuje, co bude vozit. Třídy nákladu
(sypké, kapalné, chlazené...) nepoužívá.** Tohle si pamatovat, mění to,
co je při práci důležité:

- Používají se **seznamy nákladů**: u silničních vozidel vlastnosti
  **24** (vždy povolené) a **25** (nikdy), u vlaků **2C** a **2D**.
  Zápis: počet v jednom bajtu, pak tolik bajtů a každý je index do
  překladové tabulky.
- Specifikace o nich říká, že platí *„independent of any of the other
  refit properties or the cargo classes“* a doporučuje je používat
  přednostně před starou maskou. Takže tenhle postup není improvizace,
  je to ta doporučená cesta.
- **Index je bajt → dosažitelných je všech 0-255 slotů.** Stará
  32bitová refit maska (vlastnost 16 u silničních, 1D u vlaků) je
  zastaralá a nás se netýká.
- Proto: **neřadit tabulku podle hranice 32 slotů.** Udělal jsem to
  a bylo to zbytečné — opraveno.
- Pozor na past: náklad, který ve hře neexistuje, se v seznamu podle
  specifikace **tiše ignoruje**. Překlep v labelu se nijak neprojeví.

Důsledek pro `cargo-classes.md`: ta reference je o třídách, které
nepoužíváme. Nezahazuju ji (hodí se vědět, co které číslo znamená, když
se čte cizí GRF), ale **nemá se s ní začínat**.

## Render spritů z 3D: `glb/GLB/glb3BBC.py`

Blenderový skript. Spouští se `blender --background --python glb3bbc.py`
a vyrobí PNG sprity z `.glb` modelu, který najde vedle sebe.

Jak funguje:

- Kamera je **ortografická**, pověšená na prázdný objekt („jeřáb“), který
  se přes constraint `TRACK_TO` dívá na střed modelu. Střed se počítá
  z krajních vrcholů, ne z originu.
- Model visí na druhém prázdném objektu („gramofon“) a **otáčí se model,
  ne kamera**. Seznam `ROTATION_ANGLES` jsou úhly toho otočení.
- Osvětlení je HDRI ze složky `hdri/` (`snow.exr`, `overcast.exr`,
  `sunset.hdr`). Stíny z HDRI jsou vypnuté.
- `UPRAVIT_MATERIALY` přepisuje barvu, drsnost a kovovost materiálů
  podle jména. Jména musí sedět na materiály v modelu.
- Renderuje se ve `512×512` a ukládá ve `248×248`.

Hodnoty, které si hráč nechal v komentářích pro různé modely:

| model | `CAMERA_PARALLEL_SCALE` | `CAMERA_DISTANCE` |
|---|---|---|
| shuttle | 25 | 20 |
| An-224 | 120 | 70 |
| C-17 | 60 | 70 |

Co u letadla změnit oproti autům: `HILL_TILT_DEGREES` (teď `-23`) je
náklon do kopce — letadlo terén nekopíruje, takže **na nulu**.
`CAMERA_ROTATION_DEGREES_X = 30` je okomentované jako „autaspravny“.

### Úhly

Devátý úhel v seznamu je **sprite do depa**, ne směr. Osm skutečných
směrů musí jít v pořadí výčtu `Direction` z hry:
`N, NE, E, SE, S, SW, W, NW`. Pro auta i letadla stejně.

Oba seznamy v tom skriptu jsou **tentýž seznam posunutý o 3 pozice**,
krok −45°. Pořadí je tedy správně, liší se jen natočení modelu v GLB.
U nového modelu se proto **neladí pořadí, jen počáteční posun**.

## Dvě techniky, které se osvědčily

**Číst zip z releasu bez stahování.** GitHub na release assety umí
`Range` requesty (HTTP 206). Přes ně se dá načíst konec zipu, z něj
centrální adresář, a stáhnout jen ten jeden soubor, co chci. U 156MB
zipu to ušetří všechno ostatní. Funguje i pro velké archivy.

**Rozebrat `.grf` bez nástrojů.** `grfcodec` ani `nml` tu nejsou, ale
kontejner verze 2 se čte snadno: 10 bajtů hlavička, dword offset datové
sekce, bajt komprese, a pak řetěz `dword délka + bajt info + data`.
Info `0xFF` = pseudosprite, jeho první bajt je číslo akce. Action 02
(varAction2) se pak dekóduje podle wiki stránky `VariationalAction2`
a `VarAction2Advanced` (tabulka operátorů). Takhle jsem přečetl, co
skutečně dělá `kaas_planes.grf`.

### Modely v `glb/GLB/` — rozebráno 2026-09-11

Oba jsou týž raketoplán, 9 meshů, 9 materiálů. **Liší se jmény
materiálů, a to je past:**

| | materiály | co z toho |
|---|---|---|
| `bsg__shuttle_mk._iiix0cx60.glb` (v kořeni) | `Col_shuttle_mk2_hull`, `..._doors`, `..._engines`, … | syrový export ze Sketchfabu |
| `glbobj/Shuttle.glb` | `barva`, `okna`, `dvere`, `korba`, `pneu`, `disky`, `podvozek`, `sedacky` | **sedí na slovník ve skriptu** |

Slovník `UPRAVIT_MATERIALY` je psaný na ty české názvy. Skript bere
**první `.glb` v adresáři**, tedy ten kořenový — u kterého se žádný
materiál netrefí a model se vyrenderuje v původních barvách. Projde to
bez chyby, jen se to vypíše jako varování. Proto má letecká verze výpis,
které materiály se opravdu přepsaly.

**Natočení je u obou stejné a správné.** Kořenový má na uzlu
`Sketchfab_model` matici otočení o 90° kolem X, `Shuttle.glb` má tutéž
rotaci na každém meshi zvlášť. Po převodu glTF (Y nahoru) → Blender
(Z nahoru) oba leží naplocho, délka ≈19 podél osy **Y**, šířka 6,85,
výška 4,4. Takže úhly se kvůli modelu měnit nemusí.

### Blender TU JDE — přes `pip install bpy` (2026-09-11)

Napřed jsem hráči napsal, že Blender v prostředí není a renderovat
nemůžu. **Byl to ukvapený závěr.** Blender je na PyPI jako modul `bpy`
a PyPI je odsud dostupné napřímo:

```
python3 -m pip install bpy      # Blender 5.0.1, Python 3.11
python3 muj_skript.py           # bez --background, bpy uz bezi headless
```

Skripty psané pro `blender --background --python x.py` fungují beze
změny — `bpy.data.filepath` je prázdný, takže `base_dir` vyjde na
aktuální adresář, přesně jak to ten skript čeká.

**Render je rychlý:** devět úhlů 248×248 při 64 vzorcích za **15 sekund**
na CPU. Takže zkoušet se to dá klidně opakovaně.

Ponaučení: než napíšu „tohle tu nejde“, zkusit i jiné cesty než
`command -v`. Chyběl `blender` jako binárka, ale ne Blender jako takový.

## yagl — tímhle se u nás dělá GRF (2026-09-11)

Hráč mi poslal `yagl` a řekl jasně: **chce, abych byl kompatibilní
s jeho postupy.** Zkoušel jsem instalovat `nml` a zamítl to. Takže:

- **Nástroj je `yagl`**, ne nml, ne grfcodec. Leží v `yagl/yagl-main/`,
  postup v `yagl/POSTUP.md`. Přeloží se za 32 s, testy procházejí.
- Round-trip ověřený na `kaas_planes.grf`: rozdíl 10 bajtů z 3,65 MB.
- **`.yagl` se musí jmenovat stejně jako cílový `.grf`**, jinak encoder
  spadne. A soubor se má jmenovat stejně jako jméno GRF v seznamu ve
  hře, jinak ho hráč nenajde.
- Budeme yagl rozvíjet pro vlastní potřeby — je to náš nástroj, ne jen
  vypůjčený.

Ponaučení: **než sáhnu po nástroji, zeptat se, čím to dělá hráč.**
Sáhl jsem po nml, protože je obvyklejší. Nebylo to na mně.

## Slovník materiálů v `glb3letadlo.py` je prázdný

Byl psaný na autíčka (`pneu`, `disky`, `korba`, `poklice`…) a na
raketoplánu se buď netrefil vůbec (kořenový model), nebo se trefil na
špatné díly — modrá „pneu“ přistála na motorech, žluté „disky“ na
panelech. Hráč řekl smazat, pošle ho, až budeme dělat auta. Mechanika
v skriptu zůstala, stačí slovník zase naplnit.

### Na co jsem u yaglu naletěl (2026-09-11)

Když jsem skládal `shuttle.grf`, spadlo to čtyřikrát za sebou. Pro příště:

1. **`yagl_version:` musí sedět s buildem.** Tenhle build hlásí prázdný
   řetězec, takže `yagl_version: "";`. Opsat verzi odjinud = chyba.
2. **`version: GRF8;`, ne `version: 8;`** v bloku `grf`. Je to výčtová
   hodnota, ne číslo.
3. **Pozadí spritesheetu musí být neprůhledná bílá** `(255,255,255,255)`.
   Yagl si kontroluje okraj kolem každého obdélníku; průhledné pozadí
   hlásí jako „non-white pixels in its border“.
4. **Uvnitř obdélníku naopak čistá bílá být nesmí** — znamená „tady
   sprite není“. Průhlednost se dělá alfou; RGB pod ní dávat modrou
   `(0,0,255,0)`, jak to má yagl ve svých 8bpp listech. A kdyby model
   měl opravdu bílou plochu, srazit ji na `254`.
5. **Nahraný soubor s prefixem yagl nenajde.** `64b74c3c-neco.grf`
   hlásí „does not exist“. Přejmenovat na čisté jméno.

Hotové v `shuttle/`. Round-trip sedí: složit → rozebrat → vlastnosti,
rozměry i posuny spritů zůstanou.

### `climate_availability: null` = vozidlo nikdy neuvidíš (2026-09-11)

`shuttle.grf` se načetl, v seznamu grafik svítil zeleně, **žádná chyba**
— a v nákupním menu v depu nebyl. Příčina: opsal jsem
`climate_availability: null;` z `kaas_planes`, aniž bych se podíval,
co to znamená. **`null` = žádné klima**, ne „všechna".

Hra to řeší jedním řádkem v `newgrf.cpp:1250`:

```cpp
if (!e->info.climates.Test(_settings_game.game_creation.landscape)) continue;
```

Vozidlo se prostě přeskočí. Nic nehlásí. Správně je výčet:
`Temperate | Arctic | Tropical | Toyland` — přesně jak to má hráčův
funkční `VWT1cargo.yagl`.

**Ponaučení: nekopírovat hodnoty z cizího GRF bez ověření, co znamenají.**
Předlohu mám mít v hráčově vlastním funkčním souboru, ne v prvním
cizím, co je po ruce. `kaas_planes` má 35 záznamů Action06, kterými si
vlastnosti přepisuje za běhu — proto mu `null` nevadí.

**Zelené GRF bez chybové hlášky neznamená, že je vozidlo vidět.**
Načtení a dostupnost jsou dvě různé věci.

## Fáze letu se fotí zvlášť — CZTR planeset (2026-09-12)

Rozebráno z `CZTR_Plane_set.grf` (58 MB, dekódování 19 s).

**Osm spritů = osm SMĚRŮ jedné fáze. Ne fáze.** CZTR má **398 sad po
8 spritech**. Každé letadlo má několik sad a přepíná mezi nimi podle
proměnné `0xE2`. Typický přepínač u nich vypadá takhle:

```
value1 = variable[0xE2] & 0x000000FF;
ranges:
    0x0C..0x0D: 0x00FA    // 12-13 = rozjezd po draze -> sada "na zemi"
    0x0F:       0x00F8    // 15 = CLIMBING            -> sada "stoupani"
    0x10..0x15: 0x00F9    // 16-21 = let a klesani    -> sada "let"
default:        0x00FA
```

Takže tři sady po osmi spritech na letadlo: **na zemi / stoupání / let**.
Zvednutý čumák při vzletu je **stav 15 (CLIMBING)** a chce vlastních
osm spritů, vyrenderovaných s modelem nakloněným nosem vzhůru.

**My máme jen jednu sadu**, proto shuttle letí pořád naplocho. Není to
chyba úhlů — sprity 2 a 6 jsou směry E a W, ne vzlet.

Jak to dorenderovat: v `glb3letadlo.py` je na to `HILL_TILT_DEGREES`.
Naklání „gramofon" kolem osy X, což je přesně osa klopení. U aut byl
`-23` (do kopce), u letadla jsem ho dal na nulu. **Na sadu pro stoupání
stačí kladná hodnota** a vyrenderovat druhý průchod.

CZTR používá i `0xB4` (rychlost) 20×, `0x44` (výška nad stínem) 3×
a `0x46`/`0x47`/`0x49` na další rozlišení.

## Real_Aircrafts_Betaf.grf je poškozený, ne chráněný (2026-09-12)

Hráč myslel, že je schválně pokažený proti rozbalení. **Není.** Prošel
převodem přes text v UTF-8 a to ho zničilo:

- **23 618 444 výskytů `EF BF BD`** — to je U+FFFD „neznámý znak".
  Zabírá **86 % souboru**. Zdravý CZTR má takový výskyt **jeden**.
- **Všech 166 130 konců řádku má před sebou CR.** Stoprocentní převod
  LF → CRLF, jak to dělá textový režim.
- Na začátku souboru sedí **`# -*- coding: utf-8 -*-\r\n`** — hlavička
  pythonovského zdrojáku. Někdo zapsal binárku přes `open(..., "w")`.
- **Poškození začíná už na 30. bajtu**, uprostřed magické hlavičky,
  a dál je v průměru **každé 4 bajty**. Nejdelší nepoškozený úsek: 372 B.

**Nejde to opravit ničím.** Nahradní znak je jednosměrný: milion různých
původních bajtů se sloučil do jedné trojice. Data nejsou zamíchaná,
prostě nejsou. Žádná úprava yaglu s tím nehne — a nemá smysl ji psát.
Jediná cesta je sehnat nepoškozenou kopii.

### Klopení: znaménko se musí ověřit, ne odvodit (2026-09-12)

Sady na stoupání a klesání se dělají `HILL_TILT_DEGREES`. U raketoplánu
(`glbobj/Shuttle.glb`) vyšlo:

| hodnota | co to udělá | stav `0xE2` |
|---|---|---|
| `0` | rovný let | výchozí |
| **`-12`** | **čumák nahoru — stoupání** | 15 |
| **`+12`** | **čumák dolů — klesání** | 21 |

**Je to obráceně, než říká původní komentář u aut** („kladné = do
kopce"). Nezáleží to na skriptu, ale na tom, kterým koncem model v GLB
leží — stejně jako u počátečního posunu směrů.

Jak jsem to určil: hráč řekl, že **raketoplán má vzadu modré trysky**.
Vyrenderoval jsem obě znaménka, podíval se na boční pohledy (směr E a W,
tam je klopení nejlíp vidět) a při `-12` jsou trysky dole a červený
čumák nahoře. U nového modelu se to musí ověřit znovu, ne odvodit.

Sady leží v `glb/render-test/vzlet/` a `glb/render-test/pristani/`.

### Když se přepínač 0xE2 „neprojeví" (2026-09-12)

První pokus se třemi sadami (rovně / stoupání 15 / klesání 21) se ve hře
neprojevil vůbec — čumák pořád rovně. **Prošel jsem to až na bajty
a GRF bylo správně:**

```
nase:  02 03 FF 89 E2 00 FF 00 00 00 02 F1 00 0F.. 0F.. F2 00 15.. 15.. F0 00
CZTR:  02 03 FA 89 E2 00 FF 00 00 00 03 FA 00 0C.. 0D.. F8 00 0F.. 0F.. F9 00 10.. 15.. FA 00
```

Stejný tvar. Action03 taky (`03 03 01 29 00 FF 00`). A proměnná je
v `newgrf_engine.cpp` u letadel dostupná — dřívější `switch` ji pustí
dál (`case 0x62: break; // vehicle specific, see below`).

**Co z toho plyne:** kdyby se řetěz nerozřešil, hra by spadla na původní
TTD grafiku a raketoplán by zmizel. On se zobrazoval. Takže přepínač
běžel a vracel výchozí větev — tedy hra prostě **nebyla ve stavu 15
ani 21** v okamžiku, kdy se hráč díval.

Nejpravděpodobnější důvod: **stav 15 u rychlého letadla probleskne za
zlomek vteřiny.** Měli jsme 480 mph.

Řešení převzaté z CZTR (hráč: *„na konci dráhy zvedne čumak jen trošku
a pak ve vzduchu víc"*): přidat sadu i pro **12-13, rozjezd po dráze** —
ta fáze trvá dlouho a je vidět. A srazit rychlost.

**Ponaučení: „neprojevuje se to" nemusí znamenat rozbitou strukturu.**
Než začnu přepisovat, ověřit, jestli se ten stav vůbec na dost dlouho
nastane.

### Co je u přepínače 0xE2 prověřené a co ne (2026-09-12)

Čtyřfázová verze se taky neprojevila. **Prověřeno a v pořádku:**

| co | jak ověřeno |
|---|---|
| Action01 | `01 03 04 FF 08 00` = 4 sady po 8 spritech, tvar jako CZTR |
| Action02 basic | `02 03 F0 01 01 00 00 00 00`, čtyři skupiny, každá na svou sadu |
| Action02 switch | bajt po bajtu stejný tvar jako fungující CZTR |
| Action03 | `03 03 01 29 00 FF 00`, ukazuje na přepínač |
| proměnná 0xE2 | v `newgrf_engine.cpp` se k letadlům dostane, dřívější switch ji pustí (`case 0x62: break`) |
| kešování spritu | `vehicle_base.h:1254` překresluje jen při změně směru, **ale** `is_viewport_candidate` to u viditelného letadla obchází |
| čísla stavů | 15 = CLIMBING, 21 = FLIGHT_DESCENT, ověřeno z výčtu |

**Takže chyba je někde jinde, než jsem hledal.** Místo dalšího hádání
jsem postavil `shuttletest.grf`: přepínač dává čumák nahoru **všem
pozemním stavům (0-11)**. Stojící a pojíždějící letadlo je na obrazovce
dlouho — když to nebude vidět, přepínač se nevyhodnocuje vůbec a chyba
není v číslech stavů. Když to vidět bude, čísla stavů jsou správně a
problém je v tom, že 15 a 21 netrvají dost dlouho.

**Ponaučení: dřív si postavit test, který odděluje dvě možnosti, než
opakovaně ladit tu, kterou zrovna podezřívám.** Stálo to hráče dvě kola
zkoušení nazdařbůh.

### Přepínač 0xE2 — co je vyloučeno a co zbývá (2026-09-12, jen hledání)

Diagnostický build `shuttletest.grf` (čumák nahoru pro pozemní stavy
0–11) se **neprojevil ani u stojícího letadla**. Hráč potvrdil, že CZTR
čumák v tomhle buildu zvedá. Prošel jsem všechno staticky, nic neměnil:

| co | výsledek |
|---|---|
| fork vs čisté 16.0-beta2 | rozdíly v `newgrf_engine.cpp` jen vagonová výjimka (0x47/0x72), `vehicle_base.h` jen `IsWrecked`, `aircraft_cmd.cpp` nálet + hangár, `newgrf_act2/3.cpp` **beze změny**. Letadla neovlivňuje. |
| vagonová výjimka forku | platí jen pro `IsWagonCargoExceptionWagon` (jeden GRF, jen vagony); `CollectDrawnCargoSlots` kontroluje `variable == 0x47` |
| CZTR řetěz u letadla 0x29 | Action03 → přepínač na 0x0C → default → **přepínač na 0xE2** (PrimaryDWord, `& 0xFF`) → základní skupiny. Stejný tvar jako můj. **CZTR taky používá nová ID (0x29–0x8C).** |
| load spritů | jen `zin4` 32bpp stačí, `ResizeSprites` dopočítá, 8bpp blitter dostane převod (`spritecache.cpp:480`) |
| keš spritu | `revalidate_before_draw` se spotřebuje při kreslení (`vehicle.cpp:1210`); viditelné vozidlo se přeřeší |
| var 0xE2 dispatch | generický switch má `case 0x62: break` → doteče k letadlovému; `MapAircraftMovementState` pro stojící letadlo vrací 0/1/2/3/4/7 — vše v 0–11 |
| Action03 parser | `IsValidGroupID(0xFF)` projde; default group se nastaví; `SetEngineGRF` |
| ID kolize | `dynamic_engines` default **true** → shuttle.grf a shuttletest.grf mají oddělené motory |
| kaas / c919 | **0xE2 pro sprity nepoužívají** — kaas jen v callbackách, c919 jen 0xF2 (livery). CZTR je jediná reference. |

**Logika, která zbývá:** hráč vidí *moje* sprity (jinak by spadlo na
stock letadlo přes `original_image_index`) → řetěz je připojený → kořen
je přepínač → přepínač běží a vrací default → hodnota 0xE2 není v 0–11.
Pro stojící letadlo to umožňuje jedině **18** (`GetTargetAirportIfValid
== nullptr`). Jenže to by platilo i pro CZTR ve stejné hře. Proto je
stejně pravděpodobné, že **pozorované letadlo nebylo ShuttleTEST**:
přidat nové GRF do rozehrané hry dovolí hra jen s
`newgrf_developer_tools` (`UserIsAllowedToChangeNewGRFs`).

**Dva testy zdarma, bez buildu:**
1. Jmenovalo se sledované letadlo *ShuttleTEST*? Když *Shuttle*, byl to
   starý GRF.
2. Ikona v nákupním seznamu: s `v == nullptr` je 0xE2 nedostupná →
   `error_group` = **první range** = u shuttletest sada „čumák nahoru".
   Ikona v depu tedy musí být nakloněná. Rovná ikona = řetěz není
   připojený. Nakloněná = řetěz jede, jen hodnota nesedí.

**Navržený další build (až hráč řekne):** „žebřík" — 18 → čumák dolů,
12–13 → mírně nahoru, 15 → nahoru, default rovně. Jeden pohled prozradí
skutečnou hodnotu.

Inspektor NewGRF ve hře 0xE2 **neukazuje** (jen 0x40–0x63), ale ukazuje
0x44, jehož spodní bajt je typ cílového letiště přes
`GetTargetAirportIfValid` — nepřímý test platnosti cíle.
