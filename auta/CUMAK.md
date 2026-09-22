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

---

## Oprava: náklad musí jet na viditelném dílu

První stavba verze s článkem vpředu měla chybu. Neviditelný čumák si
nechal `cargo_capacity` a viditelné auto dostalo nulu, takže pro hru
bylo pořád prázdné.

Projevilo se to dvakrát:

- **nebyla vidět grafika plného auta**
- **nešla animace na zastávce**

Obojí dělá to samé. Action02 u vozidel má dva seznamy sad spritů:

| seznam v yaglu | co to je | podle čeho se vybírá |
|---|---|---|
| `primary_spritesets` | stavy podle naloženosti | kolik nákladu díl veze |
| `secondary_spritesets` | stavy při nakládání na zastávce | kolik nákladu díl veze |

Například u valníku na dřevo jsou to `[ 0x0000 0x0001 ]` a
`[ 0x0000 0x0002 ]`, tedy prázdný a plný, a k tomu dvě sady pro
zastávku. Díl s nulovou kapacitou spadne vždycky do sady 0. Plná
sada ani ta zastávková se nemají jak ukázat.

Přesunuto na viditelný díl: `cargo_capacity`, `cargo_type`,
`refittable_cargo_classes`, `non_refittable_cargo_classes`,
`always_refittable_cargos`, `never_refittable_cargos`,
`refit_cargo_types`, `refit_cost`, `loading_speed`. Čumák má teď
kapacitu 0. Součet přes soupravu zůstává stejný, takže v nákupu se
kapacita nezměnila.

Ověřeno po zpětném rozbalení: u všech 18 má čumák kapacitu 0x00
a viditelný díl 0x09 s plným refit seznamem. Článkování, průhledné
sprity i rozcestníky beze změny.

Verze s článkem vzadu tuhle chybu nikdy neměla, tam viditelné auto
zůstalo vepředu i s nákladem. Má ale ten malý klikací box.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | `a258e5cbde833cf318c81b88d3e59e98` |
| `VWT1-S1203-clanek-vzadu.grf` | `19c944b8bd225168353f61208958a154` |


---

## Druhá oprava: čumák nesmí mít nulovou kapacitu

Předchozí oprava přestřelila. Přesunul jsem náklad na viditelné auto
a čumáku nechal nulu, jenže **motor s nulovou kapacitou přijde
o nabídku nákladů**. Projevilo se to takhle:

- v nákupním seznamu se dvanácettrojka neukázala pod filtrem „Dřevo"
- přestavba dala divnou kapacitu a vozidlo nešlo poslat k lesu
- po koupi naskočila červená hláška, že se informace o nákladu
  a přestavbě po nákupu změnily

Ta hláška je kontrola `CheckConsistencyOfArticulatedVehicle`. Hra si
z nákupního seznamu předpoví, co souprava umí vézt, po koupi to
porovná se skutečností, a když se to rozejde, nahlásí GRF jako vadný.

### Jak to má CZTR

Místo dalšího hádání jsem se podíval na vydanou sadu, která funguje.
U článkované soupravy Liaz Plachta+vlek:

| | kupovaný díl 0x0062 | článek 0x0061 |
|---|---|---|
| kapacita | 8 | 10 |
| třídy pro přestavbu | 0x06F4 | 0x06F4 |
| seznam nákladů | stejný | stejný |
| climate | plné | null |

Tedy: **oba díly mají nenulovou kapacitu a úplně stejné refit
vlastnosti.** Kapacity se sčítají.

### Co je teď

| | čumák | viditelné auto | součet |
|---|---|---|---|
| kapacita | 1 | 8 | 9 |

Součet zůstal 9 jako v původní sadě, takže se vozidlo nezesílilo.
Refit seznamy má obojí stejné, u všech 18 ověřeno. Čumák veze jednu
jednotku neviditelně, viditelné auto osm, takže jeho grafika sleduje
naloženost skoro přesně.

Ověřeno po zpětném rozbalení: 876 záznamů, 18 dvojic s kapacitami
1 a 8, shodné refit seznamy, 18 článkovacích callbacků. U valníku na
dřevo je 0x24 v seznamu na obou dílech.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | `7755dc90c5dc9537c7f08a4be429197c` |

---

## Doladění o pixel, jen jihozápad (2026-09-19)

