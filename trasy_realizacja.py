# -*- coding: utf-8 -*-
"""
Realizacja umów – trasy: dane i lista realizacji, umowa, pliki, harmonogram rzeczowo-finansowy, dziennik, faktury, podwykonawcy, rozliczenie materiałów, pogoda i wnioski o przedłużenie, dostawy, wnioski wykonawcy o zmianę umowy.
Blueprint „realizacja” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("realizacja", __name__)


def realizacja_dane(pid):
    """Dane realizacji – brakujące pola (plik niepełny, np. ze starszej wersji) uzupełniane domyślnymi, żeby widok się nie wywracał."""
    r = S.czytaj(os.path.join(S.pdir(pid), "realizacja.json"), None)
    if not isinstance(r, dict):
        r = {}
    for k, v in S.REALIZACJA_DOMYSLNE.items():
        if r.get(k) is None and v is not None or k not in r:
            r[k] = list(v) if isinstance(v, list) else v
    try:  # stawka zapisana jako „23” (wcześniejsza wersja przejścia do realizacji u zamawiającego) → 0,23
        if r.get("vat") not in (None, "") and float(r["vat"]) > 1:
            r["vat"] = float(r["vat"]) / 100
    except (TypeError, ValueError):
        pass
    return r


# ---------- rola bez dostępu do Finansów (np. „Kierownik budowy – bez finansów”): kwoty umowy, faktury, koszty, stawki – poza odpowiedzią serwera
POLA_FIN_PODSUM = ("wartosc_umowy_netto", "odebrano_netto", "zafakturowano_netto", "zafakturowano_brutto", "zaplacono_brutto", "naleznosci_brutto",
                   "przeterminowane_brutto", "koszty_netto", "koszty_niezaplacone", "robocizna", "koszty_razem", "wynik_biezacy", "wynik_prognoza",
                   "prognoza_koszt_calkowity", "prognoza_postep_proc", "prognoza_metoda")


def _pw_bez_finansow(x):
    """Podwykonawca bez wartości umowy, faktur i zapłat (zostają: nazwa, zakres, status zgłoszenia, terminy, pliki)."""
    return {**{k: v for k, v in x.items() if k not in ("wartosc_netto", "platnosci", "sumy", "uwagi")},
            "wartosc_netto": None, "platnosci": [], "sumy": {"wartosc_brutto": None, "zafakturowano": None, "zaplacono": None, "do_zaplaty": None, "zalegle": 0},
            "uwagi": [u for u in (x.get("uwagi") or []) if isinstance(x.get("uwagi"), list) and "art. 464" in u], "bez_finansow": True}


def bez_finansow_realizacji(wyn):
    """Dane realizacji dla roli bez modułu Finanse – usuwa kwoty, zostawia to, czego potrzeba na budowie (terminy, harmonogram %, dziennik, usterki)."""
    r = dict(wyn.get("realizacja") or {})
    r.update(wartosc_netto=None, wartosc_szacunkowa=None, faktury=[], koszty=[], transze=[], wydatki=[])
    if r.get("hrf"):
        h = r["hrf"]
        r["hrf"] = {**h, "dzialy": [dict(d, wartosc=None) for d in h.get("dzialy") or []], "etapy": [dict(e, wartosc=None) for e in h.get("etapy") or []]}
    if isinstance(r.get("podwykonawcy"), list):
        r["podwykonawcy"] = [_pw_bez_finansow(x) for x in r["podwykonawcy"] if isinstance(x, dict)]
    s_ = dict(wyn.get("podsumowanie") or {})
    s_.update({k: None for k in POLA_FIN_PODSUM}, koszty_kategorie={})
    o = wyn.get("oferta")
    return {**wyn, "realizacja": r, "podsumowanie": s_, "oferta": {"obiekt": o.get("obiekt")} if isinstance(o, dict) else None,
            "robocizna": [{k: v for k, v in w.items() if k not in ("stawka", "kwota")} for w in wyn.get("robocizna") or []],
            "dzialy": [dict(d, wartosc=None) for d in wyn.get("dzialy") or []], "bez_finansow": True}


def dostawy_dane(pid):
    return S.czytaj(os.path.join(S.pdir(pid), "realizacja_dostawy.json"), None)


def _dostawy_start(pid, m=None):
    """Dane realizacji umowy dostawy/usługi: zapisane albo – przy pierwszym otwarciu – startowe z oferty (bez zapisu pliku przy odczycie, H1-05)."""
    R = dostawy_dane(pid)
    if R is None:
        m = m or S.meta(pid)
        R = S.DS.nowa_umowa(m.get("rodzaj_zamowienia") or "dostawy", m.get("oferta"), m.get("formularz_cenowy"), m.get("analiza_dostawcy"), m.get("przetarg"))
    return R


LISTY_DOSTAW = {"pozycje": "lp", "zamowienia": "id", "okresy": "id", "faktury": "id", "reklamacje": "id"}


def _scal_liste(stare, nowe, klucz, usun):
    """Zapis częściowy po identyfikatorze (H1-05): element z istniejącym id – aktualizacja podanych pól, bez id – nowy element,
    elementy, których nie przysłano – bez zmian (nie giną), usunięcie – tylko wprost („usun”: [id])."""
    wyn = [dict(x) for x in stare if isinstance(x, dict) and str(x.get(klucz)) not in usun]
    po_id = {str(x.get(klucz)): x for x in wyn if x.get(klucz) not in (None, "")}
    for x in nowe:
        if not isinstance(x, dict):
            continue
        k = x.get(klucz)
        if k not in (None, "") and str(k) in usun:
            continue
        if k not in (None, "") and str(k) in po_id:
            po_id[str(k)].update(x)
        else:
            x = dict(x)
            if klucz == "id":
                x["id"] = uuid.uuid4().hex[:8] if k in (None, "") or str(k) in po_id else str(k)
            elif k in (None, ""):
                x[klucz] = max([int(y.get(klucz) or 0) for y in wyn if str(y.get(klucz) or "").isdigit()] + [0]) + 1
            wyn.append(x)
            po_id[str(x.get(klucz))] = x
    return wyn


@bp.get("/api/dostawy/realizacja")
@S.wymaga_logowania
def dostawy_lista():
    wyn, login, rola = [], session.get("login"), S.rola_sesji()
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if m and m.get("status_projektu") in ("realizacja", "zakonczony") and m.get("strona") == "dostawca" and S.ma_dostep(m, login, rola, lista=True) \
                and not m.get("archiwum"):
            R = dostawy_dane(pid) or {}
            S_lok = S.DS.podsumowanie(R) if R else {}
            wyn.append({"id": pid, "nazwa": m.get("nazwa"), "status": m.get("status_projektu"), "rodzaj": m.get("rodzaj_zamowienia"),
                        "wartosc": S_lok.get("wartosc_netto"), "proc": S_lok.get("proc_realizacji"), "przeterminowane": S_lok.get("przeterminowane_brutto"),
                        "wlasciciel": m.get("wlasciciel") or S.login_admina()})
    return jsonify(sorted(wyn, key=lambda x: (x["status"] != "realizacja", x["nazwa"] or "")))


@bp.get("/api/projekty/<pid>/dostawy")
@S.wymaga_logowania
def dostawy_pobierz(pid):
    m = S.meta(pid)
    R = _dostawy_start(pid, m)  # odczyt nie zapisuje pliku (H1-05)
    kat = os.path.join(S.pdir(pid), "realizacja", "dostawy")
    pl = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
    return jsonify({"projekt": {"id": pid, "nazwa": m.get("nazwa"), "status": m.get("status_projektu"), "rodzaj": m.get("rodzaj_zamowienia")},
                    "R": R, "S": S.DS.podsumowanie(R), "pliki": pl, "statusy_zam": S.DS.STATUSY_ZAM, "statusy_okr": S.DS.STATUSY_OKR})


@bp.post("/api/projekty/<pid>/dostawy")
@S.wymaga_logowania
def dostawy_zapisz(pid):
    """Zapis części danych realizacji (umowa, pozycje, zamówienia, okresy, faktury, reklamacje). Terminy płatności faktur liczone z umowy."""
    j = request.json or {}
    usun = j.get("usun") if isinstance(j.get("usun"), dict) else {}
    with S.BLOKADA:
        R = _dostawy_start(pid)
        for k in ("umowa", "pozycje", "zamowienia", "okresy", "faktury", "reklamacje"):
            if isinstance(j.get(k), dict) and k == "umowa":
                R[k] = {**(R.get(k) or {}), **j[k]}  # pola umowy – tylko przysłane (H1-05)
            elif k != "umowa" and (isinstance(j.get(k), list) or isinstance(usun.get(k), list)):
                # pozycje, zamówienia, okresy, faktury, reklamacje – zapis częściowy po id; usuwanie tylko wprost (H1-05)
                R[k] = _scal_liste(R.get(k) or [], j.get(k) if isinstance(j.get(k), list) else [], LISTY_DOSTAW[k],
                                   {str(x) for x in (usun.get(k) or []) if isinstance(x, (str, int))})
        u = R.get("umowa") or {}
        for z in R.get("zamowienia") or []:
            z.setdefault("id", uuid.uuid4().hex[:8])
            z["wartosc"] = S.DS.wartosc_zamowienia(R, z)
        vat = S.DS._f(u.get("vat")) if u.get("vat") not in (None, "") else 0.23
        for f in R.get("faktury") or []:
            f.setdefault("id", uuid.uuid4().hex[:8])
            if S.DS._f(f.get("netto")) and not S.DS._f(f.get("brutto")):
                f["brutto"] = round(S.DS._f(f["netto"]) * (1 + vat), 2)
            if f.get("data") and not f.get("termin"):
                d0 = S.DS._d(f["data"])
                if d0:
                    f["termin"] = (d0 + dt.timedelta(days=int(S.DS._f(u.get("termin_platnosci")) or 30))).isoformat()
        for r_ in R.get("reklamacje") or []:
            r_.setdefault("id", uuid.uuid4().hex[:8])
        if j.get("przelicz_okresy") and R.get("rodzaj") == "uslugi":
            R["okresy"] = S.DS.okresy_uslug(R)
        S.pisz(os.path.join(S.pdir(pid), "realizacja_dostawy.json"), R)
    return jsonify({"R": R, "S": S.DS.podsumowanie(R)})


@bp.post("/api/projekty/<pid>/dostawy/dokument")
@S.wymaga_logowania
def dostawy_dokument(pid):
    j = request.json or {}
    m = S.meta(pid)
    R = dostawy_dane(pid) or {}
    kat = os.path.join(S.pdir(pid), "realizacja", "dostawy")
    os.makedirs(kat, exist_ok=True)
    przedm = (m.get("przetarg") or {}).get("przedmiot") or m.get("nazwa", "")
    rodz = j.get("rodzaj")
    if rodz == "protokol":
        el = next((z for z in R.get("zamowienia") or [] if z.get("id") == j.get("id")), None)
        typ = "zamowienie"
        if not el:
            el, typ = next((o for o in R.get("okresy") or [] if o.get("id") == j.get("id")), None), "okres"
        if not el:
            return jsonify({"blad": "Nie znaleziono dostawy ani okresu."}), 404
        nazwa = f"Protokol_odbioru_{S.DOT.bezpieczna(str(el.get('nr') or el.get('okres') or el['id']))[:30]}.docx"
        S.DS.protokol_docx(os.path.join(kat, nazwa), R, S._wykonawca_dane(), przedm, el, typ)
    elif rodz == "wezwanie":
        f = next((x for x in R.get("faktury") or [] if x.get("id") == j.get("id")), None)
        if not f:
            return jsonify({"blad": "Nie znaleziono faktury."}), 404
        nazwa = f"Wezwanie_do_zaplaty_{S.DOT.bezpieczna(str(f.get('nr') or f['id']))[:30]}.docx"
        S.DS.wezwanie_docx(os.path.join(kat, nazwa), R, S._wykonawca_dane(), przedm, f)
    elif rodz == "rozliczenie":
        nazwa = f"Rozliczenie_umowy_{dt.date.today():%Y-%m-%d}.xlsx"
        S.DS.rozliczenie_xlsx(os.path.join(kat, nazwa), R, przedm)
    else:
        return jsonify({"blad": "Nieznany dokument."}), 400
    sc = f"realizacja/dostawy/{nazwa}"
    return jsonify({"plik": sc, "url": f"/pobierz/{pid}/{S.urllib.parse.quote(sc)}"})


@bp.post("/api/projekty/<pid>/dostawy/plik")
@S.wymaga_logowania
def dostawy_plik(pid):
    kat = os.path.join(S.pdir(pid), "realizacja", "dostawy")
    os.makedirs(kat, exist_ok=True)
    if request.form.get("usun"):
        p = os.path.join(kat, os.path.basename(request.form["usun"]))
        if os.path.isfile(p):
            os.remove(p)
        return jsonify({"ok": True})
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(kat, S.secure_filename_pl(f.filename)))
    return jsonify({"ok": True})


@bp.get("/api/realizacja")
@S.wymaga_logowania
def realizacja_lista():
    wyn, login, rola = [], session.get("login"), S.rola_sesji()
    strona = request.args.get("strona", "wykonawca") if S.EDYCJA == "pelna" else "zamawiajacy"
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if m and m.get("status_projektu") in ("realizacja", "zakonczony") and S.ma_dostep(m, login, rola, lista=True) \
                and (m.get("strona") or "wykonawca") == strona and not m.get("archiwum") and S.projekt_w_edycji(m) \
                and (strona != "zamawiajacy" or S.zgodny_modul(m, request.args.get("modul"))):
            try:
                s_ = S.podsumowanie_realizacji(pid)
            except Exception:
                s_ = {}
            wyn.append({"id": pid, "nazwa": m.get("nazwa"), "status": m.get("status_projektu"), "typ": m.get("typ") or "przetarg",
                        "wlasciciel": m.get("wlasciciel") or S.login_admina(),
                        **({"wartosc": s_.get("wartosc_umowy_netto"), "naleznosci": s_.get("naleznosci_brutto"),
                            "przeterminowane": s_.get("przeterminowane_brutto")} if S.moze("finanse") else {"wartosc": None, "naleznosci": None, "przeterminowane": None})})
    return jsonify(sorted(wyn, key=lambda x: (x["status"] != "realizacja", x["nazwa"] or "")))


@bp.get("/api/projekty/<pid>/realizacja")
@S.wymaga_logowania
def realizacja(pid):
    m = S.meta(pid)
    r = realizacja_dane(pid)
    if r.get("hrf"):
        r["hrf"] = S.przelicz_hrf(r["hrf"])
    wyn = _realizacja_wynik(pid, m, r)
    return jsonify(S.ukryj_innych(wyn if S.moze("finanse") else bez_finansow_realizacji(wyn)))


def _realizacja_wynik(pid, m, r):
    return ({"projekt": {k: m.get(k) for k in ("id", "nazwa", "status_projektu", "typ", "rodzaj_zamowienia")} | {"strona": m.get("strona") or "wykonawca"},
                    "notatki": [x for x in m.get("notatki", []) if not x.get("archiwum")],
                    "przetarg": (lambda d: {"przedmiot": d["nazwa"], "link": d["link"], "numer": d["numer"], "zamawiajacy": d["zamawiajacy"]})(S.dane_przetargu(m, pid)) if m.get("przetarg") else None,
                    "oferta": m.get("oferta"), "realizacja": S.bez_archiwum(S.dane_domu(r) if m.get("strona") == "inwestor" else r),
                    "podsumowanie": S.podsumowanie_realizacji(pid),
                    "pliki": S.pliki_budowy(pid), "robocizna": S.robocizna_projektu(pid, m.get("nazwa")),
                    "dzialy": S.dzialy_kosztorysu(pid), "firma": S.cfg().get("firma_nazwa", "")})


@bp.post("/api/projekty/<pid>/realizacja/umowa")
@S.wymaga_logowania
def realizacja_umowa(pid):
    r = realizacja_dane(pid)
    j = dict(request.json or {})
    if not S.moze("finanse", 2):  # kierownik budowy zapisuje nr, daty, kierownika, inspektora i adres – kwot umowy nie widzi i nie zmienia
        j.pop("wartosc_netto", None)
        j.pop("vat", None)
    try:
        r["wartosc_netto"] = S.MO.zaokr(float(str(j.get("wartosc_netto", r["wartosc_netto"]) or 0).replace(" ", "").replace("\u00a0", "").replace(",", ".")))
        v_ = str(j.get("vat", r.get("vat")) or "").replace(",", ".").replace("%", "").strip()
        r["vat"] = (float(v_) / (100 if float(v_) > 1 else 1)) if v_ else ""
    except ValueError:
        return jsonify({"blad": "Błędna wartość umowy lub VAT."}), 400
    for k in ("data_umowy", "termin_zakonczenia"):
        if j.get(k):
            try:
                dt.date.fromisoformat(str(j[k]))
            except ValueError:
                return jsonify({"blad": "Nieprawidłowa data umowy lub termin zakończenia."}), 400
    if j.get("data_umowy") and j.get("termin_zakonczenia") and str(j["termin_zakonczenia"]) < str(j["data_umowy"]):
        return jsonify({"blad": "Termin zakończenia nie może być wcześniejszy niż data umowy."}), 400
    if "adres" in j and str(j["adres"])[:200] != (r.get("adres") or ""):
        r.pop("wsp", None)  # inny adres budowy – pogoda do dziennika liczona dla nowej lokalizacji
    for k in ("umowa_nr", "data_umowy", "termin_zakonczenia", "kierownik", "inspektor", "adres",
              "wykonawca_nazwa", "wykonawca_adres", "wykonawca_nip"):
        if k in j:
            r[k] = str(j[k])[:200]
    hrf_ = r.get("hrf")
    if S.meta(pid).get("strona") == "zamawiajacy" and hrf_ and r["wartosc_netto"] and not any(e.get("status") == "odebrany" for e in hrf_["etapy"]):
        suma0 = sum(x["wartosc"] for x in hrf_["dzialy"]) or 0  # zmiana ceny umowy – harmonogram (bez odbiorów) przeliczony na nową wartość
        if suma0 and abs(suma0 - r["wartosc_netto"]) > 0.01:
            hrf_["dzialy"] = [dict(x, wartosc=S.MO.zaokr(x["wartosc"] * r["wartosc_netto"] / suma0)) for x in hrf_["dzialy"]]
            r["hrf"] = S.przelicz_hrf(hrf_)
    S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/realizacja/pliki")
@S.wymaga_logowania
def realizacja_pliki(pid):
    d = os.path.join(S.pdir(pid), "realizacja", "dokumenty")
    os.makedirs(d, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(d, S.secure_filename_pl(f.filename)))
    return jsonify(S.pliki_budowy(pid))


@bp.post("/api/projekty/<pid>/realizacja/pliki/usun")
@S.wymaga_logowania
def realizacja_pliki_usun(pid):
    d = os.path.realpath(os.path.join(S.pdir(pid), "realizacja"))
    p = os.path.realpath(os.path.join(S.pdir(pid), request.json.get("sciezka", "")))
    if p.startswith(d + os.sep) and os.path.isfile(p):
        S.archiwizuj_plik(pid, p)
    return jsonify(S.pliki_budowy(pid))


def _wniosek(m, wid):
    return next((w for w in m.get("wnioski", []) if w["id"] == wid), None)


@bp.get("/api/projekty/<pid>/rozbieznosci")
@S.wymaga_logowania
def rozbieznosci_lista(pid):
    return jsonify(S.rozbieznosci_projektu(pid))


@bp.post("/api/projekty/<pid>/rozbieznosci")
@S.wymaga_logowania
def rozbieznosci_ustaw(pid):
    """Decyzja wykonawcy o pozycji spoza przedmiaru: w cenie, pytanie do zamawiającego, na etap umowy albo nie dotyczy."""
    j = request.json or {}
    wyn, kod = S.ustaw_rozbieznosc(pid, str(j.get("id") or ""), j.get("decyzja"), bool(j.get("potwierdzam")), j.get("odpowiedz"),
                                   str(session.get("login") or ""))
    return jsonify(wyn), kod


@bp.post("/api/projekty/<pid>/warianty")
@S.wymaga_logowania
def warianty_ustaw(pid):
    """Który wariant jest w cenie, gdy dokumenty podają różne rozwiązania dla tej samej pozycji przedmiaru."""
    j = request.json or {}
    wyn, kod = S.ustaw_wariant(pid, str(j.get("id") or ""), j.get("wybrany"), j.get("pytanie"), str(session.get("login") or ""))
    return jsonify(wyn), kod


@bp.post("/api/projekty/<pid>/wnioski")
@S.wymaga_logowania
def wniosek_nowy(pid):
    rodzaj = (request.json or {}).get("rodzaj")
    if rodzaj not in S.WN.RODZAJE:
        return jsonify({"blad": "Nieznany rodzaj wniosku."}), 400
    m = S.meta(pid)
    if not S.dane_umowy_projektu(pid, m)["data"]:
        return jsonify({"blad": "Wniosek o zmianę umowy można utworzyć po podpisaniu umowy – wpisz datę umowy w danych umowy. Rozbieżności "
                                "wykryte przed złożeniem oferty zgłoś jako pytania do zamawiającego albo ujmij w cenie (krok Kosztorys i oferta)."}), 400
    lst = m.setdefault("wnioski", [])
    oferta = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), {}) or {}
    # roboty zostawione przy ofercie na etap umowy – jedyne rozbieżności z etapu oferty, które wolno wycenić we wniosku
    kand = [{"opis": str(p.get("opis", ""))[:400], "jm": str(p.get("jm", ""))[:20], "ilosc": float(p.get("ilosc") or 0), "z_oferty": True}
            for p in S.ROZB.kandydaci(oferta)] if rodzaj != "przeszkody" else []
    w = {"id": uuid.uuid4().hex[:8], "nr": f"W/{len(lst) + 1}/{dt.date.today().year}", "rodzaj": rodzaj, "rodzaj_nazwa": S.WN.RODZAJE[rodzaj],
         "data": dt.date.today().isoformat(), "status": "roboczy", "prace": kand, "dni": 0, "kwota_netto": 0, "uzasadnienie": "",
         "bledy": [b["id"] for b in S.bledy_dokumentacji(pid, m)] if rodzaj == "roznice_dokumentacji" else []}
    S.odswiez_wniosek(pid, m, w)
    lst.append(w)
    S.zapisz_meta(pid, m)
    return jsonify(w)


@bp.post("/api/projekty/<pid>/wnioski/<wid>")
@S.wymaga_logowania
def wniosek_zapisz(pid, wid):
    j = request.json or {}
    m = S.meta(pid)
    w = _wniosek(m, wid)
    if not w:
        return jsonify({"blad": "Nie ma takiego wniosku."}), 404
    if j.get("usun"):
        if w["status"] == "zaakceptowany":
            return jsonify({"blad": "Zaakceptowanego wniosku nie można usunąć (jest aneks)."}), 400
        m["wnioski"] = [x for x in m["wnioski"] if x["id"] != wid]
        S.zapisz_meta(pid, m)
        return jsonify({"ok": True})
    for k in ("uzasadnienie", "przyczyna", "organ", "od", "do", "dokumenty", "miejsce"):
        if k in j:
            w[k] = str(j[k] or "")[:4000]
    if "prace" in j:
        prace = []
        for p in j["prace"] or []:
            if str(p.get("opis", "")).strip():
                try:
                    il = float(str(p.get("ilosc") or 0).replace(",", "."))
                except ValueError:
                    il = 0
                x = {"opis": str(p["opis"])[:400], "jm": str(p.get("jm", ""))[:20], "ilosc": il}
                zn = str(p.get("znacznik") or "").strip()  # czwarte pole wiersza: „zamienna” albo „mimo to: powód”
                if zn.lower().startswith("zamien"):
                    x["zamienna"] = True
                elif zn.lower().startswith("mimo"):
                    x["mimo_to"] = True
                    x["mimo_to_powod"] = zn.split(":", 1)[1].strip()[:300] if ":" in zn else ""
                prace.append(x)
        w["prace"] = prace[:300]
    if "bledy" in j:
        w["bledy"] = [str(x) for x in j["bledy"]][:200]
    try:
        if "dni" in j:
            w["dni"] = max(0, int(j["dni"] or 0))
        if "kwota_netto" in j:
            w["kwota_netto"] = S.MO.zaokr(float(str(j["kwota_netto"] or 0).replace(" ", "").replace(",", ".")))
    except ValueError:
        return jsonify({"blad": "Liczba dni i kwota muszą być liczbami."}), 400
    S.odswiez_wniosek(pid, m, w)
    S.zapisz_meta(pid, m)
    return jsonify(w)


@bp.post("/api/projekty/<pid>/wnioski/<wid>/propozycja")
@S.wymaga_logowania
def wniosek_propozycja(pid, wid):
    return jsonify(S.uruchom("oferta", "Propozycja wniosku (AI)", S.praca_propozycja_wniosku, pid, wid))


@bp.post("/api/projekty/<pid>/wnioski/<wid>/kosztorys")
@S.wymaga_logowania
def wniosek_kosztorys(pid, wid):
    return jsonify(S.uruchom("oferta", "Kosztorys do wniosku", S.praca_kosztorys_wniosku, pid, wid))


@bp.get("/api/projekty/<pid>/wnioski/<wid>/kosztorys-dane")
@S.wymaga_logowania
def wniosek_kosztorys_dane(pid, wid):
    d = S.czytaj(os.path.join(S.pdir(pid), "wnioski", f"kosztorys_{wid}.json"), None)
    if not d:
        return jsonify({"brak": True})
    return jsonify({k: d.get(k) for k in ("dzialy", "netto", "vat", "vat_kwota", "brutto", "vat_nieustalony", "dni_realizacji")})


@bp.post("/api/projekty/<pid>/wnioski/<wid>/kosztorys-dane")
@S.wymaga_logowania
def wniosek_kosztorys_edycja(pid, wid):
    """Zmiany w kosztorysie z okienka programu (ilości, ceny, pozycje) – przeliczenie, nowy plik Excel i kwota wniosku."""
    j = request.json or {}
    dzialy = []
    for dz in j.get("dzialy") if isinstance(j.get("dzialy"), list) else []:
        poz = []
        for p in (dz.get("pozycje") if isinstance(dz, dict) and isinstance(dz.get("pozycje"), list) else []):
            if not isinstance(p, dict) or not str(p.get("opis", "")).strip():
                continue
            try:
                poz.append({"podstawa": str(p.get("podstawa", ""))[:60], "opis": str(p["opis"])[:500], "jm": str(p.get("jm", ""))[:20],
                            "ilosc": float(str(p.get("ilosc") or 0).replace(",", ".")), "cena": float(str(p.get("cena") or 0).replace(",", ".").replace(" ", "")),
                            "zrodlo": str(p.get("zrodlo", ""))[:60], "uwagi": str(p.get("uwagi", ""))[:300]})
            except ValueError:
                return jsonify({"blad": f"Nieprawidłowa ilość lub cena w pozycji: {p.get('opis', '')[:40]}"}), 400
        if poz:
            dzialy.append({"nazwa": str(dz.get("nazwa") or "Roboty")[:120], "pozycje": poz})
    if not dzialy:
        return jsonify({"blad": "Kosztorys nie ma pozycji."}), 400
    wyn = S.zapisz_kosztorys_wniosku(pid, wid, {"dzialy": dzialy})
    return jsonify(wyn)


@bp.post("/api/projekty/<pid>/wnioski/<wid>/kosztorys-wlasny")
@S.wymaga_logowania
def wniosek_kosztorys_wlasny(pid, wid):
    f = request.files.get("plik")
    if not f or not f.filename.lower().endswith((".xlsx", ".xlsm")):
        return jsonify({"blad": "Wybierz kosztorys w Excelu (.xlsx)."}), 400
    kat = os.path.join(S.pdir(pid), "wnioski")
    os.makedirs(kat, exist_ok=True)
    p = os.path.join(kat, "wgrany_" + S.secure_filename_pl(f.filename))
    f.save(p)
    try:
        _, poz = S.MM.wczytaj_kosztorys(p)
    except Exception:
        poz = []
    if not poz:
        return jsonify({"blad": "Nie rozpoznano pozycji (potrzebny nagłówek: Lp., opis, j.m., ilość, cena)."}), 400
    dane = {"dzialy": [{"nazwa": "1. Roboty wg kosztorysu wykonawcy", "pozycje": [[p_.get("podstawa", ""), p_["opis"], p_["jm"], p_["ilosc"], p_.get("cena") or 0, 1,
                                                                                    "kosztorys wykonawcy", ""] for p_ in poz]}]}
    return jsonify(S.zapisz_kosztorys_wniosku(pid, wid, dane))


@bp.post("/api/projekty/<pid>/wnioski/<wid>/dokument")
@S.wymaga_logowania
def wniosek_dokument(pid, wid):
    """Wniosek do zamawiającego (Word) – z wykazem prac, błędów dokumentacji, kwotą i nowym terminem."""
    m = S.meta(pid)
    w = _wniosek(m, wid)
    if not w:
        return jsonify({"blad": "Nie ma takiego wniosku."}), 404
    if not w.get("dni") and not w.get("kwota_netto"):
        return jsonify({"blad": "Podaj liczbę dni przedłużenia i/lub kwotę (kosztorys)."}), 400
    S.odswiez_wniosek(pid, m, w)
    if any("[UZUPEŁNIJ]" in x for x in w.get("ostrzezenia") or []):
        return jsonify({"blad": "Kosztorys wniosku ma pozycje z polem [UZUPEŁNIJ] – uzupełnij je przed wygenerowaniem wniosku."}), 400
    um = S.dane_umowy_projektu(pid, m)
    if um["termin"] and w.get("dni"):
        try:
            w["nowy_termin"] = (dt.date.fromisoformat(um["termin"]) + dt.timedelta(days=int(w["dni"]))).isoformat()
        except ValueError:
            pass
    c = S.cfg()
    bl = [b for b in S.bledy_dokumentacji(pid, m) if b["id"] in set(w.get("bledy") or [])] if w["rodzaj"] == "roznice_dokumentacji" else None
    kat = os.path.join(S.pdir(pid), "wnioski")
    os.makedirs(kat, exist_ok=True)
    nazwa = f"Wniosek_{w['nr'].replace('/', '-')}_{w['rodzaj']}.docx"
    S.WN.wniosek_docx(os.path.join(kat, nazwa), {**w, "prace": S.ROZB.do_kosztorysu(w.get("prace")), "vat": um["vat"] if um["vat"] is not None else w.get("vat")},
                    {"nazwa": c.get("firma_nazwa", ""), "adres": c.get("firma_adres", ""), "nip": c.get("firma_nip", "")},
                    S.dane_zamawiajacego_budowy(pid, m), um, m.get("nazwa", ""), w.get("miejsce") or "", bl)
    w["wniosek_plik"] = f"wnioski/{nazwa}"
    S.zapisz_meta(pid, m)
    return jsonify({"url": f"/pobierz/{pid}/wnioski/{S.urllib.parse.quote(nazwa)}", "nowy_termin": w.get("nowy_termin")})


@bp.post("/api/projekty/<pid>/wnioski/<wid>/status")
@S.wymaga_logowania
def wniosek_status(pid, wid):
    """Złożony / odrzucony / zaakceptowany. Akceptacja: termin i wynagrodzenie w realizacji, nowy etap w harmonogramie,
    kosztorys po zmianie umowy i aneks do umowy z kosztorysem jako załącznikiem."""
    j = request.json or {}
    st = j.get("status")
    if st not in ("złożony", "odrzucony", "zaakceptowany", "roboczy"):
        return jsonify({"blad": "Nieznany status."}), 400
    m = S.meta(pid)
    w = _wniosek(m, wid)
    if not w:
        return jsonify({"blad": "Nie ma takiego wniosku."}), 404
    if w["status"] == "zaakceptowany":
        return jsonify({"blad": "Wniosek jest już zaakceptowany – aneks został przygotowany."}), 400
    w["status"] = st
    if st != "zaakceptowany":
        if st == "złożony":
            w["data_zlozenia"] = dt.date.today().isoformat()
        S.zapisz_meta(pid, m)
        return jsonify(w)
    try:
        dni = max(0, int(j.get("dni", w.get("dni")) or 0))
        kw = S.MO.zaokr(float(str(j.get("kwota_netto", w.get("kwota_netto")) or 0).replace(" ", "").replace(",", ".")))
    except ValueError:
        return jsonify({"blad": "Podaj zaakceptowaną liczbę dni i kwotę."}), 400
    um = S.dane_umowy_projektu(pid, m)
    aneksy = [x for x in m.get("wnioski", []) if x.get("aneks_nr")]
    nr_aneksu = str(j.get("nr_aneksu") or len(aneksy) + 1)
    vat = um["vat"] if um["vat"] is not None else (w.get("vat") or S.MO.VAT_PODSTAWOWY)
    stary_termin, nowy_termin = um["termin"], um["termin"]
    if um["termin"] and dni:
        nowy_termin = (dt.date.fromisoformat(um["termin"]) + dt.timedelta(days=dni)).isoformat()
    stara, nowa = um["wartosc"], S.MO.zaokr(um["wartosc"] + kw)
    with S.BLOKADA:
        r = realizacja_dane(pid)
        if nowy_termin:
            r.setdefault("termin_pierwotny", r.get("termin_zakonczenia") or "")  # do ogłoszenia o wykonaniu umowy (czy w pierwotnym terminie)
            r["termin_zakonczenia"] = nowy_termin
        if kw:
            r.setdefault("wartosc_pierwotna_netto", r.get("wartosc_netto") or 0)
            r["wartosc_netto"] = nowa
        hrf = r.get("hrf")
        if hrf and kw:  # nowy dział i etap harmonogramu z pracami z aneksu
            hrf["dzialy"].append({"nazwa": f"Aneks nr {nr_aneksu} – {w['rodzaj_nazwa'].lower()}", "wartosc": kw})
            for e in hrf["etapy"]:
                e["udzialy"] = list(e.get("udzialy") or []) + [0]
            ost = max((e.get("do") or "") for e in hrf["etapy"]) if hrf["etapy"] else dt.date.today().isoformat()
            hrf["etapy"].append({"nr": len(hrf["etapy"]) + 1, "nazwa": f"Aneks nr {nr_aneksu}: {w['rodzaj_nazwa'].lower()}",
                                 "od": max(ost, dt.date.today().isoformat()) if ost else dt.date.today().isoformat(),
                                 "do": nowy_termin or ost, "udzialy": [0] * (len(hrf["dzialy"]) - 1) + [100], "status": "planowany"})
            r["hrf"] = S.przelicz_hrf(hrf)
        r.setdefault("aneksy", []).append({"nr": nr_aneksu, "wniosek": w["nr"], "dni": dni, "kwota_netto": kw, "data": j.get("data") or dt.date.today().isoformat()})
        S.zapisz_realizacje(pid, r)
    kat = os.path.join(S.pdir(pid), "wnioski")
    os.makedirs(kat, exist_ok=True)
    c = S.cfg()
    koszt_po = None
    if kw:  # kosztorys podstawowy po zmianie umowy = oferta + dział z aneksu
        baza = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), None)
        dod = S.czytaj(os.path.join(kat, f"kosztorys_{wid}.json"), None)
        if baza and dod:
            if baza.get("dzialy"):  # podstawa = kosztorys przekazany zamawiającemu (bez działu „poza przedmiarem” i notatek wewnętrznych)
                try:
                    baza = S.MO.dla_zamawiajacego(baza)[0]
                except (KeyError, TypeError, ValueError, ZeroDivisionError):
                    pass
            po = json.loads(json.dumps(baza))
            po["dzialy"] = list(baza.get("dzialy", [])) + [{"nazwa": f"Aneks nr {nr_aneksu} – " + (dz.get("nazwa") or ""), "pozycje": dz.get("pozycje", [])}
                                                           for dz in dod.get("dzialy", [])]
            for k in ("netto", "vat_kwota", "brutto"):
                po.pop(k, None)
            po.setdefault("postepowanie", {})["vat"] = vat
            po = S.MO.przelicz(po)
            po["_tytul"] = f"KOSZTORYS PO ZMIANIE UMOWY (ANEKS NR {nr_aneksu})"
            koszt_po = f"Kosztorys_po_aneksie_nr_{nr_aneksu}.xlsx"
            S.MO.zapisz_kosztorys(po, c, os.path.join(kat, koszt_po), dla_klienta=True)
    aneks = f"Aneks_nr_{nr_aneksu}_do_umowy.docx"
    S.WN.aneks_docx(os.path.join(kat, aneks), w, nr_aneksu, S.dane_zamawiajacego_budowy(pid, m),
                  {"nazwa": c.get("firma_nazwa", ""), "adres": c.get("firma_adres", ""), "nip": c.get("firma_nip", "")},
                  um, m.get("nazwa", ""), stary_termin, nowy_termin, stara, nowa if kw else None, vat, j.get("data"))
    m = S.meta(pid)
    w = _wniosek(m, wid)
    w.update(status="zaakceptowany", aneks_nr=nr_aneksu, aneks_plik=f"wnioski/{aneks}", data_akceptacji=j.get("data") or dt.date.today().isoformat(),
             dni_zaakceptowane=dni, kwota_zaakceptowana=kw, kosztorys_po_aneksie=f"wnioski/{koszt_po}" if koszt_po else None)
    S.zapisz_meta(pid, m)
    return jsonify(w)


@bp.get("/api/projekty/<pid>/pogoda")
@S.wymaga_logowania
def pogoda_budowy(pid):
    r = realizacja_dane(pid)
    u = S.ustawienia_pogody(pid, r)
    if not u.get("lat"):
        return jsonify({"ustawienia": u, "presety": S.POG.PRESETY, "blad_lokalizacji": True})
    dzis = dt.date.today()
    try:
        od = dt.date.fromisoformat(request.args.get("od")) if request.args.get("od") else max(dzis - dt.timedelta(days=30), dt.date.fromisoformat(r["data_umowy"]) if r.get("data_umowy") else dzis - dt.timedelta(days=30))
        do = dt.date.fromisoformat(request.args.get("do")) if request.args.get("do") else dzis + dt.timedelta(days=7)
    except ValueError:
        return jsonify({"blad": "Nieprawidłowy okres."}), 400
    if (do - od).days > 400:
        return jsonify({"blad": "Wybierz okres krótszy niż 400 dni."}), 400
    stacja = S.POG.najblizsza_stacja(u["lat"], u["lon"])
    S.zapisz_pomiar_imgw(pid, stacja)
    meteo = S.POG.najblizsze_meteo(u["lat"], u["lon"])  # gęstsza sieć telemetryczna – najbliższa stacja osobno dla każdego parametru
    try:
        wyn = S.POG.analiza(u["lat"], u["lon"], od, do, u["kryteria"], u["kryteria"]["godz_od"], u["kryteria"]["godz_do"],
                          bool(u.get("soboty")), realizacja_dane(pid).get("pogoda_imgw"), (S.czytaj(S.plik_meteo(pid), {}) or {}).get("dni"))
    except Exception as e:
        return jsonify({"blad": f"Nie udało się pobrać danych pogodowych ({e}). Spróbuj za chwilę."}), 502
    hm = S.czytaj(S.plik_meteo(pid), {}) or {}
    return jsonify({"ustawienia": u, "presety": S.POG.PRESETY, "stacja": stacja, "stacje_meteo": meteo, "od": od.isoformat(), "do": do.isoformat(), **wyn,
                    "meteo_historia_od": min(hm.get("dni") or {"": 0}) or None,
                    "termin_zakonczenia": r.get("termin_zakonczenia", "")})


@bp.post("/api/projekty/<pid>/pogoda/ustawienia")
@S.wymaga_logowania
def pogoda_ustawienia(pid):
    j = request.json or {}
    with S.BLOKADA:
        r = realizacja_dane(pid)
        u = r.setdefault("pogoda", {})
        if j.get("lokalizacja"):
            try:
                u.update(lat=float(j["lokalizacja"]["lat"]), lon=float(j["lokalizacja"]["lon"]), opis=str(j["lokalizacja"].get("opis") or j["lokalizacja"].get("nazwa", ""))[:160])
            except (KeyError, TypeError, ValueError):
                return jsonify({"blad": "Wybierz miejscowość z listy podpowiedzi."}), 400
        if j.get("rodzaj") in S.POG.PRESETY:
            if j["rodzaj"] != u.get("rodzaj"):
                u["kryteria"] = {}
            u["rodzaj"] = j["rodzaj"]
        if isinstance(j.get("kryteria"), dict):
            try:
                u["kryteria"] = {k: float(str(v).replace(",", ".")) for k, v in j["kryteria"].items() if k in ("tmin", "tmax", "opad", "snieg", "wiatr")}
            except ValueError:
                return jsonify({"blad": "Progi muszą być liczbami."}), 400
        for k in ("godz_od", "godz_do"):
            if k in j:
                u[k] = max(0, min(24, int(j[k])))
        if "soboty" in j:
            u["soboty"] = bool(j["soboty"])
        if j.get("liczenie") in S.POG.LICZENIE_TERMINU:  # sposób liczenia terminu w umowie (H3-01)
            u["liczenie"] = j["liczenie"]
        S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/pogoda/pismo")
@S.wymaga_logowania
def pogoda_pismo(pid):
    """Informacja albo wniosek o przedłużenie terminu z powodu warunków atmosferycznych (Word)."""
    j = request.json or {}
    m, r = S.meta(pid), realizacja_dane(pid)
    u = S.ustawienia_pogody(pid, r)
    if not u.get("lat"):
        return jsonify({"blad": "Ustaw lokalizację budowy do monitoringu pogody."}), 400
    try:
        od, do = dt.date.fromisoformat(j["od"]), dt.date.fromisoformat(j["do"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"blad": "Wybierz okres (od – do)."}), 400
    do = min(do, dt.date.today())
    wyn = S.POG.analiza(u["lat"], u["lon"], od, do, u["kryteria"], u["kryteria"]["godz_od"], u["kryteria"]["godz_do"], bool(u.get("soboty")),
                      r.get("pogoda_imgw"), (S.czytaj(S.plik_meteo(pid), {}) or {}).get("dni"))
    try:
        dni = int(j.get("dni") if j.get("dni") not in (None, "") else wyn["niekorzystne"])
        assert 0 <= dni <= 365
    except (ValueError, TypeError, AssertionError):
        return jsonify({"blad": "Podaj liczbę dni roboczych przedłużenia (0–365)."}), 400
    # H3-01: dni robocze z warunkami niekorzystnymi liczone jako robocze (bez sobót, niedziel i świąt); umowa w dniach kalendarzowych – przeliczenie jawne
    liczenie = j.get("liczenie") if j.get("liczenie") in S.POG.LICZENIE_TERMINU else (u.get("liczenie") or "robocze")
    stary = None
    if r.get("termin_zakonczenia"):
        try:
            stary = dt.date.fromisoformat(r["termin_zakonczenia"])
        except ValueError:
            pass
    pd = S.POG.przedluzenie(dni, stary, liczenie, baza=do)
    nowy = pd["nowy_termin"]
    c = S.cfg()
    zam = S.dane_zamawiajacego_budowy(pid, m)
    if j.get("zam_nazwa"):
        zam = {"nazwa": j["zam_nazwa"], "adres": j.get("zam_adres", "")}
    stacja = dict(S.POG.najblizsza_stacja(u["lat"], u["lon"]) or {}, meteo=S.POG.najblizsze_meteo(u["lat"], u["lon"]))
    kat = os.path.join(S.pdir(pid), "realizacja", "dokumenty")
    os.makedirs(kat, exist_ok=True)
    rodzaj = "wniosek" if j.get("rodzaj", "wniosek") == "wniosek" else "informacja"
    nazwa = f"{'Wniosek_przedluzenie_terminu' if rodzaj == 'wniosek' else 'Informacja_warunki_pogodowe'}_{od:%Y-%m-%d}_{do:%Y-%m-%d}.docx"
    S.POG.pismo_docx(os.path.join(kat, nazwa), rodzaj,
                   {"nazwa": c.get("firma_nazwa", ""), "adres": c.get("firma_adres", ""), "nip": c.get("firma_nip", "")}, zam,
                   m.get("nazwa", ""), {"nr": r.get("umowa_nr"), "data": r.get("data_umowy"), "adres": r.get("adres")}, (od, do), wyn,
                   {**u["kryteria"], "nazwa": S.POG.PRESETY.get(u["rodzaj"], {}).get("nazwa", "roboty budowlane")}, stacja,
                   f"{u.get('opis', '')}, {u['lat']:.4f}, {u['lon']:.4f}", dni, nowy, str(j.get("uwagi", ""))[:2000],
                   str(j.get("miejsce") or (c.get("firma_adres", "").split(",")[-1].strip().split(" ")[-1] if c.get("firma_adres") else "")),
                   liczenie=liczenie, stary_termin=stary, dziennik=realizacja_pelna(pid).get("dziennik"), wpisy_edb=str(j.get("wpisy_dziennika") or "")[:300])
    with S.BLOKADA:
        r = realizacja_dane(pid)
        r.setdefault("pisma_pogodowe", []).append({"plik": f"realizacja/dokumenty/{nazwa}", "rodzaj": rodzaj, "od": od.isoformat(), "do": do.isoformat(),
                                                  "dni": dni, "dni_kalendarzowe": pd["dni_kalendarzowe"], "liczenie": liczenie,
                                                  "niekorzystne": wyn["niekorzystne"], "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
        S.zapisz_realizacje(pid, r)
    return jsonify({"url": f"/pobierz/{pid}/realizacja/dokumenty/{nazwa}", "niekorzystne": wyn["niekorzystne"], "dni": dni,
                    "dni_kalendarzowe": pd["dni_kalendarzowe"], "liczenie": liczenie, "nowy_termin": nowy.isoformat() if nowy else None})


@bp.post("/api/projekty/<pid>/pogoda/przesun")
@S.wymaga_logowania
def pogoda_przesun(pid):
    """Po zgodzie zamawiającego: przesuwa termin zakończenia i nieodebrane etapy harmonogramu o N dni."""
    try:
        n = int((request.json or {}).get("dni"))
        assert 0 < n <= 365
    except (TypeError, ValueError, AssertionError):
        return jsonify({"blad": "Podaj liczbę dni (1–365)."}), 400
    with S.BLOKADA:
        r = realizacja_dane(pid)
        # H3-01: przy umowie liczonej w dniach roboczych termin przesuwa się o n dni roboczych (bez sobót, niedziel i świąt),
        # a nieodebrane etapy – o tyle samo dni kalendarzowych
        lj = (request.json or {}).get("liczenie")
        rob = (lj if lj in S.POG.LICZENIE_TERMINU else (r.get("pogoda") or {}).get("liczenie", "robocze")) == "robocze"
        try:
            stary = dt.date.fromisoformat(r["termin_zakonczenia"]) if r.get("termin_zakonczenia") else None
        except ValueError:
            stary = None
        delta = (S.POG.dodaj_dni_robocze(stary or dt.date.today(), n) - (stary or dt.date.today())).days if rob else n
        przes = lambda s_: (dt.date.fromisoformat(s_) + dt.timedelta(days=delta)).isoformat() if s_ else s_
        if stary:
            r["termin_zakonczenia"] = przes(r["termin_zakonczenia"])
        ile = 0
        for e in (r.get("hrf") or {}).get("etapy", []):
            if e.get("status") != "odebrany":
                e["od"], e["do"] = przes(e.get("od")), przes(e.get("do"))
                ile += 1
        r.setdefault("przedluzenia", []).append({"dni": n, "dni_kalendarzowe": delta, "liczenie": "robocze" if rob else "kalendarzowe",
                                                 "data": dt.date.today().isoformat(), "kto": session.get("login", "")})
        S.zapisz_realizacje(pid, r)
    return jsonify({"termin_zakonczenia": r.get("termin_zakonczenia"), "etapy": ile, "dni_kalendarzowe": delta, "liczenie": "robocze" if rob else "kalendarzowe"})


@bp.post("/api/projekty/<pid>/hrf/utworz")
@S.wymaga_logowania
def hrf_utworz(pid):
    m_ = S.meta(pid)
    r0 = realizacja_dane(pid)
    ZR = m_.get("strona") == "zamawiajacy"
    RZ = (m_.get("rodzaj_zamowienia") or "roboty") if ZR else "roboty"
    dz = S.dzialy_kosztorysu(pid)
    wart_um = float(r0.get("wartosc_netto") or 0)
    if ZR and not wart_um:
        return jsonify({"blad": "Najpierw wpisz w danych umowy wartość umowy netto – cenę z oferty wybranego wykonawcy."}), 400
    if not dz and ZR and wart_um:
        dz = [{"nazwa": "Przedmiot umowy", "wartosc": wart_um}]
    if not dz:
        return jsonify({"blad": "Wpisz wartość umowy w danych umowy (albo przygotuj kosztorys inwestorski)." if ZR else
                        "Brak kosztorysu – najpierw przygotuj ofertę w zakładce Projekty."}), 400
    if wart_um:  # wartości działów przeliczone na cenę umowy (kosztorys inwestorski to tylko szacunek; u wykonawcy – cena po aneksach / negocjacjach)
        suma0 = sum(x["wartosc"] for x in dz) or 1
        dz = [dict(x, wartosc=S.MO.zaokr(x["wartosc"] * wart_um / suma0)) for x in dz]
        if dz:  # groszowa reszta z zaokrągleń w największym dziale – suma harmonogramu = cena umowy
            nmax = max(range(len(dz)), key=lambda i: dz[i]["wartosc"])
            dz[nmax]["wartosc"] = S.MO.zaokr(dz[nmax]["wartosc"] + wart_um - sum(x["wartosc"] for x in dz))
    try:
        n = max(1, min(24, int(request.json.get("etapy", 4))))
        start = dt.date.fromisoformat(request.json.get("start"))
        dl = max(1, int(request.json.get("dlugosc", 30)))
    except (TypeError, ValueError):
        return jsonify({"blad": "Podaj liczbę etapów, datę startu i długość etapu."}), 400
    suma = sum(x["wartosc"] for x in dz) or 1
    etapy = [{"nr": i + 1, "nazwa": f"Etap {i + 1}", "od": (start + dt.timedelta(days=i * dl)).isoformat(),
              "do": (start + dt.timedelta(days=(i + 1) * dl - 1)).isoformat(), "udzialy": [0] * len(dz),
              "status": "planowany"} for i in range(n)]
    narast = 0.0
    for i, x in enumerate(dz):  # działy kolejno, rozłożone tak, by wartości etapów były zbliżone
        a, b = narast / suma * n, (narast + x["wartosc"]) / suma * n
        narast += x["wartosc"]
        if b - a <= 1e-9:
            etapy[min(n - 1, int(a))]["udzialy"][i] = 100
            continue
        udz = [max(0.0, min(b, k + 1) - max(a, k)) / (b - a) * 100 for k in range(n)]
        udz = [round(u, 2) for u in udz]
        kmax = max(range(n), key=lambda k: udz[k])
        udz[kmax] = round(udz[kmax] + 100 - sum(udz), 2)
        for k in range(n):
            etapy[k]["udzialy"][i] = udz[k]
    for e in etapy:
        nazwy = [re.sub(r"^[0-9.]+\s*", "", dz[i]["nazwa"]) for i, u in enumerate(e["udzialy"]) if u]
        if nazwy:
            e["nazwa"] = "; ".join(nazwy)[:120]
    if RZ in ("uslugi", "dostawy"):  # usługi świadczone w każdym okresie, dostawy częściowe – każdy dział po równo
        # udział 100/n bez zaokrąglenia do 0,01% – kwota okresu = wartość / n co do grosza (100 000 / 12 = 11 × 8 333,33 + 8 333,37);
        # groszową resztę dopisuje przelicz_hrf w ostatnim okresie
        rowne = [round(100 / n, 10)] * n
        rowne[-1] = round(100 - sum(rowne[:-1]), 10)
        for k, e in enumerate(etapy):
            e["udzialy"] = [rowne[k]] * len(dz)
            if RZ == "uslugi":
                mies = (start.month - 1 + k) % 12 + 1
                rok = start.year + (start.month - 1 + k) // 12
                e["od"] = dt.date(rok, mies, 1 if k else start.day).isoformat()
                kon = (dt.date(rok + (mies // 12), mies % 12 + 1, 1) - dt.timedelta(days=1)) if dl >= 28 else dt.date.fromisoformat(e["do"])
                e["do"] = kon.isoformat()
                e["nazwa"] = f"Okres rozliczeniowy {k + 1} ({mies:02d}.{rok})" if dl >= 28 else f"Okres rozliczeniowy {k + 1}"
            else:
                e["nazwa"] = f"Dostawa częściowa {k + 1}" if n > 1 else "Dostawa"
    r = realizacja_dane(pid)
    r["hrf"] = S.przelicz_hrf({"dzialy": dz, "etapy": etapy})
    S.zapisz_realizacje(pid, r)
    return jsonify(r["hrf"])


@bp.post("/api/projekty/<pid>/hrf/zapisz")
@S.wymaga_logowania
def hrf_zapisz(pid):
    r = realizacja_dane(pid)
    if not r.get("hrf"):
        return jsonify({"blad": "Najpierw utwórz harmonogram."}), 400
    dz = r["hrf"]["dzialy"]
    stare = {e["nr"]: e for e in r["hrf"]["etapy"]}
    etapy = []
    for i, e in enumerate(request.json.get("etapy", []), 1):
        try:
            udz = [max(0.0, min(100.0, float(str(x).replace(",", ".") or 0))) for x in e.get("udzialy", [])][:len(dz)]
        except ValueError:
            return jsonify({"blad": f"Błędny procent w etapie {i}."}), 400
        udz += [0.0] * (len(dz) - len(udz))
        s0 = stare.get(e.get("nr"), {})
        etapy.append({"nr": i, "nazwa": str(e.get("nazwa", f"Etap {i}"))[:150], "od": e.get("od", ""), "do": e.get("do", ""),
                      "udzialy": udz, "status": s0.get("status", "planowany"), "data_odbioru": s0.get("data_odbioru"),
                      "protokol": s0.get("protokol")})
    r["hrf"]["etapy"] = etapy
    r["hrf"] = S.przelicz_hrf(r["hrf"])
    S.zapisz_realizacje(pid, r)
    return jsonify(r["hrf"])


@bp.get("/api/projekty/<pid>/hrf/xlsx")
@S.wymaga_logowania
def hrf_xlsx(pid):
    if not realizacja_dane(pid).get("hrf"):
        abort(404)
    d = os.path.join(S.pdir(pid), "realizacja")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"HRF_{S.MO.bezpieczna_nazwa(S.meta(pid).get('nazwa', 'budowa'))[:60]}.xlsx")
    S.zapisz_hrf_xlsx(pid, p)
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


@bp.get("/api/projekty/<pid>/podwykonawcy")
@S.wymaga_logowania
def podwykonawcy_lista(pid):
    r = realizacja_dane(pid)
    zad = r.get("zadania_oswiadczen") or []
    for z in zad:
        k = os.path.join(S.pdir(pid), "realizacja", "podwykonawcy", "_zadania", z["id"])
        z["otrzymane"] = sorted(os.listdir(k)) if os.path.isdir(k) else []
    lista = S._pw_lista(pid, r)
    if not S.moze("finanse"):
        lista = [_pw_bez_finansow(x) for x in lista]
    return jsonify({"podwykonawcy": lista, "zadania": zad, "statusy": S.PW.STATUSY_ZGL, "strona": S.meta(pid).get("strona") or "wykonawca",
                    "dokumenty": r.get("pw_dokumenty") or []})


@bp.post("/api/projekty/<pid>/podwykonawcy")
@S.wymaga_logowania
def podwykonawcy_zapisz(pid):
    wyn = []
    fin = S.moze("finanse", 2)
    stare = {x.get("id"): x for x in realizacja_dane(pid).get("podwykonawcy") or [] if isinstance(x, dict)}
    for x in (request.json or {}).get("podwykonawcy") or []:
        if not isinstance(x, dict) or not str(x.get("nazwa", "")).strip():
            continue
        if not fin:  # rola bez edycji Finansów nie widzi kwot – zapis nie może ich wyzerować
            st = stare.get(x.get("id")) or {}
            x = {**x, "wartosc_netto": st.get("wartosc_netto"), "vat": st.get("vat"), "platnosci": st.get("platnosci") or []}
        notatka = x.get("notatka") if "notatka" in x else (x.get("uwagi") if isinstance(x.get("uwagi"), str) else (stare.get(x.get("id")) or {}).get("notatka", ""))
        tp = S.PW._f(x.get("termin_platnosci") or 30)
        plat = []
        for p in x.get("platnosci") or []:
            if not str(p.get("faktura", "")).strip() and not S.PW._f(p.get("kwota_brutto")):
                continue
            termin = str(p.get("termin") or "")[:10]
            if not termin and str(p.get("data") or "")[:10]:  # bez terminu faktura nigdy nie byłaby zaległa – termin z umowy (art. 463 Pzp: najwyżej 30 dni)
                try:
                    termin = (dt.date.fromisoformat(str(p["data"])[:10]) + dt.timedelta(days=int(tp or 30))).isoformat()
                except ValueError:
                    termin = ""
            plat.append({"id": S.DOT.bezpieczna(p.get("id") or uuid.uuid4().hex[:8]), "faktura": str(p.get("faktura") or "")[:60], "data": str(p.get("data") or "")[:10],
                         "termin": termin, "kwota_brutto": round(S.PW._f(p.get("kwota_brutto")), 2), "zaplacono": bool(p.get("zaplacono")),
                         "data_zaplaty": str(p.get("data_zaplaty") or "")[:10], "etap": str(p.get("etap") or "")[:120]})
        wyn.append({"id": S.DOT.bezpieczna(x.get("id") or uuid.uuid4().hex[:8]), "nazwa": str(x["nazwa"])[:200], "nip": str(x.get("nip") or "")[:20],
                    "adres": str(x.get("adres") or "")[:200], "kontakt": str(x.get("kontakt") or "")[:200], "zakres": str(x.get("zakres") or "")[:1000],
                    "wartosc_netto": round(S.PW._f(x.get("wartosc_netto")), 2), "vat": str(x.get("vat") or "23")[:4], "data_umowy": str(x.get("data_umowy") or "")[:10],
                    "termin_realizacji": str(x.get("termin_realizacji") or "")[:60], "termin_platnosci": str(x.get("termin_platnosci") or "30")[:4],
                    "status": x.get("status") if x.get("status") in S.PW.STATUSY_ZGL else "niezgłoszony", "data_zgloszenia": str(x.get("data_zgloszenia") or "")[:10],
                    "notatka": str(notatka or "")[:500], "platnosci": plat})
    with S.BLOKADA:
        r = realizacja_dane(pid)
        r["podwykonawcy"] = wyn
        S.zapisz_realizacje(pid, r)
    return jsonify({"zapisano": len(wyn)})


@bp.post("/api/projekty/<pid>/podwykonawcy/plik")
@S.wymaga_logowania
def podwykonawcy_plik(pid):
    idp = S.DOT.bezpieczna(request.form.get("id", ""))
    rodz = request.form.get("rodzaj") if request.form.get("rodzaj") in ("umowa", "oswiadczenia", "dokumenty", "zadanie") else "dokumenty"
    kat = os.path.join(S.pdir(pid), "realizacja", "podwykonawcy", "_zadania" if rodz == "zadanie" else idp, idp if rodz == "zadanie" else rodz)
    if request.form.get("usun"):
        p = os.path.join(kat, os.path.basename(request.form["usun"]))
        if os.path.isfile(p):
            os.remove(p)
        return jsonify({"ok": True})
    os.makedirs(kat, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(kat, S.secure_filename_pl(f.filename)))
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/podwykonawcy/dokument")
@S.wymaga_logowania
def podwykonawcy_dokument(pid):
    """Zgłoszenie podwykonawcy, oświadczenie podwykonawcy o rozliczeniu, oświadczenie wykonawcy o niezaleganiu albo
    (zamawiający) wezwanie wykonawcy do przedstawienia oświadczeń o rozliczeniu z podwykonawcami."""
    j = request.json or {}
    m, r = S.meta(pid), realizacja_dane(pid)
    rodz = j.get("rodzaj")
    lista = S._pw_lista(pid, r)
    wyk, zam = S._strony_budowy(pid, m, r)
    o = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), {}).get("postepowanie", {})
    budowa = o.get("nazwa_zamowienia") or m.get("nazwa", "")
    umowa_nr, miejsce = r.get("umowa_nr", ""), j.get("miejsce") or ""
    do_dnia = j.get("do_dnia") or dt.date.today().isoformat()
    kat = os.path.join(S.pdir(pid), "realizacja", "podwykonawcy")
    os.makedirs(kat, exist_ok=True)
    pw = next((x for x in lista if x["id"] == j.get("id")), None)
    if rodz in ("zgloszenie", "oswiadczenie_pw") and not pw:
        return jsonify({"blad": "Wybierz podwykonawcę."}), 400
    if rodz == "zgloszenie":
        nazwa = f"Zgloszenie_podwykonawcy_{S.DOT.bezpieczna(pw['nazwa'])[:40]}.docx"
        S.PW.zgloszenie_docx(os.path.join(kat, nazwa), pw, budowa, wyk, zam, umowa_nr, miejsce)
        with S.BLOKADA:
            r = realizacja_dane(pid)
            for x in r.get("podwykonawcy") or []:
                if x["id"] == pw["id"] and x.get("status") == "niezgłoszony":
                    x.update(status="zgłoszony", data_zgloszenia=dt.date.today().isoformat())
            S.zapisz_realizacje(pid, r)
    elif rodz == "oswiadczenie_pw":
        nazwa = f"Oswiadczenie_podwykonawcy_{S.DOT.bezpieczna(pw['nazwa'])[:40]}_{do_dnia}.docx"
        S.PW.oswiadczenie_pw_docx(os.path.join(kat, nazwa), pw, budowa, wyk, do_dnia, miejsce)
    elif rodz == "oswiadczenie_wyk":
        wyb = [x for x in lista if not j.get("ids") or x["id"] in j["ids"]]
        if not wyb:
            return jsonify({"blad": "Brak podwykonawców do ujęcia w oświadczeniu."}), 400
        nazwa = f"Oswiadczenie_wykonawcy_o_rozliczeniu_z_podwykonawcami_{do_dnia}.docx"
        S.PW.oswiadczenie_wyk_docx(os.path.join(kat, nazwa), wyb, budowa, wyk, zam, umowa_nr, do_dnia, j.get("zakres", ""), miejsce)
    elif rodz == "zadanie":
        termin = j.get("termin") or (dt.date.today() + dt.timedelta(days=7)).isoformat()
        nazwa = f"Wezwanie_o_oswiadczenia_podwykonawcow_{dt.date.today():%Y-%m-%d}.docx"
        S.PW.zadanie_docx(os.path.join(kat, nazwa), zam, wyk, budowa, umowa_nr, j.get("zakres", ""), termin, lista, miejsce)
        with S.BLOKADA:
            r = realizacja_dane(pid)
            r.setdefault("zadania_oswiadczen", []).append({"id": uuid.uuid4().hex[:8], "data": dt.date.today().isoformat(), "zakres": str(j.get("zakres") or "")[:300],
                                                           "termin": termin, "status": "wysłane", "plik": f"realizacja/podwykonawcy/{nazwa}"})
            S.zapisz_realizacje(pid, r)
    else:
        return jsonify({"blad": "Nieznany rodzaj dokumentu."}), 400
    sc = f"realizacja/podwykonawcy/{nazwa}"
    with S.BLOKADA:
        r = realizacja_dane(pid)
        dok = [x for x in (r.get("pw_dokumenty") or []) if x.get("plik") != sc]
        r["pw_dokumenty"] = [{"plik": sc, "rodzaj": rodz, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "podwykonawca": (pw or {}).get("nazwa", "")}] + dok[:60]
        S.zapisz_realizacje(pid, r)
    return jsonify({"plik": sc, "url": f"/pobierz/{pid}/{S.urllib.parse.quote(sc)}"})


@bp.post("/api/projekty/<pid>/podwykonawcy/zadanie-status")
@S.wymaga_logowania
def podwykonawcy_zadanie_status(pid):
    j = request.json or {}
    with S.BLOKADA:
        r = realizacja_dane(pid)
        for z in r.get("zadania_oswiadczen") or []:
            if z["id"] == j.get("id"):
                if j.get("usun"):
                    r["zadania_oswiadczen"].remove(z)
                else:
                    z["status"] = j.get("status") if j.get("status") in ("wysłane", "otrzymane – kompletne", "otrzymane – braki") else z["status"]
                break
        S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


@bp.get("/api/projekty/<pid>/rozliczenie-mat")
@S.wymaga_logowania
def rozliczenie_mat(pid):
    r = realizacja_dane(pid)
    rm = r.get("rozliczenie_mat") or {"pozycje": []}
    for x in rm["pozycje"]:
        k = os.path.join(S.pdir(pid), "realizacja", "karty_materialowe", x["id"])
        x["zalaczniki"] = sorted(os.listdir(k)) if os.path.isdir(k) else []
    m = S.meta(pid)
    return jsonify({**rm, "ma_liste": bool(m.get("lista_materialow")), "ma_kosztorys": os.path.isfile(os.path.join(S.pdir(pid), "oferta_dane.json"))})


@bp.post("/api/projekty/<pid>/rozliczenie-mat/import")
@S.wymaga_logowania
def rozliczenie_mat_import(pid):
    nowe = S._materialy_z_listy(pid, S.meta(pid))
    if not nowe:
        return jsonify({"blad": "Brak kosztorysu i listy materiałów – dodaj pozycje ręcznie."}), 400
    with S.BLOKADA:
        r = realizacja_dane(pid)
        rm = r.setdefault("rozliczenie_mat", {"pozycje": []})
        if (request.json or {}).get("zastap"):
            rm["pozycje"] = []
        znane = {S._norm(x.get("nazwa")) for x in rm["pozycje"]}
        dodane = [x for x in nowe if S._norm(x["nazwa"]) not in znane]
        rm["pozycje"] += dodane
        rm["data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        S.zapisz_realizacje(pid, r)
    return jsonify({"dodano": len(dodane), "zrodlo": nowe[0]["zrodlo"]})


@bp.post("/api/projekty/<pid>/rozliczenie-mat")
@S.wymaga_logowania
def rozliczenie_mat_zapisz(pid):
    poz = []
    for x in (request.json or {}).get("pozycje") if isinstance((request.json or {}).get("pozycje"), list) else []:
        if not isinstance(x, dict) or not str(x.get("nazwa", "")).strip():
            continue
        try:
            il_k = float(str(x.get("ilosc_kosztorys") or 0).replace(",", ".").replace(" ", ""))
            il_z = float(str(x.get("ilosc_zuzyta") or 0).replace(",", ".").replace(" ", ""))
        except ValueError:
            return jsonify({"blad": f"Nieprawidłowa ilość: {x.get('nazwa', '')[:40]}"}), 400
        poz.append({"id": S.DOT.bezpieczna(x.get("id") or uuid.uuid4().hex[:8]), "nazwa": str(x["nazwa"])[:300], "producent": str(x.get("producent") or "")[:200],
                    "jm": str(x.get("jm") or "")[:20], "ilosc_kosztorys": il_k, "ilosc_zuzyta": il_z, "dokumenty": str(x.get("dokumenty") or "")[:300],
                    "uwagi": str(x.get("uwagi") or "")[:300], "karta": bool(x.get("karta")), "zrodlo": str(x.get("zrodlo") or "dodane ręcznie")[:40]})
    with S.BLOKADA:
        r = realizacja_dane(pid)
        r["rozliczenie_mat"] = {"pozycje": poz, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        S.zapisz_realizacje(pid, r)
    return jsonify({"zapisano": len(poz)})


@bp.post("/api/projekty/<pid>/rozliczenie-mat/zalacznik")
@S.wymaga_logowania
def rozliczenie_mat_zalacznik(pid):
    mid = S.DOT.bezpieczna(request.form.get("id", ""))
    if request.form.get("usun"):
        p = os.path.join(S.pdir(pid), "realizacja", "karty_materialowe", mid, os.path.basename(request.form["usun"]))
        if os.path.isfile(p):
            os.remove(p)
        return jsonify({"ok": True})
    kat = os.path.join(S.pdir(pid), "realizacja", "karty_materialowe", mid)
    os.makedirs(kat, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(kat, S.secure_filename_pl(f.filename)))
    return jsonify({"zalaczniki": sorted(os.listdir(kat))})


@bp.post("/api/projekty/<pid>/rozliczenie-mat/dokumenty")
@S.wymaga_logowania
def rozliczenie_mat_dokumenty(pid):
    """Wykaz zużytych materiałów (Word i Excel), karty materiałowe wybranych pozycji (Word) i komplet ZIP z załącznikami –
    do dołączenia do protokołu odbioru końcowego."""
    import zipfile
    import openpyxl
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    m, r, c = S.meta(pid), realizacja_dane(pid), S.cfg()
    poz = [x for x in ((r.get("rozliczenie_mat") or {}).get("pozycje") or []) if str(x.get("nazwa", "")).strip()]
    if not poz:
        return jsonify({"blad": "Najpierw przygotuj wykaz materiałów (Pobierz z kosztorysu albo Dodaj pozycję) i zapisz go."}), 400
    kat = os.path.join(S.pdir(pid), "realizacja", "rozliczenie")
    os.makedirs(kat, exist_ok=True)
    o = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), {}).get("postepowanie", {})
    budowa = o.get("nazwa_zamowienia") or m.get("nazwa", "")
    dzis = dt.date.today()
    d = S.MO._doc()
    S.MO._akapit(d, f"{budowa}" + (f" · umowa nr {r['umowa_nr']}" if r.get("umowa_nr") else "") + (f" · {r['adres']}" if r.get("adres") else ""),
               rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    S.dodaj_wykaz_materialow(d, poz, f"Załącznik do protokołu odbioru końcowego · {dzis:%d.%m.%Y}")
    wykaz = f"Wykaz_zuzytych_materialow_{dzis:%Y-%m-%d}.docx"
    d.save(os.path.join(kat, wykaz))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zużyte materiały"
    ws.append(["Lp.", "Materiał", "Producent / typ", "j.m.", "Ilość wg kosztorysu", "Ilość zużyta", "Różnica", "Dokumenty", "Karta materiałowa", "Uwagi"])
    for i, x in enumerate(poz, 1):
        ws.append([i, x["nazwa"], x.get("producent", ""), x.get("jm", ""), x.get("ilosc_kosztorys") or 0, x.get("ilosc_zuzyta") or 0,
                   round((x.get("ilosc_zuzyta") or 0) - (x.get("ilosc_kosztorys") or 0), 3), x.get("dokumenty", ""), "tak" if x.get("karta") else "", x.get("uwagi", "")])
    for k_, sz in zip("ABCDEFGHIJ", (5, 50, 26, 7, 14, 12, 10, 30, 10, 30)):
        ws.column_dimensions[k_].width = sz
    wykaz_x = f"Wykaz_zuzytych_materialow_{dzis:%Y-%m-%d}.xlsx"
    wb.save(os.path.join(kat, wykaz_x))
    karty = []
    strona_zam = (m.get("strona") or "wykonawca") in ("zamawiajacy", "inwestor")
    for i, x in enumerate([y for y in poz if y.get("karta")], 1):
        zal_k = os.path.join(S.pdir(pid), "realizacja", "karty_materialowe", x["id"])
        zal = sorted(os.listdir(zal_k)) if os.path.isdir(zal_k) else []
        d = S.MO._doc()
        P = lambda t, **k: S.MO._akapit(d, t, **k)
        P(f"KARTA MATERIAŁOWA nr {i}", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        P(f"Zadanie: {budowa}" + (f" · umowa nr {r['umowa_nr']}" if r.get("umowa_nr") else ""), wyrownanie=WD_ALIGN_PARAGRAPH.CENTER, rozmiar=9)
        S.MO._tabela(d, [["Pole", "Treść"],
                       ["Wykonawca", (r.get("wykonawca_nazwa") if strona_zam else c.get("firma_nazwa")) or "[UZUPEŁNIJ]"],
                       ["Zamawiający", (c.get("firma_nazwa") if strona_zam else (o.get("zamawiajacy_nazwa") or r.get("zam_nazwa"))) or "[UZUPEŁNIJ]"],
                       ["Nazwa materiału / wyrobu", x["nazwa"]], ["Producent / typ / model", x.get("producent") or "[UZUPEŁNIJ]"],
                       ["Ilość", f"{S._lb(x.get('ilosc_zuzyta'))} {x.get('jm', '')}"], ["Miejsce wbudowania / zastosowanie", x.get("uwagi") or "[UZUPEŁNIJ]"],
                       ["Dokumenty odniesienia (DoP, CE/B, aprobata, normy)", x.get("dokumenty") or "[UZUPEŁNIJ]"],
                       ["Załączniki", "\n".join(zal) or "–"]])
        P("Wykonawca wnosi o zatwierdzenie powyższego materiału do wbudowania i oświadcza, że jest on zgodny z dokumentacją projektową, "
          "specyfikacją techniczną i posiada dokumenty dopuszczające do stosowania w budownictwie.", rozmiar=9)
        S.MO._tabela(d, [["Wykonawca / kierownik budowy:\n\n\n.............................", "Decyzja inspektora nadzoru / Zamawiającego:\n☐ zatwierdzam   ☐ nie zatwierdzam\n\n.............................", "Data:\n\n\n............................."]],
                   naglowek=False)
        nazwa_k = f"Karta_materialowa_{i:02d}_{S.DOT.bezpieczna(x['nazwa'])[:40]}.docx"
        d.save(os.path.join(kat, nazwa_k))
        karty.append((nazwa_k, x, zal))
    zipn = f"Rozliczenie_materialow_do_protokolu_koncowego_{dzis:%Y-%m-%d}.zip"
    with zipfile.ZipFile(os.path.join(kat, zipn), "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(kat, wykaz), f"01_{wykaz}")
        zf.write(os.path.join(kat, wykaz_x), f"01_{wykaz_x}")
        for nazwa_k, x, zal in karty:
            folder = f"02_Karty_materialowe/{os.path.splitext(nazwa_k)[0]}"
            zf.write(os.path.join(kat, nazwa_k), f"{folder}/{nazwa_k}")
            for f in zal:
                zf.write(os.path.join(S.pdir(pid), "realizacja", "karty_materialowe", x["id"], f), f"{folder}/zalaczniki/{f}")
    pr = lambda n: f"realizacja/rozliczenie/{n}"
    with S.BLOKADA:
        r = realizacja_dane(pid)
        r.setdefault("rozliczenie_mat", {"pozycje": poz})["dokumenty"] = {"wykaz": pr(wykaz), "wykaz_xlsx": pr(wykaz_x), "karty": [pr(k[0]) for k in karty],
                                                                          "zip": pr(zipn), "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        S.zapisz_realizacje(pid, r)
    return jsonify(r["rozliczenie_mat"]["dokumenty"])


@bp.post("/api/projekty/<pid>/faktury")
@S.wymaga_logowania
def faktura_dodaj(pid):
    j = request.json
    try:
        netto = S._liczba(j.get("netto"))
        v_ = str(j.get("vat") or realizacja_dane(pid).get("vat") or "").replace(",", ".").replace("%", "").strip()
        if not v_:
            return jsonify({"blad": "Podaj stawkę VAT faktury (ustal z zamawiającym lub z umowy)."}), 400
        vat = float(v_) / (100 if float(v_) > 1 else 1)
        data = dt.date.fromisoformat(j.get("data"))
        termin = dt.date.fromisoformat(j.get("termin")) if j.get("termin") else data + dt.timedelta(days=30)
    except (TypeError, ValueError):
        return jsonify({"blad": "Uzupełnij numer, datę i kwotę netto faktury."}), 400
    if not str(j.get("numer", "")).strip() or netto == 0:
        return jsonify({"blad": "Uzupełnij numer i kwotę netto faktury."}), 400
    r = realizacja_dane(pid)
    # suma faktur nie może przekroczyć wartości umowy (z aneksami) – nie dotyczy budowy domu (wydatki u wielu wykonawców)
    wart = float(r.get("wartosc_netto") or 0)
    if wart > 0 and (S.meta(pid).get("strona") or "wykonawca") != "inwestor":
        dotad = sum(float(f.get("netto") or 0) for f in r["faktury"] if not f.get("archiwum"))
        if dotad + netto > wart + 0.01:
            zostalo = max(0.0, wart - dotad)
            return jsonify({"blad": f"Suma faktur przekroczyłaby wartość umowy ({S.MO.zl(wart)} netto). Zafakturowano już {S.MO.zl(dotad)} netto, "
                                    f"do zafakturowania zostało {S.MO.zl(zostalo)} netto. Jeśli wykonano roboty dodatkowe – najpierw zawrzyj aneks "
                                    "(sekcja „Zmiany umowy: wnioski i aneksy” w projekcie); wartość umowy zwiększy się automatycznie."}), 400
    r["faktury"].append({"id": uuid.uuid4().hex[:10], "numer": str(j["numer"]).strip()[:60], "data": data.isoformat(),
                         "termin": termin.isoformat(), "netto": netto, "vat": vat, "vat_kwota": S.MO.zaokr(netto * vat),
                         "brutto": S.MO.zaokr(netto + S.MO.zaokr(netto * vat)), "etap": j.get("etap"),
                         "opis": str(j.get("opis", ""))[:200], "zaplacona": bool(j.get("zaplacona")),
                         "data_zaplaty": j.get("data_zaplaty") or (dt.date.today().isoformat() if j.get("zaplacona") else None),
                         "kto": session.get("login", "")})
    S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


def realizacja_pelna(pid):
    r = realizacja_dane(pid)
    for k in ("zdjecia", "dziennik", "usterki"):
        r.setdefault(k, [])
    return r


@bp.post("/api/projekty/<pid>/dziennik/auto")
@S.wymaga_logowania
def dziennik_auto(pid):
    """Propozycja wpisu: pogoda, pracownicy z ewidencji godzin, zdjęcia z danego dnia."""
    try:
        dzien = dt.date.fromisoformat(str((request.json or {}).get("data") or dt.date.today().isoformat()))
    except ValueError:
        return jsonify({"blad": "Nieprawidłowa data."}), 400
    r = realizacja_pelna(pid)
    m = S.meta(pid)
    wsp = S.wspolrzedne(pid, r)
    pog = S.BUD.opis_pogody(S.BUD.pogoda(wsp["lat"], wsp["lon"], dzien)) if wsp else ""
    wpisy = [w for w in S.robocizna_projektu(pid, m.get("nazwa")) if w["data"] == dzien.isoformat()]
    osoby = {}
    for w in wpisy:
        osoby[w["imie"]] = osoby.get(w["imie"], 0) + w["godziny"]
    prac = ", ".join(f"{k} ({v:g} h)" for k, v in osoby.items())
    if prac:
        prac = f"{len(osoby)} os.: " + prac
    prace = "; ".join(sorted({w["opis"] for w in wpisy if w.get("opis")}))
    materialy = "; ".join(f"{k['opis']} ({k.get('dostawca', '')})".replace(" ()", "") for k in r.get("koszty", [])
                          if k.get("data") == dzien.isoformat() and k.get("kategoria") == "materiały")
    zdj = [z["id"] for z in r["zdjecia"] if z.get("data") == dzien.isoformat() and not z.get("archiwum")]
    return jsonify({"pogoda": pog, "pracownicy": prac, "prace": prace, "materialy": materialy, "zdjecia": zdj,
                    "uwaga": "" if wsp else "Nie udało się ustalić położenia budowy – uzupełnij adres w danych umowy, aby pobierać pogodę."})


@bp.post("/api/projekty/<pid>/dziennik")
@S.wymaga_logowania
def dziennik_zapisz(pid):
    j = request.json
    try:
        dzien = dt.date.fromisoformat(j.get("data"))
    except (TypeError, ValueError):
        return jsonify({"blad": "Podaj datę wpisu."}), 400
    if dzien > dt.date.today() and not j.get("usun"):
        return jsonify({"blad": "Raport dzienny dotyczy dnia, który już trwa albo minął – nie można wpisać go z wyprzedzeniem."}), 400
    teraz, kto = dt.datetime.now().strftime("%Y-%m-%d %H:%M"), session.get("login", "")
    with S.BLOKADA:
        r = realizacja_pelna(pid)
        stary = next((x for x in r["dziennik"] if x["data"] == dzien.isoformat()), None)
        # wpisy dziennika nie znikają bez śladu (zasada dziennika budowy: wpisów się nie usuwa, zmiany są widoczne) –
        # poprzednia wersja i usunięty wpis trafiają do historii realizacji
        if stary and (j.get("usun") or any(str(stary.get(k) or "") != str(j.get(k, "") or "")[:3000] for k in POLA_DZIENNIKA)):
            r.setdefault("dziennik_historia", []).append(dict(stary, zastapiono=teraz, kto_zmienil=kto, powod="usunięty" if j.get("usun") else "zmieniony"))
        if j.get("usun"):
            r["dziennik"] = [w for w in r["dziennik"] if w["data"] != dzien.isoformat()]
        else:
            w = {"data": dzien.isoformat(), "autor": (stary or {}).get("autor") or kto, "zapisano": teraz,
                 "zdjecia": [z for z in j.get("zdjecia", []) if isinstance(z, str)][:20]}
            if stary and stary.get("autor") and stary.get("autor") != kto:
                w["zmienil"] = kto
            for k in POLA_DZIENNIKA:
                w[k] = str(j.get(k, ""))[:3000]
            w["wersja"] = sum(1 for h in r.get("dziennik_historia") or [] if h.get("data") == w["data"]) + 1
            r["dziennik"] = [x for x in r["dziennik"] if x["data"] != w["data"]] + [w]
            r["dziennik"].sort(key=lambda x: x["data"])
        S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


POLA_DZIENNIKA = ("pogoda", "pracownicy", "prace", "materialy", "sprzet", "uwagi")


@bp.get("/api/projekty/<pid>/dziennik.docx")
@S.wymaga_logowania
def dziennik_docx(pid):
    r = realizacja_pelna(pid)
    od, do = request.args.get("od", "0000"), request.args.get("do", "9999")
    wpisy = [w for w in r["dziennik"] if od <= w["data"] <= do]
    if not wpisy:
        abort(404)
    kat = os.path.join(S.pdir(pid), "realizacja")
    os.makedirs(kat, exist_ok=True)
    p = os.path.join(kat, f"Raporty_dzienne_{S.MO.bezpieczna_nazwa(S.meta(pid).get('nazwa', 'budowa'))[:50]}.docx")
    S.BUD.dziennik_docx(p, S.meta(pid).get("nazwa", ""), r, wpisy, S.folder_zdjec(pid), S.cfg())
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))
