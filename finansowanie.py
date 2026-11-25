# -*- coding: utf-8 -*-
"""
Finansowanie inwestycji zamawiającego (bank, BGK, instytucja pośrednicząca – np. KPO): wymagania z umowy finansowania i ich porównanie
z umową, harmonogramem i ofertą wykonawcy – terminy, okres kwalifikowalności, kwoty, transze, przepływy pieniężne, klauzule.
Wynik to propozycje do sprawdzenia przez zamawiającego, nie wykładnia umowy finansowania.
"""
import datetime as dt
import re

import weryfikacja as WER
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

TYPY = {"kredyt": "kredyt bankowy", "premia": "premia BGK (termomodernizacyjna / remontowa)", "dotacja": "dotacja / dofinansowanie (np. KPO, program regionalny)",
        "promesa": "Rządowy Fundusz / Polski Ład / RFIL / RFRD – promesa BGK", "pozyczka": "pożyczka", "inne": "inne finansowanie"}
# H3-04: promesa BGK (programy rządowe dla samorządów) – środki wypłacane po odbiorze robót (jednorazowo po zakończeniu inwestycji albo w transzach
# według promesy), zwykle bezpośrednio wykonawcy; wcześniej zamawiający pokrywa wkład własny. Kredyt / pożyczka JST – art. 243 ufp i WPF.
TYPY_DLUZNE = ("kredyt", "pozyczka")
INFO_PROMESA = ("Promesa BGK: wypłata następuje po odbiorze robót – jednorazowo po zakończeniu inwestycji albo w transzach, jeśli przewiduje to promesa – "
                "zwykle bezpośrednio na rachunek wykonawcy, po zapłacie przez zamawiającego części wynagrodzenia z wkładu własnego. "
                "Do tego czasu zamawiający finansuje płatności z własnych środków (prefinansowanie). Sprawdź warunki w promesie i regulaminie programu.")
INFO_243 = ("Kredyt / pożyczka jednostki samorządu terytorialnego: przed zaciągnięciem sprawdź w wieloletniej prognozie finansowej (WPF) indywidualny "
            "wskaźnik zadłużenia – relację z art. 243 ustawy o finansach publicznych (spłaty rat, odsetek i potencjalnych spłat poręczeń do dochodów) "
            "na każdy rok spłaty, oraz ujęcie przedsięwzięcia i limitu zobowiązań w WPF (art. 226 i 230 ufp) i uchwałę organu stanowiącego. "
            "Program tego nie liczy.")
STATUSY = {"zgodne": "zgodne", "rozbiezne": "rozbieżne", "brak": "brak w umowie z wykonawcą", "do_sprawdzenia": "do sprawdzenia"}
ZAPAS_DNI = 30  # minimalny zapas między końcem robót wykonawcy a terminem z umowy finansowania (odbiór, dokumenty, rozliczenie)
DNI_PLATNOSCI = 30  # domyślny termin zapłaty faktury wykonawcy

SYSTEM = ("Jesteś specjalistą od finansowania inwestycji budowlanych (kredyty bankowe, premie BGK, dotacje UE i KPO) i umów o roboty budowlane. "
          "Czytasz umowę finansowania z załącznikami i wypisujesz to, co zamawiający musi zapewnić w umowie z wykonawcą i w harmonogramie. "
          "Nie zgadujesz – brak danych = puste pole. Przy każdej pozycji dosłowny cytat z dokumentu. Odpowiadasz wyłącznie JSON.")


