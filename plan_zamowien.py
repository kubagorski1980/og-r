# -*- coding: utf-8 -*-
"""
Roczny plan zamówień i plan postępowań o udzielenie zamówień (art. 23 Pzp; wzór – rozporządzenie MRPiT z 18.12.2020, Dz.U. 2020 poz. 2362).
- Plan postępowań: zamawiający z art. 4 pkt 1 i 2 Pzp i ich związki; najpóźniej 30 dni od przyjęcia budżetu / planu finansowego; BZP i strona
  internetowa; obowiązek aktualizacji (zmiana, dodanie, rezygnacja – każda aktualizacja to nowa wersja).
- Obejmuje zamówienia, do których stosuje się Pzp (od 1.01.2026 r. od 170 000 zł netto – moduł progi); zamówienia poniżej progu i wyłączone –
  tylko w planie wewnętrznym (pilnowanie zakazu dzielenia zamówień, art. 29–30).
- Pozycja: przedmiot, rodzaj, przewidywany tryb/procedura (zamknięte listy wzoru), orientacyjna wartość netto, termin wszczęcia (miesiąc albo kwartał),
  informacje dodatkowe.
"""
import datetime as dt
import re
import uuid

import progi as PR
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

RODZAJE = {"roboty": "Roboty budowlane", "dostawy": "Dostawy", "uslugi": "Usługi"}
TRYBY_KRAJ = ["tryb podstawowy – bez negocjacji (art. 275 pkt 1)", "tryb podstawowy – negocjacje fakultatywne (art. 275 pkt 2)",
              "tryb podstawowy – negocjacje obligatoryjne (art. 275 pkt 3)", "partnerstwo innowacyjne", "negocjacje bez ogłoszenia",
              "zamówienie z wolnej ręki", "umowa ramowa"]
TRYBY_UE = ["przetarg nieograniczony", "przetarg ograniczony", "negocjacje z ogłoszeniem", "dialog konkurencyjny", "partnerstwo innowacyjne",
            "negocjacje bez ogłoszenia", "zamówienie z wolnej ręki", "umowa ramowa", "dynamiczny system zakupów"]
RODZAJE_ZAMAWIAJACEGO = ["jednostka samorządu terytorialnego", "związek jednostek samorządu terytorialnego / związek metropolitalny",
                         "organ władzy publicznej (administracja rządowa, kontrola państwowa, sąd, trybunał)", "jednostka budżetowa",
                         "samorządowy zakład budżetowy", "agencja wykonawcza / instytucja gospodarki budżetowej / państwowy fundusz celowy",
                         "ZUS, KRUS, NFZ", "samodzielny publiczny zakład opieki zdrowotnej", "uczelnia publiczna / PAN i jej jednostki",
                         "państwowa lub samorządowa instytucja kultury", "inna państwowa lub samorządowa osoba prawna (zadania publiczne)",
                         "inna państwowa jednostka organizacyjna bez osobowości prawnej", "związek podmiotów z powyższych grup",
                         "inny zamawiający (plan nieobowiązkowy)"]
INFO_DODATKOWE = {"konsultacje": "wstępne konsultacje rynkowe", "innowacyjne": "zamówienie innowacyjne", "spoleczne": "aspekty społeczne",
                  "srodowiskowe": "aspekty środowiskowe", "zastrzezone": "zamówienie zastrzeżone (art. 94)"}
STATUSY = ["zaplanowane", "wszczęte", "udzielone", "unieważnione", "rezygnacja"]
MIESIACE = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]
POLA_ZMIANY = ("przedmiot", "rodzaj", "tryb", "wartosc", "termin_typ", "termin", "info")


def _f(v):
    return liczba(v)


def nowy_plan(rok):
    return {"rok": int(rok), "rodzaj_zamawiajacego": RODZAJE_ZAMAWIAJACEGO[0], "centralny": False, "data_budzetu": "", "numer_bzp": "",
            "pozycje": [], "wersje": [], "licznik": 0}


