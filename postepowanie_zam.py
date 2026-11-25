# -*- coding: utf-8 -*-
"""
Zamawiający publiczny po publikacji ogłoszenia: kalendarz terminów postępowania, pytania wykonawców i wyjaśnienia treści SWZ,
zmiana SWZ i przedłużenie terminu składania ofert (pismo Word).

Przepisy (sprawdzone 11.11.2026): wyjaśnienia treści SWZ – art. 284 ust. 2 (tryb podstawowy: odpowiedź najpóźniej 2 dni przed terminem
składania ofert, jeśli wniosek wpłynął najpóźniej 4 dni przed nim; ust. 4 – później nie trzeba odpowiadać ani przedłużać terminu;
ust. 6 – publikacja bez ujawniania źródła zapytania), w postępowaniach od progów UE – art. 135 ust. 2 (6 dni / 14 dni); zmiana SWZ –
art. 286 (ust. 3 przedłużenie terminu, ust. 5 komunikat na stronie postępowania, ust. 9 ogłoszenie o zmianie w BZP), od progów UE – art. 137;
otwarcie ofert najpóźniej następnego dnia po terminie (art. 221), kwota na sfinansowanie przed otwarciem (art. 222 ust. 4), informacja
z otwarcia (art. 222 ust. 5); związanie ofertą – tryb podstawowy do 30 dni (art. 307), od progów UE do 90 dni (art. 220), pierwszym dniem
jest dzień upływu terminu składania ofert; zawarcie umowy – nie wcześniej niż 5 dni (art. 308 ust. 2) / 10 dni (art. 264 ust. 1)
od przesłania zawiadomienia o wyborze środkami komunikacji elektronicznej.
"""
import datetime as dt
import hashlib

import modul_oferty as MO


def _d(v):
    try:
        return dt.date.fromisoformat(str(v or "")[:10])
    except ValueError:
        return None


def _roboczy(d):
    """Termin kończący się w sobotę albo dzień ustawowo wolny od pracy – najbliższy dzień roboczy (art. 115 k.c.; z polskimi świętami)."""
    import kontrola_zam as KO
    return KO.nastepny_roboczy(d)


def _praktycznie(d):
    """Dopisek dla terminu liczonego wstecz, gdy wypada w dzień wolny: ostatni dzień roboczy przed nim."""
    import kontrola_zam as KO
    return f" (dzień wolny – praktycznie do {KO.poprzedni_roboczy(d):%d.%m.%Y})" if KO.wolny(d) else ""


def zatwierdzona(q):
    """Odpowiedź zatwierdzona przez zamawiającego (projekt AI nią nie jest; starsze wpisy bez znacznika – zatwierdzone)."""
    return bool(str(q.get("odpowiedz") or "").strip()) and q.get("zatwierdzona", True) is not False


def terminy_pytan(termin_ofert, unijne):
    """(ostatni dzień na wniosek, na który trzeba odpowiedzieć; ostatni dzień na odpowiedź)."""
    t = _d(termin_ofert)
    if not t:
        return None, None
    return t - dt.timedelta(days=14 if unijne else 4), t - dt.timedelta(days=6 if unijne else 2)


def ostrzezenia_umowy(data_wyboru, data_umowy, unijne, liczba_ofert=None):
    """Data umowy przed upływem terminu z art. 308 ust. 2 (5 dni) / art. 264 ust. 1 (10 dni) od przesłania zawiadomienia o wyborze
    (elektronicznie; termin kończący się w dzień wolny – następny dzień roboczy). Wyjątek: złożono tylko jedną ofertę
    (art. 308 ust. 3 pkt 1 lit. a / art. 264 ust. 2 pkt 1 lit. a) – gdy liczba ofert jest znana (1), bez ostrzeżenia."""
    w, u = _d(data_wyboru), _d(data_umowy)
    if not w or not u:
        return []
    dni, art, wyj = (10, "art. 264 ust. 1", "art. 264 ust. 2 pkt 1 lit. a") if unijne else (5, "art. 308 ust. 2", "art. 308 ust. 3 pkt 1 lit. a")
    k = _roboczy(w + dt.timedelta(days=dni))
    if u > k:
        return []
    if liczba_ofert == 1:
        return []
    return [f"Umowa z dnia {u:%d.%m.%Y} – przed upływem {dni} dni od przesłania zawiadomienia o wyborze ({w:%d.%m.%Y}; {art} Pzp, termin na odwołanie "
            f"do {k:%d.%m.%Y} włącznie). Umowę można zawrzeć najwcześniej {k + dt.timedelta(days=1):%d.%m.%Y}"
            + (f" – wcześniej tylko wtedy, gdy złożono jedną ofertę ({wyj} Pzp)." if liczba_ofert is None else ".")]


