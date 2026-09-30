# Pro kolegu od GRF: víc čísel bloků grafiky (Action 2) je ve hře

Od session hry (`grrrrshadow/forclaude`, větev `claude/github-connection-check-m6m898`,
commit 682797f), 30. 9. Posílám na hráčovo slovo: jedno auto se 128 náklady a spoustou
liver a přestaveb vyčerpá 255 čísel bloků, a yagl je náš, takže formát si určujeme sami.

## Co hra teď umí

GRF, který se hry zeptá na vlastnost **`decouple_more_action2_ids`** (verze 1), se od té
chvíle čte s **dvoubajtovými čísly bloků**:

| kde | dřív | teď, po dotazu |
|---|---|---|
| číslo bloku v každé Action 2 (`02 <feature> <set-id> ...`) | 1 bajt | 2 bajty, little endian |
| číslo podprogramu u proměnné 0x7E (`7E <param>`) | 1 bajt | 2 bajty, little endian |
| odkazy na bloky (rozsahy, výchozí výsledek, náhodné bloky, Action 3) | 2 bajty | beze změny, 2 bajty |

Čísla jdou **od 0 do 0x7FFD** (32 765). 0x7FFE je „vypočtený výsledek“, 0x7FFF „callback
selhal“ a nastavený horní bit znamená výsledek callbacku, stejně jako dřív.

GRF, který se nezeptá, se čte po staru, cizí GRF se tedy nic nemění. Jiná hra jméno nezná
a dvoubajtová čísla přečte špatně, takže takový GRF je zamčený i sám od sebe. Čistou
hlášku ale dá jen zámek `decouple_128_cargo` z minulé zprávy
(`hra/zamek-128-nakladu/ZPRAVA-OD-HRY.md`), proto doporučuju obojí.

## Jak to má vypadat v GRF

```
Action 14:  C "FTST"  T "NAME" "decouple_more_action2_ids"  B "MINV" 2 bajty = 1  B "SETP" 1 bajt = 9
            C "FTST"  T "NAME" "decouple_128_cargo"         B "MINV" 2 bajty = 1  B "SETP" 1 bajt = 8
Action 8:   hlavička GRF
Action 7:   0x9D, podmínka 0x00, bit 8, přeskoč 1
Action B:   závažnost 3, "Tento GRF patří ke hře OpenTTD decouple by Karel Mácha a jinde nefunguje."
Action 2:   02 01 E8 03 81 7E 58 02 00 FF 01 2C 01 05 05 07 00
            (blok 1000; zavolá podprogram 600; při výsledku 5 jde do bloku 300, jinak do bloku 7)
Action 3:   03 01 01 00 00 E8 03
```

**Oprava k minulé zprávě: Action 14 musí být před Action 8.** Hra čte Action 14 jen při
prohlížení souboru a to prohlížení končí na Action 8. Dotaz za hlavičkou hra nikdy neuvidí,
GRF pak neprojde vlastním zámkem a vypne se. Takhle to dělá i NML, Action 14 dává na začátek.
V minulé zprávě jsem psal jen „úplně na začátku“, to nestačilo.

## Co musí umět yagl

1. **Zápis:** když GRF v Action 14 žádá `decouple_more_action2_ids`, psát číslo bloku v
   každé Action 2 a parametr proměnné 0x7E na dvou bajtech. Odkazy zůstávají, jak jsou.
2. **Čtení (rozebrání GRF):** poznat ten dotaz v Action 14 na začátku souboru a číst potom
   Action 2 stejně. Bez toho yagl takový GRF rozebere špatně.
3. **Přidělování čísel:** strop 0x7FFD místo 0xFF.
4. **Pořadí:** Action 14 před Action 8.

## Ověřeno ve hře (rig)

Zkušební GRF `tests/rig/grf/bloky_siroke.nfo` ve forclaude, dá se použít jako vzor: bloky 7,
300, 600 a 1000, blok 1000 volá 600 jako podprogram a jde do 300, callback auta vrátí 0x123.
Druhý GRF `bloky_zamek.nfo` se ptá na jméno, které nikdo nezná, a vypne se na hlášce zámku,
tak jako by to udělala jiná hra.

Při psaní zkušebního GRF jsem narazil na past NFO, tak ji píšu i tobě: **blok bez rozsahů
(`nranges = 0`) nevrací svůj výchozí výsledek, ale vypočtenou hodnotu.** Moje první verze
proto vracela 0.

## Cestou opravená chyba ve hře

Odpovědi GRF na dotazy (Action 14) se po **načtení savu** ztrácely, hra si je pamatovala jen
v nové hře. GRF se zámkem by se po načtení savu sám vypnul a GRF s dvoubajtovými čísly by se
přečetl špatně. Týkalo se to i JGR vlastností, třeba návěstidel. Opraveno a scéna v rigu
hru uloží, načte a ptá se znovu.

## Co ve hře ještě není

Načítání našeho GRF z adresáře `baseset/`, jak jsme se domluvili minule. Na to potřebuju
jméno souboru a GRF ID.
