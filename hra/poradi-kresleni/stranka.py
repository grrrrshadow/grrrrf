# Sestavi stranku se zpravou pro kolegu: python3 sestav.py <adresar hra/poradi-kresleni> <vystup.html>
import html, sys

D, OUT = sys.argv[1], sys.argv[2]
zprava = open(f"{D}/ZPRAVA-KOLEGOVI.md", encoding="utf-8").read()
patch = open(f"{D}/oprava-poradi-kresleni.patch", encoding="utf-8").read()


def diff_html(t):
    radky = []
    for r in t.rstrip("\n").split("\n"):
        e = html.escape(r)
        if r.startswith("+++") or r.startswith("---"):
            radky.append(f'<span class="d-soubor">{e}</span>')
        elif r.startswith("@@"):
            radky.append(f'<span class="d-kus">{e}</span>')
        elif r.startswith("+"):
            radky.append(f'<span class="d-plus">{e}</span>')
        elif r.startswith("-"):
            radky.append(f'<span class="d-minus">{e}</span>')
        else:
            radky.append(e)
    return "\n".join(radky)


# Nakres shora na silnici SV-JZ: 1 jednotka (1/16 dlazdice) = 16 px, x 0..24, y 2.5..11.5
U = 16
X0, Y0 = 24, 30          # okraj vlevo, misto na popisek nahore


def px(x):
    return X0 + x * U


def py(y):
    return Y0 + (y - 2.5) * U


def panel(nadpis, box_a, box_b, dy):
    s = [f'<g transform="translate(0,{dy})">',
         f'<text class="n-nadpis" x="{X0}" y="18">{nadpis}</text>',
         f'<rect class="n-silnice" x="{px(0)}" y="{py(2.5)}" width="{24 * U}" height="{9 * U}"/>',
         f'<line class="n-kraj" x1="{px(0)}" y1="{py(3)}" x2="{px(24)}" y2="{py(3)}"/>',
         f'<line class="n-kraj" x1="{px(0)}" y1="{py(11)}" x2="{px(24)}" y2="{py(11)}"/>',
         f'<line class="n-stred" x1="{px(0)}" y1="{py(7)}" x2="{px(24)}" y2="{py(7)}"/>',
         f'<text class="n-strana" x="{px(0) - 6}" y="{py(7) + 4}" text-anchor="end">SV</text>',
         f'<text class="n-strana" x="{px(24) + 6}" y="{py(7) + 4}">JZ</text>',
         # auto A: zadni pruh (y 5), jede na JZ (doprava), celo na x 14, obrazek 7 jednotek
         f'<rect class="n-auto-a" x="{px(7)}" y="{py(3.7)}" width="{7 * U}" height="{2.6 * U}" rx="3"/>',
         f'<path class="n-sipka" d="M{px(14) + 4},{py(5)} l10,0 m-5,-4 l5,4 l-5,4"/>',
         # auto B: predni pruh (y 9), jede na SV (doleva), celo na x 8
         f'<rect class="n-auto-b" x="{px(8)}" y="{py(7.7)}" width="{7 * U}" height="{2.6 * U}" rx="3"/>',
         f'<path class="n-sipka" d="M{px(8) - 4},{py(9)} l-10,0 m5,-4 l-5,4 l5,4"/>',
         f'<rect class="n-krabice" x="{px(box_a[0])}" y="{py(4)}" width="{(box_a[1] - box_a[0]) * U}" height="{3 * U}"/>',
         f'<rect class="n-krabice" x="{px(box_b[0])}" y="{py(8)}" width="{(box_b[1] - box_b[0]) * U}" height="{3 * U}"/>',
         '</g>']
    return "\n".join(s)


W = X0 + 24 * U + 40
nakres = (f'<svg class="nakres" viewBox="0 0 {W} 400" role="img" aria-labelledby="nakres-popis">'
          f'<title id="nakres-popis">Pohled shora na silnici SV–JZ: dnes a s opravou</title>'
          + panel("Dnes: krabice 1 jednotka u čela", (13, 14), (8, 9), 0)
          + panel("S opravou: krabice 8 jednotek", (6, 14), (8, 16), 196)
          + '</svg>')

