# -*- coding: utf-8 -*-
"""Kreator zamówienia dla zamawiającego: co zamawiasz → wzory czy od początku → opis potrzeby → wartość → warunki → komplet
dokumentów → sprawdzenie i zmiany (akceptacja, Word ze śledzeniem zmian i czysty) → gotowe do publikacji."""
import copy
import datetime as dt
import json
import os
import re

import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

RODZAJE = {"roboty": "Roboty budowlane", "uslugi": "Usługi", "dostawy": "Dostawy"}

# ---------------------------------------------------------------- opis potrzeby – pytania zależne od rodzaju
PYTANIA = {
    "roboty": [("obiekt", "Jaki obiekt / miejsce robót?", "tekst", "np. budynek szkoły podstawowej, ul. Szkolna 1, Pszenno"),
               ("zakres", "Co ma zostać wykonane?", "dlugi", "np. termomodernizacja: ocieplenie ścian i stropodachu, wymiana okien, nowa kotłownia"),
               ("projekt", "Czy jest dokumentacja projektowa?", "wybor", ["tak – projekt budowlany/wykonawczy", "tylko program funkcjonalno-użytkowy", "nie ma – opis potrzeb"]),
               ("przedmiar", "Czy jest przedmiar robót?", "wybor", ["tak", "nie – trzeba przygotować"]),
               ("pozwolenie", "Pozwolenie na budowę / zgłoszenie", "wybor", ["jest", "w przygotowaniu", "nie wymaga"]),
               ("termin", "Do kiedy roboty mają być wykonane?", "tekst", "np. do 30.09.2027 albo 6 miesięcy od podpisania umowy")],
    "dostawy": [("przedmiot", "Co chcesz kupić i w jakich ilościach?", "dlugi", "np. 60 ławek szkolnych, 120 krzeseł, 2 tablice interaktywne"),
                ("parametry", "Najważniejsze wymagania (parametry, normy, certyfikaty)", "dlugi", "np. ławki regulowane rozmiar 4–6, atest PN-EN 1729"),
                ("miejsce", "Gdzie i jak dostarczyć?", "tekst", "np. Szkoła w Pszennie, z wniesieniem i montażem"),
                ("gwarancja", "Minimalna gwarancja / serwis", "tekst", "np. 24 miesiące, naprawa w 7 dni"),
                ("opcja", "Czy przewidujesz prawo opcji (dokupienie)?", "wybor", ["nie", "tak – do 20% ilości", "tak – inny zakres"]),
                ("termin", "Termin dostawy", "tekst", "np. do 20.08.2027")],
    "uslugi": [("przedmiot", "Jaką usługę zamawiasz?", "dlugi", "np. sprzątanie budynków urzędu, odbiór odpadów, ochrona"),
               ("ilosci", "Zakres ilościowy w całym okresie umowy (świadczenia i liczba jednostek)", "dlugi",
                "np. przerwy kawowe – 2622 porcje; obiady dwudaniowe – 606 porcji; albo: sprzątanie 2 400 m² × 12 miesięcy"),
               ("miejsce", "Gdzie (obiekty, powierzchnie)?", "dlugi", "np. 3 budynki, łącznie 2 400 m²"),
               ("czestotliwosc", "Jak często / w jakim zakresie?", "tekst", "np. codziennie w dni robocze 16–20, mycie okien 2× w roku"),
               ("okres", "Na jaki okres?", "tekst", "np. 12 miesięcy od 01.01.2027"),
               ("personel", "Wymagania wobec personelu (umowa o pracę, kwalifikacje)", "tekst", "np. zatrudnienie na umowę o pracę osób sprzątających"),
               ("standard", "Standard i sposób odbioru", "tekst", "np. protokoły miesięczne, kontrole jakości")],
}

# ---------------------------------------------------------------- warunki zamówienia – ustawienia domyślne do zmiany
WYKAZ_DOSW = ("wykaz wykonanych prac z nazwą, NIP i danymi kontaktowymi zamawiających (wystawców referencji) oraz dowody należytego wykonania "
              "(referencje, protokoły odbioru); zamawiający może zwrócić się do wystawców o potwierdzenie")


def warunki_domyslne(rodzaj, tryb, netto, vat=0.23):
    pzp = tryb in ("pzp_podstawowy", "pzp_nieograniczony")
    try:
        vat = float(vat)
        vat = vat / 100 if vat >= 1 else vat
    except (TypeError, ValueError):
        vat = 0.23
    w = {
        "wynagrodzenie": "ryczałtowe" if rodzaj != "uslugi" else "ryczałt miesięczny",
        # kryterium gwarancji z górną granicą punktowania (bez niej oferta z „gwarancją 50 lat” wypacza ranking – częsty zarzut w odwołaniach)
        "kryteria": ("Cena – 60%, okres gwarancji – 40% (punktowany od minimalnych 60 do 84 miesięcy; dłuższy okres oceniany jak 84)" if rodzaj == "roboty" else
                     "Cena – 60%, okres gwarancji – 40% (punktowany od minimalnych 24 do 48 miesięcy; dłuższy okres oceniany jak 48)" if rodzaj == "dostawy" else
                     "Cena – 60%, czas reakcji / jakość – 40%"),
        # 50% wartości zamówienia brutto (VAT 23%) – próg proporcjonalny do przedmiotu (art. 112 Pzp)
        "warunki": {"roboty": f"doświadczenie: co najmniej 1 robota podobna o wartości min. {PR.zl(round(netto * (1 + vat) * 0.5, -3) or 100000)} brutto w ostatnich 5 latach; "
                              "kierownik budowy z uprawnieniami w odpowiedniej specjalności; " + WYKAZ_DOSW,
                    "dostawy": "brak szczegółowych warunków (wystarczy oświadczenie o braku podstaw wykluczenia)",
                    "uslugi": "doświadczenie: co najmniej 1 usługa podobna w ostatnich 3 latach; " + WYKAZ_DOSW}[rodzaj],
        "gwarancja": "min. 60 miesięcy" if rodzaj == "roboty" else "min. 24 miesiące" if rodzaj == "dostawy" else "nie dotyczy",
        "kary": "0,2% wynagrodzenia brutto za każdy dzień zwłoki; łączny limit kar 20% wynagrodzenia brutto",
        "wadium": "nie wymaga się" if not pzp or netto < 1_000_000 else f"{PR.zl(round(netto * 0.01, -2))}",
        "zabezpieczenie": "5% ceny ofertowej brutto" if pzp and rodzaj == "roboty" else "nie wymaga się",
        "platnosci": "przelew w terminie 30 dni od doręczenia faktury; faktury częściowe po odbiorach" if rodzaj == "roboty" else
                     "przelew w terminie 30 dni od doręczenia faktury",
        "waloryzacja": "tak – wymagana przy umowie dłuższej niż 6 miesięcy (art. 439 Pzp)" if pzp else "według uznania",
        "podwykonawstwo": "dopuszczone; wykonawca wskaże części powierzone podwykonawcom",
        "czesci": "bez podziału na części",
        "klauzule": "zatrudnienie na umowę o pracę osób wykonujących czynności (art. 95 Pzp)" if pzp and rodzaj != "dostawy" else
                    ("" if pzp else "podanie nieprawdziwych informacji o doświadczeniu albo przedstawienie nieprawdziwych referencji uprawnia zamawiającego "
                                    "do odrzucenia oferty, a po zawarciu umowy – do odstąpienia od umowy z winy wykonawcy"),
        "platforma": "Platforma e-Zamówienia" if pzp else "e-mail / Baza Konkurencyjności / platforma zamawiającego",
        "kontakt": "",
    }
    if pzp:  # decyzje zamawiającego wpisywane do oświadczeń wykonawcy wprost (bez pola [UZUPEŁNIJ] – karta 08)
        w["wykluczenie"] = "nie stosuje się (zamawiający nie przewiduje fakultatywnych podstaw wykluczenia z art. 109 ust. 1 Pzp)"
    if tryb == "pzp_nieograniczony":
        w["jedz"] = "wyłącznie sekcja α – ogólne oświadczenie o spełnianiu wszystkich warunków udziału"
    return w


POMOC = {
    "wynagrodzenie": "Ryczałtowe – stała kwota za cały zakres (ryzyko ilości po stronie wykonawcy); kosztorysowe – według faktycznych ilości i cen jednostkowych.",
    "kryteria": "Zamawiający publiczni mogą zastosować cenę jako jedyne kryterium albo z wagą powyżej 60% tylko wtedy, gdy w opisie przedmiotu zamówienia określą wymagania jakościowe odnoszące się do co najmniej głównych elementów zamówienia (art. 246 ust. 2 Pzp); najczęściej cena 60% + kryteria jakościowe (gwarancja, termin, doświadczenie personelu).",
    "warunki": "Warunki udziału muszą być proporcjonalne do przedmiotu i wartości – zbyt wysokie ograniczają konkurencję i są częstą przyczyną odwołań.",
    "kary": "Kary liczone od zwłoki (z winy wykonawcy), z łącznym limitem – limit kar jest obowiązkowy w umowach Pzp (art. 436).",
    "wadium": "Wadium zabezpiecza ofertę; w trybie podstawowym nie więcej niż 1,5% wartości zamówienia (art. 281 ust. 4 i art. 299 ust. 3 Pzp), w procedurze unijnej do 3% (art. 97 ust. 2). Przy małych zamówieniach zwykle się z niego rezygnuje.",
    "zabezpieczenie": "Zabezpieczenie należytego wykonania umowy – do 5% ceny; więcej, do 10%, tylko gdy uzasadnia to przedmiot zamówienia albo ryzyko opisane w SWZ (art. 452 ust. 2–3 Pzp); zwrot w 30 dni od wykonania zamówienia, przy czym zamawiający może zostawić do 30% na rękojmię lub gwarancję – ta część wraca najpóźniej 15. dnia po jej upływie (art. 453).",
    "waloryzacja": "W umowach na roboty, dostawy i usługi zawieranych na dłużej niż 6 miesięcy klauzula waloryzacyjna jest obowiązkowa (art. 439 Pzp).",
    "platnosci": "Termin zapłaty faktury – najwyżej 30 dni (przepisy o terminach zapłaty w transakcjach handlowych). Umowa zawarta na dłużej niż 12 miesięcy: płatności częściowe albo zaliczki; ostatnia część najwyżej 50%, zaliczka co najmniej 5% wynagrodzenia (art. 443 Pzp).",
    "czesci": "Zamówienie dzieli się na części, gdy to możliwe; jeśli nie – w dokumentach podaje się powody braku podziału (art. 91 Pzp).",
    "klauzule": "Np. wymóg zatrudnienia na umowę o pracę (art. 95 Pzp – obowiązkowy przy usługach i robotach, gdy czynności polegają na pracy).",
    "platforma": "W zamówieniach Pzp oferty składa się elektronicznie (np. Platforma e-Zamówienia); poniżej progu – według regulaminu zamawiającego.",
    "wykluczenie": "Podstawy wykluczenia z art. 109 ust. 1 Pzp są fakultatywne – stosuje się tylko te, które zamawiający wskaże w ogłoszeniu i SWZ (art. 109 ust. 2). Wpisz punkty, np. „art. 109 ust. 1 pkt 4, 5 i 7”, albo „nie stosuje się”. Wybór trafia wprost do oświadczenia wykonawcy.",
    "jedz": "Procedura unijna: oświadczenie z art. 125 ust. 1 wykonawca składa na formularzu JEDZ. Wskaż, czy w części IV wypełnia tylko sekcję α (ogólne oświadczenie), czy sekcje A–D. Wybór trafia wprost do wzoru oświadczeń.",
}


