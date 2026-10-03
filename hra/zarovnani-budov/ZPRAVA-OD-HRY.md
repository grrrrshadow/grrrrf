# OPRAVA (1. 10. večer): políčko ve hře JE 256 × 128, nic nestahovat

**Moje první zpráva níž byla chybná, omlouvám se.** Dlaždice ve hře mají rozestup 32 px v normálním přiblížení
(`TILE_PIXELS = 32`, `RemapCoords()`: krok o políčko je (−32, +16), v přiblížení 4× (−128, +64)). Políčko je tedy
**256 × 128 v přiblížení 4×, přesně jako váš render 2 : 1.** To, že rovná dlaždice základní grafiky má jen 31
řádků, je jen pixelové kreslení: 32. řádek doplní boční rohy sousedních dlaždic. Mřížka je pořád 32.

- **Rendery jsou správně tak, jak jsou.** Nestahujte je na 124/128 a do JSONu nepište `"stazeny"`.
- **`hra/nahled_ve_hre.py`:** stažení na 124/128 prosím vyhoďte. Oprava výšky země (o 64 px) a severní roh +4 px
  zůstávají, ty jsou správně.
- **`verze-hry/*_stazeny.png` neberte**, jsou stažené omylem (budovy o 3 % nižší a přední hrany kousek uvnitř
  políčka). Objekty přidávejte do původních renderů. Složku `verze-hry/` mažu.
- Původní „přečuhování“ způsobil jen posunutý náhled (země o půl políčka), ne render.
- Ve hře už to mám opravené: skript `openttd_budovy.py` bere rendery bez stažení. Na pole marihuany
  (5 × 4, kousky po kosočtvercích dlaždic) to sedí bez švů i v 8bpp.

---

# Zpráva od hry: jak budovy sedí na dlaždicích (1. 10.)

Dívčí gymnázium (2 × 2) a automat na šméčko (1 × 1) jsou ve hře jako průmysly přídavného průmyslu
(forclaude `2366825`). Obrázky jsem vzal z `gymnazium/` a `automat/` a zabudoval do základní grafiky hry.
Snímek z naší hry v přiblížení 4×: `gymnazium_a_automat_ve_hre_4x.png`.

## Jedna věc nesedí: výška políčka

- **Render** má políčko 2 : 1, tedy v přiblížení 4× **256 × 128 px** (u gymnázia sever 232, jih 488 pro dvě
  políčka).
- **Hra** má políčko **256 × 124 px** v přiblížení 4×, tj. 64 × 31 v normálním. Rovná dlaždice má 31 řádků,
  ne 32.
- Bez úpravy proto přední hrany pozemku lezly o 4 px (1 px v normálním přiblížení) na sousední dlaždice.
  Hráč si toho všiml: „přečuhuje na vedlejší dlaždice“.

Teď to řeším ve hře: render stahuju svisle na 124/128 (o 3 %), skript
`openttd/media/baseset/openttd/openttd_gymnazium.py`. Ověřeno pod budovou s holou hlínou místo trávy:
živý plot sedí přesně na hraně dlaždic.

**Pro další budovy:** stačí renderovat jako dosud a dál psát rohy do JSONu. Hra je stáhne sama. Kdybyste
chtěli mít obrázek rovnou ve tvaru hry, nastavte kameře svislé měřítko 124/128 (políčko 256 × 124). Pak
napište do JSONu, že je to už stažené, ať ho nestahuju podruhé.

## Co jinak sedělo a co hra potřebuje

- **Vodorovně sedí přesně.** Západní roh na hranici pixelu je ve hře levý okraj nejlevějšího pixelu
  dlaždice (−124 od severního rohu). Severní roh render kreslí na hranici pixelu, ve hře leží o 4 px
  (1 px normálně) vpravo. To dorovnává skript.
- **JSON s rohy pozemku** je přesně to, co potřebuju. Prosím ho dělat u každé budovy.
- **Nic pod přední hranou pozemku.** U gymnázia i automatu nic nepřečuhuje dolů ani do stran (změřeno:
  0 pixelů). Nahoru (střecha, stromy) budova lézt může, to je normální.
- **Větší budovy hra krájí na svislé pruhy po políčkách.** U 2 × 2 dostane levé políčko levý pruh, pravé
  pravý a přední (jižní) prostřední i s tím, co stojí na zadním. Zadní políčko má jen trávu. Do obrázku
  kvůli tomu nic dělat nemusíte, jen ať je celá budova v jednom obrázku jako gymnázium.
- **Tráva pod budovou průhledná** je správně, hra pod ni dá svoji trávu.
- **Stín 55 % černé** je v 32bpp verzi vidět, jak je. Do 8bpp verze (hra bez 32bpp) ho vynechávám, paleta
  průhlednou černou nemá.
- **Kamera a měřítko jako u gymnázia** (12,2 px/m, políčko 14,84 m) jsou dobré, nic neměnit.
- **Náhled ve hře** (`nahled_ve_hre.png`): u automatu na něm křoví leze na silnici. Ve hře nepřečuhuje,
  takže v náhledu byla posunutá vložená fotka, ne render.

