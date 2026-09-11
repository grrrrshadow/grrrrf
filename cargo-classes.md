# Kódy nákladu pro GRF — rozluštěná tabulka cargo class

Zdroj: NewGRF specs, stránka CargoTypes
(https://newgrf-specs.tt-wiki.net/wiki/CargoTypes). Tu doménu mi egress
proxy blokuje, takže obsah tabulky mi sem vložil hráč 2026-09-11 — tohle
je moje jediná kopie.

## Jak se to čte

Čtyřmístné číslo u každého nákladu **není pořadové číslo**. Je to
šestnáctkový **bitmask tříd nákladu** (cargo classes) — každý bit je
jedna vlastnost a sčítají se. `0084` proto není „náklad č. 84", ale
`0x80 | 0x04` = chlazený + expresní.

| bit | hex | třída |
|---|---|---|
| 0 | `0x0001` | passengers |
| 1 | `0x0002` | mail |
| 2 | `0x0004` | express |
| 3 | `0x0008` | armoured |
| 4 | `0x0010` | bulk |
| 5 | `0x0020` | piece goods |
| 6 | `0x0040` | liquid |
| 7 | `0x0080` | refrigerated |
| 8 | `0x0100` | hazardous |
| 9 | `0x0200` | covered/sheltered |
| 10 | `0x0400` | oversized |
| 11 | `0x0800` | powderized |
| 12 | `0x1000` | non-pourable |
| 13 | `0x2000` | potable? |
| 14 | `0x4000` | non-potable? |
| 15 | `0x8000` | special |

Bity 13 a 14 (`0x2000`, `0x4000`) se v celé tabulce neobjevily ani
jednou — ve vložených datech pro ně nemám doklad, takže si je nevymýšlím.
Až bude stránka dostupná, doplnit.

Příklady rozkladu:

- `FOOD` = `0x0084` = 0x0004 + 0x0080 → express, refrigerated
- `MILK` = `0x00C4` = 0x0004 + 0x0040 + 0x0080 → express, liquid, refrigerated
- `BAKE` = `0x0A30` = 0x0010 + 0x0020 + 0x0200 + 0x0800 → bulk, piece goods, covered/sheltered, powderized
- `SCMT` = `0x1010` = 0x0010 + 0x1000 → bulk, non-pourable
- `KAOL` = `0x0250` = 0x0010 + 0x0040 + 0x0200 → bulk, liquid, covered/sheltered
- `YETI` = `0x0404` = 0x0004 + 0x0400 → express, oversized

## Formát labelu

Label je **4 znaky ASCII**, v GRF uložený jako 32bitová hodnota těch
čtyř bajtů. Kratší jména se doplňují podtržítkem: `OIL_`, `LYE_`,
`NH3_`, `PCL_`, `O2__`. Label je to, co je napříč GRFy stabilní —
slot/číslo nákladu ve hře se mění podle toho, jaký industry set běží,
proto se na slot nikdy nespoléhat a překládat přes cargo translation
table. *(Tahle část je z mojí znalosti specifikace, ne z vložených dat —
ověřit, až půjde stránka otevřít.)*

## Dvě vady ve zdroji

1. **`SCRP` má nesedící údaj.** Tabulka u něj uvádí `0010 Piece goods`,
   jenže `0x0010` je *bulk*; piece goods je `0x0020`. Jeden z těch dvou
   údajů je špatně. `SCRP` je stejně označený jako zastaralý (místo něj
   `SCMT`), takže to nejspíš nikoho netrápí — ale nekopírovat to.
   Zkontrolováno strojově: tohle je **jediný** nesoulad ze 144 řádků,
   které kód mají.
2. **`ELEC` a `NODC` chybí.** U `ELTR` je poznámka, že CZIS používá
   vlastní labely `ELEC` a `NODC` — ale ani jeden z nich v tabulce svůj
   řádek nemá. Pokud je budu potřebovat, musí se dohledat jinde.

## Celá tabulka (label → bitmask → rozklad)

Rozklad ve třetím sloupci je spočítaný z hex hodnoty, ne opsaný.
`CZIS` = náklad používá Czech Industry Set (to je pro CZTR ten podstatný
sloupec).

| label | hex | třídy z bitmasku | skupina | CZIS |
|---|---|---|---|---|
| `PASS` | `0001` | passengers | zakladni | ano |
| `COAL` | `0010` | bulk | zakladni | ano |
| `MAIL` | `0002` | mail | zakladni | ano |
| `OIL_` | `0040` | liquid | zakladni | ano |
| `LVST` | `0020` | piece goods | zakladni | ano |
| `GOOD` | `0004` | express | zakladni | ano |
| `GRAI` | `0010` | bulk | zakladni | ano |
| `WOOD` | `0020` | piece goods | zakladni | ano |
| `IORE` | `0010` | bulk | zakladni | ano |
| `STEL` | `0020` | piece goods | zakladni | ano |
| `VALU` | `0008` | armoured | zakladni |  |
| `PAPR` | `0020` | piece goods | zakladni | ano |
| `WHEA` | `0010` | bulk | zakladni |  |
| `FOOD` | `0084` | express, refrigerated | zakladni | ano |
| `GOLD` | `0008` | armoured | zakladni |  |
| `RUBR` | `0040` | liquid | zakladni |  |
| `FRUT` | `0090` | bulk, refrigerated | zakladni | ano |
| `MAIZ` | `0010` | bulk | zakladni |  |
| `CORE` | `0010` | bulk | zakladni | ano |
| `WATR` | `0040` | liquid | zakladni |  |
| `DIAM` | `0008` | armoured | zakladni |  |
| `SUGR` | `0010` | bulk | zakladni |  |
| `AORE` | `0010` | bulk | zakladni | ano |
| `BDMT` | `0220` | piece goods, covered/sheltered | zakladni | ano |
| `BEAN` | `0010` | bulk | zakladni | ano |
| `BEER` | `0064` | express, piece goods, liquid | zakladni | ano |
| `BOOM` | `0024` | express, piece goods | zakladni |  |
| `BRCK` | `0020` | piece goods | zakladni |  |
| `CBLK` | `0230` | bulk, piece goods, covered/sheltered | zakladni |  |
| `CERA` | `0020` | piece goods | zakladni |  |
| `CERE` | `0210` | bulk, covered/sheltered | zakladni |  |
| `CLAY` | `0210` | bulk, covered/sheltered | zakladni | ano |
| `CMNT` | `0210` | bulk, covered/sheltered | zakladni | ano |
| `COPR` | `0020` | piece goods | zakladni | ano |
| `CSTI` | `0020` | piece goods | zakladni |  |
| `CTAR` | `0140` | liquid, hazardous | zakladni |  |
| `DYES` | `0060` | piece goods, liquid | zakladni |  |
| `ENSP` | `0024` | express, piece goods | zakladni | ano |
| `FECR` | `0010` | bulk | zakladni |  |
| `FERT` | `0030` | bulk, piece goods | zakladni |  |
| `FICR` | `0030` | bulk, piece goods | zakladni |  |
| `FISH` | `0084` | express, refrigerated | zakladni |  |
| `FMSP` | `0024` | express, piece goods | zakladni | ano |
| `GLAS` | `0420` | piece goods, oversized | zakladni | ano |
| `GRVL` | `0010` | bulk | zakladni | ano |
| `JAVA` | `0024` | express, piece goods | zakladni |  |
| `KAOL` | `0250` | bulk, liquid, covered/sheltered | zakladni | ano |
| `LIME` | `0010` | bulk | zakladni | ano |
| `MILK` | `00C4` | express, liquid, refrigerated | zakladni | ano |
| `OLSD` | `0210` | bulk, covered/sheltered | zakladni |  |
| `PEAT` | `0010` | bulk | zakladni |  |
| `PETR` | `0040` | liquid | zakladni | ano |
| `PHOS` | `0010` | bulk | zakladni |  |
| `PLAS` | `0060` | piece goods, liquid | zakladni | ano |
| `PORE` | `0010` | bulk | zakladni |  |
| `POTA` | `0210` | bulk, covered/sheltered | zakladni |  |
| `RFPR` | `0040` | liquid | zakladni | ano |
| `SAND` | `0010` | bulk | zakladni | ano |
| `SCMT` | `1010` | bulk, non-pourable | zakladni | ano |
| `SULP` | `0250` | bulk, liquid, covered/sheltered | zakladni | ano |
| `TOUR` | `0005` | passengers, express | zakladni |  |
| `TYRE` | `0020` | piece goods | zakladni | ano |
| `URAN` | `0110` | bulk, hazardous | zakladni |  |
| `VEHI` | `0420` | piece goods, oversized | zakladni | ano |
| `WDPR` | `0030` | bulk, piece goods | zakladni | ano |
| `WOOL` | `0220` | piece goods, covered/sheltered | zakladni |  |
| `ZINC` | `0020` | piece goods | zakladni |  |
| `ACID` | `0140` | liquid, hazardous | rozsirene | ano |
| `ALUM` | `0020` | piece goods | rozsirene | ano |
| `BAKE` | `0A30` | bulk, piece goods, covered/sheltered, powderized | rozsirene |  |
| `CASS` | `0010` | bulk | rozsirene |  |
| `CHLO` | `0140` | liquid, hazardous | rozsirene |  |
| `CHSE` | `00C4` | express, liquid, refrigerated | rozsirene |  |
| `CIGR` | `0024` | express, piece goods | rozsirene |  |
| `COAT` | `0060` | piece goods, liquid | rozsirene |  |
| `COBL` | `0020` | piece goods | rozsirene |  |
| `COKE` | `0010` | bulk | rozsirene | ano |
| `ELTR` | `8000` | special | rozsirene |  |
| `EOIL` | `0060` | piece goods, liquid | rozsirene |  |
| `FRVG` | `00A4` | express, piece goods, refrigerated | rozsirene |  |
| `FUEL` | `0140` | liquid, hazardous | rozsirene |  |
| `FURN` | `0230` | bulk, piece goods, covered/sheltered | rozsirene | ano |
| `IRON` | `0020` | piece goods | rozsirene |  |
| `LYE_` | `0140` | liquid, hazardous | rozsirene |  |
| `MEAT` | `00A4` | express, piece goods, refrigerated | rozsirene |  |
| `METL` | `0020` | piece goods | rozsirene |  |
| `MNO2` | `0010` | bulk | rozsirene |  |
| `MNSP` | `0024` | express, piece goods | rozsirene |  |
| `MOLS` | `0040` | liquid | rozsirene |  |
| `MPTS` | `0220` | piece goods, covered/sheltered | rozsirene |  |
| `NH3_` | `0140` | liquid, hazardous | rozsirene | ano |
| `NHNO` | `0130` | bulk, piece goods, hazardous | rozsirene | ano |
| `NUTS` | `0020` | piece goods | rozsirene |  |
| `NICK` | `0010` | bulk | rozsirene |  |
| `NITR` | `0010` | bulk | rozsirene | ano |
| `NKOR` | `0010` | bulk | rozsirene |  |
| `OILI` | `0040` | liquid | rozsirene |  |
| `OILD` | `0040` | liquid | rozsirene |  |
| `OTI1` | `0001` | passengers | rozsirene |  |
| `OTI2` | `0001` | passengers | rozsirene |  |
| `OYST` | `00A4` | express, piece goods, refrigerated | rozsirene |  |
| `O2__` | `0040` | liquid | rozsirene |  |
| `PACK` | `0020` | piece goods | rozsirene | ano |
| `PCL_` | `0006` | mail, express | rozsirene |  |
| `PIPE` | `0020` | piece goods | rozsirene | ano |
| `POWR` | `0020` | piece goods | rozsirene | ano |
| `QLME` | `0210` | bulk, covered/sheltered | rozsirene | ano |
| `RCYC` | `0030` | bulk, piece goods | rozsirene |  |
| `SALT` | `0010` | bulk | rozsirene |  |
| `SASH` | `0210` | bulk, covered/sheltered | rozsirene |  |
| `SEED` | `0230` | bulk, piece goods, covered/sheltered | rozsirene |  |
| `SESP` | `0024` | express, piece goods | rozsirene |  |
| `SGBT` | `0010` | bulk | rozsirene | ano |
| `SGCN` | `1010` | bulk, non-pourable | rozsirene |  |
| `SLAG` | `0010` | bulk | rozsirene | ano |
| `SOAP` | `0060` | piece goods, liquid | rozsirene |  |
| `STAL` | `0020` | piece goods | rozsirene | ano |
| `STCB` | `0020` | piece goods | rozsirene |  |
| `STSE` | `0020` | piece goods | rozsirene | ano |
| `STSH` | `0020` | piece goods | rozsirene | ano |
| `STST` | `0020` | piece goods | rozsirene |  |
| `STWR` | `0020` | piece goods | rozsirene |  |
| `TATO` | `00A4` | express, piece goods, refrigerated | rozsirene |  |
| `TEXT` | `0220` | piece goods, covered/sheltered | rozsirene |  |
| `TBCO` | `1010` | bulk, non-pourable | rozsirene |  |
| `TWOD` | `0020` | piece goods | rozsirene |  |
| `VBOD` | `0020` | piece goods | rozsirene | ano |
| `VENG` | `0020` | piece goods | rozsirene | ano |
| `VPTS` | `0024` | express, piece goods | rozsirene | ano |
| `WSTE` | `0230` | bulk, piece goods, covered/sheltered | rozsirene | ano |
| `BATT` | `0020` | piece goods | rozsirene |  |
| `BUBL` | `0020` | piece goods | fantasy |  |
| `COLA` | `0040` | liquid | fantasy |  |
| `CTCD` | `0010` | bulk | fantasy |  |
| `FZDR` | `0020` | piece goods | fantasy |  |
| `PLST` | `0040` | liquid | fantasy |  |
| `SWET` | `0004` | express | fantasy |  |
| `TOFF` | `0010` | bulk | fantasy |  |
| `TOYS` | `0020` | piece goods | fantasy |  |
| `YETI` | `0404` | express, oversized | fantasy |  |
| `YETY` | `0404` | express, oversized | fantasy |  |
| `GEAR` | `8000` | special | specialni |  |
| `RSGR` | `0010` | bulk | zastarale |  |
| `SCRP` | `0010` | bulk | zastarale |  |

## Co v téhle kopii NENÍ

Vložená tabulka měla i sloupce pro ostatní industry sety (TTD, ECS,
YETI, OTIS, XIS, 2TT) a poznámky o přejmenováních a odchylkách tříd
v jednotlivých setech (např. OTIS má `PAPR` jako `0220`, XIS má `FRUT`
jako `00A4`). Z těch jsem si vytáhl jen **CZIS**, protože CZTR je český
set. Zbytek zatím uložený nemám — kdyby byl potřeba, musí se vložit znovu.

## Doplněk 2026-09-11

Labelů je celkem **146**, ne 144. `NUKF` a `NUKW` mají třídy popsané jen
slovy („Piece goods, hazardous") a číselný kód jim ve zdroji chybí, proto
v tabulkách výš nejsou. Úplný seznam zkratek je v `naklady.md`.
