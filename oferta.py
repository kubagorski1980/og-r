# -*- coding: utf-8 -*-
"""
„Nasza oferta” – treść i budowa strony (publicznej) oraz dokumentów PDF.
Strona: trzy ikony (Wykonawca, Zamawiający, Inwestor indywidualny) – po kliknięciu pokazuje się oferta dla danego klienta.
"""
import html as _h

IKONY = {
    "wykonawca": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/>',
    "zamawiajacy": '<path d="M3 21h18"/><path d="M5 21V10"/><path d="M19 21V10"/><path d="M9 21v-6h6v6"/><path d="M2 10l10-6 10 6"/><path d="M9 10v2M15 10v2"/>',
    "dostawca": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "inwestor": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/><path d="M16 7V4h2v5"/>',
    "rzeczoznawca": '<path d="M3 21h18"/><path d="M5 21V9l7-5 7 5v12"/><circle cx="12" cy="13" r="3"/><path d="M14.2 15.2L17 18"/>',
    "dotacje": '<circle cx="12" cy="12" r="9"/><path d="M12 7v10"/><path d="M15 9.5c0-1.4-1.3-2.5-3-2.5s-3 1-3 2.3c0 3.2 6 1.8 6 5 0 1.4-1.3 2.7-3 2.7s-3-1.1-3-2.5"/>',
}

