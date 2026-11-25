# -*- coding: utf-8 -*-
"""
Szacowanie wartości zamówienia (art. 28–36 Pzp) – podstawa ustalenia wartości zgodna z przepisami, nie kosztorys przygotowany przez AI.
- Roboty budowlane (art. 34 ust. 1 Pzp): kosztorys inwestorski sporządzony na etapie dokumentacji projektowej albo planowane koszty robót
  z programu funkcjonalno-użytkowego (PFU); przy „zaprojektuj i wybuduj” – planowane koszty prac projektowych i robót według PFU.
  Metody: rozporządzenie Ministra Rozwoju i Technologii z 20 grudnia 2021 r. (kosztorys inwestorski, planowane koszty, PFU).
  Dokument sporządza projektant albo kosztorysant – program go przyjmuje, odczytuje wartość i sprawdza; kosztorys przygotowany przez
  program nie jest podstawą wartości zamówienia zamawiającego publicznego.
- Dostawy i usługi: należyta staranność (art. 28) – udokumentowane rozeznanie rynku; zamówienia powtarzające się okresowo (art. 35).
- Termin (art. 36): nie wcześniej niż 3 miesiące (dostawy, usługi) albo 6 miesięcy (roboty) przed wszczęciem postępowania.
- Wynik: notatka z szacowania wartości zamówienia do dokumentacji postępowania.
"""
import datetime as dt
import re
import statistics
import uuid

import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

ROZPORZADZENIE = ("rozporządzenie Ministra Rozwoju i Technologii z dnia 20 grudnia 2021 r. w sprawie określenia metod i podstaw sporządzania "
                  "kosztorysu inwestorskiego, obliczania planowanych kosztów prac projektowych oraz planowanych kosztów robót budowlanych "
                  "określonych w programie funkcjonalno-użytkowym")
PODSTAWY = {
    "roboty": {
        "kosztorys_inwestorski": ("Kosztorys inwestorski (wykonanie robót według dokumentacji projektowej)", "art. 34 ust. 1 pkt 1 Pzp; " + ROZPORZADZENIE),
        "pfu_roboty": ("Planowane koszty robót budowlanych określone w programie funkcjonalno-użytkowym", "art. 34 ust. 1 pkt 1 Pzp; " + ROZPORZADZENIE),
        "pfu_zaprojektuj": ("Planowane koszty prac projektowych i planowane koszty robót budowlanych według PFU (zaprojektuj i wybuduj)",
                            "art. 34 ust. 1 pkt 2 Pzp; " + ROZPORZADZENIE)},
    "dostawy": {
        "rozeznanie": ("Rozeznanie rynku – udokumentowane źródła cen (należyta staranność)", "art. 28 Pzp"),
        "powtarzajace": ("Dostawy powtarzające się okresowo – wartość zamówień tego samego rodzaju z poprzednich 12 miesięcy / roku budżetowego "
                         "z uwzględnieniem zmian albo łączna wartość planowana na kolejne 12 miesięcy", "art. 35 ust. 1 Pzp")},
    "uslugi": {
        "rozeznanie": ("Rozeznanie rynku – udokumentowane źródła cen (należyta staranność)", "art. 28 Pzp"),
        "powtarzajace": ("Usługi powtarzające się okresowo – wartość zamówień tego samego rodzaju z poprzednich 12 miesięcy / roku budżetowego "
                         "z uwzględnieniem zmian albo łączna wartość planowana na kolejne 12 miesięcy", "art. 35 ust. 1 Pzp")}}
TYPY_ZRODEL = {"oferta_cenowa": "oferta cenowa / odpowiedź na zapytanie o cenę", "przetarg": "cena z rozstrzygniętego postępowania (BZP, TED)",
               "umowa": "wcześniejsza umowa zamawiającego", "kalkulacja": "kalkulacja kosztów (np. kosztów pracy)", "cennik": "cennik / katalog / publikacja",
               "konsultacje": "wstępne konsultacje rynkowe (art. 84 Pzp)", "inne": "inne źródło"}
