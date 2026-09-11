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

  **Vyřešeno 2026-09-11:** hráč mi tabulku vložil rovnou do chatu.
  Rozluštěná a uložená v `cargo-classes.md` — viz níž. Stránku samotnou
  jsem pořád nečetl, mám jen tu tabulku, kterou poslal.

  Ostatní náhradní cesty, kdyby bylo potřeba víc: hráč vloží další část,
  nebo si vezmu, co jde, z dosažitelných zdrojů (GitHub funguje —
  zdrojáky OpenTTD, NML apod.).

## Soubory v tomhle repu

- **`naklady.md`** — *tohle je ten hlavní.* Prostý slovník
  zkratka → náklad, všech 146, podle abecedy. `PASS` = Passengers a tak
  dál. Žádné odvozování, jen opsaná tabulka. Tohle mám umět neomylně.
- **`cargo-classes.md`** — rozbor čtyřmístných čísel (jsou to bitmasky
  tříd, ne pořadová čísla). Hráč k tomu 2026-09-11 řekl, že o tom nic neví
  a nechce, abych hledal souvislosti — takže je to jen odložená reference,
  ne něco, čím se má argumentovat. Přednost má slovník.
7. **Fakta znát nazpaměť, ne je odvozovat** (zadáno 2026-09-11). U věcí
   jako zkratky nákladu chce hráč spolehlivost, ne chytrost: `PASS` je
   Passengers, tečka. Nehledat v tom vzory a nedovozovat, co tam není —
   od toho je opsaná tabulka v `naklady.md`.

## Jak povolit zablokovanou doménu (zjištěno 2026-09-11)

Nepovoluje se to v chatu ani na GitHubu. Je to nastavení **cloud
environmentu** na claude.ai. Postup podle dokumentace
(https://code.claude.com/docs/en/cloud-environments#network-access):

1. Otevřít environment k editaci (ikona mráčku na příslušné obrazovce
   Claude Code — vlastní osobní environment nemá zvláštní stránku
   v nastavení účtu).
2. V dialogu položka **Network access**. Má čtyři úrovně:
   **None** (nic), **Trusted** (výchozí — balíčkové registry, GitHub,
   cloud SDK), **Full** (cokoliv), **Custom** (vlastní seznam).
3. Zvolit **Custom** a do pole **Allowed domains** napsat doménu,
   jednu na řádek. `*.` na začátku bere všechny subdomény.
4. Zaškrtnout **„Also include default list of common package managers“**,
   jinak se seznamem nahradí i ty výchozí povolené domény.

Projeví se to v **novém sezení** — běžící VM už svou politiku má.

Důležité k tomu: GitHub jde vlastní proxy mimo tenhle allowlist, takže
o přístup k repozitářům se tímhle přijít nedá. Allowlist je taky per
environment, žádný organizační společný neexistuje.

Pro `newgrf-specs.tt-wiki.net` tedy: **Custom** + řádek
`newgrf-specs.tt-wiki.net` (nebo rovnou `*.tt-wiki.net`) + ponechat
výchozí seznam. Kdo nechce nic řešit, dá **Full**, ale to otevře všechno.
