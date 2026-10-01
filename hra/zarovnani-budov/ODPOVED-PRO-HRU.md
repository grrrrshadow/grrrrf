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
