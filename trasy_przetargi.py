# -*- coding: utf-8 -*-
"""
Przetargi wykonawcy – trasy: wyszukiwanie i lista przetargów, statusy, analiza i ocena, słowa kluczowe, obszar, monitoring stron BIP, raporty zwycięzców, historia zamawiającego.
Blueprint „przetargi” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("przetargi", __name__)


def _j():
    """Treść żądania JSON jako słownik (pusta, uszkodzona albo inna niż obiekt → {} zamiast błędu 500)."""
    j = request.get_json(silent=True)
    return j if isinstance(j, dict) else {}


def _numery(v):
    """Lista numerów przetargów z żądania – tylko napisy (inne wartości pomijane)."""
    return [x for x in v if isinstance(x, str) and x] if isinstance(v, list) else []


@bp.get("/api/obszar")
@S.wymaga_logowania
def obszar_get():
    c = S.cfg()
    return jsonify({"obszar": c.get("obszar"), "wojewodztwa": list(S.WOJEWODZTWA), "opis": S.opis_obszaru(c.get("obszar"), c),
                    "centrum": c.get("centrum_nazwa"), "centrum_opis": c.get("centrum_opis", ""), "promien": c.get("promien_km"),
                    "promienie": list(S.REG.PROMIENIE), "miejscowosci": [m[0] for m in (c.get("miejscowosci") or [])][:400]})


@bp.get("/api/obszar/szukaj")
@S.wymaga_logowania
def obszar_szukaj():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify([])
    try:
        return jsonify(S.REG.szukaj_miejscowosci(q))
    except Exception as e:
        return jsonify({"blad": f"Nie udało się wyszukać miejscowości ({e})."}), 502


@bp.post("/api/obszar")
@S.wymaga_logowania
def obszar_zapisz():
    j = _j()
    ob = {"tryb": j.get("tryb", "promien"), "wojewodztwa": [w for w in j.get("wojewodztwa", []) if w in S.WOJEWODZTWA]}
    if ob["tryb"] not in ("polska", "wojewodztwa", "promien"):
        return jsonify({"blad": "Nieznany obszar"}), 400
    if ob["tryb"] == "wojewodztwa" and not ob["wojewodztwa"]:
        return jsonify({"blad": "Zaznacz co najmniej jedno województwo."}), 400
    c = S.cfg()
    zmiany = {}
    if ob["tryb"] == "promien":
        try:
            promien = int(float(str(j.get("promien") or c.get("promien_km") or 10)))
        except ValueError:
            promien = 10
        if promien not in S.REG.PROMIENIE:
            return jsonify({"blad": "Wybierz promień z listy."}), 400
        srodek = j.get("centrum")  # {nazwa, lat, lon, wojewodztwo, opis} – nowa miejscowość
        wpisane = str(j.get("miejscowosc") or "").strip()
        if not srodek and wpisane and S.W.norm(wpisane) != S.W.norm(c.get("centrum_opis") or c.get("centrum_nazwa") or ""):
            # miejscowość wpisana z klawiatury (bez wyboru z podpowiedzi) – program sam ją rozpoznaje w wykazie miejscowości
            try:
                import miejscowosci as _M
                srodek = _M.znajdz(wpisane)
            except Exception:
                srodek = None
            if not srodek:
                try:
                    srodek = next(iter(S.REG.szukaj_miejscowosci(wpisane) or []), None)
                except Exception:
                    srodek = None
            if not srodek:
                return jsonify({"blad": f"Nie znam miejscowości „{wpisane[:60]}” – sprawdź pisownię albo wybierz ją z podpowiedzi."}), 400
        if srodek:
            try:
                lat, lon = float(srodek["lat"]), float(srodek["lon"])
            except (KeyError, TypeError, ValueError):
                return jsonify({"blad": "Wybierz miejscowość z listy podpowiedzi."}), 400
            nazwa, woj = str(srodek.get("nazwa", ""))[:80], str(srodek.get("wojewodztwo", ""))[:40]
        elif c.get("centrum_nazwa") and c.get("miejscowosci"):
            lat, lon, nazwa = c["centrum_lat"], c["centrum_lon"], c["centrum_nazwa"]
            woj = c.get("centrum_woj", "")
        else:
            return jsonify({"blad": "Wpisz i wybierz miejscowość, wokół której mam szukać."}), 400
        stary = (c.get("obszar") or {})
        if True:  # zawsze od nowa – wykaz miejscowości jest wbudowany, przeliczenie trwa ułamek sekundy
            try:
                miejsca = S.REG.miejscowosci_w_promieniu(lat, lon, promien)
                woj_ob = S.REG.wojewodztwa_obszaru(lat, lon, promien, woj)
            except Exception as e:
                return jsonify({"blad": str(e)}), 502
            if not any(m[0].lower() == nazwa.lower() for m in miejsca):
                miejsca.insert(0, [nazwa, lat, lon])
            zmiany = {"centrum_nazwa": nazwa, "centrum_lat": lat, "centrum_lon": lon, "centrum_woj": woj,
                      "centrum_opis": str((srodek or {}).get("opis") or c.get("centrum_opis") or nazwa)[:160],
                      "promien_km": promien, "miejscowosci": miejsca,
                      "frazy_zawsze": [f"gmina {nazwa}", f"miasto {nazwa}"], "wykluczenia": []}
            ob["wojewodztwa_obszaru"] = woj_ob
    S.zapisz_ustawienia({**zmiany, "obszar": ob, "region_v2": True})
    c2 = S.cfg()
    return jsonify({"ok": True, "opis": S.opis_obszaru(ob, c2), "tryb": ob["tryb"], "wojewodztwa": ob["wojewodztwa"],
                    "miejscowosc": c2.get("centrum_nazwa", ""), "miejscowosc_opis": c2.get("centrum_opis", ""), "promien": c2.get("promien_km")})


@bp.get("/api/przetargi/nowe")
@S.wymaga_logowania
def przetargi_nowe():
    """Nowe przetargi w zapisanym obszarze od ostatniej wizyty. Przy pierwszym wejściu danego dnia – jeśli dziś jeszcze
    nie szukano – uruchamia wyszukiwanie w tle (np. gdy serwer spał o 7:00)."""
    w = S.wizyta_konta()
    c = S.cfg()
    w_ob = S.sprawdzacz_obszaru(c)
    tryb = request.args.get("tryb") or ""
    lista = sorted([dict(t, numer=nr) for nr, t in S.db_przetargi().items() if S.czy_nowy(t, nr, w) and w_ob(t) and S.pasuje_do_trybu(t, tryb)],
                   key=lambda t: (-(t.get("ocena") or 0), t.get("dodano", "")))
    stan = S.czytaj(S.F_POWIAD, {})
    ob = c.get("obszar") or {}
    obszar_ok = ob.get("tryb") == "polska" or (ob.get("tryb") == "wojewodztwa" and bool(ob.get("wojewodztwa"))) \
        or (ob.get("tryb", "promien") == "promien" and bool(c.get("miejscowosci")))
    zid = None
    if obszar_ok and (stan.get("ostatnie_szukanie") or "")[:10] != dt.date.today().isoformat() and request.args.get("szukaj") != "0":
        if not any(z.get("konto") == S.konto_biezace() and z.get("typ") == "szukaj" and z["status"] == "trwa" for z in S.ZADANIA.values()):
            stan["ostatnie_szukanie"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")  # najwyżej raz dziennie
            S.pisz(S.F_POWIAD, stan)
            zid = S.uruchom("szukaj", "Sprawdzanie nowych przetargów", S.praca_szukaj)["id"]
    return jsonify({"liczba": len(lista), "przetargi": [{k: t.get(k) for k in ("numer", "przedmiot", "zamawiajacy", "lokalizacja", "ocena", "termin_ofert")}
                                                        for t in lista[:5]],
                    "od": w.get("poprzednia"), "obszar": S.opis_obszaru(ob, c), "obszar_ustawiony": obszar_ok,
                    "zadanie": zid, "ostatnie_szukanie": stan.get("ostatnie_szukanie")})


@bp.post("/api/przetargi/widziane")
@S.wymaga_logowania
def przetargi_widziane():
    """Oznacza przetarg (albo wszystkie – wszystkie=true) jako przejrzany."""
    j = request.json or {}
    with S.BLOKADA:
        w = S.wizyta_konta()
        if j.get("wszystkie"):
            w["widziane"] = list(S.db_przetargi().keys())
        elif j.get("numer"):
            w["widziane"] = sorted(set(w.get("widziane") or []) | {str(j["numer"])})
        S.pisz(S.F_WIZYTY, w)
    return jsonify({"ok": True})


@bp.get("/api/przetargi")
@S.wymaga_logowania
def przetargi():
    """Domyślnie tylko przetargi z obecnie wybranego obszaru; ?zakres=wszystkie – wszystkie pobrane."""
    db = S.db_przetargi()
    # przetargi, z których powstały projekty (moje / udostępnione, niezarchiwizowane)
    login, rola = session.get("login"), S.rola_sesji()
    w_projektach = {}
    for pid in os.listdir(S.PROJ):
        m = S.czytaj(os.path.join(S.PROJ, pid, "projekt.json"), None)
        if m and m.get("przetarg_numer") and not m.get("archiwum") and S.ma_dostep(m, login, rola, lista=True):
            w_projektach.setdefault(m["przetarg_numer"], {"id": pid, "nazwa": m.get("nazwa"), "typ": m.get("typ") or "przetarg",
                                                          "status_projektu": m.get("status_projektu") or ""})
    wiz = S.wizyta_konta()
    wszystkie = [dict(t, numer=nr, nowy=S.czy_nowy(t, nr, wiz), rodzaj_zam=S.rodzaj_przetargu(t), typ_zam=S.typ_zamawiajacego(t),
                      **({"projekt": w_projektach[nr]} if nr in w_projektach else {})) for nr, t in db.items()]
    for t in wszystkie:  # pełna treść ogłoszeń nie jest potrzebna na liście (nawet kilka MB) – szybsze ładowanie, zwłaszcza na telefonie
        t.pop("tresc", None)
        t.pop("_surowe", None)
    z = (session.get("admin_zakres") or "wszystkie") if S.wlasciciel() and not session.get("jako") else "moje"  # H1-01
    obce = []
    if z != "moje":  # administrator: przetargi pobrane przez inne konta (tylko do wglądu)
        for login in S.wszystkie_konta():
            if login == S.login_admina() or (z != "wszystkie" and login != z):
                continue
            for nr, t in S.czytaj(S.F_DB.dla(login), {}).items():
                obce.append(dict(t, numer=nr, konto=login, obcy=True, nowy=False))
        if z not in ("wszystkie", S.login_admina()):
            wszystkie = []
    ost = S.ostatnie_aktualne()  # wyniki wyszukiwań z innego (wcześniejszego) obszaru nie wchodzą na listę
    if request.args.get("zakres") == "wszystkie" or z != "moje":
        wyn = wszystkie + obce
        if z != "moje" and request.args.get("zakres") != "wszystkie":
            w_ = S.sprawdzacz_obszaru()
            wyn = [t for t in wszystkie if w_(t) or t["numer"] in ost or t.get("projekt") or t.get("status") in ("startujemy", "oferta złożona", "wygrany")] + obce
    else:
        w = S.sprawdzacz_obszaru()
        # zawsze widoczne: przetargi z moich projektów, te, w których startuję / które wygrałem, oraz wyniki ostatnich wyszukiwań
        # (te zostały już dopasowane do obszaru przy wyszukiwaniu – lista nie odrzuca ich drugi raz)
        wyn = [t for t in wszystkie if w(t) or t["numer"] in ost or t.get("projekt") or t.get("status") in ("startujemy", "oferta złożona", "wygrany")]
    wyn = scal_duplikaty(wyn)
    r = jsonify(wyn)
    r.headers["X-Poza-Obszarem"] = str(max(0, len(wszystkie) - len([t for t in wyn if not t.get("obcy")])))
    r.headers["X-Wszystkich"] = str(len(wszystkie))
    return r


@bp.post("/api/przetargi/termin")
@S.wymaga_logowania
def przetarg_termin():
    """Ręczne ustawienie terminu składania ofert."""
    j = request.json or {}
    d = S.AN._jako_data(str(j.get("termin", "")).replace("T", " ")) if j.get("termin") else None
    if j.get("termin") and not d:
        return jsonify({"blad": "Podaj datę, np. 20.10.2026 10:00."}), 400
    with S.BLOKADA:
        db = S.db_przetargi()
        if j.get("numer") not in db:
            return jsonify({"blad": "Nie ma takiego przetargu."}), 404
        db[j["numer"]]["termin_ofert"] = d or ""
        db[j["numer"]]["termin_zrodlo"] = "wpisany ręcznie"
        S.pisz(S.F_DB, db)
    return jsonify({"ok": True, "termin": d})


@bp.post("/api/przetargi/analiza")
@S.wymaga_logowania
def przetarg_analiza():
    nr = (request.json or {}).get("numer")
    if nr not in S.db_przetargi():
        return jsonify({"blad": "Nie ma takiego przetargu."}), 404
    return jsonify(S.uruchom("analiza", "Pełna analiza przetargu", S.praca_analiza_pelna, nr))


@bp.post("/api/przetargi/szukaj")
@S.wymaga_logowania
def przetargi_szukaj():
    slowa = S.czysc_slowa((request.json or {}).get("slowa"))
    tryb = str((request.json or {}).get("tryb") or "wykonawca")[:20]
    return jsonify(S.uruchom("szukaj", "Wyszukiwanie przetargów", S.praca_szukaj, slowa or None, tryb))


@bp.get("/api/przetargi/ostatnie")
@S.wymaga_logowania
def przetargi_ostatnie():
    o = dict((S.czytaj(S.F_POWIAD, {}).get("ostatnie_wyszukiwanie") or {}).get(request.args.get("tryb") or "wykonawca") or {})
    if o:
        o["aktualne"] = o.get("obszar") == S.klucz_obszaru()  # wyszukiwanie z innego obszaru – lista pokaże aktywne z obecnego obszaru
    return jsonify(o)


@bp.get("/api/przetargi/slowa")
@S.wymaga_logowania
def przetargi_slowa():
    if request.args.get("tryb") == "dostawca":  # dostawca / usługodawca ma własną listę słów (dostawy i usługi)
        return jsonify({"domyslne": S.cfg().get("slowa_kluczowe_dostawy") or S.SLOWA_DOSTAWY})
    return jsonify({"domyslne": S.cfg().get("slowa_kluczowe", [])})


@bp.post("/api/przetargi/slowa")
@S.wymaga_logowania
def przetargi_slowa_zapisz():
    if S.blad_slow((request.json or {}).get("slowa")):
        return jsonify({"blad": S.blad_slow((request.json or {}).get("slowa"))}), 400
    slowa = S.czysc_slowa((request.json or {}).get("slowa"))
    if not slowa:
        return jsonify({"blad": "Lista słów kluczowych nie może być pusta."}), 400
    S.zapisz_ustawienia({"slowa_kluczowe_dostawy" if (request.json or {}).get("tryb") == "dostawca" else "slowa_kluczowe": slowa})
    return jsonify({"ok": True, "domyslne": slowa})


@bp.post("/api/przetargi/ocen")
@S.wymaga_logowania
def przetargi_ocen():
    if S.profil_pusty():  # H1-11: bez opisu firmy AI nie ma według czego oceniać (dawniej oceniała według przykładowego opisu)
        return jsonify({"blad": S.KOMUNIKAT_PROFIL, "uzupelnij_profil": True}), 400
    numery = _numery(_j().get("numery")) or [nr for nr, t in S.db_przetargi().items() if t.get("ocena") in (None, "")]
    numery = numery[: int(S.cfg()["max_do_oceny"])]
    return jsonify(S.uruchom("ocena", f"Ocena AI ({len(numery)})", S.praca_ocen, numery))


STATUSY_PRZETARGU = ("nowy", "startujemy", "do analizy", "odpuszczamy", "oferta złożona", "wygrany", "przegrany")  # karta W1 §4


@bp.post("/api/przetargi/status")
@S.wymaga_logowania
def przetargi_status():
    j = _j()
    st = j.get("status", "nowy")
    if st not in STATUSY_PRZETARGU:
        return jsonify({"blad": "Nieznany status – wybierz: " + ", ".join(STATUSY_PRZETARGU) + "."}), 400
    numery = j.get("numery", [])
    if not isinstance(numery, list):
        return jsonify({"blad": "Podaj listę numerów przetargów."}), 400
    with S.BLOKADA:
        db = S.db_przetargi()
        for nr in numery:
            if isinstance(nr, str) and nr in db:
                db[nr]["status"] = st
                if j.get("powod"):
                    db[nr]["powod_decyzji"] = str(j["powod"])[:200]
                if st in ("startujemy", "odpuszczamy", "oferta złożona", "wygrany", "przegrany"):
                    S.zapisz_decyzje(nr, db[nr], st, str(j.get("powod") or "")[:200])
        S.pisz(S.F_DB, db)
    return jsonify({"ok": True})


def klucz_przetargu(t):
    """To samo postępowanie bywa w kilku źródłach (BZP i TED – inne numery) i na listach kilku kont: klucz z przedmiotu i zamawiającego."""
    p = S.W.norm(t.get("przedmiot") or "")[:150]
    return (p + "|" + S.W.norm(t.get("zamawiajacy") or "")[:20]) if len(p) >= 12 else "nr|" + str(t.get("numer"))


def scal_duplikaty(lista):
    """Jedna pozycja na postępowanie: najpierw własna z projektem, potem własna z decyzją, własna, na końcu z listy innego konta.
    Pozostałe nie znikają bez śladu: pozycja ma „inne_konta” (kto jeszcze ma ten przetarg) i „duplikaty” (inne numery ogłoszenia)."""
    grupy = {}
    for t in lista:
        grupy.setdefault(klucz_przetargu(t), []).append(t)
    wyn = []
    for t in lista:
        g = grupy.get(klucz_przetargu(t))
        if g is None:
            continue  # grupa już wydana
        grupy[klucz_przetargu(t)] = None
        if len(g) == 1:
            wyn.append(t)
            continue
        g_ = sorted(g, key=lambda x: (bool(x.get("obcy")), not x.get("projekt"), (x.get("status") or "nowy") == "nowy",
                                      x.get("zrodlo") == "TED", -(float(x.get("ocena")) if str(x.get("ocena") or "").replace(".", "", 1).isdigit() else -1)))
        r = dict(g_[0])
        konta = sorted({x.get("konto") for x in g_ if x.get("obcy") and x.get("konto") and x.get("konto") != r.get("konto")})
        if konta:
            r["inne_konta"] = konta
        dup = sorted({x["numer"] for x in g_ if x.get("numer") != r.get("numer")})
        if dup:
            r["duplikaty"] = dup
        wyn.append(r)
    return wyn


@bp.post("/api/przetargi/przejmij")
@S.wymaga_logowania
def przetargi_przejmij():
    """Administrator: przetarg widoczny na liście innego konta trafia też na listę bieżącego konta (kopia rekordu i pobranych dokumentów),
    żeby mógł go sam ocenić i przygotować ofertę. Lista i projekty tamtego konta zostają bez zmian."""
    if not S.wlasciciel():  # H1-01: listy innych kont widzi tylko właściciel programu
        return jsonify({"blad": "Tylko właściciel programu może przejąć przetarg z listy innego konta."}), 403
    nr, konto = str(_j().get("numer") or ""), str(_j().get("konto") or "")
    if not nr or konto not in S.wszystkie_konta():
        return jsonify({"blad": "Nie znaleziono przetargu."}), 404
    zrodlo = S.czytaj(S.F_DB.dla(konto), {}).get(nr)
    if not zrodlo:
        return jsonify({"blad": "Tego przetargu nie ma już na liście konta " + konto + "."}), 404
    with S.BLOKADA:
        db = S.db_przetargi()
        if nr not in db:
            t = {k: v for k, v in zrodlo.items() if k not in ("status", "powod_decyzji", "nowy")}
            t["status"] = "nowy"
            t["z_konta"] = konto
            db[nr] = t
            S.pisz(S.F_DB, db)
    ukryte = S.cfg_surowy().get("ukryte", [])
    if nr in ukryte:  # wcześniej usunięty z mojej listy – przywracam
        S.zapisz_ustawienia({"ukryte": [x for x in ukryte if x != nr]})
    return jsonify({"ok": True, "numer": nr})


@bp.post("/api/przetargi/usun")
@S.wymaga_logowania
def przetargi_usun():
    with S.BLOKADA:
        db = S.db_przetargi()
        ukryte = S.cfg_surowy().get("ukryte", [])
        for nr in _numery(_j().get("numery")):
            db.pop(nr, None)
            ukryte.append(nr)
        S.pisz(S.F_DB, db)
    S.zapisz_ustawienia({"ukryte": ukryte[-5000:]})
    return jsonify({"ok": True})


@bp.post("/api/raporty/zwyciezcy")
@S.wymaga_logowania
@S.tylko_admin
def raport_zwyciezcy():
    j = _j()
    if str(j.get("wojewodztwo") or "dolnośląskie") not in S.WOJEWODZTWA:
        return jsonify({"blad": "Wybierz województwo z listy."}), 400
    return jsonify(S.uruchom("raport_powiaty", f"Raport zwycięzców – {j.get('wojewodztwo', '')}", S.praca_raport_wznawialny,
                           str(j.get("wojewodztwo") or "dolnośląskie"), max(1, min(36, int(S.RY._f(j.get("miesiecy")) or 12))), bool(j.get("bk", True)),
                           [z_ for z_ in (j.get("zakresy") or []) if z_ in S.HZ.RODZAJE_ZAMOWIENIA], bool(j.get("od_nowa"))))


@bp.get("/api/raporty")
@S.wymaga_logowania
def raporty_lista():
    kat = os.path.join(S.DATA, "raporty", S.konto_biezace() or "env")
    L = []
    if os.path.isdir(kat):
        for f in os.listdir(kat):
            p = os.path.join(kat, f)
            L.append({"nazwa": f, "rozmiar": os.path.getsize(p), "data": dt.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M"),
                      "url": "/api/raporty/plik/" + S.urllib.parse.quote(f)})
    return jsonify(sorted(L, key=lambda x: x["data"], reverse=True))


@bp.post("/api/raporty/usun")
@S.wymaga_logowania
@S.tylko_admin
def raporty_usun():
    """Usuwa zapisane pliki raportów konta (wybrany albo wszystkie). Dane pobrane z BZP i BK w pamięci programu zostają, chyba że raport powstanie od podstaw."""
    j = request.json or {}
    kat = os.path.join(S.DATA, "raporty", S.konto_biezace() or "env")
    usun = os.listdir(kat) if j.get("wszystkie") and os.path.isdir(kat) else [os.path.basename(str(j.get("nazwa") or ""))]
    ile = 0
    for f in usun:
        p = os.path.join(kat, f)
        if f and os.path.isfile(p):
            os.remove(p)
            ile += 1
    return jsonify({"usunieto": ile})


@bp.get("/api/raporty/plik/<nazwa>")
@S.wymaga_logowania
def raport_plik(nazwa):
    p = os.path.join(S.DATA, "raporty", S.konto_biezace() or "env", os.path.basename(nazwa))
    if not os.path.isfile(p):
        abort(404)
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


@bp.post("/api/przetargi/historia")
@S.wymaga_logowania
def historia_zamawiajacego_przetarg():
    nr = (request.json or {}).get("numer")
    t = S.db_przetargi().get(nr)
    if not t:
        return jsonify({"blad": "Nie ma takiego przetargu na liście."}), 404
    return jsonify(S.uruchom("historia", "Historia zamawiającego (BZP)", S.praca_historia_zamawiajacego, t.get("zamawiajacy") or "",
                           t.get("przedmiot") or "", t.get("cpv") or "", S._nip_z_surowych(t), None, nr, bool((request.json or {}).get("wymus"))))


@bp.get("/api/przetargi/historia/<path:nr>")
@S.wymaga_logowania
def historia_zamawiajacego_wynik(nr):
    return jsonify((S.czytaj(S.F_HIST_PRZ, {}) or {}).get(nr) or {})


def praca_bip_odkryj(log, woj, powiaty, typy, od_razu=False):
    c = S.cfg()
    S.wymagany_klucz(c)
    wyniki = S.katalog_instytucji(log, woj, powiaty, typy)
    with S.BLOKADA:
        b = S.dane_bip()
        znane = {z["url"].rstrip("/").lower() for z in b["zrodla"]} | {p["url"].rstrip("/").lower() for p in b["propozycje"]}
        dodane = 0
        for w in wyniki:
            k = w["url"].rstrip("/").lower()
            if k not in znane:
                znane.add(k)
                if od_razu:  # nowa wyszukiwarka: strony instytucji z obszaru od razu obserwowane
                    b["zrodla"].append(dict(w, id=uuid.uuid4().hex[:10], aktywne=True, status="nowe – jeszcze nie sprawdzone",
                                            dodano=dt.datetime.now().strftime("%Y-%m-%d"), wojewodztwo=woj))
                else:
                    b["propozycje"].append(w)
                dodane += 1
        S.pisz(S.F_BIP, b)
    log(f"Nowych propozycji do zatwierdzenia: {dodane}")
    return {"propozycje": dodane}


def praca_bip_sprawdz(log, tylko=None):
    c = S.cfg()
    S.wymagany_klucz(c)
    if not S.BIP_BLOKADA.acquire(blocking=False):
        log("BIP: sprawdzanie już trwa – pomijam.")
        return []
    try:
        b = S.dane_bip()
        strony = S.WSP.czytaj("bip_strony.json", {})  # wspólna pamięć stron instytucji (wszystkie konta)
        nowe = S.BIP.sprawdz_zrodla(c, b, log, tylko, wspolne=strony, swiezosc_h=float(c.get("bip_swiezosc_h", 6) or 6))
        with S.W.BLOKADA:
            akt_s = S.WSP.czytaj("bip_strony.json", {})
            akt_s.update(strony)
            S.WSP.pisz("bip_strony.json", akt_s)
        with S.BLOKADA:  # scal wyniki z aktualnym plikiem (w trakcie ktoś mógł edytować listę)
            akt = S.dane_bip()
            po_id = {z["id"]: z for z in b["zrodla"]}
            for z in akt["zrodla"]:
                if z["id"] in po_id:
                    for k in ("sprawdzono", "status", "odcisk", "zmiana", "znalezione"):
                        if k in po_id[z["id"]]:
                            z[k] = po_id[z["id"]][k]
            akt["widziane"] = {**akt.get("widziane", {}), **b.get("widziane", {})}
            S.pisz(S.F_BIP, akt)
        return nowe
    finally:
        S.BIP_BLOKADA.release()


def praca_bip_tylko(log, tylko):
    c = S.cfg()
    znane = set(S.db_przetargi()) | set(c.get("ukryte", []))
    nowe = [t for t in praca_bip_sprawdz(log, tylko) if t["numer"] not in znane]
    with S.BLOKADA:
        db = S.db_przetargi()
        for t in nowe:
            t.setdefault("dodano", dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            db[t["numer"]] = {k: v for k, v in t.items() if k != "numer"}
        S.pisz(S.F_DB, db)
    if nowe and c.get("auto_ocena") and c.get("api_key"):
        # strony wybranych instytucji – słowa i branża obu trybów (wykonawca i dostawca), wykluczenia; obszar wynika z wyboru stron
        slowa_n = [S.W.norm(x) for x in list(c.get("slowa_kluczowe") or []) + list(c.get("slowa_kluczowe_dostawy") or []) if S.W.norm(x)]
        cpv = [str(x).strip() for x in list(c.get("cpv") or []) + list(c.get("cpv_dostawy") or []) if str(x).strip()]
        wykl = [S.W.norm(x) for x in c.get("wykluczenia") or [] if S.W.norm(x)]
        kandydaci = [t["numer"] for t in nowe if not (wykl and any(w_ in S.W.norm(str(t.get("przedmiot") or "")) for w_ in wykl))]
        if len(kandydaci) < len(nowe):
            log(f"Wykluczenia: {len(nowe) - len(kandydaci)} ogłoszeń ze stron instytucji bez oceny AI.")
        if slowa_n or cpv:
            kandydaci = S.sito_do_oceny(log, kandydaci, c, slowa_n, cpv)
        else:
            kandydaci = kandydaci[: int(c["max_do_oceny"])]
        if kandydaci:
            S.praca_ocen(log, kandydaci)
    return {"nowe": len(nowe)}


@bp.get("/api/bip")
@S.wymaga_logowania
def bip_lista():
    b = S.dane_bip()
    c = S.cfg()
    return jsonify({"zrodla": [{k: v for k, v in z.items() if k != "odcisk"} for z in b["zrodla"]],
                    "propozycje": b["propozycje"], "wojewodztwa": S.BIP.WOJEWODZTWA, "typy": S.BIP.TYPY,
                    "obszar_opis": S.opis_obszaru(c.get("obszar"), c), "obszar_tryb": (c.get("obszar") or {}).get("tryb", "promien")})


@bp.post("/api/bip/odkryj-obszar")
@S.wymaga_logowania
def bip_odkryj_obszar():
    """Strony zamawiających (urzędy, szpitale, uczelnie, spółki) z obszaru ustawionego w „Obszarze wyszukiwania”."""
    typy = [t for t in (request.json or {}).get("typy", []) if t in S.BIP.TYPY]
    if not typy:
        return jsonify({"blad": "Zaznacz co najmniej jeden rodzaj zamawiających."}), 400
    c = S.cfg()
    if (c.get("obszar") or {}).get("tryb") == "polska":
        return jsonify({"blad": "Obszar wyszukiwania to cała Polska – wybierz województwa albo okolicę miejscowości, żeby znaleźć strony zamawiających."}), 400
    return jsonify(S.uruchom("bip", f"Strony zamawiających: {S.opis_obszaru(c.get('obszar'), c)}", praca_bip_odkryj_obszar, typy))


def praca_bip_odkryj_obszar(log, typy):
    c = S.cfg()
    S.wymagany_klucz(c)
    grupy = S.powiaty_obszaru(c, log)
    if not grupy:
        raise ValueError("Najpierw ustaw i zapisz obszar wyszukiwania (województwa albo okolicę miejscowości).")
    log("Obszar: " + "; ".join(f"woj. {w}" + (f" – pow. {', '.join(p)}" if p else " (całe)") for w, p in grupy.items()))
    for i, (woj, pw) in enumerate(grupy.items(), 1):
        log(f"Województwo {i}/{len(grupy)}: {woj}")
        praca_bip_odkryj(log, woj, pw, typy)
    return {"wojewodztwa": len(grupy)}


@bp.post("/api/bip/odkryj")
@S.wymaga_logowania
def bip_odkryj():
    j = _j()
    woj = j.get("wojewodztwo")
    typy = [t for t in j.get("typy", []) if t in S.BIP.TYPY]
    if woj not in S.BIP.WOJEWODZTWA or not typy:
        return jsonify({"blad": "Wybierz województwo i co najmniej jeden rodzaj urzędów."}), 400
    powiaty = [p.strip() for p in re.split(r"[,;\n]", j.get("powiaty", "")) if p.strip()]
    return jsonify(S.uruchom("bip", f"Szukam stron zamówień: woj. {woj}" + (f", pow. {', '.join(powiaty)}" if powiaty else ""),
                           praca_bip_odkryj, woj, powiaty, typy))


@bp.post("/api/bip/propozycje")
@S.wymaga_logowania
def bip_propozycje():
    urls = {u for u in (_j().get("urls") or []) if isinstance(u, str)} if isinstance(_j().get("urls"), list) else set()
    akcja = _j().get("akcja")
    with S.BLOKADA:
        b = S.dane_bip()
        wybrane = [p for p in b["propozycje"] if p["url"] in urls]
        b["propozycje"] = [p for p in b["propozycje"] if p["url"] not in urls]
        if akcja == "dodaj":
            for p in wybrane:
                b["zrodla"].append(dict(p, id=uuid.uuid4().hex[:10], aktywne=True, status="nowe – jeszcze nie sprawdzone",
                                        dodano=dt.datetime.now().strftime("%Y-%m-%d")))
        S.pisz(S.F_BIP, b)
    return jsonify({"ok": True, "ile": len(wybrane)})


@bp.post("/api/bip/zrodla")
@S.wymaga_logowania
def bip_dodaj():
    j = _j()
    url = str(j.get("url", "")).strip()
    if not url.startswith("http") or not str(j.get("nazwa", "")).strip():
        return jsonify({"blad": "Podaj nazwę urzędu i adres strony (https://…)."}), 400
    with S.BLOKADA:
        b = S.dane_bip()
        b["zrodla"].append({"id": uuid.uuid4().hex[:10], "nazwa": str(j["nazwa"]).strip()[:150],
                            "typ": j.get("typ") if j.get("typ") in S.BIP.TYPY else "gmina",
                            "wojewodztwo": str(j.get("wojewodztwo", ""))[:40], "powiat": str(j.get("powiat", ""))[:80],
                            "url": url[:500], "uwagi": "dodane ręcznie", "aktywne": True,
                            "status": "nowe – jeszcze nie sprawdzone", "dodano": dt.datetime.now().strftime("%Y-%m-%d")})
        S.pisz(S.F_BIP, b)
    return jsonify({"ok": True})


@bp.post("/api/bip/zmien")
@S.wymaga_logowania
def bip_zmien():
    j = _j()
    ids = set(j.get("ids") or [j.get("id")])
    with S.BLOKADA:
        b = S.dane_bip()
        if j.get("usun"):
            b["zrodla"] = [z for z in b["zrodla"] if z["id"] not in ids]
        for z in b["zrodla"]:
            if z["id"] in ids:
                if "aktywne" in j:
                    z["aktywne"] = bool(j["aktywne"])
                if j.get("url", "").startswith("http"):
                    z["url"] = j["url"].strip()[:500]
                    z.pop("odcisk", None)
                    z["status"] = "adres zmieniony – do sprawdzenia"
        S.pisz(S.F_BIP, b)
    return jsonify({"ok": True})


@bp.post("/api/bip/sprawdz")
@S.wymaga_logowania
def bip_sprawdz():
    ids = [x for x in (_j().get("ids") or []) if isinstance(x, str)] if isinstance(_j().get("ids"), list) else []
    ids = ids or None
    return jsonify(S.uruchom("bip", "Sprawdzam obserwowane BIP", praca_bip_tylko, ids))


@bp.get("/api/przetargi/tekst-dokumentu")
@S.wymaga_logowania
def przetarg_tekst_dokumentu():
    """Numer przetargu w parametrze (numery BZP zawierają „/”, których nie da się przekazać w ścieżce adresu)."""
    return S._tekst_odwolania(S.folder_przetargu(request.args.get("nr", "")), request.args.get("plik", ""))
