# -*- coding: utf-8 -*-
"""
Moduł budowy (zakładka „W realizacji”):
 - zdjęcia z budowy (miniatury, zmniejszanie dużych zdjęć z telefonu),
 - pogoda do raportów dziennych – dziennik pomocniczy wykonawcy (Open-Meteo, bez klucza API),
 - raporty dzienne (dziennik pomocniczy, nie dziennik budowy z art. 45 Prawa budowlanego) i lista usterek jako dokumenty Word.
"""
import datetime as dt
import json
import os
import urllib.parse
import urllib.request

import modul_oferty as MO

KODY_POGODY = {0: "bezchmurnie", 1: "przeważnie pogodnie", 2: "częściowe zachmurzenie", 3: "pochmurno", 45: "mgła", 48: "mgła szronowa",
               51: "lekka mżawka", 53: "mżawka", 55: "gęsta mżawka", 56: "marznąca mżawka", 57: "marznąca mżawka",
               61: "słaby deszcz", 63: "deszcz", 65: "ulewny deszcz", 66: "marznący deszcz", 67: "marznący deszcz",
               71: "słaby śnieg", 73: "śnieg", 75: "intensywny śnieg", 77: "ziarnisty śnieg", 80: "przelotny deszcz",
               81: "przelotne opady", 82: "gwałtowne opady", 85: "przelotny śnieg", 86: "intensywne opady śniegu",
               95: "burza", 96: "burza z gradem", 99: "silna burza z gradem"}


# ============================================================ zdjęcia

def zapisz_zdjecie(plik_flask, folder, zid):
    """Zapisuje zdjęcie (zmniejszone do 2000 px) i miniaturę 480 px. Zwraca (plik, miniatura)."""
    os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(plik_flask.filename or "")[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif"):
        ext = ".jpg"
    sciezka = os.path.join(folder, zid + ext)
    plik_flask.save(sciezka)
    mini = None
    try:
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(sciezka))
        im = im.convert("RGB")
        if max(im.size) > 2000:
            im.thumbnail((2000, 2000))
        nowa = os.path.join(folder, zid + ".jpg")
        im.save(nowa, "JPEG", quality=82, optimize=True)
        if nowa != sciezka:
            os.remove(sciezka)
            sciezka = nowa
        m = im.copy()
        m.thumbnail((480, 480))
        mini = os.path.join(folder, zid + "_m.jpg")
        m.save(mini, "JPEG", quality=75, optimize=True)
    except ImportError:
        pass  # bez biblioteki Pillow zdjęcie zostaje w oryginale
    except Exception:
        if ext != ".heic":  # HEIC (iPhone) bez wtyczki zostaje w oryginale; inny plik, którego nie da się odczytać jako obrazu, nie jest zdjęciem
            try:
                os.remove(sciezka)
            except OSError:
                pass
            raise ValueError(f"Plik „{plik_flask.filename}” nie jest zdjęciem (JPG, PNG, WEBP, GIF, HEIC).")
    return os.path.basename(sciezka), (os.path.basename(mini) if mini else None)


# ============================================================ pogoda

