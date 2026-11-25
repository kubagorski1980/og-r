# Bidivia – historia zmian

Najnowsze wersje na górze. Każda wersja: co zmieniono, dlaczego i jak sprawdzono.


## Wersja „2027-03-12 decyzje-wlasciciela”

Poprzednia wersja: „2027-03-11 pozostale-moduly”. **Paczka „KOMPLET” zawiera też wszystkie wersje od 2027-02-08 – wystarczy wgrać tę.**
Wdrożenie decyzji właściciela z listy „do decyzji” wersji 03-11 (cztery zespoły, łatki scalone w jedną wersję) oraz dokończenia po scaleniu.

### WAŻNE PRZY WGRYWANIU

1. **Pliki do ręcznego usunięcia w repozytorium GitHub** (paczka tylko nadpisuje, niczego nie kasuje; lista także w `DO_USUNIECIA.txt`):
   `szacowanie_web.py`, `szacowanie.js`, `serwer (1).py`, `serwer-1.py`, `serwer-2.py`, `files35.css`, `instrukcja-1.html`
   (opcjonalnie `instrukcja-1.pdf`). Na GitHubie: plik → kosz „Delete file” → „Commit changes”.
   **NIE usuwać** `app.js`, `index.html`, `login.html`, `styl.css`, `uklad.js`, `ksiegowosc.js`, `pzp_wykonawca.js`, `instrukcja.html`,
   `oferta.html`, `instrukcja.pdf` ani innych plików z katalogu głównego – to z nich Render buduje program.
2. **Wgrać nowy `Dockerfile`** (jest w paczce). Buduje z repozytorium płaskiego jak dotąd, a także z układu z katalogiem `static/` i z `app/`.
3. **Dawni dodatkowi administratorzy stracą wgląd w projekty właściciela** i innych firm (każdy administrator konta to teraz osobna firma).
   Jeśli mają dalej pracować nad projektem właściciela – udostępnić go w projekcie („Dostęp”).
4. **Serwer SMTP w sieci wewnętrznej przestanie działać** (np. przekaźnik na localhost, adresy prywatne) – trzeba podać publiczny serwer poczty
   (porty 25, 465, 587 albo 2525).
5. **Użytkownicy zostaną wylogowani po 8 h bezczynności** (i najpóźniej po 14 dniach od zalogowania).
6. **Płace i księgowość mają jeszcze płacę minimalną 2026** (4806 zł w `place.py`, `ksiegowosc.py`, `ksiegowosc_parametry.py`) – wartości 2027
   (4950 zł / 32,30 zł) trzeba dopisać przed 1.01.2027 (poza zakresem tej wersji).

Migracje przy starcie (same, powtarzalne): pole `firma` w kontach, role zapisane przed wersją (Płace/Kadry nie są już wymuszane), przykładowy
opis firmy usuwany z profili, wkład własny inwestycji liczony ze starych wkładów (do zatwierdzenia na ekranie). Nowych zmiennych środowiskowych nie ma.

### Bezpieczeństwo i uprawnienia
Pliki: `uwierzytelnianie.py`, `uprawnienia.py`, `bezpieczenstwo.py` (nowy), `trasy_bezpieczenstwo.py` (nowy), `trasy_admin.py`, `trasy_firma.py`,
`trasy_przetargi.py`, `trasy_dotacje.py`, `trasy_realizacja.py`, `konfiguracja.py`, `modul_harmonogram.py`, `serwer.py`, `app.js`, `index.html`, `login.html`
- Administrator konta zarządza tylko swoją firmą (projekty, użytkownicy, aktywność, AI); nie nadaje roli „Administrator”. Zmiana ról,
  „Otwórz konto”, parametry płac, diagnostyka i ustawienia wspólne – tylko właściciel programu. Zastępuje WSP-08 z 03-08.
- Płace i Kadry nie są już przyznawane każdej roli – obowiązuje opis roli. Rola bez Płac i Finansów nie widzi stawek ani kwot robocizny.
- Kierownik budowy: przedmiar bez cen (tabela i Excel), bez plików z cenami, protokół odbioru bez kwot; Archiwum – podgląd (widzi poprzednie
  i usunięte raporty dzienne oraz usterki, przywraca je przez Realizację). Dostawy i usługi (strona dostawcy) wymagają Finansów; zapis częściowy.
- Zmiana własnego hasła (`/zmien-haslo`), reset hasła przez administratora (hasło tymczasowe 72 h), sesja wygasa po 8 h bezczynności,
  CSRF przy logowaniu i wylogowaniu, nagłówek `X-Agent` także dla PATCH.
- SMTP tylko na publiczne serwery i dozwolone porty (sprawdzenie przy zapisie i przy wysyłce, bez ponownego DNS).
- RODO w kadrach: data ustania stosunku pracy i ZUS RIA, okres przechowywania (art. 94 pkt 9b KP), karta „Do trwałego usunięcia (RODO)”,
  przypomnienie na Pulpicie, trwałe usunięcie przez administratora z potwierdzeniem.
- Przykładowy opis firmy tylko jako podpowiedź; ocena przetargów przez AI wymaga uzupełnionego opisu firmy.
- Godziny pracy na budowie udostępnionej przez inną firmę – wpis do ewidencji właściciela budowy.

### Odwołania i terminy
Pliki: `odwolania_przetargi.py`, `trasy_odwolania.py`, `lista_kontroli.py`, `leady.py`, `trasy_leady.py`, `progi.py`, `rynkowosc.py`,
`sprawozdanie_uzp.py`, `serwer.py`, `app.js`
- Odwołania: „Projekt tekstu” z ostrzeżeniem (art. 398 PKE, RODO, etyka zawodowa) zamiast e-maila; bez `mailto:`.
- Przełącznik „Wartość zamówienia a progi unijne” (automatycznie / poniżej / od progów UE) – przelicza termin bez AI.
- Data i sposób przekazania informacji o wyborze – termin 5/10/15 dni wg art. 515 ust. 1, z przesunięciem z art. 509 ust. 2.
- Termin związania ofertą 30 / 90 / 120 dni (art. 307, art. 220 ust. 1), argument od dnia upływu; także w liście kontrolnej.
- Średnia z art. 224 ust. 2 pkt 1 pomija tylko oferty odrzucone z art. 226 ust. 1 pkt 1, 5a i 10; przy niepewnej podstawie – dwa wyliczenia.
- Leady: zabezpieczenie należytego wykonania z ogłoszenia/SWZ albo „do 5%” (art. 452 ust. 2).
- Kurs euro 4,31 zł, progi UE 2026–2027 i płaca minimalna 2027 potwierdzone w źródłach (komentarze w kodzie).

### Finanse, dotacje, budowa
Pliki: `pogoda.py`, `rynkowosc.py`, `finansowanie.py`, `trasy_finansowanie.py`, `dotacje_plan.py`, `plan_zamowien.py`, `trasy_zamawiajacy.py`,
`ocena_ofert.py`, `trasy_ocena.py`, `trasy_firma.py`, `trasy_projekty_wykonawcy.py`, `trasy_realizacja.py`, `modul_harmonogram.py`, `modul_oferty.py`, `serwer.py`, `app.js`
- Pismo pogodowe: termin w dniach roboczych (domyślnie) albo kalendarzowych; zdanie o dzienniku budowy tylko z wpisów EDB lub raportów dziennych.
- Wynik prognozowany z postępu prac (koszt do zakończenia); bez danych – „brak danych do prognozy”.
- Kalkulator kosztów pracy: zwolnienia z FP i FGŚP, wynagrodzenie chorobowe, PPK z wpłatą dodatkową.
- Finansowanie inwestycji: promesa BGK (RFIL, Polski Ład, RFRD), jeden wkład własny inwestycji, ostrzeżenie z art. 243 ufp.
- Plan dotacji: tryb wyboru wykonawcy po zsumowaniu zamówień tożsamych (CPV / kategoria), ostrzeżenie o dzieleniu zamówienia.
- Pusty plan postępowań – ostrzeżenie; podpisy protokołu wspólnoty (zarząd / zarządca); NIP z sumą kontrolną (komunikat, bez blokady);
  polisy OC – kontrola daty i ostrzeżenia; termin szkolenia okresowego BHP; sezon lęgowy 1.03–15.10 w poleceniach AI.

### Porządek i wygląd
Pliki: `trasy_admin.py`, `trasy_realizacja.py`, `budowa.py`, `oferta.py`, `uwierzytelnianie.py`, `serwer.py`, `Dockerfile`, `app.js`, `styl.css`,
`index.html`, `login.html`, `instrukcja.html`, `oferta.html`
- Archiwum: poprzednie i usunięte wersje raportów dziennych oraz usunięte usterki – podgląd treści i przywracanie (edycja Realizacji).
- „Raporty dzienne (dziennik pomocniczy)” zamiast „Dziennik budowy” – ekran, wydruk (`Raporty_dzienne_….docx`), instrukcja, oferta;
  zdanie, że to nie jest dziennik budowy z art. 45 Prawa budowlanego.
- Usunięte duplikaty i martwy kod (lista wyżej); nowy Dockerfile.
- „Pomoc” na telefonie i tablecie w nagłówku – nie zasłania już przycisków formularzy; przy otwartym menu na telefonie ikona jest
  ukryta, żeby nie nachodziła na „Zmień hasło” i „Wyloguj”.
- Osobna ikona „maskable” (pełne tło, znak w strefie bezpiecznej), `?v=2027c`.
- Instrukcja: opisy wszystkich nowych funkcji (hasła i sesje, administrator konta, przedmiar bez cen, RODO, Odwołania, pismo pogodowe,
  wynik prognozowany, kalkulator, finansowanie, plan dotacji, polisy OC i BHP, Archiwum raportów, Raporty dzienne).

### Sprawdzono
- Testy decyzji: uprawnienia (149 sprawdzeń), Odwołania (60), finanse (72), porządek (100), dokończenia scalenia (68, z nagłówkiem
  na 8 szerokościach ekranu) – 0 błędów.
- Wszystkie testy repozytorium (42 pliki, w tym `kryteria_dokumenty_test.py` osobno) – 0 błędów; regresja adresów: edycja pełna
  335 adresów, zamawiający 253 – 0 błędów 500.


## Wersja „2027-03-11 pozostale-moduly”

Poprzednia wersja: „2027-03-10b nowe-hero”. **Paczka zawiera też całe wersje 2027-03-07, 2027-03-08, 2027-03-09, 2027-03-10 i 2027-03-10b – wystarczy wgrać tę.**
Poprawki z testów krytycznych pozostałych modułów (cztery grupy, łatki scalone w jedną wersję) i dokończenie zabezpieczenia tekstu w przyciskach.

**Przetargi, Leady, Odwołania, Prawnik (GA-01…16)** – pliki `odwolania_przetargi.py`, `trasy_odwolania.py`, `lista_kontroli.py`, `prawnik.py`, `leady.py`,
`trasy_leady.py`, `trasy_przetargi.py`, `ted.py`, `uprawnienia.py`, `serwer.py`, `app.js`
- Odwołania: termin 5 albo 10 dni według reżimu (od progów UE – art. 515 ust. 1 pkt 1 lit. a) w notatce, e-mailu, na ekranie i w projekcie odwołania
  (nowy tryb „unijny”); terminy przeliczane przy każdym odczycie, po upływie – „termin odwołania minął” (GA-01, 02, 07, 09).
- Prawnik: tryby występujące w obu reżimach (negocjacje bez ogłoszenia, wolna ręka, partnerstwo) – oba warianty terminu; wpis od odwołania
  7 500 / 15 000 / 10 000 / 20 000 zł zamiast [UZUPEŁNIJ] (GA-03, 04).
- Nowy argument: wybrana oferta nie ma najwięcej punktów (art. 239); argumenty od najsilniejszego; kwoty i punkty po polsku (GA-05, 06).
- Leady: data wyboru z informacji o wyborze; termin ofert z godziną; CSV bez formuł Excela (CSV injection), liczby z przecinkiem (GA-10…12).
- Baza Konkurencyjności (`/api/bk`) tylko z modułem Przetargi; TED – najwcześniejszy termin z części; walidacja tras przetargów (GA-13…16).
- Firma z apostrofem w nazwie („O'Neill”) – przyciski ekranu Odwołań działają (GA-08).

**Budowa, dziennik, usterki, pracownicy, kadry, podwykonawcy, dostawy (GB-01…24)** – pliki `trasy_realizacja.py`, `uprawnienia.py`, `budowa.py`,
`trasy_projekty_wykonawcy.py`, `trasy_firma.py`, `serwer.py`, `modul_harmonogram.py`, `modul_materialy.py`, `pogoda.py`, `app.js`, `styl.css`, `uklad.js`
- Kierownik budowy (bez Finansów) nie dostaje kwot umowy, faktur, kosztów, stawek ani kwot HRF i podwykonawców – serwer i ekran; zapisuje dane
  umowy (bez wartości i VAT) i notatki; zapis bez Finansów nie zeruje kwot (GB-01…04).
- Podwykonawcy: własne uwagi w osobnym polu (nie znikają); faktura bez terminu – termin z umowy, zaległości (art. 463/465 Pzp) (GB-05, 06).
- Raport dzienny: historia wersji i usuniętych wpisów, bez dat z przyszłości, opis „pomocniczy rejestr – nie dziennik budowy”; zdjęcia z archiwum
  poza wydrukami, tylko pliki graficzne; usunięta usterka do archiwum, termin jako data (GB-07…10).
- Roboczogodziny: max 24 h na dobę, ostrzeżenie ponad 13 h (art. 132 KP), stawka nieujemna, „Kwota wg stawek”, sumy po identyfikatorze;
  kadry – kolejność dat, badania bez terminu z ostrzeżeniem (GB-11…13).
- Klient: edycja po id, NIP innego klienta – 400; nowy adres budowy – nowe współrzędne pogody; hurtownia bez e-maila – 400 (GB-14…16).
- Harmonogram dostaw: walidacja przed AI, święta w terminach zamówień, m³ = m3; pogoda – święto nie jest dniem roboczym (GB-17…20).
- Telefon: pasek kroków budowy, nagłówek bez łamania, pola dat 16 px; „do przygotowania” nie jest oznaczane ✓; bez 403 na starcie (GB-21…24).

**Dotacje, finansowanie, nieruchomości (GC-01…08)** – pliki `uklad.js`, `app.js`, `styl.css`, `trasy_projekty_wykonawcy.py`, `dotacje_plan.py`,
`serwer.py`, `trasy_finansowanie.py`, `finansowanie.py`, `trasy_dotacje.py`, `nieruchomosci.py`
- Kroki 2–4 projektu dotacji i wniosku (wymagania, budżet, rozliczenie, trwałość, zapytania) znów widoczne; bez przycisku „Przetarg wygrany”
  w dotacjach; kwoty z przecinkiem (GC-01, 02).
- Plan dotacji: walidacja pozycji (400 zamiast trwale zepsutego planu), intensywność z zakresu „50–85%” = 85%, suma co do grosza;
  trwałość 5 lat, 3 lata tylko dla MŚP (art. 65 rozp. 2021/1060) (GC-03…05).
- Finansowanie inwestycji: „Usuń” nie tworzy nowego źródła, kontrola dat i kwot, daty z AI zapisywane poprawnie (GC-06).
- Bezpieczeństwo: zapytanie ofertowe tylko do własnego projektu dotacji (GC-07). Nieruchomości: daty transakcji w różnych zapisach, bez błędu 500 (GC-08).

**Wspólnota, kalkulator, administracja, bezpieczeństwo, aplikacja mobilna (GD-01…13 + dokończenie)** – pliki `serwer.py`, `trasy_admin.py`,
`rynkowosc.py`, `weryfikacja.py`, `kontrola.py`, `wspolnota.py`, `app.js`, `index.html`, `instrukcja.html`
- Logowanie: ten sam czas odpowiedzi dla istniejących i nieistniejących kont; role – identyfikator tylko `[a-z0-9_]`; zakresy ustawień konta (GD-01…03).
- Archiwum: nie można przywrócić cudzego projektu; „Tylko podgląd” bez „Przywróć” (GD-04).
- Kalkulator kosztów pracy: pole „Początek umowy”, płaca minimalna i stawka godzinowa z okresu umowy (2026/2027), nadgodziny, dodatek nocny,
  VAT 0/5/8/23, kwoty z groszami (GD-05). Instrukcja: także rozdział oceny ofert bez sztywnej kwoty 4806 zł (dokończenie).
- 29 lutego w ocenie doświadczenia, liczby tekstowe w kontroli kosztorysu, wspólnota – pełnomocnictwo zarządu i reprezentacja (art. 21, 22 UWL) (GD-06…08).
- Pomoc i manifest aplikacji (PWA: bez blokady orientacji, ikony any/maskable); wyszukiwarka w każdym trybie + „Szukaj w projektach…”;
  nazwy ról w kontach; pulpit bez 403 (GD-09, 10, 12, 13).
- **Tekst w przyciskach (XSS)**: nowa funkcja `escA` (GD-11) użyta we wszystkich ok. 45 pozostałych miejscach (Przetargi, Odwołania, Pracownicy,
  Raporty, kreator, dotacje, windykacja, nieruchomości…); `jsa` zamiast `JSON.stringify(…).replace(…&quot;)`. Nazwy z apostrofem nie są już
  okrajane – np. „×” usuwa raport „O'Neill…”, a „Usuń” pyta o pełne imię pracownika.

**Uwaga przy wdrożeniu**
- Nowych zmiennych środowiskowych i migracji danych nie ma. Stare uwagi podwykonawców przenoszą się same do pola `notatka`.
- Zmiany zachowania: kierownik budowy nie widzi kwot; raport dzienny z przyszłą datą, hurtownia bez e-maila, złe ustawienia konta i identyfikatory ról – 400;
  „Tylko podgląd” bez „Przywróć” w Archiwum.
- W paczce płaskiej `app.js`, `styl.css`, `uklad.js`, `index.html`, `instrukcja.html`, `login.html` pochodzą z `static/` (Dockerfile kopiuje je do `static/`).

Sprawdzono: testy grup `grupa_a…d_test.py` (29 + 53 + 34 + 57) i nowy `xss_onclick_test.py` (23; Playwright: Przetargi, Pracownicy, Raporty, Odwołania –
nazwy z apostrofem i `<img onerror>`, bez wykonania kodu, przyciski działają); 31 testów repozytorium (1019 sprawdzeń) i `kryteria_dokumenty_test.py` (24) –
razem 1239 sprawdzeń, 0 błędów; regresja adresów: pełna 319, edycja zamawiającego 239 – 0 błędów; `node --check`, `py_compile`.

---

## Wersja „2027-03-10b nowe-hero”

Poprzednia wersja: „2027-03-10 nowe-hero”. **Do podmiany tylko `serwer.py`** (paczka `Bidivia_2027-03-10b_plik_do_podmiany.zip`).
- Edycja dla zamawiającego – logowanie: tytuł panelu taki sam jak w pełnej, „Więcej niż przetargi” (bez podmiany na „Zamówienia od A do Z”).
  Opis panelu dla zamawiającego („Od kreatora zamówienia, przez ocenę ofert, po rozliczenie umowy.” + „Cała inwestycja w jednym miejscu.”)
  i podtytuł dla gmin – bez zmian. Plik `serwer.py` (stała `LOGIN_ZAMAWIAJACY`).

Sprawdzono: `hero_zamawiajacy_test.py` (29 sprawdzeń) – 0 błędów; regresja adresów: edycja zamawiającego 239 adresów, pełna 319 – 0 błędów;
zrzut `/login` 390 px w edycji dla zamawiającego.

---

## Wersja „2027-03-10 nowe-hero”

Poprzednia wersja: „2027-03-09 vat-lista-kontrolna”. **Paczka zawiera też całe wersje 2027-03-07, 2027-03-08 i 2027-03-09 – wystarczy wgrać tę.**
Strona logowania: nowy panel marki według projektu (podgląd mobile 390 px) – komponent `.bd-hero`. Formularz logowania, jego pola i adres
wysyłki (`POST /login`), linki do oferty i kafelki – bez zmian. Poprawki: „Zaloguj się” jak w projekcie, teksty logowania i ekranu danych
w edycji dla zamawiającego, ucięte kolumny tabel w realizacji umowy.

**Panel marki – komponent `.bd-hero`** – plik `login.html` (w repozytorium `static/login.html`)
- Klasy: `.bd-hero` (granatowy panel, tło `--navy` #071F49 – ten sam granat co w aplikacji), `.bd-hero__logo` (znak + napis BIDIVIA, białe,
  wewnętrzne kliny znaku #7A9ACE – SVG jak dotąd), `.bd-hero__tresc`, `.bd-hero__tytul` („Więcej niż / przetargi”, 46 px na 390 px, waga 800),
  `.bd-hero__opis` (jasnoniebieski) z `.bd-hero__wyroznienie` (pogrubione białe „Cała inwestycja w jednym miejscu.”), `.bd-hero__promienie`
  z `.bd-hero__promien` / `--jasny` / `--dolny` – trzy klinowe pasy (niebieski, jasny błękit, ciemniejszy niebieski) wychodzące z lewej krawędzi
  i zbiegające się w prawym górnym rogu pasa u dołu panelu. Kolory i wysokość pasa w zmiennych `--bd-hero-*`.
- Telefon: panel na całą szerokość nad „Zaloguj się”, pas promieni 130 px. Komputer (od 861 px): jak dotąd lewy panel 42% + formularz po prawej –
  logo u góry, tytuł i opis nad promieniami, pas promieni u dołu (150–260 px zależnie od wysokości okna).
- Animacja: krótkie (0,7 s) wysunięcie promieni z punktu zbiegu (prawy górny róg pasa), tylko przy `prefers-reduced-motion: no-preference`; stan końcowy jest
  stanem bez animacji (widoczny także bez JavaScriptu).
- Usunięto stare klasy panelu (`.panel`, `.haslo`, `.logo`, `.promienie`) – nie były używane poza `login.html`.
- „Zaloguj się” jak w projekcie: 38 px na telefonie, odstęp od krawędzi 24 px (dotąd 30 px i 16 px); na komputerze 40 px.

**Edycja dla zamawiającego – logowanie** – plik `serwer.py`
- Błąd: serwer podmieniał w `login.html` dawny nagłówek „Prosta droga…”, którego od dawna nie było – urząd widział teksty dla wykonawcy.
  Podmiany są teraz w stałej `LOGIN_ZAMAWIAJACY` i pasują do panelu `.bd-hero`: tytuł „Zamówienia od A do Z”, opis „Od kreatora zamówienia,
  przez ocenę ofert, po rozliczenie umowy.” + wyróżnienie „Cała inwestycja w jednym miejscu.”, podtytuł logowania „Przygotowanie zamówień,
  ocena ofert i realizacja umów – dla gmin, urzędów i jednostek publicznych.”. Edycja pełna – bez zmian.

**Dane zamawiającego** – pliki `app.js`, `konfiguracja.py`
- Ekran „Dane zamawiającego” (tryb zamawiającego i edycja dla zamawiającego) miał teksty profilu wykonawcy. Teraz: dane trafiają do dokumentów
  zamówienia (SWZ albo zapytanie ofertowe, ogłoszenie), umowy, pism i protokołów; pola „Nazwa zamawiającego (np. Gmina Świdnica)”, „Adres siedziby”,
  „Osoba reprezentująca (np. wójt, burmistrz, dyrektor)”, „Strona www / BIP”, rachunek do wadium, godziny pracy; „Logo albo herb” w nagłówku dokumentów.
  Bez opisu firmy, certyfikatów, referencji i polisy (dokumenty wykonawcy) – zapis danych zamawiającego nie nadpisuje już opisu firmy wykonawcy
  na tym samym koncie. „Ustawienia mojego konta” u zamawiającego – tylko poczta SMTP (bez wyceny, wyszukiwania i oceny przetargów).
  Kafelek na pulpicie zamawiającego: „Dane zamawiającego”. Profil firmy wykonawcy – bez zmian.
- Przykładowy opis „Firma budowlana ze Świdnicy, 15 pracowników…” (wartość domyślna z programu okienkowego) nie trafia do zamawiającego
  (edycja dla zamawiającego, konta modułu gmina / wspólnota) – ani na ekran, ani do konfiguracji używanej przez AI i dokumenty.

**Realizacja umowy – tabele** – pliki `app.js`, `styl.css`
- Faktury: kolumna „Cofnij zapłatę” była ucięta (1920×1080 i telefon) – tabela szersza niż krok, przewijanie niewidoczne. Teraz kolumny
  „Wystawiona / termin” i „Netto / brutto” (zamiast czterech), przyciski zawijane: „Zapłacona” / „Cofnij” i kosz z etykietami dostępności
  („Cofnij zapłatę faktury …”, „Usuń fakturę …”) i podpowiedzią. Tak samo „Inne koszty” (kolumna „Data / kategoria”).
- W wąskim oknie (telefon, tablet, krok węższy niż 820 px) wiersze faktur i kosztów są kartami z etykietami pól – bez przewijania w bok.
- Tabele szersze niż okno (harmonogram rzeczowo-finansowy z wieloma etapami): widoczny pasek przewijania, przyklejona kolumna działów
  i wskazówka „Tabela jest szersza niż okno – przewiń ją w bok” (sprawdzane przy każdej zmianie szerokości). Protokoły odbioru i podwykonawcy –
  bez tabel, nic nie było ucięte.

**Pływający przycisk „Pomoc” nie zasłania treści** – plik `styl.css`
- Błąd: przycisk „Pomoc” (lewy dół) leżał na treści – np. zasłaniał „Zapisz” w karcie „Dane zamawiającego”, przyciski kafelków i ostatnie
  przyciski kart na telefonie (nawet po przewinięciu do końca).
- Komputer (od 1100 px): „Pomoc” jest w górnym pasku obok wyszukiwarki – poza treścią i menu; okienko pomocy otwiera się pod nim.
- Tablet i telefon: na dole treści (i przewijanych kolumn) zapas na przycisk – 92 px, z dolnym paskiem zakładek 160 px (plus okienka zadań),
  więc ostatni przycisk każdej karty da się przewinąć ponad „Pomoc”.

**Uwaga przy wdrożeniu**
- Brak nowych zmiennych i migracji danych. W paczce płaskiej `login.html` leży w katalogu głównym – przy budowie (Dockerfile) trafia do `static/`,
  skąd serwer go czyta (`/login`).

Sprawdzono: zrzuty Playwright `/login` 390×844 i 1440×900 porównane z projektem (układ, rozmiary, łamanie tekstu, promienie); 320, 360, 768, 1024,
1920 px – bez poziomego przewijania; bez JavaScriptu i z `prefers-reduced-motion: reduce` – promienie widoczne od razu; logowanie
admin@firma.pl na lokalnej instancji → pulpit, błędne hasło → komunikat; konsola bez błędów; edycja „zamawiajacy” – `/login` 200 z nowym panelem;
nowy test `hero_zamawiajacy_test.py` (29 sprawdzeń: logowanie w obu edycjach, podmiany pasują do `login.html`, brak opisu firmy budowlanej
u zamawiającego, teksty ekranu danych, „Zaloguj się”, tabele, „Pomoc”; na wersji 03-09 – 22 błędy); zrzuty realizacji (faktury, koszty, harmonogram,
protokoły, podwykonawcy) przy 1920, 1440, 1100, 768 i 390 px – żadna tabela faktur i kosztów nie wychodzi poza okno, harmonogram ze wskazówką,
konsola bez błędów; zrzuty „Dane zamawiającego” i logowania w edycji dla zamawiającego; zrzuty „Pomoc” (dane zamawiającego, pulpit,
realizacja, projekty, konta, archiwum, ustawienia; 1920, 1440, 1100, 1024, 768, 390 px; strona i przewijane obszary przewinięte do końca) – żaden
przycisk, link ani pole pod „Pomoc” (na wersji 03-09: 10 kolizji); 32 testy repozytorium – 0 błędów;
regresja adresów (pełna): 319 adresów, 0 błędów.

---

## Wersja „2027-03-09 vat-lista-kontrolna”

Poprzednia wersja: „2027-03-08 podglad-odczyt”. **Paczka zawiera też całe wersje 2027-03-07 i 2027-03-08 – wystarczy wgrać tę.**
Błąd: w kreatorze zamówienia pisma z listy kontrolnej (m.in. „Informacja o kwocie przeznaczonej na sfinansowanie zamówienia”, art. 222 ust. 4 Pzp)
dostawały kwotę brutto ze stałego mnożnika netto × 1,23 (gdy brak kosztorysu) albo kwotę brutto kosztorysu AI (inną niż wartość zamówienia).
Przy budownictwie społecznym (VAT 8%) pismo podawało za dużą kwotę.

**Serwer – jedna stawka VAT zamówienia (jak w ocenie ofert, ZE-27)** – pliki `trasy_kreator.py`, `kreator_zam.py`
- Nowa funkcja `trasy_kreator._brutto_zam(m, K, netto)`: wartość z VAT = wartość netto zamówienia × (1 + stawka), stawka z tej samej funkcji
  `_stawka_vat` co w ocenie ofert (kosztorys zamówienia `oferta.vat` bez „VAT nieustalony” albo pole kreatora `vat`; dozwolone 0/5/8/23%).
  Stan kreatora (`/api/projekty/<id>/kreator`) zwraca `brutto`, `stawka_vat`, `stawka_vat_znana`; `kreator_element` („Przygotuj”) przekazuje je do pisma.
  Bez wartości netto – jak dotąd kwota brutto z kosztorysu (jeśli jest).
- Stawka nieustalona – 23% i w piśmie po kwocie dopisek „[UZUPEŁNIJ: sprawdź stawkę VAT – kwotę wyliczono z wartości netto przy VAT 23%, bo stawki
  nie ustalono w kosztorysie zamówienia]” (także gdy pole kwoty na ekranie zostawiono z podpowiedzią). Kwota wpisana ręcznie przez zamawiającego – bez dopisku.
  Kwota z ekranu w piśmie w zapisie „1 080 000,00” (dotąd np. „1080000”).
- Propozycja warunku doświadczenia (50% wartości brutto) liczona tą samą stawką (`_stawka_vat` zamiast osobnego odczytu `oferta.vat`).

**Ekran** – plik `app.js`
- Lista kontrolna, pole „kwota brutto”: podpowiedź „wartość netto + VAT X% (stawka z kosztorysu zamówienia)”; przy stawce nieustalonej żółte pole
  i „stawka VAT nieustalona; sprawdź stawkę i w razie potrzeby popraw kwotę” (jak w ocenie ofert – Rynkowość).

**Inne miejsca ze stałym 23%** – sprawdzone w `trasy_kreator.py`, `kreator_zam.py`, `zamawiajacy.py`, `postepowanie_zam.py`, `serwer.py`; pozostałe są celowe:
domyślna wartość parametru `warunki_domyslne(vat=0.23)` (wywołanie podaje stawkę), lista dozwolonych stawek w `postepowanie_zam.py`, kosztorys wykonawcy
(„VAT nieustalony – przyjęto 23%”, wybór stawki, krok groszowy ceny docelowej), stawka budowy z umowy `vat_realizacji` (oznaczona „do ustalenia”).

**Uwaga przy wdrożeniu**
- Brak nowych zmiennych i migracji danych. Pisma przygotowane wcześniej nie zmieniają się – przy VAT innym niż 23% przygotuj pismo o kwocie ponownie.

Sprawdzono: nowy test `kreator_vat_test.py` – 15 sprawdzeń (gmina, wartość netto 1 000 000: kosztorys z VAT 8% → pismo 1 080 000,00 zł brutto bez dopisku,
także z podpowiedzią z ekranu, ta sama wartość co w ocenie ofert; stawka 8% z pola kreatora; bez stawki i z „VAT nieustalony” → 1 230 000,00 z dopiskiem;
kwota ręczna – bez dopisku; stawka 23% ustalona – bez dopisku; warunek doświadczenia 540 000 zł; na wersji 03-08 – 12 błędów); 30 testów repozytorium
(997 sprawdzeń) i testy poprawek f1–f4 (7 plików, 446 sprawdzeń) – 0 błędów; regresja adresów (pełna): 319 adresów, 0 błędów; `node --check app.js`.

---

## Wersja „2027-03-08 podglad-odczyt”

Poprzednia wersja: „2027-03-07 poprawki-testow”. **Paczka zawiera też całą wersję 2027-03-07 – wystarczy wgrać tę.**
Decyzja właściciela produktu w sprawie WSP-07: rola „Tylko podgląd” NIC NIE ZMIENIA w programie (pełny tryb tylko do odczytu, zgodnie z opisem roli).
Dotąd ta rola zapisywała dane własnej firmy: klientów, pracowników, hurtownie, profil firmy i ustawienia konta.

**Serwer – jedna wspólna blokada** – pliki `uwierzytelnianie.py`, `serwer.py`, `uprawnienia.py`
- Nowa reguła `blokada_podgladu` (`@app.before_request` w `serwer.py`, logika w `uwierzytelnianie.py:odmowa_podgladu`): dla roli „Tylko podgląd”
  każde żądanie POST/PUT/PATCH/DELETE dostaje 403 „Rola „Tylko podgląd” nie może zmieniać danych.” – firma, logo i dokumenty firmy, klienci, pracownicy,
  godziny, kadry, płace, hurtownie, ustawienia konta, projekty, notatki, pliki, archiwum, wyszukiwanie przetargów, zadania AI i ich przerywanie.
  Tak samo konto z rolą, której już nie ma (program i tak traktował je jak podgląd). Pozostałe role – bez zmian.
- Wyjątki (nie zmieniają danych firmy): wylogowanie; pomoc (pytanie do pomocy); kalkulator kosztów pracy i jego wydruk Word; podgląd pozwu EPU (Word);
  wyliczenie listy płac bez zapisu i usuwania; zapamiętanie ostatniego trybu widoku i oznaczenie przetargu jako przejrzanego (stan widoku tego użytkownika).
  Zmiany własnego hasła w programie nie ma (hasła zmienia administrator), więc nie ma też wyjątku.
- `uprawnienia.py:wszystkie_role` – rola „podglad” ma najwyżej poziom „podgląd” we wszystkich modułach i nie uruchamia AI, także gdy administrator
  zmieni tę rolę w edytorze ról (dotąd stałe uprawnienia firmy dawały jej „edycję” klientów, pracowników, hurtowni, kadr, płac i firmy).
- Przy okazji: lista płac z `"usun": true` wymaga poziomu „edycja” modułu Płace (dotąd tylko `"zapisz"`).
- `/api/ja` zwraca `tylko_odczyt` (true dla podglądu).

**Ekran** – plik `app.js`
- Dla podglądu działa istniejący mechanizm modułów „tylko podgląd”: w widokach Profil firmy (z ustawieniami konta), Klienci, Hurtownie, Pracownicy
  nie ma przycisków zapisu, dodawania i usuwania; pola formularzy są tylko do odczytu; opis firmy wyświetla się jako tekst.
- Górny pasek: przy nazwie użytkownika „· tylko podgląd” (z podpowiedzią). Komunikat 403 wyświetla się jak dotąd w czerwonym okienku, po polsku.

**Uwaga przy wdrożeniu**
- Brak nowych zmiennych i migracji danych. Zmiana zachowania: konta z rolą „Tylko podgląd” nie zapiszą już danych własnej firmy –
  jeśli ktoś z tą rolą ma prowadzić klientów, pracowników albo profil firmy, administrator musi mu zmienić rolę (np. „Pracownik biurowy”).

Sprawdzono: nowy test `podglad_odczyt_test.py` – 87 sprawdzeń (podgląd: 35 prób zapisu z danymi, wgrywanie plików, usunięcie projektu i każdy z 320 adresów
POST/PUT/DELETE programu → 403 i dane bez zmian; podgląd nadal czyta klientów, pracowników, hurtownie, firmę, ustawienia konta, godziny, projekty, archiwum
i pliki; wyjątki działają; żaden adres GET nie jest blokowany; administrator, kierownik, pracownik biurowy, kierownik budowy i urzędnik zapisują jak wcześniej);
skrypt testera `t2_izolacja.py` – 0 błędów (5 sprawdzeń WSP-07 przechodzi); 30 testów repozytorium (997 sprawdzeń) i testy poprawek f1–f4 (7 plików, 446 sprawdzeń) –
0 błędów; regresja adresów (pełna): 319 adresów, 0 błędów; `node --check app.js`.

---

## Wersja „2027-03-07 poprawki-testow”

Poprzednia wersja: „2027-03-06 nowe-logo”. Poprawki błędów z testów krytycznych (wykonawca, kreator zamawiającego, etapy po kreatorze,
sprawy wspólne) – cztery łatki scalone w jedną wersję, plus dokończenie poprawek odłożonych przez programistów.

**Wykonawca (WYK-02…07, WYK-11…18)** – pliki `analiza.py`, `modul_oferty.py`, `serwer.py`, `trasy_projekty_wykonawcy.py`, `trasy_przetargi.py`, `trasy_realizacja.py`, `app.js`
- Kwoty przyjmują spacje niełamliwe i apostrof („90 000,00”); nan/inf/kwoty absurdalne – odmowa 400 (WYK-06, 07).
- Kosztorys dla zamawiającego: różnica groszowa rozkładana na pozycje, w ostateczności wiersz „Wyrównanie zaokrągleń” – cena oferty bez zmian (WYK-03).
- Edycja pozycji przy aktywnej korekcie ceny – zmiana trafia do wyceny pierwotnej, korekta zostaje (WYK-04); cofnięcie unieważnionego (WYK-05).
- Komplet oferty: nazwy braków bez ścieżek, uwaga o braku formularza, więcej sformułowań „wadium nie jest wymagane” (WYK-02, 11).
- Słowa kluczowe 3–60 znaków z komunikatem (WYK-12), cena w formularzu z groszami (WYK-13), zapis złożenia/wyniku – data, cena > 0, „najpierw Cofnij” (WYK-14),
  nieistniejąca data/godzina – 400 (WYK-15), „miliard” słownie (WYK-16), nieczytelna ilość – „Do weryfikacji” (WYK-17), treść żądania niebędąca obiektem JSON – 400 (WYK-18).
- Archiwa: ZIP z PDF na początku rozpakowywany (WYK-01), uszkodzone archiwum nie przerywa wgrywania (WYK-08), archiwum w archiwum (WYK-09), polskie znaki z macOS/Windows (WYK-10).

**Kreator zamawiającego (ZAM-01, 02, 04…17; ZAM-03 czeka na decyzję)** – pliki `kontrola_zam.py`, `kreator_zam.py`, `zamawiajacy.py`, `szacowanie.py`, `trasy_kreator.py`, `trasy_zamawiajacy.py`, `app.js`
- Wybrany tryb Pzp daje dokumenty Pzp (reżim po kodzie trybu, JEDZ według wartości od progów UE) – ZAM-01; to samo w module prawnika (`serwer.py`, dokończenie).
- Kontrola terminu wykonania (ZAM-02), „gotowe” wymaga terminu składania ofert (ZAM-04), zapis warunków – tylko pola zmienione (ZAM-05),
  limit kar, art. 443, wadium w częściach, zasada konkurencyjności 7/14/30 dni (ZAM-06…09), szacowanie bez daty wszczęcia, daty w przeszłości (ZAM-10, 11),
  finansowanie bez odczytanej umowy (ZAM-12), pola art. 109 i JEDZ cz. IV zamiast [UZUPEŁNIJ] (ZAM-13), brak wartości (ZAM-14),
  usunięcie SWZ.pdf nie kasuje SWZ.docx (ZAM-15), termin zapłaty w miesiącach (ZAM-16), daty DD.MM.RRRR i błędy 500 (ZAM-17).
- Ocena ofert (weryfikacja wykonawcy) bierze warunki udziału efektywne – propozycję programu z kreatora + zmiany zamawiającego (dokończenie po ZAM-05, `trasy_ocena.py`).

**Etapy zamawiającego po kreatorze (ZE-01…29)** – pliki `ocena_ofert.py`, `trasy_ocena.py`, `rynkowosc.py`, `serwer.py`, `postepowanie_zam.py`, `trasy_realizacja.py`,
`sprawozdanie_uzp.py`, `trasy_zamawiajacy.py`, `ochrona_ludnosci.py`, `ogloszenie_wykonania.py`, `zaproszenia.py`, `zapytania.py`, `trasy_wspolnota.py`, `trasy_kreator.py`, `app.js`
- Odrzucenie oferty wymaga punktu art. 226 ust. 1 i uzasadnienia (ZE-01); remis art. 248 (ZE-02); kryterium „cena” po nazwie dokładnej (ZE-03);
  oferta poniżej „od” w kryterium – niezgodna z SWZ (ZE-04); średnia art. 224 bez ofert odrzuconych z pkt 1, 5a, 10 – także w rynkowości (ZE-05, 06);
  siedziby w informacji o wyborze (ZE-07); blokada informacji przy unieważnieniu i cenie ponad kwotę (art. 255, ZE-08, 09); numer oferty, 30% w groszach,
  zaokrąglenie punktów, terminy wezwań z świętami, kwota w protokole (ZE-10…14).
- Data umowy przed upływem terminu na odwołanie – ostrzeżenie w kalendarzu i w ostrzeżeniach postępowania kreatora, z liczbą ofert z oceny
  (jedna oferta – wyjątek art. 308 ust. 3 / 264 ust. 2) – ZE-15; zapis danych umowy w kreatorze z kontrolą ceny, VAT i dat (400) – ZE-16.
- Okresy usług co do grosza (ZE-17), protokół końcowy po odbiorze wszystkich etapów (ZE-18), sprawozdanie UZP z wartości szacunkowej i tylko konta (ZE-19…21),
  OLiOC (ZE-22, 23), rok planu 2020–2100 (ZE-24), konto gminy bez zapytań wykonawcy (ZE-25), termin ofert tylko jako data – także w zapisie kreatora (ZE-26),
  wartość z VAT do oceny ofert ze stawką VAT zamówienia (kosztorys/kreator), 23% tylko gdy stawka nieustalona – z adnotacją (ZE-27), raport art. 446 (ZE-28), VAT wspólnoty (ZE-29).

**Wspólne – bezpieczeństwo, konta, uprawnienia (WSP-01…06, 09…15; WSP-07, 08 czekają na decyzję)** – pliki `serwer.py`, `trasy_admin.py`, `trasy_firma.py`, `uprawnienia.py`, `modul_oferty.py`, `trasy_projekty_wykonawcy.py`, `app.js`, `styl.css`
- Nowe konto z loginem usuniętego nie przejmuje jego danych (WSP-01); godziny pracy tylko własnych projektów (WSP-02);
  blokada logowania nie do obejścia nagłówkiem X-Forwarded-For + limit na login 10 prób / 15 min (WSP-03);
  limity rozpakowania archiwów – zip bomb (WSP-04); „Tylko podgląd” nie dopisuje notatek ani nie przywraca z archiwum (WSP-05);
  `/pobierz/…/projekt.json` – 404 (WSP-09); lista płac w pamięci (WSP-10); kafelek „Windykacja” (WSP-11); bez 404 logo w konsoli (WSP-12);
  polskie komunikaty archiwów (WSP-13); pliki wykonywalne odrzucane (WSP-14); `/zdrowie` bez logowania – tylko podstawowe pola (WSP-15).

**Uwaga przy wdrożeniu**
- Render ustawia `RENDER` sam – limit logowania liczy ostatni adres z X-Forwarded-For. Zmienną `ZAUFANE_PROXY` (np. `2`) ustawić TYLKO wtedy,
  gdy przed Renderem jest dodatkowe proxy (np. Cloudflare z proxy). Innych nowych zmiennych nie ma; migracja danych niepotrzebna.
- Zmiany zachowania: odrzucenie oferty bez podstawy – 400; „Tylko podgląd” bez zapisu notatek; zapis umowy w kreatorze z błędną datą/VAT – 400;
  archiwum ponad limit odrzucane (200 z uwagą w nagłówku `X-Uwagi`, pozostałe pliki zapisane).

Sprawdzono: 23 testy repozytorium (551 sprawdzeń, w tym poprawiony ocena_wybor_test.py – odrzucenie z podstawą) i 6 nowych testów
(wykonawca_poprawki2 92, kreator_poprawki 67, kreator_dokonczenie 21, etapy_zam_poprawki 89, etapy_zam_dokonczenie 27, wspolne_poprawki 63 = 359) –
razem 910 sprawdzeń, 0 błędów; regresja adresów (pełna): 319 adresów, 0 błędów; `node --check app.js`; przeglądarka (komputer i Pixel 7):
pulpit, przetargi, nowy projekt wykonawcy, kreator zamówienia (wszystkie kroki), ustawienia – 24 sprawdzenia, 0 błędów JS, 0 odpowiedzi 5xx.

---

## Wersja „2027-03-06 nowe-logo”

Poprzednia wersja: „2027-03-05 czesci-powody” (paczka 2027-03-06 zawiera też zmiany 03-03…03-05 – wystarczy wgrać tę, razem z `requirements.txt`).

**Nowe logo Bidivia (pliki od grafika: BIDIVIA logo, BIDIVIA LOGO projekt)** – pliki `index.html`, `login.html`, `styl.css`, `serwer.py`
- Nagłówek programu: znak i napis BIDIVIA z oryginalnych plików SVG (logotyp z własnym krojem liter zamiast napisu czcionką strony);
  na komputerze granat #072556 i jasny niebieski #7A9ACE, na tablecie i telefonie (granatowy nagłówek) – wersja „on dark”: biały znak
  i jasnoniebieskie promienie; na telefonie sam znak (jak dotąd).
- Strona logowania: logotyp w wersji „on dark”.
- Ikona strony i aplikacji na telefonie (32, 180, 192, 512 px): nowy znak na granacie #072556; nowa nazwa pliku i adres ?v=2027b –
  przeglądarki nie pokażą starej ikony z pamięci.

---

## Wersja „2027-03-05 czesci-powody”

Poprzednia wersja: „2027-03-04 kosztorys-zero-7z” (paczka 2027-03-05 zawiera też zmiany 03-03 i 03-04 – wystarczy wgrać tę, razem z `requirements.txt`).

**Kreator zamawiającego – krok „Wartość i tryb”, Podział na części (art. 91)** – pliki `app.js`, `trasy_kreator.py`

Zgłoszenie (telefon): „Nie można wybrać braku podziału na części. Nie wyskakują powody braku podziału.”
Przyczyna: „Bez podziału” jest zaznaczone domyślnie, więc kliknięcie nic nie zmieniało, a powody braku podziału były dopiero w liście
kontrolnej (krok „Komplet dokumentów”) – w kroku części nic się nie pokazywało. Na telefonie oba przyciski wyboru były w jednej linii.

- Przy „Bez podziału” od razu widać ramkę „Powody braku podziału”: 5 typowych powodów z art. 91 ust. 2 do zaznaczenia, pole na własne
  uzasadnienie, propozycja AI (gdy „Zaproponuj podział (AI)” uznało podział za niezalecany) z przyciskiem „Wstaw”, „Zapisz powody”;
  bez powodów – ostrzeżenie, że lista kontrolna nie będzie kompletna.
- Powody zapisywane tam, gdzie czyta je lista kontrolna – pismo „Uzasadnienie braku podziału” i pole „Podział na części” w ogłoszeniu
  (te same zaznaczenia w obu miejscach). Przejście na „Podziel” i z powrotem nie gubi powodów.
- Przyciski wyboru jeden pod drugim (telefon).

Sprawdzono: nowy test kreator_czesci_powody_test.py (6 sprawdzeń, w tym pismo Word), ekran na telefonie (Pixel 7), wszystkie testy, regresja adresów.

---

## Wersja „2027-03-04 kosztorys-zero-7z”

Poprzednia wersja: „2027-03-03 pozycje-zerowe” (paczka 2027-03-04 zawiera też jej zmiany – wystarczy wgrać tę).
**Wgraj także `requirements.txt`** (nowy moduł py7zr – serwer instaluje go przy wdrożeniu).

Zgłoszenie: przetarg „Modernizacja energetyczna świetlic wiejskich w Gminie Łagiewniki” (2026/BZP 00551159) – kosztorys „Gotowe: brutto 0,00 zł”.

Przyczyny (sprawdzone na stronie):
1. Dokumentacja na platformazakupowa.pl to archiwum „SWZ+ załączniki.7z”. Program rozpakowywał tylko ZIP – archiwum 7z zostało
   pominięte, do AI trafiło samo ogłoszenie. Dziennik mylił: „wszystkie są uwzględnione”.
2. Bez przedmiaru AI dało ceny jednostkowe z ilością 0 – wartość robót 0 zł; wycenione były tylko pozycje spoza przedmiaru (17 400 zł).
3. BŁĄD: kosztorys dla zamawiającego pomija dział „poza przedmiarem” (jego koszt rozkłada na pozycje przedmiaru). Gdy przedmiar nie ma
   żadnej wycenionej pozycji, nie było na co rozłożyć – wersja dla zamawiającego miała 0 zł, a program „wyrównał” kosztorys wewnętrzny
   do tej kwoty, wpisując −16 150 zł w pozycję „Cz. 2 – Świadectwo charakterystyki energetycznej”. Cena oferty: 0 zł.

Poprawki:
- `modul_oferty.py`, `serwer.py`, `trasy_projekty_wykonawcy.py`, `trasy_kreator.py`: archiwa 7z rozpakowywane jak ZIP (pobieranie z BZP /
  platform, wgrywanie plików, kreator) – bez plików systemowych i podwójnego folderu. Gdy serwer nie ma modułu – czytelny komunikat.
- `modul_oferty.py`: kosztorys dla zamawiającego – gdy przedmiar nie ma wycenionych pozycji, pozycje spoza przedmiaru zostają jako osobne pozycje.
- `serwer.py`: wyrównanie kosztorysu wewnętrznego do wersji dla zamawiającego tylko o grosze (do 1 zł) i nigdy do ceny ujemnej.
- `serwer.py`: dziennik pobierania podaje liczbę plików uwzględnionych i pominiętych (z nazwami).
- `serwer.py`: przed wyceną – ostrzeżenie o nierozpakowanych archiwach (7z, RAR, ZIP) pominiętych w kroku 1.
- `serwer.py`: po wycenie – gdy co najmniej połowa pozycji przedmiaru ma ilość 0: ostrzeżenie „Kosztorys bez ilości… Cena oferty NIE obejmuje
  tych robót” w dzienniku i jako pierwsza pozycja „Do weryfikacji”.

Po wdrożeniu, w tym przetargu: krok 1 → „Pobierz ponownie” (albo wgraj „SWZ+ załączniki.7z”) → „Przygotuj kosztorys”.

Sprawdzono: wykonawca_poprawki_test.py (+3: przedmiar bez ilości, kosztorys dla zamawiającego, archiwum 7z), wszystkie testy, regresja adresów – 0 błędów.

---

## Wersja „2027-03-03 pozycje-zerowe”

Poprzednia wersja: „2027-03-02 wykonawca-poprawki-2”.

**Pozycje 0 zł w kosztorysie wykonawcy (W5, W6)** – pliki `rozbieznosci.py`, `kontrola.py`, `serwer.py`, `modul_oferty.py`

Sprawdzone na stronie (przetarg BZP – chodnik w Mojęcicach, ryczałt): w dziale „Pozycje uzupełniające (poza przedmiarem)” 5 pozycji z ilością 0
i ceną 0. Trzy nie dotyczyły zakresu (wywóz wliczony w rozbiórki, budki lęgowe, odgromowa), ale dwie były wymagane albo niejasne:
„Regulacja studni, włazów i zasuw – wymagane w Opisie pkt 4.9; ilości nieokreślone” oraz „Nadzór archeologiczny – zakres nieokreślony”.
Program nic o nich nie mówił: kontrola kosztorysu – 0 alertów, tabela rozbieżności ich nie pokazywała, źródło ceny „Cena rynkowa (szacunek)”.
Przy ryczałcie robota bez ceny obciąża wykonawcę.

- Polecenie dla AI: uwagi pozycji 0 zł zaczynają się od „NIE DOTYCZY – ” albo „DO USTALENIA – ” (wtedy też pytanie do zamawiającego i ryzyko).
- Program dzieli pozycje 0 zł spoza przedmiaru: „nie dotyczy” (nie dotyczy, wliczone w…, nie wymagana, brak wycinek…) i wymagane / niejasne (pozostałe).
- „Do weryfikacji” – pierwsza pozycja: „Pozycje bez wyceny (0 zł): N poz. wymaganych albo niejasnych NIE MA w cenie oferty – … Wpisz ilość
  i cenę albo zadaj pytanie zamawiającemu – przy wynagrodzeniu ryczałtowym robota bez ceny obciąża wykonawcę.”
- Kontrola kosztorysu: alert „Bez wyceny” dla każdej wymaganej / niejasnej pozycji 0 zł (osobny, z nazwą pozycji); pozycje „nie dotyczy” – bez alertu.
- Źródło ceny pozycji 0 zł: „nie wyceniono” (zamiast „Cena rynkowa (szacunek)”).
- Kosztorys zamawiającego (inwestorski) bez zmian.

Sprawdzono: wykonawca_poprawki_test.py (+4 sprawdzenia, w tym dane z Mojęcic), wszystkie testy modułów, regresja adresów – 0 błędów.

---

## Wersja „2027-03-02 wykonawca-poprawki-2”

Poprzednia wersja: „2027-03-01 wykonawca-poprawki” (paczka 2027-03-02 zawiera też wszystkie jej zmiany – wystarczy wgrać tę).

**Klucz API odrzucony** – pliki `modul_oferty.py`, `serwer.py`
- Klucz odrzucony przez AI (401/403) jest zapamiętywany na 6 godzin: kolejne zapytania idą od razu drugim kluczem (wcześniej każde
  zadanie najpierw próbowało nieważnego klucza i pisało „Klucz API odrzucony” w dzienniku).
- Administrator widzi alert „Klucz API z … odrzucony – wymień go”; /zdrowie pokazuje liczbę odrzuconych kluczy (bez ujawniania kluczy).

**Pamięć podręczna AI** – pliki `modul_oferty.py`, `serwer.py`, `app.js`, `trasy_projekty_wykonawcy.py`
- Na stronie każde zadanie zapisywało ok. 490 tys. tokenów do pamięci i nic nie odczytywało – także przy dokańczaniu odpowiedzi.
- „Test połączenia z AI” sprawdza teraz także pamięć podręczną (to samo krótkie zapytanie dwa razy, koszt kilka groszy): przy
  ustawionym czasie (1 godzina / 5 minut), a gdy nie działa – przy drugim. Wynik mówi, które ustawienie wybrać.
- W dzienniku zadania ostrzeżenie, gdy dokończenie odpowiedzi nie odczytało dokumentów z pamięci.
- Weryfikacja dokumentacji (W4): większy zapas na rozumowanie AI – duża odpowiedź nie jest dzielona na dwa zapytania
  (każde dokończenie to ponowne wysłanie wszystkich dokumentów).

**Cena docelowa brutto (W6)** – pliki `serwer.py`, `app.js`
- Przy VAT 23% nie każdą kwotę brutto da się uzyskać z ceny netto w pełnych groszach (np. 580 000 → wychodziło 580 000,01).
  Program wybiera dokładną kwotę, a gdy jej nie ma – najbliższą NIŻSZĄ (nigdy wyższą od docelowej, np. budżetu) i pokazuje komunikat.

**Komplet oferty (W7)** – pliki `serwer.py`, `app.js`
- Gdy zamawiający nie wymaga wadium, a w komplecie jest dokument wadialny – uwaga „sprawdź, czy ten dokument jest potrzebny”.

Sprawdzono: nowy test wykonawca_poprawki_test.py (17 sprawdzeń), testy wykonawca_* (10), 13 testów modułów, regresja adresów, ekran W4 w przeglądarce.

---

## Wersja „2027-03-01 wykonawca-poprawki”

Poprzednia wersja: „2027-02-28 wykonawca-karty”.

Poprawki po sprawdzeniu wersji 2027-02-28 na stronie (przetarg BZP 2026/BZP 00544691, 80 plików z BZP).

**Pobieranie dokumentów (W3)** – plik `modul_oferty.py`
- Archiwa ZIP: pomijane pliki systemowe (Thumbs.db, .DS_Store, desktop.ini, __MACOSX) – wcześniej „Thumbs.db” trafiał do dokumentów jako „Thumbs.db.doc”.
- Archiwum z jednym folderem o tej samej nazwie co archiwum nie tworzy już podwójnego folderu („Załącznik nr 9…/Załącznik nr 9…”).

**Błędy i ryzyka (W4)** – pliki `odwolania.py`, `trasy_projekty_wykonawcy.py`
- Sprawdzanie cytatów czyta tylko pliki uwzględnione w projekcie. Wcześniej czytało też pominięte (duże rysunki, skany) – na stronie trwało to ponad 2 minuty.

**Złożenie oferty (W8)** – plik `serwer.py`
- „Cofnij” przy złożonej ofercie przywraca status przetargu sprzed zapisu i usuwa decyzję „oferta złożona / wygrany / przegrany” (wcześniej zostawała jako wskazówka dla AI przy kolejnych ocenach).

Sprawdzono: testy wykonawca_* (9), 12 testów modułów, regresja adresów (319 adresów, 0 błędów).

---

## Wersja „2027-02-28 wykonawca-karty”

Poprzednia wersja: „2027-02-27 zamawiajacy-przepisy-ai”.

Zmiany z kart „Zasady działania – Wykonawca” (W1–W8, ścieżka „Znajdź przetarg i złóż ofertę”). Każda karta sprawdzona testem
na danych testowych (wykonawca_*_test.py); poniżej błędy, które testy wykazały, i ich poprawki.

**Cena ofertowa (W6)**
- Błąd krytyczny: korekta ceny nie obejmowała pozycji z wariantem rozwiązania (np. rynny PCV / tytan-cynk) – przy zapisie wariant wracał do
  ceny sprzed korekty. Cena docelowa 100 000 zł brutto dawała 102 340,93 zł, korekta −5% dawała −4,33%. Teraz warianty są ustalane na danych
  pierwotnych przed korektą, a przy zapisie cena wariantu jest mnożona przez ten sam współczynnik co pozostałe pozycje (zapamiętany w korekcie).
- Decyzja o pozycji spoza przedmiaru albo o wariancie usuwała korektę ceny bez informacji. Teraz zmiana działa na danych pierwotnych, korekta
  procentowa zostaje i jest stosowana do nowego zakresu; komunikat podaje nową cenę (cena wpisana kwotą zamienia się na korektę procentową).
- Ceny poprawione ręcznie (po kontroli kosztorysu, w edycji pozycji) są stałe przy korekcie – korektę przejmują pozostałe pozycje; cena 66 zł
  wpisana przy korekcie +10% zostaje 66 zł (wcześniej 72,60 zł).
- Identyfikator uwagi kontroli nie zależy już od kwot w opisie – decyzja „odstępstwo” zostaje po korekcie ceny.

**Błędy i ryzyka w dokumentach (W4)**
- Podstawa pytania do zamawiającego według trybu: tryb podstawowy art. 284 Pzp, procedura unijna art. 135 Pzp, poza Pzp – bez powoływania Pzp
  (wcześniej zawsze art. 135).
- W kroku widać ostatni dzień na pytania z obowiązkiem odpowiedzi: 4 dni (tryb podstawowy) / 14 dni (procedura unijna) przed terminem składania
  ofert; dzień wolny – z praktycznym ostatnim dniem roboczym; po terminie – informacja, że zamawiający może nie odpowiedzieć. Ten sam termin
  w panelu rozbieżności.
- Zmiana dokumentów po sprawdzeniu (wgranie, pobranie, usunięcie, uwzględnij / pomiń) oznacza wynik jako nieaktualny – komunikat w kroku.

**Kosztorys (W5)**
- Ceny rynkowe w poleceniu dla AI nie są już „dla Dolnego Śląska” – region z miejsca realizacji w dokumentach, a gdy nie wynika – z obszaru
  konta / adresu firmy, inaczej średnie krajowe; przyjęty region trafia do „Do weryfikacji”.
- Usunięty nieużywany wariant zasad wyceny z cennikiem jednej firmy (konkretne ceny i adres).
- Teksty o VAT w kroku 2: stawkę ustala wykonawca (roboty 23%, 8% tylko budownictwo objęte społecznym programem mieszkaniowym).

**Komplet oferty (W7)**
- Plik „Gwarancja wadialna.pdf” rozpoznawany jako dowód wadium (wcześniej pokazywany brak).

**Wynik oferty (W8)**
- Wynik (wygrany / przegrany) i złożenie oferty zapisują się w pamięci decyzji firmy – kolejne oceny AI je uwzględniają.
- Kalkulator szans: „kwota na sfinansowanie (brutto)” domyślnie pusta – nie jest już wypełniana szacowaną wartością netto ani szacunkiem AI
  (fałszywe ostrzeżenia o przekroczeniu kwoty).

Pliki: `serwer.py`, `zamawiajacy.py`, `trasy_projekty_wykonawcy.py`, `modul_oferty.py`, `rozbieznosci.py`, `kontrola.py`, `app.js`, `ZMIANY.md`.
Testy: 8 testów kart Wykonawcy (wykonawca_*_test.py) – 0 błędów, 0 zmian do wprowadzenia; 13 testów modułów i regresja adresów – 0 błędów.

---

## Wersja „2027-02-27 zamawiajacy-przepisy-ai”

Poprzednia wersja: „2027-02-26 zamawiajacy-kontrole”.

Sprawdzenie wersji 2027-02-26 na stronie (22.11.2026, prawdziwy klucz AI): gmina – świetlica 900 000 zł, tryb podstawowy, komplet 5 dokumentów,
sprawdzenie (69 propozycji), wprowadzenie zmian, pisma z listy kontrolnej; wspólnota – remont klatek. Kontrole bez AI działały jak w kartach.
Wykryte błędy dotyczyły treści pisanej przez AI:

- Błąd krytyczny: sprawdzenie dokumentów (krok 6) proponowało przedłużenie związania ofertą o 60 dni w trybie podstawowym (art. 307 ust. 2 Pzp:
  najwyżej 30 dni) z dopiskiem „co najmniej na 3 dni przed upływem” (dawna ustawa). Po przyjęciu propozycji błąd trafiał do SWZ i formularza.
  Przyczyna: polecenie sprawdzenia nie zawierało parametrów ustawowych trybu (miało je tylko pisanie dokumentów).
  Teraz: parametry ustawowe trybu są w poleceniu sprawdzenia; propozycja sprzeczna z nimi dostaje wagę „krytyczna” i dopisek
  „UWAGA PROGRAMU – zalecane: odrzuć”, więc wymaga decyzji.
- Błąd: SWZ i oświadczenia podawały, że oświadczenie o grupie kapitałowej składa się w 3 dni od otwarcia ofert (art. 24 ust. 11 dawnej ustawy).
  Teraz parametry ustawowe mówią, że to podmiotowy środek dowodowy składany na wezwanie.
- Nowa kontrola dokumentów (bez AI): zapisy sprzeczne z Pzp (przedłużenie związania ponad limit trybu, „3 dni przed upływem związania”,
  grupa kapitałowa „w 3 dni”) są wyszukiwane w dokumentach; wynik to błąd w kroku „Komplet dokumentów” / „Sprawdzenie i zmiany”
  i brak w stanie „Gotowe do publikacji”.
- Termin składania ofert w sobotę, niedzielę albo święto: ostrzeżenie w kroku „Warunki” z najbliższym dniem roboczym. Wcześniej AI przesuwało
  termin w dokumentach (13.12 → 14.12), a kalendarz postępowania i pisma liczyły od daty z kreatora. Teraz sprawdzenie AI nie zmienia
  terminu ustalonego w kreatorze.
- Protokół wyboru oferty (wspólnota) i protokół postępowania (gmina) wypełnia się po otwarciu ofert (na stronie: 110 pól) – nie są liczone jako brak „pól do uzupełnienia” przed publikacją.
- Procedura unijna: parametry ustawowe uzupełnione o przedłużenie związania ofertą o najwyżej 60 dni (art. 220 ust. 3 Pzp).

Pliki: `kontrola_zam.py`, `trasy_kreator.py`, `zamawiajacy.py`, `serwer.py` (wersja), `ZMIANY.md`.
Testy: zamawiajacy_zmiany_test.py rozszerzony o 9 sprawdzeń (razem 104); 13 testów modułów i regresja adresów – 0 błędów.

---

## Wersja „2027-02-26 zamawiajacy-kontrole”

Poprzednia wersja: „2027-02-25 widok-krokow”.

Komplet zmian modułu Zamawiający (gmina i wspólnota) po opisaniu zasad działania kreatora zamówienia, finansowania i postępowania
po publikacji. Po tej wersji prototyp działa tak, jak opisują karty „Zasady działania – Zamawiający”.
Nowy plik: `kontrola_zam.py` (kontrole kreatora bez AI). Do usunięcia z repozytorium: `szacowanie_web.py` – plik nigdzie niepodłączony.

**Krok 1 – Nowe zamówienie**
- Błąd krytyczny: budżet wpisany jako „200 000 zł”, „200.000,00” albo „ok. 200 tys.” zakładał projekt, którego kreator się nie otwierał
  (błąd serwera). Teraz kwota jest zamieniana na liczbę przy zapisie; zapis nieliczbowy jest odrzucany z komunikatem.
- Opis wymagany także na serwerze (poza startem z dokumentów). Nazwa nadana z opisu (90 znaków) jest tymczasowa – zastąpi ją nazwa z dokumentów.
- Ostrzeżenie o powtórzonym zamówieniu (ta sama nazwa albo pozycja planu) z wyborem: otwórz istniejące albo załóż nowe.
- Dokumenty źródłowe: limit 10 plików z listą pominiętych; ZIP także na ekranie startowym.
- Odczyt z dokumentów: gdy AI i tekst podają różne kwoty, żadna nie jest zapisywana do czasu wyboru; rodzaj zamówienia inny niż wybrany
  trafia na listę sprzeczności.

**Krok 2 – Szczegóły**
- Pola wymagane (roboty: obiekt, zakres, termin; dostawy: przedmiot, miejsce, termin; usługi: przedmiot, ilości, okres) – krok niepełny jest oznaczony.
- Limity 500 / 10 000 znaków; tekst ponad limit nie jest obcinany po cichu (odmowa zapisu). Odrzucane nieznane pola i wartości spoza list.
- Zmiana rodzaju zamówienia odkłada stare odpowiedzi (wcześniej gwarancja z dostaw trafiała do dokumentów robót) i przywraca je po powrocie.
- Termin z opisu: rozpoznawane daty i nazwy miesięcy („do 20 sierpnia 2027”), nie „do dachu 2027”. Opis nie jest powtarzany w dokumentach.
- „Tylko PFU”, „brak przedmiaru” i „prawo opcji” dają podpowiedzi w kroku „Wartość i tryb”.

**Krok 3 – Wartość, tryb, części**
- Gmina: tryb liczony z budżetu albo kwoty ręcznej ma dopisek „orientacyjnie”; krok niezaliczony i komplet dokumentów zablokowany do szacowania.
- Szacowanie: korekty nie mogą dać wartości ujemnej; aktualność 3 / 6 miesięcy liczona miesiącami kalendarzowymi (wcześniej 2.08 przy
  wszczęciu 2.11 było błędnie odrzucane); data ustalenia późniejsza niż wszczęcie albo przyszła – błąd; zmiana zakresu po szacowaniu wymaga
  ponownego zapisu szacowania.
- Progi: zamawiający centralny (140 000 euro), usługi społeczne (750 000 euro, art. 359 Pzp), ostrzeżenie o aktualizacji progów po 31.12.2027.
- Brak wartości = „tryb nieustalony” (wcześniej „poniżej progu”). Różnicę krytyczną w trybie potwierdza się tylko z pisemnym uzasadnieniem.
- Minimalny termin ofert w przetargu nieograniczonym: 30 dni (art. 138 ust. 4 – oferty elektroniczne), wcześniej 35.
- Brak podziału na części wymaga uzasadnienia; w dokumentach nie zostaje „[UZUPEŁNIJ: uzasadnienie braku podziału]”.
- Błąd: zapis podziału na części nadpisywał moduł pomocniczy programu (`S.W`) – późniejszy odczyt dokumentów kończył się błędem.

**Krok 4 – Warunki** (nowa kontrola przy zapisie – wcześniej program przyjmował wszystko)
- Kryteria: każde z wagą w procentach, suma 100%; cena powyżej 60% – ostrzeżenie (art. 246). Wadium: 1,5% w trybie podstawowym, 3% w unijnym.
  Zabezpieczenie: do 5%, 5–10% z ostrzeżeniem, powyżej 10% błąd. Kary: wymagany łączny limit. Płatność: najwyżej 30 dni. Termin ofert: nie krótszy
  niż minimum (gmina – błąd, wspólnota – ostrzeżenie). Godzina w zapisie GG:MM. Błędy blokują zaliczenie kroku i komplet dokumentów.
- Próg doświadczenia liczony z właściwej stawki VAT. Poprawione objaśnienia pól: art. 246 ust. 2 (wymagania jakościowe), art. 281 ust. 4
  i art. 299 ust. 3 (wadium), art. 453 (zwrot zabezpieczenia), termin zapłaty (nie art. 447 Pzp).

**Kroki 5–7 – Dokumenty, sprawdzenie, gotowość**
- Komplet bez wskazania dokumentów = komplet dla trybu (wcześniej wszystkie 12 rodzajów). Krok zaliczony dopiero przy wszystkich dokumentach
  kompletu; dokument nieudany jest wymieniony. Licznik pól „[UZUPEŁNIJ” przy dokumentach (puste pola dla wykonawcy w formularzu
  i oświadczeniach się nie liczą).
- Procedura unijna: AI dostaje parametry ustawowe (związanie ofertą 90 / 120 dni, wyjaśnienia 6 / 14 dni, termin 30 / 35 dni, JEDZ).
- „Wprowadź zmiany” wymaga decyzji przy każdej propozycji krytycznej i istotnej (wcześniej zatwierdzało krok bez żadnej decyzji).
  Ponowne sprawdzenie ostrzega o utracie decyzji.
- „Twoje wzory”: limit 10 plików, krok zalicza wzór SWZ / zapytania albo umowy, zastąpienie wzoru z propozycjami wymaga potwierdzenia,
  informacja przy plikach .doc i .odt.
- Stan „gotowe / niegotowe” z listą braków (kroki, lista kontrolna, pola do uzupełnienia, sprawy do decyzji, zmiany ręczne) – także na
  początku pliku CZYTAJ w archiwum ZIP. „Nie dotyczy” wymaga powodu. Pozycje sprawdzane w kroku 6 zaliczają się po jego zatwierdzeniu.
  Sprawy „do decyzji” można oznaczać jako rozstrzygnięte.

**Postępowanie po publikacji**
- Przedłużenie terminu składania ofert nie przesuwa terminu na wnioski o wyjaśnienie (art. 284 ust. 5, art. 135 ust. 4); zamawiający może
  świadomie przyjąć liczenie od nowego terminu.
- Kalendarz uwzględnia polskie święta (wcześniej tylko soboty i niedziele); przy terminie odpowiedzi w dzień wolny – dopisek o ostatnim dniu roboczym.
- Otwarcie ofert: art. 222 ust. 1 (wcześniej art. 221). Pismo z wyjaśnieniami: miejscowość, godzina, termin otwarcia i związania ofertą
  wpisywane przez program; tylko odpowiedzi zatwierdzone (projekt AI nie jest odpowiedzią); odpowiedź z „[DO DECYZJI ZAMAWIAJĄCEGO” nie daje
  się zatwierdzić; data pytania nie może być przyszła. Poniżej progu – bez terminów ustawowych.

**Kosztorys gminy** – poprawiona uwaga z wersji 02-24: kosztorys przygotowany przez program to materiał pomocniczy i nie jest podstawą
wartości zamówienia (tytuł: „WSTĘPNY KOSZTORYS ROBÓT (MATERIAŁ POMOCNICZY)”).

Przepisy sprawdzone w tekście jednolitym Pzp (Dz.U. z 2026 r. poz. 793, wersja 12.07–30.11.2026). Od 1.12.2026 obowiązuje nowa wersja.

Ograniczenia: polecenia dla AI nie były sprawdzone na prawdziwej odpowiedzi (brak klucza API w środowisku testowym). Zamówienia założone
wcześniej z budżetem wpisanym słownie otworzą się, ale budżet będzie pusty. Kontrola warunków czyta procenty i kwoty z tekstu – nietypowy
zapis może nie zostać rozpoznany.

Sprawdzenie: nowy `zamawiajacy_zmiany_test.py` – 95 kontroli, 0 błędów; pozostałe 12 testów i regresja adresów – 0 błędów; kreator otwarty
w przeglądarce na szerokości komputera i telefonu – brak błędów skryptu.


---

## Wersja „2027-02-25 widok-krokow”

Poprzednia wersja: „2027-02-24 kosztorys-wszedzie”.

- Wykonawca, przetarg dodany ręcznie (bez ogłoszenia z wyszukiwarki): projekt nie miał przełącznika „Widok szybki / Pokaż wszystkie
  kroki”, a po otwarciu wcześniej innego projektu dziedziczył po nim ukrycie sekcji. Teraz każdy projekt przetargowy ma ten sam
  przełącznik i pasek „Co dalej”, a ustawienie widoku nie przenosi się między projektami.
- Projekt w realizacji (wygrany): sekcja „Zmiany umowy: wnioski i aneksy” jest widoczna także w widoku szybkim.

Błąd istniał we wcześniejszych wersjach (co najmniej od 02-14), nie powstał w wersji 02-24.

Sprawdzenie: otwarcie trzech projektów wykonawcy po kolei w przeglądarce (komputer i telefon) – przełącznik w każdym, brak błędów
skryptu; testy i regresja adresów – 0 błędów.


---

## Wersja „2027-02-24 kosztorys-wszedzie”

Poprzednia wersja: „2027-02-23 warianty”.

Przegląd kosztorysowania we wszystkich modułach (wykonawca, dostawca, Kosztorysowanie, projekt własny, budowa domu, zamawiający
publiczny, wspólnoty, wniosek o roboty dodatkowe) – jedne reguły zamiast kilku różnych.

- Sprawdzanie cen w internecie – jedna zasada: pozycje tworzące razem 80% wartości kosztorysu, nie mniej niż 15 najdroższych
  i nie więcej niż 90; zapytania po 15 pozycji. Wcześniej zawsze tylko 15 najdroższych, niezależnie od wielkości kosztorysu.
  Nowe ustawienia: udział wartości (80) i górna granica (90); dotychczasowe „ile pozycji” jest teraz minimum (0 wyłącza).
  Gdy jedna z części zapytań się nie uda, pozostałe ceny zostają – dziennik mówi, których pozycji nie sprawdzono.
- Dostawy i usługi: osobne polecenia wyszukiwania cen (towar o podanych parametrach; stawka usługi z kosztami pracy).
  Wcześniej program pytał o „cenę wykonania robót z materiałem, robocizną i sprzętem” także dla towarów i usług.
- Region cen: usunięto „Dolny Śląsk” wpisany na stałe (kosztorys, zestawienie materiałów). Region wynika z dokumentów, a gdy
  ich brak – z miejsca realizacji w kreatorze albo z adresu / obszaru działania konta; gdy i tego brak – średnie ceny krajowe
  z wpisem do weryfikacji.
- Wspólnoty, spółdzielnie, deweloperzy: kosztorys nie jest już pisany jak dla gminy. Polecenie dla AI bez przepisów Pzp,
  bez „przetargu” i „wartości zamówienia”; VAT jako koszt inwestora (8% / 23%). Tytuły: „KOSZTORYS INWESTORSKI”,
  „SZACUNKOWY KOSZT USŁUG”, „SZACUNKOWY KOSZT DOSTAW”.
- Zamawiający publiczny, roboty: kosztorys przygotowany przez program nazywa się „WSTĘPNY KOSZTORYS ROBÓT (KOSZTORYS INWESTORSKI
  DO ZATWIERDZENIA)” i ma na górze listy uwagę, że podstawą wartości staje się po podpisaniu przez osobę opracowującą
  i zatwierdzeniu w kroku „Szacowanie wartości” (albo po wgraniu kosztorysu projektanta / PFU). Usunięto sprzeczność między
  modułem szacowania („AI nie sporządza kosztorysu inwestorskiego”) a krokiem kosztorysu.
- Zamawiający (gmina i wspólnota), roboty: widzi niespójności własnej dokumentacji – roboty wymagane dokumentacją, których nie ma
  w przedmiarze (ujęte w wartości), i pozycje z dwoma rozwiązaniami w dokumentach. Do wartości przyjmowany jest wariant z dokumentu
  nadrzędnego, a gdy go brak – droższy; zamawiający może wskazać obowiązujący. Uwaga na liście: poprawić przedmiar i ujednolicić
  dokumenty przed ogłoszeniem. Wcześniej panel był u zamawiającego ukryty.
- Wniosek o roboty dodatkowe: ceny nowych robót (nie z kosztorysu ofertowego) są sprawdzane w internecie tak samo jak w kosztorysie
  oferty. Cen przyjętych z oferty, z cennika firmy i poprawionych ręcznie program nie zmienia.
- Błąd w przepisach: szacowanie wartości powoływało starą numerację (Pzp z 2004 r.). Poprawiono w dokumentach i interfejsie:
  roboty budowlane – art. 34 ust. 1 Pzp, zamówienia powtarzające się – art. 35 ust. 1, termin ustalenia wartości – art. 36
  (sprawdzone w tekście ustawy z 11.09.2019 r. i w podstawie prawnej rozporządzenia z 20.12.2021 r.).

Bez zmian (świadomie): osobny przycisk dostawcy „sprawdź ceny” sprawdza wszystkie pozycje formularza; badanie rynkowości ofert
u zamawiającego i prawnika – 80% wartości albo wszystkie; plan budżetu dotacji – wszystkie pozycje.

Ograniczenia: większy kosztorys to więcej zapytań z wyszukiwaniem (do 6 zamiast 1) – wycena trwa dłużej i kosztuje więcej.
Nowe polecenia dla AI nie były sprawdzone na prawdziwej wycenie (brak klucza API w środowisku testowym) – logikę sprawdzono
na podstawionych odpowiedziach. Niespójności dokumentacji u zamawiającego pojawią się po ponownej wycenie.

Sprawdzenie: nowy `kosztorys_wszedzie_test.py` – 36 kontroli, 0 błędów; `rozbieznosci_test.py` – 54 kontrole, 0 błędów;
pozostałe testy i regresja adresów – 0 błędów.


---

## Wersja „2027-02-23 warianty”

Poprzednia wersja: „2027-02-22 rozbieznosci”.

- Rozbieżności wariantowe: gdy dokumenty podają dla tej samej pozycji przedmiaru różne rozwiązania (materiał, wymiar, grubość, liczba
  warstw – np. rynny tytan-cynk Ø10 w przedmiarze i stal powlekana Ø150 w OPZ), program nie wybiera już po cichu jednego z nich.
  AI ma zwrócić oba warianty z cenami jednostkowymi (nowe pole „warianty” w odpowiedzi; wariant A to zawsze przedmiar).
- Który wariant jest w cenie, ustala program według jednej reguły: decyzja wykonawcy, a bez niej dokument nadrzędny wskazany w SWZ /
  zapytaniu / umowie; gdy dokumenty nie ustalają pierwszeństwa – wariant droższy. Wcześniej AI wybierała raz przedmiar, raz OPZ.
- Krok „Kosztorys i oferta”: nowa tabela „Różne rozwiązania w dokumentach” – oba warianty ze źródłem i ceną, różnica w złotych
  dla ilości pozycji, wybór wariantu i zaznaczenie „pytanie do zamawiającego” (gotowe pytanie trafia na listę pytań).
  Wybór zostaje po ponownej wycenie. Ceny poprawionej ręcznie program nie nadpisuje, dopóki wykonawca sam nie wybierze wariantu.
- Lista „Do weryfikacji” ma jedną uwagę o wariantach z liczbą pozycji bez decyzji.
- Wniosek o roboty dodatkowe: przy robocie dopasowanej do pozycji, która miała dwa warianty, program podpowiada, że wykonanie innego
  wariantu niż w cenie to robota zamienna.
- Kosztorys inwestorski i formularz cenowy dostawcy: warianty nie zmieniają cen.

Ograniczenie: warianty pojawią się dopiero po ponownej wycenie projektu przez AI. W projektach wycenionych wcześniej tabela jest pusta.
Nowe polecenie dla AI nie było sprawdzone na prawdziwej wycenie (brak klucza API w środowisku testowym) – logikę sprawdzono
na podstawionych danych.

Sprawdzenie: `rozbieznosci_test.py` rozszerzony o warianty – 52 kontrole, 0 błędów; pozostałe testy – 0 błędów.


---

## Wersja „2027-02-22 rozbieznosci”

Poprzednia wersja: „2027-02-21 kosztorys-uklady”.

- Wniosek o roboty dodatkowe wyceniał drugi raz roboty ujęte już w cenie oferty (przypadek Kamionki: wniosek W/1/2026 na 242 327,54 zł netto,
  w którym 19 z 20 pozycji miało odpowiednik w kosztorysie ofertowym na 342 892,13 zł). Przyczyna: wniosek „różnice dokumentacji” brał
  wszystkie uwagi z etapu oferty i wyceniał je od nowa, nie sprawdzając kosztorysu ofertowego.
  Teraz: program porównuje każdą robotę wniosku z kosztorysem ofertowym i pomija te, które są w cenie. Lista pominiętych jest widoczna
  w edytorze wniosku z numerem pozycji oferty i kwotą. Błędne dopasowanie można uchylić dopiskiem „; mimo to: powód” w wierszu roboty.
- Roboty zamienne: dopisek „; zamienna” w wierszu roboty. Kosztorys wniosku odejmuje wtedy pozycje kosztorysu ofertowego, które
  nowe rozwiązanie zastępuje (dział „Odliczenie robót zastępowanych”), zamiast doliczać pełną cenę.
- Rozbieżności z przedmiarem (krok „Kosztorys i oferta”): każda pozycja spoza przedmiaru ma decyzję wykonawcy – ujęte w cenie oferty,
  pytanie do zamawiającego (do odpowiedzi w cenie), zostawione na etap umowy, nie dotyczy. Pozycje zostawione na etap umowy i „nie dotyczy”
  nie wchodzą do ceny; decyzja zostaje po ponownej wycenie. Program pokazuje rodzaj wynagrodzenia, podpowiedź i termin na pytania
  (4 dni przed terminem ofert). Przy ryczałcie zostawienie pozycji na etap umowy wymaga potwierdzenia ostrzeżenia.
- Nowy wniosek zaczyna od robót zostawionych przy ofercie na etap umowy – to jedyne rozbieżności z etapu oferty, które wolno w nim wycenić.
- Wniosku o zmianę umowy nie da się utworzyć bez daty umowy.
- Wniosek z polem „[UZUPEŁNIJ]” w kosztorysie nie jest generowany; AI ma zakaz używania tego znacznika w kosztorysie wniosku.
- Poprawiony błąd: ceny z kosztorysu ofertowego nie trafiały do polecenia wyceny wniosku (lista była zawsze pusta), więc te same roboty
  dostawały inne ceny niż w ofercie. To samo dotyczyło listy pozycji oferty w propozycji wniosku.
- AI przy propozycji wniosku dostaje listę robót opłaconych ceną umowy i zakaz proponowania ich ponownie.

Ograniczenie: dopasowanie robót działa po opisie, więc może oznaczyć robotę podobną do pozycji oferty (np. „dodatkowa stacja naprawcza
w trzeciej lokalizacji”) albo nie rozpoznać roboty opisanej zupełnie innymi słowami. Dlatego lista pominiętych jest jawna i można ją poprawić.

Sprawdzenie: nowy test `rozbieznosci_test.py` (dane z Kamionek: kosztorys ofertowy i wniosek W/1/2026) – 32 kontrole, 0 błędów;
pozostałe testy (konta, pozostałe moduły, wykonawca, realizacja, dostawca, przejmij, układy kosztorysu, regresja adresów) – 0 błędów.
Wyceny przez AI sprawdzono z podstawioną odpowiedzią, bez prawdziwego klucza API.


---

## Wersja „2027-02-21 kosztorys-uklady”

Poprzednia wersja: „2027-02-20 obszar”.

- Zapotrzebowanie materiałowe: błąd „Nie znaleziono pozycji – sprawdź, czy plik ma wiersz nagłówka zaczynający się od „Lp.””.
  Odczyt kosztorysu rozumiał tylko jeden układ: pierwszy arkusz, nagłówek „Lp.” w kolumnie A, numer pozycji jako liczba.
  Własny kosztorys w innym układzie (np. „L.p.”, numery „1.” albo „1.1” jako tekst, tabela od kolumny B, drugi arkusz) dawał zero pozycji.
- Teraz odczyt przegląda wszystkie arkusze i rozpoznaje typowe układy: nagłówek w dowolnym wierszu i kolumnie, nazwy kolumn
  Lp. / L.p. / Nr / Poz.; Opis / Nazwa / Wyszczególnienie; J.m. / Jedn.; Ilość / Obmiar / Przedmiar; Cena; liczby zapisane tekstem
  z przecinkiem; numery 1.1 / 1.2; działy; wiersz numerów kolumn i „Razem” pomijane; także tabela bez nagłówka i bez kolumny Lp.
  Gdy pozycji naprawdę nie ma, komunikat mówi, czego brakuje (opis, jednostka, ilość). Dotyczy też innych miejsc czytających kosztorys.
- Sprawdzono: nowy test kosztorys_uklady_test.py (9 sprawdzeń; kosztorys z programu czytany identycznie jak dotąd, przedmiar z testów:
  25 pozycji zamiast 0), testy wykonawca, realizacja, dostawca, pozostale_moduly, modul_konta, przejmij,
  regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-20 obszar”

Poprzednia wersja: „2027-02-19 logintrade-duble”.

- Przyczyna kłopotów ze zmianą obszaru „okolica + promień”: zapis obszaru zależał od zewnętrznych serwisów map (OpenStreetMap).
  Lista miejscowości w promieniu szła z serwisu Overpass (w teście: brak odpowiedzi po 93 s i błąd; dwa adresy po 90 s to więcej
  niż limit 120 s serwera, więc serwer mógł się przy tym restartować i przerywać zadania w tle), województwa obszaru – 5 zapytań
  do Nominatim (7 s), a położenie miejscowości z ogłoszeń ustalane było po 300 na noc.
- Teraz program ma wbudowany wykaz ok. 45 tys. miejscowości Polski z położeniem (nowe pliki miejscowosci.py i miejscowosci_dane.py;
  dane GeoNames, licencja CC BY 4.0). Podpowiedzi, miejscowości w promieniu, województwa obszaru i położenie miejscowości z ogłoszeń
  liczone są lokalnie: zapis obszaru trwa ok. 0,01 s i nie może się nie udać z powodu map. Serwis map zostaje tylko awaryjnie
  (nazwa spoza wykazu).
- Wyszukiwarka, krok 2: miejscowość można po prostu wpisać (także bez polskich znaków) i kliknąć „Szukaj” – nie trzeba wybierać
  z listy. Podpowiedzi mają pełny opis („Świdnica, pow. zielonogórski, lubuskie”), więc da się wybrać właściwą z kilku o tej samej
  nazwie. Po wyszukaniu pole pokazuje nową miejscowość (wcześniej wracała stara nazwa, choć obszar był już zmieniony).
  Nieznana nazwa – czytelny komunikat, obszar bez zmian. To samo w panelu obszaru w Ustawieniach (bez obowiązkowego „Znajdź”).
- Trafniejsze wyniki w okolicy: miejscowość o tej samej nazwie w innej części województwa nie daje już trafienia (tytuł „Remont drogi
  w Łomnicy” zamawiającego z Mysłakowic to Łomnica koło Mysłakowic, nie ta koło Wałbrzycha), a nazwy wsi będące zwykłymi słowami
  („Centrum”, „Naprawa”, „Mienia”) nie służą do dopasowania po tytule.
- Sprawdzono: nowy test obszar_test.py na prawdziwych ogłoszeniach BZP/TED (17 sprawdzeń; Wałbrzych + 20 km: 8 przetargów,
  + 50 km: 51, zmiana na Świdnicę lubuską: lista tylko z nowego obszaru; zero zapytań do serwisów map), test w przeglądarce
  (cztery zmiany obszaru pod rząd), testy przejmij, modul_konta, pozostale_moduly, wykonawca, realizacja, dostawca,
  regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-19 logintrade-duble”

Poprzednia wersja: „2027-02-18 wyszukiwanie”.

- Pobieranie dokumentów z platformy Logintrade (np. gminawalbrzych.logintrade.net). Ogłoszenie TED podaje tylko adres platformy,
  a jej strona główna to logowanie – program nie znajdował postępowania. Teraz szuka go po tytule na listach platformy
  („Zamówienia publiczne”, 2 strony, i „z wyłączeniem ustawy”) i pobiera publiczne załączniki (bez logowania, nazwy plików z serwera).
  Sprawdzone na „Przebudowa budynku hotelowego nr 6 … Zamku Książ”: 20 plików (ogłoszenie, SWZ, projekt umowy, formularze,
  dokumentacja projektowa w ZIP). Przy braku pasującego tytułu – czytelny komunikat, bez pobierania plików innego przetargu.
- Ten sam przetarg tylko raz na liście. Wcześniej to samo postępowanie pokazywało się kilka razy: z BZP i z TED (inne numery)
  oraz z list innych kont w widoku administratora – każde z inną oceną. Teraz jedna pozycja (pierwszeństwo: własna z projektem,
  własna z decyzją, własna, na końcu z innego konta) ze znacznikami „też u: kaska, marek” i „też w TED/BZP”.
  Wyszukiwanie nie dopisuje dubla z drugiego źródła, a „Przygotuj ofertę” z drugiego numeru otwiera istniejącą ofertę.
- Sprawdzono: przejmij_test.py rozszerzony o duble (14 sprawdzeń), test pobierania z Logintrade na żywej platformie;
  testy modul_konta, pozostale_moduly, wykonawca, realizacja, dostawca, regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-18 wyszukiwanie”

Poprzednia wersja: „2027-02-17 limit-50mb”.

- Wyszukiwanie nie czeka już na całe nocne pobranie. Wcześniej, gdy pamięć ogłoszeń nie miała zapisanego zakończonego pobrania
  (np. po restarcie serwera, wdrożeniu albo przerwanym pobraniu), każde wyszukiwanie uruchamiało pełne pobieranie: BZP, TED,
  rozstrzygnięcia z 16 województw za 21 dni, Bazę Konkurencyjności (400 stron) i położenia miejscowości – kilkanaście minut i więcej,
  a w tym czasie nie było wyników. Teraz: gdy ogłoszenia BZP są w pamięci, wyszukiwanie od razu je filtruje (kilka sekund);
  przy całkiem pustej pamięci pobiera tylko BZP i TED, a resztę robi pobranie w tle. Gdy pobieranie w tle trwa, wyszukiwanie czeka
  tylko na ogłoszenia BZP/TED. Test: 14 543 ogłoszenia przejrzane w 3 s (wcześniej po 9 min nadal bez wyniku).
- Trafniejsze dopasowanie słów: słowo musi zaczynać wyraz („dach” → „dachu”, ale już nie „zakładach”), a stałe formułki BZP
  („drogą elektroniczną”) nie dają trafień dla słowa „droga”.
- Sprawdzono: wyszukiwanie na prawdziwych danych BZP/TED (woj. dolnośląskie, „termomodernizacja”, „remont”: 157 ogłoszeń);
  testy przejmij, modul_konta, pozostale_moduly, wykonawca, realizacja, dostawca, regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-17 limit-50mb”

Poprzednia wersja: „2027-02-16 nowy-uklad”.

- Dokumenty do AI: limit podniesiony z 28 MB do 50 MB na jedno zadanie (oferta, kosztorys, analiza, weryfikacja, asystent).
  Jedno zapytanie do API Anthropic przyjmuje najwyżej 32 MB, więc gdy dokumentów jest więcej, największe pliki (PDF, zdjęcia)
  program wysyła osobno przez Files API, a w zapytaniu zostaje tylko ich identyfikator. Pliki są usuwane z konta Anthropic po godzinie.
  Licznik „Do AI: … z 50 MB”, komunikaty i instrukcja zaktualizowane. Zbyt duża liczba tokenów (limit modelu) ma osobny, jasny komunikat.
- Administrator może ofertować przetarg widoczny na liście innego konta (podgląd administratora): „Przygotuj ofertę u siebie”
  albo „Dodaj do mojej listy”. Na liście administratora powstaje kopia (status „nowy”), lista i oferta tamtego konta zostają bez zmian.
  Nowy adres POST /api/przetargi/przejmij (tylko administrator).
- Telefon: strona nie przesuwa się w bok (długie kwoty w kafelkach przetargu łamią się w kafelku).
- Sprawdzono: nowy test przejmij_test.py (11 sprawdzeń), test wysyłki ponad 32 MB na atrapie API (2 pliki przez Files API, zapytanie 4 MB),
  zrzuty telefonu; testy modul_konta, pozostale_moduly, wykonawca, realizacja, dostawca, regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-16 nowy-uklad”

Poprzednia wersja: „2027-02-15 nowy-wyglad”.

- Sposób wyświetlania jak w nowej aplikacji – mechanika bez zmian (te same przyciski, funkcje i adresy; nowy plik static/uklad.js tylko przestawia widok).
- Komputer: górny pasek na całą szerokość (logo, wyszukiwarka, użytkownik), pod nim menu boczne. Grupy „Firma” i „Program” zwijane
  (stan zapamiętany w przeglądarce, grupa z otwartą stroną zawsze rozwinięta). Podmenu sekcji z linią po lewej i zaznaczonym bieżącym krokiem.
- Projekt: zamiast jednej długiej strony – jeden krok na ekranie i panel „Kroki” po prawej (numery, ✓ dla zrobionych, stan kroku,
  „Poprzedni / Następny krok”). Lista projektów chowa się po otwarciu projektu (przycisk „Pokaż listę projektów”), projekt zajmuje całą szerokość.
  Dotyczy też realizacji, dostaw, oceny ofert i wniosków; kreator zamawiającego ma własne kroki i zostaje bez zmian.
  Linki do sekcji (podmenu, przyciski „przejdź do…”) same przełączają na właściwy krok.
- Telefon: dolny pasek zakładek (Przegląd, Szukaj, Moje oferty, Wygrane, Menu – według widocznych pozycji menu), kroki projektu jako
  przewijane zakładki u góry, przycisk pomocy nad paskiem.
- Sprawdzono: zrzuty 1440 px i 390 px (projekt wykonawcy i zamawiającego, przełączanie kroków), brak błędów skryptów; testy modul_konta,
  pozostale_moduly, wykonawca, realizacja, dostawca, regresja adresów (pełna i zamawiający) – 0 błędów.


---

## Wersja „2027-02-15 nowy-wyglad”

Poprzednia wersja: „2027-02-14 modul-konta”.

- Nowy wygląd całego programu według identyfikacji nowej aplikacji (dev.bidivia.eu): granat #071F49, błękit #729BC5, tło #F4F7FB,
  czcionka Plus Jakarta Sans, karty z cienką ramką i zaokrągleniem 14 px, przyciski główne granatowe, pola 44 px z niebieskim obrysem fokusu.
- Nowe logo (znak „B” z promieniami i napis BIDIVIA) w menu, na stronie logowania, w ofercie publicznej i w ikonach aplikacji na telefon
  (ikony generowane od nowa – nowa nazwa pliku, więc stare nie wracają z pamięci podręcznej).
- Strona logowania jak w nowej aplikacji: granatowy panel z hasłem „Więcej niż przetargi” i promieniami, po prawej formularz logowania,
  oferta dla poszczególnych odbiorców i 6 funkcji programu. Pola formularza i adres wysyłki bez zmian.
- Menu boczne (komputer): białe, aktywna pozycja na jasnym błękicie; górny pasek z wyszukiwarką w kształcie pigułki.
  Tablet i telefon: granatowy nagłówek z białym logo.
- Wybór rodzaju działalności, kafelki pulpitu, kroki projektu, kreator zamówienia, listy projektów, tabele, znaczniki i komunikaty –
  jednolite barwy marki zamiast dotychczasowego morskiego i kolorowych pasków.
- Strona „Nasza oferta” i jej PDF: nowe barwy, logo i czcionka; przycisk „Zaloguj się” granatowy.
- Pozostałe miejsca z kolorami na stałe (wykresy, nagłówki tabel w Excelu, szkice działek w wycenie nieruchomości) – barwy marki.
- Mechanika bez zmian: te same klasy, identyfikatory, adresy i obliczenia; zmieniono wyłącznie wygląd (nowa warstwa na końcu styl.css,
  podmiana kolorów i logo).
- Sprawdzono: zrzuty ekranu (logowanie, wybór działalności, pulpit, wyszukiwarka, projekty wykonawcy i zamawiającego, kreator, ustawienia,
  oferta publiczna, telefon), regresja: testy kont i modułów, wykonawcy, dostawcy, realizacji, pozostałych modułów oraz adresów API
  w edycji pełnej i zamawiającego – 0 błędów.

---

## Wersja „2027-02-14 modul-konta”

Poprzednia wersja: „2027-02-13 vat-realizacja”.

- Użytkownicy strony: nowe pole „Dostęp do modułów”. Administrator może dać kontu dostęp tylko do jednego modułu
  (np. „tylko: Dla wspólnot, spółdzielni i deweloperów”). Do wyboru: wykonawca, dostawca, prawnik, zamawiający publiczny,
  wspólnoty, inwestor, kosztorysant, dotacje, nieruchomości albo „Wszystkie moduły” (domyślnie – bez zmian dla istniejących kont).
- Interfejs takiego konta: od razu wybrany moduł, bez ekranu „rodzaj działalności”, bez przycisku „Zmień tryb” i przejść do innych modułów.
  W module wspólnot zawsze ścieżka prywatna (bez Pzp), w module gminy – publiczna.
- Serwer (nie tylko interfejs): konto nie tworzy projektów innych modułów (także przez kreator, „Realizuj umowę” i kopiowanie kosztorysu),
  nie widzi ich na listach (projekty, realizacja, OLiOC/sprawozdanie), nie otwiera ich i nie pobiera plików, nie używa adresów innych
  modułów (np. wspólnota – wyszukiwarki przetargów, dotacji, kadr i płac) i nie zmienia sobie ograniczenia (blokada kont i ról),
  nawet z rolą administratora. Rola nadal określa poziomy (podgląd / edycja) w ramach modułu. Właściciel programu – bez ograniczeń.
- Zmiana roli lub hasła bez pola modułu nie zdejmuje ograniczenia.
- Sprawdzono: nowy test `modul_konta_test.py` (28 sprawdzeń; na poprzedniej wersji 19 błędów), test interfejsu kont wspólnoty, gminy
  i wykonawcy w przeglądarce (bez błędów przy starcie i na pulpicie), regresja: testy realizacji, dostawcy, wykonawcy, pozostałych modułów,
  oceny ofert, kryteriów oraz adresów API w edycji pełnej i zamawiającego – 0 błędów.

---

## Wersja „2027-02-13 vat-realizacja”

Poprzednia wersja: „2027-02-12 pozostale-moduly”.

- Zamawiający: przy przejściu do realizacji stawka VAT z kreatora („23”) była zapisywana jako 23 zamiast 0,23 – w harmonogramie
  „Brutto etapu” wychodziło ok. 24 razy za dużo (np. 15 021 659,76 zł zamiast 769 880,08 zł). Teraz zapisywane 0,23; dane zapisane wcześniej
  program poprawia przy odczycie, a widok przelicza stawkę podaną w procentach. Znalezione przy nagrywaniu filmu instruktażowego.
- Test: realizacja_krytyczny_test (13 sprawdzeń, nowe nie przechodzi na poprzedniej wersji).

---

## Wersja „2027-02-12 pozostale-moduly”

Poprzednia wersja: „2027-02-11 wykonawca-oferta”.

### Dostawca / usługodawca (test: firma sprzątająca, przetarg na sprzątanie 4 budynków, prawdziwe AI)
- Cena poniżej minimalnych kosztów pracy nie była wykrywana (9 osób na umowę o pracę, cena 409 tys. zł przy minimum ok. 728 tys. zł). Analiza AI
  odczytuje teraz wymagany personel (liczba osób, umowa o pracę, okres), a formularz cenowy na bieżąco pokazuje ostrzeżenie (art. 224 ust. 3 pkt 4,
  art. 226 ust. 1 pkt 8 Pzp) z odnośnikiem do kalkulatora kosztów pracy.
- Płaca minimalna liczona dla okresu umowy, nie „na dziś”: 2027 – 4 950 zł (32,30 zł/h); dla lat bez rozporządzenia – ostatnia znana kwota z uwagą
  o waloryzacji (art. 436 pkt 4 lit. b Pzp).
- Data końca związania ofertą liczona przez program (AI myliła się o dzień): 30 dni, pierwszy dzień = dzień upływu terminu składania ofert.
- Projekt z ogłoszenia o usługi / dostawy trafiał do ścieżki kosztorysu robót, gdy rodzaju nie wybrano ręcznie – rodzaj brany z ogłoszenia.
- Umowa po wygranej: okres z dokumentów (np. 01.04.2027–31.03.2028) zamiast „od dziś”; groszowa reszta podziału w ostatnim okresie (suma okresów
  = wartość umowy); koniec gwarancji – ten sam dzień miesiąca (30.03 + 12 mies. → 30.03, nie 28.03).

### Realizacja umowy (wykonawca i zamawiający)
- Harmonogram rzeczowo-finansowy i protokoły odbioru zawierały dział „Pozycje uzupełniające (poza przedmiarem)” z kosztorysu wewnętrznego.
  Teraz działy z kosztorysu dla zamawiającego (koszty rozłożone na pozycje przedmiaru); harmonogram wykonawcy przeliczany na cenę z umowy.
- Suma etapów harmonogramu różniła się od ceny umowy o grosze (np. 1 877 332,01 zł) – reszta w ostatnim etapie.
- Protokół odbioru: procenty po polsku (86,17%, nie 86.17%).
- Kosztorys po aneksie (dla zamawiającego) zawierał dział „poza przedmiarem” – podstawą jest kosztorys przekazany zamawiającemu.
- Aneks: data zawarcia = data podana przy akceptacji (była „dziś”); wniosek „z dnia” = data złożenia; w załącznikach bez ścieżek plików programu.
- Ogłoszenie o wykonaniu umowy (art. 448): po odbiorze częściowym program proponował datę wykonania umowy i termin publikacji – teraz dopiero po
  odbiorze wszystkich etapów, wcześniej komunikat „odebrano 1 z 3 etapów”.
- Podwykonawcy: ostrzeżenia – termin zapłaty ponad 30 dni (art. 463, sprzeciw z art. 464 ust. 3), umowa niezgłoszona (art. 464, kopia w 7 dni),
  zaległości (bezpośrednia zapłata, art. 465); zgłoszenie nie zawiera już oświadczenia „do 30 dni”, gdy umowa przewiduje dłuższy termin.

### Wspólnoty, dotacje, odwołania
- Wspólnota: NIP, adres i kontakt z „Danych zamawiającego” trafiają do zapytania i umowy, gdy profil to ta sama wspólnota (było [UZUPEŁNIJ]);
  dopasowanie nazwy zaostrzone – „WM Słoneczna 12” nie pasuje już do „WM Polna 3” (wcześniej wystarczał wspólny początek nazwy).
- Dotacje: próg zasady konkurencyjności 80 000 zł netto (wytyczne od 25.03.2025; było 50 000 zł) i warunek „przekracza” (było „od”);
  dla zapytań opublikowanych przed 25.03.2025 – 50 000 zł. Termin 30 dni – progi z wytycznych (roboty: 5 404 000 euro od 1.01.2026; było 5 382 000).
- Trwałość projektu: błąd programu dla daty 29.02; opis – liczona od płatności końcowej (art. 65 rozp. 2021/1060).
- Odwołania: koniec terminu w dzień ustawowo wolny (np. 11.11, Wielkanoc, Wigilia od 2025) przesuwa się na następny dzień roboczy (art. 509 ust. 2 Pzp).

### Jak sprawdzono
- Prawdziwe AI: oferta usługodawcy (analiza 0,29 USD, formularze 0,05 USD), komplet dokumentów wspólnoty (5 dokumentów, 8 min, 1,46 USD – bez
  instytucji Pzp, poprawne kary, gwarancja, kaucja, termin ofert).
- Testy krytyczne (każdy nie przechodzi na poprzedniej wersji): dostawca_krytyczny_test (11), realizacja_krytyczny_test (12),
  pozostale_moduly_test (10); poprzednie testy bez błędów; regresja adresów obu edycji i wszystkich ekranów (1300 / 390 px) bez błędów.

---

## Wersja „2027-02-11 wykonawca-oferta”

Poprzednia wersja: „2027-02-10 punktacja-dokumenty”.

### Moduł wykonawcy – poprawki po teście „firma budowlana” (prawdziwe AI, przetarg na termomodernizację szkoły)
Błędy krytyczne:
- Kosztorys „dla zamawiającego” zawierał dział „Pozycje uzupełniające (poza przedmiarem)” (rezerwa na gwarancję, koszt zabezpieczenia, OC, zaplecze),
  pozycje z ilością 0 i arkusz z notatkami roboczymi (ryzyka, „do weryfikacji”). Teraz koszty spoza przedmiaru są rozłożone proporcjonalnie na ceny
  pozycji przedmiaru (suma = cena oferty co do grosza), bez pozycji z ilością 0 i bez notatek; doszedł arkusz „Tabela elementów scalonych”.
  Kosztorys wewnętrzny bez zmian – z informacją o rozłożeniu (np. „+12,9%”).
- Przy robotach formularz ofertowy był z ogólnego szablonu („zapytanie ofertowe”), bez pól wzoru zamawiającego; oświadczenia z art. 125
  program nie przygotowywał. Teraz po „Przygotuj ofertę” AI wypełnia formularz ofertowy i oświadczenia według WZORÓW z SWZ (jak przy dostawach),
  danymi firmy, ceną i gwarancją; podstawowy formularz z programu zostaje tylko w razie błędu AI i używa nazw z SWZ.
- „Oferta gotowa – komplet do złożenia” przy komplecie bez dowodu wadium i oświadczeń. Teraz program porównuje komplet z dokumentami wymaganymi
  z ofertą (formularz, kosztorys/formularz cenowy, art. 125/JEDZ, wadium, przedmiotowe środki dowodowe; pozycje warunkowe i „na wezwanie” pomija):
  „Uzupełnij komplet – brakuje: …”, a po skompletowaniu – „podpisz dokumenty i złóż ofertę przed terminem”.
Ważne:
- Kwoty w podsumowaniu i uwagach były sprzed aktualizacji cen z internetu (np. „ok. 1,78 mln” przy cenie 1,83 mln, „okna 1 180 zł/m²” przy 1 300).
  Teraz po aktualizacji cen kwoty w tekstach są przeliczane (lżejszy model, zmienia tylko kwoty); gdy się nie uda – wyraźna informacja.
- Numeracja pozycji jak w przedmiarze (1.1, 2.3…), nie 1–46.
- VAT: program kazał „ustalić stawkę z zamawiającym” – stawkę ustala wykonawca. Bez wskazania w dokumentach: roboty 23%, 8% tylko przy
  budownictwie objętym społecznym programem mieszkaniowym (wtedy uwaga do sprawdzenia).
- Gwarancja w ofercie: pole wyboru (miesiące) w kroku oferty z kryteriami z SWZ – wcześniej wpisywana automatycznie z propozycji AI.
- „Pełna analiza przetargu” korzysta z dokumentów wgranych do projektu oferty (wcześniej błąd pobierania z platformy).
- Okienko zadania w tle nie zasłania już przycisków: przewijana treść dostaje miejsce na dole, „Pomoc” na telefonie przesuwa się nad okienko;
  automatyczne „Sprawdzanie nowych przetargów” bez okienka (widać je na liście przetargów).
- Nagłówek projektu: pełna nazwa w osobnym wierszu, przyciski zawijają się. „Przetarg wygrany – do realizacji” dopiero po złożeniu oferty albo po terminie.
- Telefon: zrobione kroki oferty zwinięte (dotknij nagłówka) – strona projektu ok. 2 500 px zamiast ok. 28 000.
- Po wpisaniu wyniku „wygrana” program proponuje przeniesienie do realizacji.
- Dane firmy (e-mail, telefon, KRS, reprezentacja) trafiają do AI przy kosztorysie – nie są już wpisywane do „do uzupełnienia”.
- Techniczne: model, który nie przyjmuje trybu danych (tool_choice), jest zapamiętany w pliku danych – bez nieudanego zapytania po każdym uruchomieniu.
### Moduł zamawiającego – spójność dokumentów kompletu
- Analiza wykonawcy znalazła sprzeczności w dokumentach z kreatora (pisanych osobno): różna numeracja załączników w SWZ i w pliku oświadczeń,
  wymóg formularza cenowego, którego kreator nie tworzy, inna reguła przy braku gwarancji w formularzu i w SWZ, różna kolejność pierwszeństwa dokumentów.
  Teraz SWZ, OPZ, umowa i formularz dostają te same „ustalenia wspólne” (numeracja załączników nr 1–10, kolejność pierwszeństwa, przy ryczałcie
  bez formularza cenowego z ofertą, brak gwarancji = okres minimalny i 0 pkt), a plik oświadczeń jest numerowany od zał. nr 4 „do SWZ”.
### Testy
- Nowy wykonawca_krytyczny_test (36 sprawdzeń, plik testowy: przedmiar + dokumenty przetargu + kosztorys z prawdziwego AI); na poprzedniej wersji
  wykrywa błędy w każdym punkcie.
- Test z prawdziwym AI: kosztorys z numeracją przedmiaru, kwoty w uwagach przeliczone (5 z 5), formularz ofertowy i oświadczenie art. 125 według wzorów
  z SWZ z danymi firmy i gwarancją 84 mies., komplet: „brakuje: dowód wniesienia wadium”.
- Regresja: ocena_wybor_test i kryteria_dokumenty_test 0 błędów; adresy GET w obu edycjach bez błędów serwera; 48 widoków (1300 i 390 px) bez błędów JS.
### Pliki do podmiany
app.js, styl.css, modul_oferty.py, serwer.py, zamawiajacy.py, ZMIANY.md (oraz pliki z wersji 09.02 i 10.02, jeśli nie zostały wgrane).


---

## Wersja „2027-02-10 punktacja-dokumenty”

Poprzednia wersja: „2027-02-09 wybor-oferty”.

### Moduł zamawiającego – poprawki po teście z prawdziwym AI (SWZ, OPZ, umowa, formularz)
Błąd krytyczny:
- SWZ pisana przez AI punktowała gwarancję w zakresie (60 mies. = 0 pkt, 84 i więcej = 40 pkt), a program w ocenie ofert liczył
  „gwarancja ÷ najdłuższa gwarancja wśród ofert × 40”. Ranking i protokół mogły wskazać innego wykonawcę niż wynika z SWZ
  (przykład: 1 000 000 zł / 60 mies. i 1 150 000 zł / 72 mies. – program wybierał pierwszą, według SWZ wygrywa druga). Teraz:
  - kreator zapisuje zakres punktowania z kryterium („od 60 do 84 miesięcy”), a ocena ofert liczy tym samym wzorem; ponad 84 – jak 84;
  - AI dostaje gotowe wzory punktacji i ma je przepisać do SWZ dosłownie; ten sam opis trafia do protokołu („Sposób oceny”);
  - w ocenie ofert kolumna „Punktowana od–do” – komisja może poprawić zakres, a opis wzoru przelicza się sam;
  - ocena ofert utworzona wcześniej z kreatora dostaje zakres po ponownym przejściu z kreatora; zakres odczytywany jest też z wgranej SWZ;
  - kryteria wpisane bez myślnika („cena 60%, gwarancja 40%”) są teraz rozpoznawane.
Ważne:
- Komplet dokumentów pisał się po kolei – ok. 30 minut. Teraz SWZ, opis przedmiotu, umowa i formularz piszą się jednocześnie: ok. 15 minut
  przy obecnym limicie 2 zapytań AI naraz (ochrona pamięci serwera); na serwerze z większą pamięcią zmienna BIDIVIA_AI_NARAZ=4 skraca to do czasu
  najdłuższego dokumentu. Błąd jednego dokumentu nie przerywa już pozostałych (wcześniej przerywał całe zadanie).
- Ok. 310 miejsc „[UZUPEŁNIJ]” w czterech dokumentach – w teście po zmianie 29 (same dane, których nie da się znać przed publikacją:
  numer ogłoszenia, ID postępowania, kwota na sfinansowanie itp.):
  - dokumenty dostają z „Danych zamawiającego” NIP, REGON, adres, e-mail, telefon, stronę/BIP, rachunek do wadium i godziny pracy (nowe pola
    „Rachunek bankowy (wadium)” i „Godziny pracy”) – tylko gdy to dane tego zamawiającego (edycja urzędu albo zgodna nazwa);
  - kreator: godzina terminu składania ofert; otwarcie ofert ustawiane 30 minut później tego samego dnia;
  - prośby AI „[UZUPEŁNIJ: potwierdzić…]” zamiast w treści trafiają na listę „Do Twojej decyzji przed publikacją” (krok „Komplet dokumentów”)
    i do pliku 2_do_akt_postepowania/Do_decyzji_przed_publikacja.txt w ZIP.
- Błędne limity w SWZ: AI podawało „termin związania ofertą maksymalnie 90 dni” i „przedłużenie do 60 dni”. W trybie podstawowym to 30 dni
  i przedłużenie jednokrotnie o 30 dni (art. 307 ust. 1 i 2 Pzp). Polecenie dla AI zawiera teraz parametry ustawowe trybu: art. 307, 283, 284, 221–222.
- Zmiana punktacji gwarancji zmienia wynik w otwartych ocenach z kryterium gwarancji z zakresem – w teście ECO-Dach 80,00 pkt zamiast 94,29.
### Testy
- Nowy kryteria_dokumenty_test (24 sprawdzenia); na poprzedniej wersji wykrywa 21 błędów. ocena_wybor_test – zaktualizowane punkty, 0 błędów.
- Test z prawdziwym AI: komplet w 15,7 min (wcześniej ok. 30), 29 pól „[UZUPEŁNIJ]” (wcześniej ok. 310), 46 spraw „do decyzji”, wzór gwarancji
  w SWZ zgodny z programem, termin związania ofertą 30 dni, przedłużenie 30 dni.
- Regresja: wszystkie adresy GET w obu edycjach bez błędów serwera; 48 widoków (1300 i 390 px) bez błędów JS.
### Pliki do podmiany
app.js, kreator_zam.py, zamawiajacy.py, ocena_ofert.py, trasy_kreator.py, trasy_ocena.py, trasy_firma.py, modul_oferty.py, serwer.py, ZMIANY.md.


---

## Wersja „2027-02-09 wybor-oferty”

Poprzednia wersja: „2027-02-08 test-gminy”.

### Moduł zamawiającego – sprawdzenie ofert (test „pracownik gminy”)
Błąd krytyczny:
- „Informacja o wyborze najkorzystniejszej oferty” wskazywała ofertę z 2. miejsca z uzasadnieniem „najwyższa liczba punktów”, gdy oferta z 1. miejsca
  czekała na wyjaśnienie ceny (art. 224). Tabela w tym samym piśmie pokazywała inną ofertę na 1. miejscu. Takie pismo trafia do wszystkich wykonawców (art. 253).
  Teraz:
  - dopóki oferta najwyżej oceniona ma nierozstrzygnięte kwestie (rażąco niska cena, status inny niż „prawidłowa”), informacji o wyborze nie można przygotować –
    przycisk jest nieaktywny, a program mówi, którą ofertę i jak rozstrzygnąć (przyjąć wyjaśnienia albo odrzucić);
  - to samo w zamówieniu podzielonym na części – osobno dla każdej części;
  - w rankingu oferta z 2. miejsca ma znacznik „bez zastrzeżeń” zamiast pucharu, na liście postępowań „wybór wstrzymany” zamiast „wybrana: …”;
  - protokół w takiej sytuacji zapisuje „Wybór najkorzystniejszej oferty wstrzymany do czasu rozstrzygnięcia” i wskazuje ofertę bez zastrzeżeń jako rezerwową.
- Przycisk „Wyjaśnione / uzupełnione – oferta prawidłowa” nie zdejmował znacznika rażąco niskiej ceny (serwer pomijał tę informację) – oferta po przyjęciu
  wyjaśnień ceny nigdy nie mogła zostać wybrana. Teraz po przyjęciu wyjaśnień oferta wraca do wyboru, a protokół odnotowuje przyjęcie wyjaśnień.
Ważne:
- Protokół: w kolumnie „Sposób oceny” zamiast tekstu roboczego „z warunków kreatora – sprawdź z SWZ” – wzór, którym program liczy punkty
  (np. „(najniższa cena spośród ofert nieodrzuconych / cena badanej oferty) × 60”). Ten sam opis przy kryteriach przejętych z kreatora.
- Protokół: przy rażąco niskiej cenie konkretne uzasadnienie przy danej ofercie – kwota i różnica w %, np. „Cena 829 000,00 zł jest niższa o 42,0% od wartości
  zamówienia z VAT (1 428 756,38 zł) – obowiązkowe wezwanie do wyjaśnień (art. 224 ust. 2 pkt 1 Pzp)”.
- Punkty po polsku („94,29”, waga „60”) – w protokole, informacji o wyborze, rankingu w programie i komunikacie po ocenie (wcześniej „94.29”, „60.0”).
### Testy
- Nowy ocena_wybor_test (21 sprawdzeń); na poprzedniej wersji wykrywa 16 błędów.
- Regresja: wszystkie adresy GET w obu edycjach bez błędów serwera; 48 widoków w przeglądarce (1300 i 390 px) bez błędów JS i bez poziomego przewijania.
### Pliki do podmiany
app.js, ocena_ofert.py, trasy_ocena.py, trasy_kreator.py, serwer.py, ZMIANY.md.


---

## Wersja „2027-02-08 test-gminy”

Poprzednia wersja: „2027-02-07 po-publikacji”.

### Moduł zamawiającego – poprawki po teście „pracownik gminy”
Błędy krytyczne:
- Krok 5 „Komplet dokumentów” i pozycja „Finansowanie” w kroku 7 zaliczały się po przygotowaniu samych oświadczeń, bez SWZ i umowy.
  Teraz krok 5 wymaga dokumentów głównych (SWZ albo zaproszenia oraz wzoru umowy). Finansowanie zalicza się tylko po przygotowaniu tych dokumentów.
  Krok 7 pokazuje „Komplet nie jest gotowy do publikacji” z listą braków: dokumenty, sprawdzenie w kroku 6, wartość bez szacowania.
  Przed pobraniem niegotowego kompletu program pyta o potwierdzenie.
- ZIP „do publikacji” zawierał dokumenty wewnętrzne. Teraz ma dwa foldery:
  - „1_do_publikacji”: SWZ, opis przedmiotu, umowa, formularze, oświadczenia dla wykonawców, klauzula RODO, uzasadnienie braku podziału, wyjaśnienia SWZ;
  - „2_do_akt_postepowania”: notatka z szacowania, kosztorys inwestorski, oświadczenia z art. 56, pozycja planu, dane do formularza ogłoszenia,
    informacja o kwocie (publikowana osobno przed otwarciem ofert, art. 222 ust. 4).
  Do tego plik CZYTAJ.txt z opisem, co publikować, a czego nie.
Ważne:
- Krok „Wartość i tryb” u zamawiającego publicznego ma ✓ dopiero po szacowaniu (art. 28–36 Pzp), nie po wpisaniu budżetu orientacyjnego.
- Plan postępowań: pytanie o rok planowanego wszczęcia (a nie o rok bieżący). W piśmie termin wszczęcia z kreatora, np. „styczeń 2027 (I kwartał 2027)”.
- Notatka z szacowania: liczby po polsku („4,31 zł”, „501 392,11 €”, „23 291 240 zł”). Opis trybu nie traci już przecinków
  (wspólna funkcja w progi.py; ta sama poprawka w tekstach o rażąco niskiej cenie i podziale na części).
- Ocena ofert z kreatora:
  - dostaje tylko dokumenty zamówienia, bez pism wewnętrznych;
  - kryteria są przejęte z warunków kreatora;
  - przejęte są też znak sprawy, zamawiający, tryb, kwota na sfinansowanie i wartość zamówienia z VAT (art. 224);
  - przy ofercie można wpisać siedzibę wykonawcy (informacja z otwarcia ofert).
- Dane do ogłoszenia: zamiast „[UZUPEŁNIJ]” przy podziale na części – powody braku podziału z listy kontrolnej. Termin składania ofert w formacie
  „05.02.2027, godz. [UZUPEŁNIJ]”.
- Kalendarz postępowania ostrzega, gdy od publikacji do terminu ofert jest mniej dni niż minimum dla trybu (np. 14 dni dla robót, art. 283 Pzp).
Mniejsze:
- Edycja urzędu:
  - „Dane zamawiającego” zamiast „Profil firmy”;
  - wyszukiwarka „Szukaj zamówień…”;
  - „Przygotuj zamówienie” otwiera kreator;
  - nazwa trybu „Tryb podstawowy (procedura krajowa)” zamiast „SWZ – tryb podstawowy”.
- „Szczegóły”: zakres i termin podpowiadane z opisu z pierwszego kroku. Z kosztorysu inwestorskiego odczytywany jest też autor („Sporządził”).
- Domyślne warunki:
  - doświadczenie liczone jako 50% wartości brutto (wcześniej od kwoty netto, opisanej jako brutto);
  - kryterium gwarancji z górną granicą punktowania (roboty 60–84 mies., dostawy 24–48 mies.).
- Finansowanie: bez wgranej umowy nie ma przycisku „Odczytaj umowę (AI)”.
- Kalendarz na telefonie: wiersze jako karty, bez ucinania kolumn.
- Bez zmian: ręczna punktacja ofert (pominięta – ocena ofert korzysta z AI).
### Testy
- Nowe urzad_krytyczny_test (24 sprawdzenia) i urzad_krytyczny_ui (12, edycja urzędu). Na poprzedniej wersji wykrywają błędy. Oba dopisane do regresji.
- Regresja: testy modułów OK, testy interfejsu OK, przegląd widoków OK.
### Pliki do podmiany
app.js, styl.css, kreator_zam.py, trasy_kreator.py, trasy_ocena.py, trasy_zamawiajacy.py, szacowanie.py, progi.py, rynkowosc.py, serwer.py.

---

## Wersja „2027-02-07 po-publikacji”

Poprzednia wersja: „2027-02-06 jedna-lista-kontrolna”.

### Zamawiający po publikacji – brakujące etapy (plan, punkt 4)
- Kreator, krok 7 (zamawiający publiczny), część „Po publikacji”:
  - Kalendarz postępowania z daty publikacji, terminu ofert i daty zawiadomienia o wyborze: ostatni dzień na wniosek o wyjaśnienie SWZ
    i na odpowiedź (art. 284 ust. 2 – 4 / 2 dni; od progów UE art. 135 – 14 / 6 dni), kwota na sfinansowanie przed otwarciem, otwarcie
    najpóźniej następnego dnia (art. 221), informacja z otwarcia (art. 222 ust. 5), najdłuższe związanie ofertą (30 / 90 dni, art. 307 / 220),
    koniec terminu na odwołanie przed zawarciem umowy (5 / 10 dni, art. 308 ust. 2 / 264 ust. 1), ogłoszenie o wyniku (30 dni).
  - Pytania wykonawców: data wpływu, w terminie / po terminie (bez obowiązku odpowiedzi, art. 284 ust. 4), do kiedy odpowiedzieć,
    projekt odpowiedzi AI na podstawie dokumentów postępowania (z oznaczeniem, czy odpowiedź zmienia SWZ i czy przedłużyć termin).
  - Przedłużenie terminu składania ofert: nowy termin w kreatorze, historia zmian, kalendarz przeliczony.
  - Pismo „Wyjaśnienia treści SWZ (i zmiana SWZ)” – bez ujawniania pytającego, zmiany SWZ, przedłużenie terminu (art. 286 ust. 3),
    przypomnienie o ogłoszeniu o zmianie w BZP (art. 286 ust. 9) / Dz.U. UE i komunikacie na stronie postępowania.
- Ocena ofert:
  - Informacja z otwarcia ofert (art. 222 ust. 5): wykonawcy, siedziby, ceny, kwota na sfinansowanie (art. 222 ust. 4).
  - Wezwanie wykonawcy, którego oferta została najwyżej oceniona, do podmiotowych środków dowodowych: art. 274 ust. 1 (co najmniej 5 dni)
    albo od progów UE art. 126 ust. 1 (co najmniej 10 dni); lista środków z SWZ (nowe pole w odczycie SWZ), uwaga o bazach KRS / CEIDG.
- Wspólnota: bez zmian (te etapy dotyczą Pzp).
### Testy
- Nowe postepowanie_test (29 sprawdzeń) i postepowanie_ui; na starym kodzie 6 błędów. Oba w regresji.
- Regresja: testy modułów OK, testy interfejsu OK, przegląd widoków OK.
### Pliki do podmiany
postepowanie_zam.py (nowy), trasy_kreator.py, ocena_ofert.py, trasy_ocena.py, app.js, styl.css, serwer.py (wersja).

---

## Wersja „2027-02-06 jedna-lista-kontrolna”

Poprzednia wersja: „2027-02-05 ponawianie-klucza”.

### Jedna lista kontrolna – kreator, weryfikacja dokumentacji, prawnik (plan, punkt 3)
- Nowy moduł lista_kontroli.py: wymogi trybu (ta sama tabela co krok 7 kreatora) i lista ogólna według reżimu – Pzp, zamówienie publiczne
  poza Pzp (poniżej progu, zasada konkurencyjności) albo zamawiający prywatny (wspólnota, spółdzielnia, deweloper).
- Krok 6 kreatora: sprawdzenie dokumentów według pozycji z kroku 7 tego zamówienia (np. wolna ręka – bez kryteriów, przesłanka art. 305),
  a nie według stałej listy Pzp. Wspólnota: lista zamawiającego prywatnego (uchwała, Kodeks cywilny) – wcześniej polecenie mówiło
  „zgodność z Pzp, art. 436, art. 439”, a dopisek systemowy „Pzp nie ma zastosowania”.
- Weryfikacja dokumentacji (zamawiający publiczny): wybór trybu postępowania (domyślnie tryb z kreatora albo „ustal z dokumentów”),
  lista kontrolna trybu w poleceniu dla AI. Wspólnota – lista bez Pzp.
- Prawnik: listy z lista_kontroli.py; przy zamówieniu poza Pzp lista przedmiotu bez artykułów Pzp (Kodeks cywilny, Prawo budowlane).
- Dokumenty oferty (dostawca): linia podpisu według art. 63 – od progów UE tylko podpis kwalifikowany, poniżej progów także zaufany
  i osobisty, poza Pzp według zapytania.
### Testy
- Nowy lista_jedna_test (17 sprawdzeń) – na starym kodzie 9 błędów; w regresji. Regresja: moduły OK, interfejs OK, przegląd widoków OK.
### Pliki do podmiany
lista_kontroli.py (nowy), prawnik.py, kreator_zam.py, trasy_kreator.py, zamawiajacy.py, trasy_projekty_wykonawcy.py, app.js, serwer.py.

---

## Wersja „2027-02-05 ponawianie-klucza”

Poprzednia wersja: „2027-02-04 finansowanie-prawnik-dostawca”.

### AI – „Klucz API odrzucony” przy dobrym kluczu (zgłoszenie użytkownika)
- Błąd: chwilowy błąd serwera Anthropic 5xx „credential validation failed” był traktowany jak odrzucony klucz – program od razu przechodził
  na drugi klucz (często stary/wyłączony) i zadanie kończyło się błędem „Klucz API odrzucony”.
- Teraz: przy błędzie 5xx „credential” dwa ponowienia tym samym kluczem (po 5 i 20 s), dopiero potem drugi klucz. Błąd 401/403
  (klucz naprawdę odrzucony) – jak dotąd od razu drugi klucz.
### Testy
- Nowy klucz_test (5 scenariuszy) – na starym kodzie 2 błędy; w regresji. Regresja: testy modułów OK, testy interfejsu OK.
### Pliki do podmiany
modul_oferty.py, serwer.py (wersja).

---

## Wersja „2027-02-04 finansowanie-prawnik-dostawca”

Poprzednia wersja: „2027-02-03 wspolnota-lista-kontrolna”.

### Kreator – finansowanie: kredyt, premia BGK, KPO, dotacja (zgłoszenie użytkownika)
- Błąd: w kreatorze nie było miejsca na finansowanie. Sekcja była tylko w realizacji, czyli po zawarciu umowy, a w kroku 7 wspólnoty została sama pozycja „do odhaczenia”.
- Teraz krok „Warunki” ma sekcję „Finansowanie: kredyt, premia BGK, KPO, dotacja”:
  - źródło, umowa lub promesa, odczyt AI i ręczna poprawka terminów;
  - harmonogram pod finansowanie: zakończenie robót najpóźniej 30 dni przed terminem z umowy finansowania, etapy odbiorów pod transze.
- Dokumenty (krok 5): do zapytania lub SWZ, wzoru umowy, opisu przedmiotu i formularza trafiają wymagania instytucji:
  - termin;
  - harmonogram rzeczowo-finansowy z etapami pod transze i płatności po odbiorach;
  - obowiązki wobec instytucji, dokumenty do rozliczenia, zgoda instytucji na zmiany umowy;
  - koszty kwalifikowalne.
- Sprawdzenie (krok 6) obejmuje zgodność dokumentów z umową finansowania.
- Krok 7:
  - pozycja „Finansowanie” zalicza się sama, gdy dokumenty przygotowano po ostatniej zmianie finansowania. Po zmianie wraca do zrobienia z podpowiedzią;
  - u zamawiającego publicznego pozycja pojawia się, gdy zamówienie ma finansowanie.
- Te same dane służą po zawarciu umowy w realizacji (kontrole harmonogramu, przepływy, porównanie z umową), bez ponownego wprowadzania.
### Dla prawnika
- Lista kontrolna zależy od trybu i pochodzi z tej samej tabeli co lista kroku 7 kreatora, plus szczegóły trybu:
  - warianty trybu podstawowego;
  - JEDZ i Dziennik Urzędowy UE;
  - przesłanki wolnej ręki (art. 305 / 214) i negocjacji bez ogłoszenia (art. 301 / 209);
  - in-house (art. 216).
- Do listy ogólnej dopisano: plan postępowań (art. 23), art. 443, art. 222 ust. 4, art. 56 oraz miejsce ogłoszenia (BZP albo Dziennik Urzędowy UE).
- Poniżej progu i zasada konkurencyjności: osobna lista poza Pzp (regulamin, Kodeks cywilny, Baza Konkurencyjności), bez wymogów Pzp.
  Termin odwołania: „odwołanie do KIO nie przysługuje”. Projekt odwołania ma w tych trybach ostrzeżenie.
### Dostawca – krok 5 „Złożenie oferty”
- Podpis oferty według art. 63 Pzp, ustalany z analizy (miejsce ogłoszenia i tryb):
  - od progów unijnych tylko podpis kwalifikowany;
  - poniżej progów podpis kwalifikowany, zaufany albo osobisty;
  - poza Pzp według zapytania.
  Wcześniej tekst sugerował, że podpis zaufany zależy od SWZ.
- Lista kontrolna ma dwie części: „składane z ofertą” i „na wezwanie zamawiającego” (podmiotowe środki dowodowe, art. 126 / art. 274).
- Zaznaczenia są zapisywane na serwerze, więc są takie same na telefonie, na komputerze i u każdego użytkownika projektu. Wcześniej trzymała je przeglądarka.
  Dotychczasowe zaznaczenia przenoszą się same.
- AI przygotowujące załączniki rozróżnia:
  - przedmiotowe środki dowodowe składane z ofertą (art. 106–107);
  - podmiotowe środki dowodowe składane na wezwanie (art. 126 – unijne, art. 274 – krajowe).
### Testy
- Nowe testy fin_kreator_test i fin_kreator_ui; na starym kodzie test wykrywa 12 błędów. Oba dopisane do regresji.
- Regresja: testy modułów OK, testy interfejsu OK, przegląd widoków OK.
### Pliki do podmiany
app.js, finansowanie.py, trasy_finansowanie.py, trasy_kreator.py, zamawiajacy.py, prawnik.py, trasy_projekty_wykonawcy.py, serwer.py.

---

## Wersja „2027-02-03 wspolnota-lista-kontrolna”

Poprzednia wersja: „2027-02-02 lista-kontrolna-tryby”.

### Kreator – krok 7 dla wspólnot, spółdzielni i deweloperów
- Lista przed wysłaniem zapytania: 9 pozycji (deweloper 8 – bez uchwały). Przy zasadzie konkurencyjności +3 pozycje, tak jak u zamawiającego
  publicznego: Baza Konkurencyjności, minimalny termin 7/14/30 dni, brak powiązań osobowych i kapitałowych (wcześniej jedna ogólna pozycja,
  bez powiązań). Przy przetargu według regulaminu spółdzielni +1 pozycja.
- Protokół wyboru wykonawcy przeniesiony z listy do części „Po zebraniu ofert” (sporządza się go po ofertach).
- Tryb „Przetarg według regulaminu spółdzielni” jest dostępny tylko dla spółdzielni. Wspólnota z zapisanym tym trybem wraca do zapytania ofertowego.
- Zapytanie do wybranych wykonawców: przypomnienie o zaproszeniu co najmniej 3 wykonawców. RODO: „zamawiający jako administrator danych”
  (wcześniej „wspólnota / spółdzielnia” także u dewelopera). Finansowanie: pozycja warunkowa („jeśli prace są kredytowane lub dofinansowane”).
- Nowy rodzaj pozycji „do odhaczenia” (uchwała, rozesłanie, finansowanie, Baza Konkurencyjności, termin): „Oznacz jako zrobione” zamiast
  „Sprawdź w kroku Sprawdzenie i zmiany”. Tak samo u zamawiającego publicznego: Baza Konkurencyjności, minimalny termin i pozycja
  „bez ogłoszenia o zamówieniu” (negocjacje bez ogłoszenia, wolna ręka).
- Teksty kroku 7 dla wspólnoty: „Gotowe do wysłania”, „Komplet do wysłania wykonawcom…”, „Lista kontrolna przed wysłaniem zapytania”,
  bez przycisku „Platforma e-Zamówienia” i bez „kosztorysu inwestorskiego”. U gminy bez zmian.
### Testy
- Nowy wspolnota_lista_ui (4 rodzaje zamawiających × 4 tryby, wygląd kroku 7, odhaczanie). Na starym kodzie wykrywa błędy. Dopisany do regresja_ui.sh.
- moduly_test i moduly_ui dostosowane do zasady „regulamin tylko dla spółdzielni”.
- Regresja: testy modułów OK, testy interfejsu OK, przegląd 144 widoków OK.
### Pliki do podmiany
wspolnota.py, reguly_zamowien.py, trasy_kreator.py, kreator_zam.py, app.js, serwer.py (wersja).

---

## Wersja „2027-02-02 lista-kontrolna-tryby”

Poprzednia wersja: „2027-02-01 archiwum-ceny-wszystkie”.

### Lista kontrolna „Gotowe do publikacji” według trybu (zgłoszenie użytkownika)
- Błąd: pełną listę Pzp (14 pozycji) dostawały tylko tryb podstawowy i przetarg nieograniczony. Pozostałe tryby Pzp (przetarg ograniczony,
  negocjacje z ogłoszeniem i bez ogłoszenia, dialog, partnerstwo, wolna ręka) oraz zasada konkurencyjności dostawały listę dla zamówień poza Pzp
  (8 pozycji z „regulaminem” i „upublicznieniem”). Brakowało im planu postępowań, art. 439, art. 443 i art. 56.
- Teraz lista zależy od grupy trybu (opis: Bidivia_lista_kontrolna_wg_trybu.docx; pozycje „do potwierdzenia” przyjęte jako obowiązkowe):
  tryb podstawowy 14, tryby unijne 14–15, partnerstwo 15, negocjacje bez ogłoszenia 15, wolna ręka 12, poniżej progu 8, zasada konkurencyjności 9.
- Ogłoszenie: tryb podstawowy – BZP; przetarg nieograniczony, ograniczony, negocjacje z ogłoszeniem, dialog – Dziennik Urzędowy UE (wcześniej
  „BZP i Dz.U. UE”); partnerstwo – według wartości. Negocjacje bez ogłoszenia i wolna ręka – pozycja „bez ogłoszenia o zamówieniu” (ogłoszenie
  o zamiarze, in-house, ogłoszenie o wyniku) i uzasadnienie wyboru trybu. Pismo „Dane do ogłoszenia” ma nagłówek BZP albo Dziennik Urzędowy UE.
- Wolna ręka: bez kryteriów oceny, podziału na części i kwoty z art. 222 ust. 4; warunki udziału opcjonalne; podmiotowe środki dowodowe
  obowiązkowe, oświadczenie z art. 125 opcjonalne (art. 217).
- Zasada konkurencyjności: Baza Konkurencyjności, minimalne terminy, brak powiązań osobowych i kapitałowych zamiast regulaminu.
- Jedna definicja pozycji: lista_kontrolna() korzysta z elementy(). Moduł wspólnoty bez zmian.
### Testy
- Nowy lista_trybow_test (wszystkie 12 trybów, ogłoszenia, pismo, API kreatora) – na starym kodzie 16 błędów; w regresji.
- Regresja: testy modułów OK, testy interfejsu OK, przegląd 144 widoków OK.
### Pliki do podmiany
kreator_zam.py, reguly_zamowien.py, serwer.py (wersja).

---

## Wersja „2027-02-01 archiwum-ceny-wszystkie”

Poprzednia wersja: „2027-01-31 urzad-otwarcie-projektu”.

### Archiwum: usuwanie wszystkiego naraz (app.js)
- „Opróżnij archiwum – usuń trwale wszystko (N)” oraz „Usuń wszystkie (N)” w każdej sekcji; tylko administrator, potwierdzenie (dwukrotne przy całym archiwum).
### „Sprawdź, czy ceny są rynkowe” – wszystkie pozycje (serwer.py)
- Błąd: sprawdzanych było tylko 15 najdroższych pozycji formularza cenowego, a w wyniku mogły się znaleźć numery pozycji spoza zapytania.
- Teraz sprawdzane są wszystkie pozycje z ceną, po 15 w jednym zapytaniu z wyszukiwaniem; błąd jednej części nie przerywa pozostałych.
### Testy
- archiwum_ui, ceny17_test (na starym kodzie 4 błędy); regresja modułów i interfejsu OK.
### Pliki do podmiany
app.js (wysłany wcześniej), serwer.py.

---

## Wersja „2027-01-31 urzad-otwarcie-projektu”

Poprzednia wersja: „2027-01-30 krok6-jedno-sprawdzenie”.

### Edycja urzędu: projekt zamówienia nie otwierał się (zgłoszenie użytkownika)
- Objaw: po kliknięciu projektu na liście „Projekty zamówień” pojawiał się komunikat „Ta funkcja nie jest dostępna w edycji „Bidivia – Zamawiający””
  i projekt się nie otwierał.
- Przyczyna: przy otwieraniu każdego projektu `otworzProjekt()` pobierał razem z projektem listę hurtowni (`/api/hurtownie`) i pracowników
  (`/api/pracownicy`). To dane wykonawcy, potrzebne tylko w harmonogramie i zamówieniach materiałów. W edycji urzędu te trasy są zablokowane.
  Odrzucone jedno zapytanie przerywało wszystkie (`Promise.all`), więc projekt się nie otwierał. Błąd istniał przed wersją 2027-01-30.
- Poprawka: w edycji urzędu hurtowni i pracowników się nie pobiera. W pełnej edycji błąd tych zapytań (także listy użytkowników) daje pustą
  listę zamiast blokować otwarcie projektu.
### Testy
- Nowy `urzad_projekt_ui.py`: serwer w edycji urzędu, otwarcie projektu, wszystkie kroki kreatora i wszystkie widoki edycji bez zapytań
  do tras zablokowanych w tej edycji. Na starym kodzie 3 błędy (projekt się nie otwiera, `/api/hurtownie`, `/api/pracownicy`). Dopisany do `regresja_ui.sh`.
- Regresja: testy modułów OK, testy interfejsu OK (z nowym), przegląd 144 widoków OK, edycja2_test 0 błędów.
### Pliki do podmiany
app.js, serwer.py (wersja), ZMIANY.md. Pakiet urzędu zbuduj na nowo: `python3 pakiet_urzedu/buduj_pakiet.py <katalog>`.

---

## Wersja „2027-01-30 krok6-jedno-sprawdzenie”

Poprzednia wersja: „2027-01-29 platformy-profil”.

### Kreator zamówienia – krok 6 „Sprawdzenie i zmiany”: jedno sprawdzenie (zgłoszenie użytkownika)
- Błąd: pod krokiem 6 była druga sekcja „Sprawdzenie dokumentacji przetargowej” z osobnym przyciskiem AI. Sprawdzała ona tylko pliki
  wgrane jako materiały źródłowe (folder „dokumenty”), a nie dokumenty przygotowane w kreatorze. Jej poprawki trafiały do „dokumentów poprawionych”,
  których nie ma w komplecie do publikacji (ZIP). Skutki: dwa płatne sprawdzenia, dwie listy uwag i poprawki, które nie trafiały do publikacji.
- Krok 6 ma jedno sprawdzenie dokumentów przygotowanych wcześniej (komplet z kroku 5 albo Twoje wzory): każdy dokument osobno, a do tego
  jedno zapytanie AI o **sprzeczności między dokumentami** (terminy, wadium, gwarancja, kary, kryteria, zakres, odesłania). Sprzeczności trafiają
  na tę samą listę, z oznaczeniem „sprzeczność między dokumentami”, przypisane do dokumentu do poprawienia. Propozycje dla nieznanego dokumentu
  i duplikaty są pomijane.
- Lista do rozstrzygnięcia: licznik „Rozstrzygnięto x / n”. Przycisk „Zatwierdź i przejdź do kroku „Gotowe do publikacji”” jest aktywny dopiero po
  decyzji przy każdej pozycji. Wprowadza zaakceptowane zmiany (Word ze śledzeniem zmian i czysty) albo kopiuje dokumenty bez zmian i przechodzi
  do ostatniego kroku. Gdy błędów nie znaleziono, wystarczy przejść dalej. Zmiany do ręcznego wprowadzenia są też sygnalizowane w kroku 7.
- Krok 6 ma ✓ dopiero po zatwierdzeniu ostatniego sprawdzenia (`przeglad_nr` / `zatwierdzony_nr`). Ponowne sprawdzenie otwiera krok od nowa.
- Ponowne zatwierdzenie usuwa z dokumentów końcowych wersje z poprzedniego zatwierdzenia. Wcześniej w ZIP-ie mogły być naraz „X.docx” i „X_czysty.docx”.
- Sekcja „Sprawdzenie dokumentacji” zostaje bez zmian u wykonawcy, prawnika i w projektach z cudzą dokumentacją.
### Testy
- Nowe: `krok6_test.py` (backend; na starym kodzie 5 błędów, potem przerwanie) i `krok6_ui.py` (gmina i wspólnota w przeglądarce; jedno sprawdzenie,
  blokada przejścia bez rozstrzygnięcia, przejście do kroku 7, ponowne sprawdzenie). Oba dopisane do `regresja.sh` / `regresja_ui.sh`.
- Regresja: testy modułów OK, ro_test 0, smoke 107 tras bez 500, testy interfejsu OK, przegląd 144 widoków OK.
- Narzędzia: skrypty testów interfejsu nie wskazują już na stałe ścieżki przeglądarki (używają przeglądarki Playwright z systemu).
### Pliki do podmiany
app.js, trasy_kreator.py, kreator_zam.py, serwer.py (wersja), ZMIANY.md, instrukcja.html, instrukcja.pdf
(oraz bzp.py z wersji 2027-01-29, jeśli produkcja ma jeszcze 2027-01-28).

---

## Wersja „2027-01-29 platformy-profil”

Poprzednia wersja: „2027-01-28 platformy-ciasteczka”.

Pobieranie dokumentów z profilu zamawiającego na platformie zakupowej (zgłoszenie: link z ogłoszenia prowadził do platformazakupowa.pl/pn/niebylec/…).

- Przyczyna: link z ogłoszenia wskazywał listę postępowań zamawiającego (profil nabywcy), nie stronę postępowania. Program szukał właściwego
  postępowania po tekście linku, a na liście każdy link ma tekst „Przejdź” – tytuł stoi w tym samym wierszu tabeli; nic nie pasowało.
  Goły adres profilu (/pn/<zamawiający>) w ogóle nie zawiera listy (jest pod /pn/<zamawiający>/proceedings).
- Poprawka (bzp.py): kandydaci na stronę postępowania porównywani z przedmiotem po tekście całego wiersza tabeli (albo tekście przed linkiem);
  dla gołego profilu platformazakupowa.pl sprawdzana też lista /proceedings.
- Filtr plików serwisu sprawdza tekst linku i nazwę pliku w adresie; dodana „instrukcja pakowania” – instrukcja platformy o dzieleniu plików
  nie trafia już do dokumentów przetargu.
- Sprawdzone na profilu Gminy Niebylec: Baryczka z gołego adresu profilu – 15 plików (SWZ, umowa, SSTWiORB, rysunki, kosztorys…); dostawa materiału
  do posypywania – 1 plik (jedyny opublikowany); przetarg spoza listy – nic (bez plików cudzego postępowania).
- platforma_test rozszerzony (profil z linkami „Przejdź”, instrukcja rozpoznawana po adresie, przetarg spoza listy); na kodzie sprzed poprawki – 2 błędy.
- Regresja: 23 zestawy testów; testy pobierania (link2, e2e3, bledy, odw_wysz) – wyniki identyczne przed i po.

---

## Wersja „2027-01-28 platformy-ciasteczka”

Poprzednia wersja: „2027-01-27 edycja-urzad”.

Pobieranie dokumentów przetargu z platform zakupowych (zgłoszenie użytkownika: SWZ i przedmiar nie były pobierane z platformazakupowa.pl).

- Przyczyna: platformazakupowa.pl przy pierwszym wejściu robi „ciche” sprawdzenie logowania SSO (przekierowanie → ciasteczko → powrót na
  stronę jako gość). Moduł bzp.py otwierał strony bez ciasteczek, więc przekierowania zapętlały się („HTTP Error 302 … infinite loop”),
  strona postępowania się nie otwierała i program pokazywał komunikat o ręcznym pobraniu. BZP działał poprawnie – ma tylko ogłoszenie.
- Poprawka: wspólny otwieracz z obsługą ciasteczek (anonimowa sesja gościa) dla stron i plików w bzp.py (_otworz, _strona).
- Sprawdzone na zgłoszonym postępowaniu (transakcja 1393578, przebudowa drogi w Baryczce): pobrane 16 plików – SWZ, projekt umowy, SSTWiORB,
  opis techniczny, rysunki, kosztorys ofertowy, formularze i oświadczenia; instrukcja platformy o dzieleniu plików pomijana jako plik serwisu.
- Nowy platforma_test (imitacja platformy z cichym SSO, bez sieci) – na starym kodzie wykrywa błąd; dodany do regresji.
- W projektach, w których pobieranie się nie udało, wystarczy ponownie pobrać dokumenty.
- Regresja: 23 zestawy testów; testy pobierania (link2, e2e3, bledy, odw_wysz) – wyniki identyczne przed i po.

---

## Wersja „2027-01-27 edycja-urzad”

Poprzednia wersja: „2027-01-26 modul-interfejs”.

Edycja urzędu „Bidivia – Zamawiający” jako osobny program do instalacji w urzędzie (pilotaż; ustalenia z 2026-11-03: oba warianty
instalacji, AI przez konto Bidivia, cała ścieżka z realizacją umów).

### Program
- W edycji urzędu (BIDIVIA_EDYCJA=zamawiajacy) rejestrowane są tylko blueprinty ścieżki zamawiającego: kreator, ocena, finansowanie,
  zamawiający publiczny, realizacja, administracja, firma, projekty (pliki, sprawdzenie dokumentacji). Trasy innych modułów nie istnieją (404);
  blokada adresów zostaje jako druga warstwa.
- Luka po rozdzieleniu modułów: trasy wspólnoty (Moje zapytania, nowa inwestycja, zaproszenia) były w edycji urzędu dostępne – teraz nie istnieją.
  Projekty w edycji urzędu zawsze powstają jako projekty gminy (prywatny=false), także przy żądaniu z prywatny=true.
- Błąd sprzed tej wersji: edycja urzędu blokowała każde tworzenie projektu przez /api/projekty, więc „Nowe sprawdzenie ofert” nie działało –
  teraz dozwolone dla typów edycji urzędu, inne typy nadal zablokowane.
- Interfejs: w edycji urzędu tryb gminy wymuszony (także przy zapamiętanym w przeglądarce wyborze wspólnoty), bez przycisku „Dla wspólnot…”,
  bez zbędnego zapytania o nowe przetargi wykonawcy.
### Pakiet instalacyjny (pakiet_urzedu/)
- buduj_pakiet.py → Bidivia-Zamawiajacy-<wersja>.zip: program (app/), Dockerfile (edycja na stałe, użytkownik nie-root, healthcheck),
  docker-compose.yml (dane w ./dane poza kontenerem), .env.przyklad, kopia_zapasowa.sh, windows/ (instaluj.ps1, uruchom.bat – waitress,
  kopia_zapasowa.bat), INSTRUKCJA_INFORMATYKA.md.
- Problem wykryty testem pakietu: ciasteczko sesji z flagą Secure (COOKIE_SECURE=1 domyślnie) uniemożliwiłoby logowanie przez http:// w sieci
  urzędu – pakiet ustawia COOKIE_SECURE=0 z instrukcją przejścia na 1 po włączeniu HTTPS.
### Testy
- edycja2_test (edycja urzędu 6, pełna 1), stary test edycji, trasy API w edycji urzędu (82, bez błędów 500).
- Pakiet uruchomiony z własnego katalogu: gunicorn (jak w obrazie) i waitress (jak w Windows) – logowanie przez HTTP, kreator, lista,
  ocena ofert, moduły spoza edycji 404, gzip; test interfejsu urzędu w przeglądarce (6) – bez błędów JS.
- Nie przetestowane w tym środowisku: budowa obrazu Docker (brak Dockera) i skrypty Windows (brak Windows) – do sprawdzenia przy pierwszej instalacji.
- Regresja edycji pełnej: 22 zestawy testów, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-26 modul-interfejs”

Poprzednia wersja: „2027-01-25 reguly-serwer”.

Punkt 4 audytu, etap 3c – różnice gminy i wspólnoty w interfejsie w jednym miejscu (koniec punktu 4).

- app.js: obiekt opisu modułu MODULY_ZAM (gmina / wspolnota) i funkcja MZ() – odpowiednik reguly_zamowien.py po stronie przeglądarki:
  kafelki, menu (pozycje i nazwy), cele, nagłówki, ochrona ludności, plan na Przeglądzie, ocena według zapytań, nowa inwestycja, nagłówek
  realizacji, rozdział instrukcji, tryby dokumentacji, filtr danych (?modul=), znacznik modułu przy tworzeniu projektów.
- 27 rozproszonych warunków ZAM_PRYW zastąpionych pytaniem MZ(); ZAM_PRYW zostaje tylko jako zapamiętany wybór modułu (definicja i ustawZamPryw).
- Test różnicowy w przeglądarce (stary i nowy app.js, oba moduły): widok po wejściu, kafelki, menu z nazwami, nagłówek, realizacja – identyczne;
  rozdział instrukcji – logika równoważna (sprawdzona w kodzie).
- Regresja: testy interfejsu, 144 widoki.

---

## Wersja „2027-01-25 reguly-serwer”

Poprzednia wersja: „2027-01-24 reguly-zamowien”.

Punkt 4 audytu, etap 3b – reguły gminy i wspólnoty w szkielecie serwera.

- serwer.py korzysta z obiektu reguł (reguly_zamowien.py): generator dokumentów (nazwy dokumentów i plików, kontekst AI), wymóg dokumentu
  podstawy wartości u gminy, przypomnienie przed terminem i zaproszenia (nowa reguła przypomnienia_ofert – tylko wspólnota).
- W serwerze 0 bezpośrednich odwołań do reguł wspólnoty; zostaje jedno źródło odpowiedzi „czy to projekt wspólnoty” (projekt_wspolnoty,
  zgodny_modul) i zapis znacznika modułu przy tworzeniu projektu.
- Regresja: 22 zestawy testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-24 reguly-zamowien”

Poprzednia wersja: „2027-01-23 blueprint-prawnik-wlasciciel”.

Punkt 4 audytu, etap 3a – reguły gminy i wspólnoty w jednym miejscu (Python).

- Nowy moduł reguly_zamowien.py: obiekt reguł zamówienia – Gmina (Pzp, kreator_zam.py) i Wspolnota (bez Pzp, wspolnota.py) z tym samym
  zestawem: tryb, tryby do wyboru, lista kontrolna i elementy, warunki, termin, pomoc, rodzaje zamawiającego, nazwy dokumentów, kontekst AI,
  dokument podstawy wartości, polecenia AI oceny ofert (odczyt SWZ / zapytania, badanie oferty).
- trasy_kreator.py i trasy_ocena.py pytają obiekt reguł zamiast sprawdzać „czy wspólnota” i sięgać po reguły wspólnoty bezpośrednio
  (0 odwołań WSPOL. w obu modułach). W stanie kreatora zostaje jedno rozgałęzienie: wspólnota zastępuje tryb, warunki i termin wyliczone
  ścieżką Pzp. Biblioteka ocena_ofert.py nadal przyjmuje znacznik „prywatny” w danych (protokół i informacja bez Pzp) – to parametr biblioteki.
- Nowy reguly_test (4): polecenia AI odczytu SWZ / zapytania i badania oferty właściwe dla gminy i wspólnoty – dodany do regresji.
- czesci_powiazanie_test: funkcja odczytu SWZ wskazana nazwą zamiast wyszukiwania tekstu w kodzie (zmiana tylko w teście).
- Regresja: 22 zestawy testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-23 blueprint-prawnik-wlasciciel”

Poprzednia wersja: „2027-01-22 blueprint-projekty-wykonawcy”.

Punkt 4 audytu, etapy 2o i 2p – ostatnie blueprinty.

- trasy_prawnik.py (blueprint „prawnik”, 5 tras): sprawy, komplet dokumentów, pisma.
- trasy_leady.py (blueprint „leady”, 3 trasy, moduł właściciela – blokada dla innych kont sprawdzona) i trasy_bk.py (blueprint
  „baza_konkurencyjnosci”, 2 trasy).
- Usunięte nieużywane już w serwerze importy glob i io. Kontrola odwołań S. wykryła, że trasy_bk.py korzystał z nich jako S.glob / S.io –
  moduł importuje je teraz sam; narzędzie wydzielania nie zamienia już nazw modułów biblioteki standardowej na S. i dodaje ich import.
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0; wszystkie odwołania S. istnieją.
- Regresja: 21 zestawów testów, test prawnika, ro_test, 107 tras, 144 widoki, testy interfejsu.
- Koniec etapu 2: 17 blueprintów; w serwerze zostaje szkielet aplikacji (logowanie, strona główna, lista projektów, zadania, wyszukiwarka,
  automaty w tle, migracje).

---

## Wersja „2027-01-22 blueprint-projekty-wykonawcy”

Poprzednia wersja: „2027-01-21 blueprint-admin”.

Punkt 4 audytu, etap 2n – blueprint projektów wykonawcy (oferty).

- Nowy moduł trasy_projekty_wykonawcy.py (blueprint „projekty_wykonawcy”, 40 tras, 945 linii z serwera): pliki projektu, sprawdzenie dokumentacji
  i kontrola (AI), czat z dokumentami, formularz cenowy i pozycje, analiza dostawcy, harmonogram, konsorcjum, zamówienia u hurtowni, zdjęcia.
- Nowy test różnicowy (24 kroki ścieżki wykonawcy): wyniki przed i po etapie identyczne; starsze testy wykonawcy (błędy, linki, rynkowość,
  prawnik) – bez błędów.
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0; wszystkie odwołania S. istnieją.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-21 blueprint-admin”

Poprzednia wersja: „2027-01-20 blueprint-firma”.

Punkt 4 audytu, etap 2m – blueprint administracji i kont.

- Nowy moduł trasy_admin.py (blueprint „administracja”, 19 tras, 428 linii z serwera): użytkownicy i role, konta (praca jako konto, zakres
  administratora), ustawienia konta i programu, archiwum, diagnostyka danych. Logowanie i funkcje before_request zostają w serwerze.
- Macierz dostępu (administrator / użytkownik) dla wszystkich tras GET blueprintu identyczna przed i po etapie; użytkownik nie doda administratora (403).
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw; wszystkie odwołania S. istnieją.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-20 blueprint-firma”

Poprzednia wersja: „2027-01-19 blueprint-realizacja”.

Punkt 4 audytu, etap 2l – blueprint firmy.

- Nowy moduł trasy_firma.py (blueprint „firma”, 33 trasy, 516 linii z serwera): profil firmy, logo i dokumenty, kadry, pracownicy i godziny pracy,
  płace, klienci, własny cennik.
- Narzędzia: funkcje tras ponownie eksportowane tylko wtedy, gdy są wywoływane (serwer, inne blueprinty, testy) – wcześniej ponowny eksport trasy
  „firma” dawał fałszywe „redefinicje” w pyflakes (zmienne lokalne o tej samej nazwie). Kontrola każdego etapu sprawdza teraz, czy wszystkie
  odwołania S.nazwa we wszystkich blueprintach istnieją w serwerze (analiza drzewa składni) – wynik: wszystkie istnieją.
- Moduł nie miał testów – nowy test różnicowy (20 kroków): wyniki przed i po etapie identyczne.
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw i redefinicji.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-19 blueprint-realizacja”

Poprzednia wersja: „2027-01-18 blueprint-przetargi”.

Punkt 4 audytu, etap 2k – blueprint realizacji umów.

- Nowy moduł trasy_realizacja.py (blueprint „realizacja”, 40 tras, 976 linii z serwera): dane i lista realizacji, umowa, pliki, harmonogram
  rzeczowo-finansowy, dziennik, faktury, podwykonawcy, rozliczenie materiałów, pogoda i wnioski o przedłużenie, dostawy, wnioski wykonawcy
  o zmianę umowy (przeniesione z grupy dotacji, etap 2i). Funkcje danych (realizacja_dane) ponownie eksportowane – używane w całym programie.
- Zmienna lokalna „S” w 1 funkcji – nazwa zmieniona automatycznie (S_lok).
- Nowy test różnicowy (27 kroków: realizacja, harmonogram, faktury, wnioski wykonawcy, podwykonawcy, rozliczenie materiałów, pogoda, dziennik):
  wyniki przed i po etapie identyczne (losowe identyfikatory w adresach normalizowane).
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-18 blueprint-przetargi”

Poprzednia wersja: „2027-01-17 blueprint-dotacje”.

Punkt 4 audytu, etap 2j – blueprint przetargów wykonawcy.

- Nowy moduł trasy_przetargi.py (blueprint „przetargi”, 29 tras, 459 linii z serwera): wyszukiwanie i lista przetargów, statusy, analiza i ocena,
  słowa kluczowe, obszar, monitoring stron BIP, raporty zwycięzców, historia zamawiającego. Automat w tle korzysta z ponownie eksportowanych nazw.
- Pełny przebieg przetargów (e2e3) – wynik identyczny przed i po etapie.
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-17 blueprint-dotacje”

Poprzednia wersja: „2027-01-16 blueprint-zamawiajacy”.

Punkt 4 audytu, etap 2i – blueprint dotacji.

- Nowy moduł trasy_dotacje.py (blueprint „dotacje”, 19 tras, 504 linie z serwera): wyszukiwanie i harmonogram naborów, alerty, projekty dotacyjne
  (analiza, przygotowanie, sprawdzenie – AI), wniosek o dotację, zapytania ofertowe w projektach dotacyjnych, współczynniki SO.
- Korekta grupowania: trasy /wnioski (wnioski wykonawcy o zmianę umowy – prace dodatkowe, różnice w dokumentacji, przeszkody) trafiły do grupy
  przez przedrostek nazwy; etap cofnięty i wykonany bez nich – należą do realizacji.
- Moduł miał słabe pokrycie testami – nowy test różnicowy (18 kroków: zapytanie dotacyjne, dokumenty, protokół, ocena, wyniki, harmonogram,
  alerty, SO, nabór z linku): wyniki przed i po etapie identyczne (losowe identyfikatory alertów normalizowane).
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-16 blueprint-zamawiajacy”

Poprzednia wersja: „2027-01-15 blueprint-odwolania”.

Punkt 4 audytu, etap 2h – blueprint zamawiającego publicznego.

- Nowy moduł trasy_zamawiajacy.py (blueprint „zamawiajacy_publiczny”, 31 tras, 475 linii z serwera): plan zamówień, sprawozdanie do UZP,
  ochrona ludności, ogłoszenia o wykonaniu umów, szacowanie wartości, kalkulator kosztów pracy.
- Problem wykryty przez regresję i usunięty: funkcje sprawozdania miały zmienną lokalną „S” – zasłaniała alias serwera (błąd 500 w /api/sprawozdanie).
  Narzędzie wydzielania zmienia teraz nazwę takiej zmiennej na S_lok (4 funkcje); wcześniejsze blueprinty sprawdzone – bez tej kolizji.
  Narzędzie zatrzymuje się też na funkcjach z instrukcją global (żaden blueprint ich nie ma).
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-15 blueprint-odwolania”

Poprzednia wersja: „2027-01-14 blueprint-windykacja”.

Punkt 4 audytu, etap 2g – blueprint odwołań (moduł właściciela).

- Nowy moduł trasy_odwolania.py (blueprint „odwolania”, 9 tras, 467 linii z serwera).
- Blokada modułu właściciela obejmuje trasy blueprintu (właściciel 200, inny administrator 403/404).
- Testy odwołań przed i po etapie: odw_test, odw_wysz_test – bez błędów; odw_serwer_test i etap2_test – ten sam wynik co przed etapem
  (błąd danych przykładowych w samych testach, sprzed podziału serwera – do sprawdzenia osobno).
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-14 blueprint-windykacja”

Poprzednia wersja: „2027-01-13 blueprint-nieruchomosci”.

Punkt 4 audytu, etap 2f – blueprint windykacji (moduł właściciela).

- Nowy moduł trasy_windykacja.py (blueprint „windykacja”, 20 tras, 414 linii z serwera).
- Blokada modułu właściciela działa także dla tras w blueprincie: właściciel – 200, inny administrator – 403/404.
- Kontrole: 447 tras, bez duplikatów; bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów (w tym windykacja i e-Sąd), ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-13 blueprint-nieruchomosci”

Poprzednia wersja: „2027-01-12 blueprint-kreator”.

Punkt 4 audytu, etap 2e – blueprint nieruchomości.

- Nowy moduł trasy_nieruchomosci.py (blueprint „nieruchomosci”, 35 tras, 1155 linii z serwera): lista i dane nieruchomości, identyfikacja działki,
  dokumenty i rozpoznanie (AI), pisma, zdjęcia, transakcje, wyceny (porównawcza, kosztowa, segment, czynsze), plan miejscowy, raporty, operat.
- Moduł nie miał testów – nowy test różnicowy (28 kroków: utworzenie, zapis, odczyty, wyceny, plan, pisma, operat; sieć zablokowana jednakowo):
  wyniki wersji przed i po etapie identyczne (kody i treść odpowiedzi).
- Kontrole: 447 tras, bez duplikatów; trasy blueprintu bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-12 blueprint-kreator”

Poprzednia wersja: „2027-01-11 blueprint-ocena”.

Punkt 4 audytu, etap 2d – blueprint kreatora zamówienia.

- Nowy moduł trasy_kreator.py (blueprint „kreator”, 21 tras, 874 linie z serwera): tworzenie i stan kreatora, zapis kroków, wzory i źródła,
  podział na części, dokumenty, przegląd i zmiany (AI), umowa i realizacja części, powiązana ocena ofert. Funkcja pomocnicza AI
  _json_ai_z_ponowieniem zostaje w serwerze (używana też poza kreatorem, podmieniana w testach).
- Kontrole: 447 tras, bez duplikatów; trasy blueprintu bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu.

---

## Wersja „2027-01-11 blueprint-ocena”

Poprzednia wersja: „2027-01-10 blueprint-finansowanie”.

Punkt 4 audytu, etap 2c – blueprint sprawdzenia ofert.

- Nowy moduł trasy_ocena.py (blueprint „ocena”, 15 tras, 415 linii z serwera): lista i dane oceny, dokumenty i oferty, odczyt SWZ / zapytania
  i badanie ofert (AI), kryteria, rynkowość cen, dokumenty (protokół, informacja, wezwanie), ocena prawnika, weryfikacja wykonawców i referencji.
  Trasa tworzenia oceny z zapytania dotacyjnego zostaje w module zapytań.
- czesci_powiazanie_test szukał funkcji odczytu SWZ w tekście serwer.py – przeszukuje teraz także moduły tras (zmiana tylko w teście).
- Kontrole: 447 tras, bez duplikatów; trasy blueprintu bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, testy interfejsu; dodatkowo testy prawnika (prawnik, pr4, pr6), błędów i rynkowości.

---

## Wersja „2027-01-10 blueprint-finansowanie”

Poprzednia wersja: „2027-01-09 blueprint-wspolnota”.

Punkt 4 audytu, etap 2b – blueprint finansowania inwestycji.

- Nowy moduł trasy_finansowanie.py (blueprint „finansowanie”, 6 tras): źródła finansowania, pliki, odczyt umowy (AI), porównanie z umową wykonawcy (AI),
  raport; przeniesione funkcje ponownie eksportowane w serwerze.
- Narzędzia etapu 2 (wydzielanie z drzewa składni, kontrola blueprintu, regresja, przegląd widoków, wydanie) – ten sam przebieg dla każdego blueprintu.
- Kontrole: 447 tras, bez duplikatów; trasy blueprintu bez logowania – 401; pyflakes – 0 niezdefiniowanych nazw.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-09 blueprint-wspolnota”

Poprzednia wersja: „2027-01-08 rdzen-zadania”. Punkt 4 audytu, etap 2a – pierwszy blueprint.

- Nowy moduł trasy_wspolnota.py (blueprint „wspolnota”, 219 linii z serwera): Moje zapytania, nowa inwestycja, zaproszenia do wykonawców z okolicy
  (wyszukiwanie, wysyłka, rezygnacje).
- Wzorzec dla kolejnych blueprintów: nazwy z serwera pobierane w chwili wywołania (import serwer as S; S.nazwa) – jedna instancja serwera,
  podmiany w testach działają, bez importu cyklicznego; zamiana odwołań na tokenach Pythona (bez dotykania napisów i nazw argumentów),
  lista nazw z analizy statycznej (31 nazw, 56 odwołań). Blueprinty rejestrowane na końcu serwer.py.
- Poprawiony błąd sprzed tej wersji: blok `if __name__ == "__main__": app.run()` był w środku pliku – przy uruchomieniu „python serwer.py”
  serwer startował przed definicją funkcji migracji, które się nie wykonywały. Blok przeniesiony na koniec; serwer uruchomiony bezpośrednio
  rejestruje się jako moduł „serwer” (bez drugiej kopii dla blueprintów). Produkcja (gunicorn) – bez zmian.
- Kontrole: 447 tras przed i po (bez duplikatów), 5 tras w blueprincie; bez logowania – 401; Moje zapytania – izolacja kont;
  pyflakes: 0 niezdefiniowanych nazw w serwerze i module.
- serwer.py: 17 614 linii (przed punktem 4: 18 450).
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-08 rdzen-zadania”

Poprzednia wersja: „2027-01-07 rdzen-weryfikacja”. Punkt 4 audytu, etap 1d – zadania w tle (ostatni krok rdzenia).

- Nowy moduł zadania.py (190 linii): uruchamianie zadań (uruchom), postęp i przerywanie (Przerwano), blokada drugiego uruchomienia (ZadanieTrwa),
  opis błędów dla użytkownika, czasy i koszty zadań, pilnowanie pamięci procesu. Trasy /api/zadania… i obsługa błędów (@app) zostają w serwerze.
- Krok rozpoczęty w przerwanej sesji (niezatwierdzony plik i zmiany w serwerze) – sprawdzony od zera: pyflakes (0 niezdefiniowanych nazw, 0 redefinicji),
  testy podmieniające uruchom – wyniki identyczne przed i po kroku, pełna regresja.
- Nowy zadania_test (7) na prawdziwych wątkach: zadanie trwające i zakończone, blokada drugiego uruchomienia (409), błąd z komunikatem dla użytkownika,
  przerwanie przez użytkownika, inne konto nie widzi ani nie przerwie cudzego zadania, jeden słownik zadań w serwerze i module.
- Porządki: odstępy między trasami zadań, f-string bez zmiennych.
- Zauważone, poza zakresem: odw_serwer_test i etap2_test (moduł odwołań) kończą się błędem tak samo przed i po kroku – do sprawdzenia osobno.
- serwer.py: 17 820 linii (przed punktem 4: 18 450); rdzeń: dane.py, konfiguracja.py, uwierzytelnianie.py, zadania.py.
- Regresja: 21 zestawów testów, ro_test, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-07 rdzen-weryfikacja”

Poprzednia wersja: „2027-01-06 rdzen-uwierzytelnianie”.

- Wersja 2027-01-06 (etap 1c – uwierzytelnianie.py) powstała w przerwanej sesji pracy; zweryfikowana ponownie od zera: pyflakes serwera i modułu
  (0 niezdefiniowanych nazw, 0 redefinicji), żaden test nie podmienia przeniesionych funkcji, pełna regresja (19 zestawów, 107 tras, 144 widoki,
  testy interfejsu) i nowy auth_test (8): brak dostępu bez logowania i przy błędnym haśle, logowanie administratora, dodanie konta użytkownika,
  dostęp użytkownika do własnych danych, odmowa zarządzania kontami i modułu tylko dla właściciela, licznik nieudanych prób.
- uwierzytelnianie._marka: zmienna lokalna „g” → „ust” (zasłaniała obiekt flask.g; bez zmiany działania).

---

## Wersja „2027-01-06 rdzen-uwierzytelnianie”

Poprzednia wersja: „2027-01-05 rdzen-konfiguracja”. Punkt 4 audytu, etap 1c – logowanie i uprawnienia.

- Nowy moduł uwierzytelnianie.py (231 linii, 22 nazwy): hasła (PBKDF2), konta i role, poziomy dostępu do modułów (moze, rola_def),
  dostęp do projektów (ma_dostep, ukryj_innych), dziennik aktywności, dekoratory wymaga_logowania i tylko_admin, licznik prób logowania.
- Funkcje rejestrowane w aplikacji (@app.before_request: blokada modułów właściciela, kontrola dostępu) zostają w serwerze.
- pyflakes: 0 niezdefiniowanych nazw w serwerze; licznik prób logowania – jeden obiekt dla serwera i modułu (blokada po 5 próbach działa).
- Nowy test auth_test (10): brak dostępu bez logowania, logowanie administratora i konta, błędne hasło, izolacja projektów między kontami
  (lista i dostęp bezpośredni → 404), odmowa funkcji administratora (403), blokada po 5 próbach.
- serwer.py: 17 985 linii (przed punktem 4: 18 450).
- Regresja: 19 zestawów testów, auth_test, ro_test, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-05 rdzen-konfiguracja”

Poprzednia wersja: „2027-01-04 rdzen-dane”. Punkt 4 audytu, etap 1b – konfiguracja.

- Nowy moduł konfiguracja.py (191 linii): ustawienia programu i kont (cfg, cfg_surowy, zapisz_cfg, zapisz_ustawienia, plik_ustawien_konta, GLOBALNE),
  wartości domyślne (DOMYSLNE_WEB – wcześniej w linii 11 773 serwera), zużycie i limity AI, dane firmy z wykazu VAT (wykaz).
- Moduł rdzenia okienkowego (core) współdzielony – konfiguracja.py bierze tę samą instancję co serwer (bez podwójnego wczytania).
- 15 nazw importowanych jawnie; pyflakes: brak niezdefiniowanych nazw przed i po; brak redefinicji.
- Podmiany w testach (S.cfg, S.wykaz) działają dla wywołań z serwera; test e2e3 – wynik identyczny przed i po etapie.
- serwer.py: 18 189 linii (było 18 450 przed punktem 4).
- Regresja: 19 zestawów testów (z odwołaniami i e-Sądem), 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-04 rdzen-dane”

Poprzednia wersja: „2027-01-03 wydajnosc”. Punkt 4 audytu (podział serwer.py), etap 1a – warstwa danych.

- Nowy moduł dane.py (168 linii przeniesionych z serwer.py): katalogi i pliki danych, konto bieżące i pliki zależne od konta, globalna blokada,
  pamięć podręczna JSON (LRU), czytaj / czytaj_ro / pisz, projekty_ro, pdir / meta / zapisz_meta. Moduł nie zależy od serwera.
- serwer.py importuje 48 nazw jawnie (bez „import *”), żeby analiza statyczna (pyflakes) nadal wykrywała brakujące nazwy – przed i po etapie: 0.
- Ustawienia warstwy danych zmienia się w module (DANE.PAMIEC_LIMIT), nie w kopii nazwy w serwerze.
- Bez zmian w działaniu programu; Dockerfile kopiuje cały katalog (COPY . .), więc nowy moduł trafia do obrazu.
- Regresja: 17 zestawów testów, ro_test, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-03 wydajnosc”

Poprzednia wersja: „2027-01-02 jeden-ekran”. Priorytety 1–3 z audytu wydajności i struktury.

### 1. Warstwa danych
- Pamięć podręczna JSON: usuwanie najdawniej używanych wpisów (limit 6000) zamiast czyszczenia całości przy 3000; osobna mała blokada (8 wątków).
- czytaj_ro() – odczyt bez kopiowania dla list; projekty_ro() – jedna funkcja przeglądu projektów zamiast 10 powtórzonych pętli
  (projekty, Przegląd/alerty, Moje zapytania, realizacja, ocena ofert, zapytania, dostawy, ogłoszenia o wykonaniu, archiwum, nieruchomości).
- Dzienne pliki BZP/TED czytane bez zapisu w pamięci podręcznej (nie wypychają projektów).
- Pomiar (300 projektów, 10 MB): listy 26–33 ms → 2–7 ms; zimny start 227 → 35 ms; Przegląd ~150 → ~17 ms pracy serwera.
- Test ro_test: po wywołaniu wszystkich list pamięć podręczna identyczna z plikami (brak modyfikacji współdzielonych danych).
### 2. Dostarczanie plików
- gzip dla app.js (896 → 253 kB), styl.css (101 → 21 kB) i strony głównej; skompresowana wersja w pamięci do zmiany pliku; odpowiedzi 304 zachowane.
- Wspólny endpoint Przeglądu – nie wdrożony: po punkcie 1 pięć zapytań kosztuje łącznie ~17 ms; przebudowa ładowania Przeglądu nie była warta ryzyka.
### 3. Wspólne funkcje
- liczby.liczba() – jedna zamiana tekstu na liczbę (spacje i twarde spacje, „zł”/PLN, przecinek, 1.234,56 / 1,234.56) w miejsce 21 lokalnych wersji;
  lokalne funkcje zachowują wartości domyślne i zaokrąglenia; ocena ofert i finansowanie nadal odczytują „60 miesięcy” jako 60; faktura – błąd
  dla nieczytelnej kwoty (bez zmian). Poprawione przy okazji: twarde spacje i „zł” w kwotach dawały wcześniej 0 albo brak wartości.
- zamowienie_powiazane() – jedno wyszukiwanie zamówienia powiązanego z oceną ofert (3 powtórzenia).
### Testy
- ro_test (5), test kompresji (5), test liczba() (23 przypadki); regresja: 17 zestawów, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-02 jeden-ekran”

Poprzednia wersja: „2027-01-01 zgodnosc-prawna”.

### Zamówienie na jednym ekranie – kreator (gmina i wspólnota; zgłoszenie użytkownika)
- Krok 5 „Komplet dokumentów” bez starej sekcji „Sporządzenie dokumentacji przetargowej” (drugi formularz tego samego generatora dokumentów, z nazwami
  z Pzp także we wspólnocie) – dokumenty generuje się tylko w kroku 5.
- Bez karty „Przegląd projektu” i drugiego wyboru „Rodzaj zamówienia” pod kreatorem; notatki – przycisk „Notatki (n)” w nagłówku kreatora (ten sam blok,
  dodawanie, przypinanie, archiwum); rodzaj zamówienia – wybór w nagłówku kreatora.
- Nagłówek zamówienia (nazwa, Raport, archiwizacja) nad kreatorem; bez zdublowanego „Umowa podpisana – przekaż do realizacji” (jest w kroku 7).
- Kafelki „Kosztorys prac”, „Sporządź dokumentację”, „Sprawdź dokumentację” otwierają odpowiedni krok kreatora.
- Szczegóły kroków 3 (szacowanie / kosztorys) i 6 (pełne sprawdzenie dokumentacji) zostają pod kreatorem – mają funkcje spoza kreatora.
- Moduł prawnika (bez kreatora) – bez zmian.
### Poprawki
- Zmiana rodzaju zamówienia zmieniała rodzaj tylko w projekcie, a kreator pracował na starym – teraz w obu (błąd sprzed tej wersji).
- Wspólnota: bez „Zmień: co chcesz zrobić” w menu, „Wstecz” nie prowadzi do ekranu celów, brak automatycznego ustawiania celu.
### Testy
- jeden_ekran_ui (19 sprawdzeń, obie ścieżki + prawnik); regresja: 17 zestawów, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2027-01-01 zgodnosc-prawna”

Poprzednia wersja: „2026-12-31 wspolnota-kafelki”. Poprawki po przeglądzie zgodności z przepisami (wykonawca, zamawiający, wspólnota, kosztorysowanie).

1. Wspólnota – ocena ofert bez Pzp: osobne polecenia AI (odczyt zapytania, badanie oferty – zapytanie i Kodeks cywilny); protokół wyboru, informacja
   o wyborze i wezwania bez przepisów Pzp i bez komisji przetargowej (decyzja zarządu); znacznik w danych oceny niezależny od kolejności czynności.
2. Mała wspólnota (art. 19 ustawy o własności lokali – najwyżej 3 lokale): zgoda współwłaścicieli według KC (art. 199 / 201) zamiast uchwały.
   Wybór „Zamawiający”: wspólnota / mała wspólnota / spółdzielnia (organ według statutu) / deweloper.
3. RODO: pełna informacja z art. 14 w zaproszeniach i zapytaniach do wystawców referencji (administrator, cel i podstawa, źródło i kategorie,
   odbiorcy, okres, prawa – sprzeciw, skarga do Prezesa UODO).
4. Wspólnota – nazwy dokumentów bez SWZ / OPZ: zapytanie ofertowe, opis zakresu prac, formularz oferty, wzór umowy (KC), protokół wyboru oferty
   (nazwy plików; pliki o starych nazwach nadal rozpoznawane).
5. VAT 8%: limity powierzchni (lokale do 150 m², domy do 300 m², powyżej – proporcjonalnie; lokale użytkowe – 23%) w poleceniu kosztorysu,
   umowie, wyborze stawki i instrukcji. Korekta przeglądu: „0% / zw.” już było; 5% potrzebne w module dostawcy.
6. Zaproszenia: rejestr rezygnacji („firma zrezygnowała”) – wykluczenie z list i wysyłek; bez ponownej wysyłki z programu do tej samej firmy
   w zapytaniu (pliki .eml nie blokują); uwaga w instrukcji o ocenie radcy (Prawo komunikacji elektronicznej).
7. Rażąco niska cena (art. 224 ust. 2 pkt 1): średnia wyłącza tylko oferty odrzucone na podstawie art. 226 ust. 1 pkt 1 i 10.
8. Deweloper – lista kontrolna bez pozycji o uchwale.
9. Lista kontrolna gminy: umowa dłuższa niż 12 miesięcy – płatności częściowe albo zaliczki (art. 443: ostatnia część ≤ 50%, zaliczka ≥ 5%);
   podpowiedź o terminie zapłaty (art. 447).
### Testy
- audyt_test (27), audyt_ui (4); regresja: 17 zestawów, 107 tras, 144 widoki, wszystkie testy interfejsu.

---

## Wersja „2026-12-31 wspolnota-kafelki”

Poprzednia wersja: „2026-12-30 wspolnota-osobno”.

### Wspólnota – cztery kafelki (bez ekranu wyboru celu, bez kalkulatora kosztów pracy)
- „Przygotuj zamówienie” (kreator; szacunek kosztów, dokumenty i sprawdzenie jako kroki), „Moje zapytania”, „Sprawdź złożone oferty”,
  „Realizuj umowę / inwestycje”; menu tylko z pozycjami modułu i jego nazwami.
- Moje zapytania (nowy widok): status (w przygotowaniu / zapytanie w toku / po terminie), termin, liczba ofert; na 5 dni przed terminem bez ofert –
  pytanie o zaproszenia; wyszukiwanie i wysyłka zaproszeń przeniesione tutaj z kreatora.
- Sprawdź złożone oferty: każde zapytanie ma swoje sprawdzenie (dokumenty i kryteria zapytania, dokumenty dodane później dociągane); oferty wgrywane
  ręcznie (Baza Konkurencyjności, e-mail, papier) – bez publicznego linku do składania ofert (decyzja użytkownika).
- Realizuj umowę / inwestycje: „Nowa inwestycja” dla umowy zawartej poza programem.
- Gmina: bez przypomnienia i zaproszeń (nie było ich w modelu gminy).
### Dokładna weryfikacja wykonawców (także u zamawiającego publicznego)
- KRS: kody PKD (działalność budowlana przy robotach), wykreślenie; status VAT.
- Doświadczenie wobec wymogu zapytania (liczba podobnych prac w wymaganym okresie); polisa OC na okres realizacji.
- Uprawnienia kierownika robót (e-CRUB GUNB) i Krajowy Rejestr Zadłużonych – dane do wyszukania, link i zapis wyniku (rejestry bez interfejsu
  do automatycznego sprawdzania; e-CRUB – uprawnienia od 1995 r.).
- Lista dokumentów do dosłania; sekcja „Weryfikacja wykonawców” w protokole wyboru.
### Testy
- wsp2_test (6), wsp2_ui (14, ekran telefonu), wer2_test (8); zaktualizowane testy zaproszeń i ochrony ludności (nowe miejsce zaproszeń, wspólnota bez
  ekranu celów); regresja: 16 zestawów, 107 tras, 144 widoki, wszystkie testy interfejsu.
### Instrukcja
- Rozdział 9 – cztery kafelki, Moje zapytania, weryfikacja, inwestycje; rozdział 8 – rozszerzona weryfikacja, zaproszenia w „Moich zapytaniach”.

---

## Wersja „2026-12-30 wspolnota-osobno”

Poprzednia wersja: „2026-12-29 instrukcja-uwagi”.

### Wspólnoty, spółdzielnie i deweloperzy – osobny moduł (zgłoszenie użytkownika ze zrzutami)
- Przyczyna: wspólnota była przełącznikiem w module zamawiającego – wspólne listy zamówień, ocen i realizacji; zamówienie „prywatne” ustalane polem wyboru
  w kreatorze (dostępnym w obu modułach); lista kontrolna i tryby gminy we wspólnocie.
- Osobne dane: zamówienia, oceny ofert, realizacje i przypomnienia filtrowane według modułu; moduł ustalany przy utworzeniu, bez przenoszenia
  zamówień między modułami (wyjątek: dokumenty prawnika); oceny ofert zapamiętują moduł.
- Osobne reguły (nowy plik wspolnota.py, bez Pzp): tryby (zapytanie ofertowe, wybrani wykonawcy, regulamin spółdzielni, zasada konkurencyjności
  z umowy dotacji); lista kontrolna (uchwała / plan gospodarczy – ustawa o własności lokali, szacunek kosztów, zakres prac z Prawem budowlanym,
  umowa z KC, dokumenty, RODO, rozesłanie, wymagania finansującego, protokół wyboru); warunki domyślne bez wadium i instytucji Pzp; podpowiedzi
  z podstawą w KC; termin ofert; AI (sprawdzanie dokumentów, „Sprawdzenie i zmiany”, generator) według zasad wspólnot; kafelki bez SWZ / OPZ /
  kosztorysu inwestorskiego; sekcja dokumentacji – tylko tryby modułu.
- Gmina (zamawiający publiczny) – bez elementów wspólnot, z podziałem na części; opis kafelka ochrony ludności z normami z art. 90.
### Telefon
- Przegląd rozjeżdżał się (małe kafelki w kolumnach 1fr) – kolumny minmax(0, 1fr), zawijanie nazw, opis w małym kafelku ukryty na telefonie.
### Kontrola jakości
- Kolizja nazw: alias WSP był już zajęty (obiekt Wspolne) – nowy moduł jako WSPOL; skan kolizji aliasów i przypisań w serwerze.
- Testy: moduly_test (15), moduly_ui (6, ekran 412 px), wsp_ai_test (6); regresja: 14 zestawów, 106 tras, 144 widoki, wszystkie testy interfejsu.
### Instrukcja
- Rozdział 9 napisany od nowa jako osobny moduł (podstawy prawne, uchwała, tryby, warunki, lista kontrolna, kroki).

---

## Wersja „2026-12-29 instrukcja-uwagi”

Poprzednia wersja: „2026-12-28 finansowanie”.

### Instrukcja – uzupełnienia
- Ochrona ludności: dane sprzed wersji 2026-12-24 wymagają wyboru typu gminy; do tego czasu norma dla obszaru poza miastami i ostrzeżenie.
- Zaproszenia: ogłoszenia z BZP uzupełniane co noc; pierwsze wyszukiwanie na nowym serwerze dłuższe, komunikat „lista może być niepełna”;
  wysyłka z programu wymaga poczty e-mail, bez niej pliki .eml.

---

## Wersja „2026-12-28 finansowanie”

Poprzednia wersja: „2026-12-27 zaproszenia”.

### Finansowanie inwestycji (realizacja umów zamawiającego – wspólnoty, gminy i inni)
- Sekcja „Finansowanie inwestycji (bank, BGK, KPO, dotacje)”: kilka źródeł (kredyt, premia BGK, dotacja, pożyczka), pliki umowy i załączników.
- „Odczytaj umowę (AI)”: kwota, wkład własny, termin zakończenia realizacji i rozliczenia, okres kwalifikowalności, transze z warunkami, koszty
  kwalifikowalne, wymagania wobec umowy z wykonawcą (z cytatami), dokumenty do rozliczenia, wskaźniki, sankcje; ręczne poprawki mają pierwszeństwo.
- Kontrole bez AI, liczone na bieżąco: koniec robót a termin finansowania (zapas 30 dni na odbiór i rozliczenie), etapy poza okresem kwalifikowalności,
  umowa przed okresem kwalifikowalności (dotacje, premie), transze a etapy, wartość umowy a łączne finansowanie.
- Przepływy pieniężne miesiąc po miesiącu (płatności dla wykonawcy 30 dni po końcu etapu, wpływy z transz) i największe zapotrzebowanie na środki własne.
- „Porównaj z umową wykonawcy (AI)”: status każdego wymagania (zgodne, rozbieżne, brak, do sprawdzenia), cytat i propozycja postanowienia do aneksu;
  podpisana umowa z dokumentów budowy albo wzór umowy z kreatora. Raport Word.
### Testy
- fin_test (10), fin_ui (5); regresja: testy modułów, 106 tras, 144 widoki, wszystkie testy interfejsu. Jednorazowy błąd 502 modułu pogody w przeglądzie
  widoków – chwilowy brak odpowiedzi IMGW (ponowne wywołania poprawne, moduł bez zmian).

---

## Wersja „2026-12-27 zaproszenia”

Poprzednia wersja: „2026-12-26 referencje”.

### Przypomnienie przed terminem składania ofert i zaproszenia do wykonawców z okolicy
- Na 5 dni przed terminem składania ofert (z kreatora): przypomnienie w „Terminy do pilnowania” na Przeglądzie (i w raporcie e-mail) z liczbą ofert
  w powiązanym sprawdzeniu ofert; kliknięcie otwiera zamówienie.
- Kreator, krok „Gotowe do publikacji”: „Znajdź wykonawców z okolicy (AI)” – ogłoszenia o wyniku w BZP z 24 miesięcy (bufor dzienny programu,
  brakujące dni dociągane z limitem), firmy z podobnymi pracami (podobieństwo przedmiotu i CPV) i siedzibą albo miejscem prac w promieniu 20/30 km
  (OpenStreetMap); bez firm, które już złożyły ofertę; kontakt z CEIDG, KRS i stron firm; uzasadnienie i kolejność od AI.
- Wysyłka zaproszeń z dokumentami postępowania: ze skrzynki użytkownika (SMTP) albo jako pliki .eml; w treści źródło danych i możliwość rezygnacji;
  historia zaproszeń, zaproszone firmy oznaczone. Ograniczenie opisane w programie: BZP obejmuje tylko zamówienia publiczne.
### Poprawki
- Menu wspólnot (bez wybranego celu i w celach z sekcją firmową) pokazywało „Ochrona ludności” i „Plan i sprawozdania” – ukryte we wszystkich trybach menu.
- Pierwsza pozycja menu bez wybranego celu nazywała się „Pulpit” – ujednolicono na „Przegląd”.
- Odpowiedź AI w postaci listy była odczytywana jako jeden obiekt (wyciagnij_json zwraca pierwszy obiekt) – osobny odczyt listy w zaproszeniach.
### Testy
- zaproszenia_test (9), zaproszenia_ui (7); regresja: testy modułów, 104 trasy, 144 widoki, testy interfejsu.

---

## Wersja „2026-12-26 referencje”

Poprzednia wersja: „2026-12-25 podzial-na-czesci”.

### Wiarygodność wykonawcy i referencji (sprawdzenie ofert, w tym wspólnoty)
- Z każdej oferty odczytywane są dane wykonawcy i wykaz referencji (wystawca, NIP, zakres, wartość, okres, kontakt, plik).
- „Sprawdź wykonawcę i referencje”: wykonawca w wykazie VAT i KRS (data wpisu, zarząd); wystawcy referencji w rejestrach i powiązania z wykonawcą
  (ten sam NIP, adres, te same osoby w zarządzie); ogłoszenia o wyniku w BZP przy zamawiających publicznych; metadane plików (te same daty, program,
  autor co w ofercie). Status każdej referencji: potwierdzona / niepotwierdzona / z sygnałami nieprawdziwości – sygnały do sprawdzenia, nie dowód.
- Potwierdzenie u wystawcy: gotowy e-mail z prośbą o potwierdzenie (program pocztowy albo schowek) i zapis odpowiedzi (wysłano, potwierdził,
  zaprzeczył, brak odpowiedzi); ponowna weryfikacja zachowuje odpowiedzi; limity zapytań do wykazu VAT pilnowane (bufor, maks. 10 zapytań na ofertę).
- Kreator: warunki domyślne wymagają wykazu prac z danymi kontaktowymi wystawców; w zapytaniach bez Pzp – postanowienie o odrzuceniu oferty
  i odstąpieniu od umowy przy nieprawdziwych referencjach.
- Wykaz VAT: zapisywana data rejestracji podatnika.
### Poprawka – podział na części (wersja 2026-12-25)
- „Sprawdź złożone oferty” w kreatorze tworzy teraz powiązaną ocenę ofert (dokumenty postępowania, części i limit z kreatora); wcześniej otwierał
  niepowiązaną ocenę, przez co części nie przechodziły do oceny, a zwycięzcy części – do umów. Odczyt SWZ i podpowiedź zwycięzców korzystają
  z powiązania. Testy poprzedniej wersji tego nie wykryły (dane oceny wpisane do projektu zamówienia) – dodano test realnego przepływu.
### Testy
- referencje_test (9), referencje_ui (5), czesci_powiazanie_test (6); regresja: testy modułów, 104 trasy, 144 widoki, testy interfejsu.

---

## Wersja „2026-12-25 podzial-na-czesci”

Poprzednia wersja: „2026-12-24 ochrona-ludnosci”.

### Podział zamówienia na części (art. 91 Pzp) – cały proces
- Kreator, krok „Wartość i tryb”: wybór bez podziału / podział na części; tabela części (nazwa, zakres, wartość, CPV, termin); limity z art. 91 ust. 3
  (liczba części w ofercie, liczba części dla jednego wykonawcy + zasady wyboru); kontrole: min. 2 części, nazwy, wartości, suma = wartość
  zamówienia (tryb z łącznej wartości – art. 30).
- „Zaproponuj podział (AI)”: propozycja części z uzasadnieniem i ryzykami (na podstawie opisu i działów kosztorysu), do przyjęcia i poprawienia.
- Dokumenty: generator dostaje opis części i wymagania (SWZ według części, formularz z ceną za każdą część, odrębne umowy, OPZ według części);
  lista kontrolna – sprawdzenie podziału zamiast pisma o braku podziału; pole warunków „Podział na części” uzupełniane automatycznie.
- Sprawdzenie ofert: części z SWZ (albo z kreatora), ceny i kryteria z ofert według części; ranking, punktacja i rażąco niska cena osobno w każdej
  części; ostrzeżenia: część bez ofert (art. 255 pkt 1), przekroczony limit części dla wykonawcy; protokół i informacja o wyborze według części.
- Realizacja: „Umowy podpisane – przekaż części do realizacji” – osobna umowa i realizacja dla każdej części (powiązana z zamówieniem głównym,
  podpowiedź wybranego wykonawcy z oceny ofert); ponowne przekazanie aktualizuje zamiast dublować.
- Zamówienia bez podziału – bez zmian (ranking jak dotąd).
### Testy
- czesci_test (9), czesci_ocena_test (9), czesci_real_test (6), czesci_ui (7 w przeglądarce); regresja: testy modułów, 104 trasy, 144 widoki.
### Instrukcja
- Rozdział 8: nowa sekcja „Podział zamówienia na części (art. 91 Pzp)”.

---

## Wersja „2026-12-24 ochrona-ludnosci”

Poprzednia wersja: „2026-12-23 instrukcja-pelna”.

### Ochrona ludności (gmina) – błędy merytoryczne naprawione
- Normy według art. 90 ust. 2 ustawy o ochronie ludności i obronie cywilnej (stan na 23.08.2026): w granicach miast 50% (w tym 25% w budowlach
  ochronnych), poza miastami 25% (w tym 15%). Wcześniej program stosował dla każdej gminy normę wiejską – w miastach zaniżał wymóg o połowę.
- Typ gminy (miejska / wiejska / miejsko-wiejska); w gminie miejsko-wiejskiej ludność i obiekty osobno dla miasta i terenu poza miastem.
- Punkty schronienia (art. 84a) nie wliczają się do pokrycia obiektów zbiorowej ochrony.
- Pokrycie potwierdzone (tylko obiekty sprawne) i deklarowane (z obiektami do sprawdzenia i wymagającymi prac) – wcześniej obiekty niesprawdzone
  zawyżały pokrycie.
- Nagłówek: normy z ustawy (wcześniej błędnie przypisane uchwale), uchwała nr 72 RM zm. uchwałą nr 151 z 4.11.2025; program 2025–2026 obowiązuje
  do 31.12.2026. Raport Word według obszarów.
### Wspólnoty, spółdzielnie, deweloperzy
- Cel „Ochrona ludności i obrona cywilna (gmina)” (i roczny plan) ukryty w ścieżce zamawiającego prywatnego – wcześniej był widoczny mimo ukrytego
  kafelka; zapamiętany cel gminy nie otwiera modułu; wejście inną drogą pokazuje wyjaśnienie.
### Testy
- gmina_test zaktualizowany (wcześniejsza asercja utrwalała błędne liczenie); nowy test przeglądarkowy olioc_ui (8 sprawdzeń); regresja bez błędów.

---

## Wersja „2026-12-23 instrukcja-pelna”

Poprzednia wersja: „2026-12-22 zgodnosc-pzp”.

### Instrukcja obsługi – przebudowa (pełna, bez modułów widocznych tylko dla właściciela)
- Przyczyny słabej instrukcji (11.12): treść skrócona z ok. 155 do 38 tys. znaków, kolejne zmiany doklejane w środek, każdy rozdział od nowej strony
  z osieroconymi nagłówkami, ucięte nazwy w menu na zrzutach, kontrola tylko w jedną stronę.
- Teraz: 16 rozdziałów, ok. 155 tys. znaków, 75 stron PDF; szczegółowa treść poprzedniej pełnej instrukcji (z historii, 10.12) sprawdzona z programem +
  nowe moduły (TED, usługi pracochłonne i kalkulator, wspólnoty, plan i sprawozdania, ochrona ludności, szacowanie wartości zgodne z Pzp).
- W każdym rozdziale ścieżki: tabela „Cele, kroki i kafelki” generowana z kodu programu (nazwy zawsze zgodne, nic nie pominięte).
- Bez Odwołań, Leadów, Księgowości i Windykacji; usunięte nieaktualne fragmenty (kosztorys inwestorski AI, stare numery rozdziałów);
  9 nazw przycisków ze starej instrukcji poprawionych na obecne (np. „Archiwizuj”, „Pokaż wszystkie kroki”, „Wysyłaj mi kopię zamówień”).
- 24 nowe zrzuty (1440 px, dane pokazowe), bez uciętych nazw; zrzuty ograniczone wysokością w PDF; nagłówki trzymane z treścią.
- Kontrola automatyczna: zakazane moduły i nieaktualne treści, nazwy przycisków, kompletność (kafelki, cele, kroki), odwołania do rozdziałów,
  mapa widok → rozdział (44 widoki); każda strona PDF obejrzana.
### Program
- Menu boczne na komputerze: długie nazwy kroków zawijają się zamiast ucinać.
- Pomoc czyta całą instrukcję (limit 120 → 200 tys. znaków – wcześniej ostatnie rozdziały byłyby niewidoczne dla Pomocy).
- Mapa widok → rozdział instrukcji według nowej numeracji.

---

## Wersja „2026-12-22 zgodnosc-pzp”

Poprzednia wersja: „2026-12-21 windykacja-esad”.

### Kontrola zgodności ścieżki zamawiającego z Pzp (sprawdzone w źródłach: tekst ustawy, orzecznictwo KIO, UZP)
- Poprawiony błąd: minimalny termin składania ofert w przetargu nieograniczonym (procedura unijna) – 35 dni od przekazania ogłoszenia UPUE
  (art. 138 ust. 1), krócej (nie mniej niż 15 dni) tylko w przypadkach z art. 138 ust. 2; wcześniej program przyjmował 30 dni („30–35”).
- Doprecyzowane: kryterium ceny powyżej 60% / jako jedyne – tylko ze standardami jakościowymi w OPZ albo kosztami cyklu życia (art. 246 ust. 2);
  podstawy prawne przy terminie ofert w trybie podstawowym (art. 283: 7 / 14 dni), wadium (art. 281 ust. 3: do 1,5%), zabezpieczeniu
  (art. 452 ust. 2–3: do 5%, wyjątkowo do 10% z uzasadnieniem; art. 453: zwrot 70% / 30%); plan postępowań w liście kontrolnej – tylko dla
  zamawiających z obowiązkiem (art. 23).
- Potwierdzone bez zmian: próg Pzp 170 000 zł od 1.01.2026 (130 000 zł tylko dla postępowań wszczętych wcześniej), progi UE 2026–2027, kurs 4,31,
  waloryzacja (art. 439, umowy > 6 mies.), limit kar (art. 436), części (art. 91), umowa o pracę (art. 95), kwota przed otwarciem (art. 222 ust. 4),
  szacowanie (art. 28–36), plan (art. 23), sprawozdanie (art. 82, próg według roku), odwołania (art. 515: 5 / 10 dni).

---

## Wersja „2026-12-21 windykacja-esad”

Poprzednia wersja: „2026-12-20 windykacja-ksef”.

### Windykacja – pozew do e-sądu (elektroniczne postępowanie upominawcze)
- Sprawdzone w oficjalnych źródłach: karta usługi EPU na gov.pl (opłaty 2026, podpis i opłata wyłącznie w systemie, po opłacie pozew trafia do sądu
  automatycznie) i dokumentacja techniczna e-sądu (e-sad.gov.pl, page_id=32): usługa sieciowa tylko dla powodów masowych / pełnomocników /
  komorników (apikey) – dlatego program przygotowuje plik importu, a import, podpis i opłata – w e-sądzie.
- Pozew: należność główna (pozostała po wpłatach) z odsetkami ustawowymi za opóźnienie w transakcjach handlowych od dnia po terminie do dnia zapłaty
  (kod 15 schematu), rekompensata (1 na transakcję) z odsetkami ustawowymi od wniesienia (kod 8), opcjonalnie skapitalizowane odsetki za faktury
  zapłacone po terminie; dowody: faktury, wezwanie do zapłaty, nota; uzasadnienie (do edycji); sąd: SR Lublin-Zachód w Lublinie, VI Wydział Cywilny.
- Opłata według tabeli gov.pl (30 / 50 / 100 / 125 / 188 / 250 zł, powyżej 20 000 zł 1,25%, maks. 25 000 zł), wartość sporu zaokrąglona w górę.
- Kontrola: roszczenia wymagalne w ostatnich 3 latach, dane i adresy stron, PESEL osoby składającej, rachunek, wezwanie przedsądowe, KRZ.
- Pozwany z wykazu VAT (nazwa, KRS, REGON, adres rozłożony na pola, rodzaj strony); PESEL zaszyfrowany, nie wraca do przeglądarki.
- Podgląd pozwu (Word) → „Akceptuję pozew” → plik XML do importu, walidowany oficjalnym schematem PozewEPU.xsd (osadzonym w epu_schemat.py –
  trafia na serwer bez zmian w Dockerfile); przy błędach pliku nie wydajemy. Instrukcja 5 kroków w e-sądzie; „Pozew złożony” z sygnaturą →
  status „w sądzie (EPU)”.
### Testy
16 testów (braki, odrzucenie, kody odsetek, opłata, dowody, PESEL, plik zgodny ze schematem – niezależna walidacja, złożenie), oficjalny przykład e-sądu
przechodzi walidację, przeglądarka (komputer, telefon) – 0 błędów.

---

## Wersja „2026-12-20 windykacja-ksef”

Poprzednia wersja: „2026-12-19 windykacja”.

### Windykacja niezależna od Księgowości – pobieranie z KSeF
- Usunięty import z ewidencji Księgowości; „Pobierz z KSeF” pobiera faktury sprzedaży bezpośrednio z KSeF (w tle, przyrostowo – tylko nowe numery,
  od daty ostatniego pobrania albo 90 dni wstecz), termin płatności i znacznik zapłaty z XML.
- Token: własny (Ustawienia → KSeF, zaszyfrowany) ma pierwszeństwo; bez własnego – token zapisany w Księgowości tego konta; bez obu – czytelny komunikat.
  NIP i środowisko KSeF w ustawieniach modułu.
- Tylko faktury sprzedaży (Subject1) – nie zużywa limitu KSeF na faktury zakupu; w Księgowości nowy, opcjonalny parametr funkcji pobierania
  (domyślnie bez zmian – sprzedaż i zakupy).
### Testy
30 testów modułu (w tym token z Księgowości / własny / usunięcie, pobieranie tylko sprzedaży, bez duplikatów, konto bez Księgowości), Księgowość bez zmian.

---

## Wersja „2026-12-19 windykacja”

Poprzednia wersja: „2026-12-18 szacowanie-wartosci-pzp”.

### Nowy moduł: Windykacja (właściciel programu i konta, którym go udostępni)
- Dostęp: właściciel zawsze; inne konta – po udostępnieniu w „Kontach i aktywności” (kolumna „Windykacja”, widoczna tylko dla właściciela);
  blokada na serwerze (/api/wind); kafelek i menu tylko z dostępem; każde konto ma osobne dane; edycja dla urzędu – wyłączony; poza instrukcją.
- Faktury: z Księgowości (sprzedaż, termin i znacznik zapłaty z e-faktury XML KSeF), z plików (XML KSeF, CSV, Excel), ręcznie; bez duplikatów.
- Wpłaty: wyciąg bankowy (CSV, Excel) – dopasowanie po numerze faktury w tytule albo po NIP i kwocie; reszta do ręcznego przypisania.
- Odsetki ustawowe za opóźnienie w transakcjach handlowych według półroczy (I 2026: 14% / 12%, II 2026: 13,75% / 11,75% – obwieszczenia
  M.P. 2025 poz. 1257 i M.P. 2026 poz. 642), także za zapłaty po terminie; dłużnik – publiczny podmiot leczniczy (niższa stawka); konsument – bez.
- Rekompensata 40 / 70 / 100 € (progi 5 000 i 50 000 zł) po średnim kursie NBP z ostatniego dnia roboczego miesiąca przed wymagalnością (API NBP);
  jedna na transakcję – domyślnie na kontrahenta, „osobne transakcje” albo pole umowy.
- Harmonogram (do ustawienia): przypomnienie 3 dni przed, 1 i 7 dni po terminie, nota (14), wezwanie (21), decyzja (30); przypomnienia –
  treść do wysłania z własnej poczty (bez wysyłki automatycznej); nota odsetkowa i wezwanie przedsądowe (Word) – po zatwierdzeniu;
  decyzja: e-sąd, ugoda / raty, odpuszczenie.
- Kontrahenci: e-mail, wykaz VAT (biała lista), odnośnik do Krajowego Rejestru Zadłużonych.
- Pulpit: należności otwarte i po terminie, wiek należności, najwięksi dłużnicy, wpływy w 30 dni, odsetki i rekompensaty do żądania, odzyskane.
### Kontrola przed wydaniem
- Wykryta i poprawiona kolizja aliasu importu (WN – wnioski / windykacja); kontrola obejmuje teraz zdublowane funkcje i aliasy importów.
### Testy
22 testy modułu (dostęp, import, odsetki, rekompensata, harmonogram, dokumenty, wyciąg, decyzje) + przeglądarka (4 konta/szerokości) – 0 błędów.

---

## Wersja „2026-12-18 szacowanie-wartosci-pzp”

Poprzednia wersja: „2026-12-17 plan-i-sprawozdania”.

### Zamawiający publiczny – szacowanie wartości zamówienia zgodnie z przepisami (bez kosztorysu inwestorskiego przez AI)
- Błąd merytoryczny: wartość zamówienia brana z „kosztorysu inwestorskiego (AI)”; nazwa „kosztorys inwestorski” także przy dostawach i usługach;
  notatka z szacowania wpisywała „kosztorys inwestorski” i „ceny z internetu” jako metodę.
- Krok „Wartość i tryb” → panel „Szacowanie wartości zamówienia (art. 28–36 Pzp)” z wyborem podstawy ustalenia wartości:
  roboty (art. 33): kosztorys inwestorski albo planowane koszty według PFU / zaprojektuj i wybuduj – dokument sporządza projektant albo kosztorysant
  (rozporządzenie MRiT z 20.12.2021 r.), program go przyjmuje, odczytuje wartość netto i datę, sprawdza wymagane części;
  dostawy i usługi (art. 28, 34): udokumentowane źródła cen – oferty cenowe (zapytanie o cenę – Word), ceny z rozstrzygniętych przetargów (pamięć BZP/TED),
  wcześniejsze umowy, kalkulacja kosztów pracy, cenniki, konsultacje rynkowe; średnia / mediana / wskazane źródło; ostrzeżenia (jedno źródło, rozrzut).
- Składniki: prawo opcji, zamówienia z art. 214 ust. 1 pkt 7 i 8; data ustalenia, osoba; kontrola terminu 6 / 3 miesięcy przed wszczęciem (art. 35).
- Nowa notatka z szacowania: podstawa prawna, dokument albo źródła, wyliczenie, wartość netto i w euro, tryb.
- Wartość zamówienia publicznego (tryb, dokumenty, realizacja – wartość szacunkowa, lista kontrolna, komplet ZIP) z szacowania, nigdy z kosztorysu AI;
  sekcja projektu „Szacowanie wartości zamówienia”; kafelek „Kosztorys prac” (AI) ukryty u zamawiającego publicznego.
- Zamawiający prywatny (wspólnoty, spółdzielnie, deweloperzy – bez Pzp): „Szacunek kosztów (AI)” zostaje, oznaczony jako niebędący kosztorysem inwestorskim.
- Instrukcja (rozdział 8 i 9) zaktualizowana.
### Testy
Roboty: kosztorys AI 9,99 mln zł nie jest wartością; odczyt wgranego kosztorysu (1 234 567,89 zł, data, elementy rozporządzenia), tryb, notatka (art. 33),
lista kontrolna. Usługi: źródła, średnia + opcja, ostrzeżenia, art. 35, notatka, zapytanie o cenę, ceny z przetargów. Prywatny: szacunek AI. Przeglądarka – 0 błędów.

---

## Wersja „2026-12-17 plan-i-sprawozdania”

Poprzednia wersja: „2026-12-16 menu-telefon”.

### Zamawiający – wspólna ikona „Roczny plan zamówień / Sprawozdania do UZP”
- Jedna ikona zamiast dwóch (plan i sprawozdanie) we wszystkich celach zamawiającego; w menu jedna pozycja „Plan i sprawozdania”.
- Po wejściu – ekran wyboru: „Roczny plan zamówień” albo „Sprawozdania do UZP”, z bieżącym stanem (pozycje planu, publikacja / termin; zamówienia
  w rejestrze sprawozdania, termin 1 marca); w obu modułach przycisk powrotu do ekranu wyboru; przejście nie zmienia wybranego celu.
- Cel „Roczny plan zamówień / Sprawozdania do UZP” (pierwszy u zamawiającego). Ścieżka wspólnot – bez ikony. Edycja dla urzędu – dostępna.
- Instrukcja (rozdział 8): ekran wyboru, nowe nazwy, kto składa sprawozdanie (art. 82 – każdy zamawiający, który udzielił zamówienia), nowe zrzuty.

---

## Wersja „2026-12-16 menu-telefon”

Poprzednia wersja: „2026-12-15 roczny-plan-zamowien”.

### Menu na smartfonie
- Błąd: kafelki menu (☰) w dwóch kolumnach wychodziły poza prawą krawędź ekranu – kolumna „1fr” nie zwęża się poniżej najdłuższego słowa etykiety,
  a przy powiększonym tekście w telefonie napisy były ucięte.
- Teraz: kolumny repeat(2, minmax(0, 1fr)), etykiety zawijają się w kafelku, mniejsze kafelki (64 px) i ikony, czcionka zależna od szerokości ekranu;
  poniżej 360 px – jedna kolumna (lista).
### Testy
Menu: 340, 360, 393 i 412 px, także z tekstem powiększonym o 30% – bez wychodzenia poza ekran i bez uciętych napisów; 76 widoków na 360 px – treść mieści się.

---

## Wersja „2026-12-15 roczny-plan-zamowien”

Poprzednia wersja: „2026-12-14 leady-zbieranie-diagnostyka”.

### Zamawiający – Roczny plan zamówień (plan postępowań, art. 23 Pzp) – pierwszy cel i kafelek
- Zgodnie z art. 23 Pzp i rozporządzeniem z 18.12.2020 r. w sprawie wzoru planu postępowań (Dz.U. 2020 poz. 2362) – sprawdzone w opracowaniu UZP;
  progi zweryfikowane: próg Pzp od 1.01.2026 r. 170 000 zł (ustawa z 25.07.2025 r.), progi UE 2026–2027 (5 404 000 € / 216 000 € / 140 000 €), kurs 4,31 zł/€.
- Plan wewnętrzny (wszystkie zamówienia) i plan postępowań do BZP (tylko objęte Pzp) w dwóch tabelach (poniżej / od progów UE), według rodzaju;
  tryby z zamkniętych list wzoru, dobierane do wartości; informacje dodatkowe (konsultacje, innowacyjne, społeczne, środowiskowe, zastrzeżone).
- Kontrole: tryb a wartość, możliwe dzielenie zamówienia (roboty – klasa CPV, dostawy/usługi – grupa CPV; art. 29–30), brak CPV, termin 30 dni od budżetu.
- Pozycje: ręcznie, import z Excela (wzór), propozycje z uchwały budżetowej / planu finansowego (AI, w tle), kopia z poprzedniego roku.
- Publikacja: zestawienie do formularza BZP (Excel, z arkuszem aktualizacji i planem wewnętrznym), plan na stronę internetową (Word), zapis wersji;
  aktualizacje: zmiana, dodanie, rezygnacja (usunięcie opublikowanej pozycji = rezygnacja), historia wersji.
- „Uruchom postępowanie”: kreator z danymi pozycji, pozycja planu zapisana w projekcie (do ogłoszenia o zamówieniu), status „wszczęte”.
- Przegląd zamawiającego: przypomnienia (termin publikacji, pozycje do wszczęcia). Edycja dla urzędu – dostępne; ścieżka wspólnot – ukryte.
- Instrukcja: sekcja w rozdziale 8 ze zrzutem.
- Kontrola przed wydaniem: wszystkie pliki bez zdublowanych nazw funkcji (Python i JavaScript) – nazwa pomocnicza nowego modułu przesłaniała funkcję planu projektu w Dotacjach; poprawione przed wydaniem.
### Testy
API (kategorie, kontrole, publikacja i aktualizacja, Excel/Word, import, kopia, kreator, przypomnienia), propozycje z uchwały budżetowej (Word),
przeglądarka (pełna edycja, edycja urzędu, telefon, wspólnoty) – 0 błędów.

---

## Wersja „2026-12-14 leady-zbieranie-diagnostyka”

Poprzednia wersja: „2026-12-13 leady-zwyciezcy-caly-rynek”.

### Leady – „Zwycięzcy” pusta lista po wdrożeniu
- Przyczyny: (1) rozstrzygnięcia zbierały się dopiero w nocy albo po „Pobierz teraz” – przy pierwszym otwarciu pamięć była pusta;
  (2) komunikat przy pustej liście był z poprzedniej wersji („zwycięzcy z modułu Odwołań”) – mylący; (3) słowo w „Słowa w przedmiocie”
  (np. „roboty”) odrzucało tytuły bez tego słowa („Przebudowa drogi”).
- Teraz: przy pierwszym otwarciu (mniej niż 10 dni w pamięci) rozstrzygnięcia z 21 dni zbierają się w tle z komunikatem i samoczynnym odświeżaniem;
  pusta lista pokazuje diagnostykę: rozstrzygnięcia w okresie i województwie, po rodzaju, po słowach, po cenie – z podpowiedzią, gdy wszystko odrzucają słowa.
- Powtórzenia rozstrzygnięć usuwane przed liczeniem (diagnostyka zgodna z listą).
### Testy
Scenariusz z pustą pamięcią (dolnośląskie, roboty, słowo „roboty”): zbieranie w tle, diagnostyka 98 → 12 → 0, bez słowa 12 zwycięzców; przeglądarka – 0 błędów.

---

## Wersja „2026-12-13 leady-zwyciezcy-caly-rynek”

Poprzednia wersja: „2026-12-12 moduly-wlasciciela”.

### Leady – zwycięzcy z całego rynku (moduł właściciela)
- Dotąd zwycięzcy pochodzili tylko z postępowań obserwowanych w module Odwołań (region, próg 1 mln zł) – za wąsko.
- Pamięć rozstrzygnięć: co noc (i przy „Pobierz teraz”) ogłoszenia o wyniku z BZP dla 16 województw (wykonawca, NIP, siedziba, cena, liczba ofert –
  ten sam odczyt co „Konkurencja u zamawiającego” i raport powiatów) oraz ogłoszenia o udzieleniu zamówienia z TED (zwycięzca, NIP, miejscowość,
  wartość części, województwo z miejsca realizacji); pobierane tylko brakujące dni z ostatnich 21, ostatnie 3 dni ponownie.
- „Zwycięzcy”: rozstrzygnięte w ostatnich N dni (domyślnie 14), województwo, rodzaj, słowa, cena; etap „umowa zawarta” (BZP, TED – dla podwykonawców,
  dostawców, wynajmu, ubezpieczeń) i „przed umową” (z Odwołań, z szacunkiem zabezpieczenia 5% – dla gwarantów) na początku listy.
- Kontakt na żądanie: „Pobierz kontakt” przy firmie (biała lista VAT, KRS, CEIDG, strona www, e-Doręczenia) – zapamiętany 30 dni, w CSV.
- Wspólna funkcja danych firmy (kontakt_firmy) dla Odwołań i Leadów.
### Testy
Na żywo, 2 dni: 824 rozstrzygnięcia w 34 s; 636 zwycięzców w oknie 5 dni (98 dolnośląskie, 58 robót); kontakt TERLAN S.A. i PGE Obrót z rejestrów;
„przed umową” z Odwołań; CSV; przeglądarka – 0 błędów.

---

## Wersja „2026-12-12 moduly-wlasciciela”

Poprzednia wersja: „2026-12-11 nowa-instrukcja”.

### Odwołania, Leady, Księgowość – tylko dla właściciela programu
- Dostęp wyłącznie dla właściciela (konto z instalacji, APP_USER) – blokada na serwerze dla /api/odw, /api/leady, /api/ksieg (odmowa 403 także dla
  użytkowników z rolą administratora); kafelki i menu tylko u właściciela; moduły usunięte z edytora ról; kolumna „Księgowość” w Kontach i aktywności usunięta.
- Pomoc nie zna tych modułów (usunięte z listy przejść i opisu programu).
### Instrukcja bez tych modułów
- Usunięte rozdziały Odwołania, Leady, Księgowość i wzmianki w innych rozdziałach (moduły dodatkowe, źródło KSeF, konta, edycja urzędu, pytania);
  rozdziały przenumerowane (16), mapa rozdziałów w programie zaktualizowana; zrzuty ekranu bez tych pozycji menu. PDF: 30 stron.
### Wczytywanie Leadów i Odwołań
- Postępowania dodane do Odwołań przed zapisem województwa wypadały z filtru regionu (Odwołania i Leady – stąd puste listy) – województwo uzupełniane
  z e-Zamówień, z ogłoszenia w pamięci albo z danych zamawiającego i zapisywane na stałe.
- Ogłoszenia zapisane w pamięci przed wersją z leadami nie miały danych o wadium (lista wadialna pusta) – jednorazowe uzupełnienie w tle (ostatnie 45 dni,
  ponowne pobranie z BZP); komunikat w module i samoczynne odświeżenie.
- Leady: „Wczytywanie…” podczas pobierania i wyjaśnienie, gdy lista jest pusta.

---

## Wersja „2026-12-11 nowa-instrukcja”

Poprzednia wersja: „2026-12-10 gmina-edycja-urzedu”.

### Instrukcja przebudowana od podstaw
- Przyczyna bałaganu na pierwszej stronie: opisy nowych funkcji były dopisywane przed pierwszym znacznikiem </section> – czyli na stronie tytułowej.
- Nowa struktura: 19 rozdziałów według obecnych ścieżek i modułów (ścieżki z ekranu startowego, cele „Co chcesz zrobić?”, moduły Odwołania, Leady,
  Księgowość, kalkulator, ochrona ludności, sprawozdanie, wspólnoty), w każdym: gdzie to jest, kroki, ograniczenia.
- 88 starych zrzutów ekranu zastąpionych 16 nowymi z bieżącej wersji (konto „demo”, fikcyjna firma); HTML 11,5 MB → 2 MB, PDF 11 MB → 1,7 MB (36 stron).
- Kontrola zgodności: każda wyróżniona nazwa przycisku, kafelka i celu istnieje dosłownie w programie (poprawione m.in. „Utwórz projekt” → „Przygotuj ofertę”,
  warianty cen A/B, „Tak, mam swoje wzory”); usunięte zdania niepotwierdzone przez program.
- Mapa rozdziałów: każdy widok programu otwiera właściwy rozdział (nowe moduły dopisane; ścieżka wspólnot → rozdział 9).
- Pomoc: lista modułów, do których Pomoc może przenieść, uzupełniona o nowe moduły; opis programu w poleceniu Pomocy zaktualizowany.

### Poprawka
- Domyślna nazwa i adres firmy w ustawieniach („Revival Alicja Grześlowska”, adres w Warszawie) z wczesnej wersji – zmienione na puste pola
  do uzupełnienia w Profilu firmy (nowe konta nie dostają cudzej nazwy w dokumentach). Zapisane profile bez zmian.

---

## Wersja „2026-12-10 gmina-edycja-urzedu”

Poprzednia wersja: „2026-12-09 gmina-olioc-sprawozdanie-uzp”.

### Sprawdzenie modułów Ochrona ludności i Sprawozdanie roczne – poprawki
- Błąd: w edycji dla urzędu oba moduły (i kalkulator kosztów pracy) były niewidoczne – brak na liście widoków dozwolonych w tej edycji.
- Z repozytorium i pakietu usunięty przypadkowo dołączony plik skompilowany (__pycache__/serwer.cpython-312.pyc, 1,5 MB); dodany .gitignore.
- Sprawdzone: pokrycie ludności (budowle 15%, wszystkie obiekty 25%), brakujące miejsca, ryzyko zwrotu dotacji po terminie, raport Word;
  przypisanie zamówień do sekcji sprawozdania (II, III, IX), zestawienie Excel; widoczność w każdym celu zamawiającego w obu edycjach, telefon.

---

## Wersja „2026-12-09 gmina-olioc-sprawozdanie-uzp”

Poprzednia wersja: „2026-12-08 uslugi-pracochlonne-cel”.

### Ochrona ludności i obrona cywilna – pakiet dla gminy (nowy moduł ochrona_ludnosci.py)
- Cel zamawiającego „Ochrona ludności i obrona cywilna (gmina)”, kafelek i menu. Program OLiOC 2025–2026 (uchwała nr 72 RM z 27.05.2025).
- Inwentaryzacja obiektów zbiorowej ochrony; pokrycie: budowle ochronne co najmniej 15%, wszystkie obiekty co najmniej 25% ludności (brakujące miejsca).
- Zadania w 6 obszarach programu: dotacja, wkład, termin, status, wydatki; alerty: kwota do zwrotu po terminie, wydatek po terminie,
  termin w ciągu 30 dni, brak zamówienia, przekroczenie dotacji, zadanie poza obszarami.
- „Utwórz zamówienie” (kreator, rodzaj według obszaru, budżet = dotacja + wkład) i powiązanie z zadaniem; raport Word.
- Zestawy wyszukiwarki „Ochrona ludności (schrony)” i „Ochrona ludności (wyposażenie)”.
### Roczne sprawozdanie o udzielonych zamówieniach do UZP (nowy moduł sprawozdanie_uzp.py)
- Art. 82 Pzp; rozporządzenie z 20.12.2021 r. (Dz.U. poz. 2463); objaśnienia UZP; termin 1 marca; formularz na platformie e-Zamówienia.
- Import zamówień z projektów (umowy zawarte w roku; tryb z kreatora, wartość umowy z realizacji, oferty i odrzucone z badania ofert; bez zamawiającego prywatnego),
  pozycje ręczne; przypisanie do sekcji II, III, V, VIII, IX według wartości szacunkowej, progu krajowego (130 tys. zł do 2025, 170 tys. zł od 2026),
  progów unijnych (klasyczne i sektorowe/obronne), usług społecznych i wyłączeń; sekcje IV, VI, VII z zaznaczonych aspektów; lista braków.
- Arkusz Excel w układzie formularza (sekcje I–IX + braki; Arial, sumy formułami, żółte komórki do uzupełnienia) – przeliczony w LibreOffice bez błędów.
- Na ścieżce wspólnot, spółdzielni i deweloperów oba moduły ukryte (zamawiający prywatny nie składa sprawozdania).
### Naprawione przy okazji
- Badanie ofert: niepełne dane (np. oferta bez identyfikatora) dawały błąd serwera – brakujące elementy uzupełniane przy odczycie.
### Testy
14 testów obu modułów (sekcje dla progów 2025/2026, unijnych, sektorowych, usług społecznych, wyłączeń; zestawienie i braki; import bez powtórzeń;
arkusz; pokrycie i alerty; powiązanie; raport) + przeglądarka (cel, menu, utworzenie zamówienia, import, telefon) – 0 błędów; regresja bez zmian.

---

## Wersja „2026-12-08 uslugi-pracochlonne-cel”

Poprzednia wersja: „2026-12-07 wspolnoty-deweloperzy”.

### Sprawdzenie, czy dzisiejsze dodatki są na swoim miejscu – i poprawki
- Błąd: po wybraniu celu w „Co chcesz zrobić?” ekran główny pokazuje tylko kafelki celu – kalkulator kosztów pracy nie był w żadnym celu, więc znikał
  (przegląd widoków nie wybierał celu, dlatego tego nie wychwycił).
- Dostawca/usługodawca: nowy cel „Usługi pracochłonne: sprzątanie, ochrona, catering, odpady, przewozy” – kroki w menu: szukaj przetargów usług
  (wyszukiwarka od razu pokazuje tylko 9 zestawów tych usług), kalkulator kosztów pracy, moje oferty, wygrane i przegrane, umowy w realizacji.
- Kalkulator: przycisk w menu; w celach zamawiającego „Przygotuj zamówienie” (szacowanie wartości) i „Sprawdź złożone oferty” (rażąco niska cena);
  w sekcji firmowej celów wykonawcy i pozostałych celów dostawcy.
- Panel pobierania ogłoszeń (Konta i aktywność): opis źródeł uzupełniony o TED.
- Sprawdzone na miejscu (z wybranym celem): Leady, Odwołania, Księgowość (kafelki i menu), pasek klientów biura rachunkowego, pola marki w Ustawieniach,
  zestawy branż (10/10), karta pogody budowy (stacje telemetryczne, historia), karta wspólnot na ekranie startowym.

---

## Wersja „2026-12-07 wspolnoty-deweloperzy”

Poprzednia wersja: „2026-12-06 przeglad-modulow”.

### Wspólnoty, spółdzielnie, deweloperzy – osobna ścieżka
- Sprostowanie: w 2026-12-05 dodano tylko protokół wyboru do kompletu zamawiającego prywatnego; opcja była ukryta w kreatorze zamawiającego.
- Teraz: karta na ekranie startowym „Dla wspólnot, spółdzielni i deweloperów” (zamawiający prywatny, bez Pzp) – własny nagłówek i kafelki:
  „Nowe zapytanie ofertowe (bez Pzp)”, „Moje zapytania i inwestycje”, „Porównanie ofert”; tryb prywatny w kreatorze zaznaczony od razu
  (komplet: zapytanie ofertowe, opis, umowa, formularz, protokół wyboru); wybór karty zapamiętany. Zwykła karta zamawiającego – bez zmian.
### Testy
Przeglądarka: karty startowe, nagłówek, kafelki, kreator (tryb prywatny tylko na nowej ścieżce); pełne przejście przez widoki i regresja – 0 błędów.

---

## Wersja „2026-12-06 przeglad-modulow”

Poprzednia wersja: „2026-12-05 leady-i-nowe-branze”.

### Przegląd całego programu (nowe i stare moduły)
- Analiza statyczna Pythona (pyflakes): brak niezdefiniowanych nazw (33 uwagi kosmetyczne). Przeglądarka: każda funkcja wywoływana z przycisków istnieje (1129 funkcji).
- Przejście przez wszystkie widoki: 8 ścieżek, 128 widoków; wnętrza: 12 projektów wszystkich typów, realizacja, badanie ofert, widoki przetargów w Odwołaniach,
  5 zakładek Księgowości, Leady, Kalkulator; edycja dla urzędu – 14 widoków.
- 490 wywołań API POST z pustymi i niepełnymi danymi: 267 × 200, 223 × 4xx, 0 błędów serwera.
- Zewnętrzne źródła na żywo (12): BZP, TED, e-Zamówienia, Baza Konkurencyjności, IMGW (synop, telemetria, opad dobowy), Open-Meteo, KRS, biała lista VAT, KSeF, GUGiK – działają.

### Naprawione
- Realizacja: niepełny plik realizacji (np. ze starszej wersji) wywracał widok (brak listy faktur) – brakujące pola uzupełniane przy odczycie.
- Odwołania: rekord bez numeru wywracał listę – numer i katalog uzupełniane z klucza przy odczycie.
- Edycja dla urzędu: ekran główny pytał o alerty przetargowe niedostępne w tej edycji (404 w konsoli) – zapytanie tylko w pełnej edycji; /api/ja podaje edycję.

---

## Wersja „2026-12-05 leady-i-nowe-branze”

Poprzednia wersja: „2026-12-04 uslugi-pracochlonne”.

### Leady z przetargów (gwarancje i ubezpieczenia; podwykonawcy i dostawcy)
- Nowy moduł (leady.py, uprawnienie „Leady z przetargów”, domyślnie brak; kafelek i menu; blokada w edycji urzędu).
- Pamięć ogłoszeń: z pełnej treści BZP przy zapisie – wymóg wadium i jego kwota (sekcja 6.4, części sumowane), wymóg zabezpieczenia należytego wykonania (6.5).
  Sprawdzone na żywo: 123 z 474 ogłoszeń dnia z wadium (119 z kwotą), 149 z zabezpieczeniem.
- „Gwarancje wadialne”: otwarte przetargi z wadium, od największego. „Zwycięzcy”: wybrani wykonawcy z modułu Odwołań – firma, NIP, KRS, adres, e-mail,
  telefon, www, cena, liczba ofert, szacunek zabezpieczenia 5% (art. 450 Pzp). Filtry (województwo, rodzaj, słowa, kwota), eksport CSV.
### Nowe branże i grupy
- Medycyna: zestawy dostawcy – leki (336), sprzęt i wyroby medyczne (331, 3319), odczynniki i diagnostyka (33696, 3312), opatrunki (3314).
- Wspólnoty, spółdzielnie, deweloperzy: komplet zamawiającego prywatnego z protokołem wyboru oferty.
- Biura rachunkowe: pasek „Biuro rachunkowe – księgi klienta” w Księgowości (administrator, konta z udostępnioną Księgowością; osobne księgi klientów).
- Resellerzy: „Nazwa programu” i „Kolor wiodący” (tytuł, nagłówek, strona logowania, kolor).
### Bezpieczeństwo
- Ustawienia wspólne programu (klucz API, modele, marka) zapisuje tylko administrator programu (wcześniej konta innych firm mogły je zmienić).
### Testy
Leady (wadium z pamięci, filtry, CSV, zwycięzcy z kontaktami, brak dostępu domyślnie), marka (API, logowanie, walidacja koloru), biuro rachunkowe
(osobne księgi klienta), komplet prywatny; przeglądarka – 0 błędów; regresja obu edycji bez zmian.

---

## Wersja „2026-12-04 uslugi-pracochlonne”

Poprzednia wersja: „2026-12-03 ted-ogloszenia-ue”.

### Usługi pracochłonne (etap 1 nowych branż)
- Kalkulator kosztów pracy (kafelek u wykonawcy, dostawcy i zamawiającego): umowa o pracę, parametry 2026 – płaca minimalna 4806 zł, składki
  pracodawcy (emerytalna 9,76%, rentowa 6,5%, wypadkowa – edytowalna, FP 2,45%, FGŚP 0,1%, PPK 1,5% opcjonalnie), dodatek nocny 20% stawki godzinowej
  z minimalnego wynagrodzenia (art. 151^8 § 1 KP); zastępstwa urlopowe, absencje, odzież/BHP; materiały, koszty ogólne, zysk, VAT.
- Porównanie z ceną oferty: % pokrycia minimalnych kosztów pracy i ocena (poniżej 100% – podstawa do wezwania, art. 224 ust. 1 i ust. 3 pkt 4 Pzp).
- Wyliczenie w Wordzie (do wyjaśnień ceny wykonawcy albo szacowania wartości przez zamawiającego).
- Wyszukiwarka dostawcy – nowe zestawy branż ze słowami i CPV: ochrona osób i mienia (7971), catering i żywienie zbiorowe (5552, 5532, 5551),
  dowóz uczniów i przewozy (6013, 6011, 6014), komunikacja zastępcza PKP (6017, 6014), utrzymanie zieleni (7731, 7734), zimowe utrzymanie dróg (9062, 9063).

### Testy
Wyliczenie sprawdzone ręcznie (dodatek nocny 288,36 zł, składki 20,48%); API, ostrzeżenie poniżej płacy minimalnej, PPK, Word, ochrona ścieżki pliku;
przeglądarka (trzy ścieżki, telefon) – 0 błędów; regresja bez zmian.

---

## Wersja „2026-12-03 ted-ogloszenia-ue”

Poprzednia wersja: „2026-12-02 pogoda-uzupelnianie-luk”.

### Nowe źródło: TED (Dziennik Urzędowy UE) – m.in. przetargi PKP
- Dotąd program nie pobierał TED, więc pomijał wszystkie polskie przetargi powyżej progów unijnych (nie ma ich w BZP) – w tym zamówienia
  sektorowe PKP PLK, PKP Intercity, POLREGIO (ok. 3 ogłoszenia PKP dziennie; łącznie ok. 300 polskich ogłoszeń dziennie).
- Nowy moduł ted.py: publiczne API TED v3 (bez klucza), ogłoszenia o zamówieniu (cn-standard, cn-social, cn-desg), stronicowanie po 250.
- Format jak BZP: numer „TED …”, polski tytuł postępowania, zamawiający, rodzaj (roboty/dostawy/usługi), CPV, termin ofert, link do TED i PDF,
  w treści opis, adresy dokumentów/platformy, NIP zamawiającego, kody NUTS.
- Województwo z miejsca realizacji (NUTS); przy kilku – zapamiętane wszystkie, główne poza siedzibą zamawiającego; filtry województw
  (wyszukiwarka, zapisane przetargi, Odwołania) sprawdzają całą listę.
- Nocne pobieranie: po BZP – TED od ostatniego pobranego dnia (pierwszy raz: 21 dni wstecz).
- Odwołania od przetargów: dla ogłoszeń z TED (i postępowań od progów UE wg e-Zamówień) termin 10 dni (art. 515 ust. 1 pkt 1).
- Ograniczenie: mniejsze zamówienia sektorowe PKP prowadzone wyłącznie na platformach spółek (platformazakupowa.plk-sa.pl – aplikacja JavaScript,
  skmzamowienia.skm.pkp.pl, eb2b) – osobny etap.

### Testy
Na żywo: TED 22.10 – 315 ogłoszeń (155 dostaw, 139 usług, 21 robót), 4 PKP; wyszukiwanie: małopolskie + „teletechnik” → PKP PLK (ZLK Kraków),
cała Polska + „czystości” → PKP, promień 60 km od Świdnicy – 6 dostaw z TED; filtr wielu województw. Regresja bez zmian.

---

## Wersja „2026-12-02 pogoda-uzupelnianie-luk”

Poprzednia wersja: „2026-12-01 pogoda-historia-pomiarow”.

### Uzupełnianie luk w pomiarach (także po uśpieniu serwera)
- Codziennie od 9:00: oficjalna dobowa suma opadu IMGW-PIB (hydro-back.imgw.pl, parametr OPAD_SUM_DOB, doba 06–06 UTC) z najbliższej stacji
  opadowej budowy – przypisana do dnia, w którym doba się zaczyna (obejmuje godziny pracy tego dnia), z opisem okresu.
- Codziennie od 10:00 (aż do publikacji): miesięczne archiwum 10-minutowe IMGW (danepubliczne.imgw.pl/datastore … Meteo_RRRR-MM.zip, ok. 40 MB,
  publikowane po zakończeniu miesiąca) – pobierane raz dla wszystkich budów, wybór najbliższej stacji z danymi dla każdego parametru, dni miesiąca
  zastępowane kompletem (oznaczenie „archiwum IMGW-PIB (komplet 10-min)”); plik usuwany po przetworzeniu.
- Dzień z lukami w odczytach 10-min i opadem dobowym IMGW ponad próg – uwaga do sprawdzenia (bez automatycznego uznania dnia za niekorzystny).
- Weryfikacja na prawdziwym archiwum wrześniowym (Świdnica – Pszenno): suma 10-min w dobie 06–06 UTC = oficjalny opad dobowy w 27/27 dniach
  (czas w archiwum: UTC; data opadu dobowego IMGW = dzień końca doby).

### Testy
Na żywo: opad dobowy 25.10 (2,6 mm), archiwum wrześniowe (30 dni, 142 odczyty/dobę), usunięcie pliku, analiza dnia z archiwum, uwaga przy lukach;
regresja bez zmian.

---

## Wersja „2026-12-01 pogoda-historia-pomiarow”

Poprzednia wersja: „2026-11-30 pogoda-stacje-telemetryczne”.

### Historia pomiarów z najbliższych stacji telemetrycznych IMGW-PIB
- Zapis co 10 minut (harmonogram; jedno pobranie danych IMGW dla wszystkich budów w realizacji z monitoringiem pogody) do realizacja/meteo_imgw.json.
- Czas pomiarów IMGW traktowany jako UTC (sprawdzone na żywo: opóźnienie ok. 25 min względem UTC) i przeliczany na czas polski – przypisanie do dnia
  i do godzin pracy; kontrola świeżości (6 h) liczona w UTC.
- Agregaty dzienne: opad – suma kolejnych sum 10-minutowych (każdy odczyt raz), całodobowo i w godzinach pracy; temperatura powietrza i gruntu – min/max
  (także w godzinach pracy); wiatr średni i maksymalny, porywy – maksimum; wilgotność – średnia; kompletność = odczyty opadu / 144.
- Ocena dnia: pomiar przekraczający kryteria robót (temperatura, opad, wiatr) dodaje przyczynę „pomiar IMGW-PIB … (stacja)” i oznacza dzień
  „potwierdzone pomiarem” – w tabeli dni i w piśmie o niekorzystnych warunkach.
- Karta pogody: kolumna IMGW z dobowym podsumowaniem i kompletnością; informacja, od kiedy jest historia.

### Testy
Zapis i deduplikacja odczytów, suma opadu, min/max, UTC → czas polski (zima i lato), kryteria i potwierdzenie, analiza dnia; na żywo z API IMGW
(Świdnica – Pszenno): zapis 7 pomiarów, ponowny bez nowych odczytów – 0. Regresja bez zmian.

---

## Wersja „2026-11-30 pogoda-stacje-telemetryczne”

Poprzednia wersja: „2026-11-29 odwolania-oferenci”.

### Pogoda budowy – najbliższe stacje IMGW-PIB z gęstej sieci telemetrycznej
- Dotąd: tylko sieć synoptyczna (62 stacje) – najbliższa stacja zwykle kilkadziesiąt km od budowy.
- Teraz dodatkowo sieć telemetryczna IMGW-PIB (danepubliczne.imgw.pl/api/data/meteo, ok. 790 stacji: opad ~700, temperatura i wiatr ~315):
  najbliższa stacja osobno dla każdego pomiaru (opad, temperatura powietrza i gruntu, wiatr średni i maksymalny, poryw, wilgotność),
  tylko pomiary nie starsze niż 6 godzin, do 80 km.
- Karta pogody budowy: tabela pomiar – stacja – odległość – wartość – czas. Pismo o niekorzystnych warunkach: stacje telemetryczne pogrupowane
  (stacja, odległość, mierzone parametry) obok stacji synoptycznej.
- Poprawka: „ok, 39,5 km” → „ok. 39,5 km” w opisie stacji synoptycznej w piśmie.
- Sprawdzone na żywo: Świdnica – Pszenno 3,4 km (synop: Wrocław 39,5 km); Kazanów – opad z posterunku Kazanów 0,9 km (synop: Kozienice 32,6 km);
  Czarnia – Myszyniec 9 km (synop: Ostrołęka 35,5 km).
- Historia pomiarów z sieci telemetrycznej (zapis co 10–30 min) – do zrobienia osobno (API podaje tylko bieżące odczyty).

---

## Wersja „2026-11-29 odwolania-oferenci”

Poprzednia wersja: „2026-11-28 odwolania-widok-przetargu”.

### Oferenci z danymi kontaktowymi
- Tabela „Oferenci” w widoku przetargu: wszyscy wykonawcy z informacji z otwarcia, rankingu i odrzuceń (wybrany, miejsca, odrzuceni z podstawą) –
  cena, punkty, NIP, KRS, REGON, adres, status VAT, reprezentacja; liczona zawsze, także gdy brak argumentów za podważeniem.
- Dane kontaktowe: KRS – API Ministerstwa Sprawiedliwości (strona www, e-mail, adres do e-Doręczeń); CEIDG z tokenem – e-mail, telefon, www
  jednoosobowych działalności; strona www firmy (strona główna i /kontakt) – e-maile (najpierw ogólne skrzynki: biuro, kontakt, sekretariat, przetargi)
  i telefony tylko z odnośników tel: albo oznaczone „tel.” (bez przypadkowych liczb). Zapamiętywane 30 dni (limit wykazu VAT: 100 zapytań dziennie).
- Przyciski E-mail, Odwołanie, Badanie przy każdym oferencie poza wybranym.

### Testy
Oferenci (4 – wybrana, miejsce 2, odrzucona, złożona), dane z KRS/CEIDG/strony, pamięć kontaktów, e-mail do oferenta; na żywo: KRS (www, e-Doręczenia),
strony firm (e-mail sekretariatu, bez fałszywych telefonów); przeglądarka – 0 błędów; regresja bez zmian.

---

## Wersja „2026-11-28 odwolania-widok-przetargu”

Poprzednia wersja: „2026-11-27 odwolania-platformy”.

### Błąd: po kliknięciu przetargu „nic się nie dzieje”
Przyczyna: szczegóły były dodatkowym wierszem tabeli, a sortowanie tabeli (np. „Termin odwołania ▲”) przestawiało go na koniec listy – pod inne przetargi.

### Poprawka – widok przetargu
- Kliknięcie w przetarg otwiera osobny widok: dane postępowania, ocena z argumentami, firmy z dalszych miejsc, lista wszystkich dokumentów z linkami
  (pobrane rozstrzygnięcia i pozostałe pliki), przyciski: Lista przetargów, Analizuj ponownie, Sprawdź nowe dokumenty, Ogłoszenie, Ukryj, wniosek, notatka, e-mail, odwołanie, badanie.
- „Analizuj ponownie”: wymuszony ponowny odczyt AI dokumentów rozstrzygnięcia i przeliczenie oceny – także dla postępowań ze statusem końcowym.
- Rodzaje dokumentów opisane po polsku.

### Testy
Test wymuszonej analizy + przeglądarka (sortowanie tabeli, otwarcie widoku, powrót do listy) – 0 błędów; regresja bez zmian.

---

## Wersja „2026-11-27 odwolania-platformy”

Poprzednia wersja: „2026-11-26 ksiegowosc-28i-scalona”.

### Błąd: brak rozstrzygniętych przetargów (wszystkie „czekają na rozstrzygnięcie”)
Przyczyna (sprawdzone na żywo na przetargach z Dolnego Śląska): każde ogłoszenie BZP ma identyfikator e-Zamówień, także gdy postępowanie jest
prowadzone na innej platformie – wtedy e-Zamówienia nie mają dokumentów (HTTP 400), a program nie sprawdzał platformy zamawiającego z ogłoszenia.
Dodatkowo: ten sam plik na platformazakupowa.pl podlinkowany dwa razy (nazwa techniczna + opis) – opis był pomijany; platformy bez ciasteczek przekierowywały w kółko.

### Poprawki
- Stan postępowania z publicznego API e-Zamówień (Search/GetTender): etap (składanie ofert, badanie i ocena ofert, umowa zawarta, unieważnione),
  czy prowadzone na e-Zamówieniach, kwota przeznaczona (gdy opublikowana), województwo; unieważnione, z zawartą umową i poniżej progu kończą obserwację
  (uwaga: przy umowie zawartej API wpisuje cancellationDate – to data zamknięcia, nie unieważnienia).
- Dokumenty: z e-Zamówień tylko dla postępowań tam prowadzonych (tolerancja dziur w numeracji – 6), inaczej ze strony postępowania na platformie
  zamawiającego z ogłoszenia (bez BIP), z ciasteczkami; łączenie odnośników do tego samego pliku – zostaje opisowa nazwa.
- Adres z ogłoszenia prowadzący tylko do profilu zamawiającego – czytelna informacja w szczegółach i prośba o link do postępowania.
- Szczegóły po kliknięciu w wiersz: przedmiot, zamawiający, ogłoszenie i rodzaj, termin ofert, etap, platforma (link), kwota, dokumenty, status, ostatnie sprawdzenie;
  panel dopasowany do szerokości telefonu.
- Postępowania dopisane wcześniej: adresy platform uzupełniane z ogłoszeń przy najbliższym sprawdzeniu.

### Testy
Na żywo, 30 przetargów z Dolnego Śląska: 5 z dokumentami rozstrzygnięcia (e-Zamówienia i platformazakupowa.pl), 7 umowa zawarta, 2 unieważnione, 2 poniżej progu.
Testy modułu i regresja obu edycji – 0 błędów.

---

## Wersja „2026-11-26 ksiegowosc-28i-scalona”

Poprzednia wersja: „2026-11-25 odwolania-wyszukiwarka”.

### Scalenie dwóch odgałęzień programu
Od wersji 2026-10-28b program rozwijał się w dwóch rozmowach: 28c–28i (Księgowość) i 29.10–25.11 (pozostałe moduły). Wdrożenie
pakietów z drugiego odgałęzienia nadpisało Księgowość z 28i. Ta wersja przywraca Księgowość z 28i i zachowuje wszystko z drugiego odgałęzienia.

### Księgowość – moduł z 28i (pliki od użytkownika: ksiegowosc.py, ksiegowosc_web.py, ksiegowosc.js)
- Czyta i zapisuje dane w katalogu konta: ksiegowosc/dane.json (u administratora – dane z serwera, nietknięte).
- Rozliczenie miesiąca (KPiR, ZUS ze zdrowotną, PIT, VAT, przelewy), dokumenty (KSeF z limitami, XML, PDF/zdjęcia z AI, ręczne, duplikaty, nauka),
  środki trwałe, stan początkowy, profil z pojazdami, token KSeF zaszyfrowany, pobieranie z KSeF co tydzień, paczka do urzędu (JPK_V7M, Word, Excel).
- Odtworzone podłączenia: ma_ksiegowosc (administrator zawsze, inne konta po udostępnieniu), przełącznik „Księgowość – dostęp” w Kontach i aktywności
  (/api/uzytkownicy/ksiegowosc), informacja w /api/ja i /api/konta, widok #ksieg, kafelek i menu, blokada /api/ksieg w edycji dla urzędu.
- Usunięte: tymczasowa Księgowość z drugiego odgałęzienia (trasy /api/ks/*, ksef.py, ksiegowosc_parametry.py, odtwarzanie z XML, moduł „Księgowość” w rolach).
  Pliki pozostawione przez nią na serwerze (dokumenty.json, migracja.json, kierunek_ksef.json, kopie/) są ignorowane – można je usunąć.
- Diagnostyka danych (/api/admin/dane) liczy dokumenty z dane.json.

### Testy
20 testów Księgowości (dostęp, osobne dane kont, XML sprzedaż/koszt, rozliczenie: przychód 10 000, koszty 1 000, VAT 2 070, JPK, paczka, token, diagnostyka,
harmonogram) + przeglądarka (wszystkie zakładki, kolumna w Kontach) – 0 błędów; regresja: 11 zestawów, 93 strony/API bez błędów 500, edycja dla urzędu bez zmian.

---

## Wersja „2026-11-25 odwolania-wyszukiwarka”

Poprzednia wersja: „2026-11-24 odwolania-dokumenty”.

### Odwołania od przetargów – własna wyszukiwarka
- Region niezależny od wyszukiwarki przetargów: jak w wyszukiwarce przetargów / wybrane województwa / cała Polska (wcześniej tylko obszar z wyszukiwarki, np. Świdnica + 10 km).
- Rodzaj zamówienia: roboty budowlane, dostawy, usługi (domyślnie wszystkie) – rozpoznawany z BZP (orderType); słowa w przedmiocie; okres (1–90 dni po terminie ofert); próg wartości.
- „Szukaj” zapisuje filtry i od razu wyszukuje; zmiana filtrów zawęża listę (poza filtrami – ukryte, nie usunięte, z licznikiem).
- Na liście: rodzaj zamówienia i województwo; przy całej Polsce sprawdzanie rotacyjne (najpierw sprawdzane najdawniej, do 400 na raz).

### Testy
8 testów wyszukiwarki (region z przetargów, cała Polska, rodzaje Works/Supplies/Services, filtr rodzaju, województwo, słowa, okres, walidacja) + widok na telefonie – 0 błędów; regresja bez zmian.

---

## Wersja „2026-11-24 odwolania-dokumenty”

Poprzednia wersja: „2026-11-23 ksef-pobieranie”.

### Odwołania od przetargów – etapy 2 i 3
- Twoje dane (nadawca wniosków i wiadomości) w ustawieniach modułu – brakujące na żółto.
- Wniosek o udostępnienie protokołu i oferty wybranego wykonawcy (Word) – art. 74 ust. 1 i ust. 2 pkt 1 Pzp (sprawdzone: oferty udostępnia się niezwłocznie po otwarciu, najpóźniej w 3 dni); wnioskodawca: Ty.
- Notatka o możliwości podważenia (Word, bez AI): argumenty z wyliczeniami i podstawą, termin (art. 515), firmy, kolejne kroki.
- Projekt e-maila do każdej firmy: powód, termin, źródło danych, klauzula RODO (art. 14), rezygnacja; adres firmy wpisywany ręcznie i zapamiętywany; Kopiuj / Otwórz w programie pocztowym – program nie wysyła sam.
- Projekt odwołania do KIO (Word, AI – generator z modułu prawnika) dla wybranej firmy; nowy tryb „Postępowanie krajowe (BZP)” – termin 5 dni.
- Badanie pogłębione: przycisk zakłada badanie ofert (perspektywa wykonawcy, klient = firma) z dokumentami rozstrzygnięcia – do wgrania oferta wybranego wykonawcy.
- Uprawnienia: podgląd modułu widzi listę, dokumenty tworzy tylko edycja.

### Testy
23 testy modułu (12 z etapu 1 + 11 nowych: nadawca, wniosek, notatka, e-mail z RODO, zapis i walidacja adresu, odwołanie z terminem 5 dni, badanie, podgląd bez tworzenia) + przeglądarka – 0 błędów; regresja obu edycji bez zmian.

Pliki: odwolania_przetargi.py (dokumenty), serwer.py (trasy /api/odw/dokument, /email, /badanie, ustawienia), prawnik.py (tryb krajowy), app.js, instrukcja.

---

## Wersja „2026-11-23 ksef-pobieranie”

Poprzednia wersja: „2026-11-22 odwolania-etap1” (zawiera moduł Odwołania od przetargów – etap 1).

### KSeF – pobieranie faktur (Księgowość, etap 1b)
- Nowy moduł ksef.py według specyfikacji MF (OpenAPI api.ksef.mf.gov.pl/docs/v2 i github.com/CIRFMF/ksef-docs, sprawdzone 25.10.2026):
  challenge → szyfrowanie „token|timestampMs” kluczem publicznym KSeF (RSA-OAEP SHA-256) → /auth/ksef-token (kontekst NIP) → status (100/200)
  → redeem; metadane faktur (PermanentStorage, rosnąco, strony po 250, hasMore/isTruncated) i XML faktury.
- Księgowość → Dokumenty → karta „KSeF”: zapis tokena z Aplikacji Podatnika (zaszyfrowany kluczem z KSEF_KLUCZ albo SECRET_KEY; nie wraca do przeglądarki),
  wybór środowiska, „Pobierz z KSeF” za dowolny okres (domyślnie od 1.01.2026), usunięcie tokena; automatycznie codziennie o 6:00.
- Sprzedaż (Subject1) i koszty (Subject2) rozdzielane według KSeF; dane z metadanych + XML (stawki, opis, termin płatności); kategoria z Twoich reguł; bez duplikatów; status „do zatwierdzenia”.
- Jednorazowa poprawka kierunku faktur odtworzonych z XML: numer KSeF zaczyna się od NIP sprzedawcy (Twój NIP → sprzedaż); tylko niezatwierdzone, z wpisem w dzienniku.
- Nowa zależność: cryptography (requirements.txt).

### Testy
Na żywo (produkcja i środowisko testowe KSeF): klucz publiczny RSA 2048, challenge, szyfrowanie. Symulator KSeF: pełne logowanie (odszyfrowanie tokena kluczem prywatnym),
status w toku → sukces, sprzedaż i koszty, stronicowanie, XML, brak duplikatów, poprawka kierunku, ochrona tokena – 11 testów, 0 błędów; regresja obu edycji bez zmian.
Pełne pobieranie z prawdziwego KSeF – do sprawdzenia Twoim tokenem po wdrożeniu.

Pliki: nowy ksef.py; ksiegowosc.py (dokument_z_ksef, popraw_kierunek_ksef), serwer.py (trasy /api/ks/ksef/*, zadanie, harmonogram, wersja), ksiegowosc.js, requirements.txt, instrukcja.

---

## Wersja „2026-11-22 odwolania-etap1”

Poprzednia wersja: „2026-11-21 ksiegowosc-odtworzenie”.

### Nowy moduł: Odwołania od przetargów (etap 1)
- Kafelek na ekranie głównym i przycisk w menu; nowe uprawnienie w rolach „Odwołania od przetargów” (domyślnie brak – nadaje administrator); dane modułu wspólne w /data/odwolania_przetargow.
- Obserwowane: ogłoszenia BZP w regionie (ten sam filtr co wyszukiwanie), 0–45 dni po terminie ofert, z adresem e-Zamówień albo platformy; bez BIP i bez Bazy Konkurencyjności.
- Sprawdzanie o 7:00 i 14:00 (i przyciskiem): nowe dokumenty po nazwach (e-Zamówienia – tylko nagłówki, bez pobierania SWZ); pliki o nieopisowej nazwie rozpoznawane po nagłówku treści (ogłoszenie i SWZ wykluczone); pobierane tylko: informacja o kwocie, z otwarcia, o wyborze, unieważnienie; odczyt AI (także części zamówienia).
- Ocena bez AI: rażąco niska cena (art. 224 ust. 2 pkt 1; silny przy braku wezwania), cena poniżej kwoty przeznaczonej (pomocniczo), punkty za cenę i sumy punktów, odrzucone tańsze oferty, status VAT (biała lista), wybór po 30 dniach od terminu ofert.
- Termin odwołania: 5 dni od informacji o wyborze (BZP – poniżej progów), sobota/niedziela → dzień roboczy.
- Firmy: 2. miejsce – priorytet; odrzucone z interesem; dane z białej listy VAT. Próg wartości (domyślnie 1 mln zł) w module; dodawanie postępowania z linku (BIP odrzucany).
- Edycja dla urzędu: moduł niedostępny.

### Testy
12 testów modułu (obserwowane, BK pominięta, ocena silna, punktacja, odrzucona tańsza, firmy, termin w dniu roboczym, próg 1 mln, jedna oferta, uprawnienia, BIP) + rozpoznanie po nagłówku + na żywo: lista dokumentów z e-Zamówień + przeglądarka – 0 błędów; regresja obu edycji bez zmian (90 stron / API).

Następne etapy: wniosek o udostępnienie oferty i protokołu, projekt e-maila do firmy (bez automatycznej wysyłki), projekt odwołania; potem scalenie Księgowości z plików od użytkownika.

---

## Wersja „2026-11-21 ksiegowosc-odtworzenie”

Poprzednia wersja: „2026-11-20 ksiegowosc-dostep-kopie”.

### Przyczyna „zniknięcia” danych Księgowości
Diagnostyka na serwerze: w /data/ksiegowosc są dane.json (38 KB, 22.10), profil (21 pól) i 37 faktur XML z KSeF w pliki/ (21.10).
Dane zapisała wcześniejsza wersja modułu (plik dane.json, pliki nazwane numerem KSeF); obecna wersja czyta dokumenty.json – stąd pusta lista.
Nic nie zostało usunięte.

### Odtworzenie (jednorazowe, automatyczne, nic nie usuwa)
- Przy pierwszym wejściu do Księgowości, gdy brak dokumenty.json, a są stare dane: odczyt dane.json (listy dokumentów w dowolnej budowie;
  numer, KSeF, daty, strony, kwoty, kategoria, odliczenie VAT, status zatwierdzenia; pełny oryginalny rekord zachowany w „zrodlo_migracji”)
  + faktury XML z KSeF odczytane wprost ze struktury FA (bez AI): numer, daty, sprzedawca, nabywca, kwoty według stawek, numer KSeF z nazwy pliku.
- Bez duplikatów (numer KSeF; numer faktury + NIP sprzedawcy); dokumenty bez potwierdzonej kategorii – „do zatwierdzenia”.
- Raport odtworzenia na ekranie Księgowości i w diagnostyce (/api/admin/dane – także budowa dane.json, bez wartości).
- dane.json i pliki XML pozostają nietknięte.

### Testy
10 testów odtworzenia (FA(3) z KSeF, dane.json w nieznanej budowie, przeniesienie kategorii i zatwierdzenia, kwoty z XML, oryginał zachowany,
pliki nietknięte, jednorazowość, diagnostyka) – 0 błędów; regresja bez zmian.

Pliki: ksiegowosc.py (czytaj_fa_xml, odtworz_dokumenty), serwer.py (ks_stan, diagnostyka, wersja), ksiegowosc.js (komunikat odtworzenia).

---

## Wersja „2026-11-20 ksiegowosc-dostep-kopie”

Poprzednia wersja: „2026-11-19 diagnostyka-danych”.

### Księgowość – udostępnianie innym użytkownikom
- Nowy moduł w rolach: „Księgowość (firmy administratora)” – brak / podgląd / edycja; domyślnie wszystkie role poza administratorem: brak.
- Uprawnieni pracują na księgach firmy administratora (wspólne dane); podgląd „jako” nie przełącza ksiąg (wcześniej mógł pokazywać puste księgi innego konta).
- Kafelek i przycisk menu Księgowości widoczne dla osób z uprawnieniem; serwer pilnuje poziomu (podgląd nie zapisuje).

### Bezpieczeństwo danych Księgowości
- Kopia poprzedniej wersji przy każdym zapisie (30 ostatnich wersji każdego pliku: ksiegowosc/kopie/).
- Koniec cichego nadpisywania: plik nieczytelny → odtworzenie z najnowszej dobrej kopii (uszkodzony zachowany obok); bez kopii – błąd, plik NIE jest nadpisywany pustym stanem.

### Diagnostyka danych (/api/admin/dane) – rozszerzona
- Dla każdego konta: zawartość katalogu Księgowości (pliki, rozmiary, daty), liczba wgranych plików faktur, liczba kopii, liczba i sekcje wypełnionych pól profilu (bez wartości).
- Ślady danych księgowych w innych miejscach dysku (pliki z „ksieg”, „ksef”, „jpk”, „faktur”, pliki .tmp i uszkodzone).

### Uwagi
- W programie nie było pola na dostęp do KSeF – połączenie z KSeF to etap 1b (niezbudowany); token zostaje w Aplikacji Podatnika KSeF.
- Profil domyślny w kodzie zawiera dane podatnika (NIP, US, rachunek ZUS, samochód) – ekran profilu pokazuje je zawsze; diagnostyka pokazuje, co zostało zapisane.

### Testy
11 testów (dostęp domyślny, nadanie edycji i podglądu, wspólne księgi, kopie, odtworzenie z kopii, brak nadpisania bez kopii, „jako”, diagnostyka) – 0 błędów; regresja bez zmian (89 stron / API bez błędów 500).

---

## Wersja „2026-11-19 diagnostyka-danych”

Poprzednia wersja: „2026-11-18 link-nazwy-zip”.

- Nowy adres dla administratora: /api/admin/dane – tylko odczyt, niczego nie zmienia ani nie usuwa. Pokazuje:
  czy katalog danych jest trwałym dyskiem, zajętość, najstarszy plik (wykrycie wyczyszczenia danych przy wdrożeniu),
  zalogowane konto, konto, na którym pracujesz, podgląd „jako”, a dla każdego konta: liczbę projektów, dokumentów
  w Księgowości, profil podatnika i datę ostatniej zmiany.
- Przyczyna zgłoszenia „program zgubił dane”: dane są osobne dla każdego konta (administrator z ustawień – katalog
  główny, inne konta – /data/konta/<login>); podgląd „jako” przełącza dane na inne konto; bez trwałego dysku Render
  czyści dane przy wdrożeniu. Diagnostyka wskazuje, który przypadek zachodzi.

Pliki: serwer.py.

---

## Wersja „2026-11-18 link-nazwy-zip”

Poprzednia wersja: „2026-11-17 link-bez-starych”.

- Pobieranie z linku: pliki z archiwów ZIP z uciętą nazwą bez kropki przed rozszerzeniem (np. „…zamó__docx” w ZIP gminy Cielądz)
  dostają właściwe rozszerzenie i są odczytywane; pozostałe pliki – sprawdzenie rozszerzenia po zawartości (jak przy pobieraniu z ogłoszenia).
- Sprawdzone na żywo: przetarg Or.SO.2714.11.2026 (BIP Cielądz) – do oceny 16 plików (ogłoszenie, SWZ, 14 załączników),
  pominięte 2 dokumenty przebiegu postępowania; załącznik nr 5 odczytany.

Pliki: serwer.py (praca_pobierz_z_linku, wersja).

---

## Wersja „2026-11-17 link-bez-starych”

Poprzednia wersja: „2026-11-16 bip-pliki”.

### Problem: do oceny prawnika trafia 19 plików, w tym dokumenty spoza dokumentacji; ponowne pobranie dokłada stare pliki
Przyczyna (sprawdzone na żywo, BIP Cielądz – catering): strona przetargu ma kolejne „zdarzenia” postępowania – ogłoszenie
(SWZ, ogłoszenie, ZIP z 13 załącznikami) oraz późniejsze: informację o kwocie przeznaczonej na zamówienie i informację z otwarcia
ofert. Program brał wszystko jako dokumentację do oceny; ponowne pobranie z linku dokładało pliki do istniejących.

### Poprawka
- Dokumenty przebiegu postępowania (informacja o kwocie, z otwarcia ofert, o wyborze / zawiadomienie o wyborze, unieważnienie,
  wynik, protokół z otwarcia, odrzucenie ofert, zawarcie umowy) są pobierane, ale automatycznie oznaczone jako „pominięte” –
  nie trafiają do oceny dokumentacji; widać je w tabeli i można je włączyć. Dziennik podaje, które pominięto.
  Dotyczy pobierania z linku i „Pobierz i dodaj wszystkie dokumenty z ogłoszenia”.
- Ponowne pobranie z linku ZASTĘPUJE pliki z poprzedniego pobrania z linku (lista zapamiętana w sprawie); pliki wgrane ręcznie
  i dokumenty przygotowane w programie zostają.

### Testy
Na żywo (BIP Cielądz): catering – 19 plików, do oceny 17 (informacja o kwocie i z otwarcia – pominięte); ponowne pobranie z linku
do innego przetargu – pliki poprzedniego usunięte, plik wgrany ręcznie zachowany, zawiadomienie o wyborze pominięte.
Regresja obu edycji bez zmian (11 zestawów testów, 88 stron / API bez błędów 500).
Uwaga: na stronie przetargu „agregaty” gmina opisała informację z otwarcia ofert numerem z przetargu „catering” (Or.SO.2714.11) –
to opis po stronie gminy, nie pomyłka programu.

### Pliki
serwer.py (RE_PRZEBIEG, oznacz_przebieg, praca_pobierz_z_linku, praca_pobierz_dok, wersja), instrukcja.html / .pdf.

---

## Wersja „2026-11-16 bip-pliki”

Poprzednia wersja: „2026-11-15 bip-do-bzp”.

### Błąd: „Na stronie nie ma plików do pobrania bez logowania” dla stron BIP gmin (np. bip.cieladz.pl)
Przyczyna (sprawdzone na żywo): popularny system BIP gmin podaje pliki pod adresami bez rozszerzenia
(„redir,przetargi?plik=3438”), a typ pliku jest tylko w opisie linku („SWZ Or.SO.2714.10.2026 (PDF)”). Program rozpoznawał
pliki tylko po rozszerzeniu w adresie albo słowach „download / pobierz” – na stronie przetargu nie rozpoznał żadnego z 19 plików.

### Poprawka
- Pliki rozpoznawane także po adresach „?plik=…”, „plik,123”, „/plik/…”, „?file=…”, „?id_pliku=…” oraz po typie w opisie linku
  („(PDF)”, „(DOCX)”, „(ZIP)”…); nazwa pliku z opisu linku (także gdy serwer podaje nazwę z samego numeru).
  Sprawdzone na żywo: strona przetargu w BIP Cielądz – 19 z 19 plików (SWZ, ogłoszenie, załączniki, zmiany SWZ, odpowiedzi
  na pytania, ZIP, informacja o kwocie, z otwarcia ofert, o wyborze) z czytelnymi nazwami.
- Link do LISTY postępowań: komunikat „To jest lista postępowań…” z przykładami pozycji zamiast „brak plików bez logowania”.
- Projekt z wyszukiwarki z linkiem do ogólnej listy BIP: gdy przetargu nie ma w BZP / BK, program znajduje na stronie BIP
  odnośnik do tego postępowania po tytule (sprawdzone na żywo: zgodność 100%) i pobiera jego pliki.

### Testy
Na żywo: strona przetargu BIP Cielądz (19 plików), lista → strona przetargu, komunikat dla listy; regresja obu edycji bez zmian
(10 zestawów testów, 88 stron / API bez błędów 500).

### Pliki
bzp.py (RE_POBIERZ, RE_TYP_W_OPISIE, pobierz_z_linku, znajdz_strone_postepowania), serwer.py (praca_pobierz_dok, wersja), instrukcja.html / .pdf.

---

## Wersja „2026-11-15 bip-do-bzp”

Poprzednia wersja: „2026-11-14 oferty-rynkowosc”.

### Błąd: „Nie udało się pobrać dokumentów automatycznie” dla ogłoszeń ze stron BIP (np. bip.cieladz.pl)
Przyczyna (sprawdzone na żywo): link zapisany przy ogłoszeniu z BIP prowadził do OGÓLNEJ listy „Zamówienia publiczne”
gminy, nie do strony tego postępowania; strona „aktualne” tej gminy zawiera tylko plany postępowań (ok. 30 PDF z lat 2018–2026).
„Pobierz i dodaj wszystkie dokumenty” umiało pobierać tylko z BZP / e-Zamówień / BK, więc dla BIP od razu się poddawało.
Proste pobranie plików ze strony BIP byłoby błędem – trafiłyby do projektu plany postępowań zamiast SWZ.

### Poprawka
- Dla ogłoszenia z BIP (bez identyfikatora e-Zamówień / BK) program szuka TEGO SAMEGO postępowania we wspólnej pamięci
  ogłoszeń (BZP z ostatnich 90 dni + aktywne z Bazy Konkurencyjności): wspólne słowo z nazwy zamawiającego / miejscowości
  i co najmniej 50% zgodności słów tytułu; znalezione → dokumenty z e-Zamówień / BK, numer i zgodność w dzienniku,
  powiązanie zapisane w projekcie.
- Gdy nie znajdzie – komunikat wprost: link prowadzi do ogólnej listy zamówień na BIP; wklej link do strony tego postępowania
  albo wgraj pliki ręcznie.
- Pole „wklej link do strony TEGO postępowania” jest teraz także w projektach z wyszukiwarki (krok 1, pod przyciskiem pobierania).

### Testy
6 testów (dopasowanie BIP → BZP tej samej gminy, bez pomyłki z identycznym tytułem innej gminy i z innym przetargiem tej samej
gminy, powiązanie, komunikat przy braku) – 0 błędów; regresja obu edycji bez zmian (88 stron / API bez błędów 500).

### Pliki
serwer.py (znajdz_w_pamieci_ogloszen, praca_pobierz_dok, wersja), app.js (pole linku w kroku 1), instrukcja.html / .pdf.

---

## Wersja „2026-11-14 oferty-rynkowosc”

Poprzednia wersja: „2026-11-13 prawnik-dwie-sciezki”.

Przepisy sprawdzone w źródłach (21.10.2026): art. 224 ust. 2 pkt 1 Pzp (próg 30% – wartość zamówienia z VAT albo średnia cen
ofert niepodlegających odrzuceniu → obowiązkowe wezwanie); art. 515 Pzp (odwołanie: od progów unijnych 10 dni / 15 dni,
poniżej progów 5 dni / 10 dni – informacja elektroniczna / inna); płaca minimalna 2026 – 4806 zł, stawka godzinowa – 31,40 zł.

### Rynkowość cen ofert – nowy wspólny moduł rynkowosc.py (zamawiający i prawnik)
- Cena całkowita bez AI: próg z art. 224 ust. 2 pkt 1 z wyliczeniem (wartość zamówienia z VAT – nowe pole; średnia cen ofert).
- Pozycje oferty (AI odczytuje formularz cenowy / kosztorys ofertowy, modelem do dokumentów) a ceny rynkowe z internetu
  (AI z wyszukiwaniem, ze źródłami): domyślnie pozycje tworzące 80% wartości oferty, opcja „wszystkie”; odchylenie od ceny typowej.
- Roboty: wykrywanie możliwej inżynierii cenowej; usługi: czy cena pokrywa minimalne koszty pracy zadeklarowanego personelu.
- Ocena: rażąco niska – obowiązkowe wezwanie / niska – do wyjaśnienia / rynkowa / zawyżona, z podstawą prawną i zastrzeżeniem
  (ceny ofertowe, nie transakcyjne). Projekt wezwania do wyjaśnień ceny (art. 224) z pozycjami odstającymi – Word.
- U zamawiającego: sekcja „Rynkowość cen ofert” w istniejącym badaniu ofert.

### Dla Prawnika – trzecia ścieżka „Sprawdź oferty w przetargu”
- Kafelek (trzeci, po „Sprawdź dokumentację” i „Sporządź dokumentację”); osobna lista sprawdzeń (nie miesza się z zamawiającym).
- Ten sam przebieg co badanie ofert + karta „Czego dotyczy i dla kogo” (przedmiot, tryb, zamawiający / wykonawca, klient).
- Wynik dla klienta: raport z badania ofert (bez AI – zgodność, ranking, rynkowość, tabela pozycji), opinia prawna,
  dla wykonawcy projekt odwołania do KIO (zarzuty z podstawą, żądania, interes, uzasadnienie, dowody, termin z art. 515
  dobrany do trybu, pola [UZUPEŁNIJ] na żółto, notatka o szansach dla klienta).

### Poprawki przy okazji
- Ranking: próg rażąco niskiej ceny od wartości zamówienia z VAT (wcześniej – od kwoty przeznaczonej na sfinansowanie, co jest
  niezgodne z art. 224 ust. 2 pkt 1) i „o co najmniej 30%” (≤ 70%, wcześniej < 70%); średnia – co najmniej z 2 ofert.
- Protokół, informacja o wyborze i wezwania w badaniu ofert: zamawiający z SWZ, nie z Profilu firmy (zgodnie z zasadą).

### Testy
25 testów (próg 224: 32% / dokładnie 30% / 29%, 80% wartości, odchylenia, inżynieria cenowa, koszty pracy, ranking – wartość
z VAT vs kwota na sfinansowanie, przepływ zamawiającego z rynkowością i wezwaniem, zamawiający nie z profilu, sprawa prawnika,
rozdzielone listy, raport, opinia, odwołanie z terminem 5 dni, odmowa odwołania dla zamawiającego) + przeglądarka – 0 błędów;
regresja obu edycji bez zmian (88 stron / API bez błędów 500).

### Pliki
Nowy: rynkowosc.py. Zmienione: serwer.py, prawnik.py, ocena_ofert.py, app.js, instrukcja.html / .pdf (12.10 – trzy ścieżki).

---

## Wersja „2026-11-13 prawnik-dwie-sciezki”

Poprzednia wersja: „2026-11-12 prawnik-sporzadz”.

### Dla Prawnika – dwie osobne ścieżki (każda w 4 krokach)
**Ścieżka 1 – Sprawdź dokumentację → opinia prawna:** 1. czego dotyczy (dostawy / usługi / roboty, tryb, dla kogo, adresat,
pytania) → 2. dokumentacja do sprawdzenia (pliki albo link; bez opcji „przygotuj”) → 3. sprawdzenie → 4. opinia prawna.

**Ścieżka 2 – Sporządź dokumentację → komplet dokumentów do postępowania:**
1. czego dotyczy zamówienie: przedmiot, tryb, zamawiający (wpisywany – nie z Profilu firmy; na żółto, gdy pusty);
2. co chcesz zamówić: opis w polu tekstowym (zapisywany jako dokument źródłowy) i/lub wgrane ogłoszenie, SWZ, OPZ, własne wzory, link;
3. sprawdzenie z przepisami opisu i wgranych dokumentów (uwagi z podstawą prawną; strona: zamawiający);
4. komplet dokumentów: komplet według trybu; dokumenty dostarczone (rozpoznane po nazwie pliku: SWZ, ogłoszenie, OPZ, umowa,
   formularz, oświadczenia, protokół, uzasadnienie) domyślnie NIE są pisane od nowa; pozostałe przygotowywane na podstawie opisu,
   dokumentów i wzorów, Z UWZGLĘDNIENIEM WYNIKÓW SPRAWDZENIA (bez uwag odrzuconych); „Pobierz komplet (ZIP)” – dokumenty
   dostarczone + przygotowane + „Spis dokumentow.txt” (oznaczenie dostarczony / przygotowany, informacja o sprawdzeniu).
- Nowe trasy: POST /api/projekty/<id>/prawnik/opis, GET /api/projekty/<id>/prawnik/komplet.zip; sprawa ma pole cel_prawnika.
- Rozpoznawanie nazw plików odporne na podkreślniki (np. „SWZ_laptopy.pdf”), bez mylenia opisu z OPZ.

### Testy
13 testów ścieżki „Sporządź” (ścieżki spraw, opis jako źródło, rozpoznanie SWZ, sprawdzenie obejmuje opis, przygotowanie
uwzględnia wyniki sprawdzenia, tryb i zamawiający, ZIP z dostarczoną SWZ i przygotowanymi dokumentami, spis bez roboczego opisu)
+ przeglądarka (dwie ścieżki, różne kroki 1, 2 i 4) – 0 błędów; regresja obu edycji bez zmian (87 stron/API bez błędów 500).

### Pliki
app.js (rysujSprawePrawnika – dwie ścieżki, prawnikOpis, formularz kompletu), serwer.py (cel_prawnika, opis, dostarczone,
uwagi w przygotowaniu, komplet.zip, wersja), instrukcja.html / .pdf (12.10 – przepisany).

---

## Wersja „2026-11-12 prawnik-sporzadz”

Poprzednia wersja: „2026-11-11 prawnik-4-kroki”.

- Pulpit prawnika: dwa kafelki – **Sprawdź dokumentację** (lista spraw; w kroku 2 domyślnie wgrywanie / link) i
  **Sporządź dokumentację** (od razu nowa sprawa; po kroku 1 krok 2 otwiera się na „Przygotuj dokumentację w programie”
  z kompletem według trybu i własnymi wzorami). Obie ścieżki: te same 4 kroki, wspólna lista spraw.
- Sprawa zapamiętuje, z którego kafelka powstała (start_przygotuj) – po ponownym otwarciu właściwa zakładka kroku 2.
- Uprawnienia: widoki prawnika przypisane do modułu „Projekty” (wcześniej dostępne niezależnie od roli).

Testy: przeglądarka (dwa kafelki, nowa sprawa z „Sporządź”, krok 2 na przygotowaniu z kompletem dla przetargu ograniczonego,
sprawa ze „Sprawdź” na wgrywaniu, lista spraw) – bez błędów; regresja obu edycji bez zmian.
Pliki: app.js, serwer.py, instrukcja.html / .pdf.

---

## Wersja „2026-11-11 prawnik-4-kroki”

Poprzednia wersja: „2026-11-10 prawnik-link-bk”.

### Sprawa prawnika przebudowana na 4 kroki (odblokowywane po kolei)
1. **Czego dotyczy sprawa** – Dostawy / Usługi / Roboty budowlane na nieruchomości (duże przyciski, w tej kolejności,
   bez wyboru z góry – zatwierdzenie wymaga wyboru), tryb, dla kogo, adresat opinii, pytania klienta →
   „Zatwierdź i przejdź do dokumentacji”; po zatwierdzeniu podsumowanie i „Zmień”.
2. **Dokumentacja – wgraj albo przygotuj** (w tej samej sprawie):
   - „Mam dokumentację”: przeciąganie plików (także własne wzory do oceny), link do ogłoszenia / postępowania;
   - „Przygotuj dokumentację w programie”: krótki formularz (zamawiający – NIE z Profilu firmy, na żółto, gdy pusty;
     nazwa, znak, wartość, terminy, kryteria, wadium, gwarancja, opis przedmiotu, wymagania), własne wzory,
     komplet dokumentów dobrany do trybu z kroku 1 → dokumenty trafiają do dokumentacji sprawy
     (folder „Przygotowane w programie”) i w kroku 3 przechodzą sprawdzenie.
3. **Sprawdzenie dokumentacji** – jak dotąd (uwagi z podstawą prawną, raport Word, wprowadzanie zmian).
4. **Opinia prawna** – pismo Word.
- Z widoku sprawy usunięte sekcje innych modułów (przegląd projektu, asystent dokumentów, osobna karta ustawień,
  wybór rodzaju zamówienia); w nagłówku tylko „Raport” i „Archiwizuj”.
- Pulpit prawnika: jedna ścieżka „Sprawy” (osobna ścieżka „Sporządź dokumentację” usunięta – jest w kroku 2).
- Nowe trasy: GET /api/projekty/<id>/prawnik/komplet, POST /api/projekty/<id>/prawnik/przygotuj.

### Testy
6 testów serwera (zatwierdzenie kroku 1, komplet dla wolnej ręki, przygotowanie do dokumentacji sprawy, dokument spoza
kompletu odrzucony, tryb z kroku 1 w poleceniu, zamawiający nie z profilu, błąd bez dokumentów) + przejście całej sprawy
w przeglądarce (blokady kroków, wybór przedmiotu, wgranie pliku, formularz „Przygotuj” z kompletem) – 0 błędów;
regresja obu edycji bez zmian.

### Pliki
app.js (rysujSprawePrawnika i funkcje kroków), serwer.py (komplet, przygotowanie, wersja), prawnik.py (kolejność, znacznik
zatwierdzenia), styl.css, instrukcja.html / .pdf (12.10 – przepisany).

---

## Wersja „2026-11-10 prawnik-link-bk”

Poprzednia wersja: „2026-11-09 dla-prawnika-etap2”.

### Sprawa prawnika – bez zbędnych przycisków
- Sprawa prawnika: usunięty przycisk „Przetarg wygrany – do realizacji” (z modułu wykonawcy) – zostają „Raport” i „Archiwizuj”.
- Dokumentacja sporządzona w kreatorze ze ścieżki prawnika (oznaczana przy tworzeniu: dla_prawnika) – bez przycisku
  „Umowa podpisana – przekaż do realizacji umów”. U zamawiającego przycisk bez zmian.

### Link do ogłoszenia – w kroku 1 „Dokumentacja”
- Pole „albo podaj link do ogłoszenia / postępowania” i przycisk „Pobierz dokumenty z linku” są teraz w kroku 1, obok wgrywania
  plików – w każdym projekcie, który nie powstał z wyszukiwarki przetargów (wcześniej pole było schowane w ustawieniach sprawy).
- Nowe: linki do **Bazy Konkurencyjności** (…/ogloszenia/<numer>) – załączniki ogłoszenia przez API BK
  (sprawdzone na żywo: ogłoszenie 251339 – 3 załączniki: Word, Excel).

### Błąd: wyszukiwarka Bazy Konkurencyjności zwracała 0 ogłoszeń
- Przyczyna: serwis BK zmienił API – wyszukiwanie bez filtra statusu zwraca błąd 500 (sprawdzone na żywo); program
  traktował to jako brak wyników, więc w wyszukiwaniu przetargów nie było ogłoszeń z BK.
- Poprawka: domyślny filtr status[]=PUBLISHED (o ile adres w ustawieniach nie podaje własnego statusu).
  Sprawdzone na żywo: 100 ogłoszeń na stronę, poprawnie odczytane (numer, przedmiot, zamawiający, termin, link).

### Testy
Przeglądarka: przyciski w sprawie prawnika i w dokumentacji prawnika, przycisk u zamawiającego, pole linku w kroku 1,
pobranie z linku BK na żywo (3 pliki) – bez błędów; regresja obu edycji bez zmian.

### Pliki
app.js, serwer.py (dla_prawnika, link BK, wersja), bk.py (filtr statusu), instrukcja.html / .pdf.

---

## Wersja „2026-11-09 dla-prawnika-etap2”

Poprzednia wersja: „2026-11-08 dla-prawnika-etap1”.

### 1. Link do postępowania (sprawdzanie dokumentacji)
- W sprawie prawnika: pole „Link do postępowania” i przycisk „Pobierz dokumenty z linku” (trasa /api/projekty/<id>/pobierz-z-linku;
  działa dla każdego projektu).
- Platforma e-Zamówienia / BZP (identyfikator ocds albo ogłoszenia w linku) – ogłoszenie i komplet dokumentów przez API;
  strona BIP lub platforma zakupowa – pliki podlinkowane na stronie (PDF, Word, Excel, ODT, RTF, ZIP, XML…); strona odsyłająca
  do e-Zamówień – pobieranie stamtąd; link wprost do pliku – ten plik. Pobieranie strumieniowe z kontrolą rozmiaru i spójności ZIP.
- Archiwa ZIP rozpakowywane od razu (sprawdzanie czyta pliki, nie archiwa); po pobraniu wcześniejsze sprawdzenie – nieaktualne.
- Czytelne komunikaty: platforma wymaga logowania / ładuje pliki skryptem; **przerwa techniczna e-Zamówień** (rozpoznawana –
  w czasie testów platforma rzeczywiście miała przerwę i odpowiadała HTTP 403 stroną „Przerwa techniczna”).

### 2. Sporządzanie dokumentacji – jawny wybór trybu i komplet według trybu
- Kreator, krok „Wartość i tryb”: wybór trybu (12 trybów i wariantów) albo „automatycznie z wartości”.
- Kontrola wyboru z wartością: tryb podstawowy od progu unijnego – błąd krytyczny; zapytanie poniżej progu przy wartości
  od 170 000 zł – krytyczny; tryby z przesłankami (wolna ręka, negocjacje bez ogłoszenia, dialog, partnerstwo, negocjacje z ogłoszeniem)
  – informacja o konieczności uzasadnienia; przycisk „Wybór trybu jest świadomy – odnotuj”.
- Komplet dokumentów według trybu (kreator_zam.KOMPLET_TRYBU), 7 nowych rodzajów dokumentów z poleceniami:
  ogłoszenie o zamówieniu, wniosek o dopuszczenie do udziału, zaproszenie do składania ofert, zaproszenie do negocjacji,
  zaproszenie do ofert ostatecznych, protokół postępowania, uzasadnienie wyboru trybu (bez twierdzenia, że przesłanka jest spełniona,
  gdy dane tego nie potwierdzają). Np. przetarg ograniczony: ogłoszenie, wniosek, zaproszenie + standard + protokół;
  wolna ręka: uzasadnienie trybu, zaproszenie do negocjacji, OPZ, umowa, protokół (bez SWZ).
- Nazwa wybranego trybu trafia wprost do dokumentów.

### 3. Własne wzory
- Wzory wgrane w kreatorze (i z biblioteki wzorów konta) są dołączane do generowania KAŻDEGO dokumentu jako podstawa:
  program zachowuje ich układ, numerację i sformułowania, zmieniając tylko to, czego wymaga sprawa. Kreator pokazuje,
  które wzory zostaną użyte. Wzory można też sprawdzić – wgrywając je do sprawy prawnika jako dokumenty do oceny.

### Testy
16 testów etapu 2 (wybór trybu, kontrola z wartością, decyzja, komplety: ograniczony / wolna ręka / automatyczny, nazwa trybu
w poleceniu, własny wzór jako podstawa, 3 nowe dokumenty Word, link: zły adres, strona BIP z PDF i ZIP – lokalny serwer,
e-Zamówienia na żywo – rozpoznana przerwa techniczna) + test w przeglądarce – 0 błędów; regresja obu edycji bez zmian.

### Pliki
bzp.py (pobierz_z_linku, przerwa_techniczna), kreator_zam.py (TRYBY_WYBOR, KOMPLET_TRYBU, komplet_dokumentow, porownaj_wybor_trybu),
zamawiajacy.py (7 rodzajów dokumentów), serwer.py (stan kreatora, zapis wyboru, wzory w generowaniu, pobieranie z linku, wersja),
app.js, instrukcja.html / .pdf.

---

## Wersja „2026-11-08 dla-prawnika-etap1”

Poprzednia wersja: „2026-11-07 zapas-na-rozumowanie”. Nowy tryb na ekranie startowym: **Dla Prawnika** (po Dostawcy).

### Ustalenia
- Prawnik pracuje dla zamawiającego albo wykonawcy – wybór w każdej sprawie (także „niezależna opinia”).
- „Nieruchomości” = roboty budowlane na nieruchomości (Pzp); gospodarka nieruchomościami (UGN) poza zakresem.
- Wynik sprawdzenia: lista uwag z raportem Word ORAZ opinia prawna w formie pisma.
- Przepisy sprawdzone w źródłach: art. 439 Pzp – waloryzacja w umowach na roboty, dostawy i usługi > 6 miesięcy
  (t.j. Dz.U. 2026 poz. 793); art. 307 Pzp – związanie ofertą w trybie podstawowym maks. 30 dni.

### Etap 1 – sprawdzenie dokumentacji i opinia prawna
- Karta „Dla Prawnika” (po „Dla Dostawcy / Usługodawcy”), dwie ścieżki: Sprawdź dokumentację / Sporządź dokumentację;
  pulpit z kafelkami; lista „Sprawy – sprawdzenie dokumentacji i opinie prawne”, przycisk „Nowa sprawa”.
- Sprawa (typ projektu „prawnik”, dane osobno dla każdego konta): dokumentacja → **Sprawa – ustawienia** (przedmiot: roboty budowlane
  na nieruchomości / usługi / dostawy; tryb: 14 trybów i wariantów albo „ustal z dokumentów”; dla kogo: zamawiający / wykonawca /
  niezależna; adresat opinii; pytania klienta) → **Sprawdzenie dokumentacji** → **Opinia prawna**.
- Listy kontrolne (prawnik.py): osobne dla robót na nieruchomości (podstawy formalne inwestycji, dokumentacja projektowa
  i STWiORB / PFU, ryczałt a przedmiar, podwykonawstwo, umowa o pracę, kierownik budowy, odbiory, gwarancja), usług
  (opis przedmiotu, umowa o pracę, kryteria jakościowe, prawa autorskie, RODO, OC) i dostaw (neutralność i równoważność,
  środki dowodowe, prawo opcji, gwarancja i serwis) + wspólna (przesłanki trybu, progi, terminy, warunki, wykluczenia,
  wadium, kryteria, art. 436 / 433 / 454–455 / 439, spójność dokumentów, RODO, jawność).
- Perspektywa: zamawiający – zgodność i ryzyko (KIO, unieważnienie, korekta), gotowe nowe brzmienie; wykonawca – ryzyka,
  pytania do zamawiającego, podstawy do odwołania; niezależna – obie strony.
- Uwagi: nowe pole „podstawa prawna” (także w raporcie uwag – dla wszystkich modułów); cytaty sprawdzane w plikach,
  decyzje, wprowadzanie zmian, części przy dużej dokumentacji – jak w sprawdzaniu zamawiającego/wykonawcy.
- Zmiana przedmiotu, trybu lub strony → wcześniejsze sprawdzenie oznaczone jako nieaktualne.
- Opinia prawna (Word): przedmiot, stan faktyczny, analiza zagadnień (podstawa, rekomendacja), odpowiedzi na pytania klienta,
  wnioski, zastrzeżenia; nagłówek – kancelaria z Profilu firmy (autor pisma); adresat, miejscowość, podpis, nr wpisu –
  [UZUPEŁNIJ] na żółto; bez uwag odrzuconych; powstaje z ustaleń sprawdzenia (bez ponownego czytania dokumentów).
- Sporządź dokumentację: na razie kreator zamawiającego; jawny wybór trybu i komplet dokumentów według trybu – etap 2.
- Edycja dla urzędu: moduł prawnika niedostępny (jak inne moduły spoza ścieżki zamawiającego).

### Testy
18 testów serwera (sprawa, ustawienia, 3 listy kontrolne, 3 perspektywy, pytania klienta, podstawa prawna w uwagach
i raporcie, znacznik nieaktualności, opinia Word z nagłówkiem, adresatem, podstawą i żółtymi polami, pobieranie, ochrona
przed użyciem w innych projektach, zapamiętanie trybu) + test w przeglądarce (karta startowa po Dostawcy, ścieżki,
pulpit, sprawa z 5 sekcjami, zmiana strony przełącza sekcję błędów) – 0 błędów; regresja obu edycji bez zmian.

### Pliki
Nowy: prawnik.py. Zmienione: serwer.py (typ „prawnik”, ustawienia, gałąź sprawdzania, opinia prawna, tryb), zamawiajacy.py
(pole „podstawa”), app.js, index.html, styl.css, instrukcja.html / .pdf (12.10).

---

## Wersja „2026-11-07 zapas-na-rozumowanie”

Poprzednia wersja: „2026-11-06 bledy-zawsze-osobno”.

### Prawdziwa przyczyna pustych odpowiedzi AI („pusta odpowiedź (zakończenie: max_tokens)”, zadanie trwające ~10 min)
Modele używane przez program (Claude Sonnet 5.5, Opus 5.5) mają rozumowanie (thinking) włączone domyślnie – nie da się
go wyłączyć. Tekst rozumowania nie jest zwracany, ale jego tokeny liczą się do limitu długości odpowiedzi (max_tokens).
Program wysyłał limity 12–20 tys. tokenów, liczone jako „długość odpowiedzi”. Przy kilkuset stronach dokumentacji
rozumowanie zużywało cały limit i odpowiedź przychodziła pusta. Do tego program:
- przy pustej odpowiedzi z zakończeniem max_tokens próbował „dopisać dalszą część” (nawet 5 razy) – do pustego tekstu;
- ponawiał z tym samym limitem – więc z tym samym skutkiem.
Wcześniejsze poprawki (części, ponowienia, osobne wykrywanie błędów) zostają, ale leczyły objaw; ta usuwa przyczynę.
Źródło: dokumentacja API – Thinking (tokeny rozumowania liczą się do max_tokens; zalecenie: podnieść max_tokens)
https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting

### Poprawka (jedno miejsce – wszystkie zadania AI w programie)
- Dla modeli z domyślnym rozumowaniem do limitu odpowiedzi dodawany jest zapas 32 tys. tokenów (maks. 128 tys. – limit modelu).
  Limit to pułap – płaci się tylko za faktycznie zużyte tokeny. Poziomu wysiłku (effort) nie obniżono – jakość przed kosztem.
- Pusta odpowiedź z zakończeniem max_tokens: bez dopisywania; jedno ponowienie z zapasem 96 tys. tokenów.
- Dziennik: „AI zwróciło pustą odpowiedź (zakończenie: max_tokens; zużyto N tokenów odpowiedzi – głównie na rozumowanie) – ponawiam z większym limitem”.

### Testy
Symulacja API z rozumowaniem 60 tys. tokenów: odpowiedź uzyskana w ≤ 3 zapytaniach, każde z zapasem, bez dopisywania,
czytelny dziennik (9 testów) – 0 błędów; regresja obu edycji (analiza dostawcy, błędy, weryfikacja, kreator, Księgowość) bez zmian.

### Pliki
modul_oferty.py (limit_z_rozumowaniem, _jedno_wywolanie, _claude_stream, _tekst_z_dopisywaniem), serwer.py (wersja), instrukcja.html / .pdf.

---

## Wersja „2026-11-06 bledy-zawsze-osobno”

Poprzednia wersja: „2026-11-05 analiza-dostawcy-w-czesciach”.

### Problem: analiza widzi błędy w podsumowaniu, a lista błędów i raport są puste
Przyczyna: analiza dostawcy zwracała w jednej odpowiedzi (limit 12 000 tokenów) kolejno: podsumowanie, dane postępowania,
pozycje do zaoferowania, wymagane dokumenty, warunki – a dopiero potem błędy. Przy dużym zakresie (np. 37 zadań IT/OT)
lista pozycji wyczerpywała limit, odpowiedź była ucinana przed listą błędów. Program zachowywał kompletne fragmenty,
więc podsumowanie wspominało sprzeczności, a sekcja błędów pokazywała „Nie znaleziono błędów”, raport – „brak błędów”.

### Poprawka – błędy w dokumentacji przetargowej zawsze wykrywane osobno
- Po analizie (w tym samym zadaniu) ZAWSZE uruchamia się osobne, dokładne wykrywanie błędów – ten sam mechanizm co
  „Wykryj błędy”: dosłowne cytaty, sprawdzanie odwołań, ponowienia, części przy dużej dokumentacji. Wynik trafia do sekcji
  „Błędy i niejasności” (waga, problem, miejsce, pytanie do zamawiającego) i do wykazu błędów (Word) – bez dublowania.
- Analiza nie prosi już AI o błędy (nie konkurują z listą pozycji); limit odpowiedzi 20 000 tokenów; gdy odpowiedź mimo to
  zostanie ucięta – ostrzeżenie, że lista pozycji może być niepełna.
- Nigdy fałszywe „nie znaleziono błędów”: nieudane wykrywanie → czerwona ramka z przyczyną (poprzednie błędy zachowane);
  pusta lista przy podsumowaniu mówiącym o sprzecznościach → ostrzeżenie; „Sprawdzenie nie wykazało błędów” tylko po udanym sprawdzeniu.
- Nowe przyciski: „Wykryj błędy ponownie” (samo sprawdzenie błędów) i „Pobierz wykaz błędów (Word)” w sekcji błędów.
- Weryfikacja: dokumentacja zbyt obszerna na jedno zapytanie → od razu sprawdzanie w częściach (zamiast „Dokumenty są zbyt duże”).
- Projekty przeanalizowane wcześniej: sekcja pokaże ostrzeżenie i przycisk „Wykryj błędy ponownie”.

### Testy
11 testów (przetarg 37 zadań z uciętą analizą, 3 błędy z osobnego sprawdzenia, wagi i pytania, raport bez dublowania,
Word, nieudane sprawdzenie, przycisk ponowienia, zbyt duża dokumentacja) + widok sekcji w 5 stanach w przeglądarce – 0 błędów;
regresja obu edycji bez zmian.

### Pliki
serwer.py (polecenie_analizy_dostawcy, praca_analiza_dostawcy, praca_bledy_dostawcy, trasa /analiza-dostawcy/bledy,
bledy_dokumentacji, praca_weryfikacja, wersja), app.js (sekcja błędów, bledyD, bledyPodejrzane), instrukcja.html / .pdf.

---

## Wersja „2026-11-05 analiza-dostawcy-w-czesciach”

Poprzednia wersja: „2026-11-04 weryfikacja-w-czesciach”.

### Błąd: „Analiza przetargu (dostawca) – Odpowiedź AI nie zawiera danych (AI odpowiedziało samym tekstem)”
Przyczyny w analizie dla dostawcy (i dwóch pokrewnych funkcjach dostawcy):
- jedno wywołanie AI bez ponowienia – pierwsza pusta odpowiedź od razu kończyła się błędem;
- cichy limit 20 plików (formularz ofertowy i oświadczenia – 20, pozycje formularza cenowego – 15), choć dziennik podawał liczbę wszystkich;
- pomijany wybór „uwzględnij / pomiń” z kroku 1 – do AI trafiały także odznaczone rysunki i skany;
- pliki nieodczytane pomijane bez śladu;
- komunikat mylący: pusta odpowiedź opisywana jako „AI odpowiedziało samym tekstem”.

### Poprawki
- Analiza dostawcy: tylko pliki „uwzględnij” z kroku 1, bez limitu liczby plików, pliki nieodczytane wypisane w dzienniku;
  ponowienie (ai_dane); przy zbyt obszernej dokumentacji – analiza w częściach (SWZ w każdej części), połączenie bez powtórzeń:
  pozycje do zaoferowania, błędy dokumentacji, wymagane dokumenty, kryteria, warunki, ryzyka; dane postępowania uzupełniane
  z kolejnych części; podsumowanie informuje o analizie w częściach; projekt zapamiętuje tryb części.
- Formularz ofertowy i oświadczenia, pozycje formularza cenowego: wybór plików z kroku 1, bez cichych limitów, lista nieodczytanych.
- Wspólnie dla wszystkich zadań AI zwracających dane (dotacje, plan rozliczenia, zapytania ofertowe, nieruchomości, dostawca…):
  pusta odpowiedź → jedno automatyczne ponowienie z wyraźnym poleceniem zwrócenia danych; komunikat rozróżnia pustą odpowiedź
  (z przyczyną zakończenia i podpowiedzią: pomiń w kroku 1 rysunki i skany bez treści) od odpowiedzi tekstowej (z jej początkiem).

### Testy
13 testów analizy dostawcy (25 plików, plik odznaczony, plik nieczytelny, pusta odpowiedź na całość, części, łączenie bez
powtórzeń, formularz cenowy 24 pozycje, komunikaty) + test ponowienia na poziomie wspólnym – 0 błędów; regresja obu edycji bez zmian.

### Pliki
serwer.py (bloki_dokumentow, polacz_analizy_dostawcy, praca_analiza_dostawcy, praca_zalaczniki_dostawcy, praca_pozycje_formularza, wersja),
modul_oferty.py (ponowienie przy pustej odpowiedzi, komunikat w wyciagnij_json), instrukcja.html / .pdf.

---

## Wersja „2026-11-04 weryfikacja-w-czesciach”

Poprzednia wersja: „2026-11-03 edycja-zamawiajacy-etap1”.

### Błąd: „Weryfikacja dokumentacji – Odpowiedź AI nie zawiera danych (AI odpowiedziało samym tekstem)”
Przyczyna: weryfikacja („Wykryj błędy”) wysyłała całą dokumentację projektu w jednym zapytaniu – w zgłoszonym przypadku
ok. 318 tys. tokenów (kilkaset stron). AI zwróciło pustą odpowiedź zarówno w trybie danych, jak i tekstowym; ponowienie
odbywało się z tym samym ogromnym wejściem, więc kończyło się tak samo, a komunikat nie podawał przyczyny.
(Linia „odczytano 317,9 tys., zapisano 0,1 tys. tokenów” dotyczy pamięci podręcznej, nie długości odpowiedzi AI.)

### Poprawka
- Gdy cała dokumentacja naraz nie da wyniku, program sam sprawdza ją w częściach (ok. 120 tys. tokenów na część);
  SWZ (jeśli nieduża) jest dołączana do każdej części jako punkt odniesienia, więc sprzeczności z SWZ są nadal wykrywane.
- Uwagi z części są łączone bez powtórzeń, od krytycznych; podsumowanie informuje, że sprawdzanie odbyło się w częściach
  i że sprzeczności między dokumentami z różnych części (poza porównaniem z SWZ) mogły nie zostać wykryte.
- Projekt zapamiętuje sprawdzanie w częściach – kolejne uruchomienia od razu w częściach (bez jednej dużej, nieudanej próby).
- Komunikat błędu podaje przyczynę (odmowa AI / limit długości / zakończenie bez wyniku), długość i początek odpowiedzi AI –
  dotyczy wszystkich zadań AI zwracających dane (funkcja ai_dane).
- Część bez wyniku nie przerywa całości – jest wymieniona w podsumowaniu jako niesprawdzona.

### Testy
10 testów (duża dokumentacja z pustą odpowiedzią na całość, podział na 3 części z SWZ, limit części, łączenie uwag,
kolejność wag, informacja w podsumowaniu, zapamiętanie, drugie uruchomienie, czytelny błąd przy odmowie) – 0 błędów;
regresja obu edycji – bez zmian.

### Pliki
serwer.py (ai_dane, bloki_projektu_pliki, podziel_na_czesci, weryfikacja_w_czesciach, praca_weryfikacja, wersja),
instrukcja.html / .pdf (krok 2 „Wykryj błędy”).

---

## Wersja „2026-11-03 edycja-zamawiajacy-etap1”

Poprzednia wersja: „2026-11-02 uwagi-do-pobrania”. Etap 1 wyodrębnienia modułu zamawiającego jako programu dla urzędu.

### Jak to działa
Jeden kod, dwie edycje. Edycję wybiera zmienna środowiskowa przy instalacji (użytkownik programu jej nie zmieni):
- brak zmiennej albo `BIDIVIA_EDYCJA=pelna` – cały program, bez zmian (wdrożenie na Render działa jak dotąd);
- `BIDIVIA_EDYCJA=zamawiajacy` – „Bidivia – Zamawiający”: przygotowanie zamówienia, sprawdzenie ofert, realizacja umów
  + konta i role, archiwum, ustawienia, instrukcja, dane (profil).
Sprawdzenie: adres /zdrowie podaje pole „edycja”.

### Edycja zamawiającego – zabezpieczenia (dwie warstwy)
1. Adresy modułów innych ścieżek zwracają 404 „niedostępne w tej edycji”: przetargi, BIP, Baza Konkurencyjności, BZP,
   pobieranie ogłoszeń, alerty, historia zamawiających, wyniki ofert, raporty rynkowe, obszar, dostawy, hurtownie,
   klienci, pracownicy, godziny, kadry, płace, dotacje i zapytania beneficjenta, nieruchomości, Księgowość, strona oferty
   handlowej; nie da się też utworzyć projektu przetargu.
2. Każda trasa projektu sprawdza rodzaj projektu: dostępne tylko projekty zamawiającego (zamówienie, kosztorys
   inwestorski, weryfikacja, dokumentacja, inwestycja, ocena ofert). Projekty innych rodzajów są niewidoczne na listach.
- Zadania nocne: wyłączone pobieranie ogłoszeń, automatyczne wyszukiwanie, harmonogramy naborów, sprawdzanie wyników
  i alerty dotacji (bez ruchu sieciowego i kosztów AI); zostają pomiary pogody (dziennik budowy w realizacji umów).
- Interfejs: od razu ścieżka zamawiającego (bez wyboru trybu i bez „Zmień tryb”); przyciski i widoki innych modułów
  usuwane; próba wejścia w inny moduł → pulpit. Strona logowania z nagłówkiem dla zamawiającego, bez oferty dla firm.

### Testy
- 32 testy edycji zamawiającego (blokady 12 grup adresów, kreator, ukrycie projektu wykonawcy i jego plików, listy,
  realizacja, wspólne moduły, strona logowania i główna, zadania nocne) – 0 błędów.
- Przegląd 86 stron/API w obu edycjach – bez błędów 500; pobieranie uwag z kreatora w obu edycjach – 0 błędów;
  regresja pełnej edycji (Księgowość, nieruchomości) – bez zmian.
- Interfejs w przeglądarce (bez błędów JavaScript): start w ścieżce zamawiającego, blokada przejścia do przetargów
  i zmiany trybu, realizacja umów działa.

### Następne etapy
2. Pakiet Docker (serwer w urzędzie) + skrypt budowy pakietu edycji.
3. Tryb testowy (licencja z datą, baner, przykładowe zamówienie, „zgłoś uwagę”), ustawienia AI (osobny klucz urzędu
   z limitem), „Dane urzędu” zamiast „Profil firmy”, dziennik zdarzeń.
4. Instalator Windows (jeden komputer).
5. Dokumentacja dla urzędu (instalacja, zapora, kopie zapasowe, karta przetwarzania danych dla IOD).

### Pliki
serwer.py (EDYCJA, blokada, filtr projektów, zadania nocne, strona logowania i główna, /zdrowie), app.js (blok edycji na końcu).

---

## Wersja „2026-11-02 uwagi-do-pobrania”

Poprzednia wersja: „2026-11-01 ksiegowosc-etap0”.

### Pobieranie uwag do sporządzonej dokumentacji (kreator zamawiającego – krok 6 „Sprawdzenie i zmiany”)
- Pod listą propozycji: wybór zakresu (wszystkie / przyjęte / bez decyzji – z liczbami) i przycisk „Pobierz uwagi”.
- Plik Word „Uwagi do dokumentacji postępowania” (Uwagi_do_dokumentacji[_przyjete|_do_decyzji]_<nazwa zamówienia>.docx):
  nazwa zamówienia, data sprawdzenia i data wygenerowania; podsumowanie liczbowe (wagi i decyzje); podsumowanie sprawdzenia z AI;
  tabela: dokument – liczba uwag – krytyczne/istotne – przyjęte – do ręcznego wprowadzenia;
  uwagi pogrupowane według dokumentów, od krytycznych (krytyczne i istotne na czerwono): obecne brzmienie albo miejsce
  wstawienia nowego zapisu, proponowane brzmienie (z oznaczeniem „poprawione przez zamawiającego”), uzasadnienie, podstawa,
  decyzja (PRZYJĘTA / ODRZUCONA / DO DECYZJI) i sposób wprowadzenia (automatycznie / ręcznie);
  zmiany do ręcznego wprowadzenia z ostatniego „Wprowadź zaakceptowane zmiany”.
- Przed pobraniem program zapisuje brzmienia poprawione w polach tekstowych – plik = to, co na ekranie.
- Bez danych z Profilu firmy. Gdy nie było sprawdzenia – czytelny komunikat zamiast pustego pliku.
- Trasa: GET /api/projekty/<id>/kreator/uwagi.docx?zakres=wszystkie|przyjete|do_decyzji.

### Testy
15 testów pobierania (zakresy, kolejność wag, decyzje, poprawione brzmienie, sposób wprowadzenia, brak danych profilu,
brak sprawdzenia) – 0 błędów; podgląd pliku po konwersji do PDF; regresja całego programu bez zmian.

### Pliki
kreator_zam.py (raport_uwag_docx), serwer.py (trasa, wersja), app.js (przycisk i zapis poprawek), instrukcja.html / .pdf (krok „Sprawdzenie i zmiany”).

---

## Wersja „2026-11-01 ksiegowosc-etap0”

Poprzednia wersja: „2026-10-31 oferta-rzeczoznawca-dotacje”. Nowy moduł **Księgowość** – prototyp, etap 0 + wgrywanie dokumentów.

### Dostęp i dane
- Moduł widoczny tylko dla administratora: menu (obok „Konta i aktywność”) i kafelek na pulpicie; wszystkie trasy /api/ks/* chronione (inny użytkownik – 403).
- Dane osobno dla każdego konta: katalog konta/ksiegowosc (profil.json, dokumenty.json, reguly.json, pliki/) – gotowe do udostępnienia klientom.

### Profil podatnika (Twoje dane wpisane)
JDG, podatek liniowy, zaliczki PIT miesięczne, VAT czynny – metoda ogólna, rozliczenie miesięczne (JPK_V7M; zmiana na kwartał jednym polem),
pełny ZUS bez chorobowego, zleceniobiorcy, samochód elektryczny w użytku mieszanym (najem długoterminowy), kasa fiskalna, towary handlowe,
NIP 886-251-28-48 (suma kontrolna poprawna), US w Świdnicy – kod 0220, rachunek ZUS (suma kontrolna poprawna), księgi od 2026-10.
Na żółto do uzupełnienia: e-mail do JPK, wartość samochodu z umowy najmu, dane otwarcia styczeń–wrzesień 2026.

### Parametry roku – ksiegowosc_parametry.py
Jedno miejsce do corocznej aktualizacji; przy każdej wartości źródło, data sprawdzenia i status (potwierdzone / do weryfikacji).
Potwierdzone w źródłach 21.10.2026: podstawy ZUS 2026 (5652 zł; 1441,80 zł), płaca minimalna 4806 zł, minimalna zdrowotna 432,54 zł (od 02.2026),
zdrowotna przy liniowym 4,9%, JPK_V7M(3)/V7K(3) z oznaczeniami NrKSeF/OFF/BFK/DI, terminy KSeF, kod US 0220.
Do weryfikacji przed etapami 2–3: składka rentowa i chorobowa, limit odliczenia zdrowotnej, zasady i limity samochodowe, próg 10 000 zł.

### Dokumenty
- Wgrywanie PDF / zdjęć (kilka naraz); inne formaty odrzucane z powodem; ten sam plik drugi raz – odrzucony.
- Odczyt przez AI modelem do dokumentów (jakość przed kosztem), dokładnie z dokumentu; nieczytelne pola oznaczone.
- Kontrola bez AI: netto + VAT = brutto, suma stawek, VAT dla każdej stawki – rozbieżność z kwotą różnicy, do decyzji.
- Kierunek (sprzedaż / zakup) z Twojego NIP; ostrzeżenie, gdy NIP-u nie ma na fakturze; oznaczenie JPK: NrKSeF / BFK / DI.
- Duplikaty: ten sam plik, numer KSeF, kontrahent + numer (także w innym zapisie) – pewne; kontrahent + data + kwota – możliwe.
  Duplikatu nie da się zatwierdzić bez świadomego potwierdzenia; przy zatwierdzaniu duplikaty przeliczane na bieżąco.
- Klasyfikacja: kategoria, odliczenie VAT (100/50/0), koszt w PIT (100/75/20/0) z uzasadnieniem; podpowiedź z Twoich decyzji
  dla kontrahenta ma pierwszeństwo przed AI, inna podpowiedź AI pokazana obok; nic nie trafia dalej bez „Zatwierdź”.
- Nauka: zatwierdzone decyzje zapamiętywane dla kontrahenta i przekazywane AI jako przykłady.
- Poprawki pól z dziennikiem (stara → nowa wartość), podgląd pliku źródłowego, usuwanie do kosza (plik zostaje).

### Testy
- 20 testów logiki (NIP, NRB, sumy, kierunek, JPK, nauka, duplikaty, parametry) – 0 błędów.
- 19 testów serwera z prawdziwymi plikami PDF/JPG i atrapą odpowiedzi AI (uprawnienia, wgrywanie, odczyt, duplikaty,
  blokada zatwierdzenia, poprawki, nauka, usuwanie, plik źródłowy) – 0 błędów.
- Widok sprawdzony w przeglądarce na komputerze i telefonie (bez błędów JavaScript); regresja całego programu bez zmian.

### Pliki
Nowe: ksiegowosc.py, ksiegowosc_parametry.py, ksiegowosc.js. Zmienione: serwer.py, app.js, index.html, styl.css,
instrukcja.html / instrukcja.pdf (punkt 12.9). WERSJA_PROGRAMU = „2026-11-01 ksiegowosc-etap0”.

---

## Wersja „2026-10-31 oferta-rzeczoznawca-dotacje”

Poprzednia wersja: „2026-10-30 sito-bez-ai”. Zmiany dotyczą działu „Nasza oferta” (strona /oferta i PDF-y do pobrania).

### Nowe grupy oferty
1. **Dla rzeczoznawcy** (rzeczoznawcy majątkowi): teczka nieruchomości, przeznaczenie z rejestru planów,
   transakcje i metody wyceny, projekt operatu z punktami kontrolnymi, due diligence i analiza zabudowy;
   wyzwania → rozwiązania, proces, korzyści, 4 zrzuty ekranu, pytania. Wyraźnie: operat sporządza i podpisuje
   rzeczoznawca; oferty rynkowe to analiza rynku, nie podstawa operatu; nazwy portali nie występują.
2. **Dotacje UE/KPO** (dotąd jedno zdanie w części wspólnej): wyszukiwarka naborów, nadchodzące nabory i alerty,
   wniosek, rozliczanie; 4 zrzuty ekranu, pytania.
3. Nowe PDF-y: oferta_rzeczoznawca.pdf (6 stron), oferta_dotacje.pdf (5 stron); trasy /oferta/pdf/rzeczoznawca i /oferta/pdf/dotacje.
4. Strona logowania – „Oferta dla:” z linkami do wszystkich grup (dodane: Dostawcy, Rzeczoznawcy, Dotacje UE/KPO).

### Zaktualizowane grupy
- **Wykonawca:** pełna lista ogłoszeń z BZP i wstępne sito bez AI; pobieranie dużych archiwów z kontrolą kompletności.
- **Dostawca:** pełna lista ogłoszeń z BZP i sito.
- **Zamawiający:** kreator uzupełniany z dokumentów (także ZIP z przedmiarem), kontrola trybu z wartością i progami,
  dane zamawiającego wpisuje użytkownik (żółte pola); nowy zrzut „Kreator uzupełniony z dokumentów”.
- **Część wspólna:** zasada „dokumenty mają pierwszeństwo – różnice do decyzji”; dane z rejestrów państwowych.
- Nagłówek strony: program także dla rzeczoznawców i wnioskodawców dotacji; wybór grup w 3 kolumnach (6 kafelków).

### Sposób wygenerowania
oferta.html = oferta.strona(...) z dotychczasowymi zrzutami (wyjęte z poprzedniego oferta.html – sprawdzono, że plik
odtwarzał się bajt w bajt) i nowymi zrzutami z instrukcji (dane przykładowe). PDF-y – Chromium, A4, marginesy 0,4"
jak w poprzednich (sprawdzone: stara oferta dla wykonawcy odtworzona tą metodą ma te same 8 stron i ten sam układ).

Strony PDF: wykonawca 8, dostawca 6, zamawiający 7, inwestor 5, rzeczoznawca 6, dotacje 5, wszystkie moduły 31.

### Pliki zmienione
oferta.py, oferta.html, oferta_*.pdf (7, w tym 2 nowe), serwer.py (trasa PDF, wersja), login.html.

---

## Wersja „2026-10-30 sito-bez-ai”

Poprzednia wersja: „2026-10-29 dane-na-zywo” (jej zmiany: ZMIANY_2026-10-29.md).

### Wstępne sito bez AI przed oceną przetargów

Powód: od poprzedniej wersji program widzi wszystkie ogłoszenia z BZP (ok. 550–600 dziennie zamiast 100),
a dotychczasowe dopasowanie słów było luźne – słowo wystarczyło znaleźć gdziekolwiek w treści, także w środku
innego wyrazu („dach” w „zakładach”) albo w stałej formułce („droga” w „drogą elektroniczną” – prawie każde ogłoszenie).

1. **Punkty dopasowania bez AI** (wspolne.py – punkty_dopasowania): słowo w tytule 3 pkt, zgodny CPV 3 pkt,
   każde inne słowo tylko w treści 1 pkt; słowo liczone od początku wyrazu; formułki BZP pomijane.
2. **Do automatycznej oceny AI** trafiają ogłoszenia z co najmniej 2 pkt (Ustawienia → „Wstępne sito bez AI”, 0 = wyłączone),
   **od najlepiej pasujących** – limit „max_do_oceny” bierze najlepsze, a nie pierwsze z brzegu (serwer.py – sito_do_oceny).
3. **Nic nie znika po cichu:** odsiane ogłoszenia zostają w wynikach z oznaczeniem „słabe dopasowanie – bez oceny AI”
   (w liście, tabeli i szczegółach – z powodem); otwarcie szczegółów uruchamia ocenę. Dziennik podaje liczbę odsianych.
4. **Sprawdzanie stron wybranych instytucji (BIP)** – dotąd wysyłało wszystkie nowe ogłoszenia do AI bez filtra;
   teraz: wykluczenia + sito (słowa i CPV obu trybów: wykonawca i dostawca).
5. **Wyszukiwanie – ogłoszenia ze stron instytucji** przechodzą teraz także przez wykluczenia.
6. Ręczne „Oceń przez AI” – bez sita (decyzja użytkownika). Model oceny – bez zmian (model lekki).

### Test na prawdziwych ogłoszeniach BZP (616 ogłoszeń z jednego dnia)
| Słowa firmy | dotychczasowe dopasowanie | do AI po sicie | odsiane |
|---|---|---|---|
| budowlane (remont, termomodernizacja, dach, elewacja, kanalizacja, przebudowa + CPV) | 105 | 84 | 21 |
| drogowe (droga, nawierzchnia, chodnik, asfalt + CPV 45233) | 203 | 59 | 144 |
| sprzątanie (+ CPV 9091) | 15 | 15 | 0 |

Odsiane to głównie fałszywe trafienia (paliwa, transport krwi, dostawy mięsa, wyjazd integracyjny). Przykład trafienia
granicznego: „Malowanie ścian w budynku sądu” (słowo „remont” tylko w treści) – zostaje w wynikach z oznaczeniem;
żeby szło do AI automatycznie, dodaj słowo „malowanie” albo CPV 4544.

### Pliki zmienione
wspolne.py, serwer.py, app.js, instrukcja.html, instrukcja.pdf (109 stron). WERSJA_PROGRAMU = „2026-10-30 sito-bez-ai”.

---

## Wersja „2026-10-29 dane-na-zywo”

Poprzednia wersja: „2026-10-28 zolte-do-uzupelnienia”. Wszystkie usługi sprawdzone na żywo 20.10.2026
(uldk.gugik.gov.pl, services.gugik.gov.pl, mapy.geoportal.gov.pl, nominatim.openstreetmap.org, ezamowienia.gov.pl).

### Błędy poprawione

1. **BZP – program widział tylko 100 ogłoszeń na każde 3 dni** (bzp.py).
   Przyczyna: API ignoruje parametr PageNumber, każda „strona” zwracała te same ogłoszenia.
   Teraz: stronicowanie kursorem SearchAfter (objectId). Test: 558 ogłoszeń zamiast 100.
2. **BZP – brak ponowień przy przeciążeniu serwera (HTTP 503)** – lista bywała ucinana, a ogłoszenie PDF niepobrane.
   Teraz: 3 ponowienia (3 s, 8 s, 20 s) przy 429/5xx i przerwanym połączeniu; komunikat, gdy lista może być niepełna.
3. **BZP – treść ogłoszeń zaczynała się od kodu CSS** – psuło to filtrowanie i szukanie platform. Teraz bloki style/script są usuwane.
4. **Dokumenty postępowania – pliki ponad 80 MB były ucinane po cichu** (np. ZIP z projektem: uszkodzony).
   Teraz: pobieranie strumieniowe do 400 MB, kontrola długości i spójności ZIP; pliki pominięte są opisane w dzienniku z linkiem.
   Pominięcie dużego pliku nie przerywa pobierania kolejnych.
5. **Nazwy plików z polskimi znakami w dwóch postaciach Unicode** – teraz jednolite (NFC).
6. **ULDK – „nie znaleziono działki”, gdy obręb i numer są w kilku gminach** (np. „Nowa Ruda 100”).
   Przyczyna: pierwsza linia odpowiedzi to liczba wyników, program akceptował tylko „0”/„1”.
   Teraz: lista działek do wyboru (gmina, powiat, powierzchnia) – program nie wybiera po cichu pierwszej.
7. **Adres → budynek – trafienia w tablicę lub ulicę przyjmowane jako budynek**; „funkcja” brana z typu drogi.
   Teraz: najpierw państwowy rejestr adresów (geokoder GUGiK), potem OpenStreetMap (zapytanie strukturalne);
   przyjmowane tylko trafienie z tym samym numerem i dokładnie tą samą ulicą. Gdy trafienie tylko w ulicę –
   ostrzeżenie „lokalizacja przybliżona” w teczce i dzienniku. Nowe: budynek z ewidencji (ULDK) – identyfikator
   i powierzchnia zabudowy z obrysu.
8. **Plany miejscowe – zły adres usługi, złe warstwy i parser czytający kod CSS** (pole „uchwała” wypełniane nazwami kolumn).
   Teraz: nowy adres geoportalu, warstwy plany_granice i wektor-str, parser trzech formatów odpowiedzi gmin
   (klucz = wartość, XML, tabela HTML). Odczytywane: tytuł planu, uchwała z datą, obowiązuje od, status,
   linki do rysunku i danych planu, symbol i przeznaczenie (plany wektorowe), plan ogólny gminy.
9. **Plany – wyszukiwanie AI nadpisywało uchwałę z państwowego rejestru.**
   Teraz: rejestr ma pierwszeństwo; inna uchwała lub symbol z internetu → różnica na żółto do decyzji.
10. **Kreator – archiwa ZIP pomijane po cichu** (w nich zwykle przedmiar i formularz cenowy, czyli ilości).
    Teraz: ZIP rozpakowywany (także zagnieżdżone); lista plików nieodczytanych w ramce „Nie odczytano … plików”.
11. **Kreator – tryb nie był odczytywany z dokumentów.**
    Teraz: AI odczytuje tryb, a program sprawdza go dodatkowo bez AI w dosłownym tekście (np. „art. 275 pkt 1”)
    – tak samo wartość szacunkową, jeśli jest podana. Różnica AI ↔ tekst dokumentu → pole czeka na wybór.
    Różnica tryb z dokumentów ↔ tryb z wartości → ramka z oceną (np. tryb podstawowy od progu UE = krytyczne;
    przetarg nieograniczony poniżej progu = dopuszczalny) i przycisk „świadomy wybór – odnotuj”.
12. **Pliki binarne (np. DWG) wysyłane do AI jako tekst** – teraz trafiają na listę nieodczytanych.
13. **Duże zdjęcia / skany rysunków (np. 21 MB, 14 000 px) przerywały odczyt** – limit API ok. 5 MB.
    Teraz zmniejszane do 2000 px z adnotacją „drobne napisy sprawdź w oryginale” (mało pamięci – dekodowanie w skali).
14. **Najtańszy model czytał dokumenty i dane do wycen** – wbrew zasadzie „jakość przed kosztem”.
    Zmienione na model do dokumentów: pozycje formularza cenowego (ilości), wynik postępowania (Baza Konkurencyjności),
    strona naboru dotacji, lista naborów z portali regionalnych, dokumenty naborów, wycena orientacyjna z danych rynkowych,
    czynsze najmu, ceny do kosztorysu (ręcznie ustawiony „model_ceny” ma pierwszeństwo).
    **Bez zmian (decyzja użytkownika):** wstępna ocena przetargu, zbiorcza ocena paczek ogłoszeń, lista ogłoszeń z BIP, czat pomocy.
15. **Wycena własna – nazwy portali mogły trafić do opisów ofert** (tytuł oferty). Teraz usuwane – źródło: „dane rynkowe”.

### Sprawdzone na żywo i działające bez zmian
- Zamiana PDF → Word (pdf2docx): 4 prawdziwe dokumenty 7–22 stron, pełny tekst i tabele, 1–6 s.
- Progi: 170 000 zł netto od 1.01.2026, próg UE robót 5 404 000 € = 23 291 240 zł (kurs 4,31) – zgodne z obwieszczeniem.

### Nie sprawdzone na żywo
- Odpowiedzi AI (brak klucza API w środowisku testowym) – logika wokół AI przetestowana z podstawioną odpowiedzią.
- Dokumenty użytkownika z przetargów – nie dotarły; testy na prawdziwych SWZ z BZP
  („Szlak handlowy na pograniczu kłodzkim”, Gmina Miejska Kłodzko; „Transport krwi…”, SPZOZ).

### Pliki zmienione
serwer.py, nieruchomosci.py, bzp.py, kreator_zam.py, modul_oferty.py, ceny_rynkowe.py, analiza.py (tylko komentarz),
app.js, instrukcja.html, instrukcja.pdf (107 stron). WERSJA_PROGRAMU = „2026-10-29 dane-na-zywo” (sprawdź pod /zdrowie).
