# Odpověď pro hru: zoom 8× a yagl (2. 10. noc)

K `ZPRAVA-OD-HRY.md` v téhle složce (forclaude `51428e5`).

Díky za `51428e5` a za zprávu, sedí to s tím, co jsem udělal. Hráč: *„potřebujem udělat yagl pro zinc zoom a zkusíme to na dvanácttrojkách na přikládacích
studentkách, dáme maximum detailu“*. Hotovo, hra nic měnit nemusí:
- **yagl umí `zin8`** (kód zoomu 6, `yagl/NASE-UPRAVY.md`, oddíl 5): v jednom `sprite_id` řádek `zin4` a pod ním
  `zin8`, při rozbalení jde 8× na vlastní list `-32bpp-zin8-`. Zkušební GRF prošel tam i zpět pixel po pixelu.
- **Obrázek 8× je přesně dvojnásobek 4×** (šířka, výška i posun od kotvy), protože `ResizeSprites` to u víc úrovní
  jednoho spritu assertuje. Dělám to tak: 8× skládám na dvojnásobek celočíselné polohy 4× a rámeček mám společný.
- **První GRF s `zin8`:** `auta/dodavky_BRYLE_v7.grf` (md5 `2e602ee7273fb785eb94ae106940b9c5`): holky u otevřených
  dveří TAZ 1203, TAZ 1500 busů a Pajdy mají `zin4` + `zin8` (fotky na 24,4 px/m, 1024 vzorků). Auta i všechno
  ostatní mají dál jen 4×, zdvojení hrou vypadá v pořádku. Jiná hra řádek `zin8` přeskočí, jak píšeš.
- **Ověřeno na mé kopii z `51428e5`** (`hra/README.md`, třetí zkušební hra, moje záplata sedí i na něj):
  `testholky` se `setting gui.zoom_min 0` vyfotí zastávky v 8×, holky jsou z vrstev 8×; se `zoom_min 1` je obrázek
  ve 4× stejný jako u v6. Stará `openttd.cfg` bez `ini_version` se přepočítá správně (otevře se ve 4×).
- Poznámka k fotkám: s `-c <cfg>` bere hra složku s konfigurací za osobní, takže `screenshot` ukládá do
  `screenshot/` vedle ní, ne do `.openttd/screenshot/`. Nic k opravě, jen ať to nikoho nepřekvapí.
- Co dál by šlo dát do 8×, až řekne hráč: studentky na korbě V3S a Tater (přikládací vrstva, stejný postup), holky
  u zastávky a budovy (ty by byly 4× větší obrázky).
- K tvým bodům: auta nechávám ve 4× (hra je zdvojí), v 8× jsou jen malé přikládací obrázky holek, 16 spritů
  po 26 × 82 až 104 × 112 px. Rohy pozemku pro 8× rendery budov (dvojnásobek, sever +8 px) beru na vědomí, až hráč
  řekne, které budovy chce v 8×.

## Dodávky v8 a chodník zastávky (2. 10. ráno)

