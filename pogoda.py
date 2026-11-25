# -*- coding: utf-8 -*-
"""
Monitoring pogody na budowie.

Źródła (ogólnodostępne, bez kluczy):
 - IMGW-PIB, dane synoptyczne (danepubliczne.imgw.pl/api/data/synop) – bieżący pomiar najbliższej stacji synoptycznej,
   zapisywany w historii budowy przy każdym odświeżeniu (dowód pomiarowy),
 - Open-Meteo (api.open-meteo.com) – dane godzinowe dla współrzędnych budowy: ostatnie 92 dni i prognoza 7 dni,
   starsze okresy z archiwum (archive-api.open-meteo.com).

Ocena dnia: w godzinach pracy (np. 7–17) sprawdzane są progi dla rodzaju robót – temperatura minimalna i maksymalna,
opad deszczu, opad śniegu, prędkość wiatru. Dzień roboczy z przekroczeniem = dzień z warunkami uniemożliwiającymi prace.
"""
import datetime as dt
import json
import math
import re
import unicodedata
import urllib.parse
import urllib.request

import modul_oferty as MO
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

IMGW_SYNOP = "https://danepubliczne.imgw.pl/api/data/synop"
IMGW_METEO = "https://danepubliczne.imgw.pl/api/data/meteo"  # sieć telemetryczna IMGW-PIB: ok. 790 stacji (opad ~700, temperatura i wiatr ~315)
PARAMETRY_METEO = [  # (klucz, pole wartości, pole czasu, opis, jednostka)
    ("opad", "opad_10min", "opad_10min_data", "Opad (suma 10 min)", "mm"),
    ("temperatura", "temperatura_powietrza", "temperatura_powietrza_data", "Temperatura powietrza", "°C"),
    ("temperatura_gruntu", "temperatura_gruntu", "temperatura_gruntu_data", "Temperatura gruntu", "°C"),
    ("wiatr", "wiatr_srednia_predkosc", "wiatr_srednia_predkosc_data", "Wiatr – prędkość średnia", "m/s"),
    ("wiatr_max", "wiatr_predkosc_maksymalna", "wiatr_predkosc_maksymalna_data", "Wiatr – prędkość maksymalna", "m/s"),
    ("poryw", "wiatr_poryw_10min", "wiatr_poryw_10min_data", "Poryw wiatru (10 min)", "m/s"),
    ("wilgotnosc", "wilgotnosc_wzgledna", "wilgotnosc_wzgledna_data", "Wilgotność względna", "%"),
]
OM_PROGNOZA = "https://api.open-meteo.com/v1/forecast"
OM_ARCHIWUM = "https://archive-api.open-meteo.com/v1/archive"

# Stacje synoptyczne IMGW-PIB – przybliżone położenie (do wyboru najbliższej stacji)
STACJE = {
    "bialystok": (53.11, 23.16), "bielsko biala": (49.81, 19.00), "chojnice": (53.72, 17.55), "czestochowa": (50.81, 19.09),
    "elblag": (54.22, 19.55), "gdansk": (54.38, 18.47), "gorzow": (52.74, 15.28), "hel": (54.60, 18.81),
    "jelenia gora": (50.90, 15.79), "kalisz": (51.78, 18.08), "kasprowy wierch": (49.23, 19.98), "katowice": (50.24, 19.03),
    "ketrzyn": (54.07, 21.37), "kielce": (50.81, 20.69), "klodzko": (50.44, 16.61), "kolo": (52.20, 18.66),
    "kolobrzeg": (54.16, 15.58), "koszalin": (54.20, 16.16), "kozienice": (51.56, 21.54), "krakow": (50.08, 19.80),
    "krosno": (49.71, 21.77), "legnica": (51.19, 16.21), "leszno": (51.83, 16.53), "lebork": (54.55, 17.75),
    "lesko": (49.47, 22.34), "lublin": (51.22, 22.39), "leba": (54.75, 17.53), "lodz": (51.72, 19.40),
    "mikolajki": (53.79, 21.58), "mlawa": (53.10, 20.36), "nowy sacz": (49.63, 20.69), "olsztyn": (53.77, 20.42),
    "opole": (50.63, 17.97), "ostroleka": (53.07, 21.56), "pila": (53.13, 16.75), "platforma": (55.48, 18.18),
    "plock": (52.59, 19.73), "poznan": (52.42, 16.83), "przemysl": (49.81, 22.77), "raciborz": (50.06, 18.19),
    "resko": (53.77, 15.41), "rzeszow": (50.11, 22.04), "sandomierz": (50.70, 21.72), "siedlce": (52.18, 22.25),
    "slubice": (52.35, 14.62), "sulejow": (51.35, 19.87), "suwalki": (54.13, 22.95), "szczecin": (53.40, 14.62),
    "szczecinek": (53.72, 16.68), "sniezka": (50.74, 15.74), "swinoujscie": (53.92, 14.24), "tarnow": (50.03, 20.98),
    "terespol": (52.08, 23.62), "torun": (53.04, 18.60), "ustka": (54.59, 16.85), "warszawa": (52.16, 20.96),
    "wielun": (51.21, 18.56), "wlodawa": (51.55, 23.53), "wroclaw": (51.10, 16.88), "zakopane": (49.29, 19.96),
    "zamosc": (50.70, 23.20), "zielona gora": (51.93, 15.53),
}
GORSKIE = {"sniezka", "kasprowy wierch", "platforma"}  # szczyty i platforma morska – pomijane przy wyborze najbliższej

