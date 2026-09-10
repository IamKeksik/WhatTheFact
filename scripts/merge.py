#!/usr/bin/env python3
"""Sloucení shardů od paralelních agentů do data/soundbites.jsonl.

Agenti nikdy nepíší do knihovny přímo. Každý píše do vlastního
data/shards/<uzemi>.jsonl. Tenhle skript je jediné místo, kde se
kontroluje schéma a řeší duplicity.

    python3 scripts/merge.py            # kontrola, nic nezapíše
    python3 scripts/merge.py --apply    # slouční a zapíše
    python3 scripts/merge.py --check    # jen validace knihovny (CI)
"""
import json, sys, re, glob, os, argparse, collections, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "data", "soundbites.jsonl")
SHARDS = os.path.join(ROOT, "data", "shards")

KEYS = ["id","quote","quote_verbatim","speaker","source_title","source_type","year",
        "audio_url","audio_url_type","youtube","start_time","duration_sec","duration_estimated",
        "context_before","context_after","cultural_background","why_it_lands",
        "self_contained","recognition","licence","licence_note","topics","verification",
        "verification_note","search_query","alt_sources","beat"]

SOURCE_TYPES = {"congressional_hearing","scotus_argument","court_audio","federal_psa",
                "prelinger_film","pd_film","local_news","youtube_viral","city_council",
                "radio","podcast","speech","film","tv","advertisement","other"}
LICENCES = {"green_federal_pd","green_pd_age","yellow_verify","red_rights_reserved"}
SELF = {"yes","partial","memory_dependent"}
RECOG = {"universal","high","niche"}
VERIF = {"verified_transcript","unverified"}

def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()

def validate(r, where):
    errs = []
    missing = [k for k in KEYS if k not in r]
    extra = [k for k in r if k not in KEYS]
    if missing: errs.append(f"chybí klíče: {missing}")
    if extra:   errs.append(f"klíče navíc: {extra}")
    if missing: return errs
    if not r["id"] or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", r["id"]):
        errs.append(f"id musí být kebab-case: {r['id']!r}")
    if not str(r["quote"]).strip(): errs.append("prázdná quote")
    if r["source_type"] not in SOURCE_TYPES: errs.append(f"neznámý source_type {r['source_type']!r}")
    if r["licence"] not in LICENCES:         errs.append(f"neznámá licence {r['licence']!r}")
    if r["self_contained"] not in SELF:      errs.append(f"neznámé self_contained {r['self_contained']!r}")
    if r["recognition"] not in RECOG:        errs.append(f"neznámé recognition {r['recognition']!r}")
    if r["verification"] not in VERIF:       errs.append(f"neznámé verification {r['verification']!r}")
    if not isinstance(r["duration_sec"], (int, float)) or r["duration_sec"] <= 0:
        errs.append("duration_sec musí být kladné číslo")
    elif r["duration_sec"] > 10:
        errs.append(f"duration_sec {r['duration_sec']} > 10 (tvrdý strop) — ulož jen použitelný úsek")
    if not isinstance(r["topics"], list) or not (2 <= len(r["topics"]) <= 5):
        errs.append("topics musí být 2 až 5 položek")
    if not isinstance(r["alt_sources"], list): errs.append("alt_sources musí být pole")
    if not isinstance(r["youtube"], list):
        errs.append("youtube musí být pole (prázdné, když upload neznáš)")
    else:
        for y in r["youtube"]:
            if not isinstance(y, dict) or "url" not in y or "title" not in y:
                errs.append("položka youtube musí být objekt s url a title"); continue
            m = re.fullmatch(r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})(&t=\d+s)?", y["url"])
            if not m:
                errs.append(f"youtube url musí být https://www.youtube.com/watch?v=<11 znaků>[&t=Ns], ne {y['url']!r}")
    # tvrdá pravidla proti tichému omylu
    if r["verification"] == "verified_transcript" and not r["start_time"]:
        errs.append("verified_transcript bez start_time — ověřený řádek musí nést čas")
    if r["verification"] == "unverified" and not r["search_query"]:
        errs.append("unverified bez search_query — editor by neměl co spustit")
    if r["start_time"] and r["verification"] != "verified_transcript":
        errs.append("start_time vyplněn, ale verification není verified_transcript")
    if r["beat"] is not None:
        if not isinstance(r["beat"], dict) or "beat_id" not in r["beat"] or "fits_because" not in r["beat"]:
            errs.append("beat musí být null, nebo objekt s beat_id a fits_because")
    return [f"{where} [{r.get('id','?')}] {e}" for e in errs]

