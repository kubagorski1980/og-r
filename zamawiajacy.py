# -*- coding: utf-8 -*-
"""
Moduły dla ZAMAWIAJĄCEGO (inwestora):
 - weryfikacja dokumentacji przetargowej – wyszukiwanie błędów, sprzeczności i braków z propozycjami poprawek,
 - sporządzanie dokumentacji przetargowej (SWZ / zapytanie ofertowe, OPZ, formularz ofertowy, wzór umowy)
   na podstawie wymagań zamawiającego i załączonych dokumentów (projekt, przedmiar, kosztorys inwestorski).
Wyniki są projektami dokumentów – wymagają sprawdzenia przez osobę odpowiedzialną za zamówienie.
"""
import datetime as dt
import hashlib
import re

import modul_oferty as MO
import progi as _PR

# ============================================================ weryfikacja

SYSTEM_WER = (_PR.INFO_AI + " " + "Jesteś doświadczonym specjalistą ds. zamówień publicznych i inżynierem kosztorysantem w Polsce. Sprawdzasz "
              "dokumentację postępowania (roboty budowlane, usługi albo dostawy) przed jej publikacją: szukasz błędów, sprzeczności między dokumentami, "
              "braków, niejasności, zapisów ryzykownych lub niezgodnych z ustawą Prawo zamówień publicznych (Pzp) i zasadą "
              "konkurencyjności. Wskazujesz konkretne miejsca i proponujesz brzmienie poprawki. Nie zmyślasz problemów. "
              "Odpowiadasz WYŁĄCZNIE JSON-em.")

POLECENIE_WER = """Sprawdź dokumentację przetargową (powyżej) pod kątem:
1. SPRZECZNOŚCI między dokumentami (np. różne terminy realizacji w SWZ i wzorze umowy, różna wysokość wadium, inny zakres w OPZ i przedmiarze,
   różne okresy gwarancji, różne kryteria/wagi).
2. BŁĘDÓW (rachunkowe w przedmiarze/kosztorysie, błędne odwołania do punktów, błędne daty, jednostki, ilości niezgodne z rysunkami).
3. BRAKÓW (brak obowiązkowych elementów SWZ lub zapytania, brak kryteriów i sposobu oceny, brak opisu sposobu obliczenia ceny,
   brak terminu związania ofertą, brak klauzul waloryzacyjnych, gdy są wymagane, brak wymaganych załączników, pozycje robót bez przedmiaru).
4. NIEZGODNOŚCI Z PRAWEM I RYZYK (nieproporcjonalne warunki udziału, kary umowne bez limitu, nazwy producentów bez „lub równoważne”,
   niejednoznaczne zapisy, ryzyka dla zamawiającego).
{dodatkowe}
Zwróć JSON:
{{"podsumowanie": "3–5 zdań: ogólna ocena dokumentacji i najważniejsze problemy",
  "ocena": "gotowa do publikacji | wymaga poprawek | wymaga istotnych poprawek",
  "uwagi": [{{"waga": "krytyczna | istotna | drobna",
             "kategoria": "sprzeczność | błąd | brak | niezgodność z przepisami | ryzyko | niejasność",
             "dokument": "nazwa pliku (i drugi plik przy sprzeczności)", "miejsce": "rozdział / punkt / paragraf / strona / pozycja",
             "cytat": "DOSŁOWNY fragment z dokumentu, skopiowany znak w znak (20–300 znaków) – program sprawdza go w pliku; albo pusty", "opis": "na czym polega problem",
             "propozycja": "konkretna zmiana – najlepiej proponowane brzmienie zapisu",
             "nowy_tekst": "GOTOWE nowe brzmienie, które ma ZASTĄPIĆ cytat (ten sam zakres co cytat, gotowe do wklejenia) – albo pusty, gdy zmiana wymaga decyzji / dopisania w innym miejscu"}}]}}
Najważniejsze uwagi najpierw. Maksymalnie 40 uwag."""


RODZAJE_ZAM = {
    "roboty": {"nazwa": "Roboty budowlane", "krotko": "budowa, przebudowa, remont, termomodernizacja, drogi, sieci",
               "wartosc": "Kosztorys inwestorski", "cpv": "45000000-7 (roboty budowlane)"},
    "uslugi": {"nazwa": "Usługi", "krotko": "sprzątanie, ochrona, utrzymanie zieleni i dróg, odśnieżanie, projektowanie, nadzór, transport, IT",
               "wartosc": "Szacowanie wartości usług", "cpv": "działy 50–98 (usługi), np. 90910000-9 sprzątanie, 71000000-8 usługi projektowe"},
    "dostawy": {"nazwa": "Dostawy (towary)", "krotko": "sprzęt, wyposażenie, meble, komputery, materiały, paliwo, energia, żywność",
                "wartosc": "Szacowanie wartości dostaw (formularz cenowy)", "cpv": "działy 03–44 (dostawy), np. 30200000-1 komputery, 39100000-3 meble"},
}

WER_RODZAJ = {
    "roboty": "Zamówienie na ROBOTY BUDOWLANE: sprawdź zgodność przedmiaru z projektem i STWiORB, spójność zakresu robót w SWZ, OPZ, przedmiarze "
              "i wzorze umowy, wymagania wobec kierownika budowy, odbiory częściowe i końcowy, gwarancję i rękojmię, podwykonawstwo (art. 462–465 Pzp).",
    "uslugi": "Zamówienie na USŁUGI: sprawdź, czy OPZ jednoznacznie określa zakres, częstotliwość, standard i miejsca świadczenia usług, "
              "sposób odbioru (np. miesięczne protokoły), wymagania zatrudnienia na umowę o pracę (art. 95 Pzp), waloryzację przy umowie "
              "dłuższej niż 6 miesięcy (art. 439 Pzp), kwalifikacje personelu, kary i sposób rozliczania (ryczałt miesięczny / stawki).",
    "dostawy": "Zamówienie na DOSTAWY: sprawdź opis przedmiotu – parametry minimalne zamiast nazw i znaków towarowych (albo z dopiskiem „lub równoważne” "
               "i kryteriami równoważności), zgodność formularza asortymentowo-cenowego z OPZ (pozycje, ilości, jednostki), miejsce i termin dostawy, "
               "rozładunek i montaż, gwarancję i serwis, wymagane certyfikaty i deklaracje, prawo opcji (art. 441 Pzp).",
}


SYSTEM_WER_WYK = (_PR.INFO_AI + " " + "Jesteś doświadczonym doradcą wykonawców i dostawców w zamówieniach publicznych w Polsce (kosztorysant i specjalista Pzp). "
                  "Czytasz dokumentację przetargową OCZAMI WYKONAWCY: szukasz błędów, sprzeczności, braków i niejasności, które zagrażają "
                  "wykonawcy (koszty, termin, kary, ryzyko odrzucenia oferty) albo dają mu podstawę do pytań, robót dodatkowych lub "
                  "zamiennych, zmiany terminu i wynagrodzenia. Radzisz WYKONAWCY, co ma zrobić – NIE piszesz, jak zamawiający ma poprawić "
                  "dokumenty. Nie zmyślasz problemów. Odpowiadasz WYŁĄCZNIE JSON-em.")

