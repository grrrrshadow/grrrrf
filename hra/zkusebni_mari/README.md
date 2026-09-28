# Zkušební náklad MARI

Jen pro moji zkušební hru (`hra/`), hráčovi se nedává. Ve hře, kterou hráč hraje, je marihuana
zabudovaná (`CT_MARIJUANA`, hráč 28. 9.: *„MARI je ve hře zabudovaný“*). Moje zkušební hra je
starší verze (`forclaude` `60283b3` z 16. 9.) a MARI v ní ještě není, tak ho přidává tenhle GRF.

- `grf_id` `MAXm`, náklad do volného místa 0x14, štítek `MARI`, třída hromadný (0x0010),
  ikona hry 0x10CF.
- Zkouška zelené kupky V3S: ve zkušební hře se V3S dá přestavět na MARI (tahle stará verze ho
  vozidlům neškrtá) a `testv3s` ji naloží a vypíše obrázek naložené.

Ověřeno 28. 9.: přestavba na MARI projde, kapacita 5 (násobek jako uhlí), naložená vojenská i modrá
mají jiný obrázek než prázdná (kupka), v obou velikostech.

Postup: `yagl -e zkusebni_MARI.grf` v tomhle adresáři (yagl čte `sprites/zkusebni_MARI.yagl`).
