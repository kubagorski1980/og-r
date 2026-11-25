# -*- coding: utf-8 -*-
"""
Ochrona ludności i obrona cywilna – pakiet dla gminy (Program Ochrony Ludności i Obrony Cywilnej na lata 2025–2026, uchwała nr 72
Rady Ministrów z 27.05.2025 r.; ustawa o ochronie ludności i obronie cywilnej, obowiązująca od 1.01.2025 r.).
Inwentaryzacja obiektów zbiorowej ochrony z pokryciem (budowle ochronne co najmniej 15%, wszystkie obiekty co najmniej 25% ludności),
zadania programu w 6 obszarach, kontrola wykorzystania dotacji (ryzyko zwrotu), raport w Wordzie. Program nie składa wniosków –
przygotowuje dane, zestawienia i zamówienia.
"""
import datetime as dt
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

OBSZARY = {
    "I": ("Obiekty zbiorowej ochrony", ["budowle ochronne (schrony, ukrycia)", "miejsca doraźnego schronienia", "ewidencja obiektów zbiorowej ochrony"], "roboty"),
    "II": ("Zabezpieczenie logistyczne i ciągłość dostaw", ["magazyny i zasoby ochrony ludności", "zasilanie awaryjne, woda, żywność"], "dostawy"),
    "III": ("Podmioty ochrony ludności", ["wyposażenie ratowników", "sprzęt ratowniczy, ewakuacyjny, logistyczny, CBRN"], "dostawy"),
    "IV": ("Edukacja i szkolenia", ["edukacja", "szkolenia", "kierowcy na potrzeby ochrony ludności", "publikacje i promocja"], "uslugi"),
    "V": ("Łączność oraz alarmowanie, ostrzeganie i powiadamianie", ["syreny i systemy alarmowania", "łączność"], "dostawy"),
    "VI": ("Korpus obrony cywilnej", ["oznakowanie podmiotów obrony cywilnej"], "dostawy"),
}
KATEGORIE = {"schron": "schron (budowla ochronna)", "ukrycie": "ukrycie (budowla ochronna)",
             "mds": "miejsce doraźnego schronienia", "punkt": "punkt schronienia (nie jest obiektem zbiorowej ochrony)"}
BUDOWLE = ("schron", "ukrycie")
OZO = ("schron", "ukrycie", "mds")  # obiekty zbiorowej ochrony (art. 83–84 ustawy); punkty schronienia (art. 84a) liczone osobno
# Art. 90 ust. 2 ustawy o ochronie ludności i obronie cywilnej: % przewidywanej liczby ludności przebywającej w sytuacji zagrożenia
NORMY = {"miasto": {"nazwa": "w granicach administracyjnych miast", "wszystkie": 50, "budowle": 25},
         "poza": {"nazwa": "poza granicami administracyjnymi miast", "wszystkie": 25, "budowle": 15}}
NORMA_BUDOWLE, NORMA_WSZYSTKIE = NORMY["poza"]["budowle"], NORMY["poza"]["wszystkie"]  # zgodność wsteczna
TYPY_GMIN = {"miejska": "gmina miejska", "wiejska": "gmina wiejska", "miejsko-wiejska": "gmina miejsko-wiejska"}
STAN_POTWIERDZONY = "sprawny"  # do pokrycia potwierdzonego wliczane tylko obiekty sprawne


def _f(v):
    return liczba(v, 0.0)


def _obszary_gminy(gmina):
    """[(kod, ludność)] – gmina miejska: tylko miasto; wiejska: tylko poza miastem; miejsko-wiejska: oba obszary osobno."""
    g = gmina or {}
    typ = g.get("typ") or ""
    if typ == "miejska":
        return [("miasto", _f(g.get("mieszkancy")))]
    if typ == "miejsko-wiejska":
        return [("miasto", _f(g.get("mieszkancy_miasto"))), ("poza", _f(g.get("mieszkancy_poza")))]
    return [("poza", _f(g.get("mieszkancy")))]


