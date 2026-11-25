# -*- coding: utf-8 -*-
"""
Moduł harmonogramu dostaw i zamówień.
 - Harmonogram: dzieli materiały z listy materiałów na etapy robót (AI układa kolejność prac i procentowy
   podział dostaw), zapisuje plik Excel z planem robót, edytowalnym podziałem dostaw i zamówieniami na etapy.
 - Zamówienia: wysyła do wybranych hurtowni zamówienie lub zapytanie ofertowe na materiały danego etapu
   (e-mail z tabelą + załącznik Excel) – jako szkic w programie pocztowym albo bezpośrednio przez SMTP.
"""
import datetime as dt
import html
import json
import math
import os
import re
import smtplib
import ssl
import unicodedata
import urllib.error
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modul_oferty import claude_stream, wyciagnij_json, zaokr, zl
from modul_materialy import wczytaj_kosztorys

DNI = ["pn", "wt", "śr", "cz", "pt", "sb", "nd"]


def norm(s):
    s = str(s or "").lower().replace("ł", "l")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def data_pl(d):
    return f"{DNI[d.weekday()]} {d:%d.%m.%Y}"


def parsuj_date(s):
    s = (s or "").strip()
    for f in ("%d.%m.%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise ValueError(f"Nieprawidłowa data: „{s}” (użyj formatu DD.MM.RRRR)")


def _wolny(d):
    """Sobota, niedziela albo dzień ustawowo wolny od pracy (hurtownie nie przyjmują wtedy zamówień)."""
    try:
        from progi import swieta
        return d.weekday() >= 5 or d in swieta(d.year)
    except ImportError:
        return d.weekday() >= 5


def dzien_roboczy_przed(d):
    while _wolny(d):
        d -= dt.timedelta(days=1)
    return d


def il_pl(x):
    return f"{x:,.3f}".rstrip("0").rstrip(".").replace(",", " ").replace(".", ",")


def jm_klucz(jm):
    """Jednostka do porównań: „m³” = „m3”, „Kg” = „kg”, „t.” = „t”."""
    return str(jm or "").strip().lower().replace("³", "3").replace("²", "2").rstrip(".")


def zaokr_gora(x, jm):
    miejsca = 1 if jm_klucz(jm) in ("m3", "kg", "t", "l") else 0
    return math.ceil(round(x * 10 ** miejsca, 6)) / 10 ** miejsca


# ============================================================ odczyt listy materiałów

def wczytaj_liste(sciezka):
    """Czyta listę materiałów (z modułu Materiały lub wcześniejszą, np. Lelewela 22).
    Zwraca listę: id, nazwa, jm, kategoria, ilosc (do zamówienia), cena, pozycje, uwagi."""
    import openpyxl
    wb = openpyxl.load_workbook(sciezka, data_only=True)
    ws = wb["Lista materiałów"] if "Lista materiałów" in wb.sheetnames else wb.worksheets[0]
    # sumy z arkusza „Wg pozycji kosztorysu” (gdy formuły nie mają zapisanych wartości)
    sumy = {}
    if "Wg pozycji kosztorysu" in wb.sheetnames:
        wp = wb["Wg pozycji kosztorysu"]
        for row in wp.iter_rows(min_row=4, values_only=True):
            if row and len(row) > 9 and row[5] and isinstance(row[3], (int, float)) and isinstance(row[9], (int, float)):
                sumy[str(row[5])] = sumy.get(str(row[5]), 0) + row[3] * row[9]
    kol, kat, wynik = None, "", []
    for row in ws.iter_rows(values_only=True):
        v = list(row)
        if kol is None:
            if v and str(v[0] or "").strip().lower().startswith("lp"):
                kol = {}
                for i, x in enumerate(v):
                    t = norm(x)
                    if t == "id":
                        kol["id"] = i
                    elif t.startswith("material"):
                        kol["nazwa"] = i
                    elif t in ("jm", "j.m."):
                        kol["jm"] = i
                    elif "do zamowienia" in t:
                        kol["zam"] = i
                    elif t.startswith("zapas"):
                        kol["zapas"] = i
                    elif t.startswith("ilosc") and "ilosc" not in kol:
                        kol["ilosc"] = i
                    elif t.startswith("ilosc wg przedmiaru"):
                        kol["ilosc"] = i
                    elif t.startswith("cena"):
                        kol["cena"] = i
                    elif t.startswith("pozycje"):
                        kol["poz"] = i
                    elif t.startswith("uwagi"):
                        kol["uwagi"] = i
            continue
        if not isinstance(v[0], (int, float)):
            if isinstance(v[0], str) and v[0].strip() and not norm(v[0]).startswith("razem"):
                kat = v[0].strip()
            continue
        g = lambda k: v[kol[k]] if k in kol and kol[k] < len(v) else None
        ident = str(g("id") or f"M{int(v[0])}")
        jm = str(g("jm") or "").strip()
        zapas = g("zapas") if isinstance(g("zapas"), (int, float)) else 0.0
        ilosc = g("zam")
        if not isinstance(ilosc, (int, float)):
            baza = g("ilosc") if isinstance(g("ilosc"), (int, float)) else sumy.get(ident, 0)
            ilosc = zaokr_gora(baza * (1 + zapas), jm)
        if not ilosc:
            continue
        cena = g("cena")
        wynik.append({"id": ident, "nazwa": str(g("nazwa") or ""), "jm": jm, "kategoria": kat,
                      "ilosc": float(ilosc), "cena": float(cena) if isinstance(cena, (int, float)) else 0.0,
                      "pozycje": str(g("poz") or ""), "uwagi": str(g("uwagi") or "")})
    if not wynik:
        raise ValueError("Nie znaleziono materiałów – sprawdź, czy to plik z listą materiałów.")
    return wynik


# ============================================================ AI – podział na etapy

SYSTEM_HARM = """Jesteś doświadczonym kierownikiem budowy i zaopatrzeniowcem w firmie wykonującej termomodernizacje, \
elewacje i dachy. Układasz harmonogram robót i plan dostaw materiałów. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em."""

POLECENIE_HARM = """Ułóż harmonogram robót w {n} etapach (etap = {dl} dni kalendarzowych, start {start}, \
zespół wykonawczy: {brygady}) i rozdziel dostawy materiałów na etapy.

ZASADY:
1. Kolejność technologiczna: rusztowania, siatki i daszki → zabezpieczenie stolarki, demontaże (obróbki, rynny, \
osprzęt) → skucie tynków, oczyszczenie, gruntowanie → klejenie izolacji i kołkowanie → warstwa zbrojona → podkład \
i tynk → malowanie → obróbki blacharskie, parapety, rynny i rury → odgromowa, osprzęt, budki → demontaż rusztowań \
i odbiór. Dach może iść równolegle, jeśli liczba pracowników na to pozwala (rozbiórka → konstrukcja → izolacje → \
pokrycie → obróbki). Tempo robót dopasuj do liczby pracowników (typowe wydajności ekip elewacyjnych i dekarskich); \
dla każdego etapu podaj w "obsada" podział ludzi na fronty robót, np. "4 os. elewacja południowa, 2 os. dach". \
Jeśli pracowników jest za mało, by zmieścić zakres w {n} etapach, napisz to wyraźnie w "uwagi" i podaj, ilu brakuje.
2. Materiał dostarczamy na początek etapu, w którym jest zużywany (dostawa „just in time”). Materiały zużywane \
w kilku etapach dziel procentowo zgodnie z postępem robót. Materiały na roboty mokre (klej, tynk) zamawiaj z \
wyprzedzeniem pełnego etapu. Ostatni etap zwykle nie ma dostaw.
3. Dla każdego materiału podaj typowy czas realizacji zamówienia w hurtowni w dniach roboczych (np. styropian 2–5, \
tytan-cynk 7–10, PIR 5–10, tynki i farby barwione 3–5, towar z magazynu 1–2).
4. Uwzględnij ograniczenia: temperatura min. +5°C dla klejów, tynków i farb; okres lęgowy ptaków – przyjmij 1.03–15.10 \
(gniazda w budynku usuwa się bez zezwolenia tylko od 16.10 do końca lutego i tylko ze względów bezpieczeństwa lub sanitarnych – \
§ 9 rozporządzenia MŚ z 16.12.2016 w sprawie ochrony gatunkowej zwierząt; w sezonie – zezwolenie RDOŚ, art. 56 ustawy o ochronie \
przyrody); przy termomodernizacji budynku z gniazdami lub schronieniami (jerzyki, wróble, nietoperze) potrzebna ekspertyza \
ornitologiczna / chiropterologiczna przed robotami; przy wycince drzew i krzewów – sprawdzenie gniazd (art. 83c ust. 1–2 ustawy \
o ochronie przyrody); dokładne terminy zależą od gatunku i decyzji RDOŚ; dostępność rusztowań. Zapisz je w "uwagi".
5. "udzialy" to lista {n} liczb (ułamki 0–1) sumujących się do 1 – udział ilości materiału dostarczany na \
początek każdego etapu.
{wskazowki}

SCHEMAT:
{{
 "etapy": [{{"nr": 1, "nazwa": "Rusztowania i przygotowanie", "prace": ["..."], "pozycje": [1, 2],
   "obsada": "4 os. rusztowania, 2 os. demontaże"}}],
 "podzial": [{{"id": "M1", "udzialy": [0.7, 0.3, 0, 0, 0], "czas_realizacji_dni": 3}}],
 "uwagi": ["..."]
}}

MATERIAŁY (id | nazwa | j.m. | ilość do zamówienia | kategoria | pozycje kosztorysu):
{materialy}
{kosztorys}"""


def zbuduj_polecenie_harm(materialy, pozycje, start, n, dl, brygady, wskazowki):
    mat = "\n".join(f"{m['id']} | {m['nazwa']} | {m['jm']} | {m['ilosc']:g} | {m['kategoria']} | {m['pozycje']}"
                    for m in materialy)
    ksz = ""
    if pozycje:
        ksz = "\nKOSZTORYS (lp | dział | opis | j.m. | ilość):\n" + "\n".join(
            f"{p['lp']} | {p['dzial']} | {p['opis'][:140]} | {p['jm']} | {p['ilosc']:g}" for p in pozycje if p["ilosc"] > 0)
    return POLECENIE_HARM.format(n=n, dl=dl, start=start.strftime("%d.%m.%Y"), brygady=brygady,
                                 wskazowki=f"6. Wskazówki użytkownika: {wskazowki}" if wskazowki else "",
                                 materialy=mat, kosztorys=ksz)


def podzial_ilosci(ilosc, udzialy, jm):
    """Dzieli ilość na etapy z zaokrągleniem w górę narastająco (suma = ilość)."""
    wyn, pop, narast = [], 0.0, 0.0
    for u in udzialy:
        narast += u
        cel = zaokr_gora(ilosc * min(narast, 1.0), jm) if narast < 0.9999 else ilosc
        wyn.append(round(max(cel - pop, 0), 3))
        pop = cel
    return wyn


def przygotuj_plan(dane, materialy, start, n, dl):
    etapy = sorted(dane.get("etapy", []), key=lambda e: e.get("nr", 0))[:n]
    while len(etapy) < n:
        etapy.append({"nr": len(etapy) + 1, "nazwa": f"Etap {len(etapy) + 1}", "prace": [], "pozycje": []})
    for i, e in enumerate(etapy):
        e["nr"] = i + 1
        e["od"] = start + dt.timedelta(days=i * dl)
        e["do"] = start + dt.timedelta(days=(i + 1) * dl - 1)
    pd = {p.get("id"): p for p in dane.get("podzial", [])}
    for m in materialy:
        p = pd.get(m["id"], {})
        u = [max(float(x or 0), 0) for x in (p.get("udzialy") or [])][:n]
        u += [0.0] * (n - len(u))
        s = sum(u)
        m["udzialy"] = [x / s for x in u] if s > 0 else [1.0] + [0.0] * (n - 1)
        m["realizacja"] = int(p.get("czas_realizacji_dni") or 3)
        m["ilosci"] = podzial_ilosci(m["ilosc"], m["udzialy"], m["jm"])
    return etapy


def termin_zamowienia(etap_od, dni_rob):
    d, zostalo = etap_od, dni_rob + 1  # +1 dzień zapasu
    while zostalo > 0:
        d -= dt.timedelta(days=1)
        if not _wolny(d):
            zostalo -= 1
    return d


# ============================================================ Excel harmonogramu

def zapisz_harmonogram(sciezka, budowa, adres, etapy, materialy, uwagi, zespol=""):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter as L

    F = lambda **k: Font(name="Arial", size=k.pop("size", 9), **k)
    zolty = PatternFill("solid", fgColor="FFF2CC")
    szary = PatternFill("solid", fgColor="D9E1F2")
    cz = Side(style="thin", color="999999")
    ramka = Border(left=cz, right=cz, top=cz, bottom=cz)
    zaw = Alignment(wrap_text=True, vertical="top")
    n = len(etapy)

    def naglowek(ws, r, teksty, szer=None):
        for i, t in enumerate(teksty, 1):
            c = ws.cell(r, i, t)
            c.font = F(bold=True)
            c.fill = szary
            c.border = ramka
            c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")

    wb = openpyxl.Workbook()
    # --- Plan robót
    p = wb.active
    p.title = "Plan robót"
    for k, s in zip("ABCDEFG", (6, 30, 14, 14, 70, 18, 34)):
        p.column_dimensions[k].width = s
    p["A1"] = f"HARMONOGRAM ROBÓT I DOSTAW – {budowa}"
    p["A1"].font = F(size=12, bold=True)
    p["A2"] = f"Adres budowy / dostaw: {adres}" + (f"   Zespół: {zespol}" if zespol else "")
    p["A2"].font = F()
    naglowek(p, 4, ["Etap", "Nazwa", "Od", "Do", "Zakres prac", "Pozycje kosztorysu", "Obsada (pracownicy)"])
    for i, e in enumerate(etapy, 5):
        for j, v in enumerate([e["nr"], e.get("nazwa", ""), e["od"], e["do"], "\n".join("• " + x for x in e.get("prace", [])),
                               ", ".join(str(x) for x in e.get("pozycje", [])), e.get("obsada", "")], 1):
            c = p.cell(i, j, v)
            c.font = F()
            c.border = ramka
            c.alignment = zaw
            if j in (3, 4):
                c.number_format = "DD.MM.YYYY"
    r = 6 + n
    p.cell(r, 2, "Uwagi i ograniczenia").font = F(bold=True)
    for u in uwagi:
        r += 1
        c = p.cell(r, 2, "• " + u)
        c.font = F()
        c.alignment = zaw
        p.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        p.row_dimensions[r].height = 26

    # --- Podział dostaw
    d = wb.create_sheet("Podział dostaw")
    kpct, kq = 8, 8 + n + 1          # kolumny: % etapów, suma %, ilości etapów
    nag = ["Lp.", "ID", "Materiał", "Jm", "Ilość do zamówienia", "Cena szac. netto [zł]", "Realizacja [dni rob.]"]
    nag += [f"% etap {e['nr']}" for e in etapy] + ["Suma %"] + [f"Ilość etap {e['nr']}\n(dostawa {e['od']:%d.%m})"
                                                                   for e in etapy]
    d["A1"] = "PODZIAŁ DOSTAW NA ETAPY – żółte pola (% na etap) można zmieniać; suma w wierszu musi dać 100%."
    d["A1"].font = F(bold=True)
    naglowek(d, 3, nag)
    for k, s in zip(range(1, 8), (5, 6, 44, 6, 12, 11, 10)):
        d.column_dimensions[L(k)].width = s
    for k in range(kpct, kq + n):
        d.column_dimensions[L(k)].width = 11
    d.freeze_panes = "D4"
    r0 = 4
    for i, m in enumerate(materialy):
        r = r0 + i
        vals = [i + 1, m["id"], m["nazwa"], m["jm"], m["ilosc"], m["cena"], m["realizacja"]]
        for j, v in enumerate(vals, 1):
            c = d.cell(r, j, v)
            c.font = F(color="FF0000" if j == 6 else "000000")
            c.border = ramka
        d.cell(r, 5).number_format = "#,##0.0"
        d.cell(r, 6).number_format = "#,##0.00"
        for k in range(n):
            c = d.cell(r, kpct + k, round(m["udzialy"][k], 4))
            c.number_format = "0%"
            c.fill = zolty
            c.border = ramka
        pierwsza, ostatnia = L(kpct), L(kpct + n - 1)
        c = d.cell(r, kpct + n, f"=SUM({pierwsza}{r}:{ostatnia}{r})")
        c.number_format = "0%"
        c.border = ramka
        dec = f'IF(OR(D{r}="m3",D{r}="kg",D{r}="t",D{r}="l"),1,0)'
        for k in range(n):
            nar = f"SUM(${pierwsza}{r}:{L(kpct + k)}{r})"
            pop = f"SUM(${pierwsza}{r}:{L(kpct + k - 1)}{r})" if k else "0"
            f = (f"=IF({nar}>=0.9999,E{r},ROUNDUP(E{r}*{nar},{dec}))"
                 f"-IF({pop}>=0.9999,E{r},ROUNDUP(E{r}*{pop},{dec}))") if k else \
                f"=IF({nar}>=0.9999,E{r},ROUNDUP(E{r}*{nar},{dec}))"
            c = d.cell(r, kq + k, f)
            c.number_format = "#,##0.0"
            c.border = ramka
    rk = r0 + len(materialy)
    d.cell(rk + 1, 3, "Wartość dostaw w etapie (netto, szacunkowo)").font = F(bold=True)
    for k in range(n):
        col = L(kq + k)
        c = d.cell(rk + 1, kq + k, f"=SUMPRODUCT({col}{r0}:{col}{rk - 1},$F${r0}:$F${rk - 1})")
        c.number_format = "#,##0.00"
        c.font = F(bold=True)
    d.cell(rk + 2, 3, "Zamówić najpóźniej do (dla materiałów o najdłuższym czasie realizacji)").font = F(italic=True)
    for k, e in enumerate(etapy):
        dl = max([m["realizacja"] for m in materialy if m["ilosci"][k] > 0] or [0])
        if dl:
            c = d.cell(rk + 2, kq + k, termin_zamowienia(e["od"], dl))
            c.number_format = "DD.MM.YYYY"
            c.font = F(italic=True)

    # --- Zamówienia na etapy
    for k, e in enumerate(etapy):
        lista = [(i, m) for i, m in enumerate(materialy) if m["ilosci"][k] > 0]
        if not lista:
            continue
        z = wb.create_sheet(f"Etap {e['nr']}")
        for kk, s in zip("ABCDEFGH", (5, 46, 6, 12, 12, 14, 14, 40)):
            z.column_dimensions[kk].width = s
        z["A1"] = f"ZAMÓWIENIE – etap {e['nr']}: {e.get('nazwa','')} ({e['od']:%d.%m.%Y} – {e['do']:%d.%m.%Y})"
        z["A1"].font = F(size=11, bold=True)
        z["A2"] = f"Dostawa na: {data_pl(e['od'])}, adres: {adres}"
        z["A2"].font = F()
        naglowek(z, 4, ["Lp.", "Materiał", "Jm", "Ilość", "Cena szac. netto", "Wartość netto", "Zamówić do", "Uwagi"])
        for j, (i, m) in enumerate(lista, 5):
            rr = r0 + i
            vals = [j - 4, m["nazwa"], m["jm"], f"='Podział dostaw'!{L(kq + k)}{rr}",
                    f"='Podział dostaw'!F{rr}", f"=ROUND(D{j}*E{j},2)", termin_zamowienia(e["od"], m["realizacja"]),
                    m.get("uwagi", "")[:200]]
            for c_i, v in enumerate(vals, 1):
                c = z.cell(j, c_i, v)
                c.font = F(color="FF0000" if c_i == 5 else "000000")
                c.border = ramka
                c.alignment = zaw
            z.cell(j, 4).number_format = "#,##0.0"
            z.cell(j, 5).number_format = "#,##0.00"
            z.cell(j, 6).number_format = "#,##0.00"
            z.cell(j, 7).number_format = "DD.MM.YYYY"
        ost = 4 + len(lista)
        z.cell(ost + 1, 2, "Razem (netto, szacunkowo)").font = F(bold=True)
        c = z.cell(ost + 1, 6, f"=SUM(F5:F{ost})")
        c.number_format = "#,##0.00"
        c.font = F(bold=True)
    wb.save(sciezka)


def wczytaj_harmonogram(sciezka_json):
    """Wczytuje metadane (JSON) i aktualny podział (% z Excela, jeśli zmieniony)."""
    with open(sciezka_json, encoding="utf-8") as f:
        h = json.load(f)
    for e in h["etapy"]:
        e["od"] = dt.date.fromisoformat(e["od"])
        e["do"] = dt.date.fromisoformat(e["do"])
    n = len(h["etapy"])
    xlsx = os.path.splitext(sciezka_json)[0] + ".xlsx"
    if os.path.isfile(xlsx):
        try:
            import openpyxl
            ws = openpyxl.load_workbook(xlsx, data_only=True)["Podział dostaw"]
            po_id = {m["id"]: m for m in h["materialy"]}
            for row in ws.iter_rows(min_row=4, values_only=True):
                m = po_id.get(str(row[1])) if row and row[1] else None
                if not m:
                    continue
                if isinstance(row[4], (int, float)):
                    m["ilosc"] = float(row[4])
                if isinstance(row[5], (int, float)):
                    m["cena"] = float(row[5])
                if isinstance(row[6], (int, float)):
                    m["realizacja"] = int(row[6])
                u = [row[7 + k] if isinstance(row[7 + k], (int, float)) else 0 for k in range(n)]
                s = sum(u)
                if s > 0:
                    m["udzialy"] = [x / s for x in u]
        except Exception:
            pass
    for m in h["materialy"]:
        m["ilosci"] = podzial_ilosci(m["ilosc"], m["udzialy"], m["jm"])
    return h


# ============================================================ zamówienia – e-mail i załącznik

def materialy_dla(h, etap_idx, hurtownia):
    klucze = [norm(k) for k in re.split(r"[,;]", hurtownia.get("kategorie", "")) if k.strip()]
    wyn = []
    for m in h["materialy"]:
        il = m["ilosci"][etap_idx]
        if il <= 0:
            continue
        if klucze and not any(k in norm(m["kategoria"] + " " + m["nazwa"]) for k in klucze):
            continue
        wyn.append(dict(m, ilosc_etap=il))
    return wyn


def zapisz_zalacznik(sciezka, h, etap, hurt, mats, typ, cfg):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    F = lambda **k: Font(name="Arial", size=k.pop("size", 10), **k)
    cz = Side(style="thin", color="999999")
    ramka = Border(left=cz, right=cz, top=cz, bottom=cz)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zamówienie" if typ == "zamowienie" else "Zapytanie ofertowe"
    zap = typ != "zamowienie"
    ws["A1"] = ("ZAPYTANIE OFERTOWE" if zap else "ZAMÓWIENIE") + f" – materiały budowlane, etap {etap['nr']}"
    ws["A1"].font = F(size=13, bold=True)
    info = [("Zamawiający", f"{cfg.get('firma_nazwa','')}, {cfg.get('firma_adres','')}"),
            ("NIP", cfg.get("firma_nip", "")),
            ("Kontakt", f"{cfg.get('firma_osoba','')}, tel. {cfg.get('firma_tel','')}, {cfg.get('firma_email','')}"),
            ("Dostawca", f"{hurt.get('nazwa','')} ({hurt.get('email','')})"),
            ("Budowa", h.get("budowa", "")), ("Adres dostawy", h.get("adres", "")),
            ("Termin dostawy", data_pl(etap["od"]))]
    for i, (a, b) in enumerate(info, 3):
        ws.cell(i, 1, a).font = F(bold=True)
        ws.cell(i, 2, b).font = F()
    r = 3 + len(info) + 1
    nag = ["Lp.", "Materiał", "Jm", "Ilość", "Uwagi / wymagania"]
    if zap:
        nag += ["Oferowany produkt / producent", "Cena jedn. netto [zł]", "Wartość netto [zł]", "Termin realizacji"]
    for i, t in enumerate(nag, 1):
        c = ws.cell(r, i, t)
        c.font = F(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
        c.border = ramka
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for j, m in enumerate(mats, 1):
        rr = r + j
        vals = [j, m["nazwa"], m["jm"], m["ilosc_etap"], m.get("uwagi", "")[:250]]
        if zap:
            vals += ["", None, f"=IF(G{rr}=\"\",\"\",ROUND(D{rr}*G{rr},2))", ""]
        for i, v in enumerate(vals, 1):
            c = ws.cell(rr, i, v)
            c.font = F()
            c.border = ramka
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if zap and i in (6, 7, 9):
                c.fill = PatternFill("solid", fgColor="FFF2CC")
        ws.cell(rr, 4).number_format = "#,##0.0"
    if zap:
        k = r + len(mats) + 1
        ws.cell(k, 2, "RAZEM netto").font = F(bold=True)
        ws.cell(k, 8, f"=SUM(H{r + 1}:H{k - 1})").font = F(bold=True)
    for kk, s in zip("ABCDEFGHI", (18, 50, 7, 11, 40, 26, 14, 14, 14)):
        ws.column_dimensions[kk].width = s
    wb.save(sciezka)


def tresc_maila(h, etap, hurt, mats, typ, cfg, dopisek, termin_odp):
    zap = typ != "zamowienie"
    budowa = h.get("budowa", "")
    temat = (f"Zapytanie ofertowe – materiały – {budowa} – etap {etap['nr']}" if zap
             else f"Zamówienie materiałów – {budowa} – etap {etap['nr']} (dostawa {etap['od']:%d.%m.%Y})")
    osoba = hurt.get("osoba", "").strip()
    powit = f"Dzień dobry{', ' + osoba if osoba else ''},"
    if zap:
        wstep = (f"w imieniu firmy {cfg.get('firma_nazwa','')} prosimy o przedstawienie oferty cenowej na materiały "
                 f"budowlane wymienione poniżej (również w załączonym arkuszu).")
        prosba = ("Prosimy o podanie cen jednostkowych netto, oferowanych produktów, terminu realizacji, kosztów "
                  "transportu i warunków płatności" + (f" do dnia {termin_odp}." if termin_odp else "."))
    else:
        wstep = (f"w imieniu firmy {cfg.get('firma_nazwa','')} zamawiamy materiały budowlane wymienione poniżej "
                 f"(również w załączonym arkuszu).")
        prosba = "Prosimy o potwierdzenie przyjęcia zamówienia, terminu dostawy oraz cen."
    dane = [f"Budowa: {budowa}", f"Adres dostawy: {h.get('adres','')}",
            f"Termin dostawy: {data_pl(etap['od'])} (etap {etap['nr']}: {etap.get('nazwa','')})",
            "Warunki: dostawa na budowę z rozładunkiem; do dostawy dokument WZ oraz deklaracje właściwości użytkowych."]
    tabela_txt = "\n".join(f"{i}. {m['nazwa']} – {il_pl(m['ilosc_etap'])} {m['jm']}" for i, m in enumerate(mats, 1))
    podpis = [cfg.get("firma_osoba", ""), cfg.get("firma_nazwa", ""), cfg.get("firma_adres", ""),
              " ".join(x for x in [f"tel. {cfg['firma_tel']}" if cfg.get("firma_tel") else "",
                                   f"e-mail: {cfg['firma_email']}" if cfg.get("firma_email") else ""] if x)]
    podpis = [p for p in podpis if p and p.strip()]
    tekst = "\n".join([powit, "", wstep, "", *dane, "", tabela_txt, "", prosba] +
                      ([dopisek, ""] if dopisek else [""]) + ["Z poważaniem", *podpis])
    e = html.escape
    wiersze = "".join(f"<tr><td style='padding:4px 8px;border:1px solid #bbb'>{i}</td>"
                      f"<td style='padding:4px 8px;border:1px solid #bbb'>{e(m['nazwa'])}</td>"
                      f"<td style='padding:4px 8px;border:1px solid #bbb;text-align:right'>{il_pl(m['ilosc_etap'])}</td>"
                      f"<td style='padding:4px 8px;border:1px solid #bbb'>{e(m['jm'])}</td></tr>"
                      for i, m in enumerate(mats, 1))
    html_tresc = (f"<div style='font-family:Arial;font-size:14px'><p>{e(powit)}</p><p>{e(wstep)}</p><p>"
                  + "<br>".join(e(x) for x in dane) + "</p>"
                  "<table style='border-collapse:collapse;font-size:13px'><tr style='background:#d9e1f2'>"
                  "<th style='padding:4px 8px;border:1px solid #bbb'>Lp.</th><th style='padding:4px 8px;border:1px solid #bbb'>"
                  "Materiał</th><th style='padding:4px 8px;border:1px solid #bbb'>Ilość</th>"
                  f"<th style='padding:4px 8px;border:1px solid #bbb'>Jm</th></tr>{wiersze}</table>"
                  f"<p>{e(prosba)}</p>" + (f"<p>{e(dopisek)}</p>" if dopisek else "")
                  + "<p>Z poważaniem<br>" + "<br>".join(e(p) for p in podpis) + "</p></div>")
    return temat, tekst, html_tresc


def zbuduj_wiadomosc(cfg, hurt, temat, tekst, html_tresc, zalacznik, szkic):
    msg = EmailMessage()
    msg["Subject"] = temat
    msg["From"] = cfg.get("smtp_nadawca") or cfg.get("firma_email") or ""
    msg["To"] = hurt["email"]
    if cfg.get("kopia_do_mnie") and (cfg.get("smtp_nadawca") or cfg.get("firma_email")):
        msg["Cc"] = cfg.get("smtp_nadawca") or cfg.get("firma_email")
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    if szkic:
        msg["X-Unsent"] = "1"
    msg.set_content(tekst)
    msg.add_alternative(html_tresc, subtype="html")
    with open(zalacznik, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           filename=os.path.basename(zalacznik))
    return msg


def wyslij_smtp(cfg, wiadomosci):
    host, port = cfg.get("smtp_serwer", "").strip(), int(cfg.get("smtp_port") or 587)
    if not host:
        raise ValueError("Uzupełnij ustawienia SMTP (serwer, port, login, hasło) w zakładce Ustawienia.")
    import bezpieczenstwo as _BZ  # H1-09: tylko porty 25/465/587/2525 i publiczne adresy (po rozwiązaniu DNS, także IPv6)
    try:
        s = _BZ.polacz_smtp(host, port, timeout=60)
    except _BZ.BladSMTP as e:
        raise ValueError(str(e))
    try:
        if cfg.get("smtp_login"):
            s.login(cfg["smtp_login"], cfg.get("smtp_haslo", ""))
        for m in wiadomosci:
            s.send_message(m)
    finally:
        s.quit()


# ============================================================ interfejs – Harmonogram

def nastepny_poniedzialek():
    d = dt.date.today() + dt.timedelta(days=1)
    while d.weekday() != 0:
        d += dt.timedelta(days=1)
    return d


class ZakladkaHarmonogram(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.plik_json = None
        f = ttk.Frame(self, padding=10)
        f.pack(fill="x")
        f.columnconfigure(1, weight=1)
        ttk.Label(f, text="Lista materiałów (xlsx):").grid(row=0, column=0, sticky="w")
        self.var_lista = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_lista).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(f, text="Wybierz…", command=lambda: self._wybierz(self.var_lista, "Lista materiałów")).grid(row=0, column=2)
        ttk.Label(f, text="Kosztorys (opcjonalnie):").grid(row=1, column=0, sticky="w", pady=4)
        self.var_koszt = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_koszt).grid(row=1, column=1, sticky="ew", padx=6)
        ttk.Button(f, text="Wybierz…", command=lambda: self._wybierz(self.var_koszt, "Kosztorys")).grid(row=1, column=2)
        ttk.Label(f, text="Nazwa budowy:").grid(row=2, column=0, sticky="w")
        self.var_budowa = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_budowa).grid(row=2, column=1, sticky="ew", padx=6)
        ttk.Label(f, text="Adres dostaw (budowy):").grid(row=3, column=0, sticky="w", pady=4)
        self.var_adres = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_adres).grid(row=3, column=1, sticky="ew", padx=6)

        p = ttk.Frame(self, padding=(10, 0))
        p.pack(fill="x")
        ttk.Label(p, text="Start robót (DD.MM.RRRR):").pack(side="left")
        self.var_start = tk.StringVar(value=nastepny_poniedzialek().strftime("%d.%m.%Y"))
        ttk.Entry(p, textvariable=self.var_start, width=12).pack(side="left", padx=6)
        ttk.Label(p, text="Liczba etapów:").pack(side="left", padx=(12, 0))
        self.var_n = tk.IntVar(value=5)
        ttk.Spinbox(p, from_=1, to=30, textvariable=self.var_n, width=5).pack(side="left", padx=6)
        ttk.Label(p, text="Długość etapu [dni]:").pack(side="left", padx=(12, 0))
        self.var_dl = tk.IntVar(value=7)
        ttk.Spinbox(p, from_=1, to=60, textvariable=self.var_dl, width=5).pack(side="left", padx=6)
        ttk.Label(p, text="Brygady:").pack(side="left", padx=(12, 0))
        self.var_bryg = tk.IntVar(value=2)
        ttk.Spinbox(p, from_=1, to=10, textvariable=self.var_bryg, width=4).pack(side="left", padx=6)

        ttk.Label(self, text="Wskazówki dla AI (np. „dach i elewacja równolegle”, „rusztowania stawiamy w dwóch "
                             "etapach”, „tytan-cynk zamówić wcześniej”):").pack(anchor="w", padx=10, pady=(8, 0))
        self.txt_wsk = tk.Text(self, height=3, wrap="word", font=("Segoe UI", 10))
        self.txt_wsk.pack(fill="x", padx=10)
        a = ttk.Frame(self, padding=10)
        a.pack(fill="x")
        ttk.Button(a, text="🗓 Podziel materiały na etapy", style="Akcent.TButton", command=self.generuj).pack(side="left")
        ttk.Button(a, text="📂 Otwórz harmonogram", command=self.otworz).pack(side="left", padx=6)
        ttk.Button(a, text="✉ Przejdź do zamówień", command=self.do_zamowien).pack(side="left", padx=6)

        kol = (("nr", "Etap", 50), ("nazwa", "Nazwa", 260), ("od", "Od", 110), ("do", "Do", 110),
               ("zam", "Zamówić do", 110), ("n", "Materiałów", 90), ("wart", "Dostawy netto", 120))
        self.tree = ttk.Treeview(self, columns=[k for k, _, _ in kol], show="headings", height=8)
        for k, t, w in kol:
            self.tree.heading(k, text=t)
            self.tree.column(k, width=w, anchor="w" if k == "nazwa" else "center")
        self.tree.pack(fill="both", expand=True, padx=10)
        self.txt = tk.Text(self, height=7, wrap="word", font=("Segoe UI", 10), state="disabled", background="#fafafa",
                           relief="flat", padx=10, pady=6)
        self.txt.pack(fill="x", padx=10, pady=(6, 10))

    def _wybierz(self, var, co):
        s = filedialog.askopenfilename(title=f"Wybierz: {co}", filetypes=[("Excel", "*.xlsx")])
        if s:
            var.set(s)
            if var is self.var_lista:
                self._uzupelnij()

    def ustaw_liste(self, sciezka):
        self.var_lista.set(sciezka)
        self._uzupelnij()

    def _uzupelnij(self):
        s = self.var_lista.get()
        nazwa = re.sub(r"^Lista_materialow_", "", os.path.splitext(os.path.basename(s))[0])
        k = os.path.join(os.path.dirname(s), f"Kosztorys_ofertowy_{nazwa}.xlsx")
        if os.path.isfile(k) and not self.var_koszt.get():
            self.var_koszt.set(k)
        if not self.var_budowa.get():
            self.var_budowa.set(nazwa.replace("_", " "))

    def generuj(self):
        cfg = self.app.cfg
        if not cfg.get("api_key"):
            messagebox.showwarning("Harmonogram", "Najpierw wpisz klucz API Claude w Ustawieniach.")
            return
        try:
            materialy = wczytaj_liste(self.var_lista.get())
            start = parsuj_date(self.var_start.get())
            n, dl, bryg = int(self.var_n.get()), int(self.var_dl.get()), int(self.var_bryg.get())
        except Exception as e:
            messagebox.showerror("Harmonogram", str(e))
            return
        pozycje = []
        if self.var_koszt.get().strip():
            try:
                pozycje = wczytaj_kosztorys(self.var_koszt.get().strip())[1]
            except Exception as e:
                self.app.log(f"Harmonogram: nie odczytano kosztorysu ({e}) – AI użyje tylko listy materiałów")
        meta = {"budowa": self.var_budowa.get().strip() or "budowa", "adres": self.var_adres.get().strip()}
        if not meta["adres"]:
            if not messagebox.askyesno("Harmonogram", "Nie podano adresu dostaw. Kontynuować? "
                                                      "(adres możesz uzupełnić później w zakładce Zamówienia)"):
                return
        wsk = self.txt_wsk.get("1.0", "end").strip()
        self.app._start("Układam harmonogram i podział dostaw…", self._w_generuj, json.loads(json.dumps(cfg)),
                        materialy, pozycje, start, n, dl, bryg, wsk, meta)

    def _w_generuj(self, cfg, materialy, pozycje, start, n, dl, bryg, wsk, meta):
        content = [{"type": "text", "text": zbuduj_polecenie_harm(materialy, pozycje, start, n, dl, bryg, wsk)}]
        try:
            txt, _ = claude_stream(cfg, SYSTEM_HARM, content, max_tokens=16000,
                                   postep=lambda k: self.app.q.put(("status", f"AI układa harmonogram… ({k // 1000} tys. znaków)")))
        except urllib.error.HTTPError as e:
            self.app.q.put(("koniec", f"Błąd API {e.code}: {e.read().decode('utf-8', 'ignore')[:400]}"))
            return
        dane = wyciagnij_json(txt)
        etapy = przygotuj_plan(dane, materialy, start, n, dl)
        folder = os.path.dirname(self.var_lista.get())
        nazwa = re.sub(r"[^\w\-]+", "_", meta["budowa"]).strip("_")[:60] or "budowa"
        xlsx = os.path.join(folder, f"Harmonogram_dostaw_{nazwa}.xlsx")
        zapisz_harmonogram(xlsx, meta["budowa"], meta["adres"], etapy, materialy, dane.get("uwagi", []))
        js = os.path.splitext(xlsx)[0] + ".json"
        with open(js, "w", encoding="utf-8") as f:
            json.dump({**meta, "etapy": [dict(e, od=e["od"].isoformat(), do=e["do"].isoformat()) for e in etapy],
                       "materialy": materialy, "uwagi": dane.get("uwagi", [])}, f, ensure_ascii=False, indent=1)
        self.app.q.put(("wywolaj", self.pokaz, (js,)))
        self.app.q.put(("koniec", f"Harmonogram dostaw gotowy: {n} etapów."))

    def pokaz(self, js):
        self.plik_json = js
        h = wczytaj_harmonogram(js)
        self.tree.delete(*self.tree.get_children())
        for k, e in enumerate(h["etapy"]):
            mats = [m for m in h["materialy"] if m["ilosci"][k] > 0]
            wart = sum(m["ilosci"][k] * m["cena"] for m in mats)
            dl = max([m["realizacja"] for m in mats] or [0])
            self.tree.insert("", "end", values=(e["nr"], e.get("nazwa", ""), data_pl(e["od"]), data_pl(e["do"]),
                                                 f"{termin_zamowienia(e['od'], dl):%d.%m.%Y}" if mats else "–",
                                                 len(mats), zl(wart) if mats else "–"))
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        for u in h.get("uwagi", []):
            self.txt.insert("end", "• " + u + "\n")
        self.txt.insert("end", f"\nPlik: {os.path.splitext(js)[0]}.xlsx – podział % możesz zmienić w arkuszu "
                               "„Podział dostaw”; zamówienia uwzględnią zmiany.\n")
        self.txt.configure(state="disabled")
        tab = getattr(self.app, "tab_zamowienia", None)
        if tab is not None:
            tab.ustaw_harmonogram(js)
        self.otworz()

    def otworz(self):
        if self.plik_json:
            try:
                os.startfile(os.path.splitext(self.plik_json)[0] + ".xlsx")
            except AttributeError:
                pass

    def do_zamowien(self):
        tab = getattr(self.app, "tab_zamowienia", None)
        if tab is not None:
            if self.plik_json:
                tab.ustaw_harmonogram(self.plik_json)
            self.app.nb.select(tab)


