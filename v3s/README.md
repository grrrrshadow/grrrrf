# V3S Vejtřaska: Praga V3S jako vlastní GRF

Hráč 28. 9.: *„udělej mi vejtřasku, zas uděláme velkou malou“*, *„vojenskou a modrou“*,
*„vojenská tam je, jen ji přebarvi na modro“*, *„komunistickou modrou“*.

| GRF | `grf_id` | měřítko | délka auta | kolona |
|---|---|---|---|---|
| `grf/mala/Praga_V3S-v1.grf` | `MAXd` | jako CZTR, 12,2 px/m (zin4) | 7,7 osminy, díl 8/8 | rozestup 8, jako CZTR |
| `grf/velka/Praga_V3S_BRYLE-v1.grf` | `MAXe` | BRÝLE, o 20 % větší, 14,64 px/m | 9,25 osminy, díl 8/8 | čumák 2/8, rozestup 10 |

Balík pro hráče je `Praga_V3S_Vejtraska-v1.zip`: oba GRF a `licence.txt` (licence, převzatý model,
reklama na ottd Decouple s odkazem na itch a „No donations allowed“).

## Jméno a popis v seznamu GRF

Stejný řád jako Sergej: `{red}Praga V3S Vejtřaska{green} for ottd Decouple by Karel Macha` a na
konci symbol náklaďáku (`{truck}`) v barvě varianty, měřítko CZTR `{gold}`, BRÝLE `{lt-blue}`.
Popis: červené jméno, zelený řádek se symboly, řádek varianty v její barvě, `{orange}` informace
a model, nakonec zeleně ottd decouple, itch a licence.

## Auta

| | kupované číslo | viditelné auto (jen velká) | nátěr |
|---|---|---|---|
| Praga V3S Vejtřaska (vojenská) | 0x0100 | 0x0110 | model beze změny, olivová |
| Praga V3S Vejtřaska (modrá) | 0x0101 | 0x0111 | komunistická modrá, 4 odstíny podle nákladu |

- Uvedení **20. 2. 1952**, první funkční prototyp V3S (Praha-Vysočany). Hra dá v ten den prototyp
  jedné firmě na zkoušku, všem o rok později, jako sériová výroba od dubna 1953. Hra k datu přičte
  náhodně až 511 dní, když hra nezačala dřív než dva roky předtím.
- 60 km/h, 100 k (Tatra 912), 5,5 t, kapacita 10 jednotek. Lidé: vojenská 20 (vojáci na korbě,
  hráč: „hodně“), modrá 3 (kabina). Lidi dělá callback 0x15, jen pro PASS.
- Zvuk odjezdu náklaďáku (0x17), cena a provoz mezi Avií A31 a Tatrou 815 z CZTR.
- Na trhu do konce hry (`model_life_years 255`).

### Velká: neviditelný čumák

Stejně jako `CZTR_Truck_SetBRYLE1-clanek.grf` a dvanácettrojky (`auta/CUMAK.md`): kupované číslo
je neviditelný čumák délky 2, drží jméno, cenu a obrázek v nákupu, viditelné auto je druhý článek
délky 8. Rozestup v koloně je 8 + 2 = 10 osmin, auto má 9,25, mezera 0,75 osminy.
Čumák veze 1 jednotku (motor s nulovou kapacitou by přišel o nabídku nákladů), auto zbytek,
u lidí 1 + 2 a 1 + 19. Oba díly mají stejný seznam nákladů. Rychlost, výkon a hmotnost čte hra
jen z čumáku (`RoadVehUpdateCache`, `GetWeight`).

**Článková auta berou jen průjezdné zastávky** (hra: `STR_ERROR_NO_STOP_ARTICULATED_VEHICLE`).
Malá čumák nemá, do zálivu zajede.

## Náklady

Hráč: *„VW T1 vozí všechno, tam se inspiruj“*, *„skoro všechno“*. Seznamem, bez tříd, jak to
hráč dělá (`temata3.md`, „Jak hráč dělá GRF“).

- **Základ:** seznam VW T1 (0x0082, 71 kódů s MARI), bez GLAS (*„stavební materiály všechny
  kódy kromě skla“*) a bez FOOD.
- **Přidáno:** šrot a ocel (SCMT STEL STAL STST STSE STSH METL a z FIRS Steeltown STIG STSL STBR
  STPL STSW), železný řetězec Steeltownu (IORE COAL COKE LIME QLME IRON SLAG FEAL CSTI VBOD PLNT),
  řepa SGBT, konopná vlákna FICR, stavební GRVL SAND.
- **Jen vojenská:** FOOD (*„jídlo jenom vojenský“*) a BOOM (*„vojenská explosives, modrá ne“*).
- Modrá 96 kódů, vojenská 98. Pivo, tabák, marihuana a cigára (BEER TBCO MARI CIGR) vozí obě.
- Jména kódů z `naklady.md` a z FIRS 5.2 (`rozbalene/firs-5.2.0`), nic domyšleného. Neznámé
  labely z VW T1 (FARM LVPT HOPS ELEC NODC) zůstaly, jak je hráč má.
- Překladová tabulka: jen použité kódy v pořadí z `prekladova-tabulka-vzor.yagl`, co ve vzoru
  není, jde za MARI (98 položek).
- FIRS Steeltown má u všech 62 nákladů násobek kapacity 1 (vlastnost 1D), takže V3S vezme
  10 jednotek čehokoli. Ve hře bez FIRS má zboží násobek 2, tam vezme 10 zboží, ale 5 uhlí.

