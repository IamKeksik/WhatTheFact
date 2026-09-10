---
name: sber-hlasek
description: Sběr krátkých amerických zvukových hlášek (soundbitů) na cutaway pro kanál What The Fact — do knihovny data/soundbites.jsonl. Umí dva režimy: široká těžba nového materiálu paralelními agenty, a cílený lov k hotovému scénáři, kdy se hlášky hledají na konkrétní beaty. Použij, když má někdo najít, ověřit nebo doplnit hlášky, časy, licence, nebo když se ptá „co se hodí k tomuhle scénáři“.
---

# Sběr hlášek

Knihovna je `data/soundbites.jsonl` — jeden JSON objekt na řádek, 27 klíčů,
schéma v `references/schema.md`. Prohlížečka je `docs/soundbites.html`.

Kanál střihne 1–8sekundový klip každých 45–60 s, aby zlomil rejstřík formální
narace. Hledáš přesně tohle a nic jiného. Nepíšeš scénáře, neradíš — vyrábíš data.

## Co hledáš především

**Divák to má poznat.** Hláška, kterou Američan zná z filmu, seriálu, reklamy nebo
virálu, funguje dvakrát: jednou obsahem věty a podruhé tím, že si posluchač
vzpomene. To je hlavní ložisko a začíná se u něj.

Pořadí priorit:

1. **Kultovní film, seriál, animák** — SpongeBob, Simpsonovi, Anchorman, hlášky,
   které lidé citují mezi sebou.
2. **Virály** — Vine, YouTube, TikTok. Nejvyšší rozpoznatelnost u publika pod 35.
3. **Reklamní slogany, které přeskočily do běžné řeči** — „Where's the beef?“,
   „I've fallen and I can't get up“.
4. **Lokální zprávy a bizarní segmenty**, které se staly memem.
5. **Kongres a soudy** — teprve tady, a jen momenty, které se skutečně rozšířily.
6. **Prelinger a federální archiv** — nejnižší priorita. Právně čisté, ale skoro
   nic z toho nikdo nezná. Ber odsud jen to, co je vtipné samo o sobě.

Pole `recognition` (`universal` / `high` / `niche`) tuhle osu měří a je stejně
důležité jako `self_contained`. **Dávka, ve které je většina řádků `niche`, je
špatná dávka**, i kdyby byla právně bez chybičky.

**Licenci neřeš.** Zadavatel rozhodl, že se na ni nebere ohled. Pole `licence`
vyplň mechanicky `red_rights_reserved`, `licence_note` nech prázdné a nevybírej
podle toho, co zapsat. Rozpoznatelnost rozhoduje, licence ne.

## Nejtvrdší pravidlo

**Položka bez funkčního, časově ukotveného odkazu na skutečný zvuk je bezcenná.**
Střihač musí kliknout, do pár vteřin hlášku slyšet a vzít si ji.

Když to nejde, máš dvě možnosti a žádnou třetí: buď `verification: "unverified"`
plus konkrétní `search_query`, co má střihač spustit, nebo položku vůbec nezapsat.
Knihovnu nenafukuj.

**Existuje-li k hlášce upload na YouTube, který jsi viděl, zapiš ho do pole
`youtube`** — vždycky, i když `audio_url` míří na archiv. Střihač chce na video
kliknout a poslechnout si to. Kanonický tvar `watch?v=<11 znaků>`, ideálně rovnou
s `&t=Ns` z `scripts/yt_timestamp.py`. Validátor jiný tvar nepustí.

**Nikdy si nevymýšlej ID videa, čas ani délku.** Detailní zákazy v
`references/schema.md`, sekce „Proti falšování“. Řádek označený jako nejistý je
užitečný. Řádek tiše špatný je jed — střihač pak nepozná dobré od špatných
a zahodí celý soubor.

## Dva režimy

### A — široká těžba

Doplňuješ knihovnu novým materiálem bez ohledu na konkrétní díl. Rotuješ území,
aby knihovna zůstala široká. Tohle je výchozí režim.

### B — lov ke scénáři

Na vstupu je hotový scénář dílu. Odvodíš z něj beaty a hledáš cíleně, co se hodí
na každý z nich. Výstup není jen knihovna, ale **cue sheet** — beat → dva až tři
seřazení kandidáti, aby měl střihač náhradu, když první nevyjde.

Postup:

1. **Rozsekej scénář na beaty.** Když nese timecody, použij je. Když ne, počítej
   naraci na ~150 slov za minutu a udělej řez každých 45–60 s. Každý beat dostane
   `beat_id` (`b01`, `b02`, …) a čas.
2. **Ke každému beatu napiš hunt brief**, tři až pět vět: jaký rejstřík se má
   zlomit, o čem beat je, kam se otáčí, a tři až pět konkrétních vyhledávacích
   záměrů. Ne „něco vtipného o daních“, ale „úředník IRS pod přísahou vysvětluje,
   proč je formulář srozumitelný“.
