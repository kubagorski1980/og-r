# -*- coding: utf-8 -*-
"""
Roczne sprawozdanie o udzielonych zamówieniach (art. 82 Pzp) – przygotowanie danych do formularza na platformie e-Zamówienia.
Podstawa: rozporządzenie Ministra Rozwoju i Technologii z 20.12.2021 r. (Dz.U. poz. 2463); objaśnienia UZP „Zasady sporządzania
i przekazywania rocznego sprawozdania o udzielonych zamówieniach”. Termin: 1 marca roku następnego. Sekcje I–IX.
Program NIE wysyła sprawozdania – przygotowuje zestawienie sekcji, listę braków i arkusz do przepisania do formularza.
"""
import datetime as dt

import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

RODZAJE = {"roboty": "Roboty budowlane", "dostawy": "Dostawy", "uslugi": "Usługi"}
KATEGORIE = {"klasyczne": "Zamówienia klasyczne", "sektorowe": "Zamówienia sektorowe", "obronne": "Zamówienia w dziedzinach obronności i bezpieczeństwa"}
TRYBY = ["Tryb podstawowy bez negocjacji (art. 275 pkt 1)", "Tryb podstawowy z możliwością negocjacji (art. 275 pkt 2)",
         "Tryb podstawowy z obowiązkowymi negocjacjami (art. 275 pkt 3)", "Przetarg nieograniczony", "Przetarg ograniczony",
         "Negocjacje z ogłoszeniem", "Dialog konkurencyjny", "Partnerstwo innowacyjne", "Negocjacje bez ogłoszenia",
         "Zamówienie z wolnej ręki", "Inny"]
TRYB_Z_KREATORA = {"podstawowy_1": TRYBY[0], "podstawowy_2": TRYBY[1], "podstawowy_3": TRYBY[2], "przetarg_nieograniczony": TRYBY[3],
                   "przetarg_ograniczony": TRYBY[4], "negocjacje_z_ogloszeniem": TRYBY[5], "dialog": TRYBY[6], "partnerstwo": TRYBY[7],
                   "negocjacje_bez_ogloszenia": TRYBY[8], "wolna_reka": TRYBY[9]}
SPOLECZNE = {"zastrzezone_94": "zamówienie zastrzeżone (art. 94 ust. 1)", "dostepnosc_100": "dostępność dla osób niepełnosprawnych (art. 100 ust. 1)",
             "kryteria_spoleczne": "aspekty społeczne w kryteriach (art. 242 ust. 2)", "zatrudnienie_95": "zatrudnienie na umowę o pracę (art. 95 ust. 1)",
             "spoleczne_96": "wymagania społeczne związane z zatrudnieniem (art. 96 ust. 1)", "etykieta_spoleczna_104": "etykieta społeczna (art. 104)"}
SRODOWISKOWE = {"wymagania_101": "wymagania środowiskowe w opisie (art. 101)", "normy_116": "systemy lub normy zarządzania środowiskowego (art. 116 ust. 1)",
                "kryteria_srodowiskowe": "aspekty środowiskowe w kryteriach (art. 242 ust. 2)", "lcc_245": "rachunek kosztów cyklu życia (art. 245 ust. 1)",
                "srodowiskowe_96": "wymagania środowiskowe realizacji (art. 96 ust. 1)", "etykieta_srodowiskowa_104": "etykieta środowiskowa (art. 104)",
                "kryteria_innowacyjne": "aspekty innowacyjne w kryteriach (art. 242 ust. 2)", "innowacyjne_96": "wymagania innowacyjne realizacji (art. 96 ust. 1)"}
PROGI_UE_SEKT = {"roboty": 5404000, "dostawy": 432000, "uslugi": 432000}  # progi unijne 2026–2027 dla zamówień sektorowych i obronnych [EUR]
# progi sektorowe 432 000 € / 5 404 000 € potwierdzone 24.11.2026 w komunikacie UZP o progach 2026–2027 (dyrektywa 2014/25/UE art. 15)


