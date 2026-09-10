#!/usr/bin/env python3
"""Vygeneruje docs/soundbites.html z data/soundbites.jsonl.

    python3 scripts/render.py
"""
import json, html, collections

import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,"data","soundbites.jsonl")
OUT=os.path.join(ROOT,"docs","soundbites.html")
TPLP=os.path.join(ROOT,"scripts","soundbites.tpl.html")
rows=[json.loads(l) for l in open(SRC) if l.strip()]

SEAM={
 "film":("FILM","Kultovní filmové hlášky","Nejvyšší rozpoznatelnost vůbec. Věty, které Američan pozná z první slabiky a často je i sám používá."),
 "youtube_viral":("VIRÁL","Virály, Vine a YouTube","Nejvyšší rozpoznatelnost v celé knihovně. Skoro vždy červené — text se přemluví, scéna překreslí. Přesně na tohle je whiteboard stavěný."),
 "tv":("SERIÁL","Kultovní seriály a animace","Hlášky, které Američan pozná z první slabiky. Práva hlídají studia agresivně, ale krátká fráze chráněná není."),
 "scotus_argument":("SCOTUS","Nejvyšší soud — ústní jednání","Přepisy značí smích slovem „(Laughter)“. Federální PD, ale bez přístupu k Oyez z tohoto prostředí nejde ukotvit čas — všechny řádky nesou dohledávací dotaz."),
 "congressional_hearing":("KONGRES","Slyšení Kongresu","Nejúrodnější seam. Záznam výboru je federální dílo; ripy z YouTube a C-SPAN slouží jen k nalezení místa."),
 "prelinger_film":("PRELINGER","Výchovné a společenské filmy","Nejvyšší podíl hlášek srozumitelných bez americké paměti. Zároveň nejvíc práce s licencí — PD je zhruba dvoutřetinová, ověřuje se po souboru."),
 "federal_psa":("PSA","Federální kampaně","Pozor: dvě nejfederálnější maskoti země jsou nejméně použitelné. Detail v licenčních poznámkách."),
 "advertisement":("REKLAMA","Reklamní slogany a kampaně","Slogany, které přeskočily z televize do běžné řeči. Pozor na ochranné známky, ne jen na autorská práva."),
 "speech":("PROJEV","Projevy z Bílého domu","Prezidentova část je federální dílo. U první dámy to jednoznačné není."),
 "local_news":("LOKÁLKA","Lokální zprávy — virály","Vše červené: záznam patří stanici. Text se přemluví, scéna překreslí."),
 "radio":("RÁDIO","Rádio","Mluvené slovo z éteru — spoty, moderátoři, přenosy."),
 "podcast":("PODCAST","Podcasty","Novější seam. Rozpoznatelnost bývá vysoká u úzkého publika."),
 "court_audio":("SOUD","Soudní záznamy mimo SCOTUS","Nižší soudy, kde se úředně rozebírá nesmysl."),
 "city_council":("RADNICE","Zastupitelstva","Pozor na soukromé osoby a pranky."),
 "pd_film":("PD FILM","Starý film","Materiál, kde licenční otázka mizí věkem."),
 "other":("MISE","NASA a řízení letového provozu","Jediné dva řádky s reálně ukotveným časem v celé knihovně. Zvuk mise je federální PD; CVR z NTSB je uzavřený zdroj."),
}
ORDER=["film","tv","youtube_viral","advertisement","local_news","radio","podcast","congressional_hearing","scotus_argument","court_audio","city_council","other","federal_psa","prelinger_film","pd_film","speech"]

LIC={"green_federal_pd":("ok","ZELENÁ · FEDERÁLNÍ PD"),
     "green_pd_age":("ok","ZELENÁ · PD VĚKEM"),
     "yellow_verify":("warn","ŽLUTÁ · OVĚŘ SOUBOR"),
     "red_rights_reserved":("stop","ČERVENÁ · PŘEMLUVIT")}
RECOG={"universal":("Zná každý","Naprostá většina Američanů to okamžitě pozná."),
       "high":("Zná hodně lidí","Pozná to velká část publika, typicky jedna generace."),
       "niche":("Zná málokdo","Rozpoznatelnost skoro nulová. Musí fungovat čistě obsahem věty.")}
SELF={"yes":("Samonosné","Funguje na kohokoli. Absurdita je uvnitř věty."),
      "partial":("Částečně samonosné","Funguje samo, se znalostí zdroje je silnější."),
      "memory_dependent":("Vyžaduje paměť","Vtip žije ve vzpomínce na scénu. Nízká priorita.")}

def e(s): return html.escape(str(s), quote=True)