POLECENIE_WER_WYK = """Sprawdź dokumentację przetargową (powyżej) z perspektywy WYKONAWCY / DOSTAWCY{etap}:
1. SPRZECZNOŚCI między dokumentami (terminy, zakres w SWZ/OPZ/przedmiarze/umowie, ilości, gwarancja, wadium, kryteria).
2. BŁĘDY i BRAKI w przedmiarze / opisie (brakujące pozycje, zaniżone ilości, roboty widoczne w projekcie, a nieujęte w przedmiarze).
3. RYZYKA DLA WYKONAWCY (kary bez limitu, ryczałt przy niepełnej dokumentacji, nierealny termin, ukryte koszty, wymagania trudne do spełnienia).
4. NIEJASNOŚCI, które trzeba wyjaśnić, zanim policzy się cenę.
{dodatkowe}
Zwróć JSON:
{{"podsumowanie": "3–5 zdań: najważniejsze zagrożenia i szanse dla wykonawcy",
  "ocena": "dokumentacja bez większych ryzyk | wymaga pytań do zamawiającego | duże ryzyko dla wykonawcy",
  "uwagi": [{{"waga": "krytyczna | istotna | drobna",
             "kategoria": "sprzeczność | błąd | brak | ryzyko | niejasność | niezgodność z przepisami",
             "dokument": "nazwa pliku (i drugi plik przy sprzeczności)", "miejsce": "rozdział / punkt / paragraf / strona / pozycja",
             "cytat": "DOSŁOWNY fragment z dokumentu, skopiowany znak w znak (20–300 znaków) – program sprawdza go w pliku; albo pusty",
             "opis": "na czym polega problem i jaki ma skutek dla wykonawcy (koszt, termin, ryzyko)",
             "propozycja": "CO MA ZROBIĆ WYKONAWCA – konkretnie: {co_zrobic}",
             "pytanie_do_zamawiajacego": "gotowa treść {pytanie_podstawa}; pusty, jeśli zbędne"}}]}}
Najważniejsze uwagi najpierw. Maksymalnie 40 uwag."""

CO_ZROBIC = {
    "oferta": "zadać pytanie do zamawiającego przed terminem, przyjąć i opisać założenie w ofercie, ująć ryzyko w cenie, sprawdzić na wizji lokalnej, "
              "dołączyć wymagany dokument",
    "realizacja": "zgłosić na piśmie zamawiającemu / inspektorowi i wpisać do dziennika budowy, wstrzymać dany zakres do wyjaśnienia, przygotować "
                  "protokół konieczności i wniosek o roboty dodatkowe lub zamienne, wniosek o przedłużenie terminu i zmianę wynagrodzenia "
                  "(z podstawą w umowie lub art. 455 Pzp), zgromadzić dowody (zdjęcia, obmiary)",
}


PYTANIE_PODSTAWA = {  # podstawa wniosku o wyjaśnienie treści SWZ według trybu (rodzaj z trasy_projekty_wykonawcy.podpis_oferty)
    "unijne": "wniosku o wyjaśnienie treści SWZ (art. 135 Pzp – procedura unijna)",
    "krajowe": "wniosku o wyjaśnienie treści SWZ (art. 284 Pzp – tryb podstawowy)",
    "poza": "pytania do zamawiającego w trybie wskazanym w zapytaniu ofertowym (zamówienie poza Pzp – bez powoływania Pzp)",
    "nieznane": "wniosku o wyjaśnienie treści SWZ (tryb podstawowy – art. 284 Pzp; procedura unijna – art. 135 Pzp; ustal tryb z SWZ / ogłoszenia)",
}


def polecenie_weryfikacji_wykonawcy(dodatkowe="", rodzaj_zam="roboty", etap="oferta", rodzaj_postepowania="nieznane"):
    dod = (f"5. Dodatkowo zwróć uwagę na: {dodatkowe}\n" if dodatkowe.strip() else "")
    et = " w trakcie REALIZACJI UMOWY (umowa jest już zawarta)" if etap == "realizacja" else " PRZED ZŁOŻENIEM OFERTY"
    pp = ("pisma do zamawiającego / inspektora nadzoru" if etap == "realizacja" else
          PYTANIE_PODSTAWA.get(rodzaj_postepowania, PYTANIE_PODSTAWA["nieznane"]))
    return POLECENIE_WER_WYK.format(etap=et, dodatkowe=dod, co_zrobic=CO_ZROBIC.get(etap, CO_ZROBIC["oferta"]), pytanie_podstawa=pp)


def polecenie_weryfikacji(dodatkowe="", rodzaj_zam="roboty", lista=""):
    """lista – lista kontrolna trybu i reżimu (lista_kontroli.lista_weryfikacji): ta sama co w kreatorze i u prawnika."""
    dod = WER_RODZAJ.get(rodzaj_zam, WER_RODZAJ["roboty"]) + (f" Dodatkowo zwróć uwagę na: {dodatkowe}" if dodatkowe.strip() else "")
    lk = (f"6. Zgodność z LISTĄ KONTROLNĄ (każda niespełniona pozycja = uwaga; gdy wymogi trybu stanowią inaczej niż punkty 1–4 – "
          f"stosuj wymogi trybu):\n{lista}\n") if lista else ""
    return POLECENIE_WER.format(dodatkowe=f"5. {dod}\n{lk}")