# ============================================================ interfejs – Zamówienia

class OknoHurtowni(tk.Toplevel):
    def __init__(self, master, dane=None):
        super().__init__(master)
        self.title("Hurtownia")
        self.resizable(False, False)
        self.wynik = None
        self.vars = {}
        pola = [("nazwa", "Nazwa hurtowni"), ("email", "E-mail"), ("osoba", "Osoba kontaktowa"),
                ("kategorie", "Asortyment – słowa kluczowe, po przecinku\n(puste = wszystkie materiały)"),
                ("uwagi", "Uwagi")]
        for i, (k, t) in enumerate(pola):
            ttk.Label(self, text=t).grid(row=i, column=0, sticky="w", padx=10, pady=4)
            v = tk.StringVar(value=(dane or {}).get(k, ""))
            ttk.Entry(self, textvariable=v, width=50).grid(row=i, column=1, padx=10, pady=4)
            self.vars[k] = v
        ttk.Label(self, text="Przykład asortymentu: „blach, tytan, rynn” – hurtownia dostanie tylko blacharkę.",
                  foreground="#777").grid(row=len(pola), column=0, columnspan=2, padx=10)
        b = ttk.Frame(self)
        b.grid(row=len(pola) + 1, column=0, columnspan=2, pady=10)
        ttk.Button(b, text="Zapisz", command=self.ok).pack(side="left", padx=6)
        ttk.Button(b, text="Anuluj", command=self.destroy).pack(side="left")
        self.grab_set()

    def ok(self):
        d = {k: v.get().strip() for k, v in self.vars.items()}
        if not d["nazwa"] or not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", d["email"]):
            messagebox.showerror("Hurtownia", "Podaj nazwę i poprawny adres e-mail.", parent=self)
            return
        self.wynik = d
        self.destroy()


