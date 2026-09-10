#!/usr/bin/env python3
"""Vytáhne PŘESNÝ čas z Oyez API — jediný zdroj v celé knihovně,
který dává sekundy a k tomu přímé mp3.

Oyez má nezdokumentované veřejné API. Přepis nese u každého bloku
řeči pole start/stop v sekundách a na konci media_file s odkazy na
mp3/ogg na S3. Tím se řádek posune z "unverified" na
"verified_transcript" s reálným offsetem do konkrétního souboru.

    python3 scripts/oyez_timestamp.py --case 2006/06-593 --phrase footman
    python3 scripts/oyez_timestamp.py --url https://www.oyez.org/cases/2006/06-593 --phrase "footman"

Pozn.: v prostředí s omezeným egressem (Claude Code na webu) tohle
neprojde — api.oyez.org je blokovaný. Spouštěj lokálně.
"""
import json, re, sys, argparse, urllib.request, urllib.error

UA = {"User-Agent": "Mozilla/5.0 (WhatTheFact soundbite research)"}

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} na {url}")
    except Exception as e:
        sys.exit(f"Nepovedlo se stáhnout {url}\n  {e}\n"
                 "  Pokud jde o blokovaný egress, spusť skript lokálně mimo sandbox.")

def hhmmss(s):
    s = int(float(s)); return f"{s//3600:02d}:{s%3600//60:02d}:{s%60:02d}"

def walk(node, speaker=None, out=None):
    """Prochází JSON obecně a sbírá bloky, které mají start/stop a text.
    Tvar Oyez API není dokumentovaný a mění se, tak se na cestu nespoléháme."""
    out = [] if out is None else out
    if isinstance(node, dict):
        name = None
        sp = node.get("speaker")
        if isinstance(sp, dict): name = sp.get("name")
        elif isinstance(sp, str): name = sp
        speaker = name or speaker
        if "start" in node and "stop" in node:
            text = node.get("text")
            if isinstance(text, str) and text.strip():
                out.append((float(node["start"]), float(node["stop"]), speaker, text.strip()))
        for v in node.values(): walk(v, speaker, out)
    elif isinstance(node, list):
        for v in node: walk(v, speaker, out)
    return out

def media(node, out=None):
    out = [] if out is None else out
    if isinstance(node, dict):
        if "href" in node and isinstance(node["href"], str) and re.search(r"\.(mp3|ogg|m3u8)(\?|$)", node["href"]):
            out.append(node["href"])
        for v in node.values(): media(v, out)
    elif isinstance(node, list):
        for v in node: media(v, out)
    return out

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--case", help="term/docket, např. 2006/06-593")
    g.add_argument("--url", help="celá oyez.org URL případu")
    p.add_argument("--phrase", required=True, help="část hlášky, klidně jen jedno slovo")
    p.add_argument("--json", action="store_true", help="vypsat rovnou náplast do JSONL řádku")
    a = p.parse_args()

    case = a.case
    if a.url:
        m = re.search(r"/cases/([^/]+)/([^/?#]+)", a.url)
        if not m: sys.exit("Z URL nejde vyčíst term/docket.")
        case = f"{m.group(1)}/{m.group(2)}"

    data = get(f"https://api.oyez.org/cases/{case}")
    audios = data.get("oral_argument_audio") or []
    if not audios: sys.exit(f"Případ {case} nemá v API zvuk ústního jednání.")

    needle = a.phrase.lower()
    hits = 0
    for aud in audios:
        href = aud.get("href")
        if not href: continue
        doc = get(href)
        blocks = walk(doc)
        mp3s = [u for u in media(doc) if u.endswith(".mp3")]
        title = doc.get("title") or data.get("name") or case
        for start, stop, speaker, text in blocks:
            if needle in text.lower():
                hits += 1
                print(f"\n{title}")
                print(f"  {hhmmss(start)}  ({start:.1f} s – {stop:.1f} s, délka {stop-start:.1f} s)")
                print(f"  {speaker or 'neznámý mluvčí'}: {text}")
                if mp3s: print(f"  mp3: {mp3s[0]}")
                if a.json:
                    print("  náplast do řádku: " + json.dumps({
                        "audio_url": mp3s[0] if mp3s else None,
                        "audio_url_type": "oyez_mp3",
                        "start_time": hhmmss(start),
                        "duration_sec": round(stop - start, 1),
                        "duration_estimated": False,
                        "verification": "verified_transcript",
                        "verification_note": f"Čas z Oyez API, blok {start:.1f}–{stop:.1f} s v {href}",
                        "search_query": None,
                    }, ensure_ascii=False))
    if not hits:
        sys.exit(f"\nFráze {a.phrase!r} v přepisu není. Zkus kratší úsek nebo jedno slovo — "
                 "přepis se od citace v článcích často liší interpunkcí.")
    print(f"\n{hits} shod. Pozor: délka bloku je délka celé repliky, ne jen tvé věty — "
          "duration_sec případně zkrať na použitelný úsek.")

if __name__ == "__main__":
    main()
