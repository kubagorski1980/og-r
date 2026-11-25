# -*- coding: utf-8 -*-
"""Zamawiający: badanie złożonych ofert (zgodność z SWZ, kompletność, błędy rachunkowe, rażąco niska cena, podstawy odrzucenia),
punktacja według kryteriów z SWZ, ranking i wybór najkorzystniejszej oferty; protokół, informacja o wyborze, wezwania."""
import datetime as dt
import re

import modul_oferty as MO

import progi as _PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)
SYSTEM_SWZ = (_PR.INFO_AI + " " + "Jesteś ekspertem od zamówień publicznych (ustawa Pzp). Czytasz SWZ / zapytanie ofertowe i wyodrębniasz to, co jest potrzebne "
              "do badania i oceny ofert. Nie zmyślasz – brak danych = pusty. Odpowiadasz WYŁĄCZNIE JSON-em.")

POLECENIE_SWZ = (
    "Z dokumentów postępowania wypisz dane do badania i oceny ofert. Zwróć JSON:\n"
    '{"nazwa_zamowienia": "", "numer": "", "zamawiajacy": "", "tryb": "", "kwota_budzet_brutto": liczba albo null, '
    '"termin_skladania": "", "wadium": "kwota albo brak", '
    '"kryteria": [{"nazwa": "Cena", "cena": true tylko dla kryterium ceny lub kosztu (inne kryteria – false), "waga": 60, "typ": "min|max|punktowe", "jednostka": "zł|dni|mies.|pkt", '
    '"opis": "sposób liczenia punktów z SWZ, np. Cn/Cb × 60", "max_pkt": 60, '
    '"od": wartość, za którą przyznaje się 0 pkt (np. minimalny okres gwarancji 60) albo null, '
    '"do": wartość, od której przyznaje się pełną liczbę punktów (np. 84) albo null}], '
    '"wymagane_dokumenty": ["formularz ofertowy", "…"], "warunki_udzialu": ["…"], '
    '"wymagania_przedmiotu": ["kluczowe wymagania techniczne / parametry minimalne z OPZ"], '
    '"podstawy_wykluczenia": ["art. 108 ust. 1 Pzp", "…"], '
    '"podmiotowe_srodki": ["podmiotowe środki dowodowe, które składa na wezwanie wykonawca, którego oferta została najwyżej oceniona (np. informacja z KRK, wykaz robót z dowodami, polisa OC) – z SWZ"], '
    '"czesci": [{"nr": 1, "nazwa": "", "kwota_budzet_brutto": liczba albo null}], "limit_czesci_dla_wykonawcy": liczba albo null}\n'
    "Jeżeli zamówienie jest podzielone na części – wypisz wszystkie części z kwotą przeznaczoną na sfinansowanie każdej części (jeśli podana) "
    "i maksymalną liczbę części, które można udzielić jednemu wykonawcy (art. 91 ust. 3); bez podziału – pusta lista i null.\n"
    "typ kryterium: „min” – im mniej, tym lepiej (cena, termin realizacji); „max” – im więcej, tym lepiej (gwarancja, doświadczenie); "
    "„punktowe” – punkty przyznawane według opisu (np. tak/nie). Wagi w punktach procentowych, razem 100. "
    "Pola „od” i „do” wypełnij tylko wtedy, gdy SWZ punktuje kryterium w zakresie (np. G = (Gb − 60) / (84 − 60) × 40); "
    "gdy wzór porównuje z najlepszą ofertą (Gb / Gmax × 40) – null.")

SYSTEM_OFERTA = ("Jesteś członkiem komisji przetargowej i badasz ofertę zgodnie z ustawą Pzp (art. 223–226, 128, 224) albo zasadą "
                 "konkurencyjności. Sprawdzasz formalnie i merytorycznie, rzetelnie, z podaniem miejsca w dokumentach. Nie zgadujesz – "
                 "jeśli czegoś nie da się stwierdzić z plików, napisz to. Odpowiadasz WYŁĄCZNIE JSON-em.")


SYSTEM_SWZ_PRYW = ("Czytasz zapytanie ofertowe wspólnoty mieszkaniowej, spółdzielni albo dewelopera – zamawiającego, który NIE stosuje ustawy "
                   "Prawo zamówień publicznych – i wyodrębniasz kryteria oceny z wagami, wymagane dokumenty, wymagania wobec wykonawców i podział na części. "
                   "Nie dopisuj instytucji Pzp, których zapytanie nie przewiduje. Odpowiadasz wyłącznie JSON.")
SYSTEM_OFERTA_PRYW = ("Badasz ofertę złożoną w zapytaniu ofertowym wspólnoty mieszkaniowej, spółdzielni albo dewelopera – zamawiającego, który NIE stosuje "
                      "ustawy Prawo zamówień publicznych. Sprawdzasz zgodność oferty z zapytaniem (zakres, termin, wymagane dokumenty i warunki), "
                      "kompletność, błędy rachunkowe i ceny znacząco niższe od innych ofert lub szacunku (do wyjaśnienia z wykonawcą). Podstawą są treść "
                      "zapytania i Kodeks cywilny – nie powołuj przepisów Pzp. Odpowiadasz wyłącznie JSON.")


def _bez_pzp(t):
    """Teksty dla zamawiającego prywatnego: bez odwołań do przepisów Pzp i bez „komisji przetargowej”."""
    t = re.sub(r"\s*\((?:zgodnie z )?art\.[^()]*?(?:Pzp|ustawy Prawo zamówień publicznych)\)", "", t)
    t = re.sub(r"Działając na podstawie art\. \d+ ustawy Prawo zamówień publicznych, Zamawiający informuje", "Zamawiający informuje", t)
    PRZEPIS = r"art\.\s*\d+[a-z]?(?:\s*ust\.\s*\d+[a-z]?)?(?:\s*pkt\s*\d+[a-z]?)?(?:\s*lit\.\s*[a-z])?(?:\s*(?:i|oraz|–)\s*\d+)*\s*(?:Pzp|ustawy Prawo zamówień publicznych)"
    t = re.sub(r"(?i)\b(?:działając )?(?:na podstawie|zgodnie z|w trybie|według|na mocy)\s+" + PRZEPIS + r"\s*,?\s*", "", t)
    t = re.sub(r"\s*" + PRZEPIS, "", t)
    t = re.sub(r"(^|[.:]\s+|\d\.\s+)([a-ząćęłńóśźż])", lambda m: m.group(1) + m.group(2).upper(), t)
    return (t.replace("komisję przetargową", "zarząd").replace("komisji przetargowej", "zarządu").replace("członków komisji", "członków zarządu")
             .replace("Kierownika Zamawiającego", "Zamawiającego").replace("SWZ", "zapytaniu ofertowym").replace("zapytaniu ofertowymie", "zapytaniu ofertowym"))


def podpisy(swz):
    """H3-07: podpisy pod protokołem – komisja przetargowa u zamawiającego publicznego; we wspólnocie mieszkaniowej członkowie zarządu
    (co najmniej dwóch – art. 21 ust. 2 ustawy o własności lokali) albo zarządca, któremu powierzono zarząd (art. 18 ust. 1)."""
    if not swz.get("prywatny"):
        return "Podpisy członków komisji: ..........................................................................."
    return {"spoldzielnia": "Podpisy członków zarządu spółdzielni: ...........................................................................",
            "deweloper": "Podpis osoby uprawnionej do reprezentacji zamawiającego: ...........................................................................",
            "mala": "Podpisy współwłaścicieli albo zarządcy: ...........................................................................",
            }.get(swz.get("podmiot") or "wspolnota",
                  "Podpisy członków zarządu wspólnoty (co najmniej dwóch – art. 21 ust. 2 ustawy o własności lokali) albo zarządcy "
                  "(art. 18 ust. 1 tej ustawy): ...........................................................................")


