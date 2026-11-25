# -*- coding: utf-8 -*-
"""
Kreator zamówienia (zamawiający publiczny i wspólnota) – trasy: tworzenie i stan kreatora, zapis kroków, wzory i źródła, podział na części, dokumenty, przegląd i zmiany (AI), umowa i realizacja części, powiązana ocena ofert.
Blueprint „kreator” (etap 2 podziału serwer.py). Nazwy z serwera pobierane w chwili wywołania (S.nazwa) – jedna instancja serwera,
działające podmiany w testach, bez importu cyklicznego.
"""
import datetime as dt
import json
import os
import re
import uuid

from flask import Blueprint, abort, jsonify, request, send_file, session

import reguly_zamowien as RZ
import lista_kontroli as LK
import postepowanie_zam as PZ
import serwer as S

import kontrola_zam as KO  # noqa: E402  (kontrole kreatora bez AI)

bp = Blueprint("kreator", __name__)


def _netto_zam_zrodlo(m):
    """Wartość netto zamówienia i jej źródło. Zamawiający publiczny: z szacowania (kosztorys inwestorski / PFU / rozeznanie rynku – art. 28–36 Pzp);
    kosztorys przygotowany przez AI nie jest podstawą wartości. Zamawiający prywatny (bez Pzp): może to być szacunek kosztów AI."""
    K = m.get("kreator") or {}
    rz = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
    liczba_ = lambda v: KO.kwota(v) or 0.0  # zapis nieliczbowy = brak kwoty (nie błąd serwera)
    if not K.get("prywatny"):
        w = S.SZ.wylicz(K.get("szacowanie") or {}, rz, K.get("data_wszczecia") or None)
        if w["netto"] and w["netto"] > 0:
            return w["netto"], ("szacowanie" if w["kompletne"] else "szacowanie_niepelne")
    if K.get("wartosc_decyzja") == "dokumenty" and S.NR._f(K.get("wartosc_dok")):
        return S.NR._f(K.get("wartosc_dok")), "dokumenty"
    if K.get("prywatny") and float((m.get("oferta") or {}).get("netto") or 0):
        return float(m["oferta"]["netto"]), "szacunek_ai"
    if liczba_(K.get("wartosc_reczna")):
        return liczba_(K.get("wartosc_reczna")), "reczna"
    if liczba_(K.get("budzet")):
        return liczba_(K.get("budzet")), "budzet"
    return 0.0, ""


def _netto_zam(m):
    return _netto_zam_zrodlo(m)[0]


def _fin_kreatora(pid, K=None):
    """Finansowanie zamówienia (kredyt, premia BGK, KPO, dotacja) – ten sam zapis co w realizacji (realizacja.json), więc po zawarciu umowy
    kontrole finansowania działają bez ponownego wprowadzania. aktualne = dokumenty przygotowano po ostatniej zmianie finansowania."""
    F = S.realizacja_dane(pid).get("finansowanie")
    F = F if isinstance(F, dict) else {}
    zr = [z for z in (F.get("zrodla") or []) if isinstance(z, dict)]
    nr = int(F.get("nr") or 0)
    dok_nr = (K or {}).get("dok_fin_nr")
    return {"zrodla": zr, "liczba": len(zr), "nr": nr, "dok_nr": dok_nr, "aktualne": bool(zr) and dok_nr == nr,
            "opis": ", ".join(S.FIN.TYPY.get(z.get("typ"), "finansowanie") + (f" ({z['instytucja']})" if z.get("instytucja") else "") for z in zr),
            "tekst": S.FIN.tekst_do_dokumentow(zr), "harmonogram": S.FIN.harmonogram_szkic(zr)}


ELEMENT_FIN_GMINY = {"id": "finansowanie", "opis": "Finansowanie (kredyt, premia BGK, KPO, dotacja): wymagania instytucji finansującej uwzględnione "
                     "w dokumentach, wzorze umowy i harmonogramie (termin, transze, dokumenty do rozliczenia, zgoda na zmiany umowy)", "rodzaj": "reczne"}


GLOWNE_DOK = {"swz", "umowa", "opz", "formularz", "zaproszenie_negocjacje", "zaproszenie_oferty"}
WYMAGANE_DOK = ("swz", "zaproszenie_negocjacje", "umowa")  # bez nich nie ma czego publikować


def _dokumenty_stan(dokumenty, komplet, pryw, sciezka, wzory):
    """Czy komplet zawiera dokumenty główne (krok 5): samo przygotowanie oświadczeń nie kończy kroku."""
    if sciezka == "wzory":  # własne wzory: krok zalicza wzór dokumentu głównego (SWZ / zapytanie albo umowa), nie dowolny plik
        glowny = any(re.search(r"(?i)swz|specyfikacj|zapytani|umow", f) for f in wzory)
        return glowny, ([] if glowny else ["wzór SWZ / zapytania ofertowego albo wzór umowy"])
    brak = [k for k in komplet if not any(f.startswith(S.ZAM.prefiks_dok(k, pryw) + "_") for f in dokumenty)]  # wszystkie dokumenty kompletu dla trybu
    return bool(dokumenty) and not brak, [S.ZAM.etykieta_dok(k, pryw) for k in brak]


def _liczba_ofert(m):
    """Liczba ofert złożonych w postępowaniu (powiązana ocena ofert); None – nieznana (oferty jeszcze nie wpisane)."""
    try:
        of = [o for o in (_ocena_zamowienia(m).get("oferty") or []) if isinstance(o, dict)]
    except Exception:  # uszkodzona albo usunięta ocena – liczba ofert nieznana
        return None
    return len(of) or None


def _postepowanie_stan(K, unijne, min_dni=None, ustawowe=True, liczba_ofert=None):
    """Po publikacji (zamawiający publiczny): kalendarz terminów, pytania wykonawców, zmiany terminu składania ofert.
    ustawowe=False (poniżej progu, zasada konkurencyjności): tylko termin ofert i historia pytań – bez terminów z ustawy.
    liczba_ofert – z oceny ofert (1 = wyjątek art. 308 ust. 3 pkt 1 lit. a / art. 264 ust. 2 pkt 1 lit. a; None – nieznana)."""
    P = K.get("postepowanie") or {}
    t_pyt = K.get("termin_ofert") if (K.get("pytania_od_nowego_terminu") or not P.get("termin_pierwotny")) else P["termin_pierwotny"]
    U = K.get("umowa") or {}
    ostrz = []
    pub, t = PZ._d(P.get("data_publikacji")), PZ._d(K.get("termin_ofert"))
    if pub and t and min_dni and (t - pub).days < min_dni:
        ostrz.append(f"Od publikacji ogłoszenia ({pub:%d.%m.%Y}) do terminu składania ofert ({t:%d.%m.%Y}) jest {(t - pub).days} dni – "
                     f"minimum to {min_dni} dni. Wyznacz późniejszy termin składania ofert.")
    if pub and t and t <= pub:
        ostrz.append("Termin składania ofert jest wcześniejszy niż publikacja ogłoszenia.")
    if ustawowe:  # umowa przed upływem terminu na odwołanie (art. 308 ust. 2 / art. 264 ust. 1) – także w ostrzeżeniach postępowania
        ostrz += PZ.ostrzezenia_umowy(P.get("data_wyboru"), U.get("data_umowy"), unijne, liczba_ofert)
    return {"unijne": unijne, "data_publikacji": P.get("data_publikacji") or "", "data_wyboru": P.get("data_wyboru") or "", "ostrzezenia": ostrz,
            "kalendarz": PZ.kalendarz(K.get("termin_ofert"), unijne, P.get("data_publikacji"), P.get("data_wyboru"), U.get("data_umowy"),
                                      ustawowe=ustawowe, termin_pytan=t_pyt, liczba_ofert=liczba_ofert),
            "pytania": PZ.pytania_stan(P.get("pytania") or [], t_pyt, unijne, ustawowe=ustawowe), "zmiany_terminu": P.get("zmiany_terminu") or [],
            "ustawowe": ustawowe, "termin_pytan_od": t_pyt, "pytania_od_nowego_terminu": bool(K.get("pytania_od_nowego_terminu"))}


def _kontrola_terminu_wykonania(K, rz, opublikowane=False, netto=0.0):
    """Termin wykonania z kroku „Szczegóły” (i terminy części): data nieistniejąca, wcześniejsza niż planowana data wszczęcia albo termin
    składania ofert, miniona – błąd (termin wykonania to obowiązkowy element SWZ i umowy, art. 281 ust. 1 pkt 6, art. 436 pkt 1 Pzp);
    mniej niż 30 dni po terminie ofert – ostrzeżenie. Okres („18 miesięcy od podpisania umowy”) nie jest sprawdzany. → [(waga, opis)]."""
    P_ = K.get("potrzeba") or {}
    teksty = [("", P_.get("termin") or P_.get("okres") or "")]
    cz_ = S.KZ.czesci_normalizuj(K.get("czesci"), netto)
    if cz_["podzial"]:
        teksty += [(f"Część {x['nr']}: ", x["termin"]) for x in cz_["lista"] if x.get("termin")]
    dw, to, dzis = KO.data_iso(K.get("data_wszczecia")), KO.data_iso(K.get("termin_ofert")), dt.date.today()
    wyn = []
    for prefiks, tekst in teksty:
        d, bl = KO.data_terminu_wykonania(tekst)
        if bl:
            wyn.append(("blad", f"{prefiks}termin wykonania „{str(tekst)[:60]}”: {bl} – popraw datę."))
        elif not d:
            continue
        elif dw and d < dw:
            wyn.append(("blad", f"{prefiks}termin wykonania ({d:%d.%m.%Y}) jest wcześniejszy niż planowana data wszczęcia postępowania ({dw:%d.%m.%Y}) – "
                                "popraw termin wykonania albo datę wszczęcia."))
        elif to and d <= to:
            wyn.append(("blad", f"{prefiks}termin wykonania ({d:%d.%m.%Y}) nie jest późniejszy niż termin składania ofert ({to:%d.%m.%Y}) – "
                                "wykonawca nie może wykonać zamówienia przed zawarciem umowy; popraw termin wykonania."))
        elif d < dzis and not opublikowane:
            wyn.append(("blad", f"{prefiks}termin wykonania ({d:%d.%m.%Y}) już minął – popraw termin wykonania."))
        elif to and (d - to).days < 30:
            wyn.append(("ostrzezenie", f"{prefiks}termin wykonania ({d:%d.%m.%Y}) przypada mniej niż 30 dni po terminie składania ofert ({to:%d.%m.%Y}) – "
                                       "uwzględnij czas na ocenę ofert, wybór, termin na odwołania i zawarcie umowy."))
    return [(w_, o_[:1].upper() + o_[1:]) for w_, o_ in wyn]


