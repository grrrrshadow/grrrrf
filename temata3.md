# temata3.md — moje vlastní poznámky

Tenhle soubor je můj. Zakládám si ho v `grrrrshadow/grrrrf`, píšu si do něj
sám pravidla a poznámky, abych nic nezapomněl mezi sezeními. Není to
dokumentace projektu ani nic pro nikoho jiného — je to můj zápisník.

## Pravidla (zadal hráč 2026-09-11)

1. **`temata3.md` v `grrrrshadow/grrrrf` je můj soubor.** Sám si sem
   zapisuju pravidla i poznámky. Na moje téma.
2. **Celé `grrrrf` je jenom moje** (upřesněno 2026-09-11) — ne jen `main`.
   Můžu si v něm zakládat soubory i větve a pushovat přímo, nepotřebuju
   k tomu zvláštní větev ani se doptávat.
3. **Do ostatních repozitářů nelezu sám od sebe.** Číst je smím, ale až
   když mě tam hráč pošle. Ne že si sám vyrazím na průzkum, protože se mi
   to zrovna hodí.
4. **Export do ostatních repozitářů jen když o tom hráč ví.** Ne potichu.
5. **V ostatních repozitářích nic nepřepisovat, nemazat, needitovat.**
   Tohle platí bez výjimky.
6. **Mám sbírat informace nezbytné pro tvorbu** (zadáno 2026-09-11) —
   zdroje, které mi hráč dá, si mám otevřít a nastudovat, ne je jen
   odložit jako odkaz. Kde to nejde (viz Odkazy), musím to nahlas říct
   a domluvit náhradní cestu, ne to mlčky obejít ani předstírat,
   že jsem to četl.

## Poznámky

### 2026-09-11 — založení

- `grrrrf` bylo prázdné repo, tenhle soubor je jeho první commit.
- Pracovní repo tohohle sezení je `grrrrshadow/forclaude`, tam mám
  přidělenou větev `claude/gracious-hamilton-t0ikke` (OpenTTD build,
  spojování/rozpojování vlaků za jízdy, odtah porouchaných).
  `grrrrf` je něco jiného — to je celé moje.
- Chyba, kterou jsem hned na začátku udělal a nechci ji opakovat:
  rozjel jsem se číst `ulzvu`, `cota` a `dete`, abych zjistil, jestli
  existují starší `temata.md`/`temata2.md`. Hráč mě zastavil — tam mě
  neposlal. Pravidlo 3 vzniklo přesně z tohohle.

## Odkazy

- **NewGRF CargoTypes** — https://newgrf-specs.tt-wiki.net/wiki/CargoTypes
  (dal mi ho hráč 2026-09-11). Specifikace typů nákladu pro NewGRF —
  patří k tomu, co v `forclaude` řeší `CZTR_Wagons_cargo.yagl`.
  **Stav: nepřečteno, host je zablokovaný.** Ověřeno dvakrát —
  `WebFetch` vrátí `EGRESS_BLOCKED` a `curl` skončí na
  `CONNECT tunnel failed, response 403`. To je 403 od egress proxy,
  tedy síťová politika prostředí, ne moje nastavení.

  **Důležité, ať to znovu nepletu:** tenhle blok nejde odemknout tím,
  že mi to hráč v chatu povolí. Jeho svolení mě opravňuje ten zdroj
  použít, ale díru do sítě neudělá. Povolení domény se dělá v nastavení
  network policy toho prostředí (Claude Code on the web —
  https://code.claude.com/docs/en/claude-code-on-the-web) a projeví se
  až v novém sezení. README proxy k tomu říká jasně: 403 nezkoušet
  dokola a neobcházet, jen nahlásit zablokovaný host.

  Náhradní cesty, dokud je doména zavřená: hráč mi obsah vloží sem
  (text/soubor), nebo si stejné informace vezmu z dosažitelných zdrojů
  (GitHub jde — zdrojáky OpenTTD, NML apod.).
