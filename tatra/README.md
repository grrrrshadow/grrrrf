# Tatra 148 a 138 (rozdělaná, 29. 9.)

Hráč 29. 9.: *„my budem dělat dvě velký original size 148 a 138 a dvě malý 148 a 138. 138 vyrobíme přiložením
spritu chladiče na 148, to je jen z některých směrů, ušetříme spoustu místa MB“*, *„hans1240 berem na tekutiny.
A nádrž pak dáme pryč a dáme tam korbu na náklad, pak plachtu a kupy náklady jako u V3S“*, *„majáky pryč, žádná
vojenská, oranžový tatrovácky 148 a červený komunistická červená 138“*.

- **Model:** Tatra-148-AKT-3-3 od hans1240 (https://sketchfab.com/3d-models/tatra-148-akt-3-3-fd33c6c21dd54539b1fa449be41300ec),
  CC BY 4.0, release `par6` (`zip6/bar/tatra-148-akt-3-3.glb`), zkopírovat do `model/` (v gitu není). Cisterna
  (díly `AC`) na tekutiny, 9,25 m. Model nemá barvy ani textury, barvy dává `render_t148.py` podle jmen materiálů.
  Pneumatiky jsou `wheel_rm.2`, disky `wheel_rm.1`. Modré majáky (`kabina.15`) jsou schované, střešní světla nesvítí.
- **Nátěr:** 148 tatrovácká oranžová, 138 komunistická červená (`NATERY`).
- **Mřížka chladiče:** model má na masce jen hladkou plochu. Namodelovat mřížku 148 i 138; 138 podle hráčova
  videa skutečné T 138 (velký zaoblený otvor, nahoře širší, svislá zahnutá žebra do vějíře, nad ním červené TATRA).
- **Fotky:** `python3 render_t148.py <oranzova|cervena> <px_na_m> <výstup>`, kamera a HDRI jako vejtřaska.
- **Korba místo cisterny** (hráč: *„cisterna je fakt pro hasiče, tam z cisterny nahoře kouká takovej hrb. Jak bysme
  udělali korbu na náklad?“*, *„můžem vzít korbu z jiného auta“*): `KORBA=valnik` nebo `KORBA=sklapec` schová cisternu
  (díly `AC_` kromě blatníků `AC_kabina.3`, příčníku a tažného zařízení) a postaví korbu z kvádrů na rám: podlaha
  z = 0,32 m, y −5,00 až 1,05 m, x ±1,24 m. Valník má bočnice 0,55 m (náklady na něm jsou vidět jako u vejtřasky),
  sklápěč S1 ocelové bočnice 1,0 m se žebry a štítek nad kabinou. Hráč chce spíš přebarvování hrou (jeden obrázek
  pro 148 i 138).
- **Sklápěč S1 od hans1240** (`model/tatra-148.glb`, hráč ho poslal 29. 9.: *„co vozíme kupy a pytle, by šlo asi na
  tuhle“*): 7,54 m dlouhý, v centimetrech, kabina na −Y jako vejtřaska (bez +180). Náhled dělá
  `python3 render_sklapec.py <oranzova|cervena> <px_na_m> <rám_px> <výstup>`: nabarví po dílech (kabina, korba
  a disky lak, `RamTk` černý, `TG_POLOOSA` a `TG_T148` tmavé, `Pneu*` pneumatiky), kabinu (jeden kus i se skly)
  rozdělí na samostatné kusy a skla, zrcátka, reflektory a blinkry najde podle polohy a velikosti.
  Korba S1 změřená paprsky: podlaha z = 1,46 m (u bočnic zaoblená nahoru, vzadu od y 5,9 stoupá na 1,66),
  bočnice x ±1,13, nahoře z 2,39 až 2,61, přední čelo y 2,75, štítek nad kabinou y 1,25 až 2,5.
  `KUPA=GRVL|SAND|COAL` nasype kupu jako u vejtřasky (okraj kupy musí zůstat nad podlahou, jinak vykukuje pod
  korbou). Pytle: bočnice jsou metr vysoké, pytle by byly vidět jen shora, musely by se skládat nad bočnice.
- **Původ modelů:** oba modely od hans1240 jsou nejspíš převzaté (sklápěč z Emikova modu do Farming Simulatoru,
  cisterna AKT z GTA San Andreas), podrobně v `AUTORI-MODELU.md`, oddíl „Pozor na modely od hans1240“.
  Do GRF ani jeden bez svolení autora. Když Emik svolí, cisternu na tekutiny uděláme vlastní na jeho podvozku
  (bez hasičského hrbu).
