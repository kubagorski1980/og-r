# -*- coding: utf-8 -*-
"""
Bezpieczeństwo i ochrona danych (decyzje właściciela, wersja „h81”) – logika bez tras i bez importu serwera:
- SMTP użytkownika tylko do publicznych serwerów pocztowych (porty 25/465/587/2525; bez localhost, sieci prywatnych, link-local,
  adresów metadanych chmury – sprawdzane po rozwiązaniu nazwy DNS, także IPv6) i połączenie z tym samym, sprawdzonym adresem;
- usuwanie cen z odpowiedzi dla ról bez Finansów (przedmiar bez cen);
- okres przechowywania dokumentacji pracowniczej (art. 94 pkt 9b Kodeksu pracy);
- hasła tymczasowe, sprawdzenie pochodzenia formularza logowania (CSRF).
"""
import datetime as dt
import ipaddress
import re
import secrets
import smtplib
import socket
import ssl
from urllib.parse import urlsplit

# ============================================================ SMTP (H1-09)
PORTY_SMTP = (25, 465, 587, 2525)
NAZWY_ZABRONIONE = re.compile(r"(?i)^(localhost|localhost\.localdomain|ip6-localhost|ip6-loopback|metadata|metadata\.google\.internal|"
                              r"instance-data|instance-data\.ec2\.internal)$|\.(local|localhost|internal|lan|home|intranet|corp)$")
# adresy usług metadanych chmury (AWS, GCP, Azure, Oracle, Alibaba, AWS IPv6) – blokowane niezależnie od klasyfikacji „prywatny”
METADANE = {ipaddress.ip_address(x) for x in ("169.254.169.254", "169.254.170.2", "100.100.100.200", "192.0.0.192", "fd00:ec2::254")}


class BladSMTP(ValueError):
    pass


def adres_publiczny(ip):
    """Czy adres IP jest publiczny (globalnie routowalny). IPv4 zmapowane w IPv6 (::ffff:10.0.0.1) i NAT64 sprawdzane jak IPv4."""
    try:
        a = ipaddress.ip_address(str(ip).split("%", 1)[0])
    except ValueError:
        return False
    if isinstance(a, ipaddress.IPv6Address):
        if a.ipv4_mapped:
            a = a.ipv4_mapped
        elif a in ipaddress.ip_network("64:ff9b::/96"):
            a = ipaddress.IPv4Address(int(a) & 0xFFFFFFFF)
        elif a.sixtofour:
            a = a.sixtofour
    if a in METADANE:
        return False
    if a.is_loopback or a.is_private or a.is_link_local or a.is_multicast or a.is_reserved or a.is_unspecified:
        return False
    if isinstance(a, ipaddress.IPv4Address) and a in ipaddress.ip_network("100.64.0.0/10"):  # CGNAT (sieć operatora / chmury)
        return False
    return bool(a.is_global)


def sprawdz_ustawienia_smtp(serwer, port, rozwiaz=False):
    """Sprawdzenie przy zapisie ustawień: port z listy, nazwa bez oczywistych adresów wewnętrznych, adres IP podany wprost – publiczny.
    rozwiaz=True: dodatkowo rozwiązanie DNS (przy wysyłce). Zwraca komunikat błędu albo None."""
    if port not in (None, ""):
        try:
            p = int(port)
        except (TypeError, ValueError):
            return "Port SMTP: wpisz liczbę – 465 (SSL), 587 (STARTTLS), 25 albo 2525."
        if p not in PORTY_SMTP:
            return "Port SMTP: dozwolone są tylko porty serwerów pocztowych – 465 (SSL), 587 (STARTTLS), 25 albo 2525."
    h = str(serwer or "").strip().rstrip(".")
    if not h:
        return None
    if len(h) > 253 or not re.fullmatch(r"[A-Za-z0-9.\-:\[\]]+", h):
        return "Serwer SMTP: podaj nazwę serwera poczty, np. smtp.gmail.com (bez „smtp://”, ścieżki i portu)."
    goly = h.strip("[]")
    try:
        ipaddress.ip_address(goly)
        if not adres_publiczny(goly):
            return "Serwer SMTP: adres w sieci wewnętrznej (lokalny, prywatny, link-local albo metadane chmury) jest niedozwolony."
        return None
    except ValueError:
        pass
    if NAZWY_ZABRONIONE.search(h) or "." not in h:
        return "Serwer SMTP: podaj publiczny serwer poczty (np. smtp.gmail.com) – nazwy sieci wewnętrznej są niedozwolone."
    if rozwiaz:
        try:
            adresy_publiczne(h, int(port or 587))
        except BladSMTP as e:
            return str(e)
    return None


