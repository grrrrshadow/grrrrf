# CZTR silnice 1. třída – venkov, výstřižek pro zkušební hru

Hráč 28. 9.: *„vystřihni sprity CZTR silnice 1. třída venkov, to bys hned viděl; připrav si CZTR
silnici, jen 1. třída venkov bohatě stačí; fotit s CZTR silnicí příště“*.

- Zdroj: **CZTR Road set 2.3.1**, CZTR team, licence **CC BY-SA 3.0** (`license.txt`, stejný text
  jako v sadě). Z releasu `par3`, `zip3/4d490101-CZTR_Road_set-2.3.1.tar`, GRF md5
  `bcd4672071ba86d86ee41a4296ca5e1e`.
- Vzatá je jen silnice **RT14 „[ - ] 1. třída - venkov“**: povrch (typ 0x02, 19 spritů z Record #196,
  sada 0), vlastnosti jako v sadě (od 1970, rychlost 0x00C8, příznaky 0x04). Zastávky, depo, most
  a kurzory zůstávají výchozí.
- Aby po ní smělo běžné auto (typ ROAD), přidá se RT14 do seznamu „powered“ u ROAD. Celá sada to
  dělá taky, hra bity k existujícím přičítá (`newgrf_act0_roadtypes.cpp`).
- `grf_id` `MAXr`. Jen pro moje zkoušky, hráčovi se nedává (hráč má celou sadu).
- Na švech dlaždic prosvítá napříč silnicí tráva (tečky). Je to tak i s celou sadou (vyzkoušeno ve
  zkušební hře, obě fotky stejné): sprity nesahají úplně k okraji dlaždice. S auty to nesouvisí.

Postup: celou sadu rozbalit `yagl -d` (s obrázky), pak
`python3 vystrih_rt14.py <rozbalená sada sprites/> .` a `yagl -e CZTR_silnice_RT14.grf`.
