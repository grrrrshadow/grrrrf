# Zvuky Sergeje

Hráč: *„musí to být nejhlasitější mašinka, ten motor musí být hodně slyšet“*, *„rozstřihej to, ať dělá
bordel celou cestu“*, *„pro každou rychlost jí syntetizuj zvuk, rytmus“*, *„jak bude zrychlovat, bude
přehrávat další a další rychlejší zvuk a větší řev“*. Sergej ČSD s tlumičem, M62 Tamtam tajgy bez.

Všechno dělá `priprav_zvuky.py` (ffmpeg z `imageio-ffmpeg`):

    python3 priprav_zvuky.py <alexdarek_M62.mp3> <WalkingWithMicrophones_2M62U.mp3>

Vstupem jsou náhledy „preview-hq“ z Freesound (stránky 698211 a 557174, MP3 48 kHz stereo). Výstup:
54 wav (mono, 22 050 Hz, 16 bit), `zvuky.json` pro `pack_sergej.py`, `zdroje.txt` pro `license.txt`
a `poslech.mp3`, kde to hraje jako ve hře: volnoběh, odjezd s troubením, rozjezd přes všechna pásma,
tunel, nejdřív zelená, pak červená.

## Kdy co hraje (callback 0x33)

| událost | kdy ji hra pošle | Sergej |
|---|---|---|
| 1 | odjezd ze stanice a „zahoukej“ u nádražního směrování (`PlayLeaveStationSound`) | `troubeni.wav`, trumpetka alexdarek 0:28,8, 2,8 s |
| 2 | vjezd do tunelu | `troubeni_tunel.wav`, alexdarek 0:38,2, 2,8 s |
| 7 | každých 16 tiků, když jede (`tick_counter` vozidla, `vehicle.cpp`) | kousek motoru podle rychlosti |
| 8 | každých 16 tiků, když stojí nebo brzdí (`TrainSlowing`) | volnoběh |
| ostatní | porucha, nakládka… | callback selže (`0x7FFF`), hra pustí svůj zvuk |

Obě lokomotivy troubí stejnou nahrávkou. Tlumič má jen motor.

**`0x7FFF` a `0xFFFF` nejsou totéž.** `0xFFFF` má horní bit, takže je to výsledek 0x7FFF, neplatný
zvuk: hra nepustí nic, ani svůj výchozí (`GetGroupFromGroupID`, `PlayVehicleSound`). `0x7FFF` bez
horního bitu je výslovné selhání a hra pak pustí svůj zvuk, u poruchy `SND_10_BREAKDOWN_TRAIN_SHIP`.
Brány motoru vracejí `0xFFFF` (ticho), přepínač událostí má výchozí `0x7FFF`.

V tunelu motor není slyšet, vlak je skrytý a hra pro skrytá vozidla zvuky nevolá.

## Časování

Událost 7 chodí po 16 tících. Brána pustí kousek, jen když je čítač tiků hry (globální proměnná
0x0A, `TimerGameTick::counter`, 16 bitů) v prvních 16 tících periody: `var[0x0A] % 112` v 0–15.
Do každých 16 tiků padne právě jedna událost, takže vyjde **přesně jeden kousek za 112 tiků**
(3,024 s při 27 ms na tik).

- Perioda musí být násobek 16. Při 111 (první verze) se událost v okně každou periodu posunula o tik
  a jednou za 16 kousků se dva kousky překryly o 0,4 s.
- Kousek trvá 3,104 s, tedy o 80 ms déle, a na koncích má náběh a doznění čtvrtsinusem.
  Sousední kousky se tak prolnou se stejným výkonem, bez díry a bez rázu.
- Který ze čtyř kousků pásma hraje, určuje `var[0x0A] / 112 % 4`. Pásmo určuje rychlost celého vlaku
  (`var[0xB4]` v nadřazeném vozidle).
- Jednou za 65 536 tiků (29,5 min) čítač přeteče a 65 536 není násobek 112. Dva kousky pak začnou
  16 tiků po sobě, jednou za půl hodiny to nevadí.

`kontrola_zvuku.py` (o adresář výš) projde rozbalený GRF tik po tiku a tohle všechno ověří.

## Pásma motoru

Kousky: 2M62U 26 s, 30 s, 33 s (úsek 17–36 s, který hráč vybral jako normální jízdu) a alexdarek 42 s
(průjezd na plný výkon). Každé pásmo je přepočítané na jiné otáčky, `asetrate` mění výšku i rytmus najednou.