def kalendarz(termin_ofert, unijne, publikacja=None, data_wyboru=None, data_umowy=None, dzis=None, ustawowe=True, termin_pytan=None, liczba_ofert=None):
    """Terminy postępowania wyliczone z dat zamawiającego. [{data, co, podstawa, dni}] posortowane.
    termin_pytan – termin składania ofert, od którego liczy się wnioski o wyjaśnienie (po przedłużeniu: termin pierwotny).
    ustawowe=False – poniżej progu / zasada konkurencyjności: tylko publikacja i termin składania ofert."""
    dzis = dzis or dt.date.today()
    if not ustawowe:
        W = []
        if _d(publikacja):
            W.append({"data": _d(publikacja).isoformat(), "co": "Publikacja zapytania ofertowego", "podstawa": "", "dni": (_d(publikacja) - dzis).days})
        if _d(termin_ofert):
            W.append({"data": _d(termin_ofert).isoformat(), "co": "Termin składania ofert (terminy pytań i zawarcia umowy – według regulaminu zamawiającego albo wytycznych)",
                      "podstawa": "", "dni": (_d(termin_ofert) - dzis).days})
        return sorted(W, key=lambda x: x["data"])
    W = []
    dodaj = lambda d, co, podst: W.append({"data": d.isoformat(), "co": co, "podstawa": podst, "dni": (d - dzis).days})
    if _d(publikacja):
        dodaj(_d(publikacja), "Publikacja ogłoszenia o zamówieniu" + (" w Dzienniku Urzędowym UE" if unijne else " w BZP"), "")
    t = _d(termin_ofert)
    if t:
        wn, od = terminy_pytan(_d(termin_pytan) or t, unijne)
        art = "art. 135 ust. 2 Pzp" if unijne else "art. 284 ust. 2 Pzp"
        po_przedl = " – liczony od terminu sprzed przedłużenia" if (_d(termin_pytan) and _d(termin_pytan) != t) else ""
        dodaj(wn, "Ostatni dzień na wniosek o wyjaśnienie SWZ, na który trzeba odpowiedzieć (późniejsze – bez obowiązku odpowiedzi)" + po_przedl, art)
        dodaj(od, "Najpóźniej odpowiedzi na wnioski złożone w terminie – inaczej przedłużenie terminu składania ofert" + _praktycznie(od), art)
        dodaj(t, "Termin składania ofert; przed otwarciem – kwota na sfinansowanie zamówienia na stronie postępowania", "art. 222 ust. 4 Pzp")
        dodaj(t + dt.timedelta(days=1), "Otwarcie ofert najpóźniej tego dnia; zaraz po otwarciu – informacja z otwarcia ofert", "art. 222 ust. 1 i 5 Pzp")
        dodaj(t + dt.timedelta(days=89 if unijne else 29), f"Związanie ofertą – najdłuższy termin ({90 if unijne else 30} dni, pierwszy dzień = dzień składania ofert)",
              "art. 220 Pzp" if unijne else "art. 307 Pzp")
    w = _d(data_wyboru)
    if w:
        k = _roboczy(w + dt.timedelta(days=10 if unijne else 5))
        dodaj(k, f"Koniec terminu na odwołanie po wyborze oferty ({10 if unijne else 5} dni od zawiadomienia przesłanego elektronicznie) – umowę zawrzeć po tym dniu",
              "art. 264 ust. 1 i art. 515 Pzp" if unijne else "art. 308 ust. 2 i art. 515 Pzp")
    u = _d(data_umowy)
    for t_ in ostrzezenia_umowy(data_wyboru, data_umowy, unijne, liczba_ofert):  # art. 308 ust. 2 / art. 264 ust. 1 – umowa za wcześnie
        W.append({"data": u.isoformat(), "co": "UWAGA: " + t_, "podstawa": "art. 264 ust. 1 Pzp" if unijne else "art. 308 ust. 2 Pzp",
                  "dni": (u - dzis).days, "ostrzezenie": True})
    if u:
        dodaj(u + dt.timedelta(days=30), "Ogłoszenie o udzieleniu zamówienia w Dzienniku Urzędowym UE – do 30 dni od zawarcia umowy" if unijne
              else "Ogłoszenie o wyniku postępowania w BZP – do 30 dni od zakończenia postępowania", "")
    return sorted(W, key=lambda x: x["data"])