def _kreator_stan(pid):
    m = S.meta(pid)
    K = m.get("kreator") or {}
    rz = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
    netto, netto_zrodlo = _netto_zam_zrodlo(m)
    w_dok = S.NR._f(K.get("wartosc_dok"))
    rozbieznosc = None
    if w_dok and netto and K.get("wartosc_decyzja") not in ("dokumenty", "kosztorys") and not (0.8 <= netto / w_dok <= 1.25):
        rozbieznosc = {"dokumenty": w_dok, "zrodlo": K.get("wartosc_dok_zrodlo") or "", "kosztorys": netto, "krotnosc": round(max(netto, w_dok) / min(netto, w_dok), 1)}
    netto_trybu = w_dok if (rozbieznosc or (w_dok and not netto)) else netto  # do decyzji zamawiającego tryb liczony z wartości podanej w dokumentach
    K = dict(K, potrzeba=KO.potrzeba_rodzaju(rz, K.get("potrzeba")))  # dalej tylko odpowiedzi bieżącego rodzaju zamówienia
    tryb, tryb_opis, tw = S.KZ.tryb_z_wartosci(netto_trybu, rz, K.get("data_wszczecia") or None, K.get("prywatny"),
                                               K.get("typ_zamawiajacego") == "centralny", bool(K.get("uslugi_spoleczne")))
    tryb_nieustalony = not netto_trybu and not K.get("prywatny") and K.get("tryb_wybrany") not in S.KZ.TRYBY_WYBOR
    orientacyjne = bool(netto_trybu) and not K.get("prywatny") and netto_zrodlo != "szacowanie" and not (rozbieznosc is None and K.get("wartosc_decyzja") == "dokumenty")
    if tryb_nieustalony:
        tryb_opis = "Tryb nieustalony – brak wartości zamówienia"
    elif orientacyjne and K.get("tryb_wybrany") not in S.KZ.TRYBY_WYBOR:
        tryb_opis += " – orientacyjnie, do czasu szacowania wartości"
    # jawny wybór trybu (prawnik / zamawiający) – wartość nadal sprawdzana; różnica do decyzji
    tryb_wartosc, opis_wartosc, rozb_wyboru = tryb, tryb_opis, None
    tw_ = K.get("tryb_wybrany")
    if tw_ in S.KZ.TRYBY_WYBOR:
        nazwa_, baza_ = S.KZ.TRYBY_WYBOR[tw_]
        rozb_wyboru = None if K.get("tryb_wybor_decyzja") == tw_ else S.KZ.porownaj_wybor_trybu(tw_, tryb_wartosc, opis_wartosc)
        if rozb_wyboru:
            rozb_wyboru["kod_wyboru"] = tw_
        if baza_ in ("pzp_podstawowy", "pzp_nieograniczony", "ponizej_130"):
            tryb = baza_
        tryb_opis = nazwa_
    vat_ = _stawka_vat(m, K)[0]  # ta sama stawka co w piśmie o kwocie i w ocenie ofert (ZE-27); nieustalona – 23%
    warunki_prop = S.KZ.warunki_domyslne(rz, tryb, netto, vat_)  # propozycja programu dla bieżącej wartości i trybu (pola niezmienione ręcznie)
    warunki = dict(warunki_prop, **(K.get("warunki") or {}))
    cz_ = S.KZ.czesci_normalizuj(K.get("czesci"), netto)
    powody_ = (((K.get("elementy") or {}).get("czesci") or {}).get("dane") or {}).get("powody") or []
    uzas_cz = "; ".join([str(x) for x in powody_ if x] + ([cz_["uzasadnienie"]] if cz_["uzasadnienie"] else []))
    if not cz_["podzial"] and uzas_cz:
        warunki_prop["czesci"] = "bez podziału na części – " + uzas_cz
    if not cz_["podzial"] and not (K.get("warunki") or {}).get("czesci") and uzas_cz:
        warunki["czesci"] = "bez podziału na części – " + uzas_cz
    if tryb_nieustalony:  # brak wartości – tryb nieustalony, bez minimalnego terminu (karta 04 §9)
        dni, dni_opis = None, "nieustalony – brak wartości zamówienia (ustal wartość w kroku „Wartość i tryb”)"
    elif tw_ == "zasada_konkurencyjnosci":  # wybrana zasada konkurencyjności: terminy z wytycznych (7 / 14 / 30 dni)
        dni, dni_opis = S.KZ.min_termin_ofert("konkurencyjnosc", rz, netto_trybu)
    else:
        dni, dni_opis = S.KZ.min_termin_ofert(tryb, rz)
    tdk = K.get("tryb_dok_kontrola") or S.KZ.tryb_z_tekstu(K.get("tryb_dok")) or {}
    rozb_trybu = None if K.get("tryb_decyzja") == tdk.get("kod") else S.KZ.porownaj_tryb(tdk.get("kod"), tdk.get("opis") or K.get("tryb_dok"), tryb, tryb_opis)
    if rozb_trybu:
        rozb_trybu.update(cytat=tdk.get("cytat", ""), kod_dok=tdk.get("kod"))
    R = RZ.reguly(K.get("prywatny"))  # reguły gminy (Pzp) albo wspólnoty (bez Pzp) – reguly_zamowien.py
    pryw = R.prywatny
    if pryw and (K.get("zaproszenia") or {}).get("kandydaci"):  # kandydaci, którzy zrezygnowali z zaproszeń – oznaczeni (kopia, bez zapisu)
        R_ = S._rezygnacje()
        K = dict(K, zaproszenia=dict(K["zaproszenia"], kandydaci=[dict(k, rezygnacja=S._zrezygnowal(k, R_)) for k in K["zaproszenia"]["kandydaci"]]))
    if pryw:  # wspólnota: tryb, warunki i termin z reguł wspólnoty zastępują wyliczone ścieżką Pzp
        tryb = R.tryb(K, tryb)
        tryb_opis, rozb_wyboru, rozb_trybu = R.tryby_wybor(K)[tryb], None, None
        warunki = R.warunki(rz, K)
        warunki_prop = R.warunki(rz, dict(K, warunki={}))
        dni, dni_opis = R.termin(rz)
    d = S.pdir(pid)
    wz = os.path.join(d, "wzory")
    kon = os.path.join(d, "dokumenty_koncowe")
    props = K.get("propozycje") or []
    dec = K.get("decyzje") or {}
    # ---- kontrole kroków (stałe reguły, bez AI): komunikaty i zaliczenie kroków
    kom = {k: [] for k in ("opis", "potrzeba", "wzory", "wartosc", "warunki", "dokumenty", "zmiany", "gotowe")}
    U = lambda krok, waga, opis: kom[krok].append({"waga": waga, "opis": opis})
    braki_p = KO.braki_szczegolow(rz, K.get("potrzeba"))
    if braki_p and (K.get("sciezka") or "nowe") != "wzory":
        U("potrzeba", "ostrzezenie", "Krok niepełny – brakuje: " + "; ".join(braki_p) + ".")
    opubl = bool((K.get("postepowanie") or {}).get("data_publikacji"))
    bl_term = _kontrola_terminu_wykonania(K, rz, opubl, netto)
    for waga_, opis_ in bl_term:
        U("potrzeba", waga_, opis_)
    bl_term = [o_ for w_, o_ in bl_term if w_ == "blad"]
    dw_ = KO.data_iso(K.get("data_wszczecia"))
    if dw_ and dw_ < dt.date.today() and not opubl:
        U("wartosc", "ostrzezenie", f"Planowana data wszczęcia ({dw_:%d.%m.%Y}) już minęła – wpisz aktualną planowaną datę publikacji. Od niej zależą próg "
                                    "stosowania Pzp (130 000 / 170 000 zł), aktualność szacowania (art. 36 Pzp) i minimalny termin składania ofert.")
    odl = [S.KZ.RODZAJE.get(r_, r_).lower() for r_, v_ in (K.get("potrzeba_odlozone") or {}).items() if v_ and r_ != rz]
    if odl:
        U("potrzeba", "info", "Odpowiedzi wpisane dla innego rodzaju zamówienia (" + ", ".join(odl) + ") są odłożone i nie trafiają do dokumentów – wrócą po przywróceniu tego rodzaju.")
    P_ = K.get("potrzeba") or {}
    if "PFU" in str(P_.get("projekt") or "") and not pryw and not ((K.get("szacowanie") or {}).get("podstawa") or "").startswith("pfu"):
        U("wartosc", "info", "W „Szczegółach” wskazano, że jest tylko program funkcjonalno-użytkowy – podstawą wartości są planowane koszty z PFU (art. 34 ust. 1 Pzp).")
    if str(P_.get("przedmiar") or "").startswith("nie") and not netto:
        U("wartosc", "info", "Nie ma przedmiaru – ilości trzeba ustalić przed szacowaniem wartości.")
    if str(P_.get("opcja") or "").startswith("tak") and not pryw and not ((K.get("szacowanie") or {}).get("korekty") or {}).get("opcje"):
        U("wartosc", "ostrzezenie", "Przewidziano prawo opcji – wartość zamówienia obejmuje największy możliwy zakres z opcją (art. 31 ust. 2 Pzp). Dodaj korektę za opcję w szacowaniu.")
    if tw.get("ostrzezenie") and not pryw:
        U("wartosc", "ostrzezenie", tw["ostrzezenie"])
    if tryb_nieustalony:
        U("wartosc", "ostrzezenie", "Brak wartości zamówienia – tryb nieustalony. " + ("Przeprowadź szacowanie wartości." if not pryw else "Wpisz wartość albo przygotuj szacunek kosztów."))
    elif orientacyjne:
        U("wartosc", "ostrzezenie", "Wartość nie pochodzi z szacowania – tryb jest orientacyjny. Zamawiający publiczny ustala wartość w szacowaniu (art. 28–36 Pzp); "
                                    "do tego czasu komplet dokumentów nie zostanie przygotowany.")
    zakres_zmieniony = bool(not pryw and netto_zrodlo == "szacowanie" and K.get("szacowanie_odcisk") and K["szacowanie_odcisk"] != S.odcisk_zakresu(K, rz))
    if zakres_zmieniony:
        U("wartosc", "blad", "Po szacowaniu zmienił się zakres zamówienia (opis, przedmiot albo ilości) – sprawdź szacowanie i zapisz je ponownie, żeby je potwierdzić (art. 36 ust. 2 Pzp).")
    kryt = [r_ for r_ in (rozb_wyboru, rozb_trybu) if r_ and r_.get("waga") == "krytyczna"]
    if kryt:
        U("wartosc", "blad", "Różnica krytyczna między trybem a wartością: " + kryt[0]["ocena"] + " Potwierdzenie wymaga pisemnego uzasadnienia.")
    if not pryw and not cz_["podzial"] and not uzas_cz:
        U("wartosc", "ostrzezenie", "Brak podziału na części wymaga uzasadnienia (art. 91 ust. 2 Pzp) – wybierz powody albo wpisz własne.")
    for b_ in cz_["bledy"]:
        U("wartosc", "blad", b_)
    kontrola_w = KO.kontrola_warunkow(warunki, rz, tryb, pryw, netto, K.get("termin_ofert"), K.get("godzina_ofert"), K.get("data_wszczecia"), dni,
                                      termin_wykonania=P_.get("termin") or P_.get("okres") or "", czesci=cz_["lista"] if cz_["podzial"] else None,
                                      opublikowane=opubl)
    for x_ in kontrola_w:
        U("warunki", x_["waga"], x_["opis"])
    brak_terminu = [] if str(K.get("termin_ofert") or "").strip() else ["termin składania ofert"]
    if not pryw and not str(K.get("godzina_ofert") or "").strip():
        brak_terminu.append("godzina składania ofert")
    if brak_terminu:  # bez terminu zamówienie nie jest gotowe do publikacji (karta 10 §4; art. 281 ust. 1 pkt 13 Pzp)
        U("warunki", "ostrzezenie", "Wpisz " + " i ".join(x_.replace("godzina", "godzinę") for x_ in brak_terminu) + (" – termin ustala zarząd; trafia do zapytania ofertowego." if pryw else
                                     f" – bez {'nich' if len(brak_terminu) > 1 else 'tego'} zamówienie nie będzie gotowe do publikacji (art. 281 ust. 1 pkt 13 Pzp)."))
    wt_ = K.get("warunki_tryb")
    if K.get("warunki") and wt_ and not pryw and str(wt_).startswith("pzp") != str(tryb).startswith("pzp"):
        rozne_ = [S.KZ.ETYKIETY_WARUNKOW.get(a_, a_) for a_, v_ in (K.get("warunki") or {}).items()
                  if a_ in warunki_prop and a_ != "czesci" and str(v_).strip() != str(warunki_prop[a_]).strip()]
        if rozne_:
            U("warunki", "ostrzezenie", f"Tryb zmienił się od zapisu warunków ({'Pzp → poza Pzp' if str(wt_).startswith('pzp') else 'poza Pzp → Pzp'}). "
                                        "Pola wpisane ręcznie różnią się od propozycji dla bieżącego trybu – sprawdź: " + ", ".join(rozne_) + ".")
    blokada = []  # czego brakuje, żeby przygotować komplet dokumentów
    if not K.get("opis"):
        blokada.append("opis zamówienia (krok „Co zamawiasz”)")
    if braki_p and (K.get("sciezka") or "nowe") != "wzory":
        blokada.append("pola wymagane w kroku „Szczegóły”: " + "; ".join(braki_p))
    if bl_term:
        blokada.append("poprawny termin wykonania w kroku „Szczegóły” (" + "; ".join(bl_term)[:300] + ")")
    if tryb_nieustalony or orientacyjne:
        blokada.append("wartość zamówienia z szacowania (krok „Wartość i tryb”)")
    if zakres_zmieniony:
        blokada.append("ponowne potwierdzenie szacowania po zmianie zakresu (krok „Wartość i tryb”)")
    if rozbieznosc:
        blokada.append("decyzja o wartości – dokumenty i szacowanie podają różne kwoty (krok „Wartość i tryb”)")
    if kryt:
        blokada.append("uzasadnienie różnicy krytycznej w trybie (krok „Wartość i tryb”)")
    if any(x_["waga"] == "blad" for x_ in kontrola_w):
        blokada.append("błędy w warunkach zamówienia (krok „Warunki”)")
    for b_ in blokada:
        U("dokumenty", "blad", "Brakuje: " + b_ + ".")
    bez_dec = [p for p in props if (p.get("waga") or "").lower() in ("krytyczna", "istotna") and (dec.get(p["id"]) or {}).get("decyzja") not in ("tak", "nie")]
    if bez_dec:
        U("zmiany", "ostrzezenie", f"Bez decyzji: {len(bez_dec)} propozycji krytycznych i istotnych – każda wymaga „przyjmuję” albo „odrzucam” przed wprowadzeniem zmian.")
    dok_st = _dokumenty_stan((m.get("dokumentacja") or {}).get("pliki") or [], [k for k in S.KZ.komplet_dokumentow(tw_, tryb_wartosc) if k in S.ZAM.DOKUMENTY],
                             pryw, K.get("sciezka") or "nowe", sorted(os.listdir(wz)) if os.path.isdir(wz) else [])
    kon_pl = sorted(os.listdir(kon)) if os.path.isdir(kon) else []
    znaczniki = {}
    for f_, sc_ in [(f_, os.path.join(d, f_)) for f_ in (m.get("dokumentacja") or {}).get("pliki") or []] + \
                   [(f_, os.path.join(kon, f_)) for f_ in kon_pl if not f_.endswith("_ze_zmianami.docx")]:
        n_ = 0 if f_.startswith(("Protokol_wyboru", "Protokol_postepowania")) else _znaczniki(sc_)  # protokół wyboru wypełnia się po otwarciu ofert – nie jest brakiem przed publikacją
        if n_:
            znaczniki[f_] = n_
    for f_ in dok_st[1]:
        U("dokumenty", "ostrzezenie", f"Nie przygotowano: {f_} – przygotuj ponownie.")
    kolizje = {}
    if not pryw:
        for f_, sc_ in [(f_, os.path.join(d, f_)) for f_ in (m.get("dokumentacja") or {}).get("pliki") or []] + \
                       [(f_, os.path.join(kon, f_)) for f_ in kon_pl if not f_.endswith("_ze_zmianami.docx")]:
            k_ = _kolizje_dok(sc_, tryb)
            if k_ and (not kon_pl or f_ in kon_pl):
                kolizje[f_] = k_
                U("zmiany" if kon_pl else "dokumenty", "blad", f"{f_}: zapis sprzeczny z Pzp – " + "; ".join(k_) + ". Popraw przed publikacją.")
    if cz_["bledy"]:
        dok_st = (False, dok_st[1])
    do_dec = (m.get("dokumentacja") or {}).get("do_decyzji") or []
    elementy = _elementy_stan(pid, m, K, tryb, rz, netto)
    zatw = bool(kon_pl) and (not K.get("przeglad_nr") or K.get("zatwierdzony_nr") == K.get("przeglad_nr"))
    wzory_ok = dok_st[0] if (K.get("sciezka") or "nowe") == "wzory" else bool(os.path.isdir(wz) and os.listdir(wz))
    kroki_ok = {"opis": bool(K.get("opis")), "potrzeba": not braki_p and not bl_term, "wzory": wzory_ok,
                "wartosc": bool(netto) and not rozbieznosc and (pryw or netto_zrodlo == "szacowanie" or K.get("wartosc_decyzja") == "dokumenty") and not kryt
                and (pryw or cz_["podzial"] or bool(uzas_cz)) and not cz_["bledy"] and not zakres_zmieniony,
                "warunki": (bool(K.get("warunki")) or bool(K.get("warunki_zapisane"))) and not any(x_["waga"] == "blad" for x_ in kontrola_w)
                and not brak_terminu,
                "dokumenty": dok_st[0], "zmiany": zatw}
    braki_g = []  # stan „gotowe do publikacji”
    nazwy_k = dict(opis="Co zamawiasz", potrzeba="Szczegóły", wzory="Twoje wzory", wartosc="Wartość i tryb", warunki="Warunki", dokumenty="Komplet dokumentów", zmiany="Sprawdzenie i zmiany")
    for k_ in (["opis", "wzory", "wartosc", "warunki", "zmiany"] if (K.get("sciezka") or "nowe") == "wzory" else ["opis", "potrzeba", "wartosc", "warunki", "dokumenty", "zmiany"]):
        if not kroki_ok[k_]:
            braki_g.append(f"krok „{nazwy_k[k_]}” nie jest zaliczony")
    if bl_term and (K.get("sciezka") or "nowe") == "wzory":
        braki_g.append("termin wykonania: " + "; ".join(bl_term)[:200])
    if brak_terminu:
        braki_g.append("brak: " + " i ".join(brak_terminu) + " (krok „Warunki”)")
    for e_ in elementy:
        if e_["status"] not in ("ok", "nd"):
            braki_g.append("lista kontrolna: " + e_["opis"][:90])
    for f_, n_ in znaczniki.items():
        if not kon_pl or f_ in kon_pl:
            braki_g.append(f"{f_}: {n_} {'pole' if n_ == 1 else 'pól'} do uzupełnienia [UZUPEŁNIJ]")
    for f_, k_ in kolizje.items():
        braki_g.append(f"{f_}: zapis sprzeczny z Pzp ({len(k_)})")
    if any(not x_.get("ok") for x_ in do_dec):
        braki_g.append(f"sprawy do decyzji: {sum(1 for x_ in do_dec if not x_.get('ok'))} nierozstrzygniętych")
    if (K.get("reczne") or []) and not K.get("reczne_potwierdzone"):
        braki_g.append(f"zmiany do wprowadzenia ręcznie: {len(K['reczne'])} – wprowadź i potwierdź")
    for b_ in braki_g:
        U("gotowe", "ostrzezenie", b_)
    return {"komunikaty": kom, "kroki_ok": kroki_ok, "gotowosc": {"gotowe": not braki_g, "braki": braki_g}, "blokada_dokumentow": blokada,
            "znaczniki": znaczniki, "kolizje": kolizje, "tryb_nieustalony": tryb_nieustalony, "netto_orientacyjne": orientacyjne, "kontrola_warunkow": kontrola_w,
            "wymagane_szczegoly": list(KO.WYMAGANE.get(rz, ())), "termin_z_opisu": KO.termin_z_opisu(K.get("opis")),
            "limity": {"krotki": KO.LIMIT_KROTKI, "dlugi": KO.LIMIT_DLUGI, "pliki": KO.LIMIT_PLIKOW},
            "typ_zamawiajacego": K.get("typ_zamawiajacego") or "samorzadowy", "uslugi_spoleczne": bool(K.get("uslugi_spoleczne")),
            "bez_decyzji": len(bez_dec),
            "projekt": {"id": pid, "nazwa": m.get("nazwa")}, "K": K, "rodzaj": rz, "rodzaj_nazwa": S.KZ.RODZAJE.get(rz, rz), "sciezka": K.get("sciezka") or "nowe",
            "pytania": S.KZ.PYTANIA.get(rz, []), "warunki": warunki, "warunki_propozycja": warunki_prop, "tryb_z_wartosci": tryb_wartosc, "pomoc": R.pomoc, "netto": netto, **_brutto_zam(m, K, netto),
            "z_kosztorysu": bool((m.get("oferta") or {}).get("netto")), "tryb": tryb, "tryb_opis": tryb_opis, "tryb_info": tw,
            "min_dni": dni, "min_dni_opis": dni_opis, "kosztorys": m.get("kosztorys"),
            "wzory": sorted(os.listdir(wz)) if os.path.isdir(wz) else [], "dokumenty": (m.get("dokumentacja") or {}).get("pliki") or [],
            "biblioteka": sorted(os.listdir(S._kat_wzorow(rz))) + sorted(os.listdir(S._kat_wzorow("ogolne"))),
            "biblioteka_wg": [[rz, f] for f in sorted(os.listdir(S._kat_wzorow(rz)))] + [["ogolne", f] for f in sorted(os.listdir(S._kat_wzorow("ogolne")))],
            "propozycje": [dict(p, decyzja=(dec.get(p["id"]) or {}).get("decyzja", ""), nowy_edyt=(dec.get(p["id"]) or {}).get("nowy")) for p in props],
            "koncowe": kon_pl, "reczne": K.get("reczne") or [],
            "lista": R.lista_kontrolna(rz, tryb, K),
            "podmioty": R.podmioty, "podmiot": R.podmiot(K), "notatka": m.get("notatka_szac"), "formularz_pusty": m.get("kosztorys_pusty"),
            "elementy": elementy, "powody_czesci": S.KZ.POWODY_BRAKU_CZESCI,
            "czesci_powody": {"powody": list(powody_), "dodatkowe": str((((K.get("elementy") or {}).get("czesci") or {}).get("dane") or {}).get("dodatkowe") or "")},
            "czesci": cz_, "czesci_propozycja": K.get("czesci_propozycja"),
            "czesci_zwyciezcy": _zwyciezcy_czesci(m), "czesci_realizacje": K.get("czesci_realizacje") or {},
            "termin_ofert_dni": (lambda t_: (t_ - dt.date.today()).days if t_ else None)(S.ZP.termin_ofert(K)),
            "dzialy_kosztorysu": [d for d in S.dzialy_kosztorysu(pid) if d.get("nazwa")],
            "rozbieznosc_wartosci": rozbieznosc, "wartosc_dok": w_dok or None, "wartosc_decyzja": K.get("wartosc_decyzja"),
            "netto_zrodlo": netto_zrodlo, "prywatny": bool(K.get("prywatny")), "szacowanie": S.SZ.oczysc(K.get("szacowanie") or {}, rz),
            "szac_wynik": S.SZ.wylicz(K.get("szacowanie") or {}, rz, K.get("data_wszczecia") or None), "szac_podstawy": S.SZ.podstawy_dla(rz),
            "szac_typy": S.SZ.TYPY_ZRODEL, "szac_metody": S.SZ.METODY,
            "rozbieznosc_trybu": rozb_trybu, "tryb_dok": K.get("tryb_dok") or "",
            "tryb_wybrany": (tryb if pryw else (tw_ if tw_ in S.KZ.TRYBY_WYBOR else "")),
            "tryby_wybor": R.tryby_wybor(K),
            "tryb_z_wartosci_opis": opis_wartosc, "rozbieznosc_wyboru": rozb_wyboru,
            "komplet": [[k, R.etykieta_dok(k)] for k in S.KZ.komplet_dokumentow(tw_, tryb_wartosc) if k in S.ZAM.DOKUMENTY],
            "dokumenty_gotowe": dok_st[0], "dokumenty_brak": dok_st[1], "rok_planu": S.KZ.rok_planu(K),
            "do_decyzji": do_dec,
            "import": K.get("import") or {}, "zrodla": sorted(os.listdir(os.path.join(S.pdir(pid), "kreator_zrodla"))) if os.path.isdir(os.path.join(S.pdir(pid), "kreator_zrodla")) else [],
            "etykiety_warunkow": S.KZ.ETYKIETY_WARUNKOW,
            "finansowanie": {k: v for k, v in _fin_kreatora(pid, K).items() if k != "zrodla"},
            "postepowanie": None if pryw else _postepowanie_stan(K, tryb_wartosc == "pzp_nieograniczony", dni, ustawowe=str(tryb).startswith("pzp"),
                                                               liczba_ofert=_liczba_ofert(m)),
            "profil_firmy": ", ".join(x for x in (S.cfg().get("firma_nazwa"), S.cfg().get("firma_adres"), ("NIP " + S.cfg()["firma_nip"]) if S.cfg().get("firma_nip") else "") if x)}