PRESETY = {
    "elewacja": {"nazwa": "Roboty elewacyjne: ocieplenie ETICS, tynki, malowanie", "tmin": 5, "tmax": 25, "opad": 0.5, "snieg": 0, "wiatr": 10},
    "betonowe": {"nazwa": "Roboty betonowe i murowe", "tmin": 5, "tmax": 30, "opad": 5, "snieg": 0, "wiatr": 15},
    "dachowe": {"nazwa": "Roboty dachowe i na wysokości (papa, pokrycia, rusztowania)", "tmin": 5, "tmax": 35, "opad": 0.5, "snieg": 0, "wiatr": 10},
    "ziemne": {"nazwa": "Roboty ziemne, drogowe, nawierzchnie bitumiczne", "tmin": 5, "tmax": 35, "opad": 5, "snieg": 0, "wiatr": 20},
    "wlasne": {"nazwa": "Własne progi", "tmin": 5, "tmax": 30, "opad": 1, "snieg": 0, "wiatr": 12},
}
DNI_TYG = ["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."]


def norm(t):
    t = unicodedata.normalize("NFKD", str(t or "").replace("ł", "l").replace("Ł", "L")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]+", " ", t).strip().replace("  ", " ")


def km(a1, o1, a2, o2):
    r = 6371.0
    p1, p2 = math.radians(a1), math.radians(a2)
    dp, dl = math.radians(a2 - a1), math.radians(o2 - o1)
    return 2 * r * math.asin(math.sqrt(math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))