def _docx_bez_pzp(d):
    for p in list(d.paragraphs) + [p for t in d.tables for r in t.rows for c in r.cells for p in c.paragraphs]:
        n = _bez_pzp(p.text)
        if n != p.text and p.runs:
            p.runs[0].text = n
            for r in p.runs[1:]:
                r.text = ""


def polecenie_oferty(swz, nazwa_wyk):
    if swz.get("prywatny"):
        return _bez_pzp(_polecenie_oferty(dict(swz, prywatny=False), nazwa_wyk))
    return _polecenie_oferty(swz, nazwa_wyk)


def _polecenie_oferty(swz, nazwa_wyk):
    cz = [c for c in (swz.get("czesci") or []) if isinstance(c, dict)]
    dod = ("\nZAMÓWIENIE PODZIELONE NA CZĘŚCI: " + "; ".join(f"część {c.get('nr')} – {c.get('nazwa') or ''}" for c in cz) +
           ". Ustal, na które części złożono ofertę, i dla KAŻDEJ z nich podaj cenę brutto i wartości kryteriów w polu \"czesci\": "
           '[{"nr": 1, "cena_brutto": liczba, "wartosci_kryteriow": {"nazwa kryterium": wartość}}]. Części, na które oferty nie złożono, pomiń. '
           "W polu cena_brutto podaj sumę cen ze wszystkich części.\n") if cz else ""
    return (dod + f"Zbadaj ofertę wykonawcy „{nazwa_wyk}” (pliki oferty są oznaczone jako dokumenty OFERTY; pozostałe to dokumenty "
            "postępowania – SWZ). Sprawdź: kompletność wymaganych dokumentów, zgodność treści oferty z SWZ i OPZ (parametry, ilości, "
            "terminy), poprawność formularza cenowego (błędy rachunkowe – przelicz ilość × cena i sumy), wadium, termin związania, "
            "spełnianie warunków udziału, oznaki niepodpisania lub podpisu osoby nieuprawnionej (jeśli widać w treści), tajemnicę "
            "przedsiębiorstwa. Odczytaj wartości do kryteriów oceny.\n"
            f"KRYTERIA OCENY: {swz.get('kryteria')}\nWYMAGANE DOKUMENTY: {swz.get('wymagane_dokumenty')}\n"
            'Zwróć JSON: {"cena_brutto": liczba, "cena_netto": liczba albo null, '
            '"wartosci_kryteriow": {"nazwa kryterium": liczba albo tekst – wartość zaoferowana}, '
            '"status": "prawidłowa | do wyjaśnienia | do uzupełnienia | do odrzucenia", '
            '"braki": [{"opis": "brakujący lub wadliwy dokument – do uzupełnienia (art. 128 Pzp)", "dokument": "plik SWZ albo oferty", "miejsce": "", "cytat": ""}], '
            '"niezgodnosci": [{"opis": "niezgodność z SWZ/OPZ", "dokument": "plik oferty lub SWZ", "miejsce": "§ / pkt / poz.", "cytat": "dosłowny fragment"}], '
            '"bledy_rachunkowe": [{"opis": "…", "poprawka": "jak poprawić (art. 223 ust. 2 Pzp)", "dokument": "plik oferty", "miejsce": "poz. …", "cytat": "dosłowny wiersz / fragment"}], '
            '"do_wyjasnienia": [{"opis": "pytanie do wykonawcy (art. 223 ust. 1 Pzp)", "dokument": "", "miejsce": "", "cytat": ""}], '
            '"podstawa_odrzucenia": "przepis i uzasadnienie albo pusty", "uwagi": "krótko", '
            '"wykonawca_nip": "", "wykonawca_adres": "", '
            '"referencje": [{"wystawca": "nazwa wystawcy referencji / zamawiającego", "nip_wystawcy": "", "adres_wystawcy": "", "zakres": "", '
            '"adres_obiektu": "", "wartosc": "kwota", "data_od": "", "data_do": "", "kontakt_osoba": "", "kontakt_email": "", "kontakt_telefon": "", '
            '"plik": "nazwa pliku z referencją albo wykazem"}], '
            '"kierownik": {"imie_nazwisko": "", "nr_uprawnien": "", "specjalnosc": ""}, '
            '"polisa": {"numer": "", "ubezpieczyciel": "", "okres_od": "", "okres_do": "", "suma_gwarancyjna": ""}}\n'
            "REFERENCJE: wypisz każde doświadczenie podane w wykazie robót/usług i każdą referencję lub protokół odbioru – tak, jak je podano, "
            "bez oceny prawdziwości; puste pola, gdy brak danych.\n"
            "ODWOŁANIA: przy każdej pozycji podaj „dokument” (nazwa pliku – SWZ albo oferty), „miejsce” (§, pkt, poz., str.) i „cytat” – "
            "DOSŁOWNY fragment z tego pliku (20–300 znaków), znak w znak; program sprawdza go i pokazuje użytkownikowi. Brak dosłownego cytatu = pusty.")


def _t(x):
    """Pozycja listy jako tekst (AI zwraca obiekty z odwołaniem albo zwykłe zdania)."""
    if isinstance(x, dict):
        return str(x.get("opis") or "") + (f" ({x['miejsce']})" if x.get("miejsce") else "")
    return str(x)


def _f(x):
    return liczba(re.sub(r"[^\d,.\-]", "", str(x)) if x is not None else None)  # „60 miesięcy” → 60


def _pkt2(x):
    """Punkty zaokrąglone do 0,01 w górę od połowy (2,675 → 2,68), nie na liczbie binarnej (round(2.675, 2) = 2.67)."""
    from decimal import ROUND_HALF_UP, Decimal
    return float(Decimal(str(x or 0)).quantize(Decimal("0.01"), ROUND_HALF_UP))


# art. 226 ust. 1 Pzp – podstawy odrzucenia oferty (do wyboru przez komisję); pkt 1, 5a i 10 wyłączają ofertę ze średniej z art. 224 ust. 2 pkt 1
PUNKTY_226 = {"1": "złożona po terminie składania ofert", "2a": "wykonawca podlega wykluczeniu", "2b": "wykonawca nie spełnia warunków udziału",
              "2c": "wykonawca nie złożył w terminie oświadczenia (art. 125 ust. 1) lub podmiotowego / przedmiotowego środka dowodowego",
              "3": "oferta niezgodna z przepisami ustawy", "4": "oferta nieważna na podstawie odrębnych przepisów",
              "5": "treść oferty niezgodna z warunkami zamówienia", "5a": "wykonawca z państwa trzeciego niebędącego stroną umowy międzynarodowej",
              "6": "oferta niezgodna z wymaganiami technicznymi i organizacyjnymi komunikacji elektronicznej",
              "7": "złożona w warunkach czynu nieuczciwej konkurencji", "8": "rażąco niska cena lub koszt", "9": "wykonawca niezaproszony do składania ofert",
              "10": "błędy w obliczeniu ceny lub kosztu", "11": "wykonawca zakwestionował poprawienie omyłki (art. 223 ust. 2 pkt 3)",
              "12": "brak zgody na przedłużenie terminu związania ofertą", "13": "brak zgody na wybór oferty po upływie terminu związania",
              "14": "wadium niewniesione lub wniesione nieprawidłowo", "15": "oferta wariantowa niezłożona lub niespełniająca wymagań minimalnych",
              "16": "bezpieczeństwo publiczne lub istotny interes bezpieczeństwa państwa", "17": "produkt, usługa lub proces ICT z rekomendacji (art. 33 ust. 4 uksc)",
              "18": "brak wymaganej wizji lokalnej lub sprawdzenia dokumentów u zamawiającego",
              "19": "produkt ICT dostawcy wysokiego ryzyka (art. 67b ust. 15 uksc)"}
PUNKTY_226_SREDNIA = ("1", "5a", "10")  # art. 224 ust. 2 pkt 1 w obecnym brzmieniu


