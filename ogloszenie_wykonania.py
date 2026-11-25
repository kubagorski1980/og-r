# -*- coding: utf-8 -*-
"""Ogłoszenie o wykonaniu umowy (art. 448 Pzp, zakres – załącznik nr 7 do rozporządzenia w sprawie ogłoszeń w BZP) dla zamawiającego:
dane z zarządzania inwestycją (umowa, odbiory, faktury, aneksy, podwykonawcy) + kary i ocena wykonania, termin 30 dni, kontrola spójności,
tekst do przepisania do BZP i Word. Dodatkowo: czy wymagany jest raport z realizacji zamówienia (art. 446 Pzp)."""
import datetime as dt

import modul_oferty as MO
from liczby import liczba  # noqa: E402  (jedna zamiana tekstu na liczbę w programie)


def _f(x):
    return liczba(x, 0.0)


def _d(x):
    try:
        return dt.date.fromisoformat(str(x)[:10])
    except ValueError:
        return None


def stan(r, o, m):
    """r – dane realizacji (umowa, hrf, faktury, aneksy, podwykonawcy), o – zapisane dane ogłoszenia, m – projekt."""
    o = o or {}
    hrf = (r.get("hrf") or {}).get("etapy") or []
    odbiory = sorted(e.get("data_odbioru") for e in hrf if e.get("status") == "odebrany" and e.get("data_odbioru"))
    fakt = r.get("faktury") or []
    zapl = [f for f in fakt if f.get("zaplacona")]
    ost_plat = max([str(f.get("data_zaplaty") or "") for f in zapl] or [""])  # tylko faktyczna data zapłaty (nie termin płatności)
    # data wykonania umowy: wg UZP – dzień protokołu odbioru lub uznania całej umowy za wykonaną
    # odbiór częściowy to nie wykonanie umowy – data proponowana dopiero po odbiorze wszystkich etapów (ostatni = odbiór końcowy)
    wszystkie = bool(hrf) and all(e.get("status") == "odebrany" for e in hrf)
    propozycje = {"odbior": odbiory[-1] if odbiory and wszystkie else "", "platnosc": ost_plat[:10] if wszystkie or not hrf else "",
                  "odebrano_etapow": len(odbiory), "etapow": len(hrf)}
    data_wyk = o.get("data_wykonania") or propozycje["odbior"] or ""
    dw = _d(data_wyk)
    termin_pub = (dw + dt.timedelta(days=30)).isoformat() if dw else ""
    dni_do = (dw + dt.timedelta(days=30) - dt.date.today()).days if dw else None
    aneksy = r.get("aneksy") or []
    dni_aneksy = sum(int(_f(a.get("dni"))) for a in aneksy)
    # termin pierwotny (z umowy) i po zmianach (aneksy aktualizują termin w danych umowy)
    tk = _d(r.get("termin_zakonczenia"))
    termin_umowny = o.get("termin_pierwotny") or r.get("termin_pierwotny") or \
        ((tk - dt.timedelta(days=dni_aneksy)).isoformat() if tk and dni_aneksy else (r.get("termin_zakonczenia") or ""))
    tu = _d(termin_umowny)
    termin_po_zmianach = r.get("termin_zakonczenia") or termin_umowny
    tz = _d(termin_po_zmianach) or tu
    w_terminie = (dw <= tu) if dw and tu else None
    opoznienie_pierw = (dw - tu).days if dw and tu and dw > tu else 0
    opoznienie = (dw - tz).days if dw and tz and dw > tz else 0  # zwłoka względem terminu po zmianach umowy
    kary = [k for k in o.get("kary") or [] if _f(k.get("kwota"))]
    suma_kar = round(sum(_f(k.get("kwota")) for k in kary), 2)
    kary_niepotr = round(sum(_f(k.get("kwota")) for k in kary if not k.get("potracona")), 2)
    wyplacone_fakt = round(sum(_f(f.get("brutto")) for f in zapl), 2)
    # wynagrodzenie wypłacone – po potrąceniu kar (UZP); kary potrącone przy zapłacie faktur są już w kwotach zapłaconych
    wyplacone = round(_f(o.get("wyplacone")) if o.get("wyplacone") not in (None, "") else wyplacone_fakt - (0 if o.get("kary_w_platnosciach", True) else
                                                                                                           sum(_f(k.get("kwota")) for k in kary if k.get("potracona"))), 2)
    wart_netto = _f(r.get("wartosc_pierwotna_netto") or r.get("wartosc_netto"))
    vat = _f(r.get("vat")) if _f(r.get("vat")) < 1 else _f(r.get("vat")) / 100
    wart_brutto = round(wart_netto * (1 + (vat if r.get("vat") not in (None, "") else 0.23)), 2)
    zmiany = []
    for a in aneksy:  # aneksy z modułu „Zmiany umowy”
        zmiany.append({"nr": a.get("nr"), "data": a.get("data"), "podstawa": a.get("podstawa") or "art. 455 Pzp – postanowienia umowy (zmiany przewidziane)",
                       "przyczyna": a.get("przyczyna") or (f"wniosek wykonawcy {a.get('wniosek')}" if a.get("wniosek") else ""),
                       "opis": a.get("opis") or (f"wydłużenie terminu o {a.get('dni')} dni" if _f(a.get("dni")) else ""),
                       "wartosc": _f(a.get("kwota_netto")), "zrodlo": "aneks w programie"})
    zmiany += [dict(z, zrodlo="wpisana ręcznie") for z in o.get("zmiany") or [] if z.get("opis") or z.get("podstawa")]
    wzrost = round(sum(_f(z.get("wartosc")) for z in zmiany), 2)
    pw = r.get("podwykonawcy") or []
    nalezycie = o.get("nalezycie") or ("nie" if (opoznienie > 0 or kary) else "tak")
    pola = [  # kolejność jak w formularzu BZP (sekcje IV–V załącznika nr 7)
        ("Numer ogłoszenia o zamówieniu / identyfikator postępowania", o.get("nr_ogloszenia") or ((m.get("przetarg") or {}).get("numer")) or ""),
        ("Nazwa zamówienia", m.get("nazwa") or ""),
        ("Data zawarcia umowy", r.get("data_umowy") or ""),
        ("Numer umowy", r.get("umowa_nr") or ""),
        ("Okres, na jaki zawarto umowę", o.get("okres") or (f"od {r.get('data_umowy')} do {termin_umowny}" if r.get("data_umowy") and termin_umowny else "")),
        ("Wykonawca (nazwa i adres)", ", ".join(x for x in (r.get("wykonawca_nazwa"), r.get("wykonawca_adres"), ("NIP " + r["wykonawca_nip"]) if r.get("wykonawca_nip") else "") if x)),
        ("Termin wykonania umowy", data_wyk),
        ("Czy umowę wykonano w pierwotnie określonym terminie", "–" if w_terminie is None else "tak" if w_terminie else
         f"nie – wykonano {opoznienie_pierw} dni po pierwotnym terminie ({termin_umowny})"
         + (f"; termin zmieniony aneksami o {dni_aneksy} dni (do {termin_po_zmianach})" + (" – wykonano w terminie po zmianie" if not opoznienie else f", zwłoka {opoznienie} dni") if dni_aneksy else "")
         + (f"; przyczyna: {o['przyczyna_opoznienia']}" if o.get("przyczyna_opoznienia") else "")),
        ("Zmiany umowy", "brak" if not zmiany else "\n".join(
            f"{i}. {z.get('nr') or ''} {('z dnia ' + z['data']) if z.get('data') else ''} – podstawa: {z.get('podstawa') or '[UZUPEŁNIJ]'}; przyczyna: {z.get('przyczyna') or '[UZUPEŁNIJ]'}; "
            f"zamówienie po zmianie: {z.get('opis') or '[UZUPEŁNIJ]'}; wartość zmiany: {MO.zl(_f(z.get('wartosc')))}"
            + (f" (wzrost wynagrodzenia)" if _f(z.get("wartosc")) > 0 else "") for i, z in enumerate(zmiany, 1))),
        ("Łączna wartość wynagrodzenia wypłaconego (po potrąceniu kar)", MO.zl(wyplacone)),
        ("Czy umowa została wykonana należycie", "tak" if nalezycie == "tak" else "nie" + (f" – {o['opis_nienaleznego']}" if o.get("opis_nienaleznego") else "")),
        ("Kary umowne (informacja dodatkowa)", "nie naliczono" if not kary else "; ".join(f"{k.get('tytul') or 'kara'}: {MO.zl(_f(k.get('kwota')))}"
                                                                                          + (" (potrącona)" if k.get("potracona") else "") for k in kary)),
        ("Podwykonawcy (informacja dodatkowa)", "nie" if not pw else "; ".join(str(p.get("nazwa") or "") for p in pw if p.get("nazwa")) or "tak"),
    ]
    uw = kontrola(o, r, dw, tu, opoznienie, kary, zmiany, wyplacone, wart_brutto, wzrost, nalezycie, zapl, fakt)
    K_ = m.get("kreator") or {}
    raport = raport_446(wart_brutto, wyplacone, suma_kar, opoznienie, o, rodzaj=m.get("rodzaj_zamowienia") or K_.get("rodzaj") or "roboty",
                        wartosc_netto=_f(r.get("wartosc_szacunkowa")) or wart_netto)
    pub = o.get("publikacja") or {}
    return {"dane": o, "propozycje_daty": propozycje, "data_wykonania": data_wyk, "termin_publikacji": termin_pub, "dni_do_terminu": dni_do,
            "termin_umowny": termin_umowny, "termin_po_zmianach": termin_po_zmianach, "w_terminie": w_terminie, "opoznienie_dni": opoznienie,
            "opoznienie_pierwotne": opoznienie_pierw,
            "wyplacone": wyplacone, "wyplacone_z_faktur": wyplacone_fakt, "wartosc_umowy_brutto": wart_brutto, "suma_kar": suma_kar,
            "kary_niepotracone": kary_niepotr, "zmiany": zmiany, "nalezycie": nalezycie, "pola": pola, "uwagi": uw, "raport_446": raport,
            "opublikowane": bool(pub.get("numer") and pub.get("data")), "publikacja": pub}


