# -*- coding: utf-8 -*-
"""Beneficjent dotacji UE / KPO: wybór wykonawcy zgodnie z zasadą konkurencyjności – od zapytania ofertowego,
przez publikację w Bazie Konkurencyjności i ocenę ofert, do protokołu dołączanego do rozliczenia dotacji."""
import datetime as dt

import modul_oferty as MO
import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

PROG_ZK = PR.PROG_ZK  # zasada konkurencyjności – zamówienia powyżej 80 000 zł netto (Wytyczne dot. kwalifikowalności 2021–2027, od 25.03.2025)

SYSTEM_ZAP = (PR.INFO_AI + " " + "Jesteś ekspertem od zamówień w projektach współfinansowanych z UE (Wytyczne dotyczące kwalifikowalności wydatków "
              "na lata 2021–2027, zasada konkurencyjności) i KPO. Przygotowujesz zapytanie ofertowe, które przejdzie kontrolę instytucji "
              "pośredniczącej: jednoznaczny opis przedmiotu bez wskazywania marek (lub z „lub równoważny”), proporcjonalne warunki "
              "udziału, kryteria z wagami i sposobem oceny, terminy zgodne z wytycznymi. Nie zmyślasz danych – brak = [UZUPEŁNIJ]. "
              "Odpowiadasz WYŁĄCZNIE JSON-em.")


def _f(x):
    return liczba(x, 0.0)


def wymagania(d):
    """Co obowiązuje to zamówienie (próg, tryb, minimalny termin składania ofert) – reguły, bez AI."""
    w = _f(d.get("wartosc_netto"))
    rodz = d.get("rodzaj") or "roboty"
    pzp = bool(d.get("zamawiajacy_pzp"))
    unijne = bool(d.get("progi_unijne"))
    prog = PR.prog_pzp(d.get("data_wszczecia"))
    if pzp and w >= prog:
        tryb = "pzp"
        opis = (f"Beneficjent jest zamawiającym w rozumieniu Pzp, a wartość zamówienia osiąga próg {PR.zl(prog)} netto – stosuje się ustawę Pzp "
                "(postępowanie w BZP / e-Zamówienia), nie Bazę Konkurencyjności."
                + (" (Próg 130 000 zł – postępowanie wszczęte przed 1.01.2026.)" if prog != PR.PROG_PZP else ""))
    elif PR.wymaga_zk(w, d.get("data_wszczecia")):
        tryb = "zk"
        opis = (f"Wartość przekracza {PR.zl(PR.prog_zk(d.get('data_wszczecia')))} netto – obowiązuje zasada konkurencyjności: zapytanie ofertowe "
                "publikowane w Bazie Konkurencyjności.")
    elif w > 0:
        tryb = "ponizej"
        opis = (f"Wartość nie przekracza {PR.zl(PR.prog_zk(d.get('data_wszczecia')))} netto – zasada konkurencyjności nie jest wymagana. Sprawdź umowę o dofinansowanie i zachowaj "
                "dokumentację wyboru (np. rozeznanie rynku), jeśli wymaga jej instytucja.")
    else:
        tryb, opis = "", "Podaj szacunkową wartość zamówienia netto, aby program ustalił tryb."
    dni = 30 if unijne else (14 if rodz == "roboty" else 7)
    ostrzezenia = []
    if d.get("czesci_innych_zakupow"):
        ostrzezenia.append("Sprawdź, czy zamówienie nie jest częścią większego, tożsamego zakupu w projekcie – dzielenie zamówienia w celu "
                           "uniknięcia zasady konkurencyjności jest naruszeniem (korekta finansowa).")
    return {"tryb": tryb, "opis": opis, "min_dni": dni,
            "min_dni_opis": (f"Termin składania ofert co najmniej {dni} dni od dnia następującego po publikacji w Bazie Konkurencyjności"
                             + (" (zamówienie o wartości od progów unijnych)." if unijne else " (roboty budowlane)." if rodz == "roboty" else " (dostawy / usługi).")),
            "ostrzezenia": ostrzezenia,
            "lista": [  # lista kontrolna kontroli instytucji – to, co najczęściej kończy się korektą finansową
                ("opis", "Opis przedmiotu bez wskazania marki / producenta (albo z „lub równoważny” i kryteriami równoważności)"),
                ("warunki", "Warunki udziału proporcjonalne do przedmiotu i wartości zamówienia"),
                ("kryteria", "Kryteria oceny z wagami i opisem sposobu przyznawania punktów"),
                ("termin", "Termin składania ofert nie krótszy niż minimalny"),
                ("publikacja", "Publikacja zapytania w Bazie Konkurencyjności (numer ogłoszenia)"),
                ("powiazania", "Oświadczenia o braku powiązań osobowych lub kapitałowych (wykonawcy i osoby oceniające)"),
                ("protokol", "Protokół z postępowania z oceną wszystkich ofert"),
                ("wynik", "Informacja o wyniku opublikowana w Bazie Konkurencyjności"),
                ("umowa", "Umowa w formie pisemnej, zmiany umowy tylko w przypadkach przewidzianych w zapytaniu")]}


