# -*- coding: utf-8 -*-
"""
„Sprawdź kosztorys” – kontrola gotowego kosztorysu:
 1) reguły techniczne (bez AI): brak ceny, zero ilości, puste opisy, duplikaty, rozbieżne ceny tych samych robót,
    pozycje o bardzo dużym udziale w wartości,
 2) analiza AI: brakujące i zbędne elementy, nierealne jednostki, ilości, ceny – z konkretną sugestią poprawki.
Każdy alert ma identyfikator i numer pozycji; użytkownik może zastosować sugestię, poprawić ręcznie
albo oznaczyć alert jako świadome odstępstwo.
"""
import hashlib
import json
import re

import modul_oferty as MO
import rozbieznosci as ROZB
from liczby import liczba


def _l(v):
    """Liczba z pozycji kosztorysu – także tekst („12,5”, „1 234,50”); nieczytelna albo nan/inf – 0 (dotąd ValueError i błąd 500)."""
    x = liczba(v, 0.0)
    return x if x == x and abs(x) != float("inf") else 0.0

JM_POWIERZCHNIOWE = ("tynk", "malowan", "docieplen", "gruntowan", "okładzin", "posadzk", "pokryci", "izolacj")


def pozycje(dane):
    """Płaska lista pozycji z numeracją (lp od 1) i nazwą działu."""
    wyn, lp = [], 0
    for di, dz in enumerate(dane.get("dzialy", [])):
        for pi, p in enumerate(dz.get("pozycje", [])):
            lp += 1
            wyn.append({"lp": lp, "di": di, "pi": pi, "dzial": dz.get("nazwa", ""), **p})
    return wyn


def _id(*cz):
    return hashlib.sha1("|".join(str(c) for c in cz).encode()).hexdigest()[:10]


def _norm(t):
    return re.sub(r"\s+", " ", str(t or "").lower()).strip()


def reguly(dane):
    alerty = []
    poz = pozycje(dane)
    netto = sum(_l(p.get("wartosc")) for p in poz) or 1

    def dodaj(p, typ, kat, opis, sug=None):
        # id bez opisu – kwoty w opisie zmieniają się po korekcie ceny, a decyzja („odstępstwo”) ma zostać
        alerty.append({"id": _id(p["lp"] or str(p.get("opis") or "")[:80], kat), "lp": p["lp"], "typ": typ, "kategoria": kat, "opis": opis,
                       "sugestia": sug, "zrodlo": "reguła", "status": "nowy"})
    for p in poz:
        il, cena = _l(p.get("ilosc")), _l(p.get("cena"))
        uzup_ = "uzupełniając" in _norm(p["dzial"]) or "poza przedmiar" in _norm(p["dzial"])
        if il > 0 and cena <= 0 and not uzup_:  # pozycje spoza przedmiaru – reguła „Bez wyceny” niżej
            dodaj(p, "ostrzezenie", "Brak ceny", "Pozycja ma ilość, ale nie ma ceny jednostkowej – nie wpływa na wartość oferty.")
        if (il <= 0 or cena <= 0) and ("uzupełniając" in _norm(p["dzial"]) or "poza przedmiar" in _norm(p["dzial"])) \
                and not (ROZB.RE_NIE_DOTYCZY.search(str(p.get("uwagi") or "")) and not re.match(r"(?i)\s*do ustalenia", str(p.get("uwagi") or ""))):
            dodaj(p, "ostrzezenie", "Bez wyceny", f"„{str(p.get('opis') or '')[:90]}” – robota spoza przedmiaru wymagana albo niejasna, a w cenie oferty 0 zł"
                  + (f" ({str(p.get('uwagi'))[:120]})" if p.get("uwagi") else "") + " – wpisz ilość i cenę albo zadaj pytanie zamawiającemu.")
        if cena > 0 and il <= 0 and "uzupełniając" not in _norm(p["dzial"]):
            dodaj(p, "ostrzezenie", "Zerowa ilość", "Pozycja ma cenę, ale ilość 0 – sprawdź przedmiar.")
        if not _norm(p.get("opis")):
            dodaj(p, "ostrzezenie", "Pusty opis", "Brak opisu pozycji.")
        if not _norm(p.get("jm")) and il > 0:
            dodaj(p, "ostrzezenie", "Brak jednostki", "Brak jednostki miary.")
        jm = _norm(p.get("jm"))
        if any(s in _norm(p.get("opis")) for s in JM_POWIERZCHNIOWE) and jm in ("m3", "m³", "szt", "szt.", "kg", "t"):
            dodaj(p, "optymalizacja", "Nietypowa jednostka",
                  f"Roboty powierzchniowe zwykle liczy się w m2, a pozycja ma jednostkę „{p.get('jm')}”.")
        if _l(p.get("wartosc")) / netto > 0.35 and len(poz) > 5:
            dodaj(p, "optymalizacja", "Duży udział",
                  f"Pozycja stanowi {_l(p.get('wartosc')) / netto:.0%} wartości kosztorysu – warto szczególnie dokładnie sprawdzić jej cenę i ilość.")
    # duplikaty i rozbieżne ceny tych samych robót
    grupy = {}
    for p in poz:
        k = (_norm(p.get("opis"))[:120], _norm(p.get("jm")))
        if k[0]:
            grupy.setdefault(k, []).append(p)
    for (opis, jm), lista in grupy.items():
        if len(lista) < 2:
            continue
        ceny = [_l(x.get("cena")) for x in lista if _l(x.get("cena")) > 0]
        if ceny and max(ceny) > 1.25 * min(ceny):
            srednia = MO.zaokr(sum(ceny) / len(ceny))
            for x in lista:
                if abs(_l(x.get("cena")) - srednia) / srednia > 0.12:
                    dodaj(x, "optymalizacja", "Rozbieżne ceny",
                          f"Ta sama robota występuje w poz. {', '.join(str(y['lp']) for y in lista)} z różnymi cenami "
                          f"({MO.zl(min(ceny))} – {MO.zl(max(ceny))}). Propozycja: ujednolicić do średniej.",
                          {"pole": "cena", "wartosc": srednia})
    return alerty


