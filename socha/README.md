# Socha Karla Máchy (1 políčko)

Hráč 1. 10.: *„udělej Karel Mácha statue, políčko 1x1 sochu uprostřed, šedou z kamene a bronzovou, karel mácha bude
mít kapucu, vousy a obrovskýho džonta v ruce, ruce bude mít od sebe jako by se chystal obejmout něco velkýho, okolo
lavičky, malé křovíčko, odpaďák, odpadky“*. Pak *„ruce trochu níž, ne podél těla, asi tak něco mezi tím, vousy po
pupek dlouhý a jointa víc do trychtýře, zvýraznit trychtýřovitost, širší na konci“* (předtím to byl *„americký džont
typu fat“*) a *„mnohem méně stínů“*. Jen obrázek jako u gymnázia a automatu, do hry ho zabuduje session hry ve forclaude.

Vlastní model, žádný cizí: `render_socha.py` ho postaví v Blenderu a vyfotí. Kamera jako u automatu (`automat/`).
**Stíny mnohem slabší než u automatu:** slabší slunce, silnější světlo okolí a stín na trávu jen 20 % (automat 55 %).

- **Karel Mácha:** v mikině s kapucí nasazenou na hlavě, obličej v ní zapadlý, knír a plnovous s prameny až po
  pupek, pod ním klokaní kapsa. Ruce od sebe, jako by se chystal obejmout něco velkého, ale níž: ne podél těla,
  nadloktí šikmo dolů do stran, dlaně ve výšce hrudi. V pravé ruce obrovský joint jako trychtýř: u prstů tenký
  filtr, pak rovný kužel, který se rozevírá až do širokého konce, ten je useknutý a uprostřed zakroucený do malé
  špičky. Stojí čelem k divákovi (k jihu).
- **Dvě verze:** šedá z kamene a bronzová (kov se zelenavou patinou na místech). U kamenné jsou vousy hrubě tesané
  a o kousek tmavší, jinak by se při slabých stínech ztratily na mikině. Jinak jsou obě stejné.
- **Joint hoří** (hráč: *„uděláme na konci žhavej popel a dým z džonta“*, *„červený body v tom žhavym“*): na
  širokém konci je místo zakroucené špičky nízká kupka popela, na ní žhaví oranžová místa s červenými body, a z ní
  stoupá tenký pramen kouře, nahoře se rozšiřuje, řídne a stáčí stranou od Karlovy hlavy.
- **Podstavec** ze žuly: schod, kvádr a římsa, nahoře 1,4 m. Na obou předních stěnách (ty, co jsou vidět)
  bronzová deska s vystouplým nápisem KAREL MÁCHA.
- **Kolem:** náměstíčko z dlaždic 50 cm s obrubníkem uprostřed políčka. Tři lavičky čelem k soše: dvě za ní,
  jedna vpravo vpředu; vlevo vpředu je volno, aby byla vidět deska. Vedle pravé zadní lavičky zelený koš,
  plný až přes okraj. **Odpadky** jako u automatu (papíry, sáčky, plechovky, PET lahve, kelímky, zelené balíčky
  z automatu), nejvíc kolem koše a pod lavičkami, pod podstavcem nic. Kolem dlažby až k okraji políčka **tmavě
  zelený pás nízkých keřů** (hráč: *„to křoví je stejnou barvou jako zem, zaniká, udělej tam tmavou zelenou okolo
  dlažby“*).
- **Rostliny marihuany** (hráč: *„kytky rostou 5 metrů vysoko, na severovýchodní a severozápadní straně můžou být
  kytky marihuany velký jako socha“*, *„dopředu malý, velký SV a SZ dozadu za lavičky“*, *„odstín zelené z nákladu
  MARI“*): za oběma zadními lavičkami a v rohu mezi nimi pět velkých, 4,3 až 5 m, vpředu v pásu keřů šest malých,
  1,2 až 1,4 m. Zelené jako kupka MARI na korbě V3S, světlejší než keře. Koruny velkých jsou jen 0,9 m od kmene,
  aby nesahaly na operadla a dívky, a žádná rostlina nepřečuhuje do stran ani pod přední hranu, jen nahoru.
- **Dvakrát větší** jako automat: postava i s kapucí asi 4,8 m, s podstavcem 7,6 m, náměstíčko 11,2 × 11,2 m
  (políčko má 14,8 m). Ve skutečné velikosti by postava měla při přiblížení 4× jen asi 25 px.

