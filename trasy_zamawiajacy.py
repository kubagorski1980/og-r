# -*- coding: utf-8 -*-
"""
Zamawiający publiczny – trasy: plan zamówień (art. 23 Pzp), sprawozdanie do UZP (art. 82), ochrona ludności i obrona cywilna, ogłoszenia o wykonaniu umów (art. 448), szacowanie wartości, kalkulator kosztów pracy.
Blueprint „zamawiajacy_publiczny” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("zamawiajacy_publiczny", __name__)


@bp.post("/api/projekty/<pid>/szacowanie")
@S.wymaga_logowania
def szacowanie_zapisz(pid):
    m = S.meta(pid)
    if not m:
        abort(404)
    j = request.get_json(silent=True)
    if not isinstance(j, dict) or not isinstance(j.get("szacowanie") or {}, dict):
        return jsonify({"blad": "Szacowanie: nieprawidłowe dane – oczekiwano pól szacowania (podstawa, dokument, źródła, korekty)."}), 400
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        rz = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
        K["szacowanie"] = S.SZ.oczysc(j.get("szacowanie") or {}, rz)
        K["szacowanie_odcisk"] = S.odcisk_zakresu(K, rz)  # zmiana zakresu po szacowaniu → ponowne potwierdzenie (zapis szacowania)
        S.zapisz_meta(pid, m)
    return jsonify(S._kreator_stan(pid))


@bp.post("/api/projekty/<pid>/szacowanie/plik")
@S.wymaga_logowania
def szacowanie_plik(pid):
    """Kosztorys inwestorski / zestawienie PFU (cel=dokument) – odczyt wartości, daty i elementów; albo plik źródła ceny (cel=zrodlo)."""
    m = S.meta(pid)
    f = request.files.get("plik")
    if not m or not f:
        return jsonify({"blad": "Wybierz plik."}), 400
    kat = os.path.join(S.pdir(pid), "szacowanie")
    os.makedirs(kat, exist_ok=True)
    nazwa = S.MO.bezpieczna_nazwa(f.filename)[:120] or "plik"
    dane = f.read()
    with open(os.path.join(kat, nazwa), "wb") as w_:
        w_.write(dane)
    if request.form.get("cel") != "dokument":
        return jsonify({"plik": nazwa})
    try:
        odczyt = S.SZ.odczytaj_dokument(S.HN.tekst_pliku(nazwa, dane))
    except Exception:
        odczyt = {"wartosc": None, "data": None, "elementy": {}}
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        rz = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
        sz = S.SZ.oczysc(K.get("szacowanie") or {}, rz)
        d = sz["dokument"]
        d["plik"] = nazwa
        d["elementy"] = odczyt.get("elementy") or {}
        if odczyt.get("wartosc") and not d.get("wartosc"):
            d["wartosc"] = odczyt["wartosc"]
        if odczyt.get("data") and not d.get("data"):
            d["data"] = odczyt["data"]
        if odczyt.get("autor") and not d.get("autor"):
            d["autor"] = str(odczyt["autor"])[:200]
        K["szacowanie"] = sz
        S.zapisz_meta(pid, m)
    return jsonify(dict(S._kreator_stan(pid), odczyt=odczyt))


@bp.get("/api/projekty/<pid>/szacowanie/ceny")
@S.wymaga_logowania
def szacowanie_ceny(pid):
    """Ceny z rozstrzygniętych postępowań (pamięć rozstrzygnięć BZP i TED) – źródło do rozeznania rynku."""
    slowa = [w for w in re.findall(r"[\wąćęłńóśźż]{4,}", (request.args.get("q") or "").lower())][:6]
    if not slowa:
        return jsonify({"lista": []})
    wyn = []
    try:
        pliki = sorted(os.listdir(S.KAT_WYNIKI_DNI), reverse=True)
    except OSError:
        pliki = []
    for f_ in pliki[:2000]:
        for x in S.czytaj(os.path.join(S.KAT_WYNIKI_DNI, f_), [], pamiec=False) or []:
            if not x.get("cena") or not x.get("wykonawca") or x.get("uniewaznione"):
                continue
            prz = (x.get("przedmiot") or "").lower()
            traf = sum(1 for w in slowa if w[:6] in prz)
            if traf >= max(1, min(2, len(slowa))):
                wyn.append({"przedmiot": x.get("przedmiot"), "zamawiajacy": x.get("zamawiajacy"), "wykonawca": x.get("wykonawca"), "cena": x.get("cena"),
                            "ofert": x.get("ofert"), "data": x.get("data"), "numer": x.get("numer"), "trafien": traf})
        if len(wyn) >= 200:
            break
    wyn.sort(key=lambda x: (-x["trafien"], str(x.get("data") or "")), reverse=False)
    return jsonify({"lista": wyn[:30], "uwaga": "Ceny brutto z ogłoszeń o wyniku – przed dodaniem do szacowania przelicz na netto i sprawdź zgodność zakresu."})


@bp.post("/api/projekty/<pid>/szacowanie/zapytanie")
@S.wymaga_logowania
def szacowanie_zapytanie(pid):
    m = S.meta(pid)
    if not m:
        abort(404)
    K = m.get("kreator") or {}
    rz = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "uslugi"
    nazwa = f"Zapytanie_o_cene_{S.MO.bezpieczna_nazwa(m.get('nazwa', 'zamowienie'))[:50]}.docx"
    opis = "\n".join(x for x in (K.get("opis"), ((K.get("potrzeba") or {}).get("ilosci"))) if x)
    S.SZ.zapytanie_o_cene_docx(os.path.join(S.pdir(pid), nazwa), m.get("nazwa") or "", rz, opis,
                             S.zamawiajacy_projektu(m, {}), str((request.json or {}).get("termin") or ""))
    return jsonify({"plik": nazwa, "url": f"/pobierz/{pid}/{S.urllib.parse.quote(nazwa)}"})


def _owu_stan(pid):
    m = S.meta(pid)
    r = S.realizacja_dane(pid)
    return S.OW.stan(r, r.get("ogloszenie_wykonania") or {}, m)


@bp.get("/api/projekty/<pid>/ogloszenie-wykonania")
@S.wymaga_logowania
def owu_pobierz(pid):
    return jsonify(_owu_stan(pid))


@bp.post("/api/projekty/<pid>/ogloszenie-wykonania")
@S.wymaga_logowania
def owu_zapisz(pid):
    j = request.json or {}
    with S.BLOKADA:
        r = S.realizacja_dane(pid)
        o = r.setdefault("ogloszenie_wykonania", {})
        for k in ("data_wykonania", "termin_pierwotny", "przyczyna_opoznienia", "bez_kar_uzasadnienie", "nalezycie", "opis_nienaleznego", "okres",
                  "nr_ogloszenia", "wyplacone", "cena_ofertowa"):
            if k in j:
                o[k] = str(j[k] or "")[:2000]
        if "odstapienie" in j:  # art. 446 ust. 1 pkt 4 – odstąpienie od umowy albo wypowiedzenie (w całości lub w części)
            if j["odstapienie"] not in ("", None) + S.OW.ODSTAPIENIA:
                return jsonify({"blad": "Odstąpienie / wypowiedzenie: wybierz z listy."}), 400
            o["odstapienie"] = j["odstapienie"] or ""
        if "kary_w_platnosciach" in j:
            o["kary_w_platnosciach"] = bool(j["kary_w_platnosciach"])
        if isinstance(j.get("kary"), list):
            o["kary"] = [{"tytul": str(k.get("tytul") or "")[:200], "kwota": str(k.get("kwota") or ""), "potracona": bool(k.get("potracona"))}
                         for k in j["kary"] if isinstance(k, dict)][:30]
        if isinstance(j.get("zmiany"), list):
            o["zmiany"] = [{x: str(z.get(x) or "")[:500] for x in ("nr", "data", "podstawa", "przyczyna", "opis", "wartosc")} for z in j["zmiany"] if isinstance(z, dict)][:30]
        if isinstance(j.get("publikacja"), dict):
            o.setdefault("publikacja", {}).update({k: str(v or "")[:200] for k, v in j["publikacja"].items() if k in ("numer", "data")})
        if o.get("publikacja", {}).get("numer") and o.get("publikacja", {}).get("data"):
            m = S.meta(pid)
            if m.get("status_projektu") == "realizacja" and j.get("zamknij"):
                m["status_projektu"] = "zakonczony"
                S.zapisz_meta(pid, m)
        S.zapisz_realizacje(pid, r)
    return jsonify(_owu_stan(pid))


@bp.get("/api/projekty/<pid>/ogloszenie-wykonania/word")
@S.wymaga_logowania
def owu_word(pid):
    m = S.meta(pid)
    s_ = _owu_stan(pid)
    kat = os.path.join(S.pdir(pid), "realizacja", "dokumenty")
    os.makedirs(kat, exist_ok=True)
    if request.args.get("raport"):
        sc = os.path.join(kat, "Raport_z_realizacji_zamowienia_art_446.docx")
        S.OW.raport_docx(sc, m.get("nazwa") or "", s_, S.realizacja_dane(pid))
    else:
        sc = os.path.join(kat, "Dane_do_ogloszenia_o_wykonaniu_umowy.docx")
        S.OW.ogloszenie_docx(sc, m.get("nazwa") or "", s_)
    return send_file(sc, as_attachment=True, download_name=os.path.basename(sc))


@bp.post("/api/projekty/<pid>/ogloszenie-wykonania/dowod")
@S.wymaga_logowania
def owu_dowod(pid):
    """Dowód zamieszczenia ogłoszenia w BZP (PDF / zrzut) – do dokumentacji postępowania (art. 267 Pzp)."""
    S.meta(pid)
    f = request.files.get("plik")
    if not f:
        return jsonify({"blad": "Wybierz plik."}), 400
    kat = os.path.join(S.pdir(pid), "realizacja", "dokumenty")
    os.makedirs(kat, exist_ok=True)
    nazwa = "Dowod_publikacji_ogloszenia_o_wykonaniu_umowy" + (os.path.splitext(f.filename or "")[1].lower() or ".pdf")
    f.save(os.path.join(kat, nazwa))
    with S.BLOKADA:
        r = S.realizacja_dane(pid)
        r.setdefault("ogloszenie_wykonania", {}).setdefault("publikacja", {})["dowod"] = nazwa
        S.zapisz_realizacje(pid, r)
    return jsonify(_owu_stan(pid))


@bp.get("/api/zam/ogloszenia-wykonania")
@S.wymaga_logowania
def owu_lista():
    """Zamawiający: inwestycje z wykonaną umową bez opublikowanego ogłoszenia o wykonaniu umowy – z terminem."""
    wyn, login, rola = [], session.get("login"), S.rola_sesji()
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if not m or m.get("strona") != "zamawiajacy" or m.get("status_projektu") not in ("realizacja", "zakonczony") or m.get("archiwum") \
                or not S.ma_dostep(m, login, rola, lista=True):
            continue
        try:
            st = _owu_stan(pid)
        except Exception:
            continue
        if st["data_wykonania"] and not st["opublikowane"]:
            wyn.append({"id": pid, "nazwa": m.get("nazwa"), "termin": st["termin_publikacji"], "dni": st["dni_do_terminu"]})
    return jsonify(sorted(wyn, key=lambda x: x["termin"] or "9"))


def _olioc():
    d = S.czytaj(S._plik_konta("olioc.json"), {}) or {}
    d = d if isinstance(d, dict) else {}
    lista = lambda x: [y for y in x if isinstance(y, dict)] if isinstance(x, list) else []  # wpisy zapisane wcześniej z błędem – pomijane
    zad = lista(d.get("zadania"))
    for z in zad:
        if "wydatki" in z:
            z["wydatki"] = lista(z.get("wydatki"))
    return {"gmina": d.get("gmina") if isinstance(d.get("gmina"), dict) else {}, "obiekty": lista(d.get("obiekty")), "zadania": zad}


@bp.get("/api/olioc")
@S.wymaga_logowania
def olioc_stan():
    d = _olioc()
    return jsonify({**d, "pokrycie": S.OL.pokrycie(d["gmina"], d["obiekty"]), "kontrola": S.OL.kontrola(d["zadania"]),
                    "obszary": {k: {"nazwa": v[0], "dzialy": v[1], "rodzaj": v[2]} for k, v in S.OL.OBSZARY.items()}, "kategorie": S.OL.KATEGORIE,
                    "normy": S.OL.NORMY, "typy_gmin": S.OL.TYPY_GMIN})


@bp.post("/api/olioc")
@S.wymaga_logowania
def olioc_zapisz():
    j = request.json or {}
    d = _olioc()
    for k in ("gmina", "obiekty", "zadania"):
        if k in j:
            if not isinstance(j[k], dict if k == "gmina" else list):
                return jsonify({"blad": f"Nieprawidłowe dane: {k}"}), 400
            if k != "gmina" and not all(isinstance(x, dict) for x in j[k]):  # sprawdzenie przed zapisem – błędny wpis nie blokuje modułu
                return jsonify({"blad": f"Nieprawidłowe dane: {k} – każdy element musi być obiektem."}), 400
            if k == "zadania" and not all(isinstance(x.get("wydatki") or [], list) and all(isinstance(w, dict) for w in x.get("wydatki") or [])
                                          for x in j[k]):
                return jsonify({"blad": "Nieprawidłowe dane: wydatki zadania – lista pozycji z kwotą, datą i dokumentem."}), 400
            d[k] = j[k]
    for lista in (d["obiekty"], d["zadania"]):
        for x in lista:
            if isinstance(x, dict) and not x.get("id"):
                x["id"] = uuid.uuid4().hex[:10]
    S.pisz(S._plik_konta("olioc.json"), d)
    return jsonify({"ok": True, **d, "pokrycie": S.OL.pokrycie(d["gmina"], d["obiekty"]), "kontrola": S.OL.kontrola(d["zadania"])})


@bp.post("/api/olioc/powiaz")
@S.wymaga_logowania
def olioc_powiaz():
    j = request.json or {}
    d = _olioc()
    zad = next((x for x in d["zadania"] if isinstance(x, dict) and x.get("id") == j.get("zadanie_id")), None)
    if not zad:
        return jsonify({"blad": "Nie ma takiego zadania."}), 404
    if not _projekt_konta_id(j.get("projekt_id")):
        return jsonify({"blad": "Nie ma takiego zamówienia na tym koncie."}), 404
    zad["projekt_id"] = str(j.get("projekt_id") or "")[:40]
    if zad.get("status") in (None, "", "planowane", "przyznane"):
        zad["status"] = "w realizacji"
    S.pisz(S._plik_konta("olioc.json"), d)
    return jsonify({"ok": True})


@bp.get("/api/olioc/raport")
@S.wymaga_logowania
def olioc_raport():
    kat = os.path.join(S.katalog_konta(), "kalkulacje")
    os.makedirs(kat, exist_ok=True)
    sc = os.path.join(kat, f"Ochrona_ludnosci_{dt.date.today():%Y%m%d}.docx")
    S.OL.raport_docx(sc, _olioc())
    return send_file(sc, as_attachment=True)


def _projekt_konta(m):
    """Projekt należy do bieżącego konta (właściciel) – sprawozdanie, plan i OLiOC konta nie obejmują projektów innych kont."""
    return (m.get("wlasciciel") or S.login_admina()).lower() == S.konto_biezace().lower()


def _projekt_konta_id(pid):
    """Pusty identyfikator (odłączenie) albo projekt bieżącego konta."""
    pid = str(pid or "").strip()
    if not pid:
        return True
    m = S.czytaj(os.path.join(S.PROJ, os.path.basename(pid), "projekt.json"), None)
    return bool(m) and _projekt_konta(m)


def _sprawozdania():
    return S.czytaj(S._plik_konta("sprawozdania_uzp.json"), {}) or {}


@bp.get("/api/sprawozdanie")
@S.wymaga_logowania
def sprawozdanie_stan():
    rok = S._rok_spr(request.args.get("rok")) or dt.date.today().year - (1 if dt.date.today().month <= 3 else 0)
    S_lok = _sprawozdania().get(str(rok)) or {}
    poz = S_lok.get("pozycje") or []
    zam = {**S._dane_zamawiajacego(), **{k: v for k, v in (S_lok.get("zamawiajacy") or {}).items() if v}}
    return jsonify({"rok": rok, "zamawiajacy": zam, "pozycje": poz, "zestawienie": S.SPR.zestawienie(poz, rok), "rodzaje": S.SPR.RODZAJE,
                    "kategorie": S.SPR.KATEGORIE, "tryby": S.SPR.TRYBY, "spoleczne": S.SPR.SPOLECZNE, "srodowiskowe": S.SPR.SRODOWISKOWE,
                    "prog_krajowy": S.PR.prog_pzp(f"{rok}-06-30")})


@bp.post("/api/sprawozdanie")
@S.wymaga_logowania
def sprawozdanie_zapisz():
    j = request.json or {}
    rok = S._rok_spr(j.get("rok"))
    if not rok or not isinstance(j.get("pozycje", []), list):
        return jsonify({"blad": "Podaj rok sprawozdawczy (2021–2100) i listę zamówień."}), 400
    W = _sprawozdania()
    S_lok = W.setdefault(str(rok), {})
    if "pozycje" in j:
        S_lok["pozycje"] = [dict(p, id=p.get("id") or uuid.uuid4().hex[:10]) for p in j["pozycje"] if isinstance(p, dict)]
    if isinstance(j.get("zamawiajacy"), dict):
        S_lok["zamawiajacy"] = {k: str(v)[:300] for k, v in j["zamawiajacy"].items()}
    S.pisz(S._plik_konta("sprawozdania_uzp.json"), W)
    return jsonify({"ok": True, "zestawienie": S.SPR.zestawienie(S_lok.get("pozycje") or [], rok)})


@bp.post("/api/sprawozdanie/import")
@S.wymaga_logowania
def sprawozdanie_import():
    """Zamówienia z projektów zamawiającego, w których umowę zawarto w roku sprawozdawczym (bez powtórzeń)."""
    rok = S._rok_spr((request.json or {}).get("rok"))
    if not rok:
        return jsonify({"blad": "Podaj rok sprawozdawczy."}), 400
    W = _sprawozdania()
    S_lok = W.setdefault(str(rok), {})
    poz = S_lok.setdefault("pozycje", [])
    znane = {p.get("id") for p in poz}
    nowe = 0
    for m in S.projekty_konta():
        if m.get("strona") != "zamawiajacy" and m.get("typ") not in ("zamowienie", "ocena_ofert"):
            continue
        if (m.get("kreator") or {}).get("prywatny"):
            continue  # zamawiający prywatny (wspólnota, deweloper) nie składa sprawozdania do UZP
        if not _projekt_konta(m):
            continue  # sprawozdanie konta – tylko jego zamówienia (administrator z zakresem „wszystkie” nie importuje umów innych kont)
        try:
            netto, zrodlo = S._netto_zam_zrodlo(m)  # wartość szacunkowa jak w kreatorze; „orientacyjny budżet” nie jest wartością zamówienia
        except Exception:
            netto, zrodlo = None, ""
        try:
            oc_ = S._ocena_zamowienia(m)  # oferty w powiązanym projekcie oceny (liczba ofert i odrzuconych)
        except Exception:
            oc_ = None
        try:
            p = S.SPR.z_projektu(m, S.realizacja_dane(m["id"]), rok, wartosc_szac=netto if zrodlo != "budzet" else None, ocena=oc_)
        except Exception:
            p = None
        if p and p["id"] not in znane:
            poz.append(p)
            nowe += 1
    S.pisz(S._plik_konta("sprawozdania_uzp.json"), W)
    return jsonify({"ok": True, "dodano": nowe, "zestawienie": S.SPR.zestawienie(poz, rok), "pozycje": poz})


@bp.get("/api/sprawozdanie/xlsx")
@S.wymaga_logowania
def sprawozdanie_xlsx():
    rok = S._rok_spr(request.args.get("rok"))
    if not rok:
        return jsonify({"blad": "Podaj rok sprawozdawczy."}), 400
    S_lok = _sprawozdania().get(str(rok)) or {}
    kat = os.path.join(S.katalog_konta(), "kalkulacje")
    os.makedirs(kat, exist_ok=True)
    sc = os.path.join(kat, f"Sprawozdanie_UZP_{rok}.xlsx")
    S.SPR.xlsx(sc, {**S._dane_zamawiajacego(), **{k: v for k, v in (S_lok.get("zamawiajacy") or {}).items() if v}}, S.SPR.zestawienie(S_lok.get("pozycje") or [], rok))
    return send_file(sc, as_attachment=True)


class _BladRoku(Exception):
    pass


def _pz_rok(v):
    """Rok planu 2020–2100; inny – odpowiedź 400 z komunikatem (nie błąd serwera)."""
    try:
        return S._pz_rok(v)
    except (ValueError, TypeError, OverflowError):
        raise _BladRoku()


@bp.errorhandler(_BladRoku)
def _blad_roku(e):
    return jsonify({"blad": "Rok planu: od 2020 do 2100."}), 400


@bp.get("/api/plan")
@S.wymaga_logowania
def planz_pobierz():
    return jsonify(S._pz_odpowiedz(_pz_rok(request.args.get("rok"))))


@bp.post("/api/plan/ustawienia")
@S.wymaga_logowania
def planz_ustawienia():
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        if j.get("rodzaj_zamawiajacego") in S.PZ.RODZAJE_ZAMAWIAJACEGO:
            plan["rodzaj_zamawiajacego"] = j["rodzaj_zamawiajacego"]
        plan["centralny"] = bool(j.get("centralny"))
        d = str(j.get("data_budzetu") or "")[:10]
        if d:
            try:
                dt.date.fromisoformat(d)
            except ValueError:
                return jsonify({"blad": "Data przyjęcia budżetu w formacie RRRR-MM-DD."}), 400
        plan["data_budzetu"] = d
        plan["numer_bzp"] = str(j.get("numer_bzp") or "")[:40]
        S._pz_zapisz(P)
    return jsonify(S._pz_odpowiedz(rok))


@bp.post("/api/plan/pozycja")
@S.wymaga_logowania
def planz_pozycja():
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    r = j.get("pozycja") or {}
    if not str(r.get("przedmiot") or "").strip():
        return jsonify({"blad": "Podaj przedmiot zamówienia."}), 400
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        p_ = S.PZ.oczysc_pozycje(r, plan)
        i = next((n for n, x in enumerate(plan["pozycje"]) if x["id"] == p_["id"]), None)
        if i is None:
            plan["pozycje"].append(p_)
        else:
            plan["pozycje"][i] = p_
        S._pz_zapisz(P)
    return jsonify(dict(S._pz_odpowiedz(rok), zapisano=p_["id"]))


@bp.post("/api/plan/usun")
@S.wymaga_logowania
def planz_usun():
    """Pozycja z opublikowanego planu nie znika – dostaje status „rezygnacja” (aktualizacja planu); nieopublikowana – usuwana."""
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        opublikowane = {x["id"] for w in plan.get("wersje") or [] for x in w.get("pozycje") or []}
        if j.get("id") in opublikowane:
            for x in plan["pozycje"]:
                if x["id"] == j.get("id"):
                    x["status"] = "rezygnacja"
        else:
            plan["pozycje"] = [x for x in plan["pozycje"] if x["id"] != j.get("id")]
        S._pz_zapisz(P)
    return jsonify(S._pz_odpowiedz(rok))


@bp.post("/api/plan/kopiuj")
@S.wymaga_logowania
def planz_kopiuj():
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    with S.BLOKADA:
        P = S._pz_plany()
        zrodlo = (P.get("plany") or {}).get(str(rok - 1))
        if not zrodlo or not zrodlo.get("pozycje"):
            return jsonify({"blad": f"Brak planu na rok {rok - 1} do skopiowania."}), 400
        plan = S._pz_plan(rok, P)
        for x in zrodlo["pozycje"]:
            if x.get("status") == "rezygnacja":
                continue
            plan["pozycje"].append(S.PZ.oczysc_pozycje(dict(x, id="", status="zaplanowane", projekt_id="", id_bzp=""), plan))
        plan["rodzaj_zamawiajacego"] = zrodlo.get("rodzaj_zamawiajacego") or plan["rodzaj_zamawiajacego"]
        S._pz_zapisz(P)
    return jsonify(S._pz_odpowiedz(rok))


@bp.post("/api/plan/import")
@S.wymaga_logowania
def planz_import():
    rok = _pz_rok(request.form.get("rok"))
    f = request.files.get("plik")
    if not f or not f.filename.lower().endswith((".xlsx", ".xlsm")):
        return jsonify({"blad": "Wgraj plik Excel (.xlsx) – wzór pobierzesz przyciskiem „Wzór importu”."}), 400
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        try:
            nowe = S.PZ.import_excel(f.read(), plan)
        except Exception as e:
            return jsonify({"blad": f"Nie udało się odczytać arkusza: {str(e)[:120]}"}), 400
        plan["pozycje"] += nowe
        S._pz_zapisz(P)
    return jsonify(dict(S._pz_odpowiedz(rok), dodano=len(nowe)))


@bp.post("/api/plan/budzet")
@S.wymaga_logowania
def planz_budzet():
    rok = _pz_rok(request.form.get("rok"))
    f = request.files.get("plik")
    if not f:
        return jsonify({"blad": "Wgraj uchwałę budżetową albo plan finansowy (PDF, Word, Excel)."}), 400
    plik = S._pz_plik()
    os.makedirs(os.path.dirname(plik), exist_ok=True)
    return jsonify(S.uruchom("plan_budzet", f"Propozycje planu zamówień z budżetu ({rok})", S.praca_plan_z_budzetu, plik, f.filename, f.read(), rok))


@bp.post("/api/plan/opublikuj")
@S.wymaga_logowania
def planz_opublikuj():
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        if plan.get("wersje") and not S.PZ.zmiany_od_publikacji(plan):
            return jsonify({"blad": "Od ostatniej publikacji nie ma zmian w planie postępowań."}), 400
        pusty = S.PZ.plan_postepowan_pusty(plan)
        S.PZ.opublikuj(plan, str(j.get("numer_bzp") or "")[:40])
        S._pz_zapisz(P)
    odp = S._pz_odpowiedz(rok)
    if pusty:  # H3-06: pusty plan postępowań – ostrzeżenie, nie blokada (zapis dla porządku, np. potwierdzenie braku postępowań)
        odp["ostrzezenie"] = S.PZ.OSTRZEZENIE_PUSTY
    return jsonify(odp)


@bp.get("/api/plan/plik/<rodzaj>")
@S.wymaga_logowania
def planz_plik(rodzaj):
    rok = _pz_rok(request.args.get("rok"))
    kat = os.path.join(S.katalog_konta(), "plan_dokumenty")
    os.makedirs(kat, exist_ok=True)
    if rodzaj == "wzor":
        sc = os.path.join(kat, "Wzor_importu_planu_zamowien.xlsx")
        S.PZ.wzor_importu(sc)
        return send_file(sc, as_attachment=True)
    plan = S._pz_plan(rok, S._pz_plany())
    if rodzaj == "xlsx":
        sc = os.path.join(kat, f"Plan_postepowan_{rok}_do_BZP.xlsx")
        S.PZ.plan_xlsx(sc, plan)
    elif rodzaj == "docx":
        sc = os.path.join(kat, f"Plan_postepowan_{rok}_strona_internetowa.docx")
        S.PZ.plan_docx(sc, plan, S.cfg().get("firma_nazwa") or "")
    else:
        abort(404)
    return send_file(sc, as_attachment=True)


@bp.post("/api/plan/powiaz")
@S.wymaga_logowania
def planz_powiaz():
    j = request.json or {}
    rok = _pz_rok(j.get("rok"))
    if not _projekt_konta_id(j.get("projekt_id")):
        return jsonify({"blad": "Nie ma takiego zamówienia na tym koncie."}), 404
    with S.BLOKADA:
        P = S._pz_plany()
        plan = S._pz_plan(rok, P)
        for x in plan["pozycje"]:
            if x["id"] == j.get("id"):
                x["projekt_id"] = str(j.get("projekt_id") or "")[:20]
                x["status"] = "wszczęte"
        S._pz_zapisz(P)
    return jsonify({"ok": True})


@bp.get("/api/plan/przypomnienia")
@S.wymaga_logowania
def planz_przypomnienia():
    """Na Przegląd zamawiającego: termin publikacji planu i pozycje, których termin wszczęcia przypada w bieżącym miesiącu albo kwartale."""
    dzis = dt.date.today()
    L = []
    for rok, plan in (S._pz_plany().get("plany") or {}).items():
        if int(rok) not in (dzis.year, dzis.year + 1):
            continue
        for k in S.PZ.kontrole(plan):
            if k["opis"].startswith("Termin publikacji planu"):
                L.append({"rok": rok, "opis": k["opis"], "pilne": k["waga"] == "blad"})
        if int(rok) == dzis.year:
            kw = (dzis.month - 1) // 3 + 1
            for p_ in plan["pozycje"]:
                if p_.get("status") == "zaplanowane" and ((p_["termin_typ"] == "miesiac" and p_["termin"] <= dzis.month)
                                                          or (p_["termin_typ"] == "kwartal" and p_["termin"] <= kw)):
                    L.append({"rok": rok, "id": p_["id"], "opis": f"{p_['id']} {p_['przedmiot'][:70]} – termin wszczęcia: {S.PZ.termin_opis(p_)}",
                              "pilne": (p_["termin_typ"] == "miesiac" and p_["termin"] < dzis.month) or (p_["termin_typ"] == "kwartal" and p_["termin"] < kw)})
    return jsonify(L[:20])


@bp.post("/api/kalkulator-pracy")
@S.wymaga_logowania
def kalkulator_pracy():
    """Kalkulator kosztów pracy – usługi pracochłonne (parametry 2026, umowa o pracę)."""
    return jsonify(S.RY.kalkulator_pracy(request.json or {}))


@bp.post("/api/kalkulator-pracy/word")
@S.wymaga_logowania
def kalkulator_pracy_word():
    p = request.json or {}
    w = S.RY.kalkulator_pracy(p)
    kat = os.path.join(S.katalog_konta(), "kalkulacje")
    os.makedirs(kat, exist_ok=True)
    nazwa = f"Koszty_pracy_{dt.datetime.now():%Y%m%d_%H%M%S}.docx"
    S.RY.kalkulator_docx(os.path.join(kat, nazwa), p, w, str(p.get("tytul") or "")[:200])
    return jsonify({"url": f"/api/kalkulator-pracy/plik/{nazwa}"})


@bp.get("/api/kalkulator-pracy/plik/<nazwa>")
@S.wymaga_logowania
def kalkulator_pracy_plik(nazwa):
    if not re.fullmatch(r"Koszty_pracy_\d{8}_\d{6}\.docx", nazwa):
        abort(404)
    return send_file(os.path.join(S.katalog_konta(), "kalkulacje", nazwa), as_attachment=True)
