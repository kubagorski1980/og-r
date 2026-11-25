# -*- coding: utf-8 -*-
"""
Finansowanie inwestycji (bank, BGK, KPO, dotacje) – trasy: źródła finansowania, pliki, odczyt umowy (AI), porównanie z umową wykonawcy (AI), raport.
Blueprint „finansowanie” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("finansowanie", __name__)


def _fin(pid):
    r = S.realizacja_dane(pid)
    F = r.get("finansowanie") if isinstance(r.get("finansowanie"), dict) else {}
    F.setdefault("zrodla", [])
    return r, F


def _zmiana(F):
    """Licznik zmian finansowania – kreator rozpoznaje, czy dokumenty przygotowano po ostatniej zmianie (licznik, nie czas: zmiany w tej samej minucie)."""
    F["nr"] = int(F.get("nr") or 0) + 1


def _jst(pid):
    """Zamawiający publiczny (nie wspólnota / spółdzielnia / deweloper) – przy kredycie i pożyczce ostrzeżenie z art. 243 ufp (H3-04)."""
    m = S.meta(pid)
    return (m.get("strona") or S.strona_typu(m.get("typ") or "przetarg")) == "zamawiajacy" and not S.projekt_wspolnoty(m)


def _fin_stan(pid):
    r, F = _fin(pid)
    kat = os.path.join(S.pdir(pid), "finansowanie")
    for z in F["zrodla"]:
        d = os.path.join(kat, z["id"])
        z["pliki"] = sorted(os.listdir(d)) if os.path.isdir(d) else []
    wk, ostrz = S.FIN.wklad_inwestycji(F)
    return {"zrodla": F["zrodla"], "typy": S.FIN.TYPY, "statusy": S.FIN.STATUSY,
            "wklad_wlasny": wk, "wklad_wlasny_migracja": ostrz, "jst": _jst(pid),
            "kontrole": ([{"kolor": "zolty", "obszar": "Wkład własny", "opis": ostrz}] if ostrz else [])
            + S.FIN.porownaj_rachunkowo(F["zrodla"], r, wklad=wk, jst=_jst(pid)),
            "przeplywy": S.FIN.przeplywy(F["zrodla"], r), "porownanie": F.get("porownanie") or [], "porownanie_data": F.get("porownanie_data") or "",
            "termin_wykonawcy": (S.FIN.termin_wykonawcy(r) or "") and S.FIN.termin_wykonawcy(r).isoformat(),
            "nr": int(F.get("nr") or 0), "harmonogram": S.FIN.harmonogram_szkic(F["zrodla"])}


@bp.get("/api/projekty/<pid>/finansowanie")
@S.wymaga_logowania
def fin_pobierz(pid):
    return jsonify(_fin_stan(pid))


@bp.post("/api/projekty/<pid>/finansowanie/zrodlo")
@S.wymaga_logowania
def fin_zrodlo(pid):
    """Dodanie, zmiana albo usunięcie źródła finansowania; ręczna poprawka odczytanych danych (terminy, kwoty)."""
    j = request.json or {}
    W_ = j.get("wymagania") if isinstance(j.get("wymagania"), dict) else {}
    for k in ("kwota", "wklad_wlasny"):  # GC-06: ręczna poprawka sprawdzana przed zapisem (wcześniej „abc” i 31.02 zapisywane bez słowa)
        if str(W_.get(k) or "").strip():
            v = S.FIN.liczba(re.sub(r"(?i)\s*(zł|pln)\.?$", "", str(W_[k]).strip()), None)
            if v is None or v != v or v < 0 or v > 1e12:
                return jsonify({"blad": f"{ {'kwota': 'Kwota finansowania', 'wklad_wlasny': 'Wkład własny'}[k]}: podaj kwotę w złotych, np. 1 250 000,00."}), 400
    for k in ("termin_zakonczenia_realizacji", "okres_kwalifikowalnosci_od", "okres_kwalifikowalnosci_do"):
        if str(W_.get(k) or "").strip() and not S.FIN.data_scisla(W_[k]):
            return jsonify({"blad": f"Nieprawidłowa data: „{str(W_[k])[:20]}” – podaj istniejącą datę RRRR-MM-DD albo DD.MM.RRRR."}), 400
    od_, do_ = S.FIN.data_scisla(W_.get("okres_kwalifikowalnosci_od")), S.FIN.data_scisla(W_.get("okres_kwalifikowalnosci_do"))
    if od_ and do_ and do_ < od_:
        return jsonify({"blad": "Okres kwalifikowalności: data „do” jest wcześniejsza niż „od”."}), 400
    with S.BLOKADA:
        r, F = _fin(pid)
        S.FIN.migruj_wklad(F)  # H3-04: jedno pole wkładu własnego inwestycji (stare wkłady przy źródłach – suma do sprawdzenia)
        z = next((x for x in F["zrodla"] if x["id"] == j.get("id")), None)
        if j.get("id") and not z:  # GC-06: usunięcie / zmiana nieistniejącego źródła nie tworzy nowego „kredytu bankowego”
            return jsonify({"blad": "Nie ma takiego źródła finansowania – odśwież stronę."}), 404
        if j.get("usun"):
            if not z:
                return jsonify({"blad": "Nie ma takiego źródła finansowania – odśwież stronę."}), 404
            F["zrodla"].remove(z)
            S.shutil.rmtree(os.path.join(S.pdir(pid), "finansowanie", z["id"]), ignore_errors=True)
        else:
            if not z:
                z = {"id": uuid.uuid4().hex[:8], "typ": "kredyt", "instytucja": "", "wymagania": {}}
                F["zrodla"].append(z)
            if j.get("typ") in S.FIN.TYPY:
                z["typ"] = j["typ"]
            if "instytucja" in j:
                z["instytucja"] = str(j["instytucja"] or "")[:200]
            for k in ("kwota", "wklad_wlasny", "termin_zakonczenia_realizacji", "termin_rozliczenia", "okres_kwalifikowalnosci_od", "okres_kwalifikowalnosci_do"):
                if k in (j.get("wymagania") or {}):
                    v_ = str(j["wymagania"][k] or "").strip()[:100]
                    d_ = S.FIN.data_scisla(v_) if k not in ("kwota", "wklad_wlasny", "termin_rozliczenia") else None
                    z.setdefault("wymagania", {})[k] = d_.isoformat() if d_ else v_
                    z.setdefault("reczne", {})[k] = z["wymagania"][k]  # poprawka ręczna – ma pierwszeństwo przed ponownym odczytem AI
        _zmiana(F)
        r["finansowanie"] = F
        S.zapisz_realizacje(pid, r)
    return jsonify(_fin_stan(pid))


@bp.post("/api/projekty/<pid>/finansowanie/wklad")
@S.wymaga_logowania
def fin_wklad(pid):
    """H3-04: wkład własny inwestycji – jedno pole dla wszystkich źródeł (zapis zatwierdza też kwotę przeniesioną ze starych danych)."""
    j = request.json or {}
    t = re.sub(r"(?i)\s*(zł|pln)\.?$", "", str(j.get("wklad_wlasny") if j.get("wklad_wlasny") is not None else "").strip())
    v = S.FIN.liczba(t, None) if t else 0.0
    if v is None or v != v or v < 0 or v > 1e12:
        return jsonify({"blad": "Wkład własny: podaj kwotę w złotych, np. 250 000,00."}), 400
    with S.BLOKADA:
        r, F = _fin(pid)
        F["wklad_wlasny"] = round(v, 2)
        F.pop("wklad_wlasny_migracja", None)
        _zmiana(F)
        r["finansowanie"] = F
        S.zapisz_realizacje(pid, r)
    return jsonify(_fin_stan(pid))


@bp.post("/api/projekty/<pid>/finansowanie/<zid>/pliki")
@S.wymaga_logowania
def fin_pliki(pid, zid):
    if not any(x.get("id") == zid for x in _fin(pid)[1]["zrodla"]):  # GC-06: pliki tylko do istniejącego źródła
        return jsonify({"blad": "Nie ma takiego źródła finansowania – odśwież stronę."}), 404
    d = os.path.join(S.pdir(pid), "finansowanie", re.sub(r"[^\w]", "", zid))
    os.makedirs(d, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(d, S.secure_filename_pl(f.filename)))
    with S.BLOKADA:
        r, F = _fin(pid)
        _zmiana(F)
        r["finansowanie"] = F
        S.zapisz_realizacje(pid, r)
    return jsonify(_fin_stan(pid))


def praca_fin_odczyt(log, pid, zid):
    """Wymagania z umowy finansowania (AI, z cytatami) – terminy, transze, koszty kwalifikowalne, wymagania wobec umowy z wykonawcą."""
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    r, F = _fin(pid)
    z = next((x for x in F["zrodla"] if x["id"] == zid), None)
    if not z:
        raise ValueError("Nie ma takiego źródła finansowania.")
    bloki = S._bloki_z(os.path.join(S.pdir(pid), "finansowanie", zid))
    if not bloki:
        raise ValueError("Wgraj umowę finansowania (i załączniki: harmonogram, wniosek, audyt).")
    log(f"AI czyta umowę finansowania ({S.FIN.TYPY.get(z['typ'])}) – terminy, transze, koszty kwalifikowalne, wymagania wobec umowy z wykonawcą…")
    txt, _ = S.MO.claude_stream(c, S.FIN.SYSTEM, S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": S.FIN.polecenie_wymagan(z["typ"])}],
                              max_tokens=8000, log=log)
    W = S.MO.wyciagnij_json(txt)
    if not isinstance(W, dict):
        raise ValueError("Nie udało się odczytać umowy finansowania – sprawdź, czy wgrany plik zawiera tekst.")
    for k in ("transze", "wymagania_umowy_wykonawczej", "dokumenty_rozliczenia", "wskazniki"):
        W[k] = [x for x in (W.get(k) or []) if isinstance(x, dict)]
    for k in ("data_umowy", "termin_zakonczenia_realizacji", "okres_kwalifikowalnosci_od", "okres_kwalifikowalnosci_do"):  # daty AI w RRRR-MM-DD – pola daty
        d_ = S.FIN.data_scisla(W.get(k))  # na ekranie ich nie gubią przy „Zapisz dane” (GC-06)
        if d_:
            W[k] = d_.isoformat()
    with S.BLOKADA:
        r, F = _fin(pid)
        z = next((x for x in F["zrodla"] if x["id"] == zid), None)
        z["wymagania"], z["odczytano"] = {**W, **{k: v for k, v in (z.get("reczne") or {}).items() if v}}, dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        if not z.get("instytucja"):
            z["instytucja"] = str(W.get("instytucja") or "")[:200]
        _zmiana(F)
        r["finansowanie"] = F
        S.zapisz_realizacje(pid, r)
    log(f"Gotowe: {len(W['transze'])} transz, {len(W['wymagania_umowy_wykonawczej'])} wymagań wobec umowy z wykonawcą, "
        f"termin zakończenia realizacji: {W.get('termin_zakonczenia_realizacji') or 'nie odczytano'}.")


def praca_fin_porownanie(log, pid):
    """Wymagania umów finansowania a umowa z wykonawcą (podpisana w realizacji albo wzór z kreatora) – status i propozycje do aneksu."""
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    r, F = _fin(pid)
    wym = [dict(w, zrodlo=z.get("instytucja") or S.FIN.TYPY.get(z["typ"])) for z in F["zrodla"] for w in ((z.get("wymagania") or {}).get("wymagania_umowy_wykonawczej") or [])]
    if not wym:
        raise ValueError("Najpierw odczytaj umowę finansowania – brak wymagań wobec umowy z wykonawcą.")
    bloki = S._bloki_z(os.path.join(S.pdir(pid), "realizacja", "dokumenty"))
    zrodlo = "umowa z wykonawcą z realizacji"
    if not bloki:
        bloki = [b for b in S._bloki_z(os.path.join(S.pdir(pid), "dokumenty_postepowania")) if re.search(r"umow", json.dumps(b, ensure_ascii=False)[:400], re.I)] \
            or S._bloki_z(os.path.join(S.pdir(pid), "dokumenty_postepowania"))
        zrodlo = "wzór umowy z kreatora"
    if not bloki:
        raise ValueError("Wgraj podpisaną umowę z wykonawcą w realizacji (Dokumenty budowy) – albo przygotuj wzór umowy w kreatorze.")
    log(f"AI porównuje {len(wym)} wymagań z umową z wykonawcą ({zrodlo})…")
    tresc = [{"type": "text", "text": "=== UMOWA WYKONAWCZA (umowa z wykonawcą) ==="}] + S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + \
            [{"type": "text", "text": S.FIN.polecenie_porownania(wym)}]
    txt, _ = S.MO.claude_stream(c, S.FIN.SYSTEM, tresc, max_tokens=8000, log=log)
    try:
        L = json.loads(txt[txt.index("["):txt.rindex("]") + 1])
    except ValueError:
        L = []
    wyn = []
    for i, w in enumerate(wym):
        x = next((y for y in L if isinstance(y, dict) and y.get("nr") == i), {}) or {}
        wyn.append({"wymog": w.get("wymog"), "zrodlo": w.get("zrodlo"), "cytat_finansowania": w.get("cytat") or "",
                    "status": x.get("status") if x.get("status") in S.FIN.STATUSY else "do_sprawdzenia", "cytat_umowy": str(x.get("cytat_umowy") or "")[:600],
                    "komentarz": str(x.get("komentarz") or "")[:500], "propozycja_aneksu": str(x.get("propozycja_aneksu") or "")[:1500]})
    with S.BLOKADA:
        r, F = _fin(pid)
        F["porownanie"], F["porownanie_data"], F["porownanie_zrodlo"] = wyn, dt.datetime.now().strftime("%Y-%m-%d %H:%M"), zrodlo
        r["finansowanie"] = F
        S.zapisz_realizacje(pid, r)
    n = sum(1 for w in wyn if w["status"] in ("rozbiezne", "brak"))
    log(f"Gotowe: {len(wyn)} wymagań – rozbieżności i braki: {n}.")


@bp.post("/api/projekty/<pid>/finansowanie/<zid>/odczyt")
@S.wymaga_logowania
def fin_odczyt(pid, zid):
    return jsonify(S.uruchom("zamawiajacy", "Odczyt umowy finansowania", praca_fin_odczyt, pid, zid))


@bp.post("/api/projekty/<pid>/finansowanie/porownanie")
@S.wymaga_logowania
def fin_porownanie(pid):
    return jsonify(S.uruchom("zamawiajacy", "Umowa finansowania a umowa z wykonawcą", praca_fin_porownanie, pid))


@bp.get("/api/projekty/<pid>/finansowanie/raport.docx")
@S.wymaga_logowania
def fin_raport(pid):
    r, F = _fin(pid)
    st = _fin_stan(pid)
    kat = os.path.join(S.pdir(pid), "finansowanie")
    os.makedirs(kat, exist_ok=True)
    sc = os.path.join(kat, f"Finansowanie_zgodnosc_{dt.date.today():%Y%m%d}.docx")
    S.FIN.raport_docx(sc, S.meta(pid).get("nazwa") or "", F["zrodla"], r, st["kontrole"], st["przeplywy"], st["porownanie"])
    return send_file(sc, as_attachment=True)
