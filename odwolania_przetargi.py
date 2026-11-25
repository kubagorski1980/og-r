# -*- coding: utf-8 -*-
"""
Odwołania od przetargów – wykrywanie rozstrzygniętych przetargów (ponad próg wartości, co najmniej 2 oferty), w których wybór
da się podważyć, i firm z dalszych miejsc, które mogą wnieść odwołanie. (Nie mylić z odwolania.py – cytaty w analizach AI.)

Zasady:
- źródła: Platforma e-Zamówienia (API dokumentów) i inne platformy z informacjami jawnymi bez logowania; BIP – poza zakresem;
- termin odwołania od wyboru: 5 dni (poniżej progów unijnych) albo 10 dni (od progów) od przekazania informacji elektronicznie
  (art. 515 Pzp, sprawdzone 21.10.2026) – ogłoszenia z BZP to postępowania krajowe → domyślnie 5 dni; reżim zapisany w ocenie („unijne”)
  i użyty w pismach, wiadomościach i projekcie odwołania;
- wstępna ocena BEZ AI (wyliczenia sprawdzalne): rażąco niska cena (art. 224 ust. 2 pkt 1 – próg 30%), przeliczenie punktów za cenę
  i sum, odrzucone oferty tańsze od wybranej, status VAT wybranego wykonawcy, wybór po terminie związania ofertą (30 dni – art. 307,
  od progów UE 90/120 dni – art. 220 ust. 1); średnia z art. 224 ust. 2 pkt 1 bez ofert odrzuconych z art. 226 ust. 1 pkt 1, 5a i 10;
- AI tylko odczytuje dokumenty (informacja z otwarcia ofert, o kwocie, o wyborze) do danych;
- odwołanie może wnieść tylko wykonawca z interesem (art. 505 Pzp) – moduł wskazuje, KTO ma interes przy danym argumencie.
"""
import datetime as dt
import json
import os
import re
import shutil
import threading
import urllib.parse
import urllib.request
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

BLOKADA = threading.RLock()
PROG_DOMYSLNY = 1_000_000.0
DNI_OBSERWACJI = 75
DNI_ODWOLANIA_KRAJOWE = 5
DNI_ODWOLANIA_UNIJNE = 10
RE_OTWARCIE = re.compile(r"(?i)otwarci")
RE_KWOTA = re.compile(r"(?i)kwot\w*\W+przeznacz|kwot\w*\W+jak[aą]|informacj\w*\W+o\W+kwocie")
RE_WYBOR = re.compile(r"(?i)wyb[oó]r|zawiadomieni|rozstrzygni|o\W+wyniku|uniewa[zż]ni")
RE_UNIEWAZN = re.compile(r"(?i)uniewa[zż]ni")


def rodzaj_dokumentu(nazwa):
    n = str(nazwa or "")
    if RE_OTWARCIE.search(n):
        return "otwarcie"
    if RE_WYBOR.search(n):
        return "uniewaznienie" if RE_UNIEWAZN.search(n) and not re.search(r"(?i)wyb[oó]r", n) else "wybor"
    if RE_KWOTA.search(n):
        return "kwota"
    return None


RE_NIE_ROZSTRZYGNIECIE = re.compile(r"(?i)swz|specyfikacj|za[lł][aą]cznik|przedmiar|stwior|stwiorb|projekt|kosztorys|umow|formularz|wz[oó]r|"
                                    r"opis[ _-]*przedmiotu|opz|pytani|wyja[sś]nieni|zmian|ogloszeni|ogłoszeni")
RE_TRESC = [("uniewaznienie", re.compile(r"(?i)uniewa[zż]ni\w*\s+post[eę]powani")),
            ("wybor", re.compile(r"(?i)wyb[oó]r\w*\s+(najkorzystniejszej\s+)?ofert|najkorzystniejsz\w+\s+ofert|zawiadomieni\w*\s+o\s+wyborze")),
            ("otwarcie", re.compile(r"(?i)informacj\w*\s+z\s+otwarcia\s+ofert|zestawieni\w*\s+(złożonych\s+)?ofert")),
            ("kwota", re.compile(r"(?i)kwot\w*[,\s]+jak[aą]\s+(zamawiaj[aą]cy\s+)?zamierza\s+przeznaczy|kwot\w*\s+przeznaczon"))]


def do_sprawdzenia_tresci(nazwa):
    """Plik o nieopisowej nazwie (np. GUID), który może być dokumentem rozstrzygnięcia – do rozpoznania po treści."""
    n = (nazwa or "").lower()
    return n.endswith((".pdf", ".doc", ".docx")) and not RE_NIE_ROZSTRZYGNIECIE.search(n)


RE_NIE_TYTUL = re.compile(r"(?i)og[lł]oszeni\w*\s+o\s+(zam[oó]wieniu|wyniku|zmianie|wykonaniu)|specyfikacj\w*\s+warunk|SWZ\b")


def rodzaj_z_tresci(tekst):
    """Rodzaj dokumentu z jego NAGŁÓWKA (tytuł na początku) – nie z całej treści: ogłoszenie i SWZ też zawierają zwroty
    „termin otwarcia ofert” czy „wybór najkorzystniejszej oferty”, ale w nagłówku mają swój tytuł."""
    glowa = re.sub(r"\s+", " ", (tekst or "")[:1200])
    if RE_NIE_TYTUL.search(glowa):
        return None
    for r, rx in RE_TRESC:
        if rx.search(glowa):
            return r
    return None


WYSZ_DOMYSLNE = {"region": "jak_przetargi", "wojewodztwa": [], "rodzaje": ["roboty", "dostawy", "uslugi"], "slowa": "", "dni": 45}
RODZAJE = {"roboty": "Roboty budowlane", "dostawy": "Dostawy", "uslugi": "Usługi"}


def rodzaj_z_bzp(tekst):
    """Rodzaj zamówienia z ogłoszenia BZP (orderType: Works / Supplies / Services albo nazwa polska)."""
    t = str(tekst or "").lower()
    if re.search(r"dostaw|deliver|suppl", t):
        return "dostawy"
    if re.search(r"usług|uslug|servic", t):
        return "uslugi"
    if re.search(r"robot|works|budow", t):
        return "roboty"
    return ""


def pasuje_slowa(przedmiot, slowa):
    sl = [s.strip().lower() for s in re.split(r"[,;\n]", slowa or "") if s.strip()]
    p = str(przedmiot or "").lower()
    return not sl or any(s in p for s in sl)


def bezpieczny(nr):
    return re.sub(r"[^\w.-]+", "_", str(nr))[:80]