def adresy_publiczne(host, port):
    """Rozwiązuje nazwę i zwraca listę (rodzina, adres) – tylko gdy WSZYSTKIE adresy są publiczne (inaczej BladSMTP)."""
    try:
        wyn = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError, OSError) as e:
        raise BladSMTP(f"Nie można odnaleźć serwera poczty „{host}” ({e}).")
    adresy = [(r[0], r[4][0]) for r in wyn]
    if not adresy:
        raise BladSMTP(f"Nie można odnaleźć serwera poczty „{host}”.")
    zle = [a for _, a in adresy if not adres_publiczny(a)]
    if zle:
        raise BladSMTP(f"Serwer poczty „{host}” wskazuje na adres w sieci wewnętrznej ({zle[0]}) – połączenie zablokowane.")
    return adresy


class _PrzypietySMTP(smtplib.SMTP):
    """SMTP łączący się z adresem sprawdzonym wcześniej (bez ponownego DNS – ochrona przed podmianą adresu), nazwa serwera zostaje do TLS."""
    def __init__(self, adres, **kw):
        self._adres = adres
        super().__init__(**kw)

    def _get_socket(self, host, port, timeout):
        return socket.create_connection((self._adres, port), timeout, self.source_address)


class _PrzypietySMTP_SSL(smtplib.SMTP_SSL):
    def __init__(self, adres, **kw):
        self._adres = adres
        super().__init__(**kw)

    def _get_socket(self, host, port, timeout):
        s = socket.create_connection((self._adres, port), timeout, self.source_address)
        return self.context.wrap_socket(s, server_hostname=self._host)


def polacz_smtp(host, port, timeout=60):
    """Połączenie z serwerem SMTP użytkownika: port z listy, wszystkie adresy z DNS publiczne, połączenie z pierwszym z nich."""
    host = str(host or "").strip().rstrip(".")
    blad = sprawdz_ustawienia_smtp(host, port)
    if blad:
        raise BladSMTP(blad)
    port = int(port)
    adres = adresy_publiczne(host.strip("[]"), port)[0][1]
    kontekst = ssl.create_default_context()
    if port == 465:
        s = _PrzypietySMTP_SSL(adres, context=kontekst, timeout=timeout)
        s.connect(host.strip("[]"), port)
    else:
        s = _PrzypietySMTP(adres, timeout=timeout)
        s.connect(host.strip("[]"), port)
        s.starttls(context=kontekst)
    return s


# ============================================================ ceny dla ról bez Finansów (H1-04)
KLUCZE_CEN = re.compile(r"^(cena|ceny|cena_[a-z_]+|[a-z_]*_cena|wartosc|wartosci|wartosc_[a-z_]+|[a-z_]*_wartosc|netto|brutto|[a-z_]+_netto|"
                        r"[a-z_]+_brutto|netto_[a-z_]+|brutto_[a-z_]+|vat_kwota|kwota|kwoty|kwota_[a-z_]+|suma|sumy|stawka|stawki|stawka_[a-z_]+|koszt|koszty|koszt_[a-z_]+|"
                        r"koszty_[a-z_]+|zysk|kp|korekta|rynkowa|udzial_rynkowych|platnosci|faktury|wynik_oferty|robocizna|"
                        r"oferta_rynkowa|budzet|kosztorys_wartosc|wadium|zabezpieczenie|wynik_[a-z_]+|zaplacono[a-z_]*|zafakturowano[a-z_]*|naleznosci[a-z_]*|"
                        r"przeterminowane[a-z_]*|do_zaplaty|do_zafakturowania[a-z_]*|odebrano[a-z_]*|w_cenie|na_umowe|roznica)$")
