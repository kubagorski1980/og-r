# -*- coding: utf-8 -*-
"""
Firma – trasy: profil firmy, logo i dokumenty, kadry i dokumenty pracowników, pracownicy i godziny pracy, płace i umowy, klienci, własny cennik.
Blueprint „firma” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import serwer as S

bp = Blueprint("firma", __name__)


@bp.get("/api/cennik-wlasny")
@S.wymaga_logowania
def cennik_wlasny():
    c = S.czytaj(S.F_CENNIK_W, {}) or {}
    poz = c.get("pozycje") or []
    return jsonify({"liczba": len(poz), "plik": c.get("plik", ""), "data": c.get("data", ""), "pozycje": poz[:2000]})


@bp.post("/api/cennik-wlasny")
@S.wymaga_logowania
def cennik_wlasny_wgraj():
    f = request.files.get("plik")
    if not f or not f.filename.lower().endswith((".xlsx", ".xlsm", ".csv", ".txt")):
        return jsonify({"blad": "Wybierz cennik w Excelu (.xlsx) albo CSV."}), 400
    try:
        poz = S.CW.wczytaj(f.filename, f.read())
    except Exception as e:
        return jsonify({"blad": f"Nie udało się odczytać pliku: {e}"}), 400
    if not poz:
        return jsonify({"blad": "Nie znaleziono pozycji. Cennik powinien mieć kolumny: opis (nazwa), j.m., cena netto – zobacz wzór."}), 400
    S.pisz(S.F_CENNIK_W, {"pozycje": poz[:20000], "plik": f.filename, "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")})
    return jsonify({"liczba": len(poz), "przyklad": poz[:5]})


@bp.post("/api/cennik-wlasny/usun")
@S.wymaga_logowania
def cennik_wlasny_usun():
    S.pisz(S.F_CENNIK_W, {})
    return jsonify({"ok": True})


@bp.get("/api/cennik-wlasny/wzor.xlsx")
@S.wymaga_logowania
def cennik_wzor():
    import io
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cennik"
    ws.append(["Kod (opcjonalnie)", "Opis pozycji", "j.m.", "Cena netto [zł]"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for w in (["", "Docieplenie ścian styropianem grafitowym gr. 15 cm z tynkiem cienkowarstwowym", "m2", 210],
              ["", "Tynk silikonowy cienkowarstwowy", "m2", 48], ["", "Montaż okna PCV z obróbką ościeży", "szt", 450],
              ["", "Rusztowanie elewacyjne – montaż i demontaż", "m2", 18], ["", "Robocizna ogólnobudowlana", "r-g", 65]):
        ws.append(w)
    for k, sz in zip("ABCD", (16, 70, 8, 16)):
        ws.column_dimensions[k].width = sz
    b = io.BytesIO()
    wb.save(b)
    b.seek(0)
    return send_file(b, as_attachment=True, download_name="Wzor_cennika.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@bp.post("/api/pracownicy/zakres")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel
def pracownicy_zakres():
    session["prac_wszystkie"] = bool((request.json or {}).get("wszystkie"))
    return jsonify({"wszystkie": session["prac_wszystkie"]})


@bp.get("/api/pracownicy")
@S.wymaga_logowania
def pracownicy():
    d = S.dane_prac_konta()
    d["wszystkie_konta"] = S.wlasciciel() and bool(session.get("prac_wszystkie"))
    if d["wszystkie_konta"]:
        d["pracownicy"] = [dict(p, wlasciciel=S.wlasciciel_prac(p)) for p in d["pracownicy"]]
    if not S.moze("place"):  # warunki umów i wynagrodzenia – tylko z dostępem do płac
        d["pracownicy"] = [{k: v for k, v in p.items() if k != "umowa"} for p in d["pracownicy"]]
    if not widzi_stawki():  # H1-03: rola bez Płac i bez Finansów (np. kierownik budowy) – bez stawek i kwot
        d["pracownicy"] = [{k: v for k, v in p.items() if k != "stawka"} for p in d["pracownicy"]]
        d["wpisy"] = [{k: v for k, v in w.items() if k not in ("stawka", "kwota")} for w in d.get("wpisy") or []]
    d["stawki"] = widzi_stawki()
    if not S.moze("kadry"):
        d["pracownicy"] = [{k: v for k, v in p.items() if k != "kadry"} for p in d["pracownicy"]]
    d["pracownicy"] = [p for p in d["pracownicy"] if not p.get("archiwum")]
    return jsonify(d)


def widzi_stawki():
    """Stawki godzinowe i kwoty robocizny: rola z dostępem do Płac albo Finansów (H1-03)."""
    return S.moze("place") or S.moze("finanse")


@bp.post("/api/pracownicy")
@S.wymaga_logowania
def pracownicy_zapisz():
    lista = []
    stare_ = {p["id"]: p for p in S.dane_prac()["pracownicy"]}
    for p in request.json.get("pracownicy", []):
        imie = str(p.get("imie", "")).strip()
        if not imie:
            continue
        if not widzi_stawki():  # rola bez stawek: stawka z zapisanych danych (nowy pracownik – 0, ustala ją osoba z dostępem do Płac)
            p = dict(p, stawka=(stare_.get(p.get("id")) or {}).get("stawka", 0))
        try:
            stawka = S._kwota(str(p.get("stawka", 0) or 0).replace(" ", "").replace("\u00a0", "").replace(",", "."))
        except ValueError:
            return jsonify({"blad": f"Błędna stawka: {imie}"}), 400
        if stawka < 0:
            return jsonify({"blad": f"Stawka nie może być ujemna: {imie}"}), 400
        lista.append({"id": p.get("id") or uuid.uuid4().hex[:8], "imie": imie[:80], "stawka": stawka,
                      "stanowisko": str(p.get("stanowisko", ""))[:80], "telefon": str(p.get("telefon", ""))[:40],
                      "uwagi": str(p.get("uwagi", ""))[:200]})
    with S.BLOKADA:
        d = S.dane_prac()
        stare = {p["id"]: p for p in d["pracownicy"]}
        cudze = [p for p in d["pracownicy"] if not S.widoczny_prac(p)]  # pracownicy innych kont – bez zmian
        wynik = []
        for p in lista:
            st = stare.get(p["id"])
            if st and not S.widoczny_prac(st):
                continue  # nie można edytować cudzego pracownika
            p.update({k: v for k, v in (st or {}).items() if k not in p})  # zachowaj umowę, kartotekę kadrową itd.
            p.setdefault("wlasciciel", S.konto_biezace())
            wynik.append(p)
        ids = {p["id"] for p in wynik}
        for p in d["pracownicy"]:  # własni pracownicy usunięci z tabeli trafiają do archiwum, a nie znikają
            if S.widoczny_prac(p) and p["id"] not in ids:
                wynik.append(p if p.get("archiwum") else dict(p, archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                  archiwum_kto=session.get("login", "")))
        d["pracownicy"] = cudze + wynik
        S.pisz(S.F_PRAC, d)
    return pracownicy()


@bp.post("/api/godziny")
@S.wymaga_logowania
def godziny_dodaj():
    j = request.json
    try:
        data = dt.date.fromisoformat(j.get("data", ""))
        godz = float(str(j.get("godziny", "")).replace(",", "."))
        stawka = float(str(j.get("stawka", "")).replace(",", ".")) if widzi_stawki() else 0.0  # bez stawek – stawka pracownika (niżej)
    except ValueError:
        return jsonify({"blad": "Uzupełnij datę, liczbę godzin i stawkę."}), 400
    if not (0 < godz <= 24) or stawka < 0:
        return jsonify({"blad": "Liczba godzin musi być od 0 do 24, stawka nieujemna."}), 400
    m_ = S.projekt_dostepny(j.get("projekt_id")) if j.get("projekt_id") else None
    if j.get("projekt_id") and not m_:  # tylko projekty, do których konto ma dostęp (bez nazwy cudzego projektu w odpowiedzi)
        return jsonify({"blad": "Nie ma takiego projektu."}), 400
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, j.get("pracownik"))
        if not p:
            return jsonify({"blad": "Wybierz pracownika."}), 400
        blad, ostrz = _kontrola_doby(d, p["id"], data.isoformat(), godz)
        if blad:
            return jsonify({"blad": blad}), 400
        if not S.moze("place", 2):
            stawka = float(p["stawka"])  # stawkę może zmieniać tylko administrator
        w = {"id": uuid.uuid4().hex[:10], "data": data.isoformat(), "pracownik": p["id"], "imie": p["imie"],
             "godziny": round(godz, 2), "stawka": S._kwota(stawka), "kwota": S._kwota(godz * stawka),
             "projekt": (m_ or {}).get("nazwa") or str(j.get("projekt", ""))[:120],
             "projekt_id": j.get("projekt_id") or "", "opis": str(j.get("opis", ""))[:200],
             "kto": session.get("login", "")}
        d["wpisy"].append(w)
        S.pisz(S.F_PRAC, d)
    if not widzi_stawki():
        w = {k: v for k, v in w.items() if k not in ("stawka", "kwota")}
    return jsonify(dict(w, ostrzezenie=ostrz) if ostrz else w)


def _kontrola_doby(d, prac, data, godz, bez=None):
    """Suma godzin pracownika w danym dniu (wszystkie budowy): ponad 24 h – błąd danych; ponad 13 h – ostrzeżenie
    (art. 132 § 1 Kodeksu pracy: co najmniej 11 godzin nieprzerwanego odpoczynku w każdej dobie)."""
    suma = round(sum(float(w.get("godziny") or 0) for w in d["wpisy"] if w.get("pracownik") == prac and w.get("data") == data and w.get("id") != bez) + godz, 2)
    sp = f"{suma:g}".replace(".", ",")
    if suma > 24:
        return (f"Łącznie {sp} h w jednym dniu ({dt.date.fromisoformat(data):%d.%m.%Y}) – doba ma 24 godziny. Sprawdź wcześniejsze wpisy tego pracownika.", "")
    if suma > 13:
        return ("", f"Pracownik ma {sp} h pracy {dt.date.fromisoformat(data):%d.%m.%Y} – przy umowie o pracę to mniej niż 11 godzin odpoczynku w dobie "
                    "(art. 132 § 1 Kodeksu pracy). Sprawdź wpis albo rozlicz pracę w nadgodzinach zgodnie z przepisami.")
    return ("", "")


@bp.post("/api/godziny/edytuj")
@S.wymaga_logowania
def godziny_edytuj():
    """Zmiana wpisu roboczogodzin (data, godziny, stawka, projekt, opis)."""
    j = request.json or {}
    if j.get("projekt_id") and not S.projekt_dostepny(j.get("projekt_id")):
        return jsonify({"blad": "Nie ma takiego projektu."}), 400
    with S.BLOKADA:
        d = S.dane_prac()
        moi = {p["id"]: p for p in d["pracownicy"] if S.widoczny_prac(p)}
        w = next((x for x in d["wpisy"] if x["id"] == j.get("id") and x.get("pracownik") in moi), None)
        if not w:
            return jsonify({"blad": "Nie ma takiego wpisu."}), 404
        try:
            if "data" in j:
                dt.date.fromisoformat(j["data"])
                w["data"] = j["data"]
            if "godziny" in j:
                w["godziny"] = float(str(j["godziny"]).replace(",", "."))
                assert 0 < w["godziny"] <= 24
            if "stawka" in j and widzi_stawki():
                w["stawka"] = float(str(j["stawka"]).replace(",", "."))
                assert w["stawka"] >= 0
        except (ValueError, AssertionError):
            return jsonify({"blad": "Sprawdź datę, liczbę godzin (0–24) i stawkę (nieujemna)."}), 400
        if j.get("pracownik") in moi:
            w["pracownik"], w["imie"] = j["pracownik"], moi[j["pracownik"]]["imie"]
        blad, ostrz = _kontrola_doby(d, w["pracownik"], w["data"], float(w["godziny"]), bez=w["id"])
        if blad:
            return jsonify({"blad": blad}), 400
        for k in ("opis", "projekt_id", "projekt"):
            if k in j:
                w[k] = str(j[k] or "")[:300]
        w["kwota"] = S.MO.zaokr(float(w["godziny"]) * float(w["stawka"]))
        S.pisz(S.F_PRAC, d)
    if not widzi_stawki():
        w = {k: v for k, v in w.items() if k not in ("stawka", "kwota")}
    return jsonify(dict(w, ostrzezenie=ostrz) if ostrz else w)


@bp.post("/api/pracownicy/usun")
@S.wymaga_logowania
def pracownik_usun():
    """Usunięcie pracownika – trafia do Archiwum (z historią godzin); można go przywrócić."""
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, (request.json or {}).get("id"))
        if not p:
            return jsonify({"blad": "Nie ma takiego pracownika."}), 404
        p.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), archiwum_kto=session.get("login", ""))
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


@bp.post("/api/godziny/usun")
@S.wymaga_logowania
def godziny_usun():
    ids = set(request.json.get("ids", []))
    with S.BLOKADA:
        d = S.dane_prac()
        moi = {p["id"] for p in d["pracownicy"] if S.widoczny_prac(p)}
        d["wpisy"] = [w for w in d["wpisy"] if not (w["id"] in ids and w.get("pracownik") in moi)]
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


@bp.get("/api/godziny")
@S.wymaga_logowania
def godziny():
    od, do = request.args.get("od", "0000"), request.args.get("do", "9999")
    wpisy, lista = S.rozliczenie(od, do)
    wyn = {"wpisy": wpisy, "podsumowanie": lista, "razem_godziny": round(sum(x["godziny"] for x in lista), 2),
           "razem_kwota": S._kwota(sum(x["kwota"] for x in lista)), "stawki": widzi_stawki()}
    if not widzi_stawki():  # H1-03: bez stawek i kwot
        wyn.update(wpisy=[{k: v for k, v in w.items() if k not in ("stawka", "kwota")} for w in wpisy],
                   podsumowanie=[{k: v for k, v in x.items() if k != "kwota"} for x in lista], razem_kwota=None)
    return jsonify(wyn)


@bp.get("/api/godziny/eksport")
@S.wymaga_logowania
def godziny_eksport():
    import io
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    od, do = request.args.get("od", "0000-01-01"), request.args.get("do", "9999-12-31")
    wpisy, lista = S.rozliczenie(od, do)
    if not widzi_stawki():  # H1-03: eksport bez stawek (kolumny kwot puste)
        wpisy = [dict(w, stawka=None) for w in wpisy]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Podsumowanie"
    b = Font(bold=True)
    ws["A1"] = f"Rozliczenie godzin pracy {od} – {do}"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Kwoty wg stawek godzinowych (bez przeliczeń ZUS/PIT)."
    for i, h in enumerate(["Pracownik", "Dni", "Godziny", "Kwota wg stawek [zł]"], 1):
        c = ws.cell(4, i, h)
        c.font = b
        c.fill = PatternFill("solid", fgColor="D9E1F2")
    r = 5
    for x in lista:
        ws.cell(r, 1, x["imie"])
        ws.cell(r, 2, x["dni"])
        ws.cell(r, 5, x["pracownik"])  # identyfikator – dwie osoby o tym samym imieniu i nazwisku nie sumują się razem
        ws.cell(r, 3, f"=SUMIF(Ewidencja!H:H,E{r},Ewidencja!D:D)")
        ws.cell(r, 4, f"=SUMIF(Ewidencja!H:H,E{r},Ewidencja!F:F)")
        ws.cell(r, 4).number_format = "#,##0.00"
        r += 1
    ws.cell(r, 1, "RAZEM").font = b
    ws.cell(r, 3, f"=SUM(C5:C{r - 1})").font = b
    ws.cell(r, 4, f"=SUM(D5:D{r - 1})").font = b
    ws.cell(r, 4).number_format = "#,##0.00"
    for k, s_ in zip("ABCD", (32, 8, 12, 20)):
        ws.column_dimensions[k].width = s_
    ws.column_dimensions["E"].hidden = True
    e = wb.create_sheet("Ewidencja")
    for i, h in enumerate(["Data", "Pracownik", "Projekt / budowa", "Godziny", "Stawka [zł/h]", "Kwota [zł]", "Opis", "ID pracownika"], 1):
        c = e.cell(1, i, h)
        c.font = b
        c.fill = PatternFill("solid", fgColor="D9E1F2")
    for j, w in enumerate(wpisy, 2):
        for i, v in enumerate([dt.date.fromisoformat(w["data"]), w["imie"], w["projekt"], w["godziny"], w["stawka"],
                               f"=ROUND(D{j}*E{j},2)", w["opis"], w["pracownik"]], 1):
            e.cell(j, i, v)
        e.cell(j, 1).number_format = "DD.MM.YYYY"
        e.cell(j, 6).number_format = "#,##0.00"
    for k, s_ in zip("ABCDEFG", (12, 28, 30, 10, 12, 12, 40)):
        e.column_dimensions[k].width = s_
    e.column_dimensions["H"].hidden = True
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"Rozliczenie_godzin_{od}_{do}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@bp.get("/api/firma")
@S.wymaga_logowania
def firma():
    c, d = S.cfg_surowy(), S.dane_firmy()
    return jsonify({"dane": {k: c.get(k, "") for k in ("firma_nazwa", "firma_adres", "firma_nip", "firma_regon", "firma_email", "firma_tel",
                                                        "firma_osoba", "profil_firmy")} | {"www": d.get("www", ""), "rachunek": d.get("rachunek", ""), "godziny": d.get("godziny", "")},
                    "podpowiedz_profil": "Np. " + S.KONF.PRZYKLAD_OPISU_FIRMY,  # H1-11: przykład tylko jako podpowiedź w pustym polu
                    "logo": os.path.isfile(os.path.join(S.DIR_FIRMA, "logo.png")),
                    **{k: [x for x in d[k] if not x.get("archiwum")] for k in ("certyfikaty", "referencje", "polisy")}})


@bp.post("/api/firma")
@S.wymaga_logowania
def firma_zapisz():
    j = request.json or {}
    ostrz = ""
    if "firma_nip" in j and S.NIP.oczysc(j["firma_nip"]) and not S.NIP.poprawny(j["firma_nip"]):
        # H3-08: NIP z sumą kontrolną (nip.py); zapis nie jest blokowany – pozostałe dane profilu nie przepadają, ale komunikat jest wyraźny
        ostrz = (f"NIP „{str(j['firma_nip'])[:20]}” jest nieprawidłowy – " + ("nie ma 10 cyfr" if len(S.NIP.oczysc(j["firma_nip"])) != 10 else "błędna cyfra kontrolna")
                 + ". Sprawdź cyfry – ten NIP trafia do ofert, pism i dokumentów.")
    S.zapisz_ustawienia({k: str(j[k])[:5000] for k in ("firma_nazwa", "firma_adres", "firma_nip", "firma_regon", "firma_email", "firma_tel",
                                                      "firma_osoba", "profil_firmy") if k in j})
    with S.BLOKADA:
        d = S.dane_firmy()
        if "www" in j:
            d["www"] = str(j["www"])[:200]
        for k in ("rachunek", "godziny"):  # zamawiający: rachunek do wadium, godziny pracy – do dokumentów zamówienia
            if k in j:
                d[k] = str(j[k])[:200]
        S.pisz(S.F_FIRMA, d)
    return jsonify({"ok": True, **({"ostrzezenie": ostrz, "pole": "firma_nip"} if ostrz else {})})


@bp.post("/api/firma/logo")
@S.wymaga_logowania
def firma_logo():
    f = request.files.get("logo")
    if not f:
        return jsonify({"blad": "Wybierz plik z logo (PNG lub JPG)."}), 400
    os.makedirs(S.DIR_FIRMA, exist_ok=True)
    try:
        from PIL import Image
        im = Image.open(f.stream)
        im = im.convert("RGBA")
        im.thumbnail((800, 400))
        im.save(os.path.join(S.DIR_FIRMA, "logo.png"), "PNG")
    except Exception:
        return jsonify({"blad": "Nie udało się odczytać obrazu – użyj pliku PNG lub JPG."}), 400
    S.ustaw_logo()
    return jsonify({"ok": True})


@bp.get("/api/firma/logo.png")
@S.wymaga_logowania
def firma_logo_plik():
    p = os.path.join(S.DIR_FIRMA, "logo.png")
    if not os.path.isfile(p):
        abort(404)
    return send_file(p, mimetype="image/png", max_age=0)


@bp.post("/api/firma/dokument")
@S.wymaga_logowania
def firma_dokument():
    """Certyfikat / uprawnienie, referencja albo polisa OC – z opcjonalnym plikiem i terminem ważności."""
    rodzaj = request.form.get("rodzaj")
    if rodzaj not in S.TYPY_DOK_FIRMY:
        return jsonify({"blad": "Nieznany rodzaj dokumentu."}), 400
    pola = {k: str(request.form.get(k, ""))[:300] for k in ("nazwa", "numer", "wazny_do", "zamawiajacy", "wartosc", "rok", "suma", "ubezpieczyciel", "uwagi")}
    if not pola["nazwa"].strip():
        return jsonify({"blad": "Wpisz nazwę."}), 400
    if pola["wazny_do"].strip():  # H3-09: data ważności musi być datą – inaczej przypomnienie (30 dni przed) nigdy się nie pojawi
        try:
            pola["wazny_do"] = dt.date.fromisoformat(pola["wazny_do"].strip()[:10]).isoformat()
        except ValueError:
            return jsonify({"blad": "Nieprawidłowa data ważności – podaj datę RRRR-MM-DD."}), 400
    ostrz = ("Polisa OC bez daty ważności – program nie przypomni o jej końcu. Wpisz datę „Ważna do”."
             if rodzaj == "polisa" and not pola["wazny_do"] else "")
    with S.BLOKADA:
        d = S.dane_firmy()
        lista = d[S.TYPY_DOK_FIRMY[rodzaj]]
        x = next((y for y in lista if y["id"] == request.form.get("id")), None)
        if not x:
            x = {"id": uuid.uuid4().hex[:10], "dodano": dt.date.today().isoformat()}
            lista.append(x)
        x.update(pola)
        if request.files.get("plik"):
            x["plik"] = S._zapisz_plik_firmy(request.files["plik"], S.DIR_FIRMA, x["id"])
        S.pisz(S.F_FIRMA, d)
    return jsonify(dict(x, ostrzezenie=ostrz) if ostrz else x)


@bp.post("/api/firma/dokument/usun")
@S.wymaga_logowania
def firma_dokument_usun():
    j = request.json or {}
    with S.BLOKADA:
        d = S.dane_firmy()
        for x in d.get(S.TYPY_DOK_FIRMY.get(j.get("rodzaj"), "x"), []):
            if x["id"] == j.get("id"):
                x.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        S.pisz(S.F_FIRMA, d)
    return jsonify({"ok": True})


@bp.get("/api/firma/plik/<nazwa>")
@S.wymaga_logowania
def firma_plik(nazwa):
    p = os.path.join(S.DIR_FIRMA, os.path.basename(nazwa))
    if not os.path.isfile(p):
        abort(404)
    return send_file(p, as_attachment=True, download_name=nazwa.split("_", 1)[-1])


@bp.get("/api/kadry")
@S.wymaga_logowania
def kadry():
    wyn = []
    for p in S.dane_prac_konta()["pracownicy"]:
        if p.get("archiwum"):
            continue
        u = p.get("umowa") or {}
        k = p.get("kadry") or {}
        wyn.append({"id": p["id"], "imie": p["imie"], "stanowisko": p.get("stanowisko", ""), "telefon": p.get("telefon", ""),
                    "umowa": {x: u.get(x) for x in ("typ", "od", "do")} if u else None,
                    "kadry": {**k, "dokumenty": [x for x in k.get("dokumenty", []) if not x.get("archiwum")]}})
    return jsonify({"pracownicy": wyn, "typy": S.TYPY_DOK_KADR, "grupy_bhp": {k: v[0] for k, v in S.GRUPY_BHP.items()},
                    "miesiace_bhp": {k: v[1] for k, v in S.GRUPY_BHP.items()}})


@bp.post("/api/kadry/pracownik")
@S.wymaga_logowania
def kadry_pracownik():
    j = request.json or {}
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, j.get("id"))
        if not p:
            return jsonify({"blad": "Nie ma takiego pracownika."}), 404
        k = p.setdefault("kadry", {})
        for pole in ("zatrudniony_od", "data_ustania"):  # H1-10: daty do okresu przechowywania dokumentacji (art. 94 pkt 9b KP)
            if pole in j and j[pole]:
                try:
                    dt.date.fromisoformat(str(j[pole]))
                except ValueError:
                    return jsonify({"blad": "Nieprawidłowa data (" + ("zatrudnienia" if pole == "zatrudniony_od" else "ustania stosunku pracy") + ")."}), 400
        if j.get("zatrudniony_od") and j.get("data_ustania") and str(j["data_ustania"]) < str(j["zatrudniony_od"]):
            return jsonify({"blad": "Data ustania stosunku pracy jest wcześniejsza niż data zatrudnienia."}), 400
        for pole in ("zatrudniony_od", "data_ustania", "email", "adres", "kontakt_awaryjny", "uwagi"):
            if pole in j:
                k[pole] = str(j[pole])[:300]
        if "ria" in j:  # raport informacyjny ZUS RIA złożony (zatrudnieni 1999–2018: okres przechowywania 10 zamiast 50 lat)
            k["ria"] = bool(j["ria"])
        if "telefon" in j:
            p["telefon"] = str(j["telefon"] or "")[:40]
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


@bp.post("/api/kadry/dokument")
@S.wymaga_logowania
def kadry_dokument():
    f = request.form
    if not f.get("typ") or not f.get("pracownik"):
        return jsonify({"blad": "Wybierz pracownika i rodzaj dokumentu."}), 400
    for pole, opis in (("wazne_do", "ważności"), ("wydano", "wydania")):
        if f.get(pole):
            try:
                dt.date.fromisoformat(f[pole])
            except ValueError:
                return jsonify({"blad": f"Nieprawidłowa data {opis}."}), 400
    if f.get("wydano") and f.get("wazne_do") and f["wazne_do"] < f["wydano"]:
        return jsonify({"blad": "Data ważności jest wcześniejsza niż data wydania – sprawdź daty dokumentu."}), 400
    ostrz = ""
    wazne_auto = None
    if f.get("typ") == "szkolenie BHP" and not f.get("wazne_do"):  # H3-10: termin szkolenia okresowego z § 15 rozporządzenia MGiP z 27.07.2004
        wazne_auto = S.termin_bhp(f.get("wydano"), f.get("grupa_bhp"))
        ostrz = (f"Termin następnego szkolenia ustalono na {wazne_auto:%d.%m.%Y} – {S.GRUPY_BHP[f['grupa_bhp']][0]}; rozporządzenie MGiP z 27.07.2004 "
                 "w sprawie szkolenia w dziedzinie bhp. Pracodawca może ustalić częstsze szkolenia (§ 15 ust. 3)."
                 if wazne_auto else
                 "Wpisz termin następnego szkolenia BHP albo wybierz rodzaj stanowiska i datę szkolenia – okresowe: stanowiska robotnicze co 3 lata, "
                 "przy pracach szczególnie niebezpiecznych co rok, kierujący i inżynieryjno-techniczni co 5 lat, administracyjno-biurowi co 6 lat "
                 "(§ 15 rozporządzenia MGiP z 27.07.2004 w sprawie szkolenia w dziedzinie bhp).")
    if f.get("typ") == "badania lekarskie" and not f.get("wazne_do"):  # orzeczenie lekarskie zawsze wskazuje termin następnego badania
        ostrz = ("Wpisz termin ważności orzeczenia lekarskiego – bez aktualnego orzeczenia pracodawca nie może dopuścić pracownika do pracy "
                 "(art. 229 § 4 Kodeksu pracy), a program przypomni o terminie tylko, gdy go zna.")
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, f["pracownik"])
        if not p:
            return jsonify({"blad": "Nie ma takiego pracownika."}), 404
        docs = p.setdefault("kadry", {}).setdefault("dokumenty", [])
        x = next((y for y in docs if y["id"] == f.get("id")), None)
        if not x:
            x = {"id": uuid.uuid4().hex[:10], "dodano": dt.date.today().isoformat()}
            docs.append(x)
        for pole in ("typ", "numer", "wydano", "wazne_do", "uwagi"):
            if pole in f:
                x[pole] = str(f[pole])[:300]
        if f.get("grupa_bhp") in S.GRUPY_BHP:
            x["grupa_bhp"] = f["grupa_bhp"]
        if wazne_auto:
            x["wazne_do"] = wazne_auto.isoformat()
        if request.files.get("plik"):
            x["plik"] = S._zapisz_plik_firmy(request.files["plik"], os.path.join(S.DIR_KADRY, p["id"]), x["id"])
        S.pisz(S.F_PRAC, d)
    return jsonify(dict(x, ostrzezenie=ostrz) if ostrz else x)


@bp.post("/api/kadry/dokument/usun")
@S.wymaga_logowania
def kadry_dokument_usun():
    j = request.json or {}
    with S.BLOKADA:
        d = S.dane_prac()
        for p in d["pracownicy"]:
            if p["id"] == j.get("pracownik") and S.widoczny_prac(p):
                for x in (p.get("kadry") or {}).get("dokumenty", []):
                    if x["id"] == j.get("id"):
                        x.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


@bp.get("/api/kadry/plik/<prac>/<nazwa>")
@S.wymaga_logowania
def kadry_plik(prac, nazwa):
    if not S.moj_pracownik(S.dane_prac(), prac):
        abort(404)
    p = os.path.join(S.DIR_KADRY, os.path.basename(prac), os.path.basename(nazwa))
    if not os.path.isfile(p):
        abort(404)
    return send_file(p, as_attachment=True, download_name=nazwa.split("_", 1)[-1])


def klienci_lista():
    return S.czytaj(S.F_KLIENCI, [])


@bp.get("/api/klienci")
@S.wymaga_logowania
def klienci():
    return jsonify([k for k in klienci_lista() if not k.get("archiwum")])


@bp.post("/api/klienci")
@S.wymaga_logowania
def klienci_zapisz():
    k = request.json or {}
    if not str(k.get("nazwa", "")).strip():
        return jsonify({"blad": "Wpisz nazwę klienta (albo pobierz dane po NIP)."}), 400
    if k.get("nip") and S.NIP.oczysc(k["nip"]) and not S.NIP.poprawny(k["nip"]):
        return jsonify({"blad": "Nieprawidłowy NIP – sprawdź cyfry."}), 400
    try:
        return jsonify(S.zapisz_klienta(k, session.get("login", "")))
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400


@bp.post("/api/klienci/usun")
@S.wymaga_logowania
def klienci_usun():
    """Klient trafia do archiwum (nie jest usuwany)."""
    with S.BLOKADA:
        lista = klienci_lista()
        for x in lista:
            if x["id"] == (request.json or {}).get("id"):
                x.update(archiwum=True, archiwum_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), archiwum_kto=session.get("login", ""))
        S.pisz(S.F_KLIENCI, lista)
    return jsonify({"ok": True, "archiwum": True})


@bp.get("/api/place")
@S.wymaga_logowania
def place_info():
    d = S.dane_place()
    return jsonify({"parametry": d["parametry"], "opisy": S.PL.OPISY_PARAMETROW, "typy": S.PL.TYPY, "parametry_edycja": S.wlasciciel(),
                    "miesiace": sorted(S.listy_konta(d).keys(), reverse=True),
                    "pracownicy": [{k: p.get(k) for k in ("id", "imie", "stanowisko", "stawka", "umowa")} for p in S.dane_prac_konta()["pracownicy"]
                                   if not p.get("archiwum")]})


@bp.post("/api/place/parametry")
@S.wymaga_logowania
@S.UWIERZ.tylko_wlasciciel  # parametry płac (ZUS, PIT) są wspólne dla programu – zmienia je właściciel (H1-01)
def place_parametry():
    nowe = {}
    for k, v in (request.json or {}).items():
        if k in S.PL.PARAMETRY_2026:
            try:
                nowe[k] = float(str(v).replace(" ", "").replace(",", "."))
            except ValueError:
                return jsonify({"blad": f"Nieprawidłowa wartość: {S.PL.OPISY_PARAMETROW.get(k, k)}"}), 400
    with S.BLOKADA:
        d = S.czytaj(S.F_PLACE, {"parametry": {}, "listy": {}})
        d["parametry"] = {**d.get("parametry", {}), **nowe}
        if (request.json or {}).get("przywroc"):
            d["parametry"] = {}
        S.pisz(S.F_PLACE, d)
    return jsonify({"ok": True})


@bp.post("/api/place/umowa")
@S.wymaga_logowania
def place_umowa():
    j = request.json
    typ = j.get("typ")
    if typ not in list(S.PL.TYPY) + ["brak"]:
        return jsonify({"blad": "Wybierz rodzaj umowy."}), 400
    try:
        kwota = float(str(j.get("kwota") or 0).replace(" ", "").replace(",", "."))
    except ValueError:
        return jsonify({"blad": "Nieprawidłowa kwota."}), 400
    if kwota < 0:
        return jsonify({"blad": "Kwota nie może być ujemna."}), 400
    with S.BLOKADA:
        d = S.dane_prac()
        p = S.moj_pracownik(d, j.get("id"))
        if not p:
            return jsonify({"blad": "Nie ma takiego pracownika."}), 404
        p["umowa"] = None if typ == "brak" else {
            "typ": typ, "kwota": kwota, "od": str(j.get("od") or "")[:10], "do": str(j.get("do") or "")[:10],
            "etat": str(j.get("etat") or "1")[:6], "opcje": {k: bool((j.get("opcje") or {}).get(k)) for k in S.OPCJE_UMOWY}}
        S.pisz(S.F_PRAC, d)
    return jsonify({"ok": True})


@bp.post("/api/place/lista")
@S.wymaga_logowania
def place_lista():
    j = request.json or {}
    miesiac = str(j.get("miesiac", ""))
    if not re.fullmatch(r"\d{4}-\d{2}", miesiac):
        return jsonify({"blad": "Wybierz miesiąc."}), 400
    try:
        lista = S._lista_plac(miesiac, j.get("brutto"))
    except ValueError:
        return jsonify({"blad": "Nieprawidłowa kwota brutto."}), 400
    if j.get("zapisz"):
        with S.BLOKADA:
            d = S.czytaj(S.F_PLACE, {"parametry": {}, "listy": {}})
            wpis = {"pozycje": lista["pozycje"], "zapisano": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "kto": session.get("login", "")}
            d.setdefault("listy_konta", {}).setdefault(S.konto_biezace(), {})[miesiac] = wpis
            d.get("listy", {}).pop(miesiac, None) if S.konto_admina() else None
            S.pisz(S.F_PLACE, d)
        lista["zapisana"], lista["zapisano"] = True, wpis["zapisano"]
    elif j.get("usun"):
        with S.BLOKADA:
            d = S.czytaj(S.F_PLACE, {"parametry": {}, "listy": {}})
            (d.get("listy_konta") or {}).get(S.konto_biezace(), {}).pop(miesiac, None)
            if S.konto_admina():
                d.get("listy", {}).pop(miesiac, None)
            S.pisz(S.F_PLACE, d)
        lista = S._lista_plac(miesiac)
    return jsonify(lista)


@bp.get("/api/place/lista.xlsx")
@S.wymaga_logowania
def place_xlsx():
    miesiac = request.args.get("miesiac", "")
    if not re.fullmatch(r"\d{4}-\d{2}", miesiac):
        abort(400)
    lista = S._lista_plac(miesiac)
    import io
    b = io.BytesIO()  # w pamięci – bez wspólnego pliku DATA/Lista_plac_<miesiąc>.xlsx dla wszystkich kont (wyścig między firmami)
    S.PL.lista_xlsx(b, miesiac, lista["pozycje"], S.cfg().get("firma_nazwa", ""))
    b.seek(0)
    return send_file(b, as_attachment=True, download_name=f"Lista_plac_{miesiac}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
