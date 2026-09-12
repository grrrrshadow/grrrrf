# Zarovnání spritů autíček

- `VWT1-zarovnano.yagl` — VWT1.yagl z release `glb2` s přepsanými offsety
  u **Škody 1203 (0x0082)**. VW T1 (0x0080) je beze změny, byl už doladěný.
- skripty: `final2.py` (změří počátek = střed rozvoru na vozovce ve všech
  8 směrech), `hotovo3.py` (přenese konvenci VW T1 na další auto),
  `kolatest.py` (kontrola — promítne obdélník rozvor × rozchod na kola),
  `obraz3.py` (obrázek teď/opraveno).

Postup a naměřená čísla jsou v `temata3.md`, oddíl „Zarovnání spritů autíček".

## Nové offsety Škody 1203

| dir | | xoffs teď | nový | yoffs teď | nový |
|---|---|---|---|---|---|
| N | zatáčení | −33 | −28 | −35 | −35 |
| NE | přímý směr | −44 | −61 | −29 | −17 |
| E | zatáčení | −47 | −58 | −25 | −27 |
| SE | přímý směr | −41 | −38 | −33 | −30 |
| S | zatáčení | −32 | −27 | −35 | −42 |
| SW | přímý směr | −44 | −35 | −33 | −31 |
| W | zatáčení | −47 | −29 | −27 | −30 |
| NW | přímý směr | −41 | −16 | −33 | −23 |

## Složení GRF — správná cesta: rozebrat hotové GRF a přepsat offsety v něm

```bash
cd stavba                      # obsahuje sprites/ se spritesheety
cp VWT1-zarovnano.yagl sprites/VWT1.yagl
sed -i '1s/.*/yagl_version: "";/' sprites/VWT1.yagl   # nase binarka hlasi prazdnou verzi
yagl -e VWT1.grf sprites
mv VWT1.grf VWT1-S1203modradodavka.grf                # jmeno jako mel puvodni soubor
```

### Na co jsem narazil

- **`speed_kmh: 101;` u VW T1 není vlastnost, kterou yagl zná.** Není
  ani v naší vendorované kopii, ani v upstreamu. Soubor se s ní nesloží
  vůbec. Silnice mají jen `speed_2_kmh` (property 0x08) a podle
  `newgrf_act0_roadvehs.cpp:47` je **1 jednotka = 0,5 km/h**. Takže
  101 km/h = `speed_2_kmh: 202`. To jsem tam dal; v GRF, který byl
  v release, bylo `0x8C` = 70 km/h.
- Varování „non-background pixels in its border" jsou jen varování,
  na složení nemají vliv.

### Kontrola hotového GRF

Rozebrat nový i původní GRF a porovnat. Proti `VWT1-S1203modradodavka.grf`
z release se liší **jen**: popis (novější text hráče), rozšířená
překladová tabulka nákladů (taky hráčova novější práce, včetně `MARI`),
`speed_2_kmh` a osm offsetů Škody. Grf_id zůstává `4D 41 58 08`.

## Jak se to nakonec udělalo

Hráč to řekl správně: **rozbalit hotové GRF a zarovnání přepsat do něj.**
Ne skládat z `.yagl` v release — ten je rozpracovaný (má navíc
překladovou tabulku nákladů, jiný popis a neplatné `speed_kmh`), takže
by se do GRF dostaly i věci, o které nikdo nežádal.

```bash
mkdir z && cp VWT1-S1203modradodavka.grf z/VWT1.grf && cd z
yagl -d VWT1.grf                 # vznikne sprites/VWT1.yagl + jeden velky spritesheet
python3 patch2.py                # prepise 8 offsetu Skody
rm VWT1.grf && yagl -e VWT1.grf sprites
mv VWT1.grf VWT1-S1203modradodavka.grf
```

**Kontrola:** nový soubor má stejnou velikost jako původní a liší se
přesně v **15 bajtech**, všechny uvnitř osmi offsetů Škody. Zpětné
rozebrání ukáže jen těch osm řádků. Nic jiného se nezměnilo — rychlost,
náklady, popis ani grf_id.


---

# Druhý pokus: společný základ pro všech 18 aut

První pokus zarovnal jen Škodu 1203 (0x0082) — jedno auto z osmnácti.
Hráč jel se **sadou**, takže logicky nic nepoznal. Skutečné zadání je:
*„musí mít všechny stejnou výchozí pozici"*, aby se pak dala celá sada
posunout jedním číslem (jeho `fix_sprites.py`).

## Stav před opravou

| | |
|---|---|
| 0x0080 VW T1 cztrsize | ručně doladěné |
| 0x0081 VW T1 origsize | ručně doladěné |
| 0x0082 – 0x0097 (16 aut) | `xoffs = −w/2`, `yoffs = −h/2`, čili nic |