def kontrola(o, r, dw, tu, opoznienie, kary, zmiany, wyplacone, wart_brutto, wzrost, nalezycie, zapl, fakt):
    u = []
    hrf = (r.get("hrf") or {}).get("etapy") or []
    if not dw and hrf and any(e.get("status") != "odebrany" for e in hrf):
        u.append(("krytyczna", f"Umowa nie jest jeszcze wykonana – odebrano {sum(e.get('status') == 'odebrany' for e in hrf)} z {len(hrf)} etapów harmonogramu. "
                               "Ogłoszenie zamieszcza się w ciągu 30 dni od odbioru końcowego."))
    elif not dw:
        u.append(("krytyczna", "Brak daty wykonania umowy – wpisz datę protokołu odbioru końcowego (albo uznania umowy za wykonaną)."))
    if not tu:
        u.append(("istotna", "Brak pierwotnego terminu wykonania z umowy – uzupełnij w danych umowy."))
    if opoznienie > 0 and not o.get("przyczyna_opoznienia"):
        u.append(("istotna", f"Umowę wykonano po terminie ({opoznienie} dni) – podaj przyczynę opóźnienia."))
    if opoznienie > 0 and not kary and not o.get("bez_kar_uzasadnienie"):
        u.append(("istotna", "Jest opóźnienie, a nie wpisano kar umownych – jeśli kar nie naliczono, zapisz dlaczego (np. opóźnienie z przyczyn niezależnych od wykonawcy)."))
    if nalezycie == "tak" and kary:
        u.append(("istotna", "Naliczono kary umowne, a umowa oznaczona jako wykonana należycie – sprawdź spójność ogłoszenia."))
    if nalezycie == "nie" and not o.get("opis_nienaleznego"):
        u.append(("istotna", "Umowa wykonana nienależycie – opisz, na czym to polegało."))
    vat_ = _f(r.get("vat")) if _f(r.get("vat")) < 1 else _f(r.get("vat")) / 100
    if wart_brutto and wyplacone > (wart_brutto + max(wzrost, 0) * (1 + (vat_ if r.get("vat") not in (None, "") else 0.23))) * 1.005:
        u.append(("istotna", f"Wypłacono więcej ({MO.zl(wyplacone)}) niż wartość umowy brutto ({MO.zl(wart_brutto)}), a nie ma zmian umowy zwiększających wynagrodzenie."))
    if len(zapl) < len(fakt):
        u.append(("drobna", f"Nie wszystkie faktury są oznaczone jako zapłacone ({len(fakt) - len(zapl)}) – wynagrodzenie wypłacone może być niepełne."))
    if any(not z.get("podstawa") or "UZUPEŁNIJ" in str(z.get("podstawa")) for z in zmiany):
        u.append(("istotna", "Przy zmianie umowy brakuje podstawy prawnej (np. art. 455 ust. 1 pkt 1 Pzp)."))
    return [{"waga": w, "opis": t} for w, t in u]