class Baza:
    """Wspólne dane modułu (katalog w /data), zapis atomowy, kopie poprzednich wersji, bez cichego nadpisywania."""
    def __init__(self, katalog):
        self.kat = katalog
        self.pliki = os.path.join(katalog, "pliki")

    def _sc(self, n):
        return os.path.join(self.kat, n)

    def czytaj(self, n, dom):
        sc = self._sc(n)
        if not os.path.exists(sc):
            return dom
        try:
            with open(sc, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError) as e:
            kd = os.path.join(self.kat, "kopie")
            for k in sorted((os.path.join(kd, f) for f in os.listdir(kd) if f.startswith(n + ".")), reverse=True) if os.path.isdir(kd) else []:
                try:
                    with open(k, encoding="utf-8") as f:
                        return json.load(f)
                except (OSError, ValueError):
                    continue
            raise RuntimeError(f"Plik modułu odwołań „{n}” jest nieczytelny ({e}) i nie ma kopii – program go nie nadpisze.")

    def pisz(self, n, dane):
        os.makedirs(self.kat, exist_ok=True)
        sc = self._sc(n)
        if os.path.exists(sc):
            kd = os.path.join(self.kat, "kopie")
            os.makedirs(kd, exist_ok=True)
            shutil.copy2(sc, os.path.join(kd, f"{n}.{dt.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"))
            for f in sorted(x for x in os.listdir(kd) if x.startswith(n + "."))[:-20]:
                try:
                    os.remove(os.path.join(kd, f))
                except OSError:
                    pass
        with open(sc + ".tmp", "w", encoding="utf-8") as f:
            json.dump(dane, f, ensure_ascii=False, indent=1)
        os.replace(sc + ".tmp", sc)

    def postepowania(self):
        return self.czytaj("postepowania.json", {})

    def zapisz_postepowania(self, P):
        self.pisz("postepowania.json", P)

    def ustawienia(self):
        u = {"prog": PROG_DOMYSLNY, **self.czytaj("ustawienia.json", {})}
        u["wyszukiwanie"] = {**WYSZ_DOMYSLNE, **(u.get("wyszukiwanie") or {})}
        return u


def _nazwa_z_naglowka(cd):
    m = re.search(r"filename\*\s*=\s*UTF-8''([^;]+)", cd or "", re.I)
    if m:
        return urllib.parse.unquote(m.group(1)).strip('"')
    m = re.search(r'filename\s*=\s*"?([^";]+)"?', cd or "", re.I)
    return m.group(1).strip() if m else ""


def dokumenty_ocds(ocds, od_n=1, max_n=150, otworz=None):
    """Lista dokumentów postępowania na e-Zamówieniach (nr, nazwa, adres) – tylko nagłówki, bez pobierania treści."""
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Bidivia)"}), timeout=40))
    wyn, braki = [], 0
    for n in range(max(1, od_n), max_n + 1):
        url = f"https://ezamowienia.gov.pl/mp-readmodels/api/Tender/DownloadDocument/{ocds}/{ocds}_{n}"
        try:
            r = otworz(url)
            nazwa = _nazwa_z_naglowka(r.headers.get("Content-Disposition")) or f"dokument_{n}"
            r.close()
            wyn.append({"n": n, "nazwa": nazwa, "url": url})
            braki = 0
        except Exception as e:
            kod = getattr(e, "code", None)
            if kod in (403, 429, 503):
                raise RuntimeError(f"Platforma e-Zamówienia odpowiedziała {kod} (możliwa przerwa techniczna) – ponowię przy następnym sprawdzeniu.")
            braki += 1
            if braki >= 6:  # numeracja dokumentów na platformie bywa dziurawa (usunięte pliki)
                break
    return wyn


