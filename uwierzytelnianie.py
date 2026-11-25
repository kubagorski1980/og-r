# -*- coding: utf-8 -*-
"""
Logowanie i uprawnienia Bidivii (rdzeń, etap 1c podziału serwer.py): hasła, konta i role, poziomy dostępu do modułów,
dostęp do projektów (ma_dostep), dziennik aktywności, dekoratory tras (wymaga_logowania, tylko_admin).
Zależy od warstwy danych (dane.py) i modułu uprawnień (uprawnienia.py). Funkcje rejestrowane w aplikacji (@app.before_request)
zostają w serwerze.
"""
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from functools import wraps

from flask import abort, g, has_request_context, jsonify, redirect, request, session

import uprawnienia as UPR
from dane import (BLOKADA, F_AKTYWNOSC, F_CFG, F_ROLE, F_UZYT, czytaj, konto_admina, konto_biezace)

PROBY = {}  # ip -> [czasy nieudanych prób]


def hash_hasla(haslo, sol=None, iteracje=390000):
    sol = sol or secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", haslo.encode(), sol.encode(), iteracje).hex()
    return f"pbkdf2_sha256${iteracje}${sol}${h}"


def sprawdz_haslo(haslo):
    haslo = haslo.strip()
    zapisany = os.environ.get("APP_PASSWORD_HASH", "").strip()
    if zapisany.startswith("pbkdf2_sha256$"):
        _, it, sol, h = zapisany.split("$")
        return hmac.compare_digest(hash_hasla(haslo, sol, int(it)).split("$")[3], h)
    jawne = os.environ.get("APP_PASSWORD", "").strip()
    return bool(jawne) and hmac.compare_digest(haslo.encode(), jawne.encode())


def uzytkownicy_lista():
    return czytaj(F_UZYT, [])


def _marka():
    ust = czytaj(F_CFG, {}) or {}
    k = str(ust.get("marka_kolor") or "").strip()
    return {"nazwa": str(ust.get("marka_nazwa") or "").strip()[:60], "kolor": k if re.fullmatch(r"#[0-9a-fA-F]{6}", k) else ""}


def ma_ksiegowosc(login=None):
    """Moduł Księgowość: administrator zawsze; pozostałe konta – gdy administrator udostępnił moduł (przełącznik w „Kontach i aktywności”).
    Dane każdego konta osobno (katalog konta / ksiegowosc / dane.json)."""
    if login is None:
        return wlasciciel()  # tylko właściciel programu (w podglądzie „jako” – księgi klienta)
    return bool(login) and login == login_admina()


# ---------- ograniczenie konta do jednego modułu (np. tylko „Dla wspólnot”) – ustawia administrator w „Użytkownikach strony”
MODULY_KONTA = {"": "Wszystkie moduły", "wykonawca": "Dla wykonawcy (firma budowlana)", "dostawca": "Dla dostawcy i usługodawcy",
                "prawnik": "Dla prawnika", "gmina": "Dla zamawiającego publicznego (gmina, urząd, szkoła)",
                "wspolnota": "Dla wspólnot, spółdzielni i deweloperów", "inwestor": "Dla inwestora (budowa domu)",
                "kosztorysant": "Dla kosztorysanta", "dotacje": "Dotacje i dofinansowania", "nieruchomosci": "Nieruchomości"}


def modul_konta(login=None):
    """Moduł, do którego ograniczono konto („” – wszystkie). Właściciel programu (konto z instalacji) nie jest ograniczany."""
    if login is None:
        if not (has_request_context() and session.get("zalogowany")) or session.get("konto", "env") == "env":
            return ""
        login = session.get("login")
    if not login or login == login_admina():
        return ""
    u = next((x for x in uzytkownicy_lista() if x.get("login") == login), None)
    m = str((u or {}).get("modul") or "")
    return m if m in MODULY_KONTA else ""


def wszystkie_konta():
    return [login_admina()] + [u["login"] for u in uzytkownicy_lista() if u.get("login") != login_admina()]


