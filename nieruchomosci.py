# -*- coding: utf-8 -*-
"""Dział „DD / wycena nieruchomości”: wspólna teczka nieruchomości (identyfikacja, mapy, dokumenty, stan prawny, oględziny, rynek)
i trzy produkty – due diligence, analiza zabudowy, wycena (projekt operatu do zatwierdzenia przez rzeczoznawcę) – osobno albo w pakiecie."""
import datetime as dt
import json
import math
import re
import statistics
import urllib.parse
import urllib.request

import modul_oferty as MO
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

TYPY = {"budowlana": "Działka budowlana", "rolna": "Grunt rolny", "oze": "Grunt pod OZE", "dom": "Dom (działka z budynkiem)",
        "lokal": "Mieszkanie", "lokal_uzytkowy": "Lokal użytkowy", "komercyjny": "Obiekt komercyjny", "poprzemyslowy": "Teren poprzemysłowy"}
RODZAJ = {"budowlana": "dzialka", "rolna": "dzialka", "oze": "dzialka", "poprzemyslowy": "dzialka", "dom": "dom", "komercyjny": "dom", "lokal": "lokal", "lokal_uzytkowy": "lokal"}
POLA_LOKALU = [("nr_lokalu", "Numer lokalu"), ("pow_uzytkowa", "Powierzchnia użytkowa [m²]"), ("pokoje", "Liczba pokoi"), ("pietro", "Piętro"),
               ("kondygnacje_budynku", "Kondygnacji w budynku"), ("winda", "Winda (tak/nie)"), ("balkon", "Balkon / taras / ogródek"), ("piwnica", "Piwnica / komórka"),
               ("parking", "Miejsce postojowe / garaż"), ("forma_prawa", "Forma prawa (odrębna własność / spółdzielcze własnościowe)"), ("udzial", "Udział w częściach wspólnych"),
               ("ogrzewanie", "Ogrzewanie"), ("czynsz", "Opłaty miesięczne [zł]"), ("rok_budowy", "Rok budowy budynku"), ("technologia", "Technologia budynku"),
               ("standard", "Standard wykończenia (do remontu / przeciętny / wysoki)"), ("stan", "Stan techniczny"), ("rynek", "Rynek (wtórny / pierwotny)")]
POLA_DOMU = [("pow_uzytkowa", "Powierzchnia użytkowa budynku [m²]"), ("rok_budowy", "Rok budowy"), ("technologia", "Technologia (murowany / drewniany / szkieletowy)"),
             ("kondygnacje_budynku", "Kondygnacje"), ("standard", "Standard (do remontu / przeciętny / wysoki)"), ("stan", "Stan techniczny"), ("ogrzewanie", "Ogrzewanie"),
             ("budynki_dodatkowe", "Budynki dodatkowe (garaż, gospodarczy)"), ("rynek", "Rynek (wtórny / pierwotny)")]
PRODUKTY = {"dd": "Due diligence", "zabudowa": "Analiza zabudowy", "wycena": "Wycena"}
OBSZARY = {"prawo": "Stan prawny", "plan": "Planowanie przestrzenne", "zabytki": "Zabytki i archeologia", "sieci": "Sieci i przyłącza",
           "grunt": "Grunt i środowisko", "woda": "Woda i powódź", "przyroda": "Ochrona przyrody", "dostep": "Dostęp do drogi",
           "budynki": "Budynki – legalność i stan", "podatki": "Podatki i opłaty", "rynek": "Rynek i wartość"}
WAGI = {"czerwone": "może przekreślić zakup", "zolte": "wpływa na cenę lub czas", "zielone": "do odnotowania"}
STATUSY = {"do_sprawdzenia": "do sprawdzenia", "potwierdzone": "potwierdzone", "wykluczone": "wykluczone"}

# ---------------------------------------------------------------- mapy i rejestry (raport wstępny – odnośniki ze źródłem)
def odnosniki(teryt_id, lat=None, lon=None):
    q = urllib.parse.quote(teryt_id or "")
    return [
        ("Geoportal – działka, ewidencja, uzbrojenie terenu, plany", f"https://mapy.geoportal.gov.pl/imap/Imgp_2.html?identifyParcel={q}" if teryt_id else "https://mapy.geoportal.gov.pl/"),
        ("Zabytki i stanowiska archeologiczne (NID)", "https://mapy.zabytek.gov.pl/nid/"),
        ("Zagrożenie powodziowe (Hydroportal ISOK)", "https://wody.isok.gov.pl/imap_kzgw/?gpmap=gpPDF"),
        ("Geologia, osuwiska, tereny górnicze (PIG-PIB)", "https://geoportal.pgi.gov.pl/"),
        ("Formy ochrony przyrody, Natura 2000 (GDOŚ)", "https://geoserwis.gdos.gov.pl/mapy/"),
        ("Pozwolenia na budowę w okolicy (GUNB)", "https://wyszukiwarka.gunb.gov.pl/"),
        ("Księgi wieczyste – przeglądarka (eKW)", "https://przegladarka-ekw.ms.gov.pl/"),
    ]


# ---------------------------------------------------------------- identyfikacja działki – usługa lokalizacji działek GUGiK (ULDK)
ULDK = "https://uldk.gugik.gov.pl/"


def _uldk(params, timeout=20):
    """Zapytanie do ULDK. Pierwsza linia odpowiedzi: 0 / 1 albo liczba znalezionych działek (GetParcelByIdOrNr), -1 = brak wyników."""
    url = ULDK + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Bidivia/1.0"}), timeout=timeout) as r:
        t = r.read().decode("utf-8", "ignore").strip()
    linie = [l.strip() for l in t.splitlines()]
    pierwsza = linie[0] if linie else ""
    if not re.fullmatch(r"\d+", pierwsza.split()[0] if pierwsza else ""):
        raise ValueError("Nie znaleziono działki w ewidencji (usługa GUGiK): " + (pierwsza or "brak odpowiedzi"))
    wyn = []
    for l in linie[1:]:
        cz = l.split("|")
        if len(cz) >= 7:
            wyn.append({"geom": cz[0].split(";", 1)[-1], "teryt": cz[1], "wojewodztwo": cz[2], "powiat": cz[3], "gmina": cz[4], "obreb": cz[5], "numer": cz[6]})
    if not wyn:
        raise ValueError("Usługa GUGiK nie zwróciła działki – sprawdź numer i obręb.")
    return wyn


def opis_kandydata(x):
    """Krótki opis działki do listy wyboru (bez geometrii)."""
    return {"teryt": x.get("teryt"), "numer": x.get("numer"), "obreb": x.get("obreb"), "gmina": x.get("gmina"), "powiat": x.get("powiat"),
            "wojewodztwo": x.get("wojewodztwo"), "pow_ewid": round(pole(wkt_punkty(x.get("geom"))), 1) if x.get("geom") else None}


def identyfikuj(teryt=None, obreb_nr=None, lon=None, lat=None, x=None, y=None):
    """Działka po identyfikatorze TERYT, po „obręb numer” albo po współrzędnych (np. z adresu)."""
    res = "geom_wkt,teryt,voivodeship,county,commune,region,parcel"
    if teryt:
        return _uldk({"request": "GetParcelById", "id": teryt, "result": res, "srid": "2180"})
    if obreb_nr:
        return _uldk({"request": "GetParcelByIdOrNr", "id": obreb_nr, "result": res, "srid": "2180"})
    if x is not None and y is not None:  # układ PL-1992 (z rejestru adresów GUGiK)
        return _uldk({"request": "GetParcelByXY", "xy": f"{x},{y},2180", "result": res, "srid": "2180"})
    if lon is not None and lat is not None:
        return _uldk({"request": "GetParcelByXY", "xy": f"{lon},{lat},4326", "result": res, "srid": "2180"})
    raise ValueError("Podaj identyfikator działki, obręb i numer albo adres.")


UUG = "https://services.gugik.gov.pl/uug/"
NAGLOWKI_OSM = {"User-Agent": "Bidivia/1.0 (kontakt: biuro)"}
RE_KOD = re.compile(r"\b\d{2}-\d{3}\b")
RE_PREFIKS_ULICY = re.compile(r"(?i)^(ul\.?|ulica|al\.?|aleja|aleje|pl\.?|plac|os\.?|osiedle)\s+")


def rozbierz_adres(adres):
    """„ul. Grunwaldzka 2, 50-355 Wrocław” / „Kościuszki 50 Nowa Ruda” / „Pszenno 12” → miejscowość, ulica, numer budynku, numer lokalu."""
    t = re.sub(r"\s+", " ", RE_KOD.sub(" ", str(adres or ""))).strip(" ,")
    cz = [c.strip() for c in t.split(",") if c.strip()]
    miasto = ulica = numer = lokal = ""
    RE_NR = re.compile(r"^(.*?\D)\s+(\d+[A-Za-z]?)(?:\s*(?:/|m\.?|lok\.?)\s*(\d+[A-Za-z]?))?$")
    if len(cz) >= 2:
        z_nr = next((c for c in cz if RE_NR.match(c)), None)
        if z_nr:
            m = RE_NR.match(z_nr)
            ulica, numer, lokal = m.group(1).strip(), m.group(2), m.group(3) or ""
            miasto = next((c for c in cz if c is not z_nr), "")
        else:
            miasto, ulica = cz[-1], cz[0]
    elif cz:
        m = re.match(r"^(.*?\D)\s+(\d+[A-Za-z]?)(?:\s*/\s*(\d+[A-Za-z]?))?\s+([^\d].*)$", cz[0])  # „Kościuszki 50 Nowa Ruda”
        m2 = RE_NR.match(cz[0])
        if m:
            ulica, numer, lokal, miasto = m.group(1).strip(), m.group(2), m.group(3) or "", m.group(4).strip()
        elif m2:  # „Pszenno 12” – miejscowość bez ulic
            miasto, numer, lokal = m2.group(1).strip(), m2.group(2), m2.group(3) or ""
        else:
            miasto = cz[0]
    ulica = RE_PREFIKS_ULICY.sub("", ulica).strip()
    return {"miasto": miasto, "ulica": ulica, "numer": numer, "lokal": lokal}


def _numer_rowny(a, b):
    return bool(a) and str(a).strip().lower().replace(" ", "") == str(b or "").strip().lower().replace(" ", "")


def _ulica_zgodna(szukana, znaleziona):
    """„Kościuszki” = „Tadeusza Kościuszki”, ale „Kościuszki” ≠ „Kościelna”. Brak ulicy w zapytaniu (wieś) – zgodne, gdy brak ulicy w wyniku."""
    a = [w for w in re.findall(r"\w+", str(szukana or "").lower()) if len(w) > 2]
    b = re.findall(r"\w+", str(znaleziona or "").lower())
    if not a:
        return True  # wieś bez ulic – o zgodności decyduje numer i miejscowość
    return all(x in b for x in a)


def _uug(tekst, timeout=20):
    url = UUG + "?" + urllib.parse.urlencode({"request": "GetAddress", "address": tekst})
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Bidivia/1.0"}), timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8", "ignore"))
    return list((d.get("results") or {}).values())


def geokoduj_gugik(r):
    """Punkt adresowy z państwowego rejestru (PRG) przez geokoder GUGiK. Tylko pewne trafienie: zgodny numer i wysoka trafność nazwy."""
    if not r.get("numer") or not r.get("miasto"):
        return None
    zapytania = [f"{r['miasto']}, {r['ulica']} {r['numer']}"] if r.get("ulica") else [f"{r['miasto']}, {r['numer']}", f"{r['miasto']} {r['numer']}"]
    for q in zapytania:
        try:
            wyn = _uug(q)
        except Exception:
            return None
        for w in wyn:
            try:
                traf = float(w.get("accuracy") or 0)
            except ValueError:
                traf = 0
            ul = re.sub(r"(?i)^(ul|al|pl|os)\.\s*", "", str(w.get("street") or ""))
            if traf >= 0.8 and _numer_rowny(w.get("number"), r["numer"]) and _ulica_zgodna(r.get("ulica"), ul):
                return {"x": float(w["x"]), "y": float(w["y"]), "dokladnosc": "budynek", "zrodlo": "państwowy rejestr adresów (geokoder GUGiK)",
                        "adres_pelny": ", ".join(x for x in (f"{ul} {w.get('number')}".strip(), w.get("code") or "", w.get("city") or "") if x),
                        "miejscowosc": w.get("city") or "", "dzielnica": w.get("citypart") or "", "trafnosc": traf}
    return None


