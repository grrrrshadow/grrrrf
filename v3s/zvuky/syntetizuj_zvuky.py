# -*- coding: utf-8 -*-
# Umělý zvuk Pragy V3S (hráč 28. 9.: "musíš si poslechnout originál V3S jako vzor a udělat umělý zvuk,
# jak se rozjíždí", "ať to dělá rámus, V3S dělala velkej rámus"). Videa s V3S nemají volnou licenci,
# proto se zvuk skládá z toho, jak motor funguje, a z nahrávek v něm nic není:
#   Tatra 912: řadový šestiválec, čtyřtakt, 7,4 l, vzduchem chlazený, 72 kW při 2100 ot./min,
#   volnoběh kolem 550. Šest zapálení za dvě otáčky, tedy otáčky / 20 ran za sekundu
#   (27 ve volnoběhu, 105 na plný plyn).
# Složky: výfuk (tlakový puls každého zapálení a rezonance potrubí), klepání dieselu (krátký šum při
#   zapálení), sání, ventilátor chlazení (šum a pískání, roste s otáčkami), převodovka (kvílení podle
#   rychlosti), drnčení kabiny a korby (vejtřaska).
# Vzor (hráč 28. 9. poslal nahrávku V3S z inzerátu, jen k rozboru, v repu ani v GRF není). Z ní změřeno
#   na vytúrování 1880 ot./min: čáry ve spektru po otáčky / 120 (celý čtyřtaktní cyklus) a mezilehlé
#   jsou stejně silné jako zapalovací, takže každý válec zní jinak (VALCE_*, vlastní rána každého
#   válce); pískání na 38,4 a 60,8 a 91,2násobku otáček klikovky (1200, 1900, 2850 Hz); barva zvuku
#   (průměrné spektrum po třetinách oktávy, CIL_BARVA) s nejvíc síly mezi 1,2 a 2,5 kHz. Hloubky pod
#   125 Hz nahrávka z telefonu skoro nemá, tady zůstávají slabší, ale slyšet.
# Ve hře (pack_v3s.py, callback 0x33) jako u Sergeje (sergej/zvuky/README.md): odjezd ze zastávky
#   a z depa = rozjezd (událost 1), za jízdy každých PERIODA tiků kousek podle rychlosti (událost 7),
#   ve stání volnoběh (událost 8).
#   python3 syntetizuj_zvuky.py
# Výstup vedle skriptu: *.wav (mono, 22 050 Hz, 16 bit), zvuky.json, zdroje.txt, poslech.mp3
import os, re, json, wave, subprocess
import numpy as np
from scipy import signal
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
TU = os.path.dirname(os.path.abspath(__file__))
SRS = 44100                                       # syntéza
SR = 22050                                        # do hry (jako Sergej)
TIK = 0.027                                       # tik hry je 27 ms
PERIODA = 112                                     # 7 x 16, kousky jdou přesně po sobě (Sergej)
PRESAH = 0.08                                     # kousek je o tolik delší, další ho plynule převezme
DELKA = PERIODA * TIK + PRESAH                    # 3,104 s
MAX_OT = 2100                                     # jmenovité otáčky Tatry 912

# ---------------------------------------------------------------- motor
VALCE_A = 1 + np.array([0.30, -0.25, 0.15, -0.32, 0.22, -0.10])  # síla rány každého válce (pořadí zapalování)
VALCE_BARVA = 2.5                                                  # jak moc má každý válec vlastní barvu rány
VALCE_K = 1 + np.array([-0.35, 0.40, -0.10, 0.25, -0.45, 0.30])   # klepání každého válce jinak silné
CYKLUS = CYKLUS_STARY = None                                       # rozvod a vstřikovací čerpadlo (poloviční otáčky)
NIZKE_OT, VYSOKE_OT = 700, 1400                                    # prolnutí volnoběhu a vysokých otáček
PULSY = None

