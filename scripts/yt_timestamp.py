#!/usr/bin/env python3
"""Najde hlášku v automatických titulcích YouTube a vrátí čas.

K čemu to je: YouTube je nejlepší NÁLEZIŠTĚ a nejrychlejší způsob, jak
ukotvit čas. Není to zdroj souboru. Master se pořád bere z původního
archivu (senate.gov, archive.org, Oyez, NARA) — kvůli licenci
i kvůli tomu, že re-upload bývá překódovaný a ustřižený.

    python3 scripts/yt_timestamp.py --video 6w5sfAyxmFk --phrase "series of tubes"

Potřebuje yt-dlp v PATH. V sandboxu s blokovaným egressem to neprojde.
"""
import argparse, os, re, subprocess, sys, tempfile, glob, shutil

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()

def parse_cues(path):
    """Vrátí [(sekundy, slovo)] z VTT/SRT."""
    t = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})")
    words, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = t.search(line)
        if m:
            cur = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) + int(m.group(4))/1000
            continue
        if cur is None: continue
        txt = re.sub(r"<[^>]+>", " ", line).strip()
        if not txt or txt.isdigit() or txt.upper().startswith("WEBVTT"): continue
        for w in norm(txt).split():
            words.append((cur, w))
    # automatické titulky opakují řádky; zahoď bezprostřední duplicity
    out = []
    for s, w in words:
        if out and out[-1][1] == w and s - out[-1][0] < 4: continue
        out.append((s, w))
    return out

def hhmmss(s):
    s = int(s); return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True, help="ID videa nebo celá URL")
    p.add_argument("--phrase", required=True)
    p.add_argument("--lang", default="en")
    a = p.parse_args()

    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp není v PATH. Nainstaluj: pip install yt-dlp")

    vid = a.video
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})", vid)
    if m: vid = m.group(1)
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        sys.exit(f"{a.video!r} nevypadá jako ID videa.")

    tmp = tempfile.mkdtemp(prefix="ytcap-")
    try:
        cmd = ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
               "--sub-langs", a.lang, "--sub-format", "vtt",
               "-o", os.path.join(tmp, "cap"), f"https://www.youtube.com/watch?v={vid}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        files = glob.glob(os.path.join(tmp, "*.vtt")) + glob.glob(os.path.join(tmp, "*.srt"))
        if not files:
            sys.exit("Titulky se nestáhly.\n" + (r.stderr or r.stdout).strip()[:800])
        words = parse_cues(files[0])
        if not words: sys.exit("Titulky jsou prázdné.")

        flat = " ".join(w for _, w in words)
        needle = norm(a.phrase)
        starts, pos = [], 0
        idx = {}
        for i, (s, w) in enumerate(words):
            idx[pos] = s; pos += len(w) + 1

        found = 0
        for m2 in re.finditer(re.escape(needle), flat):
            at = max((k for k in idx if k <= m2.start()), default=None)
            if at is None: continue
            sec = idx[at]
            found += 1
            print(f"\n{hhmmss(sec)}  ({int(sec)} s)")
            print(f"  https://www.youtube.com/watch?v={vid}&t={int(sec)}s")
        if not found:
            print(f"Fráze {a.phrase!r} v automatických titulcích není.")
            print("Zkus kratší úsek — auto-titulky komolí jména a interpunkci.")
            sys.exit(2)
        print("\nTitulky jsou automatické, takže čas ber jako navigaci na vteřinu, ne na snímek.")
        print("Do řádku patří verification=verified_transcript jen tehdy, když si to poslechem potvrdíš.")
        print("Master soubor pořád ber z původního archivu, ne z tohoto videa.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
