# -*- coding: utf-8 -*-
"""
Analiza przetargu dla zakładki „Przetargi”:
 - wstępna (automatycznie po wyszukaniu) – z treści ogłoszenia,
 - pełna (na żądanie) – z pobranych dokumentów zamówienia (SWZ, wzór umowy, przedmiar).
Wynik: ocena 1–10, rekomendacja i ok. 30 pól pogrupowanych tematycznie, żeby podstawowe informacje były od razu pod ręką.
"""
import json
import re

import modul_oferty as MO

GRUPY = [
    ("Najważniejsze", [("streszczenie", "Streszczenie"), ("zakres_robot", "Zakres robót"), ("lokalizacja_robot", "Miejsce robót"),
                       ("tryb", "Tryb / rodzaj postępowania"), ("czesci", "Podział na części")]),
    ("Terminy", [("termin_skladania", "Składanie ofert"), ("termin_pytan", "Pytania do SWZ do"), ("wizja_lokalna", "Wizja lokalna"),
                 ("termin_realizacji", "Termin realizacji"), ("termin_zwiazania", "Związanie ofertą")]),
    ("Pieniądze", [("szacowana_wartosc", "Szacowana wartość"), ("budzet", "Budżet zamawiającego"), ("wadium", "Wadium"),
                   ("zabezpieczenie", "Zabezpieczenie należytego wykonania"), ("wynagrodzenie", "Rodzaj wynagrodzenia"),
                   ("platnosci", "Płatności / zaliczki"), ("kary_umowne", "Kary umowne")]),
    ("Warunki udziału i ocena ofert", [("warunki_udzialu", "Warunki udziału"), ("doswiadczenie", "Wymagane doświadczenie"),
                                       ("osoby", "Wymagane osoby / uprawnienia"), ("sytuacja_finansowa", "OC / sytuacja finansowa"),
                                       ("kryteria_oceny", "Kryteria oceny ofert"), ("gwarancja", "Gwarancja / rękojmia"),
                                       ("dokumenty", "Dokumenty do oferty"), ("miejsce_skladania", "Gdzie złożyć ofertę")]),
    ("Ocena dla firmy", [("dopasowanie", "Dlaczego taka ocena"), ("ryzyka", "Ryzyka"), ("szanse", "Szanse / konkurencja"),
                         ("nastepne_kroki", "Co zrobić dalej"), ("brakujace", "Czego brakuje w ogłoszeniu")]),
]
KLUCZE = [k for _, pola in GRUPY for k, _ in pola]

SYSTEM = ("Jesteś doświadczonym analitykiem przetargów budowlanych w Polsce. Czytasz ogłoszenia i dokumentację zamówień "
          "i wyciągasz z nich konkretne informacje: liczby, daty, kwoty, wymagania. Piszesz zwięźle po polsku. "
          "Nie zmyślasz – czego nie ma w tekście, oznaczasz. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em, bez markdown.")