GRUPY = {
    "wykonawca": {
        "tytul": "Dla Wykonawcy", "krotko": "Firmy budowlane i remontowe",
        "kto": ["firmy budowlane i remontowe startujące w przetargach publicznych i zapytaniach ofertowych",
                "wykonawcy robót termomodernizacyjnych, dachowych, elewacyjnych, instalacyjnych i drogowych",
                "firmy realizujące zlecenia wspólnot, spółdzielni, firm i inwestorów prywatnych"],
        "kolor": "#1F5A99", "haslo": "Więcej trafionych przetargów, szybsze i lepiej policzone oferty, pełna kontrola budów i roszczeń – w jednym programie.",
        "wyzwania": [
            ("Przeglądanie kilku serwisów z ogłoszeniami każdego dnia zabiera godziny, a ciekawe przetargi i tak umykają.",
             "Prosta wyszukiwarka w trzech krokach (czego, gdzie, u kogo) przeszukuje BZP, Bazę Konkurencyjności, BIP urzędów oraz strony szpitali, uczelni i dużych spółek – i codziennie powiadamia o nowych przetargach."),
            ("Czytanie SWZ, OPZ, przedmiaru i wzoru umowy, żeby zdecydować, czy w ogóle startować.",
             "Analiza przetargu w kilka minut: termin, wadium, warunki, kryteria, kary, ryzyka – z odpowiedziami na pytania z cytatem z dokumentu."),
            ("Kosztorys ofertowy powstaje wieczorami, a błąd w ilościach albo cenie kosztuje marżę.",
             "Kosztorys z przedmiaru lub projektu z cenami rynkowymi, formularze ofertowe i kontrola kosztorysu przed złożeniem oferty."),
            ("Na budowie pojawiają się prace dodatkowe, błędy w dokumentacji i przestoje – a brakuje czasu na pisma i wyliczenia.",
             "Gotowe wnioski o przedłużenie terminu i dopłatę z kosztorysem, monitoring pogody i aneksy po akceptacji zamawiającego."),
        ],
        "moduly": [
            ("Wyszukiwanie przetargów", "Codzienny przegląd ogłoszeń bez ręcznego przeszukiwania internetu.",
             ["Trzy kroki i jeden przycisk: czego szukasz (słowa i gotowe zestawy branżowe), gdzie (okolica z promieniem, województwa, cała Polska), u kogo (urzędy, szpitale, uczelnie, duże spółki, wspólnoty).",
              "Źródła: Biuletyn Zamówień Publicznych, Baza Konkurencyjności (projekty unijne), BIP urzędów oraz strony przetargowe szpitali, uczelni i spółek (KGHM, Orlen, PGE, Tauron, PKP, spółki komunalne) – znajdowane automatycznie w Twoim obszarze.",
              "Pełna lista ogłoszeń z BZP – każdego dnia wszystkie ogłoszenia o zamówieniu (zwykle 400–600); wstępne sito bez AI kieruje do oceny najpierw te, które pasują do Twoich słów w tytule lub kodzie CPV, a słabsze dopasowania zostają w wynikach z oznaczeniem.",
              "Wyniki tylko z danego wyszukiwania, z oceną dopasowania i filtrami z licznikami (urzędy, szpitale, spółki, nowe).",
              "Codzienne powiadomienie o nowych wynikach i raport e-mail; nowe przetargi widoczne od razu na pulpicie.",
              "Statusy (startujemy, do analizy, oferta złożona, wygrany, przegrany) i historia decyzji, z której uczy się ocena AI."]),
            ("Analiza i ocena przetargu", "Decyzja „startujemy czy nie” w kilka minut.",
             ["Ocena dopasowania 1–10 z uzasadnieniem, uwzględniająca profil Twojej firmy i wcześniejsze decyzje.",
              "Ok. 30 kluczowych informacji w pięciu grupach: najważniejsze, terminy, pieniądze, warunki, ocena dla firmy.",
              "Termin składania ofert z odliczaniem i kolorem pilności; wadium, gwarancja, termin realizacji, kryteria oceny.",
              "Pobranie wszystkich dokumentów postępowania jednym kliknięciem – także z platform zamawiających i duże archiwa z projektem – z rozpoznaniem formatów plików i sprawdzeniem, czy plik pobrał się w całości.",
              "Asystent dokumentów: zadajesz pytanie, dostajesz odpowiedź z cytatem, nazwą pliku i numerem strony."]),
            ("Konkurencja i szanse wygranej", "Cena, która wygrywa – a nie zgadywanie.",
             ["Konkurencja u zamawiającego: wcześniejsze przetargi, liczba ofert, ceny i zwycięzcy (z ogłoszeń o wyniku w BZP).",
              "Kalkulator szans wygranej: przy jakiej cenie masz 50%, 70% i 90% szans – i jednym kliknięciem przeliczenie oferty do tej ceny.",
              "Wygrane i przegrane: skuteczność, różnica do zwycięzcy, wyniki sprawdzane automatycznie po otwarciu ofert."]),
            ("Oferta i kosztorys", "Kompletna oferta przygotowana w programie.",
             ["Kosztorys z przedmiaru, projektu lub opisu – cenami rynkowymi albo według Twojego własnego cennika (brakujące pozycje cenami rynkowymi); najdroższe pozycje rynkowe sprawdzane w internecie.",
              "Poprawianie wybranych pozycji kosztorysu: własna nazwa, cena jednostkowa lub wartość – poprawiony kosztorys jest podstawą oferty.",
              "Wybór stawki VAT (z dokumentów przetargu albo ręcznie), dopasowanie ceny do kwoty docelowej lub procentu.",
              "Formularze ofertowe w Wordzie, kosztorys ofertowy i kosztorys dla klienta (bez notatek roboczych) w Excelu.",
              "Kontrola kosztorysu: brak ceny, zerowe ilości, nierealne ceny, rozbieżności i brakujące roboty – z propozycją poprawki.",
              "Wykrywanie błędów i sprzeczności w dokumentacji przetargowej (SWZ, przedmiar, projekt, wzór umowy).",
              "Komplet dokumentów do przetargu z profilu firmy: polisa, referencje, certyfikaty – dodawane jednym kliknięciem.",
              "Zlecenia prywatne: najpierw kosztorys (AI albo wgrany własny), potem oferta dla klienta w Wordzie i umowa o roboty budowlane."]),
            ("Materiały, hurtownie, zamówienia", "Zakupy materiałów prosto z kosztorysu.",
             ["Zapotrzebowanie materiałowe wyliczone z kosztorysu, z ilościami i cenami.",
              "Harmonogram i podział dostaw na etapy robót.",
              "Zapytania ofertowe i zamówienia do wybranych hurtowni – każda dostaje tylko swój asortyment; szkice e-maili albo wysyłka z Twojej skrzynki."]),
            ("Budowa w realizacji", "Kontrola terminów, pieniędzy i jakości na każdej budowie.",
             ["Umowa, harmonogram rzeczowo-finansowy (HRF), protokoły odbioru etapów w Wordzie.",
              "Faktury wystawione z terminami płatności, koszty budowy, robocizna; wynik bieżący i prognozowany, rozliczenie w Excelu.",
              "Raporty dzienne (dziennik pomocniczy) uzupełniane automatycznie: pogoda, pracownicy, materiały, zdjęcia; wydruk w Wordzie.",
              "Zdjęcia z telefonu, usterki i zadania z terminami i osobami odpowiedzialnymi, notatki i raport projektu w Wordzie.",
              "Monitoring pogody z najbliższej stacji IMGW, ocena dni w godzinach pracy według progów dla rodzaju robót.",
              "Podwykonawcy: zakres prac, umowy, faktury i zapłaty, zgłoszenie podwykonawcy zamawiającemu, oświadczenia podwykonawców o rozliczeniu i oświadczenie o niezaleganiu do rozliczenia z zamawiającym."]),
            ("Zmiany umowy i roszczenia", "Udokumentowane wnioski zamiast straconych pieniędzy i kar.",
             ["a) prace dodatkowe, b) błędy dokumentacji przetargowej (automatyczny wykaz błędów po zawarciu umowy), c) inne przeszkody – konserwator zabytków, wstrzymanie robót przez organ, okres lęgowy, znaleziska, kolizje z infrastrukturą.",
              "AI proponuje uzasadnienie, zakres prac, kosztorys (kwota dla zamawiającego) i liczbę dni przedłużenia – wszystko do edycji.",
              "Wniosek do zamawiającego w Wordzie; po akceptacji aneks do umowy z kosztorysem, aktualizacja terminu, wynagrodzenia i harmonogramu.",
              "Pismo o niekorzystnych warunkach atmosferycznych i wniosek o przedłużenie terminu z tabelą dni i danymi stacji IMGW."]),
            ("Firma, ludzie i dokumenty", "Porządek w sprawach firmy.",
             ["Klienci z danymi pobieranymi po NIP (wykaz VAT, CEIDG), historia i uwagi.",
              "Pracownicy i ewidencja roboczogodzin (z edycją wpisów), rozliczenie miesięczne.",
              "Kadry: umowy, badania lekarskie, szkolenia BHP, uprawnienia, SEP, UDT – z przypomnieniami o kończących się terminach.",
              "Płace: umowa o pracę, zlecenie, dzieło; składki ZUS, zaliczka PIT, PPK, koszt pracodawcy; lista płac w Excelu.",
              "Profil firmy z logo w nagłówkach dokumentów, certyfikaty, referencje i polisa OC z terminami ważności."]),
        ],
        "proces": ["Program codziennie znajduje przetargi w Twoim obszarze i ocenia je.",
                   "Otwierasz przetarg, czytasz analizę i decydujesz: startujemy.",
                   "„Przygotuj ofertę” – dokumenty pobierają się same, AI przygotowuje kosztorys i formularze.",
                   "Sprawdzasz kosztorys, dopasowujesz cenę, tworzysz komplet dokumentów i składasz ofertę.",
                   "Po wygranej: harmonogram, zamówienia materiałów, dziennik, odbiory, faktury.",
                   "Gdy pojawiają się prace dodatkowe lub przestoje – wniosek z kosztorysem, a po akceptacji aneks."],
        "korzysci": [("Więcej ofert w tym samym czasie", "Analiza przetargu i kosztorys w minutach zamiast dni – możesz startować w większej liczbie postępowań."),
                     ("Mniej przegapionych szans i terminów", "Nowe przetargi – także szpitali, uczelni i dużych spółek – widać od razu po zalogowaniu i w codziennym powiadomieniu."),
                     ("Cena dopasowana do konkurencji", "Kalkulator szans pokazuje, przy jakiej cenie oferta realnie wygrywa."),
                     ("Lepiej policzone oferty", "Ceny rynkowe, kontrola kosztorysu i wykrywanie błędów dokumentacji ograniczają ryzyko straty."),
                     ("Pieniądze za prace dodatkowe", "Gotowe, uzasadnione wnioski i aneksy z kosztorysem zamiast sporów „na słowo”."),
                     ("Wynik każdej budowy na bieżąco", "Faktury, koszty i robocizna w jednym miejscu – wiesz, która budowa zarabia."),
                     ("Firma w telefonie", "Dziennik, zdjęcia, usterki i roboczogodziny prosto z placu budowy.")],
        "zdjecia": [("90_wyszukiwarka", "Wyszukiwarka w trzech krokach"), ("02_przetargi", "Przetargi z oceną AI"), ("07_krok2", "Oferta i kosztorys"), ("84_wnioski", "Zmiany umowy: wnioski i aneksy"),
                    ("80_pogoda", "Monitoring pogody i wniosek o przedłużenie terminu")],
        "pytania": [("Czy AI składa ofertę za mnie?", "Nie. Program przygotowuje dokumenty i wyliczenia, a Ty je sprawdzasz, poprawiasz i zatwierdzasz."),
                    ("Czy muszę mieć przedmiar?", "Nie zawsze – kosztorys powstanie także z projektu, rysunków lub opisu zakresu, z pokazanymi obliczeniami ilości."),
                    ("Czy dane mojej firmy są widoczne dla innych?", "Nie. Każde konto to osobna firma z własnymi danymi.")],
    },
    "dostawca": {
        "tytul": "Dla Dostawcy / Usługodawcy", "krotko": "Dostawy i usługi",
        "kto": ["firmy dostarczające towary: sprzęt, meble, komputery, materiały, środki czystości, paliwa, żywność, wyroby medyczne",
                "firmy usługowe: sprzątanie, ochrona, transport, odbiór odpadów, serwis i konserwacja, utrzymanie zieleni, catering",
                "dostawcy szpitali, uczelni, urzędów i dużych spółek – w przetargach i zapytaniach ofertowych"],
        "kolor": "#1F5A99", "haslo": "Przetargi na dostawy i usługi znalezione, przeanalizowane i wycenione w jednym miejscu – a po wygranej pełne rozliczenie umowy.",
        "wyzwania": [
            ("Przetargi na dostawy i usługi są rozproszone: BZP, platformy szpitali, uczelni i spółek, zapytania ofertowe.",
             "Jedna wyszukiwarka dla dostaw i usług – BZP, Baza Konkurencyjności oraz strony szpitali, uczelni, urzędów i dużych spółek w Twoim obszarze."),
            ("SWZ, OPZ i formularz asortymentowo-cenowy trzeba przeczytać, żeby wiedzieć, co dokładnie zaoferować.",
             "Analiza przetargu: co zaoferować (pozycje i ilości wpisane od razu do formularza), terminy, kryteria i błędy w dokumentach z gotowymi pytaniami do zamawiającego."),
            ("Formularz ofertowy i oświadczenia różnią się w każdym postępowaniu.",
             "Formularz ofertowy i oświadczenia przygotowane według wzorów z SWZ – tylko te, których wymaga zamawiający; Ty wpisujesz wyłącznie ceny jednostkowe."),
            ("Po wygranej trudno śledzić dostawy sukcesywne, odbiory, faktury i terminy płatności.",
             "Realizacja umów: zamówienia i dostawy, wykorzystanie pozycji umowy, protokoły odbioru, faktury, wezwania do zapłaty, reklamacje i kary."),
        ],
        "moduly": [
            ("Przetargi na dostawy i usługi", "Tylko to, co sprzedajesz.",
             ["Wyszukiwarka w trzech krokach z gotowymi zestawami: sprzątanie, paliwa, środki czystości, sprzęt IT, transport, żywność, odpady, meble, ochrona i serwis.",
              "Szpitale, uczelnie, urzędy, duże spółki (KGHM, Orlen, PGE, Tauron, PKP) i spółki komunalne – strony przetargowe znajdowane automatycznie.",
              "Rodzaj zamówienia z ogłoszenia: dostawca widzi dostawy i usługi, bez robót budowlanych.",
              "Ocena dopasowania do profilu Twojej firmy i codzienne powiadomienia o nowych przetargach.",
              "Wszystkie ogłoszenia z BZP każdego dnia, ze wstępnym sitem bez AI – do oceny trafiają najpierw najlepiej pasujące."]),
            ("Oferta w pięciu krokach", "Od dokumentów do kompletu do złożenia.",
             ["1. Dokumenty przetargu pobierane jednym kliknięciem.",
              "2. Analiza przetargu i błędów w dokumentach – z pytaniami do zamawiającego.",
              "3. Formularz cenowy: pozycje i ilości wpisane przez program, Ty podajesz tylko ceny jednostkowe netto; sumy, VAT i sprawdzenie cen rynkowych w internecie.",
              "4. Dokumenty wykonawcy (KRS, polisa, referencje, certyfikaty) z profilu firmy.",
              "5. Złożenie oferty: termin, miejsce, lista kontrolna wymaganych dokumentów i ZIP gotowy do wysłania."]),
            ("Załączniki według ogłoszenia", "Właściwe dokumenty, a nie szablony.",
             ["Formularz ofertowy i oświadczenia przepisane z wzorów SWZ, z numeracją załączników i danymi firmy.",
              "Osobna lista: dokumenty do dołączenia (certyfikaty, karty produktów) i składane dopiero na wezwanie.",
              "Formularz cenowy w Excelu i formularze w Wordzie."]),
            ("Realizacja umów", "Rozliczenie wygranego przetargu.",
             ["Umowa: wartość, okres, termin płatności, kara za zwłokę, gwarancja, zabezpieczenie i jego zwrot.",
              "Dostawy sukcesywne i jednorazowe: zamówienia z ilościami, wartość z Twoich cen, wykorzystanie pozycji umowy; usługi: miesięczne okresy rozliczeniowe.",
              "Protokoły odbioru, faktury z terminami płatności, wezwania do zapłaty, reklamacje i gwarancja.",
              "Ostrzeżenia: opóźnione dostawy z szacowaną karą, faktury po terminie, koniec umowy; rozliczenie końcowe w Excelu."]),
        ],
        "proces": ["Ustawiasz, czego szukasz, gdzie i u kogo – program codziennie znajduje przetargi na dostawy i usługi.",
                   "Otwierasz przetarg: analiza mówi, co zaoferować, do kiedy i jakie są błędy w dokumentach.",
                   "Wpisujesz ceny jednostkowe – program liczy formularz, przygotowuje formularz ofertowy i oświadczenia według SWZ.",
                   "Kompletujesz dokumenty i składasz ofertę z gotowego ZIP.",
                   "Po wygranej: zamówienia, odbiory, faktury i płatności w module Realizacja umów."],
        "korzysci": [("Więcej ofert w dostawach i usługach", "Wyszukiwanie, analiza i formularze w minutach – starczy czasu na więcej postępowań."),
                     ("Nowi klienci instytucjonalni", "Szpitale, uczelnie i duże spółki ogłaszające przetargi poza BZP – w jednej liście."),
                     ("Bez błędów w formularzach", "Wartości liczone automatycznie, a załączniki zgodne z wzorami zamawiającego."),
                     ("Pieniądze na czas", "Terminy płatności, faktury po terminie i wezwania do zapłaty pod kontrolą."),
                     ("Bez kar umownych", "Opóźnione dostawy i reklamacje widoczne z wyprzedzeniem.")],
        "zdjecia": [("91_dostawca", "Wyszukiwarka dostaw i usług"), ("93_realizacja_umowy", "Realizacja umowy: dostawy, faktury, kary")],
        "pytania": [("Czy program sam ustala ceny?", "Nie – ceny jednostkowe wpisujesz Ty; program liczy wartości i porównuje je z cenami rynkowymi."),
                    ("Czy obsługuje dostawy sukcesywne?", "Tak – zamówienia częściowe, wykorzystanie pozycji umowy, odbiory i faktury do każdej dostawy."),
                    ("Czy widzę też roboty budowlane?", "Nie – w trybie Dostawcy są dostawy i usługi; roboty budowlane są w trybie Wykonawcy.")],
    },
    "zamawiajacy": {
        "tytul": "Dla Zamawiającego", "krotko": "Gminy, urzędy, wspólnoty",
        "kto": ["gminy, starostwa, urzędy i jednostki organizacyjne samorządu",
                "szkoły, szpitale, instytucje kultury i spółki komunalne",
                "wspólnoty i spółdzielnie mieszkaniowe oraz firmy zlecające roboty budowlane",
                "beneficjenci projektów unijnych stosujący zasadę konkurencyjności"],
        "kolor": "#1F5A99", "haslo": "Przetargi na roboty budowlane, usługi i dostawy przygotowane szybciej i lepiej – mniej pytań i zmian umów, pełna kontrola realizacji.",
        "wyzwania": [
            ("Ustalenie wartości zamówienia wymaga kosztorysu inwestorskiego, a czasu i ludzi jest mało.",
             "Kosztorys inwestorski przygotowany na podstawie projektu i przedmiaru, z kontrolą braków i nierealnych cen."),
            ("Sprzeczności między SWZ, OPZ, przedmiarem i wzorem umowy wychodzą dopiero w pytaniach wykonawców albo na budowie.",
             "Sprawdzenie dokumentacji przed publikacją: sprzeczności, braki, zapisy ryzykowne i niezgodne z Pzp – z propozycją poprawionego zapisu."),
            ("Przygotowanie SWZ, zapytania, formularzy i wzoru umowy dla każdego postępowania od nowa.",
             "Dokumenty postępowania sporządzane według Twoich wymagań: trybu, terminów, wadium, kryteriów, kar i zabezpieczenia."),
            ("Zamówienia na usługi i dostawy wymagają innych dokumentów i innego szacowania wartości niż roboty budowlane.",
             "Wybierasz rodzaj zamówienia – roboty budowlane, usługi albo dostawy – a program przygotowuje szacowanie, OPZ, formularz i umowę właściwe dla tej dziedziny."),
            ("Badanie złożonych ofert, wezwania do uzupełnień i wyliczanie punktów to dni pracy komisji.",
             "Sprawdzenie ofert: kompletność, zgodność z SWZ, błędy rachunkowe i rażąco niska cena; punktacja według kryteriów, ranking i protokół."),
            ("Po podpisaniu umowy trudno śledzić harmonogram, odbiory, faktury i usterki.",
             "Zarządzanie inwestycją: umowa z wykonawcą, harmonogram, protokoły, faktury, dziennik, zdjęcia, usterki i raport."),
        ],
        "moduly": [
            ("Trzy rodzaje zamówień", "Przetarg przygotowany dla danej dziedziny.",
             ["Roboty budowlane – kosztorys inwestorski, OPZ z zakresem robót, umowa o roboty budowlane.",
              "Usługi (sprzątanie, ochrona, utrzymanie zieleni i dróg, projektowanie, nadzór, transport, IT) – szacowanie wartości usług, OPZ z częstotliwością i standardem, umowa z klauzulami zatrudnienia i waloryzacji.",
              "Dostawy towarów (sprzęt, meble, komputery, materiały, paliwo, energia) – formularz asortymentowo-cenowy, OPZ z parametrami i równoważnością, umowa dostawy z gwarancją i serwisem.",
              "Sprawdzenie dokumentacji dopasowane do rodzaju zamówienia."]),
            ("Kosztorys inwestorski", "Wartość zamówienia na podstawie dokumentacji.",
             ["Kosztorys z projektu, przedmiaru, opisu technicznego i STWiORB – z cenami rynkowymi.",
              "Kontrola kosztorysu: braki, nierealne ceny, ilości; asystent odpowiadający na pytania do dokumentacji z cytatami.",
              "Plik Excel do dołączenia do dokumentacji postępowania."]),
            ("Sprawdzenie dokumentacji przetargowej", "Błędy wychwycone przed publikacją, a nie po niej.",
             ["Porównanie SWZ, OPZ, przedmiaru, projektowanych postanowień umowy i formularzy między sobą.",
              "Sprzeczności terminów, wadium, zakresu, gwarancji, kryteriów; błędy rachunkowe i odwołania; brakujące elementy.",
              "Zapisy ryzykowne lub niezgodne z ustawą Pzp i zasadą konkurencyjności (np. nazwy produktów bez „lub równoważne”, kary bez limitu).",
              "Każda uwaga z wagą (krytyczna, istotna, drobna), cytatem, miejscem i propozycją poprawionego zapisu; raport w Wordzie."]),
            ("Sporządzanie dokumentacji postępowania", "Spójne dokumenty w krótkim czasie.",
             ["SWZ w trybie podstawowym, zapytanie ofertowe w zasadzie konkurencyjności, zapytanie poniżej progu Pzp (170 tys. zł), zapytanie wspólnoty.",
              "Opis przedmiotu zamówienia, formularz ofertowy z oświadczeniami, projektowane postanowienia umowy.",
              "Według Twoich wymagań: terminy, wadium, warunki udziału, kryteria z wagami, gwarancja, płatności, kary, zabezpieczenie.",
              "Wszystkie dokumenty postępowania, kosztorys i weryfikacja w jednym projekcie zamówienia.",
              "Kreator uzupełniany z dokumentów, które już masz – także z archiwów ZIP z przedmiarem: wartość, tryb, zakres i ilości, przy każdym polu źródło; pliki, których nie da się odczytać, są wypisane.",
              "Kontrola trybu: tryb wskazany w dokumentach porównany z wartością zamówienia i progami (170 tys. zł, progi unijne) – rozbieżności pokazane do Twojej decyzji.",
              "Dane zamawiającego wpisujesz Ty – program nie podstawia ich sam; miejsca do uzupełnienia są oznaczone na żółto."]),
            ("Sprawdzenie złożonych ofert", "Badanie, ocena i ranking ofert w jednym miejscu.",
             ["Kryteria oceny, wagi, wymagane dokumenty i warunki udziału odczytane z SWZ.",
              "Każda oferta zbadana z SWZ i OPZ: kompletność, niezgodności, błędy rachunkowe, wadium, termin związania – status prawidłowa / do uzupełnienia / do wyjaśnienia / do odrzucenia.",
              "Wykrywanie możliwej rażąco niskiej ceny (art. 224 Pzp) i przekroczenia kwoty zamawiającego.",
              "Punktacja według wzorów z SWZ, ranking i wskazanie najkorzystniejszej oferty spośród ofert bez zastrzeżeń.",
              "Wezwania do wyjaśnień i uzupełnień, protokół z badania i oceny ofert oraz informacja o wyborze (art. 253) w Wordzie."]),
            ("Zarządzanie inwestycją", "Nadzór nad realizacją umowy – aż do ogłoszenia o wykonaniu umowy.",
             ["Umowa z wykonawcą (dane po NIP), harmonogram rzeczowo-finansowy z działów kosztorysu.",
              "Protokoły odbioru etapów, faktury wykonawcy do zapłaty, inne koszty inwestycji.",
              "Dziennik z pogodą, zdjęcia, usterki z terminami, notatki i raport inwestycji w Wordzie.",
              "Rejestr podwykonawców wykonawcy i wezwania do przedstawienia oświadczeń o rozliczeniu z podwykonawcami przed zapłatą faktury lub etapu."]),
        ],
        "proces": ["Wybierasz rodzaj zamówienia: roboty budowlane, usługi albo dostawy.",
                   "Wgrywasz projekt, przedmiar, opis potrzeb albo wykaz towarów – powstaje kosztorys inwestorski lub szacowanie wartości zamówienia.",
                   "Wpisujesz wymagania – program sporządza SWZ lub zapytanie, OPZ, formularz i wzór umowy.",
                   "Przed publikacją program sprawdza całą dokumentację i proponuje poprawki.",
                   "Po otwarciu ofert program bada każdą ofertę, liczy punkty, układa ranking i przygotowuje protokół.",
                   "Po wyborze wykonawcy prowadzisz inwestycję: harmonogram, odbiory, faktury, usterki."],
        "korzysci": [("Mniej pytań, odwołań i unieważnień", "Spójna dokumentacja bez sprzeczności ogranicza ryzyka postępowania."),
                     ("Szybsze przygotowanie postępowań", "Dokumenty powstają według Twoich wymagań, a nie od zera."),
                     ("Mniej zmian umów i roszczeń", "Błędy dokumentacji wychwycone przed publikacją nie wracają jako prace dodatkowe."),
                     ("Szybsza i bezpieczniejsza ocena ofert", "Badanie ofert, punktacja i protokół w godzinach zamiast dni – z podstawami prawnymi wezwań."),
                     ("Kontrola budżetu i terminów", "Harmonogram, odbiory i faktury inwestycji w jednym miejscu."),
                     ("Pełna dokumentacja inwestycji", "Wszystko zapisane, z archiwum zamiast usuwania – przydatne przy kontrolach i rozliczeniach dotacji.")],
        "zdjecia": [("92_ocena_ofert", "Sprawdzenie ofert: ranking i wybór"), ("87_zam_nowe", "Nowe zamówienie: roboty, usługi, dostawy"), ("41_weryfikacja", "Sprawdzenie dokumentacji przetargowej"), ("42_dokumentacja", "Sporządzanie dokumentacji postępowania"),
                    ("43_inwestycja", "Zarządzanie inwestycją"), ("zm_kreator", "Kreator uzupełniony z dokumentów: źródła pól i wybór przy sprzecznościach")],
        "pytania": [("Czy dokumenty są gotowe do publikacji bez sprawdzenia?", "Nie – to projekty przygotowane z pomocą AI; przed publikacją sprawdza je osoba odpowiedzialna za postępowanie."),
                    ("Czy program obsługuje zamówienia poniżej progów Pzp?", "Tak – zapytania ofertowe poniżej progu Pzp (170 tys. zł), zasadę konkurencyjności i zapytania wspólnot.")],
    },
    "inwestor": {
        "tytul": "Dla Inwestora indywidualnego", "krotko": "Budowa własnego domu",
        "kto": ["osoby budujące dom jednorodzinny z wykonawcami",
                "inwestorzy budujący częściowo systemem gospodarczym",
                "osoby planujące rozbudowę lub generalny remont domu"],
        "kolor": "#1F5A99", "haslo": "Twoja budowa pod kontrolą: koszty, terminy, wykonawcy i formalności w jednym miejscu – także w telefonie.",
        "wyzwania": [
            ("Nie wiadomo, ile naprawdę będzie kosztować dom, a oferty wykonawców trudno porównać.",
             "Kosztorys budowy z projektu i pusty kosztorys do wyceny – każdy wykonawca wycenia te same pozycje."),
            ("Budżet rozjeżdża się w trakcie budowy, a wydatki są rozrzucone po paragonach i fakturach.",
             "Budżet z kosztorysu kontra wszystkie wydatki, z paskiem wykorzystania i ostrzeżeniem o przekroczeniu."),
            ("Formalności, odbiory i transze kredytu łatwo przeoczyć.",
             "Lista formalności od pozwolenia do zakończenia budowy, protokoły odbioru etapów i transze kredytu ze statusami."),
        ],
        "moduly": [
            ("Projekt domu i kosztorys", "Wiesz, ile kosztuje budowa, zanim ją zaczniesz.",
             ["Kosztorys z projektu według etapów: roboty ziemne, stan zero, stan surowy otwarty, dach, stan surowy zamknięty, instalacje, tynki i elewacja, stan deweloperski, przyłącza.",
              "Udział materiału w pozycjach – pomocny przy budowie systemem gospodarczym; pytania do decyzji (ogrzewanie, standard).",
              "Wczytanie własnego kosztorysu od projektanta lub kosztorysanta.",
              "Pusty kosztorys dla wykonawców – ślepy kosztorys w Excelu, w którym wykonawca wpisuje ceny, a sumy liczą się same."]),
            ("Materiały i hurtownie", "Zakupy bez chaosu.",
             ["Lista materiałów z kosztorysu, harmonogram dostaw na etapy budowy.",
              "Zapytania ofertowe i zamówienia do hurtowni – szkic e-maila albo wysyłka z Twojej skrzynki."]),
            ("Budowa krok po kroku", "Etapy, odbiory i dokumentacja budowy.",
             ["Harmonogram budowy z etapami i wartościami.",
              "Protokoły odbioru etapów z wybranym wykonawcą (Ty jako zamawiający), z usterkami i terminem ich usunięcia.",
              "Raporty dzienne z pogodą, zdjęcia z telefonu, usterki i zadania, notatki, raport budowy w Wordzie.",
              "Wykonawcy i ekipy z zakresem, kontaktem i kwotą umowy; faktury przypisane do wykonawców."]),
            ("Budżet, kredyt i formalności", "Nic nie umyka.",
             ["Budżet brutto z kosztorysu, wydatki razem, pozostała kwota, faktury do zapłaty i po terminie.",
              "Transze kredytu z warunkiem wypłaty (np. stan surowy zamknięty), planowaną datą i statusem.",
              "13 formalności: mapa i warunki zabudowy, pozwolenie lub zgłoszenie, dziennik i kierownik budowy, geodeta, przyłącza, odbiory kominiarskie, pomiary, świadectwo energetyczne, zakończenie budowy, podatek."]),
        ],
        "proces": ["Wgrywasz projekt domu – powstaje kosztorys budowy według etapów.",
                   "Wysyłasz wykonawcom pusty kosztorys i porównujesz ich oferty pozycja po pozycji.",
                   "„Rozpocznij budowę” – harmonogram etapów, budżet i lista formalności gotowe.",
                   "Na bieżąco: odbiory etapów, faktury, zdjęcia, dziennik, transze kredytu."],
        "korzysci": [("Znasz koszt budowy", "Kosztorys z projektu i budżet kontra wydatki w każdej chwili."),
                     ("Porównywalne oferty wykonawców", "Wszyscy wyceniają te same pozycje i ilości."),
                     ("Spokój z formalnościami", "Lista spraw urzędowych i odbiorów ze statusami i datami."),
                     ("Dokumentacja na lata", "Protokoły, zdjęcia i faktury przydatne przy gwarancji, sporach i rozliczeniu kredytu."),
                     ("W telefonie na budowie", "Zdjęcia, usterki i wydatki dodajesz od razu, na miejscu.")],
        "zdjecia": [("71_pulpit_inw", "Pulpit inwestora"), ("73_budzet", "Budżet budowy"), ("75_formalnosci", "Formalności budowy")],
        "pytania": [("Czy muszę znać się na kosztorysowaniu?", "Nie – kosztorys powstaje z projektu, a program wyjaśnia pozycje i pokazuje, gdzie trzeba podjąć decyzję."),
                    ("Czy mogę budować systemem gospodarczym?", "Tak – w kosztorysie widać udział materiału, a zakupy prowadzisz przez moduł hurtowni.")],
    },
    'rzeczoznawca': {'tytul': 'Dla rzeczoznawcy',
     'krotko': 'Rzeczoznawcy majątkowi',
     'kto': ['rzeczoznawcy majątkowi sporządzający operaty szacunkowe – do sprzedaży, zabezpieczenia kredytu, podziału majątku, aktualizacji opłat i ubezpieczenia',
             'biura wycen i kancelarie współpracujące z rzeczoznawcami',
             'zespoły due diligence i analizy nieruchomości przygotowujące materiał dla rzeczoznawcy'],
     'kolor': '#7c3aed',
     'haslo': 'Teczka nieruchomości, przeznaczenie z rejestru planów, dobór transakcji i projekt operatu do Twojej weryfikacji – mniej przepisywania, więcej czasu na ocenę.',
     'wyzwania': [('Ustalenie działki, budynku i przeznaczenia to godziny w kilku serwisach i przepisywanie danych.',
                   'Identyfikacja z usług GUGiK: granice, powierzchnia, obręb, budynek z ewidencji z powierzchnią zabudowy – oraz plan miejscowy z państwowego rejestru planów '
                   '(uchwała, data, link do rysunku).'),
                  ('Wyciąg z rejestru cen trzeba ręcznie przesiać, a każde odrzucenie uzasadnić.',
                   'Wgrywasz wyciąg (Excel, CSV, PDF) – program wstępnie wyklucza transakcje nietypowe, innego rodzaju lub o innej powierzchni, z uzasadnieniem dla każdej grupy; '
                   'każdą możesz przywrócić.'),
                  ('Za mało transakcji na rynku lokalnym.',
                   'Karta podpowiedzi: wniosek do starostwa o wyciąg (Word), poszerzenie rynku, porównywanie parami, podejście kosztowe, dochodowe albo metoda pozostałościowa.'),
                  ('Operat powstaje od zera, a każdą liczbę trzeba sprawdzić.',
                   'Projekt operatu w Wordzie z oznaczeniem PROJEKT – wszystko, co wymaga Twojego potwierdzenia, jest wyróżnione na żółto; wersja do podpisu dopiero po zatwierdzeniu '
                   'punktów kontrolnych.'),
                  ('Aktualizacja operatu i kolejne wyceny tej samej nieruchomości.',
                   'Aktualizacja z nową datą wyceny w tej samej teczce – poprzednia wycena w archiwum, założenia i dane zostają.')],
     'moduly': [('Teczka nieruchomości',
                 'Dane zebrane raz – do wyceny, due diligence i analizy zabudowy.',
                 ['Działka, dom, mieszkanie albo lokal użytkowy; identyfikacja po numerze TERYT, obrębie i numerze albo adresie.',
                  'Gdy ten sam obręb i numer są w kilku gminach – lista do wyboru; program nie zgaduje.',
                  'Adres z państwowego rejestru adresów; gdy trafienie jest tylko w ulicę – wyraźne ostrzeżenie „lokalizacja przybliżona”.',
                  'Nieruchomość z kilku działek: suma powierzchni, rysunek granic, ostrzeżenie przy różnych księgach i działkach niestykających się.',
                  'Dokumenty: odpis księgi wieczystej czytany dział po dziale, wypisy, decyzje, umowy – z odwołaniem do miejsca w dokumencie.',
                  'Oględziny z listą kontrolną i zdjęciami; dziennik zmian – kto, kiedy i co zmienił.']),
                ('Przeznaczenie – plan miejscowy',
                 'Rejestr planów i wypis mają pierwszeństwo przed wyszukiwaniem.',
                 ['Państwowy rejestr aktów planowania: tytuł planu, numer i data uchwały, data obowiązywania, status, linki do rysunku i danych planu, a przy planach wektorowych '
                  'symbol i przeznaczenie terenu.',
                  'Symbol z wypisu odczytany przez AI; wypis wgrany do teczki ma status „potwierdzone”.',
                  'Inna uchwała albo inny symbol z wyszukiwania w internecie – pokazane jako różnica do Twojej decyzji, bez nadpisywania danych z rejestru.',
                  'Plan ogólny gminy, jeśli już obowiązuje; ryzyka: droga publiczna na części działki, opłata planistyczna, brak planu.']),
                ('Transakcje i metody wyceny',
                 'Podejście dopasowane do danych, które masz.',
                 ['Dobór podobnych transakcji (rodzaj, powierzchnia, przeznaczenie) z uzasadnieniem wykluczeń; trend cen na datę wyceny.',
                  'Porównawcze: korygowanie ceny średniej (cechy, wagi, ocena przedmiotu) i porównywanie parami; analiza wrażliwości wyniku.',
                  'Kosztowe (grunt + koszt odtworzenia − zużycie), dochodowe – kapitalizacja prosta (czynsze z ofert najmu jako analiza rynku), metoda pozostałościowa ze scenariusza '
                  'zabudowy.',
                  'Wskaźniki szacunkowe gruntów rolnych i leśnych – wskaźniki i cenę wpisujesz Ty; program ich nie zakłada.',
                  'Ustawienia rzeczoznawcy: minimalna liczba transakcji, korekty, koszty odtworzenia i uzasadnienie założeń trafiające do operatu.']),
                ('Projekt operatu',
                 'Ty decydujesz – program przygotowuje.',
                 ['Siedem punktów kontrolnych zatwierdzanych po kolei: zakres i cel, stan prawny i powierzchnie, oględziny, zbiór transakcji, podejście i metoda, cechy i obliczenia, '
                  'operat.',
                  'Na żółto: teksty przygotowane przez AI, założenia, dane wstępne i braki [UZUPEŁNIJ]; po zatwierdzeniu punktu wyróżnienia znikają.',
                  'Kontrola kompletności i spójności; projekt operatu w Wordzie i wersja do podpisu – bez wyróżnień, po zatwierdzeniu wszystkich punktów.',
                  'Zmiana w teczce po zatwierdzeniu oznacza zależne punkty do ponownego potwierdzenia; uzasadnienia zatwierdzeń mimo zastrzeżeń trafiają do operatu.']),
                ('Due diligence i analiza zabudowy',
                 'Dla zleceń wykraczających poza samą wycenę.',
                 ['Ryzyka z wagą, statusem, źródłem i kosztem usunięcia; pisma do gminy, konserwatora, gestorów sieci i zarządcy drogi w Wordzie.',
                  'Raport due diligence z rekomendacją i warunkami do umowy przedwstępnej.',
                  'Analiza zabudowy: obszar, na którym wolno stawiać budynki, scenariusze zabudowy i maksymalna cena działki.',
                  'Wstępny szacunek klienta z danych rynkowych może trafić do Ciebie w tej samej teczce – oferty zostają jako analiza rynku, nie podstawa operatu.'])],
     'proces': ['Zakładasz teczkę: adres, numer działki albo obręb i numer.',
                'Program pobiera granice, powierzchnię, budynek z ewidencji i plan miejscowy z rejestru planów.',
                'Wgrywasz odpis księgi wieczystej, wypis z planu i wyciąg z rejestru cen.',
                'Dobierasz transakcje i metodę – program liczy, Ty sprawdzasz i poprawiasz.',
                'Zatwierdzasz punkty kontrolne; wyróżnienia pokazują, co jeszcze wymaga potwierdzenia.',
                'Pobierasz projekt operatu w Wordzie, a po zatwierdzeniu wszystkiego – wersję do podpisu.'],
     'korzysci': [('Mniej przepisywania', 'Dane z rejestrów państwowych i dokumentów trafiają do teczki i operatu bez ręcznego przepisywania.'),
                  ('Decyzja zawsze po Twojej stronie', 'Nic nie trafia do wersji do podpisu bez Twojego zatwierdzenia; założenia i dane wstępne są wyróżnione.'),
                  ('Uzasadnienia gotowe do operatu', 'Każde wykluczenie transakcji, korekta i odstępstwo ma zapisane uzasadnienie.'),
                  ('Kolejne wyceny szybciej', 'Aktualizacja operatu i nowa wycena w tej samej teczce, z archiwum wycen.')],
     'zdjecia': [('rz_plan', 'Przeznaczenie z planu miejscowego: symbol, uchwała, status'),
                 ('rz_wycena', 'Wycena: punkty kontrolne rzeczoznawcy'),
                 ('rz_brak', 'Za mało transakcji – podpowiedzi'),
                 ('rz_zabudowa', 'Analiza zabudowy i maksymalna cena działki')],
     'pytania': [('Czy program sporządza operat za rzeczoznawcę?',
                  'Nie. Operat sporządza i podpisuje rzeczoznawca majątkowy po osobistych oględzinach. Program przygotowuje projekt i obliczenia do Twojej weryfikacji, a wersję do '
                  'podpisu wydaje dopiero po zatwierdzeniu wszystkich punktów kontrolnych.'),
                 ('Skąd pochodzą transakcje?',
                  'Z wyciągu z rejestru cen, który wgrywasz (Excel, CSV albo PDF). Oferty rynkowe służą wyłącznie do analizy rynku i kontroli wyniku – nie są podstawą operatu.'),
                 ('Czy przeznaczenie z mapy wystarczy?',
                  'Dane z rejestru planów to dobry punkt wyjścia, ale w operacie decyduje wypis z planu – po jego wgraniu przeznaczenie ma status „potwierdzone” i pierwszeństwo przed '
                  'innymi źródłami.')]},
    'dotacje': {'tytul': 'Dotacje UE/KPO',
     'krotko': 'Firmy, gminy, rolnicy, organizacje',
     'kto': ['mikro, małe, średnie i duże przedsiębiorstwa',
             'gminy, powiaty i ich jednostki, szkoły i instytucje kultury',
             'wspólnoty mieszkaniowe, organizacje pozarządowe i rolnicy',
             'doradcy przygotowujący wnioski i rozliczenia dla klientów'],
     'kolor': '#db2777',
     'haslo': 'Właściwy nabór, kompletny wniosek i rozliczenie bez zgubionych dokumentów – od wyszukania dotacji po okres trwałości projektu.',
     'wyzwania': [('Nabory są rozproszone po portalach województw, KPO, programach krajowych i funduszach ochrony środowiska.',
                   'Wyszukiwarka według branży, regionu i rodzaju wnioskodawcy: lista naborów z portalu Funduszy Europejskich województwa i programy krajowe, z oceną dopasowania '
                   '1–10.'),
                  ('Termin naboru łatwo przegapić.', 'Nadchodzące nabory z harmonogramów województw i instytucji oraz alerty e-mail z przypomnieniem przed startem naboru.'),
                  ('Regulamin ma dziesiątki stron, a o wyniku decydują punkty.',
                   'Program czyta regulamin: kryteria dostępu, kryteria oceny z punktami i wskazówkami, koszty kwalifikowalne i najczęstsze błędy; szacuje punkty i podpowiada '
                   'zmiany.'),
                  ('Budżet, intensywność, limity i wskaźniki trzeba policzyć bez błędu.',
                   'Pozycje projektu, budżet z intensywnością i limitami, wkład własny i wskaźniki – z ostrzeżeniami i zestawieniem w Excelu.'),
                  ('Rozliczenie: wybór wykonawców, dokumenty, wskaźniki i trwałość.',
                   'Plan rozliczenia z wyborem wykonawcy przy każdej pozycji (zasada konkurencyjności, Pzp), sprawdzeniem dokumentów i kompletem do złożenia.')],
     'moduly': [('Wyszukaj dotację',
                 'Nabory dopasowane do Ciebie.',
                 ['Branża (OZE, termomodernizacja, przemysł, rolnictwo, cyfryzacja, infrastruktura), region i wnioskodawca (MŚP, duże przedsiębiorstwo, JST, wspólnota, NGO, rolnik).',
                  'Wyniki: program i instytucja, status naboru, poziom i kwota dofinansowania, termin, dla kogo, ocena dopasowania z uzasadnieniem, linki do dokumentów.',
                  'Znasz konkretny nabór? Wklejasz link – program odczytuje warunki i pobiera regulamin, wzór wniosku i załączniki.']),
                ('Nadchodzące nabory i alerty',
                 'Wiesz wcześniej niż konkurencja.',
                 ['Zapowiedzi z harmonogramów naborów województw i instytucji pośredniczących, pogrupowane według miesiąca startu.',
                  'Alerty według regionu, branży i wnioskodawcy – e-mail o nowych naborach i przypomnienie przed startem.',
                  '„Przygotuj się do naboru” – wniosek zakładany przed ogłoszeniem.']),
                ('Uzyskaj dotację – wniosek',
                 'Od pomysłu do kompletu do złożenia.',
                 ['Dokumenty naboru pobierane automatycznie, z odrzuceniem dokumentów archiwalnych i dotyczących innego programu.',
                  '„Co chcesz zrobić?” – program wskazuje działania, limity i koszty kwalifikowalne z regulaminu i proponuje pozycje projektu.',
                  'Wycena pozycji z cen rynkowych albo Twoich ofert; roboty budowlane – w module Kosztorysowanie.',
                  'Treść wniosku, opis projektu, biznesplan, budżet, harmonogram i oświadczenia; sprawdzenie zgodności z regulaminem i szacowana punktacja.',
                  'Komplet do złożenia w ZIP; wniosek składasz w systemie wskazanym w regulaminie (np. WOD2021, LSI).']),
                ('Rozliczanie dotacji',
                 'Rozliczenie etapami albo w całości.',
                 ['Plan rozliczenia z wniosku: przy każdej pozycji sposób wyboru wykonawcy – zasada konkurencyjności z gotowym zapytaniem ofertowym, Pzp albo rozeznanie rynku.',
                  'Lista dokumentów do rozliczenia, wgrywanie albo przygotowanie w programie, sprawdzenie kompletności i opisów faktur.',
                  'Wskaźniki – plan i wykonanie; okres trwałości z datami sprawozdań i zakazami.',
                  'Komplet do złożenia z raportem sprawdzenia.'])],
     'proces': ['Wybierasz branżę, region i rodzaj wnioskodawcy – program pokazuje pasujące nabory.',
                'Przy wybranym naborze program pobiera regulamin i dokumenty.',
                'Opisujesz projekt – program ustala, co można sfinansować, liczy budżet i wskaźniki.',
                'Program przygotowuje dokumenty wniosku i sprawdza je z regulaminem.',
                'Po przyznaniu dotacji prowadzisz rozliczenie: wybór wykonawców, dokumenty, wskaźniki, trwałość.'],
     'korzysci': [('Nie przegapisz naboru', 'Wyszukiwarka, harmonogramy i alerty w jednym miejscu.'),
                  ('Wniosek pod punkty', 'Kryteria oceny z regulaminu i podpowiedzi, jak zdobyć punkty.'),
                  ('Rozliczenie bez braków', 'Plan rozliczenia, sprawdzenie dokumentów i komplet do złożenia.')],
     'zdjecia': [('dt_trzy', 'Dotacje UE/KPO: trzy moduły'),
                 ('dt_szukaj', 'Wyszukiwarka dotacji według branży, regionu i wnioskodawcy'),
                 ('dt_wniosek', 'Wniosek: wymagania naboru i dane projektu'),
                 ('dt_spr', 'Sprawdzenie i komplet do złożenia')],
     'pytania': [('Czy program składa wniosek za mnie?', 'Nie. Program przygotowuje dokumenty i komplet do złożenia; wniosek składasz w systemie wskazanym w regulaminie naboru.'),
                 ('Skąd pochodzą informacje o naborach?',
                  'Z portali Funduszy Europejskich województw, harmonogramów naborów i stron programów krajowych. Terminy i warunki zawsze sprawdź na stronie naboru – link jest przy '
                  'każdym wyniku.'),
                 ('Czy pomoże wybrać wykonawcę w projekcie?',
                  'Tak – przy każdej pozycji rozliczenia program proponuje sposób wyboru wykonawcy i przygotowuje zapytanie ofertowe w zasadzie konkurencyjności.')]},
}
WSPOLNE = ["Dokumenty mają pierwszeństwo: gdy dokument i szacunek programu albo dwa źródła się różnią, program pokazuje różnicę do Twojej decyzji – niczego nie zmienia po cichu.",
           "Dane z rejestrów państwowych: Biuletyn Zamówień Publicznych, Platforma e-Zamówienia, ewidencja działek i budynków, rejestr adresów i rejestr planów miejscowych.",
           "Osobny moduł Kosztorysowanie: kosztorys z projektu lub przedmiaru (ceny rynkowe albo własny cennik), poprawki pozycji, wycena materiałów i przeniesienie kosztorysu do modułu wykonawcy, zamawiającego lub inwestora.",
           "Sztuczna inteligencja w codziennej pracy: analiza dokumentów, kosztorysy, pisma i wnioski – zawsze do Twojej weryfikacji.",
           "Działa w przeglądarce na komputerze i telefonie (także jako aplikacja na ekranie telefonu) – bez instalowania.",
           "Każde konto to osobna firma: własne dane, profil, logo w dokumentach; inni użytkownicy nie mają dostępu do Twoich danych.",
           "Dokumenty w Wordzie i Excelu gotowe do wysłania; archiwum zamiast przypadkowego usuwania.",
           "Wygodna nawigacja: pod pozycją menu rozwija się lista sekcji otwartej strony (np. umowa, harmonogram, protokoły, faktury) – jedno kliknięcie przenosi do sekcji.",
           "Interaktywna instrukcja i pomoc AI odpowiadająca na pytania o obsługę programu."]

