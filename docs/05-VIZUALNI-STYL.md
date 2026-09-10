# Vizuální styl — animovaný whiteboard bez ruky

Rozhodnutí vypustit kreslící ruku je správné, ale mění to jednu podstatnou věc:
**ruka je to, co drží pozornost při kreslení.** Bez ní musí tempo držet něco
jiného, jinak vznikne statická tabule s voiceoverem.

Čím to nahradit:

| Bez ruky chybí | Náhrada |
|---|---|
| Pohyb během kreslení | **self-drawing stroke** — tah se vykresluje sám, 0,4–0,8 s na objekt |
| Vedení oka po tabuli | **kamera** — pomalý pan a zoom mezi bloky, nikdy skok |
| Rytmus | **jeden objekt = jedna myšlenka**, objekt zmizí, když myšlenka skončí |
| Osobnost | **opakující se postava** (viz níž) |

---

## Paleta

Tři barvy. Víc ne — čtvrtá barva ubere červené její funkci.

| Role | Barva | Použití |
|---|---|---|
| Podklad | téměř bílá, `#F7F5F0` | ne čistě bílá — na OLED bije do očí |
| Tah | téměř černá, `#1A1A1A` | veškerá kresba a text |
| Akcent | jedna červená, `#E03131` | **max 1 objekt na obrazovku** |

Červená je nejcennější prvek celého systému. Označuje **to jedno místo, kam se
má divák podívat**. Když je červené všechno, není červené nic.

Šedou (`#9A9A9A`) povol jen na potlačení už vysvětleného objektu, aby zůstal
v rámu, ale netáhl pozornost.

---

## Tah

- **Ne perfektní vektor.** Mírně nepravidelná linka čte jako ručně kreslené.
  Perfektní kruh čte jako PowerPoint.
- Šířka tahu 3–5 px při 1080p, jednotná.
- Objekt se vykresluje **od hlavního obrysu k detailu**, ne shora dolů.
- Popisky písmem s ručním charakterem, ale **čitelným na mobilu** — otestuj
  na 400 px šířky, tam se video dívá většina lidí.

---

## Opakující se postava

Původní formát řeší rytmus cutawayem do archivu. Ty archiv nevlastníš — ale máš
kresbu, takže si můžeš vytvořit **něco, co ti nikdo nezablokuje**.

Jedna figura, která vpadává do výkladu s reakcí. Nekomentuje fakta — **reaguje
na absurditu**. To je celá její funkce.

Požadavky:
- rozeznatelná v thumbnailu na 120 px
- 4–6 fixních výrazů (skepse, šok, nezájem, souhlas, panika, únava)
- žádná mluvená replika delší než 5 slov
- **nikdy to nesmí být existující chráněná postava** — detail v [01-AUTORSKA-PRAVA.md](01-AUTORSKA-PRAVA.md)

---

## Cutaway rytmus

Motor formátu. V analyzovaném dílu původního pořadu vpadne komediální střih
**každých 45–60 sekund** — bez toho je z výkladu předčítaná encyklopedie
(rozbor v [RESEARCH.md](../RESEARCH.md)).

Tři vrstvy, aby se to za deset dílů neokoukalo:

| Vrstva | Co to je | Kde brát |
|---|---|---|
| 1 | **Archivní záběr** — padesátkový PSA nebo groteska, PD | [02-ZDROJE.md](02-ZDROJE.md) 🟢/🟡 |
| 2 | **Skutečná hláška** — citace ze slyšení, soudu, zpravodajství | [03-KNIHOVNA-HLASEK.md](03-KNIHOVNA-HLASEK.md) |
| 3 | **Vlastní postava** — tvoje reakční figura | vlastní |

**Střídej je.** Dva stejné typy cutawaye za sebou zabíjejí efekt.

**Jak vypadá vrstva 1 ve whiteboard stylu:** archivní záběr nedávej naplocho do
kompozice. Vlož ho jako **obraz na tabuli** — rámeček nakreslený tahem, uvnitř
záběr, případně odbarvený do dvou tónů, aby ladil s paletou. Tím je součástí
světa videa, ne cizí vsuvkou.

**Jak vypadá vrstva 2:** hláška se **napíše na tabuli** a zároveň řekne. Text
krátké fráze není chráněný, takže tohle je zdarma i tam, kde je klip zakázaný
(🔴 položky v knihovně).

---

## Thumbnail systém

Konzistence je tady povinná, ne volitelná: jméno „What The Fact" je na EN YouTube
marker komoditního fact-kanálu, takže **odlišení musí přijít z vizuálu**
(viz [RESEARCH.md § 5](../RESEARCH.md)).

Pevná pravidla pro všechny thumbnaily:

1. **Jeden hlavní kreslený objekt.** Ne scéna. Jeden objekt.
2. **Max 4 slova textu.** Velká, tučná, čitelná na 120 px.
3. **Jedna červená věc.** Vždy ta, o které je video.
4. **Text nesmí opakovat titulek.** Titulek řekne co, thumbnail řekne pointu.
5. **Postava vpravo dole**, malá, s jedním výrazem. Buduje rozeznatelnost série.
6. **Podklad = ta samá tabule.** Napříč všemi díly. To je ta vizuální linka.

Test: dej 6 svých thumbnailů mezi 20 cizích, zmenši na 120 px. Když nepoznáš,
které jsou tvoje, systém nefunguje.

---

## Délka a struktura dílu

Podle benchmarku (viz [RESEARCH.md](../RESEARCH.md)) je 8–10 minut jediné okno,
kde krátký explainer v angličtině ještě vyhrává.

| Blok | Čas | Obsah |
|---|---|---|
| Hook | 0:00–0:30 | obraz → obrat; **žádné intro, žádné logo** |
| Data punch | 0:30–2:00 | tvrdé číslo nebo citace předpisu hned |
| Jádro | 2:00–7:30 | 3–4 bloky, mezi každými cutaway |
| Payoff | 7:30–8:45 | jak to spolu souvisí; **změna perspektivy** |
| CTA | 8:45–9:15 | otázka do komentářů + odkaz na starší díl |

Intro sekvence patří do roku 2015. Prvních 5 sekund rozhoduje o retenci.
