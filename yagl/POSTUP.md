# yagl — jak s ním pracovat

Obousměrný převodník **GRF ↔ YAGL**. Zdroj: https://github.com/UnicycleBloke/yagl
(zde vendorovaná kopie `yagl-main/`, hráč ji poslal 2026-09-11).

Tohle je ten nástroj, kterým se u nás dělá GRF. **Ne nml.**

## Přeložit

```bash
cd yagl/yagl-main
mkdir -p build && cd build
cmake -G Ninja ..
ninja
```

Trvá **32 sekund**. Potřebuje `cmake`, `ninja` (nebo `make`), `g++`
a `libpng-dev` — v tomhle prostředí bylo všechno už nainstalované.
Binárka pak leží v `yagl/yagl-main/build/yagl`.

Ověřeno: vlastní testy projdou (`./yagl_tests` → 2 685 471 assertions,
75 test cases, all passed).

## Rozebrat GRF

```bash
yagl -d neco.grf
```

Vznikne `sprites/` a v něm `neco.yagl`, spritesheety `*.png`
a zvuky `*.wav`.

## Složit GRF

```bash
yagl -e neco.grf sprites
```

## !!! POZOR NA JMÉNO !!!

**`.yagl` se musí jmenovat stejně jako cílový `.grf`.** Encoder hledá
`<jméno>.yagl` uvnitř zadané složky a podle jména cílového GRF.

```bash
yagl -e letadlo.grf sprites     # hleda sprites/letadlo.yagl
```

Když se jméno neshoduje, spadne to na
`ERROR: File 'sprites/letadlo.yagl' does not exist`.

A druhá polovina toho pravidla, kterou zadal hráč: **soubor se musí
jmenovat stejně jako jméno GRF v seznamu ve hře**, jinak ho mezi
ostatními nenajde. Takže jméno souboru, jméno `.yagl` a `name:`
v Action08 držet pohromadě.

Ještě jedna drobnost, na kterou jsem naletěl: yagl nebere cestu
s jiným názvem, než má soubor. Nahraný soubor měl prefix
(`64b74c3c-kaas_planes.grf`) a yagl hlásil „does not exist“, i když
tam byl — přejmenovat na čisté jméno.

## Ověřený round-trip

`kaas_planes.grf` (3 651 625 B) → rozebrat → složit → 3 651 635 B.
Rozdíl **10 bajtů (0,000 %)**. README to popisuje jako očekávané:
sjednocení duplicitních vlastností v Action00, jiné pořadí, varianty
kódování řetězců. Sémanticky totožné.
