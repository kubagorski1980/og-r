# -*- coding: utf-8 -*-
"""
Zaproszenia do składania ofert (wspólnoty, spółdzielnie, deweloperzy i inni zamawiający): przypomnienie przed terminem składania ofert
i lista wykonawców z okolicy, którzy w ostatnim czasie wykonywali podobne zamówienia (ogłoszenia o wyniku w BZP).
Źródło ma ograniczenie: BZP obejmuje tylko zamówienia publiczne – firmy pracujące wyłącznie dla klientów prywatnych nie trafią na listę.
"""
import datetime as dt
import math
import re

import historia_zam as HZ
import weryfikacja as WER

DNI_PRZYPOMNIENIA = 5
PROG_PODOBIENSTWA = 0.3


def termin_ofert(K):
    """Termin składania ofert z kreatora (data albo tekst z datą) – date albo None."""
    t = str((K or {}).get("termin_ofert") or "").strip()
    # tylko pełna data (RRRR-MM-DD albo DD.MM.RRRR, także z godziną) – tekst „do 15 stycznia 2027” albo sam rok nie jest terminem
    # (weryfikacja._data zamienia sam rok na 31 grudnia – zasada dla referencji, nie dla terminu składania ofert)
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})(?![\d])", t) or re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})(?![\d])", t)
    if not m:
        return None
    r_, mi, d_ = (m.group(1), m.group(2), m.group(3)) if "-" in m.group(0) else (m.group(3), m.group(2), m.group(1))
    try:
        return dt.date(int(r_), int(mi), int(d_))
    except ValueError:
        return None


def _miasto(siedziba):
    """„Świdnica (58-100)” → „Świdnica”."""
    return re.sub(r"\s*\(\d{2}-\d{3}\)\s*$", "", str(siedziba or "")).strip(" ,;")


def kandydaci(wyniki, przedmiot, cpv, lat, lon, promien, geokoduj, wyklucz_nipy=(), max_kandydatow=20, max_geokodowan=40):
    """Wykonawcy, którzy wygrali podobne zamówienia, z siedzibą albo miejscem wykonanych prac w promieniu. geokoduj(miasto) → (lat, lon) albo None."""
    wyklucz = {WER._nip(n) for n in wyklucz_nipy if n}
    grupy = {}
    for w in wyniki or []:
        if not w.get("wykonawca") or w.get("uniewaznione"):
            continue
        s = HZ.podobienstwo(przedmiot, w.get("przedmiot") or "", cpv, w.get("cpv") or "")
        if s < PROG_PODOBIENSTWA:
            continue
        nip = WER._nip(w.get("nip"))
        if nip and nip in wyklucz:
            continue
        k = nip or WER._norm(w.get("wykonawca"))[:40]
        g = grupy.setdefault(k, {"nip": nip, "nazwa": w["wykonawca"], "siedziba": _miasto(w.get("siedziba")), "prace": [], "podobienstwo": 0.0})
        g["prace"].append({"przedmiot": (w.get("przedmiot") or "")[:160], "zamawiajacy": (w.get("zamawiajacy") or "")[:120], "miasto": w.get("miasto") or "",
                           "data": w.get("data") or "", "cena": w.get("cena")})
        g["podobienstwo"] = max(g["podobienstwo"], s)
    wstepni = sorted(grupy.values(), key=lambda g: (-(g["podobienstwo"] + 0.15 * math.log(1 + len(g["prace"]))), g["nazwa"]))
    pamiec, geokod = {}, 0
    def pozycja(miasto):
        nonlocal geokod
        m = (miasto or "").strip()
        if not m:
            return None
        if m not in pamiec:
            if geokod >= max_geokodowan:
                return None
            geokod += 1
            pamiec[m] = geokoduj(m)
        return pamiec[m]
    wynik = []
    for g in wstepni:
        odl = []
        p = pozycja(g["siedziba"])
        d_siedz = HZ_km(lat, lon, p) if p else None
        for pr in g["prace"]:
            q = pozycja(pr["miasto"])
            if q:
                odl.append(HZ_km(lat, lon, q))
        d_prac = min(odl) if odl else None
        bliskie = [x for x in (d_siedz, d_prac) if x is not None]
        if not bliskie or min(bliskie) > promien:
            continue
        g["odleglosc_siedziby"] = round(d_siedz, 1) if d_siedz is not None else None
        g["odleglosc_prac"] = round(d_prac, 1) if d_prac is not None else None
        g["liczba_prac"] = len(g["prace"])
        g["prace"] = sorted(g["prace"], key=lambda x: x["data"], reverse=True)[:5]
        g["ocena"] = round(g["podobienstwo"] + 0.15 * math.log(1 + g["liczba_prac"]) - 0.3 * min(bliskie) / promien, 3)
        wynik.append(g)
    return sorted(wynik, key=lambda g: -g["ocena"])[:max_kandydatow]


def HZ_km(lat, lon, p):
    import region as RG
    return RG.km(lat, lon, p[0], p[1])


def tresc_zaproszenia(zamawiajacy, nazwa, opis, termin, kontakt, wykonawca):
    """Treść e-maila z zaproszeniem do złożenia oferty (z informacją o przetwarzaniu danych i możliwością rezygnacji)."""
    t = f"{termin:%d.%m.%Y}" if isinstance(termin, dt.date) else (termin or "[termin]")
    temat = f"Zaproszenie do złożenia oferty – {nazwa}"
    tekst = (f"Dzień dobry,\n\n{zamawiajacy or '[zamawiający]'} zaprasza {wykonawca or 'Państwa firmę'} do złożenia oferty w postępowaniu „{nazwa}”.\n\n"
             f"Przedmiot: {opis or nazwa}\nTermin składania ofert: {t}\n\n"
             "Zapytanie ofertowe i formularz są w załącznikach. Zaproszenie kierujemy do wykonawców, którzy w ostatnim czasie realizowali podobne "
             "zamówienia w okolicy (na podstawie publicznych ogłoszeń o wyniku postępowań w Biuletynie Zamówień Publicznych).\n\n"
             f"Pytania: {kontakt or 'odpowiedz na tę wiadomość'}.\n\nZ poważaniem\n{zamawiajacy or ''}\n\n"
             + WER.klauzula_art14(zamawiajacy, kontakt, f"zaproszenie do złożenia oferty w postępowaniu „{nazwa}”",
                                  "publiczne rejestry (CEIDG, KRS), ogłoszenia o wyniku postępowań w Biuletynie Zamówień Publicznych i strona internetowa firmy",
                                  "do zakończenia postępowania")
             + "\nJeżeli nie chcą Państwo otrzymywać takich zaproszeń, prosimy o krótką odpowiedź – nie będziemy kontaktować się ponownie.")
    return temat, tekst
