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
