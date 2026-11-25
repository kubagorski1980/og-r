# -*- coding: utf-8 -*-
"""
Zamówienia wspólnot mieszkaniowych, spółdzielni i deweloperów – OSOBNE reguły, bez Prawa zamówień publicznych.

Podstawy: ustawa o własności lokali (zarząd, uchwały właścicieli, plan gospodarczy), ustawa o spółdzielniach mieszkaniowych i Prawo spółdzielcze
(statut, regulamin przetargów spółdzielni), Kodeks cywilny (umowa o roboty budowlane, rękojmia, gwarancja, kary umowne), Prawo budowlane
(zgłoszenie albo pozwolenie na budowę, kierownik budowy), RODO. Pzp nie ma zastosowania – chyba że wymaga tego umowa o dofinansowanie
(wtedy obowiązują jej zasady, np. zasada konkurencyjności). Podpowiedzi to dobra praktyka, nie wymóg ustawowy, chyba że wskazano przepis.
"""

TRYBY = {
    "pryw_zapytanie": "Zapytanie ofertowe (konkurs ofert) – zaproszenie do składania ofert",
    "pryw_wybrani": "Zapytanie do wybranych wykonawców (zalecane co najmniej 3 oferty)",
    "pryw_regulamin": "Przetarg według regulaminu spółdzielni (statut / regulamin przetargów)",
    "pryw_konkurencyjnosc": "Zasada konkurencyjności – gdy wymaga jej umowa o dofinansowanie (Baza Konkurencyjności)",
}
DOMYSLNY = "pryw_zapytanie"


TRYBY_TYLKO_DLA = {"pryw_regulamin": ("spoldzielnia",)}  # przetarg według regulaminu – tylko spółdzielnia (wspólnota i deweloper nie mają regulaminu przetargów)


def tryby_dla(podmiot=None):
    """Tryby dostępne dla rodzaju zamawiającego (bez podmiotu – wszystkie)."""
    return {k: v for k, v in TRYBY.items() if not podmiot or podmiot in TRYBY_TYLKO_DLA.get(k, (podmiot,))}


def tryb(K):
    t = (K or {}).get("tryb_wybrany")
    return t if t in tryby_dla((K or {}).get("podmiot") or "wspolnota") else DOMYSLNY


def termin_ofert(rodzaj):
    """Termin składania ofert – bez przepisu; dobra praktyka: czas na wizję lokalną i przygotowanie wyceny."""
    if rodzaj == "roboty":
        return 14, "zapytanie wspólnoty / spółdzielni: termin ustala zarząd; przy robotach zalecane co najmniej 14 dni (wizja lokalna, przedmiar, wycena)"
    return 7, "zapytanie wspólnoty / spółdzielni: termin ustala zarząd; zalecane co najmniej 7 dni"


def warunki_domyslne(rodzaj):
    """Warunki zapytania prywatnego zamawiającego – bez instytucji Pzp (wadium, zabezpieczenie z art. 452, waloryzacja z art. 439, art. 95)."""
    return {
        "wynagrodzenie": "ryczałtowe" if rodzaj == "roboty" else "według cen jednostkowych z oferty",
        "kryteria": "cena 80%, okres gwarancji 20%",
        "gwarancja": "60 miesięcy" if rodzaj == "roboty" else "24 miesiące",
        "kary": "za zwłokę w zakończeniu robót 0,2% wynagrodzenia za każdy dzień; łącznie najwyżej 20% wynagrodzenia",
        "platnosci": "po odbiorze robót (albo etapów według harmonogramu), przelewem w terminie 30 dni od doręczenia faktury",
        "wadium": "nie wymagane",
        "zabezpieczenie": "kaucja gwarancyjna 5% wynagrodzenia (zatrzymywana z faktury końcowej, zwrot po upływie rękojmi) – do decyzji zarządu",
        "waloryzacja": "do decyzji stron (przy umowach dłuższych niż 12 miesięcy warto przewidzieć zmianę wynagrodzenia przy istotnej zmianie cen)",
        "podwykonawstwo": "dopuszczalne po zgłoszeniu zarządowi; wykonawca odpowiada za podwykonawców jak za własne działania",
        "warunki": ("doświadczenie: co najmniej 2 podobne prace w ostatnich 5 latach; wykaz prac z nazwą, NIP i danymi kontaktowymi zamawiających "
                    "(wystawców referencji) oraz dowody należytego wykonania (referencje, protokoły odbioru); zamawiający może zwrócić się do wystawców "
                    "o potwierdzenie; polisa OC działalności; wpis do KRS albo CEIDG" + ("; kierownik robót z uprawnieniami budowlanymi, "
                                                                                       "gdy wymaga tego Prawo budowlane" if rodzaj == "roboty" else "")),
        "klauzule": ("podanie nieprawdziwych informacji o doświadczeniu albo przedstawienie nieprawdziwych referencji uprawnia zamawiającego "
                     "do odrzucenia oferty, a po zawarciu umowy – do odstąpienia od umowy z winy wykonawcy"),
        "czesci": "bez podziału – jeden wykonawca dla całego zakresu",
        "platforma": "oferty e-mailem albo w zamkniętej kopercie w siedzibie zarządu / administratora",
        "kontakt": "",
    }