def polecenie(t, profil, z_dokumentami=False):
    zrodlo = "DOKUMENTY ZAMÓWIENIA (powyżej) oraz dane ogłoszenia" if z_dokumentami else "TREŚĆ OGŁOSZENIA"
    tresc = "" if z_dokumentami else f"\nTreść ogłoszenia:\n{(t.get('tresc') or '(brak treści w danych źródłowych)')[:15000]}\n"
    return (f"PROFIL FIRMY:\n{profil}\n\n"
            f"OGŁOSZENIE (źródło: {t.get('zrodlo', '')}, nr {t.get('numer', '')}):\n"
            f"Przedmiot: {t.get('przedmiot', '')}\nZamawiający: {t.get('zamawiajacy', '')}\nLokalizacja: {t.get('lokalizacja', '')}\n"
            f"Termin składania ofert z formularza ogłoszenia: {t.get('termin_ofert') or 'nie podano w formularzu – znajdź w treści'}\n"
            f"CPV: {t.get('cpv', '')}{tresc}\n"
            "UWAGA: termin składania ofert jest najczęściej na PIERWSZEJ STRONIE ogłoszenia / zapytania / SWZ albo w punkcie "
            "„Termin składania ofert” / „Miejsce i termin złożenia ofert”. Przeczytaj te miejsca uważnie – nie pisz „brak”, "
            "jeśli data jest gdziekolwiek w tekście. Termin z formularza ogłoszenia jest obowiązujący.\n"
            f"Na podstawie: {zrodlo}. Wypełnij JSON (wszystkie pola tekstowe, konkretnie – kwoty w zł, daty DD.MM.RRRR, liczby):\n"
            '{"ocena": 1-10 (dopasowanie do profilu firmy), "rekomendacja": "startujemy" | "do analizy" | "odpuszczamy",\n'
            ' "streszczenie": "2–3 zdania: co, gdzie, dla kogo, skala",\n'
            ' "zakres_robot": "główne roboty z ilościami, jeśli podane (np. docieplenie 1850 m², wymiana 120 okien)",\n'
            ' "lokalizacja_robot": "adres obiektu / miejscowość", "tryb": "np. tryb podstawowy bez negocjacji, zapytanie ofertowe",\n'
            ' "czesci": "czy podzielone na części i jakie; albo „bez podziału”",\n'
            ' "termin_skladania": "data i godzina", "termin_iso": "RRRR-MM-DDTGG:MM (lub RRRR-MM-DD) albo pusty", "termin_pytan": "…", "wizja_lokalna": "obowiązkowa / zalecana / brak + termin",\n'
            ' "termin_realizacji": "…", "termin_zwiazania": "…",\n'
            ' "szacowana_wartosc": "kwota netto; jeśli brak w tekście – orientacyjny szacunek z dopiskiem (szacunek AI)",\n'
            ' "budzet": "kwota, jaką zamawiający przeznaczył, jeśli podana", "wadium": "kwota i forma", "zabezpieczenie": "% ceny",\n'
            ' "wynagrodzenie": "ryczałtowe / kosztorysowe", "platnosci": "częściowe, zaliczki, termin płatności",\n'
            ' "kary_umowne": "najważniejsze kary (np. 0,2% za dzień zwłoki, limit)",\n'
            ' "warunki_udzialu": "krótko wszystkie warunki", "doswiadczenie": "wymagane referencje: ile robót, jakich, na jaką kwotę",\n'
            ' "osoby": "np. kierownik budowy z uprawnieniami bez ograniczeń w specjalności …", "sytuacja_finansowa": "OC, środki",\n'
            ' "kryteria_oceny": "kryteria z wagami", "gwarancja": "wymagana minimalna / punktowana", "dokumenty": "lista dokumentów do oferty",\n'
            ' "miejsce_skladania": "platforma / adres, forma (elektronicznie, podpis kwalifikowany)",\n'
            ' "dopasowanie": "1–2 zdania uzasadnienia oceny względem profilu firmy", "ryzyka": "najważniejsze ryzyka",\n'
            ' "szanse": "ocena szans (skala, wymagania, typowa konkurencja)", "nastepne_kroki": "2–4 konkretne kroki",\n'
            ' "brakujace": "czego nie ma w ' + ("dokumentach" if z_dokumentami else "ogłoszeniu – co sprawdzić w SWZ") + '"}\n'
            'Dla informacji, których nie ma w tekście, wpisz „brak w ' + ("dokumentach" if z_dokumentami else "ogłoszeniu") +
            '” (poza szacowaną wartością, którą możesz oszacować).')


def _wynik(tekst):
    d = MO.wyciagnij_json(tekst)
    try:
        ocena = max(1, min(10, int(round(float(str(d.get("ocena", "")).replace(",", "."))))))
    except (TypeError, ValueError):
        ocena = None
    rek = str(d.get("rekomendacja", "")).strip().lower()
    wyn = {"ocena": ocena, "rekomendacja": rek if rek in ("startujemy", "do analizy", "odpuszczamy") else "do analizy",
           "termin_iso": _jako_data(str(d.get("termin_iso") or "")) or data_i_godzina(d.get("termin_skladania"))}
    for k in KLUCZE:
        v = d.get(k, "")
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v)
        wyn[k] = re.sub(r"\s+", " ", str(v or "")).strip()[:1200]
    odw = [o for o in (d.get("odwolania") or []) if isinstance(o, dict) and (o.get("cytat") or o.get("miejsce"))]
    if odw:
        wyn["odwolania"] = [{k: str(o.get(k) or "")[:400] for k in ("pole", "dokument", "miejsce", "cytat")} for o in odw[:25]]
    return wyn


