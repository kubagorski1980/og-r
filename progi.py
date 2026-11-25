# -*- coding: utf-8 -*-
"""Progi zamówień publicznych – w jednym miejscu programu.
Od 1 stycznia 2026 r. próg stosowania ustawy Pzp: 170 000 zł netto (wcześniej 130 000 zł). Do postępowań wszczętych przed zmianą
(i umów z nich zawartych) stosuje się przepisy dotychczasowe – próg 130 000 zł."""
import datetime as dt
import re

PROG_PZP = 170000
PROG_PZP_STARY = 130000
DATA_ZMIANY = dt.date(2026, 1, 1)
PROG_ZK = 80000  # zasada konkurencyjności: zamówienia o wartości PRZEKRACZAJĄCEJ 80 000 zł netto (Wytyczne dot. kwalifikowalności 2021–2027, sekcja 3.2.1,
PROG_ZK_STARY = 50000  # wersja obowiązująca od 25.03.2025; wcześniej 50 000 zł – liczy się wersja z dnia wszczęcia, tj. publikacji zapytania ofertowego)
DATA_ZMIANY_ZK = dt.date(2025, 3, 25)
TERMIN_ZK_30 = ("30 dni – zamówienia od progów wskazanych w wytycznych (dostawy i usługi: 750 000 euro; roboty budowlane: próg unijny, "
                "od 1.01.2026 r. 5 404 000 euro – sprawdź aktualną wersję wytycznych)")


def prog_zk(data_wszczecia=None):
    """Próg zasady konkurencyjności dla daty wszczęcia (publikacji zapytania) – stosuje się, gdy wartość go PRZEKRACZA."""
    try:
        d = dt.date.fromisoformat(str(data_wszczecia)[:10]) if data_wszczecia else dt.date.today()
    except ValueError:
        d = dt.date.today()
    return PROG_ZK_STARY if d < DATA_ZMIANY_ZK else PROG_ZK


def wymaga_zk(netto, data_wszczecia=None):
    return float(netto or 0) > prog_zk(data_wszczecia)


def prog_pzp(data_wszczecia=None):
    try:
        d = dt.date.fromisoformat(str(data_wszczecia)[:10]) if data_wszczecia else dt.date.today()
    except ValueError:
        d = dt.date.today()
    return PROG_PZP if d >= DATA_ZMIANY else PROG_PZP_STARY


def zl(x):
    return f"{int(x):,}".replace(",", " ") + " zł"


def liczba_pl(x, miejsca=2):
    """1234567.8 → „1 234 567,80” (spacja tysięcy, przecinek dziesiętny)."""
    return f"{float(x):,.{miejsca}f}".replace(",", "\u00a0").replace(".", ",").replace("\u00a0", " ")


_LICZBA = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?\b|\b\d+\.\d{1,2}\b")


def pl_liczby(tekst):
    """Liczby sformatowane po angielsku w tekście („1,234,567.89”, „12.5”) → polski zapis („1 234 567,89”, „12,5”).
    Zastępuje .replace(",", " "), które psuło przecinki dziesiętne i interpunkcję."""
    return _LICZBA.sub(lambda m: m.group(0).replace(",", "\u00a0").replace(".", ",").replace("\u00a0", " "), str(tekst))


def euro(x, miejsca=2):
    return liczba_pl(x, miejsca) + " €"


def kurs_pl(k):
    return str(k).replace(".", ",") + " zł"


INFO_AI = ("STAN PRAWNY: od 1 stycznia 2026 r. próg stosowania ustawy Prawo zamówień publicznych wynosi 170 000 zł netto (wcześniej 130 000 zł; "
           "stary próg stosuje się tylko do postępowań wszczętych przed zmianą). Zamówienia poniżej 170 000 zł netto – poza Pzp (regulamin "
           "zamawiającego, zasada konkurencyjności w projektach UE – zamówienia powyżej 80 000 zł netto, od 25.03.2025 r.). Nie powołuj się na próg 130 000 zł jako aktualny.")