CSS = """
*{box-sizing:border-box} body{margin:0;font-family:"Plus Jakarta Sans",'DejaVu Sans',Arial,sans-serif;color:#0B1B3A;background:#F4F7FB;line-height:1.55}
.okl{background:#071F49;color:#fff;padding:40px 48px 96px;position:relative;overflow:hidden}
.okl .logo{display:inline-flex;align-items:center;gap:12px;color:#fff;font-size:22px;font-weight:800;letter-spacing:.09em}
.okl .logo svg{height:34px;width:auto}
.okl h1{font-size:38px;line-height:1.1;font-weight:800;margin:28px 0 8px;letter-spacing:-.02em}.okl .pod{font-size:17px;color:#C9D8EA;max-width:780px}
.wybor{max-width:1250px;margin:-64px auto 0;padding:0 24px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;position:relative}
@media screen and (max-width:1100px){.wybor{grid-template-columns:repeat(2,1fr)}}
.wybor button{all:unset;cursor:pointer;background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:22px 22px 18px;box-shadow:0 1px 2px #071f490d,0 6px 20px -10px #071f4924;
  display:flex;flex-direction:column;gap:8px;transition:transform .15s,box-shadow .15s,border-color .15s}
.wybor button:hover{transform:translateY(-2px);border-color:#729BC5;box-shadow:0 2px 6px #071f4914,0 24px 48px -16px #071f4947}
.wybor button.akt{outline:2px solid #071F49;outline-offset:2px}
.wybor .ik{width:48px;height:48px;border-radius:22%;display:grid;place-items:center;background:#E3EDF8;color:#1F5A99}
.wybor .ik svg{width:26px;height:26px}.wybor b{font-size:20px;font-weight:700}.wybor span.o{color:#4B5B74;font-size:14px}
.wybor span.dalej{margin-top:auto;font-weight:700;color:#1F5A99;font-size:14px}
.podpowiedz{max-width:1150px;margin:18px auto 0;padding:0 24px;color:#4B5B74;text-align:center}
.tresc{max-width:1150px;margin:0 auto;padding:10px 24px 10px}
.grupa-oferty{display:none}.grupa-oferty.widoczna{display:block}
.naglowek-gr{background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:22px 24px;margin:26px 0 8px;box-shadow:0 1px 2px #071f490d,0 6px 20px -10px #071f4924}
.naglowek-gr h2{margin:0 0 6px;font-size:26px;border:0;padding:0;color:#0B1B3A}.naglowek-gr .haslo{font-size:17px;font-weight:600;color:#1F5A99}
.naglowek-gr ul{margin:10px 0 0;padding-left:20px;color:#4B5B74}
h2{break-after:avoid;page-break-after:avoid;font-size:21px;font-weight:700;margin:28px 0 10px;color:#0B1B3A;border-left:4px solid #729BC5;padding-left:12px}
h3{font-size:16px;margin:0 0 4px}
.wyzwania{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.wyz{background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:14px 16px;break-inside:avoid}
.wyz .p{color:#B42318;font-size:13.5px}.wyz .p::before{content:"Problem: ";font-weight:800}
.wyz .r{margin-top:6px;font-size:13.5px;color:#17653B}.wyz .r::before{content:"Rozwiązanie: ";font-weight:800}
.moduly{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.modul{background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:16px 18px;break-inside:avoid}
.modul .op{color:#4B5B74;font-size:13.5px;margin:0 0 6px}.modul ul{margin:0;padding-left:18px}.modul li{margin:4px 0;font-size:13.5px}
.proces{counter-reset:k;list-style:none;padding:0;margin:0;display:grid;gap:8px}
.proces li{counter-increment:k;background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:10px 14px 10px 54px;position:relative;font-size:14px;break-inside:avoid}
.proces li::before{content:counter(k);position:absolute;left:12px;top:8px;width:30px;height:30px;border-radius:22%;background:#E3EDF8;color:#1F5A99;
  display:grid;place-items:center;font-weight:800;font-size:14px}
.korzysci{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.korz{background:#fff;border-radius:14px;padding:14px 16px;border:1px solid #DFE6EF;break-inside:avoid}
.korz b{display:block;color:#0B1B3A;margin-bottom:4px}.korz span{font-size:13.5px;color:#4B5B74}
.zdjecia{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.zdjecia figure{margin:0;border:1px solid #DFE6EF;border-radius:14px;overflow:hidden;break-inside:avoid;background:#fff}
.zdjecia img{width:100%;display:block}.zdjecia figcaption{font-size:12px;color:#4B5B74;padding:6px 10px}
.pyt{background:#fff;border:1px solid #DFE6EF;border-radius:14px;padding:12px 16px;margin:8px 0;break-inside:avoid}
.pyt b{display:block}.pyt span{font-size:13.5px;color:#4B5B74}
.wsp{background:#fff;border-radius:14px;padding:14px 18px 14px 34px;border:1px solid #DFE6EF}.wsp li{margin:5px 0;font-size:14px}
.kontakt{margin:26px 0 34px;padding:22px 24px;border-radius:14px;background:#071F49;color:#fff;break-inside:avoid}
.kontakt b{font-size:18px}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.pobierz{display:inline-flex;align-items:center;min-height:44px;background:#fff;color:#071F49;font-weight:700;padding:0 18px;border-radius:10px;text-decoration:none}
.pobierz.jasny{background:rgba(255,255,255,.12);color:#fff}.pobierz.maly{margin-top:12px;background:#071F49;color:#fff;min-height:40px;padding:0 14px;font-size:14px}
@media screen and (max-width:820px){.okl{padding:28px 18px 84px}.wybor,.wyzwania,.moduly,.korzysci,.zdjecia{grid-template-columns:1fr}.okl h1{font-size:28px}}
@media print{body{background:#fff}.wybor,.podpowiedz{display:none}.okl{padding-bottom:40px}.grupa-oferty{display:block!important}.kontakt{margin:26px 24px}}
"""