POMOC = {
    "wynagrodzenie": "Ryczałtowe – stała kwota za cały zakres (ryzyko ilości po stronie wykonawcy, art. 632 KC); kosztorysowe – według obmiaru i cen "
                     "jednostkowych (art. 629 KC). Przy remontach o niepewnym zakresie częściej kosztorysowe.",
    "kryteria": "Wspólnota sama ustala kryteria – poza ceną warto ocenić okres gwarancji, termin i doświadczenie; sposób oceny podaj w zapytaniu.",
    "gwarancja": "Gwarancja jest dobrowolna (art. 577 KC) – jej okres i zakres określa umowa; niezależnie od niej przysługuje rękojmia za wady.",
    "kary": "Kary umowne (art. 483–484 KC) – warto ustalić łączny limit; rażąco wygórowaną karę sąd może obniżyć.",
    "zabezpieczenie": "Kaucja albo gwarancja bankowa / ubezpieczeniowa – nie jest obowiązkowa; chroni wspólnotę na czas rękojmi i gwarancji.",
    "waloryzacja": "Nie jest obowiązkowa – przy długich umowach chroni przed zejściem wykonawcy z budowy przy wzroście cen.",
    "warunki": "Wymagania wobec wykonawców ustala zarząd – powinny być związane z zakresem prac; wykaz z kontaktami pozwala potwierdzić referencje.",
    "platforma": "Wspólnota nie musi korzystać z platform zakupowych – chyba że wymaga tego umowa o dofinansowanie (np. Baza Konkurencyjności).",
    "czesci": "Podział na części (np. dach, elewacja, instalacje) może dać więcej ofert od mniejszych firm – kosztem koordynacji kilku wykonawców.",
}

UCHWALA = ("W małej wspólnocie (najwyżej 3 lokale wyodrębnione i niewyodrębnione) zamiast uchwał stosuje się przepisy Kodeksu cywilnego o współwłasności "
           "(art. 19 ustawy o własności lokali). Prace wykraczające poza zwykły zarząd (np. termomodernizacja, wymiana dachu, remont finansowany kredytem) "
           "wymagają uchwały właścicieli lokali wyrażającej zgodę na tę czynność i udzielającej zarządowi pełnomocnictwa do zawarcia umowy (art. 22 ust. 2 "
           "ustawy o własności lokali) – w praktyce ujęcia w planie gospodarczym (art. 30) albo odrębnej uchwały; przy kredycie – uchwały o jego zaciągnięciu. "
           "Uchwała zapada większością głosów liczoną według udziałów (art. 23 ust. 2), na zebraniu albo w trybie indywidualnego zbierania głosów. "
           "Umowę w imieniu wspólnoty podpisują co najmniej dwaj członkowie zarządu (art. 21 ust. 2), a gdy zarząd powierzono zarządcy (art. 18 ust. 1) – "
           "zarządca w granicach umowy o zarządzanie. W spółdzielni decyduje organ wskazany w statucie. Zakres uchwały sprawdź z zarządcą.")


