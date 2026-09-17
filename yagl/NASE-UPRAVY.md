# Naše úpravy yaglu

Vendorovaná kopie `yagl-main/` už není čistá — rozvíjíme si ji pro sebe.
Tenhle soubor drží seznam, co jsme v ní změnili a proč, ať se to při
případné aktualizaci z upstreamu neztratí.

---

## 1. Průhledné pozadí spritesheetu (2026-09-11)

**Soubory:** `records/graphics/RealSpriteRecord.h`,
`records/graphics/RealSpriteRecord.cpp`

### Co vadilo

Yagl kontroluje pixely v pásu **kolem** každého spritu a čeká tam
čistou bílou. Náš spritesheet leze z Blenderu s **průhledným** pozadím
(alfa 0, RGB černá) a yagl na každý sprite hlásil:

```
WARNING: Sprite #00000005 has 374 non-white pixels in its border.
```

Obejít se to dalo — podložit bílou a průhledno uvnitř přebarvit na
modrou — ale to je znásilňování výstupu kvůli nástroji. Render má být
průhledný, protože průhledný ve hře být musí.

### Proč to tam bylo

Bílá jako „tady nic není" je konvence z **paletových** (8bpp) listů,
kde se průhlednost dělá indexem a volná plocha se musí nějak označit.
U **32bpp s alfa kanálem** se ale průhlednost drží v alfě a RGB pod ní
je, co tam renderer nechal — typicky černá. Takový pixel je pozadí
úplně stejně jako bílý.

### Co jsme udělali

Přibyl predikát `is_background()`: pixel je pozadí, když je plně
průhledný (alfa 0 u RGBA), **nebo** je čistě bílý. Kontrola okraje
teď používá jeho, ne `is_pure_white()`.

`is_pure_white()` zůstal beze změny a dál hlídá vnitřek spritu —
tam bílá pořád znamená „chybně zarovnaný obdélník". Že požaduje
`alpha == 0xFF`, je správně: průhledný pixel uvnitř spritu je
legitimní a za bílou se počítat nemá.

Hlášení upřesněno na `non-background pixels ... (neither pure white
nor fully transparent)`, aby bylo poznat, že už nejde jen o bílou.

### Ověřeno

- Vlastní testy yaglu: 2 685 471 assertions, 75 test cases, all passed.
- `shuttle.grf` složený z průhledného listu: **bez jediného varování**.
- Zpětné dekódování: u všech 8 spritů sedí počet průhledných pixelů
  na kus přesně proti zdrojovému renderu a největší odchylka barvy
  viditelných pixelů je **0**.

---

## 2. Chunkované sprity širší než 256 px (2026-09-17)

**Soubor:** `records/graphics/ChunkEncoder.cpp`

### Co vadilo

CZTR truck set, jehož grafika se zvětšila o 20 %, se nedal rozbalit —
yagl na něm spadl na segmentation fault. A nešlo o náš yagl: zabalila
ho starší verze pro Windows a ta ho pak sama taky nerozbalila. Chyba
je tedy v upstreamu a je v něm nejspíš dlouho, jen ji nikdo netrefil.

### Kde je zakopaný pes

Průhledný („chunkovaný") sprit se ukládá po řádcích. Každý řádek je
seznam úseků viditelných pixelů a každý úsek má hlavičku: délku a
odsazení od začátku řádku. Před řádky stojí tabulka, kde který řádek
v datech začíná.

A teď to podstatné: ve formátu jsou **dvě nezávislá rozhodnutí**,
jestli se něco píše krátce nebo dlouze, a každé se řídí něčím jiným.

| co | krátce | dlouze | podle čeho |
|---|---|---|---|
| položka tabulky řádků | 2 bajty | 4 bajty | celková délka dat > 65536 |
| hlavička úseku | 2 bajty | 4 bajty | **šířka spritu > 256** |

Dokud je sprit užší než 257 pixelů, obě odpovědi zní „krátce" a splést
si je nejde. Popelářský vůz po zvětšení měří **260 × 216** a je první
sprit v sadě, u kterého se odpovědi rozešly. Tam obě chyby vylezly.

### Dvě chyby, obě o téhle záměně

**Balič** psal úplně průhledný řádek jako `80 00 00 00`. Příznak
„poslední úsek" je ale u dlouhé hlavičky `0x8000`, ne `0x80`, a slovo
se čte od nižšího bajtu. Zpátky se to tedy přečte jako délka `0x0080`,
tedy 128 pixelů, a příznak konce řádku je pryč. Správně je
`00 80 00 00`. Konstanta `m_last_chunk` přitom byla hned vedle a
správnou hodnotu držela — jen se nepoužila.

**Rozbalovač** poznával prázdný řádek podle jeho délky, jenže velikost
hlavičky si bral z `long_offset`, což je to druhé rozhodnutí, to o
tabulce řádků. U našeho spritu vyšlo `long_offset = 0`, takže čekal
prázdný řádek dlouhý 2 bajty, ale ten měl 4. Řádek tedy nepřeskočil,
pustil se do rozbité hlavičky, uvěřil délce 128 pixelů, žádný konec
nenašel a odešel za konec bufferu. Odtud ten pád.

Sčítá se to: balič vyrobí rozbitou značku a rozbalovač na ni narazí,
protože ji nepřeskočí. Kdyby uměl jen jedno z toho, soubor by prošel.

### Co jsme udělali

- Balič bere příznak z `m_last_chunk`, takže u dlouhé hlavičky napíše
  `00 80 00 00` a u krátké `80 00`.
- Rozbalovač počítá velikost prázdného řádku z `LAST_CHUNK` (řídí se
  šířkou spritu), ne z `long_offset` (řídí se délkou dat).
- Před kopírováním pixelů přibyla kontrola mezí. Když data přece jen
  nesedí, yagl to teď řekne a vypíše čísla, místo aby spadl.
- Čítač kopírovaného úseku je `uint32_t`. U `uint16_t` by se dlouhý
  úsek přes celou šířku dal přetočit.

### Ověřeno

Rozhodující je, že to nestačí zkoušet jedním binárkem — opravený
rozbalovač spolkne i špatně zabalený soubor, takže by opravu baliče
zakryl. Proto se zvlášť přeložila verze, která má opravený **jen
balič**, a měla původní, rozbitý rozbalovač:

| soubor | rozbalovač | výsledek |
|---|---|---|
| původní z Windows yaglu | původní | **segmentation fault** |
| náš, nově zabalený | původní | rozbaleno, 3435 záznamů |

Kontrolní řádek nahoře dokazuje, že test chybu opravdu vidí. Druhý
řádek pak dokazuje, že balič už ji nedělá — nově zabalený soubor
otevře i ten starší yagl pro Windows.

Kolečko tam a zpět je navíc beze ztráty: skript yagl i všechny čtyři
spritesheety mají po rozbalení znovu zabaleného souboru **stejný
kontrolní součet** jako po rozbalení originálu.
