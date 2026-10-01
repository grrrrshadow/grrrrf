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
