# Zkratky nákladu → co to je

Prostý slovník. Vlevo label, jak se píše v GRF, vpravo co to je.
Nic víc se z toho nevyvozuje — jen opsáno z tabulky, kterou vložil
hráč 2026-09-11 (NewGRF specs, CargoTypes).

**146 zkratek.** Seřazené podle abecedy.

| zkratka | náklad |
|---|---|
| `ACID` | Acid |
| `ALUM` | Aluminium |
| `AORE` | Bauxite (Aluminium ore) |
| `BAKE` | Flour |
| `BATT` | Batteries |
| `BDMT` | Building Materials |
| `BEAN` | Beans |
| `BEER` | Alcohol |
| `BOOM` | Explosives |
| `BRCK` | Bricks |
| `BUBL` | Bubbles |
| `CASS` | Cassava |
| `CBLK` | Carbon Black |
| `CERA` | Ceramics |
| `CERE` | Cereals |
| `CHLO` | Chlorine |
| `CHSE` | Cheese |
| `CIGR` | Cigars |
| `CLAY` | Clay |
| `CMNT` | Cement |
| `COAL` | Coal |
| `COAT` | Paints & Coatings |
| `COBL` | Cobalt |
| `COKE` | Coke |
| `COLA` | Cola |
| `COPR` | Copper |
| `CORE` | Copper Ore |
| `CSTI` | Cast Iron |
| `CTAR` | Coal Tar |
| `CTCD` | Cotton Candy (Candyfloss) |
| `DIAM` | Diamonds |
| `DYES` | Dyes |
| `ELTR` | Electricity |
| `ENSP` | Engineering Supplies |
| `EOIL` | Edible Oil |
| `FECR` | Ferrochrome |
| `FERT` | Fertiliser |
| `FICR` | Fibre crops |
| `FISH` | Fish |
| `FMSP` | Farm Supplies |
| `FOOD` | Food |
| `FRUT` | Fruit |
| `FRVG` | Fruit (and optionally Vegetables) |
| `FUEL` | Natural Gas |
| `FURN` | Furniture |
| `FZDR` | Fizzy Drinks |
| `GEAR` | Locomotive regearing |
| `GLAS` | Glass |
| `GOLD` | Gold |
| `GOOD` | Goods |
| `GRAI` | Grain |
| `GRVL` | Stone |
| `IORE` | Iron Ore |
| `IRON` | Pig Iron |
| `JAVA` | Coffee |
| `KAOL` | Kaolin (China Clay) |
| `LIME` | Lime stone |
| `LVST` | Livestock |
| `LYE_` | Sodium Hydroxide (Lye) |
| `MAIL` | Mail |
| `MAIZ` | Maize |
| `MEAT` | Meat |
| `METL` | Metal |
| `MILK` | Milk |
| `MNO2` | Manganese |
| `MNSP` | Manufacturing Supplies |
| `MOLS` | Molasses |
| `MPTS` | Machine parts |
| `NH3_` | Ammonia |
| `NHNO` | NH4NO3 chemical |
| `NICK` | Nickel |
| `NITR` | Nitrate |
| `NKOR` | Nickel ore |
| `NUKF` | Nuclear fuel |
| `NUKW` | Nuclear waste |
| `NUTS` | Nuts |
| `O2__` | Oxygen |
| `OILD` | Oil (domestic) |
| `OILI` | Oil (imported) |
| `OIL_` | Oil |
| `OLSD` | Oil seed |
| `OTI1` | Workers |
| `OTI2` | Tourists |
| `OYST` | Oysters |
| `PACK` | Packaging |
| `PAPR` | Paper |
| `PASS` | Passengers |
| `PCL_` | Parcels |
| `PEAT` | Peat |
| `PETR` | Petrol / Fuel Oil |
| `PHOS` | Phosphate |
| `PIPE` | Pipe |
| `PLAS` | Plastic |
| `PLST` | Plastic |
| `PORE` | Pyrite Ore |
| `POTA` | Potash |
| `POWR` | Electrical Parts |
| `QLME` | Quicklime |
| `RCYC` | Recyclables |
| `RFPR` | Refined products |
| `RSGR` | Raw Sugar |
| `RUBR` | Rubber |
| `SALT` | Salt |
| `SAND` | Sand |
| `SASH` | Soda Ash |
| `SCMT` | Scrap Metal |
| `SCRP` | Scrap Metal |
| `SEED` | Seed |
| `SESP` | Marine Supplies |
| `SGBT` | Sugar beet |
| `SGCN` | Sugarcane |
| `SLAG` | Slag |
| `SOAP` | Cleaning Agents |
| `STAL` | Alloy Steel |
| `STCB` | Carbon Steel |
| `STEL` | Steel |
| `STSE` | Steel Sections |
| `STSH` | Steel Sheet |
| `STST` | Stainless Steel |
| `STWR` | Steel Wire Rod |
| `SUGR` | Sugar |
| `SULP` | Sulphur |
| `SWET` | Sweets (Candy) |
| `TATO` | Potatoes |
| `TBCO` | Tobacco |
| `TEXT` | Textile |
| `TOFF` | Toffee |
| `TOUR` | Tourists |
| `TOYS` | Toys |
| `TWOD` | Tropic Wood |
| `TYRE` | Tyres |
| `URAN` | Uranium |
| `VALU` | Valuables |
| `VBOD` | Vehicle bodies |
| `VEHI` | Vehicles |
| `VENG` | Vehicle Engines |
| `VPTS` | Vehicle Parts |
| `WATR` | Water |
| `WDPR` | Wood Products |
| `WHEA` | Wheat |
| `WOOD` | Wood |
| `WOOL` | Wool |
| `WSTE` | Waste |
| `YETI` | Workers, YETI dudes |
| `YETY` | Tired Workers, Tired YETI dudes |
| `ZINC` | Zinc |