def _punkt_226(o):
    """Punkt art. 226 ust. 1, na podstawie którego ofertę odrzucono: pole „punkt_226” (wybór komisji), inaczej z tekstu podstawy."""
    w_ = o.get("wynik") or {}
    p = str(w_.get("punkt_226") or o.get("punkt_226") or "").strip().lower()
    if p in PUNKTY_226:
        return p
    m = re.search(r"226\s*ust\.\s*1\s*pkt\s*(\d{1,2}[a-c]?)(?![\da-z])", str(w_.get("podstawa_odrzucenia") or o.get("powod_odrzucenia") or ""), re.I)
    return m.group(1).lower() if m else ""


def odrzucona(o):
    w_ = o.get("wynik") or {}
    return bool(o.get("odrzucona") or w_.get("status") == "do odrzucenia")


def ceny_do_sredniej_224(oferty, prywatny=False):
    """Ceny do średniej z art. 224 ust. 2 pkt 1 Pzp: wszystkie złożone oferty z wyłączeniem odrzuconych na podstawie art. 226 ust. 1 pkt 1, 5a i 10
    (u zamawiającego prywatnego – bez wszystkich ofert odrzuconych). Ta sama reguła w rankingu i w „Rynkowości cen”."""
    wyn = []
    for o in oferty or []:
        if not isinstance(o, dict):
            continue
        c = _f((o.get("wynik") or {}).get("cena_brutto"))
        if not c:
            continue
        if odrzucona(o) and (prywatny or _punkt_226(o) in PUNKTY_226_SREDNIA):
            continue
        wyn.append(c)
    return wyn


def ponizej_30(cena, kwoty):
    """Art. 224 ust. 2 pkt 1: cena niższa o co najmniej 30% od kwoty (wartości z VAT – [w]) albo od średniej kwot – liczone w groszach, bez błędu
    liczb zmiennoprzecinkowych: cena ≤ 70% · (suma / n)  ⇔  cena · n · 10 ≤ suma · 7."""
    k = [round(_f(x) * 100) for x in kwoty or [] if _f(x)]
    c = _f(cena)
    return bool(c and k and round(c * 100) * len(k) * 10 <= sum(k) * 7)


_NAZWY_CENY = re.compile(r"(?:cena|koszt)(?:\s+(?:brutto|netto|oferty|ofertowa|całkowita|oferty brutto|ofertowa brutto|całkowita brutto|całkowita oferty))?")


def jest_cena(k):
    """Kryterium ceny lub kosztu: jawne pole „cena” (kreator, odczyt SWZ) albo nazwa dokładnie „Cena”, „Cena brutto”, „Cena oferty”, „Koszt”…
    – nie każda nazwa zawierająca „cen” („Ocena koncepcji”, „Licencja”, „Recenzja” to kryteria pozacenowe)."""
    if not isinstance(k, dict):
        return False
    if isinstance(k.get("cena"), bool):
        return k["cena"]
    n = re.sub(r"\([^)]*\)", " ", str(k.get("nazwa") or "")).strip(" .:–-").lower()
    return bool(_NAZWY_CENY.fullmatch(re.sub(r"\s+", " ", n)))


def ranking(swz, oferty):
    """Ranking ofert – przy zamówieniu podzielonym na części osobno dla każdej części (art. 91 Pzp)."""
    cz = [c for c in (swz.get("czesci") or []) if isinstance(c, dict) and c.get("nr") is not None]
    return ranking_czesci(swz, oferty, cz) if cz else _ranking_jeden(swz, oferty)


def ranking_czesci(swz, oferty, czesci):
    """Dla każdej części: oferty złożone na tę część, punktacja i rażąco niska cena liczone w obrębie części, najkorzystniejsza oferta.
    Kontrola limitu części udzielanych jednemu wykonawcy (art. 91 ust. 3)."""
    wyniki, ostrz = [], []
    for o in oferty:
        o["czesci_wyniki"] = {}
        o["punkty"], o["punkty_szczegoly"], o["miejsce"] = 0.0, {}, None
        o["razaco_niska"] = o["ponad_budzet"] = False
        o["niezgodna_kryterium"] = []
    for c in czesci:
        nr = str(c.get("nr"))
        kopie = []
        for o in oferty:
            w = o.get("wynik") or {}
            wc = next((x for x in (w.get("czesci") or []) if isinstance(x, dict) and str(x.get("nr")) == nr and _f(x.get("cena_brutto"))), None)
            if wc:
                kopie.append({"id": o.get("id"), "nazwa": o.get("nazwa"), "nr": o.get("nr"), "odrzucona": o.get("odrzucona"), "punkt_226": o.get("punkt_226"),
                              "wynik": {"cena_brutto": wc.get("cena_brutto"), "wartosci_kryteriow": wc.get("wartosci_kryteriow") or {},
                                        "status": w.get("status"), "wyjasnione": w.get("wyjasnione"), "punkt_226": w.get("punkt_226"),
                                        "podstawa_odrzucenia": w.get("podstawa_odrzucenia")}})
        swz_c = {"kryteria": c.get("kryteria") or swz.get("kryteria"), "kwota_budzet_brutto": c.get("kwota_budzet_brutto"),
                 "wartosc_zam_brutto": c.get("wartosc_zam_brutto")}
        pod = _ranking_jeden(swz_c, kopie) if kopie else {"najkorzystniejsza": None, "pierwsza_w_rankingu": None, "warunkowo": False,
                                                          "srednia_cen": None, "budzet": _f(c.get("kwota_budzet_brutto"))}
        for k in kopie:
            o = next(x for x in oferty if x.get("id") == k["id"])
            o["czesci_wyniki"][nr] = {"cena_brutto": _f(k["wynik"]["cena_brutto"]), "punkty": k["punkty"], "punkty_szczegoly": k["punkty_szczegoly"],
                                      "miejsce": k["miejsce"], "razaco_niska": k["razaco_niska"], "ponad_budzet": k["ponad_budzet"],
                                      "niezgodna_kryterium": k.get("niezgodna_kryterium") or []}
            o["niezgodna_kryterium"] += [f"część {nr}: {t}" for t in k.get("niezgodna_kryterium") or []]
            o["razaco_niska"] = o["razaco_niska"] or k["razaco_niska"]
            o["ponad_budzet"] = o["ponad_budzet"] or k["ponad_budzet"]
        wyniki.append({"nr": c.get("nr"), "nazwa": c.get("nazwa") or "", "ofert": len(kopie), **pod})
        ostrz += [f"Część {c.get('nr')} ({c.get('nazwa') or ''}): {t}" for t in pod.get("ostrzezenia") or []]
        if not kopie:
            ostrz.append(f"Część {c.get('nr')} ({c.get('nazwa') or ''}): brak ofert – " + ("ponów zapytanie w tej części albo zaproś wykonawców."
                         if swz.get("prywatny") else "postępowanie w tej części podlega unieważnieniu (art. 255 pkt 1 Pzp)."))
    limit = _f(swz.get("limit_czesci_dla_wykonawcy"))
    if limit:
        ile = {}
        for w in wyniki:
            if w.get("najkorzystniejsza"):
                ile[w["najkorzystniejsza"]] = ile.get(w["najkorzystniejsza"], 0) + 1
        for oid, n in ile.items():
            if n > limit:
                naz = next((o.get("nazwa") for o in oferty if o.get("id") == oid), oid)
                ostrz.append(f"{naz} ma najkorzystniejszą ofertę w {n} częściach, a jednemu wykonawcy można udzielić najwyżej {int(limit)} – "
                             "zastosuj zasady wyboru części określone w SWZ (art. 91 ust. 3 Pzp).")
    return {"czesci": wyniki, "ostrzezenia": ostrz, "najkorzystniejsza": None, "pierwsza_w_rankingu": None, "warunkowo": False,
            "srednia_cen": None, "budzet": _f(swz.get("kwota_budzet_brutto"))}



def _pkt(x):
    """Punkty po polsku: 94.2857 → „94,29”."""
    return _PR.liczba_pl(_f(x) or 0, 2)


def _waga(w):
    """Waga kryterium po polsku: 60.0 → „60”, 12.5 → „12,5”."""
    v = _f(w)
    return _PR.pl_liczby(f"{v:g}") if v is not None else ""


