# Zdroje

Nehledej „funny quotes“. Hledej místa, kde se absurdita zapisuje úředně.

## Tier 1 — federální, public domain, původní zvuk se smí použít

Priorita. Jsou právně čisté **a** neúměrně často samonosné, protože vtip bývá
v tom, že něco absurdního říká úředně někdo úřední.

| Zdroj | URL | Poznámka |
|---|---|---|
| **Oyez** | https://www.oyez.org · API `api.oyez.org` | **Nejlepší zdroj v celém seznamu.** Zvuk synchronizovaný s přepisem, takže dostaneš přesné sekundy i mp3. Viz `verify.md`. |
| Supreme Court | https://www.supremecourt.gov | Zvuk jednání a oficiální přepisy (PDF) |
| govinfo | https://www.govinfo.gov | Slyšení, Congressional Record |
| Sněmovna | https://www.house.gov | Archivy výborů — záznam ber od výboru, ne z C-SPAN |
| Senát | https://www.senate.gov | Archivy výborů |
| National Archives | https://catalog.archives.gov | Film, zvuk, PD; má i přímá média |
| NASA | https://www.nasa.gov · https://apolloinrealtime.org | Zvuk misí. Apollo in Real Time umí skočit na GET. Logo a insignie **nejsou** PD |
| NTSB | https://www.ntsb.gov | Vyšetřování. **CVR zvuk je uzavřený natrvalo** — NTSB ho ze zákona nesmí vydat a copyright drží aerolinka. Přepisy veřejné jsou |
| FAA / LiveATC | řízení letového provozu | Záznamy ATC jsou federální PD a vydávají se. Na rozdíl od CVR |
| American Rhetoric | https://www.americanrhetoric.com | Databáze projevů s mp3. U každé položky ověř, jestli je řeč federální, nebo soukromá |
| CIA Reading Room | https://www.cia.gov/readingroom/ | Odtajněné, převážně dokumenty |

## Tier 2 — archivy a mp3 banky, ověřuj po souboru

| Zdroj | URL | Poznámka |
|---|---|---|
| Internet Archive | https://archive.org | Fulltext i metadata; u položky mp3/ogg ke stažení. `advancedsearch.php?output=json` je použitelné strojově |
| Prelinger | https://archive.org/details/prelinger | Americké výchovné, průmyslové a společenské filmy 1930–70. Kolize rejstříku s moderním tématem **nepotřebuje kulturní paměť** — pro tenhle kanál nejcennější seam |
| Library of Congress | https://www.loc.gov/audio-visual/ · National Jukebox | Nahrávky a film; Jukebox je zlatý důl pro `green_pd_age` |
| LibriVox | https://librivox.org | Předlohy v PD čtené nahlas. LibriVox nahrávky uvolňuje do public domain — ověř u konkrétní. Pozor: je to **moderní čtení**, ne dobový zvuk |
| Public Domain Review | https://publicdomainreview.org | Kurátorované, dobré na dataci |
| Wikimedia Commons | https://commons.wikimedia.org | Licence po souboru. Má i `TimedText` titulky s časy — viz `verify.md` |
| YouTube, filtr Creative Commons | rozšířené hledání | CC BY je komerčně použitelné s uvedením zdroje, ale **kryje jen vlastní obsah videa**, ne cizí hudbu a klipy uvnitř |
| Freesound | https://freesound.org | Zvukové efekty, **ne řeč**. Licence po souboru, CC0 vs CC BY. Použitelné na stingery, ne na hlášky |

## Tier 3 — na nalezení a dataci, ne na zvuk

