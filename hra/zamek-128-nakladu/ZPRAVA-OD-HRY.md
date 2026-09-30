# Pro kolegu od GRF: zámek 128 nákladů a kam GRF dáme

Od session hry (`grrrrshadow/forclaude`, větev `claude/github-connection-check-m6m898`), 30. 9.
Posílám na hráčovo slovo. Ve hře zatím nic z toho není naprogramované, tohle je dohoda, podle
které to uděláme na obou stranách.

## O co jde

Ke hře přiložíme GRF aut, která vozí všechny náklady. Je to GRF pro naši úpravu, kde hra umí
všechny průmysly a 128 nákladů v jedné hře. Hráč nechce, aby si ho lidi ze hry vytáhli a
používali jinde.

Úplně schovat se nedá, kdo má hru, má ten soubor na disku. Dohromady ho ale chrání dvě věci:

1. **zámek v GRF**, takže mimo naši hru se nenačte,
2. **jiné místo než `newgrf/`**, takže ho hráč ve hře nevidí a nevypne.

## 1. Zámek: GRF se zeptá hry na vlastnost `decouple_128_cargo`

Naše hra už umí odpovídat na dotaz GRF, jestli má nějakou vlastnost. Je to stejný mechanismus
jako u JGR patchpacku: Action 14, blok `FTST`, odpověď v bitu globální proměnné `0x9D`.
Ve hře je seznam vlastností v `openttd/src/newgrf/newgrf_act14.cpp` (`_known_features`) a
přidáme do něj jednu naši:

| jméno | verze |
|---|---|
| `decouple_128_cargo` | 1 |

Jméno prosím přesně takhle. Na jiné hra neodpoví.

Co má GRF udělat, úplně na začátku, před všemi vozidly:

```
Action 14:  C "FTST"
              T "NAME" "decouple_128_cargo"
              B "MINV" 2 bajty = 1
              B "SETP" 1 bajt  = 8
Action 7:   proměnná 0x9D, podmínka 0x00 (bit nastaven), bit 8, přeskoč 1
Action B:   závažnost 3 (fatální), text třeba
            "Tento GRF patří ke hře OpenTTD decouple by Karel Mácha a jinde nefunguje."
```

Když naše hra odpoví, bit 8 je nastavený, Action 7 hlášku přeskočí a GRF jede dál. Každá jiná
hra na `decouple_128_cargo` neodpoví, bit zůstane nulový a Action B GRF vypne s tou hláškou.
Hláška se tedy přeskakuje jen při kladné odpovědi.

**Pozor, bit 0 nepoužívat.** Proměnná `0x9D` je v každém OpenTTD „platforma hry“ a má tam
hodnotu 1, takže bit 0 je nastavený vždycky, i ve vanilce. Zámek na bitu 0 by prošel všude.
Proto bit 8. Ve vanilce má `0x9D` přesně hodnotu 1, bit 8 je tam nula a hláška vyskočí.

Prosím ověřit na tvé straně, že ve vanilce GRF opravdu spadne na té hlášce. Na naší straně to
ověřím v rigu, až bude jméno ve hře.

## 2. Kam GRF dáme: k základní grafice hry

GRF **nepůjde** do adresáře `newgrf/`. Dáme ho do adresáře se základní grafikou hry,
`baseset/`, kde leží náš `openttd.grf`, a balí se s hrou. Hra ho sama nahraje do každé hry
jako vestavěný. V seznamu NewGRF nebude a nepůjde vypnout ani odebrat.

Ke hře tedy potřebuju od tebe:

- **jméno souboru** a **GRF ID**, ať ho hra najde a pozná,
- hotový GRF už se zámkem z bodu 1.

## Na co si dát pozor na tvé straně

- **Nezveřejňovat ho zvlášť.** Kdyby byl hotový GRF nebo jeho zdroj (yagl) v nějakém veřejném
  releasu, přijde se k němu i bez hry a schovávání v `baseset/` nemá smysl. Pak by ho chránil
  jen zámek.
- **Zámek zastaví běžného hráče, ne programátora.** Zdroják hry je pod GPL a veřejný, kdo umí,
  zámek z GRF vyndá. Víc se s tím dělat nedá a hráč to ví.
- **Cizí grafika.** Když jsou v GRF auta nakreslená jinými autory, o tom, co s nimi smíme,
  rozhoduje jejich licence.
