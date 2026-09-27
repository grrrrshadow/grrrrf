# -*- coding: utf-8 -*-
# Nastříhá a připraví zvuky Sergeje ze dvou nahrávek z Freesound:
#   python3 priprav_zvuky.py <alexdarek_M62.mp3> <WalkingWithMicrophones_2M62U.mp3>
#   698211 "Heavy diesel locomotive M62 with a freight train", alexdarek, CC0
#   557174 "Freight train. Locomotive - 2M62U (2М62У)", Walking.With.Microphones, CC BY 4.0
#
# Troubení: trumpetka při odjezdu a na "zahoukej" (událost 1), druhé troubení v tunelu (událost 2).
# Motor (hráč: "rozstřihej to, ať dělá bordel celou cestu", "pro každou rychlost jí syntetizuj zvuk, rytmus"):
#   krátké kousky, pro každé pásmo rychlosti přepočítané na jiné otáčky (výška i rytmus najednou,
#   jako když motor přidá). Hra každých PERIODA tiků pustí další kousek podle rychlosti (událost 7),
#   ve stání a při brzdění volnoběh (událost 8). Sergej ČSD má motor přes tlumič.
# Hlasitost (hráč: "musí to být nejhlasitější mašinka, ten motor musí být hodně slyšet"): každý zvuk
#   se dotáhne na cíl v LUFS (EBU R128, hlasitost, jak ji slyší ucho). Pro srovnání: nejhlasitější zvuky
#   CZTR Engines Diesel 1.1.0 mají kolem -7 LUFS, CDset -17 až -34 LUFS, vlaky základní hry za jízdy
#   nezní vůbec. Rachot pod 120 Hz malé reproduktory nezahrají, proto středy nahoru a měkký ořez (tanh),
#   který uřízne špičky vlny a udělá z rachotu vyšší harmonické, slyšet je i z notebooku. Rytmus motoru
#   přitom musí zůstat (RYTMUS_MIN). S rychlostí roste hlasitost i ořez, řev je hrubší.
# Výstup vedle skriptu: *.wav, zvuky.json (pro pack_sergej.py), zdroje.txt (do license.txt), poslech.mp3
import os, sys, re, json, wave, subprocess
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
TU = os.path.dirname(os.path.abspath(__file__))
M62, U2M62 = sys.argv[1], sys.argv[2]
SR = 22050                                        # hře stačí, soubory jsou poloviční
TIK = 0.027                                       # tik hry je 27 ms
PERIODA = 112                                     # 7 x 16: událost 7 chodí po 16 ticích, kousky pak jdou přesně
                                                  # po sobě (při 111 se každých 16 kousků dva překryly)
PRESAH = 0.08                                     # kousek je o tolik delší, další ho plynule převezme
DELKA = PERIODA * TIK + PRESAH                    # 3,104 s
# nahrávky jsou 48 kHz: nejdřív mono a 44,1 kHz, teprve pak asetrate (dřív to šlo o 8 % níž a pomaleji)
VSTUP = ["pan=mono|c0=0.5*c0+0.5*c1", "aresample=44100"]
LIMITER = ["aresample=22050", "alimiter=limit=0.98:attack=1:release=20:level=false"]
# Hlasitost dělá měkký ořez (tanh), ne kompresor: kompresor jede po obálce a srovná rytmus motoru
# (modulace obálky spadla na 0,10-0,17 ze 0,31-0,37), ořez uřízne jen špičky vlny a rytmus nechá.
EQ = ["highpass=f=35",                                            # pod 60 Hz je bouchání motoru, nechat
      "equalizer=f=120:t=q:w=1:g=2", "equalizer=f=700:t=q:w=1:g=6",   # klepání a řev dvoutaktu
      "equalizer=f=1800:t=q:w=1.2:g=5", "equalizer=f=3500:t=q:w=1.5:g=3"]
EQ_TLUMIC = ["highpass=f=35", "equalizer=f=120:t=q:w=1:g=3", "equalizer=f=500:t=q:w=1:g=4"]
TLUMIC = ["lowpass=f=1400", "lowpass=f=1400", "bass=g=3:f=110"]  # tlumič: výšky pryč, basy trochu nahoru
RYTMUS_MIN = 0.5                                  # ořez smí vzít nejvýš polovinu rytmu (modulace obálky)

