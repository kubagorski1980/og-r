# -*- coding: utf-8 -*-
"""
Moduł „Dla Prawnika” – sprawdzanie dokumentacji zamówień publicznych (Pzp) i opinia prawna.

Sprawa ma trzy ustawienia, które zmieniają listę kontrolną:
- przedmiot: roboty budowlane na nieruchomości / usługi / dostawy,
- tryb (albo „ustal z dokumentów”),
- dla kogo: zamawiający / wykonawca (oferent) / niezależna opinia.
Wynik: uwagi w formacie weryfikacji (cytat, waga, podstawa prawna, propozycja) + opinia prawna (pismo Word).

Punkty odniesienia sprawdzone w źródłach (21.10.2026): art. 439 Pzp – waloryzacja w umowach na roboty, dostawy i usługi
zawartych na okres dłuższy niż 6 miesięcy (t.j. Dz.U. 2026 poz. 793); art. 307 Pzp – związanie ofertą w trybie podstawowym
najwyżej 30 dni od upływu terminu składania ofert. Pozostałe przepisy AI ma wskazywać przy każdej uwadze (podstawa prawna).
"""
import datetime as dt
import json

import lista_kontroli as LK
import modul_oferty as MO
import progi as PR

PRZEDMIOTY = {"dostawy": "Dostawy", "uslugi": "Usługi", "roboty": "Roboty budowlane na nieruchomości"}
DLA_KOGO = {"zamawiajacy": "dla zamawiającego", "wykonawca": "dla wykonawcy (oferenta)", "niezalezna": "niezależna opinia"}
TRYBY = LK.TRYBY
USTAWIENIA_DOMYSLNE = {"przedmiot": "roboty", "tryb": "auto", "dla_kogo": "zamawiajacy", "klient": "", "pytania_klienta": "", "zatwierdzone": ""}

LISTA_WSPOLNA, LISTA_PRZEDMIOTU, LISTA_POZA_PZP, DODATKI_GRUPY = LK.LISTA_WSPOLNA, LK.LISTA_PRZEDMIOTU, LK.LISTA_POZA_PZP, LK.DODATKI_GRUPY
TRYB_KREATORA, grupa, lista_trybu = LK.TRYB_KREATORA, LK.grupa, LK.lista_trybu


PERSPEKTYWA = {
    "zamawiajacy": "Pracujesz DLA ZAMAWIAJĄCEGO: oceniasz zgodność z prawem i ryzyko (odwołanie do KIO, unieważnienie postępowania, korekta finansowa przy dofinansowaniu). "
                   "Przy każdej uwadze daj konkretną propozycję poprawionego zapisu (nowy_tekst), gotową do wprowadzenia.",
    "wykonawca": "Pracujesz DLA WYKONAWCY (oferenta): wskazujesz ryzyka dla oferenta, zapisy niezgodne z prawem, które warto zakwestionować, i to, co musi uwzględnić "
                 "w ofercie. Przy każdej uwadze daj gotowe pytanie do zamawiającego (pytanie_do_zamawiajacego) i wskaż, czy jest podstawa do odwołania (z terminem).",
    "niezalezna": "Sporządzasz NIEZALEŻNĄ OPINIĘ: oceniasz zgodność z prawem i ryzyka obu stron, bez stawania po żadnej. Przy uwadze daj propozycję poprawionego zapisu "
                  "i – gdy to przydatne – pytanie do zamawiającego.",
}

SYSTEM = (PR.INFO_AI + " Jesteś doświadczonym radcą prawnym specjalizującym się w zamówieniach publicznych w Polsce (Pzp, orzecznictwo KIO, prawo budowlane, "
          "Kodeks cywilny). Opierasz się WYŁĄCZNIE na treści przekazanych dokumentów i obowiązujących przepisach; przy każdej uwadze podajesz podstawę prawną "
          "(artykuł, ustęp). Gdy nie masz pewności co do przepisu albo jego aktualnego brzmienia – piszesz to wprost. Odpowiadasz wyłącznie JSON-em.")


