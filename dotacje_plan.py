# -*- coding: utf-8 -*-
"""Plan projektu dotacyjnego – jeden model dla każdej dotacji (szkolenia, IT, rolnictwo, OZE, wspólnoty, NGO, gminy…):
typ wnioskodawcy → działania z naboru → pozycje kosztów z kategorii katalogu (formularz, wycena, wskaźniki) → budżet i dotacja
→ wskaźniki i harmonogram → punkty i zgodność z regulaminem → wniosek → wybór wykonawcy, rozliczenie i trwałość."""
import datetime as dt
import json
import re

# ---------------------------------------------------------------- typy wnioskodawców i ich dane
TYPY_WNIOSKODAWCY = {
    "firma": {"nazwa": "Przedsiębiorstwo", "pola": [
        ("wielkosc", "Wielkość", "wybor", ["mikro", "mała", "średnia", "duża"]), ("pkd", "Główne PKD", "tekst", None),
        ("zatrudnienie", "Zatrudnienie (etaty)", "liczba", None), ("de_minimis", "Pomoc de minimis w ostatnich 3 latach [zł]", "liczba", None)]},
    "rolnik": {"nazwa": "Rolnik / gospodarstwo rolne", "pola": [
        ("nr_ep", "Numer identyfikacyjny ARiMR (EP)", "tekst", None), ("ha", "Powierzchnia użytków rolnych [ha]", "liczba", None),
        ("produkcja", "Główna produkcja (np. zboża, mleko, trzoda, sady)", "tekst", None), ("wielkosc_ekonomiczna", "Wielkość ekonomiczna (SO) [EUR]", "liczba", None)]},
    "jst": {"nazwa": "Gmina / powiat / województwo", "pola": [
        ("mieszkancy", "Liczba mieszkańców", "liczba", None), ("pzp", "Stosuje ustawę Pzp", "wybor", ["tak"])]},
    "szkola": {"nazwa": "Szkoła / uczelnia / jednostka naukowa", "pola": [
        ("organ", "Organ prowadzący", "tekst", None), ("uczniowie", "Liczba uczniów / studentów", "liczba", None)]},
    "ngo": {"nazwa": "Organizacja pozarządowa", "pola": [
        ("krs", "KRS", "tekst", None), ("projekty", "Zrealizowane projekty (liczba)", "liczba", None), ("obszar", "Obszar działania", "tekst", None)]},
    "wspolnota": {"nazwa": "Wspólnota / spółdzielnia mieszkaniowa", "pola": [
        ("lokale", "Liczba lokali", "liczba", None), ("powierzchnia", "Powierzchnia użytkowa budynku [m²]", "liczba", None),
        ("rok_budowy", "Rok budowy", "liczba", None)]},
    "osoba": {"nazwa": "Osoba fizyczna", "pola": [
        ("dochod", "Przeciętny dochód na osobę [zł/mies.]", "liczba", None), ("budynek", "Rodzaj budynku (dom jednorodzinny…)", "tekst", None)]},
}