def _f(v):
    return liczba(v)


def prog_ue_zl(p):
    rodzaj = p.get("rodzaj") or "dostawy"
    if p.get("kategoria") in ("sektorowe", "obronne"):
        return round(PROGI_UE_SEKT.get(rodzaj, 432000) * PR.KURS_EURO)
    return round(PR.PROGI_UE.get(rodzaj, 216000) * PR.KURS_EURO)


def sekcja(p):
    """Sekcja sprawozdania dla zamówienia (II, III, V, VIII, IX) – według wartości szacunkowej, kategorii i podstawy wyłączenia."""
    ws = _f(p.get("wartosc_szac")) if _f(p.get("wartosc_szac")) is not None else _f(p.get("wartosc_umowy")) or 0
    kat = p.get("kategoria") or "klasyczne"
    prog_kraj = PR.prog_pzp(p.get("data_wszczecia") or p.get("data_umowy"))
    ue = prog_ue_zl(p)
    if kat == "klasyczne" and ws < prog_kraj:
        return "IX"
    if kat in ("sektorowe", "obronne") and ws < ue:
        return "IX"
    if p.get("wylaczenie"):
        return "VIII"
    if p.get("usluga_spoleczna"):
        return "V"
    return "III" if ws >= ue else "II"


def braki(p, sek):
    """Pola, których formularz wymaga w danej sekcji, a których brak."""
    b = []
    if not p.get("data_umowy"):
        b.append("data zawarcia umowy")
    if _f(p.get("wartosc_umowy")) is None:
        b.append("wartość umowy netto")
    if sek in ("II", "III", "V") and not p.get("tryb"):
        b.append("tryb")
    if sek in ("III", "V"):
        for k, n in (("cpv", "główny kod CPV"), ("oferty", "liczba ofert"), ("oferty_msp", "liczba ofert MŚP")):
            if p.get(k) in (None, ""):
                b.append(n)
    if sek == "III":
        if p.get("odrzucone") in (None, ""):
            b.append("liczba odrzuconych ofert")
        if p.get("wybrany_msp") not in ("TAK", "NIE"):
            b.append("czy wybrany wykonawca to MŚP")
        if not p.get("kraj"):
            b.append("kraj wykonawcy")
        if not p.get("numer_ogloszenia"):
            b.append("numer ogłoszenia o udzieleniu zamówienia (TED)")
    if sek == "VIII" and not p.get("wylaczenie"):
        b.append("podstawa wyłączenia (artykuł Pzp)")
    return b


