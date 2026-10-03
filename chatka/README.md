# Chatka (2 políčka)

Hráč 3. 10.: *„okolo domku lavičky velké jak u sochy, nepořádek, nízké smrčky marihuany místo plotu, sem tam díra.
přikládací holky stojící a pak přikádací holky sedící. takže bude obrázek bez holek a dva s holkama přiloženejma. chci
tam hlavně tu holku co stojí u kufru dvanácetrojky bus“*, *„velikost 1 políčko. to sem zvědavej jak se to vejde. muže
to být přes dvě políčka nebo přes čtyři políčka, to je jedno. ale holky přikládací ať ušetříme Mb“*.

- **Domek:** „A little happy hut“ od Tigrana Safaryana (Sketchfab, CC BY 4.0,
  https://sketchfab.com/3d-models/a-little-happy-hut-045afe84e4c04400a34f0babab201378 ), poslal ho hráč 3. 10.
  V gitu není (11 MB), patří do `model/a_little_happy_hut.glb` (md5 `d6cc13aa08652713f703ff08ad84a517`). Domek se
  nemění, jen se zvětší a otočí: dveře na dvorek, schody na balkon k divákovi.
- **Proč 2 políčka:** holky jsou jako u sochy a u kufru 1203 dvakrát větší (College Girl má 3,24 m). Aby holka prošla
  dveřmi, mají dveře 3,35 m. Domek pak má 14,7 × 14,6 m a 16,6 m na výšku, tedy sám zabere celé jedno políčko.
  Lavičky a nepořádek jsou na druhém políčku (vpředu vlevo), to je dvorek. Kdyby bylo všechno na jednom políčku,
  musel by být domek menší a holky by byly větší než dveře.
- **Dvorek:** ušlapaná hlína, dvě lavičky jako u sochy (dvakrát větší), nepořádek: dvě bedny na sobě, převrhlá
  bedna, hromada prken, dvě pneumatiky, kyblík a asi sto odpadků (papíry, plechovky, lahve, kelímky, sáčky, zelené
  balíčky).
- **Plot:** 31 nízkých rostlin marihuany místo plotu (Cannabis Sativa plant a Cannabis Plant jako u sochy, skutečně
  1 až 1,3 m, na obrázku dvakrát větší) podél přední pravé hrany celého pozemku a kolem dvorku. Sem tam je díra,
  vlevo široká jako branka k dveřím.
- **Světlo jako u sochy:** měkké, stín na trávu 20 %.

## Obrázky

| soubor | co to je |
|---|---|
| `chatka_zin4.png` | chatka bez holek, 400 × 360 px, 32 bpp s průhledností, přiblížení 4× |
| `chatka_stojici_zin4.png` | přikládací vrstva se stojícími holkami, stejně velká, jinde průhledná |
| `chatka_sedici_zin4.png` | přikládací vrstva se sedícími holkami |
| `chatka_zin8.png`, `chatka_stojici_zin8.png`, `chatka_sedici_zin8.png` | totéž v 8× (jen naše hra, `zin8`), 800 × 720 px, přesně dvojnásobek 4× |
| `*.json` | rohy pozemku na obrázku (`rohy`), počet políček (`policek`: 2 podél x, 1 podél y), u vrstev i `holky_obdelnik` |
| `nahled_ve_hre.png` | chatka se stojícími holkami ve fotce ze zkušební hry (políčka 45–46 × 16) |
| `animace_ve_hre.gif` | totéž, střídá se bez holek, stojící a sedící |

- **Rohy pozemku ve 4×:** sever (264, 160), východ (392, 224), západ (8, 288), jih (136, 352). V 8× je všechno
  dvakrát: (528, 320), (784, 448), (16, 576), (272, 704).
- Pozemek jsou 2 políčka podél x (k jihozápadu) a 1 podél y. Zadní políčko (u severního rohu) je domek, přední
  (u západního rohu) dvorek.
- Render 2 : 1, políčko 256 × 128 px (ve 4×), severní roh na celém pixelu dělitelném 4, jako gymnázium a pole.

## Holky (přikládací vrstvy)

- **Stojící:** holka od kufru 1203 busu (College Girl, ruce podél těla) stojí na dvorku před dveřmi, holka
  v tyrkysovém tílku s kabelkou (Character Girl) jde od branky k domku.
- **Sedící:** College Girl a holka v tyrkysovém tílku na lavičce u domku, bělovlasá Galaxia na druhé lavičce.
- **Ať se ušetří MB:** obrázek s domkem je jen jeden, holky jsou zvlášť. Vrstva má stejnou velikost a rohy jako
  obrázek bez holek a všude, kde holky nejsou, je průhledná (PNG má 4 až 15 kB). Co holky zakrývá domek, lavička nebo
  rostlina, je z vrstvy vyříznuté, takže se vrstva jen položí navrch obrázku s domkem.
- Holky nemají stín: ten by musel být v obrázku s domkem, kde holky nejsou.
- `holky_obdelnik` v JSONu říká, kde ve vrstvě holky jsou (vlevo, nahoře, vpravo, dole), kdyby hra chtěla vrstvu
  oříznout. Ve 4×: stojící [108, 226, 172, 300], sedící [68, 235, 219, 281].

## Kontrola

- 8× má rohy přesně dvakrát 4× a zmenšené na půl odpovídá 4× (barva se liší v průměru o 2 z 255, je to šum renderu).
- **Nic nepřečuhuje:** vrstvy s holkami nemají mimo pozemek ani jeden pixel. Obrázek s domkem má mimo pozemek jen okraj
  stínu s alfou nejvýš 9 z 255 (neviditelné). Domek, rostliny a holky jsou celé uvnitř a lezou jen nahoru.
- Ve vrstvách nejsou černé obrysy listů: listy rostlin mají průhlednou texturu a v zakrývání nechávaly slabý černý lem,
  proto se vrstva ořízne ještě druhým snímkem se samotnými holkami.

## Jak to složit

1. Model do `model/a_little_happy_hut.glb` (ze Sketchfabu, odkaz výš).
2. `python3 render_chatka.py <adresář>` (4×, asi minuta) a `ZIN=8 python3 render_chatka.py <adresář>` (8×, asi dvě
   minuty). `SAMPLES=32` na zkoušku, `NAHLED=1` rychlý náhled bez Cycles.
3. Náhled ve hře: `python3 ../hra/nahled_ve_hre.py <výstup.png> chatka_zin4.png@45,16` (s holkami nejdřív položit
   vrstvu na obrázek s domkem a vedle dát kopii JSONu).
