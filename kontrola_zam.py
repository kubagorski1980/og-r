# -*- coding: utf-8 -*-
"""
Kontrole kreatora zamówienia (zamawiający) – stałe reguły programu, bez AI: zapis kwot, pola wymagane i limity kroku „Szczegóły”,
rozpoznanie terminu w opisie, kontrola warunków zamówienia przy zapisie (kryteria, wadium, zabezpieczenie, kary, płatności, termin ofert),
dni wolne od pracy, miesiące kalendarzowe.
Przepisy sprawdzone w tekście jednolitym Pzp (Dz.U. z 2026 r. poz. 793, wersja 12.07–30.11.2026): art. 97 ust. 2 (wadium 3%),
art. 281 ust. 4 i art. 299 ust. 3 (wadium 1,5% w trybie podstawowym), art. 452 ust. 2–3 (zabezpieczenie 5% / 10%), art. 436 pkt 3 (limit kar),
art. 246 (cena powyżej 60%), art. 439 ust. 1 (waloryzacja), art. 443 (części / zaliczki), art. 283 i art. 138 (termin składania ofert).
"""
import datetime as dt
import re

import kreator_zam as KZ

LIMIT_KROTKI, LIMIT_DLUGI = 500, 10000
LIMIT_PLIKOW = 10
WYMAGANE = {"roboty": ("obiekt", "zakres", "termin"), "dostawy": ("przedmiot", "miejsce", "termin"), "uslugi": ("przedmiot", "ilosci", "okres")}
WSPOLNE_POLA = ("termin",)  # odpowiedzi przenoszone przy zmianie rodzaju zamówienia
MIES = "stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia"
MIES_M = "stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia|styczeń|luty|marzec|kwiecień|maj|czerwiec|lipiec|sierpień|wrzesień|październik|listopad|grudzień"


def kwota(txt):
    """„200000”, „200 000”, „200 000,00”, „200.000,00”, „200 000 zł” → liczba; zapis nieliczbowy („ok. 200 tys.”, „1,5 mln”) → None."""
    t = re.sub(r"(?i)\s*(zł|pln)\.?\s*$", "", str(txt if txt is not None else "").strip())
    t = re.sub(r"[\s ]", "", t)
    if not t:
        return None
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d{1,2})?", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d+([.,]\d{1,2})?", t):
        t = t.replace(",", ".")
    else:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def termin_z_opisu(opis):
    """Termin wykonania z opisu z kroku 1 – tylko daty, nazwy miesięcy i okres od podpisania umowy (nie „do dachu 2027”)."""
    o = str(opis or "")
    m = re.search(r"(?i)\bdo\s+(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{4})", o) \
        or re.search(rf"(?i)\bdo\s+(\d{{1,2}}\s+(?:{MIES})\s+\d{{4}})", o) \
        or re.search(rf"(?i)\bdo\s+((?:końca\s+)?(?:{MIES_M})\s+\d{{4}})", o)
    if m:
        return "do " + m.group(1)
    m = re.search(r"(?i)(\d+\s+(?:miesi\w+|tygodni\w*|dni)\s+od\s+(?:dnia\s+)?(?:podpisania|zawarcia)\s+umowy)", o)
    return m.group(1) if m else ""


MIES_NR = {"sty": 1, "lut": 2, "mar": 3, "kwi": 4, "maj": 5, "cze": 6, "lip": 7, "sie": 8, "wrz": 9, "paź": 10, "lis": 11, "gru": 12}


def _nr_miesiaca(nazwa):
    return MIES_NR.get(str(nazwa or "").lower()[:3])


