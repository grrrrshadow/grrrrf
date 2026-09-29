# Zkušební náklady pro vejtřasku

Jen pro moji zkušební hru (`hra/`), hráčovi se nedává. Mírné klima zkušební hry nemá písek, brambory,
cement, kámen ani turisty, tak je přidává tenhle GRF, aby šla vyzkoušet vejtřaska verze 4:

- brambory (TATO) mají stejnou žlutou kupku jako písek (SAND), cement (CMNT) stejnou šedou jako
  kámen (GRVL);
- turisté (TOUR) jsou lidé: vojenská jich veze 20 pod plachtou, modrá 3 v kabině.

`grf_id` `MAXn`, náklady ve volných místech 0x15 až 0x2A: SAND TATO CMNT GRVL TOUR BEER FICR CHEM TOYS
URAN WATR ACID (verze 4 a 5 vejtřasky), od verze 7 i JAVA CLAY SGCN KAOL (káva v hnědých pytlích, kupka
jílu, cukrová třtina s obrázkem vláken, kaolín v bílých pytlích), od verze 8 BRCK BDMT FRUT STUD WINE HOPS
(cihly a stavební materiál s podtypy, ovoce, studenti jako lidé, víno v sudech, chmel jako seno). Postup: `yagl -e zkusebni_naklady.grf`
v tomhle adresáři (yagl čte `sprites/zkusebni_naklady.yagl`).

Ověřeno 29. 9.: `testv3s` s `Praga_V3S-v4.grf` a `Praga_V3S_BRYLE-v4.grf`, vrstvy obrázku sedí
(TATO a SAND stejný sprite kupky, CMNT a GRVL stejný), turisté 20 a 3.