## Druhý obrázek do animace: s postavami

Hráč: *„uděláme animaci, tahle socha bez objektů se bude střídat s obrázkem s objekty“*, *„bikini girl jako že kráčí
tam, kde by byla čtvrtá lavička, college girl vyleze na sochu, obejme Karla a dá mu pusu, na lavičky zbytek:
dvě na jednu lavičku, jednu na jednu a na třetí nezbyde“*, *„měřítko k lavičce“*.

- **Na podstavci:** dívka ve školní uniformě (College Girl) stojí Karlovi po levici, čelem k němu, objímá ho
  a hlavu má zvednutou k němu. Pusa vidět není.
- **Kráčí:** dívka v bikinách jde přes náměstíčko vlevo vpředu, kde by byla čtvrtá lavička, posunutá kousek
  k jihovýchodu, aby neměla hlavu u nohou dívky na lavičce. Model stojí jako modelka (nohy od sebe, hlava zakloněná
  k nebi), proto jsou jí nohy srovnané pod kyčle do krátkého klidného kroku a hlava narovnaná dopředu. Jde šikmo
  k divákovi (hráč: *„zdá se mi nepřirozená, klidně ji nějak pootoč“*).
- **Na lavičkách:** na severozápadní (vlevo nahoře) dvě, bělovlasá anime dívka a dívka v tyrkysovém tílku
  s kabelkou, na severovýchodní (vpravo nahoře) sama zrzavá anime dívka. Jihovýchodní (vpravo dole) zůstala prázdná.
- **Měřítko k lavičce:** dívky mají 1,58 až 1,68 m a jsou dvakrát zvětšené jako lavičky, sedí zadkem na sedáku
  a chodidly na zemi.
- **Bez blikání:** každý render má trochu jiný šum, takže druhý obrázek je sloučený s prvním (`postavy/animace.py`):
  liší se jen tam, kde jsou postavy a jejich stíny. Ani z postav nic nepřečuhuje na vedlejší dlaždice.
- **Modely:** pět dívek od hráče (`postavy/`, Sketchfab, CC BY 4.0), autoři a text uvedení pro hru jsou
  v `AUTORI-MODELU.md` v oddílu „Postavy u sochy Karla Máchy“. Posazení a pózy dělá `postavy/postavy.py`.

| soubor | co to je |
|---|---|
| `socha_kamen_zin4.png` | šedá z kamene, 384 × 384 px, 32 bpp s průhledností, přiblížení 4× |
| `socha_bronz_zin4.png` | bronzová, totéž |
| `socha_kamen_zin4.json`, `socha_bronz_zin4.json` | rohy políčka na obrázku: sever (192, 128), východ (320, 192), západ (64, 192), jih (192, 256) |
| `nahled_ve_hre.png` | obě sochy ve fotce ze zkušební hry u silnice s Tatrami, zvětšeno 2× |
| `zblizka.png` | obě sochy vedle sebe zblízka |
| `socha_kamen_postavy_zin4.png`, `socha_bronz_postavy_zin4.png` | druhý obrázek do animace: totéž s postavami, rohy v JSONu stejné |
| `animace_ve_hre.gif` | obě sochy ve fotce ze hry, střídá se bez postav a s postavami |
| `zblizka_postavy.png` | obě sochy s postavami vedle sebe zblízka |

Složit znovu: `SOCHA=kamen python3 render_socha.py <výstup.png>`, bronzová `SOCHA=bronz` (128 vzorků, asi 35 s, výstup s celou cestou).
S postavami `POSTAVY=1 SOCHA=kamen python3 render_socha.py <s_postavami.png>` (asi 45 s) a pak
`python3 ../postavy/animace.py socha_kamen_zin4.png <s_postavami.png> socha_kamen_postavy_zin4.png`.
`MERITKO=1` dá skutečnou velikost, `SLUNCE`, `OKOLI` a `STIN` mění světlo (teď 2,0, 0,9 a 0,2; automat má 5,0, 0,35
a 0,55). Tělo je kostra s modifikátorem Skin a vyhlazením, takže je hladké jako tesané nebo lité; kapuce je
skořepina s otvorem pro obličej, nos, líce s bradou, knír a kapsa jsou elipsoidy. Dlouhé vousy a joint jsou
poskládané z kroužků: vousy leží kousek zanořené na mikině (její předek je změřený přímo z modelu), joint je
kroužek po kroužku podle profilu trychtýře.
