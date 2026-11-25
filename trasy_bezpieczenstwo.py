# -*- coding: utf-8 -*-
"""
Bezpieczeństwo, hasła, przedmiar bez cen, RODO w kadrach, godziny na udostępnionej budowie – trasy (decyzje właściciela, wersja „h81”).
Blueprint „bezpieczenstwo”. Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera.
- zmiana własnego hasła (/zmien-haslo, /api/haslo/zmien) i reset hasła przez administratora (hasło tymczasowe z wymuszoną zmianą);
- role bez Finansów i bez edycji Projektów (np. kierownik budowy): odpowiedzi modułu Projekty bez cen, pobieranie plików z cenami zablokowane,
  przedmiar robót bez cen (Excel);
- dokumentacja pracownicza po okresie przechowywania (art. 94 pkt 9b KP) – lista „do trwałego usunięcia” i usunięcie przez administratora;
- godziny pracy na budowie udostępnionej innemu kontu (pracownicy właściciela projektu, bez stawek);
- migracje danych tej wersji (firmy kont, role, przykładowy opis firmy).
"""
import datetime as dt
import io
import json
import os
import re
import time
import uuid

from flask import Blueprint, Response, jsonify, redirect, request, send_file, session

import bezpieczenstwo as BZ
import serwer as S

bp = Blueprint("bezpieczenstwo", __name__)


# ============================================================ H1-04: role bez cen – filtr po stronie serwera
RE_PLIK_API = re.compile(r"^/api/projekty/([0-9a-f]{12})/.+\.(docx|xlsx|zip|pdf|xls|csv)$")
RE_POBIERZ = re.compile(r"^/pobierz/([0-9a-f]{12})/(.+)$")


def _rola_bez_cen():
    return bool(session.get("zalogowany")) and S.UWIERZ.bez_cen()


@bp.before_app_request
def blokada_plikow_z_cenami():
    """Kierownik budowy (rola bez Finansów i bez edycji Projektów): pliki z cenami (kosztorys ofertowy, oferta, formularze cenowe,
    rozliczenia, protokoły z kwotami) i dokumenty Word/Excel modułu Projekty – 403. Przedmiar bez cen – dozwolony."""
    if request.method != "GET" or not _rola_bez_cen():
        return None
    sc = request.path
    m = RE_POBIERZ.match(sc)
    if m and BZ.plik_z_cenami(m.group(2)):
        return jsonify({"blad": "Ten plik zawiera ceny – Twoja rola (bez Finansów) widzi przedmiar bez cen."}), 403
    if RE_PLIK_API.match(sc) and S.UPR.modul_adresu(sc) == "projekty" and not sc.endswith("/przedmiar.xlsx"):
        return jsonify({"blad": "Ten dokument zawiera ceny – Twoja rola (bez Finansów) widzi przedmiar bez cen."}), 403
    return None


@bp.after_app_request
def odpowiedz_bez_cen(r):
    """Odpowiedzi JSON modułu Projekty dla roli bez cen: bez kwot (cena, wartość, netto, brutto…) i bez plików z cenami na listach."""
    try:
        if request.method != "GET" or r.status_code != 200 or r.mimetype != "application/json" or r.direct_passthrough \
                or r.headers.get("Content-Encoding") or not request.path.startswith("/api/") or not _rola_bez_cen():
            return r
        modul = S.UPR.modul_adresu(request.path)
        if modul == "realizacja" and re.fullmatch(r"/api/projekty/[0-9a-f]{12}/realizacja", request.path):
            dane = json.loads(r.get_data(as_text=True))  # ekran budowy: kwoty usuwa już trasa (rola bez Finansów); tu – pliki z cenami z listy
            if isinstance(dane, dict) and isinstance(dane.get("pliki"), list):
                dane["pliki"] = BZ.bez_cen(dane["pliki"])
                r.set_data(json.dumps(dane, ensure_ascii=False))
            return r
        if modul != "projekty":
            return r
        dane = json.loads(r.get_data(as_text=True))
        dane = BZ.bez_cen(dane)
        if isinstance(dane, dict):
            dane["bez_cen"] = True
        r.set_data(json.dumps(dane, ensure_ascii=False))
    except Exception:
        S.logging.exception("Filtr cen")
    return r