zprava_html = zprava.replace("</", "<\\/")
stranka = f'''<title>Pořadí kreslení aut</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;800&family=Overpass+Mono:wght@400;600&display=swap">
<style>
/* Layout: jeden sloupec zpravy (text na ~68 znaku, obrazky pres celou sirku sloupce), oddily deli prerusovana
   stredova cara jako na silnici. Pismo podle dopravniho znaceni (Overpass), barvy asfalt, znaceni a modra znacek. */
:root {{
  --bg: #f2f4f6;
  --surface: #ffffff;
  --fg: #16202b;
  --muted: #58636f;
  --line: #d3d9df;
  --accent: #1c5aa6;
  --asfalt: #3b4149;
  --znaceni: #f5f5f0;
  --auto-a: #d8a33c;
  --auto-b: #3f82c4;
  --krabice: #e0452f;
  --spatne: #b3261e;
  --dobre: #1d7a45;
  --kod-bg: #eef1f4;
  --plus: #1d7a45;
  --minus: #b3261e;
  --font-nadpis: "Overpass", "Segoe UI", system-ui, sans-serif;
  --font-text: "Overpass", "Segoe UI", system-ui, sans-serif;
  --font-kod: "Overpass Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #14181d; --surface: #1c2229; --fg: #e4e9ee; --muted: #9ca8b4; --line: #2e363f; --accent: #7eb0f5;
    --asfalt: #2c3239; --znaceni: #e6e6e0; --auto-a: #e2b457; --auto-b: #5d9ad6; --krabice: #ff7a62;
    --spatne: #ff8b80; --dobre: #6ed49b; --kod-bg: #20272f; --plus: #6ed49b; --minus: #ff8b80;
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #14181d; --surface: #1c2229; --fg: #e4e9ee; --muted: #9ca8b4; --line: #2e363f; --accent: #7eb0f5;
  --asfalt: #2c3239; --znaceni: #e6e6e0; --auto-a: #e2b457; --auto-b: #5d9ad6; --krabice: #ff7a62;
  --spatne: #ff8b80; --dobre: #6ed49b; --kod-bg: #20272f; --plus: #6ed49b; --minus: #ff8b80;
  color-scheme: dark;
}}
body {{ background: var(--bg); color: var(--fg); font-family: var(--font-text); font-size: 16px; line-height: 1.55; }}
.stranka {{ max-width: 1040px; margin: 0 auto; padding-inline: 20px; padding-block: 28px 64px; display: grid; gap: 28px; }}
.text {{ max-width: 68ch; min-width: 0; }}
header {{ display: grid; gap: 12px; }}
.stitek {{ font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 600; }}
h1 {{ font-family: var(--font-nadpis); font-weight: 800; font-size: clamp(30px, 6vw, 44px); line-height: 1.08; margin: 0; text-wrap: balance; }}
h2 {{ font-family: var(--font-nadpis); font-weight: 800; font-size: 23px; line-height: 1.2; margin: 0 0 10px; text-wrap: balance; }}
p {{ margin: 0 0 10px; }}
ul, ol {{ margin: 0 0 10px; padding-left: 22px; }}
li {{ margin-bottom: 4px; }}
code {{ font-family: var(--font-kod); font-size: .88em; background: var(--kod-bg); padding: 1px 5px; border-radius: 4px; overflow-wrap: anywhere; }}
.meta {{ color: var(--muted); font-size: 14px; }}
.shrnuti {{ font-size: 18px; }}
.tlacitka {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
button {{ font: 600 15px var(--font-text); color: var(--surface); background: var(--accent); border: 0; border-radius: 6px; padding: 10px 16px; cursor: pointer; }}
button.vedlejsi {{ color: var(--accent); background: transparent; border: 1.5px solid var(--accent); }}
button:focus-visible {{ outline: 3px solid var(--auto-a); outline-offset: 2px; }}
.hlaseni {{ font-size: 14px; color: var(--dobre); min-height: 1.2em; }}
section {{ display: grid; gap: 12px; }}
.cara {{ height: 0; border-top: 3px dashed var(--line); }}
.dvojice {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
figure {{ margin: 0; display: grid; gap: 6px; min-width: 0; }}
figure img {{ width: 100%; height: auto; border-radius: 6px; border: 1px solid var(--line); }}
figcaption {{ font-size: 14px; color: var(--muted); }}
.nakres {{ width: 100%; max-width: 480px; height: auto; }}
.n-nadpis {{ fill: var(--fg); font: 700 14px var(--font-nadpis); }}
.n-silnice {{ fill: var(--asfalt); }}
.n-kraj {{ stroke: var(--znaceni); stroke-width: 2; }}
.n-stred {{ stroke: var(--znaceni); stroke-width: 2; stroke-dasharray: 14 10; }}
.n-strana {{ fill: var(--muted); font: 600 12px var(--font-text); }}
.n-auto-a {{ fill: var(--auto-a); }}
.n-auto-b {{ fill: var(--auto-b); }}
.n-sipka {{ fill: none; stroke: var(--znaceni); stroke-width: 2; }}
.n-krabice {{ fill: none; stroke: var(--krabice); stroke-width: 2.5; stroke-dasharray: 5 3; }}
.legenda {{ display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 14px; color: var(--muted); }}
.legenda span::before {{ content: ""; display: inline-block; width: 14px; height: 10px; margin-right: 6px; vertical-align: -1px; }}
.l-a::before {{ background: var(--auto-a); }}
.l-b::before {{ background: var(--auto-b); }}
.l-k::before {{ border: 2px dashed var(--krabice); }}
.stav {{ display: inline-block; font-size: 13px; font-weight: 600; padding: 1px 8px; border-radius: 999px; border: 1.5px solid currentColor; }}
.stav.spatne {{ color: var(--spatne); }}
.stav.dobre {{ color: var(--dobre); }}
.kod {{ background: var(--kod-bg); border-radius: 6px; overflow-x: auto; min-width: 0; }}
.kod pre {{ margin: 0; padding: 14px 16px; font: 13px/1.5 var(--font-kod); }}
.d-soubor {{ color: var(--muted); font-weight: 600; }}
.d-kus {{ color: var(--accent); }}
.d-plus {{ color: var(--plus); }}
.d-minus {{ color: var(--minus); }}
@media (prefers-reduced-motion: no-preference) {{ button {{ transition: filter .15s; }} button:hover {{ filter: brightness(1.08); }} }}
</style>
<div class="stranka">
<header>
  <div class="stitek">Pro kolegu ze hry · od session GRF a spritů · 29. 9. 2026</div>
  <h1>Pořadí kreslení aut na silnici SV–JZ</h1>
  <p class="shrnuti text">Na silnici SV–JZ se auto jedoucí na jihozápad v zadním pruhu kreslí přes auto v předním pruhu.
  Příčina je v krabici, podle které hra řadí kreslení. Díl auta ji má jen tak dlouhou, jak je díl dlouhý, a dvanácttrojky
  a VW T1 mají díly dlouhé 1. Oprava je v <code>RoadVehicle::UpdateDeltaXY()</code>: krabice jako celé auto.</p>
  <p class="meta">Čteno z větve <code>claude/github-connection-check-m6m898</code> (9d23ceb), ve forclaude nic neměněno.
  Patch a obrázky jsou v <code>grrrrshadow/grrrrf</code>, složka <code>hra/poradi-kresleni/</code>.</p>
  <div class="tlacitka">
    <button id="kopiruj-zpravu" type="button">Zkopírovat zprávu pro kolegu</button>
    <button id="kopiruj-patch" type="button" class="vedlejsi">Zkopírovat patch</button>
    <span id="hlaseni" class="hlaseni" role="status" aria-live="polite"></span>
  </div>
</header>

<div class="cara" aria-hidden="true"></div>

<section>
  <div class="text">
    <h2>Co hráč vidí</h2>
    <p>Na obou fotkách jede auto nahoře v zadním pruhu na jihozápad a kreslí se přes auto v předním pruhu. Dvanácttrojka
    jede ve svém pruhu daleko od středu, takže zarovnáním spritů to není. Na silnici SZ–JV se to neděje.</p>
  </div>
  <div class="dvojice">
    <figure><img src="hrac_snimek3_1203.png" alt="TAZ 1500 se zahrádkou v zadním pruhu nakreslený přes oranžovou Tatru 148 v předním pruhu" width="1000" height="540">
      <figcaption>Hráčova fotka 3: TAZ 1500 (VW T1 GRF) přes Tatru 148.</figcaption></figure>
    <figure><img src="hrac_snimek2_tatra.png" alt="Červená Tatra 138 v zadním pruhu nakreslená přes valník TAZ 1203 v předním pruhu" width="760" height="480">
      <figcaption>Hráčova fotka 2: Tatra 138 (délka 8) přes TAZ 1203 valník.</figcaption></figure>
  </div>
</section>

<div class="cara" aria-hidden="true"></div>

<section>
  <div class="text">
    <h2>Proč</h2>
    <p><code>RoadVehicle::UpdateDeltaXY()</code> dělá třídicí krabici dílu dlouhou jako díl
    (<code>gcache.cached_veh_length</code>) a posadí ji k jeho čelu. Poslední GRF VW T1
    (<code>VWT1-S1203-clanky-oba-na-stred.grf</code>) staví každé auto z nárazníku, auta a nárazníku, všechny díly délky 1,
    a celé auto kreslí na ten prostřední. Obrázek má asi 7 jednotek (1 jednotka je 1/16 dlaždice), krabice 1. Ve výpisu
    ze zkoušky má dvanácttrojka <code>0x00B3</code> krabici x 1085..1085 a Tatra vedle ní 1073..1080.</p>
    <p>Když se dvě auta míjejí na silnici podél osy X, zadní (na jihozápad) je dál po ose x a přední (na severovýchod)
    dál po ose y. Každé je „za“ tím druhým v jiné ose, <code>ViewportSortParentSprites</code> pro ně nemá pravidlo a nechá
    je v pořadí, v jakém je hra přidala. Jihozápadní vyjde nahoře. Na silnici podél osy Y je zadní auto za předním
    v obou osách, proto tam chyba není.</p>
    <p>Rola to není. Zvednutí krabice na vagonu platí jen pro auto na vagonu a řazení je stejné jako ve vanilce.</p>
  </div>
  <figure>
    {nakres}
    <div class="legenda"><span class="l-a">auto v zadním pruhu, jede na JZ</span><span class="l-b">auto v předním pruhu, jede na SV</span><span class="l-k">krabice pro řazení</span></div>
    <figcaption>Pohled shora, v měřítku 1 jednotka = 16 bodů. Dnes se krabice v ose x nepřekrývají a o pořadí rozhodne náhoda.
    S opravou se překrývají a rozhodne pruh.</figcaption>
  </figure>
</section>

<div class="cara" aria-hidden="true"></div>

<section>
  <div class="text">
    <h2>Ověřeno ve zkušební hře</h2>
    <p>Zkušební kopie hry (60283b3) má řazení i <code>UpdateDeltaXY()</code> stejné jako tvoje větev, jen bez zvednutí na vagonu.
    Scéna <code>testpruhy</code> postaví stojící auta proti sobě: tři silnice po osmi dvojicích, čela od sebe 0 až 14/16
    dlaždice (celé míjení), a k tomu zácpu v obou pruzích. Čísla odpovídají panelům na obrázku:</p>
    <ol>
      <li><span class="stav spatne">dnes</span> Na SV–JZ je ve všech míjeních 2–8/16 nahoře zadní pruh.</li>
      <li><span class="stav dobre">s opravou</span> Nahoře je vždy přední pruh.</li>
      <li>Na SZ–JV je to dnes i s opravou správně a stejné.</li>
      <li>a 5. Zácpa v obou pruzích na SV–JZ: dnes leze zadní pruh přes přední, s opravou ne.</li>
    </ol>
  </div>
  <figure><img src="pred_po.png" alt="Dvojice aut proti sobě na silnici SV–JZ před opravou a po ní, silnice SZ–JV a zácpa v obou pruzích" width="1040" height="2708">
    <figcaption>Fotky ze zkušební hry při plném přiblížení, výřezy dvojic zvětšené.</figcaption></figure>
</section>

<div class="cara" aria-hidden="true"></div>

<section class="text">
  <h2>Oprava 1: krabice jako celé auto</h2>
  <p>Každý díl třídit krabicí celého auta (<code>VEHICLE_LENGTH</code>), ať je díl dlouhý jakkoli.</p>
  <ul>
    <li>Obrázek se nehne. Origin + offset vychází pro každou délku stejně (−2), mění se jen krabice.</li>
    <li>Rolu to neovlivní. <code>road_on_rail.cpp</code> krabici nečte, bere <code>ROAD_VEHICLE_NOSE</code> a délky dílů,
    a zvednutí na vagonu zůstává.</li>
    <li>Kolony drží. Díly jedné soupravy se překrývají jako u auta délky 8 a vepředu je ten blíž k divákovi.</li>
  </ul>
</section>

<section class="text">
  <h2>Oprava 2: posun obrázku z vagonu se nevynuluje</h2>
  <p><code>Vehicle::draw_offs</code> nastavuje <code>road_on_rail.cpp</code> autu na vagonu každý tik. Když auto vystoupí
  (<code>TryLeaveTrain</code>, <code>TryLeaveVessel</code> → <code>PlaceRoadVehicleAtStopEntrance</code>), nikdo ho
  nevynuluje a auto jezdí dál s posunutým obrázkem.</p>
  <ul>
    <li>Při výchozí palubě a boku je posun nula. Po <code>testpaluba</code> nebo <code>testbok</code> ale autu, které se vezlo,
    zůstane, dokud znovu nenastoupí.</li>
    <li>Na silnici se auto jinudy nevrací, ostatní místa ho mažou. Stačí vynulovat v
    <code>PlaceRoadVehicleAtStopEntrance</code> u čela i u přívěsů.</li>
    <li>Na hráčových fotkách to není, ty spraví oprava 1.</li>
  </ul>
</section>

<div class="cara" aria-hidden="true"></div>

<section>
  <div class="text">
    <h2>Patch</h2>
    <p>Obě opravy, jen <code>roadveh_cmd.cpp</code>, proti tvé větvi na 9d23ceb (<code>patch -p1</code> v kořeni repa).
    Tvou větev jsem s ním celou přeložil bez chyby a hra odjela 500 tiků nové hry. Pusť prosím svou baterii (<code>tests/rig</code>). Já jsem zkoušel jen rovnou silnici a zácpu, ne zastávky, mosty a Rolu.</p>
  </div>
  <div class="kod"><pre><code id="patch">{diff_html(patch)}</code></pre></div>
</section>
</div>
<script type="text/plain" id="zprava">{zprava_html}</script>
<script>
(function () {{
  var hlaseni = document.getElementById("hlaseni");
  function kopiruj(text, co) {{
    function vyber() {{
      var t = document.createElement("textarea");
      t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      var ok = false;
      try {{ ok = document.execCommand("copy"); }} catch (e) {{ ok = false; }}
      document.body.removeChild(t);
      hlaseni.textContent = ok ? co + " zkopírováno" : "Kopírování nešlo, vyber text ručně";
    }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).then(function () {{ hlaseni.textContent = co + " zkopírováno"; }}, vyber);
    }} else {{ vyber(); }}
  }}
  document.getElementById("kopiruj-zpravu").addEventListener("click", function () {{
    kopiruj(document.getElementById("zprava").textContent.replace(/<\\\\\\//g, "</"), "Zpráva");
  }});
  document.getElementById("kopiruj-patch").addEventListener("click", function () {{
    kopiruj(document.getElementById("patch").textContent, "Patch");
  }});
}})();
</script>
'''
open(OUT, "w", encoding="utf-8").write(stranka)
print(len(stranka))