# ---------- dziennik aktywności kont (dla administratora)
OPISY_AKCJI = [
    (r"^/api/projekty$", "POST", "Utworzono projekt"), (r"^/api/projekty/[^/]+$", "DELETE", "Przeniesiono projekt do archiwum"),
    (r"/oferta$", "POST", "Przygotowanie oferty / kosztorysu (AI)"), (r"/pliki$", "POST", "Dodano dokumenty"),
    (r"/pliki/usun$", "POST", "Dokumenty przeniesione do archiwum"), (r"/pobierz-dokumenty$", "POST", "Pobieranie dokumentów przetargu"),
    (r"/umowa$", "POST", "Umowa o roboty budowlane"), (r"/status$", "POST", "Zmiana statusu projektu"), (r"/dostosuj$", "POST", "Korekta ceny"),
    (r"/wnioski$", "POST", "Nowy wniosek o zmianę umowy"), (r"/wnioski/[^/]+/dokument$", "POST", "Wniosek o zmianę umowy (Word)"),
    (r"/wnioski/[^/]+/status$", "POST", "Status wniosku / aneks do umowy"), (r"/wnioski/[^/]+/propozycja$", "POST", "Propozycja wniosku (AI)"), (r"/wnioski/[^/]+/kosztorys", "POST", "Kosztorys do wniosku"),
    (r"/rozliczenie-mat/dokumenty$", "POST", "Rozliczenie materiałów – dokumenty"), (r"/podwykonawcy$", "POST", "Podwykonawcy – zapis"),
    (r"/podwykonawcy/dokument$", "POST", "Podwykonawcy – dokument"), (r"/dostawy$", "POST", "Realizacja umowy dostawy/usługi"),
    (r"/dostawy/dokument$", "POST", "Realizacja umowy – dokument"), (r"/podwykonawcy/plik$", "POST", "Podwykonawcy – plik"), (r"/rozliczenie-mat$", "POST", "Rozliczenie materiałów – zapis"),
    (r"/vat$", "POST", "Zmiana stawki VAT"), (r"/oferta-klienta$", "POST", "Oferta dla klienta (na podstawie kosztorysu)"), (r"/oferta-z-kosztorysu$", "POST", "Oferta na podstawie kosztorysu"), (r"/pozycje$", "POST", "Poprawki pozycji kosztorysu"), (r"/oferta-zlozona$", "POST", "Złożona oferta"), (r"/wynik-oferty$", "POST", "Wynik przetargu"),
    (r"/dotacja/analiza$", "POST", "Dotacja – analiza dokumentów"), (r"/dotacja/przygotuj$", "POST", "Dotacja – przygotowanie dokumentu"),
    (r"/dotacja/sprawdz$", "POST", "Dotacja – sprawdzenie dokumentów"), (r"/dotacja/komplet$", "POST", "Dotacja – komplet do złożenia"),
    (r"/dotacja/plik$", "POST", "Dotacja – wgranie dokumentu"), (r"^/api/dotacje/szukaj$", "POST", "Wyszukiwanie dotacji"),
    (r"^/api/dotacje/wniosek$", "POST", "Nowy wniosek o dotację"), (r"^/api/dotacje/alerty$", "POST", "Alert dotacji"),
    (r"^/api/dotacje/harmonogram/odswiez$", "POST", "Odświeżenie harmonogramów naborów"), (r"/wniosek-dot/(analiza|przygotuj|sprawdz|komplet)$", "POST", "Wniosek o dotację – działanie"),
    (r"^/api/cennik-wlasny$", "POST", "Własny cennik – wgranie"), (r"/kosztorys-pusty$", "POST", "Pusty kosztorys dla wykonawców"), (r"/kontrola", "POST", "Sprawdzenie kosztorysu"), (r"/czat$", "POST", "Pytanie do asystenta dokumentów"),
    (r"/weryfikacja", "POST", "Weryfikacja dokumentacji przetargowej"), (r"/dokumentacja$", "POST", "Sporządzanie dokumentacji przetargowej"),
    (r"/faktury", "POST", "Faktura"), (r"/koszty", "POST", "Koszt budowy"), (r"/dziennik", "POST", "Raport dzienny (dziennik pomocniczy)"),
    (r"/usterki", "POST", "Usterka / zadanie"), (r"/zdjecia", "POST", "Zdjęcia z budowy"), (r"/protokol", "POST", "Protokół odbioru"),
    (r"/hrf", "POST", "Harmonogram rzeczowo-finansowy"), (r"/notatki$", "POST", "Notatka"), (r"/materialy", "POST", "Zapotrzebowanie materiałowe"),
    (r"/harmonogram", "POST", "Harmonogram dostaw"), (r"/zamowienia", "POST", "Zamówienia do hurtowni"), (r"/komplet", "POST", "Komplet dokumentów do przetargu"),
    (r"/realizacja/umowa$", "POST", "Dane umowy budowy"), (r"^/api/przetargi/szukaj$", "POST", "Wyszukiwanie przetargów"),
    (r"^/api/przetargi/ocen$", "POST", "Ocena AI przetargów"), (r"^/api/przetargi/analiza$", "POST", "Pełna analiza przetargu"),
    (r"^/api/przetargi/status$", "POST", "Status przetargu"), (r"^/api/przetargi/usun$", "POST", "Usunięto przetargi z listy"),
    (r"^/api/obszar", "POST", "Obszar wyszukiwania"), (r"^/api/przetargi/slowa$", "POST", "Słowa kluczowe"), (r"^/api/bip", "POST", "Obserwowane BIP"),
    (r"^/api/klienci", "POST", "Klienci"), (r"^/api/hurtownie", "POST", "Hurtownie"), (r"^/api/pracownicy", "POST", "Pracownicy"),
    (r"^/api/godziny", "POST", "Godziny pracy"), (r"^/api/kadry", "POST", "Kadry"), (r"^/api/place", "POST", "Płace"),
    (r"^/api/firma", "POST", "Profil firmy"), (r"^/api/konto/ustawienia", "POST", "Ustawienia konta"), (r"^/api/ustawienia", "POST", "Ustawienia programu"),
    (r"^/api/uzytkownicy", "POST", "Użytkownicy"), (r"^/api/role", "POST", "Role"), (r"^/api/archiwum", "POST", "Archiwum"),
    (r"/pogoda/pismo$", "POST", "Pismo: warunki pogodowe / wniosek o przedłużenie terminu"), (r"/pogoda/przesun$", "POST", "Przesunięcie terminu (pogoda)"),
    (r"/pogoda/ustawienia$", "POST", "Monitoring pogody – ustawienia"),
    (r"^/api/pomoc$", "POST", "Pytanie do pomocy"), (r"^/pobierz/", "GET", "Pobrano plik"), (r"\.(docx|xlsx)$", "GET", "Pobrano raport / plik"),
]
_ile_wpisow = [0]