def wstepna(t, cfg, profil):
    import bip as BIP  # claude_prosty
    return _wynik(BIP.claude_prosty(cfg, SYSTEM, polecenie(t, profil), max_tokens=3500, model=cfg.get("model_lekki") or "claude-haiku-5-5"))  # wstępna ocena – model lekki (decyzja użytkownika)


ODWOLANIA_PELNA = ("\nDODATKOWO dodaj do JSON pole \"odwolania\": lista do 25 odwołań do dokumentów dla najważniejszych ustaleń – "
                   '[{"pole": "klucz pola, którego dotyczy (np. kary_umowne, warunki_udzialu, wadium, termin_realizacji, gwarancja, ryzyka)", '
                   '"dokument": "nazwa pliku", "miejsce": "§ 4 ust. 2 / pkt 3.1 / poz. 12 / str. 5", '
                   '"cytat": "DOSŁOWNY fragment z dokumentu, 20–300 znaków, znak w znak"}]. Program sprawdza cytaty w plikach i pokazuje je użytkownikowi.')


def pelna(t, cfg, profil, bloki, log):
    import ceny_rynkowe as CR
    tresc = MO.oznacz_dokumenty(bloki, MO.ustawienie_cache(cfg)) + [{"type": "text", "text": polecenie(t, profil, True) + ODWOLANIA_PELNA}]
    zap = {"model": cfg.get("model") or "claude-sonnet-5-5", "max_tokens": 8000, "system": SYSTEM,
           "messages": [{"role": "user", "content": tresc}]}
    odp = CR._post(cfg, zap)
    log(MO.opis_uzycia(odp.get("usage")) or "Analiza AI gotowa.")
    return _wynik("".join(b.get("text", "") for b in odp.get("content", []) if b.get("type") == "text"))


PRIORYTET = ("swz", "specyfikac", "siwz", "zapytanie", "ogloszenie", "ogłoszenie", "umow", "przedmiar", "opis przedmiotu", "opz",
             "formularz", "kosztorys")


def wybierz_pliki(sciezki, limit_bajtow):
    """Najpierw SWZ, ogłoszenie, wzór umowy, przedmiar; rysunki i duże pliki na końcu – do limitu wielkości zapytania."""
    import os

    def waga(p):
        n = os.path.basename(p).lower()
        idx = next((i for i, s in enumerate(PRIORYTET) if s in n), len(PRIORYTET))
        rysunek = any(s in n for s in ("rys", "rzut", "przekr", "elewac", ".dwg", "detal"))
        return (rysunek, idx, os.path.getsize(p))
    wyn, suma = [], 0
    for p in sorted(sciezki, key=waga):
        b, n, _ = MO.przygotuj_blok_tekstowy(p)
        if not b or suma + n > limit_bajtow:
            continue
        wyn += b
        suma += n
    return wyn, suma


# ============================================================ termin składania ofert

import datetime as _dt  # noqa: E402

MIESIACE_PL = {"stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6, "lipca": 7, "sierpnia": 8,
               "wrzesnia": 9, "pazdziernika": 10, "listopada": 11, "grudnia": 12}
RE_DATA = (r"(\d{1,2})\s*[.\-/]\s*(\d{1,2})\s*[.\-/]\s*(\d{4})|(\d{4})-(\d{2})-(\d{2})|"
           r"(\d{1,2})\s+(" + "|".join(MIESIACE_PL) + r")\s+(\d{4})")
RE_GODZ = r"(?:\s*r\.?)?[\s,]*(?:\(|o\s+|do\s+|w\s+)?(?:godz(?:iny|inie|\.)?|g\.)?\s*(\d{1,2})[:.](\d{2})"
FRAZY = (r"termin\w*\s+(?:na\s+)?(?:skladania|zlozenia|zlozenie|skladanie|przeslania|wplywu|otwarcia)\s+ofert\w*",
         r"ofert\w*\s+(?:nalezy|mozna|trzeba)\s+(?:zlozyc|skladac|przeslac|dostarczyc)",
         r"(?:zlozyc|skladac|przeslac)\s+ofert\w*", r"oferty\s+(?:przyjmowane\s+sa|beda\s+przyjmowane)", r"offer\w*\s+deadline",
         r"submission\s+deadline")