_ZNACZNIKI = {}


def _znaczniki(sciezka):
    """Liczba pól [UZUPEŁNIJ w pliku Word – z pamięcią według daty zmiany pliku (stan kreatora jest odczytywany często)."""
    if not sciezka.lower().endswith(".docx") or not os.path.isfile(sciezka):
        return 0
    k = (sciezka, os.path.getmtime(sciezka))
    if k not in _ZNACZNIKI:
        if len(_ZNACZNIKI) > 2000:
            _ZNACZNIKI.clear()
        _ZNACZNIKI[k] = KO.znaczniki_uzupelnij(sciezka, os.path.basename(sciezka).startswith(("Oswiadczenia", "Formularz")))
    return _ZNACZNIKI[k]


_KOLIZJE = {}


def _kolizje_dok(sciezka, tryb):
    """Zapisy w dokumencie Word sprzeczne z parametrami ustawowymi trybu (np. przedłużenie związania o 60 dni w trybie podstawowym)."""
    if not sciezka.lower().endswith(".docx") or not os.path.isfile(sciezka) or not str(tryb or "").startswith("pzp"):
        return []
    k = (sciezka, os.path.getmtime(sciezka), tryb)
    if k not in _KOLIZJE:
        if len(_KOLIZJE) > 2000:
            _KOLIZJE.clear()
        try:
            import docx as _d
            dd = _d.Document(sciezka)
            teksty = [p.text for p in dd.paragraphs] + [c.text for t in dd.tables for r in t.rows for c in r.cells]
        except Exception:
            teksty = []
        wyn = []
        for t_ in teksty:
            for o_ in KO.kolizje_z_przepisami(t_, tryb):
                if o_ not in wyn:
                    wyn.append(o_)
        _KOLIZJE[k] = wyn
    return _KOLIZJE[k]


def _elementy_stan(pid, m, K, tryb, rz, netto):
    """Lista kontrolna przed publikacją, która działa: status każdego elementu, przygotowane pismo / własny wzór."""
    E = K.get("elementy") or {}
    kat = os.path.join(S.pdir(pid), "dokumenty_postepowania")
    dok = (m.get("dokumentacja") or {}).get("pliki") or []
    wyn = []
    podz_ = bool((K.get("czesci") or {}).get("podzial"))
    fin = _fin_kreatora(pid, K)
    lista_el = RZ.reguly(K.get("prywatny")).elementy(rz, podz_, tryb, K)
    if fin["liczba"] and not any(e["id"] == "finansowanie" for e in lista_el):  # zamawiający publiczny: pozycja, gdy zamówienie ma finansowanie
        lista_el = lista_el + [dict(ELEMENT_FIN_GMINY)]
    for e in lista_el:
        z = dict(E.get(e["id"]) or {})
        st = z.get("status") or ""
        if e["id"] == "finansowanie" and fin["liczba"] and st != "nd":  # zalicza się samo: dokumenty przygotowane po ostatniej zmianie finansowania
            nieodcz = [z_ for z_ in fin["zrodla"] if not z_.get("odczytano")
                       and not any((z_.get("wymagania") if isinstance(z_.get("wymagania"), dict) else {}).get(k_) for k_ in ("kwota", "termin_zakonczenia_realizacji"))]
            st = "ok" if fin["aktualne"] and not nieodcz else ""
            z["uwaga"] = (f"Finansowanie: {fin['opis']}. " + (
                "Nie odczytano umowy finansowania: " + ", ".join(S.FIN.TYPY.get(z_.get("typ"), "finansowanie") + (f" ({z_['instytucja']})" if z_.get("instytucja") else "")
                                                                 for z_ in nieodcz)
                + " – wgraj umowę i odczytaj wymagania albo wpisz ręcznie kwotę i termin zakończenia realizacji; do tego czasu zamówienie nie jest "
                  "gotowe do publikacji." if nieodcz else
                "Dokumenty uwzględniają wymagania finansowania." if st == "ok" else
                          "Dokumenty przygotowano przed ostatnią zmianą finansowania – przygotuj je ponownie albo sprawdź w kroku „Sprawdzenie i zmiany”."
                          if fin["dok_nr"] is not None else
                          "Przygotuj dokumenty (albo sprawdź własne wzory) – wymagania finansowania trafią do zapytania, umowy i harmonogramu."))
        if e["id"] == "kosztorys":  # pliki kosztorysu i notatki rozpoznawane na dysku
            if m.get("kosztorys") and os.path.isfile(os.path.join(S.pdir(pid), m["kosztorys"])):
                z["plik_kosztorys"] = m["kosztorys"]
            if m.get("notatka_szac") and os.path.isfile(os.path.join(S.pdir(pid), m["notatka_szac"])):
                z["plik_notatka"] = m["notatka_szac"]
            if RZ.reguly(K.get("prywatny")).dokument_podstawy:  # zamawiający publiczny: dokument podstawy (kosztorys inwestorski / PFU), nie kosztorys AI
                z.pop("plik_kosztorys", None)
                dk_ = ((K.get("szacowanie") or {}).get("dokument") or {}).get("plik")
                if dk_ and os.path.isfile(os.path.join(S.pdir(pid), "szacowanie", dk_)):
                    z["plik_kosztorys"] = "szacowanie/" + dk_
                if not st:
                    st = "ok" if S.SZ.wylicz(K.get("szacowanie") or {}, rz, K.get("data_wszczecia") or None)["kompletne"] and z.get("plik_notatka") else ""
            if not st:
                st = "ok" if netto and z.get("plik_notatka") else ""
        plik_auto = None
        if e["id"] == "oswiadczenia":  # plik z kompletu dokumentów – rozpoznawany na dysku, nie tylko z listy ostatniego przygotowania
            wz_ = os.path.join(S.pdir(pid), "wzory")
            plik_auto = next((f for f in sorted(os.listdir(S.pdir(pid))) if f.startswith(S.ZAM.DOKUMENTY["oswiadczenia"][1] + "_") and f.endswith(".docx")), None)
            if not st:
                st = "ok" if plik_auto or any("świadcz" in f.lower() for f in (os.listdir(wz_) if os.path.isdir(wz_) else [])) else ""
        if z.get("plik") and not os.path.isfile(os.path.join(kat, z["plik"])):
            z.pop("plik")
        if e.get("rodzaj") == "sprawdzenie" and not st:  # pozycje sprawdzane w kroku 6: zaliczone po jego zatwierdzeniu
            kon_ = os.path.join(S.pdir(pid), "dokumenty_koncowe")
            if os.path.isdir(kon_) and os.listdir(kon_) and K.get("zatwierdzony_nr") == K.get("przeglad_nr") and K.get("przeglad_nr") \
                    and not ((K.get("reczne") or []) and not K.get("reczne_potwierdzone")):
                st = "ok"
                z["uwaga"] = z.get("uwaga") or "Sprawdzone w kroku „Sprawdzenie i zmiany”."
        wyn.append(dict(e, status=st, plik=z.get("plik"), wlasny=z.get("wlasny"), dane=z.get("dane") or {}, plik_auto=plik_auto,
                        plik_kosztorys=z.get("plik_kosztorys"), plik_notatka=z.get("plik_notatka"), netto=netto if e["id"] == "kosztorys" else None,
                        powod_nd=z.get("powod_nd") or "",
                        uwaga=z.get("uwaga") or ""))
    return wyn


@bp.post("/api/projekty/<pid>/kreator/element")
@S.wymaga_logowania
def kreator_element(pid):
    """Element listy kontrolnej: akcja „przygotuj” (pismo Word z danych kreatora), „status” (ok / nie dotyczy / do zrobienia)."""
    j = request.json or {}
    el = str(j.get("id") or "")
    st = _kreator_stan(pid)
    if el not in {e["id"] for e in st["elementy"]}:
        return jsonify({"blad": "Nieznany element."}), 400
    m = S.meta(pid)
    with S.BLOKADA:
        m = S.meta(pid)
        E = m.setdefault("kreator", {}).setdefault("elementy", {}).setdefault(el, {})
        if isinstance(j.get("dane"), dict):
            E["dane"] = {k: (v if isinstance(v, list) else str(v or "")[:2000]) for k, v in j["dane"].items()}
        if j.get("akcja") == "status":
            if j.get("status") == "nd":
                pw_ = str(j.get("powod") or (j.get("dane") or {}).get("powod_nd") or E.get("powod_nd") or "").strip()
                if len(pw_) < 3:
                    return jsonify({"blad": "„Nie dotyczy” wymaga krótkiego powodu."}), 400
                E["powod_nd"] = pw_[:500]
            E["status"] = j.get("status") if j.get("status") in ("ok", "nd", "") else ""
        S.zapisz_meta(pid, m)
    if j.get("akcja") == "przygotuj":
        kat = os.path.join(S.pdir(pid), "dokumenty_postepowania")
        os.makedirs(kat, exist_ok=True)
        ctx = {"nazwa": st["projekt"]["nazwa"], "zamawiajacy": S.zamawiajacy_projektu(m), "rodzaj": st["rodzaj"], "tryb_opis": st["tryb_opis"],
               "netto": st["netto"], "brutto": st["brutto"], "stawka_vat": st["stawka_vat"], "stawka_vat_znana": st["stawka_vat_znana"],
               "warunki": st["warunki"], "potrzeba": st["K"].get("potrzeba") or {},
               "znak": st["K"].get("znak", ""), "termin_ofert": st["K"].get("termin_ofert", ""), "opis": st["K"].get("opis", ""),
               "data_wszczecia": st["K"].get("data_wszczecia", ""),
               "czesci_powody": (((S.meta(pid).get("kreator") or {}).get("elementy") or {}).get("czesci") or {}).get("dane", {}).get("powody") or []}
        nazwa = S.KZ.PLIKI_PISM.get(el, el) + ".docx"
        if not S.KZ.pismo(el, ctx, (S.meta(pid).get("kreator") or {}).get("elementy", {}).get(el, {}).get("dane") or {}, os.path.join(kat, nazwa)):
            return jsonify({"blad": "Ten element nie jest pismem do przygotowania."}), 400
        with S.BLOKADA:
            m = S.meta(pid)
            E = m["kreator"]["elementy"][el]
            E.update(plik=nazwa, status="ok")
            S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/element/wzor")
@S.wymaga_logowania
def kreator_element_wzor(pid):
    """Własny wzór pisma zamawiającego dla elementu listy – trafia do wzorów (sprawdzanie i zmiany) i do kompletu."""
    el = request.form.get("id", "")
    f = request.files.get("plik")
    if not f:
        return jsonify({"blad": "Wybierz plik."}), 400
    wz = os.path.join(S.pdir(pid), "wzory")
    os.makedirs(wz, exist_ok=True)
    nazwa = S.secure_filename_pl(f.filename or "wzor.docx")
    f.save(os.path.join(wz, nazwa))
    S._konwertuj_pdf_wzorow(pid)
    with S.BLOKADA:
        m = S.meta(pid)
        m.setdefault("kreator", {}).setdefault("elementy", {}).setdefault(el, {}).update(wlasny=nazwa, status="ok")
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/zam/kreator")
@S.wymaga_logowania
def kreator_nowy():
    """Start kreatora: co zamawiasz + krótki opis + ścieżka (wzory / od początku) → projekt zamówienia."""
    j = request.get_json(silent=True)
    if not isinstance(j, dict):
        return jsonify({"blad": "Nieprawidłowe dane zamówienia."}), 400
    zly = [k for k in ("rodzaj", "opis", "nazwa", "budzet", "zamawiajacy", "sciezka") if j.get(k) is not None and not isinstance(j.get(k), (str, int, float))]
    if zly:
        return jsonify({"blad": "Nieprawidłowa wartość pola: " + ", ".join(f"„{k}”" for k in zly) + " – wpisz tekst."}), 400
    rz = j.get("rodzaj") if j.get("rodzaj") in S.KZ.RODZAJE else "roboty"
    opis = str(j.get("opis") or "").strip()
    if not opis and not j.get("z_dokumentow"):
        return jsonify({"blad": "Opisz krótko, co zamawiasz."}), 400
    budzet = str(j.get("budzet") or "").strip()
    if budzet and KO.kwota(budzet) is None:
        return jsonify({"blad": "Orientacyjny budżet: wpisz kwotę w złotych, np. 200 000 albo 200 000,00 (bez słów „ok.”, „tys.”, „mln”)."}), 400
    nazwa_auto = not str(j.get("nazwa") or "").strip()
    nazwa = str(j.get("nazwa") or opis or "Nowe zamówienie").strip()[:90]
    pryw_ = bool(j.get("prywatny")) and S.EDYCJA != "zamawiajacy"
    plan_ = j.get("plan") if isinstance(j.get("plan"), dict) else None
    if not j.get("potwierdz_powtorzenie") and not j.get("z_dokumentow"):  # to samo zamówienie drugi raz – ostrzeżenie, nie blokada
        for pid_, m_ in S.projekty_ro():
            if not m_ or m_.get("typ") != "zamowienie" or m_.get("archiwum") or bool(S.projekt_wspolnoty(m_)) != pryw_ \
                    or not S.ma_dostep(m_, session.get("login"), S.rola_sesji(), lista=True):
                continue
            pp_ = m_.get("plan_pozycja") or {}
            ten_plan = bool(plan_) and pp_.get("rok") == plan_.get("rok") and str(pp_.get("id")) == str(plan_.get("id"))
            if ten_plan or S.W.norm(str(m_.get("nazwa") or "")) == S.W.norm(nazwa):
                return jsonify({"blad": f"Takie zamówienie już istnieje: „{m_.get('nazwa')}”.",
                                "powtorzenie": {"id": pid_, "nazwa": m_.get("nazwa"), "powod": "ta sama pozycja planu zamówień" if ten_plan else "ta sama nazwa"}}), 409
    pid = uuid.uuid4().hex[:12]
    os.makedirs(os.path.join(S.PROJ, pid, "dokumenty"))
    m = {"id": pid, "nazwa": nazwa, "typ": "zamowienie", "strona": "zamawiajacy", "rodzaj_zamowienia": rz, "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
         "dla_prawnika": bool((request.json or {}).get("prawnik")),  # dokumentacja sporządzana przez prawnika – bez przekazania do realizacji
         "wlasciciel": S.konto_biezace(), "pominiete": [],
         "plan_pozycja": j.get("plan") if isinstance(j.get("plan"), dict) else None,  # pozycja rocznego planu (identyfikator do ogłoszenia)
         "kreator": {"rodzaj": rz, "opis": opis[:3000], "budzet": (f"{KO.kwota(budzet):.2f}" if budzet else ""), "sciezka": "wzory" if j.get("sciezka") == "wzory" else "nowe",
                     "krok": 2, "potrzeba": {}, "warunki": {}, "prywatny": pryw_, "zamawiajacy": str(j.get("zamawiajacy") or "")[:500], "nazwa_auto": nazwa_auto}}
    S.zapisz_meta(pid, m)
    # wzory z biblioteki „Moje wzory” NIE są kopiowane automatycznie – zamawiający dodaje wybrane (krok „wzory”), żeby nie mieszać postępowań
    return jsonify({"id": pid})


