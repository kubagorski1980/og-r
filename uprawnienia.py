# -*- coding: utf-8 -*-
"""
Role i uprawnienia użytkowników.

Każda rola ma poziom dostępu do każdego modułu: 0 – brak, 1 – podgląd, 2 – edycja,
oraz dwa uprawnienia dodatkowe: „ai” (uruchamianie AI: oferty, analizy, dokumenty) i „raporty” (pobieranie raportów i plików).
Administrator ma zawsze pełny dostęp (administrator konta – w obrębie swojej firmy). Role wbudowane może modyfikować (poza administratorem)
i dodawać własne tylko właściciel programu – role są wspólne dla wszystkich firm.
"""
import re

MODULY = {
    "przetargi": "Przetargi i BIP",
    "projekty": "Projekty, oferty, kosztorysy, dokumentacja",
    "realizacja": "Realizacja: harmonogram, protokoły, raporty dzienne, usterki",
    "finanse": "Finanse: faktury, koszty, rozliczenia, wartości umów",
    "klienci": "Klienci",
    "hurtownie": "Hurtownie i zamówienia",
    "pracownicy": "Pracownicy i roboczogodziny",
    "kadry": "Kadry: dokumenty i umowy pracowników",
    "place": "Płace (ZUS, podatek)",
    "firma": "Profil firmy",
    "archiwum": "Archiwum (przeglądanie i przywracanie)",
    "ustawienia": "Ustawienia programu",
    "uzytkownicy": "Użytkownicy i role",
}
NADAWANE_SWIADOMIE = ()  # domyślnie brak dostępu dla ról poza administratorem
POZIOMY = {0: "brak", 1: "podgląd", 2: "edycja"}

WSZYSTKO = {m: 2 for m in MODULY}
# Każde konto to osobna firma – swoje dane (pracownicy, profil firmy, klienci, hurtownie, archiwum) zarządza samo; Ustawienia i Użytkownicy –
# tylko administrator. H1-03: Płace i Kadry NIE są już stałe (dawniej każda rola dostawała Płace 2 i Kadry 2, więc stawki i wynagrodzenia
# widziały też role opisane jako „bez płac” / „bez finansów”) – obowiązuje definicja roli zgodna z jej opisem.
STALE_UPRAWNIENIA = {"pracownicy": 2, "firma": 2, "klienci": 2, "hurtownie": 2, "archiwum": 2, "ustawienia": 0, "uzytkownicy": 0}
STALE_DAWNIEJ = {"place": 2, "kadry": 2}  # do migracji zapisanych ról
# Wyjątki od stałych uprawnień (decyzja właściciela 03-12): kierownik budowy ma Archiwum = 1 (podgląd) – widzi listę poprzednich i usuniętych
# raportów dziennych oraz usterek; przywraca je przez moduł Realizacja (edycja), a projektów, klientów i pracowników z archiwum nie przywraca.
STALE_WYJATKI = {"kierownik_budowy": {"archiwum": 1}}
ROLE_WBUDOWANE = {
    "admin": {"nazwa": "Administrator", "opis": "pełny dostęp, także trwałe usuwanie", "uprawnienia": WSZYSTKO, "ai": True, "raporty": True,
              "wbudowana": True},
    "kierownik": {"nazwa": "Kierownik", "opis": "prowadzi projekty i budowy, widzi finanse i kadry",
                  "uprawnienia": {**{m: 2 for m in MODULY}, "place": 1, "ustawienia": 0, "uzytkownicy": 0, "archiwum": 1},
                  "ai": True, "raporty": True, "wbudowana": True},
    "uzytkownik": {"nazwa": "Pracownik biurowy", "opis": "przetargi, oferty, kosztorysy, realizacja – bez płac i ustawień",
                   "uprawnienia": {**{m: 2 for m in MODULY}, "kadry": 1, "place": 0, "firma": 1, "ustawienia": 0, "uzytkownicy": 0,
                                   "archiwum": 0}, "ai": True, "raporty": True, "wbudowana": True},
    "kierownik_budowy": {"nazwa": "Kierownik budowy", "opis": "raporty dzienne, zdjęcia, usterki, godziny – bez finansów i płac, przedmiar bez cen",
                         "uprawnienia": {**{m: 0 for m in MODULY}, "realizacja": 2, "projekty": 1, "pracownicy": 2, "hurtownie": 1,
                                         "klienci": 1, "firma": 1, "kadry": 1, "archiwum": 1}, "ai": False, "raporty": True, "wbudowana": True},
    "urzednik": {"nazwa": "Urzędnik (zamawiający)", "opis": "kosztorysy inwestorskie, dokumentacja przetargowa, inwestycje",
                 "uprawnienia": {**{m: 0 for m in MODULY}, "projekty": 2, "realizacja": 2, "finanse": 2, "klienci": 1, "firma": 1},
                 "ai": True, "raporty": True, "wbudowana": True},
    "podglad": {"nazwa": "Tylko podgląd", "opis": "przegląda i pobiera pliki, niczego nie zmienia",
                "uprawnienia": {**{m: 1 for m in MODULY}, "place": 0, "ustawienia": 0, "uzytkownicy": 0, "archiwum": 0, "kadry": 0},
                "ai": False, "raporty": True, "wbudowana": True},
}