def zapisz_aktywnosc(login, akcja, szczegoly="", konto=None, projekt=""):
    wpis = {"czas": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "login": login, "konto": konto or login, "akcja": akcja,
            "szczegoly": str(szczegoly)[:200], "projekt": projekt}
    try:
        with BLOKADA:
            with open(F_AKTYWNOSC, "a", encoding="utf-8") as f:
                f.write(json.dumps(wpis, ensure_ascii=False) + "\n")
            _ile_wpisow[0] += 1
            if _ile_wpisow[0] % 500 == 0 and os.path.getsize(F_AKTYWNOSC) > 8_000_000:  # przycinanie dziennika
                with open(F_AKTYWNOSC, encoding="utf-8") as f:
                    linie = f.readlines()[-30000:]
                with open(F_AKTYWNOSC, "w", encoding="utf-8") as f:
                    f.writelines(linie)
    except OSError:
        pass


def rola_sesji():
    """Zwraca rolę zalogowanego (albo None, gdy sesja nieważna – np. konto usunięte lub zmienione hasło)."""
    if not session.get("zalogowany"):
        return None
    if session.get("konto", "env") == "env":
        return "admin"
    u = next((x for x in uzytkownicy_lista() if x["login"] == session.get("login")), None)
    if not u or u.get("wersja", 1) != session.get("wersja"):
        return None
    return u["rola"]