| Zdroj | URL | K čemu |
|---|---|---|
| YouTube | | **Nejrychlejší náleziště a nejlepší způsob, jak ukotvit čas** (automatické titulky). Není to zdroj souboru — viz níže |
| Know Your Meme | https://knowyourmeme.com | První výskyt, datace, šíření. Výborné na `cultural_background` |
| Wikiquote | https://en.wikiquote.org | Doslovné znění |
| C-SPAN | https://www.c-span.org | Lokátor. Vlastní produkce C-SPAN je červená; pod ní bývá federální feed, ten si vezmi od výboru |
| Reddit | r/todayilearned, r/ObscureMedia, r/DeepIntoYouTube | Stopy |
| Soundboardy | 101soundboards, myinstants, movie-sounds | Na **nalezení** a poslech. Skoro vždy `red_rights_reserved` — zapiš, označ, střihač přemluví |

## YouTube: náleziště ano, zdroj ne

Používej YouTube na tři věci: najít, že klip vůbec existuje; poslechnout si ho;
a vytáhnout z automatických titulků čas.

Master soubor ber vždycky z původního archivu. Tři důvody:

1. **Licence.** Re-upload nemá práva, která předstírá. Federální PD se váže
   k původní nahrávce, ne k tomu, že ji někdo nahrál na YouTube.
2. **Kvalita.** Re-uploady bývají překódované, ustřižené a s vypálenou grafikou.
3. **Pravidlo kanálu.** `docs/01-AUTORSKA-PRAVA.md` to říká natvrdo: zdrojový
   soubor se bere z původního archivu, ne z YouTube ripu.

Stahování z YouTube je navíc proti podmínkám služby. Skript
`scripts/yt_timestamp.py` proto tahá jen titulky, ne video, a slouží k navigaci.

## Strategie hledání, které fungují

1. **Grepuj přepisy na smích.** SCOTUS a Kongres ho značí doslova: `(Laughter)`,
   `[Laughter]`. Hledej `site:oyez.org "(Laughter)"` a čti, co tomu předchází.
2. **Slyšení plus téma, kterému panel nerozumí.** Technologie, šifrování, sociální
   sítě, krypto, AI. Vzorec: `congressional hearing "senator" viral moment [téma] transcript`
3. **Pojmenovaný virál, pak zpátky k primárnímu zdroji.** Začni na Know Your Meme
   kvůli dataci, pak dohledej archivní upload.
4. **Prelinger po tématech.** `site:archive.org prelinger [téma] narration` —
   etiketa, hygiena, civilní obrana, autoškola, chování v kanceláři, randění,
   atomová bezpečnost.
5. **Kampaně agentur.** Civilní obrana, CDC, USDA, Forest Service, FCC. Úřední
   absurdita na metry — ale nejdřív si přečti zřizovací zákon, viz past níž.
6. **Soudní zvuk v podivných kauzách.** Spory o ochranné známky, značení potravin,
   obscénnost, právo na zvířata. Přepisy jsou plné úředníků, kteří s vážnou tváří
   rozebírají nesmysl.
7. **Uploady „full hearing“ s kapitolami.** Kapitoly dávají skutečné časy, které
   jsi nemusel hádat.

## Licenční pasti, které knihovnu už jednou stály chybu

- **Smokey Bear není public domain.** Smokey Bear Act z roku 1952 ho z PD
  výslovně vyňal a svěřil ministru zemědělství (16 U.S.C. § 580p).
- **Woodsy Owl je tvrdší.** 18 U.S.C. § 711a kriminalizuje komerční užití postavy,
  jména **i sloganu**. Přemluvení nepomůže, statut sahá na ta slova.
- **Protidrogové PSA nejsou vládní.** „This is your brain on drugs“ i „I learned
  it by watching you“ dělala Partnership for a Drug-Free America, soukromá
  nezisková organizace.
- **Kdo nahrával ≠ kdo mluvil.** Zvuk „series of tubes“ pořídilo Public Knowledge.
  Jednání veřejné, nahrávka soukromá.
- **První dáma není federální zaměstnankyně.** U projevu prezidenta je § 105
  jasný, u projevu první dámy ne.

Pravidlo, které z toho plyne: **nic není federální jen proto, že to federálně
vypadá.** Vždycky zřizovací zákon.