def ustawienia(m):
    u = dict(USTAWIENIA_DOMYSLNE)
    u.update({k: v for k, v in (m.get("prawnik") or {}).items() if k in USTAWIENIA_DOMYSLNE})
    if u["przedmiot"] not in PRZEDMIOTY:
        u["przedmiot"] = "roboty"
    if u["tryb"] not in TRYBY:
        u["tryb"] = "auto"
    if u["dla_kogo"] not in DLA_KOGO:
        u["dla_kogo"] = "zamawiajacy"
    return u


def polecenie(u, dodatkowe=""):
    tryb = ("Tryb ustal z dokumentów i oceń, czy jest dopuszczalny." if u["tryb"] == "auto"
            else f"Postępowanie prowadzone w trybie: {TRYBY[u['tryb']]} – sprawdź przesłanki i wymogi tego trybu.")
    pyt = f"\nPytania / obawy klienta, na które trzeba odpowiedzieć: {u['pytania_klienta']}" if u.get("pytania_klienta") else ""
    dod = f"\nDodatkowo zwróć uwagę na: {dodatkowe}" if dodatkowe.strip() else ""
    poza = grupa(u["tryb"]) in ("F", "G")  # poniżej progu / zasada konkurencyjności – bez listy Pzp
    return f"""Sprawdź dokumentację zamówienia {"(poza Pzp)" if poza else "publicznego"} (powyżej) jako prawnik. Przedmiot: {PRZEDMIOTY[u['przedmiot']]}. {tryb}
{PERSPEKTYWA[u['dla_kogo']]}{pyt}{dod}

LISTA KONTROLNA (sprawdź każdy punkt, który dotyczy tej dokumentacji; gdy wymogi trybu stanowią inaczej niż lista ogólna – stosuj wymogi trybu):
{lista_trybu(u['tryb'], u['przedmiot'])}
{LK.lista_ogolna("poza" if poza else "pzp", u['przedmiot'])}

Zwróć JSON:
{{"podsumowanie": "3–6 zdań: ocena prawna dokumentacji, rozpoznany tryb i przedmiot, najważniejsze problemy",
  "ocena": "zgodna z prawem | wymaga poprawek | wymaga istotnych poprawek / wysokie ryzyko",
  "uwagi": [{{"waga": "krytyczna | istotna | drobna",
             "kategoria": "niezgodność z przepisami | sprzeczność | brak | ryzyko | niejasność | błąd",
             "dokument": "nazwa pliku", "miejsce": "rozdział / punkt / paragraf / strona",
             "cytat": "DOSŁOWNY fragment z dokumentu, znak w znak (20–300 znaków) – program sprawdza go w pliku; albo pusty przy braku",
             "opis": "na czym polega problem prawny i jakie ma skutki",
             "podstawa": "{'przepis (np. art. 484 § 2 k.c., punkt regulaminu albo wytycznych)' if poza else 'przepis (np. art. 439 ust. 1 Pzp) albo orzeczenie KIO'}; przy niepewności – napisz to",
             "propozycja": "co zrobić", "nowy_tekst": "gotowe nowe brzmienie zastępujące cytat albo pusty",
             "pytanie_do_zamawiajacego": "gotowe pytanie albo pusty"}}]}}
Najważniejsze uwagi najpierw (krytyczne: niezgodność z prawem grożąca unieważnieniem, odwołaniem lub korektą). Maksymalnie 40 uwag."""


# ---------------------------------------------------------------- opinia prawna (pismo)
SYSTEM_OPINIA = (PR.INFO_AI + " Jesteś radcą prawnym. Na podstawie przekazanych ustaleń (uwag ze sprawdzenia dokumentacji) piszesz opinię prawną: rzeczowo, "
                 "z podstawą prawną przy każdym wniosku, bez dodawania faktów spoza ustaleń. Odpowiadasz wyłącznie JSON-em.")