def filtry(otacky, tlumic, g):
    r = VSTUP + ([f"asetrate={44100 * otacky:.0f}", "aresample=44100"] if otacky != 1.0 else [])
    r += (EQ_TLUMIC if tlumic else EQ) + [f"volume={g:.2f}dB", "asoftclip=type=tanh:oversample=4"]
    return r + (TLUMIC if tlumic else []) + LIMITER

def lufs(cesta):
    o = subprocess.run([FF, "-hide_banner", "-nostats", "-i", cesta, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

def rytmus(cesta):
    """modulace obálky po 10 ms (směrodatná odchylka / průměr): kolik je slyšet bouchání motoru"""
    w = wave.open(cesta); a = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
    n = w.getframerate() // 100; e = np.sqrt((a[: len(a) // n * n].reshape(-1, n) ** 2).mean(1))
    return e.std() / e.mean()

MERENI = []
def vyrob(zdroj, od, vystup, cil, otacky=1.0, tlumic=False, delka=DELKA, fade_in=PRESAH, fade_out=PRESAH):
    """Úsek od 'od' s, ve hře trvá 'delka' s. Zesílení před ořezem se hledá půlením: co nejblíž 'cil' LUFS,
    ale rytmus nesmí klesnout pod RYTMUS_MIN původního."""
    cesta = os.path.join(TU, vystup)
    def udelej(af):
        af = ",".join(af + [f"afade=t=in:d={fade_in}:curve=qsin", f"afade=t=out:st={delka - fade_out:.3f}:d={fade_out}:curve=qsin"])
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(od), "-t", f"{delka * otacky:.3f}",
                        "-i", zdroj, "-af", af, "-ac", "1", "-ar", str(SR), "-t", f"{delka:.3f}", "-c:a", "pcm_s16le", cesta],
                       check=True)
        return lufs(cesta), rytmus(cesta)
    _, r0 = udelej(VSTUP + ([f"asetrate={44100 * otacky:.0f}", "aresample=44100"] if otacky != 1.0 else []) + LIMITER)
    lo, hi = 0.0, 30.0
    for _ in range(9):
        g = (lo + hi) / 2
        l, r = udelej(filtry(otacky, tlumic, g))
        if l < cil and r >= RYTMUS_MIN * r0: lo = g
        else: hi = g
    l, r = udelej(filtry(otacky, tlumic, lo))
    MERENI.append((vystup, cil, l, lo, r / r0))
    return vystup

TROUBENI_LUFS = -7.0                              # houkačka jako nejhlasitější zvuky CZTR (-6,9 až -7,6)
troubeni = vyrob(M62, 28.8, "troubeni.wav", TROUBENI_LUFS, delka=2.8, fade_in=0.02, fade_out=0.25)
tunel = vyrob(M62, 38.2, "troubeni_tunel.wav", TROUBENI_LUFS, delka=2.8, fade_in=0.02, fade_out=0.25)

# kousky motoru: tři z úseku, který hráč vybral jako normální jízdu (2M62U 17–36 s, hlasitější půlka),
# jeden z průjezdu alexdarek na plný výkon
KUSY = [(U2M62, 26), (U2M62, 30), (U2M62, 33), (M62, 42)]
# hráč: "jak bude zrychlovat, bude přehrávat další a další rychlejší zvuk a větší řev"
PASMA = [(15, 0.78, -10.0), (30, 0.86, -9.4), (45, 0.95, -8.8),                # (do km/h, otáčky, LUFS)
         (60, 1.04, -8.2), (80, 1.13, -7.6), (None, 1.24, -7.0)]
VOLNOBEH = [(U2M62, 26), (M62, 46)]
VOLNOBEH_OTACKY, VOLNOBEH_LUFS = 0.70, -11.0
TLUMIC_LU = -1.5                                  # Sergej ČSD o tolik tišší, zato hlubší

