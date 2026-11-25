# -*- coding: utf-8 -*-
"""
Projekty wykonawcy (oferty) – trasy: pliki projektu, sprawdzenie dokumentacji i kontrola (AI), czat z dokumentami, formularz cenowy i pozycje kosztorysu, analiza dostawcy, harmonogram i plan, konsorcjum / wykonawcy, zamówienia u hurtowni, zdjęcia.
Blueprint „projekty_wykonawcy” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import urllib.parse
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("projekty_wykonawcy", __name__)


def pliki_wykonawcy(pid):
    d = os.path.join(S.pdir(pid), "dokumenty_wykonawcy")
    spr = set(S.meta(pid).get("sprawdzone_wykonawcy", []))
    if not os.path.isdir(d):
        return []
    return [{"nazwa": n, "rozmiar": os.path.getsize(os.path.join(d, n)), "sprawdzony": n in spr}
            for n in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, n))]


@bp.post("/api/projekty/<pid>/pliki")
@S.wymaga_logowania
def pliki_dodaj(pid):
    d = os.path.join(S.pdir(pid), "dokumenty")
    os.makedirs(d, exist_ok=True)
    uwagi, pominiete, zapisane = [], [], 0  # błąd jednego pliku (archiwum) nie przerywa zapisu pozostałych
    for f in request.files.getlist("pliki"):
        nazwa = S.secure_filename_pl(f.filename)
        if S.MO.czy_wykonywalny(nazwa):
            uwagi.append(f"{nazwa}: plik programu (wykonywalny) – nie wgrano; dokumentacja to PDF, Word, Excel, obrazy lub archiwa.")
            continue
        cel = os.path.join(d, nazwa)
        f.save(cel)
        if S.MO.czy_wykonywalny(nazwa, cel):
            os.remove(cel)
            uwagi.append(f"{nazwa}: plik programu (wykonywalny) – nie wgrano; dokumentacja to PDF, Word, Excel, obrazy lub archiwa.")
            continue
        cel = S.MO.popraw_rozszerzenie(cel)  # np. „…24.09.2024r_pdf” → „…24.09.2024r.pdf”
        nazwa = os.path.basename(cel)
        zapisane += 1
        if S.MO.czy_archiwum(nazwa):
            try:
                S.MO.rozpakuj_zip(cel, os.path.join(d, os.path.splitext(nazwa)[0]), uwagi=uwagi)
                os.remove(cel)
            except S.MO.LimitArchiwum as e:  # za duże / „zip bomb” – archiwum odrzucone
                os.remove(cel)
                uwagi.append(f"{nazwa}: {e} Archiwum nie zostało zapisane.")
            except Exception as e:  # uszkodzone, z hasłem, niebezpieczne ścieżki – zostaje, pominięte (nie idzie do AI)
                uwagi.append(f"{nazwa}: {S.MO._polski_blad(e)} Archiwum zostawiono na liście jako pominięte.")
                pominiete.append(os.path.relpath(cel, d).replace(os.sep, "/"))
    if pominiete:
        with S.BLOKADA:
            m = S.meta(pid)
            m["pominiete"] = sorted(set(m.get("pominiete", [])) | set(pominiete))
            S.zapisz_meta(pid, m)
    if zapisane:
        S.dokumenty_zmienione(pid, "Dodano dokumenty")
    r = jsonify(S.lista_plikow(pid))
    if uwagi:  # lista plików bez zmian w treści odpowiedzi; uwagi w nagłówku (app.js pokazuje je jako komunikat)
        r.headers["X-Uwagi"] = urllib.parse.quote(" ".join(uwagi)[:3000])
    return r


@bp.post("/api/projekty/<pid>/pliki/uwzglednij-wszystkie")
@S.wymaga_logowania
def pliki_uwzglednij_wszystkie(pid):
    m = S.meta(pid)
    zm_ = bool(m.get("pominiete"))
    m["pominiete"] = []
    S.zapisz_meta(pid, m)
    d = os.path.join(S.pdir(pid), "dokumenty")
    if os.path.isdir(d):
        S.popraw_nazwy_folderu(d)
    if zm_:
        S.dokumenty_zmienione(pid, "Zmieniono wybór dokumentów")
    return jsonify(S.lista_plikow(pid))


def _napisy(v):
    """Lista napisów z danych żądania (inne typy pomijane – bez błędu 500)."""
    return [x for x in v if isinstance(x, str)] if isinstance(v, list) else []


@bp.post("/api/projekty/<pid>/pliki/przelacz")
@S.wymaga_logowania
def pliki_przelacz(pid):
    m = S.meta(pid)
    pom = set(m.get("pominiete", []))
    istn = {p["sciezka"] for p in S.lista_plikow(pid)}
    for s in _napisy(request.json.get("sciezki")):
        if s in istn:  # tylko pliki projektu (nie zapisuje nieistniejących ścieżek)
            pom.symmetric_difference_update({s})
    m["pominiete"] = sorted(pom)
    S.zapisz_meta(pid, m)
    S.dokumenty_zmienione(pid, "Zmieniono wybór dokumentów")
    return jsonify(S.lista_plikow(pid))


@bp.post("/api/projekty/<pid>/pliki/usun")
@S.wymaga_logowania
def pliki_usun(pid):
    d = os.path.join(S.pdir(pid), "dokumenty")
    sciezki = request.json.get("sciezki")
    if sciezki is None:  # wszystkie – do archiwum
        sciezki = [p["sciezka"] for p in S.lista_plikow(pid)]
    sciezki = _napisy(sciezki)
    for s_ in sciezki:
        p = os.path.realpath(os.path.join(d, s_))
        if p.startswith(os.path.realpath(d) + os.sep) and os.path.isfile(p):
            S.archiwizuj_plik(pid, p)
    S.dokumenty_zmienione(pid, "Usunięto dokumenty")
    return jsonify(S.lista_plikow(pid))


def pliki_oferty(m):
    nazwa = S.MO.bezpieczna_nazwa(m.get("nazwa", "oferta"))[:60]
    if m.get("typ") == "kosztorys":
        return (f"Kosztorys_{nazwa}.xlsx", None, None)
    if m.get("typ") in S.INWESTORSKIE:
        rz = m.get("rodzaj_zamowienia")
        return ({"uslugi": f"Kosztorys_inwestorski_uslugi_{nazwa}.xlsx", "dostawy": f"Kosztorys_inwestorski_dostawy_{nazwa}.xlsx"}.get(rz, f"Kosztorys_inwestorski_{nazwa}.xlsx"), None, None)
    if m.get("typ") == "dom":
        return (f"Kosztorys_budowy_{nazwa}.xlsx", None, None)
    if m.get("typ") == "wlasny":
        return (f"Kosztorys_ofertowy_{nazwa}.xlsx", None, None)
    if m.get("rodzaj_zamowienia") in ("dostawy", "uslugi"):  # dostawca / usługodawca
        return (f"Formularz_cenowy_{nazwa}.xlsx", f"Oferta_{nazwa}_formularze.docx", None)
    return (f"Kosztorys_ofertowy_{nazwa}.xlsx", f"Oferta_{nazwa}_formularze.docx",
            f"Analiza_{'projektu' if m.get('typ') == 'wlasny' else 'przetargu'}_{nazwa}.docx")


def praca_kontrola(log, pid, z_ai):
    d = S.pdir(pid)
    dane = S.czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane:
        raise ValueError("Najpierw przygotuj ofertę lub kosztorys.")
    alerty = S.KON.reguly(dane)
    log(f"Kontrola reguł: {len(alerty)} uwag.")
    if z_ai:
        c = S.cfg()
        S.wymagany_klucz(c)
        log("Analiza AI kosztorysu…")
        try:
            alerty += S.KON.analiza_ai(c, dane, log)
        except Exception as e:
            log(f"Analiza AI nie powiodła się ({e}) – pokazuję wyniki reguł.")
    stare = {a["id"]: a for a in (S.meta(pid).get("kontrola") or {}).get("alerty", [])}
    for a in alerty:  # zachowaj wcześniejsze decyzje użytkownika
        if a["id"] in stare and stare[a["id"]].get("status") in ("odstepstwo", "zastosowany"):
            a["status"] = stare[a["id"]]["status"]
    poz = {p["lp"]: p for p in S.KON.pozycje(dane)}
    for a in alerty:
        p = poz.get(a["lp"])
        if p:
            a["pozycja"] = {k: p.get(k) for k in ("opis", "jm", "ilosc", "cena", "wartosc", "dzial")}
    m = S.meta(pid)
    m["kontrola"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "alerty": alerty}
    S.zapisz_meta(pid, m)
    return {"alerty": len(alerty)}


@bp.post("/api/projekty/<pid>/kontrola")
@S.wymaga_logowania
def kontrola(pid):
    return jsonify(S.uruchom("kontrola", "Sprawdzanie kosztorysu", praca_kontrola, pid, bool((request.json or {}).get("ai", True))))


@bp.post("/api/projekty/<pid>/kontrola/alert")
@S.wymaga_logowania
def kontrola_alert(pid):
    """Akcje na alercie: odstepstwo | przywroc | zmien (ręczna poprawka pól) | zastosuj (sugestia)."""
    j = request.json
    d = S.pdir(pid)
    m = S.meta(pid)
    alerty = (m.get("kontrola") or {}).get("alerty", [])
    a = next((x for x in alerty if x["id"] == j.get("id")), None)
    if not a:
        return jsonify({"blad": "Nie ma takiego alertu – uruchom kontrolę ponownie."}), 404
    akcja = j.get("akcja")
    if akcja in ("odstepstwo", "przywroc"):
        a["status"] = "odstepstwo" if akcja == "odstepstwo" else "nowy"
        S.zapisz_meta(pid, m)
        return jsonify({"ok": True})
    zmiany = dict(j.get("zmiany") or {})
    if akcja == "zastosuj" and a.get("sugestia"):
        zmiany = {a["sugestia"]["pole"]: a["sugestia"]["wartosc"]}
    if not a.get("lp") or not zmiany:
        return jsonify({"blad": "Brak zmian do zapisania."}), 400
    teraz = S.czytaj(os.path.join(d, "oferta_dane.json"), None)
    orig = S.czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None) or json.loads(json.dumps(teraz))
    pt = next((p for p in S.KON.pozycje(teraz) if p["lp"] == a["lp"]), None)
    if not pt:
        return jsonify({"blad": "Pozycja nie istnieje."}), 400
    po = orig["dzialy"][pt["di"]]["pozycje"][pt["pi"]]
    po = S.MO._pozycja(po)
    for pole, v in zmiany.items():
        if pole in ("ilosc", "cena"):
            try:
                v = S.MO.liczba_pl(v)
            except ValueError:
                return jsonify({"blad": f"Nieprawidłowa wartość: {pole}"}), 400
            if pole == "cena":  # cena wpisana przez wykonawcę jest ostateczna – korekta ceny oferty jej nie zmienia (zrodlo „poprawione”)
                v = S.MO.zaokr(v)
                po["zrodlo"] = "poprawione ręcznie (kontrola kosztorysu)"
        elif pole in ("jm", "opis"):
            v = str(v)[:500]
        else:
            continue
        po[pole] = v
    po["uwagi"] = (po.get("uwagi", "") + " [poprawione po kontroli]").strip()
    orig["dzialy"][pt["di"]]["pozycje"][pt["pi"]] = po
    S.pisz(os.path.join(d, "oferta_dane_oryginal.json"), orig)
    kor = (m.get("oferta") or {}).get("korekta")
    blad = S.zastosuj_korekte(pid, orig, kor.get("tryb") if kor else None, kor.get("wartosc") if kor else None)
    if blad:
        return jsonify({"blad": blad}), 400
    m = S.meta(pid)
    for x in (m.get("kontrola") or {}).get("alerty", []):
        if x["id"] == a["id"]:
            x["status"] = "zastosowany"
    S.zapisz_meta(pid, m)
    return jsonify({"ok": True, "oferta": m.get("oferta")})


def tryb_weryfikacji(m):
    """Tryb do listy kontrolnej weryfikacji: wybrany przy weryfikacji, inaczej tryb z kreatora tego projektu, inaczej „ustal z dokumentów”."""
    t = m.get("weryfikacja_tryb") or ((m.get("kreator") or {}).get("tryb_wybrany")) or "auto"
    return t if t in S.LK.TRYBY else "auto"


def praca_weryfikacja(log, pid, dodatkowe):
    c = S.cfg()
    c["_log"] = log
    # wykrywanie błędów: domyślnie średni model; najdokładniejszy (najdroższy) tylko na żądanie („dokładne sprawdzenie”)
    c["_model"] = (c.get("model_dokladny") or "claude-opus-5-5") if getattr(S._KONTEKST, "dokladne", False) else (c.get("model_oferty") or "claude-sonnet-5-5")
    S.wymagany_klucz(c)
    # większy zapas na rozumowanie: przy dużej dokumentacji odpowiedź (34 uwagi) przekraczała limit i była dokańczana
    # drugim zapytaniem – z ponownym wysłaniem wszystkich dokumentów (ok. 490 tys. tokenów). Płaci się tylko za zużyte tokeny.
    c["_zapas_rozumowania"] = 64000
    m0 = S.meta(pid)
    try:
        bloki, n = S.bloki_projektu(pid, log=log)
    except ValueError as e:  # za duże na jedno zapytanie – od razu w częściach
        if "zbyt duże" not in str(e):
            raise
        log("Dokumentacja zbyt obszerna na jedno zapytanie – sprawdzam od razu w częściach.")
        bloki, n = [], len([x for x in S.lista_plikow(pid) if x["uwzglednij"]])
        m0["weryfikacja_w_czesciach"] = True
    if not n:
        raise ValueError("Dodaj dokumentację przetargową w kroku 1 (SWZ, OPZ, przedmiar, wzór umowy, formularze).")
    strona = m0.get("strona") or S.strona_typu(m0.get("typ"))
    rodz = m0.get("rodzaj_zamowienia") or "roboty"
    if strona in ("wykonawca", "dostawca"):  # porady dla wykonawcy / dostawcy – nie dla zamawiającego
        etap = "realizacja" if (m0.get("status_projektu") in ("realizacja", "zakonczony") or m0.get("umowa_dane")) else "oferta"
        log(f"AI sprawdza {n} dokumentów z perspektywy wykonawcy ({'realizacja umowy' if etap == 'realizacja' else 'przed złożeniem oferty'})…")
        rp_ = S.rodzaj_postepowania_projektu(pid, m0)
        polec, system = S.ZAM.polecenie_weryfikacji_wykonawcy(dodatkowe or "", rodz, etap, rp_), S.ZAM.SYSTEM_WER_WYK
    elif strona == "prawnik":
        u_ = S.PRW.ustawienia(m0)
        log(f"AI sprawdza {n} dokumentów jako prawnik – {S.PRW.PRZEDMIOTY[u_['przedmiot']].lower()}, {S.PRW.TRYBY[u_['tryb']]}, {S.PRW.DLA_KOGO[u_['dla_kogo']]}…")
        polec, system = S.PRW.polecenie(u_, dodatkowe or ""), S.PRW.SYSTEM
    else:
        wsp_ = S.projekt_wspolnoty(m0)
        log(f"AI sprawdza {n} dokumentów – szuka błędów, sprzeczności i braków{' (zasady wspólnot i spółdzielni, bez Pzp)' if wsp_ else ''}…")
        tryb_ = tryb_weryfikacji(m0)
        if not wsp_:
            log(f"Lista kontrolna według trybu: {S.LK.TRYBY.get(tryb_, tryb_)}.")
        polec = S.ZAM.polecenie_weryfikacji(dodatkowe or "", rodz, S.LK.lista_weryfikacji(tryb_, rodz, bool(wsp_)))
        system = S.ZAM.SYSTEM_WER + (S.WSPOL.KONTEKST_AI if wsp_ else "")
    w = None
    if not m0.get("weryfikacja_w_czesciach"):
        tresc = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polec}]
        try:
            w = S.ai_dane(c, system, tresc, 16000, log, S.ZAM.wynik_weryfikacji, "Najważniejsze uwagi najpierw, maksymalnie 25, zwięźle.")
        except ValueError as e:
            if n < 2 or "nie zawiera danych" not in str(e):
                raise
            log(f"Cała dokumentacja naraz nie dała wyniku ({e}) – sprawdzam w częściach.")
    if w is None:
        del bloki
        w = S.weryfikacja_w_czesciach(c, system, polec, pid, log)
        m_ = S.meta(pid)
        m_["weryfikacja_w_czesciach"] = True  # kolejne sprawdzenia tego projektu – od razu w częściach
        S.zapisz_meta(pid, m_)
    w["perspektywa"] = "wykonawca" if strona in ("wykonawca", "dostawca") or (strona == "prawnik" and S.PRW.ustawienia(m0)["dla_kogo"] == "wykonawca") else "zamawiajacy"
    log("Sprawdzam cytaty i odwołania w dokumentach…")
    S.OD.dodaj(S.pdir(pid), w["uwagi"], pomin={"dokumenty/" + p_["sciezka"] for p_ in S.lista_plikow(pid) if not p_["uwzglednij"]})  # cytaty – tylko w uwzględnionych plikach
    m = S.meta(pid)
    stare = {u["id"]: u.get("status") for u in (m.get("weryfikacja") or {}).get("uwagi", [])}
    for u in w["uwagi"]:
        u["status"] = stare.get(u["id"], u["status"])
    m["weryfikacja"] = w
    S.zapisz_meta(pid, m)
    log(f"Znaleziono uwag: {len(w['uwagi'])} (krytycznych: {sum(1 for u in w['uwagi'] if u['waga'] == 'krytyczna')}).")
    return {"uwagi": len(w["uwagi"])}


@bp.post("/api/projekty/<pid>/weryfikacja")
@S.wymaga_logowania
def weryfikacja(pid):
    j = request.json or {}
    dokl = bool(j.get("dokladne"))
    if j.get("tryb") in S.LK.TRYBY:  # tryb postępowania do listy kontrolnej (zamawiający)
        with S.BLOKADA:
            m = S.meta(pid)
            m["weryfikacja_tryb"] = j["tryb"]
            S.zapisz_meta(pid, m)

    def praca(log, pid_, dod):
        S._KONTEKST.dokladne = dokl
        try:
            if dokl:
                log("Dokładne sprawdzenie – najdokładniejszy (droższy) model AI.")
            return praca_weryfikacja(log, pid_, dod)
        finally:
            S._KONTEKST.dokladne = False
    return jsonify(S.uruchom("weryfikacja", "Weryfikacja dokumentacji" + (" (dokładna)" if dokl else ""), praca, pid, str(j.get("dodatkowe", ""))[:1000]))


@bp.post("/api/projekty/<pid>/weryfikacja/uwaga")
@S.wymaga_logowania
def weryfikacja_uwaga(pid):
    j = request.json or {}
    if j.get("status") not in ("do poprawy", "poprawione", "odrzucone"):
        return jsonify({"blad": "Nieznany status."}), 400
    m = S.meta(pid)
    for u in (m.get("weryfikacja") or {}).get("uwagi", []):
        if u["id"] == j.get("id"):
            u["status"] = j["status"]
    S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


@bp.get("/api/projekty/<pid>/weryfikacja.docx")
@S.wymaga_logowania
def weryfikacja_docx(pid):
    m = S.meta(pid)
    if not m.get("weryfikacja"):
        abort(404)
    p = os.path.join(S.pdir(pid), f"Raport_weryfikacji_{S.MO.bezpieczna_nazwa(m.get('nazwa', 'dokumentacja'))[:50]}.docx")
    S.ZAM.raport_weryfikacji_docx(p, m.get("nazwa", ""), m["weryfikacja"], S.cfg())
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


def _pliki_do_przegladu(pid, st):
    d = S.pdir(pid)
    if st["sciezka"] == "wzory":
        wz = os.path.join(d, "wzory")
        pliki = sorted(os.listdir(wz)) if os.path.isdir(wz) else []
        z_pdf = {f[:-len(" (z PDF).docx")] for f in pliki if f.endswith(" (z PDF).docx") and S.KZ.docx_ma_tekst(os.path.join(wz, f))}
        pliki = [f for f in pliki if not f.endswith(" (z PDF).docx") or f[:-len(" (z PDF).docx")] in z_pdf]
        # PDF, który ma wersję Word, sprawdzamy w wersji Word (zmiany wprowadzane automatycznie)
        return [os.path.join(wz, f) for f in pliki if not (f.lower().endswith(".pdf") and os.path.splitext(f)[0] in z_pdf)]
    wlasne = [os.path.join(d, "wzory", e["wlasny"]) for e in (st.get("elementy") or []) if e.get("wlasny")]  # własne wzory pism – też sprawdzane
    return [os.path.join(d, f) for f in st["dokumenty"] if os.path.isfile(os.path.join(d, f))] + [p for p in wlasne if os.path.isfile(p)]


@bp.post("/api/projekty/<pid>/weryfikacja/decyzja")
@S.wymaga_logowania
def weryfikacja_decyzja(pid):
    """Akceptacja / odrzucenie proponowanej zmiany z uwagi (z możliwością poprawienia nowego brzmienia)."""
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        U = (m.get("weryfikacja") or {}).get("uwagi") or []
        u = next((x for x in U if x.get("id") == j.get("id")), None)
        if not u:
            return jsonify({"blad": "Nie ma takiej uwagi."}), 404
        if j.get("decyzja") in ("tak", "nie", ""):
            u["zmiana"] = j["decyzja"]
        if j.get("nowy") is not None:
            u["nowy_edyt"] = str(j["nowy"])[:3000]
        S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


@bp.post("/api/projekty/<pid>/weryfikacja/wprowadz")
@S.wymaga_logowania
def weryfikacja_wprowadz(pid):
    """Zaakceptowane zmiany z uwag → dokumenty Word ze śledzeniem zmian i czyste (PDF z tekstem zamieniany na Word);
    ogłoszenie z BZP – dodatkowo zestawienie zmian do formularza zmiany ogłoszenia w e-Zamówieniach."""
    m = S.meta(pid)
    U = [u for u in (m.get("weryfikacja") or {}).get("uwagi") or [] if u.get("zmiana") == "tak"]
    if not U:
        return jsonify({"blad": "Zaakceptuj co najmniej jedną zmianę."}), 400
    kat = os.path.join(S.pdir(pid), "dokumenty_poprawione")
    os.makedirs(kat, exist_ok=True)
    grupy, reczne, ogloszenie = {}, [], []
    for u in U:
        nowy = u.get("nowy_edyt") if u.get("nowy_edyt") is not None else u.get("nowy_tekst")
        rel = S._plik_dokumentu(pid, u.get("dokument"))
        if re.search(r"(?i)og[łl]oszeni", str(u.get("dokument") or "") + " " + str(rel or "")):
            ogloszenie.append(u)
        if not nowy or not u.get("cytat"):
            reczne.append(dict(u, powod="brak gotowego brzmienia albo cytatu – zmiana do wprowadzenia ręcznie"))
            continue
        if not rel:
            reczne.append(dict(u, powod="nie znaleziono pliku w dokumentach projektu"))
            continue
        grupy.setdefault(rel, []).append((u, nowy))
    wynik = []
    for rel, lista in grupy.items():
        sc, info = S._word_dla(pid, rel)
        if not sc:
            reczne += [dict(u, powod=info) for u, _ in lista]
            continue
        zm = [{"cytat": u["cytat"], "nowy": nowy, "id": u["id"]} for u, nowy in lista]
        baza = os.path.splitext(os.path.basename(sc))[0]
        ok, brak = S.KZ.wprowadz_zmiany(sc, zm, os.path.join(kat, f"{baza}_ze_zmianami.docx"), sledz=True)
        S.KZ.wprowadz_zmiany(sc, zm, os.path.join(kat, f"{baza}_czysty.docx"), sledz=False)
        ok_ids = {z_["id"] for z_ in ok}
        wynik.append({"plik": rel, "word": os.path.basename(sc), "info": info, "wprowadzone": len(ok), "nieodnalezione": len(brak)})
        reczne += [dict(u, powod="nie odnaleziono cytatu w dokumencie (sprawdź brzmienie)") for u, _ in lista if u["id"] not in ok_ids]
        with S.BLOKADA:
            m2 = S.meta(pid)
            for x in (m2.get("weryfikacja") or {}).get("uwagi") or []:
                if x.get("id") in ok_ids:
                    x["status"] = "poprawione"
                    x["wprowadzona"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            S.zapisz_meta(pid, m2)
    if ogloszenie:  # ogłoszenia z BZP nie zmienia się w pliku – formularz zmiany ogłoszenia w e-Zamówieniach
        d = S.MO._doc()
        S.MO._akapit(d, "ZMIANY DO WPROWADZENIA W OGŁOSZENIU O ZAMÓWIENIU (BZP)", pogrub=True, rozmiar=13)
        S.MO._akapit(d, "Ogłoszenie zmienia się na platformie e-Zamówienia formularzem zmiany ogłoszenia – poniżej punkty, obecne i nowe brzmienie do wklejenia.", kursywa=True, rozmiar=9)
        S.MO._tabela(d, [["Punkt ogłoszenia", "Obecne brzmienie", "Nowe brzmienie", "Uzasadnienie"]] +
                   [[u.get("miejsce") or "", u.get("cytat") or "", (u.get("nowy_edyt") if u.get("nowy_edyt") is not None else u.get("nowy_tekst")) or u.get("propozycja") or "",
                     u.get("opis") or ""] for u in ogloszenie])
        d.save(os.path.join(kat, "Zmiany_do_ogloszenia_BZP.docx"))
    with S.BLOKADA:
        m = S.meta(pid)
        (m.setdefault("weryfikacja", {}))["wprowadzanie"] = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wynik": wynik,
                                                            "reczne": [{k: u.get(k) for k in ("id", "dokument", "miejsce", "cytat", "nowy_tekst", "propozycja", "powod")} for u in reczne],
                                                            "pliki": sorted(os.listdir(kat)), "ogloszenie": bool(ogloszenie)}
        S.zapisz_meta(pid, m)
    return jsonify(S.meta(pid)["weryfikacja"]["wprowadzanie"])


def praca_czat(log, pid, pytanie, login):
    c = S.cfg()
    S.wymagany_klucz(c)
    d = S.pdir(pid)
    lp = [p for p in S.lista_plikow(pid) if p["uwzglednij"]]
    pliki = [os.path.join(d, "dokumenty", p["sciezka"]) for p in lp]
    if not pliki:
        raise ValueError("W projekcie nie ma dokumentów – dodaj je w kroku 1.")
    bloki = S.fragmenty_do_pytania(pid, {"dokumenty/" + p["sciezka"] for p in lp}, pytanie, log)
    suma = 0
    for p in ([] if bloki else pliki):  # brak pasujących fragmentów – całe dokumenty (bez rysunków)
        b, n, _ = S.MO.przygotuj_blok_tekstowy(p)
        for x in b:
            if x.get("type") == "document":
                x["citations"] = {"enabled": True}
        bloki += b
        suma += n
    if suma > S.MO.MAX_BAJTOW_ZAPYTANIA:
        raise ValueError("Dokumenty są zbyt duże – pomiń rysunki w kroku 1 (Uwzględnij/pomiń).")
    bloki = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c))
    bloki.append({"type": "text", "text": "To są dokumenty przetargu / projektu. Odpowiadaj na pytania wyłącznie na podstawie "
                  "tych dokumentów, po polsku, konkretnie. Każde stwierdzenie opieraj na cytacie z dokumentu. Jeśli odpowiedzi "
                  "nie ma w dokumentach – napisz to wprost."})
    wiad = [{"role": "user", "content": bloki}, {"role": "assistant", "content": "Rozumiem. Czekam na pytania."}]
    for h in (S.meta(pid).get("czat") or [])[-5:]:
        wiad += [{"role": "user", "content": h["pyt"]}, {"role": "assistant", "content": h["odp"] or "—"}]
    wiad.append({"role": "user", "content": pytanie})
    import ceny_rynkowe as CRn
    zap = {"model": c.get("model") or "claude-sonnet-5-5", "max_tokens": 2000, "messages": wiad,
           "system": "Jesteś asystentem firmy budowlanej analizującym dokumentację przetargową i umowy."}
    cc = S.MO.ustawienie_cache(c) and {"type": "ephemeral", "ttl": "1h"}  # kolejne pytania w ciągu godziny czytają dokumenty z pamięci
    if cc:
        zap["cache_control"] = cc
    try:
        odp = CRn._post(c, zap)
    except Exception as e:
        if "cache_control" in zap:
            zap.pop("cache_control")
            odp = CRn._post(c, zap)
        else:
            raise e
    tekst, cytaty = "", []
    for blok in odp.get("content", []):
        if blok.get("type") != "text":
            continue
        tekst += blok.get("text", "")
        for ct in blok.get("citations") or []:
            wpis = {"plik": ct.get("document_title") or "", "tekst": (ct.get("cited_text") or "").strip()[:400],
                    "strona": ct.get("start_page_number")}
            if wpis not in cytaty:
                cytaty.append(wpis)
            tekst += f" [{cytaty.index(wpis) + 1}]"
    log(S.MO.opis_uzycia(odp.get("usage")) or "Odpowiedź gotowa.")
    m = S.meta(pid)
    m.setdefault("czat", []).append({"pyt": pytanie, "odp": tekst.strip(), "cytaty": cytaty, "kto": login,
                                     "czas": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    m["czat"] = m["czat"][-30:]
    S.zapisz_meta(pid, m)
    return {"ok": True}


@bp.post("/api/projekty/<pid>/czat")
@S.wymaga_logowania
def czat(pid):
    pyt = str((request.json or {}).get("pytanie", "")).strip()
    if len(pyt) < 3:
        return jsonify({"blad": "Wpisz pytanie."}), 400
    return jsonify(S.uruchom("czat", "Asystent dokumentów", praca_czat, pid, pyt[:1000], session.get("login", "")))


@bp.post("/api/projekty/<pid>/czat/wyczysc")
@S.wymaga_logowania
def czat_wyczysc(pid):
    m = S.meta(pid)
    m["czat"] = []
    S.zapisz_meta(pid, m)
    return jsonify({"ok": True})


PODPIS_OFERTY = {
    "unijne": "Postępowanie od progów unijnych: ofertę składa się elektronicznie na platformie zamawiającego, opatrzoną kwalifikowanym podpisem "
              "elektronicznym – pod rygorem nieważności (art. 63 ust. 1 Pzp). Podpis zaufany ani osobisty nie wystarczą.",
    "krajowe": "Postępowanie poniżej progów unijnych: ofertę składa się elektronicznie na platformie zamawiającego, opatrzoną kwalifikowanym podpisem "
               "elektronicznym, podpisem zaufanym albo podpisem osobistym – pod rygorem nieważności (art. 63 ust. 2 Pzp).",
    "poza": "Zamówienie poza Pzp (zapytanie ofertowe, regulamin, zasada konkurencyjności): formę oferty i podpisu określa zapytanie ofertowe "
            "(np. platforma, Baza Konkurencyjności, e-mail ze skanem albo podpisem elektronicznym) – złóż ofertę dokładnie tak, jak wskazano.",
    "nieznane": "Forma podpisu zależy od postępowania: od progów unijnych – wyłącznie kwalifikowany podpis elektroniczny (art. 63 ust. 1 Pzp); poniżej progów "
                "unijnych – kwalifikowany, zaufany albo osobisty (art. 63 ust. 2 Pzp); poza Pzp – według zapytania ofertowego. Sprawdź w SWZ / zapytaniu.",
}


def podpis_oferty(P):
    """Forma podpisu oferty (art. 63 Pzp) z analizy dokumentów: miejsce ogłoszenia i tryb."""
    t = " ".join(str((P or {}).get(k) or "") for k in ("ogloszenie", "tryb")).lower()
    if re.search(r"dziennik(u)? urzędow|dz\.\s*u(rz)?\.\s*ue|\bted\b|unijn|przetarg nieograniczony|przetarg ograniczony|dialog|negocjacje z ogłoszeniem", t):
        r = "unijne"
    elif re.search(r"\bbzp\b|biuletyn|podstawow|krajow|poniżej progów unijnych", t):
        r = "krajowe"
    elif re.search(r"zapytani|poza pzp|regulamin|konkurencyjno|bez stosowania|poniżej 130|poniżej 170|brak", t):
        r = "poza"
    else:
        r = "nieznane"
    return {"rodzaj": r, "tekst": PODPIS_OFERTY[r]}


@bp.post("/api/projekty/<pid>/zlozenie")
@S.wymaga_logowania
def zlozenie_zaznacz(pid):
    """Lista kontrolna złożenia oferty (krok 5): zaznaczenia na serwerze – te same na każdym urządzeniu i dla każdego użytkownika projektu.
    Klucz to treść pozycji (nie numer), więc po ponownej analizie zaznaczenia zostają przy tych samych dokumentach."""
    j = request.json or {}
    zaz = j.get("zaznaczenia") if isinstance(j.get("zaznaczenia"), dict) else {str(j.get("klucz") or ""): bool(j.get("v"))}
    with S.BLOKADA:
        m = S.meta(pid)
        Z = m.get("zlozenie_lista") if isinstance(m.get("zlozenie_lista"), dict) else {}
        for k, v in zaz.items():
            k = str(k)[:400]
            if not k:
                continue
            if v:
                Z[k] = True
            else:
                Z.pop(k, None)
        m["zlozenie_lista"] = dict(list(Z.items())[-200:])
        S.zapisz_meta(pid, m)
    return jsonify({"zaznaczenia": m["zlozenie_lista"]})


@bp.get("/api/projekty/<pid>/formularz-cenowy")
@S.wymaga_logowania
def formularz_cenowy(pid):
    m = S.meta(pid)
    return jsonify({"podpis": podpis_oferty((m.get("analiza_dostawcy") or {}).get("postepowanie")), "zlozenie": m.get("zlozenie_lista") or {},"pozycje": m.get("formularz_cenowy") or [], "vat": m.get("formularz_vat", "0.23"), "oferta": m.get("oferta"),
                    "pamiec": S._pamiec_cen_dla(m.get("formularz_cenowy") or []),
                    "analiza": m.get("analiza_dostawcy"), "weryfikacja": m.get("formularz_weryfikacja"), "komplet": m.get("komplet"),
                    "zalaczniki": m.get("zalaczniki_dostawcy"), "koszty_pracy": S.koszty_pracy_oferty(m),
                    "link": (m.get("przetarg") or {}).get("link", "")})


@bp.post("/api/projekty/<pid>/formularz-cenowy")
@S.wymaga_logowania
def formularz_cenowy_zapisz(pid):
    """Oferta dostawcy / usługodawcy: pozycje i ceny wpisane przez użytkownika → formularz cenowy i dokumenty oferty (bez AI)."""
    j = request.json or {}
    poz = []
    for x in j.get("pozycje") if isinstance(j.get("pozycje"), list) else []:
        if not isinstance(x, dict):
            continue
        opis = str(x.get("opis") or "").strip()
        if not opis:
            continue
        poz.append({"opis": opis[:500], "jm": str(x.get("jm") or "szt.")[:20], "ilosc": S._f_liczba(x.get("ilosc") or 1),
                    "cena": S._f_liczba(x.get("cena")), "uwagi": str(x.get("uwagi") or "")[:300], "czesc": str(x.get("czesc") or "")[:20]})
    vat = str(j.get("vat") or "0.23")
    if vat not in ("0.23", "0.08", "0.05", "0"):
        vat = "0.23"
    with S.BLOKADA:
        m = S.meta(pid)
        m["formularz_cenowy"], m["formularz_vat"] = poz, vat
        S.zapisz_meta(pid, m)
        pam = S.czytaj(S.F_CENY_DOS, {}) or {}
        for p_ in poz:
            if p_["cena"]:
                pam[S._klucz_pozycji(p_["opis"], p_["jm"])] = {"opis": p_["opis"][:200], "jm": p_["jm"], "cena": p_["cena"], "data": dt.date.today().isoformat(), "projekt": m.get("nazwa", "")[:80]}
        if len(pam) > 5000:
            pam = dict(sorted(pam.items(), key=lambda kv: kv[1].get("data", ""))[-5000:])
        S.pisz(S.F_CENY_DOS, pam)
    if not j.get("przygotuj"):
        return jsonify({"zapisano": len(poz), "koszty_pracy": S.koszty_pracy_oferty(S.meta(pid))})
    if not poz:
        return jsonify({"blad": "Dodaj co najmniej jedną pozycję."}), 400
    bez_ceny = [p["opis"][:40] for p in poz if not p["cena"]]
    if bez_ceny:
        return jsonify({"blad": f"Uzupełnij cenę w {len(bez_ceny)} pozycjach (np. „{bez_ceny[0]}”)."}), 400
    m = S.meta(pid)
    t = m.get("przetarg") or {}
    A = (m.get("analiza_dostawcy") or {}).get("postepowanie") or {}
    P = {"nazwa_zamowienia": A.get("nazwa_zamowienia") or t.get("przedmiot") or m.get("nazwa", ""), "numer": A.get("numer") or t.get("numer") or m.get("przetarg_numer") or "",
         "zamawiajacy_nazwa": A.get("zamawiajacy_nazwa") or t.get("zamawiajacy", ""), "zamawiajacy_nip": A.get("zamawiajacy_nip", ""),
         "termin_skladania": A.get("termin_skladania") or t.get("termin_ofert", ""), "termin_wykonania": A.get("termin_wykonania", ""),
         "gwarancja_mies": A.get("gwarancja_mies", ""), "vat": float(vat), "obiekt": t.get("miejscowosc", "")}
    S.uzupelnij_zamawiajacego(P)
    dane = {"postepowanie": P, "dzialy": [{"nazwa": "Przedmiot zamówienia" if m.get("rodzaj_zamowienia") == "dostawy" else "Usługi",
            "pozycje": [[str(i), p["opis"], p["jm"], p["ilosc"], p["cena"], 0, "cena oferenta", p["uwagi"]] for i, p in enumerate(poz, 1)]}]}
    dane["zalaczniki_do_oferty"] = (m.get("analiza_dostawcy") or {}).get("wymagane_dokumenty") or []
    dane = S.MO.przelicz(dane)
    c = S.cfg()
    d = S.pdir(pid)
    S.pisz(os.path.join(d, "oferta_dane_oryginal.json"), dane)
    S.zapisz_oferte(pid, dane, c)  # formularz cenowy (Excel)
    return jsonify(S.uruchom("zalaczniki", "Formularz ofertowy i załączniki według ogłoszenia", S.praca_zalaczniki_dostawcy, pid))


@bp.post("/api/projekty/<pid>/analiza-dostawcy")
@S.wymaga_logowania
def analiza_dostawcy(pid):
    return jsonify(S.uruchom("analiza", "Analiza przetargu (dostawca)", praca_analiza_dostawcy, pid))


def praca_analiza_dostawcy(log, pid):
    """Krok 2 oferty dostawcy: analiza dokumentów, co trzeba zaoferować, wymagane dokumenty, terminy i błędy dokumentacji."""
    c = S.cfg()
    S.wymagany_klucz(c)
    m = S.meta(pid)
    pliki = S.bloki_dokumentow(pid, log)
    if not pliki:
        raise ValueError("Najpierw dodaj dokumenty przetargu (krok 1) – albo zaznacz „uwzględnij” przy plikach z treścią.")
    polec = S.polecenie_analizy_dostawcy(m.get("rodzaj_zamowienia"))

    def parsuj(txt):
        a_ = S.MO.wyciagnij_json(txt)
        if not isinstance(a_, dict) or not (a_.get("co_zaoferowac") or a_.get("podsumowanie")):
            raise ValueError("Odpowiedź AI nie zawiera danych analizy.")
        return a_
    a = None
    if not m.get("analiza_w_czesciach"):
        log(f"AI analizuje {len(pliki)} dokumentów przetargu…")
        tresc = S.MO.oznacz_dokumenty([b for _, bl, _ in pliki for b in bl], S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polec}]
        try:
            a = S.ai_dane(c, S.SYSTEM_ANALIZA_DOSTAWCY, tresc, 20000, log, parsuj, "Wszystkie pozycje, wymagania krótko.")
            if (S.MO.DIAG.get("ostatnia") or {}).get("stop") == "max_tokens" or a.get("_odzyskane") or a.get("_naprawiony"):
                a["uciete"] = True
        except ValueError as e:
            if len(pliki) < 2 or "nie zawiera danych" not in str(e):
                raise
            log(f"Cała dokumentacja naraz nie dała wyniku ({e}) – analizuję w częściach.")
    if a is None:
        kotwica, czesci = S.podziel_na_czesci(pliki)
        log(f"Analiza w {len(czesci)} częściach" + (f" – „{kotwica[0]}” w każdej części" if kotwica else "") + ".")
        S.wyniki, bledy_cz = [], []
        for i, cz in enumerate(czesci, 1):
            nazwy = [x[0] for x in cz]
            bl = (list(kotwica[1]) if kotwica else []) + [b for x in cz for b in x[1]]
            dop = (f"\n\nTO JEST CZĘŚĆ {i} z {len(czesci)} dokumentacji ({', '.join(nazwy) or kotwica[0]}). Inne części są analizowane osobno – "
                   "nie zgłaszaj braku dokumentów, których tu nie ma; podaj pozycje i uwagi wynikające z tej części.")
            log(f"Część {i}/{len(czesci)}: {', '.join(nazwy)[:200] or kotwica[0]}…")
            try:
                S.wyniki.append(S.ai_dane(c, S.SYSTEM_ANALIZA_DOSTAWCY, S.MO.oznacz_dokumenty(bl, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polec + dop}],
                                      20000, log, parsuj, "Wszystkie pozycje, wymagania krótko."))
            except ValueError as e:
                bledy_cz.append(f"część {i} ({', '.join(nazwy)[:120]}): {e}")
                log(f"   Część {i} bez wyniku: {e}")
        if not S.wyniki:
            raise ValueError("Żadna część dokumentacji nie dała wyniku. " + " | ".join(bledy_cz)[:600])
        a = S.polacz_analizy_dostawcy(S.wyniki, czesci)
        if bledy_cz:
            a["podsumowanie"] = (a["podsumowanie"] + " Nie przeanalizowano: " + "; ".join(bledy_cz))[:3000]
        with S.BLOKADA:
            m_ = S.meta(pid)
            m_["analiza_w_czesciach"] = True
            S.zapisz_meta(pid, m_)
    a["data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    P_ = a.get("postepowanie") or {}
    if P_.get("termin_zwiazania") and P_.get("termin_skladania"):  # data końca związania ofertą liczona przez program (AI myli się o dzień)
        P_["termin_zwiazania"] = S.termin_zwiazania_tekst(P_["termin_zwiazania"], P_["termin_skladania"])
    if a.get("bledy"):
        log("Sprawdzam cytaty i odwołania w dokumentach…")
        for b in a["bledy"]:
            if isinstance(b, dict) and not b.get("miejsce"):
                b["miejsce"] = b.get("gdzie", "")
        S.OD.dodaj(S.pdir(pid), a["bledy"])
    with S.BLOKADA:
        m = S.meta(pid)
        m["analiza_dostawcy"] = a
        stare = {str(x.get("opis", "")).strip().lower(): x.get("cena") for x in m.get("formularz_cenowy") or []}
        m["formularz_cenowy"] = [{"opis": str(p.get("opis"))[:500], "jm": str(p.get("jm") or "szt.")[:20], "ilosc": S._f_liczba(p.get("ilosc") or 1),
                                  "cena": stare.get(str(p.get("opis")).strip().lower(), 0) or 0,
                                  "uwagi": str(p.get("wymagania") or "")[:300], "czesc": str(p.get("czesc") or "")[:20]}
                                 for p in a.get("co_zaoferowac") or [] if isinstance(p, dict) and p.get("opis")]
        S.zapisz_meta(pid, m)
    if a.get("uciete"):
        log("UWAGA – odpowiedź AI była dłuższa niż limit: lista pozycji może być niepełna. W kroku 3 sprawdź liczbę pozycji z formularzem zamawiającego.")
    log(f"Analiza: {len(m['formularz_cenowy'])} pozycji do wyceny, {len(a.get('wymagane_dokumenty') or [])} wymaganych dokumentów. "
        "Teraz osobne wykrywanie błędów w dokumentacji…")
    S.praca_bledy_dostawcy(log, pid)
    return {"pozycje": len(m["formularz_cenowy"])}


@bp.post("/api/projekty/<pid>/analiza-dostawcy/bledy")
@S.wymaga_logowania
def analiza_dostawcy_bledy(pid):
    return jsonify(S.uruchom("weryfikacja", "Błędy w dokumentacji przetargowej", S.praca_bledy_dostawcy, pid))


@bp.post("/api/projekty/<pid>/formularz-cenowy/sprawdz-ceny")
@S.wymaga_logowania
def sprawdz_ceny_dostawcy(pid):
    return jsonify(S.uruchom("ceny", "Sprawdzenie, czy ceny są rynkowe", S.praca_sprawdz_ceny_dostawcy, pid))


@bp.post("/api/projekty/<pid>/formularz-cenowy/z-dokumentow")
@S.wymaga_logowania
def formularz_z_dokumentow(pid):
    return jsonify(S.uruchom("formularz", "Pozycje formularza cenowego z dokumentów", S.praca_pozycje_formularza, pid))


@bp.get("/api/projekty/<pid>/pozycje")
@S.wymaga_logowania
def pozycje_kosztorysu(pid):
    dane = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), None)
    if not dane:
        return jsonify({"brak": True})
    return jsonify({k: dane.get(k) for k in ("dzialy", "netto", "vat", "vat_kwota", "brutto")})


@bp.post("/api/projekty/<pid>/pozycje")
@S.wymaga_logowania
def pozycje_popraw(pid):
    """Poprawki wybranych pozycji kosztorysu (nazwa, cena jednostkowa albo wartość). Poprawiony kosztorys staje się bazą
    dalszych kroków: oferty, materiałów, harmonogramu, umowy."""
    d = S.pdir(pid)
    dane = S.czytaj(os.path.join(d, "oferta_dane.json"), None)
    if not dane:
        return jsonify({"blad": "Projekt nie ma jeszcze kosztorysu."}), 400
    zmiany = (request.json or {}).get("zmiany") or []
    if not isinstance(zmiany, list):
        return jsonify({"blad": "Brak zmian do zapisania."}), 400
    m = S.meta(pid)
    kor = (m.get("oferta") or {}).get("korekta")
    orig = S.czytaj(os.path.join(d, "oferta_dane_oryginal.json"), None)
    zgodny = bool(orig) and len(orig.get("dzialy") or []) == len(dane.get("dzialy") or []) and \
        all(len(a.get("pozycje") or []) == len(b.get("pozycje") or []) for a, b in zip(orig["dzialy"], dane["dzialy"]))
    if kor and zgodny:  # aktywna korekta ceny: zmiany nanoszone na wycenę pierwotną, potem ta sama korekta (pozycje poprawione – stałe)
        orig_kopia = json.loads(json.dumps(orig))
        dane = orig
    ile = 0
    do_usuniecia = []
    for z in zmiany:
        if not isinstance(z, dict):
            continue
        if z.get("usun"):
            try:
                do_usuniecia.append((int(z["d"]), int(z["p"])))
            except (KeyError, ValueError, TypeError):
                pass
            continue
        try:
            p = dane["dzialy"][int(z["d"])]["pozycje"][int(z["p"])]
        except (KeyError, IndexError, ValueError, TypeError):
            continue
        if str(z.get("opis", "")).strip():
            p["opis"] = str(z["opis"]).strip()[:500]
        try:
            nowe = {k: S.MO.liczba_pl(z[k]) for k in ("wartosc", "cena", "ilosc") if z.get(k) not in (None, "")}
        except ValueError:
            return jsonify({"blad": f"Nieprawidłowa liczba w pozycji: {str(p.get('opis', ''))[:50]} (np. 1 234,50)"}), 400
        if any(v < 0 for v in nowe.values()):
            return jsonify({"blad": f"Cena, wartość i ilość nie mogą być ujemne: {str(p.get('opis', ''))[:50]}"}), 400
        if "wartosc" in nowe:
            w = nowe["wartosc"]
            p["cena"] = round(w / float(p.get("ilosc") or 1), 2) if float(p.get("ilosc") or 0) else w
        elif "cena" in nowe:
            p["cena"] = S.MO.zaokr(nowe["cena"])
        if "ilosc" in nowe:
            p["ilosc"] = nowe["ilosc"]
        if "wartosc" in nowe or "cena" in nowe:  # cena wpisana ręcznie – stała przy korekcie ceny oferty (karta W6 §4)
            p["zrodlo"] = "poprawione ręcznie"
        ile += 1
    for di, pi in sorted(set(do_usuniecia), reverse=True):  # usuwanie całych pozycji (od końca, żeby nie przesuwać numerów)
        try:
            del dane["dzialy"][di]["pozycje"][pi]
            ile += 1
        except (IndexError, KeyError):
            pass
    dane["dzialy"] = [dz for dz in dane.get("dzialy", []) if dz.get("pozycje")]
    if not ile:
        return jsonify({"blad": "Zaznacz pozycje i wpisz zmiany albo wybierz pozycje do usunięcia."}), 400
    if not dane["dzialy"]:
        return jsonify({"blad": "Nie można usunąć wszystkich pozycji – kosztorys musi mieć co najmniej jedną pozycję."}), 400
    for k in ("netto", "vat_kwota", "brutto"):
        dane.pop(k, None)
    dane = S.MO.przelicz(dane)
    S.pisz(os.path.join(d, "oferta_dane_oryginal.json"), dane)  # poprawiony kosztorys = nowa baza (także dla „Dostosuj cenę”)
    if kor and zgodny:
        blad = S.zastosuj_korekte(pid, dane, kor.get("tryb"), kor.get("wartosc"))
        if blad:  # np. cena docelowa niższa niż suma pozycji poprawionych – nic nie zmieniono
            S.pisz(os.path.join(d, "oferta_dane_oryginal.json"), orig_kopia)
            return jsonify({"blad": blad + " Zmian pozycji nie zapisano."}), 400
    else:
        S.zapisz_oferte(pid, dane, S.cfg())
    m = S.meta(pid)
    return jsonify({"poprawiono": ile - len(set(do_usuniecia)), "usunieto": len(set(do_usuniecia)), "oferta": m.get("oferta")})


def pliki_dok(pid, z, did, faza="rozliczenie"):
    k = S.kat_dok(pid, z, did, faza)
    return sorted(f for f in os.listdir(k)) if os.path.isdir(k) else []


def pliki_z_html(h, baza):
    """Linki do dokumentów (regulamin, wzory, załączniki) na stronie naboru – z rozszerzeniem w adresie albo rozpoznane po adresie
    pobierania (np. gov.pl/attachment/…) i opisie linku („PDF, 312 kB”)."""
    wyn, widz = [], set()
    for u, t in S.linki_html(h, baza):
        p = S.urllib.parse.urlparse(u)
        sciezka = p.path.lower()
        plik = sciezka.endswith(S.ROZSZ_DOK) or S.WZOR_PLIKU_BEZ_ROZSZ.search(p.path + "?" + p.query) or \
            (S.WZOR_TEKSTU_PLIKU.search(t or "") and not sciezka.endswith((".html", ".htm")))
        if plik and u not in widz and p.scheme in ("http", "https"):
            widz.add(u)
            wyn.append({"nazwa": (t or S.urllib.parse.unquote(os.path.basename(sciezka)) or "dokument")[:150], "url": u})
    return wyn


@bp.get("/api/projekty/<pid>/plan")
@S.wymaga_logowania
def plan_pobierz(pid):
    return jsonify(S._plan_stan(pid, S.meta(pid)))


@bp.post("/api/projekty/<pid>/plan")
@S.wymaga_logowania
def plan_zapisz(pid):
    j = request.json or {}
    if "pozycje" in j and not isinstance(j.get("pozycje"), list):
        return jsonify({"blad": "Nieprawidłowe dane: pozycje planu."}), 400
    pp = None
    if isinstance(j.get("pozycje"), list):  # GC-03: kontrola przed zapisem – błędny wpis (atrybuty, „abc”, „1e400”, ujemne) nie blokuje planu
        pp = []
        for x in j["pozycje"][:200]:
            if isinstance(x, dict) and x.get("kategoria") in S.DP.KATALOG:
                q = {k: x.get(k) for k in ("id", "nazwa", "kategoria", "dzialanie", "atrybuty", "ilosc", "cena_netto", "vat", "kwalifikowalna",
                                           "zrodlo_ceny", "miesiac_od", "miesiac_do", "osiagniete", "cpv")}
                if q["cpv"] not in (None, ""):  # H3-05: kod CPV – grupowanie tożsamych zamówień przy wyborze wykonawcy
                    m_ = re.fullmatch(r"\s*(\d{8})(?:-(\d))?\s*", str(q["cpv"]))
                    if not m_:
                        return jsonify({"blad": f"„{q['nazwa'] or 'pozycja'}”: kod CPV – 8 cyfr, np. 45321000-3 (wpisano „{str(q['cpv'])[:30]}”)."}), 400
                    q["cpv"] = m_.group(1) + (f"-{m_.group(2)}" if m_.group(2) else "")
                else:
                    q.pop("cpv")
                q["id"] = S.DOT.bezpieczna(q["id"])[:20] if q["id"] else uuid.uuid4().hex[:8]
                q["nazwa"] = str(q["nazwa"] or "")[:300]
                q["atrybuty"] = {str(k)[:40]: (v if isinstance(v, (str, int, float, bool)) else [str(y)[:200] for y in v][:30] if isinstance(v, list) else "")
                                 for k, v in (q["atrybuty"] if isinstance(q["atrybuty"], dict) else {}).items()}
                for k, et, mx in (("ilosc", "Ilość", 1e7), ("cena_netto", "Cena jednostkowa netto", 1e11), ("vat", "VAT [%]", 100),
                                  ("miesiac_od", "Miesiąc od", 120), ("miesiac_do", "Miesiąc do", 120)):
                    if q[k] in (None, ""):
                        continue
                    v = S.DP.liczba(q[k], None)
                    if v is None or v != v or v < 0 or v > mx:
                        return jsonify({"blad": f"„{q['nazwa'] or 'pozycja'}”: {et} – podaj liczbę od 0 do {S.PR.liczba_pl(mx, 0)} (wpisano „{str(q[k])[:30]}”)."}), 400
                pp.append(q)
    with S.BLOKADA:
        m = S.meta(pid)
        p = S._plan(m)
        if pp is not None:
            p["pozycje"] = pp
        for k in ("pomysl", "data_konca"):
            if k in j:
                p[k] = str(j[k] or "")[:2000]
        if isinstance(j.get("reczne"), dict):
            p.setdefault("reczne", {}).update({k: v for k, v in j["reczne"].items() if k in ("intensywnosc_procent", "limit_projektu_zl", "min_koszty_zl",
                                                                                             "max_koszty_zl", "trwalosc_lat", "vat_kwalifikowalny")})
        if isinstance(j.get("wskazniki_osiagniete"), dict):
            p.setdefault("wskazniki_osiagniete", {}).update(j["wskazniki_osiagniete"])
        S.zapisz_meta(pid, m)
    if isinstance(j.get("profil"), dict):  # profil wnioskodawcy do dotacji – wspólny dla wszystkich wniosków konta
        prof = dict(S.cfg().get("dotacje_profil") or {})
        prof.update({k: str(v)[:200] for k, v in j["profil"].items()})
        S.zapisz_ustawienia({"dotacje_profil": prof})
    return jsonify(S._plan_stan(pid, S.meta(pid)))


@bp.post("/api/projekty/<pid>/plan/analiza")
@S.wymaga_logowania
def plan_analiza(pid):
    S.meta(pid)
    return jsonify(S.uruchom("dotacja", "Analiza naboru – co można sfinansować", S.praca_plan_analiza, pid))


@bp.post("/api/projekty/<pid>/plan/wycena")
@S.wymaga_logowania
def plan_wycena(pid):
    S.meta(pid)
    return jsonify(S.uruchom("dotacja", "Wycena pozycji projektu (ceny rynkowe)", S.praca_plan_wycena, pid, list((request.json or {}).get("ids") or [])))


@bp.post("/api/projekty/<pid>/plan/kontrola")
@S.wymaga_logowania
def plan_kontrola(pid):
    S.meta(pid)
    return jsonify(S.uruchom("dotacja", "Kontrola projektu z regulaminem i punktacją", S.praca_plan_kontrola, pid))


@bp.get("/api/projekty/<pid>/plan/xlsx")
@S.wymaga_logowania
def plan_xlsx(pid):
    m = S.meta(pid)
    st = S._plan_stan(pid, m)
    sc = os.path.join(S.pdir(pid), "Zestawienie_rzeczowo-finansowe.xlsx")
    S.DP.budzet_xlsx(sc, st["plan"], st["budzet"], st["wskazniki"], st["harmonogram"], m.get("nazwa") or "")
    return send_file(sc, as_attachment=True, download_name="Zestawienie_rzeczowo-finansowe.xlsx")


@bp.post("/api/projekty/<pid>/plan/kosztorys")
@S.wymaga_logowania
def plan_kosztorys(pid):
    """Pozycja robót → nowy projekt w Kosztorysowaniu z opisem z formularza (wycena z kosztorysu)."""
    j = request.json or {}
    m = S.meta(pid)
    x = next((q for q in S._plan(m).get("pozycje") or [] if q.get("id") == j.get("id")), None)
    if not x:
        return jsonify({"blad": "Nie ma takiej pozycji."}), 404
    kid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, kid, "dokumenty"))
    a = x.get("atrybuty") or {}
    opis = f"{x.get('nazwa')}. Obiekt: {a.get('obiekt', '')}. Zakres: {', '.join(a.get('zakres') or [])}. Powierzchnia: {a.get('powierzchnia', '')} m². Rok budowy: {a.get('rok_budowy', '')}."
    S.zapisz_meta(kid, {"id": kid, "nazwa": ("Dotacja – " + (x.get("nazwa") or ""))[:100], "typ": "kosztorys", "strona": "kosztorysant",
                      "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wlasciciel": S.konto_biezace(), "pominiete": [],
                      "opis_kosztorysu": opis, "z_dotacji": {"projekt": pid, "pozycja": x.get("id")}})
    with open(os.path.join(S.PROJ, kid, "dokumenty", "Opis_zakresu_robot.txt"), "w", encoding="utf-8") as f:
        f.write(opis + "\n\nPrzygotuj kosztorys robót dla tego zakresu (ceny rynkowe).")
    return jsonify({"id": kid})


@bp.post("/api/projekty/<pid>/plan/do-rozliczenia")
@S.wymaga_logowania
def plan_do_rozliczenia(pid):
    """Dotacja przyznana: nowy projekt rozliczenia z planem (pozycje, wskaźniki, harmonogram) i wyborem wykonawców."""
    m = S.meta(pid)
    if m.get("rozliczenie_id") and os.path.isdir(S.pdir(m["rozliczenie_id"])):
        return jsonify({"id": m["rozliczenie_id"]})
    rid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, rid, "dokumenty"))
    for f in os.listdir(os.path.join(S.pdir(pid), "dokumenty")):  # regulamin i wniosek przydają się przy rozliczeniu
        sp = os.path.join(S.pdir(pid), "dokumenty", f)
        if os.path.isfile(sp):
            S.shutil.copy2(sp, os.path.join(S.PROJ, rid, "dokumenty", f))
    plan = json.loads(json.dumps(S._plan(m)))
    plan.pop("kontrola", None)
    nab = S._dot(m, "wniosek").get("nabor") or {}
    S.zapisz_meta(rid, {"id": rid, "nazwa": m.get("nazwa"), "typ": "dotacja", "strona": "dotacje", "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                      "wlasciciel": m.get("wlasciciel") or S.konto_biezace(), "pominiete": [], "wniosek_id": pid,
                      "dotacja": {"dane": {"program": nab.get("program") or "", "beneficjent": S.cfg().get("firma_nazwa", ""), "opis": (m.get("nazwa") or "")},
                                  "wymagania": None, "zakres": "", "dokumenty": {}, "plan": plan}})
    with S.BLOKADA:
        m = S.meta(pid)
        m["rozliczenie_id"] = rid
        S.zapisz_meta(pid, m)
    return jsonify({"id": rid})


@bp.post("/api/projekty/<pid>/plan/zapytanie")
@S.wymaga_logowania
def plan_zapytanie(pid):
    """Pozycja wymagająca zasady konkurencyjności → zapytanie ofertowe powiązane z projektem dotacji, z danymi pozycji."""
    j = request.json or {}
    m = S.meta(pid)
    x = next((q for q in S._plan(m).get("pozycje") or [] if q.get("id") == j.get("id")), None)
    if not x:
        return jsonify({"blad": "Nie ma takiej pozycji."}), 404
    zid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, zid, "dokumenty"))
    kat = S.DP.KATALOG.get(x.get("kategoria"), {})
    rodz = "roboty" if x.get("kategoria") == "roboty" else "uslugi" if x.get("kategoria") in ("uslugi", "szkolenia", "miekkie", "promocja") else "dostawy"
    S.zapisz_meta(zid, {"id": zid, "nazwa": (x.get("nazwa") or "Zapytanie ofertowe")[:90], "typ": "zapytanie", "strona": "dotacje",
                      "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wlasciciel": S.konto_biezace(), "pominiete": [],
                      "zapytanie": {"dane": {"przedmiot": x.get("nazwa"), "rodzaj": rodz, "wartosc_netto": str(round(S.DP._f(x.get("ilosc") or 1) * S.DP._f(x.get("cena_netto")), 2)),
                                             "opis": f"{kat.get('nazwa', '')}: " + "; ".join(f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in (x.get("atrybuty") or {}).items() if v)
                                             + f". Ilość: {x.get('ilosc') or 1}.", "beneficjent": S.cfg().get("firma_nazwa", ""),
                                             "data_szacowania": dt.date.today().isoformat(), "zamawiajacy_pzp": (S.cfg().get("dotacje_profil") or {}).get("typ") in ("jst", "szkola")},
                                    "dotacja_id": pid if m.get("typ") == "dotacja" else (m.get("rozliczenie_id") or ""), "publikacja": {}, "lista": {}}})
    with S.BLOKADA:
        m = S.meta(pid)
        p = S._plan(m)
        p.setdefault("zapytania_poz", []).append({"pozycja": x.get("id"), "id": zid})
        if m.get("typ") == "dotacja":
            m.setdefault("zapytania", []).append(zid)
        S.zapisz_meta(pid, m)
    return jsonify({"id": zid})


def hurtownie_wybrane(c, idx):
    h = c.get("hurtownie", [])
    return [h[i] for i in idx if 0 <= i < len(h)]


@bp.post("/api/projekty/<pid>/zamowienie/podglad")
@S.wymaga_logowania
def zam_podglad(pid):
    c = S.cfg()
    try:
        h, k, etap = S.dane_zamowienia(pid, request.json)
    except (ValueError, IndexError) as e:
        return jsonify({"blad": str(e)}), 400
    wyn = []
    for hurt in hurtownie_wybrane(c, request.json.get("hurtownie", [])):
        mats = S.MH.materialy_dla(h, k, hurt)
        if not mats:
            wyn.append({"hurtownia": hurt["nazwa"], "email": hurt["email"], "pusto": True})
            continue
        temat, tekst, _ = S.MH.tresc_maila(h, etap, hurt, mats, request.json.get("typ", "zapytanie"), c,
                                        request.json.get("dopisek", ""), request.json.get("termin", ""))
        wyn.append({"hurtownia": hurt["nazwa"], "email": hurt["email"], "temat": temat, "tekst": tekst, "n": len(mats)})
    return jsonify(wyn)


@bp.post("/api/projekty/<pid>/zamowienie/wyslij")
@S.wymaga_logowania
def zam_wyslij(pid):
    c = S.cfg()
    p = request.json
    try:
        h, k, etap = S.dane_zamowienia(pid, p)
    except (ValueError, IndexError) as e:
        return jsonify({"blad": str(e)}), 400
    if not h.get("adres"):
        return jsonify({"blad": "Uzupełnij adres dostawy."}), 400
    typ, sposob = p.get("typ", "zapytanie"), p.get("sposob", "eml")
    folder = os.path.join(S.pdir(pid), "zamowienia")
    os.makedirs(folder, exist_ok=True)
    paczki = []
    for hurt in hurtownie_wybrane(c, p.get("hurtownie", [])):
        mats = S.MH.materialy_dla(h, k, hurt)
        if not mats:
            continue
        nh = re.sub(r"[^\w\-]+", "_", hurt["nazwa"])[:40]
        nb = re.sub(r"[^\w\-]+", "_", h.get("budowa", ""))[:40]
        zal = os.path.join(folder, f"{'Zamowienie' if typ == 'zamowienie' else 'Zapytanie'}_{nb}_etap{etap['nr']}_{nh}.xlsx")
        S.MH.zapisz_zalacznik(zal, h, etap, hurt, mats, typ, c)
        temat, tekst, htm = S.MH.tresc_maila(h, etap, hurt, mats, typ, c, p.get("dopisek", ""), p.get("termin", ""))
        paczki.append((hurt, mats, S.MH.zbuduj_wiadomosc(c, hurt, temat, tekst, htm, zal, sposob == "eml"), zal))
    if not paczki:
        return jsonify({"blad": "Żadna z zaznaczonych hurtowni nie ma materiałów w tym etapie."}), 400
    linki = []
    if sposob == "smtp":
        try:
            S.MH.wyslij_smtp(c, [x[2] for x in paczki])
        except Exception as e:
            return jsonify({"blad": f"Nie udało się wysłać: {e}"}), 400
    else:
        for hurt, mats, msg, zal in paczki:
            eml = os.path.splitext(zal)[0] + ".eml"
            with open(eml, "wb") as f:
                f.write(bytes(msg))
            linki.append({"hurtownia": hurt["nazwa"],
                          "url": f"/pobierz/{pid}/zamowienia/{os.path.basename(eml)}"})
    hist = S.czytaj(S.F_HIST, [])
    for hurt, mats, _, _ in paczki:
        hist.insert(0, {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "budowa": h.get("budowa", ""),
                        "etap": etap["nr"], "typ": "zamówienie" if typ == "zamowienie" else "zapytanie ofertowe",
                        "hurt": hurt["nazwa"], "sposob": "SMTP" if sposob == "smtp" else "szkic .eml", "n": len(mats),
                        "projekt": pid, "kto": session.get("login", "")})
    S.pisz(S.F_HIST, hist[:1000])
    return jsonify({"wyslane": len(paczki), "linki": linki})


@bp.get("/api/hurtownie")
@S.wymaga_logowania
def hurtownie():
    return jsonify(S.cfg().get("hurtownie", []))


@bp.post("/api/hurtownie")
@S.wymaga_logowania
def hurtownie_zapisz():
    lista, zle = [], []
    for h in (request.json or {}).get("hurtownie", []):
        h = {k: str(h.get(k, "")).strip() for k in ("nazwa", "email", "osoba", "kategorie", "uwagi")}
        if not h["nazwa"] and not h["email"]:
            continue  # pusty wiersz
        if h["nazwa"] and re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", h["email"]):
            lista.append(h)
        else:
            zle.append(h["nazwa"] or h["email"])
    if zle:  # bez cichego gubienia wpisanej hurtowni – zamówienia i zapytania idą e-mailem
        return jsonify({"blad": "Uzupełnij nazwę i poprawny adres e-mail hurtowni: " + ", ".join(zle[:5]) + ". Nic nie zapisano."}), 400
    with S.BLOKADA:
        S.zapisz_ustawienia({"hurtownie": lista})
    return jsonify(lista)


@bp.post("/api/projekty/<pid>/wykonawca/pliki")
@S.wymaga_logowania
def wykonawca_dodaj(pid):
    d = os.path.join(S.pdir(pid), "dokumenty_wykonawcy")
    os.makedirs(d, exist_ok=True)
    for f in request.files.getlist("pliki"):
        f.save(os.path.join(d, S.secure_filename_pl(f.filename)))
    return jsonify(pliki_wykonawcy(pid))


@bp.post("/api/projekty/<pid>/wykonawca/sprawdz")
@S.wymaga_logowania
def wykonawca_sprawdz(pid):
    m = S.meta(pid)
    spr = set(m.get("sprawdzone_wykonawcy", []))
    for n in _napisy(request.json.get("nazwy", [])):
        (spr.add if request.json.get("sprawdzony", True) else spr.discard)(n)
    m["sprawdzone_wykonawcy"] = sorted(spr)
    S.zapisz_meta(pid, m)
    return jsonify(pliki_wykonawcy(pid))


@bp.post("/api/projekty/<pid>/wykonawca/usun")
@S.wymaga_logowania
def wykonawca_usun(pid):
    d = os.path.join(S.pdir(pid), "dokumenty_wykonawcy")
    for n in _napisy(request.json.get("nazwy")) or (os.listdir(d) if os.path.isdir(d) else []):
        p = os.path.join(d, os.path.basename(n))
        if os.path.isfile(p):
            S.archiwizuj_plik(pid, p)
    return jsonify(pliki_wykonawcy(pid))


def pliki_budowy(pid):
    d = S.pdir(pid)
    grupy = []
    for kat, tytul in (("", "Kosztorys, oferta i opracowania"), ("dokumenty", "Dokumenty projektu / przetargu"),
                       ("dokumenty_wykonawcy", "Dokumenty wykonawcy"), ("realizacja/dokumenty", "Dokumenty budowy"),
                       ("realizacja/protokoly", "Protokoły odbioru"), ("zamowienia", "Zamówienia")):
        k = os.path.join(d, kat)
        if not os.path.isdir(k):
            continue
        if kat == "":
            lista = [n for n in S.wyniki(pid)]
        else:
            lista = [os.path.relpath(os.path.join(r, n), d).replace(os.sep, "/") for r, _, ns in os.walk(k) for n in sorted(ns)
                     if not n.endswith(".eml")]
        if lista:
            grupy.append({"tytul": tytul, "pliki": [{"sciezka": x, "nazwa": os.path.basename(x)} for x in lista],
                          "kat": kat})
    return grupy


@bp.post("/api/projekty/<pid>/wykonawca/z-profilu")
@S.wymaga_logowania
def wykonawca_z_profilu(pid):
    """Kopiuje wybrane dokumenty z Profilu firmy (polisa, referencje, certyfikaty) do dokumentów wykonawcy projektu."""
    d = os.path.join(S.pdir(pid), "dokumenty_wykonawcy")
    os.makedirs(d, exist_ok=True)
    ile = 0
    for n in (request.json or {}).get("pliki", []):
        src = os.path.join(S.DIR_FIRMA, os.path.basename(n))
        if os.path.isfile(src):
            S.shutil.copy2(src, os.path.join(d, os.path.basename(n).split("_", 1)[-1]))
            ile += 1
    return jsonify({"skopiowano": ile, "pliki": pliki_wykonawcy(pid)})


@bp.post("/api/projekty/<pid>/zdjecia")
@S.wymaga_logowania
def zdjecia_dodaj(pid):
    data = request.form.get("data") or dt.date.today().isoformat()
    try:
        dt.date.fromisoformat(data)
    except ValueError:
        return jsonify({"blad": "Nieprawidłowa data zdjęć."}), 400
    opis = str(request.form.get("opis", ""))[:300]
    with S.BLOKADA:
        r = S.realizacja_pelna(pid)
        nowe, pominiete = [], []
        for f in request.files.getlist("pliki"):
            zid = uuid.uuid4().hex[:12]
            try:
                plik, mini = S.BUD.zapisz_zdjecie(f, S.folder_zdjec(pid), zid)
            except ValueError as e:
                pominiete.append(str(e))
                continue
            z = {"id": zid, "plik": plik, "miniatura": mini, "data": data, "opis": opis, "kto": session.get("login", ""),
                 "dodano": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
            r["zdjecia"].append(z)
            nowe.append(z)
        S.zapisz_realizacje(pid, r)
    if pominiete and not nowe:
        return jsonify({"blad": " ".join(pominiete[:3])}), 400
    return jsonify(nowe)


@bp.post("/api/projekty/<pid>/zdjecia/zmien")
@S.wymaga_logowania
def zdjecia_zmien(pid):
    j = request.json
    with S.BLOKADA:
        r = S.realizacja_pelna(pid)
        z = next((x for x in r["zdjecia"] if x["id"] == j.get("id")), None)
        if not z:
            return jsonify({"blad": "Nie ma takiego zdjęcia."}), 404
        if j.get("usun"):  # zdjęcie trafia do archiwum
            z["archiwum"] = True
            z["archiwum_data"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        else:
            if "opis" in j:
                z["opis"] = str(j["opis"])[:300]
            if j.get("data"):
                try:
                    z["data"] = dt.date.fromisoformat(str(j["data"])).isoformat()
                except ValueError:
                    return jsonify({"blad": "Nieprawidłowa data zdjęcia."}), 400
        S.zapisz_realizacje(pid, r)
    return jsonify({"ok": True})