def polecenie_opinii(u, nazwa, w):
    uw = [{k: x.get(k) for k in ("waga", "kategoria", "dokument", "miejsce", "opis", "podstawa", "propozycja", "status")} for x in (w.get("uwagi") or [])
          if x.get("status") != "odrzucone"][:40]
    return f"""Sporządź opinię prawną {DLA_KOGO[u['dla_kogo']]} w sprawie: {nazwa}. Przedmiot zamówienia: {PRZEDMIOTY[u['przedmiot']]}; tryb: {TRYBY[u['tryb']]}.
{('Pytania klienta: ' + u['pytania_klienta']) if u.get('pytania_klienta') else ''}
Ustalenia ze sprawdzenia dokumentacji (podsumowanie: {w.get('podsumowanie', '')}):
{json.dumps(uw, ensure_ascii=False)}

Zwróć JSON:
{{"przedmiot_opinii": "1–2 zdania: czego dotyczy opinia",
  "stan_faktyczny": "3–6 zdań: jakie dokumenty i jakie postępowanie (przedmiot, tryb, rozpoznane okoliczności)",
  "analiza": [{{"zagadnienie": "krótki tytuł", "ocena": "analiza prawna 2–6 zdań", "podstawa": "przepisy", "rekomendacja": "co zrobić"}}],
  "odpowiedzi_na_pytania": [{{"pytanie": "…", "odpowiedz": "…"}}],
  "wnioski": ["wniosek końcowy 1", "…"],
  "zastrzezenia": "1–3 zdania: zakres i ograniczenia opinii"}}
Zagadnienia uporządkuj od najpoważniejszych. Połącz uwagi o tym samym problemie w jedno zagadnienie."""


