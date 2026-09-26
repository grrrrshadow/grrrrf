#!/usr/bin/env python3
"""Soupis a vytazeni souboru ze zipu v GitHub releasech, bez stazeni celeho zipu (HTTP Range).

  zipindex.py list URL                 vypise zaznamy zipu
  zipindex.py get URL JMENO VYSTUP     vytahne jeden zaznam (cast jmena staci, musi byt jednoznacna)
  zipindex.py index VYSTUP.md          projde vsechny releasy grrrrf a forclaude a zapise index:
                                       zaznamy zipu, obsah taru a vnorenych zipu, md5 a jmeno GRF

URL je odkaz ke stazeni assetu, napr.
  https://github.com/grrrrshadow/grrrrf/releases/download/par3/zip3.zip
Proxy tu potrebuje CA /root/.ccr/ca-bundle.crt.
"""
import sys, struct, subprocess, zlib, hashlib, json, re, io, zipfile, datetime

CA = "/root/.ccr/ca-bundle.crt"
REPOS = ["grrrrshadow/grrrrf", "grrrrshadow/forclaude"]


def curl(args, text=False):
    # proxy obcas spojeni zasekne: kratky pozadavek ma na sebe minutu, pak se zkusi znovu
    for pokus in range(4):
        try:
            return subprocess.run(["curl", "-sSL", "--fail", "--retry", "3", "--connect-timeout", "20", "--max-time", "60",
                                   "--cacert", CA] + args, capture_output=True, text=text, check=True).stdout
        except subprocess.CalledProcessError:
            if pokus == 3:
                raise


def rng(url, a, b):
    return curl(["-r", f"{a}-{b}", url])


def size(url):
    # HEAD na podepsanou adresu S3 vraci 401, velikost se bere z odpovedi na GET s rozsahem
    h = subprocess.run(["curl", "-sSL", "--connect-timeout", "20", "--max-time", "60", "--cacert", CA,
                        "-r", "0-0", "-D", "-", "-o", "/dev/null", url], capture_output=True, text=True).stdout
    return int(re.findall(r"(?i)content-range: bytes 0-0/(\d+)", h)[-1])


def entries(url):
    n = size(url)
    base = max(0, n - 8 * 2**20)
    tail = rng(url, base, n - 1)
    i = tail.rfind(b"PK\x05\x06")
    cnt, = struct.unpack("<H", tail[i + 10:i + 12])
    cds, cdo = struct.unpack("<II", tail[i + 12:i + 20])
    if cdo == 0xFFFFFFFF or cnt == 0xFFFF or cds == 0xFFFFFFFF:
        j = tail.rfind(b"PK\x06\x06")
        cds, cdo = struct.unpack("<QQ", tail[j + 40:j + 56])
    cd = tail[cdo - base:cdo - base + cds] if cdo >= base else rng(url, cdo, cdo + cds - 1)
    out, p = [], 0
    while p + 46 <= len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        flags, meth = struct.unpack("<HH", cd[p + 8:p + 12])
        csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
        nl, el, cl = struct.unpack("<HHH", cd[p + 28:p + 34])
        lho, = struct.unpack("<I", cd[p + 42:p + 46])
        raw = cd[p + 46:p + 46 + nl]
        try:
            name = raw.decode("utf-8")
        except UnicodeDecodeError:
            name = raw.decode("cp437")
        ex, q = cd[p + 46 + nl:p + 46 + nl + el], 0
        while q + 4 <= len(ex):                      # zip64: skutecne velikosti a offset
            hid, hl = struct.unpack("<HH", ex[q:q + 4])
            d, k = ex[q + 4:q + 4 + hl], 0
            if hid == 1:
                if usz == 0xFFFFFFFF: usz, = struct.unpack("<Q", d[k:k + 8]); k += 8
                if csz == 0xFFFFFFFF: csz, = struct.unpack("<Q", d[k:k + 8]); k += 8
                if lho == 0xFFFFFFFF: lho, = struct.unpack("<Q", d[k:k + 8]); k += 8
            q += 4 + hl
        out.append(dict(name=name, meth=meth, csz=csz, usz=usz, lho=lho))
        p += 46 + nl + el + cl
    return n, out


