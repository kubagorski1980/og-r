# -*- coding: utf-8 -*-
"""
Konfiguracja Bidivii (rdzeń, etap 1b podziału serwer.py): ustawienia programu i kont (globalne / konta), wartości domyślne,
zużycie i limity AI, dane firmy z wykazu podatników VAT (wykaz). Zależy tylko od warstwy danych (dane.py) i modułów narzędziowych.
"""
import datetime as dt
import json
import os
import re
import sys
import threading
import time
from importlib.machinery import SourceFileLoader

import modul_oferty as MO
import nip as NIP
from dane import (BLOKADA, DATA, F_CFG, F_NIP_CACHE, PROJ, SciezkaKonta, _KONTEKST, czytaj, katalog_konta, konto_admina, konto_biezace, pisz)

# moduł rdzenia aplikacji okienkowej – ta sama instancja co w serwerze (wczytany raz)
core = sys.modules.get("agent_core") or SourceFileLoader("agent_core", os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_przetargowy.pyw")).load_module()

DOMYSLNE_WEB = {"model": "claude-sonnet-5-5", "model_lekki": "claude-haiku-5-5", "model_oferty": "claude-sonnet-5-5", "model_dokladny": "claude-opus-5-5",
                "pdf_jako_tekst": True, "pomijaj_rysunki": True, "ocena_paczkami": True, "prog_pelnej_oceny": 6, "sito_prog": 2, "bk_limit_ai": 50, "firma_z_wykazu": True, "powiadomienia": False, "powiadomienia_adresy": "", "powiadomienia_min_ocena": 7, "cache_ai": "1h", "bip_w_wyszukiwaniu": True, "ceny_internet": True, "ceny_internet_pozycje": 15, "ceny_internet_udzial": 80, "ceny_internet_max": 90, "ceny_internet_materialy": 12,
                "ceny_internet_wyszukan": 10, "ceny_z_cennika": False,
                "obszar": {"tryb": "wojewodztwa", "wojewodztwa": ["dolnośląskie"]},
                "centrum_nazwa": "", "centrum_lat": 0, "centrum_lon": 0, "promien_km": 10, "miejscowosci": [],
                "frazy_zawsze": [], "wykluczenia": []}


GLOBALNE = {"marka_nazwa", "marka_kolor", "api_key", "model", "model_oferty", "model_lekki", "model_dokladny", "pdf_jako_tekst", "cache_ai", "ceidg_token", "bk_url", "bk_strony", "bk_dni", "dni_wstecz",
            "limity_ai", "pomijaj_rysunki"}  # wspólne dla programu


PRZYKLAD_OPISU_FIRMY = str(core.DEFAULT_CONFIG.get("profil_firmy") or "").strip()


def plik_ustawien_konta(login=None):
    login = login or konto_biezace()
    return F_CFG if konto_admina(login) else os.path.join(katalog_konta(login), "ustawienia.json")


def zapisz_ustawienia(zmiany, login=None):
    """Zapis ustawień: klucze wspólne programu – do ustawień globalnych, pozostałe (firma, wycena, obszar, poczta…) – do konta."""
    with BLOKADA:
        glob = czytaj(F_CFG, {})
        p = plik_ustawien_konta(login)
        if p == F_CFG:
            glob.update(zmiany)
            pisz(F_CFG, glob)
            return
        kont = czytaj(p, {})
        zmiana_glob = False
        for k, v in zmiany.items():
            if k in GLOBALNE:
                glob[k] = v
                zmiana_glob = True
            else:
                kont[k] = v
        pisz(p, kont)
        if zmiana_glob:
            pisz(F_CFG, glob)


def konto_zamawiajacego():
    """Edycja dla zamawiającego albo konto ograniczone do modułu zamawiającego (gmina, wspólnota)."""
    if (os.environ.get("BIDIVIA_EDYCJA") or "pelna").strip().lower() == "zamawiajacy":
        return True
    uw = sys.modules.get("uwierzytelnianie")
    try:
        return bool(uw) and uw.modul_konta() in ("gmina", "wspolnota")
    except Exception:
        return False


def cfg_surowy():
    baza = {**json.loads(json.dumps(core.DEFAULT_CONFIG)), **json.loads(json.dumps(DOMYSLNE_WEB))}
    glob = czytaj(F_CFG, {})
    if konto_admina():
        c = {**baza, **glob}
    else:  # inne konto: własne dane firmy i ustawienia, ze wspólnych tylko klucz API i ustawienia techniczne
        kont = czytaj(plik_ustawien_konta(), {})
        puste = {k: "" for k in ("firma_nazwa", "firma_adres", "firma_nip", "firma_regon", "firma_email", "firma_tel", "firma_osoba",
                                  "profil_firmy", "profil_dostawcy", "smtp_serwer", "smtp_login", "smtp_haslo", "smtp_nadawca", "powiadomienia_adresy")}
        puste.update(hurtownie=[], miejscowosci=[], frazy_zawsze=[], centrum_nazwa="", obszar={"tryb": "wojewodztwa", "wojewodztwa": []})
        c = {**baza, **puste, **{k: v for k, v in glob.items() if k in GLOBALNE}, **{k: v for k, v in kont.items() if k not in GLOBALNE}}
    if str(c.get("profil_firmy") or "").strip() == PRZYKLAD_OPISU_FIRMY:
        # H1-11: przykładowy opis firmy budowlanej z programu okienkowego („Firma budowlana ze Świdnicy…”) nie jest opisem tej firmy –
        # jest tylko podpowiedzią w pustym polu; AI go nie dostaje
        c["profil_firmy"] = ""
    c["ceny_z_cennika"] = False
    c["folder_ofert"] = PROJ
    c.pop("vat", None)  # brak domyślnej stawki VAT
    ust, env = (c.get("api_key") or "").strip(), (os.environ.get("ANTHROPIC_API_KEY") or "").strip()
    c["api_key_ustawienia"], c["api_key_render"] = ust, env
    c["api_key"] = ust or env           # klucz główny: z Ustawień, a gdy go brak – z Rendera
    c["api_key_alt"] = env if ust and env and env != ust else ""  # drugi klucz – próbowany, gdy główny zostanie odrzucony
    c["_licznik"] = rejestruj_zuzycie_ai
    c["_limit"] = sprawdz_limit_ai
    c["_plik_cen"] = os.path.join(DATA, "ceny_rynkowe_pamiec.json")
    MO.PDF_JAKO_TEKST["wlaczone"] = bool(c.get("pdf_jako_tekst", True))
    MO.POMIJAJ_RYSUNKI["wlaczone"] = bool(c.get("pomijaj_rysunki", True))
    return c


# ---------- licznik zużycia AI (tokeny i koszt na konto i miesiąc)
F_ZUZYCIE_AI = SciezkaKonta("zuzycie_ai.json")
_BLOKADA_AI = threading.Lock()


def rejestruj_zuzycie_ai(model, u, usd):
    """Dopisuje zużycie jednego zapytania AI do licznika konta, które je uruchomiło (także w zadaniach w tle)."""
    mies = dt.date.today().strftime("%Y-%m")
    with _BLOKADA_AI:
        d = czytaj(F_ZUZYCIE_AI, {}) or {}
        x = d.setdefault(mies, {"usd": 0.0, "zapytan": 0, "wejscie": 0, "wyjscie": 0, "zapis": 0, "odczyt": 0, "wyszukiwan": 0, "modele": {}})
        x["usd"] = round(x["usd"] + usd, 5)
        x["zapytan"] += 1
        x["wejscie"] += u.get("input_tokens") or 0
        x["wyjscie"] += u.get("output_tokens") or 0
        x["zapis"] += u.get("cache_creation_input_tokens") or 0
        x["odczyt"] += u.get("cache_read_input_tokens") or 0
        x["wyszukiwan"] += (u.get("server_tool_use") or {}).get("web_search_requests") or 0
        x["modele"][model] = round(x["modele"].get(model, 0) + usd, 5)
        typ = getattr(_KONTEKST, "typ", None) or "inne"
        x.setdefault("zadania", {})[typ] = round(x.get("zadania", {}).get(typ, 0) + usd, 5)
        pisz(F_ZUZYCIE_AI, d)
    _KONTEKST.koszt_zadania = (getattr(_KONTEKST, "koszt_zadania", 0) or 0) + usd  # koszt bieżącego zadania (ranking najdroższych)


F_KOSZTY_ZADAN = os.path.join(DATA, "koszty_zadan.json")


def sprawdz_limit_ai():
    """Miesięczny limit kosztów AI konta (ustawiany przez administratora): po przekroczeniu zapytania AI są blokowane."""
    try:
        login = konto_biezace()
    except Exception:
        return
    glob = czytaj(F_CFG, {}) or {}
    lim = float(((glob.get("limity_ai") or {}).get(login) or 0))
    if not lim:
        return
    kurs = float(glob.get("kurs_usd", 3.65) or 3.65)
    uzyte = float(zuzycie_ai_konta(login).get("usd") or 0) * kurs
    if uzyte >= lim:
        zl_ = lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")
        raise RuntimeError(f"Wykorzystano miesięczny limit kosztów AI dla konta ({zl_(uzyte)} zł z {zl_(lim)} zł). "
                           "Administrator może zwiększyć limit w zakładce Konta i aktywność.")


def zuzycie_ai_konta(login, mies=None):
    mies = mies or dt.date.today().strftime("%Y-%m")
    return (czytaj(F_ZUZYCIE_AI.dla(login), {}) or {}).get(mies) or {"usd": 0.0, "zapytan": 0}


_ODSWIEZANE = {}  # NIP -> czas ostatniej próby (żeby nie odpytywać wykazu przy każdym wywołaniu)


def wykaz(nip, czekaj=False):
    """Dane z wykazu VAT po NIP z pamięci programu; brakujące lub starsze niż 30 dni odświeża w tle
    (albo od razu, gdy czekaj=True). Nigdy nie zgłasza błędu – zwraca None."""
    n = NIP.oczysc(nip)
    if not NIP.poprawny(n):
        return None
    cache = czytaj(F_NIP_CACHE, {})
    w = cache.get(n)
    swiezy = w and (dt.date.today() - dt.date.fromisoformat(w["czas"][:10])).days <= 30 and \
        (not cfg_surowy().get("ceidg_token") or w["dane"].get("ceidg_sprawdzono"))
    if not swiezy and time.time() - _ODSWIEZANE.get(n, 0) > 3600:
        _ODSWIEZANE[n] = time.time()

        def odswiez():
            with BLOKADA:
                cc = czytaj(F_NIP_CACHE, {})
            _, blad = NIP.szukaj(n, cc, ceidg_token=cfg_surowy().get("ceidg_token"))
            if not blad:
                with BLOKADA:
                    pisz(F_NIP_CACHE, {**czytaj(F_NIP_CACHE, {}), n: cc[n]})
        if czekaj:
            odswiez()
            w = czytaj(F_NIP_CACHE, {}).get(n)
        else:
            threading.Thread(target=odswiez, daemon=True).start()
    return (w or {}).get("dane")


def cfg():
    """Konfiguracja do pracy i dokumentów: dane wykonawcy (nazwa firmy, adres, REGON) z wykazu VAT po NIP,
    jeśli ta opcja jest włączona – np. „K.A. Jakub Górski” zamiast samego imienia i nazwiska."""
    c = cfg_surowy()
    if c.get("firma_z_wykazu", True) and NIP.poprawny(c.get("firma_nip")):
        d = wykaz(c["firma_nip"])
        wlasna = (c.get("firma_nazwa") or "").strip()
        if d and d.get("nazwa") and not (d["nazwa"].lower() in wlasna.lower() and len(wlasna) > len(d["nazwa"])):
            c["firma_nazwa"] = d["nazwa"]  # nazwa wpisana ręcznie wygrywa, gdy jest pełniejsza (np. „K.A. Jakub Górski”)
            c["firma_adres"] = d.get("adres") or c.get("firma_adres", "")
            c["firma_regon"] = d.get("regon") or c.get("firma_regon", "")
            c["firma_nip"] = d.get("nip") or c["firma_nip"]
    return c


def zapisz_cfg(c):
    c = {k: v for k, v in c.items() if k != "folder_ofert"}
    if os.environ.get("ANTHROPIC_API_KEY") and c.get("api_key") == os.environ["ANTHROPIC_API_KEY"]:
        c["api_key"] = ""
    pisz(F_CFG, c)


# ============================================================ aplikacja i logowanie