# pliki z cenami: kosztorys ofertowy / inwestorski, oferta, formularz cenowy / ofertowy, rozliczenia, faktury, wycena, protokoły z kwotami
PLIK_Z_CENAMI = re.compile(r"(?i)(kosztorys|ofert|formularz|cenow|cennik|wycen|faktur|rozlicz|zestawienie_kosztow|harmonogram_rzeczowo|hrf|"
                           r"protokol_odbioru(?!.*bez_kwot)|wniosek_w|aneks)")


def plik_z_cenami(nazwa):
    n = str(nazwa or "").rsplit("/", 1)[-1]
    if re.search(r"(?i)przedmiar", n) and not re.search(r"(?i)kosztorys_ofertowy|wycen", n):
        return False
    return bool(PLIK_Z_CENAMI.search(n))


def bez_cen(dane):
    """Kopia danych bez kluczy z kwotami i bez pozycji plików z cenami (rekurencyjnie)."""
    if isinstance(dane, dict):
        wyn = {}
        for k, v in dane.items():
            if isinstance(k, str) and KLUCZE_CEN.match(k):
                continue
            wyn[k] = bez_cen(v)
        return wyn
    if isinstance(dane, list):
        wyn = []
        for x in dane:
            if isinstance(x, str) and plik_z_cenami(x) and re.search(r"\.(xlsx|xls|docx|doc|pdf|zip|eml|ath|csv)$", x, re.I):
                continue
            if isinstance(x, dict) and any(isinstance(x.get(k), str) and plik_z_cenami(x[k]) for k in ("sciezka", "plik", "nazwa")
                                           if isinstance(x.get(k), str) and re.search(r"\.(xlsx|xls|docx|doc|pdf|zip|eml|ath|csv)$", x[k], re.I)):
                continue
            wyn.append(bez_cen(x))
        return wyn
    return dane


# ============================================================ dokumentacja pracownicza (H1-10, art. 94 pkt 9b KP)
def _data(x):
    try:
        return dt.date.fromisoformat(str(x or "")[:10])
    except ValueError:
        return None


def koniec_zatrudnienia(p):
    """Data ustania stosunku pracy: wpisana w kadrach, a gdy jej brak – koniec umowy (jeśli minął) albo data usunięcia pracownika (archiwum)."""
    k = p.get("kadry") or {}
    d = _data(k.get("data_ustania"))
    if d:
        return d, "data ustania stosunku pracy (kadry)"
    u = p.get("umowa") or {}
    d = _data(u.get("do"))
    if d and d <= dt.date.today() and p.get("archiwum"):
        return d, "koniec umowy"
    if p.get("archiwum"):
        d = _data(p.get("archiwum_data"))
        if d:
            return d, "usunięcie pracownika z listy (brak daty ustania stosunku pracy)"
    return None, ""


def termin_przechowywania(p):
    """(data, opis): do kiedy przechowywać dokumentację pracowniczą pracownika (art. 94 pkt 9b KP):
    - zatrudnieni od 1.01.2019 – 10 lat od końca roku kalendarzowego, w którym stosunek pracy ustał;
    - zatrudnieni 1.01.1999–31.12.2018 – 50 lat od ustania, chyba że pracodawca złożył raport informacyjny ZUS RIA (wtedy 10 lat);
    - zatrudnieni przed 1999 r. – 50 lat od ustania.
    Brak daty ustania – (None, opis): pracownik nadal zatrudniony albo nie wiadomo, kiedy umowa ustała."""
    koniec, zrodlo = koniec_zatrudnienia(p)
    if not koniec:
        return None, "pracownik zatrudniony (albo brak daty ustania stosunku pracy) – dokumentację przechowuje się do 10 lat po ustaniu zatrudnienia"
    k = p.get("kadry") or {}
    od = _data(k.get("zatrudniony_od")) or _data((p.get("umowa") or {}).get("od"))
    ria = bool(k.get("ria"))
    if od and od < dt.date(1999, 1, 1):
        return koniec.replace(year=koniec.year + 50), f"50 lat od ustania stosunku pracy (zatrudnienie przed 1999 r.; {zrodlo})"
    if od and od <= dt.date(2018, 12, 31) and not ria:
        return koniec.replace(year=koniec.year + 50), (f"50 lat od ustania stosunku pracy (zatrudnienie 1999–2018 bez raportu ZUS RIA; {zrodlo})")
    return dt.date(koniec.year + 10, 12, 31), f"10 lat od końca roku {koniec.year} (art. 94 pkt 9b KP; {zrodlo})"