## Na co si dát pozor

Tohle nejsou moje domněnky, tyhle dvojice stojí takhle přímo
v tabulce — jen je dávám vedle sebe, protože splést je je snadné:

- `CORE` = **Copper Ore** (měděná ruda). Ne „core".
- `PLAS` = Plastic a `PLST` = Plastic. Dva různé labely, stejné jméno.
- `SCMT` = Scrap Metal a `SCRP` = Scrap Metal. `SCRP` je zastaralý.
- `IRON` = **Pig Iron** (surové železo), kdežto `IORE` = Iron Ore (ruda).
- `OTI1` = Workers, ale `OTI2` = Tourists.
- `YETI` je zkratka nákladu (Workers) i jméno celého industry setu.
- `TATO` = Potatoes, ale `BEAN` = Beans. (V CZIS je přejmenovaný
  `BEAN` na brambory — pozor při čtení českých jmen ve hře.)
- `ALUM` = Aluminium, `AORE` = Bauxite (hliníková ruda), `METL` = Metal.
- `FRUT` = Fruit a `FRVG` = Fruit (and optionally Vegetables).
- `OILI` = Oil (imported), `OILD` = Oil (domestic), `OIL_` = Oil,
  `EOIL` = Edible Oil, `OLSD` = Oil seed. Pět různých „olejů".
- Labely kratší než čtyři znaky se doplňují podtržítkem:
  `OIL_`, `LYE_`, `NH3_`, `PCL_`, `O2__`.

## Poznámka ke zdroji

`NUKF` (Nuclear fuel) a `NUKW` (Nuclear waste) mají v tabulce popis
tříd slovy, ale **chybí jim číselný kód**. Ostatních 144 ho má.

## Labely, které v té tabulce nejsou

Viděné v reálném GRF (`VWT1cargo.yagl`, hráč poslal 2026-09-11), ale ve
vložené wiki tabulce svůj řádek nemají. **Co znamenají, nevím** — neopsal
jsem je odnikud, jen jsem je našel v souboru. Netipovat.

`FARM` · `LVPT` · `HOPS` · `ELEC` · `NODC` · `CCPR` · `HWAR` · `STBL` ·
`FOCA` · `PPWK` · `RBAR` · `SEAL` · `STPP` · `STTB` · `TYCO` · `WELD` ·
`PUMP` · `NWST` · `FREE`

Z toho `ELEC` a `NODC` jsou přesně ty dva, na které se odkazovala
poznámka u `ELTR` („CZIS uses its own labels") a řádek v tabulce neměly.
Takže se opravdu používají.
