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

Použití:
- druhé obrázky budov do animace (`POSTAVY=1`): socha (`socha/render_socha.py`), automat (`automat/render_automat.py`)
  a gymnázium (`gymnazium/render_gymnazium.py`);
- `fotka_postavy.py`: jedna dívka samotná na přiložení (zastávka, holky u aut);
- studentky na korbě V3S a Tater (`v3s/render_v3s.py`): stojící (na zastávce) a od verze 14 sedící na lavicích (za jízdy).

`sedici(jmeno)` posadí Galaxii nebo College Girl (kostrou), Character Girl nebo Anime Girl (ohnutím nohou) na sedák 0,47 m jako u sochy
a vrátí bod sedu; `nacti_stojici(jmeno, vyska, poza)` dá stojící.