SYSTEM = """Jesteś doświadczonym kosztorysantem budowlanym w Polsce. Sprawdzasz gotowy kosztorys ofertowy i wskazujesz \
konkretne błędy i ryzyka. Nie wymyślasz problemów – zgłaszasz tylko rzeczy istotne. Odpowiadasz WYŁĄCZNIE JSON-em."""


def polecenie_ai(dane):
    P = dane.get("postepowanie", {})
    linie = [f"{p['lp']} | {str(p['dzial'])[:40]} | {str(p.get('opis') or '')[:150]} | {p.get('jm', '')} | {_l(p.get('ilosc')):g} | "
             f"{_l(p.get('cena')):.2f} | {_l(p.get('wartosc')):.2f}" for p in pozycje(dane)]
    return (f"Zakres: {P.get('nazwa_zamowienia', '')}. Obiekt: {P.get('obiekt', '')}. Wartość netto: {_l(dane.get('netto')):.2f} zł.\n\n"
            "KOSZTORYS (lp | dział | opis | j.m. | ilość | cena jedn. netto | wartość):\n" + "\n".join(linie) + "\n\n"
            "Sprawdź kosztorys i wskaż:\n"
            "- NIEREALNE CENY – wyraźnie zawyżone lub zaniżone względem rynku w Polsce (podaj realną cenę),\n"
            "- NIEREALNE ILOŚCI lub niespójności między pozycjami (np. tynk większy niż ściany, brak rusztowań przy elewacji),\n"
            "- NIEWŁAŚCIWE JEDNOSTKI,\n"
            "- BRAKUJĄCE ROBOTY typowe dla tego zakresu (np. gruntowanie przed tynkiem, obróbki przy dociepleniu, wywóz odpadów),\n"
            "- ZBĘDNE lub zdublowane pozycje.\n"
            "Dla każdej uwagi podaj sugestię poprawki, jeśli da się ją wyrazić jedną wartością.\n"
            'Zwróć JSON: {"alerty": [{"lp": 12, "typ": "ostrzezenie" | "optymalizacja", "kategoria": "Nierealna cena", '
            '"opis": "krótkie uzasadnienie", "sugestia": {"pole": "cena" | "ilosc" | "jm" | "opis", "wartosc": 45.0} lub null}]}. '
            'Dla brakujących robót użyj "lp": 0 i opisz, co dodać. Maksymalnie 25 uwag, najważniejsze najpierw.')


def analiza_ai(cfg, dane, log):
    import bip as BIP  # claude_prosty
    tekst = BIP.claude_prosty(cfg, SYSTEM, polecenie_ai(dane), max_tokens=5000, model=cfg.get("model_oferty"))
    wyn = []
    for a in MO.wyciagnij_json(tekst).get("alerty", []):
        try:
            lp = int(a.get("lp") or 0)
        except (TypeError, ValueError):
            lp = 0
        sug = a.get("sugestia") if isinstance(a.get("sugestia"), dict) and a["sugestia"].get("pole") in ("cena", "ilosc", "jm", "opis") else None
        wyn.append({"id": _id(lp, a.get("kategoria"), re.sub(r"\d[\d\s.,]*\s*(?:%|zł|zl)?", "#", str(a.get("opis") or ""))[:120]), "lp": lp,
                    "typ": "ostrzezenie" if a.get("typ") == "ostrzezenie" else "optymalizacja",
                    "kategoria": str(a.get("kategoria", "Uwaga"))[:60], "opis": str(a.get("opis", ""))[:500],
                    "sugestia": sug, "zrodlo": "AI", "status": "nowy"})
    log(f"AI zgłosiło {len(wyn)} uwag.")
    return wyn