def opis_kryterium(k):
    """Sposób przyznawania punktów – ten sam opis co w kreatorze i w poleceniu dla AI (kreator_zam.opis_kryterium)."""
    import kreator_zam as KZ
    return KZ.opis_kryterium(k)


def _sposob_oceny(k):
    o = str(k.get("opis") or "").strip()
    return opis_kryterium(k) if not o or "sprawdź z SWZ" in o else o


def _co_nierozstrzygniete(o, razaco=None):
    w = o.get("wynik") or {}
    co = []
    if w.get("status") and w.get("status") != "prawidłowa":
        co.append(f"ma status „{w['status']}”")
    elif not w.get("status"):
        co.append("nie została jeszcze zbadana")
    if o.get("razaco_niska") if razaco is None else razaco:
        co.append("wymaga wyjaśnienia ceny (art. 224 Pzp)")
    for t in o.get("niezgodna_kryterium") or []:
        co.append("jest niezgodna z SWZ – " + t)
    return " i ".join(co) or "ma nierozstrzygnięte kwestie"


def wstrzymany_wybor(oferty, podsum):
    """Powody, dla których nie można jeszcze wskazać najkorzystniejszej oferty (art. 253): najwyżej oceniona oferta ma nierozstrzygnięte
    kwestie – braki, wyjaśnienia, rażąco niską cenę. Pusta lista = wybór rozstrzygnięty."""
    rada = ("Najpierw rozstrzygnij: przyjmij wyjaśnienia lub uzupełnienia (przycisk „Wyjaśnione / uzupełnione – oferta prawidłowa”) "
            "albo odrzuć ofertę z podaniem podstawy prawnej i faktycznej.")
    powody = []
    if podsum.get("czesci"):
        for c in podsum["czesci"]:
            if not c.get("warunkowo"):
                continue
            nr = str(c.get("nr"))
            o = next((x for x in oferty if x.get("id") == c.get("pierwsza_w_rankingu")), None)
            if c.get("remis_248"):
                powody.append(f"Część {c.get('nr')}: " + next((t for t in c.get("ostrzezenia") or [] if "248 ust. 3" in t), "remis (art. 248 ust. 3 Pzp)."))
            elif o:
                r = (o.get("czesci_wyniki") or {}).get(nr) or {}
                powody.append(f"Część {c.get('nr')}: najwięcej punktów ma oferta nr {o.get('nr')} – {o.get('nazwa')} ({_pkt(r.get('punkty'))} pkt), "
                              f"która {_co_nierozstrzygniete(o, r.get('razaco_niska'))}.")
    elif podsum.get("warunkowo"):
        o = next((x for x in oferty if x.get("id") == podsum.get("pierwsza_w_rankingu")), None)
        if podsum.get("remis_248"):
            powody.append(next((t for t in podsum.get("ostrzezenia") or [] if "248 ust. 3" in t), "Remis (art. 248 ust. 3 Pzp)."))
        elif o:
            powody.append(f"Najwięcej punktów ma oferta nr {o.get('nr')} – {o.get('nazwa')} ({_pkt(o.get('punkty'))} pkt), "
                          f"która {_co_nierozstrzygniete(o)}.")
    return powody + [rada] if powody else []


def _art224_tekst(o, swz, podsum):
    """Konkretne uzasadnienie obowiązkowego wezwania z art. 224 ust. 2 pkt 1 – kwota i różnica w %."""
    w = o.get("wynik") or {}
    c = _f(w.get("cena_brutto"))
    if w.get("wyjasnione") and c:
        return f"Wyjaśnienia dotyczące ceny {MO.zl(c)} przyjęte – cena nie jest rażąco niska (art. 224 ust. 6 Pzp a contrario)."
    if not o.get("razaco_niska"):
        return ""
    if podsum.get("czesci"):
        cz = [nr for nr, r in (o.get("czesci_wyniki") or {}).items() if r.get("razaco_niska")]
        return (f"Cena w części {', '.join(cz)} niższa o co najmniej 30% od wartości zamówienia z VAT albo średniej cen ofert w tej części – "
                "obowiązkowe wezwanie do wyjaśnień (art. 224 ust. 2 pkt 1 Pzp).")
    wv, sr = _f(swz.get("wartosc_zam_brutto")), _f(podsum.get("srednia_cen"))
    cz = []
    if wv and c and ponizej_30(c, [wv]):
        cz.append(f"o {_PR.liczba_pl((wv - c) / wv * 100, 1)}% od wartości zamówienia z VAT ({MO.zl(wv)})")
    if sr and c and ponizej_30(c, [sr]):
        cz.append(f"o {_PR.liczba_pl((sr - c) / sr * 100, 1)}% od średniej cen ofert ({MO.zl(sr)})")
    return (f"Cena {MO.zl(c or 0)} jest niższa " + " i ".join(cz) if cz else f"Cena {MO.zl(c or 0)} jest niższa o co najmniej 30% od wartości zamówienia z VAT albo średniej cen ofert") \
        + " – obowiązkowe wezwanie do wyjaśnień (art. 224 ust. 2 pkt 1 Pzp)."