def opinia_docx(sciezka, nazwa, u, op, autor=""):
    """Opinia prawna jako pismo; miejsca do uzupełnienia oznaczone [UZUPEŁNIJ …] (na żółto)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(f"{autor or '[UZUPEŁNIJ: kancelaria / radca prawny – nazwa i adres]'}", rozmiar=9)
    A(f"[UZUPEŁNIJ: miejscowość], {dt.date.today().strftime('%d.%m.%Y')} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A(f"{u.get('klient') or '[UZUPEŁNIJ: adresat opinii]'}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("OPINIA PRAWNA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"w sprawie: {nazwa}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"({DLA_KOGO[u['dla_kogo']]}; przedmiot: {PRZEDMIOTY[u['przedmiot']].lower()}; tryb: {TRYBY[u['tryb']]})", rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    d.add_heading("I. Przedmiot opinii", level=2)
    A(op.get("przedmiot_opinii", ""))
    d.add_heading("II. Stan faktyczny", level=2)
    A(op.get("stan_faktyczny", ""))
    d.add_heading("III. Analiza prawna", level=2)
    for i, z in enumerate(op.get("analiza") or [], 1):
        A(f"{i}. {z.get('zagadnienie', '')}", pogrub=True)
        A(z.get("ocena", ""))
        if z.get("podstawa"):
            A(f"Podstawa prawna: {z['podstawa']}", kursywa=True, rozmiar=9)
        if z.get("rekomendacja"):
            A(f"Rekomendacja: {z['rekomendacja']}")
    if op.get("odpowiedzi_na_pytania"):
        d.add_heading("IV. Odpowiedzi na pytania", level=2)
        for x in op["odpowiedzi_na_pytania"]:
            A(f"Pytanie: {x.get('pytanie', '')}", pogrub=True)
            A(x.get("odpowiedz", ""))
    d.add_heading(("V." if op.get("odpowiedzi_na_pytania") else "IV.") + " Wnioski", level=2)
    for i, w_ in enumerate(op.get("wnioski") or [], 1):
        A(f"{i}. {w_}")
    A(op.get("zastrzezenia") or "", kursywa=True, rozmiar=9)
    A("Opinię przygotowano z pomocą AI na podstawie przekazanych dokumentów; wymaga weryfikacji i podpisu radcy prawnego / adwokata.", kursywa=True, rozmiar=8)
    A("\n[UZUPEŁNIJ: imię i nazwisko, tytuł zawodowy, nr wpisu]\n……………………………………\n(podpis)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# ---------------------------------------------------------------- sprawdzenie ofert: raport, projekt odwołania
# tryby tylko od progów unijnych / tylko poniżej; partnerstwo innowacyjne, negocjacje bez ogłoszenia, wolna ręka i zamówienia sektorowe
# występują w obu reżimach (np. art. 208 i art. 301, art. 213 i art. 305) – termin zależy wtedy od wartości zamówienia
TRYBY_UNIJNE = ("przetarg_nieograniczony", "przetarg_ograniczony", "negocjacje_z_ogloszeniem", "dialog", "unijny")
TRYBY_KRAJOWE = ("podstawowy_1", "podstawowy_2", "podstawowy_3", "krajowy")


def unijny(tryb):
    """True – od progów unijnych, False – poniżej, None – zależy od wartości (tryb występujący w obu reżimach albo nieustalony)."""
    return True if tryb in TRYBY_UNIJNE else False if tryb in TRYBY_KRAJOWE else None


def wpis_opis(przedmiot, tryb):
    """Wpis od odwołania (§ 2 ust. 1 rozporządzenia PRM z 31.12.2020 r., Dz.U. 2020 poz. 2437) – kwota według przedmiotu i reżimu."""
    import odwolania_przetargi as OP
    u = unijny(tryb)
    kw = lambda x: PR.liczba_pl(OP.wpis_odwolania(przedmiot, x), 0) + " zł"
    if u is None:
        return f"{kw(False)} (poniżej progów unijnych) albo {kw(True)} (od progów unijnych) – [UZUPEŁNIJ: wybierz według wartości zamówienia]"
    return kw(u) + (" (od progów unijnych)" if u else " (poniżej progów unijnych)")


def termin_odwolania(tryb):
    """Art. 515 Pzp (sprawdzone 21.10.2026): progi unijne – 10 dni (informacja elektroniczna) / 15 dni; poniżej progów – 5 / 10 dni."""
    if tryb in ("ponizej_progu", "zasada_konkurencyjnosci"):
        return ("odwołanie do KIO nie przysługuje – zamówienie poza Pzp; pozostaje droga cywilna"
                + (" i skarga do instytucji udzielającej dofinansowania (korekta finansowa)" if tryb == "zasada_konkurencyjnosci" else ""))
    if tryb in TRYBY_UNIJNE:
        return "10 dni od przekazania informacji o czynności zamawiającego środkami komunikacji elektronicznej (15 dni – w inny sposób), art. 515 ust. 1 pkt 1 Pzp"
    if tryb in TRYBY_KRAJOWE:
        return "5 dni od przekazania informacji o czynności zamawiającego środkami komunikacji elektronicznej (10 dni – w inny sposób), art. 515 ust. 1 pkt 2 Pzp"
    return ("od progów unijnych: 10 dni (elektronicznie) / 15 dni; poniżej progów: 5 dni (elektronicznie) / 10 dni – art. 515 ust. 1 Pzp "
            "[UZUPEŁNIJ: ustal wartość zamówienia i sposób przekazania informacji]")


SYSTEM_ODWOLANIE = (PR.INFO_AI + " Jesteś radcą prawnym specjalizującym się w postępowaniach przed Krajową Izbą Odwoławczą. Przygotowujesz projekt "
                    "odwołania WYŁĄCZNIE na podstawie przekazanych ustaleń z badania ofert; nie dodajesz faktów. Każdy zarzut ma podstawę prawną. "
                    "Gdy ustalenia nie dają podstaw do zarzutu – piszesz to wprost. Odpowiadasz wyłącznie JSON-em.")


def polecenie_odwolania(u, nazwa, w, O):
    oferty = [{"nazwa": o.get("nazwa"), "miejsce": o.get("miejsce"), "punkty": o.get("punkty"), "cena_brutto": (o.get("wynik") or {}).get("cena_brutto"),
               "status": (o.get("wynik") or {}).get("status"), "rynkowosc": (o.get("rynkowosc") or {}).get("klasyfikacja")} for o in O.get("oferty") or []]
    return f"""Przygotuj projekt odwołania do Prezesa Krajowej Izby Odwoławczej dla wykonawcy ({u.get('klient') or '[UZUPEŁNIJ: odwołujący]'}) w postępowaniu: {nazwa}.