def wynik_weryfikacji(tekst):
    d = MO.wyciagnij_json(tekst)
    uwagi = []
    for u in d.get("uwagi", []):
        if not isinstance(u, dict) or not u.get("opis"):
            continue
        waga = str(u.get("waga", "istotna")).lower()
        waga = waga if waga in ("krytyczna", "istotna", "drobna") else "istotna"
        uwagi.append({"id": hashlib.sha1((str(u.get("opis")) + str(u.get("miejsce"))).encode()).hexdigest()[:10], "waga": waga,
                      **{k: str(u.get(k) or "")[:1500] for k in ("kategoria", "dokument", "miejsce", "cytat", "opis", "propozycja", "pytanie_do_zamawiajacego", "nowy_tekst", "podstawa")},
                      "status": "do poprawy"})
    kol = {"krytyczna": 0, "istotna": 1, "drobna": 2}
    uwagi.sort(key=lambda u: kol[u["waga"]])
    return {"podsumowanie": str(d.get("podsumowanie", ""))[:2000], "ocena": str(d.get("ocena", ""))[:80], "uwagi": uwagi,
            "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}


def raport_weryfikacji_docx(sciezka, nazwa, w, cfg):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("RAPORT Z WERYFIKACJI DOKUMENTACJI PRZETARGOWEJ", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{nazwa} · {w.get('data', '')}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER, rozmiar=9)  # bez danych z profilu – profil nie musi być stroną postępowania
    A(f"Ocena: {w.get('ocena', '')}", pogrub=True)
    A(w.get("podsumowanie", ""))
    liczby = {k: sum(1 for u in w["uwagi"] if u["waga"] == k) for k in ("krytyczna", "istotna", "drobna")}
    A(f"Uwagi: krytyczne {liczby['krytyczna']}, istotne {liczby['istotna']}, drobne {liczby['drobna']}.")
    for i, u in enumerate(w["uwagi"], 1):
        h = d.add_heading(f"{i}. [{u['waga'].upper()}] {u['kategoria']} – {u['dokument']}", level=3)
        from docx.shared import RGBColor
        kolor = {"krytyczna": RGBColor(0x99, 0x1B, 0x1B), "istotna": RGBColor(0xDC, 0x26, 0x26)}.get(u["waga"])
        for run in h.runs:  # krytyczne i istotne – na czerwono
            if kolor:
                run.font.color.rgb = kolor
        if u.get("miejsce"):
            A(f"Miejsce: {u['miejsce']}", rozmiar=9)
        if u.get("cytat"):
            A(f"„{u['cytat']}”", kursywa=True, rozmiar=9)
        A(f"Problem: {u['opis']}")
        wyk = w.get("perspektywa") == "wykonawca"
        if u.get("propozycja"):
            A(f"{'Co zrobić' if wyk else 'Propozycja'}: {u['propozycja']}", pogrub=True)
        if u.get("podstawa"):
            A(f"Podstawa prawna: {u['podstawa']}", kursywa=True, rozmiar=9)
        if wyk and u.get("pytanie_do_zamawiajacego"):
            A(f"Pytanie do zamawiającego: {u['pytanie_do_zamawiajacego']}", kursywa=True)
        A(f"Status: {u.get('status', '')}", rozmiar=8, kursywa=True)
    A("Raport przygotowany z pomocą AI – wymaga oceny " + ("wykonawcy przed złożeniem oferty lub wniosku." if w.get("perspektywa") == "wykonawca"
      else "osoby odpowiedzialnej za przygotowanie postępowania."), kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# ============================================================ sporządzanie dokumentacji

TRYBY_POST = {
    "pzp_podstawowy": "Specyfikacja Warunków Zamówienia (SWZ) – tryb podstawowy bez negocjacji (art. 275 pkt 1 ustawy Pzp)",
    "konkurencyjnosc": "Zapytanie ofertowe – zasada konkurencyjności (Baza Konkurencyjności, projekty unijne)",
    "ponizej_130": "Zapytanie ofertowe – zamówienie o wartości poniżej progu stosowania Pzp (od 1.01.2026: 170 000 zł netto; poza Pzp, regulamin zamawiającego)",
    "prywatny": "Zapytanie ofertowe inwestora prywatnego / wspólnoty mieszkaniowej",
    "pzp_nieograniczony": "Specyfikacja Warunków Zamówienia (SWZ) – przetarg nieograniczony, procedura unijna (art. 132 ustawy Pzp)",
}
DOKUMENTY = {
    "swz": ("SWZ lub zapytanie ofertowe", "SWZ"),
    "opz": ("Opis przedmiotu zamówienia (OPZ)", "OPZ"),
    "formularz": ("Formularz ofertowy z oświadczeniami", "Formularz_ofertowy"),
    "umowa": ("Projektowane postanowienia umowy (wzór umowy)", "Wzor_umowy"),
    "oswiadczenia": ("Oświadczenia wykonawcy i wykazy (art. 125, wykaz robót / usług / dostaw, wykaz osób)", "Oswiadczenia_i_wykazy"),
    # dokumenty właściwe dla trybu (komplet według trybu – kreator_zam.KOMPLET_TRYBU)
    "ogloszenie": ("Ogłoszenie o zamówieniu (treść do publikacji)", "Ogloszenie"),
    "wniosek_dopuszczenie": ("Wzór wniosku o dopuszczenie do udziału w postępowaniu", "Wniosek_o_dopuszczenie"),
    "zaproszenie_oferty": ("Zaproszenie do składania ofert (dla wykonawców zakwalifikowanych)", "Zaproszenie_do_ofert"),
    "zaproszenie_negocjacje": ("Zaproszenie do negocjacji", "Zaproszenie_do_negocjacji"),
    "zaproszenie_ostateczne": ("Zaproszenie do składania ofert ostatecznych", "Zaproszenie_do_ofert_ostatecznych"),
    "protokol": ("Protokół postępowania", "Protokol_postepowania"),
    "uzasadnienie_trybu": ("Uzasadnienie wyboru trybu (spełnienie przesłanek)", "Uzasadnienie_trybu"),
}

SYSTEM_DOK = ("Jesteś doświadczonym specjalistą ds. zamówień publicznych (roboty budowlane, usługi i dostawy) w Polsce. Przygotowujesz kompletne, "
              "spójne i zgodne z przepisami dokumenty postępowania dla zamawiającego – po polsku, językiem urzędowym, z numeracją "
              "rozdziałów i punktów. Nie wymyślasz danych, których nie podano – zostawiasz [UZUPEŁNIJ: …]. Odpowiadasz WYŁĄCZNIE JSON-em.")


ZAKRES_RODZAJU = {
    "uslugi": {
        "opz": ("Przygotuj opis przedmiotu zamówienia na USŁUGI: zakres i rodzaj czynności, miejsca/obiekty i ich parametry (powierzchnie, ilości), "
                "częstotliwość i harmonogram świadczenia, standard i mierniki jakości, wymagany personel i sprzęt, obowiązki wykonawcy, "
                "sposób zgłaszania i odbioru usług (np. miesięczne protokoły), wymagania zatrudnienia na umowę o pracę (art. 95 Pzp), "
                "aspekty społeczne i środowiskowe, kody CPV."),
        "formularz": ("Przygotuj formularz ofertowy na USŁUGI: dane wykonawcy, cena (np. ryczałt miesięczny × liczba miesięcy albo stawki "
                      "jednostkowe × szacowane ilości) netto/VAT/brutto słownie, inne kryteria (np. doświadczenie personelu, czas reakcji), "
                      "termin świadczenia, oświadczenia, wykaz załączników, podpis."),
        "umowa": ("Przygotuj projektowane postanowienia umowy o ŚWIADCZENIE USŁUG: przedmiot i zakres, okres obowiązywania, sposób świadczenia "
                  "i odbioru (protokoły miesięczne), wynagrodzenie (ryczałtowe/według stawek) i płatności miesięczne, waloryzacja (art. 439 Pzp "
                  "przy umowie > 6 miesięcy), obowiązek zatrudnienia na umowę o pracę i kontrola (art. 95 Pzp), personel i jego zmiana, "
                  "podwykonawstwo, ubezpieczenie OC, kary umowne z łącznym limitem, zmiany umowy, odstąpienie i wypowiedzenie, RODO."),
    },
    "dostawy": {
        "opz": ("Przygotuj opis przedmiotu zamówienia na DOSTAWY: wykaz towarów z ilościami i jednostkami, minimalne parametry techniczne "
                "i funkcjonalne każdej pozycji (bez nazw producentów, a gdy to konieczne – z dopiskiem „lub równoważne” i kryteriami "
                "równoważności), wymagane certyfikaty, normy i deklaracje, miejsce, termin i sposób dostawy (rozładunek, wniesienie, montaż, "
                "szkolenie), gwarancja i serwis, prawo opcji (jeśli przewidziane), kody CPV."),
        "formularz": ("Przygotuj formularz ofertowy na DOSTAWY z formularzem asortymentowo-cenowym: dane wykonawcy, tabela pozycji (nazwa, "
                      "oferowany producent/model, j.m., ilość, cena jedn. netto, wartość netto, VAT, brutto), razem słownie, oferowany "
                      "okres gwarancji i termin dostawy, oświadczenia (zgodność z OPZ, równoważność), wykaz załączników, podpis."),
        "umowa": ("Przygotuj projektowane postanowienia umowy DOSTAWY: przedmiot (zgodnie z ofertą i formularzem cenowym), termin i miejsce dostawy, "
                  "warunki dostawy i odbioru (protokół odbioru ilościowo-jakościowego, reklamacje), wynagrodzenie i płatność, prawo opcji, "
                  "gwarancja i rękojmia, serwis i czas naprawy, kary umowne z łącznym limitem, zmiany umowy (np. produkt zamienny o lepszych "
                  "parametrach), odstąpienie, RODO."),
    },
}


# zamówienie kredytowane / dofinansowane: co z wymagań instytucji finansującej trafia do którego dokumentu
FIN_W_DOKUMENCIE = {
    "swz": ("Zamówienie jest finansowane ze źródeł podanych w wymaganiach (kredyt / premia BGK / KPO / dotacja): wskaż źródło finansowania, termin "
            "wykonania nie późniejszy niż podany w wymaganiach (z zapasem na odbiór i rozliczenie) i wymóg harmonogramu rzeczowo-finansowego "
            "z etapami dopasowanymi do transz."),
    "umowa": ("Uwzględnij wymagania instytucji finansującej: termin zakończenia robót z wymagań, harmonogram rzeczowo-finansowy jako załącznik "
              "z etapami i odbiorami częściowymi dopasowanymi do transz, płatności częściowe po odbiorach etapów, obowiązki wykonawcy wobec "
              "instytucji (kontrole, dokumenty do rozliczenia, oznakowanie, archiwizacja), zmiany umowy wymagające zgody instytucji (jeśli wymaga "
              "tego umowa finansowania), faktury z podziałem na koszty kwalifikowalne i niekwalifikowalne, inne wymagania wobec umowy z wykonawcą "
              "wymienione w wymaganiach."),
    "opz": "Uwzględnij wymagania instytucji finansującej dotyczące zakresu, standardu i dokumentacji powykonawczej (np. dokumenty do rozliczenia).",
    "formularz": "Formularz: termin wykonania zgodny z wymaganiami finansowania; cena z podziałem na etapy harmonogramu (transze), jeśli to potrzebne.",
}


def rodzaj_dokumentacji(pola):
    """Opis rodzaju dokumentacji do polecenia: kod trybu (pola["tryb"]) decyduje o reżimie, nazwa wybranego trybu (pola["tryb_nazwa"]) – o opisie."""
    kod, nazwa = str(pola.get("tryb") or ""), str(pola.get("tryb_nazwa") or "").strip()
    if nazwa and kod.startswith("pzp"):
        return (f"{nazwa} – postępowanie według ustawy Prawo zamówień publicznych"
                + (" (dokument zamówienia: Specyfikacja Warunków Zamówienia – SWZ)" if kod in ("pzp_podstawowy", "pzp_nieograniczony") else ""))
    return nazwa or TRYBY_POST.get(kod, kod)


def czy_unijny(pola):
    """Procedura unijna (JEDZ – art. 125 ust. 2, nie stosuje się poniżej progów – art. 266): z wartości zamówienia (pola["unijny"]),
    a gdy jej nie podano – z kodu trybu."""
    if pola.get("unijny") in ("tak", "nie"):
        return pola["unijny"] == "tak" and str(pola.get("tryb") or "").startswith("pzp")
    return pola.get("tryb") == "pzp_nieograniczony"


def polecenie_dokumentu(rodzaj, pola, cfg, rodzaj_zam="roboty"):
    zam = pola.get("zamawiajacy") or "[UZUPEŁNIJ: nazwa, adres i NIP zamawiającego]"  # bez danych z profilu – profil nie musi być zamawiającym
    wym = "\n".join(f"- {k}: {v}" for k, v in [
        ("Rodzaj dokumentacji", rodzaj_dokumentacji(pola)), ("Zamawiający", zam),
        ("Nazwa zamówienia", pola.get("nazwa")), ("Znak sprawy", pola.get("znak")), ("Zakres / opis", pola.get("zakres")),
        ("Wartość szacunkowa (netto)", pola.get("wartosc")), ("Termin realizacji", pola.get("termin_realizacji")),
        ("Dane zamawiającego do dokumentów (NIP, REGON, kontakt, strona, rachunek, godziny pracy)", pola.get("dane_zamawiajacego")),
        ("Termin składania ofert", pola.get("termin_ofert")), ("Termin otwarcia ofert", pola.get("termin_otwarcia")),
        ("Sposób składania ofert", pola.get("platforma")),
        ("Wadium", pola.get("wadium")), ("Warunki udziału", pola.get("warunki")), ("Kryteria oceny ofert", pola.get("kryteria")),
        ("Minimalna gwarancja", pola.get("gwarancja")), ("Wynagrodzenie", pola.get("wynagrodzenie")),
        ("Płatności", pola.get("platnosci")), ("Kary umowne", pola.get("kary")), ("Zabezpieczenie należytego wykonania", pola.get("zabezpieczenie")),
        ("Osoba do kontaktu", pola.get("kontakt")), ("Dodatkowe wymagania zamawiającego", pola.get("uwagi")),
        ("Fakultatywne podstawy wykluczenia (art. 109 ust. 1 Pzp)", pola.get("wykluczenie") if str(pola.get("tryb") or "").startswith("pzp") else ""),
        ("JEDZ – część IV (kryteria kwalifikacji)", pola.get("jedz") if czy_unijny(pola) else ""),
        ("Wymagania instytucji finansującej (kredyt / premia BGK / KPO / dotacja) – uwzględnij w dokumentach, umowie i harmonogramie",
         pola.get("finansowanie"))] if v)
    zakres = {
        "swz": ("Przygotuj pełny dokument postępowania (SWZ albo zapytanie ofertowe – zgodnie z rodzajem dokumentacji) ze wszystkimi "
                "wymaganymi elementami: zamawiający, tryb, opis przedmiotu (skrót z odesłaniem do OPZ i dokumentacji), terminy, "
                "warunki udziału i podstawy wykluczenia, wykaz oświadczeń i dokumentów, informacje o komunikacji, wadium, termin "
                "związania ofertą, sposób przygotowania i złożenia oferty, termin otwarcia, sposób obliczenia ceny, kryteria z wagami "
                "i sposobem punktacji, formalności przed zawarciem umowy, zabezpieczenie, projektowane postanowienia umowy (odesłanie), "
                "środki ochrony prawnej (przy Pzp), RODO, wykaz załączników."),
        "opz": ("Przygotuj opis przedmiotu zamówienia: stan istniejący, zakres robót (z podziałem na branże/elementy i ilościami "
                "z przedmiaru lub dokumentacji), wymagania materiałowe (parametry, „lub równoważne”), wymagania wykonawcze i odbiorowe, "
                "organizacja robót, dokumentacja powykonawcza, wymagane normy i przepisy, kody CPV."),
        "formularz": ("Przygotuj formularz ofertowy: dane wykonawcy (miejsca do uzupełnienia), cena netto/VAT/brutto z kwotą słownie, "
                      "oferowany okres gwarancji i inne kryteria, termin realizacji, oświadczenia (zapoznanie z SWZ, związanie ofertą, "
                      "akceptacja wzoru umowy, podwykonawcy, tajemnica przedsiębiorstwa, RODO, status MŚP), wykaz załączników, miejsce na podpis."),
        "oswiadczenia": ("Przygotuj załączniki dla wykonawców: oświadczenie o niepodleganiu wykluczeniu i spełnianiu warunków udziału (art. 125 Pzp; "
                         "poniżej progu – odpowiednio uproszczone), oświadczenie o przynależności do grupy kapitałowej, wykaz wykonanych robót / "
                         "usług / dostaw (zgodnie z warunkami udziału), wykaz osób skierowanych do realizacji zamówienia, oświadczenie o braku powiązań "
                         "(gdy wymagane), zobowiązanie podmiotu udostępniającego zasoby. Każdy jako osobny rozdział z miejscem na podpis."),
        "ogloszenie": ("Przygotuj treść ogłoszenia o zamówieniu do publikacji – zgodnie z wybranym trybem: zamawiający, tryb i podstawa prawna, "
                       "przedmiot i kody CPV, części, terminy (składania ofert albo wniosków, realizacji), warunki udziału i podstawy wykluczenia, "
                       "wykaz oświadczeń i dokumentów, wadium, kryteria, sposób komunikacji i adres strony postępowania. Treść w układzie pól ogłoszenia."),
        "wniosek_dopuszczenie": ("Przygotuj wzór wniosku o dopuszczenie do udziału w postępowaniu: dane wykonawcy, wskazanie postępowania, oświadczenie "
                                 "o spełnianiu warunków i niepodleganiu wykluczeniu, wykaz dokumentów potwierdzających warunki, zobowiązanie podmiotu "
                                 "udostępniającego zasoby (jeśli dotyczy), kryteria kwalifikacji (gdy zamawiający ogranicza liczbę wykonawców), podpis."),
        "zaproszenie_oferty": ("Przygotuj zaproszenie do składania ofert skierowane do wykonawców zakwalifikowanych (po ocenie wniosków): odesłanie do SWZ, "
                               "termin, miejsce i sposób składania ofert, termin związania ofertą, wadium, kryteria, sposób komunikacji."),
        "zaproszenie_negocjacje": ("Przygotuj zaproszenie do negocjacji zgodne z wybranym trybem: przedmiot i zakres negocjacji (dla trybu podstawowego – "
                                   "tylko elementy ofert podlegające ocenie w kryteriach), miejsce, termin i forma negocjacji, informacja o zasadach "
                                   "(równe traktowanie, poufność), dokumenty do przygotowania; przy wolnej ręce / negocjacjach bez ogłoszenia – "
                                   "wskazanie podstawy prawnej trybu i warunków umowy do uzgodnienia."),
        "zaproszenie_ostateczne": ("Przygotuj zaproszenie do składania ofert ostatecznych po negocjacjach: termin i sposób złożenia, informacja, "
                                   "że oferty ostateczne podlegają ocenie według kryteriów, zakres zmian wynegocjowanych, termin związania ofertą."),
        "protokol": ("Przygotuj protokół postępowania zgodny z wybranym trybem: dane zamawiającego i postępowania, tryb i jego podstawa, wartość "
                     "szacunkowa z datą ustalenia, osoby wykonujące czynności, oświadczenia o braku konfliktu interesów, terminy, lista wniosków / "
                     "ofert, przebieg negocjacji (jeśli były), ocena i wybór, uzasadnienie, załączniki. Dane, których nie ma – [UZUPEŁNIJ: …]."),
        "uzasadnienie_trybu": ("Przygotuj notatkę uzasadniającą wybór trybu: wskazanie trybu i przepisu, opis okoliczności faktycznych odpowiadających "
                               "KAŻDEJ przesłance ustawowej (np. dla wolnej ręki i negocjacji bez ogłoszenia – konkretna przesłanka z ustawy), "
                               "dowody / dokumenty potwierdzające, ocena ryzyka zakwestionowania, wnioski. Gdy faktów brak – [UZUPEŁNIJ: …]; "
                               "nie twierdź, że przesłanka jest spełniona, jeśli dane tego nie potwierdzają."),
        "umowa": ("Przygotuj projektowane postanowienia umowy (wzór umowy o roboty budowlane) z perspektywy zamawiającego: przedmiot, "
                  "terminy, wynagrodzenie (ryczałtowe/kosztorysowe), waloryzacja (gdy wymagana), płatności i odbiory częściowe, "
                  "obowiązki stron, kierownik budowy, podwykonawstwo (zgodnie z Pzp przy zamówieniach publicznych), odbiory, gwarancja "
                  "i rękojmia, kary umowne z łącznym limitem, zabezpieczenie, zmiany umowy (przesłanki), odstąpienie, postanowienia końcowe."),
    }[rodzaj]
    zakres = ZAKRES_RODZAJU.get(rodzaj_zam, {}).get(rodzaj, zakres)
    if pola.get("finansowanie") and rodzaj in FIN_W_DOKUMENCIE:
        zakres += " " + FIN_W_DOKUMENCIE[rodzaj]
    wym = f"- Rodzaj zamówienia: {RODZAJE_ZAM.get(rodzaj_zam, RODZAJE_ZAM['roboty'])['nazwa']}\n" + wym
    t_ = str(pola.get("tryb") or "")
    ust = PARAMETRY_USTAWOWE.get(t_) or (PARAMETRY_USTAWOWE["pzp_podstawowy"] if "podstawow" in t_.lower() else
                                         PARAMETRY_USTAWOWE["pzp_nieograniczony"] if "nieograniczon" in t_.lower() else "")
    wsp = ustalenia_wspolne(pola, rodzaj_zam) if rodzaj in ("swz", "opz", "umowa", "formularz", "ogloszenie") else ""
    return (f"WYMAGANIA ZAMAWIAJĄCEGO:\n{wym}\n\n" + (f"PARAMETRY USTAWOWE TRYBU (stosuj dokładnie, nie podawaj innych limitów):\n{ust}\n\n" if ust else "")
            + (f"USTALENIA WSPÓLNE DLA CAŁEGO KOMPLETU (pozostałe dokumenty powstają osobno – muszą być z nimi zgodne):\n{wsp}\n\n" if wsp else "")
            + f"Dokumenty powyżej (projekt, przedmiar, opis potrzeb, wykaz towarów, szacowanie wartości itp.) wykorzystaj do "
            f"opisu zakresu i ilości.\n\nZADANIE: {zakres}\n\nZwróć JSON: {{\"tytul\": \"tytuł dokumentu\", \"rozdzialy\": "
            "[{\"tytul\": \"1. …\", \"akapity\": [\"1.1. …\", \"1.2. …\"]}], \"do_decyzji\": [\"pkt 8.4 – … (krótko: co zamawiający musi rozstrzygnąć)\"]}. "
            "Pisz pełne zapisy (nie skróty), gotowe do wklejenia. " + ZASADY_UZUPELNIJ)


# Limity sprawdzone w tekście ustawy (art. 307 – standardyprawa.pl, 11.2026); terminy z art. 283 i 284 – jak w kalendarzu postępowania programu.
PARAMETRY_USTAWOWE = {
    "pzp_podstawowy": ("- Termin związania ofertą: nie dłużej niż 30 dni od dnia upływu terminu składania ofert; pierwszym dniem terminu jest dzień upływu "
                       "terminu składania ofert (art. 307 ust. 1 Pzp). Przedłużenie: zamawiający jednokrotnie zwraca się o zgodę na przedłużenie "
                       "o okres nie dłuższy niż 30 dni (art. 307 ust. 2 Pzp).\n"
                       "- Termin składania ofert: co najmniej 14 dni od zamieszczenia ogłoszenia w BZP przy robotach budowlanych, 7 dni przy dostawach "
                       "i usługach (art. 283 Pzp).\n"
                       "- Wyjaśnienia treści SWZ: zamawiający odpowiada nie później niż na 2 dni przed upływem terminu składania ofert na wnioski złożone "
                       "nie później niż na 4 dni przed tym terminem (art. 284 ust. 2 Pzp).\n"
                       "- Otwarcie ofert: niezwłocznie po upływie terminu składania ofert, nie później niż następnego dnia (art. 222 ust. 1 Pzp).\n"
                       "- Oświadczenie o przynależności albo braku przynależności do tej samej grupy kapitałowej (art. 108 ust. 1 pkt 5 Pzp): "
                       "podmiotowy środek dowodowy składany na wezwanie zamawiającego – NIE w terminie 3 dni od otwarcia ofert (to zasada dawnej ustawy)."),
    "pzp_nieograniczony": ("- Termin związania ofertą: nie dłużej niż 90 dni od dnia upływu terminu składania ofert (120 dni, gdy wartość robót budowlanych "
                           "jest równa lub przekracza 20 000 000 euro, a dostaw lub usług – 10 000 000 euro); pierwszym dniem terminu jest dzień upływu "
                           "terminu składania ofert; termin wskazuje się datą (art. 220 Pzp). Przedłużenie: zamawiający jednokrotnie zwraca się o zgodę na "
                           "przedłużenie o okres nie dłuższy niż 60 dni (art. 220 ust. 3 Pzp).\n"
                           "- Termin składania ofert: co najmniej 35 dni od przekazania ogłoszenia Urzędowi Publikacji UE; 30 dni, gdy oferty składa się "
                           "w całości przy użyciu środków komunikacji elektronicznej (art. 138 ust. 1 i 4 Pzp).\n"
                           "- Wyjaśnienia treści SWZ: zamawiający odpowiada nie później niż na 6 dni przed upływem terminu składania ofert na wnioski złożone "
                           "nie później niż na 14 dni przed tym terminem (art. 135 ust. 2 Pzp).\n"
                           "- Oświadczenie o niepodleganiu wykluczeniu i spełnianiu warunków: na formularzu jednolitego europejskiego dokumentu zamówienia "
                           "(art. 125 ust. 2 Pzp).\n"
                           "- Otwarcie ofert: niezwłocznie po upływie terminu składania ofert, nie później niż następnego dnia (art. 222 ust. 1 Pzp).\n"
                           "- Zawarcie umowy: nie wcześniej niż 10 dni od przesłania zawiadomienia o wyborze środkami komunikacji elektronicznej (art. 264 ust. 1 Pzp).\n"
                           "- Oświadczenie o przynależności albo braku przynależności do tej samej grupy kapitałowej (art. 108 ust. 1 pkt 5 Pzp): "
                           "podmiotowy środek dowodowy składany na wezwanie zamawiającego – NIE w terminie 3 dni od otwarcia ofert (to zasada dawnej ustawy)."),
}

ZASADY_UZUPELNIJ = (
    "Zasady pól do uzupełnienia: dane podane wyżej (zamawiający, NIP, REGON, kontakt, strona, rachunek, godziny, terminy, wzory punktacji) wpisz "
    "wprost – bez [UZUPEŁNIJ]. Znacznik [UZUPEŁNIJ: …] stosuj tylko dla faktów, których nie ma w danych ani w dokumentach i których nie da się "
    "ustalić (np. numer ogłoszenia w BZP, identyfikator postępowania na platformie). Nie wstawiaj do treści próśb o potwierdzenie ani pytań "
    "do zamawiającego (np. „[UZUPEŁNIJ: potwierdzić …]”) – zapisz w treści rozwiązanie zgodne z danymi i przepisami, a sprawy do rozstrzygnięcia "
    "przez zamawiającego wypisz krótko w liście „do_decyzji” (z numerem punktu). Wzory punktacji kryteriów przepisz dokładnie tak, jak podano.")


def dokument_docx(sciezka, dane, pola, cfg):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(pola.get("zamawiajacy") or "[UZUPEŁNIJ: zamawiający]", rozmiar=9)
    if pola.get("znak"):
        A(f"Znak sprawy: {pola['znak']}", rozmiar=9)
    A(str(dane.get("tytul") or "").upper(), pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    if pola.get("nazwa"):
        A(pola["nazwa"], pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    for r in dane.get("rozdzialy", []):
        d.add_heading(str(r.get("tytul", "")), level=2)
        for a in r.get("akapity", []):
            if isinstance(a, dict):
                a = a.get("tekst") or " ".join(str(x) for x in a.values())
            A(str(a))
    A("")
    A("Projekt dokumentu przygotowany z pomocą AI – przed publikacją wymaga sprawdzenia przez osobę odpowiedzialną za postępowanie "
      "(w zamówieniach publicznych – zgodnie z ustawą Pzp).", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
    return len(dane.get("rozdzialy", []))


DOKUMENTY_PRYW = {  # wspólnota / spółdzielnia / deweloper – nazwy bez pojęć z Pzp (SWZ, OPZ)
    "swz": ("Zapytanie ofertowe", "Zapytanie_ofertowe"),
    "opz": ("Opis zakresu prac", "Opis_zakresu_prac"),
    "formularz": ("Formularz oferty", "Formularz_oferty"),
    "umowa": ("Wzór umowy (Kodeks cywilny)", "Wzor_umowy"),
    "protokol": ("Protokół wyboru oferty", "Protokol_wyboru"),
}


def etykieta_dok(rodzaj, prywatny=False):
    return (DOKUMENTY_PRYW[rodzaj] if prywatny and rodzaj in DOKUMENTY_PRYW else DOKUMENTY[rodzaj])[0]


def prefiks_dok(rodzaj, prywatny=False):
    return (DOKUMENTY_PRYW[rodzaj] if prywatny and rodzaj in DOKUMENTY_PRYW else DOKUMENTY[rodzaj])[1]


def nazwa_pliku(rodzaj, nazwa_projektu, prywatny=False):
    return f"{prefiks_dok(rodzaj, prywatny)}_{MO.bezpieczna_nazwa(nazwa_projektu)[:50]}.docx"


def czysc(t):
    return re.sub(r"\s+", " ", str(t or "")).strip()


# ---------------------------------------------------------------- oświadczenia i wykazy – stały wzór (bez AI): treść wynika z ustawy, dane z zamówienia
PIERWSZY_ZAL_OSWIADCZEN = 4  # zał. nr 1 – formularz ofertowy, nr 2 – OPZ, nr 3 – projektowane postanowienia umowy (plan_zalacznikow)


def plan_zalacznikow(rodzaj="roboty", tryb="pzp_podstawowy", unijny=None):
    """Jedna numeracja załączników dla całego kompletu (SWZ, formularz, OPZ, umowa i plik oświadczeń) – ta sama kolejność co w oswiadczenia_docx."""
    pzp = str(tryb).startswith("pzp")
    unijny = (tryb == "pzp_nieograniczony") if unijny is None else bool(unijny)
    wykaz = {"roboty": "robót budowlanych", "uslugi": "usług", "dostawy": "dostaw"}.get(rodzaj, "robót budowlanych")
    L = ["Formularz ofertowy",
         "Opis przedmiotu zamówienia" + (" wraz z dokumentacją projektową, STWiORB i przedmiarem robót" if rodzaj == "roboty" else ""),
         "Projektowane postanowienia umowy"]
    if unijny:
        L.append("Jednolity Europejski Dokument Zamówienia (JEDZ)")
    L.append("Oświadczenie wykonawcy – art. 125 ust. 1 Pzp" if pzp else "Oświadczenie wykonawcy o braku podstaw wykluczenia i spełnianiu warunków udziału")
    if pzp:
        L += ["Oświadczenie wykonawców wspólnie ubiegających się o zamówienie (art. 117 ust. 4 Pzp)",
              "Zobowiązanie podmiotu udostępniającego zasoby (art. 118 ust. 3 Pzp)",
              "Oświadczenie o grupie kapitałowej (art. 108 ust. 1 pkt 5 Pzp)"]
    L.append(f"Wykaz {wykaz}")
    if rodzaj in ("roboty", "uslugi"):
        L.append("Wykaz osób skierowanych do realizacji zamówienia")
    if pzp:
        L.append("Oświadczenie o aktualności informacji z oświadczenia z art. 125 ust. 1 Pzp")
    return [(i, t) for i, t in enumerate(L, 1)]


def ustalenia_wspolne(pola, rodzaj="roboty"):
    """Ustalenia, które muszą być jednakowe we wszystkich dokumentach kompletu (dokumenty pisane są osobno, równolegle)."""
    tryb = pola.get("tryb") or "pzp_podstawowy"
    pzp = str(tryb).startswith("pzp")
    dok = "SWZ" if pzp else "zapytania ofertowego"
    zal = "; ".join(f"nr {n} – {t}" for n, t in plan_zalacznikow(rodzaj, tryb, czy_unijny(dict(pola, tryb=tryb))))
    wyn = str(pola.get("wynagrodzenie") or "").lower()
    U = [f"Numeracja załączników do {dok} (stosuj dokładnie, w treści i w nagłówkach): {zal}. Nie dodawaj innych numerowanych załączników.",
         f"Kolejność pierwszeństwa dokumentów (ta sama w {dok}, OPZ i umowie): 1) umowa (projektowane postanowienia), 2) {dok}, "
         + ("3) dokumentacja projektowa, 4) STWiORB, 5) przedmiar robót – pomocniczy." if rodzaj == "roboty" else "3) opis przedmiotu zamówienia, 4) oferta wykonawcy.")]
    if "kosztorys" in wyn and "ryczał" not in wyn:
        U.append("Wynagrodzenie kosztorysowe: wykonawca składa z ofertą kosztorys ofertowy sporządzony na podstawie przedmiaru (część oferty, bez osobnego "
                 "numerowanego załącznika).")
    else:
        U.append("Wynagrodzenie ryczałtowe: cenę ryczałtową wykonawca podaje w formularzu ofertowym; NIE wymagaj z ofertą formularza cenowego, "
                 "kosztorysu ani tabeli elementów scalonych (rozbicie ceny – w harmonogramie rzeczowo-finansowym po zawarciu umowy).")
    if re.search(r"(?i)gwaranc", str(pola.get("kryteria") or "")):
        U.append("Okres gwarancji jest kryterium oceny: jeżeli wykonawca nie wskaże go w formularzu ofertowym, zamawiający przyjmie okres minimalny "
                 "i przyzna 0 pkt w tym kryterium – ta sama zasada w SWZ i w formularzu ofertowym.")
    return "\n".join(f"- {u}" for u in U)


def oswiadczenia_docx(sciezka, pola, rodzaj="roboty"):
    """Załączniki dla wykonawców: oświadczenie (art. 125 ust. 1 Pzp albo – poniżej progu – oświadczenie wykonawcy), wspólne ubieganie się (art. 117 ust. 4),
    zobowiązanie podmiotu udostępniającego zasoby (art. 118 ust. 3), grupa kapitałowa (art. 108 ust. 1 pkt 5), wykaz robót / usług / dostaw, wykaz osób,
    aktualność informacji. Generowane natychmiast ze wzoru – miejsca do uzupełnienia oznaczone [UZUPEŁNIJ]."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    tryb = pola.get("tryb") or "pzp_podstawowy"
    pzp = tryb.startswith("pzp")
    unijny = czy_unijny(dict(pola, tryb=tryb))
    w109 = str(pola.get("wykluczenie") or "").strip()  # decyzja z kroku „Warunki”; brak pola (inne ścieżki) – miejsce do uzupełnienia jak dotąd
    bez_109 = bool(re.match(r"(?i)(nie\b|brak|bez\b)", w109))
    pkt_109 = re.findall(r"\b(10|[1-9])\b", re.sub(r"(?i)art\.?\s*109|ust\.?\s*1\b", " ", w109)) if w109 and not bez_109 else []
    jedz_iv = str(pola.get("jedz") or "").strip()
    przedmiot = {"roboty": "robót budowlanych", "uslugi": "usług", "dostawy": "dostaw"}.get(rodzaj, "robót budowlanych")
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    zam, nazwa, znak = pola.get("zamawiajacy") or "[UZUPEŁNIJ: zamawiający]", pola.get("nazwa") or "[UZUPEŁNIJ: nazwa zamówienia]", pola.get("znak") or "[UZUPEŁNIJ]"
    W = "Wykonawca: ........................................................ (pełna nazwa / firma, adres, NIP / KRS / CEiDG)\nreprezentowany przez: ........................................ (imię, nazwisko, podstawa reprezentacji)"
    PODPIS = ("Dokument składa się w postaci elektronicznej opatrzonej kwalifikowanym podpisem elektronicznym, podpisem zaufanym lub podpisem osobistym."
              if pzp else "Dokument podpisuje osoba uprawniona do reprezentowania wykonawcy.")

    def zalacznik(nr, tytul, podtytul=""):  # numer jak w planie załączników do SWZ (po formularzu ofertowym, OPZ i umowie)
        if nr > 1:
            d.add_page_break()
        A(f"Załącznik nr {nr + PIERWSZY_ZAL_OSWIADCZEN - 1}" + (" do SWZ" if pzp else ""), rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
        A(f"Zamawiający: {zam}", rozmiar=9)
        A(f"Znak sprawy: {znak}", rozmiar=9)
        A(tytul.upper(), pogrub=True, rozmiar=12, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        if podtytul:
            A(podtytul, kursywa=True, rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        A(f"dotyczy postępowania: {nazwa}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        A(W, rozmiar=9)

    def podpis():
        A("\n........................................ (miejscowość, data)", rozmiar=9)
        A(PODPIS, kursywa=True, rozmiar=8)

    nr = 1
    if unijny:
        zalacznik(nr, "Jednolity Europejski Dokument Zamówienia (JEDZ)", "art. 125 ust. 1 ustawy Prawo zamówień publicznych – procedura unijna")
        A("W postępowaniu o wartości równej lub przekraczającej progi unijne oświadczenie, o którym mowa w art. 125 ust. 1 Pzp, wykonawca składa na formularzu "
          "Jednolitego Europejskiego Dokumentu Zamówienia (JEDZ), sporządzonym w postaci elektronicznej (np. w serwisie eESPD) i opatrzonym kwalifikowanym podpisem elektronicznym.")
        A("Zamawiający informuje, które części JEDZ wykonawca wypełnia: część II (informacje o wykonawcy), część III (podstawy wykluczenia), część IV (kryteria kwalifikacji – "
          + (jedz_iv if jedz_iv else "[UZUPEŁNIJ: sekcja α albo sekcje A–D zgodnie z SWZ]") + "), część VI (oświadczenia końcowe).")
        A("Niezależnie od JEDZ wykonawca składa oświadczenie dotyczące przesłanek wykluczenia z art. 7 ust. 1 ustawy z dnia 13 kwietnia 2022 r. o szczególnych rozwiązaniach "
          "w zakresie przeciwdziałania wspieraniu agresji na Ukrainę oraz służących ochronie bezpieczeństwa narodowego – według wzoru poniżej.")
        nr += 1
    tytul1 = ("Oświadczenie wykonawcy" + (" – przesłanki z ustawy sankcyjnej" if unijny else " składane na podstawie art. 125 ust. 1 ustawy Prawo zamówień publicznych")
              if pzp else "Oświadczenie wykonawcy o braku podstaw wykluczenia i spełnianiu warunków udziału")
    zalacznik(nr, tytul1, "aktualne na dzień składania ofert" if pzp else "")
    if not unijny:
        A("I. OŚWIADCZENIA DOTYCZĄCE PODSTAW WYKLUCZENIA", pogrub=True)
        if pzp:
            A("1. Oświadczam, że nie podlegam wykluczeniu z postępowania na podstawie art. 108 ust. 1 ustawy Prawo zamówień publicznych.")
            if pkt_109:
                A("2. Oświadczam, że nie podlegam wykluczeniu z postępowania na podstawie art. 109 ust. 1 pkt " + ", ".join(dict.fromkeys(pkt_109)) + " ustawy Prawo zamówień publicznych.")
            elif w109 and not bez_109:
                A(f"2. Oświadczam, że nie podlegam wykluczeniu z postępowania na podstawie art. 109 ust. 1 ustawy Prawo zamówień publicznych w zakresie wskazanym przez zamawiającego: {w109}.")
            elif not w109:
                A("2. Oświadczam, że nie podlegam wykluczeniu z postępowania na podstawie art. 109 ust. 1 pkt [UZUPEŁNIJ: punkty wskazane w SWZ albo usuń] ustawy Prawo zamówień publicznych.")
            A(("2" if bez_109 else "3") + ". Oświadczam, że zachodzą w stosunku do mnie podstawy wykluczenia z postępowania na podstawie art. ........ ustawy Prawo zamówień publicznych (podać podstawę – "
              "wypełnić tylko, jeżeli dotyczy). Jednocześnie oświadczam, że w związku z ww. okolicznością, na podstawie art. 110 ust. 2 ustawy, podjąłem następujące "
              "środki naprawcze: ........................................")
        else:
            A("1. Oświadczam, że nie podlegam wykluczeniu z postępowania z przyczyn wskazanych w zapytaniu ofertowym.")
    A(("3" if pzp and not unijny and bez_109 else "4" if pzp and not unijny else "2" if not unijny else "1") + ". Oświadczam, że nie zachodzą w stosunku do mnie przesłanki wykluczenia z postępowania na podstawie art. 7 ust. 1 "
      "ustawy z dnia 13 kwietnia 2022 r. o szczególnych rozwiązaniach w zakresie przeciwdziałania wspieraniu agresji na Ukrainę oraz służących ochronie bezpieczeństwa narodowego.")
    if not unijny:
        A("II. OŚWIADCZENIE DOTYCZĄCE SPEŁNIANIA WARUNKÓW UDZIAŁU", pogrub=True)
        A("Oświadczam, że spełniam warunki udziału w postępowaniu określone przez zamawiającego w " + ("rozdziale [UZUPEŁNIJ] SWZ." if pzp else "zapytaniu ofertowym."))
        A("III. INFORMACJA W ZWIĄZKU Z POLEGANIEM NA ZASOBACH INNYCH PODMIOTÓW (wypełnić, jeżeli dotyczy)", pogrub=True)
        A("Oświadczam, że w celu wykazania spełniania warunków udziału w postępowaniu polegam na zasobach następującego podmiotu: ........................................ "
          "w następującym zakresie: ........................................")
        A("IV. OŚWIADCZENIE DOTYCZĄCE PODANYCH INFORMACJI", pogrub=True)
        A("Oświadczam, że wszystkie informacje podane w powyższych oświadczeniach są aktualne i zgodne z prawdą oraz zostały przedstawione z pełną świadomością "
          "konsekwencji wprowadzenia zamawiającego w błąd przy przedstawianiu informacji.")
    podpis()
    if pzp:
        nr += 1
        zalacznik(nr, "Oświadczenie wykonawców wspólnie ubiegających się o udzielenie zamówienia", "art. 117 ust. 4 ustawy Prawo zamówień publicznych (wypełnić, jeżeli dotyczy)")
        A("Oświadczamy, że poszczególni wykonawcy wspólnie ubiegający się o udzielenie zamówienia wykonają następujące " + przedmiot + ":")
        MO._tabela(d, [["Wykonawca (nazwa, adres)", "Zakres " + przedmiot + " wykonywanych przez wykonawcę"], ["", ""], ["", ""]])
        podpis()
        nr += 1
        zalacznik(nr, "Zobowiązanie podmiotu udostępniającego zasoby", "art. 118 ust. 3 ustawy Prawo zamówień publicznych (wypełnić, jeżeli dotyczy)")
        A("Podmiot udostępniający zasoby: ........................................ (nazwa, adres, NIP)")
        A("Zobowiązuję się do oddania do dyspozycji wykonawcy: ........................................ niezbędnych zasobów na potrzeby realizacji zamówienia.")
        A("1. Zakres dostępnych wykonawcy zasobów: ........................................")
        A("2. Sposób i okres udostępnienia oraz wykorzystania zasobów przy wykonywaniu zamówienia: ........................................")
        A("3. Czy i w jakim zakresie podmiot zrealizuje " + przedmiot + ", których dotyczą udostępniane zdolności (dotyczy wykształcenia, kwalifikacji zawodowych lub doświadczenia): "
          "........................................")
        A("Oświadczam, że nie podlegam wykluczeniu z postępowania i spełniam warunki udziału w zakresie, w jakim wykonawca powołuje się na moje zasoby.")
        podpis()
        nr += 1
        zalacznik(nr, "Oświadczenie o przynależności lub braku przynależności do tej samej grupy kapitałowej", "art. 108 ust. 1 pkt 5 ustawy Prawo zamówień publicznych – składane na wezwanie zamawiającego")
        A("Oświadczam, że (zaznaczyć właściwe):")
        A("☐ nie należę do tej samej grupy kapitałowej, w rozumieniu ustawy z dnia 16 lutego 2007 r. o ochronie konkurencji i konsumentów, z innym wykonawcą, który złożył "
          "odrębną ofertę w postępowaniu;")
        A("☐ należę do tej samej grupy kapitałowej z następującym wykonawcą / wykonawcami, który złożył odrębną ofertę: ........................................ "
          "i przedstawiam dokumenty lub informacje potwierdzające przygotowanie oferty niezależnie od innego wykonawcy należącego do tej samej grupy kapitałowej.")
        podpis()
    nr += 1
    wykaz = {"roboty": "robót budowlanych", "uslugi": "usług", "dostawy": "dostaw"}.get(rodzaj, "robót budowlanych")
    zalacznik(nr, f"Wykaz {wykaz}", "na potwierdzenie spełniania warunku doświadczenia – składany na wezwanie zamawiającego" if pzp else "na potwierdzenie spełniania warunku doświadczenia")
    if rodzaj == "roboty":
        A("Wykaz robót budowlanych wykonanych nie wcześniej niż w okresie ostatnich 5 lat, a jeżeli okres prowadzenia działalności jest krótszy – w tym okresie, "
          "wraz z podaniem ich rodzaju, wartości, daty i miejsca wykonania oraz podmiotów, na rzecz których roboty zostały wykonane:")
        MO._tabela(d, [["Lp.", "Rodzaj i zakres robót", "Wartość [zł brutto]", "Data wykonania (od–do)", "Miejsce wykonania", "Podmiot, na rzecz którego wykonano"]] + [[str(i), "", "", "", "", ""] for i in (1, 2, 3)])
        A("Do wykazu należy załączyć dowody określające, czy roboty zostały wykonane należycie (np. referencje, protokoły odbioru).", kursywa=True, rozmiar=9)
    else:
        A(f"Wykaz {wykaz} wykonanych, a w przypadku świadczeń powtarzających się lub ciągłych również wykonywanych, w okresie ostatnich 3 lat, a jeżeli okres prowadzenia "
          "działalności jest krótszy – w tym okresie, wraz z podaniem ich wartości, przedmiotu, dat wykonania i podmiotów, na rzecz których zostały wykonane:")
        MO._tabela(d, [["Lp.", "Przedmiot", "Wartość [zł brutto]", "Data wykonania (od–do)", "Podmiot, na rzecz którego wykonano"]] + [[str(i), "", "", "", ""] for i in (1, 2, 3)])
        A("Do wykazu należy załączyć dowody określające, czy " + ("usługi zostały wykonane" if rodzaj == "uslugi" else "dostawy zostały wykonane") +
          " lub są wykonywane należycie (np. referencje).", kursywa=True, rozmiar=9)
    podpis()
    if rodzaj in ("roboty", "uslugi"):
        nr += 1
        zalacznik(nr, "Wykaz osób skierowanych do realizacji zamówienia", "na potwierdzenie spełniania warunku dysponowania osobami" + (" – składany na wezwanie zamawiającego" if pzp else ""))
        MO._tabela(d, [["Lp.", "Imię i nazwisko", "Funkcja w realizacji zamówienia", "Kwalifikacje zawodowe / uprawnienia (nr, specjalność)", "Doświadczenie", "Podstawa dysponowania osobą"]]
                   + [[str(i), "", "kierownik budowy" if (rodzaj == "roboty" and i == 1) else "", "", "", ""] for i in (1, 2, 3)])
        podpis()
    if pzp:
        nr += 1
        zalacznik(nr, "Oświadczenie o aktualności informacji zawartych w oświadczeniu, o którym mowa w art. 125 ust. 1 Pzp", "składane na wezwanie zamawiającego")
        A("Oświadczam, że informacje zawarte w oświadczeniu, o którym mowa w art. 125 ust. 1 ustawy Prawo zamówień publicznych" + (" (JEDZ)" if unijny else "") +
          ", w zakresie podstaw wykluczenia z postępowania wskazanych przez zamawiającego, są aktualne.")
        podpis()
    d.add_page_break()
    A("Wzór przygotowany przez program na podstawie przepisów i danych zamówienia. Dostosuj do SWZ (warunki udziału, punkty art. 109, wymagane wykazy) i usuń załączniki, "
      "które nie dotyczą postępowania.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
    return nr
