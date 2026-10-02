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
| `gymnazium_postavy_zin4.png` | druhý obrázek do animace: totéž s holkami, rohy v JSONu (`gymnazium_postavy_zin4.json`) stejné |
| `gymnazium_zin8.png`, `gymnazium_postavy_zin8.png` (+ `.json`) | totéž v přiblížení 8× (jen naše hra, `zin8`): 1440 × 1440 px, přesně dvojnásobek 4×; rohy sever (720, 464), východ (1232, 720), západ (208, 720), jih (720, 976) |
| `animace_ve_hre.gif` | gymnázium a automat ve fotce ze hry, střídá se bez holek a s holkami |

Složit znovu: `python3 render_gymnazium.py <výstup.png>` (128 vzorků, asi 40 s; `SAMPLES=32` na zkoušku).

Ve hře je gymnázium od forclaude `2366825`: hra obrázek rozkrájí po políčkách (`openttd_budovy.py`). Render 2 : 1 sedí
na dlaždice, jak je (oprava od hry 1. 10. večer: políčko je 256 × 128, nic se nestahuje; `hra/zarovnani-budov/`).

## Druhý obrázek do animace: holky kolem školy

Hráč 1. 10.: *„spawnem holky kolem školy a automatu“*. Jako u sochy (`socha/`) se ve hře střídá obrázek bez holek
(`gymnazium_zin4.png`, ten, co už hra má) a s holkami (`gymnazium_postavy_zin4.png`).

- **1,5× větší než budova, lavičky taky** (hráč 1. 10. večer: *„škola zvětšit studentky, zvětšíme i lavičky, dveře
  do školy jsou velké dost, můžem zvětšit studentky“*). Holka měří 2,43 až 2,52 m a dveře 2,55 m, takže projde; ve 2×
  (3,2 m) by už neprošla. Všech šest laviček je 1,5× (sedák 0,71 m, délka 2,4 m), proto se změnil i obrázek bez holek.
  Předtím byly holky ve skutečné velikosti (asi 17 px při přiblížení 4×).
- **Na lavičce před školou** (vpravo od vchodu) sedí bělovlasá anime dívka (Galaxia) a dívka v tyrkysovém tílku
  (Character Girl), jako u sochy.
- **Před schody** si povídají dívka v tyrkysovém tílku a tmavovlasá ve školní uniformě (College Girl), z profilu,
  1,2 m od sebe, lampa je na obrázku mezi nimi. Bělovlasá na světlých schodech splývala, proto tam je tmavovlasá.
- **Po hlavní cestě** jde k bráně další tmavovlasá. College Girl má školní uniformu, víc stejných ve škole sedí.
- **Na hřišti** hází tmavovlasá na koš, ruce nahoře, oranžový míč nad nimi.
- **Na zadní lavičce v parku** sedí zrzavá anime dívka (Anime Girl) čelem k divákovi.
- **Bez blikání:** druhý obrázek je sloučený s prvním (`postavy/animace.py`), liší se jen tam, kde jsou holky,
  jejich stíny a pár odlesků v oknech. Nic z nich nepřečuhuje pod přední hrany ani do stran. Z pruhů, jak je hra
  krájí, se mění jen západní (hřiště) a jižní, východní je v obou obrázcích stejný.
- **Modely:** dívky od hráče (`postavy/`, Sketchfab, CC BY 4.0), autoři a text uvedení pro hru jsou
  v `AUTORI-MODELU.md` v oddílu „Postavy u automatu a gymnázia“.

Složit znovu: `python3 render_gymnazium.py <bez_postav.png>` a `POSTAVY=1 python3 render_gymnazium.py <s_postavami.png>`
(asi 30 a 45 s; `LAVICKY` a `POSTAVY_K` mění zvětšení laviček a holek, teď 1,5) a pak
`python3 ../postavy/animace.py <bez_postav.png> <s_postavami.png> gymnazium_postavy_zin4.png`.
Náhled: `hra/nahled_ve_hre.py` se dvěma obrázky na `@46,16` (gymnázium) a `@44,16` (automat), jednou bez holek
a jednou s nimi, a oba snímky do GIFu se společnou paletou.

## Ruce College Girl (2. 10.)

Dvě stojící College Girl (u školy a na schodech) měly paže otočené dovnitř trupu (`postavy/README.md`, oprava ramen
76° → 50°). `gymnazium_postavy_zin4.png` je proto vyfocený znovu, `gymnazium_zin4.png` se nemění.

## Přiblížení 8× (2. 10. odpoledne)

Hráč nejdřív: *„dívčí gymnázium neděláme, neznám současný stav, jak to tam vypadá“*, pak podle snímku z #252:
*„mám v #252 gymnázium ještě malý lavičky a malý holky. Máme už novější zvětšenou verzi? Dáme tam lavičky a holky
velký a pak můžem udělat 8×.“* Hra kolegy má pořád první školu z 1. 10. dopoledne (`7918e29`, holky a lavičky 1×);
zvětšená 1,5× je v repu od 1. 10. večer (`822f355`), stačí si vzít nové soubory.

`ZIN=8 python3 render_gymnazium.py <výstup>` (a s `POSTAVY=1`) fotí stejnou scénu stejnou kamerou na 24,4 px/m do
1440 × 1440 px (políčko 512 px): obrázek i rohy jsou přesně dvojnásobek 4×. Oba snímky animace jsou v 8×, druhý
sloučený s prvním (`postavy/animace.py`) jako ve 4×. Kontrolní 4× render po úpravě skriptu vyšel stejně jako
`gymnazium_zin4.png` v repu.