def polecenie(d, dot):
    return (f"Przygotuj ZAPYTANIE OFERTOWE (zasada konkurencyjności) dla zamówienia w projekcie dotacyjnym.\n"
            f"Beneficjent: {d.get('beneficjent') or '[UZUPEŁNIJ]'}. Projekt: {dot.get('nazwa') or '[UZUPEŁNIJ]'}"
            f"{(' (umowa ' + dot['nr_umowy'] + ')') if dot.get('nr_umowy') else ''}. Program: {dot.get('program') or '[UZUPEŁNIJ]'}.\n"
            f"Rodzaj zamówienia: {d.get('rodzaj')}. Przedmiot: {d.get('przedmiot')}. Opis potrzeb: {d.get('opis') or ''}.\n"
            f"Szacunkowa wartość netto: {d.get('wartosc_netto')} zł. Termin realizacji: {d.get('termin_realizacji') or '[UZUPEŁNIJ]'}.\n"
            f"Minimalny termin składania ofert: {wymagania(d)['min_dni']} dni od publikacji.\n"
            'Zwróć JSON: {"tytul": "Zapytanie ofertowe nr … – …", "sekcje": [{"naglowek": "1. Zamawiający", "tresc": "…"}, '
            '{"naglowek": "2. Tryb udzielenia zamówienia", "tresc": "…"}, {"naglowek": "3. Opis przedmiotu zamówienia (z kodami CPV)", "tresc": "…"}, '
            '{"naglowek": "4. Termin realizacji", "tresc": "…"}, {"naglowek": "5. Warunki udziału i sposób ich oceny", "tresc": "…"}, '
            '{"naglowek": "6. Wykluczenia (powiązania osobowe lub kapitałowe, sankcje)", "tresc": "…"}, '
            '{"naglowek": "7. Kryteria oceny ofert, wagi i sposób przyznawania punktów", "tresc": "…"}, '
            '{"naglowek": "8. Termin i sposób składania ofert (Baza Konkurencyjności)", "tresc": "…"}, '
            '{"naglowek": "9. Warunki zmiany umowy", "tresc": "…"}, {"naglowek": "10. Załączniki", "tresc": "…"}], '
            '"kryteria": [{"nazwa": "Cena", "waga": 60, "typ": "min", "opis": "…"}], "warunki_udzialu": ["…"], '
            '"wymagane_dokumenty": ["Formularz ofertowy", "Oświadczenie o braku powiązań osobowych lub kapitałowych", "…"], '
            '"ryzyka": ["zapis, który instytucja może zakwestionować – i jak go poprawić"]}')


