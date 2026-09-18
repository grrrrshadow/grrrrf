# Neviditelný článek: rozestup v koloně

`VWT1-S1203-cumak.grf` — všech 18 vozidel sady. Nahrazuje původní
`VWT1-S1203modradodavka.grf`, číslo GRF je stejné.

## Proč první pokus zmizel

Napsal jsem to obráceně: grafiku vezl zadní díl a vepředu byl
neviditelný čumák. Jenže:

```cpp
// roadveh_cmd.cpp, uvnitr CmdBuildRoadVehicle
AddArticulatedParts(v);
```

**Článek se připojuje jedině při koupi vozidla.** Auta, která už ve
hře jezdila, žádný nedostala. Zůstal z nich jen ten neviditelný
přední díl, a proto jezdila a nebyla vidět.

## Jak je to teď

Obráceně, aby to nemohlo zmizet:

| díl | číslo | délka | co dělá |
|---|---|---|---|
| přední | původní, 0x0080 až 0x0097 | 1 | **veze grafiku**, jméno, cenu, náklad i ikonu v nákupu |
| zadní | nové, 0x00A0 až 0x00B7 | 8 | neviditelný, jen dělá místo |

Auto, které ve hře už jezdí, je pořád jen ten přední díl — a ten
kreslí vůz. **Vidět tedy bude vždycky.** Jenom nedostane ten rozestup
navíc, dokud se nekoupí znovu.

## Proč to dává rozestup

Rozestup, na který auto zastaví za jiným, je natvrdo 8 jednotek mezi
středy. Díly jedné soupravy se ale pouštějí z depa po délce toho
předního a ten rozestup pak drží, a blokuje kterýkoliv díl cizí
soupravy. Takže:

> rozestup mezi dvěma auty = 8 + délka předního dílu = 8 + 1 = 9

| stav | auto zabírá | mezera z odstupu |
|---|---|---|
| před zvětšením grafiky o 20 % | 5,8 jednotky | 2,2 |
| dnes | 7,0 jednotky | 1,0 |
| **nově koupené s článkem** | 7,0 jednotky | **2,0** |

## Na co se dívat

1. **Kup nové auto.** Staré jen zůstane vidět, rozestup nedostane.
2. **Kolona.** Postav dvě tři nová za sebe a nech je zastavit.
3. **Klikání.** Přední díl má box 1 jednotku, zadní 8 za autem.
   Jestli se do auta bude trefovat blbě, dá se to přerozdělit.
4. **Zatáčky a zastávka.** Souprava je o jednotku delší než dřív.

Jestli bude mezera pořád malá, přední díl délky 2 dá rozestup 10,
tedy mezeru 3,0 — víc, než kdy bývala.

## Ověřeno

Zabaleno a zase rozbaleno: 876 záznamů, 18 předních dílů délky 1,
18 neviditelných zadních dílů délky 8, 18 článkovacích callbacků,
144 průhledných spritů, 18 rozcestníků vracejících se na původní
grafiku.
