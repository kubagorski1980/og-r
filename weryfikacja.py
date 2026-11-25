# -*- coding: utf-8 -*-
"""
Weryfikacja wykonawcy i referencji z oferty: rejestry (wykaz VAT, KRS, CEIDG), ogłoszenia o wyniku w BZP, metadane plików,
powiązania wystawcy z wykonawcą i zapytanie do wystawcy o potwierdzenie. Wynik to sygnały do sprawdzenia przez zamawiającego –
nie rozstrzygnięcie o nieprawdziwości referencji.
"""
import datetime as dt
import json
import os
import re
import urllib.request

OSTRZEZENIE, UWAGA, OK = "czerwony", "zolty", "zielony"
STATUSY = {"potwierdzona": "potwierdzona", "sprzeczna": "sygnały nieprawdziwości", "niepotwierdzona": "niepotwierdzona"}
ODPOWIEDZI = {"": "brak zapytania", "wyslano": "zapytanie wysłane", "potwierdzil": "wystawca potwierdził",
              "zaprzeczyl": "wystawca zaprzeczył", "brak_odpowiedzi": "brak odpowiedzi"}


def _nip(v):
    return re.sub(r"\D", "", str(v or ""))


def _data(v):
    """Data z tekstu: 2024-05-31, 31.05.2024, 05.2024, 2024 → date (dla samego roku: 31 grudnia, dla miesiąca: ostatni dzień – na korzyść wykonawcy)."""
    t = str(v or "").strip()
    for wz, f in ((r"(\d{4})-(\d{2})-(\d{2})", lambda m: dt.date(int(m[1]), int(m[2]), int(m[3]))),
                  (r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})", lambda m: dt.date(int(m[3]), int(m[2]), int(m[1]))),
                  (r"(?<!\d)(\d{1,2})[./-](\d{4})(?!\d)", lambda m: (dt.date(int(m[2]) + (int(m[1]) == 12), int(m[1]) % 12 + 1, 1) - dt.timedelta(days=1))),
                  (r"(?<!\d)((?:19|20)\d{2})(?!\d)", lambda m: dt.date(int(m[1]), 12, 31))):
        m = re.search(wz, t)
        if m:
            try:
                return f(m)
            except ValueError:
                continue
    return None


def _norm(t):
    return re.sub(r"[^a-ząćęłńóśźż0-9]", "", str(t or "").lower())