def zestawienie(pozycje, rok):
    """Zestawienie sekcji II–IX za rok (umowy zawarte od 1 stycznia do 31 grudnia), z brakami do uzupełnienia."""
    rok = int(rok)
    L = [p for p in pozycje or [] if str(p.get("data_umowy") or "")[:4] == str(rok) or not p.get("data_umowy")]
    wyn = {"rok": rok, "termin": f"{rok + 1}-03-01", "II": {}, "III": [], "IV": [], "V": [], "VI": [], "VII": [], "VIII": {}, "IX": {}, "braki": [], "pozycje": []}
    for p in L:
        s = sekcja(p)
        w = _f(p.get("wartosc_umowy")) or 0
        b = braki(p, s)
        q = dict(p, sekcja=s, braki=b)
        wyn["pozycje"].append(q)
        if b:
            wyn["braki"].append({"id": p.get("id"), "nazwa": p.get("nazwa"), "sekcja": s, "braki": b})
        if s == "II":
            k = (p.get("rodzaj") or "dostawy", p.get("tryb") or "(brak trybu)")
            r = wyn["II"].setdefault("|".join(k), {"rodzaj": k[0], "tryb": k[1], "liczba": 0, "wartosc": 0.0})
            r["liczba"] += 1
            r["wartosc"] += w
        elif s in ("III", "V"):
            wyn[s].append(q)
        elif s == "VIII":
            r = wyn["VIII"].setdefault(p.get("wylaczenie") or "(brak podstawy)", {"podstawa": p.get("wylaczenie") or "(brak podstawy)", "liczba": 0, "wartosc": 0.0})
            r["liczba"] += 1
            r["wartosc"] += w
        elif s == "IX":
            kat = p.get("kategoria") or "klasyczne"
            klucz = "klasyczne" if kat == "klasyczne" else f"{kat}_{p.get('rodzaj') or 'dostawy'}"
            wyn["IX"][klucz] = round(wyn["IX"].get(klucz, 0) + w, 2)
        if s in ("II", "III", "V"):
            if (p.get("konflikt") or 0) or (p.get("porozumienia") or 0):
                wyn["IV"].append(q)
            if any((p.get("spoleczne") or {}).get(k) for k in SPOLECZNE):
                wyn["VI"].append(q)
            if any((p.get("srodowiskowe") or {}).get(k) for k in SRODOWISKOWE):
                wyn["VII"].append(q)
    wyn["II"] = sorted(wyn["II"].values(), key=lambda r: (r["rodzaj"], r["tryb"]))
    wyn["VIII"] = list(wyn["VIII"].values())
    wyn["liczby"] = {s: (len(wyn[s]) if isinstance(wyn[s], list) else len(wyn[s])) for s in ("II", "III", "IV", "V", "VI", "VII", "VIII", "IX")}
    wyn["razem_netto"] = round(sum(_f(p.get("wartosc_umowy")) or 0 for p in L), 2)
    return wyn