def _naglowek(d, tytul):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = MO._doc()
    MO._akapit(doc, f"{dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(doc, d.get("beneficjent") or "[UZUPEŁNIJ: beneficjent]", pogrub=True)
    MO._akapit(doc, tytul, pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    return doc


def zapytanie_docx(sciezka, d, z):
    doc = _naglowek(d, z.get("tytul") or "ZAPYTANIE OFERTOWE")
    MO._akapit(doc, "Postępowanie prowadzone zgodnie z zasadą konkurencyjności (Wytyczne dotyczące kwalifikowalności wydatków na lata 2021–2027).",
               kursywa=True, rozmiar=9)
    for s in z.get("sekcje") or []:
        MO._akapit(doc, str(s.get("naglowek") or ""), pogrub=True)
        for akapit in str(s.get("tresc") or "").split("\n"):
            if akapit.strip():
                MO._akapit(doc, akapit.strip())
    doc.save(sciezka)


def formularz_docx(sciezka, d, z):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = _naglowek(d, "FORMULARZ OFERTOWY")
    MO._akapit(doc, f"dotyczy: {z.get('tytul') or d.get('przedmiot') or ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    for t in ("Nazwa wykonawcy: ..............................................................", "Adres: ........................................................................",
              "NIP: ....................................  e-mail / telefon: ......................................",
              "Oferujemy wykonanie przedmiotu zamówienia za cenę netto: ..................... zł, VAT: ......... zł, brutto: ..................... zł."):
        MO._akapit(doc, t)
    import ocena_ofert as OO  # kryterium ceny rozpoznawane tak samo jak w ocenie ofert („Ocena koncepcji” to nie cena)
    kr = [k for k in z.get("kryteria") or [] if isinstance(k, dict) and not OO.jest_cena(k)]
    for k in kr:
        MO._akapit(doc, f"{k.get('nazwa')}: ....................................")
    MO._akapit(doc, "Oświadczamy, że zapoznaliśmy się z zapytaniem ofertowym, akceptujemy jego warunki i jesteśmy związani ofertą przez 30 dni.")
    MO._akapit(doc, "\n\n..........................................\n(podpis wykonawcy)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    doc.save(sciezka)


def powiazania_docx(sciezka, d, dla_komisji=False):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = _naglowek(d, "OŚWIADCZENIE O BRAKU POWIĄZAŃ OSOBOWYCH LUB KAPITAŁOWYCH")
    kto = "osoby wykonującej w imieniu beneficjenta czynności związane z wyborem wykonawcy" if dla_komisji else "wykonawcy"
    MO._akapit(doc, f"Oświadczam jako {kto}, że nie jestem powiązany(-a) z beneficjentem / wykonawcą osobowo lub kapitałowo, w szczególności przez: "
                    "uczestnictwo w spółce jako wspólnik spółki cywilnej lub osobowej; posiadanie co najmniej 10% udziałów lub akcji; pełnienie funkcji "
                    "członka organu nadzorczego lub zarządzającego, prokurenta, pełnomocnika; pozostawanie w związku małżeńskim, w stosunku pokrewieństwa "
                    "lub powinowactwa w linii prostej, pokrewieństwa lub powinowactwa w linii bocznej do drugiego stopnia, w związku z przysposobieniem, "
                    "opieką lub kuratelą albo we wspólnym pożyciu; pozostawanie w stosunku pracy lub zlecenia.")
    MO._akapit(doc, "Treść oświadczenia należy porównać z wymaganiami umowy o dofinansowanie i aktualnych wytycznych programu.", kursywa=True, rozmiar=8)
    MO._akapit(doc, "\n\n..........................................\n(data i podpis)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    doc.save(sciezka)


def protokol_docx(sciezka, d, pub, oc, dot):
    """Protokół z postępowania – do dokumentacji projektu i wniosku o płatność."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = _naglowek(d, "PROTOKÓŁ Z POSTĘPOWANIA O UDZIELENIE ZAMÓWIENIA")
    MO._akapit(doc, "prowadzonego zgodnie z zasadą konkurencyjności", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    wiersze = [["Projekt", f"{dot.get('nazwa') or '[UZUPEŁNIJ]'}{(' – umowa ' + dot['nr_umowy']) if dot.get('nr_umowy') else ''}"],
               ["Przedmiot zamówienia", d.get("przedmiot") or ""], ["Rodzaj", d.get("rodzaj") or ""],
               ["Szacunkowa wartość netto", MO.zl(_f(d.get("wartosc_netto")))], ["Data ustalenia wartości", d.get("data_szacowania") or "[UZUPEŁNIJ]"],
               ["Publikacja w Bazie Konkurencyjności", f"nr {pub.get('numer') or '[UZUPEŁNIJ]'} z dnia {pub.get('data') or '[UZUPEŁNIJ]'}"],
               ["Termin składania ofert", pub.get("termin") or "[UZUPEŁNIJ]"],
               ["Zmiany zapytania / pytania wykonawców", pub.get("zmiany") or "brak"]]
    MO._tabela(doc, [["Element", "Dane"]] + wiersze)
    oferty = (oc or {}).get("oferty") or []
    if oferty:
        MO._akapit(doc, "Złożone oferty i ich ocena", pogrub=True)
        kr = [k.get("nazwa", "") for k in ((oc.get("swz") or {}).get("kryteria") or [])]
        MO._tabela(doc, [["Nr", "Wykonawca", "Cena brutto", "Status"] + kr + ["Punkty", "Miejsce"]] +
                   [[str(o.get("nr")), o.get("nazwa", ""), MO.zl(_f((o.get("wynik") or {}).get("cena_brutto"))),
                     "odrzucona" if o.get("odrzucona") else (o.get("wynik") or {}).get("status", "–")]
                    + [f"{(o.get('punkty_szczegoly') or {}).get(k, 0):.2f}" for k in kr] + [f"{o.get('punkty', 0):.2f}", str(o.get("miejsce") or "–")] for o in oferty])
        naj = next((o for o in oferty if o.get("id") == (oc.get("podsum") or {}).get("najkorzystniejsza")), None)
        MO._akapit(doc, f"Wybrana oferta: {naj['nazwa'] + ' – ' + format(naj.get('punkty', 0), '.2f') + ' pkt' if naj else '[UZUPEŁNIJ]'}.", pogrub=True)
        odrz = [o for o in oferty if not o.get("miejsce")]
        for o in odrz:
            MO._akapit(doc, f"Oferta odrzucona – {o.get('nazwa')}: {(o.get('wynik') or {}).get('podstawa_odrzucenia') or '[UZUPEŁNIJ: uzasadnienie]'}")
    else:
        MO._akapit(doc, "Złożone oferty: [UZUPEŁNIJ – wykonawcy, ceny, punktacja; albo informacja, że nie złożono ofert]")
    MO._akapit(doc, "Załączniki: zapytanie ofertowe, potwierdzenie publikacji w Bazie Konkurencyjności, złożone oferty, oświadczenia o braku "
                    "powiązań (wykonawców i osób oceniających), informacja o wyniku opublikowana w Bazie Konkurencyjności, umowa z wykonawcą.")
    MO._akapit(doc, "\n\nPodpisy osób dokonujących oceny: .........................................     Zatwierdził: .........................................")
    doc.save(sciezka)