# ---------------------------------------------------------------- katalog kategorii kosztów
# pola: (id, etykieta, typ, opcje/jednostka); wycena: kosztorys | rynek | bur | stawki | oferta | naboru
KATALOG = {
    "roboty": {"nazwa": "Roboty budowlane", "opis": "budowa, przebudowa, remont, termomodernizacja, infrastruktura", "wycena": "kosztorys",
               "pola": [("obiekt", "Obiekt", "wybor", ["dom jednorodzinny", "budynek wielorodzinny", "budynek gospodarczy / inwentarski", "hala / magazyn",
                                                    "szkoła / budynek publiczny", "biuro / lokal usługowy", "droga / infrastruktura", "inny"]),
                        ("zakres", "Zakres robót", "multi", ["ocieplenie ścian", "ocieplenie dachu / stropu", "wymiana okien", "wymiana drzwi",
                                                             "źródło ciepła", "instalacja c.o. / c.w.u.", "wentylacja z odzyskiem ciepła", "remont pomieszczeń",
                                                             "budowa / rozbudowa", "drogi / chodniki", "sieci wod.-kan.", "inne"]),
                        ("powierzchnia", "Powierzchnia [m²]", "liczba", "m²"), ("rok_budowy", "Rok budowy", "liczba", None),
                        ("audyt", "Audyt energetyczny / projekt", "wybor", ["mam", "trzeba wykonać", "nie dotyczy"])],
               "wskazniki": ["oszczednosc_energii", "powierzchnia"], "dokumenty": ["kosztorys inwestorski", "pozwolenie / zgłoszenie robót",
                                                                                  "audyt energetyczny (przy termomodernizacji)", "protokoły odbioru"]},
    "energia": {"nazwa": "Instalacje energetyczne (OZE)", "opis": "fotowoltaika, pompa ciepła, magazyn energii, kolektory, biogaz", "wycena": "rynek",
                "pola": [("rodzaj", "Rodzaj instalacji", "wybor", ["fotowoltaika", "pompa ciepła", "magazyn energii", "kolektory słoneczne",
                                                                 "biogazownia", "turbina wiatrowa", "inny"]),
                         ("moc", "Moc [kW / kWp]", "liczba", "kW"), ("magazyn", "Pojemność magazynu [kWh]", "liczba", "kWh"),
                         ("zuzycie", "Roczne zużycie energii [kWh]", "liczba", "kWh"), ("montaz", "Montaż", "wybor", ["dach", "grunt", "budynek", "nie dotyczy"])],
                "wskazniki": ["moc_oze", "produkcja_oze", "co2"], "dokumenty": ["oferty / specyfikacja", "warunki przyłączenia / zgłoszenie do OSD",
                                                                                  "protokół odbioru i uruchomienia"]},
    "maszyny": {"nazwa": "Maszyny i urządzenia", "opis": "rolnicze, produkcyjne, medyczne, laboratoryjne, pojazdy", "wycena": "rynek",
                "pola": [("rodzaj", "Rodzaj", "wybor", ["ciągnik", "kombajn", "opryskiwacz", "siewnik / sadzarka", "rozsiewacz nawozu", "pług / brona / agregat",
                                                       "prasa / owijarka", "ładowacz / ładowarka", "przyczepa", "maszyna do sadu / warzyw",
                                                       "obrabiarka CNC", "linia produkcyjna", "wózek widłowy", "kompresor / urządzenie techniczne",
                                                       "sprzęt medyczny", "sprzęt laboratoryjny", "pojazd", "inne"]),
                         ("parametry", "Parametry (moc, szerokość robocza, pojemność…)", "tekst", None), ("ilosc", "Liczba sztuk", "liczba", "szt."),
                         ("nowe", "Stan", "wybor", ["nowe", "używane"])],
                "wskazniki": ["srodki_trwale"], "dokumenty": ["oferty (porównanie cen)", "faktura i dowód zapłaty", "protokół odbioru", "ewidencja środków trwałych"]},
    "it": {"nazwa": "IT i cyfryzacja", "opis": "sprzęt, licencje, wdrożenie systemów (ERP, CRM), sklep internetowy, cyberbezpieczeństwo", "wycena": "rynek",
           "pola": [("rodzaj", "Rodzaj", "multi", ["sprzęt komputerowy", "oprogramowanie / licencje", "wdrożenie ERP / CRM", "sklep / platforma internetowa",
                                                   "e-usługi", "cyberbezpieczeństwo", "chmura / serwery", "automatyzacja / AI"]),
                    ("stanowiska", "Liczba stanowisk / użytkowników", "liczba", "szt."), ("moduly", "Moduły / funkcje", "tekst", None),
                    ("miesiace", "Czas wdrożenia [mies.]", "liczba", "mies.")],
           "wskazniki": ["wdrozone_systemy", "e_uslugi", "stanowiska"], "dokumenty": ["specyfikacja / oferty", "protokół wdrożenia", "licencje"]},
    "szkolenia": {"nazwa": "Szkolenia i kompetencje", "opis": "kursy, certyfikaty, studia podyplomowe, doradztwo rozwojowe", "wycena": "bur",
                  "pola": [("temat", "Temat / kompetencja", "tekst", None), ("osoby", "Liczba uczestników", "liczba", "os."),
                           ("godziny", "Godziny na osobę", "liczba", "h"), ("forma", "Forma", "wybor", ["stacjonarna", "zdalna", "mieszana"]),
                           ("certyfikat", "Kończy się certyfikatem / egzaminem", "wybor", ["tak", "nie"])],
                  "wskazniki": ["przeszkoleni", "certyfikaty", "osobogodziny"], "dokumenty": ["karta usługi (Baza Usług Rozwojowych)", "lista obecności",
                                                                                              "zaświadczenia / certyfikaty", "ankiety"]},
    "personel": {"nazwa": "Personel projektu", "opis": "wynagrodzenia zespołu projektowego", "wycena": "stawki",
                 "pola": [("stanowisko", "Stanowisko", "tekst", None), ("etat", "Wymiar (etat)", "liczba", "etatu"), ("miesiace", "Liczba miesięcy", "liczba", "mies."),
                          ("stawka", "Wynagrodzenie brutto z kosztami pracodawcy [zł/mies.]", "liczba", "zł")],
                 "wskazniki": ["miejsca_pracy"], "dokumenty": ["umowy / zakresy obowiązków", "listy płac", "ewidencja czasu pracy"]},
    "uslugi": {"nazwa": "Usługi zewnętrzne", "opis": "doradztwo, audyt, ekspertyzy, prace B+R, projekt, nadzór", "wycena": "oferta",
               "pola": [("rodzaj", "Rodzaj", "wybor", ["doradztwo", "audyt energetyczny", "ekspertyza / opinia", "prace B+R (podwykonawca)", "projekt / dokumentacja",
                                                      "nadzór inwestorski", "usługa marketingowa", "inna"]),
                        ("zakres", "Zakres usługi", "tekst", None)],
               "wskazniki": [], "dokumenty": ["umowa / zlecenie", "protokół odbioru usługi", "produkt usługi (raport, projekt)"]},
    "miekkie": {"nazwa": "Działania miękkie (społeczne, edukacyjne)", "opis": "warsztaty, wydarzenia, wsparcie uczestników – projekty NGO, EFS+", "wycena": "naboru",
                "pola": [("grupa", "Grupa docelowa", "tekst", None), ("uczestnicy", "Liczba uczestników", "liczba", "os."),
                         ("dzialania", "Działania (warsztaty, spotkania, wsparcie…)", "tekst", None), ("miesiace", "Czas trwania [mies.]", "liczba", "mies.")],
                "wskazniki": ["uczestnicy"], "dokumenty": ["listy obecności", "dokumentacja zdjęciowa", "formularze rekrutacyjne", "ankiety rezultatów"]},
    "niematerialne": {"nazwa": "Wartości niematerialne", "opis": "patenty, licencje, know-how, prawa autorskie", "wycena": "oferta",
                      "pola": [("przedmiot", "Przedmiot", "tekst", None)], "wskazniki": [], "dokumenty": ["umowa nabycia", "wycena / opinia rzeczoznawcy"]},
    "promocja": {"nazwa": "Promocja i rynki zagraniczne", "opis": "targi, misje gospodarcze, materiały promocyjne", "wycena": "rynek",
                 "pola": [("wydarzenia", "Wydarzenia / kraje", "tekst", None), ("liczba", "Liczba wydarzeń", "liczba", "szt.")],
                 "wskazniki": ["wydarzenia"], "dokumenty": ["faktury", "potwierdzenie udziału", "materiały"]},
    "inne": {"nazwa": "Inne koszty", "opis": "grunt, koszty pośrednie, wkład rzeczowy, inne", "wycena": "oferta",
             "pola": [("opis", "Opis", "tekst", None)], "wskazniki": [], "dokumenty": ["dokumenty potwierdzające wydatek"]},
}

# szacunki do wskaźników – zawsze opisane jako szacunek
PROD_PV_KWH_NA_KWP = 1000  # średnia roczna produkcja instalacji PV w Polsce (szacunek)
CO2_KG_NA_KWH = 0.7  # szacunkowa emisja CO2 z energii elektrycznej z sieci w Polsce – do potwierdzenia aktualnym wskaźnikiem KOBiZE


def _f(x):
    return liczba(x, 0.0)