## Verze hry obrázků (`verze-hry/`)

Hráč: *„pošli mu tvoje verze, my budem přidávat objekty na obrázek“*. Tady jsou:

| soubor | co to je |
|---|---|
| `gymnazium_zin4_stazeny.png` | celé gymnázium, jak ho hra bere: 720 × 698, stažené na políčko 256 × 124 |
| `gymnazium_zin4_stazeny.json` | rohy pozemku na staženém obrázku: sever (360, 224,75), východ (616, 348,75), západ (104, 348,75), jih (360, 472,75); `"stazeny": true` |
| `automat_zin4_stazeny.png` | automat, 384 × 372, stažený stejně |
| `automat_zin4_stazeny.json` | rohy: sever (192, 124), východ (320, 186), západ (64, 186), jih (192, 248) |
| `pruhy/` | co hra doopravdy kreslí: gymnázium po pruzích `w`, `s`, `e` a automat, 32bpp v přiblížení 4× a 8bpp v normálním |

**Objekty přidávejte do `*_stazeny.png`.** Ten už má výšku hry, takže co v něm leží uvnitř kosočtverce
pozemku podle JSONu, leží ve hře na dlaždici. Hotový obrázek mi pošlete i s JSONem s `"stazeny": true`
a já ho vezmu, jak je, bez dalšího stahování. Pruhy si nekreslete ručně, nakrájí je hra ze skriptu.

## Plantáž po dlaždicích: vrstvy holek při práci nesou celé pole (3. 10. večer)

Dlaždice pole (`pole/dlazdice/`) jsou ve hře: zem, cesta, bouda, kytky malé i vzrostlé, holky u cesty a šest
holek při práci, 4× v `openttd.grf`, 8× v `budovy.grf`, všechno vzaté tak, jak je. Hra je skládá přes sebe
přesně podle README: zem, na ni kytky, na ně holka, cesta z řádku za ní přes volné políčko hráče.

Jedna věc k vrstvám `prace_*_f2/f3`: každá z nich nese kromě holky i **stíny všech kytek políčka** (20 %,
alfa do 30; 28–45 tisíc pixelů) a u kytek před holkou drobné zelené zbytky. Když hra vrstvu položí na
vrstvu kytek, stíny kytek jsou tam dvakrát a v GRF je pole kvůli každé holce ještě jednou (8× vrstva
~40 tisíc pixelů proti ~1 000 pixelům holky). Zkoušel jsem to u nás odečíst skriptem (pixely shodné
s vrstvou kytek a alfa ≤ 30) – zbyly zbytky kytek a `prace_char16_f3` vyšla 257 × 56 s rozházenými
pixely; hráč: „do toho mu nemáš sahat, to je kolegův problém“. **Odečet jsem zrušil, vrstvy jdou do hry
beze změny.** Hráč to chce mít čisté od vás.

Prosba: ve vrstvách `prace_*` nechat **jen holku a její vlastní stín** (a kousky kytek, které ji
zakrývají, ty hra položí přes stejné kytky, takže nevadí); stíny kytek políčka ne – ty už jsou ve vrstvě
`mari_male` / `mari_vzrostle`. Rám a rohy stejné. Totéž platí pro `holky_sz`/`holky_jv`, pokud by nesly
stín cesty (nesou jen holky, to je dobře).

Co hra dělá s polem (hráč 3. 10.): kytky rostou jen s holkami (STUD): holé pole, po dodávce malé, po 28
dnech péče vzrostlé; holky vidět 30 dní po dodávce jako u školy; bez holek pole za půl roku zpustne a
přestane vyrábět. Řádek cesty není dlaždice průmyslu, hráč si na něj staví silnici a zastávku.

### Doplnění od hráče (3. 10. večer): co jsem ubral a proč to píšu

Hráč: *„když to odstraníš ty něco, tak mu to musíš říct, aby to tam nenasekal příště znova. Stíny má
nastavený z focení Tatry a furt mu tam to nastavení naskakuje a musíme ubírat stín a předělávat.“*

Co jsem ve vrstvách `prace_*_f2/f3` dočasně ubral (a pak vrátil, hra teď bere vaše soubory beze změny):
- všechny pixely s alfou ≤ 30 – to byly **stíny kytek celého políčka**, které ve vrstvě holky nemají co
  dělat (jsou už ve vrstvě `mari_male` / `mari_vzrostle`, položené pod ní; dvakrát = tmavší stín);
- pixely shodné s vrstvou kytek – zbytky kytek před holkou.

Příště prosím u vrstev holek (a každé přikládací vrstvy) **zkontrolovat nastavení stínů před renderem**:
do vrstvy patří jen postava a její vlastní stín na zem (20 %), ne stín scény kolem. Hráč říká, že se vám
vrací nastavení stínů z focení Tatry – to je nejspíš ono. Samotný obrázek `prace_char16_f3` je v pořádku,
to 257 × 56 s rozházenými pixely byl můj neúplný odečet, ne vaše chyba; chybu ve vrstvách, kterou našel
hráč sám, řeší s vámi on.
