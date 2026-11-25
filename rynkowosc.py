# -*- coding: utf-8 -*-
"""
Rynkowość ceny oferty – wspólny mechanizm dla zamawiającego (badanie ofert) i prawnika (sprawdzenie ofert w przetargu).

Trzy poziomy:
1) cena całkowita – BEZ AI: art. 224 ust. 2 pkt 1 Pzp – cena niższa o co najmniej 30% od wartości zamówienia powiększonej
   o VAT (ustalonej przed wszczęciem) albo od średniej arytmetycznej cen ofert niepodlegających odrzuceniu → obowiązkowe wezwanie
   do wyjaśnień (chyba że rozbieżność wynika z okoliczności oczywistych);
2) pozycje oferty a rynek – pozycje tworzące 80% wartości (domyślnie) albo wszystkie; ceny rynkowe z internetu (ceny ofertowe,
   nie transakcyjne); roboty – także „inżynieria cenowa”; usługi – koszty pracy (płaca minimalna, stawka godzinowa);
3) ocena: rażąco niska (obowiązkowe wezwanie) / niska – do wyjaśnienia (art. 224 ust. 1) / rynkowa / zawyżona.
Wynik to materiał dla komisji lub prawnika – nie rozstrzygnięcie.

Parametry sprawdzone w źródłach (21.10.2026): art. 224 ust. 2 pkt 1 – próg 30%; płaca minimalna 2026 – 4806 zł brutto;
minimalna stawka godzinowa 2026 – 31,40 zł brutto.
"""
import datetime as dt
import json
import re

import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

PROG_224 = 0.30
PLACA_MIN_2026 = 4806.00
STAWKA_GODZ_2026 = 31.40
# płaca minimalna i minimalna stawka godzinowa wg rozporządzeń RM. 2027: 4950 zł / 32,30 zł – rozporządzenie Rady Ministrów z 14 września 2026 r.
# w sprawie wysokości minimalnego wynagrodzenia za pracę oraz wysokości minimalnej stawki godzinowej w 2027 r. (Dz.U. 2026 poz. 1213, § 1 i § 2),
# tekst sprawdzony 24.11.2026: https://eli.gov.pl/api/acts/DU/2026/1213/text/O/D20261213.pdf;
# dla lat bez rozporządzenia – ostatnia znana wartość (z uwagą)
PLACA_MIN = {2026: 4806.00, 2027: 4950.00}
STAWKA_GODZ = {2026: 31.40, 2027: 32.30}


def placa_min(rok=None):
    rok = rok or dt.date.today().year
    return PLACA_MIN.get(rok) or PLACA_MIN[max(k for k in PLACA_MIN if k <= rok)] if rok >= min(PLACA_MIN) else PLACA_MIN[min(PLACA_MIN)]


