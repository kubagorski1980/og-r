# -*- coding: utf-8 -*-
"""
Leady z przetargów – dla gwarantów i ubezpieczycieli (gwarancje wadialne i należytego wykonania) oraz dla podwykonawców i dostawców
(zwycięzcy przetargów). Źródła: wspólna pamięć ogłoszeń (BZP: sekcja 6.4 – wadium, 6.5 – zabezpieczenie należytego wykonania umowy)
i moduł Odwołań od przetargów (informacje o wyborze, oferenci z danymi z rejestrów).
Zabezpieczenie należytego wykonania: nie więcej niż 5% ceny całkowitej podanej w ofercie (art. 452 ust. 2 Pzp; do 10% – ust. 3, gdy uzasadnia to
przedmiot lub ryzyko opisane w SWZ). Gdy ogłoszenie albo SWZ (analiza przetargu) podaje procent – kwota liczona według niego, inaczej górna granica 5%.
"""
import re
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

RE_KWOTA = re.compile(r"(\d{1,3}(?:[ .\u00a0]\d{3})+(?:,\d{1,2})?|\d+(?:,\d{1,2})?)\s*(?:zł|PLN|złotych)", re.I)


def _kw(s):
    return liczba(s, None, kropka_tysiecy=True)


def wadium_z_tresci(tekst):
    """BZP, sekcja 6.4: (wymagane: True/False/None, kwota łączna w zł albo None, opis krótki)."""
    t = re.sub(r"\s+", " ", tekst or "")
    m = re.search(r"6\.4\.\)\s*Zamawiający wymaga wadium:\s*(Tak|Nie)", t, re.I)
    if not m:
        m2 = re.search(r"(?i)wadium w wysokości[^0-9]{0,20}" + RE_KWOTA.pattern, t)
        return (True, _kw(m2.group(1)), "") if m2 else (None, None, "")
    if m.group(1).lower() == "nie":
        return False, None, ""
    seg = t[m.end():m.end() + 1500]
    koniec = re.search(r"6\.5\.\)", seg)
    seg = seg[:koniec.start()] if koniec else seg[:800]
    kw = [x for x in (_kw(a) for a in RE_KWOTA.findall(seg)) if x and x >= 50]
    return True, (round(sum(kw), 2) if kw else None), seg.strip()[:300]


def znwu_z_tresci(tekst):
    """BZP, sekcja 6.5: czy zamawiający wymaga zabezpieczenia należytego wykonania umowy (True/False/None)."""
    m = re.search(r"6\.5\.\)\s*Zamawiający wymaga zabezpieczenia należytego wykonania umowy:\s*(Tak|Nie)", re.sub(r"\s+", " ", tekst or ""), re.I)
    return None if not m else m.group(1).lower() == "tak"


ZNWU_MAX_PROC = 5.0  # art. 452 ust. 2 Pzp – górna granica, gdy dokumenty nie podają procentu
_RE_ZNWU = re.compile(r"(?i)zabezpiecz\w*\s+nale[żz]yt\w*\s+wykonani\w*(?:\s+umowy)?")
_RE_PROC = re.compile(r"(\d{1,2}(?:[.,]\d{1,2})?)\s*(?:%|proc\w*)")


def znwu_procent(tekst, cale_pole=False):
    """Procent zabezpieczenia należytego wykonania umowy z treści ogłoszenia / SWZ (np. „zabezpieczenie należytego wykonania umowy
    w wysokości 3% ceny całkowitej”) – 0 < % ≤ 10 (art. 452 ust. 2–3 Pzp), inaczej None. cale_pole – tekst dotyczy tylko zabezpieczenia
    (pole analizy przetargu „zabezpieczenie”), więc pierwszy procent w tekście."""
    t = re.sub(r"\s+", " ", str(tekst or ""))
    if not t:
        return None
    okna = [t[:300]] if cale_pole else [t[m.end():m.end() + 250] for m in _RE_ZNWU.finditer(t)]
    for ok_ in okna:
        if re.match(r"(?i)\W{0,5}(?:nie\s+(?:wymaga|jest\s+wymagane|przewiduje)|brak)", ok_):
            continue
        m = _RE_PROC.search(ok_)
        if m and not re.search(r"(?i)wadium|kar\w*\s+umown", ok_[:m.start()]):
            p = float(m.group(1).replace(",", "."))
            if 0 < p <= 10:
                return p
    return None


def znwu(cena, procent=None, zrodlo=""):
    """Kwota i opis zabezpieczenia do leadu: procent z dokumentów albo górna granica 5% (art. 452 ust. 2 Pzp)."""
    if not isinstance(cena, (int, float)) or not cena:
        return {"znwu_szac": None, "znwu_proc": procent, "znwu_opis": ""}
    if procent:
        return {"znwu_szac": round(cena * procent / 100, 2), "znwu_proc": procent,
                "znwu_opis": f"{format(float(procent), 'g').replace('.', ',')}% ceny ({zrodlo or 'dokumenty zamówienia'})"}
    return {"znwu_szac": round(cena * ZNWU_MAX_PROC / 100, 2), "znwu_proc": None,
            "znwu_opis": "do 5% ceny (art. 452 ust. 2 Pzp) – górna granica; procent podaje SWZ"}


