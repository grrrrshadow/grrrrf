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