ODSTAPIENIA = ("odstąpienie od umowy w całości", "odstąpienie od umowy w części", "wypowiedzenie umowy w całości", "wypowiedzenie umowy w części")


def raport_446(wart_brutto, wyplacone, kary, opoznienie, o, rodzaj="roboty", wartosc_netto=None):
    """Art. 446 ust. 1 Pzp – raport z realizacji zamówienia, gdy: wydatkowano ≥10% więcej niż cena ofertowa (pkt 1), kary ≥10% ceny (pkt 2),
    opóźnienie ponad 90 dni (zamówienia od 20 mln euro – roboty / 10 mln euro – dostawy i usługi) albo ponad 30 dni (mniejsze) (pkt 3),
    odstąpienie od umowy albo jej wypowiedzenie w całości lub w części (pkt 4). Wartość zamówienia netto w zł przeliczana kursem z progi.py."""
    import progi as PR
    cena = _f(o.get("cena_ofertowa")) or wart_brutto
    pow_ = []
    if cena and wyplacone >= cena * 1.10:
        pow_.append(f"wydatkowano {MO.zl(wyplacone)} – co najmniej 10% więcej niż cena ofertowa ({MO.zl(cena)})")
    if cena and kary >= cena * 0.10:
        pow_.append(f"kary umowne {MO.zl(kary)} – co najmniej 10% ceny ofertowej")
    duze = bool(wartosc_netto) and wartosc_netto / PR.KURS_EURO >= (20_000_000 if (rodzaj or "roboty") == "roboty" else 10_000_000)
    prog = 90 if duze else 30
    if opoznienie > prog:
        pow_.append(f"opóźnienie {opoznienie} dni – ponad {prog} dni" + (" (zamówienie od 20 mln euro – roboty / 10 mln euro – dostawy i usługi)" if duze else ""))
    if o.get("odstapienie") in ODSTAPIENIA:
        pow_.append(str(o["odstapienie"]) + " (art. 446 ust. 1 pkt 4)")
    return {"wymagany": bool(pow_), "powody": pow_, "prog_opoznienia": prog}