def _pulsy():
    """tlakový puls výfuku po zapálení: rychlý náběh, doznění a odražená vlna z potrubí; každý válec
    k tomu vlastní krátký šum (jiná cesta výfukovým potrubím), stejný v každém cyklu"""
    r = np.random.default_rng(912)
    tt = np.arange(int(0.04 * SRS)) / SRS
    a = lambda tau, t0=0.0: np.where(tt >= t0, ((tt - t0) / tau) * np.exp(1 - (tt - t0) / tau), 0.0)
    zaklad = a(0.004) - 0.45 * a(0.0072, 0.0118) + 0.15 * a(0.0108, 0.0292)      # oblá rána (vzor)
    out = []
    for c in range(6):
        s = r.standard_normal(len(tt)) * np.exp(-tt / r.uniform(0.003, 0.009))
        b, a2 = signal.butter(2, r.uniform(1200, 3500), "lowpass", fs=SRS)
        s = signal.lfilter(b, a2, s)
        out.append(zaklad * r.uniform(0.75, 1.25) + VALCE_BARVA * s / np.abs(s).max() * np.abs(zaklad).max())
    return out

def bpas(x, lo, hi, rad=2):
    b, a = signal.butter(rad, [lo, hi], "bandpass", fs=SRS)
    return signal.lfilter(b, a, x)

def rezon(x, f, q):
    b, a = signal.iirpeak(f, q, fs=SRS)
    return signal.lfilter(b, a, x)

def dolni(x, f, rad=2):
    b, a = signal.butter(rad, f, "lowpass", fs=SRS)
    return signal.lfilter(b, a, x)