def _osm(params):
    q = dict(params, format="json", limit=5, countrycodes="pl", extratags=1, addressdetails=1)
    with urllib.request.urlopen(urllib.request.Request("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(q), headers=NAGLOWKI_OSM), timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def geokoduj(adres, szczegoly=False):
    """OpenStreetMap: najpierw zapytanie strukturalne (ulica + miejscowość), potem tekstowe. Preferuje wynik z tym samym numerem domu."""
    r = rozbierz_adres(adres)
    proby = []
    if r["miasto"] and r["numer"]:
        proby.append({"street": f"{r['numer']} {r['ulica']}".strip() if r["ulica"] else r["numer"], "city": r["miasto"]})
    proby += [{"q": adres}, {"q": RE_KOD.sub(" ", RE_PREFIKS_ULICY.sub("", str(adres or "")))}]
    pierwszy = None
    for i, pr in enumerate(proby):
        try:
            d = _osm(pr)
        except Exception:
            d = []
        for x in d:
            if r["numer"] and _numer_rowny((x.get("address") or {}).get("house_number"), r["numer"]):
                return x if szczegoly else (float(x["lon"]), float(x["lat"]))
        pierwszy = pierwszy or (d[0] if d else None)
        if pierwszy and not r["numer"]:
            break
    if not pierwszy:
        raise ValueError("Nie znaleziono adresu – podaj numer działki i obręb.")
    return pierwszy if szczegoly else (float(pierwszy["lon"]), float(pierwszy["lat"]))


def lokalizuj_adres(adres):
    """Adres → punkt (EPSG:2180 z rejestru GUGiK albo WGS84 z OSM) + informacja, czy trafiono w budynek, czy tylko w ulicę / miejscowość."""
    r = rozbierz_adres(adres)
    g = geokoduj_gugik(r)
    osm = None
    try:
        osm = geokoduj(adres, szczegoly=True)
    except ValueError:
        if not g:
            raise
    except Exception:
        osm = None
    if g:
        g.update(rozbior=r, osm=osm if osm and _numer_rowny((osm.get("address") or {}).get("house_number"), r["numer"]) else None)
        return g
    hn = (osm.get("address") or {}).get("house_number")
    dokl = "budynek" if r["numer"] and _numer_rowny(hn, r["numer"]) else "przyblizona"
    a = osm.get("address") or {}
    return {"lon": float(osm["lon"]), "lat": float(osm["lat"]), "dokladnosc": dokl, "zrodlo": "OpenStreetMap (dane otwarte)", "adres_pelny": osm.get("display_name", ""),
            "miejscowosc": a.get("city") or a.get("town") or a.get("village") or "", "dzielnica": a.get("suburb") or a.get("quarter") or "",
            "rozbior": r, "osm": osm if dokl == "budynek" else None,
            "ostrzezenie": "" if dokl == "budynek" else (f"Nie znaleziono budynku nr {r['numer']} – trafiono tylko w {('ulicę ' + str(a.get('road'))) if a.get('road') else 'miejscowość'}. "
                                                           "Działka pod tym punktem może być drogą lub sąsiednią nieruchomością – sprawdź i podaj obręb i numer działki.")
            if r["numer"] else "Adres bez numeru budynku – lokalizacja przybliżona."}


def budynek_z_ewidencji(x, y, srid=2180):
    """Budynek z ewidencji (ULDK GetBuildingByXY, układ 2180): identyfikator i powierzchnia zabudowy z obrysu."""
    try:
        url = ULDK + "?" + urllib.parse.urlencode({"request": "GetBuildingByXY", "xy": f"{x},{y},{srid}", "result": "id,geom_wkt", "srid": "2180"})
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Bidivia/1.0"}), timeout=20) as r:
            t = r.read().decode("utf-8", "ignore").strip().splitlines()
        if len(t) < 2 or t[0].strip() != "0" or "|" not in t[1]:  # 0 = znaleziono, -1 = brak budynku w punkcie
            return {}
        cz = t[1].split("|")
        geom = cz[-1].split(";", 1)[-1]
        return {"id_budynku": cz[0], "pow_zabudowy": round(pole(wkt_punkty(geom)), 1) if geom.startswith("POLYGON") or geom.startswith("MULTIPOLYGON") else None}
    except Exception:
        return {}


def budynek_z_adresu(lok):
    """Dane budynku: z ewidencji (identyfikator, powierzchnia zabudowy) i z otwartych danych mapowych tam, gdzie są (kondygnacje, rok budowy, funkcja).
    Dane mapowe tylko przy trafieniu w budynek – nigdy z ulicy czy miejscowości. Wszystko do potwierdzenia dokumentami."""
    lok = lok or {}
    b = {"adres_pelny": lok.get("adres_pelny", ""), "miejscowosc": lok.get("miejscowosc", ""), "dzielnica": lok.get("dzielnica", ""),
         "dokladnosc": lok.get("dokladnosc", "przyblizona"), "zrodlo": lok.get("zrodlo", "")}
    if lok.get("ostrzezenie"):
        b["ostrzezenie"] = lok["ostrzezenie"]
    osm = lok.get("osm") or {}
    t = osm.get("extratags") or {}
    if t.get("building:levels"):
        b["kondygnacje_budynku"] = t["building:levels"]
    for k in ("start_date", "building:year", "construction_date"):
        if t.get(k) and re.search(r"\d{4}", str(t[k])):
            b["rok_budowy"] = re.search(r"\d{4}", str(t[k])).group(0)
            break
    fun = t.get("building") if t.get("building") not in (None, "yes") else (osm.get("type") if osm.get("class") == "building" and osm.get("type") != "yes" else "")
    if fun:
        b["funkcja"] = fun
    if any(k in b for k in ("kondygnacje_budynku", "rok_budowy", "funkcja")):
        b["zrodlo"] += " + OpenStreetMap (kondygnacje / rok / funkcja – do potwierdzenia)"
    return b


# ---------------------------------------------------------------- plan miejscowy: przeznaczenie terenu (art. 154 UGN)
KIMP = "https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaMiejscowychPlanowZagospodarowaniaPrzestrzennego"  # stary adres integracja.gugik.gov.pl przekierowuje tutaj
POG = "https://mapy.geoportal.gov.pl/wss/ext/PlanyOgolneGmin"
RE_SYMBOL = re.compile(r"(?<![A-Za-z0-9])(\d{0,3}\.?(?:MW|MN|MU|ML|M|UC|UP|US|UT|UK|U|PU|P|RM|RU|R|ZL|ZP|ZN|ZC|Z|KDGP|KDG|KDZ|KDL|KDD|KDW|KD|KS|KK|WS|W|E|K|G|IT|T)(?:/[A-Z]{1,3})?\d{0,3})(?![A-Za-z0-9])")
GRUPY_PRZEZNACZENIA = [
    ("MW", "zabudowa mieszkaniowa wielorodzinna", "budowlana"), ("MN", "zabudowa mieszkaniowa jednorodzinna", "budowlana"),
    ("MU", "zabudowa mieszkaniowo-usługowa", "budowlana"), ("ML", "zabudowa letniskowa", "budowlana"), ("M", "zabudowa mieszkaniowa", "budowlana"),
    ("PU", "tereny produkcyjno-usługowe", "budowlana"), ("U", "zabudowa usługowa", "budowlana"), ("P", "tereny produkcyjne, składy, magazyny", "budowlana"),
    ("RM", "zabudowa zagrodowa", "rolna"), ("RU", "obsługa produkcji rolnej", "rolna"), ("R", "tereny rolnicze", "rolna"), ("ZL", "lasy", "rolna"),
    ("ZP", "zieleń urządzona", None), ("ZN", "zieleń nieurządzona", None), ("ZC", "cmentarze", None), ("Z", "zieleń", None),
    ("KD", "drogi publiczne", None), ("KS", "obsługa komunikacji", None), ("KK", "tereny kolejowe", None), ("WS", "wody powierzchniowe", None),
    ("W", "infrastruktura – wodociągi", None), ("E", "infrastruktura – elektroenergetyka", None), ("K", "infrastruktura – kanalizacja", None),
    ("G", "infrastruktura – gaz", None), ("IT", "infrastruktura techniczna", None), ("T", "infrastruktura – telekomunikacja", None)]


def symbole_z_tekstu(tekst):
    """Symbole terenów z tekstu – bez przypadkowych pojedynczych liter (pojedyncza litera tylko z numerem, np. 1U, 2R)."""
    wyn = []
    for m in RE_SYMBOL.finditer(tekst or ""):
        s_ = m.group(1)
        litery = re.sub(r"[^A-Z]", "", s_)
        if (re.match(r"^\d", s_) or len(litery) >= 2) and s_ not in wyn:
            wyn.append(s_)
    return wyn


def grupa_symbolu(symbol):
    rdz = re.sub(r"^[\d.]+", "", str(symbol or "").upper())
    for pref, nazwa, typ in GRUPY_PRZEZNACZENIA:
        if rdz.startswith(pref):
            return {"symbol": symbol, "prefiks": pref, "grupa": nazwa, "typ": typ}
    return {"symbol": symbol, "prefiks": "", "grupa": "nieustalone", "typ": None}


def _srodek(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) if pts else None


def _gfi(baza, warstwy, x, y, timeout=20):
    """GetFeatureInfo w punkcie (x = wschód, y = północ w PL-1992; WMS 1.1.1 – kolejność osi jak w układzie)."""
    d = 25
    q = {"SERVICE": "WMS", "VERSION": "1.1.1", "REQUEST": "GetFeatureInfo", "LAYERS": warstwy, "QUERY_LAYERS": warstwy, "STYLES": "", "SRS": "EPSG:2180",
         "BBOX": f"{x - d},{y - d},{x + d},{y + d}", "WIDTH": 101, "HEIGHT": 101, "X": 50, "Y": 50, "INFO_FORMAT": "text/plain", "FEATURE_COUNT": 10}
    with urllib.request.urlopen(urllib.request.Request(baza + "?" + urllib.parse.urlencode(q), headers={"User-Agent": "Bidivia/1.0"}), timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def rekordy_gfi(t):
    """Odpowiedzi gmin mają różne formaty: „klucz = wartość” (GeoServer), XML z wierszami <ROW>, tabela HTML. → lista słowników."""
    t = re.sub(r"(?is)<(style|script)[^>]*>.*?</\1>", " ", t or "")
    rek = []
    if re.search(r"(?i)<ROW\b", t):
        for row in re.findall(r"(?is)<ROW\b[^>]*>(.*?)</ROW>", t):
            rek.append({k.lower(): html_txt(v) for k, v in re.findall(r"(?is)<([A-Za-z_][\w.-]*)>(.*?)</\1>", row)})
    elif re.search(r"(?i)<t[hd]\b", t):
        for tab in re.findall(r"(?is)<table\b.*?</table>", t):
            wiersze = re.findall(r"(?is)<tr\b.*?</tr>", tab)
            nag = [html_txt(x).lower() for x in re.findall(r"(?is)<th\b[^>]*>(.*?)</th>", wiersze[0])] if wiersze else []
            for w in wiersze[1:]:
                kom = [html_txt(x) for x in re.findall(r"(?is)<td\b[^>]*>(.*?)</td>", w)]
                if nag and len(kom) == len(nag):
                    rek.append(dict(zip(nag, kom)))
    else:
        for blok in re.split(r"(?m)^-{6,}\s*$|Results for FeatureType", t):
            r_, klucz = {}, None
            for l in blok.splitlines():
                m = re.match(r"^\s*([A-Za-z_][\w.:-]*)\s*=\s*(.*)$", l)
                if m:
                    klucz = m.group(1).lower()
                    r_[klucz] = m.group(2).strip()
                elif klucz and l.strip():
                    r_[klucz] += " " + l.strip()
            if r_:
                rek.append(r_)
    return [{k: v for k, v in r_.items() if v not in ("", "null", "None")} for r_ in rek if r_]


def html_txt(v):
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", str(v or "")))).strip()


def _pierwsze_pole(r_, *klucze):
    for k in klucze:
        for kk, v in r_.items():
            if kk == k or kk.endswith("." + k):
                return v
    return ""


def plan_z_geoportalu(pts, timeout=20):
    """Plan miejscowy w środku działki z krajowej integracji planów (rejestr aktów planowania) + plan ogólny gminy, jeśli już jest.
    Zwraca: symbole i przeznaczenia (plany wektorowe), dane uchwały (tytuł, numer i data, obowiązuje od, status) i linki – albo None."""
    c = _srodek(pts)
    if not c:
        return None
    rek, komunikaty = [], []
    for warstwy in ("plany_granice", "wektor-str"):
        try:
            t = _gfi(KIMP, warstwy, c[0], c[1], timeout)
        except Exception as e:
            komunikaty.append(f"{warstwy}: {e}")
            continue
        if re.search(r"(?i)brak wyniku|no results|returned no", t) and not re.search(r"=|<ROW", t):
            komunikaty.append(html_txt(t)[:160])
        rek += rekordy_gfi(t)
    plany, symbole, przezn = [], [], {}
    for r_ in rek:
        sym = _pierwsze_pole(r_, "fun_symb", "symbol", "oznaczenie", "symbol_przeznaczenia", "przeznaczenie_symbol")
        if sym:
            for s_ in [x.strip() for x in re.split(r"[,;]", sym) if x.strip()]:
                if s_ not in symbole:
                    symbole.append(s_)
                przezn.setdefault(s_, _pierwsze_pole(r_, "fun_nazwa", "przeznaczenie", "nazwa_przeznaczenia", "opis"))
        tyt = _pierwsze_pole(r_, "tytul", "nazwa_plan", "name", "nazwa_planu")
        uch = _pierwsze_pole(r_, "dokumentuchwalajacy", "uchwala", "nr_uchwaly", "numer_uchwaly")
        if tyt or uch:
            pl = {"tytul": tyt, "uchwala": re.sub(r"\s+", " ", uch)[:300], "obowiazuje_od": _pierwsze_pole(r_, "obowiazujeod", "data_wejscia", "data_uchwalenia")[:10],
                  "status": _pierwsze_pole(r_, "status", "state"), "zmieniajacy": _pierwsze_pole(r_, "dokumentzmieniajacy"),
                  "linki": [v for k, v in r_.items() if re.match(r"https?://", v) and k in ("xlinkhref", "rysunek_lacze", "lacze_gml", "dokument", "www", "url", "link")]}
            if not any(p_["tytul"] == pl["tytul"] and p_["uchwala"] == pl["uchwala"] for p_ in plany):
                plany.append(pl)
    pog = None
    try:
        rp = rekordy_gfi(_gfi(POG, "strefaPlanistyczna,aktPlanowaniaprzestrzennego", c[0], c[1], timeout))
        if rp:
            pog = {"strefa": " ".join(filter(None, (_pierwsze_pole(r_, "symbol", "oznaczenie", "profilstrefy", "nazwa") for r_ in rp)))[:200],
                   "akt": next((_pierwsze_pole(r_, "tytul", "dokumentuchwalajacy") for r_ in rp if _pierwsze_pole(r_, "tytul", "dokumentuchwalajacy")), "")[:300]}
    except Exception:
        pass
    if not plany and not symbole:
        return {"brak": True, "komunikat": "; ".join(komunikaty)[:300], "pog": pog} if (komunikaty or pog) else None
    gl = plany[0] if plany else {}
    return {"symbole": symbole[:8], "przeznaczenia": przezn, "plany": plany[:4], "uchwala": gl.get("uchwala") or "", "tytul": gl.get("tytul") or "",
            "obowiazuje_od": gl.get("obowiazuje_od", ""), "linki": list(dict.fromkeys(u for p_ in plany for u in p_["linki"]))[:8], "pog": pog,
            "tekst": "; ".join(f"{k} = {v}" for r_ in rek for k, v in r_.items() if k != "geom")[:1500],
            "zrodlo": "geoportal – krajowa integracja miejscowych planów (rejestr aktów planowania)"}


def numer_uchwaly(t):
    """„Uchwała Nr 63/VIII/07 Rady…” → „63/VIII/07” (do porównania numerów z różnych źródeł)."""
    m = re.search(r"(?i)(?:nr|numer)\.?\s*([0-9IVXLC]+(?:\s*/\s*[0-9IVXLC]+){1,3})", str(t or ""))
    return re.sub(r"\s+", "", m.group(1)).upper() if m else ""


def polecenie_planu(n, wstepne):
    i, d = n.get("identyfikacja") or {}, n.get("dane") or {}
    return (f"Nieruchomość: {opis_dzialek(n)}, adres {d.get('adres') or ''}. Dane z geoportalu (dla każdej działki): {json.dumps(wstepne or {}, ensure_ascii=False)[:2000]}.\n"
            "Ustal w internecie (BIP gminy, dziennik urzędowy województwa, geoportal gminy): czy dla działki obowiązuje miejscowy plan zagospodarowania przestrzennego, "
            "numer i datę uchwały, symbol terenu działki i jego przeznaczenie oraz ustalenia dla tego symbolu. Gdy planu nie ma – plan ogólny lub studium. "
            'Zwróć WYŁĄCZNIE JSON: {"jest_plan": true/false/null, "uchwala": "nr i data", "data_uchwalenia": "RRRR-MM-DD lub null", "symbol": "np. 2MN", '
            '"przeznaczenie": "…", "url_tekstu": "https://… (PDF / strona z tekstem uchwały) lub pusty", "parametry": {"pow_zab_pct": null, "intensywnosc_min": null, '
            '"intensywnosc_max": null, "wysokosc_m": null, "kondygnacje": null, "pbc_pct": null, "parking_na_lokal": null}, "paragraf": "§ … dla symbolu", '
            '"inne_ustalenia": ["linie zabudowy, strefy, ograniczenia"], "bez_planu": "studium / plan ogólny – jeśli brak planu", "zrodla": ["https://…"]}')


def polecenie_uchwaly(symbol, n):
    return (f"To tekst uchwały w sprawie miejscowego planu. Działka: {(n.get('identyfikacja') or {}).get('teryt') or ''}, symbol terenu: {symbol or 'ustal z tekstu'}. "
            "Odczytaj ustalenia DLA TEGO SYMBOLU (i ustalenia ogólne, które go dotyczą). "
            'Zwróć WYŁĄCZNIE JSON: {"symbol": "…", "przeznaczenie": "…", "parametry": {"pow_zab_pct": null, "intensywnosc_min": null, "intensywnosc_max": null, '
            '"wysokosc_m": null, "kondygnacje": null, "pbc_pct": null, "parking_na_lokal": null}, "paragraf": "§ …", "cytat": "dosłowny fragment 20–300 znaków", '
            '"inne_ustalenia": ["…"], "data_uchwalenia": "RRRR-MM-DD lub null"}')


def polecenie_dokumentu_planu(n, symbol_hint):
    i = n.get("identyfikacja") or {}
    return (f"Nieruchomość: {opis_dzialek(n)} (identyfikator {i.get('teryt') or ''}). Symbol terenu podany przez użytkownika: {symbol_hint or 'brak'}.\n"
            "Dokumenty powyżej dotyczą miejscowego planu zagospodarowania przestrzennego (tekst uchwały, rysunek planu, wypis i wyrys albo strona z planem).\n"
            "1) Jeśli to WYPIS z planu – podaje przeznaczenie działki wprost: wpisz symbol i przeznaczenie działki.\n"
            "2) Jeśli to tekst uchwały lub rysunek – ustal symbol terenu działki tylko wtedy, gdy wynika z dokumentu (np. numer działki w tekście, opis położenia, rysunek z numerami działek) "
            "albo użytkownik go podał. Nie zgaduj – gdy nie da się ustalić, symbol_dzialki = null.\n"
            "3) Zawsze wypisz WSZYSTKIE tereny z planu (symbol, przeznaczenie, kluczowe parametry), żeby użytkownik mógł wybrać symbol działki.\n"
            'Zwróć WYŁĄCZNIE JSON: {"rodzaj_dokumentu": "wypis | uchwała | rysunek | inny", "uchwala": "nr i data", "data_uchwalenia": "RRRR-MM-DD lub null", '
            '"symbol_dzialki": "np. 2MN lub null", "uzasadnienie_symbolu": "skąd wiadomo", "udzialy": {"symbol": "część działki, jeśli dokument podaje"}, '
            '"tereny": [{"symbol": "…", "przeznaczenie": "…", "parametry": {"pow_zab_pct": null, "intensywnosc_min": null, "intensywnosc_max": null, "wysokosc_m": null, '
            '"kondygnacje": null, "pbc_pct": null, "parking_na_lokal": null}, "paragraf": "§ …", "inne_ustalenia": ["…"]}]} – maksymalnie 60 terenów.')


def plan_z_terenu(teren, uchwala="", data_uchwalenia=None):
    """Plan teczki z wybranego terenu (symbolu) dokumentu planu."""
    return {"jest_plan": True, "symbol": teren.get("symbol"), "symbole": [teren.get("symbol")], "przeznaczenie": teren.get("przeznaczenie"),
            "parametry": teren.get("parametry") or {}, "paragraf": teren.get("paragraf"), "inne_ustalenia": teren.get("inne_ustalenia") or [],
            "uchwala": uchwala, "data_uchwalenia": data_uchwalenia}


def ryzyka_z_planu(plan, cel, typ):
    """Ryzyka DD z przeznaczenia w planie: droga na działce, przeznaczenie niezgodne z celem, opłata planistyczna, brak planu."""
    R = []
    sym = [grupa_symbolu(x) for x in plan.get("symbole") or ([plan["symbol"]] if plan.get("symbol") else [])]
    if any(g["prefiks"].startswith("KD") for g in sym) and len(sym) > 1:
        R.append(("plan", "Część działki w planie przeznaczona pod drogę publiczną (" + ", ".join(g["symbol"] for g in sym if g["prefiks"].startswith("KD")) + ") – ryzyko przejęcia pod drogę i mniejszej powierzchni do zabudowy",
                  "czerwone", "Obniżka ceny o część drogową albo odszkodowanie od gminy"))
    gl = next((g for g in sym if not g["prefiks"].startswith("KD")), sym[0] if sym else None)
    if gl and cel and re.search(r"(?i)dom|mieszka|budow", cel) and gl["typ"] != "budowlana":
        R.append(("plan", f"Przeznaczenie w planie ({gl['symbol']} – {gl['grupa']}) nie pozwala na zabudowę zgodną z celem zakupu", "czerwone", "Warunek: zmiana planu albo odstąpienie"))
    if plan.get("data_uchwalenia"):
        try:
            if (dt.date.today() - dt.date.fromisoformat(plan["data_uchwalenia"][:10])).days < 5 * 365:
                R.append(("podatki", "Plan uchwalony w ciągu ostatnich 5 lat – przy sprzedaży możliwa opłata planistyczna po stronie sprzedającego",
                          "zielone", "Oświadczenie sprzedającego o rozliczeniu opłaty planistycznej"))
        except ValueError:
            pass
    if plan.get("jest_plan") is False:
        R.append(("plan", "Brak planu miejscowego – zabudowa wymaga decyzji o warunkach zabudowy (po reformie tylko w wyznaczonych obszarach planu ogólnego)",
                  "zolte", "Warunek: uzyskanie decyzji o warunkach zabudowy przed zakupem"))
    return R


# ---------------------------------------------------------------- geometria (PUWG 1992, metry)
def wkt_punkty(wkt):
    m = re.search(r"\(\(([^()]+)\)", wkt or "")
    if not m:
        return []
    pts = []
    for para in m.group(1).split(","):
        xy = para.split()
        if len(xy) >= 2:
            pts.append((float(xy[0]), float(xy[1])))
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    return pts


def pole(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2 if len(pts) > 2 else 0.0


def _znak(pts):
    return 1 if sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) > 0 else -1


def wciecie(pts, d):
    """Wielokąt odsunięty do środka o d metrów (odległość od granic) – przybliżenie dla działek o prostym kształcie."""
    n = len(pts)
    if n < 3 or d <= 0:
        return list(pts)
    s = _znak(pts)
    linie = []
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = (-dy / L, dx / L) if s > 0 else (dy / L, -dx / L)  # normalna do środka
        linie.append(((x1 + nx * d, y1 + ny * d), (x2 + nx * d, y2 + ny * d)))
    wyn = []
    for i in range(n):
        (a1, a2), (b1, b2) = linie[i - 1], linie[i]
        x1, y1 = a1
        x2, y2 = a2
        x3, y3 = b1
        x4, y4 = b2
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-9:
            wyn.append(b1)
            continue
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        wyn.append((px, py))
    if len(wyn) < 3 or _znak(wyn) != s or pole(wyn) <= 0 or pole(wyn) >= pole(pts):
        return []
    return wyn


# ---------------------------------------------------------------- kilka działek w jednej nieruchomości
def dzialki(n):
    """Lista działek teczki (zgodność wstecz: jedna działka z identyfikacji)."""
    L = n.get("dzialki") or []
    if not L and (n.get("identyfikacja") or {}).get("teryt"):
        L = [dict(n["identyfikacja"], id="d1")]
    return L


def opis_dzialek(n):
    L = dzialki(n)
    if not L:
        d = n.get("dane") or {}
        return f"działka nr {d.get('nr_dzialki') or '[UZUPEŁNIJ]'}, obręb {d.get('obreb') or '[UZUPEŁNIJ]'}, gmina {d.get('gmina') or '[UZUPEŁNIJ]'}"
    grupy = {}
    for x in L:
        grupy.setdefault((x.get("obreb") or "", x.get("gmina") or ""), []).append(x.get("numer") or x.get("teryt") or "?")
    cz = []
    for (ob, gm), nr in grupy.items():
        cz.append(("działki nr " + ", ".join(nr[:-1]) + " i " + nr[-1] if len(nr) > 1 else f"działka nr {nr[0]}") + f", obręb {ob}, gmina {gm}")
    kw = sorted({x.get("kw") for x in L if x.get("kw")})
    return "; ".join(cz) + (f" (KW: {', '.join(kw)})" if kw else "")


def _odl_punkt_odcinek(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2)) if L2 else 0.0
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def sasiaduja(A, B, tol=0.5):
    """Czy działki stykają się granicą (wierzchołek jednej leży na granicy drugiej, z tolerancją w metrach)."""
    if not A or not B:
        return False
    for P, Q in ((A, B), (B, A)):
        for p in P:
            for i in range(len(Q)):
                if _odl_punkt_odcinek(p, Q[i], Q[(i + 1) % len(Q)]) <= tol:
                    return True
    return False


def grupy_sasiednich(polys):
    """Podział działek na grupy sąsiadujące ze sobą (spójne składowe)."""
    n = len(polys)
    rodzic = list(range(n))

    def f(i):
        while rodzic[i] != i:
            rodzic[i] = rodzic[rodzic[i]]
            i = rodzic[i]
        return i
    for i in range(n):
        for k in range(i + 1, n):
            if sasiaduja(polys[i], polys[k]):
                rodzic[f(i)] = f(k)
    g = {}
    for i in range(n):
        g.setdefault(f(i), []).append(i)
    return list(g.values())


def polacz(polys):
    """Połączenie sąsiednich działek w jeden obrys: usunięcie wspólnych krawędzi (granice z ewidencji mają wspólne wierzchołki).
    Zwraca jeden wielokąt albo None, gdy się nie da (wtedy obszar zabudowy liczony osobno dla każdej działki)."""
    if len(polys) == 1:
        return polys[0]
    kl = lambda p: (round(p[0], 2), round(p[1], 2))
    licz, kraw = {}, []
    for P in polys:
        for i in range(len(P)):
            a, b = kl(P[i]), kl(P[(i + 1) % len(P)])
            if a == b:
                continue
            kraw.append((a, b))
            licz[frozenset((a, b))] = licz.get(frozenset((a, b)), 0) + 1
    zewn = [(a, b) for a, b in kraw if licz[frozenset((a, b))] == 1]
    if not zewn or len(zewn) == len(kraw):
        return None
    nast = {}
    for a, b in zewn:
        if a in nast:
            return None  # rozgałęzienie – obrys niejednoznaczny
        nast[a] = b
    start = zewn[0][0]
    ring, p = [start], nast.get(start)
    while p is not None and p != start and len(ring) <= len(zewn):
        ring.append(p)
        p = nast.get(p)
    if p != start or len(ring) != len(zewn):
        return None  # więcej niż jeden obrys (np. otwór) – bez łączenia
    return ring


def geometria_teczki(n):
    """Wielokąty działek, obrys połączony (gdy sąsiadują) i uwagi: różne księgi, działki niesąsiadujące."""
    L = dzialki(n)
    polys = [wkt_punkty(x.get("geom")) for x in L]
    polys = [p for p in polys if len(p) >= 3]
    uwagi = []
    kw = {x.get("kw") for x in L if x.get("kw")}
    if len(kw) > 1:
        uwagi.append(f"Działki mają różne księgi wieczyste ({', '.join(sorted(kw))}) – sprawdź, czy to jedna nieruchomość w rozumieniu wyceny.")
    grupy = grupy_sasiednich(polys) if len(polys) > 1 else [[0]] if polys else []
    if len(grupy) > 1:
        uwagi.append(f"Działki tworzą {len(grupy)} osobne części (nie stykają się) – obszar zabudowy liczony osobno dla każdej części.")
    czesci = []
    for g in grupy:
        pg = polacz([polys[i] for i in g])
        if pg:
            czesci.append(pg)
        else:
            czesci += [polys[i] for i in g]
            if len(g) > 1:
                uwagi.append("Nie udało się połączyć granic sąsiednich działek – obszar zabudowy liczony osobno dla każdej działki (zaniżony przy wspólnych granicach).")
    return {"polys": polys, "czesci": czesci, "uwagi": uwagi, "pow_suma": round(sum(_f(x.get("pow_ewid")) for x in L), 1)}


def svg_dzialki(pts, wew=None, w=320, h=240, wiele=None, etykiety=None):
    """Rysunek działki (albo kilku działek – wiele) i obszaru zabudowy (wew – jeden albo lista wielokątów)."""
    if wiele:
        wsz = [p for P in wiele for p in P]
        if len(wsz) < 3:
            return ""
        xs, ys = [p[0] for p in wsz], [p[1] for p in wsz]
        sx, sy = max(xs) - min(xs) or 1, max(ys) - min(ys) or 1
        k = min((w - 40) / sx, (h - 40) / sy)
        ox, oy = (w - sx * k) / 2, (h - sy * k) / 2
        f = lambda p: (ox + (p[0] - min(xs)) * k, h - oy - (p[1] - min(ys)) * k)
        g = ""
        for i, P in enumerate(wiele):
            g += f'<polygon points="{" ".join("%.1f,%.1f" % f(p) for p in P)}" fill="var(--bdv-tlo, #F4F7FB)" stroke="#071F49" stroke-width="1.5"/>'
        for W in (wew or []):
            if W:
                g += f'<polygon points="{" ".join("%.1f,%.1f" % f(p) for p in W)}" fill="#1F5A99" fill-opacity="0.25" stroke="#1F5A99" stroke-width="1.2" stroke-dasharray="4 3"/>'
        for i, P in enumerate(wiele):
            cx, cy = f((sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)))
            if etykiety and i < len(etykiety):
                g += f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#071F49">{etykiety[i]}</text>'
        return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Działki i obszar zabudowy">{g}</svg>'
    return _svg_jednej(pts, wew, w, h)


def _svg_jednej(pts, wew=None, w=320, h=240):
    """Rysunek działki (granice) i obszaru zabudowy – do podglądu i raportów (oś Y odwrócona)."""
    if len(pts) < 3:
        return ""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sx, sy = max(xs) - min(xs) or 1, max(ys) - min(ys) or 1
    k = min((w - 40) / sx, (h - 40) / sy)
    ox, oy = (w - sx * k) / 2, (h - sy * k) / 2
    f = lambda p: f"{ox + (p[0] - min(xs)) * k:.1f},{h - oy - (p[1] - min(ys)) * k:.1f}"
    g = f'<polygon points="{" ".join(f(p) for p in pts)}" fill="var(--bdv-tlo, #F4F7FB)" stroke="#071F49" stroke-width="1.5"/>'
    if wew:
        g += f'<polygon points="{" ".join(f(p) for p in wew)}" fill="#1F5A99" fill-opacity="0.25" stroke="#1F5A99" stroke-width="1.2" stroke-dasharray="4 3"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Działka i obszar zabudowy">{g}</svg>'


# ---------------------------------------------------------------- analiza zabudowy (chłonność, scenariusze, opłacalność)
PARAM_DOMYSLNE = {"przeznaczenie": "", "pow_zab_pct": 30, "intensywnosc_max": 0.6, "intensywnosc_min": 0, "wysokosc_m": 9, "kondygnacje": 2,
                  "pbc_pct": 50, "odl_granica_m": 4, "parking_na_lokal": 1.5, "pow_lokalu_m2": 55, "zrodlo": "założenia – uzupełnij z planu miejscowego"}
SCENARIUSZE = {  # koszt budowy zł/m² pow. całkowitej i wartość sprzedaży zł/m² PUM – orientacyjne, do zmiany przez użytkownika
    "dom": ("Dom jednorodzinny", 4800, 9000), "blizniak": ("Bliźniak / szeregówka", 4500, 8500),
    "wielorodzinny": ("Budynek wielorodzinny", 5200, 10500), "uslugi": ("Usługi / hala / magazyn", 3200, 6000), "pv": ("Farma fotowoltaiczna", 0, 0)}


def _f(x, d=0.0):
    return liczba(x, d)


def chlonnosc(pow_dzialki, pts, p, ceny=None):
    """Obszar zabudowy (z granic minus odległości), parametry z planu → powierzchnie, lokale, scenariusze z opłacalnością."""
    czesci = pts if pts and isinstance(pts[0], list) else ([pts] if pts else [])
    P = _f(pow_dzialki) or sum(pole(c) for c in czesci)
    wewy = [wciecie(c, _f(p.get("odl_granica_m"), 4)) for c in czesci]
    wew = [x for x in wewy if x]
    obszar = sum(pole(x) for x in wew) if wew else (P * 0.6 if P else 0)  # bez geometrii – przybliżenie
    zab_max = min(obszar, P * _f(p.get("pow_zab_pct"), 30) / 100) if P else 0
    kond = max(1, int(_f(p.get("kondygnacje"), 2)))
    calk = min(zab_max * kond, P * _f(p.get("intensywnosc_max"), 0.6)) if P else 0
    pum = calk * 0.75
    lokale = int(pum // max(20, _f(p.get("pow_lokalu_m2"), 55))) if pum else 0
    pbc_min = P * _f(p.get("pbc_pct"), 0) / 100
    pbc_ok = (P - zab_max) >= pbc_min * 1.15  # zapas na drogi i parkingi
    ceny = ceny or {}
    sc = []
    for k, (naz, koszt0, wart0) in SCENARIUSZE.items():
        koszt_m2, wart_m2 = _f(ceny.get(k + "_koszt"), koszt0), _f(ceny.get(k + "_wartosc"), wart0)
        if k == "pv":
            moc = round(P / 15000, 2)  # ok. 1,5 ha na 1 MWp (orientacyjnie)
            sc.append({"id": k, "nazwa": naz, "wynik": f"ok. {moc} MWp", "koszt": round(moc * 3_200_000), "wartosc": None, "zysk": None, "max_cena": None,
                       "uwaga": "opłacalność z przychodów z energii i warunków przyłączenia – patrz moduł dotacji"})
            continue
        if k == "dom":
            pc, liczba = min(calk, 250.0), 1
        elif k == "blizniak":
            liczba = max(0, min(int(zab_max // 90), int(calk // 160)))
            pc = liczba * 160.0
        elif k == "uslugi":
            pc, liczba = zab_max * 1.0, 1
        else:
            pc, liczba = calk, lokale
        koszt = pc * koszt_m2
        wart = pc * 0.75 * wart_m2 if k != "uslugi" else pc * wart_m2
        zysk_dew = wart * U["marza_pct"] / 100  # oczekiwana marża inwestora (ustawienie)
        max_cena = max(0.0, wart - koszt - zysk_dew - koszt * U["koszty_dod_pct"] / 100)  # koszty dodatkowe (ustawienie)
        sc.append({"id": k, "nazwa": naz, "wynik": f"{round(pc)} m² pow. całkowitej" + (f", {liczba} lokali / segmentów" if k in ("wielorodzinny", "blizniak") else ""),
                   "koszt": round(koszt), "wartosc": round(wart), "zysk": round(wart - koszt), "max_cena": round(max_cena),
                   "koszt_m2": koszt_m2, "wartosc_m2": wart_m2})
    return {"pow_dzialki": round(P, 1), "obszar_zabudowy": round(obszar, 1), "pow_zabudowy_max": round(zab_max, 1), "pow_calkowita_max": round(calk, 1),
            "pum": round(pum, 1), "lokale": lokale, "parking": math.ceil(lokale * _f(p.get("parking_na_lokal"), 1.5)), "pbc_min": round(pbc_min, 1),
            "pbc_ok": pbc_ok, "wew": wew, "geometria": bool(wew), "scenariusze": sc}


# ---------------------------------------------------------------- wycena – podejście porównawcze, metoda korygowania ceny średniej
CECHY = {
    "budowlana": [("Lokalizacja", 30), ("Dostęp do infrastruktury technicznej", 20), ("Kształt i wielkość działki", 15), ("Otoczenie i sąsiedztwo", 15),
                  ("Dostęp do drogi publicznej", 10), ("Warunki geotechniczne / ukształtowanie", 10)],
    "lokal": [("Lokalizacja", 35), ("Standard wykończenia", 20), ("Stan techniczny budynku", 15), ("Położenie w budynku (piętro, ekspozycja)", 15),
              ("Powierzchnia i układ", 15)],
    "dom": [("Lokalizacja", 30), ("Stan techniczny i standard", 25), ("Powierzchnia użytkowa i układ", 15), ("Wielkość i zagospodarowanie działki", 15),
            ("Otoczenie i dojazd", 15)],
    "lokal_uzytkowy": [("Lokalizacja i ruch", 35), ("Funkcja i dostępność (witryna, wejście)", 20), ("Standard i stan", 20), ("Powierzchnia i układ", 15), ("Parking i dojazd", 10)],
    "rolna": [("Klasa bonitacyjna gleb", 35), ("Kształt i wielkość", 20), ("Dojazd", 15), ("Lokalizacja", 15), ("Uzbrojenie / melioracje", 15)],
}
CELE_WYCENY = [  # (cel, sugerowany rodzaj wartości)
    ("sprzedaż / ustalenie ceny transakcyjnej", "wartość rynkowa"), ("zabezpieczenie wierzytelności (kredyt hipoteczny)", "wartość rynkowa"),
    ("podział majątku / sprawa spadkowa / zniesienie współwłasności", "wartość rynkowa"), ("aktualizacja opłaty za użytkowanie wieczyste", "wartość rynkowa"),
    ("odszkodowanie (wywłaszczenie, przejęcie pod drogę)", "wartość rynkowa"), ("opłata adiacencka", "wartość rynkowa"), ("opłata planistyczna", "wartość rynkowa"),
    ("podatek (spadek, darowizna, sprzedaż – na potrzeby urzędu skarbowego)", "wartość rynkowa"), ("sprawozdawczość finansowa (wartość godziwa)", "wartość rynkowa"),
    ("ubezpieczenie nieruchomości", "wartość odtworzeniowa"), ("aport / przekształcenie spółki", "wartość rynkowa"), ("postępowanie sądowe / egzekucyjne", "wartość rynkowa"),
    ("inny cel", "")]
RODZAJE_WARTOSCI = ["wartość rynkowa", "wartość odtworzeniowa", "wartość katastralna", "inna"]
USTAWIENIA_DOMYSLNE = {  # założenia metod – ustawienia rzeczoznawcy (konto), widoczne i zmienialne, z uzasadnieniem w operacie
    "min_transakcji": 12, "korekta_parami": 0.5, "korekta_oferty_pct": 7.0, "zakres_segmentu_pct": 40, "marza_pct": 15, "koszty_dod_pct": 12,
    "koszt_odtw_do_remontu": 4200, "koszt_odtw_przecietny": 5200, "koszt_odtw_wysoki": 6800, "uzasadnienie": ""}
OPISY_USTAWIEN = {"min_transakcji": "Minimalna liczba transakcji – metoda korygowania ceny średniej",
                  "korekta_parami": "Porównywanie parami: korekta za 1 stopień różnicy cechy (× waga × rozpiętość cen)",
                  "korekta_oferty_pct": "Wycena orientacyjna: różnica cena ofertowa → transakcyjna [%]", "zakres_segmentu_pct": "Dobór podobnych transakcji: przedział powierzchni ± [%]",
                  "marza_pct": "Metoda pozostałościowa / analiza zabudowy: zysk inwestora [% wartości]", "koszty_dod_pct": "Koszty dodatkowe (projekt, przyłącza, opłaty) [% kosztu budowy]",
                  "koszt_odtw_do_remontu": "Koszt odtworzenia [zł/m²] – standard do remontu", "koszt_odtw_przecietny": "Koszt odtworzenia [zł/m²] – standard przeciętny",
                  "koszt_odtw_wysoki": "Koszt odtworzenia [zł/m²] – standard wysoki", "uzasadnienie": "Uzasadnienie przyjętych założeń (trafia do operatu)"}
U = dict(USTAWIENIA_DOMYSLNE)


def zastosuj_ustawienia(u):
    """Ustawienia konta rzeczoznawcy → założenia używane w obliczeniach (wywoływane przy każdym zapytaniu)."""
    U.clear()
    U.update(USTAWIENIA_DOMYSLNE)
    for k, v in (u or {}).items():
        if k in USTAWIENIA_DOMYSLNE:
            U[k] = str(v)[:2000] if k == "uzasadnienie" else _f(v, USTAWIENIA_DOMYSLNE[k])
    MIN_METODY["porownawcze"] = int(U["min_transakcji"])
    KOSZT_ODTW.update({"do remontu": U["koszt_odtw_do_remontu"], "przeciętny": U["koszt_odtw_przecietny"], "wysoki": U["koszt_odtw_wysoki"]})


MIN_TRANSAKCJI = 12  # zalecana liczba transakcji dla metody korygowania ceny średniej – do potwierdzenia ze standardami przyjętymi przez rzeczoznawcę
PUNKTY = [("k1", "Zakres i cel wyceny"), ("k2", "Stan prawny i powierzchnie"), ("k3", "Oględziny"), ("k4", "Zbiór transakcji"),
          ("k5", "Podejście i metoda"), ("k6", "Cechy, wagi i obliczenia"), ("k7", "Operat")]
ZALEZNOSCI = {"stan_prawny": ["k2", "k6", "k7"], "ogledziny": ["k3", "k6", "k7"], "transakcje": ["k4", "k6", "k7"], "dane": ["k1", "k2", "k7"]}


def data_transakcji(v):
    """Data transakcji z zapisu RRRR-MM-DD, DD.MM.RRRR, DD/MM/RRRR, DD-MM-RRRR albo RRRR.MM.DD → date; inaczej None (GC-08)."""
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    t = str(v or "").strip()[:10]
    m = re.fullmatch(r"(\d{4})[-./](\d{1,2})[-./](\d{1,2})", t) or re.fullmatch(r"(\d{1,2})[-./](\d{1,2})[-./](\d{4})", t)
    if not m:
        return None
    a, b, c = (int(x) for x in m.groups())
    try:
        return dt.date(a, b, c) if a > 31 else dt.date(c, b, a)
    except ValueError:
        return None


def trend(transakcje, data_wyceny):
    """Trend cen jednostkowych w czasie (regresja liniowa) → miesięczna zmiana % i ceny skorygowane na datę wyceny.
    Transakcje bez czytelnej daty zostają w zbiorze bez korekty w czasie (wcześniej znikały albo dawały błąd 500 – GC-08)."""
    W = [t for t in transakcje if not t.get("wykluczona") and _f(t.get("cena_m2"))]
    T = [t for t in W if data_transakcji(t.get("data"))]
    bez_daty = {t.get("id"): _f(t.get("cena_m2")) for t in W if not data_transakcji(t.get("data"))}
    if len(T) < 4:
        return 0.0, {**{t.get("id"): _f(t.get("cena_m2")) for t in T}, **bez_daty}
    dw = data_transakcji(data_wyceny) or dt.date.today()
    xs = [(dw - data_transakcji(t["data"])).days / 30.44 for t in T]
    ys = [_f(t["cena_m2"]) for t in T]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs) or 1
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx  # zł/m² na miesiąc „wstecz”
    mies = -b / my if my else 0.0  # zmiana miesięczna do przodu
    mies = max(-0.03, min(0.03, mies))  # ograniczenie skrajnych trendów (mała próba)
    return round(mies, 5), {**{t["id"]: round(_f(t["cena_m2"]) * (1 + mies * x), 2) for t, x in zip(T, xs)}, **bez_daty}


def korygowanie_ceny_sredniej(transakcje, cechy, oceny, pow_przedmiotu, data_wyceny):
    """W = P × Cśr × Σki, ki z przedziału [wi·Cmin/Cśr ; wi·Cmax/Cśr] według oceny cechy przedmiotu (1 gorsza – 2 przeciętna – 3 lepsza)."""
    mies, skor = trend(transakcje, data_wyceny)
    ceny = list(skor.values())
    if len(ceny) < 3:
        return {"blad": "Za mało transakcji do obliczeń (co najmniej 3, zalecane " + str(int(U["min_transakcji"])) + ")."}
    cmin, cmax, csr = min(ceny), max(ceny), statistics.mean(ceny)
    suma_w = sum(_f(c.get("waga")) for c in cechy) or 100
    wiersze, sk = [], 0.0
    for c in cechy:
        w = _f(c.get("waga")) / suma_w
        o = int(_f(oceny.get(c["nazwa"]), 2))
        cena_cechy = cmin + (o - 1) / 2 * (cmax - cmin)
        ki = w * cena_cechy / csr
        sk += ki
        wiersze.append({"cecha": c["nazwa"], "waga_pct": round(w * 100, 1), "ocena": o, "wspolczynnik": round(ki, 4)})
    cena_m2 = csr * sk
    P = _f(pow_przedmiotu)
    return {"liczba": len(ceny), "cmin": round(cmin, 2), "cmax": round(cmax, 2), "csr": round(csr, 2), "trend_mies": mies, "suma_k": round(sk, 4),
            "cena_m2": round(cena_m2, 2), "wartosc": round(cena_m2 * P, 2) if P else None, "wartosc_zaokr": round(cena_m2 * P, -2) if P else None,
            "wiersze": wiersze, "ostrzezenie": "" if len(ceny) >= int(U["min_transakcji"]) else
            f"Tylko {len(ceny)} transakcji – metoda korygowania ceny średniej zwykle wymaga ich więcej (ustawienie: {int(U["min_transakcji"])}); rozważ porównywanie parami."}


def porownywanie_parami(transakcje, wybrane, cechy, oceny, oceny_tr, pow_przedmiotu, data_wyceny):
    """Porównywanie parami: cena każdej wybranej transakcji skorygowana o różnice cech (krok oceny × waga × ½ rozpiętości cen),
    wynik = średnia cen skorygowanych. Działa od 3 transakcji."""
    mies, skor = trend(transakcje, data_wyceny)
    if not skor:
        skor = {t["id"]: _f(t.get("cena_m2")) for t in transakcje if not t.get("wykluczona")}
    T = [t for t in transakcje if not t.get("wykluczona") and t["id"] in (wybrane or []) and t["id"] in skor]
    if len(T) < 3:
        return {"blad": "Wybierz co najmniej 3 transakcje najbardziej podobne do przedmiotu wyceny."}
    wsz = list(skor.values())
    rozp = (max(wsz) - min(wsz)) if len(set(wsz)) > 1 else statistics.mean(wsz) * 0.2
    suma_w = sum(_f(c.get("waga")) for c in cechy) or 100
    wiersze = []
    for t in T:
        korekty = []
        c_t = skor[t["id"]]
        for c in cechy:
            w = _f(c.get("waga")) / suma_w
            roz = int(_f(oceny.get(c["nazwa"]), 2)) - int(_f((oceny_tr.get(t["id"]) or {}).get(c["nazwa"]), 2))
            korekty.append(round(roz * w * rozp * U["korekta_parami"], 2))
        wiersze.append({"id": t["id"], "data": t.get("data"), "lokalizacja": t.get("lokalizacja"), "cena_m2": c_t, "korekty": korekty, "skorygowana": round(c_t + sum(korekty), 2)})
    cena_m2 = statistics.mean(x["skorygowana"] for x in wiersze)
    P = _f(pow_przedmiotu)
    return {"metoda": "parami", "liczba": len(T), "trend_mies": mies, "rozpietosc": round(rozp, 2), "cechy": [c["nazwa"] for c in cechy], "wiersze": wiersze,
            "cena_m2": round(cena_m2, 2), "wartosc": round(cena_m2 * P, 2) if P else None, "wartosc_zaokr": round(cena_m2 * P, -2) if P else None}


def dochodowe(p, pow_przedmiotu):
    """Podejście dochodowe, metoda inwestycyjna, kapitalizacja prosta: W = DOR / R; DOR = czynsz × 12 × pow × (1 − pustostany) − koszty operacyjne."""
    P = _f(pow_przedmiotu)
    czynsz = _f(p.get("czynsz_m2"))
    R = _f(p.get("stopa_pct")) / 100
    if not (czynsz and P and R):
        return {"blad": "Podaj czynsz rynkowy za m² miesięcznie, powierzchnię i stopę kapitalizacji."}
    pdb = czynsz * 12 * P
    pustostany = _f(p.get("pustostany_pct"), 5) / 100
    rdb = pdb * (1 - pustostany)
    koszty = _f(p.get("koszty_zl")) or rdb * _f(p.get("koszty_pct"), 15) / 100
    dor = rdb - koszty
    return {"metoda": "dochodowe", "czynsz_m2": czynsz, "pow": P, "pdb": round(pdb, 2), "pustostany_pct": round(pustostany * 100, 1), "rdb": round(rdb, 2), "koszty": round(koszty, 2),
            "dor": round(dor, 2), "stopa_pct": round(R * 100, 2), "wartosc": round(dor / R, 2), "wartosc_zaokr": round(dor / R, -2)}


def pozostalosciowa(zw, scenariusz_id):
    """Metoda pozostałościowa (grunt inwestycyjny): wartość po realizacji − koszty budowy i dodatkowe − zysk inwestora (z analizy zabudowy)."""
    s_ = next((x for x in (zw or {}).get("scenariusze") or [] if x.get("id") == scenariusz_id and x.get("max_cena") is not None), None)
    if not s_:
        return {"blad": "Najpierw przelicz analizę zabudowy i wybierz scenariusz."}
    return {"metoda": "pozostalosciowa", "scenariusz": s_["nazwa"], "wynik_zabudowy": s_["wynik"], "wartosc_po_realizacji": s_["wartosc"], "koszt_budowy": s_["koszt"],
            "koszty_dodatkowe": round(s_["koszt"] * U["koszty_dod_pct"] / 100), "zysk_inwestora": round(s_["wartosc"] * U["marza_pct"] / 100), "wartosc": s_["max_cena"], "wartosc_zaokr": round(s_["max_cena"], -2)}


def wskazniki_gruntow(p):
    """Metoda wskaźników szacunkowych gruntów: W = Σ (powierzchnia klasy [ha] × wskaźnik [dt/ha]) × cena 1 dt (żyta albo drewna) × (1 + korekta).
    Wskaźniki dla klas i cenę wpisuje rzeczoznawca (z przepisów i aktualnego komunikatu) – program ich nie zakłada."""
    cena = _f(p.get("cena_dt"))
    klasy = [k for k in p.get("klasy") or [] if _f(k.get("pow_ha")) and _f(k.get("wskaznik"))]
    if not cena or not klasy:
        return {"blad": "Podaj cenę 1 dt i co najmniej jedną klasę z powierzchnią [ha] i wskaźnikiem [dt/ha]."}
    wiersze = [{"klasa": str(k.get("klasa") or ""), "pow_ha": _f(k["pow_ha"]), "wskaznik": _f(k["wskaznik"]), "wartosc": round(_f(k["pow_ha"]) * _f(k["wskaznik"]) * cena, 2)} for k in klasy]
    suma = sum(x["wartosc"] for x in wiersze)
    kor = _f(p.get("korekta_pct")) / 100
    w = suma * (1 + kor)
    return {"metoda": "wskazniki", "cena_dt": cena, "wiersze": wiersze, "suma": round(suma, 2), "korekta_pct": round(kor * 100, 1), "zrodlo_ceny": str(p.get("zrodlo_ceny") or "")[:200],
            "wartosc": round(w, 2), "wartosc_zaokr": round(w, -2)}


PODEJSCIA = {"porownawcze": "porównawcze – metoda korygowania ceny średniej", "parami": "porównawcze – metoda porównywania parami",
             "kosztowe": "kosztowe – grunt + koszt odtworzenia budynku − zużycie", "dochodowe": "dochodowe – metoda inwestycyjna, kapitalizacja prosta",
             "pozostalosciowa": "mieszane – metoda pozostałościowa (grunt inwestycyjny)",
             "wskazniki": "mieszane – metoda wskaźników szacunkowych gruntów (rolne, leśne)"}
KLUCZ_WYNIKU = {"porownawcze": "wynik", "parami": "parami", "kosztowe": "kosztowe", "dochodowe": "dochodowe", "pozostalosciowa": "pozostalosciowa", "wskazniki": "wskazniki"}
MIN_METODY = {"porownawcze": MIN_TRANSAKCJI, "parami": 3}


def wynik_wyceny(w):
    pod = w.get("podejscie") or "porownawcze"
    return pod, (w.get(KLUCZ_WYNIKU.get(pod, "wynik")) or {})


def wrazliwosc(transakcje, cechy, oceny, pow_przedmiotu, data_wyceny):
    """Jak zmienia się wynik, gdy ocena każdej cechy przesunie się o jeden stopień – które założenia ważą najwięcej."""
    baza = korygowanie_ceny_sredniej(transakcje, cechy, oceny, pow_przedmiotu, data_wyceny)
    if baza.get("blad") or not baza.get("cena_m2"):
        return []
    wyn = []
    for c in cechy:
        o = int(_f(oceny.get(c["nazwa"]), 2))
        for nowa in (o - 1, o + 1):
            if 1 <= nowa <= 3:
                r = korygowanie_ceny_sredniej(transakcje, cechy, dict(oceny, **{c["nazwa"]: nowa}), pow_przedmiotu, data_wyceny)
                wyn.append({"cecha": c["nazwa"], "ocena": nowa, "zmiana_pct": round((r["cena_m2"] / baza["cena_m2"] - 1) * 100, 1)})
    return sorted(wyn, key=lambda x: -abs(x["zmiana_pct"]))[:8]


TRWALOSC = {"murowany": 100, "drewniany": 60, "szkieletowy": 70}
KOSZT_ODTW = {"do remontu": 4200, "przeciętny": 5200, "wysoki": 6800}  # zł/m² pow. użytkowej – orientacyjnie, do zmiany przez rzeczoznawcę


def kosztowe(dane, k):
    """Podejście kosztowe: wartość gruntu + koszt odtworzenia budynku × (1 − zużycie). Zużycie liniowe wg wieku i trwałości, korekta o stan."""
    P_gr, P_b = max(0.0, _f(dane.get("pow_dzialki"))), max(0.0, _f(dane.get("pow_uzytkowa")))  # ujemna powierzchnia nie obniża wartości (GC-08)
    cena_gr = max(0.0, _f(k.get("cena_gruntu_m2")))
    tech = (dane.get("technologia") or "murowany").lower()
    trw = next((v for t, v in TRWALOSC.items() if t in tech), 100)
    rok = int(_f(dane.get("rok_budowy"), 0)) or dt.date.today().year
    wiek = max(0, dt.date.today().year - rok)
    zuz = min(0.9, wiek / trw)
    stan = (dane.get("stan") or "").lower()
    zuz = min(0.9, max(0.0, zuz + (0.1 if "zły" in stan or "remont" in stan else -0.05 if "bardzo dobry" in stan or "nowy" in stan else 0)))
    if _f(k.get("zuzycie_pct")):
        zuz = _f(k["zuzycie_pct"]) / 100
    std = (dane.get("standard") or "przeciętny").lower()
    k_odtw = _f(k.get("koszt_odtw_m2")) or next((v for s_, v in KOSZT_ODTW.items() if s_ in std), KOSZT_ODTW["przeciętny"])
    w_gr = P_gr * cena_gr
    w_b = P_b * k_odtw * (1 - zuz)
    dodatkowe = _f(k.get("budynki_dodatkowe_zl"))
    return {"pow_gruntu": P_gr, "cena_gruntu_m2": cena_gr, "wartosc_gruntu": round(w_gr, 2), "pow_budynku": P_b, "koszt_odtw_m2": k_odtw, "wiek": wiek, "trwalosc": trw,
            "zuzycie_pct": round(zuz * 100, 1), "wartosc_budynku": round(w_b, 2), "dodatkowe": dodatkowe, "wartosc": round(w_gr + w_b + dodatkowe, 2),
            "wartosc_zaokr": round(w_gr + w_b + dodatkowe, -2), "brak_gruntu": not cena_gr}


# ---------------------------------------------------------------- wycena orientacyjna z adresu (ceny ofertowe)
def polecenie_orientacyjnej(n):
    d, b = n.get("dane") or {}, (n.get("identyfikacja") or {}).get("budynek") or {}
    return (f"Znajdź w internecie AKTUALNE oferty sprzedaży nieruchomości podobnych do: {TYPY.get(d.get('typ'), '')} – {d.get('adres') or b.get('adres_pelny', '')} "
            f"(miejscowość {b.get('miejscowosc', '')}, dzielnica {b.get('dzielnica', '')}), powierzchnia {d.get('pow_uzytkowa') or d.get('pow_przedmiotu') or '?'} m², "
            f"pokoje {d.get('pokoje') or '?'}, piętro {d.get('pietro') or '?'}, rok budowy {d.get('rok_budowy') or b.get('rok_budowy') or '?'}, rynek {d.get('rynek') or 'wtórny'}. "
            "Szukaj w tej samej dzielnicy lub najbliższej okolicy, podobna powierzchnia (±30%), typ budynku. Co najmniej 6, najlepiej 10–15 ofert. "
            'Zwróć WYŁĄCZNIE JSON: {"oferty": [{"opis": "ulica / osiedle", "pow": liczba, "cena": liczba, "pokoje": liczba lub null, "pietro": "…", "rok": liczba lub null, '
            '"url": "https://…"}], "srednia_m2_dzielnica": liczba lub null, "zrodla": ["portal / raport"]}. Nie zmyślaj ofert – tylko znalezione.')


def wycena_orientacyjna(oferty, pow_przedmiotu, korekta_pct=None):
    korekta_pct = U["korekta_oferty_pct"] if korekta_pct in (None, "") else korekta_pct
    """Mediana cen ofertowych za m² pomniejszona o korektę oferta → transakcja; przedział z kwartyli."""
    ceny = sorted(_f(o.get("cena")) / _f(o.get("pow")) for o in oferty if _f(o.get("cena")) and _f(o.get("pow")))
    if len(ceny) < 3:
        return {"blad": "Za mało ofert do oszacowania (co najmniej 3)."}
    q = statistics.quantiles(ceny, n=4) if len(ceny) >= 4 else [ceny[0], statistics.median(ceny), ceny[-1]]
    k = 1 - _f(korekta_pct, 7) / 100
    P = _f(pow_przedmiotu)
    med = statistics.median(ceny) * k
    return {"liczba": len(ceny), "mediana_ofert_m2": round(statistics.median(ceny), 2), "korekta_pct": _f(korekta_pct, 7), "cena_m2": round(med, 2),
            "od": round(q[0] * k * P, -3) if P else None, "do": round(q[2] * k * P, -3) if P else None, "wartosc": round(med * P, -3) if P else None}


def import_transakcji(sciezka):
    """Transakcje z pliku Excel / CSV (np. wyciąg z rejestru cen): rozpoznanie kolumn po nagłówkach."""
    import csv
    wiersze = []
    if sciezka.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(sciezka, data_only=True).active
        wiersze = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    else:
        with open(sciezka, encoding="utf-8-sig", errors="ignore") as f:
            tekst = f.read()
        dial = csv.Sniffer().sniff(tekst[:2000], delimiters=";,\t") if tekst else csv.excel
        wiersze = list(csv.reader(tekst.splitlines(), dial))
    if not wiersze:
        return []
    i0 = next((i for i, r in enumerate(wiersze[:15]) if sum(1 for c in r if c and re.search(r"(?i)cena|data|pow", str(c))) >= 2), 0)
    nag = [str(c or "").lower() for c in wiersze[i0]]

    def kol(*wz):
        return next((i for i, n in enumerate(nag) if any(re.search(w, n) for w in wz)), None)
    k_data, k_cena = kol(r"data"), kol(r"cena(?!.*m)", r"cena transakcyjna", r"^cena$", r"wartość")
    k_pow, k_cm2 = kol(r"pow"), kol(r"cena.*m", r"zł/m", r"jednostk")
    k_lok, k_uw = kol(r"adres|lokaliz|obręb|położ|miejsc"), kol(r"uwag|opis")
    k_rodz = next((i for i, n_ in enumerate(nag) if re.search(r"rodzaj|typ", n_) and re.search(r"nieruch|obiekt|lokal|grunt|budyn", n_)), None)
    if k_rodz is None:  # sam „rodzaj” / „typ” – ale nie rodzaj transakcji, prawa, rynku ani umowy
        k_rodz = next((i for i, n_ in enumerate(nag) if re.search(r"rodzaj|typ", n_) and not re.search(r"transakc|praw|rynk|umow|dokument|sprzeda|zbyc", n_)), None)
    k_prz = kol(r"przeznacz|funkcj|mpzp")
    wyn = []
    for r in wiersze[i0 + 1:]:
        if not any(r):
            continue
        g = lambda k: (r[k] if k is not None and k < len(r) else None)
        cena, pw = _f(g(k_cena)), _f(g(k_pow))
        cm2 = _f(g(k_cm2)) or (cena / pw if cena and pw else 0)
        d0 = g(k_data)
        d_ = data_transakcji(d0)
        d = d_.isoformat() if d_ else ""  # „12/03/2025”, „1.8.2025” → RRRR-MM-DD; sam rok / nieczytelna – bez daty (GC-08)
        if not cm2:
            continue
        wyn.append({"id": f"t{len(wyn) + 1}", "data": d, "cena": cena, "pow": pw, "cena_m2": round(cm2, 2), "lokalizacja": str(g(k_lok) or "")[:150],
                    "rodzaj": str(g(k_rodz) or "")[:80], "uwagi": str(g(k_uw) or "")[:200], "przeznaczenie": str(g(k_prz) or "")[:80], "oceny": {}, "wykluczona": False, "powod": ""})
    return wyn


def dobierz_segment(transakcje, typ, pow_przedmiotu, symbol_planu=None, zakres=None):
    zakres = U["zakres_segmentu_pct"] / 100 if zakres is None else zakres
    """Dobór transakcji z tego samego segmentu rynku: rodzaj nieruchomości, przeznaczenie w planie i podobna powierzchnia – pozostałe wykluczone z powodem."""
    P = _f(pow_przedmiotu)
    pref = grupa_symbolu(symbol_planu)["prefiks"] if symbol_planu else ""
    rz = RODZAJ.get(typ, "dzialka")
    wz = {"lokal": r"lokal|mieszk|apartament", "dom": r"(?<!nie)zabudowan|\bdom|budyn|budynkow", "dzialka": r"niezabud|działk|dzialk|grunt(?!.*(?<!nie)zabudowan)"}.get(rz)
    for t in transakcje:
        if t.get("wykluczona"):
            continue
        rodz = (t.get("rodzaj") or "").lower()
        opisuje_rodzaj = bool(re.search(r"lokal|mieszk|grunt|dział|dzialk|budyn|zabud|\bdom|nieruchom|apartament", rodz))
        if wz and rodz and opisuje_rodzaj and not re.search(wz, rodz):
            t.update(wykluczona=True, powod=f"inny rodzaj nieruchomości ({t.get('rodzaj')})")
        elif pref and t.get("przeznaczenie") and _pref_tekstu(t["przeznaczenie"]) not in ("", pref[:1]):
            t.update(wykluczona=True, powod=f"inne przeznaczenie w planie ({t['przeznaczenie']})")
        elif P and _f(t.get("pow")) and not ((1 - zakres) * P <= _f(t["pow"]) <= (1 + zakres) * P):
            t.update(wykluczona=True, powod=f"powierzchnia {t['pow']:g} m² poza przedziałem podobnych (±{int(zakres * 100)}% od {P:g} m²)")
    return transakcje


def _pref_tekstu(t):
    m = RE_SYMBOL.search(str(t).upper())
    return grupa_symbolu(m.group(1))["prefiks"][:1] if m else ""


KATEGORIE_WYKLUCZEN = {"rodzaj": "inny rodzaj nieruchomości", "powierzchnia": "powierzchnia poza przedziałem", "przeznaczenie": "inne przeznaczenie w planie",
                       "nietypowe": "transakcja nietypowa", "odstajace": "cena odstająca", "reczne": "wykluczone ręcznie"}


def kategoria_wykluczenia(t):
    if t.get("reczne"):
        return "reczne"
    p = str(t.get("powod") or "")
    return ("rodzaj" if p.startswith("inny rodzaj") else "powierzchnia" if p.startswith("powierzchnia") else "przeznaczenie" if p.startswith("inne przeznaczenie")
            else "nietypowe" if p.startswith("transakcja nietypowa") else "odstajace" if p.startswith("cena odstająca") else "reczne")


def podsumowanie_wykluczen(transakcje):
    wyn = {}
    for t in transakcje:
        if t.get("wykluczona"):
            k = kategoria_wykluczenia(t)
            wyn[k] = wyn.get(k, 0) + 1
    return wyn


def przywroc_kategorie(transakcje, kategoria):
    ile = 0
    for t in transakcje:
        if t.get("wykluczona") and kategoria_wykluczenia(t) == kategoria:
            t.update(wykluczona=False, powod="", przywrocona=f"przywrócona ({KATEGORIE_WYKLUCZEN.get(kategoria, kategoria)})")
            ile += 1
    return ile


def zastrzezenia_punktu(k, n, w, aktywne):
    """Zatwierdzenie mimo zastrzeżeń wymaga uzasadnienia (trafia do dziennika i do operatu)."""
    pod, wyn = wynik_wyceny(w)
    z = []
    if k == "k4" and pod in MIN_METODY and 3 <= aktywne < MIN_METODY[pod]:
        z.append(f"mniej transakcji ({aktywne}) niż zalecane minimum dla metody ({MIN_METODY[pod]})")
    if k == "k6" and wyn.get("ostrzezenie"):
        z.append(wyn["ostrzezenie"])
    if k == "k7":
        z += [u["opis"] for u in kontrola_operatu(n, w) if u["waga"] == "istotna"]
    return z


def poszerz_rynek(transakcje, zakres=0.6):
    """Poszerzenie rynku: przywrócenie transakcji wykluczonych tylko za powierzchnię, jeśli mieszczą się w szerszym przedziale (rzeczoznawca zatwierdza w punkcie 4)."""
    przywr = 0
    for t in transakcje:
        if t.get("wykluczona") and str(t.get("powod", "")).startswith("powierzchnia"):
            t.update(wykluczona=False, powod="", poszerzenie=f"przywrócona przy poszerzeniu rynku (±{int(zakres * 100)}%)")
            przywr += 1
    return przywr


def odrzuc_nietypowe(transakcje):
    """Wstępne odrzucenie transakcji nietypowych (z uzasadnieniem) – rzeczoznawca zatwierdza albo przywraca w punkcie kontrolnym 4."""
    ceny = [t["cena_m2"] for t in transakcje if t.get("cena_m2")]
    if len(ceny) >= 6:
        q = statistics.quantiles(ceny, n=4)
        iqr = q[2] - q[0]
        lo, hi = q[0] - 1.5 * iqr, q[2] + 1.5 * iqr
    else:
        lo, hi = 0, float("inf")
    for t in transakcje:
        t.setdefault("wykluczona", False)
        t.setdefault("powod", "")
        u = (t.get("uwagi", "") + " " + t.get("rodzaj", "")).lower()
        if re.search(r"spokrewn|rodzin|darowizn|licytac|przetarg|udział|ułamk|zamian", u):
            t.update(wykluczona=True, powod="transakcja nietypowa (" + re.search(r"spokrewn\w*|rodzin\w*|darowizn\w*|licytac\w*|przetarg\w*|udział\w*|ułamk\w*|zamian\w*", u).group(0) + ")")
        elif not (lo <= t["cena_m2"] <= hi):
            t.update(wykluczona=True, powod="cena odstająca od pozostałych (poza zakresem typowych cen)")
    return transakcje


# ---------------------------------------------------------------- polecenia dla AI
SYSTEM = ("Jesteś doświadczonym analitykiem nieruchomości w Polsce (due diligence, planowanie przestrzenne, stan prawny, wycena). "
          "Czytasz dokumenty i wskazujesz konkretne ryzyka z odwołaniem do miejsca w dokumencie. Nie zmyślasz – brak danych = brak. "
          "Odpowiadasz WYŁĄCZNIE JSON-em.")


def polecenie_dokumentow(n):
    return (f"Nieruchomość: {json.dumps(n.get('dane') or {}, ensure_ascii=False)}. Identyfikacja: {json.dumps({k: v for k, v in (n.get('identyfikacja') or {}).items() if k != 'geom'}, ensure_ascii=False)}.\n"
            "Przeanalizuj dokumenty powyżej (odpis księgi wieczystej – dział po dziale, wypis z ewidencji, wypis/wyrys z planu, decyzje, umowy, "
            "odpowiedzi urzędów). Zrób kontrole krzyżowe: powierzchnia i numery działek w KW a w ewidencji, właściciel a sprzedający, przeznaczenie w planie a cel zakupu.\n"
            'Zwróć JSON: {"stan_prawny": {"kw": "nr", "wlasciciele": "…", "forma": "własność | użytkowanie wieczyste | …", "dzialki": "…", "pow_kw_m2": liczba lub null, '
            '"pow_ewid_m2": liczba lub null, "hipoteki": ["…"], "sluzebnosci": ["…"], "roszczenia_ostrzezenia": ["…"], "egzekucje": ["…"], "uwagi": "…"}, '
            '"plan": {"jest_plan": true/false/null, "przeznaczenie": "…", "pow_zab_pct": liczba lub null, "intensywnosc_min": liczba lub null, "intensywnosc_max": liczba lub null, '
            '"wysokosc_m": liczba lub null, "kondygnacje": liczba lub null, "pbc_pct": liczba lub null, "parking_na_lokal": liczba lub null, "inne": "…", "zrodlo": "dokument"}, '
            '"ryzyka": [{"obszar": "prawo | plan | zabytki | sieci | grunt | woda | przyroda | dostep | budynki | podatki | rynek", "opis": "…", '
            '"waga": "czerwone | zolte | zielone", "status": "potwierdzone | do_sprawdzenia", "dokument": "plik", "miejsce": "dział / punkt / §", '
            '"cytat": "dosłowny fragment 15–250 znaków", "koszt_zl": liczba lub null, "zapis_umowy": "proponowany warunek do umowy przedwstępnej"}], '
            '"braki": ["dokument lub informacja do uzyskania"], '
            '"dane_obiektu": {"nr_lokalu": null, "pow_uzytkowa": null, "pokoje": null, "pietro": null, "kondygnacje_budynku": null, "forma_prawa": null, "udzial": null, '
            '"rok_budowy": null, "technologia": null, "ogrzewanie": null, "pow_dzialki": null} (tylko to, co jest w dokumentach)}')


def polecenie_rozpoznania(n):
    i = n.get("identyfikacja") or {}
    return (f"Działka: {i.get('teryt') or ''} (gmina {i.get('gmina') or ''}, obręb {i.get('obreb') or ''}, nr {i.get('numer') or ''}), adres: {(n.get('dane') or {}).get('adres', '')}. "
            f"Typ: {TYPY.get((n.get('dane') or {}).get('typ'), '')}; cel zakupu: {(n.get('dane') or {}).get('cel', '')}.\n"
            "Sprawdź w internecie (strony gminy, BIP, geoportale, rejestry) WSTĘPNIE: czy dla tego obrębu obowiązuje plan miejscowy (nazwa, uchwała, przeznaczenie), "
            "zabytki i strefy ochrony konserwatorskiej, obszary chronione / Natura 2000, zagrożenie powodziowe, tereny górnicze, planowane inwestycje drogowe w sąsiedztwie. "
            "Podawaj tylko to, co znalazłeś, ze źródłem. To raport wstępny – wszystko ma status „do_sprawdzenia”.\n"
            'Zwróć JSON: {"plan": {"jest_plan": true/false/null, "nazwa": "…", "uchwala": "…", "przeznaczenie": "…", "zrodlo_url": "…"}, '
            '"ryzyka": [{"obszar": "…", "opis": "…", "waga": "czerwone | zolte | zielone", "zrodlo_url": "https://…"}], "pisma": ["wypis_mpzp", "wkz", "…"]}')


def polecenie_odpowiedzi(pismo, n):
    return (f"To odpowiedź na pismo „{PISMA.get(pismo.get('rodzaj'), (pismo.get('rodzaj'),))[0]}” dotyczące działki {(n.get('identyfikacja') or {}).get('teryt', '')}. "
            f"Obecne ryzyka: {json.dumps([{k: r.get(k) for k in ('id', 'obszar', 'opis', 'status')} for r in n.get('ryzyka') or []], ensure_ascii=False)[:5000]}.\n"
            "Odczytaj odpowiedź: co potwierdza, co wyklucza, jakie nowe ograniczenia, koszty i terminy.\n"
            'Zwróć JSON: {"streszczenie": "2–3 zdania", "zmiany": [{"id": "id istniejącego ryzyka", "status": "potwierdzone | wykluczone", "uzasadnienie": "…"}], '
            '"nowe_ryzyka": [{"obszar": "…", "opis": "…", "waga": "…", "koszt_zl": liczba lub null, "cytat": "…"}], '
            '"plan": {"przeznaczenie": "…", "pow_zab_pct": null, "intensywnosc_max": null, "wysokosc_m": null, "kondygnacje": null, "pbc_pct": null}}')


def polecenie_operatu(n, w):
    return (f"Przygotuj TEKSTY OPISOWE projektu operatu szacunkowego (wartość rynkowa; podejście i metoda – jak podano niżej) "
            f"dla nieruchomości: {json.dumps(n.get('dane') or {}, ensure_ascii=False)}; stan prawny: {json.dumps(n.get('stan_prawny') or {}, ensure_ascii=False)[:3000]}; "
            f"oględziny: {json.dumps(n.get('ogledziny') or {}, ensure_ascii=False)[:2500]}; plan: {json.dumps((n.get('zabudowa') or {}).get('parametry') or {}, ensure_ascii=False)}; "
            f"cel i zakres: {json.dumps({k: w.get(k) for k in ('cel', 'rodzaj_wartosci', 'data_wyceny', 'stan_na')}, ensure_ascii=False)}; "
            f"podejście: {PODEJSCIA.get(wynik_wyceny(w)[0])}; przeznaczenie: {json.dumps(n.get('plan') or {}, ensure_ascii=False)[:800]}; wynik obliczeń: {json.dumps(wynik_wyceny(w)[1], ensure_ascii=False)[:3000]}; liczba transakcji: {len([t for t in w.get('transakcje') or [] if not t.get('wykluczona')])}.\n"
            "Liczb nie zmieniaj – używaj podanych. Styl formalny operatu. To PROJEKT do zatwierdzenia przez rzeczoznawcę majątkowego.\n"
            'Zwróć JSON: {"opis_nieruchomosci": "…", "stan_prawny": "…", "przeznaczenie": "…", "analiza_rynku": "…", "uzasadnienie_podejscia": "…", '
            '"cechy_opis": "…", "klauzule": ["założenia i ograniczenia"]}')


# ---------------------------------------------------------------- pisma do urzędów i gestorów
PISMA = {
    "wypis_mpzp": ("Wniosek o wypis i wyrys z miejscowego planu zagospodarowania przestrzennego", "Wójt / Burmistrz / Prezydent Miasta",
                   "o wydanie wypisu i wyrysu z miejscowego planu zagospodarowania przestrzennego (a w razie braku planu – zaświadczenia o przeznaczeniu terenu w planie ogólnym / studium)"),
    "wkz": ("Zapytanie do wojewódzkiego konserwatora zabytków", "Wojewódzki Konserwator Zabytków",
            "o informację, czy nieruchomość lub jej otoczenie jest wpisane do rejestru zabytków, gminnej ewidencji zabytków, znajduje się w strefie ochrony konserwatorskiej "
            "lub na obszarze stanowiska archeologicznego, oraz o wymaganiach dotyczących badań archeologicznych i nadzoru przy planowanych robotach"),
    "przylacze_ee": ("Wniosek o określenie warunków przyłączenia do sieci elektroenergetycznej", "Operator Systemu Dystrybucyjnego",
                     "o określenie warunków przyłączenia do sieci elektroenergetycznej (moc przyłączeniowa: [UZUPEŁNIJ] kW) oraz informację o przebiegu linii i strefach ochronnych na działce"),
    "przylacze_wod": ("Wniosek o warunki przyłączenia do sieci wodociągowej i kanalizacyjnej", "Przedsiębiorstwo Wodociągów i Kanalizacji",
                      "o wydanie warunków przyłączenia do sieci wodociągowej i kanalizacji sanitarnej (zapotrzebowanie: [UZUPEŁNIJ] m³/d) oraz informację o przebiegu sieci"),
    "przylacze_gaz": ("Wniosek o warunki przyłączenia do sieci gazowej", "Operator gazociągów dystrybucyjnych",
                      "o określenie warunków przyłączenia do sieci gazowej oraz informację o gazociągach i strefach kontrolowanych na działce"),
    "zjazd": ("Zapytanie o możliwość lokalizacji zjazdu z drogi publicznej", "Zarządca drogi",
              "o informację o możliwości lokalizacji zjazdu z drogi publicznej i warunkach jego wykonania oraz o planowanych inwestycjach drogowych w sąsiedztwie"),
    "pinb": ("Zapytanie o legalność obiektów budowlanych", "Powiatowy Inspektor Nadzoru Budowlanego",
             "o informację o pozwoleniach na budowę, pozwoleniach na użytkowanie i postępowaniach dotyczących obiektów budowlanych na nieruchomości"),
    "wody": ("Zapytanie o urządzenia wodne i melioracje", "Państwowe Gospodarstwo Wodne Wody Polskie",
             "o informację o urządzeniach melioracyjnych, ciekach i ograniczeniach wynikających z przepisów prawa wodnego"),
    "spoldzielnia": ("Wniosek o zaświadczenie od spółdzielni / wspólnoty mieszkaniowej", "Spółdzielnia mieszkaniowa / zarząd wspólnoty",
                     "o wydanie zaświadczenia o przysługującym prawie do lokalu, braku zaległości w opłatach, osobach zameldowanych oraz o podjętych uchwałach "
                     "i planowanych remontach wraz z ich kosztem"),
    "zarzadca": ("Zapytanie do zarządcy budynku o stan techniczny i remonty", "Zarządca nieruchomości",
                 "o informację o stanie technicznym budynku, wynikach przeglądów okresowych, planowanych remontach i ich finansowaniu"),
    "rcn": ("Wniosek o udostępnienie danych z rejestru cen nieruchomości", "Starosta – ośrodek dokumentacji geodezyjnej i kartograficznej",
            "o udostępnienie danych z rejestru cen nieruchomości (ceny transakcyjne, powierzchnia, rodzaj i przeznaczenie, data transakcji) dla nieruchomości podobnych "
            "w obrębie i obrębach sąsiednich za okres ostatnich 24 miesięcy [UZUPEŁNIJ: obręby, rodzaj nieruchomości, okres], w celu sporządzenia operatu szacunkowego"),
    "ewidencja": ("Wniosek o wypis i wyrys z ewidencji gruntów i budynków", "Starosta – ośrodek dokumentacji geodezyjnej i kartograficznej",
                  "o wydanie wypisu i wyrysu z ewidencji gruntów i budynków oraz kopii mapy zasadniczej"),
}


def pismo_docx(sciezka, rodzaj, n, cfg):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    tyt, adresat, tresc = PISMA[rodzaj]
    i, d = n.get("identyfikacja") or {}, n.get("dane") or {}
    doc = MO._doc()
    MO._akapit(doc, f"{d.get('miejscowosc_pisma') or '[miejscowość]'}, {dt.date.today():%d.%m.%Y} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(doc, f"{cfg.get('firma_nazwa') or '[wnioskodawca]'}\n{cfg.get('firma_adres') or ''}")
    MO._akapit(doc, f"{adresat}\n[UZUPEŁNIJ: nazwa i adres urzędu / gestora]", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(doc, tyt.upper(), pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    if RODZAJ.get(d.get("typ")) == "lokal":
        MO._akapit(doc, f"Zwracam się z wnioskiem {tresc} dla lokalu nr {d.get('nr_lokalu') or '[UZUPEŁNIJ]'} w budynku przy {d.get('adres') or '[UZUPEŁNIJ: adres]'}"
                        + (f", księga wieczysta {d['kw']}" if d.get("kw") else "") + (f" (działka pod budynkiem: {i['teryt']})" if i.get("teryt") else "") + ".")
    else:
        L_ = dzialki(n)
        MO._akapit(doc, f"Zwracam się z wnioskiem {tresc} dla nieruchomości: {opis_dzialek(n)}"
                    + (f" (identyfikatory: {', '.join(x['teryt'] for x in L_ if x.get('teryt'))})" if L_ else "") + (f", położona: {d['adres']}" if d.get("adres") else "")
                    + (f", księga wieczysta {d['kw']}" if d.get("kw") else "") + ".")
    MO._akapit(doc, "Informacja jest potrzebna w związku z planowanym nabyciem nieruchomości. Proszę o odpowiedź na adres wnioskodawcy albo elektronicznie.")
    MO._akapit(doc, "Załączniki: mapa z zaznaczeniem nieruchomości; [opłata skarbowa / pełnomocnictwo – jeśli wymagane].", rozmiar=9)
    MO._akapit(doc, "\n\n..........................................\n(podpis)", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    podswietl(doc)
    doc.save(sciezka)


# ---------------------------------------------------------------- oględziny – listy kontrolne
OGLEDZINY = {
    "dzialka": ["Granice i znaki graniczne", "Dojazd i dostęp do drogi", "Ukształtowanie terenu, woda stojąca", "Drzewa i zieleń", "Linie napowietrzne, słupy, studzienki",
                "Ślady zanieczyszczeń, odpady", "Sąsiedztwo i uciążliwości", "Zabudowa na działce"],
    "budynek": ["Konstrukcja – rysy, ugięcia", "Wilgoć i zawilgocenia", "Dach i odwodnienie", "Stolarka okienna i drzwiowa", "Instalacja elektryczna",
                "Instalacja wodno-kanalizacyjna", "Ogrzewanie i ciepła woda", "Azbest i materiały szkodliwe", "Standard wykończenia", "Zgodność z projektem i dokumentacją"],
}


OGLEDZINY["lokal"] = ["Klatka schodowa i części wspólne", "Układ lokalu zgodny z rzutem / dokumentami", "Okna, ekspozycja i nasłonecznienie", "Instalacja elektryczna w lokalu",
                      "Instalacja wodno-kanalizacyjna i gazowa", "Ogrzewanie i wentylacja", "Łazienka i kuchnia", "Ślady zalania, wilgoci, pleśni", "Standard wykończenia",
                      "Balkon / piwnica / komórka / miejsce postojowe", "Hałas i sąsiedztwo", "Stan elewacji i dachu budynku"]


def lista_ogledzin(typ):
    rz = RODZAJ.get(typ, "dzialka")
    if rz == "lokal":
        return OGLEDZINY["lokal"]
    return OGLEDZINY["dzialka"] + (OGLEDZINY["budynek"] if rz == "dom" else [])


# ---------------------------------------------------------------- typowe ryzyka do sprawdzenia według rodzaju (lista kontrolna DD)
RYZYKA_TYPOWE = {
    "lokal": [("prawo", "Forma prawa do lokalu i księga wieczysta (odrębna własność czy spółdzielcze własnościowe prawo; księga lokalu i gruntu)", "Przedstawienie odpisu księgi lub zaświadczenia ze spółdzielni"),
              ("prawo", "Zaległości w opłatach na rzecz wspólnoty / spółdzielni", "Zaświadczenie o braku zaległości na dzień aktu"),
              ("budynki", "Uchwały wspólnoty o remontach i ich koszt, fundusz remontowy, planowane podwyżki", "Oświadczenie sprzedającego o uchwałach i kosztach remontów"),
              ("prawo", "Osoby zameldowane, najemcy, służebność mieszkania – ryzyko eksmisji", "Wymeldowanie i wydanie lokalu w określonym terminie, kara umowna"),
              ("budynki", "Legalność zmian w lokalu (przebudowa, połączenie lokali, zmiana sposobu użytkowania)", "Oświadczenie sprzedającego o legalności zmian"),
              ("podatki", "Lokal wykupiony od gminy z bonifikatą – możliwy zwrot bonifikaty przy sprzedaży przed upływem 5 lat", "Oświadczenie o sposobie nabycia i dacie"),
              ("budynki", "Stan techniczny budynku: przeglądy, instalacje, azbest, wilgoć", "Protokoły przeglądów okresowych budynku")],
    "dom": [("budynki", "Legalność budynku: pozwolenie na budowę i na użytkowanie, samowole, zgodność z projektem", "Przedstawienie pozwoleń i dokumentacji budowy"),
            ("budynki", "Stan techniczny: konstrukcja, dach, wilgoć, instalacje, azbest", "Obniżka ceny o koszt napraw wskazanych w oględzinach"),
            ("prawo", "Osoby zameldowane, najemcy, służebność mieszkania", "Wymeldowanie i wydanie nieruchomości w określonym terminie"),
            ("sieci", "Przyłącza i media: umowy, legalność, szambo / przydomowa oczyszczalnia", "Przedstawienie umów i zgłoszeń przyłączy"),
            ("dostep", "Dostęp do drogi publicznej (bezpośredni czy przez służebność)", "Ustanowienie służebności drogowej przed aktem")],
}


# ---------------------------------------------------------------- rekomendacja i raporty
# ---------------------------------------------------------------- wyróżnianie na żółto: do sprawdzenia lub potwierdzenia przez rzeczoznawcę
def M(x):
    """Oznacz fragment do sprawdzenia – w dokumencie będzie na żółto (znaczniki usuwane przy zapisie)."""
    return f"⟦{x}⟧" if str(x) else ""


LEGENDA = "Tekst wyróżniony na żółto – do sprawdzenia lub potwierdzenia przez rzeczoznawcę (propozycje programu, założenia, dane wstępne, braki)."


def _akapity_wszystkie(doc):
    for p in doc.paragraphs:
        yield p
    for t in doc.tables:
        for w in t.rows:
            for c in w.cells:
                for p in c.paragraphs:
                    yield p


def podswietl(doc, aktywne=True):
    """Fragmenty ⟦…⟧ i [UZUPEŁNIJ…] na żółto (aktywne) albo tylko usunięcie znaczników (wersja do podpisu). Formatowanie akapitu z pierwszego fragmentu."""
    import copy as _copy
    from docx.enum.text import WD_COLOR_INDEX
    from docx.oxml.ns import qn
    licz = 0
    for p in _akapity_wszystkie(doc):
        tekst = "".join(r_.text for r_ in p.runs)
        if "⟦" not in tekst and not (aktywne and "[UZUPEŁNIJ" in tekst):
            continue
        rpr = p.runs[0]._r.find(qn("w:rPr")) if p.runs else None
        bold = p.runs[0].bold if p.runs else None
        for r_ in list(p.runs):
            r_._r.getparent().remove(r_._r)
        for cz in re.split(r"(⟦.*?⟧|\[UZUPEŁNIJ[^\]]*\])", tekst, flags=re.S):
            if not cz:
                continue
            zaznacz = cz.startswith("⟦") or cz.startswith("[UZUPEŁNIJ")
            run = p.add_run(cz.strip("⟦⟧") if cz.startswith("⟦") else cz)
            if rpr is not None:
                run._r.insert(0, _copy.deepcopy(rpr))
            if bold is not None:
                run.bold = bold
            if zaznacz and aktywne:
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                licz += 1
    return licz


def rekomendacja(n):
    R = [r for r in n.get("ryzyka") or [] if r.get("status") != "wykluczone"]
    czerw = [r for r in R if r.get("waga") == "czerwone" and r.get("status") == "potwierdzone"]
    koszt = sum(_f(r.get("koszt_zl")) for r in R)
    cena = _f((n.get("dane") or {}).get("cena"))
    wart = _f(wynik_wyceny(n.get("wycena") or {})[1].get("wartosc_zaokr")) or _f(((n.get("wlasna") or {}).get("wynik") or {}).get("wartosc")) \
        or _f((n.get("orientacyjna") or {}).get("wartosc"))
    maxc = max([s.get("max_cena") or 0 for s in ((n.get("zabudowa") or {}).get("wynik") or {}).get("scenariusze") or []] or [0])
    ref = min([x for x in (wart, maxc) if x] or [0])
    if czerw:
        dec, uz = "odstąpić albo uzależnić zakup od usunięcia ryzyk", f"{len(czerw)} potwierdzone ryzyko(a) krytyczne"
    elif cena and ref and cena > ref - koszt:
        dec, uz = "negocjować cenę", f"cena {MO.zl(cena)} przewyższa wartość / maksymalną cenę ({MO.zl(ref)}) pomniejszoną o koszt ryzyk ({MO.zl(koszt)})"
    elif any(r.get("status") == "do_sprawdzenia" and r.get("waga") == "czerwone" for r in R):
        dec, uz = "wstrzymać decyzję do potwierdzenia ryzyk", "ryzyka krytyczne czekają na odpowiedzi urzędów lub dokumenty"
    elif any(r.get("status") == "do_sprawdzenia" for r in R):
        ile = len([r for r in R if r.get("status") == "do_sprawdzenia"])
        dec, uz = "kupić po wyjaśnieniu punktów do sprawdzenia", f"brak potwierdzonych ryzyk krytycznych; {ile} punktów czeka na dokumenty lub odpowiedzi"
    else:
        dec, uz = "kupić", "brak potwierdzonych ryzyk krytycznych"
    propon = round(max(0, ref - koszt), -3) if ref else None
    return {"decyzja": dec, "uzasadnienie": uz, "koszt_ryzyk": round(koszt), "cena_proponowana": propon, "wartosc": wart or None, "max_cena_zabudowa": maxc or None}


def _naglowek(tyt, n, podtytul=""):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    MO._akapit(d, tyt, pogrub=True, rozmiar=15, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    i, dn = n.get("identyfikacja") or {}, n.get("dane") or {}
    MO._akapit(d, f"{dn.get('nazwa') or ''} – {opis_dzialek(n)}" + (f", {dn['adres']}" if dn.get("adres") else ""), wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"Stan na {dt.date.today():%d.%m.%Y}" + (f" · {podtytul}" if podtytul else ""), rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, M(LEGENDA), kursywa=True, rozmiar=8, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    return d


def raport_dd(sciezka, n):
    d = _naglowek("RAPORT DUE DILIGENCE NIERUCHOMOŚCI", n, "analiza wspierająca decyzję – nie jest opinią prawną ani operatem szacunkowym")
    rk = rekomendacja(n)
    MO._akapit(d, "1. Podsumowanie", pogrub=True)
    nie_potw = any(r_.get("status") == "do_sprawdzenia" for r_ in n.get("ryzyka") or [])
    MO._akapit(d, f"Rekomendacja: {rk['decyzja'].upper()} – {rk['uzasadnienie']}." + (" " + M("Rekomendacja wstępna – część ryzyk czeka na potwierdzenie.") if nie_potw else ""), pogrub=True)
    w_ = n.get("wycena") or {}
    wyc_ok = (w_.get("punkty") or {}).get("k6", {}).get("status") == "zatwierdzony"
    wart_opis = (MO.zl(rk["wartosc"]) if wyc_ok else M(MO.zl(rk["wartosc"]) + (" – wycena niezatwierdzona" if wynik_wyceny(w_)[1].get("wartosc") else " – orientacyjna z ofert"))) if rk["wartosc"] else "nie wyceniano"
    MO._tabela(d, [["Element", "Wartość"], ["Cena wywoławcza", MO.zl(_f((n.get('dane') or {}).get('cena'))) if (n.get('dane') or {}).get('cena') else "–"],
                   ["Wartość rynkowa (wycena)", wart_opis],
                   ["Maksymalna cena z analizy zabudowy", M(MO.zl(rk["max_cena_zabudowa"]) + " – szacunek z założeń") if rk["max_cena_zabudowa"] else "–"],
                   ["Koszt usunięcia ryzyk", M(MO.zl(rk["koszt_ryzyk"]) + " – szacunek")], ["Proponowana cena zakupu", M(MO.zl(rk["cena_proponowana"])) if rk["cena_proponowana"] else "–"]])
    sp = n.get("stan_prawny") or {}
    if sp:
        MO._akapit(d, "2. Stan prawny", pogrub=True)
        MO._akapit(d, M("Stan prawny odczytany przez AI z dokumentów – sprawdź z odpisem księgi wieczystej."), kursywa=True, rozmiar=9)
        MO._tabela(d, [["Element", "Ustalenia"]] + [[a, (", ".join(sp.get(k)) if isinstance(sp.get(k), list) else str(sp.get(k) or "–"))] for a, k in
                                                       (("Księga wieczysta", "kw"), ("Właściciele", "wlasciciele"), ("Forma władania", "forma"), ("Działki", "dzialki"),
                                                        ("Hipoteki", "hipoteki"), ("Służebności", "sluzebnosci"), ("Roszczenia, ostrzeżenia", "roszczenia_ostrzezenia"),
                                                        ("Egzekucje", "egzekucje"), ("Uwagi", "uwagi"))])
    MO._akapit(d, "3. Ryzyka", pogrub=True)
    R = sorted([r for r in n.get("ryzyka") or [] if r.get("status") != "wykluczone"], key=lambda r: ["czerwone", "zolte", "zielone"].index(r.get("waga", "zolte")) if r.get("waga") in WAGI else 1)
    ds = lambda r, x: M(x) if r.get("status") == "do_sprawdzenia" and x else x
    MO._tabela(d, [["Waga", "Obszar", "Ryzyko", "Status", "Źródło", "Koszt"]] + [[r.get("waga", ""), OBSZARY.get(r.get("obszar"), r.get("obszar", "")), ds(r, r.get("opis", "")),
                                                                                ds(r, STATUSY.get(r.get("status"), "")), (r.get("dokument") or r.get("zrodlo") or "") + (" – " + r["miejsce"] if r.get("miejsce") else ""),
                                                                                M(MO.zl(_f(r.get("koszt_zl")))) if r.get("koszt_zl") else "–"] for r in R] or [["–", "", "Brak ryzyk", "", "", ""]])
    P = n.get("pisma") or []
    if P:
        MO._akapit(d, "4. Pisma do urzędów i gestorów", pogrub=True)
        MO._tabela(d, [["Pismo", "Wysłano", "Termin", "Status"]] + [[PISMA.get(p.get("rodzaj"), (p.get("rodzaj"),))[0], p.get("wyslano") or "–", p.get("termin") or "–",
                                                                       "odpowiedź otrzymana" if p.get("odpowiedz") else M("w drodze") if p.get("wyslano") else M("do wysłania")] for p in P])
    og = n.get("ogledziny") or {}
    if og.get("punkty"):
        MO._akapit(d, "5. Oględziny" + (f" ({og['data']})" if og.get("data") else ""), pogrub=True)
        MO._tabela(d, [["Punkt", "Ocena", "Uwagi"]] + [[k, v.get("ocena", ""), v.get("uwagi", "")] for k, v in og["punkty"].items() if v.get("ocena") or v.get("uwagi")])
    war = [r.get("zapis_umowy") for r in R if r.get("zapis_umowy")]
    MO._akapit(d, "6. Warunki do umowy przedwstępnej", pogrub=True)
    for w_ in war or ["[UZUPEŁNIJ: warunki do umowy przedwstępnej]"]:
        MO._akapit(d, M(w_ + " [propozycja]"), styl="List Bullet")
    MO._akapit(d, "Zastrzeżenia: raport opiera się na dokumentach, odpowiedziach urzędów, oględzinach i danych publicznych według stanu na datę raportu. "
                  "Dane z map są poglądowe. Przy transakcji raport powinien zaakceptować prawnik (stan prawny) i rzeczoznawca majątkowy (wartość).", kursywa=True, rozmiar=8)
    podswietl(d)
    d.save(sciezka)


def raport_zabudowy(sciezka, n):
    z = n.get("zabudowa") or {}
    w, p = z.get("wynik") or {}, z.get("parametry") or {}
    d = _naglowek("ANALIZA ZABUDOWY DZIAŁKI – CO I ILE MOŻNA ZBUDOWAĆ", n, "analiza przed zakupem – nie jest projektem")
    pewne = (n.get("plan") or {}).get("status") == "potwierdzone" or str(p.get("zrodlo") or "").startswith("z dokumentów")
    Mp = (lambda x: x) if pewne else M
    MO._tabela(d, [["Parametr", "Wartość"], ["Przeznaczenie", Mp(p.get("przeznaczenie") or "–")], ["Źródło parametrów", Mp((p.get("zrodlo") or "–") + ("" if pewne else " – potwierdź wypisem z planu"))],
                   ["Powierzchnia działki", f"{w.get('pow_dzialki', 0)} m²"],
                   ["Obszar, na którym wolno stawiać budynki", f"{w.get('obszar_zabudowy', 0)} m²" if w.get("geometria") else M(f"{w.get('obszar_zabudowy', 0)} m² (szacunek – brak granic)")],
                   ["Maks. powierzchnia zabudowy", f"{w.get('pow_zabudowy_max', 0)} m²"], ["Maks. powierzchnia całkowita", f"{w.get('pow_calkowita_max', 0)} m²"],
                   ["Powierzchnia użytkowa (szac.)", f"{w.get('pum', 0)} m²"], ["Liczba mieszkań (szac.)", str(w.get("lokale", 0))], ["Miejsca parkingowe", str(w.get("parking", 0))],
                   ["Min. powierzchnia biologicznie czynna", f"{w.get('pbc_min', 0)} m²" + ("" if w.get("pbc_ok", True) else " – UWAGA: może być trudna do zachowania")]])
    MO._akapit(d, "Scenariusze", pogrub=True)
    MO._tabela(d, [["Scenariusz", "Wynik", "Koszt budowy", "Wartość po realizacji", "Maks. cena działki"]] +
               [[s["nazwa"], s["wynik"], M(MO.zl(s["koszt"])) if s.get("koszt") else "–", M(MO.zl(s["wartosc"])) if s.get("wartosc") else "–",
                 M(MO.zl(s["max_cena"])) if s.get("max_cena") is not None else (s.get("uwaga") or "–")] for s in w.get("scenariusze") or []])
    MO._akapit(d, M("Koszty budowy i wartości za m² są orientacyjne (do zmiany w programie); marża inwestora 15%, koszty dodatkowe 12% – założenia."), kursywa=True, rozmiar=8)
    MO._akapit(d, "Do sprawdzenia przez projektanta: nasłonecznienie i przesłanianie, wymagania pożarowe i dojazd straży, szczegółowe odległości wg warunków technicznych, "
                  "strefy ochronne sieci według gestorów. Przy działce bez planu wynik jest szacunkiem i wymaga decyzji o warunkach zabudowy.", kursywa=True, rozmiar=8)
    podswietl(d)
    d.save(sciezka)


def operat_docx(sciezka, n, w, teksty, koncowy=False):
    """Projekt operatu (do zatwierdzenia) albo wersja do podpisu – układ: cel, przedmiot, podstawy, daty, opis, plan, rynek, metoda, obliczenia, wynik, klauzule."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    i, dn = n.get("identyfikacja") or {}, n.get("dane") or {}
    pod, wyn = wynik_wyceny(w)
    PK = w.get("punkty") or {}
    zatw = lambda k: (PK.get(k) or {}).get("status") == "zatwierdzony"
    Mz = (lambda x, k: x if koncowy or zatw(k) else M(x))  # do sprawdzenia, dopóki punkt kontrolny nie jest zatwierdzony
    d = MO._doc()
    if not koncowy:
        MO._akapit(d, "PROJEKT – DO WERYFIKACJI I ZATWIERDZENIA PRZEZ RZECZOZNAWCĘ MAJĄTKOWEGO", pogrub=True, rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        MO._akapit(d, M(LEGENDA), kursywa=True, rozmiar=8, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "OPERAT SZACUNKOWY", pogrub=True, rozmiar=16, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"określający {w.get('rodzaj_wartosci') or 'wartość rynkową'} nieruchomości", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    przedm = (f"{TYPY.get(dn.get('typ'), '')} nr {dn.get('nr_lokalu') or '[UZUPEŁNIJ]'}, {dn.get('adres') or ''}, pow. użytkowa {dn.get('pow_uzytkowa') or '[UZUPEŁNIJ]'} m²"
              if RODZAJ.get(dn.get("typ")) == "lokal" else f"{TYPY.get(dn.get('typ'), '')} – {opis_dzialek(n)}" + (f", {dn['adres']}" if dn.get("adres") else "")
              + (f", budynek {dn['pow_uzytkowa']} m²" if dn.get("pow_uzytkowa") and RODZAJ.get(dn.get("typ")) == "dom" else ""))
    pl = n.get("plan") or {}
    przezn = (f"{pl.get('symbol') or ', '.join(pl.get('symbole') or [])} – {pl.get('przeznaczenie') or ''} ({pl.get('zrodlo_opis') or pl.get('zrodlo') or ''}, {pl.get('status') or 'wstępne'})"
              if pl else "[UZUPEŁNIJ: plan miejscowy / plan ogólny / decyzja WZ / faktyczne użytkowanie]")
    if pl and pl.get("status") != "potwierdzone" and not koncowy:
        przezn = M(przezn + " – potwierdź wypisem z planu")
    MO._tabela(d, [["Element", "Dane"], ["Przedmiot wyceny", Mz(przedm, "k2")],
                   ["Księga wieczysta", Mz(dn.get("kw") or (n.get("stan_prawny") or {}).get("kw"), "k2") if (dn.get("kw") or (n.get("stan_prawny") or {}).get("kw")) else "[UZUPEŁNIJ]"],
                   ["Cel wyceny", Mz(w["cel"], "k1") if w.get("cel") else "[UZUPEŁNIJ]"],
                   ["Data wyceny / stan nieruchomości na dzień", Mz(f"{w.get('data_wyceny') or '[UZUPEŁNIJ]'} / {w.get('stan_na') or (n.get('ogledziny') or {}).get('data') or '[UZUPEŁNIJ]'}", "k1")],
                   ["Data oględzin", Mz(n["ogledziny"]["data"], "k3") if (n.get("ogledziny") or {}).get("data") else "[UZUPEŁNIJ]"],
                   ["Przeznaczenie (art. 154 UGN)", przezn],
                   ["Podejście / metoda", Mz(PODEJSCIA.get(pod, pod), "k5")], ["Zamawiający", w.get("zamawiajacy") or "[UZUPEŁNIJ]"]])
    for nr, (tyt, klucz) in enumerate((("Opis nieruchomości", "opis_nieruchomosci"), ("Stan prawny", "stan_prawny"), ("Przeznaczenie w planie miejscowym", "przeznaczenie"),
                                       ("Analiza rynku", "analiza_rynku"), ("Wybór podejścia i metody", "uzasadnienie_podejscia"), ("Cechy rynkowe i ich wagi", "cechy_opis")), 1):
        MO._akapit(d, f"{nr}. {tyt}", pogrub=True)
        tx = str((teksty or {}).get(klucz) or "")
        MO._akapit(d, (tx if koncowy else M(tx + " [tekst przygotowany przez AI – sprawdź i popraw]")) if tx else "[UZUPEŁNIJ]")
    T = [t for t in w.get("transakcje") or [] if not t.get("wykluczona")]
    zl_ = MO.zl
    if pod in ("porownawcze", "parami") and T:
        if pod == "parami":
            T = [t for t in T if t["id"] in (w.get("wybrane_parami") or [])]
        MO._akapit(d, "7. Transakcje przyjęte do porównania", pogrub=True)
        def _lok(t):
            u = []
            if t.get("przywrocona") or t.get("poszerzenie"):
                u.append(t.get("przywrocona") or t.get("poszerzenie"))
            if str(t.get("zrodlo") or "").lower().endswith((".pdf", ".jpg", ".png")):
                u.append("odczytana przez AI z wyciągu – sprawdź z dokumentem")
            return M(f"{t.get('lokalizacja', '')} ({'; '.join(u)})") if u and not koncowy else t.get("lokalizacja", "")
        MO._tabela(d, [["Lp.", "Data", "Położenie", "Pow. [m²]", "Cena [zł]", "Cena jedn. [zł/m²]"]] +
                   [[str(k), t.get("data", ""), _lok(t), f"{_f(t.get('pow')):g}", zl_(_f(t.get('cena'))), zl_(_f(t.get('cena_m2')))] for k, t in enumerate(T, 1)][:60])
    MO._akapit(d, "8. Obliczenia", pogrub=True)
    if pod == "porownawcze":
        MO._akapit(d, Mz(f"Ceny skorygowane na datę wyceny trendem {wyn.get('trend_mies', 0) * 100:.2f}% miesięcznie", "k6") + f". Cmin = {zl_(wyn.get('cmin', 0))}/m², "
                      f"Cmax = {zl_(wyn.get('cmax', 0))}/m², Cśr = {zl_(wyn.get('csr', 0))}/m², liczba transakcji: {wyn.get('liczba', 0)}.")
        MO._tabela(d, [["Cecha", "Waga [%]", "Ocena przedmiotu", "Współczynnik ki"]] + [[x["cecha"], Mz(f"{x['waga_pct']:g}", "k6"), Mz({1: "gorsza", 2: "przeciętna", 3: "lepsza"}.get(x["ocena"], ""), "k6"),
                                                                                      f"{x['wspolczynnik']:.4f}"] for x in wyn.get("wiersze") or []])
        MO._akapit(d, Mz(f"W = P × Cśr × Σki = {_f(dn.get('pow_przedmiotu')):g} m² × {zl_(wyn.get('csr', 0))} × {wyn.get('suma_k', 0):.4f} = {zl_(_f(wyn.get('wartosc')))}", "k6"))
    elif pod == "parami":
        MO._akapit(d, f"Ceny jednostkowe skorygowane na datę wyceny trendem {wyn.get('trend_mies', 0) * 100:.2f}% miesięcznie; jeden stopień różnicy cechy = waga × ½ rozpiętości cen "
                      f"({zl_(wyn.get('rozpietosc', 0))}/m²).")
        MO._tabela(d, [["Transakcja", "Cena jedn."] + list(wyn.get("cechy") or []) + ["Cena skorygowana"]] +
                   [[f"{x['data']} {x.get('lokalizacja') or ''}", zl_(x["cena_m2"])] + [Mz(f"{k:+.2f}", "k6") for k in x["korekty"]] + [zl_(x["skorygowana"])] for x in wyn.get("wiersze") or []])
        MO._akapit(d, Mz(f"Korekta za jeden stopień różnicy cechy = waga × {U['korekta_parami']:g} rozpiętości cen – założenie (ustawienia rzeczoznawcy).", "k6"), kursywa=True, rozmiar=9)
        MO._akapit(d, f"Cena jednostkowa przedmiotu wyceny = średnia cen skorygowanych = {zl_(wyn.get('cena_m2', 0))}/m²; W = {_f(dn.get('pow_przedmiotu')):g} m² × {zl_(wyn.get('cena_m2', 0))} = {zl_(_f(wyn.get('wartosc')))}")
    elif pod == "kosztowe":
        MO._tabela(d, [["Składnik", "Obliczenie", "Wartość"],
                       ["Grunt", f"{wyn.get('pow_gruntu', 0):g} m² × " + Mz(f"{zl_(wyn.get('cena_gruntu_m2', 0))}/m²", "k6"), zl_(wyn.get("wartosc_gruntu", 0))],
                       ["Budynek – koszt odtworzenia", f"{wyn.get('pow_budynku', 0):g} m² × " + (M(f"{zl_(wyn.get('koszt_odtw_m2', 0))}/m² (wartość domyślna wg standardu)")
                                                                                              if not (w.get("kosztowe_param") or {}).get("koszt_odtw_m2") and not koncowy and not zatw("k6")
                                                                                              else f"{zl_(wyn.get('koszt_odtw_m2', 0))}/m²"), zl_(_f(wyn.get('pow_budynku')) * _f(wyn.get('koszt_odtw_m2')))],
                       ["Zużycie", Mz(f"wiek {wyn.get('wiek', 0)} lat / trwałość {wyn.get('trwalosc', 0)} lat, z korektą o stan", "k6"), Mz(f"{wyn.get('zuzycie_pct', 0)}%", "k6")],
                       ["Budynek po zużyciu", "", zl_(wyn.get("wartosc_budynku", 0))], ["Budynki dodatkowe / zagospodarowanie", "", zl_(wyn.get("dodatkowe", 0))],
                       ["RAZEM", "", zl_(wyn.get("wartosc", 0))]])
    elif pod == "dochodowe":
        MO._tabela(d, [["Składnik", "Wartość"], ["Czynsz rynkowy", f"{zl_(wyn.get('czynsz_m2', 0))}/m² miesięcznie × {wyn.get('pow', 0):g} m²"],
                       ["Potencjalny dochód brutto (rocznie)", zl_(wyn.get("pdb", 0))], ["Pustostany i niezapłacone czynsze", f"{wyn.get('pustostany_pct', 0)}%"],
                       ["Rzeczywisty dochód brutto", zl_(wyn.get("rdb", 0))], ["Koszty operacyjne", zl_(wyn.get("koszty", 0))], ["Dochód operacyjny netto (DOR)", zl_(wyn.get("dor", 0))],
                       ["Stopa kapitalizacji", Mz(f"{wyn.get('stopa_pct', 0)}%", "k6")], ["W = DOR / R", zl_(wyn.get("wartosc", 0))]])
        if w.get("czynsze_ofertowe") and not koncowy and not zatw("k6"):
            MO._akapit(d, M(f"Czynsz rynkowy z ofert najmu (mediana {zl_(w['czynsze_ofertowe'].get('mediana_m2', 0))}/m²) – potwierdź z transakcjami najmu."), kursywa=True, rozmiar=9)
    elif pod == "pozostalosciowa":
        MO._tabela(d, [["Składnik", "Wartość"], ["Scenariusz zagospodarowania", f"{wyn.get('scenariusz', '')} – {wyn.get('wynik_zabudowy', '')}"],
                       ["Wartość po realizacji", zl_(wyn.get("wartosc_po_realizacji", 0))], ["Koszt budowy", zl_(wyn.get("koszt_budowy", 0))],
                       ["Koszty dodatkowe (projekt, przyłącza, opłaty)", Mz(zl_(wyn.get("koszty_dodatkowe", 0)) + f" ({U['koszty_dod_pct']:g}% kosztu budowy – założenie)", "k6")],
                       ["Zysk inwestora", Mz(zl_(wyn.get("zysk_inwestora", 0)) + f" ({U['marza_pct']:g}% wartości – założenie)", "k6")],
                       ["Wartość gruntu (pozostałość)", zl_(wyn.get("wartosc", 0))]])
    elif pod == "wskazniki":
        MO._tabela(d, [["Klasa / użytek", "Powierzchnia [ha]", "Wskaźnik [dt/ha]", "Wartość"]] +
                   [[x["klasa"], f"{x['pow_ha']:g}", Mz(f"{x['wskaznik']:g}", "k6"), zl_(x["wartosc"])] for x in wyn.get("wiersze") or []] +
                   [["RAZEM", "", "", zl_(wyn.get("suma", 0))]])
        MO._akapit(d, Mz(f"Cena 1 dt: {zl_(wyn.get('cena_dt', 0))}" + (f" ({wyn['zrodlo_ceny']})" if wyn.get("zrodlo_ceny") else "") +
                         (f"; korekta {wyn['korekta_pct']:+g}%" if wyn.get("korekta_pct") else "") + " – wskaźniki i cenę potwierdź z przepisami i aktualnym komunikatem.", "k6"))
    MO._akapit(d, "9. Wynik", pogrub=True)
    MO._akapit(d, Mz(f"Wartość nieruchomości: {zl_(_f(wyn.get('wartosc_zaokr')))} (słownie: {MO.slownie(_f(wyn.get('wartosc_zaokr')))}).", "k6"), pogrub=True)
    if U.get("uzasadnienie"):
        MO._akapit(d, "Przyjęte założenia (ustawienia rzeczoznawcy)", pogrub=True)
        MO._akapit(d, str(U["uzasadnienie"]))
    uz = [(nazwa, (w.get("punkty") or {}).get(k, {})) for k, nazwa in PUNKTY]
    uz = [(nazwa, p) for nazwa, p in uz if p.get("uwaga")]
    if uz:
        MO._akapit(d, "Uzasadnienia rzeczoznawcy przy zatwierdzaniu", pogrub=True)
        for nazwa, p in uz:
            MO._akapit(d, f"{nazwa}: {p['uwaga']}", styl="List Bullet")
    MO._akapit(d, "10. Klauzule i założenia", pogrub=True)
    for k_ in [(x if koncowy else M(str(x) + " [propozycja AI]")) for x in ((teksty or {}).get("klauzule") or [])] + ["Operat może być wykorzystywany do celu, dla którego został sporządzony, przez okres 12 miesięcy od daty jego sporządzenia, "
                                                       "chyba że wystąpiły zmiany uwarunkowań prawnych lub istotne zmiany czynników wpływających na wartość."]:
        MO._akapit(d, str(k_), styl="List Bullet")
    if not koncowy:
        MO._akapit(d, "Status punktów kontrolnych", pogrub=True)
        MO._tabela(d, [["Punkt", "Status"]] + [[nazwa, (f"zatwierdzony – {PK[k].get('kto', '')}, {PK[k].get('kiedy', '')}" if zatw(k)
                                                         else M("do ponownego potwierdzenia" if (PK.get(k) or {}).get("status") == "do_ponownego" else "niezatwierdzony"))] for k, nazwa in PUNKTY])
    MO._akapit(d, f"\n\nSporządził: {w.get('rzeczoznawca') or '[imię i nazwisko rzeczoznawcy majątkowego]'}, uprawnienia nr {w.get('nr_uprawnien') or '[UZUPEŁNIJ]'}"
                  + ("" if koncowy else "\nPROJEKT – wymaga weryfikacji, zatwierdzenia i podpisu rzeczoznawcy."), wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    podswietl(d, aktywne=not koncowy)
    d.save(sciezka)


def braki_punktu(k, n, w, aktywne):
    """Co musi być uzupełnione, żeby zatwierdzić punkt kontrolny (lista braków – pusta = można zatwierdzić)."""
    d = n.get("dane") or {}
    pod, wyn = wynik_wyceny(w)
    b = []
    if k == "k1":
        b += [x for x, ok in (("cel wyceny", w.get("cel")), ("rodzaj wartości", w.get("rodzaj_wartosci")), ("data wyceny", w.get("data_wyceny")),
                              ("rzeczoznawca", w.get("rzeczoznawca")), ("nr uprawnień", w.get("nr_uprawnien"))) if not ok]
    elif k == "k2":
        if not ((n.get("stan_prawny") or {}).get("kw") or d.get("kw") or (n.get("stan_prawny") or {}).get("wlasciciele")):
            b.append("stan prawny (analiza dokumentów albo numer księgi wieczystej)")
        if not _f(d.get("pow_przedmiotu") or d.get("pow_uzytkowa") or d.get("pow_dzialki")):
            b.append("powierzchnia przedmiotu wyceny")
    elif k == "k3":
        if not (n.get("ogledziny") or {}).get("data"):
            b.append("data oględzin")
    elif k == "k4":
        if pod in MIN_METODY and aktywne < 3:
            b.append(f"co najmniej 3 przyjęte transakcje (jest {aktywne})")
    elif k == "k5":
        if not w.get("podejscie"):
            b.append("wybrane podejście i metoda")
    elif k == "k6":
        if not wyn.get("wartosc"):
            b.append("obliczona wartość dla wybranego podejścia")
    return b


def kontrola_operatu(n, w):
    """Kontrola kompletności i spójności przed zatwierdzeniem operatu (reguły – bez AI), według wybranego podejścia i metody."""
    u = []
    dn = n.get("dane") or {}
    pod, wyn = wynik_wyceny(w)
    for pole_, opis in (("cel", "cel wyceny"), ("data_wyceny", "data wyceny"), ("rzeczoznawca", "rzeczoznawca"), ("nr_uprawnien", "numer uprawnień")):
        if not w.get(pole_):
            u.append(("krytyczna", f"Brak: {opis}."))
    if not (n.get("ogledziny") or {}).get("data"):
        u.append(("krytyczna", "Brak daty oględzin – oględziny przeprowadza rzeczoznawca osobiście."))
    if not _f(dn.get("pow_przedmiotu") or dn.get("pow_uzytkowa") or dn.get("pow_dzialki")):
        u.append(("krytyczna", "Brak powierzchni przedmiotu wyceny."))
    if not (n.get("stan_prawny") or {}).get("kw") and not dn.get("kw"):
        u.append(("istotna", "Brak numeru księgi wieczystej."))
    if not (n.get("plan") or {}).get("przeznaczenie") and not (n.get("plan") or {}).get("symbol") and not (n.get("plan") or {}).get("symbole"):
        u.append(("istotna", "Nie ustalono przeznaczenia nieruchomości (plan miejscowy / plan ogólny / decyzja WZ / faktyczne użytkowanie – art. 154 UGN)."))
    T = [t for t in w.get("transakcje") or [] if not t.get("wykluczona")]
    if pod in MIN_METODY:
        ile = len([t for t in T if t["id"] in (w.get("wybrane_parami") or [])]) if pod == "parami" else len(T)
        if ile < MIN_METODY[pod]:
            u.append(("krytyczna" if ile < 3 else "istotna", f"Liczba transakcji ({ile}) mniejsza niż wymagana dla metody {PODEJSCIA[pod].split('– ')[-1]} ({MIN_METODY[pod]})."))
        if any(t.get("wykluczona") and not t.get("powod") for t in w.get("transakcje") or []):
            u.append(("istotna", "Wykluczona transakcja bez uzasadnienia."))
        if abs(sum(_f(c.get("waga")) for c in w.get("cechy") or []) - 100) > 0.5:
            u.append(("istotna", "Wagi cech nie sumują się do 100%."))
        if w.get("data_wyceny") and T:
            dd = [x for x in (data_transakcji(t.get("data")) for t in T) if x]
            dw_ = data_transakcji(w["data_wyceny"])
            if dd and dw_ and (dw_ - min(dd)).days > 3 * 365:
                u.append(("drobna", "Najstarsza transakcja ma ponad 3 lata – sprawdź okres badania rynku."))
    if not wyn.get("wartosc"):
        u.append(("krytyczna", f"Brak obliczeń dla wybranego podejścia ({PODEJSCIA.get(pod, pod)})."))
    elif pod == "porownawcze" and dn.get("pow_przedmiotu") and abs(_f(wyn["cena_m2"]) * _f(dn["pow_przedmiotu"]) - _f(wyn["wartosc"])) > max(1, _f(dn["pow_przedmiotu"]) * 0.006):
        u.append(("krytyczna", "Wynik niezgodny z obliczeniami – przelicz wycenę."))
    if pod == "kosztowe" and (w.get("kosztowe") or {}).get("brak_gruntu"):
        u.append(("istotna", "W podejściu kosztowym brak ceny gruntu za m² – wartość gruntu = 0."))
    niezatw = [naz for k, naz in PUNKTY if (w.get("punkty") or {}).get(k, {}).get("status") != "zatwierdzony"]
    if niezatw:
        u.append(("krytyczna", "Niezatwierdzone punkty kontrolne: " + ", ".join(niezatw) + "."))
    return [{"waga": a, "opis": b} for a, b in u]


def podsumowanie_pakietu(sciezka, n):
    rk = rekomendacja(n)
    d = _naglowek("PEŁNY PAKIET – PODSUMOWANIE DLA DECYZJI", n)
    MO._tabela(d, [["", ""], ["Rekomendacja", f"{rk['decyzja']} – {rk['uzasadnienie']}"],
                   ["Wartość rynkowa (projekt operatu / operat)", MO.zl(rk["wartosc"]) if rk["wartosc"] else "–"],
                   ["Możliwa zabudowa", ((n.get("zabudowa") or {}).get("wynik") or {}).get("scenariusze", [{}])[0].get("wynik", "–") if (n.get("zabudowa") or {}).get("wynik") else "–"],
                   ["Maks. cena z analizy zabudowy", MO.zl(rk["max_cena_zabudowa"]) if rk["max_cena_zabudowa"] else "–"],
                   ["Ryzyka", f"{len([r for r in n.get('ryzyka') or [] if r.get('status') != 'wykluczone'])} (w tym krytyczne: "
                              f"{len([r for r in n.get('ryzyka') or [] if r.get('waga') == 'czerwone' and r.get('status') != 'wykluczone'])})"],
                   ["Koszt usunięcia ryzyk", MO.zl(rk["koszt_ryzyk"])], ["Proponowana cena zakupu", MO.zl(rk["cena_proponowana"]) if rk["cena_proponowana"] else "–"]])
    MO._akapit(d, "Szczegóły: raport due diligence, analiza zabudowy i operat szacunkowy w załączonych plikach.", kursywa=True, rozmiar=9)
    podswietl(d)
    d.save(sciezka)


# ================================================================ WYCENA WŁASNA – szacunek z ofert rynkowych (nie operat, bez rzeczoznawcy)
PRODUKTY["wlasna"] = "Wycena własna (szacunek z ofert)"
CECHY_WLASNE = {  # (cecha, korekta za 1 stopień różnicy [%]) – czytelny model porównawczy dla osób prywatnych
    "lokal": [("Lokalizacja", 8), ("Standard i stan", 6), ("Piętro, winda, ekspozycja", 3), ("Powierzchnia i układ", 3), ("Dodatki (balkon, parking, piwnica)", 3)],
    "dom": [("Lokalizacja", 8), ("Standard i stan", 7), ("Powierzchnia domu", 3), ("Działka (wielkość, zagospodarowanie)", 4), ("Dodatki (garaż, ogrzewanie)", 3)],
    "dzialka": [("Lokalizacja", 10), ("Przeznaczenie i media", 8), ("Kształt i wielkość", 4), ("Dojazd", 4), ("Otoczenie", 3)],
}
KOREKTA_OFERT_DOMYSLNA = 7.0  # [%] gdy brak cen transakcyjnych z okolicy


def cechy_wlasne(rodzaj):
    return CECHY_WLASNE.get(rodzaj, CECHY_WLASNE["lokal"])


def opis_przedmiotu(n):
    d, i = n.get("dane") or {}, n.get("identyfikacja") or {}
    b = i.get("budynek") or {}
    pola = {k: d.get(k) for k in ("typ", "adres", "pow_uzytkowa", "pow_dzialki", "pokoje", "pietro", "kondygnacje_budynku", "winda", "balkon", "parking", "piwnica",
                                  "rok_budowy", "technologia", "standard", "stan", "rynek", "ogrzewanie", "budynki_dodatkowe") if d.get(k)}
    pola["typ"] = TYPY.get(d.get("typ"), d.get("typ"))
    pola["miejscowosc"] = b.get("miejscowosc") or i.get("gmina") or ""
    pola["dzielnica"] = b.get("dzielnica") or i.get("obreb") or ""
    if (n.get("plan") or {}).get("przeznaczenie"):
        pola["przeznaczenie_plan"] = f"{n['plan'].get('symbol') or ''} {n['plan']['przeznaczenie']}".strip()
    return pola


def polecenie_ofert_wlasnych(n, szerzej=False, znane=()):
    p = opis_przedmiotu(n)
    rz = RODZAJ.get((n.get("dane") or {}).get("typ"), "dzialka")
    return (f"Wyceniana nieruchomość: {json.dumps(p, ensure_ascii=False)}.\n"
            "Znajdź w internecie AKTUALNE oferty sprzedaży PODOBNYCH nieruchomości (portale: Otodom, Morizon, Domiporta, Gratka, OLX Nieruchomości, Nieruchomosci-online, "
            "strony deweloperów). Kryteria: ten sam rodzaj, "
            + ("ta sama miejscowość i najbliższe okolice, powierzchnia ±50%, " if szerzej else "ta sama miejscowość i możliwie ta sama dzielnica / okolica, powierzchnia ±30%, ")
            + ("podobny rok budowy i standard, " if rz != "dzialka" else "podobne przeznaczenie i dostęp do mediów, ")
            + "co najmniej 12, najlepiej 15–20 ofert. Korzystaj także ze STRON WYNIKÓW wyszukiwania portali (lista ofert z ceną i metrażem) – każda oferta z listy to osobna "
            "pozycja; link do ogłoszenia, a gdy go nie widać – link do strony wyników. Cenę i powierzchnię podawaj jako LICZBY (bez „zł”, „m²”, spacji). "
            "Nie zmyślaj – tylko oferty, które rzeczywiście widziałeś."
            + (f" Pomiń oferty, które już mam: {', '.join(list(znane)[:30])}." if znane else "") + "\n"
            'Zwróć WYŁĄCZNIE JSON: {"oferty": [{"portal": "…", "url": "https://…", "tytul": "…", "lokalizacja": "ulica / osiedle / dzielnica", "pow": liczba, "cena": liczba, '
            '"pokoje": liczba lub null, "pietro": "…", "rok_budowy": liczba lub null, "standard": "krótko: do remontu / do odświeżenia / dobry / wysoki / deweloperski", '
            '"dodatki": "balkon, parking, piwnica…", "pow_dzialki": liczba lub null, "przeznaczenie": "…", "data": "RRRR-MM-DD lub null"}]}')


def polecenie_oferty_z_tekstu(teksty):
    return ("Poniżej treść stron z ogłoszeniami nieruchomości (każda z adresem URL). Strona może być POJEDYNCZYM ogłoszeniem albo LISTĄ WYNIKÓW z wieloma ofertami – "
            "odczytaj wszystkie oferty (do 30 na stronę), każdą z ceną i powierzchnią jako liczbami. Nie zmyślaj – brak = null.\n\n"
            + "\n\n".join(f"=== {u} ===\n{t[:20000]}" for u, t in teksty)
            + '\n\nZwróć WYŁĄCZNIE JSON: {"oferty": [{"url": "…", "portal": "…", "tytul": "…", "lokalizacja": "…", "pow": liczba, "cena": liczba, "pokoje": liczba lub null, '
            '"pietro": "…", "rok_budowy": liczba lub null, "standard": "…", "dodatki": "…", "pow_dzialki": liczba lub null, "przeznaczenie": "…"}]}')


def polecenie_ocen_wlasnych(n, oferty):
    rz = RODZAJ.get((n.get("dane") or {}).get("typ"), "dzialka")
    cechy = [c for c, _ in cechy_wlasne(rz)]
    return (f"Wyceniana nieruchomość: {json.dumps(opis_przedmiotu(n), ensure_ascii=False)}.\n"
            f"Oferty porównawcze: {json.dumps([{k: o.get(k) for k in ('id', 'tytul', 'lokalizacja', 'pow', 'pokoje', 'pietro', 'rok_budowy', 'standard', 'dodatki', 'pow_dzialki', 'przeznaczenie')} for o in oferty], ensure_ascii=False)[:14000]}\n"
            f"Dla każdej oferty oceń cechy NA TLE wycenianej nieruchomości: {', '.join(cechy)}. Skala: -2 wyraźnie gorsza, -1 gorsza, 0 podobna, 1 lepsza, 2 wyraźnie lepsza. "
            "Gdy brak informacji – 0. Krótkie uzasadnienie (do 120 znaków).\n"
            'Zwróć WYŁĄCZNIE JSON: {"oceny": [{"id": "…", "cechy": {"nazwa cechy": liczba}, "uzasadnienie": "…"}]}')


def liczba_z_tekstu(x):
    """Liczba z zapisu z ogłoszenia: „359 000 zł”, „1 250 000,00 zł”, „52,4 m²”, „450 tys. zł”, „1,2 mln”."""
    if isinstance(x, (int, float)):
        return float(x)
    t = str(x or "").lower().replace("\u00a0", " ").replace("\u202f", " ")
    m = re.search(r"\d[\d ]*(?:[.,]\d+)?", t)
    if not m:
        return 0.0
    liczba = m.group(0).replace(" ", "")
    if "," in liczba and "." in liczba:
        liczba = liczba.replace(".", "").replace(",", ".")
    else:
        liczba = liczba.replace(",", ".")
    try:
        v = float(liczba)
    except ValueError:
        return 0.0
    reszta = t[m.end():m.end() + 6]
    if re.match(r"\s*mln", reszta):
        v *= 1_000_000
    elif re.match(r"\s*tys", reszta):
        v *= 1000
    return v


RE_PORTALE = re.compile(r"(?i)\s*[|•–-]?\s*\b(otodom|morizon|domiporta|gratka|olx(\s+nieruchomości)?|nieruchomosci-online|adresowo|szybko\.pl|sprzedajemy)(\.pl)?\b\s*[|•–-]?\s*")


def bez_portalu(t):
    """W wycenie własnej źródło to „dane rynkowe” – nazwy portali nie trafiają do opisów ofert widocznych w programie i raporcie."""
    return re.sub(r"\s{2,}", " ", RE_PORTALE.sub(" ", str(t or ""))).strip(" |•–-")


def oferta_porz(o, k):
    cena, pw = liczba_z_tekstu(o.get("cena")), liczba_z_tekstu(o.get("pow"))
    if cena and pw and cena < 10000 and pw > 0:  # cena podana za m² zamiast całkowitej
        cena = cena * pw
    if not (cena and pw):
        return None
    return {"id": f"o{k}", "portal": str(o.get("portal") or "")[:40], "url": str(o.get("url") or "")[:400], "tytul": bez_portalu(o.get("tytul"))[:160],
            "lokalizacja": bez_portalu(o.get("lokalizacja"))[:160], "pow": pw, "cena": cena, "cena_m2": round(cena / pw, 2), "pokoje": liczba_z_tekstu(o.get("pokoje")) or None,
            "pietro": str(o.get("pietro") or "")[:30], "rok_budowy": o.get("rok_budowy"), "standard": str(o.get("standard") or "")[:80],
            "dodatki": str(o.get("dodatki") or "")[:160], "pow_dzialki": liczba_z_tekstu(o.get("pow_dzialki")) or None, "przeznaczenie": str(o.get("przeznaczenie") or "")[:80],
            "data": str(o.get("data") or "")[:10], "oceny": {}, "wykluczona": False, "zrodlo": str(o.get("_zrodlo") or "wyszukiwanie")}


def oblicz_wlasna(n, wl):
    """Metoda porównawcza dla wyceny własnej: cena ofertowa za m² → korekta oferta/transakcja → korekty cech (stopień × %) →
    średnia ważona podobieństwem; przedział z rozrzutu; pewność z liczby, podobieństwa i rozrzutu ofert."""
    d = n.get("dane") or {}
    rz = RODZAJ.get(d.get("typ"), "dzialka")
    P = _f(d.get("pow_uzytkowa") if rz != "dzialka" else d.get("pow_dzialki")) or _f(d.get("pow_przedmiotu"))
    O = [o for o in wl.get("oferty") or [] if not o.get("wykluczona") and _f(o.get("cena_m2"))]
    if len(O) < 3:
        return {"blad": "Za mało ofert do porównania (co najmniej 3) – wyszukaj oferty albo dodaj linki."}
    if not P:
        return {"blad": "Podaj powierzchnię wycenianej nieruchomości (krok 1)."}
    # korekta oferta → transakcja: z cen transakcyjnych w teczce (gdy są), inaczej typowa
    T = [_f(t.get("cena_m2")) for t in (n.get("wycena") or {}).get("transakcje") or [] if not t.get("wykluczona") and _f(t.get("cena_m2"))]
    med_o = statistics.median(_f(o["cena_m2"]) for o in O)
    if wl.get("korekta_pct") not in (None, ""):
        kor, zr_kor = _f(wl["korekta_pct"]), "wpisana przez użytkownika"
    elif len(T) >= 3:
        kor = max(0.0, min(25.0, round((1 - statistics.median(T) / med_o) * 100, 1)))
        zr_kor = f"z {len(T)} cen transakcyjnych w teczce (mediana transakcji / mediana ofert)"
    else:
        kor, zr_kor = KOREKTA_OFERT_DOMYSLNA, "typowa różnica (brak cen transakcyjnych z okolicy w teczce)"
    cechy = cechy_wlasne(rz)
    wiersze, wagi = [], []
    for o in O:
        oc = o.get("oceny") or {}
        sk = 1.0
        rozn = 0
        for c, proc in cechy:
            st_ = max(-2, min(2, int(_f(oc.get(c), 0))))
            sk *= (1 - st_ * proc / 100)  # oferta lepsza (+) → jej cena w dół na tle wycenianej
            rozn += abs(st_)
        c_adj = _f(o["cena_m2"]) * (1 - kor / 100) * sk
        w = 1 / (1 + rozn)  # oferty bardziej podobne ważą więcej
        wiersze.append({"id": o["id"], "cena_m2": o["cena_m2"], "po_korekcie": round(c_adj, 2), "waga": round(w, 3), "rozn": rozn})
        wagi.append(w)
    cena_m2 = sum(x["po_korekcie"] * x["waga"] for x in wiersze) / sum(wagi)
    adj = sorted(x["po_korekcie"] for x in wiersze)
    q = statistics.quantiles(adj, n=4) if len(adj) >= 4 else [adj[0], statistics.median(adj), adj[-1]]
    cv = statistics.pstdev(adj) / statistics.mean(adj) if len(adj) > 1 else 0
    sr_rozn = statistics.mean(x["rozn"] for x in wiersze)
    pkt = (2 if len(O) >= 8 else 1 if len(O) >= 5 else 0) + (2 if cv < 0.08 else 1 if cv < 0.15 else 0) + (2 if sr_rozn <= 2 else 1 if sr_rozn <= 4 else 0)
    pewnosc = "wysoka" if pkt >= 5 else "średnia" if pkt >= 3 else "niska"
    return {"pow": P, "liczba": len(O), "mediana_ofert_m2": round(med_o, 2), "korekta_pct": kor, "zrodlo_korekty": zr_kor, "cena_m2": round(cena_m2, 2),
            "wartosc": round(cena_m2 * P, -3), "od": round(q[0] * P, -3), "do": round(q[2] * P, -3), "rozrzut_pct": round(cv * 100, 1),
            "pewnosc": pewnosc, "wiersze": wiersze, "cechy": cechy, "data": dt.date.today().isoformat()}


def raport_wlasna(sciezka, n):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    wl = n.get("wlasna") or {}
    w = wl.get("wynik") or {}
    d = MO._doc()
    MO._akapit(d, "WYCENA WŁASNA – SZACUNEK WARTOŚCI RYNKOWEJ", pogrub=True, rozmiar=15, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"{(n.get('dane') or {}).get('nazwa') or ''} – {opis_dzialek(n) if RODZAJ.get((n.get('dane') or {}).get('typ')) != 'lokal' else (n.get('dane') or {}).get('adres', '')}",
               wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, f"Stan na {w.get('data') or dt.date.today().isoformat()} · szacunek z danych rynkowych – NIE jest operatem szacunkowym", rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "1. Wynik", pogrub=True)
    MO._tabela(d, [["", ""], ["Najbardziej prawdopodobna wartość", MO.zl(w.get("wartosc", 0))], ["Przedział", f"{MO.zl(w.get('od', 0))} – {MO.zl(w.get('do', 0))}"],
                   ["Cena za m²", MO.zl(w.get("cena_m2", 0))], ["Pewność szacunku", f"{w.get('pewnosc', '')} ({w.get('liczba', 0)} ofert, rozrzut cen {w.get('rozrzut_pct', 0)}%)"]])
    MO._akapit(d, "2. Wyceniana nieruchomość", pogrub=True)
    MO._tabela(d, [["Cecha", "Wartość"]] + [[k, str(v)] for k, v in opis_przedmiotu(n).items()])
    MO._akapit(d, "3. Dane rynkowe – nieruchomości porównawcze", pogrub=True)
    O = {o["id"]: o for o in wl.get("oferty") or []}
    MO._tabela(d, [["Lp.", "Położenie", "Pow. [m²]", "Cena ofertowa", "zł/m²", "Po korektach zł/m²"]] +
               [[str(k), O[x['id']].get('lokalizacja') or "oferta rynkowa", f"{_f(O[x['id']].get('pow')):g}", MO.zl(_f(O[x['id']].get('cena'))),
                 MO.zl(x["cena_m2"]), MO.zl(x["po_korekcie"])] for k, x in enumerate([x for x in w.get("wiersze") or [] if x["id"] in O], 1)])
    MO._akapit(d, "4. Metoda", pogrub=True)
    MO._akapit(d, f"Metoda porównawcza na danych rynkowych (ceny ofertowe podobnych nieruchomości). Ceny ofertowe pomniejszone o {w.get('korekta_pct', 0):g}% (różnica oferta → transakcja; {w.get('zrodlo_korekty', '')}). "
                  "Każda oferta skorygowana o różnice cech na tle wycenianej nieruchomości: " + ", ".join(f"{c} – {p}% za stopień" for c, p in w.get("cechy") or []) +
                  ". Wynik to średnia ważona podobieństwem ofert; przedział – od pierwszego do trzeciego kwartyla cen po korektach.")
    MO._akapit(d, "Zastrzeżenia: szacunek opiera się na danych rynkowych – cenach ofertowych (nie transakcyjnych) i opisach ofert. Nie jest operatem szacunkowym w rozumieniu ustawy "
                  "o gospodarce nieruchomościami i nie zastępuje wyceny rzeczoznawcy majątkowego tam, gdzie jest wymagana (bank, sąd, urząd, podatki).", kursywa=True, rozmiar=8)
    d.save(sciezka)