def data_iso(v):
    """Data z zapisu RRRR-MM-DD albo DD.MM.RRRR (także „-” i „/”) → date; zapis nieprawidłowy albo data nieistniejąca → None."""
    t = str(v or "").strip()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t[:10]) and (len(t) == 10 or t[10] in "T "):
            return dt.date.fromisoformat(t[:10])
        m = re.fullmatch(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", t)
        if m:
            return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None
    return None


def _ostatni_dzien(r, m):
    return dt.date(r + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def data_terminu_wykonania(tekst):
    """Data końcowa z terminu wykonania („do 30.09.2027”, „do 20 sierpnia 2027”, „do końca września 2027”, „2027-09-30”) → (date | None, błąd | "").
    Przy kilku datach liczy się ostatnia (np. „od 01.03.2027 do 30.09.2027”). Okres („18 miesięcy od podpisania umowy”) → (None, "").
    Data nieistniejąca (31.02.2027) → (None, opis błędu)."""
    t = str(tekst or "")
    wyn = []  # (pozycja, data | None, zapis)
    for m in re.finditer(r"\b(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})\b", t):
        try:
            wyn.append((m.start(), dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))), m.group(0)))
        except ValueError:
            wyn.append((m.start(), None, m.group(0)))
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", t):
        try:
            wyn.append((m.start(), dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))), m.group(0)))
        except ValueError:
            wyn.append((m.start(), None, m.group(0)))
    for m in re.finditer(rf"(?i)\b(\d{{1,2}})\s+({MIES})\s+(\d{{4}})", t):
        try:
            wyn.append((m.start(), dt.date(int(m.group(3)), _nr_miesiaca(m.group(2)), int(m.group(1))), m.group(0)))
        except (ValueError, TypeError):
            wyn.append((m.start(), None, m.group(0)))
    for m in re.finditer(rf"(?i)\bdo\s+(?:końca\s+)?({MIES_M})\s+(\d{{4}})", t):
        nr = _nr_miesiaca(m.group(1))
        if nr:
            wyn.append((m.start(), _ostatni_dzien(int(m.group(2)), nr), m.group(0)))
    if not wyn:
        return None, ""
    zle = [z for _, d, z in wyn if d is None]
    if zle:
        return None, f"data „{zle[0]}” nie istnieje"
    return max(wyn, key=lambda x: x[0])[1], ""


def miesiace_okresu(tekst):
    """Długość okresu z tekstu („18 miesięcy od podpisania umowy”, „52 tygodnie”, „400 dni”) w miesiącach; brak okresu → None."""
    t = str(tekst or "")
    m = re.search(r"(?i)\b(\d{1,3})\s*(miesi\w*|mies\.|tygodni\w*|tydzie\w*|dni)\b", t)
    if not m:
        return None
    n, j = int(m.group(1)), m.group(2).lower()
    return n if j.startswith("mies") else round(n * 7 / 30.4, 1) if j.startswith("tydz") or j.startswith("tygod") else round(n / 30.4, 1)


def czysc_potrzebe(rodzaj, dane):
    """Odpowiedzi kroku „Szczegóły”: tylko pytania danego rodzaju, wartości list z listy, limity znaków. → (przyjęte, błędy)."""
    P = {p[0]: p for p in KZ.PYTANIA.get(rodzaj, [])}
    ok, bledy = {}, []
    for k, v in (dane or {}).items():
        if k not in P:
            bledy.append(f"Nieznane pole „{k}” – nie zapisano.")
            continue
        v = str(v or "").strip()
        _id, et, typ, op = P[k]
        if typ == "wybor":
            if v and v not in op:
                bledy.append(f"„{et}”: wybierz wartość z listy.")
                continue
        else:
            lim = LIMIT_DLUGI if typ == "dlugi" else LIMIT_KROTKI
            if len(v) > lim:
                bledy.append(f"„{et}”: tekst ma {len(v)} znaków, limit to {lim} – skróć odpowiedź (nie została zapisana).")
                continue
        ok[k] = v
    return ok, bledy


def braki_szczegolow(rodzaj, potrzeba):
    """Brakujące pola wymagane kroku „Szczegóły” (etykiety)."""
    P = {p[0]: p[1] for p in KZ.PYTANIA.get(rodzaj, [])}
    return [P[k] for k in WYMAGANE.get(rodzaj, ()) if not str((potrzeba or {}).get(k) or "").strip()]


def potrzeba_rodzaju(rodzaj, potrzeba):
    """Tylko odpowiedzi bieżącego rodzaju zamówienia (odpowiedzi innego rodzaju są odłożone i nieużywane)."""
    ids = {p[0] for p in KZ.PYTANIA.get(rodzaj, [])}
    return {k: v for k, v in (potrzeba or {}).items() if k in ids}