def polecenie_wymagan(typ):
    return (f"Rodzaj finansowania: {TYPY.get(typ, typ)}. Wypisz z umowy finansowania i załączników (harmonogram, wniosek, audyt) JSON:\n"
            '{"instytucja": "", "numer_umowy": "", "data_umowy": "RRRR-MM-DD", "kwota": liczba, "wklad_wlasny": liczba albo null, '
            '"termin_zakonczenia_realizacji": "RRRR-MM-DD", "termin_rozliczenia": "RRRR-MM-DD albo opis", '
            '"okres_kwalifikowalnosci_od": "RRRR-MM-DD", "okres_kwalifikowalnosci_do": "RRRR-MM-DD", '
            '"transze": [{"nr": 1, "kwota": liczba, "termin": "RRRR-MM-DD albo pusty", "warunek": "np. po odbiorze etapu I i zatwierdzeniu przez inspektora banku", "cytat": ""}], '
            '"koszty_kwalifikowalne": [""], "koszty_niekwalifikowalne": [""], '
            '"wymagania_umowy_wykonawczej": [{"wymog": "co musi zawierać umowa z wykonawcą albo jak ma być prowadzona realizacja (gwarancja, kary umowne, '
            'zabezpieczenie, ubezpieczenie, zgoda instytucji na zmiany umowy, prawo kontroli, sposób wyboru wykonawcy, oznakowanie, odbiory, faktury)", '
            '"cytat": "dosłowny fragment", "miejsce": "§ / pkt"}], '
            '"dokumenty_rozliczenia": [{"dokument": "", "kiedy": "np. z wnioskiem o wypłatę transzy"}], '
            '"wskazniki": [{"nazwa": "", "wartosc": ""}], "obowiazki_informacyjne": [""], '
            '"sankcje": ["np. zwrot dotacji, utrata premii, wypowiedzenie kredytu – z warunkiem"]}\n'
            "Daty w formacie RRRR-MM-DD, kwoty w złotych jako liczby. Cytaty dosłowne (20–300 znaków).")


def polecenie_porownania(wymagania):
    lista = "\n".join(f"{i}. {w.get('wymog')}" for i, w in enumerate(wymagania))
    return ("Porównaj umowę z wykonawcą (dokumenty oznaczone jako UMOWA WYKONAWCZA) z wymaganiami umowy finansowania poniżej. Dla każdego wymagania "
            "ustal, czy umowa z wykonawcą je spełnia. JSON: [{\"nr\": 0, \"status\": \"zgodne|rozbiezne|brak|do_sprawdzenia\", "
            "\"cytat_umowy\": \"dosłowny fragment umowy z wykonawcą albo pusty\", \"komentarz\": \"krótko\", "
            "\"propozycja_aneksu\": \"treść postanowienia do aneksu – tylko przy rozbieżności albo braku\"}]\n\nWYMAGANIA:\n" + lista)


def _d(v):
    if isinstance(v, dt.date):
        return v
    t = str(v or "").strip()
    try:
        return dt.date.fromisoformat(t[:10])
    except ValueError:
        return WER._data(t)


def data_scisla(v):
    """Istniejąca data z RRRR-MM-DD albo DD.MM.RRRR (także z / i -); inaczej None – do kontroli danych wpisanych ręcznie (GC-06)."""
    t = str(v or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t[:10]) if re.match(r"\d{4}-", t) else re.fullmatch(r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})(?:\s*r\.?)?", t)
    if not m:
        return None
    a, b, c = (int(x) for x in m.groups())
    r, mi, d = (a, b, c) if a > 31 else (c, b, a)
    try:
        return dt.date(r, mi, d)
    except ValueError:
        return None


def _kw(v):
    return liczba(re.sub(r"[^\d,.\-]", "", str(v)) if v is not None else None, 0.0)  # „60 miesięcy” → 60


def _zl(v):
    return f"{v:,.2f}".replace(",", "\u00a0").replace(".", ",").replace("\u00a0", " ") + " zł"


def termin_wykonawcy(r):
    """Koniec robót według umowy z wykonawcą albo ostatniego etapu harmonogramu."""
    etapy = ((r.get("hrf") or {}).get("etapy") or [])
    kandydaci = [_d(r.get("termin_zakonczenia"))] + [_d(e.get("do")) for e in etapy]
    kandydaci = [x for x in kandydaci if x]
    return max(kandydaci) if kandydaci else None