def stan_ez(ocds, otworz=None):
    """Stan postępowania z publicznego API e-Zamówień (działa dla każdego ogłoszenia BZP, także prowadzonego na innej platformie):
    etap, unieważnienie, czy prowadzone na e-Zamówieniach, kwota przeznaczona (gdy opublikowana), województwo zamawiającego."""
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Bidivia)", "Accept": "application/json"}), timeout=30))
    with otworz(f"https://ezamowienia.gov.pl/mp-readmodels/api/Search/GetTender?id={ocds}") as r:
        d = json.loads(r.read().decode("utf-8"))
    kw = d.get("amountToFinanced") if d.get("isAmountToFinancedPublished") else None
    return {"etap": d.get("stage") or "", "stan": d.get("state") or "", "na_platformie": bool(d.get("isProceedingOnPlatform")),
            "kwota": _f(kw), "wojewodztwo": str(d.get("organizationProvince") or "").lower(), "uniewaznione": d.get("cancellationDate"),
            "ponizej_progow_ue": d.get("isTenderAmountBelowEU"), "sprawdzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}


ETAPY = {"CollectingOffers": "składanie ofert", "ExaminationOffer": "badanie i ocena ofert", "ExaminationOffers": "badanie i ocena ofert", "CompletedContract": "umowa zawarta",
         "CompletedInvalid": "unieważnione", "Invalidated": "unieważnione"}
RE_PROFIL_OGOLNY = re.compile(r"(?i)platformazakupowa\.pl/pn/[^/?#]+/?$|/rejestracja/|/instrukcj|/regulamin|^https?://[^/]+/?$")


def platformy_z_ogloszenia(adresy):
    """Adresy postępowania z ogłoszenia: bez e-Zamówień i BIP; najpierw konkretne postępowanie, potem ogólne profile zamawiającego."""
    L = [u for u in adresy or [] if "ezamowienia.gov.pl" not in u and not re.search(r"(?i)//(www\.)?bip\.|\.bip\.|/bip/", u)]
    return sorted(dict.fromkeys(L), key=lambda u: (bool(RE_PROFIL_OGOLNY.search(u)), not re.search(r"\d{4,}", u)))


def etap_opis(e):
    e = str(e or "")
    if e in ETAPY:
        return ETAPY[e]
    if "Invalid" in e:
        return "unieważnione"
    return e


SYSTEM_ODCZYT = ("Odczytujesz dokumenty zamawiającego z postępowania o udzielenie zamówienia publicznego (informacja z otwarcia ofert, "
                 "informacja o kwocie, informacja o wyborze najkorzystniejszej oferty, unieważnienie). Przepisujesz dokładnie, nie zgadujesz. "
                 "Kwoty jako liczby (kropka dziesiętna), daty RRRR-MM-DD. Odpowiadasz wyłącznie JSON-em.")

POLECENIE_ODCZYT = """Z dokumentów powyżej odczytaj dane postępowania. Gdy zamówienie ma części – osobny wpis dla każdej części.
Zwróć JSON:
{"czesci": [{"czesc": "numer części albo null",
  "kwota_przeznaczona": liczba brutto albo null,
  "oferty": [{"wykonawca": "nazwa", "adres": "…", "nip": "cyfry albo null", "cena_brutto": liczba albo null,
              "inne_kryteria": {"nazwa kryterium": "zaoferowana wartość"}}],
  "wybor": null albo {"data_informacji": "RRRR-MM-DD", "wybrany": "nazwa wykonawcy",
       "kryteria": [{"nazwa": "Cena", "waga": 60}],
       "ranking": [{"miejsce": 1, "wykonawca": "…", "nip": "…", "adres": "…", "cena_brutto": liczba,
                    "punkty": {"nazwa kryterium": liczba}, "suma": liczba}],
       "odrzucone": [{"wykonawca": "…", "nip": "…", "cena_brutto": liczba albo null, "podstawa": "art. …", "uzasadnienie": "krótko"}],
       "wezwano_do_wyjasnien_ceny": true / false / null,
       "uzasadnienie_wyboru": "krótko"},
  "uniewaznienie": null albo {"data": "RRRR-MM-DD", "podstawa": "…"}}]}
Gdy dokumentu o wyborze nie ma – "wybor": null. Nie wymyślaj danych, których w dokumentach nie ma."""


def _f(x):
    return liczba(x, None, 2)


def _norm(s):
    return re.sub(r"[^a-z0-9ąćęłńóśźż]+", " ", str(s or "").lower()).strip()


def _ten_sam(a, b):
    a, b = _norm(a), _norm(b)
    return bool(a) and bool(b) and (a == b or a[:25] == b[:25])


def wartosc_czesci(c):
    ceny = [_f(o.get("cena_brutto")) for o in c.get("oferty") or [] if _f(o.get("cena_brutto"))]
    w = c.get("wybor") or {}
    ceny += [_f(r.get("cena_brutto")) for r in w.get("ranking") or [] if _f(r.get("cena_brutto"))]
    return _f(c.get("kwota_przeznaczona")) or (max(ceny) if ceny else None)


# sposób przekazania informacji o wyborze (art. 515 ust. 1 Pzp): lit. a – środkami komunikacji elektronicznej, lit. b – w inny sposób
SPOSOBY_PRZEKAZANIA = {"elektronicznie": "środkami komunikacji elektronicznej", "inny": "w inny sposób (np. pocztą, osobiście)"}


def _sposob(s):
    return "inny" if s == "inny" else "elektronicznie"


def dni_odwolania(unijne=False, sposob="elektronicznie"):
    """Art. 515 ust. 1 Pzp (tekst ustawy sprawdzony w pzp.txt): od progów unijnych – 10 dni (pkt 1 lit. a, elektronicznie) albo 15 dni
    (pkt 1 lit. b, w inny sposób); poniżej progów – 5 dni (pkt 2 lit. a) albo 10 dni (pkt 2 lit. b). Liczone od dnia przekazania informacji."""
    inny = _sposob(sposob) == "inny"
    if unijne:
        return 15 if inny else DNI_ODWOLANIA_UNIJNE
    return 10 if inny else DNI_ODWOLANIA_KRAJOWE


def przepis_terminu(unijne=False, sposob="elektronicznie"):
    return f"art. 515 ust. 1 pkt {'1' if unijne else '2'} lit. {'b' if _sposob(sposob) == 'inny' else 'a'} Pzp"


def opis_terminu(unijne=False, sposob="elektronicznie"):
    """Opis terminu do pism i ekranów – zgodny z reżimem postępowania i sposobem przekazania informacji (art. 515 ust. 1 pkt 1/2 lit. a/b Pzp)."""
    jak = ("środkami komunikacji elektronicznej" if _sposob(sposob) != "inny"
           else "w inny sposób niż środkami komunikacji elektronicznej")
    return (f"{dni_odwolania(unijne, sposob)} dni od przekazania informacji o wyborze {jak} – {przepis_terminu(unijne, sposob)} "
            + ("(zamówienie od progów unijnych)" if unijne else "(zamówienie poniżej progów unijnych)"))


def wpis_odwolania(przedmiot="roboty", unijne=False):
    """Wpis od odwołania – § 2 ust. 1 rozporządzenia Prezesa Rady Ministrów z 31.12.2020 r. (Dz.U. 2020 poz. 2437):
    dostawy i usługi 7 500 zł / 15 000 zł, roboty budowlane 10 000 zł / 20 000 zł (poniżej / od progów unijnych)."""
    roboty = (przedmiot or "roboty") == "roboty"
    return (20000 if roboty else 15000) if unijne else (10000 if roboty else 7500)


def _pl(x, miejsca=2):
    import progi as PR
    return PR.liczba_pl(x, miejsca)


def _pkt(x):
    """Punkty po polsku: 45 → „45”, 39.13 → „39,13”."""
    try:
        x = float(x)
    except (TypeError, ValueError):
        return str(x)
    return _pl(x, 0) if abs(x - round(x)) < 0.005 else _pl(x, 2)


def termin_odwolania(data_info, unijne=False, dzis=None, sposob="elektronicznie"):
    """data_info – dzień przekazania informacji o wyborze; termin = ten dzień + 5/10/15 dni (art. 515 ust. 1, art. 509 ust. 1 Pzp i art. 111 § 2 KC)."""
    if not data_info:
        return None, None
    try:
        d0 = dt.date.fromisoformat(str(data_info)[:10])
    except ValueError:
        return None, None
    koniec = d0 + dt.timedelta(days=dni_odwolania(unijne, sposob))
    import progi as PR
    koniec = PR.koniec_terminu(koniec)  # sobota, niedziela albo dzień ustawowo wolny → następny dzień roboczy (art. 509 ust. 2 Pzp)
    return koniec.isoformat(), (koniec - (dzis or dt.date.today())).days


def zwiazanie_oferta(unijne=False, wartosc_brutto=None, rodzaj=None):
    """Najdłuższy termin związania ofertą (dni, przepis, dopisek): tryb podstawowy – 30 dni (art. 307 ust. 1); od progów unijnych – 90 dni
    (art. 220 ust. 1 pkt 1), a 120 dni (pkt 2), gdy wartość robót ≥ 20 000 000 euro, dostaw lub usług ≥ 10 000 000 euro. Wartość w module Odwołań
    to kwota przeznaczona lub najwyższa cena (brutto) – przeliczona na netto (÷ 1,23) i euro po kursie z progi.KURS_EURO, więc tylko szacunkowo."""
    if not unijne:
        return 30, "art. 307 ust. 1 Pzp", ""
    import progi as PR
    granica = 20_000_000 if (rodzaj or "roboty") == "roboty" else 10_000_000
    w = _f(wartosc_brutto)
    if w and w / 1.23 / PR.KURS_EURO >= granica:
        return 120, "art. 220 ust. 1 pkt 2 Pzp", f" – wartość ok. {_pl(w / 1.23 / PR.KURS_EURO, 0)} euro netto, od {_pl(granica, 0)} euro"
    return 90, "art. 220 ust. 1 pkt 1 Pzp", (f"; 120 dni, gdy wartość zamówienia wynosi co najmniej {_pl(granica, 0)} euro (art. 220 ust. 1 pkt 2)"
                                             if not w else "")


# Art. 224 ust. 2 pkt 1 Pzp: średnia arytmetyczna cen wszystkich złożonych ofert NIEPODLEGAJĄCYCH ODRZUCENIU na podstawie art. 226 ust. 1
# pkt 1, 5a i 10 (tekst ustawy w pzp.txt; pkt 5a – oferty wykonawców z państw trzecich, dodany nowelizacją). Oferty odrzucone z innych
# podstaw (np. pkt 2, 5, 8) wchodzą do średniej.
PKT_POMIJANE_224 = ("1", "5a", "10")
_RE_PKT_226 = re.compile(r"(?i)226\s*ust\.?\s*1\s*(?:pkt|punkt\w*)\.?\s*")
_RE_PKT_JEDEN = re.compile(r"(?i)(\d{1,2})([a-z])?(?![a-ząćęłńóśźż])(?:\s*lit\.?\s*[a-z]\)?)?")
_RE_PKT_SEP = re.compile(r"(?i)\s*(?:,|i|oraz|lub|albo|bądź)\s+(?:pkt\.?\s*)?|\s*,\s*(?:pkt\.?\s*)?")


def _punkty_226(t):
    """Numery punktów art. 226 ust. 1 wskazane w tekście: „art. 226 ust. 1 pkt 2 lit. a i pkt 10” → ["2", "10"]."""
    pkt = []
    for m in _RE_PKT_226.finditer(t):
        i = m.end()
        while True:
            j = _RE_PKT_JEDEN.match(t, i)
            if not j:
                break
            pkt.append(j.group(1) + (j.group(2) or "").lower())
            i = j.end()
            s_ = _RE_PKT_SEP.match(t, i)
            if not s_ or not _RE_PKT_JEDEN.match(t, s_.end()):
                break
            i = s_.end()
    return pkt


def podstawa_odrzucenia_224(podstawa, uzasadnienie=""):
    """Czy oferta odrzucona wchodzi do średniej z art. 224 ust. 2 pkt 1: „pomijana” (art. 226 ust. 1 pkt 1, 5a albo 10),
    „uwzgledniana” (inny wskazany punkt art. 226 ust. 1 albo art. 224 ust. 6) albo None – podstawa nieznana / niepewna."""
    t = f"{podstawa or ''} {uzasadnienie or ''}"
    pkt = _punkty_226(t)
    if pkt:
        return "pomijana" if any(p in PKT_POMIJANE_224 for p in pkt) else "uwzgledniana"
    if re.search(r"(?i)224\s*ust\.?\s*6", t):  # rażąco niska cena – odrzucenie jak z art. 226 ust. 1 pkt 8
        return "uwzgledniana"
    return None


def srednia_224(c, odrzucone, oferty, ranking):
    """Ceny do średniej z art. 224 ust. 2 pkt 1: wariant „pewny” albo – gdy podstawa odrzucenia którejś oferty jest nieznana – dwa wyliczenia
    (z tymi ofertami i bez nich). Zwraca {"warianty": [(opis, [ceny])], "pominiete": [...], "niepewne": [...], "uwzglednione_odrzucone": [...]}."""
    klas = {_norm(x.get("wykonawca")): (x.get("wykonawca"), podstawa_odrzucenia_224(x.get("podstawa"), x.get("uzasadnienie"))) for x in odrzucone or []}
    baza = [(_norm(o.get("wykonawca")), _f(o.get("cena_brutto"))) for o in (oferty or ranking) if _f(o.get("cena_brutto"))]
    znane = {n for n, _ in baza}
    if not oferty:  # bez informacji z otwarcia: odrzucone spoza rankingu (z ceną) też są „złożonymi ofertami”
        baza += [(_norm(x.get("wykonawca")), _f(x.get("cena_brutto"))) for x in odrzucone or []
                 if _f(x.get("cena_brutto")) and _norm(x.get("wykonawca")) not in znane]
    pom = {n for n, (_, k) in klas.items() if k == "pomijana"}
    niep = {n for n, (_, k) in klas.items() if k is None and n in {b for b, _ in baza}}
    ceny_z = [p for n, p in baza if n not in pom]
    ceny_bez = [p for n, p in baza if n not in pom and n not in niep]
    war = [("z ofertami odrzuconymi z nieustalonej podstawy", ceny_z), ("bez ofert odrzuconych z nieustalonej podstawy", ceny_bez)] if niep else [("", ceny_z)]
    return {"warianty": war, "pominiete": [klas[n][0] for n in pom], "niepewne": [klas[n][0] for n in niep],
            "uwzglednione_odrzucone": [w_ for n, (w_, k) in klas.items() if k == "uwzgledniana"]}


def ocen_czesc(c, prog=PROG_DOMYSLNY, termin_ofert=None, status_vat=None, unijne=False, dzis=None, przekazanie=None, rodzaj=None):
    """Argumenty za podważeniem wyboru w jednej części – każdy: typ, siła, opis, podstawa, kto ma interes (art. 505 Pzp).
    przekazanie – {"data": RRRR-MM-DD, "sposob": "elektronicznie"|"inny"} wpisane przez użytkownika (art. 515 ust. 1 lit. a/b);
    bez daty termin liczony od daty informacji o wyborze z dokumentu."""
    import rynkowosc as RY
    w = c.get("wybor")
    oferty = c.get("oferty") or []
    pk = przekazanie if isinstance(przekazanie, dict) else {}
    sposob = _sposob(pk.get("sposob"))
    wynik = {"wartosc": wartosc_czesci(c), "liczba_ofert": max(len(oferty), len((w or {}).get("ranking") or [])), "argumenty": [], "firmy": [], "status": "",
             "unijne": bool(unijne), "data_informacji": str((w or {}).get("data_informacji") or "")[:10] or None,
             "sposob_przekazania": sposob, "data_przekazania": str(pk.get("data") or "")[:10] or None}
    wynik["termin_od"] = "data przekazania (wpisana)" if wynik["data_przekazania"] else "data informacji o wyborze z dokumentu – sprawdź datę przekazania"
    wynik["opis_terminu"] = opis_terminu(unijne, sposob)
    wynik["oferenci"] = oferenci(c)
    if wynik["wartosc"] is not None and wynik["wartosc"] < prog:
        wynik["status"] = "poniżej progu wartości"
        return wynik
    if c.get("uniewaznienie"):
        wynik["status"] = "unieważnione"
        return wynik
    if wynik["liczba_ofert"] < 2:
        wynik["status"] = "jedna oferta" if wynik["liczba_ofert"] == 1 else "czeka na informację z otwarcia ofert"
        return wynik
    if not w:
        wynik["status"] = "czeka na wybór oferty"
        return wynik
    ranking = sorted(w.get("ranking") or [], key=lambda r: r.get("miejsce") or 99)
    wyb = next((r for r in ranking if _ten_sam(r.get("wykonawca"), w.get("wybrany"))), ranking[0] if ranking else None)
    A = wynik["argumenty"]
    druga = next((r for r in ranking if r is not wyb), None)
    interes_2 = f"{druga['wykonawca']} (miejsce {druga.get('miejsce') or 2})" if druga else "wykonawca z 2. miejsca"
    cena_w = _f((wyb or {}).get("cena_brutto")) or next((_f(o.get("cena_brutto")) for o in oferty if wyb and _ten_sam(o.get("wykonawca"), wyb.get("wykonawca"))), None)
    odrz = {_norm(x.get("wykonawca")) for x in w.get("odrzucone") or []}  # oferty odrzucone nie są oceniane w kryteriach (punktacja, ranking)
    # średnia z art. 224 ust. 2 pkt 1: pomijane tylko oferty odrzucone na podstawie art. 226 ust. 1 pkt 1, 5a i 10; przy nieznanej podstawie – dwa wyliczenia
    sr = srednia_224(c, w.get("odrzucone"), oferty, ranking)
    wynik["srednia_224"] = {"pominiete": sr["pominiete"], "niepewne": sr["niepewne"], "uwzglednione_odrzucone": sr["uwzglednione_odrzucone"], "warianty": []}
    wyl = [(op, RY.prog_224(cena_w, None, ceny)) for op, ceny in sr["warianty"] if cena_w and len(ceny) >= 2]
    for op, p in wyl:
        wynik["srednia_224"]["warianty"].append({"opis": op, "srednia": p.get("srednia"), "obowiazkowe": p["obowiazkowe"], "liczba_ofert": len(dict(sr["warianty"])[op])})
    if any(p["obowiazkowe"] for _, p in wyl):
        wez = w.get("wezwano_do_wyjasnien_ceny")
        oba = all(p["obowiazkowe"] for _, p in wyl)
        if len(wyl) > 1:
            opis_ = ("Dwa wyliczenia średniej – podstawa odrzucenia ofert: " + ", ".join(sr["niepewne"]) + " nie jest pewna (do średniej nie wlicza się "
                     "tylko ofert odrzuconych na podstawie art. 226 ust. 1 pkt 1, 5a i 10). "
                     + " ".join(f"Wyliczenie {i} ({op}, średnia {_pl(p['srednia'])} zł): {'próg 30% przekroczony' if p['obowiazkowe'] else 'próg 30% nieprzekroczony'}."
                                for i, (op, p) in enumerate(wyl, 1)) + " " + next(p["opis"] for _, p in wyl if p["obowiazkowe"]))
        else:
            opis_ = wyl[0][1]["opis"]
        if sr["pominiete"]:
            opis_ += " Pominięto w średniej oferty odrzucone na podstawie art. 226 ust. 1 pkt 1, 5a lub 10: " + ", ".join(sr["pominiete"]) + "."
        if sr["uwzglednione_odrzucone"]:
            opis_ += " Uwzględniono oferty odrzucone z innych podstaw: " + ", ".join(sr["uwzglednione_odrzucone"]) + "."
        A.append({"typ": "rażąco niska cena", "sila": ("silny" if wez is False else "do sprawdzenia") if oba else "do sprawdzenia",
                  "opis": opis_ + (" Z dokumentów wynika, że zamawiający NIE wezwał do wyjaśnień." if wez is False else
                                   " Sprawdź (wniosek o protokół), czy zamawiający wezwał do wyjaśnień i czy ocenił je zasadnie."),
                  "podstawa": "art. 224 ust. 2 pkt 1, art. 226 ust. 1 pkt 8 Pzp", "interes": interes_2, "dwa_wyliczenia": len(wyl) > 1})
    kw = _f(c.get("kwota_przeznaczona"))
    if cena_w and kw and cena_w <= 0.7 * kw:
        A.append({"typ": "cena znacznie poniżej kwoty zamawiającego", "sila": "średni",
                  "opis": (f"Cena wybranej oferty {_pl(cena_w)} zł to {cena_w / kw * 100:.0f}% kwoty przeznaczonej na zamówienie ({_pl(kw)} zł). "
                           "Kwota przeznaczona nie jest wartością zamówienia z art. 224 – argument pomocniczy."),
                  "podstawa": "art. 224 ust. 1 Pzp", "interes": interes_2})
    kc = next((k for k in w.get("kryteria") or [] if re.search(r"(?i)cen|koszt", str(k.get("nazwa")))), None)
    if kc and _f(kc.get("waga")):
        wg = _f(kc["waga"])
        ceny_r = [_f(r.get("cena_brutto")) for r in ranking if _f(r.get("cena_brutto")) and _norm(r.get("wykonawca")) not in odrz]
        cmin = min(ceny_r) if ceny_r else None
        poprawione = []
        for r in ranking:
            c_r = _f(r.get("cena_brutto"))
            pk = next((_f(v) for k, v in (r.get("punkty") or {}).items() if re.search(r"(?i)cen|koszt", k)), None)
            if cmin and c_r and pk is not None:
                ocz = round(cmin / c_r * wg, 2)
                if abs(ocz - pk) > 0.05:
                    poprawione.append((r, pk, ocz))
        if poprawione:
            sumy = {}
            for r in ranking:
                s = _f(r.get("suma")) or sum(_f(v) or 0 for v in (r.get("punkty") or {}).values())
                pop = next((x for x in poprawione if x[0] is r), None)
                sumy[r.get("wykonawca")] = round(s - pop[1] + pop[2], 2) if pop else s
            nowy_1 = max(sumy, key=sumy.get) if sumy else None
            zmienia = bool(nowy_1 and wyb and not _ten_sam(nowy_1, wyb.get("wykonawca")))
            A.append({"typ": "błąd w punktacji za cenę", "sila": "silny" if zmienia else "średni",
                      "opis": "; ".join(f"{r['wykonawca']}: przyznano {_pkt(pk)} pkt, wzór (cena najniższa / cena oferty × {_pkt(wg)}) daje {_pkt(ocz)} pkt" for r, pk, ocz in poprawione)
                              + (f". Po poprawce najwyżej oceniona jest oferta: {nowy_1}." if zmienia else ". Poprawka nie zmienia kolejności."),
                      "podstawa": "art. 239 ust. 1, art. 16 Pzp (ocena zgodna z kryteriami)", "interes": nowy_1 if zmienia else interes_2})
    s_wyb = _f((wyb or {}).get("suma"))
    lepsza = max((r for r in ranking if r is not wyb and _f(r.get("suma")) is not None and _norm(r.get("wykonawca")) not in odrz),
                 key=lambda r: _f(r.get("suma")), default=None)
    if s_wyb is not None and lepsza and _f(lepsza["suma"]) > s_wyb + 0.05:  # zamawiający wybiera ofertę najkorzystniejszą według kryteriów (art. 239 ust. 1)
        A.append({"typ": "wybrana oferta nie ma najwyższej liczby punktów", "sila": "silny",
                  "opis": f"Według informacji o wyborze oferta {lepsza['wykonawca']} uzyskała {_pkt(lepsza['suma'])} pkt, a wybrana oferta "
                          f"{wyb.get('wykonawca')} – {_pkt(s_wyb)} pkt. Sprawdź, czy ofertę z wyższą punktacją odrzucono (dokumenty tego nie podają).",
                  "podstawa": "art. 239 ust. 1, art. 16 pkt 1 Pzp", "interes": lepsza["wykonawca"]})
    for r in ranking:
        pk = [_f(v) for v in (r.get("punkty") or {}).values() if _f(v) is not None]
        if pk and _f(r.get("suma")) is not None and abs(sum(pk) - _f(r["suma"])) > 0.05:
            A.append({"typ": "błąd w sumie punktów", "sila": "średni",
                      "opis": f"{r['wykonawca']}: suma punktów w kryteriach {_pkt(sum(pk))}, w informacji o wyborze {_pkt(r['suma'])}.",
                      "podstawa": "art. 239 Pzp", "interes": interes_2})
    for x in w.get("odrzucone") or []:
        cx = _f(x.get("cena_brutto")) or next((_f(o.get("cena_brutto")) for o in oferty if _ten_sam(o.get("wykonawca"), x.get("wykonawca"))), None)
        if cena_w and cx and cx < cena_w:
            A.append({"typ": "odrzucona oferta tańsza od wybranej", "sila": "do sprawdzenia",
                      "opis": (f"{x['wykonawca']} – oferta {_pl(cx)} zł (wybrana {_pl(cena_w)} zł) odrzucona: {x.get('podstawa') or ''} {x.get('uzasadnienie') or ''}").strip()
                              + ". Oceń, czy podstawa odrzucenia jest zasadna.",
                      "podstawa": x.get("podstawa") or "art. 226 Pzp", "interes": x["wykonawca"]})
    if status_vat and status_vat not in ("Czynny", "?"):
        A.append({"typ": "status VAT wybranego wykonawcy", "sila": "do sprawdzenia",
                  "opis": f"Wykaz podatników VAT (biała lista): {status_vat}. Sprawdź, czy ma to znaczenie dla warunków udziału lub podstaw wykluczenia w SWZ.",
                  "podstawa": "art. 109 Pzp (jeśli przewidziano w SWZ)", "interes": interes_2})
    if termin_ofert and w.get("data_informacji"):
        try:
            dni = (dt.date.fromisoformat(w["data_informacji"][:10]) - dt.date.fromisoformat(str(termin_ofert)[:10])).days
        except ValueError:
            dni = None
        if dni is not None:
            limit, przepis, dop = zwiazanie_oferta(unijne, wynik["wartosc"], rodzaj)
            # pierwszym dniem terminu związania jest dzień upływu terminu składania ofert (art. 220 ust. 1 / art. 307 ust. 1) – ostatni: termin + (limit − 1)
            if dni >= limit:
                A.append({"typ": f"wybór po upływie {limit} dni od terminu ofert", "sila": "do sprawdzenia",
                          "opis": (f"Informację o wyborze przekazano {dni} dni po terminie składania ofert, a związanie ofertą trwa najwyżej {limit} dni "
                                   f"(pierwszy dzień – dzień upływu terminu składania ofert; {przepis}){dop}. Sprawdź termin związania ofertą w SWZ i czy go "
                                   f"przedłużono – jednokrotnie, o najwyżej {60 if unijne else 30} dni, za pisemną zgodą wykonawców "
                                   f"({'art. 220 ust. 3 i 4' if unijne else 'art. 307 ust. 2 i 3'} Pzp); wybór oferty po upływie terminu wymaga zgody wybranego wykonawcy "
                                   "(art. 226 ust. 1 pkt 12 i 13 Pzp)."),
                          "podstawa": f"{przepis}" if unijne else "art. 307 Pzp", "interes": interes_2})
    for r in ranking:
        if r is wyb:
            continue
        o_ = next((o for o in oferty if _ten_sam(o.get("wykonawca"), r.get("wykonawca"))), {})
        wynik["firmy"].append({"wykonawca": r.get("wykonawca"), "nip": r.get("nip") or o_.get("nip"), "adres": r.get("adres") or o_.get("adres"),
                               "miejsce": r.get("miejsce"), "cena_brutto": _f(r.get("cena_brutto")), "suma": _f(r.get("suma")),
                               "priorytet": "wysoki" if r is druga else "niski – musi podważyć także wyżej ocenione oferty"})
    for x in w.get("odrzucone") or []:
        if any(a["interes"] == x.get("wykonawca") for a in A):
            o_ = next((o for o in oferty if _ten_sam(o.get("wykonawca"), x.get("wykonawca"))), {})
            wynik["firmy"].append({"wykonawca": x.get("wykonawca"), "nip": x.get("nip") or o_.get("nip"), "adres": o_.get("adres"), "miejsce": "odrzucona",
                                   "cena_brutto": _f(x.get("cena_brutto")) or _f(o_.get("cena_brutto")), "priorytet": "wysoki – odwołanie od odrzucenia"})
    A.sort(key=lambda a: {"silny": 0, "średni": 1}.get(a["sila"], 2))  # najmocniejsze argumenty najpierw (ekran, notatka, e-mail – pierwsze 4)
    wynik["wybrany"] = {"wykonawca": (wyb or {}).get("wykonawca"), "nip": (wyb or {}).get("nip"), "cena_brutto": cena_w}
    wynik["termin_odwolania"], wynik["dni_do_terminu"] = termin_odwolania(wynik["data_przekazania"] or w.get("data_informacji"), unijne, dzis, sposob)
    sily = [a["sila"] for a in A]
    if wynik["dni_do_terminu"] is not None and wynik["dni_do_terminu"] < 0:
        wynik["status"] = "termin odwołania minął"
    elif "silny" in sily or "średni" in sily:
        wynik["status"] = "możliwy do podważenia"
    elif sily:
        wynik["status"] = "do sprawdzenia"
    else:
        wynik["status"] = "bez zarzutów z danych publicznych"
    wynik["sila"] = "silny" if "silny" in sily else "średni" if "średni" in sily else "do sprawdzenia" if sily else ""
    return wynik


def status_vat_nip(nip, otworz=None):
    """Biała lista VAT (API Ministerstwa Finansów): statusVat, „brak w wykazie” albo „?” przy braku odpowiedzi."""
    nip = re.sub(r"\D", "", str(nip or ""))
    if len(nip) != 10:
        return None
    url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={dt.date.today().isoformat()}"
    try:
        otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Bidivia"}), timeout=20))
        r = otworz(url)
        d = json.loads(r.read().decode("utf-8"))
        r.close()
        return ((d.get("result") or {}).get("subject") or {}).get("statusVat") or "brak w wykazie"
    except Exception:
        return "?"


# ---------------------------------------------------------------- etap 2–3: dokumenty dla pośrednika i firm
NADAWCA_POLA = ("nazwa", "osoba", "adres", "email", "telefon")


def _nad(n, k, opis):
    return (n or {}).get(k) or f"[UZUPEŁNIJ: {opis}]"


def _pln(x):
    return f"{_pl(x)} zł" if isinstance(x, (int, float)) else "–"


def _czesc_opis(rec, o):
    return f"{rec.get('przedmiot', '')}" + (f" – część {o.get('czesc')}" if o.get("czesc") else "")


def notatka_docx(sciezka, rec, o, nadawca):
    """Notatka o możliwości podważenia wyboru (bez AI) – materiał dla firmy i jej prawnika."""
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(_nad(nadawca, "nazwa", "Twoja nazwa / firma"), rozmiar=9)
    A(f"{dt.date.today().strftime('%d.%m.%Y')} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("NOTATKA – MOŻLIWOŚĆ PODWAŻENIA WYBORU OFERTY", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"Postępowanie: {_czesc_opis(rec, o)}", pogrub=True)
    A(f"Zamawiający: {rec.get('zamawiajacy', '')} · ogłoszenie: {rec.get('numer', '')} · strona postępowania: {rec.get('link', '')}")
    w = o.get("wybrany") or {}
    A(f"Wartość: {_pln(o.get('wartosc'))} · ofert: {o.get('liczba_ofert')} · wybrana oferta: {w.get('wykonawca', '')} – {_pln(w.get('cena_brutto'))}")
    A(f"Termin na odwołanie: {o.get('termin_odwolania') or '[UZUPEŁNIJ – data przekazania informacji o wyborze]'} ({opis_terminu(o.get('unijne'), o.get('sposob_przekazania'))}; "
      "koniec w sobotę lub dzień ustawowo wolny od pracy przesuwa się na następny dzień roboczy – art. 509 ust. 2 Pzp)."
      + (f" Termin liczony od dnia przekazania informacji: {dt.date.fromisoformat(o['data_przekazania']).strftime('%d.%m.%Y')} r." if o.get("data_przekazania") else
         " Termin liczony od daty informacji o wyborze z dokumentu – sprawdź faktyczną datę i sposób przekazania informacji."), pogrub=True)
    d.add_heading("Argumenty", level=2)
    for i, a in enumerate(o.get("argumenty") or [], 1):
        A(f"{i}. {a.get('typ', '')} – siła: {a.get('sila', '')}", pogrub=True)
        A(a.get("opis", ""))
        A(f"Podstawa: {a.get('podstawa', '')} · interes we wniesieniu odwołania: {a.get('interes', '')}", kursywa=True, rozmiar=9)
    d.add_heading("Firmy, które mogą wnieść odwołanie", level=2)
    for f in o.get("firmy") or []:
        bl = f.get("biala_lista") or {}
        A(f"{f.get('miejsce') or ''} · {f.get('wykonawca', '')} · NIP {f.get('nip') or '–'} · {f.get('adres') or bl.get('workingAddress') or bl.get('residenceAddress') or ''} "
          f"· cena {_pln(f.get('cena_brutto'))} · priorytet: {f.get('priorytet', '')}")
    d.add_heading("Kolejne kroki", level=2)
    for t in ("Natychmiast: wniosek o udostępnienie oferty wybranego wykonawcy i protokołu (art. 74 Pzp) – bez nich ocena opiera się tylko na dokumentach publicznych.",
              "Po otrzymaniu oferty: badanie oferty (zgodność z SWZ, rażąco niska cena, wyliczenie ceny) i decyzja o odwołaniu.",
              "Odwołanie wnosi wykonawca z interesem (art. 505 Pzp) do Prezesa KIO, z kopią do zamawiającego przed upływem terminu (art. 514 ust. 2 Pzp); "
              f"wpis {_pl(wpis_odwolania(rec.get('rodzaj_przedmiotu'), o.get('unijne')), 0)} zł (§ 2 ust. 1 rozporządzenia w sprawie wpisu od odwołania, Dz.U. 2020 poz. 2437)."):
        A(f"– {t}")
    A("Wstępna ocena przygotowana przez program z dokumentów publicznych zamawiającego – do weryfikacji przez prawnika; nie jest gwarancją wygranej.", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def wniosek_docx(sciezka, rec, o, nadawca):
    """Wniosek o udostępnienie protokołu i oferty wybranego wykonawcy (art. 74 ust. 1 i ust. 2 pkt 1 Pzp)."""
    import modul_oferty as MO
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A(f"{_nad(nadawca, 'nazwa', 'wnioskodawca – nazwa')}\n{_nad(nadawca, 'adres', 'adres')}\n{_nad(nadawca, 'email', 'e-mail do odpowiedzi')}", rozmiar=10)
    A(f"[UZUPEŁNIJ: miejscowość], {dt.date.today().strftime('%d.%m.%Y')} r.", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A(f"{rec.get('zamawiajacy') or '[UZUPEŁNIJ: zamawiający]'}", pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    A("WNIOSEK O UDOSTĘPNIENIE PROTOKOŁU POSTĘPOWANIA I OFERT", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"dotyczy postępowania: {_czesc_opis(rec, o)} (ogłoszenie {rec.get('numer', '')})", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    w = (o.get("wybrany") or {}).get("wykonawca") or "[UZUPEŁNIJ: wybrany wykonawca]"
    A("Na podstawie art. 74 ust. 1 i ust. 2 pkt 1 ustawy Prawo zamówień publicznych wnoszę o niezwłoczne udostępnienie:")
    for t in ("protokołu postępowania wraz z załącznikami (w tym informacji o wartości zamówienia ustalonej przed wszczęciem postępowania),",
              f"oferty wykonawcy {w} wraz z załącznikami, w tym kosztorysu ofertowego / formularza cenowego, podmiotowych i przedmiotowych środków dowodowych,",
              "wezwań skierowanych do tego wykonawcy w toku badania i oceny ofert (w tym do wyjaśnień ceny – art. 224 Pzp) oraz udzielonych odpowiedzi i wyjaśnień,",
              "dokumentów dotyczących oceny ofert w kryteriach (karty oceny / punktacja)."):
        A(f"– {t}")
    A("Oferty wraz z załącznikami udostępnia się niezwłocznie po otwarciu ofert, nie później niż w terminie 3 dni od dnia otwarcia ofert "
      "(art. 74 ust. 2 pkt 1 Pzp). Proszę o przekazanie dokumentów w postaci elektronicznej na adres wskazany powyżej. Informacje zastrzeżone "
      "jako tajemnica przedsiębiorstwa – proszę o wskazanie zakresu zastrzeżenia i udostępnienie pozostałej części.")
    A(f"\n{_nad(nadawca, 'osoba', 'imię i nazwisko, podpis')}", wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


# art. 398 PKE – tekst sprawdzony 24.11.2026 (lexlege.pl/komunik-elektr/art-398/; ustawa z 12.07.2024 r., Dz.U. 2024 poz. 1221)
OSTRZEZENIE_KONTAKT = (
    "Program przygotowuje wyłącznie PROJEKT tekstu i niczego nie wysyła. Używanie telekomunikacyjnych urządzeń końcowych (e-mail, telefon, SMS, "
    "komunikator) i automatycznych systemów wywołujących do przesyłania informacji handlowej, w tym marketingu bezpośredniego, wymaga UPRZEDNIEJ "
    "zgody adresata (art. 398 ust. 1 ustawy z 12 lipca 2024 r. – Prawo komunikacji elektronicznej, Dz.U. 2024 poz. 1221); naruszenie jest czynem "
    "nieuczciwej konkurencji (art. 398 ust. 4). Za handlową może zostać uznana także wiadomość, której celem jest pozyskanie zlecenia. "
    "Dane z dokumentów zamawiającego przetwarzasz jako administrator – obowiązek informacyjny (art. 14 RODO) i prawo sprzeciwu (art. 21 RODO). "
    "Radca prawny i adwokat – zasady etyki zawodowej dotyczące pozyskiwania klientów (Kodeks Etyki Radcy Prawnego, Zbiór Zasad Etyki Adwokackiej "
    "i Godności Zawodu) ograniczają składanie propozycji pomocy prawnej osobom, które o nią nie prosiły. Bez zgody adresata nie wysyłaj tego "
    "tekstu jako oferty; użyj go np. w rozmowie z firmą, która sama się zgłosiła.")


def email(rec, o, firma, nadawca):
    """PROJEKT neutralnego tekstu informacyjnego do firmy z dalszego miejsca – NIE jest wysyłany przez program (decyzja właściciela,
    2027-03: bez masowej ani automatycznej wysyłki; tylko kopiowanie tekstu). Bez propozycji usług – treść informacyjna."""
    arg = [a for a in o.get("argumenty") or [] if a.get("interes") and (firma.get("wykonawca", "") in str(a.get("interes")) or a.get("sila") in ("silny", "średni"))]
    temat = f"Informacja o rozstrzygnięciu postępowania „{_czesc_opis(rec, o)[:80]}”"
    miejsce = (('miejsce ' + str(firma.get('miejsce'))) if isinstance(firma.get('miejsce'), int) else 'pozycję: ' + str(firma.get('miejsce') or '–'))
    linie = [f"Szanowni Państwo,", "",
             f"w postępowaniu „{_czesc_opis(rec, o)}” ({rec.get('zamawiajacy', '')}, ogłoszenie {rec.get('numer', '')}) zamawiający wybrał ofertę "
             f"{(o.get('wybrany') or {}).get('wykonawca', '')}. Według opublikowanej informacji Państwa oferta zajęła {miejsce}.", "",
             "W dokumentach opublikowanych przez zamawiającego występują okoliczności, które mogą mieć znaczenie dla oceny prawidłowości wyboru:"]
    for a in arg[:4]:
        linie.append(f"– {a.get('typ', '')}: {a.get('opis', '')[:400]} (przepis: {a.get('podstawa', '')})")
    linie += ["", f"Termin na wniesienie odwołania do Prezesa Krajowej Izby Odwoławczej upływa {o.get('termin_odwolania') or '[UZUPEŁNIJ]'} "
              f"({dni_odwolania(o.get('unijne'), o.get('sposob_przekazania'))} dni od przekazania informacji o wyborze – {przepis_terminu(o.get('unijne'), o.get('sposob_przekazania'))}; "
              "sprawdź datę przekazania informacji). Odwołanie może wnieść wykonawca, który ma interes w uzyskaniu zamówienia (art. 505 Pzp).", "",
              "Powyższe ustalenia wynikają wyłącznie z dokumentów publicznych zamawiającego i mają charakter wstępny.", "",
              "Z poważaniem", _nad(nadawca, "osoba", "imię i nazwisko"), _nad(nadawca, "nazwa", "firma"), "",
              "—", "Informacja o przetwarzaniu danych (art. 14 RODO): administratorem danych jest " + _nad(nadawca, "nazwa", "administrator") +
              (f" ({_nad(nadawca, 'email', 'e-mail')})" if nadawca else "") +
              ". Dane (nazwa firmy, adres, NIP i dane z oferty) pochodzą z dokumentów udostępnionych publicznie przez zamawiającego. Przetwarzamy je w celu "
              "przekazania informacji o rozstrzygnięciu postępowania, na podstawie prawnie uzasadnionego interesu (art. 6 ust. 1 lit. f RODO), przez czas "
              "niezbędny do tego celu. Przysługuje Państwu prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, sprzeciwu "
              "oraz skargi do Prezesa UODO."]
    return temat, "\n".join(linie)


def dane_do_odwolania(rec, o, firma):
    """Dane dla generatora odwołania z modułu prawnika (prawnik.polecenie_odwolania / odwolanie_docx)."""
    u = {"przedmiot": rec.get("rodzaj_przedmiotu") or "roboty", "tryb": "unijny" if o.get("unijne") else "krajowy", "dla_kogo": "wykonawca", "klient": firma.get("wykonawca", ""),
         "pytania_klienta": "", "zatwierdzone": "1"}
    w = {"podsumowanie": f"Wybrano ofertę {(o.get('wybrany') or {}).get('wykonawca', '')}; odwołujący: {firma.get('wykonawca', '')} (miejsce {firma.get('miejsce')})",
         "uwagi": [{"waga": {"silny": "krytyczna", "średni": "istotna"}.get(a.get("sila"), "drobna"), "kategoria": a.get("typ"), "opis": a.get("opis"),
                    "podstawa": a.get("podstawa"), "dokument": "informacja zamawiającego o wyborze / z otwarcia ofert"} for a in o.get("argumenty") or []]}
    O = {"oferty": [{"nazwa": f.get("wykonawca"), "miejsce": f.get("miejsce"), "wynik": {"cena_brutto": f.get("cena_brutto")}} for f in o.get("firmy") or []]
         + [{"nazwa": (o.get("wybrany") or {}).get("wykonawca"), "miejsce": 1, "wynik": {"cena_brutto": (o.get("wybrany") or {}).get("cena_brutto"), "status": "wybrana"}}]}
    return u, w, O


# ---------------------------------------------------------------- oferenci i ich dane kontaktowe
def oferenci(c):
    """Wszyscy wykonawcy, którzy złożyli ofertę w części: z informacji z otwarcia, rankingu i odrzuceń – bez powtórzeń."""
    w = c.get("wybor") or {}
    L = []

    def dodaj(nazwa, **pola):
        if not nazwa:
            return
        x = next((o for o in L if _ten_sam(o["wykonawca"], nazwa)), None)
        if not x:
            x = {"wykonawca": nazwa}
            L.append(x)
        for k, v in pola.items():
            if v not in (None, "", [], {}) and x.get(k) in (None, "", [], {}):
                x[k] = v
    for o in c.get("oferty") or []:
        dodaj(o.get("wykonawca"), nip=o.get("nip"), adres=o.get("adres"), cena_brutto=_f(o.get("cena_brutto")), inne=o.get("inne_kryteria"))
    for r in w.get("ranking") or []:
        dodaj(r.get("wykonawca"), nip=r.get("nip"), adres=r.get("adres"), cena_brutto=_f(r.get("cena_brutto")), miejsce=r.get("miejsce"),
              punkty=r.get("punkty"), suma=_f(r.get("suma")))
    for r in w.get("odrzucone") or []:
        dodaj(r.get("wykonawca"), nip=r.get("nip"), cena_brutto=_f(r.get("cena_brutto")), odrzucona=f"{r.get('podstawa') or ''} {r.get('uzasadnienie') or ''}".strip() or True)
    for x in L:
        x["nip"] = re.sub(r"\D", "", str(x.get("nip") or "")) or None
        x["status"] = ("wybrana" if w.get("wybrany") and _ten_sam(x["wykonawca"], w.get("wybrany")) else
                       "odrzucona" if x.get("odrzucona") else f"miejsce {x['miejsce']}" if x.get("miejsce") else "złożona")
    return sorted(L, key=lambda x: (x["status"] != "wybrana", x.get("miejsce") or 99, x.get("cena_brutto") or 9e15))


def krs_kontakt(krs, otworz=None):
    """Odpis aktualny z KRS (API Ministerstwa Sprawiedliwości, bez klucza): strona www, e-mail, adres do e-Doręczeń."""
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Bidivia"}), timeout=25))
    k = re.sub(r"\D", "", str(krs or "")).zfill(10)
    for rej in ("P", "S"):
        try:
            with otworz(f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{k}?rejestr={rej}&format=json") as r:
                d = json.loads(r.read().decode("utf-8"))
        except Exception:
            continue
        s = ((d.get("odpis") or {}).get("dane") or {}).get("dzial1", {}).get("siedzibaIAdres", {}) or {}
        www = str(s.get("adresStronyInternetowej") or "").strip().lower()
        return {"www": www, "email": str(s.get("adresPocztyElektronicznej") or "").strip().lower(),
                "ade": str(s.get("adresDoDoreczenElektronicznychWpisanyDoBAE") or "").strip()}
    return {}


RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_TEL = re.compile(r"(?:\+48[\s-]?)?(?:\(?\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}|\d{3}[\s-]?\d{3}[\s-]?\d{3})")


def kontakt_ze_strony(www, otworz=None):
    """Publiczne dane kontaktowe ze strony firmy (strona główna i „kontakt”): adresy e-mail i telefony z odnośników mailto:/tel: i treści."""
    import html as _h
    if not www:
        return {}
    baza = www if www.startswith("http") else "https://" + www.strip("/")
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Bidivia)"}), timeout=15))
    em, tel = [], []
    for u in (baza, baza.rstrip("/") + "/kontakt"):
        try:
            with otworz(u) as r:
                t = _h.unescape(r.read(1_500_000).decode("utf-8", "replace"))
        except Exception:
            continue
        for e in re.findall(r"mailto:([^\"'?>\s]+)", t, re.I) + RE_EMAIL.findall(re.sub(r"<[^>]+>", " ", t)):
            e = e.strip().lower().rstrip(".")
            if e not in em and not re.search(r"\.(png|jpe?g|gif|webp|svg)$|example|sentry|wixpress", e):
                em.append(e)
        tekst = re.sub(r"<[^>]+>", " ", t)
        kand = re.findall(r"tel:([+\d\s()./-]{9,22})", t, re.I) + \
            re.findall(r"(?i)(?:\btel\.?|telefon\w*|phone|\bkom\.?|\bmob\.?)\s*[:.]?\s*((?:\+48[\s-]?)?\(?\d{2,3}\)?[\s.-]?\d{2,3}[\s.-]?\d{2,3}(?:[\s.-]?\d{2,3})?)", tekst)
        for p in kand:
            c_ = re.sub(r"\D", "", p)
            c_ = c_[2:] if len(c_) == 11 and c_.startswith("48") else c_
            if len(c_) == 9 and c_[0] != "0":
                f_ = f"{c_[:3]} {c_[3:6]} {c_[6:]}"
                if f_ not in tel:
                    tel.append(f_)
    waga = lambda e: (0 if re.match(r"(biuro|kontakt|sekretariat|przetargi|oferty|zamowienia|info|office|sprzedaz|handel)@", e) else
                      2 if re.match(r"(iod|rodo|dane\.osobowe|abi|gdpr|privacy|noreply|no-reply)", e) else 1)
    return {"emaile": sorted(em, key=waga)[:3], "telefony": tel[:3], "strona": baza}
