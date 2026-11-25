# -*- coding: utf-8 -*-
"""
Moduł ofertowy programu Bidivia.
Czyta dokumenty przetargu (PDF, DOCX, XLSX, ZIP, obrazy), przekazuje je do Claude razem z cennikiem firmy
i zasadami wyceny, a z odpowiedzi tworzy: kosztorys ofertowy (xlsx), formularze ofertowe (docx)
oraz analizę przetargu z listą rzeczy do sprawdzenia (docx).
"""
import base64
import datetime as dt
import io
import json
import os
import time
import re
import shutil
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import zipfile
from decimal import Decimal, ROUND_HALF_UP
from xml.etree import ElementTree as ET

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from cennik_import import importuj_kosztorys, scal

MAX_BAJTOW_ZAPYTANIA = 50 * 1024 * 1024  # dokumenty do jednego zadania AI; ponad limit jednego zapytania API (32 MB) duże pliki idą przez Files API
ROZSZ_PDF = {".pdf"}
ROZSZ_OBRAZ = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
ROZSZ_TEKST = {".txt", ".csv", ".md"}
MIESIACE = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


# ============================================================ kwoty

def zaokr(x):
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def liczba_pl(s, maks=1e13):
    """Liczba wpisana albo wklejona po polsku: spacje zwykłe i niełamliwe (U+00A0, U+202F, U+2009) oraz apostrof jako separator tysięcy,
    przecinek dziesiętny („90 000,50”, „1.234,50”, „1 234.50”). ValueError dla tekstu, nan, inf i wartości ponad `maks` (moduł)."""
    if isinstance(s, bool):
        raise ValueError("nie liczba")
    if isinstance(s, (int, float)):
        x = float(s)
    else:
        t = re.sub(r"[\s\u00a0\u202f\u2007\u2009']", "", str(s if s is not None else ""))
        if "," in t and "." in t and t.index(".") < t.index(","):  # 1.234,50 – kropka jako separator tysięcy
            t = t.replace(".", "")
        t = t.replace(",", ".")
        if not re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", t):
            raise ValueError("nie liczba")
        x = float(t)
    if x != x or abs(x) == float("inf") or abs(x) > maks:
        raise ValueError("nie liczba")
    return x


def zl(x):
    s = f"{zaokr(x):,.2f}".replace(",", " ").replace(".", ",")
    return s + " zł"