def _svg(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IKONY[k]}</svg>'


def _wspolne():
    return '<h2>W każdym module</h2><ul class="wsp">' + "".join(f"<li>{x}</li>" for x in WSPOLNE) + "</ul>"


def _cta(k=None, pdf=False):
    if pdf:
        return ('<div class="kontakt"><b>Zainteresowany?</b><br>Warunki współpracy dopasujemy do liczby użytkowników i wybranych modułów. '
                'Ofertę online z wyborem modułu znajdziesz na stronie logowania programu Bidivia – w okienku „Nasza oferta”.</div>')
    return (f'<div class="kontakt"><b>Zainteresowany?</b><br>Pobierz ofertę i przekaż ją w swojej firmie – warunki współpracy dopasujemy '
            f'do liczby użytkowników i wybranych modułów.<div class="cta">'
            f'<a class="pobierz" href="/oferta/pdf/{k}">Pobierz ofertę – {GRUPY[k]["tytul"].lower()} (PDF)</a>'
            f'<a class="pobierz jasny" href="/oferta/pdf/wszystkie">Oferta na wszystkie moduły (PDF)</a>'
            f'<a class="pobierz jasny" href="/login">Mam konto – zaloguj się</a></div></div>')


def sekcja(k, g, zdjecia=None, pdf=False):
    zd = (zdjecia or {}).get(k) or []
    h = (f'<section class="grupa-oferty" id="{k}" style="--k:{g["kolor"]}"><div class="naglowek-gr"><h2>{g["tytul"]}</h2>'
         f'<div class="haslo">{g["haslo"]}</div><ul>' + "".join(f"<li>{x}</li>" for x in g["kto"]) + "</ul>"
         + ("" if pdf else f'<a class="pobierz maly" href="/oferta/pdf/{k}">Pobierz tę ofertę (PDF)</a>') + "</div>")
    h += '<h2>Z czym Ci pomożemy</h2><div class="wyzwania">' + "".join(
        f'<div class="wyz"><div class="p">{p}</div><div class="r">{r}</div></div>' for p, r in g["wyzwania"]) + "</div>"
    h += '<h2>Funkcje programu</h2><div class="moduly">' + "".join(
        f'<div class="modul"><h3>{t}</h3><p class="op">{o}</p><ul>' + "".join(f"<li>{x}</li>" for x in pk) + "</ul></div>"
        for t, o, pk in g["moduly"]) + "</div>"
    h += '<h2>Jak to wygląda w praktyce</h2><ol class="proces">' + "".join(f"<li>{x}</li>" for x in g["proces"]) + "</ol>"
    h += '<h2>Korzyści</h2><div class="korzysci">' + "".join(f'<div class="korz"><b>{t}</b><span>{o}</span></div>' for t, o in g["korzysci"]) + "</div>"
    if zd:
        h += '<h2>Tak to wygląda</h2><div class="zdjecia">' + "".join(f'<figure><img src="{src}" alt=""><figcaption>{c}</figcaption></figure>' for src, c in zd) + "</div>"
    h += '<h2>Najczęstsze pytania</h2>' + "".join(f'<div class="pyt"><b>{q}</b><span>{a}</span></div>' for q, a in g["pytania"])
    if not pdf:
        h += _wspolne() + _cta(k)
    return h + "</section>"