def krs_dane(krs, otworz=None):
    """Odpis aktualny z KRS (API Ministerstwa Sprawiedliwości, bez klucza): data wpisu do KRS i osoby w organie reprezentacji."""
    otworz = otworz or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Bidivia"}), timeout=25))
    k = _nip(krs).zfill(10)
    if not k.strip("0"):
        return {}
    for rej in ("P", "S"):
        try:
            with otworz(f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{k}?rejestr={rej}&format=json") as r:
                d = json.loads(r.read().decode("utf-8"))
        except Exception:
            continue
        odp = d.get("odpis") or {}
        osoby = []
        for org in ((odp.get("dane") or {}).get("dzial2") or {}).get("reprezentacja", {}).get("sklad", []) or []:
            n = org.get("nazwisko") or {}
            nazw = n.get("nazwiskoICzlon") if isinstance(n, dict) else n
            imie = (org.get("imiona") or {}).get("imie") if isinstance(org.get("imiona"), dict) else org.get("imiona")
            if nazw:
                osoby.append(" ".join(x for x in (str(imie or "").title(), str(nazw).title()) if x))
        pkd = []
        dz3 = ((odp.get("dane") or {}).get("dzial3") or {}).get("przedmiotDzialalnosci") or {}
        for klucz in ("przedmiotPrzewazajacejDzialalnosci", "przedmiotPozostalejDzialalnosci"):
            for x in dz3.get(klucz) or []:
                if isinstance(x, dict):
                    pkd.append({"kod": f"{x.get('kodDzial') or ''}.{x.get('kodKlasa') or ''}.{x.get('kodPodklasa') or ''}".strip("."),
                                "opis": x.get("opis") or "", "przewazajaca": klucz.startswith("przedmiotPrzewazajacej")})
        nA = odp.get("naglowekA") or {}
        return {"data_rejestracji": _data(nA.get("dataRejestracjiWKRS")), "zarzad": osoby, "pkd": pkd,
                "wykreslony": bool(nA.get("dataWykreslenia") or nA.get("dataWykresleniaZRejestruPrzedsiebiorcow"))}
    return {}


def metadane_pliku(sciezka):
    """Data utworzenia, autor i program z właściwości PDF lub DOCX (puste, gdy plik ich nie ma)."""
    wyn = {"plik": os.path.basename(sciezka)}
    try:
        if sciezka.lower().endswith(".pdf"):
            from pypdf import PdfReader
            info = PdfReader(sciezka).metadata or {}
            d = str(info.get("/CreationDate") or "")
            m = re.match(r"D:(\d{4})(\d{2})(\d{2})", d)
            wyn.update(utworzono=dt.date(int(m[1]), int(m[2]), int(m[3])) if m else None, autor=str(info.get("/Author") or "").strip(),
                       program=" / ".join(x for x in (str(info.get("/Creator") or "").strip(), str(info.get("/Producer") or "").strip()) if x))
        elif sciezka.lower().endswith(".docx"):
            from docx import Document
            cp = Document(sciezka).core_properties
            wyn.update(utworzono=cp.created.date() if cp.created else None, autor=(cp.author or "").strip(), program="Word")
    except Exception:
        pass
    return wyn


def ocen_referencje(wykonawca, referencje, metadane=None, bzp=None, dzis=None):
    """Sygnały dla każdej referencji: [(kolor, opis)], status i zalecenie. wykonawca: {nip, adres, data_powstania, zrodlo_daty,
    data_rejestracji_vat, zarzad}; referencje: z odczytu oferty (wystawca, nip_wystawcy, adres_wystawcy, data_od, data_do, wartosc,
    kontakt_*, plik, wystawca_rejestr: dane z rejestru albo {"blad": ...}); bzp: {indeks referencji: [ogłoszenia o wyniku z tym wykonawcą]}."""
    dzis = dzis or dt.date.today()
    metadane, bzp = metadane or {}, bzp or {}
    wyk_nip, wyk_adres = _nip(wykonawca.get("nip")), _norm(wykonawca.get("adres"))
    wyk_zarzad = {_norm(x) for x in wykonawca.get("zarzad") or [] if x}
    wyniki = []
    for i, r in enumerate(referencje or []):
        f = []
        d_do = _data(r.get("data_do")) or _data(r.get("data_od"))
        d_pow = wykonawca.get("data_powstania")
        if d_do and d_pow and d_do < d_pow:
            f.append((OSTRZEZENIE, f"Roboty zakończone {d_do:%d.%m.%Y}, a wykonawca powstał {d_pow:%d.%m.%Y} ({wykonawca.get('zrodlo_daty') or 'rejestr'})."))
        elif d_do and wykonawca.get("data_rejestracji_vat") and d_do < wykonawca["data_rejestracji_vat"] and not d_pow:
            f.append((UWAGA, f"Roboty zakończone przed rejestracją wykonawcy jako podatnika VAT ({wykonawca['data_rejestracji_vat']:%d.%m.%Y}) – sprawdź datę powstania firmy."))
        if d_do and d_do > dzis:
            f.append((OSTRZEZENIE, f"Data zakończenia robót ({d_do:%d.%m.%Y}) jest w przyszłości."))
        rn = _nip(r.get("nip_wystawcy"))
        rej = r.get("wystawca_rejestr") or {}
        if rn and wyk_nip and rn == wyk_nip:
            f.append((OSTRZEZENIE, "Referencję wystawił sam wykonawca (ten sam NIP)."))
        adr = _norm(rej.get("adres") or r.get("adres_wystawcy"))
        if adr and wyk_adres and len(adr) > 8 and (adr == wyk_adres or adr in wyk_adres or wyk_adres in adr):
            f.append((OSTRZEZENIE, "Wystawca referencji ma ten sam adres co wykonawca – możliwe powiązanie."))
        wspolni = wyk_zarzad & {_norm(x) for x in (rej.get("reprezentanci") or []) + (rej.get("zarzad") or []) if x}
        if wspolni:
            f.append((OSTRZEZENIE, "Te same osoby w organach wystawcy i wykonawcy – podmioty powiązane."))
        if rn and rej.get("blad"):
            f.append((UWAGA, f"Wystawcy nie znaleziono w rejestrze: {rej['blad']}"))
        elif rn and rej.get("nazwa"):
            f.append((OK, f"Wystawca istnieje w rejestrze: {rej['nazwa']}."))
        trafienia = bzp.get(i) or []
        if trafienia:
            t = trafienia[0]
            f.append((OK, f"Potwierdzone w BZP: wykonawca wygrał zamówienie u tego zamawiającego ({t.get('data') or ''}{', ' + t.get('przedmiot', '')[:80] if t.get('przedmiot') else ''})."))
        elif r.get("_bzp_sprawdzono"):
            f.append((UWAGA, "W ogłoszeniach o wyniku w BZP nie ma zamówienia tego zamawiającego udzielonego temu wykonawcy (BZP obejmuje zamówienia publiczne od 2021 r.)."))
        if not (r.get("kontakt_email") or r.get("kontakt_telefon")):
            f.append((UWAGA, "Brak danych kontaktowych wystawcy – poproś wykonawcę o kontakt do osoby, która może potwierdzić referencję."))
        if r.get("odpowiedz") == "potwierdzil":
            f.append((OK, "Wystawca potwierdził referencję."))
        elif r.get("odpowiedz") == "zaprzeczyl":
            f.append((OSTRZEZENIE, "Wystawca zaprzeczył, że wykonawca wykonał te roboty."))
        wyniki.append(f)
    # metadane: referencje od różnych wystawców utworzone tego samego dnia tym samym narzędziem i przez tego samego autora co oferta
    pliki = {}
    for i, r in enumerate(referencje or []):
        md = metadane.get(r.get("plik") or "") or {}
        if md.get("utworzono") and (md.get("autor") or md.get("program")):
            pliki.setdefault((md["utworzono"], md.get("autor") or "", md.get("program") or ""), set()).add((i, _norm(r.get("wystawca"))))
    autor_oferty = {_norm(m.get("autor")) for k, m in metadane.items() if m.get("oferta") and m.get("autor")}
    for (dzien, autor, program), zb in pliki.items():
        if len({w for _, w in zb}) >= 2:
            for i, _ in zb:
                wyniki[i].append((UWAGA, f"Pliki referencji od różnych wystawców utworzono tego samego dnia ({dzien:%d.%m.%Y}) tym samym programem"
                                          f"{' przez tego samego autora' if autor else ''} – sprawdź oryginały."))
        if autor and _norm(autor) in autor_oferty:
            for i, _ in zb:
                wyniki[i].append((UWAGA, "Autor pliku referencji jest taki sam jak autor dokumentów oferty."))
    out = []
    for r, f in zip(referencje or [], wyniki):
        kol = [k for k, _ in f]
        status = "sprzeczna" if OSTRZEZENIE in kol else "potwierdzona" if (r.get("odpowiedz") == "potwierdzil" or any("Potwierdzone w BZP" in t for _, t in f)) else "niepotwierdzona"
        out.append({**{k: v for k, v in r.items() if not k.startswith("_")}, "sygnaly": f, "status": status})
    return out


def klauzula_art14(administrator, kontakt, cel, zrodlo, okres):
    """Informacja z art. 14 RODO – dane kontaktowe pozyskane nie od osoby, której dotyczą (rejestry, ogłoszenia, referencje)."""
    adm = administrator or "zamawiający"
    return ("—\nINFORMACJA O PRZETWARZANIU DANYCH (art. 14 RODO)\n"
            f"1. Administrator: {adm}" + (f", kontakt: {kontakt}" if kontakt else ", kontakt: adres nadawcy tej wiadomości") + ".\n"
            f"2. Cel i podstawa: {cel} – prawnie uzasadniony interes administratora (art. 6 ust. 1 lit. f RODO).\n"
            f"3. Kategorie i źródło danych: dane kontaktowe (imię i nazwisko, adres e-mail, telefon, stanowisko, nazwa firmy) pozyskane z: {zrodlo}.\n"
            "4. Odbiorcy: podmioty świadczące administratorowi usługi poczty elektronicznej, IT i hostingu – na podstawie umów powierzenia.\n"
            f"5. Okres przechowywania: {okres}, a po wniesieniu sprzeciwu – do jego rozpatrzenia.\n"
            "6. Przysługuje Pani/Panu prawo dostępu do danych, ich sprostowania, usunięcia lub ograniczenia przetwarzania oraz prawo sprzeciwu wobec "
            "przetwarzania (art. 21 RODO), a także prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych.\n"
            "7. Dane nie służą do zautomatyzowanego podejmowania decyzji ani profilowania.")


def zapytanie_do_wystawcy(ref, wykonawca_nazwa, zamawiajacy, zamowienie):
    """Treść e-maila do wystawcy referencji z prośbą o potwierdzenie (wysyłana przez zamawiającego z jego skrzynki)."""
    okres = " – ".join(x for x in (str(ref.get("data_od") or "").strip(), str(ref.get("data_do") or "").strip()) if x)
    return (f"Temat: Prośba o potwierdzenie referencji – {wykonawca_nazwa}\n\n"
            f"Dzień dobry,\n\nw postępowaniu „{zamowienie}” prowadzonym przez {zamawiajacy or '[zamawiający]'} wykonawca {wykonawca_nazwa} "
            f"przedstawił referencję wystawioną przez {ref.get('wystawca') or 'Państwa'} dotyczącą robót: {ref.get('zakres') or '[zakres]'}"
            f"{', o wartości ' + str(ref.get('wartosc')) if ref.get('wartosc') else ''}{', wykonanych w okresie ' + okres if okres else ''}"
            f"{', adres: ' + ref.get('adres_obiektu') if ref.get('adres_obiektu') else ''}.\n\n"
            "Uprzejmie prosimy o potwierdzenie, czy:\n1) wykonawca wykonał dla Państwa te roboty,\n2) zakres, wartość i terminy są zgodne z referencją,\n"
            "3) roboty zostały wykonane należycie.\n\nWystarczy krótka odpowiedź na tę wiadomość. Dziękujemy.\n\n"
            f"Z poważaniem\n{zamawiajacy or '[zamawiający]'}\n\n"
            + klauzula_art14(zamawiajacy, "", f"weryfikacja referencji przedstawionej przez wykonawcę w postępowaniu „{zamowienie}”",
                             f"referencja albo wykaz prac złożony w ofercie przez wykonawcę {wykonawca_nazwa}",
                             "do zakończenia postępowania i przez okres przechowywania jego dokumentacji"))


ECRUB = "https://e-crub.gunb.gov.pl"
KRZ = "https://krz.ms.gov.pl"


def _prac(n):
    """1 podobna praca, 2–4 podobne prace, 5+ podobnych prac (12–14 – podobnych prac)."""
    if n == 1:
        return "1 podobna praca"
    return f"{n} podobne prace" if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else f"{n} podobnych prac"


def _wymog_doswiadczenia(warunki):
    """„co najmniej 2 podobne prace w ostatnich 5 latach” → (2, 5); brak wymogu → (None, None)."""
    t = str(warunki or "")
    n = re.search(r"co najmniej (\d+)\s+(?:podobn|robot|usług|prac|zamówie)", t)
    l = re.search(r"ostatnich (\d+) lat", t)
    return (int(n.group(1)) if n else None), (int(l.group(1)) if l else None)


def ocen_wykonawce(wyk, rej, krs, wynik, przedmiot, rodzaj, warunki, termin_realizacji=None, dzis=None, podobienstwo=None):
    """Sygnały dotyczące wykonawcy (a nie pojedynczej referencji): status, działalność, doświadczenie wobec wymogu, polisa OC, kierownik robót.
    Zwraca (sygnaly [(kolor, opis)], do_doslania [str], do_sprawdzenia [{"pole", "opis", "link", "szukaj"}])."""
    dzis = dzis or dt.date.today()
    f, dosl, spr = [], [], []
    if rej:
        sv = str(rej.get("status_vat") or "")
        if sv and "czynny" not in sv.lower():
            f.append((OSTRZEZENIE, f"Status VAT: {sv}."))
        elif sv:
            f.append((OK, "Czynny podatnik VAT (wykaz podatników VAT)."))
    if (krs or {}).get("wykreslony"):
        f.append((OSTRZEZENIE, "Podmiot wykreślony z KRS."))
    pkd = (krs or {}).get("pkd") or []
    if rodzaj == "roboty" and pkd:
        bud = [p for p in pkd if str(p.get("kod", "")).split(".")[0] in ("41", "42", "43")]
        f.append((OK, f"Działalność budowlana w KRS (PKD {', '.join(p['kod'] for p in bud[:3])}).") if bud
                 else (UWAGA, "W KRS brak kodów PKD robót budowlanych (41–43) – sprawdź, czy wykonawca prowadzi taką działalność."))
    n_wym, lat = _wymog_doswiadczenia(warunki)
    refs = [r for r in (wynik or {}).get("referencje") or [] if isinstance(r, dict)]
    if n_wym:
        # 29 lutego minus N lat (rok nieprzestępny) – 28 lutego; dotąd ValueError i błąd serwera w każdy 29 lutego
        granica = (dzis.replace(year=dzis.year - lat) if not (dzis.month == 2 and dzis.day == 29) else dt.date(dzis.year - lat, 2, 28)) if lat else None
        podobne = []
        for r in refs:
            d = _data(r.get("data_do")) or _data(r.get("data_od"))
            if granica and d and d < granica:
                continue
            if podobienstwo and przedmiot and r.get("zakres") and podobienstwo(przedmiot, r["zakres"], "", "") < 0.25:
                continue
            podobne.append(r)
        if len(podobne) >= n_wym:
            f.append((OK, f"Doświadczenie: {_prac(len(podobne))}{f' w ostatnich {lat} latach' if lat else ''} – wymóg co najmniej {n_wym} spełniony na podstawie wykazu."))
        else:
            f.append((OSTRZEZENIE, f"Doświadczenie: {_prac(len(podobne))}{f' w ostatnich {lat} latach' if lat else ''}, a zapytanie wymaga co najmniej {n_wym}."))
            dosl.append("Wykaz podobnych prac spełniający wymóg doświadczenia, z dowodami należytego wykonania")
    if refs and not any(r.get("plik") for r in refs):
        dosl.append("Referencje albo protokoły odbioru do prac z wykazu")
    pol = (wynik or {}).get("polisa") or {}
    if isinstance(pol, dict) and (pol.get("okres_do") or pol.get("numer")):
        do = _data(pol.get("okres_do"))
        tr = _data(termin_realizacji) if termin_realizacji else None
        if do and do < dzis:
            f.append((OSTRZEZENIE, f"Polisa OC wygasła {do:%d.%m.%Y}."))
            dosl.append("Aktualna polisa OC")
        elif do and tr and do < tr:
            f.append((UWAGA, f"Polisa OC ważna do {do:%d.%m.%Y}, a realizacja potrwa do {tr:%d.%m.%Y} – potrzebne odnowienie na czas umowy."))
            dosl.append("Zobowiązanie do utrzymania polisy OC przez cały okres umowy")
        elif do:
            f.append((OK, f"Polisa OC ważna do {do:%d.%m.%Y}{', suma ' + str(pol.get('suma_gwarancyjna')) if pol.get('suma_gwarancyjna') else ''}."))
    elif "polis" in str(warunki or "").lower():
        f.append((UWAGA, "Zapytanie wymaga polisy OC, a w ofercie jej nie odczytano."))
        dosl.append("Polisa OC działalności")
    kier = (wynik or {}).get("kierownik") or {}
    if rodzaj == "roboty":
        if isinstance(kier, dict) and (kier.get("imie_nazwisko") or kier.get("nr_uprawnien")):
            spr.append({"pole": "uprawnienia", "opis": f"Uprawnienia budowlane: {kier.get('imie_nazwisko') or ''}, nr {kier.get('nr_uprawnien') or '–'}"
                                                       f"{', ' + kier['specjalnosc'] if kier.get('specjalnosc') else ''}",
                        "link": ECRUB, "szukaj": kier.get("nr_uprawnien") or kier.get("imie_nazwisko") or ""})
        elif "kierown" in str(warunki or "").lower() or "uprawnie" in str(warunki or "").lower():
            f.append((UWAGA, "W ofercie nie wskazano kierownika robót z uprawnieniami budowlanymi."))
            dosl.append("Dane kierownika robót: imię i nazwisko, numer uprawnień budowlanych, specjalność")
    spr.append({"pole": "krz", "opis": "Krajowy Rejestr Zadłużonych – upadłość, restrukturyzacja, egzekucja",
                "link": KRZ, "szukaj": (wyk or {}).get("nip") or (wyk or {}).get("nazwa") or ""})
    return f, dosl, spr