def role_firmy():
    return UPR.wszystkie_role(czytaj(F_ROLE, {}))


def rola_def(rola=None):
    rola = rola or rola_sesji()
    return role_firmy().get(rola) or (role_firmy()["podglad"] if rola else None)


def moze(modul, poziom_=1):
    return UPR.poziom(rola_def(), modul) >= poziom_


# ---------- rola „Tylko podgląd”: pełny tryb tylko do odczytu (decyzja właściciela produktu, WSP-07)
ROLA_PODGLAD = "podglad"
KOMUNIKAT_PODGLAD = "Rola „Tylko podgląd” nie może zmieniać danych."
# żądania POST dozwolone dla podglądu: wylogowanie/logowanie, odczyty wysyłane POST-em (pomoc, kalkulator kosztów pracy i jego wydruk Word)
# podgląd pozwu EPU (Word), lista płac bez zapisu i usuwania oraz zapamiętanie stanu widoku tego użytkownika (ostatnio wybrany tryb,
# przetarg oznaczony jako przejrzany) – nie są to dane firmy
PODGLAD_DOZWOLONE = re.compile(r"^/(login|logout)$|^/api/(pomoc|kalkulator-pracy|kalkulator-pracy/word|wind/esad/podglad|konto/tryb|przetargi/widziane|haslo/zmien)$")


def tylko_odczyt(rola=None):
    """Czy zalogowany ma rolę „Tylko podgląd” (także konto z rolą, której już nie ma – program traktuje je jak podgląd)."""
    rola = rola or rola_sesji()
    if not rola or rola == "admin":
        return False
    return rola == ROLA_PODGLAD or rola not in role_firmy()


def odmowa_podgladu():
    """Wspólna blokada (before_request w serwerze): rola „Tylko podgląd” dostaje 403 na każde żądanie zmieniające dane
    (POST/PUT/PATCH/DELETE), poza wyjątkami z PODGLAD_DOZWOLONE. Inne role – bez zmian."""
    if request.method in ("GET", "HEAD", "OPTIONS") or not session.get("zalogowany") or session.get("konto", "env") == "env":
        return None
    if PODGLAD_DOZWOLONE.match(request.path) or not tylko_odczyt():
        return None
    if request.path == "/api/place/lista":  # wyliczenie listy płac (odczyt) – zapis i usunięcie listy zablokowane
        j = request.get_json(silent=True) if request.is_json else None
        if isinstance(j, dict) and not j.get("zapisz") and not j.get("usun"):
            return None
    return jsonify({"blad": KOMUNIKAT_PODGLAD, "tylko_odczyt": True}), 403


def wymaga_logowania(f):
    @wraps(f)
    def w(*a, **k):
        rola = rola_sesji()
        if not rola:
            session.clear()
            if request.path.startswith("/api/") or request.path.startswith("/pobierz/"):
                return jsonify({"blad": "Sesja wygasła – zaloguj się ponownie."}), 401
            return redirect("/login")
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if request.headers.get("X-Agent") != "1":
                abort(403)  # ochrona przed żądaniami z obcych stron (CSRF): własny nagłówek wymusza zapytanie wstępne CORS, którego serwer nie przepuszcza
        if session.get("zmien_haslo") and request.path not in ZMIANA_HASLA_DOZWOLONE:
            # H1-07: logowanie hasłem tymczasowym (reset przez administratora) – najpierw nowe hasło, potem praca w programie
            if request.path.startswith("/api/") or request.path.startswith("/pobierz/"):
                return jsonify({"blad": "Najpierw zmień hasło tymczasowe.", "zmien_haslo": True}), 403
            return redirect("/zmien-haslo")
        odmowa = UPR.sprawdz(rola_def(rola), request.method, request.path, request.get_json(silent=True) if request.is_json else None)
        if odmowa:
            return jsonify({"blad": odmowa}), 403
        return f(*a, **k)
    return w


ZMIANA_HASLA_DOZWOLONE = ("/api/haslo/zmien", "/api/ja", "/zmien-haslo", "/logout")


