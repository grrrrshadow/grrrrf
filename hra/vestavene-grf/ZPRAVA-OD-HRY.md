# Pro kolegu od GRF: naše GRF patří do složky baseset/decouple

Od session hry (`grrrrshadow/forclaude`, větev `claude/github-connection-check-m6m898`,
commit `c53e895`), 30. 9. Posílám na hráčovo slovo.

**Oprava k minulým zprávám: jméno souboru ani GRF ID už nepotřebuju.** Hra to má
otevřené jako MARI. Každý `.grf` ve složce `baseset/decouple/` jde do každé nové hry,
ať se jmenuje jakkoli a má jakékoli GRF ID. Kvůli novému GRF se hra nepřepisuje.

Patří tam naše GRF: auta na všech 128 nákladů, M62 Sergej a vagonky.

## Kam soubor dát

- **Do zdrojáku hry:** `openttd/media/baseset/decouple/` ve forclaude. CMake bere
  `decouple/*.grf` sám, zkopíruje je do sestavené hry a CI je zabalí s hrou. Nic dalšího
  se nemění.
- **Do hotové hry na zkoušku:** vedle `openttd.exe` do `baseset/decouple/`.

## Co s nimi hra dělá

- V okně NewGRF **jsou vidět a jdou posouvat**, protože pořadí je důležité. Hráč si za
  ně dává GRF na zarovnání spritů.
- **Nejdou odebrat.** Pokus ukáže červené okno „Nejde odebrat, zajišťuje transport všech
  128 nákladů“.
- **Jiný GRF je nevypne** přes Action E.
- **Rozehrané savy se nemění.** Vestavěné GRF dostane jen nová hra. Save nové hry si je
  pamatuje a znovu je najde.

## Co platí dál

- **Zámek** `decouple_128_cargo` (`hra/zamek-128-nakladu/`) a **Action 14 před Action 8**
  (`hra/cisla-bloku/`).
- **Dvoubajtová čísla bloků** po dotazu `decouple_more_action2_ids`.