def _get_json(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Bidivia/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _f(x):
    return liczba(x)


def najblizsze_meteo(lat, lon, dane=None, max_km=80):
    """Najbliższa stacja sieci telemetrycznej IMGW-PIB OSOBNO dla każdego parametru (stacja z aktualnym pomiarem tego parametru):
    {klucz: {opis, jednostka, stacja, kod, odl_km, wysokosc, wartosc, czas}}. Stacje dalej niż max_km są pomijane."""
    if dane is None:
        try:
            dane = _get_json(IMGW_METEO, timeout=40)
        except Exception:
            return {}
    wyn = {}
    for klucz, pole, pole_czas, opis, jedn in PARAMETRY_METEO:
        naj = None
        for st in dane or []:
            a, o, v = _f(st.get("lat")), _f(st.get("lon")), _f(st.get(pole))
            if a is None or o is None or v is None:
                continue
            try:  # tylko aktualne pomiary (najwyżej 6 godzin) – stacja z nieaktualnym odczytem jest pomijana
                if _teraz_utc() - dt.datetime.fromisoformat(str(st.get(pole_czas))[:19]) > dt.timedelta(hours=6):  # czas IMGW – UTC
                    continue
            except ValueError:
                continue
            d = km(lat, lon, a, o)
            if d <= max_km and (not naj or d < naj[0]):
                naj = (d, st, v)
        if naj:
            d, st, v = naj
            wyn[klucz] = {"opis": opis, "jednostka": jedn, "stacja": str(st.get("nazwa_stacji") or "").title(), "kod": st.get("kod_stacji"),
                          "odl_km": round(d, 1), "wysokosc": st.get("wysokosc_npm"), "wartosc": v, "czas": st.get(pole_czas)}
    return wyn


def najblizsza_stacja(lat, lon, pomiary=None):
    """Najbliższa stacja synoptyczna IMGW z bieżącym pomiarem: {nazwa, id, odl_km, pomiar{...}} albo None."""
    if pomiary is None:
        try:
            pomiary = _get_json(IMGW_SYNOP)
        except Exception:
            pomiary = []
    naj = None
    for p in pomiary or []:
        k = norm(p.get("stacja"))
        wsp = STACJE.get(k)
        if not wsp or k in GORSKIE:
            continue
        d = km(lat, lon, *wsp)
        if not naj or d < naj[0]:
            naj = (d, p)
    if not naj:
        return None
    d, p = naj
    return {"nazwa": p.get("stacja"), "id": p.get("id_stacji"), "odl_km": round(d, 1),
            "pomiar": {"data": p.get("data_pomiaru"), "godzina": p.get("godzina_pomiaru"), "temperatura": _f(p.get("temperatura")),
                       "wiatr": _f(p.get("predkosc_wiatru")), "opad": _f(p.get("suma_opadu")), "wilgotnosc": _f(p.get("wilgotnosc_wzgledna")),
                       "cisnienie": _f(p.get("cisnienie"))}}


def godzinowe(lat, lon, od, do):
    """Dane godzinowe Open-Meteo dla współrzędnych budowy w okresie od–do (daty) – ostatnie 92 dni + prognoza z API prognoz,
    starsze z archiwum. Zwraca {data: [ {godz, t, opad, deszcz, snieg, wiatr, porywy} ]}."""
    dzis = dt.date.today()
    wyn = {}
    zm = "temperature_2m,precipitation,rain,snowfall,wind_speed_10m,wind_gusts_10m"
    czesci = []
    granica = dzis - dt.timedelta(days=90)
    if od < granica:
        czesci.append((OM_ARCHIWUM, {"start_date": od.isoformat(), "end_date": min(do, granica - dt.timedelta(days=1)).isoformat()}))
    if do >= granica:
        start = max(od, granica)
        czesci.append((OM_PROGNOZA, {"start_date": start.isoformat(), "end_date": min(do, dzis + dt.timedelta(days=7)).isoformat()}))
    for url, zakres in czesci:
        q = {"latitude": round(lat, 4), "longitude": round(lon, 4), "hourly": zm, "timezone": "Europe/Warsaw",
             "wind_speed_unit": "ms", **zakres}
        d = _get_json(f"{url}?{urllib.parse.urlencode(q)}", timeout=40).get("hourly", {})
        for i, czas in enumerate(d.get("time", [])):
            data, godz = czas[:10], int(czas[11:13])
            g = lambda k: (d.get(k) or [None] * (i + 1))[i]
            wyn.setdefault(data, []).append({"godz": godz, "t": g("temperature_2m"), "opad": g("precipitation"), "deszcz": g("rain"),
                                             "snieg": g("snowfall"), "wiatr": g("wind_speed_10m"), "porywy": g("wind_gusts_10m")})
    return wyn


def ocen_dzien(data, godziny, kr, godz_od=7, godz_do=17, soboty=False, pomiary_imgw=None):
    """Ocena jednego dnia w godzinach pracy. kr: progi {tmin, tmax, opad, snieg, wiatr}."""
    d = dt.date.fromisoformat(data)
    try:
        from progi import swieta
        swieto = d in swieta(d.year)
    except ImportError:
        swieto = False
    # dzień ustawowo wolny od pracy nie jest dniem roboczym – nie jest dniem utraconym na budowie (ustawa o dniach wolnych od pracy)
    rob = (d.weekday() < 5 or (soboty and d.weekday() == 5)) and not swieto
    h = [x for x in godziny if godz_od <= x["godz"] < godz_do]
    val = lambda k: [x[k] for x in h if x.get(k) is not None]
    t, opad, snieg, wiatr, por = val("t"), val("opad"), val("snieg"), val("wiatr"), val("porywy")
    w = {"data": data, "dzien": DNI_TYG[d.weekday()], "roboczy": rob, "prognoza": d > dt.date.today(),
         "tmin": round(min(t), 1) if t else None, "tmax": round(max(t), 1) if t else None,
         "opad": round(sum(opad), 1) if opad else 0.0, "snieg": round(sum(snieg), 1) if snieg else 0.0,
         "wiatr": round(max(wiatr), 1) if wiatr else None, "porywy": round(max(por), 1) if por else None, "powody": []}
    if not h:
        w["brak_danych"] = True
        return w
    zl = lambda x: f"{x:g}".replace(".", ",")
    if w["tmin"] is not None and w["tmin"] < kr["tmin"]:
        w["powody"].append(f"temperatura w godzinach pracy do {zl(w['tmin'])}°C – poniżej wymaganych +{zl(kr['tmin'])}°C")
    if w["tmax"] is not None and w["tmax"] > kr["tmax"]:
        w["powody"].append(f"temperatura do {zl(w['tmax'])}°C – powyżej dopuszczalnych {zl(kr['tmax'])}°C")
    if w["opad"] >= max(0.1, kr["opad"]) and w["opad"] - w["snieg"] * 0.7 > 0:
        w["powody"].append(f"opady deszczu {zl(w['opad'])} mm w godzinach pracy")
    if w["snieg"] > kr["snieg"]:
        w["powody"].append(f"opady śniegu {zl(w['snieg'])} cm")
    if w["wiatr"] is not None and w["wiatr"] > kr["wiatr"]:
        w["powody"].append(f"wiatr do {zl(w['wiatr'])} m/s (porywy {zl(w['porywy'] or 0)} m/s) – powyżej {zl(kr['wiatr'])} m/s")
    w["niekorzystny"] = bool(w["powody"])
    if pomiary_imgw:
        w["imgw"] = [p for p in pomiary_imgw if p.get("data") == data]
    return w


def analiza(lat, lon, od, do, kr, godz_od=7, godz_do=17, soboty=False, pomiary_imgw=None, meteo_dni=None):
    dane = godzinowe(lat, lon, od, do)
    dni = []
    d = od
    while d <= do:
        k = d.isoformat()
        if k in dane:
            x = ocen_dzien(k, dane[k], kr, godz_od, godz_do, soboty, pomiary_imgw)
            D = (meteo_dni or {}).get(k)
            if D:  # pomiary najbliższych stacji telemetrycznych IMGW-PIB z historii budowy
                x["meteo"] = {kk: ({z: v for z, v in vv.items() if z != "suma_"} if isinstance(vv, dict) else vv) for kk, vv in D.items()}
                x["meteo_kompletnosc"] = round(min(1.0, (D.get("opad") or {}).get("n", 0) / 144) * 100)
                pw = ocena_meteo(D, kr) if x.get("roboczy") and not x.get("prognoza") else []
                if pw:
                    x["powody"] = list(x.get("powody") or []) + pw
                    x["niekorzystny"] = True
                    x["potwierdzone_pomiarem"] = True
                od_ = D.get("opad_dobowy") or {}
                if od_ and x["meteo_kompletnosc"] < 80 and (od_.get("wartosc") or 0) >= max(0.1, kr["opad"]):
                    x["uwaga_meteo"] = (f"IMGW-PIB: opad dobowy {str(od_['wartosc']).replace('.', ',')} mm ({od_.get('okres', '')}, stacja {od_.get('stacja', '')}) – "
                                        "brak kompletu odczytów 10-minutowych; sprawdź, czy padało w godzinach pracy (pełne dane: archiwum IMGW po zakończeniu miesiąca)")
            dni.append(x)
        d += dt.timedelta(days=1)
    przeszle = [x for x in dni if not x["prognoza"]]
    return {"dni": dni, "robocze": sum(1 for x in przeszle if x["roboczy"]),
            "niekorzystne": sum(1 for x in przeszle if x["roboczy"] and x.get("niekorzystny")),
            "prognoza_niekorzystne": sum(1 for x in dni if x["prognoza"] and x["roboczy"] and x.get("niekorzystny"))}


# ============================================================ pismo do zamawiającego
LICZENIE_TERMINU = {"robocze": "dni robocze", "kalendarzowe": "dni kalendarzowe"}


def dzien_roboczy(d):
    """Dzień roboczy według umowy: poniedziałek–piątek bez dni ustawowo wolnych od pracy (ustawa z 18.01.1951 o dniach wolnych od pracy)."""
    try:
        from progi import swieta
        sw = d in swieta(d.year)
    except ImportError:
        sw = False
    return d.weekday() < 5 and not sw


def dodaj_dni_robocze(od, n):
    """Data po upływie n dni roboczych liczonych od dnia następującego po dacie „od” (H3-01: dotąd n dni dodawano jako kalendarzowe)."""
    d, n = od, max(0, int(n or 0))
    while n:
        d += dt.timedelta(days=1)
        if dzien_roboczy(d):
            n -= 1
    return d


def przedluzenie(dni, termin=None, liczenie="robocze", baza=None):
    """Przedłużenie o „dni” dni roboczych z warunkami uniemożliwiającymi prace – według sposobu liczenia terminu w umowie.
    robocze: nowy termin = termin + dni robocze (bez sobót, niedziel i świąt); kalendarzowe: jawne przeliczenie na dni kalendarzowe
    (tyle dni kalendarzowych, ile mija od terminu do upływu tych dni roboczych). Zwraca {dni_robocze, dni_kalendarzowe, nowy_termin, liczenie, baza}."""
    liczenie = liczenie if liczenie in LICZENIE_TERMINU else "robocze"
    b = termin or baza or dt.date.today()
    nowy_ = dodaj_dni_robocze(b, dni)
    return {"dni_robocze": int(dni), "dni_kalendarzowe": (nowy_ - b).days, "nowy_termin": nowy_ if termin else None,
            "liczenie": liczenie, "baza": b}


def zdanie_dziennika(niek_daty, dziennik=None, wpisy_edb=""):
    """Zdanie o dzienniku budowy – tylko to, co wynika z danych (H3-01): numery wpisów podane przez wykonawcę albo daty raportów dziennych
    zapisanych w programie; dla dni bez wpisu – pole do uzupełnienia (dotąd pismo zawsze twierdziło „odnotowane w dzienniku budowy”)."""
    if not niek_daty:
        return ""
    if str(wpisy_edb or "").strip():
        return f"Warunki te zostały odnotowane w dzienniku budowy – wpisy: {str(wpisy_edb).strip()[:300]}."
    jest = sorted({w.get("data") for w in (dziennik or []) if isinstance(w, dict) and w.get("data") in set(niek_daty)})
    brak = [x for x in sorted(niek_daty) if x not in jest]
    fd = lambda x: f"{dt.date.fromisoformat(x):%d.%m.%Y}"
    if not jest:
        return "Dni te zostały odnotowane w dzienniku budowy: [UZUPEŁNIJ: wpisy w dzienniku budowy]."
    t = ("Warunki w tych dniach opisano w raportach dziennych budowy prowadzonych przez Wykonawcę – wpisy z dni: "
         + ", ".join(fd(x) for x in jest) + "; numery wpisów w dzienniku budowy: [UZUPEŁNIJ: wpisy w dzienniku budowy].")
    if brak:
        t += " Dla dni " + ", ".join(fd(x) for x in brak) + " brak raportu dziennego w programie – [UZUPEŁNIJ: wpisy w dzienniku budowy]."
    return t


def pismo_docx(sciezka, rodzaj, wyk, zam, budowa, umowa, okres, wynik, kr, stacja, lokalizacja, dni_wydl, nowy_termin, uwagi, miejsce,
               liczenie="robocze", stary_termin=None, dziennik=None, wpisy_edb=""):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    dzis = dt.date.today()
    A(f"{miejsce or '[UZUPEŁNIJ: miejscowość]'}, dnia {dzis:%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A(f"{wyk['nazwa']}\n{wyk['adres']}" + (f"\nNIP: {wyk['nip']}" if wyk.get("nip") else ""), rozmiar=9)
    A(f"{zam.get('nazwa') or '[UZUPEŁNIJ: Zamawiający]'}\n{zam.get('adres') or ''}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    wniosek = rodzaj == "wniosek"
    A(("ZGŁOSZENIE NIEKORZYSTNYCH WARUNKÓW ATMOSFERYCZNYCH\nI WNIOSEK O PRZEDŁUŻENIE TERMINU REALIZACJI" if wniosek
       else "INFORMACJA O NIEKORZYSTNYCH WARUNKACH ATMOSFERYCZNYCH\nUNIEMOŻLIWIAJĄCYCH PROWADZENIE ROBÓT"), pogrub=True, rozmiar=13,
      wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"Dotyczy: umowy nr {umowa.get('nr') or '[UZUPEŁNIJ]'} z dnia {umowa.get('data') or '[UZUPEŁNIJ]'} na realizację zadania: {budowa}"
      + (f", adres budowy: {umowa['adres']}" if umowa.get("adres") else "") + ".", kursywa=True)
    od, do = okres
    A("Szanowni Państwo,")
    A(f"Wykonawca informuje, że w okresie od {od:%d.%m.%Y} r. do {do:%d.%m.%Y} r. na terenie budowy wystąpiły warunki atmosferyczne "
      f"uniemożliwiające prowadzenie robót ({kr.get('nazwa', 'roboty budowlane').lower()}) zgodnie z wymaganiami technologicznymi producentów "
      "materiałów, specyfikacją techniczną wykonania i odbioru robót oraz przepisami BHP. Za dni z warunkami uniemożliwiającymi prace "
      f"przyjęto dni robocze, w których w godzinach pracy ({okres_godz(kr)}) wystąpiło co najmniej jedno z poniższych:")
    for x in (f"temperatura powietrza poniżej +{kr['tmin']:g}°C", f"temperatura powietrza powyżej +{kr['tmax']:g}°C",
              f"opady deszczu (od {kr['opad']:g} mm)", "opady śniegu", f"prędkość wiatru powyżej {kr['wiatr']:g} m/s"):
        A(x.replace(".", ","), styl="List Bullet")
    niek = [x for x in wynik["dni"] if x["roboczy"] and x.get("niekorzystny") and not x["prognoza"]]
    A(f"W tym okresie na {wynik['robocze']} dni roboczych wystąpiło {len(niek)} dni z warunkami uniemożliwiającymi prowadzenie robót:", pogrub=True)
    wiersze = [["Data", "Temp. min–max [°C]", "Opad [mm]", "Śnieg [cm]", "Wiatr / porywy [m/s]", "Przyczyna"]]
    zl = lambda v: "–" if v is None else f"{v:g}".replace(".", ",")
    for x in niek:
        wiersze.append([f"{dt.date.fromisoformat(x['data']):%d.%m.%Y} ({x['dzien']})", f"{zl(x['tmin'])} … {zl(x['tmax'])}", zl(x["opad"]),
                        zl(x["snieg"]), f"{zl(x['wiatr'])} / {zl(x['porywy'])}", "; ".join(x["powody"])])
    if len(wiersze) > 1:
        MO._tabela(d, wiersze)
    else:
        A("(brak dni spełniających kryteria w podanym okresie)")
    imgw = [p for x in niek for p in (x.get("imgw") or [])]
    meteo = (stacja or {}).get("meteo") or {}
    kmtxt = lambda v: f"{v:g}".replace(".", ",")
    grupy = {}  # stacja → mierzone na niej parametry
    for x in meteo.values():
        grupy.setdefault((x["stacja"], x["odl_km"]), []).append(x["opis"].lower())
    zrodla = (f"Dane pogodowe: dane godzinowe Open-Meteo dla lokalizacji budowy ({lokalizacja})"
              + (f"; bieżące pomiary najbliższej stacji synoptycznej IMGW-PIB: {stacja['nazwa']} (ok. {kmtxt(stacja['odl_km'])} km od budowy)"
                 if stacja and stacja.get("nazwa") else "")
              + ("; najbliższe stacje sieci telemetrycznej IMGW-PIB: " + "; ".join(
                  f"{n} (ok. {kmtxt(d)} km od budowy) – {', '.join(par)}" for (n, d), par in sorted(grupy.items(), key=lambda g: g[0][1])) if grupy else "") + ".")
    A(zrodla, rozmiar=9)
    if imgw:
        A("Pomiary stacji IMGW-PIB zapisane w dniach niekorzystnych:", rozmiar=9, pogrub=True)
        MO._tabela(d, [["Data", "Godz.", "Temp. [°C]", "Wiatr [m/s]", "Opad [mm]"]] +
                   [[p.get("data", ""), str(p.get("godzina", "")), zl(p.get("temperatura")), zl(p.get("wiatr")), zl(p.get("opad"))] for p in imgw])
    if wniosek:
        pd = przedluzenie(dni_wydl, stary_termin, liczenie, baza=do)
        if pd["liczenie"] == "kalendarzowe":  # umowa liczy termin w dniach kalendarzowych – przeliczenie jawne (H3-01)
            ile = (f"{pd['dni_kalendarzowe']} dni kalendarzowych, co odpowiada {dni_wydl} dniom roboczym, w których warunki atmosferyczne "
                   f"uniemożliwiały prowadzenie robót (przeliczenie: {dni_wydl} dni roboczych – bez sobót, niedziel i dni ustawowo wolnych od pracy – "
                   f"liczonych od dnia następującego po {'dotychczasowym terminie ' + format(pd['baza'], '%d.%m.%Y') + ' r.' if stary_termin else 'dniu ' + format(pd['baza'], '%d.%m.%Y') + ' r. (brak terminu umownego w programie – przeliczenie orientacyjne)'}, "
                   f"upływa po {pd['dni_kalendarzowe']} dniach kalendarzowych)")
        else:
            ile = f"{dni_wydl} dni roboczych (termin w umowie liczony w dniach roboczych – bez sobót, niedziel i dni ustawowo wolnych od pracy)"
        A(f"W związku z powyższym, na podstawie postanowień umowy dotyczących zmiany terminu realizacji z przyczyn niezależnych od Wykonawcy "
          f"(warunki atmosferyczne), Wykonawca wnosi o przedłużenie terminu realizacji przedmiotu umowy o {ile}"
          + (f", tj. do dnia {nowy_termin:%d.%m.%Y} r." if nowy_termin else ", tj. do dnia [UZUPEŁNIJ: nowy termin].")
          + " oraz o odpowiednią aktualizację harmonogramu rzeczowo-finansowego i zawarcie aneksu do umowy.", pogrub=True)
    else:
        A("Wykonawca zastrzega prawo do wystąpienia o przedłużenie terminu realizacji o liczbę dni, w których warunki atmosferyczne "
          "uniemożliwiały prowadzenie robót, i prosi o potwierdzenie przyjęcia niniejszej informacji.")
    if uwagi:
        A(uwagi)
    zd = zdanie_dziennika([x["data"] for x in niek], dziennik, wpisy_edb)
    A((zd + " " if zd else "") + "Na żądanie Zamawiającego Wykonawca przedstawi urzędowe dane meteorologiczne IMGW-PIB "
      "(danepubliczne.imgw.pl) dla wskazanego okresu.", rozmiar=9, kursywa=True)
    A("\n\nZ poważaniem\n\n\n..........................................\n(podpis Wykonawcy)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("Załącznik: zestawienie warunków pogodowych w okresie " + f"{od:%d.%m.%Y}–{do:%d.%m.%Y}", rozmiar=9)
    d.add_page_break()
    A(f"ZAŁĄCZNIK – zestawienie warunków pogodowych w godzinach pracy ({okres_godz(kr)})", pogrub=True)
    MO._tabela(d, [["Data", "Dzień", "Temp. [°C]", "Opad [mm]", "Śnieg [cm]", "Wiatr [m/s]", "Ocena"]] +
               [[x["data"], x["dzien"], f"{zl(x['tmin'])} … {zl(x['tmax'])}", zl(x["opad"]), zl(x["snieg"]), zl(x["wiatr"]),
                 ("NIEKORZYSTNY" if x.get("niekorzystny") else "sprzyjający") if x["roboczy"] else "dzień wolny"]
                for x in wynik["dni"] if not x["prognoza"]])
    d.save(sciezka)


def okres_godz(kr):
    return f"{int(kr.get('godz_od', 7))}:00–{int(kr.get('godz_do', 17))}:00"



# ---------------------------------------------------------------- historia pomiarów sieci telemetrycznej (zapis co 10 minut)
def _teraz_utc():
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def _lokalnie(czas_utc):
    """Czas pomiaru IMGW (UTC, bez strefy) → czas polski."""
    from zoneinfo import ZoneInfo
    return dt.datetime.fromisoformat(str(czas_utc)[:19]).replace(tzinfo=dt.timezone.utc).astimezone(ZoneInfo("Europe/Warsaw")).replace(tzinfo=None)


def zapisz_meteo(hist, lat, lon, dane, godz_od=7, godz_do=17, dni_max=400):
    """Dopisuje do historii budowy nowe pomiary najbliższych stacji telemetrycznych (osobno dla każdego parametru).
    Opad: suma kolejnych sum 10-minutowych (każdy odczyt liczony raz – po czasie pomiaru); temperatura: min/max (całodobowo i w godzinach pracy);
    wiatr i porywy: maksimum; wilgotność: średnia. „n” – liczba zapisanych odczytów (kompletność: opad 144 odczyty na dobę)."""
    hist.setdefault("ostatnie", {})
    hist.setdefault("dni", {})
    hist.setdefault("stacje", {})
    nowe = 0
    for klucz, x in najblizsze_meteo(lat, lon, dane).items():
        czas = str(x.get("czas") or "")[:19]
        if not czas or czas <= hist["ostatnie"].get(klucz, ""):
            continue
        hist["ostatnie"][klucz] = czas
        hist["stacje"][klucz] = {"stacja": x["stacja"], "odl_km": x["odl_km"], "kod": x.get("kod")}
        _dodaj_odczyt(hist["dni"], klucz, czas, x["wartosc"], x["stacja"], godz_od, godz_do)
        nowe += 1
    for d in sorted(hist["dni"])[:-dni_max]:
        hist["dni"].pop(d, None)
    return nowe


def _dodaj_odczyt(dni, klucz, czas, v, stacja, godz_od=7, godz_do=17):
    """Jeden odczyt (czas UTC) do agregatów dnia (czas polski)."""
    if True:
        lok = _lokalnie(czas) - (dt.timedelta(minutes=5) if klucz == "opad" else dt.timedelta(0))  # suma 10-min przypisana do środka przedziału
        D = dni.setdefault(lok.date().isoformat(), {})
        praca = godz_od <= lok.hour < godz_do
        P = D.setdefault(klucz, {"n": 0, "stacje": []})
        P["n"] += 1
        if klucz == "opad":
            P["suma"] = round(P.get("suma", 0) + v, 1)
            if praca:
                P["praca"] = round(P.get("praca", 0) + v, 1)
        elif klucz in ("temperatura", "temperatura_gruntu"):
            P["min"], P["max"] = min(P.get("min", v), v), max(P.get("max", v), v)
            if praca:
                P["min_praca"], P["max_praca"] = min(P.get("min_praca", v), v), max(P.get("max_praca", v), v)
        elif klucz == "wilgotnosc":
            P["suma_"] = P.get("suma_", 0) + v
            P["srednia"] = round(P["suma_"] / P["n"], 1)
        else:  # wiatr, wiatr_max, poryw
            P["max"] = max(P.get("max", v), v)
            if praca:
                P["max_praca"] = max(P.get("max_praca", v), v)
        if stacja not in P["stacje"]:
            P["stacje"].append(stacja)


def ocena_meteo(D, kr):
    """Przyczyny dnia niekorzystnego z POMIARÓW IMGW (najbliższe stacje) według kryteriów robót – albo [] (brak danych / bez przekroczeń)."""
    if not D:
        return []
    zl = lambda v: f"{v:g}".replace(".", ",")
    st = lambda k: f" ({', '.join(D[k].get('stacje') or [])})"
    pw = []
    t = D.get("temperatura") or {}
    if t.get("min_praca") is not None and t["min_praca"] < kr["tmin"]:
        pw.append(f"pomiar IMGW-PIB: temperatura w godzinach pracy do {zl(t['min_praca'])}°C – poniżej +{zl(kr['tmin'])}°C" + st("temperatura"))
    if t.get("max_praca") is not None and t["max_praca"] > kr["tmax"]:
        pw.append(f"pomiar IMGW-PIB: temperatura do {zl(t['max_praca'])}°C – powyżej {zl(kr['tmax'])}°C" + st("temperatura"))
    o = D.get("opad") or {}
    if o.get("praca", 0) >= max(0.1, kr["opad"]):
        pw.append(f"pomiar IMGW-PIB: opad w godzinach pracy {zl(o['praca'])} mm (doba {zl(o.get('suma', 0))} mm)" + st("opad"))
    w = D.get("wiatr_max") or D.get("wiatr") or {}
    if w.get("max_praca") is not None and w["max_praca"] > kr["wiatr"]:
        k_ = "wiatr_max" if D.get("wiatr_max") else "wiatr"
        pw.append(f"pomiar IMGW-PIB: wiatr do {zl(w['max_praca'])} m/s – powyżej {zl(kr['wiatr'])} m/s" + st(k_))
    return pw


# ---------------------------------------------------------------- uzupełnianie: oficjalny opad dobowy (hydro-back) i archiwum miesięczne IMGW
HYDRO_BACK_STATUS = "https://hydro-back.imgw.pl/station/meteo/status?id={kod}"
ARCHIWUM_MIES = "https://danepubliczne.imgw.pl/datastore/getfiledown/Arch/Telemetria/Meteo/{rok}/Meteo_{rok}-{mies:02d}.zip"
KODY_ARCH = {"temperatura": "B00300S", "temperatura_gruntu": "B00305A", "opad": "B00608S", "wiatr": "B00702A", "wiatr_max": "B00703A",
             "poryw": "B00714A", "wilgotnosc": "B00802A"}  # kody parametrów IMGW (B00604S – opad dobowy, B00606S – godzinowy, B00608S – 10-min)


def opad_dobowy(kod, otworz=None):
    """Oficjalna dobowa suma opadu IMGW-PIB (doba klimatologiczna 06–06 UTC, przypisana do dnia, w którym się zaczęła): (dzień, mm) albo None."""
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Bidivia)"}), timeout=30))
    with otworz(HYDRO_BACK_STATUS.format(kod=kod)) as r:
        s = (json.loads(r.read().decode("utf-8")).get("status") or {}).get("precipDaily") or {}
    if s.get("value") is None or not s.get("date"):
        return None
    koniec = dt.datetime.fromisoformat(str(s["date"]).replace("Z", "")[:19])
    return (koniec - dt.timedelta(days=1)).date().isoformat(), _f(s["value"])


def stacje_kandydaci(lat, lon, dane, n=12):
    """Najbliższe stacje sieci telemetrycznej (bez względu na aktualność pomiaru) – do wyboru stacji w archiwum."""
    L = []
    for st in dane or []:
        a, o = _f(st.get("lat")), _f(st.get("lon"))
        if a is not None and o is not None:
            L.append((km(lat, lon, a, o), str(st.get("kod_stacji")), str(st.get("nazwa_stacji") or "").title()))
    return sorted(L)[:n]


def uzupelnij_z_archiwum(hist, plik_zip, rok, mies, kandydaci, godz_od=7, godz_do=17):
    """Pełne dane 10-minutowe z miesięcznego archiwum IMGW: dla każdego parametru najbliższa stacja, która ma w archiwum dane;
    dni miesiąca budowane od nowa z kompletu odczytów (zastępują dni z lukami). Zwraca liczbę dni."""
    import zipfile
    kody = {k for _, k, _ in kandydaci}
    nazwy = {k: (d, n) for d, k, n in kandydaci}
    nowe_dni = {}
    z = zipfile.ZipFile(plik_zip)
    for klucz, kod_par in KODY_ARCH.items():
        nazwa_pliku = next((n for n in z.namelist() if n.startswith(kod_par + "_")), None)
        if not nazwa_pliku:
            continue
        wg_stacji = {}
        with z.open(nazwa_pliku) as f:
            for linia in f:
                kod = linia[:9].decode("ascii", "ignore")
                if kod not in kody:
                    continue
                c = linia.decode("cp1250", "replace").strip().split(";")
                if len(c) >= 4:
                    v = _f(c[3])
                    if v is not None:
                        wg_stacji.setdefault(c[0], []).append((c[2] + ":00", v))
        wyb = min((k for k in wg_stacji), key=lambda k: nazwy[k][0], default=None)
        if not wyb:
            continue
        hist.setdefault("stacje_archiwum", {})[klucz] = {"stacja": nazwy[wyb][1], "odl_km": round(nazwy[wyb][0], 1), "kod": wyb}
        for czas, v in sorted(wg_stacji[wyb]):
            _dodaj_odczyt(nowe_dni, klucz, czas, v, nazwy[wyb][1], godz_od, godz_do)
    pref = f"{rok}-{mies:02d}"
    for d, D in nowe_dni.items():
        if d.startswith(pref):
            D["_zrodlo"] = "archiwum IMGW-PIB (komplet 10-min)"
            if (hist.get("dni", {}).get(d) or {}).get("opad_dobowy"):
                D["opad_dobowy"] = hist["dni"][d]["opad_dobowy"]
            hist.setdefault("dni", {})[d] = D
    hist.setdefault("archiwum_miesiace", []).append(pref)
    return sum(1 for d in nowe_dni if d.startswith(pref))