def pokrycie(gmina, obiekty):
    """Pokrycie według art. 90 ust. 2: osobno dla obszaru miejskiego i pozamiejskiego; potwierdzone (obiekty sprawne)
    i deklarowane (sprawne, wymagające prac i do sprawdzenia); punkty schronienia poza pokryciem."""
    g, obiekty = gmina or {}, [o for o in (obiekty or []) if isinstance(o, dict)]
    typ = g.get("typ") or ""
    domyslny = "miasto" if typ == "miejska" else "poza"
    obs = []
    for kod, lud in _obszary_gminy(g):
        n = NORMY[kod]
        ozo = [o for o in obiekty if o.get("kategoria") in OZO and o.get("stan") != "nie spełnia wymagań"
               and (typ != "miejsko-wiejska" or (o.get("obszar") or "miasto") == kod)]
        potw = [o for o in ozo if o.get("stan") == STAN_POTWIERDZONY]
        suma = lambda lst, bud=False: sum(_f(o.get("pojemnosc")) for o in lst if not bud or o.get("kategoria") in BUDOWLE)
        wym_w, wym_b = (round(lud * n["wszystkie"] / 100), round(lud * n["budowle"] / 100)) if lud else (None, None)
        pw, pb, dw, db = suma(potw), suma(potw, True), suma(ozo), suma(ozo, True)
        pr = lambda x: round(x / lud * 100, 1) if lud else None
        obs.append({"kod": kod, "nazwa": n["nazwa"], "ludnosc": lud, "norma_wszystkie": n["wszystkie"], "norma_budowle": n["budowle"],
                    "wymagane_wszystkie": wym_w, "wymagane_budowle": wym_b, "wszystkie_miejsc": pw, "budowle_miejsc": pb,
                    "wszystkie_deklarowane": dw, "budowle_deklarowane": db, "wszystkie_proc": pr(pw), "budowle_proc": pr(pb),
                    "wszystkie_proc_dekl": pr(dw), "budowle_proc_dekl": pr(db),
                    "brak_wszystkie": max(0, wym_w - round(pw)) if lud else None, "brak_budowle": max(0, wym_b - round(pb)) if lud else None})
    lud = sum(o["ludnosc"] for o in obs)
    punkty = [o for o in obiekty if o.get("kategoria") == "punkt"]
    ostrz = []
    if not typ:
        ostrz.append("Wybierz typ gminy – w granicach miast norma wynosi 50% (w tym 25% w budowlach ochronnych), poza miastami 25% (w tym 15%). "
                     "Do czasu wyboru program liczy normę dla obszaru poza miastami.")
    if typ == "miejsko-wiejska" and not (_f(g.get("mieszkancy_miasto")) and _f(g.get("mieszkancy_poza"))):
        ostrz.append("Gmina miejsko-wiejska: podaj osobno liczbę ludności w mieście i poza miastem – normy są różne.")
    if typ == "miejsko-wiejska" and any(o.get("kategoria") in OZO and not o.get("obszar") for o in obiekty):
        ostrz.append("Część obiektów nie ma wskazanego obszaru (miasto / poza miastem) – liczone jako w mieście.")
    nzw = sum(1 for o in obiekty if o.get("kategoria") in OZO and o.get("stan") in ("", None, "do sprawdzenia", "wymaga prac"))
    if nzw:
        ostrz.append(f"{nzw} obiektów jest do sprawdzenia albo wymaga prac – nie są wliczane do pokrycia potwierdzonego.")
    return {"typ": typ, "domyslny_obszar": domyslny, "obszary": obs, "mieszkancy": lud,
            # podsumowanie całej gminy (pokrycie potwierdzone) – także dla raportu i zgodności wstecznej
            "budowle_miejsc": sum(o["budowle_miejsc"] for o in obs), "wszystkie_miejsc": sum(o["wszystkie_miejsc"] for o in obs),
            "budowle_proc": round(sum(o["budowle_miejsc"] for o in obs) / lud * 100, 1) if lud else None,
            "wszystkie_proc": round(sum(o["wszystkie_miejsc"] for o in obs) / lud * 100, 1) if lud else None,
            "brak_budowle": sum(o["brak_budowle"] or 0 for o in obs) if lud else None,
            "brak_wszystkie": sum(o["brak_wszystkie"] or 0 for o in obs) if lud else None,
            "punkty_liczba": len(punkty), "punkty_miejsc": sum(_f(o.get("pojemnosc")) for o in punkty),
            "do_sprawdzenia": sum(1 for o in obiekty if o.get("stan") in ("", None, "do sprawdzenia")),
            "wymaga_prac": sum(1 for o in obiekty if o.get("stan") == "wymaga prac"),
            "koszt_prac": round(sum(_f(o.get("koszt")) for o in obiekty), 2), "ostrzezenia": ostrz}