def kategoria(p, plan):
    """„wylaczone” / „ponizej_pzp” / „krajowe” / „unijne” – według wartości netto, rodzaju i progów obowiązujących w roku planu."""
    if p.get("wylaczone"):
        return "wylaczone"
    w = p.get("wartosc") or 0
    t = PR.tryb_wedlug_wartosci(w, p.get("rodzaj") or "roboty", f"{plan['rok']}-01-01", bool(plan.get("centralny")))
    if w < t["prog_pzp"]:
        return "ponizej_pzp"
    return "unijne" if w >= t["prog_ue_zl"] else "krajowe"


def oczysc_pozycje(r, plan):
    rodz = r.get("rodzaj") if r.get("rodzaj") in RODZAJE else "roboty"
    tt = "kwartal" if r.get("termin_typ") == "kwartal" else "miesiac"
    t = int(_f(r.get("termin")) or 1)
    t = max(1, min(4 if tt == "kwartal" else 12, t))
    p = {"id": r.get("id") or "", "przedmiot": str(r.get("przedmiot") or "")[:500], "rodzaj": rodz,
         "cpv": re.sub(r"[^\d\-, ]", "", str(r.get("cpv") or ""))[:60], "wartosc": round(_f(r.get("wartosc")) or 0, 2),
         "termin_typ": tt, "termin": t, "tryb": str(r.get("tryb") or ""),
         "info": {k: bool((r.get("info") or {}).get(k)) for k in INFO_DODATKOWE}, "info_tekst": str(r.get("info_tekst") or "")[:1000],
         "komorka": str(r.get("komorka") or "")[:120], "zrodlo": str(r.get("zrodlo") or "")[:200],
         "wylaczone": bool(r.get("wylaczone")), "podstawa_wylaczenia": str(r.get("podstawa_wylaczenia") or "")[:200],
         "status": r.get("status") if r.get("status") in STATUSY else "zaplanowane", "projekt_id": str(r.get("projekt_id") or ""),
         "id_bzp": str(r.get("id_bzp") or "")[:30]}
    if not p["id"]:
        plan["licznik"] = int(plan.get("licznik") or 0) + 1
        p["id"] = f"P-{plan['licznik']:03d}"
    kat = kategoria(p, plan)
    dozw = TRYBY_UE if kat == "unijne" else TRYBY_KRAJ
    if p["tryb"] not in dozw:
        p["tryb"] = dozw[0] if kat in ("krajowe", "unijne") else ""
    return p


def termin_opis(p):
    return f"{p['termin']} kwartał" if p["termin_typ"] == "kwartal" else MIESIACE[p["termin"] - 1]


def info_opis(p):
    return "; ".join([INFO_DODATKOWE[k] for k, v in (p.get("info") or {}).items() if v] + ([p["info_tekst"]] if p.get("info_tekst") else []))


