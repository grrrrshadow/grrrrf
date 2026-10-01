# Socha Karla Máchy (1 políčko)

Hráč 1. 10.: *„udělej Karel Mácha statue, políčko 1x1 sochu uprostřed, šedou z kamene a bronzovou, karel mácha bude
mít kapucu, vousy a obrovskýho džonta v ruce, ruce bude mít od sebe jako by se chystal obejmout něco velkýho, okolo
lavičky, malé křovíčko, odpaďák, odpadky“*. Jen obrázek jako u gymnázia a automatu, do hry ho zabuduje session hry
ve forclaude.

Vlastní model, žádný cizí: `render_socha.py` ho postaví v Blenderu a vyfotí. Kamera, světlo a stín na trávu
(55 %) jako u automatu (`automat/`), aby k sobě seděly.

- **Karel Mácha:** v mikině s kapucí nasazenou na hlavě, obličej v ní zapadlý, plnovous až na prsa a knír, na
  břiše klokaní kapsa. Ruce roztažené dopředu od sebe, jako by se chystal obejmout něco velkého. V pravé ruce
  obrovský joint: u prstů úzký, na konci široký se zakroucenou špičkou. Stojí čelem k divákovi (k jihu), takže
  roztažené ruce jsou na obrázku vodorovně.
- **Dvě verze:** šedá z kamene a bronzová (kov se zelenavou patinou na místech). Jinak jsou stejné.
- **Podstavec** ze žuly: schod, kvádr a římsa, nahoře 1,4 m. Na obou předních stěnách (ty, co jsou vidět)
  bronzová deska s vystouplým nápisem KAREL MÁCHA.
- **Kolem:** náměstíčko z dlaždic 50 cm s obrubníkem uprostřed políčka. Tři lavičky čelem k soše: dvě za ní,
  jedna vpravo vpředu; vlevo vpředu je volno, aby byla vidět deska. Vedle pravé zadní lavičky zelený koš,
  plný až přes okraj. **Odpadky** jako u automatu (papíry, sáčky, plechovky, PET lahve, kelímky, zelené balíčky
  z automatu), nejvíc kolem koše a pod lavičkami, pod podstavcem nic. **Malé křovíčko** v rozích políčka mimo
  dlažbu (to v severním rohu je schované za sochou).
- **Dvakrát větší** jako automat: postava i s kapucí asi 4,8 m, s podstavcem 7,6 m, náměstíčko 11,2 × 11,2 m
  (políčko má 14,8 m). Ve skutečné velikosti by postava měla při přiblížení 4× jen asi 25 px.

| soubor | co to je |
|---|---|
| `socha_kamen_zin4.png` | šedá z kamene, 384 × 384 px, 32 bpp s průhledností, přiblížení 4× |
| `socha_bronz_zin4.png` | bronzová, totéž |
| `socha_kamen_zin4.json`, `socha_bronz_zin4.json` | rohy políčka na obrázku: sever (192, 128), východ (320, 192), západ (64, 192), jih (192, 256) |
| `nahled_ve_hre.png` | obě sochy ve fotce ze zkušební hry u silnice s Tatrami, zvětšeno 2× |
| `zblizka.png` | obě sochy vedle sebe zblízka |

Složit znovu: `SOCHA=kamen python3 render_socha.py <výstup.png>`, bronzová `SOCHA=bronz` (128 vzorků, asi 20 s).
`MERITKO=1` dá skutečnou velikost. Tělo je kostra s modifikátorem Skin a vyhlazením, takže je hladké jako
tesané nebo lité; kapuce je skořepina s otvorem pro obličej, vousy, nos a kapsa jsou elipsoidy.
