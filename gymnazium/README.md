# Dívčí gymnázium (2 × 2 políčka)

Hráč 1. 10.: *„uděláme budovu školy, dívčí gymnázium, 2x2 políčka, nízká budova, něco okolo budovy hřiště
park“*, *„jenom obrázek a vedle ve forclaude to zabudujem do základního průmyslu hry“*, *„jo to je hezký, pak si
budovu zarovnáme sprit na dlaždice“*.

Vlastní model, žádný cizí: `render_gymnazium.py` ho postaví v Blenderu (modul `bpy`) a vyfotí.

- **Budova:** dvoupatrová, okrová omítka, bílé římsy a lizény, šedý sokl, valbová střecha z pálených tašek se
  dvěma komíny. Uprostřed průčelí rizalit se štítem a kulatým oknem, vstup po třech schodech, nad dveřmi nápis
  DÍVČÍ GYMNÁZIUM, vedle stožár s vlajkou. 22 × 10,6 m, okap 8,3 m, hřeben 11,4 m.
- **Okolí:** vlevo hřiště s červeným povrchem, čarami a dvěma koši, vpravo park s kruhovým náměstíčkem, záhonem,
  lavičkami a keři, tři stromy, lampy u cesty, dlažba před budovou, kolem živý plot s mezerami pro cesty.
- **Měřítko a kamera jako u aut** (vejtřaska, Tatra): 12,2 px/m v přiblížení 4×, políčko 14,84 m, kamera 30°
  shora, světlo jako u Tatry se silnějšími stíny. Stín na trávu je v obrázku na 55 % (průhledně černý).
- Tráva pod budovou je průhledná, je vidět tráva hry. Všechno je uvnitř pozemku.

| soubor | co to je |
|---|---|
| `gymnazium_zin4.png` | celý obrázek, 720 × 720 px, 32 bpp s průhledností, přiblížení 4× |
| `gymnazium_zin4.json` | kde jsou na obrázku rohy pozemku: sever (360, 232), východ (616, 360), západ (104, 360), jih (360, 488) |
| `nahled_ve_hre.png` | obrázek vložený do fotky ze zkušební hry (políčka 46–47 × 16–17, vedle silnice s Tatrou) |

Složit znovu: `python3 render_gymnazium.py <výstup.png>` (128 vzorků, asi 40 s; `SAMPLES=32` na zkoušku).

**Dál:** rozřezat na čtyři sprity, každý na svou dlaždici (hráč: *„pak si budovu zarovnáme sprit na dlaždice“*).
Do hry to zabuduje session hry ve forclaude.