def kontrole(plan):
    """Ostrzeżenia: tryb niezgodny z wartością, możliwe dzielenie zamówienia (art. 29–30), brak CPV, termin publikacji planu."""
    wyn = []
    aktywne = [p for p in plan.get("pozycje") or [] if p.get("status") != "rezygnacja"]
    for p in aktywne:
        kat = kategoria(p, plan)
        if kat == "unijne" and p.get("tryb") not in TRYBY_UE:
            wyn.append(("blad", p["id"], f"{p['id']}: wartość od progu unijnego – tryb z listy unijnej (np. przetarg nieograniczony)."))
        if kat == "krajowe" and p.get("tryb") not in TRYBY_KRAJ:
            wyn.append(("blad", p["id"], f"{p['id']}: wartość poniżej progów unijnych – tryb z listy krajowej (np. tryb podstawowy)."))
        if not p.get("cpv"):
            wyn.append(("info", p["id"], f"{p['id']}: brak kodu CPV – bez niego program nie sprawdzi dzielenia zamówienia."))
    grupy = {}
    for p in aktywne:
        if p.get("cpv") and not p.get("wylaczone"):
            # roboty: ta sama klasa CPV (5 cyfr) – liczy się obiekt/inwestycja; dostawy i usługi: ta sama grupa CPV (3 cyfry) – rodzajowo podobne
            grupy.setdefault((p["rodzaj"], re.sub(r"\D", "", p["cpv"])[:5 if p["rodzaj"] == "roboty" else 3]), []).append(p)
    for (rodz, cpv3), L in grupy.items():
        if len(L) < 2:
            continue
        suma = sum(p["wartosc"] for p in L)
        kat_sumy = kategoria({"rodzaj": rodz, "wartosc": suma}, plan)
        nizej = [p for p in L if kategoria(p, plan) != kat_sumy]
        if nizej:
            wyn.append(("ostrzezenie", ",".join(p["id"] for p in L),
                        f"Możliwe dzielenie zamówienia: {', '.join(p['id'] for p in L)} ({RODZAJE[rodz].lower()}, CPV {cpv3}…) – łącznie "
                        f"{zl(suma)} netto, co daje kategorię „{opis_kategorii(kat_sumy)}”, a osobno pozycje są niżej. Sprawdź tożsamość "
                        f"przedmiotową, czasową i podmiotową (art. 29–30 Pzp)"
                        + ("; przy robotach – czy to ten sam obiekt lub ta sama inwestycja" if rodz == "roboty" else "")
                        + "; przy tożsamych zamówieniach wartością jest suma."))
    d = plan.get("data_budzetu")
    if d and not plan.get("wersje"):
        try:
            termin = dt.date.fromisoformat(d) + dt.timedelta(days=30)
            dni = (termin - dt.date.today()).days
            wyn.append(("blad" if dni < 0 else "info", "", f"Termin publikacji planu w BZP i na stronie: {termin.isoformat()} "
                        + (f"(minął {-dni} dni temu)" if dni < 0 else f"(za {dni} dni)") + " – 30 dni od przyjęcia budżetu (art. 23 ust. 1)."))
        except ValueError:
            pass
    return [{"waga": w, "pozycje": i, "opis": o} for w, i, o in wyn]


def zl(v):
    return f"{v:,.0f}".replace(",", " ") + " zł"


def opis_kategorii(k):
    return {"wylaczone": "wyłączone z Pzp", "ponizej_pzp": "poniżej progu stosowania Pzp", "krajowe": "Pzp – poniżej progów UE",
            "unijne": "Pzp – od progów UE"}[k]


def podsumowanie(plan):
    akt = [p for p in plan.get("pozycje") or [] if p.get("status") != "rezygnacja"]
    kat = {k: [p for p in akt if kategoria(p, plan) == k] for k in ("wylaczone", "ponizej_pzp", "krajowe", "unijne")}
    t = PR.tryb_wedlug_wartosci(0, "roboty", f"{plan['rok']}-01-01")
    return {"pozycji": len(akt), "suma": round(sum(p["wartosc"] for p in akt), 2),
            "w_planie_postepowan": len(kat["krajowe"]) + len(kat["unijne"]), "krajowe": len(kat["krajowe"]), "unijne": len(kat["unijne"]),
            "poza_planem": len(kat["ponizej_pzp"]) + len(kat["wylaczone"]), "prog_pzp": t["prog_pzp"], "kurs": t["kurs"],
            "progi_ue": {r: round(PR.PROGI_UE[r + ("_centralne" if plan.get("centralny") and r != "roboty" else "")] * PR.KURS_EURO) for r in RODZAJE}}


def pozycje_planu_postepowan(plan, pozycje=None):
    """Pozycje do BZP: tylko Pzp (krajowe i unijne), bez rezygnacji – w podziale na tabele i rodzaje, jak we wzorze."""
    pozycje = plan.get("pozycje") if pozycje is None else pozycje
    wyn = {"krajowe": {r: [] for r in RODZAJE}, "unijne": {r: [] for r in RODZAJE}}
    for p in pozycje:
        if p.get("status") == "rezygnacja":
            continue
        k = kategoria(p, plan)
        if k in wyn:
            wyn[k][p["rodzaj"]].append(p)
    return wyn


