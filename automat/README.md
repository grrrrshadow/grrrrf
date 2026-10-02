# Automat na marihuanu (1 políčko)

Hráč 1. 10. s fotkami automatů CBD MAT: *„ještě udělej 1x1 políčko automat na marihuanu s lavičkou a keříčkem
křoví“*, pak *„lavičku postav před automat, otoč ji sedadlem k automatu a máš čtverec“*, *„2x větší jo, dáme do
rohu políčka a zbytek políčka křoví“*, *„vedle lavičky dej odpadkový koš a odpadky rozházené po zemi“*.
Jen obrázek jako u gymnázia, do hry ho zabuduje session hry ve forclaude.

Vlastní model, žádný cizí: `render_automat.py` ho postaví v Blenderu a vyfotí. Kamera a světlo jako gymnázium
(`gymnazium/`) a auta, stín na trávu na 55 %.

- **Automat podle fotek:** tmavě šedá skříň na nožičkách. Vpředu prosklená dvířka se šesti policemi balíčků,
  svítícím pásem LED a nálepkou POZOR, vpravo zelený pruh s ceníkem, čtečkou karet, displejem, klávesnicí
  a mincemi, dole výdejní klapka se zeleným štítkem PULL. Bok polepený zelenou fólií s listy konopí, paprsky
  a bílým nápisem CBD MAT. Polep a předek kreslí skript sám (`textury/bok.png`, `textury/predek.png`).
- **Do čtverce:** automat vzadu, lavička před ním sedadlem k automatu, keřík vpravo vedle, zelený plechový koš
  vlevo vedle lavičky, plný až přes okraj. Pod tím čtverec betonové dlažby se spárami a obrubníkem.
- **Odpadky** po dlažbě, nejvíc kolem koše a pod lavičkou, pár zafoukaných do křoví: papíry, sáčky, plechovky,
  PET lahve, kelímky a zelené balíčky z automatu.
- **Dvakrát větší** (hráč vybral ze skutečné a dvojnásobné): ve skutečné velikosti by měl automat při přiblížení
  4× jen asi 15 × 20 px. Automat 3,7 m, dlažba 8 × 8 m. Stejně zvětšené je i křoví.
- **V severním rohu políčka** (na obrázku nahoře), dlažba 0,3 m od severních hran. **Zbytek políčka** zarostlý
  divokým neudržovaným křovím v několika zelených, některé keře se suchými hnědými místy, mezi nimi plevel.
  U dlažby je křoví nižší, aby lavička a automat zůstaly vidět. Všechno je uvnitř políčka.

| soubor | co to je |
|---|---|
| `automat_zin4.png` | obrázek, 384 × 384 px, 32 bpp s průhledností, přiblížení 4× |
| `automat_zin4.json` | rohy políčka na obrázku: sever (192, 128), východ (320, 192), západ (64, 192), jih (192, 256) |
| `nahled_ve_hre.png` | obrázek ve fotce ze zkušební hry u silnice s Tatrami, zvětšeno 2× |
| `automat_postavy_zin4.png` | druhý obrázek do animace: totéž s holkami, rohy v JSONu (`automat_postavy_zin4.json`) stejné |
| `automat_zin8.png`, `automat_postavy_zin8.png` | totéž v přiblížení 8× (jen naše hra, `zin8`): 768 × 768 px, přesně dvojnásobek 4×; rohy v `*_zin8.json`: sever (384, 256), východ (640, 384), západ (128, 384), jih (384, 512) |

Složit znovu: `python3 render_automat.py <výstup.png>` (128 vzorků, asi 20 s). `MERITKO=1` dá skutečnou velikost.
Křoví se skládá z koulí přímo v síti (bmesh) s hrbolky ze šumu: stovky samostatných objektů s modifikátory
by Blender zpomalily na desítky minut.

## Druhý obrázek do animace: holky u automatu

Hráč 1. 10.: *„spawnem holky kolem školy a automatu“*. Jako u sochy (`socha/`) se ve hře střídá obrázek bez holek
(`automat_zin4.png`, ten, co už hra má) a s holkami (`automat_postavy_zin4.png`).

- **U automatu platí** tmavovlasá dívka ve školní uniformě (College Girl), zády k divákovi, pravou ruku má
  u zeleného pruhu s placením.
- **Na lavičce sedí** dívka v tyrkysovém tílku (Character Girl), čelem k automatu, blíž ke koši.
- **Vpravo vpředu stojí** bělovlasá anime dívka (Galaxia) čelem k divákovi, jako když odchází s nákupem.
- **Dvakrát větší** jako automat a lavička. Na lavičce sedí zadkem na sedáku a chodidly na zemi.
- **Bez blikání:** druhý obrázek je sloučený s prvním (`postavy/animace.py`), liší se jen tam, kde jsou holky
  a jejich stíny. Nic z nich nepřečuhuje pod přední hrany ani do stran.
- **Modely:** dívky od hráče (`postavy/`, Sketchfab, CC BY 4.0), autoři a text uvedení pro hru jsou
  v `AUTORI-MODELU.md` v oddílu „Postavy u automatu a gymnázia“.

Ukázka střídání ve fotce ze hry, i s gymnáziem: `../gymnazium/animace_ve_hre.gif`.

Složit znovu: `POSTAVY=1 python3 render_automat.py <s_postavami.png>` (asi 20 s) a pak
`python3 ../postavy/animace.py automat_zin4.png <s_postavami.png> automat_postavy_zin4.png`.
Ruku u placení nastavují `PL_DOPREDU`, `PL_DOLU` a `PL_LOKET` (stupně, teď 82, 50 a 70).

## Přiblížení 8× a ruce (2. 10.)

Hráč: *„uděláme 8× holky u automatu na šméčko, 4× jim zůstane a přidáme 8×“*. `ZIN=8 python3 render_automat.py <výstup>`
(a s `POSTAVY=1`) fotí stejnou scénu stejnou kamerou na 24,4 px/m do 768 × 768 px: přesně dvojnásobek 4× i s rohy.
Oba snímky animace jsou v 8×. Zároveň je **levá ruka dívky u placení** otočená o 50° místo 76° (`placeni` v
`render_automat.py`): College Girl má paže v modelu už 25° dolů a větší otočení je dávalo do trupu (hráč: *„na všech
fotkách je asi bez rukou“*, `postavy/README.md`). `automat_postavy_zin4.png` je proto znovu, `automat_zin4.png` je stejný.