def tryb_z_wartosci(netto, rodzaj, data_wszczecia=None, prywatny=False, centralny=False, spoleczne=False):
    if prywatny:
        return "prywatny", "Zapytanie ofertowe inwestora prywatnego / wspólnoty", PR.tryb_wedlug_wartosci(netto, rodzaj, data_wszczecia)
    tw = PR.tryb_wedlug_wartosci(netto, rodzaj, data_wszczecia, centralny, spoleczne)
    if netto < tw["prog_pzp"]:
        return "ponizej_130", f"Zapytanie ofertowe – poniżej progu Pzp ({PR.zl(tw['prog_pzp'])} netto)", tw
    if netto < tw["prog_ue_zl"]:
        return "pzp_podstawowy", "Tryb podstawowy (procedura krajowa)", tw
    return "pzp_nieograniczony", "Przetarg nieograniczony (procedura unijna)", tw


def min_termin_ofert(tryb, rodzaj, netto=None):
    if tryb == "pzp_podstawowy":
        return 14 if rodzaj == "roboty" else 7, "tryb podstawowy: co najmniej 14 dni (roboty budowlane) / 7 dni (dostawy, usługi) od zamieszczenia ogłoszenia w BZP (art. 283 Pzp), z uwzględnieniem złożoności zamówienia"
    if tryb == "konkurencyjnosc":  # zasada konkurencyjności (wytyczne dot. kwalifikowalności) – karta 04
        prog_30 = round((PR.PROGI_UE["roboty"] if rodzaj == "roboty" else PR.PROG_SPOLECZNE) * PR.KURS_EURO)
        if netto and netto >= prog_30:
            return 30, "zasada konkurencyjności: " + PR.TERMIN_ZK_30 + " – od publikacji zapytania w Bazie Konkurencyjności"
        return (14 if rodzaj == "roboty" else 7), ("zasada konkurencyjności: co najmniej 14 dni (roboty budowlane) / 7 dni (dostawy, usługi) od publikacji "
                                                   "zapytania w Bazie Konkurencyjności (wytyczne dotyczące kwalifikowalności wydatków)")
    if tryb == "pzp_nieograniczony":
        return 30, ("przetarg nieograniczony (procedura unijna): co najmniej 30 dni od przekazania ogłoszenia Urzędowi Publikacji UE – 35 dni "
                    "(art. 138 ust. 1 Pzp) pomniejszone o 5 dni, bo oferty składa się w całości elektronicznie (art. 138 ust. 4); krócej, nie mniej niż "
                    "15 dni – tylko po wstępnym ogłoszeniu informacyjnym albo przy uzasadnionej pilnej potrzebie (art. 138 ust. 2)")
    return 7, "poniżej progu Pzp: według regulaminu zamawiającego (zwykle co najmniej 7 dni)"



