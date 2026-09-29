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