## Změřené rozvory (rozestup kol v bočním pohledu)

| auto | rozvor v px |
|---|---|
| VW T1 cztrsize | 36,0 |
| VW T1 origsize | 44,2 |
| Škoda 1203 Pajda + všechny TAZ 1203 | 42,5 |
| TAZ 1500 | 43,0 |

Všechny TAZ 1203 mají mezi sebou **stejný podvozek na pixel přesně**
(pás kolem kol jim sedí s IoU 0,95–1,00). Škoda 1203 Pajda má stejný
rozvor 42,5 px, ale pás se jí liší (IoU 0,84–0,92) — kvůli otevřeným
dveřím a jiné karoserii. Je to jedno auto s různými nástavbami.

## Pravidlo

Kotva = pevný bod nad **středem rozvoru na vozovce**. Ten bod se změří
z obrázku (viz `temata3.md`), pro každý směr a každé auto. Posun kotvy
proti němu se převezme z VW T1 origsize, proložený tuhým 3D bodem, aby
auto v zatáčce nepodskočilo:

| dir | vodorovně | svisle |
|---|---|---|
| N | −1,3 | −21,5 |
| NE | +4,7 | −21,1 |
| E | +5,0 | −20,5 |
| SE | −0,6 | −20,1 |
| S | −8,8 | −20,1 |
| SW | −14,8 | −20,4 |
| W | −15,0 | −21,0 |
| NW | −9,4 | −21,4 |

Hodnoty jsou z proložení `C + X·sin α + Y·cos α` (vodorovně) a
`C + X·cos α + Y·sin α` (svisle). Naměřené hodnoty VW T1 origsize se od
nich liší až o 11 px vodorovně a 8 px svisle — to je to podskočení,
které hráč nechtěl. Proložení ho odstraní.

Konkrétní čísla pro všech 18 aut jsou v `offsety-vse.md`.

## Skripty

`vse.py` (změří počátek u všech aut), `vse2.py` (spočte nové offsety),
`patch3.py` (přepíše je v rozbaleném GRF), `overka.py` (obrázek na kontrolu:
všechna auta vedle sebe s kotvou na společném křížku).


---

# Třetí pokus: ono je sad po osmi spritech 58, ne 18

**Tohle je ta chyba, kvůli které hráč neviděl žádnou změnu.**

Každé vozidlo nemá jednu sadu 8 spritů, ale **dvě až čtyři** — podle
stavu naložení. Action02 to rozděluje:

```
sprite_groups<RoadVehicles, 0xFF>   // Action02 basic
{
    primary_spritesets:   [ 0x0000 0x0001 ];   // prazdne
    secondary_spritesets: [ 0x0003 0x0002 ];   // nalozene
}
```

Celkem je v GRF **58 sad po 8 spritech** na 18 vozidel. Můj parser bral
„poslední sadu o osmi spritech před jménem vozidla", takže jsem
přepisoval **jednu sadu z každého vozidla — a byla to ta naložená**.
Hráč zkoušel nenaložená auta, čili sady `0x0000`, kterých jsem se
vůbec nedotkl.

**Ponaučení:** než něco přepíšu, spočítat, kolik těch věcí vlastně je,
a ověřit, že sedí počet. 58 ≠ 18 by mě zastavilo hned.

## Kontrola, že to teď sedí

Vzdálenost linky kol od kotvy v bočním pohledu (= jak daleko je auto
od krajnice), základní nenaložená sada:

| | rozptyl mezi auty |
|---|---|
| před | 19–27 px, čili **8 px** rozdíl |
| po | 26–27 px, čili **1 px** |

A ve všech osmi směrech:

| dir | před | po |
|---|---|---|
| N | 2 px | 3 px |
| NE | 11 px | 3 px |
| E | 8 px | 1 px |
| SE | 8 px | 3 px |
| S | 13 px | 2 px |
| SW | 10 px | 2 px |
| W | 6 px | 2 px |
| NW | 8 px | 2 px |

Zbylé 1–3 px jsou rozdílné rozchody kol (VW T1 cztrsize je menší, jeho
kola jsou blíž k ose) a zaokrouhlení na celý pixel.

Druhá kontrola: sady téhož vozidla mají podvozek shodný, takže po
zarovnání musí sednout na sebe. Zbytkový posun mezi sadami vyšel
**(0, 0) u všech 18 vozidel** (`kontrola58.py`).

## Skripty

`sady.py` (najde všech 58 sad), `mereni58.py` (změří je), `nove58.py`
(spočte nové offsety), `patch58.py` (přepíše), `kontrola58.py` a
`krajnice.py` (kontroly), `overka58.py` (obrázek).