PODMIOTY = {
    "wspolnota": "wspólnota mieszkaniowa (więcej niż 3 lokale)",
    "mala": "mała wspólnota (najwyżej 3 lokale wyodrębnione i niewyodrębnione – art. 19 ustawy o własności lokali)",
    "spoldzielnia": "spółdzielnia mieszkaniowa",
    "deweloper": "deweloper / inny inwestor prywatny",
}


def zgoda(podmiot):
    """Pozycja listy kontrolnej o zgodzie na prace – zależnie od rodzaju zamawiającego; deweloper – brak (decyduje sam)."""
    return {
        "wspolnota": "Uchwała właścicieli lokali albo plan gospodarczy obejmujący prace i ich finansowanie (art. 22 i 30 ustawy o własności lokali); "
                     "przy pracach przekraczających zwykły zarząd – uchwała wyrażająca zgodę i udzielająca zarządowi pełnomocnictwa do zawarcia umowy "
                     "(art. 22 ust. 2); przy kredycie – uchwała o jego zaciągnięciu",
        "mala": "Zgoda współwłaścicieli według Kodeksu cywilnego (art. 19 ustawy o własności lokali): na czynności przekraczające zwykły zarząd "
                "– zgoda wszystkich współwłaścicieli (art. 199 KC), na czynności zwykłego zarządu – większość udziałów (art. 201 KC)",
        "spoldzielnia": "Decyzja organu spółdzielni według statutu (zarząd / rada nadzorcza) i plan remontów; przy kredycie – zgoda właściwego organu",
    }.get(podmiot or "wspolnota")


def elementy(rodzaj, podzial=False, tryb_=DOMYSLNY, podmiot="wspolnota"):
    """Lista kontrolna przed rozesłaniem zapytania – wspólnota / spółdzielnia / deweloper (bez Pzp).
    Rodzaje: „sprawdzenie” – dokument zapytania (sprawdzany w kroku 6), „reczne” – czynność do odhaczenia, „auto” – kosztorys.
    Protokół wyboru wykonawcy jest po zebraniu ofert (sekcja „Po zebraniu ofert” w kroku 7), nie na tej liście."""
    podmiot = podmiot or "wspolnota"
    E = [("uchwala", zgoda(podmiot), "reczne")] if zgoda(podmiot) else []
    if tryb_ == "pryw_regulamin" and podmiot == "spoldzielnia":
        E.append(("regulamin_sp", "Zgodność z regulaminem przetargów spółdzielni (ogłoszenie, komisja, termin, otwarcie ofert)", "reczne"))
    E += [("kosztorys", "Szacunek kosztów albo kosztorys / przedmiar – do budżetu i porównania ofert", "auto"),
          ("zakres", "Opis zakresu prac (przedmiar, ekspertyza, projekt – gdy potrzebny); zgłoszenie albo pozwolenie na budowę według Prawa budowlanego"
                     if rodzaj == "roboty" else "Opis zakresu usług / dostaw z wymaganiami jakościowymi", "sprawdzenie"),
          ("kryteria", "Kryteria wyboru oferty (cena, gwarancja, termin, doświadczenie) i sposób oceny podany w zapytaniu", "sprawdzenie"),
          ("dokumenty", "Wymagane dokumenty: wykaz prac z kontaktami do zamawiających, referencje, polisa OC, wpis do KRS albo CEIDG", "sprawdzenie"),
          ("umowa", "Wzór umowy (Kodeks cywilny): zakres, termin, wynagrodzenie, odbiory, gwarancja i rękojmia, kary umowne z limitem, kaucja, podwykonawcy"
                    + ("; reprezentacja wspólnoty: co najmniej dwaj członkowie zarządu (art. 21 ust. 2 ustawy o własności lokali) albo zarządca, "
                       "któremu powierzono zarząd (art. 18 ust. 1)" if podmiot == "wspolnota" else ""),
           "sprawdzenie"),
          ("rodo", "Informacja o przetwarzaniu danych oferentów (zamawiający jako administrator danych)", "sprawdzenie"),
          ("rozeslanie", ("Zaproszenie co najmniej 3 wykonawców (zalecane, żeby porównać oferty); termin i sposób składania ofert" if tryb_ == "pryw_wybrani"
                          else "Termin i sposób składania ofert; rozesłanie zapytania do wykonawców") + " (także „Zaproś wykonawców z okolicy”)", "reczne"),
          ("finansowanie", "Jeśli prace są kredytowane lub dofinansowane: wymagania banku albo instytucji finansującej wobec wyboru wykonawcy i umowy "
                           "(sekcja „Finansowanie inwestycji” w realizacji)", "reczne")]
    if tryb_ == "pryw_konkurencyjnosc":  # te same pozycje co zasada konkurencyjności u zamawiającego publicznego (kreator_zam.elementy, grupa G)
        E += [("bk2021", "Publikacja zapytania ofertowego i informacji o wyniku w Bazie Konkurencyjności (BK2021)", "reczne"),
              ("termin_bk", "Termin składania ofert: co najmniej 7 dni (dostawy, usługi), 14 dni (roboty budowlane), 30 dni (od progów z wytycznych: dostawy i usługi – 750 000 euro, roboty budowlane – próg unijny, od 1.01.2026 r. 5 404 000 euro)", "reczne"),
              ("powiazania", "Konflikt interesów – brak powiązań osobowych i kapitałowych wykonawców z zamawiającym, oświadczenia (wytyczne 2021–2027 i umowa o dofinansowanie)", "sprawdzenie")]
    if podzial:
        E.append(("czesci", "Podział na części: opis każdej części i cena za każdą część w formularzu oferty", "sprawdzenie"))
    return [{"id": i, "opis": o, "rodzaj": r} for i, o, r in E]