def umowa_bledy(j):
    """Kontrola danych umowy z kroku „Po wyborze oferty” (do użycia w zapisie kreatora): cena netto – kwota, VAT – 0/5/8/23 (albo 0,05…0,23),
    daty – RRRR-MM-DD. Zwraca listę komunikatów (pusta = dane poprawne)."""
    from liczby import liczba
    bl = []
    c = str((j or {}).get("cena_netto") or "").strip()
    if c and (liczba(c) is None or liczba(c) <= 0):
        bl.append(f"Cena oferty netto: „{c[:40]}” nie jest kwotą (np. 1 234 567,89).")
    v = str((j or {}).get("vat") or "").strip().replace(",", ".").rstrip("%").strip()
    if v and v not in ("0", "5", "8", "23", "0.05", "0.08", "0.23", "0.0", "0.00"):
        bl.append("VAT: dozwolone stawki 0%, 5%, 8% albo 23%.")
    for k, n in (("data_umowy", "Data umowy"), ("termin", "Termin wykonania")):
        x = str((j or {}).get(k) or "").strip()
        if x and not _d(x):
            bl.append(f"{n}: „{x[:20]}” nie jest datą (RRRR-MM-DD).")
    return bl


def pytania_stan(pytania, termin_ofert, unijne, dzis=None, ustawowe=True):
    """Każde pytanie: czy wpłynęło w terminie (obowiązek odpowiedzi) i do kiedy odpowiedzieć. termin_ofert – termin, od którego liczy się
    wnioski (po przedłużeniu: termin pierwotny). Poza Pzp (ustawowe=False) – bez terminów ustawowych."""
    dzis = dzis or dt.date.today()
    if not ustawowe:
        return [dict(q, w_terminie=None, odpowiedz_do="", po_terminie_odpowiedzi=False, zatwierdzona=zatwierdzona(q)) for q in pytania or []]
    wn, od = terminy_pytan(termin_ofert, unijne)
    wyn = []
    for q in pytania or []:
        d = _d(q.get("data"))
        w_terminie = bool(d and wn and d <= wn)
        wyn.append(dict(q, w_terminie=w_terminie, odpowiedz_do=od.isoformat() if (w_terminie and od) else "", zatwierdzona=zatwierdzona(q),
                        po_terminie_odpowiedzi=bool(w_terminie and od and not zatwierdzona(q) and dzis > od)))
    return wyn


def nowe_id(tresc):
    return hashlib.sha1((str(tresc) + dt.datetime.now().isoformat()).encode()).hexdigest()[:10]


SYSTEM_ODPOWIEDZ = ("Jesteś specjalistą ds. zamówień publicznych po stronie zamawiającego. Przygotowujesz projekt odpowiedzi na pytanie wykonawcy "
                    "o treść SWZ WYŁĄCZNIE na podstawie dokumentów postępowania. Gdy dokumenty nie dają odpowiedzi albo odpowiedź wymaga decyzji "
                    "zamawiającego – piszesz to i oznaczasz [DO DECYZJI ZAMAWIAJĄCEGO: …]. Odpowiadasz wyłącznie JSON-em.")


def polecenie_odpowiedzi(pytanie, unijne):
    return ("Pytanie wykonawcy o treść SWZ:\n" + str(pytanie) + "\n\nPrzygotuj odpowiedź zamawiającego. Zwróć JSON: "
            '{"odpowiedz": "treść odpowiedzi – rzeczowo, z odesłaniem do punktu dokumentu", '
            '"zmiana_swz": true/false (czy odpowiedź zmienia treść SWZ lub załączników – np. termin, wymagania, wzór umowy), '
            '"zmiana_opis": "co i gdzie zmienić w SWZ (gdy zmiana_swz)", '
            '"przedluzenie": true/false (czy zmiana jest istotna dla przygotowania ofert i wymaga przedłużenia terminu składania ofert – '
            + ("art. 137 Pzp" if unijne else "art. 286 ust. 3 Pzp") + '), "podstawa": "punkt dokumentu, na którym oparto odpowiedź"}')