METODY = {"srednia": "średnia ze źródeł", "mediana": "mediana ze źródeł", "wybrane": "wartość ze wskazanego źródła"}
ELEMENTY_KOSZTORYSU = {"strona tytułowa": r"(?i)kosztorys\s+inwestorski|nazwa\s+(obiektu|zamówienia)",
                       "ogólna charakterystyka obiektu": r"(?i)charakterystyk|opis\s+ogólny|ogólna\s+charakter",
                       "przedmiar robót": r"(?i)przedmiar",
                       "kalkulacja (ceny jednostkowe)": r"(?i)cen[aąy]\s+jednostkow|kalkulacj|KNR|KNNR",
                       "tabela wartości elementów scalonych": r"(?i)element[óoy]?\s+scalon|zestawienie\s+wartości|tabela\s+wartości",
                       "założenia / źródła cen": r"(?i)założen|źródł[oa]\s+cen|sekocenbud|intercenbud|analiz[ay]\s+własn"}


def _f(v):
    return liczba(v)


def zl(v):
    return f"{v:,.2f} zł".replace(",", " ").replace(".", ",")


def podstawy_dla(rodzaj):
    return PODSTAWY.get(rodzaj) or PODSTAWY["uslugi"]


def oczysc(sz, rodzaj):
    sz = dict(sz) if isinstance(sz, dict) else {}  # zapis złego typu (API, import) – jak puste szacowanie, bez błędu serwera
    P = podstawy_dla(rodzaj)
    sz["podstawa"] = sz.get("podstawa") if sz.get("podstawa") in P else ""
    d = sz.get("dokument") if isinstance(sz.get("dokument"), dict) else {}
    sz["dokument"] = {"plik": str(d.get("plik") or "")[:200], "wartosc": _f(d.get("wartosc")), "data": str(d.get("data") or "")[:10],
                      "autor": str(d.get("autor") or "")[:200], "elementy": d.get("elementy") if isinstance(d.get("elementy"), dict) else {}}
    zr = []
    for z in (sz.get("zrodla") if isinstance(sz.get("zrodla"), list) else []):
        if not isinstance(z, dict):
            continue
        zr.append({"id": z.get("id") or uuid.uuid4().hex[:8], "typ": z.get("typ") if z.get("typ") in TYPY_ZRODEL else "inne",
                   "opis": str(z.get("opis") or "")[:300], "data": str(z.get("data") or "")[:10], "wartosc": _f(z.get("wartosc")),
                   "plik": str(z.get("plik") or "")[:200], "pominiete": bool(z.get("pominiete"))})
    sz["zrodla"] = zr
    sz["metoda"] = sz.get("metoda") if sz.get("metoda") in METODY else "srednia"
    sz["zrodlo_wybrane"] = str(sz.get("zrodlo_wybrane") or "")
    k = sz.get("korekty") if isinstance(sz.get("korekty"), dict) else {}
    sz["korekty"] = {"opcje": _f(k.get("opcje")) or 0.0, "uzupelniajace": _f(k.get("uzupelniajace")) or 0.0, "inne": _f(k.get("inne")) or 0.0,
                     "opis": str(k.get("opis") or "")[:500]}
    sz["data_ustalenia"] = str(sz.get("data_ustalenia") or "")[:10]
    sz["osoba"] = str(sz.get("osoba") or "")[:200]
    sz["uwagi"] = str(sz.get("uwagi") or "")[:2000]
    return sz