_J = ["", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć"]
_N = ["dziesięć", "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście", "szesnaście",
      "siedemnaście", "osiemnaście", "dziewiętnaście"]
_D = ["", "", "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt", "sześćdziesiąt",
      "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
_S = ["", "sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset", "siedemset", "osiemset", "dziewięćset"]


def _odmiana(n, f1, f2, f5):
    if n == 1:
        return f1
    if n % 100 in (12, 13, 14):
        return f5
    if n % 10 in (2, 3, 4):
        return f2
    return f5


def _trojka(n):
    s, r = divmod(n, 100)
    d, j = divmod(r, 10)
    cz = [_S[s]]
    if d == 1:
        cz.append(_N[j])
    else:
        cz += [_D[d], _J[j]]
    return " ".join(c for c in cz if c)


def slownie(kwota):
    kwota = zaokr(kwota)
    zlote = int(kwota)
    grosze = int(round((kwota - zlote) * 100))
    if zlote == 0:
        tekst = "zero"
    else:
        cz = []
        for dziel, formy in ((1_000_000_000, ("miliard", "miliardy", "miliardów")), (1_000_000, ("milion", "miliony", "milionów")),
                             (1000, ("tysiąc", "tysiące", "tysięcy"))):
            n, zlote_r = divmod(zlote, dziel)
            if n:
                cz.append(formy[0] if n == 1 else f"{_trojka(n)} {_odmiana(n, *formy)}")
            zlote = zlote_r
        if zlote:
            cz.append(_trojka(zlote))
        tekst = " ".join(cz)
    n = int(kwota)
    return f"{tekst} {_odmiana(n, 'złoty', 'złote', 'złotych')} {grosze:02d}/100"


# ============================================================ odczyt dokumentów

def tekst_docx(sciezka):
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(sciezka) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    wiersze = []
    for el in root.iter():
        if el.tag == ns + "p":
            t = "".join(x.text or "" for x in el.iter(ns + "t"))
            if t.strip():
                wiersze.append(t)
        elif el.tag == ns + "tr":
            pass
    # tabele: dopisz wiersze tabel w formie "a | b | c"
    for tr in root.iter(ns + "tr"):
        komorki = ["".join(x.text or "" for x in tc.iter(ns + "t")).strip() for tc in tr.iter(ns + "tc")]
        if any(komorki):
            wiersze.append(" | ".join(komorki))
    return "\n".join(wiersze)


def _tekst_doc_heurystyka(dane):
    """Awaryjny odczyt starego formatu Word (.doc) bez zewnętrznych programów: wyszukuje w pliku ciągi tekstu
    zapisane jako UTF-16 (polskie znaki) i jako 8-bitowe cp1250. Nie zachowuje układu, ale wystarcza do analizy treści."""
    znaki = r"0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż.,;:!?()\[\]%/+\-–—„”\"'§°²³ \t\r\n"
    wzor = re.compile("[" + znaki + "]{12,}")
    kawalki = []
    for przes in (0, 1):
        t = dane[przes:].decode("utf-16-le", errors="ignore")
        kawalki += [k for k in wzor.findall(t) if sum(c.isalpha() for c in k) > 8 and " " in k]
    if sum(len(k) for k in kawalki) < 200:
        t = dane.decode("cp1250", errors="ignore")
        kawalki += [k for k in wzor.findall(t) if sum(c.isalpha() for c in k) > 8 and " " in k]
    wynik, widziane = [], set()
    for k in kawalki:
        k = re.sub(r"[ \t]+", " ", k.replace("\r", "\n")).strip()
        if not k or k in widziane:
            continue
        if len(k) < 40 and all(ord(c) < 128 for c in k):  # nazwy stylów i pola techniczne Worda
            continue
        widziane.add(k)
        wynik.append(k)
    return "\n".join(wynik)


def tekst_doc(sciezka):
    """Tekst ze starego pliku Word (.doc): antiword (na serwerze), LibreOffice (jeśli zainstalowany) albo odczyt awaryjny."""
    import shutil
    import subprocess
    if shutil.which("antiword"):
        try:
            w = subprocess.run(["antiword", "-m", "UTF-8.txt", "-w", "0", sciezka], capture_output=True, timeout=120)
            t = w.stdout.decode("utf-8", "replace")
            if len(t.strip()) > 50:
                return t
        except Exception:
            pass
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        try:
            wyj = tempfile.mkdtemp()
            subprocess.run([soffice, "--headless", "--convert-to", "docx", "--outdir", wyj, sciezka], capture_output=True, timeout=180)
            docx_ = os.path.join(wyj, os.path.splitext(os.path.basename(sciezka))[0] + ".docx")
            if os.path.exists(docx_):
                t = tekst_docx(docx_)
                shutil.rmtree(wyj, ignore_errors=True)
                if t.strip():
                    return t
        except Exception:
            pass
    with open(sciezka, "rb") as f:
        return _tekst_doc_heurystyka(f.read())


def tekst_xlsx(sciezka):
    import openpyxl
    wb = openpyxl.load_workbook(sciezka, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f"## Arkusz: {ws.title}")
        for row in ws.iter_rows(values_only=True):
            if any(v not in (None, "") for v in row):
                out.append("\t".join("" if v is None else str(v) for v in row))
    return "\n".join(out)


ARCHIWA = (".zip", ".7z")  # rozpakowywane automatycznie (RAR – wymaga zewnętrznego programu, pomijany)
# limity rozpakowania (ochrona dysku przed „zip bomb”); liczone łącznie dla archiwów zagnieżdżonych
LIMITY_ARCHIWUM = {"bajty": 500 * 1024 * 1024, "pliki": 2000, "wspolczynnik": 200, "wspolczynnik_od": 5 * 1024 * 1024, "glebokosc": 3}
# programy i skrypty – nie są dokumentacją; odrzucane przy wgrywaniu i pomijane przy rozpakowaniu
PLIKI_WYKONYWALNE = (".exe", ".com", ".bat", ".cmd", ".msi", ".msp", ".scr", ".pif", ".cpl", ".vbs", ".vbe", ".js", ".jse", ".wsf", ".wsh",
                     ".ps1", ".psm1", ".jar", ".dll", ".sys", ".lnk", ".hta", ".reg", ".sh", ".apk", ".app")
_PLIKI_SYSTEMOWE = r"(?i)(^|/)(thumbs\.db|\.ds_store|desktop\.ini)$|(^|/)__macosx/"


class BladArchiwum(ValueError):
    """Archiwum, którego nie da się (albo nie wolno) rozpakować – komunikat po polsku, bez nazwy pliku (dopisuje ją wywołujący)."""


class LimitArchiwum(BladArchiwum):
    """Przekroczony limit rozpakowania (rozmiar, liczba plików, współczynnik kompresji, zagnieżdżenie) – archiwum odrzucane."""


def czy_archiwum(sciezka):
    return str(sciezka).lower().endswith(ARCHIWA)


def czy_wykonywalny(nazwa, sciezka=None):
    """Plik programu: po końcówce nazwy albo (gdy podano ścieżkę) po sygnaturze EXE/ELF na początku pliku."""
    if str(nazwa).lower().endswith(PLIKI_WYKONYWALNE):
        return True
    if sciezka:
        try:
            with open(sciezka, "rb") as f:
                p = f.read(4)
            return p[:2] == b"MZ" or p == b"\x7fELF"
        except OSError:
            return False
    return False


def _mb(b):
    return f"{b / 1024 / 1024:.0f} MB"


def _sprawdz_limity(budzet, wpisy_rozmiary, rozmiar_archiwum, glebokosc):
    """Sprawdza deklarowane rozmiary przed rozpakowaniem; zwiększa licznik plików w budżecie."""
    L = budzet["limity"]
    if glebokosc >= L["glebokosc"]:
        raise LimitArchiwum(f"archiwa zagnieżdżone głębiej niż {L['glebokosc']} poziomy – rozpakuj je na komputerze i wgraj potrzebne pliki.")
    budzet["pliki"] += len(wpisy_rozmiary)
    if budzet["pliki"] > L["pliki"]:
        raise LimitArchiwum(f"archiwum zawiera więcej niż {L['pliki']} plików – rozpakuj je na komputerze i wgraj potrzebne pliki.")
    suma = sum(max(0, int(r or 0)) for r in wpisy_rozmiary)
    if budzet["bajty"] + suma > L["bajty"]:
        raise LimitArchiwum(f"archiwum po rozpakowaniu przekracza {_mb(L['bajty'])} – rozpakuj je na komputerze i wgraj potrzebne pliki.")
    if suma > L["wspolczynnik_od"] and suma > L["wspolczynnik"] * max(1, rozmiar_archiwum):
        raise LimitArchiwum(f"nietypowo duży współczynnik kompresji (ponad {L['wspolczynnik']}:1) – archiwum może być „bombą” zapełniającą dysk; "
                            "rozpakuj je na komputerze i wgraj potrzebne pliki.")


def _dolicz(budzet, n):
    budzet["bajty"] += n
    if budzet["bajty"] > budzet["limity"]["bajty"]:
        raise LimitArchiwum(f"archiwum po rozpakowaniu przekracza {_mb(budzet['limity']['bajty'])} – rozpakuj je na komputerze i wgraj potrzebne pliki.")


def _polski_blad(e):
    """Komunikat po polsku dla wyjątku z zipfile / py7zr / systemu plików."""
    if isinstance(e, BladArchiwum):
        return str(e)
    t = f"{type(e).__name__}: {e}".lower()
    if "password" in t or "encrypt" in t:
        return "archiwum jest zabezpieczone hasłem – rozpakuj je na komputerze i wgraj pliki."
    if "symlink" in t or "path is bad" in t or "absolutepath" in t or "out of target" in t:
        return "archiwum zawiera niebezpieczne ścieżki lub dowiązania – rozpakuj je na komputerze i wgraj pliki."
    if "unsupported" in t or isinstance(e, NotImplementedError):
        return "archiwum używa nieobsługiwanej metody kompresji – rozpakuj je na komputerze i wgraj pliki."
    if "bomb" in t or "exceeds limit" in t:
        return f"archiwum po rozpakowaniu przekracza {_mb(LIMITY_ARCHIWUM['bajty'])} – rozpakuj je na komputerze i wgraj potrzebne pliki."
    if isinstance(e, OSError) and getattr(e, "errno", None) == 28:
        return "brak miejsca na dysku serwera – archiwum nie zostało rozpakowane."
    return "archiwum jest uszkodzone lub niepełne i nie da się go rozpakować – rozpakuj je na komputerze (albo pobierz ponownie) i wgraj pliki."


def _rozpakuj_7z(sciezka, cel, glebokosc=0, budzet=None):
    """Archiwum 7z (np. „SWZ+ załączniki.7z” z platformazakupowa.pl) – te same zasady co ZIP: bez plików systemowych, bez podwójnego folderu."""
    try:
        import py7zr
    except ImportError:
        raise BladArchiwum("archiwum 7z – brak modułu py7zr na serwerze (requirements.txt); rozpakuj archiwum na komputerze i wgraj pliki.")
    pliki = []
    try:  # py7zr ≥ 1.0 sam przerywa rozpakowanie po przekroczeniu rozmiaru
        z7 = py7zr.SevenZipFile(sciezka, mode="r", max_extract_size=max(1, budzet["limity"]["bajty"] - budzet["bajty"]))
    except TypeError:
        z7 = py7zr.SevenZipFile(sciezka, mode="r")
    with z7 as z:
        info_ =[i for i in z.list() if not i.is_directory]
        wpisy = [(i.filename.replace("\\", "/"), i) for i in info_]
        wpisy = [(n, i) for n, i in wpisy if not re.search(_PLIKI_SYSTEMOWE, n)]
        for n, _ in wpisy:
            if czy_wykonywalny(n):
                budzet["uwagi"].append(f"pominięto program „{os.path.basename(n)}” (pliki wykonywalne nie są wgrywane)")
        wpisy = [(n, i) for n, i in wpisy if not czy_wykonywalny(n)]
        _sprawdz_limity(budzet, [i.uncompressed for _, i in wpisy], os.path.getsize(sciezka), glebokosc)
        wpisy = [n for n, _ in wpisy]
        tmp = tempfile.mkdtemp(prefix="7z_")
        try:
            try:
                z.reset()
            except Exception:
                pass
            z.extract(path=tmp, targets=wpisy)
            gl = {n.split("/", 1)[0] for n in wpisy if "/" in n}
            zdejmij = len(gl) == 1 and all("/" in n for n in wpisy) and next(iter(gl)).strip().lower() == os.path.basename(os.path.normpath(cel)).strip().lower()
            for nazwa in wpisy:
                zrodlo = os.path.join(tmp, nazwa)
                if os.path.islink(zrodlo) or not os.path.isfile(zrodlo):
                    continue
                _dolicz(budzet, os.path.getsize(zrodlo))  # faktyczny rozmiar (deklarowany mógł być fałszywy)
                if zdejmij:
                    nazwa = nazwa.split("/", 1)[1]
                czysta = os.path.normpath(nazwa).lstrip(os.sep).replace("..", "_")
                docel = os.path.join(cel, czysta)
                os.makedirs(os.path.dirname(docel), exist_ok=True)
                shutil.move(zrodlo, docel)
                budzet["utworzone"].append(docel)
                pliki += _zagniezdzone(docel, glebokosc, budzet)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return pliki


def _zagniezdzone(docel, glebokosc, budzet):
    """Plik z archiwum: archiwum wewnętrzne rozpakowane do folderu i usunięte (uszkodzone – zostaje, pominięte z uwagą)."""
    if not czy_archiwum(docel):
        return [docel]
    try:
        wew = _rozpakuj(docel, os.path.splitext(docel)[0], glebokosc + 1, budzet)
    except LimitArchiwum:
        raise
    except Exception as e:
        budzet["uwagi"].append(f"{os.path.basename(docel)}: {_polski_blad(e)}")
        budzet["nierozpakowane"].append(docel)
        return [docel]
    try:
        os.remove(docel)
        budzet["utworzone"].remove(docel)
    except (OSError, ValueError):
        pass
    return wew


def _rozpakuj(sciezka, cel, glebokosc, budzet):
    with open(sciezka, "rb") as f_:
        if f_.read(6) == b"7z\xbc\xaf\x27\x1c":
            return _rozpakuj_7z(sciezka, cel, glebokosc, budzet)
    pliki = []
    with zipfile.ZipFile(sciezka) as z:
        def _nazwa(info):
            n = info.filename
            if not (info.flag_bits & 0x800):
                try:
                    surowe = n.encode("cp437")
                except UnicodeEncodeError:
                    surowe = None
                if surowe is not None:
                    try:
                        n = surowe.decode("utf-8")  # macOS „Kompresuj”: UTF-8 bez flagi
                    except UnicodeDecodeError:
                        try:
                            n = surowe.decode("cp852")  # Eksplorator Windows (polska strona kodowa)
                        except UnicodeDecodeError:
                            pass  # zostaje cp437
            return n.replace("\\", "/")
        wpisy = [(i, _nazwa(i)) for i in z.infolist() if not i.is_dir()]
        # pliki systemowe (Thumbs.db, .DS_Store, desktop.ini, __MACOSX) – nie są dokumentacją
        wpisy = [(i, n) for i, n in wpisy if not re.search(_PLIKI_SYSTEMOWE, n)]
        for _, n in wpisy:
            if czy_wykonywalny(n):
                budzet["uwagi"].append(f"pominięto program „{os.path.basename(n)}” (pliki wykonywalne nie są wgrywane)")
        wpisy = [(i, n) for i, n in wpisy if not czy_wykonywalny(n)]
        _sprawdz_limity(budzet, [i.file_size for i, _ in wpisy], os.path.getsize(sciezka), glebokosc)
        # archiwum z jednym folderem o tej samej nazwie co folder docelowy – bez podwójnego folderu
        gl = {n.split("/", 1)[0] for _, n in wpisy if "/" in n}
        zdejmij = len(gl) == 1 and all("/" in n for _, n in wpisy) and next(iter(gl)).strip().lower() == os.path.basename(os.path.normpath(cel)).strip().lower()
        for info, nazwa in wpisy:
            if zdejmij:
                nazwa = nazwa.split("/", 1)[1]
            czysta = os.path.normpath(nazwa).lstrip(os.sep).replace("..", "_")
            docel = os.path.join(cel, czysta)
            os.makedirs(os.path.dirname(docel), exist_ok=True)
            budzet["utworzone"].append(docel)
            with z.open(info) as zr, open(docel, "wb") as zw:
                while True:  # kopiowanie z licznikiem faktycznie zapisanych bajtów (deklarowany rozmiar można sfałszować)
                    blok = zr.read(1 << 20)
                    if not blok:
                        break
                    _dolicz(budzet, len(blok))
                    zw.write(blok)
            pliki += _zagniezdzone(docel, glebokosc, budzet)
    return pliki


def rozpakuj_zip(sciezka, cel, glebokosc=0, uwagi=None, limity=None):
    """Rozpakowuje archiwum ZIP albo 7z (także zagnieżdżone) do folderu cel. Zwraca listę plików.
    Limity (LIMITY_ARCHIWUM) liczone łącznie z archiwami wewnętrznymi; po przekroczeniu albo przy uszkodzonym archiwum – BladArchiwum
    z komunikatem po polsku i usunięcie częściowo rozpakowanych plików. Uwagi (pominięte programy, uszkodzone archiwa wewnętrzne) – do listy uwagi."""
    budzet = {"bajty": 0, "pliki": 0, "limity": {**LIMITY_ARCHIWUM, **(limity or {})}, "utworzone": [], "uwagi": [], "nierozpakowane": []}
    try:
        wyn = _rozpakuj(sciezka, cel, glebokosc, budzet)
    except Exception as e:
        for p in reversed(budzet["utworzone"]):
            try:
                os.remove(p)
            except OSError:
                pass
        for r, ds, _ in sorted(os.walk(cel), key=lambda x: -len(x[0])) if os.path.isdir(cel) else []:
            try:
                os.rmdir(r)  # tylko puste foldery
            except OSError:
                pass
        if isinstance(e, BladArchiwum):
            raise
        raise BladArchiwum(_polski_blad(e)) from e
    if uwagi is not None:
        uwagi += budzet["uwagi"]
    return wyn


def rozpoznaj_typ(sciezka):
    """Rozpoznaje rodzaj pliku po zawartości (a nie po nazwie) – np. „Zapytanie 24.09.2024r_pdf” to PDF.
    Zwraca rozszerzenie (.pdf, .docx, .xlsx, .doc, .zip, .jpg, .png, .gif, .webp, .txt) albo None."""
    try:
        with open(sciezka, "rb") as f:
            p = f.read(8192)
    except OSError:
        return None
    if p.startswith(b"%PDF"):
        return ".pdf"
    # sygnatury archiwów najpierw: w ZIP bez kompresji (albo 7z z małym PDF) „%PDF-” jest w pierwszych bajtach, a to nadal archiwum
    if p.startswith(b"7z\xbc\xaf\x27\x1c"):
        return ".7z"
    if p.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return ".xls" if b"W\x00o\x00r\x00k\x00b\x00o\x00o\x00k" in p else ".doc"
    if p.startswith(b"PK\x03\x04"):
        try:
            import zipfile
            with zipfile.ZipFile(sciezka) as z:
                nazwy = z.namelist()
            if any(n.startswith("word/") for n in nazwy):
                return ".docx"
            if any(n.startswith("xl/") for n in nazwy):
                return ".xlsx"
            if any(n.startswith("ppt/") for n in nazwy):
                return ".pptx"
            return ".zip"
        except Exception:
            return ".zip"
    if p.startswith(b"Rar!"):
        return ".rar"
    if b"%PDF-" in p[:1024]:  # PDF z kilkoma bajtami przed nagłówkiem (np. z poczty / platformy)
        return ".pdf"
    if p.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if p.startswith(b"\x89PNG"):
        return ".png"
    if p[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if p[:4] == b"RIFF" and p[8:12] == b"WEBP":
        return ".webp"
    if p.startswith(b"Rar!"):
        return ".rar"
    if p.startswith(b"7z\xbc\xaf"):
        return ".7z"
    if p.startswith(b"{\\rtf"):
        return ".rtf"
    try:
        p.decode("utf-8")
        return ".txt" if p.strip() else None
    except UnicodeDecodeError:
        return None


ZNANE_ROZSZ = (".pdf", ".docx", ".doc", ".xlsx", ".xlsm", ".xls", ".zip", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".txt", ".csv",
               ".rtf", ".rar", ".7z", ".pptx", ".dwg", ".ath", ".odt", ".ods", ".xml", ".md")


def popraw_rozszerzenie(sciezka):
    """Nadaje plikowi właściwą końcówkę, gdy nazwa jej nie ma albo jest zniekształcona (np. „…2024r_pdf” → „…2024r.pdf”).
    Zwraca nową ścieżkę."""
    katalog, nazwa = os.path.split(sciezka)
    rozsz = os.path.splitext(nazwa)[1].lower()
    if rozsz in ARCHIWA and rozpoznaj_typ(sciezka) in (".zip", ".7z", ".docx", ".xlsx", ".pptx"):
        return sciezka  # archiwum zostaje archiwum (rozpakowanie rozpoznaje ZIP/7z po sygnaturze)
    if rozsz in ZNANE_ROZSZ and rozpoznaj_typ(sciezka) in (rozsz, None, ".txt") or rozsz in (".dwg", ".ath", ".xml", ".csv", ".md"):
        return sciezka
    typ = rozpoznaj_typ(sciezka)
    if not typ or typ == ".txt" and rozsz in ZNANE_ROZSZ:
        return sciezka
    baza = re.sub(r"[ _.-]?(pdf|docx?|xlsx?|zip|jpe?g|png)$", "", nazwa, flags=re.I) if rozsz not in ZNANE_ROZSZ else os.path.splitext(nazwa)[0]
    nowa = os.path.join(katalog, (baza or "dokument") + typ)
    i = 2
    while os.path.exists(nowa) and os.path.abspath(nowa) != os.path.abspath(sciezka):
        nowa = os.path.join(katalog, f"{baza}_{i}{typ}")
        i += 1
    os.replace(sciezka, nowa)
    return nowa


PDF_JAKO_TEKST = {"wlaczone": True, "min_znakow_na_strone": 500}


def tekst_pdf(sciezka):
    """Tekst PDF ze znacznikami stron albo '' – gdy to skan lub rysunek (mało tekstu na stronę), zostaje wysłany jako PDF."""
    try:
        import logging
        import pypdf
        logging.getLogger("pypdf").setLevel(logging.ERROR)
        r = pypdf.PdfReader(sciezka)
        strony = [(s.extract_text() or "").strip() for s in r.pages]
    except Exception:
        return ""
    if not strony:
        return ""
    znaki = sum(len(s) for s in strony)
    pelne = sum(1 for s in strony if len(s) >= 200)
    if znaki / len(strony) < PDF_JAKO_TEKST["min_znakow_na_strone"] or pelne < 0.7 * len(strony):
        return ""
    return "\n\n".join(f"[strona {i}]\n{s}" for i, s in enumerate(strony, 1))


MAKS_OBRAZ_PX = 2000          # dłuższy bok obrazu wysyłanego do AI (rysunki pozostają czytelne)
MAKS_OBRAZ_BAJTY = 3_700_000  # limit API to ok. 5 MB po zakodowaniu base64 (×4/3)


def obraz_dla_ai(sciezka, typ):
    """Obraz w granicach limitów API: duże zdjęcia i skany rysunków są zmniejszane (wcześniej 20-megabajtowy JPG przerywał cały odczyt)."""
    dane = open(sciezka, "rb").read()
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 400_000_000
        with Image.open(sciezka) as im:
            w0, h0 = im.size
            if len(dane) <= MAKS_OBRAZ_BAJTY and max(w0, h0) <= 8000:
                return dane, typ, ""
            if im.format == "JPEG":
                im.draft("RGB", (MAKS_OBRAZ_PX, MAKS_OBRAZ_PX))  # dekodowanie w zmniejszonej skali – mało pamięci
            im = im.convert("RGB")
            im.thumbnail((MAKS_OBRAZ_PX, MAKS_OBRAZ_PX))
            for jakosc in (88, 80, 70, 60):
                bufor = io.BytesIO()
                im.save(bufor, "JPEG", quality=jakosc, optimize=True)
                if bufor.tell() <= MAKS_OBRAZ_BAJTY:
                    break
            return bufor.getvalue(), "image/jpeg", f" – zmniejszony z {w0}×{h0} do {im.size[0]}×{im.size[1]} px; drobne napisy sprawdź w oryginale"
    except Exception:
        return dane, typ, ""


def przygotuj_blok(sciezka):
    """Zwraca (bloki_content, bajty, ostrzeżenie) dla jednego pliku."""
    nazwa = os.path.basename(sciezka)
    rozsz = os.path.splitext(nazwa)[1].lower()
    if rozsz not in ROZSZ_PDF and rozsz not in ROZSZ_OBRAZ and rozsz not in (".docx", ".doc", ".xlsx", ".xlsm") and rozsz not in ROZSZ_TEKST:
        rozsz = rozpoznaj_typ(sciezka) or rozsz  # format po zawartości, gdy nazwa ma złą końcówkę
    try:
        if rozsz in ROZSZ_PDF:
            dane = open(sciezka, "rb").read()
            if PDF_JAKO_TEKST["wlaczone"]:
                t = tekst_pdf(sciezka)
                if t:  # PDF z warstwą tekstową: tekst zamiast obrazu stron – kilkukrotnie mniej tokenów
                    return [{"type": "document", "title": nazwa,
                             "source": {"type": "text", "media_type": "text/plain", "data": t}}], len(t.encode()), ""
            return [{"type": "document", "title": nazwa,
                     "source": {"type": "base64", "media_type": "application/pdf",
                                "data": base64.b64encode(dane).decode()}}], len(dane) * 4 // 3, ""
        if rozsz in ROZSZ_OBRAZ:
            dane, typ, uwaga = obraz_dla_ai(sciezka, ROZSZ_OBRAZ[rozsz])
            return [{"type": "text", "text": f"[Obraz: {nazwa}{uwaga}]"},
                    {"type": "image", "source": {"type": "base64", "media_type": typ,
                                                 "data": base64.b64encode(dane).decode()}}], len(dane) * 4 // 3, ""
        if rozsz == ".docx":
            t = tekst_docx(sciezka)
        elif rozsz == ".doc":
            t = tekst_doc(sciezka)
            if t.strip():
                t = "[Tekst odczytany ze starego formatu Word .doc – układ tabel mógł zostać uproszczony]\n" + t
        elif rozsz in (".xlsx", ".xlsm"):
            t = tekst_xlsx(sciezka)
        elif rozsz in ROZSZ_TEKST:
            with open(sciezka, "rb") as f:
                poczatek = f.read(4096)
            if b"\x00" in poczatek:  # plik binarny (np. rysunek DWG) – nie wysyłamy śmieci jako tekstu
                return [], 0, f"{nazwa}: plik binarny ({os.path.splitext(nazwa)[1] or 'bez rozszerzenia'}) – program go nie odczyta; zapisz rysunek jako PDF"
            t = open(sciezka, encoding="utf-8", errors="replace").read()
        else:
            return [], 0, f"{nazwa}: nieobsługiwany format ({rozsz}) – zapisz jako PDF, DOC/DOCX lub XLSX"
        if not t.strip():
            return [], 0, f"{nazwa}: brak tekstu"
        return [{"type": "document", "title": nazwa,
                 "source": {"type": "text", "media_type": "text/plain", "data": t}}], len(t.encode()), ""
    except Exception as e:
        return [], 0, f"{nazwa}: nie udało się odczytać ({e})"


RE_RYSUNEK = re.compile(r"(?i)(^|[\W_])(rys|rysunek|rysunki|pzt|plan[\W_]|rzut|przekr[oó]j|elewacj|schemat|detal|aksonometr|zestawienie[\W_]stolarki|dwg)")


def pdf_bez_tekstu(sciezka):
    try:
        return not (tekst_pdf(sciezka) or "").strip()
    except Exception:
        return False


def przygotuj_blok_tekstowy(sciezka, max_stron_skanu=30):
    """Dokument do zadań tekstowych (wykrywanie błędów, SWZ, asystent, analizy): rysunki (PDF bez tekstu, nazwa jak rysunek)
    są pomijane, a długie skany ograniczone do pierwszych stron – obraz strony kosztuje ok. 1,5 tys. tokenów."""
    nazwa = os.path.basename(sciezka)
    if os.path.splitext(nazwa)[1].lower() in ROZSZ_PDF and PDF_JAKO_TEKST["wlaczone"] and POMIJAJ_RYSUNKI["wlaczone"] and pdf_bez_tekstu(sciezka):
        if RE_RYSUNEK.search(os.path.splitext(nazwa)[0]):
            return [], 0, f"{nazwa}: rysunek (PDF bez tekstu) – pominięty w tym zadaniu"
        try:
            import pypdf
            r = pypdf.PdfReader(sciezka)
            if len(r.pages) > max_stron_skanu:
                w = pypdf.PdfWriter()
                for p in r.pages[:max_stron_skanu]:
                    w.add_page(p)
                import io
                b = io.BytesIO()
                w.write(b)
                dane = b.getvalue()
                return [{"type": "document", "title": f"{nazwa} (pierwsze {max_stron_skanu} z {len(r.pages)} stron skanu)",
                         "source": {"type": "base64", "media_type": "application/pdf", "data": base64.b64encode(dane).decode()}}], \
                    len(dane) * 4 // 3, f"{nazwa}: skan {len(r.pages)} stron – do AI pierwsze {max_stron_skanu}"
        except Exception:
            pass
    return przygotuj_blok(sciezka)


POMIJAJ_RYSUNKI = {"wlaczone": True}


def szacuj_tokeny(sciezka):
    """Szacunkowa liczba tokenów dokumentu wysłanego do AI (tekst ~3,5 znaku na token, strona skanu / rysunku ~1 500 tokenów)."""
    rozsz = os.path.splitext(sciezka)[1].lower()
    try:
        if rozsz in ROZSZ_PDF:
            t = tekst_pdf(sciezka) if PDF_JAKO_TEKST["wlaczone"] else ""
            if t and t.strip():
                return int(len(t) / 3.5), "tekst"
            import pypdf
            n = len(pypdf.PdfReader(sciezka).pages)
            return n * 1500, "rysunek" if RE_RYSUNEK.search(os.path.basename(sciezka)) else "skan"
        if rozsz in ROZSZ_OBRAZ:
            return 1500, "obraz"
        return int(os.path.getsize(sciezka) / 6), "tekst"
    except Exception:
        return 0, "?"


# ============================================================ połączenie z API (klucze, ponawianie, komunikaty)

class BladAI(RuntimeError):
    """Błąd połączenia z AI z czytelnym komunikatem po polsku."""


PRZEJSCIOWE = (408, 429, 500, 502, 503, 504, 529)


ODRZUCONE_KLUCZE = {}  # skrót klucza → czas odrzucenia (401/403); taki klucz idzie na koniec kolejki przez CZAS_ODRZUCENIA
CZAS_ODRZUCENIA = 6 * 3600


def _skrot_klucza(k):
    import hashlib
    return hashlib.sha256((k or "").encode()).hexdigest()[:16]


def klucz_odrzucony(k):
    t = ODRZUCONE_KLUCZE.get(_skrot_klucza(k))
    return bool(t and time.time() - t < CZAS_ODRZUCENIA)


def klucze_api(cfg):
    """Klucz z Ustawień i klucz z Rendera (ANTHROPIC_API_KEY) – bez powtórzeń, najpierw główny.
    Klucz niedawno odrzucony przez API (nieważny) idzie na koniec – kolejne zapytania nie tracą czasu na pewny błąd."""
    wyn = []
    for k in (cfg.get("api_key"), cfg.get("api_key_alt")):
        k = (k or "").strip()
        if k and k not in wyn:
            wyn.append(k)
    return sorted(wyn, key=klucz_odrzucony)


def odrzucone_klucze(cfg):
    """Źródła kluczy odrzuconych przez API w ostatnich godzinach (bez ujawniania kluczy) – do ostrzeżenia w programie."""
    return [z for z, k in (("Ustawienia", cfg.get("api_key_ustawienia")), ("Render (ANTHROPIC_API_KEY)", cfg.get("api_key_render")))
            if (k or "").strip() and klucz_odrzucony(k.strip())]


def opis_bledu(kod, tresc):
    t = (tresc or "").lower()
    if kod == 401 or "invalid x-api-key" in t or "authentication_error" in t:
        return ("Klucz API został odrzucony (nieprawidłowy lub wyłączony). Wpisz aktualny klucz z console.anthropic.com "
                "w Ustawieniach (pole „Klucz API Claude”) i/lub w Renderze (ANTHROPIC_API_KEY).")
    if "credential" in t:
        return ("Serwer AI nie potwierdził klucza API (błąd 503 „credential validation failed”). Najczęściej oznacza to stary, "
                "wyłączony klucz w Ustawieniach albo chwilową awarię po stronie Anthropic. Sprawdź klucz przyciskiem "
                "„Test połączenia z AI” w Ustawieniach i spróbuj ponownie za kilka minut.")
    if kod == 403:
        return "Klucz API nie ma uprawnień do tej operacji (403) – sprawdź klucz i obszar roboczy w console.anthropic.com."
    if "credit balance" in t or "billing" in t:
        return "Brak środków na koncie Anthropic – doładuj konto w console.anthropic.com (Billing)."
    if kod == 404 and "model" in t:
        return "Nieznany model AI – sprawdź pole „Model Claude” w Ustawieniach."
    if "prompt is too long" in t:
        return "Dokumenty mają za dużo treści dla AI (limit tokenów modelu) – pomiń rysunki i duże skany w kroku 1 (Uwzględnij/pomiń)."
    if kod == 413 or "too large" in t:
        return "Dokumenty są zbyt duże dla jednego zapytania (limit 50 MB) – pomiń rysunki i duże skany w kroku 1 (Uwzględnij/pomiń)."
    if kod == 429:
        return "Przekroczono limit zapytań do AI – spróbuj ponownie za minutę."
    if kod in (500, 502, 503, 504, 529) or "overloaded" in t:
        return f"Serwer AI jest chwilowo przeciążony lub niedostępny (błąd {kod}) – spróbuj ponownie za kilka minut."
    return f"Błąd AI {kod}: {(tresc or '')[:300]}"


# Modele zastępcze: gdy nowszy (tańszy) model nie jest dostępny dla klucza API, program przełącza się na sprawdzony.
ZAPASOWE_MODELE = {"claude-haiku-5-5": "claude-sonnet-5", "claude-sonnet-5-5": "claude-sonnet-5", "claude-opus-5-5": "claude-sonnet-5"}
NIEDOSTEPNE_MODELE = set()

# Ceny modeli [USD za 1 mln tokenów]: wejście, wyjście, zapis 5 min, zapis 1 h, odczyt z pamięci (cennik API, 10.2026)
CENY_MODELI = {"claude-opus-5-5": (4, 20, 5, 8, 0.20), "claude-sonnet-5-5": (2, 10, 2.5, 4, 0.10), "claude-sonnet-5": (2, 10, 2.5, 4, 0.20),
               "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.20, 0.01)}


def koszt_usd(model, u):
    """Koszt jednego zapytania w USD na podstawie pola usage z odpowiedzi API."""
    if not u:
        return 0.0
    c = CENY_MODELI.get(model, CENY_MODELI["claude-opus-5-5"])
    wej, wyj = u.get("input_tokens") or 0, u.get("output_tokens") or 0
    odc = u.get("cache_read_input_tokens") or 0
    cc = u.get("cache_creation") or {}
    z1h = cc.get("ephemeral_1h_input_tokens") or 0
    z5 = (u.get("cache_creation_input_tokens") or 0) - z1h
    if model == "claude-haiku-5-5" and wej + odc + z5 + z1h > 100000:  # Haiku 5.5: wyższe ceny dla długich zapytań
        c = (0.5, 2.5, 0.625, 1.0, 0.05)
    szuk = ((u.get("server_tool_use") or {}).get("web_search_requests") or 0) * 0.01
    return (wej * c[0] + wyj * c[1] + z5 * c[2] + z1h * c[3] + odc * c[4]) / 1e6 + szuk


def zapisz_uzycie(cfg, model, u):
    """Przekazuje zużycie do licznika programu (konto, miesiąc) – jeśli serwer go podłączył."""
    f = cfg.get("_licznik") if isinstance(cfg, dict) else None
    if f and u:
        try:
            f(model, u, koszt_usd(model, u))
        except Exception:
            pass


LIMIT_ZAPYTANIA_API = 30 * 1024 * 1024  # API przyjmuje do 32 MB w jednym zapytaniu – zapas na treść poleceń
FILES_BETA = "files-api-2025-04-14"


def _wyslij_plik_api(klucz, dane, nazwa, typ):
    """Wysyła plik do Files API (Anthropic) i zwraca file_id. Plik w zapytaniu nie liczy się do limitu 32 MB."""
    granica = "----bidivia" + os.urandom(8).hex()
    nazwa = re.sub(r'[\r\n"]', "_", nazwa or "plik")
    body = (f'--{granica}\r\nContent-Disposition: form-data; name="file"; filename="{nazwa}"\r\n'
            f"Content-Type: {typ}\r\n\r\n").encode("utf-8") + dane + f"\r\n--{granica}--\r\n".encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/files", data=body, method="POST", headers={
        "x-api-key": klucz, "anthropic-version": "2023-06-01", "anthropic-beta": FILES_BETA,
        "content-type": f"multipart/form-data; boundary={granica}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode())["id"]


def _usun_pliki_api(klucz, ids, po_sekundach=3600):
    """Pliki wysłane na potrzeby jednego zadania są usuwane z konta Anthropic po godzinie (zadanie zdąży je przeczytać)."""
    def usun():
        for fid in ids:
            try:
                urllib.request.urlopen(urllib.request.Request(f"https://api.anthropic.com/v1/files/{fid}", method="DELETE", headers={
                    "x-api-key": klucz, "anthropic-version": "2023-06-01", "anthropic-beta": FILES_BETA}), timeout=60).close()
            except Exception:
                pass
    tm = threading.Timer(po_sekundach, usun)
    tm.daemon = True
    tm.start()


def _odciaz_zapytanie(dane, klucz, log=None):
    """Zapytanie większe niż limit API: największe pliki (PDF, obrazy w base64) idą przez Files API, a w zapytaniu zostaje
    tylko ich identyfikator. Zwraca (nowe_dane, lista_file_id). Mniejsze zapytania zostają bez zmian."""
    body_len = len(json.dumps(dane).encode("utf-8"))
    if body_len <= LIMIT_ZAPYTANIA_API:
        return dane, []
    dane = json.loads(json.dumps(dane))  # kopia – oryginalne bloki zostają do ponowień z innym kluczem
    bloki = []
    for w in dane.get("messages") or []:
        if isinstance(w.get("content"), list):
            for b in w["content"]:
                s = b.get("source") if isinstance(b, dict) else None
                if b.get("type") in ("document", "image") and isinstance(s, dict) and s.get("type") == "base64":
                    bloki.append(b)
    bloki.sort(key=lambda b: -len(b["source"].get("data") or ""))
    ids = []
    for i, b in enumerate(bloki):
        if body_len <= LIMIT_ZAPYTANIA_API:
            break
        s = b["source"]
        surowe = base64.b64decode(s["data"])
        typ = s.get("media_type") or "application/octet-stream"
        nazwa = (b.get("title") or f"plik_{i + 1}") + ("" if "." in (b.get("title") or "")[-6:] else (".pdf" if typ == "application/pdf" else ""))
        fid = _wyslij_plik_api(klucz, surowe, nazwa, typ)
        ids.append(fid)
        body_len -= len(s["data"])
        b["source"] = {"type": "file", "file_id": fid}
    if log and ids:
        log(f"Duże dokumenty ponad limit jednego zapytania (liczba: {len(ids)}) wysłane do AI osobno, przez Files API.")
    return dane, ids


def otworz_api(cfg, dane, timeout=900, stream=False, log=None):
    """Wysyła zapytanie do API: ponawia przy chwilowych błędach (503, 529…), a przy odrzuconym kluczu
    próbuje drugiego klucza (Ustawienia / Render). Zwraca otwartą odpowiedź. Błąd 400 zwraca jako HTTPError
    (obsługa zgodności wstecznej wyżej), pozostałe jako BladAI z komunikatem po polsku."""
    if callable(cfg.get("_limit")):  # miesięczny limit kosztów AI konta – przed wysłaniem zapytania
        cfg["_limit"]()
    if dane.get("model") in NIEDOSTEPNE_MODELE:
        dane = dict(dane, model=ZAPASOWE_MODELE[dane["model"]])
    klucze = klucze_api(cfg)
    if not klucze:
        raise BladAI("Brak klucza API – wpisz klucz z console.anthropic.com w Ustawieniach (pole „Klucz API Claude”).")
    ostatni = None
    for ki, klucz in enumerate(klucze):
        try:  # ponad 32 MB: największe pliki osobno przez Files API (pliki należą do konta danego klucza)
            dane_k, pliki_api = _odciaz_zapytanie(dane, klucz, log)
        except urllib.error.HTTPError as e:
            tresc = e.read().decode("utf-8", "ignore")
            if e.code in (401, 403):
                ODRZUCONE_KLUCZE[_skrot_klucza(klucz)] = time.time()
            if e.code in (401, 403) and ki + 1 < len(klucze):
                continue
            raise BladAI(opis_bledu(e.code, tresc))
        except urllib.error.URLError as e:
            raise BladAI(f"Brak połączenia z serwerem AI ({e.reason}).")
        if pliki_api:
            _usun_pliki_api(klucz, pliki_api)
        body = json.dumps(dane_k).encode("utf-8")
        nagl = {"x-api-key": klucz, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        if pliki_api:
            nagl["anthropic-beta"] = FILES_BETA
        for proba in range(3):
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST", headers=nagl)
            try:
                return urllib.request.urlopen(req, timeout=timeout)
            except urllib.error.HTTPError as e:
                tresc = e.read().decode("utf-8", "ignore")
                if e.code in (400, 404) and "model" in tresc.lower() and dane.get("model") in ZAPASOWE_MODELE \
                        and ("not_found" in tresc.lower() or "not found" in tresc.lower() or "invalid model" in tresc.lower()):
                    NIEDOSTEPNE_MODELE.add(dane["model"])  # model niedostępny dla tego klucza – zapasowy do końca działania serwera
                    if log:
                        log(f"Model {dane['model']} niedostępny – używam {ZAPASOWE_MODELE[dane['model']]}.")
                    return otworz_api(cfg, dict(dane, model=ZAPASOWE_MODELE[dane["model"]]), timeout, stream, log)
                if e.code == 400:
                    raise urllib.error.HTTPError(e.url, e.code, tresc[:500] or e.reason, e.headers, io.BytesIO(tresc.encode("utf-8")))
                ostatni = (e.code, tresc)
                klucz_zly = e.code in (401, 403)  # klucz naprawdę odrzucony – od razu drugi klucz
                # 5xx „credential validation failed” to zwykle chwilowa awaria po stronie Anthropic przy dobrym kluczu:
                # najpierw ponowienie tym samym kluczem, dopiero potem drugi klucz
                chwilowy_klucz = not klucz_zly and ("credential" in tresc.lower() or "authentication" in tresc.lower())
                if klucz_zly:
                    ODRZUCONE_KLUCZE[_skrot_klucza(klucz)] = time.time()
                if klucz_zly and ki + 1 < len(klucze):
                    if log:
                        log("Klucz API odrzucony – używam drugiego klucza (z Rendera / Ustawień); kolejne zadania od razu drugim kluczem. "
                            "Wymień nieważny klucz w Ustawieniach („Test połączenia z AI”).")
                    break
                if chwilowy_klucz and proba < 2:
                    czekaj = (5, 20)[proba]
                    if log:
                        log(f"Serwer AI chwilowo nie potwierdził klucza (błąd {e.code}) – ponawiam tym samym kluczem za {czekaj} s…")
                    time.sleep(czekaj)
                    continue
                if chwilowy_klucz and ki + 1 < len(klucze):
                    if log:
                        log("Klucz nadal niepotwierdzony – próbuję drugiego klucza (z Rendera / Ustawień)…")
                    break
                if e.code in PRZEJSCIOWE and proba < 2:
                    czekaj = (3, 10)[proba]
                    if log:
                        log(f"Serwer AI odpowiedział błędem {e.code} – ponawiam za {czekaj} s…")
                    time.sleep(czekaj)
                    continue
                raise BladAI(opis_bledu(e.code, tresc))
            except urllib.error.URLError as e:
                ostatni = (0, str(e.reason))
                if proba < 2:
                    time.sleep((3, 10)[proba])
                    continue
                raise BladAI(f"Brak połączenia z serwerem AI ({e.reason}).")
    raise BladAI(opis_bledu(*(ostatni or (0, ""))))


def test_ai(cfg):
    """Krótkie zapytanie sprawdzające każdy klucz. Zwraca listę wyników."""
    wyn = []
    for zrodlo, k in (("Ustawienia", cfg.get("api_key_ustawienia")), ("Render (ANTHROPIC_API_KEY)", cfg.get("api_key_render"))):
        k = (k or "").strip()
        if not k:
            wyn.append({"zrodlo": zrodlo, "klucz": "brak", "ok": None, "opis": "nie ustawiono"})
            continue
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST", headers={
            "x-api-key": k, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            data=json.dumps({"model": cfg.get("model") or "claude-sonnet-5", "max_tokens": 5,
                             "messages": [{"role": "user", "content": "Odpowiedz: OK"}]}).encode())
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                json.loads(r.read().decode())
            wyn.append({"zrodlo": zrodlo, "klucz": "…" + k[-4:], "ok": True, "opis": "działa"})
        except urllib.error.HTTPError as e:
            wyn.append({"zrodlo": zrodlo, "klucz": "…" + k[-4:], "ok": False, "opis": opis_bledu(e.code, e.read().decode("utf-8", "ignore"))})
        except Exception as e:
            wyn.append({"zrodlo": zrodlo, "klucz": "…" + k[-4:], "ok": False, "opis": f"brak połączenia ({e})"})
    return wyn


def test_cache(cfg, klucz=None):
    """Czy pamięć podręczna AI działa: to samo zapytanie (ok. 6 tys. tokenów stałej treści) wysłane dwa razy – przy drugim
    API powinno odczytać treść z pamięci. Sprawdza ustawiony czas pamięci (1 godzina / 5 minut), a gdy nie działa – także drugi.
    Koszt: kilka groszy. Wynik: {"ok", "opis", "proby": [...]}."""
    klucze = [klucz] if klucz else [k for k in klucze_api(cfg) if not klucz_odrzucony(k)] or klucze_api(cfg)
    if not klucze:
        return {"ok": None, "opis": "brak klucza", "proby": []}
    model = cfg.get("model_oferty") or "claude-sonnet-5-5"
    stala = ("Tekst testowy pamięci podręcznej Bidivia. " + " ".join(f"Akapit {i}: zamawiający, wykonawca, kosztorys, przedmiar, oferta, termin, umowa." for i in range(700)))
    tryby = [str(cfg.get("cache_ai", "5m")).strip().lower()]
    tryby += [t for t in ("1h", "5m") if t not in tryby]
    proby = []
    for tryb in tryby[:2]:
        cc = {"type": "ephemeral", "ttl": "1h"} if tryb in ("1h", "60m") else {"type": "ephemeral"}
        znacznik = f"[{tryb} {time.time():.0f}] "  # inna treść przy każdym teście – pierwszy zapis zawsze nowy
        dane = {"model": model, "max_tokens": 16, "system": [{"type": "text", "text": znacznik + stala, "cache_control": cc}],
                "messages": [{"role": "user", "content": "Odpowiedz jednym słowem: OK"}]}
        u = []
        for _ in range(2):
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST", data=json.dumps(dane).encode(), headers={
                "x-api-key": klucze[0], "anthropic-version": "2023-06-01", "content-type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    u.append(json.loads(r.read().decode()).get("usage") or {})
            except urllib.error.HTTPError as e:
                proby.append({"tryb": tryb, "ok": False, "opis": opis_bledu(e.code, e.read().decode("utf-8", "ignore"))})
                break
            except Exception as e:
                proby.append({"tryb": tryb, "ok": False, "opis": f"brak połączenia ({e})"})
                break
            time.sleep(2)
        if len(u) == 2:
            zap, odc = u[0].get("cache_creation_input_tokens") or 0, u[1].get("cache_read_input_tokens") or 0
            proby.append({"tryb": tryb, "ok": odc > 0, "zapisano": zap, "odczytano": odc,
                          "opis": f"zapisano {zap}, przy powtórzeniu odczytano {odc} tokenów"})
        if proby and proby[-1].get("ok"):
            break
    ok = bool(proby) and proby[0].get("ok")
    if ok:
        opis = "pamięć podręczna działa"
    elif any(p.get("ok") for p in proby):
        dz = next(p["tryb"] for p in proby if p.get("ok"))
        opis = f"pamięć podręczna nie działa przy ustawieniu „{tryby[0]}”, działa przy „{dz}” – zmień w Ustawieniach „Pamięć podręczna AI”"
    else:
        opis = "pamięć podręczna nie działa (zapis bez odczytu) – każde zadanie płaci pełną cenę za dokumenty"
    return {"ok": ok, "opis": opis, "proby": proby}


# ============================================================ Claude (strumieniowo)

KONTYNUUJ = ("Twoja poprzednia odpowiedź została ucięta z powodu limitu długości. Kontynuuj DOKŁADNIE od miejsca, "
             "w którym przerwałeś – od następnego znaku, bez powtarzania wcześniejszego tekstu, bez wstępu, "
             "bez komentarzy i bez znaczników ```. Dokończ poprawny JSON.")


CACHE_NIEDOSTEPNY = {"flaga": False}  # ustawiane, gdy API odrzuci parametry pamięci podręcznej


def ustawienie_cache(cfg):
    """Pamięć podręczna promptów (prompt caching): None = wyłączona, inaczej obiekt cache_control."""
    if CACHE_NIEDOSTEPNY["flaga"]:
        return None
    tryb = str(cfg.get("cache_ai", "5m")).strip().lower()
    if tryb in ("brak", "wyłącz", "wylacz", "off", "0", ""):
        return None
    return {"type": "ephemeral", "ttl": "1h"} if tryb in ("1h", "60m", "1 godzina") else {"type": "ephemeral"}


def oznacz_dokumenty(content, cc):
    """Jawny punkt pamięci podręcznej na ostatnim bloku dokumentu/obrazu – dokumenty przetargu są wtedy
    odczytywane z pamięci przy dokańczaniu długich odpowiedzi i przy ponownym przygotowaniu oferty
    (także gdy zmienią się wskazówki, które są dopisywane po dokumentach)."""
    if not cc:
        return content
    idx = [i for i, b in enumerate(content) if isinstance(b, dict) and b.get("type") in ("document", "image")]
    if not idx:
        return content
    content = list(content)
    content[idx[-1]] = dict(content[idx[-1]], cache_control=cc)
    return content


def opis_uzycia(u):
    """Krótki opis zużycia tokenów z pamięcią podręczną (do dziennika zadania)."""
    if not u:
        return ""
    zap, odc, wej = u.get("cache_creation_input_tokens") or 0, u.get("cache_read_input_tokens") or 0, u.get("input_tokens") or 0
    if not zap and not odc:
        return ""
    razem = zap + odc + wej
    t = lambda x: f"{x / 1000:.1f}".replace(".", ",")
    return (f"Pamięć podręczna AI: odczytano {t(odc)} tys., zapisano {t(zap)} tys. tokenów"
            + (f" ({odc / razem:.0%} wejścia z pamięci)" if razem else ""))


NARZEDZIE_WYNIK = {"name": "zapisz_wynik", "description": "Zapisz wynik zadania – obiekt o strukturze opisanej w poleceniu (te same pola i listy).",
                   "input_schema": {"type": "object", "additionalProperties": True}}
TRYB_DANYCH = {"wylaczony": False}  # zgodność wsteczna – rozstrzyga tryb_danych_dostepny(model)
# Modele, które odrzucają wymuszone narzędzie (tool_choice) – zapamiętane w pliku danych, żeby po każdym uruchomieniu serwera nie wysyłać
# zapytania z góry skazanego na błąd (dotyczy m.in. modeli z rozumowaniem, które nie przyjmują wymuszonego narzędzia).
_PLIK_TRYBU = os.path.join(os.environ.get("DATA_DIR") or "/data", "tryb_danych_modele.json")
try:
    _BEZ_TRYBU = set(json.load(open(_PLIK_TRYBU, encoding="utf-8")).get("bez_trybu_danych", []))
except Exception:
    _BEZ_TRYBU = set()


def _model_cfg(cfg):
    return cfg.get("_model") or cfg.get("model_oferty") or "claude-sonnet-5-5"


def tryb_danych_dostepny(cfg):
    return not TRYB_DANYCH["wylaczony"] and _model_cfg(cfg) not in _BEZ_TRYBU


def _wylacz_tryb_danych(cfg):
    _BEZ_TRYBU.add(_model_cfg(cfg))
    try:
        os.makedirs(os.path.dirname(_PLIK_TRYBU), exist_ok=True)
        with open(_PLIK_TRYBU, "w", encoding="utf-8") as f:
            json.dump({"bez_trybu_danych": sorted(_BEZ_TRYBU)}, f, ensure_ascii=False)
    except OSError:
        pass


# Modele z rozumowaniem włączonym domyślnie (nie da się go wyłączyć): tokeny rozumowania liczą się do max_tokens,
# choć jego tekst nie jest zwracany. Przy dużych dokumentach rozumowanie zużywało cały limit i odpowiedź przychodziła PUSTA
# (zakończenie: max_tokens). Dlatego do limitu odpowiedzi dodajemy zapas na rozumowanie (płaci się tylko za zużyte tokeny).
RE_MODEL_ROZUMUJACY = re.compile(r"claude-(opus|sonnet|haiku|fable|mythos)-5")
ZAPAS_ROZUMOWANIA = 32000
MAKS_ODPOWIEDZI = 128000  # maksymalna długość odpowiedzi modeli 5.x (Messages API)


def limit_z_rozumowaniem(model, max_tokens, zapas=None):
    if not RE_MODEL_ROZUMUJACY.search(str(model or "")):
        return max_tokens
    return min(MAKS_ODPOWIEDZI, int(max_tokens) + int(zapas if zapas is not None else ZAPAS_ROZUMOWANIA))


def _jedno_wywolanie(cfg, system, messages, max_tokens, postep, przesuniecie, uzycie=None, dane_strukturalne=False):
    model_ = cfg.get("_model") or cfg.get("model_oferty") or "claude-sonnet-5-5"
    dane = {
        "model": model_,
        "max_tokens": limit_z_rozumowaniem(model_, max_tokens, cfg.get("_zapas_rozumowania")),
        "stream": True,
        "system": system,
        "messages": messages,
    }
    if dane_strukturalne:  # odpowiedź jako obiekt danych (wymuszone narzędzie) – bez komentarzy, bloków ```json i tekstu wokół
        dane["tools"] = [NARZEDZIE_WYNIK]
        dane["tool_choice"] = {"type": "tool", "name": NARZEDZIE_WYNIK["name"]}
    cc = ustawienie_cache(cfg)
    if cc:
        dane["cache_control"] = cc  # automatyczny punkt pamięci na ostatnim bloku (rozmowa przy dokańczaniu)
    tekst, powod, dl, tekst_obok = [], None, 0, []
    try:
        resp = otworz_api(cfg, dane, timeout=900, log=cfg.get("_log"))
    except urllib.error.HTTPError as e:
        tresc = e.read().decode("utf-8", "ignore")
        if cc and e.code == 400 and "cache" in tresc.lower():
            CACHE_NIEDOSTEPNY["flaga"] = True  # zgodność wsteczna: ponów bez pamięci podręcznej
            bez = [dict(mm, content=[{k: v for k, v in b.items() if k != "cache_control"} if isinstance(b, dict) else b
                                     for b in mm["content"]]) if isinstance(mm.get("content"), list) else mm for mm in messages]
            return _jedno_wywolanie(cfg, system, bez, max_tokens, postep, przesuniecie, uzycie, dane_strukturalne)
        raise urllib.error.HTTPError(e.url, e.code, tresc[:500] or e.reason, e.headers, io.BytesIO(tresc.encode("utf-8")))
    with resp:
        for linia in resp:
            linia = linia.decode("utf-8", "ignore").strip()
            if not linia.startswith("data:"):
                continue
            try:
                ev = json.loads(linia[5:].strip())
            except ValueError:
                continue
            typ = ev.get("type")
            if typ == "content_block_delta" and ev.get("delta", {}).get("type") in ("text_delta", "input_json_delta"):
                kaw = ev["delta"].get("text") if ev["delta"]["type"] == "text_delta" else ev["delta"].get("partial_json")
                if dane_strukturalne and ev["delta"]["type"] == "text_delta":
                    tekst_obok.append(kaw or "")  # tekst obok obiektu – zapas, gdy obiekt przyjdzie pusty
                    continue
                tekst.append(kaw or "")
                dl += len(kaw or "")
                if postep and len(tekst) % 40 == 0:
                    postep(przesuniecie + dl)
            elif typ == "content_block_start" and dane_strukturalne and (ev.get("content_block") or {}).get("type") == "tool_use":
                wej = (ev.get("content_block") or {}).get("input")
                if isinstance(wej, dict) and wej:  # obiekt przysłany od razu w całości (bez kawałków)
                    tekst.append(json.dumps(wej, ensure_ascii=False))
            elif typ == "message_start" and uzycie is not None:
                uzycie.update(ev.get("message", {}).get("usage", {}) or {})
            elif typ == "message_delta":
                powod = ev.get("delta", {}).get("stop_reason") or powod
                if uzycie is not None and ev.get("usage"):
                    uzycie.update({k: v for k, v in ev["usage"].items() if v is not None})
            elif typ == "error":
                err = ev.get("error", {})
                raise BladAI(opis_bledu(529 if err.get("type") == "overloaded_error" else 500, err.get("message", "błąd API")))
    wynik = "".join(tekst)
    if dane_strukturalne:
        if not wynik.strip() or wynik.strip() == "{}":
            wynik = "".join(tekst_obok)
        DIAG["ostatnia"] = {"stop": powod, "dl_obiektu": len("".join(tekst)), "dl_tekstu": len("".join(tekst_obok))}
    else:
        DIAG["ostatnia"] = {"stop": powod, "dl_tekstu": len(wynik)}
    if uzycie is not None and uzycie.get("output_tokens"):
        DIAG["ostatnia"]["wyjscie"] = uzycie.get("output_tokens")
    return wynik, powod


DIAG = {"ostatnia": {}}


def _dolacz(calosc, nowy):
    nowy = re.sub(r"^\s*```(?:json)?\s*", "", nowy)
    # usuń ewentualne powtórzenie końcówki poprzedniej części
    for n in range(min(300, len(calosc), len(nowy)), 9, -1):
        if calosc.endswith(nowy[:n]):
            return calosc + nowy[n:]
    return calosc + nowy


# najwyżej 2 duże zapytania AI naraz (dokumenty w pamięci) – chroni serwer przed przekroczeniem limitu pamięci (plan 512 MB).
# Serwer z większą pamięcią (np. urząd, Docker 1 GB+): zmienna BIDIVIA_AI_NARAZ=4 – komplet dokumentów zamówienia pisze się wtedy w pełni równolegle.
import threading as _th
try:
    _AI_NARAZ = min(8, max(1, int(os.environ.get("BIDIVIA_AI_NARAZ") or 2)))
except ValueError:
    _AI_NARAZ = 2
LIMIT_AI = _th.BoundedSemaphore(_AI_NARAZ)


def claude_stream(cfg, system, content, max_tokens=32000, postep=None, log=None, max_kontynuacji=5):
    """Wywołanie AI ze strumieniowaniem. Gdy odpowiedź przekroczy limit długości,
    automatycznie prosi o dokończenie i skleja części."""
    if not LIMIT_AI.acquire(timeout=1):
        if log:
            log("Czekam na zakończenie innej analizy AI (oszczędzanie pamięci serwera)…")
        LIMIT_AI.acquire()
    try:
        return _claude_stream(cfg, system, content, max_tokens, postep, log, max_kontynuacji)
    finally:
        LIMIT_AI.release()


def _claude_stream(cfg, system, content, max_tokens=32000, postep=None, log=None, max_kontynuacji=5):
    try:  # aktualny próg Pzp (170 000 zł od 2026 r.) – AI nie może powoływać się na stare 130 000 zł
        import progi as _PR
        if isinstance(system, str) and "STAN PRAWNY" not in system and any(s in system.lower() for s in ("pzp", "zamówie", "przetarg", "dotac", "konkurencyjno", "swz")):
            system = _PR.INFO_AI + " " + system
    except Exception:
        pass
    calosc, powod = "", None
    if isinstance(content, list):
        content = oznacz_dokumenty(content, ustawienie_cache(cfg))
    messages = [{"role": "user", "content": content}]
    if _oczekuje_danych(system, content):
        if tryb_danych_dostepny(cfg) and (max_tokens <= 24000 or max_kontynuacji <= 1):
            try:
                uzycie = {}
                txt, powod = _jedno_wywolanie(cfg, system, messages, max_tokens, postep, 0, uzycie, dane_strukturalne=True)
                zapisz_uzycie(cfg, cfg.get("_model") or cfg.get("model_oferty") or "claude-sonnet-5-5", uzycie)
                if log and opis_uzycia(uzycie):
                    log(opis_uzycia(uzycie))
                if "{" in txt:
                    if powod == "max_tokens" and log:
                        log("Odpowiedź AI dłuższa niż limit – program zachowuje wszystkie kompletne elementy.")
                    return txt, powod
                if log:
                    d_ = DIAG["ostatnia"]
                    log(f"Tryb danych: brak obiektu danych (zakończenie: {d_.get('stop')}, tekst: {d_.get('dl_tekstu', 0)} znaków) – przepisuję odpowiedź na dane…")
                if txt.strip():
                    return _przepisz_na_dane(cfg, system, content, txt, max_tokens, log), "end_turn"
            except urllib.error.HTTPError as e:
                if e.code == 400 and re.search(r"(?i)tool", str(e.reason) + str(getattr(e, "msg", ""))):
                    _wylacz_tryb_danych(cfg)  # zapamiętane dla tego modelu – kolejne zapytania od razu w zwykłym trybie
                    if log:
                        log(f"Model {_model_cfg(cfg)} nie przyjmuje trybu danych – zwykły tryb odpowiedzi (zapamiętane).")
                else:
                    raise
        txt, powod = _tekst_z_dopisywaniem(cfg, system, content, messages, max_tokens, postep, log, max_kontynuacji)
        if not txt.strip():  # pusta odpowiedź (nie „sam tekst”) – jedno ponowienie z wyraźnym poleceniem zwrócenia danych
            if log:
                wyj_ = (DIAG.get("ostatnia") or {}).get("wyjscie")
                log(f"AI zwróciło pustą odpowiedź (zakończenie: {powod or DIAG['ostatnia'].get('stop')}"
                    + (f"; zużyto {wyj_} tokenów odpowiedzi – głównie na rozumowanie" if wyj_ else "") + ")"
                    + (" – ponawiam z większym limitem…" if powod == "max_tokens" else " – ponawiam…"))
            m2 = [{"role": "user", "content": (list(content) if isinstance(content, list) else [{"type": "text", "text": str(content)}])
                   + [{"type": "text", "text": "WAŻNE: odpowiedz wyłącznie danymi (JSON) w strukturze opisanej w poleceniu."}]}]
            zapas2 = 96000 if powod == "max_tokens" else None  # rozumowanie zjadło limit – więcej miejsca, nie to samo zapytanie
            txt, powod = _tekst_z_dopisywaniem(dict(cfg, _zapas_rozumowania=zapas2) if zapas2 else cfg, system, content, m2, max_tokens, postep, log, 0)
            DIAG["ostatnia"] = dict(DIAG.get("ostatnia") or {}, stop=powod or (DIAG.get("ostatnia") or {}).get("stop"), pusta=not txt.strip())
        if "{" not in txt and txt.strip():
            if log:
                log("AI odpowiedziało opisem zamiast danych – przepisuję odpowiedź na dane…")
            return _przepisz_na_dane(cfg, system, content, txt, max_tokens, log), "end_turn"
        return txt, powod
    return _tekst_z_dopisywaniem(cfg, system, content, messages, max_tokens, postep, log, max_kontynuacji)


def _przepisz_na_dane(cfg, system, content, odpowiedz, max_tokens, log):
    """Odpowiedź opisowa → dane: AI dostaje swoją odpowiedź i przepisuje ją do struktury z polecenia (bez ponownej analizy dokumentów)."""
    polecenie = ""
    if isinstance(content, list):
        polecenie = next((b.get("text") for b in reversed(content) if isinstance(b, dict) and b.get("type") == "text"), "") or ""
    elif isinstance(content, str):
        polecenie = content
    struktura = polecenie[-5000:]
    msg = [{"role": "user", "content": "Poniżej Twoja wcześniejsza odpowiedź na zadanie. Przepisz WSZYSTKIE jej ustalenia do struktury danych opisanej w poleceniu "
                                     "(te same pola, listy i nazwy kluczy). Nie dodawaj nowych ustaleń, nie pomijaj istniejących.\n\nPOLECENIE (fragment ze strukturą):\n"
                                     + struktura + "\n\nODPOWIEDŹ DO PRZEPISANIA:\n" + odpowiedz[:60000]}]
    for strukt in ((True, False) if tryb_danych_dostepny(cfg) else (False,)):
        try:
            uzycie = {}
            txt, _ = _jedno_wywolanie(cfg, system, msg, max_tokens, None, 0, uzycie, dane_strukturalne=strukt)
            zapisz_uzycie(cfg, cfg.get("_model") or cfg.get("model_oferty") or "claude-sonnet-5-5", uzycie)
            if "{" in txt:
                if log:
                    log("Odpowiedź przepisana na dane.")
                return txt
        except urllib.error.HTTPError:
            continue
    return odpowiedz


def _tekst_z_dopisywaniem(cfg, system, content, messages, max_tokens, postep, log, max_kontynuacji):
    calosc, powod = "", None
    for nr in range(max_kontynuacji + 1):
        uzycie = {}
        czesc, powod = _jedno_wywolanie(cfg, system, messages, max_tokens, postep, len(calosc), uzycie)
        zapisz_uzycie(cfg, cfg.get("_model") or cfg.get("model_oferty") or "claude-sonnet-5-5", uzycie)
        if log and opis_uzycia(uzycie):
            log(opis_uzycia(uzycie))
            if nr and not uzycie.get("cache_read_input_tokens") and (uzycie.get("cache_creation_input_tokens") or 0) > 20000:
                log("UWAGA: dokończenie odpowiedzi nie odczytało dokumentów z pamięci podręcznej (zapłacono pełną cenę ponownie) – "
                    "sprawdź „Test połączenia z AI” w Ustawieniach.")
        calosc = _dolacz(calosc, czesc) if calosc else czesc
        if powod != "max_tokens":
            return calosc, powod
        if not calosc.strip():  # limit zużyty na rozumowanie, brak tekstu – nie ma czego dopisywać (ponowienie z większym limitem robi wywołujący)
            return calosc, powod
        if nr < max_kontynuacji:
            if log:
                log(f"Odpowiedź dłuższa niż limit – AI dopisuje dalszą część ({nr + 2})…")
            messages = [{"role": "user", "content": content},
                        {"role": "assistant", "content": calosc.rstrip()},
                        {"role": "user", "content": KONTYNUUJ}]
    return calosc, powod


def _oczekuje_danych(system, content):
    """Czy zadanie oczekuje odpowiedzi w postaci danych (JSON) – wtedy tryb wymuszonej struktury."""
    ost = ""
    if isinstance(content, list):
        for b in reversed(content):
            if isinstance(b, dict) and b.get("type") == "text":
                ost = b.get("text") or ""
                break
    elif isinstance(content, str):
        ost = content
    return "JSON" in ost[-6000:] or "JSON" in str(system or "")[-3000:]


def _napraw_json(txt):
    """Próbuje odzyskać ucięty JSON: obcina do ostatniego pełnego elementu i domyka nawiasy."""
    stos, w_tekscie, esc, punkty = [], False, False, []
    for i, ch in enumerate(txt):
        if w_tekscie:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                w_tekscie = False
            continue
        if ch == '"':
            w_tekscie = True
        elif ch in "{[":
            stos.append(ch)
        elif ch in "}]":
            if stos:
                stos.pop()
            punkty.append((i + 1, list(stos)))
    for kon, st in reversed(punkty[-400:]):
        kand = txt[:kon].rstrip().rstrip(",") + "".join("}" if s == "{" else "]" for s in reversed(st))
        try:
            return json.loads(kand)
        except ValueError:
            continue
    raise ValueError("Nie udało się odczytać odpowiedzi AI (niepełny JSON).")


def obiekty_z_tekstu(txt, wymagane=("cytat",)):
    """Odzyskiwanie kompletnych obiektów {…} z uciętej albo sklejonej odpowiedzi AI: każdy zamknięty obiekt z wymaganymi polami osobno."""
    wyn, i, n = [], 0, len(txt)
    while i < n:
        if txt[i] != "{":
            i += 1
            continue
        gl, w_t, esc, j = 0, False, False, i
        while j < n:
            ch = txt[j]
            if w_t:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    w_t = False
            elif ch == '"':
                w_t = True
            elif ch == "{":
                gl += 1
            elif ch == "}":
                gl -= 1
                if gl == 0:
                    break
            j += 1
        if j >= n:
            i += 1
            continue
        try:
            o = json.loads(txt[i:j + 1])
        except ValueError:
            i += 1
            continue
        if isinstance(o, dict) and all(k in o for k in wymagane):
            wyn.append(o)
            i = j + 1
        else:
            i += 1  # obiekt zewnętrzny bez wymaganych pól – szukamy w środku
        if not wymagane and wyn and wyn[-1] is o:
            i = j + 1
    return wyn


def wyciagnij_json(txt):
    txt = re.sub(r"```(?:json)?", "", txt or "").strip()
    start = txt.find("{")
    if start < 0:
        d_ = DIAG.get("ostatnia") or {}
        if not txt:
            raise ValueError("Odpowiedź AI nie zawiera danych – AI zwróciło pustą odpowiedź"
                             + (f" (zakończenie: {d_.get('stop')})" if d_.get("stop") else "")
                             + ". Najczęstsza przyczyna: zbyt obszerne dokumenty w jednym zapytaniu – pomiń w kroku 1 rysunki i skany bez treści.")
        raise ValueError(f"Odpowiedź AI nie zawiera danych (AI odpowiedziało samym tekstem: „{txt[:160]}”) – spróbuj ponownie.")
    koniec = txt.rfind("}")
    try:
        return json.loads(txt[start:koniec + 1])
    except ValueError:
        pass
    try:
        dane = _napraw_json(txt[start:])
        if isinstance(dane, dict):
            dane["_naprawiony"] = True
            return dane
    except Exception:
        pass
    dane = odzyskaj_dane(txt[start:])
    if dane:
        return dane
    raise ValueError("Odpowiedź AI była niekompletna i nie udało się odzyskać danych – spróbuj ponownie.")


def odzyskaj_dane(txt):
    """Odzysk z uciętej / zepsutej odpowiedzi: pola proste najwyższego poziomu (tekst, liczby) i kompletne elementy każdej listy obiektów."""
    wyn = {}
    for m_ in re.finditer(r'"([A-Za-z_][\w]*)"\s*:\s*("(?:[^"\\]|\\.)*"|-?\d+(?:\.\d+)?|true|false|null)', txt[:4000]):
        k, v = m_.group(1), m_.group(2)
        if k not in wyn:
            try:
                wyn[k] = json.loads(v)
            except ValueError:
                pass
    for m_ in re.finditer(r'"([A-Za-z_][\w]*)"\s*:\s*\[', txt):
        k = m_.group(1)
        if isinstance(wyn.get(k), list) and wyn[k]:
            continue
        obj = [o for o in obiekty_z_tekstu(txt[m_.end():], ()) if isinstance(o, dict)]
        # tylko obiekty bezpośrednio z tej listy: kończymy na pierwszym obiekcie, który nie wygląda jak jej element (inny zestaw kluczy)
        if obj:
            klucze = set(obj[0])
            el = [o for o in obj if len(set(o) & klucze) >= max(1, len(klucze) // 2)]
            wyn[k] = el
    if not any(isinstance(v, list) and v for v in wyn.values()) and len(wyn) < 2:
        return None
    wyn["_odzyskane"] = True
    return wyn


SYSTEM_OFERTA = """Jesteś doświadczonym kosztorysantem i specjalistą ds. przetargów w polskiej firmie budowlanej \
wykonującej termomodernizacje i remonty elewacji. Przygotowujesz kosztorys ofertowy i dane do formularzy \
ofertowych na podstawie dokumentów przetargu, cennika firmy i zasad wyceny firmy. Odpowiadasz WYŁĄCZNIE \
poprawnym JSON-em zgodnym ze schematem, bez markdown, bez komentarzy przed ani po."""

SCHEMAT = """SCHEMAT ODPOWIEDZI (JSON):
{
 "postepowanie": {
  "numer": "nr zapytania / postępowania",
  "nazwa_zamowienia": "pełny opis przedmiotu zamówienia",
  "nazwa_projektu": "nazwa projektu dofinansowania lub \\"\\"",
  "obiekt": "np. ul. Lelewela 22, Świdnica",
  "zamawiajacy_nazwa": "", "zamawiajacy_adres": "", "zamawiajacy_nip": "",
  "sposob_skladania": "np. Baza Konkurencyjności BK2021",
  "termin_skladania": "DD.MM.RRRR GG:MM",
  "termin_zwiazania": "np. 30 dni od upływu terminu składania ofert",
  "termin_wykonania": "",
  "wadium": "kwota i rachunek lub \\"nie wymagane\\"",
  "kryteria": "opis kryteriów i wag",
  "gwarancja_min_mies": 36,
  "gwarancja_mies": 60,
  "wynagrodzenie": "ryczałtowe / kosztorysowe",
  "kosztorys_do_oferty": true,
  "oznaczenie_formularza": "np. Załącznik nr 1 do Zapytania ofertowego",
  "oznaczenie_oswiadczenia": "np. Załącznik nr 2 do Zapytania ofertowego",
  "oznaczenie_wykazu": "np. Załącznik nr 3 do Zapytania ofertowego",
  "ref_wykluczenie": "np. Rozdziału VII ust. 2",
  "ref_warunki": "np. Rozdziale VII ust. 1",
  "ref_kierownik": "np. Rozdz. VII ust. 1 pkt 4",
  "wymagane_roboty": "wymóg doświadczenia (liczba, wartość, rodzaj robót, okres)",
  "polisa_oc": "np. min. 300 000 zł",
  "kierownik_budowy": "wymagania wobec kierownika budowy",
  "budzet_zamawiajacego": "np. audyt: 420 349,13 zł netto lub \\"brak danych\\"",
  "vat": "stawka z dokumentów przetargu, np. 0.23 lub 0.08; null, gdy dokumenty jej nie określają"
 },
 "dzialy": [
  {"nazwa": "1. Nazwa działu z przedmiaru",
   "pozycje": [
    ["KNR 0-23 2611-05", "Przygotowanie podłoża - gruntowanie", "m2", 57.146, 11.96, 1, "", "", "2.1"]
   ]}
 ],
 "zalaczniki_do_oferty": ["lista dokumentów wymaganych do złożenia z ofertą"],
 "podsumowanie": "3-5 zdań: co to za zamówienie, najważniejsze wymagania i ryzyka, rekomendacja",
 "ryzyka": ["..."],
 "do_weryfikacji": ["konkretne pozycje/założenia do sprawdzenia przed złożeniem"],
 "do_uzupelnienia": ["dane i dokumenty, których brakuje w formularzach"],
 "pytania_do_zamawiajacego": ["..."],
 "warianty": [
  {"lp": "numer pozycji przedmiaru, której dotyczy różnica", "opis": "czego dotyczy różnica, np. materiał i średnica rynien",
   "a": {"zrodlo": "przedmiar poz. 28", "opis": "rynny Ø10 cm z tytan-cynku", "cena": 198.0},
   "b": {"zrodlo": "OPZ rozdz. II pkt 4", "opis": "rynny Ø150 mm ze stali powlekanej", "cena": 98.0},
   "nadrzedny": "a albo b – dokument, który ma pierwszeństwo według SWZ / zapytania / umowy; \"\" gdy dokumenty tego nie rozstrzygają"}
 ]
}
WARIANTY: gdy dokumenty podają dla tej samej pozycji przedmiaru różne rozwiązania (materiał, wymiar, grubość, liczba warstw, \
przekrój), NIE wybieraj po cichu – dodaj wpis do "warianty". Wariant "a" to zawsze rozwiązanie z przedmiaru, wariant "b" – \
z innego dokumentu (OPZ, projekt, STWiORB, umowa). Podaj cenę jednostkową netto OBU rozwiązań dla jednostki tej pozycji. \
Pozycję wyceń wariantem z dokumentu nadrzędnego, a gdy dokumenty nie ustalają pierwszeństwa – droższym. Tej samej różnicy \
nie opisuj drugi raz w "do_weryfikacji". Gdy różnic nie ma, zwróć pustą listę.
KAŻDA POZYCJA to tablica 9 elementów w tej kolejności: [podstawa, opis, j.m., ilość, cena jednostkowa netto, \
rynkowa (1 = cena rynkowa, 0 = z cennika firmy), źródło ceny, uwagi, lp]. lp = numer pozycji DOKŁADNIE jak w przedmiarze \
(np. "1.1", "2.3", "15 d.2") – zamawiający porównuje kosztorys z przedmiarem po tym numerze; pozycje spoza przedmiaru: "". Gdy cena jest rynkowa i nie masz nic \
do dodania, zostaw źródło puste "" – program wpisze je sam. Uwagi zostaw puste "", jeśli nie są potrzebne. \
Opis przepisuj z przedmiaru, ale możesz pominąć powtarzające się zbędne dopiski. Uwagi najwyżej 80 znaków, \
bez powtarzania opisu pozycji. Nie dodawaj spacji ani wcięć w JSON-ie (zapis zwarty). Liczby podawaj jako liczby (kropka dziesiętna), ceny z dokładnością do grosza."""


ZASADY_RYNKOWE = """ZASADY WYCENY (tryb: WYŁĄCZNIE CENY RYNKOWE):
1. Ilości, jednostki, opisy i podstawy (KNR) przepisuj DOKŁADNIE z przedmiaru zamawiającego, w jego kolejności i z jego \
podziałem na działy. Nie pomijaj pozycji. Jeśli przedmiar jest skanem – odczytaj ilości z kolumny RAZEM i dopisz \
to do "do_weryfikacji". Jeśli przedmiaru nie ma – ilości weź z audytu energetycznego/dokumentacji, a w polu "uwagi" \
pozycji podaj podstawę ilości.
2. Każdą pozycję wyceń AKTUALNĄ CENĄ RYNKOWĄ netto na {miesiac_rok} ({region}): pełna cena jednostkowa \
wykonawcy (materiał + robocizna + sprzęt + koszty pośrednie + zysk), na poziomie typowych ofert firm wykonawczych \
i ogólnodostępnych cenników robót budowlanych. NIE korzystaj z cen z wcześniejszych kosztorysów ani wycen firmy. Każda pozycja ma \
rynkowa = 1, a źródło zostaw puste "" (program wpisze „Cena rynkowa (szacunek, {miesiac_rok})”). W uwagach krótko podaj główne założenie \
ceny, gdy ma znaczenie (np. "styropian EPS 031 15 cm, kołki 22 cm", "tytan-cynk 0,7 mm").
3. Cena ma odzwierciedlać wymagania z przedmiaru, projektu, audytu i zapytania: grubość i lambda izolacji, rodzaj \
blachy (tytan-cynk jest wyraźnie droższy od ocynku), rodzaj tynku i farby (silikatowe / silikonowe), wysokość \
rusztowań, roboty w obiekcie zabytkowym. Gdy dokumenty są sprzeczne co do rozwiązania w pozycji \
przedmiaru, postępuj według zasady WARIANTY poniżej schematu.
4. Czas pracy (najem) rusztowań bez ilości w przedmiarze: przyjmij m2 rusztowań i rynkową stawkę za okres robót; \
dodaj do "do_weryfikacji".
5. Zawsze dodaj ostatni dział "Pozycje uzupełniające (poza przedmiarem)": budki lęgowe / zamknięcie wlotów wg opinii \
ornitologicznej lub chiropterologicznej, instalacja odgromowa, wywóz i utylizacja odpadów, inne roboty wymagane \
dokumentacją lub umową, a nieujęte w przedmiarze. Wyceń je, gdy ilość da się ustalić; w przeciwnym razie ilość 0, \
cena 0, a "uwagi" zacznij od „NIE DOTYCZY – ” (robota nie występuje albo jest wliczona w inne pozycje – podaj w które) \
albo „DO USTALENIA – ” (robota wymagana albo prawdopodobna, ale ilości nie da się ustalić – podaj dokument i punkt; \
dodaj pytanie do "pytania_do_zamawiajacego" i ryzyko do "ryzyka", bo przy ryczałcie nie ma jej w cenie).
6. {vat_zasada}
7. Gwarancja: zaproponuj liczbę miesięcy dającą maksimum punktów w kryteriach (domyślnie {gwarancja}), nie mniej niż minimum.
8. Sprawdź i opisz w "ryzyka"/"do_weryfikacji": termin składania ofert względem DZISIEJSZEJ daty ({dzis}); wadium \
(kwota, rachunek, tytuł przelewu); rodzaj wynagrodzenia (ryczałt = ryzyko błędów przedmiaru); kary umowne; termin \
wykonania i pogodę/okres lęgowy ptaków (1.03–15.10; przy budynku z gniazdami – ekspertyza ornitologiczna i ewentualnie zezwolenie RDOŚ); rozbieżności przedmiar vs projekt/audyt; błędy w zapytaniu; budżet \
z audytu vs cena oferty (ryzyko przekroczenia budżetu i rażąco niskiej ceny); wymagania: referencje, polisa OC, \
kierownik budowy, podpis.
9. Nigdy nie wymyślaj danych wykonawcy, referencji ani numerów uprawnień – brakujące rzeczy wpisz do "do_uzupelnienia".
10. Pytania do zamawiającego formułuj gotowe do wklejenia w Bazie Konkurencyjności / na platformie."""


def cennik_tekst(cennik):
    linie = ["typ | opis | j.m. | cena netto | źródło"]
    for p in cennik:
        linie.append(f"{p['typ']} | {p['opis']} | {p['jm']} | {p['cena']:.2f} | {p['zrodlo']} [{p.get('oferta','')}]")
    return "\n".join(linie)


VAT_PODSTAWOWY = 0.23  # tylko do obliczeń, gdy stawki nie wybrano i nie wynika z dokumentów – oznaczana jako „do ustalenia”


def zasada_vat(wybor):
    """Polecenie dla AI dotyczące VAT: stawka wybrana przez użytkownika albo odczytana z dokumentów przetargu (bez domyślnej)."""
    try:
        w = float(wybor)
        return (f"Stawka VAT: {w:.0%} – wybrana przez Wykonawcę (Wykonawca odpowiada za prawidłową stawkę); wpisz \"vat\": {w}.")
    except (TypeError, ValueError):
        return ("Stawka VAT: stawkę ustala WYKONAWCA według ustawy o VAT (zamawiający nie ustala stawki). Gdy dokumenty przetargu ją wskazują "
                "– przyjmij ją. Gdy nie: roboty budowlane – stawka podstawowa 23% (\"vat\": 0.23); 8% tylko dla budownictwa objętego społecznym "
                "programem mieszkaniowym (budynki i lokale mieszkalne w limicie powierzchni) – wtedy \"vat\": null i do \"do_weryfikacji\": "
                "\"Stawka VAT – sprawdź, czy roboty dotyczą budownictwa objętego społecznym programem mieszkaniowym (8%)\". "
                "Nie pisz, że stawkę trzeba ustalić z zamawiającym.")


def zbuduj_polecenie(cfg, cennik, przetarg, wskazowki):
    dzis = dt.date.today()
    kp, zysk = float(cfg.get("kp", 73)), float(cfg.get("zysk", 15))
    param = dict(miesiac_rok=f"{MIESIACE[dzis.month - 1]} {dzis.year}",
                 vat_zasada=zasada_vat(cfg.get("vat_wybor")), gwarancja=cfg.get("gwarancja", 60),
                 dzis=dzis.strftime("%d.%m.%Y"), rg=cfg.get("stawka_rg", 40), kp=kp, zysk=zysk,
                 kp_mn=f"{1 + kp / 100:.2f}", zysk_mn=f"{1 + zysk / 100:.2f}")
    reg_ = str(cfg.get("_region_realizacji") or cfg.get("centrum_opis") or cfg.get("centrum_nazwa") or cfg.get("firma_adres") or "").strip()
    param["region"] = ("miejsce realizacji z dokumentów; gdy z nich nie wynika – " + (reg_ or "średnie ceny krajowe")
                       + "; przyjęty region wpisz do \"do_weryfikacji\"")
    zasady = ZASADY_RYNKOWE.format(**param)
    if cennik:  # cennik firmy (aplikacja okienkowa): pierwszeństwo cen z cennika, reszta rynkowa
        zasady += ("\nCENNIK FIRMY: pozycje, które odpowiadają pozycjom cennika poniżej, wyceń DOKŁADNIE ceną z cennika – \"rynkowa\": 0, "
                   "w źródle nazwa i pozycja cennika; pozostałe – ceną rynkową jak wyżej.")
    if cfg.get("_rola_inwestorska"):  # zamawiający / inwestor sporządza kosztorys inwestorski – NIE ma wykonawcy
        firma = (f"ZAMAWIAJĄCY: {cfg.get('_zamawiajacy') or 'zamawiający wskazany w dokumentach (jeśli brak – pola zamawiajacy_* zostaw puste)'}. "
                 "Kosztorys inwestorski (szacowanie wartości zamówienia przed wyborem wykonawcy) sporządza zamawiający. "
                 "WYKONAWCA NIE JEST ZNANY – zostanie wyłoniony w postępowaniu: nigdzie nie wpisuj danych wykonawcy, "
                 "nie pisz o ofercie, formularzu ofertowym ani o „złożeniu oferty”. Pola zamawiajacy_* – zamawiający powyżej albo z dokumentów. "
                 "ILOŚCI WYŁĄCZNIE z dokumentów zamawiającego i jego opisu/odpowiedzi – NIE zakładaj ilości (osób, dni, porcji, wydarzeń) "
                 "i NIE dodawaj pozycji ani usług, których nie ma w zakresie zamówienia. Gdy ilości brak: ilość 0, w uwagach "
                 "„ILOŚĆ DO UZUPEŁNIENIA” i wpis do \"do_uzupelnienia\". W uwagach podawaj, skąd ilość (dokument / punkt). "
                 + (f"Ceny – rynkowe dla miejsca realizacji: {cfg['_region_realizacji']}; ceny z innych regionów oznacz w źródle "
                    "„inny region” i skoryguj do poziomu tego regionu." if cfg.get("_region_realizacji") else ""))
    else:
        firma = (f"WYKONAWCA: {cfg.get('firma_nazwa')}, {cfg.get('firma_adres')}, NIP: {cfg.get('firma_nip') or 'brak'}, "
                 f"REGON: {cfg.get('firma_regon') or 'brak'}"
                 + "".join(f", {et}: {cfg.get(k)}" for k, et in (("firma_krs", "KRS"), ("firma_email", "e-mail"), ("firma_tel", "telefon"),
                                                                ("firma_osoba", "reprezentacja / kontakt")) if cfg.get(k))
                 + " (te dane są znane – nie wpisuj ich do „do_uzupelnienia”)")
    info = ""
    if przetarg:
        info = (f"OGŁOSZENIE (z wyszukiwarki): {przetarg.get('przedmiot','')} | {przetarg.get('zamawiajacy','')} | "
                f"termin ofert: {przetarg.get('termin_ofert','')} | {przetarg.get('link','')}\n")
    return (f"Dzisiejsza data: {dzis.strftime('%d.%m.%Y')}.\n{firma}\n{info}\n"
            f"Powyżej są dokumenty przetargu. Przygotuj kosztorys ofertowy i dane do formularzy.\n\n{zasady}\n\n"
            + (f"CENNIK FIRMY ({len(cennik)} pozycji):\n{cennik_tekst(cennik)}\n\n" if cennik else "")
            + f"DODATKOWE WSKAZÓWKI UŻYTKOWNIKA: {wskazowki or 'brak'}\n\n{SCHEMAT}")


# ============================================================ obliczenia

KLUCZE_POZ = ("podstawa", "opis", "jm", "ilosc", "cena", "rynkowa", "zrodlo", "uwagi", "lp")  # lp – numer pozycji z przedmiaru (np. „2.3”)


def _pozycja(p):
    if isinstance(p, list):
        p = dict(zip(KLUCZE_POZ, p + [""] * (len(KLUCZE_POZ) - len(p))))
    p = dict(p)
    p["rynkowa"] = bool(p.get("rynkowa")) and str(p.get("rynkowa")).lower() not in ("0", "false", "nie")
    for k in ("podstawa", "opis", "jm", "zrodlo", "uwagi", "lp"):
        p[k] = "" if p.get(k) is None else str(p.get(k)).strip()
    try:
        zero = not float(p.get("cena") or 0) or not float(p.get("ilosc") or 0)
    except (TypeError, ValueError):
        zero = True
    if zero and (not p["zrodlo"].strip() or p["zrodlo"].startswith("Cena rynkowa (szacunek")):
        p["zrodlo"] = "nie wyceniono"  # pozycja 0 zł – nie „cena rynkowa”
    elif not p["zrodlo"].strip():
        d = dt.date.today()
        p["zrodlo"] = f"Cena rynkowa (szacunek, {MIESIACE[d.month - 1]} {d.year})" if p["rynkowa"] else ""
    return p


def przelicz(dane):
    netto = 0.0
    for d in dane.get("dzialy", []):
        d["pozycje"] = [_pozycja(p) for p in d.get("pozycje", []) if isinstance(p, (list, dict))]
        suma = 0.0
        for p in d.get("pozycje", []):
            for k_ in ("ilosc", "cena"):  # „12,5”, „1 234.50” (odpowiedź AI, kosztorys z Excela) – jak wpisane; nieczytelne – 0 i uwaga
                try:
                    p[k_] = liczba_pl(p.get(k_) or 0)
                except (TypeError, ValueError):
                    uw = (f"Pozycja „{str(p.get('opis') or '')[:60]}”: nieczytelna {'ilość' if k_ == 'ilosc' else 'cena'} "
                          f"„{str(p.get(k_))[:20]}” – przyjęto 0, popraw w kosztorysie.")
                    if uw not in dane.setdefault("do_weryfikacji", []):
                        dane["do_weryfikacji"].append(uw)
                    p[k_] = 0.0
            p["wartosc"] = zaokr(p["ilosc"] * zaokr(p["cena"]))
            suma += p["wartosc"]
        d["suma"] = zaokr(suma)
        netto += d["suma"]
    surowy = dane.get("postepowanie", {}).get("vat")
    try:
        vat = float(str(surowy).replace(",", ".").replace("%", "")) if surowy not in (None, "", "null") else None
        if vat is not None and vat > 1:  # np. 23 zamiast 0.23
            vat = vat / 100
    except ValueError:
        vat = None
    dane["vat_nieustalony"] = vat is None
    # starsze odpowiedzi AI: „Stawka VAT – ustal z zamawiającym” – stawkę ustala wykonawca, uwaga zastępowana właściwą (poniżej)
    dane["do_weryfikacji"] = [x for x in dane.get("do_weryfikacji") or [] if not re.search(r"(?i)VAT.{0,80}ustal\w*.{0,20}\bz\s+zamawiaj", str(x))]
    if vat is None:  # brak stawki w dokumentach i brak wyboru – do obliczeń stawka podstawowa, wyraźnie oznaczona
        vat = VAT_PODSTAWOWY
        dane.setdefault("postepowanie", {})["vat"] = None
        uw = ("Stawka VAT nie wynika z dokumentów – przyjęto stawkę podstawową 23%. Stawkę ustala Wykonawca; 8% wyłącznie przy budownictwie "
              "objętym społecznym programem mieszkaniowym – zmień w kroku „Kosztorys i oferta”, jeśli dotyczy.")
        if uw not in dane.setdefault("do_weryfikacji", []):
            dane["do_weryfikacji"].insert(0, uw)
    dane["netto"] = zaokr(netto)
    dane["vat_kwota"] = zaokr(netto * vat)
    dane["brutto"] = zaokr(dane["netto"] + dane["vat_kwota"])
    dane["vat"] = vat
    rynek = sum(p["wartosc"] for d in dane["dzialy"] for p in d["pozycje"] if p.get("rynkowa"))
    dane["udzial_rynkowych"] = rynek / netto if netto else 0
    dane["wartosc_rynkowych"] = zaokr(rynek)
    return dane


# ============================================================ kosztorys xlsx

def _poza_przedmiarem(d, p):
    return bool(re.search(r"(?i)poza\s+przedmiar", str(d.get("nazwa") or "")) or re.search(r"(?i)poza\s+przedmiar", str(p.get("podstawa") or "")))


def _wyrownaj_do_grosza(k, roznica):
    """Różnica z zaokrągleń cen jednostkowych (kosztorys dla zamawiającego) – tak, aby suma była równa cenie oferty co do grosza.
    1) jedna pozycja, której cena po zmianie o pełne grosze daje dokładnie tę różnicę (najpierw pozycje z ilością 1, potem o najmniejszej ilości);
    2) kolejno kilka pozycji – od największej ilości (zgrubnie) do najmniejszej (dokładnie);
    3) gdy groszami cen nie da się dojść do kwoty (np. same ilości parzyste) – wiersz „Wyrównanie zaokrągleń” (1 kpl, cena dodatnia).
    Cena oferty się nie zmienia; ceny jednostkowe nigdy nie spadają poniżej 0,01 zł."""
    poz = [p for d in k["dzialy"] for p in d["pozycje"] if (p.get("ilosc") or 0) > 0]
    gr = lambda x: int(round(x * 100))
    cel = gr(roznica)

    def delta(p, c_):  # zmiana wartości pozycji (w groszach) przy cenie c_
        return gr(zaokr(p["ilosc"] * c_)) - gr(p["wartosc"])

    def ceny(p, r):  # ceny (pełne grosze, > 0) w pobliżu ceny dającej różnicę r groszy
        c0 = zaokr(p["cena"] + r / 100 / p["ilosc"])
        return [c_ for c_ in (zaokr(c0 + i / 100) for i in (0, -1, 1, -2, 2)) if c_ >= 0.01]

    def ustaw(p, c_):
        p["cena"] = c_
        p["wartosc"] = zaokr(p["ilosc"] * c_)

    for p in sorted(poz, key=lambda p: (p["ilosc"] != 1, p["ilosc"], -p["wartosc"])):
        c_ = next((c_ for c_ in ceny(p, cel) if delta(p, c_) == cel), None)
        if c_ is not None:
            ustaw(p, c_)
            return
    reszta = cel
    for p in sorted(poz, key=lambda p: -p["ilosc"]):
        if not reszta:
            return
        lep = min(ceny(p, reszta), key=lambda c_: abs(reszta - delta(p, c_)), default=None)
        if lep is not None and abs(reszta - delta(p, lep)) < abs(reszta):
            reszta -= delta(p, lep)
            ustaw(p, lep)
    if not reszta:
        return
    if reszta < 0:  # wiersz wyrównania tylko z ceną dodatnią – najpierw obniż o grosz pozycję o najmniejszej ilości
        p = min(poz, key=lambda p: p["ilosc"])
        c_ = zaokr(p["cena"] - 0.01)
        while delta(p, c_) > reszta and c_ > 0.01:
            c_ = zaokr(c_ - 0.01)
        reszta -= delta(p, c_)
        ustaw(p, c_)
    if reszta > 0:
        k["_wyrownanie"] = reszta / 100
        k["dzialy"][-1]["pozycje"].append(_pozycja({"lp": "", "opis": "Wyrównanie zaokrągleń cen jednostkowych do ceny oferty", "jm": "kpl",
                                                    "ilosc": 1.0, "cena": reszta / 100, "wartosc": reszta / 100, "zrodlo": "wyrównanie zaokrągleń"}))


def dla_zamawiajacego(dane):
    """Kosztorys do przekazania zamawiającemu: koszty z działu „poza przedmiarem” (rezerwy, zaplecze, OC, zabezpieczenie…) rozłożone
    proporcjonalnie na ceny pozycji przedmiaru – suma bez zmian; bez pozycji z ilością 0 i bez pustych działów. Zwraca (kopia, opis)
    albo (kopia bez zmian, ""), gdy nie ma czego rozkładać. Gdy groszowe zaokrąglenia zmienią sumę, różnicę przejmuje pozycja
    z ilością 1 albo inna pozycja / pozycje (_wyrownaj_do_grosza) – suma kosztorysu dla zamawiającego zawsze równa cenie oferty."""
    import copy as _c
    k = _c.deepcopy(dane)
    dod = sum(zaokr(p.get("wartosc") or 0) for d in k["dzialy"] for p in d["pozycje"] if _poza_przedmiarem(d, p))
    baza = [p for d in k["dzialy"] for p in d["pozycje"] if not _poza_przedmiarem(d, p) and (p.get("wartosc") or 0) > 0]
    suma_bazy = sum(zaokr(p["wartosc"]) for p in baza)
    opis = ""
    if dod > 0 and suma_bazy > 0:
        f = (suma_bazy + dod) / suma_bazy
        for p in baza:
            p["cena"] = zaokr(p["cena"] * f)
            p["wartosc"] = zaokr(p["ilosc"] * p["cena"])
        opis = (f"W kosztorysie dla zamawiającego koszty spoza przedmiaru ({zl(dod)}) rozłożono proporcjonalnie na ceny pozycji przedmiaru "
                f"(+{str(round((f - 1) * 100, 1)).replace('.', ',')}%).")
    zostaw_poza = suma_bazy <= 0  # przedmiar bez wycenionych pozycji – koszty spoza przedmiaru zostają jako osobne pozycje (suma bez zmian)
    for d in k["dzialy"]:
        d["pozycje"] = [p for p in d["pozycje"] if (zostaw_poza or not _poza_przedmiarem(d, p)) and (p.get("ilosc") or 0) > 0]
        d["suma"] = zaokr(sum(p["wartosc"] for p in d["pozycje"]))
    k["dzialy"] = [d for d in k["dzialy"] if d["pozycje"]]
    roznica = zaokr(zaokr(dane.get("netto") or 0) - sum(d["suma"] for d in k["dzialy"]))
    if roznica and k["dzialy"]:
        _wyrownaj_do_grosza(k, roznica)
        if k.pop("_wyrownanie", None):
            opis = (opis + " " if opis else "W kosztorysie dla zamawiającego koszty spoza przedmiaru – ") + \
                "różnicę z zaokrągleń cen jednostkowych ujęto w wierszu „Wyrównanie zaokrągleń” (suma równa cenie oferty)."
        for d in k["dzialy"]:
            d["suma"] = zaokr(sum(x["wartosc"] for x in d["pozycje"]))
    k["netto"] = zaokr(sum(d["suma"] for d in k["dzialy"]))
    k["vat_kwota"] = zaokr(k["netto"] * k["vat"])
    k["brutto"] = zaokr(k["netto"] + k["vat_kwota"])
    return k, opis


def zapisz_kosztorys(dane, cfg, sciezka, dla_klienta=False):
    """Kosztorys ofertowy w Excelu. dla_klienta=True – wersja do przekazania klientowi / zamawiającemu:
    bez kolumn „Źródło ceny” i „Uwagi / podstawa ilości”, bez oznaczeń kolorami i notatek roboczych."""
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    P = dane["postepowanie"]
    wb = openpyxl.Workbook()
    ws = wb.active
    INW = bool(dane.get("_inwestorski"))  # kosztorys inwestorski zamawiającego / inwestora – bez wykonawcy i „oferty”
    ws.title = "Kosztorys inwestorski" if INW else "Kosztorys ofertowy"
    F = lambda **k: Font(name="Arial", size=k.pop("size", 9), **k)
    zolty = PatternFill("solid", fgColor="FFF2CC")
    szary = PatternFill("solid", fgColor="D9E1F2")
    cienka = Side(style="thin", color="999999")
    ramka = Border(left=cienka, right=cienka, top=cienka, bottom=cienka)
    zawin = Alignment(wrap_text=True, vertical="top")
    ost_kol = "G" if dla_klienta else "I"
    n_kol = 7 if dla_klienta else 9
    for kol, szer in zip("ABCDEFGHI"[:n_kol], (5, 20, 60, 7, 11, 13, 15, 38, 30)):
        ws.column_dimensions[kol].width = szer

    ws["A1"] = dane.get("_tytul") or "KOSZTORYS OFERTOWY"
    ws["A1"].font = F(size=14, bold=True)
    numer = str(P.get("numer", "")).strip()
    if INW:
        ws["A2"] = f"Zamówienie: {P.get('nazwa_zamowienia','')}" + (f" – {P['obiekt']}" if P.get("obiekt") else "") + (f" (znak sprawy {numer})" if numer else "")
    elif not numer:
        ws["A2"] = f"Zadanie: {P.get('nazwa_zamowienia','')}" + (f" – {P['obiekt']}" if P.get("obiekt") else "")
    else:
        numer = numer if re.search(r"\bnr\b", numer, re.I) else f"nr {numer}"
        ws["A2"] = f"Załącznik do oferty w postępowaniu {numer} - {P.get('nazwa_zamowienia','')}"
    if INW:  # zamawiający = dane z profilu; wykonawca nieznany (wyłoniony w postępowaniu)
        ws["A3"] = f"{dane.get('_rola_nazwa') or 'Zamawiający'}: {dane.get('_zamawiajacy') or '[UZUPEŁNIJ: nazwa i adres zamawiającego]'}"
        ws["A4"] = "Data:"
        ws["C4"] = dt.date.today().strftime("%d.%m.%Y")
    else:
        ws["A3"] = (f"Zamawiający: {P.get('zamawiajacy_nazwa','')}, {P.get('zamawiajacy_adres','')}"
                    + (f", NIP {P['zamawiajacy_nip']}" if P.get("zamawiajacy_nip") else ""))
        ws["A4"] = "Wykonawca:"
        ws["C4"] = f"{cfg.get('firma_nazwa','')}, {cfg.get('firma_adres','')}"
    if INW and not dla_klienta:
        ws["A5"] = "Legenda:"
        ws["C5"] = ("Kosztorys inwestorski – szacowanie wartości zamówienia (art. 28–36 Pzp), wartość netto bez VAT. Ilości z dokumentów "
                    "zamawiającego (kol. I – skąd ilość). Ceny na CZERWONO – ceny rynkowe na dzień sporządzenia (kol. H – źródło). "
                    "Komórki z RÓŻOWYM tłem – ilość bez potwierdzenia w dokumentach: sprawdź przed przyjęciem wartości.")
    elif dla_klienta:
        ws["A5"] = "Data:"
        ws["C5"] = dt.date.today().strftime("%d.%m.%Y")
    else:
        ws["A5"] = "Legenda:"
        ws["C5"] = ("Żółte pola może zmieniać Wykonawca (cena jednostkowa netto, stawka VAT). Ilości i opisy z przedmiaru "
                    "zamawiającego. Pozycje na CZERWONO to ceny rynkowe (szacunek na dzień sporządzenia) - zweryfikuj przed "
                    "złożeniem; pozycje w czerni pochodzą z kosztorysów Wykonawcy (kol. H).")
    for r in range(2, 6):
        for c in ("A", "C"):
            ws[f"{c}{r}"].font = F()
            ws[f"{c}{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(f"C{r}:{ost_kol}{r}") if r >= 4 else ws.merge_cells(f"A{r}:{ost_kol}{r}")
    ws.row_dimensions[2].height = 28
    ws.row_dimensions[5].height = 16 if dla_klienta else 38

    r = 7
    for i, h in enumerate(["Lp.", "Podstawa", "Opis robót", "j.m.", "Ilość", "Cena jedn. netto [zł]",
                           "Wartość netto [zł]", "Źródło ceny", "Uwagi / podstawa ilości"][:n_kol], 1):
        c = ws.cell(r, i, h)
        c.font = F(bold=True)
        c.fill = szary
        c.border = ramka
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.freeze_panes = "A8"
    r += 1
    lp, sumy = 1, []
    lp_przedmiaru = any(str(p.get("lp") or "").strip() for d in dane["dzialy"] for p in d["pozycje"])  # numeracja jak w przedmiarze
    for d in dane["dzialy"]:
        c = ws.cell(r, 1, d.get("nazwa", ""))
        c.font = F(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=n_kol)
        r += 1
        pierwszy = r
        for p in d["pozycje"]:
            kolor = "FF0000" if p.get("rynkowa") and not dla_klienta else "000000"
            bez_podstawy = INW and p.get("ilosc_bez_podstawy") and not dla_klienta
            wart = [(str(p.get("lp") or "").strip() or f"u.{lp}") if lp_przedmiaru else lp, p.get("podstawa", ""), p.get("opis", ""), p.get("jm", ""), p["ilosc"], p["cena"],
                    p.get("wartosc", zaokr(p["ilosc"] * zaokr(p["cena"]))), p.get("zrodlo", ""), p.get("uwagi", "")][:n_kol]
            for i, v in enumerate(wart, 1):
                c = ws.cell(r, i, v)
                c.font = F(color=kolor)
                c.border = ramka
                c.alignment = zawin
            ws.cell(r, 5).number_format = "#,##0.000"
            if bez_podstawy:
                for kk in (5, 9):
                    ws.cell(r, kk).fill = PatternFill("solid", fgColor="FFC7CE")
                ws.cell(r, 9).value = ("ILOŚĆ BEZ POTWIERDZENIA W DOKUMENTACH – sprawdź. " + str(p.get("uwagi") or ""))[:500]
            ws.cell(r, 6).number_format = "#,##0.00"
            ws.cell(r, 7).number_format = "#,##0.00"
            if not dla_klienta:
                ws.cell(r, 6).fill = zolty
            lp += 1
            r += 1
        nazwa_dz = re.sub(r"^[0-9.]+\s*", "", d.get("nazwa", ""))
        ws.cell(r, 3, f"Razem - {nazwa_dz} (netto)").font = F(bold=True)
        c = ws.cell(r, 7, d.get("suma", 0))  # kwoty wpisane wprost – widoczne w każdym podglądzie (telefon, poczta), nie tylko w Excelu
        c.font = F(bold=True)
        c.number_format = "#,##0.00"
        sumy.append(f"G{r}")
        r += 2

    def wiersz(etykieta, formula, fmt="#,##0.00", pogrub=True, wypelnij=None):
        nonlocal r
        ws.cell(r, 3, etykieta).font = F(bold=pogrub, size=10)
        c = ws.cell(r, 7, formula)
        c.font = F(bold=pogrub, size=10)
        c.number_format = fmt
        c.border = ramka
        if wypelnij:
            c.fill = wypelnij
        r += 1
        return f"G{r - 1}"

    netto = wiersz("WARTOŚĆ ZAMÓWIENIA NETTO [zł]" if INW else "CENA OFERTY NETTO [zł]" if not dla_klienta else "RAZEM NETTO [zł]", dane.get("netto", 0))
    stawka = wiersz(("Stawka VAT (informacyjnie)" if INW else "Stawka VAT" if dla_klienta else "Stawka VAT (ustala Wykonawca)")
                    + (" – DO USTALENIA" if dane.get("vat_nieustalony") and not dla_klienta else ""), dane["vat"], "0%", False,
                    None if dla_klienta else zolty)
    vat = wiersz("VAT [zł]", dane.get("vat_kwota", 0))
    wiersz("KWOTA BRUTTO – do zabezpieczenia środków (informacyjnie) [zł]" if INW else "RAZEM BRUTTO [zł]" if dla_klienta else "CENA OFERTY BRUTTO [zł]",
           dane.get("brutto", 0))
    r += 1
    if INW:
        ws.cell(r, 3, "Wartość zamówienia ustala się bez VAT (art. 28 Pzp). Datę i sposób szacowania udokumentuj w notatce z szacowania.").font = F(italic=True)
        r += 1
        if dane.get("_kontrola_ilosci"):
            ws.cell(r, 3, dane["_kontrola_ilosci"]).font = F(italic=True, bold=True, color="C00000")
            r += 1
        ws.cell(r, 3, f"W tym pozycje wycenione rynkowo (czerwone): {zl(dane['wartosc_rynkowych'])} netto "
                      f"({dane['udzial_rynkowych']:.0%} wartości netto)").font = F(italic=True, color="FF0000")
    elif dla_klienta:
        ws.cell(r, 3, f"Sporządził: {cfg.get('firma_nazwa', '')}" + (f", {cfg['firma_osoba']}" if cfg.get("firma_osoba") else "")
                + (f", tel. {cfg['firma_tel']}" if cfg.get("firma_tel") else "")).font = F(italic=True)
    else:
        ws.cell(r, 3, "Wartości netto / VAT / brutto przepisz do formularza ofertowego.").font = F(italic=True)
        r += 1
        ws.cell(r, 3, f"W tym pozycje wycenione rynkowo (czerwone): {zl(dane['wartosc_rynkowych'])} netto "
                      f"({dane['udzial_rynkowych']:.0%} ceny netto)").font = F(italic=True, color="FF0000")
    ws.print_title_rows = "7:7"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    if dla_klienta and not INW:  # do zamawiającego: tabela elementów scalonych zamiast notatek roboczych (uwagi, ryzyka) – te zostają w wersji wewnętrznej
        t = wb.create_sheet("Tabela elementów scalonych")
        for kol, szer in zip("ABC", (6, 70, 18)):
            t.column_dimensions[kol].width = szer
        t["A1"] = "TABELA ELEMENTÓW SCALONYCH"
        t["A1"].font = F(size=12, bold=True)
        t["A2"] = ws["A2"].value
        t["A2"].font = F()
        rr = 4
        for i, h in enumerate(("Lp.", "Element robót", "Wartość netto [zł]"), 1):
            c = t.cell(rr, i, h)
            c.font, c.fill, c.border = F(bold=True), szary, ramka
        for i, d in enumerate(dane["dzialy"], 1):
            rr += 1
            for k, v in enumerate((i, re.sub(r"^[0-9.]+\s*", "", d.get("nazwa", "")), d.get("suma", 0)), 1):
                c = t.cell(rr, k, v)
                c.font, c.border = F(), ramka
            t.cell(rr, 3).number_format = "#,##0.00"
        for et, v, fmt in (("RAZEM NETTO [zł]", dane.get("netto", 0), "#,##0.00"), ("Stawka VAT", dane["vat"], "0%"),
                           ("VAT [zł]", dane.get("vat_kwota", 0), "#,##0.00"), ("RAZEM BRUTTO [zł]", dane.get("brutto", 0), "#,##0.00")):
            rr += 1
            t.cell(rr, 2, et).font = F(bold=True)
            c = t.cell(rr, 3, v)
            c.font, c.number_format, c.border = F(bold=True), fmt, ramka
        wb.save(sciezka)
        return
    u = wb.create_sheet("Uwagi")
    u.column_dimensions["A"].width = 5
    u.column_dimensions["B"].width = 120
    u["B1"] = "Założenia i uwagi do kosztorysu"
    u["B1"].font = F(size=12, bold=True)
    rr = 3
    for tytul, lista in ((("Do sprawdzenia przed przyjęciem wartości" if INW else "Do weryfikacji przed złożeniem"), dane.get("do_weryfikacji", [])),
                         (("Co może zmienić wartość zamówienia" if INW else "Ryzyka"), dane.get("ryzyka", [])),
                         (("Do ustalenia przed wszczęciem postępowania" if INW else "Do uzupełnienia"), dane.get("do_uzupelnienia", []))):
        u.cell(rr, 2, tytul).font = F(bold=True, size=10)
        rr += 1
        for i, t in enumerate(lista, 1):
            u.cell(rr, 1, i).font = F()
            c = u.cell(rr, 2, t)
            c.font = F()
            c.alignment = Alignment(wrap_text=True, vertical="top")
            rr += 1
        rr += 1
    wb.save(sciezka)


# ============================================================ dokumenty Word

LOGO = None  # ścieżka do logo firmy (ustawiana przez serwer, gdy logo jest wgrane w Profilu firmy)


def _doc():
    import docx
    from docx.shared import Pt, Cm
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2)
        s.top_margin = s.bottom_margin = Cm(1.8)
        lg = LOGO() if callable(LOGO) else LOGO
        if lg and os.path.isfile(lg):  # logo firmy w nagłówku każdej strony
            try:
                s.header.paragraphs[0].add_run().add_picture(lg, height=Cm(1.2))
            except Exception:
                pass
    return d


def _akapit(d, tekst, pogrub=False, kursywa=False, rozmiar=None, wyrownanie=None, styl=None):
    """Akapit, w którym fragmenty [UZUPEŁNIJ...] są podświetlone na żółto."""
    from docx.enum.text import WD_COLOR_INDEX
    from docx.shared import Pt
    p = d.add_paragraph(style=styl) if styl else d.add_paragraph()
    for cz in re.split(r"(\[UZUPEŁNIJ[^\]]*\])", tekst):
        if not cz:
            continue
        run = p.add_run(cz)
        run.bold = pogrub
        run.italic = kursywa
        if rozmiar:
            run.font.size = Pt(rozmiar)
        if cz.startswith("[UZUPEŁNIJ"):
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    if wyrownanie is not None:
        p.alignment = wyrownanie
    return p


def _tabela(d, wiersze, naglowek=True):
    t = d.add_table(rows=len(wiersze), cols=len(wiersze[0]))
    t.style = "Table Grid"
    for i, w in enumerate(wiersze):
        for j, v in enumerate(w):
            c = t.cell(i, j)
            c.text = ""
            p = c.paragraphs[0]
            from docx.enum.text import WD_COLOR_INDEX
            for cz in re.split(r"(\[UZUPEŁNIJ[^\]]*\])", str(v)):
                if cz:
                    run = p.add_run(cz)
                    run.bold = naglowek and i == 0
                    if cz.startswith("[UZUPEŁNIJ"):
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return t


def _podpis(d):
    _tabela(d, [["....................................................\nmiejscowość, data",
                 "....................................................\npodpis(y) osoby(ób) upoważnionej(ych) do reprezentowania Wykonawcy"]],
            naglowek=False)


def _pole(cfg, klucz, opis):
    v = (cfg.get(klucz) or "").strip()
    return v if v else f"[UZUPEŁNIJ: {opis}]"


def zapisz_formularze(dane, cfg, sciezka):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    P = dane["postepowanie"]
    d = _doc()
    firma = _pole(cfg, "firma_nazwa", "nazwa firmy")
    adres = _pole(cfg, "firma_adres", "adres")
    przedmiot = P.get("nazwa_zamowienia", "")
    projekt = f" w ramach projektu pn. „{P['nazwa_projektu']}”" if P.get("nazwa_projektu") else ""
    gw = P.get("gwarancja_mies") or cfg.get("gwarancja", 60)
    # przetarg według Pzp (SWZ, platforma) albo zapytanie ofertowe (zasada konkurencyjności / poniżej progu) – właściwe nazwy w formularzu
    pzp = bool(re.search(r"(?i)\bSWZ\b|specyfikacj|\bPzp\b|e-?zam[oó]wie|tryb podstawow|przetarg", " ".join(
        str(P.get(k) or "") for k in ("sposob_skladania", "oznaczenie_formularza", "termin_zwiazania", "kryteria", "numer", "ref_warunki"))))
    DOK_D, DOK_C = ("SWZ", "SWZ") if pzp else ("Zapytania ofertowego", "zapytaniu ofertowym")
    tw = str(P.get("termin_wykonania") or "").strip().rstrip(".")

    # --- Załącznik: formularz ofertowy
    _akapit(d, P.get("oznaczenie_formularza") or f"Załącznik nr 1 do {DOK_D}", kursywa=True,
            wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _akapit(d, "OFERTA", pogrub=True, rozmiar=14, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    _akapit(d, (f"Odpowiadając na ogłoszenie o zamówieniu w postępowaniu nr {P.get('numer','')} pn.: {przedmiot}{projekt}," if pzp else
                f"Odpowiadając na zapytanie ofertowe nr {P.get('numer','')} na wybór wykonawcy: {przedmiot}{projekt},"))
    _akapit(d, "działając w imieniu i na rzecz Wykonawcy:")
    _tabela(d, [["nazwa (firma) Wykonawcy", "adres siedziby Wykonawcy"], [firma, adres]])
    _akapit(d, f"składamy ofertę w przedmiotowym postępowaniu o udzielenie zamówienia: {przedmiot}:")
    _akapit(d, f"Oferuję/my wykonanie zamówienia za całkowitą cenę brutto: {zl(dane['brutto'])}; "
               f"słownie: {slownie(dane['brutto'])},", styl="List Number")
    _akapit(d, f"Netto: {zl(dane['netto'])}; słownie: {slownie(dane['netto'])},")
    _akapit(d, f"VAT ({dane['vat']:.0%}): {zl(dane['vat_kwota'])}; słownie: {slownie(dane['vat_kwota'])},")
    _akapit(d, "zgodnie z załączonym kosztorysem ofertowym." if P.get("kosztorys_do_oferty", True)
            else f"zgodnie z treścią {'SWZ' if pzp else 'zapytania ofertowego'}.")
    if tw:
        _akapit(d, f"Zobowiązuję/my się wykonać przedmiot zamówienia w terminie: {tw}.",
                styl="List Number")
    _akapit(d, f"Na wykonany przedmiot zamówienia udzielam(y) {gw} miesięcy gwarancji jakości.", styl="List Number")
    _akapit(d, "Ponadto:")
    for t in [
        f"Uważamy się za związanych niniejszą ofertą przez okres wskazany w {DOK_C} "
        f"({P.get('termin_zwiazania') or '30 dni od upływu terminu składania ofert'});",
        "Zobowiązujemy się w przypadku wyboru naszej oferty do zawarcia umowy w miejscu i terminie wskazanym przez Zamawiającego;",
        "Oświadczamy, że niniejsza oferta oraz wszelkie załączniki do niej są jawne i nie zawierają informacji stanowiących "
        "tajemnicę przedsiębiorstwa w rozumieniu przepisów o zwalczaniu nieuczciwej konkurencji za wyjątkiem następujących "
        "informacji: [UZUPEŁNIJ: wpisać lub „brak”];",
        "Oświadczamy, że wyrażamy zgodę na przetwarzanie przez Zamawiającego informacji zawierających dane osobowe oraz, "
        "że poinformowaliśmy pisemnie i uzyskaliśmy zgodę każdej osoby, której dane osobowe są podane w ofercie oraz "
        "w dokumentach składanych wraz z ofertą;",
        "Zamierzam(y) powierzać podwykonawcom następujące części niniejszego zamówienia:",
    ]:
        _akapit(d, t, styl="List Bullet")
    _tabela(d, [["L.p.", "Zakres wykonywanych prac", "Nazwa Wykonawcy (podwykonawcy)"],
                ["1.", "[UZUPEŁNIJ lub wpisz „nie dotyczy”]", "[UZUPEŁNIJ]"], ["2.", "", ""]])
    _akapit(d, f"Zapoznałem(liśmy) się z treścią {DOK_D} dla niniejszego zamówienia i gwarantuję(emy) "
               "wykonanie całości niniejszego zamówienia zgodnie z jego treścią.", styl="List Bullet")
    _akapit(d, "Wszelką korespondencję związaną z niniejszym postępowaniem należy kierować na:", pogrub=True)
    _akapit(d, f"imię i nazwisko/firma: {firma}")
    _akapit(d, f"adres: {adres}")
    _akapit(d, f"e-mail: {_pole(cfg, 'firma_email', 'e-mail')}")
    _akapit(d, f"NIP: {_pole(cfg, 'firma_nip', 'NIP')}   REGON: {_pole(cfg, 'firma_regon', 'REGON')}")
    _akapit(d, f"Osoba do kontaktu / tel.: {_pole(cfg, 'firma_osoba', 'osoba')} / {_pole(cfg, 'firma_tel', 'telefon')}")
    _podpis(d)
    _akapit(d, "Załączniki do oferty:", pogrub=True)
    for z in dane.get("zalaczniki_do_oferty") or []:
        _akapit(d, z, styl="List Bullet")
    d.add_page_break()

    # --- Oświadczenie
    _akapit(d, P.get("oznaczenie_oswiadczenia") or f"Załącznik nr 2 do {DOK_D}", kursywa=True,
            wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _akapit(d, "OŚWIADCZENIE o niepodleganiu wykluczeniu oraz spełnianiu warunków udziału w postępowaniu",
            pogrub=True, rozmiar=12, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    _akapit(d, "Działając w imieniu:")
    _akapit(d, f"nazwa (firma) podmiotu: {firma}")
    _akapit(d, f"adres podmiotu: {adres}")
    _akapit(d, f"składając ofertę w postępowaniu nr {P.get('numer','')} na wybór wykonawcy: {przedmiot}{projekt} "
               f"oświadczam, że:")
    _akapit(d, f"nie podlegam wykluczeniu z postępowania na podstawie {P.get('ref_wykluczenie') or ('SWZ' if pzp else 'treści zapytania ofertowego')}, "
               "w tym nie jestem powiązany osobowo ani kapitałowo z Zamawiającym oraz nie zachodzą wobec mnie przesłanki "
               "zakazu udzielania zamówień wynikające z przepisów dotyczących sankcji wobec Rosji;", styl="List Bullet")
    _akapit(d, f"spełniam warunki udziału w postępowaniu określone w {P.get('ref_warunki') or ('SWZ' if pzp else 'treści zapytania ofertowego')}.",
            styl="List Bullet")
    _podpis(d)
    d.add_page_break()

    # --- Wykaz robót
    _akapit(d, P.get("oznaczenie_wykazu") or f"Załącznik nr 3 do {DOK_D}", kursywa=True,
            wyrownanie=WD_ALIGN_PARAGRAPH.RIGHT)
    _akapit(d, "WYKAZ ZREALIZOWANYCH ROBÓT", pogrub=True, rozmiar=12, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    if P.get("wymagane_roboty"):
        _akapit(d, f"Wymaganie zamawiającego: {P['wymagane_roboty']}", kursywa=True)
    _tabela(d, [["L.p.", "Przedmiot / rodzaj robót", "Wartość brutto [zł]", "Data wykonania", "Miejsce wykonania", "Odbiorca"],
                ["1.", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]"],
                ["2.", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]"],
                ["3.", "", "", "", "", ""]])
    _akapit(d, "Do wykazu załączam dowody potwierdzające należyte wykonanie robót (referencje / protokoły odbioru).")
    _podpis(d)
    d.add_page_break()

    # --- Kierownik budowy
    _akapit(d, "OŚWIADCZENIE O DYSPONOWANIU KIEROWNIKIEM BUDOWY", pogrub=True, rozmiar=12,
            wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    _akapit(d, f"Składając ofertę w postępowaniu nr {P.get('numer','')} oświadczam, że dysponuję osobą, która będzie "
               f"pełnić funkcję kierownika budowy, zgodnie z wymaganiami {P.get('ref_kierownik') or ('SWZ' if pzp else 'zapytania ofertowego')}:")
    if P.get("kierownik_budowy"):
        _akapit(d, f"Wymaganie zamawiającego: {P['kierownik_budowy']}", kursywa=True)
    _tabela(d, [["Imię i nazwisko", "Rodzaj i numer uprawnień", "Doświadczenie", "Podstawa dysponowania"],
                ["[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]", "[UZUPEŁNIJ]"]])
    _podpis(d)
    d.save(sciezka)


def zapisz_analize(dane, cfg, sciezka):
    P = dane["postepowanie"]
    d = _doc()
    d.add_heading(f"Analiza przetargu – {P.get('obiekt') or P.get('numer','')}", level=1)
    _akapit(d, dane.get("podsumowanie", ""))
    d.add_heading("Najważniejsze dane", level=2)
    wiersze = [["Pozycja", "Wartość"]]
    for k, n in [("numer", "Nr postępowania"), ("zamawiajacy_nazwa", "Zamawiający"), ("sposob_skladania", "Sposób składania"),
                 ("termin_skladania", "Termin składania ofert"), ("termin_wykonania", "Termin wykonania"),
                 ("wadium", "Wadium"), ("kryteria", "Kryteria oceny"), ("wynagrodzenie", "Wynagrodzenie"),
                 ("wymagane_roboty", "Wymagane doświadczenie"), ("polisa_oc", "Polisa OC"),
                 ("kierownik_budowy", "Kierownik budowy"), ("budzet_zamawiajacego", "Budżet zamawiającego")]:
        if P.get(k):
            wiersze.append([n, str(P[k])])
    wiersze += [["Cena netto", zl(dane["netto"])], [f"VAT {dane['vat']:.0%}", zl(dane["vat_kwota"])],
                ["Cena brutto", zl(dane["brutto"])],
                ["Pozycje rynkowe (czerwone)", f"{zl(dane['wartosc_rynkowych'])} ({dane['udzial_rynkowych']:.0%} netto)"],
                ["Gwarancja w ofercie", f"{P.get('gwarancja_mies') or cfg.get('gwarancja', 60)} mies."]]
    _tabela(d, wiersze)
    for tytul, klucz in (("Do weryfikacji przed złożeniem", "do_weryfikacji"), ("Ryzyka", "ryzyka"),
                         ("Do uzupełnienia w formularzach", "do_uzupelnienia"),
                         ("Pytania do zamawiającego (gotowe do wklejenia)", "pytania_do_zamawiajacego"),
                         ("Dokumenty do złożenia z ofertą", "zalaczniki_do_oferty")):
        if dane.get(klucz):
            d.add_heading(tytul, level=2)
            for t in dane[klucz]:
                _akapit(d, t, styl="List Number" if klucz == "pytania_do_zamawiajacego" else "List Bullet")
    _akapit(d, f"Wygenerowano automatycznie {dt.datetime.now():%d.%m.%Y %H:%M}. Ceny rynkowe to szacunki AI – "
               "sprawdź je w aktualnych cennikach, hurtowniach lub u podwykonawców.", kursywa=True, rozmiar=8)
    d.save(sciezka)


# ============================================================ pobieranie załączników z Bazy Konkurencyjności

BK = "https://bazakonkurencyjnosci.funduszeeuropejskie.gov.pl"


def _get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Bidivia)"})
    return urllib.request.urlopen(req, timeout=timeout)


def _kandydaci_plikow(o, wynik):
    if isinstance(o, dict):
        nazwa = o.get("fileName") or o.get("filename") or o.get("originalName") or o.get("name")
        ident = o.get("id") or o.get("uuid") or o.get("fileId")
        url = o.get("url") or o.get("downloadUrl") or o.get("path")
        if nazwa and re.search(r"\.(pdf|docx?|xlsx?|zip|rar|7z|jpg|png|ath)$", str(nazwa), re.I) and (ident or url):
            wynik.append((str(nazwa), ident, url))
        for v in o.values():
            _kandydaci_plikow(v, wynik)
    elif isinstance(o, list):
        for v in o:
            _kandydaci_plikow(v, wynik)


def pobierz_zalaczniki_bk(bk_id, folder, log):
    """Próba automatycznego pobrania załączników ogłoszenia BK. Zwraca listę zapisanych plików."""
    dane = None
    for url in (f"{BK}/api/announcements/{bk_id}", f"{BK}/api/announcements/{bk_id}/details"):
        try:
            dane = json.loads(_get(url).read().decode("utf-8"))
            break
        except Exception as e:
            log(f"BK: {url} – {e}")
    if dane is None:
        return []
    kand = []
    _kandydaci_plikow(dane, kand)
    os.makedirs(folder, exist_ok=True)
    zapisane = []
    for nazwa, ident, url in kand:
        adresy = []
        if url:
            adresy.append(url if url.startswith("http") else BK + "/" + url.lstrip("/"))
        if ident:
            adresy += [f"{BK}/api/files/{ident}", f"{BK}/api/files/{ident}/download", f"{BK}/api/attachments/{ident}"]
        for a in adresy:
            try:
                r = _get(a)
                if "json" in (r.headers.get("Content-Type") or "") or "html" in (r.headers.get("Content-Type") or ""):
                    continue
                cel = os.path.join(folder, re.sub(r'[\\/:*?"<>|]', "_", nazwa))
                with open(cel, "wb") as f:
                    shutil.copyfileobj(r, f)
                zapisane.append(cel)
                log(f"Pobrano: {nazwa}")
                break
            except Exception:
                continue
    return zapisane


# ============================================================ interfejs – zakładka Oferty

def bezpieczna_nazwa(s):
    s = re.sub(r'[\\/:*?"<>|]+', " ", s or "oferta").strip()
    return re.sub(r"\s+", "_", s)[:80] or "oferta"


class ZakladkaOferty(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pliki = []          # [ścieżka, uwzględnij]
        self.przetarg = None     # rekord z listy przetargów (opcjonalnie)
        self.folder = None
        self._zbuduj()

    def _zbuduj(self):
        g = ttk.Frame(self)
        g.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Label(g, text="Nazwa oferty (folder):").pack(side="left")
        self.var_nazwa = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_nazwa, width=45).pack(side="left", padx=6)
        self.lbl_przetarg = ttk.Label(g, text="", foreground="#555")
        self.lbl_przetarg.pack(side="left", padx=8)

        b = ttk.Frame(self)
        b.pack(fill="x", padx=10, pady=4)
        ttk.Button(b, text="➕ Dodaj pliki…", command=self.dodaj_pliki).pack(side="left")
        ttk.Button(b, text="📁 Dodaj folder…", command=self.dodaj_folder).pack(side="left", padx=4)
        ttk.Button(b, text="⬇ Pobierz z ogłoszenia", command=self.pobierz).pack(side="left", padx=4)
        ttk.Button(b, text="✔/✘ Uwzględnij", command=self.przelacz).pack(side="left", padx=4)
        ttk.Button(b, text="🗑 Usuń wszystkie pliki", command=self.usun_wszystkie).pack(side="left", padx=4)
        self.lbl_rozmiar = ttk.Label(b, text="")
        self.lbl_rozmiar.pack(side="right")

        rama = ttk.Frame(self)
        rama.pack(fill="both", expand=True, padx=10, pady=4)
        self.tree = ttk.Treeview(rama, columns=("u", "plik", "typ", "rozmiar"), show="headings", height=9)
        for k, n, w in (("u", "✔", 40), ("plik", "Plik", 560), ("typ", "Typ", 80), ("rozmiar", "Rozmiar", 90)):
            self.tree.heading(k, text=n)
            self.tree.column(k, width=w, anchor="center" if k != "plik" else "w")
        self.tree.bind("<Double-1>", lambda e: self.przelacz())
        self.tree.bind("<Delete>", lambda e: self.usun())
        sb = ttk.Scrollbar(rama, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        ttk.Label(self, text="Podwójne kliknięcie – uwzględnij/pomiń plik; klawisz Delete – usuń zaznaczone.",
                  foreground="#777").pack(anchor="w", padx=10)

        w = ttk.Frame(self)
        w.pack(fill="x", padx=10, pady=4)
        ttk.Label(w, text="Wskazówki dla AI (opcjonalnie, np. „gwarancja 60 mies., wysokość budynku 18 m”):").pack(anchor="w")
        self.txt_wsk = tk.Text(w, height=3, wrap="word", font=("Segoe UI", 10))
        self.txt_wsk.pack(fill="x")

        a = ttk.Frame(self)
        a.pack(fill="x", padx=10, pady=6)
        ttk.Button(a, text="⚙ Przygotuj ofertę i kosztorys", style="Akcent.TButton", command=self.generuj).pack(side="left")
        ttk.Button(a, text="📂 Otwórz folder oferty", command=self.otworz_folder).pack(side="left", padx=6)
        ttk.Button(a, text="📦 Zapotrzebowanie materiałowe", command=self.do_materialow).pack(side="left", padx=6)
        ttk.Label(a, text="Oferta trwa zwykle 2–6 minut. Pliki PDF (także skany) AI czyta bezpośrednio.",
                  foreground="#777").pack(side="left", padx=10)

        self.txt_wynik = tk.Text(self, height=12, wrap="word", font=("Segoe UI", 10), state="disabled",
                                 background="#fafafa", relief="flat", padx=10, pady=8)
        self.txt_wynik.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.txt_wynik.tag_configure("h", font=("Segoe UI", 11, "bold"))
        self.txt_wynik.tag_configure("r", foreground="#c00000")

    # ---------- lista plików
    def ustaw_przetarg(self, numer, rekord):
        self.przetarg = dict(rekord, numer=numer)
        self.var_nazwa.set(bezpieczna_nazwa(rekord.get("przedmiot", "")[:50] or numer))
        self.lbl_przetarg.config(text=f"Przetarg: {numer} ({rekord.get('zrodlo','')})")
        self.folder = None

    def _folder(self):
        baza = self.app.cfg.get("folder_ofert") or os.path.join(os.path.expanduser("~"), "Documents", "Oferty")
        self.folder = os.path.join(baza, bezpieczna_nazwa(self.var_nazwa.get()))
        os.makedirs(self.folder, exist_ok=True)
        return self.folder

    def _dodaj(self, sciezki):
        tmp = os.path.join(self._folder(), "dokumenty_przetargu")
        for s in sciezki:
            if czy_archiwum(s):
                try:
                    for p in rozpakuj_zip(s, os.path.join(tmp, os.path.splitext(os.path.basename(s))[0])):
                        self.pliki.append([p, not p.lower().endswith((".dwg", ".dxf", ".ath", ".rar"))])
                except zipfile.BadZipFile:
                    messagebox.showerror("Oferty", f"Uszkodzony plik ZIP: {s}")
            elif os.path.isfile(s):
                self.pliki.append([s, True])
        widziane, unik = set(), []
        for p in self.pliki:
            if p[0] not in widziane:
                widziane.add(p[0])
                unik.append(p)
        self.pliki = unik
        self.odswiez()

    def dodaj_pliki(self):
        s = filedialog.askopenfilenames(title="Wybierz dokumenty przetargu",
                                        filetypes=[("Dokumenty", "*.pdf *.doc *.docx *.xlsx *.zip *.jpg *.jpeg *.png *.txt"),
                                                   ("Wszystkie", "*.*")])
        if s:
            self._dodaj(list(s))

    def dodaj_folder(self):
        f = filedialog.askdirectory(title="Wybierz folder z dokumentami przetargu")
        if f:
            self._dodaj([os.path.join(r, n) for r, _, ns in os.walk(f) for n in ns])

    def przelacz(self):
        for iid in self.tree.selection():
            self.pliki[int(iid)][1] = not self.pliki[int(iid)][1]
        self.odswiez()

    def usun(self):
        do_usun = {int(i) for i in self.tree.selection()}
        self.pliki = [p for i, p in enumerate(self.pliki) if i not in do_usun]
        self.odswiez()

    def usun_wszystkie(self):
        if not self.pliki:
            return
        if not messagebox.askyesno("Oferty", f"Usunąć wszystkie pliki ({len(self.pliki)}) z listy?\n\n"
                                             "Skasowane zostaną też kopie rozpakowane lub pobrane przez program "
                                             "(folder „dokumenty_przetargu”). Twoje oryginalne pliki zostaną na dysku."):
            return
        self.pliki = []
        if self.folder:
            kopie = os.path.join(self.folder, "dokumenty_przetargu")
            if os.path.isdir(kopie):
                shutil.rmtree(kopie, ignore_errors=True)
        self.odswiez()

    def odswiez(self):
        self.tree.delete(*self.tree.get_children())
        suma = 0
        for i, (p, u) in enumerate(self.pliki):
            r = os.path.getsize(p) if os.path.exists(p) else 0
            rozsz = os.path.splitext(p)[1].lower()
            if u:
                suma += r * (4 / 3 if rozsz in ROZSZ_PDF or rozsz in ROZSZ_OBRAZ else 0.3)
            self.tree.insert("", "end", iid=str(i), values=("✔" if u else "✘", p, rozsz.strip("."),
                                                            f"{r / 1024 / 1024:.1f} MB"))
        kolor = "#c00000" if suma > MAX_BAJTOW_ZAPYTANIA else "#333"
        self.lbl_rozmiar.config(text=f"Do wysłania ok. {suma / 1024 / 1024:.1f} MB z 50 MB", foreground=kolor)

    def pobierz(self):
        if not self.przetarg:
            messagebox.showinfo("Oferty", "Wybierz przetarg na liście w zakładce Przetargi i kliknij „📝 Przygotuj ofertę”.")
            return
        bk_id = self.przetarg.get("bk_id")
        link = self.przetarg.get("link")
        if not bk_id:
            if link:
                webbrowser.open(link)
            messagebox.showinfo("Oferty", "Dla ogłoszeń z BZP dokumenty są zwykle na platformie zamawiającego. "
                                          "Otworzyłem ogłoszenie – pobierz dokumenty i dodaj je przyciskiem „Dodaj pliki”.")
            return
        folder = os.path.join(self._folder(), "dokumenty_przetargu")
        self.app._start("Pobieram załączniki z Bazy Konkurencyjności…", self._w_pobierz, bk_id, folder, link)

    def _w_pobierz(self, bk_id, folder, link):
        pliki = pobierz_zalaczniki_bk(bk_id, folder, self.app.log)
        if pliki:
            self.app.q.put(("wywolaj", self._dodaj, (pliki,)))
            self.app.q.put(("koniec", f"Pobrano {len(pliki)} plików z ogłoszenia."))
        else:
            if link:
                webbrowser.open(link)
            self.app.q.put(("koniec", "Nie udało się pobrać plików automatycznie – pobierz je ze strony ogłoszenia "
                                      "(otworzyłem ją w przeglądarce) i dodaj przyciskiem „Dodaj pliki”."))

    # ---------- generowanie
    def generuj(self):
        cfg = self.app.cfg
        if not cfg.get("api_key"):
            messagebox.showwarning("Oferty", "Najpierw wpisz klucz API Claude w Ustawieniach.")
            return
        wybrane = [p for p, u in self.pliki if u]
        if not wybrane:
            messagebox.showinfo("Oferty", "Dodaj dokumenty przetargu (zapytanie/SWZ, przedmiar, umowa, formularze, audyt).")
            return
        if not self.var_nazwa.get().strip():
            self.var_nazwa.set(dt.date.today().isoformat())
        folder = self._folder()
        wsk = self.txt_wsk.get("1.0", "end").strip()
        cennik = list(self.app.cennik) if cfg.get("ceny_z_cennika") else []
        self.app._start("Przygotowuję ofertę…", self._w_generuj, json.loads(json.dumps(cfg)), wybrane, folder, wsk,
                        self.przetarg, cennik)

    def _w_generuj(self, cfg, wybrane, folder, wsk, przetarg, cennik):
        log = self.app.log
        content, suma, ostrz = [], 0, []
        for p in wybrane:
            bloki, b, o = przygotuj_blok(p)
            if o:
                ostrz.append(o)
                log(o)
            content += bloki
            suma += b
        if suma > MAX_BAJTOW_ZAPYTANIA:
            self.app.q.put(("koniec", f"Za dużo danych ({suma / 1024 / 1024:.0f} MB). Odznacz (✘) rysunki i duże "
                                      "załączniki dokumentacji projektowej, zostaw zapytanie, przedmiar, umowę, audyt."))
            return
        content.append({"type": "text", "text": zbuduj_polecenie(cfg, cennik, przetarg, wsk)})
        log(f"Wysyłam do AI {len(wybrane)} plików (ok. {suma / 1024 / 1024:.1f} MB); "
            + (f"cennik firmy: {len(cennik)} pozycji" if cennik else "wycena wyłącznie rynkowa"))

        def postep(n):
            self.app.q.put(("status", f"AI przygotowuje kosztorys… ({n // 1000} tys. znaków)"))
        try:
            txt, powod = claude_stream(cfg, SYSTEM_OFERTA, content, postep=postep)
        except urllib.error.HTTPError as e:
            tresc = e.read().decode("utf-8", "ignore")[:500]
            self.app.q.put(("koniec", f"Błąd API {e.code}: {tresc}"))
            return
        with open(os.path.join(folder, "odpowiedz_ai.json.txt"), "w", encoding="utf-8") as f:
            f.write(txt)
        if powod == "max_tokens":
            log("Uwaga: odpowiedź AI została ucięta (limit długości) – kosztorys może być niepełny.")
        dane = przelicz(wyciagnij_json(txt))
        nazwa = bezpieczna_nazwa(os.path.basename(folder))
        pk = os.path.join(folder, f"Kosztorys_ofertowy_{nazwa}.xlsx")
        pf = os.path.join(folder, f"Oferta_{nazwa}_formularze.docx")
        pa = os.path.join(folder, f"Analiza_przetargu_{nazwa}.docx")
        zapisz_kosztorys(dane, cfg, pk)
        zapisz_formularze(dane, cfg, pf)
        zapisz_analize(dane, cfg, pa)
        dane["_ostrzezenia"] = ostrz
        self.app.q.put(("wywolaj", self.pokaz_wynik, (dane, [pk, pf, pa])))
        self.app.q.put(("koniec", f"Oferta gotowa: brutto {zl(dane['brutto'])}. Pliki w folderze oferty."))

    def pokaz_wynik(self, dane, pliki):
        self.ostatni_kosztorys = pliki[0]
        tab = getattr(self.app, "tab_materialy", None)
        if tab is not None:
            tab.ustaw_kosztorys(pliki[0])
        P = dane["postepowanie"]
        t = self.txt_wynik
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.insert("end", f"{P.get('nazwa_zamowienia','')}\n", "h")
        t.insert("end", f"Nr {P.get('numer','')} | termin składania: {P.get('termin_skladania','')} | "
                        f"wadium: {P.get('wadium','')}\n\n")
        t.insert("end", f"Netto: {zl(dane['netto'])}   VAT {dane['vat']:.0%}: {zl(dane['vat_kwota'])}   "
                        f"BRUTTO: {zl(dane['brutto'])}\n", "h")
        t.insert("end", f"Pozycje rynkowe (czerwone): {zl(dane['wartosc_rynkowych'])} = "
                        f"{dane['udzial_rynkowych']:.0%} ceny netto\n\n", "r")
        t.insert("end", dane.get("podsumowanie", "") + "\n\n")
        for tytul, k in (("Do weryfikacji przed złożeniem", "do_weryfikacji"), ("Do uzupełnienia", "do_uzupelnienia")):
            if dane.get(k):
                t.insert("end", tytul + "\n", "h")
                for i, x in enumerate(dane[k], 1):
                    t.insert("end", f"{i}. {x}\n")
                t.insert("end", "\n")
        t.insert("end", "Pliki:\n", "h")
        for p in pliki:
            t.insert("end", p + "\n")
        t.configure(state="disabled")
        self.otworz_folder()

    def do_materialow(self):
        tab = getattr(self.app, "tab_materialy", None)
        if tab is None:
            return
        if getattr(self, "ostatni_kosztorys", None):
            tab.ustaw_kosztorys(self.ostatni_kosztorys)
        self.app.nb.select(tab)

    def otworz_folder(self):
        f = self.folder or (self.var_nazwa.get().strip() and self._folder())
        if f and os.path.isdir(f):
            try:
                os.startfile(f)
            except AttributeError:
                webbrowser.open("file://" + f)


# ============================================================ interfejs – zakładka Cennik

class ZakladkaCennik(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        g = ttk.Frame(self)
        g.pack(fill="x", padx=10, pady=8)
        ttk.Button(g, text="📥 Importuj kosztorys (xlsx)…", command=self.importuj).pack(side="left")
        ttk.Button(g, text="🗑 Usuń zaznaczone", command=self.usun).pack(side="left", padx=6)
        ttk.Label(g, text="   Szukaj:").pack(side="left")
        self.var = tk.StringVar()
        self.var.trace_add("write", lambda *a: self.odswiez())
        ttk.Entry(g, textvariable=self.var, width=30).pack(side="left", padx=4)
        self.lbl = ttk.Label(g, text="")
        self.lbl.pack(side="right")
        ttk.Label(self, text="Cennik jest używany tylko wtedy, gdy w Ustawieniach włączysz „Wyceniaj oferty cenami z poprzednich "
                             "kosztorysów”. Domyślnie oferty są wyceniane wyłącznie cenami rynkowymi.",
                  foreground="#c00000").pack(fill="x", padx=10)
        ttk.Label(self, text="Pozycje „własna” (czarne) pochodzą z Twoich kosztorysów szczegółowych i mają pierwszeństwo. "
                             "Pozycje „rynkowa” (czerwone) to wcześniejsze szacunki – AI użyje ich dla spójności, "
                             "ale nadal oznaczy je na czerwono. Import rozpoznaje czerwone wiersze automatycznie.",
                  wraplength=1100, foreground="#555").pack(fill="x", padx=10)
        rama = ttk.Frame(self)
        rama.pack(fill="both", expand=True, padx=10, pady=8)
        kol = (("typ", "Typ", 70), ("opis", "Opis", 520), ("jm", "j.m.", 50), ("cena", "Cena netto", 90),
               ("zrodlo", "Źródło", 300), ("oferta", "Kosztorys", 110))
        self.tree = ttk.Treeview(rama, columns=[k for k, _, _ in kol], show="headings")
        for k, n, w in kol:
            self.tree.heading(k, text=n)
            self.tree.column(k, width=w, anchor="e" if k == "cena" else "w")
        self.tree.tag_configure("rynkowa", foreground="#c00000")
        sb = ttk.Scrollbar(rama, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.odswiez()

    def odswiez(self):
        self.tree.delete(*self.tree.get_children())
        f = self.var.get().lower()
        for i, p in enumerate(self.app.cennik):
            if f and f not in (p["opis"] + p["zrodlo"] + p.get("oferta", "")).lower():
                continue
            self.tree.insert("", "end", iid=str(i), tags=(p["typ"],),
                             values=(p["typ"], p["opis"], p["jm"], f"{p['cena']:.2f}", p["zrodlo"], p.get("oferta", "")))
        wl = sum(p["typ"] == "własna" for p in self.app.cennik)
        self.lbl.config(text=f"Własne: {wl}   rynkowe: {len(self.app.cennik) - wl}")

    def importuj(self):
        pliki = filedialog.askopenfilenames(title="Wybierz kosztorysy ofertowe", filetypes=[("Excel", "*.xlsx")])
        dodane = 0
        for s in pliki:
            try:
                dodane += scal(self.app.cennik, importuj_kosztorys(s))
            except Exception as e:
                messagebox.showerror("Cennik", f"{os.path.basename(s)}: {e}")
        if pliki:
            self.app.zapisz_cennik()
            self.odswiez()
            messagebox.showinfo("Cennik", f"Dodano {dodane} nowych pozycji.")

    def usun(self):
        sel = {int(i) for i in self.tree.selection()}
        if sel and messagebox.askyesno("Cennik", f"Usunąć {len(sel)} pozycji z cennika?"):
            self.app.cennik[:] = [p for i, p in enumerate(self.app.cennik) if i not in sel]
            self.app.zapisz_cennik()
            self.odswiez()


# ---------------------------------------------------------------- miejsca do uzupełnienia na żółto (dokumenty zamawiającego)
RE_DO_UZUPELNIENIA = re.compile(r"\[UZUPEŁNIJ[^\]]*\]|\.{4,}|…{2,}|(?<!\S)(?:\. ){3,}\.|_{4,}")


def _akapity_dokumentu(doc):
    def z_tabel(tabele):
        for t in tabele:
            for w in t.rows:
                for c in w.cells:
                    yield from c.paragraphs
                    yield from z_tabel(c.tables)
    yield from doc.paragraphs
    yield from z_tabel(doc.tables)
    for s in doc.sections:
        for cz in (s.header, s.footer):
            try:
                yield from cz.paragraphs
                yield from z_tabel(cz.tables)
            except Exception:
                pass


def zaznacz_do_uzupelnienia(doc):
    """Każde miejsce do uzupełnienia na żółto: [UZUPEŁNIJ…], wykropkowane pola, podkreślenia do wpisania. Formatowanie fragmentów zachowane
    (fragment wydzielany z tego samego przebiegu tekstu z kopią jego formatowania). Zwraca liczbę zaznaczeń."""
    import copy as _copy
    from docx.enum.text import WD_COLOR_INDEX
    licz = 0
    for p in _akapity_dokumentu(doc):
        for run in list(p.runs):
            t = run.text
            if not t or not RE_DO_UZUPELNIENIA.search(t):
                continue
            czesci, poz = [], 0
            for m in RE_DO_UZUPELNIENIA.finditer(t):
                if m.start() > poz:
                    czesci.append((t[poz:m.start()], False))
                czesci.append((m.group(0), True))
                poz = m.end()
            if poz < len(t):
                czesci.append((t[poz:], False))
            r0 = run._r
            for k, (tekst, zolty) in enumerate(czesci):
                if k == 0:
                    run.text = tekst
                    if zolty:
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                        licz += 1
                    continue
                nowy = _copy.deepcopy(r0)
                r0.addnext(nowy)
                r0 = nowy
                from docx.text.run import Run
                rn = Run(nowy, p)
                rn.text = tekst
                rn.font.highlight_color = WD_COLOR_INDEX.YELLOW if zolty else None
                licz += 1 if zolty else 0
        # „[UZUPEŁNIJ…]” rozbite na kilka przebiegów tekstu – zaznaczenie wszystkich przebiegów, które go tworzą
        pelny = "".join(r.text for r in p.runs)
        if "[UZUPEŁNIJ" in pelny:
            poz = 0
            zakresy = [(m.start(), m.end()) for m in re.finditer(r"\[UZUPEŁNIJ[^\]]*\]", pelny)]
            for r in p.runs:
                a, b = poz, poz + len(r.text)
                if r.text and any(a < z2 and b > z1 for z1, z2 in zakresy) and r.font.highlight_color != WD_COLOR_INDEX.YELLOW:
                    r.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    licz += 1
                poz = b
    return licz


def zapisz_z_zaznaczeniem(doc, sciezka):
    zaznacz_do_uzupelnienia(doc)
    doc.save(sciezka)