def _zl(v):
    return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " zł"


def kontrola(zadania, dzis=None):
    """Alerty do zadań: termin, niewykorzystana dotacja (ryzyko zwrotu), wydatki po terminie, przekroczenie, brak zamówienia."""
    dzis = dzis or dt.date.today()
    wyn = []
    for z in zadania or []:
        if not isinstance(z, dict):
            continue
        wydatki = [w for w in z.get("wydatki") or [] if isinstance(w, dict)] if isinstance(z.get("wydatki"), list) else []
        dot, wyd = _f(z.get("dotacja")), sum(_f(w.get("kwota")) for w in wydatki)
        a = []
        try:
            term = dt.date.fromisoformat(str(z.get("termin"))[:10])
        except ValueError:
            term = None
        wyd_kw, wyd_nkw = wyd, 0.0  # wydatki kwalifikowalne (do terminu) – podstawa wykorzystania dotacji i kwoty do zwrotu
        if term:
            for w in wydatki:
                try:
                    if dt.date.fromisoformat(str(w.get("data"))[:10]) > term:
                        wyd_nkw += _f(w.get("kwota"))
                except ValueError:
                    pass
            wyd_kw = wyd - wyd_nkw
            dni = (term - dzis).days
            if dni < 0 and dot and wyd_kw < dot and z.get("status") != "rozliczone":
                a.append(("czerwony", f"termin minął {abs(dni)} dni temu – niewykorzystane {_zl(dot - wyd_kw)} do zwrotu"
                          + (f" (wydatki po terminie {_zl(wyd_nkw)} są niekwalifikowalne i nie pomniejszają zwrotu)" if wyd_nkw else "")))
            elif 0 <= dni <= 30 and dot and wyd_kw < dot:
                a.append(("zolty", f"do terminu {dni} dni – wykorzystano {round(wyd_kw / dot * 100) if dot else 0}% dotacji"))
            for w in wydatki:
                try:
                    if dt.date.fromisoformat(str(w.get("data"))[:10]) > term:
                        a.append(("czerwony", f"wydatek {w.get('dokument') or ''} z {w.get('data')} po terminie – niekwalifikowalny"))
                except ValueError:
                    a.append(("zolty", f"wydatek {w.get('dokument') or ''} bez daty"))
        else:
            a.append(("zolty", "brak terminu wykorzystania dotacji"))
        if dot and wyd > dot:
            a.append(("zolty", f"wydatki przekraczają dotację o {_zl(wyd - dot)} – różnica ze środków własnych"))
        if z.get("status") in ("przyznane", "w realizacji") and not z.get("projekt_id"):
            a.append(("zolty", "brak zamówienia – utwórz postępowanie albo zapytanie ofertowe"))
        if z.get("obszar") not in OBSZARY:
            a.append(("czerwony", "zadanie poza obszarami programu – wydatek może zostać uznany za niezgodny"))
        wyn.append({"id": z.get("id"), "wydatki": round(wyd, 2), "wydatki_niekwalifikowalne": round(wyd_nkw, 2),
                    "wykorzystanie": round(wyd_kw / dot * 100, 1) if dot else None, "alerty": a})
    return wyn