def zwyciezcy(postepowania, procenty=None):
    """procenty – {numer: (procent, źródło)} z ogłoszenia / analizy SWZ (trasy_leady); bez nich – górna granica 5% (art. 452 ust. 2 Pzp)."""
    procenty = procenty or {}
    # Wybrani wykonawcy z modułu Odwołań (informacje o wyborze): firma, NIP, kontakty, przedmiot, cena, szacunek zabezpieczenia.
    wyn = []
    for nr, r in (postepowania or {}).items():
        for o in r.get("ocena") or []:
            w = o.get("wybrany") or {}
            if not w.get("wykonawca"):
                continue
            of = next((x for x in o.get("oferenci") or [] if x.get("status") == "wybrana"), {}) or {}
            k = of.get("rejestr") or {}
            cena = w.get("cena_brutto") or of.get("cena_brutto")
            wyn.append({"numer": nr, "przedmiot": r.get("przedmiot", "") + (f" – część {o['czesc']}" if o.get("czesc") else ""),
                        "zamawiajacy": r.get("zamawiajacy", ""), "wojewodztwo": r.get("wojewodztwo", ""), "rodzaj": r.get("rodzaj_przedmiotu", ""),
                        "link": r.get("link", ""), "wykonawca": w.get("wykonawca"), "nip": of.get("nip") or w.get("nip") or "", "cena_brutto": cena,
                        **znwu(cena, *(procenty.get(nr) or (None, ""))), "liczba_ofert": o.get("liczba_ofert"),
                        "data_wyboru": o.get("data_informacji") or (((r.get("dane") or {}).get("czesci") or [{}])[0].get("wybor") or {}).get("data_informacji")
                        or (r.get("sprawdzono") or "")[:10],
                        "adres": k.get("adres") or of.get("adres") or "", "email": ", ".join(x for x in dict.fromkeys([k.get("email", "")] + (k.get("emaile_strona") or [])) if x),
                        "telefon": ", ".join(x for x in dict.fromkeys([k.get("telefon", "")] + (k.get("telefony_strona") or [])) if x),
                        "www": k.get("www", ""), "krs": k.get("krs", ""), "status_vat": k.get("status_vat", "")})
    return sorted(wyn, key=lambda x: -(x["cena_brutto"] or 0))


# ---------------------------------------------------------------- zwycięzcy z całego rynku: ogłoszenia o wyniku (BZP) i o udzieleniu zamówienia (TED)
TED_POLA_WYNIK = ["publication-number", "title-proc", "buyer-name", "contract-nature", "place-of-performance", "publication-date",
                  "organisation-name-tenderer", "organisation-identifier-tenderer", "organisation-city-tenderer", "tender-value",
                  "winner-country", "classification-cpv"]


def ted_wyniki_dnia(data, otworz=None):
    """Polskie ogłoszenia o udzieleniu zamówienia (TED, powyżej progów UE) z jednego dnia: zwycięzca, NIP, miejscowość, wartość części."""
    import json as _j
    import urllib.request as _u
    import ted as T
    q = f"buyer-country=POL AND publication-date={data.replace('-', '')} AND notice-type IN (can-standard can-social)"
    wyn, strona = [], 1
    while strona <= 20:
        body = _j.dumps({"query": q, "fields": TED_POLA_WYNIK, "limit": 250, "page": strona}).encode()
        req = _u.Request(T.API, data=body, headers={"Content-Type": "application/json", "User-Agent": "Bidivia"})
        with (otworz or (lambda r: _u.urlopen(r, timeout=90)))(req) as r:
            d = _j.loads(r.read().decode("utf-8"))
        partia = d.get("notices") or []
        for n in partia:
            nazwy = (n.get("organisation-name-tenderer") or {})
            nazwy = nazwy.get("pol") or next(iter(nazwy.values()), []) if isinstance(nazwy, dict) else (nazwy or [])
            ids = n.get("organisation-identifier-tenderer") or []
            miasta = n.get("organisation-city-tenderer") or []
            wart = n.get("tender-value") or []
            nuts = [c for c in n.get("place-of-performance") or [] if re.fullmatch(r"PL\d{2,3}", str(c))]
            woj = next((T.NUTS_WOJ.get(c[:4]) for c in nuts if T.NUTS_WOJ.get(c[:4])), "")
            rodz = {"works": "Works", "supplies": "Delivery", "services": "Services"}.get((n.get("contract-nature") or [""])[0], "")
            for i, nazwa in enumerate(nazwy):
                nip = re.sub(r"\D", "", str(ids[i] if i < len(ids) else ""))
                try:
                    cena = float(wart[i]) if i < len(wart) else None
                except (TypeError, ValueError):
                    cena = None
                wyn.append({"zrodlo": "TED", "numer": f"TED {n.get('publication-number')}", "data": data, "typ_zam": rodz,
                            "zamawiajacy": T._pol(n.get("buyer-name")), "przedmiot": T._pol(n.get("title-proc")), "wojewodztwo": woj,
                            "cpv": ", ".join(list(dict.fromkeys(n.get("classification-cpv") or []))[:5]), "wykonawca": str(nazwa)[:160],
                            "nip": nip if len(nip) == 10 else "", "siedziba": str(miasta[i] if i < len(miasta) else ""), "cena": cena,
                            "ofert": None, "link": f"https://ted.europa.eu/pl/notice/-/detail/{n.get('publication-number')}"})
        if len(partia) < 250:
            break
        strona += 1
    return wyn
