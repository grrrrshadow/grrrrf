# Třídy nákladu (cargo classes) — podle specifikace

Ověřeno **přímo ze zdroje** 2026-09-11, kdy se otevřel přístup na wiki:
https://newgrf-specs.tt-wiki.net/wiki/Action0/Cargos (sekce CargoClasses)
a https://newgrf-specs.tt-wiki.net/wiki/CargoTypes.

Čtyřmístné číslo u nákladu je **bitmask tříd**, ne pořadové číslo.
Vlastnost se v Action0 jmenuje **CargoClasses (16)**, label je **17**.

| bit | hodnota | třída | česky | jak kombinovat |
|---|---|---|---|---|
| 0 | `0x0001` | Passengers | cestující | nekombinovat s ničím jiným |
| 1 | `0x0002` | Mail | pošta | nekombinovat s ničím jiným |
| 2 | `0x0004` | Express | expresní | — |
| 3 | `0x0008` | Armored | cenný / pancéřovaný | nekombinovat s ničím jiným |
| 4 | `0x0010` | Bulk (Uncountable) | sypký, nepočitatelný | lze kombinovat s Piece Goods nebo Liquid |
| 5 | `0x0020` | Piece Goods (Countable) | kusový, počitatelný | lze kombinovat s Bulk nebo Liquid |
| 6 | `0x0040` | Liquid | kapalný | lze kombinovat s Piece Goods nebo Bulk |
| 7 | `0x0080` | Refrigerated | chlazený | nastavit i Piece Goods |
| 8 | `0x0100` | Hazardous | nebezpečný | kombinovat s Piece Goods, Liquid, Bulk nebo Express |
| 9 | `0x0200` | Covered (weather protected) | krytý proti počasí | kombinovat s Piece Goods nebo Bulk |
| 10 | `0x0400` | Oversized | nadrozměrný | kombinovat s Piece Goods |
| 11 | `0x0800` | Powderized | práškový (vyfukuje se vzduchem) | kombinovat s Bulk |
| 12 | `0x1000` | Non-pourable | nesypatelný (do otevřeného, ne do výsypného) | kombinovat s Bulk |
| 13 | `0x2000` | Potable | poživatelný (potravinářský) | nastavit všem potravinářským nákladům |
| 14 | `0x4000` | Non-potable | nepoživatelný | nastavit všem nepotravinářským nákladům |
| 15 | `0x8000` | special | speciální | nenastavovat |

Bity 13 a 14 (Potable / Non-potable) jsem dřív měl s otazníkem, protože
se v žádném nákladu té tabulky neobjevily. **Teď jsou potvrzené ze
specifikace.** Slouží k tomu, aby se potravina nevozila v cisterně od
chemikálií a naopak.

## Tohle je důležitější než samotné bity

Specifikace u té tabulky říká rovnou tři varování, která mění, jak se
na třídy dívat:

1. **Třídy nejsou zaručené.** Doslova: *„there is no guarantee that
   classes won't vary over time or between sets"*. Tentýž label může mít
   v jiném průmyslovém setu jiné třídy.
2. **Na konkrétní náklady se dělá refit podle labelu, ne podle tříd.**
   Třídy jsou na pohodlné hromadné refity („všechno sypké"). Když nám
   záleží na tom, že zrovna tenhle vagon veze zrovna tenhle náklad,
   musí to jít přes label.
3. **Měnit label bez moc dobrého důvodu je považováno za špatnou praxi.**
   Takže co jednou zavedeme, to se nepřejmenovává.

Navíc: **FIRS, AXIS, ITI, Sunshine Trains a Iron Horse se touhle
tabulkou neřídí.** Používají vlastní schéma FRAX
(https://grf.farm/polar-fox/frax_latest.html). Jestli chceme být
kompatibilní s některým z nich, tahle tabulka pro něj neplatí.

## Drobnost, která se hodí

Náklady ve třídě 0 (Passengers) se objeví v **autobusových** zastávkách,
náklady, které v ní nejsou, v **nákladních**. Nic mezi tím.

## Jak se ta překladová tabulka vlastně píše

Je to vlastnost **09** v Action0 pro feature 08 (Global Settings).
V syrovém NFO vypadá takhle (příklad přímo ze specifikace):

```
 // Cargo translation table
   1 * 169      00 08 01 29 00 09
           "COAL" "WATR" "RUBB" "MAIL" "OIL_" // 0-4
           "LVST" "GOOD" "CERE" "GRAN" "WHET" // 5-9
           ...
```

Rozbor hlavičky: `00` = Action0, `08` = feature Global Settings,
`01` = jedna vlastnost, `29` = počet položek (0x29 = 41),
`00 09` = od instance 0, vlastnost 09. Pak jdou čtyřznakové labely
za sebou a **jejich pořadí určuje čísla slotů**.

## Co jsem se tím dozvěděl o slotech

- **GRF verze 8** (tu používáme): hodnota, kterou se náklad označuje
  ve vlastnostech vozidel i průmyslu a v Action3, **je pozice labelu
  v téhle tabulce**. Tím je potvrzené, proč se pořadí nesmí míchat.
- **Od OpenTTD 15.0**: když GRF vlastní tabulku nedodá, použije se
  výchozí podle klimatu (viz CargoDefaultProps). V GRF v8 má **32
  položek**, v GRF v7 dvanáct.
- Výchozí tabulka se chová stejně jako naše vlastní: když se label
  přesune do jiného slotu, přeloží se to správně; když label zmizí,
  náklad se namapuje na neplatný.

## Poznámka ke starému příkladu

V tom příkladu výš jsou labely `RUBB`, `GRAN`, `WHET`, `WODT`, `CERE`,
které v dnešním seznamu nákladů nejsou (dnes `RUBR`, `WHEA`, ...).
Je to starý příklad z dob TTDPatche — **neopisovat z něj labely**,
brát z něj jen tvar zápisu.