Kvůli zarovnání na vagonky. Čtyři vozidla, **jen směr 5 jihozápad**,
všechny čtyři sady spritů (prázdná, plná, dvě zastávkové), posun
**x−1 y−1** přímo na offsetech. Jiný směr se nikde nezměnil.

| vozidlo | sada 0 | sada 1 | sada 2 | sada 3 |
|---|---|---|---|---|
| 0x0082 Škoda 1203 Pajda karavan | −29 −30 → −30 −31 | −29 −31 → −30 −32 | −30 −35 → −31 −36 | −30 −35 → −31 −36 |
| 0x0095 TAZ 1500 dodávka zahrádka | −28 −31 → −29 −32 | −28 −30 → −29 −31 | −29 −31 → −30 −32 | −27 −36 → −28 −37 |
| 0x0096 TAZ 1500 dodávka zahrádka bedna | −28 −31 → −29 −32 | −28 −30 → −29 −31 | −27 −35 → −28 −36 | −27 −36 → −28 −37 |
| 0x0097 TAZ 1500 dodávka | **−28 −28 → −29 −29** | −28 −27 → −29 −28 | −29 −28 → −30 −29 | −27 −36 → −28 −37 |

Tučná hodnota je ta, kterou jsi uvedl jako příklad. Seděla, takže
jsem mířil na správné sprity.

### Co se kontrolovalo předem

Jeden sprit karavanu má podezřele nízké číslo (0x06), tak jsem
prověřil, jestli si některý z těch šestnácti spritů nepůjčuje i jiné
vozidlo. **Nepůjčuje**, všech šestnáct patří jen těmhle čtyřem.

### Ověřeno

Zabaleno a zase rozbaleno: 876 záznamů, **32 rozdílných řádků**, tedy
přesně těch šestnáct změn a nic jiného. Mimo sprity se nezměnilo nic.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | `aeebde590a614220174a2cf66c587923` |

---

## Zatáčky: sever a jih na osu (2026-09-22)

Zatáčecí směry nikdy žádnou odchylku x y nedostaly. Tohle je první.

### Proč to šlo změřit bez hry

Hráčův postřeh: **zrcadlový odraz dvou spritů musí mít křížek na
stejném místě.** U severu a jihu je auto čelem, takže sprit je
zrcadlově souměrný **sám v sobě** a křížek musí sedět na jeho vlastní
ose. To se dá najít proložením siluety s jejím zrcadlem.

| směr | osa proti kotvě před | po |
|---|---|---|
| S sever | +1,0 až +1,5 px | **0,0 až +0,5 px** |
| J jih | +8,5 až +9,0 px | **−0,5 až 0,0 px** |

Shoda siluety se zrcadlem je 0,97 až 1,00, takže osa je určená dobře.
Jih byl o devět pixelů mimo, sever o jeden a půl.

### Posun

**Jednotný pro všechna auta**, aby zůstala řada, která už je hotová:

| směr | xrel | yrel |
|---|---|---|
| S sever | **−1** | beze změny |
| J jih | **−9** | beze změny |

Nasazeno na **58 sad**, tedy všechny, u všech 18 vozidel. Svisle se
nesáhlo na nic: sever a jih mají linku kol 32 a 31 px pod kotvou,
tedy pixel od sebe, a lepší měřítko pro svislou složku nemám.

### Východ a západ zůstaly

Tam auto stojí bokem, takže samo o sobě souměrné není, a zrcadlo se
musí hledat mezi dvěma sprity. Jenže stejnou odchylku, +4 až +15 px,
ukazují i **jízdní** dvojice SV/SZ a JV/JZ, o kterých hráč říká, že
jsou dobře. Zrcadlo napříč levá–pravá tedy není spolehlivé měřítko
a hádat nebudu.

### Ověřeno

Zabaleno a zase rozbaleno: 876 záznamů, **232 rozdílných řádků**,
tedy 116 spritů krát dva, a mimo sprity **nic**.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | `6c24ce81f3f6d9f5e27ab5acb882d06a` |

---

## Zatáčky: i východ a západ (2026-09-22)

Hráč měl pravdu, že protějšek má každý směr, a moje opatrnost u boků
byla zbytečná. Nechal jsem počítač najít, který sprit se kterým
zrcadlově kryje nejlíp, ať se párování nehádá:

| zrcadlím | najde | shoda |
|---|---|---|
| S sever | sám sebe | 0,99 |
| J jih | sám sebe | 1,00 |
| SV | SZ | 0,98 |
| V východ | Z západ | 0,98 |
| JV | JZ | 0,99 |