def zmiany_od_publikacji(plan):
    """Różnice między bieżącym planem a ostatnią opublikowaną wersją (tylko pozycje planu postępowań): dodanie, zmiana, rezygnacja."""
    if not plan.get("wersje"):
        return []
    stare = {p["id"]: p for p in plan["wersje"][-1]["pozycje"] if kategoria(p, plan) in ("krajowe", "unijne") and p.get("status") != "rezygnacja"}
    nowe = {p["id"]: p for p in plan["pozycje"] if kategoria(p, plan) in ("krajowe", "unijne") and p.get("status") != "rezygnacja"}
    zm = []
    for i, p in nowe.items():
        if i not in stare:
            zm.append({"id": i, "typ": "dodanie", "przedmiot": p["przedmiot"]})
        elif any(p.get(k) != stare[i].get(k) for k in POLA_ZMIANY):
            zm.append({"id": i, "typ": "zmiana", "przedmiot": p["przedmiot"],
                       "pola": [k for k in POLA_ZMIANY if p.get(k) != stare[i].get(k)]})
    for i, p in stare.items():
        if i not in nowe:
            zm.append({"id": i, "typ": "rezygnacja", "przedmiot": p["przedmiot"]})
    return zm


OSTRZEZENIE_PUSTY = ("Plan postępowań nie zawiera żadnej pozycji od progu stosowania ustawy Pzp (pozycje poniżej progu i wyłączone nie trafiają do planu "
                     "w BZP). Plan zapisano jako opublikowany – sprawdź, czy rzeczywiście publikujesz pusty plan (art. 23 Pzp dotyczy planowanych postępowań).")


def plan_postepowan_pusty(plan):
    """H3-06: czy plan postępowań (pozycje od progu Pzp, bez rezygnacji) jest pusty – ostrzeżenie przy publikacji, bez blokady."""
    return not any(kategoria(p, plan) in ("krajowe", "unijne") and p.get("status") != "rezygnacja" for p in plan.get("pozycje") or [])


def opublikuj(plan, numer_bzp="", data=None):
    """Zapis opublikowanej wersji (pierwotny plan albo aktualizacja) – kopia pozycji i lista zmian."""
    zm = zmiany_od_publikacji(plan) if plan.get("wersje") else []
    plan.setdefault("wersje", []).append({"nr": len(plan["wersje"]) + 1, "data": data or dt.date.today().isoformat(),
                                          "numer_bzp": numer_bzp or plan.get("numer_bzp") or "", "zmiany": zm,
                                          "pozycje": [dict(p) for p in plan["pozycje"]]})
    if numer_bzp:
        plan["numer_bzp"] = numer_bzp
    return plan["wersje"][-1]


# ---------------------------------------------------------------- import i propozycje
def import_excel(dane, plan):
    """Pozycje z arkusza: kolumny rozpoznawane po nagłówkach (przedmiot, rodzaj, CPV, wartość, termin/miesiąc/kwartał, tryb, komórka)."""
    import io
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(dane), data_only=True, read_only=True)
    ws = wb.worksheets[0]
    wiersze = [list(r) for r in ws.iter_rows(values_only=True)]
    if not wiersze:
        return []
    nag = [str(x or "").strip().lower() for x in wiersze[0]]
    def kol(*wz):
        return next((i for i, n in enumerate(nag) if any(w in n for w in wz)), None)
    k = {"przedmiot": kol("przedmiot", "nazwa"), "rodzaj": kol("rodzaj"), "cpv": kol("cpv"), "wartosc": kol("wartość", "wartosc", "kwota"),
         "termin": kol("termin", "miesiąc", "miesiac", "kwartał", "kwartal"), "tryb": kol("tryb"), "komorka": kol("komórka", "komorka", "wydział")}
    wyn = []
    for r in wiersze[1:]:
        g = lambda n: r[k[n]] if k[n] is not None and k[n] < len(r) else None
        if not g("przedmiot"):
            continue
        rz = str(g("rodzaj") or "").lower()
        rodz = "dostawy" if "dostaw" in rz else "uslugi" if "usług" in rz or "uslug" in rz else "roboty"
        tt, t = "miesiac", 1
        tr = str(g("termin") or "")
        m = re.search(r"(\d)\s*(?:kw|kwartał|kwartal|q)", tr, re.I) or re.search(r"^(?:q|kw\.?\s*)(\d)", tr, re.I)
        if m:
            tt, t = "kwartal", int(m.group(1))
        else:
            mm = next((i + 1 for i, n in enumerate(MIESIACE) if n[:3] in tr.lower()), None) or (int(_f(tr)) if _f(tr) else 1)
            t = mm
        tryb = str(g("tryb") or "")
        tryb = next((x for x in TRYBY_UE + TRYBY_KRAJ if tryb and tryb.lower()[:12] in x), "")
        wyn.append(oczysc_pozycje({"przedmiot": g("przedmiot"), "rodzaj": rodz, "cpv": g("cpv"), "wartosc": g("wartosc"), "termin_typ": tt,
                                   "termin": t, "tryb": tryb, "komorka": g("komorka")}, plan))
    return wyn