def strona(kontakt=None, link="", zdjecia=None, tylko=None, tytul="Bidivia – nasza oferta", pdf=False):
    """Strona oferty: na starcie tylko trzy okienka do wyboru; po kliknięciu rozwija się oferta dla danego klienta
    (z przyciskiem pobrania PDF). pdf=True – dokument do druku (wszystkie wybrane sekcje widoczne). Bez danych kontaktowych."""
    grupy = {k: g for k, g in GRUPY.items() if not tylko or k == tylko}
    wybor = "" if pdf else ('<div class="wybor">' + "".join(
        f'<button style="--k:{g["kolor"]}" data-g="{k}" onclick="pokazOferte(\'{k}\')"><span class="ik">{_svg(k)}</span><b>{g["tytul"]}</b>'
        f'<span class="o">{g["krotko"]} – {g["haslo"]}</span><span class="dalej">Zobacz ofertę →</span></button>' for k, g in GRUPY.items()) + "</div>"
        '<p class="podpowiedz" id="podpowiedz">Wybierz, kim jesteś – pokażemy funkcje i korzyści dla Ciebie.</p>')
    sekcje = "".join(sekcja(k, g, zdjecia, pdf) for k, g in grupy.items())
    if pdf:
        sekcje = sekcje.replace('class="grupa-oferty"', 'class="grupa-oferty widoczna"') + _wspolne() + _cta(pdf=True)
    skrypt = "" if pdf else """<script>
function pokazOferte(k){document.querySelectorAll('.grupa-oferty').forEach(function(s){s.classList.toggle('widoczna',s.id===k)});
document.querySelectorAll('.wybor button').forEach(function(b){b.classList.toggle('akt',b.dataset.g===k)});
var p=document.getElementById('podpowiedz'); if(p) p.style.display='none';
history.replaceState(null,'','?dla='+k); document.getElementById(k).scrollIntoView({behavior:'smooth'});}
var d=new URLSearchParams(location.search).get('dla')||location.hash.slice(1); if(d&&document.getElementById(d)) setTimeout(function(){pokazOferte(d)},50);
</script>"""
    pod = ("Jeden program dla przetargów, inwestycji, wycen i dotacji: od wyszukania przetargu, przez ofertę i kosztorys, po realizację i rozliczenie umowy – dla wykonawców, dostawców, zamawiających, inwestorów, rzeczoznawców i wnioskodawców dotacji."
           if not tylko else GRUPY[tylko]["haslo"])
    return (f'<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{_h.escape(tytul)}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="okl"><span class="logo"><svg viewBox="245 244 753 753" aria-hidden="true"><path d="M245 244H810L998 433L810 621L245 307Z" fill="#fff"/><path d="M245 997H810L998 809L810 621L245 935Z" fill="#fff"/><path d="M245 401L810 621L245 574Z" fill="#9DB8DA"/><path d="M245 668L810 621L245 841Z" fill="#9DB8DA"/></svg>BIDIVIA</span>'
            f'<h1>{_h.escape(tytul)}</h1><div class="pod">{pod}</div></div>{wybor}<div class="tresc">{sekcje}</div>{skrypt}</body></html>')
