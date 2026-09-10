# Schéma řádku

Jeden JSON objekt na řádek, **všech 25 klíčů vždy přítomných**. Validuje
`scripts/merge.py`; co neprojde, se do knihovny nedostane.

```json
{
  "id": "stevens-series-of-tubes",
  "quote": "It's not a big truck. It's a series of tubes.",
  "quote_verbatim": true,
  "speaker": "Sen. Ted Stevens (R-AK)",
  "source_title": "Senate Commerce Committee markup on net neutrality",
  "source_type": "congressional_hearing",
  "year": 2006,
  "audio_url": "https://www.youtube.com/watch?v=VIDEO_ID&t=317s",
  "audio_url_type": "youtube_timestamp",
  "start_time": "00:05:17",
  "duration_sec": 5,
  "duration_estimated": true,
  "context_before": "Co zaznělo těsně předtím.",
  "context_after": "Co následuje, ať střihač ví, kde uříznout.",
  "cultural_background": "Proč to Američan pozná. Kdy to vstoupilo do kultury, jak široce, čeho je to zkratka.",
  "why_it_lands": "Mechanismus. Je absurdita uvnitř věty, v přednesu, nebo v ironii toho, kdo to říká?",
  "self_contained": "yes",
  "licence": "yellow_verify",
  "licence_note": "Co přesně ověřit a proč.",
  "topics": ["regulátoři, co nechápou, co regulují", "internetová infrastruktura"],
  "verification": "unverified",
  "verification_note": "Odkud pochází znění, co se nepodařilo ověřit a proč.",
  "search_query": "Co má střihač spustit, aby to našel.",
  "alt_sources": ["https://knowyourmeme.com/memes/series-of-tubes"],
  "beat": null
}
```

## Proti falšování

Tyhle body přebíjejí všechno ostatní. Když je porušíš, je nepoužitelná celá
knihovna, protože střihač nepozná dobré řádky od špatných.

1. **Nikdy nevymýšlej ID videa na YouTube.** Použij jen ID, které jsi skutečně
   viděl ve výsledku hledání nebo na stránce, kterou jsi otevřel.
2. **Nikdy nevymýšlej čas.** `start_time` vyplň jen z přepisu s časy, ze stránky,
   která ho uvádí, z kapitoly, z popisku, z komentáře citujícího čas, nebo ze
   zdroje typu Oyez, který synchronizuje text se zvukem. Jinak `null`.
3. **Nikdy nehádej délku.** Když ji neznáš, odhadni z počtu slov (zhruba 2,5 slova
   za sekundu) a nastav `duration_estimated: true`.
4. **Cituj doslova.** Máš-li jen parafrázi, `quote_verbatim: false` a v poznámce
   napiš, odkud znění pochází.
5. **Nejistotu zapiš do řádku.** Řádek označený jako nejistý je užitečný.
6. **Netvrď, že jsi zvuk poslouchal.** To neumíš. `verified_transcript` jen tehdy,
   když čas uvádí přepis nebo stránka; jinak `unverified`.

## Pravidla polí

**`self_contained`** — nejdůležitější klasifikace. Střihač není Američan a sám
neposoudí, jestli vtip sedne.

- `yes` — vtipné nebo úderné pro někoho, kdo to nikdy neslyšel. Absurdita je
  uvnitř věty. *(„It's a series of tubes.“)*
- `partial` — funguje samo, se znalostí zdroje je to silnější.
- `memory_dependent` — humor žije ve vzpomínce na scénu. **Zapisuj, ale je to
  nízká priorita.** V `why_it_lands` napiš natvrdo, co musí posluchač znát předem.

**`licence`**

- `green_federal_pd` — dílo federální vlády USA, 17 U.S.C. § 105, komerčně
  použitelné. Slyšení výborů nahraná výborem, zvuk jednání SCOTUS, filmy a PSA
  federálních agentur, NASA, NTSB, FAA. **Původní zvuk se smí použít.**
- `green_pd_age` — vydáno 1930 a dřív (zvukové nahrávky 1925 a dřív).
- `yellow_verify` — nejspíš volné, ale ověřuje se po souboru. Většina Prelinger
  kolekce: zhruba 65 % je public domain, ne všechno. Hledej Public Domain Mark
  nebo CC0 v metadatech položky a zapiš, cos našel.
- `red_rights_reserved` — filmy, TV, zpravodajství, sport, komerční hudba, vlastní
  produkce C-SPAN, uživatelské uploady. Původní zvuk použít nelze. **Řádek stejně
  zapiš** — text krátké fráze není chráněný (37 C.F.R. § 202.1), takže se dá
  přemluvit. Napiš to do `licence_note`.

Výjimka, na kterou se naletí: u Woodsyho Owla je chráněný i slogan
(18 U.S.C. § 711a). Tam přemluvení nepomůže. Takové případy patří do
`licence_note` velkými písmeny.

**`source_type`** — jedno z: `congressional_hearing`, `scotus_argument`,
`court_audio`, `federal_psa`, `prelinger_film`, `pd_film`, `local_news`,
`youtube_viral`, `city_council`, `radio`, `podcast`, `speech`, `film`, `tv`,
`advertisement`, `other`.

**`duration_sec`** — cíl 1–8. Tvrdý strop 10. Delší se do formátu nevejde;
buď to zahoď, nebo zapiš jen použitelný úsek.

**`topics`** — 2 až 5 tagů běžnou řečí, pojmenovávajících témata explaineru, které
by klip mohl přerušit. Takhle to bude střihač hledat, takže buď konkrétní a
štědrý: ne `politika`, ale `regulátoři, co nechápou, co regulují`.

**`beat`** — `null` v režimu široké těžby. V režimu lovu ke scénáři objekt:

```json
"beat": {
  "beat_id": "b04",
  "beat_timecode": "00:03:10",
  "fits_because": "Narace tady tvrdí, že pravidlo psali lidé, co produkt nikdy neviděli. Tahle věta to dokládá z první ruky.",
  "rank": 1
}
```

`rank` 1 je první volba, 2 a 3 jsou náhrady. Ke každému beatu měj aspoň dva
kandidáty — první volba často padne na licenci.

## Vztahy mezi poli, které validátor vynucuje

- `verified_transcript` ⇒ `start_time` není `null`. Ověřený řádek bez času je
  protimluv.
- `unverified` ⇒ `search_query` není `null`. Jinak by střihač neměl co spustit.
- `start_time` vyplněn ⇒ `verification` je `verified_transcript`.
- `duration_sec` ≤ 10.
- `topics` má 2 až 5 položek.
- `id` je kebab-case a v knihovně unikátní; unikátní musí být i normalizované
  znění hlášky (malá písmena, bez interpunkce).

## Nahrazení lepším zdrojem

Našel-li jsi k existující položce lepší zdroj — skutečný čas tam, kde nebyl, nebo
PD tam, kde bylo červené — zapiš ji znovu se stejným `id` a do
`verification_note` napiš proč. `merge.py` přepíše původní řádek jen tehdy, když
nový nese `verified_transcript` a starý ne.

## Laťka kvality — raději zahoď, než nafukuj

Nezapisuj: nedohledatelný zvuk; nad 10 sekund bez použitelného úseku; větu tak
obecnou, že nic nepodtrhne; hudbu bez mluveného slova; cokoli, co neumíš připsat
jmenovanému zdroji a roku.

**Dávka osmi solidních řádků je lepší než dávka třiceti, kde má dvacet vymyšlený čas.**
