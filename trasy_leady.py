# -*- coding: utf-8 -*-
"""
Leady z przetargów (moduł właściciela) – trasy: lista leadów i ustawienia.
Blueprint „leady” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("leady", __name__)


def _znwu_procenty(P):
    """{numer: (procent, źródło)} zabezpieczenia należytego wykonania dla postępowań z modułu Odwołań: pole „zabezpieczenie” z analizy
    przetargu (SWZ/ogłoszenie), pełna treść ogłoszenia w bazie przetargów, wspólna pamięć ogłoszeń BZP (sekcja 6.5 i dalsze)."""
    nr_ = [nr for nr, r in P.items() if r.get("ocena")]
    if not nr_:
        return {}
    wyn = {}
    try:
        db = S.db_przetargi() or {}
    except Exception:
        db = {}
    for nr in nr_:
        t = db.get(nr) or {}
        p = S.LD.znwu_procent(t.get("zabezpieczenie"), cale_pole=True)
        if p:
            wyn[nr] = (p, "analiza przetargu – sprawdź w SWZ")
            continue
        p = S.LD.znwu_procent(t.get("tresc"))
        if p:
            wyn[nr] = (p, "ogłoszenie")
    brak = [nr for nr in nr_ if nr not in wyn]
    if brak:
        try:
            idx = {o.get("numer"): o for o in S.WSP.wszystkie(120)}
        except Exception:
            idx = {}
        for nr in brak:
            o = idx.get(nr) or {}
            p = o.get("znwu_proc") or S.LD.znwu_procent(o.get("tresc"))
            if p:
                wyn[nr] = (p, "ogłoszenie BZP")
    return wyn


def _leady(typ, a):
    """Leady: typ „wadium” (otwarte przetargi z wadium – pamięć ogłoszeń) albo „zwyciezcy” (wybrani wykonawcy – moduł Odwołań)."""
    woj = a.get("woj") or ""
    rodz = a.get("rodzaj") or ""
    slowa = [s.strip().lower() for s in re.split(r"[,;]", a.get("slowa") or "") if s.strip()]
    mn = S.RY._f(a.get("min")) or 0
    pas = lambda przedmiot, w_, r_: (not woj or w_ == woj) and (not rodz or r_ == rodz) and (not slowa or any(s in (przedmiot or "").lower() for s in slowa))
    if typ == "wadium":
        teraz = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")
        L = []
        for o in S.WSP.wszystkie(60):
            tm = str(o.get("termin_ofert") or "").replace(" ", "T")[:16]
            # termin z godziną – porównanie z chwilą obecną (dawniej przetarg z terminem dziś o 10:00 był leadem do końca dnia);
            # sama data – do końca tego dnia
            if not o.get("wadium_wymagane") or not tm or (tm < teraz if len(tm) > 10 else tm < teraz[:10]):
                continue
            w_ = S.wojewodztwo_ogloszenia(o)
            r_ = S.OP.rodzaj_z_bzp(o.get("rodzaj"))
            if (o.get("wadium") or 0) < mn or not pas(o.get("przedmiot"), w_, r_):
                continue
            L.append({"numer": o.get("numer"), "przedmiot": o.get("przedmiot"), "zamawiajacy": o.get("zamawiajacy"), "wojewodztwo": w_, "rodzaj": r_,
                      "wadium": o.get("wadium"), "znwu": o.get("znwu"), "znwu_proc": o.get("znwu_proc"), "termin_ofert": str(o.get("termin_ofert") or "")[:16], "link": o.get("link")})
        return sorted(L, key=lambda x: -(x["wadium"] or 0))[:1000]
    B_ = S._op()
    P = B_.postepowania()
    dni = max(1, min(60, int(S.RY._f(a.get("dni")) or 14)))
    dzis = dt.date.today()
    kody = {S.WOJEWODZTWA[woj]: woj} if woj in S.WOJEWODZTWA else {k: n for n, k in S.WOJEWODZTWA.items()}
    L = []
    for i_ in range(0, dni + 1):
        d = (dzis - dt.timedelta(days=i_)).isoformat()
        for kod, nazwa in kody.items():
            for x in S.czytaj(os.path.join(S.KAT_WYNIKI_DNI, f"{kod}_{d}_v3.json"), [], pamiec=False) or []:
                if x.get("wykonawca") and not x.get("uniewaznione"):
                    L.append(dict(x, zrodlo="BZP", wojewodztwo=nazwa, etap="umowa zawarta"))
        for x in S.czytaj(os.path.join(S.KAT_WYNIKI_DNI, f"TED_{d}.json"), [], pamiec=False) or []:
            if x.get("wykonawca") and (not woj or x.get("wojewodztwo") == woj):
                L.append(dict(x, etap="umowa zawarta"))
    if any(not r_.get("wojewodztwo") for r_ in P.values()):
        S._odw_uzupelnij_woj(B_, P)
    for x in S.LD.zwyciezcy(P, _znwu_procenty(P)):  # wcześniejszy sygnał: informacja o wyborze, przed podpisaniem umowy
        x["wojewodztwo"] = x["wojewodztwo"] or (P.get(x["numer"]) or {}).get("wojewodztwo") or ""
        if not woj or x["wojewodztwo"] == woj:
            L.append(dict(x, zrodlo="Odwołania", etap="przed umową", data=x.get("data_wyboru") or "", cena=x.get("cena_brutto"),
                          ofert=x.get("liczba_ofert"), typ_zam=x.get("rodzaj")))
    with S.OP.BLOKADA:
        K = B_.czytaj("kontakty.json", {})
    L_, widz = [], set()
    for x in L:  # to samo rozstrzygnięcie (np. zapisane przy ponownym pobraniu dnia) – raz
        klucz = (x.get("numer"), (x.get("nip") or x.get("wykonawca") or "")[:40], round(x.get("cena") or 0))
        if klucz not in widz:
            widz.add(klucz)
            L_.append(x)
    L = L_
    diag = {"w_okresie": len(L), "po_rodzaju": 0, "po_slowach": 0, "po_cenie": 0}
    wyn = []
    for x in L:
        r_ = x.get("rodzaj") if x.get("rodzaj") in S.OP.RODZAJE else (S.OP.rodzaj_z_bzp(x.get("typ_zam")) or "")
        if rodz and r_ != rodz:
            continue
        diag["po_rodzaju"] += 1
        if slowa and not any(s_ in (x.get("przedmiot") or "").lower() for s_ in slowa):
            continue
        diag["po_slowach"] += 1
        if (x.get("cena") or 0) < mn:
            continue
        diag["po_cenie"] += 1
        k = K.get(S.NIP.oczysc(x.get("nip"))) or {}
        em = x.get("email") or ", ".join(e for e in dict.fromkeys([k.get("email", "")] + (k.get("emaile_strona") or [])) if e)  # Odwołania: kontakt oferenta
        tel = x.get("telefon") or ", ".join(t for t in dict.fromkeys([k.get("telefon", "")] + (k.get("telefony_strona") or [])) if t)
        if x.get("www") or x.get("adres") or x.get("krs"):
            k = dict(k, www=k.get("www") or x.get("www"), adres=k.get("adres") or x.get("adres"), krs=k.get("krs") or x.get("krs"), _z_odwolan=True)
        wyn.append({"data": x.get("data") or "", "etap": x["etap"], "zrodlo": x.get("zrodlo"), "wykonawca": x.get("wykonawca"), "nip": x.get("nip") or "",
                    "siedziba": x.get("siedziba") or "", "przedmiot": x.get("przedmiot") or "", "zamawiajacy": x.get("zamawiajacy") or "",
                    "wojewodztwo": x.get("wojewodztwo") or "", "rodzaj": r_, "cena_brutto": x.get("cena"), "liczba_ofert": x.get("ofert"),
                    "znwu_szac": x.get("znwu_szac") if x["etap"] == "przed umową" else None,  # % z ogłoszenia/SWZ albo do 5% (art. 452 ust. 2 Pzp)
                    "znwu_proc": x.get("znwu_proc") if x["etap"] == "przed umową" else None,
                    "znwu_opis": x.get("znwu_opis") or "" if x["etap"] == "przed umową" else "",
                    "numer": x.get("numer") or "", "link": x.get("link") or "", "kontakt_pobrany": bool(k), "adres": k.get("adres") or "",
                    "krs": k.get("krs") or "", "email": em, "telefon": tel, "www": k.get("www") or "", "status_vat": k.get("status_vat") or "",
                    "ade": k.get("ade") or ""})
    wyn.sort(key=lambda x: (x["etap"] == "przed umową", x["data"], x["cena_brutto"] or 0), reverse=True)  # przed umową, najnowsze, najwyższa cena
    if S.has_request_context():
        S.g.leady_diag = diag
    return wyn[:1000]


@bp.get("/api/leady")
@S.wymaga_logowania
def leady():
    typ = request.args.get("typ") if request.args.get("typ") in ("wadium", "zwyciezcy") else "wadium"
    if typ == "wadium" and not S._WADIUM_STAN["trwa"] and S._WADIUM_STAN["dzien"] != dt.date.today().isoformat():
        S.threading.Thread(target=S.uzupelnij_wadium_w_pamieci, daemon=True).start()  # raz dziennie: brakujące dane o wadium w starszych ogłoszeniach
        S._WADIUM_STAN["trwa"] = True
    zbieranie = False
    if typ == "zwyciezcy":
        if S._ROZSTRZ_STAN["trwa"]:
            zbieranie = True
        elif S._ROZSTRZ_STAN["dzien"] != dt.date.today().isoformat() and S._rozstrzygniecia_w_pamieci() < 10:
            S._ROZSTRZ_STAN["trwa"] = zbieranie = True  # pierwsze otwarcie: rozstrzygnięcia z ostatnich 21 dni w tle (kilka minut)
            S.threading.Thread(target=S._zbierz_rozstrzygniecia_w_tle, daemon=True).start()
    lista = _leady(typ, request.args)
    return jsonify({"typ": typ, "lista": lista, "wojewodztwa": list(S.WOJEWODZTWA), "rodzaje": S.OP.RODZAJE,
                    "uzupelnianie": S._WADIUM_STAN["trwa"] if typ == "wadium" else False, "zbieranie": zbieranie,
                    "dni_w_pamieci": S._rozstrzygniecia_w_pamieci() if typ == "zwyciezcy" else None, "diag": getattr(S.g, "leady_diag", None)})


@bp.post("/api/leady/kontakt")
@S.wymaga_logowania
def leady_kontakt():
    """Kontakt do firmy na żądanie (rejestry i strona www) – zapamiętywany na 30 dni."""
    B_ = S._op()
    with S.OP.BLOKADA:
        K = B_.czytaj("kontakty.json", {})
    k, nowe = S.kontakt_firmy((request.json or {}).get("nip"), K)
    if not k:
        return jsonify({"blad": "Brak poprawnego NIP-u – kontakt sprawdź ręcznie."}), 400
    if nowe:
        with S.OP.BLOKADA:
            B_.pisz("kontakty.json", {**B_.czytaj("kontakty.json", {}), **K})
    em = ", ".join(e for e in dict.fromkeys([k.get("email", "")] + (k.get("emaile_strona") or [])) if e)
    tel = ", ".join(t for t in dict.fromkeys([k.get("telefon", "")] + (k.get("telefony_strona") or [])) if t)
    return jsonify({"email": em, "telefon": tel, "www": k.get("www") or "", "adres": k.get("adres") or "", "krs": k.get("krs") or "",
                    "status_vat": k.get("status_vat") or "", "ade": k.get("ade") or ""})


@bp.get("/api/leady.csv")
@S.wymaga_logowania
def leady_csv():
    import csv
    import io as _io
    typ = request.args.get("typ") if request.args.get("typ") in ("wadium", "zwyciezcy") else "wadium"
    L = _leady(typ, request.args)
    kol = (["numer", "przedmiot", "zamawiajacy", "wojewodztwo", "rodzaj", "wadium", "znwu", "znwu_proc", "termin_ofert", "link"] if typ == "wadium" else
           ["data", "etap", "zrodlo", "wykonawca", "nip", "siedziba", "krs", "adres", "email", "telefon", "www", "status_vat", "przedmiot", "zamawiajacy",
            "wojewodztwo", "rodzaj", "cena_brutto", "liczba_ofert", "znwu_szac", "znwu_opis", "numer", "link"])
    b = _io.StringIO()
    w = csv.writer(b, delimiter=";")
    w.writerow(kol)
    def kom(v):
        """Komórka CSV dla Excela (średnik, polskie ustawienia): liczby z przecinkiem dziesiętnym; tekst zaczynający się od =, +, -, @
        (nazwy z publicznych ogłoszeń) poprzedzony apostrofem – Excel nie wykona go jako formuły."""
        if v is None:
            return ""
        if isinstance(v, bool):
            return "tak" if v else "nie"
        if isinstance(v, float):
            return (f"{v:.2f}" if abs(v - round(v)) > 1e-9 else str(int(round(v)))).replace(".", ",")
        v = str(v)
        return "'" + v if v[:1] in ("=", "+", "-", "@", "\t", "\r") else v
    for x in L:
        w.writerow([kom(x.get(k)) for k in kol])
    return S.Response("\ufeff" + b.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename=leady_{typ}_{dt.date.today():%Y%m%d}.csv"})
