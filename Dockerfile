FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 DATA_DIR=/data TZ=Europe/Warsaw
# mniej „rozproszonej” pamięci w programie wielowątkowym (ważne na planie 512 MB)
ENV MALLOC_ARENA_MAX=2
# antiword – odczyt starych plików Word (.doc); bez niego program użyje odczytu awaryjnego
RUN apt-get update && apt-get install -y --no-install-recommends antiword && rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
COPY . .
# Trzy układy repozytorium: (1) katalog app/ – kopiowany w całości; (2) płaski (paczki „do podmiany” na GitHubie) – pliki .html/.js/.css/.pdf
# z katalogu głównego trafiają do /app/static; (3) kopia robocza z katalogiem static/ – najpierw static/, potem pliki z katalogu głównego,
# które mają pierwszeństwo (repozytorium płaskie działa jak dotąd). Brak plików .html/.js/.css w katalogu głównym nie przerywa budowania.
RUN set -e; \
    pip install --no-cache-dir -r requirements.txt; \
    mkdir -p /app/static /data; \
    if [ -d app ]; then cp -r app/. /app/; \
    else cp *.py *.pyw /app/; \
      if [ -d static ]; then cp -r static/. /app/static/; fi; \
      for f in *.html *.js *.css *.pdf; do \
        if [ -f "$f" ]; then \
          if [ -f "static/$f" ] && ! cmp -s "$f" "static/$f"; then echo "UWAGA: $f z katalogu głównego różni się od static/$f – użyto pliku z katalogu głównego"; fi; \
          cp "$f" /app/static/; \
        fi; done; fi; \
    for f in serwer.py tk_stub.py agent_przetargowy.pyw modul_oferty.py modul_materialy.py modul_harmonogram.py \
             cennik_import.py cennik_domyslny.py ceny_rynkowe.py bip.py region.py \
             static/index.html static/login.html static/app.js static/styl.css; do \
      test -f /app/$f || { echo "BRAK PLIKU W REPOZYTORIUM: $f"; exit 1; }; done; \
    cd / && rm -rf /src
WORKDIR /app
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -w 1 --threads 8 --timeout 120 -b 0.0.0.0:${PORT:-8000} serwer:app"]