def tylko_admin(f):
    """Administrator: właściciel programu albo administrator konta (firmy) – ten drugi działa tylko w obrębie swojej firmy (H1-01)."""
    @wraps(f)
    def w(*a, **k):
        if rola_sesji() != "admin":
            return jsonify({"blad": "Tę operację może wykonać tylko administrator."}), 403
        return f(*a, **k)
    return w


def tylko_wlasciciel(f):
    """Operacje na całym programie (wszystkie konta, ustawienia wspólne, klucze AI, pobieranie ogłoszeń) – tylko właściciel programu."""
    @wraps(f)
    def w(*a, **k):
        if not wlasciciel():
            return jsonify({"blad": "Tę operację może wykonać tylko właściciel programu."}), 403
        return f(*a, **k)
    return w


# ---------- firmy (H1-01): konto = firma; administrator konta zarządza tylko swoją firmą, właściciel programu – wszystkimi
def _uzytkownik(login):
    lg = str(login or "").lower()
    return next((x for x in uzytkownicy_lista() if str(x.get("login", "")).lower() == lg), None)


def firma_id(login):
    """Identyfikator firmy konta: właściciel programu i użytkownicy założeni przez niego – firma właściciela (login z instalacji);
    administrator konta – jego własny login; użytkownicy założeni przez administratora konta – login tego administratora."""
    adm = login_admina()
    if not login or str(login).lower() == adm.lower():
        return adm
    u = _uzytkownik(login)
    if not u:
        return str(login)
    f = str(u.get("firma") or "")
    if f:
        return f
    return u["login"] if u.get("rola") == "admin" else adm


def czlonkowie_firmy(login=None):
    """Loginy (małymi literami) należące do firmy danego konta – łącznie z nim samym."""
    login = login or session.get("login") or ""
    adm = login_admina()
    f = firma_id(login).lower()
    wyn = {f, str(login).lower()}
    for u in uzytkownicy_lista():  # firma_id bez ponownego czytania listy dla każdego użytkownika
        fu = str(u.get("firma") or "") or (u.get("login") if u.get("rola") == "admin" else adm)
        if str(fu).lower() == f:
            wyn.add(str(u.get("login", "")).lower())
    return wyn


def admin_firmy():
    """Administrator konta (rola „Administrator” nadana przez właściciela) – nie właściciel programu."""
    return rola_sesji() == "admin" and not wlasciciel()


def wlasciciel():
    """Właściciel programu – konto z instalacji (APP_USER). Tylko on widzi Odwołania, Leady i Księgowość."""
    return has_request_context() and bool(session.get("zalogowany")) and session.get("konto", "env") == "env"


TYLKO_WLASCICIEL = ("/api/odw", "/api/leady", "/api/ksieg")


def ma_windykacje(login=None):
    """Windykacja: właściciel programu i konta, którym właściciel ją udostępnił (Konta i aktywność)."""
    if login is None:
        if wlasciciel():
            return True
        if not (has_request_context() and session.get("zalogowany")):
            return False
        login = session.get("login") or konto_biezace()
    if login == login_admina():
        return True
    u = next((x for x in uzytkownicy_lista() if x.get("login") == login), None)
    return bool(u and u.get("windykacja"))


def login_admina():
    return os.environ.get("APP_USER", "").strip()