def wszystkie_role(zapisane):
    """Role wbudowane (z ewentualnymi zmianami) + własne role firmy."""
    wyn = {}
    for k, r in ROLE_WBUDOWANE.items():
        wyn[k] = {**r, "uprawnienia": dict(r["uprawnienia"])}
    for k, r in (zapisane or {}).items():
        if k == "admin" or k.startswith("_") or not isinstance(r, dict):
            continue
        baza = wyn.get(k, {"wbudowana": False, "uprawnienia": {m: 0 for m in MODULY}})
        wyn[k] = {**baza, **{x: r[x] for x in ("nazwa", "opis", "ai", "raporty") if x in r},
                  "uprawnienia": {**baza["uprawnienia"], **{m: int(v) for m, v in (r.get("uprawnienia") or {}).items() if m in MODULY}}}
    for k, r in ROLE_WBUDOWANE.items():  # Księgowość: domyślnie brak dostępu – administrator nadaje ją świadomie (rola lub własna rola)
        for m_ in NADAWANE_SWIADOMIE:
            if k != "admin" and m_ not in ((zapisane or {}).get(k, {}).get("uprawnienia") or {}):
                wyn[k]["uprawnienia"][m_] = 0
    for k, r in wyn.items():  # zasady firmy: Ustawienia i Użytkownicy tylko dla administratora
        if k != "admin":
            r["uprawnienia"].update(STALE_UPRAWNIENIA)
            r["uprawnienia"].update(STALE_WYJATKI.get(k, {}))
    if "podglad" in wyn:  # „Tylko podgląd” niczego nie zmienia (także danych własnej firmy) – najwyżej poziom „podgląd”, bez AI
        wyn["podglad"]["uprawnienia"] = {m: min(1, int(v)) for m, v in wyn["podglad"]["uprawnienia"].items()}
        wyn["podglad"]["ai"] = False
    return wyn


def poziom(rola_def, modul):
    if not rola_def:
        return 0
    return int((rola_def.get("uprawnienia") or {}).get(modul, 0))


# ---------- przypisanie adresów API do modułów (kontrola po stronie serwera)
REGULY = [
    (r"^/api/projekty/[^/]+/(faktury|koszty)(/|$)", "finanse"),
    (r"^/api/projekty/[^/]+/rozliczenie", "finanse"),
    # dane umowy budowy (nr, daty, kierownik, inspektor, adres) – moduł Realizacja; wartość umowy i VAT zmienia tylko rola z edycją Finansów
    # (pilnuje tego trasa zapisu), wydruk HRF z kwotami etapów – Finanse
    (r"^/api/projekty/[^/]+/hrf/xlsx", "finanse"),
    # realizacja umów dostaw i usług (strona dostawcy): kwoty umowy, zamówień, faktur – cały moduł wymaga Finansów (H1-05)
    (r"^/api/projekty/[^/]+/dostawy", "finanse"),
    # godziny pracy na budowie (także udostępnionej) – wpisuje kierownik budowy z edycją Realizacji (H1-12)
    (r"^/api/projekty/[^/]+/godziny", "realizacja"),
    (r"^/api/projekty/[^/]+/(realizacja|hrf|protokol|dziennik|usterki|zdjecia|wykonawcy|formalnosci|transze|pogoda|rozliczenie-mat|podwykonawcy)", "realizacja"),
    (r"^/api/projekty/[^/]+/wykonawca/z-profilu", "projekty"),
    (r"^/api/projekty", "projekty"),
    (r"^/pobierz/", "projekty"),
    (r"^/api/realizacja", "realizacja"),
    (r"^/api/(przetargi|obszar|bip|bzp|bk)(/|$)", "przetargi"),  # także Baza Konkurencyjności (dane surowe ogłoszeń)
    (r"^/api/wyniki-ofert", "projekty"),
    (r"^/api/dostawy", "finanse"),
    (r"^/api/ocena-ofert", "projekty"),
    (r"^/api/zapytania", "projekty"),
    (r"^/api/zam/", "projekty"),
    (r"^/api/olioc", "projekty"),
    (r"^/api/sprawozdanie", "projekty"),
    (r"^/api/nier", "projekty"),
    (r"^/api/raporty", "przetargi"),
    (r"^/api/klienci", "klienci"),
    (r"^/api/(hurtownie|historia)", "hurtownie"),
    (r"^/api/cennik-wlasny", "projekty"),
    (r"^/api/dotacje", "projekty"),
    (r"^/api/(pracownicy|godziny)", "pracownicy"),
    (r"^/api/kadry", "kadry"),
    (r"^/api/place", "place"),
    (r"^/api/firma", "firma"),
    (r"^/api/archiwum", "archiwum"),
    (r"^/api/powiadomienia", "firma"),
    (r"^/api/konto/", "firma"),
    (r"^/api/(ustawienia|ai/test)", "ustawienia"),
    (r"^/api/(uzytkownicy|role)", "uzytkownicy"),
]
AI = re.compile(r"^/api/(projekty/[^/]+/(oferta|materialy|harmonogram|kontrola$|czat$|weryfikacja$|dokumentacja$|umowa$)|"
                r"przetargi/(ocen|analiza)|bip/odkryj|projekty/[^/]+/wnioski/[^/]+/(kosztorys|propozycja)$|projekty/[^/]+/(dotacja|wniosek-dot)/(analiza|przygotuj|sprawdz)$|dotacje/szukaj$|dotacje/harmonogram/odswiez$)")
