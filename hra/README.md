# Zkušební hra s obrazem

Moje kopie OpenTTD na zkoušení GRF, **ne hra pro hráče**. Přeložená z kopie zdrojáků hry
(`forclaude`, `openttd/`, commit `60283b3` z 16. 9. 2026, jen čteno, nic tam neměněno)
s mými zkušebními příkazy. Uložená sem, ať se příště nemusí 20 minut překládat
(hráč 28. 9.: *„hlavně si to ulož v repu, ať nestavíš znova s grafikou“*).

| soubor | co to je |
|---|---|
| `ottd-zkusebni-gfx.tar.xz` | přeložená hra (SDL2, 32bpp blittery, i `-vnull`), `lang/`, `baseset/`, `ai/`, `game/` a domov `domov/` s OpenGFX 7.1 a čistým `openttd.cfg` |
| `zkusebni-prikazy.patch` | všechny moje změny proti zdrojákům hry (`patch -p1` v kopii `openttd/` na `60283b3`) |
| `cztr_silnice/` | výstřižek silnice CZTR RT14 „1. třída – venkov“ (`CZTR_silnice_RT14.grf`), v domově už je zapsaný, okruh na fotce se staví z ní |
| `zkusebni_mari/` | zkušební náklad `MARI` (`zkusebni_MARI.grf`): tahle stará verze hry ho nemá, ve hře hráče je zabudovaný |
| `zkusebni_naklady/` | zkušební náklady SAND TATO CMNT GRVL TOUR BEER FICR CHEM TOYS URAN WATR ACID JAVA CLAY SGCN KAOL BRCK BDMT FRUT STUD WINE HOPS MLTR (`zkusebni_naklady.grf`, `MAXn`), mírné klima je nemá; na zkoušku kupek, pytlů, sudů, sena, turistů a toho, co které auto nevozí |

## Zkušební příkazy

| příkaz | co udělá |
|---|---|
| `testv3s` | koupí každé kupovatelné silniční auto z GRF v `TEST_RV_GRF` (např. `MAXd`), vypíše pořadí v nákupu (`list_position`), přestaví ho na GOOD PASS MAIL STEL COAL IORE LVST WOOD GRAI VALU SAND MARI TATO CMNT GRVL TOUR BEER FICR CHEM TOYS URAN WATR ACID OIL_ JAVA CLAY SGCN KAOL BRCK BDMT FRUT STUD WINE HOPS MLTR (co ve hře je; náklad, který auto nevozí, hlásí „NE (nevozi)“), u nákladů s podtypy (LVST FICR BEER BRCK BDMT TATO) i podtypy 0 až 3 s jménem (callback 0x19) a vrstvami a vypíše díly, délky, kapacity a čísla spritů; každý náklad i naloží a vypíše vrstvy obrázku naložené (auto + kupka nebo plachta); vypíše i, co by psalo okno nákupu (kolik nákladů auto umí a co mu chybí); u aut se zvukovým callbackem vypíše, co GRF vrátí pro výjezd z depa, odjezd ze zastávky, jízdu v 0–60 km/h, stání a poruchu (čítač tiků na chvíli posune do taktu zvuku) |
| `testv3sfoto <tiků> [RTxx] [fotek] [tiků mezi fotkami]` | postaví silniční okruh s depem (ze silnice s daným štítkem, jinak CZTR RT14, když je načtená, jinak z běžné), dva původní náklaďáky hry a deset naložených V3S (`MAXd`, `MAXe`: od verze 8 cihly červené a šedé, ovoce, brambory na kupě a v pytlích, pivo Plzeň a Budvar, chmel; seznam `nakupy` v `ConTestV3SFoto`, i s podtypem), po zadaném počtu tiků vyfotí okruh při plném přiblížení, případně víckrát po sobě, a hru ukončí. U každé fotky vypíše počátek pohledu (`V3SPOHLED`) a polohu, směr a posun kreslení každého dílu (`V3SDIL`), takže se dá každé auto vystřihnout |
| `TEST_FOTO_SADA=tatra` + `testv3sfoto …` | místo vejtřasek koupí na okruh deset Tater z verze 10 (`MAXd`, `MAXe`, čísla `0x0102` až `0x0105`): sklápěč s uhlím, cisterny s vodou, ropou a kyselinou, valník s obilím, pivo v cisterně Plzeň, zelená s vojenskou technikou a uranem, plachta s ocelí, kravičky (seznam `nakupy_tatra`) |
| `testpruhy x\|y [tiků] [kolona]` | pořadí kreslení aut proti sobě (29. 9.): postaví tři rovné silnice podél osy X (SV–JZ) nebo Y (SZ–JV) a na každou osm dvojic stojících aut proti sobě, zadní a přední pruh, čela od sebe 0 až 14/16 dlaždice (celé míjení); s `kolona` místo dvojic zácpu v obou pruzích. Auta: TAZ 1500 bus zahrádka, TAZ 1203 plachta a VW T1 z GRF VW T1 (`auta/VWT1-S1203-clanky-oba-na-stred.grf` musí být v domově) a Tatry z verze 10. Vypíše krabice dílů (`PRUHY: … box x … y …`), vyfotí a skončí; vystřihnout dvojice umí `hra/poradi-kresleni/vystrih.py`. Jiná auta: `TEST_PRUHY_AUTA="MAXe:0102/MAXe:0103;4D415808:0093/4D415808:0092;…"` (po řadách zadní/přední pruh, GRF jako 4 znaky nebo 8 šestnáctkových číslic); s `mrizka` stejná dvojice (odstup `TEST_PRUHY_ODSTUP`, jinak 6) posunutá po dlaždici. CZTR Truck Set chce svoje silnice, na zkoušku mu stačí přesměrovat je na `RT14`, a starší auta chtějí `setting vehicle.never_expire_vehicles 1` |
| `testspoj` | kolegova scénka se spojováním vlaků; s `TEST_LOCO_GRF=MAXb` vezme lokomotivu z toho GRF (zkouška zvuků Sergeje) |