def ma_dostep(m, login=None, rola=None, lista=False):
    """Właściciel programu ma dostęp do wszystkich projektów; na listach (lista=True) widzi projekty konta, na którym pracuje.
    Administrator konta (firmy) – projekty swojej firmy i udostępnione mu. Pozostali – swoje i udostępnione im (H1-01)."""
    rola = rola or rola_sesji()
    if rola == "admin" and has_request_context() and session.get("zalogowany") and not wlasciciel():  # administrator konta: tylko jego firma (dawniej – wszystkie firmy)
        login = (login or session.get("login") or "").lower()
        wl = (m.get("wlasciciel") or login_admina()).lower()
        if not login:
            return False
        if wl in czlonkowie_firmy(login):
            return True
        return login in [x.lower() for x in (m.get("dostep") or [])] and _udostepnienie_wazne(wl, login)
    if rola == "admin":
        if not lista:
            return True
        k = konto_biezace().lower()
        wl = (m.get("wlasciciel") or login_admina()).lower()
        if not session.get("jako") and konto_admina():  # administrator na swoim koncie: zakres wybrany w filtrze
            z = (session.get("admin_zakres") or "wszystkie").lower()
            return z == "wszystkie" or wl == z or (z == "moje" and wl == k) or (z == "moje" and k in [x.lower() for x in (m.get("dostep") or [])])
        return wl == k or k in [x.lower() for x in (m.get("dostep") or [])]
    login = (login or session.get("login") or "").lower()
    wl = (m.get("wlasciciel") or login_admina()).lower()
    # użytkownik widzi swoje projekty i te, które udostępnił mu administrator – właściciel programu albo administrator jego firmy
    return bool(login) and (wl == login or (login in [x.lower() for x in (m.get("dostep") or [])] and _udostepnienie_wazne(wl, login)))


def _udostepnienie_wazne(wl, login):
    """Udostępnienie działa, gdy projekt należy do właściciela programu albo do administratora firmy tego użytkownika."""
    if wl == login_admina().lower():
        return True
    u = _uzytkownik(wl)
    return bool(u) and u.get("rola") == "admin" and firma_id(wl).lower() == firma_id(login).lower()


def filtr_dostepu(dostep):
    """Lista udostępnień projektu widoczna dla zalogowanego: właściciel – cała, administrator konta – tylko osoby z jego firmy, inni – pusta."""
    if wlasciciel():
        return list(dostep or [])
    if rola_sesji() == "admin":
        cz = czlonkowie_firmy()
        return [x for x in (dostep or []) if str(x).lower() in cz]
    return []


def ukryj_innych(dane):
    """Dla użytkowników: loginy innych użytkowników (autorzy wpisów, notatek, zdjęć…) zastąpione opisem – nikt poza
    administratorem nie widzi, kto jeszcze korzysta z programu."""
    if wlasciciel():
        return dane
    ja, adm = session.get("login"), login_admina()
    swoi = czlonkowie_firmy() if rola_sesji() == "admin" else {str(ja or "").lower()}  # administrator konta widzi loginy swojej firmy

    def m(x):
        if isinstance(x, dict):
            return {k: (("administrator" if v == adm else "inny użytkownik") if k in ("kto", "autor", "archiwum_kto", "wlasciciel")
                        and isinstance(v, str) and v and v != ja and v.lower() not in swoi else m(v)) for k, v in x.items()}
        if isinstance(x, list):
            return [m(v) for v in x]
        return x
    return m(dane)


# ---------- sesja (H1-08): wygasa po 8 godzinach bezczynności, najdłużej po 14 dniach od zalogowania
BEZCZYNNOSC_S = 8 * 3600
MAKS_SESJA_S = 14 * 86400


def sesja_wygasla():
    """True, gdy sesja zalogowanego wygasła (bezczynność albo limit 14 dni). Odświeża znacznik ostatniej aktywności (co najwyżej raz na minutę,
    żeby nie wysyłać ciasteczka przy każdym żądaniu). Sesje sprzed tej wersji (bez znaczników) dostają je teraz – bez wylogowania."""
    if not session.get("zalogowany"):
        return False
    t = time.time()
    start, ost = session.get("start"), session.get("ostatnio")
    if not isinstance(start, (int, float)):
        session["start"] = start = t
    if not isinstance(ost, (int, float)):
        session["ostatnio"] = t
        return False
    if t - ost > BEZCZYNNOSC_S or t - start > MAKS_SESJA_S:
        return True
    if t - ost > 60:
        session["ostatnio"] = t
    return False


# ---------- role bez cen (H1-04): bez modułu Finanse i bez edycji Projektów (np. „Kierownik budowy”) – przedmiar bez cen
def bez_cen(rd=None):
    if wlasciciel():
        return False
    rd = rd or rola_def()
    return bool(rd) and UPR.poziom(rd, "finanse") < 1 and UPR.poziom(rd, "projekty") < 2