def wklad_inwestycji(F, zrodla=None):
    """H3-04: jeden wkład własny na całą inwestycję. Stare dane (wkład przy każdym źródle) – suma z ostrzeżeniem do sprawdzenia
    (dotąd ten sam wkład wpisany przy dwóch umowach liczył się dwa razy). Zwraca (kwota, ostrzeżenie migracji albo "")."""
    F = F if isinstance(F, dict) else {}
    if "wklad_wlasny" in F:
        return _kw(F.get("wklad_wlasny")), str(F.get("wklad_wlasny_migracja") or "")
    zr = [z for z in (zrodla if zrodla is not None else F.get("zrodla") or []) if _kw((z.get("wymagania") or {}).get("wklad_wlasny"))]
    if not zr:
        return 0.0, ""
    suma = round(sum(_kw(z["wymagania"]["wklad_wlasny"]) for z in zr), 2)
    ostrz = (f"Wkład własny przeniesiono ze źródeł finansowania do jednego pola inwestycji: suma {_zl(suma)} z {len(zr)} "
             + ("źródła" if len(zr) == 1 else "źródeł") + " (" + "; ".join(f"{z.get('instytucja') or TYPY.get(z.get('typ'), 'źródło')}: {_zl(_kw(z['wymagania']['wklad_wlasny']))}" for z in zr)
             + "). Sprawdź i zatwierdź kwotę" + (" – jeśli kilka umów podaje ten sam wkład, liczył się on wcześniej wielokrotnie." if len(zr) > 1 else "."))
    return suma, ostrz


def migruj_wklad(F):
    """Migracja przy zapisie: pole wkładu własnego inwestycji z sumy starych wkładów przy źródłach (z ostrzeżeniem do zatwierdzenia)."""
    if isinstance(F, dict) and "wklad_wlasny" not in F:
        kw, ostrz = wklad_inwestycji(F)
        F["wklad_wlasny"] = kw
        if ostrz:
            F["wklad_wlasny_migracja"] = ostrz
    return F


