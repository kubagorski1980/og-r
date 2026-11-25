# -*- coding: utf-8 -*-
"""
Bidivia – wersja internetowa.
Serwer Flask z logowaniem, API dla przeglądarki i zadaniami w tle.
Korzysta z tej samej logiki co program na Windows (moduły modul_*.py).

Zmienne środowiskowe:
  APP_USER, APP_PASSWORD      – login i hasło (albo APP_PASSWORD_HASH z ustaw_haslo.py)
  ANTHROPIC_API_KEY           – klucz API Claude (można też wpisać w Ustawieniach)
  SECRET_KEY                  – klucz sesji (jeśli brak, generowany i zapisywany w DATA_DIR)
  DATA_DIR                    – katalog danych (domyślnie /data)
  COOKIE_SECURE               – 1 (domyślnie) = ciasteczko tylko przez https; 0 do testów lokalnych
  AUTO_SZUKAJ_GODZINA         – godzina automatycznego wyszukiwania w dni robocze (domyślnie 7, -1 = wyłącz)
"""
import calendar
import datetime as dt
import statistics
import hashlib
import logging
import hmac
import json
import math
import os
import re
import secrets
import shutil
import threading
import time
import socket
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid
from functools import wraps
from importlib.machinery import SourceFileLoader

import tk_stub  # noqa: F401  (musi być przed modułami programu)

from flask import Flask, Response, abort, g, has_request_context, jsonify, redirect, request, send_file, send_from_directory, session
from werkzeug.utils import secure_filename

BASE = os.path.dirname(os.path.abspath(__file__))
core = SourceFileLoader("agent_core", os.path.join(BASE, "agent_przetargowy.pyw")).load_module()
import modul_oferty as MO  # noqa: E402
import modul_materialy as MM  # noqa: E402
import modul_harmonogram as MH  # noqa: E402
import ceny_rynkowe as CR  # noqa: E402
import bip as BIP  # noqa: E402
import region as REG  # noqa: E402
import umowa as UM  # noqa: E402
import bzp as BZ  # noqa: E402
import budowa as BUD  # noqa: E402
import kontrola as KON  # noqa: E402
import place as PL  # noqa: E402
import nip as NIP  # noqa: E402
import analiza as AN  # noqa: E402
import bk as BKM  # noqa: E402
import pogoda as POG  # noqa: E402
import prawnik as PRW  # noqa: E402
import lista_kontroli as LK  # noqa: E402  jedna lista kontrolna: kreator, weryfikacja, prawnik
import rynkowosc as RY  # noqa: E402
import ted as TED  # noqa: E402
import leady as LD  # noqa: E402
import plan_zamowien as PZ  # noqa: E402
import szacowanie as SZ  # noqa: E402
import windykacja as WK  # noqa: E402
import ksiegowosc as KS_MOD  # noqa: E402
import sprawozdanie_uzp as SPR  # noqa: E402
import ochrona_ludnosci as OL  # noqa: E402
import odwolania_przetargi as OP  # noqa: E402  (nie mylić z odwolania.py = OD – cytaty w analizach)
import wnioski as WN  # noqa: E402
import rozbieznosci as ROZB  # noqa: E402
import cennik_wlasny as CW  # noqa: E402
import dotacje as DOT  # noqa: E402
import podwykonawcy as PW  # noqa: E402
import harmonogramy as HN  # noqa: E402
import historia_zam as HZ  # noqa: E402
import weryfikacja as WER  # noqa: E402
import zaproszenia as ZP  # noqa: E402
import finansowanie as FIN  # noqa: E402
import wspolnota as WSPOL  # noqa: E402  (wspólnoty, spółdzielnie, deweloperzy – osobne reguły, bez Pzp)
import dostawy as DS  # noqa: E402
import ocena_ofert as OO  # noqa: E402
import odwolania as OD  # noqa: E402
import wspolne as W  # noqa: E402
import zapytania as ZQ  # noqa: E402
import dotacje_plan as DP  # noqa: E402
import ogloszenie_wykonania as OW  # noqa: E402
import progi as PR  # noqa: E402
import kreator_zam as KZ  # noqa: E402
import nieruchomosci as NR  # noqa: E402
import zamawiajacy as ZAM  # noqa: E402
import postepowanie_zam as PZ_  # noqa: E402  (terminy pytań do SWZ – wykonawca)
import uprawnienia as UPR  # noqa: E402
import reguly_zamowien as RZ  # noqa: E402  reguły gminy (Pzp) i wspólnoty (bez Pzp)
import copy  # noqa: E402
import collections  # noqa: E402
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)

from dane import (  # noqa: E402,F401  warstwa danych (rdzeń) – dane.py; jawna lista, żeby analiza statyczna wykrywała brakujące nazwy
    BIP_BLOKADA, BLOKADA, DATA, DIR_FIRMA, DIR_KADRY, DIR_KONT, F_AKTYWNOSC, F_BIP, F_CENNIK_W, F_CENY_DOS, F_CFG, F_DB, F_DECYZJE, F_FIRMA,
    F_HIST, F_KLIENCI, F_NIP_CACHE, F_PLACE, F_POWIAD, F_PRAC, F_ROLE, F_SEKRET, F_UZYT, F_WIDZIANI, F_WIZYTY, MASKA, PAMIEC_LIMIT, PROJ,
    ROLE, SEKRETY, STREFA, SciezkaKonta, _KONTEKST, _PAMIEC, _PAMIEC_BLOKADA, _WEJSCIA, _WIDZIANI, _czytaj_wspolne, czytaj, czytaj_ro,
    katalog_konta, konto_admina, konto_biezace, meta, pdir, pisz, projekty_ro, zapisz_meta,
)
import dane as DANE  # noqa: E402  zmiany ustawień warstwy danych (np. DANE.PAMIEC_LIMIT) – w module, nie w kopii nazw

from konfiguracja import (  # noqa: E402,F401  konfiguracja (rdzeń) – konfiguracja.py
    DOMYSLNE_WEB, F_KOSZTY_ZADAN, F_ZUZYCIE_AI, GLOBALNE, _BLOKADA_AI, _ODSWIEZANE, cfg, cfg_surowy, plik_ustawien_konta,
    rejestruj_zuzycie_ai, sprawdz_limit_ai, wykaz, zapisz_cfg, zapisz_ustawienia, zuzycie_ai_konta,
)
import konfiguracja as KONF  # noqa: E402  zmiany ustawień modułu konfiguracji – w module, nie w kopii nazw


app = Flask(__name__, static_folder=os.path.join(BASE, "static"), static_url_path="/static")

# ================================================================ EDYCJE PROGRAMU
# „pelna” – cały program (domyślnie); „zamawiajacy” – wersja dla urzędu: tylko ścieżka zamawiającego (przygotowanie
# zamówienia, sprawdzenie ofert, realizacja umów) + wspólne (konta, role, archiwum, ustawienia, instrukcja).
# Ustawiane zmienną środowiskową BIDIVIA_EDYCJA przy instalacji – użytkownik programu jej nie zmieni.
EDYCJE = {"pelna": "Bidivia", "zamawiajacy": "Bidivia – Zamawiający"}
EDYCJA = (os.environ.get("BIDIVIA_EDYCJA") or "pelna").strip().lower()
if EDYCJA not in EDYCJE:
    EDYCJA = "pelna"
# moduły innych ścieżek – w edycji zamawiającego niedostępne (adresy API i stron)
ZABLOKOWANE_W_EDYCJI = {"zamawiajacy": (
    "/api/przetargi", "/api/bip", "/api/bk", "/api/bzp", "/api/wspolne", "/api/alerty", "/api/historia", "/api/wyniki-ofert", "/api/raporty",
    "/api/obszar", "/api/dostawy", "/api/hurtownie", "/api/klienci", "/api/pracownicy", "/api/godziny", "/api/kadry", "/api/place",
    "/api/dotacje", "/api/zapytania", "/api/nier", "/api/ksieg", "/api/odw", "/api/leady", "/api/wind", "/oferta")}
# rodzaje projektów zamawiającego (projekty innych rodzajów są w tej edycji niewidoczne)
TYPY_EDYCJI_ZAM = ("zamowienie", "inwestorski", "weryfikacja", "dokumentacja", "inwestycja", "ocena_ofert")


def projekt_w_edycji(m):
    """Czy projekt należy do bieżącej edycji (w pełnej – każdy) i do modułu, do którego ograniczono konto (jeśli ograniczono)."""
    if not projekt_modulu(m, modul_konta()):
        return False
    if EDYCJA == "pelna":
        return True
    return (m or {}).get("strona") == "zamawiajacy" or (m or {}).get("typ") in TYPY_EDYCJI_ZAM


@app.before_request
def blokada_edycji():
    if EDYCJA == "pelna":
        return None
    sc = request.path
    if any(sc == z or sc.startswith(z + "/") or sc.startswith(z + "?") for z in ZABLOKOWANE_W_EDYCJI.get(EDYCJA, ())) \
            or (sc == "/api/projekty" and request.method == "POST"
                and (request.get_json(silent=True) or {}).get("typ") not in TYPY_EDYCJI_ZAM):  # nowy projekt innego typu (np. przetarg) – tylko w pełnej edycji
        if sc.startswith("/api/"):
            return jsonify({"blad": f"Ta funkcja nie jest dostępna w edycji „{EDYCJE[EDYCJA]}”."}), 404
        abort(404)
    cz = sc.split("/")
    if len(cz) >= 4 and cz[1] == "api" and cz[2] == "projekty" and cz[3]:
        m_ = czytaj(os.path.join(PROJ, os.path.basename(cz[3]), "projekt.json"), None)
        if m_ is not None and not projekt_w_edycji(m_):
            return jsonify({"blad": "Projekt niedostępny w tej edycji programu."}), 404
    return None


# ================================================================ KONTO OGRANICZONE DO JEDNEGO MODUŁU
# Administrator może nadać kontu dostęp tylko do jednego modułu (np. „Dla wspólnot”): pozostałe ścieżki znikają z interfejsu,
# a serwer blokuje ich adresy, projekty innych modułów i tworzenie projektów innego rodzaju.
SCIEZKA_ZAM = ("/api/zam", "/api/plan", "/api/olioc", "/api/sprawozdanie")  # tylko ścieżka zamawiającego
KONTA_I_ROLE = ("/api/uzytkownicy", "/api/role")  # konto ograniczone nie zarządza kontami (nawet z rolą administratora)
SZUKANIE_PRZETARGOW = ("/api/przetargi", "/api/bip", "/api/bk", "/api/bzp", "/api/alerty", "/api/obszar", "/api/wyniki-ofert", "/api/historia", "/api/wspolne")


def blokady_modulu(modul):
    """Adresy API niedostępne dla konta ograniczonego do modułu (prefiksy)."""
    if not modul:
        return ()
    if modul in ("gmina", "wspolnota"):
        return tuple(z for z in ZABLOKOWANE_W_EDYCJI["zamawiajacy"] if z != "/api/alerty") + KONTA_I_ROLE  # alerty: terminy zamówień też
    b = SCIEZKA_ZAM + KONTA_I_ROLE
    if modul != "dotacje":
        b += ("/api/dotacje", "/api/zapytania")
    if modul != "nieruchomosci":
        b += ("/api/nier",)
    if modul in ("inwestor", "dotacje", "nieruchomosci"):
        b += SZUKANIE_PRZETARGOW
    return b


def projekt_modulu(m, modul):
    """Czy projekt należy do modułu (wykonawca, dostawca i kosztorysant mają wspólne projekty wykonawcy)."""
    if not modul:
        return True
    m = m or {}
    typ = m.get("typ") or "przetarg"
    st = m.get("strona") or strona_typu(typ)
    if modul in ("gmina", "wspolnota"):
        return st == "zamawiajacy" and projekt_wspolnoty(m) == (modul == "wspolnota")
    if modul == "inwestor":
        return typ == "dom"
    if modul in ("prawnik", "dotacje", "nieruchomosci"):
        return st == modul
    return st == "wykonawca"


def _odmowa_modulu():
    return jsonify({"blad": "To konto ma dostęp tylko do modułu „" + UWIERZ.MODULY_KONTA.get(modul_konta(), "") + "”."}), 403


@app.before_request
def blokada_modulu_konta():
    mk = modul_konta()
    if not mk:
        return None
    sc = request.path
    if any(sc == z or sc.startswith(z + "/") or sc.startswith(z + "?") for z in blokady_modulu(mk)):
        return _odmowa_modulu()
    j = request.get_json(silent=True) if request.method == "POST" and request.is_json else None
    j = j if isinstance(j, dict) else {}
    nowy = None  # projekt, który żądanie utworzy
    if sc == "/api/projekty" and request.method == "POST":
        typ = j.get("typ") if j.get("typ") in TYPY_PROJEKTOW else "przetarg"
        nowy = {"typ": typ, "strona": "prawnik" if typ == "ocena_ofert" and j.get("prawnik") is not None else strona_typu(typ),
                "prywatny": bool(j.get("prywatny"))}
    elif sc == "/api/zam/kreator" and request.method == "POST":
        nowy = {"typ": "zamowienie", "strona": "zamawiajacy", "prywatny": bool(j.get("prywatny"))}
    elif sc == "/api/zam/inwestycja" and request.method == "POST":
        nowy = {"typ": "zamowienie", "strona": "zamawiajacy", "prywatny": True}
    elif request.method == "POST" and sc.startswith("/api/projekty/") and sc.endswith("/kopiuj"):
        nowy = {"typ": j.get("typ"), "strona": strona_typu(j.get("typ")), "prywatny": False}
    if nowy is not None and not projekt_modulu(nowy, mk):
        return _odmowa_modulu()
    cz = sc.split("/")
    pid_ = cz[3] if len(cz) >= 4 and cz[1] == "api" and cz[2] == "projekty" else cz[2] if len(cz) >= 3 and cz[1] == "pobierz" else ""
    if pid_:
        m_ = czytaj(os.path.join(PROJ, os.path.basename(pid_), "projekt.json"), None)
        if m_ is not None and not projekt_modulu(m_, mk):
            return jsonify({"blad": "Projekt należy do innego modułu niż ten, do którego ma dostęp to konto."}), 404
    return None


if os.environ.get("SECRET_KEY"):
    app.secret_key = os.environ["SECRET_KEY"]
else:
    if not os.path.exists(F_SEKRET):
        with open(F_SEKRET, "w") as f:
            f.write(secrets.token_hex(32))
    app.secret_key = open(F_SEKRET).read().strip()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "1") == "1",
    PERMANENT_SESSION_LIFETIME=dt.timedelta(days=14),
    MAX_CONTENT_LENGTH=300 * 1024 * 1024,
)

from uwierzytelnianie import (  # noqa: E402,F401  logowanie i uprawnienia (rdzeń) – uwierzytelnianie.py
    OPISY_AKCJI, PROBY, TYLKO_WLASCICIEL, _ile_wpisow, _marka, hash_hasla, login_admina, ma_dostep, ma_ksiegowosc, ma_windykacje, moze,
    rola_def, rola_sesji, role_firmy, sprawdz_haslo, tylko_admin, ukryj_innych, uzytkownicy_lista, wlasciciel, wszystkie_konta,
    wymaga_logowania, zapisz_aktywnosc, modul_konta,
)
import uwierzytelnianie as UWIERZ  # noqa: E402  zmiany ustawień modułu – w module, nie w kopii nazw
import bezpieczenstwo as BEZP  # noqa: E402  SMTP, ceny dla ról bez Finansów, RODO w kadrach, hasła tymczasowe, CSRF logowania


def wygasanie_sesji():
    """H1-08: sesja wygasa po 8 godzinach bezczynności (najdłużej 14 dni od logowania) – przed wszystkimi innymi sprawdzeniami."""
    if UWIERZ.sesja_wygasla():
        session.clear()
        if request.path.startswith(("/api/", "/pobierz/")):
            return jsonify({"blad": "Sesja wygasła po 8 godzinach bezczynności – zaloguj się ponownie."}), 401
        if request.path == "/" or request.path == "/zmien-haslo":
            return redirect("/login?blad=sesja")  # pliki statyczne, ikony, manifest – bez przekierowania (sesja i tak wyczyszczona)
    return None


app.before_request_funcs.setdefault(None, []).insert(0, wygasanie_sesji)

@app.before_request
def blokada_modulow_wlasciciela():
    sc = request.path
    if any(sc == z_ or sc.startswith(z_ + "/") or sc.startswith(z_ + ".") or sc.startswith(z_ + "?") for z_ in TYLKO_WLASCICIEL) and not wlasciciel():
        return jsonify({"blad": "Ten moduł jest dostępny tylko dla właściciela programu."}), 403
    if (sc == "/api/wind" or sc.startswith("/api/wind/")) and not ma_windykacje():
        return jsonify({"blad": "Moduł Windykacja nie jest udostępniony temu kontu."}), 403
    return None


RE_PROJ = re.compile(r"^/(?:api/projekty|pobierz)/([0-9a-f]{12})(?:/|$)")


@app.before_request
def kontrola_dostepu():
    """Blokuje dostęp do cudzych projektów (wszystkie ścieżki /api/projekty/<id>/… i /pobierz/<id>/…)."""
    mm = RE_PROJ.match(request.path)
    if not mm or not session.get("zalogowany"):
        return None
    m = czytaj(os.path.join(PROJ, mm.group(1), "projekt.json"), None)
    if m is not None and not ma_dostep(m):
        return jsonify({"blad": "Nie masz dostępu do tego projektu."}), 404
    if m is not None and session.get("konto", "env") == "env" and not session.get("jako"):
        wl = m.get("wlasciciel") or login_admina()
        if wl != login_admina():
            g.konto_projektu = wl  # dokumenty projektu powstają z danymi firmy jego właściciela
    elif m is not None and UWIERZ.admin_firmy():  # administrator konta w projekcie osoby ze swojej firmy – dane firmy właściciela projektu
        wl = m.get("wlasciciel") or login_admina()
        if wl.lower() != str(session.get("login") or "").lower() and wl.lower() in UWIERZ.czlonkowie_firmy():
            g.konto_projektu = wl


@app.before_request
def blokada_podgladu():
    """Rola „Tylko podgląd” – tylko odczyt: każde żądanie zmieniające dane dostaje 403 (wyjątki: uwierzytelnianie.PODGLAD_DOZWOLONE)."""
    return UWIERZ.odmowa_podgladu()


@app.before_request
def odrzuc_programy():
    """Pliki wykonywalne (.exe, .bat, .msi…) nie są dokumentami – odrzucane we wszystkich formularzach wgrywania.
    Dokumenty projektu (/api/projekty/<id>/pliki) pomijają taki plik i zapisują pozostałe."""
    if request.method != "POST" or not session.get("zalogowany") or not (request.content_type or "").startswith("multipart/") \
            or request.endpoint == "projekty_wykonawcy.pliki_dodaj":
        return None
    zle = [f.filename for _, f in request.files.items(multi=True) if f and f.filename and MO.czy_wykonywalny(f.filename)]
    if zle:
        return jsonify({"blad": f"„{secure_filename_pl(zle[0])}” to plik programu (wykonywalny) – takich plików nie wgrywamy. "
                                "Wgraj dokument (PDF, Word, Excel, obraz) albo archiwum ZIP/7z."}), 400
    return None


@app.before_request
def json_slownik():
    """Adresy API przyjmują w treści żądania obiekt JSON – lista, liczba albo null to 400 z komunikatem, nie błąd 500."""
    if request.method in ("POST", "PUT", "PATCH") and request.path.startswith("/api/") and request.is_json and request.content_length:
        j = request.get_json(silent=True)
        if not isinstance(j, dict):
            return jsonify({"blad": "Nieprawidłowe dane żądania – oczekiwano obiektu JSON."}), 400
    return None


@app.after_request
def dziennik_aktywnosci(r):
    try:
        if r.status_code < 400 and session.get("zalogowany"):
            login, teraz = session.get("login"), time.time()
            if teraz - _WIDZIANI.get(login, 0) > 300:  # „ostatnio w programie” – każde użycie programu, nie tylko zmiany
                _WIDZIANI[login] = teraz
                with BLOKADA:
                    w = czytaj(F_WIDZIANI, {})
                    w[login] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
                    pisz(F_WIDZIANI, w)
            if request.path == "/api/ja" and teraz - _WEJSCIA.get((login, "program"), 0) > 7200:
                _WEJSCIA[(login, "program")] = teraz  # otwarcie programu (także przy zapamiętanym logowaniu)
                zapisz_aktywnosc(login, "Otwarcie programu", konto=konto_biezace())
            m_ = RE_PROJ.match(request.path)
            if m_ and request.method == "GET" and re.fullmatch(r"/api/projekty/[0-9a-f]{12}(/realizacja)?", request.path) \
                    and teraz - _WEJSCIA.get((login, m_.group(1)), 0) > 3600:
                _WEJSCIA[(login, m_.group(1))] = teraz
                nazwa = (czytaj(os.path.join(PROJ, m_.group(1), "projekt.json"), {}) or {}).get("nazwa", "")
                zapisz_aktywnosc(login, "Otwarto budowę" if request.path.endswith("/realizacja") else "Otwarto projekt",
                                 konto=konto_biezace(), projekt=nazwa)
        if r.status_code < 400 and session.get("zalogowany") and request.path.startswith(("/api/", "/pobierz/")):
            akcja = next((opis for wzor, met, opis in OPISY_AKCJI if met == request.method and re.search(wzor, request.path)), None)
            if akcja:
                m_ = RE_PROJ.match(request.path)
                nazwa = (czytaj(os.path.join(PROJ, m_.group(1), "projekt.json"), {}) or {}).get("nazwa", "") if m_ else ""
                szcz = os.path.basename(request.path) if request.method == "GET" else ""
                zapisz_aktywnosc(session.get("login"), akcja, szcz, konto=konto_biezace(), projekt=nazwa)
    except Exception:
        pass
    return r


_GZ_STATYCZNE = {}  # ścieżka pliku statycznego -> ((czas zmiany, rozmiar), skompresowane bajty) – kompresja raz na wersję pliku


def _gz_statyczny(r):
    """app.js (~900 kB) i styl.css kompresowane gzipem – na telefonie kilka razy mniej danych; skompresowana wersja trzymana w pamięci."""
    if r.status_code != 200 or not request.path.startswith("/static/") or not request.path.endswith((".js", ".css")) \
            or "gzip" not in (request.headers.get("Accept-Encoding") or "") or r.headers.get("Content-Encoding"):
        return r
    sciezka = os.path.join(app.static_folder, os.path.normpath(request.path[len("/static/"):]).lstrip(os.sep))
    if not sciezka.startswith(app.static_folder) or not os.path.isfile(sciezka):
        return r
    st = os.stat(sciezka)
    znak = (st.st_mtime_ns, st.st_size)
    w = _GZ_STATYCZNE.get(sciezka)
    if not w or w[0] != znak:
        import gzip
        with open(sciezka, "rb") as f:
            w = (znak, gzip.compress(f.read(), 6))
        _GZ_STATYCZNE[sciezka] = w
    r.direct_passthrough = False
    r.set_data(w[1])
    r.headers["Content-Encoding"] = "gzip"
    r.headers["Vary"] = "Accept-Encoding"
    return r  # ETag bez zmian – warianty rozróżnia Vary: Accept-Encoding (zachowane odpowiedzi 304)


@app.after_request
def kompresja(r):
    """Duże odpowiedzi JSON (lista przetargów, projekty) i strona główna kompresowane gzipem – kilka razy mniej danych na telefonie."""
    try:
        r = _gz_statyczny(r)
    except Exception:
        pass
    try:
        if (r.status_code == 200 and not r.direct_passthrough and r.mimetype in ("application/json", "text/html")
                and "gzip" in (request.headers.get("Accept-Encoding") or "") and not r.headers.get("Content-Encoding")):
            dane = r.get_data()
            if len(dane) > 20000:
                import gzip
                r.set_data(gzip.compress(dane, 5))
                r.headers["Content-Encoding"] = "gzip"
                r.headers["Vary"] = "Accept-Encoding"
    except Exception:
        pass
    return r


@app.after_request
def naglowki(r):
    if request.path.startswith("/static/") and request.args.get("v"):
        r.headers["Cache-Control"] = "public, max-age=31536000, immutable"  # plik z numerem wersji – może zostać w pamięci przeglądarki
    elif request.path.startswith("/static/") and request.path.endswith((".js", ".css", ".html")) or request.path == "/login":
        r.headers["Cache-Control"] = "no-cache"  # zawsze sprawdzaj, czy nie ma nowszej wersji (ważne na telefonach)
    if request.method == "GET" and request.path.startswith("/api/") and r.status_code == 200 and r.mimetype == "application/json":
        # ETag: gdy dane się nie zmieniły, przeglądarka dostaje krótką odpowiedź 304 zamiast całej listy
        r.set_etag(hashlib.md5(r.get_data()).hexdigest())
        r.headers["Cache-Control"] = "no-cache"
        r.make_conditional(request)
    r.headers["X-Frame-Options"] = "SAMEORIGIN"
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["Referrer-Policy"] = "same-origin"
    return r


@app.errorhandler(404)
def nie_znaleziono(e):
    if request.path.startswith(("/api/", "/pobierz/")):
        return jsonify({"blad": "Nie znaleziono – element mógł zostać usunięty lub przeniesiony do archiwum."}), 404
    return ('<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Nie znaleziono – Bidivia</title></head><body style="font-family:Arial,sans-serif;background:#071F49;color:#fff;'
            'display:grid;place-items:center;min-height:100vh;margin:0"><div style="background:#fff;color:#0f172a;padding:32px;border-radius:18px;'
            'max-width:420px;text-align:center"><h1 style="margin-top:0">Nie ma takiej strony</h1><p>Adres jest nieprawidłowy albo strona została '
            'przeniesiona.</p><p><a href="/login" style="font-weight:700">Przejdź do logowania</a> · <a href="/oferta" style="font-weight:700">'
            'Zobacz ofertę</a></p></div></body></html>'), 404


@app.get("/oferta")
def oferta_publiczna():
    """„Nasza oferta” – strona dostępna dla każdego z linkiem (bez logowania, bez dostępu do innych modułów)."""
    h = None
    for p in (os.path.join(app.static_folder, "oferta.html"), os.path.join(BASE, "oferta.html")):
        try:
            with open(p, encoding="utf-8") as f:
                h = f.read()
            break
        except OSError:
            continue
    if h is None:  # brak pliku ze zrzutami ekranów – strona oferty tworzona w programie
        import oferta as OF
        h = OF.strona("{{KONTAKT}}", "{{LINK}}")
    link = request.url_root.rstrip("/") + "/oferta"
    import html as _h
    h = h.replace("<body>", '<body><a href="/login" style="position:fixed;top:14px;right:16px;z-index:9;background:#071F49;color:#fff;'
                  'font-weight:700;padding:10px 18px;border-radius:10px;text-decoration:none;font-family:\'Plus Jakarta Sans\',Arial,sans-serif;'
                  'border:1px solid rgba(255,255,255,.35)">Zaloguj się</a>', 1)
    r = app.response_class(h.replace("{{KONTAKT}}", "").replace("{{LINK}}", _h.escape(link)), mimetype="text/html")
    r.headers["Cache-Control"] = "no-cache"
    return r


@app.get("/oferta/pdf/<dla>")
def oferta_pdf(dla):
    """Oferta w PDF do pobrania przez zainteresowanego (bez logowania)."""
    if dla not in ("wykonawca", "dostawca", "zamawiajacy", "inwestor", "rzeczoznawca", "dotacje", "wszystkie"):
        abort(404)
    nazwa = f"oferta_{dla}.pdf"
    for kat in (app.static_folder, BASE):
        if os.path.isfile(os.path.join(kat, nazwa)):
            return send_from_directory(kat, nazwa, as_attachment=True,
                                       download_name={"wykonawca": "Bidivia_oferta_dla_Wykonawcy.pdf", "dostawca": "Bidivia_oferta_dla_Dostawcy_Uslugodawcy.pdf",
                                                      "zamawiajacy": "Bidivia_oferta_dla_Zamawiajacych.pdf",
                                                      "inwestor": "Bidivia_oferta_dla_Inwestora_indywidualnego.pdf",
                                                      "rzeczoznawca": "Bidivia_oferta_dla_Rzeczoznawcy.pdf", "dotacje": "Bidivia_oferta_Dotacje_UE_KPO.pdf",
                                                      "wszystkie": "Bidivia_oferta_wszystkie_moduly.pdf"}[dla])
    abort(404)


LOGIN_ZAMAWIAJACY = (  # edycja „zamawiajacy”: podmiany tekstów w login.html – opis panelu .bd-hero i podtytuł (tytuł „Więcej niż przetargi” jak w pełnej)
    ('<p class="bd-hero__opis">Od przetargu, przez ofertę i umowę, po realizację. ',
     '<p class="bd-hero__opis">Od kreatora zamówienia, przez ocenę ofert, po rozliczenie umowy. '),
    ("Przetargi, oferty, kosztorysy, budowy i dotacje – Bidivia dopasuje pulpit do tego, czym się zajmujesz.",
     "Przygotowanie zamówień, ocena ofert i realizacja umów – dla gmin, urzędów i jednostek publicznych."),
)


def _token_logowania(h):
    """H1-08: token CSRF w formularzu logowania (sprawdzany przy POST /login razem z nagłówkami Origin/Referer)."""
    t = session.get("csrf_login") or secrets.token_urlsafe(24)
    session["csrf_login"] = t
    return h.replace('<form class="karta" method="post" action="/login">',
                     f'<form class="karta" method="post" action="/login"><input type="hidden" name="csrf" value="{t}">', 1)


@app.get("/login")
def login_strona():
    mk = _marka()
    if EDYCJA == "pelna":
        with open(os.path.join(app.static_folder, "login.html"), encoding="utf-8") as f:
            h = f.read()
        if mk["nazwa"]:
            h = h.replace("Bidivia", __import__("html").escape(mk["nazwa"]))
        if mk["kolor"]:
            h = h.replace("</head>", f"<style>:root{{--akcent:{mk['kolor']};--niebieski:{mk['kolor']}}}</style></head>", 1)
        r = Response(_token_logowania(h), mimetype="text/html")
        r.headers["Cache-Control"] = "no-store"
        return r
    with open(os.path.join(app.static_folder, "login.html"), encoding="utf-8") as f:
        h = f.read()
    h = _token_logowania(h)
    h = h.replace("<title>Bidivia – logowanie</title>", f"<title>{EDYCJE[EDYCJA]} – logowanie</title>")
    # panel marki (.bd-hero) – teksty dla zamawiającego publicznego (gmina, urząd, szkoła)
    for stary, nowy in LOGIN_ZAMAWIAJACY:
        h = h.replace(stary, nowy)
    h = h.replace("</head>", "<style>.oferta-link,.dla,.cechy{display:none!important}</style>\n</head>", 1)
    r = app.response_class(h, mimetype="text/html")
    r.headers["Cache-Control"] = "no-store"
    return r


def ip_klienta():
    """Adres klienta do limitu prób logowania. Nagłówek X-Forwarded-For podaje klient (dowolny pierwszy element), a każdy pośrednik
    dopisuje adres, od którego dostał połączenie, NA KOŃCU. Ufamy tylko tylu ostatnim wpisom, ilu jest pośredników platformy:
    ZAUFANE_PROXY (domyślnie 1 na Render – zmienna RENDER, 0 lokalnie: wtedy nagłówek jest ignorowany)."""
    try:
        n = int(os.environ.get("ZAUFANE_PROXY", "1" if os.environ.get("RENDER") else "0"))
    except ValueError:
        n = 0
    wpisy = [x.strip() for x in request.headers.get("X-Forwarded-For", "").split(",") if x.strip()]
    if n > 0 and len(wpisy) >= n:
        return wpisy[-n]
    return request.remote_addr or ""


LIMIT_PROB_IP, LIMIT_PROB_LOGIN = 5, 10  # nieudane próby w 15 minut: z jednego adresu / na jeden login (niezależnie od adresu)


@app.post("/login")
def login():
    # H1-08: CSRF logowania – formularz z obcej strony (Origin/Referer/Sec-Fetch-Site) albo niezgodny token z formularza
    tok = request.form.get("csrf")
    if BEZP.obce_pochodzenie(request.headers, request.host_url) or (tok is not None and not (
            session.get("csrf_login") and hmac.compare_digest(str(tok), str(session.get("csrf_login"))))):
        return redirect("/login?blad=csrf")
    ip = ip_klienta()
    klucz_l = "login:" + request.form.get("user", "").strip().lower()[:80]
    teraz = time.time()
    if len(PROBY) > 5000:  # porządek: bez nieograniczonego wzrostu przy próbach z wieloma loginami / adresami
        for k_ in [k_ for k_, v_ in list(PROBY.items()) if not v_ or teraz - v_[-1] >= 900]:
            PROBY.pop(k_, None)
    PROBY[ip] = [t for t in PROBY.get(ip, []) if teraz - t < 900]
    PROBY[klucz_l] = [t for t in PROBY.get(klucz_l, []) if teraz - t < 900]
    if len(PROBY[ip]) >= LIMIT_PROB_IP or len(PROBY[klucz_l]) >= LIMIT_PROB_LOGIN:
        return redirect("/login?blad=blokada")
    wzor_user = os.environ.get("APP_USER", "").strip()
    brak = [k for k, v in (("APP_USER", wzor_user), ("APP_PASSWORD", os.environ.get("APP_PASSWORD", "").strip()
                                                     or os.environ.get("APP_PASSWORD_HASH", "").strip())) if not v]
    if brak:
        return ("<meta charset='utf-8'><div style='font-family:Arial;max-width:640px;margin:60px auto;line-height:1.5'>"
                "<h2>Logowanie nie jest skonfigurowane</h2><p>Na serwerze brakuje zmiennych: <b>" + ", ".join(brak) +
                "</b>.</p><p>Render → usługa → <b>Environment</b> → <b>Edit</b> → <b>+ Add variable</b>: w kolumnie KEY "
                "wpisz dokładnie tę nazwę, w VALUE swój login / hasło → <b>Save, rebuild, and deploy</b>.</p>"
                "<p><a href='/login'>Wróć do logowania</a></p></div>"), 503
    user = request.form.get("user", "").strip()
    haslo = request.form.get("haslo", "")
    ok_user = hmac.compare_digest(user.lower().encode(), wzor_user.lower().encode())
    if ok_user and sprawdz_haslo(haslo):
        session.clear()
        session.update(zalogowany=True, konto="env", login=wzor_user, start=time.time(), ostatnio=time.time())
        session.permanent = True
        PROBY.pop(ip, None), PROBY.pop(klucz_l, None)
        zapisz_aktywnosc(wzor_user, "Logowanie", konto=wzor_user)
        return redirect("/")
    u = next((x for x in uzytkownicy_lista() if x["login"].lower() == user.lower()), None)
    # ten sam koszt sprawdzenia hasła dla loginu istniejącego i nieistniejącego – czas odpowiedzi nie zdradza, czy konto istnieje (enumeracja kont)
    try:
        _, it, sol, h = (u or {}).get("hash", "").split("$")
        int(it)
    except ValueError:
        u, it, sol, h = None, "390000", "0" * 32, ""
    zgodne = hmac.compare_digest(hash_hasla(haslo.strip(), sol, int(it)).split("$")[3], h)
    if u and zgodne and u.get("haslo_tymczasowe") and str(u.get("tymczasowe_do") or "") < dt.datetime.now().strftime("%Y-%m-%d %H:%M"):
        zgodne = False  # hasło tymczasowe ważne 72 godziny – potem administrator resetuje je ponownie
    if u:
        if zgodne:
            session.clear()
            session.update(zalogowany=True, konto="lista", login=u["login"], wersja=u.get("wersja", 1), start=time.time(), ostatnio=time.time())
            if u.get("haslo_tymczasowe"):
                session["zmien_haslo"] = True  # H1-07: hasło tymczasowe – najpierw zmiana hasła
                PROBY.pop(ip, None), PROBY.pop(klucz_l, None)
                zapisz_aktywnosc(u["login"], "Logowanie hasłem tymczasowym", konto=u["login"])
                return redirect("/zmien-haslo")
            session.permanent = True
            PROBY.pop(ip, None), PROBY.pop(klucz_l, None)
            zapisz_aktywnosc(u["login"], "Logowanie", konto=u["login"])
            return redirect("/")
    PROBY[ip].append(teraz)
    PROBY[klucz_l].append(teraz)
    time.sleep(1)
    return redirect("/login?blad=1")


@app.post("/logout")
def logout():
    if BEZP.obce_pochodzenie(request.headers, request.host_url):  # wylogowanie z obcej strony (CSRF) – ignorowane
        return redirect("/")
    session.clear()
    return redirect("/login")


def wersja_plikow():
    """Znacznik wersji (czas modyfikacji skryptu i stylów) – po aktualizacji telefony i komputery pobiorą nowe pliki,
    zamiast używać starych z pamięci przeglądarki."""
    try:
        return str(int(max(os.path.getmtime(os.path.join(app.static_folder, n)) for n in ("app.js", "styl.css", "ksiegowosc.js", "uklad.js") if os.path.exists(os.path.join(app.static_folder, n)))))
    except OSError:
        return "1"


@app.get("/")
@wymaga_logowania
def index():
    with open(os.path.join(app.static_folder, "index.html"), encoding="utf-8") as f:
        h = f.read()
    v = wersja_plikow()
    if EDYCJA != "pelna":
        h = h.replace("<title>Bidivia</title>", f"<title>{EDYCJE[EDYCJA]}</title>").replace(
            '<script src="/static/app.js"></script>', f'<script>window.EDYCJA = "{EDYCJA}";</script>\n<script src="/static/app.js"></script>')
    h = h.replace('href="/static/styl.css"', f'href="/static/styl.css?v={v}"').replace('src="/static/app.js"', f'src="/static/app.js?v={v}"').replace('src="/static/ksiegowosc.js"', f'src="/static/ksiegowosc.js?v={v}"').replace('src="/static/uklad.js"', f'src="/static/uklad.js?v={v}"')
    r = app.response_class(h, mimetype="text/html")
    r.headers["Cache-Control"] = "no-cache"
    return r




@app.get("/api/ja")
@wymaga_logowania
def ja():
    rd = rola_def()
    role = role_firmy()
    return jsonify({"login": session.get("login"), "rola": rola_sesji(), "rola_nazwa": rd.get("nazwa"), "uprawnienia": rd.get("uprawnienia"),
                    "ksiegowosc": ma_ksiegowosc(), "wlasciciel": wlasciciel(), "windykacja": ma_windykacje() and EDYCJA == "pelna", "marka": _marka(), "edycja": EDYCJA,
                    "prac_wszystkie": bool(session.get("prac_wszystkie")), "konto_biezace": konto_biezace(), "jako": session.get("jako") or "",
                    "admin_zakres": session.get("admin_zakres") or "wszystkie", "ostatni_tryb": cfg_surowy().get("ostatni_tryb", ""), "modul": modul_konta(),
                    "firma": cfg_surowy().get("firma_nazwa", ""), "logo": os.path.isfile(os.path.join(DIR_FIRMA, "logo.png")),
                    "konta": wszystkie_konta() if wlasciciel() else [k for k in wszystkie_konta() if k.lower() in UWIERZ.czlonkowie_firmy()]
                    if rola_sesji() == "admin" else [],
                    "admin_firmy": UWIERZ.admin_firmy(), "bez_cen": UWIERZ.bez_cen(rd), "zmien_haslo": bool(session.get("zmien_haslo")),
                    "zmiana_hasla": session.get("konto", "env") != "env",
                    "ai": rd.get("ai"), "raporty": rd.get("raporty", True), "tylko_odczyt": UWIERZ.tylko_odczyt(),
                    "role": {k: f"{r['nazwa']} – {r.get('opis', '')}" for k, r in role.items()}})


@app.get("/api/zuzycie-ai")
@wymaga_logowania
def zuzycie_ai():
    """Zużycie AI: administrator – wszystkie konta, użytkownik – własne konto (bieżący i poprzedni miesiąc)."""
    dzis = dt.date.today()
    poprz = (dzis.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
    kurs = float(cfg_surowy().get("kurs_usd", 3.65) or 3.65)
    konta_ = (wszystkie_konta() if wlasciciel() else [k for k in wszystkie_konta() if k.lower() in UWIERZ.czlonkowie_firmy()]) \
        if rola_sesji() == "admin" and not session.get("jako") else [konto_biezace()]  # administrator konta – tylko jego firma (H1-01)
    wyn, zad = [], {}
    for k in konta_:
        b, p = zuzycie_ai_konta(k), zuzycie_ai_konta(k, poprz)
        wyn.append({"konto": k, "biezacy": b, "poprzedni": p, "biezacy_zl": round(b.get("usd", 0) * kurs, 2), "poprzedni_zl": round(p.get("usd", 0) * kurs, 2)})
        for t, v in (b.get("zadania") or {}).items():
            zad[t] = round(zad.get(t, 0) + v * kurs, 2)
    return jsonify({"miesiac": dzis.strftime("%Y-%m"), "poprzedni_miesiac": poprz, "kurs_usd": kurs, "konta": wyn, "zadania": zad,
                    "pobranie": WSP.stan().get("czas") or WSP.stan().get("ostatnie_pobranie") or ""})








@app.get("/api/aktywnosc")
@wymaga_logowania
@tylko_admin
def aktywnosc():
    konto = request.args.get("konto", "")
    limit = min(int(request.args.get("limit", 300) or 300), 2000)
    wyn = []
    swoi = None if wlasciciel() else UWIERZ.czlonkowie_firmy()  # administrator konta – dziennik tylko swojej firmy (H1-01)
    try:
        with open(F_AKTYWNOSC, encoding="utf-8") as f:
            linie = f.readlines()[-30000:]
    except OSError:
        linie = []
    for linia in reversed(linie):
        try:
            w = json.loads(linia)
        except ValueError:
            continue
        if konto and w.get("konto") != konto and w.get("login") != konto:
            continue
        if swoi is not None and str(w.get("konto") or "").lower() not in swoi and str(w.get("login") or "").lower() not in swoi:
            continue
        wyn.append(w)
        if len(wyn) >= limit:
            break
    return jsonify(wyn)


KONTO_EDYCJA = [("stawka_rg", "Stawka roboczogodziny do wyceny [zł/h]", "float"), ("kp", "Koszty pośrednie Kp [%]", "float"),
                ("zysk", "Zysk Z [%]", "float"), ("gwarancja", "Domyślna gwarancja [miesiące]", "int"),
                ("auto_szukaj", "Szukaj przetargów automatycznie w dni robocze rano", "bool"),
                ("auto_ocena", "Automatycznie oceniaj nowe przetargi przez AI", "bool"),
                ("powiadomienia", "Wysyłaj codzienny raport e-mail", "bool"), ("powiadomienia_adresy", "Adresy e-mail do raportu (po przecinku)", "str"),
                ("powiadomienia_min_ocena", "Minimalna ocena przetargu w raporcie (1–10)", "int"),
                ("smtp_serwer", "Serwer poczty SMTP (np. smtp.gmail.com)", "str"), ("smtp_port", "Port SMTP (np. 465)", "int"),
                ("smtp_login", "Login poczty", "str"), ("smtp_haslo", "Hasło poczty (Gmail: hasło aplikacji)", "secret"),
                ("smtp_nadawca", "Adres nadawcy zamówień", "str"), ("kopia_do_mnie", "Wysyłaj mi kopię zamówień", "bool")]






















# ============================================================ aplikacja na telefon (PWA)

@app.get("/manifest.webmanifest")
def manifest():
    # id – stała tożsamość aplikacji (zmiana start_url nie tworzy drugiej aplikacji); bez blokady orientacji (tablet poziomo, tabele szerokie);
    # ikony osobno „any” i „maskable” (łączne „any maskable” odradzane – ikona przycinana także tam, gdzie nie trzeba); w edycji dla zamawiającego – jej nazwa i opis
    nazwa = "Bidivia" if EDYCJA == "pelna" else EDYCJE.get(EDYCJA, "Bidivia")
    dane = {"id": "/", "name": nazwa, "short_name": "Bidivia", "lang": "pl", "dir": "ltr", "start_url": "/", "scope": "/",
            "display": "standalone", "background_color": "#071F49", "theme_color": "#071F49",
            "description": ("Więcej niż przetargi – od przetargu, przez ofertę i umowę, po realizację. W jednym miejscu." if EDYCJA == "pelna" else
                            "Przygotowanie zamówień, ocena ofert i realizacja umów – dla gmin, urzędów i jednostek publicznych."),
            # „any” – ikona z zaokrąglonymi rogami (znak 62%); „maskable” – osobny plik: pełne tło, znak 52% w strefie bezpiecznej (koło 80%)
            "icons": [{"src": f"/ikona-{r}.png?v={WERSJA_IKON}", "sizes": f"{r}x{r}", "type": "image/png", "purpose": "any"} for r in (192, 512)]
            + [{"src": f"/ikona-maskable-{r}.png?v={WERSJA_IKON}", "sizes": f"{r}x{r}", "type": "image/png", "purpose": "maskable"} for r in (192, 512)]}
    return app.response_class(json.dumps(dane, ensure_ascii=False), mimetype="application/manifest+json")


WERSJA_IKON = "2027c"  # dopisek ?v= w odnośnikach do ikon (index.html, login.html, manifest) i nazwa plików w DATA – zmiana = przeglądarki pobierają ikony od nowa

# znak Bidivia – te same wielokąty co w SVG znaku (logo 2027, plik BIDIVIA-mark, viewBox 0 0 320 320; tak samo w index.html i login.html)
ZNAK_SVG_BIALY = [(0, 0), (0, 26.67), (240, 160), (0, 293.33), (0, 320), (240, 320), (320, 240), (240, 160), (320, 80), (240, 0)]
ZNAK_SVG_PROMIENIE = ([(0, 66.67), (0, 140), (240, 160)], [(0, 180), (0, 253.33), (240, 160)])
UDZIAL_ZNAKU_MASKABLE = 0.52  # ≤ 56%: narożniki znaku (0,52 × √2 / 2 = 0,37 szerokości od środka) mieszczą się w kole strefy bezpiecznej (promień 0,40)


def rysuj_ikone_bidivia(rozmiar, maskable=False):
    """Ikona Bidivia (identyfikacja 2027): granatowe tło #072556, biały znak „B” z promieniami #7A9ACE – rysowany z wielokątów SVG znaku.
    Zwykła („any”): kwadrat z zaokrąglonymi rogami, znak 62%. Maskable: pełne tło bez zaokrągleń (kształt nadaje system), znak 52% – strefa bezpieczna."""
    from PIL import Image, ImageDraw
    S_ = 4 * rozmiar  # rysowanie w 4× i pomniejszenie – gładkie krawędzie
    im = Image.new("RGBA", (S_, S_), (7, 37, 86, 255))  # granat logo #072556
    d = ImageDraw.Draw(im)
    udzial = UDZIAL_ZNAKU_MASKABLE if maskable else 0.62
    sk, x0 = S_ * udzial / 320, S_ * (1 - udzial) / 2  # wyśrodkowany
    f = lambda pts: [(x0 + x * sk, x0 + y * sk) for x, y in pts]
    d.polygon(f(ZNAK_SVG_BIALY), fill=(255, 255, 255, 255))
    for pr in ZNAK_SVG_PROMIENIE:
        d.polygon(f(pr), fill=(122, 154, 206, 255))  # #7A9ACE
    if not maskable:
        maska = Image.new("L", (S_, S_), 0)
        ImageDraw.Draw(maska).rounded_rectangle([0, 0, S_ - 1, S_ - 1], radius=int(S_ * 0.22), fill=255)
        im.putalpha(maska)
    return im.resize((rozmiar, rozmiar), Image.LANCZOS)


def _plik_ikony(rozmiar, maskable):
    p = os.path.join(DATA, f"ikona-bidivia{WERSJA_IKON}-{'maskable-' if maskable else ''}{rozmiar}.png")  # nowa nazwa – stare ikony z pamięci podręcznej nie wracają
    if not os.path.exists(p):
        im = rysuj_ikone_bidivia(rozmiar, maskable)
        if maskable or rozmiar in (180, 192, 512):  # na telefonie ikona musi mieć pełne tło
            tlo = __import__("PIL.Image", fromlist=["Image"]).new("RGB", im.size, (7, 37, 86))
            tlo.paste(im, (0, 0), im)
            im = tlo
        im.save(p, "PNG", optimize=True)
    return send_file(p, mimetype="image/png", max_age=86400)


@app.get("/ikona-<int:rozmiar>.png")
def ikona(rozmiar):
    if rozmiar not in (32, 180, 192, 512):
        abort(404)
    return _plik_ikony(rozmiar, False)


@app.get("/ikona-maskable-<int:rozmiar>.png")
def ikona_maskable(rozmiar):
    """Ikona do maskowania przez system (Android: koło, kropla, zaokrąglony kwadrat) – osobna od zwykłej, znak w strefie bezpiecznej."""
    if rozmiar not in (192, 512):
        abort(404)
    return _plik_ikony(rozmiar, True)


@app.get("/sw.js")
def service_worker():
    js = """// Bidivia – obsługa aplikacji na telefonie (zawsze pobiera świeże dane z serwera)
self.addEventListener("install", e => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || e.request.mode !== "navigate") return;
  e.respondWith(fetch(e.request).catch(() => new Response(
    '<meta charset="utf-8"><meta name="viewport" content="width=device-width"><body style="font-family:sans-serif;padding:30px;text-align:center">' +
    '<h2>Brak połączenia z internetem</h2><p>Bidivia wymaga internetu. Sprawdź połączenie i odśwież stronę.</p></body>',
    {headers: {"Content-Type": "text/html; charset=utf-8"}})));
});
"""
    r = app.response_class(js, mimetype="application/javascript")
    r.headers["Service-Worker-Allowed"] = "/"
    r.headers["Cache-Control"] = "no-cache"
    return r


WERSJA_PROGRAMU = "2027-03-12 decyzje-wlasciciela"  # widoczna pod adresem /zdrowie – pozwala sprawdzić, czy działa najnowsza wersja


@app.get("/zdrowie")
def zdrowie():
    # diagnostyka bez ujawniania wartości
    def _ma(plik, tekst):
        try:
            with open(os.path.join(app.static_folder, plik), encoding="utf-8") as f:
                return tekst in f.read()
        except OSError:
            return False
    spojne = _ma("index.html", 'id="p-karty"') and _ma("app.js", "function rysujKarty") and _ma("styl.css", ".wy-pasek")
    if not (session.get("zalogowany") and wlasciciel()):  # bez logowania (i dla kont innych niż właściciel) – bez pamięci, nazw zadań i ustawień serwera
        return {"ok": True, "wersja": WERSJA_PROGRAMU, "edycja": EDYCJA, "pliki_spojne": spojne}
    return {"ok": True, "wersja": WERSJA_PROGRAMU, "edycja": EDYCJA, "pliki_spojne": spojne, "pamiec_mb": pamiec_mb(), "pamiec_szczyt_mb": PAMIEC["szczyt_mb"],
            "pamiec_szczyt_przy": PAMIEC["szczyt_zadanie"], "pamiec_szczyt_czas": PAMIEC["szczyt_czas"], "oferta_html": os.path.isfile(os.path.join(app.static_folder, "oferta.html")),
            "APP_USER_ustawiony": bool(os.environ.get("APP_USER", "").strip()),
            "APP_PASSWORD_ustawione": bool(os.environ.get("APP_PASSWORD", "").strip()
                                           or os.environ.get("APP_PASSWORD_HASH", "").strip()),
            "ANTHROPIC_API_KEY_ustawiony": bool(os.environ.get("ANTHROPIC_API_KEY", "").strip()),
            "klucze_odrzucone": len(MO.ODRZUCONE_KLUCZE)}


# ============================================================ zadania w tle

from zadania import (  # noqa: E402,F401  zadania w tle (rdzeń) – zadania.py
    CZAS_DOMYSLNY, F_CZASY_ZADAN, PAMIEC, Przerwano, ZADANIA, ZadanieTrwa, _pilnuj_pamieci, _zapisz_czas_zadania, opis_bledu_zadania,
    pamiec_mb, postep_zadania, uruchom, zwolnij_pamiec,
)
import zadania as ZAD  # noqa: E402  stan zadań – w module

@app.errorhandler(ZadanieTrwa)
def _zadanie_trwa(e):
    """Zadanie już trwa – zwracamy też jego identyfikator, żeby okienko z postępem i przyciskiem Przerwij pokazało się ponownie."""
    z_ = e.zadanie
    return jsonify({"blad": str(e), "zadanie_trwa": {"id": z_.get("id"), "opis": z_.get("opis"), "status": "trwa"} if z_ else None}), 409


@app.get("/api/zadania/<zid>")
@wymaga_logowania
def zadanie(zid):
    z = ZADANIA.get(zid)
    if z and z.get("konto") != konto_biezace() and not wlasciciel():
        z = None  # zadania innych kont są niewidoczne (także dla administratora konta – H1-01)
    if not z:
        return jsonify({"blad": "Nie ma takiego zadania"}), 404
    return jsonify({**{k: v for k, v in z.items() if not k.startswith("_")}, "postep": postep_zadania(z)}), 200


@app.get("/api/zadania-aktywne")
@wymaga_logowania
def zadania_aktywne():
    """Trwające zadania konta – okienko zadania odnajduje po nich raport wznowiony po ponownym uruchomieniu serwera."""
    return jsonify([{"id": z_["id"], "opis": z_["opis"], "typ": z_["typ"]} for z_ in list(ZADANIA.values())
                    if z_["status"] == "trwa" and z_.get("konto") == konto_biezace()])
@app.post("/api/zadania/<zid>/przerwij")
@wymaga_logowania
def zadanie_przerwij(zid):
    z = ZADANIA.get(zid)
    if not z or (z.get("konto") != konto_biezace() and not wlasciciel()):
        return jsonify({"ok": True, "brak": True})  # zadanie już nie istnieje (np. po ponownym uruchomieniu serwera)
    if z["status"] == "trwa":
        z["przerwij"] = True
        z["log"].append(f"[{dt.datetime.now():%H:%M:%S}] Przerywam… (zadanie zakończy się na najbliższym etapie)")
    return jsonify({"ok": True})


@app.get("/api/zadania")
@wymaga_logowania
def zadania():
    return jsonify([{k: v for k, v in z.items() if k != "log"} for z in ZADANIA.values() if z.get("konto") == konto_biezace()][-20:])


def wymagany_klucz(c):
    if not c.get("api_key"):
        raise ValueError("Brak klucza API Claude – wpisz go w Ustawieniach lub ustaw ANTHROPIC_API_KEY na serwerze.")


# ============================================================ przetargi

def db_przetargi():
    return czytaj(F_DB, {})


WOJEWODZTWA = {  # nazwa: kod TERYT (tak oznacza je BZP)
    "dolnośląskie": "02", "kujawsko-pomorskie": "04", "lubelskie": "06", "lubuskie": "08", "łódzkie": "10",
    "małopolskie": "12", "mazowieckie": "14", "opolskie": "16", "podkarpackie": "18", "podlaskie": "20",
    "pomorskie": "22", "śląskie": "24", "świętokrzyskie": "26", "warmińsko-mazurskie": "28",
    "wielkopolskie": "30", "zachodniopomorskie": "32"}


def _woj_wzorzec(nazwa):
    n = core.norm(nazwa)
    return re.compile(r"(?<![a-z\-])" + re.escape(n) + r"(?:go|j|m)?(?![a-z])")


WOJ_RE = {w: _woj_wzorzec(w) for w in WOJEWODZTWA}


def wojewodztwo_ogloszenia(o):
    """Ustala województwo ogłoszenia (kod TERYT z BZP albo nazwa w danych). Zwraca nazwę lub ''."""
    if o.get("wojewodztwo") in WOJEWODZTWA:
        return o["wojewodztwo"]
    try:
        sur = json.loads(o.get("_surowe") or "{}")
    except ValueError:
        sur = {}
    kod = str(sur.get("organizationProvince") or "").upper().replace("PL", "").strip()
    for w, k in WOJEWODZTWA.items():
        if kod == k:
            return w
    tekst = core.norm(" ".join([o.get("miasto", ""), o.get("zamawiajacy", ""), o.get("_surowe", "")]))
    for w, rx in WOJ_RE.items():
        if rx.search(tekst):
            return w
    return ""


def filtruj_obszar(ogloszenia, c, znane, obszar):
    tryb = (obszar or {}).get("tryb", "promien")
    if tryb == "promien":
        if not c.get("miejscowosci"):
            return []
        dozw = set((obszar or {}).get("wojewodztwa_obszaru") or [])
        if dozw:  # odrzuć ogłoszenia z innych województw (miejscowości o tych samych nazwach)
            ogloszenia = [o for o in ogloszenia if (wojewodztwo_ogloszenia(o) or next(iter(dozw))) in dozw]
        return core.filtruj(ogloszenia, c, znane)
    wybrane = set((obszar or {}).get("wojewodztwa") or [])
    slowa = [core.norm(x) for x in c["slowa_kluczowe"]]
    cpv = [str(x).strip() for x in c["cpv"] if str(x).strip()]
    wyniki, widziane = [], set(znane)
    for o in ogloszenia:
        nr = o.get("numer")
        if not nr or nr in widziane:
            continue
        if not (any(p in core.norm(o["cpv"]) for p in cpv)
                or any(s_ in core.norm(o["przedmiot"] + " " + o["tresc"][:3000]) for s_ in slowa)):
            continue
        woj = wojewodztwo_ogloszenia(o)
        if tryb == "wojewodztwa" and woj not in wybrane and not (set(o.get("wojewodztwa") or []) & wybrane):  # TED: kilka miejsc realizacji
            continue
        widziane.add(nr)
        r = {k: v for k, v in o.items() if k != "_surowe"}
        r["tresc"] = r["tresc"][:12000]
        r["lokalizacja"] = ", ".join(x for x in (o.get("miasto", "")[:60], woj) if x) or "brak danych"
        r["wojewodztwo"] = woj
        r["status"] = "nowy"
        r["dodano"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        wyniki.append(r)
    return wyniki


def opis_obszaru(ob, c):
    t = (ob or {}).get("tryb", "promien")
    if t == "polska":
        return "cała Polska"
    if t == "wojewodztwa":
        return "woj. " + ", ".join(ob.get("wojewodztwa") or []) if ob.get("wojewodztwa") else "brak wybranych województw"
    if not c.get("centrum_nazwa") or not c.get("miejscowosci"):
        return "okolica miejscowości – nie wybrano miejscowości"
    return f"{c.get('centrum_nazwa')} + {c.get('promien_km'):g} km ({len(c.get('miejscowosci') or [])} miejscowości w zasięgu)"


@app.post("/api/bzp/test")
@wymaga_logowania
def bzp_test():
    return jsonify(uruchom("bzp", "Test połączenia z BZP", lambda log: BZ.test(cfg(), log)))








def migracja_dostepu():
    """Projekty użytkowników nie mogą być udostępnione innym użytkownikom – udostępnia właściciel programu (swoje projekty) albo
    administrator konta (swoje projekty, tylko osobom ze swojej firmy – H1-01)."""
    adm = login_admina().lower()
    uz = {str(u.get("login", "")).lower(): u for u in uzytkownicy_lista()}
    for pid in os.listdir(PROJ):
        p = os.path.join(PROJ, pid, "projekt.json")
        m = czytaj(p, None)
        wl = (m.get("wlasciciel") or adm).lower() if m else adm
        if m and m.get("dostep") and wl != adm:
            u = uz.get(wl)
            if u and u.get("rola") == "admin":
                swoi = UWIERZ.czlonkowie_firmy(u["login"])
                nowe = [x for x in m["dostep"] if str(x).lower() in swoi]
            else:
                nowe = []
            if nowe != m["dostep"]:
                m["dostep"] = nowe
                pisz(p, m)


def migracja_vat():
    """Usuwa zapisaną domyślną stawkę VAT z ustawień (VAT wybiera się teraz przy każdej ofercie)."""
    c = czytaj(F_CFG, {})
    if "vat" in c:
        c.pop("vat")
        pisz(F_CFG, c)


def migracja_projektow_zamawiajacego():
    """Kosztorys inwestorski, weryfikacja i dokumentacja to teraz jeden projekt zamówienia (typ „zamowienie”)."""
    for pid in os.listdir(PROJ):
        p = os.path.join(PROJ, pid, "projekt.json")
        m = czytaj(p, None)
        if m and m.get("typ") in ("inwestorski", "weryfikacja", "dokumentacja"):
            m["typ_pierwotny"], m["typ"], m["strona"] = m["typ"], "zamowienie", "zamawiajacy"
            pisz(p, m)


def migracja_regionu():
    """Jednorazowo usuwa dawny, domyślny rejon Świdnicy – region wybiera się teraz w panelu obszaru."""
    with BLOKADA:
        cc = czytaj(F_CFG, {})
        if cc.get("region_v2"):
            return
        for k in ("centrum_nazwa", "centrum_lat", "centrum_lon", "miejscowosci", "frazy_zawsze", "wykluczenia", "promien_km"):
            cc.pop(k, None)
        if (cc.get("obszar") or {}).get("tryb", "promien") == "promien":
            cc["obszar"] = {"tryb": "wojewodztwa", "wojewodztwa": ["dolnośląskie"]}
        cc["region_v2"] = True
        pisz(F_CFG, cc)


def migracja_modeli_ai():
    """Jednorazowo: modele dobrane do zadań (tańsze tam, gdzie wystarczą) i mniej wyszukiwań cen – jeśli administrator
    nie zmieniał ich wcześniej ręcznie (zostawione wartości domyślne starszej wersji)."""
    g_ = czytaj(F_CFG, {}) or {}
    if g_.get("modele_v2"):
        return
    if g_.get("model") in (None, "", "claude-sonnet-5"):
        g_["model"] = "claude-sonnet-5-5"
    if g_.get("model_oferty") in (None, "", "claude-opus-5-5"):
        g_["model_oferty"] = "claude-sonnet-5-5"
    g_.setdefault("model_lekki", "claude-haiku-5-5")
    g_.setdefault("model_dokladny", "claude-opus-5-5")
    g_.setdefault("pdf_jako_tekst", True)
    if g_.get("cache_ai") in (None, "", "5m") and not g_.get("cache_ai_wybrane"):
        g_["cache_ai"] = "1h"  # dokumenty projektu czytane z pamięci przez kolejne zadania w ciągu godziny
    g_["modele_v2"] = True
    pisz(F_CFG, g_)


def migracja_wyszukan_cen():
    """Jednorazowo: przywrócenie 10 wyszukiwań cen na jedno sprawdzenie, jeśli poprzednia wersja ustawiła 5 automatycznie."""
    g_ = czytaj(F_CFG, {}) or {}
    if g_.get("wyszukan_v3"):
        return
    if g_.get("modele_v2") and int(g_.get("ceny_internet_wyszukan", 10) or 10) == 5:
        g_["ceny_internet_wyszukan"] = 10
    g_["wyszukan_v3"] = True
    pisz(F_CFG, g_)


for _migracja in (migracja_regionu, migracja_projektow_zamawiajacego, migracja_vat, migracja_dostepu, migracja_modeli_ai, migracja_wyszukan_cen):
    try:  # błąd porządkowania starych danych nie może zablokować uruchomienia nowej wersji programu
        _migracja()
    except Exception as _e:
        print(f"Migracja {_migracja.__name__} pominięta: {_e}", flush=True)


def czysc_slowa(lista):
    """Słowa kluczowe 3–60 znaków, bez powtórzeń (bez względu na wielkość liter), do 200. Słowa spoza zakresu – pomijane
    (nie obcinane); listę pominiętych podaje slowa_odrzucone()."""
    wyn = []
    for x in (lista if isinstance(lista, list) else []):
        x = re.sub(r"\s+", " ", str(x)).strip()
        if 3 <= len(x) <= 60 and x.lower() not in [y.lower() for y in wyn]:
            wyn.append(x)
    return wyn[:200]


def slowa_odrzucone(lista):
    """Słowa kluczowe, których program nie użyje (krótsze niż 3 albo dłuższe niż 60 znaków) – do komunikatu."""
    sl = [re.sub(r"\s+", " ", str(x)).strip() for x in (lista if isinstance(lista, list) else [])]
    return [x for x in sl if x and not 3 <= len(x) <= 60]


def blad_slow(lista):
    """Komunikat o słowach spoza zakresu 3–60 znaków albo None."""
    odrz = slowa_odrzucone(lista)
    if not odrz:
        return None
    return "Słowo kluczowe musi mieć 3–60 znaków: " + ", ".join(f"„{x[:30]}{'…' if len(x) > 30 else ''}” ({len(x)} zn.)" for x in odrz[:5]) + "."


def pobierz_bk_pelne(c, log):
    """Ogłoszenia z Bazy Konkurencyjności: lista z ostatnich tygodni + szczegóły (miejsce realizacji) dla ogłoszeń
    pasujących do słów kluczowych, gdy lista nie podała miejsca."""
    lista = BKM.pobierz(c, log)
    slowa = [core.norm(x) for x in c.get("slowa_kluczowe") or []]
    cpv = [str(x).strip() for x in c.get("cpv") or [] if str(x).strip()]
    do_uzup = [o for o in lista if not o.get("miasto")
               and (any(s_ in core.norm(o["przedmiot"] + " " + o["tresc"][:3000]) for s_ in slowa) or any(p in o.get("cpv", "") for p in cpv)
                    or "Roboty budowlane" in o.get("kategoria", ""))]
    ile = 0
    for o in do_uzup[:120]:
        if BKM.uzupelnij_szczegoly(o):
            ile += 1
    if ile:
        log(f"Baza Konkurencyjności: pobrano szczegóły (miejsce realizacji) dla {ile} ogłoszeń.")
    return lista


# ============================================================ WSPÓLNA PAMIĘĆ OGŁOSZEŃ (pobieranie raz na dobę o 01:00)
WSP = W.Wspolne(os.path.join(DATA, "wspolne"))
NOC_BLOKADA = threading.Lock()


def _kompakt(o):
    """Ogłoszenie do wspólnej pamięci: bez surowych danych, z województwem (miejsce realizacji w BK, siedziba zamawiającego w BZP)."""
    woj = wojewodztwo_ogloszenia(o)
    r = {k: v for k, v in o.items() if k not in ("_surowe", "numer")}
    if o.get("zrodlo") != "TED":  # BZP: sekcja 6.4 (wadium) i 6.5 (zabezpieczenie) – z pełnej treści, zanim zostanie skrócona
        w_, kw_, _ = LD.wadium_z_tresci(o.get("tresc"))
        r["wadium_wymagane"], r["wadium"], r["znwu"] = w_, kw_, LD.znwu_z_tresci(o.get("tresc"))
        r["znwu_proc"] = LD.znwu_procent(o.get("tresc"))  # % zabezpieczenia, gdy ogłoszenie go podaje (art. 452 ust. 2–3 Pzp)
    r["tresc"] = str(r.get("tresc") or "")[:3000]
    r["wojewodztwo"] = woj
    return r


def _geokoduj(log, klucze, limit=900):
    """Współrzędne miejscowości (wspólne, raz na nazwę; serwis map – 1 zapytanie na sekundę)."""
    g = WSP.geo()
    brak = [k for k in dict.fromkeys(klucze) if k and k not in g]
    try:  # wbudowany wykaz miejscowości zna położenie od razu – do serwisu map idą tylko nazwy spoza wykazu
        import miejscowosci as _M
        brak = [k for k in brak if not _M.polozenie(*k.split("|", 1))]
    except Exception:
        pass
    brak = brak[:limit]
    if not brak:
        return 0
    log(f"Ustalam położenie {len(brak)} nowych miejscowości (raz – potem z pamięci)…")
    for i, k in enumerate(brak, 1):
        miasto, woj = k.split("|", 1)
        try:
            time.sleep(1.1)
            wyn = REG._szukaj_miejscowosci_mapy(miasto) or []
            traf = next((x for x in wyn if not woj or x.get("wojewodztwo") == woj), None) or (wyn[0] if wyn and not woj else None)
            g[k] = [float(traf["lat"]), float(traf["lon"])] if traf else None
        except Exception:
            continue
        if i % 100 == 0:
            WSP.zapisz_geo(g)
            log(f"Położenie miejscowości: {i}/{len(brak)}")
    WSP.zapisz_geo(g)
    return len(brak)


def praca_pobierz_ogloszenia(log, szybko=False):
    """Nocne pobranie (01:00): nowe ogłoszenia z BZP (od ostatniego pobrania), aktywne z Bazy Konkurencyjności z miejscem
    realizacji, położenie miejscowości; potem sprzątanie baz kont. Wyszukiwanie w ciągu dnia korzysta z tej pamięci.
    szybko=True (pierwsze wyszukiwanie przy pustej pamięci): tylko BZP i TED – reszta (rozstrzygnięcia, Baza Konkurencyjności,
    położenia) zostaje dla pobrania w tle, żeby użytkownik nie czekał kilkunastu minut na wynik."""
    if not NOC_BLOKADA.acquire(blocking=False):
        log("Pobieranie ogłoszeń już trwa – czekam na jego zakończenie…")
        with NOC_BLOKADA:
            return {"pominieto": True}
    try:
        c = cfg()
        st = WSP.stan()
        dzis = dt.date.today()
        od = dt.date.fromisoformat(st["bzp_do"]) - dt.timedelta(days=1) if st.get("bzp_do") else dzis - dt.timedelta(days=int(c.get("pamiec_dni_start", 21) or 21))
        log(f"BZP: pobieram ogłoszenia z całej Polski od {od:%d.%m.%Y}…")
        ile_bzp, klucze, start = 0, [], od
        while start <= dzis:
            koniec = min(start + dt.timedelta(days=2), dzis)
            try:
                surowe, _ = BZ._pobierz_okres(start, koniec, log, False)
            except Exception as e:
                log(f"BZP {start:%d.%m}–{koniec:%d.%m}: błąd ({e}) – spróbuję przy następnym pobraniu.")
                break
            dni_ = {}
            for n in surowe:
                o = BZ.normalizuj(n)
                if not o.get("numer"):
                    continue
                d = str(o.get("data_publikacji") or start.isoformat())[:10]
                k = _kompakt(o)
                dni_.setdefault(d, {})[o["numer"]] = k
                klucze.append(W.klucz_geo(k.get("miasto"), k.get("wojewodztwo")))
            for d, L in dni_.items():
                WSP.zapisz_dzien(d, L)
                ile_bzp += len(L)
            WSP.zapisz_stan(bzp_do=koniec.isoformat())
            start = koniec + dt.timedelta(days=1)
        log(f"BZP: zapisano {ile_bzp} ogłoszeń.")
        # TED – ogłoszenia powyżej progów UE (w tym zamówienia sektorowe, np. PKP), których nie ma w BZP
        try:
            st = WSP.stan()
            d_ = dt.date.fromisoformat(st["ted_do"]) - dt.timedelta(days=1) if st.get("ted_do") else dzis - dt.timedelta(days=int(c.get("pamiec_dni_start", 21) or 21))
            ile_ted = 0
            while d_ <= dzis:
                L_ = {o["numer"]: _kompakt(o) for o in TED.pobierz_dzien(d_.isoformat()) if o.get("numer")}
                if L_:
                    WSP.zapisz_dzien(d_.isoformat(), L_)
                    klucze += [W.klucz_geo(k.get("miasto"), k.get("wojewodztwo")) for k in L_.values()]
                ile_ted += len(L_)
                WSP.zapisz_stan(ted_do=d_.isoformat())
                d_ += dt.timedelta(days=1)
            log(f"TED: zapisano {ile_ted} ogłoszeń (powyżej progów UE, m.in. PKP).")
        except Exception as e:
            log(f"TED: błąd ({e}) – spróbuję przy następnym pobraniu.")
        if szybko:
            log("Ogłoszenia BZP i TED są w pamięci – szukam. Baza Konkurencyjności i rozstrzygnięcia dojdą przy pobraniu w tle.")
            return {"bzp": ile_bzp, "szybko": True}
        try:  # rozstrzygnięcia z całej Polski – dla Leadów (zwycięzcy) i raportów
            zbieraj_rozstrzygniecia(log)
        except Exception as e:
            log(f"Rozstrzygnięcia: błąd ({e}) – spróbuję przy następnym pobraniu.")
        # Baza Konkurencyjności – aktywne ogłoszenia z miejscem realizacji (szczegóły tylko dla nowych)
        try:
            lista = BKM.pobierz(c, log)
            stare = WSP.bk()
            teraz_ = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            granica_pub = (dzis - dt.timedelta(days=30)).isoformat()
            akt, do_uzup = {}, []
            for o in lista:
                if o.get("termin_ofert") and str(o["termin_ofert"])[:16] < teraz_:
                    continue
                if not o.get("termin_ofert") and str(o.get("data_publikacji") or "")[:10] < granica_pub:
                    continue
                prev = stare.get(o["numer"])
                if prev and prev.get("miasto") and not o.get("miasto"):
                    o = dict(o, **{k: prev[k] for k in ("miasto", "wojewodztwo", "termin_ofert", "termin_zrodlo") if prev.get(k)})
                if not o.get("miasto"):
                    do_uzup.append(o)
                akt[o["numer"]] = o
            for i, o in enumerate(do_uzup[:int(c.get("bk_szczegoly_noc", 400) or 400)], 1):
                try:
                    BKM.uzupelnij_szczegoly(o)
                except Exception:
                    pass
                if i % 50 == 0:
                    log(f"Baza Konkurencyjności: miejsce realizacji {i}/{min(len(do_uzup), 400)}")
            bk = {}
            for nr, o in akt.items():
                k = _kompakt(o)
                bk[nr] = k
                klucze.append(W.klucz_geo(k.get("miasto"), k.get("wojewodztwo")))
            WSP.zapisz_bk(bk)
            log(f"Baza Konkurencyjności: {len(bk)} aktywnych ogłoszeń.")
        except Exception as e:
            log(f"Baza Konkurencyjności: błąd ({e}).")
        if not klucze:  # pierwsze uruchomienie po aktualizacji – położenie także dla wcześniej zapisanych
            klucze = [W.klucz_geo(o.get("miasto"), o.get("wojewodztwo")) for o in WSP.wszystkie(10)]
        _geokoduj(log, klucze, limit=int(c.get("geokody_noc", 300) or 300))
        WSP.sprzataj(int(c.get("pamiec_dni", 60) or 60))
        WSP.zapisz_stan(ostatnie_pobranie=dzis.isoformat(), czas=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), bzp_ostatnio=ile_bzp)
        # sprzątanie baz kont (brakujące terminy) – w nocy, nie przy wyszukiwaniu użytkownika
        for login in wszystkie_konta():
            _KONTEKST.login = login
            try:
                popraw_brakujace_terminy(lambda *_: None, limit=25)
            except Exception:
                pass
        _KONTEKST.login = None
        log("Gotowe – wyszukiwanie w ciągu dnia korzysta z pobranych ogłoszeń.")
        return {"bzp": ile_bzp}
    finally:
        NOC_BLOKADA.release()


def zrodla_w_obszarze(c, log=None):
    """Obserwowane strony instytucji z bieżącego obszaru (okolica: powiaty w promieniu; województwa; cała Polska)."""
    zr = [z for z in dane_bip()["zrodla"] if z.get("aktywne", True)]
    ob = c.get("obszar") or {}
    t = ob.get("tryb", "promien")
    if t == "polska":
        return zr
    if t == "wojewodztwa":
        return [z for z in zr if z.get("wojewodztwo") in set(ob.get("wojewodztwa") or [])]
    kl = klucz_obszaru(c)
    pam = c.get("powiaty_obszaru_pam") or {}
    if kl not in pam:
        try:
            pam = {kl: {w: list(p) for w, p in powiaty_obszaru(c, log or (lambda *_: None)).items()}}
            zapisz_ustawienia({"powiaty_obszaru_pam": pam})
        except Exception:
            pam = {kl: {}}
    grupy = pam.get(kl) or {}
    np_ = lambda x: W.norm(re.sub(r"^powiat\s+", "", str(x or ""), flags=re.I))
    return [z for z in zr if z.get("wojewodztwo") in grupy and (not z.get("powiat") or not grupy[z["wojewodztwo"]]
                                                               or np_(z["powiat"]) in {np_(p) for p in grupy[z["wojewodztwo"]]})]


def praca_szukaj(log, slowa=None, tryb=""):
    """Wyszukiwanie konta: filtr wspólnej pamięci ogłoszeń (słowa / CPV, rodzaj zamówienia, obszar po odległości) + strony
    instytucji z obszaru. Bez pobierania BZP i BK z internetu – to robi nocne pobranie."""
    c = cfg()
    tryb = tryb or "wykonawca"
    if slowa:
        c["slowa_kluczowe"] = czysc_slowa(slowa)
    if not WSP.stan().get("ostatnie_pobranie") and not WSP.stan().get("bzp_do"):
        # pusta pamięć ogłoszeń: tylko BZP + TED (kilka minut), bez czekania na całe nocne pobranie
        if NOC_BLOKADA.locked():  # pobieranie w tle już trwa – czekam tylko na ogłoszenia BZP/TED, nie na całość
            log("Trwa pobieranie ogłoszeń do wspólnej pamięci – czekam na ogłoszenia BZP i TED (kilka minut)…")
            for _ in range(300):
                if WSP.stan().get("ted_do") or not NOC_BLOKADA.locked():
                    break
                time.sleep(2)
        else:
            log("Pierwsze pobranie ogłoszeń do wspólnej pamięci programu – kilka minut; kolejne wyszukiwania zajmą sekundy.")
            praca_pobierz_ogloszenia(log, szybko=True)
    st = WSP.stan()
    slowa_n = [W.norm(x) for x in c.get("slowa_kluczowe") or [] if W.norm(x)]
    cpv = [str(x).strip() for x in ((c.get("cpv_dostawy") or []) if tryb == "dostawca" else (c.get("cpv") or [])) if str(x).strip()]
    if not slowa_n and not cpv:
        log("Brak słów kluczowych i branży – wpisz, czego szukasz (krok 1).")
        return {"nowe": 0}
    wykl = [W.norm(x) for x in c.get("wykluczenia") or [] if W.norm(x)]
    ob = W.Obszar(c, WSP.geo())
    if ob.tryb == "promien" and (ob.lat is None or not c.get("miejscowosci")):
        log("Nie wybrano miejscowości dla trybu „okolica” – wybierz ją w kroku 2.")
    db = db_przetargi()
    ukryte = set(c.get("ukryte", []))
    teraz_s = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    teraz_ = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    gr_pub = (dt.date.today() - dt.timedelta(days=30)).isoformat()
    przejrzano = slow = w_ob = 0
    trafione, nowe = [], []
    klucz_dup = lambda x: (W.norm(x.get("przedmiot") or "")[:150] + "|" + W.norm(x.get("zamawiajacy") or "")[:20]) \
        if len(W.norm(x.get("przedmiot") or "")) >= 12 else "nr|" + str(x.get("numer"))
    znane_kl = {klucz_dup(dict(v, numer=k)): k for k, v in db.items()}
    for o in WSP.wszystkie(int(c.get("pamiec_dni_szukania", 45) or 45)):
        przejrzano += 1
        tm = str(o.get("termin_ofert") or "")
        if tm and tm[:16] < teraz_s:
            continue
        if not tm and str(o.get("data_publikacji") or "")[:10] < gr_pub:
            continue
        rz = rodzaj_przetargu(o)
        if (tryb == "dostawca" and rz == "roboty") or (tryb == "wykonawca" and rz in ("dostawy", "uslugi")):
            continue
        if not W.pasuje_slowa(o, slowa_n, cpv):
            continue
        if wykl and any(w_ in W.norm(str(o.get("przedmiot") or "")) for w_ in wykl):
            continue
        slow += 1
        ok, lok = ob.sprawdz(o)
        if not ok:
            continue
        w_ob += 1
        nr = o["numer"]
        if nr in ukryte:
            continue
        kl = klucz_dup(o)
        if nr not in db and kl in znane_kl:  # to samo postępowanie jest już na liście z innego źródła (BZP / TED) – bez dubla
            trafione.append(znane_kl[kl])
            continue
        znane_kl.setdefault(kl, nr)
        trafione.append(nr)
        if nr not in db:
            r = {k: v for k, v in o.items() if k != "numer"}
            r.update(lokalizacja=lok or r.get("miasto", ""), status="nowy", dodano=teraz_)
            nowe.append(dict(r, numer=nr))
    log(f"Przejrzano {przejrzano} ogłoszeń z całej Polski (pobrane {st.get('czas') or st.get('ostatnie_pobranie') or 'BZP do ' + str(st.get('bzp_do') or '–')}) → pasujące do słów i rodzaju: {slow} "
        f"→ w obszarze ({opis_obszaru(c.get('obszar'), c)}): {w_ob} → nowe: {len(nowe)}")
    # strony instytucji – tylko z obszaru; ich ogłoszenia też przechodzą przez słowa i rodzaj zamówienia
    if c.get("bip_w_wyszukiwaniu", True) and c.get("api_key") and dane_bip()["zrodla"]:
        try:
            zr = zrodla_w_obszarze(c, log)
            ids = {z["id"] for z in zr}
            if ids:
                bip_nowe = praca_bip_sprawdz(log, list(ids))
                def ok_bip(t):
                    rz_ = rodzaj_przetargu(t)
                    return not ((tryb == "dostawca" and rz_ == "roboty") or (tryb == "wykonawca" and rz_ in ("dostawy", "uslugi"))) \
                        and W.pasuje_slowa(t, slowa_n, cpv) and not (str(t.get("termin_ofert") or "") and str(t["termin_ofert"])[:16] < teraz_s) \
                        and not (wykl and any(w_ in W.norm(str(t.get("przedmiot") or "")) for w_ in wykl))
                for t in bip_nowe:
                    if ok_bip(t) and t["numer"] not in ukryte:
                        trafione.append(t["numer"])
                        if t["numer"] not in db:
                            nowe.append(t)
                for nr_, t in db.items():  # znane wcześniej ogłoszenia ze stron z obszaru
                    if t.get("bip_zrodlo") in ids and ok_bip(t) and nr_ not in ukryte:
                        trafione.append(nr_)
                log(f"Strony instytucji z obszaru: {len(ids)} – pasujące ogłoszenia: {len([t for t in bip_nowe if ok_bip(t)])} nowych.")
        except Exception as e:
            log(f"Strony instytucji: błąd ({e})")
    uzupelnione = 0
    for t in nowe[:40]:  # termin składania ofert ze strony ogłoszenia – tylko dla nowych z obszaru
        if not t.get("termin_ofert") and uzupelnij_termin(t):
            uzupelnione += 1
    with BLOKADA:
        db = db_przetargi()
        for t in nowe:
            t.setdefault("dodano", teraz_)
            db[t["numer"]] = {k: v for k, v in t.items() if k != "numer"}
        pisz(F_DB, db)
        stan_ = czytaj(F_POWIAD, {})
        stan_["ostatnie_szukanie"] = teraz_
        stan_.setdefault("ostatnie_wyszukiwanie", {})[tryb] = {"data": teraz_, "slowa": list(c.get("slowa_kluczowe") or [])[:60], "obszar": klucz_obszaru(c),
                                                                "numery": list(dict.fromkeys(trafione))}
        pisz(F_POWIAD, stan_)
    if c.get("auto_ocena") and c.get("api_key"):
        do_oceny = sito_do_oceny(log, trafione, c, slowa_n, cpv)
        if do_oceny:
            log(f"Ocena AI: {len(do_oceny)} przetargów bez oceny.")
            praca_ocen(log, do_oceny)
    return {"nowe": len(nowe), "wyniki": len(set(trafione))}


@app.get("/api/koszty-zadan")
@wymaga_logowania
@UWIERZ.tylko_wlasciciel
def koszty_zadan():
    mies = dt.date.today().strftime("%Y-%m")
    kurs = float(cfg_surowy().get("kurs_usd", 3.65) or 3.65)
    L = [dict(x, zl=round(x["usd"] * kurs, 2)) for x in (czytaj(F_KOSZTY_ZADAN, []) or []) if x.get("data", "").startswith(mies)]
    return jsonify({"najdrozsze": sorted(L, key=lambda x: -x["usd"])[:15], "limity": (czytaj(F_CFG, {}) or {}).get("limity_ai") or {}, "kurs": kurs})


@app.post("/api/koszty-zadan/limit")
@wymaga_logowania
@UWIERZ.tylko_wlasciciel
def koszty_limit():
    j = request.json or {}
    lim = dict(cfg_surowy().get("limity_ai") or {})
    try:
        v = float(str(j.get("limit") or 0).replace(",", ".").replace(" ", ""))
    except ValueError:
        return jsonify({"blad": "Podaj kwotę w zł."}), 400
    if v > 0:
        lim[str(j.get("konto") or "")] = v
    else:
        lim.pop(str(j.get("konto") or ""), None)
    with BLOKADA:
        glob = czytaj(F_CFG, {}) or {}
        glob["limity_ai"] = lim
        pisz(F_CFG, glob)
    return jsonify({"ok": True, "limity": lim})


@app.post("/api/wspolne/pobierz")
@wymaga_logowania
@UWIERZ.tylko_wlasciciel
def wspolne_pobierz():
    """Administrator: pobierz ogłoszenia teraz (zamiast czekać do 01:00)."""
    return jsonify(uruchom("pobieranie", "Pobieranie ogłoszeń (BZP, TED, Baza Konkurencyjności)", praca_pobierz_ogloszenia))


def praca_szukaj_stara(log, slowa=None, tryb=""):
    c = cfg()
    if slowa:  # słowa kluczowe podane przy tym wyszukiwaniu (domyślne z Ustawień + dodane przez użytkownika)
        c["slowa_kluczowe"] = czysc_slowa(slowa)
        log(f"Słowa kluczowe ({len(c['slowa_kluczowe'])}): {', '.join(c['slowa_kluczowe'][:25])}{' …' if len(c['slowa_kluczowe']) > 25 else ''}")
    db = db_przetargi()
    znane = set(db) | set(c.get("ukryte", []))
    wszystkie = []
    for nazwa, f in (("BZP", BZ.pobierz_bzp), ("Baza Konkurencyjności", pobierz_bk_pelne)):
        try:
            wszystkie += f(c, log)
        except Exception as e:
            log(f"{nazwa}: nie udało się pobrać danych ({e})")
    if (c.get("obszar") or {}).get("tryb", "promien") == "promien" and not c.get("miejscowosci"):
        log("Nie wybrano miejscowości dla trybu „okolica” – wybierz ją w panelu „Obszar wyszukiwania”.")
    nowe = filtruj_obszar(wszystkie, c, znane, c.get("obszar"))
    try:  # wszystkie ogłoszenia z obszaru znalezione w TYM wyszukiwaniu (także znane wcześniej) – lista pokaże tylko je
        trafione = [t["numer"] for t in filtruj_obszar(wszystkie, c, set(c.get("ukryte", [])), c.get("obszar"))]
    except Exception:
        trafione = [t["numer"] for t in nowe]
    log(f"Obszar: {opis_obszaru(c.get('obszar'), c)}. Pobrano {len(wszystkie)} ogłoszeń, nowych w obszarze: {len(nowe)}")
    if c.get("bip_w_wyszukiwaniu", True) and c.get("api_key") and dane_bip()["zrodla"]:
        try:
            nowe += [t for t in praca_bip_sprawdz(log) if t["numer"] not in znane]
        except Exception as e:
            log(f"BIP: błąd ({e})")
    uzupelnione = 0
    for t in nowe[:60]:  # termin składania ofert z formularza ogłoszenia (Baza Konkurencyjności: strona ogłoszenia)
        if not t.get("termin_ofert") and uzupelnij_termin(t):
            uzupelnione += 1
    if uzupelnione:
        log(f"Uzupełniono termin składania ofert w {uzupelnione} ogłoszeniach (ze strony ogłoszenia).")
    with BLOKADA:
        db = db_przetargi()
        teraz_ = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        for t in nowe:
            t.setdefault("dodano", teraz_)
            db[t["numer"]] = {k: v for k, v in t.items() if k != "numer"}
        pisz(F_DB, db)
        stan_ = czytaj(F_POWIAD, {})
        stan_["ostatnie_szukanie"] = teraz_
        if tryb:  # wyniki ostatniego wyszukiwania osobno dla każdego trybu (wykonawca, dostawca…)
            stan_.setdefault("ostatnie_wyszukiwanie", {})[tryb] = {"data": teraz_, "slowa": list(c.get("slowa_kluczowe") or [])[:60], "obszar": klucz_obszaru(c),
                                                                    "numery": list(dict.fromkeys(trafione + [t["numer"] for t in nowe]))}
        pisz(F_POWIAD, stan_)
    popraw_brakujace_terminy(log, limit=25)
    brak_miejsca = [(nr, t) for nr, t in db_przetargi().items() if t.get("bk_id") and not t.get("miasto")][:30]
    for nr, t in brak_miejsca:  # starsze ogłoszenia z BK bez miejsca realizacji – do filtrowania po obszarze
        if BKM.uzupelnij_szczegoly(t):
            with BLOKADA:
                db = db_przetargi()
                if nr in db:
                    db[nr].update({k: t[k] for k in ("miasto", "wojewodztwo", "termin_ofert", "termin_zrodlo", "tresc") if t.get(k)})
                    pisz(F_DB, db)
    if c.get("auto_ocena") and c.get("api_key"):
        # ocena AI wszystkich wyników tego wyszukiwania, które jeszcze nie mają oceny (nowe i wcześniej pominięte) – bez ręcznego „Oceń przez AI”
        db_ = db_przetargi()
        do_oceny = [n for n in dict.fromkeys([t["numer"] for t in nowe] + list(trafione)) if n in db_ and db_[n].get("ocena") in (None, "")]
        if do_oceny:
            praca_ocen(log, do_oceny[: int(c["max_do_oceny"])])
    return {"nowe": len(nowe)}


def sito_do_oceny(log, numery, c, slowa_n, cpv):
    """Wstępne sito bez AI przed automatyczną oceną: punkty dopasowania słów i branży (W.punkty_dopasowania).
    Do AI trafiają ogłoszenia z co najmniej „sito_prog” punktów, w kolejności od najlepiej pasujących (limit „max_do_oceny” bierze najlepsze).
    Odsiane zostają w wynikach z oznaczeniem „słabe dopasowanie – bez oceny AI” (można je ocenić ręcznie) – nic nie znika po cichu."""
    prog = int(c.get("sito_prog", 2) or 0)
    limit = int(c.get("max_do_oceny") or 30)
    db = db_przetargi()
    oc = []
    for n_ in dict.fromkeys(numery):
        t = db.get(n_)
        if t is None or t.get("ocena") not in (None, ""):
            continue
        pkt, opis = W.punkty_dopasowania(t, slowa_n, cpv)
        oc.append((pkt, str(t.get("data_publikacji") or t.get("dodano") or ""), n_, opis))
    oc.sort(key=lambda x: x[1], reverse=True)  # najnowsze…
    oc.sort(key=lambda x: -x[0])  # …w obrębie tej samej liczby punktów (sortowanie stabilne)
    przechodzi = [x for x in oc if x[0] >= prog] if prog > 0 else oc
    odsiane = [x for x in oc if prog > 0 and x[0] < prog]
    with BLOKADA:
        db = db_przetargi()
        for pkt, _, n_, opis in oc:
            if n_ in db:
                db[n_]["sito"] = {"pkt": pkt, "opis": opis, "slabe": prog > 0 and pkt < prog}
        pisz(F_DB, db)
    if odsiane:
        log(f"Wstępne sito (bez AI): {len(odsiane)} z {len(oc)} ogłoszeń bez oceny AI – słabe dopasowanie: słowo kluczowe tylko raz w treści ogłoszenia albo tylko jako fragment innego wyrazu lub stałej formułki, nie w tytule ani CPV "
            f"(zostają w wynikach z oznaczeniem „słabe dopasowanie”; można je ocenić ręcznie). Próg: {prog} pkt w Ustawieniach.")
    if len(przechodzi) > limit:
        log(f"Do oceny AI: {limit} najlepiej pasujących z {len(przechodzi)} (limit „max_do_oceny”); pozostałe – przy kolejnych wyszukiwaniach albo ręcznie.")
    return [x[2] for x in przechodzi[:limit]]


def profil_pusty(c=None):
    """H1-11: profil firmy (opis działalności) i profil dostawcy puste – AI nie ma według czego oceniać przetargów."""
    c = c or cfg()
    return not str(c.get("profil_firmy") or "").strip() and not str(c.get("profil_dostawcy") or "").strip()


KOMUNIKAT_PROFIL = ("Uzupełnij profil firmy (Profil firmy → „Opis firmy”: zakres robót, doświadczenie, obszar działania) – "
                    "AI ocenia przetargi według tego opisu.")


def praca_ocen(log, numery):
    c = cfg()
    wymagany_klucz(c)
    if profil_pusty(c):  # bez opisu firmy ocena nie ma sensu (dawniej – przykładowy opis „Firma budowlana ze Świdnicy…”)
        log(KOMUNIKAT_PROFIL + " Ocena AI pominięta.")
        return
    dec = tekst_decyzji()
    c_ucz = dict(c, profil_firmy=(c.get("profil_firmy", "") + "\n" + dec).strip()) if dec else c
    profil_dost = (c.get("profil_dostawcy") or "").strip()

    def profil_dla(t):  # przetargi na dostawy i usługi oceniane według profilu dostawcy / usługodawcy (jeśli jest wypełniony)
        return profil_dost if profil_dost and rodzaj_przetargu(t) in ("dostawy", "uslugi") else c_ucz.get("profil_firmy", "")
    if dec:
        log("Ocena uwzględnia wcześniejsze decyzje firmy (startujemy / odpuszczamy).")
    ok = 0
    pelna_dla = list(numery)
    if len(numery) > 3 and c.get("ocena_paczkami", True):
        # 1) szybka ocena wszystkich paczkami po 12 (instrukcja i profil raz na paczkę, z pamięcią podręczną promptu)
        prog = int(c.get("prog_pelnej_oceny", 6) or 6)
        pelna_dla, bez_wyniku = [], []
        db0 = db_przetargi()
        grupy_ = {}  # paczki z jednym profilem: budowlane według profilu firmy, dostawy i usługi według profilu dostawcy
        for n_ in numery:
            if db0.get(n_):
                grupy_.setdefault(profil_dla(db0[n_]), []).append(n_)
        paczki_ = [L_[i_:i_ + 12] for L_ in grupy_.values() for i_ in range(0, len(L_), 12)]
        zrobione_ = 0
        for nr_paczki in paczki_:
            paczka = [dict(db_przetargi().get(nr) or {}, numer=nr) for nr in nr_paczki if db_przetargi().get(nr)]
            zrobione_ += len(nr_paczki)
            if not paczka:
                continue
            log(f"Ocena {zrobione_}/{len(numery)} (szybka ocena paczkami)")
            try:
                wyn, uz = AN.ocena_paczki(paczka, c, profil_dla(paczka[0]), bool(MO.ustawienie_cache(c)))
                if MO.opis_uzycia(uz):
                    log(MO.opis_uzycia(uz))
            except Exception as e:
                log(f"Szybka ocena paczki nie powiodła się ({e}) – oceniam te przetargi pojedynczo.")
                wyn = {}
            for t in paczka:
                w = wyn.get(t["numer"])
                if not w:
                    bez_wyniku.append(t["numer"])
                    continue
                with BLOKADA:
                    db = db_przetargi()
                    if t["numer"] in db:
                        if w.get("zakres") and not db[t["numer"]].get("rodzaj"):
                            db[t["numer"]]["rodzaj"] = w["zakres"]  # rodzaj zamówienia ustalony przez AI (gdy ogłoszenie go nie podało)
                        if not db[t["numer"]].get("analiza_zrodlo", "").startswith(("dokumenty", "ogłoszenie")):
                            db[t["numer"]].update({k: v for k, v in w.items() if k not in ("termin_iso", "zakres") and v not in ("", None)},
                                                  analiza_zrodlo="ocena szybka", analiza_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
                        else:
                            db[t["numer"]].update(ocena=w["ocena"], rekomendacja=w["rekomendacja"])
                        pisz(F_DB, db)
                zapisz_termin_z_analizy(t["numer"], w)
                ok += 1
                if w["ocena"] >= prog:
                    pelna_dla.append(t["numer"])
        pelna_dla += bez_wyniku
        if pelna_dla:
            log(f"Szczegółowa analiza z ogłoszenia dla {len(pelna_dla)} przetargów z oceną co najmniej {prog} (pozostałe mają szybką ocenę).")
    for i, nr in enumerate(pelna_dla, 1):
        t = db_przetargi().get(nr)
        if not t:
            continue
        log(f"Ocena szczegółowa {i}/{len(pelna_dla)}: {t.get('przedmiot', '')[:80]}")
        if not t.get("termin_ofert") and uzupelnij_termin(t):
            with BLOKADA:
                db = db_przetargi()
                if nr in db:
                    db[nr].update({k: t[k] for k in ("termin_ofert", "termin_zrodlo", "tresc") if t.get(k)})
                    pisz(F_DB, db)
        odcz = (WSP.czytaj("odczyty.json", {}) or {}).get(nr)
        if odcz and odcz.get("data", "") >= (dt.date.today() - dt.timedelta(days=30)).isoformat() and t.get("ocena") not in (None, ""):
            # ogłoszenie odczytane już dla innego konta – dane ogłoszenia ze wspólnej pamięci, ocena dopasowania z oceny paczkami
            with BLOKADA:
                db = db_przetargi()
                if nr in db and not db[nr].get("analiza_zrodlo", "").startswith("dokumenty"):
                    db[nr].update({k: v for k, v in odcz.items() if k != "data" and v not in ("", None)},
                                  analiza_zrodlo="ogłoszenie", analiza_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
                    pisz(F_DB, db)
            log(f"Dane ogłoszenia {nr} – ze wspólnej pamięci programu (bez ponownego odczytu AI).")
            continue
        try:
            w = AN.wstepna(dict(t, numer=nr), c, profil_dla(t))
        except Exception as e:
            log(f"Nie udało się ocenić {nr}: {e}")
            continue
        try:  # część niezależna od profilu firmy – wspólna dla wszystkich kont
            wsp_pola = {k: w[k] for _, pola in AN.GRUPY[:4] for k, _ in pola if w.get(k)}
            if wsp_pola:
                with W.BLOKADA:
                    od_ = WSP.czytaj("odczyty.json", {})
                    od_[nr] = dict(wsp_pola, data=dt.date.today().isoformat())
                    if len(od_) > 6000:
                        od_ = dict(sorted(od_.items(), key=lambda x: x[1].get("data", ""))[-5000:])
                    WSP.pisz("odczyty.json", od_)
        except Exception:
            pass
        with BLOKADA:
            db = db_przetargi()
            if nr in db:
                if db[nr].get("analiza_zrodlo", "").startswith("dokumenty"):  # nie nadpisuj pełnej analizy
                    w = {k: w[k] for k in ("ocena", "rekomendacja")}
                else:
                    w.update(analiza_zrodlo="ogłoszenie", analiza_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
                db[nr].update({k: v for k, v in w.items() if k != "termin_iso"})
                pisz(F_DB, db)
        zapisz_termin_z_analizy(nr, w)
        ok += 0 if nr in numery and len(numery) > 3 and c.get("ocena_paczkami", True) else 1
    return {"ocenione": ok}


def sprawdzacz_obszaru(c=None):
    """Zwraca funkcję t -> True/False: czy zapisany przetarg leży w obecnie wybranym obszarze wyszukiwania
    (okolica miejscowości z promieniem, wybrane województwa albo cała Polska)."""
    c = c or cfg()
    ob = c.get("obszar") or {}
    tryb = ob.get("tryb", "promien")
    if tryb == "polska":
        return lambda t: True

    def woj_przetargu(t):
        if t.get("wojewodztwo"):
            return t["wojewodztwo"]
        tekst = core.norm(" ".join(str(t.get(k, "")) for k in ("miasto", "zamawiajacy", "lokalizacja", "lokalizacja_robot")) + " "
                          + str(t.get("tresc", ""))[:3000])
        return next((w for w, rx in WOJ_RE.items() if rx.search(tekst)), "")

    if tryb == "wojewodztwa":
        wybrane = set(ob.get("wojewodztwa") or [])
        return lambda t: woj_przetargu(t) in wybrane or bool(set(t.get("wojewodztwa") or []) & wybrane)
    if not c.get("miejscowosci") or c.get("centrum_lat") is None:
        return lambda t: False
    ob_ = W.Obszar(c, WSP.geo())  # ten sam filtr po odległości co wyszukiwanie

    def w_obszarze(t):
        if not t.get("wojewodztwo"):
            t = dict(t, wojewodztwo=woj_przetargu(t))
        return ob_.sprawdz(t)[0]
    return w_obszarze


def wizyta_konta():
    """Wizyty konta: przy pierwszym wejściu danego dnia poprzednia wizyta staje się granicą „nowych” przetargów."""
    teraz = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with BLOKADA:
        w = czytaj(F_WIZYTY, {})
        if (w.get("biezaca") or "")[:10] != teraz[:10]:  # pierwsze wejście danego dnia
            w = {"poprzednia": w.get("ostatnio") or w.get("biezaca") or (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                 "biezaca": teraz, "ostatnio": teraz, "widziane": []}
            pisz(F_WIZYTY, w)
        elif w.get("ostatnio", "")[:16] != teraz:
            w["ostatnio"] = teraz  # ostatnia aktywność – granica „nowych” przy następnej wizycie
            pisz(F_WIZYTY, w)
    return w


def czy_nowy(t, nr, w):
    return (t.get("dodano") or "") > (w.get("poprzednia") or "") and nr not in set(w.get("widziane") or [])






def rodzaj_przetargu(t):
    """roboty / dostawy / uslugi / "" (nieustalony) – z rodzaju zamówienia w ogłoszeniu (BZP), kategorii BK, CPV albo przedmiotu."""
    return HZ.rodzaj_zamowienia(t.get("rodzaj") or t.get("typ_zamowienia") or t.get("orderType") or "", t.get("cpv", ""),
                                t.get("przedmiot", ""), t.get("kategoria", ""))


def pasuje_do_trybu(t, tryb):
    """Wykonawca: roboty (i nieustalone); dostawca: dostawy, usługi (i nieustalone)."""
    r = t.get("rodzaj_zam") if "rodzaj_zam" in t else rodzaj_przetargu(t)
    if tryb == "dostawca":
        return r != "roboty"
    if tryb == "wykonawca":
        return r not in ("dostawy", "uslugi")
    return True


def migracja_rodzaju():
    """Rodzaj zamówienia z BZP dla przetargów zapisanych wcześniej – odczyt z przechowywanej treści ogłoszenia."""
    for login in wszystkie_konta():
        p = F_DB.dla(login)
        db = czytaj(p, {}) or {}
        zm = 0
        for t in db.values():
            if t.get("rodzaj") or not t.get("_surowe"):
                continue
            m_ = re.search(r'"(?:orderType|orderKind|typeOfOrder)"\s*:\s*"([^"]+)"', str(t["_surowe"]))
            if m_:
                t["rodzaj"] = m_.group(1)
                zm += 1
        if zm:
            pisz(p, db)
            print(f"Rodzaj zamówienia uzupełniony: {login} – {zm} przetargów", flush=True)


def typ_zamawiajacego(t):
    """jst / szpital / uczelnia / spolka / inny – do filtra listy przetargów."""
    if t.get("typ_zamawiajacego") in ("szpital", "uczelnia", "spolka"):
        return t["typ_zamawiajacego"]
    if t.get("typ_zamawiajacego") in ("gmina", "powiat", "wojewodztwo"):
        return "jst"
    n = HZ._norm(t.get("zamawiajacy", ""))
    if re.search(r"wspolnota mieszkaniow|spoldzielni", n):
        return "wspolnota"
    if re.search(r"szpital|sp zoz|zoz\b|opieki zdrowotnej|centrum medyczn|klinik|onkologi|pogotowi|ratownictwa medycznego|krwiodawstw|sanatori|uzdrowisk", n):
        return "szpital"
    if re.search(r"uniwersytet|politechnik|akademi|uczelni|szkola wyzsza|instytut|pan\b", n):
        return "uczelnia"
    if re.search(r"kghm|orlen|pge|tauron|enea|energa|pkp|poczta polska|jsw|azoty|pgz|gaz system|pse\b|wodociag|mpk|komunikacj|cieplown|energetyk|"
                 r"\bs a\b|sp z o o|spolka", n):
        return "spolka"
    if re.search(r"^(gmina|miasto|powiat|wojewodztwo|urzad|starostwo|zarzad drog|miejski|gminny|powiatowy)", n):
        return "jst"
    return "inny"


SLOWA_DOSTAWY = []  # dostawca wybiera branżę (gotowe zestawy z kodami CPV) – ogólne „dostaw / usług / zakup” pasowały do wszystkiego
OGOLNE_SLOWA_DOSTAWY = {"dostaw", "dostawa", "zakup", "usług", "usluga", "materiał", "projekt", "dokumentacj", "sprzęt", "druk", "nadzór",
                        "szkoleni", "przegląd", "serwis", "olej"}




def szczegoly_bk(bk_id):
    """Pełne dane ogłoszenia z Bazy Konkurencyjności (to, co widać na stronie ogłoszenia)."""
    for url in (f"{MO.BK}/api/announcements/{bk_id}", f"{MO.BK}/api/announcements/{bk_id}/details"):
        try:
            return json.loads(MO._get(url, timeout=30).read().decode("utf-8"))
        except Exception:
            continue
    return None


def uzupelnij_termin(t):
    """Ustala termin składania ofert, gdy brak go w danych z wyszukiwarki: pola formularza ogłoszenia,
    strona ogłoszenia w Bazie Konkurencyjności, treść ogłoszenia (np. „Termin składania ofert: 20.10.2026 godz. 10:00”).
    Modyfikuje słownik t; zwraca True, gdy termin znaleziono."""
    kandydat, zrodlo = None, ""
    if t.get("_surowe"):
        try:
            kandydat, zrodlo = AN.termin_z_danych(json.loads(t["_surowe"])), "formularz ogłoszenia"
        except ValueError:
            pass
    if not kandydat and t.get("bk_id"):
        d = szczegoly_bk(t["bk_id"])
        if d:
            kandydat, zrodlo = AN.termin_z_danych(d), "strona ogłoszenia (Baza Konkurencyjności)"
            if not kandydat:
                kandydat = AN.termin_z_tekstu(core.html_na_tekst(json.dumps(d, ensure_ascii=False)))
            if not t.get("tresc"):
                opis = next((d.get(k) for k in ("description", "content", "orderDescription") if d.get(k)), "")
                if opis:
                    t["tresc"] = core.html_na_tekst(opis)[:15000]
    if not kandydat:
        kandydat, zrodlo = AN.termin_z_tekstu(t.get("tresc")), "treść ogłoszenia"
    if kandydat:
        t["termin_ofert"], t["termin_zrodlo"] = kandydat, zrodlo
        return True
    return False


def popraw_brakujace_terminy(log, limit=25):
    """Uzupełnia termin w zapisanych wcześniej ogłoszeniach, które go nie mają."""
    brak = [(nr, t) for nr, t in db_przetargi().items() if not t.get("termin_ofert") and t.get("status") != "odpuszczamy"][:limit]
    ile = 0
    for nr, t in brak:
        if uzupelnij_termin(t):
            with BLOKADA:
                db = db_przetargi()
                if nr in db:
                    db[nr].update({k: t[k] for k in ("termin_ofert", "termin_zrodlo", "tresc") if t.get(k)})
                    pisz(F_DB, db)
            ile += 1
    if ile and log:
        log(f"Uzupełniono brakujący termin składania ofert w {ile} wcześniej zapisanych ogłoszeniach.")
    return ile


def zapisz_termin_z_analizy(nr, w, pliki_tekst=""):
    """Po analizie: jeśli ogłoszenie nie ma terminu – bierze go z dokumentów (pierwsze strony) albo z odpowiedzi AI."""
    with BLOKADA:
        db = db_przetargi()
        t = db.get(nr)
        if not t or t.get("termin_ofert"):
            return
        kand = AN.termin_z_tekstu(pliki_tekst) if pliki_tekst else None
        zr = "dokumenty zamówienia"
        if not kand and w.get("termin_iso"):
            kand, zr = w["termin_iso"], "analiza AI"
        if kand:
            t["termin_ofert"], t["termin_zrodlo"] = kand, zr
            pisz(F_DB, db)




def folder_przetargu(nr):
    return os.path.join(DATA, "przetargi_dok", hashlib.sha1(nr.encode()).hexdigest()[:14])


def praca_analiza_pelna(log, nr):
    """Pełna analiza przetargu z dokumentów zamówienia (pobieranych automatycznie) – bez zakładania projektu."""
    c = cfg()
    wymagany_klucz(c)
    t = db_przetargi().get(nr)
    if not t:
        raise ValueError("Nie ma takiego przetargu.")
    folder = folder_przetargu(nr)
    os.makedirs(folder, exist_ok=True)
    # dokumenty już wgrane do projektu tej oferty (np. SWZ pobrana ręcznie z platformy) – bez ponownego pobierania
    k_ = konto_biezace()
    z_projektu = []
    for pid_ in os.listdir(PROJ):
        m_ = czytaj(os.path.join(PROJ, pid_, "projekt.json"), None)
        if m_ and m_.get("przetarg_numer") == nr and not m_.get("archiwum") and (m_.get("wlasciciel") or login_admina()) == k_:
            z_projektu = [os.path.join(PROJ, pid_, "dokumenty", p_["sciezka"]) for p_ in lista_plikow(pid_) if p_.get("uwzglednij", True)]
            if z_projektu:
                log(f"Dokumenty z projektu oferty „{m_.get('nazwa')}” ({len(z_projektu)}) – bez pobierania z platformy.")
                for f_ in z_projektu:
                    if os.path.isfile(f_):
                        shutil.copy2(f_, os.path.join(folder, os.path.basename(f_)))
                break
    if not z_projektu:
        log("Pobieram dokumenty zamówienia…")
    try:
        if z_projektu:
            pobrane = []
        elif t.get("bk_id"):
            pobrane = MO.pobierz_zalaczniki_bk(t["bk_id"], folder, log)
        elif t.get("zrodlo") == "BIP" and t.get("link"):
            pobrane = BZ.pobierz_z_platformy([t["link"]], t.get("przedmiot", ""), folder, log)
        else:
            pobrane = BZ.pobierz_dokumenty(dict(t, numer=nr), folder, log)["pliki"]
    except Exception as e:
        log(f"Pobieranie nie powiodło się: {e}")
        pobrane = []
    for p in [p for p in pobrane if MO.czy_archiwum(p)]:
        try:
            MO.rozpakuj_zip(p, os.path.splitext(p)[0])
            os.remove(p)
        except Exception as e:
            log(f"Nie udało się rozpakować {os.path.basename(p)}: {e}")
    pliki = popraw_nazwy_folderu(folder, log)
    if not pliki:
        raise ValueError("Nie udało się pobrać dokumentów automatycznie (platforma może wymagać logowania). "
                         "Otwórz ogłoszenie, pobierz SWZ ręcznie i przygotuj ofertę w projekcie – albo zostań przy analizie z ogłoszenia.")
    if not t.get("termin_ofert") and uzupelnij_termin(t):
        zapisz_termin_z_analizy(nr, {"termin_iso": t["termin_ofert"]})
    teksty = []
    for p in sorted(pliki, key=lambda p: next((i for i, x in enumerate(AN.PRIORYTET) if x in os.path.basename(p).lower()), 99))[:8]:
        rozsz = os.path.splitext(p)[1].lower()
        try:
            teksty.append(AN.tekst_z_pdf(p) if rozsz == ".pdf" else MO.tekst_docx(p) if rozsz == ".docx" else
                          MO.tekst_doc(p) if rozsz == ".doc" else "")
        except Exception:
            pass
    tekst_pocz = "\n".join(x[:20000] for x in teksty if x)
    bloki, rozm = AN.wybierz_pliki(pliki, MO.MAX_BAJTOW_ZAPYTANIA)
    if not bloki:
        raise ValueError("Pobrane pliki nie zawierają czytelnej treści.")
    log(f"AI czyta {len(pliki)} plików (ok. {rozm / 1048576:.1f} MB)…")
    dec = tekst_decyzji()
    t = db_przetargi().get(nr, t)
    if not str(c.get("profil_firmy") or "").strip():
        log(KOMUNIKAT_PROFIL + " Analiza bez oceny dopasowania do firmy.")
    w = AN.pelna(dict(t, numer=nr), c, (c.get("profil_firmy", "") + "\n" + dec).strip(), bloki, log)
    if w.get("odwolania"):
        log("Sprawdzam cytaty i odwołania w dokumentach…")
        OD.dodaj(folder, w["odwolania"], katalogi=(".",))
    zapisz_termin_z_analizy(nr, w, tekst_pocz)
    w.pop("termin_iso", None)
    w.update(analiza_zrodlo=f"dokumenty ({len(pliki)} plików)", analiza_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
             dok_pliki=sorted(os.path.relpath(p, folder) for p in pliki)[:80])
    with BLOKADA:
        db = db_przetargi()
        if nr in db:
            db[nr].update({k: v for k, v in w.items() if v not in (None, "")})
            pisz(F_DB, db)
    return {"pliki": len(pliki)}




# ---------- nowa wyszukiwarka: 1) czego szukasz  2) gdzie  3) u kogo  →  Szukaj

INSTYTUCJE = {"urzedy": ("jst", ["gmina", "powiat", "wojewodztwo"]), "szpitale": ("szpital", ["szpital"]), "uczelnie": ("uczelnia", ["uczelnia"]),
              "spolki": ("spolka", ["spolka"]), "wspolnoty": ("wspolnota", [])}


def klucz_obszaru(c=None):
    """Odcisk obszaru wyszukiwania – wyniki zapisanego wyszukiwania są ważne tylko dla obszaru, w którym je znaleziono."""
    c = c or cfg()
    ob = c.get("obszar") or {}
    return json.dumps([ob.get("tryb"), sorted(ob.get("wojewodztwa") or []), c.get("centrum_nazwa") if ob.get("tryb") == "promien" else "",
                       c.get("promien_km") if ob.get("tryb") == "promien" else ""], ensure_ascii=False)


def ostatnie_aktualne():
    """Numery z ostatnich wyszukiwań (wszystkie tryby), ale tylko tych wykonanych w obecnym obszarze."""
    k = klucz_obszaru()
    return {n for v in (czytaj(F_POWIAD, {}).get("ostatnie_wyszukiwanie") or {}).values() if v.get("obszar") == k for n in v.get("numery") or []}


@app.get("/api/wyszukiwarka")
@wymaga_logowania
def wyszukiwarka_stan():
    c = cfg()
    tryb = request.args.get("tryb") or "wykonawca"
    ws = (c.get("wyszukiwarka") or {}).get(tryb) or {}
    slowa = (c.get("slowa_kluczowe_dostawy") or SLOWA_DOSTAWY) if tryb == "dostawca" else (c.get("slowa_kluczowe") or [])
    ob = c.get("obszar") or {}
    return jsonify({"slowa": slowa, "obszar": {"tryb": ob.get("tryb", "promien"), "wojewodztwa": ob.get("wojewodztwa") or [],
                    "miejscowosc": c.get("centrum_opis") or c.get("centrum_nazwa", ""), "promien": c.get("promien_km") or 20, "opis": opis_obszaru(ob, c)},
                    "instytucje": ws.get("instytucje") or [], "cpv": c.get("cpv_dostawy") or [] if tryb == "dostawca" else [],
                    "pobranie": WSP.stan().get("czas") or WSP.stan().get("ostatnie_pobranie") or "", "powiadamiaj": bool(c.get("powiadamiaj_" + tryb, tryb == "wykonawca" and c.get("auto_szukaj", True))),
                    "wojewodztwa": list(WOJEWODZTWA), "promienie": list(REG.PROMIENIE),
                    "ostatnie": dict((czytaj(F_POWIAD, {}).get("ostatnie_wyszukiwanie") or {}).get(tryb) or {},
                                     aktualne=((czytaj(F_POWIAD, {}).get("ostatnie_wyszukiwanie") or {}).get(tryb) or {}).get("obszar") == klucz_obszaru())})


@app.post("/api/wyszukiwarka")
@wymaga_logowania
def wyszukiwarka_szukaj():
    """Zapisuje ustawienia trzech kroków (słowa, obszar, instytucje) i uruchamia wyszukiwanie. Obszar zapisuje istniejące /api/obszar."""
    j = request.json or {}
    tryb = "dostawca" if j.get("tryb") == "dostawca" else "wykonawca"
    if blad_slow(j.get("slowa")):
        return jsonify({"blad": blad_slow(j.get("slowa"))}), 400
    slowa = czysc_slowa(j.get("slowa"))
    if not slowa and not j.get("cpv"):
        return jsonify({"blad": "Krok 1: wpisz co najmniej jedno słowo albo wybierz branżę – czego szukasz."}), 400
    inst = [x for x in (j.get("instytucje") or []) if x in INSTYTUCJE]
    c = cfg()
    ws = dict(c.get("wyszukiwarka") or {})
    ws[tryb] = {"instytucje": inst}
    cpv_ = [re.sub(r"[^0-9]", "", str(x))[:8] for x in (j.get("cpv") or []) if re.sub(r"[^0-9]", "", str(x))][:60]
    if tryb == "dostawca":
        ws[tryb]["cpv"] = cpv_
    zapisz_ustawienia({"slowa_kluczowe_dostawy" if tryb == "dostawca" else "slowa_kluczowe": slowa, "wyszukiwarka": ws,
                       **({"cpv_dostawy": cpv_} if tryb == "dostawca" else {}),
                       "powiadamiaj_" + tryb: bool(j.get("powiadamiaj"))} | ({"auto_szukaj": bool(j.get("powiadamiaj"))} if tryb == "wykonawca" else {}))
    return jsonify(uruchom("szukaj", "Wyszukiwanie przetargów", praca_wyszukiwarka, slowa, tryb, inst))


def praca_wyszukiwarka(log, slowa, tryb, inst):
    """Przy pierwszym wyszukiwaniu z wybranymi instytucjami w danym obszarze program sam znajduje i dodaje ich strony z przetargami."""
    c = cfg()
    typy = sorted({t for x in inst for t in INSTYTUCJE[x][1]})
    if typy and c.get("api_key") and (c.get("obszar") or {}).get("tryb") != "polska":
        klucz_ob = json.dumps([c.get("obszar"), c.get("centrum_nazwa"), c.get("promien_km")], ensure_ascii=False, sort_keys=True)
        zrobione = c.get("odkryte_instytucje") or {}
        brak = [t for t in typy if f"{klucz_ob}|{t}" not in zrobione]
        if brak:
            log("Szukam stron instytucji z Twojego obszaru (pierwszy raz dla tego obszaru – potem już nie)…")
            try:
                for woj, pw in powiaty_obszaru(c, log).items():
                    praca_bip_odkryj(log, woj, pw, brak, od_razu=True)
                zrobione.update({f"{klucz_ob}|{t}": dt.date.today().isoformat() for t in brak})
                zapisz_ustawienia({"odkryte_instytucje": zrobione})
            except Exception as e:
                log(f"Strony instytucji: {e}")
    return praca_szukaj(log, slowa, tryb)
















# ============================================================ projekty (oferty)



def lista_plikow(pid):
    d = os.path.join(pdir(pid), "dokumenty")
    m = meta(pid)
    wyl = set(m.get("pominiete", []))
    wyn = []
    for r, _, pliki in os.walk(d):
        for n in sorted(pliki):
            sc = os.path.join(r, n)
            rel = os.path.relpath(sc, d).replace(os.sep, "/")
            ext = os.path.splitext(n)[1].lower()
            wyn.append({"sciezka": rel, "rozmiar": os.path.getsize(sc), "typ": ext.strip("."),
                        "uwzglednij": rel not in wyl and ext not in (".dwg", ".dxf", ".ath", ".rar", ".7z", ".zip") + MO.PLIKI_WYKONYWALNE})
    return wyn


def wyniki(pid):
    d = pdir(pid)
    return sorted([n for n in os.listdir(d) if n.lower().endswith((".xlsx", ".docx", ".eml", ".zip"))
                   and os.path.isfile(os.path.join(d, n))])




@app.get("/api/projekty")
@wymaga_logowania
def projekty():
    wyn, login, rola = [], session.get("login"), rola_sesji()
    for pid, m in projekty_ro():  # tylko do odczytu – bez kopiowania
        if m and ma_dostep(m, login, rola, lista=True) and not m.get("archiwum") and projekt_w_edycji(m):
            wyn.append({k: m.get(k) for k in ("id", "nazwa", "utworzono", "przetarg_numer", "status_projektu")} |
                       {"typ": m.get("typ") or "przetarg", "rodzaj_zamowienia": m.get("rodzaj_zamowienia"), "wlasciciel": m.get("wlasciciel") or login_admina(),
                        "dostep": m.get("dostep") or [], "link": (m.get("przetarg") or {}).get("link"),
                        "termin_ofert": (m.get("przetarg") or {}).get("termin_ofert"), "notatek": len([x for x in m.get("notatki", []) if not x.get("archiwum")])} |
                       {"brutto": (m.get("oferta") or {}).get("brutto"), "wspolnota": projekt_wspolnoty(m)})
    for x in wyn:
        x["dostep"] = UWIERZ.filtr_dostepu(x["dostep"])  # H1-01: administrator konta widzi udostępnienia tylko w swojej firmie
    return jsonify(ukryj_innych(sorted(wyn, key=lambda x: x.get("utworzono") or "", reverse=True)))


TYPY_ZAMAWIAJACEGO = ("zamowienie", "inwestorski", "weryfikacja", "dokumentacja", "inwestycja")


def zamowienie_powiazane(m):
    """Zamówienie, z którego utworzono ocenę ofert (pole zamowienie_id), albo sam projekt, gdy powiązania nie ma – do zmian i zapisu."""
    zid = (m or {}).get("zamowienie_id")
    return meta(zid) if zid and os.path.isfile(os.path.join(PROJ, zid, "projekt.json")) else m


def projekt_wspolnoty(m):
    """Czy projekt należy do modułu wspólnot / spółdzielni / deweloperów (osobne dane i reguły) – a nie do zamawiającego publicznego."""
    if m.get("prywatny"):
        return True
    if (m.get("kreator") or {}).get("prywatny"):
        return True
    zid = m.get("zamowienie_id")
    if zid and m.get("typ") == "ocena_ofert" and os.path.isfile(os.path.join(PROJ, zid, "projekt.json")):
        return bool(((czytaj_ro(os.path.join(PROJ, zid, "projekt.json"), {}) or {}).get("kreator") or {}).get("prywatny"))
    return False


def zgodny_modul(m, modul):
    """Filtr list zamawiającego: modul = „wspolnota” albo „gmina” (brak parametru – bez filtra)."""
    return not modul or projekt_wspolnoty(m) == (modul == "wspolnota")
INWESTORSKIE = ("inwestorski", "zamowienie")
TYPY_PROJEKTOW = ("przetarg", "wlasny", "kosztorys", "dom", "dotacja", "wniosek_dot", "ocena_ofert", "zapytanie", "nieruchomosc", "prawnik") + TYPY_ZAMAWIAJACEGO


def oferta_przygotowana(m):
    """Projekt z przetargu: czy z kosztorysu przygotowano już ofertę (formularze). Starsze projekty z formularzami – tak."""
    return bool(m.get("oferta_przygotowana")) or any("_formularze" in str(x) for x in (m.get("pliki_oferty") or []))


def tylko_kosztorys_typ(m):
    # najpierw sam kosztorys (AI albo wgrany własny); oferta powstaje osobnym przyciskiem na jego podstawie:
    # projekt własny – oferta dla klienta, projekt z przetargu – formularze ofertowe i analiza
    if (m.get("typ") or "przetarg") == "przetarg":
        if m.get("rodzaj_zamowienia") in ("dostawy", "uslugi"):  # dostawca: od razu formularz cenowy + formularz ofertowy
            return False
        return not oferta_przygotowana(m)
    return m.get("typ") in ("kosztorys", "inwestorski", "zamowienie", "dom", "wlasny")


def strona_typu(typ):
    if typ == "prawnik":
        return "prawnik"
    return "zamawiajacy" if typ in TYPY_ZAMAWIAJACEGO or typ == "ocena_ofert" else "inwestor" if typ == "dom" else "dotacje" if typ in ("dotacja", "wniosek_dot", "zapytanie") else "nieruchomosci" if typ == "nieruchomosc" else "wykonawca"


@app.post("/api/projekty")
@wymaga_logowania
def projekt_nowy():
    nr = request.json.get("przetarg")
    if nr:  # jedna oferta na postępowanie: istniejący projekt tego konta dla tego przetargu jest otwierany, a nie dublowany
        k = konto_biezace()
        t0 = db_przetargi().get(nr) or {}
        p0 = W.norm(t0.get("przedmiot") or "")[:150]
        kl0 = p0 + "|" + W.norm(t0.get("zamawiajacy") or "")[:20] if len(p0) >= 12 else None
        for pid_ in os.listdir(PROJ):
            m_ = czytaj(os.path.join(PROJ, pid_, "projekt.json"), None)
            if not m_ or m_.get("archiwum") or (m_.get("wlasciciel") or login_admina()) != k:
                continue
            pm = m_.get("przetarg") or {}
            kl_ = W.norm(pm.get("przedmiot") or "")[:150] + "|" + W.norm(pm.get("zamawiajacy") or "")[:20]
            if m_.get("przetarg_numer") == nr or (kl0 and m_.get("przetarg_numer") and kl_ == kl0):  # to samo postępowanie z BZP i z TED
                return jsonify(dict(m_, istniejacy=True))
    pid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(PROJ, pid, "dokumenty"))
    t = db_przetargi().get(nr) if nr else None
    nazwa = (request.json.get("nazwa") or (t or {}).get("przedmiot", "")[:70] or "Nowa oferta").strip()
    typ = request.json.get("typ") if request.json.get("typ") in TYPY_PROJEKTOW else "przetarg"
    m = {"id": pid, "nazwa": nazwa, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "typ": typ,
         "strona": strona_typu(typ), "prywatny": bool(request.json.get("prywatny")) if typ in ("ocena_ofert",) + TYPY_ZAMAWIAJACEGO and EDYCJA != "zamawiajacy" else False,
         "wlasciciel": konto_biezace() or login_admina(), "dostep": [],
         "przetarg_numer": nr, "przetarg": dict(t, numer=nr) if t else None, "pominiete": []}
    if typ in TYPY_ZAMAWIAJACEGO:
        m["rodzaj_zamowienia"] = request.json.get("rodzaj_zamowienia") if request.json.get("rodzaj_zamowienia") in ZAM.RODZAJE_ZAM else "roboty"
    elif typ == "prawnik":  # sprawa prawnika: przedmiot, tryb, dla kogo (zmieniają listę kontrolną)
        m["prawnik"] = PRW.ustawienia({"prawnik": request.json.get("prawnik") or {}})
        m["rodzaj_zamowienia"] = m["prawnik"]["przedmiot"]
        m["cel_prawnika"] = "sporzadz" if request.json.get("przygotuj") else "sprawdz"  # ścieżka: sprawdzenie → opinia albo sporządzenie → komplet
        if m["cel_prawnika"] == "sporzadz":
            m["prawnik"]["dla_kogo"] = "zamawiajacy"
    elif typ == "ocena_ofert":
        m["ocena"] = {"swz": {}, "oferty": [], "podsum": {}}
        if request.json.get("prawnik") is not None:  # prawnik: sprawdzenie ofert w przetargu (osobna lista, ustawienia sprawy)
            m["strona"] = "prawnik"
            m["prawnik"] = PRW.ustawienia({"prawnik": request.json["prawnik"] if isinstance(request.json["prawnik"], dict) else {}})
    elif typ == "zapytanie":  # beneficjent dotacji – wybór wykonawcy wg zasady konkurencyjności
        dot_id = str(request.json.get("dotacja_id") or "")
        dm = czytaj(os.path.join(PROJ, dot_id, "projekt.json"), None) if re.fullmatch(r"[0-9a-f]{12}", dot_id) else None
        if dm and (dm.get("typ") != "dotacja" or not ma_dostep(dm)):  # GC-07: tylko własny projekt rozliczenia dotacji
            dm = None
        m["zapytanie"] = {"dane": {"przedmiot": nazwa, "rodzaj": request.json.get("rodzaj") or "roboty",
                                   "beneficjent": (cfg().get("firma") or {}).get("nazwa") or cfg().get("firma_nazwa", ""),
                                   "data_szacowania": dt.date.today().isoformat()},
                          "dotacja_id": dot_id if dm else "", "publikacja": {}, "lista": {}}
        if dm:
            dm.setdefault("zapytania", []).append(pid)
            zapisz_meta(dot_id, dm)
    elif typ == "przetarg" and (request.json.get("rodzaj_zamowienia") in ("dostawy", "uslugi")
                                or (not request.json.get("rodzaj_zamowienia") and t and rodzaj_przetargu(t) in ("dostawy", "uslugi"))):
        # oferta dostawcy / usługodawcy – rodzaj z wyboru albo z ogłoszenia (usługi nie mogą trafić do ścieżki kosztorysu robót)
        m["rodzaj_zamowienia"] = request.json.get("rodzaj_zamowienia") or rodzaj_przetargu(t)
        m["strona"] = "dostawca"
    zapisz_meta(pid, m)
    skopiowane = 0
    if nr and os.path.isdir(folder_przetargu(nr)):  # dokumenty pobrane już przy pełnej analizie
        shutil.copytree(folder_przetargu(nr), os.path.join(PROJ, pid, "dokumenty"), dirs_exist_ok=True)
        skopiowane = sum(len(ns) for _, _, ns in os.walk(os.path.join(PROJ, pid, "dokumenty")))
    return jsonify(dict(m, dokumenty_skopiowane=skopiowane))


def dane_przetargu(m, pid):
    """Najdokładniejsze podstawowe dane przetargu: aktualny rekord z listy przetargów (termin, analiza) + dane odczytane
    przez AI z dokumentów przy przygotowaniu oferty (numer, nazwa, zamawiający – urzędowo z wykazu VAT). Zwraca słownik."""
    t = dict(m.get("przetarg") or {})
    nr = m.get("przetarg_numer") or t.get("numer")
    if nr:
        biezacy = db_przetargi().get(nr)
        if biezacy:
            t.update({k: v for k, v in biezacy.items() if v not in (None, "", []) and k != "_surowe"})
            t["numer"] = nr
    P = (czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie", {})
    wyb = lambda *w: next((str(x).strip() for x in w if x not in (None, "") and str(x).strip() and not str(x).startswith("[UZUPEŁNIJ")), "")
    termin_dok = AN.data_i_godzina(P.get("termin_skladania")) if P.get("termin_skladania") else None
    return {
        "numer": wyb(P.get("numer"), t.get("numer")), "numer_bazy": t.get("numer", ""),
        "nazwa": wyb(P.get("nazwa_zamowienia"), t.get("przedmiot")),
        "zamawiajacy": wyb(P.get("zamawiajacy_nazwa"), t.get("zamawiajacy")), "zamawiajacy_adres": wyb(P.get("zamawiajacy_adres")),
        "zamawiajacy_nip": wyb(P.get("zamawiajacy_nip")), "lokalizacja": wyb(P.get("obiekt"), t.get("lokalizacja_robot"), t.get("lokalizacja")),
        "termin_ofert": wyb(t.get("termin_ofert"), termin_dok), "termin_zrodlo": t.get("termin_zrodlo") or ("dokumenty" if termin_dok else ""),
        "wadium": wyb(P.get("wadium"), t.get("wadium")), "termin_realizacji": wyb(P.get("termin_wykonania"), t.get("termin_realizacji")),
        "kryteria": wyb(P.get("kryteria"), t.get("kryteria_oceny")), "wynagrodzenie": wyb(P.get("wynagrodzenie"), t.get("wynagrodzenie")),
        "gwarancja": wyb(f"min. {P['gwarancja_min_mies']} mies." if P.get("gwarancja_min_mies") else "", t.get("gwarancja")),
        "szacowana_wartosc": wyb(t.get("szacowana_wartosc")), "sposob_skladania": wyb(P.get("sposob_skladania"), t.get("miejsce_skladania")),
        "zrodlo": t.get("zrodlo", ""), "link": t.get("link", ""), "przedmiot": t.get("przedmiot", ""),
    }


# ---------- moje wyniki: złożone oferty, wygrane i przegrane (wynik z BZP albo wpisany ręcznie)

F_WYNIKI_OFERT = SciezkaKonta("wyniki_ofert.json")


def _moja_firma():
    c = cfg()
    return c.get("firma_nazwa", ""), re.sub(r"\D", "", c.get("firma_nip", "") or "")


def _ustaw_status_przetargu(nr, st):
    if not nr:
        return
    with BLOKADA:
        db = db_przetargi()
        if nr in db:
            db[nr]["status"] = st
            pisz(F_DB, db)
            t_ = dict(db[nr])
        else:
            t_ = None
    if t_ and st in ("oferta złożona", "wygrany", "przegrany"):  # wynik oferty – wskazówka do kolejnych ocen AI (tekst_decyzji)
        zapisz_decyzje(nr, t_, st)


@app.post("/api/projekty/<pid>/oferta-zlozona")
@wymaga_logowania
def oferta_zlozona(pid):
    """Zapis złożonej oferty (cena, data) – program później sam sprawdzi wynik w BZP."""
    m = meta(pid)
    j = request.json or {}
    if j.get("cofnij"):
        with BLOKADA:
            W = czytaj(F_WYNIKI_OFERT, {}) or {}
            x = W.pop(pid, None)
            pisz(F_WYNIKI_OFERT, W)
        if x and x.get("numer"):  # cofnięcie: status przetargu sprzed zapisu, bez decyzji „oferta złożona / wygrany / przegrany”
            nr = x["numer"]
            with BLOKADA:
                db = db_przetargi()
                st_wyn = ("oferta złożona", "wygrany", "przegrany") + (("odpuszczamy",) if (x.get("wynik") or {}).get("status") == "unieważniony" else ())
                if nr in db and db[nr].get("status") in st_wyn:  # także „odpuszczamy” nadane przez wynik „unieważniony”
                    db[nr]["status"] = x.get("status_przed") or "startujemy"
                    pisz(F_DB, db)
                dec = czytaj(F_DECYZJE, [])
                dec2 = [d_ for d_ in dec if not (d_.get("numer") == nr and d_.get("decyzja") in ("oferta złożona", "wygrany", "przegrany"))]
                if len(dec2) != len(dec):
                    pisz(F_DECYZJE, dec2)
        return jsonify({"ok": True})
    t = dane_przetargu(m, pid) if m.get("przetarg") else {}
    zap_ = (czytaj(F_WYNIKI_OFERT, {}) or {}).get(pid) or {}
    if (zap_.get("wynik") or {}).get("status") not in (None, "oczekuje"):
        return jsonify({"blad": "Wynik tej oferty jest już zapisany – aby zmienić dane złożonej oferty, najpierw kliknij „Cofnij”."}), 409
    try:
        cena = MO.liczba_pl(j.get("cena_brutto") or (m.get("oferta") or {}).get("brutto") or 0)
    except ValueError:
        return jsonify({"blad": "Podaj cenę oferty brutto (liczba, np. 250 000,50)."}), 400
    if cena <= 0:
        return jsonify({"blad": "Cena oferty brutto musi być większa od zera – przygotuj ofertę albo wpisz cenę brutto." if j.get("cena_brutto")
                        else "Najpierw przygotuj ofertę albo wpisz cenę brutto."}), 400
    data_zl = str(j.get("data") or "").strip()[:10] or dt.date.today().isoformat()
    try:
        dt.date.fromisoformat(data_zl)
    except ValueError:
        return jsonify({"blad": "Podaj datę złożenia oferty w formacie RRRR-MM-DD (np. 2026-12-15)."}), 400
    nr = m.get("przetarg_numer") or (m.get("przetarg") or {}).get("numer") or ""
    surowy = db_przetargi().get(nr) or {}
    with BLOKADA:
        W = czytaj(F_WYNIKI_OFERT, {}) or {}
        W[pid] = {"pid": pid, "numer": nr, "przedmiot": t.get("przedmiot") or m.get("nazwa", ""), "zamawiajacy": t.get("zamawiajacy") or "",
                  "cpv": surowy.get("cpv", ""), "nip_zam": _nip_z_surowych(surowy), "nasza_cena": round(cena, 2),
                  "data_zlozenia": data_zl, "termin_ofert": str(t.get("termin_ofert") or "")[:10],
                  "wynik": {"status": "oczekuje"},
                  "status_przed": (W.get(pid) or {}).get("status_przed") or (surowy.get("status") if surowy.get("status") not in ("oferta złożona", "wygrany", "przegrany") else "startujemy")}
        pisz(F_WYNIKI_OFERT, W)
    _ustaw_status_przetargu(nr, "oferta złożona")
    return jsonify(W[pid])


@app.post("/api/projekty/<pid>/wynik-oferty")
@wymaga_logowania
def wynik_oferty_reczny(pid):
    j = request.json or {}
    st = j.get("status")
    if st not in ("wygrana", "przegrana", "unieważniony"):
        return jsonify({"blad": "Wybierz wynik."}), 400
    with BLOKADA:
        W = czytaj(F_WYNIKI_OFERT, {}) or {}
        x = W.get(pid)
        if not x:
            return jsonify({"blad": "Najpierw zapisz złożoną ofertę."}), 400
        f = lambda v: MO.liczba_pl(v) if str(v or "").strip() else None
        try:
            cz = f(j.get("cena_zwyciezcy"))
            if cz is not None and cz <= 0:
                return jsonify({"blad": "Cena zwycięzcy musi być większa od zera (albo zostaw pole puste)."}), 400
            x["wynik"] = {"status": st, "zwyciezca": str(j.get("zwyciezca") or "")[:160], "cena_zwyciezcy": cz, "ofert": int(j["ofert"]) if re.fullmatch(r"[0-9]{1,4}", str(j.get("ofert") or "")) else None,
                          "zrodlo": "wpisane ręcznie", "data_wyniku": dt.date.today().isoformat()}
        except ValueError:
            return jsonify({"blad": "Nieprawidłowa kwota."}), 400
        if cz and st == "przegrana":
            x["wynik"]["roznica_proc"] = round((x["nasza_cena"] / cz - 1) * 100, 1)
        pisz(F_WYNIKI_OFERT, W)
    _ustaw_status_przetargu(x.get("numer"), {"wygrana": "wygrany", "przegrana": "przegrany"}.get(st, "odpuszczamy"))
    return jsonify(x)


def praca_sprawdz_wyniki(log, pid=None):
    """Szuka w BZP ogłoszeń o wyniku dla złożonych ofert (po terminie składania) i zapisuje: wygrana / przegrana, zwycięzca, różnica ceny."""
    W = czytaj(F_WYNIKI_OFERT, {}) or {}
    firma, nip_f = _moja_firma()
    dzis = dt.date.today().isoformat()
    do_spr = [x for k, x in W.items() if (not pid or k == pid) and (x.get("wynik") or {}).get("status") == "oczekuje" and (x.get("termin_ofert") or "") <= dzis]
    if not do_spr:
        log("Brak ofert oczekujących na wynik po terminie składania.")
        return {"sprawdzono": 0}
    zmian = 0
    for i, x in enumerate(do_spr, 1):
        log(f"Sprawdzam wynik {i}/{len(do_spr)}: {x['przedmiot'][:70]}")
        if str(x.get("numer") or "").startswith("BK-"):  # przetarg z Bazy Konkurencyjności – wynik wprost z ogłoszenia
            t_ = db_przetargi().get(x["numer"]) or {}
            wyn = [dict(cz, przedmiot=x["przedmiot"], data=x.get("termin_ofert") or "", cpv=x.get("cpv", ""))
                   for cz in bk_wynik_ogloszenia(t_.get("bk_id") or x["numer"], wymus=True)]
        else:
            try:
                wyn = HZ.pobierz_wyniki(x["zamawiajacy"], lambda *_: None, 12, x.get("nip_zam", ""))
            except Exception as e:
                log(f"BZP niedostępny: {opis_bledu_zadania(e, 'szukaj')}")
                continue
        kand = [w for w in wyn if (w.get("data") or "") >= (x.get("termin_ofert") or x.get("data_zlozenia") or "")[:10]
                and HZ.podobienstwo(x["przedmiot"], w.get("przedmiot", ""), x.get("cpv", ""), w.get("cpv", "")) >= 0.7]
        if not kand:
            continue
        kand.sort(key=lambda w: HZ.podobienstwo(x["przedmiot"], w.get("przedmiot", ""), x.get("cpv", ""), w.get("cpv", "")), reverse=True)
        w = kand[0]
        if w.get("uniewaznione"):
            st = "unieważniony"
        else:
            nasz = (nip_f and re.sub(r"\D", "", w.get("nip") or "") == nip_f) or (firma and HZ.ten_sam_zamawiajacy(firma, w.get("wykonawca", "")))
            st = "wygrana" if nasz else "przegrana"
        wynik = {"status": st, "zwyciezca": w.get("wykonawca", ""), "cena_zwyciezcy": w.get("cena"), "najnizsza": w.get("najnizsza"), "najwyzsza": w.get("najwyzsza"),
                 "ofert": w.get("ofert"), "zrodlo": "Baza Konkurencyjności" if str(x.get("numer") or "").startswith("BK-") else "BZP",
                 "numer_ogloszenia": w.get("numer") or x.get("numer"), "link": w.get("link"), "data_wyniku": w.get("data")}
        if w.get("cena") and st == "przegrana":
            wynik["roznica_proc"] = round((x["nasza_cena"] / w["cena"] - 1) * 100, 1)
        with BLOKADA:
            W2 = czytaj(F_WYNIKI_OFERT, {}) or {}
            if x["pid"] in W2:
                W2[x["pid"]]["wynik"] = wynik
                pisz(F_WYNIKI_OFERT, W2)
        _ustaw_status_przetargu(x.get("numer"), {"wygrana": "wygrany", "przegrana": "przegrany"}.get(st, "odpuszczamy"))
        zmian += 1
        log(f"Wynik: {st} – {w.get('wykonawca', '')[:60]}")
    log(f"Gotowe: znaleziono wyniki dla {zmian} z {len(do_spr)} ofert.")
    return {"sprawdzono": len(do_spr), "znaleziono": zmian}


@app.post("/api/wyniki-ofert/sprawdz")
@wymaga_logowania
def wyniki_sprawdz():
    return jsonify(uruchom("historia", "Sprawdzanie wyników przetargów (BZP)", praca_sprawdz_wyniki, (request.json or {}).get("pid")))


@app.get("/api/wyniki-ofert")
@wymaga_logowania
def wyniki_ofert():
    W = list((czytaj(F_WYNIKI_OFERT, {}) or {}).values())
    W.sort(key=lambda x: x.get("data_zlozenia", ""), reverse=True)
    rozstrz = [x for x in W if x["wynik"]["status"] in ("wygrana", "przegrana")]
    wyg = [x for x in rozstrz if x["wynik"]["status"] == "wygrana"]
    roz = [x["wynik"]["roznica_proc"] for x in rozstrz if x["wynik"].get("roznica_proc") is not None]
    grupy = {}
    for x in rozstrz:
        g = HZ.grupa_cpv(x.get("cpv"), x.get("przedmiot"))
        y = grupy.setdefault(g, {"grupa": g, "zlozone": 0, "wygrane": 0, "roznice": []})
        y["zlozone"] += 1
        y["wygrane"] += x["wynik"]["status"] == "wygrana"
        if x["wynik"].get("roznica_proc") is not None:
            y["roznice"].append(x["wynik"]["roznica_proc"])
    gr = []
    for y in grupy.values():
        gr.append({"grupa": y["grupa"], "zlozone": y["zlozone"], "wygrane": y["wygrane"],
                   "srednia_roznica": round(sum(y["roznice"]) / len(y["roznice"]), 1) if y["roznice"] else None})
    gr.sort(key=lambda y: -y["zlozone"])
    return jsonify({"oferty": W, "stat": {"zlozone": len(W), "rozstrzygniete": len(rozstrz), "wygrane": len(wyg),
                    "skutecznosc": round(100 * len(wyg) / len(rozstrz)) if rozstrz else None,
                    "srednia_roznica": round(sum(roz) / len(roz), 1) if roz else None, "oczekuje": sum(1 for x in W if x["wynik"]["status"] == "oczekuje")},
                    "grupy": gr})


# ---------- raport: zwycięzcy przetargów w województwie według powiatów (Excel)

KAT_WYNIKI_DNI = os.path.join(DATA, "bzp_wyniki_dni")  # pamięć: wyniki z każdego dnia (dane publiczne, wspólne)
F_POWIATY_MIAST = os.path.join(DATA, "powiaty_miejscowosci.json")


def powiat_miejscowosci(miasto, woj, pam):
    """Powiat miejscowości (siedziby zamawiającego) – z pamięci albo z mapy (OpenStreetMap), zapamiętany na stałe."""
    k = f"{woj}|{miasto}"
    if k in pam:
        return pam[k]
    pw = ""
    try:
        time.sleep(1.1)  # zasady serwisu map: najwyżej 1 zapytanie na sekundę
        for x in REG.szukaj_miejscowosci(f"{miasto}, województwo {woj}"):
            if x.get("wojewodztwo") == woj:
                pw = x.get("powiat") or x.get("nazwa") or ""
                break
    except Exception:
        return ""
    pw = re.sub(r"^(powiat|miasto na prawach powiatu)\s+", "", pw.strip(), flags=re.I)
    pam[k] = pw
    return pw


F_BK_WYNIKI = os.path.join(DATA, "bk_wyniki_ogloszen_v2.json")  # v2: poprawiony odczyt (wcześniejsze wyniki sprawdzane od nowa)  # pamięć rozstrzygnięć ogłoszeń BK (wspólna, dane publiczne)


KAT_BK_SUROWE = os.path.join(DATA, "bk_surowe")
BK_DODATKOWE = ("", "/details", "/offers", "/results", "/result", "/resolution", "/settlement", "/settlements", "/winners", "/orders",
                "/offers/public", "/selected-offer", "/summary")
BK_PDF = ("/pdf", "/print", "/export/pdf", "/download", "/download/pdf")  # wersja „Pobierz plik PDF” – zawiera też rozstrzygnięcie








BK_LIMIT_AI = {"pozostalo": None}  # limit odczytów przez AI w jednym raporcie (zapasowy odczyt kosztuje tokeny)














def wyniki_bk_wojewodztwa(log, woj, od):
    """Rozstrzygnięcia z Bazy Konkurencyjności (zamawiający niepubliczni: wspólnoty, spółdzielnie, firmy, organizacje – projekty z funduszy UE).
    Indeks ogłoszeń i wyniki są pamiętane; przy kolejnych raportach program dociąga tylko nowe ogłoszenia i sprawdza te bez wyniku."""
    import bk as BKM
    plik = os.path.join(DATA, f"bk_indeks_{DOT.bezpieczna(woj)}.json")
    I = czytaj(plik, {}) or {}
    ogl = I.setdefault("ogloszenia", {})
    if I.get("wersja") != 2:  # poprawiony odczyt rozstrzygnięć – wyniki zapisane wcześniej sprawdzamy ponownie
        for x in ogl.values():
            x["wynik"], x["sprawdzono"] = None, ""
        I["wersja"] = 2
    granica = od.isoformat()
    u = urllib.parse.urlsplit(cfg().get("bk_url") or BKM.SZUKAJ)
    baza_q = [(k, v) for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True) if k not in ("page", "limit")]
    ost_skan = I.get("ostatni_skan", "")
    poza = I.setdefault("poza", {})  # ogłoszenia spoza województwa (żeby nie sprawdzać ich ponownie)
    bez_miejsca = I.setdefault("bez_miejsca", {})  # ogłoszenia, których lista nie podaje miejsca – miejsce ze szczegółów
    stat = {"lista": 0, "w_woj": 0, "bez_miejsca": 0}
    for strona in range(1, 2500):
        url = urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, urllib.parse.urlencode(baza_q + [("page", str(strona)), ("limit", "100")]), ""))
        try:
            lista = BKM.znajdz_liste(BKM._get(url)) or []
        except Exception as e:
            log(f"Baza Konkurencyjności: strona {strona} – błąd ({e})")
            break
        if strona == 1:
            os.makedirs(KAT_BK_SUROWE, exist_ok=True)
            pisz(os.path.join(KAT_BK_SUROWE, "_lista_strona1.json"), lista[:30])  # próbka do diagnostyki
        daty, znane = [], 0
        for n in lista:
            if not isinstance(n, dict):
                continue
            o = BKM.normalizuj(n)
            daty.append(o["data_publikacji"][:10])
            stat["lista"] += 1
            sid = str(o["bk_id"])
            if sid in ogl or sid in poza:
                znane += 1
                continue
            if o["data_publikacji"][:10] and o["data_publikacji"][:10] < granica:
                continue
            a = n.get("advertisement") if isinstance(n.get("advertisement"), dict) else n
            mies = BKM._miejsca(a.get("orders") or a)
            tekst_ = json.dumps(n, ensure_ascii=False).lower()
            w_woj = any(str(m.get("voivodeship") or "").strip().lower() == woj for m in mies) or o.get("wojewodztwo") == woj or f'"{woj}"' in tekst_ \
                or f"województwo {woj}" in tekst_ or f"woj. {woj}" in tekst_
            if not w_woj:
                if mies or "voivodeship" in tekst_ or "województwo" in tekst_:
                    poza[sid] = 1
                else:
                    bez_miejsca[sid] = {"data": o["data_publikacji"][:10]}
                    stat["bez_miejsca"] += 1
                continue
            stat["w_woj"] += 1
            pw = next((str(m.get("poviat")).strip() for m in mies if m.get("poviat") and str(m.get("voivodeship") or "").strip().lower() == woj), "")
            ogl[str(o["bk_id"])] = {"data": o["data_publikacji"][:10], "termin": (o["termin_ofert"] or "")[:10], "zamawiajacy": o["zamawiajacy"],
                                    "przedmiot": o["przedmiot"][:300], "miasto": (o["miasto"] or "").split(",")[0].strip(), "powiat": pw, "numer": o["numer"],
                                    "kategoria": o.get("kategoria", ""), "cpv": (o.get("cpv") or "").split(",")[0].strip(),
                                    "wynik": None, "sprawdzono": ""}
        if strona % 10 == 0:
            log(f"Baza Konkurencyjności: przeglądanie ogłoszeń – strona {strona}, w województwie: {len(ogl)}")
            pisz(plik, I)
        if len(lista) < 100 or (daty and max(daty) < granica) or (ost_skan and znane == len(lista) and daty and max(daty) < ost_skan):
            break
    # ogłoszenia, których lista nie podaje miejsca realizacji: miejsce ze szczegółów (do 1500 na raport – kolejne przy następnych raportach)
    do_ustal = [k for k, v in bez_miejsca.items() if v.get("data", "") >= granica][:1500]
    if do_ustal:
        log(f"Baza Konkurencyjności: ustalanie miejsca realizacji z ogłoszeń – {len(do_ustal)} (pozostało {len(bez_miejsca)})")
    for i, k in enumerate(do_ustal, 1):
        o = {"bk_id": k, "numer": f"BK-{k}"}
        try:
            BKM.uzupelnij_szczegoly(o)
        except Exception:
            continue
        data_ = (bez_miejsca.pop(k, None) or {}).get("data", "")
        if (o.get("wojewodztwo") or "").lower() == woj or woj in (o.get("_surowe") or "").lower():
            ogl[k] = {"data": data_ or (o.get("data_publikacji") or "")[:10], "termin": (o.get("termin_ofert") or "")[:10], "zamawiajacy": o.get("zamawiajacy", ""),
                      "przedmiot": (o.get("przedmiot") or "")[:300], "miasto": (o.get("miasto") or "").split(",")[0].strip(), "powiat": "",
                      "numer": f"BK-{k}", "kategoria": o.get("kategoria", ""), "cpv": (o.get("cpv") or "").split(",")[0].strip(), "wynik": None, "sprawdzono": ""}
        else:
            poza[k] = 1
        if i % 50 == 0:
            log(f"Baza Konkurencyjności: ustalanie miejsca {i}/{len(do_ustal)}")
            pisz(plik, I)
    # przegląd po numerach ogłoszeń: lista BK pokazuje głównie ogłoszenia otwarte, więc rozstrzygnięte wcześniej trzeba odnaleźć po numerze
    try:
        ids_listy = [int(k) for k in list(ogl) + list(poza) + list(bez_miejsca) if str(k).isdigit()]
        max_id = max(ids_listy + [int(I.get("max_id") or 0)]) if ids_listy or I.get("max_id") else 0
        I["max_id"] = max_id
        if max_id:
            min_id = (I.get("min_id") or {}).get(granica)
            if not min_id:
                lo, hi = max(1, max_id - 600000), max_id
                while hi - lo > 50:
                    mid = (lo + hi) // 2
                    d_ = None
                    for p_ in range(mid, mid + 6):
                        d_ = _bk_szczeg(BKM, p_)
                        if d_:
                            break
                    data_ = BKM.normalizuj(d_)["data_publikacji"][:10] if d_ else ""
                    if not data_ or data_ >= granica:
                        hi = mid
                    else:
                        lo = mid
                min_id = lo
                I.setdefault("min_id", {})[granica] = min_id
            znane_ = set(ogl) | set(poza)
            do_skan = [i for i in range(max_id, min_id - 1, -1) if str(i) not in znane_][:20000]
            wszystkie_ = max_id - min_id + 1
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=3) as pula:  # kilka zapytań naraz, ale z umiarem – serwer musi dalej odpowiadać
                for i0 in range(0, len(do_skan), 30):
                    paczka = do_skan[i0:i0 + 30]
                    for n_, d_ in zip(paczka, pula.map(lambda x: _bk_szczeg(BKM, x), paczka)):
                        if not d_:
                            poza[str(n_)] = 0
                            continue
                        o = BKM.normalizuj(d_)
                        a = d_.get("advertisement") if isinstance(d_.get("advertisement"), dict) else d_
                        mies = BKM._miejsca(a.get("orders") or a)
                        t_ = json.dumps(d_, ensure_ascii=False).lower()
                        if any(str(m.get("voivodeship") or "").strip().lower() == woj for m in mies) or f'"{woj}"' in t_ or f"województwo {woj}" in t_:
                            pw = next((str(m.get("poviat")).strip() for m in mies if m.get("poviat") and str(m.get("voivodeship") or "").strip().lower() == woj), "")
                            ogl[str(n_)] = {"data": o["data_publikacji"][:10], "termin": (o["termin_ofert"] or "")[:10],
                                            "zamawiajacy": o["zamawiajacy"] or _bk_zamawiajacy(d_),
                                            "przedmiot": o["przedmiot"][:300], "miasto": (o["miasto"] or "").split(",")[0].strip(), "powiat": pw,
                                            "numer": f"BK-{n_}", "kategoria": o.get("kategoria", ""), "cpv": (o.get("cpv") or "").split(",")[0].strip(),
                                            "wynik": None, "sprawdzono": ""}
                        else:
                            poza[str(n_)] = 1
                        del d_, t_
                    time.sleep(0.2)  # oddech dla serwera (odpowiedzi dla użytkowników i kontrola działania)
                    if (i0 // 30) % 10 == 0 or i0 + 30 >= len(do_skan):
                        pisz(plik, I)
                    if True:  # postęp i możliwość przerwania po każdej paczce
                        log(f"Baza Konkurencyjności: przegląd numerów ogłoszeń {min(i0 + 30, len(do_skan))}/{len(do_skan)} "
                            f"(sprawdzono łącznie {min(wszystkie_, len(set(ogl) | set(poza)))} z {wszystkie_})")
            pozostalo = max(0, wszystkie_ - len({k for k in set(ogl) | set(poza) if str(k).isdigit() and min_id <= int(k) <= max_id}))
            I["pozostalo_numerow"] = pozostalo
            if pozostalo:
                log(f"Baza Konkurencyjności: do przejrzenia zostało {pozostalo} numerów ogłoszeń – uruchom raport ponownie, aby uzupełnić dane.")
    except Exception as e:
        log(f"Baza Konkurencyjności: przegląd po numerach przerwany ({e}).")
    log(f"Baza Konkurencyjności: przejrzano {stat['lista']} ogłoszeń z listy, w województwie {stat['w_woj']}, bez miejsca w liście {stat['bez_miejsca']}; "
        f"w indeksie województwa łącznie {len(ogl)}.")
    I["ostatni_skan"] = dt.date.today().isoformat()
    pisz(plik, I)
    dzis = dt.date.today().isoformat()
    do_spr = [k for k, x in ogl.items() if x["data"] >= granica and (x["termin"] or x["data"]) < dzis and x["wynik"] is None
              and (not x["sprawdzono"] or (dt.date.today() - dt.date.fromisoformat(x["sprawdzono"])).days >= 14)]
    for i, k in enumerate(do_spr, 1):
        ogl[k]["sprawdzono"] = dzis
        w = bk_wynik_ogloszenia(k, wymus=True)
        if w:
            ogl[k]["wynik"] = w
        if i % 20 == 0 or i == len(do_spr):
            log(f"Baza Konkurencyjności: sprawdzanie wyników {i}/{len(do_spr)}")
            pisz(plik, I)
    wyn = []
    for k, x in ogl.items():
        if x["data"] < granica or not x.get("wynik"):
            continue
        for cz in x["wynik"]:
            if cz.get("wykonawca"):
                nz_, sd_ = HZ.rozdziel_adres(cz["wykonawca"], cz.get("siedziba", ""))
                cz = dict(cz, wykonawca=nz_, siedziba=sd_)
            wyn.append({"numer": x["numer"], "data": x["termin"] or x["data"], "zamawiajacy": x["zamawiajacy"], "miasto": x["miasto"], "powiat_bk": x["powiat"],
                        "przedmiot": x["przedmiot"], "cpv": x.get("cpv", ""), "kategoria": x.get("kategoria", ""), "zrodlo": "Baza Konkurencyjności", **cz})
    log(f"Baza Konkurencyjności: rozstrzygnięć z wybranym wykonawcą – {sum(1 for w in wyn if w.get('wykonawca'))}.")
    return wyn


def praca_raport_powiatow(log, woj, miesiecy, z_bk=True, zakresy=None, od_nowa=False):
    BK_LIMIT_AI["pozostalo"] = int(cfg().get("bk_limit_ai", 50) or 0)  # najwyżej tyle odczytów AI na raport
    try:
        return _praca_raport_powiatow(log, woj, miesiecy, z_bk, zakresy, od_nowa)
    finally:
        BK_LIMIT_AI["pozostalo"] = None


def _praca_raport_powiatow(log, woj, miesiecy, z_bk=True, zakresy=None, od_nowa=False):
    """Ogłoszenia o wyniku z BZP dla województwa (dzień po dniu, z pamięcią), przypisanie zamawiających do powiatów i Excel z rankingiem."""
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    kod = WOJEWODZTWA.get(woj)
    if not kod:
        raise ValueError("Wybierz województwo.")
    os.makedirs(KAT_WYNIKI_DNI, exist_ok=True)
    do = dt.date.today() - dt.timedelta(days=1)
    od = do - dt.timedelta(days=int(30.4 * miesiecy))
    dni = [od + dt.timedelta(days=i) for i in range((do - od).days + 1)]
    wyniki, braki = [], []
    for i, d in enumerate(dni, 1):
        plik = os.path.join(KAT_WYNIKI_DNI, f"{kod}_{d.isoformat()}_v3.json")  # v3: NIP i siedziba zwycięzcy, bez powtórzeń i luk
        if os.path.exists(plik) and not od_nowa and d < dt.date.today() - dt.timedelta(days=3):
            dz = czytaj(plik, [], pamiec=False)
        else:
            dz, kompletne = HZ.pobierz_wyniki_dnia(d, kod)
            time.sleep(0.1)
            if kompletne:
                pisz(plik, dz)
            else:
                braki.append(d.isoformat())
        wyniki += dz
        log(f"Pobieranie wyników z BZP: dzień {i}/{len(dni)} ({d.isoformat()}), rozstrzygnięć: {len(wyniki)}")  # co dzień – szybkie przerwanie
    for w in wyniki:
        w.setdefault("zrodlo", "BZP")
    if braki:
        log(f"Uwaga: BZP nie odpowiedział dla {len(braki)} dni – te dni zostaną pobrane ponownie przy następnym raporcie.")
    if z_bk:
        if od_nowa:  # od podstaw: indeks ogłoszeń BK województwa budowany ponownie
            try:
                os.remove(os.path.join(DATA, f"bk_indeks_{DOT.bezpieczna(woj)}.json"))
            except OSError:
                pass
        try:
            wyniki += wyniki_bk_wojewodztwa(log, woj, od)
        except Exception as e:
            log(f"Baza Konkurencyjności niedostępna: {opis_bledu_zadania(e, 'szukaj')}")
    if not wyniki:
        raise ValueError("Nie znaleziono ogłoszeń o wyniku dla tego województwa i okresu – spróbuj ponownie później.")
    zakresy = [z_ for z_ in (zakresy or []) if z_ in HZ.RODZAJE_ZAMOWIENIA] or list(HZ.RODZAJE_ZAMOWIENIA)
    przed_ = len(wyniki)
    wyniki = HZ.bez_duplikatow(wyniki)
    if przed_ != len(wyniki):
        log(f"Usunięto powtórzone rozstrzygnięcia: {przed_ - len(wyniki)}.")
    for w in wyniki:
        w["rodzaj"] = HZ.rodzaj_zamawiajacego(w.get("zamawiajacy"))
        w["rodzaj_zam"] = HZ.rodzaj_zamowienia(w.get("typ_zam", ""), w.get("cpv", ""), w.get("przedmiot", ""), w.get("kategoria", ""))
    if len(zakresy) < len(HZ.RODZAJE_ZAMOWIENIA):  # wybrany zakres zamówień (rozstrzygnięcia bez ustalonego rodzaju są pomijane)
        przed = len(wyniki)
        wyniki = [w for w in wyniki if w["rodzaj_zam"] in zakresy]
        log(f"Zakres zamówień: {', '.join(HZ.RODZAJE_ZAMOWIENIA[z_] for z_ in zakresy)} – {len(wyniki)} z {przed} rozstrzygnięć.")
        if not wyniki:
            raise ValueError("W wybranym zakresie zamówień nie ma rozstrzygnięć – zmień zakres albo okres.")
    pam = czytaj(F_POWIATY_MIAST, {}) or {}
    miasta = sorted({w.get("miasto") for w in wyniki if w.get("miasto")})
    nowe = [m_ for m_ in miasta if f"{woj}|{m_}" not in pam]
    for i, m_ in enumerate(nowe, 1):
        powiat_miejscowosci(m_, woj, pam)
        if i % 10 == 0 or i == len(nowe):
            pisz(F_POWIATY_MIAST, pam)
            log(f"Przypisywanie miejscowości do powiatów: {i}/{len(nowe)}")
    mapa = {m_: pam.get(f"{woj}|{m_}", "") for m_ in miasta}
    norm_pw = lambda p: re.sub(r"^(powiat|miasto na prawach powiatu|m\.?)\s+", "", (p or "").strip(), flags=re.I)
    for w in wyniki:  # Baza Konkurencyjności podaje powiat miejsca realizacji – ma pierwszeństwo przed ustaleniem po miejscowości
        w["powiat"] = norm_pw(w.get("powiat_bk")) or mapa.get(w.get("miasto") or "", "") or "nieustalony"
    R = HZ.ranking_powiatow([dict(w, miasto="#" + w["powiat"]) for w in wyniki], {"#" + w["powiat"]: w["powiat"] for w in wyniki})
    NIEPUB = ("Wspólnota mieszkaniowa", "Spółdzielnia mieszkaniowa", "Inna spółdzielnia", "Organizacja (fundacja, stowarzyszenie, parafia)", "Firma prywatna", "Inny")
    R_np = HZ.ranking_powiatow([dict(w, miasto="#" + w["powiat"]) for w in wyniki if w["rodzaj"] in NIEPUB], {"#" + w["powiat"]: w["powiat"] for w in wyniki})
    log("Tworzę plik Excel…")
    wb = openpyxl.Workbook()
    NAG = PatternFill("solid", fgColor="071F49")
    BIAL = Font(bold=True, color="FFFFFF")
    PAS = PatternFill("solid", fgColor="F0F5FB")

    def naglowek(ws, kol, szer):
        ws.append(kol)
        for c_ in ws[ws.max_row]:
            c_.fill, c_.font = NAG, BIAL
            c_.alignment = Alignment(wrap_text=True, vertical="center")
        for i_, w_ in enumerate(szer, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i_)].width = w_
        ws.freeze_panes = f"A{ws.max_row + 1}"

    ws = wb.active
    ws.title = "Podsumowanie powiatów"
    ws.append([f"Zwycięzcy przetargów – województwo {woj}, rozstrzygnięcia {od:%d.%m.%Y} – {do:%d.%m.%Y} ({'BZP i Baza Konkurencyjności' if z_bk else 'BZP'}); "
               f"zakres: {', '.join(HZ.RODZAJE_ZAMOWIENIA[z_] for z_ in zakresy)}"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Źródła: Biuletyn Zamówień Publicznych (zamawiający publiczni) i Baza Konkurencyjności (m.in. wspólnoty, spółdzielnie, firmy, organizacje – projekty z funduszy UE). "
               "Powiat: dla BK – miejsce realizacji, dla BZP – miejscowość siedziby zamawiającego."])
    mies_ = {}
    for w in wyniki:
        mies_[str(w.get("data") or "")[:7]] = mies_.get(str(w.get("data") or "")[:7], 0) + 1
    puste = []
    m_ = dt.date(od.year, od.month, 1)
    while m_ <= do:
        if not mies_.get(m_.strftime("%Y-%m")):
            puste.append(m_.strftime("%m.%Y"))
        m_ = (m_ + dt.timedelta(days=32)).replace(day=1)
    ws.append([("Kompletność: " + (f"brak rozstrzygnięć w miesiącach {', '.join(puste)} – BZP mógł nie odpowiedzieć; wygeneruj raport ponownie." if puste else "dane z każdego miesiąca okresu."))
               + (f" Dni do ponownego pobrania: {len(braki)}." if braki else "") + f" Rozstrzygnięć z Bazy Konkurencyjności: {sum(1 for w in wyniki if w.get('zrodlo') != 'BZP')}."])
    naglowek(ws, ["Powiat", "Rozstrzygnięte przetargi", "w tym BZP", "w tym Baza Konkurencyjności", "w tym wspólnoty i spółdzielnie", "Liczba różnych zwycięzców",
                  "Łączna wartość umów [zł]", "Najczęściej wygrywa", "Jego wygrane"], [26, 14, 10, 14, 14, 14, 18, 46, 10])
    for pw in sorted(R, key=lambda x: (x == "nieustalony", x.lower())):
        L = R[pw]
        Wp = [w for w in wyniki if w["powiat"] == pw and w.get("wykonawca")]
        ws.append([pw, sum(z["wygrane"] for z in L), sum(1 for w in Wp if w["zrodlo"] == "BZP"), sum(1 for w in Wp if w["zrodlo"] != "BZP"),
                   sum(1 for w in Wp if w["rodzaj"] in ("Wspólnota mieszkaniowa", "Spółdzielnia mieszkaniowa", "Inna spółdzielnia")),
                   len(L), round(sum(z["wartosc"] for z in L), 2), L[0]["wykonawca"] if L else "", L[0]["wygrane"] if L else 0])
        ws.cell(ws.max_row, 7).number_format = "#,##0.00"
    ws2 = wb.create_sheet("Zwycięzcy wg powiatów")
    naglowek(ws2, ["Powiat", "Miejsce", "Wykonawca", "NIP", "Siedziba wykonawcy", "Wygrane", "Łączna wartość [zł]", "Śr. liczba ofert", "Ostatnia wygrana",
                   "U jakich zamawiających (liczba wygranych)"], [24, 8, 46, 14, 22, 9, 16, 10, 14, 70])
    for pw in sorted(R, key=lambda x: (x == "nieustalony", x.lower())):
        for i_, z in enumerate(R[pw], 1):
            ws2.append([pw, i_, z["wykonawca"], z["nip"], z.get("siedziba", ""), z["wygrane"], round(z["wartosc"], 2), round(sum(z["ofert"]) / len(z["ofert"]), 1) if z["ofert"] else None,
                        z["ostatnio"], "; ".join(f"{k} ({v})" for k, v in sorted(z["zamawiajacy"].items(), key=lambda kv: -kv[1]))])
            ws2.cell(ws2.max_row, 7).number_format = "#,##0.00"
            if i_ <= 3:
                for c_ in ws2[ws2.max_row]:
                    c_.fill = PAS
    ws2.auto_filter.ref = ws2.dimensions
    wsn = wb.create_sheet("Zwycięzcy – niepubliczni")
    wsn.append(["Ranking wykonawców w zamówieniach wspólnot, spółdzielni, firm i organizacji (głównie Baza Konkurencyjności)"])
    wsn["A1"].font = Font(bold=True, size=12)
    naglowek(wsn, ["Powiat", "Miejsce", "Wykonawca", "NIP", "Siedziba wykonawcy", "Wygrane", "Łączna wartość [zł]", "Śr. liczba ofert", "Ostatnia wygrana",
                   "U jakich zamawiających (liczba wygranych)"], [24, 8, 46, 14, 22, 9, 16, 10, 14, 70])
    for pw in sorted(R_np, key=lambda x: (x == "nieustalony", x.lower())):
        for i_, z in enumerate(R_np[pw], 1):
            wsn.append([pw, i_, z["wykonawca"], z["nip"], z.get("siedziba", ""), z["wygrane"], round(z["wartosc"], 2), round(sum(z["ofert"]) / len(z["ofert"]), 1) if z["ofert"] else None,
                        z["ostatnio"], "; ".join(f"{k} ({v})" for k, v in sorted(z["zamawiajacy"].items(), key=lambda kv: -kv[1]))])
            wsn.cell(wsn.max_row, 7).number_format = "#,##0.00"
            if i_ <= 3:
                for c_ in wsn[wsn.max_row]:
                    c_.fill = PAS
    if not R_np:
        wsn.append(["Brak rozstrzygnięć zamawiających niepublicznych w wybranym okresie."])
    wsz = wb.create_sheet("Zwycięzcy – zestawienie", 1)  # każdy zwycięzca raz (po NIP, a bez NIP – po nazwie)
    Z = HZ.zestawienie_zwyciezcow(wyniki)
    wsz.append([f"Każdy zwycięzca raz – łączenie po NIP, a gdy NIP brak, po nazwie (bez formy prawnej, z drobnymi różnicami w pisowni). Zwycięzców: {len(Z)}."])
    wsz["A1"].font = Font(bold=True, size=12)
    naglowek(wsz, ["Lp.", "Wykonawca", "NIP", "Siedziba", "Wygrane przetargi", "Łączna kwota [zł]", "Liczba powiatów", "Powiaty (liczba wygranych)",
                   "Liczba zamawiających", "Ostatnia wygrana", "Źródło", "Inne warianty nazwy"], [6, 46, 14, 22, 10, 18, 10, 46, 12, 14, 18, 50])
    for i_, z in enumerate(Z, 1):
        wsz.append([i_, z["wykonawca"], z["nip"], z["siedziba"], z["wygrane"], z["wartosc"], len(z["powiaty"]),
                    "; ".join(f"{k} ({v})" for k, v in z["powiaty"].items()), z["zamawiajacych"], z["ostatnio"], z["zrodla"], "; ".join(z["warianty"][:5])])
        wsz.cell(wsz.max_row, 6).number_format = "#,##0.00"
        if i_ <= 10:
            for c_ in wsz[wsz.max_row]:
                c_.fill = PAS
    wsz.auto_filter.ref = f"A2:L{wsz.max_row}"
    wsr = wb.create_sheet("Zamawiający wg rodzaju")
    naglowek(wsr, ["Powiat"] + HZ.RODZAJE_ZAM, [24] + [16] * len(HZ.RODZAJE_ZAM))
    for pw in sorted(R, key=lambda x: (x == "nieustalony", x.lower())):
        wsr.append([pw] + [sum(1 for w in wyniki if w["powiat"] == pw and w.get("wykonawca") and w["rodzaj"] == r_) for r_ in HZ.RODZAJE_ZAM])
    ws3 = wb.create_sheet("Wszystkie rozstrzygnięcia")
    naglowek(ws3, ["Data", "Źródło", "Powiat", "Zamawiający", "Rodzaj zamawiającego", "Rodzaj zamówienia", "Miejscowość", "Przedmiot", "Liczba ofert",
                   "Cena wybranej oferty [zł]", "Najniższa [zł]", "Najwyższa [zł]", "Wykonawca", "NIP", "Siedziba wykonawcy", "Unieważnione", "Nr ogłoszenia"],
             [11, 12, 20, 36, 22, 16, 16, 60, 9, 16, 14, 14, 40, 14, 22, 10, 20])
    for w in sorted(wyniki, key=lambda x: x.get("data", "")):
        ws3.append([w.get("data"), w.get("zrodlo", "BZP"), w["powiat"], w.get("zamawiajacy"), w["rodzaj"], HZ.RODZAJE_ZAMOWIENIA.get(w["rodzaj_zam"], "nieustalony"),
                    w.get("miasto"), w.get("przedmiot"), w.get("ofert"), w.get("cena"), w.get("najnizsza"), w.get("najwyzsza"), w.get("wykonawca"), w.get("nip"),
                    w.get("siedziba", ""), "tak" if w.get("uniewaznione") else "", w.get("numer")])
        for k_ in (10, 11, 12):
            ws3.cell(ws3.max_row, k_).number_format = "#,##0.00"
    ws3.auto_filter.ref = ws3.dimensions
    kat = os.path.join(DATA, "raporty", konto_biezace() or "env")
    os.makedirs(kat, exist_ok=True)
    nazwa = (f"Zwyciezcy_przetargow_{DOT.bezpieczna(woj)}_powiaty" + ("" if len(zakresy) == 3 else "_" + "_".join(zakresy))
             + f"_{dt.date.today():%Y-%m-%d}.xlsx")
    wb.save(os.path.join(kat, nazwa))
    log(f"Gotowe: {len(wyniki)} rozstrzygnięć, {len(R)} powiatów.")
    return {"plik": nazwa, "url": "/api/raporty/plik/" + urllib.parse.quote(nazwa)}


F_WZNOW = os.path.join(DATA, "zadania_do_wznowienia.json")  # długie raporty – wznawiane po ponownym uruchomieniu serwera


def praca_raport_wznawialny(log, woj, miesiecy, z_bk, zakresy, od_nowa):
    """Raport powiatów z zapisem „do wznowienia”: jeśli serwer zostanie zrestartowany w trakcie, raport ruszy sam po starcie
    i dokończy pracę od miejsca, w którym przerwał (pobrane dni i sprawdzone ogłoszenia są zapamiętane)."""
    klucz = f"{konto_biezace()}|{woj}"
    with BLOKADA:
        W = czytaj(F_WZNOW, {}) or {}
        W[klucz] = {"konto": konto_biezace(), "woj": woj, "miesiecy": miesiecy, "z_bk": z_bk, "zakresy": zakresy, "od": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "proby": (W.get(klucz) or {}).get("proby", 0)}
        pisz(F_WZNOW, W)
    try:
        return praca_raport_powiatow(log, woj, miesiecy, z_bk, zakresy, od_nowa)
    finally:  # zakończenie (także błąd albo przerwanie przez użytkownika) – nie wznawiać
        with BLOKADA:
            W = czytaj(F_WZNOW, {}) or {}
            W.pop(klucz, None)
            pisz(F_WZNOW, W)


def wznow_zadania_po_starcie():
    """Wznawia przerwane raporty dopiero 3 minuty po starcie (serwer zdąży odpowiadać) i najwyżej 2 razy z rzędu –
    gdyby raport sam powodował restarty, program nie wpadnie w pętlę."""
    time.sleep(int(os.environ.get("WZNOW_PO_SEKUNDACH", "180")))
    if os.environ.get("BEZ_WZNAWIANIA") == "1":
        return
    with BLOKADA:
        W = czytaj(F_WZNOW, {}) or {}
        for k, x in list(W.items()):
            x["proby"] = int(x.get("proby", 0)) + 1
            if x["proby"] > 2:
                W.pop(k)
                print("Raport nie zostanie wznowiony automatycznie (2 próby):", k, flush=True)
        pisz(F_WZNOW, W)
    for k, x in list(W.items()):
        _KONTEKST.login = x.get("konto")
        try:
            uruchom("raport_powiaty", f"Raport zwycięzców – {x['woj']}", praca_raport_wznawialny, x["woj"], x["miesiecy"], x["z_bk"], x["zakresy"], False)
            print("Wznowiono raport:", k, flush=True)
        except Exception as e:
            print("Wznowienie raportu nie powiodło się:", k, e, flush=True)
        finally:
            _KONTEKST.login = None


def podtrzymuj_serwer():
    """Hosting w darmowym planie usypia serwer po kilkunastu minutach bez ruchu – co 4 minuty, gdy trwa zadanie, program odwiedza sam siebie."""
    adres = (os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("ADRES_PROGRAMU") or "").rstrip("/")
    if not adres:
        return
    while True:
        time.sleep(240)
        if any(z_["status"] == "trwa" for z_ in list(ZADANIA.values())):
            try:
                urllib.request.urlopen(adres + "/zdrowie", timeout=20).read(200)
            except Exception:
                pass










# ---------- historia zamawiającego: ceny w podobnych przetargach, liczba ofert, zwycięzcy (BZP – ogłoszenia o wyniku)

KAT_HISTORIA = os.path.join(DATA, "historia_zamawiajacych")


def _nip_z_surowych(t):
    try:
        r = json.loads(t.get("_surowe") or "{}")
        return str(r.get("organizationNationalId") or r.get("buyerNationalId") or "")
    except ValueError:
        return ""


def praca_historia_zamawiajacego(log, zam, przedmiot, cpv, nip, pid=None, numer=None, wymus=False):
    """Pobiera z BZP wyniki postępowań zamawiającego (pamięć 7 dni na zamawiającego) i liczy statystyki dla tego przetargu."""
    os.makedirs(KAT_HISTORIA, exist_ok=True)
    plik = os.path.join(KAT_HISTORIA, hashlib.sha1((re.sub(r"\D", "", nip) or HZ._norm(zam)).encode()).hexdigest()[:16] + ".json")
    pam = czytaj(plik, None)
    if pam and not wymus and (dt.datetime.now() - dt.datetime.strptime(pam["data"], "%Y-%m-%d %H:%M")).days < 7:
        wyniki = pam["wyniki"]
        log(f"Historia zamawiającego z pamięci programu ({pam['data']}) – bez ponownego pobierania z BZP.")
    else:
        log(f"Pobieram z BZP ogłoszenia o wyniku postępowań: {zam[:80]} (ostatnie 24 miesiące)…")
        wyniki = HZ.pobierz_wyniki(zam, log, 24, nip)
        for w in wyniki:
            w.setdefault("zrodlo", "BZP")
        try:
            wyniki += bk_wyniki_zamawiajacego(zam, log)
        except Exception as e:
            log(f"Baza Konkurencyjności niedostępna: {opis_bledu_zadania(e, 'szukaj')}")
        pisz(plik, {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "zamawiajacy": zam, "wyniki": wyniki})
    st = HZ.statystyki([dict(w) for w in wyniki], przedmiot, cpv)
    wynik = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "zamawiajacy": zam, "przedmiot": przedmiot, **st}
    if pid:
        with BLOKADA:
            m = meta(pid)
            m["historia_zam"] = wynik
            zapisz_meta(pid, m)
    if numer:
        H_ = czytaj(F_HIST_PRZ, {}) or {}
        H_[numer] = wynik
        pisz(F_HIST_PRZ, dict(list(H_.items())[-200:]))
    log(f"Gotowe: rozstrzygnięć {st['wszystkie']['liczba']}, podobnych przetargów {st['podobne']['liczba']}.")
    return {"ok": True}


F_HIST_PRZ = SciezkaKonta("historia_zamawiajacych_przetargi.json")


@app.post("/api/projekty/<pid>/historia-zamawiajacego")
@wymaga_logowania
def historia_zamawiajacego_projekt(pid):
    m = meta(pid)
    t = dane_przetargu(m, pid) if m.get("przetarg") else {}
    zam = (request.json or {}).get("zamawiajacy") or t.get("zamawiajacy") or (m.get("przetarg") or {}).get("zamawiajacy")
    if not zam:
        return jsonify({"blad": "Brak nazwy zamawiającego – projekt nie pochodzi z przetargu."}), 400
    surowy = db_przetargi().get(m.get("przetarg_numer") or (m.get("przetarg") or {}).get("numer") or "") or {}
    return jsonify(uruchom("historia", "Historia zamawiającego (BZP)", praca_historia_zamawiajacego, zam, t.get("przedmiot") or m.get("nazwa", ""),
                           surowy.get("cpv") or "", _nip_z_surowych(surowy), pid, None, bool((request.json or {}).get("wymus"))))






@app.get("/api/projekty/<pid>")
@wymaga_logowania
def projekt(pid):
    m = meta(pid)
    if m.get("przetarg"):
        m["przetarg_dane"] = dane_przetargu(m, pid)
        m["przetarg"] = dict(m["przetarg"], termin_ofert=m["przetarg_dane"]["termin_ofert"] or m["przetarg"].get("termin_ofert"),
                             link=m["przetarg_dane"]["link"] or m["przetarg"].get("link"))
    m["wlasciciel"] = m.get("wlasciciel") or login_admina()
    m["dostep"] = m.get("dostep") or []
    if m.get("oferta"):  # cena z kosztorysu przed ręczną korektą – podstawa kalkulatora szans
        orig = czytaj(os.path.join(pdir(pid), "oferta_dane_oryginal.json"), None)
        if orig:
            try:
                m["oferta"] = dict(m["oferta"], brutto_rynkowe=MO.przelicz(orig).get("brutto"))
            except Exception:
                pass
    m["wynik_oferty"] = (czytaj(F_WYNIKI_OFERT, {}) or {}).get(pid)
    m["pliki"] = lista_plikow(pid)
    m["wyniki"] = wyniki(pid)
    m["pliki_wykonawcy"] = pliki_wykonawcy(pid)
    m["notatki"] = [x for x in m.get("notatki", []) if not x.get("archiwum")]
    m["bledy_dokumentacji"] = bledy_dokumentacji(pid, m)
    m["umowa_dane"] = dane_umowy_projektu(pid, m)
    m["rozbieznosci_dane"] = rozbieznosci_projektu(pid, m)
    if (m.get("typ") or "przetarg") == "przetarg" and m.get("przetarg") and not m.get("status_projektu"):
        try:
            m["termin_pytan"] = termin_pytan_projektu(pid, m)
        except Exception:
            m["termin_pytan"] = None
    if m.get("status_projektu") in ("realizacja", "zakonczony"):
        try:
            r_ = realizacja_dane(pid)
            s_ = podsumowanie_realizacji(pid)
            hrf_ = r_.get("hrf") or {"etapy": []}
            m["realizacja_skrot"] = {"termin": r_.get("termin_zakonczenia"), "umowa_nr": r_.get("umowa_nr"), **s_,
                                     "etapy": len(hrf_["etapy"]), "odebrane": sum(1 for e in hrf_["etapy"] if e.get("status") == "odebrany"),
                                     "usterki_otwarte": sum(1 for u in r_.get("usterki", []) if u.get("status") in ("otwarta", "w toku"))}
        except Exception:
            pass
    if m.get("kontrola"):  # aktualne dane pozycji w alertach (po poprawkach i korektach ceny)
        dane_k = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), None)
        if dane_k:
            poz_k = {p["lp"]: p for p in KON.pozycje(dane_k)}
            for a in m["kontrola"].get("alerty", []):
                p = poz_k.get(a.get("lp"))
                if p:
                    a["pozycja"] = {k: p.get(k) for k in ("opis", "jm", "ilosc", "cena", "wartosc", "dzial")}
    if (m.get("typ") or "przetarg") == "wlasny":
        dane_of = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), None)
        m["umowa_formularz"] = {**UM.domyslne(dane_of, m, cfg()), **(m.get("umowa") or {}).get("pola", {})}
        if dane_of and not (m.get("umowa") or {}).get("pola_reczne_netto"):
            m["umowa_formularz"]["netto"] = dane_of.get("netto", 0)
            m["umowa_formularz"]["vat"] = "" if dane_of.get("vat_nieustalony") else dane_of.get("vat", "")
    try:
        m["wymagane_dokumenty"] = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}).get("zalaczniki_do_oferty", [])
    except Exception:
        m["wymagane_dokumenty"] = []
    m["dostep"] = UWIERZ.filtr_dostepu(m["dostep"])  # lista osób, którym udostępniono projekt – użytkownicy jej nie widzą (H1-01)
    m = ukryj_innych(m)
    hj = m.get("harmonogram_json")
    if hj and os.path.isfile(os.path.join(pdir(pid), hj)):
        h = MH.wczytaj_harmonogram(os.path.join(pdir(pid), hj))
        m["etapy"] = [{"nr": e["nr"], "nazwa": e.get("nazwa", ""), "od": e["od"].isoformat(), "do": e["do"].isoformat(),
                       "obsada": e.get("obsada", ""),
                       "materialow": sum(1 for x in h["materialy"] if x["ilosci"][k] > 0),
                       "wartosc": round(sum(x["ilosci"][k] * x["cena"] for x in h["materialy"]), 2)}
                      for k, e in enumerate(h["etapy"])]
        m["adres_dostaw"] = h.get("adres", "")
    if m.get("typ") in INWESTORSKIE:
        try:
            m["dokumentacja_domyslne"] = dokumentacja_domyslne(pid, m)
        except Exception:
            m["dokumentacja_domyslne"] = {"pola": {}, "zrodla": {}}
    if (m.get("strona") or strona_typu(m.get("typ"))) == "zamawiajacy" and not projekt_wspolnoty(m):  # weryfikacja dokumentacji: lista kontrolna według trybu
        import trasy_projekty_wykonawcy as _TW
        m["weryfikacja_tryb"], m["tryby_weryfikacji"] = _TW.tryb_weryfikacji(m), LK.TRYBY
    return jsonify(m)


@app.post("/api/projekty/<pid>/typ")
@wymaga_logowania
def projekt_typ(pid):
    typ = request.json.get("typ")
    if typ not in TYPY_PROJEKTOW:
        return jsonify({"blad": "Nieznany typ projektu"}), 400
    m = meta(pid)
    m["typ"] = typ
    zapisz_meta(pid, m)
    dane = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), None)
    if dane:  # dotwórz formularze i analizę dla projektu, który był samym kosztorysem
        zapisz_oferte(pid, MO.przelicz(dane), cfg(), (m.get("oferta") or {}).get("korekta"))
    return jsonify({"ok": True})


@app.post("/api/projekty/<pid>/kopiuj")
@wymaga_logowania
def projekt_kopiuj(pid):
    """Kosztorysowanie: kopia kosztorysu do innego modułu – projekt własny (wykonawca), projekt zamówienia (zamawiający)
    albo budowa domu (inwestor indywidualny). Kosztorys zostaje też w Kosztorysowaniu."""
    j = request.json or {}
    typ = j.get("typ")
    if typ not in ("wlasny", "przetarg", "zamowienie", "dom", "kosztorys"):
        return jsonify({"blad": "Wybierz moduł docelowy."}), 400
    zr = pdir(pid)
    if not os.path.isfile(os.path.join(zr, "oferta_dane.json")):
        return jsonify({"blad": "Najpierw przygotuj kosztorys."}), 400
    nowy = uuid.uuid4().hex[:12]
    shutil.copytree(zr, os.path.join(PROJ, nowy), ignore=shutil.ignore_patterns("realizacja*", "wnioski"))
    m = meta(nowy)
    for k in ("status_projektu", "wnioski", "oferta_klienta", "oferta_przygotowana", "umowa", "umowa_dane", "umowa_formularz", "harmonogram",
              "harmonogram_json", "harmonogram_uwagi", "harmonogram_zespol", "etapy", "materialy", "lista_materialow", "komplet", "archiwum",
              "weryfikacja", "dokumentacja", "dokumentacja_pola", "kosztorys_pusty", "realizacja_skrot", "czat", "kontrola", "pliki_wykonawcy",
              "sprawdzone_wykonawcy", "dostep", "przetarg", "przetarg_numer", "przetarg_dane"):
        m.pop(k, None)
    m.update(id=nowy, typ=typ, strona=strona_typu(typ), wlasciciel=konto_biezace() if session.get("jako") else (m.get("wlasciciel") or session.get("login")),
             utworzono=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), nazwa=str(j.get("nazwa") or m.get("nazwa", ""))[:120], z_kosztorysu=pid,
             pliki_oferty=[])
    if typ == "zamowienie":
        m["rodzaj_zamowienia"] = "roboty"
    zapisz_meta(nowy, m)
    for f in os.listdir(os.path.join(PROJ, nowy)):  # stare pliki wynikowe – zostaną utworzone ponownie dla nowego modułu
        if f.lower().endswith((".xlsx", ".docx", ".eml", ".zip")):
            try:
                os.remove(os.path.join(PROJ, nowy, f))
            except OSError:
                pass
    zapisz_oferte(nowy, MO.przelicz(czytaj(os.path.join(PROJ, nowy, "oferta_dane.json"), {})), cfg())
    zapisz_aktywnosc(session.get("login"), f"Kosztorys przeniesiony do modułu ({typ})", konto=konto_biezace(), projekt=m["nazwa"])
    return jsonify({"id": nowy, "typ": typ, "strona": m["strona"]})


@app.post("/api/projekty/<pid>/nazwa")
@wymaga_logowania
def projekt_nazwa(pid):
    m = meta(pid)
    m["nazwa"] = (str(request.json.get("nazwa") or "").strip() or m["nazwa"])[:120]
    zapisz_meta(pid, m)
    return jsonify({"ok": True})


@app.delete("/api/projekty/<pid>")
@wymaga_logowania
def projekt_usun(pid):
    """Projekt nie jest usuwany – trafia do archiwum (przywrócenie w zakładce Archiwum)."""
    m = meta(pid)
    m.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), archiwum_kto=session.get("login", ""))
    zapisz_meta(pid, m)
    return jsonify({"ok": True, "archiwum": True})


def archiwizuj_plik(pid, sciezka_bezwzgledna):
    """Przenosi plik projektu do folderu _archiwum zamiast go usuwać; zapisuje, skąd pochodzi."""
    if not os.path.isfile(sciezka_bezwzgledna):
        return
    d = pdir(pid)
    kat = os.path.join(d, "_archiwum")
    os.makedirs(kat, exist_ok=True)
    fid = uuid.uuid4().hex[:10]
    cel = os.path.join(kat, f"{fid}_{os.path.basename(sciezka_bezwzgledna)}")
    shutil.move(sciezka_bezwzgledna, cel)
    m = meta(pid)
    m.setdefault("archiwum_plikow", []).append({"id": fid, "plik": os.path.relpath(cel, d).replace(os.sep, "/"),
                                                "oryginal": os.path.relpath(sciezka_bezwzgledna, d).replace(os.sep, "/"),
                                                "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "kto": session.get("login", "")})
    zapisz_meta(pid, m)




def secure_filename_pl(n):
    n = os.path.basename((n or "plik").replace("\\", "/"))
    n = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", n).strip(" .")
    return n[:150] or "plik"








def popraw_nazwy_folderu(folder, log=None):
    """Poprawia końcówki nazw wszystkich plików w folderze (format rozpoznany po zawartości); zwraca nowe ścieżki."""
    wyn = []
    for r, _, ns in os.walk(folder):
        for n in ns:
            p = os.path.join(r, n)
            q = MO.popraw_rozszerzenie(p)
            if q != p and log:
                log(f"Poprawiono nazwę pliku: {n} → {os.path.basename(q)}")
            wyn.append(q)
    return wyn


def _slowa_tytulu(t):
    return {w for w in re.findall(r"\w+", W.norm(t or "")) if len(w) >= 4 and not w.isdigit()}


def znajdz_w_pamieci_ogloszen(t, dni=90):
    """To samo postępowanie w BZP / Bazie Konkurencyjności (wspólna pamięć ogłoszeń) – dla ogłoszeń z BIP, których link prowadzi
    do strony gminy (często ogólnej listy zamówień), a dokumenty są na Platformie e-Zamówienia albo w BK.
    Warunek: wspólne słowo z nazwy zamawiającego / miejscowości i co najmniej 50% zgodności słów tytułu."""
    tyt = _slowa_tytulu(t.get("przedmiot"))
    zam = _slowa_tytulu(" ".join(str(t.get(k) or "") for k in ("zamawiajacy", "miasto")))
    if len(tyt) < 2 or not zam:
        return None, 0
    najl, wynik = None, 0.0
    for o in WSP.wszystkie(dni):
        if o.get("numer") == t.get("numer"):
            continue
        zo = _slowa_tytulu(" ".join(str(o.get(k) or "") for k in ("zamawiajacy", "miasto")))
        if not (zam & zo):
            continue
        to = _slowa_tytulu(o.get("przedmiot"))
        if not to:
            continue
        w = len(tyt & to) / len(tyt | to)
        if w > wynik:
            najl, wynik = o, w
    return (najl, round(wynik, 2)) if wynik >= 0.5 else (None, round(wynik, 2))


def praca_pobierz_dok(log, pid, wszystkie=True):
    """Pobiera WSZYSTKIE dokumenty przetargu (BZP / Platforma e-Zamówienia / platforma zamawiającego / Baza Konkurencyjności),
    rozpakowuje archiwa, poprawia nazwy plików i zaznacza wszystkie jako uwzględnione."""
    m = meta(pid)
    t = m.get("przetarg") or {}
    if not t:
        raise ValueError("Projekt nie jest powiązany z ogłoszeniem – dodaj dokumenty ręcznie.")
    folder = os.path.join(pdir(pid), "dokumenty")
    os.makedirs(folder, exist_ok=True)
    przed = {os.path.join(r, n) for r, _, ns in os.walk(folder) for n in ns}
    pliki, platformy = [], []
    nr = m.get("przetarg_numer") or t.get("numer")
    if nr and os.path.isdir(folder_przetargu(nr)):  # dokumenty pobrane wcześniej przy „Pełnej analizie”
        shutil.copytree(folder_przetargu(nr), folder, dirs_exist_ok=True)
        log("Skopiowano dokumenty pobrane przy pełnej analizie przetargu.")
    zrodlo_t = t
    tekst_t = " ".join(str(t.get(k) or "") for k in ("link", "pdf", "tresc"))
    if not t.get("bk_id") and not BZ.RE_OCDS.search(tekst_t) and "ezamowienia.gov.pl" not in tekst_t:
        # ogłoszenie z BIP – link zwykle prowadzi do strony gminy; szukamy tego samego postępowania w BZP / BK
        rown, zgod = znajdz_w_pamieci_ogloszen(t)
        if rown:
            log(f"Ogłoszenie pochodzi ze strony BIP – to samo postępowanie jest w {'Bazie Konkurencyjności' if rown.get('bk_id') else 'BZP'}: "
                f"{rown.get('numer')} „{str(rown.get('przedmiot', ''))[:90]}” (zgodność tytułu {int(zgod * 100)}%) – pobieram stamtąd.")
            zrodlo_t = rown
            m_ = meta(pid)
            m_["przetarg_powiazany"] = {"numer": rown.get("numer"), "zgodnosc": zgod, "link": rown.get("link")}
            zapisz_meta(pid, m_)
        else:
            log("Ogłoszenie pochodzi ze strony BIP – nie znaleziono tego postępowania w BZP ani w Bazie Konkurencyjności (pamięć ogłoszeń).")
            if re.match(r"(?i)https?://", str(t.get("link") or "")):  # strona BIP: szukamy na niej odnośnika do tego przetargu i pobieramy jego pliki
                strona_p, zg = BZ.znajdz_strone_postepowania(t["link"], t.get("przedmiot"))
                if strona_p:
                    log(f"Na stronie BIP znaleziono to postępowanie (zgodność tytułu {int(zg * 100)}%): {strona_p} – pobieram załączone pliki…")
                    try:
                        w_ = BZ.pobierz_z_linku(strona_p, folder, log)
                        if w_["pliki"]:
                            zrodlo_t = {"bk_id": None, "_pobrane": w_["pliki"]}
                    except ValueError as e:
                        log(f"   {e}")
    if zrodlo_t.get("_pobrane"):
        pliki = list(zrodlo_t["_pobrane"])
    elif zrodlo_t.get("bk_id"):
        pliki = MO.pobierz_zalaczniki_bk(zrodlo_t["bk_id"], folder, log)
    else:
        w = BZ.pobierz_dokumenty(zrodlo_t, folder, log)
        pliki, platformy = w["pliki"], w["platformy"]
    pliki = [MO.popraw_rozszerzenie(p) if os.path.isfile(p) else p for p in pliki]
    for p in pliki:
        if MO.czy_archiwum(p):
            try:
                MO.rozpakuj_zip(p, os.path.splitext(p)[0])
                os.remove(p)
            except Exception as e:
                log(f"Nie udało się rozpakować {os.path.basename(p)}: {e}")
    popraw_nazwy_folderu(folder, log)
    po = {os.path.join(r, n) for r, _, ns in os.walk(folder) for n in ns}
    nowe = len(po - przed)
    if not pliki and nowe:
        pliki = sorted(po - przed)
    tylko_ogloszenie = len(pliki) <= 1 and not t.get("bk_id")
    if not tylko_ogloszenie:
        platformy = []
    m = meta(pid)
    m["platformy_zakupowe"] = platformy
    if wszystkie:
        m["pominiete"] = []  # jednym kliknięciem: wszystkie dokumenty uwzględnione…
    zapisz_meta(pid, m)
    oznacz_przebieg(pid, sorted(os.path.relpath(p_, folder) for p_ in (po - przed)), log)  # …poza dokumentami przebiegu postępowania
    if po - przed:
        dokumenty_zmienione(pid, "Pobrano dokumenty")
    _lp = lista_plikow(pid)
    _pom = [x["sciezka"] for x in _lp if not x["uwzglednij"]]
    log(f"W projekcie jest {len(_lp)} plików dokumentacji (nowych: {nowe}); uwzględnione: {len(_lp) - len(_pom)}"
        + (f", pominięte: {len(_pom)} ({', '.join(_pom[:5])}{'…' if len(_pom) > 5 else ''})." if _pom else "."))
    if platformy:
        log("Dokumenty zamówienia są na platformie zamawiającego – pobierz je ręcznie: " + ", ".join(platformy))
    if not pliki:
        ogolna = re.search(r"(?i)redir,przetargi|zamowienia-publiczne|/przetargi/?$|/zamowienia/?$", str(t.get("link") or ""))
        raise ValueError("Nie udało się pobrać dokumentów automatycznie – "
                         + ("link z ogłoszenia prowadzi do OGÓLNEJ listy zamówień na stronie BIP zamawiającego (nie do tego postępowania) i nie znaleziono "
                            "tego przetargu w BZP ani Bazie Konkurencyjności. " if ogolna else "")
                         + "Otwórz ogłoszenie" + (f" / platformę ({platformy[0]})" if platformy else f" ({t.get('link', '')})")
                         + ", pobierz SWZ i przedmiar i dodaj je w kroku 1 – albo wklej link do strony tego postępowania.")
    if tylko_ogloszenie:
        log("Pobrano tylko ogłoszenie – SWZ i przedmiar dodaj ręcznie z platformy zamawiającego; bez przedmiaru kosztorys będzie orientacyjny.")
    return {"pobrane": len(pliki), "platformy": platformy}


praca_pobierz_bk = praca_pobierz_dok


@app.post("/api/projekty/<pid>/pobierz-dokumenty")
@wymaga_logowania
def pobierz_dokumenty(pid):
    return jsonify(uruchom("pobieranie", "Pobieranie dokumentów przetargu", praca_pobierz_dok, pid))


@app.post("/api/projekty/<pid>/pobierz-bk")
@wymaga_logowania
def pobierz_bk(pid):
    return jsonify(uruchom("pobieranie", "Pobieranie załączników", praca_pobierz_bk, pid))


# ---------- oferta

def praca_oferta(log, pid, wskazowki):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    c["vat_wybor"] = meta(pid).get("vat_wybor", "auto")
    d = pdir(pid)
    m = meta(pid)
    if m.get("typ") in INWESTORSKIE or m.get("typ") == "dom":  # zamawiający / inwestor: profil to ZAMAWIAJĄCY, wykonawca nieznany
        c["_rola_inwestorska"] = True
        c["_zamawiajacy"] = (m.get("kreator") or {}).get("zamawiajacy") or ""
        with BLOKADA:  # opis / wskazówki zamawiającego – źródło ilości dla kontroli kosztorysu
            m_ = meta(pid)
            m_["wskazowki_oferty"] = (wskazowki or "")[:6000]
            zapisz_meta(pid, m_)
        K_ = m.get("kreator") or {}
        c["_region_realizacji"] = (K_.get("potrzeba") or {}).get("miejsce") or (K_.get("potrzeba") or {}).get("obiekt") or K_.get("miejsce") or c.get("firma_adres", "")
        c["_prywatny"] = projekt_wspolnoty(m)  # wspólnota, spółdzielnia, deweloper: bez Pzp – inne polecenie i tytuły kosztorysu
    pryw = bool(c.get("_prywatny"))
    cennik_ = (czytaj(F_CENNIK_W, {}) or {}).get("pozycje") or [] if m.get("ceny_zrodlo") == "cennik" else []
    if m.get("ceny_zrodlo") == "cennik":
        if cennik_:
            log(f"Wycena według własnego cennika ({len(cennik_)} pozycji); pozycje spoza cennika – ceny rynkowe.")
            wskazowki = (wskazowki or "") + CW.do_polecenia(cennik_)
        else:
            log("Wybrano własny cennik, ale cennik jest pusty – wycena cenami rynkowymi.")
    wybrane = [os.path.join(d, "dokumenty", p["sciezka"]) for p in lista_plikow(pid) if p["uwzglednij"]]
    if not wybrane and m.get("przetarg"):
        log("Brak dokumentów w projekcie – próbuję pobrać je z ogłoszenia…")
        try:
            praca_pobierz_dok(log, pid)
        except ValueError as e:
            log(str(e))
        wybrane = [os.path.join(d, "dokumenty", p["sciezka"]) for p in lista_plikow(pid) if p["uwzglednij"]]
    if m.get("typ") in INWESTORSKIE:  # kreator zamówienia: wzory zamawiającego (SWZ, OPZ…) zawierają zakres i ilości – też do kosztorysu
        wz = os.path.join(d, "wzory")
        if os.path.isdir(wz):
            pl = sorted(os.listdir(wz))
            z_pdf = {f[:-len(" (z PDF).docx")] for f in pl if f.endswith(" (z PDF).docx")}
            dod = [os.path.join(wz, f) for f in pl if not (f.lower().endswith(".pdf") and os.path.splitext(f)[0] in z_pdf)]
            if dod:
                log(f"Do kosztorysu dołączam wzory dokumentów zamawiającego ({len(dod)}): zakres i ilości.")
                wybrane += dod
    if not wybrane and not (tylko_kosztorys_typ(m) and (wskazowki or "").strip()):
        raise ValueError("Dodaj dokumenty (przedmiar, projekt, opis, umowa, zdjęcia)"
                         + (" albo opisz zakres prac z wymiarami." if tylko_kosztorys_typ(m) else "."))
    content, suma = [], 0
    for p in wybrane:
        bloki, b, o = MO.przygotuj_blok(p)
        if o:
            log(o)
        content += bloki
        suma += b
    if suma > MO.MAX_BAJTOW_ZAPYTANIA:
        raise ValueError(f"Za dużo danych ({suma / 1024 / 1024:.0f} MB > 50 MB). Wyłącz rysunki i duże załączniki.")
    typ = m.get("typ") or "przetarg"
    if typ == "dom":
        wskazowki = ("KOSZTORYS BUDOWY DOMU JEDNORODZINNEGO dla INWESTORA INDYWIDUALNEGO (na podstawie projektu domu). "
                     "Działy wg etapów budowy: 1. Roboty przygotowawcze i ziemne; 2. Fundamenty i izolacje (stan zero); "
                     "3. Ściany, stropy, schody, kominy (stan surowy otwarty); 4. Dach (więźba, pokrycie, obróbki, rynny); "
                     "5. Stolarka okienna i drzwi zewnętrzne, brama garażowa (stan surowy zamknięty); 6. Instalacje (wod-kan, CO/pompa ciepła, "
                     "elektryka, wentylacja); 7. Tynki, wylewki, ocieplenie i elewacja; 8. Wykończenie (stan deweloperski); "
                     "9. Przyłącza, ogrodzenie i zagospodarowanie terenu – pomiń działy, których nie da się ustalić z dokumentów. "
                     "Ilości z projektu (zestawienia powierzchni, rzuty, przekroje, opis techniczny); brakujące wymiary przyjmij jawnie "
                     "i dopisz do \"do_weryfikacji\". Ceny rynkowe w regionie budowy: materiał + robocizna (wykonawca); w uwagach "
                     "przy pozycji podaj udział materiału, gdy jest istotny (inwestor może budować systemem gospodarczym). "
                     "W \"pytania_do_zamawiajacego\" wpisz decyzje, które inwestor powinien podjąć (np. rodzaj ogrzewania, standard). "
                     + ("" if not m.get("kosztorys_wlasny") else
                        "UWAGA: w dokumentach jest GOTOWY KOSZTORYS INWESTORA – przepisz WSZYSTKIE jego pozycje, ilości i ceny DOKŁADNIE, "
                        "bez własnej wyceny; tylko pogrupuj je w działy etapów budowy, jeśli nie są pogrupowane. ")
                     + (wskazowki or ""))
        content.append({"type": "text", "text": polecenie_kosztorysu(c, wskazowki)})
        system = SYSTEM_KOSZTORYS_INW if c.get("_rola_inwestorska") else SYSTEM_KOSZTORYS
    elif typ in INWESTORSKIE and m.get("rodzaj_zamowienia") in ("uslugi", "dostawy"):
        if m["rodzaj_zamowienia"] == "uslugi":
            wskazowki = (("SZACOWANIE KOSZTU USŁUG dla INWESTORA PRYWATNEGO (wspólnota mieszkaniowa, spółdzielnia, deweloper) – budżet przed "
                          "zebraniem ofert od wykonawców. Zamawiający NIE stosuje ustawy Pzp – nie powołuj jej przepisów. " if pryw else
                          "SZACOWANIE WARTOŚCI ZAMÓWIENIA NA USŁUGI dla ZAMAWIAJĄCEGO (przed przetargiem). ") + "Działy = rodzaje usług lub obiekty/lokalizacje. "
                         "Pozycje: usługa (np. sprzątanie pomieszczeń biurowych 5 dni w tygodniu), j.m. (m-c, m2/m-c, godz., usługa, km), "
                         "ilość = liczba jednostek w CAŁYM okresie umowy (np. 12 miesięcy × powierzchnia), cena jednostkowa netto – średnia rynkowa "
                         "w regionie z kosztami pracy (płaca minimalna, narzuty) i zyskiem. Okres umowy, ilości (np. liczba porcji, godzin, m²) "
                         "i częstotliwość WYŁĄCZNIE z dokumentów i opisu zamawiającego – nie zakładaj ich i nie dodawaj usług spoza zakresu; "
                         "brak ilości = ilość 0 i wpis do \"do_uzupelnienia\". W podstawie wpisz kod CPV. "
                         + (wskazowki or ""))
        else:
            wskazowki = (("SZACOWANIE KOSZTU DOSTAW dla INWESTORA PRYWATNEGO (wspólnota mieszkaniowa, spółdzielnia, deweloper) – budżet przed "
                          "zebraniem ofert od dostawców. Zamawiający NIE stosuje ustawy Pzp – nie powołuj jej przepisów. To NIE jest oferta ani "
                          "formularz wykonawcy. Działy = grupy asortymentowe (np. wyposażenie, urządzenia, materiały). " if pryw else
                          "KOSZTORYS INWESTORSKI – SZACOWANIE WARTOŚCI ZAMÓWIENIA NA DOSTAWY sporządzany przez ZAMAWIAJĄCEGO przed wszczęciem "
                          "postępowania (art. 28–36 Pzp: wartość netto, bez VAT, z należytą starannością). To NIE jest oferta ani formularz wykonawcy. "
                          "Działy = grupy asortymentowe (np. meble, sprzęt komputerowy, wyposażenie); jeśli przewidziane – osobny dział „Prawo opcji / "
                          "zamówienia przewidziane w umowie” (wlicza się do wartości). ") + "Pozycje: towar opisany minimalnymi parametrami (bez nazw "
                         "producentów), j.m. (szt., kpl., op., l, kg), ilość z dokumentów, cena jednostkowa netto – AKTUALNA średnia cena rynkowa "
                         "(z dostawą, transportem, montażem i szkoleniem, jeśli wymagane). W uwagach podaj źródło ceny (sklep, katalog, wcześniejsze "
                         "zamówienie, zapytanie rynkowe) i kluczowe parametry; w podstawie kod CPV. Ilości WYŁĄCZNIE z dokumentów i opisu "
                         "zamawiającego – brak ilości = ilość 0 i wpis do \"do_uzupelnienia\"; nie dodawaj towarów spoza zakresu. " + (wskazowki or ""))
        content.append({"type": "text", "text": polecenie_kosztorysu(c, wskazowki)})
        system = SYSTEM_KOSZTORYS_INW if c.get("_rola_inwestorska") else SYSTEM_KOSZTORYS
    elif typ in INWESTORSKIE:
        wskazowki = (("KOSZTORYS INWESTORSKI dla INWESTORA PRYWATNEGO (wspólnota mieszkaniowa, spółdzielnia, deweloper) – do ustalenia budżetu "
                      "robót i porównania ofert wykonawców przed wysłaniem zapytania ofertowego. Zamawiający NIE stosuje ustawy Pzp – "
                      "nie powołuj jej przepisów ani pojęć (przetarg, wartość zamówienia w rozumieniu Pzp). " if pryw else
                      "KOSZTORYS INWESTORSKI sporządzany dla ZAMAWIAJĄCEGO – do ustalenia wartości zamówienia przed przetargiem. ")
                     + "Opis robót zgodnie z dokumentacją projektową i przedmiarem, ilości z przedmiaru (albo wyliczone z dokumentacji), "
                     "ceny średnie rynkowe (jak w publikacjach cenowych) obejmujące koszty pośrednie i zysk. Pole \"zamawiajacy_nazwa\" "
                     "to inwestor. " + ROZB.POLECENIE_ZAMAWIAJACEGO + (wskazowki or ""))
        content.append({"type": "text", "text": polecenie_kosztorysu(c, wskazowki)})
        system = SYSTEM_KOSZTORYS_INW if c.get("_rola_inwestorska") else SYSTEM_KOSZTORYS
    elif typ in ("kosztorys", "wlasny"):
        if typ == "wlasny":
            wskazowki = ("KOSZTORYS OFERTOWY dla projektu własnego firmy (zlecenie od inwestora prywatnego lub firmy) – na jego podstawie "
                         "powstanie oferta dla klienta. " + ("UWAGA: w dokumentach jest GOTOWY KOSZTORYS – przepisz WSZYSTKIE jego pozycje, "
                         "ilości i ceny DOKŁADNIE, bez własnej wyceny. " if m.get("kosztorys_wlasny") else "") + (wskazowki or ""))
        content.append({"type": "text", "text": polecenie_kosztorysu(c, wskazowki)})
        system = SYSTEM_KOSZTORYS_INW if c.get("_rola_inwestorska") else SYSTEM_KOSZTORYS
    else:
        if typ == "przetarg" and m.get("rodzaj_zamowienia") in ("dostawy", "uslugi"):  # oferta dostawcy / usługodawcy
            if m["rodzaj_zamowienia"] == "dostawy":
                wskazowki = ("OFERTA DOSTAWCY w zamówieniu na DOSTAWY (nie roboty budowlane). Zamiast kosztorysu budowlanego przygotuj FORMULARZ "
                             "CENOWY / ASORTYMENTOWO-CENOWY: jeśli w dokumentach jest wzór formularza cenowego, przepisz DOKŁADNIE jego pozycje, "
                             "kolejność, j.m. i ilości; inaczej zbuduj go z opisu przedmiotu zamówienia. Działy = części zamówienia lub grupy asortymentu. "
                             "Pozycje: towar z wymaganymi parametrami, j.m. (szt., kpl., op., l, kg, t), ilość, cena jednostkowa netto – rynkowa cena "
                             "dostawcy z kosztem dostawy (i wniesienia, montażu, szkolenia, jeśli wymagane) oraz marżą. W uwagach pozycji: kluczowe "
                             "parametry i wymagany termin dostawy/gwarancji. Brakujące ilości przyjmij jawnie i dopisz do \"do_weryfikacji\". "
                             + (wskazowki or ""))
            else:
                wskazowki = ("OFERTA USŁUGODAWCY w zamówieniu na USŁUGI (nie roboty budowlane). Zamiast kosztorysu budowlanego przygotuj FORMULARZ "
                             "CENOWY / KALKULACJĘ CENY USŁUGI: jeśli w dokumentach jest wzór formularza cenowego, przepisz DOKŁADNIE jego pozycje, "
                             "j.m. i ilości; inaczej zbuduj go z opisu przedmiotu zamówienia. Działy = rodzaje usług, obiekty lub części zamówienia. "
                             "Pozycje: usługa, j.m. (m-c, godz., m2/m-c, km, usługa, osoba), ilość = liczba jednostek w CAŁYM okresie umowy "
                             "(np. 12 miesięcy × powierzchnia), cena jednostkowa netto – z kosztami pracy (płaca minimalna, ZUS, urlopy), środkami, "
                             "sprzętem, dojazdami, kosztami ogólnymi i zyskiem. W uwagach: okres umowy, częstotliwość, wymagany personel. "
                             "Brakujące założenia przyjmij jawnie i dopisz do \"do_weryfikacji\". " + (wskazowki or ""))
        if m.get("kosztorys_wlasny"):
            wskazowki = ("UWAGA: w dokumentach jest GOTOWY KOSZTORYS WYKONAWCY – przepisz WSZYSTKIE jego pozycje, ilości i ceny DOKŁADNIE, "
                         "bez własnej wyceny; pozostałe dane (postępowanie, zamawiający, terminy, wymagania) odczytaj z dokumentów przetargu. "
                         + (wskazowki or ""))
        if typ == "wlasny":
            wskazowki = ("To projekt własny firmy (zlecenie od inwestora prywatnego lub umowa), a nie przetarg publiczny – "
                         "nie wymagaj formalności przetargowych (wadium, JEDZ, oświadczenia), jeśli dokumenty ich nie przewidują; "
                         "numer postępowania zostaw pusty, jeśli go brak. " + (wskazowki or ""))
        content.append({"type": "text", "text": MO.zbuduj_polecenie(c, [], m.get("przetarg"), wskazowki)})
        system = MO.SYSTEM_OFERTA
    log(f"Wysyłam do AI {len(wybrane)} plików ({suma / 1024 / 1024:.1f} MB); wycena cenami rynkowymi")
    arch_ = [x["sciezka"] for x in lista_plikow(pid) if not x["uwzglednij"] and x["sciezka"].lower().endswith((".7z", ".rar", ".zip"))]
    if arch_:  # np. „SWZ+ załączniki.7z” – bez rozpakowania AI nie widzi przedmiaru i SWZ
        log("UWAGA: nierozpakowane archiwa nie trafiają do AI: " + ", ".join(arch_[:5])
            + " – rozpakuj je na komputerze i wgraj pliki w kroku 1 (inaczej kosztorys nie będzie miał ilości z przedmiaru).")
    ost = [0]

    def postep(n):
        if n - ost[0] > 4000:
            ost[0] = n
            log(f"AI pisze kosztorys… {n // 1000} tys. znaków")
    txt, powod = MO.claude_stream(c, system, content, postep=postep, log=log)
    with open(os.path.join(d, "odpowiedz_ai_oferta.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    dane = MO.wyciagnij_json(txt)
    if powod == "max_tokens" or dane.get("_naprawiony"):
        log("UWAGA: odpowiedź AI była niepełna – kosztorys może nie zawierać wszystkich pozycji. Sprawdź go z przedmiarem.")
    try:  # stawka VAT wybrana przez użytkownika ma pierwszeństwo przed odczytem AI
        dane.setdefault("postepowanie", {})["vat"] = float(c.get("vat_wybor"))
    except (TypeError, ValueError):
        pass
    dane = MO.przelicz(dane)
    if dane.get("vat_nieustalony"):
        log("UWAGA: stawka VAT nie wynika z dokumentów – przyjęto 23% do obliczeń. Wybierz właściwą stawkę w kroku 2 (Zmień stawkę VAT).")
    else:
        log(f"Stawka VAT: {dane['vat']:.0%}" + (" (wybrana)" if c.get("vat_wybor") not in (None, "", "auto") else " (z dokumentów przetargu)"))
    uzupelnij_zamawiajacego(dane.get("postepowanie", {}), log)
    if cennik_ and not m.get("kosztorys_wlasny"):  # ceny z cennika mają pierwszeństwo; reszta zostaje rynkowa
        CW.zastosuj(dane, cennik_, log)
        dane = MO.przelicz(dane)
    if c.get("ceny_internet", True) and not m.get("kosztorys_wlasny"):
        try:
            przed = {(i, j): (p_.get("cena"), p_.get("opis")) for i, dz in enumerate(dane.get("dzialy", [])) for j, p_ in enumerate(dz.get("pozycje", []))}
            netto_przed = dane.get("netto")
            rodzaj_cen = m.get("rodzaj_zamowienia") if m.get("rodzaj_zamowienia") in ("dostawy", "uslugi") and (typ in INWESTORSKIE or jest_dostawca(m)) else "roboty"
            if CR.weryfikuj_kosztorys(c, dane, log, dane.get("postepowanie", {}).get("obiekt", "") or region_domyslny(c), rodzaj_cen):
                dane = MO.przelicz(dane)
                zmiany = [(opis, st, p_.get("cena"), p_.get("jm")) for i, dz in enumerate(dane.get("dzialy", []))
                          for j, p_ in enumerate(dz.get("pozycje", [])) for st, opis in [przed.get((i, j), (None, None))]
                          if st is not None and abs((p_.get("cena") or 0) - st) >= 0.01]
                if zmiany:
                    odswiez_teksty_oferty(c, dane, zmiany, netto_przed, log)
        except Exception as e:
            log(f"Nie udało się pobrać cen z internetu ({e}) – zostają ceny rynkowe oszacowane przez AI.")
    pisz(os.path.join(d, "oferta_dane_oryginal.json"), dane)
    zapisz_oferte(pid, dane, c)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), dane)
    pp_ = [p_ for dz in dane.get("dzialy", []) if not ROZB.RE_POZA.search(str(dz.get("nazwa") or "")) for p_ in dz.get("pozycje", [])]
    bez_il = [p_ for p_ in pp_ if not float(p_.get("ilosc") or 0)]
    if pp_ and len(bez_il) >= max(1, len(pp_) // 2):  # np. tylko ogłoszenie, bez przedmiaru – AI dało ceny jednostkowe, ilości 0
        uw = (f"Kosztorys bez ilości: {len(bez_il)} z {len(pp_)} pozycji ma ilość 0 – w dokumentach projektu nie ma przedmiaru ani projektu "
              "(sprawdź krok 1: nierozpakowane archiwa, pominięte pliki). Cena oferty NIE obejmuje tych robót.")
        m_ = meta(pid)
        if uw not in (m_.get("oferta") or {}).get("do_weryfikacji", []):
            m_.setdefault("oferta", {}).setdefault("do_weryfikacji", []).insert(0, uw)
            zapisz_meta(pid, m_)
        log("UWAGA: " + uw)
    log(f"Gotowe: brutto {MO.zl(dane['brutto'])}")
    return meta(pid)["oferta"]


POLA_TEKSTOW_OFERTY = ("podsumowanie", "ryzyka", "do_weryfikacji", "do_uzupelnienia", "pytania_do_zamawiajacego")


def odswiez_teksty_oferty(c, dane, zmiany, netto_przed, log):
    """Po aktualizacji cen z internetu: kwoty w podsumowaniu i uwagach (pisanych przez AI przed aktualizacją) przeliczone do nowych cen
    i nowej ceny oferty – lżejszy model, zmienia wyłącznie kwoty. Gdy się nie uda – wyraźna informacja, że kwoty w uwagach są sprzed aktualizacji."""
    teksty = {k: dane.get(k) for k in POLA_TEKSTOW_OFERTY if dane.get(k)}
    if not teksty:
        return
    zm = "\n".join(f"- {o[:90]}: było {MO.zl(st)}/{jm or 'j.m.'}, jest {MO.zl(nw)}/{jm or 'j.m.'}" for o, st, nw, jm in zmiany[:40])
    pol = (f"Ceny niektórych pozycji kosztorysu zmieniono po sprawdzeniu w internecie:\n{zm}\n"
           f"Cena oferty netto: było {MO.zl(netto_przed or 0)}, jest {MO.zl(dane['netto'])}; brutto jest {MO.zl(dane['brutto'])} (VAT {dane['vat']:.0%}).\n"
           "Poniżej teksty napisane PRZED zmianą. Popraw w nich WYŁĄCZNIE kwoty, które wynikają z tych cen (ceny jednostkowe, wartości, cena oferty, "
           "kwoty liczone od ceny oferty, np. kara dzienna, limit kar, zabezpieczenie). Nie zmieniaj niczego innego – ta sama liczba elementów list, "
           "ta sama kolejność i treść. Zwróć JSON z tymi samymi kluczami.\n" + json.dumps(teksty, ensure_ascii=False))
    try:
        cl = dict(c, _model=c.get("model_lekki") or c.get("model"))
        txt, _ = MO.claude_stream(cl, "Poprawiasz kwoty w tekstach kosztorysu. Odpowiadasz wyłącznie JSON-em.", [{"type": "text", "text": pol}],
                                  max_tokens=8000, log=log)
        nowe = MO.wyciagnij_json(txt) or {}
        ok_ = {k: v for k, v in nowe.items() if k in teksty and type(v) is type(teksty[k])
               and (not isinstance(v, list) or len(v) == len(teksty[k]))}
        if ok_:
            dane.update(ok_)
            log(f"Kwoty w podsumowaniu i uwagach przeliczone do nowych cen ({len(ok_)} z {len(teksty)} części).")
        if len(ok_) == len(teksty):
            return
    except Exception as e:
        log(f"Nie udało się przeliczyć kwot w uwagach ({str(e)[:80]}).")
    uw = "Kwoty w podsumowaniu i uwagach mogą pochodzić sprzed aktualizacji cen z internetu – aktualne ceny i cena oferty są w kosztorysie."
    if uw not in dane.setdefault("do_weryfikacji", []):
        dane["do_weryfikacji"].insert(0, uw)


SYSTEM_KOSZTORYS = """Jesteś doświadczonym kosztorysantem w polskiej firmie budowlanej (termomodernizacje, elewacje, dachy, \
remonty, roboty ogólnobudowlane). Na podstawie dokumentów (przedmiar, projekt, rysunki, opis techniczny, zdjęcia, \
opis użytkownika) przygotowujesz kosztorys prac z aktualnymi cenami rynkowymi. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em."""


SYSTEM_KOSZTORYS_INW = """Jesteś doświadczonym kosztorysantem inwestorskim pracującym dla ZAMAWIAJĄCEGO (jednostki publicznej lub inwestora). \
Szacujesz wartość zamówienia przed wyborem wykonawcy – rzetelnie, na podstawie rzeczywistego zakresu z dokumentów i opisu zamawiającego, \
z aktualnymi cenami rynkowymi w regionie realizacji. Nie zgadujesz ilości. Odpowiadasz WYŁĄCZNIE poprawnym JSON-em."""


def odcisk_zakresu(K, rodzaj):
    """Skrót zakresu zamówienia (opis, przedmiot, zakres, ilości) – do wykrycia zmiany po szacowaniu wartości."""
    import hashlib
    p = (K or {}).get("potrzeba") or {}
    t = "|".join(re.sub(r"\s+", " ", str(x or "")).strip().lower() for x in ((K or {}).get("opis"), p.get("przedmiot"), p.get("zakres"), p.get("ilosci"), rodzaj))
    return hashlib.sha1(t.encode("utf-8")).hexdigest()[:12]


def region_domyslny(c):
    """Region cen, gdy nie wynika z dokumentów: miejsce realizacji z kreatora → siedziba / obszar działania konta. Bez regionu wpisanego na stałe."""
    return str(c.get("_region_realizacji") or c.get("centrum_opis") or c.get("centrum_nazwa") or c.get("firma_adres") or "").strip()


def polecenie_kosztorysu(c, opis):
    dzis = dt.date.today()
    mies = f"{MO.MIESIACE[dzis.month - 1]} {dzis.year}"
    if c.get("_rola_inwestorska"):  # zamawiający: kosztorys inwestorski – bez wykonawcy, ilości tylko z dokumentów / opisu
        region = region_domyslny(c) or "miejsce wynikające z dokumentów (gdy brak – średnie ceny krajowe; przyjęty region wpisz do \"do_weryfikacji\")"
        pryw = bool(c.get("_prywatny"))
        zam = c.get("_zamawiajacy") or "zamawiający wskazany w dokumentach (jeśli brak – pole zamawiajacy_nazwa zostaw puste)"
        return (f"Dzisiejsza data: {dzis:%d.%m.%Y}. ZAMAWIAJĄCY: {zam}. Kosztorys inwestorski sporządza zamawiający (albo osoba działająca na jego rzecz). "
                + ("WYKONAWCA NIE JEST ZNANY – zostanie wybrany po zebraniu ofert; nie wpisuj nigdzie danych wykonawcy ani słów o ofercie. "
                 "Zamawiający jest podmiotem prywatnym i NIE stosuje ustawy Pzp – nie powołuj jej przepisów.\n" if pryw else
                 "WYKONAWCA NIE JEST ZNANY – zostanie wyłoniony w postępowaniu; nie wpisuj nigdzie danych wykonawcy ani słów o ofercie.\n")
                + f"OPIS ZAKRESU OD ZAMAWIAJĄCEGO: {opis or 'brak – opieraj się na dokumentach'}\n\n"
                + ("Przygotuj kosztorys inwestorski (szacunek kosztów przed zebraniem ofert).\n\nZASADY:\n" if pryw else
                   "Przygotuj kosztorys inwestorski (szacowanie wartości zamówienia).\n\nZASADY:\n") +
                ""
                "1. Jeśli w dokumentach jest przedmiar albo wykaz ilości – przepisz pozycje DOKŁADNIE (opis, j.m., ilość, podstawa).\n"
                "2. ILOŚCI WYŁĄCZNIE z dokumentów i z opisu zamawiającego (dla robót – także obliczone z rysunków i wymiarów, z obliczeniem w uwagach). "
                "NIE zakładaj ilości (osób, dni, porcji, wydarzeń, kursów) i NIE dodawaj pozycji ani usług spoza zakresu zamówienia. "
                "Gdy ilości brak: ilość 0, w uwagach „ILOŚĆ DO UZUPEŁNIENIA”, wpis do \"do_uzupelnienia\". W uwagach każdej pozycji podaj, skąd ilość.\n"
                f"3. Każdą pozycję wyceń AKTUALNĄ CENĄ RYNKOWĄ netto na {mies} dla miejsca realizacji: {region} – pełna cena, jaką zapłaci zamawiający "
                "(z kosztami wykonawcy i zyskiem). Ceny z innych regionów oznacz w źródle „inny region” i skoryguj. rynkowa = 1.\n"
                "4. Grupuj pozycje w działy (rodzaje robót / usług / grupy towarów).\n"
                + ("5. VAT: inwestor prywatny płaci cenę brutto – ustal stawkę (8% dla budynków mieszkalnych objętych społecznym programem "
                   "mieszkaniowym, w pozostałych przypadkach 23%) i dopisz założenie do \"do_weryfikacji\".\n" if pryw else
                   "5. VAT podaj informacyjnie (wartość zamówienia jest bez VAT); założenie stawki dopisz do \"do_weryfikacji\".\n") +
                ""
                "6. W \"postepowanie\" wpisz: nazwa_zamowienia, obiekt (miejsce realizacji), zamawiajacy_nazwa (zamawiający powyżej); numer pusty.\n"
                "7. Listy: \"do_weryfikacji\" – co sprawdzić przed przyjęciem wartości; \"ryzyka\" – co może zmienić koszt; "
                "\"do_uzupelnienia\" – czego brakuje do rzetelnego szacowania; \"pytania_do_zamawiajacego\" – pusta lista.\n\n" + MO.SCHEMAT)
    reg = region_domyslny(c)
    reg = (f"miejsce realizacji z dokumentów; gdy z nich nie wynika – {reg}" if reg else "miejsce realizacji z dokumentów; gdy z nich nie wynika – "
           "średnie ceny krajowe") + "; przyjęty region wpisz do \"do_weryfikacji\""
    return (f"Dzisiejsza data: {dzis:%d.%m.%Y}. Wykonawca: {c.get('firma_nazwa', '')}.\n"
            f"OPIS ZAKRESU OD UŻYTKOWNIKA: {opis or 'brak – opieraj się na dokumentach'}\n\n"
            "Przygotuj kosztorys prac.\n\nZASADY:\n"
            "1. Jeśli w dokumentach jest przedmiar – przepisz jego pozycje DOKŁADNIE (opis, j.m., ilość, podstawa), "
            "w jego kolejności i działach.\n"
            "2. Jeśli przedmiaru nie ma – sporządź go sam z rysunków, opisów, zdjęć i wymiarów podanych przez użytkownika. "
            "Przy każdej pozycji w uwagach pokaż obliczenie ilości (np. \"elewacja 12,50 × 9,80 − okna 14 × 1,80 = 97,30 m2\"). "
            "Nie zgaduj bez podstaw: brakujące wymiary przyjmij jawnie jako założenie i dopisz je do \"do_weryfikacji\".\n"
            "3. Uwzględnij roboty towarzyszące, bez których prac nie da się wykonać (rusztowania, zabezpieczenia, "
            "demontaże, wywóz odpadów, sprzątanie), jeśli wynikają z zakresu.\n"
            f"4. Każdą pozycję wyceń AKTUALNĄ CENĄ RYNKOWĄ netto na {mies} ({reg}): pełna "
            "cena wykonawcy (materiał + robocizna + sprzęt + koszty pośrednie + zysk). rynkowa = 1, źródło zostaw puste. "
            "W uwagach podaj główne założenie ceny, gdy ma znaczenie (np. grubość izolacji, rodzaj materiału).\n"
            "5. Grupuj pozycje w działy wg rodzajów robót (lub wg działów przedmiaru).\n"
            "6. VAT: 8% dla obiektów budownictwa objętego społecznym programem mieszkaniowym (art. 41 ust. 12–12c ustawy o VAT: budynki mieszkalne, "
            "lokale mieszkalne do 150 m², domy jednorodzinne do 300 m²; powyżej limitu – 8% tylko proporcjonalnie do limitu, reszta 23%); "
            "lokale użytkowe i obiekty niemieszkalne – 23% – "
            "przyjmij właściwy i napisz założenie w \"do_weryfikacji\".\n"
            "7. W \"postepowanie\" wpisz: nazwa_zamowienia (nazwa zadania), obiekt (adres), zamawiajacy_nazwa (inwestor, jeśli znany), "
            "vat; numer zostaw pusty; pozostałe pola mogą być puste.\n"
            "8. \"podsumowanie\": 3–5 zdań o zakresie i głównych założeniach; \"ryzyka\": co może zmienić cenę; "
            "\"pytania_do_zamawiajacego\": pytania do inwestora, które doprecyzują wycenę.\n\n" + MO.SCHEMAT)


def zamawiajacy_projektu(m, P=None):
    """Zamawiający w dokumentach zamawiającego: wpisany w kreatorze → odczytany z dokumentów → „[UZUPEŁNIJ]”.
    Dane z profilu firmy NIE są wstawiane automatycznie (profil może należeć do osoby przygotowującej zamówienie)."""
    K = m.get("kreator") or {}
    if (K.get("zamawiajacy") or "").strip():
        return K["zamawiajacy"].strip()
    P = P or {}
    z = ", ".join(x for x in (P.get("zamawiajacy_nazwa"), P.get("zamawiajacy_adres"), ("NIP " + P["zamawiajacy_nip"]) if P.get("zamawiajacy_nip") else "") if x)
    return z or "[UZUPEŁNIJ: nazwa i adres zamawiającego]"


def _liczby_z_tekstu(t):
    wyn = set()
    for x in re.findall(r"(?<![\d,.])\d{1,3}(?:[ \u00a0.]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?", t or ""):
        x = x.replace("\u00a0", "").replace(" ", "")
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", x):
            x = x.replace(".", "")
        try:
            v = float(x.replace(",", "."))
        except ValueError:
            continue
        if 0 < v < 1e8:
            wyn.add(round(v, 3))
    return wyn


def kontrola_ilosci(pid, m, dane):
    """Kosztorys inwestorski: każda ilość musi mieć oparcie w dokumentach zamawiającego albo w jego opisie (kreator).
    Ilość, której nie ma w tekstach (ani jako iloczyn dwóch liczb z tekstów), jest oznaczana jako „bez potwierdzenia”."""
    teksty = []
    try:
        teksty += [d.get("tekst") or "" for d in OD.teksty(pdir(pid), ("dokumenty", "wzory")).values()]
    except Exception:
        pass
    K = m.get("kreator") or {}
    teksty += [K.get("opis") or ""] + [str(v) for v in (K.get("potrzeba") or {}).values()] + [m.get("wskazowki_oferty") or ""]
    liczby = set()
    for t in teksty:
        liczby |= _liczby_z_tekstu(t)
    male = sorted(x for x in liczby if x <= 400)[:300]
    iloczyny = {round(a * b, 3) for a in male for b in liczby if b < 1e6}
    brak = []
    for dz in dane.get("dzialy") or []:
        for p in dz.get("pozycje") or []:
            il = round(float(p.get("ilosc") or 0), 3)
            if not il:
                continue
            ok = il in liczby or il in iloczyny or il in (1, 1.0) and str(p.get("jm", "")).lower() in ("kpl", "kpl.", "komplet", "usługa", "usl", "szt", "szt.")
            if not ok:
                p["ilosc_bez_podstawy"] = True
                brak.append(f"{str(p.get('opis') or '')[:60]} – {il:g} {p.get('jm', '')}")
    if brak:
        dane.setdefault("do_weryfikacji", [])[:0] = [f"ILOŚĆ BEZ POTWIERDZENIA W DOKUMENTACH: {x}" for x in brak[:20]]
        dane["_kontrola_ilosci"] = (f"UWAGA: {len(brak)} pozycji ma ilość, której nie ma w dokumentach zamawiającego ani w jego opisie – "
                                    "nie przyjmuj wartości przed sprawdzeniem (pozycje z różowym tłem).")
    dane["_ilosci_bez_podstawy"] = brak
    return brak




def plik_klienta(m):
    return f"Kosztorys_dla_klienta_{MO.bezpieczna_nazwa(m.get('nazwa', 'oferta'))[:60]}.xlsx"


def uzupelnij_zamawiajacego(P, log=None):
    """Dane zamawiającego z wykazu VAT, gdy AI odczytało z dokumentów poprawny NIP."""
    if not NIP.poprawny(P.get("zamawiajacy_nip")):
        return False
    d = wykaz(P["zamawiajacy_nip"], czekaj=True)
    if not d or not d.get("nazwa"):
        if log:
            log("Zamawiającego nie ma w wykazie VAT – zostają dane odczytane z dokumentów.")
        return False
    P["zamawiajacy_nazwa"], P["zamawiajacy_nip"] = d["nazwa"], d["nip"]
    if d.get("adres"):
        P["zamawiajacy_adres"] = d["adres"]
    if d.get("regon"):
        P["zamawiajacy_regon"] = d["regon"]
    if log:
        log(f"Dane zamawiającego z wykazu VAT: {d['nazwa']}, {d.get('adres', '')}")
    return True


def jest_dostawca(m):
    return (m.get("typ") or "przetarg") == "przetarg" and m.get("rodzaj_zamowienia") in ("dostawy", "uslugi")


def zapisz_oferte(pid, dane, c, korekta=None):
    """Zapisuje dane oferty oraz generuje kosztorys, formularze i analizę; aktualizuje podsumowanie projektu."""
    d = pdir(pid)
    m = meta(pid)
    stare = [m.get("kosztorys")] + (m.get("pliki_oferty") or [])
    pk, pf, pa = pliki_oferty(m)
    pkl = None if m.get("typ") in INWESTORSKIE + ("dom",) or jest_dostawca(m) else plik_klienta(m)
    for n in stare:  # gdy zmieniono nazwę projektu – usuń stare wersje
        if n and n not in (pk, pf, pa, pkl) and not n.startswith("Komplet_") and os.path.isfile(os.path.join(d, n)):
            os.remove(os.path.join(d, n))
    tylko_kosztorys = tylko_kosztorys_typ(m)
    dane = zastosuj_decyzje_rozbieznosci(m, dane, korekta)
    if m.get("typ") in INWESTORSKIE or m.get("typ") == "dom":
        dane["_inwestorski"] = True
        dane["_rola_nazwa"] = "Inwestor" if m.get("typ") == "dom" else "Zamawiający"
        dane["_zamawiajacy"] = (f"{c.get('firma_nazwa', '')}, {c.get('firma_adres', '')}" if m.get("typ") == "dom"
                                else zamawiajacy_projektu(m, dane.get("postepowanie") or {}))
        if m.get("typ") in INWESTORSKIE:
            kontrola_ilosci(pid, m, dane)
    pryw_ = m.get("typ") in INWESTORSKIE and projekt_wspolnoty(m)
    if m.get("typ") in INWESTORSKIE:
        dane["do_weryfikacji"] = [x for x in dane.get("do_weryfikacji") or [] if not str(x).startswith(UWAGA_WSTEPNY)]
        if not pryw_ and m.get("rodzaj_zamowienia") not in ("uslugi", "dostawy") and not m.get("kosztorys_wlasny"):
            dane["do_weryfikacji"].insert(0, UWAGA_WSTEPNY + " przygotowany przez program – materiał pomocniczy. NIE jest podstawą wartości zamówienia: "
                                          "wartość zamówienia na roboty budowlane ustala się na podstawie kosztorysu inwestorskiego albo planowanych kosztów "
                                          "z PFU sporządzonych przez projektanta lub kosztorysanta (art. 34 ust. 1 Pzp) – wgraj ten dokument w szacowaniu wartości.")
    dane["_tytul"] = (({"uslugi": "SZACUNKOWY KOSZT USŁUG", "dostawy": "SZACUNKOWY KOSZT DOSTAW"} if pryw_ else
                       {"uslugi": "KOSZTORYS INWESTORSKI – SZACOWANIE WARTOŚCI ZAMÓWIENIA NA USŁUGI", "dostawy": "KOSZTORYS INWESTORSKI – SZACOWANIE WARTOŚCI ZAMÓWIENIA NA DOSTAWY"})
                      .get(m.get("rodzaj_zamowienia"), "KOSZTORYS INWESTORSKI" if pryw_ or m.get("kosztorys_wlasny") else "WSTĘPNY KOSZTORYS ROBÓT (MATERIAŁ POMOCNICZY)")) if m.get("typ") in INWESTORSKIE else "KOSZTORYS BUDOWY DOMU" if m.get("typ") == "dom" \
        else "KOSZTORYS OFERTOWY" if m.get("typ") == "wlasny" else "KOSZTORYS" if tylko_kosztorys \
        else ("FORMULARZ ASORTYMENTOWO-CENOWY" if m.get("rodzaj_zamowienia") == "dostawy" else "FORMULARZ CENOWY") if jest_dostawca(m) else None
    dane_kl = None
    if pkl:  # wersja dla zamawiającego: koszty spoza przedmiaru w cenach pozycji, bez pozycji z ilością 0 – suma równa cenie oferty
        dane_kl, opis_kl = MO.dla_zamawiajacego(dane)
        rozn = MO.zaokr(dane_kl["netto"] - dane["netto"])
        if rozn and abs(rozn) <= 1:  # tylko groszowe zaokrąglenia (bez pozycji z ilością 1) – ta sama kwota w kosztorysie wewnętrznym
            kpl = [p_ for dz in dane["dzialy"] for p_ in dz["pozycje"] if p_.get("ilosc") == 1 and (p_.get("cena") or 0) > abs(rozn)]
            if kpl:
                kpl[-1]["cena"] = MO.zaokr(kpl[-1]["cena"] + rozn)
                dane = MO.przelicz(dane)
        dane["do_weryfikacji"] = [x for x in dane.get("do_weryfikacji", []) if not str(x).startswith("W kosztorysie dla zamawiającego koszty")]
        if opis_kl:
            dane["do_weryfikacji"].append(opis_kl)
    if m.get("gwarancja_oferty"):  # wybór wykonawcy ma pierwszeństwo przed propozycją AI
        dane.setdefault("postepowanie", {})["gwarancja_mies"] = m["gwarancja_oferty"]
    MO.zapisz_kosztorys(dane, c, os.path.join(d, pk))
    if pkl:
        MO.zapisz_kosztorys(dane_kl, c, os.path.join(d, pkl), dla_klienta=True)
    if tylko_kosztorys:
        pf = pa = None
    elif jest_dostawca(m):  # dostawca: załączniki według ogłoszenia przygotowuje praca_zalaczniki_dostawcy (nie szablony budowlane)
        if not os.path.isfile(os.path.join(d, pf)):
            pf = None
    else:
        MO.zapisz_formularze(dane, c, os.path.join(d, pf))
        if pa:
            MO.zapisz_analize(dane, c, os.path.join(d, pa))
    pisz(os.path.join(d, "oferta_dane.json"), dane)
    P = dane["postepowanie"]
    m["kosztorys"] = pk
    m["pliki_oferty"] = [x for x in (pk, pf, pa, pkl) if x]
    m["kosztorys_klienta"] = pkl
    m["oferta"] = {"netto": dane["netto"], "vat": dane["vat"], "vat_nieustalony": bool(dane.get("vat_nieustalony")),
                   "vat_kwota": dane["vat_kwota"], "brutto": dane["brutto"],
                   "rynkowe": dane["wartosc_rynkowych"], "udzial_rynkowych": dane["udzial_rynkowych"],
                   "nazwa_zamowienia": P.get("nazwa_zamowienia", ""), "numer": P.get("numer", ""),
                   "gwarancja_ai": P.get("gwarancja_mies") if not m.get("gwarancja_oferty") else (m.get("oferta") or {}).get("gwarancja_ai"),
                   "kryteria": P.get("kryteria", ""),
                   "termin_skladania": P.get("termin_skladania", ""), "wadium": P.get("wadium", ""),
                   "obiekt": P.get("obiekt", ""), "podsumowanie": dane.get("podsumowanie", ""),
                   "do_weryfikacji": dane.get("do_weryfikacji", []), "do_uzupelnienia": dane.get("do_uzupelnienia", []),
                   "ryzyka": dane.get("ryzyka", []), "pytania": dane.get("pytania_do_zamawiajacego", []),
                   "z_internetu": sum(1 for dz in dane.get("dzialy", []) for p in dz.get("pozycje", [])
                                      if "internet" in str(p.get("zrodlo", ""))),
                   "ilosci_bez_podstawy": dane.get("_ilosci_bez_podstawy", []),
                   "korekta": korekta}
    orig = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None)
    if orig:
        m["oferta"]["netto_pierwotne"] = orig.get("netto")
        m["oferta"]["brutto_pierwotne"] = orig.get("brutto")
    zapisz_meta(pid, m)
    if m.get("typ") == "wlasny" and m.get("oferta_klienta"):  # kosztorys się zmienił – odśwież ofertę dla klienta (te same warunki)
        try:
            generuj_oferte_klienta(pid, (m["oferta_klienta"] or {}).get("pola") or {})
        except Exception:
            pass


def generuj_oferte_klienta(pid, pola):
    """Oferta dla klienta (Word) na podstawie kosztorysu projektu własnego: zakres (działy), cena, warunki; kosztorys dla klienta jako załącznik."""
    d = pdir(pid)
    m = meta(pid)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane or not dane.get("dzialy"):
        raise ValueError("Najpierw przygotuj kosztorys albo wgraj własny kosztorys (krok 2) – oferta powstaje na jego podstawie.")
    c = cfg()
    nazwa = f"Oferta_dla_klienta_{MO.bezpieczna_nazwa(m.get('nazwa', 'oferta'))[:50]}.docx"
    nr = pola.get("numer") or f"OF/{dt.date.today():%Y/%m}/{pid[:4].upper()}"
    WN.oferta_klienta_docx(os.path.join(d, nazwa), dane, c, {**pola, "numer": nr}, m.get("nazwa", ""), m.get("kosztorys_klienta"))
    m = meta(pid)
    m["oferta_klienta"] = {"plik": nazwa, "pola": {**pola, "numer": nr}, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                           "netto": dane.get("netto"), "brutto": dane.get("brutto")}
    m["pliki_oferty"] = sorted(set((m.get("pliki_oferty") or []) + [nazwa]))
    zapisz_meta(pid, m)
    return nazwa


@app.post("/api/projekty/<pid>/oferta-z-kosztorysu")
@wymaga_logowania
def oferta_z_kosztorysu(pid):
    """Projekt z przetargu: oferta (formularze ofertowe i analiza) na podstawie przygotowanego wcześniej kosztorysu."""
    d = pdir(pid)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane or not dane.get("dzialy"):
        return jsonify({"blad": "Najpierw przygotuj kosztorys albo wgraj własny kosztorys."}), 400
    m = meta(pid)
    m["oferta_przygotowana"] = True
    gw = str((request.json or {}).get("gwarancja") or "").strip()
    if gw:
        if not re.fullmatch(r"[0-9]{1,3}", gw) or not 1 <= int(gw) <= 240:
            return jsonify({"blad": "Okres gwarancji podaj w pełnych miesiącach (np. 60)."}), 400
        m["gwarancja_oferty"] = int(gw)
    zapisz_meta(pid, m)
    zapisz_oferte(pid, MO.przelicz(dane), cfg(), (m.get("oferta") or {}).get("korekta"))
    m = meta(pid)
    wyn = {"pliki": m.get("pliki_oferty"), "oferta": m.get("oferta")}
    c = cfg()
    if not jest_dostawca(m) and (c.get("api_key") or c.get("api_key_alt")) and lista_plikow(pid):
        # roboty: formularz ofertowy i oświadczenia według WZORÓW zamawiającego (jak przy dostawach) – podstawowy formularz programu zostaje w razie błędu
        try:
            wyn["zadanie"] = uruchom("zalaczniki", "Formularz ofertowy i oświadczenia według wzorów z SWZ", praca_zalaczniki_dostawcy, pid)
        except ZadanieTrwa as e:
            wyn["uwaga"] = str(e)
    return jsonify(wyn)


@app.post("/api/projekty/<pid>/oferta-klienta")
@wymaga_logowania
def oferta_klienta(pid):
    pola = {k: str(v or "")[:1000] for k, v in (request.json or {}).items()
            if k in ("klient_nazwa", "klient_adres", "klient_osoba", "termin_realizacji", "gwarancja", "platnosc", "waznosc", "uwagi", "miejsce", "numer")}
    try:
        nazwa = generuj_oferte_klienta(pid, pola)
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    if pola.get("klient_nazwa"):
        try:
            zapisz_klienta({"nazwa": pola["klient_nazwa"], "adres": pola.get("klient_adres", ""), "osoba": pola.get("klient_osoba", "")}, session.get("login", ""))
        except Exception:
            pass
    return jsonify({"url": f"/pobierz/{pid}/{urllib.parse.quote(nazwa)}", "plik": nazwa})


@app.post("/api/projekty/<pid>/dostosuj")
@wymaga_logowania
def dostosuj(pid):
    """Proporcjonalna zmiana wszystkich cen jednostkowych do zadanej ceny oferty (liczone od cen pierwotnych)."""
    d = pdir(pid)
    orig = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not orig:
        return jsonify({"blad": "Najpierw przygotuj ofertę."}), 400
    pisz(os.path.join(d, "oferta_dane_oryginal.json"), orig)
    tryb = request.json.get("tryb")
    if tryb == "reset":
        blad = zastosuj_korekte(pid, orig, "reset", None)
    else:
        try:
            w = MO.liczba_pl(request.json.get("wartosc", ""))
        except ValueError:
            return jsonify({"blad": "Podaj liczbę (np. 90 000,00)."}), 400
        blad = zastosuj_korekte(pid, orig, tryb, w)
    if blad:
        return jsonify({"blad": blad}), 400
    return jsonify(meta(pid)["oferta"])


def zastosuj_korekte(pid, orig, tryb, w):
    """Przelicza ofertę z danych pierwotnych: bez korekty (reset) albo z korektą do ceny netto/brutto/procentu."""
    c = cfg()
    dane = zastosuj_decyzje_rozbieznosci(meta(pid), MO.przelicz(json.loads(json.dumps(orig))))  # warianty i pozycje poza ceną – przed korektą
    dane = MO.przelicz(dane)
    n0, vat = dane["netto"], dane["vat"]
    if tryb == "reset" or not tryb:
        zapisz_oferte(pid, dane, c)
        return None
    cel = {"netto": w, "brutto": w / (1 + vat), "procent": n0 * (1 + w / 100)}.get(tryb)
    if cel is None or not math.isfinite(cel) or cel <= 0 or cel > 1e12 or n0 <= 0:
        return "Nieprawidłowa wartość docelowa."
    cel = MO.zaokr(cel)
    info_brutto = ""
    if tryb == "brutto":  # netto w groszach → nie każda kwota brutto jest osiągalna (VAT 23%: krok ok. 1,23 gr); bierzemy dokładną
        # albo najbliższą NIE WYŻSZĄ od docelowej (cena docelowa to zwykle górna granica – budżet zamawiającego)
        br = lambda n_: MO.zaokr(MO.zaokr(n_) + MO.zaokr(MO.zaokr(n_) * vat))
        kand = [MO.zaokr(cel + k / 100) for k in range(-3, 4)]
        dokl = [n_ for n_ in kand if abs(br(n_) - w) < 0.005]
        cel = dokl[0] if dokl else max([n_ for n_ in kand if br(n_) <= w + 1e-9] or [cel])
        if not dokl:
            info_brutto = (f"Kwoty {MO.zl(w)} brutto nie da się uzyskać z ceny netto w pełnych groszach przy VAT {round(vat * 100)}% – "
                           f"przyjęto najbliższą niższą: {MO.zl(br(cel))} brutto.")
    # ceny poprawione ręcznie (np. po kontroli kosztorysu) są stałe – korektę przejmują pozostałe pozycje
    reczna = lambda p: str(p.get("zrodlo") or "").startswith("poprawione")
    stale = MO.zaokr(sum(p["wartosc"] for dz in dane["dzialy"] for p in dz["pozycje"] if reczna(p)))
    if n0 - stale <= 0 or cel - stale <= 0:
        return "Cena docelowa jest niższa niż suma pozycji poprawionych ręcznie – zmień cenę docelową albo te pozycje."
    f = (cel - stale) / (n0 - stale)
    for dz in dane["dzialy"]:
        for p in dz["pozycje"]:
            if not reczna(p):
                p["cena"] = MO.zaokr(p["cena"] * f)
    dane = MO.przelicz(dane)
    reszta = MO.zaokr(cel - dane["netto"])
    if abs(reszta) >= 0.01:  # różnica z zaokrągleń – koryguj pozycję z ilością 1 (np. kpl)
        kand = [p for dz in dane["dzialy"] for p in dz["pozycje"] if abs(p["ilosc"] - 1) < 1e-9 and p["cena"] > abs(reszta) and not reczna(p)]
        if kand:
            x = max(kand, key=lambda p: p["cena"])
            x["cena"] = MO.zaokr(x["cena"] + reszta)
            dane = MO.przelicz(dane)
    zapisz_oferte(pid, dane, c, korekta={"procent": round((cel / n0 - 1) * 100, 2), "wspolczynnik": f, "tryb": tryb, "wartosc": w,
                                          "roznica_zaokraglen": MO.zaokr(cel - dane["netto"]), **({"info": info_brutto} if info_brutto else {})})
    return None


# ============================================================ kontrola kosztorysu







# ============================================================ zamawiający: weryfikacja i sporządzanie dokumentacji

def bloki_projektu(pid, cytaty=False, log=None):
    """Dokumenty projektu do zadań tekstowych – bez rysunków (PDF bez tekstu), długie skany ograniczone do pierwszych stron."""
    d = pdir(pid)
    pliki = [os.path.join(d, "dokumenty", p["sciezka"]) for p in lista_plikow(pid) if p["uwzglednij"]]
    bloki, suma = [], 0
    for p in pliki:
        b, n, ostrz = MO.przygotuj_blok_tekstowy(p)
        if ostrz and log:
            log(ostrz)
        if cytaty:
            for x in b:
                if x.get("type") == "document":
                    x["citations"] = {"enabled": True}
        bloki += b
        suma += n
    if suma > MO.MAX_BAJTOW_ZAPYTANIA:
        raise ValueError("Dokumenty są zbyt duże – pomiń rysunki w kroku 1 (Uwzględnij/pomiń).")
    return bloki, len(pliki)


def bloki_projektu_pliki(pid, log=None):
    """Jak bloki_projektu, ale osobno dla każdego pliku: [(nazwa, bloki, rozmiar)] – do sprawdzania dużej dokumentacji w częściach."""
    d = pdir(pid)
    wyn = []
    for p in [os.path.join(d, "dokumenty", x["sciezka"]) for x in lista_plikow(pid) if x["uwzglednij"]]:
        b, n, ostrz = MO.przygotuj_blok_tekstowy(p)
        if ostrz and log:
            log(ostrz)
        if b:
            wyn.append((os.path.basename(p), b, n))
    return wyn


TOKENY_CZESCI = 120_000  # ok. tyle tokenów dokumentów na jedno zapytanie przy sprawdzaniu w częściach
ZNAKI_NA_TOKEN = 3.3     # szacunek dla tekstu polskiego


def podziel_na_czesci(pliki, limit_tok=TOKENY_CZESCI):
    """Pliki → części ≤ limit (szacunek z rozmiaru). SWZ (jeśli nieduża) jest kotwicą dołączaną do każdej części."""
    tok = lambda n: n / ZNAKI_NA_TOKEN
    kotwica = next((x for x in pliki if re.search(r"(?i)\bswz\b|specyfikacj", x[0]) and tok(x[2]) <= 50_000), None)
    reszta = [x for x in pliki if x is not kotwica]
    limit = limit_tok - (tok(kotwica[2]) if kotwica else 0)
    czesci, biez, suma = [], [], 0
    for x in sorted(reszta, key=lambda x: -x[2]):
        if biez and suma + tok(x[2]) > limit:
            czesci.append(biez)
            biez, suma = [], 0
        biez.append(x)
        suma += tok(x[2])
    if biez:
        czesci.append(biez)
    if not czesci and kotwica:
        czesci = [[]]
    return kotwica, czesci


def ai_dane(c, system, tresc, max_tokens, log, parsuj, skroc=""):
    """Zadanie AI zwracające dane: tryb wymuszonej struktury (MO.claude_stream), odzysk kompletnych elementów z uciętej odpowiedzi,
    a gdy mimo to brak danych – jedno ponowienie z poleceniem krótszej odpowiedzi."""
    txt, powod = MO.claude_stream(c, system, tresc, max_tokens=max_tokens, log=log, max_kontynuacji=1)
    try:
        w = parsuj(txt)
        if isinstance(w, dict) and (w.get("_odzyskane") or w.get("_naprawiony")) and log:
            log("Odpowiedź była niekompletna – zachowano wszystkie kompletne elementy.")
        return w
    except ValueError as e:
        if log:
            log(f"{e} Ponawiam z krótszą odpowiedzią…")
    tresc2 = list(tresc) + [{"type": "text", "text": "WAŻNE: odpowiedz wyłącznie danymi w opisanej strukturze. " + (skroc or "Odpowiedź możliwie zwięzła.")}]
    txt, powod2 = MO.claude_stream(c, system, tresc2, max_tokens=max_tokens, log=log, max_kontynuacji=0)
    try:
        return parsuj(txt)
    except ValueError as e:
        d_ = MO.DIAG.get("ostatnia") or {}
        przyczyna = {"refusal": "AI odmówiło wykonania zadania", "max_tokens": "odpowiedź przekroczyła limit długości",
                     "end_turn": "AI zakończyło bez wyniku"}.get(d_.get("stop") or powod2, str(d_.get("stop") or powod2 or "nieznana"))
        raise ValueError(f"{e} Przyczyna: {przyczyna}; długość odpowiedzi: {len(txt or '')} znaków"
                         + (f" (początek: „{(txt or '').strip()[:200]}”)" if (txt or "").strip() else "") + ".") from None


def weryfikacja_w_czesciach(c, system, polec, pid, log):
    """Duża dokumentacja: sprawdzenie w częściach (SWZ w każdej części jako punkt odniesienia), połączenie uwag bez powtórzeń."""
    kotwica, czesci = podziel_na_czesci(bloki_projektu_pliki(pid, log))
    log(f"Sprawdzanie w {len(czesci)} częściach" + (f" – „{kotwica[0]}” w każdej części jako punkt odniesienia" if kotwica else "") + ".")
    uwagi, podsum, oceny, bledy = {}, [], [], []
    for i, cz in enumerate(czesci, 1):
        nazwy = [x[0] for x in cz]
        bl = (list(kotwica[1]) if kotwica else []) + [b for x in cz for b in x[1]]
        dop = (f"\n\nTO JEST CZĘŚĆ {i} z {len(czesci)} dokumentacji. Sprawdź dokumenty tej części: {', '.join(nazwy) or kotwica[0]}"
               + (f", w tym ich zgodność z „{kotwica[0]}”. Uwagi dotyczące wyłącznie „{kotwica[0]}” zgłaszaj tylko w części 1." if kotwica else ".")
               + " Inne części sprawdzane są osobno – nie zgłaszaj braku dokumentów, których tu nie ma.")
        tresc = MO.oznacz_dokumenty(bl, MO.ustawienie_cache(c)) + [{"type": "text", "text": polec + dop}]
        log(f"Część {i}/{len(czesci)}: {', '.join(nazwy)[:200] or kotwica[0]}…")
        try:
            w = ai_dane(c, system, tresc, 16000, log, ZAM.wynik_weryfikacji, "Najważniejsze uwagi najpierw, maksymalnie 20, zwięźle.")
        except ValueError as e:
            bledy.append(f"część {i} ({', '.join(nazwy)[:120]}): {e}")
            log(f"   Część {i} bez wyniku: {e}")
            continue
        widziane = {(u.get("dokument"), (u.get("cytat") or "")[:80]) for u in uwagi.values()}
        for u in w["uwagi"]:
            if u["id"] not in uwagi and (u.get("dokument"), (u.get("cytat") or "")[:80]) not in widziane:
                uwagi[u["id"]] = u
        if w.get("podsumowanie"):
            podsum.append(f"Część {i}: {w['podsumowanie']}")
        if w.get("ocena"):
            oceny.append(w["ocena"])
    if not uwagi and bledy and len(bledy) == len(czesci):
        raise ValueError("Żadna część dokumentacji nie dała wyniku. " + " | ".join(bledy)[:600])
    kol = {"krytyczna": 0, "istotna": 1, "drobna": 2}
    L = sorted(uwagi.values(), key=lambda u: kol.get(u["waga"], 3))
    uw = (f"Dokumentację sprawdzono w {len(czesci)} częściach (była zbyt obszerna na jedno zapytanie); sprzeczności między dokumentami "
          f"z różnych części mogły nie zostać wykryte" + (f", poza porównaniem z „{kotwica[0]}”" if kotwica else "") + ".")
    if bledy:
        uw += " Nie sprawdzono: " + "; ".join(bledy)[:400]
    return {"podsumowanie": (uw + " " + " ".join(podsum))[:2000], "ocena": "; ".join(dict.fromkeys(oceny))[:80], "uwagi": L,
            "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "w_czesciach": len(czesci)}




RE_PRZEBIEG = re.compile(r"(?i)informacj\w*[ _-]+o[ _-]+kwo[cć]|informacj\w*[ _-]+z[ _-]+otwarci|zawiadomieni\w*[ _-]+o[ _-]+wybor|informacj\w*[ _-]+o[ _-]+wybor"
                         r"|uniewa[zż]nieni|o[ _-]+wyniku|wynik\w*[ _-]+post[eę]powani|protok[oó][lł][ _-]+z[ _-]+(otwarci|post)|odrzuceni\w*[ _-]+ofert|zawart\w*[ _-]+umow")


def oznacz_przebieg(pid, nowe_rel, log):
    """Dokumenty przebiegu postępowania (po otwarciu ofert: informacja o kwocie, z otwarcia, o wyborze, unieważnienie, wynik)
    to nie dokumentacja do sprawdzenia – zostają w projekcie, ale jako „pominięte” (można je włączyć)."""
    przeb = [r for r in nowe_rel if RE_PRZEBIEG.search(os.path.basename(r))]
    if przeb:
        with BLOKADA:
            m = meta(pid)
            m["pominiete"] = sorted(set(m.get("pominiete") or []) | set(przeb))
            zapisz_meta(pid, m)
        log(f"Pominięto w ocenie {len(przeb)} dokumentów przebiegu postępowania (nie są dokumentacją do sprawdzenia): "
            + ", ".join(os.path.basename(x) for x in przeb[:5]) + " – możesz je włączyć w tabeli.")
    return przeb


def praca_pobierz_z_linku(log, pid, url):
    """Dokumenty postępowania z linku (Platforma e-Zamówienia, BZP, BIP, platforma zakupowa) do kroku „Dokumentacja” – ZIP-y rozpakowane."""
    folder = os.path.join(pdir(pid), "dokumenty")
    os.makedirs(folder, exist_ok=True)
    # ponowne pobranie ZASTĘPUJE pliki z poprzedniego pobrania z linku (pliki wgrane ręcznie i przygotowane w programie zostają)
    stare = (meta(pid).get("link_postepowania") or {}).get("lista") or []
    usun = 0
    for r_ in stare:
        sc = os.path.join(folder, r_)
        if os.path.isfile(sc) and not r_.startswith("Przygotowane w programie/"):
            os.remove(sc)
            usun += 1
    for d_, _, f_ in sorted(os.walk(folder), reverse=True):  # puste foldery po rozpakowanych ZIP-ach
        if d_ != folder and not f_ and not os.listdir(d_):
            os.rmdir(d_)
    if usun:
        log(f"Usunięto {usun} plików z poprzedniego pobrania z linku – zastępuję je nowymi.")
    przed = {os.path.relpath(os.path.join(r, n), folder) for r, _, ns in os.walk(folder) for n in ns}
    m_bk = re.search(r"(?i)bazakonkurencyjnosci\.funduszeeuropejskie\.gov\.pl/ogloszenia/(\d+)", url)
    if m_bk:  # Baza Konkurencyjności – załączniki przez jej API (strona jest aplikacją ładowaną skryptem)
        log(f"Link do Bazy Konkurencyjności (ogłoszenie {m_bk.group(1)}) – pobieram załączniki…")
        pl_ = MO.pobierz_zalaczniki_bk(m_bk.group(1), folder, log) or []
        w = {"pliki": pl_, "pominiete": [], "sposob": "Baza Konkurencyjności",
             "uwaga": "" if pl_ else "Ogłoszenie w Bazie Konkurencyjności nie ma załączników do pobrania (albo serwis jest niedostępny) – wgraj pliki ręcznie."}
    else:
        w = BZ.pobierz_z_linku(url, folder, log)
    rozp = 0
    for p_ in list(w["pliki"]):
        if MO.czy_archiwum(p_):
            try:
                wew = MO.rozpakuj_zip(p_, os.path.splitext(p_)[0])
                rozp += len(wew)
                os.remove(p_)
                log(f"Rozpakowano {os.path.basename(p_)}: {len(wew)} plików.")
            except Exception as e:
                log(f"Nie udało się rozpakować {os.path.basename(p_)}: {e}")
    for x in w.get("pominiete") or []:
        log(f"UWAGA – nie pobrano „{x['nazwa']}”: {x['powod']}")
    if w.get("uwaga"):
        log("UWAGA – " + w["uwaga"])
    for rel_ in sorted({os.path.relpath(os.path.join(r, n), folder) for r, _, ns in os.walk(folder) for n in ns} - przed):
        p_ = os.path.join(folder, rel_)
        if re.search(r"(?i)_+(docx?|xlsx?|pdf|odt|rtf)$", rel_) and "." not in os.path.basename(rel_)[-6:]:  # ucięta nazwa w ZIP: „…zamó__docx”
            nowa = re.sub(r"(?i)_+(docx?|xlsx?|pdf|odt|rtf)$", lambda m_: "." + m_.group(1).lower(), p_)
            if not os.path.exists(nowa):
                os.replace(p_, nowa)
                log(f"Poprawiono nazwę pliku: {os.path.basename(nowa)}")
        elif os.path.isfile(p_):
            MO.popraw_rozszerzenie(p_)
    po = {os.path.relpath(os.path.join(r, n), folder) for r, _, ns in os.walk(folder) for n in ns}
    nowe_rel = sorted(po - przed)
    przeb = oznacz_przebieg(pid, nowe_rel, log)
    with BLOKADA:
        m = meta(pid)
        m["link_postepowania"] = {"url": url, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "sposob": w["sposob"],
                                  "pliki": len(nowe_rel), "uwaga": w.get("uwaga", ""), "pominiete": len(w.get("pominiete") or []),
                                  "przebieg": len(przeb), "lista": nowe_rel}
        if m.get("weryfikacja"):
            m["weryfikacja"]["nieaktualna"] = "Dodano dokumenty z linku po sprawdzeniu – sprawdź dokumentację ponownie."
        zapisz_meta(pid, m)
    if not w["pliki"]:
        raise ValueError(w.get("uwaga") or "Nie pobrano żadnych plików.")
    log(f"Gotowe: {len(nowe_rel)} plików ({w['sposob']})" + (f", w tym {rozp} z archiwów" if rozp else "")
        + (f"; do oceny: {len(nowe_rel) - len(przeb)} (dokumenty przebiegu postępowania pominięte)" if przeb else "") + ".")
    return {"pliki": len(w["pliki"])}


@app.post("/api/projekty/<pid>/pobierz-z-linku")
@wymaga_logowania
def pobierz_z_linku(pid):
    url = str((request.json or {}).get("url") or "").strip()
    if not re.match(r"(?i)^https?://", url):
        return jsonify({"blad": "Podaj pełny adres postępowania (https://…)."}), 400
    meta(pid)  # 404 dla nieistniejącego projektu
    return jsonify(uruchom("pobieranie", "Dokumenty z linku do postępowania", praca_pobierz_z_linku, pid, url))


RE_DOSTARCZONE = {"swz": r"(?<![a-ząćęłńóśźż])swz(?![a-ząćęłńóśźż])|specyfikacj|zapytani\w*[ _]ofertow", "ogloszenie": r"og[lł]oszeni",
                  "opz": r"(?<![a-ząćęłńóśźż])opz(?![a-ząćęłńóśźż])|opis\w*[ _]przedmiotu",
                  "umowa": r"umow|(?<![a-z])ppu(?![a-z])|postanowie", "formularz": r"formularz\w*[ _](ofert|cenow)", "oswiadczenia": r"o[sś]wiadcz|wykaz",
                  "protokol": r"protok", "uzasadnienie_trybu": r"uzasadnieni"}


def dostarczone_prawnika(pid):
    """Rodzaje dokumentów, które prawnik już dostarczył (wgrane pliki, poza „Przygotowane w programie”)."""
    nazwy = [x["sciezka"].lower() for x in lista_plikow(pid) if x["uwzglednij"] and not x["sciezka"].startswith("Przygotowane w programie/")]
    return [k for k, wz in RE_DOSTARCZONE.items() if any(re.search(wz, n) for n in nazwy)]


def _komplet_prawnika(m):
    u = PRW.ustawienia(m)
    tw = u["tryb"] if u["tryb"] in KZ.TRYBY_WYBOR else None
    return [[k, ZAM.DOKUMENTY[k][0]] for k in KZ.komplet_dokumentow(tw, "pzp_podstawowy") if k in ZAM.DOKUMENTY]








def tryb_prawnika(u, wartosc=None):
    """Tryb sprawy prawnika do generatora dokumentów (jak kreator, ZAM-01): pola["tryb"] = KOD trybu (pzp_podstawowy, pzp_nieograniczony, pzp_inny,
    ponizej_130, konkurencyjnosc) – od niego zależy reżim dokumentów (SWZ / Pzp / zapytanie poza Pzp); nazwa wybranego trybu tylko jako opis
    (pola["tryb_nazwa"]); procedura unijna (JEDZ, art. 125 ust. 2, art. 266) – z wartości szacunkowej netto, gdy ją podano. „Ustal z dokumentów” – bez trybu."""
    t = u.get("tryb") or "auto"
    if t == "auto":
        return {}
    if t in KZ.TRYBY_WYBOR:
        nazwa, kod = KZ.TRYBY_WYBOR[t]
    else:  # tryby spoza kreatora: sektorowe – Pzp (inny tryb), krajowe – tryb podstawowy poniżej progów UE
        nazwa, kod = PRW.TRYBY.get(t, ""), {"krajowy": "pzp_podstawowy"}.get(t, "pzp_inny")
    w = {"tryb": kod, "tryb_nazwa": nazwa}
    if not kod.startswith("pzp"):
        return w
    if t == "krajowy":
        w["unijny"] = "nie"
    else:
        import kontrola_zam as KO_
        netto = KO_.kwota(wartosc) if str(wartosc or "").strip() else None
        if netto:
            w["unijny"] = "tak" if KZ.tryb_z_wartosci(netto, u.get("przedmiot") or "roboty")[0] == "pzp_nieograniczony" else "nie"
    return w


def praca_przygotuj_prawnik(log, pid, rodzaje, pola_in):
    """Krok 2 „Przygotuj dokumentację”: komplet według trybu z kroku 1, na podstawie własnych wzorów (folder wzory),
    zapisany do dokumentów sprawy – żeby w kroku 3 przeszedł sprawdzenie. Zamawiający – wyłącznie z formularza (nie z Profilu firmy)."""
    m = meta(pid)
    u = PRW.ustawienia(m)
    pola = {k: ZAM.czysc(str(v))[:3000] for k, v in (pola_in or {}).items() if v}
    pola.setdefault("nazwa", m.get("nazwa", ""))
    pola.update(tryb_prawnika(u, pola.get("wartosc")))
    uw = [x for x in ((m.get("weryfikacja") or {}).get("uwagi") or []) if x.get("status") != "odrzucone"][:20]
    if uw:  # dokumenty piszemy tak, żeby nie powtarzały niezgodności znalezionych w materiale prawnika
        pola["uwagi"] = ((pola.get("uwagi") or "") + "\nUWZGLĘDNIJ WYNIKI SPRAWDZENIA MATERIAŁU (nie powtarzaj tych niezgodności, zastosuj właściwe rozwiązania): "
                         + " | ".join(f"{x.get('opis', '')} [{x.get('podstawa', '')}]" + (f" → {x.get('propozycja')}" if x.get("propozycja") else "") for x in uw))[:3000]
    start = time.time()
    praca_dokumentacja(log, pid, pola, rodzaje)
    cel = os.path.join(pdir(pid), "dokumenty", "Przygotowane w programie")
    os.makedirs(cel, exist_ok=True)
    prefiksy = tuple(ZAM.prefiks_dok(r, pw_) + "_" for r in rodzaje for pw_ in (False, True))
    przen = []
    for f in sorted(os.listdir(pdir(pid))):
        sc = os.path.join(pdir(pid), f)
        if f.startswith(prefiksy) and f.endswith(".docx") and os.path.getmtime(sc) >= start - 1:
            shutil.copy2(sc, os.path.join(cel, f))
            przen.append(f)
    with BLOKADA:
        m = meta(pid)
        m["przygotowanie_prawnika"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "pliki": przen, "pola": pola}
        if m.get("weryfikacja"):
            m["weryfikacja"]["nieaktualna"] = "Przygotowano nową dokumentację – sprawdź ją ponownie (krok 3)."
        zapisz_meta(pid, m)
    log(f"Dokumentacja dodana do sprawy ({len(przen)} plików) – folder „Przygotowane w programie”; przejdź do kroku 3.")
    return {"pliki": len(przen)}






def praca_opinia_prawna(log, pid):
    """Opinia prawna (pismo Word) na podstawie uwag ze sprawdzenia dokumentacji – bez ponownego czytania dokumentów."""
    c = cfg()
    c["_log"] = log
    c["_model"] = c.get("model_oferty") or "claude-sonnet-5-5"
    wymagany_klucz(c)
    m = meta(pid)
    w = m.get("weryfikacja")
    if not w or not w.get("uwagi") and not w.get("podsumowanie"):
        raise ValueError("Najpierw sprawdź dokumentację – opinia powstaje na podstawie jej wyników.")
    u = PRW.ustawienia(m)
    log("AI przygotowuje opinię prawną na podstawie ustaleń ze sprawdzenia…")

    def parsuj(txt):
        o = MO.wyciagnij_json(txt)
        if not isinstance(o, dict) or not (o.get("analiza") or o.get("wnioski")):
            raise ValueError("Odpowiedź AI nie zawiera danych opinii.")
        return o
    op = ai_dane(c, PRW.SYSTEM_OPINIA, [{"type": "text", "text": PRW.polecenie_opinii(u, m.get("nazwa", ""), w)}], 12000, log, parsuj)
    autor = ", ".join(x for x in (c.get("firma_nazwa"), c.get("firma_adres")) if x)  # autor opinii = kancelaria z profilu (autor pisma, nie zamawiający)
    nazwa_pl = f"Opinia_prawna_{MO.bezpieczna_nazwa(m.get('nazwa') or 'sprawa')[:50]}.docx"
    PRW.opinia_docx(os.path.join(pdir(pid), nazwa_pl), m.get("nazwa", ""), u, op, autor)
    with BLOKADA:
        m = meta(pid)
        m["opinia_prawna"] = {"plik": nazwa_pl, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "zagadnien": len(op.get("analiza") or [])}
        zapisz_meta(pid, m)
    log(f"Gotowe: opinia prawna – {len(op.get('analiza') or [])} zagadnień, {len(op.get('wnioski') or [])} wniosków.")
    return {"plik": nazwa_pl}


@app.post("/api/projekty/<pid>/opinia-prawna")
@wymaga_logowania
def opinia_prawna(pid):
    if meta(pid).get("typ") != "prawnik":
        return jsonify({"blad": "Opinia prawna jest dostępna w sprawach prawnika."}), 400
    return jsonify(uruchom("opinia_prawna", "Opinia prawna", praca_opinia_prawna, pid))








def praca_dokumentacja(log, pid, pola, rodzaje):
    c = cfg()
    tylko_wzory = all(r == "oswiadczenia" for r in rodzaje)
    if not tylko_wzory:
        wymagany_klucz(c)
    bloki, n = ([], 0) if tylko_wzory else bloki_projektu(pid)
    wz = os.path.join(pdir(pid), "wzory")
    if not tylko_wzory and os.path.isdir(wz):  # własne wzory (prawnika / zamawiającego) – układ i sformułowania do zachowania
        wlasne = [f for f in sorted(os.listdir(wz)) if not f.startswith(".") and not (f.lower().endswith(".pdf") and os.path.exists(os.path.join(wz, os.path.splitext(f)[0] + " (z PDF).docx")))]
        for f in wlasne:
            b_, _, _ = MO.przygotuj_blok_tekstowy(os.path.join(wz, f))
            if b_:
                bloki += [{"type": "text", "text": f"[WŁASNY WZÓR UŻYTKOWNIKA: {f}] – jeśli to wzór dokumentu, który piszesz, zachowaj jego układ, numerację i sformułowania; zmieniaj tylko to, czego wymaga ta sprawa."}] + b_
        if wlasne:
            log(f"Własne wzory jako podstawa ({len(wlasne)}): {', '.join(wlasne)[:200]}")
    R_dok = RZ.reguly(projekt_wspolnoty(meta(pid)))  # nazwy dokumentów i kontekst AI według modułu (reguly_zamowien.py)
    log(f"Dokumenty źródłowe: {n}. Przygotowuję: {', '.join(R_dok.etykieta_dok(r) for r in rodzaje)}")
    wyniki, do_decyzji = {}, []
    if "oswiadczenia" in rodzaje:  # stały wzór z ustawy – natychmiast, bez AI
        nazwa = R_dok.nazwa_pliku("oswiadczenia", meta(pid).get("nazwa", "postepowanie"))
        ile = ZAM.oswiadczenia_docx(os.path.join(pdir(pid), nazwa), pola, meta(pid).get("rodzaj_zamowienia") or "roboty")
        wyniki["oswiadczenia"] = nazwa
        log(f"Gotowe: {nazwa} ({ile} załączników, wzór standardowy – bez AI)")
    rodzaje_ai = [r for r in rodzaje if r != "oswiadczenia"]
    rodzaj_zam = meta(pid).get("rodzaj_zamowienia") or "roboty"
    nazwa_post = meta(pid).get("nazwa", "postepowanie")

    def jeden(r):
        """Jeden dokument AI – wywoływany równolegle dla kompletu (SWZ, OPZ, umowa, formularz piszą się jednocześnie)."""
        et = R_dok.etykieta_dok(r)
        log(f"AI pisze: {et}…")
        tresc = MO.oznacz_dokumenty(list(bloki), MO.ustawienie_cache(c)) + [{"type": "text", "text": ZAM.polecenie_dokumentu(r, pola, c, rodzaj_zam)}]
        ost = [0]

        def postep(k):
            if k - ost[0] > 12000:
                ost[0] = k
                log(f"   {et}: {k // 1000} tys. znaków…")
        txt, powod = MO.claude_stream(c, ZAM.SYSTEM_DOK + R_dok.kontekst_ai, tresc, postep=postep, log=log)
        dane = MO.wyciagnij_json(txt)
        if not dane.get("rozdzialy"):
            log(f"Nie udało się odczytać dokumentu {et} – spróbuj ponownie.")
            return None, []
        nazwa = R_dok.nazwa_pliku(r, nazwa_post)
        ile = ZAM.dokument_docx(os.path.join(pdir(pid), nazwa), dane, pola, c)
        log(f"Gotowe: {nazwa} ({ile} rozdziałów)" + (" – UWAGA: odpowiedź mogła być niepełna" if powod == "max_tokens" else ""))
        dd = [{"dokument": et, "punkt": str(x.get("tekst") or x.get("punkt") or " ".join(map(str, x.values()))) if isinstance(x, dict) else str(x)}
              for x in (dane.get("do_decyzji") or []) if x]
        return nazwa, [d_ for d_ in dd if d_["punkt"].strip()][:40]

    if rodzaje_ai:
        from concurrent.futures import ThreadPoolExecutor
        kont = dict(getattr(_KONTEKST, "__dict__", {}))
        koszt0 = kont.get("koszt_zadania", 0) or 0

        def w_watku(r):  # kontekst konta zadania (ustawienia, klucz, rozliczenie kosztów) w wątku roboczym
            _KONTEKST.__dict__.update(kont)
            _KONTEKST.koszt_zadania = 0.0
            try:
                return jeden(r), _KONTEKST.koszt_zadania
            except Exception as e:  # błąd jednego dokumentu nie przerywa pozostałych; przerwanie przez użytkownika – tak
                if isinstance(e, Przerwano):
                    raise
                log(f"{R_dok.etykieta_dok(r)}: {opis_bledu_zadania(e, 'dokumentacja')}")
                return (None, []), _KONTEKST.koszt_zadania
        if len(rodzaje_ai) > 1:
            log(f"Dokumenty AI piszą się jednocześnie ({len(rodzaje_ai)}) – komplet będzie gotowy po najdłuższym z nich.")
        with ThreadPoolExecutor(max_workers=min(4, len(rodzaje_ai))) as pula:
            fut = {r: pula.submit(w_watku, r) for r in rodzaje_ai}
            koszt = 0.0
            blad = None
            for r in rodzaje_ai:
                try:
                    (nazwa, dd), k_ = fut[r].result()
                except Przerwano as e:
                    blad = e
                    continue
                koszt += k_ or 0
                if nazwa:
                    wyniki[r] = nazwa
                    do_decyzji += dd
        _KONTEKST.koszt_zadania = koszt0 + koszt
        if blad:
            raise blad
    wyniki = [wyniki[r] for r in rodzaje if r in wyniki]
    with BLOKADA:  # uzupełnienie listy, nie zastąpienie – przygotowanie części dokumentów nie „gubi” wcześniejszych
        m = meta(pid)
        prefiksy = tuple(ZAM.prefiks_dok(r, pw_) + "_" for r in rodzaje for pw_ in (False, True))
        stare = [f for f in (m.get("dokumentacja") or {}).get("pliki") or [] if not f.startswith(prefiksy) and os.path.isfile(os.path.join(pdir(pid), f))]
        stare_dd = [x for x in (m.get("dokumentacja") or {}).get("do_decyzji") or []
                    if x.get("dokument") not in {R_dok.etykieta_dok(r) for r in rodzaje}]  # decyzje z dokumentów przygotowanych ponownie – zastąpione
        m["dokumentacja"] = {"pliki": stare + wyniki, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "do_decyzji": stare_dd + do_decyzji}
        zapisz_meta(pid, m)
    return {"pliki": len(wyniki)}


# ============================================================ KREATOR ZAMÓWIENIA (zamawiający)
KAT_WZOROW = SciezkaKonta("wzory_zamawiajacego")


def _kat_wzorow(rodzaj=""):
    k = os.path.join(os.fspath(KAT_WZOROW), rodzaj or "ogolne")
    os.makedirs(k, exist_ok=True)
    return k














# ============================================================ DD / WYCENA NIERUCHOMOŚCI
def _n(m):
    try:
        NR.zastosuj_ustawienia(cfg().get("nier_ustawienia"))  # założenia metod z ustawień konta rzeczoznawcy
    except Exception:
        pass
    return m.setdefault("nier", {"produkty": {"dd": True, "zabudowa": False, "wycena": False}, "dane": {}, "identyfikacja": {}, "ryzyka": [], "pisma": [],
                                 "ogledziny": {"punkty": {}}, "zabudowa": {"parametry": dict(NR.PARAM_DOMYSLNE), "ceny": {}}, "wycena": {"transakcje": [], "cechy": [], "oceny": {}, "punkty": {}},
                                 "dziennik": []})


def _dziennik(n, co):
    n.setdefault("dziennik", []).append({"czas": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "kto": konto_biezace(), "co": co[:300]})
    n["dziennik"] = n["dziennik"][-400:]


def _uniewaznij(n, obszar):
    """Zmiana danych teczki po zatwierdzeniu: punkty kontrolne wyceny zależne od niej – do ponownego potwierdzenia."""
    P = (n.get("wycena") or {}).get("punkty") or {}
    zm = []
    for k in NR.ZALEZNOSCI.get(obszar, []):
        if (P.get(k) or {}).get("status") == "zatwierdzony":
            P[k]["status"] = "do_ponownego"
            zm.append(dict(NR.PUNKTY)[k])
    if zm:
        _dziennik(n, f"Zmiana: {obszar} → do ponownego potwierdzenia: {', '.join(zm)}")










































































def _pow_przedm(n):
    return n["dane"].get("pow_przedmiotu") or n["dane"].get("pow_uzytkowa") or n["dane"].get("pow_dzialki")














def _wl_dodaj_oferty(pid, nowe, log):
    with BLOKADA:
        m = meta(pid)
        n = _n(m)
        wl = n.setdefault("wlasna", {"oferty": []})
        O = wl.setdefault("oferty", [])
        znane = {o.get("url") for o in O if o.get("url")}
        k0 = max([int(o["id"][1:]) for o in O if str(o.get("id", "")).startswith("o") and o["id"][1:].isdigit()] or [0])
        dod, bez_danych, powt = 0, 0, 0
        klucze = {(round(o["cena"]), round(o["pow"], 1)) for o in O}
        for x in nowe:
            o = NR.oferta_porz(x, k0 + dod + 1)
            if not o:
                bez_danych += 1
                continue
            kl = (round(o["cena"]), round(o["pow"], 1))
            if (o.get("url") and o["url"] in znane and kl in klucze) or kl in klucze:  # ta sama oferta (z listy wyników link bywa wspólny)
                powt += 1
                continue
            O.append(o)
            znane.add(o.get("url"))
            klucze.add(kl)
            dod += 1
        wl["wynik"] = None
        _dziennik(n, f"Wycena własna: dodano {dod} ofert")
        zapisz_meta(pid, m)
    log(f"Dodano {dod} ofert porównawczych" + (f"; pominięto {bez_danych} bez ceny lub powierzchni" if bez_danych else "") + (f", {powt} powtórzonych" if powt else "") + ".")
    return dod


def praca_wl_szukaj(log, pid):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    n = _n(meta(pid))
    cm = dict(c, _model=c.get("model_oferty") or c.get("model"))
    dod = 0
    for tura, szerzej in ((1, False), (2, True)):
        n = _n(meta(pid))
        akt = [o for o in (n.get("wlasna") or {}).get("oferty") or [] if not o.get("wykluczona")]
        if tura == 2 and len(akt) >= 10:
            break
        log("Szukam danych rynkowych – ofert sprzedaży podobnych nieruchomości…" if tura == 1
            else f"Mam {len(akt)} ofert – szukam szerzej (cała miejscowość i okolice, powierzchnia ±50%)…")
        txt, _ = CR.claude_z_wyszukiwaniem(cm, NR.SYSTEM, NR.polecenie_ofert_wlasnych(n, szerzej, [o.get("url") for o in akt if o.get("url")]),
                                           max_wyszukan=15, max_tokens=12000, log=log)
        try:
            r = MO.wyciagnij_json(txt) or {}
        except ValueError:
            r = {"oferty": MO.obiekty_z_tekstu(txt, ("cena",))}
        dod += _wl_dodaj_oferty(pid, [dict(o, _zrodlo="wyszukiwanie") for o in r.get("oferty") or [] if isinstance(o, dict)], log)
    if not dod:
        raise ValueError("Nie znaleziono ofert z ceną i powierzchnią – wklej link do listy ofert podobnych nieruchomości albo do pojedynczych ofert, albo dodaj oferty ręcznie.")
    return {"oferty": dod}


def praca_wl_linki(log, pid, linki):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    teksty = []
    for u in linki:
        try:
            dane, _, _ = _pobierz_url(u, timeout=30)
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", dane.decode("utf-8", "ignore"))))
            teksty.append((u, t))
            log(f"Odczytano dane z linku {len(teksty)}.")
        except Exception as e:
            log(f"Nie udało się odczytać jednego z linków – strona mogła zablokować odczyt; dodaj tę ofertę ręcznie.")
    if not teksty:
        raise ValueError("Nie udało się odczytać żadnego linku – strony czasem blokują automatyczny odczyt. Dodaj oferty ręcznie (cena, powierzchnia, lokalizacja).")
    txt, _ = MO.claude_stream(c, NR.SYSTEM, [{"type": "text", "text": NR.polecenie_oferty_z_tekstu(teksty)}], max_tokens=12000, log=log)
    try:
        r = MO.wyciagnij_json(txt) or {}
    except ValueError:
        r = {"oferty": MO.obiekty_z_tekstu(txt, ("cena",))}
    _wl_dodaj_oferty(pid, [dict(o, _zrodlo="link użytkownika") for o in r.get("oferty") or [] if isinstance(o, dict)], log)
    return {"ok": True}


def praca_wl_oceny(log, pid):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    n = _n(meta(pid))
    O = [o for o in (n.get("wlasna") or {}).get("oferty") or [] if not o.get("wykluczona")]
    if not O:
        raise ValueError("Najpierw dodaj oferty porównawcze.")
    log(f"AI ocenia cechy {len(O)} ofert na tle wycenianej nieruchomości…")
    txt, _ = MO.claude_stream(c, NR.SYSTEM, [{"type": "text", "text": NR.polecenie_ocen_wlasnych(n, O)}], max_tokens=8000, log=log)
    r = MO.wyciagnij_json(txt) or {}
    with BLOKADA:
        m = meta(pid)
        n = _n(m)
        wl = n["wlasna"]
        ido = {o["id"]: o for o in wl.get("oferty") or []}
        for x in r.get("oceny") or []:
            o = ido.get(str(x.get("id")))
            if o and isinstance(x.get("cechy"), dict):
                o["oceny"] = {str(k): max(-2, min(2, int(NR._f(v, 0)))) for k, v in x["cechy"].items()}
                o["uzasadnienie"] = str(x.get("uzasadnienie") or "")[:200]
        wl["wynik"] = NR.oblicz_wlasna(n, wl) if len([o for o in wl["oferty"] if not o.get("wykluczona")]) >= 3 else None
        if wl["wynik"] and wl["wynik"].get("blad"):
            wl["wynik"] = None
        _dziennik(n, "Wycena własna: ocena cech ofert (AI)" + (f", wynik {wl['wynik']['wartosc']} zł" if wl.get("wynik") else ""))
        zapisz_meta(pid, m)
    return {"ok": True}


























def MO_liczba(x):
    return NR.liczba_z_tekstu(x)
























































































@app.get("/api/zam/wzory")
@wymaga_logowania
def wzory_lista():
    return jsonify({r: sorted(os.listdir(_kat_wzorow(r))) for r in list(KZ.RODZAJE) + ["ogolne"]})


@app.post("/api/zam/wzory/usun")
@wymaga_logowania
def wzory_usun():
    j = request.json or {}
    p = os.path.join(_kat_wzorow(j.get("rodzaj") if j.get("rodzaj") in list(KZ.RODZAJE) + ["ogolne"] else "ogolne"), os.path.basename(str(j.get("nazwa") or "")))
    if os.path.isfile(p):
        os.remove(p)
    return jsonify({"ok": True})




def _konwertuj_pdf_wzorow(pid, log=None):
    """Wzory w PDF → Word (plik „… (z PDF).docx” obok), żeby propozycje zmian dało się wprowadzić automatycznie."""
    wz = os.path.join(pdir(pid), "wzory")
    wyn = []
    if not os.path.isdir(wz):
        return wyn
    for f in sorted(os.listdir(wz)):
        if not f.lower().endswith(".pdf"):
            continue
        cel = os.path.join(wz, os.path.splitext(f)[0] + " (z PDF).docx")
        if os.path.isfile(cel) and not KZ.docx_ma_tekst(cel):  # wcześniejsza konwersja bez tekstu (skan) – usuń, sprawdzany będzie PDF
            os.remove(cel)
        if os.path.isfile(cel) and os.path.getmtime(cel) >= os.path.getmtime(os.path.join(wz, f)):
            continue
        ok, opis = KZ.pdf_na_docx(os.path.join(wz, f), cel)
        wyn.append({"plik": f, "ok": ok, "opis": opis})
        if log:
            log(f"{f}: {'zamieniono na Word – ' + opis if ok else opis}")
    return wyn




LIMIT_CZASU_DOK = 600  # maks. czas sprawdzania jednego dokumentu [s]


def _z_kontekstem(f):
    """Funkcja do wątku roboczego z kontekstem konta bieżącego zadania (ustawienia, klucz API, limity kosztów)."""
    kont = dict(getattr(_KONTEKST, "__dict__", {}))

    def w(*a, **k):
        _KONTEKST.__dict__.update(kont)
        return f(*a, **k)
    return w


def _odzyskaj_propozycje(txt):
    """Ucięta / sklejona odpowiedź: kompletne propozycje i dopisania wyciągnięte osobno (zamiast odrzucać całą odpowiedź)."""
    props = [o for o in MO.obiekty_z_tekstu(txt, ("cytat",)) if "nowy" in o or "uzasadnienie" in o]
    dop = MO.obiekty_z_tekstu(txt, ("po_cytacie",))
    pod = re.search(r'"podsumowanie"\s*:\s*"((?:[^"\\]|\\.)*)"', txt)
    return {"podsumowanie": pod.group(1) if pod else "", "propozycje": props, "dopisac": dop, "_odzyskane": True} if (props or dop) else None


def _json_ai_z_ponowieniem(c, system, tresc, log, max_tokens, opis, max_kontynuacji=5):
    """Wywołanie AI oczekujące JSON-a: odpowiedź ucięta albo sklejona – odzyskanie kompletnych propozycji; brak danych – druga próba
    z krótszym, ściślejszym poleceniem."""
    txt, powod = MO.claude_stream(c, system, tresc, max_tokens=max_tokens, log=log, max_kontynuacji=max_kontynuacji)
    try:
        r = MO.wyciagnij_json(txt)
        if not r.get("_naprawiony") or r.get("propozycje"):
            return r
    except ValueError:
        pass
    od = _odzyskaj_propozycje(txt)
    if od:
        log(f"{opis}: odpowiedź AI ucięta – odzyskano {len(od['propozycje']) + len(od['dopisac'])} kompletnych propozycji.")
        return od
    log(f"{opis}: AI odpowiedziało tekstem zamiast danych ({txt.strip()[:120]!r}) – ponawiam z krótszym poleceniem…")
    tresc2 = tresc[:-1] + [{"type": "text", "text": tresc[-1]["text"] + "\n\nWAŻNE: odpowiedz WYŁĄCZNIE obiektem JSON zaczynającym się od znaku { – "
                                                                    "bez żadnego tekstu przed i po. Maksymalnie 12 najważniejszych propozycji, cytaty do 250 znaków."}]
    txt, _ = MO.claude_stream(c, system, tresc2, max_tokens=max_tokens, log=log, max_kontynuacji=max_kontynuacji)
    try:
        return MO.wyciagnij_json(txt)
    except ValueError:
        od = _odzyskaj_propozycje(txt)
        if od:
            return od
        raise


MODELE_PRZEGLADU = {"standardowy": ("model_oferty", "claude-sonnet-5-5", 16000, 20),
                    "dokladny": ("model_dokladny", "claude-opus-5-5", 16000, 20)}  # (klucz ustawień, model domyślny, limit odpowiedzi, maks. propozycji) – bez modelu tańszego: jakość analizy prawnej ma pierwszeństwo














# pola dokumentacji ↔ dane kreatora / wgranych dokumentów (źródło przy każdym polu)
MAPA_DOK_KREATOR = {"wadium": "warunki.wadium", "gwarancja": "warunki.gwarancja", "kryteria": "warunki.kryteria", "wynagrodzenie": "warunki.wynagrodzenie",
                    "platnosci": "warunki.platnosci", "kary": "warunki.kary", "zabezpieczenie": "warunki.zabezpieczenie", "platforma": "warunki.platforma",
                    "warunki": "warunki.warunki", "kontakt": "warunki.kontakt", "znak": "co.znak", "zamawiajacy": "co.zamawiajacy", "termin_ofert": "co.termin_ofert",
                    "termin_realizacji": "potrzeba.termin", "wartosc": "wartosc", "nazwa": "co.nazwa", "zakres": "co.opis"}


def dokumentacja_domyslne(pid, m):
    """Pola formularza „Sporządzenie dokumentacji” z danych zamówienia: kreator, wgrane dokumenty, kosztorys inwestorski – ze źródłem."""
    if m.get("typ") not in INWESTORSKIE:
        return {"pola": {}, "zrodla": {}}
    st = _kreator_stan(pid)
    K = st["K"]
    pola = KZ.pola_dokumentacji(dict(K, warunki=st["warunki"]), st["projekt"]["nazwa"], st["netto"], "prywatny" if st.get("prywatny") else st["tryb"])
    pola["zamawiajacy"] = (K.get("zamawiajacy") or "").strip()
    pola = {k: v for k, v in pola.items() if v not in (None, "")}
    imp = (K.get("import") or {}).get("pola") or {}
    zr = {}
    for k in pola:
        klucz = MAPA_DOK_KREATOR.get(k)
        if k == "termin_realizacji" and "potrzeba.termin" not in imp and "potrzeba.okres" in imp:
            klucz = "potrzeba.okres"
        if klucz in imp:
            zr[k] = ("⚠ do aktualizacji – " if imp[klucz].get("do_aktualizacji") else "") + "z dokumentu: " + imp[klucz].get("zrodlo", "")
        elif k == "wartosc" and st.get("netto_zrodlo"):
            zr[k] = {"szacowanie": "z szacowania wartości (notatka z szacowania)", "dokumenty": "z dokumentów zamawiającego",
                     "szacunek_ai": "szacunek kosztów (AI) – zamawiający prywatny", "reczna": "wpisana – bez udokumentowanej podstawy",
                     "budzet": "budżet orientacyjny"}.get(st["netto_zrodlo"], "")
        elif k == "tryb":
            zr[k] = "dobrany według wartości (" + st["tryb_opis"] + ")"
        elif k.startswith(("wadium", "gwarancja", "kryteria", "wynagrodzenie", "platnosci", "kary", "zabezpieczenie", "platforma", "warunki")) and not (K.get("warunki") or {}).get(k):
            zr[k] = "propozycja programu (kreator – warunki)"
        else:
            zr[k] = "z kreatora zamówienia"
    return {"pola": pola, "zrodla": zr}


@app.post("/api/projekty/<pid>/dokumentacja")
@wymaga_logowania
def dokumentacja(pid):
    j = request.json or {}
    pola = {k: ZAM.czysc(v)[:3000] for k, v in (j.get("pola") or {}).items()}
    rodzaje = [r for r in j.get("dokumenty", []) if r in ZAM.DOKUMENTY]
    if not rodzaje:
        return jsonify({"blad": "Zaznacz, które dokumenty przygotować."}), 400
    if not pola.get("nazwa") or not pola.get("zakres"):
        return jsonify({"blad": "Podaj nazwę zamówienia i opis zakresu."}), 400
    with BLOKADA:
        m = meta(pid)
        m["dokumentacja_pola"] = pola
        if m.get("typ") in INWESTORSKIE:  # te same dane w kreatorze – bez dwóch różnych wersji zamówienia
            K = m.setdefault("kreator", {"rodzaj": m.get("rodzaj_zamowienia") or "roboty", "sciezka": "nowe", "krok": 1})
            for kd, kk in MAPA_DOK_KREATOR.items():
                v = pola.get(kd)
                if not v:
                    continue
                if kk.startswith("warunki."):
                    K.setdefault("warunki", {})[kk[8:]] = v
                elif kk.startswith("potrzeba."):
                    K.setdefault("potrzeba", {})[kk[9:]] = v
                elif kk == "co.nazwa":
                    m["nazwa"] = v[:90]
                elif kk == "co.opis":
                    K["opis"] = K.get("opis") or v
                elif kk == "wartosc":
                    if not (m.get("oferta") or {}).get("netto"):
                        K["wartosc_reczna"] = re.sub(r"[^0-9.]", "", v.replace(" ", "").replace(",", "."))[:20]
                else:
                    K[kk[3:]] = v
        zapisz_meta(pid, m)
    return jsonify(uruchom("dokumentacja", "Sporządzanie dokumentacji przetargowej", praca_dokumentacja, pid, pola, rodzaje))


def _plik_dokumentu(pid, nazwa_z_uwagi):
    """Plik w dokumentach projektu odpowiadający nazwie z uwagi (dokładnie albo po podobieństwie nazwy)."""
    pl = [p["sciezka"] for p in lista_plikow(pid)]
    n_ = W.norm(str(nazwa_z_uwagi or "").split(",")[0].split(" i ")[0])
    for p in pl:
        if W.norm(os.path.basename(p)) == n_ or W.norm(os.path.splitext(os.path.basename(p))[0]) == W.norm(os.path.splitext(n_)[0]):
            return p
    return next((p for p in pl if n_ and (W.norm(os.path.splitext(os.path.basename(p))[0])[:18] in n_ or n_[:18] in W.norm(os.path.basename(p)))), None)


def _word_dla(pid, rel):
    """Ścieżka Worda do wprowadzania zmian: .docx bez zmian, PDF z tekstem → kopia „(z PDF).docx”, skan → None."""
    sc = os.path.join(pdir(pid), "dokumenty", rel)
    if rel.lower().endswith(".docx"):
        return sc, ""
    if rel.lower().endswith(".pdf"):
        kat = os.path.join(pdir(pid), "dokumenty_word")
        os.makedirs(kat, exist_ok=True)
        cel = os.path.join(kat, os.path.splitext(os.path.basename(rel))[0] + " (z PDF).docx")
        if not (os.path.isfile(cel) and os.path.getmtime(cel) >= os.path.getmtime(sc) and KZ.docx_ma_tekst(cel)):
            ok, opis = KZ.pdf_na_docx(sc, cel)
            if not ok:
                return None, opis
        return cel, "zamieniony z PDF na Word"
    return None, "format pliku nie pozwala na automatyczne zmiany (wgraj Word albo PDF z tekstem)"






_STRONY_PDF = {}


@app.get("/api/projekty/<pid>/tokeny")
@wymaga_logowania
def tokeny_projektu(pid):
    """Szacunek tokenów dokumentów projektu wysyłanych do AI: całość (kosztorys) i zadania tekstowe (bez rysunków, skany do 30 stron)."""
    d = pdir(pid)
    try:
        tx = OD.teksty(d, ("dokumenty",))
    except Exception:
        tx = {}
    pliki, cal, tekstowe, rys = [], 0, 0, 0
    for p in lista_plikow(pid):
        if not p["uwzglednij"]:
            continue
        rel, sc = "dokumenty/" + p["sciezka"], os.path.join(d, "dokumenty", p["sciezka"])
        t = (tx.get(rel) or {}).get("tekst") or ""
        if t.strip():
            n, rodz = int(len(t) / 3.5), "tekst"
            nt = n
        elif sc.lower().endswith(".pdf"):
            k = (sc, os.path.getmtime(sc))
            if k not in _STRONY_PDF:
                try:
                    import pypdf
                    _STRONY_PDF[k] = len(pypdf.PdfReader(sc).pages)
                except Exception:
                    _STRONY_PDF[k] = 1
            st = _STRONY_PDF[k]
            n = st * 1500
            rysunek = bool(MO.RE_RYSUNEK.search(os.path.splitext(os.path.basename(sc))[0])) and MO.POMIJAJ_RYSUNKI["wlaczone"]
            rodz = "rysunek" if rysunek else "skan"
            nt = 0 if rysunek else min(st, 30) * 1500 if MO.POMIJAJ_RYSUNKI["wlaczone"] else n
            rys += 1 if rysunek else 0
        elif sc.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            n, nt, rodz = 1500, 1500, "obraz"
        else:
            n = nt = int(p["rozmiar"] / 6)
            rodz = "inne"
        cal += n
        tekstowe += nt
        pliki.append({"plik": p["sciezka"], "tokeny": n, "rodzaj": rodz})
    return jsonify({"calosc": cal, "tekstowe": tekstowe, "rysunki_pominiete": rys, "pliki": sorted(pliki, key=lambda x: -x["tokeny"])[:15]})


# ============================================================ czat z dokumentami
def fragmenty_do_pytania(pid, dozwolone, pytanie, log=None, ile=12, dl=1600):
    """Wyszukiwanie fragmentów dokumentów pasujących do pytania (tekst z pamięci odwołań) – do AI trafia kilkanaście
    fragmentów zamiast całych dokumentów. Pusta lista = brak trafień (wtedy całe dokumenty)."""
    try:
        tx = OD.teksty(pdir(pid), ("dokumenty",))
    except Exception:
        return []
    slowa = [w[:6] for w in W.norm(pytanie).split() if len(w) >= 4 and w not in ("jakie", "jaki", "jaka", "czy", "ktore", "gdzie", "kiedy", "dokument", "dokumentach")]
    if not slowa:
        return []
    kand = []
    for rel, d in tx.items():
        if rel not in dozwolone or not d.get("tekst"):
            continue
        t, strony = d["tekst"], d.get("strony") or [0]
        for start in range(0, len(t), dl * 3 // 4):
            fr = t[start:start + dl]
            n = W.norm(fr)
            pkt = sum(n.count(w) for w in slowa) + 3 * sum(1 for w in set(slowa) if w in n)
            if pkt:
                strona = max([i + 1 for i, s0 in enumerate(strony) if s0 <= start] or [1])
                kand.append((pkt, rel, strona, start, fr))
    if not kand:
        return []
    kand.sort(key=lambda x: -x[0])
    wyb, zajete = [], set()
    for pkt, rel, strona, start, fr in kand:
        k = (rel, start // dl)
        if k in zajete:
            continue
        zajete.add(k)
        wyb.append({"type": "document", "title": f"{os.path.basename(rel)} – str. {strona}", "citations": {"enabled": True},
                    "source": {"type": "text", "media_type": "text/plain", "data": fr}})
        if len(wyb) >= ile:
            break
    if log:
        log(f"Do AI trafia {len(wyb)} najlepiej pasujących fragmentów dokumentów (zamiast całych dokumentów).")
    return wyb









def _f_liczba(v):
    return liczba(v, 0.0, 4)




def _klucz_pozycji(opis, jm):
    return W.norm(str(opis))[:160] + "|" + W.norm(str(jm or ""))[:10]


def _pamiec_cen_dla(pozycje):
    """Ostatnio oferowane ceny za te same lub bardzo podobne pozycje (ta sama j.m., ≥ 60% wspólnych słów)."""
    pam = czytaj(F_CENY_DOS, {}) or {}
    if not pam:
        return [None] * len(pozycje)
    sl = lambda t: {w for w in W.norm(t).split() if len(w) > 2}
    wyn = []
    for p_ in pozycje:
        k_ = _klucz_pozycji(p_.get("opis"), p_.get("jm"))
        if k_ in pam:
            wyn.append(dict(pam[k_], podobienstwo=1.0))
            continue
        a, jm = sl(p_.get("opis")), W.norm(str(p_.get("jm") or ""))[:10]
        best, bs = None, 0.0
        for v in pam.values():
            if W.norm(str(v.get("jm") or ""))[:10] != jm:
                continue
            b = sl(v.get("opis"))
            if a and b:
                sc = len(a & b) / len(a | b)
                if sc > bs:
                    best, bs = v, sc
        wyn.append(dict(best, podobienstwo=round(bs, 2)) if best and bs >= 0.6 else None)
    return wyn




SYSTEM_ZALACZNIKI = ("Przygotowujesz dokumenty oferty w zamówieniu publicznym (roboty budowlane, dostawy, usługi) dokładnie według SWZ "
                     "i ogłoszenia. Przepisujesz wzory formularzy i oświadczeń z dokumentów zamawiającego (numeracja załączników, tytuły, treść, "
                     "wszystkie punkty i pola wyboru) i wypełniasz je danymi wykonawcy i oferty. NIE dodajesz dokumentów, których zamawiający "
                     "nie wymaga (np. oświadczeń o kierowniku budowy przy dostawach). Czego nie wiesz – wstaw [UZUPEŁNIJ: …]. "
                     "Odpowiadasz WYŁĄCZNIE JSON-em.")


def praca_zalaczniki_dostawcy(log, pid):
    """Formularz ofertowy i oświadczenia wymagane w TYM ogłoszeniu – na podstawie wzorów z SWZ, wypełnione danymi firmy i ceną.
    Dostawy i usługi oraz roboty budowlane (przy robotach podstawowy formularz z programu zostaje, gdy AI nie przygotuje dokumentów)."""
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    c = cfg()
    m = meta(pid)
    d = pdir(pid)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), {})
    dostawca = jest_dostawca(m)
    A = m.get("analiza_dostawcy") or {}
    P = (A.get("postepowanie") or {}) if dostawca else dict(dane.get("postepowanie") or {})
    wym = (A.get("wymagane_dokumenty") or []) if dostawca else (dane.get("zalaczniki_do_oferty") or [])
    if m.get("gwarancja_oferty"):  # okres gwarancji wybrany przez wykonawcę (decyzja handlowa) – nie z propozycji AI
        P["gwarancja_mies"] = m["gwarancja_oferty"]
    firma = {k: c.get(k, "") for k in ("firma_nazwa", "firma_adres", "firma_nip", "firma_regon", "firma_krs", "firma_email", "firma_tel",
                                         "firma_telefon", "firma_osoba", "firma_reprezentant", "firma_wielkosc")}
    oferta = {"netto": dane.get("netto"), "vat": dane.get("vat"), "brutto": dane.get("brutto"),
              "pozycje": [(p.get("opis"), p.get("jm"), p.get("ilosc"), p.get("cena")) for dz in dane.get("dzialy", []) for p in dz.get("pozycje", [])][:60]}
    dokumenty, do_dolaczenia = [], []
    pliki = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(d, "dokumenty")) for f in fs]
    if pliki and (c.get("api_key") or c.get("api_key_alt")):
        bloki = [b for _, bl, _ in bloki_dokumentow(pid, log) for b in bl]
        log(f"AI przygotowuje formularz ofertowy i oświadczenia wymagane w ogłoszeniu ({len(wym)} pozycji na liście wymaganych dokumentów)…")
        pol = ("Na podstawie dokumentów zamówienia przygotuj DOKUMENTY OFERTY, które wykonawca składa wraz z ofertą: formularz ofertowy oraz "
               "wymagane oświadczenia i zobowiązania – TYLKO te, których wymaga zamawiający, według WZORÓW z SWZ (ta sama numeracja załączników). "
               "Nie przygotowuj formularza cenowego, kosztorysu ani tabeli elementów scalonych (są osobno w Excelu) ani dokumentów, które wykonawca uzyskuje sam (certyfikaty, KRS, "
               "foldery producenta, referencje) – te wypisz w do_dolaczenia. Przedmiotowe środki dowodowe (art. 106–107 Pzp: karty katalogowe, "
               "certyfikaty, opisy techniczne) składa się WRAZ Z OFERTĄ – wypisz je w do_dolaczenia. Podmiotowych środków dowodowych składanych dopiero na "
               "wezwanie zamawiającego (art. 126 ust. 1 – od progów unijnych, art. 274 ust. 1 – poniżej progów; np. KRS, zaświadczenia ZUS i US, KRK, "
               "wykazy z dowodami) nie przygotuj – wypisz je w na_wezwanie.\n"
               f"WYMAGANE DOKUMENTY (z analizy): {json.dumps(wym, ensure_ascii=False)}\n"
               f"DANE WYKONAWCY: {json.dumps(firma, ensure_ascii=False)}\n"
               f"OFERTA: cena netto {oferta['netto']} zł, VAT {oferta['vat']}, brutto {oferta['brutto']} zł; termin realizacji: {P.get('termin_wykonania', '')}; "
               f"gwarancja: {P.get('gwarancja_mies', '')}; zamawiający: {P.get('zamawiajacy_nazwa', '')}; postępowanie: {P.get('nazwa_zamowienia', '')} "
               f"nr {P.get('numer', '')}.\n"
               'Zwróć JSON: {"dokumenty": [{"tytul": "Załącznik nr 1 do SWZ – Formularz ofertowy", "akapity": ["tekst akapitu z wypełnionymi danymi", "…"], '
               '"tabela": [["nagłówek 1", "nagłówek 2"], ["…", "…"]] albo [], "podpis": true}], "do_dolaczenia": ["…"], "na_wezwanie": ["…"]}')
        try:
            txt, _ = MO.claude_stream(c, SYSTEM_ZALACZNIKI, MO.oznacz_dokumenty(bloki, MO.ustawienie_cache(c)) + [{"type": "text", "text": pol}],
                                      max_tokens=16000, log=log)
            w = MO.wyciagnij_json(txt)
            dokumenty = [x for x in (w.get("dokumenty") or []) if isinstance(x, dict) and x.get("tytul")]
            do_dolaczenia = [str(x) for x in (w.get("do_dolaczenia") or [])][:30]
            na_wezwanie = [str(x) for x in (w.get("na_wezwanie") or [])][:30]
        except Exception as e:
            log(f"AI nie przygotowało załączników ({e}) – tworzę podstawowy formularz ofertowy.")
            na_wezwanie = []
    else:
        na_wezwanie = []
    if not dokumenty and not dostawca:  # roboty: zostaje podstawowy formularz z programu (przygotowany z kosztorysem)
        log("Zostaje podstawowy formularz ofertowy z programu – sprawdź go ze wzorem z SWZ.")
        return {"dokumenty": 0}
    if not dokumenty:  # zapasowo: podstawowy formularz ofertowy (bez szablonów budowlanych)
        dokumenty = [{"tytul": "FORMULARZ OFERTOWY", "akapity": [
            f"Zamawiający: {P.get('zamawiajacy_nazwa') or (m.get('przetarg') or {}).get('zamawiajacy', '[UZUPEŁNIJ]')}",
            f"Dotyczy postępowania: {P.get('nazwa_zamowienia') or m.get('nazwa', '')}{(' nr ' + P['numer']) if P.get('numer') else ''}",
            f"Wykonawca: {firma['firma_nazwa'] or '[UZUPEŁNIJ]'}, {firma['firma_adres'] or '[UZUPEŁNIJ]'}, NIP {firma['firma_nip'] or '[UZUPEŁNIJ]'}",
            f"Oferujemy wykonanie przedmiotu zamówienia za cenę netto {MO.zl(oferta['netto'] or 0)}, brutto {MO.zl(oferta['brutto'] or 0)}, "
            "zgodnie z formularzem cenowym stanowiącym załącznik do oferty.",
            f"Termin realizacji: {P.get('termin_wykonania') or '[UZUPEŁNIJ]'}. Okres gwarancji: {P.get('gwarancja_mies') or '[UZUPEŁNIJ]'}.",
            "Oświadczamy, że zapoznaliśmy się z SWZ i projektowanymi postanowieniami umowy, akceptujemy je bez zastrzeżeń i uważamy się "
            "za związanych ofertą przez okres wskazany w SWZ."], "tabela": [], "podpis": True}]
    import trasy_projekty_wykonawcy as _TW
    podpis = {"unijne": "kwalifikowany podpis elektroniczny osoby upoważnionej (art. 63 ust. 1 Pzp)",
              "krajowe": "kwalifikowany podpis elektroniczny / podpis zaufany / osobisty osoby upoważnionej (art. 63 ust. 2 Pzp)",
              "poza": "podpis osoby upoważnionej – w formie wskazanej w zapytaniu ofertowym"}.get(
        _TW.podpis_oferty(P)["rodzaj"], "kwalifikowany podpis elektroniczny osoby upoważnionej – od progów UE wyłącznie ten; poniżej progów także podpis zaufany / osobisty")
    doc = MO._doc()
    for i, x in enumerate(dokumenty):
        if i:
            doc.add_page_break()
        MO._akapit(doc, str(x["tytul"]), pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
        for a in x.get("akapity") or []:
            MO._akapit(doc, str(a))
        tab = [r for r in (x.get("tabela") or []) if isinstance(r, list) and r]
        if len(tab) > 1:
            MO._tabela(doc, [[str(k) for k in r] for r in tab])
        if x.get("podpis", True):
            MO._akapit(doc, f"\n\n..........................................\n({podpis})",
                       rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _, pf, _ = pliki_oferty(m)
    doc.save(os.path.join(d, pf))
    with BLOKADA:
        m = meta(pid)
        m["pliki_oferty"] = [x for x in [m.get("kosztorys"), pf] if x] if dostawca else \
            [x for x in (m.get("pliki_oferty") or []) if x != pf] + [pf]
        m["oferta_przygotowana"] = True
        m["zalaczniki_dostawcy"] = {"dokumenty": [x["tytul"] for x in dokumenty], "do_dolaczenia": do_dolaczenia, "na_wezwanie": na_wezwanie,
                                    "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        zapisz_meta(pid, m)
    log(f"Gotowe: {len(dokumenty)} dokumentów do podpisu; do dołączenia przez wykonawcę: {len(do_dolaczenia)}; na wezwanie: {len(na_wezwanie)}.")
    return {"dokumenty": len(dokumenty)}


SYSTEM_ANALIZA_DOSTAWCY = ("Jesteś specjalistą od zamówień publicznych, który przygotowuje oferty firm dostawczych i usługowych. Czytasz SWZ, "
                           "opis przedmiotu zamówienia, formularze i wzór umowy. Piszesz po polsku, konkretnie, nie zmyślasz – brak danych = pusty. "
                           "Odpowiadasz WYŁĄCZNIE JSON-em.")


def termin_zwiazania_tekst(tekst, termin_skladania):
    """„30 dni od upływu terminu składania ofert” + termin składania → data końca związania ofertą (pierwszy dzień = dzień upływu terminu
    składania ofert, art. 220 ust. 1 i art. 307 ust. 1 Pzp) – liczona przez program, nie przez AI."""
    m_ = re.search(r"(\d{1,3})\s*dni", str(tekst or ""))
    try:
        d0 = dt.date.fromisoformat(str(termin_skladania or "")[:10])
    except ValueError:
        return tekst
    if not m_:
        return tekst
    n = int(m_.group(1))
    return f"{n} dni od upływu terminu składania ofert, tj. do {d0 + dt.timedelta(days=n - 1):%d.%m.%Y}"


def koszty_pracy_oferty(m, pozycje=None):
    """Usługi: czy cena netto pokrywa minimalne koszty pracy personelu wymaganego w SWZ (umowa o pracę, płaca minimalna) – liczone kalkulatorem
    kosztów pracy programu. None, gdy SWZ nie podaje liczby osób albo okresu."""
    A = m.get("analiza_dostawcy") or {}
    os_ = A.get("personel") or {}
    osoby = MO_liczba(os_.get("etaty")) or MO_liczba(os_.get("osoby"))
    mies = MO_liczba(os_.get("okres_mies"))
    od = None
    mm = re.findall(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", str((A.get("postepowanie") or {}).get("termin_wykonania") or ""))
    try:
        daty = [dt.date(int(y), int(mo), int(d)) for d, mo, y in mm[:2]]
    except ValueError:
        daty = []
    if daty:
        od = daty[0].isoformat()  # płaca minimalna z okresu świadczenia usługi, nie z dnia składania oferty
    if not mies and len(daty) == 2:
        mies = round(((daty[1] - daty[0]).days + 1) / 30.44)
    if not osoby or not mies or m.get("rodzaj_zamowienia") != "uslugi":
        return None
    poz = pozycje if pozycje is not None else (m.get("formularz_cenowy") or [])
    netto = round(sum((MO_liczba(p.get("ilosc")) or 0) * (MO_liczba(p.get("cena")) or 0) for p in poz), 2)
    w = RY.kalkulator_pracy({"osoby": osoby, "miesiace": mies, "od": od or (A.get("postepowanie") or {}).get("termin_skladania")})
    minimum = w["minimum_netto"]
    pokr = round(netto / minimum * 100, 1) if minimum and netto else None
    ocena = ("" if not netto else
             f"Cena NIE pokrywa minimalnych kosztów pracy {osoby:g} os. na umowę o pracę przez {mies:g} mies. ({PR.liczba_pl(minimum)} zł netto) – "
             f"ryzyko odrzucenia oferty jako rażąco niskiej (art. 224 ust. 3 pkt 4, art. 226 ust. 1 pkt 8 Pzp)." if netto < minimum else
             "Cena pokrywa minimalne koszty pracy, ale zostaje mniej niż 10% na środki, sprzęt, koszty ogólne i zysk." if netto < minimum * 1.1 else
             f"Cena pokrywa minimalne koszty pracy {osoby:g} os. z zapasem.")
    if w.get("uwagi") and ocena:
        ocena += " " + " ".join(w["uwagi"])
    return {"osoby": osoby, "miesiace": mies, "minimum_netto": minimum, "na_etat_mies": w["na_etat_mies"]["razem"], "oferta_netto": netto,
            "placa_minimalna": w["parametry"]["placa_minimalna"],
            "pokrycie_proc": pokr, "ocena": ocena, "za_nisko": bool(netto and netto < minimum)}


def polecenie_analizy_dostawcy(rodzaj):
    return ("Przeanalizuj dokumenty zamówienia na " + ("DOSTAWY" if rodzaj == "dostawy" else "USŁUGI") + " z perspektywy oferenta. Zwróć JSON:\n"
            '{"podsumowanie": "3–5 zdań: co, dla kogo, skala, najważniejsze warunki", '
            '"postepowanie": {"nazwa_zamowienia": "", "numer": "", "zamawiajacy_nazwa": "", "zamawiajacy_nip": "", "termin_skladania": "RRRR-MM-DD GG:MM", '
            '"termin_wykonania": "termin realizacji / okres umowy", "termin_zwiazania": "", "wadium": "kwota albo brak", "gwarancja_mies": "", '
            '"sposob_zlozenia": "platforma / adres / e-mail, link jeśli podany", "kryteria_oceny": ["cena 60%", "…"], '
            '"tryb": "tryb postępowania z dokumentów (np. tryb podstawowy, przetarg nieograniczony, zapytanie ofertowe)", '
            '"ogloszenie": "BZP | Dziennik Urzędowy UE | brak (zapytanie ofertowe / poza Pzp) – gdzie opublikowano ogłoszenie"}, '
            '"co_zaoferowac": [{"opis": "towar lub usługa z wymaganymi parametrami", "jm": "", "ilosc": liczba, "wymagania": "kluczowe wymagania, termin, gwarancja – krótko", '
            '"czesc": "numer części, jeśli zamówienie jest podzielone"}], '
            '"wymagane_dokumenty": ["TYLKO dokumenty składane WRAZ Z OFERTĄ: formularz ofertowy, formularz cenowy, oświadczenie z art. 125, przedmiotowe środki dowodowe (karty katalogowe, certyfikaty), pełnomocnictwo, wadium – według SWZ", "…"], '
            '"dokumenty_na_wezwanie": ["podmiotowe środki dowodowe składane dopiero na wezwanie zamawiającego (art. 126 – od progów unijnych, art. 274 – poniżej): KRS/CEIDG, zaświadczenia ZUS i US, informacja z KRK, wykazy dostaw / usług z dowodami, polisa OC – według SWZ", "…"], '
            '"warunki_udzialu": ["…"], '
            '"personel": {"osoby": "minimalna liczba osób wymagana do realizacji (liczba) albo null", "etaty": "liczba etatów, jeśli podana, albo null", '
            '"umowa_o_prace": true/false/null, "okres_mies": "liczba miesięcy świadczenia usługi albo null"}, '
            '"ryzyka": ["kary umowne, krótkie terminy, nietypowe wymagania – krótko"]}\n'
            "Błędów i sprzeczności w dokumentach NIE wypisuj tutaj – sprawdza je osobne, dokładne zadanie. "
            "Pozycje co_zaoferowac przepisz z formularza cenowego / asortymentowo-cenowego zamawiającego (dokładnie: kolejność, j.m., ilości); gdy go brak – "
            "z opisu przedmiotu zamówienia. NIE podawaj cen. " + OD.INSTRUKCJA)




def bloki_dokumentow(pid, log):
    """Dokumenty projektu do AI: tylko pliki „uwzględnij” z kroku 1, bez cichych limitów; pliki nieodczytane wypisane w dzienniku."""
    pliki = bloki_projektu_pliki(pid, log)
    wszystkie = [x["sciezka"] for x in lista_plikow(pid) if x["uwzglednij"]]
    brak = [os.path.basename(x) for x in wszystkie if os.path.basename(x) not in {n for n, _, _ in pliki}]
    if brak and log:
        log(f"UWAGA – nie odczytano {len(brak)} plików (brak tekstu albo nieobsługiwany format): {', '.join(brak[:8])}" + (" …" if len(brak) > 8 else ""))
    return pliki


def polacz_analizy_dostawcy(wyniki, nazwy_czesci):
    """Analizy z części dokumentacji → jedna: listy bez powtórzeń, dane postępowania uzupełniane z kolejnych części."""
    klucz = lambda x: re.sub(r"\s+", " ", str((x.get("opis") or x.get("nazwa") or x.get("dokument") or json.dumps(x, ensure_ascii=False))
                                            if isinstance(x, dict) else x)).strip().lower()[:200]
    a = {}
    for w in wyniki:
        for k, v in w.items():
            if isinstance(v, list):
                obecne = {klucz(x) for x in a.setdefault(k, [])}
                for x in v:
                    if klucz(x) not in obecne:
                        a[k].append(x)
                        obecne.add(klucz(x))
            elif isinstance(v, dict):
                d = a.setdefault(k, {})
                for kk, vv in v.items():
                    if vv not in (None, "", [], {}) and d.get(kk) in (None, "", [], {}):
                        d[kk] = vv
            elif k == "podsumowanie" and v:
                a["podsumowanie"] = (a.get("podsumowanie", "") + " " + str(v)).strip()
            elif v not in (None, "") and a.get(k) in (None, ""):
                a[k] = v
    a["podsumowanie"] = (f"Dokumentację przeanalizowano w {len(nazwy_czesci)} częściach (była zbyt obszerna na jedno zapytanie). "
                         + a.get("podsumowanie", ""))[:3000]
    a["w_czesciach"] = len(nazwy_czesci)
    return a




WAGA_DOSTAWCY = {"krytyczna": "wysoka", "istotna": "średnia", "drobna": "niska"}


def praca_bledy_dostawcy(log, pid):
    """Błędy w dokumentacji przetargowej – ZAWSZE osobnym, dokładnym sprawdzeniem (ten sam mechanizm co „Wykryj błędy”: cytaty,
    odwołania, ponowienia, części przy dużej dokumentacji). Wynik trafia do analizy (sekcja „Błędy i niejasności”) i do raportu.
    Gdy sprawdzenie się nie uda – zapisany jest błąd (widoczny w programie), a nie fałszywe „nie znaleziono błędów”."""
    try:
        praca_weryfikacja(log, pid, "")
        uw = (meta(pid).get("weryfikacja") or {}).get("uwagi") or []
        bl = [{"opis": u.get("opis", ""), "gdzie": " – ".join(x for x in (u.get("dokument"), u.get("miejsce")) if x), "dokument": u.get("dokument", ""),
               "miejsce": u.get("miejsce", ""), "cytat": u.get("cytat", ""), "waga": WAGA_DOSTAWCY.get(u.get("waga"), "średnia"),
               "pytanie_do_zamawiajacego": u.get("pytanie_do_zamawiajacego", ""), "propozycja": u.get("propozycja", ""), "odw": u.get("odw"),
               "z_weryfikacji": True} for u in uw if u.get("status") != "odrzucone"]
        stan = {"bledy_status": "ok", "bledy_data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "bledy_blad": ""}
    except Exception as e:
        bl, stan = None, {"bledy_status": "blad", "bledy_blad": str(e)[:500], "bledy_data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        log(f"Wykrywanie błędów nie powiodło się: {e}")
    with BLOKADA:
        m = meta(pid)
        a = m.get("analiza_dostawcy") or {}
        if bl is not None:
            a["bledy"] = bl
        a.update(stan)
        m["analiza_dostawcy"] = a
        zapisz_meta(pid, m)
    if bl is not None:
        log(f"Błędy w dokumentacji: {len(bl)} (wysokiej wagi: {sum(1 for b in bl if b['waga'] == 'wysoka')}).")
    return {"bledy": len(bl or [])}






def praca_sprawdz_ceny_dostawcy(log, pid):
    """Porównanie cen wpisanych przez oferenta z cenami rynkowymi znalezionymi w internecie – wszystkie pozycje z ceną, po 15 w jednym zapytaniu."""
    c = cfg()
    wymagany_klucz(c)
    m = meta(pid)
    poz = [dict(p, lp=i) for i, p in enumerate(m.get("formularz_cenowy") or [], 1) if p.get("cena")]
    if not poz:
        raise ValueError("Wpisz najpierw ceny w formularzu cenowym.")
    poz = sorted(poz, key=lambda p: -(p["cena"] * (p.get("ilosc") or 1)))  # wszystkie pozycje z ceną – najdroższe najpierw
    PACZKA = 15  # tyle pozycji na jedno zapytanie z wyszukiwaniem (dokładność); więcej pozycji = kolejne zapytania
    paczki = [poz[i:i + PACZKA] for i in range(0, len(poz), PACZKA)]
    log(f"Sprawdzam w internecie ceny rynkowe {len(poz)} pozycji" + (f" w {len(paczki)} częściach…" if len(paczki) > 1 else "…"))
    wyn, ile, bledy = {}, 0, []
    for nr, paczka in enumerate(paczki, 1):
        if len(paczki) > 1:
            log(f"Część {nr}/{len(paczki)}: pozycje {', '.join(str(p['lp']) for p in paczka)}")
        lista = "\n".join(f"{p['lp']}. {p['opis']} | j.m.: {p['jm']} | ilość: {p['ilosc']} | cena oferenta netto: {p['cena']} zł" for p in paczka)
        try:
            txt, n_ = CR.claude_z_wyszukiwaniem(c, "Jesteś analitykiem cen w zamówieniach publicznych w Polsce. Odpowiadasz wyłącznie JSON-em.",
                f"Dla każdej pozycji oferty ({'dostawy' if m.get('rodzaj_zamowienia') == 'dostawy' else 'usługi'}) ustal aktualny zakres cen rynkowych netto "
                "w Polsce (sklepy, hurtownie, cenniki, wyniki podobnych przetargów; dla usług – stawki rynkowe z kosztami pracy) i oceń cenę oferenta. "
                'Zwróć JSON: {"pozycje": [{"lp": numer, "od": liczba, "do": liczba, "ocena": "za nisko|rynkowa|za wysoko", '
                '"komentarz": "1 zdanie", "zrodlo": "źródło ceny"}]}. Cena „za nisko” = wyraźnie poniżej rynku (ryzyko rażąco niskiej ceny), '
                "„za wysoko” = wyraźnie powyżej. Brak danych – pomiń pozycję.\n\nPOZYCJE:\n" + lista,
                max_wyszukan=int(c.get("ceny_internet_wyszukan", 10)), log=log)
        except Exception as e:  # jedna część nie przerywa całości – pozostałe pozycje są sprawdzane dalej
            if len(paczki) == 1:
                raise
            bledy.append(nr)
            log(f"Część {nr}: nie udało się sprawdzić ({e}) – przechodzę dalej.")
            continue
        ile += n_
        dozw = {str(p["lp"]) for p in paczka}
        w = MO.wyciagnij_json(txt)
        wyn.update({str(x.get("lp")): x for x in (w.get("pozycje") or []) if isinstance(x, dict) and str(x.get("lp")) in dozw})
    if bledy and not wyn:
        raise ValueError("Nie udało się sprawdzić cen – spróbuj ponownie za kilka minut.")
    with BLOKADA:
        m = meta(pid)
        m["formularz_weryfikacja"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "pozycje": wyn}
        zapisz_meta(pid, m)
    nisko = sum(1 for x in wyn.values() if x.get("ocena") == "za nisko")
    log(f"Gotowe: sprawdzono {len(wyn)} z {len(poz)} pozycji ({ile} wyszukiwań)" + (f", nie sprawdzono części: {', '.join(map(str, bledy))}" if bledy else "") + f"; za nisko: {nisko}, za wysoko: {sum(1 for x in wyn.values() if x.get('ocena') == 'za wysoko')}.")
    return {"sprawdzono": len(wyn)}




def praca_pozycje_formularza(log, pid):
    """Odczyt pozycji (nazwa, j.m., ilość) z formularza cenowego zamawiającego – BEZ cen; ceny wpisuje oferent."""
    c = cfg()
    wymagany_klucz(c)
    pliki = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(pdir(pid), "dokumenty")) for f in fs]
    if not pliki:
        raise ValueError("Najpierw dodaj dokumenty przetargu (krok 1).")
    bloki = [b for _, bl, _ in bloki_dokumentow(pid, log) for b in bl]
    log(f"AI odczytuje pozycje formularza cenowego z {len(pliki)} plików (bez cen)…")
    tresc = MO.oznacz_dokumenty(bloki, MO.ustawienie_cache(c)) + [{"type": "text", "text":
        "Odczytaj z dokumentów zamówienia POZYCJE formularza cenowego / asortymentowo-cenowego (albo – gdy go brak – z opisu przedmiotu zamówienia): "
        "nazwa towaru lub usługi z kluczowymi parametrami, jednostka miary, ilość. NIE podawaj cen. Zwróć JSON: "
        '{"pozycje": [{"opis": "...", "jm": "...", "ilosc": liczba, "uwagi": "wymagane parametry, termin, gwarancja – krótko"}]}'}]
    txt, _ = MO.claude_stream(dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5"), "Odczytujesz dokumenty zamówień publicznych. Odpowiadasz wyłącznie JSON-em.",
                              tresc, max_tokens=8000, log=log)
    poz = [p for p in (MO.wyciagnij_json(txt).get("pozycje") or []) if isinstance(p, dict) and p.get("opis")]
    with BLOKADA:
        m = meta(pid)
        stare = {str(x.get("opis", "")).lower(): x.get("cena") for x in m.get("formularz_cenowy") or []}
        m["formularz_cenowy"] = [{"opis": str(p["opis"])[:500], "jm": str(p.get("jm") or "szt.")[:20], "ilosc": _f_liczba(p.get("ilosc") or 1),
                                  "cena": stare.get(str(p["opis"]).lower(), 0) or 0, "uwagi": str(p.get("uwagi") or "")[:300]} for p in poz]
        zapisz_meta(pid, m)
    log(f"Odczytano {len(poz)} pozycji – wpisz ceny i kliknij „Przygotuj ofertę”.")
    return {"pozycje": len(poz)}


@app.post("/api/projekty/<pid>/oferta")
@wymaga_logowania
def oferta(pid):
    m = meta(pid)
    if jest_dostawca(m):
        return jsonify({"blad": "W ofercie dostawcy / usługodawcy ceny wpisujesz sam w formularzu cenowym (krok 2)."}), 400
    m["opis_zakresu"] = str(request.json.get("wskazowki", ""))[:5000]
    vw = str(request.json.get("vat_wybor", "auto"))
    m["vat_wybor"] = vw if vw in ("auto", "0.23", "0.08", "0.05", "0") else "auto"
    m["ceny_zrodlo"] = "cennik" if request.json.get("ceny") == "cennik" else "rynkowe"
    if m["ceny_zrodlo"] == "cennik" and not (czytaj(F_CENNIK_W, {}) or {}).get("pozycje"):
        return jsonify({"blad": "Nie masz jeszcze własnego cennika – wgraj go (Excel lub CSV) albo wybierz ceny rynkowe."}), 400
    zapisz_meta(pid, m)
    return jsonify(uruchom("oferta", "Przygotowanie kosztorysu" if tylko_kosztorys_typ(m) else "Przygotowanie oferty",
                           praca_oferta, pid, request.json.get("wskazowki", "")))


# ---------- własny cennik (konto) i poprawianie wybranych pozycji kosztorysu













# ---------- dotacje UE/KPO: wyszukiwanie, wnioski o dofinansowanie (faza „wniosek”) i rozliczanie (faza „rozliczenie”)

FAZY = {"rozliczenie": {"klucz": "dotacja", "folder": "rozliczenie", "url": "dotacja"},
        "wniosek": {"klucz": "wniosek_dot", "folder": "wniosek", "url": "wniosek-dot"}}
F_DOT_SZUKAJ = SciezkaKonta("dotacje_wyszukiwanie.json")






def zakres_klucz(z):
    return DOT.bezpieczna(z or "calosc")


def zakres_opis(m, z, faza="rozliczenie"):
    if faza == "wniosek":
        return "wniosek o dofinansowanie"
    if not z or z == "calosc":
        return "rozliczenie końcowe (cała dotacja)"
    e = next((x for x in ((_dot(m).get("wymagania") or {}).get("etapy") or []) if x.get("id") == z), None)
    return f"rozliczenie etapu: {e['nazwa'] if e else z}"


def dokumenty_zakresu(m, z, faza="rozliczenie"):
    wym = _dot(m, faza).get("wymagania") or {}
    if faza == "wniosek":
        return list(wym.get("dokumenty") or [])
    koncowe = (z or "calosc") == "calosc"
    return [d for d in (wym.get("dokumenty") or []) if d.get("dla", "oba") in ("oba", "koncowe" if koncowe else "etap")]


def kat_dok(pid, z, did, faza="rozliczenie"):
    return os.path.join(pdir(pid), FAZY[faza]["folder"], zakres_klucz(z), DOT.bezpieczna(did))




def _zakres(m, faza):
    return "calosc" if faza == "wniosek" else (_dot(m, faza).get("zakres") or "calosc")


def _dane_wnioskodawcy():
    c = cfg()
    return {k: c.get(k, "") for k in ("firma_nazwa", "firma_nip", "firma_regon", "firma_adres", "firma_opis", "firma_osoba", "firma_email", "firma_tel")}




PRIORYTET_DOT = ("regulamin", "kryter", "umow", "wniosk", "instrukc", "zalacz", "załącz", "wskaz", "wskaź", "harmonogram", "kwalifikow", "porozumien")


def _tekst_pliku_dot(sciezka, nazwa):
    """Tekst dokumentu dotacji (PDF jako tekst, a nie obraz strony – kilkanaście razy taniej przy długich regulaminach)."""
    r = os.path.splitext(nazwa)[1].lower()
    if r == ".pdf":
        import logging
        import pypdf
        logging.getLogger("pypdf").setLevel(logging.ERROR)
        czytnik = pypdf.PdfReader(sciezka)
        return "\n".join(f"[strona {i}] " + (s_.extract_text() or "") for i, s_ in enumerate(czytnik.pages, 1))
    if r == ".docx":
        return MO.tekst_docx(sciezka)
    if r == ".doc":
        return MO.tekst_doc(sciezka)
    if r in (".xlsx", ".xlsm"):
        return MO.tekst_xlsx(sciezka)
    if r in (".txt", ".csv", ".md", ".html", ".htm", ".xml", ".rtf"):
        return open(sciezka, encoding="utf-8", errors="replace").read()
    return ""


def bloki_dotacji(pid, log=None, katalog=None, limit=480_000):
    """Dokumenty dotacji jako tekst (z ZIP-ów też), najważniejsze najpierw (regulamin, kryteria, wzór wniosku…), w limicie znaków."""
    import zipfile
    import tempfile
    kat = katalog or os.path.join(pdir(pid), "dokumenty")
    pliki = []
    if katalog:
        for kor, _, pl in os.walk(kat):
            pliki += [os.path.join(kor, f) for f in sorted(pl)]
    else:
        pliki = [os.path.join(kat, p["sciezka"]) for p in lista_plikow(pid) if p["uwzglednij"]]
    teksty, pominiete = [], []
    with tempfile.TemporaryDirectory() as tmp:
        rozwiniete = []
        for p in pliki:
            if p.lower().endswith(".zip"):
                try:
                    with zipfile.ZipFile(p) as z:
                        for n in z.namelist()[:60]:
                            if not n.endswith("/"):
                                cel = os.path.join(tmp, f"{len(rozwiniete)}_{os.path.basename(n)}")
                                with open(cel, "wb") as f:
                                    f.write(z.read(n))
                                rozwiniete.append((cel, f"{os.path.basename(p)} / {os.path.basename(n)}"))
                except Exception:
                    pominiete.append(os.path.basename(p))
            else:
                rozwiniete.append((p, os.path.basename(p)))
        waga = lambda n: next((i for i, k in enumerate(PRIORYTET_DOT) if k in n.lower()), len(PRIORYTET_DOT))
        for sc, nazwa in sorted(rozwiniete, key=lambda x: waga(x[1])):
            try:
                t = _tekst_pliku_dot(sc, os.path.basename(sc)).strip()
            except Exception:
                t = ""
            if not t or (sc.lower().endswith(".pdf") and len(t) < 200):
                # skan bez warstwy tekstowej – mały PDF wysyłamy jako obraz dokumentu (maks. 2 takie pliki)
                if sc.lower().endswith(".pdf") and os.path.getsize(sc) < 6_000_000 and sum(1 for x in teksty if x[1] is None) < 2:
                    teksty.append((nazwa, None, sc))
                    continue
                pominiete.append(nazwa)
                continue
            teksty.append((nazwa, t[:150_000]))
        bloki, suma, uciete = [], 0, []
        for poz in teksty:
            nazwa, t = poz[0], poz[1]
            if t is None:  # skan PDF
                b_, rozm, _ = MO.przygotuj_blok_tekstowy(poz[2])
                for x in b_:
                    x["title"] = nazwa
                bloki += b_
                suma += 60_000
                continue
            if suma >= limit:
                uciete.append(nazwa)
                continue
            t = t[:limit - suma]
            suma += len(t)
            bloki.append({"type": "document", "title": nazwa, "source": {"type": "text", "media_type": "text/plain", "data": t}})
    if log:
        log(f"Dokumenty do analizy: {len(bloki)} (ok. {suma // 4000} tys. tokenów)" + (f"; pominięte bez tekstu: {', '.join(pominiete[:5])}" if pominiete else "")
            + (f"; poza limitem: {', '.join(uciete[:5])}" if uciete else ""))
    return bloki, len(bloki)


def _lista_slownikow(x, klucz="nazwa"):
    """AI czasem zwraca listę napisów zamiast obiektów – zamiana na obiekty, żeby dalsze kroki się nie wysypały."""
    wyn = []
    for e in x or []:
        if isinstance(e, dict):
            wyn.append(e)
        elif isinstance(e, str) and e.strip():
            wyn.append({klucz: e.strip()})
    return wyn












def bloki_rozliczenia(pid, z, faza="rozliczenie"):
    kat = os.path.join(pdir(pid), FAZY[faza]["folder"], zakres_klucz(z))
    if not os.path.isdir(kat):
        return [], 0
    return bloki_dotacji(pid, None, katalog=kat, limit=250_000)












def _rejestruj_dotacje():
    for faza, f in FAZY.items():
        u = f["url"]
        app.add_url_rule(f"/api/projekty/<pid>/{u}/dane", f"{u}_dane", wymaga_logowania(lambda pid, faza=faza: dot_dane_impl(pid, faza)), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}", f"{u}_stan", wymaga_logowania(lambda pid, faza=faza: dot_stan_impl(pid, faza)), methods=["GET"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/analiza", f"{u}_analiza", wymaga_logowania(lambda pid, faza=faza: jsonify(uruchom(
            "dotacja", "Analiza dokumentów naboru" if faza == "wniosek" else "Analiza dokumentów dotacji", praca_dot_analiza, pid, faza))), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/plik", f"{u}_plik", wymaga_logowania(lambda pid, faza=faza: dot_plik_impl(pid, faza)), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/plik/usun", f"{u}_plik_usun", wymaga_logowania(lambda pid, faza=faza: dot_plik_usun_impl(pid, faza)), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/przygotuj", f"{u}_przygotuj", wymaga_logowania(lambda pid, faza=faza: jsonify(uruchom(
            "dotacja", f"Przygotowanie dokumentu ({DOT.bezpieczna((request.json or {}).get('dok', ''))})", praca_dot_przygotuj, pid,
            DOT.bezpieczna((request.json or {}).get("dok", "")), faza))), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/sprawdz", f"{u}_sprawdz", wymaga_logowania(lambda pid, faza=faza: jsonify(uruchom(
            "dotacja", "Sprawdzenie wniosku" if faza == "wniosek" else "Sprawdzenie dokumentów rozliczenia", praca_dot_sprawdz, pid, faza))), methods=["POST"])
        app.add_url_rule(f"/api/projekty/<pid>/{u}/komplet", f"{u}_komplet", wymaga_logowania(lambda pid, faza=faza: dot_komplet_impl(pid, faza)), methods=["POST"])


_rejestruj_dotacje()


# --- wyszukiwanie dotacji


# --- bezpośredni odczyt portali regionalnych z naborami (bez polegania na wyszukiwarce internetowej)

PORTALE_REGIONALNE = {
    "dolnośląskie": "https://funduszeuedolnoslaskie.pl/", "kujawsko-pomorskie": "https://funduszeue.kujawsko-pomorskie.pl/",
    "lubelskie": "https://funduszeue.lubelskie.pl/", "lubuskie": "https://funduszeue.lubuskie.pl/", "łódzkie": "https://funduszeue.lodzkie.pl/",
    "małopolskie": "https://fundusze.malopolska.pl/", "mazowieckie": "https://funduszeuedlamazowsza.eu/", "opolskie": "https://funduszeue.opolskie.pl/",
    "podkarpackie": "https://funduszeue.podkarpackie.pl/", "podlaskie": "https://funduszeuepodlaskie.pl/", "pomorskie": "https://funduszeuepomorskie.pl/",
    "śląskie": "https://funduszeue.slaskie.pl/", "świętokrzyskie": "https://funduszeueswietokrzyskie.pl/",
    "warmińsko-mazurskie": "https://funduszeeuropejskie.warmia.mazury.pl/", "wielkopolskie": "https://wrpo.wielkopolskie.pl/",
    "zachodniopomorskie": "https://funduszeue.wzp.pl/"}
ROZSZ_DOK = (".pdf", ".docx", ".doc", ".xlsx", ".xls", ".odt", ".ods", ".zip", ".rtf", ".7z")


def tekst_html(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr)>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    import html as _h
    h = _h.unescape(h)
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", h)).strip()


def linki_html(h, baza):
    import html as _html
    b = re.search(r"""(?is)<base\s[^>]*href=["']([^"']+)["']""", h)  # <base href> zmienia sposób składania adresów względnych
    baza = urllib.parse.urljoin(baza, _html.unescape(b.group(1).strip())) if b else baza
    wyn = []
    for href, tekst in re.findall(r"""(?is)<a\s[^>]*?href=["']([^"'#]+)["'][^>]*>(.*?)</a>""", h):
        t = re.sub(r"\s+", " ", tekst_html(tekst)).strip()
        # „&amp;” w adresie to „&” – bez zamiany serwer zwraca 404 (częste w linkach do pobierania plików)
        wyn.append((urllib.parse.urljoin(baza, _html.unescape(href.strip())), t))
    return wyn


OGOLNE_SLOWA_NABORU = {"program", "programu", "priorytetowy", "priorytetowego", "nabor", "naboru", "konkurs", "wsparcie", "dotacja", "dotacji",
                       "dofinansowanie", "pozyczka", "pozyczki", "preferencyjna", "przedsiebiorcow", "przedsiebiorcy", "czesc", "edycja", "inwestycje",
                       "projektow", "zakresie", "ramach", "srodkow", "fundusz", "funduszu", "oraz", "lata"}


def identyfikatory_naboru(nab):
    """Po czym rozpoznać dokumenty TEGO naboru: nazwa programu (np. „energia plus”), numery działań (I.10.2, 7.2.2), słowa kluczowe nazwy."""
    nazwa = str(nab.get("nazwa") or "")
    frazy = set()
    for czesc in re.split(r"[–—:(),\-]| dla | na ", nazwa):
        n = W.norm(czesc)
        if len(n) >= 5 and n not in OGOLNE_SLOWA_NABORU:
            frazy.add(n)
    for q in re.findall(r"[„\"]([^”\"]{4,60})[”\"]", nazwa + " " + str(nab.get("program") or "")):
        frazy.add(W.norm(q))
    kody = set(re.findall(r"\b[IVX]{0,4}\.?\d{1,2}(?:\.\d{1,2}){1,3}\b", nazwa + " " + str(nab.get("program") or "")))
    slowa = {w for w in W.norm(nazwa).split() if len(w) > 4 and w not in OGOLNE_SLOWA_NABORU}
    return {"frazy": [f for f in frazy if f], "kody": [k.lower() for k in kody], "slowa": list(slowa)}


def zgodnosc_dokumentu(sciezka, nab):
    """('ok' | 'obcy' | 'niepewny', opis). Dokument innego programu (np. „Edukacja ekologiczna” zamiast „Energia Plus”) – 'obcy'."""
    try:
        tekst, _ = OD._tekst_pliku(sciezka)
    except Exception:
        return "niepewny", "nie udało się odczytać treści"
    if len(tekst.strip()) < 200:
        return "niepewny", "brak tekstu (skan?) – sprawdź ręcznie"
    t = W.norm(tekst[:12000])
    idn = identyfikatory_naboru(nab)
    if any(f in t for f in idn["frazy"]) or any(k in tekst[:12000].lower() for k in idn["kody"]):
        return "ok", "dokument dotyczy tego naboru"
    traf_slow = sum(1 for w in idn["slowa"] if w in t)
    # tytuł innego programu na początku dokumentu: „Program priorytetowy „Xxx”” / „Regulamin naboru … „Xxx””
    inne = re.findall(r"(?:program(?:u)? priorytetow\w*|regulamin\w*(?: naboru)?|konkurs\w*|nab[oó]r\w*)\s*(?:pn\.?|pod nazwą)?\s*[„\"]([^”\"]{4,80})[”\"]", tekst[:6000], flags=re.I)
    inne = [x for x in inne if not any(f in W.norm(x) for f in idn["frazy"])]
    if inne and traf_slow < 2:
        return "obcy", f"dotyczy innego programu: „{inne[0].strip()[:70]}”"
    if idn["slowa"] and traf_slow == 0:
        return "obcy", "w treści nie ma nazwy ani słów tego naboru"
    return "niepewny" if traf_slow < 2 else "ok", "częściowo pasuje – sprawdź" if traf_slow < 2 else "pasuje"


def ocena_pliku_naboru(nazwa, url, nabor):
    """Czy plik ze strony dotyczy tego naboru: regulamin / wniosek / załączniki i słowa z nazwy naboru – wyżej;
    dokumenty archiwalne (stare lata, „archiwum”) – nisko."""
    t = W.norm(f"{nazwa} {urllib.parse.unquote(url)}")
    pkt = 0
    if re.search(r"regulamin|wzor wniosk|wniosek o|wniosku|formularz|instrukcj|zalacznik|kryteri|ogloszen|komunikat|program priorytet|biznesplan|oswiadcz|umow", t):
        pkt += 3
    slowa = [w for w in W.norm(nabor.get("nazwa") or "").split() if len(w) > 4 and w not in ("nabor", "program", "naboru", "programu", "wsparcie")]
    pkt += min(4, 2 * sum(1 for w in slowa if w in t))
    if slowa and not any(w in t for w in slowa) and re.search(r"program priorytet|edukacj|przyrod|ochrony srodowiska", t):
        pkt -= 4  # na stronach funduszy z wieloma programami – plik innego programu
    lata = [int(x) for x in re.findall(r"(?<!\d)(20[0-3]\d)(?!\d)", t)]
    if lata and max(lata) <= dt.date.today().year - 3:
        pkt -= 6  # np. „kryteria obowiązujące od 2013 r.”
    if re.search(r"archiw|nieaktualn|uchylon", t):
        pkt -= 6
    return pkt


# pliki bez rozszerzenia w adresie: gov.pl (/attachment/<id>), portale z „pobierz”, „download”, „getfile”, „?file=” itp.
WZOR_PLIKU_BEZ_ROZSZ = re.compile(r"(?i)/attachment/|download|/pobierz|getfile|get_file|/file/|/files/|/plik|[?&](file|plik|id_pliku|attachment|gid|fileid)=|/media/|/uploads?/|/storage/")
WZOR_TEKSTU_PLIKU = re.compile(r"(?i)\.(pdf|docx?|xlsx?|odt|ods|zip|rtf)\b|\b(pdf|docx|xlsx|zip)\b|\(\s*\d+[.,]?\d*\s*[kKmM][bB]\s*\)")
WZOR_PODSTRONY_NABORU = re.compile(r"(?i)dokument|regulamin|formularz|wz[oó]r|za[łl][aą]cznik|do pobrania|materia[łl]y|nab[oó]r|wnios|instrukcj|kryteri")




def podstrony_naboru(h, baza, nab=None):
    """Odnośniki na tej samej stronie, za którymi są dokumenty TEGO naboru: z nazwą/numerem naboru w opisie lub adresie albo
    podstrony bieżącej strony („Dokumenty do pobrania” pod adresem naboru). Ogólne menu serwisu (wszystkie programy funduszu) – pomijane."""
    host = urllib.parse.urlparse(baza).netloc
    sciezka_bazy = urllib.parse.urlparse(baza).path.rstrip("/")
    idn = identyfikatory_naboru(nab or {})
    klucze = idn["frazy"] + idn["kody"] + idn["slowa"]
    wyn = []
    for u, t in linki_html(h, baza):
        p = urllib.parse.urlparse(u)
        if not (p.netloc == host and t and not p.path.lower().endswith(ROZSZ_DOK) and not WZOR_PLIKU_BEZ_ROZSZ.search(p.path)
                and u.split("#")[0].rstrip("/") != baza.split("#")[0].rstrip("/")):
            continue
        opis = W.norm(t + " " + urllib.parse.unquote(p.path))
        o_naborze = any(k in opis for k in klucze) if klucze else False
        podstrona = bool(sciezka_bazy) and p.path.startswith(sciezka_bazy + "/")
        dok = bool(re.search(r"(?i)dokument|do pobrania|regulamin|formularz|wz[oó]r|za[łl][aą]cznik|instrukcj", t))
        # kolejność: strony z nazwą / numerem naboru → podstrony tej strony → ogólne „Dokumenty do pobrania” (treść plików i tak jest sprawdzana)
        prio = 0 if o_naborze else 1 if (podstrona and WZOR_PODSTRONY_NABORU.search(t)) else 2 if dok else None
        if prio is not None:
            wyn.append((prio, u.split("#")[0]))
            PODSTRONY_OPIS[u.split("#")[0]] = t
    return list(dict.fromkeys(u for _, u in sorted(wyn)))[:5]


PODSTRONY_OPIS = {}  # opis linku podstrony – nazwa pliku, gdy „podstrona” okazuje się plikiem


def lista_naborow_portalu(region, log=None):
    """Lista naborów z portalu regionalnego programu FE: strona główna → zakładka „Nabory” → odnośniki do naborów z fragmentem opisu."""
    url = PORTALE_REGIONALNE.get(region)
    if not url:
        return []
    try:
        dane, _, kon = _pobierz_url(url)
        h = dane.decode("utf-8", errors="ignore")
        lista_url = next((u for u, t in linki_html(h, kon) if re.fullmatch(r"(?i)\s*nabory(\s+wniosków)?\s*", t or "")), None) \
            or urllib.parse.urljoin(kon, "nabory")
        dane, _, kon2 = _pobierz_url(lista_url)
        h2 = dane.decode("utf-8", errors="ignore")
    except Exception as e:
        if log:
            log(f"Portal regionalny ({region}) niedostępny: {opis_bledu_zadania(e, 'szukaj')}")
        return []
    wyn, widz = [], set()
    tekst = tekst_html(h2)
    for u, t in linki_html(h2, kon2):
        if not re.search(r"(?i)nab[oó]r", t or "") or len(t) < 15 or u in widz or u.rstrip("/") == lista_url.rstrip("/"):
            continue
        if not re.search(r"/nabory/|nabor|/w/", u, re.I):
            continue
        widz.add(u)
        i = tekst.find(t[:40])
        fragment = tekst[i:i + 700] if i >= 0 else ""
        wyn.append({"nazwa": t[:300], "link": u, "fragment": fragment})
    if log:
        log(f"Portal regionalny {urllib.parse.urlparse(url).netloc}: odczytano {len(wyn)} naborów.")
    return wyn[:60]


def praca_nabor_z_linku(log, url):
    """Nabór dodany z linku: odczyt strony naboru (dane i dokumenty) – działa dla portali regionalnych, KPO i innych instytucji."""
    c = cfg()
    wymagany_klucz(c)
    zap = (pamiec_naborow().get("nabory") or {}).get(_klucz_naboru(url))
    if zap and zap.get("dokumenty") and zap.get("zrodlo") == "link":
        log("Nabór jest w pamięci programu – bez ponownego pobierania.")
        w = czytaj(F_DOT_SZUKAJ, {}) or {}
        w["wyniki"] = [dict(zap, status=_status_naboru(zap))] + [x for x in (w.get("wyniki") or []) if x.get("id") != zap["id"]]
        pisz(F_DOT_SZUKAJ, w)
        return {"id": zap["id"]}
    log(f"Odczytuję stronę naboru: {url[:90]}…")
    dane, typ, kon = _pobierz_url(url)
    if "html" not in typ:
        raise ValueError("Ten link prowadzi do pliku, a nie do strony naboru – wklej adres strony z opisem naboru.")
    h = dane.decode("utf-8", errors="ignore")
    pliki = pliki_z_html(h, kon)
    tytul = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", h)
    tekst = tekst_html(h)[:30000]
    pol = ("Poniżej treść strony naboru dotacji. Odczytaj dane naboru WYŁĄCZNIE z tej treści (nie zgaduj). Zwróć JSON: "
           '{"nazwa": "…", "program": "…", "instytucja": "…", "dla_kogo": "…", "region": "…", "branze": ["…"], "forma": "dotacja | pożyczka | …", '
           '"poziom_dofinansowania": "…", "kwota": "alokacja / min–max wartość", "nabor_od": "RRRR-MM-DD", "nabor_do": "RRRR-MM-DD", '
           '"status": "otwarty | planowany | zamknięty", "opis": "na co (2–3 zdania)", "sposob_skladania": "…"}\n\nTREŚĆ STRONY:\n' + tekst)
    txt, _ = MO.claude_stream(dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5"), DOT.SYSTEM, [{"type": "text", "text": pol}],
                              max_tokens=3000, log=log)
    n = MO.wyciagnij_json(txt)
    n["nazwa"] = n.get("nazwa") or (tekst_html(tytul.group(1)) if tytul else url)
    n.update(link=kon, dokumenty=pliki, zrodlo="link", dopasowanie=None)
    dodaj_do_pamieci([n], None, "link")
    n = dict((pamiec_naborow().get("nabory") or {}).get(_klucz_naboru(kon)) or n)
    if _klucz_naboru(url) != _klucz_naboru(kon):  # adres po przekierowaniu – zapamiętaj też podany
        dodaj_do_pamieci([dict(n, link=url)], None, "link")
    w = czytaj(F_DOT_SZUKAJ, {}) or {}
    w["wyniki"] = [n] + [x for x in (w.get("wyniki") or []) if x.get("link") != kon]
    w.setdefault("data", dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
    pisz(F_DOT_SZUKAJ, w)
    log(f"Dodano nabór: {n['nazwa'][:80]} · dokumentów na stronie: {len(pliki)}.")
    return {"id": n["id"]}





F_NABORY = os.path.join(DATA, "dotacje_pamiec_naborow.json")  # wspólna pamięć naborów (dane publiczne) – raz pobrany nabór nie jest pobierany ponownie
KAT_PLIKI_NAB = os.path.join(DATA, "dotacje_pliki")


def pamiec_naborow():
    return czytaj(F_NABORY, {}) or {}


def _klucz_naboru(link):
    return url_bezpieczny(link).rstrip("/").lower() if link else ""


def dodaj_do_pamieci(nabory, region=None, zrodlo=""):
    with BLOKADA:
        p = pamiec_naborow()
        n_ = p.setdefault("nabory", {})
        teraz = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        for x in nabory:
            if not isinstance(x, dict) or not x.get("link"):
                continue
            k = _klucz_naboru(x["link"])
            stary = n_.get(k) or {}
            nowy = {**stary, **{kk: v for kk, v in x.items() if v not in (None, "", [])}}
            nowy.setdefault("pobrano", teraz)
            nowy["zaktualizowano"] = teraz
            if region and not nowy.get("region_portalu"):
                nowy["region_portalu"] = region
            if zrodlo and not nowy.get("zrodlo"):
                nowy["zrodlo"] = zrodlo
            nowy["id"] = stary.get("id") or (DOT.bezpieczna(nowy.get("nazwa") or "nabor")[:30] + "_" + hashlib.sha1(k.encode()).hexdigest()[:6])
            n_[k] = nowy
        pisz(F_NABORY, p)
    return p


def _status_naboru(x):
    """Status z dat (nabór trwa / planowany / zamknięty) – dane z pamięci mogą być sprzed kilku dni."""
    dzis = dt.date.today().isoformat()
    od, do = str(x.get("nabor_od") or "")[:10], str(x.get("nabor_do") or "")[:10]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", do) and do < dzis:
        return "zamknięty"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", od) and od > dzis:
        return "planowany"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", od) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", do):
        return "otwarty"
    return x.get("status") or ""


def _norm(t):
    import unicodedata
    return unicodedata.normalize("NFKD", str(t or "").replace("ł", "l").replace("Ł", "L")).encode("ascii", "ignore").decode().lower()


def dopasowanie_naboru(x, k):
    """Czy nabór pasuje do kryteriów (region, branża, wnioskodawca, słowa) i jak bardzo (0 = nie pokazuj)."""
    region = k.get("region") or "cała Polska"
    reg = _norm(x.get("region"))
    prog = _norm(" ".join(str(x.get(p_) or "") for p_ in ("program", "instytucja", "nazwa")))
    krajowy = not x.get("region_portalu") and (not reg or re.search(r"cala polsk|ogolnopol|krajow|^polska", reg)
                                               or (re.search(r"\bkpo\b|feniks|feng|fers|nfos|bgk|parp|arimr", prog) and not re.search(r"wfos|regionaln|fe[a-z]{2,3} 2021", prog)))
    if region != "cała Polska":
        if x.get("region_portalu") and x["region_portalu"] != region:
            return 0  # nabór z programu regionalnego innego województwa
        if not x.get("region_portalu") and not krajowy and not re.search(r"(?<![a-z])" + re.escape(_norm(region)), reg + " " + prog):
            return 0  # nabór regionalny innego województwa (np. „śląskie” ≠ „dolnośląskie”)
    tekst = _norm(" ".join(str(x.get(p_) or "") for p_ in ("nazwa", "opis", "dla_kogo", "program")) + " " + " ".join(x.get("branze") or [])
                  + " " + " ".join(x.get("wnioskodawcy") or []))
    wynik = 5
    if k.get("branza"):
        if k["branza"] in (x.get("branze") or []):
            wynik += 3
        elif any(re.search(r"(?<![a-z])" + re.escape(w_), tekst) for w_ in [_norm(w)[:7] for w in re.split(r"[ ,()/+]+", k["branza"])
                                                                          if len(w) >= 3 and _norm(w) not in ("dla", "oraz", "inne")]):
            wynik += 1
        else:
            return 0
    if k.get("wnioskodawca"):
        if k["wnioskodawca"] in (x.get("wnioskodawcy") or []):
            wynik += 2
        elif x.get("wnioskodawcy"):
            return 0
    if k.get("slowa"):
        slowa = [_norm(w)[:6] for w in re.split(r"[ ,;]+", k["slowa"]) if len(w) > 3]
        wynik += min(2, sum(1 for w in slowa if w in tekst))
    if k.get("pomysl"):  # wyszukiwanie odwrotne: nabory pasujące do pomysłu wyżej
        pom = [_norm(w)[:6] for w in re.split(r"[ ,;.]+", k["pomysl"]) if len(w) > 4][:30]
        wynik += min(3, sum(1 for w in pom if w in tekst))
    return min(10, wynik)


def praca_szukaj_dotacji(log, kryteria):
    """Wyszukiwanie z pamięcią: nabory pobrane wcześniej są brane z pamięci programu; z portalu pobierane i porządkowane są tylko nowe,
    a wyszukiwanie w internecie (programy krajowe) dla tych samych kryteriów jest powtarzane najwyżej raz na 7 dni."""
    c = cfg()
    wymagany_klucz(c)
    region = kryteria.get("region") or "cała Polska"
    log(f"Szukam naborów: {kryteria.get('branza') or 'dowolna branża'}, {region}" + (f", {kryteria['wnioskodawca']}" if kryteria.get("wnioskodawca") else ""))
    p = pamiec_naborow()
    log(f"Pamięć programu: {len(p.get('nabory') or {})} wcześniej pobranych naborów.")
    # 1) portal regionalny – lista jest tania (strona HTML); AI porządkuje tylko nabory, których nie ma w pamięci
    if region in PORTALE_REGIONALNE:
        lista = lista_naborow_portalu(region, log)
        znane = set((p.get("nabory") or {}).keys())
        nowe = [x for x in lista if _klucz_naboru(x["link"]) not in znane]
        log(f"Portal regionalny: {len(lista)} naborów, z pamięci: {len(lista) - len(nowe)}, nowych do pobrania: {len(nowe)}.")
        for i0 in range(0, len(nowe), 25):
            partia = nowe[i0:i0 + 25]
            txt, _ = MO.claude_stream(dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5"), DOT.SYSTEM_SZUKAJ,
                                      [{"type": "text", "text": DOT.polecenie_struktury(partia, region)}], max_tokens=12000, log=log)
            dane = MO.wyciagnij_json(txt)
            dane = dane.get("dotacje") if isinstance(dane, dict) else dane
            linki_ok = {_klucz_naboru(x["link"]): x["link"] for x in partia}
            dobre = [dict(x, link=linki_ok[_klucz_naboru(x["link"])], region=region) for x in (dane or [])
                     if isinstance(x, dict) and x.get("link") and _klucz_naboru(x["link"]) in linki_ok]
            p = dodaj_do_pamieci(dobre, region, "portal regionalny")
    # 2) programy krajowe i KPO – wyszukiwanie w internecie dla danych kryteriów najwyżej raz na 7 dni
    klucz_z = "|".join([kryteria.get("branza") or "", kryteria.get("wnioskodawca") or "", (kryteria.get("slowa") or "").lower().strip(),
                        (kryteria.get("pomysl") or "").lower().strip()[:120],
                        "" if region in PORTALE_REGIONALNE else region])
    ost = (p.get("zapytania") or {}).get(klucz_z)
    if ost and not kryteria.get("odswiez") and (dt.datetime.now() - dt.datetime.strptime(ost, "%Y-%m-%d %H:%M")).days < 7:
        log(f"Programy krajowe: wyniki z pamięci (wyszukiwanie z {ost}) – bez ponownego pobierania.")
    else:
        log("AI przegląda strony programów krajowych i KPO…")
        k2 = dict(kryteria, slowa=(kryteria.get("slowa") or "") + (" (tylko programy krajowe i KPO – nabory regionalne odczytano z portalu)" if region in PORTALE_REGIONALNE else ""))
        try:
            txt, n = CR.claude_z_wyszukiwaniem(c, DOT.SYSTEM_SZUKAJ, DOT.polecenie_szukania(k2), max_wyszukan=10, max_tokens=12000, log=log)
            dane = MO.wyciagnij_json(txt)
            dane = dane.get("dotacje") if isinstance(dane, dict) else dane
            znalezione = [dict(x, dokumenty=[d_ for d_ in (x.get("dokumenty") or []) if isinstance(d_, dict) and str(d_.get("url", "")).startswith("http")][:20])
                          for x in (dane or []) if isinstance(x, dict) and x.get("link")]
            p = dodaj_do_pamieci(znalezione, None, "wyszukiwanie w internecie")
            with BLOKADA:
                p = pamiec_naborow()
                p.setdefault("zapytania", {})[klucz_z] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
                pisz(F_NABORY, p)
            log(f"Programy krajowe: znaleziono {len(znalezione)} naborów (wyszukiwań w internecie: {n}).")
        except Exception as e:
            log(f"Wyszukiwanie w internecie nie powiodło się: {opis_bledu_zadania(e, 'szukaj')}")
    # 3) wynik – tylko nabory pasujące do bieżących kryteriów (bez naborów z innych programów regionalnych i zamkniętych)
    wyniki = []
    for x in (pamiec_naborow().get("nabory") or {}).values():
        st = _status_naboru(x)
        if st == "zamknięty":
            continue
        sc = dopasowanie_naboru(x, kryteria)
        if sc:
            wyniki.append(dict(x, status=st, dopasowanie=sc))
    wyniki.sort(key=lambda x: (-(x["dopasowanie"] or 0), 0 if x.get("status") == "otwarty" else 1, str(x.get("nabor_do") or "9999")))
    pisz(F_DOT_SZUKAJ, {"kryteria": kryteria, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wyniki": wyniki[:60]})
    log(f"Pasujące nabory: {len(wyniki)} (pokazuję tylko te zgodne z wybranym regionem, branżą i wnioskodawcą).")
    return {"liczba": len(wyniki)}






def url_bezpieczny(url):
    """Adres z polskimi znakami albo spacjami (częste w nazwach plików na portalach) → poprawnie zakodowany adres."""
    p = urllib.parse.urlsplit(url.strip())
    sciezka = urllib.parse.quote(urllib.parse.unquote(p.path), safe="/:@!$&'()*+,;=-._~")
    zapytanie = urllib.parse.quote(urllib.parse.unquote(p.query), safe="=&/:@!$'()*+,;-._~")
    return urllib.parse.urlunsplit((p.scheme, p.netloc.encode("idna").decode() if p.netloc else "", sciezka, zapytanie, ""))


PRZEGLADARKA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/pdf,application/zip,application/octet-stream,*/*;q=0.8",
                "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.6"}


def _pobierz_url(url, timeout=60, referer=None):
    """Pobranie strony lub pliku jak zwykła przeglądarka (część portali odrzuca nietypowe programy), z jednym ponowieniem."""
    u = url_bezpieczny(url)
    ost = None
    for proba in range(2):
        req = urllib.request.Request(u, headers=dict(PRZEGLADARKA, **({"Referer": referer} if referer else {})))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(40 * 1024 * 1024), (r.headers.get("Content-Type") or "").lower(), r.geturl()
        except urllib.error.HTTPError as e:
            ost = e
            if e.code in (404, 410):
                break
        except Exception as e:
            ost = e
        time.sleep(2)
    raise ost


def praca_pobierz_dok_naboru(log, pid):
    """Pobiera dokumenty wybranego naboru (regulamin, wzór wniosku, załączniki): z linków zapisanych przy naborze oraz wszystkie pliki
    podlinkowane na stronie naboru. Wynik (pobrane i nieudane z przyczyną) zapisuje przy wniosku."""
    m = meta(pid)
    nab = (_dot(m, "wniosek").get("nabor") or {})
    strona = nab.get("link") or ""
    jest_plik = lambda u: urllib.parse.urlparse(u).path.lower().endswith(ROZSZ_DOK)
    wszystkie = [((x.get("nazwa") or ""), x["url"]) for x in (nab.get("dokumenty") or []) if x.get("url")]
    linki = [x for x in wszystkie if jest_plik(x[1])]
    # odnośniki do stron (np. „Strona programu – listy gmin, regulaminy”) to nie pliki: program czyta je jak stronę naboru
    strony = ([strona] if strona else []) + [u for _, u in wszystkie if not jest_plik(u) and u != strona] + list(nab.get("strony_dodatkowe") or [])
    if nab.get("_tylko_ai"):  # druga próba: strona naboru miała tylko dokumenty innych programów – szukamy w internecie
        strony, linki, wszystkie = [], [], []
    bledy_stron = []
    kolejka, odwiedzone, glebokosc = list(dict.fromkeys(strony))[:6], set(), {}
    while kolejka and len(odwiedzone) < 12:
        st_url = kolejka.pop(0)
        if st_url in odwiedzone:
            continue
        odwiedzone.add(st_url)
        try:
            log(f"Czytam stronę: {st_url[:90]}")
            dane, typ, kon = _pobierz_url(st_url, timeout=35)
            if "html" in typ:
                html_ = dane.decode("utf-8", errors="ignore")
                nowe = pliki_z_html(html_, kon)
                znane = {url_bezpieczny(u) for _, u in linki}
                linki += [(x["nazwa"], x["url"]) for x in nowe if url_bezpieczny(x["url"]) not in znane]
                log(f"Na stronie jest {len(nowe)} plików do pobrania.")
                if len(nowe) < 2 and glebokosc.get(st_url, 0) == 0:  # dokumenty bywają na podstronie („Dokumenty do pobrania”, „Regulamin”)
                    pod = [u for u in podstrony_naboru(html_, kon, nab) if u not in odwiedzone]
                    if pod:
                        log(f"Sprawdzam {len(pod)} podstron z dokumentami naboru…")
                    for u in pod:
                        glebokosc[u] = 1
                    kolejka += pod
            else:
                linki.append((PODSTRONY_OPIS.get(st_url) or next((n for n, u in wszystkie if u == st_url), "") or "dokument", kon))
        except Exception as e:
            opis = opis_bledu_zadania(e, "dotacje")
            if "na czas" in opis or "timed out" in str(e).lower():
                opis = ("strona instytucji nie odpowiedziała na czas – serwer bywa przeciążony albo nie wpuszcza programów; otwórz link w przeglądarce "
                        "i pobierz pliki ręcznie albo wklej poniżej link bezpośrednio do strony z dokumentami lub do pliku")
            bledy_stron.append({"nazwa": "Strona: " + (next((n for n, u in wszystkie if u == st_url), "") or st_url[:60]), "url": st_url, "blad": opis})
            log(f"Nie udało się otworzyć strony {st_url[:70]}: {opis}")
    if not linki:  # strona naboru bez plików (albo niedostępna) – AI szuka w internecie bezpośrednich linków do dokumentów
        try:
            c_ = cfg()
            wymagany_klucz(c_)
            log("Na stronie naboru nie ma plików – szukam dokumentów naboru w internecie (AI)…")
            pol = (f"Znajdź w internecie BEZPOŚREDNIE linki do plików dokumentacji naboru: „{nab.get('nazwa') or m.get('nazwa')}” "
                   f"({nab.get('program') or ''}, {nab.get('instytucja') or ''}). Szukaj na stronach instytucji (gov.pl, strony programów, BIP): "
                   "regulamin / komunikat ministra / ogłoszenie o naborze, wzór wniosku, instrukcja wypełniania, załączniki. Podaj tylko linki, "
                   "które prowadzą do pliku (PDF, DOCX, XLSX, ZIP) albo do strony gov.pl/attachment. "
                   'Zwróć WYŁĄCZNIE JSON: {"dokumenty": [{"nazwa": "…", "url": "https://…"}], "strona_naboru": "https://… albo pusty"}')
            txt, _ = CR.claude_z_wyszukiwaniem(dict(c_, _model=c_.get("model_oferty") or c_.get("model")), "Wyszukujesz oficjalne dokumenty naborów "
                                               "dotacji w Polsce. Nie zmyślasz adresów – podajesz tylko te, które znalazłeś. Odpowiadasz WYŁĄCZNIE JSON-em.",
                                               pol, max_wyszukan=5, max_tokens=3000, log=log)
            j_ = MO.wyciagnij_json(txt) or {}
            for x in (j_.get("dokumenty") or [])[:12]:
                if isinstance(x, dict) and str(x.get("url", "")).startswith("http"):
                    linki.append((str(x.get("nazwa") or "dokument")[:150], x["url"]))
            if j_.get("strona_naboru", "").startswith("http") and j_["strona_naboru"] not in odwiedzone:
                try:
                    dane, typ, kon = _pobierz_url(j_["strona_naboru"], timeout=35)
                    if "html" in typ:
                        linki += [(x["nazwa"], x["url"]) for x in pliki_z_html(dane.decode("utf-8", errors="ignore"), kon)]
                except Exception:
                    pass
            if linki:
                log(f"Znaleziono w internecie {len(linki)} dokumentów naboru – pobieram.")
                with BLOKADA:  # zapamiętaj znalezione adresy przy naborze – kolejne pobranie od razu z nich
                    m2 = meta(pid)
                    n2 = _dot(m2, "wniosek").setdefault("nabor", {})
                    n2["dokumenty"] = (n2.get("dokumenty") or []) + [{"nazwa": a, "url": b} for a, b in linki]
                    if j_.get("strona_naboru", "").startswith("http") and not n2.get("link"):
                        n2["link"] = j_["strona_naboru"]
                    zapisz_meta(pid, m2)
        except Exception as e:
            log(f"Wyszukiwanie dokumentów w internecie nie powiodło się: {opis_bledu_zadania(e, 'dotacje')}")
    if not linki:
        m = meta(pid)
        _dot(m, "wniosek")["pobieranie"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "pobrane": [], "bledy": bledy_stron}
        zapisz_meta(pid, m)
        przyczyna = ("strona naboru nie otworzyła się (" + bledy_stron[0]["blad"][:120] + ")") if bledy_stron else \
            ("na stronie naboru nie ma plików, a wyszukiwanie w internecie ich nie znalazło" if strony else "nabór nie ma zapisanego adresu strony")
        raise ValueError(f"Nie znaleziono plików do pobrania – {przyczyna}. Otwórz stronę naboru w przeglądarce i wgraj regulamin oraz wzór "
                         "wniosku, albo wklej poniżej („Masz inny link?”) adres strony z dokumentami.")
    kat = os.path.join(pdir(pid), "dokumenty")
    os.makedirs(kat, exist_ok=True)
    pobrane, bledy, widz = [], list(bledy_stron), set()
    juz_sa, duplikaty = set(), 0
    for f_ in os.listdir(kat):
        try:
            juz_sa.add(hashlib.sha1(open(os.path.join(kat, f_), "rb").read()).hexdigest())
        except OSError:
            pass
    # tylko pliki dotyczące tego naboru: linki zapisane przy naborze zawsze, ze stron – najlepiej ocenione (bez archiwalnych), najwyżej 20
    odrzucone, niepewne = [], []
    jawne = {url_bezpieczny(u) for _, u in wszystkie}
    ocenione = sorted(((ocena_pliku_naboru(n_, u_, nab) if url_bezpieczny(u_) not in jawne else 99, i, n_, u_) for i, (n_, u_) in enumerate(linki)),
                      key=lambda x: (-x[0], x[1]))
    wybrane = [(n_, u_) for p_, _, n_, u_ in ocenione if p_ > -3][:20]
    pominiete = len(linki) - len(wybrane)
    if pominiete:
        log(f"Pominięto {pominiete} plików archiwalnych lub niezwiązanych z tym naborem (np. dokumenty z poprzednich lat).")
    linki = wybrane
    for nazwa, url in linki[:40]:
        u = url_bezpieczny(url)
        if u in widz:
            continue
        widz.add(u)
        try:
            klucz_p = hashlib.sha1(u.encode()).hexdigest()
            w_pamieci = os.path.join(KAT_PLIKI_NAB, klucz_p)
            if os.path.isfile(w_pamieci + ".bin") and os.path.isfile(w_pamieci + ".json"):
                info = czytaj(w_pamieci + ".json", {})
                dane, typ, kon = open(w_pamieci + ".bin", "rb").read(), info.get("typ", ""), info.get("url", u)
                log(f"Z pamięci programu (pobrany wcześniej): {urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(kon).path))[:70]}")
            else:
                dane, typ, kon = _pobierz_url(url, referer=strona or None)
                if "html" in typ and dane.lstrip()[:1] == b"<":
                    raise ValueError("zamiast pliku serwer zwrócił stronę (plik może wymagać zalogowania)")
                os.makedirs(KAT_PLIKI_NAB, exist_ok=True)
                with open(w_pamieci + ".bin", "wb") as f_:
                    f_.write(dane)
                pisz(w_pamieci + ".json", {"typ": typ, "url": kon, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
            z_adresu = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(kon).path))
            # plik bez nazwy w adresie (np. gov.pl/attachment/<id>) – nazwa z opisu linku, rozszerzenie dopisze popraw_rozszerzenie
            plik = secure_filename_pl(z_adresu) if os.path.splitext(z_adresu)[1].lower() in ROZSZ_DOK else \
                (secure_filename_pl(re.sub(r"\s*\(?\b(pdf|docx?|xlsx?|zip)\b.*$", "", nazwa or "", flags=re.I)[:90]) or secure_filename_pl(z_adresu) or "dokument")
            if hashlib.sha1(dane).hexdigest() in juz_sa:  # ten sam plik już jest w dokumentach wniosku
                log(f"Już jest w dokumentach: {plik[:70]}")
                duplikaty += 1
                continue
            juz_sa.add(hashlib.sha1(dane).hexdigest())
            sc = os.path.join(kat, plik)
            with open(sc, "wb") as f:
                f.write(dane)
            sc = MO.popraw_rozszerzenie(sc) or sc
            zg, opis_zg = zgodnosc_dokumentu(sc, nab)
            if zg == "obcy":  # dokument innego programu / naboru – nie trafia do wniosku
                try:
                    os.remove(sc)
                except OSError:
                    pass
                odrzucone.append({"nazwa": nazwa or plik, "url": url, "powod": opis_zg})
                log(f"Odrzucono (inny nabór): {plik[:70]} – {opis_zg}")
                continue
            pobrane.append(os.path.basename(sc))
            if zg == "niepewny":
                niepewne.append(os.path.basename(sc))
            log(f"Pobrano: {os.path.basename(sc)} ({len(dane) // 1024} kB){' – ' + opis_zg if zg == 'niepewny' else ''}")
        except Exception as e:
            opis = opis_bledu_zadania(e, "dotacje") if not isinstance(e, ValueError) else str(e)
            bledy.append({"nazwa": nazwa or os.path.basename(urllib.parse.urlparse(url).path), "url": url, "blad": opis})
            log(f"Nie pobrano: {nazwa or url[:80]} – {opis}")
    m = meta(pid)
    _dot(m, "wniosek")["pobieranie"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "pobrane": pobrane, "bledy": bledy, "pominiete": pominiete,
                                       "odrzucone": odrzucone, "niepewne": niepewne}
    zapisz_meta(pid, m)
    if not pobrane and duplikaty:
        log(f"Wszystkie dostępne dokumenty ({duplikaty}) są już w punkcie 1.")
        return {"pobrano": 0, "bledy": len(bledy)}
    if not pobrane and odrzucone and not nab.get("_tylko_ai"):
        log(f"Na stronie były tylko dokumenty innych programów (odrzucono {len(odrzucone)}) – szukam dokumentów tego naboru w internecie…")
        with BLOKADA:
            m2 = meta(pid)
            _dot(m2, "wniosek").setdefault("nabor", {})["_tylko_ai"] = True
            zapisz_meta(pid, m2)
        try:
            return praca_pobierz_dok_naboru(log, pid)
        finally:
            with BLOKADA:
                m2 = meta(pid)
                _dot(m2, "wniosek").setdefault("nabor", {}).pop("_tylko_ai", None)
                zapisz_meta(pid, m2)
    if not pobrane:
        if odrzucone:
            raise ValueError(f"Znalezione dokumenty dotyczą innych programów (odrzucono {len(odrzucone)}). Wklej poniżej („Masz inny link?”) adres "
                             f"strony naboru „{nab.get('nazwa') or ''}” albo wgraj regulamin i wzór wniosku z dysku.")
        raise ValueError(f"Nie udało się pobrać żadnego z {len(bledy)} dokumentów – przyczyna: {bledy[0]['blad'] if bledy else 'brak plików'}. "
                         "Linki są w punkcie 1 – pobierz je w przeglądarce i wgraj.")
    log(f"Pobrano dokumentów naboru: {len(pobrane)}" + (f", nie udało się: {len(bledy)} (linki w punkcie 1)." if bledy else ".")
        + " Następny krok: „Ustal wymagania wniosku (AI)”.")
    return {"pobrano": len(pobrane), "bledy": len(bledy)}


# --- nadchodzące nabory: harmonogramy naborów województw i instytucji, alerty

F_HARM = os.path.join(DATA, "dotacje_harmonogramy.json")  # wspólne dla wszystkich kont (dane publiczne)
F_ALERTY_DOT = SciezkaKonta("dotacje_alerty.json")


def harm_dane():
    return czytaj(F_HARM, {}) or {}


def _znajdz_harmonogram(url_portalu, log):
    """Na stronie portalu programu szuka odnośnika „Harmonogram naborów”, a na nim – najnowszego pliku harmonogramu."""
    dane, typ, kon = _pobierz_url(url_portalu)
    h = dane.decode("utf-8", errors="ignore")
    kandydaci = [(u, t) for u, t in linki_html(h, kon) if "harmonogram" in (t or "").lower() or "harmonogram" in u.lower()]
    if not kandydaci:
        for pod in ("dokumenty", "nabory", "dokumenty-programowe"):
            try:
                d2, _, k2 = _pobierz_url(urllib.parse.urljoin(kon, pod))
                kandydaci = [(u, t) for u, t in linki_html(d2.decode("utf-8", errors="ignore"), k2) if "harmonogram" in ((t or "") + u).lower()]
                if kandydaci:
                    break
            except Exception:
                continue
    if not kandydaci:
        return None
    kandydaci.sort(key=lambda x: (0 if "nabor" in _norm((x[1] or "") + x[0]) else 1))
    for u, t in kandydaci[:4]:
        if urllib.parse.urlparse(u).path.lower().endswith(HN.ROZSZ_HARM):
            return u
        try:
            d3, typ3, k3 = _pobierz_url(u)
        except Exception:
            continue
        if "html" not in typ3:
            return k3
        pliki = [x for x in pliki_z_html(d3.decode("utf-8", errors="ignore"), k3)
                 if "harmonogram" in _norm(x["nazwa"] + x["url"]) and x["url"].lower().split("?")[0].endswith(HN.ROZSZ_HARM)]
        if pliki:
            return pliki[0]["url"]  # pierwszy na stronie = zwykle najnowszy
        return k3  # harmonogram jako tabela na stronie
    return None


def praca_odswiez_harmonogramy(log, regiony=None, wymus=False):
    """Pobiera harmonogramy naborów; AI czyta tylko pliki, które zmieniły się od ostatniego pobrania."""
    c = cfg()
    wymagany_klucz(c)
    H = harm_dane()
    zrodla_wlasne = H.get("wlasne_zrodla") or []
    regiony = regiony or list(PORTALE_REGIONALNE.keys()) + sorted({z["region"] for z in zrodla_wlasne} - set(PORTALE_REGIONALNE))
    zm, bez = 0, 0
    for region in regiony:
        zr = [z for z in zrodla_wlasne if z["region"] == region]
        cele = [(z.get("nazwa") or region, z["url"]) for z in zr]
        if not cele and region in PORTALE_REGIONALNE:
            try:
                u = _znajdz_harmonogram(PORTALE_REGIONALNE[region], log)
            except Exception as e:
                u = None
                log(f"{region}: portal niedostępny – {opis_bledu_zadania(e, 'szukaj')}")
            if u:
                cele = [(f"FE dla województwa {region}", u)]
            else:
                H.setdefault("zrodla", {})[region] = {"status": "nie znaleziono harmonogramu – dodaj adres ręcznie", "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
                log(f"{region}: nie znaleziono harmonogramu na portalu.")
                continue
        nowe_nabory = []
        for nazwa, url in cele:
            klucz = f"{region}|{url}"
            st = (H.get("zrodla") or {}).get(klucz) or {}
            try:
                dane, typ, kon = _pobierz_url(url)
            except Exception as e:
                H.setdefault("zrodla", {})[klucz] = {**st, "region": region, "url": url, "status": "błąd pobierania: " + opis_bledu_zadania(e, "pobierz")}
                log(f"{region}: nie pobrano {url[:80]}")
                nowe_nabory += [n for n in (H.get("nabory") or []) if n.get("zrodlo_klucz") == klucz]  # zostają poprzednie dane
                continue
            sk = HN.skrot(dane)
            if st.get("skrot") == sk and not wymus:
                bez += 1
                nowe_nabory += [n for n in (H.get("nabory") or []) if n.get("zrodlo_klucz") == klucz]
                log(f"{region}: harmonogram bez zmian – dane z pamięci programu.")
                continue
            plik = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(kon).path)) or "strona.html"
            if "html" in typ and not plik.lower().endswith(HN.ROZSZ_HARM):
                plik = "strona.html"
            tekst = HN.tekst_pliku(plik, dane)
            if len(tekst) < 200:
                H.setdefault("zrodla", {})[klucz] = {**st, "region": region, "url": url, "status": "plik bez tekstu (np. skan)"}
                continue
            czesci = HN.fragmenty(tekst)
            log(f"{region}: nowy harmonogram ({plik}) – AI odczytuje nabory ({len(czesci)} cz.)…")
            lista = []
            for cz in czesci:
                txt, _ = MO.claude_stream(dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5"), HN.SYSTEM_HARM,
                                          [{"type": "text", "text": HN.polecenie_harmonogramu(cz, region, url, DOT.BRANZE, DOT.WNIOSKODAWCY, dt.date.today().isoformat())}],
                                          max_tokens=16000, log=log)
                lista += [n for n in (HN.wyciagnij(txt).get("nabory") or []) if isinstance(n, dict) and n.get("tytul")]
            teraz = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            for n in lista:
                n.update(region=region, zrodlo_url=kon, zrodlo_nazwa=nazwa, zrodlo_plik=plik, zrodlo_klucz=klucz, aktualizacja=teraz)
                n["id"] = HN.id_naboru(region, n)
            nowe_nabory += lista
            H.setdefault("zrodla", {})[klucz] = {"region": region, "url": url, "plik_url": kon, "plik": plik, "skrot": sk, "data": teraz,
                                                 "status": f"odczytano {len(lista)} naborów", "nazwa": nazwa}
            zm += 1
        H["nabory"] = [n for n in (H.get("nabory") or []) if n.get("region") != region] + nowe_nabory
        H.setdefault("zrodla", {}).pop(region, None)
        pisz(F_HARM, H)
    H["odswiezono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    pisz(F_HARM, H)
    log(f"Gotowe: zaktualizowano {zm} harmonogramów, {bez} bez zmian. Naborów w bazie: {len(H.get('nabory') or [])}.")
    return {"zmienione": zm, "bez_zmian": bez}


def nabory_harmonogramu(filtr, trwajace=False):
    dzis = dt.date.today().isoformat()
    wyn = []
    for n in harm_dane().get("nabory") or []:
        st = HN.status(n, dzis)
        if st == "zakończony" or (st == "trwa" and not trwajace):
            continue
        if HN.pasuje(n, filtr):
            wyn.append(dict(n, status=st))
    return sorted(wyn, key=HN.poczatek)








def alerty_dot():
    return czytaj(F_ALERTY_DOT, {"alerty": [], "wyslane": {}}) or {"alerty": [], "wyslane": {}}






def sprawdz_alerty_dotacji(log=print):
    """Dla każdego konta: nowe nabory pasujące do alertów i przypomnienia przed startem naboru – e-mail (jeśli skonfigurowany)."""
    dzis = dt.date.today()
    for login in wszystkie_konta():
        _KONTEKST.login = login
        try:
            A = alerty_dot()
            if not A.get("alerty"):
                continue
            wys = A.setdefault("wyslane", {})
            do_maila = []
            for a in A["alerty"]:
                for n in nabory_harmonogramu(a):
                    k_nowy, k_przyp = f"{a['id']}|{n['id']}|nowy", f"{a['id']}|{n['id']}|przyp"
                    if k_nowy not in wys:
                        do_maila.append(("Nowy nabór w harmonogramie", a, n))
                        wys[k_nowy] = dzis.isoformat()
                    od = HN.poczatek(n)
                    if od != "9999-12-31" and k_przyp not in wys and 0 <= (dt.date.fromisoformat(od) - dzis).days <= a.get("dni_przed", 14):
                        do_maila.append((f"Nabór rusza za {(dt.date.fromisoformat(od) - dzis).days} dni", a, n))
                        wys[k_przyp] = dzis.isoformat()
            pisz(F_ALERTY_DOT, A)
            c = cfg()
            adresy = [x.strip() for x in re.split(r"[,;\s]+", c.get("powiadomienia_adresy", "") or "") if "@" in x]
            do_maila = [x for x in do_maila if x[1].get("email")]
            if do_maila and adresy and c.get("smtp_serwer"):
                from email.message import EmailMessage
                msg = EmailMessage()
                msg["Subject"] = f"Bidivia – nadchodzące nabory dotacji ({len(do_maila)})"
                msg["From"], msg["To"] = c.get("smtp_nadawca") or c.get("smtp_login"), ", ".join(adresy)
                linie = [f"- [{p}] {n.get('tytul')} – {n.get('region')}, {n.get('program', '')}; termin: "
                         f"{n.get('data_od') or n.get('termin_opis') or '?'}{' – ' + n['data_do'] if n.get('data_do') else ''} (alert: {a['nazwa']})"
                         for p, a, n in do_maila[:60]]
                msg.set_content("Nadchodzące nabory pasujące do Twoich alertów w programie Bidivia:\n\n" + "\n".join(linie)
                                + "\n\nSzczegóły: Dotacje UE/KPO → Nadchodzące nabory.")
                MH.wyslij_smtp(c, [msg])
                log(f"{login}: wysłano powiadomienie o {len(do_maila)} naborach.")
        except Exception as e:
            log(f"{login}: alerty dotacji – {e}")
        finally:
            _KONTEKST.login = None


# ============================================================ PLAN PROJEKTU DOTACYJNEGO (zakres → wycena → budżet → wskaźniki → punkty)
def _plan(m):
    t = _dot(m, "wniosek") if m.get("typ") == "wniosek_dot" else m.setdefault("dotacja", {"dane": {}, "wymagania": None, "zakres": "", "dokumenty": {}})
    return t.setdefault("plan", {"pomysl": "", "pozycje": []})


def _plan_stan(pid, m):
    p = _plan(m)
    prof = cfg().get("dotacje_profil") or {}
    reg = dict(p.get("reguly") or {})
    for k, v in (p.get("reczne") or {}).items():  # wartości wpisane ręcznie mają pierwszeństwo przed analizą
        if v not in ("", None):
            reg[k] = v
    nab = (_dot(m, "wniosek").get("nabor") or {}) if m.get("typ") == "wniosek_dot" else {}
    poz = p.get("pozycje") or []
    b = DP.budzet(poz, reg, nab.get("poziom_dofinansowania"))  # „od 50% do 85%” → 85% (GC-04; wcześniej 5085%)
    w = DP.wskazniki(poz)
    h = DP.harmonogram(poz)
    typ = prof.get("typ") or ""
    wyb, wyb_ostrz = DP.wybor_wykonawcow(poz, typ, reg)  # H3-05: tryb po zsumowaniu tożsamych zamówień (CPV / kategoria)
    return {"plan": p, "reguly": reg, "budzet": b, "wskazniki": w, "harmonogram": h, "wybor": wyb, "wybor_ostrzezenia": wyb_ostrz, "profil": prof,
            "trwalosc": DP.trwalosc(p.get("data_konca"), reg.get("trwalosc_lat"), typ, prof.get("wielkosc")) if p.get("data_konca") else {},
            "katalog": {k: {"nazwa": v["nazwa"], "opis": v["opis"], "pola": v["pola"], "wycena": v["wycena"], "dokumenty": v["dokumenty"]} for k, v in DP.KATALOG.items()},
            "typy_wnioskodawcy": {k: {"nazwa": v["nazwa"], "pola": v["pola"]} for k, v in DP.TYPY_WNIOSKODAWCY.items()},
            "pomoc": DP.POMOC, "adres_firmy": cfg().get("firma_adres", ""),
            "faza": "wniosek" if m.get("typ") == "wniosek_dot" else "rozliczenie", "nazwa": m.get("nazwa"), "id": pid,
            "zapytania": {z.get("pozycja"): z.get("id") for z in p.get("zapytania_poz") or []}}






def _bloki_naboru(pid, log):
    try:
        b, _ = bloki_dotacji(pid, log, limit=300_000)
        return b
    except Exception:
        return []


def praca_plan_analiza(log, pid):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    p = _plan(m)
    nab = _dot(m, "wniosek").get("nabor") or {}
    bloki = _bloki_naboru(pid, log)
    log(f"AI czyta regulamin naboru ({len(bloki)} dokumentów) i ustala, co można sfinansować – działania, kategorie kosztów, limity, punkty…")
    prof = dict(cfg().get("dotacje_profil") or {}, firma=_dane_wnioskodawcy().get("firma_nazwa"))
    tresc = MO.oznacz_dokumenty(bloki, MO.ustawienie_cache(c)) + [{"type": "text", "text": DP.polecenie_analizy(nab, prof, p.get("pomysl"))}]
    txt, _ = MO.claude_stream(c, DP.SYSTEM_PLAN, tresc, max_tokens=12000, log=log)
    r = MO.wyciagnij_json(txt)
    if not isinstance(r, dict):
        raise RuntimeError("AI nie zwróciło analizy naboru – spróbuj ponownie.")
    with BLOKADA:
        m = meta(pid)
        p = _plan(m)
        p["reguly"] = {k: r.get(k) for k in ("kategorie", "intensywnosc_procent", "limit_projektu_zl", "min_koszty_zl", "max_koszty_zl", "vat_kwalifikowalny",
                                             "pomoc", "bur", "trwalosc_lat", "wskazniki_obowiazkowe", "kryteria_punktowe", "typy_wnioskodawcow", "wylaczenia")}
        p["dzialania"] = [d for d in (r.get("dzialania") or []) if isinstance(d, dict)][:40]
        p["analiza_data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        if not p.get("pozycje") and r.get("proponowane_pozycje"):
            p["pozycje"] = [{"id": uuid.uuid4().hex[:8], "nazwa": x.get("nazwa"), "kategoria": x.get("kategoria") if x.get("kategoria") in DP.KATALOG else "inne",
                             "dzialanie": x.get("dzialanie"), "atrybuty": x.get("atrybuty") or {}, "ilosc": x.get("ilosc") or 1}
                            for x in r["proponowane_pozycje"] if isinstance(x, dict)][:30]
        zapisz_meta(pid, m)
    log(f"Gotowe: {len(p['dzialania'])} działań do wyboru.")
    return {"ok": True}


def praca_plan_wycena(log, pid, ids):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    poz = [x for x in _plan(m).get("pozycje") or [] if not ids or x.get("id") in ids]
    if not poz:
        raise ValueError("Brak pozycji do wyceny.")
    region = (cfg().get("dotacje_profil") or {}).get("region") or c.get("centrum_nazwa", "")
    log(f"Sprawdzam aktualne ceny w internecie dla {len(poz)} pozycji…")
    txt, _ = CR.claude_z_wyszukiwaniem(dict(c, _model=c.get("model_oferty") or c.get("model")), "Jesteś kosztorysantem i specjalistą od zakupów. "
                                       "Podajesz tylko ceny znalezione w wiarygodnych źródłach. Odpowiadasz WYŁĄCZNIE JSON-em.",
                                       DP.polecenie_wyceny(poz, region), max_wyszukan=10, max_tokens=6000, log=log)
    r = MO.wyciagnij_json(txt) or {}
    ceny = {x.get("id"): x for x in (r.get("ceny") or []) if isinstance(x, dict)}
    with BLOKADA:
        m = meta(pid)
        n = 0
        for x in _plan(m).get("pozycje") or []:
            cz = ceny.get(x.get("id"))
            if cz and DP._f(cz.get("cena_netto_jednostkowa")):
                x["cena_netto"] = round(DP._f(cz["cena_netto_jednostkowa"]), 2)
                x["zrodlo_ceny"] = f"{cz.get('zrodlo') or 'internet'}{(' – ' + cz['uwagi']) if cz.get('uwagi') else ''} ({dt.date.today():%d.%m.%Y})"[:300]
                n += 1
        zapisz_meta(pid, m)
    log(f"Wyceniono {n} z {len(poz)} pozycji. Pozostałe uzupełnij z ofert albo kosztorysu.")
    return {"wyceniono": n}


def praca_plan_kontrola(log, pid):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    st = _plan_stan(pid, m)
    bloki = _bloki_naboru(pid, log)
    log("AI porównuje projekt z regulaminem i kryteriami punktowymi…")
    prof = dict(st["profil"], firma=_dane_wnioskodawcy().get("firma_nazwa"))
    tresc = MO.oznacz_dokumenty(bloki, MO.ustawienie_cache(c)) + [{"type": "text", "text": DP.polecenie_kontroli(
        _dot(m, "wniosek").get("nabor") or {}, st["plan"], st["budzet"], st["wskazniki"], prof)}]
    txt, _ = MO.claude_stream(c, DP.SYSTEM_PLAN, tresc, max_tokens=10000, log=log)
    r = MO.wyciagnij_json(txt)
    if not isinstance(r, dict):
        raise RuntimeError("AI nie zwróciło wyniku kontroli – spróbuj ponownie.")
    r["uwagi"] = [u for u in r.get("uwagi") or [] if isinstance(u, dict)]
    OD.dodaj(pdir(pid), r["uwagi"])  # odwołania do punktów regulaminu – podgląd po najechaniu
    r["data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with BLOKADA:
        m = meta(pid)
        _plan(m)["kontrola"] = r
        zapisz_meta(pid, m)
    return {"ok": True}
















# ---------- kalkulator SO (wielkość ekonomiczna gospodarstwa) – współczynniki wspólne dla wszystkich kont


def praca_so_wspolczynniki(log, region, wersja):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    log(f"Szukam oficjalnych współczynników SO ({wersja}) dla regionu FADN „{region}”…")
    txt, n = CR.claude_z_wyszukiwaniem(dict(c, _model=c.get("model_oferty") or c.get("model")), "Wyszukujesz oficjalne dane statystyki rolniczej (FADN, IERiGŻ, ARiMR). "
                                       "Podajesz tylko liczby z oficjalnych tabel, ze źródłem. Odpowiadasz WYŁĄCZNIE JSON-em.",
                                       DP.polecenie_so(region, wersja), max_wyszukan=8, max_tokens=6000, log=log)
    r = MO.wyciagnij_json(txt) or {}
    wu = {k: DP._f(v) for k, v in (r.get("uprawy") or {}).items() if DP._f(v)}
    wz = {k: DP._f(v) for k, v in (r.get("zwierzeta") or {}).items() if DP._f(v)}
    if not wu and not wz:
        raise RuntimeError("Nie znaleziono oficjalnych współczynników – wpisz je ręcznie z arkusza ARiMR albo sprawdź wynik w kalkulator-so.pl.")
    with W.BLOKADA:
        d = WSP.czytaj("so_wspolczynniki.json", {})
        d[f"{region}|{wersja}"] = {"uprawy": wu, "zwierzeta": wz, "zrodlo": str(r.get("zrodlo") or "")[:200], "zrodlo_url": str(r.get("zrodlo_url") or "")[:300],
                                   "wersja": str(r.get("wersja") or wersja)[:40], "data": dt.date.today().isoformat()}
        WSP.pisz("so_wspolczynniki.json", d)
    log(f"Znaleziono współczynniki: {len(wu)} upraw, {len(wz)} grup zwierząt (źródło: {r.get('zrodlo') or 'internet'}).")
    return {"ok": True}








@app.post("/api/projekty/<pid>/wniosek-dot/link")
@wymaga_logowania
def dotacje_dodaj_link(pid):
    """Dodatkowy link do strony z dokumentami naboru albo do pliku – i ponowne pobieranie."""
    url = str((request.json or {}).get("url") or "").strip()
    if not re.match(r"https?://", url):
        return jsonify({"blad": "Wklej pełny adres (https://…) strony z dokumentami albo pliku."}), 400
    with BLOKADA:
        m = meta(pid)
        nab = _dot(m, "wniosek").get("nabor") or {}
        _dot(m, "wniosek")["nabor"] = nab
        if urllib.parse.urlparse(url).path.lower().endswith(ROZSZ_DOK):
            nab.setdefault("dokumenty", []).append({"nazwa": "dodany link", "url": url})
        else:
            nab.setdefault("strony_dodatkowe", [])
            if url not in nab["strony_dodatkowe"]:
                nab["strony_dodatkowe"].append(url)
        zapisz_meta(pid, m)
    return jsonify(uruchom("pobierz", "Pobieranie dokumentów naboru", praca_pobierz_dok_naboru, pid))


@app.post("/api/projekty/<pid>/wniosek-dot/pobierz")
@wymaga_logowania
def dotacje_pobierz_ponownie(pid):
    return jsonify(uruchom("pobierz", "Pobieranie dokumentów naboru", praca_pobierz_dok_naboru, pid))


@app.post("/api/projekty/<pid>/rodzaj-zamowienia")
@wymaga_logowania
def rodzaj_zamowienia(pid):
    r = (request.json or {}).get("rodzaj")
    if r not in ZAM.RODZAJE_ZAM:
        return jsonify({"blad": "Wybierz: roboty budowlane, usługi albo dostawy."}), 400
    with BLOKADA:
        m = meta(pid)
        m["rodzaj_zamowienia"] = r
        if isinstance(m.get("kreator"), dict):  # kreator czyta rodzaj ze swoich danych – zmiana w obu miejscach (wcześniej tylko w projekcie)
            m["kreator"]["rodzaj"] = r
        zapisz_meta(pid, m)
    return jsonify({"rodzaj_zamowienia": r})


@app.get("/api/rodzaje-zamowien")
@wymaga_logowania
def rodzaje_zamowien():
    return jsonify(ZAM.RODZAJE_ZAM)


@app.post("/api/projekty/<pid>/kosztorys-wlasny")
@wymaga_logowania
def kosztorys_wlasny(pid):
    """Własny kosztorys inwestora (Excel, PDF): gdy Excel ma typowy układ (Lp., opis, j.m., ilość, cena) – wczytywany od razu;
    inaczej AI przepisuje go dokładnie (bez własnej wyceny) i grupuje w etapy budowy."""
    f = request.files.get("plik")
    if not f:
        return jsonify({"blad": "Wybierz plik z kosztorysem (Excel lub PDF)."}), 400
    d = os.path.join(pdir(pid), "dokumenty")
    os.makedirs(d, exist_ok=True)
    cel = os.path.join(d, secure_filename_pl(f.filename))
    f.save(cel)
    cel = MO.popraw_rozszerzenie(cel)
    m = meta(pid)
    przetarg_ = (m.get("typ") or "przetarg") == "przetarg"
    if cel.lower().endswith((".xlsx", ".xlsm")) and not przetarg_:  # przetarg: AI czyta też SWZ, by uzupełnić dane do formularzy
        try:
            _, poz = MM.wczytaj_kosztorys(cel)
        except Exception:
            poz = []
        if poz and sum(1 for p in poz if p.get("cena")) >= max(1, len(poz) // 2):
            dzialy = {}
            for p in poz:
                dzialy.setdefault(p.get("dzial") or "1. Kosztorys inwestora", []).append(
                    [p.get("podstawa", ""), p["opis"], p["jm"], p["ilosc"], p["cena"], 0, "kosztorys własny inwestora", ""])
            dane = {"postepowanie": {"nazwa_zamowienia": m.get("nazwa", ""), "vat": None},
                    "dzialy": [{"nazwa": k, "pozycje": v} for k, v in dzialy.items()],
                    "podsumowanie": f"Kosztorys wczytany z pliku {os.path.basename(cel)} ({len(poz)} pozycji).",
                    "do_weryfikacji": [], "ryzyka": [], "pytania_do_zamawiajacego": []}
            dane = MO.przelicz(dane)
            pisz(os.path.join(pdir(pid), "oferta_dane_oryginal.json"), dane)
            zapisz_oferte(pid, dane, cfg())
            return jsonify({"wczytano": len(poz), "oferta": meta(pid).get("oferta")})
    m["kosztorys_wlasny"] = True
    poprzednie = list(m.get("pominiete") or [])
    if not przetarg_:
        m["pominiete"] = [p["sciezka"] for p in lista_plikow(pid) if os.path.join(d, p["sciezka"]) != cel]  # AI czyta tylko ten kosztorys
    zapisz_meta(pid, m)

    def praca(log):
        try:
            return praca_oferta(log, pid, f"Przepisz kosztorys z pliku {os.path.basename(cel)}.")
        finally:
            m2 = meta(pid)
            m2.pop("kosztorys_wlasny", None)
            m2["pominiete"] = poprzednie
            zapisz_meta(pid, m2)
    return jsonify({"zadanie": uruchom("oferta", "Wczytywanie własnego kosztorysu", praca)})


def zapisz_kosztorys_pusty(pid, dane):
    """Kosztorys ślepy (bez cen) dla wykonawców: pozycje i ilości z kosztorysu projektu, żółte pola na ceny jednostkowe,
    wartości, sumy działów, VAT i brutto liczone formułami Excela."""
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    m, c = meta(pid), cfg()
    r = realizacja_dane(pid) if m.get("status_projektu") else {}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kosztorys do wyceny"
    zolte = PatternFill("solid", fgColor="FFF7CC")
    szare = PatternFill("solid", fgColor="E8EEF8")
    cienka = Side(style="thin", color="B7C0CC")
    ramka = Border(left=cienka, right=cienka, top=cienka, bottom=cienka)
    pog = Font(bold=True)
    for kol, sz in zip("ABCDEFG", (6, 62, 8, 11, 15, 17, 30)):
        ws.column_dimensions[kol].width = sz
    w = 1

    def pole(etykieta, wartosc="", do_wpisania=False):
        nonlocal w
        ws.cell(w, 1, etykieta).font = pog
        ws.merge_cells(start_row=w, start_column=1, end_row=w, end_column=2)
        k = ws.cell(w, 3, wartosc)
        ws.merge_cells(start_row=w, start_column=3, end_row=w, end_column=7)
        if do_wpisania:
            for kk in range(3, 8):
                ws.cell(w, kk).fill = zolte
                ws.cell(w, kk).border = ramka
        w += 1
        return k
    rz_ = m.get("rodzaj_zamowienia") if m.get("typ") in INWESTORSKIE else ""
    t = ws.cell(w, 1, {"dostawy": "FORMULARZ ASORTYMENTOWO-CENOWY – DO WYPEŁNIENIA PRZEZ WYKONAWCĘ (załącznik do SWZ / zapytania)",
                       "uslugi": "FORMULARZ CENOWY – DO WYPEŁNIENIA PRZEZ WYKONAWCĘ (załącznik do SWZ / zapytania)"}.get(rz_, "KOSZTORYS OFERTOWY (ŚLEPY) – DO WYCENY PRZEZ WYKONAWCĘ"))
    t.font = Font(bold=True, size=14)
    ws.merge_cells(start_row=w, start_column=1, end_row=w, end_column=7)
    w += 2
    pole("Zamawiający:" if m.get("typ") in INWESTORSKIE else "Inwestor:",
         zamawiajacy_projektu(m, (dane or {}).get("postepowanie") or {}) if m.get("typ") in INWESTORSKIE
         else ", ".join(x for x in (c.get("firma_nazwa", ""), c.get("firma_adres", ""), c.get("firma_tel", ""), c.get("firma_email", "")) if x))
    pole("Budowa:", m.get("nazwa", ""))
    pole("Adres budowy:", r.get("adres") or (dane.get("postepowanie") or {}).get("obiekt", ""))
    w += 1
    for et in ("Wykonawca (nazwa, adres):", "NIP wykonawcy:", "Telefon / e-mail:", "Proponowany termin realizacji:",
               "Okres gwarancji [miesiące]:", "Oferta ważna do:"):
        pole(et, "", True)
    w += 1
    uw = ws.cell(w, 1, "Proszę wpisać ceny jednostkowe netto w żółtych polach kolumny E – wartości, sumy, VAT i kwota brutto policzą się same. "
                       "Cena jednostkowa obejmuje materiał, robociznę, sprzęt, transport, koszty pośrednie i zysk. Ilości wynikają z projektu budowlanego; "
                       "uwagi do pozycji (np. inna technologia, wątpliwości co do ilości) proszę wpisać w kolumnie G.")
    uw.alignment = Alignment(wrap_text=True, vertical="top")
    uw.font = Font(italic=True, size=9)
    ws.merge_cells(start_row=w, start_column=1, end_row=w, end_column=7)
    ws.row_dimensions[w].height = 42
    w += 2
    nag = ("Lp.", "Opis robót", "j.m.", "Ilość", "Cena jedn. netto [zł]", "Wartość netto [zł]", "Uwagi wykonawcy")
    for kk, n in enumerate(nag, 1):
        x = ws.cell(w, kk, n)
        x.font, x.fill, x.border = pog, szare, ramka
        x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = ws.cell(w + 1, 1)
    w += 1
    sumy = []
    for dz in dane.get("dzialy", []):
        x = ws.cell(w, 1, dz.get("nazwa", ""))
        x.font, x.fill = pog, szare
        ws.merge_cells(start_row=w, start_column=1, end_row=w, end_column=7)
        w += 1
        pocz = w
        for i, p in enumerate(dz.get("pozycje", []), 1):
            opis, jm, il = (p[1], p[2], p[3]) if isinstance(p, (list, tuple)) else (p.get("opis"), p.get("jm"), p.get("ilosc"))
            wart = (i, opis, jm, il, None, f"=IF(E{w}=\"\",\"\",ROUND(D{w}*E{w},2))", None)
            for kk, v in enumerate(wart, 1):
                x = ws.cell(w, kk, v)
                x.border = ramka
                x.alignment = Alignment(wrap_text=kk in (2, 7), vertical="top")
            ws.cell(w, 5).fill = zolte
            ws.cell(w, 4).number_format = "#,##0.00"
            ws.cell(w, 5).number_format = ws.cell(w, 6).number_format = "#,##0.00"
            w += 1
        x = ws.cell(w, 5, f"Razem {dz.get('nazwa', '')[:40]}:")
        x.font = pog
        x.alignment = Alignment(horizontal="right")
        s_ = ws.cell(w, 6, f"=SUM(F{pocz}:F{w - 1})")
        s_.font, s_.number_format, s_.border = pog, "#,##0.00", ramka
        sumy.append(f"F{w}")
        w += 2
    wiersze_sum = [("RAZEM NETTO [zł]", "=" + "+".join(sumy) if sumy else "=0")]
    for et, f in wiersze_sum:
        ws.cell(w, 5, et).font = pog
        x = ws.cell(w, 6, f)
        x.font, x.number_format, x.border = pog, "#,##0.00", ramka
        netto = w
        w += 1
    ws.cell(w, 5, "Stawka VAT [%]").font = pog
    v = ws.cell(w, 6, None)
    v.fill, v.border = zolte, ramka
    vat = w
    w += 1
    ws.cell(w, 5, "VAT [zł]").font = pog
    x = ws.cell(w, 6, f"=IF(F{vat}=\"\",\"\",ROUND(F{netto}*F{vat}/100,2))")
    x.number_format, x.border = "#,##0.00", ramka
    vk = w
    w += 1
    ws.cell(w, 5, "RAZEM BRUTTO [zł]").font = pog
    x = ws.cell(w, 6, f"=IF(F{vat}=\"\",\"\",F{netto}+F{vk})")
    x.font, x.number_format, x.border = Font(bold=True, size=12), "#,##0.00", ramka
    w += 3
    ws.cell(w, 5, "…………………………………………")
    ws.cell(w + 1, 5, "data, podpis i pieczęć Wykonawcy").font = Font(italic=True, size=9)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    nazwa = ({"dostawy": "Formularz_asortymentowo-cenowy_dla_wykonawcow_", "uslugi": "Formularz_cenowy_dla_wykonawcow_"}.get(rz_, "Kosztorys_do_wyceny_")
             + f"{MO.bezpieczna_nazwa(m.get('nazwa', 'budowa'))[:50]}.xlsx")
    wb.save(os.path.join(pdir(pid), nazwa))
    m = meta(pid)
    m["kosztorys_pusty"] = nazwa
    zapisz_meta(pid, m)
    return nazwa


@app.post("/api/projekty/<pid>/kosztorys-pusty")
@wymaga_logowania
def kosztorys_pusty(pid):
    """Pusty (ślepy) kosztorys dla wykonawców. Gdy projekt nie ma jeszcze kosztorysu – najpierw AI przygotuje go z projektu."""
    d = pdir(pid)
    dane = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or czytaj(os.path.join(d, "oferta_dane.json"), None)
    if dane and dane.get("dzialy"):
        n = zapisz_kosztorys_pusty(pid, dane)
        return jsonify({"plik": n, "url": f"/pobierz/{pid}/{urllib.parse.quote(n)}"})
    if not lista_plikow(pid):
        return jsonify({"blad": "Najpierw wgraj dokumenty w kroku 1 (projekt, przedmiar albo wykaz potrzeb)."}), 400

    def praca(log):
        praca_oferta(log, pid, "")
        dane_ = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or czytaj(os.path.join(d, "oferta_dane.json"), None)
        n = zapisz_kosztorys_pusty(pid, dane_)
        log(f"Gotowe: {n} – do wysłania wykonawcom / dołączenia do SWZ.")
        return {"plik": n}
    return jsonify({"zadanie": uruchom("oferta", "Pusty kosztorys dla wykonawców", praca)})










@app.post("/api/projekty/<pid>/notatka-szacowania")
@wymaga_logowania
def notatka_szacowania(pid):
    """Notatka z szacowania wartości zamówienia (art. 28–36 Pzp). Zamawiający publiczny – z podstawy ustalenia wartości (kosztorys inwestorski,
    PFU, rozeznanie rynku, zamówienia powtarzające się), nie z kosztorysu AI. Zamawiający prywatny – jak dotąd (szacunek kosztów)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    m, j = meta(pid), request.json or {}
    K_ = m.get("kreator") or {}
    if RZ.reguly(K_.get("prywatny")).dokument_podstawy:
        rz_ = K_.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
        nazwa = f"Notatka_z_szacowania_wartosci_{MO.bezpieczna_nazwa(m.get('nazwa', 'zamowienie'))[:50]}.docx"
        w = SZ.notatka_docx(os.path.join(pdir(pid), nazwa), K_.get("szacowanie") or {}, rz_, m.get("nazwa") or "",
                            zamawiajacy_projektu(m, (czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie") or {}),
                            K_.get("data_wszczecia") or None)
        with BLOKADA:
            m = meta(pid)
            m["notatka_szac"] = nazwa
            zapisz_meta(pid, m)
        tw = PR.tryb_wedlug_wartosci(w["netto"] or 0, rz_, K_.get("data_wszczecia") or None)
        return jsonify({"plik": nazwa, "url": f"/pobierz/{pid}/{urllib.parse.quote(nazwa)}", "tryb": tw, "kompletne": w["kompletne"]})
    o = m.get("oferta") or {}
    dane = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    rz = m.get("rodzaj_zamowienia") or "roboty"
    netto = float(o.get("netto") or 0)
    opcje = sum(float(dz.get("suma") or 0) for dz in dane.get("dzialy") or [] if re.search(r"(?i)opcj|przewidzian", str(dz.get("nazwa") or "")))
    data_sz = str(j.get("data") or dt.date.today().isoformat())[:10]
    tw = PR.tryb_wedlug_wartosci(netto, rz, j.get("data_wszczecia") or None, bool(j.get("centralny")))
    waznosc = 6 if rz == "roboty" else 3
    d = MO._doc()
    MO._akapit(d, zamawiajacy_projektu(m, (czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie") or {}), pogrub=True)
    MO._akapit(d, "NOTATKA Z SZACOWANIA WARTOŚCI ZAMÓWIENIA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "art. 28–36 ustawy Prawo zamówień publicznych", kursywa=True, rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._tabela(d, [["Element", "Dane"],
                   ["Przedmiot zamówienia", m.get("nazwa") or ""],
                   ["Rodzaj zamówienia", {"roboty": "roboty budowlane", "dostawy": "dostawy", "uslugi": "usługi"}.get(rz, rz)],
                   ["Data ustalenia wartości", data_sz],
                   ["Metoda", {"roboty": "kosztorys inwestorski (dokumentacja projektowa, przedmiar, ceny rynkowe)",
                               "dostawy": "kosztorys inwestorski – aktualne ceny rynkowe towarów z dostawą (rozeznanie cen)",
                               "uslugi": "kosztorys inwestorski – stawki rynkowe × zakres i okres świadczenia usług"}.get(rz, "")],
                   ["Źródła cen", str(j.get("zrodla") or "ceny rynkowe sprawdzone w internecie i publikacjach cenowych (szczegóły w kosztorysie inwestorskim)")],
                   ["Wartość zamówienia netto (bez VAT)", MO.zl(netto)],
                   ["w tym prawo opcji / zamówienia przewidziane w umowie", MO.zl(opcje) if opcje else "brak"],
                   ["Równowartość w euro", f"{PR.euro(tw['euro'])} (kurs {PR.kurs_pl(tw['kurs'])})"],
                   ["Kwota brutto (do zabezpieczenia środków – informacyjnie)", MO.zl(float(o.get("brutto") or 0))],
                   ["Próg stosowania Pzp", MO.zl(tw["prog_pzp"]) + " netto"],
                   ["Próg unijny", f"{PR.euro(tw['prog_ue_eur'], 0)} = {PR.zl(tw['prog_ue_zl'])}"],
                   ["Wniosek – tryb", tw["opis"]],
                   ["Ważność szacowania", f"wartość ustalona nie wcześniej niż {waznosc} miesięcy przed wszczęciem postępowania ({'roboty budowlane' if rz == 'roboty' else 'dostawy i usługi'})"]])
    MO._akapit(d, "Sprawdź, czy zamówienia tego samego rodzaju w roku budżetowym nie podlegają łącznemu szacowaniu (zakaz dzielenia zamówienia). "
                  "Kurs euro i progi unijne według obwieszczenia Prezesa UZP na lata 2026–2027 – zweryfikuj z aktualnym obwieszczeniem.", kursywa=True, rozmiar=8)
    MO._akapit(d, "\n\nSporządził(a): .................................................          Zatwierdził(a): .................................................")
    nazwa = f"Notatka_z_szacowania_wartosci_{MO.bezpieczna_nazwa(m.get('nazwa', 'zamowienie'))[:50]}.docx"
    MO.zapisz_z_zaznaczeniem(d, os.path.join(pdir(pid), nazwa))
    with BLOKADA:
        m = meta(pid)
        m["notatka_szac"] = nazwa
        zapisz_meta(pid, m)
    return jsonify({"plik": nazwa, "url": f"/pobierz/{pid}/{urllib.parse.quote(nazwa)}", "tryb": tw})


@app.post("/api/projekty/<pid>/vat")
@wymaga_logowania
def zmien_vat(pid):
    """Zmiana stawki VAT gotowej oferty / kosztorysu – przelicza kosztorys, formularze i kwoty."""
    try:
        v = MO.liczba_pl(str((request.json or {}).get("vat", "")).replace("%", ""))
        v = v / 100 if v > 1 else v
        assert 0 <= v <= 0.3
    except (ValueError, AssertionError):
        return jsonify({"blad": "Wybierz stawkę VAT."}), 400
    d = pdir(pid)
    orig = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not orig:
        return jsonify({"blad": "Najpierw przygotuj ofertę lub kosztorys."}), 400
    orig.setdefault("postepowanie", {})["vat"] = v
    orig["do_weryfikacji"] = [x for x in orig.get("do_weryfikacji", []) if not str(x).startswith("Stawka VAT nie wynika")]
    pisz(os.path.join(d, "oferta_dane_oryginal.json"), orig)
    m = meta(pid)
    m["vat_wybor"] = str(v)
    zapisz_meta(pid, m)
    kor = (m.get("oferta") or {}).get("korekta")
    blad = zastosuj_korekte(pid, orig, kor.get("tryb") if kor else None, kor.get("wartosc") if kor else None)
    if blad:
        return jsonify({"blad": blad}), 400
    return jsonify(meta(pid).get("oferta"))


# ---------- materiały

def praca_materialy(log, pid, wskazowki, kosztorys):
    c = cfg()
    wymagany_klucz(c)
    d = pdir(pid)
    kosz = os.path.join(d, kosztorys) if kosztorys else None
    if not kosz or not os.path.isfile(kosz):
        raise ValueError("Najpierw przygotuj kosztorys ofertowy albo wgraj własny kosztorys (xlsx).")
    tytul, pozycje = MM.wczytaj_kosztorys(kosz)
    aktywne = [p for p in pozycje if p["ilosc"] > 0]
    log(f"Kosztorys: {len(aktywne)} pozycji z ilością > 0")
    ost = [0]

    def postep(n):
        if n - ost[0] > 4000:
            ost[0] = n
            log(f"AI dobiera materiały… {n // 1000} tys. znaków")
    txt, powod = MO.claude_stream(c, MM.SYSTEM_MAT, [{"type": "text", "text": MM.zbuduj_polecenie_mat(aktywne, wskazowki, (meta(pid).get("oferta") or {}).get("obiekt", "") or region_domyslny(c))}],
                                  postep=postep, log=log)
    with open(os.path.join(d, "odpowiedz_ai_materialy.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    if powod == "max_tokens":
        log("Uwaga: odpowiedź AI została ucięta – lista może być niepełna.")
    dane = MM.wyciagnij_json(txt)
    if c.get("ceny_internet", True):
        try:
            CR.weryfikuj_materialy(c, dane, aktywne, log, (meta(pid).get("oferta") or {}).get("obiekt", ""))
        except Exception as e:
            log(f"Nie udało się pobrać cen materiałów z internetu ({e}) – zostają szacunki AI.")
    lista, wiersze, razem = MM.przelicz_materialy(dane, aktywne)
    nazwa = re.sub(r"^Kosztorys_ofertowy_", "", os.path.splitext(os.path.basename(kosz))[0])
    wyj = f"Lista_materialow_{nazwa}.xlsx"
    MM.zapisz_liste(tytul, pozycje, dane, lista, wiersze, os.path.join(d, wyj), kosz)
    netto = sum(p["ilosc"] * p["cena"] for p in pozycje)
    m = meta(pid)
    m["lista_materialow"] = wyj
    m["materialy"] = {"liczba": len(lista), "razem": razem, "udzial": razem / netto if netto else None,
                      "najwieksze": [{"nazwa": x["nazwa"], "ilosc": x["do_zam"], "jm": x["jm"], "wartosc": x["wartosc"]}
                                     for x in sorted(lista, key=lambda x: -x["wartosc"])[:8]],
                      "uslugi": len(dane.get("uslugi", [])), "uwagi": dane.get("uwagi_ogolne", [])}
    zapisz_meta(pid, m)
    log(f"Gotowe: {len(lista)} materiałów, {MO.zl(razem)} netto")
    return m["materialy"]


@app.post("/api/projekty/<pid>/materialy")
@wymaga_logowania
def materialy(pid):
    kosz = request.json.get("kosztorys") or meta(pid).get("kosztorys")
    return jsonify(uruchom("materialy", "Zapotrzebowanie materiałowe", praca_materialy, pid,
                           request.json.get("wskazowki", ""), kosz))


# ---------- harmonogram

def praca_harmonogram(log, pid, p):
    c = cfg()
    wymagany_klucz(c)
    d = pdir(pid)
    m = meta(pid)
    lista = p.get("lista") or m.get("lista_materialow")
    if not lista or not os.path.isfile(os.path.join(d, lista)):
        raise ValueError("Najpierw utwórz listę materiałów albo wgraj własną (xlsx).")
    materialy_ = MH.wczytaj_liste(os.path.join(d, lista))
    start = MH.parsuj_date(p.get("start", ""))
    n, dl = int(p.get("etapy", 5)), int(p.get("dlugosc", 7))
    try:
        liczba = max(1, int(p.get("pracownicy") or 0))
    except ValueError:
        raise ValueError("Podaj liczbę pracowników.")
    prac = {x["id"]: x for x in dane_prac_konta()["pracownicy"]}
    wybrani = [prac[i] for i in p.get("wybrani", []) if i in prac]
    liczba = max(liczba, len(wybrani))
    bryg = "1 pracownik" if liczba == 1 else f"{liczba} pracowników"
    if wybrani:
        bryg += " – w tym: " + ", ".join(f"{x['imie']}" + (f" ({x['stanowisko']})" if x.get("stanowisko") else "") for x in wybrani)
        if liczba > len(wybrani):
            bryg += f" oraz {liczba - len(wybrani)} dodatkowych"
    pozycje = []
    if m.get("kosztorys") and os.path.isfile(os.path.join(d, m["kosztorys"])):
        pozycje = MM.wczytaj_kosztorys(os.path.join(d, m["kosztorys"]))[1]
    log(f"{len(materialy_)} materiałów, {n} etapów po {dl} dni od {start:%d.%m.%Y}; zespół: {bryg}")
    txt, _ = MO.claude_stream(c, MH.SYSTEM_HARM, [{"type": "text", "text": MH.zbuduj_polecenie_harm(
        materialy_, pozycje, start, n, dl, bryg, p.get("wskazowki", ""))}], max_tokens=16000, log=log)
    dane = MH.wyciagnij_json(txt)
    etapy = MH.przygotuj_plan(dane, materialy_, start, n, dl)
    budowa = (p.get("budowa") or m.get("nazwa") or "budowa").strip()
    nazwa = re.sub(r"[^\w\-]+", "_", budowa).strip("_")[:60] or "budowa"
    xlsx = f"Harmonogram_dostaw_{nazwa}.xlsx"
    MH.zapisz_harmonogram(os.path.join(d, xlsx), budowa, p.get("adres", ""), etapy, materialy_, dane.get("uwagi", []), bryg)
    js = os.path.join(d, os.path.splitext(xlsx)[0] + ".json")
    with open(js, "w", encoding="utf-8") as f:
        json.dump({"budowa": budowa, "adres": p.get("adres", ""),
                   "etapy": [dict(e, od=e["od"].isoformat(), do=e["do"].isoformat()) for e in etapy],
                   "materialy": materialy_, "uwagi": dane.get("uwagi", [])}, f, ensure_ascii=False, indent=1)
    m = meta(pid)
    m["harmonogram_json"] = os.path.basename(js)
    m["harmonogram_uwagi"] = dane.get("uwagi", [])
    m["harmonogram_zespol"] = {"liczba": liczba, "wybrani": [x["id"] for x in wybrani], "opis": bryg}
    zapisz_meta(pid, m)
    log("Gotowe.")
    return {"etapy": n}


@app.post("/api/projekty/<pid>/harmonogram")
@wymaga_logowania
def harmonogram(pid):
    p = dict(request.json or {})
    try:  # błędne dane – od razu komunikat, bez uruchamiania AI
        MH.parsuj_date(p.get("start", ""))
        n, dl = int(p.get("etapy", 5)), int(p.get("dlugosc", 7))
    except (TypeError, ValueError) as e:
        return jsonify({"blad": str(e) if "data" in str(e).lower() else "Liczba etapów i długość etapu muszą być liczbami całkowitymi."}), 400
    if not (1 <= n <= 52) or not (1 <= dl <= 365):
        return jsonify({"blad": "Liczba etapów: 1–52, długość etapu: 1–365 dni."}), 400
    return jsonify(uruchom("harmonogram", "Harmonogram dostaw", praca_harmonogram, pid, p))


@app.post("/api/projekty/<pid>/wgraj-wynik")
@wymaga_logowania
def wgraj_wynik(pid):
    """Wgranie własnego kosztorysu / listy materiałów / poprawionego harmonogramu (xlsx)."""
    f = request.files.get("plik")
    rodzaj = request.form.get("rodzaj")
    if not f or not f.filename.lower().endswith(".xlsx"):
        return jsonify({"blad": "Wybierz plik .xlsx"}), 400
    d = pdir(pid)
    m = meta(pid)
    if rodzaj == "harmonogram":
        if not m.get("harmonogram_json"):
            return jsonify({"blad": "Najpierw utwórz harmonogram w programie."}), 400
        f.save(os.path.join(d, os.path.splitext(m["harmonogram_json"])[0] + ".xlsx"))
    else:
        nazwa = secure_filename_pl(f.filename)
        f.save(os.path.join(d, nazwa))
        m["kosztorys" if rodzaj == "kosztorys" else "lista_materialow"] = nazwa
        zapisz_meta(pid, m)
    return jsonify({"ok": True})


# ---------- zamówienia



def dane_zamowienia(pid, p):
    d = pdir(pid)
    m = meta(pid)
    if not m.get("harmonogram_json"):
        raise ValueError("Najpierw utwórz harmonogram dostaw.")
    h = MH.wczytaj_harmonogram(os.path.join(d, m["harmonogram_json"]))
    if p.get("adres"):
        h["adres"] = p["adres"]
    k = int(p.get("etap", 0))
    if not 0 <= k < len(h["etapy"]):  # ujemny numer wybrałby po cichu ostatni etap
        raise IndexError("Nie ma takiego etapu w harmonogramie.")
    return h, k, h["etapy"][k]






@app.get("/api/historia")
@wymaga_logowania
def historia():
    h = czytaj(F_HIST, [])
    if rola_sesji() != "admin":
        widoczne = {pid for pid in os.listdir(PROJ) if ma_dostep(czytaj(os.path.join(PROJ, pid, "projekt.json"), {}))}
        h = [x for x in h if x.get("projekt") in widoczne]
    return jsonify(h[:200])


@app.post("/api/projekty/<pid>/dostep")
@wymaga_logowania
@tylko_admin
def projekt_dostep(pid):
    """Administrator zmienia właściciela projektu i listę osób, którym projekt jest udostępniony. Administrator konta (firmy) – tylko
    w obrębie swojej firmy: projekt przekazuje między sobą a osobami ze swojej firmy i udostępnia swoje projekty tylko im (H1-01)."""
    loginy = {u["login"].lower(): u["login"] for u in uzytkownicy_lista()}
    loginy[login_admina().lower()] = login_admina()
    adm = login_admina().lower()
    if not wlasciciel():
        swoi = UWIERZ.czlonkowie_firmy()
        loginy = {k: v for k, v in loginy.items() if k in swoi}
        adm = str(session.get("login") or "").lower()  # „administrator” w regułach poniżej = administrator tej firmy
    wl = str(request.json.get("wlasciciel", "")).strip().lower()
    if wl not in loginy:
        return jsonify({"blad": "Nieznany użytkownik."}), 400
    m = meta(pid)
    stary = (m.get("wlasciciel") or login_admina()).lower()
    if not wlasciciel() and stary not in loginy:
        return jsonify({"blad": "Projekt nie należy do Twojej firmy – dostęp zmienia jego właściciel."}), 403
    if wl != stary and adm not in (wl, stary):
        return jsonify({"blad": "Projekt można przekazać tylko między administratorem a użytkownikiem – nie między dwoma użytkownikami."}), 400
    m["wlasciciel"] = loginy[wl]
    # udostępniać innym użytkownikom można tylko projekty administratora; projekt użytkownika widzi on i administrator
    m["dostep"] = sorted({loginy[x.lower()] for x in request.json.get("dostep", []) if x.lower() in loginy and x.lower() != wl}) if wl == adm else []
    zapisz_meta(pid, m)
    return jsonify({"wlasciciel": m["wlasciciel"], "dostep": m["dostep"]})


# ============================================================ pobieranie plików

@app.get("/pobierz/<pid>/<path:rel>")
@wymaga_logowania
def pobierz(pid, rel):
    d = os.path.realpath(pdir(pid))
    p = os.path.realpath(os.path.join(d, rel))
    if not p.startswith(d + os.sep) or not os.path.isfile(p):
        abort(404)
    wzgl = os.path.relpath(p, d).replace(os.sep, "/")
    if ("/" not in wzgl and wzgl.lower().endswith(".json")) or wzgl.lower().endswith((".tmp", ".lock")) \
            or any(cz.startswith(".") for cz in wzgl.split("/")):
        abort(404)  # pliki wewnętrzne projektu (projekt.json z listą udostępnień, dane kosztorysu, realizacji) – tylko przez API
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


# ============================================================ hurtownie, cennik, ustawienia





POMIN = {"folder_ofert", "ceny_z_cennika", "stawka_rg", "kp", "zysk", "centrum_nazwa", "centrum_lat", "centrum_lon",
         "promien_km", "miejscowosci", "frazy_zawsze", "wykluczenia"}
POLA = [(k, e, t) for k, e, t in core.POLA_USTAWIEN if k not in POMIN] + [
    ("marka_nazwa", "Nazwa programu (marka resellera – zamiast „Bidivia” w tytule, menu i na stronie logowania; puste = Bidivia)", "text"),
    ("marka_kolor", "Kolor wiodący marki (np. #1F5A99; puste = domyślny)", "text")]
_i = [k for k, _, _ in POLA].index("vat")
POLA.pop(_i)  # bez domyślnej stawki VAT – stawkę ustala się z zamawiającym lub z warunków przetargu (wybór przy ofercie)
POLA[_i:_i] = [
    ("firma_z_wykazu", "Nazwę firmy, adres i REGON wykonawcy pobieraj z wykazu VAT / CEIDG po NIP (do wszystkich dokumentów)", "bool"),
    ("ceidg_token", "Token API CEIDG (bezpłatny, biznes.gov.pl) – pełne nazwy firm jednoosobowych, np. „K.A. Jakub Górski”", "secret"),
    ("powiadomienia", "Wysyłaj codzienny raport e-mail po automatycznym wyszukiwaniu (nowe przetargi, terminy, zaległości)", "bool"),
    ("powiadomienia_adresy", "Adresy e-mail do raportu (po przecinku)", "str"),
    ("powiadomienia_min_ocena", "Minimalna ocena AI przetargu w raporcie (1–10)", "int"),
    ("bip_w_wyszukiwaniu", "Sprawdzaj obserwowane strony BIP przy każdym wyszukiwaniu przetargów", "bool"),
    ("model_lekki", "Model AI do czatu pomocy – najtańszy (dokumentów i danych do wyceny nie czyta)", "str"),
    ("model_oferty", "Model AI do kosztorysów, ofert, wniosków i dokumentów", "str"),
    ("model_dokladny", "Model AI do weryfikacji dokumentacji i sprawdzania wniosków (najdokładniejszy, najdroższy)", "str"),
    ("pdf_jako_tekst", "Wysyłaj do AI pliki PDF z warstwą tekstową jako tekst (kilkukrotnie taniej; skany i rysunki zawsze jako obraz)", "bool"),
    ("pomijaj_rysunki", "W zadaniach tekstowych (wykrywanie błędów, dokumenty, asystent, analizy) pomijaj rysunki PDF i ograniczaj długie skany do 30 stron", "bool"),
    ("profil_dostawcy", "Profil firmy – DOSTAWY i USŁUGI (co dostarczasz, jakie usługi świadczysz, w jakim regionie) – do oceny przetargów w trybie Dostawca/Usługodawca", "text"),
    ("ocena_paczkami", "Oceniaj nowe przetargi paczkami (szybka ocena wielu ogłoszeń jednym zapytaniem – kilkukrotnie taniej)", "bool"),
    ("bk_limit_ai", "Raport zwycięzców: najwyżej tyle odczytów rozstrzygnięć z Bazy Konkurencyjności przez AI na jeden raport (0 = bez AI)", "int"),
    ("prog_pelnej_oceny", "Szczegółowa ocena z ogłoszenia tylko dla przetargów z szybką oceną co najmniej (1–10)", "int"),
    ("sito_prog", "Wstępne sito bez AI przed oceną (punkty: słowo w tytule 3, kod CPV 3, słowo tylko w treści 1; 2 = domyślnie, 0 = wyłączone)", "int"),
    ("cache_ai", "Pamięć podręczna AI (prompt caching) dla dokumentów przetargu", "wybor:1h=1 godzina (zalecane – kolejne zadania na tych samych dokumentach taniej)|5m=5 minut|brak=wyłączona"),
    ("ceny_internet", "Sprawdzaj aktualne ceny rynkowe w internecie (oferta i materiały)", "bool"),
    ("ceny_internet_pozycje", "Sprawdzanie cen w internecie: co najmniej tyle najdroższych pozycji kosztorysu (0 = wyłącz)", "int"),
    ("ceny_internet_udzial", "Sprawdzanie cen w internecie: pozycje tworzące razem tyle procent wartości kosztorysu", "int"),
    ("ceny_internet_max", "Sprawdzanie cen w internecie: nie więcej niż tyle pozycji w jednym kosztorysie", "int"),
    ("ceny_internet_materialy", "Ile najważniejszych materiałów sprawdzać w internecie", "int"),
    ("ceny_internet_wyszukan", "Maks. liczba wyszukiwań na jedno sprawdzenie", "int"),
]
POLA_WEB = [k for k, _, _ in POLA]




def _odswiez_firme_po_zapisie():
    c = cfg_surowy()
    if c.get("firma_z_wykazu", True) and NIP.poprawny(c.get("firma_nip")):
        _ODSWIEZANE.pop(NIP.oczysc(c["firma_nip"]), None)
        threading.Thread(target=lambda: wykaz(c["firma_nip"], czekaj=True), daemon=True).start()




# ============================================================ obserwowane BIP

def dane_bip():
    return czytaj(F_BIP, {"zrodla": [], "widziane": {}, "propozycje": []})


def katalog_instytucji(log, woj, powiaty, typy):
    """Wspólny katalog stron instytucji (wszystkie konta): strony z danego powiatu i rodzaju AI wyszukuje w internecie
    raz na 120 dni, a każde kolejne konto dostaje je z katalogu – bez kosztów AI."""
    kat = WSP.czytaj("katalog_instytucji.json", {})
    granica = (dt.date.today() - dt.timedelta(days=120)).isoformat()
    np_ = lambda x: W.norm(re.sub(r"^powiat\s+", "", str(x or ""), flags=re.I))
    pw = [np_(p) for p in powiaty] or ["*"]
    wynik, brak_typy = [], []
    for t in typy:
        klucze = [f"{woj}|{p}|{t}" for p in pw]
        if all((kat.get(k) or {}).get("data", "") >= granica for k in klucze):
            for k in klucze:
                wynik += kat[k]["zrodla"]
        else:
            brak_typy.append(t)
    if brak_typy:
        c = cfg()
        wymagany_klucz(c)
        nowe = BIP.odkryj(c, woj, powiaty, brak_typy, log)
        with W.BLOKADA:
            kat = WSP.czytaj("katalog_instytucji.json", {})
            dzis = dt.date.today().isoformat()
            for t in brak_typy:
                for p in pw:
                    kat[f"{woj}|{p}|{t}"] = {"data": dzis, "zrodla": [x for x in nowe if x.get("typ") == t and (p == "*" or not x.get("powiat") or np_(x["powiat"]) == p)]}
            WSP.pisz("katalog_instytucji.json", kat)
        wynik += nowe
    else:
        log(f"Strony instytucji ({woj}): z katalogu programu – bez wyszukiwania w internecie.")
    return wynik










def powiaty_obszaru(c, log):
    """Województwa i powiaty obszaru wyszukiwania: {województwo: [powiaty] (puste = całe województwo)}."""
    ob = c.get("obszar") or {}
    tryb = ob.get("tryb", "promien")
    if tryb == "wojewodztwa":
        return {w: [] for w in ob.get("wojewodztwa") or [] if w in BIP.WOJEWODZTWA}
    if tryb != "promien":
        return {}
    miejsc = c.get("miejscowosci") or []
    if not miejsc:
        return {}
    probka = miejsc[:: max(1, len(miejsc) // 25)][:25]  # do 25 miejscowości rozłożonych w całym promieniu
    pam = czytaj(F_POWIATY_MIAST, {}) or {}
    wyn = {}
    for i, mj in enumerate(probka, 1):
        nazwa = mj[0] if isinstance(mj, (list, tuple)) else str(mj)
        k = f"?|{nazwa}"
        if k not in pam:
            try:
                time.sleep(1.1)
                x = next(iter(REG.szukaj_miejscowosci(nazwa) or []), {})
                pam[k] = [x.get("wojewodztwo", ""), re.sub(r"^powiat\s+", "", x.get("powiat", "") or "", flags=re.I)]
            except Exception:
                continue
        woj, pw = (pam.get(k) or ["", ""])[:2]
        if woj in BIP.WOJEWODZTWA and pw:
            wyn.setdefault(woj, set()).add(pw)
        if i % 5 == 0:
            log(f"Ustalam powiaty obszaru: {i}/{len(probka)}")
    pisz(F_POWIATY_MIAST, pam)
    return {w: sorted(p) for w, p in wyn.items()}
















# ============================================================ pracownicy i godziny

def dane_prac():
    """Wszyscy pracownicy wszystkich kont (do zapisu i zestawień budów). W widokach używaj dane_prac_konta()."""
    return czytaj(F_PRAC, {"pracownicy": [], "wpisy": []})


def wlasciciel_prac(p):
    return p.get("wlasciciel") or login_admina()  # pracownicy sprzed podziału na konta należą do administratora


def widoczny_prac(p):
    """Każde konto widzi tylko własnych pracowników; administrator może włączyć podgląd wszystkich kont."""
    if has_request_context() and wlasciciel() and session.get("prac_wszystkie") and konto_admina():
        return True
    return wlasciciel_prac(p) == konto_biezace()


def dane_prac_konta():
    d = dane_prac()
    prac = [p for p in d["pracownicy"] if widoczny_prac(p)]
    ids = {p["id"] for p in prac}
    return {"pracownicy": prac, "wpisy": [w for w in d["wpisy"] if w.get("pracownik") in ids]}


def moj_pracownik(d, pid_):
    """Pracownik z pełnych danych d, o ile należy do bieżącego konta (inaczej None)."""
    return next((x for x in d["pracownicy"] if x["id"] == pid_ and widoczny_prac(x)), None)




def _kwota(x):
    return MO.zaokr(float(x or 0))














def rozliczenie(od, do):
    d = dane_prac_konta()
    wpisy = sorted([w for w in d["wpisy"] if od <= w["data"] <= do], key=lambda w: (w["data"], w["imie"]))
    suma = {}
    for w in wpisy:
        s_ = suma.setdefault(w["pracownik"], {"imie": w["imie"], "godziny": 0.0, "kwota": 0.0, "dni": set()})
        s_["godziny"] += w["godziny"]
        s_["kwota"] += w["kwota"]
        s_["dni"].add(w["data"])
    lista = [{"pracownik": k, "imie": v["imie"], "godziny": round(v["godziny"], 2), "kwota": _kwota(v["kwota"]),
              "dni": len(v["dni"])} for k, v in suma.items()]
    lista.sort(key=lambda x: x["imie"])
    return wpisy, lista






# ============================================================ dokumenty wykonawcy i komplet oferty







# dokumenty składane z ofertą → po czym poznać, że są w komplecie (nazwa pliku albo tytuł dokumentu przygotowanego przez program)
WZORCE_KOMPLETU = [
    (r"formularz\w*\s+ofertow|\boferta\b(?!.*cen)", r"formularz|_formularze|oferta"),
    (r"formularz\w*\s+cenow|kosztorys|elementów scalonych|asortymentowo", r"kosztorys|formularz.?cenow|cenow|TES|elementow"),
    (r"art\.?\s*125|JEDZ|ESPD|oświadczeni\w*\s+o\s+niepodleganiu|oświadczeni\w*\s+wykonawcy", r"125|JEDZ|ESPD|oswiadcz|oświadcz|niepodleg"),
    (r"wadium", r"wadium|wadial|gwarancj\w*\s*(bankow|ubezpiecz)|przelew|potwierdzenie"),
    (r"przedmiotow\w+\s+środk|karty?\s+(katalog|techniczn)|certyfikat|deklaracj\w+\s+właściwości", r"kart|katalog|certyfikat|deklarac|DWU|DoP"),
]
WARUNKOWE_KOMPLETU = r"(?i)jeśli|jeżeli|o ile|ewentualnie|na wezwanie|tylko przy|wyłącznie przy|gdy dotyczy|dotyczy\)|nie z ofertą|po wyborze|przed zawarciem"


def braki_kompletu(wymagane, nazwy_plikow, tytuly=()):
    """Wymagane z ofertą dokumenty, których nie ma w komplecie. Pozycje warunkowe (pełnomocnictwo „jeśli”, „na wezwanie” itp.) i nierozpoznane
    rodzaje nie są brakami – zostają w spisie „do sprawdzenia”."""
    tekst = " | ".join(list(nazwy_plikow) + list(tytuly))
    braki = []
    for w in wymagane or []:
        w_ = str(w)
        if re.search(WARUNKOWE_KOMPLETU, w_):
            continue
        for rx_wym, rx_plik in WZORCE_KOMPLETU:
            if re.search(rx_wym, w_, re.I):
                if not re.search(rx_plik, tekst, re.I):
                    braki.append(re.split(r"\s+[–(-]\s*|\s*\(", w_)[0][:90])
                break
    return braki


@app.post("/api/projekty/<pid>/komplet")
@wymaga_logowania
def komplet(pid):
    """Tworzy folder „komplet_oferty” i archiwum ZIP: dokumenty oferty + sprawdzone dokumenty wykonawcy."""
    import zipfile as zf
    d = pdir(pid)
    m = meta(pid)
    wyk = pliki_wykonawcy(pid)
    niespr = [p["nazwa"] for p in wyk if not p["sprawdzony"]]
    if niespr and not request.json.get("mimo_to"):
        return jsonify({"blad": "Niesprawdzone dokumenty: " + ", ".join(niespr), "niesprawdzone": niespr}), 409
    kat = os.path.join(d, "komplet_oferty")
    shutil.rmtree(kat, ignore_errors=True)
    os.makedirs(os.path.join(kat, "2_Dokumenty_wykonawcy"))
    os.makedirs(os.path.join(kat, "1_Oferta"))
    dolaczone = []
    oferta_pl = [x for x in (m.get("pliki_oferty") or []) if x and not x.startswith("Analiza_")]
    if any(x.startswith("Kosztorys_dla_klienta_") for x in oferta_pl):  # do zamawiającego trafia wersja bez notatek roboczych
        oferta_pl = [x for x in oferta_pl if not x.startswith("Kosztorys_ofertowy_") and not x == m.get("kosztorys")]
    for n in oferta_pl:
        if os.path.isfile(os.path.join(d, n)):
            shutil.copy2(os.path.join(d, n), os.path.join(kat, "1_Oferta", n))
            dolaczone.append("1_Oferta/" + n)
    for p in wyk:
        shutil.copy2(os.path.join(d, "dokumenty_wykonawcy", p["nazwa"]), os.path.join(kat, "2_Dokumenty_wykonawcy", p["nazwa"]))
        dolaczone.append("2_Dokumenty_wykonawcy/" + p["nazwa"])
    if not dolaczone:
        return jsonify({"blad": "Brak dokumentów do spakowania – przygotuj ofertę i dodaj dokumenty wykonawcy."}), 400
    wymagane = czytaj(os.path.join(d, "oferta_dane.json"), {}).get("zalaczniki_do_oferty", [])
    spis = ["SPIS DOKUMENTÓW OFERTY", f"Projekt: {m.get('nazwa')}", f"Utworzono: {dt.datetime.now():%d.%m.%Y %H:%M}", ""]
    spis += [f"{i}. {x}" for i, x in enumerate(dolaczone, 1)]
    if wymagane:
        spis += ["", "Wymagane przez zamawiającego (sprawdź, czy wszystko jest):"] + [f"- {x}" for x in wymagane]
    with open(os.path.join(kat, "0_Spis_dokumentow.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(spis))
    nazwa_zip = f"Komplet_oferty_{MO.bezpieczna_nazwa(m.get('nazwa', 'oferta'))[:60]}.zip"
    for n in os.listdir(d):
        if n.startswith("Komplet_oferty_") and n.endswith(".zip"):
            os.remove(os.path.join(d, n))
    with zf.ZipFile(os.path.join(d, nazwa_zip), "w", zf.ZIP_DEFLATED) as z:
        for r, _, pliki in os.walk(kat):
            for n in pliki:
                z.write(os.path.join(r, n), os.path.relpath(os.path.join(r, n), kat))
    tytuly = [str(t) for t in ((m.get("zalaczniki_dostawcy") or {}).get("dokumenty") or [])]
    braki = braki_kompletu(wymagane, [os.path.basename(x) for x in dolaczone], tytuly)  # nazwy plików, nie folderów („1_Oferta”)
    uwagi = []
    if not m.get("oferta_przygotowana") and not jest_dostawca(m) and not any(re.search(r"(?i)formularz", os.path.basename(x)) for x in dolaczone) \
            and not any(re.search(r"(?i)formularz\w*\s+ofertow", b) for b in braki):
        uwagi.append("Brak formularza ofertowego – kliknij „Przygotuj ofertę na podstawie kosztorysu” albo dodaj formularz do dokumentów wykonawcy.")
    wad_ = str((m.get("oferta") or {}).get("wadium") or "").lower().strip()
    if re.search(r"nie\s+(jest\s+)?wymag|brak\s+wymog|nie\s+żąda|nie\s+dotyczy|^\s*(brak|nie|-|–|0|0[,.]00(\s*zł)?)\s*\.?\s*$", wad_):  # wadium niewymagane, a w komplecie dokument wadialny
        zb = [os.path.basename(x) for x in dolaczone if re.search(r"(?i)wadi", os.path.basename(x))]
        if zb:
            uwagi.append(f"Zamawiający nie wymaga wadium, a w komplecie jest: {', '.join(zb)} – sprawdź, czy ten dokument jest potrzebny.")
    m["komplet"] = {"zip": nazwa_zip, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "plikow": len(dolaczone), "braki": braki, "uwagi": uwagi}
    zapisz_meta(pid, m)
    return jsonify({"url": f"/pobierz/{pid}/{nazwa_zip}", "plikow": len(dolaczone), "niesprawdzone": niespr, "braki": braki, "uwagi": uwagi})


# ============================================================ realizacja budów

def nazwa_projektu(pid):
    try:
        return meta(pid).get("nazwa", "") if pid else ""
    except Exception:
        return ""


def projekt_dostepny(pid):
    """Metadane projektu, gdy istnieje i zalogowane konto ma do niego dostęp; inaczej None (bez ujawniania, czy projekt istnieje)."""
    if not pid or not re.fullmatch(r"[0-9a-f]{12}", str(pid)):
        return None
    m = czytaj(os.path.join(PROJ, str(pid), "projekt.json"), None)
    return m if m and ma_dostep(m) else None


@app.post("/api/projekty/<pid>/umowa")
@wymaga_logowania
def umowa_generuj(pid):
    d = pdir(pid)
    m = meta(pid)
    dane_of = czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane_of:
        return jsonify({"blad": "Najpierw przygotuj ofertę i kosztorys (krok 2) – umowa powstaje na ich podstawie."}), 400
    pola = {k: v for k, v in (request.json or {}).items() if k in UM.domyslne(dane_of, m, cfg())}
    try:
        pola["netto"] = float(str(pola.get("netto", dane_of["netto"])).replace(" ", "").replace(",", "."))
        v_ = str(pola.get("vat") if pola.get("vat") not in (None, "") else ("" if dane_of.get("vat_nieustalony") else dane_of.get("vat", ""))).replace(",", ".").replace("%", "")
        if not v_.strip():
            return jsonify({"blad": "Wybierz stawkę VAT – ustal ją z zamawiającym lub z warunków przetargu."}), 400
        pola["vat"] = float(v_) / (100 if float(v_) > 1 else 1)
        for k in ("termin_platnosci", "zaliczka", "gwarancja", "kara_zwloka", "kara_wady", "kara_odstapienie", "kara_limit"):
            if k in pola and str(pola[k]).strip() != "":
                pola[k] = float(str(pola[k]).replace(",", "."))
    except ValueError:
        return jsonify({"blad": "Sprawdź pola liczbowe (kwota, VAT, terminy, kary)."}), 400
    if pola["netto"] <= 0:
        return jsonify({"blad": "Wynagrodzenie netto musi być większe od zera."}), 400
    for k in ("start", "koniec", "data"):
        if pola.get(k):
            try:
                dt.date.fromisoformat(pola[k])
            except ValueError:
                return jsonify({"blad": "Nieprawidłowa data."}), 400
    if pola.get("start") and pola.get("koniec") and pola["koniec"] < pola["start"]:
        return jsonify({"blad": "Termin zakończenia jest wcześniejszy niż rozpoczęcie."}), 400
    if pola.get("zam_typ") != "konsument" and NIP.poprawny(pola.get("zam_id")):
        dz = wykaz(pola["zam_id"], czekaj=True)
        if dz and dz.get("nazwa"):
            pola["zam_nazwa"], pola["zam_id"] = dz["nazwa"], dz["nip"]
            pola["zam_adres"] = dz.get("adres") or pola.get("zam_adres", "")
    zal = ["Kosztorys ofertowy", "Oferta Wykonawcy"]
    r = realizacja_dane(pid)
    if r.get("hrf"):
        zal.append("Harmonogram rzeczowo-finansowy")
    nazwa = f"Umowa_o_roboty_budowlane_{MO.bezpieczna_nazwa(m.get('nazwa', 'projekt'))[:50]}.docx"
    kwoty = UM.generuj(os.path.join(d, nazwa), pola, dane_of, cfg(), zal)
    if pola.get("zam_nazwa") and pola.get("zam_typ") != "konsument":  # zapamiętaj klienta w bazie
        try:
            zapisz_klienta({"nazwa": pola["zam_nazwa"], "adres": pola.get("zam_adres", ""), "reprezentant": pola.get("zam_reprezentant", ""),
                            **({"nip": pola["zam_id"]} if NIP.poprawny(pola.get("zam_id")) else {})}, session.get("login", ""))
        except Exception:
            pass
    m = meta(pid)
    m["umowa"] = {"plik": nazwa, "pola": pola, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), **kwoty,
                  "pola_reczne_netto": abs(pola["netto"] - float(dane_of.get("netto", 0))) > 0.005}
    zapisz_meta(pid, m)
    return jsonify({"url": f"/pobierz/{pid}/{nazwa}", **kwoty})


@app.post("/api/projekty/<pid>/status")
@wymaga_logowania
def projekt_status(pid):
    st = request.json.get("status")
    if st not in ("oferta", "realizacja", "zakonczony"):
        return jsonify({"blad": "Nieznany status"}), 400
    m = meta(pid)
    m["status_projektu"] = st
    if st == "realizacja":
        try:
            plik_bledow(pid, m)  # umowa zawarta mimo błędów w dokumentacji – od razu wykaz błędów do wykorzystania we wnioskach
        except Exception:
            pass
    zapisz_meta(pid, m)
    if st == "realizacja":
        r = realizacja_dane(pid)
        um = (m.get("umowa") or {}).get("pola")
        o = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {})
        if m.get("strona") == "zamawiajacy":
            # zamawiający: wartość umowy = cena oferty wybranego wykonawcy (z kreatora – „Po wyborze oferty”), a nie kosztorys inwestorski
            if not r.get("wartosc_szacunkowa") and _netto_zam(m):
                r["wartosc_szacunkowa"] = _netto_zam(m)  # z szacowania wartości (zamawiający publiczny) – nie z kosztorysu AI
            um_ = (m.get("kreator") or {}).get("umowa") or {}
            for k_, kk in (("wykonawca_nazwa", "wykonawca_nazwa"), ("wykonawca_nip", "wykonawca_nip"), ("wykonawca_adres", "wykonawca_adres"), ("umowa_nr", "umowa_nr"),
                           ("data_umowy", "data_umowy"), ("termin_zakonczenia", "termin")):
                if um_.get(kk) and not r.get(k_) and (k_ != "data_umowy" or PZ_._d(um_[kk])):  # błędna data umowy – nie przenosimy
                    r[k_] = str(um_[kk])[:200]
            if um_.get("cena_netto") and not r.get("wartosc_netto"):
                r["wartosc_netto"] = _f_liczba(um_["cena_netto"])
                if um_.get("vat") not in (None, ""):
                    v_ = _f_liczba(um_["vat"])
                    r["vat"] = v_ / 100 if v_ > 1 else v_  # „23” z kreatora = 0,23 (inaczej brutto liczone ×24)
            if not r.get("adres"):
                r["adres"] = ((m.get("kreator") or {}).get("potrzeba") or {}).get("miejsce") or ""
            zapisz_realizacje(pid, r)
            return jsonify({"ok": True})
        if um and not r.get("umowa_nr"):
            r.update(umowa_nr=um.get("numer", ""), data_umowy=um.get("data", ""), wartosc_netto=MO.zaokr(um.get("netto") or 0),
                     vat=um.get("vat") or ("" if o.get("vat_nieustalony") else o.get("vat")) or "", termin_zakonczenia=um.get("koniec", ""), kierownik=um.get("kierownik", ""),
                     adres=um.get("obiekt", ""))
            zapisz_realizacje(pid, r)
        if not r.get("wartosc_netto"):
            r.update(wartosc_netto=o.get("netto", 0), vat="" if o.get("vat_nieustalony") else (o.get("vat") or ""))
            zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


REALIZACJA_DOMYSLNE = {"umowa_nr": "", "data_umowy": "", "wartosc_netto": 0, "vat": "", "hrf": None, "koszty": [], "faktury": [],
                       "zdjecia": [], "dziennik": [], "usterki": []}




def zapisz_realizacje(pid, r):
    pisz(os.path.join(pdir(pid), "realizacja.json"), r)


def dzialy_kosztorysu(pid):
    """Działy kosztorysu do harmonogramu rzeczowo-finansowego i protokołów odbioru – w wersji dla zamawiającego (koszty spoza przedmiaru
    rozłożone na pozycje przedmiaru), bo harmonogram i protokoły trafiają do zamawiającego."""
    o = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {})
    if o.get("dzialy"):
        try:
            o = MO.dla_zamawiajacego(o)[0]
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            pass
    return [{"nazwa": dz.get("nazwa", ""), "wartosc": dz.get("suma", 0)} for dz in o.get("dzialy", [])]


def przelicz_hrf(hrf):
    dz = hrf["dzialy"]
    for e in hrf["etapy"]:
        e["wartosc"] = MO.zaokr(sum(dz[i]["wartosc"] * float(e["udzialy"][i] if i < len(e["udzialy"]) else 0) / 100
                                    for i in range(len(dz))))
    E = hrf["etapy"]
    pelne = E and dz and all(abs(sum(float(e["udzialy"][i] if i < len(e["udzialy"]) else 0) for e in E) - 100) < 0.01 for i in range(len(dz)))
    if pelne:  # wszystkie działy rozłożone w 100% – groszowa reszta z zaokrągleń w ostatnim etapie (suma etapów = wartość umowy)
        k = max(i for i, e in enumerate(E) if e["wartosc"] or i == 0)
        if E[k].get("status") != "odebrany" or len(E) == 1:
            E[k]["wartosc"] = MO.zaokr(E[k]["wartosc"] + sum(x["wartosc"] for x in dz) - sum(e["wartosc"] for e in E))
    return hrf


def robocizna_projektu(pid, nazwa):
    """Godziny pracy na budowie – tylko pracowników właściciela projektu (wpisy innych firm nie wchodzą do rozliczenia)."""
    try:
        wl = (meta(pid).get("wlasciciel") or login_admina()).lower()
    except Exception:
        wl = login_admina().lower()
    d = dane_prac()
    swoi = {p["id"] for p in d["pracownicy"] if wlasciciel_prac(p).lower() == wl}
    wpisy = [w for w in d["wpisy"] if w.get("pracownik") in swoi
             and (w.get("projekt_id") == pid or (not w.get("projekt_id") and nazwa and w.get("projekt") == nazwa))]
    return wpisy


def prognoza_wyniku(s_):
    """H3-02: wynik prognozowany z postępu prac (metoda kosztu do zakończenia przy stałej wydajności kosztowej):
    prognozowany koszt całkowity = koszty dotąd ÷ postęp, wynik = wartość umowy − prognozowany koszt całkowity.
    Postęp rzeczowy = odebrane etapy ÷ wartość umowy; gdy brak odbiorów – postęp finansowy = zafakturowano netto ÷ wartość umowy.
    Bez postępu (albo bez kosztów, umowy) – brak kwoty: dotąd „umowa − koszty dotąd” pokazywało na starcie budowy całą wartość umowy jako zysk."""
    W, K = s_.get("wartosc_umowy_netto") or 0, s_.get("koszty_razem") or 0
    for zrodlo, kw in (("rzeczowy (odebrane etapy harmonogramu)", s_.get("odebrano_netto") or 0), ("finansowy (zafakturowano netto)", s_.get("zafakturowano_netto") or 0)):
        if W > 0 and kw > 0:
            post = min(1.0, kw / W)
            if K <= 0:
                break
            koszt_calk = MO.zaokr(K / post)
            return {"wynik_prognoza": MO.zaokr(W - koszt_calk), "prognoza_koszt_calkowity": koszt_calk, "prognoza_postep_proc": round(post * 100, 1),
                    "prognoza_metoda": f"Postęp {zrodlo}: {round(post * 100, 1):g}%. Prognozowany koszt całkowity = koszty dotąd ÷ postęp "
                                       f"({MO.zl(K)} ÷ {round(post * 100, 1):g}% = {MO.zl(koszt_calk)}); wynik = wartość umowy − prognozowany koszt całkowity."}
    powod = ("brak wartości umowy" if W <= 0 else "brak kosztów zapisanych na budowie" if K <= 0 else
             "postęp prac nieznany (brak odebranych etapów i faktur)")
    return {"wynik_prognoza": None, "prognoza_koszt_calkowity": None, "prognoza_postep_proc": None,
            "prognoza_metoda": f"Brak danych do prognozy – {powod}. Prognoza liczy się z postępu prac: koszty dotąd ÷ postęp (odbiory etapów albo faktury)."}


def podsumowanie_realizacji(pid):
    m = meta(pid)
    r = realizacja_dane(pid)
    dzis = dt.date.today().isoformat()
    fakt = r.get("faktury", [])
    koszty = r.get("koszty", [])
    rob = robocizna_projektu(pid, m.get("nazwa"))
    hrf = r.get("hrf") or {"etapy": []}
    s_ = {
        "wartosc_umowy_netto": MO.zaokr(r.get("wartosc_netto") or 0),
        "odebrano_netto": MO.zaokr(sum(e.get("wartosc", 0) for e in hrf["etapy"] if e.get("status") == "odebrany")),
        "zafakturowano_netto": MO.zaokr(sum(f["netto"] for f in fakt)),
        "zafakturowano_brutto": MO.zaokr(sum(f["brutto"] for f in fakt)),
        "zaplacono_brutto": MO.zaokr(sum(f["brutto"] for f in fakt if f.get("zaplacona"))),
        "naleznosci_brutto": MO.zaokr(sum(f["brutto"] for f in fakt if not f.get("zaplacona"))),
        "przeterminowane_brutto": MO.zaokr(sum(f["brutto"] for f in fakt if not f.get("zaplacona") and f.get("termin", "9") < dzis)),
        "koszty_netto": MO.zaokr(sum(k["netto"] for k in koszty)),
        "koszty_niezaplacone": MO.zaokr(sum(k["netto"] for k in koszty if not k.get("zaplacona"))),
        "robocizna": MO.zaokr(sum(w["kwota"] for w in rob)),
        "robocizna_godziny": round(sum(w["godziny"] for w in rob), 2),
    }
    s_["koszty_razem"] = MO.zaokr(s_["koszty_netto"] + s_["robocizna"])
    s_["wynik_biezacy"] = MO.zaokr(s_["zafakturowano_netto"] - s_["koszty_razem"])
    s_.update(prognoza_wyniku(s_))
    kat = {}
    for k in koszty:
        kat[k.get("kategoria", "inne")] = MO.zaokr(kat.get(k.get("kategoria", "inne"), 0) + k["netto"])
    s_["koszty_kategorie"] = kat
    return s_




# ---------- realizacja umów dostawcy / usługodawcy (po wygraniu przetargu)



def _wykonawca_dane():
    c = cfg()
    adr = c.get("firma_adres", "")
    m_ = re.search(r"\d{2}-\d{3}\s+([^,]+)", adr)
    return {"nazwa": c.get("firma_nazwa", ""), "adres": adr, "nip": c.get("firma_nip", ""), "miejscowosc": m_.group(1).strip() if m_ else ""}












# ---------- zamawiający: sprawdzenie złożonych ofert, ocena i ranking



def _bloki_z(katalog, limit=25):
    bloki = []
    for dp, _, fs in os.walk(katalog):
        for f in sorted(fs)[:limit]:
            try:
                b, _, _ = MO.przygotuj_blok(os.path.join(dp, f))
                bloki += b
            except Exception:
                continue
    return bloki


# ============================================================ BENEFICJENT DOTACJI – ZASADA KONKURENCYJNOŚCI




@app.get("/api/zapytania")
@wymaga_logowania
def zapytania_lista():
    """Zapytania ofertowe beneficjenta (zasada konkurencyjności); ?dotacja=<id> – tylko z danego projektu dotacji."""
    dot = request.args.get("dotacja")
    wyn, login, rola = [], session.get("login"), rola_sesji()
    for pid, m in projekty_ro():  # tylko do odczytu – bez kopiowania
        if m and m.get("typ") == "zapytanie" and ma_dostep(m, login, rola, lista=True) and not m.get("archiwum"):
            Z = m.get("zapytanie") or {}
            if dot and Z.get("dotacja_id") != dot:
                continue
            st = _zapytanie_stan(pid, m)
            wyn.append({"id": pid, "nazwa": m.get("nazwa"), "utworzono": m.get("utworzono"), "wartosc": (Z.get("dane") or {}).get("wartosc_netto"),
                        "tryb": st["wymagania"]["tryb"], "gotowe": sum(1 for x in st["lista"] if x["ok"]), "razem": len(st["lista"]),
                        "dotacja": st["dotacja"].get("nazwa", ""), "wybrany": (st["ocena"] or {}).get("najkorzystniejsza")})
    return jsonify(sorted(wyn, key=lambda x: x.get("utworzono") or "", reverse=True))






































def _przedmiot_oceny(m):
    rz = (PRW.ustawienia(m)["przedmiot"] if m.get("strona") == "prawnik" else m.get("rodzaj_zamowienia")) or ""
    return rz if rz in ("roboty", "uslugi", "dostawy") else "roboty"


def praca_rynkowosc(log, pid, ids=None, wszystkie=False):
    """Rynkowość ceny: art. 224 (bez AI) + pozycje oferty (80% wartości albo wszystkie) a ceny rynkowe z internetu
    + roboty: inżynieria cenowa, usługi: koszty pracy. Model do dokumentów (jakość przed kosztem)."""
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    O = ocena_dane(m)
    rz = _przedmiot_oceny(m)
    swz = O.get("swz") or {}
    oceniane = [o for o in O["oferty"] if (o.get("wynik") or {}).get("cena_brutto")]
    if not oceniane:
        raise ValueError("Najpierw zbadaj oferty (krok 4) – potrzebna jest cena każdej oferty.")
    ceny_nieodrz = OO.ceny_do_sredniej_224(O["oferty"], swz.get("prywatny"))  # ta sama reguła co ranking (art. 224 ust. 2 pkt 1: bez odrzuconych z art. 226 ust. 1 pkt 1, 5a, 10)
    if not swz.get("wartosc_zam_brutto"):
        log("UWAGA – brak wartości zamówienia z VAT: próg z art. 224 ust. 2 liczony tylko od średniej cen ofert. Wpisz wartość, aby porównanie było pełne.")
    c2 = dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5")
    wyniki = {}
    for i, o in enumerate([o for o in oceniane if not ids or o["id"] in ids], 1):
        log(f"Oferta {i}: {o['nazwa']} – odczyt pozycji formularza cenowego…")
        ob = _bloki_z(os.path.join(pdir(pid), "oferty", o["id"]))
        pozycje, zatr = [], {}
        if ob:
            try:
                r = ai_dane(c2, RY.SYSTEM_POZYCJE, MO.oznacz_dokumenty(ob, MO.ustawienie_cache(c)) + [{"type": "text", "text": RY.polecenie_pozycji(rz)}],
                            16000, log, lambda t: MO.wyciagnij_json(t) or {})
                pozycje = [p for p in r.get("pozycje") or [] if isinstance(p, dict)]
                zatr = r.get("zatrudnienie") or {}
            except ValueError as e:
                log(f"   Pozycji nie odczytano: {e}")
        wybrane, proc = (pozycje, 100.0) if wszystkie else RY.pareto(pozycje)
        rynek = []
        for k in range(0, len(wybrane), 12):
            paczka = wybrane[k:k + 12]
            log(f"   Ceny rynkowe: pozycje {k + 1}–{k + len(paczka)} z {len(wybrane)} ({'wszystkie' if wszystkie else f'{proc}% wartości oferty'})…")
            try:
                txt, _ = CR.claude_z_wyszukiwaniem(c2, RY.SYSTEM_RYNEK, RY.polecenie_rynku(rz, paczka, c.get("region", "")), max_wyszukan=10, max_tokens=6000, log=log)
                rynek += (MO.wyciagnij_json(txt) or {}).get("pozycje") or []
            except Exception as e:
                log(f"   Wyszukiwanie cen nie powiodło się: {e}")
        wyniki[o["id"]] = RY.ocena_oferty((o.get("wynik") or {}).get("cena_brutto"), swz.get("wartosc_zam_brutto"), ceny_nieodrz, pozycje, rynek, zatr, rz,
                                          proc if not wszystkie else 100.0)
        wyniki[o["id"]]["pozycji_oferty"] = len(pozycje)
        wyniki[o["id"]]["sprawdzono_pozycji"] = len(wybrane)
        log(f"   Wynik: {wyniki[o['id']]['klasyfikacja']}" + (f" ({wyniki[o['id']]['podstawa']})" if wyniki[o["id"]]["podstawa"] else ""))
    with BLOKADA:
        m = meta(pid)
        O = ocena_dane(m)
        for o in O["oferty"]:
            if o["id"] in wyniki:
                o["rynkowosc"] = wyniki[o["id"]]
        m["ocena"] = O
        zapisz_meta(pid, m)
    return {"oferty": len(wyniki)}




def _ustalenia_z_ofert(O):
    """Ustalenia z badania ofert i rynkowości → uwagi w formacie sprawdzenia (do opinii i odwołania)."""
    uw = []
    for o in O["oferty"]:
        w, r = o.get("wynik") or {}, o.get("rynkowosc") or {}
        for k, waga in (("niezgodnosci", "krytyczna"), ("braki", "istotna"), ("bledy_rachunkowe", "istotna"), ("do_wyjasnienia", "drobna")):
            for x in w.get(k) or []:
                if isinstance(x, dict):
                    uw.append({"waga": waga, "kategoria": k, "dokument": f"oferta: {o['nazwa']} – {x.get('dokument', '')}", "miejsce": x.get("miejsce", ""),
                               "opis": x.get("opis", ""), "podstawa": {"niezgodnosci": "art. 226 ust. 1 pkt 5 Pzp", "braki": "art. 128 Pzp",
                                                                        "bledy_rachunkowe": "art. 223 ust. 2 Pzp", "do_wyjasnienia": "art. 223 ust. 1 Pzp"}[k],
                               "propozycja": x.get("poprawka", "")})
        if w.get("podstawa_odrzucenia"):
            uw.append({"waga": "krytyczna", "kategoria": "odrzucenie", "dokument": f"oferta: {o['nazwa']}", "opis": w["podstawa_odrzucenia"], "podstawa": "art. 226 Pzp"})
        if r.get("klasyfikacja") and r["klasyfikacja"] != "rynkowa":
            uw.append({"waga": "krytyczna" if "rażąco" in r["klasyfikacja"] else "istotna", "kategoria": "cena", "dokument": f"oferta: {o['nazwa']}",
                       "opis": f"Cena: {r['klasyfikacja']}. {r.get('art224', {}).get('opis', '')} {r.get('inzynieria_cenowa', '')} "
                               f"{(r.get('koszty_pracy') or {}).get('opis', '')}".strip(), "podstawa": r.get("podstawa") or "art. 224 Pzp"})
    return uw








def _tekst_odwolania(baza, plik):
    p = os.path.normpath(os.path.join(baza, plik))
    if not p.startswith(os.path.normpath(baza) + os.sep) or not os.path.isfile(p):  # z separatorem – nie katalog o podobnej nazwie obok
        return jsonify({"blad": "Nie znaleziono pliku."}), 404
    katalog = os.path.dirname(os.path.relpath(p, baza)) or "."
    tx = OD.teksty(baza, (katalog,))
    rel = os.path.relpath(p, baza).replace(os.sep, "/")
    d = tx.get(rel) or tx.get("./" + rel) or next((v for k, v in tx.items() if k.endswith(os.path.basename(p))), None) or {"tekst": "", "strony": [0]}
    return jsonify({"tekst": d["tekst"][:400000], "strony": d.get("strony") or [0], "nazwa": os.path.basename(p)})


@app.get("/api/projekty/<pid>/tekst-dokumentu")
@wymaga_logowania
def projekt_tekst_dokumentu(pid):
    """Pełny tekst dokumentu do podglądu odwołania (§, punkt, pozycja) – z zaznaczonym fragmentem."""
    meta(pid)
    return _tekst_odwolania(pdir(pid), request.args.get("plik", ""))




# ============================================================ OGŁOSZENIE O WYKONANIU UMOWY (art. 448 Pzp) – zamawiający






















# ---------- budowa domu (inwestor indywidualny): wykonawcy, formalności, transze kredytu

FORMALNOSCI_DOM = [
    "Mapa do celów projektowych i warunki zabudowy / wypis z MPZP", "Pozwolenie na budowę albo zgłoszenie budowy",
    "Dziennik budowy (e-Dziennik) i kierownik budowy", "Zawiadomienie nadzoru budowlanego o rozpoczęciu robót",
    "Wytyczenie budynku przez geodetę", "Warunki i umowy przyłączy (prąd, woda, kanalizacja, gaz)",
    "Ubezpieczenie budowy", "Odbiory kominiarskie (przewody kominowe i wentylacyjne)", "Pomiary instalacji elektrycznej",
    "Inwentaryzacja powykonawcza (geodeta)", "Świadectwo charakterystyki energetycznej",
    "Zawiadomienie o zakończeniu budowy / pozwolenie na użytkowanie", "Zgłoszenie nieruchomości do podatku od nieruchomości"]


def dane_domu(r):
    r.setdefault("wykonawcy", [])
    r.setdefault("transze", [])
    if not r.get("formalnosci"):
        r["formalnosci"] = [{"id": f"f{i}", "nazwa": n, "status": "do zrobienia", "data": "", "uwagi": ""} for i, n in enumerate(FORMALNOSCI_DOM, 1)]
    return r


@app.post("/api/projekty/<pid>/wykonawcy")
@wymaga_logowania
def dom_wykonawcy(pid):
    j = request.json or {}
    with BLOKADA:
        r = dane_domu(realizacja_dane(pid))
        if j.get("usun"):
            r["wykonawcy"] = [x for x in r["wykonawcy"] if x["id"] != j.get("id")]
        else:
            if not str(j.get("nazwa", "")).strip():
                return jsonify({"blad": "Wpisz nazwę wykonawcy / ekipy."}), 400
            x = next((y for y in r["wykonawcy"] if y["id"] == j.get("id")), None)
            if not x:
                x = {"id": uuid.uuid4().hex[:10]}
                r["wykonawcy"].append(x)
            for k in ("nazwa", "zakres", "telefon", "email", "nip", "adres", "uwagi"):
                if k in j:
                    x[k] = str(j[k] or "")[:300]
            try:
                x["kwota"] = MO.zaokr(float(str(j.get("kwota") or 0).replace(" ", "").replace(",", ".")))
            except ValueError:
                return jsonify({"blad": "Nieprawidłowa kwota umowy."}), 400
        zapisz_realizacje(pid, r)
    return jsonify(r["wykonawcy"])


@app.post("/api/projekty/<pid>/formalnosci")
@wymaga_logowania
def dom_formalnosci(pid):
    j = request.json or {}
    with BLOKADA:
        r = dane_domu(realizacja_dane(pid))
        if j.get("nowa"):
            r["formalnosci"].append({"id": uuid.uuid4().hex[:8], "nazwa": str(j["nowa"])[:200], "status": "do zrobienia", "data": "", "uwagi": ""})
        for x in r["formalnosci"]:
            if x["id"] == j.get("id"):
                if j.get("usun"):
                    r["formalnosci"].remove(x)
                    break
                if j.get("status") in ("do zrobienia", "w toku", "zrobione", "nie dotyczy"):
                    x["status"] = j["status"]
                for k in ("data", "uwagi"):
                    if k in j:
                        x[k] = str(j[k] or "")[:300]
        zapisz_realizacje(pid, r)
    return jsonify(r["formalnosci"])


@app.post("/api/projekty/<pid>/transze")
@wymaga_logowania
def dom_transze(pid):
    j = request.json or {}
    with BLOKADA:
        r = dane_domu(realizacja_dane(pid))
        if j.get("usun"):
            r["transze"] = [x for x in r["transze"] if x["id"] != j.get("id")]
        else:
            x = next((y for y in r["transze"] if y["id"] == j.get("id")), None)
            if not x:
                x = {"id": uuid.uuid4().hex[:8], "status": "planowana"}
                r["transze"].append(x)
            try:
                if "kwota" in j:
                    x["kwota"] = MO.zaokr(float(str(j["kwota"] or 0).replace(" ", "").replace(",", ".")))
            except ValueError:
                return jsonify({"blad": "Nieprawidłowa kwota transzy."}), 400
            for k in ("warunek", "data", "data_wyplaty", "uwagi"):
                if k in j:
                    x[k] = str(j[k] or "")[:200]
            if j.get("status") in ("planowana", "wniosek złożony", "wypłacona"):
                x["status"] = j["status"]
        zapisz_realizacje(pid, r)
    return jsonify(r["transze"])


# ---------- wnioski o zmianę umowy (prace dodatkowe, różnice w dokumentacji, przeszkody) i aneksy

def dane_umowy_projektu(pid, m):
    r = realizacja_dane(pid)
    up = (m.get("umowa") or {}).get("pola") or {}
    vat = r.get("vat") if r.get("vat") not in (None, "") else (m.get("oferta") or {}).get("vat")
    return {"nr": r.get("umowa_nr") or up.get("numer", ""), "data": r.get("data_umowy") or up.get("data", ""),
            "termin": r.get("termin_zakonczenia") or up.get("koniec", ""), "adres": r.get("adres") or up.get("obiekt", ""),
            "wartosc": float(r.get("wartosc_netto") or (m.get("oferta") or {}).get("netto") or 0),
            "vat": float(vat) if vat not in (None, "") else None}



# ───────────────────────── rozbieżności przedmiaru i decyzje wykonawcy ─────────────────────────

UWAGA_POZA_CENA = "Poza ceną oferty (decyzja wykonawcy):"
UWAGA_WARIANTY = "Rozbieżności wariantowe:"
UWAGA_WSTEPNY = "Wstępny kosztorys"
UWAGA_DOKUMENTACJA = "Niespójności dokumentacji:"
UWAGA_BEZ_WYCENY = "Pozycje bez wyceny (0 zł):"


def zastosuj_decyzje_rozbieznosci(m, dane, korekta=None):
    """Pozycje spoza przedmiaru z decyzją „na etap umowy” albo „nie dotyczy” nie wchodzą do ceny – także po ponownej wycenie.
    Dopisuje do uwag, co zostało poza ceną."""
    zm = False
    for rid, z in (m.get("rozbieznosci") or {}).items():
        if (z or {}).get("decyzja") in ROZB.POZA_CENA:
            try:
                zm = ROZB.ustaw(dane, rid, z["decyzja"])[1] or zm
            except ValueError:
                pass
    zam_roboty = m.get("typ") in INWESTORSKIE and m.get("rodzaj_zamowienia") not in ("uslugi", "dostawy")
    wykonawca_roboty = (m.get("typ") not in INWESTORSKIE + ("dom",) and not jest_dostawca(m)) or zam_roboty
    if wykonawca_roboty:  # warianty rozstrzyga wykonawca robót albo zamawiający (do wartości i do poprawienia dokumentów); formularz cenowy – tylko opis
        f_ = float((korekta or {}).get("wspolczynnik") or 0) or 1 + float((korekta or {}).get("procent") or 0) / 100
        zm = ROZB.normalizuj_warianty(dane, m.get("warianty"), wspolczynnik=f_) or zm
    if zm:
        for k in ("netto", "vat_kwota", "brutto"):
            dane.pop(k, None)
        dane = MO.przelicz(dane)
    dane["do_weryfikacji"] = [x for x in dane.get("do_weryfikacji") or [] if not str(x).startswith((UWAGA_POZA_CENA, UWAGA_WARIANTY, UWAGA_DOKUMENTACJA, UWAGA_BEZ_WYCENY))]
    war = ROZB.lista_wariantow(dane) if wykonawca_roboty else []
    if zam_roboty:
        poza = ROZB.lista(dane, m.get("rozbieznosci"))
        if war or poza:
            dane["do_weryfikacji"].append(
                f"{UWAGA_DOKUMENTACJA} " + "; ".join(x for x in (
                    f"{len(poza)} robót wymaganych dokumentacją nie ma w przedmiarze ({MO.zl(sum(x['wartosc'] for x in poza))} netto, ujęte w wartości)" if poza else "",
                    f"w {len(war)} poz. dokumenty podają różne rozwiązania (do wartości przyjęto wariant z dokumentu nadrzędnego, a gdy go brak – droższy)" if war else "") if x)
                + ". Popraw przedmiar i ujednolić dokumenty przed ogłoszeniem – inaczej wykonawcy złożą nieporównywalne oferty albo zgłoszą roboty dodatkowe.")
    elif war:
        bez = [w for w in war if not w["decyzja"]]
        dane["do_weryfikacji"].append(f"{UWAGA_WARIANTY} dokumenty podają różne rozwiązania w {len(war)} poz. przedmiaru ("
                                      + "; ".join(f"poz. {w['lp']}: w cenie {w[w['wybrany']]['opis'][:50]}" for w in war[:6]) + ("…" if len(war) > 6 else "")
                                      + f"). Bez decyzji wykonawcy: {len(bez)}. Wybierz wariant i zapytaj zamawiającego w tabeli rozbieżności.")
    bw = ROZB.bez_wyceny(dane) if wykonawca_roboty and not zam_roboty else []
    do_ust, nd_ = [p for p, nd in bw if not nd], [p for p, nd in bw if nd]
    if do_ust:  # robota wymagana / niejasna, a w cenie 0 zł – przy ryczałcie nie będzie za nią zapłaty
        dane["do_weryfikacji"].insert(0, f"{UWAGA_BEZ_WYCENY} {len(do_ust)} poz. wymaganych albo niejasnych NIE MA w cenie oferty – "
                                      + "; ".join(f"{str(p.get('opis', ''))[:70]} ({str(p.get('uwagi', ''))[:60]})" for p in do_ust[:6])
                                      + ("…" if len(do_ust) > 6 else "") + ". Wpisz ilość i cenę w kosztorysie albo zadaj pytanie zamawiającemu"
                                      + (" – przy wynagrodzeniu ryczałtowym robota bez ceny obciąża wykonawcę." if ROZB.rodzaj_wynagrodzenia(dane) == "ryczalt" else ".")
                                      + (f" Nie dotyczy (0 zł, bez wpływu na cenę): {len(nd_)} poz." if nd_ else ""))
    um = ROZB.kandydaci(dane)
    if um:
        s = sum(MO.zaokr(float(p.get("ilosc") or 0) * MO.zaokr(float(p.get("cena") or 0))) for p in um)
        dane["do_weryfikacji"].append(f"{UWAGA_POZA_CENA} {len(um)} poz. spoza przedmiaru na {MO.zl(s)} netto zostawiono na etap umowy – "
                                      + "; ".join(str(p.get("opis", ""))[:70] for p in um[:6]) + ("…" if len(um) > 6 else "") + ".")
    return dane


def rodzaj_postepowania_projektu(pid, m=None):
    """unijne / krajowe / poza / nieznane – z danych postępowania odczytanych z dokumentów (ogłoszenie, tryb) i z ogłoszenia na liście (TED = unijne)."""
    import trasy_projekty_wykonawcy as _TW
    m = m or meta(pid)
    P = dict((czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie") or {})
    t = (m.get("przetarg") or {})
    t_ = db_przetargi().get(m.get("przetarg_numer") or t.get("numer") or "") or {}
    P["tryb"] = " ".join(str(x or "") for x in (P.get("tryb"), t_.get("tryb") or t.get("tryb")))
    if str(t_.get("zrodlo") or t.get("zrodlo") or "").upper() == "TED":
        P["ogloszenie"] = (str(P.get("ogloszenie") or "") + " TED").strip()
    elif not P.get("ogloszenie") and str(t_.get("zrodlo") or t.get("zrodlo") or "").upper() == "BZP":
        P["ogloszenie"] = "BZP"
    return _TW.podpis_oferty(P)["rodzaj"]


def termin_pytan_projektu(pid, m=None, termin=None):
    """Ostatni dzień na wniosek o wyjaśnienie, na który zamawiający musi odpowiedzieć: 4 dni (tryb podstawowy) albo 14 dni (procedura unijna)
    przed terminem składania ofert; gdy wypada w dzień wolny – także ostatni dzień roboczy przed nim. None, gdy brak terminu albo poza Pzp."""
    m = m or meta(pid)
    if termin is None:
        termin = dane_przetargu(m, pid).get("termin_ofert") if m.get("przetarg") else \
            (czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie", {}).get("termin_skladania")
    d = AN.data_i_godzina(str(termin or "").replace("T", " ")) if termin and not re.match(r"\d{4}-\d{2}-\d{2}", str(termin)) else str(termin or "")[:10]
    try:
        t = dt.date.fromisoformat(str(d)[:10])
    except ValueError:
        return None
    rp = rodzaj_postepowania_projektu(pid, m)
    if rp == "poza":
        return None
    un = rp == "unijne"
    import kontrola_zam as _KO
    wn, odp = PZ_.terminy_pytan(t.isoformat(), un)
    dzis = dt.date.today()
    praktycznie = _KO.poprzedni_roboczy(wn) if _KO.wolny(wn) else None
    return {"data": wn.isoformat(), "minal": wn < dzis, "dni": (wn - dzis).days, "praktycznie": praktycznie.isoformat() if praktycznie else "",
            "odpowiedz_do": odp.isoformat(), "unijne": un, "rodzaj": rp, "podstawa": "art. 135 ust. 2 Pzp" if un else "art. 284 ust. 2 Pzp",
            "dni_przed": 14 if un else 4, "termin_ofert": t.isoformat()}


def dokumenty_zmienione(pid, co="Zmieniono dokumenty"):
    """Po zmianie dokumentacji w kroku 1 wynik „Błędy i ryzyka” / sprawdzenia dokumentacji jest nieaktualny."""
    with BLOKADA:
        m = meta(pid)
        if m.get("weryfikacja"):
            m["weryfikacja"]["nieaktualna"] = f"{co} po sprawdzeniu – sprawdź dokumentację ponownie."
            zapisz_meta(pid, m)


def rozbieznosci_projektu(pid, m=None):
    m = m or meta(pid)
    dane = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    if not dane.get("dzialy") and not dane.get("_poza_cena"):
        return {"lista": [], "warianty": []}
    lst = ROZB.lista(dane, m.get("rozbieznosci"))
    war = ROZB.lista_wariantow(dane)
    rw = ROZB.rodzaj_wynagrodzenia(dane)
    return {"lista": lst, "wynagrodzenie": rw, "termin_pytan": termin_pytan_projektu(pid, m, (dane.get("postepowanie") or {}).get("termin_skladania")) if (m.get("typ") or "przetarg") == "przetarg" else ROZB.termin_pytan((dane.get("postepowanie") or {}).get("termin_skladania")),
            "w_cenie": MO.zaokr(sum(x["wartosc"] for x in lst if x["w_cenie"])), "na_umowe": MO.zaokr(sum(x["wartosc"] for x in lst if x["decyzja"] == "umowa")),
            "ostrzezenie": ROZB.OSTRZEZENIE_RYCZALT if rw == "ryczalt" else "", "decyzje": ROZB.DECYZJE, "warianty": war,
            "podpowiedz": "pytanie" if rw == "ryczalt" else "umowa" if rw == "kosztorysowe" else "cena"}


def _po_decyzji_kosztorysu(pid, orig):
    """Decyzja o rozbieżności albo wariancie zmieniła dane pierwotne kosztorysu: zapis i ponowne zastosowanie bieżącej korekty ceny
    (jako procentowej – do zmienionego zakresu). Zwraca opis dla użytkownika albo komunikat błędu (blad, None)."""
    d = pdir(pid)
    for k in ("netto", "vat_kwota", "brutto"):
        orig.pop(k, None)
    orig = MO.przelicz(orig)
    pisz(os.path.join(d, "oferta_dane_oryginal.json"), orig)
    kor = (meta(pid).get("oferta") or {}).get("korekta") or {}
    if kor.get("procent"):
        blad = zastosuj_korekte(pid, orig, "procent", float(kor["procent"]))
        if blad:
            return None, blad
        o = meta(pid).get("oferta") or {}
        info = (f"Korekta ceny {str(kor['procent']).replace('.', ',')}% zastosowana do zmienionego zakresu – cena oferty: {MO.zl(o.get('brutto') or 0)} brutto."
                + (" Cena docelowa wpisana kwotą zamieniona na korektę procentową – ustaw kwotę ponownie, jeśli ma zostać ta sama." if kor.get("tryb") in ("brutto", "netto") else ""))
        return info, None
    zapisz_oferte(pid, json.loads(json.dumps(orig)), cfg())
    return "", None


def ustaw_rozbieznosc(pid, rid, decyzja, potwierdzam=False, odpowiedz=None, kto=""):
    """Zapisuje decyzję wykonawcy. Zwraca (wynik, kod HTTP). Zmiana zakresu – na danych pierwotnych, z zachowaniem korekty ceny."""
    if decyzja not in ROZB.DECYZJE:
        return {"blad": "Nieznana decyzja."}, 400
    d = pdir(pid)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane:
        return {"blad": "Projekt nie ma jeszcze kosztorysu."}, 400
    orig = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or json.loads(json.dumps(dane))
    m = meta(pid)
    if decyzja == "umowa" and ROZB.rodzaj_wynagrodzenia(dane) == "ryczalt" and not potwierdzam:
        return {"potwierdz": ROZB.OSTRZEZENIE_RYCZALT}, 409
    p, zm = ROZB.ustaw(orig, rid, decyzja)
    if p is None:
        return {"blad": "Nie ma takiej pozycji spoza przedmiaru."}, 404
    if not orig.get("dzialy"):
        return {"blad": "Nie można wyłączyć z ceny wszystkich pozycji – kosztorys musi mieć co najmniej jedną pozycję."}, 400
    zapis = m.setdefault("rozbieznosci", {}).setdefault(rid, {})
    zapis.update(decyzja=decyzja, kiedy=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), kto=kto, opis=str(p.get("opis", ""))[:200])
    if odpowiedz is not None:
        zapis["odpowiedz"] = str(odpowiedz)[:1000]
    if decyzja == "pytanie":
        pyt = ROZB.pytanie_tekst(p)
        if pyt not in (orig.setdefault("pytania_do_zamawiajacego", [])):
            orig["pytania_do_zamawiajacego"].append(pyt)
    zapisz_meta(pid, m)
    info, blad = _po_decyzji_kosztorysu(pid, orig)
    if blad:
        return {"blad": blad}, 400
    return {"rozbieznosci": rozbieznosci_projektu(pid), "oferta": meta(pid).get("oferta"), "info": info, "zmiana_zakresu": zm}, 200


def ustaw_wariant(pid, wid, wybrany, pytanie=None, kto=""):
    """Wybór wariantu przy rozbieżności w dokumentach (a = przedmiar, b = inny dokument) i ewentualne pytanie do zamawiającego."""
    if wybrany not in ("a", "b"):
        return {"blad": "Wybierz wariant a albo b."}, 400
    d = pdir(pid)
    dane = czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane:
        return {"blad": "Projekt nie ma jeszcze kosztorysu."}, 400
    w = next((x for x in dane.get("warianty") or [] if isinstance(x, dict) and x.get("id") == wid), None)
    if not w:
        return {"blad": "Nie ma takiej rozbieżności."}, 404
    orig = czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or json.loads(json.dumps(dane))
    m = meta(pid)
    zapis = m.setdefault("warianty", {}).setdefault(wid, {})
    zapis.update(wybrany=wybrany, kiedy=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), kto=kto, lp=w.get("lp", ""))
    if pytanie is not None:
        zapis["pytanie"] = bool(pytanie)
    zapisz_meta(pid, m)
    ROZB.normalizuj_warianty(orig, m["warianty"], wymus=wid)  # cena wariantu na danych pierwotnych; korekta – przy przeliczeniu
    if zapis.get("pytanie"):
        pyt = ROZB.pytanie_wariantu(w)
        if pyt not in orig.setdefault("pytania_do_zamawiajacego", []):
            orig["pytania_do_zamawiajacego"].append(pyt)
    info, blad = _po_decyzji_kosztorysu(pid, orig)
    if blad:
        return {"blad": blad}, 400
    return {"rozbieznosci": rozbieznosci_projektu(pid), "oferta": meta(pid).get("oferta"), "info": info}, 200


def ostrzezenia_wniosku(pid, m, w):
    """Ostrzeżenia do wniosku o zmianę umowy: roboty ujęte już w cenie oferty, ryczałt, braki w kosztorysie."""
    wyn = []
    oferta = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    wo = [p for p in w.get("prace") or [] if p.get("w_ofercie")]
    pom = [p for p in wo if p not in ROZB.do_kosztorysu(w.get("prace"))]
    if pom:
        wyn.append(f"{len(pom)} z {len(w.get('prace') or [])} robót jest już w cenie oferty – nie wejdą do kosztorysu wniosku.")
    if w.get("rodzaj") != "przeszkody" and ROZB.rodzaj_wynagrodzenia(oferta) == "ryczalt":
        wyn.append("Wynagrodzenie jest ryczałtowe: zakres wynikający z dokumentacji znanej przed ofertą jest w cenie. Wniosek ma podstawę tylko "
                   "dla okoliczności, których nie dało się przewidzieć z dokumentów, albo dla zmian zleconych przez zamawiającego.")
    kos = czytaj(os.path.join(pdir(pid), "wnioski", f"kosztorys_{w['id']}.json"), {}) or {}
    if any("[UZUPEŁNIJ" in str(p.get("opis", "") if isinstance(p, dict) else p) for dz in kos.get("dzialy", []) for p in dz.get("pozycje", [])):
        wyn.append("Kosztorys wniosku ma pozycje z polem [UZUPEŁNIJ] – uzupełnij je przed wygenerowaniem wniosku.")
    return wyn


def odswiez_wniosek(pid, m, w):
    """Oznacza roboty wniosku ujęte w cenie oferty i przelicza ostrzeżenia (po każdej zmianie wykazu robót)."""
    oferta = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    ROZB.oznacz_prace(w.get("prace") or [], oferta)
    w["ostrzezenia"] = ostrzezenia_wniosku(pid, m, w)
    return w


NAZWA_ODLICZEN = "Odliczenie robót zastępowanych (z kosztorysu ofertowego)"


def bledy_dokumentacji(pid, m):
    """Błędy i różnice w dokumentacji przetargowej wykryte przez program: sprawdzenie dokumentacji (AI) oraz uwagi
    „do weryfikacji”, ryzyka i pytania z analizy przy przygotowaniu oferty."""
    wyn = []
    for u in (m.get("weryfikacja") or {}).get("uwagi", []):
        if u.get("status") != "odrzucone":
            wyn.append({"id": "w" + u["id"], "waga": u.get("waga", ""), "dokument": u.get("dokument", ""), "miejsce": u.get("miejsce", ""),
                        "opis": u.get("opis", ""), "propozycja": u.get("propozycja", ""), "zrodlo": "sprawdzenie dokumentacji",
                        "cytat": u.get("cytat", ""), "kategoria": u.get("kategoria", ""), "odw": u.get("odw"),
                        "pytanie": u.get("pytanie_do_zamawiajacego", ""), "perspektywa": (m.get("weryfikacja") or {}).get("perspektywa", "")})
    for i, b in enumerate((m.get("analiza_dostawcy") or {}).get("bledy") or []):  # dostawca: błędy z kroku 2 „Analiza przetargu”
        if isinstance(b, dict) and not b.get("z_weryfikacji"):  # te z osobnego sprawdzenia są już wyżej (z weryfikacji)
            wyn.append({"id": f"ad{i}", "waga": {"wysoka": "krytyczna", "średnia": "istotna", "niska": "drobna"}.get(b.get("waga", ""), "istotna"),
                        "dokument": b.get("dokument", ""), "miejsce": b.get("miejsce") or b.get("gdzie", ""), "opis": b.get("opis", ""), "propozycja": "",
                        "zrodlo": "analiza przetargu", "cytat": b.get("cytat", ""), "kategoria": "", "odw": b.get("odw"),
                        "pytanie": b.get("pytanie_do_zamawiajacego", ""), "perspektywa": "wykonawca"})
    o = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    for klucz, waga in (("do_weryfikacji", "istotna"), ("ryzyka", "istotna"), ("pytania_do_zamawiajacego", "drobna")):
        for i, t in enumerate(o.get(klucz) or []):
            t = str(t)
            if t.startswith("Stawka VAT nie wynika"):
                continue
            wyn.append({"id": f"{klucz[:3]}{i}", "waga": waga, "dokument": "analiza przy ofercie", "miejsce": "", "opis": t, "propozycja": "",
                        "zrodlo": {"do_weryfikacji": "do weryfikacji", "ryzyka": "ryzyka", "pytania_do_zamawiajacego": "pytania do zamawiającego"}[klucz]})
    return wyn


def plik_bledow(pid, m=None):
    m = m or meta(pid)
    bl = bledy_dokumentacji(pid, m)
    if not bl:
        return None
    c = cfg()
    kat = os.path.join(pdir(pid), "wnioski")
    os.makedirs(kat, exist_ok=True)
    nazwa = "Wykaz_bledow_dokumentacji_przetargowej.docx"
    WN.bledy_docx(os.path.join(kat, nazwa), bl, m.get("nazwa", ""), dane_umowy_projektu(pid, m),
                  {"nazwa": c.get("firma_nazwa", ""), "adres": c.get("firma_adres", "")})
    return f"wnioski/{nazwa}"








def praca_kosztorys_wniosku(log, pid, wid):
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    w = _wniosek(m, wid)
    if not w or not w.get("prace"):
        raise ValueError("Najpierw wpisz wykaz prac (opis, j.m., ilość) i zapisz wniosek.")
    baza = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    odswiez_wniosek(pid, m, w)
    zapisz_meta(pid, m)
    prace_k = ROZB.do_kosztorysu(w["prace"])
    pominiete = [p for p in w["prace"] if p not in prace_k]
    if pominiete:
        log(f"Pomijam {len(pominiete)} robót ujętych już w cenie oferty: " + "; ".join(
            f"{p['opis'][:50]} (poz. {', '.join(str(x.get('lp')) for x in p['w_ofercie'][:2])})" for p in pominiete[:8]) + ("…" if len(pominiete) > 8 else ""))
    if not prace_k:
        raise ValueError("Wszystkie roboty z wykazu są już ujęte w cenie oferty – wniosek nie ma czego wyceniać. Zostaw w wykazie tylko roboty, "
                         "których nie ma w kosztorysie ofertowym, oznacz robotę jako zamienną albo dopisz „mimo to: powód”.")
    ceny = []
    for dz in baza.get("dzialy", []):
        for p in dz.get("pozycje", []):
            if isinstance(p, dict) and p.get("opis"):
                ceny.append(f"{p.get('opis')} | {p.get('jm', '')} | {p.get('cena', 0)}")
            elif isinstance(p, (list, tuple)) and len(p) > 4:
                ceny.append(f"{p[1]} | {p[2]} | {p[4]}")
    wykaz = "\n".join(f"{i}. {p['opis']} | {p['jm']} | {p['ilosc']:g}"
                      + (" | ROBOTA ZAMIENNA – wyceń pełne nowe rozwiązanie; odliczenie pozycji zastępowanych doliczy program" if p.get("zamienna") else "")
                      for i, p in enumerate(prace_k, 1))
    polecenie = (f"Przygotuj KOSZTORYS {'PRAC DODATKOWYCH' if w['rodzaj'] == 'prace_dodatkowe' else 'ROBÓT DODATKOWYCH / ZAMIENNYCH'} do umowy "
                 f"na zadanie: {m.get('nazwa', '')}.\n\nWYKAZ PRAC (opis | j.m. | ilość):\n{wykaz}\n\n"
                 + (f"Uzasadnienie wykonawcy: {w.get('uzasadnienie', '')}\n\n" if w.get("uzasadnienie") else "")
                 + ("CENY JEDNOSTKOWE Z KOSZTORYSU OFERTOWEGO (opis | j.m. | cena netto) – dla robót takich samych lub podobnych użyj "
                    "tych cen (zasada umowna: ceny z oferty), dla nowych robót – ceny rynkowe na tym samym poziomie:\n" + "\n".join(ceny[:500]) + "\n\n"
                    if ceny else "")
                 + "Zachowaj ilości z wykazu. Wyceniaj tylko roboty z wykazu – niczego nie dodawaj. Nie używaj znacznika [UZUPEŁNIJ]: brakujące "
                   "dane opisz w uwagach pozycji. Oszacuj też, ile dni roboczych zajmie wykonanie tych robót typową brygadą. Zwróć WYŁĄCZNIE JSON: "
                   "{\"dzialy\": [{\"nazwa\": \"1. …\", \"pozycje\": "
                   "[[\"podstawa (KNR/kalkulacja)\", \"opis\", \"j.m.\", ilość, cena_jedn_netto, 1, \"źródło ceny: oferta/rynek\", \"uwagi\"]]}], "
                   "\"dni_realizacji\": liczba_dni_roboczych, \"uwagi\": [\"…\"]}")
    log(f"AI przygotowuje kosztorys {len(prace_k)} pozycji" + (" (ceny z kosztorysu ofertowego tam, gdzie to możliwe)…" if ceny else "…"))
    txt, _ = MO.claude_stream(c, "Jesteś doświadczonym kosztorysantem robót budowlanych w Polsce. Odpowiadasz wyłącznie JSON-em.",
                              [{"type": "text", "text": polecenie}], max_tokens=16000, log=log)
    dane = MO.wyciagnij_json(txt)
    if not dane.get("dzialy"):
        raise ValueError("Nie udało się odczytać kosztorysu – spróbuj ponownie.")
    if c.get("ceny_internet", True):  # ceny nowych robót (nie z kosztorysu ofertowego) sprawdzane w internecie tak samo jak w kosztorysie oferty
        pola = ("podstawa", "opis", "jm", "ilosc", "cena", "rynkowa", "zrodlo", "uwagi")
        for dz in dane.get("dzialy", []):
            dz["pozycje"] = [dict(zip(pola, list(p) + [""] * (len(pola) - len(p)))) if isinstance(p, (list, tuple)) else p for p in dz.get("pozycje", [])]
            for p in dz["pozycje"]:
                for k in ("ilosc", "cena"):
                    try:
                        p[k] = float(p.get(k) or 0)
                    except (TypeError, ValueError):
                        p[k] = 0.0
        try:
            CR.weryfikuj_kosztorys(c, dane, log, (baza.get("postepowanie") or {}).get("obiekt", "") or region_domyslny(c))
        except Exception as e:
            log(f"Nie udało się sprawdzić cen w internecie ({str(e)[:80]}) – zostają ceny oszacowane przez AI.")
    return zapisz_kosztorys_wniosku(pid, wid, dane, log)


def zapisz_kosztorys_wniosku(pid, wid, dane, log=None):
    m = meta(pid)
    w = _wniosek(m, wid)
    um = dane_umowy_projektu(pid, m)
    zam_ = dane_zamawiajacego_budowy(pid, m)
    dane.setdefault("postepowanie", {}).update(nazwa_zamowienia=f"{m.get('nazwa', '')} – {w['rodzaj_nazwa'].lower()} (wniosek {w['nr']})",
                                                vat=um["vat"], zamawiajacy_nazwa=zam_.get("nazwa", ""), zamawiajacy_adres=zam_.get("adres", ""),
                                                obiekt=um.get("adres", ""))
    for k in ("do_weryfikacji", "ryzyka", "pytania_do_zamawiajacego"):
        dane.setdefault(k, [])
    # roboty zamienne: od ceny nowego rozwiązania odejmuje się pozycje kosztorysu ofertowego, które ono zastępuje
    dane["dzialy"] = [dz for dz in dane.get("dzialy", []) if str(dz.get("nazwa", "")).strip() != NAZWA_ODLICZEN]
    odl = ROZB.odliczenia(odswiez_wniosek(pid, m, w).get("prace"))
    if odl:
        dane["dzialy"].append({"nazwa": NAZWA_ODLICZEN, "pozycje": [
            {"podstawa": "kosztorys ofertowy", "opis": f"Odliczenie: poz. {x.get('lp')} – {x.get('opis')}", "jm": x.get("jm", ""), "ilosc": x.get("ilosc", 0),
             "cena": -abs(float(x.get("cena") or 0)), "zrodlo": "kosztorys ofertowy", "uwagi": "robota zastępowana przez robotę zamienną"} for x in odl]})
    dane = MO.przelicz(dane)
    dane["_tytul"] = "KOSZTORYS PRAC DODATKOWYCH" if w["rodzaj"] == "prace_dodatkowe" else "KOSZTORYS ROBÓT DODATKOWYCH / ZAMIENNYCH"
    kat = os.path.join(pdir(pid), "wnioski")
    os.makedirs(kat, exist_ok=True)
    nazwa = f"Kosztorys_{w['nr'].replace('/', '-')}_{'prace_dodatkowe' if w['rodzaj'] == 'prace_dodatkowe' else 'roboty_dodatkowe_zamienne'}.xlsx"
    MO.zapisz_kosztorys(dane, cfg(), os.path.join(kat, nazwa), dla_klienta=True)
    pisz(os.path.join(kat, f"kosztorys_{wid}.json"), dane)
    m = meta(pid)
    w = _wniosek(m, wid)
    # kwota z kosztorysu = kwota proponowana dla zamawiającego (użytkownik może ją zmienić)
    w.update(kosztorys_plik=f"wnioski/{nazwa}", kwota_netto=dane["netto"], vat=dane["vat"], kwota_kosztorysu=dane["netto"])
    odswiez_wniosek(pid, m, w)
    try:
        dr = int(float(dane.get("dni_realizacji") or 0))
    except (TypeError, ValueError):
        dr = 0
    if dr > 0:
        w.setdefault("propozycja", {})["dni_realizacji"] = dr
        if not w.get("dni"):
            w["dni"] = int(round(dr * 7 / 5))  # dni robocze → kalendarzowe
    zapisz_meta(pid, m)
    if log:
        log(f"Kosztorys gotowy: {MO.zl(dane['netto'])} netto.")
    return {"netto": dane["netto"]}


def praca_propozycja_wniosku(log, pid, wid):
    """Propozycja AI: uzasadnienie wniosku, zakres prac dodatkowych / zamiennych i liczba dni przedłużenia,
    a potem kosztorys tych prac – kwota kosztorysu staje się kwotą proponowaną dla zamawiającego."""
    c = cfg()
    wymagany_klucz(c)
    c["_log"] = log
    m = meta(pid)
    w = _wniosek(m, wid)
    if not w:
        raise ValueError("Nie ma takiego wniosku.")
    um = dane_umowy_projektu(pid, m)
    baza = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
    dzialy = "\n".join(f"- {dz.get('nazwa', '')}: {MO.zl(dz.get('suma', 0))} netto" for dz in baza.get("dzialy", []))
    poz = [f"{p.get('lp') or ''} {p.get('opis', '')} [{p.get('jm', '')}]".strip() if isinstance(p, dict) else f"{p[1]} [{p[2]}]"
           for dz in baza.get("dzialy", []) for p in dz.get("pozycje", [])
           if (isinstance(p, dict) and p.get("opis")) or (isinstance(p, (list, tuple)) and len(p) > 2)][:200]
    w_cenie = [x for x in ROZB.lista(baza, m.get("rozbieznosci")) if x["w_cenie"]]
    na_umowe = ROZB.kandydaci(baza)
    r = realizacja_dane(pid)
    dziennik = "\n".join(f"{x.get('data')}: {x.get('prace', '')} {x.get('uwagi', '')}".strip() for x in (r.get("dziennik") or [])[-15:])
    usterki = "\n".join(f"- {u.get('tytul', '')}: {u.get('opis', '')}" for u in (r.get("usterki") or [])[-15:])
    bl = [b for b in bledy_dokumentacji(pid, m) if b["id"] in set(w.get("bledy") or [])]
    kontekst = [f"Zadanie: {m.get('nazwa', '')}. Umowa nr {um['nr'] or '?'} z {um['data'] or '?'}, termin zakończenia {um['termin'] or '?'}, "
                f"wynagrodzenie {MO.zl(um['wartosc'])} netto."]
    if dzialy:
        kontekst.append("Kosztorys ofertowy (działy):\n" + dzialy)
    if poz:
        kontekst.append("Pozycje kosztorysu ofertowego – ROBOTY JUŻ OPŁACONE CENĄ UMOWY (nie wolno ich proponować ponownie):\n" + "; ".join(poz))
    if w_cenie:
        kontekst.append("Roboty spoza przedmiaru, które wykonawca UJĄŁ W CENIE OFERTY (nie wolno ich proponować):\n" +
                        "\n".join(f"- {x['opis'][:160]} ({x['ilosc']:g} {x['jm']})" for x in w_cenie))
    if na_umowe:
        kontekst.append("Roboty spoza przedmiaru, które wykonawca ZOSTAWIŁ NA ETAP UMOWY (nie są w cenie – kandydaci do wniosku):\n" +
                        "\n".join(f"- {p.get('opis', '')[:160]} ({float(p.get('ilosc') or 0):g} {p.get('jm', '')})" for p in na_umowe))
    if bl:
        kontekst.append("Błędy / różnice w dokumentacji przetargowej wskazane przez wykonawcę:\n" +
                        "\n".join(f"- {b['dokument']} {b.get('miejsce', '')}: {b['opis']}" + (f" (propozycja: {b['propozycja']})" if b.get("propozycja") else "") for b in bl))
    if w["rodzaj"] == "przeszkody":
        kontekst.append(f"Przeszkoda: {w.get('przyczyna', '')}; okres {w.get('od', '?')} – {w.get('do', '?')}; organ/pismo: {w.get('organ', '')}; "
                        f"dokumenty: {w.get('dokumenty', '')}.")
    if w.get("uzasadnienie"):
        kontekst.append("Notatki / opis wykonawcy: " + w["uzasadnienie"])
    if w.get("prace"):
        kontekst.append("Prace wpisane przez wykonawcę: " + "; ".join(f"{p['opis']} {p['ilosc']:g} {p['jm']}" for p in w["prace"]))
    if dziennik:
        kontekst.append("Ostatnie raporty dzienne wykonawcy (dziennik pomocniczy, nie dziennik budowy):\n" + dziennik)
    if usterki:
        kontekst.append("Usterki / zadania na budowie:\n" + usterki)
    cel = {"prace_dodatkowe": "wniosek o prace dodatkowe (roboty nieobjęte umową, konieczne do prawidłowego wykonania zamówienia)",
           "roznice_dokumentacji": "wniosek z powodu błędów / różnic między dokumentacją przetargową a stanem rzeczywistym (roboty dodatkowe lub zamienne)",
           "przeszkody": "wniosek o przedłużenie terminu z powodu przeszkody niezależnej od wykonawcy"}[w["rodzaj"]]
    polecenie = ("\n\n".join(kontekst) + f"\n\nZADANIE: przygotuj propozycję – {cel}.\n"
                 "1. \"uzasadnienie\": rzeczowe uzasadnienie do pisma (5–10 zdań, język formalny, fakty z kontekstu; bez zmyślania dat i numerów – "
                 "brakujące oznacz [UZUPEŁNIJ]).\n"
                 "2. \"prace\": zakres robót dodatkowych / zamiennych wynikający z sytuacji – konkretne pozycje z jednostką i szacowaną ilością "
                 "(dla przeszkód zwykle pusta lista albo tylko roboty zabezpieczające). Proponuj WYŁĄCZNIE roboty, których nie ma w kosztorysie "
                 "ofertowym ani wśród robót ujętych w cenie oferty: roboty zostawione na etap umowy oraz roboty wynikające z dziennika budowy, "
                 "usterek, przeszkód i warunków innych niż w dokumentacji. Gdy takich robót nie ma, zwróć pustą listę. Robotę, która zastępuje "
                 "pozycję kosztorysu ofertowego innym rozwiązaniem, oznacz \"zamienna\": true. Nie używaj znacznika [UZUPEŁNIJ] w opisie roboty.\n"
                 "3. \"dni\": proponowane przedłużenie terminu w dniach kalendarzowych (czas robót dodatkowych i/lub czas trwania przeszkody "
                 "z zapasem na wznowienie robót) oraz \"uzasadnienie_dni\" (1–2 zdania).\n"
                 "Zwróć WYŁĄCZNIE JSON: {\"uzasadnienie\": \"…\", \"prace\": [{\"opis\": \"…\", \"jm\": \"…\", \"ilosc\": liczba, \"zamienna\": false}], "
                 "\"dni\": liczba, \"uzasadnienie_dni\": \"…\"}")
    log("AI przygotowuje uzasadnienie, zakres prac i proponowany termin…")
    txt, _ = MO.claude_stream(c, "Jesteś doświadczonym kierownikiem budowy i specjalistą od rozliczeń umów o roboty budowlane w Polsce. "
                                 "Odpowiadasz wyłącznie JSON-em.", [{"type": "text", "text": polecenie}], max_tokens=8000, log=log)
    d = MO.wyciagnij_json(txt)
    if not d.get("uzasadnienie"):
        raise ValueError("Nie udało się odczytać propozycji – spróbuj ponownie.")
    prace = []
    for p in d.get("prace") or []:
        try:
            prace.append({"opis": str(p.get("opis", ""))[:400], "jm": str(p.get("jm", ""))[:20], "ilosc": float(str(p.get("ilosc") or 0).replace(",", ".")),
                          **({"zamienna": True} if p.get("zamienna") is True else {})})
        except (ValueError, AttributeError):
            continue
    try:
        dni = max(0, int(float(d.get("dni") or 0)))
    except (TypeError, ValueError):
        dni = 0
    m = meta(pid)
    w = _wniosek(m, wid)
    w.update(uzasadnienie=str(d["uzasadnienie"])[:4000], dni=dni,
             propozycja={"dni": dni, "uzasadnienie_dni": str(d.get("uzasadnienie_dni", ""))[:500], "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    if prace:
        w["prace"] = prace[:100]
    odswiez_wniosek(pid, m, w)
    zapisz_meta(pid, m)
    log(f"Propozycja: {len(prace)} pozycji prac, przedłużenie o {dni} dni.")
    if ROZB.do_kosztorysu(w.get("prace")):
        praca_kosztorys_wniosku(log, pid, wid)
        m = meta(pid)
        w = _wniosek(m, wid)
        w["propozycja"]["kwota"] = w.get("kwota_kosztorysu")
        w["propozycja"]["dni"] = w.get("dni")
        zapisz_meta(pid, m)
    elif w.get("prace"):
        log("Wszystkie zaproponowane roboty są już w cenie oferty – kosztorysu nie przygotowano.")
    log("Sprawdź propozycję, popraw ją w razie potrzeby i kliknij „Akceptuję – generuj wniosek”.")
    return {"dni": w.get("dni"), "kwota": w.get("kwota_netto")}
















@app.post("/api/projekty/<pid>/bledy-dokumentacji")
@wymaga_logowania
def bledy_plik(pid):
    p = plik_bledow(pid)
    if not p:
        return jsonify({"blad": "Brak wykrytych błędów – kliknij „Wykryj błędy dokumentacji (AI)”."}), 400
    return jsonify({"url": f"/pobierz/{pid}/{p}"})


# ---------- monitoring pogody i pisma o niekorzystnych warunkach (wykonawca)



def zapisz_pomiar_imgw(pid, stacja):
    """Zapisuje bieżący pomiar najbliższej stacji IMGW w historii budowy (dowód pomiarowy dla pism)."""
    if not stacja or not stacja.get("pomiar"):
        return
    with BLOKADA:
        r = realizacja_dane(pid)
        lst = r.setdefault("pogoda_imgw", [])
        p = dict(stacja["pomiar"], stacja=stacja["nazwa"], odl_km=stacja["odl_km"])
        if not any(x.get("data") == p.get("data") and str(x.get("godzina")) == str(p.get("godzina")) for x in lst):
            lst.append(p)
            r["pogoda_imgw"] = lst[-1500:]
            zapisz_realizacje(pid, r)






def dane_zamawiajacego_budowy(pid, m):
    um = (m.get("umowa") or {}).get("pola") or {}
    if um.get("zam_nazwa"):
        return {"nazwa": um["zam_nazwa"], "adres": um.get("zam_adres", "")}
    d = dane_przetargu(m, pid) if m.get("przetarg") else {}
    P = (czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}).get("postepowanie", {})
    return {"nazwa": d.get("zamawiajacy") or P.get("zamawiajacy_nazwa", ""), "adres": d.get("zamawiajacy_adres") or P.get("zamawiajacy_adres", "")}






def plik_meteo(pid):
    return os.path.join(pdir(pid), "realizacja", "meteo_imgw.json")


def zbieraj_meteo():
    """Co 10 minut: pomiary najbliższych stacji sieci telemetrycznej IMGW-PIB dla budów z monitoringiem pogody (jedno pobranie dla wszystkich).
    Dobowe sumy opadu i ekstrema temperatury i wiatru powstają z kolejnych odczytów; luki (np. uśpiony serwer) widać w kompletności."""
    try:
        dane = POG._get_json(POG.IMGW_METEO, timeout=40)
    except Exception:
        return 0
    razem = 0
    for pid in os.listdir(PROJ):
        m = czytaj(os.path.join(PROJ, pid, "projekt.json"), None)
        if not m or m.get("status_projektu") != "realizacja" or m.get("archiwum"):
            continue
        u = (czytaj(os.path.join(PROJ, pid, "realizacja.json"), {}) or {}).get("pogoda") or {}
        if not u.get("lat"):
            continue
        kr = u.get("kryteria") or {}
        try:
            with BLOKADA:
                h = czytaj(plik_meteo(pid), {}) or {}
                n = POG.zapisz_meteo(h, u["lat"], u["lon"], dane, int(kr.get("godz_od", 7)), int(kr.get("godz_do", 17)))
                if n:
                    os.makedirs(os.path.dirname(plik_meteo(pid)), exist_ok=True)
                    pisz(plik_meteo(pid), h)
            razem += n
        except Exception as e:
            logging.warning("Pomiary IMGW (sieć telemetryczna), projekt %s: %s", pid, e)
    return razem


def _budowy_z_pogoda():
    for pid in os.listdir(PROJ):
        m = czytaj(os.path.join(PROJ, pid, "projekt.json"), None)
        if not m or m.get("status_projektu") != "realizacja" or m.get("archiwum"):
            continue
        u = (czytaj(os.path.join(PROJ, pid, "realizacja.json"), {}) or {}).get("pogoda") or {}
        if u.get("lat"):
            yield pid, u


def zbieraj_opad_dobowy():
    """Codziennie rano: oficjalna dobowa suma opadu IMGW-PIB (doba 06–06 UTC) z najbliższej stacji opadowej – także gdy serwer był uśpiony."""
    try:
        dane = POG._get_json(POG.IMGW_METEO, timeout=40)
    except Exception:
        dane = []
    for pid, u in _budowy_z_pogoda():
        try:
            with BLOKADA:
                h = czytaj(plik_meteo(pid), {}) or {}
            st = (h.get("stacje") or {}).get("opad") or {}
            if not st.get("kod"):
                x = POG.najblizsze_meteo(u["lat"], u["lon"], dane).get("opad")
                st = {"kod": x and x.get("kod"), "stacja": x and x["stacja"]}
            if not st.get("kod"):
                continue
            w = POG.opad_dobowy(st["kod"])
            if not w:
                continue
            dzien, v = w
            nast = (dt.date.fromisoformat(dzien) + dt.timedelta(days=1)).isoformat()
            with BLOKADA:
                h = czytaj(plik_meteo(pid), {}) or {}
                h.setdefault("dni", {}).setdefault(dzien, {})["opad_dobowy"] = {"wartosc": v, "stacja": st.get("stacja"), "kod": st["kod"],
                                                                                "okres": f"{dzien} 06:00 – {nast} 06:00 UTC"}
                os.makedirs(os.path.dirname(plik_meteo(pid)), exist_ok=True)
                pisz(plik_meteo(pid), h)
        except Exception as e:
            logging.warning("Opad dobowy IMGW, projekt %s: %s", pid, e)


def uzupelnij_archiwum_meteo():
    """Gdy IMGW opublikuje miesięczne archiwum 10-minutowe (po zakończeniu miesiąca): komplet danych za miesiąc dla każdej budowy –
    zastępuje dni z lukami. Archiwum pobierane raz na wszystkie budowy i usuwane po przetworzeniu."""
    budowy = list(_budowy_z_pogoda())
    if not budowy:
        return 0
    dzis = dt.date.today()
    miesiace = []
    for k in (1, 2):
        d = (dzis.replace(day=1) - dt.timedelta(days=1))
        for _ in range(k - 1):
            d = d.replace(day=1) - dt.timedelta(days=1)
        miesiace.append((d.year, d.month))
    try:
        dane = POG._get_json(POG.IMGW_METEO, timeout=40)
    except Exception:
        return 0
    zrobione = 0
    for rok, mies in miesiace:
        pref = f"{rok}-{mies:02d}"
        potrzebne = [(pid, u) for pid, u in budowy if pref not in ((czytaj(plik_meteo(pid), {}) or {}).get("archiwum_miesiace") or [])
                     and any(d.startswith(pref) for d in ((czytaj(plik_meteo(pid), {}) or {}).get("dni") or {}))]
        if not potrzebne:
            continue
        sc = os.path.join(DATA, "cache_imgw", f"Meteo_{pref}.zip")
        os.makedirs(os.path.dirname(sc), exist_ok=True)
        try:
            req = urllib.request.Request(POG.ARCHIWUM_MIES.format(rok=rok, mies=mies), headers={"User-Agent": "Mozilla/5.0 (Bidivia)"})
            with urllib.request.urlopen(req, timeout=600) as r:
                if "zip" not in (r.headers.get("Content-Type") or ""):
                    continue  # jeszcze nieopublikowane
                with open(sc, "wb") as f:
                    shutil.copyfileobj(r, f)
            for pid, u in potrzebne:
                kr = u.get("kryteria") or {}
                with BLOKADA:
                    h = czytaj(plik_meteo(pid), {}) or {}
                    n = POG.uzupelnij_z_archiwum(h, sc, rok, mies, POG.stacje_kandydaci(u["lat"], u["lon"], dane),
                                                 int(kr.get("godz_od", 7)), int(kr.get("godz_do", 17)))
                    pisz(plik_meteo(pid), h)
                zrobione += n
        except Exception as e:
            logging.warning("Archiwum IMGW %s: %s", pref, e)
        finally:
            if os.path.exists(sc):
                os.remove(sc)
    return zrobione


def zbieraj_pomiary_pogody():
    """Co kilka godzin zapisuje pomiary najbliższych stacji IMGW dla budów z monitoringiem pogody (wszystkie konta)."""
    try:
        pomiary = POG._get_json(POG.IMGW_SYNOP)
    except Exception:
        return
    for pid in os.listdir(PROJ):
        m = czytaj(os.path.join(PROJ, pid, "projekt.json"), None)
        if not m or m.get("status_projektu") != "realizacja" or m.get("archiwum"):
            continue
        u = (czytaj(os.path.join(PROJ, pid, "realizacja.json"), {}) or {}).get("pogoda") or {}
        if u.get("lat"):
            try:
                zapisz_pomiar_imgw(pid, POG.najblizsza_stacja(u["lat"], u["lon"], pomiary))
            except Exception:
                pass


# ---------- harmonogram rzeczowo-finansowy





def zapisz_hrf_xlsx(pid, sciezka):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter as L
    m, r = meta(pid), realizacja_dane(pid)
    hrf = przelicz_hrf(r["hrf"])
    dz, et = hrf["dzialy"], hrf["etapy"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "HRF"
    b = Font(bold=True, name="Arial", size=10)
    zw = Font(name="Arial", size=10)
    nag = PatternFill("solid", fgColor="DBE5FF")
    zol = PatternFill("solid", fgColor="FFF2CC")
    cz = Side(style="thin", color="999999")
    ramka = Border(left=cz, right=cz, top=cz, bottom=cz)
    ws["A1"] = "HARMONOGRAM RZECZOWO-FINANSOWY"
    ws["A1"].font = Font(bold=True, name="Arial", size=14)
    ws["A2"] = f"Zadanie: {m.get('nazwa')}   Umowa nr: {r.get('umowa_nr') or '…'} z dnia {r.get('data_umowy') or '…'}"
    if m.get("strona") in ("zamawiajacy", "inwestor"):  # zamawiający / inwestor: profil to zamawiający, wykonawca z umowy
        ws["A3"] = (f"Zamawiający: {cfg().get('firma_nazwa', '')}" + (f"   Wykonawca: {r['wykonawca_nazwa']}" if r.get("wykonawca_nazwa") else ""))
    else:
        ws["A3"] = f"Wykonawca: {cfg().get('firma_nazwa', '')}"
    for c in ("A2", "A3"):
        ws[c].font = zw
    n = len(et)
    rn = 5
    naglowki = ["Lp.", "Element robót (dział kosztorysu)", "Wartość netto [zł]"] + \
               [f"Etap {e['nr']}\n{e.get('od', '')} – {e.get('do', '')}\n[%]" for e in et] + ["Suma %"] + \
               [f"Etap {e['nr']}\n[zł netto]" for e in et]
    for i, h in enumerate(naglowki, 1):
        c = ws.cell(rn, i, h)
        c.font = b
        c.fill = nag
        c.border = ramka
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[rn].height = 48
    kp, kq = 4, 4 + n + 1
    for i, x in enumerate(dz):
        rr = rn + 1 + i
        ws.cell(rr, 1, i + 1)
        ws.cell(rr, 2, x["nazwa"])
        ws.cell(rr, 3, x["wartosc"]).number_format = "#,##0.00"
        for k, e in enumerate(et):
            c = ws.cell(rr, kp + k, (e["udzialy"][i] if i < len(e["udzialy"]) else 0) / 100)
            c.number_format = "0%"
            c.fill = zol
            ws.cell(rr, kq + k, f"=ROUND($C{rr}*{L(kp + k)}{rr},2)").number_format = "#,##0.00"
        ws.cell(rr, kp + n, f"=SUM({L(kp)}{rr}:{L(kp + n - 1)}{rr})").number_format = "0%"
        for c_ in range(1, kq + n):
            ws.cell(rr, c_).border = ramka
            ws.cell(rr, c_).font = zw
    ost = rn + len(dz)
    wiersze = [("RAZEM NETTO", None), (f"VAT {vat_realizacji(r):.0%}", vat_realizacji(r)), ("RAZEM BRUTTO", "b"),
               ("Narastająco netto", "n"), ("Narastająco [% umowy]", "p")]
    for j, (et_, typ) in enumerate(wiersze, 1):
        rr = ost + j
        ws.cell(rr, 2, et_).font = b
        if typ is None:
            ws.cell(rr, 3, f"=SUM(C{rn + 1}:C{ost})")
        for k in range(n + 1):
            col = L(kq + k) if k < n else "C"
            if k == n:
                continue
            if typ is None:
                f = f"=SUM({col}{rn + 1}:{col}{ost})"
            elif typ == "b":
                f = f"={col}{ost + 1}+{col}{ost + 2}"
            elif typ == "n":
                f = f"=SUM(${L(kq)}{ost + 1}:{col}{ost + 1})"
            elif typ == "p":
                f = f"=IF($C${ost + 1}=0,0,{col}{ost + 4}/$C${ost + 1})"
            else:
                f = f"=ROUND({col}{ost + 1}*{typ},2)"
            c = ws.cell(rr, kq + k, f)
            c.number_format = "0.0%" if typ == "p" else "#,##0.00"
            c.font = b
        if typ is None:
            ws.cell(rr, 3).number_format = "#,##0.00"
            ws.cell(rr, 3).font = b
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 16
    for k in range(kp, kq + n):
        ws.column_dimensions[L(k)].width = 14
    rr = ost + 8
    ws.cell(rr, 2, "Zatwierdził (Zamawiający): ........................").font = zw
    ws.cell(rr + 2, 2, "Sporządził (Wykonawca): ........................").font = zw
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    wb.save(sciezka)




# ---------- protokoły odbioru

@app.post("/api/projekty/<pid>/protokol")
@wymaga_logowania
def protokol(pid):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    j = request.json
    r = realizacja_dane(pid)
    if not r.get("hrf"):
        return jsonify({"blad": "Najpierw utwórz harmonogram rzeczowo-finansowy."}), 400
    hrf = przelicz_hrf(r["hrf"])
    try:
        k = int(j.get("etap"))
        e = hrf["etapy"][k]
        data = dt.date.fromisoformat(j.get("data") or dt.date.today().isoformat())
    except (TypeError, ValueError, IndexError):
        return jsonify({"blad": "Wybierz etap i datę odbioru."}), 400
    m = meta(pid)
    c = cfg()
    o = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}).get("postepowanie", {})
    # odbiór końcowy dopiero, gdy wszystkie pozostałe etapy są odebrane (nie „ostatni etap według kolejności”)
    nieodebrane = [x.get("nr") for i, x in enumerate(hrf["etapy"]) if i != k and x.get("status") != "odebrany"]
    koncowy = not nieodebrane
    vat = vat_realizacji(r)
    netto = e["wartosc"]
    vat_k = MO.zaokr(netto * vat)
    brutto = MO.zaokr(netto + vat_k)
    narast = MO.zaokr(sum(x["wartosc"] for x in hrf["etapy"][:k + 1]))
    umowa = r.get("wartosc_netto") or sum(x["wartosc"] for x in hrf["dzialy"]) or 1
    def dpl(x):
        try:
            return dt.date.fromisoformat(x).strftime("%d.%m.%Y")
        except (TypeError, ValueError):
            return x or ""
    d = MO._doc()
    P = lambda t, **kw: MO._akapit(d, t, **kw)
    P(f"PROTOKÓŁ ODBIORU {'KOŃCOWEGO' if koncowy else 'CZĘŚCIOWEGO'} NR {e['nr']}", pogrub=True, rozmiar=14,
      wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    P(f"sporządzony dnia {data:%d.%m.%Y} r. w {j.get('miejsce') or r.get('adres') or o.get('obiekt') or '[UZUPEŁNIJ: miejsce]'}",
      wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    P(f"Dotyczy umowy nr {r.get('umowa_nr') or '[UZUPEŁNIJ]'} z dnia {dpl(r.get('data_umowy')) or '[UZUPEŁNIJ]'} "
      f"na realizację zadania: {o.get('nazwa_zamowienia') or m.get('nazwa')}.")
    wyk_domu = next((x for x in (r.get("wykonawcy") or []) if x["id"] == j.get("wykonawca_id")), None)
    if wyk_domu:
        r.update(wykonawca_nazwa=wyk_domu.get("nazwa", ""), wykonawca_adres=wyk_domu.get("adres", ""), wykonawca_nip=wyk_domu.get("nip", ""))
    if (m.get("strona") or "wykonawca") in ("zamawiajacy", "inwestor"):  # protokół sporządza inwestor – role odwrócone
        zam_txt = (f"{c.get('firma_nazwa', '')}\n{c.get('firma_adres', '')}" if m.get("strona") == "inwestor" else zamawiajacy_projektu(m, o))
        wyk_txt = (f"{r.get('wykonawca_nazwa', '')}\n{r.get('wykonawca_adres', '')}" +
                   (f"\nNIP: {r['wykonawca_nip']}" if r.get("wykonawca_nip") else "")).strip() or "[UZUPEŁNIJ: wykonawca]"
    else:
        zam_txt = f"{o.get('zamawiajacy_nazwa', '')}\n{o.get('zamawiajacy_adres', '')}".strip() or "[UZUPEŁNIJ]"
        wyk_txt = f"{c.get('firma_nazwa', '')}\n{c.get('firma_adres', '')}"
    MO._tabela(d, [["Zamawiający", "Wykonawca"], [zam_txt, wyk_txt]])
    P("Komisja w składzie:", pogrub=True)
    P("Przedstawiciele Zamawiającego: " + (j.get("komisja_zam") or "[UZUPEŁNIJ]"))
    P("Przedstawiciele Wykonawcy: " + (j.get("komisja_wyk") or r.get("kierownik") or "[UZUPEŁNIJ]"))
    RZ = (m.get("rodzaj_zamowienia") or "roboty") if m.get("strona") == "zamawiajacy" else "roboty"
    if r.get("inspektor"):
        P(("Inspektor nadzoru: " if RZ == "roboty" else "Osoba nadzorująca realizację umowy: ") + r["inspektor"])
    przedm = {"uslugi": ("usług", "Element usług", "usługi objęte niniejszym protokołem zostały wykonane zgodnie z umową i opisem przedmiotu zamówienia"),
              "dostawy": ("dostaw", "Element dostawy", "dostawa objęta niniejszym protokołem została zrealizowana zgodnie z umową i opisem przedmiotu "
                          "zamówienia – ilościowo i jakościowo")}.get(RZ or "roboty", ("robót", "Element robót", "roboty objęte niniejszym protokołem zostały wykonane "
                                                                                    "zgodnie z umową, dokumentacją projektową, zasadami wiedzy technicznej i obowiązującymi przepisami"))
    P(f"1. Zakres {przedm[0]} objętych odbiorem – etap {e['nr']}: {e.get('nazwa', '')} "
      f"(termin wg harmonogramu: {dpl(e.get('od'))} – {dpl(e.get('do'))})", pogrub=True)
    bez_kwot = not moze("finanse")  # H1-04: rola bez Finansów (np. kierownik budowy) – protokół bez wartości (uzupełnia osoba z Finansami)
    wiersze = [["Lp.", przedm[1], "% zakresu w etapie"] + ([] if bez_kwot else ["Wartość netto [zł]"])]
    lp = 0
    for i, x in enumerate(hrf["dzialy"]):
        u = e["udzialy"][i] if i < len(e["udzialy"]) else 0
        if u:
            lp += 1
            wiersze.append([str(lp), x["nazwa"], f"{u:g}".replace(".", ",") + "%"] + ([] if bez_kwot else [MO.zl(x["wartosc"] * u / 100).replace(" zł", "")]))
    if not bez_kwot:
        wiersze.append(["", "RAZEM", "", MO.zl(netto).replace(" zł", "")])
    MO._tabela(d, wiersze)
    if RZ == "dostawy":  # odbiór ilościowo-jakościowy: asortyment i ilości w tej dostawie (z kosztorysu / formularza)
        od_ = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), {}) or {}
        poz_ = []
        for i, dzial in enumerate(od_.get("dzialy") or []):
            u = e["udzialy"][i] if i < len(e["udzialy"]) else 0
            for p_ in (dzial.get("pozycje") or []) if u else []:
                il = float(p_.get("ilosc") or 0) * float(u) / 100
                if il:
                    poz_.append([str(len(poz_) + 1), str(p_.get("opis") or "")[:140], str(p_.get("jm") or ""), f"{il:g}".replace(".", ","), "", ""])
        if poz_:
            P("Asortyment i ilości w dostawie:", pogrub=True)
            MO._tabela(d, [["Lp.", "Asortyment", "j.m.", "Ilość wg umowy", "Ilość dostarczona", "Uwagi"]] + poz_[:150])
        P(f"Zgodność ilościowa: {j.get('zgodnosc_ilosc') or '[tak / nie]'}. Zgodność jakościowa (parametry, stan, oznakowanie): "
          f"{j.get('zgodnosc_jakosc') or '[tak / nie]'}.")
        P(f"Dokumenty dostawy (WZ, karty gwarancyjne, instrukcje, certyfikaty): {j.get('dokumenty_dostawy') or '[UZUPEŁNIJ]'}.")
    elif RZ == "uslugi":
        P(f"Usługi w okresie rozliczeniowym wykonano należycie: {j.get('nalezycie') or '[tak / nie]'}"
          + (f". Potrącenia / kary za okres: {j['kary_okres']}" if j.get("kary_okres") else "") + ".")
    P(f"2. Wartość {przedm[0]} odebranych", pogrub=True)
    if bez_kwot:
        P("Netto: [UZUPEŁNIA osoba upoważniona do rozliczeń – według harmonogramu rzeczowo-finansowego]")
        P("VAT: [UZUPEŁNIA]          Brutto: [UZUPEŁNIA]")
    else:
        P(f"Netto: {MO.zl(netto)} (słownie: {MO.slownie(netto)})")
        P(f"VAT {vat:.0%}: {MO.zl(vat_k)}")
        P(f"Brutto: {MO.zl(brutto)} (słownie: {MO.slownie(brutto)})")
        P(f"Wartość {przedm[0]} odebranych narastająco: {MO.zl(narast)} netto, tj. " + f"{narast / umowa * 100:.1f}".replace(".", ",") + "% wartości umowy.")
    P("3. Ustalenia komisji", pogrub=True)
    P(f"Komisja stwierdza, że {przedm[2]}" + (" oraz dokonuje odbioru końcowego." if koncowy else " i dokonuje odbioru częściowego."))
    usterki = (j.get("usterki") or "").strip()
    if usterki:
        P("Stwierdzone usterki / wady do usunięcia:" if (RZ or "roboty") == "roboty" else "Stwierdzone nieprawidłowości / braki do usunięcia:")
        for u in [x for x in usterki.splitlines() if x.strip()]:
            P(u.strip(), styl="List Bullet")
        P(f"Termin usunięcia {'usterek' if RZ == 'roboty' else 'nieprawidłowości'}: {j.get('termin_usterek') or '[UZUPEŁNIJ]'}.")
    else:
        P("Nie stwierdzono wad ani usterek." if RZ == "roboty" else "Nie stwierdzono nieprawidłowości ani braków.")
    if (j.get("uwagi") or "").strip():
        P("4. Uwagi", pogrub=True)
        P(j["uwagi"].strip())
    P(f"{'5' if (j.get('uwagi') or '').strip() else '4'}. Niniejszy protokół stanowi podstawę do wystawienia faktury "
      f"{'końcowej' if koncowy else 'częściowej'} na kwotę " + ("wskazaną w pkt 2." if bez_kwot else f"{MO.zl(brutto)} brutto."), pogrub=True)
    P("Protokół sporządzono w dwóch jednobrzmiących egzemplarzach, po jednym dla każdej ze stron.")
    MO._tabela(d, [["Zamawiający:\n\n\n..........................................", "Wykonawca:\n\n\n.........................................."]],
               naglowek=False)
    rm_ = [x for x in ((r.get("rozliczenie_mat") or {}).get("pozycje") or []) if str(x.get("nazwa", "")).strip()]
    if koncowy and rm_ and j.get("dolacz_materialy", True):  # rozliczenie materiałów jako załącznik do protokołu końcowego
        karty_ = [x for x in rm_ if x.get("karta")]
        P("Załączniki:", pogrub=True)
        P(f"1. Wykaz materiałów zużytych / wbudowanych na budowie ({len(rm_)} pozycji).", styl="List Bullet")
        if karty_:
            P(f"2. Karty materiałowe ({len(karty_)}): " + "; ".join(x["nazwa"] for x in karty_[:30]) + ".", styl="List Bullet")
        d.add_page_break()
        dodaj_wykaz_materialow(d, rm_, "Załącznik nr 1 do protokołu odbioru końcowego")
    kat = os.path.join(pdir(pid), "realizacja", "protokoly")
    os.makedirs(kat, exist_ok=True)
    nazwa = f"Protokol_odbioru_{'koncowego' if koncowy else 'czesciowego'}_etap{e['nr']}_{data:%Y-%m-%d}{'_bez_kwot' if bez_kwot else ''}.docx"
    d.save(os.path.join(kat, nazwa))
    e.update(status="odebrany", data_odbioru=data.isoformat(), protokol=f"realizacja/protokoly/{nazwa}")
    r["hrf"] = hrf
    zapisz_realizacje(pid, r)
    return jsonify({"url": f"/pobierz/{pid}/realizacja/protokoly/{nazwa}", **({} if bez_kwot else {"netto": netto, "brutto": brutto, "vat": vat_k}),
                    "koncowy": koncowy, "ostrzezenie": (f"Protokół częściowy – nieodebrane etapy: {', '.join(str(x) for x in nieodebrane)}. Odbiór końcowy "
                                                        "po odebraniu wszystkich etapów." if nieodebrane and k == len(hrf["etapy"]) - 1 else "")})


# ---------- podwykonawcy: zgłoszenia, umowy, rozliczenia, oświadczenia

def _strony_budowy(pid, m, r):
    """Dane wykonawcy i zamawiającego – zależnie od tego, po której stronie jest konto."""
    c = cfg()
    firma = {"nazwa": c.get("firma_nazwa", ""), "adres": c.get("firma_adres", "")}
    if (m.get("strona") or "wykonawca") == "zamawiajacy":
        return {"nazwa": r.get("wykonawca_nazwa", ""), "adres": r.get("wykonawca_adres", "")}, firma
    return firma, dane_zamawiajacego_budowy(pid, m)


def _pw_lista(pid, r):
    lista = r.get("podwykonawcy") or []
    for x in lista:
        k = os.path.join(pdir(pid), "realizacja", "podwykonawcy", x["id"])
        x["pliki_umowy"] = sorted(os.listdir(os.path.join(k, "umowa"))) if os.path.isdir(os.path.join(k, "umowa")) else []
        x["pliki_oswiadczenia"] = sorted(os.listdir(os.path.join(k, "oswiadczenia"))) if os.path.isdir(os.path.join(k, "oswiadczenia")) else []
        x["pliki_dokumenty"] = sorted(os.listdir(os.path.join(k, "dokumenty"))) if os.path.isdir(os.path.join(k, "dokumenty")) else []
        x["sumy"] = PW.sumy(x)
        m_ = meta(pid)
        if isinstance(x.get("uwagi"), str) and not x.get("notatka"):  # dawny zapis: własne uwagi użytkownika były w polu „uwagi” (nadpisywanym ostrzeżeniami)
            x["notatka"] = x["uwagi"]
        x["uwagi"] = PW.uwagi(x, roboty=(m_.get("rodzaj_zamowienia") or "roboty") == "roboty" and m_.get("strona") != "inwestor") \
            if (m_.get("strona") or "wykonawca") == "wykonawca" else []
    return lista












# ---------- rozliczenie inwestycji: karta (wykaz) zużytych materiałów i karty materiałowe

def _materialy_z_listy(pid, m):
    """Pozycje z listy materiałów (krok „Zapotrzebowanie materiałowe”), a gdy jej nie ma – z pozycji kosztorysu."""
    import openpyxl
    d = pdir(pid)
    wyn = []
    if m.get("lista_materialow") and os.path.isfile(os.path.join(d, m["lista_materialow"])):
        ws = openpyxl.load_workbook(os.path.join(d, m["lista_materialow"]), data_only=True).worksheets[0]
        kol = None
        for w in ws.iter_rows(values_only=True):
            if kol is None:
                if w and "Materiał" in [str(x or "") for x in w]:
                    kol = {str(x or ""): i for i, x in enumerate(w)}
                continue
            naz = w[kol["Materiał"]] if kol.get("Materiał") is not None and kol["Materiał"] < len(w) else None
            if not naz or str(naz).startswith(("Razem", "RAZEM", "Materiały pomocnicze")) or w[0] in (None, "") and not w[kol.get("Jm", 3)]:
                continue
            g = lambda k_: w[kol[k_]] if kol.get(k_) is not None and kol[k_] < len(w) else None
            wyn.append({"nazwa": str(naz), "jm": str(g("Jm") or ""), "ilosc_kosztorys": g("Ilość wg kosztorysu") or g("Ilość do zamówienia") or 0,
                        "ilosc_zuzyta": g("Ilość do zamówienia") or g("Ilość wg kosztorysu") or 0, "zrodlo": "lista materiałów"})
    if not wyn:
        dane = czytaj(os.path.join(d, "oferta_dane.json"), {}) or {}
        for dz in dane.get("dzialy", []):
            for p in dz.get("pozycje", []):
                if isinstance(p, dict):
                    wyn.append({"nazwa": p.get("opis", ""), "jm": p.get("jm", ""), "ilosc_kosztorys": p.get("ilosc", 0), "ilosc_zuzyta": p.get("ilosc", 0),
                                "zrodlo": "pozycja kosztorysu"})
    for x in wyn:
        x.update(id=uuid.uuid4().hex[:8], producent="", dokumenty="", uwagi="", karta=False)
    return wyn










def _lb(x):
    return f"{float(x or 0):g}".replace(".", ",")


def dodaj_wykaz_materialow(d, poz, tytul):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    MO._akapit(d, tytul, kursywa=True, rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    MO._akapit(d, "WYKAZ MATERIAŁÓW ZUŻYTYCH (WBUDOWANYCH) NA BUDOWIE", pogrub=True, rozmiar=13, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._tabela(d, [["Lp.", "Materiał", "Producent / typ", "j.m.", "Ilość wg kosztorysu", "Ilość zużyta", "Dokumenty (DoP, CE/B, aprobata)", "Karta mat."]] +
               [[str(i), x["nazwa"], x.get("producent", ""), x.get("jm", ""), _lb(x.get("ilosc_kosztorys")), _lb(x.get("ilosc_zuzyta")),
                 x.get("dokumenty", ""), "tak" if x.get("karta") else "–"] for i, x in enumerate(poz, 1)])
    MO._akapit(d, "Oświadczamy, że wymienione materiały zostały wbudowane zgodnie z dokumentacją projektową i posiadają wymagane "
                  "dokumenty dopuszczające do obrotu i stosowania w budownictwie.", rozmiar=9)
    MO._tabela(d, [["Kierownik budowy:\n\n\n..........................................", "Inspektor nadzoru / Zamawiający:\n\n\n.........................................."]],
               naglowek=False)




# ---------- faktury i koszty

def _liczba(x):
    w = liczba(x, 0.0) if str(x if x is not None else "").strip() == "" else liczba(x)
    if w is None:
        raise ValueError(f"Nieprawidłowa kwota: {x}")  # faktura: błąd dla użytkownika zamiast kwoty 0
    return MO.zaokr(w)




@app.post("/api/projekty/<pid>/koszty")
@wymaga_logowania
def koszt_dodaj(pid):
    j = request.json
    try:
        netto = _liczba(j.get("netto"))
        data = dt.date.fromisoformat(j.get("data"))
    except (TypeError, ValueError):
        return jsonify({"blad": "Uzupełnij datę i kwotę netto kosztu."}), 400
    if netto == 0 or not str(j.get("opis", "")).strip():
        return jsonify({"blad": "Uzupełnij opis i kwotę netto kosztu."}), 400
    r = realizacja_dane(pid)
    r["koszty"].append({"id": uuid.uuid4().hex[:10], "data": data.isoformat(), "kategoria": str(j.get("kategoria", "inne"))[:40],
                        "opis": str(j["opis"]).strip()[:200], "dostawca": str(j.get("dostawca", ""))[:100],
                        "dokument": str(j.get("dokument", ""))[:60], "netto": netto, "zaplacona": bool(j.get("zaplacona")),
                        "kto": session.get("login", "")})
    zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


@app.post("/api/projekty/<pid>/<rodzaj>/zmien")
@wymaga_logowania
def pozycja_zmien(pid, rodzaj):
    if rodzaj not in ("faktury", "koszty"):
        abort(404)
    r = realizacja_dane(pid)
    j = request.json
    for x in r[rodzaj]:
        if x["id"] == j.get("id"):
            if j.get("usun"):
                r[rodzaj].remove(x)
            elif "zaplacona" in j:
                x["zaplacona"] = bool(j["zaplacona"])
                if rodzaj == "faktury":
                    x["data_zaplaty"] = (j.get("data_zaplaty") or dt.date.today().isoformat()) if x["zaplacona"] else None
            break
    zapisz_realizacje(pid, r)
    return jsonify({"ok": True})


@app.get("/api/projekty/<pid>/rozliczenie.xlsx")
@wymaga_logowania
def rozliczenie_xlsx(pid):
    import io
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    m, r, s_ = meta(pid), realizacja_dane(pid), podsumowanie_realizacji(pid)
    wb = openpyxl.Workbook()
    b, nag = Font(bold=True), PatternFill("solid", fgColor="DBE5FF")
    ws = wb.active
    ws.title = "Podsumowanie"
    ZR_ = m.get("strona") == "zamawiajacy"
    ws["A1"] = f"{'Rozliczenie umowy' if ZR_ else 'Rozliczenie budowy'}: {m.get('nazwa')}"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = f"Stan na {dt.date.today():%d.%m.%Y}"
    poz = [("Wartość umowy netto", s_["wartosc_umowy_netto"]), ("Odebrano (etapy) netto", s_["odebrano_netto"]),
           ("Zafakturowano netto", s_["zafakturowano_netto"]), ("Zafakturowano brutto", s_["zafakturowano_brutto"]),
           ("Zapłacono brutto", s_["zaplacono_brutto"]), ("Należności (niezapłacone) brutto", s_["naleznosci_brutto"]),
           ("w tym przeterminowane", s_["przeterminowane_brutto"]), ("Koszty (materiały, usługi, inne) netto", s_["koszty_netto"]),
           ("Koszty pracownicze", s_["robocizna"]), ("Koszty razem", s_["koszty_razem"]),
           ("Wynik bieżący (zafakturowano − koszty)", s_["wynik_biezacy"]), ("Wynik prognozowany (umowa − koszty dotąd ÷ postęp prac)", s_["wynik_prognoza"] if s_["wynik_prognoza"] is not None else "brak danych do prognozy")]
    if ZR_:  # zamawiający: zobowiązania wobec wykonawcy i koszty zamówienia, bez „wyniku” wykonawcy
        poz = [("Wartość umowy netto", s_["wartosc_umowy_netto"]), ("Odebrano netto", s_["odebrano_netto"]),
               ("Pozostało do odbioru netto", max(0, s_["wartosc_umowy_netto"] - s_["odebrano_netto"])),
               ("Faktury wykonawcy netto", s_["zafakturowano_netto"]), ("Faktury wykonawcy brutto", s_["zafakturowano_brutto"]),
               ("Zapłacono wykonawcy brutto", s_["zaplacono_brutto"]), ("Do zapłaty brutto", s_["naleznosci_brutto"]),
               ("w tym po terminie", s_["przeterminowane_brutto"]), ("Inne koszty zamówienia netto", s_["koszty_netto"])]
    for i, (a, v) in enumerate(poz, 4):
        ws.cell(i, 1, a)
        ws.cell(i, 2, v).number_format = "#,##0.00"
    if not ZR_ and s_.get("prognoza_metoda"):  # H3-02: metoda prognozy wyniku
        ws.cell(len(poz) + 5, 1, s_["prognoza_metoda"]).font = Font(italic=True, size=9)
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 18

    def arkusz(tytul, kol, wiersze):
        a = wb.create_sheet(tytul)
        for i, (h, _) in enumerate(kol, 1):
            c = a.cell(1, i, h)
            c.font = b
            c.fill = nag
            a.column_dimensions[openpyxl.utils.get_column_letter(i)].width = max(12, len(h) + 4)
        for j_, w in enumerate(wiersze, 2):
            for i, (_, f) in enumerate(kol, 1):
                v = f(w)
                a.cell(j_, i, v)
                if isinstance(v, float):
                    a.cell(j_, i).number_format = "#,##0.00"
    arkusz("Faktury", [("Numer", lambda f: f["numer"]), ("Data", lambda f: f["data"]), ("Termin", lambda f: f["termin"]),
                       ("Netto", lambda f: f["netto"]), ("VAT", lambda f: f["vat_kwota"]), ("Brutto", lambda f: f["brutto"]),
                       ("Zapłacona", lambda f: "TAK" if f.get("zaplacona") else "NIE"),
                       ("Data zapłaty", lambda f: f.get("data_zaplaty") or ""), ("Opis", lambda f: f.get("opis", ""))], r["faktury"])
    arkusz("Koszty", [("Data", lambda k: k["data"]), ("Kategoria", lambda k: k["kategoria"]), ("Opis", lambda k: k["opis"]),
                      ("Dostawca", lambda k: k.get("dostawca", "")), ("Dokument", lambda k: k.get("dokument", "")),
                      ("Netto", lambda k: k["netto"]), ("Zapłacony", lambda k: "TAK" if k.get("zaplacona") else "NIE")], r["koszty"])
    if not ZR_:
        arkusz("Robocizna", [("Data", lambda w: w["data"]), ("Pracownik", lambda w: w["imie"]), ("Godziny", lambda w: float(w["godziny"])),
                             ("Stawka", lambda w: float(w["stawka"])), ("Kwota", lambda w: float(w["kwota"])), ("Opis", lambda w: w.get("opis", ""))],
               robocizna_projektu(pid, m.get("nazwa")))
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"Rozliczenie_{MO.bezpieczna_nazwa(m.get('nazwa', 'budowa'))[:50]}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ============================================================ profil firmy

TYPY_DOK_FIRMY = {"certyfikat": "certyfikaty", "referencja": "referencje", "polisa": "polisy"}


def dane_firmy():
    d = czytaj(F_FIRMA, {"www": "", "certyfikaty": [], "referencje": [], "polisy": []})
    for k in ("certyfikaty", "referencje", "polisy"):
        d.setdefault(k, [])
    return d


def logo_konta():
    p = os.path.join(DIR_FIRMA, "logo.png")
    return p if os.path.isfile(p) else None


def ustaw_logo():
    MO.LOGO = logo_konta  # logo firmy bieżącego konta – odczytywane przy tworzeniu każdego dokumentu


ustaw_logo()


def _zapisz_plik_firmy(f, katalog, prefiks):
    os.makedirs(katalog, exist_ok=True)
    nazwa = f"{prefiks}_{secure_filename_pl(f.filename)}"
    f.save(os.path.join(katalog, nazwa))
    return nazwa


















# ============================================================ kadry (dokumenty i terminy pracowników)

TYPY_DOK_KADR = ["badania lekarskie", "szkolenie BHP", "uprawnienia budowlane", "uprawnienia SEP", "uprawnienia UDT",
                 "szkolenie wysokościowe", "prawo jazdy", "karta pobytu / zezwolenie na pracę", "inne"]
# H3-10: termin szkolenia okresowego BHP – rozporządzenie MGiP z 27.07.2004 w sprawie szkolenia w dziedzinie bhp (t.j. Dz.U. 2024 poz. 1327), § 15:
# ust. 1 – stanowiska robotnicze nie rzadziej niż raz na 3 lata, prace szczególnie niebezpieczne – raz w roku; ust. 2 – pracodawcy, kierujący
# pracownikami, inżynieryjno-techniczni, służba bhp i inni z § 14 ust. 2 pkt 6 – raz na 5 lat, administracyjno-biurowi – raz na 6 lat;
# ust. 4 – pierwsze szkolenie okresowe: kierujący pracownikami – do 6 miesięcy, pozostali – do 12 miesięcy od rozpoczęcia pracy na stanowisku.
GRUPY_BHP = {
    "robotnicze": ("stanowisko robotnicze – szkolenie okresowe co 3 lata (§ 15 ust. 1)", 36),
    "robotnicze_niebezpieczne": ("stanowisko robotnicze, prace szczególnie niebezpieczne – co 1 rok (§ 15 ust. 1)", 12),
    "kierujacy": ("pracodawca / osoba kierująca pracownikami (kierownik, mistrz, brygadzista) – co 5 lat (§ 15 ust. 2)", 60),
    "inzynieryjno": ("pracownik inżynieryjno-techniczny, służba bhp – co 5 lat (§ 15 ust. 2)", 60),
    "biurowe": ("stanowisko administracyjno-biurowe – co 6 lat (§ 15 ust. 2)", 72),
    "wstepne_kierujacy": ("szkolenie wstępne – kierujący pracownikami: pierwsze okresowe do 6 miesięcy (§ 15 ust. 4)", 6),
    "wstepne": ("szkolenie wstępne – pozostali: pierwsze okresowe do 12 miesięcy (§ 15 ust. 4)", 12),
}


def termin_bhp(wydano, grupa):
    """Termin następnego szkolenia BHP od daty szkolenia według grupy stanowisk (§ 15 rozporządzenia); 29.02 → 28.02. None – brak danych."""
    if grupa not in GRUPY_BHP:
        return None
    try:
        d = dt.date.fromisoformat(str(wydano)[:10])
    except (TypeError, ValueError):
        return None
    m = d.month - 1 + GRUPY_BHP[grupa][1]
    r, mi = d.year + m // 12, m % 12 + 1
    return dt.date(r, mi, min(d.day, calendar.monthrange(r, mi)[1]))












def alerty_terminow(dni=30, rola=None):
    """Kończące się i przeterminowane: dokumenty pracowników, umowy, certyfikaty i polisy firmy."""
    rd = rola_def(rola) if rola is not False else UPR.ROLE_WBUDOWANE["admin"]
    dzis = dt.date.today()
    wyn = []

    def dodaj(kat, opis, termin, widok):
        try:
            t = dt.date.fromisoformat(str(termin)[:10])
        except (TypeError, ValueError):
            return
        n = (t - dzis).days
        if n <= dni:
            wyn.append({"kategoria": kat, "opis": opis, "termin": t.isoformat(), "dni": n, "widok": widok})
    if UPR.poziom(rd, "kadry") >= 1 or UPR.poziom(rd, "pracownicy") >= 1:
        for p in (dane_prac() if rola is False else dane_prac_konta())["pracownicy"]:
            if p.get("archiwum"):
                continue
            for x in (p.get("kadry") or {}).get("dokumenty", []):
                if not x.get("archiwum") and x.get("wazne_do"):
                    dodaj("Kadry", f"{p['imie']}: {x.get('typ', '')}", x["wazne_do"], "kadry")
            if (p.get("umowa") or {}).get("do"):
                dodaj("Umowy", f"{p['imie']}: koniec umowy", p["umowa"]["do"], "kadry")
    if rola is not False:  # zamówienia: termin składania ofert za ≤ 5 dni – przypomnienie i możliwość zaproszenia wykonawców z okolicy
        login_ = session.get("login") if has_request_context() else None
        for pid_, m_ in projekty_ro():  # tylko do odczytu – bez kopiowania
            if not m_ or m_.get("typ") != "zamowienie" or m_.get("archiwum") or m_.get("status_projektu") == "realizacja" or m_.get("rodzic") \
                    or not RZ.reguly(projekt_wspolnoty(m_)).przypomnienia_ofert:  # przypomnienie i zaproszenia – reguła modułu (tylko wspólnota)
                continue
            if login_ and not ma_dostep(m_, login_, rola_sesji(), lista=True):
                continue
            t_ = ZP.termin_ofert(m_.get("kreator"))
            if t_ and 0 <= (t_ - dzis).days <= ZP.DNI_PRZYPOMNIENIA:
                oid_ = (m_.get("kreator") or {}).get("ocena_id")
                n_ = len((czytaj_ro(os.path.join(PROJ, oid_, "projekt.json"), {}) or {}).get("ocena", {}).get("oferty") or []) if oid_ else 0
                wyn.append({"kategoria": "Zamówienia", "opis": (f"Nikt nie złożył oferty: {m_.get('nazwa')} – zaprosić wykonawców z okolicy? (Moje zapytania)" if not n_
                            else f"Termin składania ofert: {m_.get('nazwa')} – ofert: {n_}"), "termin": t_.isoformat(), "dni": (t_ - dzis).days,
                            "widok": "zam_zapytania", "projekt": pid_, "wspolnota": True})
    if rola is not False and has_request_context() and wlasciciel():  # klucze AI są wspólne – zarządza nimi właściciel programu
        for z_ in MO.odrzucone_klucze(cfg()):  # nieważny klucz AI – program używa drugiego, ale warto wymienić
            wyn.append({"kategoria": "AI", "opis": f"Klucz API z „{z_}” odrzucony przez AI (nieważny) – program używa drugiego klucza. Wymień go i sprawdź „Test połączenia z AI”.",
                        "termin": dzis.isoformat(), "dni": 0, "widok": "ustawienia"})
    if rola is not False and has_request_context() and rola_sesji() == "admin" and UPR.poziom(rd, "kadry") >= 1:  # H1-10: RODO w kadrach
        n_ = T_BEZPIECZENSTWO.liczba_rodo() if "T_BEZPIECZENSTWO" in globals() else 0
        if n_:
            wyn.append({"kategoria": "Kadry", "opis": f"RODO: {n_} dok. pracowniczych po okresie przechowywania (art. 94 pkt 9b KP) – do trwałego usunięcia "
                        "(Kadry → Do trwałego usunięcia)", "termin": dzis.isoformat(), "dni": 0, "widok": "kadry"})
    if UPR.poziom(rd, "firma") >= 1:
        d = dane_firmy()
        for kl, nazwa in (("certyfikaty", "Certyfikat"), ("polisy", "Polisa OC")):
            for x in d[kl]:
                if not x.get("archiwum") and x.get("wazny_do"):
                    dodaj("Firma", f"{nazwa}: {x.get('nazwa', '')}", x["wazny_do"], "firma")
    return sorted(wyn, key=lambda x: x["dni"])


@app.get("/api/alerty")
@wymaga_logowania
def alerty():
    return jsonify(alerty_terminow())


@app.post("/api/ai/test")
@wymaga_logowania
@UWIERZ.tylko_wlasciciel
def ai_test():
    """Sprawdza klucze API (z Ustawień i z Rendera) krótkim zapytaniem."""
    c = cfg()
    wyn = MO.test_ai(c)
    pam = None
    if (request.json or {}).get("pamiec", True) and any(x.get("ok") for x in wyn):
        dziala = next(x for x in wyn if x.get("ok"))
        klucz = c.get("api_key_ustawienia") if dziala["zrodlo"] == "Ustawienia" else c.get("api_key_render")
        pam = MO.test_cache(c, (klucz or "").strip() or None)
    return jsonify({"wyniki": wyn, "model": c.get("model_oferty"), "pamiec": pam})


# ============================================================ pomoc: czat o obsłudze programu

_INSTR = {"znak": None, "tekst": ""}
WIDOKI_POMOCY = {"pulpit": "Przegląd", "przetargi": "Przetargi", "projekty": "Projekty z przetargów", "wyniki": "Wygrane i przegrane",
                 "wlasne": "Własne projekty", "kosztorys": "Kosztorysowanie", "kos_projekty": "Kosztorysy", "realizacja": "W realizacji",
                 "dos_realizacja": "Realizacja umów (dostawca)", "kalk_pracy": "Kalkulator kosztów pracy", "klienci": "Klienci", "hurtownie": "Hurtownie",
                 "pracownicy": "Pracownicy", "kadry": "Kadry", "place": "Płace", "firma": "Profil firmy", "archiwum": "Archiwum",
                 "ustawienia": "Ustawienia", "instrukcja": "Instrukcja", "zam_nowe": "Nowe zamówienie", "zam_projekty": "Projekty zamówień",
                 "zam_oferty": "Sprawdzenie ofert", "plan_zam": "Roczny plan zamówień", "plan_spr": "Roczny plan zamówień / Sprawozdania do UZP", "zam_realizacja": "Realizacja umów (zamawiający)", "sprawozdanie": "Sprawozdanie roczne do UZP",
                 "olioc": "Ochrona ludności", "inw_projekty": "Mój dom – projekt i kosztorys", "inw_budowa": "Budowa (inwestor)",
                 "dot_szukaj": "Wyszukaj dotację", "dot_wnioski": "Uzyskaj dotację", "dot_projekty": "Rozliczanie dotacji", "nier": "Nieruchomości",
                 "pr_sprawy": "Sprawy prawnika", "pr_oferty": "Sprawdzenia ofert (prawnik)", "konta": "Konta i aktywność"}


def tekst_instrukcji():
    p = os.path.join(app.static_folder, "instrukcja.html")
    try:
        st = os.stat(p)
    except OSError:
        return ""
    if _INSTR["znak"] != st.st_mtime_ns:
        with open(p, encoding="utf-8") as f:
            h = f.read()
        h = re.sub(r'src="data:[^"]+"', "", h)
        h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
        h = re.sub(r"</(p|li|h1|h2|h3|tr|div)>", "\n", h)
        t = re.sub(r"<[^>]+>", " ", h)
        t = re.sub(r"[ \t]+", " ", html_unescape(t))
        _INSTR.update(znak=st.st_mtime_ns, tekst=re.sub(r"\n\s*\n+", "\n", t).strip()[:200000])  # pełna instrukcja (ok. 155 tys. znaków) – bez ucinania ostatnich rozdziałów
    return _INSTR["tekst"]


def html_unescape(t):
    import html as _h
    return _h.unescape(t)


@app.post("/api/pomoc")
@wymaga_logowania
def pomoc():
    j = request.json or {}
    pyt = str(j.get("pytanie", "")).strip()[:800]
    if len(pyt) < 3:
        return jsonify({"blad": "Wpisz pytanie."}), 400
    c = cfg()
    if not c.get("api_key"):
        return jsonify({"blad": "Brak klucza API – administrator musi go wpisać w Ustawieniach."}), 400
    system = [{"type": "text", "text": (
        "Jesteś pomocnikiem w programie „Bidivia” (przetargi, oferty, kosztorysy, realizacja umów, zamówienia, dotacje, nieruchomości, prawnik). Odpowiadasz krótko "
        "po polsku, konkretnymi krokami (1., 2., 3.) z nazwami przycisków i zakładek dokładnie jak w programie – WYŁĄCZNIE na podstawie "
        "instrukcji poniżej. Jeśli czegoś nie ma w instrukcji, powiedz to wprost. Na końcu, jeśli pasuje, dodaj znacznik "
        "[[przejdz:KLUCZ]] z jednym kluczem z listy: " + ", ".join(f"{k} ({v})" for k, v in WIDOKI_POMOCY.items()) +
        ".\n\nINSTRUKCJA PROGRAMU:\n" + tekst_instrukcji())}]
    cc = MO.ustawienie_cache(c) and {"type": "ephemeral", "ttl": "1h"}
    if cc:
        system[0]["cache_control"] = cc  # instrukcja jest stała – kolejne pytania czytają ją z pamięci podręcznej
    kontekst = f"Użytkownik jest teraz w module: {WIDOKI_POMOCY.get(j.get('widok'), j.get('widok') or 'nieznany')}. Rola: {rola_def().get('nazwa')}."
    h_ = j.get("historia") if isinstance(j.get("historia"), list) else []  # inny typ (słownik, liczba) – bez historii, nie błąd 500
    h_ = h_[-6:] if len(h_) % 2 == 0 else h_[-5:]  # pary pytanie–odpowiedź: historia zawsze zaczyna się od pytania użytkownika
    hist = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(x)[:1500]} for i, x in enumerate(h_)]
    if hist and hist[-1]["role"] == "user":
        hist = hist[:-1]
    zap = {"model": c.get("model_lekki") or "claude-haiku-5-5", "max_tokens": 900, "system": system,
           "messages": hist + [{"role": "user", "content": f"{kontekst}\nPytanie: {pyt}"}]}
    try:
        odp = CR._post(c, zap)
    except Exception as e:
        if cc and "cache" in str(e).lower():
            system[0].pop("cache_control", None)
            odp = CR._post(c, zap)
        else:
            return jsonify({"blad": f"Pomoc chwilowo niedostępna ({str(e)[:120]})."}), 502
    tekst = "".join(b.get("text", "") for b in odp.get("content", []) if b.get("type") == "text")
    m = re.search(r"\[\[przejdz:([a-z_]+)\]\]", tekst)
    tekst = re.sub(r"\[\[przejdz:[a-z_]+\]\]", "", tekst).strip()
    return jsonify({"odpowiedz": tekst, "przejdz": m.group(1) if m and m.group(1) in WIDOKI_POMOCY else None,
                    "przejdz_nazwa": WIDOKI_POMOCY.get(m.group(1)) if m else None})


# ============================================================ notatki i raport projektu

@app.post("/api/projekty/<pid>/notatki")
@wymaga_logowania
def notatki(pid):
    j = request.json or {}
    m = meta(pid)
    lista = m.setdefault("notatki", [])
    if j.get("id"):
        for x in lista:
            if x["id"] == j["id"]:
                if j.get("usun"):
                    x.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
                elif "przypiete" in j:
                    x["przypiete"] = bool(j["przypiete"])
    else:
        t = str(j.get("tekst", "")).strip()
        if not t:
            return jsonify({"blad": "Wpisz treść notatki."}), 400
        lista.append({"id": uuid.uuid4().hex[:10], "tekst": t[:3000], "kto": session.get("login", ""),
                      "czas": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    zapisz_meta(pid, m)
    return jsonify([x for x in lista if not x.get("archiwum")])


@app.get("/api/projekty/<pid>/raport.docx")
@wymaga_logowania
def raport_projektu(pid):
    import raport as RAP
    m = meta(pid)
    r = realizacja_dane(pid) if m.get("status_projektu") else None
    s_ = podsumowanie_realizacji(pid) if r else None
    dane_of = czytaj(os.path.join(pdir(pid), "oferta_dane.json"), None)
    p = os.path.join(pdir(pid), f"Raport_projektu_{MO.bezpieczna_nazwa(m.get('nazwa', 'projekt'))[:50]}.docx")
    if m.get("przetarg"):
        m["przetarg_dane"] = dane_przetargu(m, pid)
    c_ = cfg()
    if m.get("strona") == "zamawiajacy":
        c_ = dict(c_, firma_nazwa=zamawiajacy_projektu(m, (dane_of or {}).get("postepowanie") or {}))
    RAP.raport_docx(p, m, dane_of, r, s_, lista_plikow(pid), wyniki(pid), c_, moze("finanse"))
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


# ============================================================ archiwum (zamiast usuwania)



def _archiwum_akcja(j, trwale):
    rodzaj, i, pid = j.get("rodzaj"), j.get("id"), j.get("pid")
    if rodzaj == "projekt":
        m = meta(i)
        if not m.get("archiwum"):
            return "Projekt nie jest w archiwum."
        if trwale:
            shutil.rmtree(pdir(i), ignore_errors=True)
        else:
            for k in ("archiwum", "archiwum_data", "archiwum_kto"):
                m.pop(k, None)
            zapisz_meta(i, m)
    elif rodzaj == "plik":
        if str(i).startswith("zdj:"):
            r = realizacja_pelna(pid)
            z = next((x for x in r["zdjecia"] if x["id"] == i[4:]), None)
            if z and trwale:
                for n in (z.get("plik"), z.get("miniatura")):
                    if n and os.path.isfile(os.path.join(folder_zdjec(pid), n)):
                        os.remove(os.path.join(folder_zdjec(pid), n))
                r["zdjecia"].remove(z)
            elif z:
                z.pop("archiwum", None)
            zapisz_realizacje(pid, r)
            return None
        m = meta(pid)
        f = next((x for x in m.get("archiwum_plikow", []) if x["id"] == i), None)
        if not f:
            return "Nie ma takiego pliku w archiwum."
        src = os.path.join(pdir(pid), f["plik"])
        if trwale:
            if os.path.isfile(src):
                os.remove(src)
        else:
            cel = os.path.join(pdir(pid), f["oryginal"])
            os.makedirs(os.path.dirname(cel), exist_ok=True)
            if os.path.exists(cel):
                baza, ext = os.path.splitext(cel)
                cel = f"{baza}_przywrocony{ext}"
            shutil.move(src, cel)
        m["archiwum_plikow"] = [x for x in m.get("archiwum_plikow", []) if x["id"] != i]
        zapisz_meta(pid, m)
    elif rodzaj == "klient":
        with BLOKADA:
            lista = klienci_lista()
            if trwale:
                lista = [x for x in lista if x["id"] != i]
            for x in lista:
                if x["id"] == i:
                    for k in ("archiwum", "archiwum_data", "archiwum_kto"):
                        x.pop(k, None)
            pisz(F_KLIENCI, lista)
    elif rodzaj == "pracownik":
        with BLOKADA:
            d = dane_prac()
            if not moj_pracownik(d, i):
                return "Nie ma takiego pracownika na Twoim koncie."
            if trwale:
                d["pracownicy"] = [p for p in d["pracownicy"] if p["id"] != i]
            for p in d["pracownicy"]:
                if p["id"] == i:
                    for k in ("archiwum", "archiwum_data", "archiwum_kto"):
                        p.pop(k, None)
            pisz(F_PRAC, d)
    else:
        return "Nieznany rodzaj."
    return None






# ============================================================ klienci i dane po NIP

@app.get("/api/nip/<nr>")
@wymaga_logowania
def nip_szukaj(nr):
    with BLOKADA:
        cache = czytaj(F_NIP_CACHE, {})
    dane, blad = NIP.szukaj(nr, cache, ceidg_token=cfg_surowy().get("ceidg_token"))
    if blad:
        return jsonify({"blad": blad}), 400 if "Nieprawidłowy" in blad else 404
    with BLOKADA:
        pisz(F_NIP_CACHE, cache)
    return jsonify(dane)




def zapisz_klienta(k, login=""):
    """Dodaje albo aktualizuje klienta (po id, a gdy go brak – po NIP). Zwraca zapisany rekord."""
    with BLOKADA:
        lista = klienci_lista()
        nip_c = NIP.oczysc(k.get("nip"))
        # edycja – tylko klient o tym id (inny klient z tym samym NIP-em nie może zostać nadpisany); nowy – dopasowanie po NIP (bez dubli)
        ist = next((x for x in lista if x["id"] == k["id"]), None) if k.get("id") else \
            next((x for x in lista if nip_c and NIP.oczysc(x.get("nip")) == nip_c and not x.get("archiwum")), None)
        if k.get("id") and nip_c and any(x is not ist and not x.get("archiwum") and NIP.oczysc(x.get("nip")) == nip_c for x in lista):
            raise ValueError(f"Klient z NIP {k.get('nip')} jest już na liście – edytuj tamtą kartę zamiast powielać dane.")
        if not ist:
            ist = {"id": uuid.uuid4().hex[:10], "dodano": dt.date.today().isoformat(), "kto": login}
            lista.append(ist)
        for pole in ("nazwa", "adres", "nip", "regon", "krs", "status_vat", "osoba", "telefon", "email", "uwagi", "reprezentant"):
            if pole in k:
                ist[pole] = str(k.get(pole) or "")[:300]
        if "rachunki" in k:
            ist["rachunki"] = [str(x)[:40] for x in (k.get("rachunki") or [])][:5]
        if ist.get("nip") and NIP.poprawny(ist["nip"]):
            ist["nip"] = NIP.formatuj(ist["nip"])
        ist["zmieniono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        pisz(F_KLIENCI, sorted(lista, key=lambda x: x.get("nazwa", "").lower()))
    return ist








# ============================================================ płace: umowy, ZUS, podatek (tylko administrator)

OPCJE_UMOWY = ("pit2", "mlody", "student", "dojezdza", "chorobowe", "ppk", "inne_zatrudnienie", "autorskie")


def dane_place():
    d = czytaj(F_PLACE, {"parametry": {}, "listy": {}})
    d["parametry"] = {**PL.PARAMETRY_2026, **d.get("parametry", {})}
    return d


def listy_konta(d, login=None):
    """Zatwierdzone listy płac bieżącego konta ({miesiąc: lista}); dawne wspólne listy należą do administratora."""
    login = login or konto_biezace()
    konta = d.get("listy_konta") or {}
    if login == login_admina() and d.get("listy"):
        return {**d["listy"], **konta.get(login, {})}
    return dict(konta.get(login, {}))








def _lista_plac(miesiac, nadpisania=None):
    """Oblicza listę płac za miesiąc RRRR-MM. nadpisania: {id: brutto} – kwoty wpisane ręcznie."""
    d = dane_place()
    P = d["parametry"]
    listy = listy_konta(d)
    zapisana = listy.get(miesiac, {})
    zapis_brutto = {p["id"]: p["brutto"] for p in zapisana.get("pozycje", [])}
    nadpisania = {k: v for k, v in (nadpisania or {}).items() if v not in (None, "")}
    godziny = {}
    konto = dane_prac_konta()
    for w in konto["wpisy"]:
        if w["data"][:7] == miesiac:
            godziny[w["pracownik"]] = godziny.get(w["pracownik"], 0) + float(w["godziny"])
    pozycje = []
    for p in konto["pracownicy"]:
        u = p.get("umowa")
        if not u or p.get("archiwum"):
            continue
        typ = u["typ"]
        h = round(godziny.get(p["id"], 0), 2)
        if typ == "uop":
            domyslne = u["kwota"]
        elif typ == "zlecenie":
            domyslne = r = round(h * u["kwota"], 2)
        else:
            domyslne = 0.0
        if p["id"] in nadpisania:
            brutto = float(str(nadpisania[p["id"]]).replace(" ", "").replace(",", "."))
        elif p["id"] in zapis_brutto:
            brutto = zapis_brutto[p["id"]]
        else:
            brutto = domyslne
        wyn = PL.oblicz(typ, brutto, u.get("opcje"), P, PL.narastajaco(listy, p["id"], miesiac))
        if typ == "zlecenie" and u["kwota"] < P["minimalna_stawka_godz"]:
            wyn["uwagi"].append(f"stawka {u['kwota']:.2f} zł/h jest niższa od minimalnej ({P['minimalna_stawka_godz']:.2f} zł/h)".replace(".", ","))
        if typ == "uop" and brutto and float(u.get("etat") or 1) >= 1 and brutto < P["minimalne_wynagrodzenie"]:
            wyn["uwagi"].append("wynagrodzenie niższe od minimalnego dla pełnego etatu")
        pozycje.append({"id": p["id"], "imie": p["imie"], "stanowisko": p.get("stanowisko", ""), "brutto": brutto,
                        "domyslne": domyslne, "godziny": h, "stawka": u["kwota"], "wynik": wyn})
    return {"miesiac": miesiac, "pozycje": pozycje, "zapisana": bool(zapisana), "zapisano": zapisana.get("zapisano"),
            "parametry": P}






# ============================================================ budowa: zdjęcia, dziennik, usterki

def folder_zdjec(pid):
    return os.path.join(pdir(pid), "realizacja", "zdjecia")


def vat_realizacji(r):
    """Stawka VAT budowy z danych umowy; gdy nie wpisano – 23% wyłącznie do wyliczeń (w programie oznaczone „do ustalenia”)."""
    try:
        v = float(str(r.get("vat")).replace(",", "."))
        return v / 100 if v > 1 else v
    except (TypeError, ValueError):
        return MO.VAT_PODSTAWOWY




def bez_archiwum(r):
    r = dict(r)
    r["zdjecia"] = [z for z in r.get("zdjecia", []) if not z.get("archiwum")]
    return r






def wspolrzedne(pid, r):
    if r.get("wsp"):
        return r["wsp"]
    adres = r.get("adres") or ((meta(pid).get("oferta") or {}).get("obiekt")) or ""
    if not adres:
        return None
    for q in (adres, adres.split(",")[-1].strip()):
        try:
            w = REG.szukaj_miejscowosci(q)
        except Exception:
            w = []
        if w:
            r["wsp"] = {"lat": w[0]["lat"], "lon": w[0]["lon"]}
            zapisz_realizacje(pid, r)
            return r["wsp"]
    return None








STATUSY_USTEREK = ("otwarta", "w toku", "usunięta", "zamknięta")


@app.post("/api/projekty/<pid>/usterki")
@wymaga_logowania
def usterki_zapisz(pid):
    j = request.json
    with BLOKADA:
        r = realizacja_pelna(pid)
        if j.get("id"):
            u = next((x for x in r["usterki"] if x["id"] == j["id"]), None)
            if not u:
                return jsonify({"blad": "Nie ma takiej pozycji."}), 404
            if j.get("usun"):  # pozycja trafia do historii realizacji (zgłoszona usterka nie znika bez śladu)
                r["usterki"].remove(u)
                r.setdefault("usterki_archiwum", []).append(dict(u, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), archiwum_kto=session.get("login", "")))
                zapisz_realizacje(pid, r)
                return jsonify({"ok": True})
        else:
            if not str(j.get("tytul", "")).strip():
                return jsonify({"blad": "Wpisz, czego dotyczy usterka lub zadanie."}), 400
            u = {"id": uuid.uuid4().hex[:10], "zgloszono": dt.date.today().isoformat(), "kto": session.get("login", ""),
                 "status": "otwarta"}
            r["usterki"].append(u)
        if j.get("termin"):
            try:
                dt.date.fromisoformat(str(j["termin"]))
            except ValueError:
                return jsonify({"blad": "Nieprawidłowy termin (RRRR-MM-DD)."}), 400
        if "tytul" in j and not str(j.get("tytul") or "").strip():
            return jsonify({"blad": "Wpisz, czego dotyczy usterka lub zadanie."}), 400
        for k in ("typ", "tytul", "opis", "lokalizacja", "osoba", "termin", "zdjecie", "etap"):
            if k in j:
                u[k] = str(j[k] or "")[:1000]
        if j.get("status") in STATUSY_USTEREK:
            u["status"] = j["status"]
            if j["status"] in ("usunięta", "zamknięta"):
                u.setdefault("usunieto", dt.date.today().isoformat())
            else:
                u.pop("usunieto", None)
        u["typ"] = u.get("typ") if u.get("typ") in ("usterka", "zadanie") else "usterka"
        zapisz_realizacje(pid, r)
    return jsonify(u)


@app.get("/api/projekty/<pid>/usterki.docx")
@wymaga_logowania
def usterki_docx(pid):
    r = realizacja_pelna(pid)
    tylko_otwarte = request.args.get("otwarte") == "1"
    lista = [u for u in r["usterki"] if not tylko_otwarte or u.get("status") in ("otwarta", "w toku")]
    if not lista:
        abort(404)
    kat = os.path.join(pdir(pid), "realizacja")
    os.makedirs(kat, exist_ok=True)
    p = os.path.join(kat, f"Lista_usterek_{MO.bezpieczna_nazwa(meta(pid).get('nazwa', 'budowa'))[:50]}.docx")
    BUD.usterki_docx(p, meta(pid).get("nazwa", ""), r, lista, folder_zdjec(pid), cfg())
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


# ============================================================ decyzje (uczenie oceny) i powiadomienia

def zapisz_decyzje(nr, t, status, powod=""):
    with BLOKADA:
        dec = czytaj(F_DECYZJE, [])
        dec = [d_ for d_ in dec if d_.get("numer") != nr]
        dec.append({"numer": nr, "przedmiot": t.get("przedmiot", "")[:200], "zamawiajacy": t.get("zamawiajacy", "")[:120],
                    "lokalizacja": t.get("lokalizacja", "")[:80], "ocena_ai": t.get("ocena"), "decyzja": status,
                    "powod": str(powod or "")[:200], "data": dt.date.today().isoformat()})
        pisz(F_DECYZJE, dec[-300:])


def tekst_decyzji():
    dec = czytaj(F_DECYZJE, [])
    tak = [d_ for d_ in dec if d_["decyzja"] in ("startujemy", "oferta złożona", "wygrany")][-15:]
    nie = [d_ for d_ in dec if d_["decyzja"] in ("odpuszczamy",)][-15:]
    przeg = [d_ for d_ in dec if d_["decyzja"] == "przegrany"][-5:]
    if not (tak or nie):
        return ""
    lin = ["", "WCZEŚNIEJSZE DECYZJE FIRMY – ucz się z nich, oceniając podobne przetargi wyżej lub niżej:"]
    if tak:
        lin.append("Przetargi, w których startowaliśmy / które nas interesowały:")
        lin += [f"- {d_['przedmiot']} ({d_['zamawiajacy']}, {d_['lokalizacja']})" for d_ in tak]
    if nie:
        lin.append("Przetargi odrzucone:")
        lin += [f"- {d_['przedmiot']} ({d_['lokalizacja']})" + (f" – powód: {d_['powod']}" if d_.get("powod") else "") for d_ in nie]
    if przeg:
        lin.append("Przetargi przegrane (uwzględnij ryzyko):")
        lin += [f"- {d_['przedmiot']}" + (f" – {d_['powod']}" if d_.get("powod") else "") for d_ in przeg]
    return "\n".join(lin)


def raport_dzienny(c, wymus=False):
    """Buduje raport e-mail: nowe dobre przetargi, zbliżające się terminy, zaległości na budowach. Zwraca (temat, tekst, html) lub None."""
    stan = czytaj(F_POWIAD, {})
    od = stan.get("ostatni") or (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    prog = int(c.get("powiadomienia_min_ocena", 7) or 7)
    w_ob = sprawdzacz_obszaru(c)
    db = {nr: t for nr, t in db_przetargi().items() if w_ob(t)}  # raport tylko z wybranego obszaru
    nowe = sorted([dict(t, numer=nr) for nr, t in db.items() if (t.get("dodano") or "") > od and (t.get("ocena") or 0) >= prog],
                  key=lambda t: -(t.get("ocena") or 0))
    dzis = dt.date.today()
    granica = (dzis + dt.timedelta(days=5)).isoformat()
    terminy = sorted([dict(t, numer=nr) for nr, t in db.items() if t.get("status") in ("startujemy", "do analizy")
                      and dzis.isoformat() <= str(t.get("termin_ofert") or "")[:10] <= granica],
                     key=lambda t: str(t.get("termin_ofert")))
    zaleglosci = []
    for pid in os.listdir(PROJ):
        m = czytaj(os.path.join(PROJ, pid, "projekt.json"), None)
        if not m or m.get("status_projektu") != "realizacja" or m.get("archiwum") \
                or (m.get("wlasciciel") or login_admina()) != konto_biezace():  # raport tylko z budów tego konta
            continue
        r = czytaj(os.path.join(PROJ, pid, "realizacja.json"), {})
        for f in r.get("faktury", []):
            if not f.get("zaplacona") and f.get("termin", "9") < dzis.isoformat():
                zaleglosci.append(f"{m['nazwa']}: faktura {f['numer']} ({MO.zl(f['brutto'])}) – termin minął {f['termin']}")
        for u in r.get("usterki", []):
            if u.get("status") in ("otwarta", "w toku") and u.get("termin") and u["termin"] < dzis.isoformat():
                zaleglosci.append(f"{m['nazwa']}: {u.get('typ', 'usterka')} „{u.get('tytul', '')}” – termin minął {u['termin']}")
    kadry_term = [f"{a['opis']} – {'po terminie' if a['dni'] < 0 else 'ważne do'} {a['termin']}" for a in alerty_terminow(30, False)]
    if not (nowe or terminy or zaleglosci or kadry_term) and not wymus:
        return None
    e = lambda x: str(x or "").replace("&", "&amp;").replace("<", "&lt;")
    lin, htm = [], ["<div style='font-family:Arial;font-size:14px'>"]
    lin.append(f"Raport programu Bidivia – {dzis:%d.%m.%Y}")
    htm.append(f"<h2 style='color:#1e3a8a'>Raport programu Bidivia – {dzis:%d.%m.%Y}</h2>")
    for tytul, lista, fmt in (
            (f"Nowe przetargi z oceną {prog}+ ({len(nowe)})", nowe,
             lambda t: f"[{t.get('ocena')}/10] {t.get('przedmiot')} – {t.get('zamawiajacy')}, {t.get('lokalizacja')}; termin: {str(t.get('termin_ofert'))[:16]}"),
            (f"Terminy składania ofert w ciągu 5 dni ({len(terminy)})", terminy,
             lambda t: f"{str(t.get('termin_ofert'))[:16]} – {t.get('przedmiot')} ({t.get('status')})"),
            (f"Zaległości na budowach ({len(zaleglosci)})", zaleglosci, lambda x: x),
            (f"Kończące się dokumenty, umowy, certyfikaty i polisy OC – 30 dni ({len(kadry_term)})", kadry_term, lambda x: x)):
        lin += ["", tytul] + [" • " + fmt(x) for x in lista[:25]] + ([" (brak)"] if not lista else [])
        htm.append(f"<h3 style='color:#16a34a'>{e(tytul)}</h3><ul>" + "".join(
            f"<li>{e(fmt(x))}" + (f" – <a href='{e(x.get('link'))}'>ogłoszenie</a>" if isinstance(x, dict) and x.get("link") else "") + "</li>"
            for x in lista[:25]) + ("<li>brak</li>" if not lista else "") + "</ul>")
    htm.append("<p style='color:#64748b;font-size:12px'>Wiadomość wysłana automatycznie przez program Bidivia.</p></div>")
    return (f"Bidivia – raport {dzis:%d.%m.%Y}: {len(nowe)} nowych, {len(terminy)} terminów", "\n".join(lin), "".join(htm))


def wyslij_raport(log, wymus=False):
    c = cfg()
    adresy = [a.strip() for a in re.split(r"[,;\s]+", c.get("powiadomienia_adresy", "") or "") if "@" in a]
    if not adresy:
        raise ValueError("Wpisz adresy e-mail do powiadomień w Ustawieniach.")
    if not c.get("smtp_serwer"):
        raise ValueError("Skonfiguruj pocztę SMTP w Ustawieniach (sekcja Poczta).")
    rap = raport_dzienny(c, wymus)
    if not rap:
        log("Brak nowych informacji – raportu nie wysłano.")
        return {"wyslano": False}
    temat, tekst, htm = rap
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = temat, c.get("smtp_nadawca") or c.get("smtp_login"), ", ".join(adresy)
    msg.set_content(tekst)
    msg.add_alternative(htm, subtype="html")
    MH.wyslij_smtp(c, [msg])
    pisz(F_POWIAD, {**czytaj(F_POWIAD, {}), "ostatni": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    log(f"Wysłano raport do: {', '.join(adresy)}")
    return {"wyslano": True}


@app.post("/api/powiadomienia/test")
@wymaga_logowania
def powiadomienia_test():
    return jsonify(uruchom("raport", "Raport e-mail", lambda log: wyslij_raport(log, wymus=True)))


def praca_szukaj_i_raport(log, tryb="wykonawca"):
    c = cfg()
    wyn = praca_szukaj(log, (c.get("slowa_kluczowe_dostawy") or SLOWA_DOSTAWY) if tryb == "dostawca" else None, tryb)
    if cfg().get("powiadomienia"):
        try:
            wyslij_raport(log)
        except Exception as e:
            log(f"Raport e-mail: {e}")
    return wyn


# ============================================================ automatyczne wyszukiwanie

def harmonogram_automatu():
    PELNA = EDYCJA == "pelna"  # edycja zamawiającego: bez pobierania ogłoszeń, wyszukiwania przetargów, naborów i alertów dotacji
    godz = int(os.environ.get("AUTO_SZUKAJ_GODZINA", "7"))
    if godz < 0:
        return
    ostatnio, ostatni_pomiar, ostatni_harm, ostatnie_alerty, ostatnie_wyniki = None, None, None, None, None
    godz_noc = int(os.environ.get("POBIERANIE_GODZINA", "1"))

    def czekaj_na(zad):  # konta po kolei – jedno wyszukiwanie naraz (mniej pamięci serwera)
        for _ in range(900):
            if (ZADANIA.get(zad.get("id")) or {}).get("status") != "trwa":
                return
            time.sleep(2)
    time.sleep(90)
    while True:
        teraz = dt.datetime.now(STREFA) if STREFA else dt.datetime.now()
        # 01:00 – wspólne pobranie ogłoszeń (także nadrobienie po restarcie serwera, jeśli dziś jeszcze nie pobrano)
        if PELNA and teraz.hour >= godz_noc and WSP.stan().get("ostatnie_pobranie") != teraz.date().isoformat() and not NOC_BLOKADA.locked():
            _KONTEKST.login = None
            try:
                z = uruchom("pobieranie", "Pobieranie ogłoszeń (BZP, TED, Baza Konkurencyjności)", praca_pobierz_ogloszenia)
                czekaj_na(z)
            except ZadanieTrwa:
                pass
        if PELNA and teraz.weekday() < 5 and teraz.hour == godz and ostatnio != teraz.date():
            ostatnio = teraz.date()
            for login in wszystkie_konta():  # każde konto (firma) ma własny obszar, słowa kluczowe i raport – po kolei
                _KONTEKST.login = login
                c_ = cfg()
                if c_.get("auto_szukaj", True) and ((c_.get("obszar") or {}).get("tryb") or c_.get("miejscowosci")):
                    try:
                        czekaj_na(uruchom("szukaj", "Automatyczne wyszukiwanie", praca_szukaj_i_raport))
                    except ZadanieTrwa:
                        pass
                if c_.get("powiadamiaj_dostawca") and ((c_.get("obszar") or {}).get("tryb") or c_.get("miejscowosci")):
                    try:
                        czekaj_na(uruchom("szukaj", "Automatyczne wyszukiwanie – dostawy i usługi", praca_szukaj_i_raport, "dostawca"))
                    except ZadanieTrwa:
                        pass
            _KONTEKST.login = None
        if PELNA and teraz.weekday() == 0 and teraz.hour == 6 and ostatni_harm != teraz.date():  # harmonogramy naborów – raz w tygodniu
            ostatni_harm = teraz.date()
            try:
                praca_odswiez_harmonogramy(print)
            except Exception as e:
                print("Harmonogramy naborów:", e, flush=True)
        if PELNA and teraz.hour in (7, 14) and globals().get("_ODW_OSTATNIO") != (teraz.date(), teraz.hour) \
                and os.path.exists(os.path.join(DATA, "odwolania_przetargow", "postepowania.json")):  # odwołania od przetargów – 2× dziennie
            globals()["_ODW_OSTATNIO"] = (teraz.date(), teraz.hour)
            _KONTEKST.login = login_admina()
            try:
                praca_odw_sprawdz(lambda *_: None)
            except Exception as e:
                logging.warning("Odwołania od przetargów: %s", e)
        if PELNA and teraz.hour == 9 and ostatnie_wyniki != teraz.date():  # wyniki złożonych ofert – codziennie
            ostatnie_wyniki = teraz.date()
            for login_ in wszystkie_konta():
                _KONTEKST.login = login_
                try:
                    if any((x.get("wynik") or {}).get("status") == "oczekuje" for x in (czytaj(F_WYNIKI_OFERT, {}) or {}).values()):
                        praca_sprawdz_wyniki(lambda *_: None)
                except Exception as e:
                    print("Wyniki ofert:", login_, e, flush=True)
                finally:
                    _KONTEKST.login = None
        if PELNA and teraz.hour == 7 and teraz.minute >= 30 and ostatnie_alerty != teraz.date():  # alerty dotacji – codziennie
            ostatnie_alerty = teraz.date()
            sprawdz_alerty_dotacji()
        if teraz.hour >= 9 and globals().get("_OPAD_DOB_OSTATNIO") != teraz.date():  # oficjalny opad dobowy IMGW za poprzednią dobę
            globals()["_OPAD_DOB_OSTATNIO"] = teraz.date()
            zbieraj_opad_dobowy()
        if teraz.hour >= 10 and globals().get("_ARCH_IMGW_OSTATNIO") != teraz.date():  # archiwum miesięczne IMGW (po publikacji)
            globals()["_ARCH_IMGW_OSTATNIO"] = teraz.date()
            threading.Thread(target=uzupelnij_archiwum_meteo, daemon=True).start()
        if globals().get("_METEO_OSTATNIO") != (teraz.date(), teraz.hour, teraz.minute // 10):  # sieć telemetryczna IMGW – co 10 minut
            globals()["_METEO_OSTATNIO"] = (teraz.date(), teraz.hour, teraz.minute // 10)
            zbieraj_meteo()
        if teraz.hour in (8, 11, 14, 17) and ostatni_pomiar != (teraz.date(), teraz.hour):
            ostatni_pomiar = (teraz.date(), teraz.hour)
            zbieraj_pomiary_pogody()
        time.sleep(60)


if os.environ.get("AGENT_BEZ_AUTOMATU") != "1":
    threading.Thread(target=harmonogram_automatu, daemon=True).start()
    threading.Thread(target=wznow_zadania_po_starcie, daemon=True).start()
    threading.Thread(target=podtrzymuj_serwer, daemon=True).start()



# ================================================================ KSIĘGOWOŚĆ (prototyp – tylko administrator; dane osobno dla każdego konta)
def _op():
    """Wspólne dane modułu (administrator i osoby z uprawnieniem „Odwołania od przetargów”), niezależne od podglądu „jako”."""
    return OP.Baza(os.path.join(DATA, "odwolania_przetargow"))


KONCOWE_ODW = ("poniżej progu wartości", "jedna oferta", "unieważnione", "termin odwołania minął", "umowa zawarta – po terminie odwołania", "ukryty", "zakończono obserwację")
KOLEJNOSC_ODW = {"możliwy do podważenia": 0, "do sprawdzenia": 1, "czeka na wybór oferty": 2, "czeka na informację z otwarcia ofert": 3,
                 "obserwowany": 4, "bez zarzutów z danych publicznych": 5, "termin odwołania minął": 6, "jedna oferta": 7,
                 "poniżej progu wartości": 8, "unieważnione": 9, "zakończono obserwację": 9, "ukryty": 10}




def kontakt_firmy(nip, K=None, log=None, nazwa=""):
    """Dane firmy z rejestrów i strony www: biała lista VAT (+ CEIDG z tokenem), KRS (www, e-mail, e-Doręczenia), kontakt ze strony firmy.
    K – słownik pamięci (kontakty.json); wynik zapamiętywany na 30 dni (limit wykazu VAT: 100 zapytań dziennie). Zwraca (dane, czy_nowe)."""
    n = NIP.oczysc(nip)
    if not NIP.poprawny(n):
        return None, False
    K = K if K is not None else {}
    k = K.get(n)
    if k and (dt.date.today() - dt.date.fromisoformat(k.get("czas", "2000-01-01")[:10])).days <= 30:
        return k, False
    dane = wykaz(n, czekaj=True) or {}
    kr = OP.krs_kontakt(dane.get("krs")) if dane.get("krs") else {}
    www = kr.get("www") or dane.get("www") or ""
    strona = OP.kontakt_ze_strony(www) if www else {}
    k = {"czas": dt.datetime.now().isoformat(timespec="minutes"), "nazwa": dane.get("nazwa_rejestr") or dane.get("nazwa"), "adres": dane.get("adres"),
         "status_vat": dane.get("status_vat"), "krs": dane.get("krs"), "regon": dane.get("regon"), "reprezentanci": dane.get("reprezentanci") or [],
         "www": www, "email": kr.get("email") or dane.get("email") or "", "telefon": dane.get("telefon") or "", "ade": kr.get("ade") or "",
         "emaile_strona": strona.get("emaile") or [], "telefony_strona": strona.get("telefony") or []}
    K[n] = k
    if log:
        log(f"   dane firmy: {nazwa[:50]} (NIP {n})")
    return k, True


















def zbieraj_rozstrzygniecia(log=None, dni=21):
    """Ogłoszenia o wyniku (BZP, wszystkie województwa) i o udzieleniu zamówienia (TED) z ostatnich dni – do pamięci wyników
    (ta sama co raport „kto wygrywa w powiatach”). Pobierane są tylko brakujące dni; ostatnie 3 dni – ponownie (publikacje z opóźnieniem)."""
    os.makedirs(KAT_WYNIKI_DNI, exist_ok=True)
    dzis = dt.date.today()
    ile = 0
    for i in range(1, dni + 1):
        d = dzis - dt.timedelta(days=i)
        swieze = d >= dzis - dt.timedelta(days=3)
        for kod in WOJEWODZTWA.values():
            plik = os.path.join(KAT_WYNIKI_DNI, f"{kod}_{d.isoformat()}_v3.json")
            if os.path.exists(plik) and not swieze:
                continue
            try:
                dz, kompletne = HZ.pobierz_wyniki_dnia(d, kod)
            except Exception as e:
                if log:
                    log(f"Rozstrzygnięcia BZP {d} ({kod}): {e}")
                continue
            if kompletne:
                pisz(plik, dz)
                ile += len(dz)
        plik = os.path.join(KAT_WYNIKI_DNI, f"TED_{d.isoformat()}.json")
        if not os.path.exists(plik) or swieze:
            try:
                dz = LD.ted_wyniki_dnia(d.isoformat())
                pisz(plik, dz)
                ile += len(dz)
            except Exception as e:
                if log:
                    log(f"Rozstrzygnięcia TED {d}: {e}")
    if log:
        log(f"Rozstrzygnięcia (BZP, TED): zapisano {ile} pozycji z ostatnich {dni} dni.")
    return ile






_WADIUM_STAN = {"trwa": False, "dzien": None, "zrobione": 0}


def uzupelnij_wadium_w_pamieci(dni=45):
    """Jednorazowo: ogłoszenia BZP zapisane w pamięci przed wersją z leadami nie mają danych o wadium (sekcja 6.4 była poza skróconą treścią).
    Pobiera te dni ponownie z BZP i dopisuje wadium i zabezpieczenie (pamięć scala zmiany)."""
    _WADIUM_STAN.update(trwa=True, zrobione=0)
    try:
        granica = (dt.date.today() - dt.timedelta(days=dni)).isoformat()
        for d in WSP.dni_bzp():
            if d < granica:
                break
            D = WSP.dzien(d)
            brak = [nr for nr, o in D.items() if o.get("zrodlo") != "TED" and not nr.startswith("TED ") and "wadium_wymagane" not in o]
            if not brak:
                continue
            try:
                dzien = dt.date.fromisoformat(d)
                pelne = {o.get("numer"): o for o in (BZ.normalizuj(x) for x in BZ._pobierz_okres(dzien, dzien, lambda *a: None)[0])}
            except Exception as e:
                logging.warning("Uzupełnianie wadium %s: %s", d, e)
                continue
            zm = {}
            for nr in brak:
                o = pelne.get(nr)
                if not o:
                    continue
                w_, kw_, _ = LD.wadium_z_tresci(o.get("tresc"))
                zm[nr] = dict(D[nr], wadium_wymagane=w_, wadium=kw_, znwu=LD.znwu_z_tresci(o.get("tresc")), znwu_proc=LD.znwu_procent(o.get("tresc")))
            if zm:
                WSP.zapisz_dzien(d, zm)
                _WADIUM_STAN["zrobione"] += len(zm)
    finally:
        _WADIUM_STAN.update(trwa=False, dzien=dt.date.today().isoformat())


_ROZSTRZ_STAN = {"trwa": False, "dzien": None}


def _rozstrzygniecia_w_pamieci(dni=14):
    """Ile dni z ostatnich `dni` ma w pamięci rozstrzygnięcia BZP (dowolne województwo) – do decyzji o zebraniu w tle."""
    dzis = dt.date.today()
    try:
        pliki = set(os.listdir(KAT_WYNIKI_DNI))
    except OSError:
        return 0
    return sum(1 for i in range(1, dni + 1) if any(f.endswith(f"_{(dzis - dt.timedelta(days=i)).isoformat()}_v3.json") for f in pliki))


def _zbierz_rozstrzygniecia_w_tle():
    try:
        zbieraj_rozstrzygniecia(None, 21)
    finally:
        _ROZSTRZ_STAN.update(trwa=False, dzien=dt.date.today().isoformat())








# ================================================================ OCHRONA LUDNOŚCI (gmina) i ROCZNE SPRAWOZDANIE DO UZP
def projekty_konta():
    """Projekty widoczne dla bieżącego konta (te same zasady co lista projektów), bez archiwum."""
    login, rola = session.get("login"), rola_sesji()
    for pid in os.listdir(PROJ):
        m = czytaj(os.path.join(PROJ, pid, "projekt.json"), None)
        if m and ma_dostep(m, login, rola, lista=True) and not m.get("archiwum") and projekt_w_edycji(m):
            yield m


def _plik_konta(nazwa):
    return os.path.join(katalog_konta(), nazwa)














def _dane_zamawiajacego():
    c = cfg()
    return {"nazwa": c.get("firma_nazwa") or "", "adres": c.get("firma_adres") or "", "nip": c.get("firma_nip") or "", "regon": c.get("firma_regon") or "",
            "email": c.get("firma_email") or "", "osoba": c.get("firma_osoba") or "", "rodzaj": "", "www": ""}


def _rok_spr(v):
    try:
        r = int(v)
        return r if 2021 <= r <= 2100 else None
    except (TypeError, ValueError):
        return None










# ================================================================ ROCZNY PLAN ZAMÓWIEŃ (art. 23 Pzp)
def _pz_plik(login=None):
    return os.path.join(katalog_konta(login), "plan_zamowien.json")


def _pz_plany(login=None):
    return czytaj(_pz_plik(login), {}) or {}


def _pz_plan(rok, P=None):
    P = _pz_plany() if P is None else P
    return P.setdefault("plany", {}).setdefault(str(rok), PZ.nowy_plan(rok))


def _pz_zapisz(P):
    os.makedirs(os.path.dirname(_pz_plik()), exist_ok=True)
    pisz(_pz_plik(), P)


def _pz_odpowiedz(rok):
    with BLOKADA:
        P = _pz_plany()
        plan = _pz_plan(rok, P)
        zm = False
        for p_ in plan["pozycje"]:  # postępowanie uruchomione z pozycji – status „wszczęte”
            if p_.get("projekt_id") and p_.get("status") == "zaplanowane" and os.path.exists(os.path.join(PROJ, p_["projekt_id"], "projekt.json")):
                p_["status"], zm = "wszczęte", True
        if zm:
            _pz_zapisz(P)
    return {"plan": {k: v for k, v in plan.items() if k != "wersje"}, "wersje": [{k: v for k, v in w.items() if k != "pozycje"} for w in plan.get("wersje") or []],
            "kategorie": {p_["id"]: PZ.kategoria(p_, plan) for p_ in plan["pozycje"]}, "podsumowanie": PZ.podsumowanie(plan),
            "kontrole": PZ.kontrole(plan), "zmiany": PZ.zmiany_od_publikacji(plan), "lata": sorted((P.get("plany") or {}).keys()),
            "listy": {"rodzaje": PZ.RODZAJE, "tryby_kraj": PZ.TRYBY_KRAJ, "tryby_ue": PZ.TRYBY_UE, "rodzaje_zamawiajacego": PZ.RODZAJE_ZAMAWIAJACEGO,
                      "info": PZ.INFO_DODATKOWE, "statusy": PZ.STATUSY, "miesiace": PZ.MIESIACE}}


def _pz_rok(v):
    r = int(RY._f(v) or (dt.date.today().year + (1 if dt.date.today().month >= 10 else 0)))
    if not 2020 <= r <= 2100:
        raise ValueError
    return r














def praca_plan_z_budzetu(log, plik, nazwa, dane, rok):
    """Propozycje pozycji planu z uchwały budżetowej / planu finansowego (AI) – dopisywane jako „zaplanowane” do sprawdzenia."""
    c = cfg()
    tekst = HN.tekst_pliku(nazwa, dane)[:120000]
    if not tekst.strip():
        raise ValueError("Nie udało się odczytać tekstu dokumentu (skan bez warstwy tekstowej?).")
    log(f"Czytam dokument budżetu: {nazwa} ({len(tekst)} znaków)…")
    w = ai_dane(c, PZ.SYSTEM_BUDZET, f"Rok planu: {rok}\n\n{tekst}", 12000, log, MO.wyciagnij_json, "Tylko najważniejsze zadania, maksymalnie 60.")
    with BLOKADA:
        P = czytaj(plik, {}) or {}
        plan = P.setdefault("plany", {}).setdefault(str(rok), PZ.nowy_plan(rok))
        nowe = PZ.pozycje_z_ai(w, plan)
        plan["pozycje"] += nowe
        pisz(plik, P)
    log(f"Gotowe: {len(nowe)} propozycji pozycji – sprawdź przedmiot, rodzaj, wartość i termin.")












# ================================================================ WINDYKACJA (właściciel + konta, którym ją udostępniono)
def _wn_plik():
    return os.path.join(katalog_konta(), "windykacja.json")


def _wn_stan():
    st = czytaj(_wn_plik(), None) or WK.pusty_stan()
    for k, v in WK.pusty_stan().items():
        st.setdefault(k, v)
    st["ustawienia"] = dict(WK.pusty_stan()["ustawienia"], **(st.get("ustawienia") or {}))
    if not st["ustawienia"].get("nadawca"):
        c = cfg()
        st["ustawienia"]["nadawca"] = ", ".join(x for x in (c.get("firma_nazwa"), c.get("firma_adres"), ("NIP " + c["firma_nip"]) if c.get("firma_nip") else "") if x)
    return st


def _wn_zapisz(st):
    os.makedirs(os.path.dirname(_wn_plik()), exist_ok=True)
    pisz(_wn_plik(), st)


def _ksef_fernet():
    """Ten sam klucz co w Księgowości – token zapisany tam da się odczytać tutaj (i odwrotnie)."""
    from cryptography.fernet import Fernet
    import base64 as _b64
    import hashlib as _hl
    return Fernet(_b64.urlsafe_b64encode(_hl.sha256(("bidivia-ksef|" + str(app.secret_key)).encode()).digest()))


def _wn_ksef_dane(st, kat=None):
    """Token KSeF dla windykacji: własny (wgrany w module) albo z Księgowości tego konta. Zwraca (token, źródło, nip, środowisko)."""
    kat = kat or katalog_konta()
    w = st.get("ksef") or {}
    dk = czytaj(os.path.join(kat, "ksiegowosc", "dane.json"), None) or {}
    ks = dk.get("ksef") or {}
    nip = re.sub(r"\D", "", str(w.get("nip") or "")) or re.sub(r"\D", "", str((dk.get("profil") or {}).get("nip") or ""))
    if not nip and has_request_context():
        nip = re.sub(r"\D", "", str(cfg().get("firma_nip") or ""))
    for zrodlo, sz, srod in (("wlasny", w.get("token"), w.get("srodowisko")), ("ksiegowosc", ks.get("token"), ks.get("srodowisko"))):
        if sz:
            try:
                return _ksef_fernet().decrypt(sz.encode()).decode(), zrodlo, nip, (srod or "produkcja")
            except Exception:
                continue
    return None, "", nip, (w.get("srodowisko") or "produkcja")


def _wn_odpowiedz(st=None):
    st = st or _wn_stan()
    rek = WK.rekompensaty(st)
    akcje = WK.akcje_do_zrobienia(st)
    nast = {a["faktura"]: a for a in akcje}
    F = []
    for f in sorted(st["faktury"], key=lambda f: (f["status"] != "otwarta", f["termin"] or "9999")):
        F.append(dict(f, stan=WK.stan_faktury(f), rekompensata=rek.get(f["id"]), nastepna=nast.get(f["id"])))
    tok, zr, nip, srod = _wn_ksef_dane(st)
    w = st.get("ksef") or {}
    return {"faktury": F, "akcje": akcje, "pulpit": WK.pulpit(st), "ustawienia": st["ustawienia"], "kontrahenci": st["kontrahenci"],
            "wplaty_nieprzypisane": [w_ for w_ in st["wplaty"] if not w_.get("faktura")][-100:], "statusy": WK.STATUSY, "akcje_opis": WK.AKCJE,
            "ksef": {"zrodlo": zr, "nip": nip, "srodowisko": srod, "wlasny": bool(w.get("token")), "pobrano_do": w.get("pobrano_do") or "",
                     "ostatnia": w.get("ostatnia") or "", "zostalo": w.get("zostalo") or 0, "srodowiska": list(KS_MOD.KSEF_ADRESY)}}














def _wn_dodaj(st, nowe):
    """Dopisuje faktury bez duplikatów (ten sam numer i NIP / kontrahent albo numer KSeF)."""
    znane = {(WK._norm(f["numer"]), f["nip"] or WK._norm(f["kontrahent"])) for f in st["faktury"]} | {f["ksef_nr"] for f in st["faktury"] if f["ksef_nr"]}
    ile = 0
    for f in nowe:
        if (f["ksef_nr"] and f["ksef_nr"] in znane) or (WK._norm(f["numer"]), f["nip"] or WK._norm(f["kontrahent"])) in znane:
            continue
        f["leczniczy"] = bool((st["kontrahenci"].get(f["nip"] or f["kontrahent"].lower()[:60]) or {}).get("leczniczy"))
        st["faktury"].append(f)
        ile += 1
    return ile
















# ---------------------------------------------------------------- E-SĄD: pozew w elektronicznym postępowaniu upominawczym


def _esad_ustawienia(st, z_peselem=False):
    e = st.get("esad") or {}
    sk = dict(e.get("skladajacy") or {})
    pesel = ""
    if sk.get("pesel_enc"):
        try:
            pesel = _ksef_fernet().decrypt(sk["pesel_enc"].encode()).decode()
        except Exception:
            pesel = ""
    sk.pop("pesel_enc", None)
    sk["pesel"] = pesel if z_peselem else ("•••••••" + pesel[-4:] if pesel else "")
    u = st.get("ustawienia") or {}
    c = cfg() if has_request_context() else {}
    pw = dict(e.get("powod") or {})
    pw.setdefault("nazwa", c.get("firma_nazwa") or "")
    pw.setdefault("nip", re.sub(r"\D", "", str(c.get("firma_nip") or "")))
    pw.setdefault("rodzaj", "1")
    if not pw.get("adres"):
        pw["adres"] = WK.parsuj_adres(c.get("firma_adres") or "")
    rach = re.sub(r"\D", "", str(u.get("rachunek") or ""))[-26:]
    return sk, pw, rach


def _esad_pozwany(st, klucz):
    k = (st.get("kontrahenci") or {}).get(klucz) or {}
    if k.get("pozwany"):
        return k["pozwany"]
    f = next((x for x in st["faktury"] if (x["nip"] or x["kontrahent"].lower()[:60]) == klucz), None) or {}
    p = {"rodzaj": "2", "nazwa": f.get("kontrahent") or "", "nip": f.get("nip") or "", "krs": "", "regon": "", "siedziba": "", "imie": "", "nazwisko": "",
         "adres": {"ulica": "", "nr_domu": "", "nr_mieszkania": "", "kod": "", "miejscowosc": ""}}
    if NIP.poprawny(NIP.oczysc(p["nip"])):
        d = wykaz(NIP.oczysc(p["nip"]), czekaj=True) or {}
        p["nazwa"] = d.get("nazwa_rejestr") or d.get("nazwa") or p["nazwa"]
        p["krs"] = re.sub(r"\D", "", str(d.get("krs") or ""))
        p["regon"] = re.sub(r"\D", "", str(d.get("regon") or ""))[:9]
        p["adres"] = WK.parsuj_adres(d.get("adres") or "")
        p["siedziba"] = p["adres"].get("miejscowosc") or ""
        p["rodzaj"] = ("3" if re.search(r"(?i)spółka (jawna|komandytowa|partnerska)|sp\. ?j\.|sp\. ?k\.", p["nazwa"]) else "2") if p["krs"] else "1"
    return p


def _esad_kontrola(dane, sk, pw, pz, rach):
    U = list(dane["uwagi"])
    blad = lambda t: U.append({"waga": "blad", "opis": t})
    if not re.fullmatch(r"\d{11}", sk.get("pesel") or ""):
        blad("Uzupełnij PESEL osoby składającej pozew (wymagany do konta w e-sądzie i w pozwie).")
    for n, o in (("osoby składającej", sk), ("powoda", pw), ("pozwanego", pz)):
        a = o.get("adres") or {}
        if not (a.get("ulica") and a.get("nr_domu") and re.fullmatch(r"\d{2}-?\d{3}", str(a.get("kod") or "")) and a.get("miejscowosc")):
            blad(f"Uzupełnij adres {n} (ulica, numer, kod pocztowy, miejscowość).")
    for n, o in (("powoda", pw), ("pozwanego", pz)):
        if o.get("rodzaj") in ("0", "1") and not (o.get("imie") and o.get("nazwisko")):
            blad(f"Uzupełnij imię i nazwisko {n} (osoba fizyczna / jednoosobowa działalność).")
        if o.get("rodzaj") in ("2", "3") and not o.get("nazwa"):
            blad(f"Uzupełnij nazwę {n}.")
    if not (sk.get("imie") and sk.get("nazwisko")):
        blad("Uzupełnij imię i nazwisko osoby składającej pozew.")
    if len(rach) != 26:
        blad("Uzupełnij numer rachunku (26 cyfr) w Ustawieniach Windykacji – do zapłaty i zwrotu opłat.")
    return U








def _esad_przygotuj(klucz, skap):
    st = _wn_stan()
    dane = WK.pozew_dane(st, klucz, odsetki_skapitalizowane=skap)
    sk, pw, rach = _esad_ustawienia(st, True)
    pz = _esad_pozwany(st, klucz)
    k = (st.get("kontrahenci") or {}).get(klucz) or {}
    uz = k.get("uzasadnienie") or WK.uzasadnienie_domyslne(dane, pw.get("nazwa"), st["faktury"])
    return st, dane, sk, pw, rach, pz, uz


































# ================================================================ KSIĘGOWOŚĆ – moduł (ksiegowosc.py + ksiegowosc_web.py), dane w katalogu konta / ksiegowosc / dane.json
import ksiegowosc_web  # noqa: E402
ksiegowosc_web.zarejestruj(globals())




def migracja_wyszukiwania():
    """Ogólne słowa dostawcy („dostaw”, „zakup”, „usług”…) i domyślne frazy „zawsze pasujące” (powiat świdnicki…) usunięte z kont."""
    stare_frazy = {"powiat świdnicki", "gmina świdnica", "starostwo powiatowe w świdnicy"}
    for login in wszystkie_konta():
        _KONTEKST.login = login
        try:
            zm = {}
            sd = cfg().get("slowa_kluczowe_dostawy") or []
            if sd and any(x in OGOLNE_SLOWA_DOSTAWY for x in sd):
                zm["slowa_kluczowe_dostawy"] = [x for x in sd if x not in OGOLNE_SLOWA_DOSTAWY]
            fz = cfg().get("frazy_zawsze") or []
            if set(fz) & stare_frazy:
                zm["frazy_zawsze"] = [x for x in fz if x not in stare_frazy]
            if zm:
                zapisz_ustawienia(zm)
        except Exception as e:
            print("Migracja wyszukiwania:", login, e, flush=True)
    _KONTEKST.login = None


try:
    migracja_wyszukiwania()
except Exception as _e:
    print("Migracja wyszukiwania:", _e, flush=True)


try:  # rodzaj zamówienia z BZP dla przetargów zapisanych przed tą wersją
    migracja_rodzaju()
except Exception as _e:
    print("Migracja rodzaju zamówienia:", _e, flush=True)


# Edycja urzędu („Bidivia – Zamawiający”): rejestrowane są tylko blueprinty ścieżki zamawiającego publicznego – trasy innych modułów
# (wspólnoty, przetargi wykonawcy, dotacje, nieruchomości, prawnik, moduły właściciela) w tej instalacji nie istnieją (404).
# Blokada adresów w blokada_edycji() zostaje jako druga warstwa.
BLUEPRINTY_EDYCJI = {"zamawiajacy": {"kreator", "ocena", "finansowanie", "zamawiajacy_publiczny", "realizacja", "administracja", "firma",
                                     "projekty_wykonawcy", "bezpieczenstwo"}}


def _rejestruj_blueprint(bp):
    if EDYCJA in BLUEPRINTY_EDYCJI and bp.name not in BLUEPRINTY_EDYCJI[EDYCJA]:
        return
    app.register_blueprint(bp)


# ============================================================ blueprinty (etap 2 podziału serwer.py) – na końcu pliku: moduły tras
# pobierają nazwy serwera w chwili wywołania (import serwer as S), więc serwer musi być już w całości wczytany.
if __name__ == "__main__":  # uruchomienie „python serwer.py”: blueprinty mają widzieć ten sam moduł, nie drugą kopię
    import sys as _sys
    _sys.modules.setdefault("serwer", _sys.modules[__name__])

import trasy_wspolnota as T_WSP  # noqa: E402  wspólnoty, spółdzielnie, deweloperzy
from trasy_wspolnota import F_ZAPR_REZYGNACJE, _rezygnacje, _zrezygnowal, praca_zaproszenia  # noqa: E402,F401  używane w kreatorze i testach

_rejestruj_blueprint(T_WSP.bp)
import trasy_finansowanie as T_FINANSOWANIE  # noqa: E402
from trasy_finansowanie import ( _fin, _fin_stan, fin_odczyt, fin_pliki, fin_pobierz, fin_porownanie, fin_raport, fin_zrodlo,
    praca_fin_odczyt, praca_fin_porownanie,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_FINANSOWANIE.bp)
import trasy_ocena as T_OCENA  # noqa: E402
from trasy_ocena import ( _wer_dane_wyk, _wer_przelicz, ocena_dane, ocena_dokument, ocena_kryteria, ocena_lista, ocena_oferta, ocena_plik,
    ocena_pobierz, ocena_potwierdzenie, ocena_prawnik, ocena_referencja, ocena_referencja_zapytanie, ocena_rynkowosc, ocena_sprawdz,
    ocena_swz, ocena_wartosc, ocena_weryfikacja, praca_ocena_ofert, praca_ocena_swz, praca_weryfikacja_oferty,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_OCENA.bp)
import trasy_kreator as T_KREATOR  # noqa: E402
from trasy_kreator import ( _elementy_stan, _kreator_stan, _kz_pusty, _kz_ustaw, _kz_wartosc, _netto_zam, _netto_zam_zrodlo,
    _ocena_zamowienia, _zwyciezcy_czesci, kreator_czesci_propozycja, kreator_czesci_realizacja, kreator_decyzje, kreator_dokumenty,
    kreator_element, kreator_element_wzor, kreator_nowy, kreator_ocena, kreator_pobierz, kreator_przeglad, kreator_sprzecznosc,
    kreator_umowa, kreator_uwagi_docx, kreator_wprowadz, kreator_wzor_z_biblioteki, kreator_wzory, kreator_wzory_usun, kreator_zapisz,
    kreator_zip, kreator_zrodla, kreator_zrodla_ponownie, praca_kreator_czesci, praca_kreator_import, praca_kreator_przeglad,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_KREATOR.bp)
import trasy_nieruchomosci as T_NIERUCHOMOSC  # noqa: E402
from trasy_nieruchomosci import ( _nier_bloki, _nier_dodaj_transakcje, _nier_przelicz_pow, _nier_stan, _nier_zastosuj_plan, nier_czynsze,
    nier_dokumenty, nier_dzialka, nier_identyfikuj, nier_kosztowe, nier_lista, nier_metoda, nier_nowa, nier_oblicz, nier_odpowiedz,
    nier_operat, nier_orientacyjna, nier_pismo, nier_pismo_zmien, nier_plan, nier_plan_link, nier_plan_plik, nier_plan_wybierz,
    nier_pobierz, nier_poszerz, nier_przywroc, nier_punkt, nier_raport, nier_rozpoznanie, nier_segment, nier_transakcje, nier_ustawienia,
    nier_ustawienia_zapisz, nier_wl_linki, nier_wl_oceny, nier_wl_szukaj, nier_wl_zapisz, nier_wycena_nowa, nier_zapisz, nier_zdjecia,
    praca_nier_czynsze, praca_nier_dokumenty, praca_nier_odpowiedz, praca_nier_operat, praca_nier_orientacyjna, praca_nier_plan,
    praca_nier_plan_dok, praca_nier_plan_link, praca_nier_rozpoznanie, praca_nier_transakcje_ai,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_NIERUCHOMOSC.bp)
import trasy_windykacja as T_WINDYKACJA  # noqa: E402
from trasy_windykacja import ( praca_wind_ksef, wind_akcja, wind_esad, wind_esad_akceptuj, wind_esad_podglad, wind_esad_pozwany,
    wind_esad_ustawienia, wind_esad_zlozony, wind_faktura, wind_faktura_usun, wind_import_plik, wind_kontrahent, wind_ksef_pobierz,
    wind_ksef_token, wind_plik, wind_stan, wind_status, wind_ustawienia, wind_wplata_przypisz, wind_wyciag, wind_zaplata,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_WINDYKACJA.bp)
import trasy_odwolania as T_ODWOLANIA  # noqa: E402
from trasy_odwolania import ( _odw_czesc, _odw_dokumenty_platformy, _odw_filtr, _odw_firma, _odw_jedno, _odw_kontakty, _odw_uzupelnij_woj,
    odw_badanie, odw_dodaj, odw_dokument, odw_email, odw_plik, odw_sprawdz, odw_stan, odw_ukryj, odw_ustawienia, praca_odw_odwolanie,
    praca_odw_sprawdz,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_ODWOLANIA.bp)
import trasy_zamawiajacy as T_ZAMAWIAJACY_  # noqa: E402
from trasy_zamawiajacy import ( _olioc, _owu_stan, _sprawozdania, kalkulator_pracy, kalkulator_pracy_plik, kalkulator_pracy_word,
    olioc_powiaz, olioc_raport, olioc_stan, olioc_zapisz, owu_dowod, owu_lista, owu_pobierz, owu_word, owu_zapisz, planz_budzet,
    planz_import, planz_kopiuj, planz_opublikuj, planz_plik, planz_pobierz, planz_powiaz, planz_pozycja, planz_przypomnienia,
    planz_ustawienia, planz_usun, sprawozdanie_import, sprawozdanie_stan, sprawozdanie_xlsx, sprawozdanie_zapisz, szacowanie_ceny,
    szacowanie_plik, szacowanie_zapisz, szacowanie_zapytanie,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_ZAMAWIAJACY_.bp)
import trasy_dotacje as T_DOTACJE  # noqa: E402
from trasy_dotacje import ( _dot, _dotacja, _dotacja_info, _zapytanie_stan, dot_dane_impl, dot_komplet_impl, dot_plik_impl,
    dot_plik_usun_impl, dot_stan_impl, dotacje_alerty, dotacje_alerty_zapisz, dotacje_harmonogram, dotacje_harmonogram_odswiez,
    dotacje_harmonogram_zrodla, dotacje_nowy_wniosek, dotacje_szukaj, dotacje_wyniki, dotacje_z_linku, praca_dot_analiza,
    praca_dot_przygotuj, praca_dot_sprawdz, praca_dotacja_analiza, praca_dotacja_przygotuj, praca_dotacja_sprawdz,
    praca_zapytanie_dokumenty, so_dane, so_oblicz, so_wspolczynniki, zapytanie_do_rozliczenia, zapytanie_dokumenty, zapytanie_ocena,
    zapytanie_plik, zapytanie_pobierz, zapytanie_protokol, zapytanie_zapisz,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_DOTACJE.bp)
import trasy_przetargi as T_PRZETARGI  # noqa: E402
from trasy_przetargi import ( bip_dodaj, bip_lista, bip_odkryj, bip_odkryj_obszar, bip_propozycje, bip_sprawdz, bip_zmien,
    historia_zamawiajacego_przetarg, historia_zamawiajacego_wynik, obszar_get, obszar_szukaj, obszar_zapisz, praca_bip_odkryj,
    praca_bip_odkryj_obszar, praca_bip_sprawdz, praca_bip_tylko, przetarg_analiza, przetarg_tekst_dokumentu, przetarg_termin, przetargi,
    przetargi_nowe, przetargi_ocen, przetargi_ostatnie, przetargi_slowa, przetargi_slowa_zapisz, przetargi_status, przetargi_szukaj,
    przetargi_usun, przetargi_widziane, raport_plik, raport_zwyciezcy, raporty_lista, raporty_usun,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_PRZETARGI.bp)
import trasy_realizacja as T_REALIZACJA  # noqa: E402
from trasy_realizacja import ( _wniosek, dostawy_dane, dostawy_dokument, dostawy_lista, dostawy_plik, dostawy_pobierz, dostawy_zapisz,
    dziennik_auto, dziennik_docx, dziennik_zapisz, faktura_dodaj, hrf_utworz, hrf_xlsx, hrf_zapisz, podwykonawcy_dokument,
    podwykonawcy_lista, podwykonawcy_plik, podwykonawcy_zadanie_status, podwykonawcy_zapisz, pogoda_budowy, pogoda_pismo, pogoda_przesun,
    pogoda_ustawienia, realizacja, realizacja_dane, realizacja_lista, realizacja_pelna, realizacja_pliki, realizacja_pliki_usun,
    realizacja_umowa, rozliczenie_mat, rozliczenie_mat_dokumenty, rozliczenie_mat_import, rozliczenie_mat_zalacznik, rozliczenie_mat_zapisz,
    wniosek_dokument, wniosek_kosztorys, wniosek_kosztorys_dane, wniosek_kosztorys_edycja, wniosek_kosztorys_wlasny, wniosek_nowy,
    wniosek_propozycja, wniosek_status, wniosek_zapisz,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_REALIZACJA.bp)
import trasy_firma as T_FIRMA  # noqa: E402
from trasy_firma import ( klienci_lista,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_FIRMA.bp)
import trasy_admin as T_ADMINISTRACJ  # noqa: E402
from trasy_admin import ( ustawienia_pogody,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_ADMINISTRACJ.bp)
import trasy_projekty_wykonawcy as T_PROJEKTY_WYK  # noqa: E402
from trasy_projekty_wykonawcy import ( _pliki_do_przegladu, hurtownie_wybrane, pliki_budowy, pliki_dok, pliki_oferty, pliki_wykonawcy,
    pliki_z_html, praca_analiza_dostawcy, praca_czat, praca_kontrola, praca_weryfikacja,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_PROJEKTY_WYK.bp)
import trasy_prawnik as T_PRAWNIK  # noqa: E402
from trasy_prawnik import ( praca_prawnik_oferty,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_PRAWNIK.bp)
import trasy_leady as T_LEADY  # noqa: E402
from trasy_leady import ( _leady,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_LEADY.bp)
import trasy_bk as T_BAZA_KONKURE  # noqa: E402
from trasy_bk import ( _bk_szczeg, _bk_zamawiajacy, bk_dane_ogloszenia, bk_tekst_pdf, bk_wynik_ai, bk_wynik_ogloszenia,
    bk_wyniki_zamawiajacego,)  # noqa: E402,F401  ponowny eksport (serwer, testy)
_rejestruj_blueprint(T_BAZA_KONKURE.bp)
import trasy_bezpieczenstwo as T_BEZPIECZENSTWO  # noqa: E402  hasła, przedmiar bez cen, RODO w kadrach, godziny na budowie, migracje h81
_rejestruj_blueprint(T_BEZPIECZENSTWO.bp)
try:
    T_BEZPIECZENSTWO.migracja_h81()
except Exception as _e:
    print("Migracja h81:", _e, flush=True)


if __name__ == "__main__":  # na końcu – po definicjach i migracjach (wcześniej blok był w środku pliku i migracje się nie wykonywały)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=False, threaded=True)