def ogloszenie_docx(sciezka, nazwa, s):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    MO._akapit(d, "DANE DO OGŁOSZENIA O WYKONANIU UMOWY", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "art. 448 ustawy Prawo zamówień publicznych – do przepisania w formularzu Biuletynu Zamówień Publicznych", kursywa=True,
               wyrownanie=WD_ALIGN_PARAGRAPH.CENTER, rozmiar=9)
    MO._akapit(d, f"Termin zamieszczenia w BZP: {s['termin_publikacji'] or '[ustal datę wykonania umowy]'} (30 dni od wykonania umowy).", pogrub=True)
    MO._tabela(d, [["Pole", "Treść"]] + [[a, b or "[UZUPEŁNIJ]"] for a, b in s["pola"]])
    if s["raport_446"]["wymagany"]:
        MO._akapit(d, "Uwaga: wymagany raport z realizacji zamówienia (art. 446 Pzp) – " + "; ".join(s["raport_446"]["powody"]) + ".", pogrub=True)
    MO._akapit(d, "Dowód zamieszczenia ogłoszenia przechowuje się w dokumentacji postępowania (art. 267 ust. 2 pkt 8 i ust. 3 Pzp). Zakres pól "
                  "odpowiada załącznikowi nr 7 do rozporządzenia w sprawie ogłoszeń zamieszczanych w BZP – sprawdź z aktualnym formularzem.",
               kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)


def raport_docx(sciezka, nazwa, s, r):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = MO._doc()
    MO._akapit(d, "RAPORT Z REALIZACJI ZAMÓWIENIA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    MO._akapit(d, "art. 446 ustawy Prawo zamówień publicznych", kursywa=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER, rozmiar=9)
    MO._tabela(d, [["Element", "Dane"], ["Zamówienie", nazwa], ["Umowa", f"{r.get('umowa_nr') or ''} z dnia {r.get('data_umowy') or ''}"],
                   ["Wykonawca", r.get("wykonawca_nazwa") or ""], ["Przesłanki sporządzenia raportu", "; ".join(s["raport_446"]["powody"])],
                   ["Wartość umowy brutto / wypłacono", f"{MO.zl(s['wartosc_umowy_brutto'])} / {MO.zl(s['wyplacone'])}"],
                   ["Kary umowne", MO.zl(s["suma_kar"])], ["Opóźnienie", f"{s['opoznienie_dni']} dni"]])
    for t in ("Ocena realizacji zamówienia i przyczyny nieprawidłowości: [UZUPEŁNIJ]",
              "Ocena, czy i w jakim zakresie nieprawidłowości wynikały z wad dokumentacji, opisu przedmiotu zamówienia lub warunków umowy: [UZUPEŁNIJ]",
              "Wnioski na przyszłość (np. zmiany w opisie przedmiotu zamówienia, warunkach umowy, sposobie szacowania wartości): [UZUPEŁNIJ]"):
        MO._akapit(d, t)
    MO._akapit(d, "Raport sporządza się po wykonaniu umowy – sprawdź aktualne wymagania art. 446 Pzp (termin, publikacja, przekazanie).", kursywa=True, rozmiar=8)
    MO.zapisz_z_zaznaczeniem(d, sciezka)