def _gr(x):
    """Zaokrąglenie do grosza „połówki w górę” (73 125,325 → 73 125,33), jak w dokumentach finansowych."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _atr(p):
    """Atrybuty pozycji – zawsze słownik (wpis z błędem nie blokuje planu – GC-03)."""
    a = p.get("atrybuty") if isinstance(p, dict) else None
    return a if isinstance(a, dict) else {}


def _lista(v):
    return v if isinstance(v, list) else ([v] if isinstance(v, str) and v else [])


def intensywnosc_z_tekstu(t):
    """Intensywność z opisu naboru: „do 85%”, „od 50% do 85%”, „85,5 %” → najwyższy procent (0–100); bez „%” – liczba ≤ 100; inaczej None (GC-04).
    Wcześniej z „od 50% do 85%” powstawało 5085%."""
    if t in (None, ""):
        return None
    if isinstance(t, (int, float)):
        return float(t) if 0 < float(t) <= 100 else None
    tx = str(t)
    L = [float(x.replace(",", ".")) for x in re.findall(r"(\d{1,3}(?:[.,]\d+)?)\s*%", tx)]
    if not L:
        L = [float(x.replace(",", ".")) for x in re.findall(r"(?<![\d.,])(\d{1,3}(?:[.,]\d+)?)(?![\d.,])", tx)]
    L = [x for x in L if 0 < x <= 100]
    return max(L) if L else None


def wskazniki(pozycje):
    """Wskaźniki projektu wyliczone z pozycji (szacunki – do potwierdzenia w audycie / ofertach)."""
    w = {}

    def dodaj(k, nazwa, wart, jedn, uwaga=""):
        if wart:
            x = w.setdefault(k, {"nazwa": nazwa, "wartosc": 0, "jednostka": jedn, "uwaga": uwaga})
            x["wartosc"] = round(x["wartosc"] + wart, 2)
    for p in pozycje:
        a, kat = _atr(p), p.get("kategoria")
        if kat == "energia":
            moc, rodz = _f(a.get("moc")), a.get("rodzaj", "")
            dodaj("moc_oze", "Dodatkowa moc OZE", moc, "kW")
            if rodz == "fotowoltaika":
                prod = moc * PROD_PV_KWH_NA_KWP / 1000
                dodaj("produkcja_oze", "Produkcja energii z OZE", prod, "MWh/rok", "szacunek: ok. 1000 kWh z 1 kWp rocznie")
                dodaj("co2", "Szacowany spadek emisji CO₂", prod * CO2_KG_NA_KWH, "t/rok", "szacunek – potwierdź wskaźnikiem KOBiZE / audytem")
            if _f(a.get("magazyn")):
                dodaj("magazyn", "Pojemność magazynów energii", _f(a.get("magazyn")), "kWh")
        elif kat == "roboty":
            if any("ociepl" in z or "okien" in z or "źródło" in z for z in _lista(a.get("zakres")) if isinstance(z, str)):
                dodaj("powierzchnia", "Powierzchnia zmodernizowanych budynków", _f(a.get("powierzchnia")), "m²")
                dodaj("oszczednosc_energii", "Budynki poddane termomodernizacji", 1, "szt.", "oszczędność energii – z audytu energetycznego")
        elif kat == "maszyny":
            dodaj("srodki_trwale", "Zakupione maszyny i urządzenia", _f(a.get("ilosc")) or 1, "szt.")
        elif kat == "it":
            r = [x for x in _lista(a.get("rodzaj")) if isinstance(x, str)]
            if any("wdrożenie" in x or "automatyzacja" in x for x in r):
                dodaj("wdrozone_systemy", "Wdrożone systemy / rozwiązania cyfrowe", 1, "szt.")
            if any("e-usług" in x or "sklep" in x for x in r):
                dodaj("e_uslugi", "Udostępnione e-usługi", 1, "szt.")
            dodaj("stanowiska", "Stanowiska objęte cyfryzacją", _f(a.get("stanowiska")), "szt.")
        elif kat == "szkolenia":
            os_ = _f(a.get("osoby"))
            dodaj("przeszkoleni", "Osoby przeszkolone", os_, "os.")
            dodaj("osobogodziny", "Godziny szkoleń (osobogodziny)", os_ * _f(a.get("godziny")), "h")
            if a.get("certyfikat") == "tak":
                dodaj("certyfikaty", "Osoby z certyfikatem / kwalifikacją", os_, "os.")
        elif kat == "personel":
            dodaj("miejsca_pracy", "Etaty w projekcie", _f(a.get("etat")), "etatu")
        elif kat == "miekkie":
            dodaj("uczestnicy", "Uczestnicy projektu", _f(a.get("uczestnicy")), "os.")
        elif kat == "promocja":
            dodaj("wydarzenia", "Wydarzenia promocyjne / targi", _f(a.get("liczba")), "szt.")
    return list(w.values())


def budzet(pozycje, reguly, nabor_intens=None):
    """Budżet: koszty kwalifikowalne, VAT, dotacja wg intensywności kategorii i limitów, wkład własny, ostrzeżenia."""
    reg = reguly or {}
    ostrz = []
    kat_reg = {k.get("id"): k for k in (reg.get("kategorie") or []) if isinstance(k, dict)}
    domysl = intensywnosc_z_tekstu(reg.get("intensywnosc_procent")) or intensywnosc_z_tekstu(nabor_intens) or 0.0
    if _f(reg.get("intensywnosc_procent")) > 100:
        ostrz.append(f"Intensywność {reg.get('intensywnosc_procent')}% jest większa niż 100% – popraw ją w „Zasadach naboru” (do obliczeń przyjęto 0%).")
    wiersze = []
    suma = {"netto": 0.0, "vat": 0.0, "brutto": 0.0, "kwal": 0.0, "niekwal": 0.0, "dotacja": 0.0}
    per_kat = {}
    for p in pozycje:  # kwoty wierszy w groszach – suma = suma wierszy z tabeli (GC-04)
        netto = _gr(_f(p.get("ilosc") or 1) * _f(p.get("cena_netto")))
        vat = _gr(netto * _f(p.get("vat") if p.get("vat") not in (None, "") else 23) / 100)
        r = kat_reg.get(p.get("kategoria")) or {}
        kwal_kat = r.get("kwalifikowalna", True) is not False
        kwal = netto + (vat if reg.get("vat_kwalifikowalny") else 0) if (kwal_kat and p.get("kwalifikowalna", True) is not False) else 0.0
        intens = intensywnosc_z_tekstu(r.get("intensywnosc_procent")) or domysl
        kwal = _gr(kwal)
        dot = _gr(kwal * intens / 100)
        if not kwal_kat:
            ostrz.append(f"„{p.get('nazwa')}”: kategoria „{KATALOG.get(p.get('kategoria'), {}).get('nazwa', p.get('kategoria'))}” "
                         f"nie jest kwalifikowalna w tym naborze{(' – ' + r['uwagi']) if r.get('uwagi') else ''}.")
        per_kat.setdefault(p.get("kategoria"), [0.0, 0.0])
        per_kat[p.get("kategoria")][0] += kwal
        per_kat[p.get("kategoria")][1] += dot
        wiersze.append({"id": p.get("id"), "nazwa": p.get("nazwa"), "kategoria": p.get("kategoria"), "netto": round(netto, 2), "vat": round(vat, 2),
                        "kwalifikowalne": round(kwal, 2), "intensywnosc": intens, "dotacja": round(dot, 2)})
        suma["netto"] += netto
        suma["vat"] += vat
        suma["brutto"] += netto + vat
        suma["kwal"] += kwal
        suma["niekwal"] += netto + vat - kwal
        suma["dotacja"] += dot
    for k, (kw, dt_) in per_kat.items():  # limity kategorii
        lim = _f((kat_reg.get(k) or {}).get("limit_zl"))
        if lim and dt_ > lim:
            ostrz.append(f"Dotacja w kategorii „{KATALOG.get(k, {}).get('nazwa', k)}” ({dt_:,.0f} zł) przekracza limit {lim:,.0f} zł – przyjęto limit.".replace(",", " "))
            suma["dotacja"] -= dt_ - lim
    lim_p = _f(reg.get("limit_projektu_zl"))
    if lim_p and suma["dotacja"] > lim_p:
        ostrz.append(f"Dotacja ({suma['dotacja']:,.0f} zł) przekracza limit na projekt {lim_p:,.0f} zł – przyjęto limit.".replace(",", " "))
        suma["dotacja"] = lim_p
    mn = _f(reg.get("min_koszty_zl"))
    if mn and suma["kwal"] and suma["kwal"] < mn:
        ostrz.append(f"Koszty kwalifikowalne ({suma['kwal']:,.0f} zł) są niższe niż minimum naboru {mn:,.0f} zł.".replace(",", " "))
    mx = _f(reg.get("max_koszty_zl"))
    if mx and suma["kwal"] > mx:
        ostrz.append(f"Koszty kwalifikowalne ({suma['kwal']:,.0f} zł) przekraczają maksimum naboru {mx:,.0f} zł.".replace(",", " "))
    if not domysl and not any(intensywnosc_z_tekstu((kat_reg.get(p.get('kategoria')) or {}).get('intensywnosc_procent')) for p in pozycje):
        ostrz.append("Nie ustalono intensywności dofinansowania – uruchom analizę naboru albo wpisz intensywność ręcznie.")
    if (reg.get("pomoc") or "").startswith("de minimis"):
        ostrz.append("Pomoc de minimis – sprawdź limit pomocy otrzymanej w ostatnich 3 latach (dane w profilu wnioskodawcy).")
    suma = {k: round(v, 2) for k, v in suma.items()}
    suma["wklad_wlasny"] = round(suma["brutto"] - suma["dotacja"], 2)
    return {"wiersze": wiersze, "suma": suma, "ostrzezenia": ostrz}


MAX_MIESIECY = 120


def harmonogram(pozycje, start=None):
    """Harmonogram z pozycji: miesiąc od–do (od początku realizacji), domyślnie po kolei: usługi i projekt → roboty → zakupy → szkolenia."""
    kol = {"uslugi": 1, "niematerialne": 1, "roboty": 2, "energia": 3, "maszyny": 3, "it": 3, "szkolenia": 4, "miekkie": 4, "promocja": 4, "personel": 0, "inne": 2}
    wyn = []
    for p in pozycje:
        mies = lambda v: max(0, min(MAX_MIESIECY, int(_f(v))))  # miesiące realizacji 1–120 (np. „1e9” nie rysuje miliarda kolumn – GC-03)
        od = mies(p.get("miesiac_od")) or kol.get(p.get("kategoria"), 2)
        do = mies(p.get("miesiac_do")) or min(MAX_MIESIECY, od + (mies(_atr(p).get("miesiace")) or 2) - 1)
        if p.get("kategoria") == "personel" and not mies(p.get("miesiac_od")):
            od, do = 1, max(1, mies(_atr(p).get("miesiace")) or 12)
        wyn.append({"id": p.get("id"), "nazwa": p.get("nazwa"), "od": max(1, od), "do": max(od, do)})
    return wyn


def wybor_wykonawcy(p, typ_wnioskodawcy, reguly, netto=None):
    """Jak wybrać wykonawcę dla pozycji po przyznaniu dotacji (netto – wartość do progu: łączna wartość tożsamych zamówień, H3-05)."""
    netto = _f(p.get("ilosc") or 1) * _f(p.get("cena_netto")) if netto is None else netto
    if p.get("kategoria") == "szkolenia" and (reguly or {}).get("bur"):
        return "Baza Usług Rozwojowych", "usługę wybierasz w Bazie Usług Rozwojowych (karta usługi)"
    if p.get("kategoria") == "personel":
        return "zatrudnienie", "umowa o pracę / zlecenie – zasada konkurencyjności nie dotyczy wynagrodzeń personelu"
    pzp = typ_wnioskodawcy in ("jst", "szkola") or (reguly or {}).get("pzp")
    import progi as PR
    if pzp and netto >= PR.prog_pzp():
        return "Pzp", "zamówienie publiczne – moduł Zamawiającego (SWZ, BZP)"
    if PR.wymaga_zk(netto):
        return "zasada konkurencyjności", "zapytanie ofertowe w Bazie Konkurencyjności"
    return "rozeznanie rynku", "do 80 000 zł netto – zachowaj dokumentację wyboru (np. 2–3 oferty), jeśli wymaga jej umowa"


def cpv_pozycji(p):
    """Kod CPV pozycji (pole „cpv” albo atrybut „cpv”) – 8 cyfr, z cyfrą kontrolną albo bez; inaczej pusty."""
    m = re.search(r"\b(\d{8})(?:-\d)?\b", str((p or {}).get("cpv") or _atr(p).get("cpv") or ""))
    return m.group(1) if m else ""


def grupa_zamowienia(p):
    """Klucz tożsamości zamówienia: dział i grupa CPV (3 pierwsze cyfry), gdy podano kod; inaczej kategoria kosztu."""
    c = cpv_pozycji(p)
    return (f"CPV {c[:3]}", f"CPV {c[:3]}…") if c else (f"kat {p.get('kategoria')}", f"kategoria „{KATALOG.get(p.get('kategoria'), {}).get('nazwa', p.get('kategoria'))}”")


def wybor_wykonawcow(pozycje, typ_wnioskodawcy, reguly):
    """H3-05: tryb wyboru wykonawcy po zsumowaniu tożsamych zamówień (dotąd – osobno dla każdej pozycji, co pozwalało „zejść” poniżej progu
    przez podział). Grupy: ta sama grupa CPV albo – bez kodu – ta sama kategoria kosztu. Progi: zasada konkurencyjności – wartość
    przekraczająca 80 000 zł netto (Wytyczne kwalifikowalności 2021–2027, sekcja 3.2); Pzp – od 170 000 zł netto dla zamawiającego publicznego
    (art. 2 ust. 1 pkt 1 Pzp). Zwraca ({id: {tryb, opis, grupa, grupa_netto, grupa_pozycji}}, [ostrzeżenia])."""
    import progi as PR
    netto = lambda x: _f(x.get("ilosc") or 1) * _f(x.get("cena_netto"))
    wyl = lambda x: x.get("kategoria") == "personel" or (x.get("kategoria") == "szkolenia" and (reguly or {}).get("bur"))
    grupy = {}
    for x in pozycje:
        if isinstance(x, dict) and not wyl(x):
            grupy.setdefault(grupa_zamowienia(x)[0], []).append(x)
    wyn, ostrz = {}, []
    for x in pozycje:
        if not isinstance(x, dict):
            continue
        if wyl(x):
            t, o = wybor_wykonawcy(x, typ_wnioskodawcy, reguly)
            wyn[x.get("id")] = {"tryb": t, "opis": o, "grupa": "", "grupa_netto": round(netto(x), 2), "grupa_pozycji": 1}
            continue
        k, nazwa = grupa_zamowienia(x)
        g = grupy[k]
        suma = round(sum(netto(y) for y in g), 2)
        t, o = wybor_wykonawcy(x, typ_wnioskodawcy, reguly, suma)
        if len(g) > 1:
            o += PR.pl_liczby(f" – według łącznej wartości {len(g)} pozycji ({nazwa}): {suma:,.2f} zł netto")
        wyn[x.get("id")] = {"tryb": t, "opis": o, "grupa": nazwa, "grupa_netto": suma, "grupa_pozycji": len(g)}
    for k, g in grupy.items():
        if len(g) < 2:
            continue
        suma = round(sum(netto(y) for y in g), 2)
        laczny = wybor_wykonawcy(g[0], typ_wnioskodawcy, reguly, suma)[0]
        osobno = {wybor_wykonawcy(y, typ_wnioskodawcy, reguly)[0] for y in g}
        if osobno != {laczny}:
            ostrz.append(PR.pl_liczby(
                f"Pozycje {', '.join('„' + str(y.get('nazwa') or '') + '”' for y in g[:6])}{' i inne' if len(g) > 6 else ''} ({grupa_zamowienia(g[0])[1]}) "
                f"mają łącznie {suma:,.2f} zł netto – jeśli to zamówienia tożsame (ten sam rodzaj, czas, możliwy jeden wykonawca), wybierz wykonawcę "
                f"w trybie: {laczny}. Nie dziel zamówienia, by uniknąć zasady konkurencyjności (powyżej 80 000 zł netto) albo Pzp (od 170 000 zł netto "
                "u zamawiającego publicznego) – art. 29–30 Pzp, Wytyczne kwalifikowalności 2021–2027, sekcja 3.2. Jeśli zamówienia nie są tożsame, "
                "wpisz przy pozycjach różne kody CPV."))
    return wyn, ostrz


MSP = ("mikro", "mała", "średnia")


def trwalosc(data_konca, lata, typ_wnioskodawcy, wielkosc=None):
    """Okres trwałości i daty przypomnień (sprawozdania roczne). Domyślnie (gdy nabór nie podaje): 5 lat, 3 lata tylko dla MŚP
    (art. 65 ust. 1 rozporządzenia 2021/1060) – duże przedsiębiorstwo i firma bez podanej wielkości: 5 lat (GC-05)."""
    try:
        k = dt.date.fromisoformat(str(data_konca)[:10])
    except ValueError:
        return {}
    n = max(0, min(20, int(_f(lata)))) or (3 if typ_wnioskodawcy == "firma" and wielkosc in MSP else 5)

    def plus_lat(i):  # 29.02 + i lat → 28.02 (bez błędu w latach nieprzestępnych)
        try:
            return k.replace(year=k.year + i)
        except ValueError:
            return k.replace(year=k.year + i, day=28)
    do = plus_lat(n)
    # art. 65 rozporządzenia 2021/1060: trwałość liczona od płatności końcowej na rzecz beneficjenta (3 lata – MŚP, gdy tak stanowi program)
    return {"lata": n, "od": k.isoformat(), "do": do.isoformat(), "uwaga": "Okres trwałości liczy się od dnia płatności końcowej na rzecz "
            "beneficjenta (art. 65 rozporządzenia 2021/1060) – jeśli płatność końcowa wpłynie później niż koniec projektu, wpisz jej datę.",
            "przypomnienia": [plus_lat(i).isoformat() for i in range(1, n + 1)],
            "zakazy": ["nie sprzedawaj, nie wynajmuj i nie przenoś dofinansowanych środków trwałych bez zgody instytucji",
                       "utrzymaj cel projektu i osiągnięte wskaźniki", "przechowuj dokumentację projektu i oznaczenia (logotypy)",
                       "nie zmieniaj istotnie charakteru działalności i lokalizacji inwestycji"]}


# ---------------------------------------------------------------- polecenia AI
import progi as _PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)
SYSTEM_PLAN = (_PR.INFO_AI + " " + "Jesteś doradcą ds. dotacji UE i krajowych w Polsce (KPO, FENG, FERS, FEnIKS, programy regionalne, PS WPR / ARiMR, NFOŚiGW, "
               "KFS, programy ministerialne). Czytasz regulamin naboru i przekładasz go na konkretny projekt wnioskodawcy. Nie zmyślasz – gdy "
               "regulamin czegoś nie mówi, zostawiasz pole puste. Odpowiadasz WYŁĄCZNIE JSON-em.")


def polecenie_analizy(nabor, wnioskodawca, pomysl):
    kat = "; ".join(f"{k} = {v['nazwa']} ({v['opis']})" for k, v in KATALOG.items())
    return (f"Nabór: {json.dumps(nabor, ensure_ascii=False)[:1500]}\nWnioskodawca: {json.dumps(wnioskodawca, ensure_ascii=False)}\n"
            f"Pomysł wnioskodawcy (co chce zrobić): {pomysl or 'brak – zaproponuj typowe działania'}\n\n"
            f"Na podstawie dokumentów naboru powyżej ustal, CO MOŻNA SFINANSOWAĆ i na jakich zasadach. Kategorie kosztów programu: {kat}.\n"
            'Zwróć JSON: {"dzialania": [{"id": "d1", "nazwa": "działanie / obszar z regulaminu, np. Obszar B – mikroinstalacje OZE", '
            '"kategorie": ["id kategorii z listy"], "limit_zl": liczba lub null, "intensywnosc_procent": liczba lub null, "opis": "co obejmuje, warunki", '
            '"wymagania": ["np. moc PV do 50 kW, magazyn obowiązkowy"], "podstawa": "punkt regulaminu"}], '
            '"kategorie": [{"id": "id kategorii", "kwalifikowalna": true/false, "limit_zl": liczba lub null, "intensywnosc_procent": liczba lub null, '
            '"uwagi": "warunki / wyłączenia, np. ciągniki niekwalifikowalne", "podstawa": "punkt regulaminu"}], '
            '"intensywnosc_procent": liczba (domyślna), "limit_projektu_zl": liczba lub null, "min_koszty_zl": liczba lub null, "max_koszty_zl": liczba lub null, '
            '"vat_kwalifikowalny": true/false, "pomoc": "de minimis | pomoc publiczna | brak | nie wiadomo", "bur": true/false (czy usługi szkoleniowe przez BUR), '
            '"trwalosc_lat": liczba lub null, "wskazniki_obowiazkowe": [{"nazwa": "…", "jednostka": "…"}], '
            '"kryteria_punktowe": [{"nazwa": "…", "punkty_max": liczba lub null, "jak_spelnic": "…"}], '
            '"typy_wnioskodawcow": ["…"], "wylaczenia": ["czego nie finansuje nabór"], '
            '"proponowane_pozycje": [{"nazwa": "…", "kategoria": "id", "dzialanie": "d1", "atrybuty": {"klucz": "wartość"}, "ilosc": 1}] '
            '(tylko gdy pomysł wnioskodawcy jest podany – pozycje zgodne z pomysłem i regulaminem)}')


def polecenie_wyceny(pozycje, region):
    linie = "\n".join(f"{p['id']} | {KATALOG.get(p.get('kategoria'), {}).get('nazwa', '')} | {p.get('nazwa')} | {json.dumps(p.get('atrybuty') or {}, ensure_ascii=False)} "
                      f"| ilość {p.get('ilosc') or 1}" for p in pozycje)
    d = dt.date.today()
    return (f"Dziś jest {d:%d.%m.%Y}. Region: {region or 'Polska'}. Sprawdź w internecie AKTUALNE ceny netto (zł) dla pozycji projektu dotacyjnego. "
            "Instalacje OZE, maszyny, sprzęt i IT – ceny ofertowe sprzedawców i instalatorów; szkolenia – ceny podobnych usług w Bazie Usług Rozwojowych "
            "(za osobę lub całość, podaj sposób); roboty budowlane – typowy koszt za m² lub komplet w regionie; personel – mediana wynagrodzeń na stanowisku.\n"
            f"Pozycje (id | kategoria | nazwa | parametry | ilość):\n{linie}\n"
            'Zwróć WYŁĄCZNIE JSON: {"ceny": [{"id": "…", "cena_netto_jednostkowa": liczba, "jednostka": "szt. / komplet / os. / m² / mies.", '
            '"zrodlo": "skąd (nazwa sklepu / portal / BUR)", "uwagi": "założenia"}]}. Pomiń pozycje, dla których nie znajdziesz wiarygodnych cen.')


def polecenie_kontroli(nabor, plan, budzet_, wskazniki_, wnioskodawca):
    return (f"Nabór: {json.dumps(nabor, ensure_ascii=False)[:1200]}\nWnioskodawca: {json.dumps(wnioskodawca, ensure_ascii=False)}\n"
            f"Projekt – pozycje: {json.dumps(plan.get('pozycje'), ensure_ascii=False)[:6000]}\nBudżet: {json.dumps(budzet_.get('suma'), ensure_ascii=False)}\n"
            f"Wskaźniki: {json.dumps(wskazniki_, ensure_ascii=False)}\nKryteria punktowe z analizy: {json.dumps((plan.get('reguly') or {}).get('kryteria_punktowe'), ensure_ascii=False)}\n\n"
            "Na podstawie dokumentów naboru powyżej: (1) sprawdź zgodność projektu z regulaminem (kwalifikowalność, limity, wymagania techniczne, "
            "typ wnioskodawcy, wymagane załączniki); (2) oszacuj punkty w kryteriach oceny i podpowiedz konkretne zmiany, które dadzą więcej punktów. "
            'Zwróć JSON: {"ocena": "zgodny | wymaga zmian | niezgodny", "podsumowanie": "2–4 zdania", "punkty_szacowane": liczba lub null, "punkty_max": liczba lub null, '
            '"wiecej_punktow": [{"zmiana": "co zmienić / dodać", "zysk_pkt": liczba lub null, "kryterium": "…", "koszt_zmiany": "orientacyjnie"}], '
            '"uwagi": [{"waga": "krytyczna | istotna | drobna", "opis": "…", "propozycja": "…", "dokument": "plik", "miejsce": "pkt regulaminu", '
            '"cytat": "DOSŁOWNY fragment regulaminu 20–300 znaków albo pusty"}]}')


def polecenie_pomyslu(pomysl, wnioskodawca, region):
    """Wyszukiwanie odwrotne: od pomysłu do naborów (dodatek do zwykłego wyszukiwania naborów)."""
    return (f"Wnioskodawca: {json.dumps(wnioskodawca, ensure_ascii=False)}. Region: {region or 'cała Polska'}.\n"
            f"Co chce zrobić: {pomysl}\n")


def opis_planu(plan, wskazniki_, budzet_, harm):
    """Tekst planu projektu do przygotowania wniosku (opis, zestawienie rzeczowo-finansowe, wskaźniki, harmonogram)."""
    poz = plan.get("pozycje") or []
    lin = [f"- {p.get('nazwa')} [{KATALOG.get(p.get('kategoria'), {}).get('nazwa', '')}] {json.dumps(p.get('atrybuty') or {}, ensure_ascii=False)}, "
           f"ilość {p.get('ilosc') or 1}, cena netto {p.get('cena_netto') or '?'} zł" for p in poz]
    s = budzet_.get("suma") or {}
    return ("ZAKRES PROJEKTU (z planu w programie):\n" + "\n".join(lin) +
            f"\nBUDŻET: netto {s.get('netto')} zł, brutto {s.get('brutto')} zł, koszty kwalifikowalne {s.get('kwal')} zł, dotacja {s.get('dotacja')} zł, "
            f"wkład własny {s.get('wklad_wlasny')} zł.\nWSKAŹNIKI: " + "; ".join(f"{w['nazwa']}: {w['wartosc']} {w['jednostka']}" for w in wskazniki_) +
            "\nHARMONOGRAM (miesiące realizacji): " + "; ".join(f"{h['nazwa']}: m. {h['od']}–{h['do']}" for h in harm))


def budzet_xlsx(sciezka, plan, budzet_, wskazniki_, harm, nazwa):
    """Zestawienie rzeczowo-finansowe do wniosku (Excel)."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zestawienie"
    NAG = PatternFill("solid", fgColor="071F49")
    ws.append([f"Zestawienie rzeczowo-finansowe – {nazwa}"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append([])
    ws.append(["Lp.", "Pozycja", "Kategoria", "Ilość", "Cena netto [zł]", "Wartość netto [zł]", "VAT [zł]", "Koszty kwalifikowalne [zł]", "Intensywność [%]", "Dotacja [zł]"])
    for c in ws[3]:
        c.font, c.fill = Font(bold=True, color="FFFFFF"), NAG
    poz = {p.get("id"): p for p in plan.get("pozycje") or []}
    for i, w in enumerate(budzet_["wiersze"], 1):
        p = poz.get(w["id"]) or {}
        ws.append([i, w["nazwa"], KATALOG.get(w["kategoria"], {}).get("nazwa", ""), _f(p.get("ilosc") or 1), _f(p.get("cena_netto")), w["netto"], w["vat"],
                   w["kwalifikowalne"], w["intensywnosc"], w["dotacja"]])
    s = budzet_["suma"]
    ws.append(["", "RAZEM", "", "", "", s["netto"], s["vat"], s["kwal"], "", s["dotacja"]])
    ws.append(["", "Wkład własny (brutto – dotacja)", "", "", "", "", "", "", "", s["wklad_wlasny"]])
    for col, szer in zip("ABCDEFGHIJ", (5, 46, 26, 8, 14, 16, 12, 18, 12, 14)):
        ws.column_dimensions[col].width = szer
    w2 = wb.create_sheet("Wskaźniki")
    w2.append(["Wskaźnik", "Wartość", "Jednostka", "Uwagi"])
    for w in wskazniki_:
        w2.append([w["nazwa"], w["wartosc"], w["jednostka"], w.get("uwaga", "")])
    w3 = wb.create_sheet("Harmonogram")
    w3.append(["Zadanie", "Od miesiąca", "Do miesiąca"])
    for h in harm:
        w3.append([h["nazwa"], h["od"], h["do"]])
    for x in (w2, w3):
        x.column_dimensions["A"].width = 50
    wb.save(sciezka)


# ---------------------------------------------------------------- wyjaśnienia pojęć (przycisk „?” przy polach i słowniczek)
POMOC = {
    "wielkosc_ekonomiczna": ("Wielkość ekonomiczna gospodarstwa (SO)",
        "SO, czyli standardowa produkcja, to szacunkowa roczna wartość produkcji gospodarstwa w euro – liczona z powierzchni upraw i liczby "
        "zwierząt według stałych współczynników dla regionu, a nie z faktycznej sprzedaży. Wiele naborów ARiMR wymaga minimalnej (a czasem "
        "nie większej niż określona) wielkości ekonomicznej.",
        "Jak obliczyć: kliknij „Oblicz SO” pod polem – wpisz uprawy (ha) i zwierzęta (sztuki), a program policzy wynik ze współczynników dla Twojego "
        "regionu. Oficjalny arkusz i kalkulator są też na stronie ARiMR (Kalkulator obliczania wielkości ekonomicznej gospodarstw – SO)."),
    "nr_ep": ("Numer identyfikacyjny ARiMR (EP)",
        "Numer nadany przez ARiMR w ewidencji producentów rolnych. Bez niego nie złożysz wniosku do ARiMR.",
        "Jak sprawdzić: jest na decyzjach o płatnościach bezpośrednich i w aplikacji eWniosekPlus; nadaje go biuro powiatowe ARiMR."),
    "ha": ("Powierzchnia użytków rolnych",
        "Łączna powierzchnia gruntów ornych, sadów, łąk i pastwisk w gospodarstwie (własnych i dzierżawionych).",
        "Jak sprawdzić: z ostatniego wniosku o płatności bezpośrednie albo z ewidencji gruntów."),
    "produkcja": ("Główna produkcja", "Czym zajmuje się gospodarstwo – np. zboża, mleko, trzoda, drób, sady, warzywa. Część naborów jest tylko dla wybranej produkcji.", ""),
    "wielkosc": ("Wielkość przedsiębiorstwa",
        "Mikro: mniej niż 10 osób i obrót lub suma bilansowa do 2 mln euro. Mała: mniej niż 50 osób i do 10 mln euro. Średnia: mniej niż 250 osób "
        "i obrót do 50 mln euro lub suma bilansowa do 43 mln euro. Powyżej – duża. Liczą się też firmy powiązane i partnerskie.",
        "Jak sprawdzić: ze sprawozdania finansowego i liczby pracowników; w razie powiązań z innymi firmami sumuje się ich dane."),
    "pkd": ("PKD", "Kod rodzaju działalności firmy. Niektóre nabory wykluczają określone branże (np. rolnictwo, transport).",
            "Jak sprawdzić: w CEIDG albo w KRS – kod przeważającej działalności."),
    "zatrudnienie": ("Zatrudnienie (etaty)", "Średnia liczba etatów w ostatnim roku (osoby na część etatu liczy się proporcjonalnie).", ""),
    "de_minimis": ("Pomoc de minimis",
        "Pomoc publiczna o niewielkiej wartości (np. dotacje, ulgi, preferencyjne pożyczki), która nie wymaga zgody Komisji Europejskiej. "
        "Ma limit na 3 lata – ogólny limit to 300 000 euro, a w rolnictwie i rybołówstwie obowiązują niższe limity. Jeśli nabór jest pomocą "
        "de minimis, musisz wykazać, ile takiej pomocy już otrzymałeś.",
        "Jak sprawdzić: w systemie SUDOP (UOKiK) – wyszukaj swoją firmę po NIP; zachowaj też zaświadczenia o pomocy de minimis."),
    "mieszkancy": ("Liczba mieszkańców", "Liczba mieszkańców gminy / powiatu – część naborów jest tylko dla mniejszych gmin.", "Jak sprawdzić: GUS (Bank Danych Lokalnych) albo ewidencja ludności."),
    "pzp": ("Stosuje ustawę Pzp", "Gminy, szkoły, szpitale i inne jednostki publiczne muszą kupować według ustawy Prawo zamówień publicznych – zmienia to sposób wyboru wykonawców w projekcie.", ""),
    "krs": ("KRS", "Numer w Krajowym Rejestrze Sądowym – stowarzyszenia i fundacje go mają. Na jego podstawie instytucja sprawdza statut i reprezentację.", ""),
    "projekty": ("Zrealizowane projekty", "Ile projektów (dotacji) organizacja już przeprowadziła – w części naborów doświadczenie daje punkty.", ""),
    "lokale": ("Liczba lokali", "Wszystkie lokale w budynku (mieszkalne i użytkowe) – potrzebne do wskaźników i części programów dla wspólnot.", ""),
    "powierzchnia": ("Powierzchnia użytkowa", "Suma powierzchni lokali / pomieszczeń w budynku, bez ścian i klatek schodowych.", "Jak sprawdzić: z dokumentacji budynku, świadectwa charakterystyki energetycznej albo księgi wieczystej."),
    "rok_budowy": ("Rok budowy", "Rok oddania budynku do użytku – część programów dotyczy tylko starszych budynków.", ""),
    "dochod": ("Przeciętny dochód na osobę",
        "Miesięczny dochód na jedną osobę w gospodarstwie domowym. W programach dla osób fizycznych (np. Czyste Powietrze) decyduje o poziomie dofinansowania.",
        "Jak sprawdzić: z zeznania PIT za ostatni rok albo zaświadczenia z gminy (ośrodka pomocy społecznej)."),
    "budynek": ("Rodzaj budynku", "Np. dom jednorodzinny, lokal w budynku wielorodzinnym – programy dla osób fizycznych różnią się zakresem dla tych rodzajów.", ""),
    "moc": ("Moc (kW / kWp)",
        "kWp to moc szczytowa paneli fotowoltaicznych; kW – moc urządzenia (np. pompy ciepła). Nabory często mają limit mocy, np. „do 50 kW”.",
        "Jak dobrać: przy fotowoltaice orientacyjnie 1 kWp na 1000 kWh rocznego zużycia prądu; ostateczną moc poda instalator."),
    "magazyn": ("Magazyn energii (kWh)", "Akumulator przechowujący prąd z fotowoltaiki – pojemność w kWh. W części naborów jest wymagany albo daje punkty.", ""),
    "zuzycie": ("Roczne zużycie energii", "Ile energii zużywasz w roku (kWh).", "Jak sprawdzić: z rachunków za prąd lub ciepło z ostatnich 12 miesięcy."),
    "montaz": ("Montaż", "Gdzie zostanie zamontowana instalacja – na dachu, na gruncie czy w budynku. Wpływa na koszt i formalności.", ""),
    "audyt": ("Audyt energetyczny",
        "Opracowanie fachowca, które pokazuje, co i jak ocieplić lub wymienić oraz jaką oszczędność energii to da. W wielu naborach na "
        "termomodernizację jest obowiązkowy, a oszczędność z audytu to wskaźnik projektu.",
        "Kto wykonuje: audytor energetyczny – koszt audytu często jest kosztem kwalifikowalnym."),
    "obiekt": ("Obiekt", "Jakiego budynku lub obiektu dotyczą roboty – od tego zależą wymagania i ceny.", ""),
    "zakres": ("Zakres robót", "Co dokładnie zostanie zrobione – zaznacz wszystkie elementy; na tej podstawie program wycenia roboty i liczy wskaźniki.", ""),
    "parametry": ("Parametry maszyny", "Najważniejsze dane techniczne, np. moc silnika (KM), szerokość robocza (m), pojemność zbiornika (l) – potrzebne do wyceny i porównania ofert.", ""),
    "nowe": ("Nowe czy używane", "Większość naborów finansuje tylko nowe maszyny i urządzenia – sprawdź w regulaminie.", ""),
    "stanowiska": ("Stanowiska / użytkownicy", "Ile osób lub stanowisk będzie korzystać ze sprzętu albo systemu – podstawa wyceny licencji i wskaźników.", ""),
    "moduly": ("Moduły / funkcje", "Np. w systemie ERP: księgowość, magazyn, sprzedaż, produkcja; w sklepie internetowym: płatności, integracja z kurierem.", ""),
    "osoby": ("Liczba uczestników", "Ile osób weźmie udział w szkoleniu – wskaźnik „osoby przeszkolone”.", ""),
    "godziny": ("Godziny na osobę", "Długość szkolenia w godzinach dla jednego uczestnika.", ""),
    "certyfikat": ("Certyfikat / egzamin",
        "Szkolenie kończące się egzaminem i dokumentem potwierdzającym kwalifikacje (np. certyfikat, uprawnienia). Często daje punkty i jest osobnym wskaźnikiem.", ""),
    "etat": ("Wymiar etatu", "1 = pełny etat, 0,5 = pół etatu.", ""),
    "stawka": ("Wynagrodzenie z kosztami pracodawcy",
        "Pełny koszt pracownika: wynagrodzenie brutto plus składki pracodawcy (ok. 20% ponad brutto).", "Jak sprawdzić: z listy płac albo od księgowej."),
    "grupa": ("Grupa docelowa", "Do kogo kierujesz projekt – np. seniorzy, osoby bezrobotne, uczniowie. Musi być zgodna z regulaminem naboru.", ""),
    "uczestnicy": ("Liczba uczestników", "Ile osób skorzysta z działań projektu – podstawowy wskaźnik w projektach społecznych.", ""),
    # pola kroku „Wymagania naboru i dane projektu”
    "opis_projektu": ("Opis projektu",
        "Krótko i konkretnie: co zrobisz (zakres), gdzie (miejsce realizacji), po co (problem lub potrzeba, którą rozwiązujesz) i jakie będą efekty "
        "(np. moc instalacji, oszczędność energii, liczba przeszkolonych osób). Na tej podstawie program przygotuje treść wniosku.",
        "Podpowiedź: najpierw uzupełnij krok 3 „Zakres projektu” – program sam ułoży z niego opis."),
    "koszt_calkowity": ("Koszt całkowity",
        "Suma wszystkich wydatków projektu brutto – kwalifikowalnych i niekwalifikowalnych (razem z VAT).", "Program wylicza go z budżetu w kroku 3."),
    "kwota_wnioskowana": ("Wnioskowana kwota",
        "Ile dotacji chcesz dostać: koszty kwalifikowalne × intensywność dofinansowania, ale nie więcej niż limit naboru.", "Program wylicza ją z budżetu w kroku 3."),
    "okres_realizacji": ("Okres realizacji",
        "Od kiedy do kiedy będziesz realizować projekt – od pierwszego wydatku do ostatniego odbioru. Uwaga: w wielu naborach nie wolno zacząć "
        "inwestycji (np. podpisać umowy z wykonawcą) przed złożeniem wniosku.", "Program podpowiada długość z harmonogramu w kroku 3."),
    "lokalizacja": ("Lokalizacja (miejsce realizacji)",
        "Adres lub działka, gdzie będzie realizowany projekt (np. gdzie stanie instalacja, który budynek będzie ocieplony). Część naborów jest tylko dla wybranych gmin lub województw.", ""),
    # pojęcia budżetu i zasad naboru
    "intensywnosc_procent": ("Intensywność dofinansowania",
        "Jaki procent kosztów kwalifikowalnych pokrywa dotacja – np. 65% oznacza, że z 100 000 zł kosztów dostaniesz 65 000 zł, a 35 000 zł to Twój wkład.", ""),
    "kwalifikowalne": ("Koszty kwalifikowalne",
        "Wydatki, które regulamin naboru pozwala sfinansować z dotacji. Pozostałe (niekwalifikowalne) płacisz w całości sam.", ""),
    "wklad_wlasny": ("Wkład własny", "Część kosztów, którą pokrywasz sam: koszty niekwalifikowalne, VAT (jeśli możesz go odzyskać) i różnica ponad dotację.", ""),
    "limit_projektu_zl": ("Limit dotacji na projekt", "Najwyższa kwota dotacji, jaką można dostać w tym naborze na jeden projekt (albo na wnioskodawcę).", ""),
    "min_koszty_zl": ("Minimalne koszty kwalifikowalne", "Projekt musi mieć co najmniej tyle kosztów kwalifikowalnych – mniejsze projekty są odrzucane.", ""),
    "max_koszty_zl": ("Maksymalne koszty kwalifikowalne", "Górna granica kosztów kwalifikowalnych projektu w tym naborze.", ""),
    "trwalosc_lat": ("Okres trwałości",
        "Ile lat po zakończeniu projektu musisz utrzymać jego efekty (nie sprzedawać sprzętu, nie zmieniać przeznaczenia). Zwykle 3 lata dla MŚP, 5 lat dla pozostałych.", ""),
    "vat_kwalifikowalny": ("VAT kwalifikowalny",
        "VAT jest kosztem kwalifikowalnym tylko wtedy, gdy nie możesz go odzyskać (np. nie jesteś czynnym podatnikiem VAT). Firmy rozliczające VAT zwykle płacą go same.", ""),
}


# ---------------------------------------------------------------- kalkulator wielkości ekonomicznej gospodarstwa (SO)
# Regiony FADN (współczynniki SO są ustalane dla regionów, nie województw)
REGIONY_FADN = {
    "Pomorze i Mazury": ["zachodniopomorskie", "pomorskie", "kujawsko-pomorskie", "warmińsko-mazurskie"],
    "Wielkopolska i Śląsk": ["wielkopolskie", "lubuskie", "dolnośląskie", "opolskie"],
    "Mazowsze i Podlasie": ["mazowieckie", "łódzkie", "lubelskie", "podlaskie"],
    "Małopolska i Pogórze": ["śląskie", "małopolskie", "świętokrzyskie", "podkarpackie"],
}
SO_UPRAWY = ["pszenica zwyczajna i orkisz", "żyto", "jęczmień", "owies", "pszenżyto", "mieszanki zbożowe", "kukurydza na ziarno",
             "rzepak i rzepik", "buraki cukrowe", "ziemniaki", "strączkowe na ziarno (groch, bobik, łubin)", "kukurydza na zielonkę / kiszonkę",
             "rośliny pastewne (koniczyna, lucerna, trawy na gruntach ornych)", "łąki i pastwiska trwałe", "warzywa gruntowe",
             "warzywa pod osłonami", "truskawki", "sady – jabłonie i inne owoce ziarnkowe", "krzewy owocowe (porzeczki, maliny, borówka)",
             "tytoń", "chmiel", "ugory z dopłatami"]
SO_ZWIERZETA = ["krowy mleczne", "pozostałe krowy", "cielęta do 1 roku", "bydło 1–2 lata", "bydło 2 lata i więcej (bez krów)",
                "owce", "kozy", "konie", "prosięta do 20 kg", "warchlaki i tuczniki (od 20 kg)", "lochy (maciory) 50 kg i więcej",
                "kury nioski", "brojlery (kurczęta rzeźne)", "indyki", "kaczki", "gęsi", "matki pszczele (rodziny pszczele)"]


def region_fadn(woj):
    return next((r for r, L in REGIONY_FADN.items() if woj in L), "")


def polecenie_so(region, wersja):
    return (f"Znajdź w internecie OFICJALNE współczynniki Standardowej Produkcji (SO) w wersji „{wersja}” dla regionu FADN „{region}” w Polsce "
            "(źródło: Instytut Ekonomiki Rolnictwa i Gospodarki Żywnościowej – FADN, ARiMR, Ministerstwo Rolnictwa). Podaj wartości w EUR: "
            "dla upraw na 1 ha, dla zwierząt na 1 sztukę średniorocznie (jeśli tabela podaje drób na 100 sztuk – podziel przez 100).\n"
            f"Uprawy: {'; '.join(SO_UPRAWY)}\nZwierzęta: {'; '.join(SO_ZWIERZETA)}\n"
            'Zwróć WYŁĄCZNIE JSON: {"wersja": "…", "region": "…", "zrodlo": "nazwa dokumentu", "zrodlo_url": "https://…", '
            '"uprawy": {"nazwa z listy": liczba EUR/ha}, "zwierzeta": {"nazwa z listy": liczba EUR/szt.}}. '
            "Pomiń pozycje, dla których nie znalazłeś wartości w oficjalnej tabeli – nie szacuj.")


def oblicz_so(uprawy, zwierzeta, wsp):
    """SO = Σ (ha × współczynnik) + Σ (sztuki × współczynnik); zwraca sumę i szczegóły."""
    wu, wz = (wsp or {}).get("uprawy") or {}, (wsp or {}).get("zwierzeta") or {}
    szcz, suma, braki = [], 0.0, []
    for nazwa, ilosc, wl in [(u.get("nazwa"), u.get("ha"), u.get("wsp")) for u in uprawy] + [(z.get("nazwa"), z.get("sztuk"), z.get("wsp")) for z in zwierzeta]:
        il = _f(ilosc)
        if not nazwa or not il:
            continue
        k = _f(wl) or _f(wu.get(nazwa) or wz.get(nazwa))
        if not k:
            braki.append(nazwa)
        szcz.append({"nazwa": nazwa, "ilosc": il, "wsp": k, "so": round(il * k, 2)})
        suma += il * k
    return {"so": round(suma, 2), "szczegoly": szcz, "braki": braki}
