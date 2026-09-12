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