| pásmo | rychlost | otáčky | zelená LUFS | rytmus zelená | červená LUFS | rytmus červená |
|---|---|---|---|---|---|---|
| volnoběh | stojí, brzdí | ×0,70 | −11,1 | 68–84 % | −12,6 | 90–105 % |
| p0 | do 15 km/h | ×0,78 | −10,1 | 63–81 % | −11,6 | 87–105 % |
| p1 | do 30 km/h | ×0,86 | −9,5 | 61–77 % | −11,0 | 84–101 % |
| p2 | do 45 km/h | ×0,95 | −8,9 | 58–74 % | −10,4 | 81–101 % |
| p3 | do 60 km/h | ×1,04 | −8,3 | 55–66 % | −9,8 | 82–95 % |
| p4 | do 80 km/h | ×1,13 | −7,7 | 52–62 % | −9,2 | 77–89 % |
| p5 | nad 80 km/h | ×1,24 | −7,1 | 52–55 % | −8,6 | 75–82 % |

Troubení −7,1 LUFS. Surové kousky mají −24 až −15 LUFS.

## Hlasitost

LUFS je hlasitost podle EBU R128, jak ji slyší ucho. Pro srovnání (rozbalené GRF z BaNaNaS):

- **CZTR Engines Diesel 1.1.0:** jen rozjezd a tunel, −17 až −7 LUFS. Nejhlasitější jsou
  750 rozjezd −7,0 a 742 tunel −6,9.
- **CDset:** −34 až −17 LUFS.
- **Základní hra:** vlaky za jízdy nezní vůbec.

Sergej hraje pořád a na plné rychlosti tak nahlas jako nejhlasitější zvuk CZTR.

Řetěz jednoho kousku: mono → 44,1 kHz → `asetrate` na otáčky → horní propust 35 Hz → ekvalizér
(+2 dB 120 Hz, +6 dB 700 Hz, +5 dB 1,8 kHz, +3 dB 3,5 kHz) → zesílení → měkký ořez `asoftclip=tanh`
(4× převzorkování) → 22 050 Hz → limiter 0,98 → náběh a doznění. Zesílení se hledá půlením: co nejblíž
cíli v LUFS, ale **rytmus nesmí klesnout pod polovinu**. Rytmus se měří jako modulace obálky po 10 ms,
tedy jak moc je slyšet bouchání motoru.

Proč ořez a ne kompresor:

- **Kompresor jede po obálce a rytmus srovná.** S kompresorem nebo paralelní kompresí spadla modulace
  z 0,31–0,37 na 0,10–0,17. Ořez uřízne jen špičky vlny, rytmus nechá a přidá vyšší harmonické.
- **Harmonické jsou slyšet i z notebooku.** Kousky z 2M62U mají přes 70 % energie pod 120 Hz, a to
  malé reproduktory nezahrají. Středy 0,5–2 kHz stouply z 9–17 % na 24–40 %.
- **Horní propust jen 35 Hz.** Propust 60 Hz vzala třetinu rytmu, bouchání je hodně nízko.

S rychlostí roste zesílení do ořezu, takže řev je hlasitější i hrubší.

**Tlumič** (Sergej ČSD): menší ekvalizér (+3 dB 120 Hz, +4 dB 500 Hz), po ořezu dvakrát dolní propust
1,4 kHz a +3 dB basů na 110 Hz. Je o 1,5 LU tišší a hlubší, rytmus mu zůstane skoro celý.

**Nahrávky jsou 48 kHz.** První verze dávala `asetrate=44100·otáčky` rovnou na 48 kHz, takže všechno
včetně troubení hrálo o 8 % níž a pomaleji. Teď se nejdřív převzorkuje na 44,1 kHz.

## Licence

`zdroje.txt` se při balení přepisuje do `license.txt` vedle GRF (řádky `cs:` a `en:`):

- alexdarek, „Heavy diesel locomotive M62 with a freight train“, https://freesound.org/s/698211/ , CC0;
- Walking.With.Microphones, „Freight train. Locomotive - 2M62U (2М62У)“, https://freesound.org/s/557174/ ,
  CC BY 4.0, uvést autora a úpravy.

Kopie wav v `grf/*/sprites/` dělá `pack_sergej.py` a do gitu nejdou, zdroj je tady.
