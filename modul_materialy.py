# -*- coding: utf-8 -*-
"""
Moduł zapotrzebowania materiałowego.
Na podstawie kosztorysu ofertowego (xlsx) AI dobiera materiały i normy zużycia dla każdej pozycji
oraz rynkowe ceny hurtowe. Program liczy ilości i zapisuje listę materiałów w Excelu:
  - „Lista materiałów” – zestawienie zbiorcze z zapasem, ilością do zamówienia i wyceną,
  - „Usługi i najem” – rusztowania, wywóz odpadów, sprzęt, podwykonawcy,
  - „Wg pozycji kosztorysu” – zużycie materiałów przy każdej pozycji (do zamawiania etapami).
"""
import datetime as dt
import json
import math
import os
import re
import urllib.error

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modul_oferty import claude_stream, wyciagnij_json, zaokr, zl, MIESIACE


# ============================================================ odczyt kosztorysu

_JM = {"m", "m2", "m3", "m²", "m³", "mb", "szt", "szt.", "kpl", "kpl.", "kg", "t", "l", "r-g", "rg", "m-g", "mg", "godz", "godz.", "ha", "a",
       "km", "cm", "mm", "op", "op.", "kmpl", "kmpl.", "kompl", "kompl.", "ryczałt", "ryczalt", "rycz.", "pkt", "pkt.", "stopa", "odc", "odc.",
       "ark", "para", "zest", "zest.", "tona", "elem", "elem.", "otw", "otw.", "mp", "m.p.", "prób", "prob", "msc", "m-c", "dni", "dzień"}


def _n(x):
    t = str(x if x is not None else "").strip().lower()
    for a, b in zip("ąćęłńóśźż", "acelnoszz"):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)