def porownaj_rachunkowo(zrodla, r, dzis=None, wklad=None, jst=False):
    """Kontrole bez AI: terminy, okres kwalifikowalności, kwoty, transze. Zwraca [{"kolor", "obszar", "opis"}].
    wklad – wkład własny inwestycji (jeden na projekt, H3-04); None – z danych finansowania w realizacji (albo suma starych wkładów przy źródłach).
    jst – zamawiający publiczny (gmina, powiat, województwo): przy kredycie i pożyczce ostrzeżenie z art. 243 ufp i WPF."""
    wyn = []
    dodaj = lambda k, o, t: wyn.append({"kolor": k, "obszar": o, "opis": t})
    if wklad is None:
        wklad, ostrz_m = wklad_inwestycji(r.get("finansowanie") if isinstance(r.get("finansowanie"), dict) else {"zrodla": zrodla}, zrodla)
        if ostrz_m:
            dodaj("zolty", "Wkład własny", ostrz_m)
    koniec = termin_wykonawcy(r)
    d_umowy = _d(r.get("data_umowy"))
    vat = _kw(r.get("vat")) if r.get("vat") not in (None, "") else 0.23
    brutto = _kw(r.get("wartosc_netto")) * (1 + (vat if vat < 1 else vat / 100))
    suma_fin = 0.0
    for z in zrodla:
        W = z.get("wymagania") or {}
        inst = z.get("instytucja") or W.get("instytucja") or ""
        naz = inst or TYPY.get(z.get("typ"), "finansowanie").capitalize()
        z_kim = f"z {inst}" if inst else "z instytucją finansującą"
        tz = _d(W.get("termin_zakonczenia_realizacji"))
        if tz and koniec:
            zapas = (tz - koniec).days
            if zapas < 0:
                dodaj("czerwony", "Terminy", f"{naz}: roboty kończą się {koniec:%d.%m.%Y}, a termin zakończenia realizacji z umowy finansowania to {tz:%d.%m.%Y} "
                                             f"({-zapas} dni po terminie) – ryzyko utraty finansowania; skróć termin wykonawcy albo uzgodnij zmianę {z_kim}.")
            elif zapas < ZAPAS_DNI:
                dodaj("zolty", "Terminy", f"{naz}: tylko {zapas} dni między końcem robót ({koniec:%d.%m.%Y}) a terminem z umowy finansowania ({tz:%d.%m.%Y}) – "
                                          "za mało na odbiór końcowy i komplet dokumentów do rozliczenia.")
            else:
                dodaj("zielony", "Terminy", f"{naz}: koniec robót {koniec:%d.%m.%Y}, termin finansowania {tz:%d.%m.%Y} – zapas {zapas} dni.")
        elif not tz:
            dodaj("zolty", "Terminy", f"{naz}: nie odczytano terminu zakończenia realizacji – uzupełnij ręcznie.")
        od, do = _d(W.get("okres_kwalifikowalnosci_od")), _d(W.get("okres_kwalifikowalnosci_do"))
        if od and d_umowy and d_umowy < od and z.get("typ") in ("dotacja", "premia"):
            dodaj("czerwony", "Kwalifikowalność", f"{naz}: umowa z wykonawcą zawarta {d_umowy:%d.%m.%Y}, przed początkiem okresu kwalifikowalności ({od:%d.%m.%Y}) – "
                                                  "sprawdź, czy wydatki z tej umowy mogą być kwalifikowalne.")
        if do:
            po = [e for e in ((r.get("hrf") or {}).get("etapy") or []) if _d(e.get("do")) and _d(e.get("do")) > do]
            if po:
                dodaj("czerwony", "Kwalifikowalność", f"{naz}: {len(po)} etapów harmonogramu kończy się po okresie kwalifikowalności ({do:%d.%m.%Y}) – "
                                                      f"wydatki z nich mogą nie zostać sfinansowane: " + ", ".join(e.get("nazwa") or str(e.get("nr")) for e in po[:4]) + ".")
        suma_fin += _kw(W.get("kwota"))  # wkład własny – raz dla całej inwestycji (niżej), nie przy każdym źródle
        transze = [t for t in (W.get("transze") or []) if isinstance(t, dict)]
        etapy = (r.get("hrf") or {}).get("etapy") or []
        if transze and etapy and len(transze) > len(etapy):
            dodaj("zolty", "Transze", f"{naz}: {len(transze)} transz, a harmonogram wykonawcy ma {len(etapy)} etapów – wypłata transz zwykle wymaga odbiorów etapów; "
                                      "dostosuj podział harmonogramu.")
        for t in transze:
            tt = _d(t.get("termin"))
            if tt and etapy and not any(_d(e.get("do")) and _d(e.get("do")) <= tt for e in etapy):
                dodaj("zolty", "Transze", f"{naz}: transza {t.get('nr')} ({tt:%d.%m.%Y}) – żaden etap nie kończy się przed tym terminem, więc warunek wypłaty "
                                          f"({t.get('warunek') or 'odbiór robót'}) może nie zostać spełniony.")
    typy_ = {z.get("typ") for z in zrodla}
    if "promesa" in typy_:
        dodaj("zolty", "Promesa BGK", INFO_PROMESA + ("" if wklad else " Promesa wymaga wkładu własnego – wpisz wkład własny inwestycji."))
    if jst and typy_ & set(TYPY_DLUZNE):
        dodaj("zolty", "Art. 243 ufp i WPF", INFO_243)
    suma_fin = round(suma_fin + (wklad or 0), 2)
    if brutto and suma_fin and brutto > suma_fin + 1:
        dodaj("zolty", "Kwoty", f"Wartość umowy z wykonawcą ({_zl(brutto)} brutto) przekracza łączne finansowanie z wkładem własnym ({_zl(suma_fin)}) "
                                f"o {_zl(brutto - suma_fin)} – zapewnij dodatkowe środki.")
    return wyn