def xlsx(sciezka, zamawiajacy, z):
    """Arkusz w układzie formularza (sekcje I–IX + braki): Arial, sumy formułami, żółte – do uzupełnienia."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    F, FB = Font(name="Arial", size=10), Font(name="Arial", size=10, bold=True)
    ZOLTY = PatternFill("solid", fgColor="FFF59D")
    NAG = PatternFill("solid", fgColor="E0F2F1")
    tn = lambda v: "TAK" if v is True else "NIE" if v is False else v

    def arkusz(nazwa, tytul, kolumny, wiersze, suma_kol=None):
        ws = wb.create_sheet(nazwa)
        ws.append([tytul])
        ws["A1"].font = Font(name="Arial", size=11, bold=True)
        ws.append([f"Rok sprawozdawczy: {z['rok']} · termin przekazania: {z['termin']} (platforma e-Zamówienia) · żółte komórki – do uzupełnienia"])
        ws["A2"].font = F
        ws.append(kolumny)
        for c in ws[3]:
            c.font, c.fill = FB, NAG
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for w in wiersze:
            ws.append([tn(x) for x in w])
            for c in ws[ws.max_row]:
                c.font = F
                if c.value in (None, ""):
                    c.fill = ZOLTY
        if suma_kol and wiersze:
            r = ws.max_row + 1
            ws.cell(r, 1, "RAZEM").font = FB
            for k in suma_kol:
                col = get_column_letter(k)
                ws.cell(r, k, f"=SUM({col}4:{col}{r - 1})").font = FB
        for i, _ in enumerate(kolumny, 1):
            ws.column_dimensions[get_column_letter(i)].width = 16 if i > 1 else 34
        return ws

    ws = wb.active
    ws.title = "I Zamawiający"
    ws.append(["Sekcja I – Zamawiający"])
    ws["A1"].font = Font(name="Arial", size=11, bold=True)
    for k, n in (("nazwa", "Nazwa zamawiającego"), ("adres", "Adres siedziby"), ("nip", "NIP"), ("regon", "REGON"), ("rodzaj", "Rodzaj zamawiającego (art. 4, 5, 6 Pzp)"),
                 ("www", "Strona internetowa"), ("email", "E-mail"), ("osoba", "Osoba do kontaktu")):
        ws.append([n, (zamawiajacy or {}).get(k) or ""])
        ws.cell(ws.max_row, 1).font = FB
        c = ws.cell(ws.max_row, 2)
        c.font = F
        if not c.value:
            c.fill = ZOLTY
    ws.append(["Czynność", "sprawozdanie (nie korekta)"])
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 40, 60
    arkusz("II", "Sekcja II – zamówienia klasyczne poniżej progów unijnych (bez usług społecznych)", ["Rodzaj zamówienia", "Tryb", "Liczba postępowań", "Wartość umów netto [zł]"],
           [[RODZAJE.get(r["rodzaj"], r["rodzaj"]), r["tryb"], r["liczba"], round(r["wartosc"], 2)] for r in z["II"]], [3, 4])
    kol3 = ["Nazwa", "Nr ogłoszenia o udzieleniu (TED)", "Rodzaj", "CPV", "Tryb", "Kraj wykonawcy", "Wartość umowy netto [zł]", "Liczba części",
            "Liczba ofert", "Odrzucone", "Oferty MŚP", "Wybrany MŚP", "Kategoria"]
    arkusz("III", "Sekcja III – zamówienia od progów unijnych (bez usług społecznych)", kol3,
           [[p.get("nazwa"), p.get("numer_ogloszenia"), RODZAJE.get(p.get("rodzaj"), p.get("rodzaj")), p.get("cpv"), p.get("tryb"), p.get("kraj"),
             _f(p.get("wartosc_umowy")), p.get("czesci"), p.get("oferty"), p.get("odrzucone"), p.get("oferty_msp"), p.get("wybrany_msp"),
             KATEGORIE.get(p.get("kategoria") or "klasyczne")] for p in z["III"]], [7])
    arkusz("IV", "Sekcja IV – konflikt interesów (art. 56 ust. 2) i porozumienia zakłócające konkurencję (art. 108 ust. 1 pkt 5)",
           ["Nazwa", "Nr ogłoszenia", "Rodzaj", "CPV", "Tryb", "Przypadki konfliktu interesów", "Wykryte porozumienia", "Oferty odrzucone (art. 108 ust. 1 pkt 5)"],
           [[p.get("nazwa"), p.get("numer_ogloszenia"), RODZAJE.get(p.get("rodzaj")), p.get("cpv"), p.get("tryb"), p.get("konflikt") or 0, p.get("porozumienia") or 0,
             p.get("odrzucone_porozumienia") or 0] for p in z["IV"]])
    arkusz("V", "Sekcja V – usługi społeczne i inne szczególne usługi (art. 359, art. 392 ust. 1)",
           ["Nazwa", "Nr ogłoszenia", "Opis usługi (zał. XIV dyrektywy)", "CPV", "Tryb", "Zastrzeżone (art. 361 ust. 1 / 392 ust. 3)", "Wartość umowy netto [zł]",
            "Liczba części", "Liczba ofert", "Oferty MŚP"],
           [[p.get("nazwa"), p.get("numer_ogloszenia"), p.get("opis_uslugi"), p.get("cpv"), p.get("tryb"), p.get("zastrzezone_361"), _f(p.get("wartosc_umowy")),
             p.get("czesci"), p.get("oferty"), p.get("oferty_msp")] for p in z["V"]], [7])
    arkusz("VI", "Sekcja VI – aspekty społeczne", ["Nazwa", "Nr ogłoszenia", "Rodzaj", "CPV", "Tryb", "Wartość umowy netto [zł]", "Liczba ofert"] + list(SPOLECZNE.values()),
           [[p.get("nazwa"), p.get("numer_ogloszenia"), RODZAJE.get(p.get("rodzaj")), p.get("cpv"), p.get("tryb"), _f(p.get("wartosc_umowy")), p.get("oferty")]
            + [bool((p.get("spoleczne") or {}).get(k)) for k in SPOLECZNE] for p in z["VI"]], [6])
    arkusz("VII", "Sekcja VII – aspekty środowiskowe lub innowacyjne", ["Nazwa", "Nr ogłoszenia", "Rodzaj", "CPV", "Tryb", "Wartość umowy netto [zł]"] + list(SRODOWISKOWE.values()),
           [[p.get("nazwa"), p.get("numer_ogloszenia"), RODZAJE.get(p.get("rodzaj")), p.get("cpv"), p.get("tryb"), _f(p.get("wartosc_umowy"))]
            + [bool((p.get("srodowiskowe") or {}).get(k)) for k in SRODOWISKOWE] for p in z["VII"]], [6])
    arkusz("VIII", "Sekcja VIII – zamówienia udzielone z wyłączeniem stosowania ustawy (podstawy z Pzp)", ["Podstawa wyłączenia (artykuł Pzp)", "Liczba zamówień", "Wartość netto [zł]"],
           [[r["podstawa"], r["liczba"], round(r["wartosc"], 2)] for r in z["VIII"]], [2, 3])
    prog = PR.prog_pzp(f"{z['rok']}-06-30")
    ix = z["IX"]
    arkusz("IX", f"Sekcja IX – zamówienia klasyczne poniżej {prog:,} zł oraz sektorowe i obronne poniżej progów unijnych".replace(",", " "), ["Wiersz", "Wartość netto [zł]"],
           [[f"1. Klasyczne poniżej {prog:,} zł".replace(",", " "), ix.get("klasyczne", 0)],
            ["2. Sektorowe – roboty budowlane", ix.get("sektorowe_roboty", 0)], ["3. Sektorowe – dostawy", ix.get("sektorowe_dostawy", 0)],
            ["4. Sektorowe – usługi", ix.get("sektorowe_uslugi", 0)], ["5. Obronność i bezpieczeństwo – roboty budowlane", ix.get("obronne_roboty", 0)],
            ["6. Obronność i bezpieczeństwo – dostawy", ix.get("obronne_dostawy", 0)], ["7. Obronność i bezpieczeństwo – usługi", ix.get("obronne_uslugi", 0)]], [2])
    arkusz("Braki", "Braki do uzupełnienia przed przekazaniem", ["Zamówienie", "Sekcja", "Brakuje"],
           [[b["nazwa"], b["sekcja"], ", ".join(b["braki"])] for b in z["braki"]])
    wb.save(sciezka)


def z_projektu(m, real, rok, wartosc_szac=None, ocena=None):
    """Pozycja sprawozdania z projektu zamawiającego (kreator, realizacja, badanie ofert) – to, co program wie; resztę uzupełnia użytkownik.
    wartosc_szac – wartość zamówienia netto z szacowania (ta sama co w kreatorze; nigdy „orientacyjny budżet”), ocena – powiązana ocena ofert."""
    K = m.get("kreator") or {}
    O = [o for o in ((ocena if ocena is not None else m.get("ocena")) or {}).get("oferty") or [] if isinstance(o, dict)]
    data = str(real.get("data_umowy") or "")[:10]
    if not data.startswith(str(rok)):
        return None
    p = {"id": f"projekt:{m.get('id')}", "zrodlo": "projekt", "projekt_id": m.get("id"), "nazwa": m.get("nazwa") or "",
         "rodzaj": K.get("rodzaj") or m.get("rodzaj_zamowienia") or "", "tryb": TRYB_Z_KREATORA.get(K.get("tryb_wybrany") or "", ""),
         "kategoria": "klasyczne", "wartosc_szac": _f(wartosc_szac) or None, "wartosc_umowy": _f(real.get("wartosc_netto")) or None,
         "data_umowy": data, "kraj": "PL", "cpv": K.get("cpv") or ""}
    if O:
        p["oferty"] = len(O)
        p["odrzucone"] = sum(1 for o in O if o.get("odrzucona") or o.get("status") == "odrzucona" or (o.get("wynik") or {}).get("status") == "do odrzucenia")
    return p