def _liczba(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    t = str(x or "").replace("\xa0", "").replace(" ", "").replace("zł", "").replace(",", ".")
    try:
        return float(t) if re.fullmatch(r"-?\d+(\.\d+)?", t) else None
    except ValueError:
        return None


def _kolumny_z_naglowka(v):
    """Wiersz nagłówka tabeli kosztorysu → {pole: numer kolumny} albo None. Rozpoznaje różne nazwy kolumn
    (Lp. / L.p. / Nr / Poz.; Opis / Nazwa / Wyszczególnienie; J.m. / Jedn.; Ilość / Obmiar / Przedmiar; Cena)."""
    kol = {}
    for i, x in enumerate(v):
        t = _n(x)
        if not t or len(t) > 60:
            continue
        if t.startswith(("podstawa ilo", "uwagi")):
            continue
        if "lp" not in kol and re.match(r"^(l\.? ?p\.?|nr|nr poz\.?|poz\.?|pozycja|numer|l\.p)$", t):
            kol["lp"] = i
        elif "podstawa" not in kol and t.startswith(("podstawa", "kod", "knr", "nr spec", "numer spec", "symbol", "katalog")):
            kol["podstawa"] = i
        elif "opis" not in kol and t.startswith(("opis", "nazwa", "wyszczegol", "rodzaj rob", "przedmiot", "zakres", "element", "asortyment", "tresc")):
            kol["opis"] = i
        elif "jm" not in kol and (t in ("jm", "j.m", "j.m.", "j. m.", "jedn", "jedn.", "j.") or t.startswith(("j.m", "jedn", "jm ", "j. m"))):
            kol["jm"] = i
        elif "ilosc" not in kol and t.startswith(("ilo", "obmiar", "przedmiar", "krotnosc", "il.")):
            kol["ilosc"] = i
        elif "cena" not in kol and t.startswith("cena"):
            kol["cena"] = i
    return kol if "opis" in kol and ("ilosc" in kol or "jm" in kol or "lp" in kol) else None


def _pozycje_arkusza(ws):
    """Pozycje z jednego arkusza: nagłówek może stać w dowolnym wierszu i zaczynać się w dowolnej kolumnie; numer pozycji może
    być liczbą, tekstem („1.”, „1.2”, „d.1.3”) albo go nie być. Bez nagłówka – kolumny z układu danych (opis, jednostka, ilość)."""
    wiersze = [list(r) for r in ws.iter_rows(values_only=True)]
    tytul, kol, start = "", None, 0
    for nr, v in enumerate(wiersze[:80]):
        if not tytul and v and isinstance(v[0], str) and "postępowani" in v[0].lower():
            tytul = v[0]
        k = _kolumny_z_naglowka(v)
        if k:
            kol, start = k, nr + 1
            break
    if kol is None:  # brak nagłówka: kolumna jednostek = ta, w której najczęściej stoi „m2”, „szt.”…; ilość = liczba obok; opis = najdłuższy tekst
        ile_jm, szer = {}, max((len(v) for v in wiersze), default=0)
        for v in wiersze:
            for i, x in enumerate(v):
                if isinstance(x, str) and _n(x) in _JM:
                    ile_jm[i] = ile_jm.get(i, 0) + 1
        if not ile_jm or max(ile_jm.values()) < 2:
            return tytul, []
        kj = max(ile_jm, key=ile_jm.get)
        dl = {i: sum(len(str(v[i])) for v in wiersze if i < len(v) and isinstance(v[i], str)) for i in range(szer) if i != kj}
        ko = max(dl, key=dl.get)
        ki = next((i for i in (kj + 1, kj - 1, kj + 2) if 0 <= i < szer and i != ko
                   and sum(1 for v in wiersze if i < len(v) and _liczba(v[i]) is not None) >= max(ile_jm.values()) // 2), None)
        kol = {"opis": ko, "jm": kj}
        if ki is not None:
            kol["ilosc"] = ki
    poz, dzial = [], ""
    kom = lambda v, k: (v[kol[k]] if k in kol and kol[k] < len(v) else None)
    for v in wiersze[start:]:
        if not any(x not in (None, "") for x in v):
            continue
        opis = str(kom(v, "opis") or "").strip()
        jm = str(kom(v, "jm") or "").strip()
        ilosc = _liczba(kom(v, "ilosc"))
        lp_s = str(kom(v, "lp") if kom(v, "lp") is not None else "").strip()
        pierwsza = str(v[0] if v and v[0] is not None else "").strip()
        if _n(opis).startswith(("razem", "suma", "ogolem", "wartosc", "podatek", "vat", "netto", "brutto", "slownie")) \
                or _n(lp_s).startswith(("razem", "suma", "ogolem")) or _n(pierwsza).startswith(("razem", "suma", "ogolem")):
            continue
        # wiersz działu: jest nazwa, nie ma jednostki ani ilości (albo nagłówek działu w pierwszej kolumnie: „1. Roboty ziemne”)
        if not jm and ilosc is None:
            if isinstance(v[0], str) and re.match(r"^\d+(\.\d+)*\.?\s+\S", pierwsza):
                dzial = pierwsza
            elif opis and len(opis) < 160 and (not lp_s or not re.fullmatch(r"\d+\.?", lp_s) or "ilosc" in kol):
                dzial = (lp_s + " " if lp_s and lp_s not in opis else "") + opis
            continue
        if not opis or len(opis) < 3:
            continue
        if re.fullmatch(r"[\d\s.,]+", opis):  # wiersz z numerami kolumn (1 2 3 4 …)
            continue
        cena = _liczba(kom(v, "cena"))
        m_lp = re.fullmatch(r"(\d+)(\.0)?\.?", lp_s)
        poz.append({"lp": int(m_lp.group(1)) if m_lp else len(poz) + 1, "dzial": dzial,
                    "podstawa": str(kom(v, "podstawa") or "").strip(), "opis": opis, "jm": jm,
                    "ilosc": ilosc or 0.0, "cena": cena or 0.0})
    if len({p["lp"] for p in poz}) != len(poz):  # numeracja od nowa w każdym dziale albo „1.1, 1.2” – numery kolejne
        for i, p in enumerate(poz, 1):
            p["lp"] = i
    return tytul, poz


def wczytaj_kosztorys(sciezka):
    """Zwraca (tytuł, lista pozycji) z kosztorysu w Excelu – z programu albo własnego (dowolny typowy układ tabeli).
    Przegląda wszystkie arkusze i bierze ten, w którym jest najwięcej pozycji z ilością."""
    import openpyxl
    try:
        wb = openpyxl.load_workbook(sciezka, data_only=True)
    except Exception as e:
        raise ValueError(f"Nie udało się otworzyć kosztorysu ({os.path.basename(str(sciezka))}) – potrzebny plik Excel .xlsx ({str(e)[:80]}).")
    najl = ("", [])
    for ws in wb.worksheets:
        try:
            tytul, poz = _pozycje_arkusza(ws)
        except Exception:
            continue
        if sum(1 for p in poz if p["ilosc"] > 0) > sum(1 for p in najl[1] if p["ilosc"] > 0) or (poz and not najl[1]):
            najl = (tytul or najl[0], poz)
    if not najl[1]:
        raise ValueError("W kosztorysie nie znaleziono pozycji z opisem, jednostką i ilością. Potrzebna jest tabela z kolumnami: "
                         "opis (nazwa) roboty, jednostka miary, ilość – w dowolnym arkuszu pliku .xlsx. "
                         "Jeśli kosztorys jest w PDF albo ma wartości tylko jako formuły bez wyników, zapisz go w Excelu jako .xlsx i wgraj ponownie.")
    return najl


# ============================================================ AI

SYSTEM_MAT = """Jesteś doświadczonym kosztorysantem i zaopatrzeniowcem w polskiej firmie budowlanej \
(termomodernizacje, elewacje, dachy). Na podstawie kosztorysu ofertowego przygotowujesz zapotrzebowanie \
materiałowe z normami zużycia i rynkowymi cenami hurtowymi. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em."""

POLECENIE_MAT = """Poniżej jest kosztorys ofertowy ({n} pozycji). Dla KAŻDEJ pozycji z ilością > 0 określ materiały \
potrzebne do jej wykonania (bez robocizny i sprzętu) wraz z normą zużycia na jednostkę miary pozycji.

ZASADY:
1. Normy zużycia przyjmuj wg nakładów KNR/KNNR dla danej podstawy lub wg kart technicznych producentów \
(np. klej do styropianu ok. 4–5 kg/m2 na mocowanie + 3–4 kg/m2 na warstwę zbrojoną, siatka ok. 1,15 m2/m2, \
tynk cienkowarstwowy 2 mm ok. 3 kg/m2, farba ok. 0,3–0,5 l/m2 na 2 warstwy).
2. Uwzględnij wymagania z opisu pozycji: grubość i lambda izolacji (styropian liczony w m3 = m2 × grubość), \
długość łączników dobrana do grubości, rodzaj blachy (tytan-cynk / stal ocynkowana / PLX), grubości papy itp.
3. Ten sam materiał używany w kilku pozycjach ma JEDNO id. Nazwy techniczne, z przykładową marką \
„lub równoważny”, jednostki handlowe (kg, l, m2, m3, mb, szt., rolka, opak.).
4. Ceny: rynkowe ceny hurtowe netto na {miesiac_rok}, region: {region}, dostawa na budowę. Nie używaj cen z kosztorysu.
5. Zapas: 5% standardowo, 10% dla siatki, papy, folii, membran i blachy (docinki), 0% dla elementów liczonych \
w sztukach (budki, wpusty, nasady).
6. Pozycje, które nie są materiałami do zamówienia w hurtowni (rusztowania – najem, czas pracy rusztowań, \
wywóz i utylizacja odpadów, kontenery, piaskowanie, instalacja odgromowa u podwykonawcy, opłaty za zajęcie pasa \
drogowego), wpisz do "uslugi". Materiały zużywane przy montażu rusztowań i daszków (deski, siatki osłonowe, folie) \
podaj jako materiały tylko wtedy, gdy nie wchodzą w skład najmu.
7. Kategorie grupuj wg rodzaju robót, np.: "Docieplenie ścian (ETICS)", "Tynki i malowanie", "Blacharka", \
"Dach – izolacje i pokrycie", "Konstrukcje drewniane", "Kominy i murowanie", "Rusztowania i zabezpieczenia", \
"Instalacja odgromowa", "Wentylacja", "Pozostałe".
8. Wypisz w "uwagi_ogolne" ryzyka i założenia: materiały, których cena mocno się waha, wymagania konserwatorskie, \
pozycje z niepewną ilością, długie terminy dostaw (np. tytan-cynk 7–10 dni).
{wskazowki}

SCHEMAT:
{{
 "materialy": [{{"id": "M1", "nazwa": "płyty styropianowe EPS 031 gr. 15 cm fasadowe", "jm": "m3",
   "kategoria": "Docieplenie ścian (ETICS)", "cena": 330.00, "zapas": 0.05, "uwagi": ""}}],
 "zuzycie": [{{"poz": 5, "id": "M1", "norma": 0.153}}],
 "uslugi": [{{"nazwa": "Najem rusztowań rurowych do 25 m", "jm": "m2", "ilosc": 1327.1, "pozycje": "11",
   "uwagi": "montaż, demontaż, najem na czas robót"}}],
 "uwagi_ogolne": ["..."]
}}
"norma" to ilość materiału w jego j.m. na 1 j.m. pozycji kosztorysu. Liczby jako liczby (kropka dziesiętna).

KOSZTORYS (lp | dział | podstawa | opis | j.m. | ilość):
{kosztorys}"""


def zbuduj_polecenie_mat(pozycje, wskazowki, region=""):
    dzis = dt.date.today()
    linie = [f"{p['lp']} | {p['dzial']} | {p['podstawa']} | {p['opis']} | {p['jm']} | {p['ilosc']:g}"
             for p in pozycje]
    return POLECENIE_MAT.format(
        n=len(pozycje), miesiac_rok=f"{MIESIACE[dzis.month - 1]} {dzis.year}", region=region or "miejsce budowy (gdy nieznane – średnie ceny krajowe)",
        wskazowki=f"9. Wskazówki użytkownika: {wskazowki}" if wskazowki else "",
        kosztorys="\n".join(linie))


def przelicz_materialy(dane, pozycje):
    poz = {p["lp"]: p for p in pozycje}
    mat = {m["id"]: dict(m, ilosc=0.0, pozycje=[]) for m in dane.get("materialy", [])}
    wiersze = []
    for z in dane.get("zuzycie", []):
        p, m = poz.get(int(z.get("poz", 0) or 0)), mat.get(z.get("id"))
        if not p or not m:
            continue
        norma = float(z.get("norma") or 0)
        il = p["ilosc"] * norma
        if il <= 0:
            continue
        m["ilosc"] += il
        if p["lp"] not in m["pozycje"]:
            m["pozycje"].append(p["lp"])
        wiersze.append({"poz": p, "mat": m, "norma": norma, "ilosc": il})
    lista = [m for m in mat.values() if m["ilosc"] > 0]
    for m in lista:
        m["cena"] = float(m.get("cena") or 0)
        m["zapas"] = float(m.get("zapas") or 0)
        miejsca = 1 if str(m["jm"] or "").strip().lower().replace("³", "3").rstrip(".") in ("m3", "kg", "t", "l") else 0  # „m³” jak „m3”
        m["do_zam"] = math.ceil(round(m["ilosc"] * (1 + m["zapas"]) * 10 ** miejsca, 6)) / 10 ** miejsca
        m["wartosc"] = zaokr(m["do_zam"] * m["cena"])
    kolejnosc = []
    for m in lista:
        if m["kategoria"] not in kolejnosc:
            kolejnosc.append(m["kategoria"])
    lista.sort(key=lambda m: (kolejnosc.index(m["kategoria"]), min(m["pozycje"])))
    return lista, wiersze, zaokr(sum(m["wartosc"] for m in lista))


# ============================================================ Excel

def zapisz_liste(tytul, pozycje, dane, lista, wiersze, sciezka, zrodlo):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    F = lambda **k: Font(name="Arial", size=k.pop("size", 9), **k)
    zolty = PatternFill("solid", fgColor="FFF2CC")
    szary = PatternFill("solid", fgColor="D9E1F2")
    sekcja = PatternFill("solid", fgColor="EDEDED")
    cienka = Side(style="thin", color="999999")
    ramka = Border(left=cienka, right=cienka, top=cienka, bottom=cienka)
    zawin = Alignment(wrap_text=True, vertical="top")
    dzis = dt.date.today()
    mies = f"{MIESIACE[dzis.month - 1]} {dzis.year}"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lista materiałów"
    for k, s in zip("ABCDEFGHIJK", (5, 6, 46, 7, 14, 9, 14, 14, 15, 14, 55)):
        ws.column_dimensions[k].width = s
    krotki = re.sub(r"^Załącznik do oferty w postępowaniu\s*", "", tytul or "").strip()
    krotki = (krotki[:160] + "…") if len(krotki) > 160 else krotki
    ws["A1"] = f"LISTA MATERIAŁÓW – {krotki or os.path.basename(zrodlo)}"
    ws["A1"].font = F(size=12, bold=True)
    ws["A2"] = (f"Źródło: {os.path.basename(zrodlo)} (ilości pozycji) oraz normy zużycia wg KNR / kart technicznych. "
                f"Ceny: rynkowe ceny hurtowe netto – szacunek na {mies} (kolor czerwony), zweryfikuj zapytaniem do "
                f"hurtowni. Kwoty są wpisane wprost (widoczne także w podglądzie na telefonie); zapas i ceny zmienisz w programie.")
    ws["A2"].font = F(italic=True)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:K2")
    ws.row_dimensions[2].height = 30
    nagl = ["Lp.", "ID", "Materiał", "Jm", "Ilość wg kosztorysu", "Zapas [%]", "Ilość do zamówienia",
            "Cena rynkowa netto [zł]", "Wartość netto [zł]", "Pozycje kosztorysu", "Uwagi / wymagania"]
    for i, h in enumerate(nagl, 1):
        c = ws.cell(4, i, h)
        c.font = F(bold=True)
        c.fill = szary
        c.border = ramka
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.freeze_panes = "C5"
    WP = "'Wg pozycji kosztorysu'"
    r, lp, sumy, kat = 5, 1, [], None
    pierwszy = None

    sumy_kat = {}
    for m_ in lista:
        sumy_kat[m_["kategoria"]] = zaokr(sumy_kat.get(m_["kategoria"], 0) + m_["wartosc"])

    def zamknij(r):  # kwoty wpisane wprost – widoczne w każdym podglądzie (telefon, poczta), nie tylko w Excelu
        ws.cell(r, 3, f"Razem – {kat}").font = F(bold=True)
        c = ws.cell(r, 9, sumy_kat.get(kat, 0))
        c.font = F(bold=True)
        c.number_format = "#,##0.00"
        sumy.append(f"I{r}")
        return r + 1

    for m in lista:
        if m["kategoria"] != kat:
            if kat is not None:
                r = zamknij(r)
            kat = m["kategoria"]
            c = ws.cell(r, 1, kat)
            c.font = F(bold=True)
            c.fill = sekcja
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
            r += 1
            pierwszy = r
        wart = [lp, m["id"], m["nazwa"], m["jm"],
                round(m["ilosc"], 3), m["zapas"], m["do_zam"],
                m["cena"], m["wartosc"], ", ".join(str(x) for x in sorted(m["pozycje"])),
                m.get("uwagi", "")]
        for i, v in enumerate(wart, 1):
            c = ws.cell(r, i, v)
            c.font = F(color="FF0000" if i == 8 else "000000")
            c.border = ramka
            c.alignment = zawin
        ws.cell(r, 5).number_format = "#,##0.000"
        ws.cell(r, 6).number_format = "0%"
        ws.cell(r, 7).number_format = "#,##0.0"
        ws.cell(r, 8).number_format = "#,##0.00"
        ws.cell(r, 9).number_format = "#,##0.00"
        ws.cell(r, 6).fill = zolty
        ws.cell(r, 8).fill = zolty
        lp += 1
        r += 1
    if kat is not None:
        r = zamknij(r)
    r += 1
    ws.cell(r, 3, "RAZEM MATERIAŁY (netto, szacunkowo)").font = F(bold=True, size=10)
    c = ws.cell(r, 9, zaokr(sum(m_["wartosc"] for m_ in lista)))
    c.font = F(bold=True, size=10)
    c.number_format = "#,##0.00"
    c.border = ramka
    razem = f"I{r}"
    netto_koszt = zaokr(sum(p["ilosc"] * p["cena"] for p in pozycje))
    if netto_koszt:
        r += 1
        ws.cell(r, 3, f"Udział materiałów w cenie kosztorysu netto ({zl(netto_koszt)})").font = F(italic=True)
        c = ws.cell(r, 9, round(sum(m_["wartosc"] for m_ in lista) / netto_koszt, 4))
        c.number_format = "0.0%"
        c.font = F(italic=True)
    r += 2
    ws.cell(r, 3, "Materiały pomocnicze (ok. 1,5–3%), woda, drobne akcesoria i usługi nie są ujęte w tej liście – "
                  "patrz arkusz „Usługi i najem”.").font = F(italic=True)
    for u in dane.get("uwagi_ogolne", []):
        r += 1
        c = ws.cell(r, 3, "• " + u)
        c.font = F()
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=11)
        ws.row_dimensions[r].height = 26
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "4:4"

    # --- Usługi
    u = wb.create_sheet("Usługi i najem")
    for k, s in zip("ABCDEF", (5, 60, 7, 14, 16, 60)):
        u.column_dimensions[k].width = s
    u["A1"] = "USŁUGI, NAJEM I PODWYKONAWSTWO (poza materiałami)"
    u["A1"].font = F(size=12, bold=True)
    for i, h in enumerate(["Lp.", "Pozycja", "Jm", "Ilość", "Pozycje kosztorysu", "Uwagi"], 1):
        c = u.cell(3, i, h)
        c.font = F(bold=True)
        c.fill = szary
        c.border = ramka
    for n, s in enumerate(dane.get("uslugi", []), 1):
        for i, v in enumerate([n, s.get("nazwa", ""), s.get("jm", ""), s.get("ilosc", ""), s.get("pozycje", ""),
                               s.get("uwagi", "")], 1):
            c = u.cell(3 + n, i, v)
            c.font = F()
            c.border = ramka
            c.alignment = zawin

    # --- Wg pozycji
    w = wb.create_sheet("Wg pozycji kosztorysu")
    for k, s in zip("ABCDEFGHIJK", (6, 26, 50, 11, 6, 6, 40, 6, 12, 12, 12)):
        w.column_dimensions[k].width = s
    w["A1"] = "Zużycie materiałów wg pozycji kosztorysu (ilość = ilość pozycji × norma)"
    w["A1"].font = F(size=12, bold=True)
    nag = ["Poz.", "Dział", "Opis pozycji", "Ilość poz.", "j.m.", "ID", "Materiał", "Jm", "Ilość materiału",
           "Norma na j.m. poz.", "Wartość netto [zł]"]
    for i, h in enumerate(nag, 1):
        c = w.cell(3, i, h)
        c.font = F(bold=True)
        c.fill = szary
        c.border = ramka
        c.alignment = Alignment(wrap_text=True, vertical="center")
    w.freeze_panes = "A4"
    LM = "'Lista materiałów'"
    for n, x in enumerate(sorted(wiersze, key=lambda x: x["poz"]["lp"]), 4):
        p, m = x["poz"], x["mat"]
        vals = [p["lp"], re.sub(r"^[0-9.]+\s*", "", p["dzial"]), p["opis"][:120], p["ilosc"], p["jm"], m["id"],
                m["nazwa"], m["jm"], round(x["ilosc"], 4), x["norma"], zaokr(x["ilosc"] * m["cena"])]
        for i, v in enumerate(vals, 1):
            c = w.cell(n, i, v)
            c.font = F()
            c.border = ramka
        w.cell(n, 9).number_format = "#,##0.000"
        w.cell(n, 10).number_format = "0.0000"
        w.cell(n, 11).number_format = "#,##0.00"
    wb.save(sciezka)


# ============================================================ interfejs

class ZakladkaMaterialy(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.plik_wyniku = None
        g = ttk.Frame(self)
        g.pack(fill="x", padx=10, pady=(12, 4))
        ttk.Label(g, text="Kosztorys ofertowy (xlsx):").pack(side="left")
        self.var_plik = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_plik, width=90).pack(side="left", padx=6, fill="x", expand=True)
        ttk.Button(g, text="Wybierz…", command=self.wybierz).pack(side="left")

        ttk.Label(self, text="Wskazówki dla AI (opcjonalnie, np. „styropian grafitowy 15 cm, λ 0,031; "
                             "blacha tytan-cynk 0,7 mm; rusztowania wynajmujemy z deskami”):").pack(anchor="w", padx=10)
        self.txt_wsk = tk.Text(self, height=3, wrap="word", font=("Segoe UI", 10))
        self.txt_wsk.pack(fill="x", padx=10)

        a = ttk.Frame(self)
        a.pack(fill="x", padx=10, pady=8)
        ttk.Button(a, text="📦 Utwórz zapotrzebowanie materiałowe", style="Akcent.TButton",
                   command=self.generuj).pack(side="left")
        ttk.Button(a, text="📂 Otwórz folder", command=self.otworz).pack(side="left", padx=6)
        ttk.Button(a, text="🗓 Podziel na etapy", command=self.do_harmonogramu).pack(side="left", padx=6)
        ttk.Label(a, text="Ceny materiałów to rynkowe ceny hurtowe (szacunek AI) – zweryfikuj je zapytaniem do hurtowni.",
                  foreground="#777").pack(side="left", padx=10)

        self.txt = tk.Text(self, wrap="word", font=("Segoe UI", 10), state="disabled", background="#fafafa",
                           relief="flat", padx=10, pady=8)
        self.txt.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.txt.tag_configure("h", font=("Segoe UI", 11, "bold"))

    def ustaw_kosztorys(self, sciezka):
        self.var_plik.set(sciezka)

    def wybierz(self):
        s = filedialog.askopenfilename(title="Wybierz kosztorys ofertowy", filetypes=[("Excel", "*.xlsx")])
        if s:
            self.var_plik.set(s)

    def generuj(self):
        cfg = self.app.cfg
        plik = self.var_plik.get().strip()
        if not cfg.get("api_key"):
            messagebox.showwarning("Materiały", "Najpierw wpisz klucz API Claude w Ustawieniach.")
            return
        if not plik or not os.path.isfile(plik):
            messagebox.showinfo("Materiały", "Wskaż plik kosztorysu ofertowego (xlsx).")
            return
        try:
            tytul, pozycje = wczytaj_kosztorys(plik)
        except Exception as e:
            messagebox.showerror("Materiały", f"Nie udało się odczytać kosztorysu:\n{e}")
            return
        wsk = self.txt_wsk.get("1.0", "end").strip()
        self.app._start(f"Przygotowuję zapotrzebowanie dla {len(pozycje)} pozycji…", self._w_generuj,
                        json.loads(json.dumps(cfg)), plik, tytul, pozycje, wsk)

    def _w_generuj(self, cfg, plik, tytul, pozycje, wsk):
        aktywne = [p for p in pozycje if p["ilosc"] > 0]
        content = [{"type": "text", "text": zbuduj_polecenie_mat(aktywne, wsk)}]

        def postep(n):
            self.app.q.put(("status", f"AI dobiera materiały i normy… ({n // 1000} tys. znaków)"))
        try:
            txt, powod = claude_stream(cfg, SYSTEM_MAT, content, postep=postep)
        except urllib.error.HTTPError as e:
            self.app.q.put(("koniec", f"Błąd API {e.code}: {e.read().decode('utf-8', 'ignore')[:400]}"))
            return
        folder = os.path.dirname(plik)
        nazwa = re.sub(r"^Kosztorys_ofertowy_", "", os.path.splitext(os.path.basename(plik))[0])
        with open(os.path.join(folder, f"materialy_odpowiedz_ai_{nazwa}.json.txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        if powod == "max_tokens":
            self.app.log("Uwaga: odpowiedź AI została ucięta – lista materiałów może być niepełna.")
        dane = wyciagnij_json(txt)
        lista, wiersze, razem = przelicz_materialy(dane, aktywne)
        wyj = os.path.join(folder, f"Lista_materialow_{nazwa}.xlsx")
        zapisz_liste(tytul, pozycje, dane, lista, wiersze, wyj, plik)
        self.app.q.put(("wywolaj", self.pokaz, (dane, lista, razem, wyj, pozycje)))
        self.app.q.put(("koniec", f"Lista materiałów gotowa: {len(lista)} pozycji, ok. {zl(razem)} netto."))

    def pokaz(self, dane, lista, razem, wyj, pozycje):
        self.plik_wyniku = wyj
        tab = getattr(self.app, "tab_harmonogram", None)
        if tab is not None:
            tab.ustaw_liste(wyj)
        t = self.txt
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.insert("end", f"Materiały: {len(lista)} pozycji, wartość ok. {zl(razem)} netto (z zapasem)\n", "h")
        netto = sum(p["ilosc"] * p["cena"] for p in pozycje)
        if netto:
            t.insert("end", f"To ok. {razem / netto:.0%} ceny kosztorysu netto ({zl(netto)}).\n")
        t.insert("end", "\nNajwiększe pozycje:\n", "h")
        for m in sorted(lista, key=lambda m: -m["wartosc"])[:8]:
            t.insert("end", f"• {m['nazwa']}: {m['do_zam']:,.1f} {m['jm']} × {m['cena']:.2f} zł = "
                            f"{zl(m['wartosc'])}\n".replace(",", " "))
        if dane.get("uslugi"):
            t.insert("end", f"\nUsługi i najem: {len(dane['uslugi'])} pozycji (osobny arkusz).\n")
        if dane.get("uwagi_ogolne"):
            t.insert("end", "\nUwagi:\n", "h")
            for u in dane["uwagi_ogolne"]:
                t.insert("end", f"• {u}\n")
        t.insert("end", f"\nPlik: {wyj}\n")
        t.configure(state="disabled")
        self.otworz()

    def do_harmonogramu(self):
        tab = getattr(self.app, "tab_harmonogram", None)
        if tab is None:
            return
        if self.plik_wyniku:
            tab.ustaw_liste(self.plik_wyniku)
        self.app.nb.select(tab)

    def otworz(self):
        f = os.path.dirname(self.plik_wyniku or self.var_plik.get() or "")
        if f and os.path.isdir(f):
            try:
                os.startfile(f)
            except AttributeError:
                pass