def wylicz(sz, rodzaj, data_wszczecia=None):
    """Wartość netto z podstawy (dokument albo źródła) + korekty; ostrzeżenia zgodności z przepisami."""
    sz = oczysc(sz, rodzaj)
    ostrz = []
    baza = None
    szczeg = ""
    if not sz["podstawa"]:
        ostrz.append(("blad", "Wybierz podstawę ustalenia wartości zamówienia."))
    elif rodzaj == "roboty":
        d = sz["dokument"]
        baza = d["wartosc"]
        nazwa = "kosztorysu inwestorskiego" if sz["podstawa"] == "kosztorys_inwestorski" else "zestawienia planowanych kosztów (PFU)"
        if not d["plik"]:
            ostrz.append(("blad", f"Wgraj dokument {nazwa} sporządzony przez projektanta albo kosztorysanta – AI go nie sporządza."))
        if not baza:
            ostrz.append(("blad", f"Wpisz wartość netto z {nazwa}."))
        if not d["data"]:
            ostrz.append(("ostrzezenie", f"Wpisz datę sporządzenia {nazwa}."))
        if sz["podstawa"] == "kosztorys_inwestorski" and d["plik"] and d["elementy"]:
            brak = [k for k, v in d["elementy"].items() if not v]
            if brak:
                ostrz.append(("ostrzezenie", "W kosztorysie nie rozpoznano: " + ", ".join(brak) + " – sprawdź zgodność z rozporządzeniem."))
        szczeg = f"wartość z {nazwa}" + (f" z dnia {d['data']}" if d["data"] else "")
    else:
        L = [z for z in sz["zrodla"] if z["wartosc"] and not z["pominiete"]]
        if not L:
            ostrz.append(("blad", "Dodaj co najmniej jedno źródło ceny (oferta cenowa, rozstrzygnięty przetarg, wcześniejsza umowa, kalkulacja, cennik)."))
        else:
            w = [z["wartosc"] for z in L]
            if sz["metoda"] == "wybrane":
                z = next((z for z in L if z["id"] == sz["zrodlo_wybrane"]), None)
                baza = z["wartosc"] if z else None
                if not z:
                    ostrz.append(("blad", "Wskaż źródło, którego wartość przyjmujesz."))
            else:
                baza = round(statistics.median(w) if sz["metoda"] == "mediana" else sum(w) / len(w), 2)
            if sz["podstawa"] == "rozeznanie" and len(L) < 2:
                ostrz.append(("ostrzezenie", "Jedno źródło ceny – dla należytej staranności zaleca się co najmniej 2–3 niezależne źródła."))
            if len(w) >= 2 and min(w) > 0 and max(w) / min(w) > 2:
                ostrz.append(("ostrzezenie", f"Duży rozrzut cen ({zl(min(w))} – {zl(max(w))}) – sprawdź, czy źródła dotyczą tego samego zakresu; "
                                             "skrajne źródło możesz pominąć z uzasadnieniem."))
            szczeg = f"{METODY[sz['metoda']]} – uwzględnionych źródeł: {len(L)}"
    k = sz["korekty"]
    if k["opcje"] < 0 or k["uzupelniajace"] < 0:
        ostrz.append(("blad", "Korekty za opcje i zamówienia podobne nie mogą być ujemne – zwiększają wartość zamówienia (art. 31 Pzp)."))
    netto = round((baza or 0) + k["opcje"] + k["uzupelniajace"] + k["inne"], 2) if baza else None
    if netto is not None and netto <= 0:
        ostrz.append(("blad", "Po korektach wartość zamówienia nie jest dodatnia – popraw korekty."))
    # termin ustalenia wartości (art. 36)
    miesiace = 6 if rodzaj == "roboty" else 3
    du = sz["data_ustalenia"] or (sz["dokument"]["data"] if rodzaj == "roboty" else "")
    if not sz["data_ustalenia"]:
        ostrz.append(("ostrzezenie", "Wpisz datę ustalenia wartości zamówienia."))
    import kontrola_zam as _KO
    d1_ = _KO.data_iso(data_wszczecia)  # planowana data wszczęcia: RRRR-MM-DD albo DD.MM.RRRR
    if du and data_wszczecia and d1_:
        data_wszczecia = d1_.isoformat()
        try:
            d0, d1 = dt.date.fromisoformat(du), d1_
            granica = _KO.miesiace_wstecz(d1, miesiace)  # miesiące kalendarzowe: dzień przypadający dokładnie 3 / 6 miesięcy wcześniej jest poprawny
            if d0 > d1:
                ostrz.append(("blad", f"Data ustalenia wartości ({du}) jest późniejsza niż planowana data wszczęcia ({data_wszczecia})."))
            elif d0 < granica:
                ostrz.append(("blad", f"Wartość ustalona {du} – wcześniej niż {miesiace} miesięcy przed wszczęciem ({data_wszczecia}); "
                                      f"zaktualizuj szacowanie (art. 36 Pzp)."))
        except ValueError:
            pass
    elif du and _KO.data_iso(du):  # bez planowanej daty wszczęcia – aktualność sprawdzana względem dnia dzisiejszego (wszczęcie nie może być wcześniejsze)
        if _KO.data_iso(du) < _KO.miesiace_wstecz(dt.date.today(), miesiace):
            ostrz.append(("ostrzezenie", f"Wartość ustalona {du} – wcześniej niż {miesiace} miesięcy przed dniem dzisiejszym. Wpisz planowaną datę wszczęcia "
                                         f"postępowania; jeżeli nie zostało jeszcze wszczęte, zaktualizuj szacowanie (art. 36 Pzp)."))
        else:
            ostrz.append(("info", "Wpisz planowaną datę wszczęcia postępowania – bez niej program nie potwierdzi aktualności wartości (art. 36 Pzp)."))
    if du:
        try:
            if dt.date.fromisoformat(du) > dt.date.today():
                ostrz.append(("blad", f"Data ustalenia wartości ({du}) jest datą przyszłą."))
        except ValueError:
            pass
    if not sz["osoba"]:
        ostrz.append(("info", "Wpisz osobę, która ustaliła wartość (do notatki)."))
    return {"netto": netto, "baza": baza, "szczegoly": szczeg, "ostrzezenia": [{"waga": a, "opis": b} for a, b in ostrz],
            "kompletne": bool(netto) and not any(a == "blad" for a, _ in ostrz), "miesiace": miesiace}


