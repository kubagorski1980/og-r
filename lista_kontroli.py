# -*- coding: utf-8 -*-
"""
Jedna lista kontrolna dokumentacji zamówienia – dla kroku 6 kreatora (sprawdzenie dokumentów), modułu „Weryfikacja dokumentacji”
i prawnika. Wymogi trybu pochodzą z tej samej tabeli co lista kroku 7 kreatora (kreator_zam.elementy / wspolnota.elementy),
lista ogólna zależy od reżimu: Pzp, zamówienie publiczne poza Pzp (poniżej progu, zasada konkurencyjności) albo zamawiający prywatny.
"""
import kreator_zam as KZ

TRYBY = {
    "auto": "Ustal z dokumentów",
    "podstawowy_1": "Tryb podstawowy bez negocjacji (art. 275 pkt 1)",
    "podstawowy_2": "Tryb podstawowy z możliwością negocjacji (art. 275 pkt 2)",
    "podstawowy_3": "Tryb podstawowy z obowiązkowymi negocjacjami (art. 275 pkt 3)",
    "przetarg_nieograniczony": "Przetarg nieograniczony",
    "przetarg_ograniczony": "Przetarg ograniczony",
    "negocjacje_z_ogloszeniem": "Negocjacje z ogłoszeniem",
    "dialog": "Dialog konkurencyjny",
    "partnerstwo": "Partnerstwo innowacyjne",
    "negocjacje_bez_ogloszenia": "Negocjacje bez ogłoszenia",
    "wolna_reka": "Zamówienie z wolnej ręki",
    "sektorowe": "Zamówienie sektorowe",
    "ponizej_progu": "Poniżej progu stosowania Pzp (regulamin / zapytanie ofertowe)",
    "zasada_konkurencyjnosci": "Zasada konkurencyjności (projekty z dofinansowaniem UE)",
    "krajowy": "Postępowanie krajowe (BZP – poniżej progów unijnych)",
    "unijny": "Postępowanie od progów unijnych (Dziennik Urzędowy UE)",
}
LISTA_WSPOLNA = """WSPÓLNE DLA KAŻDEGO PRZEDMIOTU:
- tryb: czy wybrany tryb jest dopuszczalny i czy spełniono jego przesłanki (np. wolna ręka, negocjacje bez ogłoszenia, warianty trybu podstawowego); wartość szacunkowa a progi (170 000 zł netto, progi unijne), zakaz dzielenia zamówienia, części zamówienia i uzasadnienie niepodzielenia;
- terminy: składania ofert (minimalne dla trybu i przedmiotu), związania ofertą (tryb podstawowy – najwyżej 30 dni, art. 307; od progów unijnych – najwyżej 90 dni, a 120 dni przy wartości robót od 20 000 000 euro / dostaw i usług od 10 000 000 euro, art. 220 ust. 1; pierwszym dniem jest dzień upływu terminu składania ofert), terminy na pytania i odwołania;
- warunki udziału – proporcjonalne do przedmiotu (art. 112), podstawy wykluczenia obligatoryjne i fakultatywne (art. 108, 109 – fakultatywne tylko wskazane w ogłoszeniu), podmiotowe i przedmiotowe środki dowodowe;
- wadium i zabezpieczenie należytego wykonania – dopuszczalna wysokość i formy;
- kryteria oceny ofert i opis sposobu ich stosowania (art. 239–246), w tym ograniczenia stosowania ceny jako jedynego kryterium;
- umowa: obowiązkowe postanowienia (art. 436 – m.in. łączna maksymalna wysokość kar umownych), postanowienia zakazane (art. 433), zmiany umowy (art. 454–455), waloryzacja – obowiązkowa w umowach na roboty, dostawy i usługi zawartych na okres dłuższy niż 6 miesięcy (art. 439);
- umowa zawarta na okres dłuższy niż 12 miesięcy: wynagrodzenie płatne w częściach albo zaliczki – ostatnia część najwyżej 50% wynagrodzenia, zaliczka co najmniej 5% (art. 443);
- formalności postępowania: zamówienie w planie postępowań (art. 23), oświadczenia osób wykonujących czynności o braku konfliktu interesów (art. 56), kwota na sfinansowanie zamówienia podana przed otwarciem ofert (art. 222 ust. 4), właściwe miejsce ogłoszenia – Biuletyn Zamówień Publicznych (tryby krajowe) albo Dziennik Urzędowy UE (od progów unijnych), w trybach bez ogłoszenia – ogłoszenie o wyniku / o udzieleniu zamówienia;
- spójność dokumentów (SWZ / ogłoszenie / opis przedmiotu / formularze / wzór umowy) – terminy, kwoty, zakres, gwarancja;
- RODO (klauzula informacyjna, powierzenie danych), jawność i tajemnica przedsiębiorstwa."""

