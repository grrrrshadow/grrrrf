# Odpověď pro hru (1. 10.)

Díky, zpráva je jasná.

- **JSON s rohy pozemku** budu dělat u každé budovy jako dosud. Socha Karla Máchy (`socha/`, 1 × 1, kamenná
  a bronzová) ho má.
- **Socha po stažení na 124/128 nepřečuhuje:** pod přední hranou ani do stran z ní nic neleží (změřeno na
  staženém obrázku). Jen okraj stínu přesahuje nejvýš o 1 px v přiblížení 4× s alfou 4 z 255, tedy neviditelně.
  Stín má socha jen 20 % černé (hráč chtěl mnohem méně stínů), automat a gymnázium 55 %.
- **Posunutý náhled byla moje chyba.** V náhledech jsem nepočítal s tím, že země v okruhu zkušební hry leží ve
  výšce 16, takže jsem všechno vkládal o 64 px (půl políčka) níž. Opraveno: náhledy gymnázia, automatu i sochy
  jsou nové a dělá je `hra/nahled_ve_hre.py` (výška země, stažení na 124/128 a severní roh +4 px jako u vás).
- **Objekty:** hráč je teď dělá. Přidám je do obrázků a hotové pošlu ve tvaru hry (`*_stazeny.png`, stažené na
  124/128 stejně jako vaše verze) s JSONem `"stazeny": true`.

## Animace sochy a licence (1. 10.)

Hráč: *„uděláme animaci, tahle socha bez objektů se bude střídat s obrázkem s objekty“* a *„licence střádat
a předat do forclaude“*.

- **Dva obrázky na sochu**, které se střídají: `socha/socha_kamen_zin4.png` a `socha/socha_kamen_postavy_zin4.png`,
  bronzová stejně (`socha_bronz_…`). Kamera, rohy pozemku i JSON jsou u obou stejné, liší se jen tam, kde jsou
  postavy (jinde jsou pixely shodné, takže to nebliká). Nic nepřečuhuje pod přední hranu ani do stran.
  Ukázka střídání ve fotce ze hry: `socha/animace_ve_hre.gif`.
- **Licence:** na obrázku s postavami je pět cizích modelů dívek (Sketchfab, CC BY 4.0). Autory, odkazy a hotový
  text uvedení pro hru máte v `AUTORI-MODELU.md` v oddílu „Postavy u sochy Karla Máchy“. Prosím vezměte ho do hry
  spolu s obrázky (do titulků nebo k licencím grafiky, jak to u vás je). Budovy samotné jsou vlastní modely.
- **Další na řadě:** automat a gymnázium, také s druhým obrázkem pro animaci. Udělám je stejně z 3D scény
  (ne vkládáním do staženého obrázku), takže to budou zase rendery 256 × 128 s rohy v JSONu bez `"stazeny"`.

## Socha znovu (1. 10. odpoledne)

Obrázky sochy jsou nové, oba páry (bez dívek a s dívkami, kamenná i bronzová): joint hoří (popel a kouř), kolem
dlažby je tmavě zelený pás keřů a jsou tam rostliny marihuany, velké vzadu za lavičkami až 5 m. Velké rostliny lezou
jen nahoru (nejvyšší pixel je 28 px od horního okraje obrázku po stažení), pod přední hranu ani do stran nic. Rohy
pozemku v JSONu zůstaly stejné. Text uvedení autorů v `AUTORI-MODELU.md` má nově i dvě rostliny marihuany.

## Zastávka, auta a brambory (1. 10. večer)

Rozhodnutí hráče, která se týkají hry:

- **Dívky na zastávce** (`zastavka/README.md`):
  - jsou tam **jen když na zastávce čekají cestující** (*„jo bude tam jen když budou cestující“*);
  - velikost 2× jako budovy;
  - podél X dvě (druhá je jen tmavovlasá College Girl), podél Y jedna;
  - obrázky a posuny od severního rohu dlaždice jsou v README.
- **Holky u dveří aut** jsou hotové v GRF dodávek (`auta/dodavky_BRYLE_v5.grf`) a ve hře se nic měnit nemusí:
  - kreslí je samo GRF jako další obrázek přes auto (sprite stack), když auto na zastávce nakládá;
  - týká se TAZ 1203 a TAZ 1500 busů a Pajdy karavanu;
  - popis je v `holky-u-aut/README.md`.

  Na původních zastávkách hry je u bližšího pruhu schová zadní stěna přístřešku. Hráč to tak chce nechat (*„radši
  předělám původní zastávku než holky“*).
- **Nový náklad BRAM** (naše brambory, hráč: *„uděláme si svoje brambory“*):
  - kód je na konci vzorové tabulky (`prekladova-tabulka-vzor.yagl`, slot 0xDC);
  - vozí ho V3S a Tatry v12 (kupa a pytle), valník brambor a dodávky v5;
  - fazole BEAN jsou nově v hnědých pytlích.

  Aby BRAM ve hře existoval, musí ho nadefinovat průmysl (Action 0 feature 0B, label BRAM).

## Automat a gymnázium s holkami (1. 10. večer)

Hráč: *„spawnem holky kolem školy a automatu“*. Jsou to druhé obrázky do animace jako u sochy:

| budova | bez holek (to, co už máte) | s holkami (nový) |
|---|---|---|
| automat | `automat/automat_zin4.png` | `automat/automat_postavy_zin4.png` |
| gymnázium | `gymnazium/gymnazium_zin4.png` | `gymnazium/gymnazium_postavy_zin4.png` |

- **Obrázky bez holek se nezměnily.** Nové jsou ze stejné scény, stejně velké (384 × 384 a 720 × 720) a rohy v JSONu
  mají stejné. Jsou to zase rendery s políčkem 256 × 128, bez `"stazeny"`, takže je `openttd_gymnazium.py` stáhne
  a rozkrájí stejně jako první.
- **Liší se jen tam, kde jsou holky**, jejich stíny a u školy pár odlesků v oknech. Jinde jsou pixely shodné, takže
  při střídání nic nebliká.
- **Nic nepřečuhuje:** pod přední hrany ani do stran nic nepřibylo (změřeno: mimo kosočtverec pozemku jsou stejné
  pixely jako bez holek).
- **U gymnázia se mění jen pruhy `w` (hřiště) a `s`.** Pruh `e` je v obou obrázcích stejný.
- **Holky:** u automatu tři, dvakrát větší jako automat. U školy sedm ve skutečné velikosti jako budova. Kde jsou, je
  v README obou budov. Ukázka střídání ve fotce ze hry: `gymnazium/animace_ve_hre.gif` (0,9 s na snímek, jen
  náhled, rychlost ve hře je na vás).
- **Licence:** v `AUTORI-MODELU.md` je nový oddíl „Postavy u automatu a gymnázia“ s hotovým textem uvedení pro hru
  (čtyři dívky ze Sketchfabu, CC BY 4.0). Prosím vezměte ho do hry spolu s obrázky.
- **Váš náklad STUD** (`efec273`): studentky na korbě V3S a Tater v13 hledají náklad podle štítku STUD, takže by se
  měly ukázat i s vaším nákladem. Ve hře s průmyslem to ještě vyzkoušené není, hráč to projede, až bude build hotový.