@bp.get("/api/projekty/<pid>/przedmiar.xlsx")
@S.wymaga_logowania
def przedmiar_xlsx(pid):
    """Przedmiar robót z kosztorysu projektu – opis, jednostka i ilość, bez cen (dla każdej roli z dostępem do projektu)."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    dane = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), None)
    if not dane:
        return jsonify({"blad": "Projekt nie ma jeszcze kosztorysu."}), 404
    m = S.meta(pid)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Przedmiar"
    ws["A1"] = f"Przedmiar robót – {m.get('nazwa', '')}"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Zestawienie ilości (bez cen)."
    nag = ["Lp.", "Podstawa", "Opis pozycji", "j.m.", "Ilość"]
    for i, h in enumerate(nag, 1):
        c = ws.cell(4, i, h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
    r, lp = 5, 0
    for dz in dane.get("dzialy") or []:
        ws.cell(r, 1, str(dz.get("nazwa") or "")).font = Font(bold=True)
        r += 1
        for p in dz.get("pozycje") or []:
            lp += 1
            for i, v in enumerate([lp, p.get("podstawa", ""), p.get("opis", ""), p.get("jm", ""), p.get("ilosc")], 1):
                ws.cell(r, i, v)
            r += 1
    for k, sz in zip("ABCDE", (6, 18, 80, 8, 12)):
        ws.column_dimensions[k].width = sz
    b = io.BytesIO()
    wb.save(b)
    b.seek(0)
    nazwa = re.sub(r"[^\w\-]+", "_", str(m.get("nazwa") or "projekt"))[:60]
    return send_file(b, as_attachment=True, download_name=f"Przedmiar_{nazwa}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ============================================================ H1-07: hasła
STRONA_HASLA = """<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zmiana hasła – Bidivia</title><style>
:root{--navy:#071F49;--tlo:#f4f6fb;--tekst:#14213d;--blad:#b42318;--blad-tlo:#fdecea;--ok:#14532d;--ok-tlo:#e7f6ec;--ramka:#d0d7e2}
@media (prefers-color-scheme: dark){:root{--tlo:#0b1220;--tekst:#e6ebf5;--ramka:#33415c;--blad-tlo:#3b1212;--ok-tlo:#0f2a19;--ok:#9be3b4;--blad:#ff9d94}}
*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--tlo);color:var(--tekst)}
main{max-width:460px;margin:48px auto;padding:0 16px}h1{font-size:22px;margin:0 0 8px}p{line-height:1.5;font-size:15px}
form{background:rgba(127,127,127,.06);border:1px solid var(--ramka);border-radius:12px;padding:18px}
label{display:block;font-weight:700;font-size:14px;margin:12px 0 4px}input{width:100%;font-size:16px;padding:11px 12px;border:1px solid var(--ramka);border-radius:8px;background:transparent;color:inherit}
button{margin-top:16px;width:100%;font-size:16px;font-weight:700;padding:12px;border:0;border-radius:10px;background:var(--navy);color:#fff;cursor:pointer}
.blad{color:var(--blad);background:var(--blad-tlo);border-radius:8px;padding:8px 12px;margin-top:12px;font-weight:600}
.ok{color:var(--ok);background:var(--ok-tlo);border-radius:8px;padding:8px 12px;margin-top:12px;font-weight:600}
.ukryj{display:none}a{color:inherit}.dol{display:flex;justify-content:space-between;margin-top:14px;font-size:14px}
</style></head><body><main>
<h1>Zmiana hasła</h1>
<p id="opis">__OPIS__</p>
<form id="f" class="__FORM__" autocomplete="on">
  <input type="text" name="username" autocomplete="username" value="__LOGIN__" hidden>
  <label for="stare">Obecne hasło__TYMCZ__</label><input id="stare" type="password" autocomplete="current-password" required>
  <label for="nowe">Nowe hasło (co najmniej 10 znaków)</label><input id="nowe" type="password" autocomplete="new-password" minlength="10" required>
  <label for="nowe2">Powtórz nowe hasło</label><input id="nowe2" type="password" autocomplete="new-password" minlength="10" required>
  <button type="submit" id="zapisz">Zmień hasło</button>
  <div id="komunikat" class="ukryj" role="alert"></div>
</form>
<div class="dol"><a href="/" id="powrot" class="__POWROT__">← Wróć do programu</a>
<form method="post" action="/logout" style="all:unset"><button type="submit" style="all:unset;cursor:pointer;text-decoration:underline">Wyloguj</button></form></div>
</main><script>
document.getElementById("f").addEventListener("submit", async e => {
  e.preventDefault();
  const k = document.getElementById("komunikat"), n = document.getElementById("nowe").value;
  const pokaz = (t, ok) => { k.textContent = t; k.className = ok ? "ok" : "blad"; };
  if (n !== document.getElementById("nowe2").value) return pokaz("Nowe hasła różnią się – wpisz je ponownie.");
  const r = await fetch("/api/haslo/zmien", {method: "POST", headers: {"Content-Type": "application/json", "X-Agent": "1"},
    body: JSON.stringify({stare: document.getElementById("stare").value, nowe: n})}).catch(() => null);
  if (!r) return pokaz("Brak połączenia z programem.");
  if (r.status === 401) { location.href = "/login"; return; }
  const d = await r.json().catch(() => ({}));
  if (!r.ok) return pokaz(d.blad || "Nie udało się zmienić hasła.");
  pokaz("Hasło zmienione. Za chwilę wrócisz do programu.", true);
  setTimeout(() => location.href = "/", 1200);
});
</script></body></html>"""


def _html(t):
    import html
    return html.escape(str(t or ""), quote=True)


@bp.get("/zmien-haslo")
def strona_zmiany_hasla():
    if not S.rola_sesji():
        return redirect("/login")
    wymus = bool(session.get("zmien_haslo"))
    if session.get("konto", "env") == "env":
        opis, form = ("Hasło właściciela programu jest ustawione na serwerze (zmienna APP_PASSWORD_HASH albo APP_PASSWORD) – zmienia się je "
                      "w ustawieniach serwera (instrukcja: WDROZENIE.md)."), "ukryj"
    elif wymus:
        opis, form = ("Logujesz się hasłem tymczasowym nadanym przez administratora. Ustaw własne hasło – dopiero wtedy otworzy się program."), ""
    else:
        opis, form = "Po zmianie hasła program wyloguje Cię na innych urządzeniach.", ""
    h = (STRONA_HASLA.replace("__OPIS__", _html(opis)).replace("__FORM__", form).replace("__LOGIN__", _html(session.get("login")))
         .replace("__TYMCZ__", " (tymczasowe)" if wymus else "").replace("__POWROT__", "ukryj" if wymus else ""))
    r = Response(h, mimetype="text/html")
    r.headers["Cache-Control"] = "no-store"
    return r


PROBY_ZMIANY = {}


@bp.post("/api/haslo/zmien")
@S.wymaga_logowania
def haslo_zmien():
    """Zmiana własnego hasła: obecne hasło + nowe (co najmniej 10 znaków, inne niż obecne i niż login). Inne urządzenia – wylogowane."""
    if session.get("konto", "env") == "env":
        return jsonify({"blad": "Hasło właściciela programu ustawia się na serwerze (APP_PASSWORD_HASH) – patrz WDROZENIE.md."}), 400
    j = request.json or {}
    stare, nowe = str(j.get("stare") or ""), str(j.get("nowe") or "")
    login = session.get("login")
    teraz = time.time()
    PROBY_ZMIANY[login] = [t for t in PROBY_ZMIANY.get(login, []) if teraz - t < 900]
    if len(PROBY_ZMIANY[login]) >= 10:
        return jsonify({"blad": "Zbyt wiele nieudanych prób – spróbuj ponownie za 15 minut."}), 429
    blad = BZ.blad_hasla(nowe, login)
    if blad:
        return jsonify({"blad": blad}), 400
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        u = next((x for x in lista if x.get("login") == login), None)
        if not u:
            return jsonify({"blad": "Nie ma takiego konta."}), 404
        try:
            _, it, sol, h = u.get("hash", "").split("$")
            zgodne = S.hmac.compare_digest(S.hash_hasla(stare.strip(), sol, int(it)).split("$")[3], h)
        except ValueError:
            zgodne = False
        if not zgodne:
            PROBY_ZMIANY[login].append(teraz)
            return jsonify({"blad": "Obecne hasło jest nieprawidłowe."}), 400
        if nowe.strip() == stare.strip():
            return jsonify({"blad": "Nowe hasło musi się różnić od obecnego."}), 400
        u["hash"] = S.hash_hasla(nowe.strip())
        u.pop("haslo_tymczasowe", None)
        u.pop("tymczasowe_do", None)
        u["wersja"] = u.get("wersja", 0) + 1  # inne urządzenia – wylogowane; to urządzenie zostaje zalogowane
        u["haslo_zmienione"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        S.pisz(S.F_UZYT, lista)
    session["wersja"] = u["wersja"]
    session.pop("zmien_haslo", None)
    PROBY_ZMIANY.pop(login, None)
    S.zapisz_aktywnosc(login, "Zmiana własnego hasła", konto=login)
    return jsonify({"ok": True})


@bp.post("/api/uzytkownicy/reset-hasla")
@S.wymaga_logowania
@S.tylko_admin
def haslo_reset():
    """Reset hasła przez administratora (właściciel – każde konto, administrator konta – osoby ze swojej firmy, bez administratorów):
    jednorazowe hasło tymczasowe (72 h) z wymuszoną zmianą przy logowaniu. E-mail – tylko gdy skonfigurowano SMTP i login jest adresem
    e-mail; inaczej hasło pokazuje się administratorowi, który przekazuje je osobiście."""
    import trasy_admin as TA
    j = request.json or {}
    login = str(j.get("login") or "")
    odm = TA._uzytkownik_firmy(login)
    if odm or (not S.wlasciciel() and login.lower() not in S.UWIERZ.czlonkowie_firmy()):
        return jsonify({"blad": odm or "Nie ma takiego użytkownika w Twojej firmie."}), 403
    tymcz = BZ.haslo_tymczasowe()
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        u = next((x for x in lista if x.get("login", "").lower() == login.lower()), None)
        if not u:
            return jsonify({"blad": "Nie ma takiego użytkownika."}), 404
        u["hash"] = S.hash_hasla(tymcz)
        u["haslo_tymczasowe"] = True
        u["tymczasowe_do"] = (dt.datetime.now() + dt.timedelta(hours=BZ.WAZNOSC_TYMCZASOWEGO_H)).strftime("%Y-%m-%d %H:%M")
        u["wersja"] = u.get("wersja", 0) + 1  # dotychczasowe sesje tej osoby – wylogowane
        S.pisz(S.F_UZYT, lista)
    S.zapisz_aktywnosc(session.get("login"), "Reset hasła użytkownika", u["login"], konto=S.konto_biezace())
    wyslano = False
    c = S.cfg()
    if j.get("wyslij") and c.get("smtp_serwer") and re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", u["login"], re.I):
        try:
            from email.message import EmailMessage
            msg = EmailMessage()
            msg["Subject"] = "Hasło tymczasowe do programu"
            msg["From"] = c.get("smtp_nadawca") or c.get("firma_email") or c.get("smtp_login") or ""
            msg["To"] = u["login"]
            msg.set_content(f"Administrator ustawił Ci hasło tymczasowe: {tymcz}\n\nJest ważne {BZ.WAZNOSC_TYMCZASOWEGO_H} godziny. "
                            "Po zalogowaniu program poprosi o ustawienie własnego hasła.")
            S.MH.wyslij_smtp(c, [msg])
            wyslano = True
        except Exception as e:
            S.logging.warning("Reset hasła – e-mail nie wysłany: %s", e)
    wyn = {"ok": True, "login": u["login"], "wazne_do": u["tymczasowe_do"], "wyslano": wyslano}
    if not wyslano:
        wyn["haslo"] = tymcz
    return jsonify(wyn)


# ============================================================ H1-10: RODO w kadrach (art. 94 pkt 9b KP)
def _rodo():
    return BZ.rodo_lista(S.dane_prac_konta()["pracownicy"])


@bp.get("/api/kadry/rodo")
@S.wymaga_logowania
def kadry_rodo():
    L = _rodo()
    return jsonify({"do_usuniecia": [x for x in L if x["do_usuniecia"]], "przechowywane": [x for x in L if not x["do_usuniecia"]],
                    "moze_usuwac": S.rola_sesji() == "admin",
                    "zasada": "Dokumentację pracowniczą przechowuje się 10 lat od końca roku kalendarzowego, w którym ustał stosunek pracy "
                              "(art. 94 pkt 9b Kodeksu pracy – zatrudnieni od 1.01.2019). Zatrudnieni w latach 1999–2018 – 50 lat, chyba że "
                              "pracodawca złożył raport informacyjny ZUS RIA (wtedy 10 lat); zatrudnieni przed 1999 r. – 50 lat. Po upływie "
                              "okresu dokumentację niszczy się (RODO art. 5 ust. 1 lit. e – ograniczenie przechowywania)."})


@bp.post("/api/kadry/rodo/usun")
@S.wymaga_logowania
@S.tylko_admin
def kadry_rodo_usun():
    """Trwałe usunięcie dokumentów pracowniczych po upływie okresu przechowywania – tylko administrator, z potwierdzeniem w programie."""
    j = request.json or {}
    if j.get("potwierdzam") is not True:
        return jsonify({"blad": "Potwierdź trwałe usunięcie – dokumentów nie da się przywrócić.", "potwierdz": True}), 400
    prac, id_ = str(j.get("pracownik") or ""), str(j.get("id") or "")
    do_usun = [x for x in _rodo() if x["pracownik"] == prac and (id_ in ("*", x["id"]))]
    if not do_usun:
        return jsonify({"blad": "Nie ma takiego dokumentu w archiwum kadr."}), 404
    if any(not x["do_usuniecia"] for x in do_usun):
        return jsonify({"blad": "Okres przechowywania tej dokumentacji jeszcze trwa – nie można jej trwale usunąć."}), 400
    ids = {x["id"] for x in do_usun}
    usunieto = 0
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, prac)
        if not p:
            return jsonify({"blad": "Nie ma takiego pracownika."}), 404
        docs = (p.get("kadry") or {}).get("dokumenty") or []
        for x in [x for x in docs if x.get("id") in ids]:
            if x.get("plik"):
                sc = os.path.join(S.DIR_KADRY, os.path.basename(p["id"]), os.path.basename(x["plik"]))
                try:
                    os.remove(sc)
                except OSError:
                    pass
            usunieto += 1
        p["kadry"]["dokumenty"] = [x for x in docs if x.get("id") not in ids]
        S.pisz(S.F_PRAC, d)
    S.zapisz_aktywnosc(session.get("login"), "Kadry: trwałe usunięcie dokumentacji po okresie przechowywania (RODO)",
                       f"dokumentów: {usunieto}", konto=S.konto_biezace())
    return jsonify({"ok": True, "usunieto": usunieto})


def liczba_rodo():
    try:
        return sum(1 for x in _rodo() if x["do_usuniecia"])
    except Exception:
        return 0


# ============================================================ H1-12: godziny pracy na budowie (także udostępnionej innemu kontu)
def _wl(pid):
    return (S.meta(pid).get("wlasciciel") or S.login_admina())


def _pracownicy_budowy(pid):
    wl = _wl(pid).lower()
    return [p for p in S.dane_prac()["pracownicy"] if S.wlasciciel_prac(p).lower() == wl and not p.get("archiwum")]


def _widzi_stawki():
    return S.moze("place") or S.moze("finanse")


@bp.get("/api/projekty/<pid>/godziny")
@S.wymaga_logowania
def godziny_budowy(pid):
    """Pracownicy właściciela projektu i godziny wpisane na tej budowie (tylko ten projekt). Stawki – tylko z dostępem do Płac albo Finansów."""
    if S.EDYCJA != "pelna":
        return jsonify({"blad": "Funkcja niedostępna w tej edycji."}), 404
    st = _widzi_stawki()
    m = S.meta(pid)
    prac = [{k: p.get(k) for k in ("id", "imie", "stanowisko") + (("stawka",) if st else ())} for p in _pracownicy_budowy(pid)]
    wpisy = S.robocizna_projektu(pid, m.get("nazwa"))
    if not st:
        wpisy = [{k: v for k, v in w.items() if k not in ("stawka", "kwota")} for w in wpisy]
    ja = str(session.get("login") or "")
    wpisy = [dict(w, moje=(w.get("kto") == ja)) for w in sorted(wpisy, key=lambda w: (w.get("data") or "", w.get("imie") or ""), reverse=True)]
    return jsonify(S.ukryj_innych({"pracownicy": prac, "wpisy": wpisy, "stawki": st, "udostepniony": _wl(pid).lower() != S.konto_biezace().lower(),
                                   "moze_wpisywac": S.moze("realizacja", 2) and not S.UWIERZ.tylko_odczyt()}))


@bp.post("/api/projekty/<pid>/godziny")
@S.wymaga_logowania
def godziny_budowy_dodaj(pid):
    """Wpis godzin pracownika właściciela projektu na tej budowie – stawka z kartoteki pracownika (osoba wpisująca jej nie widzi)."""
    if S.EDYCJA != "pelna":
        return jsonify({"blad": "Funkcja niedostępna w tej edycji."}), 404
    import trasy_firma as TF
    j = request.json or {}
    try:
        data = dt.date.fromisoformat(str(j.get("data") or ""))
        godz = float(str(j.get("godziny") or "").replace(",", "."))
    except ValueError:
        return jsonify({"blad": "Uzupełnij datę i liczbę godzin."}), 400
    if not (0 < godz <= 24):
        return jsonify({"blad": "Liczba godzin musi być od 0 do 24."}), 400
    if data > dt.date.today():
        return jsonify({"blad": "Nie można wpisać godzin z przyszłą datą."}), 400
    m = S.meta(pid)
    with S.BLOKADA:
        d = S.dane_prac()
        swoi = {p["id"]: p for p in _pracownicy_budowy(pid)}
        p = next((x for x in d["pracownicy"] if x["id"] == j.get("pracownik") and x["id"] in swoi), None)
        if not p:
            return jsonify({"blad": "Wybierz pracownika tej budowy."}), 400
        blad, ostrz = TF._kontrola_doby(d, p["id"], data.isoformat(), godz)
        if blad:
            return jsonify({"blad": blad}), 400
        stawka = float(p.get("stawka") or 0)
        w = {"id": uuid.uuid4().hex[:10], "data": data.isoformat(), "pracownik": p["id"], "imie": p["imie"], "godziny": round(godz, 2),
             "stawka": S._kwota(stawka), "kwota": S._kwota(godz * stawka), "projekt": m.get("nazwa", ""), "projekt_id": pid,
             "opis": str(j.get("opis") or "")[:200], "kto": session.get("login", "")}
        d["wpisy"].append(w)
        S.pisz(S.F_PRAC, d)
    if not _widzi_stawki():
        w = {k: v for k, v in w.items() if k not in ("stawka", "kwota")}
    return jsonify(dict(w, ostrzezenie=ostrz) if ostrz else w)


@bp.post("/api/projekty/<pid>/godziny/usun")
@S.wymaga_logowania
def godziny_budowy_usun(pid):
    """Usunięcie wpisu godzin z tej budowy: własny wpis albo (właściciel projektu / jego administrator) każdy wpis budowy."""
    wid = str((request.json or {}).get("id") or "")
    ja = str(session.get("login") or "")
    pelny = S.wlasciciel() or _wl(pid).lower() == S.konto_biezace().lower()
    with S.BLOKADA:
        d = S.dane_prac()
        swoi = {p["id"] for p in _pracownicy_budowy(pid)}
        w = next((x for x in d["wpisy"] if x.get("id") == wid and x.get("projekt_id") == pid and x.get("pracownik") in swoi), None)
        if not w:
            return jsonify({"blad": "Nie ma takiego wpisu."}), 404
        if not pelny and w.get("kto") != ja:
            return jsonify({"blad": "Możesz usunąć tylko swoje wpisy."}), 403
        d["wpisy"] = [x for x in d["wpisy"] if x is not w]
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


# ============================================================ migracje danych tej wersji
def migracja_h81():
    """Jednorazowe (idempotentne) migracje:
    1) H1-01 – każde konto dostaje pole „firma”: administrator konta (rola „Administrator”, nie właściciel) – własna firma (jego login),
       pozostali – firma właściciela programu (puste pole). Dane kont nie są przenoszone ani usuwane; administratorzy kont tracą tylko
       wgląd w inne firmy (projekty, użytkownicy, hasła, role).
    2) H1-03 – zapisane role: z nadpisań ról wbudowanych usunięte wymuszane dawniej poziomy (Płace/Kadry/… 2), role własne – zapisane wprost.
    3) H1-11 – profile firm z przykładowym opisem „Firma budowlana ze Świdnicy…” – opis wyczyszczony (zostaje podpowiedzią w pustym polu)."""
    wyn = {"konta": 0, "role": False, "profile": 0}
    with S.BLOKADA:
        lista = S.uzytkownicy_lista()
        zm = False
        for u in lista:
            if "firma" not in u:
                u["firma"] = u.get("login", "") if u.get("rola") == "admin" else ""
                zm = True
                wyn["konta"] += 1
        if zm:
            S.pisz(S.F_UZYT, lista)
        role_, zm_r = S.UPR.migruj_zapisane_role(S.czytaj(S.F_ROLE, {}))
        if zm_r and any(not k.startswith("_") for k in role_):
            S.pisz(S.F_ROLE, role_)
            wyn["role"] = True
        przyklad = str(S.KONF.core.DEFAULT_CONFIG.get("profil_firmy") or "").strip()
        for login in S.wszystkie_konta():
            p = S.plik_ustawien_konta(login)
            c = S.czytaj(p, None)
            if isinstance(c, dict) and przyklad and str(c.get("profil_firmy") or "").strip() == przyklad:
                c["profil_firmy"] = ""
                S.pisz(p, c)
                wyn["profile"] += 1
    if any(wyn.values()):
        S.logging.info("Migracja h81: %s", wyn)
    return wyn