def wyjasnienia_docx(sciezka, nazwa, znak, zamawiajacy, pytania, unijne, zmiany_terminu=None, termin_ofert="", godzina="", miejscowosc=""):
    """Wyjaśnienia treści SWZ (bez ujawniania źródła zapytań) i – jeśli były – zmiana SWZ z przedłużeniem terminu składania ofert."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(zamawiajacy or "[UZUPEŁNIJ: zamawiający]", rozmiar=9)
    A(f"{miejscowosc or '[UZUPEŁNIJ: miejscowość]'}, {dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    if znak:
        A(f"Znak sprawy: {znak}", rozmiar=9)
    A("Do wykonawców – strona internetowa prowadzonego postępowania", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    zm = [q for q in pytania if q.get("zmiana_swz") and zatwierdzona(q)]
    A("WYJAŚNIENIA TREŚCI SWZ" + (" I ZMIANA SWZ" if zm or zmiany_terminu else ""), pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"dotyczy: {nazwa or '[UZUPEŁNIJ: nazwa zamówienia]'}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    art_w, art_z = ("art. 135 ust. 2 i 6", "art. 137 ust. 1") if unijne else ("art. 284 ust. 2 i 6", "art. 286 ust. 1")
    pytania = [q for q in pytania if zatwierdzona(q)]  # tylko odpowiedzi zatwierdzone przez zamawiającego (bez projektów AI)
    zm = [q for q in pytania if q.get("zmiana_swz")]
    odp = list(pytania)
    A(f"Działając na podstawie {art_w} ustawy Prawo zamówień publicznych, Zamawiający udostępnia treść zapytań wraz z wyjaśnieniami, "
      "bez ujawniania źródła zapytania.")
    for i, q in enumerate(odp, 1):
        A(f"Pytanie {i}", pogrub=True)
        A(str(q.get("tresc") or ""))
        A(f"Odpowiedź {i}", pogrub=True)
        A(str(q.get("odpowiedz") or ""))
    if not odp:
        A("[UZUPEŁNIJ: pytania i odpowiedzi]")
    if zm:
        A("ZMIANA TREŚCI SWZ", pogrub=True)
        A(f"Na podstawie {art_z} ustawy Prawo zamówień publicznych Zamawiający zmienia treść SWZ:")
        for q in zm:
            A(str(q.get("zmiana_opis") or "[UZUPEŁNIJ: zmieniany punkt SWZ – dotychczasowe i nowe brzmienie]"), styl="List Bullet")
    if zmiany_terminu:
        z = zmiany_terminu[-1]
        nowy = _d(z.get("nowy"))
        A("PRZEDŁUŻENIE TERMINU SKŁADANIA OFERT", pogrub=True)
        import re as _re
        import kreator_zam as _KZ
        g_ok = bool(_re.fullmatch(r"\d{1,2}:\d{2}", str(godzina or "").strip()))
        otw = _KZ.termin_otwarcia(nowy.isoformat(), godzina) if g_ok else ""
        zw = nowy + dt.timedelta(days=89 if unijne else 29)  # najdłuższy termin związania; pierwszym dniem jest dzień składania ofert
        A(f"Na podstawie {'art. 137 ust. 6' if unijne else 'art. 286 ust. 3'} ustawy Prawo zamówień publicznych Zamawiający przedłuża termin składania "
          f"ofert do dnia {nowy:%d.%m.%Y} r., godz. {godzina if g_ok else '[UZUPEŁNIJ]'}" + (f" ({z['powod']})" if z.get("powod") else "")
          + f". Otwarcie ofert nastąpi w dniu {otw or '[UZUPEŁNIJ]'}, a termin związania ofertą upływa w dniu {zw:%d.%m.%Y} r. – odpowiednio zmienia się SWZ.")
        A("Zmiana ogłoszenia o zamówieniu: " + ("ogłoszenie o zmianach lub dodatkowych informacjach w Dzienniku Urzędowym UE." if unijne else
          "ogłoszenie o zmianie ogłoszenia w Biuletynie Zamówień Publicznych (art. 286 ust. 9 w zw. z art. 267 ust. 2 pkt 6 Pzp); "
          "komunikat o przedłużeniu terminu na stronie internetowej postępowania (art. 286 ust. 5)."), rozmiar=9)
    A("Wyjaśnienia i zmiany są wiążące dla wykonawców i stają się integralną częścią SWZ.")
    A("\n\n..........................................\n(podpis Kierownika Zamawiającego lub osoby upoważnionej)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("Projekt pisma przygotowany z pomocą programu – przed publikacją wymaga sprawdzenia.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
