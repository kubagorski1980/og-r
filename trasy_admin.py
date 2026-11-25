# -*- coding: utf-8 -*-
"""
Administracja i konta – trasy: użytkownicy i role, konta (praca jako konto, zakres administratora), ustawienia konta i programu, archiwum, diagnostyka danych.
Blueprint „administracja” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

import bezpieczenstwo as BZ

bp = Blueprint("administracja", __name__)


@bp.get("/api/admin/dane")
@S.wymaga_logowania
def diagnostyka_danych():
    """Gdzie są dane: trwały dysk, bieżące konto / podgląd „jako”, dla każdego konta – projekty, Księgowość, ostatnia zmiana.
    Tylko odczyt – niczego nie zmienia ani nie usuwa."""
    if not S.wlasciciel():  # dane wszystkich kont – tylko właściciel programu (H1-01)
        return jsonify({"blad": "Tylko właściciel programu."}), 403
    import shutil as _sh

    def czas(t):
        return dt.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M") if t else None

    def ostatnia_zmiana(kat):
        najn = 0
        for r, _, fs in os.walk(kat):
            for f in fs[:200]:
                try:
                    najn = max(najn, os.path.getmtime(os.path.join(r, f)))
                except OSError:
                    pass
        return czas(najn)

    def wypelnione(o, pref=""):
        if isinstance(o, dict):
            return [x for k, v in o.items() for x in wypelnione(v, f"{pref}{k}.")]
        return [pref.rstrip(".")] if o not in (None, "", [], {}, False, 0) else []

    def ksiegi(kat):
        kk = os.path.join(kat, "ksiegowosc")
        dane_ = S.czytaj(os.path.join(kk, "dane.json"), None) or {}  # moduł Księgowość (dane.json)
        d = dane_.get("dokumenty")
        prof = dane_.get("profil") or S.czytaj(os.path.join(kk, "profil.json"), None)
        pliki = []
        if os.path.isdir(kk):
            for f in sorted(os.listdir(kk)):
                sc = os.path.join(kk, f)
                if os.path.isfile(sc):
                    pliki.append(f"{f} – {os.path.getsize(sc)} B – {czas(os.path.getmtime(sc))}")
        n_pl = sum(len(fs) for _, _, fs in os.walk(os.path.join(kk, "pliki"))) if os.path.isdir(os.path.join(kk, "pliki")) else 0
        n_kop = len(os.listdir(os.path.join(kk, "kopie"))) if os.path.isdir(os.path.join(kk, "kopie")) else 0
        pola = wypelnione(prof) if isinstance(prof, dict) else []
        stare = S.czytaj(os.path.join(kk, "dane.json"), None)

        def budowa(o, gl=0):
            if gl > 3:
                return "…"
            if isinstance(o, dict):
                return {k_: budowa(v, gl + 1) for k_, v in list(o.items())[:25]}
            if isinstance(o, list):
                return f"lista: {len(o)} rekordów" + (f", pola: {sorted(o[0].keys())[:25]}" if o and isinstance(o[0], dict) else "")
            return type(o).__name__
        return {"dokumenty": len(d) if isinstance(d, (list, dict)) else 0, "profil": bool(prof), "profil_wypelnionych_pol": len(pola),
                "profil_sekcje": sorted({x.split(".")[0] for x in pola}), "pliki_faktur": n_pl, "kopie": n_kop, "zawartosc_katalogu": pliki,
                "dane_json_budowa": budowa(stare) if stare is not None else None, "odtworzenie": S.czytaj(os.path.join(kk, "migracja.json"), None)}
    proj = {}
    if os.path.isdir(S.PROJ):
        for pid in os.listdir(S.PROJ):
            m = S.czytaj(os.path.join(S.PROJ, pid, "projekt.json"), None)
            if isinstance(m, dict):
                w = m.get("wlasciciel") or m.get("konto") or S.login_admina()
                proj[w] = proj.get(w, 0) + 1
    konta = [{"konto": S.login_admina() + " (administrator z ustawień – katalog główny)", "katalog": S.DATA, "projekty": proj.get(S.login_admina(), 0),
              "ksiegowosc": ksiegi(S.DATA), "ostatnia_zmiana": ostatnia_zmiana(os.path.join(S.DATA, "ksiegowosc"))}]
    if os.path.isdir(S.DIR_KONT):
        for k in sorted(os.listdir(S.DIR_KONT)):
            kat = os.path.join(S.DIR_KONT, k)
            if os.path.isdir(kat):
                konta.append({"konto": k, "katalog": kat, "projekty": proj.get(k, 0), "ksiegowosc": ksiegi(kat), "ostatnia_zmiana": ostatnia_zmiana(kat)})
    najst = None
    for r, _, fs in os.walk(S.DATA):
        for f in fs[:50]:
            try:
                t = os.path.getmtime(os.path.join(r, f))
                najst = t if najst is None or t < najst else najst
            except OSError:
                pass
    slady = []  # ślady danych księgowych w innych miejscach dysku (poza projektami i pamięcią ogłoszeń)
    for r, ds, fs in os.walk(S.DATA):
        ds[:] = [x for x in ds if x not in ("projekty", "wspolne") and not x.startswith(".")]
        for f in fs:
            sc = os.path.join(r, f)
            if re.search(r"(?i)ksieg|ksef|jpk|faktur|\.tmp$|uszkodzony", sc) and "/kopie/" not in sc:
                try:
                    slady.append(f"{os.path.relpath(sc, S.DATA)} – {os.path.getsize(sc)} B – {czas(os.path.getmtime(sc))}")
                except OSError:
                    pass
        if len(slady) > 300:
            break
    u = _sh.disk_usage(S.DATA)
    return jsonify({"katalog_danych": S.DATA, "dysk_trwaly": os.path.ismount(S.DATA),
                    "uwaga_dysk": "" if os.path.ismount(S.DATA) else "UWAGA: katalog danych NIE jest osobnym dyskiem – dane mogą znikać przy każdym wdrożeniu.",
                    "zajete_mb": round((u.total - u.free) / 1e6), "wolne_mb": round(u.free / 1e6),
                    "najstarszy_plik": czas(najst), "zalogowany": session.get("login"), "pracujesz_na_koncie": S.konto_biezace(),
                    "podglad_jako": session.get("jako") or "", "konta": konta, "projekty_wedlug_wlasciciela": proj, "slady_ksiegowosci": slady[:300]})


@bp.get("/api/konta")
@S.wymaga_logowania
@S.tylko_admin
def konta():
    """Konta (firmy) korzystające z programu – ze statystykami i ostatnią aktywnością."""
    ostatnia, liczby = {}, {}
    try:
        with open(S.F_AKTYWNOSC, encoding="utf-8") as f:
            for linia in f.readlines()[-30000:]:
                try:
                    w = json.loads(linia)
                    ostatnia[w.get("konto")] = w
                    liczby[w.get("konto")] = liczby.get(w.get("konto"), 0) + 1
                except ValueError:
                    continue
    except OSError:
        pass
    projekty_ = {}
    for pid in os.listdir(S.PROJ):
        m = S.czytaj(os.path.join(S.PROJ, pid, "projekt.json"), None)
        if m and not m.get("archiwum"):
            k = m.get("wlasciciel") or S.login_admina()
            projekty_.setdefault(k, {"projekty": 0, "realizacja": 0})
            projekty_[k]["projekty"] += 1
            projekty_[k]["realizacja"] += m.get("status_projektu") == "realizacja"
    prac = S.dane_prac()["pracownicy"]
    uz = {u["login"]: u for u in S.uzytkownicy_lista()}
    widziani = S.czytaj(S.F_WIDZIANI, {})
    wyn = []
    swoi = None if S.wlasciciel() else S.UWIERZ.czlonkowie_firmy()  # administrator konta – tylko konta swojej firmy (H1-01)
    for login in S.wszystkie_konta():
        if swoi is not None and login.lower() not in swoi:
            continue
        c_ = {**S.czytaj(S.F_CFG, {}), **({} if login == S.login_admina() else S.czytaj(S.plik_ustawien_konta(login), {}))}
        o = ostatnia.get(login) or {}
        wyn.append({"login": login, "admin": login == S.login_admina() if S.wlasciciel() else login == session.get("login"), "ksiegowosc": S.ma_ksiegowosc(login), "windykacja": S.ma_windykacje(login), "rola": "admin" if login == S.login_admina() else (uz.get(login) or {}).get("rola", ""),
                    "utworzono": (uz.get(login) or {}).get("utworzono", ""), "firma": c_.get("firma_nazwa", "") if login == S.login_admina() or
                    os.path.exists(S.plik_ustawien_konta(login)) else "", "nip": c_.get("firma_nip", "") if login != S.login_admina() or True else "",
                    **projekty_.get(login, {"projekty": 0, "realizacja": 0}),
                    "klienci": len([k for k in S.czytaj(S.F_KLIENCI.dla(login), []) if not k.get("archiwum")]),
                    "przetargi": len(S.czytaj(S.F_DB.dla(login), {})),
                    "pracownicy": sum(1 for p in prac if (p.get("wlasciciel") or S.login_admina()) == login and not p.get("archiwum")),
                    "ostatnia_aktywnosc": o.get("czas", ""), "ostatnia_akcja": o.get("akcja", ""),
                    "ostatnio_w_programie": widziani.get(login, ""), "wpisow": liczby.get(login, 0),
                    "ai_usd": round(S.zuzycie_ai_konta(login).get("usd", 0), 2), "ai_zapytan": S.zuzycie_ai_konta(login).get("zapytan", 0)})
    return jsonify({"konta": wyn, "jako": session.get("jako") or ""})


@bp.post("/api/admin/zakres")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel
def admin_zakres():
    """Zakres list administratora: „wszystkie” konta, „moje” albo login jednego konta."""
    z = str((request.json or {}).get("zakres") or "wszystkie")
    if z not in ("wszystkie", "moje") and z not in S.wszystkie_konta():
        return jsonify({"blad": "Nie ma takiego konta."}), 400
    session["admin_zakres"] = z
    return jsonify({"zakres": z})


@bp.post("/api/konta/jako")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel
def konta_jako():
    """Administrator przełącza się na podgląd / pracę na koncie użytkownika (albo wraca na swoje)."""
    login = str((request.json or {}).get("login") or "")
    if session.get("konto", "env") != "env":
        return jsonify({"blad": "Tylko główny administrator może przeglądać konta."}), 403
    if login and login not in S.wszystkie_konta():
        return jsonify({"blad": "Nie ma takiego konta."}), 404
    if login and login != S.login_admina():
        session["jako"] = login
        S.zapisz_aktywnosc(session.get("login"), "Administrator otworzył konto", konto=login)
    else:
        session.pop("jako", None)
    session.pop("prac_wszystkie", None)
    return jsonify({"jako": session.get("jako") or ""})


@bp.get("/api/konto/ustawienia")
@S.wymaga_logowania
def konto_ustawienia():
    c = S.cfg_surowy()
    return jsonify({"pola": [{"klucz": k, "etykieta": e, "typ": t} for k, e, t in S.KONTO_EDYCJA],
                    "wartosci": {k: (S.MASKA if c.get(k) else "") if t == "secret" else c.get(k) for k, _, t in S.KONTO_EDYCJA},
                    "konto": S.konto_biezace()})


@bp.post("/api/konto/tryb")
@S.wymaga_logowania
def konto_tryb():
    """Zapamiętuje ostatnio wybrany tryb (wykonawca / zamawiający / inwestor) – przy kolejnym wejściu program otwiera go od razu."""
    t = (request.json or {}).get("tryb")
    if t not in ("wykonawca", "zamawiajacy", "inwestor", "kosztorysant", "dotacje", "dostawca", "prawnik", "nieruchomosci", ""):
        return jsonify({"blad": "Nieznany tryb."}), 400
    S.zapisz_ustawienia({"ostatni_tryb": t}, login=session.get("login") if not session.get("jako") else None)
    return jsonify({"ok": True})


ZAKRESY_KONTA = {"stawka_rg": (0, 10000), "kp": (0, 500), "zysk": (0, 500), "gwarancja": (0, 240), "powiadomienia_min_ocena": (1, 10), "smtp_port": (1, 65535)}


@bp.post("/api/konto/ustawienia")
@S.wymaga_logowania
def konto_ustawienia_zapisz():
    zm = {}
    for k, _, t in S.KONTO_EDYCJA:
        if k not in (request.json or {}):
            continue
        v = request.json[k]
        if t == "secret" and v == S.MASKA:
            continue
        try:
            v = int(v) if t == "int" else float(str(v).replace(",", ".")) if t == "float" else bool(v) if t == "bool" else str(v)[:300]
        except (TypeError, ValueError):
            return jsonify({"blad": f"Nieprawidłowa wartość: {k}"}), 400
        zakres = ZAKRESY_KONTA.get(k)  # liczby spoza sensownego zakresu (np. port 0, ocena 50, ujemny zysk) – odmowa zamiast cichego zapisu
        if zakres and not (zakres[0] <= v <= zakres[1]) or (t == "float" and v != v):
            return jsonify({"blad": f"„{dict((x, e) for x, e, _ in S.KONTO_EDYCJA).get(k, k)}”: wartość spoza zakresu {zakres[0]:g}–{zakres[1]:g}." if zakres
                            else f"Nieprawidłowa wartość: {k}"}), 400
        zm[k] = v
    blad = BZ.sprawdz_ustawienia_smtp(zm.get("smtp_serwer"), zm.get("smtp_port"))  # H1-09: serwer poczty tylko publiczny, porty 25/465/587/2525
    if blad:
        return jsonify({"blad": blad}), 400
    S.zapisz_ustawienia(zm)
    return jsonify({"ok": True})


@bp.get("/api/role")
@S.wymaga_logowania
@S.tylko_admin
def role_lista():
    swoi = None if S.wlasciciel() else S.UWIERZ.czlonkowie_firmy()  # administrator konta: liczba osób tylko w jego firmie
    uz = [u for u in S.uzytkownicy_lista() if swoi is None or str(u.get("login", "")).lower() in swoi]
    return jsonify({"role": S.role_firmy(), "moduly": S.UPR.MODULY, "poziomy": S.UPR.POZIOMY, "edycja": S.wlasciciel(),
                    "uzycie": {k: sum(1 for u in uz if u.get("rola") == k) for k in S.role_firmy()}})


@bp.post("/api/role")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel
def role_zapisz():
    """Role są wspólne dla wszystkich firm – zmienia je tylko właściciel programu (H1-01)."""
    j = request.json or {}
    rid = str(j.get("id") or "").strip()
    if j.get("usun"):
        if rid in S.UPR.ROLE_WBUDOWANE:
            return jsonify({"blad": "Ról wbudowanych nie można usunąć (można je zmienić)."}), 400
        if any(u.get("rola") == rid for u in S.uzytkownicy_lista()):
            return jsonify({"blad": "Rola jest przypisana użytkownikom – najpierw zmień im rolę."}), 400
        with S.BLOKADA:
            r = S.czytaj(S.F_ROLE, {})
            r.pop(rid, None)
            S.pisz(S.F_ROLE, r)
        return jsonify({"ok": True})
    if rid == "admin":
        return jsonify({"blad": "Roli administratora nie można zmieniać."}), 400
    if not rid:
        rid = re.sub(r"[^a-z0-9_]", "_", str(j.get("nazwa", "")).lower().translate(str.maketrans("ąćęłńóśźż", "acelnoszz")))[:30].strip("_")
    if not rid or not str(j.get("nazwa", "")).strip():
        return jsonify({"blad": "Podaj nazwę roli."}), 400
    if not re.fullmatch(r"[a-z0-9][a-z0-9_]{0,29}", rid):  # identyfikator trafia do atrybutów onclick na ekranie ról – tylko litery, cyfry i „_”
        return jsonify({"blad": "Nieprawidłowy identyfikator roli (dozwolone: małe litery bez polskich znaków, cyfry, „_”)."}), 400
    try:
        upr = {m: max(0, min(2, int(v))) for m, v in (j.get("uprawnienia") or {}).items() if m in S.UPR.MODULY}
    except (TypeError, ValueError, AttributeError):
        return jsonify({"blad": "Poziom uprawnień: 0 (brak), 1 (podgląd) albo 2 (edycja)."}), 400
    with S.BLOKADA:
        r = S.czytaj(S.F_ROLE, {})
        r[rid] = {"nazwa": str(j["nazwa"]).strip()[:60], "opis": str(j.get("opis", ""))[:150], "uprawnienia": upr,
                  "ai": bool(j.get("ai")), "raporty": bool(j.get("raporty", True))}
        S.pisz(S.F_ROLE, r)
    return jsonify({"ok": True, "id": rid})


@bp.get("/api/uzytkownicy")
@S.wymaga_logowania
@S.tylko_admin
def uzytkownicy():
    """Właściciel programu – wszyscy użytkownicy; administrator konta – tylko osoby ze swojej firmy (bez siebie)."""
    wl = S.wlasciciel()
    swoi = None if wl else S.UWIERZ.czlonkowie_firmy()
    ja = str(session.get("login") or "").lower()
    return jsonify([{k: u.get(k) for k in ("login", "rola", "utworzono")} | {"modul": S.modul_konta(u.get("login")),
                    "haslo_tymczasowe": bool(u.get("haslo_tymczasowe"))} | ({"firma": S.UWIERZ.firma_id(u.get("login"))} if wl else {})
                    for u in S.uzytkownicy_lista() if wl or (str(u.get("login", "")).lower() in swoi and str(u.get("login", "")).lower() != ja)])


def _uzytkownik_firmy(login):
    """Czy zalogowany może zarządzać kontem „login”: właściciel – każdym; administrator konta – osobą ze swojej firmy, która nie jest
    administratorem i nie jest nim samym. Zwraca komunikat odmowy albo None."""
    if S.wlasciciel():
        return None
    lg = str(login or "").lower()
    if lg == str(session.get("login") or "").lower():
        return "Swoje konto zmieniasz w „Zmień hasło” – rolę i dostęp zmienia właściciel programu."
    u = S.UWIERZ._uzytkownik(login)
    if not u or lg not in S.UWIERZ.czlonkowie_firmy():
        return None if not u else "Nie ma takiego użytkownika w Twojej firmie."
    if u.get("rola") == "admin":
        return "Administratora konta może zmienić tylko właściciel programu."
    return None


@bp.post("/api/uzytkownicy")
@S.wymaga_logowania
@S.tylko_admin
def uzytkownik_zapisz():
    login = str(request.json.get("login", "")).strip()
    haslo = str(request.json.get("haslo", "")).strip()
    rola = str(request.json.get("rola") or "uzytkownik")  # lista / liczba w polu – nieznana rola (400), nie błąd 500
    modul = request.json.get("modul")  # dostęp tylko do jednego modułu („” – wszystkie; brak pola – bez zmiany)
    modul = None if modul is None else str(modul)
    if modul is not None and modul not in S.UWIERZ.MODULY_KONTA:
        return jsonify({"blad": "Nieznany moduł."}), 400
    if modul and S.EDYCJA != "pelna" and modul != "gmina":
        return jsonify({"blad": "W tej edycji programu jest tylko moduł zamawiającego publicznego."}), 400
    if not re.fullmatch(r"[\w.\-@]{3,40}", login):
        return jsonify({"blad": "Login: 3–40 znaków (litery, cyfry, . - _ @), bez spacji."}), 400
    if rola not in S.role_firmy():
        return jsonify({"blad": "Nieznana rola."}), 400
    if login.lower() == os.environ.get("APP_USER", "").strip().lower():
        return jsonify({"blad": "Ten login należy do administratora z Rendera."}), 400
    if rola == "admin" and not S.wlasciciel():  # H1-01: rolę „Administrator” nadaje tylko właściciel programu
        return jsonify({"blad": "Rolę „Administrator” może nadać tylko właściciel programu."}), 403
    odm = _uzytkownik_firmy(login)
    if odm:
        return jsonify({"blad": odm}), 403
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        u = next((x for x in lista if x["login"].lower() == login.lower()), None)
        if u and not S.wlasciciel() and login.lower() not in S.UWIERZ.czlonkowie_firmy():
            return jsonify({"blad": "Ten login jest już zajęty – wybierz inny."}), 400
        if not u and len(haslo) < 10:
            return jsonify({"blad": "Hasło musi mieć co najmniej 10 znaków."}), 400
        if haslo and len(haslo) < 10:
            return jsonify({"blad": "Hasło musi mieć co najmniej 10 znaków."}), 400
        if not u:
            osieroc_dane_konta(login)  # dane po dawnym koncie z tym loginem (usuniętym przed tą poprawką) – nie dla nowego konta
            # wersja od czasu utworzenia: sesja (ciasteczko) usuniętego konta z tym samym loginem nie pasuje do nowego konta
            u = {"login": login, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wersja": int(S.time.time() * 1_000_000),
                 # firma nowego konta: administrator konta zakłada osoby w swojej firmie; właściciel – w swojej (rola „Administrator” = nowa firma)
                 "firma": "" if S.wlasciciel() else S.UWIERZ.firma_id(session.get("login"))}
            lista.append(u)
        if S.wlasciciel() and rola == "admin" and u.get("rola") != "admin" and not u.get("firma"):
            u["firma"] = u["login"]  # administrator konta nadany przez właściciela – osobna firma (zarządza tylko nią)
        u["rola"] = rola
        if modul is not None:
            u["modul"] = modul
        if haslo:
            u["hash"] = S.hash_hasla(haslo)
            u.pop("haslo_tymczasowe", None)
            u.pop("tymczasowe_do", None)
        u["wersja"] = u.get("wersja", 0) + 1  # wylogowuje tę osobę na innych urządzeniach
        S.pisz(S.F_UZYT, lista)
    return jsonify({"ok": True})


@bp.post("/api/uzytkownicy/windykacja")
@S.wymaga_logowania
def uzytkownik_windykacja():
    """Udostępnienie / odebranie modułu Windykacja kontu – tylko właściciel programu (dane konta zostają zachowane)."""
    if not S.wlasciciel():
        return jsonify({"blad": "Windykację udostępnia tylko właściciel programu."}), 403
    j = request.json or {}
    login = str(j.get("login") or "")
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        u = next((x for x in lista if x.get("login") == login), None)
        if not u:
            return jsonify({"blad": "Nie ma takiego konta."}), 404
        u["windykacja"] = bool(j.get("dostep"))
        S.pisz(S.F_UZYT, lista)
    return jsonify({"ok": True, "login": login, "windykacja": u["windykacja"]})


@bp.post("/api/uzytkownicy/ksiegowosc")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel
def uzytkownik_ksiegowosc():
    """Udostępnienie / odebranie modułu Księgowość kontu (tylko administrator; dane konta zostają zachowane)."""
    j = request.json or {}
    login = str(j.get("login") or "")
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        u = next((x for x in lista if x.get("login") == login), None)
        if not u:
            return jsonify({"blad": "Nie ma takiego konta."}), 404
        u["ksiegowosc"] = bool(j.get("dostep"))
        S.pisz(S.F_UZYT, lista)
    S.logging.info("Księgowość: %s dostęp dla %s", "nadano" if u["ksiegowosc"] else "odebrano", login)
    return jsonify({"ok": True, "login": login, "ksiegowosc": u["ksiegowosc"]})


def osieroc_dane_konta(login):
    """Dane konta (usuniętego albo sprzed jego ponownego założenia) przechodzą na właściciela „usuniete:<login>:<czas>” – nowe konto
    z tym samym loginem startuje bez nich, a administrator nadal widzi je na liście wszystkich projektów (Konta i aktywność, filtr „wszystkie”).
    Projekty: pole „wlasciciel”, login usunięty z udostępnień; katalog DATA/konta/<login>; pracownicy; listy płac; raporty; limit AI.
    Zwraca liczbę przeniesionych elementów."""
    lg = str(login or "").strip().lower()
    if not lg or lg == S.login_admina().lower():
        return 0
    nowy = f"usuniete:{login}:{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"
    ile = 0
    with S.BLOKADA:
        for pid in sorted(os.listdir(S.PROJ)) if os.path.isdir(S.PROJ) else []:
            sc = os.path.join(S.PROJ, pid, "projekt.json")
            m = S.czytaj(sc, None)
            if not isinstance(m, dict):
                continue
            zm = False
            if str(m.get("wlasciciel") or "").lower() == lg:
                m["wlasciciel"], m["usuniete_konto"] = nowy, login
                zm = True
            if any(str(x).lower() == lg for x in (m.get("dostep") or [])):
                m["dostep"] = [x for x in m["dostep"] if str(x).lower() != lg]
                zm = True
            if zm:
                S.pisz(sc, m)
                ile += 1
        stary = S.katalog_konta(login)
        if os.path.isdir(stary) and os.path.abspath(stary) != os.path.abspath(S.DATA):
            os.rename(stary, S.katalog_konta(nowy))
            ile += 1
        d = S.czytaj(S.F_PRAC, None)
        if isinstance(d, dict):
            pr = [p for p in d.get("pracownicy", []) if str(p.get("wlasciciel") or "").lower() == lg]
            for p in pr:
                p["wlasciciel"] = nowy
            if pr:
                S.pisz(S.F_PRAC, d)
                ile += len(pr)
        pl = S.czytaj(S.F_PLACE, None)
        if isinstance(pl, dict):
            lk = pl.get("listy_konta") or {}
            k_ = [k for k in lk if str(k).lower() == lg]
            for k in k_:
                lk[nowy] = lk.pop(k)
            if k_:
                S.pisz(S.F_PLACE, pl)
                ile += 1
        rap = os.path.join(S.DATA, "raporty")
        for n in os.listdir(rap) if os.path.isdir(rap) else []:
            if n.lower() == lg:
                os.rename(os.path.join(rap, n), os.path.join(rap, nowy))
                ile += 1
        glob_ = S.czytaj(S.F_CFG, {}) or {}
        lim = glob_.get("limity_ai") or {}
        if any(str(k).lower() == lg for k in lim):
            glob_["limity_ai"] = {k: v for k, v in lim.items() if str(k).lower() != lg}
            S.pisz(S.F_CFG, glob_)
    if ile:
        S.logging.info("Dane konta %s przeniesione na właściciela %s (%s elementów)", login, nowy, ile)
    return ile


@bp.post("/api/uzytkownicy/usun")
@S.wymaga_logowania
@S.tylko_admin
def uzytkownik_usun():
    login = str(request.json.get("login", "")).lower()
    odm = _uzytkownik_firmy(login)
    if odm or (not S.wlasciciel() and login not in S.UWIERZ.czlonkowie_firmy()):
        return jsonify({"blad": odm or "Nie ma takiego użytkownika w Twojej firmie."}), 403
    with S.BLOKADA:
        u = next((x for x in S.uzytkownicy_lista() if x["login"].lower() == login), None)
        S.pisz(S.F_UZYT, [u for u in S.uzytkownicy_lista() if u["login"].lower() != login])
        ile = osieroc_dane_konta(u["login"]) if u else 0  # dane nie przechodzą na nowe konto z tym samym loginem
    return jsonify({"ok": True, "przeniesiono": ile})


@bp.get("/api/ustawienia")
@S.wymaga_logowania
def ustawienia():
    c = S.cfg_surowy()
    etykiety = {"auto_szukaj": "Szukaj automatycznie w dni robocze (godzina: AUTO_SZUKAJ_GODZINA, domyślnie 7:00)",
                "smtp_serwer": "Serwer SMTP (np. smtp.gmail.com, smtp.office365.com – dane podaje dostawca poczty)",
                "smtp_haslo": "Hasło SMTP (dla Gmaila: 16-znakowe hasło aplikacji) – zapisywane na serwerze, niewidoczne w przeglądarce",
                "auto_ocena": "Automatycznie oceniaj nowe ogłoszenia przez AI"}
    wyn = {"pola": [{"klucz": k, "etykieta": etykiety.get(k, e), "typ": t} for k, e, t in S.POLA], "wartosci": {}}
    for k in S.POLA_WEB:
        v = c.get(k)
        if k in S.SEKRETY:
            v = S.MASKA if v else ""
        wyn["wartosci"][k] = v
    cd = S.cfg()
    wyn["wykonawca"] = {"nazwa": cd.get("firma_nazwa"), "adres": cd.get("firma_adres"), "regon": cd.get("firma_regon"),
                        "z_wykazu": cd.get("firma_nazwa") != c.get("firma_nazwa") or bool(S.wykaz(c.get("firma_nip")))}
    wyn["klucz_z_serwera"] = bool(os.environ.get("ANTHROPIC_API_KEY"))
    wyn["ukrytych"] = len(c.get("ukryte", []))
    return jsonify(wyn)


@bp.post("/api/ustawienia")
@S.wymaga_logowania
def ustawienia_zapisz():
    if True:
        c = {}
        typy = {k: t for k, _, t in S.POLA}
        admin_programu = session.get("konto", "env") == "env" and S.rola_sesji() == "admin"
        for k, v in request.json.items():
            if k not in typy:
                continue
            if k in S.GLOBALNE and not admin_programu:  # ustawienia wspólne programu (klucz API, modele, marka) – tylko administrator programu
                continue
            t = typy[k]
            if k in S.SEKRETY and (v == S.MASKA):
                continue
            try:
                if t == "int":
                    v = int(v)
                elif t == "float":
                    v = float(str(v).replace(",", "."))
                elif t == "bool":
                    v = bool(v)
                elif t == "lines":
                    v = [x.strip() for x in (v if isinstance(v, list) else str(v).splitlines()) if x.strip()]
                elif t.startswith("wybor:"):
                    dozw = [x.split("=")[0] for x in t[6:].split("|")]
                    if str(v) not in dozw:
                        return jsonify({"blad": f"Nieprawidłowa wartość w polu: {k}"}), 400
                    v = str(v)
                elif t == "places":
                    lista = []
                    for linia in (v if isinstance(v, list) else str(v).splitlines()):
                        if isinstance(linia, list):
                            lista.append(linia)
                            continue
                        if not linia.strip():
                            continue
                        cz = [x.strip() for x in linia.split(";")]
                        lista.append([cz[0], float(cz[1].replace(",", ".")), float(cz[2].replace(",", "."))])
                    v = lista
                else:
                    v = str(v).strip()
            except (ValueError, IndexError, TypeError, AttributeError):  # np. lista zamiast liczby – 400, nie błąd 500
                return jsonify({"blad": f"Błędna wartość w polu: {k}"}), 400
            c[k] = v
        blad = BZ.sprawdz_ustawienia_smtp(c.get("smtp_serwer"), c.get("smtp_port"))  # H1-09
        if blad:
            return jsonify({"blad": blad}), 400
        if request.json.get("przywroc_ukryte"):
            c["ukryte"] = []
        S.zapisz_ustawienia(c)
    S._odswiez_firme_po_zapisie()
    return jsonify({"ok": True})


def ustawienia_pogody(pid, r=None):
    r = r or S.realizacja_dane(pid)
    u = dict(r.get("pogoda") or {})
    u.setdefault("rodzaj", "elewacja")
    kr = {**S.POG.PRESETY.get(u["rodzaj"], S.POG.PRESETY["elewacja"]), **(u.get("kryteria") or {})}
    kr.update(godz_od=int(u.get("godz_od", 7)), godz_do=int(u.get("godz_do", 17)))
    u["kryteria"] = kr
    if not u.get("lat"):
        w = S.wspolrzedne(pid, r)  # z adresu budowy
        if w:
            u.update(lat=w["lat"], lon=w["lon"], opis=u.get("opis") or r.get("adres") or "adres budowy")
    return u


@bp.get("/api/archiwum")
@S.wymaga_logowania
def archiwum():
    login, rola = session.get("login"), S.rola_sesji()
    proj, pliki, dziennik, usterki = [], [], [], []
    real_odczyt = S.moze("realizacja", 1)
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if not m or not S.ma_dostep(m, login, rola, lista=True):
            continue
        if m.get("archiwum"):
            proj.append({"id": pid, "nazwa": m.get("nazwa"), "typ": m.get("typ") or "przetarg", "data": m.get("archiwum_data"),
                         "kto": m.get("archiwum_kto")})
        for f in m.get("archiwum_plikow", []):
            pliki.append({**f, "pid": pid, "projekt": m.get("nazwa")})
        r = S.czytaj(os.path.join(S.PROJ, pid, "realizacja.json"), {})
        if not isinstance(r, dict):
            r = {}
        for z in r.get("zdjecia", []):
            if z.get("archiwum"):
                pliki.append({"id": "zdj:" + z["id"], "pid": pid, "projekt": m.get("nazwa"), "oryginal": "zdjęcie: " + (z.get("opis") or z["plik"]),
                              "plik": f"realizacja/zdjecia/{z['plik']}", "data": z.get("archiwum_data")})
        if real_odczyt:  # historia raportów dziennych i usunięte usterki – tylko z dostępem do modułu Realizacja (jak na ekranie budowy)
            for i, h in enumerate(r.get("dziennik_historia") or []):
                if isinstance(h, dict) and h.get("data"):
                    dziennik.append({"id": _id_hist(i, h), "pid": pid, "projekt": m.get("nazwa"), "data": h.get("data"), "wersja": h.get("wersja") or 1,
                                     "powod": h.get("powod") or "zmieniony", "zastapiono": h.get("zastapiono") or "", "kto": h.get("kto_zmienil") or "",
                                     "autor": h.get("autor") or "", "zapisano": h.get("zapisano") or "",
                                     **{k: str(h.get(k) or "") for k in POLA_RAPORTU}})
            for u in r.get("usterki_archiwum") or []:
                if isinstance(u, dict) and u.get("id"):
                    usterki.append({k: u.get(k) for k in ("id", "typ", "tytul", "opis", "lokalizacja", "osoba", "termin", "status", "zgloszono", "kto",
                                                           "archiwum_data", "archiwum_kto")} | {"pid": pid, "projekt": m.get("nazwa")})
    return jsonify(S.ukryj_innych({"projekty": sorted(proj, key=lambda x: x.get("data") or "", reverse=True),
                    "pliki": sorted(pliki, key=lambda x: x.get("data") or "", reverse=True),
                    "klienci": [k for k in S.klienci_lista() if k.get("archiwum")] if S.moze("klienci", 1) else [],  # bez dostępu do modułu – bez jego danych
                    "pracownicy": [{k: p.get(k) for k in ("id", "imie", "stanowisko", "archiwum_data")} for p in S.dane_prac_konta()["pracownicy"] if p.get("archiwum")]
                    if S.moze("pracownicy", 1) else [],
                    "dziennik": sorted(dziennik, key=lambda x: x.get("zastapiono") or "", reverse=True),
                    "usterki": sorted(usterki, key=lambda x: x.get("archiwum_data") or "", reverse=True),
                    "przywracanie": not S.UWIERZ.tylko_odczyt() and S.moze("archiwum", 2),
                    # raporty dzienne i usterki przywraca rola z edycją Realizacji (jak przy zapisie na ekranie budowy); podgląd – tylko do odczytu
                    "przywracanie_realizacji": not S.UWIERZ.tylko_odczyt() and S.moze("realizacja", 2),
                    "trwale": rola == "admin"}))


POLA_RAPORTU = ("pogoda", "pracownicy", "prace", "materialy", "sprzet", "uwagi")  # pola raportu dziennego (jak POLA_DZIENNIKA w trasy_realizacja.py)


def _id_hist(i, h):
    """Identyfikator wersji z historii raportów: pozycja + data raportu + chwila zastąpienia (sprawdzane przy przywróceniu)."""
    return f"dzh:{i}:{h.get('data') or ''}:{h.get('zastapiono') or ''}"


def _przywroc_realizacje(rodzaj, pid, id_):
    """Przywrócenie wersji raportu dziennego z historii albo usuniętej usterki. Zwraca tekst błędu albo None.
    Raport: obecna wersja z tego dnia (jeśli jest) trafia do historii, przywrócona staje się bieżącą – historia niczego nie traci."""
    teraz, kto = dt.datetime.now().strftime("%Y-%m-%d %H:%M"), session.get("login", "")
    with S.BLOKADA:
        r = S.realizacja_pelna(pid)
        if rodzaj == "dziennik":
            hist = r.get("dziennik_historia") or []
            try:
                _, i, data, zast = str(id_).split(":", 3)
                h = hist[int(i)]
            except (ValueError, IndexError, TypeError):
                return "Nie ma takiej wersji raportu w historii."
            if not isinstance(h, dict) or h.get("data") != data or (h.get("zastapiono") or "") != zast:
                return "Nie ma takiej wersji raportu w historii (historia się zmieniła – odśwież Archiwum)."
            stary = next((x for x in r["dziennik"] if x.get("data") == data), None)
            if stary:
                hist.append(dict(stary, zastapiono=teraz, kto_zmienil=kto, powod="zastąpiony przywróconą wersją"))
            w = {"data": data, "autor": h.get("autor") or kto, "zapisano": teraz, "przywrocono_z": h.get("zastapiono") or "",
                 "zdjecia": [z for z in (h.get("zdjecia") or []) if isinstance(z, str)][:20], **{k: str(h.get(k) or "") for k in POLA_RAPORTU}}
            if w["autor"] != kto:
                w["zmienil"] = kto
            r["dziennik_historia"] = hist
            w["wersja"] = sum(1 for x in hist if x.get("data") == data) + 1
            r["dziennik"] = sorted([x for x in r["dziennik"] if x.get("data") != data] + [w], key=lambda x: x.get("data") or "")
        else:
            arch = r.get("usterki_archiwum") or []
            u = next((x for x in arch if isinstance(x, dict) and x.get("id") == id_), None)
            if not u:
                return "Nie ma takiej usterki w archiwum."
            arch.remove(u)
            u = {k: v for k, v in u.items() if k not in ("archiwum_data", "archiwum_kto")}
            if any(x.get("id") == u["id"] for x in r["usterki"]):
                u["id"] = uuid.uuid4().hex[:10]
            u["przywrocono"] = teraz
            r["usterki"].append(u)
            r["usterki_archiwum"] = arch
        S.zapisz_realizacje(pid, r)
    return None


@bp.post("/api/archiwum/przywroc")
@S.wymaga_logowania
def archiwum_przywroc():
    j = request.json or {}
    if j.get("rodzaj") in ("projekt", "plik"):
        # projekt: sprawdzany jest ten sam identyfikator, który zostanie przywrócony (pole „id”) – nie „pid” z żądania
        # (dotąd „pid” własnego projektu przepuszczał przywrócenie cudzego projektu podanego w „id”)
        pid_ = str((j.get("id") if j.get("rodzaj") == "projekt" else j.get("pid")) or "x")
        m = S.czytaj(os.path.join(S.PROJ, os.path.basename(pid_), "projekt.json"), None)
        if not m or not S.ma_dostep(m):
            return jsonify({"blad": "Nie masz dostępu do tego projektu."}), 404
        modul_ = "realizacja" if j.get("rodzaj") == "plik" and str(j.get("id") or "").startswith("zdj:") else "projekty"
        if not S.moze(modul_, 2):  # przywrócenie zmienia projekt – wymaga edycji modułu (nie wystarczy podgląd)
            return jsonify({"blad": f"Brak uprawnień do modułu „{S.UPR.MODULY[modul_]}” (edycja). Poproś administratora o zmianę roli."}), 403
    elif j.get("rodzaj") in ("dziennik", "usterka"):  # historia raportu dziennego / usunięta usterka – jak zapis na ekranie budowy (edycja Realizacji)
        return przywroc_realizacje(str(j.get("pid") or "x"))
    elif j.get("rodzaj") in ("klient", "pracownik"):  # klient – moduł Klienci, pracownik – moduł Pracownicy (edycja), jak przy zwykłym zapisie
        modul_ = "klienci" if j.get("rodzaj") == "klient" else "pracownicy"
        if not S.moze(modul_, 2):
            return jsonify({"blad": f"Brak uprawnień do modułu „{S.UPR.MODULY[modul_]}” (edycja). Poproś administratora o zmianę roli."}), 403
    blad = S._archiwum_akcja(j, False)
    return (jsonify({"blad": blad}), 400) if blad else jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/realizacja/przywroc")
@S.wymaga_logowania
def przywroc_realizacje(pid):
    """Przywrócenie z Archiwum wersji raportu dziennego albo usuniętej usterki. Adres w module Realizacja – uprawnienia jak przy zapisie
    raportu i usterki na ekranie budowy (edycja Realizacji), niezależnie od poziomu modułu Archiwum."""
    j = request.json or {}
    if j.get("rodzaj") not in ("dziennik", "usterka"):
        return jsonify({"blad": "Nieznany rodzaj."}), 400
    pid = os.path.basename(str(pid))
    m = S.czytaj(os.path.join(S.PROJ, pid, "projekt.json"), None)
    if not m or not S.ma_dostep(m):
        return jsonify({"blad": "Nie masz dostępu do tego projektu."}), 404
    if S.UWIERZ.tylko_odczyt() or not S.moze("realizacja", 2):
        return jsonify({"blad": f"Brak uprawnień do modułu „{S.UPR.MODULY['realizacja']}” (edycja). Poproś administratora o zmianę roli."}), 403
    blad = _przywroc_realizacje(j["rodzaj"], pid, j.get("id"))
    return (jsonify({"blad": blad}), 400) if blad else jsonify({"ok": True})


@bp.post("/api/archiwum/usun")
@S.wymaga_logowania
@S.tylko_admin
def archiwum_usun():
    """Trwałe usunięcie – tylko administrator i tylko elementów, które są już w archiwum."""
    blad = S._archiwum_akcja(request.json or {}, True)
    return (jsonify({"blad": blad}), 400) if blad else jsonify({"ok": True})
