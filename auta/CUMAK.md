# Neviditelný čumák: rozestup v koloně

`VWT1-S1203-cumak.grf` — všech 18 vozidel sady přestavěno.
Testovací soubor, jméno GRF a číslo zůstávají stejná, takže se
nahradí původní `VWT1-S1203modradodavka.grf`.

## Proč to jinak nejde

Odstup, na který auto zastaví za jiným, je v OpenTTD natvrdo 8
jednotek mezi středy a délka vozidla do něj nevstupuje. Žádná
vlastnost GRF na to nesahá.

Ale díly jedné soupravy se pouštějí z depa po `cached_veh_length`
snímcích toho **předního** a ten rozestup pak drží. A blokuje
kterýkoliv díl cizí soupravy. Takže:

> rozestup mezi dvěma auty = 8 + délka vedoucího dílu

## Jak je to udělané

Z každého vozidla je dvoudílná souprava:

| díl | číslo | délka | co dělá |
|---|---|---|---|
| čumák | původní, 0x0080 až 0x0097 | 1 | neviditelný, drží jméno, cenu, náklad i ikonu v nákupu |
| auto | nové, 0x00A0 až 0x00B7 | 8 | veze grafiku, v nákupu se neukazuje |

**Kupované číslo se nemění.** Z původního čísla se stal ten čumák,
takže uložené hry o motor nepřijdou. Přibylo jen nové číslo pro
viditelné auto.

Délka auta do rozestupu nevstupuje, takže si nechalo plných 8 a s
tím i plný klikací box.

## Čísla

| stav | auto zabírá | mezera z 8 |
|---|---|---|
| před zvětšením grafiky o 20 % | 5,8 jednotky | 2,2 |
| dnes | 7,0 jednotky | 1,0 |
| **s čumákem délky 1** | 7,0 jednotky | **2,0** |

Měřeno na inkoustu spritů dvanácettrojky ve čtyřech hlavních směrech
jízdy: 56 px při čtyřnásobném přiblížení, a jedna jednotka délky je
tam 8 px.

Čumák délky 1 tedy vrací skoro přesně mezeru, jaká byla před
zvětšením. Kdyby to bylo málo, dvojka dá mezeru 3,0, tedy víc, než
kdy bývala.

## Na co se dívat

1. **Kolona.** Postav pár aut za sebe a nech je zastavit. Mezi nimi
   má být mezera zhruba jako před zvětšením.
2. **Nákupní seznam.** Ikona má být jako dřív. Jestli se kreslí dvakrát
   nebo divně, je to tím, že článkovaná souprava se v seznamu vykresluje
   po dílech — dá se doladit.
3. **Kde auto stojí.** Viditelné auto se kreslí o jednu jednotku za
   místem, kde si hra myslí, že vozidlo je. Na zastávce to může být
   o 8 px při čtyřnásobném přiblížení.
4. **Zatáčky.** Souprava je teď o jednotku delší, průjezd zatáčkou se
   může chovat jinak.

## Ověřeno

Zabaleno a zase rozbaleno: 876 záznamů, 18 čumáků délky 1, 18
viditelných dílů délky 8, 18 článkovacích callbacků a 144 průhledných
spritů. Vše přežilo.
