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

Složit znovu: `python3 render_automat.py <výstup.png>` (128 vzorků, asi 20 s). `MERITKO=1` dá skutečnou velikost.
Křoví se skládá z koulí přímo v síti (bmesh) s hrbolky ze šumu: stovky samostatných objektů s modifikátory
by Blender zpomalily na desítky minut.