BEZ_OGONKOW = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")


def _data_z_dopasowania(m):
    try:
        if m.group(1):
            d = _dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        elif m.group(4):
            d = _dt.date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
        else:
            d = _dt.date(int(m.group(9)), MIESIACE_PL[m.group(8).lower().translate(BEZ_OGONKOW)], int(m.group(7)))
    except (ValueError, KeyError):
        return None
    return d if 2020 <= d.year <= 2035 else None


def data_i_godzina(tekst):
    """Pierwsza data (z godziną, jeśli jest) w krótkim tekście, np. „12 października 2026 r., godz. 9:00”."""
    t = re.sub(r"\s+", " ", str(tekst or "")).translate(BEZ_OGONKOW)
    m = re.search(RE_DATA, t, re.I)
    d = _data_z_dopasowania(m) if m else None
    if not d:
        return None
    g = re.match(RE_GODZ, t[m.end():m.end() + 40], re.I)
    return f"{d.isoformat()}T{int(g.group(1)):02d}:{g.group(2)}" if g and int(g.group(1)) < 24 and int(g.group(2)) < 60 else d.isoformat()


def termin_z_tekstu(tekst):
    """Termin składania ofert z tekstu ogłoszenia / SWZ (np. „Termin składania ofert: 20.10.2026 r. godz. 10:00”).
    Zwraca „RRRR-MM-DDTGG:MM” albo „RRRR-MM-DD”, albo None."""
    if not tekst:
        return None
    t = re.sub(r"\s+", " ", str(tekst)).translate(BEZ_OGONKOW)
    for fraza in FRAZY:
        for f in re.finditer(fraza, t, re.I):
            okno = t[f.end():f.end() + 220]
            m = re.search(RE_DATA, okno, re.I)
            if not m or m.start() > 180:
                continue
            d = _data_z_dopasowania(m)
            if not d:
                continue
            g = re.match(RE_GODZ, okno[m.end():m.end() + 40], re.I)
            if g and int(g.group(1)) < 24 and int(g.group(2)) < 60:
                return f"{d.isoformat()}T{int(g.group(1)):02d}:{g.group(2)}"
            return d.isoformat()
    return None


KLUCZE_TERMINU = ("submissiondeadline", "offerdeadline", "offerssubmission", "submittingoffers", "offersdeadline", "deadline",
                  "termin", "submission", "offer", "closing", "enddate", "dateto")


def _jako_data(v):
    if not isinstance(v, str):
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}))?", v.strip())
    if m:
        try:  # data i godzina muszą istnieć (np. „2026-12-15T25:00”, „2027-02-31” – odrzucone)
            _dt.datetime.strptime(m.group(1) + " " + (m.group(2) or "00:00"), "%Y-%m-%d %H:%M")
        except ValueError:
            return None
        return m.group(1) + (f"T{m.group(2)}" if m.group(2) and m.group(2) != "00:00" else "")
    return data_i_godzina(v)


def termin_z_danych(obj):
    """Termin z danych formularza ogłoszenia (np. JSON Bazy Konkurencyjności) – po nazwach pól."""
    znal = []

    def szukaj(o, sciezka=""):
        if isinstance(o, dict):
            for k, v in o.items():
                kl = re.sub(r"[^a-z]", "", str(k).lower())
                if isinstance(v, (dict, list)):
                    szukaj(v, sciezka + "/" + kl)
                    continue
                waga = next((i for i, x in enumerate(KLUCZE_TERMINU) if x in kl), None)
                if waga is not None and not any(x in kl for x in ("publication", "publish", "created", "modified", "start", "open",
                                                                    "realiz", "contract", "execution", "umow", "wykonan")):
                    d = _jako_data(v)
                    if d:
                        znal.append((waga, d))
        elif isinstance(o, list):
            for x in o:
                szukaj(x, sciezka)
    szukaj(obj)
    return sorted(znal)[0][1] if znal else None


def tekst_z_pdf(sciezka, strony=3):
    """Tekst pierwszych stron PDF (tam zwykle jest termin składania ofert). Wymaga biblioteki pypdf."""
    try:
        from pypdf import PdfReader
        r = PdfReader(sciezka)
        return "\n".join((r.pages[i].extract_text() or "") for i in range(min(strony, len(r.pages))))
    except Exception:
        return ""


