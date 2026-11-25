# -*- coding: utf-8 -*-
"""
TED – Dziennik Urzędowy UE: polskie ogłoszenia o zamówieniu powyżej progów unijnych (w tym zamówienia sektorowe – np. PKP PLK,
PKP Intercity, POLREGIO), których nie ma w BZP. Publiczne API wyszukiwania TED v3 (api.ted.europa.eu/v3/notices/search, bez klucza;
sprawdzone 26.10.2026: ok. 280 polskich ogłoszeń o zamówieniu dziennie).
Rekordy w tym samym formacie co ogłoszenia BZP (bzp.normalizuj) – działają w wyszukiwarce, sicie, analizie i filtrze regionu.
Województwo z miejsca realizacji (kod NUTS), nie z siedziby zamawiającego.
"""
import json
import re
import time
import urllib.error
import urllib.request

API = "https://api.ted.europa.eu/v3/notices/search"
TYPY = "cn-standard cn-social cn-desg"  # ogłoszenia o zamówieniu (tryb standardowy, usługi społeczne, konkursy)
POLA = ["publication-number", "title-proc", "title-lot", "buyer-name", "buyer-city", "buyer-identifier", "notice-type", "contract-nature",
        "classification-cpv", "place-of-performance", "place-of-performance-city-proc", "deadline-receipt-tender-date-lot", "deadline-time-lot",
        "publication-date", "description-proc", "document-url-lot", "submission-url-lot", "procedure-type", "estimated-value-proc",
        "estimated-value-lot"]
NUTS_WOJ = {"PL21": "małopolskie", "PL22": "śląskie", "PL41": "wielkopolskie", "PL42": "zachodniopomorskie", "PL43": "lubuskie",
            "PL51": "dolnośląskie", "PL52": "opolskie", "PL61": "kujawsko-pomorskie", "PL62": "warmińsko-mazurskie", "PL63": "pomorskie",
            "PL71": "łódzkie", "PL72": "świętokrzyskie", "PL81": "lubelskie", "PL82": "podkarpackie", "PL84": "podlaskie",
            "PL91": "mazowieckie", "PL92": "mazowieckie"}
RODZAJ = {"works": "Roboty budowlane", "supplies": "Dostawy", "services": "Usługi"}


def _zapytanie(q, strona, limit=250, otworz=None):
    body = json.dumps({"query": q, "fields": POLA, "limit": limit, "page": strona}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json", "User-Agent": "Bidivia"})
    for proba in range(3):
        try:
            with (otworz or (lambda r: urllib.request.urlopen(r, timeout=90)))(req) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and proba < 2:
                time.sleep(10 * (proba + 1))
                continue
            raise RuntimeError(f"TED: HTTP {e.code} – {e.read(300).decode('utf-8', 'replace')}")
        except urllib.error.URLError as e:
            if proba < 2:
                time.sleep(5)
                continue
            raise RuntimeError(f"TED niedostępny ({e.reason})")


def _pol(v):
    """Wartość wielojęzyczna TED → tekst polski (albo pierwszy dostępny)."""
    if isinstance(v, dict):
        v = v.get("pol") or v.get("mul") or next(iter(v.values()), "")
    if isinstance(v, list):
        v = " / ".join(dict.fromkeys(str(x) for x in v if x))
    return str(v or "").strip()


def normalizuj(n):
    nr = n.get("publication-number") or ""
    nuts = [c for c in n.get("place-of-performance") or [] if re.fullmatch(r"PL\d{2,3}", str(c))]
    woj_lista = list(dict.fromkeys(NUTS_WOJ[c[:4]] for c in nuts if NUTS_WOJ.get(c[:4])))
    siedziba = "mazowieckie" if re.search(r"(?i)warszaw", _pol(n.get("buyer-city"))) else ""
    woj = next((w for w in woj_lista if w != siedziba), woj_lista[0] if woj_lista else "")  # miejsce realizacji poza siedzibą zamawiającego ma pierwszeństwo
    # części mogą mieć różne terminy – najwcześniejszy (bezpieczny dla wykonawcy); godzina z tej samej części
    daty = [str(x or "")[:10] for x in n.get("deadline-receipt-tender-date-lot") or []]
    godziny = [str(x or "") for x in n.get("deadline-time-lot") or []]
    pary = sorted((d, godziny[i] if i < len(godziny) else "") for i, d in enumerate(daty) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))
    termin, godz = pary[0] if pary else ("", "")
    adresy = list(dict.fromkeys((n.get("document-url-lot") or []) + (n.get("submission-url-lot") or [])))
    nip = next((re.sub(r"\D", "", x) for x in n.get("buyer-identifier") or [] if len(re.sub(r"\D", "", x)) == 10), "")
    kw = n.get("estimated-value-proc") or sum(x for x in (n.get("estimated-value-lot") or []) if isinstance(x, (int, float))) or None
    miasto = _pol(n.get("place-of-performance-city-proc")).split(" / ")[0] or _pol(n.get("buyer-city")).split(" / ")[0]
    tresc = "\n".join(x for x in (
        _pol(n.get("description-proc")),
        ("Dokumenty i składanie ofert: " + " ".join(adresy)) if adresy else "",
        f"NIP zamawiającego: {nip}" if nip else "",
        f"Miejsce realizacji (NUTS): {', '.join(nuts)}" if nuts else "Miejsce realizacji: cała Polska / nie wskazano",
        f"Wartość szacunkowa: {kw}" if kw else "") if x)
    return {"numer": f"TED {nr}", "zrodlo": "TED", "przedmiot": _pol(n.get("title-proc")) or _pol(n.get("title-lot")),
            "zamawiajacy": _pol(n.get("buyer-name")), "miasto": miasto, "wojewodztwo": woj,
            "termin_ofert": f"{termin}T{godz[:5]}" if termin and godz else termin, "data_publikacji": str(n.get("publication-date") or "")[:10],
            "rodzaj": RODZAJ.get((n.get("contract-nature") or [""])[0], ""), "cpv": ", ".join(list(dict.fromkeys(n.get("classification-cpv") or []))[:10]),
            "link": f"https://ted.europa.eu/pl/notice/-/detail/{nr}", "pdf": f"https://ted.europa.eu/pl/notice/{nr}/pdf",
            "tresc": tresc, "tryb": n.get("procedure-type") or "", "wartosc_szacunkowa": kw, "nuts": list(dict.fromkeys(nuts)), "wojewodztwa": woj_lista}


def pobierz_dzien(data, log=None, otworz=None):
    """Wszystkie polskie ogłoszenia o zamówieniu opublikowane w TED danego dnia (RRRR-MM-DD)."""
    q = f"buyer-country=POL AND publication-date={data.replace('-', '')} AND notice-type IN ({TYPY})"
    wyn, strona = [], 1
    while True:
        d = _zapytanie(q, strona, otworz=otworz)
        partia = d.get("notices") or []
        wyn += [normalizuj(n) for n in partia]
        if len(partia) < 250 or strona >= 20:
            break
        strona += 1
    if log:
        log(f"TED {data}: {len(wyn)} ogłoszeń")
    return wyn