### Odstíny modré

Hráč: *„máme hodně nákladů, tak všechny modrý použijem, míchej to“*: C světloučká stavby,
D tmavá strojírenství, A zboží, B zemědělství. Grafika se volí v Action 3 podle nákladu.

| odstín | lak v texture | náklady |
|---|---|---|
| A | 30, 60, 130 | zboží a všechno, co není v B, C, D (i lidi a pošta, obrázek v nákupu) |
| B | 40, 62, 100 | TATO BEAN SGBT TBCO MARI FICR FMSP SEED OLSD LVST WOOL FRUT JAVA NUTS |
| C | 60, 90, 130 | CMNT BDMT BRCK CCPR CERA GRVL SAND LIME QLME RBAR STSW |
| D | 25, 45, 95 | ocel, šrot, ruda, uhlí, koks, železo, struska, motory, díly, stroje (40 kódů) |

## Kotva spritů

Konvence VW T1 orig size (`temata3.md`, hráč: *„podle linky mezi koly“*), **zrcadlově srovnaná**
(hráč: *„a zrcadlová verifikace středu“*). Kotva (bod −xoffs, −yoffs) je proti bodu na zemi pod
středem auta vodorovně `10,0 · sin a`, svisle `−20,8 − 0,7 · cos a`, a = 45° · směr. Z proložení
VW T1 zmizely části, které zrcadlové nejsou (konstanta −5 px a `3,8 · cos a`): sever a jih mají
kotvu na ose, SV–SZ, V–Z a JV–JZ jsou zrcadla. Pro S, J, V a Z je to přesně oprava, kterou už
dostaly dvanácettrojky (sever −1, jih −9, východ a západ −5). V jízdních směrech je V3S o 2 px
(SV, SZ) a o 8 px (JV, JZ) jinde než VW T1, protože ten v nich zrcadlový není (otevřené
v `auta/CUMAK.md`).

Střed auta je v půlce délky, ne v půlce rozvoru. V3S má za zadní nápravou dlouhou korbu, střed
rozvoru je o metr blíž k čelu, auto by pak v zastávce i na vagonu stálo o metr dozadu.

Kontroly na rozbaleném GRF (`yagl -d`):
- `kontrola_zrcadla.py`: zrcadlo spritu 8 − k položené podle offsetů na sprite k. Obě velikosti,
  všech 5 sad: sever a jih kotva na ose, dvojice odchylka **0 px**, shoda siluet 0,95 až 1,00.
- `kontrola_vw.py`: vedle VW T1 orig size na společném křížku. V bočním pohledu (vzdálenost od
  krajnice) má V3S linku kol 27 až 28 px pod kotvou, VW T1 27 a 28 px.

## Jak to vzniklo

1. **Model**: `praga-v3s.glb` z releasu `par6` (`zip6/bar/`), zkopírovat do `model/`. Autor
   **hans1240**, „Praga-V3S“, CC BY 4.0,
   https://sketchfab.com/3d-models/praga-v3s-5593b3ca44cb41adb5a1c6ecb81297d3
2. **Nátěr** (`nater_v3s.py`): olivový lak (odstín 36–80°) na modrou se zachováním jasu, tedy stínů,
   špíny a prken. Rez, pneumatiky, sklo, světla a cedulka PRAGA V3S zůstávají.
3. **Focení** (`render_v3s.py`): kamera, HDRI a Cycles jako Sergej, 8 směrů ve stejném měřítku
   (silniční vozidla se na rovné silnici nestlačují), kabina natočená po směru jízdy (kontroluje se).
   `python3 render_v3s.py <vojenska|modra_A..D> <px_na_m> <výstup>`
4. **Balení** (`pack_v3s.py`): `python3 pack_v3s.py <mala|velka> <adresář fotek> grf/<mala|velka>`,
   pak v `grf/<varianta>` `yagl -e Praga_V3S-v1.grf` (nebo `Praga_V3S_BRYLE-v1.grf`).
5. **Zkouška ve hře** (`hra/`, moje kopie hry, ne forclaude): příkaz `testv3s` koupí každé auto
   z GRF, přestaví ho na náklady a vypíše články, délky, kapacity a sprity. Ověřeno: načte se bez
   chyby, velká čumák 2 + auto 8, malá 8, lidi 3 a 20, zboží 10, modrá má jiný sprite pro ocel,
   uhlí a rudu (D), dobytek (B) a zboží a poštu (A). Příkaz `testv3sfoto` nechá V3S jezdit po okruhu
   s původními náklaďáky hry a vyfotí to: V3S jedou ve stejném pruhu jako původní náklaďáky
   (`kontrola/hra_kolona.png`, `kontrola/hra_detail.png`). Malá těsně za velkou se překryje asi
   o půl osminy (velká je delší, čumák chrání jen její čelo), stane se jen při míchání velikostí.

Na silnici CZTR RT14 „1. třída – venkov“ (hráč: *„fotit s CZTR silnicí“*) jede V3S ve svém
pruhu mezi středovou přerušovanou čárou a krajnicí a nepřejíždí ani jednu (`kontrola/hra_cztr_silnice.png`).

Obrázky v `kontrola/`: `porovnani_vw.png` (srovnání s VW T1 na společném křížku), `vyber_modre.png`
(odstíny A až D, jak si je hráč vybral), `hra_*.png` (fotky ze zkušební hry).

Verze (`VERZE` v `pack_v3s.py`, je ve jménu souboru i v Action14): 1 první vydání.