def load(path):
    out = []
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line: continue
        try: out.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"CHYBA {path}:{i} neparsovatelný JSON — {e}"); sys.exit(1)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="zapsat sloučenou knihovnu")
    ap.add_argument("--check", action="store_true", help="jen zvalidovat knihovnu")
    a = ap.parse_args()

    lib = load(LIB) if os.path.exists(LIB) else []
    errs = []
    for r in lib: errs.extend(validate(r, "knihovna"))

    if a.check:
        report(lib, errs, [])
        sys.exit(1 if errs else 0)

    by_id = {r["id"]: r for r in lib}
    by_quote = {norm(r["quote"]): r["id"] for r in lib}
    added, superseded, skipped = [], [], []

    for path in sorted(glob.glob(os.path.join(SHARDS, "*.jsonl"))):
        name = os.path.basename(path)
        for r in load(path):
            e = validate(r, name)
            if e: errs.extend(e); continue
            sup = r.get("beat") and None  # beat nikdy nenese supersedes
            old = r["id"] in by_id
            dup = by_quote.get(norm(r["quote"]))
            if old:
                if r.get("verification") == "verified_transcript" and by_id[r["id"]]["verification"] != "verified_transcript":
                    by_id[r["id"]] = r; superseded.append((name, r["id"], "doplněn čas"))
                else:
                    skipped.append((name, r["id"], "id už v knihovně"))
                continue
            if dup and dup != r["id"]:
                skipped.append((name, r["id"], f"stejná hláška už je jako {dup}"))
                continue
            by_id[r["id"]] = r
            by_quote[norm(r["quote"])] = r["id"]
            added.append((name, r["id"]))

    report(list(by_id.values()), errs, added, superseded, skipped)
    if errs:
        print("\nNic se nezapsalo — nejdřív oprav chyby výše."); sys.exit(1)
    if a.apply:
        with open(LIB, "w", encoding="utf-8") as f:
            for r in by_id.values():
                f.write(json.dumps({k: r[k] for k in KEYS}, ensure_ascii=False) + "\n")
        done = os.path.join(SHARDS, "merged")
        os.makedirs(done, exist_ok=True)
        for p in glob.glob(os.path.join(SHARDS, "*.jsonl")):
            shutil.move(p, os.path.join(done, os.path.basename(p)))
        print(f"\nZapsáno {len(by_id)} řádků do data/soundbites.jsonl; shardy přesunuty do data/shards/merged/.")
        print("Nezapomeň: python3 scripts/render.py")
    else:
        print("\nZkušební běh. Zapíšeš to přidáním --apply.")

def report(rows, errs, added, superseded=(), skipped=()):
    print(f"Řádků celkem: {len(rows)}")
    for label, key in (("Licence", "licence"), ("Ověření", "verification"), ("Seam", "source_type")):
        c = collections.Counter(r.get(key) for r in rows)
        print(f"  {label}: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    if added:      print(f"\nPřibude {len(added)}: " + ", ".join(i for _, i in added))
    if superseded: print(f"Přepíše {len(superseded)}: " + ", ".join(f"{i} ({w})" for _, i, w in superseded))
    if skipped:    print(f"Vynechá {len(skipped)}:\n  " + "\n  ".join(f"{n}: {i} — {w}" for n, i, w in skipped))
    if errs:
        print(f"\n{len(errs)} CHYB:")
        for e in errs: print("  " + e)

if __name__ == "__main__":
    main()