NOTATKI = re.compile(r"^/api/projekty/[^/]+/notatki$")
# odczyty zapisywane jako POST (nie zmieniają danych)
POST_ODCZYT = re.compile(r"^/api/(place/lista$|pomoc$|konto/tryb$|przetargi/widziane$)")  # tryb i „przejrzane” – stan widoku użytkownika, nie dane firmy  # notatki: POST zawsze zapisuje (dopisanie, przypięcie, archiwum) – odczyt przez GET projektu


def modul_adresu(sciezka):
    for wzor, modul in REGULY:
        if re.match(wzor, sciezka):
            return modul
    return None


def sprawdz(rola_def, metoda, sciezka, dane_json=None):
    """None, gdy wolno; inaczej komunikat odmowy."""
    if rola_def is None:
        return "Brak uprawnień."
    if rola_def.get("uprawnienia") == WSZYSTKO and rola_def.get("ai") and rola_def.get("wbudowana") and rola_def.get("nazwa") == "Administrator":
        return None
    modul = modul_adresu(sciezka)
    if not modul:
        return None
    wym = 1 if metoda == "GET" or POST_ODCZYT.match(sciezka) else 2
    if modul == "projekty" and NOTATKI.match(sciezka) and poziom(rola_def, "realizacja") >= 2:
        modul = "realizacja"  # notatki budowy (telefony, ustalenia) dopisuje też kierownik budowy z edycją Realizacji
    if modul == "place" and sciezka == "/api/place/lista" and ((dane_json or {}).get("zapisz") or (dane_json or {}).get("usun")):
        wym = 2
    if poziom(rola_def, modul) < wym:
        return (f"Brak uprawnień do modułu „{MODULY[modul]}” ({'edycja' if wym == 2 else 'podgląd'}). "
                "Poproś administratora o zmianę roli.")
    if metoda != "GET" and AI.match(sciezka) and not rola_def.get("ai"):
        return "Twoja rola nie pozwala uruchamiać funkcji AI (oferty, analizy, generowanie dokumentów)."
    if metoda == "GET" and (sciezka.startswith("/pobierz/") or sciezka.endswith((".docx", ".xlsx"))) and not rola_def.get("raporty", True):
        return "Twoja rola nie pozwala pobierać plików i raportów."
    return None


def migruj_zapisane_role(zapisane):
    """H1-03: role zapisane przed tą wersją. Ekran ról wysyłał przy zapisie wymuszone wartości (Płace 2, Kadry 2…), więc w nadpisaniach ról
    wbudowanych nie są one świadomym wyborem – usuwamy je (obowiązuje definicja roli zgodna z opisem). Role własne dostają te wartości zapisane
    wprost (tak działały dotąd) – administrator może je teraz zmienić na ekranie ról. Zwraca (nowe_role, czy_zmieniono)."""
    if not isinstance(zapisane, dict) or zapisane.get("_wersja_uprawnien") == 2:
        return zapisane, False
    wyn = {}
    for k, r in zapisane.items():
        if not isinstance(r, dict) or k.startswith("_"):
            wyn[k] = r
            continue
        u = dict(r.get("uprawnienia") or {})
        if k in ROLE_WBUDOWANE:
            for m in STALE_DAWNIEJ:
                u.pop(m, None)
        else:
            u.update(STALE_DAWNIEJ)
        wyn[k] = {**r, "uprawnienia": u}
    wyn["_wersja_uprawnien"] = 2
    return wyn, True