def odczytaj_dokument(tekst):
    """Wartość netto i data z kosztorysu inwestorskiego / zestawienia PFU (tekst z pliku) oraz rozpoznane elementy kosztorysu."""
    t = re.sub(r"[ \t\u00a0]+", " ", tekst or "")
    wart = None
    for wz in (r"(?i)(?:wartość\s+kosztorysow\w*|razem\s+netto|ogółem\s+netto|wartość\s+netto|suma\s+netto|razem\s+wartość)[^\d]{0,60}"
               r"(\d{1,3}(?:[ .]\d{3})+(?:,\d{2})?|\d+(?:,\d{2})?)",
               r"(?i)netto[^\d]{0,30}(\d{1,3}(?:[ .]\d{3})+,\d{2})"):
        m = list(re.finditer(wz, t))
        if m:
            wart = _f(m[-1].group(1).replace(".", "").replace(" ", ""))
            break
    data = None
    m = re.search(r"(?i)(?:data\s+(?:opracowania|sporządzenia)|sporządzon\w*\s+dnia|opracowano)[^\d]{0,20}(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", t)
    if m:
        try:
            data = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
        except ValueError:
            data = None
    elementy = {k: bool(re.search(v, t)) for k, v in ELEMENTY_KOSZTORYSU.items()}
    autor = None  # „Sporządził: mgr inż. Jan Kowalski, upr. nr …” / „Kosztorysant: …”
    m = re.search(r"(?i)(?:sporządził\(?a?\)?|opracował\(?a?\)?|kosztorysant|autor\s+kosztorysu)\s*[:\-–]?\s*([^\n;,]{3,80})", t)
    if m and not re.match(r"(?i)\s*(dnia|data|\d)", m.group(1)):
        autor = m.group(1).strip(" .")
    return {"wartosc": wart, "data": data, "elementy": elementy, "autor": autor}