def przeplywy(zrodla, r):
    """Plan miesięczny: płatności dla wykonawcy (wartość etapu brutto, 30 dni po końcu etapu) i wpływy z transz; saldo narastająco.
    Promesa BGK bez transz z terminami (H3-04): cała kwota wpływa w miesiącu zapłaty za ostatni etap (wypłata po odbiorze końcowym) –
    dotąd promesa bez transz nie dawała żadnego wpływu, a transze z umowną datą nie uwzględniały, że BGK płaci dopiero po odbiorze."""
    vat = _kw(r.get("vat")) if r.get("vat") not in (None, "") else 0.23
    mn = 1 + (vat if vat < 1 else vat / 100)
    mies = {}
    ost = None
    for e in (r.get("hrf") or {}).get("etapy") or []:
        d = _d(e.get("do"))
        if d and _kw(e.get("wartosc")):
            k = (d + dt.timedelta(days=DNI_PLATNOSCI)).strftime("%Y-%m")
            mies.setdefault(k, [0.0, 0.0])[0] += round(_kw(e["wartosc"]) * mn, 2)
            ost = max(ost or k, k)
    for z in zrodla:
        tr = [t for t in ((z.get("wymagania") or {}).get("transze") or []) if isinstance(t, dict) and _d(t.get("termin")) and _kw(t.get("kwota"))]
        if z.get("typ") == "promesa" and not tr and _kw((z.get("wymagania") or {}).get("kwota")):
            tw = termin_wykonawcy(r)
            k = ost or ((tw + dt.timedelta(days=DNI_PLATNOSCI)).strftime("%Y-%m") if tw else None)
            if k:
                mies.setdefault(k, [0.0, 0.0])[1] += _kw(z["wymagania"]["kwota"])
            continue
        for t in tr:  # transze (także promesy – w terminach według promesy)
            mies.setdefault(_d(t["termin"]).strftime("%Y-%m"), [0.0, 0.0])[1] += _kw(t["kwota"])
    wyn, saldo, max_luka = [], 0.0, 0.0
    for k in sorted(mies):
        wyp, wpl = mies[k]
        saldo = round(saldo + wpl - wyp, 2)
        max_luka = min(max_luka, saldo)
        wyn.append({"miesiac": k, "platnosci": wyp, "wplywy": wpl, "saldo": saldo})
    return {"miesiace": wyn, "najwieksza_luka": round(-max_luka, 2)}