def _ranking_jeden(swz, oferty):
    """Punktacja według kryteriów (wzory min/max), rażąco niska cena (art. 224 Pzp) i ranking ofert nieodrzuconych."""
    kryt = swz.get("kryteria") or [{"nazwa": "Cena", "waga": 100, "typ": "min"}]
    waz = [o for o in oferty if not odrzucona(o)]
    # art. 224 ust. 2 pkt 1 Pzp: średnia cen wszystkich złożonych ofert z wyłączeniem odrzuconych na podstawie art. 226 ust. 1 pkt 1, 5a i 10
    # (u zamawiającego prywatnego – bez ofert do odrzucenia); wspólna reguła z „Rynkowością cen”
    ceny_sr = ceny_do_sredniej_224(oferty, swz.get("prywatny"))
    srednia = sum(ceny_sr) / len(ceny_sr) if ceny_sr else None
    budzet = _f(swz.get("kwota_budzet_brutto"))
    wartosc_vat = _f(swz.get("wartosc_zam_brutto"))  # wartość zamówienia z VAT ustalona przed wszczęciem (art. 224 ust. 2 pkt 1) – nie kwota na sfinansowanie
    k_naj = max(kryt, key=lambda k: _f(k.get("waga")) or 0) if kryt else None  # kryterium o najwyższej wadze (art. 248 ust. 1)
    for o in oferty:
        w = o.get("wynik") or {}
        pkt, szcz, niezg = 0.0, {}, []
        for k in kryt:
            nazwa, waga, typ = k.get("nazwa", ""), _f(k.get("waga")) or 0, (k.get("typ") or "min").lower()
            jc = jest_cena(k)
            val = _f(w.get("cena_brutto")) if jc else _f((w.get("wartosci_kryteriow") or {}).get(nazwa))
            wartosci = []
            for x in waz:
                wx = x.get("wynik") or {}
                v = _f(wx.get("cena_brutto")) if jc else _f((wx.get("wartosci_kryteriow") or {}).get(nazwa))
                if v is not None:
                    wartosci.append(v)
            p = 0.0
            if val is not None and wartosci:
                if typ == "min" and val > 0:
                    p = min(wartosci) / val * waga
                elif typ == "max" and _f(k.get("od")) is not None and _f(k.get("do")) is not None and _f(k.get("do")) > _f(k.get("od")):
                    od_, do_ = _f(k.get("od")), _f(k.get("do"))  # zakres z SWZ: „od” = 0 pkt, „do” i więcej = pełna waga
                    p = max(0.0, (min(val, do_) - od_) / (do_ - od_)) * waga
                    if val < od_:  # poniżej minimum z SWZ – treść oferty niezgodna z warunkami zamówienia (art. 226 ust. 1 pkt 5)
                        niezg.append(f"„{nazwa}”: zaoferowano {_PR.pl_liczby(f'{val:g}')} – poniżej minimum {_PR.pl_liczby(f'{od_:g}')} wymaganego w SWZ; "
                                     "oferta do odrzucenia (art. 226 ust. 1 pkt 5 Pzp)")
                elif typ == "max" and max(wartosci) > 0:
                    p = val / max(wartosci) * waga
                elif typ == "punktowe":
                    p = min(val, waga)
            szcz[nazwa] = _pkt2(p)
            pkt += p
        o["punkty"] = _pkt2(pkt)
        o["punkty_szczegoly"] = szcz
        o["niezgodna_kryterium"] = niezg
        c = _f(w.get("cena_brutto"))
        o["razaco_niska"] = bool(c and not w.get("wyjasnione") and ((srednia and len(ceny_sr) >= 2 and ponizej_30(c, ceny_sr))
                                                                  or (wartosc_vat and ponizej_30(c, [wartosc_vat]))))
        o["ponad_budzet"] = bool(c and budzet and c > budzet)
    # art. 248: przy równej punktacji – wyższa ocena w kryterium o najwyższej wadze (ust. 1), potem niższa cena (ust. 2)
    klucz = lambda o: (-o["punkty"], -((o["punkty_szczegoly"] or {}).get(k_naj.get("nazwa", ""), 0) if k_naj else 0),
                       _f((o.get("wynik") or {}).get("cena_brutto")) or float("inf"))
    kolej = sorted([o for o in oferty if o in waz], key=klucz)
    for i, o in enumerate(kolej, 1):
        o["miejsce"] = i
    for o in oferty:
        if o not in waz:
            o["miejsce"] = None
    ostrz, remis, art248 = [], [], ""
    if len(kolej) >= 2 and kolej[0]["punkty"] == kolej[1]["punkty"]:
        a, b = kolej[0], kolej[1]
        naz = lambda x: f"nr {x.get('nr') or '?'} ({x.get('nazwa') or ''})"
        if klucz(a) == klucz(b):
            remis = [x["id"] for x in kolej if klucz(x) == klucz(a)]
            ostrz.append("Remis – oferty " + ", ".join(naz(x) for x in kolej if x["id"] in remis) + f" mają po {_pkt(a['punkty'])} pkt, taką samą ocenę "
                         "w kryterium o najwyższej wadze i taką samą cenę: wezwij wykonawców do złożenia ofert dodatkowych (art. 248 ust. 3 Pzp); "
                         "takie same oferty dodatkowe = unieważnienie postępowania (art. 255 pkt 4 Pzp).")
        elif klucz(a)[1] != klucz(b)[1]:
            art248 = (f"Oferty {naz(a)} i {naz(b)} uzyskały jednakową łączną liczbę punktów ({_pkt(a['punkty'])}) – zgodnie z art. 248 ust. 1 Pzp "
                      f"wybrano ofertę z najwyższą oceną w kryterium o najwyższej wadze („{k_naj.get('nazwa', '')}”).")
        else:
            art248 = (f"Oferty {naz(a)} i {naz(b)} uzyskały jednakową łączną liczbę punktów ({_pkt(a['punkty'])}) i taką samą ocenę w kryterium "
                      "o najwyższej wadze – zgodnie z art. 248 ust. 2 Pzp wybrano ofertę z najniższą ceną.")
    # najkorzystniejsza: najwyżej oceniona oferta bez nierozstrzygniętych kwestii (braki, wyjaśnienia, rażąco niska cena, niezgodność z SWZ)
    pewne = [o for o in kolej if (o.get("wynik") or {}).get("status") == "prawidłowa" and not o.get("razaco_niska") and not o.get("niezgodna_kryterium")]
    naj = pewne[0] if pewne and pewne[0] is kolej[0] else (kolej[0] if kolej and not pewne else (pewne[0] if pewne else None))
    if remis:  # art. 248 ust. 3 – bez oferty najkorzystniejszej do czasu ofert dodatkowych
        naj = None
    warunkowo = bool(kolej) and (naj is not kolej[0] or not pewne or bool(remis))
    for o in kolej:
        for t in o.get("niezgodna_kryterium") or []:
            ostrz.append(f"Oferta nr {o.get('nr') or '?'} – {o.get('nazwa') or ''}: {t}.")
    return {"srednia_cen": round(srednia, 2) if srednia else None, "budzet": budzet, "najkorzystniejsza": naj["id"] if naj else None,
            "pierwsza_w_rankingu": kolej[0]["id"] if kolej else None, "warunkowo": warunkowo, "remis_248": remis, "art248": art248, "ostrzezenia": ostrz}


def podstawa_odrzucenia(o):
    """Uzasadnienie faktyczne i prawne odrzucenia (art. 253 ust. 1 pkt 2): przepis wybrany przez komisję + uzasadnienie faktyczne."""
    w = o.get("wynik") or {}
    t = str(w.get("podstawa_odrzucenia") or o.get("powod_odrzucenia") or "").strip()
    p = _punkt_226(o)
    przepis = f"art. 226 ust. 1 pkt {p} Pzp ({PUNKTY_226[p]})" if p in PUNKTY_226 else ""
    if przepis and not re.search(r"226\s*ust\.\s*1\s*pkt", t):
        t = przepis + (" – " + t if t else "")
    return t or "[UZUPEŁNIJ: podstawa prawna i faktyczna]"


def siedziba(o):
    """Siedziba albo miejsce wykonywania działalności wykonawcy (art. 253 ust. 1 pkt 1 Pzp) – z wpisu oferty albo odczytana z oferty."""
    return str(o.get("adres") or (o.get("wynik") or {}).get("wykonawca_adres") or "").strip() or "[UZUPEŁNIJ: siedziba]"


def tekst_kwoty_255(swz, oferty, podsum):
    """Cena najkorzystniejszej oferty ponad kwotę na sfinansowanie (art. 255 pkt 3): decyzja zamawiającego – zwiększenie kwoty albo unieważnienie."""
    zw = swz.get("zwiekszona_kwota") or {}
    if zw.get("do"):
        return (f"Zamawiający zwiększył kwotę przeznaczoną na sfinansowanie zamówienia z {MO.zl(_f(zw.get('z')) or 0)} do {MO.zl(_f(zw.get('do')))} brutto "
                f"(do ceny najkorzystniejszej oferty{', ' + zw['data'] if zw.get('data') else ''}) – art. 255 pkt 3 Pzp.")
    naj = next((o for o in oferty if o.get("id") == podsum.get("najkorzystniejsza")), None)
    if not naj or not naj.get("ponad_budzet") or not podsum.get("budzet"):
        return ""
    c = _f((naj.get("wynik") or {}).get("cena_brutto")) or 0
    return (f"Cena najkorzystniejszej oferty ({MO.zl(c)}) przewyższa kwotę, którą Zamawiający zamierza przeznaczyć na sfinansowanie zamówienia "
            f"({MO.zl(podsum['budzet'])}), o {MO.zl(c - podsum['budzet'])}. Decyzja Zamawiającego: [UZUPEŁNIJ: zwiększenie kwoty do ceny najkorzystniejszej "
            "oferty albo unieważnienie postępowania – art. 255 pkt 3 Pzp].")