3. **Rozděl beaty mezi agenty** po třech až pěti a pusť je paralelně (níže).
4. **Zapiš řádky s vyplněným polem `beat`** — `beat_id`, `beat_timecode`,
   `fits_because` (proč sedí právě sem), `rank` (1 je první volba).
   Hlášky, které jsou v knihovně už teď, se do cue sheetu jen odkazují přes `id`;
   nekopíruj je znovu.
5. **Nakonec vyskládej cue sheet** — tabulka beat → kandidáti → licence → co
   dohledat. To je věc, kterou střihač reálně otevře.

Beat pole nesmí nahradit ostatní: řádek pořád musí projít validátorem, tedy nést
licenci, délku i stav ověření. Hláška, která se hodí k beatu a nemá dohledatelný
zvuk, je pořád nepoužitelná.

## Paralelní běh — pět agentů

Fan-out dává smysl, protože úzké hrdlo je počet webových hledání, ne přemýšlení.
Pět agentů zkrátí těžbu zhruba pětkrát. **Neurychlí ověřování**, pokud je síť
omezená — subagenti dědí stejnou egress politiku jako ty.

Než něco pustíš, přečti `data/TERRITORIES.md` — co je vytěžené a co si kdo drží.

**Duplicitám se předchází rozdělením území, ne kontrolou na konci.** Agenti na
sebe nevidí a svoje řádky si navzájem nepřečtou. Proto každý dostane území, které
se s ostatními nepřekrývá — jiný seam, jiné období, jiná tematická osa.

Každému agentovi v zadání předej:

- **jeho území** a výslovný zákaz vyjet mimo ně,
- **cestu k jeho shardu**: `data/shards/<uzemi>.jsonl`, kam píše a nikam jinam,
  hlavně ne do `data/soundbites.jsonl`,
- **schéma** — ať si přečte `references/schema.md`, celé, než napíše první řádek,
- **seznam `id`, která už v knihovně jsou** pro jeho seam (vyfiltruj mu je),
- **cílový počet** 8–15 řádků a pokyn raději vrátit šest dobrých než třicet,
  z nichž dvacet má vymyšlený čas.

Po doběhnutí:

```
python3 scripts/merge.py            # zkušební běh: co přibude, co se vynechá, co je špatně
python3 scripts/merge.py --apply    # sloučí, přesune shardy do data/shards/merged/
python3 scripts/render.py           # přegeneruje docs/soundbites.html
```

`merge.py` je jediné místo, kde se kontroluje schéma a řeší duplicity. Hlídá i
shodu normalizovaného znění hlášky, takže chytí i tutéž větu nalezenou dvěma
cestami. Když jeden agent přinese k existujícímu `id` skutečný čas, přepíše
původní řádek — to je jediné povolené přepsání.

Území, která se neperou (rozvrh na jeden běh):

| Agent | Území |
|---|---|
| 1 | Kultovní film — jeden žánr nebo dekáda, hlášky, které lidé citují mezi sebou |
| 2 | Seriály a animace — SpongeBob, Simpsonovi, sitcomy |
| 3 | Virály — Vine, YouTube, TikTok, jedno období |
| 4 | Reklamní slogany, které přeskočily do běžné řeči |
| 5 | Kongres, soudy a archiv — jen momenty, které se skutečně rozšířily |

Rotuj je mezi běhy, ať se knihovna nevykloní k jednomu seamu.

## Ověřování — jak reálně získat čas

Tohle je nejcennější část práce a většina řádků ji potřebuje. Recepty jsou
v `references/verify.md`. Ve zkratce:

- **Oyez API** dává u SCOTUS přesné sekundy a přímé mp3.
  `python3 scripts/oyez_timestamp.py --case 2006/06-593 --phrase footman`
- **YouTube automatické titulky** ukotví čas u čehokoli, co je na YouTube.
  `python3 scripts/yt_timestamp.py --video 6w5sfAyxmFk --phrase "series of tubes"`
  YouTube je **náleziště, ne zdroj souboru** — master ber z původního archivu.
- **Archive.org** má u položky vlastní přehrávač a často přepis nebo titulky.

Oba skripty potřebují síť. V sandboxu s omezeným egressem neprojdou; pak zapiš
`unverified` a `search_query` a ověření nech na běh mimo sandbox.

## Zdroje

Tiery zdrojů jsou v `references/sources.md`. Postup, který funguje nejlíp:
vlákno na Redditu vybere kandidáty → Know Your Meme dá dataci a znění → přepis
na Fandomu nebo IMDb ověří doslovnost → YouTube ukotví čas.

## Výstup do chatu

Po každé dávce vypiš tři věci a hned pokračuj další dávkou, bez ptaní:

1. jednořádkové ohlášení území — `DÁVKA 7 — SCOTUS, potravinové značení`,
2. řádky JSONL v jednom code fence,
3. přehledovou tabulku `| id | hláška (60 znaků) | rok | délka | samonosnost | licence |`
   a tři řádky: `VYTĚŽENO:` / `DALŠÍ:` / `VYČERPÁNO:`.

Sběr běží, dokud operátor nenapíše `STOP`.