def wzor_importu(sciezka):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plan zamówień"
    ws.append(["Przedmiot zamówienia", "Rodzaj (roboty/dostawy/usługi)", "CPV", "Wartość netto [zł]", "Termin wszczęcia (np. marzec albo 2 kw.)",
               "Tryb (opcjonalnie)", "Komórka"])
    ws.append(["Przebudowa drogi gminnej nr 123", "roboty", "45233140-2", 1850000, "marzec", "tryb podstawowy – bez negocjacji", "Wydział Inwestycji"])
    ws.append(["Dostawa oleju opałowego", "dostawy", "09135100-5", 240000, "3 kw.", "", "Wydział Administracji"])
    for i, w in enumerate((48, 26, 14, 18, 30, 40, 22), 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    wb.save(sciezka)


SYSTEM_BUDZET = ("Jesteś specjalistą od zamówień publicznych w samorządzie. Z uchwały budżetowej, planu finansowego albo wieloletniej prognozy "
                 "finansowej wypisz zadania, które wymagają udzielenia zamówienia w danym roku (głównie wydatki majątkowe: inwestycje, zakupy "
                 "inwestycyjne; oraz istotne wydatki bieżące na usługi i dostawy, np. odbiór odpadów, dowóz uczniów, energia, utrzymanie dróg). "
                 "Odpowiedz WYŁĄCZNIE JSON: {\"pozycje\": [{\"przedmiot\": \"…\", \"rodzaj\": \"roboty|dostawy|uslugi\", \"wartosc\": liczba netto "
                 "w zł (kwotę z budżetu brutto podziel przez 1,23, jeśli to wydatek z VAT), \"cpv\": \"kod CPV jeśli pewny, inaczej pusty\", "
                 "\"zrodlo\": \"dział/rozdział/§ albo nr zadania z dokumentu\"}]}. Nie wymyślaj zadań spoza dokumentu.")


def pozycje_z_ai(dane, plan):
    wyn = []
    for x in (dane or {}).get("pozycje") or []:
        if isinstance(x, dict) and x.get("przedmiot"):
            p = oczysc_pozycje(dict(x, termin_typ="kwartal", termin=1), plan)
            p["zrodlo"] = ("propozycja AI z budżetu: " + str(x.get("zrodlo") or ""))[:200]
            wyn.append(p)
    return wyn


# ---------------------------------------------------------------- dokumenty
def _wiersze_planu(plan, pozycje=None):
    pp = pozycje_planu_postepowan(plan, pozycje)
    W = []
    for kat, naglowek in (("krajowe", "Zamówienia o wartości mniejszej niż progi unijne"), ("unijne", "Zamówienia o wartości równej lub przekraczającej progi unijne")):
        for rodz, L in pp[kat].items():
            for i, p in enumerate(L, 1):
                W.append({"tabela": naglowek, "rodzaj": RODZAJE[rodz], "lp": i, "id": p.get("id_bzp") or p["id"], "przedmiot": p["przedmiot"],
                          "tryb": p["tryb"], "wartosc": p["wartosc"], "termin": termin_opis(p), "info": info_opis(p)})
    return W


def plan_xlsx(sciezka, plan):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Plan postępowań {plan['rok']}"
    ws.append([f"Plan postępowań o udzielenie zamówień na rok {plan['rok']} – zestawienie do formularza w BZP (Platforma e-Zamówienia)"])
    ws.append([f"Rodzaj zamawiającego: {plan.get('rodzaj_zamawiajacego', '')}"])
    ws.append([])
    ws.append(["Tabela", "Rodzaj zamówienia", "Lp.", "Identyfikator", "Przedmiot zamówienia", "Przewidywany tryb albo procedura",
               "Orientacyjna wartość [zł netto]", "Przewidywany termin wszczęcia", "Informacje dodatkowe"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for w in _wiersze_planu(plan):
        ws.append([w["tabela"], w["rodzaj"], w["lp"], w["id"], w["przedmiot"], w["tryb"], w["wartosc"], w["termin"], w["info"]])
    zm = zmiany_od_publikacji(plan)
    if zm:
        ws2 = wb.create_sheet("Aktualizacja")
        ws2.append(["Identyfikator", "Rodzaj aktualizacji", "Przedmiot", "Zmienione pola"])
        for z in zm:
            ws2.append([z["id"], z["typ"], z["przedmiot"], ", ".join(z.get("pola") or [])])
    wp = wb.create_sheet("Plan wewnętrzny")
    wp.append(["Id", "Przedmiot", "Rodzaj", "CPV", "Wartość netto", "Kategoria", "Tryb", "Termin", "Komórka", "Źródło finansowania", "Status", "Uwagi"])
    for p in plan.get("pozycje") or []:
        wp.append([p["id"], p["przedmiot"], RODZAJE[p["rodzaj"]], p["cpv"], p["wartosc"], opis_kategorii(kategoria(p, plan)), p["tryb"],
                   termin_opis(p), p["komorka"], p["zrodlo"], p["status"], p.get("podstawa_wylaczenia") or ""])
    for arkusz in wb.worksheets:
        for kol in "ABCDEFGHIJKL":
            arkusz.column_dimensions[kol].width = 22
    ws.column_dimensions["E"].width = 60
    wb.save(sciezka)


def plan_docx(sciezka, plan, nazwa_zamawiajacego=""):
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    zm = zmiany_od_publikacji(plan)
    A(nazwa_zamawiajacego or "[nazwa zamawiającego]", rozmiar=9)
    A(f"PLAN POSTĘPOWAŃ O UDZIELENIE ZAMÓWIEŃ NA ROK {plan['rok']}" + (" – AKTUALIZACJA" if zm else ""), pogrub=True, rozmiar=13,
      wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"(art. 23 ustawy z dnia 11 września 2019 r. – Prawo zamówień publicznych){' · numer w BZP: ' + plan['numer_bzp'] if plan.get('numer_bzp') else ''}",
      rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    W = _wiersze_planu(plan)
    for tabela in ("Zamówienia o wartości mniejszej niż progi unijne", "Zamówienia o wartości równej lub przekraczającej progi unijne"):
        A(tabela, pogrub=True)
        for rodz in RODZAJE.values():
            L = [w for w in W if w["tabela"] == tabela and w["rodzaj"] == rodz]
            if not L:
                continue
            A(rodz, pogrub=True, rozmiar=10)
            MO._tabela(d, [["Lp.", "Identyfikator", "Przedmiot zamówienia", "Przewidywany tryb albo procedura", "Orientacyjna wartość (zł netto)",
                            "Przewidywany termin wszczęcia", "Informacje dodatkowe"]]
                       + [[str(w["lp"]), w["id"], w["przedmiot"], w["tryb"], f"{w['wartosc']:,.2f}".replace(",", " ").replace(".", ","),
                           w["termin"], w["info"]] for w in L])
    if zm:
        A("Informacja na temat aktualizacji", pogrub=True)
        MO._tabela(d, [["Identyfikator", "Rodzaj aktualizacji", "Przedmiot"]] + [[z["id"], z["typ"], z["przedmiot"]] for z in zm])
    A("Treść tożsama z planem zamieszczonym w Biuletynie Zamówień Publicznych (art. 23 ust. 1 Pzp).", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def nowe_id():
    return uuid.uuid4().hex[:8]