LISTA_PRZEDMIOTU = {
    "roboty": """ROBOTY BUDOWLANE NA NIERUCHOMOŚCI:
- podstawy formalne inwestycji: prawo do dysponowania nieruchomością na cele budowlane, pozwolenie na budowę albo zgłoszenie, decyzje (środowiskowa, konserwatorska, inne), zgodność z planem miejscowym lub warunkami zabudowy – czy dokumentacja ich wymaga i czy na nie wskazuje;
- opis przedmiotu: dokumentacja projektowa i specyfikacja techniczna wykonania i odbioru robót (art. 103), program funkcjonalno-użytkowy przy „zaprojektuj i wybuduj”; spójność projektu, przedmiaru, specyfikacji i umowy;
- wynagrodzenie ryczałtowe albo kosztorysowe – spójność z przedmiarem i ryzyko robót dodatkowych / zamiennych;
- podwykonawstwo robót (art. 462–465): obowiązki w umowie, zgłaszanie umów, płatności bezpośrednie;
- zatrudnienie na podstawie umowy o pracę osób wykonujących czynności (art. 95);
- kierownik budowy i uprawnienia budowlane, warunki doświadczenia proporcjonalne do zakresu;
- harmonogram, odbiory częściowe i końcowy, gwarancja i rękojmia, ubezpieczenie, przekazanie terenu budowy, wizja lokalna.""",
    "uslugi": """USŁUGI:
- opis przedmiotu zamówienia – jednoznaczny i wyczerpujący, mierniki jakości (np. poziomy usług), sposób rozliczania;
- zatrudnienie na podstawie umowy o pracę (art. 95), aspekty społeczne, usługi społeczne i szczególne (jeśli dotyczy – właściwy tryb);
- kryteria jakościowe i sposób ich oceny (doświadczenie personelu, organizacja);
- prawa autorskie przy usługach projektowych, IT, szkoleniowych (przeniesienie praw, pola eksploatacji, licencje);
- poufność, powierzenie przetwarzania danych osobowych, odpowiedzialność i ubezpieczenie OC;
- kary i odstąpienie proporcjonalne do usługi ciągłej, okres umowy a waloryzacja (powyżej 6 miesięcy).""",
    "dostawy": """DOSTAWY:
- opis przedmiotu – neutralność: znaki towarowe, patenty, pochodzenie tylko gdy uzasadnione przedmiotem, z dopuszczeniem rozwiązań równoważnych i kryteriami równoważności (art. 99); wymagania wskazujące jednego producenta;
- etykiety, certyfikaty, normy i przedmiotowe środki dowodowe (art. 104–107) – czy wymagane zasadnie i czy przewidziano ich uzupełnienie;
- prawo opcji i dostawy częściowe (art. 441), ilości minimalne i maksymalne;
- termin, miejsce i warunki dostawy, odbiór ilościowy i jakościowy, reklamacje;
- gwarancja i serwis, szkolenia, dokumentacja, licencje (przy sprzęcie z oprogramowaniem);
- okres umowy a waloryzacja (powyżej 6 miesięcy)."""}