Párování tedy sedí a siluety jsou opravdu zrcadla. Při překlopení se
kotva se měří od druhého okraje: `sirka - 1 - kotva`.

### Oprava boků

Dvojice se srovnává tak, že se odchylka rozdělí na půl a **oba**
sprity se posunou o polovinu ve vlastním rámci. To je v obraze posun
na opačné strany, takže dvojice zůstane souměrná.

| dvojice | odchylka před | posun | odchylka po |
|---|---|---|---|
| V východ ↔ Z západ | +10 až +11 px | **oba xrel −5** | **+0 až +1 px** |

Nasazeno na všech 58 sad. Svisle beze změny, tam byla odchylka −1 až
+1 px už předtím.

### Co zůstává otevřené: jízdní dvojice

Stejný test na jízdních směrech dává:

| dvojice | odchylka |
|---|---|
| SV ↔ SZ | +4 až +5 px |
| JV ↔ JZ | +13 až +15 px |

Souměrné tedy nejsou ani ony. Srovnat by je šlo stejně, posunem o 2
a o 7 px u každého člena. **Nesáhl jsem na ně**, protože jízdní směry
jsou odsouhlasené a ve hře odzkoušené, a takový posun by byl vidět.
Čeká to na rozhodnutí.

### Ověřeno

876 záznamů, 232 rozdílných řádků, mimo sprity nic.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanek-vpredu.grf` | `cadb1bde0df409fc957b23d7a59cd5e8` |

---

## Články z obou stran (2026-09-22)

### Nejdřív to, co nejde

Článek **nejde zmenšit pod jednu osminu dlaždice**. OpenTTD počítá

```
delka = 8 - shorten_vehicle,   shorten_vehicle je cele cislo nejvys 7
```

takže délka je celý počet osmin, 1 až 8. Čtvrtina ani polovina osminy
neexistuje, není to volba nastavení, je to formát.

### Jak se rozestup vlastně skládá

Díly soupravy se pouštějí z depa po délce toho **předního**, a blokuje
kterýkoliv díl cizí soupravy. Pro sestavu čumák, auto, ocas tedy:

```
rozestup auto-auto = delka auta + 8 + delka cumaku
```

Zadní článek nepřidá svoji délku, ale **délku auta před sebou**. To je
to podstatné a je to proti intuici.

| sestava | čumák | auto | ocas | rozestup | proti 8 |
|---|---|---|---|---|---|
| článek jen vepředu | 1 | 8 | – | 9 | +12,5 % |
| oba články, auto dlouhé | 1 | 8 | 1 | **17** | +112,5 % |
| oba články, auto krátké | 1 | 1 | 1 | **10** | **+25,0 %** |

### Dosažitelné kroky

| rozestup | proti 8 |
|---|---|
| 9 | +12,5 % |
| 10 | **+25,0 %** |
| 11 | +37,5 % |
| 12 | +50,0 % |

**25 % tedy sedí přesně. 20 % je mezi dvěma kroky a nedá se zapsat.**

### Dva soubory

| soubor | sestava | rozestup |
|---|---|---|
| `VWT1-S1203-clanky-oba-dlouhe-auto.grf` | 1, 8, 1 | 17 |
| `VWT1-S1203-clanky-oba-na-stred.grf` | 1, 1, 1 | 10 |

Ten druhý je těch 25 %. Auto je v soupravě uprostřed, mezi dvěma
stejně dlouhými články, takže by mělo líp sednout na vagon.

**Co to stojí:** klikací box je u silničního vozidla přesně jeho
délka, takže u varianty na střed spadne z 8 jednotek na 1. Články po
stranách mají po jedné, dohromady 3 jednotky kolem auta.

Zadní článek je jedno společné číslo `0x00C0` pro všech 18 vozidel,
neviditelné, délka 1.

### Ověřeno

Obě varianty zabaleny a zase rozbaleny: 888 záznamů, tři díly na
soupravu, čumák 1, ocas 1, auto 8 respektive 1.

| soubor | md5 |
|---|---|
| `VWT1-S1203-clanky-oba-dlouhe-auto.grf` | `1fc97038aad4463c21494bc5180de597` |
| `VWT1-S1203-clanky-oba-na-stred.grf` | `43dc34528aae5fb164b7127686bd9a30` |
