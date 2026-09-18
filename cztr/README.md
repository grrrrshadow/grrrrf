# CZTR truck set

## CZTR_Truck_SetBRYLE1-prebaleno.grf

Původní set rozbalený a znovu zabalený naším opraveným yaglem.
**Žádná obsahová změna** — je to kontrola, že přebalení nic nerozbilo,
než se sáhne na rozestupy.

Proč to vůbec bylo potřeba: po zvětšení grafiky o 20 % se set nedal
rozbalit, yagl na něm padal. Nešlo o náš yagl — zabalila ho starší
verze pro Windows a ta ho pak sama taky nerozbalila. Rozbor a oprava
jsou v `../yagl/NASE-UPRAVY.md`, kapitola 2.

Ověření, že přebalení je beze ztráty: rozbalí-li se tenhle soubor
znovu, skript yagl i všechny čtyři spritesheety mají **stejný
kontrolní součet** jako z originálu.

| | |
|---|---|
| záznamů | 3435 |
| velikost | 38 261 099 B (originál 38 261 102 B) |
| md5 | `aee7f8a1f043b1d7b1a49a1976dddfe8` |

Otevře ho i ten starší yagl pro Windows — značka konce řádku je v něm
už napsaná správně.

---

## CZTR_Truck_SetBRYLE1-rozestupy.grf

Tohle je ten soubor k vyzkoušení ve hře. Přebalený set **plus zvětšené
rozestupy** mezi tahačem a přívěsem.

### Proč byl rozestup malý

Sprity vyrostly o 20 %, ale délky vozidel ve hře zůstaly. Sprit se
kreslí celý, ať se do své délky vejde nebo ne, takže o co sprit
povyrostl, o to se nacpal do mezery za sebou. Mezera se scvrkla
zhruba o desetinu součtu délek obou spritů.

### Co se změnilo

Délka vozidla se zadává vlastností `shorten_vehicle` po osminách
dlaždice: délka = (8 − N)/8. Všech 37 vozidel dostalo délku o 20 %
větší, což u hodnot 1 až 4 vždycky vyjde na **N o jedničku menší**:

| bylo N | je N | délka bylo | délka je | změna | kusů |
|---|---|---|---|---|---|
| 1 | 0 | 7/8 | 8/8 | +14,3 % | 7 |
| 2 | 1 | 6/8 | 7/8 | +16,7 % | 10 |
| 3 | 2 | 5/8 | 6/8 | +20,0 % | 14 |
| 4 | 3 | 4/8 | 5/8 | +25,0 % | 6 |

U N=1 je strop: 8/8 je celá dlaždice a delší road vehicle být nemůže,
takže tahle sedmička dostala jen +14,3 % místo +20 %. Rozptyl +14 až
+25 % jde za osminovým rozlišením formátu, jemněji to zadat nejde.

### Oba „Neviditelné články" zůstaly beze změny

Schválně. Mají délku 1/8 a 2/8 a 20 % z osminy je 0,15 osminy —
nejbližší zadatelná hodnota je pořád ta stávající. Není to potřeba:
mezeru obnoví už samo prodloužení tahače a přívěsu. Kdyby prodloužil
i článek, byla by mezera o 20 % větší, než bývala. Takhle se vrátí
přesně na původní velikost.

Jestli chceš mezeru **větší, než byla původně**, řekni a přidám
článku jednu osminu. To je ale skok o 100 % u kratšího a 50 % u
delšího, jemnější krok formát nedovolí.

### Ověřeno

- Rozbalením znovu: **jediný rozdíl** proti původnímu skriptu je těch
  37 hodnot. Nic jiného, ani o řádek.
- Všechny čtyři spritesheety mají **stejný kontrolní součet** jako
  z originálu. Na grafiku se nesáhlo.
- Otevře ho i starší yagl pro Windows s původním rozbalovačem:
  3435 záznamů, bez pádu.

| | |
|---|---|
| záznamů | 3435 |
| velikost | 38 261 099 B |
| md5 | `3c54f81d084d2c136fb51963c25106b9` |

### Všech 39 vozidel