def row_html(r):
    lic_cls, lic_lab = LIC[r["licence"]]
    self_lab, self_hint = SELF[r["self_contained"]]
    rec_lab, rec_hint = RECOG[r["recognition"]]
    ver_ok = r["verification"] == "verified_transcript"
    dur = r["duration_sec"]
    pct = min(dur/10*100, 100)
    over = " is-over" if dur > 8 else ""
    links=[]
    if r["audio_url"]:
        links.append(f'<a class="lk lk-main" href="{e(r["audio_url"])}" target="_blank" rel="noopener">Zdroj zvuku ↗</a>')
    else:
        links.append('<span class="lk lk-none">Přímý odkaz na zvuk chybí</span>')
    for i, y in enumerate(r.get("youtube") or []):
        lab = "YouTube ↗" if i == 0 else f"YouTube {i+1} ↗"
        links.append(f'<a class="lk lk-yt" href="{e(y["url"])}" target="_blank" rel="noopener" title="{e(y["title"])}">{lab}</a>')
    for u in r["alt_sources"]:
        host = u.split("/")[2].replace("www.","") if "//" in u else u
        links.append(f'<a class="lk" href="{e(u)}" target="_blank" rel="noopener">{e(host)}</a>')
    st = f'<span class="tstamp">{e(r["start_time"])}</span>' if r["start_time"] else ''
    b = r.get("beat")
    bt = f'<span class="beat">beat {e(b["beat_id"])}</span>' if b else ''
    vq = '' if r["quote_verbatim"] else '<span class="warnmark" title="Znění není potvrzeno doslovně">znění nepotvrzeno</span>'
    sq = ''
    if r["search_query"]:
        sq = f'<div class="sq"><span class="sq-lab">Co dohledat</span>{e(r["search_query"])}</div>'
    hay = " ".join([r["quote"], r["speaker"], r["source_title"], r["why_it_lands"],
                    r["cultural_background"], " ".join(r["topics"]), str(r["year"]), r["id"]]).lower()
    topics = "".join(f'<span class="tp">{e(t)}</span>' for t in r["topics"])
    return f'''<article class="row" data-lic="{e(r['licence'])}" data-ver="{'v' if ver_ok else 'u'}" data-self="{e(r['self_contained'])}" data-rec="{e(r['recognition'])}" data-hay="{e(hay)}">
  <div class="row-a">
    <p class="q">„{e(r['quote'])}“ {vq}</p>
    <p class="who"><b>{e(r['speaker'])}</b> · {e(r['source_title'])} · {r['year']}</p>
    <p class="why">{e(r['why_it_lands'])}</p>
    <details class="more"><summary>Kontext, kulturní pozadí, licence</summary>
      <dl class="dets">
        <dt>Před</dt><dd>{e(r['context_before'])}</dd>
        <dt>Po</dt><dd>{e(r['context_after'])}</dd>
        <dt>Pozadí</dt><dd>{e(r['cultural_background'])}</dd>
        <dt>Licence</dt><dd>{e(r['licence_note'])}</dd>
        <dt>Ověření</dt><dd>{e(r['verification_note'])}</dd>
      </dl>
    </details>
    {sq}
    <div class="tps">{topics}</div>
    <div class="lks">{''.join(links)}</div>
  </div>
  <div class="row-b">
    <div class="dur{over}">
      <div class="dur-n">{dur}<span>s</span>{'<i>odhad</i>' if r['duration_estimated'] else '<i>přesně</i>'}</div>
      <div class="dur-bar"><span style="width:{pct:.0f}%"></span></div>
    </div>
    {st}{bt}
    <span class="lictag t-{lic_cls}">{lic_lab}</span>
    <span class="ver {'v-ok' if ver_ok else 'v-no'}">{'Ověřeno přepisem' if ver_ok else 'Neověřeno'}</span>
    <span class="rec rec-{e(r['recognition'])}" title="{e(rec_hint)}">{rec_lab}</span>
    <span class="sc sc-{e(r['self_contained'])}" title="{e(self_hint)}">{self_lab}</span>
    <code class="rid">{e(r['id'])}</code>
  </div>
</article>'''

groups=collections.OrderedDict()
for k in ORDER: groups[k]=[]
unknown=set()
for r in rows:
    st=r["source_type"]
    if st not in groups: unknown.add(st); st="other"
    groups[st].append(r)
if unknown: print("POZOR: neznámý source_type zařazen do 'other':", ", ".join(sorted(unknown)))

n_lic=collections.Counter(r["licence"] for r in rows)
n_ver=sum(1 for r in rows if r["verification"]=="verified_transcript")
n_self=sum(1 for r in rows if r["self_contained"]=="yes")
n_yt=sum(1 for r in rows if r.get("youtube"))
n_uni=sum(1 for r in rows if r["recognition"]=="universal")
n_niche=sum(1 for r in rows if r["recognition"]=="niche")

sections=[]
for k in ORDER:
    rs=groups[k]
    if not rs: continue
    code,title,note=SEAM[k]
    sections.append(f'''<section class="grp" data-seam="{e(k)}">
  <div class="grp-head"><span class="grp-id">{code}</span><h2>{title}</h2><span class="grp-n">{len(rs)}</span></div>
  <p class="grp-note">{note}</p>
  <div class="rows">{''.join(row_html(r) for r in rs)}</div>
</section>''')

seam_tabs="".join(
  f'<button class="chip" data-f="seam" data-v="{k}" aria-pressed="false">{SEAM[k][0]} <span>{len(groups[k])}</span></button>'
  for k in ORDER if groups[k])

TPL = open(TPLP, encoding="utf-8").read()
out = (TPL.replace("@@TOTAL@@", str(len(rows)))
          .replace("@@GREEN@@", str(n_lic["green_federal_pd"]))
          .replace("@@YELLOW@@", str(n_lic["yellow_verify"]))
          .replace("@@RED@@", str(n_lic["red_rights_reserved"]))
          .replace("@@VER@@", str(n_ver))
          .replace("@@SELF@@", str(n_self))
          .replace("@@YT@@", str(n_yt))
          .replace("@@UNI@@", str(n_uni))
          .replace("@@NICHE@@", str(n_niche))
          .replace("@@SEAMTABS@@", seam_tabs)
          .replace("@@SECTIONS@@", "\n".join(sections)))
open(OUT,"w",encoding="utf-8").write(out)
print("wrote", OUT, len(out), "bytes,", len(rows), "rows")
