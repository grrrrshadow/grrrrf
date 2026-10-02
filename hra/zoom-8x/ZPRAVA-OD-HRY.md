# Zpráva od hry: 8× zoom je ve hře (forclaude `51428e5`), GRF může nést sprity v 8× (zin8)

Hráč: *„zinc8 uděláme, jo, to není problém“*, *„máme yagl, kterej to zvládne, až budem potřebovat, tak to yagl naučíme“*.

## Co je ve hře

- Nový stupeň přiblížení **8×** (`ZoomLevel::In8x`) nad původními 4×. Zapíná se v nastavení Rozhraní → Grafika →
  „Maximální úroveň přiblížení: 8x“ (`zoom_min = 0` v cfg). Výchozí zůstává 4×, aby to nikomu nebralo paměť.
- Bez 8× spritů v GRF hra v 8× kreslí 4× sprity zdvojené (každý pixel 2×2). Nic se nerozbije, jen to není ostřejší.
- Vnitřní souřadnice pohledu jsou teď v osminách pixelu (dřív ve čtvrtinách). Pro GRF se nic nemění, posuny
  spritů (`x_offs`, `y_offs`) jsou dál v pixelech dané úrovně.

## Jak zapsat 8× sprite do GRF (náš formát)

Kontejner verze 2, hlavička obrázku v datové sekci: `id (4 B) | délka (4 B) | barvy (1 B) | zoom (1 B) | výška (2 B) | šířka (2 B) | x_offs (2 B) | y_offs (2 B) | data`.

| zoom byte | úroveň | poznámka |
|---|---|---|
| 0 | 1× (normální) | NewGRF |
| 1 | 4× (zin4) | NewGRF |
| 2 | 2× (zin2) | NewGRF |
| 3, 4, 5 | 1/2, 1/4, 1/8 | NewGRF |
| **6** | **8× (zin8)** | **jen naše hra** (`spriteloader/grf.cpp`, `zoom_lvl_map[6]`) |

- V 8× má políčko **512 × 256 px**, severní roh je ve hře o 8 px vpravo od rohu renderu (u 4× to byly 4 px).
  Rohy pozemku v JSONu pro 8× render jsou dvojnásobek těch pro 4× (gymnázium: sever (720, 464), východ (1232, 720),
  západ (208, 720), jih (720, 976) na obrázku 1440 × 1440).
- `x_offs`, `y_offs` 8× spritu jsou v 8× pixelech, tedy dvojnásobek 4× hodnot. Hra kontroluje, že `šířka_8x == 2 × šířka_4x`
  (zaokrouhleno nahoru), jinak sprite dorovná paddingem; nejlíp ať 8× render je přesně 2× rozměr 4× renderu.
- Vanilla, JGRPP i nforenum/grfcodec kód 6 neznají: vanila takový sprite přeskočí (`is_wanted_zoom_lvl = false`
  pro neznámý kód), GRF jim dál funguje se 4×.
- Hra 8× sprite načte jen když má hráč „Nejvyšší rozlišení spritů“ na 8x (výchozí) a GRF ho má; s nastavením 4x
  a níž ho přeskočí (`AllowZoomMin4x`), jako dnes přeskakuje 4× při nastavení 2x.

## Na co dát pozor

- **Paměť:** 8× 32bpp sprite má 4× tolik pixelů co 4×. Pro pár budov (gymnázium, automat, socha, plantáž) to je v pořádku,
  pro auta (stovky spritů × směry × livery) ne. Auta nechte ve 4×, v 8× budou zdvojená.
- Zatím ve hře žádné 8× sprity nejsou; naše budovy v `openttd.grf` jsou 4× a hra je v 8× zdvojí. Až pošlete 8× rendery,
  přidám je do základní grafiky hry vedle 4× (skript `openttd_budovy.py` to umí rozšířit).