def raport_docx(sciezka, nazwa, zrodla, r, kontrole, przepl, porownanie):
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("FINANSOWANIE INWESTYCJI – ZGODNOŚĆ Z UMOWĄ WYKONAWCZĄ", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{nazwa} – stan na {dt.date.today():%d.%m.%Y}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A("1. Źródła finansowania", pogrub=True)
    MO._tabela(d, [["Źródło", "Instytucja", "Kwota", "Termin zakończenia realizacji", "Okres kwalifikowalności"]] +
               [[TYPY.get(z.get("typ"), ""), z.get("instytucja") or (z.get("wymagania") or {}).get("instytucja") or "", MO.zl(_kw((z.get("wymagania") or {}).get("kwota"))),
                 str((z.get("wymagania") or {}).get("termin_zakonczenia_realizacji") or "–"),
                 " – ".join(str((z.get("wymagania") or {}).get(k) or "") for k in ("okres_kwalifikowalnosci_od", "okres_kwalifikowalnosci_do")).strip(" –") or "–"]
                for z in zrodla])
    wk, _ = wklad_inwestycji(r.get("finansowanie") if isinstance(r.get("finansowanie"), dict) else {"zrodla": zrodla}, zrodla)
    A(f"Wkład własny inwestycji (jeden dla wszystkich źródeł): {MO.zl(wk) if wk else '[UZUPEŁNIJ]'}.")
    A("2. Kontrola terminów, kwot i transz", pogrub=True)
    for k in kontrole:
        A(f"{'UWAGA' if k['kolor'] == 'czerwony' else 'Do sprawdzenia' if k['kolor'] == 'zolty' else 'Zgodne'} – {k['obszar']}: {k['opis']}")
    A("3. Przepływy pieniężne (płatności dla wykonawcy a wpływy z finansowania)", pogrub=True)
    if przepl["miesiace"]:
        MO._tabela(d, [["Miesiąc", "Płatności dla wykonawcy", "Wpływy z finansowania", "Saldo narastająco"]] +
                   [[m["miesiac"], MO.zl(m["platnosci"]), MO.zl(m["wplywy"]), MO.zl(m["saldo"])] for m in przepl["miesiace"]])
        A(f"Największe zapotrzebowanie na środki własne (prefinansowanie): {MO.zl(przepl['najwieksza_luka'])}.", pogrub=True)
    else:
        A("Brak danych – uzupełnij harmonogram wykonawcy (etapy z wartościami) i terminy transz.")
    A("4. Wymagania umowy finansowania a umowa z wykonawcą", pogrub=True)
    for p in porownanie:
        A(f"{STATUSY.get(p.get('status'), p.get('status'))}: {p.get('wymog')}" + (f" – {p['komentarz']}" if p.get("komentarz") else ""), pogrub=p.get("status") in ("rozbiezne", "brak"))
        if p.get("propozycja_aneksu"):
            A(f"Propozycja postanowienia do aneksu: {p['propozycja_aneksu']}", kursywa=True)
    A("Zestawienie pomocnicze przygotowane z użyciem AI – wymaga sprawdzenia z treścią umów; zmiany umowy z wykonawcą i umowy finansowania "
      "uzgadnia się ze stronami i z instytucją finansującą.", kursywa=True, rozmiar=9)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# ---------------------------------------------------------------- kreator zamówienia: wymagania finansowania w dokumentach i harmonogramie
def koniec_robot_najpozniej(zrodla):
    """Najpóźniejszy koniec robót wykonawcy: najwcześniejszy termin zakończenia realizacji / kwalifikowalności minus zapas na odbiór i rozliczenie."""
    t = [_d((z.get("wymagania") or {}).get(k)) for z in zrodla for k in ("termin_zakonczenia_realizacji", "okres_kwalifikowalnosci_do")]
    t = [x for x in t if x]
    return (min(t) - dt.timedelta(days=ZAPAS_DNI)) if t else None


def tekst_do_dokumentow(zrodla):
    """Wymagania umów finansowania (kredyt, premia BGK, KPO, dotacja) do przygotowania zapytania / SWZ, wzoru umowy i harmonogramu.
    Pusty tekst, gdy zamówienie nie ma źródeł finansowania."""
    if not zrodla:
        return ""
    cz = []
    for z in zrodla:
        W = z.get("wymagania") or {}
        naz = TYPY.get(z.get("typ"), "finansowanie") + (f" – {z.get('instytucja') or W.get('instytucja')}" if (z.get("instytucja") or W.get("instytucja")) else "")
        o = [naz + (f", umowa {W['numer_umowy']}" if W.get("numer_umowy") else "") + (f", kwota {_zl(_kw(W['kwota']))}" if _kw(W.get("kwota")) else "")]
        tz = _d(W.get("termin_zakonczenia_realizacji"))
        if tz:
            o.append(f"termin zakończenia realizacji {tz:%d.%m.%Y}")
        od, do = _d(W.get("okres_kwalifikowalnosci_od")), _d(W.get("okres_kwalifikowalnosci_do"))
        if od or do:
            o.append("okres kwalifikowalności wydatków" + (f" od {od:%d.%m.%Y}" if od else "") + (f" do {do:%d.%m.%Y}" if do else ""))
        tr = [t for t in (W.get("transze") or []) if isinstance(t, dict)]
        if tr:
            o.append("transze: " + "; ".join(" ".join(x for x in (f"{t.get('nr') or i + 1})", _zl(_kw(t["kwota"])) if _kw(t.get("kwota")) else "",
                                                                  f"do {_d(t['termin']):%d.%m.%Y}" if _d(t.get("termin")) else "",
                                                                  f"– {t['warunek']}" if t.get("warunek") else "") if x)
                                              for i, t in enumerate(tr)))
        wym = [w.get("wymog") for w in (W.get("wymagania_umowy_wykonawczej") or []) if isinstance(w, dict) and w.get("wymog")]
        if wym:
            o.append("wymagania wobec umowy z wykonawcą: " + "; ".join(wym[:15]))
        if W.get("obowiazki_informacyjne"):
            o.append("obowiązki informacyjne: " + "; ".join(str(x) for x in W["obowiazki_informacyjne"][:5]))
        dok = [d.get("dokument") for d in (W.get("dokumenty_rozliczenia") or []) if isinstance(d, dict) and d.get("dokument")]
        if dok:
            o.append("dokumenty do rozliczenia, które musi dostarczyć wykonawca: " + "; ".join(dok[:8]))
        if not z.get("odczytano") and not any(W.get(k) for k in ("kwota", "termin_zakonczenia_realizacji")):
            o.append("umowa finansowania nie została jeszcze odczytana – szczegóły oznacz [UZUPEŁNIJ: wymagania instytucji finansującej]")
        cz.append(", ".join(o))
    kn = koniec_robot_najpozniej(zrodla)
    return (" | ".join(cz) + ". ZASTOSUJ W DOKUMENTACH: (1) termin wykonania" + (f" – zakończenie robót najpóźniej {kn:%d.%m.%Y} ({ZAPAS_DNI} dni przed "
            "terminem z umowy finansowania, na odbiór końcowy i rozliczenie)" if kn else " zgodny z terminem z umowy finansowania z zapasem na odbiór i rozliczenie")
            + "; (2) harmonogram rzeczowo-finansowy z etapami i odbiorami częściowymi dopasowanymi do transz, płatności częściowe po odbiorach etapów; "
            "(3) w umowie: obowiązki wykonawcy wobec instytucji finansującej (kontrole, dokumenty do rozliczenia, oznakowanie, archiwizacja), "
            "zmiana umowy wymagająca zgody instytucji finansującej, gdy tak stanowi umowa finansowania, faktury i protokoły w podziale na koszty "
            "kwalifikowalne i niekwalifikowalne; (4) w zapytaniu / SWZ: informacja o źródle finansowania.")


def harmonogram_szkic(zrodla, start=None):
    """Szkic harmonogramu dla kreatora: etap na każdą transzę (termin transzy minus 30 dni na odbiór i wniosek), koniec robót najpóźniej."""
    kn = koniec_robot_najpozniej(zrodla)
    tr = sorted(((_d(t.get("termin")), t) for z in zrodla for t in ((z.get("wymagania") or {}).get("transze") or []) if isinstance(t, dict)),
                key=lambda x: x[0] or dt.date.max)
    et = []
    for i, (d, t) in enumerate(tr):
        do = d - dt.timedelta(days=ZAPAS_DNI) if d else None
        if kn and do and do > kn:
            do = kn
        et.append({"nr": i + 1, "do": do.isoformat() if do else "", "kwota": _kw(t.get("kwota")) or None,
                   "opis": f"Etap {i + 1} – odbiór częściowy pod transzę {t.get('nr') or i + 1}" + (f" ({t['warunek']})" if t.get("warunek") else "")})
    return {"koniec_najpozniej": kn.isoformat() if kn else "", "etapy": et}
