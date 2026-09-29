# Zkušební náklady SAND TATO CMNT GRVL TOUR

Jen pro moji zkušební hru (`hra/`), hráčovi se nedává. Mírné klima zkušební hry nemá písek, brambory,
cement, kámen ani turisty, tak je přidává tenhle GRF, aby šla vyzkoušet vejtřaska verze 4:

- brambory (TATO) mají stejnou žlutou kupku jako písek (SAND), cement (CMNT) stejnou šedou jako
  kámen (GRVL);
- turisté (TOUR) jsou lidé: vojenská jich veze 20 pod plachtou, modrá 3 v kabině.

`grf_id` `MAXn`, náklady ve volných místech 0x15 až 0x19. Postup: `yagl -e zkusebni_naklady.grf`
v tomhle adresáři (yagl čte `sprites/zkusebni_naklady.yagl`).

Ověřeno 29. 9.: `testv3s` s `Praga_V3S-v4.grf` a `Praga_V3S_BRYLE-v4.grf`, vrstvy obrázku sedí
(TATO a SAND stejný sprite kupky, CMNT a GRVL stejný), turisté 20 a 3.
