# Automat na marihuanu (1 políčko)

Hráč 1. 10. s fotkami automatů CBD MAT: *„ještě udělej 1x1 políčko automat na marihuanu s lavičkou a keříčkem
křoví“*, pak *„to máš obdélníček, něco jako 2x1 políčko“*, *„lavičku postav před automat, otoč ji sedadlem
k automatu a máš čtverec“*. Jen obrázek jako u gymnázia, do hry ho zabuduje session hry ve forclaude.

Vlastní model, žádný cizí: `render_automat.py` ho postaví v Blenderu a vyfotí. Kamera, měřítko a světlo jako
gymnázium (`gymnazium/`) a auta: 12,2 px/m v přiblížení 4×, políčko 14,84 m, stín na trávu na 55 %.

- **Automat podle fotek:** tmavě šedá skříň 90 × 85 × 183 cm na nožičkách. Vpředu prosklená dvířka se šesti
  policemi balíčků, svítícím pásem LED a nálepkou POZOR, vpravo zelený pruh s ceníkem, čtečkou karet, displejem,
  klávesnicí a mincemi, dole výdejní klapka se zeleným štítkem PULL. Bok polepený zelenou fólií s listy konopí,
  paprsky a bílým nápisem CBD MAT. Polep a předek kreslí skript sám (`textury/bok.png`, `textury/predek.png`).
- **Kolem, do čtverce:** automat vzadu, lavička před ním sedadlem k automatu, hrbolatý keřík vpravo vedle
  automatu, pod tím čtverec 4 × 4 m betonové dlažby 50 cm se spárami a obrubníkem, uprostřed políčka.
  Předek automatu míří k jihozápadu (na obrázku doleva dolů), bok s polepem k jihovýchodu.
- Ve skutečné velikosti je automat při přiblížení 4× jen asi 15 × 20 px. Proto i dvakrát větší skupina
  (`MERITKO=2`, i s dlažbou 8 × 8 m), vedle aut je ale velká: automat 3,7 m, lavička 3,2 m. Hráč vybere.

| soubor | co to je |
|---|---|
| `automat_zin4.png` | skutečná velikost, 384 × 384 px, 32 bpp s průhledností, přiblížení 4× |
| `automat_2x_zin4.png` | totéž dvakrát větší |
| `*_zin4.json` | rohy políčka na obrázku: sever (192, 128), východ (320, 192), západ (64, 192), jih (192, 256) |
| `nahled_ve_hre.png` | obě velikosti ve fotce ze zkušební hry u silnice s Tatrami, zvětšeno 2× |

Složit znovu: `python3 render_automat.py <výstup.png>`, dvakrát větší `MERITKO=2 python3 render_automat.py …`.