| vozidlo | název | bylo | je | délka bylo | délka je | změna |
|---|---|---|---|---|---|---|
| `0x0058` | Neviditelný článek | 7 | 7 | 0.125 | 0.125 | beze změny |
| `0x0059` | Neviditelný článek | 6 | 6 | 0.250 | 0.250 | beze změny |
| `0x005A` | Škoda Sentinel (Valník) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x005B` | Avia A31 (Pošta) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x005C` | Avia A31 (Chladicí vůz) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x005D` | Avia A31 (Plachta) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x005E` | Avia A31 (Sklápěč) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x005F` | Avia A31 (Valník) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0060` | Liaz.100 (Plachta) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x0061` | Liaz.100 (Plachta+vlek) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0062` | Liaz.100 (Plachta+vlek) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x0063` | Liaz.100 - Kamion (Plachta) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0064` | Liaz.100 - Kamion (Plachta) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x0065` | Liaz.100 - Kamion (Kontejner) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0066` | Liaz.100 - Kamion (Kontejner) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x0067` | Liaz.100 - Kamion (Chemie) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0068` | Liaz.100 - Kamion (Chemie) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x0069` | Liaz.100 - Kamion (BENZINA) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x006A` | Liaz.100 - Kamion (BENZINA) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x006B` | Liaz.100 (Chladicí vůz) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x006C` | Liaz.100 (Chladicí vůz) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x006D` | Liaz.300 (Popeláři) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x006E` | Liaz.100 - Cisterna (Benzina) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x006F` | Liaz.100 - Kamion (Sklápěč) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0070` | Liaz.100 - Kamion (Sklápěč) | 4 | 3 | 0.500 | 0.625 | +25.0 % |
| `0x0071` | Škoda 706 (Mléko) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0072` | Škoda 706 (Agro) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0073` | Škoda 706 (Agro+vlek) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0074` | Škoda 706 (Agro+vlek) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0075` | Tatra 111 (Cisterna) | 1 | 0 | 0.875 | 1.000 | +14.3 % |
| `0x0076` | Tatra 148 (Dřevo) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0077` | Tatra 148 (Dřevo) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x0078` | Tatra 815 6x6 (Autodomíchávač) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x0079` | Tatra 815 6x6(Sklápěč) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x007A` | Tatra 815 6x6(Sklápěč+vlek) | 3 | 2 | 0.625 | 0.750 | +20.0 % |
| `0x007B` | Tatra 815 6x6(Sklápěč+vlek) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x007C` | Tatra 815 6x6 (Valník) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x007D` | Tatra 815 6x6 (Valník+vlek) | 2 | 1 | 0.750 | 0.875 | +16.7 % |
| `0x007E` | Tatra 815 6x6 (Valník+vlek) | 2 | 1 | 0.750 | 0.875 | +16.7 % |

---

## CZTR_Truck_SetBRYLE1-rozestupy-cisty.grf

To samé co `-rozestupy`, plus vyčištěné sprity.

### Co se čistilo

Rendery mají dvě vrstvy smetí:

1. **Závoj** průhlednosti 1 až 7 přes celý obdélník spritu. Je to
   2 % plochy listů a je úplně neviditelný, ale drží obdélníky
   nafouklé, protože podle něj vypadá, že tam obsah je.
2. **Smítka**, hrstka plně krycích pixelů daleko od vozu. Ta už
   vidět jsou — při čtyřnásobném přiblížení jsou to tečky na silnici.

Popelář byl nejhorší: obdélník 260 × 216 na vůz široký 35 px, kvůli
smítku 3 × 4 px ve vzdálenosti 220 px. Právě tohle smítko přehouplo
sprit přes 256 px a shodilo yagl.

### Jak se hledal vůz

Sloupec po sloupci a řádek po řádku se sečtou neprůhledné pixely,
a bere se ten souvislý úsek, kde jich je nejvíc. Mezera do 32 px se
toleruje, aby se neutrhlo rameno jeřábu nebo zrcátko. Postupuje se
od obou okrajů dovnitř. Pak se přidá jeden pixel čistého lemu, aby
yagl nehlásil, že se obsah dotýká kraje.

### Výsledek

| | před | po |
|---|---|---|
| nejširší sprit | 260 px | 228 px |
| spritů nad 256 px | 4 | 0 |
| plocha spritů | 17,2 M px | 16,3 M px |
| velikost souboru | 38 261 099 B | 36 825 474 B |
| varování při balení | 3021 | 3021 |

Žádný sprit už nepřelézá 256 px, takže se ten chunkovaný formát ani
nepřepne do dlouhé varianty.

### Ověřeno pixel po pixelu

Rozbalí-li se výsledek a porovná se s originálem tak, že se každý
sprit položí podle své kotvy:

| | |
|---|---|
| viditelných pixelů, které zmizely | 149 (to jsou ta smítka, ve 20 spritech) |
| viditelných pixelů, které přibyly | 0 |
| pixelů na stejném místě s jinou barvou | 0 |

**Nic se nepohnulo.** Zarovnání zůstalo na milimetr stejné, ubyla
jen ta smetí.

| | |
|---|---|
| záznamů | 3435 |
| md5 | `e094c60267aade095090ab76f685e0f4` |