LISTA_POZA_PZP = """ZAMÓWIENIE POZA PZP (nie stosuje się przepisów Pzp, odwołania do KIO nie przysługują – nie zgłaszaj uwag „niezgodne z Pzp”):
- podstawa wyłączenia: wartość szacunkowa poniżej 170 000 zł netto (art. 2 ust. 1 pkt 1 Pzp) ustalona rzetelnie, bez dzielenia zamówienia w celu uniknięcia progu;
- zgodność z regulaminem udzielania zamówień zamawiającego (albo – przy dofinansowaniu – z umową o dofinansowanie i wytycznymi), zasady przejrzystości, równego traktowania i uczciwej konkurencji;
- zapytanie ofertowe: jednoznaczny opis przedmiotu, termin i sposób składania ofert, kryteria z wagami i sposobem punktacji, warunki udziału (jeśli są) proporcjonalne, termin związania ofertą;
- umowa według Kodeksu cywilnego: kary umowne (rażące wygórowanie – art. 484 § 2 k.c.), odstąpienie, gwarancja i rękojmia, zmiany umowy, waloryzacja (zalecana przy dłuższych umowach);
- spójność dokumentów, RODO, konflikt interesów osób przygotowujących i oceniających."""

# szczegóły trybów, których nie ma w liście kontrolnej kreatora (lista kreatora: kreator_zam.elementy – ta sama tabela w kreatorze i u prawnika)
DODATKI_GRUPY = {
    "A": "- wariant trybu podstawowego: pkt 2 – możliwość negocjacji zastrzeżona w ogłoszeniu i SWZ; pkt 3 – obowiązkowe negocjacje i opis potrzeb zamiast pełnej SWZ; "
         "związanie ofertą najwyżej 30 dni (art. 307); minimalne terminy składania ofert dla trybu podstawowego.",
    "B": "- od progów unijnych: ogłoszenie w Dzienniku Urzędowym UE, oświadczenie w formie JEDZ, minimalne terminy unijne, kwalifikowany podpis elektroniczny oferty; "
         "przetarg ograniczony / negocjacje z ogłoszeniem / dialog – etap wniosków, liczba zapraszanych wykonawców i kryteria selekcji.",
    "C": "- partnerstwo innowacyjne: opis potrzeby innowacyjnego rozwiązania, etapy i cele pośrednie, prawa własności intelektualnej, wynagrodzenie za etapy.",
    "D": "- negocjacje bez ogłoszenia: konkretna przesłanka ustawowa (poniżej progów unijnych – art. 301, od progów – art. 209) opisana faktami i udokumentowana; "
         "wybór zapraszanych wykonawców zapewniający konkurencję; przebieg negocjacji w protokole; ogłoszenie o wyniku (art. 309) albo o udzieleniu zamówienia (Dz.U. UE).",
    "E": "- wolna ręka: konkretna przesłanka ustawowa (poniżej progów unijnych – art. 305, od progów – art. 214 ust. 1) opisana faktami i udokumentowana, wykładana ściśle; "
         "bez kryteriów oceny ofert, podziału na części i kwoty z art. 222 ust. 4; zaproszenie do negocjacji z projektowanymi postanowieniami umowy; podmiotowe środki "
         "dowodowe najpóźniej do zawarcia umowy, oświadczenie z art. 125 opcjonalne (art. 217); in-house – ogłoszenie o zamiarze zawarcia umowy i 14 dni (art. 216).",
    "G": "- zasada konkurencyjności (wytyczne kwalifikowalności 2021–2027 i umowa o dofinansowanie): zapytanie i wynik w Bazie Konkurencyjności, minimalne terminy, "
         "brak powiązań osobowych i kapitałowych, protokół – naruszenia skutkują korektą finansową, nie odwołaniem do KIO.",
}
# tryb u prawnika → (kategoria z wartości, tryb w kreatorze)
TRYB_KREATORA = {"podstawowy_1": ("pzp_podstawowy", "podstawowy_1"), "podstawowy_2": ("pzp_podstawowy", "podstawowy_2"),
                 "podstawowy_3": ("pzp_podstawowy", "podstawowy_3"), "krajowy": ("pzp_podstawowy", "podstawowy_1"),
                 "unijny": ("pzp_nieograniczony", "przetarg_nieograniczony"),
                 "przetarg_nieograniczony": ("pzp_nieograniczony", "przetarg_nieograniczony"), "przetarg_ograniczony": ("pzp_nieograniczony", "przetarg_ograniczony"),
                 "negocjacje_z_ogloszeniem": ("pzp_nieograniczony", "negocjacje_z_ogloszeniem"), "dialog": ("pzp_nieograniczony", "dialog"),
                 "partnerstwo": ("pzp_inny", "partnerstwo"), "negocjacje_bez_ogloszenia": ("pzp_inny", "negocjacje_bez_ogloszenia"),
                 "wolna_reka": ("pzp_inny", "wolna_reka"), "ponizej_progu": ("ponizej_130", "ponizej_progu"),
                 "zasada_konkurencyjnosci": ("konkurencyjnosc", "zasada_konkurencyjnosci")}