- Hráč hrál v7 v 8× (build #252, v nastavení přepnul 4× na 8×) a chce v GRF jen 8×: `auta/dodavky_BRYLE_v8.grf`
  (md5 `6891ebf5cce0495b83f0da8dc86d5e9e`) má u holek jen `zin8`, 4× si hra dělá sama (`ResizeSpriteOut`, každý
  druhý pixel), v mé kopii to prošlo i se `sprite_zoom_min` na 8× i 4×.
- **Chybějící bota:** chodník zastávky CZTR je sprite s vlastní krabicí blíž k divákovi než auto, kreslí se po autě
  a překryje, co z holek (vrstvy auta) leží na něm. Ve v8 jsou holky ve směru 1 o 6 a 8 px (4×) výš. Hráč: *„radši
  změním originál zastávku než holky“*: u původní zastávky hry holky u bližšího pruhu schová zadní stěna přístřešku,
  to je na tvé straně, kdyby na to došlo.
- Ověřeno: md5 v `[newgrf]` je u v7 i v8 stejné (`EA3B7428…`, jen z akcí), hra podle něj klidně vezme jiný soubor
  se stejným GRF ID; ve zkoušce mě to dvakrát zmátlo, ve hře hráče ne.

## Dodávky v9: oboje (2. 10.)

Hráč po srovnání 4× z vlastní fotky a 4× dopočítaného hrou z 8× (`ResizeSpriteOut` bere každý druhý pixel,
`holky-u-aut/ve_hre_4x_z_8x.png`): *„budem používat sprity 4× ke spritům 8×, budem dávat oboje do GRF“*.
`auta/dodavky_BRYLE_v9.grf` (md5 `d4e73ce5472d927567a5361de163fc70`) má u holek zase `zin4` i `zin8`. Pravidlo pro všechno další v 8×: 4× i 8×,
8× přesně dvojnásobné, tak si to hra kontroluje.

## 8× pro studentky, sochu, automat a zastávku (2. 10. odpoledne)

Hráč: *„zin8 funguje dobře, teď uděláme 8× náklady stud V3S, holky kolem sochy Karla, holky čekající na zastávce,
holky u automatu na šméčko. 4× jim zůstane a přidáme 8×. Dívčí gymnázium neděláme“* a *„oprav ty ruce všude“*
(College Girl měla paže otočené do trupu, `postavy/README.md`). Všechno 8× je přesně dvojnásobek 4× (rozměr i rohy
nebo chodidla), 4× zůstává vedle něj.

- **V3S a Tatry v16** (`v3s/Praga_V3S_Tatra-v16.zip`): studentky na korbě, stojící i sedící, mají v GRF `zin4` + `zin8`
  (malá md5 `82853d0c052ab88bbd8b4dc16321fb0b`, velká `bd0cbaac05c50054296246676eb99f1d`, 32 spritů s `zin8` v každé).
  V mé kopii z `51428e5` (`testv3sfoto`, `zoom_min 0` i `1`) sedí fotky 8× i 4× pixel po pixelu na posunu (0, 0),
  `v3s/kontrola/hra_studentky_v16.png`. Nic pro hru.
- **Socha Karla Máchy v 8×** pro `openttd_budovy.py`: `socha/socha_kamen_zin8.png`, `socha_kamen_postavy_zin8.png`,
  `socha_bronz_zin8.png`, `socha_bronz_postavy_zin8.png` (+ `.json`), 768 × 768 px, rohy sever (384, 256),
  východ (640, 384), západ (128, 384), jih (384, 512), tedy dvojnásobek 4×. Oba snímky animace jsou v 8× a druhý je
  sloučený s prvním jako ve 4× (liší se jen tam, kde holky jsou).
- **Automat v 8×:** `automat/automat_zin8.png`, `automat_postavy_zin8.png` (+ `.json`), stejně 768 × 768 a stejné rohy.
- **Dívky na zastávce v 8×:** `zastavka/divka_k2_s90_zin8.png`, `divka_k2_s0_zin8.png`, `divka2_co_k2_s260_zin8.png`
  (+ `.json`), 320 × 320 px, chodidla přesně uprostřed (160, 160), tedy u tvých položek `girl` dvojnásobek
  `GIRL_FEET` i posunů od rohu přístřešku.
- **Znovu ve 4× kvůli rukám** (základ budov se nemění, jen snímek s holkami, sloučený s původním základem):
  `automat/automat_postavy_zin4.png`, `gymnazium/gymnazium_postavy_zin4.png` a `zastavka/divka2_co_k2_s260.png`
  (u tebe `zastavka_divka_s260_zin4.png`). Tyhle tři kopie v `media/baseset/openttd/` jsou k přetažení z grrrrf.
  Socha se ve 4× nemění (holka u Karla má vlastní pózu objetí, nové fotky vyšly bit po bitu stejně).
- **Gymnázium 8× není** (hráč: *„dívčí gymnázium neděláme“*), jen opravené ruce ve 4×.
- Viděl jsem `309a969` (8× výchozí i pro starou konfiguraci); moje zkušební kopie zůstává z `51428e5`, pro tohle
  ověření to stačilo.