# ---------- szybka ocena wielu przetargów w jednym zapytaniu (paczki) – instrukcja i profil firmy wysyłane raz

SYSTEM_PACZKA = ("Jesteś doświadczonym analitykiem przetargów budowlanych w Polsce. Oceniasz, czy ogłoszenia pasują do profilu firmy. "
                 "Piszesz zwięźle po polsku, nie zmyślasz. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em, bez markdown.")

INSTRUKCJA_PACZKI = (
    "Dla KAŻDEGO ogłoszenia z listy (pole nr) zwróć ocenę dopasowania do profilu firmy. Zwróć JSON:\n"
    '{"oceny": [{"nr": "numer ogłoszenia dokładnie jak na liście", "ocena": 1-10, "rekomendacja": "startujemy" | "do analizy" | "odpuszczamy", '
    '"streszczenie": "1 zdanie: co, gdzie, skala", "dopasowanie": "1 zdanie uzasadnienia oceny względem profilu", '
    '"termin_iso": "RRRR-MM-DDTGG:MM albo RRRR-MM-DD albo pusty – termin składania ofert", '
    '"szacowana_wartosc": "kwota z ogłoszenia albo orientacyjny szacunek z dopiskiem (szacunek AI)", '
    '"zakres": "roboty | dostawy | uslugi – rodzaj zamówienia"}]}\n'
    "Oceń wszystkie ogłoszenia, w tej samej kolejności. Termin z formularza ogłoszenia jest obowiązujący.")


def ocena_paczki(lista, cfg, profil, uzyj_cache=True):
    """Szybka ocena 10–15 przetargów jednym zapytaniem. Instrukcja i profil są w stałym początku zapytania
    (pamięć podręczna promptu – kolejne paczki w ciągu kilku minut czytają je taniej). Zwraca {nr: wynik}."""
    import ceny_rynkowe as CR
    stale = f"{INSTRUKCJA_PACZKI}\n\nPROFIL FIRMY:\n{profil}"
    system = [{"type": "text", "text": SYSTEM_PACZKA}, {"type": "text", "text": stale}]
    if uzyj_cache:
        system[-1]["cache_control"] = {"type": "ephemeral"}
    pozycje = []
    for t in lista:
        pozycje.append(f"--- nr: {t.get('numer', '')}\nPrzedmiot: {t.get('przedmiot', '')}\nZamawiający: {t.get('zamawiajacy', '')}\n"
                       f"Lokalizacja: {t.get('lokalizacja', '') or t.get('miasto', '')}\nTermin z formularza: {t.get('termin_ofert') or 'nie podano'}\n"
                       f"CPV: {t.get('cpv', '')}\nTreść (początek): {(t.get('tresc') or '')[:2500]}")
    zap = {"model": cfg.get("model_lekki") or "claude-haiku-5-5", "max_tokens": min(16000, 400 * len(lista) + 600), "system": system,
           "messages": [{"role": "user", "content": "OGŁOSZENIA DO OCENY:\n\n" + "\n\n".join(pozycje)}]}
    odp = CR._post(cfg, zap)
    d = MO.wyciagnij_json("".join(b.get("text", "") for b in odp.get("content", []) if b.get("type") == "text"))
    wyn = {}
    for o in (d.get("oceny") if isinstance(d, dict) else None) or []:
        if not isinstance(o, dict) or not o.get("nr"):
            continue
        try:
            ocena = max(1, min(10, int(round(float(str(o.get("ocena", "")).replace(",", "."))))))
        except (TypeError, ValueError):
            continue
        rek = str(o.get("rekomendacja", "")).strip().lower()
        wyn[str(o["nr"]).strip()] = {"ocena": ocena, "rekomendacja": rek if rek in ("startujemy", "do analizy", "odpuszczamy") else "do analizy",
                                     "streszczenie": str(o.get("streszczenie") or "")[:600], "dopasowanie": str(o.get("dopasowanie") or "")[:600],
                                     "szacowana_wartosc": str(o.get("szacowana_wartosc") or "")[:200],
                                     "termin_iso": _jako_data(str(o.get("termin_iso") or "")), "zakres": str(o.get("zakres") or "")[:30]}
    return wyn, odp.get("usage") or {}