Przedmiot: {PRZEDMIOTY[u['przedmiot']]}; tryb: {TRYBY[u['tryb']]}. Oferty i ranking: {json.dumps(oferty, ensure_ascii=False)}
Ustalenia z badania ofert (niezgodności, braki, rażąco niska cena, błędy): {json.dumps(w.get('uwagi') or [], ensure_ascii=False)[:12000]}
Typowe zarzuty: zaniechanie odrzucenia oferty niezgodnej z warunkami zamówienia (art. 226 ust. 1 pkt 5), z rażąco niską ceną (art. 226 ust. 1 pkt 8),
zaniechanie wezwania do wyjaśnień ceny (art. 224 ust. 1 / ust. 2 pkt 1), błędy w ocenie ofert, naruszenie art. 16 – tylko gdy wynikają z ustaleń.
Zwróć JSON:
{{"czynnosc": "czynność / zaniechanie zamawiającego, na które wnosi się odwołanie",
  "zarzuty": [{{"przepis": "art. … Pzp", "tresc": "zarzut naruszenia – jednym zdaniem"}}],
  "zadania": ["żądanie (np. unieważnienia wyboru, powtórzenia badania i oceny ofert, odrzucenia oferty …)"],
  "interes": "interes we wniesieniu odwołania i możliwość poniesienia szkody (art. 505 ust. 1 Pzp)",
  "uzasadnienie": [{{"zarzut": "nr / skrót", "tresc": "uzasadnienie faktyczne i prawne 3–8 zdań"}}],
  "dowody": ["dowód (np. oferta wykonawcy X – formularz cenowy, poz. …)"],
  "ocena_szans": "1–3 zdania: realna ocena szans i ryzyk (wpis, koszty)"}}"""


def odwolanie_docx(sciezka, nazwa, u, od):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(f"[UZUPEŁNIJ: miejscowość], {dt.date.today().strftime('%d.%m.%Y')} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("Prezes Krajowej Izby Odwoławczej\nul. Postępu 17a, 02-676 Warszawa [sprawdź aktualny adres / wniesienie elektroniczne]", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A(f"Odwołujący: {u.get('klient') or '[UZUPEŁNIJ: nazwa, adres, NIP, KRS odwołującego]'}\nPełnomocnik: [UZUPEŁNIJ: radca prawny / adwokat, adres do doręczeń]")
    A("Zamawiający: [UZUPEŁNIJ: nazwa i adres zamawiającego]")
    A(f"Postępowanie: {nazwa} – [UZUPEŁNIJ: numer ogłoszenia / znak sprawy]; tryb: {TRYBY[u['tryb']]}")
    A(f"Wartość zamówienia: [UZUPEŁNIJ] · Wpis od odwołania: {wpis_opis(u.get('przedmiot'), u.get('tryb'))} – wpłata na rachunek Urzędu Zamówień Publicznych "
      "najpóźniej do upływu terminu na wniesienie odwołania; dowód uiszczenia w załączeniu")
    A("ODWOŁANIE", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"od: {od.get('czynnosc') or '[UZUPEŁNIJ: czynność / zaniechanie zamawiającego]'}")
    A("Zamawiającemu zarzucam naruszenie:", pogrub=True)
    for i, z in enumerate(od.get("zarzuty") or [], 1):
        A(f"{i}. {z.get('przepis', '')} – {z.get('tresc', '')}")
    A("W związku z powyższym wnoszę o nakazanie zamawiającemu:", pogrub=True)
    for i, z in enumerate(od.get("zadania") or [], 1):
        A(f"{i}. {z}")
    A("Interes we wniesieniu odwołania", pogrub=True)
    A(od.get("interes") or "[UZUPEŁNIJ]")
    if u["tryb"] in ("ponizej_progu", "zasada_konkurencyjnosci"):
        A(f"UWAGA: {termin_odwolania(u['tryb'])} – [UZUPEŁNIJ: sprawdź wartość zamówienia; projekt odwołania ma zastosowanie tylko do zamówienia objętego Pzp].")
    else:
        A(f"Termin: odwołanie wnosi się w terminie {termin_odwolania(u['tryb'])}. Informację o czynności przekazano: [UZUPEŁNIJ: data i sposób]. "
          "Kopię odwołania przekazuje się zamawiającemu przed upływem terminu (art. 514 ust. 2 Pzp).")
    d.add_heading("Uzasadnienie", level=2)
    for z in od.get("uzasadnienie") or []:
        A(str(z.get("zarzut", "")), pogrub=True)
        A(z.get("tresc", ""))
    if od.get("dowody"):
        A("Dowody:", pogrub=True)
        for x in od["dowody"]:
            A(f"– {x}")
    A("Załączniki: dowód uiszczenia wpisu, pełnomocnictwo, dowód przekazania kopii odwołania zamawiającemu, [UZUPEŁNIJ: dowody].")
    A("\n[UZUPEŁNIJ: podpis kwalifikowany pełnomocnika]", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    if od.get("ocena_szans"):
        d.add_heading("Notatka dla klienta (usuń przed wniesieniem)", level=3)
        A(od["ocena_szans"], kursywa=True)
    A("Projekt przygotowany z pomocą AI na podstawie ustaleń z badania ofert – wymaga weryfikacji i podpisu pełnomocnika.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def raport_ofert_docx(sciezka, nazwa, u, O):
    """Raport z badania ofert (bez AI): zgodność z zamówieniem, ranking i rynkowość ceny każdej oferty."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("RAPORT Z BADANIA OFERT", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{nazwa} · {PRZEDMIOTY[u['przedmiot']]} · {TRYBY[u['tryb']]} · {DLA_KOGO[u['dla_kogo']]}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER, rozmiar=9)
    swz = O.get("swz") or {}
    A(f"Wartość zamówienia z VAT (art. 224 ust. 2 pkt 1): {swz.get('wartosc_zam_brutto') or '[UZUPEŁNIJ – brak; porównanie tylko ze średnią ofert]'}; "
      f"kwota przeznaczona na sfinansowanie: {swz.get('kwota_budzet_brutto') or '–'}.")
    for o in sorted(O.get("oferty") or [], key=lambda x: x.get("miejsce") or 99):
        w, r = o.get("wynik") or {}, o.get("rynkowosc") or {}
        d.add_heading(f"{o.get('nr', '')}. {o.get('nazwa', '')}" + (f" – miejsce {o['miejsce']}, {o.get('punkty')} pkt" if o.get("miejsce") else ""), level=2)
        A(f"Cena brutto: {w.get('cena_brutto') or '–'} · status badania: {w.get('status') or 'nie zbadano'}")
        for k, t in (("niezgodnosci", "Niezgodności z warunkami zamówienia"), ("braki", "Braki / do uzupełnienia"), ("bledy_rachunkowe", "Błędy rachunkowe"),
                     ("do_wyjasnienia", "Do wyjaśnienia")):
            L = [x for x in w.get(k) or [] if isinstance(x, dict)]
            if L:
                A(t + ":", pogrub=True)
                for x in L:
                    A(f"– {x.get('opis', '')}" + (f" ({x.get('dokument', '')} {x.get('miejsce', '')})" if x.get("dokument") else ""))
        if w.get("podstawa_odrzucenia"):
            A(f"Podstawa odrzucenia: {w['podstawa_odrzucenia']}", pogrub=True)
        if r:
            A(f"Rynkowość ceny: {r.get('klasyfikacja', '').upper()}" + (f" ({r['podstawa']})" if r.get("podstawa") else ""), pogrub=True)
            A((r.get("art224") or {}).get("opis", ""))
            if r.get("inzynieria_cenowa"):
                A(r["inzynieria_cenowa"])
            if r.get("koszty_pracy"):
                A(r["koszty_pracy"]["opis"])
            if r.get("pozycje"):
                A(f"Pozycje porównane z rynkiem ({r.get('zakres', '')}; {r.get('sprawdzono_pozycji', '')} z {r.get('pozycji_oferty', '')}):", rozmiar=9)
                t = d.add_table(rows=1, cols=6)
                try:
                    t.style = "Table Grid"
                except Exception:
                    pass
                for c_, h in zip(t.rows[0].cells, ("Poz.", "Opis", "Cena jedn. oferty", "Rynek (typowa)", "Odchylenie", "Ocena")):
                    c_.text = h
                for p in r["pozycje"]:
                    for c_, v in zip(t.add_row().cells, (p["lp"], str(p["opis"])[:80], f"{p['cena_jedn']:.2f}", f"{p['rynek_typowa']:.2f}", f"{p['odchylenie_proc']}%", p["flaga"])):
                        c_.text = str(v)
            A(r.get("zastrzezenie", ""), kursywa=True, rozmiar=8)
    A("Raport przygotowany przez program z wyników badania ofert (AI) i porównania z cenami rynkowymi – wymaga weryfikacji.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