def blokada_informacji(swz, oferty, podsum):
    """Powód, dla którego nie można przygotować informacji o wyborze (pusty – można): wybór wstrzymany, brak oferty do wyboru (art. 255 pkt 1–2),
    cena ponad kwotę bez decyzji o zwiększeniu kwoty (art. 255 pkt 3)."""
    wstrz = wstrzymany_wybor(oferty, podsum)
    if wstrz:  # art. 253: informacja o wyborze dopiero po rozstrzygnięciu oferty najwyżej ocenionej (wyjaśnienia albo odrzucenie)
        return "Informacji o wyborze nie można jeszcze przygotować. " + " ".join(wstrz)
    if podsum.get("czesci"):
        return ""
    pryw = swz.get("prywatny")
    if not podsum.get("najkorzystniejsza"):
        if oferty and not any(o.get("wynik") for o in oferty):
            return "Informacji o wyborze nie można jeszcze przygotować – najpierw zbadaj oferty i wpisz ich ceny (krok 4)."
        if pryw:
            return "Nie ma oferty do wyboru – " + ("nie złożono żadnej oferty" if not oferty else "wszystkie oferty odrzucono") + \
                ". Ponów zapytanie ofertowe albo zaproś innych wykonawców."
        return ("Nie ma oferty do wyboru – " + ("nie złożono żadnej oferty: postępowanie podlega unieważnieniu (art. 255 pkt 1 Pzp)" if not oferty else
                "wszystkie oferty podlegają odrzuceniu: postępowanie podlega unieważnieniu (art. 255 pkt 2 Pzp)")
                + ". Przygotuj zawiadomienie o unieważnieniu postępowania (art. 260 Pzp).")
    if not pryw and tekst_kwoty_255(swz, oferty, podsum) and not (swz.get("zwiekszona_kwota") or {}).get("do"):
        return ("Informacji o wyborze nie można jeszcze przygotować – " + tekst_kwoty_255(swz, oferty, podsum).replace("Decyzja Zamawiającego: [UZUPEŁNIJ: ", "Zdecyduj: ")
                .rstrip("].") + ". Przycisk „Zwiększam kwotę do ceny oferty” w kroku 5 zapisuje decyzję.")
    return ""


