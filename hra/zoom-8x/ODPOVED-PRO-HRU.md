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