def stream(url, e):
    """Rozbaleny obsah jednoho zaznamu po kouscich, jednim pozadavkem."""
    if e["meth"] not in (0, 8):
        raise IOError(f"metoda {e['meth']} neumim")
    if e["csz"] == 0:
        return
    lh = rng(url, e["lho"], e["lho"] + 29)
    nl, el = struct.unpack("<HH", lh[26:30])
    start = e["lho"] + 30 + nl + el
    # dlouhy proud: kdyz minutu tece min nez 10 kB/s, curl skonci a zaznam se stahne znovu
    p = subprocess.Popen(["curl", "-sSL", "--fail", "--connect-timeout", "20", "--speed-limit", "10240",
                          "--speed-time", "60", "--cacert", CA, "-r", f"{start}-{start + e['csz'] - 1}", url],
                         stdout=subprocess.PIPE)
    d = zlib.decompressobj(-15) if e["meth"] == 8 else None
    got = 0
    while True:
        b = p.stdout.read(1 << 20)
        if not b:
            break
        got += len(b)
        yield d.decompress(b) if d else b
    if d:
        yield d.flush()
    p.wait()
    if p.returncode != 0 or got != e["csz"]:
        raise IOError(f"stazeno {got} z {e['csz']} B")


class Reader:
    def __init__(self, it):
        self.it, self.buf, self.eof = it, bytearray(), False

    def read(self, n):
        while len(self.buf) < n and not self.eof:
            try:
                self.buf += next(self.it)
            except StopIteration:
                self.eof = True
        out = bytes(self.buf[:n])
        del self.buf[:n]
        return out


def grf_info(head):
    """grf_id a jmeno z Action08 na zacatku GRF (kontejner 1 i 2)."""
    try:
        if head[:10] == b"\x00\x00GRF\x82\r\n\x1a\n":
            pos, big = 15, True
        else:
            pos, big = 0, False
        while pos < len(head) - 5:
            if big:
                sz, info = struct.unpack("<IB", head[pos:pos + 5]); pos += 5
            else:
                sz, info = struct.unpack("<HB", head[pos:pos + 3]); pos += 3
            if sz == 0:
                return None
            data = head[pos:pos + sz]
            if info == 0xFF and data[:1] == b"\x08":
                gid = data[2:6]
                nm = data[6:].split(b"\x00")[0]
                nm = nm[2:].decode("utf-8", "replace") if nm[:2] == b"\xc3\x9e" else nm.decode("latin-1")
                gid_s = "".join(chr(c) if 32 < c < 127 and chr(c) not in '\\"' else f"\\x{c:02X}" for c in gid)
                return f'{gid.hex()} "{gid_s}" {nm.strip()}'
            if info != 0xFF and not big:
                return None                          # kontejner 1: prvni skutecny sprite, Action08 uz nebude
            pos += sz if (info == 0xFF or big) else 0
    except Exception:
        return None
    return None


def md5_and_head(chunks, keep=512 * 1024):
    md, head = hashlib.md5(), bytearray()
    for b in chunks:
        md.update(b)
        if len(head) < keep:
            head += b[:keep - len(head)]
    return md.hexdigest(), bytes(head)


def tar_list(r):
    files, longname, paxpath = [], None, None
    while True:
        h = r.read(512)
        if len(h) < 512 or h == b"\0" * 512:
            break
        name = h[0:100].split(b"\0")[0].decode("utf-8", "replace")
        if h[257:262] == b"ustar":
            pre = h[345:500].split(b"\0")[0].decode("utf-8", "replace")
            if pre:
                name = pre + "/" + name
        f = h[124:136]
        sz = int.from_bytes(f[1:], "big") if f[0] & 0x80 else int(f.split(b"\0")[0].strip() or b"0", 8)
        typ = h[156:157]
        meta = typ in (b"L", b"x", b"g")
        md, head, data, left = hashlib.md5(), bytearray(), bytearray(), sz
        while left > 0:
            b = r.read(min(left, 1 << 20))
            if not b:
                raise IOError("tar je useknuty")
            left -= len(b)
            md.update(b)
            if meta:
                data += b
            elif len(head) < 512 * 1024:
                head += b[:512 * 1024 - len(head)]
        r.read((512 - sz % 512) % 512)
        if typ == b"L":
            longname = bytes(data).split(b"\0")[0].decode("utf-8", "replace"); continue
        if typ == b"x":
            for m in re.finditer(rb"\d+ path=([^\n]*)\n", bytes(data)):
                paxpath = m.group(1).decode("utf-8", "replace")
            continue
        if typ == b"g":
            continue
        name = paxpath or longname or name
        longname = paxpath = None
        if typ in (b"0", b"\0", b"7"):
            files.append((name, sz, md.hexdigest(), grf_info(bytes(head)) if name.lower().endswith(".grf") else None))
        elif typ == b"5":
            files.append((name.rstrip("/") + "/", 0, None, None))
    return files