def pogoda(lat, lon, dzien):
    """Pogoda dzienna z Open-Meteo: {'opis', 'tmin', 'tmax', 'opady'} albo None."""
    d = dzien.isoformat()
    dni_temu = (dt.date.today() - dzien).days
    baza = "https://api.open-meteo.com/v1/forecast" if dni_temu <= 60 else "https://archive-api.open-meteo.com/v1/archive"
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "start_date": d, "end_date": d, "timezone": "Europe/Warsaw",
                                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum"})
    try:
        req = urllib.request.Request(f"{baza}?{q}", headers={"User-Agent": "Bidivia/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            dz = json.loads(r.read().decode("utf-8")).get("daily", {})
        kod = (dz.get("weathercode") or [None])[0]
        return {"opis": KODY_POGODY.get(kod, "brak danych"), "tmin": (dz.get("temperature_2m_min") or [None])[0],
                "tmax": (dz.get("temperature_2m_max") or [None])[0], "opady": (dz.get("precipitation_sum") or [None])[0]}
    except Exception:
        return None


def opis_pogody(p):
    if not p:
        return ""
    t = p["opis"]
    if p.get("tmin") is not None and p.get("tmax") is not None:
        t += f", temp. {p['tmin']:.0f}…{p['tmax']:.0f}°C"
    if p.get("opady"):
        t += ", opady " + f"{p['opady']:.1f}".replace(".", ",") + " mm"
    return t


# ============================================================ dokumenty Word

def _dpl(s):
    try:
        return dt.date.fromisoformat(s).strftime("%d.%m.%Y")
    except (TypeError, ValueError):
        return s or ""


def dziennik_docx(sciezka, nazwa_budowy, r, wpisy, folder_zdjec, cfg):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("RAPORTY DZIENNE (DZIENNIK POMOCNICZY)", pogrub=True, rozmiar=15, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(nazwa_budowy, pogrub=True, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"Adres: {r.get('adres') or '–'} · Umowa: {r.get('umowa_nr') or '–'} · Wykonawca: {cfg.get('firma_nazwa', '')} · "
      f"Kierownik budowy: {r.get('kierownik') or '–'}", rozmiar=9, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A("Dokument pomocniczy wykonawcy. To nie jest dziennik budowy w rozumieniu art. 45 Prawa budowlanego (elektroniczny dziennik budowy EDB "
      "albo dziennik w formie papierowej wydany przez organ). Wpisy do dziennika budowy dokonuje uprawniona osoba w EDB lub w dzienniku papierowym.",
      kursywa=True, rozmiar=8, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    zdj = {z["id"]: z for z in r.get("zdjecia", []) if not z.get("archiwum")}  # zdjęcia usunięte (archiwum) – poza wydrukiem
    for w in sorted(wpisy, key=lambda x: x["data"]):
        d.add_heading(f"{_dpl(w['data'])} ({['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela'][dt.date.fromisoformat(w['data']).weekday()]})", level=2)
        wiersze = [["Pogoda", w.get("pogoda") or "–"], ["Pracownicy na budowie", w.get("pracownicy") or "–"],
                   ["Wykonane prace", w.get("prace") or "–"], ["Dostawy / materiały", w.get("materialy") or "–"],
                   ["Sprzęt", w.get("sprzet") or "–"], ["Zdarzenia, polecenia, uwagi", w.get("uwagi") or "–"]]
        t = MO._tabela(d, [["Pole", "Treść"]] + wiersze)
        for wiersz in t.rows:
            wiersz.cells[0].width = Cm(4.5)
            wiersz.cells[1].width = Cm(12.5)
        fotki = [zdj[i] for i in w.get("zdjecia", []) if i in zdj][:6]
        for z in fotki:
            p = os.path.join(folder_zdjec, z.get("miniatura") or z["plik"])
            try:
                d.add_picture(p, width=Cm(7.5))
                A(z.get("opis") or "", kursywa=True, rozmiar=8)
            except Exception:
                pass
        if w.get("autor"):
            A(f"Wpis: {w['autor']}" + (f", zmienił: {w['zmienil']}" if w.get("zmienil") else "") + (f" · zapisano {w['zapisano']}" if w.get("zapisano") else "")
              + (f" · wersja {w['wersja']} (poprzednie w historii wpisów)" if (w.get("wersja") or 1) > 1 else ""), rozmiar=8, kursywa=True)
    d.save(sciezka)


def usterki_docx(sciezka, nazwa_budowy, r, usterki, folder_zdjec, cfg):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm
    d = MO._doc()
    A = lambda t, **k: MO._akapit(d, t, **k)
    A("LISTA USTEREK I ZADAŃ", pogrub=True, rozmiar=15, wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    A(f"{nazwa_budowy} · stan na {dt.date.today():%d.%m.%Y}", wyrownanie=WD_ALIGN_PARAGRAPH.CENTER)
    wiersze = [["Nr", "Rodzaj", "Opis", "Lokalizacja", "Odpowiedzialny", "Termin", "Status"]]
    for i, u in enumerate(usterki, 1):
        wiersze.append([str(i), u.get("typ", ""), (u.get("tytul", "") + ("\n" + u["opis"] if u.get("opis") else "")),
                        u.get("lokalizacja", ""), u.get("osoba", ""), _dpl(u.get("termin")), u.get("status", "")])
    MO._tabela(d, wiersze)
    zdj = {z["id"]: z for z in r.get("zdjecia", []) if not z.get("archiwum")}  # zdjęcia usunięte (archiwum) – poza wydrukiem
    fotki = [(i, zdj[u["zdjecie"]]) for i, u in enumerate(usterki, 1) if u.get("zdjecie") in zdj]
    if fotki:
        d.add_heading("Dokumentacja zdjęciowa", level=2)
        for i, z in fotki:
            try:
                d.add_picture(os.path.join(folder_zdjec, z.get("miniatura") or z["plik"]), width=Cm(7))
                A(f"Poz. {i}: {z.get('opis') or ''}", kursywa=True, rozmiar=8)
            except Exception:
                pass
    d.save(sciezka)