def slozky(ot, zatez, rychlost, seed):
    """ot (ot./min), zatez (0-1), rychlost (km/h): pole po vzorcích SRS. Vrací slovník složek."""
    global PULSY, CYKLUS, CYKLUS_STARY
    if PULSY is None: PULSY = _pulsy()
    if CYKLUS_STARY is None:
        # vysoké otáčky: zamrzlý šum s cvaknutími, jak se hráči líbil ("od 0:26 super")
        rs = np.random.default_rng(1953)
        CYKLUS_STARY = rs.standard_normal(8192) * (1 + 1.5 * (rs.random(8192) < 0.04))
    if CYKLUS is None:
        # hluk, který se opakuje jednou za cyklus (dvě otáčky): ventily, vačky a čerpadlo, pro každou
        # polohu v cyklu pořád stejný, takže dělá čáry po otáčky / 120 jako ve vzoru
        # s rovnou barvou (náhodné fáze, stejná síla všech čar): obyčejný zamrzlý šum má náhodná silná
        # místa, která se opakují každý cyklus a ucho z nich slyší tón (na volnoběhu kolem 640 Hz);
        # k tomu 12 cvaknutí ventilů za cyklus (dva na válec) v pevných polohách
        rc = np.random.default_rng(1954)
        N = 8192
        CYKLUS = np.fft.irfft(np.exp(1j * rc.uniform(0, 2 * np.pi, N // 2 + 1)) * (np.arange(N // 2 + 1) > 0), N)
        CYKLUS /= CYKLUS.std()
        for v_ in range(12):
            i_ = (int((v_ + rc.uniform(-0.15, 0.15)) / 12 * N) + np.arange(60)) % N
            CYKLUS[i_] += np.exp(-np.arange(60) / 12.0) * rc.uniform(2.0, 3.5) * np.sign(rc.standard_normal(60))
    r = np.random.default_rng(seed)
    n = len(ot)
    faze = np.cumsum(ot / 60.0) / SRS             # otáčky klikovky
    k = np.floor(faze * 3).astype(np.int64)       # zapálení každou třetinu otáčky
    zap = np.nonzero(np.diff(k) > 0)[0] + 1
    valec = k[zap] % 6
    L = zatez[zap]
    # výfuk: puls za pulsem, síla podle plynu, válce a náhody, každý válec svou ranou
    vyfuk = np.zeros(n)
    sila = (0.22 + 0.78 * L ** 0.8) * VALCE_A[valec] * (1 + 0.13 * r.standard_normal(len(zap)))
    for c in range(6):
        imp = np.zeros(n); m = valec == c
        imp[zap[m]] = sila[m]
        vyfuk += signal.fftconvolve(imp, PULSY[c])[:n]
    # rezonance potrubí; ta nejvyšší by na volnoběhu po každé ráně zvonila (tón kolem 640 Hz), tak roste s otáčkami
    vyfuk = vyfuk + 0.7 * rezon(vyfuk, 92, 2.5) + 0.5 * rezon(vyfuk, 235, 3.5) + 0.35 * np.clip((ot - 500) / 1000, 0.1, 1) * rezon(vyfuk, 610, 4.5)
    vyfuk = dolni(vyfuk, 3200)
    # klepání dieselu: krátký šum při každém zapálení, ve volnoběhu je ho slyšet nejvíc
    ik = np.zeros(n)
    ik[zap] = (0.55 + 0.45 * L) * (0.9 - 0.15 * ot[zap] / MAX_OT) * VALCE_K[valec] * (1 + 0.3 * r.standard_normal(len(zap))).clip(0.2)
    obal = signal.fftconvolve(ik, np.exp(-np.arange(int(0.012 * SRS)) / (0.0013 * SRS)))[:n]
    klepani = bpas(r.standard_normal(n), 1300, 5200) * obal
    # sání: šum pod 900 Hz v rytmu zapálení
    ryt = dolni(np.abs(vyfuk), 60)
    ryt = ryt / (np.abs(ryt).max() + 1e-9)
    sani = dolni(r.standard_normal(n), 900) * (0.3 + ryt) * (0.2 + 0.8 * zatez) * (ot / MAX_OT)
    # ventilátor chlazení: šum a pískání, roste s otáčkami; tóny na násobcích otáček klikovky jako ve vzoru
    # (38,4 a 30,4 s harmonickými 60,8 a 91,2, tedy 1200, 1900 a 2850 Hz při 1880 ot./min)
    sila = 0.05 + 0.95 * (ot / MAX_OT) ** 2.5        # na volnoběhu ventilátor skoro neslyšet
    vsum = bpas(r.standard_normal(n), 350, 4200) * sila
    # pískání až od vyšších otáček (hráč 28. 9.: "v nízkých otáčkách tam jsou takové vysoké tóny")
    pisk = np.clip((ot - 650) / (1880 - 650), 0, 1) ** 1.5
    chveni = 1 + 0.25 * np.sin(2 * np.pi * faze * 3)                  # vibrace motoru v tónu
    piskot = np.zeros(n)
    for nasobek, a_ in ((38.4, 1.0), (30.4, 0.25), (60.8, 2.1), (91.2, 0.8)):
        piskot += a_ * np.sin(2 * np.pi * np.cumsum(ot / 60.0 * nasobek) / SRS + nasobek)
    piskot *= pisk * chveni
    # převodovka a rozvodovka: kvílení podle rychlosti, jen když jede a táhne
    fg = 14.0 * rychlost
    kvileni = np.sin(2 * np.pi * np.cumsum(fg) / SRS) * np.clip(rychlost / 20, 0, 1) * (0.4 + 0.6 * zatez)
    # vejtřaska: plechy kabiny (cinknutí) a prkna korby (bouchnutí), víc při otřesech
    otres = 0.45 + 0.55 * zatez * (ot / MAX_OT)
    drnceni = np.zeros(n)
    t = 0.0
    while True:
        t += r.exponential(1.0 / (3 + 12 * float(otres[min(int(t * SRS), n - 1)])))
        i = int(t * SRS)
        if i >= n: break
        if r.random() < 0.8:                     # cinknutí plechu, až od vyšších otáček
            f, tau = r.uniform(1300, 3800), r.uniform(0.002, 0.009)   # (hráč: na nízkých vysoké tóny vadí)
            a = r.uniform(0.3, 1.0) * float(np.clip((ot[i] - 800) / 600, 0, 1))
        else:
            f, tau, a = r.uniform(140, 380), r.uniform(0.012, 0.03), r.uniform(0.6, 1.6)
        m = min(n - i, int(6 * tau * SRS))
        tt = np.arange(m) / SRS
        drnceni[i:i + m] += a * otres[i] * np.sin(2 * np.pi * f * tt + r.uniform(0, 6.3)) * np.exp(-tt / tau)
    # nestejné válce rozhoupou motor a kabinu: dunění, které se opakuje jednou za cyklus (vejtřaska);
    # čáry po otáčky / 120 v hloubkách, ve vzoru stejně silné jako zapalovací
    poloha = (faze / 2) % 1.0
    rh = np.random.default_rng(812)
    dun = np.zeros(n)
    for kk in range(1, 25):
        if kk % 6 == 0: continue
        dun += rh.uniform(0.5, 1.0) / (1 + kk / 12) * np.cos(2 * np.pi * kk * poloha + rh.uniform(0, 6.3))
    dun *= (0.3 + 0.7 * zatez) * (0.5 + 0.5 * ot / MAX_OT)
    N = len(CYKLUS)
    w = np.clip((ot - NIZKE_OT) / (VYSOKE_OT - NIZKE_OT), 0, 1)
    mech = (w * CYKLUS_STARY[(poloha * N).astype(np.int64)]
            + (1 - w) * np.interp(poloha * N, np.arange(N + 1), np.append(CYKLUS, CYKLUS[0])))
    mech = bpas(mech, 120, 3000) * (0.35 + 0.65 * ot / MAX_OT) * (0.6 + 0.4 * zatez)
    return {"vyfuk": vyfuk, "klepani": klepani, "sani": sani, "ventilator": vsum, "piskot": piskot,
            "kvileni": kvileni, "drnceni": drnceni, "mechanika": mech, "duneni": dun}

# váhy složek (každá srovnaná na stejnou sílu při plném plynu 1800 ot./min): výfuk nese rytmus, klepání
# a ventilátor dělají "tatrovku", drnčení a dunění vejtřasku. Dunění a mechanika nastavené tak, aby čáry
# po otáčky / 120 byly proti zapalovacím jako ve vzoru (hloubky -3, středy +1 dB)
VAHY = {"vyfuk": 1.0, "klepani": 0.40, "sani": 0.22, "ventilator": 0.30, "piskot": 0.07, "kvileni": 0.035,
        "drnceni": 0.16, "mechanika": 0.8, "duneni": 2.0}
_ref = None
def ref_rms():
    global _ref
    if _ref is None:
        n = SRS
        s = slozky(np.full(n, 1800.0), np.full(n, 0.9), np.full(n, 40.0), 7)
        _ref = {k: float(np.sqrt((v ** 2).mean())) + 1e-12 for k, v in s.items()}
    return _ref

# Barva podle vzoru na všech otáčkách. Zkoušel jsem pod 700 ot./min syrovou (hlubší volnoběh), ale
# dunění cyklu (4,7 Hz na volnoběhu) pak kolébalo a hráč to nechtěl ("od 0:18 to ne, to tam nebylo");
# vysoké tóny na nízkých otáčkách dělalo pískání, ventilátor a cinkání plechů, ty jsou tam teď slabé.
# Nad VYSOKE_OT přesný filtr podle vzoru (zvuk, který hráč schválil), pod NIZKE_OT vyhlazený a krátký:
# přesný má úzký hrb a díru (500-630 a 800 Hz) a na volnoběhu mezi ranami dozvání jako tón.
def motor(ot, zatez, rychlost, seed, rovnat=True):
    s = slozky(ot, zatez, rychlost, seed)
    ref = ref_rms()
    x = sum(VAHY[k] * s[k] / ref[k] for k in s)
    if not rovnat: return x
    w = np.clip((ot - NIZKE_OT) / (VYSOKE_OT - NIZKE_OT), 0, 1)
    return w * signal.fftconvolve(x, vyrovnani(), mode="same") + (1 - w) * signal.fftconvolve(x, vyrovnani(hladke=True), mode="same")

# Barva zvuku podle vzoru: průměrné spektrum po třetinách oktávy (dB proti nejsilnějšímu pásmu),
# změřené na vytúrování 1880 ot./min. Pod 125 Hz nejvýš HLOUBKY_MIN pod vrcholem (telefon hloubky nebere,
# ve hře by bez nich motor zněl jako z rádia).
CIL_BARVA = {50: -47.8, 63: -43.9, 80: -32.3, 100: -22.2, 125: -16.4, 160: -16.5, 200: -15.2, 250: -13.4,
             315: -7.0, 400: -7.9, 500: -2.8, 630: -2.4, 800: -10.8, 1000: -7.3, 1250: -0.5, 1600: 0.0,
             2000: 0.0, 2500: -1.1, 3150: -8.4, 4000: -14.7, 5000: -28.7, 6300: -33.0, 8000: -39.4, 10000: -41.8}
HLOUBKY_MIN = -14.0

def tretiny(x, sr=SRS):
    f, P = signal.welch(x, sr, nperseg=8192)
    out = {}
    for fc in CIL_BARVA:
        m = (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))
        out[fc] = 10 * np.log10(P[m].mean() + 1e-20)
    mx = max(out.values())
    return {k: v - mx for k, v in out.items()}

def cil_barvy(hladke=False):
    """cíl; hladký je vyhlazený přes sousední pásma (úzký hrb a díra ze vzoru, nejspíš telefon a místnost,
    by ve filtru zvonily a na volnoběhu, kde je mezi ranami ticho, je slyšet tón)"""
    fc = sorted(CIL_BARVA)
    c = np.array([max(CIL_BARVA[k], HLOUBKY_MIN) if k <= 125 else CIL_BARVA[k] for k in fc])
    for _ in range(2 if hladke else 0):
        c = np.convolve(np.pad(c, 1, mode="edge"), [0.25, 0.5, 0.25], "valid")
    return dict(zip(fc, c))

_fir = {}
def vyrovnani(hladke=False):
    """FIR, které srovná barvu syntézy (plný plyn 1880 ot./min) na cíl; tři kola, další dorovnává zbytek"""
    if hladke in _fir: return _fir[hladke]
    n = 3 * SRS
    x = motor(np.full(n, 1880.0), np.full(n, 0.85), np.full(n, 40.0), 5, rovnat=False)
    fc = np.array(sorted(CIL_BARVA)); cil = cil_barvy(hladke)
    taps = 1023 if hladke else 4095                # krátký filtr zvoní méně
    d = np.zeros(len(fc))
    for _ in range(3):
        y = signal.fftconvolve(x, _navrh(fc, d, taps), mode="same") if d.any() else x
        moje = tretiny(y)
        d = d + np.array([cil[k] - moje[k] for k in fc])
    _fir[hladke] = _navrh(fc, d, taps)
    return _fir[hladke]

def _navrh(fc, d, taps):
    dd = np.convolve(np.pad(d, 1, mode="edge"), [0.25, 0.5, 0.25], "valid")      # vyhladit sousední pásma
    dd = np.clip(dd - dd.max(), -45, 0)
    f = np.concatenate([[0], fc, [SRS / 2]]) / (SRS / 2)
    g = 10 ** (np.concatenate([[dd[0]], dd, [dd[-1]]]) / 20)
    return signal.firwin2(taps, f, g)

def krivka(body, delka):
    """lomená čára [(čas s, hodnota)] po vzorcích SRS, mezi body kosinem (plynulé přechody)"""
    t = np.arange(int(delka * SRS)) / SRS
    out = np.empty_like(t)
    for (t0, v0), (t1, v1) in zip(body[:-1], body[1:]):
        m = (t >= t0) & (t <= t1)
        u = (t[m] - t0) / max(t1 - t0, 1e-9)
        out[m] = v0 + (v1 - v0) * (1 - np.cos(np.pi * u)) / 2
    out[t > body[-1][0]] = body[-1][1]
    return out

def zivost(n, seed, kolik):
    """pomalé kolísání (0,3-2 Hz), aby otáčky nestály jako přibité"""
    r = np.random.default_rng(seed + 1000)
    x = dolni(r.standard_normal(n + SRS), 2.0, rad=1)[SRS:]
    return 1 + kolik * x / (np.abs(x).max() + 1e-9)

# ---------------------------------------------------------------- do hry: EQ, ořez, hlasitost
EQ = ["highpass=f=35"]                            # barvu dělá vyrovnani() podle vzoru
LIMITER = ["aresample=22050", "alimiter=limit=0.98:attack=1:release=20:level=false"]
RYTMUS_MIN = 0.5                                  # ořez smí vzít nejvýš polovinu rytmu (Sergej)

def lufs(cesta):
    o = subprocess.run([FF, "-hide_banner", "-nostats", "-i", cesta, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

def rytmus(cesta):
    w = wave.open(cesta); a = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
    n = w.getframerate() // 100; e = np.sqrt((a[: len(a) // n * n].reshape(-1, n) ** 2).mean(1))
    return e.std() / e.mean()

def zapis_float(x, cesta):
    x = (x / (np.abs(x).max() + 1e-9) * 0.5).astype(np.float32)
    with open(cesta, "wb") as f:
        import struct
        data = x.tobytes()
        f.write(b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVEfmt " +
                struct.pack("<IHHIIHH", 16, 3, 1, SRS, SRS * 4, 4, 32) + b"data" + struct.pack("<I", len(data)) + data)

MERENI = []
def vyrob(x, vystup, cil, fade_in=PRESAH, fade_out=PRESAH):
    """syrový signál -> wav do hry: EQ, zesílení a měkký ořez (tanh) půlením na cíl v LUFS, rytmus hlídaný"""
    syr = os.path.join(TU, "_syrovy.wav"); zapis_float(x, syr)
    cesta = os.path.join(TU, vystup); delka = len(x) / SRS
    def udelej(af):
        af = ",".join(af + [f"afade=t=in:d={fade_in}:curve=qsin",
                            f"afade=t=out:st={delka - fade_out:.3f}:d={fade_out}:curve=qsin"])
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", syr, "-af", af, "-ac", "1",
                        "-ar", str(SR), "-c:a", "pcm_s16le", cesta], check=True)
        return lufs(cesta), rytmus(cesta)
    _, r0 = udelej(LIMITER)
    lo, hi = 0.0, 30.0
    for _ in range(9):
        g = (lo + hi) / 2
        l, r = udelej(EQ + [f"volume={g:.2f}dB", "asoftclip=type=tanh:oversample=4"] + LIMITER)
        if l < cil and r >= RYTMUS_MIN * r0: lo = g
        else: hi = g
    l, r = udelej(EQ + [f"volume={lo:.2f}dB", "asoftclip=type=tanh:oversample=4"] + LIMITER)
    os.remove(syr)
    MERENI.append((vystup, cil, l, lo, r / r0))
    return vystup

# ---------------------------------------------------------------- zvuky
# pásma jízdy: (do km/h, otáčky, plyn, LUFS); V3S jede nejvýš 60 km/h
# otáčky podle vzoru: vytúrování na 1880 ot./min, pod zátěží pomalu dolů k 1810
PASMA = [(15, 1350, 0.95, -10.5), (30, 1550, 0.9, -10.0), (45, 1750, 0.85, -9.5), (60, 1880, 0.8, -9.0)]
VOLNOBEH_OT, VOLNOBEH_LUFS = 560, -12.0
ROZJEZD_LUFS = -7.5                               # rámus při rozjezdu, jako nejhlasitější zvuky CZTR (-7)
VARIANT = 4

n = int(DELKA * SRS)
jizda = []
for i, (do_kmh, ot, plyn, cil) in enumerate(PASMA):
    rychl = (do_kmh - 7.5) if i < len(PASMA) - 1 else 55.0
    soubory = []
    for v in range(VARIANT):
        s = 100 * i + v
        o = ot * (1 + 0.015 * (v - 1.5)) * zivost(n, s, 0.035)
        z = np.clip(plyn * zivost(n, s + 50, 0.12), 0, 1)
        soubory.append(vyrob(motor(o, z, np.full(n, rychl), s), f"jizda_p{i}_{v}.wav", cil))
    jizda.append({"do_kmh": do_kmh, "otacky": ot, "lufs": cil, "zvuky": soubory})
stani = []
for v in range(VARIANT):
    s = 900 + v
    o = VOLNOBEH_OT * zivost(n, s, 0.03)
    stani.append(vyrob(motor(o, np.full(n, 0.12), np.zeros(n), s), f"stani_{v}.wav", VOLNOBEH_LUFS))

# rozjezd: volnoběh, přidá plyn, spojka chytne a otáčky spadnou, řev v jedničce až pod omezovač,
# přeřazení (plyn pryč, otáčky dolů) a doznění, další kousky jízdy převezmou
D = 4.4
ot_r = krivka([(0, 560), (0.30, 560), (0.62, 1150), (0.95, 860), (1.25, 900), (3.35, 1880), (3.55, 1885),
               (4.0, 1300), (D, 1250)], D)                  # stoupá asi 470 ot./min za s, ve vzoru 550
pl_r = krivka([(0, 0.12), (0.28, 0.12), (0.34, 1.0), (3.5, 1.0), (3.62, 0.18), (D, 0.3)], D)
rch_r = krivka([(0, 0), (0.95, 0), (3.5, 14), (D, 15)], D)
rozjezd = vyrob(motor(ot_r * zivost(len(ot_r), 77, 0.01), pl_r, rch_r, 77), "rozjezd.wav", ROZJEZD_LUFS,
                fade_in=0.02, fade_out=0.45)

# ---------------------------------------------------------------- klakson a výjezd z depa
# Hráč 28. 9.: "klakson a výjezd z depa motor s klaksonem", "asi klakson z Tatry 148". Elektrický
# dvoutónový klakson: membránu rozkmitává přerušovač, takže bzučí (pravoúhlá vlna s mnoha vyššími
# harmonickými), trychtýř zesílí pásma kolem 1,1, 2,3 a 3,4 kHz. Dva tóny o velkou tercii, 352 a 440 Hz.
def klakson(tony, delka, seed=148):
    """tony: [(začátek s, konec s)]; signál délky 'delka' s"""
    r = np.random.default_rng(seed)
    n = int(delka * SRS); t = np.arange(n) / SRS
    obal = np.zeros(n); od = np.full(n, 10.0)
    for z, k in tony:
        m = (t >= z) & (t < k + 0.1)
        u = t[m] - z
        obal[m] = np.maximum(obal[m], np.minimum(1, u / 0.012) * np.where(t[m] > k, np.exp(-(t[m] - k) / 0.02), 1))
        od[m] = np.minimum(od[m], u)
    y = np.zeros(n)
    for f0, a0 in ((352.0, 1.0), (440.0, 0.8)):
        jit = dolni(r.standard_normal(n), 25); jit /= np.abs(jit).max() + 1e-9
        f = f0 * (1 - 0.035 * np.exp(-od / 0.025)) * (1 + 0.003 * jit)     # při náběhu o kousek níž
        faze = np.cumsum(f) / SRS
        for kk in range(1, int(7000 / f0) + 1):                            # pravoúhlá vlna, střída 0,35
            y += a0 * (2 / (np.pi * kk)) * np.sin(np.pi * kk * 0.35) * np.cos(2 * np.pi * kk * faze)
        y += a0 * 0.15 * bpas(r.standard_normal(n), 2000, 6000) * ((faze % 1) < 0.08)   # chrapot kontaktů
    y = y + 1.2 * rezon(y, 1100, 3) + 0.9 * rezon(y, 2300, 4) + 0.5 * rezon(y, 3400, 5)
    return y * obal

def startovani(delka, seed=912):
    """startér protáčí motor kolem 170 ot./min bez zapalování: komprese motor brzdí a pouští (syčení
    a bouchnutí vzduchu), startér kvílí (věnec setrvačníku 120 zubů, asi 340 Hz a vyšší)"""
    r = np.random.default_rng(seed)
    n = int(delka * SRS)
    f0 = np.cumsum(np.full(n, 170 / 60)) / SRS
    ot = 170 * (1 + 0.18 * np.sin(2 * np.pi * f0 * 3 - 1.2))
    faze = np.cumsum(ot / 60) / SRS
    k = np.floor(faze * 3).astype(np.int64); komp = np.nonzero(np.diff(k) > 0)[0] + 1
    imp = np.zeros(n); imp[komp] = 1 + 0.15 * r.standard_normal(len(komp))
    tt = np.arange(int(0.06 * SRS)) / SRS
    vzduch = signal.fftconvolve(imp, (tt / 0.008) * np.exp(1 - tt / 0.008))[:n]
    obal = dolni(signal.fftconvolve(imp, np.exp(-tt / 0.03))[:n], 30)
    syceni = bpas(r.standard_normal(n), 200, 2500) * obal
    fs = 2 * np.pi * np.cumsum(ot / 60 * 120) / SRS
    kvil = sum((0.8 / kk) * np.sin(kk * fs + kk) for kk in range(1, 7)) + 0.4 * np.sin(1.4 * fs)
    kvil = kvil * (0.8 + 0.2 * np.sin(2 * np.pi * faze * 3)) + 0.3 * bpas(r.standard_normal(n), 1000, 4000)
    norm = lambda s: s / (np.sqrt((s ** 2).mean()) + 1e-12)
    return norm(vzduch) + 0.6 * norm(syceni) + 0.5 * norm(kvil)

# Výjezd z depa: startér, motor chytne a srovná se na volnoběh, zatroubí "tú-túú", přidá plyn a vyjede.
# Hra ho pouští jako odjezd (událost 1), jen když je auto ještě schované v depu (pack_v3s.py, var 0xB2).
DZ, CHYTNE = 5.0, 0.95
nz = int(DZ * SRS); tz = np.arange(nz) / SRS
st = np.zeros(nz); s_ = startovani(1.35); st[:len(s_)] = s_ * np.clip((1.3 - tz[:len(s_)]) / 0.3, 0, 1)
ot_z = krivka([(0, 200), (0.2, 700), (0.45, 1050), (0.9, 700), (1.4, 640), (2.45, 640), (2.55, 680), (3.7, 1300),
               (DZ - CHYTNE, 1350)], DZ - CHYTNE)
pl_z = krivka([(0, 0.7), (0.25, 1.0), (0.5, 0.3), (1.2, 0.12), (2.45, 0.12), (2.55, 1.0), (3.75, 1.0), (DZ - CHYTNE, 0.6)],
              DZ - CHYTNE)
rch_z = krivka([(0, 0), (2.55, 0), (DZ - CHYTNE, 8)], DZ - CHYTNE)
mot = motor(ot_z * zivost(len(ot_z), 88, 0.01), pl_z, rch_z, 88)
mz = np.zeros(nz); i0 = int(CHYTNE * SRS); mz[i0:i0 + len(mot)] = mot[: nz - i0] * np.clip((tz[i0:i0 + len(mot)] - CHYTNE) / 0.05, 0, 1)
rms_vol = np.sqrt((mz[int(2.0 * SRS):int(3.2 * SRS)] ** 2).mean())    # motor na volnoběh kolem troubení
kl = klakson([(2.2, 2.42), (2.54, 3.02)], DZ)
kl *= 1.6 * rms_vol / np.sqrt((kl[int(2.25 * SRS):int(2.95 * SRS)] ** 2).mean())
# Hrac 29. 9.: "ustrihni starter ze zvuku, tu prvni vterinu, mozna dve vteriny, kdyz ho pustim z depa". Starter hraje
# do 1,3 s (motor chytne v 0,95 s pod nim), zvuk proto zacina az v 1,3 s: motor se vytaci, srovna na volnobeh,
# zatrouba a vyjede (3,7 s misto 5 s).
STRIH = 1.3
vyjezd = vyrob((0.8 * rms_vol * st + mz + kl)[int(STRIH * SRS):], "vyjezd_z_depa.wav", ROZJEZD_LUFS, fade_in=0.03, fade_out=0.5)

json.dump({"perioda_tiku": PERIODA, "1": rozjezd, "1_depo": vyjezd, "jizda": jizda, "stani": stani},
          open(os.path.join(TU, "zvuky.json"), "w"), indent=1)
open(os.path.join(TU, "zdroje.txt"), "w").write(
    "cs: Zvuky: umělé, složené podle motoru Tatra 912 (vlastní práce, bez cizích nahrávek).\n"
    "en: Sounds: synthesized after the Tatra 912 engine (own work, no third-party recordings).\n")

# ---------------------------------------------------------------- poslech: jak to hraje ve hře
def cti(f):
    w = wave.open(os.path.join(TU, f)); return np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
P = PERIODA * TIK
plan = [(0.0, vyjezd)]                                              # vyjede z depa (událost 1 v depu)
t1 = 16 * TIK
for j, p in enumerate([0, 0, 1, 1, 2]):                             # jede, zrychluje
    plan.append((t1 + j * P, jizda[p]["zvuky"][j % VARIANT]))
t2 = t1 + 5 * P
plan += [(t2 + k * P, stani[k % VARIANT]) for k in range(2)]        # stojí v zastávce
t3 = t2 + 2 * P
plan.append((t3, rozjezd))                                          # odjede ze zastávky (událost 1)
for j, p in enumerate([0, 1, 2, 3, 3]):
    plan.append((t3 + 16 * TIK + j * P, jizda[p]["zvuky"][(j + 1) % VARIANT]))
konec = t3 + 16 * TIK + 5 * P
plan += [(konec + k * P, stani[(k + 2) % VARIANT]) for k in range(2)]   # zastaví
mix = np.zeros(int((konec + 2 * P + 1) * SR))
for t, f in plan:
    a = cti(f); i = int(t * SR); mix[i:i + len(a)] += a[: len(mix) - i]
mix = np.clip(mix, -1, 1)
tmp = os.path.join(TU, "_poslech.wav")
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "128k",
                os.path.join(TU, "poslech.mp3")], check=True)
os.remove(tmp)

for f, cil, l, g, r in MERENI:
    print(f"{f:18s} cil {cil:6.1f} LUFS  vyslo {l:6.1f}  zesileni {g:+5.1f} dB  rytmus {r * 100:3.0f} %")
print("hotovo:", sum(len(p["zvuky"]) for p in jizda), "kousku jizdy,", len(stani), "volnobeh,", rozjezd, vyjezd)