def fmt(n):
    return f"{n:>13,}".replace(",", " ")


def deep(url, e):
    """Obsah zaznamu: tar -> jeho soubory, zip -> jeho zaznamy, grf -> md5 a jmeno."""
    low = e["name"].lower()
    if low.endswith(".tar"):
        return [("tar", x) for x in tar_list(Reader(stream(url, e)))]
    if low.endswith(".grf"):
        md, head = md5_and_head(stream(url, e))
        return [("grf", (md, grf_info(head)))]
    if low.endswith(".zip") and e["usz"] < 256 * 2**20:
        z = zipfile.ZipFile(io.BytesIO(b"".join(stream(url, e))))
        return [("zip", (i.filename, i.file_size)) for i in z.infolist()]
    return []


def releases(repo):
    return json.loads(curl([f"https://api.github.com/repos/{repo}/releases"], text=True))


def index(out):
    L = [f"# Index releasů\n",
         f"Vygenerováno `tools/zipindex.py index` {datetime.date.today()}. Každý zip v releasech",
         "repozitářů `grrrrf` a `forclaude`, u tarů, vnořených zipů a GRF i to, co je uvnitř.",
         "U GRF je md5 (podle něj hra pozná GRF v savu) a `grf_id` se jménem z Action08.\n",
         "Jeden soubor se dá vytáhnout bez stažení celého zipu:",
         "`python3 tools/zipindex.py get <odkaz na asset> <část jména> <výstup>`\n"]
    for repo in REPOS:
        for r in releases(repo):
            for a in r["assets"]:
                url = a["browser_download_url"]
                L.append(f"## {repo.split('/')[1]} / {r['tag_name']} — {a['name']}\n")
                L.append(f"`{url}`\n")
                if not a["name"].lower().endswith(".zip"):
                    L.append(f"{fmt(a['size'])} B, není zip\n"); continue
                n, es = entries(url)
                L.append(f"{fmt(n).strip()} B, {len(es)} záznamů\n")
                L.append("```")
                for e in es:
                    m = "uložený" if e["meth"] == 0 else "deflate" if e["meth"] == 8 else f"metoda {e['meth']}"
                    L.append(f"{fmt(e['usz'])}  {e['name']}   ({m})" if not e["name"].endswith("/") else f"{'':>13}  {e['name']}")
                    for pokus in range(3):
                        try:
                            obsah = deep(url, e)
                            break
                        except Exception as ex:
                            obsah = ex
                    try:
                        if isinstance(obsah, Exception):
                            raise obsah
                        for kind, x in obsah:
                            if kind == "tar":
                                nm, sz, md, gi = x
                                L.append(f"{'':>13}    ↳ {fmt(sz).strip():>11}  {nm}" + (f"  md5 {md}" if nm.lower().endswith('.grf') else "") + (f"\n{'':>13}        GRF {gi}" if gi else ""))
                            elif kind == "zip":
                                L.append(f"{'':>13}    ↳ {fmt(x[1]).strip():>11}  {x[0]}")
                            else:
                                L.append(f"{'':>13}    md5 {x[0]}" + (f"\n{'':>13}    GRF {x[1]}" if x[1] else ""))
                    except Exception as ex:
                        L.append(f"{'':>13}    !! obsah nepřečten: {ex}")
                    print(f"{repo} {r['tag_name']} {e['name']}", file=sys.stderr, flush=True)
                L.append("```\n")
    open(out, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "list":
        n, es = entries(sys.argv[2])
        print(f"zip {n} B, {len(es)} zaznamu")
        for e in es:
            print(f"{fmt(e['usz'])} m{e['meth']} {e['name']}")
    elif cmd == "get":
        url, want, outp = sys.argv[2:5]
        n, es = entries(url)
        hit = [e for e in es if want in e["name"]]
        if len(hit) != 1:
            sys.exit(f"'{want}' odpovida {len(hit)} zaznamum: " + ", ".join(e["name"] for e in hit[:10]))
        with open(outp, "wb") as f:
            for b in stream(url, hit[0]):
                f.write(b)
        print(f"{hit[0]['name']} -> {outp}")
    elif cmd == "index":
        index(sys.argv[2])
    else:
        print(__doc__)
