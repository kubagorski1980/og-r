# -*- coding: utf-8 -*-
"""
Sprawdzenie ofert – trasy: lista i dane oceny, dokumenty i oferty, odczyt SWZ / zapytania i badanie ofert (AI), kryteria, rynkowość cen, dokumenty (protokół, informacja, wezwanie), weryfikacja wykonawców i referencji.
Blueprint „ocena” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import reguly_zamowien as RZ
import serwer as S

bp = Blueprint("ocena", __name__)


def _wer_dane_wyk(dane, krs):
    """Dane wykonawcy do oceny referencji: data powstania z KRS (data wpisu), data rejestracji VAT, adres, zarząd."""
    d_krs = (krs or {}).get("data_rejestracji")
    d_vat = S.WER._data((dane or {}).get("data_rejestracji_vat"))
    return {"nip": (dane or {}).get("nip") or "", "nazwa": (dane or {}).get("nazwa") or "", "adres": (dane or {}).get("adres") or "",
            "data_powstania": d_krs, "zrodlo_daty": "data wpisu do KRS" if d_krs else "", "data_rejestracji_vat": d_vat,
            "zarzad": ((krs or {}).get("zarzad") or []) + ((dane or {}).get("reprezentanci") or [])}


def _wer_przelicz(o):
    """Ponowne wyliczenie sygnałów z zapisanych danych (bez zapytań do rejestrów) – np. po wpisaniu odpowiedzi wystawcy."""
    W = o.get("weryfikacja") or {}
    wyk = dict(W.get("wykonawca") or {})
    for k in ("data_powstania", "data_rejestracji_vat"):
        wyk[k] = S.WER._data(wyk.get(k)) if wyk.get(k) else None
    refs = W.get("wejscie") or []
    bzp = {i: r.get("_bzp") or [] for i, r in enumerate(refs)}
    md = {k: {**v, "utworzono": S.WER._data(v.get("utworzono")) if v.get("utworzono") else None} for k, v in (W.get("metadane") or {}).items()}
    W["referencje"] = S.WER.ocen_referencje(wyk, refs, md, bzp)
    W["podsumowanie"] = {s_: sum(1 for r in W["referencje"] if r["status"] == s_) for s_ in S.WER.STATUSY}
    o["weryfikacja"] = W


def _warunki_kreatora(zid):
    """Warunki udziału obowiązujące w zamówieniu z kreatora – efektywne, tak jak liczy je kreator: propozycja programu dla wartości i trybu
    + pola zmienione przez zamawiającego (po ZAM-05 niezmienione pola nie są zapisywane w K["warunki"]). Pusty tekst – brak / błąd."""
    if not zid:
        return ""
    try:
        import trasy_kreator as TK
        return str(((TK._kreator_stan(zid).get("warunki") or {}).get("warunki")) or "").strip()
    except Exception:  # zamówienie usunięte / uszkodzone – ocena bierze warunki z SWZ jak dotąd
        return ""


def praca_weryfikacja_oferty(log, pid, oid):
    """Wykonawca w rejestrach (wykaz VAT, KRS), wystawcy referencji, ogłoszenia o wyniku w BZP i metadane plików – sygnały do sprawdzenia."""
    m = S.meta(pid)
    O = ocena_dane(m)
    o = next((x for x in O["oferty"] if x.get("id") == oid), None)
    if not o:
        raise ValueError("Nie ma takiej oferty.")
    w = o.get("wynik") or {}
    refs = [dict(r) for r in (w.get("referencje") or []) if isinstance(r, dict)]
    if not refs:
        raise ValueError("Program nie odczytał referencji z tej oferty – najpierw sprawdź ofertę (krok badania ofert), a jeżeli wykonawca nie złożył "
                         "wykazu robót lub referencji, poproś o nie.")
    stare = {(S.WER._norm(r.get("wystawca")), str(r.get("data_do") or "")): r.get("odpowiedz") for r in ((o.get("weryfikacja") or {}).get("wejscie") or [])}
    cache = S.czytaj(S.F_NIP_CACHE, {})
    token = S.cfg_surowy().get("ceidg_token")
    nip_w = o.get("nip") or w.get("wykonawca_nip") or ""
    dane_w, krs_w = {}, {}
    if nip_w:
        log(f"Wykonawca {o.get('nazwa')}: wykaz podatników VAT i KRS…")
        dane_w, bl = S.NIP.szukaj(nip_w, cache, ceidg_token=token)
        if bl:
            log(f"Wykonawca – rejestr: {bl}")
            dane_w = {"nip": nip_w, "adres": w.get("wykonawca_adres") or ""}
        elif dane_w.get("krs"):
            krs_w = S.WER.krs_dane(dane_w["krs"])
    else:
        log("W ofercie nie odczytano NIP wykonawcy – data powstania firmy nie zostanie sprawdzona.")
    wyk = _wer_dane_wyk(dane_w or {"adres": w.get("wykonawca_adres") or ""}, krs_w)
    zapytan = 0
    for i, r in enumerate(refs[:15]):
        r["odpowiedz"] = stare.get((S.WER._norm(r.get("wystawca")), str(r.get("data_do") or ""))) or ""
        rn = S.WER._nip(r.get("nip_wystawcy"))
        if rn and zapytan < 10:
            zapytan += 1
            dane_r, bl = S.NIP.szukaj(rn, cache, ceidg_token=token)
            r["wystawca_rejestr"] = {"blad": bl} if bl else {k: dane_r.get(k) for k in ("nazwa", "adres", "krs", "reprezentanci")}
            if not bl and dane_r.get("krs") and zapytan <= 6:
                r["wystawca_rejestr"]["zarzad"] = S.WER.krs_dane(dane_r["krs"]).get("zarzad") or []
        if r.get("wystawca") and not S.HZ.rodzaj_zamawiajacego(r["wystawca"]).startswith(("Firma", "Inny", "Wspólnota", "Spółdzielnia", "Inna")) and i < 6:
            log(f"BZP: ogłoszenia o wyniku – {r['wystawca'][:60]}…")
            try:
                wyn = S.HZ.pobierz_wyniki(r["wystawca"], lambda *a: None, miesiecy=72, nip=rn)
                nz = S.WER._norm(o.get("nazwa"))[:12]
                r["_bzp"] = [{"data": x.get("data") or "", "przedmiot": x.get("przedmiot") or x.get("nazwa") or ""} for x in wyn
                             if (nip_w and S.WER._nip(x.get("nip")) == S.WER._nip(nip_w)) or (nz and nz in S.WER._norm(x.get("wykonawca")))][:3]
                r["_bzp_sprawdzono"] = True
            except Exception as e:
                log(f"BZP niedostępne ({str(e)[:60]}) – pomijam.")
    S.pisz(S.F_NIP_CACHE, cache)
    kat = os.path.join(S.pdir(pid), "oferty", oid)
    md = {}
    for f in sorted(os.listdir(kat)) if os.path.isdir(kat) else []:
        x = S.WER.metadane_pliku(os.path.join(kat, f))
        x["oferta"] = bool(re.search(r"ofert|formularz", f, re.I))
        if x.get("utworzono"):
            x["utworzono"] = x["utworzono"].isoformat()
        md[f] = x
    mz = S.zamowienie_powiazane(m)
    Kz = mz.get("kreator") or {}
    w_ef = _warunki_kreatora(m.get("zamowienie_id") if mz is not m else pid) if Kz else ""
    warunki_ = w_ef or " ".join(str(x) for x in (((Kz.get("warunki") or {}).get("warunki")) or "", (O.get("swz") or {}).get("warunki_udzialu") or "", (RZ.reguly(Kz.get("prywatny")).warunki(Kz.get("rodzaj") or "roboty", Kz) or {}).get("warunki", "")
                                          if not (Kz.get("warunki") or {}).get("warunki") else ""))
    sw_, dosl_, spr_ = S.WER.ocen_wykonawce(wyk, dane_w, krs_w, w, f"{mz.get('nazwa') or ''} {Kz.get('opis') or ''}", mz.get("rodzaj_zamowienia") or Kz.get("rodzaj") or "roboty",
                                          warunki_, (Kz.get("potrzeba") or {}).get("termin") or (Kz.get("potrzeba") or {}).get("okres") or (Kz.get("umowa") or {}).get("termin"),
                                          podobienstwo=S.HZ.podobienstwo)
    W = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wejscie": refs, "metadane": md,
         "wykonawca_sygnaly": sw_, "do_doslania": dosl_, "do_sprawdzenia": spr_,
         "potwierdzenia": ((o.get("weryfikacja") or {}).get("potwierdzenia") or {}),
         "wykonawca": {**wyk, "data_powstania": wyk["data_powstania"].isoformat() if wyk["data_powstania"] else "",
                       "data_rejestracji_vat": wyk["data_rejestracji_vat"].isoformat() if wyk["data_rejestracji_vat"] else ""}}
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        o = next((x for x in O["oferty"] if x.get("id") == oid), None)
        o["weryfikacja"] = W
        _wer_przelicz(o)
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    p_ = o["weryfikacja"]["podsumowanie"]
    log(f"Gotowe: {len(refs)} referencji – potwierdzone {p_['potwierdzona']}, z sygnałami nieprawdziwości {p_['sprzeczna']}, niepotwierdzone {p_['niepotwierdzona']}.")


@bp.post("/api/projekty/<pid>/ocena/<oid>/weryfikacja")
@S.wymaga_logowania
def ocena_weryfikacja(pid, oid):
    return jsonify(S.uruchom("ocena_ofert", "Weryfikacja wykonawcy i referencji", praca_weryfikacja_oferty, pid, oid))


@bp.post("/api/projekty/<pid>/ocena/<oid>/potwierdzenie")
@S.wymaga_logowania
def ocena_potwierdzenie(pid, oid):
    """Wynik sprawdzenia w rejestrze bez interfejsu do automatycznych zapytań (e-CRUB – uprawnienia, KRZ) – zapisany przez użytkownika."""
    j = request.json or {}
    if j.get("pole") not in ("uprawnienia", "krz") or j.get("wynik") not in ("", "potwierdzone", "zastrzezenia"):
        return jsonify({"blad": "Nieprawidłowe dane."}), 400
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        o = next((x for x in O["oferty"] if x.get("id") == oid), None)
        if not o or not o.get("weryfikacja"):
            return jsonify({"blad": "Najpierw sprawdź wykonawcę."}), 400
        o["weryfikacja"].setdefault("potwierdzenia", {})[j["pole"]] = {"wynik": j["wynik"], "notatka": str(j.get("notatka") or "")[:300],
                                                                       "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "kto": session.get("login") or ""}
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    return jsonify(o["weryfikacja"])


@bp.post("/api/projekty/<pid>/ocena/<oid>/referencja")
@S.wymaga_logowania
def ocena_referencja(pid, oid):
    """Odpowiedź wystawcy referencji (wysłano zapytanie / potwierdził / zaprzeczył / brak odpowiedzi) i notatka."""
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        o = next((x for x in O["oferty"] if x.get("id") == oid), None)
        refs = ((o or {}).get("weryfikacja") or {}).get("wejscie") or []
        i = int(j.get("i", -1)) if str(j.get("i", "")).lstrip("-").isdigit() else -1
        if not (0 <= i < len(refs)) or j.get("odpowiedz") not in S.WER.ODPOWIEDZI:
            return jsonify({"blad": "Nieprawidłowa referencja albo odpowiedź."}), 400
        refs[i]["odpowiedz"] = j["odpowiedz"]
        refs[i]["notatka"] = str(j.get("notatka") or refs[i].get("notatka") or "")[:500]
        _wer_przelicz(o)
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    return jsonify(o["weryfikacja"])


@bp.get("/api/projekty/<pid>/ocena/<oid>/referencja/<int:i>/zapytanie")
@S.wymaga_logowania
def ocena_referencja_zapytanie(pid, oid, i):
    m = S.meta(pid)
    O = ocena_dane(m)
    o = next((x for x in O["oferty"] if x.get("id") == oid), None)
    refs = ((o or {}).get("weryfikacja") or {}).get("wejscie") or []
    if not (0 <= i < len(refs)):
        return jsonify({"blad": "Nie ma takiej referencji."}), 404
    mz = S.zamowienie_powiazane(m)
    zam = ((mz.get("kreator") or {}).get("zamawiajacy") or (O.get("swz") or {}).get("zamawiajacy") or "").strip()
    return jsonify({"tresc": S.WER.zapytanie_do_wystawcy(refs[i], o.get("nazwa") or "", zam, (O.get("swz") or {}).get("nazwa_zamowienia") or m.get("nazwa") or ""),
                    "email": refs[i].get("kontakt_email") or ""})


def _unijne(m, swz):
    """Od progów UE? Z kreatora zamówienia, z którego powstała ocena (wartość), inaczej z trybu w SWZ."""
    zid = m.get("zamowienie_id")
    if zid and os.path.isfile(os.path.join(S.PROJ, str(zid), "projekt.json")):
        try:
            import trasy_kreator as TK
            P = TK._kreator_stan(zid).get("postepowanie")
            if P:
                return bool(P["unijne"])
        except Exception:
            pass
    return S.OO.unijne(swz)


def ocena_dane(m):
    """Dane badania ofert – brakujące elementy (np. dane niepełne ze starszej wersji albo importu) uzupełniane, żeby widok się nie wywracał."""
    d = m.get("ocena") or {}
    if not isinstance(d, dict):
        d = {}
    d.setdefault("swz", {})
    if not isinstance(d["swz"], dict):
        d["swz"] = {}
    if S.projekt_wspolnoty(m):  # wspólnota / spółdzielnia / deweloper – ocena, protokół i informacja bez Pzp
        d["swz"]["prywatny"] = True
        d["swz"]["podmiot"] = str((S.zamowienie_powiazane(m).get("kreator") or {}).get("podmiot") or "wspolnota")  # podpisy pod protokołem (H3-07)
    d.setdefault("oferty", [])
    d.setdefault("podsum", {})
    for i, o in enumerate(d["oferty"]):
        if isinstance(o, dict) and not o.get("id"):
            o["id"] = f"oferta{i + 1}"
    return d


@bp.get("/api/ocena-ofert")
@S.wymaga_logowania
def ocena_lista():
    wyn, login, rola = [], session.get("login"), S.rola_sesji()
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if m and m.get("typ") == "ocena_ofert" and S.ma_dostep(m, login, rola, lista=True) and not m.get("archiwum") \
                and (m.get("strona") == "prawnik") == (request.args.get("strona") == "prawnik") and S.zgodny_modul(m, request.args.get("modul")):
            O = ocena_dane(m)
            naj = next((o for o in O["oferty"] if o.get("id") == (O.get("podsum") or {}).get("najkorzystniejsza")), None)
            wyn.append({"id": pid, "nazwa": m.get("nazwa"), "utworzono": m.get("utworzono"), "ofert": len(O["oferty"]), "najkorzystniejsza": (naj or {}).get("nazwa"),
                        "naj_nip": (naj or {}).get("nip"), "naj_adres": (naj or {}).get("adres"), "naj_cena_netto": (naj or {}).get("cena_netto"), "naj_cena_brutto": (naj or {}).get("cena_brutto"),
                        "warunkowo": bool(S.OO.wstrzymany_wybor(O["oferty"], O.get("podsum") or {}))})
    return jsonify(sorted(wyn, key=lambda x: x.get("utworzono") or "", reverse=True))


@bp.get("/api/projekty/<pid>/ocena")
@S.wymaga_logowania
def ocena_pobierz(pid):
    m = S.meta(pid)
    O = ocena_dane(m)
    swz_pl = sorted(f for _, _, fs in os.walk(os.path.join(S.pdir(pid), "dokumenty")) for f in fs)
    for o in O["oferty"]:
        k = os.path.join(S.pdir(pid), "oferty", o["id"])
        o["pliki"] = sorted(f for _, _, fs in os.walk(k) for f in fs) if os.path.isdir(k) else []
    kat = os.path.join(S.pdir(pid), "ocena")
    return jsonify({"projekt": {"id": pid, "nazwa": m.get("nazwa"), "zapytanie_id": m.get("zapytanie_id"), "strona": m.get("strona"),
                                "z_kreatora": bool(m.get("zamowienie_id")), "punkty_226": S.OO.PUNKTY_226,
                                "prawnik": S.PRW.ustawienia(m) if m.get("strona") == "prawnik" else None, "prawnik_oferty": m.get("prawnik_oferty") or {}}, "O": O, "swz_pliki": swz_pl,
                    "dokumenty": sorted(os.listdir(kat)) if os.path.isdir(kat) else []})


STATUSY_OFERTY = ("prawidłowa", "do wyjaśnienia", "do uzupełnienia", "do odrzucenia")


def _wynik_reczny(w):
    """Wpis komisji (bez AI): cena brutto, wartości kryteriów pozacenowych, ocena oferty. Pozostałe pola wyniku badania AI bez zmian."""
    wyn = {}
    if "cena_brutto" in w:
        wyn["cena_brutto"] = S.OO._f(w["cena_brutto"])
    if isinstance(w.get("wartosci_kryteriow"), dict):
        wyn["wartosci_kryteriow"] = {str(k)[:80]: S.OO._f(v) for k, v in w["wartosci_kryteriow"].items() if str(v).strip() != ""}
    if "wyjasnione" in w:  # wyjaśnienia / uzupełnienia przyjęte przez komisję (np. cena – art. 224) – zdejmuje znacznik rażąco niskiej ceny
        wyn["wyjasnione"] = bool(w["wyjasnione"])
    if w.get("status") in STATUSY_OFERTY:
        wyn["status"] = w["status"]
    elif w.get("status") == "":
        wyn["status"] = None
    if "podstawa_odrzucenia" in w:  # uzasadnienie faktyczne i prawne odrzucenia wpisane przez komisję (art. 253 ust. 1 pkt 2)
        wyn["podstawa_odrzucenia"] = str(w.get("podstawa_odrzucenia") or "").strip()[:1000]
    if "punkt_226" in w:
        p_ = str(w.get("punkt_226") or "").strip().lower()
        wyn["punkt_226"] = p_ if p_ in S.OO.PUNKTY_226 else ""
    if wyn:
        wyn["wpis_komisji"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return wyn


def _odrzucenie(o, j, O):
    """Odrzucenie oferty przez komisję – wymagane uzasadnienie faktyczne i (Pzp) podstawa prawna: punkt art. 226 ust. 1 albo przepis w treści.
    Przywrócenie oferty usuwa podstawę wpisaną przez komisję. Zwraca komunikat błędu albo pusty tekst."""
    w = j.get("wynik") if isinstance(j.get("wynik"), dict) else {}
    if not bool(j["odrzucona"]):
        o["odrzucona"] = False
        if (o.get("wynik") or {}).get("odrzucenie_komisji"):
            for k in ("podstawa_odrzucenia", "punkt_226", "odrzucenie_komisji"):
                o["wynik"].pop(k, None)
        return ""
    pryw = bool((O.get("swz") or {}).get("prywatny"))
    tekst = str(w.get("podstawa_odrzucenia") if "podstawa_odrzucenia" in w else j.get("podstawa_odrzucenia") or "").strip()
    punkt = str(w.get("punkt_226") if "punkt_226" in w else j.get("punkt_226") or "").strip().lower()
    if punkt and punkt not in S.OO.PUNKTY_226:
        return "Nieprawidłowy punkt art. 226 ust. 1 – wybierz z listy (1, 2a–2c, 3–5, 5a, 6–19)."
    if len(tekst) < 5:
        return ("Podaj uzasadnienie odrzucenia oferty – trafi do informacji o wyborze." if pryw else
                "Podaj podstawę prawną (punkt art. 226 ust. 1 Pzp) i uzasadnienie faktyczne odrzucenia oferty – trafią do informacji o wyborze "
                "(art. 253 ust. 1 pkt 2 Pzp).")
    if not pryw and not punkt and not re.search(r"art\.\s*\d+", tekst):
        return "Wskaż podstawę prawną odrzucenia – punkt art. 226 ust. 1 Pzp."
    o["odrzucona"] = True
    o["wynik"] = {**(o.get("wynik") or {}), "podstawa_odrzucenia": tekst[:1000], "punkt_226": punkt, "odrzucenie_komisji": True,
                  "wpis_komisji": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
    if isinstance(j.get("wynik"), dict):  # już zapisane powyżej – bez ponownego nadpisania pustym tekstem
        j["wynik"] = {k: v for k, v in j["wynik"].items() if k not in ("podstawa_odrzucenia", "punkt_226")}
    return ""


@bp.post("/api/projekty/<pid>/ocena/oferta")
@S.wymaga_logowania
def ocena_oferta(pid):
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        if j.get("usun"):
            O["oferty"] = [o for o in O["oferty"] if o["id"] != j["usun"]]
            S.shutil.rmtree(os.path.join(S.pdir(pid), "oferty", S.DOT.bezpieczna(j["usun"])), ignore_errors=True)
        elif j.get("id"):
            for o in O["oferty"]:
                if o["id"] == j["id"]:
                    for k in ("nazwa", "nip", "nr", "data_zlozenia", "adres"):
                        if k in j:
                            o[k] = str(j[k])[:200]
                    if "odrzucona" in j:
                        bl = _odrzucenie(o, j, O)
                        if bl:
                            return jsonify({"blad": bl}), 400
                    if isinstance(j.get("wynik"), dict):
                        o["wynik"] = {**(o.get("wynik") or {}), **_wynik_reczny(j["wynik"])}
        else:
            nazwa = str(j.get("nazwa") or "").strip()
            if not nazwa:
                return jsonify({"blad": "Podaj nazwę wykonawcy."}), 400
            nr_ = max([int(o["nr"]) for o in O["oferty"] if str(o.get("nr", "")).isdigit()] or [0]) + 1  # numer unikalny także po usunięciu oferty
            O["oferty"].append({"id": uuid.uuid4().hex[:8], "nr": str(nr_), "nazwa": nazwa[:200], "nip": str(j.get("nip") or "")[:20],
                                "adres": str(j.get("adres") or "")[:200],
                                "data_zlozenia": str(j.get("data_zlozenia") or dt.date.today().isoformat())[:16]})
        if O["oferty"] and any(o.get("wynik") for o in O["oferty"]):
            O["podsum"] = S.OO.ranking(O.get("swz") or {}, O["oferty"])
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/ocena/plik")
@S.wymaga_logowania
def ocena_plik(pid):
    """Pliki oferty wykonawcy (ZIP rozpakowywany automatycznie)."""
    import zipfile
    oid = S.DOT.bezpieczna(request.form.get("id", ""))
    kat = os.path.join(S.pdir(pid), "oferty", oid)
    os.makedirs(kat, exist_ok=True)
    for f in request.files.getlist("pliki"):
        p = os.path.join(kat, S.secure_filename_pl(f.filename))
        f.save(p)
        if p.lower().endswith(".zip"):
            try:
                with zipfile.ZipFile(p) as z:
                    for n in z.namelist():
                        if not n.endswith("/") and ".." not in n:
                            with z.open(n) as zr, open(os.path.join(kat, S.secure_filename_pl(os.path.basename(n))), "wb") as zw:
                                zw.write(zr.read())
                os.remove(p)
            except zipfile.BadZipFile:
                pass
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/ocena/swz")
@S.wymaga_logowania
def ocena_swz(pid):
    return jsonify(S.uruchom("ocena_swz", "Kryteria i wymagania z SWZ", praca_ocena_swz, pid))


def praca_ocena_swz(log, pid):
    c = S.cfg()
    S.wymagany_klucz(c)
    bloki = S._bloki_z(os.path.join(S.pdir(pid), "dokumenty"))
    if not bloki:
        raise ValueError("Najpierw wgraj dokumenty postępowania (SWZ, OPZ, formularze).")
    log("AI odczytuje z SWZ kryteria oceny, wymagane dokumenty i warunki…")
    R = RZ.reguly(S.projekt_wspolnoty(S.meta(pid)))
    pryw_ = R.prywatny
    txt, _ = S.MO.claude_stream(c, R.system_swz, S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c))
                              + [{"type": "text", "text": R.polecenie_swz}],
                              max_tokens=6000, log=log)
    swz = S.MO.wyciagnij_json(txt)
    if not isinstance(swz, dict) or not swz.get("kryteria"):
        raise ValueError("Nie udało się odczytać kryteriów oceny – sprawdź, czy wgrano SWZ.")
    mo = S.meta(pid)
    mz = S.zamowienie_powiazane(mo)
    kc = S.KZ.czesci_normalizuj((mz.get("kreator") or {}).get("czesci"))  # podział z kreatora zamówienia, gdy SWZ go nie opisuje wprost
    if kc["podzial"] and len(kc["lista"]) >= 2 and not [x for x in (swz.get("czesci") or []) if isinstance(x, dict)]:
        swz["czesci"] = [{"nr": x["nr"], "nazwa": x["nazwa"]} for x in kc["lista"]]
        swz["limit_czesci_dla_wykonawcy"] = swz.get("limit_czesci_dla_wykonawcy") or kc["max_udzielen"]
    if [x for x in (swz.get("czesci") or []) if isinstance(x, dict)]:
        log(f"Zamówienie podzielone na {len(swz['czesci'])} części – oferty będą oceniane osobno w każdej części.")
    swz["prywatny"] = bool(pryw_)
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        O["swz"] = swz
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    log(f"Gotowe: {len(swz['kryteria'])} kryteriów, {len(swz.get('wymagane_dokumenty') or [])} wymaganych dokumentów.")
    return {"kryteria": len(swz["kryteria"])}


def _kryterium(k):
    """Kryterium z edycji komisji: zakres punktowania od–do (typ „wyższa”) zachowany; opis wygenerowany przez program odświeżany po zmianie."""
    typ = k.get("typ") if k.get("typ") in ("min", "max", "punktowe") else "min"
    w = {"nazwa": str(k.get("nazwa") or "")[:80], "waga": S.OO._f(k.get("waga")) or 0, "typ": typ}
    if isinstance(k.get("cena"), bool):  # jawne oznaczenie kryterium ceny (odczyt SWZ) – zachowane
        w["cena"] = k["cena"]
    od, do = S.OO._f(k.get("od")), S.OO._f(k.get("do"))
    if typ == "max" and od is not None and do is not None and do > od:
        w["od"], w["do"] = od, do
    opis = str(k.get("opis") or "").strip()
    w["opis"] = (S.OO.opis_kryterium(w) if not opis or opis.startswith("liczba punktów =") or opis.startswith("punkty przyznane według")
                 or "sprawdź z SWZ" in opis else opis)[:400]
    return w


@bp.post("/api/projekty/<pid>/ocena/kryteria")
@S.wymaga_logowania
def ocena_kryteria(pid):
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        swz = O.get("swz") or {}
        if isinstance(j.get("kryteria"), list):
            swz["kryteria"] = [_kryterium(k) for k in j["kryteria"] if isinstance(k, dict) and str(k.get("nazwa") or "").strip()]
        if "kwota_budzet_brutto" in j and S.OO._f(j["kwota_budzet_brutto"]) != S.OO._f(swz.get("kwota_budzet_brutto")):
            swz["kwota_budzet_brutto"] = S.OO._f(j["kwota_budzet_brutto"])
            swz.pop("zwiekszona_kwota", None)  # kwota zmieniona ręcznie – wcześniejsza decyzja nieaktualna
        if j.get("zwieksz_kwote"):  # art. 255 pkt 3 – decyzja: zwiększenie kwoty do ceny najkorzystniejszej oferty
            pod = S.OO.ranking(swz, O["oferty"]) if O["oferty"] else {}
            naj = next((o for o in O["oferty"] if o.get("id") == pod.get("najkorzystniejsza")), None)
            c = S.OO._f(((naj or {}).get("wynik") or {}).get("cena_brutto"))
            if not naj or not c or not naj.get("ponad_budzet"):
                return jsonify({"blad": "Cena najkorzystniejszej oferty nie przekracza kwoty na sfinansowanie – nie ma czego zwiększać."}), 400
            swz["zwiekszona_kwota"] = {"z": swz.get("kwota_budzet_brutto"), "do": c, "data": dt.date.today().isoformat(), "kto": session.get("login") or ""}
            swz["kwota_budzet_brutto"] = c
        O["swz"] = swz
        if O["oferty"]:
            O["podsum"] = S.OO.ranking(swz, O["oferty"])
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/ocena/sprawdz")
@S.wymaga_logowania
def ocena_sprawdz(pid):
    return jsonify(S.uruchom("ocena_ofert", "Sprawdzenie i ocena ofert", praca_ocena_ofert, pid, (request.json or {}).get("ids")))


def praca_ocena_ofert(log, pid, ids=None):
    """Każda oferta: dokumenty postępowania (w pamięci podręcznej – czytane taniej przy kolejnych ofertach) + pliki oferty → wynik badania.
    Na końcu punktacja według kryteriów i ranking."""
    c = S.cfg()
    S.wymagany_klucz(c)
    m = S.meta(pid)
    O = ocena_dane(m)
    if not O.get("swz", {}).get("kryteria"):
        praca_ocena_swz(log, pid)
        m = S.meta(pid)
        O = ocena_dane(m)
    swz_bloki = S.MO.oznacz_dokumenty(S._bloki_z(os.path.join(S.pdir(pid), "dokumenty")), S.MO.ustawienie_cache(c))
    do_spr = [o for o in O["oferty"] if not ids or o["id"] in ids]
    if not do_spr:
        raise ValueError("Dodaj złożone oferty (krok 3).")
    c2 = dict(c, _model=c.get("model_dokladny") or "claude-opus-5-5")
    for i, o in enumerate(do_spr, 1):
        ob = S._bloki_z(os.path.join(S.pdir(pid), "oferty", o["id"]))
        if not ob:
            log(f"Oferta {i}/{len(do_spr)} ({o['nazwa']}): brak plików – pomijam.")
            continue
        log(f"Badanie oferty {i}/{len(do_spr)}: {o['nazwa']}")
        tresc = swz_bloki + [{"type": "text", "text": "=== PONIŻEJ: DOKUMENTY OFERTY ==="}] + ob + [{"type": "text", "text": S.OO.polecenie_oferty(O["swz"], o["nazwa"])}]
        try:
            txt, _ = S.MO.claude_stream(c2, RZ.reguly((O.get("swz") or {}).get("prywatny")).system_oferta, tresc, max_tokens=8000, log=log)
            w = S.MO.wyciagnij_json(txt)
        except Exception as e:
            log(f"Nie udało się zbadać oferty {o['nazwa']}: {e}")
            continue
        if isinstance(w, dict):
            w["data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            for kl in ("braki", "niezgodnosci", "bledy_rachunkowe", "do_wyjasnienia"):  # cytaty z SWZ i z oferty sprawdzone w plikach
                w[kl] = [x if isinstance(x, dict) else {"opis": str(x)} for x in (w.get(kl) or [])]
                S.OD.dodaj(S.pdir(pid), w[kl], katalogi=("dokumenty", f"oferty/{o['id']}"))
            with S.BLOKADA:
                m = S.meta(pid)
                O = ocena_dane(m)
                for x in O["oferty"]:
                    if x["id"] == o["id"]:
                        x["wynik"] = w
                m["ocena"] = O
                S.zapisz_meta(pid, m)
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        O["podsum"] = S.OO.ranking(O.get("swz") or {}, O["oferty"])
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    naj = next((o for o in O["oferty"] if o["id"] == O["podsum"].get("najkorzystniejsza")), None)
    log(f"Gotowe. Najkorzystniejsza oferta: {naj['nazwa'] + ' (' + S.PR.liczba_pl(naj['punkty'], 2) + ' pkt)' if naj else 'brak ofert nieodrzuconych'}.")
    return {"najkorzystniejsza": (naj or {}).get("nazwa")}


@bp.post("/api/projekty/<pid>/ocena/wartosc")
@S.wymaga_logowania
def ocena_wartosc(pid):
    """Wartość zamówienia z VAT ustalona przed wszczęciem – podstawa progu z art. 224 ust. 2 pkt 1 Pzp."""
    w = S.RY._f((request.json or {}).get("wartosc_brutto"))
    with S.BLOKADA:
        m = S.meta(pid)
        O = ocena_dane(m)
        O.setdefault("swz", {})["wartosc_zam_brutto"] = w
        O["swz"]["wartosc_zam_reczna"] = True  # wartość z VAT potwierdzona przez zamawiającego (nie netto × 1,23 z kreatora)
        if O["oferty"]:
            O["podsum"] = S.OO.ranking(O["swz"], O["oferty"])
        m["ocena"] = O
        S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/ocena/rynkowosc")
@S.wymaga_logowania
def ocena_rynkowosc(pid):
    j = request.json or {}
    return jsonify(S.uruchom("rynkowosc", "Rynkowość cen ofert", S.praca_rynkowosc, pid, j.get("ids") or None, bool(j.get("wszystkie"))))


@bp.post("/api/projekty/<pid>/ocena/prawnik/<co>")
@S.wymaga_logowania
def ocena_prawnik(pid, co):
    if S.meta(pid).get("strona") != "prawnik" or co not in ("raport", "opinia", "odwolanie"):
        return jsonify({"blad": "Dostępne w sprawie prawnika: raport, opinia, odwołanie."}), 400
    return jsonify(S.uruchom("prawnik", {"raport": "Raport z badania ofert", "opinia": "Opinia prawna (oferty)", "odwolanie": "Projekt odwołania do KIO"}[co],
                           S.praca_prawnik_oferty, pid, co))


@bp.post("/api/projekty/<pid>/ocena/dokument")
@S.wymaga_logowania
def ocena_dokument(pid):
    j = request.json or {}
    m = S.meta(pid)
    O = ocena_dane(m)
    if O["oferty"]:
        O["podsum"] = S.OO.ranking(O.get("swz") or {}, O["oferty"])
    kat = os.path.join(S.pdir(pid), "ocena")
    os.makedirs(kat, exist_ok=True)
    zam = (O.get("swz") or {}).get("zamawiajacy") or "[UZUPEŁNIJ: zamawiający]"  # z SWZ – nigdy z Profilu firmy
    rodz = j.get("rodzaj")
    if rodz == "protokol":
        nazwa = "Protokol_z_badania_i_oceny_ofert.docx"
        S.OO.protokol_docx(os.path.join(kat, nazwa), O.get("swz") or {}, O["oferty"], O["podsum"], zam)
    elif rodz == "informacja":
        bl = S.OO.blokada_informacji(O.get("swz") or {}, O["oferty"], O["podsum"] or {})
        if bl:  # art. 253 – rozstrzygnięcie oferty najwyżej ocenionej; art. 255 pkt 1–3 – brak oferty do wyboru albo cena ponad kwotę
            return jsonify({"blad": bl}), 400
        nazwa = "Informacja_o_wyborze_najkorzystniejszej_oferty.docx"
        S.OO.informacja_docx(os.path.join(kat, nazwa), O.get("swz") or {}, O["oferty"], O["podsum"], zam)
    elif rodz == "wezwanie224":
        o = next((x for x in O["oferty"] if x["id"] == j.get("id")), None)
        if not o or not o.get("rynkowosc"):
            return jsonify({"blad": "Najpierw sprawdź rynkowość ceny tej oferty."}), 400
        nazwa = f"Wezwanie_art_224_{S.DOT.bezpieczna(o['nazwa'])[:40]}.docx"
        S.RY.wezwanie_224_docx(os.path.join(kat, nazwa), m.get("nazwa", ""), zam, o, o["rynkowosc"])
    elif rodz == "otwarcie":
        nazwa = "Informacja_z_otwarcia_ofert.docx"
        S.OO.informacja_otwarcia_docx(os.path.join(kat, nazwa), O.get("swz") or {}, O["oferty"], zam)
    elif rodz == "srodki":  # wykonawca najwyżej oceniony (albo wskazany) – art. 126 ust. 1 / art. 274 ust. 1
        oid = j.get("id") or (O.get("podsum") or {}).get("pierwsza_w_rankingu")
        o = next((x for x in O["oferty"] if x["id"] == oid), None)
        if not o:
            return jsonify({"blad": "Najpierw oceń oferty – wezwanie dotyczy oferty najwyżej ocenionej."}), 400
        nazwa = f"Wezwanie_podmiotowe_srodki_{S.DOT.bezpieczna(o['nazwa'])[:40]}.docx"
        S.OO.wezwanie_srodki_docx(os.path.join(kat, nazwa), O.get("swz") or {}, o, zam, _unijne(m, O.get("swz") or {}))
    elif rodz == "wezwanie":
        o = next((x for x in O["oferty"] if x["id"] == j.get("id")), None)
        if not o:
            return jsonify({"blad": "Nie znaleziono oferty."}), 404
        nazwa = f"Wezwanie_{S.DOT.bezpieczna(o['nazwa'])[:40]}.docx"
        S.OO.wezwanie_docx(os.path.join(kat, nazwa), O.get("swz") or {}, o, zam)
    else:
        return jsonify({"blad": "Nieznany dokument."}), 400
    sc = f"ocena/{nazwa}"
    return jsonify({"plik": sc, "url": f"/pobierz/{pid}/{S.urllib.parse.quote(sc)}"})