# średni kurs złotego do euro do przeliczania wartości zamówień i progi unijne na lata 2026–2027:
# obwieszczenie Prezesa UZP z 8 grudnia 2025 r. (M.P. poz. 1247) – 5 404 000 € = 23 291 240 zł, 216 000 € = 930 960 zł, 140 000 € = 603 400 zł,
# usługi społeczne 750 000 € = 3 232 500 zł (art. 359 Pzp)
# Sprawdzone w źródłach 24.11.2026: UZP – „Aktualne progi unijne oraz aktualny średni kurs złotego w stosunku do euro” (kurs 4,31; obwieszczenie
# z 8.12.2025 r., M.P. poz. 1247, stosowane od 1.01.2026 r.): https://www.gov.pl/web/uzp-en/current-thresholds-in-public-procurement-and-current-average-exchange-rate-pln-euro ;
# progi UE – rozporządzenie delegowane Komisji (UE) 2025/2152 z 22.10.2025 r. (dyrektywa 2014/24/UE: 5 404 000 / 140 000 / 216 000 €, od 1.01.2026 r.):
# https://eur-lex.europa.eu/eli/reg_del/2025/2152/oj ; ten sam kurs 4,31 – obwieszczenie MFiG z 22.12.2025 r. (M.P. 2025 poz. 1288, koncesje).
KURS_EURO = 4.31
PROGI_UE = {"roboty": 5404000, "dostawy": 216000, "uslugi": 216000, "dostawy_centralne": 140000, "uslugi_centralne": 140000}
PROG_SPOLECZNE = 750000
PROGI_WAZNE_DO = dt.date(2027, 12, 31)  # po tej dacie nowe obwieszczenie – program ostrzega


def tryb_wedlug_wartosci(netto, rodzaj="roboty", data_wszczecia=None, centralny=False, spoleczne=False):
    """Który reżim: poniżej progu Pzp / krajowy (tryb podstawowy) / unijny – na podstawie wartości szacunkowej netto.
    centralny – zamawiający centralny (140 000 € dla dostaw i usług); spoleczne – usługi społeczne (750 000 €, art. 359 Pzp)."""
    prog = prog_pzp(data_wszczecia)
    ue_eur = PROG_SPOLECZNE if (spoleczne and rodzaj == "uslugi") else \
        PROGI_UE.get(rodzaj + ("_centralne" if centralny and rodzaj != "roboty" else ""), PROGI_UE.get(rodzaj, 216000))
    ue_zl = round(ue_eur * KURS_EURO)
    eur_ = euro(ue_eur, 0)
    if netto < prog:
        t = f"poniżej progu stosowania Pzp ({zl(prog)} netto) – zamówienie na podstawie regulaminu zamawiającego (zapytanie ofertowe)"
    elif netto < ue_zl:
        t = f"Pzp – procedura krajowa (np. tryb podstawowy, art. 275), poniżej progu unijnego ({eur_} = {zl(ue_zl)})"
    else:
        t = f"Pzp – procedura unijna (np. przetarg nieograniczony), wartość od progu unijnego ({eur_} = {zl(ue_zl)})"
    try:
        dw = dt.date.fromisoformat(str(data_wszczecia)[:10]) if data_wszczecia else dt.date.today()
    except ValueError:
        dw = dt.date.today()
    nieaktualne = ("Progi unijne i kurs euro (4,31 zł) obowiązują do 31.12.2027 r. – dla postępowań wszczynanych później sprawdź nowe obwieszczenie "
                   "Prezesa UZP i zaktualizuj program.") if dw > PROGI_WAZNE_DO else ""
    return {"opis": t, "prog_pzp": prog, "prog_ue_zl": ue_zl, "prog_ue_eur": ue_eur, "euro": round(netto / KURS_EURO, 2), "kurs": KURS_EURO,
            "ostrzezenie": nieaktualne}


def _wielkanoc(rok):
    a, b, c = rok % 19, rok // 100, rok % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    mies = (h + l_ - 7 * m + 114) // 31
    return dt.date(rok, mies, (h + l_ - 7 * m + 114) % 31 + 1)


def swieta(rok):
    """Dni ustawowo wolne od pracy (ustawa o dniach wolnych od pracy; Wigilia – od 2025 r.)."""
    w = _wielkanoc(rok)
    S = {dt.date(rok, 1, 1), dt.date(rok, 1, 6), w, w + dt.timedelta(days=1), dt.date(rok, 5, 1), dt.date(rok, 5, 3), w + dt.timedelta(days=49),
         w + dt.timedelta(days=60), dt.date(rok, 8, 15), dt.date(rok, 11, 1), dt.date(rok, 11, 11), dt.date(rok, 12, 25), dt.date(rok, 12, 26)}
    if rok >= 2025:
        S.add(dt.date(rok, 12, 24))
    return S


def koniec_terminu(d):
    """Art. 509 ust. 2 Pzp (i art. 115 KC): koniec terminu w sobotę lub dzień ustawowo wolny od pracy → następny dzień roboczy."""
    while d.weekday() >= 5 or d in swieta(d.year):
        d += dt.timedelta(days=1)
    return d