def grupa(tryb):
    """Grupa trybu jak w kreatorze (A–G); None – tryb do ustalenia z dokumentów albo sektorowy."""
    t = TRYB_KREATORA.get(tryb)
    return KZ.grupa_trybu(*t) if t else None


def lista_trybu(tryb, przedmiot="roboty"):
    """Wymogi właściwe dla trybu – z tej samej tabeli co lista kontrolna kreatora zamówienia (kreator_zam.elementy)."""
    if tryb == "auto":
        return ("WYMOGI TRYBU: najpierw ustal tryb i wartość z dokumentów, potem stosuj wymogi tego trybu – tryb podstawowy: ogłoszenie w BZP, "
                "związanie ofertą do 30 dni (art. 307); od progów unijnych: Dziennik Urzędowy UE, JEDZ, związanie ofertą do 90 dni (120 dni – art. 220 ust. 1 pkt 2); negocjacje bez ogłoszenia i wolna ręka: przesłanka ustawowa "
                "(art. 301 / 305, od progów art. 209 / 214), bez kryteriów i kwoty z art. 222 ust. 4 w wolnej ręce; poniżej 170 000 zł netto – Pzp nie stosuje się "
                "(regulamin); dofinansowanie UE – zasada konkurencyjności (Baza Konkurencyjności).")
    if tryb == "sektorowe":
        return ("WYMOGI TRYBU (zamówienie sektorowe): podstawa uznania za zamawiającego sektorowego i działalność sektorową, progi sektorowe, "
                "tryby i terminy dla zamówień sektorowych, regulamin dla zamówień poniżej progów sektorowych.")
    baza, kod = TRYB_KREATORA[tryb]
    g = KZ.grupa_trybu(baza, kod)
    el = [e["opis"] for e in KZ.elementy(baza, przedmiot, False, kod) if e["id"] != "kosztorys"]
    return (f"WYMOGI TRYBU „{TRYBY[tryb]}” (lista jak w kreatorze zamówienia – sprawdź, czy dokumentacja je spełnia):\n"
            + "\n".join("- " + x for x in el) + ("\n" + DODATKI_GRUPY[g] if g in DODATKI_GRUPY else ""))


LISTA_PRZEDMIOTU_POZA = {  # ten sam zakres bez instytucji Pzp – zamówienie poza Pzp albo zamawiający prywatny
    "roboty": """ROBOTY BUDOWLANE (bez Pzp):
- podstawy formalne: prawo do dysponowania nieruchomością na cele budowlane, pozwolenie na budowę albo zgłoszenie (Prawo budowlane), decyzje i uzgodnienia, jeśli wymagane;
- opis zakresu prac: projekt, przedmiar albo opis robót spójny z umową; wymagania materiałowe z dopuszczeniem rozwiązań równoważnych;
- wynagrodzenie ryczałtowe (art. 632 k.c.) albo kosztorysowe (art. 629 k.c.) – spójność z przedmiarem, roboty dodatkowe i zamienne;
- podwykonawcy (art. 647¹ k.c. – solidarna odpowiedzialność inwestora), kierownik budowy i uprawnienia;
- harmonogram, odbiory częściowe i końcowy, gwarancja i rękojmia, ubezpieczenie, przekazanie terenu budowy.""",
    "uslugi": """USŁUGI (bez Pzp):
- jednoznaczny opis usługi, mierniki jakości, sposób rozliczania;
- prawa autorskie przy usługach projektowych i IT, poufność, powierzenie przetwarzania danych osobowych;
- odpowiedzialność, ubezpieczenie OC, kary i wypowiedzenie proporcjonalne do usługi ciągłej, waloryzacja przy dłuższych umowach (zalecana).""",
    "dostawy": """DOSTAWY (bez Pzp):
- opis przedmiotu bez wskazania jednego producenta albo z „lub równoważny” i kryteriami równoważności;
- termin, miejsce i warunki dostawy, odbiór ilościowy i jakościowy, reklamacje;
- gwarancja i serwis, dokumentacja, licencje przy sprzęcie z oprogramowaniem."""}