@bp.get("/api/projekty/<pid>/kreator")
@S.wymaga_logowania
def kreator_pobierz(pid):
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator")
@S.wymaga_logowania
def kreator_zapisz(pid):
    j = request.get_json(silent=True)
    if not isinstance(j, dict):
        return jsonify({"blad": "Nieprawidłowe dane – oczekiwano pól kreatora."}), 400
    zly = [k for k in ("rodzaj", "podmiot", "tryb_wybrany", "tryb_wybor_decyzja", "tryb_decyzja", "typ_zamawiajacego", "sciezka", "wartosc_decyzja")
           if j.get(k) is not None and not isinstance(j.get(k), str)]
    if zly:
        return jsonify({"blad": "Nieprawidłowa wartość pola: " + ", ".join(f"„{k}”" for k in zly) + " – wybierz wartość z listy."}), 400
    for k, et in (("data_wszczecia", "Planowana data wszczęcia"), ("termin_ofert", "Termin składania ofert")):  # daty: RRRR-MM-DD albo DD.MM.RRRR
        if k in j and str(j[k] if j[k] is not None else "").strip():
            d_ = KO.data_iso(j[k]) if isinstance(j[k], str) else None
            if not d_:
                return jsonify({"blad": f"{et}: nieprawidłowa data „{str(j[k])[:20]}” – wpisz istniejącą datę w zapisie RRRR-MM-DD albo DD.MM.RRRR."}), 400
            j[k] = d_.isoformat()
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {"rodzaj": m.get("rodzaj_zamowienia") or "roboty", "sciezka": "nowe", "krok": 1})
        for k in ("budzet", "wartosc_reczna"):  # kwoty: zamieniane na liczbę przy zapisie; zapis nieliczbowy odrzucany
            if k in j and str(j[k] or "").strip():
                if KO.kwota(j[k]) is None:
                    return jsonify({"blad": ("Orientacyjny budżet" if k == "budzet" else "Wartość") + ": wpisz kwotę w złotych, np. 200 000 albo "
                                            "200 000,00 (bez słów „ok.”, „tys.”, „mln”)."}), 400
                j[k] = f"{KO.kwota(j[k]):.2f}"
        if isinstance(j.get("potrzeba"), dict):
            rz_p = j.get("rodzaj") if j.get("rodzaj") in S.KZ.RODZAJE else (K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty")
            j["potrzeba"], bl_ = KO.czysc_potrzebe(rz_p, j["potrzeba"])
            if bl_:
                return jsonify({"blad": " ".join(bl_)}), 400
        for k in ("opis", "budzet", "znak", "termin_ofert", "godzina_ofert", "wartosc_reczna", "data_wszczecia", "zamawiajacy", "tryb_uzasadnienie"):
            if k in j:
                K[k] = str(j[k] or "")[:(500 if k == "zamawiajacy" else 3000)]
        if j.get("typ_zamawiajacego") in ("samorzadowy", "centralny"):
            K["typ_zamawiajacego"] = j["typ_zamawiajacego"]
        for k in ("uslugi_spoleczne", "pytania_od_nowego_terminu", "reczne_potwierdzone"):
            if k in j:
                K[k] = bool(j[k])
        if j.get("sciezka") in ("wzory", "nowe"):
            K["sciezka"] = j["sciezka"]
        if j.get("rodzaj") in S.KZ.RODZAJE:
            _zmien_rodzaj(K, m, j["rodzaj"])
        if j.get("podmiot") in RZ.reguly(K.get("prywatny")).podmioty:  # wspólnota / mała wspólnota / spółdzielnia / deweloper
            K["podmiot"] = j["podmiot"]
        if "prywatny" in j and m.get("dla_prawnika"):  # moduł (gmina / wspólnota) ustalany przy tworzeniu – bez przenoszenia zamówień między modułami
            K["prywatny"] = bool(j["prywatny"])
        if isinstance(j.get("czesci"), dict):  # podział na części (art. 91) – tryb liczony z łącznej wartości
            cz = S.KZ.czesci_normalizuj(j["czesci"], _netto_zam(m))
            K["czesci"] = {k: v for k, v in cz.items() if k not in ("bledy", "suma")}
            if isinstance(j["czesci"].get("powody"), list):  # powody braku podziału (art. 91 ust. 2) – te same co w liście kontrolnej (pismo)
                Ec = K.setdefault("elementy", {}).setdefault("czesci", {})
                Dc = Ec.setdefault("dane", {})
                Dc["powody"] = [str(x)[:500] for x in j["czesci"]["powody"] if str(x or "").strip()][:12]
                Dc["dodatkowe"] = str(j["czesci"].get("dodatkowe") or "").strip()[:2000]
            W_ = K.setdefault("warunki", {})
            if cz["podzial"] and cz["lista"]:
                W_["czesci"] = f"zamówienie podzielone na {len(cz['lista'])} części: " + "; ".join(f"część {x['nr']} – {x['nazwa']}" for x in cz["lista"]) \
                    + ("" if not cz["max_ofert"] else f"; oferty maksymalnie na {cz['max_ofert']} części")
            elif str(W_.get("czesci") or "").startswith("zamówienie podzielone na"):
                W_.pop("czesci", None)  # powrót do wartości domyślnej (bez podziału – z uzasadnieniem)
        if j.get("wartosc_decyzja") in ("dokumenty", "kosztorys", ""):
            K["wartosc_decyzja"] = j["wartosc_decyzja"]
        if "tryb_wybrany" in j and (RZ.reguly(K.get("prywatny")).tryb_dozwolony(j["tryb_wybrany"]) or j["tryb_wybrany"] in ("", None)):
            K["tryb_wybrany"] = j["tryb_wybrany"] or ""
            K.pop("tryb_wybor_decyzja", None)
        if j.get("tryb_wybor_decyzja") or j.get("tryb_decyzja"):  # różnica krytyczna: potwierdzenie tylko z pisemnym uzasadnieniem
            st_ = _kreator_stan(pid)
            r_ = st_.get("rozbieznosc_wyboru") if j.get("tryb_wybor_decyzja") else st_.get("rozbieznosc_trybu")
            if (r_ or {}).get("waga") == "krytyczna" and len(str(j.get("tryb_uzasadnienie") or K.get("tryb_uzasadnienie") or "").strip()) < 10:
                return jsonify({"blad": "To różnica krytyczna – potwierdzenie wymaga pisemnego uzasadnienia (np. podstawa wyłączenia stosowania ustawy). "
                                        "Wpisz uzasadnienie albo zmień wartość lub tryb."}), 400
        if "tryb_wybor_decyzja" in j and (j["tryb_wybor_decyzja"] in S.KZ.TRYBY_WYBOR or j["tryb_wybor_decyzja"] in ("", None)):
            K["tryb_wybor_decyzja"] = j["tryb_wybor_decyzja"] or ""
        if "tryb_decyzja" in j and (j["tryb_decyzja"] in S.KZ.NAZWY_TRYBU or j["tryb_decyzja"] in ("", None)):
            K["tryb_decyzja"] = j["tryb_decyzja"] or ""  # zamawiający świadomie potwierdził tryb z dokumentów mimo różnicy
        prop_w = _kreator_stan(pid) if isinstance(j.get("warunki"), dict) else None  # propozycja programu przed zapisem (wartość i tryb)
        for k in ("potrzeba", "warunki"):
            if isinstance(j.get(k), dict):
                for a, b in j[k].items():
                    pi = ((K.get("import") or {}).get("pola") or {}).get(f"{k}.{a}")
                    if pi and str(b or "") != str((K.get(k) or {}).get(a) or ""):
                        pi["do_aktualizacji"] = False  # zamawiający poprawił wartość
                        pi["zmienione"] = True
                nowe_ = {a: str(b or "")[:(KO.LIMIT_DLUGI if k == "potrzeba" else 2000)] for a, b in j[k].items()}
                if k == "warunki":  # zapisywane tylko pola różne od propozycji programu – niezmienione dalej podążają za wartością i trybem (Z-182)
                    Pw_, Kw_ = prop_w.get("warunki_propozycja") or {}, K.setdefault("warunki", {})
                    for a in [a for a, v in nowe_.items() if a in Pw_ and v.strip() == str(Pw_[a]).strip()
                              and not ((K.get("import") or {}).get("pola") or {}).get(f"warunki.{a}")]:
                        nowe_.pop(a)
                        Kw_.pop(a, None)
                    K["warunki_zapisane"] = True
                    K["warunki_tryb"] = prop_w.get("tryb")
                K.setdefault(k, {}).update(nowe_)
        if isinstance(j.get("krok"), int):
            K["krok"] = j["krok"]
        if j.get("nazwa") and str(j["nazwa"])[:90] != m.get("nazwa"):
            m["nazwa"] = str(j["nazwa"])[:90]
            K["nazwa_auto"] = False
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


def _zmien_rodzaj(K, m, nowy):
    """Zmiana rodzaju zamówienia: odpowiedzi ze „Szczegółów” dla poprzedniego rodzaju są odkładane (nie trafiają do dokumentów ani kosztorysu)
    i wracają, gdy zamawiający przywróci ten rodzaj; przenoszona jest tylko odpowiedź o terminie."""
    stary = K.get("rodzaj") or m.get("rodzaj_zamowienia") or "roboty"
    if nowy == stary:
        K["rodzaj"] = m["rodzaj_zamowienia"] = nowy
        return
    od = K.setdefault("potrzeba_odlozone", {})
    biez = dict(K.get("potrzeba") or {})
    if biez:
        od[stary] = biez
    nowe = dict(od.pop(nowy, {}) or {})
    for k in KO.WSPOLNE_POLA:
        if biez.get(k) and not nowe.get(k) and k in {p[0] for p in S.KZ.PYTANIA.get(nowy, [])}:
            nowe[k] = biez[k]
    K["potrzeba"] = nowe
    K["rodzaj"] = m["rodzaj_zamowienia"] = nowy


def _kz_ustaw(K, m, pole, wartosc):
    """Wpis pola kreatora o identyfikatorze „grupa.klucz” (co.*, potrzeba.*, warunki.*, wartosc)."""
    w = str(wartosc or "")[:3000]
    if pole == "wartosc":
        K["wartosc_reczna"] = re.sub(r"[^0-9,.]", "", w.replace(" ", "")).replace(",", ".")[:20]
    elif pole.startswith("co."):
        k_ = pole[3:]
        if k_ == "nazwa":
            m["nazwa"] = w[:90]
            K["nazwa_auto"] = False
        elif k_ == "rodzaj":
            if w in S.KZ.RODZAJE:
                _zmien_rodzaj(K, m, w)
        else:
            K[k_] = w
    elif pole.startswith("potrzeba."):
        K.setdefault("potrzeba", {})[pole[9:]] = str(wartosc or "")[:KO.LIMIT_DLUGI]
    elif pole.startswith("warunki."):
        K.setdefault("warunki", {})[pole[8:]] = w


def _kz_wartosc(K, m, pole):
    if pole == "co.nazwa":
        return m.get("nazwa")
    if pole == "co.rodzaj":
        return K.get("rodzaj") or m.get("rodzaj_zamowienia")
    if pole.startswith("co."):
        return K.get(pole[3:])
    if pole.startswith("potrzeba."):
        return (K.get("potrzeba") or {}).get(pole[9:])
    if pole.startswith("warunki."):
        return (K.get("warunki") or {}).get(pole[8:])
    return None


def _kz_pusty(K, m, pole):
    if pole == "wartosc":
        return not _netto_zam(m)
    if pole == "co.nazwa":
        return not m.get("nazwa") or str(m.get("nazwa")).startswith("Nowe zamówienie") or bool(K.get("nazwa_auto")) \
            or m.get("nazwa") in ((K.get("opis") or "")[:90], (K.get("opis") or "")[:80])
    if pole.startswith("co."):
        return not K.get(pole[3:])
    if pole.startswith("potrzeba."):
        return not (K.get("potrzeba") or {}).get(pole[9:])
    if pole.startswith("warunki."):
        return not (K.get("warunki") or {}).get(pole[8:])
    return True


def praca_kreator_import(log, pid):
    """Główne założenia zamówienia z dokumentów zamawiającego → pola kreatora (ze źródłem); pytania tylko o brakujące."""
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    m = S.meta(pid)
    K = m.get("kreator") or {}
    kat = os.path.join(S.pdir(pid), "kreator_zrodla")
    pliki = [os.path.join(kat, f) for f in sorted(os.listdir(kat))] if os.path.isdir(kat) else []
    if not pliki:  # dokumenty wgrane wcześniej do projektu (np. ogłoszenie w kroku „Szczegóły”)
        pliki = [os.path.join(S.pdir(pid), "dokumenty", p["sciezka"]) for p in S.lista_plikow(pid) if p.get("uwzglednij", True)]
    if not pliki:
        raise ValueError("Wgraj dokumenty: listę potrzeb, ogłoszenie, SWZ, notatkę albo kosztorys.")
    rozpakowane = []  # załączniki z BZP często są w ZIP (formularz cenowy, przedmiar – ilości); wcześniej były pomijane po cichu
    for p in pliki:
        if S.MO.czy_archiwum(p) or S.MO.rozpoznaj_typ(p) in (".zip", ".7z"):
            try:
                wew = S.MO.rozpakuj_zip(p, os.path.join(S.pdir(pid), "kreator_rozpakowane", os.path.splitext(os.path.basename(p))[0]))
                log(f"Rozpakowano {os.path.basename(p)}: {len(wew)} plików.")
                rozpakowane += wew
            except Exception as e:
                rozpakowane.append(p)
                log(f"Nie udało się rozpakować {os.path.basename(p)}: {e}")
        else:
            rozpakowane.append(p)
    bloki, nieodczytane = [], []
    for p in rozpakowane:
        nazwa = os.path.relpath(p, S.pdir(pid)) if p.startswith(S.pdir(pid)) else os.path.basename(p)
        try:
            b, _, blad = S.MO.przygotuj_blok(p)
            if blad or not b:
                nieodczytane.append({"plik": os.path.basename(p), "powod": blad or "brak treści do odczytu"})
            bloki += b
        except Exception as e:
            nieodczytane.append({"plik": os.path.basename(p), "powod": str(e)[:160]})
    if nieodczytane:
        log(f"UWAGA – nie odczytano {len(nieodczytane)} plików: " + "; ".join(f"{x['plik']} ({x['powod'][:80]})" for x in nieodczytane[:8]))
    if not bloki:
        raise ValueError("Żaden z dokumentów nie dał się odczytać – " + "; ".join(x["powod"] for x in nieodczytane[:3]))
    # kontrola bez AI – tryb i wartość podane wprost w tekście dokumentów (do porównania z odczytem AI)
    tekst_dok = S.KZ.tekst_blokow(bloki)
    kontrola = {"tryb": S.KZ.tryb_z_tekstu(tekst_dok), "wartosci": S.KZ.wartosc_z_tekstu(tekst_dok)}
    if kontrola["tryb"]:
        log(f"Tryb wskazany w dokumentach: {kontrola['tryb']['opis']}.")
    log(f"AI odczytuje założenia zamówienia z {len(rozpakowane) - len(nieodczytane)} dokumentów…")
    txt, _ = S.MO.claude_stream(c, S.KZ.SYSTEM_PRZEGLAD.split(" Sprawdzasz")[0] + " Odczytujesz założenia zamówienia z dokumentów. Odpowiadasz WYŁĄCZNIE JSON-em.",
                              S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": S.KZ.polecenie_importu(K.get("rodzaj"))}],
                              max_tokens=12000, log=log)
    r = S.MO.wyciagnij_json(txt)
    if not isinstance(r, dict):
        raise RuntimeError("AI nie zwróciło założeń – spróbuj ponownie.")
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        imp = K.setdefault("import", {"pola": {}})
        if r.get("rodzaj") in S.KZ.RODZAJE and (K.get("rodzaj_z_importu") or not K.get("opis")):
            _zmien_rodzaj(K, m, r["rodzaj"])
        elif r.get("rodzaj") in S.KZ.RODZAJE and r["rodzaj"] != (K.get("rodzaj") or m.get("rodzaj_zamowienia")):
            imp.setdefault("sprzecznosci_kreator", []).append({"pole": "co.rodzaj", "warianty": [
                {"wartosc": K.get("rodzaj") or m.get("rodzaj_zamowienia"), "zrodlo": "wybrane w kreatorze"},
                {"wartosc": r["rodzaj"], "zrodlo": "z dokumentów: " + str(r.get("rodzaj_dokumentow") or "")[:150]}]})
        wpisane, pominiete = 0, 0
        for pole, v in (r.get("pola") or {}).items():
            if not isinstance(v, dict) or v.get("wartosc") in (None, ""):
                continue
            pole = str(pole)
            if not (pole in ("wartosc",) or re.match(r"^(co|potrzeba|warunki)\.[a-z_]+$", pole)) or pole == "co.rodzaj":
                continue
            akt = bool(v.get("do_aktualizacji")) or (bool(r.get("archiwalny")) and pole in S.KZ.DO_AKTUALIZACJI)
            if pole == "wartosc":  # wartość z dokumentów zapamiętana zawsze – porównanie z kosztorysem i podstawa trybu
                wd = S.MO_liczba(v["wartosc"])
                if wd:
                    K["wartosc_dok"], K["wartosc_dok_zrodlo"] = wd, str(v.get("zrodlo") or "")[:200]
                    K.pop("wartosc_decyzja", None)
            if not _kz_pusty(K, m, pole) and pole != "wartosc":
                obecna = _kz_wartosc(K, m, pole)
                if obecna and S.W.norm(str(obecna))[:200] != S.W.norm(str(v["wartosc"]))[:200]:
                    imp.setdefault("sprzecznosci_kreator", []).append({"pole": pole, "warianty": [
                        {"wartosc": str(obecna)[:1500], "zrodlo": "obecnie w kreatorze"}, {"wartosc": str(v["wartosc"])[:1500], "zrodlo": str(v.get("zrodlo") or "dokument")[:200]}]})
            if _kz_pusty(K, m, pole):
                _kz_ustaw(K, m, pole, v["wartosc"])
                imp["pola"][pole] = {"zrodlo": str(v.get("zrodlo") or "")[:200], "do_aktualizacji": akt, "wartosc": str(v["wartosc"])[:300]}
                wpisane += 1
            else:
                pominiete += 1  # pole już wypełnione przez zamawiającego – nie nadpisujemy
        # odczyt AI kontra kontrola bez AI – różnice do decyzji (dokument rozstrzyga, nie program)
        pola_ai = r.get("pola") or {}
        wd_ai = S.MO_liczba((pola_ai.get("wartosc") or {}).get("wartosc")) if isinstance(pola_ai.get("wartosc"), dict) else None
        for w_ in kontrola["wartosci"]:
            if wd_ai and abs(w_["wartosc"] - wd_ai) > max(1.0, 0.005 * wd_ai):
                imp.setdefault("sprzecznosci_kreator", []).append({"pole": "wartosc", "warianty": [
                    {"wartosc": str(wd_ai), "zrodlo": "odczyt AI: " + str((pola_ai.get("wartosc") or {}).get("zrodlo") or "")[:150]},
                    {"wartosc": f"{w_['wartosc']:.2f}" + (" (brutto)" if w_["netto"] is False else ""), "zrodlo": "kontrola tekstu: " + w_["cytat"][:150]}]})
                if K.get("wartosc_dok") == wd_ai:  # sprzeczność: do czasu wyboru żadna kwota nie jest wartością z dokumentów
                    K.pop("wartosc_dok", None)
                    K.pop("wartosc_dok_zrodlo", None)
                    if imp["pola"].pop("wartosc", None) and KO.kwota(K.get("wartosc_reczna")) == wd_ai:
                        K.pop("wartosc_reczna", None)
                        wpisane -= 1
            elif not wd_ai and not K.get("wartosc_dok") and w_["netto"] is not False:
                K["wartosc_dok"], K["wartosc_dok_zrodlo"] = w_["wartosc"], ("kontrola tekstu: " + w_["cytat"])[:200]
                K.pop("wartosc_decyzja", None)
        tr = kontrola["tryb"]
        tryb_ai = S.KZ.tryb_z_tekstu((pola_ai.get("co.tryb_dok") or {}).get("wartosc")) if isinstance(pola_ai.get("co.tryb_dok"), dict) else None
        if tr and tryb_ai and tr["kod"] != tryb_ai["kod"]:
            imp.setdefault("sprzecznosci_kreator", []).append({"pole": "co.tryb_dok", "warianty": [
                {"wartosc": str((pola_ai.get("co.tryb_dok") or {}).get("wartosc"))[:300], "zrodlo": "odczyt AI: " + str((pola_ai.get("co.tryb_dok") or {}).get("zrodlo") or "")[:120]},
                {"wartosc": tr["opis"], "zrodlo": "dosłownie w dokumencie: „…" + tr["cytat"][:150] + "…”"}]})
            if "co.tryb_dok" in imp["pola"]:  # wpisane przed chwilą przez AI – pole czeka na decyzję zamawiającego
                imp["pola"].pop("co.tryb_dok")
                K.pop("tryb_dok", None)
                wpisane -= 1
            tr = dict(tr, sporny=True)
        if tr:
            K["tryb_dok_kontrola"] = {k: tr[k] for k in ("kod", "opis", "cytat", "inne")}
            if not K.get("tryb_dok") and not tr.get("sporny"):
                K["tryb_dok"] = tr["opis"]
                imp["pola"]["co.tryb_dok"] = {"zrodlo": "kontrola tekstu: " + tr["cytat"][:150], "do_aktualizacji": False, "wartosc": tr["opis"]}
        imp["nieodczytane"] = nieodczytane[:30]
        imp["sprzecznosci"] = ([s_ for s_ in (r.get("sprzecznosci") or []) if isinstance(s_, dict) and s_.get("pole") and len(s_.get("warianty") or []) > 1]
                               + imp.pop("sprzecznosci_kreator", []))[:25]
        imp.update(archiwalny=bool(r.get("archiwalny")), rodzaj_dokumentow=str(r.get("rodzaj_dokumentow") or "")[:200], uwagi=[str(u)[:300] for u in r.get("uwagi") or []][:10],
                   pliki=[os.path.basename(p) for p in rozpakowane], data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        S.zapisz_meta(pid, m)
    dok = os.path.join(S.pdir(pid), "dokumenty")  # dokumenty także do kosztorysu inwestorskiego (ilości)
    os.makedirs(dok, exist_ok=True)
    for p in [x for x in rozpakowane if not any(n_["plik"] == os.path.basename(x) for n_ in nieodczytane)]:
        if not os.path.exists(os.path.join(dok, os.path.basename(p))):
            S.shutil.copy2(p, os.path.join(dok, os.path.basename(p)))
    log(f"Gotowe: uzupełniono {wpisane} pól" + (f", pominięto {pominiete} już wypełnionych" if pominiete else "")
        + (f", sprzeczności do wyjaśnienia: {len(imp['sprzecznosci'])}" if imp["sprzecznosci"] else "") + ".")
    return {"wpisane": wpisane, "sprzecznosci": len(imp["sprzecznosci"])}


def _ocena_zamowienia(m):
    """Ocena ofert powiązana z zamówieniem (osobny projekt utworzony z kreatora) albo – dla zgodności – zapisana w samym zamówieniu."""
    oid = (m.get("kreator") or {}).get("ocena_id")
    if oid and os.path.isfile(os.path.join(S.PROJ, oid, "projekt.json")):
        return S.ocena_dane(S.meta(oid))
    return m.get("ocena") or {}


@bp.post("/api/projekty/<pid>/kreator/ocena")
@S.wymaga_logowania
def kreator_ocena(pid):
    """Sprawdzenie złożonych ofert dla zamówienia z kreatora: powiązany projekt oceny z dokumentami zamówienia (tylko publikowanymi – bez
    dokumentów wewnętrznych), kryteriami, kwotą i podziałem na części z kreatora."""
    m = S.meta(pid)
    K = m.get("kreator") or {}
    st = _kreator_stan(pid)
    pub, _ = _komplet_plikow(pid, m, st)
    swz_k = _swz_z_kreatora(pid, m, st)
    oid = K.get("ocena_id") if K.get("ocena_id") and os.path.isfile(os.path.join(S.PROJ, K["ocena_id"], "projekt.json")) else None
    if oid:
        with S.BLOKADA:  # uzupełnienie brakujących danych (bez nadpisywania wpisanych lub odczytanych z SWZ)
            mo = S.meta(oid)
            O = mo.get("ocena") or {}
            swz = O.get("swz") or {}
            for k, v in swz_k.items():
                if swz.get(k) in (None, "", [], {}):
                    swz[k] = v
            for k in swz.get("kryteria") or []:  # ocena utworzona wcześniej: zakres punktowania (od–do) z kreatora, jeśli brak
                kk = next((x for x in swz_k.get("kryteria") or [] if x["nazwa"].lower() == str(k.get("nazwa") or "").lower()), None)
                if kk and kk.get("od") is not None and k.get("od") is None and k.get("typ") == kk.get("typ"):
                    k.update(od=kk["od"], do=kk["do"], opis=kk["opis"])
            O["swz"] = swz
            mo["ocena"] = O
            S.zapisz_meta(oid, mo)
    else:
        oid = uuid.uuid4().hex[:12]
        os.makedirs(os.path.join(S.PROJ, oid, "dokumenty"))
        cz = S.KZ.czesci_normalizuj(K.get("czesci"), _netto_zam(m))
        swz = dict(swz_k)
        if cz["podzial"] and len(cz["lista"]) >= 2:
            swz.update({"czesci": [{"nr": x["nr"], "nazwa": x["nazwa"]} for x in cz["lista"]], "limit_czesci_dla_wykonawcy": cz["max_udzielen"]})
        S.zapisz_meta(oid, {"id": oid, "nazwa": "Oferty – " + (m.get("nazwa") or "")[:80], "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          "typ": "ocena_ofert", "strona": "zamawiajacy", "wlasciciel": m.get("wlasciciel") or S.konto_biezace(), "dostep": list(m.get("dostep") or []),
                          "pominiete": [], "zamowienie_id": pid, "prywatny": bool(K.get("prywatny")),
                          "ocena": {"swz": dict(swz, prywatny=bool(K.get("prywatny"))), "oferty": [], "podsum": {}}})
        with S.BLOKADA:
            m = S.meta(pid)
            m.setdefault("kreator", {})["ocena_id"] = oid
            S.zapisz_meta(pid, m)
    cel_ = os.path.join(S.PROJ, oid, "dokumenty")
    os.makedirs(cel_, exist_ok=True)
    for p_ in pub:  # dokumenty zamówienia (także dodane po utworzeniu oceny)
        if p_.lower().endswith((".docx", ".pdf", ".xlsx")) and not os.path.exists(os.path.join(cel_, os.path.basename(p_))):
            S.shutil.copy2(p_, os.path.join(cel_, os.path.basename(p_)))
    return jsonify({"id": oid})


def kryteria_z_tekstu(t):
    """Kryteria z warunków kreatora – wspólna funkcja kreatora (ten sam wzór w SWZ i w ocenie ofert)."""
    return S.KZ.kryteria_z_tekstu(t)


def _stawka_vat(m, K):
    """Stawka VAT zamówienia jako ułamek (0,23 / 0,08 / 0,05 / 0) i czy jest ustalona: z kosztorysu zamówienia (oferta.vat, bez „VAT nieustalony”)
    albo z pola kreatora; inaczej 0,23 (nieustalona – do sprawdzenia przez zamawiającego)."""
    of = m.get("oferta") or {}
    for v, znana in ((of.get("vat"), not of.get("vat_nieustalony")), (K.get("vat"), True)):
        if v in (None, "") or isinstance(v, bool):
            continue
        try:
            x = float(str(v).replace(",", ".").rstrip("%").strip())
        except ValueError:
            continue
        x = x / 100 if x >= 1 else x
        if x in (0, 0.05, 0.08, 0.23) or any(abs(x - y) < 1e-9 for y in (0.05, 0.08, 0.23)):
            return round(x, 2), znana
    return 0.23, False


def _brutto_zam(m, K, netto):
    """Wartość zamówienia z VAT do pism listy kontrolnej (kwota na sfinansowanie, art. 222 ust. 4): netto × (1 + stawka VAT zamówienia) – ta sama
    stawka co w ocenie ofert (_stawka_vat, ZE-27). Stawka nieustalona – 23% i stawka_vat_znana=False (pismo i ekran: „sprawdź stawkę VAT”).
    Bez wartości netto – jak dotąd kwota brutto z kosztorysu (jeśli jest)."""
    vat, znana = _stawka_vat(m, K)
    if netto:
        return {"brutto": round(netto * (1 + vat), 2), "stawka_vat": vat, "stawka_vat_znana": znana}
    return {"brutto": float(S.NR._f((m.get("oferta") or {}).get("brutto")) or 0), "stawka_vat": vat, "stawka_vat_znana": True}


def _swz_z_kreatora(pid, m, st):
    """Dane do oceny ofert z kreatora: nazwa, znak, zamawiający, tryb, kryteria z warunków, kwota na sfinansowanie, wartość z VAT
    (wartość netto × (1 + stawka VAT zamówienia) – stawka z kosztorysu albo kreatora; nieustalona – 23% z adnotacją w ocenie)."""
    K = st["K"]
    vat, vat_znana = _stawka_vat(m, K)
    brutto = round(st["netto"] * (1 + vat), 2) if st["netto"] else None
    kw = S.NR._f(((K.get("elementy") or {}).get("kwota") or {}).get("dane", {}).get("kwota")) or brutto
    P = st.get("postepowanie") or {}
    swz = {"nazwa_zamowienia": m.get("nazwa") or "", "numer": K.get("znak") or "", "zamawiajacy": S.zamawiajacy_projektu(m), "tryb": st["tryb_opis"],
           "kryteria": kryteria_z_tekstu((st.get("warunki") or {}).get("kryteria")), "kwota_budzet_brutto": kw,
           "wartosc_zam_brutto": brutto, "termin_skladania": K.get("termin_ofert") or ""}
    if brutto:
        swz.update(stawka_vat=vat, stawka_vat_znana=vat_znana)
    if P:
        swz["unijne"] = bool(P.get("unijne"))
    return {k: v for k, v in swz.items() if v not in (None, "", [])} | ({"unijne": swz["unijne"]} if "unijne" in swz else {})


def _zwyciezcy_czesci(m):
    """Najkorzystniejsze oferty w poszczególnych częściach – z powiązanej oceny ofert (podpowiedź do umów)."""
    O = _ocena_zamowienia(m)
    wyn = {}
    for c in ((O.get("podsum") or {}).get("czesci") or []):
        o = next((x for x in O.get("oferty") or [] if x.get("id") == c.get("najkorzystniejsza")), None)
        if o:
            r = (o.get("czesci_wyniki") or {}).get(str(c.get("nr"))) or {}
            wyn[str(c.get("nr"))] = {"nazwa": o.get("nazwa") or "", "nip": o.get("nip") or "", "cena_brutto": r.get("cena_brutto"), "warunkowo": bool(c.get("warunkowo"))}
    return wyn


@bp.post("/api/projekty/<pid>/kreator/czesci/realizacja")
@S.wymaga_logowania
def kreator_czesci_realizacja(pid):
    """Zamówienie podzielone na części: osobna umowa i realizacja dla każdej części – powiązane zamówienia z danymi wykonawcy i umowy.
    Ponowne wywołanie aktualizuje istniejące realizacje części zamiast tworzyć nowe."""
    j = request.json or {}
    utworzone = []
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.get("kreator") or {}
        cz = S.KZ.czesci_normalizuj(K.get("czesci"), _netto_zam(m))
        if not cz["podzial"] or len(cz["lista"]) < 2:
            return jsonify({"blad": "Zamówienie nie jest podzielone na części."}), 400
        mapa = K.setdefault("czesci_realizacje", {})
        for x in [x for x in (j.get("czesci") or []) if isinstance(x, dict)]:
            nr = str(x.get("nr") or "")
            c = next((y for y in cz["lista"] if str(y["nr"]) == nr), None)
            if not c or not str(x.get("wykonawca_nazwa") or "").strip() or not str(x.get("cena_netto") or "").strip():
                continue  # część bez wybranego wykonawcy (np. unieważniona) – bez realizacji
            umowa = {k: str(x.get(k) or "")[:200] for k in ("wykonawca_nazwa", "wykonawca_nip", "wykonawca_adres", "cena_netto", "vat", "umowa_nr", "data_umowy", "termin")}
            K.setdefault("czesci_umowy", {})[nr] = umowa  # do ponownego wyświetlenia w kreatorze zamówienia głównego
            cid = mapa.get(nr)
            if cid and os.path.isfile(os.path.join(S.PROJ, cid, "projekt.json")):
                mc = S.meta(cid)
                mc.setdefault("kreator", {})["umowa"] = umowa
                S.zapisz_meta(cid, mc)
            else:
                cid = uuid.uuid4().hex[:12]
                os.makedirs(os.path.join(S.PROJ, cid, "dokumenty"), exist_ok=True)
                S.zapisz_meta(cid, {"id": cid, "nazwa": f"{m.get('nazwa') or 'Zamówienie'} – część {c['nr']}: {c['nazwa']}"[:120], "typ": "zamowienie",
                                  "strona": "zamawiajacy", "rodzaj_zamowienia": m.get("rodzaj_zamowienia") or K.get("rodzaj") or "roboty",
                                  "utworzono": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "wlasciciel": m.get("wlasciciel") or S.konto_biezace(),
                                  "dostep": list(m.get("dostep") or []), "pominiete": [], "rodzic": {"id": pid, "czesc": c["nr"]},
                                  "kreator": {"rodzaj": K.get("rodzaj") or "roboty", "opis": c["zakres"] or c["nazwa"], "sciezka": K.get("sciezka") or "nowe", "krok": 2,
                                              "potrzeba": {}, "warunki": {}, "prywatny": bool(K.get("prywatny")), "zamawiajacy": K.get("zamawiajacy") or "",
                                              "wartosc_decyzja": "dokumenty", "wartosc_dok": str(c["wartosc"] or ""), "umowa": umowa}})
                mapa[nr] = cid
            utworzone.append({"nr": c["nr"], "id": cid})
        S.zapisz_meta(pid, m)
    if not utworzone:
        return jsonify({"blad": "Wpisz wykonawcę i cenę netto co najmniej dla jednej części."}), 400
    return jsonify({"projekty": utworzone})


def praca_kreator_czesci(log, pid):
    """Propozycja podziału zamówienia na części (art. 91 Pzp) – do przyjęcia albo poprawienia w kreatorze."""
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    m = S.meta(pid)
    K = m.get("kreator") or {}
    netto = _netto_zam(m)
    if not (K.get("opis") or (K.get("potrzeba") or {})):
        raise ValueError("Opisz najpierw zamówienie (krok „Co zamawiasz” i „Szczegóły”) – bez tego nie da się zaproponować podziału.")
    log("AI analizuje przedmiot zamówienia i proponuje podział na części…")
    txt, _ = S.MO.claude_stream(c, S.KZ.SYSTEM_CZESCI, [{"type": "text", "text": S.KZ.polecenie_podzialu(K, m.get("nazwa") or "", netto, S.dzialy_kosztorysu(pid))}],
                              max_tokens=4000, log=log)
    w = S.MO.wyciagnij_json(txt)
    if not isinstance(w, dict):
        raise ValueError("Nie udało się odczytać propozycji podziału – spróbuj ponownie.")
    lista = [x for x in (w.get("lista") or []) if isinstance(x, dict) and x.get("nazwa")]
    prop = {"lista": S.KZ.czesci_normalizuj({"podzial": True, "lista": lista}, netto)["lista"], "zalecany": bool(w.get("podzial_zalecany")) and len(lista) >= 2,
            "uzasadnienie": str(w.get("uzasadnienie") or "")[:2000], "ryzyka": [str(r)[:300] for r in (w.get("ryzyka") or []) if r][:8],
            "powody_braku": str(w.get("powody_braku_podzialu") or "")[:2000], "data": dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
    with S.BLOKADA:
        m = S.meta(pid)
        m.setdefault("kreator", {})["czesci_propozycja"] = prop
        S.zapisz_meta(pid, m)
    log(f"Gotowe: {'zalecany podział na ' + str(len(prop['lista'])) + ' części' if prop['zalecany'] else 'podział niezalecany – powody w kreatorze'}.")


@bp.post("/api/projekty/<pid>/kreator/czesci/propozycja")
@S.wymaga_logowania
def kreator_czesci_propozycja(pid):
    return jsonify(S.uruchom("zamawiajacy", "Propozycja podziału zamówienia na części", praca_kreator_czesci, pid))


@bp.post("/api/projekty/<pid>/kreator/zrodla")
@S.wymaga_logowania
def kreator_zrodla(pid):
    S.meta(pid)
    kat = os.path.join(S.pdir(pid), "kreator_zrodla")
    os.makedirs(kat, exist_ok=True)
    wszystkie = request.files.getlist("pliki")
    pominiete = [f.filename for f in wszystkie[KO.LIMIT_PLIKOW:]]
    for f in wszystkie[:KO.LIMIT_PLIKOW]:
        f.save(os.path.join(kat, S.secure_filename_pl(f.filename or "dokument.pdf")))
    if request.form.get("rodzaj_z_importu") == "1":
        with S.BLOKADA:
            m = S.meta(pid)
            m.setdefault("kreator", {})["rodzaj_z_importu"] = True
            S.zapisz_meta(pid, m)
    z = S.uruchom("zamawiajacy", "Uzupełnianie kreatora z dokumentów", praca_kreator_import, pid)
    return jsonify(dict(z, pominiete=pominiete) if pominiete else z)


@bp.post("/api/projekty/<pid>/kreator/umowa")
@S.wymaga_logowania
def kreator_umowa(pid):
    """Po wyborze oferty: wykonawca, cena oferty, VAT, umowa i termin – przenoszone do realizacji umowy.
    Cena netto, stawka VAT (0/5/8/23) i daty (RRRR-MM-DD) sprawdzane przed zapisem – błędne dane: 400, nic nie jest zapisywane."""
    j = request.get_json(silent=True)
    if not isinstance(j, dict):
        return jsonify({"blad": "Nieprawidłowe dane umowy – oczekiwano pól umowy."}), 400
    bl = PZ.umowa_bledy({k: (v if isinstance(v, (str, int, float)) else "") for k, v in j.items()})
    if bl:
        return jsonify({"blad": " ".join(bl)}), 400
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        K["umowa"] = {k: str(j.get(k) or "")[:200] for k in ("wykonawca_nazwa", "wykonawca_nip", "wykonawca_adres", "cena_netto", "vat", "umowa_nr", "data_umowy", "termin", "ocena_id")}
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/zrodla/ponownie")
@S.wymaga_logowania
def kreator_zrodla_ponownie(pid):
    """Ponowny odczyt dokumentów już wgranych (wartość z dokumentów, różnice z danymi w kreatorze)."""
    S.meta(pid)
    return jsonify(S.uruchom("zamawiajacy", "Ponowny odczyt dokumentów zamówienia", praca_kreator_import, pid))


@bp.post("/api/projekty/<pid>/kreator/sprzecznosc")
@S.wymaga_logowania
def kreator_sprzecznosc(pid):
    """Wybór wartości przy sprzeczności między dokumentami."""
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        imp = K.setdefault("import", {"pola": {}})
        s_ = next((x for x in imp.get("sprzecznosci") or [] if x.get("pole") == j.get("pole")), None)
        if not s_:
            return jsonify({"blad": "Nie ma takiej sprzeczności."}), 404
        war = next((v for v in s_["warianty"] if str(v.get("wartosc")) == str(j.get("wartosc"))), None) or {"wartosc": j.get("wartosc"), "zrodlo": "wybór zamawiającego"}
        _kz_ustaw(K, m, s_["pole"], war["wartosc"])
        if s_["pole"] == "wartosc":
            wd_ = KO.kwota(str(war["wartosc"]).replace(" (brutto)", ""))
            if wd_:
                K["wartosc_dok"], K["wartosc_dok_zrodlo"] = wd_, str(war.get("zrodlo") or "wybór zamawiającego")[:200]
        if s_["pole"] == "co.tryb_dok":  # wybrany tryb zastępuje wynik kontroli tekstu
            t_ = S.KZ.tryb_z_tekstu(war["wartosc"])
            if t_:
                K["tryb_dok_kontrola"] = {k: t_[k] for k in ("kod", "opis", "cytat", "inne")}
            else:
                K.pop("tryb_dok_kontrola", None)
        imp["pola"][s_["pole"]] = {"zrodlo": f"wybrane przez zamawiającego spośród: {war.get('zrodlo') or ''}"[:200], "do_aktualizacji": False, "wartosc": str(war["wartosc"])[:300]}
        imp["sprzecznosci"] = [x for x in imp["sprzecznosci"] if x is not s_]
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/wzory")
@S.wymaga_logowania
def kreator_wzory(pid):
    """Wgranie wzorów zamawiającego do zamówienia (opcjonalnie także do biblioteki „Moje wzory”)."""
    m = S.meta(pid)
    wz = os.path.join(S.pdir(pid), "wzory")
    os.makedirs(wz, exist_ok=True)
    do_bibl = request.form.get("biblioteka") == "1"
    wszystkie = request.files.getlist("pliki")
    pominiete = [f.filename for f in wszystkie[KO.LIMIT_PLIKOW:]]
    z_prop = {x.get("plik") for x in (m.get("kreator") or {}).get("propozycje") or []}
    kolizje = [S.secure_filename_pl(f.filename or "") for f in wszystkie[:KO.LIMIT_PLIKOW] if S.secure_filename_pl(f.filename or "") in z_prop]
    if kolizje and request.form.get("zastap") != "1":
        return jsonify({"zastap": kolizje, "blad": "Do tych wzorów są już propozycje zmian: " + ", ".join(kolizje) + ". Wgranie nowej wersji je zastąpi."}), 409
    bez_auto = []
    for f in wszystkie[:KO.LIMIT_PLIKOW]:
        nazwa = S.secure_filename_pl(f.filename or "wzor.docx")
        if nazwa.lower().endswith((".doc", ".odt")):
            bez_auto.append(nazwa)
        f.save(os.path.join(wz, nazwa))
        if do_bibl:
            S.shutil.copy2(os.path.join(wz, nazwa), os.path.join(S._kat_wzorow((m.get("kreator") or {}).get("rodzaj") or "ogolne"), nazwa))
    konw = S._konwertuj_pdf_wzorow(pid)
    return jsonify(dict(_kreator_stan(pid), konwersja=konw, pominiete=pominiete, bez_auto=bez_auto))


@bp.post("/api/projekty/<pid>/kreator/wzory/usun")
@S.wymaga_logowania
def kreator_wzory_usun(pid):
    """Usunięcie wzoru z zamówienia razem z tym, co z niego powstało: wersja Word z PDF, dokumenty po zmianach, propozycje zmian."""
    S.meta(pid)
    nazwa = os.path.basename(str((request.json or {}).get("nazwa") or ""))
    p = os.path.join(S.pdir(pid), "wzory", nazwa)
    baza = re.sub(r" \(z PDF\)$", "", os.path.splitext(nazwa)[0])
    usuniete = {nazwa}
    if os.path.isfile(p):
        os.remove(p)
        wersja_word = os.path.join(S.pdir(pid), "wzory", baza + " (z PDF).docx")  # usunięcie PDF usuwa też jego wersję Word
        if p.lower().endswith(".pdf") and os.path.isfile(wersja_word):
            os.remove(wersja_word)
            usuniete.add(os.path.basename(wersja_word))
    kon = os.path.join(S.pdir(pid), "dokumenty_koncowe")
    wz_ = os.path.join(S.pdir(pid), "wzory")
    pozostale = {os.path.splitext(f)[0] for f in (os.listdir(wz_) if os.path.isdir(wz_) else []) if not f.lower().endswith(".pdf")}  # PDF – zmiany w jego wersji Word
    bazy = {os.path.splitext(f)[0] for f in usuniete}  # nazwy bazowe usuniętych plików; „SWZ.pdf” nie zabiera dokumentów innego wzoru „SWZ.docx” (Z-202)
    if os.path.isdir(kon):
        for f in os.listdir(kon):
            wl = [b for b in bazy | pozostale if os.path.splitext(f)[0] == b or f.startswith(b + "_")]  # właściciel: najdłuższa pasująca nazwa wzoru
            if wl and max(wl, key=len) in bazy and max(wl, key=len) not in pozostale:
                os.remove(os.path.join(kon, f))
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.get("kreator") or {}
        if K.get("propozycje"):
            K["propozycje"] = [x for x in K["propozycje"] if x.get("plik") not in usuniete]
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/wzory/z-biblioteki")
@S.wymaga_logowania
def kreator_wzor_z_biblioteki(pid):
    """Dodanie wybranego wzoru z biblioteki „Moje wzory” do tego zamówienia."""
    j = request.json or {}
    rodz = j.get("rodzaj") if j.get("rodzaj") in list(S.KZ.RODZAJE) + ["ogolne"] else "ogolne"
    zr = os.path.join(S._kat_wzorow(rodz), os.path.basename(str(j.get("nazwa") or "")))
    if not os.path.isfile(zr):
        return jsonify({"blad": "Nie ma takiego wzoru w bibliotece."}), 404
    wz = os.path.join(S.pdir(pid), "wzory")
    os.makedirs(wz, exist_ok=True)
    S.shutil.copy2(zr, os.path.join(wz, os.path.basename(zr)))
    S._konwertuj_pdf_wzorow(pid)
    return jsonify(_kreator_stan(pid))


def _dane_zam_do_dok(m):
    """NIP, REGON, kontakt, strona, rachunek i godziny pracy z „Danych zamawiającego” – do dokumentów, gdy dane konta dotyczą tego
    zamawiającego: edycja urzędu albo nazwa z kreatora zgodna z nazwą w Danych zamawiającego (profil może należeć do osoby przygotowującej
    zamówienie dla innego zamawiającego – wtedy nic nie jest wstawiane)."""
    if m.get("dla_prawnika"):  # wspólnota / spółdzielnia też – gdy profil to ona sama (nazwa zgodna); zarządca przygotowujący dla wspólnoty – nic
        return ""
    pryw = bool((m.get("kreator") or {}).get("prywatny"))
    c, d = S.cfg(), S.dane_firmy()
    naz = re.sub(r"\W+", " ", str(c.get("firma_nazwa") or "")).strip().lower()
    zam = re.sub(r"\W+", " ", str((m.get("kreator") or {}).get("zamawiajacy") or "")).strip().lower()
    zgodna = bool(zam) and (naz in zam or set(naz.split()) <= set(zam.split()))  # cała nazwa z profilu w nazwie zamawiającego (nie sam początek)
    if not naz or not (S.EDYCJA == "zamawiajacy" or zgodna):
        return ""
    el = [("NIP", c.get("firma_nip")), ("REGON", c.get("firma_regon")), ("adres", c.get("firma_adres")), ("e-mail", c.get("firma_email")),
          ("telefon", c.get("firma_tel")), ("strona internetowa" if pryw else "strona internetowa / BIP", d.get("www")),
          ("rachunek bankowy" if pryw else "rachunek bankowy (wadium)", d.get("rachunek")),
          ("godziny pracy", d.get("godziny"))]
    return "; ".join(f"{k}: {str(v).strip()}" for k, v in el if str(v or "").strip())


@bp.post("/api/projekty/<pid>/kreator/dokumenty")
@S.wymaga_logowania
def kreator_dokumenty(pid):
    """Ścieżka „od początku”: komplet dokumentów z odpowiedzi kreatora (istniejący generator dokumentacji) + formularz cenowy pusty."""
    j = request.json or {}
    st = _kreator_stan(pid)
    rodzaje = [r for r in j.get("dokumenty") or [k for k, _ in st["komplet"]] if r in S.ZAM.DOKUMENTY]  # bez wskazania: komplet dla trybu
    if st["blokada_dokumentow"] and set(rodzaje) != {"oswiadczenia"}:
        return jsonify({"blad": "Nie można jeszcze przygotować dokumentów. Brakuje: " + "; ".join(st["blokada_dokumentow"]) + "."}), 400
    tw_ = st["K"].get("tryb_wybrany")
    baza_ = S.KZ.TRYBY_WYBOR[tw_][1] if (tw_ in S.KZ.TRYBY_WYBOR and not st.get("prywatny")) else None
    kod_ = "prywatny" if st.get("prywatny") else ("pzp_inny" if baza_ == "pzp_inny" else baza_ or st["tryb"])  # reżim dokumentów po KODZIE trybu
    pola = S.KZ.pola_dokumentacji(dict(st["K"], warunki=st["warunki"]), st["projekt"]["nazwa"], st["netto"], kod_)
    if st.get("tryb_wybrany"):
        pola["tryb_nazwa"] = st["tryb_opis"]  # nazwa wybranego trybu wprost w dokumentach (np. „Przetarg ograniczony”) – tylko opis, nie reżim
    if not st.get("prywatny"):  # JEDZ i procedura unijna – z wartości zamówienia (art. 125 ust. 2, art. 266 Pzp)
        pola["unijny"] = "tak" if st.get("tryb_z_wartosci") == "pzp_nieograniczony" else "nie"
    fin = _fin_kreatora(pid, st["K"])
    if fin["tekst"]:  # kredyt / premia BGK / KPO / dotacja: wymagania instytucji do zapytania, umowy i harmonogramu
        pola["finansowanie"] = fin["tekst"]
    dz = _dane_zam_do_dok(S.meta(pid))
    if dz:
        pola["dane_zamawiajacego"] = dz
    pola = {k: S.ZAM.czysc(v)[:(6000 if k == "finansowanie" else 3000)] for k, v in pola.items()}

    def praca(log):
        with S.BLOKADA:
            m = S.meta(pid)
            m["dokumentacja_pola"] = pola
            S.zapisz_meta(pid, m)
        if fin["liczba"]:
            log(f"Finansowanie ({fin['opis']}) – wymagania instytucji trafią do zapytania, wzoru umowy i harmonogramu.")
        w = S.praca_dokumentacja(log, pid, pola, rodzaje)
        if j.get("formularz") and st["rodzaj"] != "roboty":
            dane = S.czytaj(os.path.join(S.pdir(pid), "oferta_dane_oryginal.json"), None) or S.czytaj(os.path.join(S.pdir(pid), "oferta_dane.json"), None)
            if dane and dane.get("dzialy"):
                n = S.zapisz_kosztorys_pusty(pid, dane)
                log(f"Gotowe: {n} – formularz cenowy dla wykonawców.")
        with S.BLOKADA:
            m = S.meta(pid)
            m.setdefault("kreator", {})["krok"] = max(int((m.get("kreator") or {}).get("krok") or 0), 6)
            if set(rodzaje) & GLOWNE_DOK:  # samo przygotowanie oświadczeń nie oznacza, że dokumenty uwzględniają finansowanie
                m["kreator"]["dok_fin_nr"] = fin["nr"]  # dokumenty uwzględniają finansowanie w tej wersji (licznik zmian)
            S.zapisz_meta(pid, m)
        return w
    return jsonify(S.uruchom("dokumentacja", "Komplet dokumentów zamówienia", praca))


def praca_kreator_przeglad(log, pid, dodatkowe, model="standardowy"):
    """Sprawdzenie dokumentów: każdy dokument osobno (krótsza odpowiedź AI – pewniejszy wynik), równolegle po 2, z limitem długości
    odpowiedzi i czasu na dokument – całość w kilka minut zamiast kilkudziesięciu."""
    import concurrent.futures as _cf
    c = S.cfg()
    S.wymagany_klucz(c)
    klucz_m, dom_m, limit_tok, max_prop = S.MODELE_PRZEGLADU.get(model, S.MODELE_PRZEGLADU["standardowy"])
    c = dict(c, _model=c.get(klucz_m) or dom_m)
    log(f"Model: {model} ({c['_model']}), do {max_prop} propozycji na dokument.")
    st = _kreator_stan(pid)
    if st["sciezka"] == "wzory":
        S._konwertuj_pdf_wzorow(pid, log)
    pliki = S._pliki_do_przegladu(pid, st)
    if not pliki:
        raise ValueError("Brak dokumentów do sprawdzenia – wgraj wzory albo przygotuj komplet dokumentów.")
    import docx as _docx
    props, podsum, pominiete = [], [], []
    fin = _fin_kreatora(pid, st["K"])
    if fin["tekst"]:  # zgodność dokumentów z umową finansowania (termin, transze, wymagania wobec umowy z wykonawcą)
        log(f"Sprawdzenie obejmuje wymagania finansowania: {fin['opis']}.")
        dodatkowe = ((dodatkowe + " ") if dodatkowe else "") + ("ZGODNOŚĆ Z UMOWĄ FINANSOWANIA – sprawdź, czy dokumenty uwzględniają (brak albo "
                    "sprzeczność = propozycja zmiany): " + fin["tekst"])[:5000]
    # ta sama lista co krok 7 (i prawnik / weryfikacja dokumentacji) – według trybu; wspólnota: lista bez Pzp
    lista = LK.lista_kreatora(st["elementy"], S.KZ.grupa_trybu(st["tryb"], st["K"].get("tryb_wybrany")), st.get("prywatny"), st["rodzaj"], st["tryb_opis"])
    polec0 = S.KZ.polecenie_przegladu(dict(st["K"], warunki=st["warunki"]), st["projekt"]["nazwa"], st["netto"], st["tryb_opis"], dodatkowe,
                                      max_prop=max_prop, lista=lista)
    ust_ = S.ZAM.PARAMETRY_USTAWOWE.get(st["tryb"]) if not st.get("prywatny") else ""
    if ust_:  # te same limity co przy pisaniu dokumentów – propozycja sprzeczna z nimi wprowadziłaby błąd do kompletu
        polec0 += ("\n\nPARAMETRY USTAWOWE TRYBU (obowiązują – nie proponuj zmian z nimi sprzecznych; zapis z nimi sprzeczny popraw na zgodny):\n" + ust_)
    if st["K"].get("termin_ofert"):
        polec0 += (f"\nTermin składania ofert ({st['K']['termin_ofert']}, godz. {st['K'].get('godzina_ofert') or '—'}) ustalił zamawiający w programie – "
                   "nie proponuj jego zmiany; jeśli budzi wątpliwości (np. dzień wolny od pracy), napisz o tym w podsumowaniu.")
    zadania = []
    for p in pliki:
        nazwa = os.path.basename(p)
        try:
            bloki, _, _ = S.MO.przygotuj_blok(p)
        except Exception:
            bloki = []
        if not bloki:
            pominiete.append(f"{nazwa} (brak tekstu do odczytu)")
            log(f"Nie udało się odczytać: {nazwa} – pomijam.")
            continue
        zadania.append((p, nazwa, bloki))
    SPRZ = "__sprzecznosci__"  # drugie spojrzenie: sprzeczności MIĘDZY dokumentami – każdy dokument osobno tego nie wykryje
    sprz = len(zadania) >= 2
    if sprz:
        log("Dodatkowo: sprawdzenie sprzeczności między dokumentami (całość razem).")
    log(f"Sprawdzam {len(zadania)} dokumentów (po 2 jednocześnie, do {max(1, S.LIMIT_CZASU_DOK // 60)} min na dokument)…")

    def jeden(p, nazwa, bloki):
        polec = polec0 + (f"\n\nSprawdzasz TERAZ dokument „{nazwa}” (pole \"dokument\" = „{nazwa}”). Maksymalnie {max_prop} NAJWAŻNIEJSZYCH propozycji dla tego dokumentu "
                          "(drobne błędy redakcyjne pomiń). Zwięźle: cytat do 300 znaków, nowe brzmienie tylko dla zmienianego fragmentu (do 800 znaków), "
                          "uzasadnienie do 300 znaków. Odpowiedź zacznij od znaku {.")
        tresc = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polec}]
        return S._json_ai_z_ponowieniem(c, S.KZ.SYSTEM_PRZEGLAD + RZ.reguly(S.projekt_wspolnoty(S.meta(pid))).kontekst_ai, tresc, log, limit_tok, nazwa,
                                      max_kontynuacji=0)  # bez dopisywania – ucięta odpowiedź jest odzyskiwana

    wyniki, start = {}, {}

    def sprzecznosci():
        nazwy, tresc = [n for _p, n, _b in zadania], []
        for _p, n, b in zadania:
            tresc += [{"type": "text", "text": f"[DOKUMENT: {n}]"}] + list(b)
        polec = S.KZ.polecenie_sprzecznosci(nazwy, dodatkowe, max_prop=max_prop)
        return S._json_ai_z_ponowieniem(c, S.KZ.SYSTEM_PRZEGLAD + RZ.reguly(S.projekt_wspolnoty(S.meta(pid))).kontekst_ai,
                                        S.MO.oznacz_dokumenty(tresc, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": polec}], log, limit_tok,
                                        "sprzeczności między dokumentami", max_kontynuacji=0)

    def z_czasem(p, nazwa, bloki):
        start[p] = S.time.time()
        return sprzecznosci() if p == SPRZ else jeden(p, nazwa, bloki)
    ex = _cf.ThreadPoolExecutor(max_workers=2)
    fut = {ex.submit(S._z_kontekstem(z_czasem), p, nazwa, bloki): (p, nazwa) for p, nazwa, bloki in zadania + ([(SPRZ, "sprzeczności między dokumentami", None)] if sprz else [])}
    ile_zad = len(fut)
    otwarte, gotowe = set(fut), 0
    try:
        while otwarte:
            zrobione, otwarte = _cf.wait(otwarte, timeout=5, return_when=_cf.FIRST_COMPLETED)
            for f in zrobione:
                p, nazwa = fut[f]
                gotowe += 1
                try:
                    wyniki[p] = f.result()
                    log(f"[{gotowe}/{ile_zad}] sprawdzono: {nazwa}")
                except Exception as e:
                    powod = S.opis_bledu_zadania(e, "zamawiajacy")
                    pominiete.append(f"{nazwa} ({powod[:160]})")
                    log(f"[{gotowe}/{ile_zad}] {nazwa}: nie udało się uzyskać propozycji ({powod}).")
            for f in list(otwarte):  # jeden dokument nie blokuje całości – po limicie czasu pomijamy go
                p, nazwa = fut[f]
                if p in start and S.time.time() - start[p] > S.LIMIT_CZASU_DOK * (2 if p == SPRZ else 1):  # całość razem – dłużej
                    otwarte.discard(f)
                    gotowe += 1
                    pominiete.append(f"{nazwa} (przekroczono czas {S.LIMIT_CZASU_DOK // 60} min – sprawdź ten dokument osobno)")
                    log(f"[{gotowe}/{ile_zad}] {nazwa}: przekroczono czas – pomijam.")
    finally:
        ex.shutdown(wait=False, cancel_futures=True)
    for p, nazwa, _b in zadania:
        r = wyniki.get(p)
        if not isinstance(r, dict):
            continue
        if r.get("podsumowanie"):
            podsum.append(f"{nazwa}: {str(r['podsumowanie'])[:400]}")
        dok = None
        if p.lower().endswith(".docx"):
            try:
                dok = _docx.Document(p)
            except Exception:
                dok = None
        for x in [y for y in r.get("propozycje") or [] if isinstance(y, dict)][:max_prop]:
            pr = {"id": f"p{len(props) + 1}", "typ": "zmiana", **{k: str(x.get(k) or "")[:3000] for k in ("cytat", "nowy", "uzasadnienie", "podstawa", "waga")}}
            pr.update(dokument=nazwa, plik=nazwa, odnaleziony=bool(dok is not None and S.KZ._znajdz(dok, pr["cytat"])[0] is not None))
            props.append(pr)
        for x in [y for y in r.get("dopisac") or [] if isinstance(y, dict)][:6]:
            pr = {"id": f"d{len(props) + 1}", "typ": "dopisanie", "cytat": str(x.get("po_cytacie") or "")[:1000], "waga": "istotna",
                  **{k: str(x.get(k) or "")[:3000] for k in ("nowy", "uzasadnienie", "podstawa")}}
            pr.update(dokument=nazwa, plik=nazwa, odnaleziony=bool(dok is not None and S.KZ._znajdz(dok, pr["cytat"])[0] is not None))
            props.append(pr)
    r = wyniki.get(SPRZ)
    if isinstance(r, dict):
        po_nazwie = {n: p for p, n, _b in zadania}
        po_nazwie_m = {n.lower(): n for n in po_nazwie}
        dok_ = {}
        n_sprz = 0
        for x in [y for y in r.get("propozycje") or [] if isinstance(y, dict)][:max_prop]:
            d_ = str(x.get("dokument") or "").strip()
            nazwa = d_ if d_ in po_nazwie else po_nazwie_m.get(d_.lower()) or next((n for n in po_nazwie if d_ and (d_.lower() in n.lower() or os.path.splitext(n)[0].lower() in d_.lower())), None)
            if not nazwa:
                continue
            pr = {"id": f"s{len(props) + 1}", "typ": "zmiana", "sprzecznosc": True, **{k: str(x.get(k) or "")[:3000] for k in ("cytat", "nowy", "uzasadnienie", "podstawa", "waga")}}
            if any(q.get("plik") == nazwa and S.KZ._norm(q.get("cytat")) == S.KZ._norm(pr["cytat"]) for q in props):
                continue  # ta sama uwaga już jest z przeglądu dokumentu
            sc = po_nazwie[nazwa]
            if nazwa not in dok_:
                try:
                    dok_[nazwa] = _docx.Document(sc) if sc.lower().endswith(".docx") else None
                except Exception:
                    dok_[nazwa] = None
            pr.update(dokument=nazwa, plik=nazwa, odnaleziony=bool(dok_[nazwa] is not None and S.KZ._znajdz(dok_[nazwa], pr["cytat"])[0] is not None))
            props.append(pr)
            n_sprz += 1
        if r.get("podsumowanie"):
            podsum.append(f"Spójność dokumentów: {str(r['podsumowanie'])[:400]}")
        log(f"Sprzeczności między dokumentami: {n_sprz}.")
    if not st.get("prywatny"):  # propozycja sprzeczna z parametrami ustawowymi: ostrzeżenie programu, decyzja wymagana, domyślnie do odrzucenia
        for pr in props:
            kol = KO.kolizje_z_przepisami(pr.get("nowy"), st["tryb"])
            if kol:
                pr.update(waga="krytyczna", kolizja="; ".join(kol),
                          uzasadnienie=("UWAGA PROGRAMU – propozycja sprzeczna z przepisami: " + "; ".join(kol) + ". Zalecane: odrzuć. | " + pr.get("uzasadnienie", ""))[:3000])
        if any(pr.get("kolizja") for pr in props):
            log(f"Propozycje sprzeczne z parametrami ustawowymi: {sum(1 for pr in props if pr.get('kolizja'))} – oznaczone do odrzucenia.")
    if not props and pominiete:
        raise ValueError("Nie udało się sprawdzić dokumentów: " + "; ".join(pominiete) + ". Szczegóły w dzienniku zadania – spróbuj ponownie "
                         "albo wgraj wersję Word (.docx).")
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        K["przeglad_nr"] = int(K.get("przeglad_nr") or 0) + 1  # krok 6 zakończony dopiero po zatwierdzeniu TEGO sprawdzenia
        if fin["liczba"] and st["sciezka"] == "wzory":  # własne wzory: finansowanie sprawdzone w tym przeglądzie
            K["dok_fin_nr"] = fin["nr"]
        K.update(propozycje=props, decyzje={}, przeglad_podsumowanie=" ".join(podsum)[:3000] + (f" Nie sprawdzono: {', '.join(pominiete)}." if pominiete else ""),
                 przeglad_data=dt.datetime.now().strftime("%Y-%m-%d %H:%M"), krok=max(int(K.get("krok") or 0), 7))
        S.zapisz_meta(pid, m)
    log(f"Gotowe: {len(props)} propozycji zmian ({sum(1 for x in props if x['odnaleziony'])} do wprowadzenia automatycznie).")
    return {"propozycje": len(props)}


@bp.post("/api/projekty/<pid>/kreator/przeglad")
@S.wymaga_logowania
def kreator_przeglad(pid):
    S.meta(pid)
    j = request.json or {}
    model = j.get("model") if j.get("model") in S.MODELE_PRZEGLADU else "standardowy"
    return jsonify(S.uruchom("weryfikacja", "Sprawdzenie dokumentów i propozycje zmian", praca_kreator_przeglad, pid, str(j.get("dodatkowe") or "")[:500], model))


@bp.post("/api/projekty/<pid>/kreator/decyzje")
@S.wymaga_logowania
def kreator_decyzje(pid):
    j = request.get_json(silent=True)
    if not isinstance(j, dict) or not isinstance(j.get("decyzje") or {}, dict):
        return jsonify({"blad": "Decyzje: nieprawidłowe dane – oczekiwano listy decyzji {identyfikator propozycji: {decyzja: tak / nie}}."}), 400
    with S.BLOKADA:
        m = S.meta(pid)
        dec = m.setdefault("kreator", {}).setdefault("decyzje", {})
        for k, v in (j.get("decyzje") or {}).items():
            if isinstance(v, dict) and v.get("decyzja") in ("tak", "nie", ""):
                dec[k] = {"decyzja": v["decyzja"], **({"nowy": str(v["nowy"])[:3000]} if v.get("nowy") is not None else {})}
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.get("/api/projekty/<pid>/kreator/uwagi.docx")
@S.wymaga_logowania
def kreator_uwagi_docx(pid):
    """Uwagi do sporządzonej dokumentacji (krok „Sprawdzenie i zmiany”) z decyzjami – Word do pobrania; zakres: wszystkie / przyjete / do_decyzji."""
    st = _kreator_stan(pid)
    if not st.get("propozycje"):
        return jsonify({"blad": "Brak uwag – najpierw uruchom „Sprawdź i zaproponuj zmiany (AI)”."}), 404
    zakres = request.args.get("zakres", "wszystkie")
    if zakres not in S.KZ.ZAKRESY_UWAG:
        zakres = "wszystkie"
    m = S.meta(pid)
    nazwa = (st.get("K") or {}).get("nazwa") or m.get("nazwa", "")
    dop = {"wszystkie": "", "przyjete": "_przyjete", "do_decyzji": "_do_decyzji"}[zakres]
    p = os.path.join(S.pdir(pid), f"Uwagi_do_dokumentacji{dop}_{S.MO.bezpieczna_nazwa(nazwa or 'zamowienie')[:50]}.docx")
    S.KZ.raport_uwag_docx(p, nazwa, st, zakres)
    return send_file(p, as_attachment=True, download_name=os.path.basename(p))


@bp.post("/api/projekty/<pid>/kreator/do-decyzji")
@S.wymaga_logowania
def kreator_do_decyzji(pid):
    """Sprawa do decyzji wskazana przy pisaniu dokumentów: oznaczenie jako rozstrzygnięta (albo cofnięcie)."""
    j = request.json or {}
    with S.BLOKADA:
        m = S.meta(pid)
        L = (m.get("dokumentacja") or {}).get("do_decyzji") or []
        try:
            L[int(j.get("nr"))]["ok"] = bool(j.get("ok", True))
        except (TypeError, ValueError, IndexError):
            return jsonify({"blad": "Nie ma takiej pozycji."}), 404
        S.zapisz_meta(pid, m)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/wprowadz")
@S.wymaga_logowania
def kreator_wprowadz(pid):
    """Zaakceptowane zmiany → dla każdego dokumentu Word: wersja ze śledzeniem zmian i wersja czysta (folder dokumentów końcowych)."""
    st = _kreator_stan(pid)
    d = S.pdir(pid)
    pliki = {os.path.basename(p): p for p in S._pliki_do_przegladu(pid, st)}
    przyjete = [p for p in st["propozycje"] if p["decyzja"] == "tak"]
    if st["bez_decyzji"]:
        return jsonify({"blad": f"Najpierw rozstrzygnij {st['bez_decyzji']} propozycji krytycznych i istotnych – każda wymaga decyzji „przyjmuję” albo „odrzucam”."}), 400
    kon = os.path.join(d, "dokumenty_koncowe")
    os.makedirs(kon, exist_ok=True)
    wynik, reczne = [], []
    for nazwa, sc in pliki.items():
        zm = [{"cytat" if p["typ"] == "zmiana" else "po_cytacie": p["cytat"], "nowy": p["nowy_edyt"] if p.get("nowy_edyt") is not None else p["nowy"], "id": p["id"]}
              for p in przyjete if p.get("plik") == nazwa]
        baza = os.path.splitext(nazwa)[0]
        for st_ in (nazwa, f"{baza}.docx", f"{baza}_ze_zmianami.docx", f"{baza}_czysty.docx"):  # ponowne zatwierdzenie – bez wersji z poprzedniego razu
            if os.path.isfile(os.path.join(kon, st_)):
                os.remove(os.path.join(kon, st_))
        if not nazwa.lower().endswith(".docx"):
            S.shutil.copy2(sc, os.path.join(kon, nazwa))
            reczne += [dict(p, powod="dokument nie jest w formacie Word (.docx)") for p in przyjete if p.get("plik") == nazwa]
            continue
        if not zm:
            S.shutil.copy2(sc, os.path.join(kon, f"{baza}.docx"))
            continue
        ok, brak = S.KZ.wprowadz_zmiany(sc, zm, os.path.join(kon, f"{baza}_ze_zmianami.docx"), sledz=True)
        S.KZ.wprowadz_zmiany(sc, zm, os.path.join(kon, f"{baza}_czysty.docx"), sledz=False)
        wynik.append({"plik": nazwa, "wprowadzone": len(ok), "nieodnalezione": len(brak)})
        reczne += [dict(next(p for p in przyjete if p["id"] == z["id"]), powod="nie odnaleziono fragmentu w dokumencie") for z in brak]
    reczne += [dict(p, powod="nie wskazano dokumentu Word") for p in przyjete if not p.get("plik")]
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        K["reczne"] = [{k: p.get(k) for k in ("id", "dokument", "cytat", "nowy", "uzasadnienie", "powod")} for p in reczne]
        K["reczne_potwierdzone"] = False
        K["wprowadzono"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        K["zatwierdzony_nr"] = K.get("przeglad_nr")
        K["krok"] = max(int(K.get("krok") or 0), 8)
        S.zapisz_meta(pid, m)
    return jsonify(dict(_kreator_stan(pid), wynik=wynik))


# pisma z listy kontrolnej: do publikacji (część dokumentów zamówienia) albo do akt postępowania (wewnętrzne)
PISMA_PUBLICZNE = {"rodo", "czesci"}


def _komplet_plikow(pid, m, st):
    """Pliki kompletu podzielone na: do publikacji (dla wykonawców) i do akt postępowania (notatka, kosztorys inwestorski, oświadczenia
    z art. 56, plan, dane do ogłoszenia, kwota na sfinansowanie – publikowana osobno przed otwarciem ofert)."""
    d = S.pdir(pid)
    pub = [os.path.join(d, "dokumenty_koncowe", f) for f in st["koncowe"] if not f.endswith("_ze_zmianami.docx")] or \
        [os.path.join(d, f) for f in st["dokumenty"]] + [os.path.join(d, "wzory", f) for f in st["wzory"]]
    akta = []
    publiczny = not (m.get("kreator") or {}).get("prywatny")
    if m.get("kosztorys_pusty") and os.path.isfile(os.path.join(d, m["kosztorys_pusty"])):  # formularz cenowy dla wykonawców
        pub.append(os.path.join(d, m["kosztorys_pusty"]))
    for x in ((None if publiczny else m.get("kosztorys")), m.get("notatka_szac")):  # publiczny: bez kosztorysu AI
        if x and os.path.isfile(os.path.join(d, x)):
            akta.append(os.path.join(d, x))
    ks_ = os.path.join(d, "szacowanie")  # kosztorys inwestorski / PFU i źródła cen – do akt, nie dla wykonawców
    if publiczny and os.path.isdir(ks_):
        akta += [os.path.join(ks_, f) for f in sorted(os.listdir(ks_))]
    kp = os.path.join(d, "dokumenty_postepowania")
    rodzaj_pliku = {S.KZ.PLIKI_PISM.get(e["id"], "") + ".docx": e["id"] for e in st["elementy"]}
    zastapione = {S.KZ.PLIKI_PISM.get(e["id"], "") + ".docx" for e in st["elementy"] if e.get("wlasny")}  # własny wzór zastępuje pismo programu
    if os.path.isdir(kp):
        for f in sorted(os.listdir(kp)):
            if f in zastapione:
                continue
            # pisma wewnętrzne programu (notatki, plan, art. 56, dane do ogłoszenia, kwota) – do akt; pozostałe pliki zamówienia – do publikacji
            (akta if f in rodzaj_pliku and rodzaj_pliku[f] not in PISMA_PUBLICZNE else pub).append(os.path.join(kp, f))
    for e in st["elementy"]:
        p_ = os.path.join(d, "wzory", e["wlasny"]) if e.get("wlasny") else None
        if p_ and os.path.isfile(p_) and p_ not in pub and p_ not in akta:
            (pub if e["id"] in PISMA_PUBLICZNE else akta).append(p_)
    return [p_ for p_ in pub if os.path.isfile(p_)], [p_ for p_ in akta if os.path.isfile(p_)]


@bp.get("/api/projekty/<pid>/kreator/zip")
@S.wymaga_logowania
def kreator_zip(pid):
    """Komplet: 1_do_publikacji (dokumenty zamówienia dla wykonawców) i 2_do_akt_postepowania (dokumenty wewnętrzne)."""
    import zipfile
    m = S.meta(pid)
    st = _kreator_stan(pid)
    d = S.pdir(pid)
    pub, akta = _komplet_plikow(pid, m, st)
    pryw = bool(st.get("prywatny"))
    P1, P2 = ("1_do_wyslania_wykonawcom", "2_do_dokumentacji_zamawiajacego") if pryw else ("1_do_publikacji", "2_do_akt_postepowania")
    sc = os.path.join(d, f"Komplet_zamowienia_{S.MO.bezpieczna_nazwa(m.get('nazwa') or 'zamowienie')[:50]}.zip")
    with zipfile.ZipFile(sc, "w", zipfile.ZIP_DEFLATED) as z:
        for kat, L in ((P1, pub), (P2, akta)):
            for p_ in L:
                z.write(p_, f"{kat}/{os.path.basename(p_)}")
        z.writestr(f"{P2}/Lista_kontrolna_przed_publikacja.txt", "\n".join(("[x] " if e["status"] == "ok" else "[–] " if e["status"] == "nd" else "[ ] ") + e["opis"]
                                                                          + (f" (nie dotyczy: {e['powod_nd']})" if e["status"] == "nd" and e.get("powod_nd") else "")
                                                                          for e in st["elementy"]) + f"\n\nTermin składania ofert: {st['min_dni_opis']}")
        uwagi = []
        if st.get("dokumenty_brak"):
            uwagi.append("UWAGA: brak dokumentów: " + ", ".join(st["dokumenty_brak"]) + " – przygotuj je w kroku „Komplet dokumentów”.")
        dd_ = (m.get("dokumentacja") or {}).get("do_decyzji") or []
        if dd_:  # sprawy do rozstrzygnięcia przez zamawiającego wskazane przy pisaniu dokumentów – zamiast próśb o potwierdzenie w treści
            z.writestr(f"{P2}/Do_decyzji_przed_publikacja.txt", "Sprawy do rozstrzygnięcia przed publikacją (wskazane przy przygotowaniu dokumentów):\n\n"
                       + "\n".join(f"[{'x' if x.get('ok') else ' '}] {x.get('dokument')}: {x.get('punkt')}" for x in dd_))
        G = st["gotowosc"]
        uwagi = (["STAN: GOTOWE DO " + ("WYSŁANIA" if pryw else "PUBLIKACJI") + "."] if G["gotowe"] else
                 ["STAN: NIEGOTOWE – przed " + ("wysłaniem" if pryw else "publikacją") + " uzupełnij:"] + ["  - " + b_ for b_ in G["braki"]]) + [""] + uwagi
        z.writestr("CZYTAJ.txt", "\n".join(uwagi + [
            f"{P1}: dokumenty zamówienia do " + ("wysłania wykonawcom." if pryw else "publikacji na stronie postępowania (platforma) razem z dokumentacją "
            "projektową, przedmiarem i specyfikacjami technicznymi (STWiORB) z kroku 1 – te pliki dołącz sam."),
            f"{P2}: dokumenty " + ("zamawiającego – nie wysyłaj ich wykonawcom." if pryw else "wewnętrzne – NIE publikuj ich z dokumentami zamówienia "
            "(notatka z szacowania, kosztorys inwestorski, oświadczenia z art. 56, pozycja planu, dane do formularza ogłoszenia). "
            "Informację o kwocie na sfinansowanie zamówienia publikuje się osobno, najpóźniej przed otwarciem ofert (art. 222 ust. 4 Pzp)."),
        ]))
    return send_file(sc, as_attachment=True, download_name=os.path.basename(sc))


# ---------------------------------------------------------------- po publikacji: kalendarz, pytania wykonawców, zmiana SWZ i terminu
def _postepowanie_zapis(pid, f):
    with S.BLOKADA:
        m = S.meta(pid)
        K = m.setdefault("kreator", {})
        P = K.setdefault("postepowanie", {})
        wynik = f(K, P)
        S.zapisz_meta(pid, m)
    return wynik


@bp.post("/api/projekty/<pid>/kreator/postepowanie")
@S.wymaga_logowania
def kreator_postepowanie(pid):
    """Daty postępowania: publikacja ogłoszenia, przesłanie zawiadomienia o wyborze (do kalendarza terminów)."""
    j = request.json or {}

    def f(K, P):
        for k in ("data_publikacji", "data_wyboru"):
            if k in j:
                P[k] = str(j[k] or "")[:10] if (not j[k] or PZ._d(j[k])) else P.get(k, "")
    _postepowanie_zapis(pid, f)
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/pytanie")
@S.wymaga_logowania
def kreator_pytanie(pid):
    """Pytanie wykonawcy o treść SWZ: dodanie, odpowiedź, zmiana SWZ, usunięcie."""
    j = request.json or {}

    def f(K, P):
        L = P.setdefault("pytania", [])
        q = next((x for x in L if x["id"] == j.get("id")), None)
        if j.get("usun"):
            if q:
                L.remove(q)
            return
        if not q:
            if not str(j.get("tresc") or "").strip():
                raise ValueError("Wpisz treść pytania.")
            q = {"id": PZ.nowe_id(j.get("tresc")), "data": dt.date.today().isoformat()}
            L.append(q)
        if "data" in j and PZ._d(j["data"]):
            if PZ._d(j["data"]) > dt.date.today():
                raise ValueError("Data wpływu pytania nie może być przyszła.")
            q["data"] = str(j["data"])[:10]
        if "odpowiedz" in j and "[DO DECYZJI" in str(j.get("odpowiedz") or "").upper():
            raise ValueError("Odpowiedź zawiera oznaczenie „[DO DECYZJI ZAMAWIAJĄCEGO…” – rozstrzygnij tę sprawę i usuń oznaczenie przed zatwierdzeniem.")
        if "odpowiedz" in j:
            q["zatwierdzona"] = bool(str(j.get("odpowiedz") or "").strip())  # zapis przez zamawiającego = zatwierdzenie (projekt AI nim nie jest)
        for k, n in (("tresc", 4000), ("odpowiedz", 6000), ("zmiana_opis", 3000)):
            if k in j:
                q[k] = str(j[k] or "")[:n]
        if "zmiana_swz" in j:
            q["zmiana_swz"] = bool(j["zmiana_swz"])
    try:
        _postepowanie_zapis(pid, f)
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    return jsonify(_kreator_stan(pid))


@bp.post("/api/projekty/<pid>/kreator/przedluz")
@S.wymaga_logowania
def kreator_przedluz(pid):
    """Przedłużenie terminu składania ofert (zmiana SWZ): nowy termin w kreatorze, historia zmian do pisma i kalendarza."""
    j = request.json or {}
    nowy = PZ._d(j.get("termin"))
    if not nowy:
        return jsonify({"blad": "Podaj nowy termin składania ofert."}), 400

    def f(K, P):
        stary = K.get("termin_ofert") or ""
        if PZ._d(stary) and nowy <= PZ._d(stary):
            raise ValueError("Nowy termin musi być późniejszy niż obecny.")
        P.setdefault("termin_pierwotny", stary)  # termin na wnioski o wyjaśnienie liczy się od terminu sprzed przedłużenia (art. 284 ust. 5 / art. 135 ust. 4)
        P.setdefault("zmiany_terminu", []).append({"stary": stary, "nowy": nowy.isoformat(), "powod": str(j.get("powod") or "")[:500],
                                                    "data": dt.date.today().isoformat()})
        K["termin_ofert"] = nowy.isoformat()
    try:
        _postepowanie_zapis(pid, f)
    except ValueError as e:
        return jsonify({"blad": str(e)}), 400
    return jsonify(_kreator_stan(pid))


@bp.get("/api/projekty/<pid>/kreator/wyjasnienia.docx")
@S.wymaga_logowania
def kreator_wyjasnienia(pid):
    st = _kreator_stan(pid)
    P = st["postepowanie"] or {}
    kat = os.path.join(S.pdir(pid), "dokumenty_postepowania")
    os.makedirs(kat, exist_ok=True)
    sc = os.path.join(kat, f"Wyjasnienia_tresci_SWZ_{dt.date.today():%Y%m%d}.docx")
    PZ.wyjasnienia_docx(sc, st["projekt"]["nazwa"], st["K"].get("znak", ""), S.zamawiajacy_projektu(S.meta(pid)), P.get("pytania") or [],
                        P.get("unijne"), P.get("zmiany_terminu"), st["K"].get("termin_ofert", ""), godzina=st["K"].get("godzina_ofert", ""),
                        miejscowosc=str((S.cfg().get("firma_adres") or "")).split(",")[-1].strip().lstrip("0123456789- ") if not S.meta(pid).get("dla_prawnika") else "")
    return send_file(sc, as_attachment=True)


def _dokumenty_do_odpowiedzi(pid, st):
    """Dokumenty po zatwierdzeniu zmian (krok 6) – wersje „czyste”; bez nich dokumenty z kroku 5 albo własne wzory."""
    kon = os.path.join(S.pdir(pid), "dokumenty_koncowe")
    if os.path.isdir(kon):
        k = [os.path.join(kon, f) for f in sorted(os.listdir(kon)) if f.lower().endswith((".docx", ".pdf")) and "_ze_zmianami" not in f]
        if k:
            return k
    return S._pliki_do_przegladu(pid, st)


def praca_odpowiedz(log, pid, qid):
    """Projekt odpowiedzi na pytanie wykonawcy (AI) – na podstawie dokumentów postępowania; decyzję podejmuje zamawiający."""
    c = S.cfg()
    S.wymagany_klucz(c)
    c["_log"] = log
    st = _kreator_stan(pid)
    P = st["postepowanie"] or {}
    q = next((x for x in P.get("pytania") or [] if x["id"] == qid), None)
    if not q:
        raise ValueError("Nie ma takiego pytania.")
    bloki = []
    for p in _dokumenty_do_odpowiedzi(pid, st)[:12]:
        try:
            bloki += S.MO.przygotuj_blok(p)[0]
        except Exception:
            log(f"Nie udało się odczytać: {os.path.basename(p)} – pomijam.")
    if not bloki:
        raise ValueError("Brak dokumentów postępowania – przygotuj je w kreatorze (krok 5) albo wgraj wzory.")
    log("AI przygotowuje projekt odpowiedzi na podstawie dokumentów postępowania…")
    tresc = S.MO.oznacz_dokumenty(bloki, S.MO.ustawienie_cache(c)) + [{"type": "text", "text": PZ.polecenie_odpowiedzi(q.get("tresc"), P.get("unijne"))}]
    w = S._json_ai_z_ponowieniem(c, PZ.SYSTEM_ODPOWIEDZ, tresc, log, 4000, "odpowiedź na pytanie")
    if not isinstance(w, dict) or not w.get("odpowiedz"):
        raise ValueError("AI nie przygotowało odpowiedzi – spróbuj ponownie.")

    def f(K, P_):
        x = next((y for y in P_.get("pytania") or [] if y["id"] == qid), None)
        if x:
            x["odpowiedz"] = str(w.get("odpowiedz"))[:6000]
            x["zmiana_swz"] = bool(w.get("zmiana_swz"))
            x["zmiana_opis"] = str(w.get("zmiana_opis") or "")[:3000]
            x["przedluzenie_ai"] = bool(w.get("przedluzenie"))
            x["podstawa"] = str(w.get("podstawa") or "")[:300]
            x["ai"] = True
            x["zatwierdzona"] = False  # projekt AI – odpowiedzią staje się po zatwierdzeniu przez zamawiającego
    _postepowanie_zapis(pid, f)
    log("Gotowe: projekt odpowiedzi" + (" – odpowiedź zmienia SWZ" if w.get("zmiana_swz") else "") +
        ("; AI proponuje przedłużenie terminu składania ofert" if w.get("przedluzenie") else "") + ". Sprawdź i popraw przed publikacją.")


@bp.post("/api/projekty/<pid>/kreator/pytanie/<qid>/ai")
@S.wymaga_logowania
def kreator_pytanie_ai(pid, qid):
    return jsonify(S.uruchom("dokumentacja", "Odpowiedź na pytanie wykonawcy", praca_odpowiedz, pid, qid))