def _lata_okresu(od, mies):
    """Rok każdego miesiąca okresu umowy (od – data początku, domyślnie dziś; mies – liczba miesięcy, najwyżej 120)."""
    try:
        d = dt.date.fromisoformat(str(od)[:10]) if od else dt.date.today()
    except ValueError:
        d = dt.date.today()
    n = min(120, max(1, int(round(mies or 12))))
    return d, [(d.year + (d.month - 1 + i) // 12) for i in range(n)]


def stawka_godz_min(rok=None):
    """Minimalna stawka godzinowa (umowy zlecenia) w roku – jak placa_min: rok bez rozporządzenia – ostatnia znana kwota."""
    rok = rok or dt.date.today().year
    return STAWKA_GODZ.get(rok) or (STAWKA_GODZ[max(k for k in STAWKA_GODZ if k <= rok)] if rok >= min(STAWKA_GODZ) else STAWKA_GODZ[min(STAWKA_GODZ)])


def placa_min_okresu(od, mies):
    """Średnia płaca minimalna w okresie świadczenia usługi (np. kwiecień 2027 – marzec 2028) i uwaga, gdy dla części okresu nie ma
    jeszcze rozporządzenia (przyjęto ostatnią znaną kwotę – realnie będzie wyższa)."""
    d, lata = _lata_okresu(od, mies)
    n = len(lata)
    sr = round(sum(placa_min(r) for r in lata) / n, 2)
    brak = sorted({r for r in lata if r > max(PLACA_MIN)})
    uwaga = (f"Dla {', '.join(map(str, brak))} r. nie ma jeszcze rozporządzenia o płacy minimalnej – przyjęto {PR.liczba_pl(PLACA_MIN[max(PLACA_MIN)])} zł "
             "(realnie będzie wyższa; uwzględnij to w cenie albo w klauzuli waloryzacyjnej, art. 436 pkt 4 lit. b Pzp).") if brak else ""
    return sr, uwaga
NARZUT_PRACODAWCY = 1.2048  # koszt pracodawcy ≈ płaca × ok. 1,2048 (składki ZUS pracodawcy, FP, FGŚP, PPK pominięte) – szacunek do sprawdzenia
VAT_DOMYSLNY = 0.23


def _f(x):
    return liczba(x, None, 2)


def prog_224(cena_brutto, wartosc_zam_brutto, ceny_ofert_brutto):
    """Art. 224 ust. 2 pkt 1 Pzp – wyliczenie bez AI. ceny_ofert_brutto: ceny ofert niepodlegających odrzuceniu (z badaną)."""
    c = _f(cena_brutto)
    if not c:
        return {"ocena": "brak ceny", "obowiazkowe": False, "opis": "Brak ceny całkowitej oferty – nie można policzyć progu z art. 224 ust. 2."}
    ceny = [x for x in (_f(y) for y in ceny_ofert_brutto or []) if x]
    srednia = round(sum(ceny) / len(ceny), 2) if ceny else None
    w = _f(wartosc_zam_brutto)
    wyn = {"cena": c, "srednia": srednia, "wartosc_brutto": w, "obowiazkowe": False, "podstawy": []}
    import ocena_ofert as OO  # porównanie w groszach – ta sama funkcja co ranking ofert
    if w:
        r = round((w - c) / w * 100, 1)
        wyn["roznica_wartosc_proc"] = r
        if OO.ponizej_30(c, [w]):
            wyn["obowiazkowe"] = True
            wyn["podstawy"].append(PR.pl_liczby(f"cena {c:,.2f} zł jest niższa o {r}% od wartości zamówienia z VAT {w:,.2f} zł (próg 30%: {w * 0.7:,.2f} zł)"))
    if srednia and len(ceny) >= 2:
        r = round((srednia - c) / srednia * 100, 1)
        wyn["roznica_srednia_proc"] = r
        if OO.ponizej_30(c, ceny):
            wyn["obowiazkowe"] = True
            wyn["podstawy"].append(PR.pl_liczby(f"cena {c:,.2f} zł jest niższa o {r}% od średniej cen ofert {srednia:,.2f} zł (próg 30%: {srednia * 0.7:,.2f} zł)"))
    if wyn["obowiazkowe"]:
        wyn["opis"] = ("Obowiązkowe wezwanie do wyjaśnień (art. 224 ust. 2 pkt 1 Pzp), chyba że rozbieżność wynika z okoliczności oczywistych: "
                       + "; ".join(wyn["podstawy"]) + ".")
    else:
        wyn["opis"] = "Cena całkowita nie przekracza progu 30% z art. 224 ust. 2 pkt 1 Pzp" + (
            "" if w else " (wartość zamówienia z VAT nieznana – porównanie tylko ze średnią ofert)") + "."
    return wyn


def pareto(pozycje, prog=0.8):
    """Pozycje tworzące łącznie co najmniej `prog` wartości oferty (od największych)."""
    L = sorted([p for p in pozycje if _f(p.get("wartosc"))], key=lambda p: -_f(p["wartosc"]))
    razem = sum(_f(p["wartosc"]) for p in L) or 0
    wyn, suma = [], 0
    for p in L:
        if razem and suma >= prog * razem:
            break
        wyn.append(p)
        suma += _f(p["wartosc"])
    return wyn, (round(suma / razem * 100, 1) if razem else 0)


SYSTEM_POZYCJE = ("Odczytujesz z oferty w przetargu publicznym formularz cenowy / kosztorys ofertowy. Przepisujesz dokładnie, nie zgadujesz. "
                  "Odpowiadasz wyłącznie JSON-em.")


def polecenie_pozycji(przedmiot):
    dod = {"dostawy": ' "producent": "…", "model": "oferowany model / typ", ',
           "uslugi": ' "osoby": liczba osób albo null, "godziny": liczba godzin albo null, ',
           "roboty": " "}.get(przedmiot, " ")
    return ("Z oferty powyżej wypisz pozycje formularza cenowego albo kosztorysu ofertowego (wszystkie, w kolejności z dokumentu). Zwróć JSON:\n"
            '{"pozycje": [{"lp": "1", "opis": "…", "jm": "…", "ilosc": liczba,' + dod + '"cena_jedn": liczba netto, "wartosc": liczba netto}], '
            '"cena_netto": liczba, "cena_brutto": liczba, '
            '"zatrudnienie": {"osoby": liczba albo null, "etaty": liczba albo null, "okres_mies": liczba albo null, "umowa_o_prace": true/false/null, '
            '"opis": "co oferta mówi o personelu (usługi)"}, "uwagi": "…"}\n'
            "Kwoty jako liczby (kropka dziesiętna). Gdy oferta nie ma rozbicia na pozycje – pusta lista i cena całkowita.")


SYSTEM_RYNEK = ("Jesteś kosztorysantem i analitykiem cen w Polsce. Sprawdzasz w internecie AKTUALNE ceny rynkowe (2026 r.) – sklepy, hurtownie, "
                "cenniki, kosztorysy, ogłoszone wyniki przetargów. Podajesz tylko ceny ze znalezionych źródeł, z adresem. "
                "To są ceny ofertowe, nie transakcyjne. Odpowiadasz wyłącznie JSON-em.")


def polecenie_rynku(przedmiot, pozycje, region=""):
    co = {"roboty": "roboty budowlane (cena jednostkowa robocizny z materiałem i sprzętem, netto)", "dostawy": "produkty (cena netto za sztukę / jednostkę)",
          "uslugi": "usługi (stawka netto za jednostkę / godzinę / miesiąc)"}.get(przedmiot, "pozycje")
    L = [{"lp": p.get("lp"), "opis": str(p.get("opis", ""))[:200], "jm": p.get("jm"), "producent": p.get("producent"), "model": p.get("model")} for p in pozycje]
    return (f"Sprawdź aktualne ceny rynkowe w Polsce{(' – region: ' + region) if region else ''} dla pozycji – {co}:\n"
            f"{json.dumps(L, ensure_ascii=False)}\n"
            'Zwróć JSON: {"pozycje": [{"lp": "…", "cena_min": liczba, "cena_max": liczba, "cena_typowa": liczba, '
            '"zrodla": [{"nazwa": "…", "url": "https://…", "cena": liczba}], "uwagi": "np. inna jednostka, model zastępczy"}]}\n'
            "Ceny netto w zł za jednostkę z pozycji. Gdy nie znalazłeś wiarygodnych cen – pomiń pozycję, nie zgaduj.")


def ocen_pozycje(pozycje, rynek):
    """Odchylenie ceny jednostkowej oferty od ceny typowej rynku (%), dla pozycji z ceną rynkową."""
    rk = {str(r.get("lp")): r for r in rynek or [] if _f(r.get("cena_typowa"))}
    wyn = []
    for p in pozycje:
        r = rk.get(str(p.get("lp")))
        cj = _f(p.get("cena_jedn"))
        if not r or not cj:
            continue
        typ = _f(r["cena_typowa"])
        odch = round((cj - typ) / typ * 100, 1)
        wyn.append({"lp": p.get("lp"), "opis": p.get("opis"), "jm": p.get("jm"), "ilosc": p.get("ilosc"), "cena_jedn": cj, "wartosc": _f(p.get("wartosc")),
                    "rynek_min": _f(r.get("cena_min")), "rynek_max": _f(r.get("cena_max")), "rynek_typowa": typ, "odchylenie_proc": odch,
                    "zrodla": [z for z in r.get("zrodla") or [] if isinstance(z, dict) and str(z.get("url", "")).startswith("http")][:3],
                    "uwagi": str(r.get("uwagi") or "")[:200],
                    "flaga": "znacznie poniżej rynku" if odch <= -30 else "poniżej rynku" if odch <= -15 else "znacznie powyżej rynku" if odch >= 50 else
                    "powyżej rynku" if odch >= 20 else "rynkowa"})
    return wyn


def inzynieria_cenowa(oceny):
    """Roboty: pozycje znacznie zawyżone obok znacznie zaniżonych – możliwe przerzucanie cen (np. na roboty wykonywane wcześniej)."""
    gora = [o for o in oceny if o["odchylenie_proc"] >= 50]
    dol = [o for o in oceny if o["odchylenie_proc"] <= -40]
    if len(gora) >= 2 and len(dol) >= 2:
        return (f"Możliwa inżynieria cenowa: {len(gora)} pozycji co najmniej 50% powyżej rynku (np. {gora[0]['lp']}: {gora[0]['opis'][:60]}) "
                f"i {len(dol)} pozycji co najmniej 40% poniżej (np. {dol[0]['lp']}: {dol[0]['opis'][:60]}). Sprawdź kolejność wykonania i płatności.")
    return ""


def koszty_pracy(zatrudnienie, cena_netto, okres_mies=None, od=None):
    """Usługi: czy cena netto pokrywa minimalne koszty pracy zadeklarowanego personelu (umowa o pracę, płaca minimalna w okresie umowy)."""
    z = zatrudnienie or {}
    etaty = _f(z.get("etaty")) or _f(z.get("osoby"))
    mies = _f(z.get("okres_mies")) or _f(okres_mies)
    c = _f(cena_netto)
    if not (etaty and mies and c):
        return None
    pmin, _ = placa_min_okresu(od, mies)
    minimum = round(etaty * mies * pmin * NARZUT_PRACODAWCY, 2)
    return {"etaty": etaty, "okres_mies": mies, "minimum": minimum, "udzial_proc": round(minimum / c * 100, 1),
            "opis": PR.pl_liczby(f"Minimalne koszty pracy {etaty:g} etatu(-ów) × {mies:g} mies. × {pmin:,.2f} zł × narzut pracodawcy ≈ {minimum:,.2f} zł netto "
                     f"= {minimum / c * 100:.1f}% ceny oferty.")
            + (" Cena NIE pokrywa minimalnych kosztów pracy – podstawa do wezwania (art. 224 ust. 3 pkt 4 Pzp – zgodność z przepisami o kosztach pracy)."
               if minimum > c else " Pozostała część ceny musi pokryć inne koszty i zysk – oceń, czy to realne.")}


def klasyfikuj(p224, oceny, praca, przedmiot):
    if p224.get("obowiazkowe"):
        return "rażąco niska – obowiązkowe wezwanie", "art. 224 ust. 2 pkt 1 Pzp"
    if praca and praca["minimum"] > (p224.get("cena") or 0) / (1 + VAT_DOMYSLNY):
        return "niska – do wyjaśnienia", "art. 224 ust. 1 i ust. 3 pkt 4 Pzp (koszty pracy)"
    wart = sum(o["wartosc"] or 0 for o in oceny)
    nisko = sum(o["wartosc"] or 0 for o in oceny if o["odchylenie_proc"] <= -30)
    wysoko = sum(o["wartosc"] or 0 for o in oceny if o["odchylenie_proc"] >= 50)
    if wart and nisko / wart >= 0.25:
        return "niska – do wyjaśnienia", "art. 224 ust. 1 Pzp (istotne części składowe ceny)"
    r = p224.get("roznica_wartosc_proc")
    if (r is not None and r <= -20) or (wart and wysoko / wart >= 0.4):
        return "zawyżona", "porównanie z wartością zamówienia / rynkiem"
    return "rynkowa", ""


def ocena_oferty(cena_brutto, wartosc_brutto, ceny_ofert, pozycje, rynek, zatrudnienie, przedmiot, wybrane_proc):
    p224 = prog_224(cena_brutto, wartosc_brutto, ceny_ofert)
    oceny = ocen_pozycje(pozycje, rynek)
    praca = koszty_pracy(zatrudnienie, (_f(cena_brutto) or 0) / (1 + VAT_DOMYSLNY) if cena_brutto else None) if przedmiot == "uslugi" else None
    ic = inzynieria_cenowa(oceny) if przedmiot == "roboty" else ""
    kl, podst = klasyfikuj(p224, oceny, praca, przedmiot)
    return {"klasyfikacja": kl, "podstawa": podst, "art224": p224, "pozycje": oceny, "inzynieria_cenowa": ic, "koszty_pracy": praca,
            "zakres": f"pozycje tworzące {wybrane_proc}% wartości oferty" if wybrane_proc else "",
            "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "zastrzezenie": "Ceny z internetu to ceny ofertowe, nie transakcyjne – ocena jest materiałem dla komisji / prawnika, nie rozstrzygnięciem."}


def wezwanie_224_docx(sciezka, nazwa_zam, zamawiajacy, o, r):
    """Projekt wezwania do wyjaśnień ceny (art. 224 ust. 1 / ust. 2 Pzp) – z pozycjami odstającymi od rynku."""
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(zamawiajacy or "[UZUPEŁNIJ: zamawiający]", rozmiar=9)
    A(f"[UZUPEŁNIJ: miejscowość], {dt.date.today().strftime('%d.%m.%Y')} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A(f"{o.get('nazwa') or '[UZUPEŁNIJ: wykonawca]'}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("WEZWANIE DO ZŁOŻENIA WYJAŚNIEŃ DOTYCZĄCYCH CENY OFERTY", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"dotyczy postępowania: {nazwa_zam}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    obow = r.get("art224", {}).get("obowiazkowe")
    A(f"Działając na podstawie art. 224 ust. {'2 pkt 1' if obow else '1'} ustawy Prawo zamówień publicznych, zamawiający wzywa do złożenia wyjaśnień, "
      "w tym złożenia dowodów, w zakresie wyliczenia ceny oferty" + (" oraz jej istotnych części składowych wskazanych poniżej" if r.get("pozycje") else "") + ".")
    if obow:
        A("Uzasadnienie: " + r["art224"]["opis"])
    odst = [p for p in r.get("pozycje") or [] if p["odchylenie_proc"] <= -15]
    if odst:
        A("Istotne części składowe ceny budzące wątpliwości:", pogrub=True)
        for p in odst:
            A(PR.pl_liczby(f"– poz. {p['lp']} „{str(p['opis'])[:120]}”: cena jednostkowa {p['cena_jedn']:,.2f} zł netto, ceny rynkowe ok. "
                           f"{p['rynek_typowa']:,.2f} zł (odchylenie {p['odchylenie_proc']}%)"))
    if r.get("koszty_pracy"):
        A("Koszty pracy: " + r["koszty_pracy"]["opis"])
    A("Wyjaśnienia mogą dotyczyć w szczególności okoliczności z art. 224 ust. 3 Pzp (m.in. zarządzania procesem produkcji lub świadczenia usług, "
      "wybranych rozwiązań technicznych, wyjątkowo korzystnych warunków, zgodności z przepisami dotyczącymi kosztów pracy). Obowiązek wykazania, "
      "że oferta nie zawiera rażąco niskiej ceny, spoczywa na wykonawcy (art. 224 ust. 5 Pzp).")
    A("Termin złożenia wyjaśnień: [UZUPEŁNIJ: data i godzina], sposób: [UZUPEŁNIJ: platforma / adres].")
    A("Brak wyjaśnień albo wyjaśnienia niepotwierdzające, że cena nie jest rażąco niska, skutkują odrzuceniem oferty (art. 224 ust. 6, art. 226 ust. 1 pkt 8 Pzp).",
      rozmiar=9)
    A("\n[UZUPEŁNIJ: podpis osoby upoważnionej]", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# ---------------------------------------------------------------- kalkulator kosztów pracy (usługi pracochłonne)
SKLADKI_PRACODAWCY_2026 = {  # % wynagrodzenia brutto – składki finansowane przez pracodawcę (umowa o pracę)
    "emerytalna": 9.76, "rentowa": 6.50, "wypadkowa": 1.67, "fundusz_pracy": 2.45, "fgsp": 0.10}
DODATEK_NOCNY_PROC = 20  # art. 151^8 § 1 KP – 20% stawki godzinowej wynikającej z minimalnego wynagrodzenia

# H3-03: zwolnienia ze składek na Fundusz Pracy i FGŚP (sprawdzone 24.11.2026 w tekstach ustaw):
# FP – ustawa z 20.03.2025 o rynku pracy i służbach zatrudnienia (Dz.U. 2025 poz. 620): art. 261 (kobiety 55+, mężczyźni 60+),
#      art. 262 ust. 1 (50+ z rejestru bezrobotnych, 12 mies.), art. 262 ust. 2 (skierowany bezrobotny do 30 r.ż., 12 mies.), art. 263 (powrót z urlopu, 36 mies.);
# FGŚP – ustawa z 13.07.2006 o ochronie roszczeń pracowniczych w razie niewypłacalności pracodawcy: art. 9a (36 mies. po urlopie), art. 9b ust. 1 (50+ bezrobotny,
#      12 mies.), art. 9b ust. 2 (55+/60+), art. 9c (skierowany bezrobotny do 30 r.ż., 12 mies.).
ZWOLNIENIA_FP = {
    "": ("brak zwolnienia", None, ""),
    "wiek": ("kobieta 55+ / mężczyzna 60+", None, "art. 261 ustawy o rynku pracy i służbach zatrudnienia; art. 9b ust. 2 ustawy o ochronie roszczeń pracowniczych"),
    "urlop": ("powrót z urlopu macierzyńskiego, rodzicielskiego lub wychowawczego (36 mies.)", 36,
              "art. 263 ustawy o rynku pracy i służbach zatrudnienia; art. 9a ustawy o ochronie roszczeń pracowniczych"),
    "do30": ("bezrobotny do 30 r.ż. skierowany przez PUP – pierwsze 12 mies. zatrudnienia", 12,
             "art. 262 ust. 2 ustawy o rynku pracy i służbach zatrudnienia; art. 9c ustawy o ochronie roszczeń pracowniczych"),
    "bezrobotny50": ("50+ zarejestrowany jako bezrobotny 30 dni przed zatrudnieniem (12 mies.)", 12,
                     "art. 262 ust. 1 ustawy o rynku pracy i służbach zatrudnienia; art. 9b ust. 1 ustawy o ochronie roszczeń pracowniczych"),
}
# wynagrodzenie chorobowe: art. 92 § 1 i 2 KP – 80% podstawy (przeciętne wynagrodzenie po odliczeniu składek społecznych pracownika 13,71%)
# za czas niezdolności do pracy do 33 dni w roku (14 dni – pracownik po ukończeniu 50 lat); dalej zasiłek chorobowy z ZUS (nie koszt pracodawcy)
SKLADKI_PRACOWNIKA_PROC = 13.71
DNI_CHOROBOWEGO_PRACODAWCY = 33
DNI_CHOROBOWEGO_50 = 14
PPK_PODSTAWOWA = 1.5  # art. 26 ust. 1 ustawy o PPK
PPK_DODATKOWA_MAX = 2.5  # art. 26 ust. 2 ustawy o PPK – wpłata dodatkowa pracodawcy do 2,5%


WYMIAR_GODZ = 168  # przeciętny miesięczny wymiar czasu pracy pełnego etatu (8 h × ok. 21 dni) – podstawa stawki godzinowej
VAT_DOZWOLONE = (0, 5, 8, 23)


def kalkulator_pracy(p):
    """Minimalny koszt usługi pracochłonnej (umowa o pracę). p: osoby (etaty), miesiace, brutto (wynagrodzenie na etat, domyślnie minimalne),
    godziny_mies (na etat, domyślnie 168), nocne_proc (% godzin w porze nocnej), wypadkowa, ppk (bool), zastepstwa_proc (urlopy – domyślnie 10),
    absencje_proc (choroby – domyślnie 3), inne_os_mies (odzież, BHP, badania, szkolenia – zł/os./mies.), materialy_proc, ogolne_proc, zysk_proc,
    vat (stawka %), cena_oferty_brutto (opcjonalnie – porównanie)."""
    ujemne = []

    def f(k, d, maks=None):
        v = _f(p.get(k))
        if v is None:
            return d
        if v < 0:  # liczba etatów, miesiące, procenty i kwoty nie mogą być ujemne (dotąd obniżały koszt pracy)
            ujemne.append(k)
            return 0.0
        return min(v, maks) if maks is not None else v
    osoby, mies = f("osoby", 1, 10000), f("miesiace", 12, 120)
    pmin, uw_pmin = placa_min_okresu(p.get("od"), mies)  # płaca minimalna w okresie umowy (nie „na dziś”)
    d_od, lata = _lata_okresu(p.get("od"), mies)
    smin = round(sum(stawka_godz_min(r) for r in lata) / len(lata), 2)  # minimalna stawka godzinowa – ten sam okres co płaca minimalna
    brutto = f("brutto", pmin)
    godz = f("godziny_mies", WYMIAR_GODZ, 400) or WYMIAR_GODZ
    skl = dict(SKLADKI_PRACODAWCY_2026, wypadkowa=f("wypadkowa", SKLADKI_PRACODAWCY_2026["wypadkowa"], 10))
    uwagi = [uw_pmin] if uw_pmin else []
    if p.get("ppk") or _f(p.get("ppk_dodatkowa")):
        skl["ppk"] = PPK_PODSTAWOWA
        dod = f("ppk_dodatkowa", 0)
        if dod > PPK_DODATKOWA_MAX:
            uwagi.append(PR.pl_liczby(f"Wpłata dodatkowa PPK pracodawcy wynosi najwyżej {PPK_DODATKOWA_MAX:g}% (art. 26 ust. 2 ustawy o PPK) – przyjęto {PPK_DODATKOWA_MAX:g}%."))
            dod = PPK_DODATKOWA_MAX
        if dod:
            skl["ppk_dodatkowa"] = round(dod, 2)
    zw = str(p.get("zwolnienie_fp") or "")
    if zw not in ZWOLNIENIA_FP:
        uwagi.append("Nieznany rodzaj zwolnienia z FP i FGŚP – przyjęto brak zwolnienia.")
        zw = ""
    if brutto < pmin - 0.005:
        uwagi.append(PR.pl_liczby(f"Wynagrodzenie {brutto:.2f} zł jest niższe od minimalnego ({pmin:.2f} zł) – przy pełnym etacie niedopuszczalne."))
    # dodatek nocny: 20% stawki godzinowej z płacy minimalnej (płaca minimalna ÷ wymiar czasu pracy) za każdą godzinę w porze nocnej (art. 151^8 § 1 KP)
    dod_noc = round(pmin / WYMIAR_GODZ * DODATEK_NOCNY_PROC / 100 * godz * f("nocne_proc", 0, 100) / 100, 2)  # na etat / mies.
    # godziny ponad wymiar pełnego etatu: wynagrodzenie za te godziny + dodatek 50% (art. 151^1 § 1 pkt 2 KP) – dotąd pomijane (koszt zaniżony)
    nadg = max(0.0, godz - WYMIAR_GODZ)
    dod_nadg = round(brutto / WYMIAR_GODZ * nadg * 1.5, 2)
    if nadg:
        uwagi.append(PR.pl_liczby(f"{nadg:g} h ponad wymiar pełnego etatu ({WYMIAR_GODZ} h) to godziny nadliczbowe – doliczono wynagrodzenie z dodatkiem 50% "
                                  f"(art. 151^1 KP). Roczny limit to 150 h na pracownika (art. 151 § 3 KP), chyba że układ, regulamin albo umowa przewiduje inny."
                                  if nadg * 12 <= 150 else
                                  f"{nadg:g} h nadliczbowych miesięcznie (ok. {nadg * 12:g} h rocznie) przekracza limit 150 h rocznie (art. 151 § 3 KP) – "
                                  "zaplanuj więcej etatów; doliczono wynagrodzenie z dodatkiem 50%."))
    if ujemne:
        uwagi.append("Wartości ujemne (" + ", ".join(ujemne) + ") przyjęto jako 0.")
    podst = brutto + dod_noc + dod_nadg
    skladki_pelne = round(podst * sum(skl.values()) / 100, 2)
    # zwolnienie z FP i FGŚP: część etatów (domyślnie wszystkie) przez część okresu (36 / 12 mies. albo cały okres) – średnio na etat i miesiąc
    zw_info = None
    if zw:
        et_zw = min(osoby, f("osoby_zwolnione", osoby, 10000)) if osoby else 0.0
        mies_zw = min(mies, ZWOLNIENIA_FP[zw][1] or mies)
        udzial = (et_zw / osoby if osoby else 0) * (mies_zw / mies if mies else 0)
        oszcz = round(podst * (skl["fundusz_pracy"] + skl["fgsp"]) / 100 * udzial, 2)
        zw_info = {"rodzaj": zw, "opis": ZWOLNIENIA_FP[zw][0], "podstawa": ZWOLNIENIA_FP[zw][2], "etaty": et_zw, "miesiace": mies_zw,
                   "oszczednosc_na_etat_mies": oszcz, "oszczednosc_razem": round(podst * (skl["fundusz_pracy"] + skl["fgsp"]) / 100 * et_zw * mies_zw, 2)}
        uwagi.append(PR.pl_liczby(f"Zwolnienie ze składek na FP i FGŚP ({ZWOLNIENIA_FP[zw][0]}): {et_zw:g} et. przez {mies_zw:g} mies. "
                                  f"({ZWOLNIENIA_FP[zw][2]}). Warunki zwolnienia (wiek, data powrotu z urlopu, skierowanie z urzędu pracy) sprawdź dla każdej osoby."))
    else:
        oszcz = 0.0
    skladki = round(skladki_pelne - oszcz, 2)
    zast = round((podst + skladki) * f("zastepstwa_proc", 10, 100) / 100, 2)
    chor = None
    if p.get("absencje_metoda") == "chorobowe":  # H3-03: wynagrodzenie chorobowe jako parametr (art. 92 KP) zamiast % kosztu
        dni_ch = f("dni_choroby_rok", 10, 365)
        lim = DNI_CHOROBOWEGO_50 if p.get("pracownicy_50") else DNI_CHOROBOWEGO_PRACODAWCY
        proc_ch = f("chorobowe_proc", 80, 100)
        dni_pl = min(dni_ch, lim)
        abs_ = round(podst * (1 - SKLADKI_PRACOWNIKA_PROC / 100) * proc_ch / 100 / 30 * dni_pl / 12, 2)
        chor = {"dni_choroby_rok": dni_ch, "dni_platne_przez_pracodawce": dni_pl, "limit_dni": lim, "procent": proc_ch,
                "opis": PR.pl_liczby(f"Wynagrodzenie chorobowe (art. 92 KP): {proc_ch:g}% podstawy (wynagrodzenie po odliczeniu {SKLADKI_PRACOWNIKA_PROC:g}% składek pracownika) "
                                     f"za {dni_pl:g} z {dni_ch:g} dni choroby w roku (pracodawca płaci do {lim} dni rocznie"
                                     + (", pracownik po 50. roku życia" if lim == DNI_CHOROBOWEGO_50 else "") + "; dalej zasiłek z ZUS). "
                                     "Za dni choroby nie płaci się wynagrodzenia zasadniczego ani składek, więc zastępstwo w tym czasie mieści się w koszcie etatu.")}
        if dni_ch > lim:
            uwagi.append(PR.pl_liczby(f"{dni_ch:g} dni choroby w roku – pracodawca płaci wynagrodzenie chorobowe za {lim} dni, pozostałe {dni_ch - lim:g} dni – zasiłek chorobowy z ZUS."))
    else:
        abs_ = round((podst + skladki) * f("absencje_proc", 3, 100) / 100, 2)
    inne = f("inne_os_mies", 0)
    na_etat = round(podst + skladki + zast + abs_ + inne, 2)
    praca = round(na_etat * osoby * mies, 2)
    mat = round(praca * f("materialy_proc", 0, 1000) / 100, 2)
    ogolne = round((praca + mat) * f("ogolne_proc", 0, 1000) / 100, 2)
    zysk = round((praca + mat + ogolne) * f("zysk_proc", 0, 1000) / 100, 2)
    netto = round(praca + mat + ogolne + zysk, 2)
    vat = f("vat", 23)
    if vat not in VAT_DOZWOLONE:  # tylko stawki VAT z ustawy o VAT (0, 5, 8, 23%) – inna wartość dawała dowolną cenę brutto
        uwagi.append(PR.pl_liczby(f"Stawka VAT {vat:g}% nie istnieje – przyjęto 23%."))
        vat = 23.0
    okres = f"{d_od:%m.%Y}, {mies:g} mies." + (f" (lata {min(lata)}–{max(lata)})" if min(lata) != max(lata) else f" ({lata[0]} r.)")
    wyn = {"parametry": {"placa_minimalna": pmin, "stawka_godzinowa_min": smin, "skladki_pracodawcy": skl, "dodatek_nocny_proc": DODATEK_NOCNY_PROC,
                         "od": d_od.isoformat(), "okres": okres, "wymiar_godz": WYMIAR_GODZ,
                         "placa_minimalna_lata": {str(r): placa_min(r) for r in sorted(set(lata))},
                         "zwolnienie_fp": zw_info, "chorobowe": chor, "ppk_dodatkowa": skl.get("ppk_dodatkowa", 0),
                         "absencje_metoda": "chorobowe" if chor else "procent"},
           "na_etat_mies": {"wynagrodzenie": brutto, "dodatek_nocny": dod_noc, "nadgodziny": dod_nadg, "skladki": skladki, "zastepstwa": zast, "absencje": abs_, "inne": inne, "razem": na_etat},
           "koszty_pracy": praca, "materialy": mat, "ogolne": ogolne, "zysk": zysk, "cena_netto": netto, "cena_brutto": round(netto * (1 + vat / 100), 2),
           "minimum_netto": praca, "minimum_brutto": round(praca * (1 + vat / 100), 2), "osoby": osoby, "miesiace": mies, "vat": vat, "uwagi": uwagi}
    c = _f(p.get("cena_oferty_brutto"))
    if c:
        pokr = round(c / wyn["minimum_brutto"] * 100, 1) if wyn["minimum_brutto"] else None
        wyn["porownanie"] = {"cena_oferty_brutto": c, "pokrycie_proc": pokr,
                             "ocena": ("Cena NIE pokrywa minimalnych kosztów pracy – podstawa do wezwania do wyjaśnień (art. 224 ust. 1 i ust. 3 pkt 4 Pzp)."
                                       if c < wyn["minimum_brutto"] else
                                       "Cena pokrywa minimalne koszty pracy, ale zostaje mniej niż 10% na materiały, koszty ogólne i zysk – do wyjaśnienia."
                                       if c < wyn["minimum_brutto"] * 1.1 else
                                       "Cena pokrywa minimalne koszty pracy z zapasem.")}
    return wyn


def kalkulator_docx(sciezka, p, w, tytul=""):
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    zl = lambda v: PR.liczba_pl(v) + " zł"
    A("WYLICZENIE KOSZTÓW PRACY", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    if tytul:
        A(tytul, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    P_ = w["parametry"]
    lata_ = P_.get("placa_minimalna_lata") or {}
    A(f"Założenia: {PR.liczba_pl(w['osoby']).replace(',00', '')} etatu(-ów), {w['miesiace']:g} mies. od {P_.get('okres') or ''}, umowa o pracę; "
      f"minimalne wynagrodzenie w okresie umowy: {zl(P_['placa_minimalna'])}"
      + (" (średnio: " + ", ".join(f"{r} r. – {zl(v)}" for r, v in lata_.items()) + ")" if len(lata_) > 1 else "") + "; "
      f"składki pracodawcy: " + ", ".join(f"{k.replace('_', ' ')} {v:g}%" for k, v in w["parametry"]["skladki_pracodawcy"].items())
      + f"; dodatek za pracę w nocy: {w['parametry']['dodatek_nocny_proc']}% stawki godzinowej z minimalnego wynagrodzenia (art. 151^8 § 1 KP).")
    if P_.get("ppk_dodatkowa"):  # H3-03: wybrane opcje w wydruku
        A(PR.pl_liczby(f"PPK: wpłata podstawowa pracodawcy {PPK_PODSTAWOWA:g}% i dodatkowa {P_['ppk_dodatkowa']:g}% (art. 26 ustawy o PPK)."))
    elif "ppk" in P_["skladki_pracodawcy"]:
        A(PR.pl_liczby(f"PPK: wpłata podstawowa pracodawcy {PPK_PODSTAWOWA:g}% (art. 26 ust. 1 ustawy o PPK), bez wpłaty dodatkowej."))
    if P_.get("zwolnienie_fp"):
        z_ = P_["zwolnienie_fp"]
        A(PR.pl_liczby(f"Zwolnienie ze składek na Fundusz Pracy i FGŚP: {z_['opis']} – {z_['etaty']:g} et. przez {z_['miesiace']:g} mies. ({z_['podstawa']}); "
                       f"oszczędność w okresie: {PR.liczba_pl(z_['oszczednosc_razem'])} zł."))
    if P_.get("chorobowe"):
        A(P_["chorobowe"]["opis"])
    else:
        A("Absencje chorobowe: ryczałtowo jako procent kosztu etatu (bez wyliczenia wynagrodzenia chorobowego z art. 92 KP).")
    e = w["na_etat_mies"]
    for t_, v in (("Wynagrodzenie brutto", e["wynagrodzenie"]), ("Dodatek nocny", e["dodatek_nocny"]), ("Godziny nadliczbowe z dodatkiem", e.get("nadgodziny") or 0), ("Składki pracodawcy", e["skladki"]),
                  ("Zastępstwa urlopowe", e["zastepstwa"]), ("Absencje chorobowe", e["absencje"]), ("Odzież, BHP, badania, szkolenia", e["inne"]),
                  ("Koszt etatu miesięcznie", e["razem"])):
        A(f"{t_}: {zl(v)}", pogrub=t_.startswith("Koszt"))
    A(f"Koszty pracy w okresie: {zl(w['koszty_pracy'])} · materiały: {zl(w['materialy'])} · koszty ogólne: {zl(w['ogolne'])} · zysk: {zl(w['zysk'])}")
    A(f"Cena netto: {zl(w['cena_netto'])} · VAT {w['vat']:g}% · cena brutto: {zl(w['cena_brutto'])}", pogrub=True)
    A(f"Minimalne koszty pracy (bez materiałów, kosztów ogólnych i zysku): {zl(w['minimum_netto'])} netto / {zl(w['minimum_brutto'])} brutto.")
    if w.get("porownanie"):
        A(f"Porównanie z ceną oferty {zl(w['porownanie']['cena_oferty_brutto'])} brutto: pokrycie minimalnych kosztów pracy {w['porownanie']['pokrycie_proc']}%. "
          + w["porownanie"]["ocena"], pogrub=True)
    for u in w.get("uwagi") or []:
        A(u)
    A("Wyliczenie pomocnicze – parametry i założenia (zastępstwa, absencje, narzuty) do weryfikacji dla konkretnego zamówienia.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