LISTA_PRYWATNA = """ZAMAWIAJĄCY PRYWATNY (wspólnota, spółdzielnia, deweloper – bez Pzp; zasady z umowy o dofinansowanie tylko, gdy ją wskazano):
- podstawa decyzji: uchwała właścicieli lokali albo plan gospodarczy (wspólnota), zgoda współwłaścicieli (mała wspólnota), regulamin spółdzielni;
- zapytanie ofertowe: zakres prac, termin i sposób składania ofert, kryteria z wagami i sposobem oceny, wymagane dokumenty i referencje możliwe do potwierdzenia;
- umowa według Kodeksu cywilnego: wynagrodzenie, odbiory, płatności, kaucja gwarancyjna, łączny limit kar umownych, odstąpienie, gwarancja i rękojmia, podwykonawcy;
- spójność dokumentów i RODO (zamawiający jako administrator danych)."""

REZIMY = {"pzp": "Pzp", "poza": "zamówienie publiczne poza Pzp", "prywatny": "zamawiający prywatny (bez Pzp)"}


def rezim(grupa_, prywatny=False):
    """pzp | poza (poniżej progu, zasada konkurencyjności) | prywatny (wspólnota, spółdzielnia, deweloper)."""
    return "prywatny" if prywatny else "poza" if grupa_ in ("F", "G") else "pzp"


def lista_ogolna(rez, przedmiot="roboty"):
    """Lista przedmiotu i lista ogólna właściwe dla reżimu."""
    przedm = (LISTA_PRZEDMIOTU if rez == "pzp" else LISTA_PRZEDMIOTU_POZA).get(przedmiot) or LISTA_PRZEDMIOTU_POZA["roboty"]
    return przedm + "\n" + {"pzp": LISTA_WSPOLNA, "poza": LISTA_POZA_PZP, "prywatny": LISTA_PRYWATNA}[rez]


def lista_kreatora(elementy, grupa_, prywatny, przedmiot="roboty", tryb_opis=""):
    """Krok 6 kreatora: pozycje listy kontrolnej kroku 7 (te same, które zamawiający odhacza przed publikacją) + szczegóły trybu
    + lista ogólna reżimu."""
    rez = rezim(grupa_, prywatny)
    el = [e["opis"] for e in elementy if e.get("id") != "kosztorys"]
    return (f"LISTA KONTROLNA – {tryb_opis or REZIMY[rez]} ({REZIMY[rez]}); gdy wymogi trybu stanowią inaczej niż lista ogólna – stosuj wymogi trybu:\n"
            + "\n".join("- " + x for x in el)
            + ("\n" + DODATKI_GRUPY[grupa_] if rez == "pzp" and grupa_ in DODATKI_GRUPY else "")
            + "\n" + lista_ogolna(rez, przedmiot))


def lista_weryfikacji(tryb, przedmiot="roboty", prywatny=False):
    """Moduł „Weryfikacja dokumentacji” (zamawiający): tryb jak u prawnika (TRYBY, „auto” = ustal z dokumentów)."""
    if prywatny:
        return lista_ogolna("prywatny", przedmiot)
    rez = rezim(grupa(tryb))
    return lista_trybu(tryb, przedmiot) + "\n" + lista_ogolna(rez, przedmiot)