def raport_docx(sciezka, d):
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = MO._doc()
    A = lambda t, **k: MO._akapit(doc, t, **k)
    zl = lambda v: f"{_f(v):,.2f} zł".replace(",", " ").replace(".", ",")
    g = d.get("gmina") or {}
    A("OCHRONA LUDNOŚCI I OBRONA CYWILNA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{g.get('nazwa') or 'Gmina'} – zestawienie na dzień {dt.date.today():%d.%m.%Y}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    p = pokrycie(g, d.get("obiekty"))
    A("1. Obiekty zbiorowej ochrony – pokrycie", pogrub=True)
    A(f"Normy z art. 90 ust. 2 ustawy o ochronie ludności i obronie cywilnej; {TYPY_GMIN.get(p['typ'], 'typ gminy nieustalony')}. "
      "Pokrycie potwierdzone obejmuje wyłącznie obiekty sprawne; deklarowane – także obiekty do sprawdzenia i wymagające prac.")
    if p["mieszkancy"]:
        for o in p["obszary"]:
            if not o["ludnosc"]:
                continue
            A(f"{o['nazwa'].capitalize()}: przewidywana liczba ludności {int(o['ludnosc'])}. Wszystkie obiekty zbiorowej ochrony: "
              f"{int(o['wszystkie_miejsc'])} miejsc potwierdzonych ({o['wszystkie_proc']}%; deklarowane {o['wszystkie_proc_dekl']}%), norma co najmniej "
              f"{o['norma_wszystkie']}% = {o['wymagane_wszystkie']} miejsc, brakuje {o['brak_wszystkie']}. W tym budowle ochronne: "
              f"{int(o['budowle_miejsc'])} miejsc ({o['budowle_proc']}%; deklarowane {o['budowle_proc_dekl']}%), norma co najmniej "
              f"{o['norma_budowle']}% = {o['wymagane_budowle']} miejsc, brakuje {o['brak_budowle']}.")
        if p["punkty_liczba"]:
            A(f"Punkty schronienia (art. 84a – nie są obiektami zbiorowej ochrony, nie wliczają się do pokrycia): {p['punkty_liczba']}, "
              f"{int(p['punkty_miejsc'])} miejsc.")
        for t in p["ostrzezenia"]:
            A(f"Uwaga: {t}", rozmiar=9)
    else:
        A("Uzupełnij typ gminy i przewidywaną liczbę ludności, żeby policzyć pokrycie.")
    for o in d.get("obiekty") or []:
        A(f"• {o.get('nazwa') or ''}, {o.get('adres') or ''} – {KATEGORIE.get(o.get('kategoria'), o.get('kategoria') or '')}, {int(_f(o.get('pojemnosc')))} miejsc, "
          f"stan: {o.get('stan') or 'do sprawdzenia'}" + (f"; prace: {o.get('prace')}" if o.get("prace") else "") + (f"; koszt szacunkowy {zl(o.get('koszt'))}" if _f(o.get("koszt")) else ""))
    A("2. Zadania w ramach Programu Ochrony Ludności i Obrony Cywilnej", pogrub=True)
    K = {k["id"]: k for k in kontrola(d.get("zadania"))}
    for z in d.get("zadania") or []:
        k = K.get(z.get("id"), {})
        A(f"• Obszar {z.get('obszar')} ({OBSZARY.get(z.get('obszar'), ('',))[0]}) – {z.get('nazwa') or ''}: dotacja {zl(z.get('dotacja'))}, wkład własny {zl(z.get('wklad'))}, "
          f"termin {z.get('termin') or '–'}, status: {z.get('status') or 'planowane'}, wydatki {zl(k.get('wydatki'))}"
          + (f", w tym niekwalifikowalne (po terminie) {zl(k.get('wydatki_niekwalifikowalne'))}" if k.get("wydatki_niekwalifikowalne") else "")
          + (f" (wykorzystanie dotacji {k.get('wykorzystanie')}%)" if k.get("wykorzystanie") is not None else ""))
        for poziom, t in k.get("alerty") or []:
            A(f"   – {'UWAGA' if poziom == 'czerwony' else 'do sprawdzenia'}: {t}", rozmiar=9)
    A("Zestawienie pomocnicze. Środki wydane niezgodnie z programem albo po terminie podlegają zwrotowi do budżetu państwa – przed rozliczeniem "
      "sprawdź warunki umowy dotacji i wytyczne wojewody.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(doc, sciezka)