# ---------------------------------------------------------------- dni wolne i miesiące kalendarzowe
def _wielkanoc(r):
    a, b, c = r % 19, r // 100, r % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return dt.date(r, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def swieta(rok):
    """Dni ustawowo wolne od pracy w Polsce (od 2025 r. także 24 grudnia)."""
    w = _wielkanoc(rok)
    stale = [(1, 1), (1, 6), (5, 1), (5, 3), (8, 15), (11, 1), (11, 11), (12, 25), (12, 26)] + ([(12, 24)] if rok >= 2025 else [])
    return {dt.date(rok, m, d) for m, d in stale} | {w, w + dt.timedelta(days=1), w + dt.timedelta(days=49), w + dt.timedelta(days=60)}


def wolny(d):
    return d.weekday() >= 5 or d in swieta(d.year)


def nastepny_roboczy(d):
    """Termin kończący się w sobotę albo dzień ustawowo wolny – najbliższy dzień roboczy (art. 115 k.c.)."""
    while wolny(d):
        d += dt.timedelta(days=1)
    return d


def poprzedni_roboczy(d):
    while wolny(d):
        d -= dt.timedelta(days=1)
    return d


def miesiace_wstecz(d, n):
    """Data o n miesięcy kalendarzowych wcześniejsza (31.05 − 3 mies. = 28/29.02)."""
    m = d.month - n
    r = d.year + (m - 1) // 12
    m = (m - 1) % 12 + 1
    ost = (dt.date(r + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(r, m, min(d.day, ost))


# ---------------------------------------------------------------- kontrola warunków przy zapisie
def _procenty(t):
    return [float(x.replace(",", ".")) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*%", str(t or ""))]


_SLOWA_DNI = {"czternast": 14, "dwudziest\\w* jeden": 21, "trzydziest": 30, "czterdziest\\w* pięci": 45, "sześćdziesi": 60, "dziewięćdziesi": 90}
_SLOWA_MIES = {"jedn": 1, "dw": 2, "trz": 3, "czter": 4, "sześ": 6}
_ZAPLATA = r"(?:termin\w*|w ciągu|płatn\w*|zapłat\w*|przelew\w*|po upływie)"


def _dni_zaplaty(t):
    """Terminy zapłaty z tekstu płatności w dniach: „30 dni”, „2 miesięcy” (×30), „3 tygodni” (×7), „trzydziestu dni”."""
    t = str(t or "").lower()
    dni = [int(x) for x in re.findall(r"(\d{1,3})\s*dni", t)]
    dni += [int(n) * (30 if j.startswith("mies") else 7) for n, j in re.findall(_ZAPLATA + r"\D{0,25}?\b(\d{1,2})\s*(miesi\w*|mies\.|tygodni\w*)", t)]
    for wz, n in _SLOWA_DNI.items():
        if re.search(wz + r"\w*\s+(?:\(\d+\)\s*)?dni", t):
            dni.append(n)
    for wz, n in _SLOWA_MIES.items():
        if re.search(_ZAPLATA + r"\D{0,25}?\b" + wz + r"\w*\s+miesi", t):
            dni.append(n * 30)
    return dni


def _wadium_czesci(wad, czesci, limit):
    """Wadium przy podziale na części (art. 97 ust. 3 Pzp): kwota dla każdej części, limit liczony od wartości części.
    → (lista błędów, czy wadium podano osobno dla części)."""
    war = {int(c.get("nr") or i + 1): float(c.get("wartosc") or 0) for i, c in enumerate(czesci)}
    bledy, osobno = [], False
    for m in re.finditer(r"(?i)cz(?:ęść|esc|\.)\s*(?:nr\s*)?(\d{1,2})\s*[–:\-—)]?\s*([^;\n]*)", str(wad or "")):
        nr, seg = int(m.group(1)), m.group(2)
        osobno = True
        pr = _procenty(seg)
        kw = None if pr else next((kwota(x) for x in re.findall(r"\d[\d  .,]*\d", seg) if kwota(x)), None)
        if kw and war.get(nr):
            pr = [round(kw / war[nr] * 100, 3)]
        if pr and max(pr) > limit + 1e-9:
            bledy.append(f"Wadium dla części {nr}: {KZ._pl(max(pr))}% wartości tej części" + (f" ({KZ.PR.zl(war[nr])})" if war.get(nr) else "")
                         + f" przekracza limit {KZ._pl(limit)}% – kwotę wadium określa się dla każdej części od jej wartości (art. 97 ust. 3 Pzp).")
    return bledy, osobno


def kontrola_warunkow(w, rodzaj, tryb, prywatny, netto, termin_ofert="", godzina="", data_wszczecia="", min_dni=None, dzis=None,
                      termin_wykonania="", czesci=None, opublikowane=False):
    """Lista {waga: blad | ostrzezenie, pole, opis}. tryb: pzp_podstawowy / pzp_nieograniczony / ponizej_130 / prywatny…
    termin_wykonania – tekst z kroku „Szczegóły” (art. 443 przy umowie dłuższej niż 12 miesięcy); czesci – lista części z wartościami
    (wadium osobno dla każdej części); opublikowane – po publikacji nie sprawdza się, czy termin składania ofert minął."""
    w = w or {}
    dzis = dzis or dt.date.today()
    pzp = str(tryb or "").startswith("pzp") and not prywatny
    U = []
    dodaj = lambda waga, pole, opis: U.append({"waga": waga, "pole": pole, "opis": opis})
    # kryteria
    kt = str(w.get("kryteria") or "")
    if kt.strip():
        cz = [c for c in KZ._podziel_kryteria(kt) if c.strip()]
        K = KZ.kryteria_z_tekstu(kt)
        if len(K) < len(cz):
            dodaj("blad", "kryteria", "Kryteria oceny: każde kryterium musi mieć wagę w procentach (np. „Cena – 60%, okres gwarancji – 40%”).")
        elif abs(sum(k["waga"] for k in K) - 100) > 0.01:
            dodaj("blad", "kryteria", f"Kryteria oceny: suma wag wynosi {KZ._pl(sum(k['waga'] for k in K))}%, a musi wynosić 100%.")
        cena = next((k["waga"] for k in K if re.search(r"(?i)\bcen", k["nazwa"])), None)
        if pzp and cena and cena > 60:
            dodaj("ostrzezenie", "kryteria", f"Cena z wagą {KZ._pl(cena)}%: waga powyżej 60% jest dopuszczalna tylko wtedy, gdy opis przedmiotu zamówienia "
                                             "określa wymagania jakościowe dla co najmniej głównych elementów zamówienia (art. 246 ust. 2 Pzp).")
    if pzp:
        # wadium
        wad = str(w.get("wadium") or "")
        limit = 1.5 if tryb == "pzp_podstawowy" else 3.0
        cz_ = [c for c in (czesci or []) if isinstance(c, dict) and c.get("wartosc")]
        bl_cz, osobno = _wadium_czesci(wad, cz_, limit) if len(cz_) >= 2 else ([], False)
        for b_ in bl_cz:
            dodaj("blad", "wadium", b_)
        pr = _procenty(wad)
        kw = None if pr else next((kwota(x) for x in re.findall(r"\d[\d  .,]*\d", wad) if kwota(x)), None)
        if kw and len(cz_) >= 2 and not osobno:  # jedna kwota przy podziale na części – porównanie z najmniejszą częścią (art. 97 ust. 3)
            naj = min(cz_, key=lambda c: float(c["wartosc"]))
            pr_ = round(kw / float(naj["wartosc"]) * 100, 3)
            if pr_ > limit + 1e-9:
                dodaj("blad", "wadium", f"Wadium {KZ.PR.zl(kw)} to {KZ._pl(pr_)}% wartości części {naj.get('nr') or ''} ({KZ.PR.zl(float(naj['wartosc']))}) – "
                                        f"przekracza limit {KZ._pl(limit)}%. Przy podziale na części kwotę wadium określa się dla każdej części (art. 97 ust. 3 Pzp).")
            else:
                dodaj("ostrzezenie", "wadium", "Wadium przy podziale na części: określ kwotę osobno dla każdej części (art. 97 ust. 3 Pzp), "
                                               "np. „część 1 – 20 000 zł; część 2 – 1 500 zł”.")
            kw = None
        if kw and netto:
            pr = [round(kw / netto * 100, 3)]
        if pr and not osobno and max(pr) > limit + 1e-9:
            dodaj("blad", "wadium", f"Wadium: {KZ._pl(max(pr))}% wartości zamówienia przekracza limit {KZ._pl(limit)}% "
                                    f"({'art. 281 ust. 4 Pzp' if tryb == 'pzp_podstawowy' else 'art. 97 ust. 2 Pzp'}).")
        # zabezpieczenie
        pr = _procenty(w.get("zabezpieczenie"))
        if pr and max(pr) > 10:
            dodaj("blad", "zabezpieczenie", f"Zabezpieczenie: {KZ._pl(max(pr))}% przekracza najwyższy dopuszczalny poziom 10% ceny (art. 452 ust. 3 Pzp).")
        elif pr and max(pr) > 5:
            dodaj("ostrzezenie", "zabezpieczenie", f"Zabezpieczenie {KZ._pl(max(pr))}%: powyżej 5% tylko wtedy, gdy uzasadnia to przedmiot zamówienia albo ryzyko "
                                                   "opisane w dokumentach zamówienia (art. 452 ust. 3 Pzp).")
        # kary
        kary = str(w.get("kary") or "")
        if kary.strip() and not re.search(r"(?i)limit|łączn\w+|maksymaln\w+|najwyżej|nie więcej niż|\bma(?:x|ks)\b\.?|\bsum\w* kar|przekroczy\w*|"
                                          r"do wysokości|do kwoty|nie wyższ\w*|górn\w* granic", kary):
            dodaj("blad", "kary", "Kary umowne: podaj łączną maksymalną wysokość kar (art. 436 pkt 3 Pzp), np. „łączny limit kar 20% wynagrodzenia brutto”.")
        # płatności
        dni = _dni_zaplaty(w.get("platnosci"))
        if dni and max(dni) > 30:
            dodaj("blad", "platnosci", f"Płatności: termin zapłaty {max(dni)} dni – zamawiający publiczny płaci najpóźniej w 30 dni od doręczenia faktury.")
        # umowa dłuższa niż 12 miesięcy – płatności częściowe albo zaliczka (art. 443 ust. 1 Pzp)
        mies = miesiace_okresu(termin_wykonania)
        if mies is None:
            dk, _ = data_terminu_wykonania(termin_wykonania)
            od_ = data_iso(termin_ofert) or data_iso(data_wszczecia) or dzis
            mies = round((dk - od_).days / 30.4, 1) if dk else None
        tekst_pl = (str(w.get("platnosci") or "") + " " + str(w.get("wynagrodzenie") or "")).lower()
        if mies and mies > 12 and not re.search(r"częściow|etap|zaliczk|transz|miesięczn|kwartaln|okresow|w ratach|\brat[ay]?\b", tekst_pl):
            dodaj("ostrzezenie", "platnosci", f"Płatności: umowa na ok. {KZ._pl(mies)} miesięcy (termin wykonania: „{str(termin_wykonania)[:60]}”) – przy umowie dłuższej niż "
                                              "12 miesięcy zamawiający płaci wynagrodzenie w częściach po wykonaniu części umowy albo udziela zaliczki; "
                                              "ostatnia część najwyżej 50% wynagrodzenia, zaliczka co najmniej 5% (art. 443 Pzp).")
        # waloryzacja
        wal = str(w.get("waloryzacja") or "").strip().lower()
        if wal.startswith(("nie", "brak", "bez")):
            dodaj("ostrzezenie", "waloryzacja", "Waloryzacja: w umowie zawartej na okres dłuższy niż 6 miesięcy klauzula zmiany wynagrodzenia jest "
                                                "obowiązkowa (art. 439 ust. 1 Pzp).")
    # termin i godzina składania ofert
    g = str(godzina or "").strip()
    if g and not (re.fullmatch(r"\d{1,2}:\d{2}", g) and int(g.split(":")[0]) <= 23 and int(g.split(":")[1]) <= 59):
        dodaj("blad", "godzina_ofert", "Godzina składania ofert: wpisz w zapisie GG:MM (00:00–23:59).")
    t = data_iso(termin_ofert)
    if str(termin_ofert or "").strip() and not t:
        dodaj("blad", "termin_ofert", f"Termin składania ofert „{str(termin_ofert)[:20]}”: nieprawidłowa data – wpisz datę w zapisie RRRR-MM-DD albo DD.MM.RRRR.")
    if t and not opublikowane and t < dzis:
        dodaj("ostrzezenie" if prywatny else "blad", "termin_ofert",
              f"Termin składania ofert {t:%d.%m.%Y} już minął – wyznacz termin przypadający po planowanej publikacji.")
    if t and wolny(t):
        dodaj("ostrzezenie", "termin_ofert", f"Termin składania ofert {t:%d.%m.%Y} wypada w dzień wolny od pracy ("
              + ("sobota" if t.weekday() == 5 else "niedziela" if t.weekday() == 6 else "święto") + ") – ustaw dzień roboczy, np. "
              + f"{nastepny_roboczy(t):%d.%m.%Y}. Termin z kreatora trafia do dokumentów, kalendarza postępowania i pism.")
    if t and min_dni:
        od = data_iso(data_wszczecia) or dzis
        if (t - od).days < min_dni:
            dodaj("ostrzezenie" if (prywatny or not pzp) else "blad", "termin_ofert",
                  f"Termin składania ofert: {(t - od).days} dni od {'planowanej publikacji' if data_iso(data_wszczecia) else 'dziś'} ({od:%d.%m.%Y}) – "
                  + (f"zalecane co najmniej {min_dni} dni." if (prywatny or not pzp) else f"minimum dla tego trybu to {min_dni} dni."))
    return U


def znaczniki_uzupelnij(sciezka_docx, tylko_opisane=False):
    """Liczba pól „[UZUPEŁNIJ…” w dokumencie Word (akapity i tabele). tylko_opisane – formularz ofertowy i oświadczenia: puste pola
    „[UZUPEŁNIJ]” wypełnia wykonawca, liczą się tylko pola opisane „[UZUPEŁNIJ: …]” (dla zamawiającego)."""
    try:
        import docx
        d = docx.Document(sciezka_docx)
    except Exception:
        return 0
    teksty = [p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells]
    return sum(t.count("[UZUPEŁNIJ:" if tylko_opisane else "[UZUPEŁNIJ") for t in teksty)


# Zapisy sprzeczne z Pzp, które AI powtarza za dawną ustawą (2004) albo myli tryby – sprawdzane w tekście dokumentów i w propozycjach zmian.
def kolizje_z_przepisami(tekst, tryb):
    """Lista opisów sprzeczności z parametrami ustawowymi trybu (pusta = brak). tekst – fragment dokumentu albo nowe brzmienie propozycji."""
    t = re.sub(r"\s+", " ", str(tekst or "")).lower()
    tryb = str(tryb or "")
    U = []
    if "związan" in t and "ofert" in t:
        if tryb == "pzp_podstawowy" and re.search(r"(przedłuż\w*).{0,200}?\b(4[5-9]|[5-9]\d|1[0-2]\d)\s*dni", t):
            U.append("przedłużenie terminu związania ofertą w trybie podstawowym: najwyżej o 30 dni (art. 307 ust. 2 Pzp)")
        if tryb == "pzp_nieograniczony" and re.search(r"(przedłuż\w*).{0,200}?\b(6[1-9]|[7-9]\d|1[0-2]\d)\s*dni", t):
            U.append("przedłużenie terminu związania ofertą w procedurze unijnej: najwyżej o 60 dni (art. 220 ust. 3 Pzp)")
        if re.search(r"co najmniej (na )?3 dni przed upływem terminu związania", t):
            U.append("wymóg zwrócenia się „co najmniej na 3 dni przed upływem terminu związania ofertą” pochodzi z dawnej ustawy – "
                     "obecnie zamawiający zwraca się jednokrotnie przed upływem terminu (art. 307 ust. 2 / art. 220 ust. 3 Pzp)")
    if "grup" in t and "kapitałow" in t and re.search(r"(w terminie|w ciągu) (3|trzech) dni", t):
        U.append("oświadczenie o przynależności do grupy kapitałowej w terminie 3 dni od otwarcia ofert – zasada dawnej ustawy (art. 24 ust. 11 "
                 "Pzp z 2004 r.); obecnie to podmiotowy środek dowodowy składany na wezwanie zamawiającego")
    return U
