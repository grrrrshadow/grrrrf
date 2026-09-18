# Neviditelný článek: rozestup v koloně

Dvě verze téhož triku na sadě dvanácettrojek, obě přestavují všech 18
vozidel na dvoudílnou soupravu. Liší se jen tím, **který díl je vidět**.

| soubor | vepředu | vzadu |
|---|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | neviditelný, délka 1 | **auto**, délka 8 |
| `VWT1-S1203-clanek-vzadu.grf` | **auto**, délka 1 | neviditelný, délka 8 |

## Proč to dává rozestup

Odstup, na který auto zastaví za jiným, je v OpenTTD natvrdo 8 jednotek
mezi středy a délka vozidla do něj nevstupuje. Díly jedné soupravy se
ale pouštějí z depa po délce toho **předního** a ten rozestup pak drží.
A blokuje kterýkoliv díl cizí soupravy. Z toho:

> rozestup mezi dvěma auty = 8 + délka předního dílu = 8 + 1 = 9

Obě verze tedy dávají **stejný rozestup 9 místo 8**. Mezera mezi auty
vyroste z 1,0 jednotky na 2,0.

## Čím se liší

|  | článek vpředu | článek vzadu |
|---|---|---|
| rozestup v koloně | 9 | 9 |
| klikací box na autě | **8 jednotek, celý** | 1 jednotka |
| auta, která ve hře už jezdí | zmizí, dokud je nekoupíš znovu | zůstanou vidět |

Klikací box je u silničního vozidla přesně jeho délka. U verze
s článkem vpředu má viditelné auto plných 8 jednotek. U verze s článkem
vzadu má auto délku 1 a těch 8 jednotek sedí za ním, nad prázdnou
silnicí.

**Doporučuju tu s článkem vpředu.** Rozestup je stejný, klikací box
o hodně lepší, a to zmizení starých aut je jednorázová věc: článek se
připojuje jedině při koupi, v `CmdBuildRoadVehicle`, takže stačí koupit
nové. Ověřeno ve hře.

## Jak je to postavené

| díl | číslo | délka |
|---|---|---|
| kupovaný | původní, 0x0080 až 0x0097 | 1 |
| přidaný | nové, 0x00A0 až 0x00B7 | 8 |

Kupované číslo se nemění, takže uložené hry o motor nepřijdou. Jméno,
cena, náklad i ikona v nákupu zůstávají na původním čísle.

Grafiku nese ten díl, který má být vidět; ten druhý dostane osm plně
průhledných spritů 4×4 px.

## Měření

Inkoust spritu dvanácettrojky ve čtyřech hlavních směrech jízdy je při
čtyřnásobném přiblížení 56 px, a jedna jednotka délky je tam 8 px.

| | |
|---|---|
| auto zabírá | 7,0 jednotky |
| odstup v koloně dnes | 8 → mezera 1,0 |
| odstup s článkem | 9 → mezera 2,0 |

Kdyby to bylo málo, přední díl délky 2 dá rozestup 10, tedy mezeru 3,0.

## Ověřeno

Obě verze zabaleny a zase rozbaleny: 876 záznamů, 18 dílů délky 1,
18 dílů délky 8, 18 článkovacích callbacků, 144 průhledných spritů.