KONTEKST_AI = (
    "\n\nWAŻNE – ZAMAWIAJĄCY PRYWATNY: zamawiającym jest wspólnota mieszkaniowa, spółdzielnia mieszkaniowa albo deweloper. NIE stosuje on ustawy "
    "Prawo zamówień publicznych – nie wymagaj ani nie oceniaj instytucji Pzp (SWZ, tryby, ogłoszenie w BZP, plan postępowań, oświadczenia z art. 125, "
    "wadium i zabezpieczenie według Pzp, waloryzacja z art. 439, art. 95, kwota z art. 222, warunki udziału według Pzp, regulamin zamówień jednostki "
    "publicznej, BIP, Baza Konkurencyjności) – chyba że dokument wprost odwołuje się do umowy o dofinansowanie wymagającej zasady konkurencyjności. "
    "W małej wspólnocie (najwyżej 3 lokale) decyzje podejmują współwłaściciele według Kodeksu cywilnego (art. 199 i 201 KC), nie uchwałami. "
    "We wspólnocie (więcej niż 3 lokale) czynność przekraczająca zwykły zarząd wymaga uchwały właścicieli wyrażającej zgodę i udzielającej zarządowi "
    "pełnomocnictwa do zawarcia umowy (art. 22 ust. 2 ustawy o własności lokali), a umowę za wspólnotę podpisują co najmniej dwaj członkowie zarządu "
    "(art. 21 ust. 2) albo zarządca, któremu powierzono zarząd (art. 18 ust. 1) – we wzorze umowy wskaż reprezentację wspólnoty zgodnie z tym. "
    "Oceniaj według: Kodeksu cywilnego (umowa o roboty budowlane art. 647–658, wynagrodzenie ryczałtowe art. 632 i kosztorysowe art. 629, rękojmia, "
    "gwarancja art. 577, kary umowne art. 483–484), ustawy o własności lokali (uchwały właścicieli, plan gospodarczy) albo statutu i regulaminu "
    "spółdzielni, Prawa budowlanego (zgłoszenie albo pozwolenie, kierownik budowy) i RODO oraz dobrej praktyki: jasny zakres prac, kryteria i sposób "
    "oceny, wymagane dokumenty i referencje możliwe do potwierdzenia, odbiory, płatności, kaucja, limit kar, podwykonawcy. Używaj słów: zapytanie "
    "ofertowe, opis zakresu prac, formularz oferty, umowa – nie SWZ ani OPZ.")