def protokol_docx(sciezka, swz, oferty, podsum, zamawiajacy):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    MO._akapit(d, f"{zamawiajacy or swz.get('zamawiajacy') or '[UZUPEŁNIJ: Zamawiający]'}", pogrub=True)
    MO._akapit(d, "PROTOKÓŁ Z BADANIA I OCENY OFERT", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"Postępowanie: {swz.get('nazwa_zamowienia') or '[UZUPEŁNIJ]'}{(' nr ' + swz['numer']) if swz.get('numer') else ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    budzet_ = podsum.get("budzet") or _f(swz.get("kwota_budzet_brutto"))
    MO._akapit(d, f"Kwota przeznaczona na sfinansowanie zamówienia: {MO.zl(budzet_) if budzet_ else '[UZUPEŁNIJ]'} brutto. "
                  f"Liczba złożonych ofert: {len(oferty)}. Średnia cena ofert nieodrzuconych: {MO.zl(podsum['srednia_cen']) if podsum.get('srednia_cen') else '–'}.")
    MO._akapit(d, "1. Kryteria oceny ofert", pogrub=True)
    MO._tabela(d, [["Kryterium", "Waga", "Sposób oceny"]] + [[k.get("nazwa", ""), _waga(k.get("waga")), _sposob_oceny(k)] for k in swz.get("kryteria") or []])
    MO._akapit(d, "2. Badanie ofert", pogrub=True)
    for o in oferty:
        w = o.get("wynik") or {}
        MO._akapit(d, f"Oferta nr {o.get('nr')} – {o.get('nazwa')}{(' (NIP ' + o['nip'] + ')') if o.get('nip') else ''}: cena {MO.zl(_f(w.get('cena_brutto')) or 0)} brutto – "
                      f"status: {w.get('status', 'nie zbadano')}.", pogrub=True)
        for et, kl in (("Braki / do uzupełnienia", "braki"), ("Niezgodności z SWZ", "niezgodnosci"), ("Do wyjaśnienia", "do_wyjasnienia")):
            if w.get(kl):
                MO._akapit(d, f"{et}: " + "; ".join(_t(x) for x in w[kl]))
        if w.get("bledy_rachunkowe"):
            MO._akapit(d, "Błędy rachunkowe: " + "; ".join(f"{b.get('opis', '')} → {b.get('poprawka', '')}" for b in w["bledy_rachunkowe"] if isinstance(b, dict)))
        t224 = _art224_tekst(o, swz, podsum)
        if t224:
            MO._akapit(d, t224, kursywa=True)
        if w.get("podstawa_odrzucenia") or (o.get("odrzucona") and _punkt_226(o)):
            MO._akapit(d, f"Podstawa odrzucenia: {podstawa_odrzucenia(o)}")
    MO._akapit(d, "3. Ocena ofert nieodrzuconych", pogrub=True)
    if podsum.get("czesci"):
        _czesci_docx(d, swz, oferty, podsum, "protokol")
        _weryfikacja_docx(d, oferty)
        MO._akapit(d, "Protokół przygotowany pomocniczo na podstawie analizy AI – wymaga weryfikacji i zatwierdzenia przez komisję przetargową.", kursywa=True, rozmiar=9)
        _docx_bez_pzp(d) if swz.get("prywatny") else None
        MO._akapit(d, "\n\n" + podpisy(swz))
        MO.zapisz_z_zaznaczeniem(d, sciezka)
        return
    kryt = [k.get("nazwa", "") for k in swz.get("kryteria") or []]
    wiersze = [["Miejsce", "Wykonawca", "Cena brutto"] + kryt + ["Razem pkt"]]
    for o in sorted([o for o in oferty if o.get("miejsce")], key=lambda o: o["miejsce"]):
        wiersze.append([str(o["miejsce"]), o.get("nazwa", ""), MO.zl(_f((o.get("wynik") or {}).get("cena_brutto")) or 0)]
                       + [_pkt(o['punkty_szczegoly'].get(k, 0)) for k in kryt] + [_pkt(o['punkty'])])
    MO._tabela(d, wiersze)
    naj = next((o for o in oferty if o.get("id") == podsum.get("najkorzystniejsza")), None)
    wstrz = wstrzymany_wybor(oferty, podsum)
    if wstrz:  # nie wskazujemy oferty z 2. miejsca jako najkorzystniejszej, dopóki oferta z 1. miejsca nie jest rozstrzygnięta
        MO._akapit(d, "Wybór najkorzystniejszej oferty wstrzymany do czasu rozstrzygnięcia: " + " ".join(wstrz[:-1]), pogrub=True)
        if naj and naj.get("id") != podsum.get("pierwsza_w_rankingu"):
            MO._akapit(d, f"Najwyżej oceniona oferta bez zastrzeżeń (do wyboru, jeżeli oferta z 1. miejsca zostanie odrzucona): "
                          f"nr {naj.get('nr')} – {naj['nazwa']}, {_pkt(naj['punkty'])} pkt.")
    else:
        MO._akapit(d, f"Najkorzystniejsza oferta: {naj['nazwa'] + ' – ' + _pkt(naj['punkty']) + ' pkt' if naj else '–'}.", pogrub=True)
    if podsum.get("art248"):
        MO._akapit(d, podsum["art248"])
    for t in podsum.get("ostrzezenia") or []:
        if "248 ust. 3" not in t or not wstrz:
            MO._akapit(d, f"Uwaga: {t}", kursywa=True)
    t255 = tekst_kwoty_255(swz, oferty, podsum)
    if t255:
        MO._akapit(d, t255, pogrub=True)
    _weryfikacja_docx(d, oferty)
    MO._akapit(d, "Protokół przygotowany pomocniczo na podstawie analizy AI – wymaga weryfikacji i zatwierdzenia przez komisję przetargową.", kursywa=True, rozmiar=9)
    _docx_bez_pzp(d) if swz.get("prywatny") else None
    MO._akapit(d, "\n\n" + podpisy(swz))
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def _weryfikacja_docx(d, oferty):
    """Weryfikacja wykonawców (referencje, doświadczenie, uprawnienia, polisa, rejestry) – w protokole wyboru."""
    ofw = [o for o in oferty if o.get("weryfikacja")]
    if not ofw:
        return
    MO._akapit(d, "Weryfikacja wykonawców", pogrub=True)
    st = {"potwierdzona": "potwierdzona", "sprzeczna": "z sygnałami nieprawdziwości", "niepotwierdzona": "niepotwierdzona"}
    for o in ofw:
        W = o["weryfikacja"]
        P = W.get("podsumowanie") or {}
        MO._akapit(d, f"{o.get('nazwa')}: referencje – " + ", ".join(f"{st[k]} {P.get(k, 0)}" for k in st) + f" (sprawdzono {W.get('data') or ''}).")
        for k, t in W.get("wykonawca_sygnaly") or []:
            if k != "zielony":
                MO._akapit(d, f"– {t}", rozmiar=9)
        for pole, nazwa in (("uprawnienia", "uprawnienia budowlane (e-CRUB)"), ("krz", "Krajowy Rejestr Zadłużonych")):
            pw = (W.get("potwierdzenia") or {}).get(pole) or {}
            if any(x.get("pole") == pole for x in W.get("do_sprawdzenia") or []):
                MO._akapit(d, f"– {nazwa}: " + {"potwierdzone": "sprawdzone – bez zastrzeżeń", "zastrzezenia": "sprawdzone – zastrzeżenia"}.get(pw.get("wynik"), "nie sprawdzono")
                           + (f" ({pw.get('data')})" if pw.get("data") else ""), rozmiar=9)
        if W.get("do_doslania"):
            MO._akapit(d, "– do dosłania: " + "; ".join(W["do_doslania"]), rozmiar=9)


def _czesci_docx(d, swz, oferty, podsum, rodzaj):
    """Wyniki według części: punktacja ofert złożonych na daną część i oferta najkorzystniejsza (protokół / informacja o wyborze)."""
    for c in podsum.get("czesci") or []:
        nr = str(c.get("nr"))
        MO._akapit(d, f"Część {c.get('nr')} – {c.get('nazwa') or ''}", pogrub=True)
        kryt = [k.get("nazwa", "") for k in (next((x for x in swz.get("czesci") or [] if str(x.get("nr")) == nr), {}).get("kryteria") or swz.get("kryteria") or [])]
        ofe = sorted([o for o in oferty if (o.get("czesci_wyniki") or {}).get(nr, {}).get("miejsce")], key=lambda o: o["czesci_wyniki"][nr]["miejsce"])
        if not ofe:
            MO._akapit(d, "Brak ofert podlegających ocenie w tej części." + (" Postępowanie w tej części podlega unieważnieniu (art. 255 pkt 1 Pzp)."
                                                                             if not c.get("ofert") else ""))
            continue
        inf = rodzaj == "informacja"  # art. 253 ust. 1 pkt 1 – siedziby wykonawców
        MO._tabela(d, [["Miejsce", "Wykonawca"] + (["Siedziba"] if inf else []) + ["Cena brutto"] + kryt + ["Razem pkt"]] +
                   [[str(o["czesci_wyniki"][nr]["miejsce"]), o.get("nazwa", "")] + ([siedziba(o)] if inf else []) + [MO.zl(o["czesci_wyniki"][nr]["cena_brutto"] or 0)]
                    + [_pkt(o['czesci_wyniki'][nr]['punkty_szczegoly'].get(k, 0)) for k in kryt] + [_pkt(o['czesci_wyniki'][nr]['punkty'])] for o in ofe])
        naj = next((o for o in oferty if o.get("id") == c.get("najkorzystniejsza")), None)
        if c.get("warunkowo") and (naj or c.get("remis_248")):  # oferta z 1. miejsca nierozstrzygnięta albo remis – bez wskazania najkorzystniejszej
            MO._akapit(d, f"Wybór w części {c.get('nr')} wstrzymany: " + " ".join(x.split(": ", 1)[-1] for x in wstrzymany_wybor(oferty, {"czesci": [c]})[:-1]), pogrub=True)
        elif naj:
            r = naj["czesci_wyniki"][nr]
            MO._akapit(d, f"Najkorzystniejsza oferta w części {c.get('nr')}: nr {naj.get('nr')} – {naj.get('nazwa')}"
                          f"{(', z siedzibą: ' + siedziba(naj)) if rodzaj == 'informacja' else ''}"
                          f"{(', NIP ' + naj['nip']) if naj.get('nip') and rodzaj == 'informacja' else ''}, cena {MO.zl(r['cena_brutto'] or 0)} brutto, "
                          f"{_pkt(r['punkty'])} pkt.", pogrub=True)
    for t in podsum.get("ostrzezenia") or []:
        MO._akapit(d, f"Uwaga: {t}", kursywa=True)


def informacja_docx(sciezka, swz, oferty, podsum, zamawiajacy):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    bl = blokada_informacji(swz, oferty, podsum)
    if bl:
        raise ValueError(bl)
    d = MO._doc()
    MO._akapit(d, f"{dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, f"{zamawiajacy or swz.get('zamawiajacy') or '[UZUPEŁNIJ: Zamawiający]'}", pogrub=True)
    MO._akapit(d, "INFORMACJA O WYBORZE NAJKORZYSTNIEJSZEJ OFERTY", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"dotyczy: {swz.get('nazwa_zamowienia') or '[UZUPEŁNIJ]'}{(' nr ' + swz['numer']) if swz.get('numer') else ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    if podsum.get("czesci"):
        MO._akapit(d, "Działając na podstawie art. 253 ustawy Prawo zamówień publicznych, Zamawiający informuje o wyborze najkorzystniejszych ofert "
                      "w poszczególnych częściach zamówienia.")
        _czesci_docx(d, swz, oferty, podsum, "informacja")
        MO._akapit(d, "\n\n..........................................\n(podpis Kierownika Zamawiającego)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
        _docx_bez_pzp(d) if swz.get("prywatny") else None
        MO.zapisz_z_zaznaczeniem(d, sciezka)
        return
    naj = next((o for o in oferty if o.get("id") == podsum.get("najkorzystniejsza")), None)
    if naj:
        MO._akapit(d, f"Działając na podstawie art. 253 ustawy Prawo zamówień publicznych, Zamawiający informuje, że jako najkorzystniejszą wybrano ofertę "
                      f"nr {naj.get('nr')} złożoną przez: {naj.get('nazwa')}, z siedzibą: {siedziba(naj)}{(', NIP ' + naj['nip']) if naj.get('nip') else ''}, z ceną "
                      f"{MO.zl(_f((naj.get('wynik') or {}).get('cena_brutto')) or 0)} brutto, która uzyskała {_pkt(naj['punkty'])} pkt.")
        MO._akapit(d, "Uzasadnienie: oferta jest zgodna z warunkami zamówienia, nie podlega odrzuceniu, a wykonawca nie podlega wykluczeniu; "
                      "oferta uzyskała najwyższą liczbę punktów w kryteriach oceny ofert." + (" " + podsum["art248"] if podsum.get("art248") else ""))
    kryt = [k.get("nazwa", "") for k in swz.get("kryteria") or []]
    MO._akapit(d, "Punktacja ofert:", pogrub=True)
    MO._tabela(d, [["Nr", "Wykonawca", "Siedziba"] + kryt + ["Razem"]] +
               [[str(o.get("nr")), o.get("nazwa", ""), siedziba(o)] + [_pkt(o['punkty_szczegoly'].get(k, 0)) for k in kryt] + [_pkt(o['punkty'])]
                for o in sorted([o for o in oferty if o.get("miejsce")], key=lambda o: o["miejsce"])])
    odrz = [o for o in oferty if not o.get("miejsce")]
    if odrz:
        MO._akapit(d, "Oferty odrzucone:", pogrub=True)
        for o in odrz:
            MO._akapit(d, f"Oferta nr {o.get('nr')} – {o.get('nazwa')} ({siedziba(o)}): {podstawa_odrzucenia(o)}")
    MO._akapit(d, "\n\n..........................................\n(podpis Kierownika Zamawiającego)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _docx_bez_pzp(d) if swz.get("prywatny") else None
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def wezwanie_docx(sciezka, swz, o, zamawiajacy):
    """Wezwanie wykonawcy: wyjaśnienia (art. 223), uzupełnienie (art. 128), wyjaśnienie ceny (art. 224)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    w = o.get("wynik") or {}
    d = MO._doc()
    MO._akapit(d, f"{dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, f"{zamawiajacy or swz.get('zamawiajacy') or '[UZUPEŁNIJ: Zamawiający]'}")
    MO._akapit(d, f"{o.get('nazwa')}{(chr(10) + 'NIP ' + o['nip']) if o.get('nip') else ''}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, "WEZWANIE", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"dotyczy: {swz.get('nazwa_zamowienia') or '[UZUPEŁNIJ]'}{(' nr ' + swz['numer']) if swz.get('numer') else ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    import kontrola_zam as KO
    termin = KO.nastepny_roboczy(dt.date.today() + dt.timedelta(days=5)).strftime("%d.%m.%Y")  # art. 115 k.c. – soboty i święta
    n = 0
    if w.get("braki"):
        n += 1
        MO._akapit(d, f"{n}. Na podstawie art. 128 ust. 1 Pzp wzywamy do złożenia / uzupełnienia / poprawienia dokumentów:", pogrub=True)
        for x in w["braki"]:
            MO._akapit(d, _t(x), styl="List Bullet")
    if w.get("do_wyjasnienia") or w.get("niezgodnosci"):
        n += 1
        MO._akapit(d, f"{n}. Na podstawie art. 223 ust. 1 Pzp prosimy o wyjaśnienie treści oferty:", pogrub=True)
        for x in (w.get("do_wyjasnienia") or []) + (w.get("niezgodnosci") or []):
            MO._akapit(d, _t(x), styl="List Bullet")
    if o.get("razaco_niska"):
        n += 1
        MO._akapit(d, f"{n}. Na podstawie art. 224 ust. 1 Pzp wzywamy do udzielenia wyjaśnień, w tym złożenia dowodów, dotyczących wyliczenia ceny "
                      "(cena niższa o co najmniej 30% od średniej arytmetycznej ofert lub od wartości zamówienia).", pogrub=True)
    if not n:
        MO._akapit(d, "[UZUPEŁNIJ: treść wezwania]")
    MO._akapit(d, f"Odpowiedź prosimy złożyć w terminie do {termin} r. za pośrednictwem platformy, na której prowadzone jest postępowanie.")
    MO._akapit(d, "\n\n..........................................\n(podpis Zamawiającego)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _docx_bez_pzp(d) if swz.get("prywatny") else None
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# ---------------------------------------------------------------- informacja z otwarcia ofert, wezwanie do podmiotowych środków dowodowych
def unijne(swz):
    """Postępowanie od progów UE: wskazanie z kreatora (swz["unijne"]) albo – gdy brak – z trybu odczytanego z SWZ."""
    if isinstance(swz.get("unijne"), bool):
        return swz["unijne"]
    return bool(re.search(r"przetarg nieograniczony|przetarg ograniczony|dialog|negocjacje z ogłoszeniem|partnerstwo|unijn|dzienniku urzędowym",
                          str(swz.get("tryb") or "").lower()))


def informacja_otwarcia_docx(sciezka, swz, oferty, zamawiajacy):
    """Informacja z otwarcia ofert (art. 222 ust. 5 Pzp): wykonawcy, siedziby, ceny; kwota na sfinansowanie (art. 222 ust. 4)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    MO._akapit(d, zamawiajacy or swz.get("zamawiajacy") or "[UZUPEŁNIJ: Zamawiający]", rozmiar=9)
    MO._akapit(d, f"[UZUPEŁNIJ: miejscowość], {dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, "INFORMACJA Z OTWARCIA OFERT", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"dotyczy: {swz.get('nazwa_zamowienia') or '[UZUPEŁNIJ]'}{(' nr ' + swz['numer']) if swz.get('numer') else ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "Działając na podstawie art. 222 ust. 5 ustawy Prawo zamówień publicznych, Zamawiający udostępnia na stronie internetowej "
                  "prowadzonego postępowania informacje o otwarciu ofert. Otwarcie ofert nastąpiło w dniu [UZUPEŁNIJ: data i godzina].")
    kw = _f(swz.get("kwota_budzet_brutto"))
    MO._akapit(d, "Kwota, jaką Zamawiający zamierza przeznaczyć na sfinansowanie zamówienia (art. 222 ust. 4): "
                  + (f"{kw:,.2f} zł brutto".replace(",", " ").replace(".", ",") if kw else "[UZUPEŁNIJ]") + ".")
    w = [["Lp.", "Wykonawca", "Siedziba / miejsce prowadzenia działalności", "Cena brutto [zł]"]]
    for i, o in enumerate([x for x in oferty if isinstance(x, dict)], 1):
        c = _f((o.get("wynik") or {}).get("cena_brutto") or o.get("cena_brutto"))
        w.append([str(i), str(o.get("nazwa") or "[UZUPEŁNIJ]"), str(o.get("adres") or "[UZUPEŁNIJ: siedziba]"),
                  f"{c:,.2f}".replace(",", " ").replace(".", ",") if c else "[UZUPEŁNIJ]"])
    if len(w) > 1:
        MO._tabela(d, w)
    else:
        MO._akapit(d, "[UZUPEŁNIJ: wykonawcy, których oferty zostały otwarte, ich siedziby i ceny]")
    MO._akapit(d, "\n\n..........................................\n(podpis Zamawiającego)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def wezwanie_srodki_docx(sciezka, swz, o, zamawiajacy, unijne_=False):
    """Wezwanie wykonawcy, którego oferta została najwyżej oceniona, do złożenia podmiotowych środków dowodowych:
    od progów UE art. 126 ust. 1 (termin nie krótszy niż 10 dni), poniżej – art. 274 ust. 1 (nie krótszy niż 5 dni)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    dni = 10 if unijne_ else 5
    d = MO._doc()
    MO._akapit(d, f"{dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, zamawiajacy or swz.get("zamawiajacy") or "[UZUPEŁNIJ: Zamawiający]")
    MO._akapit(d, f"{o.get('nazwa')}{(chr(10) + 'NIP ' + o['nip']) if o.get('nip') else ''}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, "WEZWANIE DO ZŁOŻENIA PODMIOTOWYCH ŚRODKÓW DOWODOWYCH", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"dotyczy: {swz.get('nazwa_zamowienia') or '[UZUPEŁNIJ]'}{(' nr ' + swz['numer']) if swz.get('numer') else ''}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"Działając na podstawie {'art. 126 ust. 1' if unijne_ else 'art. 274 ust. 1'} ustawy Prawo zamówień publicznych, Zamawiający "
                  "wzywa Wykonawcę, którego oferta została najwyżej oceniona, do złożenia aktualnych na dzień złożenia podmiotowych środków "
                  "dowodowych:")
    L = [_t(x) for x in (swz.get("podmiotowe_srodki") or []) if _t(x)]
    for x in L or ["[UZUPEŁNIJ: podmiotowe środki dowodowe wskazane w SWZ – rozdział …]"]:
        MO._akapit(d, x, styl="List Bullet")
    import kontrola_zam as KO
    termin = KO.nastepny_roboczy(dt.date.today() + dt.timedelta(days=dni))  # art. 115 k.c. – soboty, niedziele i święta
    MO._akapit(d, f"Dokumenty należy złożyć w terminie do dnia {termin:%d.%m.%Y} r. (nie krócej niż {dni} dni od dnia wezwania) za pośrednictwem "
                  "platformy, na której prowadzone jest postępowanie, w formie lub postaci elektronicznej wskazanej w SWZ.")
    MO._akapit(d, "Zamawiający nie wzywa do złożenia dokumentów, które może uzyskać za pomocą bezpłatnych i ogólnodostępnych baz danych "
                  "(np. KRS, CEIDG), jeżeli Wykonawca wskazał dane umożliwiające dostęp do nich (art. 127 ust. 1 pkt 1 Pzp) – "
                  "[UZUPEŁNIJ: usuń z listy dokumenty, które Zamawiający pobierze sam].", rozmiar=9)
    MO._akapit(d, "\n\n..........................................\n(podpis Zamawiającego)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