Výpisy V3S jdou i na stderr (`dbg: [misc:0] V3S…`), s obrazem by jinak zůstaly jen v okně konzole.
Zvuková zkouška Sergeje vypisuje řádky `ZVUK: vuz … udalost … callback … zvuk …`.

## Jak pustit

```bash
apt-get install -y libsdl2-2.0-0        # jednou v novém kontejneru; xvfb-run tam už je
mkdir -p /tmp/hra && tar -xJf hra/ottd-zkusebni-gfx.tar.xz -C /tmp/hra
H=/tmp/hra/ottd-zkusebni/domov
cp v3s/grf/mala/Praga_V3S_Tatra-v10.grf v3s/grf/velka/Praga_V3S_Tatra_BRYLE-v10.grf hra/zkusebni_mari/zkusebni_MARI.grf hra/zkusebni_naklady/zkusebni_naklady.grf $H/.openttd/newgrf/
sed -i 's/^\[newgrf\]$/[newgrf]\nzkusebni_MARI.grf = \nzkusebni_naklady.grf = \nPraga_V3S_Tatra-v10.grf = \nPraga_V3S_Tatra_BRYLE-v10.grf = /' $H/.openttd/openttd.cfg
printf 'setting starting_year 1990\nnewgame\n' > $H/.openttd/scripts/autoexec.scr
printf 'testv3sfoto 1500\n' > $H/.openttd/scripts/game_start.scr
cd /tmp/hra/ottd-zkusebni
HOME=$H xvfb-run -a -s "-screen 0 1024x768x24" ./openttd -v sdl -b 32bpp-anim -r 800x500 -s null -m null > $H/log 2>&1
# fotka: $H/.openttd/screenshot/v3s_okruh.png (3200 x 2000, přiblížení 4x)
```

Pozor při výměně GRF za novou verzi: hra si po prvním spuštění zapíše do `[newgrf]` řádky jako
`4D415864|<md5>|Praga_V3S-v7.grf = ` a pak načítá přesně ten soubor s tím md5. Starý řádek se musí přepsat
celý (na `Praga_V3S-v8.grf = `), jinak zkouška tiše běží se starou verzí (29. 9. se to stalo u verze 8).
Md5 v tom řádku počítá hra jen z dat GRF (akce), ne z obrázků: GRF se stejnými pravidly a jinými obrázky
má stejné md5 (u verze 10 nanečisto i naostro), proto soubor vždycky zkontrolovat `md5sum`.

Stromy, které auta na okruhu zakrývají, schová v `openttd.cfg` `transparency_options = 2`
a `invisibility_options = 2`.

Víc fotek po sobě: `testv3sfoto 300 RT14 12 100` (první za 300 tiků, pak 11 dalších po 100),
soubory `v3s_okruh_00.png` až `v3s_okruh_11.png`. Bod fotky, kam hra položí kotvu dílu:
`8·(y+ky − x−kx) − vlevo`, `4·(x+kx + y+ky − z) − nahoře` (px, `kx ky` = „kresli“ z `V3SDIL`).

Bez obrazu, jen výpisy (třeba `testv3s`), stačí `./openttd -vnull:ticks=200 -snull -mnull`
a v `game_start.scr` příkaz, na konci `quit` není potřeba.
`-G <číslo>` dá pokaždé stejnou mapu.

## Jak přeložit znova

```bash
cp -r /home/user/forclaude/openttd /tmp/openttd     # kopie, ve forclaude nic neměnit
cd /tmp && patch -p1 < /home/user/grrrrf/hra/zkusebni-prikazy.patch   # cesty v patchi jsou openttd/src/…
apt-get install -y libsdl2-dev
mkdir /tmp/b && cd /tmp/b && cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -DOPTION_DEDICATED=OFF /tmp/openttd && ninja openttd
```

Asi 20 minut na 4 jádrech. Když se zdroják mění během překladu, ninja si to nemusí všimnout
(soubor se přeloží ze starší verze a objekt je pak novější než zdroják): `touch` a přeložit znova.
