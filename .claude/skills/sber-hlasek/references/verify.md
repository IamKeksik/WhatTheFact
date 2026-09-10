# Jak reálně získat čas

Většina řádků v knihovně je `unverified`, protože ověření je ta pracná část.
Tady jsou cesty, které fungují, seřazené od nejlepší.

## 1. Oyez API — přesné sekundy a mp3 (jen SCOTUS)

Oyez má nezdokumentované veřejné API. Přepis nese u každého bloku řeči pole
`start` a `stop` v sekundách, na konci je `media_file` s odkazy na mp3, ogg a
m3u8 na S3. To je v celé knihovně jediný zdroj, který dá offset do konkrétního
souboru.

```
python3 scripts/oyez_timestamp.py --case 2006/06-593 --phrase footman
python3 scripts/oyez_timestamp.py --url https://www.oyez.org/cases/2006/06-593 --phrase "footman" --json
```

`--json` vypíše rovnou náplast do řádku: `audio_url`, `start_time`,
`duration_sec`, `duration_estimated: false`, `verification: "verified_transcript"`.

Dvě upozornění. Délka bloku je délka **celé repliky**, ne jen tvé věty — pokud je
delší než 10 sekund, `duration_sec` zkrať na použitelný úsek. A hledej krátce,
klidně jedno slovo: přepis se od citace v článcích liší interpunkcí.

Term je rok začátku období, ne rok jednání: případ souzený v dubnu 2007 spadá pod
term 2006.

## 2. Automatické titulky YouTube

Funguje na cokoli, co na YouTube je, tedy skoro na všechno.

```
python3 scripts/yt_timestamp.py --video 6w5sfAyxmFk --phrase "series of tubes"
```

Vrátí čas a hotovou `&t=` URL. Potřebuje `yt-dlp` v PATH (`pip install yt-dlp`).
Skript stahuje **jen titulky**, ne video.

Automatické titulky komolí jména a interpunkci, takže hledej krátký úsek bez
vlastních jmen. Čas ber jako navigaci na vteřinu, ne na snímek.

**`verification: "verified_transcript"` z automatických titulků zapiš jen tehdy,
když si to poslechem potvrdíš.** Jinak nech `unverified` a do `search_query` dej
hotovou `&t=` URL — to je pro střihače pořád obrovský posun.

A pořád platí: `audio_url` může na YouTube ukazovat kvůli navigaci, ale master
soubor se bere z původního archivu.

## 3. Wikimedia Commons TimedText

U videí na Commons bývají titulky jako samostatná stránka `TimedText:<soubor>.en.srt`
s časovými značkami. Například Duck and Cover má takový soubor. Otevři ho a
odečti cue time.

## 4. Kapitoly a popisky u „full hearing“ uploadů

Dlouhé záznamy slyšení mívají v popisku nebo v kapitolách rozpis časů podle
tazatelů. To je skutečný čas, který jsi nemusel hádat — a často stačí, protože
kolo jednoho kongresmana trvá pět minut.

## 5. Přepis s číslem stránky, pak dopočet

Oficiální PDF přepisy SCOTUS a Kongresu nemají časy, mají čísla stránek. Na čas
to nepřeváděj odhadem — to už je vymýšlení. Použij je na ověření **znění**
a čas získej jinou cestou.

## Co dělat, když ověření neprojde

V prostředí s omezeným egressem (Claude Code na webu) jsou Oyez, archive.org,
YouTube i govinfo blokované. Pak:

- `start_time: null`
- `verification: "unverified"`
- `verification_note` napiš, cos ověřil a co ne, a proč
- `search_query` napiš tak, aby se dal spustit **beze změny** — konkrétní dotaz,
  konkrétní stránka, konkrétní místo v souboru

Špatně: `najít na YouTube`.
Dobře: `archive.org/details/HabitPat1954 — je to první věta filmu, do 30 sekund; v metadatech zkontroluj Public Domain Mark`.

## Dávkové doplnění časů

Když je knihovna hotová a máš síť, projeď SCOTUS řádky jedním během:

```
python3 - <<'EOF'
import json, subprocess
for l in open("data/soundbites.jsonl"):
    r = json.loads(l)
    if r["source_type"] == "scotus_argument" and r["verification"] == "unverified":
        print("\n===", r["id"], "—", r["quote"][:60])
        print("   ", r["search_query"])
EOF
```

Vypíše ti seznam, co dohledat, včetně připravených dotazů. Pak na každý pusť
`oyez_timestamp.py` a doplněné řádky zapiš do `data/shards/oyez-doplneni.jsonl`
a slouč — `merge.py` je pozná podle `id` a přepíše původní verzi, protože nesou
`verified_transcript`.
