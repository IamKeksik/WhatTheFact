# What The Fact

Anglický YouTube kanál pro americký trh. Krátké explainery o amerických
pravidlech, institucích a věcech, které všichni znají a nikdo nechápe.

Formát: **animovaný whiteboard bez kreslící ruky, 8–10 minut, 1× týdně.**

---

## Dokumentace

| Dokument | Co v něm je |
|---|---|
| [RESEARCH.md](RESEARCH.md) | Průzkum trhu podle AOY — rozbor referenčního formátu, benchmark US kanálů, pravidla pro titulky, dostupnost handlu, pozice kanálu |
| [docs/01-AUTORSKA-PRAVA.md](docs/01-AUTORSKA-PRAVA.md) | Co smíš a co ne. Proč „trochu to pozměním" nefunguje a proč je whiteboard výhoda |
| [docs/02-ZDROJE.md](docs/02-ZDROJE.md) | Knihovna zdrojů podle licenčního rizika — zelená / žlutá / červená |
| [docs/03-KNIHOVNA-HLASEK.md](docs/03-KNIHOVNA-HLASEK.md) | Hlášky a momenty pro cutaway. Náhrada archivu, na kterém stojí originál |
| [docs/04-VIDEA-01-30.md](docs/04-VIDEA-01-30.md) | 36 videí v šesti pilířích — titulky, premisa, loop, metafora, otočka, thumbnaily, cutaway assety |
| [docs/05-VIZUALNI-STYL.md](docs/05-VIZUALNI-STYL.md) | Paleta, tah, opakující se postava, thumbnail systém, struktura dílu |
| [docs/06-ROZBOR-FORMATU.md](docs/06-ROZBOR-FORMATU.md) | Rozbor tří dílů referenčního pořadu s 18× rozptylem — co dělá dobře, co špatně, a osmibodový checklist pro každý díl |
| [docs/07-METODIKA.md](docs/07-METODIKA.md) | Podle čeho se vybírá téma a titulek — pět filtrů, čtyři pravidla, data na 15 dílech a jejich limity |
| [prompts/SBER-HLASEK.md](prompts/SBER-HLASEK.md) | Prompt do samostatného chatu na průběžný sběr hlášek. Vynucuje časově ukotvený odkaz na audio, délku, kulturní kontext a licenci — bez nich se položka nezapisuje |
| [docs/knihovna.html](docs/knihovna.html) | **Prohledatelná knihovna** — hlášky i videa v jedné stránce, filtr podle licence a hledání. [Publikovaná verze](https://claude.ai/code/artifact/7ee5ea1d-5326-4c94-8392-d8b44670518e) |

---

## Tři pravidla, na kterých kanál stojí

**1. Pointa musí být doslovně pravda.**
Nejsilnější gag formátu je vtip s razítkem federálního předpisu. Každý díl má
v [04](docs/04-VIDEA-01-30.md) sloupec *Ověř* — dokud není odškrtnutý, scénář
se nepíše.

**2. Žádný cutaway bez licenčního stavu.**
Každá položka v [03](docs/03-KNIHOVNA-HLASEK.md) má značku 🟢/🟡/🔴. Nemá-li ji,
do videa nejde. Zdrojový soubor se bere z původního archivu, ne z YouTube ripu.

**3. Titulek je konkrétní anomálie a předmětem je divák.**
„How does X work?“ prohraje se search giganty. A v referenčním pořadu platí, že kde
je předmětem titulku divák sám, výsledek je řádově vyšší — „Proč **nemáme** rádi
církev“ 313 K vs „Jak vzniklo očkování“ 18 K. Data v
[06-ROZBOR-FORMATU.md](docs/06-ROZBOR-FORMATU.md), benchmark v [RESEARCH.md](RESEARCH.md).

---

## Stav

- [x] Průzkum trhu a referenčního formátu
- [x] Právní režim cutawayů
- [x] Knihovna zdrojů
- [x] Startovní knihovna hlášek
- [x] 36 videí — titulky, struktura a thumbnaily
- [x] Metodika výběru témat a titulků
- [x] Rozbor formátu — co referenční pořad dělá dobře a co špatně
- [x] Vizuální systém
- [ ] Handle ověřený v YouTube Studiu (`@whatthefacttv`, záloha `@whatthefactusa`)
- [ ] Sběr produkční knihovny hlášek (prompt hotový, běh na operátorovi)
- [ ] Scénář dílu 01
- [ ] Vizuální identita — postava, thumbnail šablona
- [ ] Díl 01 nahraný

Doporučený pilotní díl: **D6 — Duck and Cover.** Jediný z třiceti, kde je celý
archivní film v public domain, takže nejmenší produkční i právní riziko.
Zdůvodnění v [04](docs/04-VIDEA-01-30.md).
