# -*- coding: utf-8 -*-
"""
Moduł wspólnot, spółdzielni i deweloperów – trasy (etap 2 podziału serwer.py, blueprint „wspolnota”): Moje zapytania, nowa inwestycja,
zaproszenia do wykonawców z okolicy (wyszukiwanie, wysyłka, rezygnacje).
Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera, działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, jsonify, request, session

import serwer as S
from uwierzytelnianie import wymaga_logowania

bp = Blueprint("wspolnota", __name__)


@bp.get("/api/zam/zapytania")
@wymaga_logowania
def zam_zapytania():
    """Moje zapytania (wspólnoty, spółdzielnie, deweloperzy): w przygotowaniu i rozesłane – termin, liczba ofert, zaproszenia."""
    wyn, login, rola, dzis = [], session.get("login"), S.rola_sesji(), dt.date.today()
    for pid, m in S.projekty_ro():  # tylko do odczytu – bez kopiowania
        if not m or m.get("typ") != "zamowienie" or m.get("archiwum") or m.get("rodzic") or not S.projekt_wspolnoty(m) \
                or m.get("status_projektu") in ("realizacja", "zakonczony") or not S.ma_dostep(m, login, rola, lista=True):
            continue
        K = m.get("kreator") or {}
        t = S.ZP.termin_ofert(K)
        oid = K.get("ocena_id")
        n = len(((S.czytaj_ro(os.path.join(S.PROJ, oid, "projekt.json"), {}) or {}).get("ocena") or {}).get("oferty") or []) if oid else 0
        Z = K.get("zaproszenia") or {}
        wyn.append({"id": pid, "nazwa": m.get("nazwa"), "utworzono": m.get("utworzono"), "termin_ofert": t.isoformat() if t else "",
                    "dni": (t - dzis).days if t else None, "oferty": n, "ocena_id": oid or "",
                    "status": "w przygotowaniu" if not t else ("po terminie" if t < dzis else "zapytanie w toku"),
                    "kandydatow": len(Z.get("kandydaci") or []), "zaproszono": len(Z.get("wyslane") or [])})
    return jsonify(sorted(wyn, key=lambda x: (x["termin_ofert"] == "", x["termin_ofert"] or x["utworzono"] or "")))


@bp.post("/api/zam/inwestycja")
@wymaga_logowania
def zam_inwestycja():
    """Realizuj umowę / inwestycje (wspólnota): umowa zawarta poza programem – od razu w realizacji."""
    j = request.json or {}
    nazwa = str(j.get("nazwa") or "").strip()[:120]
    if not nazwa:
        return jsonify({"blad": "Podaj nazwę inwestycji."}), 400
    import postepowanie_zam as PZ_
    bl = PZ_.umowa_bledy(j)  # cena, stawka VAT (0/5/8/23 – bez stałej 8%), daty
    if bl:
        return jsonify({"blad": " ".join(bl)}), 400
    pid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, pid, "dokumenty"))
    umowa = {k: str(j.get(k) or "")[:200] for k in ("wykonawca_nazwa", "wykonawca_nip", "wykonawca_adres", "cena_netto", "vat", "umowa_nr", "data_umowy", "termin")}
    S.zapisz_meta(pid, {"id": pid, "nazwa": nazwa, "typ": "zamowienie", "strona": "zamawiajacy", "rodzaj_zamowienia": j.get("rodzaj") if j.get("rodzaj") in S.KZ.RODZAJE else "roboty",
                      "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wlasciciel": S.konto_biezace(), "pominiete": [], "prywatny": True,
                      "kreator": {"rodzaj": j.get("rodzaj") if j.get("rodzaj") in S.KZ.RODZAJE else "roboty", "opis": nazwa, "sciezka": "nowe", "krok": 2, "potrzeba": {},
                                  "warunki": {}, "prywatny": True, "umowa": umowa}})
    return jsonify({"id": pid})


def _geokoduj_miasto(miasto):
    try:
        w = S.REG.szukaj_miejscowosci(miasto)
        return (w[0]["lat"], w[0]["lon"]) if w else None
    except Exception:
        return None


def praca_zaproszenia(log, pid, promien=25, lokalizacja=""):
    """Wykonawcy z okolicy, którzy w ostatnich 24 miesiącach wygrali podobne zamówienia (BZP) – z kontaktem i uzasadnieniem."""
    m = S.meta(pid)
    K = m.get("kreator") or {}
    p = K.get("potrzeba") or {}
    miejsce = (lokalizacja or p.get("obiekt") or p.get("miejsce") or K.get("zamawiajacy") or "").strip()
    if not miejsce:
        raise ValueError("Podaj miejsce realizacji (miejscowość albo adres), żeby wyznaczyć okolicę.")
    kandyd_m = re.findall(r"\d{2}-\d{3}\s+([A-ZĄĆĘŁŃÓŚŹŻ][\wąćęłńóśźż\- ]+)", miejsce) or [x.strip() for x in re.split(r",", miejsce) if x.strip()][::-1]
    poz = None
    for q in kandyd_m[:3] + [miejsce]:
        w = S.REG.szukaj_miejscowosci(q)
        if w:
            poz = w[0]
            break
    if not poz:
        raise ValueError(f"Nie znaleziono miejscowości „{miejsce[:60]}” – wpisz samą nazwę miejscowości.")
    log(f"Okolica: {poz['nazwa']} ({poz.get('wojewodztwo') or ''}), promień {promien} km.")
    woj = S.REG.wojewodztwa_obszaru(poz["lat"], poz["lon"], promien, poz.get("wojewodztwo") or "") or [poz.get("wojewodztwo")]
    kody = [S.WOJEWODZTWA[w_] for w_ in woj if w_ in S.WOJEWODZTWA]
    os.makedirs(S.KAT_WYNIKI_DNI, exist_ok=True)
    dzis = dt.date.today()
    wyniki, pobrane, brak = [], 0, 0
    for i in range(1, 731):
        d = dzis - dt.timedelta(days=i)
        for kod in kody:
            plik = os.path.join(S.KAT_WYNIKI_DNI, f"{kod}_{d.isoformat()}_v3.json")
            if os.path.exists(plik):
                wyniki += S.czytaj(plik, [], pamiec=False)
            elif pobrane < 120:
                try:
                    dz, kompletne = S.HZ.pobierz_wyniki_dnia(d, kod)
                    pobrane += 1
                    if kompletne:
                        S.pisz(plik, dz)
                    wyniki += dz
                except Exception:
                    brak += 1
            else:
                brak += 1
        if i % 60 == 0:
            log(f"Ogłoszenia o wyniku z BZP: {i} dni wstecz, {len(wyniki)} rozstrzygnięć.")
    if brak:
        log(f"Brakuje danych z {brak} dni (uzupełniają się co noc) – lista może być niepełna; uruchom ponownie później.")
    nazwa = m.get("nazwa") or ""
    przedmiot = f"{nazwa} {K.get('opis') or ''} {p.get('zakres') or ''}"
    wyklucz = [o.get("nip") for o in (S._ocena_zamowienia(m).get("oferty") or [])]
    log("Wybór wykonawców podobnych prac w okolicy…")
    R_ = _rezygnacje()
    wyklucz = list(wyklucz) + [n for n in R_ if n.isdigit()]
    L = S.ZP.kandydaci(wyniki, przedmiot, "", poz["lat"], poz["lon"], int(promien), _geokoduj_miasto, wyklucz)
    cache, token = S.czytaj(S.F_NIP_CACHE, {}), S.cfg_surowy().get("ceidg_token")
    for i, k in enumerate(L[:15], 1):
        log(f"Dane kontaktowe {i}/{min(15, len(L))}: {k['nazwa'][:50]}")
        if k.get("nip"):
            dane, bl = S.NIP.szukaj(k["nip"], cache, ceidg_token=token)
            if not bl:
                k["email"], k["telefon"], k["adres"] = dane.get("email") or "", dane.get("telefon") or "", dane.get("adres") or ""
                if not k["email"] and dane.get("krs"):
                    kk = S.OP.krs_kontakt(dane["krs"])
                    k["email"], k["www"] = kk.get("email") or "", kk.get("www") or ""
                    if not k["email"] and k["www"]:
                        ks = S.OP.kontakt_ze_strony(k["www"])
                        k["email"] = (ks.get("emaile") or ks.get("email") or [""])[0] if isinstance(ks.get("emaile") or ks.get("email"), list) else (ks.get("email") or "")
    S.pisz(S.F_NIP_CACHE, cache)
    L = [k for k in L if not _zrezygnowal(k, R_)]  # firmy, które zrezygnowały (także po adresie e-mail)
    if L:
        try:
            c = S.cfg()
            S.wymagany_klucz(c)
            lista = [{"nr": i, "nazwa": k["nazwa"], "podobne_prace": [x["przedmiot"] for x in k["prace"][:3]], "liczba_prac": k["liczba_prac"],
                      "km": k.get("odleglosc_siedziby") or k.get("odleglosc_prac")} for i, k in enumerate(L)]
            txt, _ = S.MO.claude_stream(c, "Doradzasz zamawiającemu, których wykonawców zaprosić do złożenia oferty. Odpowiadasz wyłącznie JSON.",
                                      [{"type": "text", "text": f"Zamówienie: {przedmiot[:600]}\nKandydaci: {json.dumps(lista, ensure_ascii=False)}\n"
                                        'Dla każdego kandydata podaj jedno zdanie uzasadnienia i priorytet 1–3 (1 = najbardziej dopasowany). JSON: [{"nr": 0, "uzasadnienie": "", "priorytet": 1}]'}],
                                      max_tokens=3000, log=log)
            try:  # odpowiedź to lista – wyciagnij_json zwraca tylko pierwszy obiekt
                lista_ai = json.loads(txt[txt.index("["):txt.rindex("]") + 1])
            except ValueError:
                lista_ai = []
            for x in lista_ai if isinstance(lista_ai, list) else []:
                if isinstance(x, dict) and isinstance(x.get("nr"), int) and 0 <= x["nr"] < len(L):
                    L[x["nr"]]["uzasadnienie"] = str(x.get("uzasadnienie") or "")[:300]
                    L[x["nr"]]["priorytet"] = int(x.get("priorytet") or 3) if str(x.get("priorytet") or "3").isdigit() else 3
            L.sort(key=lambda k: (k.get("priorytet", 3), -k["ocena"]))
        except Exception as e:
            log(f"Uzasadnienia AI pominięte ({str(e)[:80]}) – lista według podobieństwa i odległości.")
    with S.BLOKADA:
        m = S.meta(pid)
        Z = m.setdefault("kreator", {}).setdefault("zaproszenia", {})
        Z.update({"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "promien": int(promien), "miejsce": poz["nazwa"], "kandydaci": L,
                  "uwaga": "Źródło: ogłoszenia o wyniku w BZP z 24 miesięcy – firmy pracujące tylko dla klientów prywatnych nie trafią na listę."})
        S.zapisz_meta(pid, m)
    log(f"Gotowe: {len(L)} wykonawców w promieniu {promien} km, {sum(1 for k in L if k.get('email'))} z adresem e-mail.")


@bp.post("/api/projekty/<pid>/kreator/zaproszenia/kandydaci")
@wymaga_logowania
def zaproszenia_kandydaci(pid):
    j = request.json or {}
    pr = int(j.get("promien") or 25) if str(j.get("promien") or "25").isdigit() else 25
    return jsonify(S.uruchom("zamawiajacy", "Wykonawcy z okolicy do zaproszenia", praca_zaproszenia, pid, max(5, min(pr, 50)), str(j.get("lokalizacja") or "")[:200]))


F_ZAPR_REZYGNACJE = S.SciezkaKonta("zaproszenia_rezygnacje.json")


def _rezygnacje():
    return S.czytaj(F_ZAPR_REZYGNACJE, {}) or {}


def _zrezygnowal(k, R=None):
    R = _rezygnacje() if R is None else R
    return any(x and x in R for x in (S.WER._nip(k.get("nip")), str(k.get("email") or "").lower().strip()))


@bp.post("/api/zam/zaproszenia/rezygnacja")
@wymaga_logowania
def zaproszenia_rezygnacja():
    """Firma nie chce otrzymywać zaproszeń (odpowiedź na zaproszenie, sprzeciw – art. 21 RODO) – wykluczana z kolejnych list i wysyłek."""
    j = request.json or {}
    klucze = [x for x in (S.WER._nip(j.get("nip")), str(j.get("email") or "").lower().strip()) if x]
    if not klucze:
        return jsonify({"blad": "Podaj NIP albo adres e-mail firmy."}), 400
    with S.BLOKADA:
        R = _rezygnacje()
        for k in klucze:
            R[k] = {"nazwa": str(j.get("nazwa") or "")[:120], "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "kto": session.get("login") or ""}
        S.pisz(F_ZAPR_REZYGNACJE, R)
    return jsonify({"ok": True, "liczba": len(R)})


@bp.post("/api/projekty/<pid>/kreator/zaproszenia/wyslij")
@wymaga_logowania
def zaproszenia_wyslij(pid):
    """Zaproszenia do złożenia oferty z dokumentami postępowania – przez skrzynkę użytkownika (SMTP) albo jako pliki .eml do wysłania z programu pocztowego."""
    import mimetypes
    from email.message import EmailMessage
    j = request.json or {}
    m = S.meta(pid)
    K = m.get("kreator") or {}
    Z = K.get("zaproszenia") or {}
    R_ = _rezygnacje()
    juz = {(x.get("nip") or x.get("nazwa")) for x in Z.get("wyslane") or [] if x.get("sposob") == "e-mail"}  # tylko wysłane z programu (plik .eml – przygotowany, nie wysłany)
    wybrani = [k for k in Z.get("kandydaci") or [] if (k.get("nip") or k.get("nazwa")) in (j.get("wybrani") or []) and k.get("email")
               and not _zrezygnowal(k, R_) and (k.get("nip") or k.get("nazwa")) not in juz]  # bez rezygnujących i bez ponownej wysyłki
    if not wybrani:
        return jsonify({"blad": "Zaznacz wykonawców, którzy mają adres e-mail."}), 400
    c = S.cfg()
    zal = []
    kat = os.path.join(S.pdir(pid), "dokumenty_postepowania")
    for f in sorted(os.listdir(kat)) if os.path.isdir(kat) else []:
        sc = os.path.join(kat, f)
        if f.lower().endswith((".pdf", ".docx", ".xlsx")) and sum(os.path.getsize(x) for x in zal) + os.path.getsize(sc) < 15_000_000:
            zal.append(sc)
    nadawca = c.get("smtp_od") or c.get("smtp_login") or c.get("firma_email") or ""
    folder = os.path.join(S.pdir(pid), "zaproszenia")
    os.makedirs(folder, exist_ok=True)
    wiad, pliki = [], []
    for k in wybrani:
        temat, tekst = S.ZP.tresc_zaproszenia(K.get("zamawiajacy") or "", m.get("nazwa") or "", K.get("opis") or "", S.ZP.termin_ofert(K) or K.get("termin_ofert"),
                                            (K.get("warunki") or {}).get("kontakt") or "", k.get("nazwa"))
        msg = EmailMessage()
        msg["Subject"], msg["To"] = temat, k["email"]
        if nadawca:
            msg["From"] = nadawca
        msg.set_content(tekst)
        for sc in zal:
            with open(sc, "rb") as fh:
                typ = mimetypes.guess_type(sc)[0] or "application/octet-stream"
                msg.add_attachment(fh.read(), maintype=typ.split("/")[0], subtype=typ.split("/")[1], filename=os.path.basename(sc))
        wiad.append((k, msg))
    if j.get("sposob") == "smtp":
        try:
            S.MH.wyslij_smtp(c, [x[1] for x in wiad])
        except Exception as e:
            return jsonify({"blad": f"Nie udało się wysłać: {e}"}), 400
    else:
        for k, msg in wiad:
            nazwa_ = re.sub(r"[^\w\-]+", "_", k["nazwa"])[:40] + ".eml"
            with open(os.path.join(folder, nazwa_), "wb") as fh:
                fh.write(bytes(msg))
            pliki.append(nazwa_)
    with S.BLOKADA:
        m = S.meta(pid)
        Zp = m.setdefault("kreator", {}).setdefault("zaproszenia", {})
        Zp.setdefault("wyslane", []).extend({"nip": k.get("nip"), "nazwa": k["nazwa"], "email": k["email"], "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                             "sposob": "e-mail" if j.get("sposob") == "smtp" else "plik .eml"} for k, _ in wiad)
        S.zapisz_meta(pid, m)
    return jsonify({"wyslano": len(wiad) if j.get("sposob") == "smtp" else 0, "pliki": [f"/pobierz/{pid}/zaproszenia/{f}" for f in pliki], "zalaczniki": len(zal)})