class ZakladkaZamowienia(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.h = None
        self.plik_json = None
        self.historia_plik = os.path.join(app.data_dir, "zamowienia_historia.json")

        g = ttk.Frame(self, padding=10)
        g.pack(fill="x")
        ttk.Label(g, text="Harmonogram dostaw:").pack(side="left")
        self.var_plik = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_plik, width=70).pack(side="left", padx=6, fill="x", expand=True)
        ttk.Button(g, text="Wybierz…", command=self.wybierz).pack(side="left")

        o = ttk.Frame(self, padding=(10, 0))
        o.pack(fill="x")
        ttk.Label(o, text="Etap:").pack(side="left")
        self.cb_etap = ttk.Combobox(o, state="readonly", width=45)
        self.cb_etap.pack(side="left", padx=6)
        self.cb_etap.bind("<<ComboboxSelected>>", lambda e: self.podglad())
        self.var_typ = tk.StringVar(value="zapytanie")
        ttk.Radiobutton(o, text="Zapytanie ofertowe", variable=self.var_typ, value="zapytanie",
                        command=self.podglad).pack(side="left", padx=(16, 4))
        ttk.Radiobutton(o, text="Zamówienie", variable=self.var_typ, value="zamowienie",
                        command=self.podglad).pack(side="left", padx=4)
        ttk.Label(o, text="Odpowiedź do:").pack(side="left", padx=(16, 0))
        self.var_termin = tk.StringVar()
        ttk.Entry(o, textvariable=self.var_termin, width=12).pack(side="left", padx=6)

        a = ttk.Frame(self, padding=(10, 6))
        a.pack(fill="x")
        ttk.Label(a, text="Adres dostawy:").pack(side="left")
        self.var_adres = tk.StringVar()
        ttk.Entry(a, textvariable=self.var_adres, width=60).pack(side="left", padx=6, fill="x", expand=True)

        pw = ttk.PanedWindow(self, orient="horizontal")
        pw.pack(fill="both", expand=True, padx=10, pady=4)
        lewa = ttk.Frame(pw)
        ttk.Label(lewa, text="Hurtownie (zaznacz odbiorców – Ctrl+klik):", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        kol = (("nazwa", "Nazwa", 150), ("email", "E-mail", 170), ("kat", "Asortyment", 120))
        self.tree_h = ttk.Treeview(lewa, columns=[k for k, _, _ in kol], show="headings", height=8, selectmode="extended")
        for k, t, w in kol:
            self.tree_h.heading(k, text=t)
            self.tree_h.column(k, width=w)
        self.tree_h.pack(fill="both", expand=True)
        self.tree_h.bind("<<TreeviewSelect>>", lambda e: self.podglad())
        bh = ttk.Frame(lewa)
        bh.pack(fill="x", pady=4)
        ttk.Button(bh, text="➕ Dodaj", command=self.dodaj_h).pack(side="left")
        ttk.Button(bh, text="✏ Edytuj", command=self.edytuj_h).pack(side="left", padx=4)
        ttk.Button(bh, text="🗑 Usuń", command=self.usun_h).pack(side="left")
        ttk.Label(lewa, text="Dopisek do wiadomości (opcjonalnie):").pack(anchor="w", pady=(6, 0))
        self.txt_dop = tk.Text(lewa, height=4, wrap="word", font=("Segoe UI", 10))
        self.txt_dop.pack(fill="x")
        pw.add(lewa, weight=1)

        prawa = ttk.Frame(pw)
        ttk.Label(prawa, text="Podgląd wiadomości (dla pierwszej zaznaczonej hurtowni):",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.txt_pod = tk.Text(prawa, wrap="word", font=("Consolas", 9), state="disabled", background="#fafafa")
        self.txt_pod.pack(fill="both", expand=True)
        pw.add(prawa, weight=2)

        s = ttk.Frame(self, padding=10)
        s.pack(fill="x")
        ttk.Button(s, text="✉ Otwórz jako szkice w programie pocztowym", style="Akcent.TButton",
                   command=lambda: self.wyslij(szkic=True)).pack(side="left")
        ttk.Button(s, text="📤 Wyślij bezpośrednio (SMTP)", command=lambda: self.wyslij(szkic=False)).pack(side="left", padx=8)
        ttk.Button(s, text="📂 Folder zamówień", command=self.otworz_folder).pack(side="left")
        ttk.Label(s, text="Szkice otwierają się w Outlooku / Poczcie Windows z załącznikiem – sprawdzasz i klikasz Wyślij.",
                  foreground="#777").pack(side="left", padx=10)

        ttk.Label(self, text="Historia wysłanych:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        kol = (("data", "Data", 130), ("budowa", "Budowa", 180), ("etap", "Etap", 50), ("typ", "Typ", 120),
               ("hurt", "Hurtownia", 180), ("sposob", "Sposób", 90), ("n", "Pozycji", 60))
        self.tree_hist = ttk.Treeview(self, columns=[k for k, _, _ in kol], show="headings", height=5)
        for k, t, w in kol:
            self.tree_hist.heading(k, text=t)
            self.tree_hist.column(k, width=w)
        self.tree_hist.pack(fill="x", padx=10, pady=(0, 10))
        self.odswiez_h()
        self.odswiez_hist()

    # ---------- dane
    def ustaw_harmonogram(self, js):
        self.var_plik.set(js)
        self.wczytaj()

    def wybierz(self):
        s = filedialog.askopenfilename(title="Wybierz harmonogram dostaw",
                                       filetypes=[("Harmonogram", "Harmonogram_dostaw_*.json *.xlsx"), ("Wszystkie", "*.*")])
        if s:
            if s.lower().endswith(".xlsx"):
                s = os.path.splitext(s)[0] + ".json"
            self.var_plik.set(s)
            self.wczytaj()

    def wczytaj(self):
        try:
            self.h = wczytaj_harmonogram(self.var_plik.get())
        except Exception as e:
            messagebox.showerror("Zamówienia", f"Nie udało się wczytać harmonogramu:\n{e}")
            return
        self.plik_json = self.var_plik.get()
        self.cb_etap["values"] = [f"Etap {e['nr']}: {e.get('nazwa','')} (dostawa {e['od']:%d.%m.%Y})"
                                  for e in self.h["etapy"]]
        if self.h["etapy"]:
            self.cb_etap.current(0)
        self.var_adres.set(self.h.get("adres", ""))
        self.podglad()

    def hurtownie(self):
        return self.app.cfg.setdefault("hurtownie", [])

    def odswiez_h(self):
        self.tree_h.delete(*self.tree_h.get_children())
        for i, h in enumerate(self.hurtownie()):
            self.tree_h.insert("", "end", iid=str(i), values=(h["nazwa"], h["email"], h.get("kategorie", "") or "wszystko"))

    def dodaj_h(self):
        o = OknoHurtowni(self)
        self.wait_window(o)
        if o.wynik:
            self.hurtownie().append(o.wynik)
            self.app.zapisz_cfg()
            self.odswiez_h()

    def edytuj_h(self):
        sel = self.tree_h.selection()
        if not sel:
            return
        i = int(sel[0])
        o = OknoHurtowni(self, self.hurtownie()[i])
        self.wait_window(o)
        if o.wynik:
            self.hurtownie()[i] = o.wynik
            self.app.zapisz_cfg()
            self.odswiez_h()

    def usun_h(self):
        sel = {int(i) for i in self.tree_h.selection()}
        if sel and messagebox.askyesno("Hurtownie", f"Usunąć {len(sel)} hurtowni z listy?"):
            self.app.cfg["hurtownie"] = [h for i, h in enumerate(self.hurtownie()) if i not in sel]
            self.app.zapisz_cfg()
            self.odswiez_h()

    def _etap(self):
        if not self.h or self.cb_etap.current() < 0:
            return None, None
        k = self.cb_etap.current()
        return k, self.h["etapy"][k]

    def podglad(self):
        self.txt_pod.configure(state="normal")
        self.txt_pod.delete("1.0", "end")
        k, etap = self._etap()
        sel = self.tree_h.selection()
        if etap is None:
            self.txt_pod.insert("end", "Wybierz harmonogram dostaw i etap.")
        elif not sel:
            self.txt_pod.insert("end", "Zaznacz hurtownię (lub kilka) na liście po lewej.")
        else:
            h = dict(self.h, adres=self.var_adres.get())
            hurt = self.hurtownie()[int(sel[0])]
            mats = materialy_dla(h, k, hurt)
            if not mats:
                self.txt_pod.insert("end", "Ta hurtownia nie ma w tym etapie żadnych materiałów ze swojego asortymentu.")
            else:
                temat, tekst, _ = tresc_maila(h, etap, hurt, mats, self.var_typ.get(), self.app.cfg,
                                              self.txt_dop.get("1.0", "end").strip(), self.var_termin.get().strip())
                self.txt_pod.insert("end", f"Do: {hurt['email']}\nTemat: {temat}\nZałącznik: arkusz Excel "
                                           f"({len(mats)} pozycji)\n{'-' * 70}\n{tekst}")
        self.txt_pod.configure(state="disabled")

    # ---------- wysyłka
    def wyslij(self, szkic):
        k, etap = self._etap()
        sel = [int(i) for i in self.tree_h.selection()]
        if etap is None or not sel:
            messagebox.showinfo("Zamówienia", "Wybierz harmonogram, etap i co najmniej jedną hurtownię.")
            return
        cfg = self.app.cfg
        if not self.var_adres.get().strip():
            messagebox.showwarning("Zamówienia", "Uzupełnij adres dostawy.")
            return
        h = dict(self.h, adres=self.var_adres.get().strip())
        typ = self.var_typ.get()
        dop = self.txt_dop.get("1.0", "end").strip()
        folder = os.path.join(os.path.dirname(self.plik_json), "zamowienia")
        os.makedirs(folder, exist_ok=True)
        paczki, pominiete = [], []
        for i in sel:
            hurt = self.hurtownie()[i]
            mats = materialy_dla(h, k, hurt)
            if not mats:
                pominiete.append(hurt["nazwa"])
                continue
            nazwa_h = re.sub(r"[^\w\-]+", "_", hurt["nazwa"])[:40]
            nazwa_b = re.sub(r"[^\w\-]+", "_", h.get("budowa", ""))[:40]
            zal = os.path.join(folder, f"{'Zapytanie' if typ != 'zamowienie' else 'Zamowienie'}_{nazwa_b}_etap"
                                       f"{etap['nr']}_{nazwa_h}.xlsx")
            zapisz_zalacznik(zal, h, etap, hurt, mats, typ, cfg)
            temat, tekst, htm = tresc_maila(h, etap, hurt, mats, typ, cfg, dop, self.var_termin.get().strip())
            paczki.append((hurt, mats, zbuduj_wiadomosc(cfg, hurt, temat, tekst, htm, zal, szkic), zal))
        if not paczki:
            messagebox.showinfo("Zamówienia", "Żadna z zaznaczonych hurtowni nie ma materiałów w tym etapie.")
            return
        opis = "\n".join(f"• {p[0]['nazwa']} <{p[0]['email']}> – {len(p[1])} pozycji" for p in paczki)
        if pominiete:
            opis += "\n\nPominięte (brak materiałów z ich asortymentu): " + ", ".join(pominiete)
        rodzaj = "zapytanie ofertowe" if typ != "zamowienie" else "ZAMÓWIENIE"
        if szkic:
            for hurt, mats, msg, zal in paczki:
                eml = os.path.splitext(zal)[0] + ".eml"
                with open(eml, "wb") as f:
                    f.write(bytes(msg))
                try:
                    os.startfile(eml)
                except AttributeError:
                    pass
                self._historia(h, etap, typ, hurt, "szkic", len(mats))
            messagebox.showinfo("Zamówienia", f"Otwarto {len(paczki)} szkic(e) w programie pocztowym:\n\n{opis}\n\n"
                                              "Sprawdź treść i kliknij „Wyślij” w programie pocztowym.")
            return
        if not messagebox.askyesno("Potwierdź wysyłkę", f"Wysłać {rodzaj} (etap {etap['nr']}) do:\n\n{opis}\n\n"
                                                         "Wiadomości zostaną wysłane natychmiast."):
            return
        self.app._start("Wysyłam wiadomości…", self._w_smtp, dict(cfg), paczki, h, etap, typ)

    def _w_smtp(self, cfg, paczki, h, etap, typ):
        try:
            wyslij_smtp(cfg, [p[2] for p in paczki])
        except Exception as e:
            self.app.q.put(("koniec", f"Nie udało się wysłać: {e}"))
            return
        for hurt, mats, _, _ in paczki:
            self.app.q.put(("wywolaj", self._historia, (h, etap, typ, hurt, "SMTP", len(mats))))
        self.app.q.put(("koniec", f"Wysłano {len(paczki)} wiadomości."))

    def _historia(self, h, etap, typ, hurt, sposob, n):
        try:
            hist = json.load(open(self.historia_plik, encoding="utf-8"))
        except Exception:
            hist = []
        hist.insert(0, {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "budowa": h.get("budowa", ""),
                        "etap": etap["nr"], "typ": "zamówienie" if typ == "zamowienie" else "zapytanie ofertowe",
                        "hurt": hurt["nazwa"], "sposob": sposob, "n": n})
        with open(self.historia_plik, "w", encoding="utf-8") as f:
            json.dump(hist[:500], f, ensure_ascii=False, indent=1)
        self.odswiez_hist()

    def odswiez_hist(self):
        self.tree_hist.delete(*self.tree_hist.get_children())
        try:
            hist = json.load(open(self.historia_plik, encoding="utf-8"))
        except Exception:
            hist = []
        for x in hist[:100]:
            self.tree_hist.insert("", "end", values=(x["data"], x["budowa"], x["etap"], x["typ"], x["hurt"],
                                                     x["sposob"], x["n"]))

    def otworz_folder(self):
        if self.plik_json:
            f = os.path.join(os.path.dirname(self.plik_json), "zamowienia")
            os.makedirs(f, exist_ok=True)
            try:
                os.startfile(f)
            except AttributeError:
                pass
