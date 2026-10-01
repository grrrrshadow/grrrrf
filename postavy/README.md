# Postavy do obrázků budov

Pět dívek od hráče (`zip7.zip`, 1. 10.), všechny ze Sketchfabu pod CC BY 4.0. Autoři, odkazy a text uvedení
pro hru jsou v `../AUTORI-MODELU.md` (oddíl „Postavy u sochy Karla Máchy“).

| soubor | model, autor | kostra |
|---|---|---|
| `anime_girl.glb` | Anime Girl, demidrew | ne, stojí jako socha; má černou obrysovou slupku a sama svítí |
| `character_people_girl_001.glb` | Character People Girl 001, kiemtruongkts | ne |
| `college_girl.glb` | College Girl, Rotmill | ano, v souboru jsou čtyři dívky (dvě na kostře, dvě v pevné póze) |
| `galaxia_anime_girl.glb` | Galaxia anime girl, Tatenashi | ano (VRM), navíc v souboru koule |
| `girl_bikini.glb` | Girl Bikini, squalll_999 | ne |

- `postavy.py`: načtení, pózy a postavení do scény. Postavy s kostrou se napozují kostmi a póza se zapeče do
  sítě, postavám bez kostry se ohnou nohy přímo v síti (stehno kolem kyčle, lýtko kolem kolena, hladký přechod).
  `sed()` vybere úhel stehen tak, aby na sedáku 0,47 m došla chodidla na zem.
- `animace.py`: druhý obrázek budovy (s postavami) sloučí s prvním, aby se lišily jen tam, kde postavy jsou.

Použití: socha (`socha/render_socha.py`, `POSTAVY=1`). Pak přijde automat a gymnázium.
