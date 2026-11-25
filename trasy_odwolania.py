# -*- coding: utf-8 -*-
"""
Odwołania od przetargów (moduł właściciela) – trasy: wyszukiwanie rozstrzygnięć, analiza szans (AI), kontakty, oferty dla wykonawców.
Blueprint „odwolania” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("odwolania", __name__)


def _odw_dokumenty_platformy(url):
    """Platforma zakupowa (bez BIP): odnośniki do plików na stronie postępowania – (adres, opis). Z ciasteczkami (platformy przekierowują bez nich w kółko)."""
    import html as _h
    import http.cookiejar
    op_ = S.urllib.request.build_opener(S.urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    with op_.open(S.urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Bidivia", "Accept": "text/html"}), timeout=40) as r:
        strona = r.read(5_000_000).decode("utf-8", "replace")
    wyn = []
    for href, txt in re.findall(r"""(?is)<a\b[^>]*?href\s*=\s*["']([^"'#]+)["'][^>]*>(.*?)</a>""", strona):
        a = S.urllib.parse.urljoin(url, _h.unescape(href.strip()))
        opis = re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", txt))).strip()
        if a.startswith("http") and (S.BZ.RE_PLIK.search(a) or S.BZ.RE_POBIERZ.search(a) or S.BZ.RE_TYP_W_OPISIE.search(opis)):
            wyn.append({"url": a, "nazwa": opis or os.path.basename(S.urllib.parse.urlparse(a).path)})
    if not wyn and re.search(r"(?i)zaloguj|logowanie|login", strona):
        raise RuntimeError("platforma wymaga logowania – dokumenty niedostępne publicznie")
    pol = {}  # ten sam plik bywa podlinkowany kilka razy (ikona z nazwą techniczną + opis) – zostaje opisowa nazwa
    for d in wyn:
        stary = pol.get(d["url"])
        if not stary or (S.OP.rodzaj_dokumentu(d["nazwa"]) and not S.OP.rodzaj_dokumentu(stary["nazwa"])) or \
                (re.fullmatch(r"[0-9a-f]{16,}\.\w+", stary["nazwa"]) and not re.fullmatch(r"[0-9a-f]{16,}\.\w+", d["nazwa"])):
            pol[d["url"]] = d
    return list(pol.values())


def _odw_kontakty(B, oceny, log=None):
    """Dane oferentów z rejestrów i strony www – zapamiętywane na 30 dni (B/kontakty.json)."""
    with S.OP.BLOKADA:
        K = B.czytaj("kontakty.json", {})
    zm = False
    for o in oceny:
        for f in o.get("oferenci") or []:
            k, nowe = S.kontakt_firmy(f.get("nip"), K, log, f.get("wykonawca", ""))
            if k:
                f["rejestr"] = k
                zm = zm or nowe
    if zm:
        with S.OP.BLOKADA:
            B.pisz("kontakty.json", {**B.czytaj("kontakty.json", {}), **K})


def odw_unijne_auto(nr, rec):
    """Reżim z danych źródła: TED albo e-Zamówienia („isTenderAmountBelowEU” = false) → od progów UE. Postępowanie dodane z linku platformy
    (bez e-Zamówień) – wartość nieznana, przyjmowane „poniżej progów” do czasu ręcznego ustawienia."""
    if str(nr).startswith("TED "):
        return True, "ogłoszenie w TED (Dziennik Urzędowy UE)"
    pp = (rec.get("ez") or {}).get("ponizej_progow_ue")
    if pp is False:
        return True, "e-Zamówienia: wartość równa lub przekraczająca progi UE"
    if pp is True:
        return False, "e-Zamówienia: wartość poniżej progów UE"
    if str(nr).startswith("LINK-") or rec.get("z_linku") and not rec.get("ocds"):
        return False, "nieznany (postępowanie z linku platformy) – przyjęto poniżej progów UE; ustaw ręcznie"
    return False, "ogłoszenie w BZP – przyjęto poniżej progów UE"


def odw_unijne(nr, rec):
    """(unijne, opis źródła) – ręczne ustawienie użytkownika (rec["unijne_reczne"]: True/False) ma pierwszeństwo przed automatem."""
    r = rec.get("unijne_reczne")
    if isinstance(r, bool):
        return r, "ustawione ręcznie: " + ("równa lub przekracza progi UE" if r else "poniżej progów UE")
    return odw_unijne_auto(nr, rec)


def klucz_czesci(cz):
    return str((cz or {}).get("czesc") or "")


def odw_ocen(B, nr, rec, prog, log=None, z_siecia=False):
    """Ocena części z danych odczytanych (rec["dane"]) – bez AI. z_siecia: biała lista VAT i kontakty z rejestrów (przy sprawdzaniu);
    bez sieci (zmiana reżimu / daty przekazania) – dane z rejestrów przenoszone z poprzedniej oceny."""
    poprz = {klucz_czesci(o): o for o in rec.get("ocena") or []}
    unijne_, _ = odw_unijne(nr, rec)
    oceny = []
    for cz in rec["dane"].get("czesci") or []:
        st = poprz.get(klucz_czesci(cz)) or {}
        wyb = next((r for r in ((cz.get("wybor") or {}).get("ranking") or []) if S.OP._ten_sam(r.get("wykonawca"), (cz.get("wybor") or {}).get("wybrany"))), None)
        if z_siecia:
            vat = S.OP.status_vat_nip((wyb or {}).get("nip")) if wyb and (wyb or {}).get("nip") else None
        else:
            vat = st.get("status_vat_wybranego")
        o = S.OP.ocen_czesc(cz, prog, rec.get("termin_ofert"), vat, unijne_, None, (rec.get("przekazanie") or {}).get(klucz_czesci(cz)),
                            rec.get("rodzaj_przedmiotu"))
        o["czesc"] = cz.get("czesc")
        o["status_vat_wybranego"] = vat
        stare_f = {f.get("wykonawca"): f for f in st.get("firmy") or []}
        stare_o = {f.get("wykonawca"): f for f in st.get("oferenci") or []}
        for f in o["firmy"]:  # dane firm z białej listy VAT
            if not z_siecia:
                if stare_f.get(f.get("wykonawca"), {}).get("biala_lista"):
                    f["biala_lista"] = stare_f[f["wykonawca"]]["biala_lista"]
                continue
            if f.get("nip") and len(re.sub(r"\D", "", str(f["nip"]))) == 10:
                try:
                    r_ = S.urllib.request.urlopen(S.urllib.request.Request(f"https://wl-api.mf.gov.pl/api/search/nip/{re.sub(r'\D', '', str(f['nip']))}?date={dt.date.today().isoformat()}",
                                                                       headers={"User-Agent": "Bidivia"}), timeout=20)
                    s_ = (json.loads(r_.read().decode("utf-8")).get("result") or {}).get("subject") or {}
                    f["biala_lista"] = {k: s_.get(k) for k in ("name", "statusVat", "workingAddress", "residenceAddress", "krs", "regon")}
                except Exception:
                    pass
        if not z_siecia:
            for f in o.get("oferenci") or []:
                if stare_o.get(f.get("wykonawca"), {}).get("rejestr"):
                    f["rejestr"] = stare_o[f["wykonawca"]]["rejestr"]
        oceny.append(o)
    if z_siecia:
        _odw_kontakty(B, oceny, log)
    rec["ocena"] = oceny
    st = sorted([o["status"] for o in oceny] or ["czeka na informację z otwarcia ofert"], key=lambda x: S.KOLEJNOSC_ODW.get(x, 5))
    rec["status"] = st[0]
    dni = [o.get("dni_do_terminu") for o in oceny if o.get("dni_do_terminu") is not None]
    rec["dni_do_terminu"] = (min(d for d in dni if d >= 0) if any(d >= 0 for d in dni) else max(dni)) if dni else None
    rec["sila"] = next((o.get("sila") for o in oceny if o.get("sila")), "")


def _odw_jedno(log, c, B, nr, rec, prog):
    """Jedno postępowanie: nowe dokumenty rozstrzygnięcia → pobranie → odczyt AI → ocena (bez AI)."""
    folder = os.path.join(B.pliki, S.OP.bezpieczny(nr))
    rec["katalog"] = S.OP.bezpieczny(nr)  # bezpieczna nazwa do adresów plików (numer BZP zawiera „/”)
    znane = {d["url"] for d in rec.get("dokumenty") or []}
    nowe = []
    if rec.get("ocds"):  # stan postępowania z e-Zamówień – także gdy prowadzone na innej platformie
        try:
            rec["ez"] = S.OP.stan_ez(rec["ocds"])
        except Exception as e:
            rec.setdefault("ez", {})["blad"] = str(e)[:120]
        ez = rec.get("ez") or {}
        if ez.get("wojewodztwo") and not rec.get("wojewodztwo"):
            rec["wojewodztwo"] = ez["wojewodztwo"]
        if ez.get("etap") == "CompletedContract" and not rec.get("ocena"):  # umowa zawarta (API wpisuje wtedy też cancellationDate – to data zamknięcia)
            rec["status"], rec["koniec_obserwacji"] = "umowa zawarta – po terminie odwołania", True
            rec["sprawdzono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            return
        if ez.get("stan") == "Invalidated" or "Invalid" in str(ez.get("etap")):
            rec["status"], rec["koniec_obserwacji"] = "unieważnione", True
            rec["sprawdzono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            return
        if ez.get("kwota") and ez["kwota"] < prog:
            rec["status"], rec["koniec_obserwacji"] = "poniżej progu wartości", True
            rec["sprawdzono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            return
    if rec.get("ocds") and (rec.get("ez") or {}).get("na_platformie", True):
        for d in S.OP.dokumenty_ocds(rec["ocds"], od_n=(rec.get("ostatni_n") or 0) + 1):
            rec["ostatni_n"] = max(rec.get("ostatni_n") or 0, d["n"])
            if d["url"] not in znane:
                d["rodzaj"] = S.OP.rodzaj_dokumentu(d["nazwa"])
                rec.setdefault("dokumenty", []).append(d)
                if d["rodzaj"]:
                    nowe.append(d)
    if not (rec.get("ocds") and (rec.get("ez") or {}).get("na_platformie", True)) or not rec.get("dokumenty"):
        for url in (rec.get("platformy") or [])[:2]:  # platforma zamawiającego z ogłoszenia (platformazakupowa.pl, ezamawiajacy.pl, …)
            if S.OP.RE_PROFIL_OGOLNY.search(url):
                rec["blad_platformy"] = (f"Ogłoszenie podaje tylko ogólny adres zamawiającego na platformie ({url}), nie stronę tego postępowania – "
                                         "wklej link do postępowania w „Dodaj postępowanie z linku”.")
                continue
            try:
                lista_ = _odw_dokumenty_platformy(url)
            except Exception as e:
                rec["blad_platformy"] = f"{url}: {str(e)[:100]}"
                continue
            rec.pop("blad_platformy", None)
            for d in lista_:
                if d["url"] not in znane:
                    d["rodzaj"] = S.OP.rodzaj_dokumentu(d["nazwa"])
                    rec.setdefault("dokumenty", []).append(d)
                    znane.add(d["url"])
                    if d["rodzaj"]:
                        nowe.append(d)
    for d in [x for x in rec.get("dokumenty") or [] if not x.get("rodzaj") and not x.get("tresc_sprawdzona") and S.OP.do_sprawdzenia_tresci(x["nazwa"])]:
        d["tresc_sprawdzona"] = True  # nieopisowa nazwa (np. GUID) – rozpoznanie po treści pierwszych stron
        p = S.BZ._zapisz(d["url"], folder, d["nazwa"] if "." in d["nazwa"][-6:] else d["nazwa"] + ".pdf")
        if p:
            try:
                b_, _, _ = S.MO.przygotuj_blok_tekstowy(p)
                tekst = " ".join(x.get("text", "") or (x.get("source") or {}).get("data", "") for x in b_ if isinstance(x, dict))
            except Exception:
                tekst = ""
            d["rodzaj"] = S.OP.rodzaj_z_tresci(tekst)
            if d["rodzaj"]:
                d["plik"] = os.path.basename(p)
                d["rozpoznano_po_tresci"] = True
                nowe.append(d)
            else:
                os.remove(p)
    if rec.pop("wymus_odczyt", False):  # „Analizuj ponownie”: wszystkie dokumenty rozstrzygnięcia jeszcze raz do odczytu
        nowe += [d for d in rec.get("dokumenty") or [] if d.get("rodzaj") and d not in nowe]
    for d in nowe:
        if not d.get("plik"):
            p = S.BZ._zapisz(d["url"], folder, d["nazwa"] if "." in d["nazwa"][-6:] else d["nazwa"] + ".pdf")
            d["plik"] = os.path.basename(p) if p else None
        log(f"   {rec.get('przedmiot', '')[:60]}: nowy dokument „{d['nazwa'][:70]}” ({d['rodzaj']}{', rozpoznany po treści' if d.get('rozpoznano_po_tresci') else ''})")
    if nowe:
        bloki = []
        for d in rec.get("dokumenty") or []:
            if d.get("rodzaj") and d.get("plik"):
                b_, _, _ = S.MO.przygotuj_blok_tekstowy(os.path.join(folder, d["plik"]))
                bloki += b_
        if bloki:
            c2 = dict(c, _model=c.get("model_oferty") or "claude-sonnet-5-5", _log=log)
            rec["dane"] = S.ai_dane(c2, S.OP.SYSTEM_ODCZYT, S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c2)) + [{"type": "text", "text": S.OP.POLECENIE_ODCZYT}],
                                  12000, log, lambda t: S.MO.wyciagnij_json(t) or {})
            rec["odczytano"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    if rec.get("dane"):
        odw_ocen(B, nr, rec, prog, log, z_siecia=True)
    else:
        rec["status"] = "obserwowany"
    rec["sprawdzono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    rec.pop("blad", None)


def _odw_filtr(c, ust):
    """Filtr wyszukiwarki modułu: region (jak w wyszukiwarce przetargów / województwa / cała Polska), rodzaj zamówienia, słowa."""
    w = ust.get("wyszukiwanie") or S.OP.WYSZ_DOMYSLNE
    if w.get("region") == "polska":
        reg = lambda t: True
    elif w.get("region") == "wojewodztwa":
        wyb = set(w.get("wojewodztwa") or [])
        reg = lambda t: (t.get("wojewodztwo") or S.wojewodztwo_ogloszenia(t)) in wyb or bool(set(t.get("wojewodztwa") or []) & wyb)
    else:
        reg = S.sprawdzacz_obszaru(c)
    rodz = set(w.get("rodzaje") or S.OP.RODZAJE)

    def f(t):
        r = t.get("rodzaj_przedmiotu") or S.OP.rodzaj_z_bzp(t.get("rodzaj"))
        return (not r or r in rodz) and S.OP.pasuje_slowa(t.get("przedmiot"), w.get("slowa")) and reg(t)
    return f


def praca_odw_sprawdz(log, tylko=None):
    """Odwołania od przetargów: dopisanie obserwowanych (pamięć BZP w regionie, po terminie ofert) i sprawdzenie dokumentów rozstrzygnięcia."""
    c = S.cfg()
    B = S._op()
    ust = B.ustawienia()
    prog = float(ust.get("prog") or S.OP.PROG_DOMYSLNY)
    dzis = dt.date.today()
    with S.OP.BLOKADA:
        P = B.postepowania()
    if not tylko:
        w_obszarze = _odw_filtr(c, ust)  # wyszukiwarka modułu: region, rodzaj zamówienia, słowa
        dni_max = int((ust.get("wyszukiwanie") or {}).get("dni") or 45)
        dod = 0
        for o in S.WSP.wszystkie(90):
            tm = str(o.get("termin_ofert") or "")[:10]
            try:
                dni = (dzis - dt.date.fromisoformat(tm)).days
            except ValueError:
                continue
            nr = o.get("numer")
            if not nr or nr in P or not (0 <= dni <= dni_max) or o.get("bk_id"):
                continue
            if not w_obszarze(o):
                continue
            tekst = " ".join(str(o.get(k) or "") for k in ("link", "tresc"))
            oc = S.BZ.RE_OCDS.search(tekst)
            P[nr] = {"numer": nr, "przedmiot": o.get("przedmiot", ""), "zamawiajacy": o.get("zamawiajacy", ""), "miasto": o.get("miasto", ""),
                     "link": o.get("link", ""), "termin_ofert": o.get("termin_ofert", ""), "ocds": oc.group(0) if oc else "",
                     "platformy": S.OP.platformy_z_ogloszenia(S.BZ.adresy_platform(o.get("tresc", ""))), "platformy_ustalone": 2, "zrodlo": "BZP", "status": "obserwowany",
                     "rodzaj_przedmiotu": S.OP.rodzaj_z_bzp(o.get("rodzaj")) or "roboty", "wojewodztwo": S.wojewodztwo_ogloszenia(o),
                     "dodano": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
            dod += 1
        log(f"Obserwowane: +{dod} nowych, razem {len(P)}.")
    idx = None
    for nr, r in P.items():  # postępowania dopisane wcześniej – adres platformy zamawiającego z ogłoszenia (dawniej pomijany, gdy był numer e-Zamówień)
        if r.get("platformy_ustalone") != 2 and r.get("status") not in S.KONCOWE_ODW and not r.get("z_linku"):
            if idx is None:
                idx = {o.get("numer"): o for o in S.WSP.wszystkie(120)}
            r["platformy"] = S.OP.platformy_z_ogloszenia(S.BZ.adresy_platform((idx.get(nr) or {}).get("tresc", ""))) or S.OP.platformy_z_ogloszenia(r.get("platformy"))
            r["platformy_ustalone"] = 2
    sprawdz = [nr for nr, r in P.items() if ((tylko and nr in tylko) or (not tylko and r.get("status") not in S.KONCOWE_ODW))
               and (r.get("ocds") or r.get("platformy"))]
    pominiete_bez_zrodla = sum(1 for r in P.values() if not r.get("ocds") and not r.get("platformy") and r.get("status") not in S.KONCOWE_ODW)
    if pominiete_bez_zrodla:
        log(f"{pominiete_bez_zrodla} postępowań bez adresu e-Zamówień ani platformy w ogłoszeniu – poza zasięgiem modułu.")
    sprawdz.sort(key=lambda nr: P[nr].get("sprawdzono") or "")  # rotacyjnie – najpierw sprawdzane najdawniej (przy dużym zasięgu)
    for i, nr in enumerate(sprawdz[:400], 1):
        rec = P[nr]
        try:
            tm = str(rec.get("termin_ofert") or "")[:10]
            if not tylko and tm and (dzis - dt.date.fromisoformat(tm)).days > S.OP.DNI_OBSERWACJI and rec.get("status") != "możliwy do podważenia":
                rec["status"] = "termin odwołania minął" if rec.get("ocena") else "zakończono obserwację"
                rec["koniec_obserwacji"] = True
                continue
            _odw_jedno(log, c, B, nr, rec, prog)
        except Exception as e:
            rec["blad"] = str(e)[:300]
            log(f"   {rec.get('przedmiot', '')[:60]}: {e}")
            if "przerwa techniczna" in str(e):
                break
        if i % 10 == 0:
            with S.OP.BLOKADA:
                B.zapisz_postepowania(P)
    with S.OP.BLOKADA:
        aktualne = B.postepowania()
        aktualne.update({k: v for k, v in P.items() if k not in aktualne or aktualne[k].get("status") != "ukryty"})
        B.zapisz_postepowania(aktualne)
        B.pisz("stan.json", {"ostatnie": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    mozliwe = sum(1 for r in P.values() if r.get("status") == "możliwy do podważenia")
    log(f"Gotowe: sprawdzono {len(sprawdz[:400])} postępowań; możliwe do podważenia: {mozliwe}.")
    return {"mozliwe": mozliwe}


STATUSY_PRZED_TERMINEM = ("możliwy do podważenia", "do sprawdzenia", "bez zarzutów z danych publicznych")


def odw_aktualne_terminy(r, dzis=None):
    """Dni do terminu odwołania liczone w chwili odczytu (zapisane przy sprawdzeniu dezaktualizują się z każdym dniem);
    po upływie terminu we wszystkich częściach status „termin odwołania minął”. Zmienia kopię rekordu."""
    dzis = dzis or dt.date.today()
    dni = []
    for o in r.get("ocena") or []:
        try:
            o["dni_do_terminu"] = (dt.date.fromisoformat(str(o.get("termin_odwolania"))[:10]) - dzis).days
        except ValueError:
            continue
        if o.get("status") in STATUSY_PRZED_TERMINEM and o["dni_do_terminu"] < 0:
            o["status"] = "termin odwołania minął"
        dni.append(o["dni_do_terminu"])
    if dni:
        r["dni_do_terminu"] = min(d for d in dni if d >= 0) if any(d >= 0 for d in dni) else max(dni)
        if r.get("status") in STATUSY_PRZED_TERMINEM and all(d < 0 for d in dni):
            r["status"] = "termin odwołania minął"
    return r


@bp.get("/api/odw/stan")
@S.wymaga_logowania
def odw_stan():
    B = S._op()
    P = B.postepowania()
    _odw_uzupelnij_woj(B, P)
    P = {nr: odw_aktualne_terminy(json.loads(json.dumps(r))) for nr, r in P.items()}
    for nr, r in P.items():  # reżim postępowania (progi UE) – automat albo ręczne ustawienie; wpływa na termin odwołania (5/10 albo 10/15 dni)
        u_, zr_ = odw_unijne(nr, r)
        r["rezim"] = {"unijne": u_, "opis": zr_, "reczne": r.get("unijne_reczne") if isinstance(r.get("unijne_reczne"), bool) else None,
                      "auto": odw_unijne_auto(nr, r)[0]}
    L = sorted((dict(r, numer=r.get("numer") or nr, katalog=r.get("katalog") or S.OP.bezpieczny(nr)) for nr, r in P.items()),
               key=lambda r: (S.KOLEJNOSC_ODW.get(r.get("status"), 5), r.get("dni_do_terminu") if r.get("dni_do_terminu") is not None else 99,
                                          str(r.get("termin_ofert") or "")))
    ust = B.ustawienia()
    f = _odw_filtr(S.cfg(), ust)
    wszystkie = len(L)
    L = [r for r in L if f(r)]
    return jsonify({"postepowania": L, "poza_filtrem": wszystkie - len(L), "ustawienia": ust, "stan": B.czytaj("stan.json", {}),
                    "wojewodztwa": list(S.WOJEWODZTWA), "rodzaje": S.OP.RODZAJE,
                    "region": S.opis_obszaru(S.cfg().get("obszar"), S.cfg()), "liczniki": {k: sum(1 for r in P.values() if r.get("status") == k) for k in S.KOLEJNOSC_ODW}})


@bp.post("/api/odw/sprawdz")
@S.wymaga_logowania
def odw_sprawdz():
    nr = (request.json or {}).get("numer")
    if nr and (request.json or {}).get("od_nowa"):  # „Analizuj ponownie” – wymuszony ponowny odczyt AI dokumentów rozstrzygnięcia
        B = S._op()
        with S.OP.BLOKADA:
            P = B.postepowania()
            if nr in P:
                P[nr]["wymus_odczyt"] = True
                P[nr].pop("koniec_obserwacji", None)
                if P[nr].get("status") in ("termin odwołania minął",):
                    P[nr]["status"] = "obserwowany"
                B.zapisz_postepowania(P)
    return jsonify(S.uruchom("odwolania", "Odwołania od przetargów: sprawdzanie rozstrzygnięć", praca_odw_sprawdz, [nr] if nr else None))


@bp.post("/api/odw/dodaj")
@S.wymaga_logowania
def odw_dodaj():
    """Postępowanie z linku (e-Zamówienia albo platforma; bez BIP) – do obserwacji i natychmiastowego sprawdzenia."""
    j = request.json or {}
    url = str(j.get("url") or "").strip()
    if not re.match(r"(?i)^https?://", url):
        return jsonify({"blad": "Podaj pełny adres postępowania (https://…)."}), 400
    if re.search(r"(?i)\bbip\.|/bip/", url):
        return jsonify({"blad": "Strony BIP są poza zakresem modułu – podaj adres postępowania na Platformie e-Zamówienia albo platformie zakupowej."}), 400
    oc = S.BZ.RE_OCDS.search(url)
    nr = oc.group(0) if oc else "LINK-" + S.hashlib.sha1(url.encode()).hexdigest()[:10]
    B = S._op()
    with S.OP.BLOKADA:
        P = B.postepowania()
        P.setdefault(nr, {"numer": nr, "przedmiot": str(j.get("przedmiot") or url)[:300], "zamawiajacy": str(j.get("zamawiajacy") or "")[:200],
                          "link": url, "termin_ofert": str(j.get("termin_ofert") or ""), "ocds": oc.group(0) if oc else "", "platformy": [] if oc else [url], "z_linku": True, "platformy_ustalone": 2,
                          "zrodlo": "link", "status": "obserwowany", "dodano": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
        if P[nr].get("status") == "ukryty":
            P[nr]["status"] = "obserwowany"
        B.zapisz_postepowania(P)
    return jsonify(S.uruchom("odwolania", "Odwołania od przetargów: sprawdzanie postępowania z linku", praca_odw_sprawdz, [nr]))


@bp.post("/api/odw/ukryj")
@S.wymaga_logowania
def odw_ukryj():
    nr = (request.json or {}).get("numer")
    B = S._op()
    with S.OP.BLOKADA:
        P = B.postepowania()
        if nr not in P:
            return jsonify({"blad": "Nie ma takiego postępowania."}), 404
        P[nr]["status"] = "ukryty"
        B.zapisz_postepowania(P)
    return jsonify({"ok": True})


@bp.post("/api/odw/parametry")
@S.wymaga_logowania
def odw_parametry():
    """Ręczne parametry postępowania, od których zależy termin odwołania (art. 515 ust. 1 Pzp):
    unijne – "auto" | true | false (wartość równa lub przekraczająca progi UE; przełącznik dla postępowań z linku platformy i korekta automatu);
    czesc (indeks części) + data_przekazania (RRRR-MM-DD albo "") + sposob ("elektronicznie" | "inny") – dzień i sposób przekazania informacji o wyborze.
    Ocena przeliczana bez AI i bez sieci."""
    j = request.json or {}
    nr = j.get("numer")
    if not isinstance(nr, str):
        return jsonify({"blad": "Brak numeru postępowania."}), 400
    if "unijne" in j and j["unijne"] not in ("auto", True, False, None):
        return jsonify({"blad": "Reżim: auto, true albo false."}), 400
    if "sposob" in j and j["sposob"] not in ("elektronicznie", "inny"):
        return jsonify({"blad": "Sposób przekazania: „elektronicznie” albo „inny”."}), 400
    data = str(j.get("data_przekazania") or "").strip()
    if data:
        try:
            d_ = dt.date.fromisoformat(data[:10])
        except ValueError:
            return jsonify({"blad": "Data przekazania w formacie RRRR-MM-DD."}), 400
        if d_ > dt.date.today() + dt.timedelta(days=1) or d_.year < 2021:
            return jsonify({"blad": "Data przekazania nie może być z przyszłości ani sprzed 2021 r."}), 400
        data = d_.isoformat()
    B = S._op()
    with S.OP.BLOKADA:
        P = B.postepowania()
        rec = P.get(nr)
        if not rec:
            return jsonify({"blad": "Nie ma takiego postępowania."}), 404
        if "unijne" in j:
            if isinstance(j["unijne"], bool):
                rec["unijne_reczne"] = j["unijne"]
            else:
                rec.pop("unijne_reczne", None)
        if "czesc" in j:
            czesci = (rec.get("dane") or {}).get("czesci") or []
            try:
                cz = czesci[int(j["czesc"])]
            except (TypeError, ValueError, IndexError):
                return jsonify({"blad": "Nie ma takiej części postępowania."}), 400
            k = klucz_czesci(cz)
            if data or j.get("sposob"):
                stare = (rec.get("przekazanie") or {}).get(k) or {}
                rec.setdefault("przekazanie", {})[k] = {"data": data if "data_przekazania" in j else stare.get("data", ""),
                                                        "sposob": j.get("sposob") or stare.get("sposob") or "elektronicznie"}
            else:
                (rec.get("przekazanie") or {}).pop(k, None)
        if rec.get("dane"):
            odw_ocen(B, nr, rec, float(B.ustawienia().get("prog") or S.OP.PROG_DOMYSLNY))
        B.zapisz_postepowania(P)
    u, zr = odw_unijne(nr, rec)
    return jsonify({"ok": True, "unijne": u, "rezim": zr, "ocena": rec.get("ocena") or []})


def _odw_uzupelnij_woj(B_, P):
    """Postępowania w module Odwołań dodane przed zapisem województwa: z e-Zamówień, z ogłoszenia w pamięci albo z danych zamawiającego –
    zapis na stałe (filtry regionu w Odwołaniach i Leadach)."""
    braki = [nr for nr, r in P.items() if not r.get("wojewodztwo")]
    if not braki:
        return
    idx = {o.get("numer"): o for o in S.WSP.wszystkie(120)}
    zm = {}
    for nr in braki:
        r_ = P[nr]
        w_ = (r_.get("ez") or {}).get("wojewodztwo") or (S.wojewodztwo_ogloszenia(idx[nr]) if nr in idx else "") or S.wojewodztwo_ogloszenia(r_) or ""
        if w_ in S.WOJEWODZTWA:
            r_["wojewodztwo"] = zm[nr] = w_
    if zm:
        with S.OP.BLOKADA:
            P2 = B_.postepowania()
            for nr, w_ in zm.items():
                if nr in P2 and not P2[nr].get("wojewodztwo"):
                    P2[nr]["wojewodztwo"] = w_
            B_.zapisz_postepowania(P2)


@bp.post("/api/odw/ustawienia")
@S.wymaga_logowania
def odw_ustawienia():
    j = request.json or {}
    B = S._op()
    zmiany = {}
    if "prog" in j:
        prog = S.RY._f(j.get("prog"))
        if not prog or prog < 0:
            return jsonify({"blad": "Podaj próg wartości w zł."}), 400
        zmiany["prog"] = prog
    if isinstance(j.get("wyszukiwanie"), dict):
        w = j["wyszukiwanie"]
        zmiany["wyszukiwanie"] = {"region": w.get("region") if w.get("region") in ("jak_przetargi", "wojewodztwa", "polska") else "jak_przetargi",
                                  "wojewodztwa": [x for x in w.get("wojewodztwa") or [] if x in S.WOJEWODZTWA],
                                  "rodzaje": [x for x in w.get("rodzaje") or [] if x in S.OP.RODZAJE] or list(S.OP.RODZAJE),
                                  "slowa": str(w.get("slowa") or "")[:300], "dni": max(1, min(90, int(S.RY._f(w.get("dni")) or 45)))}
        if zmiany["wyszukiwanie"]["region"] == "wojewodztwa" and not zmiany["wyszukiwanie"]["wojewodztwa"]:
            return jsonify({"blad": "Wybierz co najmniej jedno województwo."}), 400
    if isinstance(j.get("nadawca"), dict):  # dane pośrednika do wniosków i wiadomości
        zmiany["nadawca"] = {k: str(j["nadawca"].get(k) or "").strip()[:200] for k in S.OP.NADAWCA_POLA}
    with S.OP.BLOKADA:
        B.pisz("ustawienia.json", dict(B.czytaj("ustawienia.json", {}), **zmiany))
    return jsonify({"ok": True, "ustawienia": B.ustawienia()})


def _odw_czesc(numer, czesc):
    B = S._op()
    P = B.postepowania()
    rec = P.get(numer)
    if not rec or not rec.get("ocena"):
        raise ValueError("Brak oceny tego postępowania – najpierw „Sprawdź ponownie”.")
    try:
        o = rec["ocena"][int(czesc or 0)]
    except (ValueError, IndexError):
        raise ValueError("Nie ma takiej części postępowania.")
    return B, P, rec, o


def _odw_firma(o, nazwa):
    f = next((x for x in o.get("firmy") or [] if x.get("wykonawca") == nazwa), None) or \
        next((dict(x, miejsce=x.get("miejsce") or x.get("status")) for x in o.get("oferenci") or [] if x.get("wykonawca") == nazwa and x.get("status") != "wybrana"), None)
    if not f:
        raise ValueError("Nie ma takiej firmy na liście tego postępowania.")
    return f


def praca_odw_odwolanie(log, numer, czesc, firma):
    """Projekt odwołania do KIO dla firmy z dalszego miejsca – generator z modułu prawnika (AI); termin i wpis według reżimu (krajowy / unijny)."""
    B, P, rec, o = _odw_czesc(numer, czesc)
    f = _odw_firma(o, firma)
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    c["_model"] = c.get("model_oferty") or "claude-sonnet-5-5"
    u, w, O = S.OP.dane_do_odwolania(rec, o, f)
    log(f"AI przygotowuje projekt odwołania dla: {firma}…")
    od = S.ai_dane(c, S.PRW.SYSTEM_ODWOLANIE, [{"type": "text", "text": S.PRW.polecenie_odwolania(u, S.OP._czesc_opis(rec, o), w, O)}], 12000, log,
                 lambda t: S.MO.wyciagnij_json(t) or {})
    folder = os.path.join(B.pliki, S.OP.bezpieczny(numer))
    os.makedirs(folder, exist_ok=True)
    nazwa = f"Projekt_odwolania_{S.MO.bezpieczna_nazwa(firma)[:40]}.docx"
    S.PRW.odwolanie_docx(os.path.join(folder, nazwa), S.OP._czesc_opis(rec, o), u, od)
    with S.OP.BLOKADA:
        P = B.postepowania()
        P[numer].setdefault("pisma", {})[f"odwolanie|{czesc}|{firma}"] = {"plik": nazwa, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        B.zapisz_postepowania(P)
    log(f"Gotowe: {nazwa}")
    return {"plik": nazwa}


@bp.post("/api/odw/dokument")
@S.wymaga_logowania
def odw_dokument():
    """Notatka o możliwości podważenia, wniosek o udostępnienie protokołu i oferty (od razu, bez AI) albo projekt odwołania (zadanie AI)."""
    j = request.json or {}
    numer, czesc, rodz = j.get("numer"), j.get("czesc", 0), j.get("rodzaj")
    try:
        B, P, rec, o = _odw_czesc(numer, czesc)
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    if rodz == "odwolanie":
        try:
            _odw_firma(o, j.get("firma"))
        except ValueError as e:
            return jsonify({"blad": str(e)}), 400
        return jsonify(S.uruchom("odw_odwolanie", f"Projekt odwołania – {j.get('firma')}", praca_odw_odwolanie, numer, czesc, j.get("firma")))
    if rodz not in ("notatka", "wniosek"):
        return jsonify({"blad": "Nieznany dokument."}), 400
    folder = os.path.join(B.pliki, S.OP.bezpieczny(numer))
    os.makedirs(folder, exist_ok=True)
    nazwa = f"{'Notatka_mozliwosc_podwazenia' if rodz == 'notatka' else 'Wniosek_udostepnienie_oferty_protokolu'}_{S.OP.bezpieczny(numer)[-20:]}" + (f"_cz{o.get('czesc')}" if o.get("czesc") else "") + ".docx"
    (S.OP.notatka_docx if rodz == "notatka" else S.OP.wniosek_docx)(os.path.join(folder, nazwa), rec, o, B.ustawienia().get("nadawca") or {})
    return jsonify({"url": f"/api/odw/plik/{S.OP.bezpieczny(numer)}/{nazwa}"})


@bp.post("/api/odw/email")
@S.wymaga_logowania
def odw_email():
    """PROJEKT neutralnego tekstu do firmy – program NIE wysyła (decyzja właściciela: tylko „przygotuj projekt” + ostrzeżenie art. 398 PKE / RODO /
    etyka zawodowa; bez wysyłki masowej i automatycznej). Adres e-mail firmy wpisuje użytkownik (zapamiętany przy postępowaniu)."""
    j = request.json or {}
    try:
        B, P, rec, o = _odw_czesc(j.get("numer"), j.get("czesc", 0))
        f = _odw_firma(o, j.get("firma"))
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    em = str(j.get("email") or "").strip()
    if em:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", em, re.I):
            return jsonify({"blad": "Niepoprawny adres e-mail."}), 400
        with S.OP.BLOKADA:
            P = B.postepowania()
            P[j["numer"]].setdefault("kontakty", {})[f["wykonawca"]] = em
            B.zapisz_postepowania(P)
    temat, tresc = S.OP.email(rec, o, f, B.ustawienia().get("nadawca") or {})
    return jsonify({"temat": temat, "tresc": tresc, "email": em or (rec.get("kontakty") or {}).get(f["wykonawca"], ""),
                    "projekt": True, "wysylka": False, "ostrzezenie": S.OP.OSTRZEZENIE_KONTAKT})


@bp.post("/api/odw/badanie")
@S.wymaga_logowania
def odw_badanie():
    """Badanie pogłębione: nowe sprawdzenie ofert (moduł badania ofert, perspektywa wykonawcy) z dokumentami rozstrzygnięcia –
    ofertę wybranego wykonawcy (z wniosku o udostępnienie) wgrywasz tam."""
    j = request.json or {}
    try:
        B, P, rec, o = _odw_czesc(j.get("numer"), j.get("czesc", 0))
        f = _odw_firma(o, j.get("firma")) if j.get("firma") else {}
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    pid = uuid.uuid4().hex[:12]
    d = os.path.join(S.PROJ, pid)
    os.makedirs(os.path.join(d, "dokumenty"), exist_ok=True)
    m = {"id": pid, "nazwa": f"Odwołanie – {S.OP._czesc_opis(rec, o)[:80]}", "typ": "ocena_ofert", "strona": "prawnik", "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
         "wlasciciel": S.konto_biezace(), "ocena": {"swz": {}, "oferty": [], "podsum": {}},
         "prawnik": S.PRW.ustawienia({"prawnik": {"przedmiot": rec.get("rodzaj_przedmiotu") or "roboty", "tryb": "unijny" if o.get("unijne") else "krajowy", "dla_kogo": "wykonawca",
                                                "klient": f.get("wykonawca", ""), "zatwierdzone": "1"}}),
         "z_odwolan": {"numer": j.get("numer"), "czesc": j.get("czesc", 0), "link": rec.get("link")}}
    zrod = os.path.join(B.pliki, S.OP.bezpieczny(j.get("numer")))
    for x in rec.get("dokumenty") or []:
        if x.get("plik") and os.path.isfile(os.path.join(zrod, x["plik"])):
            S.shutil.copy2(os.path.join(zrod, x["plik"]), os.path.join(d, "dokumenty", x["plik"]))
    S.zapisz_meta(pid, m)
    with S.OP.BLOKADA:
        P = B.postepowania()
        P[j["numer"]]["badanie_id"] = pid
        B.zapisz_postepowania(P)
    return jsonify({"id": pid})


@bp.get("/api/odw/plik/<katalog>/<path:nazwa>")
@S.wymaga_logowania
def odw_plik(katalog, nazwa):
    folder = os.path.join(S._op().pliki, S.OP.bezpieczny(katalog))
    sc = os.path.realpath(os.path.join(folder, nazwa))
    if not sc.startswith(os.path.realpath(folder) + os.sep) or not os.path.isfile(sc):
        abort(404)
    return send_file(sc, as_attachment=True)