# ---------------------------------------------------------------- dokumenty
def notatka_docx(sciezka, sz, rodzaj, nazwa, zamawiajacy, data_wszczecia=None, centralny=False):
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    sz = oczysc(sz, rodzaj)
    w = wylicz(sz, rodzaj, data_wszczecia)
    netto = w["netto"] or 0
    tw = PR.tryb_wedlug_wartosci(netto, rodzaj, data_wszczecia or None, centralny)
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(zamawiajacy or "[nazwa zamawiającego]", pogrub=True)
    A("NOTATKA Z SZACOWANIA WARTOŚCI ZAMÓWIENIA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A("art. 28–36 ustawy z dnia 11 września 2019 r. – Prawo zamówień publicznych", kursywa=True, rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    pod = podstawy_dla(rodzaj).get(sz["podstawa"], ("nie wskazano", ""))
    W = [["Element", "Dane"], ["Przedmiot zamówienia", nazwa or ""],
         ["Rodzaj zamówienia", {"roboty": "roboty budowlane", "dostawy": "dostawy", "uslugi": "usługi"}.get(rodzaj, rodzaj)],
         ["Podstawa ustalenia wartości", pod[0]], ["Podstawa prawna", pod[1]],
         ["Data ustalenia wartości", sz["data_ustalenia"] or "[uzupełnij]"], ["Ustalił(a)", sz["osoba"] or "[uzupełnij]"]]
    if rodzaj == "roboty":
        dk = sz["dokument"]
        W += [["Dokument", dk["plik"] or "[brak – wgraj dokument]"], ["Sporządził", dk["autor"] or "[uzupełnij]"],
              ["Data sporządzenia dokumentu", dk["data"] or "[uzupełnij]"], ["Wartość netto z dokumentu", zl(dk["wartosc"]) if dk["wartosc"] else "[uzupełnij]"]]
    W += [["Wyliczenie", w["szczegoly"] or "–"]]
    k = sz["korekty"]
    if k["opcje"]:
        W.append(["Prawo opcji (największy możliwy zakres)", zl(k["opcje"])])
    if k["uzupelniajace"]:
        W.append(["Zamówienia, o których mowa w art. 214 ust. 1 pkt 7 i 8 Pzp", zl(k["uzupelniajace"])])
    if k["inne"]:
        W.append(["Inne składniki (opis niżej)", zl(k["inne"])])
    W += [["WARTOŚĆ ZAMÓWIENIA NETTO (bez VAT)", zl(netto) if netto else "[nie ustalono]"],
          ["Równowartość w euro", f"{PR.euro(tw['euro'])} (kurs {PR.kurs_pl(tw['kurs'])})"],
          ["Próg stosowania Pzp", zl(tw["prog_pzp"]) + " netto"], ["Próg unijny", f"{PR.euro(tw['prog_ue_eur'], 0)} = {PR.zl(tw['prog_ue_zl'])}"],
          ["Wniosek – tryb", tw["opis"]],
          ["Termin ważności ustalenia", f"nie wcześniej niż {w['miesiace']} miesięcy przed wszczęciem postępowania (art. 36 Pzp)"]]
    MO._tabela(d, W)
    if rodzaj != "roboty":
        A("Źródła cen", pogrub=True)
        Z = [["Lp.", "Rodzaj źródła", "Opis", "Data", "Wartość netto", "Uwzględnione"]]
        for i, z in enumerate(sz["zrodla"], 1):
            Z.append([str(i), TYPY_ZRODEL[z["typ"]], z["opis"] + (f" (plik: {z['plik']})" if z["plik"] else ""), z["data"],
                      zl(z["wartosc"]) if z["wartosc"] else "–", "nie (pominięte)" if z["pominiete"] else "tak"])
        if len(Z) == 1:
            Z.append(["", "", "brak źródeł", "", "", ""])
        MO._tabela(d, Z)
    if k["opis"] or sz["uwagi"]:
        A("Uzasadnienie i uwagi", pogrub=True)
        A("; ".join(x for x in (k["opis"], sz["uwagi"]) if x))
    A("Przy ustalaniu wartości uwzględniono łączną wartość zamówień tego samego rodzaju (zakaz dzielenia zamówienia – art. 29–30 Pzp). "
      "Kwota brutto służy wyłącznie zabezpieczeniu środków w budżecie.", kursywa=True, rozmiar=8)
    A("\n\nSporządził(a): .................................................          Zatwierdził(a): .................................................")
    MO.zapisz_z_zaznaczeniem(d, sciezka)
    return w


def zapytanie_o_cene_docx(sciezka, nazwa, rodzaj, opis, zamawiajacy, termin=""):
    """Zapytanie o cenę do szacowania wartości – rozeznanie rynku (to nie jest zapytanie ofertowe ani wszczęcie postępowania)."""
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(zamawiajacy or "[nazwa zamawiającego]", pogrub=True)
    A(f"[miejscowość], dnia {dt.date.today():%d.%m.%Y}", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("[nazwa i adres wykonawcy]")
    A("ZAPYTANIE O CENĘ – SZACOWANIE WARTOŚCI ZAMÓWIENIA", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"Zamawiający prowadzi rozeznanie rynku w celu oszacowania wartości zamówienia na {('dostawy' if rodzaj == 'dostawy' else 'usługi')}: "
      f"„{nazwa}”. Uprzejmie prosimy o podanie orientacyjnej ceny netto za cały zakres opisany poniżej.")
    A("Zakres:", pogrub=True)
    A(opis or "[opis przedmiotu, ilości, okres, miejsce realizacji, wymagania]")
    A(f"Prosimy o odpowiedź do dnia {termin or '[data]'} na adres: [e-mail zamawiającego]. W odpowiedzi prosimy podać cenę netto, stawkę VAT i datę ważności.")
    A("Zapytanie służy wyłącznie oszacowaniu wartości zamówienia (art. 28 Pzp). Nie stanowi zapytania ofertowego ani wszczęcia postępowania o udzielenie "
      "zamówienia i nie zobowiązuje zamawiającego do zawarcia umowy.", kursywa=True, rozmiar=9)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