# ---------------------------------------------------------------- kryteria oceny – jeden wzór punktacji dla SWZ (AI) i oceny ofert
def _liczba_kr(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _podziel_kryteria(t):
    """„Cena – 60%, okres gwarancji – 40% (punktowany od 60 do 84 miesięcy; dłuższy jak 84)” → kryteria z uwagami w nawiasach (średnik w nawiasie nie dzieli)."""
    cz, buf, gl = [], "", 0
    for ch in str(t or ""):
        if ch == "(":
            gl += 1
        elif ch == ")":
            gl = max(0, gl - 1)
        if ch in ";,\n" and gl == 0:
            cz.append(buf)
            buf = ""
        else:
            buf += ch
    return [x for x in cz + [buf] if x.strip()]


def kryteria_z_tekstu(t):
    """Tekst kryteriów z kreatora → [{nazwa, waga, typ, od, do, opis}]. typ: min (cena, koszt, termin), max (gwarancja, doświadczenie), punktowe.
    Zakres punktowania z nawiasu („od 60 do 84”): wartość „od” = 0 pkt, „do” i więcej = pełna waga."""
    wyn = []
    for cz in _podziel_kryteria(t):
        nawias = " ".join(re.findall(r"\(([^)]*)\)", cz))
        bez = re.sub(r"\([^)]*\)", "", cz)
        mm = re.match(r"\s*(.+?)\s*(?:[–:-]\s*)?(\d+(?:[.,]\d+)?)\s*%", bez)
        if not mm:
            continue
        nazwa, waga = mm.group(1).strip(), float(mm.group(2).replace(",", "."))
        n = nazwa.lower()
        typ = "min" if re.search(r"cen|koszt|termin|czas", n) else "max" if re.search(r"gwaranc|doświadcz|rękojm", n) else "punktowe"
        k = {"nazwa": nazwa[:1].upper() + nazwa[1:], "waga": waga, "typ": typ}
        zz = re.search(r"od\s+(?:minimaln\w+\s+)?(\d+(?:[.,]\d+)?)\s*(?:\w+\s+)?do\s+(\d+(?:[.,]\d+)?)", nawias, re.I)
        if typ == "max" and zz and _liczba_kr(zz.group(2)) > _liczba_kr(zz.group(1)):
            k["od"], k["do"] = _liczba_kr(zz.group(1)), _liczba_kr(zz.group(2))
        k["opis"] = opis_kryterium(k)
        wyn.append(k)
    return wyn


def _pl(v):
    return PR.pl_liczby(f"{v:g}") if v is not None else ""


def opis_kryterium(k):
    """Sposób przyznawania punktów – dokładnie ten wzór, którym program liczy punkty w ocenie ofert (ocena_ofert._ranking_jeden)."""
    nazwa, typ = str(k.get("nazwa") or ""), (k.get("typ") or "min").lower()
    waga = _pl(_liczba_kr(k.get("waga")))
    if typ == "min":
        co = "cena" if re.search(r"cen", nazwa.lower()) else "wartość"
        naj = "najniższa cena" if co == "cena" else "najniższa wartość"
        return f"liczba punktów = ({naj} spośród ofert nieodrzuconych / {co} badanej oferty) × {waga}"
    if typ == "max":
        od, do = _liczba_kr(k.get("od")), _liczba_kr(k.get("do"))
        if od is not None and do is not None and do > od:
            return (f"liczba punktów = ((wartość w badanej ofercie, nie więcej niż {_pl(do)}) − {_pl(od)}) / ({_pl(do)} − {_pl(od)}) × {waga}; "
                    f"{_pl(od)} = 0 pkt, {_pl(do)} i więcej = {waga} pkt; wartość poniżej {_pl(od)} – oferta niezgodna z warunkami zamówienia")
        return f"liczba punktów = (wartość w badanej ofercie / najwyższa wartość spośród ofert nieodrzuconych) × {waga}"
    return f"punkty przyznane według opisu kryterium w SWZ, najwyżej {waga}"


def wzory_kryteriow(t):
    """Wzory punktacji do polecenia dla AI – SWZ ma zawierać dokładnie te wzory (program ocenia oferty według nich)."""
    return "; ".join(f"{k['nazwa']} (waga {_pl(k['waga'])}): {k['opis']}" for k in kryteria_z_tekstu(t))


def termin_z_godzina(data, godz):
    """„2027-02-08” + „10:00” → „08.02.2027, godz. 10:00” (bez godziny – sama data)."""
    try:
        d = dt.date.fromisoformat(str(data or "")[:10])
    except ValueError:
        return str(data or "")
    g = str(godz or "").strip()
    return f"{d:%d.%m.%Y}" + (f", godz. {g}" if re.fullmatch(r"\d{1,2}:\d{2}", g) else "")


def termin_otwarcia(data, godz):
    """Otwarcie ofert tego samego dnia 30 minut po terminie składania (art. 222 ust. 1 – nie później niż następnego dnia)."""
    g = str(godz or "").strip()
    if not re.fullmatch(r"\d{1,2}:\d{2}", g):
        return ""
    try:
        t = dt.datetime.combine(dt.date.fromisoformat(str(data or "")[:10]), dt.time(*map(int, g.split(":")))) + dt.timedelta(minutes=30)
    except ValueError:
        return ""
    return f"{t:%d.%m.%Y}, godz. {t:%H:%M}"


def pola_dokumentacji(K, nazwa, netto, tryb):
    """Pola do istniejącego generatora dokumentów (sporządzanie dokumentacji) z odpowiedzi kreatora."""
    p, w = K.get("potrzeba") or {}, K.get("warunki") or {}
    _n = lambda t: re.sub(r"\s+", " ", str(t or "")).strip().lower()
    zakres = "\n".join(f"{et}: {p[i]}" for i, et, *_ in PYTANIA.get(K.get("rodzaj"), []) if p.get(i) and _n(p[i]) != _n(K.get("opis")))
    cz = opis_czesci(czesci_normalizuj(K.get("czesci"), netto))
    return {"tryb": tryb, "nazwa": nazwa, "zakres": (K.get("opis") or "") + ("\n" + zakres if zakres else "") + ("\n\n" + cz if cz else ""),
            "wartosc": f"{netto:.2f} zł netto" if netto else "",
            "termin_realizacji": p.get("termin") or p.get("okres") or "", "wadium": w.get("wadium", ""), "warunki": w.get("warunki", ""),
            "kryteria": w.get("kryteria", "") + (("\nWZORY PUNKTACJI – wpisz do SWZ dokładnie te wzory (program ocenia oferty według nich, "
                                                  "inny wzór w SWZ da inny ranking): " + wzory_kryteriow(w.get("kryteria", "")))
                                                 if kryteria_z_tekstu(w.get("kryteria", "")) else ""), "gwarancja": w.get("gwarancja", "") or (p.get("gwarancja", "") if K.get("rodzaj") == "dostawy" else ""), "wynagrodzenie": w.get("wynagrodzenie", ""),
            "platnosci": w.get("platnosci", ""), "kary": w.get("kary", ""), "zabezpieczenie": w.get("zabezpieczenie", ""), "platforma": w.get("platforma", ""),
            "kontakt": w.get("kontakt", ""), "znak": K.get("znak", ""), "wykluczenie": w.get("wykluczenie", ""), "jedz": w.get("jedz", ""), "termin_ofert": termin_z_godzina(K.get("termin_ofert"), K.get("godzina_ofert")),
            "termin_otwarcia": termin_otwarcia(K.get("termin_ofert"), K.get("godzina_ofert")),
            "zamawiajacy": (K.get("zamawiajacy") or "").strip() or "[UZUPEŁNIJ: nazwa, adres i NIP zamawiającego]",
            "uwagi": "; ".join(x for x in (f"Waloryzacja: {w.get('waloryzacja')}" if w.get("waloryzacja") else "", f"Podwykonawstwo: {w.get('podwykonawstwo')}" if w.get("podwykonawstwo") else "",
                                           f"Podział na części: {w.get('czesci')}" if w.get("czesci") else "", f"Klauzule: {w.get('klauzule')}" if w.get("klauzule") else "") if x)}


# ---------------------------------------------------------------- sprawdzenie wzorów / dokumentów: propozycje zmian
SYSTEM_PRZEGLAD = (PR.INFO_AI + " Jesteś doświadczonym specjalistą ds. zamówień w Polsce (publicznych i prywatnych). Sprawdzasz dokumenty zamawiającego "
                   "(SWZ / zapytanie, OPZ, wzór umowy, formularze) i proponujesz KONKRETNE zmiany tekstu: zgodność z przepisami właściwymi dla tego "
                   "zamawiającego i trybu (Pzp z aktualnymi progami albo – poza Pzp – regulamin, wytyczne, Kodeks cywilny), "
                   "dopasowanie do tego zamówienia, usunięcie błędów i ryzyk. Każda zmiana to dokładny cytat z dokumentu i nowy tekst. "
                   "Odpowiadasz WYŁĄCZNIE JSON-em.")


def polecenie_przegladu(K, nazwa, netto, tryb_opis, dodatkowe="", max_prop=40, lista=""):
    """lista – lista kontrolna trybu i reżimu (lista_kontroli.lista_kreatora); bez niej – dawna lista ogólna Pzp."""
    p = K.get("potrzeba") or {}
    zgodnosc = ("(2) zgodność z LISTĄ KONTROLNĄ poniżej (każda pozycja, której dokumenty nie spełniają = propozycja zmiany)" if lista else
                "(2) zgodność z przepisami (próg 170 000 zł, limit kar art. 436, waloryzacja art. 439, „lub równoważny”, terminy składania ofert, "
                "warunki proporcjonalne, kryteria, RODO)")
    return (f"Zamówienie: {nazwa}. Rodzaj: {RODZAJE.get(K.get('rodzaj'), '')}. Opis: {K.get('opis') or ''}. Szczegóły: {json.dumps(p, ensure_ascii=False)}.\n"
            f"Wartość szacunkowa netto: {netto:.2f} zł → {tryb_opis}. Warunki ustalone przez zamawiającego: {json.dumps(K.get('warunki') or {}, ensure_ascii=False)}.\n"
            f"{('Dodatkowo zwróć uwagę na: ' + dodatkowe) if dodatkowe else ''}\n"
            "Sprawdź dokumenty powyżej i zaproponuj zmiany: (1) dopasowanie do TEGO zamówienia (przedmiot, terminy, wartość, tryb, warunki), "
            f"{zgodnosc}, (3) błędy, sprzeczności między dokumentami, nieaktualne odwołania.\n"
            + (lista + "\n" if lista else "") +
            'Zwróć JSON: {"podsumowanie": "2–4 zdania", "propozycje": [{"dokument": "nazwa pliku", "cytat": "DOSŁOWNY fragment obecnego tekstu (jedno '
            'zdanie albo akapit, 15–400 znaków, znak w znak)", "nowy": "proponowany nowy tekst tego fragmentu (pusty = usunąć)", "uzasadnienie": "dlaczego", '
            '"podstawa": "przepis albo dobra praktyka", "waga": "krytyczna | istotna | drobna"}], '
            '"dopisac": [{"dokument": "plik", "po_cytacie": "dosłowny fragment, po którym wstawić nowy akapit", "nowy": "treść nowego akapitu", '
            '"uzasadnienie": "…", "podstawa": "…"}]}. ' + f"Najważniejsze najpierw, maksymalnie {max_prop} propozycji.")



def polecenie_sprzecznosci(nazwy, dodatkowe="", max_prop=20):
    """Drugie spojrzenie na komplet: tylko sprzeczności MIĘDZY dokumentami (każdy dokument osobno tego nie wykryje)."""
    return (f"Powyżej jest komplet dokumentów zamówienia: {', '.join(nazwy)}.\n"
            f"{('Dodatkowo zwróć uwagę na: ' + dodatkowe) if dodatkowe else ''}\n"
            "Szukaj WYŁĄCZNIE sprzeczności między dokumentami: różne terminy (wykonania, składania ofert, związania ofertą, płatności), "
            "wadium, zabezpieczenie, okres gwarancji i rękojmi, kary umowne, kryteria i ich wagi, zakres i ilości, warunki udziału, "
            "nazwy i numery załączników, odesłania do nieistniejących punktów. Pomiń uwagi dotyczące jednego dokumentu.\n"
            "Przy każdej sprzeczności wskaż dokument, który należy poprawić (zwykle ten, który odbiega od SWZ / ustaleń zamawiającego), "
            "i podaj w uzasadnieniu, z którym dokumentem jest sprzeczny.\n"
            'Zwróć JSON: {"podsumowanie": "1–2 zdania", "propozycje": [{"dokument": "nazwa pliku do poprawienia – dokładnie jak na liście", '
            '"cytat": "DOSŁOWNY fragment tego dokumentu (15–300 znaków, znak w znak)", "nowy": "nowe brzmienie zgodne z drugim dokumentem", '
            '"uzasadnienie": "sprzeczne z: <dokument> – <czego dotyczy>", "podstawa": "przepis albo spójność dokumentacji", "waga": "krytyczna | istotna | drobna"}]}. '
            f"Maksymalnie {max_prop} propozycji, najważniejsze najpierw. Brak sprzeczności – pusta lista. Odpowiedź zacznij od znaku {{.")

# ---------------------------------------------------------------- wprowadzanie zmian do Worda (śledzenie zmian albo wersja czysta)
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _q(t):
    return "{%s}%s" % (W_NS, t)


def _norm(t):
    return re.sub(r"\s+", " ", str(t or "").replace("\u00a0", " ")).strip()


def _tekst_akapitu(p):
    return "".join(r.text for r in p.runs)


def _akapity(doc):
    for p in doc.paragraphs:
        yield p
    for t in doc.tables:
        for w in t.rows:
            for c in w.cells:
                for p in c.paragraphs:
                    yield p


def _znajdz(doc, cytat):
    c = _norm(cytat)
    if len(c) < 8:
        return None, -1
    for p in _akapity(doc):
        t = _norm(_tekst_akapitu(p))
        i = t.find(c)
        if i >= 0:
            return p, i
    krotki = c[:60]
    for p in _akapity(doc):
        t = _norm(_tekst_akapitu(p))
        if len(krotki) >= 25 and krotki in t:
            return p, t.find(krotki)
    return None, -1


def _run_xml(tekst, rpr, usuniety=False):
    from docx.oxml import OxmlElement
    r = OxmlElement("w:r")
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = OxmlElement("w:delText" if usuniety else "w:t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = tekst
    r.append(t)
    return r


def _zamien_w_akapicie(p, stary, nowy, sledz, autor, nr):
    """Podmienia fragment akapitu (cały tekst akapitu składany na nowo: przed + [usunięte/wstawione] + po), zachowując styl pierwszego przebiegu."""
    from docx.oxml import OxmlElement
    caly = _norm(_tekst_akapitu(p))
    st = _norm(stary)
    i = caly.find(st)
    if i < 0:
        return False
    przed, po = caly[:i], caly[i + len(st):]
    rpr = None
    if p.runs and p.runs[0]._r.find(_q("rPr")) is not None:
        rpr = p.runs[0]._r.find(_q("rPr"))
    for r in list(p._p):
        if r.tag in (_q("r"), _q("ins"), _q("del"), _q("hyperlink")):
            p._p.remove(r)
    data = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if przed:
        p._p.append(_run_xml(przed, rpr))
    if sledz:
        if st:
            d = OxmlElement("w:del")
            d.set(_q("id"), str(nr * 2 + 1000)); d.set(_q("author"), autor); d.set(_q("date"), data)
            d.append(_run_xml(st, rpr, usuniety=True))
            p._p.append(d)
        if nowy:
            n = OxmlElement("w:ins")
            n.set(_q("id"), str(nr * 2 + 1001)); n.set(_q("author"), autor); n.set(_q("date"), data)
            n.append(_run_xml(nowy, rpr))
            p._p.append(n)
    elif nowy:
        p._p.append(_run_xml(nowy, rpr))
    if po:
        p._p.append(_run_xml(po, rpr))
    return True


def _dopisz_po(p, nowy, sledz, autor, nr):
    from docx.oxml import OxmlElement
    nowy_p = copy.deepcopy(p._p)
    for r in list(nowy_p):
        if r.tag != _q("pPr"):
            nowy_p.remove(r)
    rpr = p.runs[0]._r.find(_q("rPr")) if p.runs and p.runs[0]._r.find(_q("rPr")) is not None else None
    if sledz:
        n = OxmlElement("w:ins")
        n.set(_q("id"), str(nr * 2 + 5001)); n.set(_q("author"), autor); n.set(_q("date"), dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        n.append(_run_xml(nowy, rpr))
        nowy_p.append(n)
    else:
        nowy_p.append(_run_xml(nowy, rpr))
    p._p.addnext(nowy_p)
    return True


def wprowadz_zmiany(sciezka_wzoru, zmiany, sciezka_wyj, sledz=True, autor="Bidivia"):
    """zmiany: [{"cytat","nowy"} | {"po_cytacie","nowy"}] → zapisany Word; zwraca (wprowadzone, nieodnalezione)."""
    import docx
    doc = docx.Document(sciezka_wzoru)
    ok, brak = [], []
    zmiany = sorted(zmiany, key=lambda z: 0 if z.get("po_cytacie") else 1)  # dopisania najpierw – szukają tekstu sprzed zmian
    for nr, z in enumerate(zmiany, 1):
        if z.get("po_cytacie"):
            p, _ = _znajdz(doc, z["po_cytacie"])
            (ok if p is not None and _dopisz_po(p, z.get("nowy") or "", sledz, autor, nr) else brak).append(z)
            continue
        p, _ = _znajdz(doc, z.get("cytat"))
        if p is None:
            brak.append(z)
            continue
        cyt = _norm(z.get("cytat"))
        if cyt not in _norm(_tekst_akapitu(p)):  # odnaleziony po początku cytatu – zamieniamy od początku do końca akapitu
            caly = _norm(_tekst_akapitu(p))
            cyt = caly[caly.find(cyt[:60]):]
        (ok if _zamien_w_akapicie(p, cyt, z.get("nowy") or "", sledz, autor, nr) else brak).append(z)
    doc.save(sciezka_wyj)
    return ok, brak


def lista_kontrolna(tryb, rodzaj, tryb_wybrany=None):
    """Lista kontrolna jako teksty – ta sama tabela co elementy() (jedna definicja pozycji dla wszystkich trybów)."""
    return [e["opis"] for e in elementy(tryb, rodzaj, False, tryb_wybrany)]


# ---------------------------------------------------------------- PDF → Word (żeby zmiany w SWZ / wzorach PDF dało się wprowadzić automatycznie)
RE_NOWY_AKAPIT = re.compile(r"^(\d{1,2}(\.\d{1,2})*[.)]\s|[a-z]\)\s|[-–•]\s|Rozdzia[łl]\b|ROZDZIA[ŁL]\b|§\s*\d|[IVXL]{1,5}\.\s|Art\.\s|Za[łl][aą]cznik)")


def pdf_na_docx(sciezka_pdf, sciezka_docx):
    """Konwersja PDF z warstwą tekstową do Worda. Najpierw pdf2docx (zachowuje układ i tabele), a gdy go brak –
    odtworzenie tekstu akapitami (numeracja, rozdziały i § jako osobne akapity; nagłówki i stopki stron usunięte).
    Zwraca (True, opis) albo (False, powód)."""
    try:
        from pdf2docx import Converter
        cv = Converter(sciezka_pdf)
        cv.convert(sciezka_docx)
        cv.close()
        if docx_ma_tekst(sciezka_docx):
            return True, "z zachowaniem układu"
    except Exception:
        pass
    if os.path.isfile(sciezka_docx):  # konwersja bez tekstu (np. skan – same obrazy stron) nie może zostać jako „wersja Word”
        os.remove(sciezka_docx)
    try:
        import pypdf
        strony = [(p.extract_text() or "") for p in pypdf.PdfReader(sciezka_pdf).pages]
    except Exception as e:
        return False, f"nie udało się odczytać PDF ({e})"
    if sum(len(s.strip()) for s in strony) < 30:
        return False, "PDF bez warstwy tekstowej (skan) – wgraj wersję Word albo PDF z tekstem"
    from collections import Counter
    linie_stron = [[l.strip() for l in s.splitlines() if l.strip()] for s in strony]
    powt = Counter(l for ls in linie_stron for l in set(ls[:2] + ls[-2:]))
    stopki = {l for l, n in powt.items() if n >= max(2, len(strony) // 2)}
    akapity, biez = [], ""
    for ls in linie_stron:
        for l in ls:
            if l in stopki or re.fullmatch(r"(str(ona)?\.?\s*)?\d{1,3}(\s*(z|/)\s*\d{1,3})?", l, flags=re.I):
                continue
            if not biez:
                biez = l
            elif RE_NOWY_AKAPIT.match(l) or re.search(r"[.:;]$", biez) and (l[:1].isupper() or l[:1].isdigit()):
                akapity.append(biez)
                biez = l
            elif biez.endswith("-") and not biez.endswith(" -"):
                biez = biez[:-1] + l
            else:
                biez += " " + l
    if biez:
        akapity.append(biez)
    import docx
    d = docx.Document()
    for a in akapity:
        p = d.add_paragraph()
        r = p.add_run(a)
        if re.match(r"^(Rozdzia[łl]|ROZDZIA[ŁL]|§\s*\d+\.?$|[IVXL]{1,5}\.\s)", a) or (a.isupper() and len(a) < 120):
            r.bold = True
    d.save(sciezka_docx)
    return True, "tekst odtworzony akapitami (sprawdź formatowanie)"


def docx_ma_tekst(sciezka, minimum=30):
    """Czy Word ma tekst do sprawdzenia (także w tabelach i polach tekstowych) – plik z samymi obrazami stron to skan."""
    try:
        import zipfile
        xml = zipfile.ZipFile(sciezka).read("word/document.xml").decode("utf-8", "ignore")
        return len(re.sub(r"\s+", "", "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)))) >= minimum
    except Exception:
        return False


# ---------------------------------------------------------------- elementy postępowania (lista kontrolna, która działa)
# rodzaj: "pismo" – program przygotuje (albo wgrasz własny wzór); "sprawdzenie" – sprawdzane w kroku „Sprawdzenie i zmiany”;
# "auto" – status wynika z danych kreatora
POWODY_BRAKU_CZESCI = [
    "podział mógłby spowodować nadmierne trudności techniczne wykonania zamówienia",
    "podział mógłby spowodować nadmierne koszty wykonania zamówienia",
    "konieczność skoordynowania działań różnych wykonawców realizujących poszczególne części groziłaby właściwemu wykonaniu zamówienia",
    "przedmiot zamówienia stanowi funkcjonalną i technologiczną całość (jeden obiekt / jeden proces)",
    "jeden wykonawca zapewni jednolitą odpowiedzialność, gwarancję i rękojmię za cały przedmiot zamówienia",
]


# ---------------------------------------------------------------- podział zamówienia na części (art. 91 Pzp)
def _kw(v):
    return liczba(v, 0.0, 2)


def _int_lub_brak(v):
    try:
        n = int(str(v).strip())
        return n if n > 0 else None
    except (TypeError, ValueError):
        return None


def czesci_normalizuj(c, netto=0.0):
    """Podział na części z kreatora: oczyszczone dane i lista problemów do pokazania użytkownikowi."""
    c = c if isinstance(c, dict) else {}
    lista = []
    for i, x in enumerate([x for x in (c.get("lista") or []) if isinstance(x, dict)], 1):
        lista.append({"nr": i, "nazwa": str(x.get("nazwa") or "").strip()[:200], "zakres": str(x.get("zakres") or "").strip()[:2000],
                      "wartosc": _kw(x.get("wartosc")), "cpv": str(x.get("cpv") or "").strip()[:40], "termin": str(x.get("termin") or "").strip()[:120]})
    wyn = {"podzial": bool(c.get("podzial")), "lista": lista, "max_ofert": _int_lub_brak(c.get("max_ofert")),
           "max_udzielen": _int_lub_brak(c.get("max_udzielen")), "zasady_limitu": str(c.get("zasady_limitu") or "").strip()[:1000],
           "uzasadnienie": str(c.get("uzasadnienie") or "").strip()[:2000]}
    bledy = []
    if wyn["podzial"]:
        if len(lista) < 2:
            bledy.append("Podział wymaga co najmniej dwóch części.")
        if any(not x["nazwa"] for x in lista):
            bledy.append("Każda część musi mieć nazwę.")
        suma = round(sum(x["wartosc"] for x in lista), 2)
        if netto and lista and abs(suma - netto) > max(1.0, netto * 0.005):
            bledy.append(f"Suma wartości części ({PR.liczba_pl(suma)} zł) różni się od wartości zamówienia ({PR.liczba_pl(netto)} zł). Tryb i progi ustala się "
                         "według łącznej wartości wszystkich części (art. 30 Pzp) – popraw wartości części albo szacowanie.")
        if any(not x["wartosc"] for x in lista):
            bledy.append("Podaj szacunkową wartość każdej części.")
        n = len(lista)
        if wyn["max_ofert"] and wyn["max_ofert"] >= n:
            wyn["max_ofert"] = None  # brak ograniczenia
        if wyn["max_udzielen"] and wyn["max_udzielen"] >= n:
            wyn["max_udzielen"] = None
        if wyn["max_udzielen"] and not wyn["zasady_limitu"]:
            bledy.append("Przy ograniczeniu liczby części dla jednego wykonawcy podaj obiektywne zasady wyboru części, które otrzyma (art. 91 ust. 3).")
    wyn["suma"] = round(sum(x["wartosc"] for x in lista), 2)
    wyn["bledy"] = bledy
    return wyn


def opis_czesci(c):
    """Opis podziału do kontekstu generatora dokumentów (SWZ, formularz, umowa, OPZ)."""
    if not (c or {}).get("podzial") or not c.get("lista"):
        return ""
    w = [f"ZAMÓWIENIE PODZIELONE NA {len(c['lista'])} CZĘŚCI (art. 91 Pzp) – uwzględnij podział w każdym dokumencie:"]
    for x in c["lista"]:
        w.append(f"Część {x['nr']}: {x['nazwa']}" + (f" – zakres: {x['zakres']}" if x["zakres"] else "") + (f"; CPV {x['cpv']}" if x["cpv"] else "")
                 + (f"; termin realizacji: {x['termin']}" if x["termin"] else ""))
    w.append("Oferty można składać na wszystkie części." if not c.get("max_ofert") else f"Ofertę można złożyć maksymalnie na {c['max_ofert']} części.")
    if c.get("max_udzielen"):
        w.append(f"Jednemu wykonawcy można udzielić zamówienia maksymalnie na {c['max_udzielen']} części; zasady wyboru części: {c.get('zasady_limitu')}.")
    w.append("Wymagania: SWZ – opis każdej części, warunki udziału, kryteria oceny, wadium i termin realizacji osobno dla każdej części oraz zasady składania "
             "ofert na części; formularz ofertowy – cena (i inne kryteria) osobno dla każdej części, z polem wyboru części, na które wykonawca składa ofertę; "
             "wzór umowy – odrębna umowa dla każdej części (wspólny wzór z oznaczeniem części, przedmiotu i wynagrodzenia); opis przedmiotu – w podziale na części. "
             "Wartości szacunkowe części nie są podawane wykonawcom.")
    return "\n".join(w)


SYSTEM_CZESCI = ("Jesteś specjalistą ds. zamówień publicznych w Polsce. Proponujesz podział zamówienia na części zgodnie z art. 91 Pzp: części mają być "
                 "samodzielne, możliwe do odrębnego wykonania i odbioru, sprzyjać udziałowi małych i średnich przedsiębiorstw, a jednocześnie nie powodować "
                 "nadmiernych trudności technicznych, nadmiernych kosztów ani ryzyka niewłaściwej koordynacji. Nigdy nie dzielisz zamówienia w celu uniknięcia "
                 "stosowania przepisów – tryb zależy od łącznej wartości wszystkich części. Odpowiadasz wyłącznie poprawnym JSON, bez komentarzy.")


def polecenie_podzialu(K, nazwa, netto, dzialy=None):
    p = K.get("potrzeba") or {}
    zakres = "\n".join(f"{et}: {p[i]}" for i, et, *_ in PYTANIA.get(K.get("rodzaj"), []) if p.get(i))
    dz = "\n".join(f"- {d.get('nazwa')}: {PR.liczba_pl(float(d.get('wartosc') or 0))} zł netto" for d in (dzialy or []) if d.get("nazwa"))
    return (f"Zamówienie: {nazwa}\nRodzaj: {RODZAJE.get(K.get('rodzaj'), K.get('rodzaj'))}\nOpis: {K.get('opis') or ''}\n{zakres}\n"
            f"Łączna wartość szacunkowa: {PR.liczba_pl(netto)} zł netto\n" + (f"Działy kosztorysu:\n{dz}\n" if dz else "")
            + "Zaproponuj, czy i jak podzielić zamówienie na części (branże, lokalizacje, etapy, grupy asortymentu). Wartości części mają sumować się do "
              "łącznej wartości. Jeżeli podział nie jest uzasadniony, zwróć pustą listę i podaj powody braku podziału (art. 91 ust. 2). Format JSON:\n"
              '{"podzial_zalecany": true, "lista": [{"nazwa": "", "zakres": "", "wartosc": 0, "cpv": "", "termin": ""}], '
              '"uzasadnienie": "dlaczego taki podział (2–4 zdania)", "ryzyka": ["ryzyko koordynacji itp."], "powody_braku_podzialu": ""}')


# Grupy trybów listy kontrolnej (krok 7 „Gotowe do publikacji”) – opis: Bidivia_lista_kontrolna_wg_trybu.docx (9.11.2026)
GRUPA_TRYBU = {"podstawowy_1": "A", "podstawowy_2": "A", "podstawowy_3": "A",
               "przetarg_nieograniczony": "B", "przetarg_ograniczony": "B", "negocjacje_z_ogloszeniem": "B", "dialog": "B",
               "partnerstwo": "C", "negocjacje_bez_ogloszenia": "D", "wolna_reka": "E",
               "ponizej_progu": "F", "zasada_konkurencyjnosci": "G"}
GRUPA_Z_WARTOSCI = {"pzp_podstawowy": "A", "pzp_nieograniczony": "B", "pzp_inny": "A", "ponizej_130": "F", "konkurencyjnosc": "G"}
GRUPY_PZP = ("A", "B", "C", "D", "E")


def grupa_trybu(tryb, tryb_wybrany=None):
    """A tryb podstawowy · B tryby unijne konkurencyjne · C partnerstwo · D negocjacje bez ogłoszenia · E wolna ręka ·
    F poniżej progu (regulamin) · G zasada konkurencyjności."""
    return GRUPA_TRYBU.get(tryb_wybrany) or GRUPA_Z_WARTOSCI.get(tryb, "F")


def elementy(tryb, rodzaj, podzial=False, tryb_wybrany=None):
    """Lista kontrolna przed publikacją według grupy trybu. tryb – kategoria z wartości (pzp_podstawowy / pzp_nieograniczony = od progów UE…),
    tryb_wybrany – tryb wybrany w kreatorze (klucz TRYBY_WYBOR)."""
    g = grupa_trybu(tryb, tryb_wybrany)
    unijna = tryb == "pzp_nieograniczony"  # wartość od progów unijnych – procedura unijna (partnerstwo, negocjacje bez ogłoszenia, wolna ręka)
    E = [("kosztorys", ("Kosztorys inwestorski albo planowane koszty według PFU i notatka z szacowania (data nie starsza niż 6 mies.)" if rodzaj == "roboty"
                        else "Szacowanie wartości (źródła cen) i notatka z szacowania (data nie starsza niż 3 mies.)"), "auto"),
         ("opz", "Opis przedmiotu zamówienia bez nazw producentów (albo z „lub równoważny” i kryteriami równoważności)", "sprawdzenie"),
         ("warunki", "Warunki udziału – opcjonalnie w zamówieniu z wolnej ręki; jeśli są, proporcjonalne do przedmiotu i wartości" if g == "E"
          else "Warunki udziału proporcjonalne do przedmiotu i wartości", "sprawdzenie")]
    if g != "E":  # wolna ręka: negocjacje z jednym wykonawcą – bez kryteriów oceny ofert
        E.append(("kryteria", "Kryteria oceny z wagami i sposobem przyznawania punktów", "sprawdzenie"))
    E += [("umowa", "Wzór umowy: kary z łącznym limitem, zmiany umowy, odbiory, płatności" if g != "E"
           else "Projektowane postanowienia umowy (przekazywane z zaproszeniem do negocjacji): kary z łącznym limitem, zmiany, odbiory, płatności", "sprawdzenie"),
          ("rodo", "Klauzula informacyjna RODO", "pismo")]
    if g in GRUPY_PZP:
        E += [("plan", "Plan postępowań – zamówienie ujęte w planie na dany rok (art. 23)", "pismo"),
              ("waloryzacja", "Klauzula waloryzacyjna przy umowie dłuższej niż 6 miesięcy (art. 439)", "sprawdzenie"),
              ("platnosci", "Umowa zawarta na okres dłuższy niż 12 miesięcy: wynagrodzenie płatne w częściach albo zaliczki – ostatnia część najwyżej 50% wynagrodzenia, zaliczka co najmniej 5% (art. 443)", "sprawdzenie")]
        if g != "E":
            E.append(("czesci", "Podział na części: opis części, kryteria i wadium dla każdej części, zasady składania ofert na części (art. 91)", "sprawdzenie")
                     if podzial else ("czesci", "Uzasadnienie braku podziału na części (art. 91)", "pismo"))
        uzas = {"B": "Uzasadnienie wyboru trybu – przesłanka negocjacji z ogłoszeniem / dialogu konkurencyjnego (art. 129 ust. 2)",
                "C": "Uzasadnienie wyboru trybu partnerstwa innowacyjnego – potrzeba innowacyjnego rozwiązania niedostępnego na rynku",
                "D": "Uzasadnienie wyboru trybu negocjacji bez ogłoszenia – przesłanka ustawowa (" + ("art. 209" if unijna else "art. 301") + ")",
                "E": "Uzasadnienie wyboru trybu zamówienia z wolnej ręki – przesłanka ustawowa (" + ("art. 214 ust. 1" if unijna else "art. 305") + ")"}
        if g == "A":
            E.append(("ogloszenie", "Ogłoszenie o zamówieniu w BZP – dane do formularza", "pismo"))
        elif g == "B":
            E.append(("ogloszenie", "Ogłoszenie o zamówieniu w Dzienniku Urzędowym UE – dane do formularza", "pismo"))
        elif g == "C":
            E.append(("ogloszenie", "Ogłoszenie o zamówieniu w " + ("Dzienniku Urzędowym UE" if unijna else "BZP") + " – dane do formularza", "pismo"))
        elif g == "D":
            E.append(("ogloszenia_bez", "Bez ogłoszenia o zamówieniu – zaproszenie do negocjacji wybranych wykonawców; " + (
                "po udzieleniu zamówienia ogłoszenie o udzieleniu zamówienia w Dzienniku Urzędowym UE" if unijna else
                "możliwe ogłoszenie o zamiarze zawarcia umowy w BZP (art. 302); po zakończeniu ogłoszenie o wyniku w BZP – do 30 dni (art. 309)"), "reczne"))
        else:
            E.append(("ogloszenia_bez", "Bez ogłoszenia o zamówieniu – zaproszenie do negocjacji jednego wykonawcy; zamówienie in-house (art. 214 ust. 1 pkt 11–14): "
                      "ogłoszenie o zamiarze zawarcia umowy w BZP i co najmniej 14 dni do zawarcia umowy (art. 216); po zakończeniu – ogłoszenie o wyniku", "reczne"))
        if g in uzas and (g != "B" or tryb_wybrany in ("dialog", "negocjacje_z_ogloszeniem")):
            E.append(("uzasadnienie_trybu", uzas[g], "sprawdzenie"))
        E.append(("oswiadczenia", {"B": "Oświadczenie JEDZ (art. 125) i wykaz podmiotowych środków dowodowych",
                                   "D": "Oświadczenia wykonawcy (art. 125) i wykaz podmiotowych środków dowodowych (przy pilnej potrzebie – art. 301 ust. 1 pkt 3 – można odstąpić od oświadczenia)",
                                   "E": "Podmiotowe środki dowodowe – brak podstaw wykluczenia (najpóźniej do zawarcia umowy); oświadczenie z art. 125 – opcjonalnie, wskazać w zaproszeniu (art. 217)"}
                  .get(g, "Oświadczenia wykonawcy (art. 125) i wykaz podmiotowych środków dowodowych"), "auto"))
        if g != "E":
            E.append(("kwota", "Kwota na sfinansowanie zamówienia do podania przed otwarciem ofert (art. 222 ust. 4)", "pismo"))
        E.append(("komisja", "Oświadczenia osób wykonujących czynności w postępowaniu – brak konfliktu interesów (art. 56)", "pismo"))
    elif g == "G":
        E += [("bk2021", "Publikacja zapytania ofertowego i informacji o wyniku w Bazie Konkurencyjności (BK2021)", "reczne"),
              ("termin_bk", "Termin składania ofert: co najmniej 7 dni (dostawy, usługi), 14 dni (roboty budowlane), 30 dni (od progów z wytycznych: dostawy i usługi – 750 000 euro, roboty budowlane – próg unijny, od 1.01.2026 r. 5 404 000 euro)", "reczne"),
              ("powiazania", "Konflikt interesów – brak powiązań osobowych i kapitałowych wykonawców z zamawiającym, oświadczenia (wytyczne 2021–2027 i umowa o dofinansowanie)", "sprawdzenie")]
    else:
        E += [("regulamin", "Zgodność z regulaminem udzielania zamówień jednostki", "sprawdzenie"),
              ("upublicznienie", "Sposób upublicznienia zapytania (strona / BIP / platforma / Baza Konkurencyjności)", "sprawdzenie")]
    return [{"id": i, "opis": o, "rodzaj": r} for i, o, r in E]


def _dok_naglowek(tytul, zam, nazwa, znak=""):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(10)
    p = d.add_paragraph(zam or "[UZUPEŁNIJ: zamawiający]")
    p.runs[0].bold = True
    if znak:
        d.add_paragraph(f"Znak sprawy: {znak}")
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(tytul)
    r.bold, r.font.size = True, Pt(13)
    if nazwa:
        p = d.add_paragraph(f"dotyczy postępowania: {nazwa}")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return d


def _tabela(d, wiersze):
    t = d.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for a, b in wiersze:
        c = t.add_row().cells
        c[0].text, c[1].text = str(a), str(b or "[UZUPEŁNIJ]")
        c[0].paragraphs[0].runs[0].bold = True


MIESIACE = ("styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień")


def data_pl(v):
    try:
        return dt.date.fromisoformat(str(v or "")[:10]).strftime("%d.%m.%Y")
    except ValueError:
        return str(v or "")


def okres_wszczecia(v):
    """Planowana data wszczęcia → „styczeń 2027 (I kwartał 2027)” do planu postępowań."""
    try:
        d = dt.date.fromisoformat(str(v or "")[:10])
    except ValueError:
        return ""
    return f"{MIESIACE[d.month - 1]} {d.year} ({('I', 'II', 'III', 'IV')[(d.month - 1) // 3]} kwartał {d.year})"


def rok_planu(K):
    """Rok planu postępowań: rok planowanego wszczęcia (albo terminu ofert), inaczej bieżący."""
    for v in ((K or {}).get("data_wszczecia"), (K or {}).get("termin_ofert")):
        try:
            return dt.date.fromisoformat(str(v or "")[:10]).year
        except ValueError:
            pass
    return dt.date.today().year


def czesci_ogloszenia(tekst, powody):
    """Pole „Podział na części” w ogłoszeniu: powody z listy kontrolnej zamiast znacznika [UZUPEŁNIJ]."""
    tekst = str(tekst or "")
    if powody and "[UZUPEŁNIJ" in tekst:
        return re.sub(r"\s*–?\s*\[UZUPEŁNIJ[^\]]*\]", "", tekst).strip() + " – " + "; ".join(powody)
    return tekst


def pismo(el, ctx, dane, sciezka):
    """Przygotowanie pisma postępowania (Word) z danych kreatora. ctx: nazwa, zamawiajacy, rodzaj, tryb_opis, netto, brutto,
    warunki, potrzeba, znak, termin_ofert; dane – odpowiedzi użytkownika dla tego pisma."""
    zam, nazwa, znak = ctx["zamawiajacy"], ctx["nazwa"], ctx.get("znak", "")
    dzis = dt.date.today().strftime("%d.%m.%Y")
    if el == "rodo":
        d = _dok_naglowek("KLAUZULA INFORMACYJNA RODO", zam, nazwa, znak)
        for t in [
            "Zgodnie z art. 13 ust. 1 i 2 rozporządzenia Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. (RODO) informuję, że:",
            f"1) administratorem Pani/Pana danych osobowych jest {zam};",
            f"2) kontakt z inspektorem ochrony danych osobowych: {dane.get('iod') or '[UZUPEŁNIJ: e-mail / adres IOD]'};",
            f"3) Pani/Pana dane osobowe przetwarzane będą na podstawie art. 6 ust. 1 lit. c RODO w celu związanym z postępowaniem o udzielenie zamówienia „{nazwa}”;",
            "4) odbiorcami Pani/Pana danych osobowych będą osoby lub podmioty, którym udostępniona zostanie dokumentacja postępowania w oparciu o art. 18 oraz art. 74 ustawy Prawo zamówień publicznych;",
            "5) Pani/Pana dane osobowe będą przechowywane, zgodnie z art. 78 ust. 1 ustawy Pzp, przez okres 4 lat od dnia zakończenia postępowania o udzielenie zamówienia, a jeżeli czas trwania umowy przekracza 4 lata – przez cały czas trwania umowy;",
            "6) obowiązek podania danych osobowych bezpośrednio Pani/Pana dotyczących jest wymogiem ustawowym określonym w przepisach ustawy Pzp, związanym z udziałem w postępowaniu; konsekwencje niepodania określonych danych wynikają z ustawy Pzp;",
            "7) w odniesieniu do Pani/Pana danych osobowych decyzje nie będą podejmowane w sposób zautomatyzowany, stosownie do art. 22 RODO;",
            "8) posiada Pani/Pan: prawo dostępu do danych (art. 15 RODO); prawo do ich sprostowania (art. 16 RODO) – skorzystanie z tego prawa nie może skutkować zmianą wyniku postępowania ani zmianą postanowień umowy w zakresie niezgodnym z ustawą Pzp oraz nie może naruszać integralności protokołu oraz jego załączników; prawo żądania ograniczenia przetwarzania (art. 18 RODO) z zastrzeżeniem przypadków, o których mowa w art. 18 ust. 2 RODO; prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych, gdy uzna Pani/Pan, że przetwarzanie danych narusza przepisy RODO;",
            "9) nie przysługuje Pani/Panu: prawo do usunięcia danych (art. 17 ust. 3 lit. b, d lub e RODO), prawo do przenoszenia danych (art. 20 RODO) ani prawo sprzeciwu (art. 21 RODO), gdyż podstawą prawną przetwarzania jest art. 6 ust. 1 lit. c RODO."]:
            d.add_paragraph(t)
    elif el == "kwota":
        kw_ = liczba(dane.get("kwota")) if dane.get("kwota") else None  # kwota z ekranu (np. „1080000” z podpowiedzi) w zapisie „1 080 000,00”
        kw = (PR.liczba_pl(kw_) if kw_ else dane.get("kwota")) or (PR.liczba_pl(ctx['brutto']) if ctx.get("brutto") else "")
        # kwota wyliczona z netto przy stawce VAT nieustalonej (23%, jak w ocenie ofert – ZE-27) – także gdy pole na ekranie zostawiono z tą podpowiedzią
        sprawdz_vat = bool(kw) and ctx.get("stawka_vat_znana") is False and (not dane.get("kwota") or abs((kw_ or 0) - float(ctx.get("brutto") or 0)) < 0.01)
        d = _dok_naglowek("INFORMACJA O KWOCIE PRZEZNACZONEJ NA SFINANSOWANIE ZAMÓWIENIA", zam, nazwa, znak)
        d.add_paragraph(f"Działając na podstawie art. 222 ust. 4 ustawy Prawo zamówień publicznych, Zamawiający informuje, że na sfinansowanie "
                        f"zamówienia zamierza przeznaczyć kwotę: {kw or '[UZUPEŁNIJ]'} zł brutto."
                        + (" [UZUPEŁNIJ: sprawdź stawkę VAT – kwotę wyliczono z wartości netto przy VAT 23%, bo stawki nie ustalono w kosztorysie zamówienia]"
                           if sprawdz_vat else ""))
        d.add_paragraph("Informację udostępnia się na stronie internetowej prowadzonego postępowania najpóźniej przed otwarciem ofert.")
        d.add_paragraph(f"\n{dzis}\n\n.................................................\n(podpis kierownika zamawiającego lub osoby upoważnionej)")
    elif el == "czesci":
        powody = dane.get("powody") or []
        d = _dok_naglowek("UZASADNIENIE BRAKU PODZIAŁU ZAMÓWIENIA NA CZĘŚCI", zam, nazwa, znak)
        d.add_paragraph("Na podstawie art. 91 ust. 2 ustawy Prawo zamówień publicznych Zamawiający wskazuje powody niedokonania podziału zamówienia na części:")
        for pw in powody or ["[UZUPEŁNIJ: powody]"]:
            d.add_paragraph(pw, style="List Bullet")
        if dane.get("dodatkowe"):
            d.add_paragraph(dane["dodatkowe"])
        d.add_paragraph("Zamawiający zapewnia jednocześnie udział małych i średnich przedsiębiorstw – warunki udziału w postępowaniu są proporcjonalne "
                        "do przedmiotu zamówienia, a wykonawcy mogą powierzać części zamówienia podwykonawcom i polegać na zasobach innych podmiotów.")
        d.add_paragraph("Uzasadnienie zamieszcza się w dokumentach zamówienia (SWZ) albo w protokole postępowania.")
    elif el == "plan":
        d = _dok_naglowek("POZYCJA PLANU POSTĘPOWAŃ O UDZIELENIE ZAMÓWIEŃ – DO AKTUALIZACJI", zam, nazwa, znak)
        _tabela(d, [("Przedmiot zamówienia", nazwa), ("Rodzaj zamówienia", RODZAJE.get(ctx["rodzaj"], "")),
                    ("Przewidywany tryb albo procedura", ctx["tryb_opis"]),
                    ("Orientacyjna wartość zamówienia (netto)", PR.liczba_pl(ctx['netto']) + " zł" if ctx.get("netto") else ""),
                    ("Przewidywany termin wszczęcia (kwartał / miesiąc)", dane.get("termin") or okres_wszczecia(ctx.get("data_wszczecia")) or "[UZUPEŁNIJ]"),
                    ("Informacje dodatkowe (np. umowa ramowa, zamówienie zastrzeżone – art. 94)", dane.get("dodatkowe") or "brak")])
        d.add_paragraph("Plan postępowań zamawiający publiczny zamieszcza w Biuletynie Zamówień Publicznych i na stronie internetowej (art. 23 Pzp); "
                        "nową pozycję dodaje się w aktualizacji planu. Zamieszczenie pozycji w planie nie zobowiązuje do przeprowadzenia postępowania.")
    elif el == "ogloszenie":
        w, p = ctx.get("warunki") or {}, ctx.get("potrzeba") or {}
        to_ = str(ctx.get("tryb_opis") or "").lower()  # tryby unijne (i wartość od progów UE) – Dziennik Urzędowy UE, krajowe – BZP
        ue_ = any(x in to_ for x in ("przetarg nieograniczony", "przetarg ograniczony", "negocjacje z ogłoszeniem", "dialog", "procedura unijna")) or (
            "partnerstwo" in to_ and tryb_z_wartosci(float(ctx.get("netto") or 0), ctx.get("rodzaj") or "roboty")[0] == "pzp_nieograniczony")
        d = _dok_naglowek("DANE DO OGŁOSZENIA O ZAMÓWIENIU (" + ("DZIENNIK URZĘDOWY UE" if ue_ else "BZP") + ")", zam, nazwa, znak)
        _tabela(d, [("Zamawiający", zam), ("Nazwa zamówienia", nazwa), ("Identyfikator / znak sprawy", znak),
                    ("Rodzaj zamówienia", RODZAJE.get(ctx["rodzaj"], "")), ("Tryb", ctx["tryb_opis"]),
                    ("Krótki opis przedmiotu", (ctx.get("opis") or "")[:600]), ("Główny kod CPV", dane.get("cpv") or ""),
                    ("Podział na części", czesci_ogloszenia(w.get("czesci", ""), ctx.get("czesci_powody"))), ("Okres realizacji", p.get("termin") or p.get("okres") or ""),
                    ("Warunki udziału", w.get("warunki", "")), ("Kryteria oceny ofert", w.get("kryteria", "")), ("Wadium", w.get("wadium", "")),
                    ("Zabezpieczenie należytego wykonania umowy", w.get("zabezpieczenie", "")), ("Sposób składania ofert", w.get("platforma", "")),
                    ("Termin składania ofert", data_pl(ctx.get("termin_ofert")) + (", godz. [UZUPEŁNIJ]" if ctx.get("termin_ofert") else "[UZUPEŁNIJ]")),
                    ("Termin otwarcia ofert", dane.get("otwarcie") or ""),
                    ("Termin związania ofertą", dane.get("zwiazanie") or "30 dni od upływu terminu składania ofert"),
                    ("Wymagania dot. zatrudnienia (art. 95)", w.get("klauzule", ""))])
        d.add_paragraph("Ogłoszenie wypełnia się w formularzu na platformie e-Zamówienia; pola mogą różnić się nazwami – przepisz odpowiednie dane.")
    elif el == "komisja":
        d = _dok_naglowek("OŚWIADCZENIE O BRAKU PODSTAW DO WYŁĄCZENIA Z POSTĘPOWANIA (art. 56 ustawy Pzp)", zam, nazwa, znak)
        d.add_paragraph("Imię i nazwisko: ...............................................   Funkcja w postępowaniu: ...............................................")
        for t in ["Oświadczam, że nie podlegam wyłączeniu z postępowania na podstawie art. 56 ust. 2 i 3 ustawy Prawo zamówień publicznych, w szczególności:",
                  "1) nie ubiegam się o udzielenie tego zamówienia;",
                  "2) nie pozostaję w związku małżeńskim, w stosunku pokrewieństwa lub powinowactwa w linii prostej, pokrewieństwa lub powinowactwa w linii bocznej do drugiego stopnia, nie jestem związany(-a) z tytułu przysposobienia, opieki lub kurateli albo nie pozostaję we wspólnym pożyciu z wykonawcą, jego zastępcą prawnym lub członkami organów zarządzających lub organów nadzorczych wykonawców ubiegających się o udzielenie zamówienia;",
                  "3) w okresie 3 lat przed wszczęciem postępowania nie pozostawałem(-am) w stosunku pracy lub zlecenia z wykonawcą, nie byłem(-am) członkiem organów zarządzających lub nadzorczych wykonawców ubiegających się o udzielenie zamówienia;",
                  "4) nie pozostaję z wykonawcą w takim stosunku prawnym lub faktycznym, że istnieje uzasadniona wątpliwość co do mojej bezstronności lub niezależności w związku z postępowaniem;",
                  "5) nie zostałem(-am) prawomocnie skazany(-a) za przestępstwo popełnione w związku z postępowaniem o udzielenie zamówienia, przestępstwo przekupstwa, przestępstwo przeciwko obrotowi gospodarczemu lub inne przestępstwo popełnione w celu osiągnięcia korzyści majątkowych;",
                  "6) nie mam, w rozumieniu art. 56 ust. 3 ustawy Pzp, bezpośrednio lub pośrednio interesu finansowego, ekonomicznego lub innego interesu osobistego, który postrzegany mógłby być jako zagrażający mojej bezstronności lub niezależności w związku z postępowaniem.",
                  "Oświadczenie składam po zapoznaniu się z listą wykonawców, którzy złożyli oferty. W przypadku zaistnienia okoliczności powodujących wyłączenie niezwłocznie poinformuję o tym kierownika zamawiającego.",
                  "\n.................................................          .................................................\n(miejscowość, data)                                                   (podpis)"]:
            d.add_paragraph(t)
    else:
        return False
    import modul_oferty as _MO  # miejsca do uzupełnienia na żółto
    _MO.zapisz_z_zaznaczeniem(d, sciezka)
    return True


PLIKI_PISM = {"rodo": "Klauzula_informacyjna_RODO", "kwota": "Informacja_o_kwocie_na_sfinansowanie_zamowienia", "czesci": "Uzasadnienie_braku_podzialu_na_czesci",
              "plan": "Pozycja_planu_postepowan", "ogloszenie": "Dane_do_ogloszenia_o_zamowieniu", "komisja": "Oswiadczenie_art_56_brak_konfliktu_interesow"}


# ---------------------------------------------------------------- uzupełnianie kreatora z dokumentów (lista potrzeb, ogłoszenie, SWZ, notatka…)
POLA_CO = [("co.nazwa", "Nazwa zamówienia"), ("co.opis", "Krótki opis – co, gdzie, na kiedy"), ("co.zamawiajacy", "Zamawiający (nazwa, adres, NIP)"),
           ("co.cpv", "Główny kod CPV"), ("co.znak", "Znak sprawy"), ("wartosc", "Wartość zamówienia netto [zł] (jeśli podana)"),
           ("co.tryb_dok", "Tryb udzielenia zamówienia z podstawą prawną – dosłownie z dokumentu (np. tryb podstawowy bez negocjacji, art. 275 pkt 1 Pzp)")]
ETYKIETY_WARUNKOW = {"wynagrodzenie": "Wynagrodzenie (ryczałtowe / kosztorysowe)", "kryteria": "Kryteria oceny ofert z wagami", "warunki": "Warunki udziału",
                     "gwarancja": "Gwarancja / rękojmia", "kary": "Kary umowne", "wadium": "Wadium", "zabezpieczenie": "Zabezpieczenie należytego wykonania",
                     "platnosci": "Płatności", "waloryzacja": "Waloryzacja wynagrodzenia", "podwykonawstwo": "Podwykonawstwo", "czesci": "Podział na części",
                     "klauzule": "Klauzule społeczne / zatrudnienie", "platforma": "Sposób składania ofert", "kontakt": "Osoba do kontaktu"}
DO_AKTUALIZACJI = {"co.znak", "wartosc", "potrzeba.termin", "potrzeba.okres"}


def polecenie_importu(rodzaj):
    rodz = [rodzaj] if rodzaj in PYTANIA else list(PYTANIA)
    pola = POLA_CO + [(f"potrzeba.{i}", f"{et} [{RODZAJE[r]}]") for r in rodz for i, et, *_ in PYTANIA[r]] + [(f"warunki.{k}", v) for k, v in ETYKIETY_WARUNKOW.items()]
    lista = "\n".join(f"- {i}: {et}" for i, et in dict(pola).items())
    return ("Dokumenty powyżej dostarczył zamawiający (lista lub wykaz potrzeb, ogłoszenie o zamówieniu, SWZ z poprzedniego postępowania, notatka, wniosek, kosztorys). "
            "Odczytaj z nich główne założenia zamówienia i rozłóż je na pola kreatora:\n" + lista + "\n\n"
            "ZASADY: 1) Tylko to, co jest w dokumentach – nie zgaduj; brak = pomiń pole. 2) Ilości przepisuj DOKŁADNIE (liczby, jednostki), w polu ilości zbierz wszystkie pozycje. "
            "3) Przy każdym polu podaj źródło: plik i miejsce (punkt, §, strona, wiersz). 4) Jeśli dokument dotyczy wcześniejszego postępowania (np. stare ogłoszenie / SWZ), "
            "pola z datami, terminami, kwotami i znakiem sprawy oznacz do_aktualizacji = true. 5) Gdy dokumenty podają RÓŻNE wartości tego samego pola – nie wybieraj, "
            "wpisz pole do \"sprzecznosci\" z wariantami i źródłami. 6) Rodzaj zamówienia: roboty | uslugi | dostawy.\n"
            'Zwróć WYŁĄCZNIE JSON: {"rodzaj": "roboty | uslugi | dostawy | null", "archiwalny": true/false, "rodzaj_dokumentow": "…", '
            '"pola": {"id pola": {"wartosc": "…", "zrodlo": "plik – miejsce", "do_aktualizacji": false}}, '
            '"sprzecznosci": [{"pole": "id pola", "warianty": [{"wartosc": "…", "zrodlo": "…"}]}], "uwagi": ["…"]}')


# ---------------------------------------------------------------- kontrola bez AI: tryb i wartość odczytane wprost z tekstu dokumentów
NAZWY_TRYBU = {"ponizej_130": "poza Pzp (zapytanie ofertowe / regulamin)", "pzp_podstawowy": "tryb podstawowy (procedura krajowa)",
               "pzp_nieograniczony": "przetarg nieograniczony", "pzp_inny": "inny tryb Pzp (negocjacje, zamówienie z wolnej ręki…)"}
WARIANTY_275 = {"1": "bez negocjacji (art. 275 pkt 1)", "2": "z możliwością negocjacji (art. 275 pkt 2)", "3": "z obowiązkowymi negocjacjami (art. 275 pkt 3)"}
_WZORY_TRYBU = [
    ("pzp_nieograniczony", r"przetarg\w*\s+nieograniczon\w*|art\.?\s*132\b"),
    ("pzp_podstawowy", r"tryb\w*\s+podstawow\w*|art\.?\s*275\b"),
    ("pzp_inny", r"negocjac\w+\s+z\s+ogłoszeniem|dialog\w*\s+konkurencyjn\w*|z\s+wolnej\s+ręki|art\.?\s*(?:209|214|305)\b"),
    ("ponizej_130", r"zapytani\w*\s+ofertow\w*|nie\s+stosuje\s+się\s+(?:przepisów\s+)?ustawy|art\.?\s*2\s*ust\.?\s*1\s*pkt\s*1\b|zasad\w*\s+konkurencyjności"),
]


def tryb_z_tekstu(tekst):
    """Tryb wskazany w dokumentach (bez AI). Zwraca {"kod", "opis", "cytat", "liczby": {kod: ile}} albo None.
    Przy kilku różnych trybach w tekście – najczęstszy, a pozostałe w „inne” (do sprawdzenia)."""
    t = re.sub(r"\s+", " ", str(tekst or ""))
    liczby, cytaty = {}, {}
    for kod, wz in _WZORY_TRYBU:
        for m in re.finditer("(?i)" + wz, t):
            liczby[kod] = liczby.get(kod, 0) + 1
            cytaty.setdefault(kod, t[max(0, m.start() - 60):m.end() + 80].strip())
    if not liczby:
        return None
    # „art. 2 ust. 1 pkt 1” i „zasada konkurencyjności” pojawiają się też w SWZ Pzp (np. w odesłaniach) – liczą się tylko, gdy brak trybu Pzp
    kody = [k for k in liczby if k != "ponizej_130"] or ["ponizej_130"]
    kod = max(kody, key=lambda k: liczby[k])
    opis = NAZWY_TRYBU[kod]
    if kod == "pzp_podstawowy":
        w = re.search(r"(?i)art\.?\s*275\s*pkt\.?\s*([123])", t)
        if w:
            opis += " – " + WARIANTY_275[w.group(1)]
        elif re.search(r"(?i)bez\s+(przeprowadzenia\s+)?negocjacji", t):
            opis += " – bez negocjacji"
    return {"kod": kod, "opis": opis, "cytat": cytaty[kod][:240], "liczby": liczby, "inne": [k for k in kody if k != kod and liczby[k] >= 3]}


def _kwota(txt):
    t = re.sub(r"[\s\u00a0]", "", txt).replace(".", "").replace(",", ".") if re.search(r",\d{2}$", txt.strip()) else re.sub(r"[\s\u00a0.,]", "", txt)
    try:
        return float(t)
    except ValueError:
        return None


def wartosc_z_tekstu(tekst):
    """Wartość szacunkowa zamówienia podana wprost w dokumencie (bez AI) – lista {wartosc, netto: True/False/None, cytat}.
    Nie bierze „kwoty na sfinansowanie” (to zwykle brutto i inny parametr)."""
    t = re.sub(r"\s+", " ", str(tekst or ""))
    wyn = []
    for m in re.finditer(r"(?i)(szacunkow\w+\s+wartoś\w+|wartoś\w+\s+szacunkow\w+|wartoś\w+\s+zamówienia)[^.;:]{0,90}?(?:wynosi|:|–|-|to)?\s*(\d{1,3}(?:[ \u00a0.]\d{3})+(?:,\d{2})?|\d{4,9}(?:,\d{2})?)\s*(?:zł|PLN)", t):
        w = _kwota(m.group(2))
        if not w or w < 1000:
            continue
        okol = t[m.start():m.end() + 40].lower()
        netto = True if "netto" in okol or "bez vat" in okol or "bez podatku" in okol else False if "brutto" in okol else None
        if not any(abs(x["wartosc"] - w) < 0.5 for x in wyn):
            wyn.append({"wartosc": w, "netto": netto, "cytat": t[max(0, m.start() - 20):m.end() + 30].strip()[:240]})
    return wyn[:5]


def tekst_blokow(bloki):
    """Sam tekst z bloków przygotowanych do AI (PDF z warstwą tekstową, Word, Excel) – do kontroli bez AI."""
    cz = []
    for b in bloki or []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            cz.append(b.get("text") or "")
        src = b.get("source") or {}
        if src.get("type") == "text":
            cz.append(src.get("data") or "")
    return "\n".join(cz)


def porownaj_tryb(kod_dok, opis_dok, tryb_wyliczony, opis_wyliczony):
    """Różnica między trybem z dokumentów a trybem wynikającym z wartości – opis do decyzji (None = zgodne)."""
    if not kod_dok or kod_dok == tryb_wyliczony or tryb_wyliczony == "prywatny":
        return None
    if kod_dok == "pzp_nieograniczony" and tryb_wyliczony == "pzp_podstawowy":
        ocena = "dopuszczalne – poniżej progu unijnego zamawiający może wybrać przetarg nieograniczony zamiast trybu podstawowego; potwierdź, że to celowy wybór"
        waga = "informacja"
    elif kod_dok == "pzp_podstawowy" and tryb_wyliczony == "pzp_nieograniczony":
        ocena = "wartość jest na poziomie progu unijnego lub wyżej – tryb podstawowy nie jest dostępny; sprawdź wartość albo zmień tryb"
        waga = "krytyczna"
    elif kod_dok == "ponizej_130" and tryb_wyliczony.startswith("pzp"):
        ocena = "dokumenty przewidują postępowanie poza Pzp, a wartość jest od progu stosowania ustawy – sprawdź wartość (zakaz dzielenia zamówienia) albo prowadź postępowanie według Pzp"
        waga = "krytyczna"
    elif kod_dok.startswith("pzp") and tryb_wyliczony == "ponizej_130":
        ocena = "dokumenty przewidują tryb Pzp przy wartości poniżej progu – dopuszczalne (dobrowolne stosowanie ustawy), ale sprawdź, czy wartość jest właściwa"
        waga = "istotna"
    else:
        ocena = "tryby różnią się – sprawdź podstawę prawną"
        waga = "istotna"
    return {"dokumenty": opis_dok, "z_wartosci": opis_wyliczony, "ocena": ocena, "waga": waga}


# ---------------------------------------------------------------- raport uwag z kroku „Sprawdzenie i zmiany”
ZAKRESY_UWAG = {"wszystkie": "wszystkie uwagi", "przyjete": "uwagi przyjęte do wprowadzenia", "do_decyzji": "uwagi bez decyzji"}
OPIS_DECYZJI = {"tak": "PRZYJĘTA", "nie": "ODRZUCONA", "": "DO DECYZJI"}
KOLEJNOSC_WAG = {"krytyczna": 0, "istotna": 1, "drobna": 2}


def raport_uwag_docx(sciezka, nazwa, stan, zakres="wszystkie"):
    """Uwagi do sporządzonej dokumentacji (propozycje zmian z kroku 6) z decyzjami zamawiającego – do pobrania w Wordzie.
    Bez danych z profilu firmy (profil nie musi być stroną postępowania)."""
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor
    K = stan.get("K") or {}
    P = list(stan.get("propozycje") or [])
    if zakres == "przyjete":
        P = [p for p in P if p.get("decyzja") == "tak"]
    elif zakres == "do_decyzji":
        P = [p for p in P if not p.get("decyzja")]
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("UWAGI DO DOKUMENTACJI POSTĘPOWANIA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{nazwa or '[UZUPEŁNIJ: nazwa zamówienia]'}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"Sprawdzenie: {K.get('przeglad_data') or '–'} · zakres raportu: {ZAKRESY_UWAG.get(zakres, zakres)} · wygenerowano: "
      f"{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}", rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    wszystkie = stan.get("propozycje") or []
    ile = lambda f: sum(1 for p in wszystkie if f(p))
    A(f"Wszystkie uwagi: {len(wszystkie)} – krytyczne {ile(lambda p: p.get('waga') == 'krytyczna')}, istotne {ile(lambda p: p.get('waga') == 'istotna')}, "
      f"drobne {ile(lambda p: p.get('waga') not in ('krytyczna', 'istotna'))}. Decyzje: przyjęte {ile(lambda p: p.get('decyzja') == 'tak')}, "
      f"odrzucone {ile(lambda p: p.get('decyzja') == 'nie')}, bez decyzji {ile(lambda p: not p.get('decyzja'))}.", pogrub=True)
    if K.get("przeglad_podsumowanie"):
        A("Podsumowanie sprawdzenia", pogrub=True)
        A(K["przeglad_podsumowanie"])
    if not P:
        A("Brak uwag w wybranym zakresie.", kursywa=True)
    else:
        dok = {}
        for p in P:
            dok.setdefault(p.get("plik") or p.get("dokument") or "dokument", []).append(p)
        t = d.add_table(rows=1, cols=5)
        try:
            t.style = "Table Grid"
        except Exception:
            pass
        for c_, h in zip(t.rows[0].cells, ("Dokument", "Uwag", "Krytyczne / istotne", "Przyjęte", "Do ręcznego wprowadzenia")):
            c_.text = h
            for r in c_.paragraphs[0].runs:
                r.font.bold = True
                r.font.size = Pt(9)
        for nazwa_d, L in dok.items():
            w = t.add_row().cells
            for c_, v in zip(w, (nazwa_d, len(L), f"{sum(1 for x in L if x.get('waga') == 'krytyczna')} / {sum(1 for x in L if x.get('waga') == 'istotna')}",
                                 sum(1 for x in L if x.get("decyzja") == "tak"), sum(1 for x in L if not x.get("odnaleziony")))):
                c_.text = str(v)
                for r in c_.paragraphs[0].runs:
                    r.font.size = Pt(9)
        nr = 0
        for nazwa_d, L in dok.items():
            d.add_heading(nazwa_d, level=2)
            for p in sorted(L, key=lambda x: KOLEJNOSC_WAG.get(x.get("waga"), 3)):
                nr += 1
                waga = (p.get("waga") or "drobna").upper()
                h = d.add_heading(f"{nr}. [{waga}] {'Nowy zapis' if p.get('typ') == 'dopisanie' else 'Zmiana treści'} – {OPIS_DECYZJI.get(p.get('decyzja') or '', 'DO DECYZJI')}", level=3)
                kolor = {"KRYTYCZNA": RGBColor(0x99, 0x1B, 0x1B), "ISTOTNA": RGBColor(0xDC, 0x26, 0x26)}.get(waga)
                for run in h.runs:
                    if kolor:
                        run.font.color.rgb = kolor
                if p.get("typ") == "dopisanie":
                    A(f"Miejsce – po fragmencie: „{p.get('cytat', '')}”", kursywa=True, rozmiar=9)
                else:
                    A(f"Obecne brzmienie: „{p.get('cytat', '')}”", kursywa=True, rozmiar=9)
                nowy = p.get("nowy_edyt") if p.get("nowy_edyt") not in (None, "") else p.get("nowy", "")
                A(f"{'Proponowany zapis' if p.get('typ') == 'dopisanie' else 'Proponowane brzmienie'}{' (poprawione przez zamawiającego)' if p.get('nowy_edyt') not in (None, '', p.get('nowy')) else ''}: „{nowy}”", pogrub=True)
                if p.get("uzasadnienie"):
                    A(f"Uzasadnienie: {p['uzasadnienie']}")
                if p.get("podstawa"):
                    A(f"Podstawa: {p['podstawa']}", rozmiar=9)
                A("Wprowadzenie: " + ("program wprowadzi zmianę automatycznie (wersja Word ze śledzeniem zmian)" if p.get("odnaleziony")
                                      else "do ręcznego wprowadzenia – tekstu nie odnaleziono dokładnie w dokumencie"), rozmiar=8, kursywa=True)
    reczne = stan.get("reczne") or []
    if reczne and zakres != "do_decyzji":
        d.add_heading("Zmiany do ręcznego wprowadzenia (po ostatnim „Wprowadź zaakceptowane zmiany”)", level=2)
        for r in reczne:
            A(f"{r.get('dokument', '')}: „{(r.get('cytat') or '')[:300]}” → „{(r.get('nowy') or '')[:600]}” ({r.get('powod', '')})", rozmiar=9)
    A("Uwagi przygotowane z pomocą AI na podstawie treści dokumentów – wymagają oceny osoby odpowiedzialnej za przygotowanie postępowania. "
      "Decyzje (przyjęta / odrzucona) podjął zamawiający w programie.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
    return len(P)


# ---------------------------------------------------------------- jawny wybór trybu i komplet dokumentów według trybu
# baza – kategoria dla progów, terminów i warunków domyślnych (ponizej_130 / pzp_podstawowy / pzp_nieograniczony / pzp_inny / konkurencyjnosc)
TRYBY_WYBOR = {
    "podstawowy_1": ("Tryb podstawowy bez negocjacji (art. 275 pkt 1 Pzp)", "pzp_podstawowy"),
    "podstawowy_2": ("Tryb podstawowy z możliwością negocjacji (art. 275 pkt 2 Pzp)", "pzp_podstawowy"),
    "podstawowy_3": ("Tryb podstawowy z obowiązkowymi negocjacjami (art. 275 pkt 3 Pzp)", "pzp_podstawowy"),
    "przetarg_nieograniczony": ("Przetarg nieograniczony", "pzp_nieograniczony"),
    "przetarg_ograniczony": ("Przetarg ograniczony", "pzp_inny"),
    "negocjacje_z_ogloszeniem": ("Negocjacje z ogłoszeniem", "pzp_inny"),
    "dialog": ("Dialog konkurencyjny", "pzp_inny"),
    "partnerstwo": ("Partnerstwo innowacyjne", "pzp_inny"),
    "negocjacje_bez_ogloszenia": ("Negocjacje bez ogłoszenia", "pzp_inny"),
    "wolna_reka": ("Zamówienie z wolnej ręki", "pzp_inny"),
    "ponizej_progu": ("Zapytanie ofertowe – poniżej progu Pzp (regulamin zamawiającego)", "ponizej_130"),
    "zasada_konkurencyjnosci": ("Zapytanie ofertowe – zasada konkurencyjności (dofinansowanie UE)", "konkurencyjnosc"),
}
STANDARD = ["swz", "opz", "umowa", "formularz", "oswiadczenia"]
KOMPLET_TRYBU = {  # dokumenty właściwe dla trybu (poza standardem albo zamiast niego)
    "podstawowy_1": STANDARD,
    "podstawowy_2": STANDARD + ["zaproszenie_negocjacje", "zaproszenie_ostateczne", "protokol"],
    "podstawowy_3": STANDARD + ["zaproszenie_negocjacje", "zaproszenie_ostateczne", "protokol"],
    "przetarg_nieograniczony": STANDARD,
    "przetarg_ograniczony": ["ogloszenie", "wniosek_dopuszczenie", "zaproszenie_oferty"] + STANDARD + ["protokol"],
    "negocjacje_z_ogloszeniem": ["ogloszenie", "wniosek_dopuszczenie", "zaproszenie_oferty", "zaproszenie_negocjacje", "zaproszenie_ostateczne"] + STANDARD + ["protokol"],
    "dialog": ["ogloszenie", "wniosek_dopuszczenie", "zaproszenie_negocjacje", "zaproszenie_ostateczne"] + STANDARD + ["protokol"],
    "partnerstwo": ["ogloszenie", "wniosek_dopuszczenie", "zaproszenie_oferty", "zaproszenie_negocjacje", "zaproszenie_ostateczne"] + STANDARD + ["protokol"],
    "negocjacje_bez_ogloszenia": ["uzasadnienie_trybu", "zaproszenie_negocjacje", "opz", "umowa", "formularz", "oswiadczenia", "protokol"],
    "wolna_reka": ["uzasadnienie_trybu", "zaproszenie_negocjacje", "opz", "umowa", "protokol"],
    "ponizej_progu": ["swz", "opz", "umowa", "formularz", "protokol"],
    "zasada_konkurencyjnosci": ["swz", "opz", "umowa", "formularz", "oswiadczenia", "protokol"],
}
KOMPLET_Z_WARTOSCI = {"pzp_podstawowy": STANDARD, "pzp_nieograniczony": STANDARD, "ponizej_130": ["swz", "opz", "umowa", "formularz", "protokol"],
                      "prywatny": ["swz", "opz", "umowa", "formularz", "protokol"]}  # wspólnoty, spółdzielnie, deweloperzy – z protokołem wyboru oferty


def komplet_dokumentow(tryb_wybrany, tryb_z_wartosci):
    if tryb_wybrany in KOMPLET_TRYBU:
        return list(KOMPLET_TRYBU[tryb_wybrany])
    return list(KOMPLET_Z_WARTOSCI.get(tryb_z_wartosci, STANDARD))


def porownaj_wybor_trybu(wybrany, tryb_wartosc, opis_wartosc):
    """Tryb wybrany przez prawnika / zamawiającego a tryb wynikający z wartości – opis do decyzji albo None."""
    if wybrany not in TRYBY_WYBOR:
        return None
    nazwa, baza = TRYBY_WYBOR[wybrany]
    if baza == "pzp_inny":  # przetarg ograniczony, negocjacje, dialog, partnerstwo, wolna ręka – o dopuszczalności decydują przesłanki trybu
        if tryb_wartosc == "ponizej_130":
            return {"dokumenty": nazwa, "z_wartosci": opis_wartosc, "waga": "informacja",
                    "ocena": "wartość poniżej progu stosowania Pzp – procedura Pzp jest dobrowolna; sprawdź, czy to celowy wybór"}
        return {"dokumenty": nazwa, "z_wartosci": opis_wartosc, "waga": "informacja",
                "ocena": "tryb wybrany ręcznie – program nie ocenia jego przesłanek; uzasadnij je w dokumentacji (np. dokument „Uzasadnienie wyboru trybu”)"} \
            if wybrany in ("negocjacje_bez_ogloszenia", "wolna_reka", "dialog", "partnerstwo", "negocjacje_z_ogloszeniem") else None
    return porownaj_tryb(baza if baza != "konkurencyjnosc" else "ponizej_130", nazwa, tryb_wartosc, opis_wartosc)