vystup = {}
for natier, tlumic, ubrat in (("zeleny", False, 0), ("cerveny", True, TLUMIC_LU)):
    pasma = []
    for p, (do_kmh, ot, cil) in enumerate(PASMA):
        pasma.append({"do_kmh": do_kmh, "otacky": ot, "lufs": cil + ubrat, "zvuky": [
            vyrob(z, od, f"{natier}_p{p}_{i}.wav", cil + ubrat, otacky=ot, tlumic=tlumic)
            for i, (z, od) in enumerate(KUSY, 1)]})
    stani = [vyrob(z, od, f"{natier}_stani_{i}.wav", VOLNOBEH_LUFS + ubrat, otacky=VOLNOBEH_OTACKY, tlumic=tlumic)
             for i, (z, od) in enumerate(VOLNOBEH, 1)]
    vystup[natier] = {"1": troubeni, "2": tunel, "jizda": pasma, "stani": stani, "perioda_tiku": PERIODA}
json.dump(vystup, open(os.path.join(TU, "zvuky.json"), "w"), indent=1, ensure_ascii=False)

open(os.path.join(TU, "zdroje.txt"), "w").write("""cs: Zvuky: troubení a část motoru z "Heavy diesel locomotive M62 with a freight train", autor alexdarek,
cs:     https://freesound.org/s/698211/ , licence CC0.
cs: Motor z "Freight train. Locomotive - 2M62U (2М62У)", autor Walking.With.Microphones,
cs:     https://freesound.org/s/557174/ , licence CC BY 4.0.
cs: Úpravy: nastříhané kousky, přepočítané na otáčky podle rychlosti, mono, ekvalizér, komprese,
cs:     měkký ořez a zesílení; u Sergeje ČSD navíc tlumič (seříznuté výšky).
en: Sounds: horn and part of the engine from "Heavy diesel locomotive M62 with a freight train" by alexdarek,
en:     https://freesound.org/s/698211/ , CC0.
en: Engine from "Freight train. Locomotive - 2M62U (2М62У)" by Walking.With.Microphones,
en:     https://freesound.org/s/557174/ , CC BY 4.0.
en: Changes: cut into short pieces, re-pitched per speed band, mono, EQ, compression,
en:     soft clipping and amplification; Sergej ČSD also muffled (silencer).
""")

# poslech jako ve hře: kousky po PERIODA ticích (s přesahem), troubení při rozjezdu přes motor,
# volnoběh, rozjezd přes všechna pásma po dvou kouscích, tunel; zeleně a pak červeně
def nacti(f):
    w = wave.open(os.path.join(TU, f)); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.int32)
krok = int(round(PERIODA * TIK * SR))
stopa = []                                        # (začátek ve vzorcích, soubor)
t = 0
for natier in ("zeleny", "cerveny"):
    z = vystup[natier]
    for f in z["stani"]:
        stopa.append((t, f)); t += krok
    stopa.append((t, z["1"]))                     # odjezd: troubí a rozjíždí se
    for p in z["jizda"]:
        for f in p["zvuky"][:2]:
            stopa.append((t, f)); t += krok
    t += SR
    stopa.append((t, z["2"])); t += 4 * SR
mix = np.zeros(t + 4 * SR, np.int32)
for zac, f in stopa:
    a = nacti(f); mix[zac:zac + len(a)] += a
mix = np.clip(mix, -32768, 32767).astype(np.int16)  # hra míchá stejně: sečte a ořízne
tmp = os.path.join(TU, "_poslech.wav")
w = wave.open(tmp, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(mix.tobytes()); w.close()
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-b:a", "160k", os.path.join(TU, "poslech.mp3")],
               check=True)
os.remove(tmp)
for f, cil, l, g, r in MERENI:
    print(f"{f:24s} cil {cil:6.1f} LUFS  vyslo {l:6.1f}  zesileni {g:+5.1f} dB  rytmus {r * 100:3.0f} %")
print("hotovo:", sum(len(p["zvuky"]) for p in vystup["zeleny"]["jizda"]), "kousku jizdy na natier, perioda", PERIODA, "tiku")