# ============================================================ hasła i logowanie (H1-07, H1-08)
ZNAKI_HASLA = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
MIN_DLUGOSC_HASLA = 10
WAZNOSC_TYMCZASOWEGO_H = 72


def haslo_tymczasowe(dlugosc=14):
    return "".join(secrets.choice(ZNAKI_HASLA) for _ in range(dlugosc))


def blad_hasla(nowe, login=""):
    """Polityka haseł – jak przy zakładaniu konta (co najmniej 10 znaków), bez hasła równego loginowi."""
    nowe = str(nowe or "")
    if len(nowe.strip()) < MIN_DLUGOSC_HASLA:
        return f"Hasło musi mieć co najmniej {MIN_DLUGOSC_HASLA} znaków."
    if login and nowe.strip().lower() == str(login).strip().lower():
        return "Hasło nie może być takie samo jak login."
    return None


def obce_pochodzenie(naglowki, host_url):
    """Formularz z obcej strony (CSRF logowania): nagłówek Sec-Fetch-Site „cross-site” albo Origin/Referer z innego adresu niż serwer.
    Brak nagłówków (programy, testy) – nie jest odrzucany; przeglądarki wysyłają Origin przy każdym POST formularza."""
    sfs = (naglowki.get("Sec-Fetch-Site") or "").lower()
    if sfs == "cross-site":
        return True
    wlasny = urlsplit(host_url)
    for n in ("Origin", "Referer"):
        v = naglowki.get(n)
        if not v:
            continue
        if v == "null":
            return True
        u = urlsplit(v)
        if (u.scheme, u.netloc.lower()) != (wlasny.scheme, wlasny.netloc.lower()):
            # za odwrotnym proxy (Render, Caddy) serwer widzi http – porównujemy wtedy samą nazwę hosta
            if u.netloc.lower() != wlasny.netloc.lower():
                return True
        return False
    return False


def rodo_lista(pracownicy, dzis=None):
    """Dokumenty kadrowe w archiwum (usunięte przez użytkownika albo należące do pracownika usuniętego z listy) z terminem przechowywania.
    Zwraca listę słowników: pracownik, imie, id, typ, numer, usunieto, plik, termin (ISO albo None), podstawa, do_usuniecia (bool)."""
    dzis = dzis or dt.date.today()
    wyn = []
    for p in pracownicy or []:
        docs = (p.get("kadry") or {}).get("dokumenty") or []
        arch_p = bool(p.get("archiwum"))
        if not docs:
            continue
        termin, podstawa = termin_przechowywania(p)
        for x in docs:
            if not (x.get("archiwum") or arch_p):
                continue
            wyn.append({"pracownik": p.get("id"), "imie": p.get("imie", ""), "id": x.get("id"), "typ": x.get("typ", ""), "numer": x.get("numer", ""),
                        "usunieto": x.get("archiwum_data") or (p.get("archiwum_data") if arch_p else ""), "plik": bool(x.get("plik")),
                        "pracownik_w_archiwum": arch_p, "termin": termin.isoformat() if termin else None, "podstawa": podstawa,
                        "do_usuniecia": bool(termin and termin < dzis)})
    return sorted(wyn, key=lambda x: (not x["do_usuniecia"], x["termin"] or "9999", x["imie"]))
