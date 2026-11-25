# -*- coding: utf-8 -*-
"""
Dotacje – trasy: wyszukiwanie i harmonogram naborów, alerty, projekty dotacyjne (analiza, przygotowanie, sprawdzenie – AI), wniosek o dotację, zapytania ofertowe w projektach dotacyjnych (dokumenty, ocena, protokół, rozliczenie), współczynniki SO.
Blueprint „dotacje” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, has_request_context, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("dotacje", __name__)


def _dot(m, faza="rozliczenie"):
    return m.setdefault(S.FAZY[faza]["klucz"], {"dane": {}, "wymagania": None, "zakres": "", "dokumenty": {}})


def _dotacja(m):
    return _dot(m, "rozliczenie")


def dot_dane_impl(pid, faza):
    j = request.json or {}
    m = S.meta(pid)
    t = _dot(m, faza)
    pola = ("program", "nr_umowy", "kwota", "beneficjent", "opis") if faza == "rozliczenie" else \
        ("opis_projektu", "kwota_wnioskowana", "koszt_calkowity", "okres_realizacji", "lokalizacja", "uwagi")
    t["dane"] = {**(t.get("dane") or {}), **{k: str(j.get(k) or "")[:3000] for k in pola if k in j}}
    if "zakres" in j and faza == "rozliczenie":
        t["zakres"] = str(j["zakres"] or "calosc")[:40]
    S.zapisz_meta(pid, m)
    return jsonify(t)


def praca_dot_analiza(log, pid, faza):
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    bloki, n = S.bloki_dotacji(pid, log)
    t = _dot(S.meta(pid), faza)
    if not n:
        raise ValueError("Wgraj w punkcie 1 dokumenty dotacji: umowę o dofinansowanie (objęcie wsparciem), wniosek, regulamin naboru."
                         if faza == "rozliczenie" else "W punkcie 1 pobierz dokumenty naboru (regulamin, wzór wniosku, załączniki) albo wgraj je.")
    if faza == "wniosek":
        log(f"AI analizuje {n} dokumentów naboru – kryteria, koszty kwalifikowalne, wymagane dokumenty wniosku…")
        polecenie = S.DOT.polecenie_analizy_wniosku({**(t.get("dane") or {}), "wnioskodawca": S._dane_wnioskodawcy()}, t.get("nabor") or {})
        kategorie = S.DOT.KATEGORIE_W
    else:
        log(f"AI analizuje {n} dokumentów dotacji – ustala etapy, wskaźniki i dokumenty potrzebne do rozliczenia…")
        polecenie = S.DOT.polecenie_analizy(t.get("dane") or {})
        kategorie = S.DOT.KATEGORIE
    tresc = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polecenie}]
    txt, _ = S.MO.claude_stream(c, S.DOT.SYSTEM, tresc, max_tokens=16000, log=log)
    w = S.MO.wyciagnij_json(txt)
    if not isinstance(w, dict):
        w = {"dokumenty": w if isinstance(w, list) else []}
    w["dokumenty"] = S._lista_slownikow(w.get("dokumenty"))
    w["etapy"] = S._lista_slownikow(w.get("etapy"))
    w["wskazniki"] = S._lista_slownikow(w.get("wskazniki"))
    w["kryteria_oceny"] = S._lista_slownikow(w.get("kryteria_oceny"))
    for k_ in ("kryteria_dostepu", "koszty_kwalifikowalne", "ryzyka", "uwagi", "terminy"):
        w[k_] = [x if isinstance(x, str) else (x.get("nazwa") or x.get("opis") or json.dumps(x, ensure_ascii=False)) for x in (w.get(k_) or [])
                 if isinstance(x, (str, dict))]
    if not w.get("dokumenty"):
        raise ValueError("Nie udało się ustalić listy dokumentów – sprawdź wgrane dokumenty i spróbuj ponownie.")
    for i, d_ in enumerate(w["dokumenty"], 1):
        d_["id"] = S.DOT.bezpieczna(d_.get("id") or f"d{i}")
        if d_.get("kategoria") not in kategorie:
            d_["kategoria"] = "Inne"
    for i, e in enumerate(w.get("etapy") or [], 1):
        e["id"] = S.DOT.bezpieczna(e.get("id") or f"e{i}")
    m = S.meta(pid)
    _dot(m, faza)["wymagania"] = w
    S.zapisz_meta(pid, m)
    log(f"Gotowe: {len(w['dokumenty'])} rodzajów dokumentów" + (f", {len(w.get('etapy') or [])} etapów." if faza == "rozliczenie" else "."))
    return {"dokumenty": len(w["dokumenty"])}


def praca_dotacja_analiza(log, pid):
    return praca_dot_analiza(log, pid, "rozliczenie")


def dot_stan_impl(pid, faza):
    m = S.meta(pid)
    t = _dot(m, faza)
    z = S._zakres(m, faza)
    lista = []
    for d_ in S.dokumenty_zakresu(m, z, faza):
        st = (t.get("dokumenty") or {}).get(f"{S.zakres_klucz(z)}/{d_['id']}", {})
        lista.append({**d_, "pliki": S.pliki_dok(pid, z, d_["id"], faza), "stan": st.get("stan", ""), "uwagi_spr": st.get("uwagi", ""),
                      "przygotowany": st.get("przygotowany")})
    return jsonify({"faza": faza, "folder": S.FAZY[faza]["folder"], "dane": t.get("dane"), "nabor": t.get("nabor"), "wymagania": t.get("wymagania"),
                    "zakres": z, "zakres_opis": S.zakres_opis(m, z, faza), "lista": lista,
                    "sprawdzenie": (t.get("sprawdzenia") or {}).get(S.zakres_klucz(z)), "komplet": (t.get("komplety") or {}).get(S.zakres_klucz(z)),
                    "programy": S.DOT.PROGRAMY, "wnioskodawca": S._dane_wnioskodawcy() if faza == "wniosek" else None})


def dot_plik_impl(pid, faza):
    m = S.meta(pid)
    z = S._zakres(m, faza)
    did = S.DOT.bezpieczna(request.form.get("dok", ""))
    if not any(d_["id"] == did for d_ in S.dokumenty_zakresu(m, z, faza)):
        return jsonify({"blad": "Nie ma takiego dokumentu w wykazie."}), 400
    kat = S.kat_dok(pid, z, did, faza)
    os.makedirs(kat, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(kat, S.secure_filename_pl(f.filename)))
    st = _dot(m, faza).setdefault("dokumenty", {}).setdefault(f"{S.zakres_klucz(z)}/{did}", {})
    st["stan"] = "wgrany"
    S.zapisz_meta(pid, m)
    return jsonify({"pliki": S.pliki_dok(pid, z, did, faza)})


def dot_plik_usun_impl(pid, faza):
    j = request.json or {}
    m = S.meta(pid)
    z = S._zakres(m, faza)
    p = os.path.join(S.kat_dok(pid, z, j.get("dok", ""), faza), os.path.basename(str(j.get("plik", ""))))
    if os.path.isfile(p):
        arch = os.path.join(S.pdir(pid), S.FAZY[faza]["folder"], "_archiwum")
        os.makedirs(arch, exist_ok=True)
        S.shutil.move(p, os.path.join(arch, f"{dt.datetime.now():%Y%m%d%H%M%S}_{os.path.basename(p)}"))
    return jsonify({"ok": True})


def praca_dot_przygotuj(log, pid, did, faza):
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    m = S.meta(pid)
    t = _dot(m, faza)
    z = S._zakres(m, faza)
    dok = next((d_ for d_ in S.dokumenty_zakresu(m, z, faza) if d_["id"] == did), None)
    if not dok:
        raise ValueError("Nie ma takiego dokumentu w wykazie.")
    bloki, _ = S.bloki_dotacji(pid, log, limit=300_000)
    b2, _ = S.bloki_rozliczenia(pid, z, faza)
    wgrane = [f"{d_['nazwa']}: {', '.join(S.pliki_dok(pid, z, d_['id'], faza))}" for d_ in S.dokumenty_zakresu(m, z, faza) if S.pliki_dok(pid, z, d_["id"], faza)]
    dane = dict(t.get("dane") or {})
    if faza == "wniosek":
        dane.update(wnioskodawca=S._dane_wnioskodawcy(), nabor=t.get("nabor") or {})
        st_ = S._plan_stan(pid, m)
        if (st_["plan"].get("pozycje") or []):  # zakres, budżet, wskaźniki i harmonogram z planu projektu – wniosek wypełnia się z nich
            dane["plan_projektu"] = S.DP.opis_planu(st_["plan"], st_["wskazniki"], st_["budzet"], st_["harmonogram"])
            dane["profil_wnioskodawcy"] = S.cfg().get("dotacje_profil") or {}
    log(f"AI przygotowuje: {dok['nazwa']} ({S.zakres_opis(m, z, faza)})…")
    tresc = S.MO.oznacz_dokumenty(bloki + b2, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": S.DOT.polecenie_dokumentu(
        dok, S.zakres_opis(m, z, faza), dane, t.get("wymagania") or {}, wgrane)}]
    txt, _ = S.MO.claude_stream(c, S.DOT.SYSTEM, tresc, max_tokens=16000, log=log)
    d_ = S.MO.wyciagnij_json(txt)
    if not isinstance(d_, dict):
        d_ = {"tytul": dok["nazwa"], "rozdzialy": [{"tytul": "", "akapity": [str(x) for x in (d_ if isinstance(d_, list) else [d_])]}]}
    d_["rozdzialy"] = [r_ if isinstance(r_, dict) else {"tytul": "", "akapity": [str(r_)]} for r_ in (d_.get("rozdzialy") or [])]
    kat = S.kat_dok(pid, z, did, faza)
    os.makedirs(kat, exist_ok=True)
    nazwa = f"{S.DOT.bezpieczna(dok['nazwa'])}_przygotowany.docx"
    wym = t.get("wymagania") or {}
    S.DOT.zapisz_dokument(os.path.join(kat, nazwa), d_, f"{S.cfg().get('firma_nazwa', '')} · {wym.get('projekt') or m.get('nazwa', '')}"
                        + (f" · umowa {wym['nr_umowy']}" if wym.get("nr_umowy") else ""))
    m = S.meta(pid)
    st = _dot(m, faza).setdefault("dokumenty", {}).setdefault(f"{S.zakres_klucz(z)}/{did}", {})
    st.update(stan="przygotowany – do sprawdzenia", przygotowany=nazwa)
    S.zapisz_meta(pid, m)
    log(f"Gotowe: {nazwa}" + (f" · do uzupełnienia: {len(d_.get('do_uzupelnienia') or [])} pkt" if d_.get("do_uzupelnienia") else ""))
    return {"plik": nazwa}


def praca_dotacja_przygotuj(log, pid, did):
    return praca_dot_przygotuj(log, pid, did, "rozliczenie")


def praca_dot_sprawdz(log, pid, faza):
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    m = S.meta(pid)
    t = _dot(m, faza)
    z = S._zakres(m, faza)
    b2, n2 = S.bloki_rozliczenia(pid, z, faza)
    if not n2:
        raise ValueError("Wgraj albo przygotuj dokumenty (punkt 3), a potem uruchom sprawdzenie.")
    bloki, _ = S.bloki_dotacji(pid, log, limit=250_000)
    lista = [{"id": d_["id"], "nazwa": d_["nazwa"], "pliki": S.pliki_dok(pid, z, d_["id"], faza)} for d_ in S.dokumenty_zakresu(m, z, faza)]
    log(f"AI sprawdza {n2} plików ({S.zakres_opis(m, z, faza)})…")
    c["_model"] = c.get("model_dokladny") or "claude-opus-5-5"
    pol = S.DOT.polecenie_sprawdzenia_wniosku(t.get("wymagania") or {}, lista) if faza == "wniosek" else \
        S.DOT.polecenie_sprawdzenia(S.zakres_opis(m, z, faza), t.get("wymagania") or {}, lista)
    tresc = S.MO.oznacz_dokumenty(bloki + b2, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": pol}]
    txt, _ = S.MO.claude_stream(c, S.DOT.SYSTEM, tresc, max_tokens=12000, log=log)
    w = S.MO.wyciagnij_json(txt)
    if not isinstance(w, dict):
        w = {"ocena": "", "podsumowanie": str(w)[:2000]}
    w["dokumenty"] = S._lista_slownikow(w.get("dokumenty"), "id")
    w["uwagi"] = S._lista_slownikow(w.get("uwagi"), "opis")
    kat = os.path.join(S.pdir(pid), S.FAZY[faza]["folder"], S.zakres_klucz(z))
    os.makedirs(kat, exist_ok=True)
    S.DOT.raport_docx(os.path.join(kat, "Raport_sprawdzenia.docx"), w, S.zakres_opis(m, z, faza), t.get("wymagania") or {})
    m = S.meta(pid)
    t = _dot(m, faza)
    for d_ in w.get("dokumenty") or []:
        st = t.setdefault("dokumenty", {}).setdefault(f"{S.zakres_klucz(z)}/{S.DOT.bezpieczna(d_.get('id', ''))}", {})
        st.update(stan=d_.get("stan", ""), uwagi=d_.get("uwagi", ""))
    t.setdefault("sprawdzenia", {})[S.zakres_klucz(z)] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "ocena": w.get("ocena", ""),
                                                        "podsumowanie": w.get("podsumowanie", ""), "uwagi": w.get("uwagi") or []}
    S.zapisz_meta(pid, m)
    log(f"Ocena: {w.get('ocena', '')} · uwag: {len(w.get('uwagi') or [])}")
    return {"ocena": w.get("ocena")}


def praca_dotacja_sprawdz(log, pid):
    return praca_dot_sprawdz(log, pid, "rozliczenie")


def dot_komplet_impl(pid, faza):
    import zipfile
    m = S.meta(pid)
    t = _dot(m, faza)
    z = S._zakres(m, faza)
    kategorie = S.DOT.KATEGORIE_W if faza == "wniosek" else S.DOT.KATEGORIE
    poz = []
    kat = os.path.join(S.pdir(pid), S.FAZY[faza]["folder"], S.zakres_klucz(z))
    for d_ in S.dokumenty_zakresu(m, z, faza):
        st = (t.get("dokumenty") or {}).get(f"{S.zakres_klucz(z)}/{d_['id']}", {})
        pl = S.pliki_dok(pid, z, d_["id"], faza)
        poz.append({"id": d_["id"], "nazwa": d_["nazwa"], "kategoria": d_.get("kategoria", "Inne"), "pliki": pl, "stan": st.get("stan") or ("brak" if not pl else "wgrany")})
    if not any(p["pliki"] for p in poz):
        return jsonify({"blad": "Brak dokumentów do spakowania – wgraj lub przygotuj dokumenty w punkcie 3."}), 400
    os.makedirs(kat, exist_ok=True)
    S.DOT.spis_docx(os.path.join(kat, "Spis_zalacznikow.docx"), poz, S.zakres_opis(m, z, faza), t.get("wymagania") or {})
    nazwa = (f"Komplet_wniosku_o_dofinansowanie_{dt.date.today():%Y-%m-%d}.zip" if faza == "wniosek"
             else f"Komplet_rozliczenia_{S.zakres_klucz(z)}_{dt.date.today():%Y-%m-%d}.zip")
    with zipfile.ZipFile(os.path.join(S.pdir(pid), nazwa), "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(kat, "Spis_zalacznikow.docx"), "00_Spis_zalacznikow.docx")
        if os.path.isfile(os.path.join(kat, "Raport_sprawdzenia.docx")):
            zf.write(os.path.join(kat, "Raport_sprawdzenia.docx"), "00_Raport_sprawdzenia_(do_uzytku_wewnetrznego).docx")
        for p in poz:
            nr = kategorie.index(p["kategoria"]) + 1 if p["kategoria"] in kategorie else 9
            for f in p["pliki"]:
                zf.write(os.path.join(kat, p["id"], f), f"{nr:02d}_{S.DOT.bezpieczna(p['kategoria'])}/{S.DOT.bezpieczna(p['nazwa'])}/{f}")
    t.setdefault("komplety", {})[S.zakres_klucz(z)] = {"plik": nazwa, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                     "brakuje": [p["nazwa"] for p in poz if not p["pliki"]]}
    S.zapisz_meta(pid, m)
    return jsonify({"url": f"/pobierz/{pid}/{S.urllib.parse.quote(nazwa)}", "brakuje": t["komplety"][S.zakres_klucz(z)]["brakuje"]})


@bp.post("/api/dotacje/z-linku")
@S.wymaga_logowania
def dotacje_z_linku():
    url = str((request.json or {}).get("url") or "").strip()
    if not re.match(r"https?://", url):
        return jsonify({"blad": "Wklej pełny adres strony naboru (zaczynający się od https://)."}), 400
    return jsonify(S.uruchom("dotacje_szukaj", "Odczyt naboru z linku", S.praca_nabor_z_linku, url))


@bp.post("/api/dotacje/szukaj")
@S.wymaga_logowania
def dotacje_szukaj():
    j = request.json or {}
    k = {x: str(j.get(x) or "")[:200] for x in ("branza", "region", "wnioskodawca", "slowa")}
    k["pomysl"] = str(j.get("pomysl") or "")[:600]  # wyszukiwanie odwrotne: od pomysłu do naborów
    k["odswiez"] = bool(j.get("odswiez"))
    return jsonify(S.uruchom("dotacje_szukaj", "Wyszukiwanie dotacji", S.praca_szukaj_dotacji, k))


@bp.get("/api/dotacje/wyniki")
@S.wymaga_logowania
def dotacje_wyniki():
    return jsonify({**(S.czytaj(S.F_DOT_SZUKAJ, {}) or {}), "branze": S.DOT.BRANZE, "wnioskodawcy": S.DOT.WNIOSKODAWCY})


@bp.get("/api/dotacje/harmonogram")
@S.wymaga_logowania
def dotacje_harmonogram():
    a = request.args
    f = {"region": a.get("region") or "", "branza": a.get("branza") or "", "wnioskodawca": a.get("wnioskodawca") or "", "slowa": a.get("slowa") or ""}
    H = S.harm_dane()
    zrodla = [{"klucz": k, **v} for k, v in (H.get("zrodla") or {}).items()]
    return jsonify({"nabory": S.nabory_harmonogramu(f, a.get("trwajace") == "1")[:300], "odswiezono": H.get("odswiezono", ""), "zrodla": zrodla,
                    "wlasne_zrodla": H.get("wlasne_zrodla") or [], "regiony": list(S.PORTALE_REGIONALNE.keys()), "branze": S.DOT.BRANZE,
                    "wnioskodawcy": S.DOT.WNIOSKODAWCY, "liczba_wszystkich": len(H.get("nabory") or [])})


@bp.post("/api/dotacje/harmonogram/odswiez")
@S.wymaga_logowania
def dotacje_harmonogram_odswiez():
    j = request.json or {}
    reg = [r for r in (j.get("regiony") or []) if isinstance(r, str)][:20] or None
    return jsonify(S.uruchom("dotacje_harm", "Odświeżanie harmonogramów naborów", S.praca_odswiez_harmonogramy, reg, bool(j.get("wymus"))))


@bp.post("/api/dotacje/harmonogram/zrodla")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel  # źródła harmonogramów są wspólne dla wszystkich kont (H1-01)
def dotacje_harmonogram_zrodla():
    """Własne źródła harmonogramów (np. strona instytucji pośredniczącej albo bezpośredni plik), przypisane do regionu."""
    j = request.json or {}
    with S.BLOKADA:
        H = S.harm_dane()
        L = H.get("wlasne_zrodla") or []
        if j.get("usun"):
            L = [z for z in L if z["url"] != j["usun"]]
        else:
            url = str(j.get("url") or "").strip()
            if not re.match(r"https?://", url):
                return jsonify({"blad": "Podaj pełny adres (https://…) strony z harmonogramem albo pliku."}), 400
            L.append({"region": str(j.get("region") or "cała Polska")[:40], "url": url, "nazwa": str(j.get("nazwa") or "")[:120]})
        H["wlasne_zrodla"] = L
        S.pisz(S.F_HARM, H)
    return jsonify({"wlasne_zrodla": L})


@bp.get("/api/dotacje/alerty")
@S.wymaga_logowania
def dotacje_alerty():
    A = S.alerty_dot()
    for a in A.get("alerty") or []:
        tr = S.nabory_harmonogramu(a, trwajace=False)
        a["trafienia"] = len(tr)
        a["nowe"] = [n["id"] for n in tr if n["id"] not in set((A.get("widziane") or {}).get(a["id"], []))]
    return jsonify(A)


@bp.post("/api/dotacje/alerty")
@S.wymaga_logowania
def dotacje_alerty_zapisz():
    j = request.json or {}
    with S.BLOKADA:
        A = S.alerty_dot()
        L = A.get("alerty") or []
        if j.get("usun"):
            L = [a for a in L if a["id"] != j["usun"]]
        elif j.get("widziane"):
            A.setdefault("widziane", {})[j["widziane"]] = [n["id"] for n in S.nabory_harmonogramu(next((a for a in L if a["id"] == j["widziane"]), {}))]
        else:
            a = {"id": S.DOT.bezpieczna(j.get("id") or uuid.uuid4().hex[:8]), "nazwa": str(j.get("nazwa") or "Mój alert")[:80],
                 "regiony": [r for r in (j.get("regiony") or []) if r in S.PORTALE_REGIONALNE or r == "cała Polska"],
                 "branze": [b for b in (j.get("branze") or []) if b in S.DOT.BRANZE], "wnioskodawcy": [w for w in (j.get("wnioskodawcy") or []) if w in S.DOT.WNIOSKODAWCY],
                 "slowa": str(j.get("slowa") or "")[:200], "dni_przed": max(0, min(90, int(j.get("dni_przed") or 14))), "email": bool(j.get("email", True)),
                 "utworzono": dt.date.today().isoformat()}
            L = [x for x in L if x["id"] != a["id"]] + [a]
            A.setdefault("widziane", {}).setdefault(a["id"], [n["id"] for n in S.nabory_harmonogramu(a)]) if j.get("bez_obecnych") else None
        A["alerty"] = L
        S.pisz(S.F_ALERTY_DOT, A)
    return jsonify({"ok": True})


@bp.get("/api/dotacje/so")
@S.wymaga_logowania
def so_dane():
    return jsonify({"regiony": S.DP.REGIONY_FADN, "uprawy": S.DP.SO_UPRAWY, "zwierzeta": S.DP.SO_ZWIERZETA,
                    "wspolczynniki": S.WSP.czytaj("so_wspolczynniki.json", {}), "dane": (S.cfg().get("dotacje_profil") or {}).get("so_dane") or {}})


@bp.post("/api/dotacje/so/wspolczynniki")
@S.wymaga_logowania
def so_wspolczynniki():
    j = request.json or {}
    region = j.get("region") if j.get("region") in S.DP.REGIONY_FADN else ""
    if not region:
        return jsonify({"blad": "Wybierz województwo."}), 400
    wersja = str(j.get("wersja") or "SO 2017")[:20]
    return jsonify(S.uruchom("dotacja", f"Współczynniki SO – {region}", S.praca_so_wspolczynniki, region, wersja))


@bp.post("/api/dotacje/so/oblicz")
@S.wymaga_logowania
def so_oblicz():
    """Wynik kalkulatora SO; zapis danych gospodarstwa i wyniku w profilu wnioskodawcy."""
    j = request.json or {}
    wsp = S.WSP.czytaj("so_wspolczynniki.json", {}).get(f"{j.get('region')}|{j.get('wersja') or 'SO 2017'}") or {}
    upr = [x for x in j.get("uprawy") or [] if isinstance(x, dict)][:60]
    zw = [x for x in j.get("zwierzeta") or [] if isinstance(x, dict)][:60]
    w = S.DP.oblicz_so(upr, zw, wsp)
    prof = dict(S.cfg().get("dotacje_profil") or {})
    prof["so_dane"] = {"region": j.get("region"), "wersja": j.get("wersja") or "SO 2017", "woj": j.get("woj"), "uprawy": upr, "zwierzeta": zw}
    if j.get("zapisz") and w["so"]:
        prof["wielkosc_ekonomiczna"] = str(round(w["so"]))
    S.zapisz_ustawienia({"dotacje_profil": prof})
    return jsonify(dict(w, zrodlo=wsp.get("zrodlo", ""), zrodlo_url=wsp.get("zrodlo_url", "")))


@bp.post("/api/dotacje/wniosek")
@S.wymaga_logowania
def dotacje_nowy_wniosek():
    """„Uzyskaj dotację”: nowy wniosek o dofinansowanie z naboru znalezionego w wyszukiwarce (albo pusty) i pobranie jego dokumentów."""
    j = request.json or {}
    wyn = (S.czytaj(S.F_DOT_SZUKAJ, {}) or {}).get("wyniki") or []
    nab = next((x for x in wyn if x.get("id") == j.get("nabor")), None) if j.get("nabor") else None
    if not nab and j.get("nabor"):
        nab = next((x for x in (S.pamiec_naborow().get("nabory") or {}).values() if x.get("id") == j.get("nabor")), None)
    if not nab and j.get("harmonogram"):  # wniosek z nadchodzącego naboru – dokumenty pojawią się po ogłoszeniu naboru
        h_ = next((x for x in S.harm_dane().get("nabory") or [] if x.get("id") == j["harmonogram"]), None)
        if h_:
            nab = {"id": h_["id"], "nazwa": h_.get("tytul"), "program": h_.get("program"), "instytucja": h_.get("instytucja"),
                   "dla_kogo": h_.get("wnioskodawcy_opis"), "kwota": h_.get("kwota"), "nabor_od": h_.get("data_od") or h_.get("termin_opis"),
                   "nabor_do": h_.get("data_do"), "status": "planowany", "opis": h_.get("typy_projektow"), "link": h_.get("zrodlo_url"), "dokumenty": []}
    pid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, pid, "dokumenty"))
    m = {"id": pid, "nazwa": str(j.get("nazwa") or (nab or {}).get("nazwa") or "Wniosek o dofinansowanie")[:120], "typ": "wniosek_dot", "strona": "dotacje",
         "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wlasciciel": S.konto_biezace(), "pominiete": [],
         "wniosek_dot": {"dane": {}, "wymagania": None, "dokumenty": {}, "nabor": nab,
                         "plan": {"pomysl": ((S.czytaj(S.F_DOT_SZUKAJ, {}) or {}).get("kryteria") or {}).get("pomysl", ""), "pozycje": []}}}
    S.zapisz_meta(pid, m)
    zid = S.uruchom("pobierz", "Pobieranie dokumentów naboru", S.praca_pobierz_dok_naboru, pid)["id"] if nab and (nab.get("dokumenty") or nab.get("link")) else None
    S.zapisz_aktywnosc(session.get("login"), "Nowy wniosek o dotację", konto=S.konto_biezace(), projekt=m["nazwa"])
    return jsonify({"id": pid, "zadanie": zid})


def _dotacja_dostepna(dot_id):
    """Projekt rozliczenia dotacji, do którego zalogowany ma dostęp – albo None (GC-07: bez cudzych projektów i ścieżek „../”)."""
    if not re.fullmatch(r"[0-9a-f]{12}", str(dot_id or "")):
        return None
    dm = S.czytaj(os.path.join(S.PROJ, dot_id, "projekt.json"), None)
    if not dm or dm.get("typ") != "dotacja":
        return None
    if has_request_context() and not S.ma_dostep(dm, session.get("login"), S.rola_sesji()):  # zadanie w tle – powiązanie sprawdzone przy zapisie
        return None
    return dm


def _dotacja_info(dot_id):
    dm = _dotacja_dostepna(dot_id)
    if not dm:
        return {}
    w = (dm.get("dotacja") or {}).get("wymagania") or {}
    return {"id": dot_id, "nazwa": dm.get("nazwa"), "program": w.get("program", ""), "nr_umowy": w.get("nr_umowy", "")}


def _zapytanie_stan(pid, m):
    Z = m.get("zapytanie") or {}
    d = Z.get("dane") or {}
    wym = S.ZQ.wymagania(d)
    kat = os.path.join(S.pdir(pid), "zapytanie")
    pliki = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
    oc = None
    if Z.get("ocena_id"):
        om = S.czytaj(os.path.join(S.PROJ, Z["ocena_id"], "projekt.json"), None)
        if om:
            O = S.ocena_dane(om)
            naj = next((o for o in O["oferty"] if o.get("id") == (O.get("podsum") or {}).get("najkorzystniejsza")), None)
            oc = {"id": Z["ocena_id"], "ofert": len(O["oferty"]), "najkorzystniejsza": (naj or {}).get("nazwa"), "punkty": (naj or {}).get("punkty")}
    pub = Z.get("publikacja") or {}
    auto = {"publikacja": bool(pub.get("numer") and pub.get("data")), "protokol": any(p.startswith("Protokol") for p in pliki),
            "termin": bool(pub.get("termin") and pub.get("data") and (dt.date.fromisoformat(pub["termin"][:10]) - dt.date.fromisoformat(pub["data"][:10])).days - 1 >= wym["min_dni"]) if pub.get("termin") and pub.get("data") else False,
            "powiazania": any(p.startswith("Oswiadczenie") for p in pliki), "wynik": bool(pub.get("wynik_data"))}
    lista = [{"id": k, "opis": o, "ok": bool((Z.get("lista") or {}).get(k) or auto.get(k))} for k, o in wym["lista"]]
    return {"projekt": {"id": pid, "nazwa": m.get("nazwa")}, "Z": Z, "wymagania": wym, "pliki": pliki, "ocena": oc, "lista": lista,
            "dotacja": _dotacja_info(Z.get("dotacja_id")),
            "dotacje": [{"id": p, "nazwa": x.get("nazwa")} for p in os.listdir(S.PROJ)
                        for x in [S.czytaj(os.path.join(S.PROJ, p, "projekt.json"), None)] if x and x.get("typ") == "dotacja" and not x.get("archiwum")
                        and S.ma_dostep(x, session.get("login"), S.rola_sesji(), lista=True)]}


@bp.get("/api/projekty/<pid>/zapytanie")
@S.wymaga_logowania
def zapytanie_pobierz(pid):
    return jsonify(_zapytanie_stan(pid, S.meta(pid)))


@bp.post("/api/projekty/<pid>/zapytanie")
@S.wymaga_logowania
def zapytanie_zapisz(pid):
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        Z = m.setdefault("zapytanie", {})
        for k in ("dane", "publikacja", "lista"):
            if isinstance(j.get(k), dict):
                Z.setdefault(k, {}).update({a: b for a, b in j[k].items() if isinstance(a, str)})
        if "dotacja_id" in j:
            stara, nowa = Z.get("dotacja_id"), str(j.get("dotacja_id") or "")
            if nowa and not _dotacja_dostepna(nowa):
                return jsonify({"blad": "Nie ma takiego projektu rozliczenia dotacji na Twoim koncie."}), 404
            for d_id, dodaj in ((stara, False), (nowa, True)):
                dm = _dotacja_dostepna(d_id) if d_id else None
                if dm:
                    L = [x for x in dm.get("zapytania", []) if x != pid] + ([pid] if dodaj else [])
                    dm["zapytania"] = L
                    S.zapisz_meta(d_id, dm)
            Z["dotacja_id"] = nowa
        if (Z.get("dane") or {}).get("przedmiot"):
            m["nazwa"] = Z["dane"]["przedmiot"][:90]
        S.zapisz_meta(pid, m)
    return jsonify(_zapytanie_stan(pid, S.meta(pid)))


def praca_zapytanie_dokumenty(log, pid):
    c = S.cfg()
    S.wymagany_klucz(c)
    m = S.meta(pid)
    Z = m.get("zapytanie") or {}
    d = dict(Z.get("dane") or {})
    dot = _dotacja_info(Z.get("dotacja_id"))
    bloki = []
    for katalog in [os.path.join(S.pdir(pid), "dokumenty")] + ([os.path.join(S.PROJ, Z["dotacja_id"], "dokumenty")] if dot else []):
        if os.path.isdir(katalog):
            bloki += S._bloki_z(katalog, limit=8)
    log(f"AI przygotowuje zapytanie ofertowe ({len(bloki)} dokumentów źródłowych: projekt dotacji i materiały zamówienia)…")
    tresc = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": S.ZQ.polecenie(d, dot)}]
    txt, _ = S.MO.claude_stream(c, S.ZQ.SYSTEM_ZAP, tresc, max_tokens=12000, log=log)
    z = S.MO.wyciagnij_json(txt)
    if not isinstance(z, dict) or not z.get("sekcje"):
        raise RuntimeError("AI nie zwróciło treści zapytania – spróbuj ponownie.")
    kat = os.path.join(S.pdir(pid), "zapytanie")
    os.makedirs(kat, exist_ok=True)
    S.ZQ.zapytanie_docx(os.path.join(kat, "Zapytanie_ofertowe.docx"), d, z)
    S.ZQ.formularz_docx(os.path.join(kat, "Formularz_ofertowy.docx"), d, z)
    S.ZQ.powiazania_docx(os.path.join(kat, "Oswiadczenie_o_braku_powiazan_wykonawca.docx"), d)
    S.ZQ.powiazania_docx(os.path.join(kat, "Oswiadczenie_o_braku_powiazan_komisja.docx"), d, dla_komisji=True)
    with S.BLOKADA:
        m = S.meta(pid)
        m.setdefault("zapytanie", {})["tresc"] = {k: z.get(k) for k in ("tytul", "kryteria", "warunki_udzialu", "wymagane_dokumenty", "ryzyka")}
        S.zapisz_meta(pid, m)
    log("Gotowe: zapytanie ofertowe, formularz ofertowy i oświadczenia o braku powiązań (Word).")
    return {"ok": True}


@bp.post("/api/projekty/<pid>/zapytanie/dokumenty")
@S.wymaga_logowania
def zapytanie_dokumenty(pid):
    S.meta(pid)
    return jsonify(S.uruchom("zapytanie", "Zapytanie ofertowe (zasada konkurencyjności)", praca_zapytanie_dokumenty, pid))


@bp.get("/api/projekty/<pid>/zapytanie/plik/<path:nazwa>")
@S.wymaga_logowania
def zapytanie_plik(pid, nazwa):
    S.meta(pid)
    kat = os.path.join(S.pdir(pid), "zapytanie")
    p = os.path.normpath(os.path.join(kat, nazwa))
    if not p.startswith(os.path.normpath(kat)) or not os.path.isfile(p):
        return jsonify({"blad": "Nie znaleziono pliku."}), 404
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


@bp.post("/api/projekty/<pid>/zapytanie/ocena")
@S.wymaga_logowania
def zapytanie_ocena(pid):
    """Sprawdzenie złożonych ofert: nowy projekt oceny z zapytaniem jako „SWZ” i kryteriami z zapytania."""
    m = S.meta(pid)
    Z = m.get("zapytanie") or {}
    if Z.get("ocena_id") and os.path.isdir(S.pdir(Z["ocena_id"])):
        return jsonify({"id": Z["ocena_id"]})
    oid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, oid, "dokumenty"))
    kat = os.path.join(S.pdir(pid), "zapytanie")
    if os.path.isdir(kat):
        for f in os.listdir(kat):
            if f.startswith(("Zapytanie", "Formularz")):
                S.shutil.copy2(os.path.join(kat, f), os.path.join(S.PROJ, oid, "dokumenty", f))
    kr = [dict(k, waga=k.get("waga") or 0, typ=(k.get("typ") or "min")) for k in ((Z.get("tresc") or {}).get("kryteria") or [])]
    om = {"id": oid, "nazwa": "Oferty – " + (m.get("nazwa") or "")[:80], "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "typ": "ocena_ofert",
          "strona": "zamawiajacy", "wlasciciel": m.get("wlasciciel") or S.konto_biezace(), "dostep": [], "pominiete": [], "zapytanie_id": pid,
          "ocena": {"swz": {"kryteria": kr, "kwota_zamawiajacego": (Z.get("dane") or {}).get("wartosc_netto") or "",
                            "zrodlo": "zapytanie ofertowe (zasada konkurencyjności)"} if kr else {}, "oferty": [], "podsum": {}}}
    S.zapisz_meta(oid, om)
    with S.BLOKADA:
        m = S.meta(pid)
        m.setdefault("zapytanie", {})["ocena_id"] = oid
        S.zapisz_meta(pid, m)
    return jsonify({"id": oid})


@bp.post("/api/projekty/<pid>/zapytanie/protokol")
@S.wymaga_logowania
def zapytanie_protokol(pid):
    m = S.meta(pid)
    Z = m.get("zapytanie") or {}
    oc = S.ocena_dane(S.meta(Z["ocena_id"])) if Z.get("ocena_id") and os.path.isdir(S.pdir(Z["ocena_id"])) else None
    kat = os.path.join(S.pdir(pid), "zapytanie")
    os.makedirs(kat, exist_ok=True)
    S.ZQ.protokol_docx(os.path.join(kat, "Protokol_z_postepowania.docx"), Z.get("dane") or {}, Z.get("publikacja") or {}, oc, _dotacja_info(Z.get("dotacja_id")))
    return jsonify(_zapytanie_stan(pid, S.meta(pid)))


@bp.post("/api/projekty/<pid>/zapytanie/do-rozliczenia")
@S.wymaga_logowania
def zapytanie_do_rozliczenia(pid):
    """Komplet dokumentów postępowania do projektu dotacji (folder dokumentów rozliczenia) – do wniosku o płatność."""
    m = S.meta(pid)
    Z = m.get("zapytanie") or {}
    if not Z.get("dotacja_id") or not _dotacja_dostepna(Z["dotacja_id"]):
        return jsonify({"blad": "Najpierw wybierz projekt dotacji, którego dotyczy to zamówienie (krok 1)."}), 400
    cel = os.path.join(S.pdir(Z["dotacja_id"]), "rozliczenie", "Zamowienia", re.sub(r"[^\w\- ]", "_", m.get("nazwa") or pid)[:60])
    os.makedirs(cel, exist_ok=True)
    ile = 0
    kat = os.path.join(S.pdir(pid), "zapytanie")
    for f in (os.listdir(kat) if os.path.isdir(kat) else []):
        S.shutil.copy2(os.path.join(kat, f), os.path.join(cel, f))
        ile += 1
    if Z.get("ocena_id") and os.path.isdir(os.path.join(S.pdir(Z["ocena_id"]), "ocena")):
        for f in os.listdir(os.path.join(S.pdir(Z["ocena_id"]), "ocena")):
            S.shutil.copy2(os.path.join(S.pdir(Z["ocena_id"]), "ocena", f), os.path.join(cel, f))
            ile += 1
    with S.BLOKADA:
        m = S.meta(pid)
        m.setdefault("zapytanie", {})["przekazano"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        S.zapisz_meta(pid, m)
    return jsonify({"ok": True, "plikow": ile, "folder": os.path.relpath(cel, S.pdir(Z["dotacja_id"]))})
