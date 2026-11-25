"use strict";
// ================================================================ ikony
const IK = {
  logo: '<path d="M2 20h20"/><path d="M5 20V8l7-5 7 5v12"/><path d="M9 20v-6h6v6"/>',
  szukaj: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  ciezarowka: '<path d="M2 6h12v10H2z"/><path d="M14 9h4l4 4v3h-8"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/>',
  ludzie: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18.5 14.3c2 .8 3 2.8 3 5.7"/>',
  suwaki: '<path d="M4 6h9M17 6h3M4 12h3M11 12h9M4 18h11M19 18h1"/><circle cx="15" cy="6" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="17" cy="18" r="2"/>',
  wyloguj: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
  iskra: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7L19 20l-.7-1.8-1.8-.7 1.8-.7z"/>',
  dokument: '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="M8 13h8M8 17h5"/>',
  wgraj: '<path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
  pobierz: '<path d="M12 4v12"/><path d="m7 11 5 5 5-5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
  kask: '<path d="M2 18h20"/><path d="M4 18v-2a8 8 0 0 1 16 0v2"/><path d="M10 8V5h4v3"/>',
  faktura: '<path d="M6 2h12v20l-3-2-3 2-3-2-3 2z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
  portfel: '<path d="M3 7a2 2 0 0 1 2-2h13v4"/><path d="M3 7v11a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2z"/><circle cx="16" cy="14.5" r="1.3"/>',
  protokol: '<path d="M9 3h6v3H9z"/><path d="M8 5H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><path d="m9 14 2 2 4-4"/>',
  tabela: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 4v16M15 4v16"/>',
  teczka: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
  trofeum: '<path d="M8 21h8M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3a3 3 0 0 1-3 4M7 5H4a3 3 0 0 0 3 4"/>',
  kalkulator: '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8v4H8z"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
  ksiazka: '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 21.5A2.5 2.5 0 0 1 6.5 19H20v3H6.5"/><path d="M9 7h7M9 11h5"/>',
  czat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12z"/><path d="M8 11h8M8 14h5"/>',
  aparat: '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
  alarm: '<path d="M12 3 2 21h20z"/><path d="M12 10v5M12 18h.01"/>',
  wizytowka: '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="11" r="2.2"/><path d="M4.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4"/><path d="M14 10h5M14 13h4"/>',
  siatka: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
  kosz: '<path d="M4 7h16"/><path d="M10 11v6M14 11v6"/><path d="M6 7l1 13h10l1-13"/><path d="M9 7V4h6v3"/>',
  paczka: '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/>',
  kalendarz: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
  wyslij: '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
  oko: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  zegar: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  procent: '<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
  cofnij: '<path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
  zapisz: '<path d="M5 3h11l3 3v13a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M7 3v5h8V3M7 21v-7h10v7"/>',
  odswiez: '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
  link: '<path d="M14 4h6v6"/><path d="M20 4 10 14"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  flaga: '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  przelacz: '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
};
const ik = (n, cls = "") => IK[n] ? `<svg class="ik ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${IK[n]}</svg>` : "";
function wstawIkony(root = document) {
  root.querySelectorAll("[data-ik]:not([data-ik-ok])").forEach(el => { el.insertAdjacentHTML("afterbegin", ik(el.dataset.ik)); el.setAttribute("data-ik-ok", "1"); });
}
// ---------- wygodniejsze tabele: sortowanie po kliknięciu nagłówka i filtr przy dłuższych tabelach
const wartoscKomorki = t => {
  const s = (t || "").trim();
  let m = s.match(/^(\d{2})\.(\d{2})\.(\d{4})/); if (m) return +(m[3] + m[2] + m[1]);
  m = s.match(/^(\d{4})-(\d{2})-(\d{2})/); if (m) return +(m[1] + m[2] + m[3]);
  const n = s.replace(/zł|%|h|\s/g, "").replace(",", "."); if (/^-?\d+(\.\d+)?$/.test(n)) return parseFloat(n);
  return s.toLowerCase();
};
function ulepszTabele() {
  document.querySelectorAll("table.tabela:not([data-ulepszona]):not(.wn-k-tab):not(.poz-tab):not(.rm-tab):not(.pw-plat)").forEach(tab => {
    tab.dataset.ulepszona = "1";
    const wiersze = [...tab.rows]; if (wiersze.length < 3 || !wiersze[0].querySelector("th")) return;
    const nag = wiersze[0];
    [...nag.cells].forEach((th, i) => {
      if (th.onclick || th.classList.contains("sort") || th.getAttribute("onclick") || !th.textContent.trim()) return;
      th.classList.add("sortowalna"); th.title = "Kliknij, aby posortować";
      th.addEventListener("click", () => {
        const kier = th.dataset.kier === "rosn" ? "mal" : "rosn";
        [...nag.cells].forEach(c => { delete c.dataset.kier; });
        th.dataset.kier = kier;
        const dane = [...tab.rows].slice(1).filter(r => !r.classList.contains("km-razem") && !/RAZEM|Netto etapu|Brutto etapu|Narastająco/.test(r.cells[0]?.textContent || ""));
        const stale = [...tab.rows].slice(1).filter(r => !dane.includes(r));
        dane.sort((a, b) => { const x = wartoscKomorki(a.cells[i]?.textContent), y = wartoscKomorki(b.cells[i]?.textContent);
          return (x > y ? 1 : x < y ? -1 : 0) * (kier === "rosn" ? 1 : -1); });
        const rodzic = wiersze[1].parentNode; dane.concat(stale).forEach(r => rodzic.appendChild(r));
      });
    });
    const okno = tab.closest(".tabela-okno");
    if (okno && wiersze.length > 9 && !(okno.previousElementSibling || {}).classList?.contains("filtr-tabeli")) {
      const f = document.createElement("input"); f.className = "filtr-tabeli"; f.placeholder = `Szukaj w tabeli (${wiersze.length - 1} wierszy)…`;
      f.addEventListener("input", () => { const q = f.value.toLowerCase(); [...tab.rows].slice(1).forEach(r => r.style.display = !q || r.textContent.toLowerCase().includes(q) ? "" : "none"); });
      okno.before(f);
    }
  });
}
let _ulepszT = null;
new MutationObserver(() => { wstawIkony(); clearTimeout(_ulepszT); _ulepszT = setTimeout(ulepszTabele, 150); }).observe(document.body, {childList: true, subtree: true});
wstawIkony();
// ================================================================ narzędzia
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
const jsa = s => esc(JSON.stringify(String(s ?? "")));  // napis jako argument JS w atrybucie onclick="f(${jsa(x)})" – bezpieczny także z apostrofem (np. „O'Neill”)
// tekst jako argument JS w cudzysłowie pojedynczym wewnątrz atrybutu HTML (onclick="f('${escA(x)}')"): przeglądarka zamienia &#39; z esc() z powrotem
// na apostrof PRZED wykonaniem JS, więc samo esc() nie chroni – najpierw zabezpieczamy znaki JS (\, ', znaki nowej linii), potem HTML
const escA = s => esc(String(s ?? "").replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/\r/g, "\\r").replace(/\n/g, "\\n").replace(/[\u2028\u2029]/g, " "));
const zl = x => (x == null || x === "") ? "–" : Number(x).toLocaleString("pl-PL", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + " zł";
const liczba = (x, m = 1) => Number(x).toLocaleString("pl-PL", {maximumFractionDigits: m});
const pkt = x => Number(x || 0).toLocaleString("pl-PL", {minimumFractionDigits: 2, maximumFractionDigits: 2});  // punkty po polsku: 94,29
const STATUSY = ["nowy", "startujemy", "do analizy", "odpuszczamy", "oferta złożona", "wygrany", "przegrany"];

async function api(url, opcje = {}) {
  const o = {headers: {"X-Agent": "1"}, ...opcje};
  if (o.json !== undefined) { o.method = o.method || "POST"; o.headers["Content-Type"] = "application/json"; o.body = JSON.stringify(o.json); }
  let r;
  try { r = await fetch(url, o); } catch (e) { throw new Error("Brak połączenia z programem – sprawdź internet i spróbuj ponownie."); }
  if (r.status === 401) { location.href = "/login"; throw new Error("Zaloguj się ponownie"); }
  const d = await r.json().catch(() => ({}));
  if (r.status === 409 && d.zadanie_trwa && d.zadanie_trwa.id) {  // to zadanie już trwa – pokaż jego okienko (postęp i Przerwij)
    komunikat("To zadanie już trwa – poniżej jego postęp; możesz je przerwać.");
    return d.zadanie_trwa;
  }
  if (!r.ok) { const e_ = new Error(d.blad || opisBledu(r.status)); e_.dane = d; e_.status = r.status; throw e_; }
  const uw_ = r.headers.get("X-Uwagi"); if (uw_) { try { komunikat(decodeURIComponent(uw_), true); } catch (e) {} }  // np. archiwum pominięte przy wgrywaniu
  return d;
}
function opisBledu(kod) {
  return ({
    400: "Nieprawidłowe dane – sprawdź wpisane wartości (błąd 400).",
    403: "Brak uprawnień do tej operacji (błąd 403).",
    404: "Nie znaleziono – element mógł zostać usunięty lub przeniesiony do archiwum (błąd 404).",
    408: "Przekroczono czas oczekiwania – spróbuj ponownie (błąd 408).",
    413: "Plik jest zbyt duży – zmniejsz go lub podziel na części (błąd 413).",
    429: "Zbyt wiele zapytań naraz – odczekaj chwilę i spróbuj ponownie (błąd 429).",
    500: "Wewnętrzny błąd programu – spróbuj ponownie; jeśli się powtarza, zgłoś to obsłudze programu (błąd 500).",
    502: "Program właśnie się uruchamia po aktualizacji lub zmianie ustawień. Odczekaj 2–3 minuty i odśwież stronę (błąd 502).",
    503: "Program jest chwilowo niedostępny (uruchamianie lub przeciążenie). Odczekaj 2–3 minuty i odśwież stronę (błąd 503).",
    504: "Serwer nie odpowiedział na czas – operacja mogła trwać zbyt długo. Odśwież stronę za chwilę (błąd 504).",
  })[kod] || `Nieoczekiwany błąd (${kod}) – spróbuj ponownie.`;
}
function komunikat(t, blad = false) {
  const d = document.createElement("div");
  d.textContent = t; if (blad) d.className = "blad";
  $("#komunikat").appendChild(d); setTimeout(() => d.remove(), blad ? 7000 : 3500);
}
async function bezpiecznie(f) { try { return await f(); } catch (e) { komunikat(e.message, true); } }
function dataPl(s) { const m = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}))?/.exec(s || ""); return m ? `${m[3]}.${m[2]}.${m[1]}${m[4] ? " " + m[4] + ":" + m[5] : ""}` : (s || ""); }

// ================================================================ zadania w tle
const PO_ZADANIU = {};
const SLEDZONE = new Set();
// okienka zadań są przypięte do dołu ekranu – przewijana treść dostaje tyle miejsca na dole, ile zajmują, żeby niczego nie zasłaniały
(function miejsceNaZadania() {
  const ust = () => { const z = document.getElementById("zadania"); const h = z && z.children.length ? z.offsetHeight + 16 : 0;
    document.documentElement.style.setProperty("--zadania-h", h + "px"); document.body.classList.toggle("ma-zadania", h > 0); };
  const start = () => { const z = document.getElementById("zadania"); if (!z) return setTimeout(start, 500);
    new MutationObserver(ust).observe(z, {childList: true, subtree: true, characterData: true}); window.addEventListener("resize", ust); ust(); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
async function pokazTrwajaceZadania() {  // zadania działające w tle (np. raport wznowiony po restarcie serwera) – z okienkiem i przyciskiem Przerwij
  const L = await api("/api/zadania-aktywne").catch(() => []);
  // automatyczne sprawdzanie nowych przetargów pokazuje się na liście przetargów („sprawdzam nowe ogłoszenia…”) – bez okienka zasłaniającego treść
  for (const z of L) if (!SLEDZONE.has(z.id) && !(z.typ === "szukaj" && /^Sprawdzanie nowych przetargów/.test(z.opis || "")))
    sledz({...z, status: "trwa"}, () => { if (WIDOK === "wyniki") rysujWyniki(); });
}
async function sledz(zad, poZakonczeniu) {
  if (!zad || !zad.id) return;
  if (SLEDZONE.has(zad.id)) { const st = $("#z-" + zad.id); if (st) st.scrollIntoView({block: "nearest"}); return; }
  SLEDZONE.add(zad.id);
  PO_ZADANIU[zad.id] = poZakonczeniu;
  const el = document.createElement("div");
  el.className = "zadanie trwa"; el.id = "z-" + zad.id;
  $("#zadania").appendChild(el);
  const rysuj = z => {  // zamiast dziennika – kółko z procentem wykonanej pracy
    const p = z.status === "trwa" ? Math.max(1, Math.min(99, z.postep || 1)) : 100, R = 26, OB = 2 * Math.PI * R;
    const kolor = z.status === "blad" ? "#dc2626" : z.status === "przerwane" ? "#94a3b8" : z.status === "ok" ? "#16a34a" : "#1F5A99";
    const stan = z.status === "trwa" ? "W toku…" : z.status === "ok" ? "Gotowe" : z.status === "przerwane" ? "Przerwano" : "Nie udało się";
    const log = el.classList.contains("pokaz-log");
    el.className = "zadanie " + z.status + (log ? " pokaz-log" : "");
    el.innerHTML = `<div class="z-kolo"><svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="${R}" class="z-tlo"/>
        <circle cx="32" cy="32" r="${R}" class="z-pas" stroke="${kolor}" stroke-dasharray="${OB}" stroke-dashoffset="${OB * (1 - p / 100)}"/></svg>
        <span>${z.status === "ok" ? "✓" : z.status === "blad" ? "!" : z.status === "przerwane" ? "✕" : p + "%"}</span></div>
      <div class="z-tresc"><b>${esc(z.opis)}</b><small>${stan}${(z.log || []).length ? ` · <a href="#" class="z-szcz" onclick="this.closest('.zadanie').classList.toggle('pokaz-log'); return false">szczegóły</a>` : ""}</small>
        <pre class="z-log">${esc((z.log || []).slice(-8).join("\n"))}</pre>
        ${z.status === "blad" || z.status === "przerwane" ? `<p class="z-blad">${esc((z.blad || (z.log || []).slice(-1)[0] || "").replace(/^\[\d+:\d+:\d+\]\s*/, ""))}</p>` : ""}</div>
      <div class="z-akcje">${z.status === "trwa" ? `<button class="przerwij" onclick="przerwijZadanie('${zad.id}', this)">Przerwij</button>`
        : '<button onclick="this.closest(\'.zadanie\').remove()">Zamknij</button>'}</div>`;
  };
  rysuj(zad);
  let brak = 0;
  while (true) {
    await new Promise(r => setTimeout(r, 2000));
    let z;
    try { z = await api("/api/zadania/" + zad.id); brak = 0; }
    catch (e) {
      if (/404|Nie znaleziono|Nie ma takiego/.test(e.message) && ++brak >= 2) {  // zadanie zniknęło (np. serwer uruchomił się ponownie)
        // długie raporty serwer wznawia sam po starcie – szukamy wznowionego zadania o tej samej nazwie (do 2 minut)
        let nowe = null;
        for (let i = 0; i < 12 && !nowe; i++) {
          const L = await api("/api/zadania-aktywne").catch(() => []);
          nowe = L.find(x => x.opis === zad.opis);
          if (!nowe) await new Promise(r => setTimeout(r, 10000));
          if (!nowe && i === 0) rysuj({...zad, status: "trwa", postep: zad.postep || 1});
        }
        if (nowe) {
          PO_ZADANIU[nowe.id] = PO_ZADANIU[zad.id]; SLEDZONE.add(nowe.id); zad = {...zad, id: nowe.id}; brak = 0;
          komunikat("Serwer uruchomił się ponownie – raport wznowiono od miejsca, w którym przerwał.");
          continue;
        }
        z = {...zad, status: "przerwane", log: [...(zad.log || []), "Zadanie nie istnieje – serwer został uruchomiony ponownie (np. po aktualizacji). Uruchom je jeszcze raz – program wykorzysta dane już pobrane."]};
        rysuj(z); return z;
      }
      continue;
    }
    rysuj(z);
    if (z.status !== "trwa") {
      if (z.status === "ok") setTimeout(() => el.remove(), 15000);
      if (PO_ZADANIU[zad.id]) PO_ZADANIU[zad.id](z);
      return z;
    }
  }
}

async function przerwijZadanie(id, btn) {
  if (!confirm("Przerwać to zadanie? Zakończy się na najbliższym etapie (trwające zapytanie do AI zostanie dokończone, ale jego wynik nie będzie zapisany).")) return;
  if (btn) { btn.disabled = true; btn.textContent = "Przerywam…"; }
  await bezpiecznie(() => api(`/api/zadania/${id}/przerwij`, {json: {}}));
}

// ================================================================ nawigacja
let WIDOK = "przetargi";
document.querySelectorAll("#nav button").forEach(b => b.onclick = () => pokaz(b.dataset.w));
const TRYBY = {projekty: "przetarg", wlasne: "wlasny", kosztorys: "kosztorys",
  zam_kosztorys: "zamowienie", zam_weryfikacja: "zamowienie", zam_dokumentacja: "zamowienie", zam_projekty: "zamowienie", inw_projekty: "dom", kos_projekty: "kosztorys", dot_projekty: "dotacja", dot_wnioski: "wniosek_dot", pr_sprawy: "prawnik", pr_sporzadz: "prawnik"};
const FOKUS_WIDOKU = {zam_kosztorys: "sek-kosztorys", zam_weryfikacja: "sek-weryfikacja", zam_dokumentacja: "sek-dokumentacja"};
let FOKUS = null; let FOKUS_KZ = null; let KZ_NOTATKI_OTWARTE = false; let KZ_NT_NODE = null; let KZ_NT_PID = null;
let STRONA = null;  // "zamawiajacy" | "wykonawca" – wybór z ekranu startowego
const KAFLE = {
  prawnik: [
    ["pr_sprawy", "szukaj", "Sprawdź dokumentację", "1. czego dotyczy (dostawy, usługi, roboty; tryb; dla kogo) → 2. wgraj dokumentację albo podaj link → 3. sprawdzenie → 4. opinia prawna.", "fiol"],
    ["pr_sporzadz", "dokument", "Sporządź dokumentację", "1. czego dotyczy (dostawy, usługi, roboty; tryb) → 2. co chcesz zamówić: opis, ogłoszenie, SWZ, własne wzory → 3. sprawdzenie z przepisami → 4. komplet dokumentów do postępowania (ZIP).", "nieb"],
    ["pr_oferty", "trofeum", "Sprawdź oferty w przetargu", "Zgodność ofert z zamówieniem i rynkowość ceny (art. 224, ceny rynkowe pozycji) – dla zamawiającego albo wykonawcy; raport, opinia prawna, projekt odwołania do KIO.", "ziel"]],
  zamawiajacy: [
    ["olioc", "alarm", "Ochrona ludności (gmina)", "Schrony, ukrycia i miejsca doraźnego schronienia – pokrycie według art. 90 ustawy (miasta 50% / 25%, poza miastami 25% / 15%), zadania programu w 6 obszarach, kontrola dotacji (ryzyko zwrotu), zamówienia i raport.", "czer"],
    ["plan_spr", "kalendarz", "Roczny plan zamówień / Sprawozdania do UZP", "Plan postępowań (art. 23 Pzp) z kontrolą dzielenia zamówień i tabelami do BZP oraz roczne sprawozdanie o udzielonych zamówieniach (art. 82 Pzp) – do 1 marca.", "nieb"],
    ["kalk_pracy", "kalkulator", "Kalkulator kosztów pracy", "Usługi pracochłonne (sprzątanie, ochrona, catering, odpady, przewozy): minimalny koszt pracy 2026, cena z narzutami, porównanie z ceną oferty (art. 224), wyliczenie w Wordzie.", "zolt"],
    ["zam_nowe", "plus", "Nowe zamówienie – wybierz zakres", "Roboty budowlane, usługi albo dostawy towarów – program przygotuje przetarg z danej dziedziny.", "fiol"],
    ["zam_projekty", "folder", "Projekty zamówień", "Wszystko w jednym projekcie: dokumentacja, kosztorys, sprawdzenie, SWZ i umowa, notatki, raport.", "nieb"],
    ["zam_kosztorys", "kalkulator", "Kosztorys prac", "Kosztorys inwestorski sporządzony zgodnie z załączoną dokumentacją projektową.", "ziel"],
    ["zam_weryfikacja", "alarm", "Sprawdź dokumentację", "Wyszukanie błędów, sprzeczności i braków w dokumentacji przetargowej z propozycjami poprawek.", "czer"],
    ["zam_dokumentacja", "dokument", "Sporządź dokumentację", "SWZ lub zapytanie ofertowe, OPZ, formularz ofertowy i wzór umowy według Twoich wymagań.", "nieb"],
    ["zam_realizacja", "kask", "Realizacja umów", "Umowa z wykonawcą, harmonogram lub okresy rozliczeniowe, odbiory, faktury, reklamacje i ogłoszenie o wykonaniu umowy.", "zolt"],
    ["zam_oferty", "trofeum", "Sprawdzenie ofert", "Badanie złożonych ofert: kompletność, zgodność z SWZ, błędy rachunkowe, rażąco niska cena; punktacja, ranking i wybór.", "fiol"]],
  nieruchomosci: [
    ["nier", "teczka", "Dla rzeczoznawcy / Due Diligence / Wycena nieruchomości", "Teczka nieruchomości: identyfikacja działki, mapy, dokumenty, stan prawny, oględziny – due diligence, analiza zabudowy i wycena.", "ziel"]],
  dotacje: [
    ["dot_nadchodzace", "kalendarz", "Nadchodzące nabory", "Harmonogramy naborów województw i instytucji – co ruszy w najbliższych miesiącach; alerty dla Twojego regionu i zakresu.", "fiol"],
    ["dot_szukaj", "szukaj", "Wyszukaj dotację", "Aktualne nabory KPO, FEnIKS, FENG, programów regionalnych, NFOŚiGW, BGK, PARP – według branży, regionu i rodzaju wnioskodawcy.", "nieb"],
    ["dot_wnioski", "dokument", "Uzyskaj dotację", "Wniosek o dofinansowanie: dokumenty naboru pobrane z wyszukiwarki, wymagania i kryteria, wypełnienie wniosku i załączników, komplet do złożenia.", "ziel"],
    ["dot_projekty", "portfel", "Rozliczanie dotacji", "Umowa o dofinansowanie, dokumenty do rozliczenia etapu lub całości, przygotowanie, sprawdzenie i komplet do złożenia.", "zolt"]],
  kosztorysant: [
    ["kos_projekty", "kalkulator", "Kosztorysy", "Kosztorys z projektu lub przedmiaru – cenami rynkowymi albo z Twojego cennika; poprawki pozycji, wycena materiałów, przeniesienie do innego modułu.", "nieb"],
    ["hurtownie", "ciezarowka", "Hurtownie", "Zapytania ofertowe o ceny materiałów z listy materiałów kosztorysu.", "zolt"],
    ["firma", "wizytowka", "Profil firmy", "Dane firmy i logo w nagłówkach kosztorysów.", "ziel"]],
  inwestor: [
    ["inw_projekty", "folder", "Mój dom – projekt i kosztorys", "Wgraj projekt domu: kosztorys budowy przez AI albo własny, lista materiałów, harmonogram dostaw.", "nieb"],
    ["inw_budowa", "kask", "Budowa: etapy, odbiory, koszty", "Harmonogram budowy, protokoły odbioru, wydatki i budżet, wykonawcy, formalności, transze kredytu, raporty dzienne.", "ziel"],
    ["hurtownie", "ciezarowka", "Hurtownie i zamówienia", "Lista hurtowni – zapytania ofertowe i zamówienia materiałów prosto z projektu domu.", "zolt"],
    ["firma", "wizytowka", "Moje dane", "Dane inwestora do protokołów, zamówień i dokumentów budowy.", "czer"]],
  dostawca: [
    ["kalk_pracy", "kalkulator", "Kalkulator kosztów pracy", "Usługi pracochłonne (sprzątanie, ochrona, catering, odpady, przewozy): minimalny koszt pracy 2026, cena z narzutami, porównanie z ceną oferty (art. 224), wyliczenie w Wordzie.", "zolt"],
    ["przetargi", "szukaj", "Przetargi – dostawy i usługi", "BZP, Baza Konkurencyjności i BIP: zamówienia na dostawy i usługi, ocena AI według profilu dostawcy.", "nieb"],
    ["projekty", "folder", "Oferty", "Analiza przetargu, formularz cenowy z Twoimi cenami, załączniki według ogłoszenia, komplet do złożenia.", "ziel"],
    ["dos_realizacja", "kask", "Realizacja umów", "Po wygranej: dostawy i zamówienia, okresy usług, odbiory, faktury i płatności, reklamacje, kary, rozliczenie.", "czer"],
    ["wyniki", "trofeum", "Wygrane i przegrane", "Wyniki złożonych ofert: skuteczność i różnica do ceny zwycięzcy.", "zolt"],
    ["klienci", "wizytowka", "Klienci", "Zamawiający i kontrahenci z danymi pobieranymi po NIP.", "ziel"]],
  wykonawca: [
    ["kalk_pracy", "kalkulator", "Kalkulator kosztów pracy", "Usługi pracochłonne (sprzątanie, ochrona, catering, odpady, przewozy): minimalny koszt pracy 2026, cena z narzutami, porównanie z ceną oferty (art. 224), wyliczenie w Wordzie.", "zolt"],
    ["przetargi", "szukaj", "Przetargi", "Wyszukiwanie w BZP, Bazie Konkurencyjności i BIP, analiza i ocena AI.", "nieb"],
    ["projekty", "folder", "Projekty z przetargów", "Oferta i kosztorys, dokumenty, komplet do przetargu, materiały, zamówienia.", "ziel"],
    ["wyniki", "trofeum", "Wygrane i przegrane", "Wyniki złożonych ofert z BZP: skuteczność, różnica do ceny zwycięzcy, w czym jesteś za drogi.", "zolt"],
    ["wlasne", "teczka", "Własne projekty", "Zlecenia spoza przetargów: oferta, umowa o roboty budowlane, realizacja.", "zolt"],
    ["kosztorys", "kalkulator", "Kosztorysowanie", "Szybka wycena z dokumentów albo z opisu i wymiarów, kosztorys dla klienta.", "nieb"],
    ["realizacja", "kask", "W realizacji", "Budowy: harmonogram, protokoły odbioru, faktury, koszty, raporty dzienne, usterki.", "czer"],
    ["klienci", "wizytowka", "Klienci", "Baza klientów z danymi pobieranymi po NIP.", "ziel"],
    ["hurtownie", "ciezarowka", "Hurtownie", "Dostawcy i historia zapytań oraz zamówień materiałów.", "zolt"],
    ["pracownicy", "ludzie", "Pracownicy", "Ewidencja roboczogodzin i rozliczenie bez narzutów.", "nieb"],
    ["kadry", "teczka", "Kadry (HR)", "Kartoteki, umowy, badania, BHP, uprawnienia – z przypomnieniami o terminach.", "ziel"],
    ["place", "portfel", "Płace", "Umowy, lista płac z ZUS i podatkiem, koszt pracodawcy.", "czer"]],
};
async function rysujPulpit() {
  const s = STRONA || "wykonawca", cd = celDef(s);
  if (s === "zamawiajacy" && MZ().plan_na_pulpicie) setTimeout(async () => {  // roczny plan zamówień: termin publikacji, postępowania do wszczęcia
    const L = await api("/api/plan/przypomnienia").catch(() => []); const el = $("#pulpit-alerty"); if (!el || !L.length) return;
    el.insertAdjacentHTML("afterbegin", `<div class="ramka-uwaga"><b>${ik("kalendarz")} Roczny plan zamówień:</b><ul class="lista">${L.slice(0, 8).map(x =>
      `<li class="${x.pilne ? "czerwone" : ""}"><a href="#" onclick="PLN.rok=${x.rok}; pokaz('plan_zam'); return false">${esc(x.opis)}</a></li>`).join("")}</ul></div>`);
  }, 80);
  if (s === "zamawiajacy") setTimeout(async () => {  // ogłoszenia o wykonaniu umowy do opublikowania (art. 448 Pzp)
    const L = await api("/api/zam/ogloszenia-wykonania").catch(() => []); const el = $("#zam-owu"); if (!el || !L.length) return;
    el.innerHTML = `<div class="ramka-uwaga"><b>Ogłoszenia o wykonaniu umowy do opublikowania w BZP (${L.length}):</b><ul class="lista">${L.map(x => `<li><a href="#" onclick="doRealizacji('${x.id}', false); return false">${esc(x.nazwa)}</a> – termin ${dataPl(x.termin)}${x.dni < 0 ? ` <b class="czerwone">(po terminie ${-x.dni} dni)</b>` : ` (zostało ${x.dni} dni)`}</li>`).join("")}</ul></div>`;
  }, 50);
  // Przegląd pokazuje tylko kafelki wybranej ścieżki („Co chcesz zrobić?”) i jej sekcji Firma
  let kafle = cd ? KAFLE[s].filter(k => cd.kroki.some(x => x[0] === k[0]) || (cd.firma || []).includes(k[0])) : KAFLE[s];
  if (s === "zamawiajacy" && !MZ().kafel_kosztorys) kafle = kafle.filter(k => k[0] !== "zam_kosztorys");  // zamawiający publiczny: bez kosztorysu inwestorskiego przez AI
  if (s === "zamawiajacy" && MZ().kafle) kafle = MZ().kafle;  // wspólnota: własne kafelki modułu (MODULY_ZAM)

  const typy = {zam_projekty: "zamowienie", projekty: "przetarg", wlasne: "wlasny", kosztorys: "kosztorys", inw_projekty: "dom", kos_projekty: "kosztorys", dot_projekty: "dotacja", dot_wnioski: "wniosek_dot", pr_sprawy: "prawnik"};
  $("#pulpit").innerHTML = `<div class="pulpit-glowka">${s === "wykonawca" ? `<div class="powitanie"><h1>Witaj w Bidivia!</h1><p>Szybsze oferty. Więcej wygranych.</p></div>` : `<h2>${{dostawca: "Dla Dostawcy / Usługodawcy", zamawiajacy: MZ().naglowek_pulpitu, inwestor: "Dla Inwestora indywidualnego – budowa domu", kosztorysant: "Kosztorysowanie", dotacje: "Dotacje UE/KPO",
      nieruchomosci: "Dla rzeczoznawcy / Due Diligence / Wycena nieruchomości", prawnik: "Dla Prawnika"}[s] || "Dla Wykonawcy"}</h2>`}
      <button class="maly" data-ik="przelacz" onclick="pokaz('start')">Zmień tryb</button></div>
    ${s === "wykonawca" ? `<div class="kpi" id="pulpit-kpi">${[["szukaj", "Nowe przetargi", "kpi-nowe", "nieb"], ["dokument", "Oferty w przygotowaniu", "kpi-oferty", "nieb"],
      ["kask", "Realizowane budowy", "kpi-budowy", "pom"], ["portfel", "Aktywne dotacje", "kpi-dotacje", "ziel"]].map(([i_, t, id, k]) =>
      `<div class="kpi-karta${id === "kpi-nowe" ? " klik" : ""}" ${id === "kpi-nowe" ? 'onclick="pokazNowe()" title="Pokaż nowe przetargi"' : ""}><span class="kpi-ik k-${k}">${ik(i_)}</span><div><small>${t}</small><b id="${id}">–</b><em id="${id}-op"></em></div></div>`).join("")}</div>
    <div class="polecane" id="pulpit-polecane"></div>` : ""}
    <div id="pulpit-alerty"></div>
    <div id="zam-owu"></div>
    <div class="kafle">${kafle.filter(k => (k[5] !== "admin" || ADMIN()) && wolnoWidok(k[0])).map(([w, ikona, tyt, opis, kol]) => `
      <button class="kafel k-${kol}" onclick="pokaz('${w}')"><span class="kafel-ik">${ik(ikona)}</span><b>${tyt}</b><span class="kafel-opis">${opis}</span>
        <span class="kafel-licznik" id="kl-${w}"></span></button>`).join("")}</div>
    <div class="kafle male">
      ${poziomU("ustawienia") >= 1 ? `<button class="kafel maly-k" onclick="pokaz('ustawienia')"><span class="kafel-ik">${ik("suwaki")}</span><b>Ustawienia</b></button>` : ""}
      ${ADMIN() ? `<button class="kafel maly-k" onclick="pokaz('konta')"><span class="kafel-ik">${ik("ludzie")}</span><b>Konta i aktywność</b></button>` : ""}
      ${JA && JA.windykacja ? `<button class="kafel maly-k" onclick="pokaz('windykacja')"><span class="kafel-ik">${ik("procent")}</span><b>Windykacja</b><span class="kafel-opis">Należności, przypomnienia, odsetki i rekompensaty, noty i wezwania.</span></button>` : ""}
      ${WLASC() ? `<button class="kafel maly-k" onclick="pokaz('leady')"><span class="kafel-ik">${ik("ludzie")}</span><b>Leady z przetargów</b></button>` : ""}
      ${WLASC() ? `<button class="kafel maly-k" onclick="pokaz('odwolania')"><span class="kafel-ik">${ik("protokol")}</span><b>Odwołania od przetargów</b></button>` : ""}
      ${JA.ksiegowosc ? `<button class="kafel maly-k" onclick="pokaz('ksiegowosc')"><span class="kafel-ik">${ik("portfel")}</span><b>Księgowość</b></button>` : ""}
      ${poziomU("firma") >= 1 && s !== "inwestor" && s !== "kosztorysant" && s !== "dotacje" ? `<button class="kafel maly-k" onclick="pokaz('firma')"><span class="kafel-ik">${ik("wizytowka")}</span><b>${s === "zamawiajacy" ? "Dane zamawiającego" : "Profil firmy"}</b></button>` : ""}
      ${poziomU("archiwum") >= 1 ? `<button class="kafel maly-k" onclick="pokaz('archiwum')"><span class="kafel-ik">${ik("teczka")}</span><b>Archiwum</b></button>` : ""}
      <button class="kafel maly-k" onclick="pokaz('instrukcja')"><span class="kafel-ik">${ik("ksiazka")}</span><b>Instrukcja</b></button>
      <button class="kafel maly-k" onclick="pokaz('start')"><span class="kafel-ik">${ik("przelacz")}</span><b>Zmień tryb</b></button></div>`;
  if (s === "wykonawca") { if (NOWE_INFO) rysujNowePulpit(); else odswiezLicznikNowych(); }
  if (!JA.edycja || JA.edycja === "pelna") api("/api/alerty").then(A => { A = (A || []).filter(a => a.wspolnota === undefined || STRONA !== "zamawiajacy" || !!a.wspolnota === MZ().prywatny); if (!A.length) return;
    $("#pulpit-alerty").innerHTML = `<div class="alerty-pulpit"><b>${ik("alarm")} Terminy do pilnowania (30 dni)</b><ul>${A.slice(0, 8).map(a => `<li class="${a.dni < 0 ? "czerwone" : ""}">
      <a href="#" onclick="${a.projekt ? `ZW_ID='${a.projekt}'; pokaz('zam_zapytania')` : `pokaz('${a.widok}')`}; return false">${esc(a.opis)}</a> – ${a.dni < 0 ? "po terminie " + esc(dataPl(a.termin)) : a.dni === 0 ? "dziś" : "za " + odm(a.dni, "dzień", "dni", "dni") + " (" + esc(dataPl(a.termin)) + ")"}</li>`).join("")}
      ${A.length > 8 ? `<li class="opis">…i ${A.length - 8} więcej</li>` : ""}</ul></div>`; }).catch(() => {});
  try {  // liczniki na kafelkach
    const [pr, re] = await Promise.all([api("/api/projekty"), api("/api/realizacja?strona=" + s)]);
    const dosP = p => ["dostawy", "uslugi"].includes(p.rodzaj_zamowienia);  // oferty dostawcy liczone tylko u dostawcy, oferty wykonawcy – u wykonawcy
    Object.entries(typy).forEach(([w, t]) => { const n = pr.filter(p => (p.typ || "przetarg") === t && (t !== "przetarg" || (s === "dostawca" ? dosP(p) : !dosP(p)))).length, el = $("#kl-" + w);
      if (el && n) el.textContent = odm(n, "projekt", "projekty", "projektów"); });
    if (s === "nieruchomosci" && $("#kl-nier")) { const nr = await api("/api/nier").catch(() => []); if (nr.length) $("#kl-nier").textContent = odm(nr.length, "nieruchomość", "nieruchomości", "nieruchomości"); }
    const el = $("#kl-" + ({zamawiajacy: "zam_realizacja", inwestor: "inw_budowa", dostawca: "dos_realizacja"}[s] || "realizacja"));
    const [l1, l2, l5] = {zamawiajacy: ["umowa w realizacji", "umowy w realizacji", "umów w realizacji"], dostawca: ["umowa w realizacji", "umowy w realizacji", "umów w realizacji"]}[s] || ["budowa", "budowy", "budów"];
    if (el && re.length) el.textContent = odm(re.length, l1, l2, l5);
    if (s === "wykonawca" && poziomU("przetargi") >= 1) { const p = await api("/api/przetargi");  // rola bez modułu Przetargi (np. kierownik budowy) – bez zapytania (403) const n = p.filter(t => t.rekomendacja === "startujemy" && !["dostawy", "uslugi"].includes(t.rodzaj_zam) && (!t.termin_ofert || String(t.termin_ofert).slice(0, 10) >= DZIS_ISO())).length;
      if (n && $("#kl-przetargi")) $("#kl-przetargi").textContent = odm(n, "przetarg do startu", "przetargi do startu", "przetargów do startu");
      const dzis = DZIS_ISO(), aktualne = p.filter(t => !t.obcy && (!t.termin_ofert || String(t.termin_ofert).slice(0, 10) >= dzis) && !["dostawy", "uslugi"].includes(t.rodzaj_zam));
      const nowe = aktualne.filter(t => t.nowy).length;
      const kpi = (id, v, op) => { const e = $("#" + id); if (e) e.textContent = v; const o = $("#" + id + "-op"); if (o && op) o.textContent = op; };
      kpi("kpi-nowe", nowe || aktualne.length, nowe ? "od ostatniej wizyty" : "aktualnych w obszarze");
      kpi("kpi-oferty", pr.filter(x => (x.typ || "przetarg") === "przetarg" && x.status_projektu !== "realizacja" && !x.archiwum).length + pr.filter(x => x.typ === "wlasny" && x.status_projektu !== "realizacja").length);
      kpi("kpi-budowy", re.length);
      const dot = await api("/api/projekty").then(L => L.filter(x => ["dotacja", "wniosek_dot"].includes(x.typ)).length).catch(() => 0);
      kpi("kpi-dotacje", dot);
      const pol = aktualne.filter(t => t.ocena).sort((a, b) => (b.ocena || 0) - (a.ocena || 0) || String(a.termin_ofert || "9").localeCompare(String(b.termin_ofert || "9"))).slice(0, 5);
      if ($("#pulpit-polecane")) $("#pulpit-polecane").innerHTML = pol.length ? `<div class="polecane-gora"><b>Polecane przetargi</b>
          <a href="#" onclick="pokaz('przetargi'); return false">Zobacz wszystkie →</a></div>
        ${pol.map(t => `<a class="polecany" href="#" onclick="otworzPrzetarg(${jsa(t.numer || "")}, ${jsa(t.konto || "")}); return false">
          <span class="pol-ik">${ik("kask")}</span><span class="pol-txt"><b>${esc((t.przedmiot || "").slice(0, 110))}</b><small>${esc(t.zamawiajacy || "")}${t.miejscowosc ? " · " + esc(t.miejscowosc) : ""}</small></span>
          ${t.nowy ? '<span class="znacznik z-do-analizy">Nowy</span>' : ""}${(t.ocena || 0) >= 8 ? '<span class="znacznik z-startujemy">Wysokie dopasowanie</span>' : ""}
          <span class="pol-termin"><small>Termin</small><b>${esc(dataPl(String(t.termin_ofert || "").slice(0, 10)) || "–")}</b></span></a>`).join("")}` : ""; }
  } catch (e) {}
}
// ================================================================ CELE: „Co chcesz zrobić?” – ścieżki pracy w każdym trybie
const FIRMA_WYK = ["klienci", "hurtownie", "pracownicy", "kadry", "place", "kalk_pracy"];
const ZESTAWY_PRACOCHLONNE = ["Sprzątanie", "Ochrona osób i mienia", "Catering i żywienie zbiorowe", "Odpady", "Dowóz uczniów i przewozy", "Komunikacja zastępcza (PKP)",
  "Utrzymanie zieleni", "Zimowe utrzymanie dróg", "Transport"];
const CELE = {
  wykonawca: [
    {id: "przetargi", tytul: "Znajdź przetarg i złóż ofertę", ik: "szukaj", start: "przetargi", firma: FIRMA_WYK,
     kroki: [["przetargi", "Szukaj przetargów"], ["projekty", "Moje oferty"], ["wyniki", "Wygrane i przegrane"], ["realizacja", "W realizacji"]]},
    {id: "wlasne", tytul: "Własny projekt (zlecenie poza przetargiem)", ik: "teczka", start: "wlasne", firma: FIRMA_WYK,
     kroki: [["wlasne", "Moje projekty"], ["realizacja", "W realizacji"]]},
    {id: "kosztorys", tytul: "Kosztorys", ik: "kalkulator", start: "kosztorys", firma: ["hurtownie", "kalk_pracy"], kroki: [["kosztorys", "Kosztorysowanie"]]}],
  dostawca: [
    {id: "przetargi", tytul: "Znajdź przetarg i złóż ofertę", ik: "szukaj", start: "przetargi", firma: ["klienci", "kalk_pracy"],
     kroki: [["przetargi", "Szukaj przetargów"], ["projekty", "Moje oferty"], ["wyniki", "Wygrane i przegrane"]]},
    {id: "uslugi", tytul: "Usługi pracochłonne: sprzątanie, ochrona, catering, odpady, przewozy", ik: "ludzie", start: "przetargi", firma: ["klienci", "pracownicy", "place"],
     kroki: [["przetargi", "Szukaj przetargów usług"], ["kalk_pracy", "Kalkulator kosztów pracy"], ["projekty", "Moje oferty"], ["wyniki", "Wygrane i przegrane"], ["dos_realizacja", "Umowy w realizacji"]]},
    {id: "umowy", tytul: "Realizuj umowę", ik: "kask", start: "dos_realizacja", firma: ["klienci", "kalk_pracy"], kroki: [["dos_realizacja", "Umowy w realizacji"]]}],
  prawnik: [
    {id: "sprawy", tytul: "Sprawdź dokumentację: dokumentacja → sprawdzenie → opinia prawna", ik: "szukaj", start: "pr_sprawy", kroki: [["pr_sprawy", "Sprawy"]]},
    {id: "sporzadz", tytul: "Sporządź dokumentację: opis albo dokumenty → sprawdzenie z przepisami → komplet dokumentów", ik: "dokument", start: "pr_sporzadz", kroki: [["pr_sprawy", "Sprawy"]]},
    {id: "oferty", tytul: "Sprawdź oferty w przetargu: zgodność z zamówieniem, rynkowość ceny → raport, opinia, projekt odwołania", ik: "trofeum", start: "pr_oferty", kroki: [["pr_oferty", "Sprawdzenia ofert"]]}],
  zamawiajacy: [
    {id: "plan", tytul: "Roczny plan zamówień / Sprawozdania do UZP", ik: "kalendarz", start: "plan_spr", firma: ["plan_zam", "sprawozdanie"],
     kroki: [["plan_spr", "Plan i sprawozdania"], ["zam_nowe", "Nowe zamówienie (kreator)"], ["zam_projekty", "Moje zamówienia"]]},
    {id: "olioc", tytul: "Ochrona ludności i obrona cywilna (gmina)", ik: "alarm", start: "olioc", firma: ["plan_spr", "plan_zam", "sprawozdanie"],
     kroki: [["olioc", "Ochrona ludności"], ["zam_nowe", "Nowe zamówienie (kreator)"], ["zam_projekty", "Moje zamówienia"], ["zam_realizacja", "Realizacja umów"]]},
    {id: "przygotuj", tytul: "Przygotuj zamówienie", ik: "plus", start: "zam_nowe", firma: ["plan_spr", "plan_zam", "sprawozdanie"],
     kroki: [["zam_nowe", "Nowe zamówienie (kreator)"], ["zam_projekty", "Moje zamówienia"], ["kalk_pracy", "Kalkulator kosztów pracy (szacowanie wartości)"]]},
    {id: "oferty", tytul: "Sprawdź złożone oferty", ik: "trofeum", start: "zam_oferty", firma: ["plan_spr", "plan_zam", "sprawozdanie"], kroki: [["zam_oferty", "Sprawdzenie ofert"], ["kalk_pracy", "Kalkulator kosztów pracy (rażąco niska cena)"]]},
    {id: "inwestycja", tytul: "Realizuj umowę (inwestycja, usługi, dostawy)", ik: "kask", start: "zam_realizacja", firma: ["plan_spr", "plan_zam", "sprawozdanie"], kroki: [["zam_realizacja", "Realizacja umów"]]}],
  inwestor: [
    {id: "plan", tytul: "Zaplanuj budowę domu", ik: "folder", start: "inw_projekty", firma: ["hurtownie"], kroki: [["inw_projekty", "Projekt i kosztorys domu"]]},
    {id: "budowa", tytul: "Prowadź budowę", ik: "kask", start: "inw_budowa", firma: ["hurtownie"], kroki: [["inw_budowa", "Budowa"]]}],
  nieruchomosci: [
    {id: "dd", tytul: "Zbadaj nieruchomość (due diligence)", ik: "szukaj", start: "nier", kroki: [["nier", "Rzeczoznawca / DD / wycena"]]},
    {id: "zabudowa", tytul: "Sprawdź, co można zbudować na działce", ik: "kask", start: "nier", kroki: [["nier", "Rzeczoznawca / DD / wycena"]]},
    {id: "wycena", tytul: "Wyceń nieruchomość (projekt operatu dla rzeczoznawcy)", ik: "kalkulator", start: "nier", kroki: [["nier", "Rzeczoznawca / DD / wycena"]]},
    {id: "pakiet", tytul: "Pełny pakiet: DD, zabudowa i wycena", ik: "teczka", start: "nier", kroki: [["nier", "Rzeczoznawca / DD / wycena"]]},
    {id: "wlasna", tytul: "Wyceń samodzielnie – szacunek z ofert rynkowych (bez rzeczoznawcy)", ik: "szukaj", start: "nier", kroki: [["nier", "Rzeczoznawca / DD / wycena"]]}],
  dotacje: [
    {id: "znajdz", tytul: "Znajdź dotację", ik: "szukaj", start: "dot_szukaj",
     kroki: [["dot_szukaj", "Wyszukaj dotację"], ["dot_nadchodzace", "Nadchodzące nabory"], ["dot_wnioski", "Uzyskaj dotację"]]},
    {id: "rozlicz", tytul: "Rozlicz dotację", ik: "portfel", start: "dot_projekty", kroki: [["dot_projekty", "Rozliczanie dotacji"]]},
    {id: "wykonawca", tytul: "Wybierz wykonawcę w projekcie (zasada konkurencyjności)", ik: "dokument", start: "dot_zapytania",
     kroki: [["dot_zapytania", "Zapytania ofertowe"], ["zam_oferty", "Sprawdzenie ofert"], ["dot_projekty", "Rozliczanie dotacji"]]}],
};
let CEL = null;
// Cele niedostępne dla zamawiającego prywatnego (wspólnoty, spółdzielnie, deweloperzy): roczny plan i ochrona ludności dotyczą zamawiających publicznych i gmin
const celUkryty = (s, id) => s === "zamawiajacy" && MZ().cele_ukryte.includes(id);
const celDef = (s = STRONA, id = CEL) => celUkryty(s, id) ? null : (CELE[s] || []).find(c => c.id === id) || null;
function zapamietanyCel(s) { try { return localStorage.getItem("cel_" + s); } catch (e) { return null; } }
function rysujCel() {
  const L = (CELE[STRONA] || []).filter(c => !celUkryty(STRONA, c.id));
  $("#cel-tytul").textContent = "Co chcesz zrobić?";
  $("#cel-kafle").innerHTML = L.map(c => `<button class="cel-kafel" onclick="wybierzCel('${c.id}')"><span class="cel-ik">${ik(c.ik)}</span><b>${esc(c.tytul)}</b><span class="cel-strz">›</span></button>`).join("");
}
function wybierzCel(id, bezPrzejscia) {
  if (celUkryty(STRONA, id)) return pokaz("cel");  // np. zapamiętana ścieżka gminy po przejściu do ścieżki wspólnot
  CEL = id;
  try { localStorage.setItem("cel_" + STRONA, id); } catch (e) {}
  zastosujCel();
  if (!bezPrzejscia) { const c = celDef(); if (c) pokaz(c.start); }
}
function zastosujCel() {  // menu: tylko kroki wybranej ścieżki (ponumerowane) + Firma + pozycje programu
  const c = celDef(), maCele = !!CELE[STRONA];
  document.body.classList.toggle("z-celem", !!c);
  document.querySelectorAll("#nav .g1 button, #nav .g2 button").forEach(b => {
    const lab = b.querySelector(".etykieta"); if (lab && !b.dataset.orig) b.dataset.orig = lab.textContent;
    if (b.dataset.w === "cel") { b.classList.toggle("poza-celem", !maCele || (STRONA === "zamawiajacy" && !MZ().ma_cele)); return; }
    const M = MZ();
    const ukryta = STRONA === "zamawiajacy" && ((M.menu && b.dataset.strona === "zamawiajacy" && !M.menu.includes(b.dataset.w)) || M.ukryte_w_menu.includes(b.dataset.w));  // pozycje innego modułu
    if (!c) { b.classList.toggle("poza-celem", ukryta); if (lab) lab.textContent = b.dataset.w === "pulpit" ? "Przegląd" : (STRONA === "zamawiajacy" && M.nazwy_menu[b.dataset.w]) || b.dataset.orig; return; }
    if (b.dataset.strona && b.dataset.strona !== STRONA) return;
    const i = c.kroki.findIndex(k => k[0] === b.dataset.w && (!b.dataset.strona || b.dataset.strona === STRONA));
    const wFirmie = (c.firma || []).includes(b.dataset.w);
    b.classList.toggle("poza-celem", ukryta || (i < 0 && !wFirmie && b.dataset.w !== "pulpit"));
    if (lab) lab.textContent = i >= 0 ? (c.kroki.length > 1 ? `${i + 1}. ${c.kroki[i][1]}` : c.kroki[i][1]) : b.dataset.w === "pulpit" ? "Przegląd" : b.dataset.orig;
  });
  if (c) {  // kolejność pozycji w menu = kolejność kroków ścieżki
    let kotwica = document.querySelector('#nav .g1 button[data-w="pulpit"]');
    c.kroki.forEach(([w]) => {
      const b = [...document.querySelectorAll(`#nav .g1 button[data-w="${w}"]`)].find(x => !x.dataset.strona || x.dataset.strona === STRONA);
      if (b && kotwica) { kotwica.after(b); kotwica = b; }
    });
    const nc = document.querySelector("#nav .g1 button.nav-cel"); if (nc && kotwica) kotwica.after(nc);
  }
  setTimeout(odswiezGrupyMenu, 0);
}
function celDlaWidoku(w) {  // przejście do widoku z innej ścieżki (np. wygrany przetarg → W realizacji) – ścieżka zmienia się sama
  const c = celDef();
  if (!CELE[STRONA] || (STRONA === "zamawiajacy" && !MZ().ma_cele) || ["start", "cel", "pulpit", "firma", "archiwum", "konta", "ustawienia", "instrukcja"].includes(w)) return;
  if (c && (c.kroki.some(k => k[0] === w) || (c.firma || []).includes(w))) return;
  const inny = CELE[STRONA].find(x => x.kroki.some(k => k[0] === w));
  if (inny) wybierzCel(inny.id, true);
}
const PIERWSZA = {prawnik: "pr_sprawy", dostawca: "przetargi", zamawiajacy: "zam_projekty", wykonawca: "przetargi", inwestor: "inw_projekty", kosztorysant: "kos_projekty", dotacje: "dot_szukaj", nieruchomosci: "nier"};
function odswiezGrupyMenu() {  // grupa menu bez widocznych przycisków (np. „Firma” u zamawiającego) jest ukrywana
  document.querySelectorAll("#nav .nav-grupa").forEach(g => g.classList.toggle("pusta", ![...g.querySelectorAll("button")].some(b => getComputedStyle(b).display !== "none")));
}
function wybierzStrone(s, pytaj, bezPrzejscia) {
  STRONA = s; CEL = null; document.body.classList.remove("tryb-zamawiajacy", "tryb-wykonawca", "tryb-inwestor", "tryb-kosztorysant", "tryb-dotacje", "tryb-dostawca", "tryb-nieruchomosci");
  document.body.classList.add("tryb-" + s);
  SLOWA = null;  // słowa kluczowe są osobne dla wykonawcy i dla dostawcy
  try {  // wyszukiwarka i wyniki należą do trybu – po zmianie trybu nic nie zostaje z poprzedniego
    WY = null; OSTATNIE = null;
    ["#wysz", "#p-wyniki-gora", "#p-karty"].forEach(s => { const e = $(s); if (e) e.innerHTML = ""; });
    const sz = $("#p-szczegoly"); if (sz) sz.classList.add("ukryj");
  } catch (e) {}
  const etF = s === "inwestor" ? "Moje dane" : s === "zamawiajacy" ? "Dane zamawiającego" : "Profil firmy";
  const fe = document.querySelector('#nav button[data-w="firma"] .etykieta'); if (fe) fe.textContent = etF;
  const fh = document.querySelector("#w-firma > h2"); if (fh) fh.textContent = etF;
  const gs = $("#gp-szukaj"); if (gs) gs.placeholder = s === "zamawiajacy" ? "Szukaj zamówień, projektów, dokumentów…" : "Szukaj przetargów, projektów, dokumentów…";
  try { sessionStorage.setItem("strona", s); localStorage.setItem("tryb", s); } catch (e) {}
  setTimeout(odswiezGrupyMenu, 0);
  if (JA.ostatni_tryb !== s) { JA.ostatni_tryb = s; api("/api/konto/tryb", {json: {tryb: s}}).catch(() => {}); }
  zastosujCel();
  if (bezPrzejscia) return;
  if (s === "zamawiajacy" && !MZ().ma_cele) { CEL = null; zastosujCel(); return pokaz("pulpit"); }  // wspólnota: cztery kafelki zamiast wyboru celu
  if (CELE[s]) {  // „Co chcesz zrobić?” – po kliknięciu kafelka trybu; po zalogowaniu od razu zapamiętana ścieżka
    const zap = zapamietanyCel(s);
    if (!pytaj && zap && !celUkryty(s, zap) && CELE[s].some(c => c.id === zap)) return wybierzCel(zap);
    return pokaz("cel");
  }
  pokaz("pulpit");
}
let TRYB = "przetarg";
function przelaczMenu(zamknij) {
  const h = document.querySelector("header"), otw = zamknij ? false : !h.classList.contains("otwarte");
  h.classList.toggle("otwarte", otw);
  if (otw) odswiezPodmenu();
  const b = $("#menu-btn"); if (b) b.innerHTML = ik(otw ? "plus" : "menu");
  if (otw) b.querySelector("svg").style.transform = "rotate(45deg)";
}
let ZDARZENIE_INSTALACJI = null;
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); ZDARZENIE_INSTALACJI = e; $("#instaluj")?.classList.remove("ukryj"); });
async function instalujAplikacje() {
  if (!ZDARZENIE_INSTALACJI) return komunikat("Na iPhonie: w Safari kliknij „Udostępnij” → „Do ekranu początkowego”.");
  ZDARZENIE_INSTALACJI.prompt(); await ZDARZENIE_INSTALACJI.userChoice.catch(() => null);
  ZDARZENIE_INSTALACJI = null; $("#instaluj").classList.add("ukryj");
}
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
function ustawWysokoscNaglowka() {  // na komputerze menu jest z boku – nad treścią jest tylko górny pasek z wyszukiwarką
  const boczne = window.matchMedia("(min-width: 1100px)").matches, gp = $("#gora-pasek"), h = document.querySelector("header");
  const wys = boczne ? (gp && gp.offsetParent ? gp.offsetHeight : 0) : (h ? h.offsetHeight : 72);
  document.documentElement.style.setProperty("--wys-nagl", wys + "px");
}
window.addEventListener("resize", ustawWysokoscNaglowka);
// ---------- ODWOŁANIA DO DOKUMENTÓW: § 4, pkt 3.1, poz. 12 – podświetlone; dymek z treścią po najechaniu, pełny dokument po kliknięciu
const ODW = [];
function odwChip(o, etykieta, ctx) {  // ctx: {typ: "projekt"|"przetarg", id}
  if (!o) return "";
  const i = ODW.push({...o, ctx}) - 1;
  const et = etykieta || o.miejsce || (o.znaleziono ? "fragment dokumentu" : "odwołanie");
  return `<span class="odw ${o.znaleziono ? "" : "odw-brak"}" data-odw="${i}" tabindex="0" role="button">${esc(et)}</span>`;
}
function odwWTekscie(tekstEsc, miejsce, chip) {  // miejsce w treści uwagi zamienione na podświetlenie; inaczej chip na końcu
  if (!chip) return tekstEsc;
  const m = esc(miejsce || "").trim();
  if (m && m.length >= 2 && tekstEsc.includes(m)) return tekstEsc.replace(m, chip);
  return tekstEsc + " " + chip;
}
function odwWTresci(tekstEsc, u, ctx) {  // „§ 4 ust. 2” w treści uwagi też podświetlone (gdy występuje w zdaniu)
  const m = esc((u && u.miejsce) || "").trim();
  if (!u || !u.odw || m.length < 2 || !tekstEsc.includes(m)) return tekstEsc;
  return tekstEsc.replace(m, odwChip(u.odw, u.miejsce, ctx));
}
function odwPola(t, k) {  // pełna analiza wykonawcy: odwołania przy polu (kary umowne, warunki udziału, wadium…)
  const L = (t.odwolania || []).filter(o => o.pole === k && o.odw);
  return L.length ? " " + L.map(o => odwChip(o.odw, o.miejsce || "źródło", {typ: "przetarg", id: t.numer})).join(" ") : "";
}
function odwPozostale(t) {
  const pola = new Set(GRUPY_ANALIZY.flatMap(([, p]) => p.filter(([k]) => t[k]).map(([k]) => k)));
  const L = (t.odwolania || []).filter(o => o.odw && !pola.has(o.pole));
  return L.length ? `<h4 class="grupa-analizy">Odwołania do dokumentów</h4><p>${L.map(o => `${esc(o.pole || "")} ${odwChip(o.odw, o.miejsce || "źródło", {typ: "przetarg", id: t.numer})}`).join(" · ")}</p>` : "";
}
function odwFragment(o) {
  const f = o.fragment || "", a = Math.max(0, o.od || 0), b = Math.max(a, o.do || 0);
  return esc(f.slice(0, a)) + "<mark>" + esc(f.slice(a, b)) + "</mark>" + esc(f.slice(b));
}
function odwDymekPokaz(el) {
  const o = ODW[+el.dataset.odw]; if (!o) return;
  let d = $("#odw-dymek"); if (!d) { d = document.createElement("div"); d.id = "odw-dymek"; document.body.appendChild(d); }
  d.innerHTML = o.znaleziono
    ? `<div class="odw-glowa"><b>${esc(o.nazwa || "")}</b>${o.strona ? " · str. " + o.strona : ""}${o.miejsce ? " · " + esc(o.miejsce) : ""}${o.jak === "miejsce" ? ' · <i>odnalezione po numerze</i>' : ""}</div>
       <div class="odw-tresc">${odwFragment(o)}</div><div class="odw-stopka">Kliknij, aby otworzyć cały dokument w tym miejscu</div>`
    : `<div class="odw-glowa"><b>${esc(o.miejsce || "Odwołanie")}</b></div><div class="odw-tresc">Nie znaleziono tego fragmentu dosłownie w dokumentach – sprawdź ręcznie (AI mogło pomylić numerację albo dokument jest skanem).</div>`;
  d.style.display = "block"; d.dataset.dla = el.dataset.odw;
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  const r = el.getBoundingClientRect(), w = Math.min(520, W - 24);
  d.style.width = w + "px";
  d.style.left = Math.max(12, Math.min(r.left, W - w - 12)) + "px";
  const h = d.offsetHeight;
  d.style.top = (r.bottom + h + 12 < H ? r.bottom + 8 : Math.max(12, r.top - h - 8)) + "px";
}
let ODW_TAP = null;  // telefon: odwołanie pokazane pierwszym dotknięciem
function odwDymekUkryj() { const d = $("#odw-dymek"); if (d) d.style.display = "none"; ODW_TAP = null; }
async function odwOtworz(o) {
  if (!o || !o.znaleziono) return;
  const u = o.ctx && o.ctx.typ === "przetarg" ? `/api/przetargi/tekst-dokumentu?nr=${encodeURIComponent(o.ctx.id)}&plik=${encodeURIComponent(o.plik)}`
    : `/api/projekty/${o.ctx && o.ctx.id}/tekst-dokumentu?plik=${encodeURIComponent(o.plik)}`;
  const d = await bezpiecznie(() => api(u)); if (!d) return;
  const t = d.tekst || "", p = Math.max(0, Math.min(o.poz || 0, t.length)), dl = Math.max(1, (o.do || 0) - (o.od || 0));
  let m = $("#odw-okno"); if (!m) { m = document.createElement("div"); m.id = "odw-okno"; document.body.appendChild(m); }
  m.innerHTML = `<div class="odw-okno-karta"><div class="odw-okno-gora"><span class="odw-okno-tyt"><b>${esc(d.nazwa)}</b>${o.strona ? " · str. " + o.strona : ""}${o.miejsce ? " · " + esc(o.miejsce) : ""}</span>
      <button class="maly" onclick="$('#odw-okno').style.display='none'">Zamknij ✕</button></div>
    <div class="odw-okno-tresc">${esc(t.slice(0, p))}<mark id="odw-cel">${esc(t.slice(p, p + dl))}</mark>${esc(t.slice(p + dl))}</div></div>`;
  m.style.display = "flex";
  m.onclick = e => { if (e.target === m) m.style.display = "none"; };
  setTimeout(() => { const c = $("#odw-cel"); if (c) c.scrollIntoView({block: "center"}); }, 50);
}
document.addEventListener("mouseover", e => { const el = e.target.closest && e.target.closest(".odw"); if (el && !window.matchMedia("(hover: none)").matches) odwDymekPokaz(el); });
document.addEventListener("mouseout", e => {
  if (window.matchMedia("(hover: none)").matches) return;  // telefon: dymek zamyka dotknięcie obok
  const el = e.target.closest && e.target.closest(".odw, #odw-dymek"), dok = e.relatedTarget;
  if (el && !(dok && (el.contains(dok) || (dok.closest && dok.closest(".odw, #odw-dymek"))))) odwDymekUkryj();  // można przejechać myszką na dymek i kliknąć
});
document.addEventListener("focusin", e => { const el = e.target.closest && e.target.closest(".odw"); if (el && !window.matchMedia("(hover: none)").matches) odwDymekPokaz(el); });
document.addEventListener("focusout", e => { if (e.target.closest && e.target.closest(".odw") && !window.matchMedia("(hover: none)").matches) odwDymekUkryj(); });
document.addEventListener("click", e => {
  const el = e.target.closest && e.target.closest(".odw");
  if (!el) {
    const dym = e.target.closest && e.target.closest("#odw-dymek");
    if (dym) { const o = ODW[+dym.dataset.dla]; odwDymekUkryj(); odwOtworz(o); return; }  // dotknięcie dymku otwiera cały dokument
    odwDymekUkryj(); return;
  }
  e.preventDefault(); e.stopPropagation();
  const dot = window.matchMedia("(hover: none)").matches;
  if (dot && ODW_TAP !== el.dataset.odw) { odwDymekPokaz(el); ODW_TAP = el.dataset.odw; return; }  // telefon: 1. dotknięcie – dymek, 2. – dokument
  odwDymekUkryj(); odwOtworz(ODW[+el.dataset.odw]);
}, true);

// ---------- podmenu: pod aktywną pozycją menu lista sekcji otwartej strony (np. W realizacji → umowa, harmonogram r-f, protokoły, faktury…)
const KONTENERY_SEKCJI = ["#realizacja", "#projekt", "#dos-real", "#ocena", "#wniosek"];
let PODMENU_T = null;
function odswiezPodmenu() {
  clearTimeout(PODMENU_T);
  PODMENU_T = setTimeout(() => {
    document.querySelectorAll("#nav .podmenu").forEach(x => x.remove());
    const sek = document.getElementById("w-" + WIDOK); if (!sek) return;
    const kont = KONTENERY_SEKCJI.map(s => sek.querySelector(s)).find(Boolean); if (!kont) return;
    const kroki = [...kont.querySelectorAll(".krok")].filter(k => k.offsetParent !== null && k.querySelector("h3") && !k.parentElement.closest(".krok"));
    if (kroki.length < 2) return;
    const btn = [...document.querySelectorAll("#nav button.akt")].find(b => getComputedStyle(b).display !== "none"); if (!btn) return;
    kroki.forEach((k, i) => { if (!k.id) k.id = "sekcja-" + WIDOK + "-" + i; });
    const div = document.createElement("div"); div.className = "podmenu";
    div.innerHTML = kroki.map(k => { const t = (k.querySelector("h3").textContent || "").replace(/^\s*\d+\.\s*/, "").trim().split(" – ")[0];
      return `<a href="#${k.id}" data-cel="${k.id}" title="${esc(t)}">${esc(t.length > 48 ? t.slice(0, 46) + "…" : t)}</a>`; }).join("");
    div.querySelectorAll("a").forEach(a => a.onclick = e => {
      e.preventDefault();
      div.querySelectorAll("a").forEach(x => x.classList.toggle("akt", x === a));
      const mob = window.matchMedia("(max-width: 1099px)").matches;
      if (mob) przelaczMenu(true);  // najpierw zamknięcie menu (zmienia układ strony), potem przewinięcie
      setTimeout(() => { const c = document.getElementById(a.dataset.cel); if (c) c.scrollIntoView({behavior: "smooth", block: "start"}); }, mob ? 250 : 0);
    });
    btn.after(div);
  }, 250);
}
setInterval(() => { if (!document.querySelector("#nav .podmenu") && !document.hidden) odswiezPodmenu(); }, 2000);  // zabezpieczenie, gdyby zmiana strony nie została wychwycona
new MutationObserver(m => { if (m.some(x => x.target.closest && !x.target.closest("header, #nav, #zadania, #komunikat, .komunikat") && x.target.closest("main, .widok"))) odswiezPodmenu(); })
  .observe(document.body, {childList: true, subtree: true});

// ---------- przycisk Wstecz (telefon i przeglądarka) – powrót do poprzedniego ekranu zamiast wyjścia z programu
let Z_HISTORII = false, WYJSCIE_T = 0;
function zapiszHistorie(w) {
  if (Z_HISTORII) return;
  const st = history.state || {};
  const nowy = {w, s: STRONA, c: CEL, p: TRYBY[w] ? PROJEKT_ID : null};
  if (st.w === nowy.w && st.s === nowy.s && st.c === nowy.c && st.p === nowy.p) return;
  history.pushState(nowy, "", location.pathname);
}
function zamknijNakladke() {  // otwarte okno, dymek, menu albo pomoc – Wstecz najpierw je zamyka
  const o = $("#odw-okno"); if (o && o.style.display === "flex") { o.style.display = "none"; return true; }
  const d = $("#odw-dymek"); if (d && d.style.display === "block") { odwDymekUkryj(); return true; }
  const h = document.querySelector("header"); if (h && h.classList.contains("otwarte")) { przelaczMenu(true); return true; }
  const pp = $("#pomoc-panel"); if (pp && !pp.classList.contains("ukryj")) { przelaczPomoc(); return true; }
  return false;
}
window.addEventListener("popstate", e => {
  const st = e.state || {};
  if (zamknijNakladke()) { history.pushState(Object.assign({}, st.korzen ? {w: WIDOK, s: STRONA, c: CEL} : st), "", location.pathname); return; }
  if (st.korzen || !st.w) {  // początek historii: zamiast wyjścia – ekran „Co chcesz zrobić?” albo wybór trybu; drugi Wstecz na starcie zamyka
    if (WIDOK === "start" && Date.now() - WYJSCIE_T < 2500) { history.back(); return; }
    const cel = WIDOK !== "cel" && WIDOK !== "start" && CELE[STRONA] && !(STRONA === "zamawiajacy" && !MZ().ma_cele) ? "cel" : "start";
    history.pushState({w: cel, s: STRONA, c: CEL}, "", location.pathname);
    Z_HISTORII = true; try { pokaz(cel); } finally { Z_HISTORII = false; }
    if (cel === "start") { WYJSCIE_T = Date.now(); komunikat("Naciśnij Wstecz jeszcze raz, aby zamknąć program."); }
    return;
  }
  Z_HISTORII = true;
  try {
    if (st.s && st.s !== STRONA) wybierzStrone(st.s, false, true);
    if ((st.c || null) !== CEL && st.s) { CEL = st.c || null; zastosujCel(); }
    if (st.w !== WIDOK) pokaz(st.w);
    if (TRYBY[st.w]) {
      if (st.p && st.p !== PROJEKT_ID) otworzProjekt(st.p);
      else if (!st.p && PROJEKT_ID) { PROJEKT_ID = null; $("#projekt").innerHTML = pustyProjekt(); document.querySelectorAll("#lista-projektow li").forEach(li => li.classList.remove("akt")); }
    }
  } finally { Z_HISTORII = false; }
});
function pokaz(w) {
  setTimeout(odswiezPodmenu, 700);
  if (w === "cel" && !CELE[STRONA]) w = "pulpit";
  celDlaWidoku(w);
  if (typeof wolnoWidok === "function" && JA.uprawnienia && !wolnoWidok(w)) return komunikat("Twoja rola nie ma dostępu do tego modułu.", true);
  WIDOK = w;
  document.body.classList.toggle("tryb-start", w === "start");
  document.body.classList.toggle("tryb-cel", w === "cel");
  zapiszHistorie(w);
  setTimeout(odswiezGrupyMenu, 0);
  if (w !== "start" && !STRONA) { const s = document.querySelector(`#nav button[data-w="${w}"]`)?.dataset.strona; if (s) wybierzStrone(s); }
  przelaczMenu(true);
  const btn = [...document.querySelectorAll(`#nav button[data-w="${w}"]`)].find(b => !b.dataset.strona || b.dataset.strona === STRONA)?.querySelector(".etykieta");
  if ($("#tytul-mob")) $("#tytul-mob").textContent = w === "cel" ? "Co chcesz zrobić?" : btn ? btn.textContent : $("#tytul-mob").textContent;
  const sekcja = TRYBY[w] ? "projekty" : w === "place" || w === "kadry" ? "pracownicy" : w === "zam_realizacja" || w === "inw_budowa" ? "realizacja" : w === "pr_oferty" ? "zam_oferty" : w;
  document.body.classList.toggle("widok-kolumny", ["projekty", "realizacja"].includes(sekcja));
  setTimeout(ustawWysokoscNaglowka, 0);
  if (w === "zam_realizacja" || w === "realizacja" || w === "inw_budowa") { const s = {zam_realizacja: "zamawiajacy", inw_budowa: "inwestor"}[w] || "wykonawca"; if (STRONA_REAL !== s) { STRONA_REAL = s; REAL_ID = null; } }
  if (TRYBY[w] && TRYB !== TRYBY[w]) { TRYB = TRYBY[w]; PROJEKT_ID = null; $("#projekt").innerHTML = pustyProjekt(); if ($("#pr-szukaj")) $("#pr-szukaj").value = ""; }
  if (TRYBY[w]) { FOKUS = FOKUS_WIDOKU[w] || null; FOKUS_KZ = {zam_kosztorys: "wartosc", zam_dokumentacja: "dokumenty", zam_weryfikacja: "zmiany"}[w] || null; if (PROJEKT_ID && FOKUS) setTimeout(() => document.getElementById(FOKUS)?.scrollIntoView({behavior: "smooth"}), 600); }
  document.querySelectorAll("#nav button").forEach(b => b.classList.toggle("akt", b.dataset.w === w));
  document.querySelectorAll(".widok").forEach(s => s.classList.toggle("ukryj", s.id !== "w-" + sekcja));
  ({przetargi: () => { ladujObszar(); ladujPrzetargi(); if (!SLOWA) ladujSlowa(); else rysujSlowa(); if (NOWE_INFO) rysujNowePulpit(); }, projekty: ladujProjekty, wlasne: ladujProjekty, kosztorys: ladujProjekty,
    wyniki: rysujWyniki, kalk_pracy: rysujKalkPracy, plan_zam: () => ladujPlanZam(), plan_spr: () => ladujPlanSpr(), olioc: ladujOlioc, zam_zapytania: () => ladujZapytaniaWsp(), sprawozdanie: () => ladujSprawozdanie(), windykacja: () => (JA && JA.windykacja) ? ladujWind() : komunikat("Moduł Windykacja nie jest udostępniony temu kontu.", true), leady: () => WLASC() ? ladujLeady() : komunikat("Ten moduł jest dostępny tylko dla właściciela programu.", true), ksiegowosc: () => { if (!JA.ksiegowosc) return komunikat("Moduł Księgowość nie jest udostępniony dla tego konta – poproś administratora o dostęp.", true); ladujKsieg(); ksKlienciBiura(); }, dos_realizacja: ladujDostawy, zam_oferty: ladujOceny, pr_oferty: ladujOceny, realizacja: ladujRealizacje, zam_realizacja: ladujRealizacje, inw_budowa: ladujRealizacje, inw_projekty: ladujProjekty, kos_projekty: ladujProjekty, dot_projekty: ladujProjekty, dot_wnioski: ladujProjekty, dot_szukaj: rysujSzukajDotacji, dot_nadchodzace: rysujNadchodzace, zam_nowe: rysujZamNowe, zam_kosztorys: ladujProjekty, zam_weryfikacja: ladujProjekty,
    zam_dokumentacja: ladujProjekty, zam_projekty: ladujProjekty, odwolania: () => WLASC() ? ladujOdwolania() : komunikat("Ten moduł jest dostępny tylko dla właściciela programu.", true), pr_sprawy: ladujProjekty, pr_sporzadz: () => { ladujProjekty(); setTimeout(nowaSprawaPrzygotuj, 300); }, firma: ladujFirme, konta: ladujKonta, cel: rysujCel, dot_zapytania: ladujZapytania, nier: ladujNier, kadry: () => { ladujPracownikow(); podzakladka("kadry"); }, start: () => {}, pulpit: rysujPulpit, archiwum: ladujArchiwum, klienci: ladujKlientow, hurtownie: ladujHurtownie,
    pracownicy: () => { ladujPracownikow(); podzakladka("rg"); }, place: () => { ladujPracownikow(); podzakladka("umowy"); },
    ustawienia: ladujUstawienia,
    instrukcja: () => otworzInstrukcje(ROZDZIAL_DO_OTWARCIA)})[w]();
}

// ================================================================ PRZETARGI
let PRZETARGI = [], P_SORT = ["ocena", -1], P_WYBRANE = new Set(), P_AKT = null;
let ZAKRES_P = "obszar", POZA_OBSZAREM = 0;
let P_DO_OTWARCIA = null, P_FILTR_PO = null, OSTATNIE = null;
function pokazNowe() { P_FILTR_PO = "nowe"; if (WIDOK === "przetargi") { $("#p-filtr").value = "nowe"; P_FILTR_PO = null; rysujPrzetargi(); } else pokaz("przetargi"); }
function otworzPrzetarg(nr, konto) {  // przejście z pulpitu (polecane przetargi) prosto do szczegółów przetargu
  P_DO_OTWARCIA = {nr, konto: konto || ""};
  const q = $("#p-szukaj"); if (q) q.value = "";
  if (WIDOK === "przetargi" && PRZETARGI && PRZETARGI.length) { otworzOczekujacy(); return; }
  pokaz("przetargi");
}
function otworzOczekujacy() {
  if (!P_DO_OTWARCIA) return;
  const {nr, konto} = P_DO_OTWARCIA; P_DO_OTWARCIA = null;
  if (!(PRZETARGI || []).some(t => t.numer === nr)) {
    if (ZAKRES_P !== "wszystkie") { P_DO_OTWARCIA = {nr, konto}; komunikat("Przetarg jest spoza wybranego obszaru – pokazuję wszystkie pobrane."); ustawZakres("wszystkie"); }
    else komunikat("Nie znaleziono tego przetargu na liście.", true);
    return;
  }
  const f = $("#p-filtr"); if (f && f.value !== "wszystkie" && f.value !== "aktywne") { f.value = "wszystkie"; rysujPrzetargi(); }
  szczegolyP(nr, konto);
  setTimeout(() => { const el = $("#p-szczegoly"); if (el) el.scrollIntoView({behavior: "smooth", block: "start"}); }, 150);
}
async function ladujPrzetargi() {
  const strona = STRONA || "wykonawca";
  if (!WY && $("#wysz") && !$("#wysz").innerHTML) $("#wysz").innerHTML = '<div class="wy-pasek"><span class="wy-pasek-opis">Ładuję wyszukiwarkę i wyniki…</span></div>';
  await bezpiecznie(async () => {
    // lista przetargów, ostatnie wyszukiwanie i ustawienia wyszukiwarki – równolegle, nie jedno po drugim
    const [r, ost] = await Promise.all([
      fetch("/api/przetargi" + (ZAKRES_P === "wszystkie" ? "?zakres=wszystkie" : ""), {headers: {"X-Agent": "1"}}),
      api("/api/przetargi/ostatnie?tryb=" + strona).catch(() => null),
      (!WY || WY._strona !== strona) ? ladujWyszukiwarke().then(() => { if (WY) WY._strona = strona; }) : null]);
    if (r.status === 401) { location.href = "/login"; return; }
    if ((STRONA || "wykonawca") !== strona) return;  // w międzyczasie zmieniono tryb – te dane już nieaktualne
    PRZETARGI = await r.json(); POZA_OBSZAREM = +(r.headers.get("X-Poza-Obszarem") || 0);
    OSTATNIE = ost;
    const info = $("#p-zakres-info");
    if (info) info.innerHTML = ZAKRES_P === "obszar"
      ? (POZA_OBSZAREM ? `Pokazano przetargi z wybranego obszaru oraz te z Twoich projektów i wygrane. Ukryto ${POZA_OBSZAREM} spoza obszaru – <a href="#" onclick="ustawZakres('wszystkie'); return false">pokaż wszystkie pobrane</a>.` : "Pokazano przetargi z wybranego obszaru.")
      : `Pokazano wszystkie pobrane przetargi – <a href="#" onclick="ustawZakres('obszar'); return false">tylko z wybranego obszaru</a>.`;
    if (P_FILTR_PO && $("#p-filtr")) { $("#p-filtr").value = P_FILTR_PO; P_FILTR_PO = null; }
    else if (!TABELA() && $("#p-filtr") && !["nowe"].includes($("#p-filtr").value)) $("#p-filtr").value = (OSTATNIE && OSTATNIE.aktualne && (OSTATNIE.numery || []).length) ? "ostatnie" : "aktywne";
    rysujPrzetargi();
    if (P_DO_OTWARCIA) setTimeout(otworzOczekujacy, 50);
  });
}
function ustawZakres(z) { ZAKRES_P = z; const s = $("#p-zakres"); if (s) s.value = z; ladujPrzetargi(); }
function rysujPrzetargi() {  // zabezpieczenie: błąd rysowania nie może zostawić pustego ekranu
  try { rysujPrzetargiW(); }
  catch (e) {
    console.error(e);
    const el = $("#p-karty") || $("#p-tabela");
    if (el) el.innerHTML = `<div class="ramka-uwaga">Nie udało się wyświetlić listy przetargów (${esc(e.message)}). Odśwież stronę klawiszami Ctrl+F5;
      jeśli to nie pomoże – prześlij zrzut tego komunikatu.</div>`;
  }
}
function rysujPrzetargiW() {
  const f = $("#p-filtr").value, q = $("#p-szukaj").value.toLowerCase(), teraz = new Date().toISOString().slice(0, 16);
  const rz = $("#p-rodzaj") ? $("#p-rodzaj").value : "", tz = $("#p-typzam") ? $("#p-typzam").value : "";
  const ost = f === "ostatnie" ? new Set((OSTATNIE || {}).numery || []) : null;
  let l = PRZETARGI.filter(t => {
    if (ost && !ost.has(t.numer)) return false;
    if (STRONA === "dostawca" && !rz && t.rodzaj_zam === "roboty" && !(t.projekt && t.projekt.rodzaj_zamowienia)) return false;
    if (rz && t.rodzaj_zam !== rz) return false;
    if (tz && t.typ_zam !== tz) return false;
    // ze stron zamawiających program pobiera wszystkie rodzaje zamówień – wykonawca widzi roboty budowlane (chyba że wybrał rodzaj w filtrze)
    // wykonawca widzi roboty budowlane; dostawy i usługi są w trybie Dostawca (chyba że wybrano rodzaj w filtrze)
    if (STRONA === "wykonawca" && !rz && ["dostawy", "uslugi"].includes(t.rodzaj_zam) && !t.projekt && !["startujemy", "oferta złożona", "wygrany"].includes(t.status)) return false;
    if (f === "nieocenione" && t.ocena != null && t.ocena !== "") return false;
    if (f === "nowe" && !t.nowy) return false;
    if (STATUSY.includes(f) && t.status !== f) return false;
    const trwa = t.status === "wygrany" || (t.projekt && t.projekt.status_projektu !== "zakonczony");  // mój projekt / wygrany – wciąż aktywny
    if ((f === "aktywne" || (f === "ostatnie" && !TABELA())) && !trwa && /^\d{4}-\d{2}-\d{2}/.test(t.termin_ofert || "") && t.termin_ofert.slice(0, 16) < teraz) return false;
    return !q || JSON.stringify(t).toLowerCase().includes(q);
  });
  if (!TABELA() && $("#p-karty") && $("#p-wyniki-gora")) { rysujKarty(l); return; }
  document.body.classList.add("bez-kart");  // stary układ strony (np. niepełna aktualizacja) – lista w tabeli
  const [k, kier] = P_SORT;
  l.sort((a, b) => { const x = k === "ocena" ? (+a[k] || -1) : String(a[k] || ""), y = k === "ocena" ? (+b[k] || -1) : String(b[k] || "");
    return (x > y ? 1 : x < y ? -1 : 0) * kier; });
  const kol = [["", ""], ["ocena", "Ocena"], ["rekomendacja", "Rekomendacja"], ["status", "Status"], ["termin_ofert", "Termin ofert"],
    ["przedmiot", "Przedmiot"], ["zamawiajacy", "Zamawiający"], ["lokalizacja", "Lokalizacja"], ["zrodlo", "Źródło"]];
  $("#p-tabela").innerHTML = "<tr>" + kol.map(([k, n]) => k ? `<th class="sort" onclick="sortujP('${k}')">${n}${P_SORT[0] === k ? (P_SORT[1] > 0 ? " ▲" : " ▼") : ""}</th>` :
    `<th><input type="checkbox" onclick="zaznaczWszystkieP(this.checked)"></th>`).join("") + "</tr>" +
    l.map(t => {
      const kl = t.status === "startujemy" || t.rekomendacja === "startujemy" ? "start" : t.status === "odpuszczamy" || t.rekomendacja === "odpuszczamy" ? "odpusc" : t.rekomendacja === "do analizy" ? "analiza" : "";
      return `<tr class="klik ${kl} ${t.nowy ? "nowy" : ""} ${P_AKT === t.numer ? "wybrany" : ""}" onclick="szczegolyP('${escA(t.numer)}', '${escA(t.konto || "")}')">
        <td>${t.obcy ? "" : `<input type="checkbox" ${P_WYBRANE.has(t.numer) ? "checked" : ""} onclick="event.stopPropagation(); zaznaczP('${escA(t.numer)}', this.checked)">`}</td>
        <td>${t.ocena != null && t.ocena !== "" ? `<span class="ocena">${esc(t.ocena)}</span>` : "–" + znacznikSita(t)}</td>
        <td>${t.rekomendacja ? `<span class="znacznik z-${esc(t.rekomendacja).replace(" ", "-")}">${esc(t.rekomendacja)}</span>` : ""}</td>
        <td>${esc(t.status || "nowy")}${t.projekt ? `<br><a href="#" class="znacznik z-startujemy" title="Otwórz projekt: ${esc(t.projekt.nazwa)}"
          onclick="event.stopPropagation(); ${t.projekt.status_projektu ? `doRealizacji('${t.projekt.id}', false)` : `kartaProjektu('${t.projekt.id}', '${t.projekt.typ}')`}; return false">${t.projekt.status_projektu === "realizacja" ? "w realizacji" : t.projekt.status_projektu === "zakonczony" ? "zakończony" : "w projekcie"}</a>` : ""}</td>
        <td>${esc(dataPl(t.termin_ofert))}</td><td>${t.nowy ? '<span class="znacznik-nowy">NOWY</span> ' : ""}${esc(t.przedmiot)}</td>
        <td>${esc(t.zamawiajacy)}</td><td>${esc(t.lokalizacja)}</td><td>${esc(t.zrodlo)}${t.konto ? `<br><span class="znacznik z-odpuszczamy">konto: ${esc(t.konto)}</span>` : ""}</td></tr>`;
    }).join("");
  const ileNowych = PRZETARGI.filter(t => t.nowy).length;
  $("#p-licznik").innerHTML = esc(`Widoczne: ${l.length} / wszystkie: ${PRZETARGI.length}` + (P_WYBRANE.size ? ` · zaznaczone: ${P_WYBRANE.size}` : ""))
    + (ileNowych ? ` · <a href="#" onclick="$('#p-filtr').value='nowe'; rysujPrzetargi(); return false"><b>${ileNowych} nowych</b></a>
      · <a href="#" onclick="przejrzaneWszystkie(); return false">oznacz jako przejrzane</a>` : "")
    + (f === "ostatnie" ? `<br><b>Wyniki wyszukiwania ${OSTATNIE && OSTATNIE.data ? "z " + esc(OSTATNIE.data) : ""}</b>${OSTATNIE && (OSTATNIE.slowa || []).length ? ` (słowa: ${esc(OSTATNIE.slowa.slice(0, 8).join(", "))}${OSTATNIE.slowa.length > 8 ? "…" : ""})` : ""}
      · <a href="#" onclick="$('#p-filtr').value='aktywne'; rysujPrzetargi(); return false">pokaż wszystkie aktywne</a>`
      : (OSTATNIE && (OSTATNIE.numery || []).length ? ` · <a href="#" onclick="$('#p-filtr').value='ostatnie'; rysujPrzetargi(); return false">wyniki ostatniego wyszukiwania</a>` : ""));
  ustawLicznikNav(ileNowych);
}
function sortujP(k) { P_SORT = P_SORT[0] === k ? [k, -P_SORT[1]] : [k, k === "ocena" ? -1 : 1]; rysujPrzetargi(); }
function zaznaczP(nr, v) { v ? P_WYBRANE.add(nr) : P_WYBRANE.delete(nr); rysujPrzetargi(); }
function zaznaczWszystkieP(v) { document.querySelectorAll("#p-tabela tr.klik").forEach((tr, i) => {}); if (!v) P_WYBRANE.clear();
  else PRZETARGI.forEach(t => P_WYBRANE.add(t.numer)); rysujPrzetargi(); }
const GRUPY_ANALIZY = [
  ["Najważniejsze", [["streszczenie", "Streszczenie"], ["zakres_robot", "Zakres robót"], ["lokalizacja_robot", "Miejsce robót"], ["tryb", "Tryb postępowania"], ["czesci", "Podział na części"]]],
  ["Terminy", [["termin_skladania", "Składanie ofert"], ["termin_pytan", "Pytania do SWZ do"], ["wizja_lokalna", "Wizja lokalna"], ["termin_realizacji", "Termin realizacji"], ["termin_zwiazania", "Związanie ofertą"]]],
  ["Pieniądze", [["szacowana_wartosc", "Szacowana wartość"], ["budzet", "Budżet zamawiającego"], ["wadium", "Wadium"], ["zabezpieczenie", "Zabezpieczenie należytego wykonania"],
    ["wynagrodzenie", "Rodzaj wynagrodzenia"], ["platnosci", "Płatności / zaliczki"], ["kary_umowne", "Kary umowne"]]],
  ["Warunki udziału i ocena ofert", [["warunki_udzialu", "Warunki udziału"], ["doswiadczenie", "Wymagane doświadczenie"], ["osoby", "Wymagane osoby / uprawnienia"],
    ["sytuacja_finansowa", "OC / sytuacja finansowa"], ["kryteria_oceny", "Kryteria oceny ofert"], ["gwarancja", "Gwarancja / rękojmia"], ["dokumenty", "Dokumenty do oferty"],
    ["miejsce_skladania", "Gdzie złożyć ofertę"]]],
  ["Ocena dla firmy", [["dopasowanie", "Dlaczego taka ocena"], ["ryzyka", "Ryzyka"], ["szanse", "Szanse / konkurencja"], ["nastepne_kroki", "Co zrobić dalej"], ["brakujace", "Czego brakuje"]]]];
function dniDo(termin) {
  if (!termin) return null; const d = new Date(String(termin).slice(0, 10) + "T12:00:00"); if (isNaN(d)) return null;
  return Math.round((d - new Date(DZIS_ISO() + "T12:00:00")) / 86400000);
}
function szczegolyP(nr, konto) {
  konto = typeof konto === "string" ? konto : "";
  const t = PRZETARGI.find(x => x.numer === nr && (x.konto || "") === konto); if (!t) return;
  if (t.nowy) { t.nowy = false; api("/api/przetargi/widziane", {json: {numer: nr}}).then(odswiezLicznikNowych).catch(() => {}); }
  P_AKT = nr; rysujPrzetargi();
  const puste = v => !v || /^(brak w (ogłoszeniu|dokumentach)|brak danych|nie podano)\.?$/i.test(String(v).trim());
  const dni = dniDo(t.termin_ofert);
  const kafel = (tyt, v, kl = "") => `<div class="${kl}"><span>${tyt}</span><b>${esc(v || "–")}</b></div>`;
  const oceniony = t.ocena != null && t.ocena !== "";
  const el = $("#p-szczegoly"); el.classList.remove("ukryj");
  el.innerHTML = `<h3>${esc(t.przedmiot)}</h3>
    <div class="opis">${esc(t.zamawiajacy)} · ${esc(t.lokalizacja)} · ${esc(t.zrodlo)} · nr ${esc(nr)}</div>
    <div class="kwoty kafle-przetargu">
      <div class="${dni !== null && dni < 0 ? "alarm" : dni !== null && dni <= 3 ? "pilne" : "brutto"}"><span>Termin składania ofert
        <button class="maly edytuj-termin bez-podgladu" title="Popraw termin" onclick="edytujTermin('${escA(nr)}')">✎</button></span>
        <b>${t.termin_ofert ? esc(dataPl(t.termin_ofert)) : "nie ustalono"}</b>
        <small>${dni === null ? "" : dni < 0 ? "termin minął" : dni === 0 ? "dziś!" : `za ${odm(dni, "dzień", "dni", "dni")}`}${t.termin_zrodlo ? " · " + esc(t.termin_zrodlo) : ""}</small></div>
      ${kafel("Szacowana wartość", puste(t.szacowana_wartosc) ? "" : t.szacowana_wartosc)}
      ${kafel("Wadium", puste(t.wadium) ? "" : t.wadium)}
      ${kafel("Termin realizacji", puste(t.termin_realizacji) ? "" : t.termin_realizacji)}
      ${kafel("Wymagana gwarancja", puste(t.gwarancja) ? "" : t.gwarancja)}
      ${kafel("Wynagrodzenie", puste(t.wynagrodzenie) ? "" : t.wynagrodzenie)}
    </div>
    ${oceniony ? `<p class="opis" style="margin:4px 0 10px">Analiza: <b>${t.analiza_zrodlo ? esc(t.analiza_zrodlo) : "z ogłoszenia"}</b>${t.analiza_data ? " · " + esc(t.analiza_data) : ""}
      ${t.analiza_zrodlo === "ocena szybka" ? ` – to szybka ocena dopasowania. <a href="#" onclick="api('/api/przetargi/ocen', {json: {numery: ['${escA(t.numer)}']}}).then(z => sledz(z, () => szczegolyP('${escA(t.numer)}', '${escA(t.konto || "")}'))); return false">Szczegółowa ocena z ogłoszenia</a> albo <b>Pełna analiza z dokumentami</b> pokażą terminy, warunki i ryzyka.`
        : (t.analiza_zrodlo || "").startsWith("dokumenty") ? "" : STRONA === "dostawca" ? " – pełną analizę z dokumentów zrobi krok 2 oferty („Przygotuj ofertę”)." : " – więcej szczegółów da <b>Pełna analiza z dokumentami</b>."}</p>
      ${GRUPY_ANALIZY.map(([g, pola]) => { const wiersze = pola.filter(([k]) => t[k] && !puste(t[k]));
        const braki = pola.filter(([k]) => k !== "brakujace" && puste(t[k])).map(([, n]) => n);
        return wiersze.length || braki.length ? `<h4 class="grupa-analizy">${esc(g)}</h4><dl>${wiersze.map(([k, n]) => `<dt>${n}</dt><dd>${esc(t[k])}${odwPola(t, k)}</dd>`).join("")}</dl>
          ${braki.length ? `<p class="opis braki">Brak w ${(t.analiza_zrodlo || "").startsWith("dokumenty") ? "dokumentach" : "ogłoszeniu"}: ${esc(braki.join(", "))}</p>` : ""}` : ""; }).join("")}
      ${odwPozostale(t)}
      ${(t.dok_pliki || []).length ? `<details class="opis"><summary>Przeanalizowane dokumenty (${t.dok_pliki.length})</summary>${t.dok_pliki.map(esc).join("<br>")}</details>` : ""}`
      : `${(t.sito || {}).slabe ? `<p class="opis">Wstępne sito bez AI: słabe dopasowanie do Twoich słów (${esc(t.sito.opis || "")}) – dlatego nie było oceniane automatycznie.</p>` : ""}<p class="pusto" id="p-ocena-auto">${autoOcena(t) ? "Trwa ocena AI tego przetargu – wynik pojawi się za chwilę." : "Ten przetarg nie ma jeszcze oceny AI – zostanie oceniony przy najbliższym wyszukiwaniu."}</p>`}
    <div class="pasek" style="margin-top:12px">
      <button class="zielony" data-ik="dokument" onclick="ofertaZPrzetargu('${escA(nr)}')">Przygotuj ofertę</button>
      ${STRONA === "dostawca" ? "" : `<button class="glowny" data-ik="iskra" onclick="pelnaAnaliza('${escA(nr)}')">Pełna analiza z dokumentami</button>`}
      ${t.link ? `<a class="przycisk dozw" data-ik="link" href="${esc(t.link)}" target="_blank" rel="noopener">Otwórz ogłoszenie</a>` : ""}
      <select id="p-status">${STATUSY.map(s => `<option ${s === (t.status || "nowy") ? "selected" : ""}>${s}</option>`).join("")}</select>
      <button data-ik="flaga" onclick="ustawStatus(['${escA(nr)}'], $('#p-status').value)">Ustaw status</button>
      <button class="niebezp tylko-admin" data-ik="kosz" onclick="usunP(['${escA(nr)}'])">Usuń</button>
    </div>
    <div class="historia-zam" id="p-historia"><div class="pasek"><button data-ik="trofeum" onclick="historiaPrzetargu('${escA(nr)}')">Konkurencja u zamawiającego – ceny, liczba ofert, zwycięzcy</button>
      <span class="opis" style="margin:0">z ogłoszeń o wyniku postępowań w BZP (ostatnie 24 miesiące)</span></div></div>`;
  api("/api/przetargi/historia/" + encodeURIComponent(nr)).then(h => { if (h && h.data && P_AKT === nr) rysujHistorie($("#p-historia"), h, () => historiaPrzetargu(nr, true)); }).catch(() => {});
  if (t.obcy) {  // przetarg z listy innego konta – podgląd; działania na koncie właściciela
    el.querySelectorAll("button, select").forEach(b => b.remove());
    el.insertAdjacentHTML("afterbegin", `<div class="ramka-uwaga" style="margin-bottom:10px">Przetarg z listy konta <b>${esc(t.konto)}</b> (podgląd administratora).
      Możesz go też ofertować u siebie – na Twojej liście powstanie kopia, a lista i oferta konta ${esc(t.konto)} zostają bez zmian.
      <div class="pasek" style="margin-top:8px"><button class="glowny" data-ik="dokument" onclick="przejmijPrzetarg('${escA(nr)}', '${escA(t.konto)}', true)">Przygotuj ofertę u siebie</button>
      <button data-ik="plus" onclick="przejmijPrzetarg('${escA(nr)}', '${escA(t.konto)}', false)">Dodaj do mojej listy</button>
      <button class="maly" onclick="otworzKonto('${escA(t.konto)}')">Otwórz konto ${esc(t.konto)}</button></div></div>`);
  }
  el.scrollIntoView({behavior: "smooth", block: "nearest"});
}
async function pelnaAnaliza(nr) {
  komunikat("Pobieram dokumenty i analizuję – zwykle 1–3 minuty.");
  sledz(await bezpiecznie(() => api("/api/przetargi/analiza", {json: {numer: nr}})), async () => { await ladujPrzetargi(); szczegolyP(nr); });
}
async function edytujTermin(nr) {
  const t = PRZETARGI.find(x => x.numer === nr);
  const v = prompt("Termin składania ofert (np. 20.10.2026 10:00):", t.termin_ofert ? dataPl(t.termin_ofert) : "");
  if (v === null) return;
  if (await bezpiecznie(() => api("/api/przetargi/termin", {json: {numer: nr, termin: v}}))) { await ladujPrzetargi(); szczegolyP(nr); }
}
let OBSZAR = null;
// ---------- obserwowane BIP
let BIPD = null;
async function ladujBIP() {
  BIPD = await bezpiecznie(() => api("/api/bip")); if (!BIPD) return;
  const Z = BIPD.zrodla, P = BIPD.propozycje, T = BIPD.typy;
  $("#bip-licznik").textContent = Z.length ? `${Z.filter(z => z.aktywne !== false).length} obserwowanych` + (P.length ? ` · ${P.length} do zatwierdzenia` : "") : "";
  const q = ($("#bip-szukaj") && $("#bip-szukaj").value || "").toLowerCase();
  $("#bip").innerHTML = `
  <p class="opis">Program codziennie odwiedza strony zamówień wybranych urzędów (BIP lub platforma zakupowa) i gdy pojawi się coś nowego,
    AI wyłapuje ogłoszenia o zamówieniach – roboty budowlane, dostawy i usługi – także zapytania ofertowe poniżej progu Pzp (170 tys. zł), których nie ma w BZP.
    Oprócz urzędów możesz dodać <b>szpitale, uczelnie i instytuty</b> oraz <b>duże spółki</b> (KGHM, Orlen, PGE, Tauron, PKP, Poczta Polska, spółki komunalne),
    które ogłaszają dużo przetargów, często na własnych platformach. Nowe ogłoszenia trafiają do listy przetargów ze źródłem „BIP”.</p>
  <div class="karta" style="margin-top:0"><h3>${ik("szukaj")} Znajdź strony zamawiających w moim obszarze</h3>
    <p class="opis" style="margin:0 0 6px">Obszar: <b>${esc(BIPD.obszar_opis || "nie ustawiono")}</b> – ustawiasz go raz, w panelu <b>Obszar wyszukiwania</b> powyżej; ten sam obszar służy do filtrowania BZP i Bazy Konkurencyjności.</p>
    <div class="wybor-h">${Object.entries(T).map(([k, v]) => `<label><input type="checkbox" class="bip-typ" value="${k}" checked> ${esc(v)}</label>`).join("")}</div>
    <div class="pasek"><button class="zolty" data-ik="iskra" onclick="odkryjBIP()" ${BIPD.obszar_tryb === "polska" ? "disabled title=\"Wybierz województwa albo okolicę\"" : ""}>Znajdź strony zamówień (AI)</button>
      <span class="opis" style="margin:0">${BIPD.obszar_tryb === "polska" ? "Przy obszarze „cała Polska” wybierz województwa albo okolicę miejscowości." : "Jeden powiat to ok. 1–2 min, całe województwo – kilkanaście–kilkadziesiąt minut."}</span></div>
  </div>
  ${P.length ? `<div class="karta"><h3>${ik("protokol")} Znalezione strony – sprawdź i zatwierdź (${P.length})</h3>
    <div class="tabela-okno" style="max-height:380px"><table class="tabela"><tr><th><input type="checkbox" onclick="document.querySelectorAll('.bip-p').forEach(c => c.checked = this.checked)"></th>
      <th>Urząd</th><th>Rodzaj</th><th>Powiat</th><th>Strona</th><th>Uwagi</th></tr>
      ${P.map(p => `<tr><td><input type="checkbox" class="bip-p" value="${esc(p.url)}" checked></td><td><b>${esc(p.nazwa)}</b></td><td>${esc(T[p.typ] || p.typ)}</td>
        <td>${esc(p.powiat || "")}</td><td><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.url.replace(/^https?:\/\//, "").slice(0, 60))}</a></td><td>${esc(p.uwagi || "")}</td></tr>`).join("")}</table></div>
    <div class="pasek" style="margin-top:10px"><button class="zielony" data-ik="plus" onclick="propozycjeBIP('dodaj')">Dodaj zaznaczone do obserwowanych</button>
      <button class="niebezp" data-ik="kosz" onclick="propozycjeBIP('odrzuc')">Odrzuć zaznaczone</button></div></div>` : ""}
  <div class="karta"><h3>${ik("flaga")} Obserwowane (${Z.length})</h3>
    <div class="pasek"><button class="zielony" data-ik="szukaj" onclick="sprawdzBIP()">Sprawdź wszystkie teraz</button>
      <input id="bip-szukaj" placeholder="Filtruj…" value="${esc(q)}" oninput="ladujBIPlokalnie()" style="min-width:200px">
      <button data-ik="plus" onclick="$('#bip-reczne').classList.toggle('ukryj')">Dodaj ręcznie</button></div>
    <div id="bip-reczne" class="siatka ukryj"><label>Nazwa urzędu<input id="br-naz"></label><label>Adres strony zamówień<input id="br-url" placeholder="https://..."></label>
      <label>Rodzaj<select id="br-typ">${Object.entries(T).map(([k, v]) => `<option value="${k}">${esc(v)}</option>`).join("")}</select></label>
      <label>Województwo<select id="br-woj">${BIPD.wojewodztwa.map(w => `<option ${w === "dolnośląskie" ? "selected" : ""}>${w}</option>`).join("")}</select></label>
      <label>Powiat<input id="br-pow"></label><label>&nbsp;<button class="zielony" data-ik="zapisz" onclick="dodajBIP()">Zapisz</button></label></div>
    <div id="bip-tabela"></div></div>`;
  ladujBIPlokalnie();
}
function ladujBIPlokalnie() {
  const q = ($("#bip-szukaj")?.value || "").toLowerCase(), T = BIPD.typy;
  const Z = BIPD.zrodla.filter(z => !q || JSON.stringify(z).toLowerCase().includes(q));
  $("#bip-tabela").innerHTML = Z.length ? `<div class="tabela-okno" style="max-height:460px"><table class="tabela"><tr><th>Urząd</th><th>Rodzaj</th><th>Obszar</th><th>Strona</th>
    <th>Ostatnio</th><th>Stan</th><th>Znalezione</th><th></th></tr>
    ${Z.map(z => `<tr class="${z.aktywne === false ? "odpusc" : ""}"><td><b>${esc(z.nazwa)}</b></td><td>${esc(T[z.typ] || z.typ)}</td>
      <td>${esc([z.powiat && "pow. " + z.powiat, z.wojewodztwo].filter(Boolean).join(", "))}</td>
      <td><a href="${esc(z.url)}" target="_blank" rel="noopener">${esc(z.url.replace(/^https?:\/\//, "").slice(0, 45))}</a></td>
      <td>${esc(z.sprawdzono || "–")}</td><td class="${/błąd|pusta/.test(z.status || "") ? "czerwone" : ""}">${esc(z.status || "")}</td>
      <td class="liczba">${z.znalezione || 0}</td>
      <td style="white-space:nowrap"><button class="maly" data-ik="szukaj" title="Sprawdź teraz" onclick="sprawdzBIP(['${z.id}'])"></button>
        <button class="maly" data-ik="przelacz" title="Zmień adres" onclick="zmienUrlBIP('${z.id}')"></button>
        <button class="maly" onclick="zmienBIP('${z.id}', {aktywne: ${z.aktywne === false}})">${z.aktywne === false ? "Włącz" : "Wstrzymaj"}</button>
        <button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Przestać obserwować?')) zmienBIP('${z.id}', {usun: true})"></button></td></tr>`).join("")}</table></div>`
    : '<p class="pusto">Brak obserwowanych stron – użyj „Dodaj obszar” powyżej.</p>';
}
async function odkryjBIP() {  // obszar z panelu „Obszar wyszukiwania” – region ustawiany tylko raz
  const typy = [...document.querySelectorAll(".bip-typ:checked")].map(c => c.value);
  if (BIPD.obszar_tryb === "wojewodztwa" && !confirm(`Wyszukać strony zamawiających w obszarze: ${BIPD.obszar_opis}? Całe województwa to kilkadziesiąt minut i więcej wyszukiwań AI.`)) return;
  sledz(await bezpiecznie(() => api("/api/bip/odkryj-obszar", {json: {typy}})), () => { if (WIDOK === "przetargi") ladujBIP(); });
}
async function propozycjeBIP(akcja) {
  const urls = [...document.querySelectorAll(".bip-p:checked")].map(c => c.value); if (!urls.length) return komunikat("Zaznacz strony.", true);
  const w = await bezpiecznie(() => api("/api/bip/propozycje", {json: {urls, akcja}}));
  if (w) { komunikat(akcja === "dodaj" ? `Dodano do obserwowanych: ${w.ile}. Kliknij „Sprawdź wszystkie teraz”, żeby pobrać ogłoszenia.` : `Odrzucono: ${w.ile}.`); ladujBIP(); }
}
async function sprawdzBIP(ids) {
  sledz(await bezpiecznie(() => api("/api/bip/sprawdz", {json: {ids: ids || null}})), () => { ladujPrzetargi(); if ($("#bip-panel").open) ladujBIP(); });
}
async function zmienBIP(id, zm) { if (await bezpiecznie(() => api("/api/bip/zmien", {json: {id, ...zm}}))) ladujBIP(); }
function zmienUrlBIP(id) { const z = BIPD.zrodla.find(x => x.id === id); const u = prompt("Nowy adres strony zamówień:", z.url); if (u) zmienBIP(id, {url: u}); }
async function dodajBIP() {
  const d = {nazwa: $("#br-naz").value, url: $("#br-url").value, typ: $("#br-typ").value, powiat: $("#br-pow").value, wojewodztwo: $("#br-woj").value};
  if (await bezpiecznie(() => api("/api/bip/zrodla", {json: d}))) { komunikat("Dodano stronę do obserwowanych."); ladujBIP(); }
}
async function ladujObszar() {
  api("/api/bip").then(b => { BIPD = b; $("#bip-licznik").textContent = b.zrodla.length ? `${b.zrodla.filter(z => z.aktywne !== false).length} obserwowanych` + (b.propozycje.length ? ` · ${b.propozycje.length} do zatwierdzenia` : "") : "– dodaj urzędy z wybranego obszaru"; }).catch(() => {});
  OBSZAR = await bezpiecznie(() => api("/api/obszar")); if (!OBSZAR) return;
  NOWE_CENTRUM = null;
  const o = OBSZAR.obszar || {tryb: "wojewodztwa", wojewodztwa: []}, wyb = new Set(o.wojewodztwa || []);
  const prom = OBSZAR.promienie.includes(+OBSZAR.promien) ? +OBSZAR.promien : 10;
  $("#obszar").innerHTML = `<div class="tryby"><b>${ik("szukaj")} Obszar wyszukiwania:</b>
    <label><input type="radio" name="ob" value="polska" ${o.tryb === "polska" ? "checked" : ""} onchange="rysujWoj()"> Cała Polska</label>
    <label><input type="radio" name="ob" value="wojewodztwa" ${o.tryb === "wojewodztwa" ? "checked" : ""} onchange="rysujWoj()"> Wybrane województwa</label>
    <label><input type="radio" name="ob" value="promien" ${o.tryb === "promien" ? "checked" : ""} onchange="rysujWoj()"> Okolica wybranej miejscowości</label>
    <span class="opis" style="margin:0 0 0 auto">Teraz: <b>${esc(OBSZAR.opis)}</b></span></div>
    <div class="woj" id="ob-woj">${OBSZAR.wojewodztwa.map(w => `<label><input type="checkbox" class="obw" value="${esc(w)}" ${wyb.has(w) ? "checked" : ""}> ${esc(w)}</label>`).join("")}</div>
    <div id="ob-prom" class="region">
      <div class="region-wiersz">
        <label class="region-pole">Miejscowość (środek obszaru)
          <div class="region-szukaj"><input id="ob-miasto" placeholder="np. Świdnica, Wałbrzych, Opole…" value="${esc(OBSZAR.centrum_opis || OBSZAR.centrum || "")}" oninput="NOWE_CENTRUM = null"
            onkeydown="if (event.key === 'Enter') { event.preventDefault(); szukajMiasta(); }">
          <button type="button" data-ik="szukaj" onclick="szukajMiasta()">Znajdź</button></div></label>
        <div class="region-pole">Promień
          <div class="segmenty">${OBSZAR.promienie.map(r => `<label><input type="radio" name="obr" value="${r}" ${r === prom ? "checked" : ""}><span>+${r} km</span></label>`).join("")}</div></div>
      </div>
      <div id="ob-podpowiedzi" class="podpowiedzi"></div>
      <div id="ob-wybrana" class="opis" style="margin:6px 0 0">${OBSZAR.centrum ? `Wybrana: <b>${esc(OBSZAR.centrum_opis || OBSZAR.centrum)}</b>` +
        (OBSZAR.miejscowosci.length ? ` · w zasięgu m.in.: ${esc(OBSZAR.miejscowosci.slice(1, 16).join(", "))}${OBSZAR.miejscowosci.length > 16 ? "…" : ""}` : "") : "Wpisz nazwę miejscowości i kliknij „Znajdź”."}</div>
    </div>
    <div class="pasek" style="margin:10px 0 0"><button data-ik="zapisz" onclick="zapiszObszar()">Zapisz obszar</button>
      <button class="tylko-admin" data-ik="przelacz" onclick="testBZP()">Test połączenia z BZP</button></div>`;
  rysujWoj();
}
let NOWE_CENTRUM = null, PODPOWIEDZI = [];
function rysujWoj() {
  const t = document.querySelector('input[name=ob]:checked')?.value;
  $("#ob-woj").classList.toggle("ukryj", t !== "wojewodztwa");
  $("#ob-prom").classList.toggle("ukryj", t !== "promien");
}
async function szukajMiasta() {
  const q = $("#ob-miasto").value.trim(); if (q.length < 2) return komunikat("Wpisz nazwę miejscowości.", true);
  $("#ob-podpowiedzi").innerHTML = '<span class="opis">Szukam…</span>';
  PODPOWIEDZI = await bezpiecznie(() => api("/api/obszar/szukaj?q=" + encodeURIComponent(q))) || [];
  $("#ob-podpowiedzi").innerHTML = PODPOWIEDZI.length ? PODPOWIEDZI.map((m, i) =>
    `<button type="button" class="maly" onclick="wybierzMiasto(${i})">${esc(m.opis)}</button>`).join("") : '<span class="opis">Nie znaleziono – sprawdź pisownię.</span>';
}
function wybierzMiasto(i) {
  NOWE_CENTRUM = PODPOWIEDZI[i];
  $("#ob-miasto").value = NOWE_CENTRUM.opis || NOWE_CENTRUM.nazwa;
  $("#ob-podpowiedzi").innerHTML = "";
  $("#ob-wybrana").innerHTML = `Wybrana: <b>${esc(NOWE_CENTRUM.opis)}</b> – kliknij „Zapisz obszar” albo „Szukaj teraz”.`;
}
function daneObszaru() {
  const tryb = document.querySelector('input[name=ob]:checked')?.value || "wojewodztwa";
  const ob = {tryb, wojewodztwa: [...document.querySelectorAll(".obw:checked")].map(c => c.value),
    promien: +(document.querySelector('input[name=obr]:checked')?.value || 10)};
  if (tryb === "promien") {
    if (NOWE_CENTRUM) ob.centrum = NOWE_CENTRUM;
    else if ($("#ob-miasto").value.trim()) ob.miejscowosc = $("#ob-miasto").value.trim();  // wpisana bez „Znajdź” – serwer rozpozna ją sam
    else { komunikat("Wpisz nazwę miejscowości.", true); return null; }
  }
  return ob;
}
async function zapiszObszar(cicho) {
  const ob = daneObszaru(); if (!ob) return null;
  const zap = await bezpiecznie(() => api("/api/obszar", {json: ob})); if (!zap) return null;
  if (!cicho) komunikat("Zapisano obszar: " + zap.opis);
  await ladujObszar();
  ladujPrzetargi();  // lista od razu pokazuje przetargi z nowego obszaru
  return zap;
}
async function testBZP() {
  const z = await bezpiecznie(() => api("/api/bzp/test", {json: {}}));
  sledz(z, w => komunikat(w.status === "ok" && w.wynik && w.wynik.liczba ? `BZP działa: ${w.wynik.liczba} ogłoszeń z ostatniego dnia.` :
    "BZP nie zwróciło ogłoszeń – szczegóły w okienku zadania (prawy dolny róg).", !(w.wynik && w.wynik.liczba)));
}
// ---------- nowe przetargi od ostatniej wizyty
function ustawLicznikNav(n) {
  const b = document.querySelector('#nav button[data-w="przetargi"] .etykieta'); if (!b) return;
  b.innerHTML = "Przetargi" + (n ? ` <span class="licznik-nowych">${n}</span>` : "");
}
async function przejrzaneWszystkie() {
  await bezpiecznie(() => api("/api/przetargi/widziane", {json: {wszystkie: true}}));
  PRZETARGI.forEach(t => t.nowy = false); if ($("#p-filtr").value === "nowe") $("#p-filtr").value = "aktywne"; rysujPrzetargi(); odswiezLicznikNowych();
}
let NOWE_INFO = null;
async function odswiezLicznikNowych(szukaj = false) {
  if (window.EDYCJA && window.EDYCJA !== "pelna") return null;  // edycja urzędu: bez przetargów wykonawcy (trasy nie istnieją)
  if (["gmina", "wspolnota", "inwestor", "dotacje", "nieruchomosci"].includes(JA.modul)) return null;  // konto bez modułu przetargów
  if (JA.uprawnienia && poziomU("przetargi") < 1) return null;  // rola bez Przetargów (np. kierownik budowy) – bez zapytania kończącego się błędem 403
  const d = await api("/api/przetargi/nowe?tryb=" + (STRONA || "") + (szukaj ? "" : "&szukaj=0")).catch(() => null); if (!d) return null;
  NOWE_INFO = d; ustawLicznikNav(d.liczba); rysujNowePulpit();
  return d;
}
function rysujNowePulpit() {
  const d = NOWE_INFO;
  // kafelek „Przetargi” na Pulpicie: podświetlenie i liczba nowych
  const kaf = document.querySelector('.kafel[onclick="pokaz(\'przetargi\')"]');
  if (kaf) { kaf.classList.toggle("ma-nowe", !!(d && d.liczba)); let b = kaf.querySelector(".kafel-nowe");
    if (d && d.liczba) { if (!b) { b = document.createElement("span"); b.className = "kafel-nowe"; kaf.appendChild(b); } b.textContent = odm(d.liczba, "nowy", "nowe", "nowych"); b.title = "Pokaż nowe przetargi"; b.onclick = e => { e.stopPropagation(); pokazNowe(); }; }
    else if (b) b.remove(); }
  // zakładka Przetargi: pasek z nowymi przetargami
  const el = $("#p-nowe"); if (!el || !d) return;
  if (!d.obszar_ustawiony) { el.innerHTML = `<div class="nowe-pulpit brak">${ik("szukaj")} Zapisz obszar wyszukiwania (panel powyżej) – program będzie codziennie pokazywał tu nowe przetargi z Twojej okolicy.</div>`; return; }
  const kiedy = d.od ? dataPl(d.od.slice(0, 10)) : "";
  el.innerHTML = `<div class="nowe-pulpit ${d.liczba ? "" : "zero"}"><div class="nowe-gora">${ik("szukaj")}
    <b>${d.liczba ? `${odm(d.liczba, "nowy przetarg", "nowe przetargi", "nowych przetargów")} w Twoim obszarze` : "Brak nowych przetargów w Twoim obszarze"}</b>
    <span class="opis" style="margin:0">od ostatniej wizyty${kiedy ? " (" + esc(kiedy) + ")" : ""}${SZUKANIE_TRWA ? " · <b>sprawdzam nowe ogłoszenia…</b>" : ""}</span>
    ${d.liczba ? `<button class="maly glowny" onclick="$('#p-filtr').value='nowe'; rysujPrzetargi()">Pokaż tylko nowe</button>
      <button class="maly" onclick="przejrzaneWszystkie()">Oznacz jako przejrzane</button>` : ""}</div></div>`;
}
let SZUKANIE_TRWA = false;
async function sprawdzNowePrzyStarcie() {
  const d = await odswiezLicznikNowych(true); if (!d || !d.zadanie) return;
  SZUKANIE_TRWA = true; rysujNowePulpit();
  const czekaj = async () => {
    const z = await api("/api/zadania/" + d.zadanie).catch(() => null);
    if (z && z.status === "trwa") return setTimeout(czekaj, 4000);
    SZUKANIE_TRWA = false; await odswiezLicznikNowych();
    if (WIDOK === "przetargi") ladujPrzetargi();
    if (NOWE_INFO && NOWE_INFO.liczba) komunikat(`Znaleziono nowe przetargi w Twoim obszarze: ${NOWE_INFO.liczba}.`);
  };
  setTimeout(czekaj, 4000);
}

// ---------- słowa kluczowe wyszukiwania: domyślne z Ustawień + własne
let SLOWA = null, SLOWA_DOM = [];
async function ladujSlowa() {
  const d = await api("/api/przetargi/slowa?tryb=" + (STRONA || "")).catch(() => null); if (!d) return;
  SLOWA_DOM = d.domyslne || [];
  try { SLOWA = JSON.parse(sessionStorage.getItem("slowa_" + (STRONA || "")) || "null"); } catch (e) { SLOWA = null; }
  if (!SLOWA) SLOWA = [...SLOWA_DOM];
  rysujSlowa();
}
function rysujSlowa() {
  const el = $("#slowa"); if (!el || !SLOWA) return;
  const dodane = SLOWA.filter(s => !SLOWA_DOM.includes(s)).length, usuniete = SLOWA_DOM.filter(s => !SLOWA.includes(s)).length;
  $("#slowa-licznik").textContent = `${SLOWA.length} słów${dodane ? ` · ${dodane} dodanych` : ""}${usuniete ? ` · ${usuniete} wyłączonych` : ""}`;
  el.innerHTML = `<p class="opis" style="margin:4px 0 8px">Program szuka ogłoszeń, których przedmiot lub treść zawiera któreś z tych słów (wystarczy początek słowa, np. „termomoderniz”).
      Domyślne słowa pochodzą z Ustawień; możesz dodać własne na to wyszukiwanie.</p>
    <div class="slowa">${SLOWA.map((s, i) => `<span class="slowo ${SLOWA_DOM.includes(s) ? "" : "nowe"}">${esc(s)}<button title="Usuń" onclick="SLOWA.splice(${i},1); zapamietajSlowa()">×</button></span>`).join("")}</div>
    <div class="pasek" style="margin-top:8px"><input id="slowo-nowe" placeholder="${STRONA === "dostawca" ? "Dodaj słowo lub frazę, np. sprzątanie, dostawa mebli, catering" : "Dodaj słowo lub frazę, np. elewacja, kanalizacja, dach"}" style="flex:1;min-width:240px"
        onkeydown="if (event.key === 'Enter') dodajSlowo()"><button class="maly zielony" data-ik="plus" onclick="dodajSlowo()">Dodaj</button>
      <button class="maly" data-ik="cofnij" onclick="SLOWA=[...SLOWA_DOM]; zapamietajSlowa()">Przywróć domyślne</button>
      <button class="maly" data-ik="zapisz" onclick="zapiszSlowaDomyslne()">Zapisz jako domyślne</button></div>`;
}
function zapamietajSlowa() { try { sessionStorage.setItem("slowa_" + (STRONA || ""), JSON.stringify(SLOWA)); } catch (e) {} rysujSlowa(); }
function dodajSlowo() {
  const nowe = $("#slowo-nowe").value.split(/[,;\n]/).map(s => s.trim()).filter(s => s.length >= 3 && !SLOWA.map(x => x.toLowerCase()).includes(s.toLowerCase()));
  if (!nowe.length) return komunikat("Wpisz słowo (min. 3 znaki), którego nie ma jeszcze na liście.", true);
  SLOWA.push(...nowe); zapamietajSlowa(); $("#slowo-nowe").focus();
}
async function zapiszSlowaDomyslne() {
  if (!confirm("Zapisać tę listę jako domyślne słowa kluczowe Twojego konta?")) return;
  const w = await bezpiecznie(() => api("/api/przetargi/slowa", {json: {slowa: SLOWA, tryb: STRONA}})); if (w) { SLOWA_DOM = w.domyslne; komunikat("Zapisano domyślne słowa kluczowe."); rysujSlowa(); }
}
function poWyszukaniu() {  // po wyszukaniu panel zwija się do paska, wyniki od razu widoczne
  P_FILTR_PO = "ostatnie"; WY.filtr = ""; WY.zwiniety = true; zapamietajZwiniecie();
  ladujPrzetargi().then(() => ladujWyszukiwarke(true));
}

// ---------- WYSZUKIWARKA: 1) czego szukasz  2) gdzie  3) u kogo  →  Szukaj; wyniki z filtrami-licznikami
let WY = null;
const TABELA = () => document.body.classList.contains("lista-tabela");
const INST = [["urzedy", "Urzędy"], ["szpitale", "Szpitale"], ["uczelnie", "Uczelnie"], ["spolki", "Duże spółki"], ["wspolnoty", "Wspólnoty i spółdzielnie"]];
const INST_TYP = {urzedy: "jst", szpitale: "szpital", uczelnie: "uczelnia", spolki: "spolka", wspolnoty: "wspolnota"};
const FILTRY_WYN = [["jst", "Urzędy"], ["szpital", "Szpitale"], ["uczelnia", "Uczelnie"], ["spolka", "Spółki"], ["wspolnota", "Wspólnoty"], ["inny", "Inni"]];
const ZESTAWY = {
  wykonawca: {"Termomodernizacja": ["termomodernizac", "docieplen", "elewac", "stolark"], "Drogi": ["drog", "chodnik", "nawierzchni", "parking"],
    "Instalacje": ["instalac", "wentylac", "elektryczn", "fotowolta", "pomp ciepła"], "Dachy": ["dach", "pokryci dachow"], "Remonty": ["remont", "modernizac", "przebudow", "adaptac"],
    "Woda i kanalizacja": ["kanalizac", "wodociąg", "oczyszczal"], "Budowa": ["budow", "rozbudow", "wykonanie robót"],
    "Ochrona ludności (schrony)": ["schron", "ukryci", "doraźnego schronienia", "obiektów zbiorowej ochrony", "ochrony ludności"]},
  dostawca: {"Sprzątanie": ["sprzątan", "utrzymani czystości", "mycie okien"], "Paliwa": ["paliw", "olej napędow", "olej opałow", "gaz płynn"],
    "Środki czystości": ["środków czystości", "artykułów higienicznych", "chemii gospodarczej"], "Sprzęt IT": ["komputer", "laptop", "drukark", "oprogramowani"],
    "Transport": ["usługi transportow", "przewóz", "dowóz"], "Żywność": ["żywnoś", "artykułów spożywcz", "catering", "wyżywieni"], "Odpady": ["odbiór odpadów", "wywóz", "odpadów komunalnych"],
    "Meble i wyposażenie": ["mebl", "wyposażeni"], "Ochrona i serwis": ["ochron", "konserwac", "serwis"],
    "Ochrona osób i mienia": ["ochrony osób", "ochrona mienia", "ochrony obiektu", "monitoring"], "Catering i żywienie zbiorowe": ["catering", "przygotowanie posiłków", "żywieni", "wyżywieni"],
    "Dowóz uczniów i przewozy": ["dowóz uczniów", "dowozu dzieci", "przewóz osób", "przewozu uczniów"], "Komunikacja zastępcza (PKP)": ["komunikacji zastępczej", "zastępcza komunikacja", "autobusowej komunikacji"],
    "Utrzymanie zieleni": ["utrzymanie zieleni", "pielęgnacj", "koszeni", "nasadzeń"], "Zimowe utrzymanie dróg": ["zimowe utrzymanie", "odśnieżani", "zimowego utrzymania"],
    "Leki": ["leków", "produktów leczniczych", "farmaceut"], "Sprzęt i wyroby medyczne": ["sprzętu medycznego", "wyrobów medycznych", "aparatury medycznej", "jednorazow"],
    "Odczynniki i diagnostyka": ["odczynnik", "diagnostyk", "testów", "laboratoryjn"], "Opatrunki i materiały medyczne": ["opatrunk", "materiałów medycznych", "rękawic"],
    "Ochrona ludności (wyposażenie)": ["agregat", "syren", "obrony cywilnej", "ochrony ludności", "magazyn", "zasilania awaryjnego"]}};
// kody CPV branż dostawcy (początek kodu) – precyzyjnie wskazują rodzaj zamówienia, niezależnie od słów w tytule
const CPV_ZESTAWOW = {"Sprzątanie": ["9091"], "Paliwa": ["0910", "0913", "0912"], "Środki czystości": ["3983", "3376"], "Sprzęt IT": ["302", "4800"],
  "Transport": ["601"], "Żywność": ["15", "5552", "5532"], "Odpady": ["905"], "Meble i wyposażenie": ["391"], "Ochrona i serwis": ["7971", "507", "5075"],
  "Ochrona osób i mienia": ["7971"], "Catering i żywienie zbiorowe": ["5552", "5532", "5551"], "Dowóz uczniów i przewozy": ["6013", "6011", "6014"],
  "Komunikacja zastępcza (PKP)": ["6017", "6014"], "Utrzymanie zieleni": ["7731", "7734"], "Zimowe utrzymanie dróg": ["9062", "9063"],
  "Leki": ["336"], "Sprzęt i wyroby medyczne": ["331", "3319"], "Odczynniki i diagnostyka": ["33696", "3312"], "Opatrunki i materiały medyczne": ["3314"],
  "Ochrona ludności (wyposażenie)": ["31121"]};
function bezPowtorzen(L) {  // „robot budowlan” i „roboty budowlane” to to samo – zostaje krótsze (szersze); kolejność bez zmian
  const s = [...new Set(L.map(x => String(x).trim().toLowerCase()).filter(Boolean))];
  const zawiera = (krot, dl) => { const a = krot.split(/\s+/), b = dl.split(/\s+/); return a.length === b.length && a.every((w, i) => b[i].startsWith(w)); };
  return s.filter(x => !s.some(k => k !== x && k.length <= x.length && zawiera(k, x)));
}
function zapamietajZwiniecie() { try { localStorage.setItem("wy_zwiniety", WY.zwiniety ? "1" : "0"); } catch (e) {} }
async function ladujWyszukiwarke(odswiezTylkoGore) {
  const d = await api("/api/wyszukiwarka?tryb=" + (STRONA === "dostawca" ? "dostawca" : "wykonawca")).catch(() => null); if (!d) return;
  let zw = false; try { zw = localStorage.getItem("wy_zwiniety") === "1"; } catch (e) {}
  if (!odswiezTylkoGore || !WY) WY = {slowa: bezPowtorzen(d.slowa || []), cpv: [...(d.cpv || [])], obszar: {...d.obszar, centrum: null}, inst: [...(d.instytucje || [])], powiadamiaj: d.powiadamiaj,
    wojewodztwa: d.wojewodztwa, promienie: d.promienie, tylkoNowe: false, sort: WY ? WY.sort : "ocena", filtr: "", zwiniety: zw && !!(d.ostatnie || {}).data && !!(d.ostatnie || {}).aktualne,
    wszystkieSlowa: false, zestawy: false};
  WY.instSzukane = d.instytucje || []; WY.ostatnie = d.ostatnie; WY.opisObszaru = d.obszar.opis; WY.pobranie = d.pobranie || "";
  rysujWyszukiwarke();
  if (odswiezTylkoGore && WIDOK === "przetargi") rysujPrzetargi();
}
function opisWyszukania() {
  const sl = WY.slowa.slice(0, 3).join(", ") + (WY.slowa.length > 3 ? ` +${WY.slowa.length - 3}` : "");
  const gdzie = WY.opisObszaru || "";
  const kto = (WY.instSzukane || []).filter(k => INST_TYP[k]).map(k => INST.find(x => x[0] === k)[1].toLowerCase()).join(", ") || "wszyscy";
  return `${esc(sl || "brak słów")} · ${esc(gdzie)} · ${esc(kto)}`;
}
function rysujWyszukiwarke() {
  try { rysujWyszukiwarkeW(); }
  catch (e) { console.error(e); const el = $("#wysz"); if (el) el.innerHTML = `<div class="ramka-uwaga">Błąd wyszukiwarki (${esc(e.message)}) – odśwież stronę (Ctrl+F5).</div>`; }
}
function rysujWyszukiwarkeW() {
  const el = $("#wysz"); if (!el || !WY) return;
  WY.instSzukane = WY.instSzukane || []; WY.inst = (WY.inst || []).filter(k => INST_TYP[k]); WY.slowa = WY.slowa || [];
  let zest = ZESTAWY[STRONA === "dostawca" ? "dostawca" : "wykonawca"], o = WY.obszar;
  if (STRONA === "dostawca" && CEL === "uslugi") {  // cel „Usługi pracochłonne” – tylko zestawy tych usług, widoczne od razu
    zest = Object.fromEntries(Object.entries(zest).filter(([k]) => ZESTAWY_PRACOCHLONNE.includes(k)));
    if (!WY.slowa.length) WY.zestawy = true;
  }
  if (WY.zwiniety) {
    el.innerHTML = `<div class="wy-pasek"><span class="wy-pasek-ik">${ik("szukaj")}</span><span class="wy-pasek-opis">${opisWyszukania()}</span>
      <button class="maly" onclick="WY.zwiniety = false; zapamietajZwiniecie(); rysujWyszukiwarke()">Zmień</button>
      <button class="maly wy-pom" onclick="szukajWy()">Szukaj ponownie</button></div>`;
    wstawIkony(el); return;
  }
  const chip = (t, akt, on, x) => `<button class="wy-chip ${akt ? "akt" : ""}" onclick="${on}">${esc(t)}${x ? " ×" : ""}</button>`;
  const LIMIT = 6, pokaz = WY.wszystkieSlowa ? WY.slowa : WY.slowa.slice(0, LIMIT);
  el.innerHTML = `<div class="wy-karta">
    <div class="wy-gora"><b>Szukaj przetargów</b>${(WY.ostatnie || {}).data ? `<button class="maly" onclick="WY.zwiniety = true; zapamietajZwiniecie(); rysujWyszukiwarke()" title="Zwiń">Zwiń ▲</button>` : ""}</div>
    <div class="wy-siatka">
      <div class="wy-pole"><label class="wy-et"><span class="wy-nr">1</span> Czego szukasz?</label>
        <div class="wy-wiersz"><input id="wy-slowo" placeholder="${STRONA === "dostawca" ? "np. sprzątanie, paliwo" : "np. termomodernizacja, dach"}"
          onfocus="if (!WY.zestawy) { WY.zestawy = true; rysujWyszukiwarke(); $('#wy-slowo').focus(); }" onkeydown="if (event.key === 'Enter') dodajSlowoWy()"><button onclick="dodajSlowoWy()" aria-label="Dodaj">+</button></div>
        <div class="wy-chipy">${pokaz.map(s => chip(s, true, `WY.slowa.splice(WY.slowa.indexOf('${escA(s)}'),1); rysujWyszukiwarke()`, true)).join("")}
          ${WY.slowa.length > LIMIT ? `<button class="wy-wiecej" onclick="WY.wszystkieSlowa = !WY.wszystkieSlowa; rysujWyszukiwarke()">${WY.wszystkieSlowa ? "pokaż mniej" : "+" + (WY.slowa.length - LIMIT) + " więcej"}</button>` : ""}
          ${!WY.slowa.length ? `<span class="opis">${STRONA === "dostawca" ? "Wybierz branżę (gotowe zestawy poniżej) albo wpisz, co dostarczasz." : "Wpisz słowo albo wybierz gotowy zestaw."}</span>` : ""}
          ${STRONA === "dostawca" && (WY.cpv || []).length ? `<span class="wy-cpv" title="Kody CPV: ${esc(WY.cpv.join(", "))}">+ kody CPV branży (${WY.cpv.length}) <a href="#" onclick="WY.cpv = []; rysujWyszukiwarke(); return false">×</a></span>` : ""}</div>
        ${WY.zestawy || !WY.slowa.length || (STRONA === "dostawca" && !(WY.cpv || []).length) ? `<div class="wy-zestawy">${Object.keys(zest).map(z => `<button class="wy-zestaw" onclick="zestawWy('${z}')">+ ${esc(z)}</button>`).join("")}
          ${WY.slowa.length ? `<button class="wy-zestaw wy-wyczysc" onclick="WY.slowa = []; rysujWyszukiwarke()">wyczyść słowa</button>` : ""}</div>`
          : `<button class="wy-wiecej" onclick="WY.zestawy = true; rysujWyszukiwarke()">gotowe zestawy ▾</button>`}</div>
      <div class="wy-pole"><label class="wy-et"><span class="wy-nr">2</span> Gdzie?</label>
        <div class="wy-tryby">${[["promien", "Okolica"], ["wojewodztwa", "Województwa"], ["polska", "Cała Polska"]].map(([k, n]) =>
          `<button class="${o.tryb === k ? "akt" : ""}" onclick="WY.obszar.tryb = '${k}'; rysujWyszukiwarke()">${n}</button>`).join("")}</div>
        ${o.tryb === "promien" ? `<div class="wy-wiersz"><input id="wy-miejsc" list="wy-podp" autocomplete="off" value="${esc(o.wpisane != null ? o.wpisane : o.centrum ? (o.centrum.opis || o.centrum.nazwa) : o.miejscowosc || "")}" placeholder="Miejscowość, np. Świdnica" oninput="WY.obszar.wpisane = this.value; WY.obszar.centrum = null; wybierzMiejscWy(this.value); podpowiedziWy(this.value)" onchange="wybierzMiejscWy(this.value)" onkeydown="if (event.key === 'Enter') szukajWy()">
            <datalist id="wy-podp"></datalist>
            <select id="wy-km" onchange="WY.obszar.promien = +this.value">${WY.promienie.map(k => `<option value="${k}" ${+k === +o.promien ? "selected" : ""}>${k} km</option>`).join("")}</select></div>`
          : o.tryb === "wojewodztwa" ? `<div class="wy-chipy">${WY.wojewodztwa.map(w => chip(w, o.wojewodztwa.includes(w), `przelaczWojWy('${w}')`)).join("")}</div>`
          : '<p class="opis" style="margin:4px 0 0">Cała Polska – wyników może być bardzo dużo; zawęź słowa.</p>'}</div>
    </div>
    <div class="wy-dol"><span class="wy-et"><span class="wy-nr">3</span> U kogo?</span>
      ${chip("Wszyscy", !WY.inst.length, "WY.inst = []; rysujWyszukiwarke()")}${INST.map(([k, n]) => chip(n, WY.inst.includes(k), `przelaczInstWy('${k}')`)).join("")}
      <span class="wy-dol-prawo"><label class="wy-powiad"><input type="checkbox" ${WY.powiadamiaj ? "checked" : ""} onchange="WY.powiadamiaj = this.checked"> powiadamiaj codziennie</label>
        <button class="wy-szukaj" onclick="szukajWy()">${ik("szukaj")} Szukaj</button></span></div>
  </div>`;
  wstawIkony(el);
}
function dodajSlowoWy() {
  const e = $("#wy-slowo"), nowe = (e.value || "").split(/[,;]/).map(s => s.trim().replace(/\s+/g, " ").toLowerCase()).filter(Boolean);
  const zle = nowe.filter(s => s.length < 3 || s.length > 60);  // jak na serwerze (karta W1: słowo 3–60 znaków)
  if (zle.length) komunikat("Słowo kluczowe musi mieć 3–60 znaków – pominięto: " + zle.map(s => `„${s.length > 30 ? s.slice(0, 30) + "…" : s}” (${s.length} zn.)`).join(", "), true);
  WY.slowa = bezPowtorzen(WY.slowa.concat(nowe.filter(s => s.length >= 3 && s.length <= 60)));
  rysujWyszukiwarke(); setTimeout(() => $("#wy-slowo") && $("#wy-slowo").focus(), 0);
}
function zestawWy(z) {
  WY.slowa = bezPowtorzen(WY.slowa.concat(ZESTAWY[STRONA === "dostawca" ? "dostawca" : "wykonawca"][z] || []));
  if (STRONA === "dostawca") { WY.cpv = [...new Set((WY.cpv || []).concat(CPV_ZESTAWOW[z] || []))]; WY.branze = [...new Set((WY.branze || []).concat([z]))]; }
  rysujWyszukiwarke();
}
function przelaczWojWy(w) { const L = WY.obszar.wojewodztwa; L.includes(w) ? L.splice(L.indexOf(w), 1) : L.push(w); rysujWyszukiwarke(); }
function przelaczInstWy(k) { WY.inst.includes(k) ? WY.inst.splice(WY.inst.indexOf(k), 1) : WY.inst.push(k); rysujWyszukiwarke(); }  // ustawienie – działa po „Szukaj”
let WY_PODP = [], WY_PODP_T = null;
function podpowiedziWy(q) {
  clearTimeout(WY_PODP_T); if ((q || "").length < 2) return;
  WY_PODP_T = setTimeout(async () => {
    WY_PODP = await api("/api/obszar/szukaj?q=" + encodeURIComponent(q)).catch(() => []) || [];
    if (!Array.isArray(WY_PODP)) WY_PODP = [];
    const dl = $("#wy-podp"); if (dl) dl.innerHTML = WY_PODP.map(p => `<option value="${esc(p.opis || p.nazwa)}"></option>`).join("");  // pełny opis – odróżnia np. dwie Świdnice
    const e = $("#wy-miejsc"); if (e) wybierzMiejscWy(e.value);
  }, 350);
}
function wybierzMiejscWy(v) {  // wybór z podpowiedzi (pełny opis); sama nazwa wpisana z klawiatury – rozpozna ją serwer przy „Szukaj”
  const p = WY_PODP.find(x => (x.opis || x.nazwa) === v); if (p) WY.obszar.centrum = p;
}
async function szukajWy() {
  if (!WY.slowa.length) { const e = $("#wy-slowo"); if (e && e.value.trim()) dodajSlowoWy(); }
  if (!WY.slowa.length && !(WY.cpv || []).length) return komunikat("Krok 1: wpisz, czego szukasz (albo wybierz gotowy zestaw).", true);
  const o = WY.obszar;
  if (o.tryb === "wojewodztwa" && !o.wojewodztwa.length) return komunikat("Krok 2: zaznacz co najmniej jedno województwo.", true);
  if (o.tryb === "promien") {
    const e = $("#wy-miejsc"); if (e) { o.wpisane = e.value; wybierzMiejscWy(e.value); }
    const km = $("#wy-km"); if (km) o.promien = +km.value;
    if (!o.centrum && !(o.wpisane || "").trim() && !o.miejscowosc) return komunikat("Krok 2: wpisz miejscowość, wokół której szukać.", true);
  }
  komunikat("Zapisuję obszar…");
  // miejscowość: wybrana z podpowiedzi (centrum) albo sam wpisany tekst – serwer rozpozna ją w wykazie miejscowości
  const ob = await bezpiecznie(() => api("/api/obszar", {json: {tryb: o.tryb, wojewodztwa: o.wojewodztwa, promien: o.promien, centrum: o.centrum || undefined,
    miejscowosc: o.centrum ? undefined : (o.wpisane != null ? o.wpisane.trim() : undefined)}})); if (!ob) return;
  o.centrum = null; o.wpisane = null;
  if (ob.miejscowosc != null) { o.miejscowosc = ob.miejscowosc_opis || ob.miejscowosc; if (ob.promien) o.promien = ob.promien; }
  WY.opisObszaru = ob.opis; rysujWyszukiwarke();
  const z = await bezpiecznie(() => api("/api/wyszukiwarka", {json: {tryb: STRONA === "dostawca" ? "dostawca" : "wykonawca", slowa: WY.slowa, cpv: WY.cpv || [], instytucje: WY.inst, powiadamiaj: WY.powiadamiaj}}));
  if (z) { komunikat("Szukam: " + ob.opis); sledz(z, poWyszukaniu); }
}
function rysujKarty(l) {
  const ost = (OSTATNIE || {}), f = $("#p-filtr").value, s = WY ? WY.sort : "ocena";
  const typ = t => FILTRY_WYN.some(x => x[0] === t.typ_zam) ? t.typ_zam : "inny";
  const licz = {}; l.forEach(t => { licz[typ(t)] = (licz[typ(t)] || 0) + 1; });
  const nowych = l.filter(t => t.nowy).length;
  // „U kogo?” z wyszukiwania ustawia filtr wyników – ale nigdy nie chowa wszystkiego: gdy u wybranych nic nie ma, widać wszystkie wyniki z informacją
  const wybr = new Set(((WY && WY.instSzukane) || []).map(k => INST_TYP[k]).filter(Boolean));
  const ileWybr = l.filter(t => wybr.has(typ(t))).length;
  let info = "";
  if (WY && f === "ostatnie" && WY._filtrDla !== ost.data) {
    WY._filtrDla = ost.data;
    WY.filtr = wybr.size && ileWybr ? (wybr.size === 1 ? [...wybr][0] : "wybrani") : "";
    if (wybr.size && !ileWybr) WY._brakWybr = true; else WY._brakWybr = false;
  }
  if (WY && WY._brakWybr && f === "ostatnie" && !WY.filtr) info = `<div class="ramka-uwaga">U wybranych zamawiających (${[...wybr].map(k => (FILTRY_WYN.find(x => x[0] === k) || [k, k])[1].toLowerCase()).join(", ")}) nic nie znaleziono – pokazuję wszystkie wyniki wyszukiwania.</div>`;
  if (WY && WY.filtr && !["nowe", "wybrani"].includes(WY.filtr) && !licz[WY.filtr]) WY.filtr = "";
  let w = l.filter(t => !WY || !WY.filtr || (WY.filtr === "nowe" ? t.nowy : WY.filtr === "wybrani" ? wybr.has(typ(t)) : typ(t) === WY.filtr));
  w = [...w].sort((a, b) => s === "termin" ? String(a.termin_ofert || "9").localeCompare(String(b.termin_ofert || "9")) : (+b.ocena || -1) - (+a.ocena || -1));
  const fch = (k, n, ile) => `<button class="wy-filtr ${(WY && WY.filtr) === k ? "akt" : ""}" ${ile ? "" : "disabled"} onclick="WY.filtr = '${k}'; rysujPrzetargi()">${n} <b>${ile}</b></button>`;
  const tyt = f === "ostatnie" && ost.data ? `Wyniki wyszukiwania <small class="opis">(${esc(ost.data)}${WY && WY.pobranie ? " · ogłoszenia pobrane " + esc(WY.pobranie) : ""})</small>`
    : f === "nowe" ? `Nowe przetargi od ostatniej wizyty · <a href="#" onclick="$('#p-filtr').value='ostatnie'; rysujPrzetargi(); return false">wyniki wyszukiwania</a>`
    : OSTATNIE && OSTATNIE.data && !OSTATNIE.aktualne ? "Aktywne przetargi z Twojego obszaru – obszar zmienił się od ostatniego wyszukiwania, kliknij <b>Szukaj</b>, żeby zobaczyć nowe wyniki"
    : "Aktywne przetargi – kliknij <b>Szukaj</b>, żeby zobaczyć wyniki według ustawień";
  $("#p-wyniki-gora").innerHTML = `<div class="wy-wyniki-gora"><span class="wy-tyt">${tyt}</span><span class="zakres-admin-miejsce"></span>
      <select class="wy-sort" onchange="WY.sort = this.value; rysujPrzetargi()"><option value="ocena" ${s === "ocena" ? "selected" : ""}>najlepiej dopasowane</option><option value="termin" ${s === "termin" ? "selected" : ""}>najbliższy termin</option></select></div>
    <div class="wy-filtry">${fch("", "Wszystkie", l.length)}${wybr.size > 1 && ileWybr ? fch("wybrani", "Wybrani zamawiający", ileWybr) : ""}${FILTRY_WYN.filter(([k]) => licz[k]).map(([k, n]) => fch(k, n, licz[k] || 0)).join("")}${fch("nowe", "Nowe", nowych)}</div>`;
  wstawZakresAdmina();
  const pusto = !l.length
    ? (f === "ostatnie" ? `Nic nie znaleziono${WY && (WY.instSzukane || []).filter(k => INST_TYP[k]).length ? " u wybranych zamawiających (" + WY.instSzukane.filter(k => INST_TYP[k]).map(k => INST.find(x => x[0] === k)[1].toLowerCase()).join(", ") + ")" : ""}. Dodaj słowa, poszerz obszar albo wybierz „Wszyscy” w kroku 3 i kliknij Szukaj ponownie.` : "Brak aktywnych przetargów.")
    : "Brak przetargów w tej grupie.";
  $("#p-karty").innerHTML = info + (w.length ? w.slice(0, 300).map(t => `<div class="wy-wynik ${P_AKT === t.numer ? "akt" : ""}" onclick="szczegolyP('${escA(t.numer)}', '${escA(t.konto || "")}')">
      <div class="wy-wynik-gora"><b>${esc(t.przedmiot || "")}</b>${t.ocena != null && t.ocena !== "" ? `<span class="wy-ocena o${Math.round(+t.ocena / 3.4)}">${esc(t.ocena)}/10</span>` : ""}</div>
      <div class="wy-wynik-dol">${esc(t.zamawiajacy || "")}${t.lokalizacja ? " · " + esc(t.lokalizacja) : ""} · termin ${esc(dataPl(t.termin_ofert) || "–")}
        ${t.nowy ? '<span class="znacznik-nowy">NOWY</span>' : ""}${t.status && t.status !== "nowy" ? ` <span class="znacznik z-${esc(t.status).replace(" ", "-")}">${esc(t.status)}</span>` : ""}
        ${t.projekt ? ' <span class="znacznik z-startujemy">w projekcie</span>' : ""}${!t.rodzaj_zam ? ' <span class="znacznik z-odpuszczamy" title="Ogłoszenie nie podaje rodzaju zamówienia">rodzaj nieustalony</span>' : ""}${znacznikSita(t)}${znacznikKont(t)}</div></div>`).join("")
    : `<div class="ramka-uwaga">${pusto}</div>`);
}
// wstępne sito bez AI: ogłoszenie zostało w wynikach, ale nie trafiło do automatycznej oceny (słowo tylko w treści ogłoszenia)
function znacznikSita(t) {
  if (!t || !(t.sito || {}).slabe || (t.ocena != null && t.ocena !== "")) return "";
  return ` <span class="znacznik z-odpuszczamy" title="${esc("Wstępne sito bez AI: " + (t.sito.opis || "") + ". Otwórz, aby ocenić przez AI.")}">słabe dopasowanie – bez oceny AI</span>`;
}
// przetarg bez oceny otwarty w szczegółach: program sam zleca jego ocenę (raz), zamiast przycisku „Oceń przez AI”
const OCENA_ZLECONA = new Set();
function autoOcena(t) {
  if (!t || t.obcy) return false;
  if (OCENA_ZLECONA.has(t.numer)) return true;
  OCENA_ZLECONA.add(t.numer);
  api("/api/przetargi/ocen", {json: {numery: [t.numer]}}).then(z => sledz(z, () => { ladujPrzetargi(); if (P_AKT === t.numer) setTimeout(() => szczegolyP(t.numer), 300); }))
    .catch(() => { const e = $("#p-ocena-auto"); if (e) e.textContent = "Ten przetarg nie ma jeszcze oceny AI – zostanie oceniony przy najbliższym wyszukiwaniu."; });
  return true;
}
async function ocenAI(numery) {
  numery = numery || (P_WYBRANE.size ? [...P_WYBRANE] : null);
  const z = await bezpiecznie(() => api("/api/przetargi/ocen", {json: {numery}})); sledz(z, () => { ladujPrzetargi(); if (P_AKT) setTimeout(() => szczegolyP(P_AKT), 300); });
}
async function ustawStatus(numery, status) {
  let powod = "";
  if (status === "odpuszczamy" || status === "przegrany") {
    powod = prompt(status === "odpuszczamy" ? "Dlaczego odpuszczamy? (opcjonalnie – AI nauczy się na tej decyzji, np. „za daleko”, „za małe”, „brak referencji”)"
      : "Dlaczego przegraliśmy? (opcjonalnie, np. „cena wyższa o 8%”)", "");
    if (powod === null) return;
  }
  await bezpiecznie(() => api("/api/przetargi/status", {json: {numery, status, powod}})); komunikat("Zapisano status."); await ladujPrzetargi(); if (P_AKT) szczegolyP(P_AKT); }
async function usunP(numery) {
  if (!confirm(`Usunąć ${numery.length} przetarg(i)? Nie pojawią się ponownie przy wyszukiwaniu (przywrócisz je w Ustawieniach).`)) return;
  await bezpiecznie(() => api("/api/przetargi/usun", {json: {numery}})); P_AKT = null; $("#p-szczegoly").classList.add("ukryj"); ladujPrzetargi();
}
// administrator: przetarg z listy innego konta → kopia na mojej liście (opcjonalnie od razu oferta)
async function przejmijPrzetarg(nr, konto, oferta) {
  const z = await bezpiecznie(() => api("/api/przetargi/przejmij", {json: {numer: nr, konto}})); if (!z) return;
  await ladujPrzetargi();
  if (oferta) return ofertaZPrzetargu(nr);
  komunikat("Przetarg jest na Twojej liście – możesz go ocenić, zmienić status albo przygotować ofertę."); szczegolyP(nr);
}
// ten sam przetarg na listach innych kont / w innym źródle (BZP i TED) – jedna pozycja z informacją zamiast dubli
function znacznikKont(t) {
  const k = [...(t.obcy && t.konto ? [t.konto] : []), ...(t.inne_konta || [])];
  return (k.length ? ` <span class="znacznik" title="Ten przetarg mają też na liście te konta">${t.obcy ? "konto" : "też u"}: ${esc(k.join(", "))}</span>` : "")
    + ((t.duplikaty || []).length ? ` <span class="znacznik" title="To samo postępowanie opublikowano też pod numerem: ${esc(t.duplikaty.join(", "))}">też w ${(t.duplikaty || []).some(n => /^\d+-\d{4}$/.test(n)) ? "TED" : "BZP"}</span>` : "");
}
async function ofertaZPrzetargu(nr) {
  const ist = (PRZETARGI || []).find(t => t.numer === nr && t.projekt && !t.obcy);
  if (ist) { komunikat("Oferta dla tego przetargu już istnieje – otwieram ją (jedna oferta na postępowanie)."); return kartaProjektu(ist.projekt.id, ist.projekt.typ); }
  const tp = (PRZETARGI || []).find(t => t.numer === nr) || {};
  const rodzaj = STRONA === "dostawca" ? (["dostawy", "uslugi"].includes(tp.rodzaj_zam) ? tp.rodzaj_zam : "dostawy") : undefined;
  const p = await bezpiecznie(() => api("/api/projekty", {json: {przetarg: nr, rodzaj_zamowienia: rodzaj}}));
  if (p && p.istniejacy) { komunikat("Oferta dla tego przetargu już istnieje – otwieram ją (jedna oferta na postępowanie)."); TRYB = "przetarg"; PROJEKT_ID = p.id; return pokaz("projekty"); }
  if (p) { await ustawStatus([nr], "do analizy"); TRYB = "przetarg"; PROJEKT_ID = p.id; pokaz("projekty");
    if (p.dokumenty_skopiowane) komunikat(`Skopiowano ${p.dokumenty_skopiowane} dokumentów pobranych przy pełnej analizie.`);
    else sledz(await bezpiecznie(() => api(`/api/projekty/${p.id}/pobierz-dokumenty`, {json: {}})), odswiezProjekt); }
}

// ================================================================ PROJEKTY
let PROJEKT_ID = null, PROJEKT = null, HURTOWNIE = [], PRACOWNICY = [], UZYTKOWNICY = [];
const OPISY_TRYBU = {
  prawnik: {tytul: "Sprawy – sprawdzenie dokumentacji i opinie prawne", nowy: "Nowa sprawa",
    pusty: "Sprawa to jedno postępowanie: wgrywasz dokumentację, wybierasz przedmiot (roboty budowlane, usługi, dostawy), tryb i stronę (zamawiający, wykonawca, niezależna opinia). Program sprawdza dokumentację według listy kontrolnej prawnika, daje uwagi z podstawą prawną i propozycją brzmienia, raport uwag i opinię prawną w Wordzie.",
    pytanie: "Nazwa sprawy (np. „Gmina X – przebudowa drogi, opinia dla zamawiającego”):"},
  przetarg: {tytul: "Projekty z przetargów", nowy: "Nowy projekt", pusty: "Wybierz projekt z listy albo utwórz nowy. Projekt z przetargu utworzysz też przyciskiem „Przygotuj ofertę” w zakładce Przetargi.", pytanie: "Nazwa projektu (np. „Termomodernizacja – ul. Lelewela 22”):"},
  wlasny: {tytul: "Własne projekty", nowy: "Nowy własny projekt", pusty: "Własne projekty to zlecenia spoza przetargów: umowy z inwestorami prywatnymi, wspólnotami, firmami. Wrzucasz umowę i dokumenty, przygotowujesz ofertę i kosztorys, a po podpisaniu umowy przenosisz projekt do realizacji.", pytanie: "Nazwa własnego projektu (np. „Elewacja – dom jednorodzinny, Świebodzice”):"},
  kosztorys: {tytul: "Kosztorysowanie", nowy: "Nowy kosztorys", pusty: "Kosztorysowanie prac na podstawie dokumentów: przedmiaru, projektu, rysunków, opisu lub zdjęć. Jeśli nie ma przedmiaru, AI wyliczy ilości z dokumentów i pokaże obliczenia. Gotowy kosztorys możesz zamienić we własny projekt.", pytanie: "Nazwa kosztorysu (np. „Remont dachu – ul. Długa 5”):"},
};
Object.assign(OPISY_TRYBU, {
  wniosek_dot: {tytul: "Uzyskaj dotację – wnioski o dofinansowanie", nowy: "Nowy wniosek o dotację", pusty: "Wniosek o dofinansowanie krok po kroku: 1) dokumenty naboru (pobrane z wyszukiwarki dotacji albo wgrane); 2) wymagania naboru i opis projektu; 3) wypełnienie wniosku i załączników przez program albo wgranie własnych; 4) sprawdzenie i komplet do złożenia. Najwygodniej zacząć od „Wyszukaj dotację” i przycisku „Uzyskaj dotację” przy wybranym naborze.", pytanie: "Nazwa wniosku (np. „FEDS – pompa ciepła i PV dla zakładu w Świdnicy”):"},
  dotacja: {tytul: "Rozliczanie dotacji UE / KPO", nowy: "Nowe rozliczenie dotacji", pusty: "Rozliczenie dotacji krok po kroku: 1) wgraj dokumenty dotacji (umowa o dofinansowanie lub objęcie wsparciem, wniosek, regulamin naboru); 2) program wskaże, jakie dokumenty są potrzebne do rozliczenia etapu albo całości; 3) wgraj je albo poproś program o ich przygotowanie; 4) program sprawdzi poprawność i przygotuje komplet do złożenia.", pytanie: "Nazwa projektu dotacji (np. „KPO – termomodernizacja szkoły w Żarowie”):"},
  dom: {tytul: "Mój dom – projekt i kosztorys", nowy: "Nowa budowa domu", pusty: "Wgraj projekt swojego domu (PDF: projekt budowlany, rzuty, przekroje, opis techniczny, zestawienie powierzchni). Program przygotuje kosztorys budowy według etapów (stan zero, stan surowy, dach, instalacje, wykończenie) albo wczyta Twój własny kosztorys. Dalej: lista materiałów, harmonogram dostaw, zapytania i zamówienia do hurtowni, a po rozpoczęciu budowy – etapy, odbiory, wydatki i budżet.", pytanie: "Nazwa budowy (np. „Dom w Mokrzeszowie, dz. 123/4”):"},
  zamowienie: {tytul: "Projekty zamówień", nowy: "Nowy projekt zamówienia", pusty: "Jeden projekt zamówienia zawiera wszystko: dokumentację projektową, kosztorys inwestorski, sprawdzenie dokumentacji przetargowej, przygotowanie SWZ / zapytania i umowy – a po przetargu zarządzanie inwestycją. Wybierz projekt z listy albo utwórz nowy.", pytanie: "Nazwa zamówienia (np. „Termomodernizacja budynku szkoły”):"},
  inwestorski: {tytul: "Kosztorys prac (inwestorski)", nowy: "Nowy kosztorys", pusty: "Kosztorys inwestorski sporządzany zgodnie z załączonymi dokumentami: projektem, przedmiarem, opisem technicznym, rysunkami. Służy do ustalenia wartości zamówienia przed przetargiem. Gotowy kosztorys możesz dołączyć do dokumentacji przetargowej albo przekazać do zarządzania inwestycją.", pytanie: "Nazwa kosztorysu (np. „Termomodernizacja budynku przy ul. Długiej 5”):"},
  weryfikacja: {tytul: "Sprawdź dokumentację przetargową", nowy: "Nowe sprawdzenie", pusty: "Wrzuć dokumentację przetargową (SWZ lub zapytanie, OPZ, przedmiar, wzór umowy, formularze). AI wyszuka błędy, sprzeczności między dokumentami, braki i zapisy ryzykowne lub niezgodne z przepisami – i zaproponuje poprawki.", pytanie: "Nazwa postępowania do sprawdzenia:"},
  dokumentacja: {tytul: "Sporządź dokumentację przetargową", nowy: "Nowe postępowanie", pusty: "Przygotowanie dokumentów postępowania: SWZ albo zapytania ofertowego, opisu przedmiotu zamówienia, formularza ofertowego i wzoru umowy – zgodnie z Twoimi wymaganiami i na podstawie projektu, przedmiaru i kosztorysu inwestorskiego.", pytanie: "Nazwa zamówienia (np. „Remont dachu budynku szkoły”):"},
});
const pustyProjekt = () => `<p class="pusto">${esc(OPISY_TRYBU[TRYB].pusty)}</p>`;
async function ladujProjekty() {
  $("#pr-tytul").textContent = OPISY_TRYBU[TRYB].tytul;
  $("#pr-nowy .etykieta").textContent = OPISY_TRYBU[TRYB].nowy;
  await bezpiecznie(async () => {
    const dost = p => ["dostawy", "uslugi"].includes(p.rodzaj_zamowienia);
    const l = (await api("/api/projekty")).filter(p => (p.typ || "przetarg") === TRYB && (TRYB !== "przetarg" || STRONA !== "dostawca" || dost(p))
      && (STRONA !== "zamawiajacy" || !!p.wspolnota === MZ().prywatny));  // zamawiający publiczny i wspólnota – osobne dane
    if (STRONA === "dostawca" && TRYB === "przetarg") { $("#pr-tytul").textContent = "Oferty – dostawy i usługi"; $("#pr-nowy .etykieta").textContent = "Nowa oferta"; }
    if (PROJEKT_ID && !l.some(p => p.id === PROJEKT_ID)) { PROJEKT_ID = null; $("#projekt").innerHTML = pustyProjekt(); }
    if (!PROJEKT_ID) $("#projekt").innerHTML = pustyProjekt();
    $("#lista-projektow").innerHTML = l.map(p => `<li class="${p.id === PROJEKT_ID ? "akt" : ""}" onclick="otworzProjekt('${p.id}')">
      ${esc(p.nazwa)}${p.link ? ` <a class="link-przetargu" href="${esc(p.link)}" target="_blank" rel="noopener" title="Ogłoszenie przetargu" onclick="event.stopPropagation()">↗</a>` : ""}<small>${p.termin_ofert && !p.status_projektu ? "oferty do " + esc(dataPl(p.termin_ofert)) + " · " : ""}${esc(p.utworzono)}${p.brutto ? " · " + zl(p.brutto) : ""}${ADMIN() && p.wlasciciel && p.wlasciciel !== JA.login ? " · " + esc(p.wlasciciel) : ""}${p.status_projektu === "realizacja" ? " · w realizacji" : p.status_projektu === "zakonczony" ? " · zakończony" : ""}</small></li>`).join("") || '<li class="pusto">Brak pozycji</li>';
    filtrujProjekty();
    if (PROJEKT_ID) otworzProjekt(PROJEKT_ID);
  });
}
async function nowyProjekt() {
  if (TRYB === "zamowienie") { KZN = {rodzaj: "", sciezka: ""}; return pokaz("zam_nowe"); }  // zamówienie zawsze przez kreator
  const nazwa = prompt(OPISY_TRYBU[TRYB].pytanie); if (!nazwa) return;
  const p = await bezpiecznie(() => api("/api/projekty", {json: {nazwa, typ: TRYB, prywatny: STRONA === "zamawiajacy" && MZ().prywatny, rodzaj_zamowienia: STRONA === "dostawca" && TRYB === "przetarg"
    ? (confirm("Czy to zamówienie na USŁUGI? (OK = usługi, Anuluj = dostawy)") ? "uslugi" : "dostawy") : undefined}})); if (p) { PROJEKT_ID = p.id; ladujProjekty(); }
}
async function otworzProjekt(id) {
  const inny = PROJEKT_ID !== id || !PROJEKT || PROJEKT.id !== id;
  PROJEKT_ID = id;
  zapiszHistorie(WIDOK);  // Wstecz z otwartego projektu wraca do listy
  document.querySelectorAll("#lista-projektow li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  // hurtownie i pracownicy – dane wykonawcy (harmonogram, zamówienia materiałów): w edycji urzędu tych tras nie ma, a ich brak
  // nie może blokować otwarcia projektu – pobierane pomocniczo, błąd = pusta lista
  // konto ograniczone do modułu zamawiającego (gmina, wspólnota) – adresy wykonawcy zablokowane (403), więc bez zapytań
  const pomocn = u => (window.EDYCJA && window.EDYCJA !== "pelna") || ["gmina", "wspolnota"].includes((typeof JA !== "undefined" && JA && JA.modul) || "") ? Promise.resolve(null) : api(u).catch(() => null);
  const [p, h, pr, uz] = await Promise.all([api("/api/projekty/" + id), pomocn("/api/hurtownie"), pomocn("/api/pracownicy"),
    ADMIN() ? api("/api/uzytkownicy").catch(() => null) : Promise.resolve(null)]).catch(e => { komunikat(e.message, true); return []; });
  if (!p) return;
  PROJEKT = p; HURTOWNIE = h || []; PRACOWNICY = (pr && pr.pracownicy) || []; UZYTKOWNICY = uz || []; rysujProjekt();
  if (inny) $("#projekt").scrollTop = 0;
}
const plik = n => `<a href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(n)}">${esc(n)}</a>`;
// ---------- rozbieżności przedmiaru: pozycje spoza przedmiaru i decyzja wykonawcy (w cenie / pytanie / na etap umowy / nie dotyczy)
function panelRozbieznosci(p, zam) {
  const R = p.rozbieznosci_dane || {}, L = R.lista || [], V = R.warianty || []; if (!L.length && !V.length) return "";
  if (zam && p.rodzaj_zamowienia && p.rodzaj_zamowienia !== "roboty") return "";
  const D = R.decyzje || {}, tp = R.termin_pytan, wyn = {ryczalt: "ryczałtowe", kosztorysowe: "kosztorysowe"}[R.wynagrodzenie];
  const pod = {pytanie: "zapytaj zamawiającego; do czasu odpowiedzi pozycja zostaje w cenie", umowa: "pozycje spoza przedmiaru można zostawić na etap umowy (rozliczenie obmiarem)", cena: ""}[R.podpowiedz] || "";
  const strona = (v, k) => `<b>${k === "a" ? "A" : "B"}</b> · ${esc(v[k].zrodlo || (k === "a" ? "przedmiar" : "dokumentacja"))}<br>${esc(v[k].opis)}<br><b>${zl(v[k].cena)}</b>/${esc(v.jm || "j.m.")}`;
  const tabWar = !V.length ? "" : `<h3 style="margin-top:12px">Różne rozwiązania w dokumentach – ${V.length} poz.</h3>
    <p class="opis">${zam ? `Dokumenty podają dla tej samej pozycji przedmiaru dwa rozwiązania. Wybierz obowiązujące – według niego liczona jest wartość –
      i <b>ujednolić dokumenty przed ogłoszeniem</b>. Bez Twojej decyzji program przyjmuje wariant z dokumentu nadrzędnego, a gdy dokumenty tego nie rozstrzygają – droższy.`
      : `Dokumenty podają dla tej samej pozycji przedmiaru dwa rozwiązania. Wybierz, które jest w cenie oferty. Bez Twojej decyzji program przyjmuje
      wariant z dokumentu nadrzędnego, a gdy dokumenty tego nie rozstrzygają – droższy.`}</p>
    <div class="tabela-okno"><table class="tabela"><tr><th style="min-width:210px">Pozycja</th><th>Wariant A (przedmiar)</th><th>Wariant B</th><th>Różnica B − A</th><th>${zam ? "Obowiązuje" : "W cenie"}</th></tr>
      ${V.map(v => `<tr><td><b>${esc(v.lp)}</b> ${esc(v.opis)}${v.znaleziono ? `<br><small class="opis">${String(v.ilosc).replace(".", ",")} ${esc(v.jm)}</small>` : '<br><small class="czerwone">nie znaleziono pozycji w kosztorysie – popraw cenę ręcznie</small>'}
          ${v.cena_pozycji_reczna ? '<br><small class="czerwone">cena pozycji poprawiona ręcznie – wybierz wariant, żeby ją zastąpić</small>' : ""}
          ${v.kiedy ? `<br><small class="opis">decyzja: ${esc(v.kiedy)}${v.kto ? ", " + esc(v.kto) : ""}</small>` : '<br><small class="opis">przyjęte przez program' + (v.nadrzedny ? " (dokument nadrzędny)" : " (droższy wariant)") + "</small>"}</td>
        <td>${strona(v, "a")}</td><td>${strona(v, "b")}</td><td>${zl(v.roznica)}</td>
        <td><select style="max-width:170px" onchange="ustawWariant('${v.id}', this.value, ${v.pytanie ? "true" : "false"})"><option value="a" ${v.wybrany === "a" ? "selected" : ""}>Wariant A</option><option value="b" ${v.wybrany === "b" ? "selected" : ""}>Wariant B</option></select>
          ${zam ? "" : `<br><label class="opis" style="margin:4px 0 0"><input type="checkbox" ${v.pytanie ? "checked" : ""} onchange="ustawWariant('${v.id}', '${v.wybrany}', this.checked)"> pytanie do zamawiającego</label>`}</td></tr>`).join("")}
    </table></div>`;
  if (!L.length) return tabWar;
  if (zam) return `${tabWar}<h3 style="margin-top:12px">Roboty, których nie ma w przedmiarze – ${L.length} poz.</h3>
    <p class="opis">Dokumentacja wymaga tych robót, ale przedmiar ich nie zawiera. Są ujęte w wartości (<b>${zl(R.w_cenie || 0)}</b> netto).
      <b>Uzupełnij przedmiar przed ogłoszeniem</b> – inaczej wykonawcy wycenią różny zakres albo zgłoszą roboty dodatkowe.</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Pozycja</th><th>Ilość</th><th>Wartość netto</th></tr>
      ${L.map(x => `<tr><td>${x.lp ? "<b>" + esc(x.lp) + "</b> " : ""}${esc(x.opis)}</td><td>${String(x.ilosc).replace(".", ",")} ${esc(x.jm)}</td><td>${zl(x.wartosc)}</td></tr>`).join("")}
    </table></div>`;
  return `${tabWar}<h3 style="margin-top:12px">Rozbieżności z przedmiarem – ${L.length} poz.</h3>
    <p class="opis">Roboty wymagane dokumentacją, których nie ma w przedmiarze. Przy każdej zdecyduj, co z nią zrobić. W cenie oferty: <b>${zl(R.w_cenie || 0)}</b> netto${R.na_umowe ? `; zostawione na etap umowy: <b>${zl(R.na_umowe)}</b>` : ""}.
      ${wyn ? `Wynagrodzenie: <b>${wyn}</b>${pod ? " – " + pod : ""}.` : "Rodzaj wynagrodzenia nieustalony – sprawdź w umowie, czy to ryczałt."}
      ${tp ? (tp.minal ? ` <b class="czerwone">Termin na pytania minął ${esc(dataPl(tp.data))}.</b>` : ` Pytania do zamawiającego można wysłać do <b>${esc(dataPl(tp.data))}</b>.`) : ""}</p>
    ${R.ostrzezenie ? `<div class="ramka-uwaga">${esc(R.ostrzezenie)}</div>` : ""}
    <div class="tabela-okno"><table class="tabela"><tr><th>Pozycja</th><th>Ilość</th><th>Wartość netto</th><th>Decyzja</th></tr>
      ${L.map(x => `<tr class="${x.w_cenie ? "" : "wyszarzony"}"><td>${x.lp ? "<b>" + esc(x.lp) + "</b> " : ""}${esc(x.opis)}${x.kiedy ? `<br><small class="opis">decyzja: ${esc(x.kiedy)}${x.kto ? ", " + esc(x.kto) : ""}</small>` : ""}</td>
        <td>${String(x.ilosc).replace(".", ",")} ${esc(x.jm)}</td><td>${zl(x.wartosc)}${x.w_cenie ? "" : '<br><small class="opis">poza ceną</small>'}</td>
        <td><select style="max-width:250px" onchange="ustawRozbieznosc('${x.id}', this.value)">${Object.entries(D).map(([k, v]) => `<option value="${k}" ${k === x.decyzja ? "selected" : ""}>${esc(v)}</option>`).join("")}</select></td></tr>`).join("")}
    </table></div>`;
}
async function ustawRozbieznosc(id, decyzja, potwierdzam) {
  const r = await fetch(`/api/projekty/${PROJEKT_ID}/rozbieznosci`, {method: "POST", headers: {"Content-Type": "application/json", "X-Agent": "1"}, body: JSON.stringify({id, decyzja, potwierdzam: !!potwierdzam})});
  const j = await r.json().catch(() => ({}));
  if (r.status === 409 && j.potwierdz) { if (confirm(j.potwierdz + "\n\nZostawić mimo to na etap umowy?")) return ustawRozbieznosc(id, decyzja, true); return otworzProjekt(PROJEKT_ID); }
  if (!r.ok) { komunikat(j.blad || "Nie udało się zapisać decyzji.", true); return otworzProjekt(PROJEKT_ID); }
  komunikat(`Zapisano decyzję. Cena oferty: ${zl((j.oferta || {}).netto || 0)} netto.` + (j.info ? " " + j.info : "")); otworzProjekt(PROJEKT_ID);
}
async function ustawWariant(id, wybrany, pytanie) {
  const j = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/warianty`, {json: {id, wybrany, pytanie: !!pytanie}}));
  if (j) komunikat(`Zapisano wariant. ${["zamowienie", "inwestorski"].includes((PROJEKT || {}).typ) ? "Wartość" : "Cena oferty"}: ${zl((j.oferta || {}).netto || 0)} netto.` + (j.info ? " " + j.info : ""));
  otworzProjekt(PROJEKT_ID);
}
function lista(t, arr, num = false) { return arr && arr.length ? `<h3 style="margin-top:12px">${t}</h3><${num ? "ol" : "ul"} class="lista">${arr.map(x => `<li>${esc(x)}</li>`).join("")}</${num ? "ol" : "ul"}>` : ""; }

// rola bez Finansów i bez edycji Projektów (np. kierownik budowy): karta projektu z przedmiarem bez cen – serwer i tak nie przysyła kwot (H1-04)
function rysujProjektBezCen(p) {
  const real = ["realizacja", "zakonczony"].includes(p.status_projektu);
  $("#projekt").innerHTML = `<div class="naglowek"><h2 style="margin:0">${esc(p.nazwa)}</h2>
      ${real ? `<button class="glowny" data-ik="kask" onclick="doRealizacji('${escA(p.id)}', false)">Otwórz budowę</button>` : ""}</div>
    <div class="ramka-uwaga" id="bez-cen-info">Twoja rola (${esc(JA.rola_nazwa || "")}) nie obejmuje Finansów – widzisz przedmiar robót <b>bez cen</b>.
      Kosztorys ofertowy, ceny i pliki z kwotami są niedostępne.</div>
    ${p.przetarg ? `<div class="opis">Przetarg: ${esc(p.przetarg.przedmiot || "")} · ${esc(p.przetarg.zamawiajacy || "")}</div>` : ""}
    <div class="krok"><div class="tytul"><span class="nr">${ik("tabela")}</span><h3>Przedmiar robót (bez cen)</h3></div><div class="tresc" id="przedmiar-bez-cen"><p class="opis">Ładuję…</p></div></div>
    <div class="krok"><div class="tytul"><span class="nr">${ik("folder")}</span><h3>Dokumenty projektu</h3><span class="stan">${(p.pliki || []).length}</span></div><div class="tresc">
      ${(p.pliki || []).length ? `<ul class="lista">${p.pliki.map(f => `<li><a href="/pobierz/${encodeURIComponent(p.id)}/dokumenty/${f.sciezka.split("/").map(encodeURIComponent).join("/")}">${esc(f.sciezka)}</a></li>`).join("")}</ul>`
        : '<p class="pusto">Brak dokumentów.</p>'}</div></div>`;
  wstawIkony($("#projekt"));
  api(`/api/projekty/${p.id}/pozycje`).then(d => {
    const el = $("#przedmiar-bez-cen"); if (!el) return;
    if (!d || d.brak || !(d.dzialy || []).length) { el.innerHTML = '<p class="pusto">Projekt nie ma jeszcze przedmiaru (kosztorysu).</p>'; return; }
    let lp = 0;
    el.innerHTML = `<div class="pasek" style="margin:0 0 8px"><a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${encodeURIComponent(p.id)}/przedmiar.xlsx">Pobierz przedmiar (Excel, bez cen)</a></div>
      <div class="tabela-okno" style="max-height:520px"><table class="tabela"><tr><th>Lp.</th><th>Podstawa</th><th>Opis pozycji</th><th>j.m.</th><th>Ilość</th></tr>
      ${d.dzialy.map(dz => `<tr class="wn-k-dzial"><td colspan="5">${esc(dz.nazwa || "")}</td></tr>` + (dz.pozycje || []).map(x => `<tr><td>${++lp}</td><td>${esc(x.podstawa || "")}</td>
        <td>${esc(x.opis || "")}</td><td>${esc(x.jm || "")}</td><td class="liczba">${String(x.ilosc ?? "").replace(".", ",")}</td></tr>`).join("")).join("")}</table></div>`;
    wstawIkony(el);
  }).catch(() => { const el = $("#przedmiar-bez-cen"); if (el) el.innerHTML = '<p class="pusto">Nie udało się wczytać przedmiaru.</p>'; });
}
function rysujProjekt() {
  if (typeof JA !== "undefined" && JA && JA.bez_cen && PROJEKT) return rysujProjektBezCen(PROJEKT);
  if ((PROJEKT || {}).typ === "prawnik") return rysujSprawePrawnika(PROJEKT);
  const p = PROJEKT, o = p.oferta, m = p.materialy, t = p.przetarg, typ = p.typ || "przetarg", U = typ === "zamowienie", I = typ === "inwestorski" || U,
    K = typ === "kosztorys" || I, W = typ === "wlasny", Z = typ === "weryfikacja" || typ === "dokumentacja" || typ === "prawnik", D = typ === "dom",
    RZ = p.rodzaj_zamowienia || "roboty";
  const T = {
    dok: {przetarg: "Dokumenty przetargu", wlasny: "Umowa i dokumenty projektu", kosztorys: "Dokumenty do wyceny", inwestorski: "Dokumentacja projektowa",
      zamowienie: ({uslugi: "Opis potrzeb i dokumenty postępowania", dostawy: "Wykaz towarów i dokumenty postępowania"}[p.rodzaj_zamowienia] || "Dokumentacja projektu i postępowania"), dom: "Projekt domu i dokumenty", dotacja: "Dokumenty dotacji", wniosek_dot: "Dokumenty naboru",
      weryfikacja: "Dokumentacja przetargowa do sprawdzenia", dokumentacja: "Materiały źródłowe (projekt, przedmiar, kosztorys)", prawnik: "Dokumentacja postępowania do sprawdzenia"}[typ],
    dokOpis: {przetarg: "", wlasny: '<p class="opis">Umowa, zapytanie lub zlecenie inwestora, przedmiar, projekt, opis techniczny, zdjęcia.</p>',
      kosztorys: '<p class="opis">Przedmiar, projekt, rysunki, opis techniczny, zdjęcia. Jeśli nie masz dokumentów, opisz zakres i wymiary w polu w kroku 2.</p>',
      inwestorski: '<p class="opis">Projekt budowlany/wykonawczy, przedmiar robót, opis techniczny, STWiORB, rysunki. Kosztorys zostanie sporządzony zgodnie z tymi dokumentami.</p>',
      wniosek_dot: '<p class="opis">Dokumenty wybranego naboru: regulamin, wzór wniosku, instrukcja wypełniania, kryteria oceny, wzory załączników. Pobierają się same z wyszukiwarki dotacji; możesz też je wgrać. <button class="maly" onclick="pobierzDokNaboru()">Pobierz dokumenty naboru ponownie</button></p>',
      dotacja: '<p class="opis">Dokumenty będące podstawą dotacji: umowa o dofinansowanie / o objęcie przedsięwzięcia wsparciem (z aneksami), wniosek o dofinansowanie, regulamin naboru, wytyczne programu, harmonogram rzeczowo-finansowy, wskaźniki i kamienie milowe.</p>',
      dom: '<p class="opis">Projekt budowlany domu (PDF), rzuty, przekroje, elewacje, opis techniczny, zestawienie powierzchni, projekt instalacji, ewentualnie przedmiar lub gotowy kosztorys. Duże rysunki możesz pominąć (Uwzględnij/pomiń), jeśli opis techniczny zawiera wymiary.</p>',
      zamowienie: ({uslugi: '<p class="opis">Dokumenty zamówienia na usługi: opis potrzeb (zakres, obiekty, powierzchnie, częstotliwość, okres), dotychczasowe umowy i ich koszty, a także SWZ / zapytanie, OPZ i wzór umowy do sprawdzenia.</p>',
        dostawy: '<p class="opis">Dokumenty zamówienia na dostawy: wykaz potrzebnych towarów z ilościami i wymaganymi parametrami, oferty rynkowe, a także SWZ / zapytanie, OPZ, formularz cenowy i wzór umowy do sprawdzenia.</p>'}[p.rodzaj_zamowienia]
        || '<p class="opis">Wszystkie dokumenty zamówienia w jednym miejscu: projekt, przedmiar, STWiORB, rysunki, a także SWZ / zapytanie, OPZ i wzór umowy do sprawdzenia. Z tych plików korzystają kosztorys, weryfikacja i sporządzanie dokumentacji poniżej.</p>'),
      weryfikacja: '<p class="opis">SWZ lub zapytanie ofertowe, opis przedmiotu zamówienia, przedmiar, projektowane postanowienia umowy, formularze, kosztorys inwestorski.</p>',
      prawnik: '<p class="opis">Ogłoszenie, SWZ lub zapytanie, opis przedmiotu zamówienia (dokumentacja projektowa, STWiORB, przedmiar przy robotach), projektowane postanowienia umowy, formularze, wyjaśnienia i zmiany SWZ.</p>',
      dokumentacja: '<p class="opis">Opcjonalnie: projekt, przedmiar, STWiORB, kosztorys inwestorski, wcześniejsze dokumenty zamawiającego (np. regulamin udzielania zamówień).</p>'}[typ],
    of: D ? "Kosztorys budowy domu" : W || typ === "przetarg" ? "Kosztorys i oferta" : U ? ((p.kreator || {}).prywatny ? "Szacunek kosztów (AI) – inwestor prywatny, bez Pzp" : "Szacowanie wartości zamówienia") : K ? "Kosztorys" : "Oferta i kosztorys",
    btn: D ? "Przygotuj kosztorys budowy (AI)" : W || typ === "przetarg" ? "Przygotuj kosztorys w programie (AI)" : U ? "Przygotuj szacunek kosztów (AI)" : K ? "Przygotuj kosztorys" : "Przygotuj ofertę i kosztorys",
    wsk: D ? "Wskazówki (opcjonalnie), np. „stan deweloperski, pompa ciepła, dachówka ceramiczna, budowa z ekipami” albo „system gospodarczy – część prac sam”" : U && RZ === "uslugi" ? "Zakres i ilości usług w całym okresie umowy – np. „przerwy kawowe – 2622 porcje, obiady dwudaniowe – 606 porcji” albo „sprzątanie 2 400 m² × 12 miesięcy”" : U && RZ === "dostawy" ? "Asortyment i ilości – np. „60 ławek szkolnych regulowanych, 120 krzeseł, 2 tablice interaktywne, z dostawą i montażem”" : K ? "Opis zakresu prac, wymiary, materiały – np. „ocieplenie ścian domu 10 × 12 m, wys. 7 m, styropian grafitowy 20 cm, 14 okien 1,5 × 1,5 m, tynk silikonowy”"
           : "Wskazówki dla AI (opcjonalnie), np. „gwarancja 60 mies., wysokość budynku 18 m, styropian grafitowy”",
  };
  const wynikiTyp = re => (p.wyniki || []).filter(n => re.test(n));
  const poniedzialek = (() => { const d = new Date(); d.setDate(d.getDate() + ((8 - d.getDay()) % 7 || 7)); return d.toISOString().slice(0, 10); })();
  $("#projekt").innerHTML = `
  ${U ? '<div id="kreator-zam"></div>' : ""}
  <div class="naglowek"><input id="pr-nazwa" value="${esc(p.nazwa)}" onchange="zmienNazwe(this.value)">
    <button class="maly dozw" data-ik="pobierz" onclick="location.href='/api/projekty/${p.id}/raport.docx'" title="Raport projektu (Word)">Raport</button>
    ${D ? (p.status_projektu ? `<button class="glowny" data-ik="kask" onclick="doRealizacji('${p.id}', false)">Otwórz budowę</button>`
      : `<button class="zielony" data-ik="kask" onclick="doRealizacji('${p.id}', true)" ${o ? "" : 'title="Najpierw przygotuj kosztorys"'}>Rozpocznij budowę</button>`) :
    typ === "weryfikacja" || typ === "prawnik" || typ === "dotacja" || typ === "wniosek_dot" || (U && (p.dla_prawnika || STRONA === "prawnik")) ? "" :  // dotacje: bez „Przetarg wygrany – do realizacji” (GC-02)
    I || typ === "dokumentacja" ? (p.status_projektu ? `<button class="glowny" data-ik="kask" onclick="doRealizacji('${p.id}', false)">Otwórz w zarządzaniu inwestycją</button>`
      : `<button class="zielony" data-ik="trofeum" onclick="doRealizacji('${p.id}', true)">${I ? "Umowa podpisana – przekaż do realizacji umów" : "Przetarg rozstrzygnięty – zarządzaj inwestycją"}</button>`)
      : K ? `<button class="zielony" data-ik="teczka" onclick="kosztorysNaProjekt('${p.id}')">Utwórz z tego projekt własny</button>`
      : p.status_projektu === "realizacja" || p.status_projektu === "zakonczony"
      ? `<button class="glowny" data-ik="kask" onclick="doRealizacji('${p.id}', false)">Otwórz w realizacji</button>`
      : typ === "wlasny" || p.oferta_zlozona || p.wynik_oferty || !(p.przetarg || {}).termin_ofert || String((p.przetarg || {}).termin_ofert).slice(0, 16).replace("T", " ") < new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16).replace("T", " ")
      ? `<button class="zielony" data-ik="trofeum" onclick="doRealizacji('${p.id}', true)">${typ === "wlasny" ? "Przenieś do realizacji" : "Przetarg wygrany – do realizacji"}</button>`
      : ""}
    <button class="maly" data-ik="teczka" onclick="usunProjekt()" title="Projekt trafi do Archiwum – można go przywrócić">Archiwizuj</button></div>
  ${ADMIN() ? panelDostepu(p) : (p.wlasciciel && p.wlasciciel !== JA.login ? `<div class="opis">Projekt udostępniony przez administratora.</div>`
    : `<div class="opis">${ik("ludzie")} Projekt widzisz tylko Ty i administrator programu – inni użytkownicy nie mają do niego dostępu.</div>`)}
  ${U ? `<div class="rodzaj-zam">${ik({roboty: "kask", uslugi: "ludzie", dostawy: "ciezarowka"}[RZ])} Rodzaj zamówienia:
    <select onchange="zmienRodzajZam(this.value)">${Object.entries(RODZ_ZAM).map(([k, v]) => `<option value="${k}" ${k === RZ ? "selected" : ""}>${v}</option>`).join("")}</select>
    <span class="opis" style="margin:0">– od tego zależą szacowanie wartości, dokumenty postępowania i zakres sprawdzenia dokumentacji.</span></div>` : ""}
  ${t ? `<div class="opis">Przetarg: ${esc(t.przedmiot)} · ${esc(t.zamawiajacy)} · termin ofert ${esc(dataPl(t.termin_ofert))}
    ${t.link ? ` · <a href="${esc(t.link)}" target="_blank" rel="noopener">ogłoszenie</a>` : ""}</div>` : ""}

  ${panelPrzegladu(p)}
  <div class="krok" id="sek-dokumenty"><div class="tytul"><span class="nr">${ik("wgraj")}</span><h3>1. ${T.dok}</h3><span class="stan">${p.pliki.length} ${p.pliki.length === 1 ? "plik" : [2,3,4].includes(p.pliki.length % 10) && ![12,13,14].includes(p.pliki.length % 100) ? "pliki" : "plików"}</span></div><div class="tresc">${T.dokOpis}
    <div class="upusc" id="upusc">Przeciągnij tutaj pliki (PDF, DOC, DOCX, XLSX, ZIP, JPG) albo
      <label class="przycisk" data-ik="wgraj">wybierz z dysku<input type="file" multiple hidden onchange="wgrajPliki(this.files)"></label></div>
    ${true ? `<div style="display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;margin:8px 0">
      <label class="ks-pole" style="flex:1;min-width:240px">${t ? "albo wklej link do strony TEGO postępowania (gdy ogłoszenie odsyła do ogólnej listy zamówień)" : "albo podaj link do ogłoszenia / postępowania (e-Zamówienia, BZP, Baza Konkurencyjności, BIP, platforma zakupowa)"}
        <input id="dok-link" type="url" placeholder="https://…" value="${esc((p.link_postepowania || {}).url || "")}"></label>
      <button class="zielony" data-ik="pobierz" onclick="pobierzZLinku()">Pobierz dokumenty z linku</button></div>
      ${p.link_postepowania ? `<p class="opis" style="margin:0 0 6px">Z linku ${esc(p.link_postepowania.data)}: ${p.link_postepowania.pliki} plików (${esc(p.link_postepowania.sposob)})${p.link_postepowania.uwaga ? " – " + esc(p.link_postepowania.uwaga) : ""}.</p>` : ""}` : ""}
    <div class="pasek">
      ${t ? `<button class="zielony" data-ik="pobierz" onclick="pobierzBK()">Pobierz i dodaj wszystkie dokumenty z ogłoszenia (${t.bk_id ? "Baza Konkurencyjności" : "BZP / e-Zamówienia / platforma"})</button>` : ""}
      ${p.pliki.some(x => !x.uwzglednij) ? `<button data-ik="iskra" onclick="uwzglednijWszystkie()">Uwzględnij wszystkie (${p.pliki.filter(x => !x.uwzglednij).length} pominiętych)</button>` : ""}
      <button data-ik="przelacz" onclick="przelaczPliki()">Uwzględnij / pomiń zaznaczone</button>
      <button data-ik="kosz" onclick="usunPliki(false)">Usuń zaznaczone</button>
      <button class="niebezp" data-ik="kosz" onclick="usunPliki(true)">Usuń wszystkie pliki</button>
      <span class="licznik" id="licznik-ai">Do AI: ok. ${liczba(p.pliki.filter(f => f.uwzglednij).reduce((s, f) => s + f.rozmiar * (/pdf|jpe?g|png|webp/.test(f.typ) ? 1.34 : 0.3), 0) / 1048576)} MB z 50 MB</span>
    </div>
    ${(p.platformy_zakupowe || []).length ? `<div class="ramka-uwaga" style="margin:0 0 10px">Dokumenty zamówienia (SWZ, przedmiar) są na platformie zamawiającego –
      pobierz je stamtąd i dodaj powyżej: ${p.platformy_zakupowe.map(u => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace(/^https?:\/\//, "").slice(0, 60))}</a>`).join(", ")}</div>` : ""}
    ${p.pliki.length ? `<div class="tabela-okno" style="max-height:260px"><table class="tabela"><tr><th></th><th>Uwzględnij</th><th>Plik</th><th>Typ</th><th>Rozmiar</th></tr>
      ${p.pliki.map(f => `<tr><td><input type="checkbox" class="pl" value="${esc(f.sciezka)}"></td><td>${f.uwzglednij ? "✔" : '<span class="czerwone">pominięty</span>'}</td>
      <td>${esc(f.sciezka)}</td><td>${esc(f.typ)}</td><td class="liczba">${liczba(f.rozmiar / 1048576, 2)} MB</td></tr>`).join("")}</table></div>` : ""}
  </div></div>

  ${panelCzatu(p)}
  ${Z ? (typ === "prawnik" ? prawnikUstawienia(p) + krokZamawiajacego(p, "weryfikacja") + prawnikOpinia(p) : krokZamawiajacego(p)) + "<!--KONIEC-->" : ""}
  ${!Z && (U || W || typ === "przetarg") ? krokZamawiajacego(p, "weryfikacja", 2) : ""}

  <div class="krok k-ziel" id="sek-kosztorys"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>2. ${T.of}</h3><span class="stan">${o ? "gotowe" : "do zrobienia"}</span></div><div class="tresc">
    ${W || typ === "przetarg" ? `<h4 class="etap-kroku"><span>A</span> Kosztorys – przygotuj go w programie albo wgraj własny</h4>` : ""}
    <textarea id="wsk-oferta" placeholder="${esc(T.wsk)}" ${K ? 'style="min-height:110px"' : ""}>${esc(p.opis_zakresu || "")}</textarea>
    <div class="vat-wybor"><label>Stawka VAT ${selectVat("vat-wybor", p.vat_wybor || "auto")}</label>
      <span class="opis">${I ? "Wartość zamówienia ustala się bez VAT (art. 28 Pzp) – kwota brutto służy tylko do zabezpieczenia środków w budżecie."
        : `Stawkę VAT ustala wykonawca (ustawa o VAT): „auto” – z dokumentów przetargu, a gdy ich brak – roboty budowlane 23%.
        8% tylko dla budownictwa objętego społecznym programem mieszkaniowym (budynki i lokale mieszkalne w limitach powierzchni) – do potwierdzenia.`}</span></div>
    ${Z ? "" : `<div class="ceny-wybor"><b>Ceny w kosztorysie:</b>
      <label><input type="radio" name="ceny-zrodlo" value="rynkowe" ${p.ceny_zrodlo !== "cennik" ? "checked" : ""}> <b>A</b> – ceny rynkowe</label>
      <label><input type="radio" name="ceny-zrodlo" value="cennik" ${p.ceny_zrodlo === "cennik" ? "checked" : ""}> <b>B</b> – według mojego cennika</label>
      <span class="opis" style="margin:0;flex-basis:100%">W wariancie B pozycje, których nie ma w Twoim cenniku, zostaną wycenione według cen rynkowych.</span>
      <div id="cennik-stan" class="cennik-stan"></div></div>`}
    <div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="iskra" onclick="generujOferte()">${T.btn}</button>
      <span class="opis" style="margin:0">Trwa zwykle 3–10 minut. Wycena cenami rynkowymi; najdroższe pozycje są sprawdzane w internecie.</span></div>
    ${W || typ === "przetarg" ? `<div class="pasek" style="margin-top:6px"><span class="opis" style="margin:0 6px 0 0"><b>albo</b></span>
      <label class="przycisk" data-ik="wgraj">Wgraj własny kosztorys (Excel lub PDF)<input type="file" accept=".xlsx,.xlsm,.pdf,.xls,.ods" hidden onchange="wgrajKosztorysWlasny(this.files[0])"></label>
      <span class="opis" style="margin:0">Masz już kosztorys (np. z programu kosztorysowego)? Program go wczyta bez zmiany cen${typ === "przetarg" ? ", a dane przetargu odczyta z SWZ" : ""} –
        oferta powstanie na jego podstawie (punkt B).</span></div>` : ""}
    ${D ? `<div class="pasek" style="margin-top:6px"><label class="przycisk" data-ik="wgraj">Wgraj własny kosztorys (Excel lub PDF)<input type="file" accept=".xlsx,.xlsm,.pdf,.xls,.ods" hidden onchange="wgrajKosztorysWlasny(this.files[0])"></label>
      <span class="opis" style="margin:0">Masz kosztorys od projektanta lub kosztorysanta? Program go wczyta (bez własnej wyceny) i pogrupuje w etapy budowy.</span></div>
    <div class="pasek" style="margin-top:6px"><button class="zolty" data-ik="pobierz" onclick="kosztorysPusty()">Pusty kosztorys dla wykonawców (do wyceny)</button>
      <span class="opis" style="margin:0">Kosztorys ślepy z pozycjami i ilościami z projektu, bez cen – wykonawcy wpisują swoje ceny w żółte pola, a Excel sam liczy sumy, VAT i brutto.
        ${p.kosztorys_pusty ? `Ostatnio: <a href="/pobierz/${p.id}/${encodeURIComponent(p.kosztorys_pusty)}">${esc(p.kosztorys_pusty)}</a>` : ""}</span></div>` : ""}
    ${o && o.vat_nieustalony ? `<div class="ramka-uwaga"><b>Stawka VAT do ustalenia.</b> Dokumenty przetargu jej nie określają – do obliczeń przyjęto 23%.
      Stawkę ustala wykonawca (roboty budowlane 23%; 8% tylko budownictwo objęte społecznym programem mieszkaniowym) – wybierz ją poniżej: ${selectVat("vat-zmiana", "auto")} <button class="maly zolty" onclick="zmienVat()">Przelicz z tą stawką</button></div>` : ""}
    ${o ? `<div class="kwoty"><div><span>Netto</span><b>${zl(o.netto)}</b></div><div class="${o.vat_nieustalony ? "pilne" : ""}"><span>VAT ${Math.round(o.vat * 100)}%${o.vat_nieustalony ? " – do ustalenia" : ""}</span><b>${zl(o.vat_kwota)}</b></div>
      <div class="brutto"><span>Brutto</span><b>${zl(o.brutto)}</b></div>${o.z_internetu ? `<div><span>Ceny z internetu</span><b>${o.z_internetu} poz.</b></div>` : ""}</div>
      <div class="opis">${esc(o.nazwa_zamowienia)}${typ === "przetarg" ? `<br>Nr ${esc(o.numer)} · termin składania: <b>${esc(o.termin_skladania)}</b> · wadium: ${esc(o.wadium)}` : (o.obiekt ? " · " + esc(o.obiekt) : "")}</div>
      <p>${esc(o.podsumowanie)}</p>
      ${lista(I ? "Do sprawdzenia przed przyjęciem wartości" : "Do weryfikacji przed złożeniem", o.do_weryfikacji, true)}${lista("Do uzupełnienia", o.do_uzupelnienia)}
      ${panelRozbieznosci(p, I)}
      ${I && (o.ilosci_bez_podstawy || []).length ? `<div class="ramka-uwaga" style="border-color:#C00000"><b>⚠ ${o.ilosci_bez_podstawy.length} pozycji ma ilość, której nie ma w dokumentach ani w Twoim opisie</b> – nie przyjmuj wartości przed sprawdzeniem.
        Uzupełnij ilości w opisie (kreator: Szczegóły → zakres ilościowy) albo wgraj ogłoszenie / SWZ i przelicz kosztorys.<ul class="lista">${o.ilosci_bez_podstawy.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}
      ${lista(I ? "Co może zmienić wartość zamówienia" : K ? "Co może zmienić cenę" : "Ryzyka", o.ryzyka)}${lista(typ === "przetarg" ? "Pytania do zamawiającego" : I ? "Do ustalenia przed wszczęciem postępowania" : "Pytania do inwestora", o.pytania, true)}
      ${I ? `<div class="pasek" style="margin:8px 0"><button class="glowny" data-ik="dokument" onclick="notatkaSzacowania()">Notatka z szacowania wartości (Word)</button>
        ${RZ !== "roboty" ? `<button class="maly" data-ik="pobierz" onclick="kosztorysPusty()">Pusty formularz ${RZ === "dostawy" ? "asortymentowo-cenowy" : "cenowy"} dla wykonawców (do SWZ)</button>` : ""}
        <span class="opis" style="margin:0" id="tryb-szac"></span></div>` : ""}
      <div class="korekta"><h3>${ik("procent")} ${D ? "Dostosuj budżet (wartość kosztorysu)" : K ? "Dostosuj wartość kosztorysu" : "Dostosuj cenę ofertową"}</h3>
        <p class="opis">Zmienia proporcjonalnie ceny jednostkowe wszystkich pozycji kosztorysu (liczone od wyceny pierwotnej:
          netto ${zl(o.netto_pierwotne ?? o.netto)}, brutto ${zl(o.brutto_pierwotne ?? o.brutto)}). Kosztorys, formularze i kwoty słownie zostaną przeliczone.
          ${o.korekta ? `<br><b class="${o.korekta.procent < 0 ? "czerwone" : "zielone"}">Aktualna korekta: ${o.korekta.procent > 0 ? "+" : ""}${liczba(o.korekta.procent, 2)}%</b>` : ""}</p>
        ${o.vat_nieustalony ? "" : `<div class="pasek" style="margin:0 0 8px"><span class="opis" style="margin:0">Stawka VAT: <b>${Math.round(o.vat * 100)}%</b> – zmień:</span>
          ${selectVat("vat-zmiana", String(o.vat))}<button class="maly" onclick="zmienVat()">Przelicz z tą stawką</button></div>`}
        <div class="tryby">
          <label><input type="radio" name="kt" value="brutto" checked> Cena docelowa brutto [zł]</label>
          <label><input type="radio" name="kt" value="netto"> Cena docelowa netto [zł]</label>
          <label><input type="radio" name="kt" value="procent"> Zmiana procentowa [%] (np. -5 lub 3,5)</label>
        </div>
        <div class="pasek"><input id="kt-wartosc" placeholder="wartość" style="width:180px">
          <button class="glowny" data-ik="procent" onclick="dostosujCene()">Przelicz ofertę</button>
          ${o.korekta ? `<button data-ik="cofnij" onclick="dostosujCene(true)">Przywróć cenę pierwotną</button>` : ""}</div>
      </div>` : ""}
    <div class="pliki-wynik">${[...wynikiTyp(/^Kosztorys_/), ...wynikiTyp(/^Oferta_/), ...wynikiTyp(/^Analiza_/)].map(plik).join("")}</div>
    ${o && p.kosztorys_klienta ? `<p class="opis" style="margin:6px 0 0">${ik("dokument")} <b>Kosztorys_dla_klienta</b> – wersja do przekazania klientowi lub zamawiającemu:
      bez kolumn „Źródło ceny” i „Uwagi / podstawa ilości”, bez oznaczeń kolorami i notatek roboczych${typ === "przetarg" ? "; to ta wersja trafia do kompletu dokumentów przetargu" : ""}.</p>` : ""}
    ${o ? panelKontroli(p) : ""}
  </div></div>

  ${W ? krokUmowy(p) : ""}
  ${K && typ !== "kosztorys" ? (U ? krokZamawiajacego(p, "dokumentacja", 4) : I ? `<div class="karta"><b>Co dalej?</b> Kosztorys inwestorski możesz pobrać powyżej. Wartość netto wpisz jako wartość szacunkową
    w module „Sporządź dokumentację”, a plik dołącz do dokumentacji przetargowej. Po podpisaniu umowy kliknij „Umowa podpisana – przekaż do realizacji umów” –
    harmonogram rzeczowo-finansowy i protokoły odbioru powstaną na podstawie działów tego kosztorysu.</div>`
    : `<div class="karta"><b>Co dalej?</b> Kosztorys możesz pobrać powyżej. Aby przygotować z niego ofertę, listę materiałów, harmonogram
    i zamówienia, a potem przenieść prace do realizacji – kliknij „Utwórz z tego projekt własny” na górze.</div>`) : `
  <div class="krok k-ziel" id="sek-dok-wyk"><div class="tytul"><span class="nr">${ik("teczka")}</span><h3>${W ? 4 : 3}. Dokumenty wykonawcy do oferty</h3><span class="stan">${
    p.komplet ? ((p.komplet.braki || []).length ? `brakuje: ${p.komplet.braki.length}` : "komplet gotowy") : (p.pliki_wykonawcy.length ? p.pliki_wykonawcy.filter(x => x.sprawdzony).length + "/" + p.pliki_wykonawcy.length + " sprawdzonych" : "do zrobienia")}</span></div><div class="tresc">
    <p class="opis">Dodaj dokumenty firmy dołączane do oferty: podpisane formularze, KRS/CEIDG, polisę OC, referencje, uprawnienia,
      pełnomocnictwa, zaświadczenia. Po sprawdzeniu każdego pliku utwórz komplet – oferta i dokumenty trafią do jednego folderu (ZIP).</p>
    ${p.wymagane_dokumenty && p.wymagane_dokumenty.length ? `<div class="karta" style="margin:0 0 14px;padding:14px 18px"><b>Wymagane przez zamawiającego (z analizy oferty):</b>
      <ul class="lista">${p.wymagane_dokumenty.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}
    <div class="upusc" id="upusc-wyk">Przeciągnij tutaj dokumenty wykonawcy albo
      <label class="przycisk" data-ik="wgraj">wybierz z dysku<input type="file" multiple hidden onchange="wgrajWykonawca(this.files)"></label></div>
    ${p.pliki_wykonawcy.length ? `<div class="tabela-okno" style="max-height:300px"><table class="tabela"><tr><th></th><th>Dokument</th><th>Rozmiar</th><th>Sprawdzony</th></tr>
      ${p.pliki_wykonawcy.map(f => `<tr><td><input type="checkbox" class="plw" value="${esc(f.nazwa)}"></td>
        <td><a href="/pobierz/${PROJEKT_ID}/dokumenty_wykonawcy/${encodeURIComponent(f.nazwa)}">${esc(f.nazwa)}</a></td>
        <td class="liczba">${liczba(f.rozmiar / 1048576, 2)} MB</td>
        <td><label style="display:flex;gap:8px;align-items:center;font-weight:600;color:${f.sprawdzony ? "var(--zielony)" : "var(--zolty-ciemny)"}">
          <input type="checkbox" ${f.sprawdzony ? "checked" : ""} onchange="sprawdzWyk(['${escA(f.nazwa)}'], this.checked)"> ${f.sprawdzony ? "sprawdzony" : "do sprawdzenia"}</label></td></tr>`).join("")}
      </table></div>
      <div class="pasek" style="margin-top:10px"><button data-ik="protokol" onclick="sprawdzWyk(zaznaczoneWyk(), true)">Oznacz zaznaczone jako sprawdzone</button>
        <button data-ik="kosz" onclick="usunWyk(false)">Usuń zaznaczone</button>
        <button class="niebezp" data-ik="kosz" onclick="usunWyk(true)">Usuń wszystkie</button></div>` : ""}
    <div class="pasek"><button data-ik="wizytowka" onclick="zProfiluFirmy()">Dodaj z Profilu firmy (polisa, referencje, certyfikaty)</button></div><div id="z-profilu"></div>
    <div class="pasek" style="margin-top:6px"><button class="zielony" data-ik="teczka" onclick="utworzKomplet()">Utwórz komplet dokumentów do przetargu</button>
      ${p.komplet ? `<span class="opis" style="margin:0">Ostatnio: ${esc(p.komplet.utworzono)}, ${p.komplet.plikow} plików</span>` : ""}</div>
    ${p.komplet ? `<div class="pliki-wynik"><a href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(p.komplet.zip)}">${esc(p.komplet.zip)}</a></div>` : ""}
  </div></div>

  <div class="krok k-zolt"><div class="tytul"><span class="nr">${ik("paczka")}</span><h3>${W ? 5 : 4}. Zapotrzebowanie materiałowe</h3><span class="stan">${m ? m.liczba + " materiałów" : "do zrobienia"}</span></div><div class="tresc">
    <textarea id="wsk-mat" placeholder="Wskazówki (opcjonalnie), np. „styropian grafitowy 15 cm λ 0,031; tytan-cynk 0,7 mm; rusztowania wynajmujemy z deskami”"></textarea>
    <div class="pasek" style="margin-top:8px"><button class="zolty" data-ik="paczka" onclick="generujMaterialy()">Utwórz listę materiałów</button>
      <label class="przycisk" data-ik="wgraj">Wgraj własny kosztorys (xlsx)<input type="file" accept=".xlsx" hidden onchange="wgrajWynik(this, 'kosztorys')"></label>
      <span class="opis" style="margin:0">Kosztorys: ${esc(p.kosztorys || "brak")}</span></div>
    ${m ? `<div class="kwoty"><div><span>Materiały netto (z zapasem)</span><b>${zl(m.razem)}</b></div>${m.udzial ? `<div><span>Udział w cenie netto</span><b>${Math.round(m.udzial * 100)}%</b></div>` : ""}</div>
      <table class="tabela" style="max-width:900px"><tr><th>Największe pozycje</th><th>Ilość</th><th>Wartość</th></tr>
      ${m.najwieksze.map(x => `<tr><td>${esc(x.nazwa)}</td><td class="liczba">${liczba(x.ilosc)} ${esc(x.jm)}</td><td class="liczba">${zl(x.wartosc)}</td></tr>`).join("")}</table>
      ${lista("Uwagi", m.uwagi)}` : ""}
    <div class="pliki-wynik">${wynikiTyp(/^Lista_materialow_/).map(plik).join("")}</div>
  </div></div>

  <div class="krok k-czer"><div class="tytul"><span class="nr">${ik("kalendarz")}</span><h3>${W ? 6 : 5}. Harmonogram i podział dostaw</h3><span class="stan">${p.etapy ? p.etapy.length + " etapów" + (p.harmonogram_zespol ? " · " + p.harmonogram_zespol.liczba + " os." : "") : "do zrobienia"}</span></div><div class="tresc">
    <div class="siatka">
      <label>Start robót<input type="date" id="h-start" value="${p.etapy ? p.etapy[0].od : poniedzialek}"></label>
      <label>Liczba etapów<input type="number" id="h-n" min="1" max="30" value="${p.etapy ? p.etapy.length : 5}"></label>
      <label>Długość etapu [dni]<input type="number" id="h-dl" min="1" max="60" value="7"></label>
      <label>Liczba pracowników<input type="number" id="h-prac" min="1" max="200" value="${(p.harmonogram_zespol && p.harmonogram_zespol.liczba) || Math.max(PRACOWNICY.length, 4)}"></label>
    </div>
    ${PRACOWNICY.length ? `<div class="opis" style="margin:4px 0 2px;font-weight:600">Pracownicy na budowie (opcjonalnie – zaznaczeni zwiększają liczbę, jeśli jest mniejsza):</div>
      <div class="wybor-h">${PRACOWNICY.map(x => `<label><input type="checkbox" class="h-wyb" value="${esc(x.id)}" onchange="liczWybranych()"
        ${p.harmonogram_zespol && (p.harmonogram_zespol.wybrani || []).includes(x.id) ? "checked" : ""}> ${esc(x.imie)}${x.stanowisko ? ` <small class="opis" style="margin:0">(${esc(x.stanowisko)})</small>` : ""}</label>`).join("")}</div>`
      : `<p class="opis">Pracowników dodasz w zakładce Pracownicy – wtedy wybierzesz ich tutaj z listy.</p>`}
    <div class="siatka"><label>Nazwa budowy<input id="h-budowa" value="${esc(p.nazwa)}"></label>
      <label style="grid-column: span 2">Adres dostaw<input id="h-adres" value="${esc(p.adres_dostaw || (o && o.obiekt) || "")}"></label></div>
    <textarea id="wsk-harm" placeholder="Wskazówki (opcjonalnie), np. „dach i elewacja równolegle”, „tytan-cynk zamówić wcześniej”"></textarea>
    <div class="pasek" style="margin-top:8px"><button class="glowny" data-ik="kalendarz" onclick="generujHarmonogram()">Podziel materiały na etapy</button>
      <label class="przycisk" data-ik="wgraj">Wgraj własną listę materiałów<input type="file" accept=".xlsx" hidden onchange="wgrajWynik(this, 'lista')"></label>
      ${p.etapy ? `<label class="przycisk" data-ik="wgraj">Wgraj poprawiony harmonogram<input type="file" accept=".xlsx" hidden onchange="wgrajWynik(this, 'harmonogram')"></label>` : ""}</div>
    ${p.etapy ? `<div class="tabela-okno"><table class="tabela"><tr><th>Etap</th><th>Nazwa</th><th>Od</th><th>Do</th><th>Obsada</th><th>Materiałów</th><th>Dostawy netto</th></tr>
      ${p.etapy.map(e => `<tr><td>${e.nr}</td><td>${esc(e.nazwa)}</td><td>${dataPl(e.od)}</td><td>${dataPl(e.do)}</td><td>${esc(e.obsada || "")}</td><td class="liczba">${e.materialow}</td><td class="liczba">${e.materialow ? zl(e.wartosc) : "–"}</td></tr>`).join("")}
      </table></div>${lista("Uwagi i ograniczenia", p.harmonogram_uwagi)}
      <p class="opis">Procentowy podział możesz zmienić w arkuszu „Podział dostaw”, a potem wgrać plik z powrotem – zamówienia uwzględnią zmiany.</p>` : ""}
    <div class="pliki-wynik">${wynikiTyp(/^Harmonogram_dostaw_/).map(plik).join("")}</div>
  </div></div>

  <div class="krok"><div class="tytul"><span class="nr">${ik("ciezarowka")}</span><h3>${W ? 7 : 6}. Zamówienia do hurtowni</h3></div><div class="tresc">
    ${!p.etapy ? '<p class="pusto">Najpierw utwórz harmonogram dostaw (krok 5).</p>' : !HURTOWNIE.length ?
      '<p class="pusto">Nie masz jeszcze hurtowni. <button class="maly zielony" onclick="pokaz(\'hurtownie\'); setTimeout(dodajHurtownie, 500)">Dodaj hurtownię</button> – wpisz nazwę, e-mail i asortyment, kliknij „Zapisz” i wróć do projektu.</p>' : `
    <div class="siatka">
      <label>Etap<select id="z-etap">${p.etapy.map((e, i) => `<option value="${i}">Etap ${e.nr}: ${esc(e.nazwa)} (dostawa ${dataPl(e.od)})</option>`).join("")}</select></label>
      <label>Rodzaj<select id="z-typ"><option value="zapytanie">Zapytanie ofertowe</option><option value="zamowienie">Zamówienie</option></select></label>
      <label>Odpowiedź do (dla zapytań)<input id="z-termin" placeholder="DD.MM.RRRR"></label>
    </div>
    <div class="siatka"><label style="grid-column: 1/-1">Adres dostawy<input id="z-adres" value="${esc(p.adres_dostaw || "")}"></label></div>
    <div class="wybor-h">${HURTOWNIE.map((h, i) => `<label><input type="checkbox" class="zh" value="${i}"> ${esc(h.nazwa)} <small class="opis" style="margin:0">(${esc(h.kategorie || "wszystko")})</small></label>`).join("")}</div>
    <textarea id="z-dopisek" placeholder="Dopisek do wiadomości (opcjonalnie)"></textarea>
    <div class="pasek" style="margin-top:8px">
      <button data-ik="oko" onclick="podgladZam()">Podgląd</button>
      <button class="glowny" data-ik="mail" onclick="wyslijZam('eml')">Pobierz szkice e-maili (.eml)</button>
      <button class="zielony" data-ik="wyslij" onclick="wyslijZam('smtp')">Wyślij bezpośrednio (SMTP)</button></div>
    <div id="z-wynik"></div>`}
  </div></div>`}`;
  if (Z) { const k = [...$("#projekt").childNodes].find(n => n.nodeType === 8 && n.textContent === "KONIEC");
    while (k && k.nextSibling) k.nextSibling.remove(); }
  if (typ === "przetarg" || W) { $("#projekt").insertAdjacentHTML("beforeend", sekcjaWnioskow(p)); if (WNIOSEK_OTWARTY) ladujKosztorysWniosku(); }
  const dostP = ["dostawy", "uslugi"].includes(p.rodzaj_zamowienia);
  $("#projekt").classList.remove("widok-szybki");  // klasa nie może zostać po poprzednio otwartym projekcie
  if (typ === "przetarg" && (dostP || !p.przetarg) && document.querySelector("#projekt > .krok")) {  // dostawca / usługodawca: 5 kroków; przetarg dodany ręcznie: ten sam przełącznik widoku
    widokSzybki(p);
  } else if (typ === "przetarg" && p.przetarg && document.querySelector("#projekt > .krok")) {  // konkurencja u zamawiającego
    document.querySelector("#projekt > .krok").insertAdjacentHTML("afterend", `<div class="historia-zam" id="pr-historia">${p.historia_zam ? "" :
      `<div class="karta hz"><div class="pasek"><button data-ik="trofeum" onclick="historiaProjektu()">Konkurencja u zamawiającego – ceny w podobnych przetargach, liczba ofert, kto wygrywa</button>
        <span class="opis" style="margin:0">ogłoszenia o wyniku z BZP</span></div></div>`}</div>`);
    if (p.historia_zam) rysujHistorie($("#pr-historia"), p.historia_zam, () => historiaProjektu(true));
    $("#pr-historia").insertAdjacentHTML("afterend", '<div id="pr-szanse"></div>');
    rysujSzanse(p);
    widokSzybki(p);
  }
  if (U) ladujKreator();
  if (U && !(p.kreator || {}).prywatny && $("#sek-kosztorys")) $("#sek-kosztorys").outerHTML = sekcjaSzacowania(p);
  licznikTokenow();  // kreator zamówienia prowadzi krok po kroku; pozostałe sekcje pod przyciskiem „Pokaż wszystkie sekcje”
  if (typ === "dotacja" || typ === "wniosek_dot") {  // dotacje: punkt 1 = dokumenty (+ asystent), dalej własne punkty 2–4
    [...document.querySelectorAll("#projekt > .krok")].forEach((k, i) => { const h = k.querySelector("h3")?.textContent || ""; if (i > 0 && !/Asystent/.test(h)) k.remove(); });
    const pb = typ === "wniosek_dot" && (p.wniosek_dot || {}).pobieranie, k1 = document.querySelector("#projekt > .krok > .tresc");
    if (pb && k1) k1.insertAdjacentHTML("afterbegin", `<div class="${pb.bledy.length ? "ramka-uwaga" : "wn-gotowe"}" style="margin-bottom:10px"><span>
      <b>Pobieranie dokumentów naboru (${esc(pb.data)}):</b> pobrano ${pb.pobrane.length}${pb.pominiete ? `, pominięto ${pb.pominiete} archiwalnych lub niezwiązanych z naborem` : ""}${(pb.odrzucone || []).length ? `, <b>odrzucono ${pb.odrzucone.length} dotyczących innego programu</b>` : ""}
      ${(pb.niepewne || []).length ? `<br><small>Sprawdź, czy dotyczą tego naboru: ${pb.niepewne.map(esc).join(", ")}</small>` : ""}
      ${(pb.odrzucone || []).length ? `<details><summary>Odrzucone dokumenty</summary><ul class="lista">${pb.odrzucone.map(b => `<li><a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.nazwa)}</a> <small class="opis">– ${esc(b.powod)}</small></li>`).join("")}</ul></details>` : ""}${pb.bledy.length ? `, <b class="czerwone">nie udało się ${pb.bledy.length}</b> – pobierz je w przeglądarce i wgraj tutaj:
      <ul class="lista">${pb.bledy.slice(0, 5).map(b => `<li><a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.nazwa)}</a> <small class="opis">– ${esc(b.blad)}</small></li>`).join("")}</ul>
      ${pb.bledy.length > 5 ? `<details><summary>Pokaż pozostałe (${pb.bledy.length - 5})</summary><ul class="lista">${pb.bledy.slice(5).map(b => `<li><a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.nazwa)}</a> <small class="opis">– ${esc(b.blad)}</small></li>`).join("")}</ul></details>` : ""}` : "."}</span></div>`);
    if (typ === "wniosek_dot" && k1) k1.insertAdjacentHTML("beforeend", `<div class="pasek" style="margin-top:8px"><b>Masz inny link?</b>
      <input id="wd-link" placeholder="link do strony z dokumentami naboru albo do pliku (np. regulaminu)" style="flex:1;min-width:240px">
      <button data-ik="pobierz" onclick="dodajLinkNaboru()">Pobierz z tego linku</button></div>`);
    $("#projekt").insertAdjacentHTML("beforeend", '<div id="dotacja" class="kroki-przezr"><p class="opis">Ładuję rozliczenie…</p></div>');  // kroki 2–4 i plan w panelu „Kroki” (GC-01)
    ladujDotacje();
  }
  if (typ === "kosztorys") {  // Kosztorysowanie: bez dokumentów wykonawcy; wycena materiałów; przeniesienie do innego modułu
    [...document.querySelectorAll("#projekt > .krok")].forEach(k => { if (/Dokumenty wykonawcy/.test(k.querySelector("h3")?.textContent || "")) k.remove(); });
    document.querySelectorAll("#projekt > .krok h3").forEach(h => { h.textContent = h.textContent.replace("Zapotrzebowanie materiałowe", "Wycena materiałów (zapotrzebowanie materiałowe)"); });
    let nr = 1; document.querySelectorAll("#projekt > .krok > .tytul h3").forEach(h => { if (/^\d+\./.test(h.textContent)) h.textContent = h.textContent.replace(/^\d+\./, () => (nr++) + "."); });
    if (p.oferta && $("#sek-kosztorys > .tresc")) {
      $("#sek-kosztorys > .tresc").insertAdjacentHTML("beforeend", `<div class="etap-b"><h4 class="etap-kroku"><span>A+</span> Modyfikuj lub usuń pozycje kosztorysu
        <button class="maly" data-ik="przelacz" onclick="const e=$('#popraw-pozycje'); if (e.innerHTML) e.innerHTML=''; else ladujPozycje();">Pokaż pozycje kosztorysu</button></h4>
        <div id="popraw-pozycje"></div></div>` + przeniesienieKosztorysu(p));
      wstawIkony($("#sek-kosztorys"));
    }
  }
  if ((W || typ === "przetarg") && $("#sek-kosztorys > .tresc")) {  // krok 2: A kosztorys → poprawki wybranych pozycji → B oferta
    if (p.oferta) $("#sek-kosztorys > .tresc").insertAdjacentHTML("beforeend", `<div class="etap-b"><h4 class="etap-kroku"><span>A+</span> Modyfikuj lub usuń pozycje kosztorysu
      <button class="maly" data-ik="przelacz" onclick="const e=$('#popraw-pozycje'); if (e.innerHTML) e.innerHTML=''; else ladujPozycje();">Pokaż pozycje kosztorysu</button></h4>
      <div id="popraw-pozycje"></div></div>`);
    $("#sek-kosztorys > .tresc").insertAdjacentHTML("beforeend", W ? sekcjaOfertyKlienta(p) : sekcjaOfertyPrzetargowej(p));
    wstawIkony($("#sek-kosztorys"));
  }
  if (p.oferta && !$("#popraw-pozycje") && $("#sek-kosztorys > .tresc") && !["dotacja", "wniosek_dot"].includes(typ)) {  // każdy kosztorys: modyfikuj / usuń pozycje
    $("#sek-kosztorys > .tresc").insertAdjacentHTML("beforeend", `<div class="etap-b"><h4 class="etap-kroku"><span>A+</span> Modyfikuj lub usuń pozycje kosztorysu
      <button class="maly" data-ik="przelacz" onclick="const e=$('#popraw-pozycje'); if (e.innerHTML) e.innerHTML=''; else ladujPozycje();">Pokaż pozycje kosztorysu</button></h4>
      <div id="popraw-pozycje"></div></div>`);
    wstawIkony($("#sek-kosztorys"));
  }
  if ($("#cennik-stan")) ladujCennikStan();
  if (D) {  // budowa domu: bez dokumentów wykonawcy do oferty; kolejne kroki numerowane od 3
    [...document.querySelectorAll("#projekt > .krok")].forEach(k => { if (/Dokumenty wykonawcy/.test(k.querySelector("h3")?.textContent || "")) k.remove(); });
    let nr = 1; document.querySelectorAll("#projekt > .krok h3").forEach(h => { h.textContent = h.textContent.replace(/^\d+\./, () => (nr++) + "."); });
  }
  paskiSekcji();
  if (FOKUS) { const f = FOKUS; FOKUS = null; setTimeout(() => document.getElementById(f)?.scrollIntoView({behavior: "smooth"}), 300); }
  wypelnijListeKlientow();
  const uw = $("#upusc-wyk");
  if (uw) {
    ["dragenter", "dragover"].forEach(e => uw.addEventListener(e, ev => { ev.preventDefault(); uw.classList.add("nad"); }));
    ["dragleave", "drop"].forEach(e => uw.addEventListener(e, ev => { ev.preventDefault(); uw.classList.remove("nad"); }));
    uw.addEventListener("drop", ev => wgrajWykonawca(ev.dataTransfer.files));
  }
  const u = $("#upusc");
  if (u) {
    ["dragenter", "dragover"].forEach(e => u.addEventListener(e, ev => { ev.preventDefault(); u.classList.add("nad"); }));
    ["dragleave", "drop"].forEach(e => u.addEventListener(e, ev => { ev.preventDefault(); u.classList.remove("nad"); }));
    u.addEventListener("drop", ev => wgrajPliki(ev.dataTransfer.files));
  }
}
async function wgrajWykonawca(files) {
  if (!files || !files.length) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wykonawca/pliki`, {method: "POST", body: fd})); otworzProjekt(PROJEKT_ID);
}
const zaznaczoneWyk = () => [...document.querySelectorAll(".plw:checked")].map(c => c.value);
async function sprawdzWyk(nazwy, v) { if (!nazwy.length) return komunikat("Zaznacz dokumenty.", true);
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wykonawca/sprawdz`, {json: {nazwy, sprawdzony: v}})); otworzProjekt(PROJEKT_ID); }
async function usunWyk(wszystkie) {
  const nazwy = wszystkie ? null : zaznaczoneWyk(); if (!wszystkie && !nazwy.length) return komunikat("Zaznacz dokumenty.", true);
  if (!confirm(wszystkie ? "Usunąć wszystkie dokumenty wykonawcy z projektu?" : `Usunąć ${nazwy.length} dokument(y)?`)) return;
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wykonawca/usun`, {json: {nazwy}})); otworzProjekt(PROJEKT_ID);
}
async function utworzKomplet(mimoTo) {
  const r = await fetch(`/api/projekty/${PROJEKT_ID}/komplet`, {method: "POST", headers: {"X-Agent": "1", "Content-Type": "application/json"}, body: JSON.stringify({mimo_to: !!mimoTo})});
  const d = await r.json().catch(() => ({}));
  if (r.status === 409) { if (confirm(`Nie wszystkie dokumenty są sprawdzone:\n${d.niesprawdzone.join("\n")}\n\nUtworzyć komplet mimo to?`)) utworzKomplet(true); return; }
  if (!r.ok) return komunikat(d.blad || "Błąd", true);
  komunikat((d.braki || []).length ? `Komplet spakowany (${d.plikow} plików), ale brakuje: ${d.braki.join("; ")}. Dodaj je w „Dokumentach wykonawcy” i przygotuj komplet ponownie.`
    : `Komplet gotowy: ${d.plikow} plików.` + ((d.uwagi || []).length ? " " + d.uwagi.join(" ") : ""), (d.braki || []).length > 0); otworzProjekt(PROJEKT_ID); location.href = d.url;
}
async function doRealizacji(id, zmien) {
  if (STRONA === "dostawca") {  // dostawca / usługodawca: realizacja umowy dostaw lub usług
    if (zmien && !confirm("Oznaczyć przetarg jako wygrany i przenieść umowę do zakładki „Realizacja umów”?")) return;
    if (zmien && !(await bezpiecznie(() => api(`/api/projekty/${id}/status`, {json: {status: "realizacja"}})))) return;
    DS_ID = id; pokaz("dos_realizacja"); return;
  }
  const zam = STRONA === "zamawiajacy", inw = STRONA === "inwestor";
  if (zmien && !confirm(inw ? "Rozpocząć budowę? Harmonogram etapów, odbiory i rozliczenie kosztów powstaną na podstawie kosztorysu." :
    zam ? "Umowa podpisana? Przekazać zamówienie do zakładki „Realizacja umów”?" : "Oznaczyć przetarg jako wygrany i przenieść projekt do zakładki „W realizacji”?")) return;
  if (zmien && !(await bezpiecznie(() => api(`/api/projekty/${id}/status`, {json: {status: "realizacja"}})))) return;
  STRONA_REAL = inw ? "inwestor" : zam ? "zamawiajacy" : "wykonawca"; REAL_ID = id; pokaz(inw ? "inw_budowa" : zam ? "zam_realizacja" : "realizacja");
}
// ---------- karta projektu (przegląd), notatki, szybkie przejścia
function odliczanie(termin, etykieta) {
  const d = dniDo(termin); if (d === null) return "";
  const kl = d < 0 ? "alarm" : d <= 7 ? "pilne" : "brutto";
  return `<div class="${kl}"><span>${etykieta}</span><b>${esc(dataPl(termin))}</b><small>${d < 0 ? `po terminie ${odm(-d, "dzień", "dni", "dni")}` : d === 0 ? "dziś!" : `pozostało ${odm(d, "dzień", "dni", "dni")}`}</small></div>`;
}
function panelPrzegladu(p) {
  const t = p.przetarg, o = p.oferta, rs = p.realizacja_skrot, fin = poziomU("finanse") >= 1;
  const kaf = [];
  if (rs) { kaf.push(odliczanie(rs.termin, "Zakończenie robót") || `<div><span>Zakończenie robót</span><b>–</b><small>uzupełnij w realizacji</small></div>`);
    kaf.push(`<div><span>Odbiory etapów</span><b>${rs.odebrane}/${rs.etapy}</b><small>${rs.usterki_otwarte ? odm(rs.usterki_otwarte, "otwarta usterka", "otwarte usterki", "otwartych usterek") : "bez otwartych usterek"}</small></div>`);
    if (fin) kaf.push(`<div><span>Zafakturowano / zapłacono</span><b>${zl(rs.zafakturowano_brutto)}</b><small>zapłacono ${zl(rs.zaplacono_brutto)}${rs.przeterminowane_brutto ? ` · <span class="czerwone">po terminie ${zl(rs.przeterminowane_brutto)}</span>` : ""}</small></div>`);
  } else if (t) kaf.push(odliczanie((p.przetarg_dane || {}).termin_ofert || t.termin_ofert, "Termin składania ofert")
      || `<div><span>Termin składania ofert</span><b>nie ustalono</b><small>uzupełnij w zakładce Przetargi (✎)</small></div>`);
  if (o && fin) kaf.push(`<div><span>${p.typ === "zamowienie" || p.typ === "inwestorski" ? ({uslugi: "Wartość usług", dostawy: "Wartość dostaw"}[p.rodzaj_zamowienia] || "Kosztorys inwestorski") : "Oferta"} brutto</span><b>${zl(o.brutto)}</b><small>netto ${zl(o.netto)}</small></div>`);
  kaf.push(`<div><span>Dokumenty</span><b>${p.pliki.length + (p.wyniki || []).length}</b><small>${p.pliki.length} wgranych · ${(p.wyniki || []).length} wygenerowanych</small></div>`);
  const N = (p.notatki || []).slice().sort((a, b) => (b.przypiete ? 1 : 0) - (a.przypiete ? 1 : 0) || b.czas.localeCompare(a.czas));
  return `<div class="karta przeglad" id="sek-przeglad"><div class="przeglad-gora"><h3>${ik("siatka")} Przegląd projektu</h3>
      ${t && t.link ? `<a class="przycisk dozw maly" data-ik="link" href="${esc(t.link)}" target="_blank" rel="noopener">Ogłoszenie przetargu</a>` : ""}
      ${rs ? `<button class="maly glowny" data-ik="kask" onclick="doRealizacji('${p.id}', false)">${p.strona === "zamawiajacy" ? "Realizacja umowy" : "Realizacja"}</button>
        ${fin ? `<button class="maly" data-ik="faktura" onclick="doRealizacji('${p.id}', false); setTimeout(() => $('#fv-nr')?.scrollIntoView({behavior:'smooth', block:'center'}), 1500)">Dodaj fakturę</button>` : ""}` : ""}
      <a class="przycisk dozw maly" data-ik="pobierz" href="/api/projekty/${p.id}/raport.docx">Raport projektu (Word)</a></div>
    ${p.przetarg_dane ? (d => `<div class="dane-przetargu"><div><span>Przedmiot</span><b>${esc(d.nazwa || "–")}</b></div>
      <div><span>Zamawiający</span><b>${esc(d.zamawiajacy || "–")}</b>${d.zamawiajacy_adres ? `<small>${esc(d.zamawiajacy_adres)}</small>` : ""}</div>
      <div><span>Numer postępowania</span><b>${esc(d.numer || "–")}</b>${d.numer_bazy && d.numer_bazy !== d.numer ? `<small>w bazie: ${esc(d.numer_bazy)}</small>` : ""}</div>
      ${d.wadium ? `<div><span>Wadium</span><b>${esc(d.wadium)}</b></div>` : ""}${d.termin_realizacji ? `<div><span>Termin realizacji</span><b>${esc(d.termin_realizacji)}</b></div>` : ""}
      ${d.gwarancja ? `<div><span>Gwarancja</span><b>${esc(d.gwarancja)}</b></div>` : ""}${d.kryteria ? `<div><span>Kryteria</span><b>${esc(d.kryteria)}</b></div>` : ""}</div>`)(p.przetarg_dane) : ""}
    <div class="kwoty kafle-przetargu">${kaf.join("")}</div>
    <div class="notatki"><h4 class="grupa-analizy">Notatki (${N.length})</h4>
      ${N.map(n => `<div class="notatka ${n.przypiete ? "przypieta" : ""}"><div>${esc(n.tekst).replace(/\n/g, "<br>")}</div>
        <small class="opis">${esc(n.kto)} · ${esc(n.czas)} · <a href="#" onclick="notatka('${n.id}', {przypiete: ${!n.przypiete}}); return false">${n.przypiete ? "odepnij" : "przypnij"}</a> ·
        <a href="#" onclick="notatka('${n.id}', {usun: true}); return false">do archiwum</a></small></div>`).join("") || '<p class="opis">Brak notatek – zapisz tu ustalenia, telefony, rzeczy do sprawdzenia.</p>'}
      <div class="pasek"><input id="nt-tekst" placeholder="Nowa notatka…" style="flex:1;min-width:220px" onkeydown="if (event.key === 'Enter') notatka()">
        <button class="zielony maly" data-ik="plus" onclick="notatka()">Dodaj</button></div></div></div>`;
}
async function notatka(id, zm) {
  const d = id ? {id, ...zm} : {tekst: $("#nt-tekst").value};
  const pidN = WIDOK === "realizacja" || WIDOK === "zam_realizacja" ? REAL_ID : PROJEKT_ID;
  if (await bezpiecznie(() => api(`/api/projekty/${pidN}/notatki`, {json: d}))) { if (pidN === REAL_ID && (WIDOK === "realizacja" || WIDOK === "zam_realizacja")) odswiezReal(); else otworzProjekt(PROJEKT_ID); }
}
function numerujKroki() {  // numeracja kroków projektu po kolei (1, 2, 3…) – bez ręcznego przesuwania numerów po dodaniu kroku
  let n = 0;
  document.querySelectorAll("#projekt > .krok").forEach(k => {
    const h = k.querySelector(":scope > .tytul h3"); if (!h || k.offsetParent === null) return;
    const m = h.innerHTML.match(/^\s*\d+\.\s/); if (!m) return;
    h.innerHTML = h.innerHTML.replace(/^\s*\d+\.\s/, `${++n}. `);
  });
}
function paskiSekcji(sel = "#projekt") {
  if (sel === "#projekt") numerujKroki();
  const szybki = !!document.querySelector(sel + ".widok-szybki");
  const kroki = [...document.querySelectorAll(`${sel} > .krok, ${sel} > .karta.przeglad`)].filter(k => (k.id || k.querySelector("h3")) && !(szybki && k.classList.contains("zaaw")));
  document.querySelectorAll(sel + " .pasek-sekcji").forEach(x => x.remove());
  if (kroki.length < 3) return;
  kroki.forEach((k, i) => { if (!k.id) k.id = (sel === "#projekt" ? "sek-" : "sek-r-") + i; });
  const pas = document.createElement("div"); pas.className = "pasek-sekcji";
  pas.innerHTML = kroki.map(k => `<a href="#${k.id}" onclick="document.getElementById('${k.id}').scrollIntoView({behavior:'smooth'}); return false">${esc((k.querySelector("h3")?.textContent || "").replace(/^\s*\d+\.\s*/, "").trim().slice(0, 34))}</a>`).join("");
  const nag = $(sel + " .naglowek"); nag && nag.after(pas);
}

function kartaRealizacji(R) {
  const RZ = R.projekt.strona === "zamawiajacy" ? (R.projekt.rodzaj_zamowienia || "roboty") : "roboty", U_ = RZ !== "roboty";
  const r = R.realizacja, hrf = r.hrf || {etapy: []}, odeb = hrf.etapy.filter(e => e.status === "odebrany").length;
  const otw = (r.usterki || []).filter(u => u.status === "otwarta" || u.status === "w toku").length;
  const N = (R.notatki || []).slice().sort((a, b) => (b.przypiete ? 1 : 0) - (a.przypiete ? 1 : 0) || b.czas.localeCompare(a.czas));
  return `<div class="karta przeglad"><div class="kwoty kafle-przetargu" style="margin-top:0">
      ${odliczanie(r.termin_zakonczenia, U_ ? "Wykonanie umowy" : "Zakończenie robót") || `<div><span>${U_ ? "Wykonanie umowy" : "Zakończenie robót"}</span><b>–</b><small>wpisz w danych umowy</small></div>`}
      <div><span>${RZ === "uslugi" ? "Odebrane okresy" : RZ === "dostawy" ? "Odebrane dostawy" : "Odbiory etapów"}</span><b>${odeb}/${hrf.etapy.length}</b><small>${hrf.etapy.length ? Math.round(odeb / hrf.etapy.length * 100) + "%" : "brak harmonogramu"}</small></div>
      <div><span>${U_ ? "Reklamacje i zadania" : "Usterki i zadania"}</span><b>${otw}</b><small>otwartych</small></div>
      ${R.przetarg && R.przetarg.link ? `<div><span>Przetarg</span><b><a href="${esc(R.przetarg.link)}" target="_blank" rel="noopener">ogłoszenie ↗</a></b><small>${esc((R.przetarg.przedmiot || "").slice(0, 60))}</small></div>` : ""}</div>
    <div class="notatki"><h4 class="grupa-analizy">Notatki (${N.length})</h4>
      ${N.map(n => `<div class="notatka ${n.przypiete ? "przypieta" : ""}"><div>${esc(n.tekst).replace(/\n/g, "<br>")}</div>
        <small class="opis">${esc(n.kto)} · ${esc(n.czas)} · <a href="#" onclick="notatka('${n.id}', {przypiete: ${!n.przypiete}}); return false">${n.przypiete ? "odepnij" : "przypnij"}</a> ·
        <a href="#" onclick="notatka('${n.id}', {usun: true}); return false">do archiwum</a></small></div>`).join("") || '<p class="opis">Brak notatek.</p>'}
      <div class="pasek"><input id="nt-tekst" placeholder="Nowa notatka (ustalenia, telefony, rzeczy do sprawdzenia)…" style="flex:1;min-width:220px" onkeydown="if (event.key === 'Enter') notatka()">
        <button class="zielony maly" data-ik="plus" onclick="notatka()">Dodaj</button></div></div></div>`;
}
// ---------- zamawiający: rodzaj zamówienia (roboty budowlane / usługi / dostawy)
const RODZ_ZAM = {roboty: "Roboty budowlane", uslugi: "Usługi", dostawy: "Dostawy (towary)"};
async function zmienRodzajZam(r) {
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/rodzaj-zamowienia`, {json: {rodzaj: r}}))) { komunikat(`Rodzaj zamówienia: ${RODZ_ZAM[r]}.`); odswiezProjekt(); }
}
// ================================================================ KREATOR ZAMÓWIENIA (zamawiający)
let KZN = {rodzaj: "", sciezka: ""};
let ZAM_PRYW = (() => { try { return localStorage.getItem("zam_prywatny") === "1"; } catch (e) { return false; } })();  // ścieżka wspólnot, spółdzielni, deweloperów
// Opis modułu zamawiającego: zamawiający publiczny (gmina, Pzp) albo wspólnota / spółdzielnia / deweloper (bez Pzp).
// Jedno miejsce różnic w interfejsie – reszta kodu pyta MZ() zamiast sprawdzać ZAM_PRYW (odpowiednik reguly_zamowien.py).
const MODULY_ZAM = {
  gmina: {klucz: "gmina", prywatny: false, ma_cele: true, cele_ukryte: [], menu: null, ukryte_w_menu: ["zam_zapytania"], nazwy_menu: {},
    kafle: null, kafel_kosztorys: false, plan_na_pulpicie: true, ochrona_ludnosci: true, ocena_wg_zapytan: false, nowa_inwestycja: false,
    realizacja_naglowek: "Realizacja umów", rozdzial_instrukcji: null, naglowek_pulpitu: "Dla Zamawiającego",
    tryby_dokumentacji: [["pzp_podstawowy", "SWZ – tryb podstawowy (ustawa Pzp)"], ["pzp_nieograniczony", "SWZ – przetarg nieograniczony (procedura unijna)"],
      ["konkurencyjnosc", "Zapytanie ofertowe – zasada konkurencyjności"], ["ponizej_130", "Zapytanie ofertowe – poniżej progu Pzp (170 000 zł netto)"]]},
  wspolnota: {klucz: "wspolnota", prywatny: true, ma_cele: false, cele_ukryte: ["plan", "olioc"],
    menu: ["pulpit", "zam_nowe", "zam_zapytania", "zam_oferty", "zam_realizacja"],
    ukryte_w_menu: ["olioc", "plan_spr", "plan_zam", "sprawozdanie", "kalk_pracy", "cel"],
    nazwy_menu: {zam_nowe: "Przygotuj zamówienie", zam_zapytania: "Moje zapytania", zam_oferty: "Sprawdź złożone oferty", zam_realizacja: "Realizuj umowę / inwestycje"},
    kafle: [["zam_nowe", "plus", "Przygotuj zamówienie", "Kreator: opis i szacunek kosztów, tryb, warunki, zapytanie ofertowe, wzór umowy, sprawdzenie dokumentów i lista kontrolna – bez Pzp.", "fiol"],
      ["zam_zapytania", "mail", "Moje zapytania", "Zapytania w przygotowaniu i rozesłane: termin i liczba ofert; na 5 dni przed terminem bez ofert – zaproszenia do firm z okolicy.", "nieb"],
      ["zam_oferty", "trofeum", "Sprawdź złożone oferty", "Oferty z zapytań: zgodność, ranking, rynkowość cen i dokładna weryfikacja wykonawców – referencje, doświadczenie, uprawnienia, polisa, rejestry.", "zolt"],
      ["zam_realizacja", "kask", "Realizuj umowę / inwestycje", "Umowy przeniesione z „Przygotuj zamówienie” albo dodane od razu: harmonogram, odbiory, faktury, rękojmia i finansowanie.", "ziel"]],
    kafel_kosztorys: true, plan_na_pulpicie: false, ochrona_ludnosci: false, ocena_wg_zapytan: true, nowa_inwestycja: true,
    realizacja_naglowek: "Realizuj umowę / inwestycje", rozdzial_instrukcji: 9, naglowek_pulpitu: "Dla wspólnot, spółdzielni i deweloperów",
    tryby_dokumentacji: [["prywatny", "Zapytanie ofertowe wspólnoty / spółdzielni / dewelopera (bez Pzp)"], ["konkurencyjnosc", "Zapytanie ofertowe – zasada konkurencyjności (gdy wymaga jej umowa o dofinansowanie)"]]},
};
function MZ() { return ZAM_PRYW ? MODULY_ZAM.wspolnota : MODULY_ZAM.gmina; }
function ustawZamPryw(v) { ZAM_PRYW = !!v; try { v ? localStorage.setItem("zam_prywatny", "1") : localStorage.removeItem("zam_prywatny"); } catch (e) {} }
function rysujZamNowe() {
  const O = [["roboty", "kask", "Roboty budowlane", "budowa, remont, termomodernizacja, drogi, sieci"], ["uslugi", "ludzie", "Usługi", "sprzątanie, ochrona, utrzymanie, projektowanie, transport, IT"],
             ["dostawy", "ciezarowka", "Dostawy", "sprzęt, meble, komputery, materiały, paliwo, żywność"]];
  $("#zam-nowe").innerHTML = `<div class="kreator-start">
    <h2>Nowe zamówienie</h2>
    <div class="karta" style="border-left:4px solid #1F5A99;margin:8px 0 14px"><b>Masz już dokumenty?</b> Lista lub wykaz potrzeb, ogłoszenie o zamówieniu, SWZ z poprzedniego postępowania, notatka, kosztorys –
      program odczyta z nich założenia, uzupełni kreator i zapyta tylko o to, czego brakuje.
      <div class="pasek" style="margin:8px 0 0"><label class="przycisk glowny" data-ik="wgraj">Wgraj dokumenty – program uzupełni resztę<input type="file" multiple hidden accept=".pdf,.docx,.doc,.xlsx,.xls,.csv,.txt,.jpg,.jpeg,.png,.zip" onchange="startZDokumentow(this.files)"></label></div></div>
    <h3 class="kz-pyt">1. Co chcesz zamówić?</h3>
    <div class="kz-kafle">${O.map(([k, i_, t, o]) => `<button class="kz-kafel ${KZN.rodzaj === k ? "akt" : ""}" onclick="KZN.rodzaj='${k}'; rysujZamNowe()"><span class="cel-ik">${ik(i_)}</span><b>${t}</b><small>${o}</small></button>`).join("")}</div>
    ${KZN.rodzaj ? `<label class="kz-lab">Opisz krótko, co zamawiasz (co, gdzie, na kiedy)
      <textarea id="kz-opis" placeholder="${{roboty: "np. Termomodernizacja budynku szkoły w Pszennie – ocieplenie ścian, wymiana okien, do września 2027", uslugi: "np. Sprzątanie 3 budynków urzędu przez 12 miesięcy od stycznia 2027", dostawy: "np. Dostawa i montaż 60 ławek i 120 krzeseł do szkoły do 20 sierpnia 2027"}[KZN.rodzaj]}">${esc(KZN.opis || "")}</textarea></label>
      <div class="siatka"><label>Nazwa zamówienia<input id="kz-nazwa" value="${esc(KZN.nazwa || "")}" placeholder="np. Termomodernizacja szkoły w Pszennie"></label>
        <label>Zamawiający (nazwa, adres) – opcjonalnie<input id="kz-zam" placeholder="np. Gmina Pszenno, ul. Szkolna 1"></label>
        <label>Orientacyjny budżet netto [zł] (opcjonalnie)<input id="kz-budzet" inputmode="decimal" value="${esc(KZN.budzet || "")}"></label></div>
      ${STRONA === "prawnik" ? `<label class="wiersz"><input type="checkbox" id="kz-pryw" ${KZN.prywatny ? "checked" : ""}> Dokumenty dla wspólnoty / inwestora prywatnego (bez Pzp)</label>` : ""}
      <h3 class="kz-pyt">2. Czy masz własne wzory dokumentów?</h3>
      <div class="kz-kafle kz-2">
        <button class="kz-kafel" onclick="startKreatora('wzory')"><span class="cel-ik">${ik("wgraj")}</span><b>Tak, mam swoje wzory</b><small>Wgrasz SWZ / zapytanie, OPZ, umowę – program dopasuje je do zamówienia, sprawdzi i zaproponuje zmiany do akceptacji.</small></button>
        <button class="kz-kafel" onclick="startKreatora('nowe')"><span class="cel-ik">${ik("iskra")}</span><b>Nie – przygotuj wszystko od początku</b><small>Program zapyta o szczegóły, policzy wartość, dobierze tryb i przygotuje komplet dokumentów krok po kroku.</small></button></div>` : ""}
  </div>`;
  wstawIkony($("#zam-nowe"));
}
async function startKreatora(sciezka) {
  const opis = $("#kz-opis").value.trim(), nazwa = $("#kz-nazwa").value.trim();  // pusta nazwa = nazwa tymczasowa z opisu (nadaje serwer)
  if (!opis) return komunikat("Opisz krótko, co zamawiasz.", true);
  const dane = {rodzaj: KZN.rodzaj, opis, nazwa, budzet: $("#kz-budzet").value, sciezka, prywatny: STRONA === "prawnik" ? !!($("#kz-pryw") || {}).checked : MZ().prywatny, zamawiajacy: $("#kz-zam").value, prawnik: STRONA === "prawnik", plan: KZN.plan || undefined};
  const p = await zalozZamowienie(dane); if (!p) return;
  KZN = {rodzaj: "", sciezka: ""}; TRYB = "zamowienie"; PROJEKT_ID = p.id; pokaz("zam_projekty");
}
// Założenie zamówienia z ostrzeżeniem o powtórzeniu (ta sama pozycja planu albo nazwa): można otworzyć istniejące albo założyć nowe.
async function zalozZamowienie(dane) {
  dane = dane.json || dane;
  try { return await api("/api/zam/kreator", {json: dane}); }
  catch (e) {
    const pw = (e.dane || {}).powtorzenie;
    if (!pw) { komunikat(e.message, true); return null; }
    if (!confirm(`Takie zamówienie już istnieje: „${pw.nazwa}” (${pw.powod}).\n\nOK – załóż mimo to nowe (np. powtórzone postępowanie)\nAnuluj – otwórz istniejące`)) { TRYB = "zamowienie"; PROJEKT_ID = pw.id; pokaz("zam_projekty"); return null; }
    return await bezpiecznie(() => api("/api/zam/kreator", {json: {...dane, potwierdz_powtorzenie: true}}));
  }
}
async function startZDokumentow(files) {
  if (!files.length) return;
  const nazwy = [...files].map(f => f.name).join(", ");
  const p = await bezpiecznie(() => api("/api/zam/kreator", {json: {rodzaj: KZN.rodzaj || "roboty", opis: "", nazwa: "Nowe zamówienie (z dokumentów)", sciezka: "nowe", prawnik: STRONA === "prawnik", z_dokumentow: true,
    prywatny: STRONA === "prawnik" ? false : MZ().prywatny}})); if (!p) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); if (!KZN.rodzaj) fd.append("rodzaj_z_importu", "1");
  const z = await bezpiecznie(() => api(`/api/projekty/${p.id}/kreator/zrodla`, {method: "POST", body: fd})); if (!z) return;
  KZN = {rodzaj: "", sciezka: ""}; TRYB = "zamowienie"; PROJEKT_ID = p.id; KZ_AKT = null; pokaz("zam_projekty");
  komunikat((z.pominiete || []).length ? `Limit to 10 plików na jedno wgranie – pominięto: ${z.pominiete.join(", ")}. Wgraj je osobno.` : "Odczytuję założenia z: " + nazwy + " – kreator uzupełni się za chwilę.", !!(z.pominiete || []).length);
  sledz(z, () => { KZ_AKT = null; odswiezProjekt(); });
}
async function noweZamowienie(rodzaj) { KZN.rodzaj = rodzaj; pokaz("zam_nowe"); }
// ---------- panel kreatora w projekcie zamówienia
let KZ = null;
async function ladujKosztyZadan() {
  const [d, ZU] = await Promise.all([api("/api/koszty-zadan").catch(() => null), api("/api/zuzycie-ai").catch(() => ({konta: []}))]); const el = $("#koszty-zadan"); if (!d || !el) return;
  const konta = (ZU.konta || []).map(k => k.konto).filter(Boolean);
  el.innerHTML = `${d.najdrozsze.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Data</th><th>Konto</th><th>Zadanie</th><th>Koszt</th></tr>
      ${d.najdrozsze.map(x => `<tr><td>${esc(x.data)}</td><td>${esc(x.konto)}</td><td>${esc(x.opis)}<br><small class="opis">${esc(NAZWY_ZADAN[x.typ] || x.typ)}</small></td><td class="liczba">${zl(x.zl)}</td></tr>`).join("")}</table></div>`
      : '<p class="pusto">Brak zadań z kosztem AI w tym miesiącu.</p>'}
    <h4 class="grupa-analizy">Miesięczny limit kosztów AI na konto</h4>
    <p class="opis">Po przekroczeniu limitu program zablokuje zadania AI na tym koncie do końca miesiąca (0 albo puste = bez limitu).</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Konto</th><th>Wykorzystano</th><th>Limit [zł / mies.]</th><th></th></tr>
      ${(ZU.konta || []).map(k => { const lim = d.limity[k.konto] || ""; const uz = k.biezacy_zl || 0; const pr = lim ? uz / lim : 0;
        return `<tr><td>${esc(k.konto)}</td><td class="liczba ${pr >= 1 ? "czerwone" : pr >= 0.8 ? "pilne" : ""}">${zl(uz)}${lim ? ` (${Math.round(pr * 100)}%)` : ""}</td>
          <td><input style="width:110px" inputmode="decimal" id="lim-${esc(k.konto)}" value="${esc(String(lim))}"></td>
          <td><button class="maly" onclick="zapiszLimit('${escA(k.konto)}')">Zapisz</button></td></tr>`; }).join("")}</table></div>`;
}
async function zapiszLimit(konto) {
  const r = await bezpiecznie(() => api("/api/koszty-zadan/limit", {json: {konto, limit: document.getElementById("lim-" + konto).value}})); if (r) { komunikat("Zapisano limit."); ladujKosztyZadan(); }
}
async function licznikTokenow() {
  const el = $("#licznik-ai"); if (!el || !PROJEKT_ID) return;
  const t = await api(`/api/projekty/${PROJEKT_ID}/tokeny`).catch(() => null); if (!t || !t.calosc) return;
  const tys = x => (x / 1000).toLocaleString("pl-PL", {maximumFractionDigits: 0}) + " tys.";
  el.innerHTML = `Do AI: ok. <b>${tys(t.calosc)} tokenów</b> (kosztorys)${t.tekstowe !== t.calosc ? ` · zadania tekstowe: <b>${tys(t.tekstowe)}</b>` : ""}${t.rysunki_pominiete ? ` · pomijane rysunki: ${t.rysunki_pominiete}` : ""}`;
  el.title = "Największe pliki: " + t.pliki.slice(0, 6).map(f => `${f.plik} – ${tys(f.tokeny)} (${f.rodzaj})`).join("; ");
}
async function ladujKreator() { if (!$("#kreator-zam") || !PROJEKT_ID) { FOKUS_KZ = null; return; } KZ = await api(`/api/projekty/${PROJEKT_ID}/kreator`).catch(() => null);
  if (KZ && FOKUS_KZ) { KZ_AKT = FOKUS_KZ; FOKUS_KZ = null; FOKUS = null; setTimeout(() => $("#kreator-zam")?.scrollIntoView({behavior: "smooth"}), 300); }  // kafelek → krok kreatora
  if (KZ) rysujKreator(); }
const KZ_GOTOWE = S => S && S.prywatny ? "Gotowe do wysłania" : "Gotowe do publikacji";
function krokiKreatora(S) {
  const nowe = S.sciezka !== "wzory";
  return (nowe ? [["opis", "Co zamawiasz"], ["potrzeba", "Szczegóły"], ["wartosc", "Wartość i tryb"], ["warunki", "Warunki"], ["dokumenty", "Komplet dokumentów"], ["zmiany", "Sprawdzenie i zmiany"], ["gotowe", "Gotowe do publikacji"]]
    : [["opis", "Co zamawiasz"], ["wzory", "Twoje wzory"], ["wartosc", "Wartość i tryb"], ["warunki", "Warunki"], ["zmiany", "Sprawdzenie i zmiany"], ["gotowe", "Gotowe do publikacji"]]).map(([k, t]) => [k, k === "gotowe" ? KZ_GOTOWE(S) : t]);
}
function stanKroku(S, id) {
  if (S.kroki_ok && id in S.kroki_ok) return !!S.kroki_ok[id];  // zaliczenie kroków liczy serwer (jedne reguły dla ekranu i dokumentów)
  // zamawiający publiczny: wartość dopiero po szacowaniu (art. 28–36 Pzp), nie z budżetu orientacyjnego; komplet – z dokumentami głównymi (SWZ, umowa)
  const wart = S.netto > 0 && !S.rozbieznosc_wartosci && (S.prywatny || S.netto_zrodlo === "szacowanie");
  return {opis: !!S.K.opis, potrzeba: Object.values(S.K.potrzeba || {}).some(Boolean), wzory: S.wzory.length > 0, wartosc: wart,
          warunki: Object.keys(S.K.warunki || {}).length > 0, dokumenty: S.dokumenty_gotowe ?? S.dokumenty.length > 0, zmiany: kzZatwierdzone(S), gotowe: false}[id];
}
// krok 6 zakończony: lista rozstrzygnięta i zatwierdzona po ostatnim sprawdzeniu (ponowne sprawdzenie otwiera krok od nowa)
const kzZatwierdzone = S => S.koncowe.length > 0 && (!S.K.przeglad_nr || S.K.zatwierdzony_nr === S.K.przeglad_nr);
let KZ_AKT = null;
// „Szczegóły”: puste pola podpowiadane z opisu z pierwszego kroku (zakres, termin) – do poprawienia przed zapisem
function kzZOpisu(S, id) {
  const o = String(S.K.opis || ""); if (!o) return "";
  if (["zakres", "przedmiot", "co"].includes(id)) return o;
  if (["termin", "okres"].includes(id)) return S.termin_z_opisu || "";  // rozpoznanie terminu – jedna reguła na serwerze (daty i nazwy miesięcy)
  return "";
}
// komunikaty kontroli kroku (błędy, ostrzeżenia, informacje) – wyliczane na serwerze
function kzKomunikaty(S, krok) {
  const L = (S.komunikaty || {})[krok] || []; if (!L.length) return "";
  const B = L.filter(x => x.waga === "blad"), O = L.filter(x => x.waga === "ostrzezenie"), I = L.filter(x => x.waga === "info");
  const lista = (t, A, kl) => A.length ? `<div class="${kl}" style="margin:0 0 10px"><b>${t}</b><ul class="lista" style="margin:4px 0 0">${A.map(x => `<li>${esc(x.opis)}</li>`).join("")}</ul></div>` : "";
  if (krok === "gotowe") return (S.gotowosc || {}).gotowe ? `<div class="karta" style="border-left:4px solid #16a34a;margin:0 0 10px"><b>${S.prywatny ? "Gotowe do wysłania" : "Gotowe do publikacji"}.</b></div>`
    : lista(`Niegotowe – przed ${S.prywatny ? "wysłaniem" : "publikacją"} uzupełnij (${O.length}):`, O, "ramka-uwaga");
  return lista("Do poprawienia:", B, "ramka-uwaga") + lista("Uwagi:", O, "ramka-uwaga") + (I.length ? `<p class="opis" style="margin:0 0 8px">${I.map(x => esc(x.opis)).join(" ")}</p>` : "");
}
async function kzDoDecyzji(nr, ok) { const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/do-decyzji`, {json: {nr, ok}})); if (r) { KZ = r; rysujKreator(); } }
async function kzPotwierdzTryb(pole, kod, krytyczna) {
  const dane = {[pole]: kod};
  if (krytyczna) { const u = prompt("To różnica krytyczna. Wpisz uzasadnienie (np. podstawa wyłączenia stosowania ustawy) – trafi do dokumentacji:", (KZ.K || {}).tryb_uzasadnienie || ""); if (u === null) return; dane.tryb_uzasadnienie = u; }
  zapiszKreator(dane);
}
function rysujKreator() {
  const S = KZ, kroki = krokiKreatora(S);
  if (!KZ_AKT || !kroki.some(k => k[0] === KZ_AKT)) KZ_AKT = (kroki.find(k => !stanKroku(S, k[0])) || kroki[kroki.length - 1])[0];
  const IMP = (S.import || {}).pola || {};
  const zr = pole => { const x = IMP[pole]; return x ? `<small class="kz-zr ${x.do_aktualizacji ? "kz-akt" : ""}">${x.do_aktualizacji ? "⚠ do aktualizacji – " : ""}${x.zmienione ? "poprawione · " : ""}z dokumentu: ${esc(x.zrodlo || "")}</small>` : ""; };
  const wymag = id => (S.wymagane_szczegoly || []).includes(id) ? ' <b class="czerwone" title="pole wymagane">*</b>' : "";
  const pyt = ([id, et0, typ, op], _i, _a, et = et0) => typ === "wybor" ? `<label>${esc(et)}<select data-kzp="${id}"><option value=""></option>${op.map(o => `<option ${o === (S.K.potrzeba || {})[id] ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`
    : typ === "dlugi" ? `<label style="grid-column:1/-1">${esc(et)}${wymag(id)}<textarea data-kzp="${id}" maxlength="${(S.limity || {}).dlugi || 10000}" placeholder="${esc(op || "")}">${esc((S.K.potrzeba || {})[id] || kzZOpisu(S, id))}</textarea>${zr("potrzeba." + id)}</label>`
    : `<label>${esc(et)}${wymag(id)}<input data-kzp="${id}" maxlength="${(S.limity || {}).krotki || 500}" placeholder="${esc(op || "")}" value="${esc((S.K.potrzeba || {})[id] || kzZOpisu(S, id))}">${zr("potrzeba." + id)}</label>`;
  const pomK = k => S.pomoc[k] ? `<button type="button" class="pom-ik" title="${esc(S.pomoc[k])}" onclick="komunikat(${jsa(S.pomoc[k])})">?</button>` : "";
  const ETW = {wynagrodzenie: "Wynagrodzenie", kryteria: "Kryteria oceny ofert", warunki: "Warunki udziału", gwarancja: "Gwarancja", kary: "Kary umowne", wadium: "Wadium",
               zabezpieczenie: "Zabezpieczenie należytego wykonania", platnosci: "Płatności", waloryzacja: "Waloryzacja wynagrodzenia", podwykonawstwo: "Podwykonawstwo",
               czesci: "Podział na części", klauzule: "Klauzule społeczne / środowiskowe", platforma: "Sposób składania ofert", kontakt: "Osoba do kontaktu"};
  if ("wykluczenie" in (S.warunki || {})) ETW.wykluczenie = "Fakultatywne podstawy wykluczenia (art. 109 ust. 1 Pzp)";  // tylko tryby Pzp
  if ("jedz" in (S.warunki || {})) ETW.jedz = "JEDZ – część IV (kryteria kwalifikacji)";  // tylko procedura unijna
  const plk = (f, kat) => `<a href="/pobierz/${S.projekt.id}/${kat ? kat + "/" : ""}${encodeURIComponent(f)}">${esc(f)}</a>`;
  const tresc = {
    opis: `${(() => { const im = S.import || {}, ile = Object.keys(im.pola || {}).length; return `<div class="karta" style="margin:0 0 12px;padding:10px 14px;border-left:4px solid #1F5A99">
        <b>Uzupełnij z dokumentów</b> <span class="opis">– lista potrzeb, ogłoszenie, SWZ, notatka, kosztorys. Program wypełnia tylko puste pola; Twoich wpisów nie nadpisuje.</span>
        <div class="pasek" style="margin:6px 0 0"><label class="przycisk maly glowny" data-ik="wgraj">Wgraj dokumenty<input type="file" multiple hidden accept=".pdf,.docx,.doc,.xlsx,.xls,.csv,.txt,.jpg,.jpeg,.png,.zip" onchange="kzZrodla(this.files)"></label>
          ${S.zrodla.length ? `<span class="opis" style="margin:0">Wgrane: ${S.zrodla.map(esc).join(", ")}</span>` : ""}
          <button class="maly" data-ik="przelacz" onclick="kzOdczytajPonownie()" title="Odczyt dokumentów już wgranych do projektu – wartość, zakres, ilości; różnice z danymi w kreatorze do wyboru">Odczytaj ponownie wgrane dokumenty</button></div>
        ${ile ? `<p class="opis" style="margin:6px 0 0">Uzupełniono z dokumentów <b>${ile}</b> pól (${esc(im.data || "")})${im.archiwalny ? " · <b>dokument z wcześniejszego postępowania – daty, terminy, kwoty i znak sprawy oznaczone „do aktualizacji”</b>" : ""}.</p>` : ""}
        ${(im.uwagi || []).length ? `<ul class="lista">${im.uwagi.map(u => `<li>${esc(u)}</li>`).join("")}</ul>` : ""}
        ${(im.nieodczytane || []).length ? `<div class="ramka-uwaga"><b>Nie odczytano ${im.nieodczytane.length} plików</b> – ich treść nie została uwzględniona (np. ilości z przedmiaru). Zapisz je jako PDF z tekstem, Word lub Excel i wgraj ponownie:
          <ul class="lista">${im.nieodczytane.map(x => `<li>${esc(x.plik)} <small class="opis">– ${esc(x.powod)}</small></li>`).join("")}</ul></div>` : ""}
        ${(im.sprzecznosci || []).length ? `<div class="ramka-uwaga"><b>Dokumenty podają inne wartości niż kreator albo różnią się między sobą – wybierz właściwą:</b>${im.sprzecznosci.map(s_ => `<div style="margin:6px 0"><b>${esc(kzEtykieta(s_.pole))}</b>
          ${s_.warianty.map(v => `<div class="pasek" style="margin:2px 0"><button class="maly" onclick="kzSprzecznosc('${escA(s_.pole)}', ${jsa(String(v.wartosc))})">Przyjmij</button><span>${esc(String(v.wartosc).slice(0, 160))} <small class="opis">(${esc(v.zrodlo || "")})</small></span></div>`).join("")}</div>`).join("")}</div>` : ""}</div>`; })()}
      <div class="siatka"><label style="grid-column:1/-1">Nazwa zamówienia<input id="kz-e-nazwa" value="${esc(S.projekt.nazwa || "")}">${zr("co.nazwa")}</label>
        <label style="grid-column:1/-1">Zamawiający (nazwa, adres, NIP) – trafia do dokumentów<input id="kz-e-zam" value="${esc(S.K.zamawiajacy || "")}" placeholder="np. Gmina Pszenno, ul. Szkolna 1, 58-100 Pszenno, NIP …">${zr("co.zamawiajacy")}
          ${S.profil_firmy ? `<button type="button" class="maly" style="margin-top:4px" onclick="$('#kz-e-zam').value=${jsa(S.profil_firmy)}">Wstaw dane z profilu firmy (gdy to Ty jesteś zamawiającym)</button>` : ""}</label>
        <label style="grid-column:1/-1">Co zamawiasz (opis)<textarea id="kz-e-opis">${esc(S.K.opis || "")}</textarea>${zr("co.opis")}</label>
        <label>Rodzaj<select id="kz-e-rodzaj">${Object.entries({roboty: "Roboty budowlane", uslugi: "Usługi", dostawy: "Dostawy"}).map(([k, v]) => `<option value="${k}" ${k === S.rodzaj ? "selected" : ""}>${v}</option>`).join("")}</select></label>
        <label>Dokumenty<select id="kz-e-sciezka"><option value="nowe" ${S.sciezka !== "wzory" ? "selected" : ""}>przygotuj od początku</option><option value="wzory" ${S.sciezka === "wzory" ? "selected" : ""}>mam swoje wzory</option></select></label></div>
      <div class="pasek"><button class="glowny" onclick="zapiszKreator({nazwa: $('#kz-e-nazwa').value, opis: $('#kz-e-opis').value, rodzaj: $('#kz-e-rodzaj').value, sciezka: $('#kz-e-sciezka').value, zamawiajacy: $('#kz-e-zam').value}, 1)">Zapisz i dalej →</button></div>`,
    potrzeba: `<p class="opis">Odpowiedz na pytania – na tej podstawie program policzy wartość i przygotuje dokumenty. Wgraj też, co masz: projekt, przedmiar, wykaz potrzeb, zdjęcia.</p>
      <div class="siatka">${S.pytania.map(pyt).join("")}</div>
      <div class="pasek"><label class="przycisk maly" data-ik="wgraj">Wgraj dokumenty (projekt, przedmiar, wykaz)<input type="file" multiple hidden onchange="wgrajPliki(this.files)"></label>
        <button class="glowny" onclick="zapiszKreator({potrzeba: zbierzKz('kzp')}, 1)">Zapisz i dalej →</button></div>`,
    wzory: `<p class="opis">Wgraj swoje wzory – Word (.docx) albo PDF: SWZ albo zapytanie ofertowe, OPZ, wzór umowy, formularz ofertowy, oświadczenia. PDF z tekstem program zamienia na Word („… (z PDF).docx”), żeby zaakceptowane zmiany wprowadzić automatycznie. Skany bez tekstu – zmiany do ręcznego wprowadzenia.</p>
      <h4 class="grupa-analizy">Wzory w tym zamówieniu (${S.wzory.length})</h4>
      ${S.wzory.length ? `<ul class="lista">${S.wzory.map(f => `<li>${plk(f, "wzory")} <button class="maly" onclick="usunWzorKz('${escA(f)}')">usuń z zamówienia</button></li>`).join("")}</ul>` : '<p class="pusto">Brak wzorów – wgraj swoje albo dodaj z biblioteki.</p>'}
      ${(S.biblioteka_wg || []).length ? `<details ${S.wzory.length ? "" : "open"}><summary><b>Biblioteka „Moje wzory” (${S.biblioteka_wg.length})</b> – dodaj wybrane do tego zamówienia</summary>
        <ul class="lista">${S.biblioteka_wg.map(([r, f]) => `<li>${esc(f)} ${S.wzory.includes(f) ? '<span class="znacznik z-startujemy">w zamówieniu</span>' : `<button class="maly glowny" onclick="wzorZBiblioteki('${r}', '${escA(f)}')">Dodaj do tego zamówienia</button>`}
          <button class="maly niebezp" onclick="usunZBiblioteki('${r}', '${escA(f)}')">usuń z biblioteki</button></li>`).join("")}</ul></details>` : ""}
      <div class="pasek"><label class="przycisk" data-ik="wgraj">Wgraj wzory<input type="file" multiple accept=".docx,.doc,.pdf,.odt" hidden onchange="wgrajWzoryKz(this.files)"></label>
        <label class="wiersz" style="margin:0" title="Zaznacz tylko dla wzorów ogólnych – nie dla dokumentów konkretnego postępowania"><input type="checkbox" id="kz-bibl"> zapisz też w bibliotece „Moje wzory” (tylko wzory ogólne, do kolejnych zamówień)</label>
        ${S.wzory.length ? `<button class="glowny" onclick="KZ_AKT='wartosc'; rysujKreator()">Dalej →</button>` : ""}</div>`,
    wartosc: `<div class="kwoty kafle-przetargu"><div><span>Wartość netto</span><b>${S.netto ? zl(S.netto) : "–"}</b><small>${({szacowanie: S.rodzaj === "roboty" ? (((S.szacowanie || {}).podstawa || "") === "kosztorys_inwestorski" ? "z kosztorysu inwestorskiego" : "z planowanych kosztów (PFU)") : "z szacowania (źródła cen)",
        dokumenty: "z dokumentów", szacunek_ai: "szacunek kosztów (AI)", reczna: "wpisana – bez udokumentowanej podstawy", budzet: "budżet orientacyjny"})[S.netto_zrodlo] || ""}</small></div>
        <div><span>W euro</span><b>${S.tryb_info.euro ? S.tryb_info.euro.toLocaleString("pl-PL") + " €" : "–"}</b>${S.rozbieznosc_wartosci ? '<small>z wartości w dokumentach (podstawa trybu)</small>' : ""}</div><div style="grid-column:span 2"><span>Tryb</span><b style="font-size:15px">${esc(S.tryb_opis)}</b></div></div>
      <p class="opis">${esc(S.tryb_info.opis)}</p>${zr("wartosc") ? `<p style="margin:0 0 6px">${zr("wartosc")}</p>` : ""}
      ${S.prywatny ? "" : `<div class="pasek" style="margin:0 0 8px"><label style="margin:0">Zamawiający <select onchange="zapiszKreator({typ_zamawiajacego: this.value})" title="Od rodzaju zamawiającego zależy próg unijny dla dostaw i usług: samorządowy 216 000 euro, centralny 140 000 euro">
          <option value="samorzadowy" ${S.typ_zamawiajacego !== "centralny" ? "selected" : ""}>samorządowy i pozostali (216 000 €)</option><option value="centralny" ${S.typ_zamawiajacego === "centralny" ? "selected" : ""}>centralny (140 000 €)</option></select></label>
        ${S.rodzaj === "uslugi" ? `<label class="wiersz" style="margin:0"><input type="checkbox" ${S.uslugi_spoleczne ? "checked" : ""} onchange="zapiszKreator({uslugi_spoleczne: this.checked})"> usługi społeczne i inne szczególne usługi (próg 750 000 €)</label>` : ""}</div>`}
      ${S.rozbieznosc_wartosci ? (() => { const r = S.rozbieznosc_wartosci; return `<div class="ramka-uwaga" style="border-color:#DC2626;background:#FEF2F2">
        <b>Wartość w dokumentach różni się od kosztorysu ${r.krotnosc}×</b><br>
        Dokumenty: <b>${zl(r.dokumenty)}</b> netto <small class="opis">(${esc(r.zrodlo)})</small> · kosztorys inwestorski: <b>${zl(r.kosztorys)}</b> netto.<br>
        Do Twojej decyzji <b>tryb jest liczony z wartości z dokumentów</b>. Sprawdź kosztorys – najczęściej ma niepełny zakres albo ilości z innego zamówienia.
        <div class="pasek" style="margin:6px 0 0"><button class="glowny" onclick="zapiszKreator({wartosc_decyzja: 'dokumenty'})">Przyjmij wartość z dokumentów</button>
          <button class="maly" onclick="if (confirm('Przyjąć wartość z kosztorysu? Wartość w ogłoszeniu i dokumentach trzeba będzie zmienić.')) zapiszKreator({wartosc_decyzja: 'kosztorys'})">Przyjmij kosztorys (dokumenty do zmiany)</button></div></div>`; })()
        : S.wartosc_dok ? `<p class="opis" style="margin:0 0 6px">Wartość podana w dokumentach: <b>${zl(S.wartosc_dok)}</b> netto${S.wartosc_decyzja ? ` · przyjęto: ${S.wartosc_decyzja === "dokumenty" ? "wartość z dokumentów" : "kosztorys"} <a href="#" onclick="zapiszKreator({wartosc_decyzja: ''}); return false">zmień</a>` : ""}</p>` : ""}
      ${S.prywatny ? `<label class="ks-pole" style="margin:6px 0;max-width:560px">Zamawiający <select onchange="zapiszKreator({podmiot: this.value})">${Object.entries(S.podmioty || {}).map(([k, t]) => `<option value="${k}" ${k === S.podmiot ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
        <p class="opis" style="margin:0 0 6px">Od rodzaju zamawiającego zależy, jaka zgoda jest potrzebna na prace (uchwała właścicieli, zgoda współwłaścicieli w małej wspólnocie, organ spółdzielni).</p>` : ""}
      <label class="ks-pole" style="margin:6px 0;max-width:560px">Tryb postępowania
        <select onchange="zapiszKreator({tryb_wybrany: this.value})">${S.prywatny ? "" : `<option value="">Automatycznie z wartości – ${esc(S.tryb_z_wartosci_opis || "")}</option>`}
          ${Object.entries(S.tryby_wybor || {}).map(([k, t]) => `<option value="${k}" ${S.tryb_wybrany === k ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
      ${S.rozbieznosc_wyboru ? (() => { const r = S.rozbieznosc_wyboru; return `<div class="ramka-uwaga" style="${r.waga === "krytyczna" ? "border-color:#DC2626;background:#FEF2F2" : ""}">
        <b>Wybrany tryb a wartość zamówienia</b><br>Wybrany: <b>${esc(r.dokumenty || "")}</b> · z wartości: <b>${esc(r.z_wartosci || "")}</b><br>${esc(r.ocena || "")}
        <div class="pasek" style="margin:6px 0 0"><button class="maly" onclick="kzPotwierdzTryb('tryb_wybor_decyzja', '${escA(r.kod_wyboru || "")}', ${r.waga === "krytyczna"})">Wybór trybu jest świadomy – odnotuj${r.waga === "krytyczna" ? " (z uzasadnieniem)" : ""}</button></div></div>`; })() : ""}
      ${S.rozbieznosc_trybu ? (() => { const r = S.rozbieznosc_trybu; return `<div class="ramka-uwaga" style="${r.waga === "krytyczna" ? "border-color:#DC2626;background:#FEF2F2" : ""}">
        <b>Tryb w dokumentach różni się od trybu wynikającego z wartości</b><br>
        Dokumenty: <b>${esc(r.dokumenty || "")}</b>${r.cytat ? ` <small class="opis">(„…${esc(r.cytat.slice(0, 160))}…”)</small>` : ""}<br>
        Z wartości zamówienia: <b>${esc(r.z_wartosci || "")}</b><br>${esc(r.ocena || "")}
        <div class="pasek" style="margin:6px 0 0"><button class="maly" onclick="kzPotwierdzTryb('tryb_decyzja', '${escA(r.kod_dok || "")}', ${r.waga === "krytyczna"})">Tryb z dokumentów jest świadomym wyborem – odnotuj${r.waga === "krytyczna" ? " (z uzasadnieniem)" : ""}</button></div></div>`; })()
        : S.tryb_dok ? `<p class="opis" style="margin:0 0 6px">Tryb w dokumentach: <b>${esc(S.tryb_dok)}</b>${S.K.tryb_decyzja ? ` · potwierdzony przez zamawiającego <a href="#" onclick="zapiszKreator({tryb_decyzja: ''}); return false">cofnij</a>` : ""}</p>` : ""}
      ${S.rodzaj !== "roboty" ? `<label style="display:block;margin:6px 0">Zakres ilościowy w całym okresie umowy (jeśli nie ma go w dokumentach)
        <textarea id="kz-ilosci" placeholder="np. przerwy kawowe – 2622 porcje; obiady dwudaniowe – 606 porcji" onchange="zapiszKreator({potrzeba: {ilosci: this.value}})">${esc((S.K.potrzeba || {}).ilosci || "")}</textarea></label>` : ""}
      ${S.prywatny ? `<div class="pasek"><button class="zolty" data-ik="iskra" onclick="kosztorysKreatora()">${S.z_kosztorysu ? "Przelicz szacunek kosztów (AI)" : "Szacunek kosztów (AI)"}</button>
        <span class="opis" style="margin:0">albo</span><input id="kz-wart" inputmode="decimal" placeholder="wpisz wartość netto" style="width:170px" value="${esc(S.K.wartosc_reczna || "")}">
        <button class="maly" onclick="zapiszKreator({wartosc_reczna: $('#kz-wart').value})">Zapisz</button></div>
        <p class="opis" style="margin:2px 0 6px">Zamawiający prywatny (bez Pzp): szacunek kosztów przygotowany przez AI jest pomocniczy – nie jest kosztorysem inwestorskim.</p>
      <div class="pasek">${S.kosztorys ? plk(S.kosztorys) : ""}<button class="maly" data-ik="dokument" onclick="notatkaSzacowania()">Notatka z szacowania (Word)</button>
        <label class="maly" style="margin:0">Data wszczęcia <input type="date" value="${esc(S.K.data_wszczecia || "")}" onchange="zapiszKreator({data_wszczecia: this.value})"></label>
        ${S.netto ? `<button class="glowny" onclick="KZ_AKT='warunki'; rysujKreator()">Dalej →</button>` : ""}</div>` : szacPanel(S)}${kzCzesci(S)}`,
    warunki: `<p class="opis">Ustawienia domyślne są bezpieczne dla trybu „${esc(S.tryb_opis)}” – zmień, co chcesz. Przy każdym polu „?” wyjaśnia, co to znaczy.</p>
      <div class="siatka">${Object.entries(ETW).map(([k, et]) => `<label style="${["warunki", "kryteria", "kary"].includes(k) ? "grid-column:1/-1" : ""}"><span class="lab-pom">${et}${pomK(k)}</span>
        ${["warunki", "kryteria", "kary", "platnosci"].includes(k) ? `<textarea data-kzw="${k}">${esc(S.warunki[k] || "")}</textarea>` : `<input data-kzw="${k}" value="${esc(S.warunki[k] || "")}">`}${zr("warunki." + k) || ((S.K.warunki || {})[k] ? "" : '<small class="kz-zr">propozycja programu</small>')}</label>`).join("")}
        <label>Znak sprawy<input id="kz-znak" value="${esc(S.K.znak || "")}"></label><label>Termin składania ofert<input type="date" id="kz-termin" value="${esc(S.K.termin_ofert || "")}"></label>
        <label title="Otwarcie ofert program ustawia 30 minut później tego samego dnia">Godzina<input type="time" id="kz-godz" value="${esc(S.K.godzina_ofert || "")}" style="width:110px"></label></div>
      <p class="opis">Minimalny termin składania ofert: ${esc(S.min_dni_opis)}.</p>
      <details class="karta" id="kz-fin" style="margin:10px 0;padding:8px 14px;border-left:4px solid #7c3aed" ${(S.finansowanie || {}).liczba ? "open" : ""}>
        <summary><b>Finansowanie: kredyt, premia BGK, KPO, dotacja</b> <span class="opis" id="kzfin-stan">${(S.finansowanie || {}).liczba ? esc(S.finansowanie.opis) : "opcjonalnie"}</span></summary>
        <div id="kzfin-tresc"><p class="opis">Ładuję…</p></div></details>
      <div class="pasek"><button class="glowny" onclick="zapiszKreator({warunki: zbierzKz('kzw'), znak: $('#kz-znak').value, termin_ofert: $('#kz-termin').value, godzina_ofert: $('#kz-godz').value}, 1)">Zapisz i dalej →</button></div>`,
    dokumenty: `<p class="opis">Program przygotuje dokumenty dobrane do trybu (${esc(S.tryb_opis)}) z Twoich odpowiedzi, kosztorysu i wgranych materiałów.</p>
      ${(KZ.wzory || []).length ? `<p class="opis">Własne wzory (${KZ.wzory.length}) zostaną użyte jako podstawa – program zachowa ich układ i sformułowania: ${esc(KZ.wzory.join(", "))}.</p>` : ""}
      <div class="pasek" style="flex-wrap:wrap">${(S.komplet || [["swz", "SWZ / zapytanie ofertowe"], ["opz", "Opis przedmiotu zamówienia"], ["umowa", "Wzór umowy"], ["formularz", "Formularz ofertowy"], ["oswiadczenia", "Oświadczenia i wykazy"]]).map(([k, t]) =>
        `<label class="wiersz" style="margin:0"><input type="checkbox" class="kz-dok" value="${k}" checked> ${t}</label>`).join("")}
        ${S.rodzaj !== "roboty" ? `<label class="wiersz" style="margin:0"><input type="checkbox" id="kz-form" checked> Formularz cenowy dla wykonawców (pusty)</label>` : ""}</div>
      <div class="pasek"><button class="zolty" data-ik="iskra" onclick="dokumentyKreatora()">${S.dokumenty.length ? "Przygotuj ponownie (AI)" : "Przygotuj komplet dokumentów (AI)"}</button></div>
      ${S.dokumenty.length ? `<ul class="lista">${S.dokumenty.map(f => `<li>${plk(f)}</li>`).join("")}</ul>
        ${(S.do_decyzji || []).length ? `<details class="ramka-uwaga"><summary><b>Do Twojej decyzji przed publikacją (${S.do_decyzji.length})</b> – AI zapisało w dokumentach rozwiązanie zgodne z danymi i przepisami; sprawdź te punkty</summary>
          <ul class="lista">${S.do_decyzji.map((x, nr) => `<li><label class="wiersz" style="margin:0"><input type="checkbox" ${x.ok ? "checked" : ""} onchange="kzDoDecyzji(${nr}, this.checked)" title="Zaznacz, gdy sprawa jest rozstrzygnięta"> <span><b>${esc(x.dokument)}:</b> ${esc(x.punkt)}</span></label></li>`).join("")}</ul></details>` : ""}<div class="pasek"><button class="glowny" onclick="KZ_AKT='zmiany'; rysujKreator()">Dalej – sprawdzenie →</button></div>` : ""}`,
    zmiany: `<p class="opis">AI sprawdza ${S.sciezka === "wzory" ? "Twoje wzory" : "przygotowane dokumenty"} i proponuje zmiany: dopasowanie do zamówienia, zgodność z przepisami, błędy. Przy każdej zdecyduj: akceptuj, odrzuć albo popraw tekst.</p>
      <textarea id="kz-dod" placeholder="Na co zwrócić szczególną uwagę (opcjonalnie)"></textarea>
      <div class="pasek"><label style="margin:0">Model AI <select id="kz-model"><option value="standardowy" selected>standardowy (do 20 propozycji na dokument)</option>
        <option value="dokladny">dokładny – najstaranniejszy, kilka razy drożej (duże zamówienia)</option></select></label>
        <button class="zolty" data-ik="iskra" onclick="przegladKreatora()">${S.propozycje.length ? "Sprawdź ponownie (AI)" : "Sprawdź i zaproponuj zmiany (AI)"}</button></div>
      ${S.K.przeglad_podsumowanie ? `<div class="karta" style="margin:8px 0">${esc(S.K.przeglad_podsumowanie)}</div>` : ""}
      ${S.K.przeglad_data && !S.propozycje.length ? `<p class="zielone"><b>Nie znaleziono błędów ani sprzeczności między dokumentami.</b></p>
        <div class="pasek"><button class="glowny" onclick="zatwierdzKreator()">Przejdź do kroku „${KZ_GOTOWE(S)}” →</button></div>` : ""}
      ${S.propozycje.length ? `<h4 class="grupa-analizy">Do rozstrzygnięcia: ${S.propozycje.length} ${S.propozycje.length === 1 ? "pozycja" : "pozycji"} – przy każdej akceptuj albo odrzuć</h4>
        <div class="pasek"><button class="maly" onclick="decyzjaWszystkie('tak')">Akceptuj wszystkie</button><button class="maly" onclick="decyzjaWszystkie('nie')">Odrzuć wszystkie</button>
        <span class="opis" style="margin:0">Rozstrzygnięto: ${S.propozycje.filter(p => p.decyzja).length} / ${S.propozycje.length} (zaakceptowano: ${S.propozycje.filter(p => p.decyzja === "tak").length})</span></div>
        ${S.propozycje.map(p => `<div class="alert-k kz-prop ${p.decyzja === "tak" ? "kz-tak" : p.decyzja === "nie" ? "kz-nie" : ""}">
          <div class="alert-gora"><span class="znacznik ${p.waga === "krytyczna" ? "z-czerwony" : p.waga === "istotna" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(p.waga || "")}</span>
            <b>${esc(p.plik || p.dokument || "")}</b>${p.sprzecznosc ? ' <span class="znacznik z-do-analizy">sprzeczność między dokumentami</span>' : ""}${p.typ === "dopisanie" ? ' <span class="znacznik z-startujemy">nowy zapis</span>' : ""}${p.odnaleziony ? "" : ' <span class="znacznik z-odpuszczamy">do ręcznego wprowadzenia</span>'}</div>
          ${p.typ === "zmiana" ? `<div class="kz-diff"><del>${esc(p.cytat)}</del></div>` : `<div class="opis">po: „${esc(p.cytat.slice(0, 120))}…”</div>`}
          <textarea class="kz-nowy" data-id="${p.id}" rows="2">${esc(p.nowy_edyt ?? p.nowy)}</textarea>
          <div class="opis">${esc(p.uzasadnienie)}${p.podstawa ? ` <i>(${esc(p.podstawa)})</i>` : ""}</div>
          <div class="pasek" style="margin:4px 0 0"><button class="maly ${p.decyzja === "tak" ? "glowny" : ""}" onclick="decyzjaKz('${p.id}', 'tak')">✓ Akceptuj</button>
            <button class="maly" onclick="decyzjaKz('${p.id}', 'nie')">✕ Odrzuć</button></div></div>`).join("")}
        ${(() => { const zost = S.propozycje.filter(p => !p.decyzja).length; return zost
          ? `<div class="pasek"><button class="glowny" disabled>Zatwierdź i przejdź dalej</button><span class="opis" style="margin:0">Zostało do rozstrzygnięcia: ${zost}.</span></div>`
          : `<div class="pasek"><button class="glowny" data-ik="dokument" onclick="zatwierdzKreator()">Zatwierdź i przejdź do kroku „${KZ_GOTOWE(S)}” →</button>
              <span class="opis" style="margin:0">${S.propozycje.some(p => p.decyzja === "tak") ? "Zaakceptowane zmiany zostaną wprowadzone: wersja Word ze śledzeniem zmian i wersja czysta." : "Wszystkie odrzucone – dokumenty bez zmian."}</span></div>`; })()}
        <div class="pasek"><span class="opis" style="margin:0">Pobierz uwagi (Word):</span>
          <select id="kz-uwagi-zakres"><option value="wszystkie">wszystkie (${S.propozycje.length})</option><option value="przyjete">przyjęte (${S.propozycje.filter(p => p.decyzja === "tak").length})</option>
            <option value="do_decyzji">bez decyzji (${S.propozycje.filter(p => !p.decyzja).length})</option></select>
          <button data-ik="pobierz" onclick="pobierzUwagiKz()">Pobierz uwagi</button></div>` : ""}
      ${S.koncowe.length ? `<h4 class="grupa-analizy">Dokumenty po zmianach</h4><ul class="lista">${S.koncowe.map(f => `<li>${plk(f, "dokumenty_koncowe")}${/_ze_zmianami/.test(f) ? ' <small class="opis">– ze śledzeniem zmian (Recenzja → Zaakceptuj / Odrzuć w Wordzie)</small>' : ""}</li>`).join("")}</ul>` : ""}
      ${S.reczne.length ? `<div class="ramka-uwaga"><b>Do ręcznego wprowadzenia (${S.reczne.length}):</b><ul class="lista">${S.reczne.map(r => `<li>${esc(r.dokument || "")}: „${esc((r.cytat || "").slice(0, 100))}” → „${esc((r.nowy || "").slice(0, 160))}” <small class="opis">(${esc(r.powod)})</small></li>`).join("")}</ul></div>` : ""}
      `,
    gotowe: `<p class="opis">${S.prywatny ? "Komplet do wysłania wykonawcom: zapytanie ofertowe, opis zakresu, wzór umowy, formularz oferty, szacunek kosztów i lista kontrolna."
      : `Komplet do publikacji: dokumenty, kosztorys inwestorski, notatka z szacowania${S.rodzaj !== "roboty" ? ", formularz cenowy dla wykonawców" : ""} i lista kontrolna.`}</p>
      ${kzBrakiPublikacji(S)}
      ${S.reczne.length ? `<div class="ramka-uwaga"><b>Zaakceptowane zmiany do wprowadzenia ręcznie (${S.reczne.length})</b> – program nie odnalazł fragmentu w dokumencie; szczegóły w kroku „Sprawdzenie i zmiany”.
        <label class="wiersz" style="margin:6px 0 0"><input type="checkbox" ${S.K.reczne_potwierdzone ? "checked" : ""} onchange="zapiszKreator({reczne_potwierdzone: this.checked})"> wprowadziłem te zmiany ręcznie</label></div>` : ""}
      ${Object.keys(S.znaczniki || {}).length ? `<div class="ramka-uwaga"><b>Pola do uzupełnienia w dokumentach:</b><ul class="lista">${Object.entries(S.znaczniki).map(([f, n]) => `<li>${esc(f)} – ${n} × [UZUPEŁNIJ…]</li>`).join("")}</ul></div>` : ""}
      <div class="pasek"><a class="przycisk glowny" data-ik="pobierz" href="/api/projekty/${S.projekt.id}/kreator/zip" onclick="return kzZipPotwierdz()">Pobierz komplet (ZIP)</a>
        ${S.prywatny ? "" : `<a class="przycisk maly" href="https://ezamowienia.gov.pl/" target="_blank" rel="noopener">Platforma e-Zamówienia ↗</a>`}</div>
      <h4 class="grupa-analizy">Lista kontrolna przed ${S.prywatny ? "wysłaniem zapytania" : "publikacją"} – ${S.elementy.filter(e => e.status).length} z ${S.elementy.length}</h4>
      <p class="opis">${S.prywatny ? "Dokumenty zapytania sprawdzisz w kroku „Sprawdzenie i zmiany”; czynności (uchwała, rozesłanie, finansowanie) odhacz po wykonaniu."
        : "Pisma program przygotuje sam – albo wgraj swój wzór, a program go sprawdzi w kroku „Sprawdzenie i zmiany”."}</p>
      ${S.elementy.map(elementKz).join("")}
      <p class="opis">Termin składania ofert: ${esc(S.min_dni_opis)}.</p>
      <h4 class="grupa-analizy">${S.prywatny ? "Po zebraniu ofert" : "Po publikacji"}</h4>${S.prywatny ? "" : kzPostepowanie(S)}<div class="pasek"><button class="maly" data-ik="trofeum" onclick="kzOcena()">Sprawdź złożone oferty</button></div>
      ${S.prywatny ? `<p class="opis">Po wyborze oferty: protokół wyboru wykonawcy${S.podmiot === "deweloper" ? "" : " i informacja dla właścicieli / członków"} (porównanie ofert i uzasadnienie wyboru – w „Sprawdź złożone oferty”).</p>` : ""}
      ${S.prywatny ? `<p class="opis">Termin, liczba ofert i zaproszenia do firm z okolicy – w kafelku <a href="#" onclick="ZW_ID='${PROJEKT_ID}'; pokaz('zam_zapytania'); return false">Moje zapytania</a>.</p>` : ""}
      ${(S.czesci || {}).podzial && (S.czesci.lista || []).length >= 2 ? kzUmowyCzesci(S) : (() => { const u = S.K.umowa || {}; return `<h4 class="grupa-analizy">Po wyborze oferty – umowa z wykonawcą</h4>
        <p class="opis">Dane przejdą do realizacji umowy: wartość umowy to cena z oferty wybranego wykonawcy (nie ${S.prywatny ? "szacunek kosztów" : "kosztorys inwestorski"}).</p>
        <div class="pasek" style="flex-wrap:wrap"><button class="maly" data-ik="trofeum" onclick="kzZOceny()">Pobierz z oceny ofert</button><span id="kz-oceny"></span></div>
        <div class="siatka"><label>Wykonawca<input id="ku-naz" value="${esc(u.wykonawca_nazwa || "")}"></label><label>NIP<input id="ku-nip" value="${esc(u.wykonawca_nip || "")}"></label>
          <label>Adres wykonawcy<input id="ku-adr" value="${esc(u.wykonawca_adres || "")}"></label><label>Cena oferty netto [zł]<input id="ku-cena" value="${esc(u.cena_netto || "")}"></label>
          <label>VAT<select id="ku-vat">${[["", "–"], ["0.23", "23%"], ["0.08", "8%"], ["0.05", "5%"], ["0", "0% / zw."]].map(([v, t]) => `<option value="${v}" ${String(u.vat || "") === v ? "selected" : ""}>${t}</option>`).join("")}</select></label>
          <label>Nr umowy<input id="ku-nr" value="${esc(u.umowa_nr || "")}"></label><label>Data umowy<input type="date" id="ku-data" value="${esc(u.data_umowy || "")}"></label>
          <label>Termin wykonania<input type="date" id="ku-term" value="${esc(u.termin || "")}"></label></div>
        ${((S.postepowanie || {}).kalendarz || []).filter(k => k.ostrzezenie).map(k => `<div class="ramka-uwaga" style="margin:6px 0">⚠ ${esc(k.co.replace(/^UWAGA: /, ""))}</div>`).join("")}
        <div class="pasek"><button class="glowny" data-ik="kask" onclick="kzUmowa(true)">Umowa podpisana – prowadź realizację umowy</button><button class="maly" onclick="kzUmowa(false)">Zapisz</button></div>`; })()}`,
  };
  $("#kreator-zam").innerHTML = `<div class="karta kreator-panel"><div class="pasek" style="margin:0 0 8px"><b>Kreator zamówienia ·</b> <select class="kz-rodzaj" title="Rodzaj zamówienia – od niego zależą szacowanie, dokumenty i zakres sprawdzenia" onchange="zmienRodzajZam(this.value)">${Object.entries(RODZ_ZAM).map(([k, t]) => `<option value="${k}" ${k === S.rodzaj ? "selected" : ""}>${esc(t)}</option>`).join("")}</select> <b>· ${S.sciezka === "wzory" ? "Twoje wzory" : "od początku"}</b>
      </div>
    <div class="kz-stepper">${kroki.map(([id, t], i) => `<button class="kz-krok ${id === KZ_AKT ? "akt" : ""} ${stanKroku(S, id) ? "ok" : ""}" onclick="KZ_AKT='${id}'; rysujKreator()"><span>${stanKroku(S, id) ? "✓" : i + 1}</span>${t}</button>`).join("")}</div>
    <div class="kz-tresc"><h3>${kroki.findIndex(k => k[0] === KZ_AKT) + 1}. ${esc(kroki.find(k => k[0] === KZ_AKT)[1])}</h3>${kzKomunikaty(S, KZ_AKT)}${tresc[KZ_AKT]}</div></div>`;
  wstawIkony($("#kreator-zam"));
  if (KZ_AKT === "warunki" && $("#kzfin-tresc")) ladujFin(S.projekt.id, true);
  // tylko kreator: sekcje szczegółowe pokazywane pod krokiem, którego dotyczą
  const MAPA = {potrzeba: ["sek-dokumenty", "asystent"], wzory: ["asystent"], wartosc: ["sek-kosztorys"]}[KZ_AKT] || [];
  let pokazane = 0;
  document.querySelectorAll("#projekt > .krok").forEach(k => {
    const ok = MAPA.includes(k.id) || (MAPA.includes("asystent") && /Asystent dokumentów/.test(k.querySelector("h3")?.textContent || ""));
    k.classList.toggle("kz-ukryj", !ok); if (ok) pokazane++; });
  document.querySelectorAll("#projekt .pasek-sekcji, #projekt > .widok-przelacznik").forEach(e => e.style.display = "none");
  const ng_ = $("#projekt > .naglowek");
  if (ng_ && ng_.nextElementSibling !== $("#kreator-zam")) {
    const dost_ = ng_.nextElementSibling && /Dostęp|widzisz tylko/.test(ng_.nextElementSibling.textContent || "") ? ng_.nextElementSibling : null;
    $("#projekt").insertBefore(ng_, $("#kreator-zam"));
    if (dost_) $("#projekt").insertBefore(dost_, $("#kreator-zam"));
  }
  if (ng_) ng_.querySelectorAll("button").forEach(bt => { if (/doRealizacji\('[^']+', true\)/.test(bt.getAttribute("onclick") || "")) bt.style.display = "none"; });  // krok 7 kreatora
  // jeden ekran: kreator – bez karty „Przegląd projektu” (liczniki, raport – są w kreatorze i nagłówku) i bez drugiego wyboru rodzaju zamówienia
  document.querySelectorAll("#projekt .rodzaj-zam, #projekt #sek-przeglad").forEach(e => e.style.display = "none");
  if (KZ_NT_PID !== PROJEKT_ID) { KZ_NT_PID = PROJEKT_ID; KZ_NT_NODE = null; KZ_NOTATKI_OTWARTE = false; }  // inne zamówienie – własne notatki
  const nt_ = $("#projekt #sek-przeglad .notatki") || KZ_NT_NODE;  // po ponownym rysowaniu kreatora – ten sam blok notatek
  if (nt_) {
    KZ_NT_NODE = nt_;
    const ile = nt_.querySelectorAll(".notatka").length;
    $("#kreator-zam").insertAdjacentHTML("afterbegin", `<details id="kz-notatki" style="float:right;margin:0 0 6px 10px;max-width:420px"><summary class="przycisk maly" style="cursor:pointer">Notatki (${ile})</summary><div class="karta" style="padding:8px 12px;margin-top:6px"></div></details>`);
    nt_.querySelector("h4")?.remove();
    $("#kz-notatki .karta").appendChild(nt_);
    if (KZ_NOTATKI_OTWARTE) $("#kz-notatki").open = true;
    $("#kz-notatki").addEventListener("toggle", e => { KZ_NOTATKI_OTWARTE = e.target.open; });
  }
  if (pokazane) $("#kreator-zam .kz-tresc").insertAdjacentHTML("beforeend", `<p class="opis" style="margin:10px 0 0">⬇ Szczegóły tego kroku: ${KZ_AKT === "wartosc" ? "pozycje kosztorysu inwestorskiego" : KZ_AKT === "dokumenty" ? "formularz dokumentacji (dane z kreatora)" : "dokumenty i asystent"} – poniżej.</p>`);
}
function elementKz(e) {
  const S = KZ, d = e.dane || {}, ikonka = e.status === "ok" ? "✓" : e.status === "nd" ? "–" : "○";
  const pobierz = e.plik ? `<a class="przycisk maly" data-ik="pobierz" href="/pobierz/${S.projekt.id}/dokumenty_postepowania/${encodeURIComponent(e.plik)}">Pobierz</a>` : "";
  const wlasny = `<label class="przycisk maly" data-ik="wgraj">Mam własny wzór<input type="file" hidden accept=".docx,.doc,.pdf,.odt" onchange="wzorElementu('${e.id}', this.files[0])"></label>`;
  const nd = `<button class="maly" onclick="statusElementu('${e.id}', '${e.status === "nd" ? "" : "nd"}')">${e.status === "nd" ? "Przywróć" : "Nie dotyczy"}</button>`;
  const pola = {
    rodo: `<input id="el-rodo-iod" placeholder="kontakt do inspektora ochrony danych (e-mail / adres)" value="${esc(d.iod || "")}" style="flex:1;min-width:220px">`,
    kwota: `<input id="el-kwota-kwota" inputmode="decimal" placeholder="kwota brutto [zł]" value="${esc(d.kwota || (S.brutto ? String(S.brutto) : ""))}" style="width:170px${S.netto && S.stawka_vat_znana === false ? ";background:var(--zolty-jasny)" : ""}">
      ${S.netto && S.brutto ? `<small class="opis" style="margin:0">${S.stawka_vat_znana === false ? "podpowiedź: wartość netto + VAT 23% – stawka VAT nieustalona; sprawdź stawkę i w razie potrzeby popraw kwotę" : `podpowiedź: wartość netto + VAT ${Math.round((+S.stawka_vat || 0) * 100)}% (stawka z kosztorysu zamówienia)`}</small>` : ""}`,
    plan: `<span class="opis" style="margin:0">Czy zamówienie jest już w planie postępowań na ${S.rok_planu || new Date().getFullYear()} r.?</span>
      <button class="maly" onclick="statusElementu('plan', 'ok')">Tak, jest w planie</button>
      <input id="el-plan-termin" placeholder="przewidywany termin wszczęcia, np. I kwartał ${S.rok_planu || new Date().getFullYear()}" value="${esc(d.termin || "")}" style="min-width:220px">`,
    czesci: `<div style="width:100%">${S.powody_czesci.map((p, i) => `<label class="wiersz" style="margin:2px 0;display:flex;gap:6px;align-items:flex-start"><input type="checkbox" class="el-czesci-pow" value="${esc(p)}" ${(d.powody || []).includes(p) ? "checked" : ""}> ${esc(p)}</label>`).join("")}
      <input id="el-czesci-dodatkowe" placeholder="dodatkowe uzasadnienie (opcjonalnie)" value="${esc(d.dodatkowe || "")}" style="width:100%"></div>`,
    ogloszenie: `<input id="el-ogloszenie-cpv" placeholder="główny kod CPV, np. 55320000-9" value="${esc(d.cpv || "")}" style="width:220px">
      <input id="el-ogloszenie-otwarcie" placeholder="termin otwarcia ofert" value="${esc(d.otwarcie || "")}" style="width:180px">`,
  }[e.id] || "";
  let akcje = "";
  if (e.rodzaj === "pismo") akcje = `${pola}<button class="${e.plik ? "maly" : "glowny"}" data-ik="dokument" onclick="przygotujElement('${e.id}')">${e.id === "plan" ? "Nie – przygotuj pozycję planu" : e.plik ? "Przygotuj ponownie" : "Przygotuj"}</button>${pobierz}${wlasny}${nd}`;
  else if (e.rodzaj === "sprawdzenie") akcje = `<button class="maly" onclick="KZ_AKT='zmiany'; rysujKreator()">Sprawdź w kroku „Sprawdzenie i zmiany”</button>
      <button class="maly ${e.status === "ok" ? "glowny" : ""}" onclick="statusElementu('${e.id}', '${e.status === "ok" ? "" : "ok"}')">${e.status === "ok" ? "✓ Sprawdzone" : "Oznacz jako sprawdzone"}</button>${nd}`;
  else if (e.id === "finansowanie" && e.uwaga) akcje = `<span class="opis" style="margin:0;flex-basis:100%">${esc(e.uwaga)}</span>
      <button class="maly" onclick="KZ_AKT='warunki'; rysujKreator(); setTimeout(() => $('#kz-fin')?.scrollIntoView({behavior: 'smooth'}), 300)">Finansowanie (krok „Warunki”)</button>
      ${e.status === "ok" ? "" : `<button class="maly" onclick="KZ_AKT='${S.sciezka === "wzory" ? "zmiany" : "dokumenty"}'; rysujKreator()">${S.sciezka === "wzory" ? "Sprawdź wzory" : "Przygotuj dokumenty"}</button>`}${nd}`;
  else if (e.rodzaj === "reczne") akcje = `<button class="maly ${e.status === "ok" ? "glowny" : ""}" onclick="statusElementu('${e.id}', '${e.status === "ok" ? "" : "ok"}')">${e.status === "ok" ? "✓ Zrobione" : "Oznacz jako zrobione"}</button>${nd}`;
  else if (e.id === "kosztorys") {
    const pob = (f, t) => f ? `<a class="przycisk maly" data-ik="pobierz" href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(f)}">${t}</a>` : "";
    akcje = (e.netto ? "" : `<button class="glowny" data-ik="kalkulator" onclick="KZ_AKT='wartosc'; rysujKreator(); setTimeout(() => kosztorysKreatora(), 50)">Przygotuj kosztorys (AI)</button>
        <button class="maly" onclick="KZ_AKT='wartosc'; rysujKreator()">Wpisz wartość ręcznie</button>`)
      + (e.netto ? `<button class="${e.plik_notatka ? "maly" : "glowny"}" data-ik="dokument" onclick="notatkaKreatora()">${e.plik_notatka ? "Notatka – przygotuj ponownie" : "Przygotuj notatkę z szacowania"}</button>` : "")
      + pob(e.plik_kosztorys, "Pobierz kosztorys") + pob(e.plik_notatka, "Pobierz notatkę") + nd;
  }
  else if (e.id === "oswiadczenia") akcje = `<button class="${e.plik_auto ? "maly" : "glowny"}" data-ik="dokument" onclick="przygotujOswiadczenia()">${e.plik_auto ? "Przygotuj ponownie" : "Przygotuj"}</button>
      ${e.plik_auto ? `<a class="przycisk maly" data-ik="pobierz" href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(e.plik_auto)}">Pobierz</a>` : ""}${wlasny}${nd}`;
  else akcje = e.status === "ok" ? `<span class="opis" style="margin:0">gotowe</span>` : `<button class="maly" onclick="KZ_AKT='${e.id === "kosztorys" ? "wartosc" : "dokumenty"}'; rysujKreator()">Przejdź do kroku</button>${nd}`;
  return `<div class="kz-el kz-el-${e.status || "brak"}"><div class="kz-el-gora"><span class="kz-el-ik">${ikonka}</span><span>${esc(e.opis)}</span>
    ${e.wlasny ? `<small class="opis">– Twój wzór: ${esc(e.wlasny)}</small>` : ""}</div><div class="pasek" style="margin:6px 0 0;flex-wrap:wrap">${akcje}</div></div>`;
}
function daneElementu(id) {
  const v = x => ($("#" + x) || {}).value || "";
  return {rodo: {iod: v("el-rodo-iod")}, kwota: {kwota: v("el-kwota-kwota")}, plan: {termin: v("el-plan-termin")}, ogloszenie: {cpv: v("el-ogloszenie-cpv"), otwarcie: v("el-ogloszenie-otwarcie")},
          czesci: {powody: [...document.querySelectorAll(".el-czesci-pow:checked")].map(e => e.value), dodatkowe: v("el-czesci-dodatkowe")}}[id] || {};
}
async function przygotujElement(id) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/element`, {json: {id, akcja: "przygotuj", dane: daneElementu(id)}})); if (!r) return;
  KZ = r; rysujKreator(); const e = r.elementy.find(x => x.id === id);
  komunikat("Przygotowano: " + (e && e.plik || "pismo") + " – pobierz i uzupełnij pola [UZUPEŁNIJ].");
}
async function statusElementu(id, status) {
  let powod;
  if (status === "nd") { powod = prompt("Dlaczego ta pozycja nie dotyczy tego zamówienia? (krótki powód – trafi do listy kontrolnej)", ((KZ.elementy || []).find(e => e.id === id) || {}).powod_nd || ""); if (powod === null) return; }
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/element`, {json: {id, akcja: "status", status, powod, dane: daneElementu(id)}})); if (r) { KZ = r; rysujKreator(); }
}
async function wzorElementu(id, f) {
  if (!f) return; const fd = new FormData(); fd.append("id", id); fd.append("plik", f);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/element/wzor`, {body: fd, method: "POST"})); if (!r) return;
  KZ = r; rysujKreator(); komunikat("Wgrano Twój wzór – zostanie sprawdzony w kroku „Sprawdzenie i zmiany” i dołączony do kompletu.");
}
function kzEtykieta(pole) {
  const [g, k] = pole.split("."), S = KZ;
  if (pole === "wartosc") return "Wartość zamówienia netto";
  if (g === "co") return {nazwa: "Nazwa zamówienia", opis: "Opis", zamawiajacy: "Zamawiający", cpv: "Kod CPV", znak: "Znak sprawy", tryb_dok: "Tryb udzielenia zamówienia"}[k] || k;
  if (g === "potrzeba") return ((S.pytania || []).find(p => p[0] === k) || [k, k])[1];
  if (g === "warunki") return (S.etykiety_warunkow || {})[k] || k;
  return pole;
}
async function kzOdczytajPonownie() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/zrodla/ponownie`, {method: "POST"})), () => { KZ_AKT = null; ladujKreator(); }); }
async function kzZrodla(files) {
  if (!files.length) return; const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  const z = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/zrodla`, {method: "POST", body: fd})); if (!z) return;
  if ((z.pominiete || []).length) komunikat(`Limit to 10 plików na jedno wgranie – pominięto: ${z.pominiete.join(", ")}. Wgraj je osobno.`, true);
  sledz(z, () => { KZ_AKT = null; ladujKreator(); });
}
async function kzSprzecznosc(pole, wartosc) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/sprzecznosc`, {json: {pole, wartosc}})); if (r) { KZ = r; rysujKreator(); komunikat("Przyjęto: " + kzEtykieta(pole)); }
}
async function kzZOceny() {
  const L = await bezpiecznie(() => api("/api/ocena-ofert")); if (!L) return;
  const z = L.filter(x => x.najkorzystniejsza);
  $("#kz-oceny").innerHTML = z.length ? `<select id="ku-oc">${z.map(x => `<option value="${x.id}">${esc(x.nazwa)} → ${esc(x.najkorzystniejsza)}${x.naj_cena_netto ? " · " + zl(x.naj_cena_netto) + " netto" : x.naj_cena_brutto ? " · " + zl(x.naj_cena_brutto) + " brutto" : ""}</option>`).join("")}</select>
    <button class="maly glowny" onclick="kzWstawOcene()">Wstaw</button>` : '<span class="opis" style="margin:0">Brak ocen ofert z wybraną najkorzystniejszą ofertą (Sprawdź złożone oferty).</span>';
  window._OCENY = z;
}
function kzWstawOcene() {
  const x = (window._OCENY || []).find(o => o.id === nrv("ku-oc")); if (!x) return;
  $("#ku-naz").value = x.najkorzystniejsza || ""; $("#ku-nip").value = x.naj_nip || ""; $("#ku-adr").value = x.naj_adres || "";
  if (x.naj_cena_netto) $("#ku-cena").value = x.naj_cena_netto; else if (x.naj_cena_brutto) { $("#ku-cena").value = ""; komunikat("Ocena ma cenę brutto (" + zl(x.naj_cena_brutto) + ") – wpisz cenę netto i VAT z oferty.", true); }
}
async function kzUmowa(realizuj) {
  const json = {wykonawca_nazwa: nrv("ku-naz"), wykonawca_nip: nrv("ku-nip"), wykonawca_adres: nrv("ku-adr"), cena_netto: nrv("ku-cena"), vat: nrv("ku-vat"), umowa_nr: nrv("ku-nr"), data_umowy: nrv("ku-data"), termin: nrv("ku-term")};
  if (realizuj && (!json.wykonawca_nazwa || !json.cena_netto)) return komunikat("Wpisz wykonawcę i cenę oferty netto.", true);
  if (json.cena_netto && !(parseFloat(json.cena_netto.replace(/\s/g, "").replace(",", ".")) > 0 && /^[\d\s.,]+(zł)?$/.test(json.cena_netto.trim()))) return komunikat("Cena oferty netto: wpisz kwotę, np. 1 234 567,89.", true);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/umowa`, {json})); if (!r) return; KZ = r;
  if (realizuj) doRealizacji(PROJEKT_ID, true); else { rysujKreator(); komunikat("Zapisano."); }
}
function przelaczSekcjeKz() { localStorage.setItem("kz_wszystko", localStorage.getItem("kz_wszystko") === "1" ? "0" : "1"); rysujKreator(); }
function zbierzKz(atr) { const o = {}; document.querySelectorAll(`[data-${atr}]`).forEach(e => o[e.dataset[atr]] = e.value); return o; }
// ---------------------------------------------------------------- podział zamówienia na części (art. 91 Pzp)
function kzCzesci(S) {
  const c = S.czesci || {podzial: false, lista: []}, P = S.czesci_propozycja, zl = v => liczba(v || 0, 2) + " zł";
  const wej = (i, k, v, typ = "text", szer = "") => `<input data-kzc="${i}.${k}" type="${typ}" value="${esc(v ?? "")}" ${szer ? `style="width:${szer}"` : ""}>`;
  const prop = P ? `<div class="karta" style="margin:8px 0;padding:10px 14px;border-left:4px solid #1F5A99"><b>Propozycja AI (${esc(P.data || "")})</b>
      ${P.zalecany ? `<ol class="lista">${P.lista.map(x => `<li><b>${esc(x.nazwa)}</b> – ${zl(x.wartosc)}${x.zakres ? `<br><small class="opis">${esc(x.zakres)}</small>` : ""}</li>`).join("")}</ol>`
        : `<p class="opis">Podział niezalecany: ${esc(P.powody_braku || "")}</p>`}
      ${P.uzasadnienie ? `<p class="opis" style="margin:4px 0">${esc(P.uzasadnienie)}</p>` : ""}
      ${(P.ryzyka || []).length ? `<p class="opis" style="margin:4px 0"><b>Ryzyka:</b> ${P.ryzyka.map(esc).join("; ")}</p>` : ""}
      ${P.zalecany ? `<button class="maly glowny" onclick="kzCzesciPrzyjmij()">Przyjmij propozycję</button> <span class="opis">– możesz ją potem poprawić</span>` : ""}</div>` : "";
  const tab = c.podzial ? `<div class="tabela-okno" style="margin-top:8px"><table class="tabela"><tr><th>Nr</th><th>Nazwa części</th><th>Zakres</th><th>Wartość netto [zł]</th><th>CPV</th><th>Termin realizacji</th><th></th></tr>
      ${(c.lista || []).map((x, i) => `<tr><td>${i + 1}</td><td>${wej(i, "nazwa", x.nazwa, "text", "180px")}</td><td><textarea data-kzc="${i}.zakres" rows="2" style="width:220px">${esc(x.zakres || "")}</textarea></td>
        <td>${wej(i, "wartosc", x.wartosc || "", "number", "120px")}</td><td>${wej(i, "cpv", x.cpv, "text", "110px")}</td><td>${wej(i, "termin", x.termin, "text", "140px")}</td>
        <td><button class="maly" onclick="kzCzesciUsun(${i})">Usuń</button></td></tr>`).join("")}
      <tr><td colspan="3"><b>Razem</b></td><td><b>${zl(c.suma)}</b>${S.netto ? `<br><small class="opis">wartość zamówienia: ${zl(S.netto)}</small>` : ""}</td><td colspan="3"></td></tr></table></div>
      <button class="maly" data-ik="plus" onclick="kzCzesciDodaj()">Dodaj część</button>
      <div class="siatka" style="margin-top:10px">
        <label>Ofertę można złożyć na (puste = wszystkie części)<input id="kzc-max-ofert" type="number" min="1" value="${esc(c.max_ofert || "")}" placeholder="wszystkie"></label>
        <label>Maksymalna liczba części dla jednego wykonawcy (puste = bez limitu)<input id="kzc-max-udz" type="number" min="1" value="${esc(c.max_udzielen || "")}" placeholder="bez limitu"></label>
        <label style="grid-column:1/-1">Zasady wyboru części przy limicie (obiektywne i niedyskryminujące – art. 91 ust. 3)<textarea id="kzc-zasady" rows="2">${esc(c.zasady_limitu || "")}</textarea></label>
      </div>
      ${(c.bledy || []).map(b => `<div class="ramka-uwaga" style="margin:6px 0">${esc(b)}</div>`).join("")}
      <button class="glowny" onclick="kzCzesciZapisz(true)">Zapisz podział</button>` : "";
  return `<div class="karta" id="kz-czesci" style="margin-top:14px"><h3 style="margin-top:0">Podział na części</h3>
    <p class="opis">Pzp zachęca do dzielenia zamówień na części (art. 91) – brak podziału trzeba uzasadnić. Tryb i progi wynikają z <b>łącznej wartości wszystkich części</b> (art. 30), więc podział nie zmienia trybu.
      Mniejsze części to zwykle więcej ofert od małych firm.</p>
    <label class="wiersz" style="display:flex;gap:8px;align-items:flex-start;margin:6px 0"><input type="radio" name="kz-podzial" ${!c.podzial ? "checked" : ""} onchange="kzCzesciZapisz(false)"> <span>Bez podziału – zaznacz powody poniżej (art. 91 ust. 2)</span></label>
    <label class="wiersz" style="display:flex;gap:8px;align-items:flex-start;margin:6px 0"><input type="radio" name="kz-podzial" ${c.podzial ? "checked" : ""} onchange="kzCzesciZapisz(true)"> <span>Podziel zamówienie na części</span></label>
    ${c.podzial ? "" : kzCzesciPowody(S, P)}
    <div class="pasek" style="margin:6px 0"><button class="maly" data-ik="iskra" onclick="kzCzesciAI()">Zaproponuj podział (AI)</button>
      <span class="opis">AI analizuje przedmiot i kosztorys, proponuje części z uzasadnieniem i ryzykami – decyzja należy do Ciebie.</span></div>
    ${prop}${tab}</div>`;
}
function kzCzesciPowody(S, P) {  // bez podziału: powody z art. 91 ust. 2 – te same trafiają do pisma w liście kontrolnej i do ogłoszenia
  const W = S.czesci_powody || {}, wyb = W.powody || [], lista = [...(S.powody_czesci || []), ...wyb.filter(p => !(S.powody_czesci || []).includes(p))];
  const ai = P && !P.zalecany && P.powody_braku ? P.powody_braku : "";
  return `<div class="karta" id="kzc-powody" style="margin:8px 0;padding:10px 14px;border-left:4px solid ${wyb.length || W.dodatkowe ? "#2E7D32" : "#C0391B"}">
      <b>Powody braku podziału</b> <span class="opis">– zaznacz co najmniej jeden albo wpisz własny; trafią do uzasadnienia (lista kontrolna) i do ogłoszenia</span>
      ${lista.map(p => `<label class="wiersz" style="display:flex;gap:8px;align-items:flex-start;margin:4px 0"><input type="checkbox" class="kzc-pow" value="${esc(p)}" ${wyb.includes(p) ? "checked" : ""}> <span>${esc(p)}</span></label>`).join("")}
      <label style="display:block;margin-top:6px">Własne uzasadnienie (opcjonalnie)<textarea id="kzc-pow-dod" rows="2" style="width:100%">${esc(W.dodatkowe || "")}</textarea></label>
      ${ai ? `<p class="opis" style="margin:6px 0">Propozycja AI: ${esc(ai)} <button class="maly" onclick="$('#kzc-pow-dod').value = ${esc(JSON.stringify(ai))}; kzCzesciZapisz(false)">Wstaw</button></p>` : ""}
      <button class="glowny" style="margin-top:6px" onclick="kzCzesciZapisz(false)">Zapisz powody</button>
      ${wyb.length || W.dodatkowe ? "" : `<div class="ramka-uwaga" style="margin-top:6px">Brak podziału trzeba uzasadnić (art. 91 ust. 2 Pzp) – bez powodów lista kontrolna nie będzie kompletna.</div>`}</div>`;
}
function kzCzesciZbierz() {  // aktualne wpisy z tabeli (bez utraty niezapisanych zmian)
  const c = JSON.parse(JSON.stringify(KZ.czesci || {lista: []})); c.lista = c.lista || [];
  if ($("#kzc-powody")) { c.powody = [...document.querySelectorAll(".kzc-pow:checked")].map(e => e.value); c.dodatkowe = $("#kzc-pow-dod").value; }
  document.querySelectorAll("[data-kzc]").forEach(e => { const [i, k] = e.dataset.kzc.split("."); if (c.lista[+i]) c.lista[+i][k] = e.value; });
  if ($("#kzc-max-ofert")) { c.max_ofert = $("#kzc-max-ofert").value; c.max_udzielen = $("#kzc-max-udz").value; c.zasady_limitu = $("#kzc-zasady").value; }
  return c;
}
function kzCzesciZapisz(podzial) {
  const c = kzCzesciZbierz(); c.podzial = !!podzial;
  if (c.podzial && c.lista.length < 2) while (c.lista.length < 2) c.lista.push({nazwa: "", zakres: "", wartosc: ""});
  return zapiszKreator({czesci: c});
}
function kzCzesciDodaj() { const c = kzCzesciZbierz(); c.lista.push({nazwa: "", zakres: "", wartosc: ""}); c.podzial = true; zapiszKreator({czesci: c}); }
function kzCzesciUsun(i) { const c = kzCzesciZbierz(); c.lista.splice(i, 1); c.podzial = true; zapiszKreator({czesci: c}); }
function kzCzesciPrzyjmij() { const P = KZ.czesci_propozycja || {}; zapiszKreator({czesci: {...kzCzesciZbierz(), podzial: true, lista: P.lista || []}}); }
async function kzCzesciAI() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/czesci/propozycja`, {method: "POST"})), () => ladujKreator()); }
function ocCzesciHtml(O, P) {  // zamówienie podzielone na części – ranking i wybór osobno w każdej części (art. 91 Pzp)
  const swzC = (O.swz || {}).czesci || [];
  return P.czesci.map(c => {
    const nr = String(c.nr), kryt = (swzC.find(x => String(x.nr) === nr) || {}).kryteria || (O.swz || {}).kryteria || [];
    const lst = O.oferty.filter(o => o.czesci_wyniki?.[nr]?.miejsce).sort((a, b) => a.czesci_wyniki[nr].miejsce - b.czesci_wyniki[nr].miejsce);
    return `<h4 style="margin:12px 0 4px">Część ${esc(String(c.nr))} – ${esc(c.nazwa || "")} <small class="opis">(${odm(c.ofert || 0, "oferta", "oferty", "ofert")})</small></h4>
      ${lst.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Miejsce</th><th>Wykonawca</th><th>Cena brutto</th>${kryt.map(k => `<th>${esc(k.nazwa)} (${k.waga})</th>`).join("")}<th>Razem pkt</th></tr>
        ${lst.map(o => { const r = o.czesci_wyniki[nr], naj = o.id === c.najkorzystniejsza;
          return `<tr class="${naj && !c.warunkowo ? "wybrany" : ""}"><td><b>${r.miejsce}</b>${naj ? (c.warunkowo ? (o.id !== c.pierwsza_w_rankingu ? ' <small class="znacznik">bez zastrzeżeń</small>' : "") : " 🏆") : ""}${o.wynik?.status !== "prawidłowa" || r.razaco_niska ? ' <small class="znacznik z-do-analizy">warunkowo</small>' : ""}</td><td>${esc(o.nazwa)}</td>
            <td class="liczba">${r.cena_brutto ? zl(+r.cena_brutto) : "–"}${r.ponad_budzet ? ' <small class="czerwone">ponad kwotę</small>' : ""}</td>${kryt.map(k => `<td class="liczba">${pkt(r.punkty_szczegoly?.[k.nazwa])}</td>`).join("")}
            <td class="liczba"><b>${pkt(r.punkty)}</b></td></tr>`; }).join("")}</table></div>
        ${c.warunkowo ? `<div class="ramka-uwaga">Wybór w tej części jest wstrzymany – najwyżej oceniona oferta ma nierozstrzygnięte kwestie (braki, wyjaśnienia albo rażąco niską cenę). Przyjmij wyjaśnienia albo odrzuć ofertę – dopiero wtedy przygotujesz informację o wyborze.</div>` : ""}`
      : `<p class="opis">Brak ocenionych ofert w tej części.</p>`}`; }).join("")
    + (P.ostrzezenia || []).map(t => `<div class="ramka-uwaga" style="margin:6px 0">${esc(t)}</div>`).join("");
}
function kzUmowyCzesci(S) {  // zamówienie w częściach: osobna umowa i realizacja dla każdej części
  const W = S.czesci_zwyciezcy || {}, R = S.czesci_realizacje || {};
  return `<h4 class="grupa-analizy">Po wyborze ofert – umowy w poszczególnych częściach</h4>
    <p class="opis">Każda część to osobna umowa i osobna realizacja (harmonogram, odbiory, faktury). Wartość umowy to cena z oferty wybranego wykonawcy w danej części.
      Część bez wybranego wykonawcy (np. unieważniona) zostaw pustą.</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Część</th><th>Wykonawca</th><th>NIP</th><th>Cena netto [zł]</th><th>VAT [%]</th><th>Nr umowy</th><th>Data umowy</th><th>Termin</th><th>Realizacja</th></tr>
    ${S.czesci.lista.map(c => { const nr = String(c.nr), w = W[nr] || {}, u = ((S.K.czesci_umowy || {})[nr]) || {};
      const pole = (k, v, typ = "text", szer = "120px") => `<input data-kzu="${nr}.${k}" type="${typ}" value="${esc(v ?? "")}" style="width:${szer}">`;
      return `<tr><td><b>${esc(nr)}</b> ${esc(c.nazwa)}${w.nazwa ? `<br><small class="opis">wybrana oferta: ${esc(w.nazwa)}${w.cena_brutto ? " · " + zl(+w.cena_brutto) + " brutto" : ""}${w.warunkowo ? " · warunkowo" : ""}</small>` : ""}</td>
        <td>${pole("wykonawca_nazwa", u.wykonawca_nazwa || w.nazwa, "text", "170px")}</td><td>${pole("wykonawca_nip", u.wykonawca_nip || w.nip, "text", "110px")}</td>
        <td>${pole("cena_netto", u.cena_netto, "number")}</td><td>${pole("vat", u.vat ?? 23, "number", "60px")}</td><td>${pole("umowa_nr", u.umowa_nr)}</td>
        <td>${pole("data_umowy", u.data_umowy, "date", "140px")}</td><td>${pole("termin", u.termin, "text", "120px")}</td>
        <td>${R[nr] ? `<a href="#" onclick="otworzRealizacje('${R[nr]}'); return false">otwórz</a>` : "–"}</td></tr>`; }).join("")}</table></div>
    <div class="pasek"><button class="glowny" data-ik="trofeum" onclick="kzRealizacjeCzesci()">Umowy podpisane – przekaż części do realizacji</button></div>`;
}
async function kzRealizacjeCzesci() {
  const m = {}; document.querySelectorAll("[data-kzu]").forEach(e => { const [nr, k] = e.dataset.kzu.split("."); (m[nr] = m[nr] || {nr})[k] = e.value; });
  const czesci = Object.values(m), gotowe = czesci.filter(c => c.wykonawca_nazwa && c.cena_netto);
  if (!gotowe.length) return komunikat("Wpisz wykonawcę i cenę netto co najmniej dla jednej części.", true);
  if (!confirm(`Umowy podpisane? Program utworzy realizację dla ${gotowe.length} ${gotowe.length === 1 ? "części" : "części"} w zakładce „Realizacja umów”.`)) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/czesci/realizacja`, {json: {czesci}})); if (!r) return;
  for (const x of r.projekty) await bezpiecznie(() => api(`/api/projekty/${x.id}/status`, {json: {status: "realizacja"}}));
  komunikat(`Przekazano do realizacji: ${r.projekty.length} części.`); ladujKreator();
}
// ---------------------------------------------------------------- wiarygodność wykonawcy i referencji (rejestry, BZP, metadane, potwierdzenie u wystawcy)
function ocWerHtml(o) {
  const W = o.weryfikacja, kol = {czerwony: "#dc2626", zolty: "#ca8a04", zielony: "#16a34a"};
  const ST = {potwierdzona: ["potwierdzona", "z-wygrany"], sprzeczna: ["sygnały nieprawdziwości", "z-przegrany"], niepotwierdzona: ["niepotwierdzona", "z-do-analizy"]};
  const ODP = {"": "brak zapytania", wyslano: "zapytanie wysłane", potwierdzil: "wystawca potwierdził", zaprzeczyl: "wystawca zaprzeczył", brak_odpowiedzi: "brak odpowiedzi"};
  const glowa = `<div class="pasek" style="margin:8px 0 4px"><b>Wiarygodność wykonawcy i referencji</b>
    <button class="maly" data-ik="szukaj" onclick="ocWeryfikuj('${o.id}')">${W ? "Sprawdź ponownie" : "Sprawdź wykonawcę i referencje"}</button>
    <span class="opis">rejestry (VAT, KRS), ogłoszenia o wyniku w BZP, metadane plików, powiązania z wykonawcą</span></div>`;
  if (!W) return `<div class="karta" style="margin:8px 0;padding:8px 12px">${glowa}</div>`;
  const wy = W.wykonawca || {}, P = W.podsumowanie || {};
  return `<div class="karta" style="margin:8px 0;padding:8px 12px">${glowa}
    <p class="opis" style="margin:2px 0">Wykonawca: ${esc(wy.nazwa || o.nazwa || "")}${wy.nip ? " · NIP " + esc(wy.nip) : ""}${wy.data_powstania ? " · wpis do KRS " + esc(wy.data_powstania) : ""}${wy.data_rejestracji_vat ? " · rejestracja VAT " + esc(wy.data_rejestracji_vat) : ""} · sprawdzono ${esc(W.data || "")}</p>
    ${(W.wykonawca_sygnaly || []).length ? `<div style="margin:6px 0">${W.wykonawca_sygnaly.map(([k, t]) => `<div style="margin:2px 0"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${kol[k] || "#999"};margin-right:5px"></span>${esc(t)}</div>`).join("")}</div>` : ""}
    ${(W.do_sprawdzenia || []).map(d => { const pw = (W.potwierdzenia || {})[d.pole] || {}; return `<div class="pasek" style="flex-wrap:wrap;margin:4px 0;align-items:center">
      <span><b>Sprawdź w rejestrze:</b> ${esc(d.opis)}${d.szukaj ? ` – wyszukaj: <code>${esc(d.szukaj)}</code>` : ""}</span>
      <a class="przycisk maly" href="${esc(d.link)}" target="_blank" rel="noopener">${d.pole === "uprawnienia" ? "e-CRUB (GUNB)" : "KRZ"}</a>
      <select onchange="ocPotwierdzenie('${o.id}', '${d.pole}', this.value)">${[["", "nie sprawdzono"], ["potwierdzone", "sprawdzone – bez zastrzeżeń"], ["zastrzezenia", "sprawdzone – zastrzeżenia"]].map(([k, t]) => `<option value="${k}" ${k === (pw.wynik || "") ? "selected" : ""}>${t}</option>`).join("")}</select>
      ${pw.data ? `<small class="opis">${esc(pw.data)}${pw.kto ? " · " + esc(pw.kto) : ""}</small>` : ""}</div>`; }).join("")}
    ${(W.do_doslania || []).length ? `<div class="ramka-uwaga" style="margin:6px 0"><b>Do dosłania przez wykonawcę:</b><ul class="lista">${W.do_doslania.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}
    <p style="margin:4px 0">Referencje: <b>${P.potwierdzona || 0}</b> potwierdzone · <b style="color:#dc2626">${P.sprzeczna || 0}</b> z sygnałami nieprawdziwości · <b>${P.niepotwierdzona || 0}</b> niepotwierdzone</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Wystawca</th><th>Zakres, wartość, okres</th><th>Sygnały</th><th>Status</th><th>Potwierdzenie u wystawcy</th></tr>
    ${(W.referencje || []).map((r, i) => `<tr><td>${esc(r.wystawca || "–")}${r.nip_wystawcy ? `<br><small class="opis">NIP ${esc(r.nip_wystawcy)}</small>` : ""}${r.kontakt_osoba || r.kontakt_email || r.kontakt_telefon ? `<br><small class="opis">${esc([r.kontakt_osoba, r.kontakt_email, r.kontakt_telefon].filter(Boolean).join(", "))}</small>` : ""}</td>
      <td>${esc(r.zakres || "")}${r.wartosc ? `<br><small>${esc(String(r.wartosc))}</small>` : ""}<br><small class="opis">${esc([r.data_od, r.data_do].filter(Boolean).join(" – "))}</small></td>
      <td>${(r.sygnaly || []).map(([k, t]) => `<div style="margin:2px 0"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${kol[k] || "#999"};margin-right:5px"></span>${esc(t)}</div>`).join("") || '<span class="opis">–</span>'}</td>
      <td><span class="znacznik ${(ST[r.status] || ST.niepotwierdzona)[1]}">${(ST[r.status] || ST.niepotwierdzona)[0]}</span></td>
      <td><button class="maly" onclick="ocZapytanie('${o.id}', ${i})">Zapytanie do wystawcy</button>
        <select onchange="ocReferencja('${o.id}', ${i}, this.value)">${Object.entries(ODP).map(([k, t]) => `<option value="${k}" ${k === (r.odpowiedz || "") ? "selected" : ""}>${t}</option>`).join("")}</select></td></tr>`).join("")}</table></div>
    <p class="opis" style="margin:4px 0 0">Sygnały to wskazówki do sprawdzenia, nie dowód nieprawdziwości. Najpewniejsze jest potwierdzenie u wystawcy – wyślij zapytanie ze swojej skrzynki i zapisz odpowiedź.
      Możesz też poprosić wykonawcę o protokoły odbioru i faktury dotyczące referencji.</p></div>`;
}
async function ocWeryfikuj(oid) { sledz(await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/${oid}/weryfikacja`, {method: "POST"})), () => otworzOcene(OC_ID)); }
async function ocPotwierdzenie(oid, pole, wynik) {
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/${oid}/potwierdzenie`, {json: {pole, wynik}}))) { komunikat("Zapisano."); otworzOcene(OC_ID); }
}
async function ocReferencja(oid, i, odpowiedz) {
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/${oid}/referencja`, {json: {i, odpowiedz}}))) { komunikat("Zapisano."); otworzOcene(OC_ID); }
}
async function ocZapytanie(oid, i) {
  const r = await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/${oid}/referencja/${i}/zapytanie`)); if (!r) return;
  const [temat, ...tresc] = r.tresc.split("\n"), body = tresc.join("\n").trim();
  try { await navigator.clipboard.writeText(r.tresc); } catch (e) {}
  if (r.email) window.location.href = `mailto:${encodeURIComponent(r.email)}?subject=${encodeURIComponent(temat.replace(/^Temat:\s*/, ""))}&body=${encodeURIComponent(body)}`;
  komunikat(r.email ? "Otworzono wiadomość w programie pocztowym (treść skopiowana do schowka). Po wysłaniu zmień status na „zapytanie wysłane”."
                    : "Treść zapytania skopiowano do schowka – wklej ją do wiadomości do wystawcy (w referencji nie ma adresu e-mail).");
}
async function kzOcena() {  // powiązane sprawdzenie ofert: dokumenty postępowania i podział na części przenoszone z kreatora
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/ocena`, {method: "POST"})); if (!r) return;
  OC_ID = r.id; pokaz("zam_oferty");
}
function kzZaproszenia(S) {  // mało ofert przed terminem – zaproszenia do wykonawców z okolicy, którzy wykonywali podobne zamówienia
  const Z = S.K.zaproszenia || {}, L = Z.kandydaci || [], wys = new Set((Z.wyslane || []).map(x => x.nip || x.nazwa));
  const t = S.K.termin_ofert ? S.K.termin_ofert : "", dni = S.termin_ofert_dni;
  return `<h4 class="grupa-analizy">Mało ofert? Zaproś wykonawców z okolicy</h4>
    <p class="opis">${t ? `Termin składania ofert: <b>${esc(t)}</b>${dni != null ? (dni >= 0 ? ` (za ${odm(dni, "dzień", "dni", "dni")})` : " (minął)") : ""}. ` : ""}Program wyszuka firmy, które w ostatnich 24 miesiącach wygrały podobne zamówienia
      i mają siedzibę albo wykonywały prace w promieniu od miejsca inwestycji (ogłoszenia o wyniku w BZP), z kontaktem i uzasadnieniem AI. Firmy pracujące tylko dla klientów prywatnych nie trafią na listę.</p>
    <div class="pasek" style="flex-wrap:wrap"><label>Miejsce <input id="kzz-miejsce" value="${esc(Z.miejsce || (S.K.potrzeba || {}).obiekt || "")}" placeholder="miejscowość" style="width:200px"></label>
      <label>Promień <select id="kzz-promien">${[20, 30].map(k => `<option value="${k}" ${k === (Z.promien || 20) ? "selected" : ""}>${k} km</option>`).join("")}</select></label>
      <button class="maly" data-ik="szukaj" onclick="kzZaproszeniaSzukaj()">Znajdź wykonawców z okolicy (AI)</button></div>
    ${L.length ? `<p class="opis" style="margin:4px 0">${esc(Z.miejsce || "")}, ${Z.promien} km · ${L.length} firm · ${esc(Z.data || "")}</p>
      <div class="tabela-okno"><table class="tabela"><tr><th></th><th>Wykonawca</th><th>Podobne prace</th><th>Odległość</th><th>Kontakt</th></tr>
      ${L.map(k => { const id = k.nip || k.nazwa; return `<tr><td><input type="checkbox" class="kzz-wyb" value="${esc(id)}" ${k.email && !wys.has(id) && !k.rezygnacja ? "" : "disabled"}></td>
        <td><b>${esc(k.nazwa)}</b>${k.nip ? `<br><small class="opis">NIP ${esc(k.nip)}</small>` : ""}${k.uzasadnienie ? `<br><small>${esc(k.uzasadnienie)}</small>` : ""}${wys.has(id) ? '<br><small class="znacznik z-wygrany">zaproszono</small>' : ""}${k.rezygnacja ? '<br><small class="znacznik z-przegrany">zrezygnowała z zaproszeń</small>' : ""}</td>
        <td><small>${k.liczba_prac} · ${(k.prace || []).slice(0, 2).map(p => esc(p.przedmiot.slice(0, 70)) + (p.miasto ? " (" + esc(p.miasto) + ")" : "")).join("<br>")}</small></td>
        <td><small>${k.odleglosc_siedziby != null ? "siedziba " + k.odleglosc_siedziby + " km" : ""}${k.odleglosc_prac != null ? "<br>prace " + k.odleglosc_prac + " km" : ""}</small></td>
        <td><small>${esc(k.email || "brak e-mail")}${k.telefon ? "<br>" + esc(k.telefon) : ""}${k.email || k.nip ? `<br><a href="#" onclick="kzRezygnacja('${escA(k.nip || "")}', '${escA(k.email || "")}', '${escA(k.nazwa)}'); return false">firma zrezygnowała</a>` : ""}${k.www ? `<br><a href="${esc(/^http/.test(k.www) ? k.www : "https://" + k.www)}" target="_blank" rel="noopener">strona</a>` : ""}</small></td></tr>`; }).join("")}</table></div>
      <div class="pasek"><button class="glowny" data-ik="wyslij" onclick="kzZaproszeniaWyslij('smtp')">Wyślij zaproszenia z mojej skrzynki</button>
        <button class="maly" data-ik="pobierz" onclick="kzZaproszeniaWyslij('eml')">Przygotuj wiadomości (.eml)</button>
        <span class="opis">W załącznikach: dokumenty postępowania z kreatora. Wiadomość zawiera informację o źródle danych i możliwości rezygnacji.</span></div>
      <p class="opis">${esc(Z.uwaga || "")}</p>` : ""}`;
}
async function kzRezygnacja(nip, email, nazwa) {
  if (!confirm(`${nazwa} nie chce otrzymywać zaproszeń? Firma zostanie wykluczona z kolejnych list i wysyłek.`)) return;
  if (await bezpiecznie(() => api("/api/zam/zaproszenia/rezygnacja", {json: {nip, email, nazwa}}))) { komunikat("Zapisano rezygnację – firma nie będzie zapraszana."); kzOdswiez(); }
}
async function kzZaproszeniaSzukaj() {
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/zaproszenia/kandydaci`, {json: {promien: +$("#kzz-promien").value, lokalizacja: $("#kzz-miejsce").value}})), () => kzOdswiez());
}
async function kzZaproszeniaWyslij(sposob) {
  const wybrani = [...document.querySelectorAll(".kzz-wyb:checked")].map(e => e.value);
  if (!wybrani.length) return komunikat("Zaznacz wykonawców (z adresem e-mail).", true);
  if (sposob === "smtp" && !confirm(`Wysłać zaproszenia do ${wybrani.length} wykonawców z Twojej skrzynki pocztowej?`)) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/zaproszenia/wyslij`, {json: {wybrani, sposob}})); if (!r) return;
  if (sposob === "smtp") komunikat(`Wysłano ${r.wyslano} zaproszeń (załączniki: ${r.zalaczniki}).`);
  else { r.pliki.forEach(u => window.open(u, "_blank")); komunikat(`Przygotowano ${r.pliki.length} wiadomości – otwórz je w programie pocztowym i wyślij.`); }
  kzOdswiez();
}
// ---------------------------------------------------------------- finansowanie inwestycji (umowa z bankiem / BGK / instytucją KPO a umowa z wykonawcą)
// FIN_KZ – ta sama sekcja w kreatorze zamówienia (krok „Warunki”): źródła i wymagania przed dokumentami; kontrole harmonogramu wykonawcy
// i porównanie z umową – w realizacji (ten sam zapis, więc po zawarciu umowy nic nie trzeba wprowadzać drugi raz)
let FIN = null, FIN_PID = null, FIN_KZ = false;
async function ladujFin(pid = REAL_ID, kz = false) {
  FIN_PID = pid; FIN_KZ = kz;
  FIN = await api(`/api/projekty/${pid}/finansowanie`).catch(() => null); if (FIN) rysujFin();
}
function rysujFin() {
  const P = FIN_KZ ? "#kzfin" : "#fin"; if (!$(P + "-tresc")) return;
  const F = FIN, kol = {czerwony: "#dc2626", zolty: "#ca8a04", zielony: "#16a34a"}, kropka = k => `<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${kol[k] || "#999"};margin-right:6px"></span>`;
  const czerw = F.kontrole.filter(k => k.kolor === "czerwony").length, rozb = F.porownanie.filter(p => p.status === "rozbiezne" || p.status === "brak").length;
  if ($(P + "-stan")) $(P + "-stan").textContent = !F.zrodla.length ? "brak źródeł" : FIN_KZ ? odm(F.zrodla.length, "źródło", "źródła", "źródeł") : czerw || rozb ? `${czerw + rozb} do wyjaśnienia` : "bez kolizji";
  const H = F.harmonogram || {etapy: []};
  const pole = (z, k, et, typ = "text") => `<label>${et}<input data-fin="${z.id}.${k}" type="${typ}" value="${esc((z.wymagania || {})[k] ?? "")}"></label>`;
  $(P + "-tresc").innerHTML = `<p class="opis">${FIN_KZ ? `Jeśli prace są kredytowane albo dofinansowane (kredyt, premia BGK, KPO, dotacja), dodaj źródło i wgraj umowę (albo promesę / wniosek).
      Program odczyta terminy, transze i wymagania instytucji – trafią do zapytania, wzoru umowy i harmonogramu w kroku „Komplet dokumentów” i do sprawdzenia w kroku 6.
      Po zawarciu umowy z wykonawcą te same dane służą w realizacji do kontroli harmonogramu i przepływów.`
      : `Wgraj umowę kredytu, premii BGK albo dofinansowania (z załącznikami). Program odczyta terminy, transze, koszty kwalifikowalne i wymagania wobec umowy z wykonawcą,
      a potem porówna je z harmonogramem i umową wykonawcy. Wynik to propozycje do sprawdzenia – zmiany uzgadnia się z wykonawcą i instytucją finansującą.`}</p>
    ${F.zrodla.map(z => { const W = z.wymagania || {}; return `<div class="karta" style="margin:8px 0;padding:10px 14px">
      <div class="pasek" style="flex-wrap:wrap"><select onchange="finZapisz('${z.id}', {typ: this.value})">${Object.entries(F.typy).map(([k, t]) => `<option value="${k}" ${k === z.typ ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>
        <input value="${esc(z.instytucja || "")}" placeholder="instytucja (bank, BGK, instytucja pośrednicząca)" style="width:260px" onchange="finZapisz('${z.id}', {instytucja: this.value})">
        <label class="przycisk maly" data-ik="wgraj">Wgraj umowę i załączniki<input type="file" multiple hidden accept=".pdf,.docx,.doc,.xlsx,.jpg,.png" onchange="finPliki('${z.id}', this.files)"></label>
        ${z.pliki.length ? `<button class="maly" data-ik="iskra" onclick="finOdczyt('${z.id}')">${z.odczytano ? "Odczytaj ponownie (AI)" : "Odczytaj umowę (AI)"}</button>`
          : '<span class="opis" style="margin:0">wgraj umowę, żeby AI odczytało wymagania – albo wpisz dane poniżej</span>'}
        <button class="maly" onclick="if (confirm('Usunąć to źródło finansowania?')) finZapisz('${z.id}', {usun: true})">Usuń</button></div>
      ${z.pliki.length ? `<p class="opis" style="margin:4px 0">Pliki: ${z.pliki.map(esc).join(", ")}${z.odczytano ? ` · odczytano ${esc(z.odczytano)}` : ""}</p>` : ""}
      ${z.typ === "promesa" ? '<p class="opis" style="margin:4px 0">Promesa BGK: wypłata po odbiorze (jednorazowo po zakończeniu albo w transzach wg promesy), zwykle bezpośrednio wykonawcy – najpierw zamawiający płaci z wkładu własnego. Wpisz terminy transz z promesy; bez nich program przyjmie wpływ po zapłacie za ostatni etap.</p>' : ""}
      ${["kredyt", "pozyczka"].includes(z.typ) && F.jst ? '<p class="opis" style="margin:4px 0;background:var(--zolty-jasny);padding:4px 8px;border-radius:6px">Kredyt / pożyczka gminy: sprawdź w WPF indywidualny wskaźnik zadłużenia (art. 243 ustawy o finansach publicznych) na każdy rok spłaty i limit zobowiązań – program go nie liczy.</p>' : ""}
      <div class="siatka">${pole(z, "kwota", "Kwota finansowania [zł]", "number")}${(z.wymagania || {}).wklad_wlasny ? `<label>Wkład własny wg tej umowy (informacyjnie)<input disabled value="${esc(String(z.wymagania.wklad_wlasny))}"></label>` : ""}
        ${pole(z, "termin_zakonczenia_realizacji", "Termin zakończenia realizacji", "date")}${pole(z, "termin_rozliczenia", "Termin rozliczenia")}
        ${pole(z, "okres_kwalifikowalnosci_od", "Kwalifikowalność od", "date")}${pole(z, "okres_kwalifikowalnosci_do", "Kwalifikowalność do", "date")}</div>
      <button class="maly" data-ik="zapisz" onclick="finZapiszPola('${z.id}')">Zapisz dane</button>
      ${(W.transze || []).length ? `<h4 style="margin:10px 0 4px">Transze</h4><div class="tabela-okno"><table class="tabela"><tr><th>Nr</th><th>Kwota</th><th>Termin</th><th>Warunek wypłaty</th></tr>
        ${W.transze.map(t => `<tr><td>${esc(String(t.nr ?? ""))}</td><td class="liczba">${t.kwota ? zl(+t.kwota) : "–"}</td><td>${t.termin ? esc(/^\d{4}-\d\d-\d\d$/.test(t.termin) ? dataPl(t.termin) : t.termin) : "–"}</td><td><small>${esc(t.warunek || "")}</small></td></tr>`).join("")}</table></div>` : ""}
      ${(W.dokumenty_rozliczenia || []).length ? `<details style="margin-top:6px"><summary>Dokumenty do rozliczenia (${W.dokumenty_rozliczenia.length})</summary><ul class="lista">${W.dokumenty_rozliczenia.map(d => `<li>${esc(d.dokument || "")}${d.kiedy ? ` <small class="opis">– ${esc(d.kiedy)}</small>` : ""}</li>`).join("")}</ul></details>` : ""}
      ${(W.sankcje || []).length ? `<details><summary>Sankcje (${W.sankcje.length})</summary><ul class="lista">${W.sankcje.map(x => `<li>${esc(typeof x === "string" ? x : JSON.stringify(x))}</li>`).join("")}</ul></details>` : ""}
    </div>`; }).join("")}
    <button class="maly" data-ik="plus" onclick="finZapisz('', {typ: 'kredyt'})">Dodaj źródło finansowania</button>
    ${F.zrodla.length ? `<div class="karta" style="margin:8px 0;padding:10px 14px"><b>Wkład własny inwestycji</b> <span class="opis">– jeden dla wszystkich źródeł (nie wpisuj go przy każdej umowie)</span>
      ${F.wklad_wlasny_migracja ? `<div class="ramka-uwaga" style="margin:6px 0">${esc(F.wklad_wlasny_migracja)}</div>` : ""}
      <div class="pasek" style="margin-top:6px"><label>Wkład własny [zł]<input id="fin-wklad" inputmode="decimal" value="${esc(F.wklad_wlasny ? String(F.wklad_wlasny) : "")}" style="width:160px"></label>
        <button class="maly" data-ik="zapisz" onclick="finWklad()">${F.wklad_wlasny_migracja ? "Zatwierdź kwotę" : "Zapisz wkład własny"}</button></div></div>` : ""}
    ${FIN_KZ ? (F.zrodla.length ? `<h4 class="grupa-analizy">Harmonogram pod finansowanie</h4>
      ${H.koniec_najpozniej ? `<p>Zakończenie robót najpóźniej: <b>${esc(dataPl(H.koniec_najpozniej))}</b> <small class="opis">– 30 dni przed terminem z umowy finansowania (odbiór końcowy, dokumenty do rozliczenia)</small></p>` : '<p class="opis">Uzupełnij termin zakończenia realizacji z umowy finansowania.</p>'}
      ${H.etapy.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Etap</th><th>Odbiór do</th><th>Transza</th></tr>${H.etapy.map(e => `<tr><td>${esc(e.opis)}</td><td>${e.do ? esc(dataPl(e.do)) : "–"}</td><td class="liczba">${e.kwota ? zl(+e.kwota) : "–"}</td></tr>`).join("")}</table></div>` : ""}
      <p class="opis">Te terminy i wymagania instytucji trafią do dokumentów (krok 5) – po zmianie finansowania przygotuj dokumenty ponownie.</p>` : "")
    : F.zrodla.length ? `<h4 class="grupa-analizy">Terminy, kwalifikowalność, kwoty i transze${F.termin_wykonawcy ? ` <small class="opis">(koniec robót wykonawcy: ${esc(dataPl(F.termin_wykonawcy))})</small>` : ""}</h4>
      ${F.kontrole.map(k => `<div style="margin:3px 0">${kropka(k.kolor)}<b>${esc(k.obszar)}:</b> ${esc(k.opis)}</div>`).join("") || '<p class="opis">Uzupełnij dane finansowania i harmonogram wykonawcy.</p>'}
      <h4 class="grupa-analizy">Przepływy pieniężne</h4>
      ${F.przeplywy.miesiace.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Miesiąc</th><th>Płatności dla wykonawcy</th><th>Wpływy z finansowania</th><th>Saldo narastająco</th></tr>
        ${F.przeplywy.miesiace.map(m => `<tr><td>${esc(m.miesiac)}</td><td class="liczba">${zl(m.platnosci)}</td><td class="liczba">${zl(m.wplywy)}</td><td class="liczba ${m.saldo < 0 ? "czerwone" : ""}">${zl(m.saldo)}</td></tr>`).join("")}</table></div>
        <p>Największe zapotrzebowanie na środki własne (prefinansowanie): <b>${zl(F.przeplywy.najwieksza_luka)}</b> <small class="opis">– płatność faktury ${30} dni po końcu etapu, wpływy według terminów transz</small></p>`
        : '<p class="opis">Brak danych – potrzebne etapy harmonogramu z wartościami i terminy transz.</p>'}
      <h4 class="grupa-analizy">Umowa z wykonawcą a wymagania finansującego</h4>
      <div class="pasek"><button class="maly" data-ik="iskra" onclick="finPorownaj()">Porównaj z umową wykonawcy (AI)</button>
        <a class="przycisk maly" data-ik="dokument" href="/api/projekty/${FIN_PID}/finansowanie/raport.docx">Raport (Word)</a>
        ${F.porownanie_data ? `<span class="opis">porównano ${esc(F.porownanie_data)}</span>` : ""}</div>
      ${F.porownanie.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Wymaganie finansującego</th><th>Status</th><th>Umowa z wykonawcą</th><th>Propozycja do aneksu</th></tr>
        ${F.porownanie.map(p => `<tr><td>${esc(p.wymog || "")}<br><small class="opis">${esc(p.zrodlo || "")}</small></td>
          <td><span class="znacznik ${p.status === "zgodne" ? "z-wygrany" : p.status === "do_sprawdzenia" ? "z-do-analizy" : "z-przegrany"}">${esc(F.statusy[p.status] || p.status)}</span></td>
          <td><small>${esc(p.komentarz || "")}${p.cytat_umowy ? `<br><i>„${esc(p.cytat_umowy.slice(0, 220))}”</i>` : ""}</small></td><td><small>${esc(p.propozycja_aneksu || "")}</small></td></tr>`).join("")}</table></div>` : ""}` : ""}`;
}
async function finZapisz(id, json) { const r = await bezpiecznie(() => api(`/api/projekty/${FIN_PID}/finansowanie/zrodlo`, {json: {id, ...json}})); if (r) { FIN = r; rysujFin(); finKz(); } return r; }
function finKz() { if (FIN_KZ && FIN_PID === PROJEKT_ID) api(`/api/projekty/${PROJEKT_ID}/kreator`).then(r => { if (r && FIN_PID === PROJEKT_ID) KZ = r; }).catch(() => {}); }  // stan listy kontrolnej (krok 7)
function finZapiszPola(id) {
  const w = {}; document.querySelectorAll(`[data-fin^="${id}."]`).forEach(e => w[e.dataset.fin.split(".")[1]] = e.value);
  finZapisz(id, {wymagania: w}).then(r => { if (r) komunikat("Zapisano."); });  // błąd (np. data 31.02) – zostaje komunikat o błędzie
}
async function finWklad() { const r = await bezpiecznie(() => api(`/api/projekty/${FIN_PID}/finansowanie/wklad`, {json: {wklad_wlasny: $("#fin-wklad").value}})); if (r) { FIN = r; rysujFin(); finKz(); komunikat("Zapisano wkład własny inwestycji."); } }
async function finPliki(id, files) {
  if (!files.length) return; const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  const r = await bezpiecznie(() => api(`/api/projekty/${FIN_PID}/finansowanie/${id}/pliki`, {method: "POST", body: fd})); if (r) { FIN = r; rysujFin(); finKz(); komunikat("Wgrano – kliknij „Odczytaj umowę (AI)”."); }
}
async function finOdczyt(id) { const [p, k] = [FIN_PID, FIN_KZ]; sledz(await bezpiecznie(() => api(`/api/projekty/${p}/finansowanie/${id}/odczyt`, {method: "POST"})), () => { ladujFin(p, k); if (k) finKz(); }); }
async function finPorownaj() { const p = FIN_PID; sledz(await bezpiecznie(() => api(`/api/projekty/${p}/finansowanie/porownanie`, {method: "POST"})), () => ladujFin(p)); }
// ---------------------------------------------------------------- wspólnota: Moje zapytania
let ZW_ID = null;
function kzOdswiez() { return WIDOK === "zam_zapytania" ? ladujZapytaniaWsp() : ladujKreator(); }
async function ladujZapytaniaWsp() {
  const L = await bezpiecznie(() => api("/api/zam/zapytania")); if (!L) return;
  if (ZW_ID && !L.some(x => x.id === ZW_ID)) ZW_ID = null;
  if (!ZW_ID && L.length) ZW_ID = (L.find(x => x.dni != null && x.dni >= 0 && x.dni <= 5 && !x.oferty) || L[0]).id;
  const kol = x => x.status === "w przygotowaniu" ? "z-do-analizy" : x.status === "po terminie" ? "z-przegrany" : "z-wygrany";
  let szczeg = "";
  if (ZW_ID) {
    PROJEKT_ID = ZW_ID;
    const S = await api(`/api/projekty/${ZW_ID}/kreator`).catch(() => null), x = L.find(y => y.id === ZW_ID);
    if (S && x) szczeg = `<div class="karta"><h3 style="margin-top:0">${esc(x.nazwa)}</h3>
      <p><span class="znacznik ${kol(x)}">${esc(x.status)}</span> ${x.termin_ofert ? `termin składania ofert <b>${dataPl(x.termin_ofert)}</b>${x.dni != null ? (x.dni >= 0 ? ` (za ${odm(x.dni, "dzień", "dni", "dni")})` : " (minął)") : ""} · ` : "termin nie ustalony · "}ofert: <b>${x.oferty}</b>${x.zaproszono ? ` · zaproszono: ${x.zaproszono}` : ""}</p>
      ${x.dni != null && x.dni >= 0 && x.dni <= 5 && !x.oferty ? `<div class="ramka-uwaga"><b>Nikt jeszcze nie złożył oferty, a do terminu ${odm(x.dni, "został", "zostały", "zostało")} ${odm(x.dni, "dzień", "dni", "dni")}.</b> Zaprosić wykonawców z okolicy, którzy wykonywali podobne prace?</div>` : ""}
      <div class="pasek"><button class="maly" data-ik="folder" onclick="TRYB='zamowienie'; pokaz('zam_projekty'); PROJEKT_ID='${x.id}'; otworzProjekt('${x.id}')">Otwórz zapytanie</button>
        <button class="maly" data-ik="trofeum" onclick="ocDlaZapytania('${x.id}')">Sprawdź złożone oferty</button></div>
      ${!x.termin_ofert ? `<p class="opis">Ustal termin składania ofert w kreatorze (krok „Warunki”) – wtedy program przypomni o nim 5 dni wcześniej.</p>` : ""}
      ${kzZaproszenia(S)}</div>`;
  }
  $("#zam-zapytania").innerHTML = `<div class="zw-uklad">
    <div><button class="glowny" data-ik="plus" onclick="pokaz('zam_nowe')">Przygotuj zamówienie</button>
      <ul class="zw-lista">${L.map(x => `<li class="${x.id === ZW_ID ? "akt" : ""}" onclick="ZW_ID='${x.id}'; ladujZapytaniaWsp()">${esc(x.nazwa)}
        <small>${esc(x.status)}${x.termin_ofert ? " · " + dataPl(x.termin_ofert) : ""} · ${odm(x.oferty, "oferta", "oferty", "ofert")}</small></li>`).join("") || '<li class="opis">Brak zapytań – zacznij od „Przygotuj zamówienie”.</li>'}</ul></div>
    <div>${szczeg}</div></div>`;
  wstawIkony($("#zam-zapytania"));
}
async function ocDlaZapytania(pid) {  // „Sprawdź złożone oferty” zapytania – powiązana ocena z dokumentami i kryteriami zapytania
  const r = await bezpiecznie(() => api(`/api/projekty/${pid}/kreator/ocena`, {method: "POST"})); if (!r) return;
  OC_ID = r.id; pokaz("zam_oferty");
}
async function nowaInwestycja() {
  const nazwa = prompt("Nazwa inwestycji (np. Termomodernizacja budynku Lipowa 5):"); if (!nazwa) return;
  const wyk = prompt("Wykonawca (nazwa firmy):") || "", nip = prompt("NIP wykonawcy (opcjonalnie):") || "", netto = prompt("Wartość umowy netto [zł]:") || "";
  // stawka VAT z umowy: 8% – budownictwo objęte społecznym programem mieszkaniowym (lokale mieszkalne), 23% – m.in. lokale użytkowe, garaże
  let vat = (prompt("Stawka VAT z umowy [%] – 8 (budownictwo mieszkaniowe objęte społecznym programem mieszkaniowym) albo 23 (np. lokale użytkowe, garaże). Puste = uzupełnisz w danych umowy:", "") || "").replace("%", "").trim();
  if (vat && !["0", "5", "8", "23"].includes(vat)) return komunikat("Stawka VAT: 0, 5, 8 albo 23.", true);
  const r = await bezpiecznie(() => api("/api/zam/inwestycja", {json: {nazwa, wykonawca_nazwa: wyk, wykonawca_nip: nip, cena_netto: netto, vat}})); if (!r) return;
  await bezpiecznie(() => api(`/api/projekty/${r.id}/status`, {json: {status: "realizacja"}}));
  komunikat("Dodano inwestycję – uzupełnij umowę, harmonogram i finansowanie."); await ladujRealizacje(); otworzRealizacje(r.id);
}
// ostatni krok: czego brakuje do publikacji (dokumenty główne, sprawdzenie w kroku 6)
function kzBrakiPublikacji(S) {
  const B = [];
  if (!stanKroku(S, "dokumenty")) B.push(S.sciezka === "wzory" ? "nie wgrano Twoich wzorów dokumentów" : `nie przygotowano: ${esc((S.dokumenty_brak || []).join(", ") || "dokumentów zamówienia")} (krok „Komplet dokumentów”)`);
  else if (!stanKroku(S, "zmiany")) B.push("dokumenty nie zostały sprawdzone i zatwierdzone w kroku „Sprawdzenie i zmiany”");
  if (!stanKroku(S, "wartosc")) B.push(S.prywatny ? "brak wartości zamówienia" : "wartość zamówienia nie jest ustalona szacowaniem (krok „Wartość i tryb”)");
  return B.length ? `<div class="ramka-uwaga" id="kz-braki"><b>Komplet nie jest gotowy do ${S.prywatny ? "wysłania" : "publikacji"}:</b><ul class="lista">${B.map(b => `<li>${b}</li>`).join("")}</ul></div>` : "";
}
function kzZipPotwierdz() {
  return !$("#kz-braki") || confirm("Komplet nie jest gotowy (" + $("#kz-braki").innerText.replace(/\s+/g, " ").slice(0, 300) + ").\n\nPobrać mimo to?");
}
// ---------------------------------------------------------------- po publikacji (zamawiający publiczny): kalendarz terminów, pytania wykonawców, zmiana SWZ
function kzPostepowanie(S) {
  const P = S.postepowanie; if (!P) return "";
  const stan = d => d < 0 ? '<span class="opis">minął</span>' : d === 0 ? '<b class="czerwone">dziś</b>' : d <= 3 ? `<b class="czerwone">za ${odm(d, "dzień", "dni", "dni")}</b>` : `za ${odm(d, "dzień", "dni", "dni")}`;
  const art = P.unijne ? "art. 135" : "art. 284";
  return `<div class="karta" id="kz-post" style="margin:8px 0;padding:10px 14px;border-left:4px solid #1F5A99">
    <b>Kalendarz postępowania</b> <small class="opis">– ${P.unijne ? "postępowanie od progów UE" : "postępowanie krajowe (poniżej progów UE)"}</small>
    <div class="siatka"><label>Publikacja ogłoszenia<input type="date" id="kzp-pub" value="${esc(P.data_publikacji)}"></label>
      <label>Termin składania ofert<input type="date" value="${esc(S.K.termin_ofert || "")}" disabled title="Zmiana: krok „Warunki” albo przedłużenie terminu poniżej"></label>
      <label>Zawiadomienie o wyborze przesłane<input type="date" id="kzp-wyb" value="${esc(P.data_wyboru)}"></label></div>
    <div class="pasek"><button class="maly" data-ik="zapisz" onclick="kzPostZapisz()">Zapisz daty</button></div>
    ${[...new Set((P.ostrzezenia || []).concat(P.kalendarz.filter(k => k.ostrzezenie).map(k => k.co.replace(/^UWAGA: /, ""))))].map(o => `<div class="ramka-uwaga" style="margin:6px 0">⚠ ${esc(o)}</div>`).join("")}
    ${P.kalendarz.length ? `<div class="tabela-okno"><table class="tabela kz-kal"><tr><th>Data</th><th>Co</th><th>Kiedy</th><th>Podstawa</th></tr>
      ${P.kalendarz.filter(k => !k.ostrzezenie).map(k => `<tr class="${k.dni < 0 ? "wyszarz" : ""}"><td data-et="Data">${esc(dataPl(k.data))}</td><td data-et="Co">${esc(k.co)}</td><td data-et="Kiedy">${stan(k.dni)}</td><td data-et="Podstawa"><small>${esc(k.podstawa)}</small></td></tr>`).join("")}</table></div>`
      : '<p class="opis">Ustal termin składania ofert w kroku „Warunki” – program wyliczy terminy pytań, otwarcia ofert i związania ofertą.</p>'}
    <small class="opis">Terminy liczone w dniach kalendarzowych; termin kończący się w sobotę lub niedzielę przesuwa się na poniedziałek (święta – sprawdź sam).</small></div>
  <div class="karta" id="kz-pytania" style="margin:8px 0;padding:10px 14px;border-left:4px solid #ca8a04">
    <b>Pytania wykonawców i wyjaśnienia SWZ</b> <small class="opis">– ${art}: odpowiedź obowiązkowa, gdy wniosek wpłynął w terminie; publikacja bez ujawniania pytającego</small>
    <div class="pasek" style="flex-wrap:wrap"><label style="margin:0">Wpłynęło <input type="date" id="kzq-data" value="${new Date().toISOString().slice(0, 10)}"></label>
      <textarea id="kzq-tresc" placeholder="Treść pytania wykonawcy" style="flex:1;min-width:240px;min-height:44px"></textarea>
      <button class="maly" data-ik="plus" onclick="kzPytanieDodaj()">Dodaj pytanie</button></div>
    ${P.pytania.map((q, i) => `<div class="ds-zam" data-kzq="${q.id}"><div class="pasek" style="flex-wrap:wrap"><b>Pytanie ${i + 1}</b> <small class="opis">wpłynęło ${esc(dataPl(q.data))}</small>
        ${q.w_terminie ? `<span class="znacznik ${q.po_terminie_odpowiedzi ? "z-czerwony" : q.odpowiedz ? "z-wygrany" : "z-do-analizy"}">${q.odpowiedz ? "odpowiedź przygotowana" : q.po_terminie_odpowiedzi ? "minął termin odpowiedzi – przedłuż termin składania ofert" : "odpowiedz do " + esc(dataPl(q.odpowiedz_do))}</span>`
          : '<span class="znacznik z-odpuszczamy">po terminie – odpowiedź nieobowiązkowa</span>'}</div>
      <p style="margin:4px 0">${esc(q.tresc || "")}</p>
      <textarea class="kzq-odp" placeholder="Odpowiedź zamawiającego">${esc(q.odpowiedz || "")}</textarea>
      ${q.podstawa ? `<small class="opis">Podstawa (AI): ${esc(q.podstawa)}</small>` : ""}
      <div class="pasek" style="flex-wrap:wrap"><label class="wiersz" style="margin:0"><input type="checkbox" class="kzq-zm" ${q.zmiana_swz ? "checked" : ""}> odpowiedź zmienia SWZ</label>
        <input class="kzq-zmop" placeholder="co zmienić w SWZ (punkt, nowe brzmienie)" value="${esc(q.zmiana_opis || "")}" style="flex:1;min-width:200px">
        ${q.przedluzenie_ai ? '<span class="znacznik z-do-analizy">AI: rozważ przedłużenie terminu składania ofert</span>' : ""}</div>
      <div class="pasek"><button class="maly" data-ik="zapisz" onclick="kzPytanieZapisz('${q.id}')">Zapisz</button>
        <button class="maly" data-ik="iskra" onclick="kzPytanieAI('${q.id}')">Projekt odpowiedzi (AI)</button>
        <button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć pytanie?')) kzPytanie({id: '${q.id}', usun: true})"></button></div></div>`).join("")}
    <h4 class="grupa-analizy">Zmiana SWZ – przedłużenie terminu składania ofert</h4>
    <div class="pasek" style="flex-wrap:wrap"><label style="margin:0">Nowy termin <input type="date" id="kzq-nowy"></label>
      <input id="kzq-powod" placeholder="powód (np. odpowiedzi na pytania, zmiana opisu przedmiotu)" style="flex:1;min-width:220px">
      <button class="maly" onclick="kzPrzedluz()">Przedłuż termin</button></div>
    ${P.zmiany_terminu.length ? `<ul class="lista">${P.zmiany_terminu.map(z => `<li>${esc(dataPl(z.stary) || "–")} → <b>${esc(dataPl(z.nowy))}</b>${z.powod ? ` <small class="opis">– ${esc(z.powod)}</small>` : ""}</li>`).join("")}</ul>` : ""}
    <div class="pasek"><a class="przycisk maly" data-ik="dokument" href="/api/projekty/${S.projekt.id}/kreator/wyjasnienia.docx">Wyjaśnienia${P.pytania.some(q => q.zmiana_swz) || P.zmiany_terminu.length ? " i zmiana SWZ" : " treści SWZ"} (Word)</a></div>
    <small class="opis">${P.unijne ? "Zmiana ogłoszenia – ogłoszenie o zmianach w Dzienniku Urzędowym UE (art. 137)." : "Zmiana ogłoszenia – ogłoszenie o zmianie w BZP (art. 286 ust. 9), komunikat o przedłużeniu na stronie postępowania (art. 286 ust. 5)."}</small></div>`;
}
async function kzPost(url, json) { const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/${url}`, {json})); if (r) { KZ = r; rysujKreator(); } return r; }
function kzPostZapisz() { kzPost("postepowanie", {data_publikacji: $("#kzp-pub").value, data_wyboru: $("#kzp-wyb").value}).then(r => r && komunikat("Zapisano.")); }
function kzPytanie(json) { return kzPost("pytanie", json); }
function kzPytanieDodaj() { const t = $("#kzq-tresc").value.trim(); if (!t) return komunikat("Wpisz treść pytania.", true); kzPytanie({tresc: t, data: $("#kzq-data").value}); }
function kzPytanieZapisz(id) {
  const e = document.querySelector(`[data-kzq="${id}"]`);
  return kzPytanie({id, odpowiedz: e.querySelector(".kzq-odp").value, zmiana_swz: e.querySelector(".kzq-zm").checked, zmiana_opis: e.querySelector(".kzq-zmop").value}).then(r => r && komunikat("Zapisano."));
}
async function kzPytanieAI(id) {
  const e = document.querySelector(`[data-kzq="${id}"]`);
  if (e.querySelector(".kzq-odp").value.trim() && !confirm("Zastąpić wpisaną odpowiedź projektem AI?")) return;
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/pytanie/${id}/ai`, {method: "POST"})), () => ladujKreator());
}
function kzPrzedluz() {
  const t = $("#kzq-nowy").value; if (!t) return komunikat("Podaj nowy termin składania ofert.", true);
  kzPost("przedluz", {termin: t, powod: $("#kzq-powod").value}).then(r => r && komunikat("Termin składania ofert przedłużony – opublikuj zmianę SWZ i ogłoszenie o zmianie."));
}
async function zapiszKreator(json, dalej) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator`, {json})); if (!r) return;
  KZ = r; if (json.nazwa) { PROJEKT.nazwa = json.nazwa; }
  if (dalej) { const kr = krokiKreatora(KZ), i = kr.findIndex(k => k[0] === KZ_AKT); KZ_AKT = (kr[i + 1] || kr[i])[0]; }
  rysujKreator(); komunikat("Zapisano.");
}
async function wgrajWzoryKz(files) {
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); fd.append("biblioteka", $("#kz-bibl")?.checked ? "1" : "0");
  let r;
  try { r = await api(`/api/projekty/${PROJEKT_ID}/kreator/wzory`, {body: fd, method: "POST"}); }
  catch (e) {
    if (!(e.dane || {}).zastap) return komunikat(e.message, true);
    if (!confirm(e.message + "\n\nZastąpić?")) return;
    const fd2 = new FormData(); [...files].forEach(f => fd2.append("pliki", f)); fd2.append("biblioteka", $("#kz-bibl")?.checked ? "1" : "0"); fd2.append("zastap", "1");
    r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/wzory`, {body: fd2, method: "POST"})); if (!r) return;
  }
  KZ = r; rysujKreator();
  const k = r.konwersja || [], uw = [];
  if (k.length) uw.push("PDF: " + k.map(x => `${x.plik} – ${x.ok ? "zamieniony na Word (zmiany będą wprowadzane automatycznie)" : x.opis}`).join("; "));
  if ((r.pominiete || []).length) uw.push(`Limit to 10 plików na jedno wgranie – pominięto: ${r.pominiete.join(", ")}`);
  if ((r.bez_auto || []).length) uw.push(`${r.bez_auto.join(", ")}: program odczyta ten plik, ale zmian nie wprowadzi w nim sam – wgraj wersję Word (.docx)`);
  komunikat("Wgrano wzory. " + uw.join(". "), k.some(x => !x.ok) || !!(r.pominiete || []).length || !!(r.bez_auto || []).length);
}
async function usunWzorKz(nazwa) { const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/wzory/usun`, {json: {nazwa}})); if (r) { KZ = r; rysujKreator(); } }
async function kosztorysKreatora() {
  if ($("#kz-ilosci") && $("#kz-ilosci").value !== ((KZ.K.potrzeba || {}).ilosci || "")) await zapiszKreator({potrzeba: {ilosci: $("#kz-ilosci").value}});
  const p = KZ.K.potrzeba || {}, w = $("#wsk-oferta");
  // ilości: z dokumentów (krok 1 projektu albo Twoje wzory) lub z odpowiedzi w kreatorze – program ich nie zgaduje
  const maDok = (PROJEKT.pliki || []).some(f => f.uwzglednij) || (KZ.wzory || []).length > 0;
  const maIlosci = [KZ.K.opis, ...Object.values(p)].some(t => /\d/.test(String(t || "")));
  if (KZ.rodzaj !== "roboty" && !maDok && !maIlosci &&
      !confirm("Nie podano ilości (np. „obiady – 606 porcji”) ani dokumentów z ilościami (ogłoszenie / SWZ).\n\n"
               + "Program nie zgaduje ilości – pozycje dostaną ilość 0 do uzupełnienia. Kontynuować?\n\n(Anuluj = uzupełnij ilości w kroku „Szczegóły”.)")) {
    $("#kz-ilosci")?.focus(); return;
  }
  if (w) w.value = [KZ.K.opis, ...Object.values(p)].filter(Boolean).join(". ");  // zawsze aktualne odpowiedzi z kreatora (ilości!)
  await generujOferte();
}
async function dokumentyKreatora() {
  const dok = [...document.querySelectorAll(".kz-dok:checked")].map(e => e.value);
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/dokumenty`, {json: {dokumenty: dok, formularz: !!$("#kz-form")?.checked}})), odswiezProjekt);
}
async function notatkaKreatora() {  // notatka z szacowania z listy kontrolnej – bez opuszczania kreatora
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/notatka-szacowania`, {json: {}})); if (!r) return;
  komunikat("Przygotowano notatkę z szacowania."); ladujKreator();
}
async function wzorZBiblioteki(rodzaj, nazwa) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/wzory/z-biblioteki`, {json: {rodzaj, nazwa}})); if (r) { KZ = r; rysujKreator(); komunikat("Dodano wzór: " + nazwa); }
}
async function usunZBiblioteki(rodzaj, nazwa) {
  if (!confirm(`Usunąć „${nazwa}” z biblioteki „Moje wzory”? (Zamówienia, które już go mają, zachowują swoją kopię.)`)) return;
  if (await bezpiecznie(() => api("/api/zam/wzory/usun", {json: {rodzaj, nazwa}}))) ladujKreator();
}
async function przygotujOswiadczenia() {  // tylko oświadczenia i wykazy (art. 125) – bez przygotowywania całego kompletu od nowa
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/dokumenty`, {json: {dokumenty: ["oswiadczenia"], formularz: false}})), ladujKreator);
}
async function przegladKreatora() {
  if (KZ && (KZ.propozycje || []).some(p => p.decyzja) && !confirm("Nowe sprawdzenie zaczyna listę propozycji od nowa – dotychczasowe decyzje zostaną usunięte. Kontynuować?")) return;
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/przeglad`, {json: {dodatkowe: $("#kz-dod").value, model: ($("#kz-model") || {}).value || "standardowy"}})), ladujKreator); }
function zebraneNowe() { const o = {}; document.querySelectorAll(".kz-nowy").forEach(t => o[t.dataset.id] = t.value); return o; }
async function decyzjaKz(id, d) {
  const nowe = zebraneNowe();
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/decyzje`, {json: {decyzje: {[id]: {decyzja: d, nowy: nowe[id]}}}})); if (r) { KZ = r; rysujKreator(); }
}
async function decyzjaWszystkie(d) {
  const nowe = zebraneNowe(), dec = {}; KZ.propozycje.forEach(p => dec[p.id] = {decyzja: d, nowy: nowe[p.id]});
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/decyzje`, {json: {decyzje: dec}})); if (r) { KZ = r; rysujKreator(); }
}
// uwagi z kroku „Sprawdzenie i zmiany” do pobrania – najpierw zapis poprawionych brzmień z pól tekstowych, żeby raport = to, co na ekranie
async function pobierzUwagiKz() {
  const dec = {};
  document.querySelectorAll(".kz-nowy").forEach(t => { const p = (KZ.propozycje || []).find(x => x.id === t.dataset.id);
    if (p && t.value !== (p.nowy_edyt ?? p.nowy)) dec[p.id] = {decyzja: p.decyzja || "", nowy: t.value}; });
  if (Object.keys(dec).length) { const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/decyzje`, {json: {decyzje: dec}})); if (!r) return; KZ = r; }
  location.href = `/api/projekty/${PROJEKT_ID}/kreator/uwagi.docx?zakres=${encodeURIComponent($("#kz-uwagi-zakres").value)}`;
}
// krok 6: po rozstrzygnięciu każdej pozycji – wprowadzenie zaakceptowanych zmian (albo komplet bez zmian) i przejście do „Gotowe do publikacji”
async function zatwierdzKreator() {
  const P = KZ.propozycje || [], nowe = zebraneNowe(), dec = {};
  if (P.some(p => !p.decyzja)) return komunikat("Najpierw rozstrzygnij każdą pozycję: akceptuj albo odrzuć.", true);
  P.filter(p => p.decyzja === "tak").forEach(p => dec[p.id] = {decyzja: "tak", nowy: nowe[p.id]});
  if (Object.keys(dec).length && !await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/decyzje`, {json: {decyzje: dec}}))) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/wprowadz`, {method: "POST"})); if (!r) return;
  KZ = r; KZ_AKT = "gotowe"; rysujKreator(); window.scrollTo(0, 0);
  const wpr = (r.wynik || []).reduce((a, w) => a + w.wprowadzone, 0);
  komunikat(wpr ? `Wprowadzono zmian: ${wpr}${r.reczne.length ? ` · do ręcznego wprowadzenia: ${r.reczne.length}` : ""}.` : "Dokumenty bez zmian – gotowe do publikacji.", !!r.reczne.length);
}

// ---------- wnioski o zmianę umowy i aneksy (wykonawca)
let WNIOSEK_OTWARTY = null;
let BLEDY_OTW = false;
function listaBledowDok(B) {  // błędy i różnice w dokumentacji przetargowej – z sprawdzenia dokumentacji i z analizy przy ofercie
  const kol = {krytyczna: "z-czerwony", istotna: "z-do-analizy", drobna: "z-odpuszczamy"};
  const grupy = {};
  B.forEach(b => (grupy[b.zrodlo || "inne"] = grupy[b.zrodlo || "inne"] || []).push(b));
  return `<div class="karta" id="wn-bledy" style="margin:10px 0"><div class="pasek" style="margin:0 0 6px"><b>Błędy dokumentacji przetargowej (${B.length})</b>
      <button class="maly" style="margin-left:auto" onclick="BLEDY_OTW = false; rysujProjekt()">Zwiń ▲</button></div>
    ${Object.entries(grupy).map(([g, L]) => `<h4 class="grupa-analizy">${esc(g.charAt(0).toUpperCase() + g.slice(1))} (${L.length})</h4>
      ${L.map(b => `<div class="alert-k ${b.waga === "krytyczna" ? "ostrzezenie" : ""}">
        <div class="alert-gora"><span class="znacznik ${kol[b.waga] || ""}">${esc(b.waga || "")}</span>${b.kategoria ? `<b>${esc(b.kategoria)}</b>` : ""}
          <small class="opis" style="margin:0">${b.dokument && b.dokument !== "analiza przy ofercie" ? esc(b.dokument) : ""}${b.odw ? " · " + odwChip(b.odw, b.miejsce, {typ: "projekt", id: PROJEKT_ID}) : b.miejsce ? " · " + esc(b.miejsce) : ""}</small></div>
        ${b.cytat ? `<div class="cytat">„${esc(b.cytat)}”</div>` : ""}
        <div>${odwWTresci(esc(b.opis || ""), b, {typ: "projekt", id: PROJEKT_ID})}</div>
        ${b.propozycja ? `<div class="sugestia"><b>${b.perspektywa === "wykonawca" ? "Co zrobić:" : "Propozycja:"}</b> ${esc(b.propozycja)}</div>` : ""}
        ${b.pytanie ? `<div class="cytat" style="border-left-color:#0284c7"><b>Pytanie do zamawiającego:</b> ${esc(b.pytanie)}</div>` : ""}</div>`).join("")}`).join("")}
    ${B.some(b => b.pytanie) ? `<div class="pasek"><button class="maly" data-ik="dokument" onclick="kopiujPytaniaBledow()">Kopiuj pytania do zamawiającego</button></div>` : ""}
    ${B.some(b => b.perspektywa !== "wykonawca" && b.zrodlo === "sprawdzenie dokumentacji") ? '<p class="opis">Część uwag pochodzi ze starszego sprawdzenia (porady dla zamawiającego) – kliknij „Sprawdź ponownie (AI)”, żeby dostać porady dla wykonawcy.</p>' : ""}</div>`;
}
function kopiujPytaniaBledow() {
  const t = ((PROJEKT || {}).bledy_dokumentacji || []).filter(b => b.pytanie).map((b, i) => `${i + 1}. ${b.pytanie}`).join("\n");
  navigator.clipboard?.writeText("Pytania dotyczące treści dokumentacji:\n" + t).then(() => komunikat("Skopiowano pytania do zamawiającego."), () => prompt("Skopiuj pytania:", t));
}
const RODZ_WN = {prace_dodatkowe: "a) Prace dodatkowe", roznice_dokumentacji: "b) Błędy dokumentacji", przeszkody: "c) Inne przeszkody"};
const PRZESZKODY = ["Wstrzymanie lub ograniczenie robót przez wojewódzkiego konserwatora zabytków", "Wstrzymanie robót decyzją organu (nadzór budowlany, RDOŚ, inne instytucje)",
  "Okres lęgowy ptaków / ochrona gatunkowa (np. jerzyki, nietoperze) – zakaz prowadzenia prac", "Znaleziska archeologiczne lub niewypały – wstrzymanie robót",
  "Kolizja z niewykazaną w dokumentacji infrastrukturą (sieci, instalacje)", "Brak przekazania terenu budowy / frontu robót przez Zamawiającego",
  "Oczekiwanie na decyzje, uzgodnienia lub dokumentację od Zamawiającego", "Siła wyższa", "Inna przyczyna niezależna od Wykonawcy"];
const plikL = (pid, sc, et) => sc ? `<a class="dozw" href="/pobierz/${pid}/${sc.split("/").map(encodeURIComponent).join("/")}">${et}</a>` : "";
// dokument jako ikona pliku (Word – niebieska, Excel – zielona) z podpisem
function plikIk(pid, sc, et, maly) {
  if (!sc) return "";
  const ext = (sc.split(".").pop() || "").toLowerCase(), xl = ext.startsWith("xls"), kol = xl ? "#16a34a" : ext === "pdf" ? "#dc2626" : "#2563eb";
  return `<a class="plik-ik ${maly ? "maly" : ""} dozw" href="/pobierz/${pid}/${sc.split("/").map(encodeURIComponent).join("/")}" title="Pobierz: ${esc(sc.split("/").pop())}">
    <svg viewBox="0 0 40 48" aria-hidden="true"><path d="M4 2h22l10 10v32a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z" fill="#fff" stroke="${kol}" stroke-width="2"/>
      <path d="M26 2v10h10" fill="none" stroke="${kol}" stroke-width="2"/>
      <rect x="0" y="26" width="30" height="13" rx="2" fill="${kol}"/><text x="15" y="35.5" text-anchor="middle" font-size="8.5" font-weight="700" fill="#fff" font-family="Arial">${xl ? "XLSX" : ext.toUpperCase()}</text>
      ${xl ? '<path d="M10 16h16M10 20h16M18 12v10" stroke="' + kol + '" stroke-width="1.4"/>' : '<path d="M9 13h14M9 17h18M9 21h12" stroke="' + kol + '" stroke-width="1.6"/>'}</svg>
    <span>${et}</span></a>`;
}
function sekcjaWnioskow(p) {
  const W_ = p.wnioski || [], um = p.umowa_dane || {}, B = p.bledy_dokumentacji || [];
  const stKl = {roboczy: "z-odpuszczamy", "złożony": "z-do-analizy", zaakceptowany: "z-startujemy", odrzucony: "z-czerwony"};
  const w = W_.find(x => x.id === WNIOSEK_OTWARTY);
  return `<div class="krok k-nieb" id="sek-wnioski"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Zmiany umowy: wnioski i aneksy</h3>
      <span class="stan">${W_.length ? odm(W_.length, "wniosek", "wnioski", "wniosków") : "brak wniosków"}</span></div><div class="tresc">
    <p class="opis">Wnioski do zamawiającego o przedłużenie terminu wykonania prac i zmianę wynagrodzenia. Po akceptacji wniosku program
      aktualizuje termin, wynagrodzenie i harmonogram oraz przygotowuje aneks do umowy z kosztorysem.</p>
    <div class="kwoty kafle-przetargu" style="margin-top:0"><div><span>Umowa</span><b>${esc(um.nr || "–")}</b><small>${um.data ? "z " + esc(dataPl(um.data)) : "uzupełnij w W realizacji"}</small></div>
      <div><span>Termin zakończenia</span><b>${um.termin ? esc(dataPl(um.termin)) : "–"}</b></div>
      <div><span>Wynagrodzenie netto</span><b>${zl(um.wartosc || 0)}</b></div>
      <div class="${B.length ? "pilne klik" : ""}" ${B.length ? `onclick="BLEDY_OTW = !BLEDY_OTW; rysujProjekt(); setTimeout(() => $('#wn-bledy')?.scrollIntoView({behavior:'smooth', block:'start'}), 100)" role="button" title="Pokaż listę błędów"` : ""}>
        <span>Błędy dokumentacji</span><b>${B.length}</b><small>${B.length ? (BLEDY_OTW ? "dotknij, aby zwinąć ▲" : "dotknij, aby zobaczyć ▼") : "wykryte przez program"}</small></div></div>
    ${B.length && BLEDY_OTW ? listaBledowDok(B) : ""}
    <div class="wn-rodzaje">
      <div class="wn-rodzaj"><div class="wn-lit">a)</div><div><b>Prace dodatkowe</b>
        <p>Roboty nieobjęte umową, bez których nie da się prawidłowo wykonać zamówienia. Wniosek zawiera wykaz prac i ich kosztorys
          (ceny z oferty lub rynkowe), wydłużenie terminu i kwotę do dopłaty.</p>
        <button class="maly zielony" data-ik="plus" onclick="nowyWniosek('prace_dodatkowe')">Nowy wniosek: prace dodatkowe</button></div></div>
      ${(() => {
        const wer = p.weryfikacja, sprawdzono = !!wer || B.length > 0, wnB = W_.filter(x => x.rodzaj === "roznice_dokumentacji");
        const ost = wnB[wnB.length - 1];
        const stan = sprawdzono
          ? `<div class="wn-gotowe">${ik("iskra")} <span><b>Sprawdzenie dokumentacji wykonane</b>${wer && wer.data ? ` (${esc(wer.data)})` : ""} –
              ${B.length ? `wykryto <b>${odm(B.length, "błąd lub różnicę", "błędy lub różnice", "błędów lub różnic")}</b>.` : "nie wykryto błędów."}
              ${B.length ? (ost ? ` Wniosek ${esc(ost.nr)} – status: <b>${esc(ost.status)}</b>.` : " <b>Możesz złożyć wniosek o przedłużenie terminu i zmianę ceny.</b>") : ""}</span></div>`
          : `<div class="wn-krok">1. Najpierw wykryj błędy w dokumentach – w <b>kroku 2</b> projektu.</div>`;
        return `<div class="wn-rodzaj ${sprawdzono && B.length && !ost ? "podswietl-wn" : ""}"><div class="wn-lit">b)</div><div><b>Błędy dokumentacji przetargowej</b>
          <p>Różnice między dokumentacją, na podstawie której zawarto umowę, a stanem rzeczywistym. Wniosek zawiera wykaz błędów,
            roboty dodatkowe lub zamienne z kosztorysem, wydłużenie terminu i zmianę ceny.</p>
          ${stan}
          <div class="pasek" style="margin:0">
            ${B.length ? (ost ? `<button class="maly glowny" onclick="WNIOSEK_OTWARTY='${ost.id}'; rysujProjekt(); setTimeout(() => $('#wn-edytor')?.scrollIntoView({behavior:'smooth'}), 100)">Otwórz wniosek ${esc(ost.nr)}</button>
                <button class="maly zielony" data-ik="plus" onclick="nowyWniosek('roznice_dokumentacji')">Kolejny wniosek</button>`
              : `<button class="zielony pulsuj" data-ik="plus" onclick="nowyWniosek('roznice_dokumentacji')">Złóż wniosek: błędy dokumentacji</button>`)
              : `<button class="maly zielony" data-ik="plus" onclick="nowyWniosek('roznice_dokumentacji')">Nowy wniosek: błędy dokumentacji</button>`}
            ${sprawdzono ? "" : `<button class="maly zolty" data-ik="iskra" onclick="document.getElementById('sek-weryfikacja') ? document.getElementById('sek-weryfikacja').scrollIntoView({behavior:'smooth'}) : wykryjBledy()">Wykryj błędy (krok 2)</button>`}
            ${B.length ? `<button class="maly" data-ik="dokument" onclick="BLEDY_OTW = true; rysujProjekt(); setTimeout(() => $('#wn-bledy')?.scrollIntoView({behavior:'smooth', block:'start'}), 100)">Pokaż błędy (${B.length})</button>
              <button class="maly" data-ik="pobierz" onclick="pobierzBledy()">Wykaz błędów (Word)</button>` : ""}</div></div></div>`;
      })()}
      <div class="wn-rodzaj"><div class="wn-lit">c)</div><div><b>Inne przeszkody</b>
        <p>Przyczyny niezależne od wykonawcy, które uniemożliwiają prowadzenie robót: wstrzymanie przez konserwatora zabytków lub inny organ,
          okres lęgowy, znaleziska archeologiczne, kolizje z infrastrukturą, brak frontu robót. Wniosek o wydłużenie terminu (opcjonalnie z kosztami przestoju).</p>
        <button class="maly zielony" data-ik="plus" onclick="nowyWniosek('przeszkody')">Nowy wniosek: inne przeszkody</button></div></div>
    </div>
    ${W_.length ? `<h4 class="grupa-analizy">Twoje wnioski</h4><div class="tabela-okno"><table class="tabela"><tr><th>Nr</th><th>Rodzaj</th><th>Data</th><th>Dni</th><th>Kwota netto</th><th>Status</th><th>Dokumenty</th><th></th></tr>
      ${W_.map(x => `<tr class="${x.id === WNIOSEK_OTWARTY ? "wybrany" : ""}"><td><b>${esc(x.nr)}</b></td><td>${esc(RODZ_WN[x.rodzaj])}</td><td>${esc(dataPl(x.data))}</td>
        <td class="liczba">${x.dni_zaakceptowane ?? x.dni ?? 0}</td><td class="liczba">${zl(x.kwota_zaakceptowana ?? x.kwota_netto ?? 0)}</td>
        <td><span class="znacznik ${stKl[x.status] || ""}">${esc(x.status)}</span>${x.aneks_nr ? `<br><small>aneks nr ${esc(x.aneks_nr)}</small>` : ""}</td>
        <td><div class="pliki-ik">${[plikIk(p.id, x.wniosek_plik, "Wniosek", 1), plikIk(p.id, x.kosztorys_plik, "Kosztorys", 1), plikIk(p.id, x.aneks_plik, "Aneks", 1), plikIk(p.id, x.kosztorys_po_aneksie, "Kosztorys po aneksie", 1)].filter(Boolean).join("") || "–"}</div></td>
        <td><button class="maly" onclick="WNIOSEK_OTWARTY='${x.id}'; rysujProjekt(); setTimeout(() => $('#wn-edytor')?.scrollIntoView({behavior:'smooth'}), 100)">Otwórz</button></td></tr>`).join("")}</table></div>` : ""}
    ${w ? edytorWniosku(p, w, B) : ""}
  </div></div>`;
}
function edytorWniosku(p, w, B) {
  const zam = w.status === "zaakceptowany", r = w.rodzaj, pr = w.propozycja || {};
  const prace = (w.prace || []).map(x => `${x.opis}; ${x.jm}; ${String(x.ilosc).replace(".", ",")}${x.zamienna ? "; zamienna" : x.mimo_to ? "; mimo to: " + (x.mimo_to_powod || "") : ""}`).join("\n");
  const wOf = (w.prace || []).filter(x => (x.w_ofercie || []).length);
  const kk = w.kwota_kosztorysu, rozna = kk != null && Math.abs((+w.kwota_netto || 0) - kk) > 0.5;
  return `<div class="korekta" id="wn-edytor" style="display:block;margin-top:14px"><h3>Wniosek ${esc(w.nr)} – ${esc(RODZ_WN[r])}</h3>
    ${r === "przeszkody" ? `<div class="siatka"><label style="grid-column: 1 / -1">Przyczyna<select id="wn-przyczyna">${PRZESZKODY.map(x => `<option ${x === w.przyczyna ? "selected" : ""}>${esc(x)}</option>`).join("")}</select></label>
      <label>Od<input type="date" id="wn-od" value="${esc(w.od || "")}"></label><label>Do<input type="date" id="wn-do" value="${esc(w.do || "")}"></label>
      <label style="grid-column: span 2">Organ / pismo (np. decyzja WKZ nr …)<input id="wn-organ" value="${esc(w.organ || "")}"></label>
      <label style="grid-column: 1 / -1">Dokumenty potwierdzające (załączniki)<input id="wn-dok" value="${esc(w.dokumenty || "")}" placeholder="np. pismo konserwatora z 12.05.2026, wpisy w dzienniku budowy nr 14–16"></label></div>` : ""}
    ${r === "roznice_dokumentacji" ? `<div class="opis" style="margin:6px 0 2px"><b>Błędy / różnice w dokumentacji</b> (zaznacz te, których dotyczy wniosek):</div>
      ${B.length ? `<div class="wybor-pion">${B.map(b => `<label><input type="checkbox" class="wn-bl" value="${esc(b.id)}" ${(w.bledy || []).includes(b.id) ? "checked" : ""}>
        <span><b>${esc(b.dokument)}${b.miejsce ? " · " + esc(b.miejsce) : ""}</b> – ${esc(b.opis)}</span></label>`).join("")}</div>`
        : '<p class="opis">Program nie wykrył jeszcze błędów – kliknij „Wykryj błędy (AI)” powyżej albo opisz różnice w uzasadnieniu.</p>'}` : ""}
    ${zam ? "" : `<div class="wn-ai"><div><b>${ik("iskra")} Propozycja AI</b><br><span class="opis" style="margin:0">Program zaproponuje uzasadnienie, zakres
      ${r === "przeszkody" ? "ewentualnych robót" : "prac dodatkowych / zamiennych"}, przygotuje kosztorys (kwota dla zamawiającego) i zaproponuje liczbę dni przedłużenia.
      ${r === "prace_dodatkowe" ? " Możesz najpierw wpisać w uzasadnieniu kilka słów, czego dotyczą prace." : ""} Wszystko możesz potem zmienić.</span>
      ${pr.data ? `<br><small class="zielone">Ostatnia propozycja: ${esc(pr.data)}</small>` : ""}</div>
      <button class="zolty" data-ik="iskra" onclick="propozycjaWniosku()">${pr.data ? "Zaproponuj ponownie" : "Zaproponuj uzasadnienie, zakres, kosztorys i termin"}</button></div>`}
    <label class="opis wn-et">1. Uzasadnienie ${pr.data ? '<span class="wn-ai-znacznik">propozycja AI – możesz zmienić</span>' : ""}</label>
    <textarea id="wn-uzas" style="min-height:120px" placeholder="${r === "przeszkody" ? "np. roboty wstrzymano do czasu zakończenia okresu lęgowego (gniazda jerzyków na elewacji)" : "np. po skuciu tynków stwierdzono skorodowane nadproża, nieujęte w przedmiarze"}">${esc(w.uzasadnienie || "")}</textarea>
    <label class="opis wn-et">2. Zakres prac ${r === "prace_dodatkowe" ? "dodatkowych" : "dodatkowych / zamiennych"} – każda w osobnej linii: <b>opis; j.m.; ilość</b>
      ${pr.data && (w.prace || []).length ? '<span class="wn-ai-znacznik">propozycja AI – możesz zmienić</span>' : ""}</label>
    <textarea id="wn-prace" style="min-height:110px" placeholder="Wymiana nadproży stalowych nad oknami; szt.; 14&#10;Naprawa tynku podłoża pod ocieplenie; m2; 85">${esc(prace)}</textarea>
    ${(w.ostrzezenia || []).length ? `<div class="ramka-uwaga">${w.ostrzezenia.map(x => esc(x)).join("<br>")}</div>` : ""}
    ${wOf.length ? `<div class="opis" style="margin:6px 0 2px"><b>Roboty ujęte już w cenie oferty</b> – program nie wyceni ich we wniosku. Jeśli to robota zamienna, dopisz na końcu wiersza „; zamienna” (program odejmie zastępowaną pozycję).
        Jeśli dopasowanie jest błędne, dopisz „; mimo to: powód”.</div>
      <ul class="lista">${wOf.map(x => `<li>${esc(x.opis.slice(0, 90))} → ${x.w_ofercie.map(m => `poz. <b>${esc(m.lp || "?")}</b> ${esc(m.opis.slice(0, 60))} (${zl(m.wartosc)})${m.wariant ? " – dokumenty miały tu dwa warianty; inny wariant niż w cenie to robota zamienna" : ""}`).join("; ")}
        ${x.zamienna ? ' – <b class="zielone">zamienna: liczona różnica</b>' : x.mimo_to && x.mimo_to_powod ? ' – <b>wyceniana mimo to</b>' : ' – <b class="czerwone">pomijana</b>'}</li>`).join("")}</ul>` : ""}
    ${zam ? "" : `<div class="pasek" style="margin:6px 0 0"><button class="maly zolty" data-ik="iskra" onclick="kosztorysWniosku()">${w.kosztorys_plik ? "Przelicz kosztorys dla tego zakresu (AI)" : "Przygotuj kosztorys (AI)"}</button>
      <label class="przycisk maly" data-ik="wgraj">Wgraj własny kosztorys (Excel)<input type="file" accept=".xlsx,.xlsm" hidden onchange="kosztorysWnioskuWlasny(this.files[0])"></label>
      </div>`}
    <div id="wn-kosztorys" class="wn-kosztorys">${w.kosztorys_plik ? '<p class="opis">Ładuję kosztorys…</p>' : ""}</div>
    <div class="siatka" style="margin-top:10px">
      <label>3. Kwota proponowana dla zamawiającego – netto [zł]<input id="wn-kwota" value="${w.kwota_netto || 0}">
        <small class="opis">${kk != null ? `z kosztorysu: <b>${zl(kk)}</b>${rozna ? ' – <b class="czerwone">zmieniona ręcznie</b>' : ""}` : (r === "przeszkody" ? "opcjonalnie, np. koszty przestoju" : "wpisze się po przygotowaniu kosztorysu")}</small></label>
      <label>4. Przedłużenie terminu o [dni]<input id="wn-dni" value="${w.dni || 0}">
        <small class="opis">${pr.dni != null ? `propozycja: <b>${pr.dni} dni</b>${pr.dni_realizacji ? ` (roboty ok. ${pr.dni_realizacji} dni roboczych)` : ""}${pr.uzasadnienie_dni ? " – " + esc(pr.uzasadnienie_dni) : ""}` : "wpisz albo użyj propozycji AI"}
          ${p.umowa_dane && p.umowa_dane.termin && +w.dni ? `<br>nowy termin: <b>${esc(dataPl(new Date(new Date(p.umowa_dane.termin).getTime() + (+w.dni) * 86400000).toISOString().slice(0, 10)))}</b>` : ""}</small></label>
      <label>Miejscowość pisma<input id="wn-miejsce" value="${esc(w.miejsce || "")}" placeholder="np. Świdnica"></label></div>
    ${zam ? "" : `<div class="pasek" style="margin-top:10px"><button data-ik="zapisz" onclick="zapiszWniosek()">Zapisz zmiany</button>
      <button class="zielony" data-ik="dokument" onclick="dokumentWniosku()">Akceptuję – generuj wniosek do zamawiającego</button>
      <button class="maly niebezp" data-ik="kosz" onclick="usunWniosek()">Usuń</button></div>`}
    ${w.kosztorys_plik || w.wniosek_plik || w.aneks_plik ? `<div class="opis wn-et">Dokumenty wniosku</div><div class="pliki-ik">${[plikIk(p.id, w.kosztorys_plik, "Kosztorys"), plikIk(p.id, w.wniosek_plik, "Wniosek do zamawiającego"),
      plikIk(p.id, w.aneks_plik, `Aneks nr ${esc(w.aneks_nr || "")}`), plikIk(p.id, w.kosztorys_po_aneksie, "Kosztorys po aneksie")].filter(Boolean).join("")}</div>` : ""}
    ${zam ? `<p class="zielone"><b>Zaakceptowany ${esc(dataPl(w.data_akceptacji || ""))}</b>: przedłużenie o ${w.dni_zaakceptowane} dni, kwota ${zl(w.kwota_zaakceptowana || 0)} netto – termin, wynagrodzenie i harmonogram budowy zaktualizowane; aneks nr ${esc(w.aneks_nr)} przygotowany.</p>`
      : w.wniosek_plik ? `<div class="pasek" style="margin-top:8px"><span class="opis" style="margin:0">Po wysłaniu wniosku – status: <b>${esc(w.status)}</b></span>
        <button class="maly" onclick="statusWniosku('złożony')">Oznacz jako złożony</button>
        <button class="maly zielony" onclick="akceptujWniosek()">Zamawiający zaakceptował → aneks</button>
        <button class="maly" onclick="statusWniosku('odrzucony')">Odrzucony</button></div>` : ""}
  </div>`;
}
// ---------- okienko kosztorysu wniosku: pozycje z kwotami, edycja ilości i cen
let KW = null;
async function ladujKosztorysWniosku() {
  const el = $("#wn-kosztorys"); if (!el) return;
  const w = (PROJEKT.wnioski || []).find(x => x.id === WNIOSEK_OTWARTY); if (!w || !w.kosztorys_plik) { el.innerHTML = ""; return; }
  const d = await api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/kosztorys-dane`).catch(() => null);
  if (!d || d.brak) { el.innerHTML = ""; return; }
  KW = d; rysujKosztorysWniosku(w.status === "zaakceptowany");
}
function rysujKosztorysWniosku(tylkoOdczyt) {
  const d = KW, el = $("#wn-kosztorys"), w = (PROJEKT.wnioski || []).find(x => x.id === WNIOSEK_OTWARTY) || {};
  const ro = tylkoOdczyt ? "disabled" : "";
  let lp = 0;
  el.innerHTML = `<div class="wn-k-gora"><b>${ik("kalkulator")} Kosztorys prac – wniosek ${esc(w.nr || "")}</b>
      ${w.kosztorys_plik ? plikIk(PROJEKT_ID, w.kosztorys_plik, "Pobierz", 1) : ""}</div>
    <div class="tabela-okno"><table class="tabela wn-k-tab"><tr><th>Lp.</th><th>Opis robót</th><th>j.m.</th><th>Ilość</th><th>Cena jedn. netto [zł]</th><th>Wartość netto [zł]</th><th>Źródło ceny</th>${ro ? "" : "<th></th>"}</tr>
      ${d.dzialy.map((dz, di) => `<tr class="wn-k-dzial"><td colspan="${ro ? 7 : 8}">${esc(dz.nazwa)}</td></tr>
        ${dz.pozycje.map((p, pi) => `<tr><td>${++lp}</td><td>${esc(p.opis)}${p.uwagi ? `<br><small class="opis">${esc(p.uwagi)}</small>` : ""}</td><td>${esc(p.jm)}</td>
          <td><input class="wn-k-in" ${ro} value="${String(p.ilosc).replace(".", ",")}" oninput="zmienKW(${di},${pi},'ilosc',this.value)"></td>
          <td><input class="wn-k-in" ${ro} value="${String(p.cena).replace(".", ",")}" oninput="zmienKW(${di},${pi},'cena',this.value)"></td>
          <td class="liczba" id="kw-w-${di}-${pi}"><b>${zl(p.wartosc)}</b></td><td><small class="opis">${esc(p.zrodlo || "")}</small></td>
          ${ro ? "" : `<td><button class="maly" title="Usuń pozycję" onclick="KW.dzialy[${di}].pozycje.splice(${pi},1); przeliczKW(); rysujKosztorysWniosku()">×</button></td>`}</tr>`).join("")}
        <tr class="wn-k-suma"><td colspan="5">Razem – ${esc(dz.nazwa.replace(/^[0-9.]+\s*/, ""))}</td><td class="liczba" id="kw-d-${di}"><b>${zl(dz.suma)}</b></td><td colspan="${ro ? 1 : 2}"></td></tr>`).join("")}
      <tr class="wn-k-razem"><td colspan="5">RAZEM NETTO</td><td class="liczba" id="kw-netto"><b>${zl(d.netto)}</b></td><td colspan="${ro ? 1 : 2}"></td></tr>
      <tr class="wn-k-razem"><td colspan="5">VAT ${Math.round((d.vat || 0) * 100)}%${d.vat_nieustalony ? " (do ustalenia)" : ""}</td><td class="liczba" id="kw-vat">${zl(d.vat_kwota)}</td><td colspan="${ro ? 1 : 2}"></td></tr>
      <tr class="wn-k-razem"><td colspan="5">RAZEM BRUTTO</td><td class="liczba" id="kw-brutto"><b>${zl(d.brutto)}</b></td><td colspan="${ro ? 1 : 2}"></td></tr></table></div>
    ${ro ? "" : `<div class="pasek" style="margin-top:8px"><button class="zielony maly" data-ik="zapisz" onclick="zapiszKW()">Zapisz zmiany w kosztorysie</button>
      <span class="opis" style="margin:0" id="kw-info">Zmień ilości lub ceny – kwoty przeliczą się od razu; po zapisaniu kwota wniosku przyjmie wartość kosztorysu.</span></div>`}`;
}
const liczbaPL = v => parseFloat(String(v).replace(/\s/g, "").replace(",", ".")) || 0;
function przeliczKW() {
  let netto = 0;
  KW.dzialy.forEach(dz => { dz.suma = 0; dz.pozycje.forEach(p => { p.wartosc = Math.round(liczbaPL(p.ilosc) * liczbaPL(p.cena) * 100) / 100; dz.suma += p.wartosc; }); netto += dz.suma; });
  KW.netto = Math.round(netto * 100) / 100; KW.vat_kwota = Math.round(KW.netto * (KW.vat || 0) * 100) / 100; KW.brutto = KW.netto + KW.vat_kwota;
}
function zmienKW(di, pi, pole, v) {
  KW.dzialy[di].pozycje[pi][pole] = v; przeliczKW();
  const p = KW.dzialy[di].pozycje[pi];
  $(`#kw-w-${di}-${pi}`).innerHTML = `<b>${zl(p.wartosc)}</b>`; $(`#kw-d-${di}`).innerHTML = `<b>${zl(KW.dzialy[di].suma)}</b>`;
  $("#kw-netto").innerHTML = `<b>${zl(KW.netto)}</b>`; $("#kw-vat").textContent = zl(KW.vat_kwota); $("#kw-brutto").innerHTML = `<b>${zl(KW.brutto)}</b>`;
  $("#kw-info").innerHTML = '<b class="czerwone">Niezapisane zmiany</b> – kliknij „Zapisz zmiany w kosztorysie”.';
}
async function zapiszKW() {
  const dz = KW.dzialy.map(d => ({nazwa: d.nazwa, pozycje: d.pozycje.map(p => ({...p, ilosc: liczbaPL(p.ilosc), cena: liczbaPL(p.cena)}))}));
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/kosztorys-dane`, {json: {dzialy: dz}}));
  if (w) { komunikat(`Zapisano kosztorys: ${zl(w.netto)} netto – kwota wniosku zaktualizowana.`); otworzProjekt(PROJEKT_ID); }
}
async function propozycjaWniosku() {
  if (!(await zapiszWniosek(true))) return;
  komunikat("AI przygotowuje propozycję wniosku – to potrwa 1–3 minuty.");
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/propozycja`, {json: {}})),
    () => { odswiezProjekt(); setTimeout(() => $("#wn-edytor")?.scrollIntoView({behavior: "smooth"}), 600); });
}
function daneWniosku() {
  const d = {uzasadnienie: $("#wn-uzas").value, dni: $("#wn-dni").value, kwota_netto: $("#wn-kwota").value, miejsce: $("#wn-miejsce").value};
  if ($("#wn-prace")) d.prace = $("#wn-prace").value.split("\n").map(l => l.split(";").map(x => x.trim())).filter(a => a[0]).map(a => ({opis: a[0], jm: a[1] || "", ilosc: a[2] || 0, znacznik: a.slice(3).join("; ")}));
  if ($("#wn-przyczyna")) Object.assign(d, {przyczyna: $("#wn-przyczyna").value, od: $("#wn-od").value, do: $("#wn-do").value, organ: $("#wn-organ").value, dokumenty: $("#wn-dok").value});
  if (document.querySelector(".wn-bl")) d.bledy = [...document.querySelectorAll(".wn-bl:checked")].map(c => c.value);
  return d;
}
async function nowyWniosek(rodzaj) {
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski`, {json: {rodzaj}})); if (!w) return;
  WNIOSEK_OTWARTY = w.id; await otworzProjekt(PROJEKT_ID); setTimeout(() => $("#wn-edytor")?.scrollIntoView({behavior: "smooth"}), 150);
}
async function zapiszWniosek(cicho) {
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}`, {json: daneWniosku()}));
  if (w && !cicho) { komunikat("Zapisano wniosek."); otworzProjekt(PROJEKT_ID); }
  return w;
}
async function kosztorysWniosku() {
  if (!(await zapiszWniosek(true))) return;
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/kosztorys`, {json: {}})), odswiezProjekt);
}
async function kosztorysWnioskuWlasny(f) {
  if (!f) return; await zapiszWniosek(true); const fd = new FormData(); fd.append("plik", f);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/kosztorys-wlasny`, {method: "POST", body: fd}));
  if (w) { komunikat(`Wczytano kosztorys: ${zl(w.netto)} netto.`); otworzProjekt(PROJEKT_ID); }
}
async function dokumentWniosku() {
  if (!(await zapiszWniosek(true))) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/dokument`, {json: {}}));
  if (w) { location.href = w.url; otworzProjekt(PROJEKT_ID); }
}
async function statusWniosku(status) {
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/status`, {json: {status}}))) { komunikat("Zmieniono status."); otworzProjekt(PROJEKT_ID); }
}
async function akceptujWniosek() {
  await zapiszWniosek(true);
  const dni = prompt("Ile dni przedłużenia zaakceptował zamawiający?", $("#wn-dni").value); if (dni === null) return;
  const kw = prompt("Jaką kwotę netto zaakceptował zamawiający? (0 – bez zmiany wynagrodzenia)", $("#wn-kwota").value); if (kw === null) return;
  const nr = prompt("Numer aneksu:", String((PROJEKT.wnioski || []).filter(x => x.aneks_nr).length + 1)); if (nr === null) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}/status`, {json: {status: "zaakceptowany", dni, kwota_netto: kw, nr_aneksu: nr}}));
  if (w) { komunikat(`Aneks nr ${w.aneks_nr} przygotowany; termin i wynagrodzenie zaktualizowane.`); otworzProjekt(PROJEKT_ID); }
}
async function usunWniosek() {
  if (confirm("Usunąć wniosek?") && await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wnioski/${WNIOSEK_OTWARTY}`, {json: {usun: true}}))) { WNIOSEK_OTWARTY = null; otworzProjekt(PROJEKT_ID); }
}
async function wykryjBledy() {
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/weryfikacja`, {json: {dodatkowe: "różnice, które mogą wymagać robót dodatkowych lub zamiennych oraz wpływać na termin i wynagrodzenie"}})), odswiezProjekt);
}
async function pobierzBledy() { const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/bledy-dokumentacji`, {json: {}})); if (w) location.href = w.url; }

// ---------- podwykonawcy: zgłoszenia, umowy, rozliczenia, oświadczenia (wykonawca) / żądanie oświadczeń (zamawiający)
let PWD = null, PW_OTW = null;
async function ladujPw() { PWD = await api(`/api/projekty/${REAL_ID}/podwykonawcy`).catch(() => null); if (PWD) rysujPw(); }
const pwPlik = (x, rodz, f) => plikIk(REAL_ID, `realizacja/podwykonawcy/${x}/${rodz}/${f}`, f.length > 22 ? f.slice(0, 20) + "…" : f, 1);
function rysujPw() {
  const el = $("#pw-tresc"), L = PWD.podwykonawcy, ZR = PWD.strona === "zamawiajacy", dzis = DZIS_ISO();
  const BF = poziomU("finanse") < 1 || L.some(x => x.bez_finansow);  // rola bez Finansów: bez wartości umów, faktur i zapłat podwykonawców
  const stKl = s => ({"zaakceptowany": "z-startujemy", "zgłoszony": "z-do-analizy", "zastrzeżenia / sprzeciw": "z-czerwony"})[s] || "z-odpuszczamy";
  el.innerHTML = `<p class="opis">${ZR ? "Rejestr podwykonawców zgłoszonych przez wykonawcę: zakres prac, umowy, status akceptacji. Przy usługach i dostawach obowiązki wykonawcy wobec podwykonawców wynikają przede wszystkim z postanowień umowy. Przed zapłatą faktury lub etapu możesz wezwać wykonawcę do przedstawienia oświadczeń o rozliczeniu z podwykonawcami danego zakresu."
      : "Podwykonawcy: zakres prac, umowy, faktury i zapłaty. Program przygotuje zgłoszenie podwykonawcy zamawiającemu, oświadczenie podwykonawcy o rozliczeniu z Tobą oraz – na ich podstawie – Twoje oświadczenie o niezaleganiu wobec podwykonawców do rozliczenia z zamawiającym."}</p>
    <div class="pasek"><button class="maly" data-ik="plus" onclick="dodajPw()">Dodaj podwykonawcę</button></div>
    ${L.length ? `<div class="pw-lista">${L.map((x, i) => `<div class="pw-karta ${PW_OTW === x.id ? "otw" : ""}" data-i="${i}">
      <div class="pw-gora" onclick="PW_OTW = PW_OTW === '${x.id}' ? null : '${x.id}'; zbierzPw(); rysujPw()">
        <b>${esc(x.nazwa || "(nowy podwykonawca)")}</b> <span class="znacznik ${stKl(x.status)}">${esc(x.status || "niezgłoszony")}</span>
        <span class="opis" style="margin:0">${esc((x.zakres || "").slice(0, 90))}</span>
        ${BF ? "" : `<span class="pw-kwoty">umowa ${zl(x.sumy.wartosc_brutto)} · zapłacono ${zl(x.sumy.zaplacono)}${x.sumy.zalegle > 0.01 ? ` · <b class="czerwone">zaległe ${zl(x.sumy.zalegle)}</b>` : ""}</span>`}
        ${(x.uwagi || []).map(u => `<span class="czerwone" style="display:block;font-size:.88em;margin-top:3px">${esc(u)}</span>`).join("")}</div>
      ${PW_OTW === x.id ? `<div class="pw-szczeg">
        <div class="siatka">
          <label>Nazwa podwykonawcy<input class="pw-nazwa" value="${esc(x.nazwa)}"></label>
          <label>NIP<span style="display:flex;gap:6px"><input class="pw-nip" value="${esc(x.nip || "")}"><button class="maly zolty" onclick="pwNip(${i})">Pobierz</button></span></label>
          <label>Adres<input class="pw-adres" value="${esc(x.adres || "")}"></label><label>Osoba kontaktowa / telefon<input class="pw-kontakt" value="${esc(x.kontakt || "")}"></label>
          <label style="grid-column:1 / -1">Zakres powierzonych prac (robót, usług, dostaw)<textarea class="pw-zakres" style="min-height:60px">${esc(x.zakres || "")}</textarea></label>
          ${BF ? "" : `<label>Wartość umowy netto [zł]<input class="pw-wart" inputmode="decimal" value="${esc(String(x.wartosc_netto || ""))}"></label><label>VAT [%]<input class="pw-vat" value="${esc(x.vat || "23")}"></label>`}
          <label>Data umowy<input type="date" class="pw-data" value="${esc(x.data_umowy || "")}"></label><label>Termin realizacji<input class="pw-termin" value="${esc(x.termin_realizacji || "")}"></label>
          <label>Termin zapłaty [dni]<input class="pw-tp" value="${esc(x.termin_platnosci || "30")}"></label>
          <label>Status zgłoszenia<select class="pw-status">${PWD.statusy.map(s => `<option ${s === x.status ? "selected" : ""}>${s}</option>`).join("")}</select></label>
          <label>Data zgłoszenia<input type="date" class="pw-dzgl" value="${esc(x.data_zgloszenia || "")}"></label>
          <label style="grid-column:1 / -1">Uwagi (własne)<input class="pw-uwagi" value="${esc(x.notatka || "")}"></label></div>
        ${BF ? "" : `<h4 class="grupa-analizy">Faktury i zapłaty</h4>
        <div class="tabela-okno"><table class="tabela pw-plat"><tr><th>Faktura</th><th>Data</th><th>Termin zapłaty</th><th>Kwota brutto</th><th>Zapłacono</th><th>Data zapłaty</th><th>Etap / zakres</th><th></th></tr>
          ${(x.platnosci || []).map((p, k) => `<tr data-k="${k}"><td><input class="pf-nr" value="${esc(p.faktura || "")}"></td><td><input type="date" class="pf-data" value="${esc(p.data || "")}"></td>
            <td><input type="date" class="pf-term" value="${esc(p.termin || "")}"></td><td><input class="pf-kw wn-k-in" value="${String(p.kwota_brutto ?? "").replace(".", ",")}"></td>
            <td><input type="checkbox" class="pf-zap" ${p.zaplacono ? "checked" : ""}></td><td><input type="date" class="pf-dz" value="${esc(p.data_zaplaty || "")}"></td>
            <td><input class="pf-etap" value="${esc(p.etap || "")}"></td><td><button class="maly niebezp" data-ik="kosz" onclick="zbierzPw(); PWD.podwykonawcy[${i}].platnosci.splice(${k},1); rysujPw()"></button></td></tr>`).join("")}</table></div>
        <div class="pasek"><button class="maly" data-ik="plus" onclick="zbierzPw(); PWD.podwykonawcy[${i}].platnosci = PWD.podwykonawcy[${i}].platnosci || []; PWD.podwykonawcy[${i}].platnosci.push({}); rysujPw()">Dodaj fakturę</button></div>`}
        <h4 class="grupa-analizy">Pliki</h4>
        <div class="pw-pliki"><div><b>Umowa / projekt umowy</b><div class="pliki-ik">${(x.pliki_umowy || []).map(f => pwPlik(x.id, "umowa", f)).join("") || '<span class="opis">brak</span>'}</div>
            <label class="przycisk maly" data-ik="wgraj">Wgraj<input type="file" multiple hidden onchange="pwWgraj('${x.id}','umowa',this.files)"></label></div>
          <div><b>Oświadczenia o rozliczeniu (podpisane)</b><div class="pliki-ik">${(x.pliki_oswiadczenia || []).map(f => pwPlik(x.id, "oswiadczenia", f)).join("") || '<span class="opis">brak</span>'}</div>
            <label class="przycisk maly" data-ik="wgraj">Wgraj<input type="file" multiple hidden onchange="pwWgraj('${x.id}','oswiadczenia',this.files)"></label></div>
          <div><b>Inne (protokoły, dowody zapłaty)</b><div class="pliki-ik">${(x.pliki_dokumenty || []).map(f => pwPlik(x.id, "dokumenty", f)).join("") || '<span class="opis">brak</span>'}</div>
            <label class="przycisk maly" data-ik="wgraj">Wgraj<input type="file" multiple hidden onchange="pwWgraj('${x.id}','dokumenty',this.files)"></label></div></div>
        <div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="zapisz" onclick="zapiszPw()">Zapisz</button>
          ${ZR ? "" : `<button data-ik="dokument" onclick="pwDok('zgloszenie','${x.id}')">Zgłoszenie podwykonawcy zamawiającemu (Word)</button>
          ${BF ? "" : `<button data-ik="dokument" onclick="pwDok('oswiadczenie_pw','${x.id}')">Oświadczenie podwykonawcy o rozliczeniu (Word)</button>`}`}
          <button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć podwykonawcę z listy?')) { zbierzPw(); PWD.podwykonawcy.splice(${i},1); zapiszPw(); }">Usuń</button></div>
      </div>` : ""}</div>`).join("")}</div>` : '<p class="pusto">Brak podwykonawców.</p>'}
    ${L.length && !ZR && !BF ? `<div class="ramka-uwaga" style="margin-top:12px"><b>Oświadczenie o niezaleganiu wobec podwykonawców</b> – do rozliczenia faktury lub etapu z zamawiającym, na podstawie zapłat i oświadczeń podwykonawców.
      <div class="pasek" style="margin-top:6px"><label>Stan na dzień <input type="date" id="pw-dodnia" value="${dzis}"></label>
        <label>Zakres / etap / faktura <input id="pw-zakres" placeholder="np. faktura częściowa nr 3 – etap II"></label>
        <button class="glowny" data-ik="dokument" onclick="pwDok('oswiadczenie_wyk')">Oświadczenie wykonawcy (Word)</button></div>
      ${L.some(x => x.sumy.zalegle > 0.01) ? '<p class="czerwone" style="margin:6px 0 0">Uwaga: są niezapłacone faktury po terminie – oświadczenie wykaże zaległości.</p>' : ""}</div>` : ""}
    ${ZR ? `<div class="ramka-uwaga" style="margin-top:12px"><b>Żądanie oświadczeń o rozliczeniu z podwykonawcami</b> – przed zapłatą faktury lub etapu.
      <div class="pasek" style="margin-top:6px"><label>Zakres / etap / faktura <input id="pw-zakres" placeholder="np. faktura nr 3/2026 – etap II"></label>
        <label>Termin <input type="date" id="pw-termin" value="${new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10)}"></label>
        <button class="glowny" data-ik="dokument" onclick="pwDok('zadanie')">Wezwij wykonawcę (Word)</button></div>
      ${(PWD.zadania || []).length ? `<div class="tabela-okno" style="margin-top:8px"><table class="tabela"><tr><th>Data</th><th>Zakres</th><th>Termin</th><th>Status</th><th>Wezwanie</th><th>Otrzymane dokumenty</th></tr>
        ${PWD.zadania.map(z => `<tr><td>${esc(dataPl(z.data))}</td><td>${esc(z.zakres)}</td><td class="${z.status === "wysłane" && z.termin < dzis ? "czerwone" : ""}">${esc(dataPl(z.termin))}</td>
          <td><select onchange="pwZadStatus('${z.id}', this.value)">${["wysłane", "otrzymane – kompletne", "otrzymane – braki"].map(s => `<option ${s === z.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
          <td>${plikIk(REAL_ID, z.plik, "Wezwanie", 1)}</td>
          <td><div class="pliki-ik">${(z.otrzymane || []).map(f => plikIk(REAL_ID, `realizacja/podwykonawcy/_zadania/${z.id}/${f}`, f.length > 20 ? f.slice(0, 18) + "…" : f, 1)).join("")}</div>
            <label class="przycisk maly" data-ik="wgraj">Wgraj<input type="file" multiple hidden onchange="pwWgraj('${z.id}','zadanie',this.files)"></label></td></tr>`).join("")}</table></div>` : ""}</div>` : ""}
    ${(PWD.dokumenty || []).length ? `<h4 class="grupa-analizy">Przygotowane dokumenty</h4><div class="pliki-ik">${PWD.dokumenty.slice(0, 12).map(d => plikIk(REAL_ID, d.plik,
      ({zgloszenie: "Zgłoszenie", oswiadczenie_pw: "Oświadczenie podwyk.", oswiadczenie_wyk: "Oświadczenie wykonawcy", zadanie: "Wezwanie"})[d.rodzaj] + (d.podwykonawca ? " – " + d.podwykonawca.slice(0, 18) : ""))).join("")}</div>` : ""}`;
  wstawIkony(el);
}
function zbierzPw() {
  document.querySelectorAll(".pw-karta.otw").forEach(k => { const x = PWD.podwykonawcy[+k.dataset.i]; const g = c => k.querySelector(c)?.value ?? "";
    Object.assign(x, {nazwa: g(".pw-nazwa"), nip: g(".pw-nip"), adres: g(".pw-adres"), kontakt: g(".pw-kontakt"), zakres: g(".pw-zakres"),
      data_umowy: g(".pw-data"), termin_realizacji: g(".pw-termin"), termin_platnosci: g(".pw-tp"), status: g(".pw-status"), data_zgloszenia: g(".pw-dzgl"), notatka: g(".pw-uwagi")});
    if (k.querySelector(".pw-wart")) Object.assign(x, {wartosc_netto: g(".pw-wart"), vat: g(".pw-vat")});  // własne uwagi osobno od ostrzeżeń programu (x.uwagi)
    if (k.querySelector(".pw-plat")) x.platnosci = [...k.querySelectorAll(".pw-plat tr[data-k]")].map(t => ({faktura: t.querySelector(".pf-nr").value, data: t.querySelector(".pf-data").value, termin: t.querySelector(".pf-term").value,
      kwota_brutto: t.querySelector(".pf-kw").value, zaplacono: t.querySelector(".pf-zap").checked, data_zaplaty: t.querySelector(".pf-dz").value, etap: t.querySelector(".pf-etap").value}));
  });
}
function dodajPw() { zbierzPw(); const id = Math.random().toString(16).slice(2, 10); PWD.podwykonawcy.push({id, nazwa: "", status: "niezgłoszony", platnosci: [], sumy: {wartosc_brutto: 0, zaplacono: 0, zalegle: 0}}); PW_OTW = id; rysujPw(); }
async function zapiszPw(cicho) {
  zbierzPw();
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/podwykonawcy`, {json: {podwykonawcy: PWD.podwykonawcy}}));
  if (w && !cicho) komunikat(`Zapisano podwykonawców: ${w.zapisano}.`);
  if (w) await ladujPw();
  return w;
}
async function pwNip(i) {
  zbierzPw(); const d = await pobierzNip(PWD.podwykonawcy[i].nip); if (!d) return;
  Object.assign(PWD.podwykonawcy[i], {nazwa: PWD.podwykonawcy[i].nazwa || d.nazwa, nip: d.nip, adres: d.adres}); rysujPw();
}
async function pwWgraj(id, rodzaj, pliki) {
  if (rodzaj !== "zadanie" && !(await zapiszPw(true))) return;
  const fd = new FormData(); fd.append("id", id); fd.append("rodzaj", rodzaj); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/podwykonawcy/plik`, {method: "POST", body: fd}))) { komunikat("Wgrano."); ladujPw(); }
}
async function pwDok(rodzaj, id) {
  if (rodzaj !== "zadanie" && !(await zapiszPw(true))) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/podwykonawcy/dokument`, {json: {rodzaj, id, do_dnia: $("#pw-dodnia")?.value, zakres: $("#pw-zakres")?.value, termin: $("#pw-termin")?.value}}));
  if (w) { komunikat("Dokument gotowy."); location.href = w.url; ladujPw(); }
}
async function pwZadStatus(id, status) { if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/podwykonawcy/zadanie-status`, {json: {id, status}}))) komunikat("Zapisano status."); }

// ---------- rozliczenie inwestycji: karta zużytych materiałów i karty materiałowe
let RM = null;
async function ladujRozlMat() { RM = await api(`/api/projekty/${REAL_ID}/rozliczenie-mat`).catch(() => null); if (RM) rysujRozlMat(); }
function rysujRozlMat() {
  const el = $("#rozl-mat"), P = RM.pozycje || [], dk = RM.dokumenty;
  el.innerHTML = `<p class="opis">Wykaz materiałów zużytych (wbudowanych) na budowie – do dołączenia do protokołu odbioru końcowego. Pozycje pobierzesz z
      ${RM.ma_liste ? "listy materiałów (krok „Zapotrzebowanie materiałowe”)" : "kosztorysu"}, każdą możesz zmienić, usunąć i dodać nowe.
      Zaznacz <b>Karta</b> przy materiałach, dla których potrzebna jest karta materiałowa, i dołącz do nich dokumenty (DoP, karta techniczna, certyfikat, aprobata).</p>
    <div class="pasek"><button class="zolty" data-ik="pobierz" onclick="importRozlMat(${P.length ? "false" : "true"})">${P.length ? "Dociągnij brakujące z kosztorysu" : "Pobierz materiały z kosztorysu"}</button>
      ${P.length ? `<button class="maly" onclick="importRozlMat(true)">Pobierz od nowa (zastąp)</button>` : ""}
      <button class="maly" data-ik="plus" onclick="dodajRozlMat()">Dodaj pozycję</button></div>
    ${P.length ? `<div class="tabela-okno" style="max-height:520px"><table class="tabela rm-tab"><tr><th>Karta</th><th>Materiał</th><th>Producent / typ</th><th>j.m.</th>
        <th>Ilość wg kosztorysu</th><th>Ilość zużyta</th><th>Dokumenty (DoP, CE/B…)</th><th>Miejsce wbudowania / uwagi</th><th>Załączniki karty</th><th></th></tr>
      ${P.map((x, i) => `<tr data-i="${i}"><td><input type="checkbox" class="rm-karta" ${x.karta ? "checked" : ""}></td>
        <td><input class="rm-nazwa" value="${esc(x.nazwa)}"><small class="opis">${esc(x.zrodlo || "")}</small></td><td><input class="rm-prod" value="${esc(x.producent || "")}"></td>
        <td><input class="rm-jm wn-k-in" style="width:56px" value="${esc(x.jm || "")}"></td><td class="liczba">${String(x.ilosc_kosztorys ?? "").replace(".", ",")}</td>
        <td><input class="rm-il wn-k-in" value="${String(x.ilosc_zuzyta ?? "").replace(".", ",")}"></td>
        <td><input class="rm-dok" value="${esc(x.dokumenty || "")}" placeholder="np. DoP 12/2026, CE"></td><td><input class="rm-uw" value="${esc(x.uwagi || "")}"></td>
        <td><div class="pliki-ik">${(x.zalaczniki || []).map(f => plikIk(REAL_ID, `realizacja/karty_materialowe/${x.id}/${f}`, f.length > 20 ? f.slice(0, 18) + "…" : f, 1)
          + `<button class="maly" title="Usuń załącznik" onclick="usunZalRozlMat('${x.id}','${escA(f)}')">×</button>`).join("")}</div>
          <label class="przycisk maly" data-ik="wgraj">Dołącz<input type="file" multiple hidden onchange="zalRozlMat('${x.id}', this.files)"></label></td>
        <td><button class="maly niebezp" data-ik="kosz" title="Usuń pozycję" onclick="RM.pozycje.splice(${i},1); zbierzRozlMat(true); rysujRozlMat()"></button></td></tr>`).join("")}</table></div>
      <div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="zapisz" onclick="zapiszRozlMat()">Zapisz wykaz</button>
        <button class="glowny" data-ik="dokument" onclick="dokRozlMat()">Generuj wykaz i karty materiałowe (Word, Excel, ZIP)</button>
        <span class="opis" style="margin:0">Pozycji: ${P.length} · z kartą: ${P.filter(x => x.karta).length}</span></div>` : '<p class="pusto">Brak pozycji – pobierz je z kosztorysu albo dodaj ręcznie.</p>'}
    ${dk ? `<h4 class="grupa-analizy">Dokumenty rozliczenia (${esc(dk.data)})</h4><div class="pliki-ik">${plikIk(REAL_ID, dk.wykaz, "Wykaz zużytych materiałów")}${plikIk(REAL_ID, dk.wykaz_xlsx, "Wykaz (Excel)")}
      ${dk.karty.map((k, i) => plikIk(REAL_ID, k, "Karta materiałowa " + (i + 1))).join("")}${plikIk(REAL_ID, dk.zip, "Komplet do protokołu końcowego (ZIP)")}</div>
      <p class="opis" style="font-size:12px">Przy protokole odbioru końcowego zaznacz „dołącz wykaz zużytych materiałów” – wykaz trafi do protokołu jako załącznik nr 1, a karty materiałowe zostaną wymienione w załącznikach.</p>` : ""}`;
  wstawIkony(el);
}
function zbierzRozlMat(cicho) {
  document.querySelectorAll(".rm-tab tr[data-i]").forEach(t => { const x = RM.pozycje[+t.dataset.i]; if (!x) return;
    Object.assign(x, {karta: t.querySelector(".rm-karta").checked, nazwa: t.querySelector(".rm-nazwa").value, producent: t.querySelector(".rm-prod").value,
      jm: t.querySelector(".rm-jm").value, ilosc_zuzyta: t.querySelector(".rm-il").value, dokumenty: t.querySelector(".rm-dok").value, uwagi: t.querySelector(".rm-uw").value}); });
}
function dodajRozlMat() { zbierzRozlMat(); RM.pozycje.push({id: Math.random().toString(16).slice(2, 10), nazwa: "", jm: "", ilosc_kosztorys: 0, ilosc_zuzyta: "", zrodlo: "dodane ręcznie"}); rysujRozlMat(); }
async function zapiszRozlMat(cicho) {
  zbierzRozlMat();
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/rozliczenie-mat`, {json: {pozycje: RM.pozycje}}));
  if (w && !cicho) { komunikat(`Zapisano wykaz: ${w.zapisano} pozycji.`); ladujRozlMat(); }
  return w;
}
async function importRozlMat(zastap) {
  if (zastap && RM.pozycje.length && !confirm("Zastąpić obecny wykaz pozycjami z kosztorysu? Twoje zmiany zostaną utracone.")) return;
  if (!zastap && RM.pozycje.length) await zapiszRozlMat(true);
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/rozliczenie-mat/import`, {json: {zastap}}));
  if (w) { komunikat(`Dodano ${w.dodano} pozycji (${w.zrodlo}).`); ladujRozlMat(); }
}
async function zalRozlMat(id, pliki) {
  await zapiszRozlMat(true); const fd = new FormData(); fd.append("id", id); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/rozliczenie-mat/zalacznik`, {method: "POST", body: fd}))) { komunikat("Dołączono."); ladujRozlMat(); }
}
async function usunZalRozlMat(id, plik) {
  if (!confirm(`Usunąć załącznik ${plik}?`)) return; const fd = new FormData(); fd.append("id", id); fd.append("usun", plik);
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/rozliczenie-mat/zalacznik`, {method: "POST", body: fd}))) ladujRozlMat();
}
async function dokRozlMat() {
  if (!(await zapiszRozlMat(true))) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/rozliczenie-mat/dokumenty`, {json: {}}));
  if (w) { komunikat(`Gotowe: wykaz${w.karty.length ? " i " + w.karty.length + " kart materiałowych" : ""}.`); ladujRozlMat(); }
}

// ---------- monitoring pogody (wykonawca)
let POGODA = null, POGODA_ID = null, POGODA_OKRES = null;
async function ladujPogode(nowa) {
  if (nowa || POGODA_ID !== REAL_ID) { POGODA = null; POGODA_OKRES = null; }
  if (!POGODA) {
    const q = POGODA_OKRES ? `?od=${POGODA_OKRES[0]}&do=${POGODA_OKRES[1]}` : "";
    const r = await fetch(`/api/projekty/${REAL_ID}/pogoda${q}`, {headers: {"X-Agent": "1"}}).catch(() => null);
    const d = r ? await r.json().catch(() => null) : null;
    if (!r || !r.ok) { $("#pogoda-tresc").innerHTML = `<p class="czerwone">${esc((d && d.blad) || "Nie udało się pobrać danych pogodowych.")}</p>` + formularzLokalizacji({}); return; }
    POGODA = d; POGODA_ID = REAL_ID;
  }
  rysujPogode();
}
function formularzLokalizacji(u) {
  return `<div class="pasek" style="margin:8px 0"><input id="pg-miasto" placeholder="Miejscowość budowy, np. Żarów" style="flex:1;min-width:200px" value="">
    <button class="maly" data-ik="szukaj" onclick="szukajMiejscaPogody()">Znajdź</button></div><div id="pg-podp"></div>`;
}
async function szukajMiejscaPogody() {
  const q = $("#pg-miasto").value.trim(); if (q.length < 2) return komunikat("Wpisz miejscowość.", true);
  const l = await bezpiecznie(() => api("/api/obszar/szukaj?q=" + encodeURIComponent(q))) || [];
  window.__pgPodp = l;
  $("#pg-podp").innerHTML = l.length ? l.slice(0, 6).map((m, i) => `<button class="maly" onclick="ustawMiejscePogody(${i})">${esc(m.opis || m.nazwa)}</button>`).join(" ") : '<span class="opis">Nie znaleziono.</span>';
}
async function ustawMiejscePogody(i) {
  const m = window.__pgPodp[i];
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/pogoda/ustawienia`, {json: {lokalizacja: {nazwa: m.nazwa, lat: m.lat, lon: m.lon, opis: m.opis || m.nazwa}}}))) ladujPogode(true);
}
function rysujPogode() {
  const P = POGODA, u = P.ustawienia, kr = u.kryteria || {};
  if (P.blad_lokalizacji) {
    $("#pogoda-stan").textContent = "ustaw lokalizację";
    $("#pogoda-tresc").innerHTML = `<p class="opis">Podaj lokalizację budowy – program znajdzie najbliższą stację synoptyczną IMGW i będzie sprawdzał pogodę w godzinach pracy.</p>` + formularzLokalizacji(u);
    return;
  }
  const przeszle = P.dni.filter(x => !x.prognoza), prog = P.dni.filter(x => x.prognoza);
  $("#pogoda-stan").textContent = `${P.niekorzystne} dni niekorzystnych`;
  const zl1 = v => v == null ? "–" : String(v).replace(".", ",");
  const st = P.stacja, pm = st && st.pomiar;
  const wiersz = x => `<tr class="${x.niekorzystny && x.roboczy ? "niek" : ""} ${!x.roboczy ? "wolny" : ""}"><td>${esc(dataPl(x.data))}</td><td>${x.dzien}</td>
    <td>${zl1(x.tmin)} … ${zl1(x.tmax)}</td><td>${zl1(x.opad)}</td><td>${zl1(x.snieg)}</td><td>${zl1(x.wiatr)} / ${zl1(x.porywy)}</td>
    <td>${x.meteo ? `<small>${x.meteo.opad ? `opad ${zl1(x.meteo.opad.suma || 0)} mm${x.meteo.opad.praca != null ? ` (w godz. pracy ${zl1(x.meteo.opad.praca)})` : ""}<br>` : ""}${x.meteo.temperatura ? `t ${zl1(x.meteo.temperatura.min)} … ${zl1(x.meteo.temperatura.max)}°C<br>` : ""}${(x.meteo.wiatr_max || x.meteo.wiatr) ? `wiatr do ${zl1((x.meteo.wiatr_max || x.meteo.wiatr).max)} m/s${x.meteo.poryw ? `, porywy ${zl1(x.meteo.poryw.max)}` : ""}<br>` : ""}<span class="opis">${x.meteo._zrodlo ? esc(x.meteo._zrodlo) : `kompletność ${x.meteo_kompletnosc}%`}${x.potwierdzone_pomiarem ? ' · <b class="czerwone">potwierdzone pomiarem</b>' : ""}</span>${x.meteo.opad_dobowy ? `<br><span class="opis">opad dobowy IMGW: ${zl1(x.meteo.opad_dobowy.wartosc)} mm (${esc(x.meteo.opad_dobowy.okres || "")})</span>` : ""}${x.uwaga_meteo ? `<br><span style="background:var(--zolty-jasny)">${esc(x.uwaga_meteo)}</span>` : ""}</small>` : ""}
      ${(x.imgw || []).length ? `${x.meteo ? "<br>" : ""}<small class="opis">synop: ${(x.imgw || []).map(p => `${esc(p.godzina)}:00 ${zl1(p.temperatura)}°C, ${zl1(p.opad)} mm`).join("; ")}</small>` : x.meteo ? "" : "–"}</td>
    <td>${!x.roboczy ? '<span class="opis">wolny</span>' : x.niekorzystny ? `<b class="czerwone">✖ ${esc(x.powody.join("; "))}</b>` : '<span class="zielone">✔ sprzyjające</span>'}</td></tr>`;
  $("#pogoda-tresc").innerHTML = `<div class="dwie" style="gap:14px">
    <div><p class="opis" style="margin-top:0">Lokalizacja: <b>${esc(u.opis || "")}</b> (${Number(u.lat).toFixed(3)}, ${Number(u.lon).toFixed(3)})
      <a href="#" onclick="$('#pg-zmiana').classList.toggle('ukryj'); return false">zmień</a></p>
      <div id="pg-zmiana" class="ukryj">${formularzLokalizacji(u)}</div>
      ${Object.keys(P.stacje_meteo || {}).length ? `<div class="karta" style="margin-bottom:10px"><b>${ik("flaga")} Najbliższe stacje IMGW-PIB – sieć telemetryczna (osobno dla każdego pomiaru)</b>
        <div class="tabela-okno"><table class="tabela" style="margin-top:6px"><tr><th>Pomiar</th><th>Stacja</th><th>Odległość</th><th>Wartość</th><th>Czas pomiaru</th></tr>
        ${Object.values(P.stacje_meteo).map(x => `<tr><td>${esc(x.opis)}</td><td>${esc(x.stacja)}</td><td class="liczba">${zl1(x.odl_km)} km</td><td class="liczba">${zl1(x.wartosc)} ${esc(x.jednostka)}</td><td>${esc(String(x.czas || "").slice(0, 16))}</td></tr>`).join("")}</table></div>
        <p class="opis" style="margin:4px 0 0">Oficjalne pomiary IMGW-PIB z najbliższej stacji mierzącej dany parametr (pomiary nie starsze niż 6 godzin). Program zapisuje je co 10 minut${P.meteo_historia_od ? ` – historia od ${esc(dataPl(P.meteo_historia_od))}` : " – historia zacznie się od pierwszego zapisu"}; dobowe sumy i ekstrema są w tabeli dni (kolumna IMGW, z kompletnością – luki, gdy serwer był uśpiony). Dane godzinowe dla dokładnego punktu budowy – Open-Meteo.</p></div>` : ""}
      ${st ? `<div class="karta pogoda-teraz"><b>${ik("flaga")} Najbliższa stacja IMGW: ${esc(st.nazwa)}</b> <span class="opis">(${zl1(st.odl_km)} km)</span><br>
        ${pm ? `Pomiar ${esc(dataPl(pm.data))} godz. ${esc(pm.godzina)}:00 – <b>${zl1(pm.temperatura)}°C</b>, wiatr ${zl1(pm.wiatr)} m/s, opad ${zl1(pm.opad)} mm, wilgotność ${zl1(pm.wilgotnosc)}%` : ""}</div>`
        : '<p class="opis">Stacja IMGW chwilowo niedostępna – ocena z danych godzinowych dla lokalizacji budowy.</p>'}</div>
    <div class="karta" style="margin:0"><b>Progi dla robót</b>
      <div class="siatka" style="margin-top:6px"><label>Rodzaj robót<select id="pg-rodzaj" onchange="zapiszUstPogody(true)">${Object.entries(P.presety).map(([k, v]) =>
        `<option value="${k}" ${k === u.rodzaj ? "selected" : ""}>${esc(v.nazwa)}</option>`).join("")}</select></label></div>
      <div class="siatka"><label>Temp. min [°C]<input id="pg-tmin" value="${kr.tmin}"></label><label>Temp. max [°C]<input id="pg-tmax" value="${kr.tmax}"></label>
        <label>Opad deszczu od [mm]<input id="pg-opad" value="${kr.opad}"></label><label>Śnieg powyżej [cm]<input id="pg-snieg" value="${kr.snieg}"></label>
        <label>Wiatr powyżej [m/s]<input id="pg-wiatr" value="${kr.wiatr}"></label><label>Godziny pracy<span style="display:flex;gap:4px"><input id="pg-godz-od" value="${kr.godz_od}" style="width:60px">–<input id="pg-godz-do" value="${kr.godz_do}" style="width:60px"></span></label></div>
      <label class="check"><input type="checkbox" id="pg-soboty" ${u.soboty ? "checked" : ""}> soboty są dniami roboczymi</label>
      <button class="maly zielony" data-ik="zapisz" onclick="zapiszUstPogody(false)">Zapisz progi</button></div></div>
    ${prog.length ? `<h4 class="grupa-analizy">Prognoza na najbliższe dni</h4><div class="prognoza">${prog.map(x => `<div class="${x.roboczy && x.niekorzystny ? "niek" : "ok"}">
      <b>${x.dzien} ${esc(dataPl(x.data).slice(0, 5))}</b><span>${zl1(x.tmin)}…${zl1(x.tmax)}°C</span><span>${zl1(x.opad)} mm · ${zl1(x.wiatr)} m/s</span>
      <small>${x.niekorzystny ? "✖ " + esc(x.powody[0] || "") : "✔ pogoda sprzyja"}</small></div>`).join("")}</div>` : ""}
    <h4 class="grupa-analizy">Warunki na budowie w godzinach pracy</h4>
    <div class="pasek"><label>Od <input type="date" id="pg-od" value="${P.od}"></label><label>Do <input type="date" id="pg-do" value="${P.do}"></label>
      <button class="maly" data-ik="szukaj" onclick="POGODA_OKRES=[$('#pg-od').value, $('#pg-do').value]; POGODA=null; ladujPogode()">Pokaż okres</button>
      <span class="opis" style="margin:0"><b class="${P.niekorzystne ? "czerwone" : "zielone"}">${P.niekorzystne} z ${P.robocze} dni roboczych</b> z warunkami uniemożliwiającymi prace</span></div>
    <div class="tabela-okno" style="max-height:420px"><table class="tabela pogoda-tab"><tr><th>Data</th><th>Dzień</th><th>Temp. [°C]</th><th>Opad [mm]</th><th>Śnieg [cm]</th><th>Wiatr / porywy [m/s]</th><th>Pomiar IMGW</th><th>Ocena</th></tr>
      ${przeszle.slice().reverse().map(wiersz).join("")}</table></div>
    <div class="korekta" style="display:block;margin-top:14px"><h3>${ik("dokument")} Pismo do zamawiającego</h3>
      <p class="opis">Program przygotuje pismo w Wordzie z zestawieniem dni niekorzystnych w wybranym okresie (tabela dni, przyczyny, stacja IMGW, dane godzinowe),
        z Twoimi danymi i danymi zamawiającego oraz numerem umowy.</p>
      <div class="siatka"><label>Rodzaj pisma<select id="pg-rodzaj-pisma"><option value="wniosek">Wniosek o przedłużenie terminu realizacji</option>
          <option value="informacja">Informacja o warunkach uniemożliwiających prace</option></select></label>
        <label>Przedłużenie o [dni robocze z warunkami niekorzystnymi]<input id="pg-dni" inputmode="numeric" value="${P.niekorzystne}"></label>
        <label>Termin w umowie liczony w dniach<select id="pg-liczenie" onchange="pgLiczenie(this.value)">
          <option value="robocze" ${(u.liczenie || "robocze") === "robocze" ? "selected" : ""}>roboczych (bez sobót, niedziel i świąt)</option>
          <option value="kalendarzowe" ${u.liczenie === "kalendarzowe" ? "selected" : ""}>kalendarzowych – program przeliczy dni robocze jawnie</option></select></label>
        <label>Miejscowość pisma<input id="pg-miejsce" placeholder="np. Świdnica"></label>
        <label style="grid-column: 1 / -1">Wpisy w dzienniku budowy (EDB) – numery lub daty (opcjonalnie)<input id="pg-wpisy" placeholder="np. wpisy nr 12–15 z 03–06.03.2027 – puste: program wskaże raporty dzienne albo pole [UZUPEŁNIJ]"></label>
        <label style="grid-column: 1 / -1">Uwagi / dodatkowe uzasadnienie (opcjonalnie)<input id="pg-uwagi" placeholder="np. przestoje uzgodnione z inspektorem nadzoru"></label></div>
      <p class="opis" style="margin:4px 0">Liczba dni przedłużenia to dni robocze, w których pogoda uniemożliwiała prace. Gdy umowa liczy termin w dniach roboczych, nowy termin to termin umowny + tyle dni roboczych (bez sobót, niedziel i świąt);
        gdy w kalendarzowych – pismo podaje przeliczenie na dni kalendarzowe. Zdanie o dzienniku budowy program pisze tylko na podstawie wpisów: numerów podanych wyżej albo raportów dziennych zapisanych w programie – w innym razie zostawia pole do uzupełnienia.</p>
      <div class="pasek"><button class="zielony" data-ik="dokument" onclick="pismoPogodowe()">Generuj pismo (Word)</button>
        <button data-ik="kalendarz" onclick="przesunTermin()">Przesuń termin i harmonogram (po zgodzie zamawiającego)</button></div>
      <div id="pg-wynik"></div></div>
    <p class="opis" style="font-size:12px">Dane: pomiary stacji synoptycznych IMGW-PIB (zapisywane w historii budowy przy każdym odświeżeniu i automatycznie kilka razy dziennie)
      oraz dane godzinowe Open-Meteo dla współrzędnych budowy (ostatnie tygodnie i prognoza 7 dni). Urzędowe dane archiwalne IMGW: danepubliczne.imgw.pl.</p>`;
}
async function zapiszUstPogody(zmianaRodzaju) {
  const d = {rodzaj: $("#pg-rodzaj").value, godz_od: $("#pg-godz-od").value, godz_do: $("#pg-godz-do").value, soboty: $("#pg-soboty").checked};
  if (!zmianaRodzaju) d.kryteria = {tmin: $("#pg-tmin").value, tmax: $("#pg-tmax").value, opad: $("#pg-opad").value, snieg: $("#pg-snieg").value, wiatr: $("#pg-wiatr").value};
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/pogoda/ustawienia`, {json: d}))) { komunikat("Zapisano progi."); POGODA = null; ladujPogode(); }
}
async function pismoPogodowe() {
  const d = {od: $("#pg-od").value, do: $("#pg-do").value, rodzaj: $("#pg-rodzaj-pisma").value, dni: $("#pg-dni").value, miejsce: $("#pg-miejsce").value, uwagi: $("#pg-uwagi").value,
    liczenie: $("#pg-liczenie").value, wpisy_dziennika: $("#pg-wpisy").value};
  komunikat("Przygotowuję pismo…");
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/pogoda/pismo`, {json: d})); if (!w) return;
  $("#pg-wynik").innerHTML = `<div class="pliki-wynik"><a href="${w.url}">${esc(decodeURIComponent(w.url.split("/").pop()))}</a></div>
    <p class="opis">Dni niekorzystnych w okresie: <b>${w.niekorzystne}</b>; wnioskowane przedłużenie: <b>${w.liczenie === "kalendarzowe" ? `${w.dni_kalendarzowe} dni kalendarzowych (= ${w.dni} dni roboczych)` : `${w.dni} dni roboczych`}</b>${w.nowy_termin ? `, nowy termin: <b>${esc(dataPl(w.nowy_termin))}</b>` : ""}. Pismo zapisano też w dokumentach budowy.</p>`;
  location.href = w.url;
}
function pgLiczenie(v) { api(`/api/projekty/${REAL_ID}/pogoda/ustawienia`, {json: {liczenie: v}}).then(() => { if (POGODA && POGODA.ustawienia) POGODA.ustawienia.liczenie = v; }).catch(() => {}); }
async function przesunTermin() {
  const kal = $("#pg-liczenie") && $("#pg-liczenie").value === "kalendarzowe";
  const n = prompt(`O ile dni ${kal ? "kalendarzowych" : "roboczych (bez sobót, niedziel i świąt)"} przesunąć termin zakończenia i nieodebrane etapy harmonogramu? (zrób to po zgodzie zamawiającego / aneksie)`, $("#pg-dni").value);
  if (!n) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/pogoda/przesun`, {json: {dni: n, liczenie: kal ? "kalendarzowe" : "robocze"}}));
  if (w) { komunikat(`Nowy termin zakończenia: ${dataPl(w.termin_zakonczenia || "")} (+${w.dni_kalendarzowe} dni kalendarzowych); przesunięto etapów: ${w.etapy}.`); odswiezReal(); }
}

// ---------- budowa domu: budżet, wykonawcy, formalności, transze
function kwotyDomu(R) {
  const r = R.realizacja, s = R.podsumowanie, vat = (r.vat === "" || r.vat == null) ? 0.23 : (+r.vat > 1 ? +r.vat / 100 : +r.vat);
  const budzet = (s.wartosc_umowy_netto || 0) * (1 + vat), wydane = (s.zafakturowano_brutto || 0) + (s.koszty_netto || 0);
  const umowy = (r.wykonawcy || []).reduce((a, w) => a + (+w.kwota || 0), 0);
  const kredyt = (r.transze || []).reduce((a, t) => a + (t.status === "wypłacona" ? +t.kwota || 0 : 0), 0);
  const k = (et, v, kl = "") => `<div class="${kl}"><span>${et}</span><b>${zl(v)}</b></div>`;
  return `<div class="kwoty">${k("Budżet brutto (kosztorys)", budzet)}${k("Wydano razem", wydane, wydane > budzet && budzet ? "alarm" : "")}
    ${k("Pozostało z budżetu", budzet - wydane, budzet - wydane < 0 ? "alarm" : "brutto")}${k("Faktury do zapłaty", s.naleznosci_brutto)}
    ${s.przeterminowane_brutto ? k("Po terminie", s.przeterminowane_brutto, "alarm") : ""}${umowy ? k("Umowy z wykonawcami", umowy) : ""}
    ${kredyt ? k("Wypłacone transze kredytu", kredyt) : ""}</div>
    ${budzet ? `<div class="pasek-postepu" title="Wykorzystanie budżetu"><div style="width:${Math.min(100, wydane / budzet * 100).toFixed(1)}%"></div>
      <span>wykorzystano ${(wydane / budzet * 100).toFixed(1).replace(".", ",")}% budżetu</span></div>` : ""}`;
}
function sekcjeDomu(R) {
  const r = R.realizacja, W = r.wykonawcy || [], F = r.formalnosci || [], T = r.transze || [];
  const wyd = (w) => (r.faktury || []).filter(f => (f.opis || "").toLowerCase().includes((w.nazwa || "").toLowerCase().slice(0, 12)) && w.nazwa).reduce((a, f) => a + f.brutto, 0);
  return `<div class="krok k-ziel" id="sek-wykonawcy"><div class="tytul"><span class="nr">${ik("ludzie")}</span><h3>Wykonawcy i ekipy</h3>
      <span class="stan">${odm(W.length, "wykonawca", "wykonawców", "wykonawców")}</span></div><div class="tresc">
    <p class="opis">Ekipy i firmy na budowie z zakresem prac i kwotą umowy. Wybierzesz je przy protokole odbioru etapu; faktury z nazwą wykonawcy w opisie sumują się przy nim.</p>
    ${W.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Wykonawca</th><th>Zakres / etap</th><th>Kontakt</th><th>Umowa</th><th>Faktury</th><th></th></tr>
      ${W.map(w => `<tr><td><b>${esc(w.nazwa)}</b>${w.nip ? `<br><small class="opis">NIP ${esc(w.nip)}</small>` : ""}</td><td>${esc(w.zakres || "")}</td>
        <td>${esc(w.telefon || "")}${w.email ? `<br><a href="mailto:${esc(w.email)}">${esc(w.email)}</a>` : ""}</td>
        <td class="liczba">${w.kwota ? zl(w.kwota) : "–"}</td><td class="liczba">${zl(wyd(w))}</td>
        <td><button class="maly niebezp" data-ik="kosz" onclick="domZapisz('wykonawcy', {id: '${w.id}', usun: true})"></button></td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak wykonawców.</p>'}
    <div class="siatka" style="margin-top:10px"><label>Nazwa / ekipa<input id="dw-nazwa" placeholder="np. Firma Budex – stan surowy"></label>
      <label>Zakres / etap<input id="dw-zakres" placeholder="np. fundamenty i ściany"></label><label>Telefon<input id="dw-tel"></label>
      <label>E-mail<input id="dw-email"></label><label>NIP<input id="dw-nip"></label><label>Kwota umowy brutto<input id="dw-kwota"></label></div>
    <button class="zielony maly" data-ik="plus" onclick="domDodajWykonawce()">Dodaj wykonawcę</button></div></div>

  <div class="krok k-zolt" id="sek-formalnosci"><div class="tytul"><span class="nr">${ik("protokol")}</span><h3>Formalności budowy</h3>
      <span class="stan">${F.filter(x => x.status === "zrobione" || x.status === "nie dotyczy").length}/${F.length} załatwionych</span></div><div class="tresc">
    <p class="opis">Lista spraw urzędowych i odbiorów przy budowie domu – od pozwolenia do zawiadomienia o zakończeniu budowy. Oznaczaj postęp i zapisuj daty.</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Sprawa</th><th>Status</th><th>Data</th><th>Uwagi</th><th></th></tr>
      ${F.map(x => `<tr class="${x.status === "zrobione" || x.status === "nie dotyczy" ? "zalatwione" : ""}"><td>${esc(x.nazwa)}</td><td><select onchange="domZapisz('formalnosci', {id: '${x.id}', status: this.value})">${["do zrobienia", "w toku", "zrobione", "nie dotyczy"].map(s => `<option ${s === x.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
        <td><input type="date" value="${esc(x.data || "")}" onchange="domZapisz('formalnosci', {id: '${x.id}', data: this.value})"></td>
        <td><input value="${esc(x.uwagi || "")}" placeholder="np. nr decyzji, termin" onchange="domZapisz('formalnosci', {id: '${x.id}', uwagi: this.value})"></td>
        <td><button class="maly" data-ik="kosz" title="Usuń z listy" onclick="domZapisz('formalnosci', {id: '${x.id}', usun: true})"></button></td></tr>`).join("")}</table></div>
    <div class="pasek" style="margin-top:8px"><input id="df-nowa" placeholder="Dodaj własną sprawę, np. wycinka drzew" style="flex:1;min-width:220px">
      <button class="maly" data-ik="plus" onclick="domZapisz('formalnosci', {nowa: $('#df-nowa').value})">Dodaj</button></div></div></div>

  <div class="krok" id="sek-transze"><div class="tytul"><span class="nr">${ik("portfel")}</span><h3>Transze kredytu</h3>
      <span class="stan">${T.length ? zl(T.filter(t => t.status === "wypłacona").reduce((a, t) => a + (+t.kwota || 0), 0)) + " wypłacone" : "opcjonalnie"}</span></div><div class="tresc">
    <p class="opis">Jeśli budujesz na kredyt: transze z warunkiem wypłaty (np. „stan surowy zamknięty”), planowaną datą i statusem.</p>
    ${T.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Warunek / etap</th><th>Kwota</th><th>Planowana data</th><th>Status</th><th>Wypłacono</th><th></th></tr>
      ${T.map(t => `<tr><td>${esc(t.warunek || "")}</td><td class="liczba">${zl(t.kwota || 0)}</td><td>${esc(dataPl(t.data || ""))}</td>
        <td><select onchange="domZapisz('transze', {id: '${t.id}', status: this.value, data_wyplaty: this.value === 'wypłacona' ? dzis() : ''})">${["planowana", "wniosek złożony", "wypłacona"].map(s => `<option ${s === t.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
        <td>${esc(dataPl(t.data_wyplaty || ""))}</td><td><button class="maly niebezp" data-ik="kosz" onclick="domZapisz('transze', {id: '${t.id}', usun: true})"></button></td></tr>`).join("")}</table></div>` : ""}
    <div class="siatka" style="margin-top:8px"><label>Warunek / etap<input id="dt-war" placeholder="np. stan surowy zamknięty"></label><label>Kwota<input id="dt-kwota"></label>
      <label>Planowana data<input type="date" id="dt-data"></label></div>
    <button class="maly zielony" data-ik="plus" onclick="domZapisz('transze', {warunek: $('#dt-war').value, kwota: $('#dt-kwota').value, data: $('#dt-data').value})">Dodaj transzę</button></div></div>`;
}
async function domZapisz(rodzaj, d) {
  if (d.usun && !confirm("Usunąć?")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/${rodzaj}`, {json: d}))) odswiezReal();
}
async function domDodajWykonawce() {
  const d = {nazwa: $("#dw-nazwa").value, zakres: $("#dw-zakres").value, telefon: $("#dw-tel").value, email: $("#dw-email").value, nip: $("#dw-nip").value, kwota: $("#dw-kwota").value};
  if (NIP_OK(d.nip) && !d.nazwa) { const n = await pobierzNip(d.nip); if (n) { d.nazwa = n.nazwa; d.adres = n.adres; } }
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/wykonawcy`, {json: d}))) { komunikat("Dodano wykonawcę."); odswiezReal(); }
}
const NIP_OK = n => /^\d{10}$/.test(String(n || "").replace(/\D/g, ""));
function kartaProjektu(id, typ) {
  const w = {przetarg: "projekty", wlasny: "wlasne", kosztorys: STRONA === "kosztorysant" ? "kos_projekty" : "kosztorys", zamowienie: "zam_projekty", dom: "inw_projekty", dotacja: "dot_projekty", wniosek_dot: "dot_wnioski"}[typ] || "projekty";
  PROJEKT_ID = id; TRYB = TRYBY[w]; pokaz(w);
}

// ---------- moduły zamawiającego: weryfikacja i sporządzanie dokumentacji
const NAZWY_ZADAN = {szukaj: "Wyszukiwanie i ocena przetargów", pobieranie: "Pobieranie ogłoszeń", bip: "Strony instytucji", ocena: "Ocena przetargów",
  pelna: "Pełna analiza z dokumentami", weryfikacja: "Sprawdzenie dokumentacji", oferta: "Kosztorys i oferta", ocena_ofert: "Sprawdzenie ofert",
  ocena_swz: "Kryteria z SWZ", analiza_dostawcy: "Analiza przetargu (dostawca)", zalaczniki: "Załączniki oferty", inne: "Inne"};
let UWAGI_OTW = false;  // uwagi w kroku „Błędy w dokumentach” zwinięte, dopóki nie klikniesz „Pokaż uwagi”
function krokZamawiajacego(p, rodzaj, nr = 2) {
  if ((rodzaj || p.typ) === "weryfikacja") {
    const w = p.weryfikacja, U = (w && w.uwagi) || [];
    const kol = {krytyczna: "z-czerwony", istotna: "z-do-analizy", drobna: "z-odpuszczamy"};
    const WYK = ["wykonawca", "dostawca"].includes(p.strona) || ["przetarg", "wlasny"].includes(p.typ) || (p.typ === "prawnik" && (p.prawnik || {}).dla_kogo === "wykonawca");  // porady dla wykonawcy, nie dla zamawiającego
    const ST = WYK ? {"do poprawy": "otwarte", "poprawione": "wyjaśnione", "odrzucone": "nieistotne"} : {"do poprawy": "do poprawy", "poprawione": "poprawione", "odrzucone": "odrzucone"};
    const otw = U.filter(u => u.status === "do poprawy").length;
    return `<div class="krok k-czer" id="sek-weryfikacja"><div class="tytul"><span class="nr">${ik("alarm")}</span><h3>${nr}. ${WYK ? "Błędy i ryzyka w dokumentach przetargu" : "Sprawdzenie dokumentacji przetargowej"}</h3>
      <span class="stan">${w ? (WYK ? odm(otw, "otwarta uwaga", "otwarte uwagi", "otwartych uwag") : odm(otw, "uwaga do poprawy", "uwagi do poprawy", "uwag do poprawy")) : "do zrobienia"}</span></div><div class="tresc">
      <p class="opis">${WYK ? `AI czyta dokumenty oczami wykonawcy: sprzeczności, braki w przedmiarze, niejasności i ryzyka (kary, ryczałt, terminy) – przy każdej uwadze
        mówi, <b>co zrobić</b>, i daje gotowe <b>pytanie do zamawiającego</b>. Te same uwagi są potem podstawą wniosków w <b>Zmianach umowy i aneksach</b>
        (roboty dodatkowe lub zamienne, przedłużenie terminu, zmiana wynagrodzenia).`
        : `AI porównuje dokumenty między sobą i z przepisami: sprzeczności (terminy, wadium, zakres, gwarancja), błędy, braki,
        zapisy ryzykowne lub niezgodne z Pzp i zasadą konkurencyjności – z propozycją poprawionego zapisu. Uwagi wykorzystasz także przy zmianach umowy i aneksach.`}</p>
      ${w && w.nieaktualna ? `<div class="ramka-uwaga">${esc(w.nieaktualna)}</div>` : ""}
      ${WYK && p.termin_pytan ? (() => { const t = p.termin_pytan; return `<div class="${t.minal ? "ramka-uwaga" : "karta"}" style="margin:0 0 10px;padding:10px 14px">
        ${ik("kalendarz")} <b>Pytania do zamawiającego z obowiązkiem odpowiedzi: do ${esc(dataPl(t.data))}</b>
        ${t.praktycznie ? ` (dzień wolny – praktycznie do ${esc(dataPl(t.praktycznie))})` : ""}
        <span class="opis" style="margin:0"> · ${t.dni_przed} dni przed terminem składania ofert ${esc(dataPl(t.termin_ofert))} (${esc(t.podstawa)})
        ${t.minal ? " · <b>termin minął – zamawiający może nie odpowiedzieć i nie musi przedłużać terminu składania ofert</b>" : t.dni === 0 ? " · <b>to dziś</b>" : ` · zostało ${odm(t.dni, "dzień", "dni", "dni")}`}</span></div>`; })() : ""}
      <textarea id="wer-dod" placeholder="${WYK ? "Na co zwrócić uwagę (opcjonalnie), np. „ilości w przedmiarze”, „kary umowne”, „termin realizacji”" : "Na co zwrócić szczególną uwagę (opcjonalnie), np. „zgodność przedmiaru z projektem”, „klauzule waloryzacyjne”"}"></textarea>
      ${!WYK && p.typ !== "prawnik" && p.tryby_weryfikacji ? `<label style="margin:4px 0">Tryb postępowania (lista kontrolna jak w kreatorze i u prawnika)
        <select id="wer-tryb">${Object.entries(p.tryby_weryfikacji).map(([k, t]) => `<option value="${k}" ${k === p.weryfikacja_tryb ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>` : ""}
      <label class="wiersz" style="margin:4px 0"><input type="checkbox" id="wer-dokl"> Dokładne sprawdzenie – najdokładniejszy model AI (kilka razy droższy; zalecane przy dużych zamówieniach)</label>
      <div class="pasek" style="margin-top:8px"><button class="zolty" data-ik="iskra" onclick="uruchomWeryfikacje()">${w ? "Sprawdź ponownie" : WYK ? "Wykryj błędy (AI)" : "Sprawdź dokumentację"}</button>
        ${WYK && U.some(u => u.pytanie_do_zamawiajacego) ? `<button class="maly" data-ik="dokument" onclick="kopiujPytaniaWer()">Kopiuj pytania do zamawiającego</button>` : ""}
        ${w ? `<a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${PROJEKT_ID}/weryfikacja.docx">Raport (Word)</a>` : ""}</div>
      ${w ? `<div class="karta" style="margin:12px 0"><b>Ocena: ${esc(w.ocena)}</b> <span class="opis">· ${esc(w.data)}</span><p style="margin:6px 0 0">${esc(w.podsumowanie)}</p></div>
        ${U.length ? `<button class="maly" style="width:100%;justify-content:center" onclick="UWAGI_OTW = !UWAGI_OTW; rysujProjekt()">${UWAGI_OTW ? "Zwiń uwagi ▲" : `Pokaż uwagi (${U.length}) ▼`}</button>` : ""}
        ${!UWAGI_OTW && U.length ? "" : U.map(u => `<div class="alert-k ${u.waga === "krytyczna" ? "ostrzezenie" : ""} ${u.status !== "do poprawy" ? "zastosowany" : ""}">
          <div class="alert-gora"><span class="znacznik ${kol[u.waga]}">${esc(u.waga)}</span><b>${esc(u.kategoria)}</b>
            <small class="opis" style="margin:0">${esc(u.dokument)}${u.odw ? " · " + odwChip(u.odw, u.miejsce, {typ: "projekt", id: PROJEKT_ID}) : u.miejsce ? " · " + esc(u.miejsce) : ""}</small></div>
          ${u.cytat ? `<div class="cytat">„${esc(u.cytat)}”</div>` : ""}
          <div>${odwWTresci(esc(u.opis), u, {typ: "projekt", id: PROJEKT_ID})}</div>
          ${u.propozycja ? `<div class="sugestia"><b>${WYK ? "Co zrobić:" : "Propozycja:"}</b> ${esc(u.propozycja)}</div>` : ""}
          ${!WYK && u.cytat && (u.nowy_tekst || u.nowy_edyt) ? `<div class="kz-diff" style="margin-top:6px"><small class="opis">Nowe brzmienie (zastąpi cytat – możesz poprawić):</small>
            <textarea class="kz-nowy wer-nowy" data-id="${u.id}" rows="2">${esc(u.nowy_edyt ?? u.nowy_tekst)}</textarea>
            <div class="pasek" style="margin:4px 0 0"><button class="maly ${u.zmiana === "tak" ? "glowny" : ""}" onclick="werDecyzja('${u.id}', 'tak')">✓ Akceptuj zmianę</button>
              <button class="maly" onclick="werDecyzja('${u.id}', 'nie')">✕ Odrzuć</button>${u.wprowadzona ? `<span class="znacznik z-startujemy">wprowadzona ${esc(u.wprowadzona)}</span>` : ""}</div></div>` : ""}
          ${WYK && u.pytanie_do_zamawiajacego ? `<div class="cytat" style="border-left-color:#0284c7"><b>Pytanie do zamawiającego:</b> ${esc(u.pytanie_do_zamawiajacego)}</div>` : ""}
          <div class="pasek" style="margin:8px 0 0"><select onchange="statusUwagi('${u.id}', this.value)">${["do poprawy", "poprawione", "odrzucone"].map(s => `<option value="${s}" ${s === u.status ? "selected" : ""}>${ST[s]}</option>`).join("")}</select></div>
        </div>`).join("") || '<p class="zielone"><b>Nie znaleziono uwag.</b></p>'}
        ${!WYK && U.some(u => u.nowy_tekst || u.nowy_edyt) ? (() => { const wp = w.wprowadzanie; return `<div class="karta" style="margin:10px 0;border-left:4px solid #1F5A99">
          <b>Wprowadzanie zmian</b> <span class="opis">– zaakceptowano: ${U.filter(u => u.zmiana === "tak").length}. Powstaną dokumenty Word ze śledzeniem zmian i czyste; PDF z tekstem program zamieni na Word. Ogłoszenie z BZP zmienia się w e-Zamówieniach – dostaniesz zestawienie zmian do formularza.</span>
          <div class="pasek" style="margin:6px 0 0"><button class="maly" onclick="werWszystkie('tak')">Akceptuj wszystkie</button><button class="glowny" data-ik="dokument" onclick="werWprowadz()">Wprowadź zaakceptowane zmiany</button></div>
          ${wp ? `<p class="opis" style="margin:6px 0 0">${esc(wp.data)}: ${wp.wynik.map(x => `${esc(x.word)} – wprowadzono ${x.wprowadzone}${x.info ? " (" + esc(x.info) + ")" : ""}`).join("; ") || "brak zmian w plikach"}</p>
            <div class="pliki-wynik">${wp.pliki.map(n => `<a href="/pobierz/${PROJEKT_ID}/dokumenty_poprawione/${encodeURIComponent(n)}">${esc(n)}</a>`).join("")}</div>
            ${wp.reczne.length ? `<div class="ramka-uwaga"><b>Do wprowadzenia ręcznie (${wp.reczne.length}):</b><ul class="lista">${wp.reczne.map(r => `<li>${esc(r.miejsce || r.dokument || "")}: ${esc((r.nowy_tekst || r.propozycja || "").slice(0, 160))} <small class="opis">(${esc(r.powod)})</small></li>`).join("")}</ul></div>` : ""}` : ""}</div>`; })() : ""}` : ""}
    </div></div>`;
  }
  const RZd = p.rodzaj_zamowienia || "roboty", PRZ = {
    roboty: {nazwa: "np. Termomodernizacja budynku szkoły", warunki: "np. 2 roboty po 500 tys. zł w ostatnich 5 latach; kierownik budowy z uprawnieniami", zakres: "Zakres zamówienia – opis robót",
             zakres_ph: "np. docieplenie ścian EPS 15 cm (ok. 1850 m²), wymiana stolarki okiennej, remont dachu…", gw: "np. 60 miesięcy", kryt: "np. cena 60%, gwarancja 40%"},
    uslugi: {nazwa: "np. Sprzątanie budynków urzędu w 2027 r.", warunki: "np. 1 usługa podobna o wartości min. 100 tys. zł w ostatnich 3 latach; personel z doświadczeniem", zakres: "Zakres zamówienia – opis usług",
             zakres_ph: "np. sprzątanie 2 400 m² powierzchni biurowych 5 dni w tygodniu, mycie okien 2 razy w roku, przez 12 miesięcy…", gw: "np. nie dotyczy / czas reakcji na reklamację 2 h", kryt: "np. cena 60%, czas reakcji 40%"},
    dostawy: {nazwa: "np. Dostawa mebli szkolnych", warunki: "np. brak szczegółowych warunków (oświadczenie o braku podstaw wykluczenia)", zakres: "Zakres zamówienia – opis dostaw (asortyment i ilości)",
              zakres_ph: "np. 60 ławek szkolnych regulowanych, 120 krzeseł, 2 tablice interaktywne – z dostawą, wniesieniem i montażem…", gw: "np. 24 miesiące", kryt: "np. cena 60%, termin dostawy 40%"}}[RZd] || {};
  const D = p.dokumentacja_domyslne || {pola: {}, zrodla: {}}, f = Object.assign({}, D.pola, p.dokumentacja_pola || {}), dk = p.dokumentacja;
  const zrd = id => (p.dokumentacja_pola || {})[id] ? "" : D.zrodla[id] ? `<small class="kz-zr ${/do aktualizacji/.test(D.zrodla[id]) ? "kz-akt" : ""}">${esc(D.zrodla[id])}</small>` : "";
  const pole = (id, et, ph = "", span = false) => `<label ${span ? 'style="grid-column: 1 / -1"' : ""}>${et}<input id="dk-${id}" value="${esc(f[id] || "")}" placeholder="${esc(ph)}">${zrd(id)}</label>`;
  return `<div class="krok k-ziel" id="sek-dokumentacja"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>${nr}. Sporządzenie dokumentacji przetargowej</h3>
    <span class="stan">${dk ? odm(dk.pliki.length, "dokument", "dokumenty", "dokumentów") : "do zrobienia"}</span></div><div class="tresc">
    <div class="siatka"><label style="grid-column: 1 / -1">Rodzaj postępowania<select id="dk-tryb">${MZ().tryby_dokumentacji.map(([v, n]) => `<option value="${v}" ${f.tryb === v ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      ${pole("nazwa", "Nazwa zamówienia", PRZ.nazwa, true)}${pole("zamawiajacy", "Zamawiający (nazwa, adres, NIP)", "nazwa, adres, NIP", true)}
      ${pole("znak", "Znak sprawy")}${pole("wartosc", "Wartość szacunkowa netto", "np. z notatki z szacowania")}
      ${pole("termin_realizacji", "Termin realizacji", "np. do 30.06.2027")}${pole("termin_ofert", "Termin składania ofert")}
      ${pole("wadium", "Wadium", "np. 20 000 zł albo brak")}${pole("gwarancja", "Minimalna gwarancja", PRZ.gw)}
      ${pole("kryteria", "Kryteria oceny", PRZ.kryt)}${pole("wynagrodzenie", "Wynagrodzenie", "ryczałtowe / kosztorysowe")}
      ${pole("platnosci", "Płatności", "np. faktury częściowe po odbiorach, 30 dni")}${pole("kary", "Kary umowne", "np. 0,1% za dzień zwłoki, limit 20%")}
      ${pole("zabezpieczenie", "Zabezpieczenie należytego wykonania", "np. 5% ceny")}${pole("platforma", "Sposób składania ofert", "platforma e-Zamówienia / Baza Konkurencyjności / e-mail")}
      ${pole("warunki", "Warunki udziału", PRZ.warunki, true)}
      ${pole("kontakt", "Osoba do kontaktu")}</div>
    <label class="opis" style="display:block;margin:6px 0 4px">${PRZ.zakres}</label>
    <textarea id="dk-zakres" placeholder="${esc(PRZ.zakres_ph)}">${esc(f.zakres || "")}</textarea>${zrd("zakres")}
    ${Object.keys(D.pola || {}).length ? '<p class="opis" style="margin:4px 0">Pola uzupełnione z danych zamówienia (kreator, wgrane dokumenty, kosztorys) – zmiany zapisane tutaj trafią też do kreatora.</p>' : ""}
    <label class="opis" style="display:block;margin:6px 0 4px">Dodatkowe wymagania (opcjonalnie)</label><textarea id="dk-uwagi" style="min-height:50px">${esc(f.uwagi || "")}</textarea>
    <div class="wybor-h">${[["swz", "SWZ / zapytanie ofertowe"], ["opz", "Opis przedmiotu zamówienia"], ["formularz", "Formularz ofertowy"], ["umowa", "Wzór umowy"], ["oswiadczenia", "Oświadczenia i wykazy"]]
      .map(([k, n]) => `<label><input type="checkbox" class="dk-dok" value="${k}" checked> ${n}</label>`).join("")}</div>
    <div class="pasek"><button class="zielony" data-ik="iskra" onclick="sporzadzDokumentacje()">Sporządź dokumentację</button>
      <span class="opis" style="margin:0">Każdy dokument to 2–5 minut pracy AI.</span></div>
    ${dk && dk.pliki.length ? `<div class="pliki-wynik">${dk.pliki.map(n => `<a href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(n)}">${esc(n)}</a>`).join("")}</div>` : ""}
    <div class="ramka-uwaga">Dokumenty to projekty przygotowane z pomocą AI. Przed publikacją sprawdź je – w zamówieniach publicznych zgodnie z ustawą Pzp –
      i uzupełnij pola [UZUPEŁNIJ]. Możesz je potem zweryfikować w module „Sprawdź dokumentację”.</div>
  </div></div>`;
}
function kopiujPytaniaWer() {
  const t = ((PROJEKT.weryfikacja || {}).uwagi || []).filter(u => u.pytanie_do_zamawiajacego && u.status !== "odrzucone").map((u, i) => `${i + 1}. ${u.pytanie_do_zamawiajacego}`).join("\n");
  navigator.clipboard?.writeText("Pytania dotyczące treści dokumentacji:\n" + t).then(() => komunikat("Skopiowano pytania do zamawiającego."), () => prompt("Skopiuj pytania:", t));
}
async function uruchomWeryfikacje() {
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/weryfikacja`, {json: {dodatkowe: $("#wer-dod").value, dokladne: !!$("#wer-dokl")?.checked, tryb: $("#wer-tryb")?.value}})), odswiezProjekt);
}
async function werDecyzja(id, decyzja) {
  const t = document.querySelector(`.wer-nowy[data-id="${id}"]`);
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/weryfikacja/decyzja`, {json: {id, decyzja, nowy: t ? t.value : null}})); odswiezProjekt();
}
async function werWszystkie(decyzja) {
  for (const t of document.querySelectorAll(".wer-nowy")) await api(`/api/projekty/${PROJEKT_ID}/weryfikacja/decyzja`, {json: {id: t.dataset.id, decyzja, nowy: t.value}}).catch(() => null);
  odswiezProjekt();
}
async function werWprowadz() {
  for (const t of document.querySelectorAll(".wer-nowy")) await api(`/api/projekty/${PROJEKT_ID}/weryfikacja/decyzja`, {json: {id: t.dataset.id, nowy: t.value}}).catch(() => null);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/weryfikacja/wprowadz`, {method: "POST"})); if (!r) return;
  komunikat(`Wprowadzono zmiany: ${r.wynik.reduce((a, x) => a + x.wprowadzone, 0)}${r.reczne.length ? `, do ręcznego wprowadzenia: ${r.reczne.length}` : ""}.`); odswiezProjekt();
}
async function statusUwagi(id, status) { await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/weryfikacja/uwaga`, {json: {id, status}})); odswiezProjekt(); }
async function sporzadzDokumentacje() {
  const pola = {}; ["tryb", "nazwa", "zamawiajacy", "znak", "wartosc", "termin_realizacji", "termin_ofert", "wadium", "gwarancja", "kryteria", "wynagrodzenie",
    "platnosci", "kary", "zabezpieczenie", "platforma", "warunki", "kontakt", "zakres", "uwagi"].forEach(k => { const e = $("#dk-" + k); if (e) pola[k] = e.value; });
  const dokumenty = [...document.querySelectorAll(".dk-dok:checked")].map(c => c.value);
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/dokumentacja`, {json: {pola, dokumenty}})), odswiezProjekt);
}
function panelDostepu(p) {
  const nazwaRoli = {admin: "administrator", uzytkownik: "pracownik biurowy", podglad: "podgląd"};
  const mojProjekt = p.wlasciciel === JA.login;
  // projekt użytkownika: przekazanie tylko administratorowi (lub z powrotem), bez udostępniania innym użytkownikom
  const wlasciciele = mojProjekt ? [JA.login, ...UZYTKOWNICY.map(u => u.login)] : [p.wlasciciel, JA.login];
  const inni = mojProjekt ? UZYTKOWNICY.filter(u => u.login !== p.wlasciciel) : [];
  return `<details class="dostep"><summary>${ik("ludzie")} Dostęp: właściciel <b>${esc(p.wlasciciel)}</b>${p.dostep.length ? ` · udostępniono: ${esc(p.dostep.join(", "))}` : " · widzi go tylko właściciel i administrator"}</summary>
    <div class="siatka" style="margin-top:10px"><label>Właściciel projektu<select id="dst-wl">${wlasciciele.map(l => `<option ${l === p.wlasciciel ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></label></div>
    ${mojProjekt ? (inni.length ? `<div class="opis" style="margin:4px 0">Udostępnij ten projekt (Twój) użytkownikom:</div><div class="wybor-h">${inni.map(u =>
      `<label><input type="checkbox" class="dst-u" value="${esc(u.login)}" ${p.dostep.includes(u.login) ? "checked" : ""}> ${esc(u.login)} <small class="opis" style="margin:0">(${nazwaRoli[u.rola] || u.rola})</small></label>`).join("")}</div>`
      : '<p class="opis">Nie ma innych użytkowników.</p>')
      : `<p class="opis">Projekt użytkownika <b>${esc(p.wlasciciel)}</b> widzi tylko on i Ty. Nie można go udostępnić innym użytkownikom ani przekazać innemu użytkownikowi – możesz go jedynie przejąć (właściciel: ${esc(JA.login)}).</p>`}
    <button class="glowny maly" data-ik="zapisz" onclick="zapiszDostep()">Zapisz dostęp</button></details>`;
}
async function zapiszDostep() {
  const d = {wlasciciel: $("#dst-wl").value, dostep: [...document.querySelectorAll(".dst-u:checked")].map(c => c.value)};
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/dostep`, {json: d}))) { komunikat("Zapisano dostęp do projektu."); otworzProjekt(PROJEKT_ID); ladujProjekty(); }
}
const odm = (n, f1, f2, f5) => `${n} ${n === 1 ? f1 : [2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100) ? f2 : f5}`;
// ---------- asystent dokumentów (czat)
// pytania podpowiadane w asystencie dokumentów – zależnie od rodzaju projektu (dotacja to nie przetarg: bez wadium i kar umownych)
const PYTANIA_DOT = ["Kto może złożyć wniosek i jakie są warunki dostępu?", "Jakie koszty są kwalifikowalne, a jakie nie?",
  "Jaki jest poziom dofinansowania i limity kwot?", "Za co można dostać punkty w ocenie?", "Do kiedy i jak złożyć wniosek, jakie załączniki?",
  "Jakie są obowiązki po otrzymaniu dotacji (trwałość, rozliczenie)?"];
const PYTANIA_ZQ = ["Jakie wydatki w projekcie wymagają zasady konkurencyjności?", "Jakie są terminy realizacji projektu?", "Jakie kryteria wyboru wykonawcy są dopuszczalne?"];
const PYTANIA = ["Jakie są kary umowne?", "Jakie jest wadium i do kiedy składamy ofertę?", "Jakie są warunki udziału (doświadczenie, osoby)?",
  "Jaki jest termin realizacji i wymagana gwarancja?", "Czy wynagrodzenie jest ryczałtowe?"];
function panelCzatu(p) {
  const h = p.czat || [];
  return `<div class="krok"><div class="tytul"><span class="nr">${ik("czat")}</span><h3>Asystent dokumentów</h3>
    <span class="stan">${h.length ? odm(h.length, "pytanie", "pytania", "pytań") : "zapytaj o dokumenty"}</span></div><div class="tresc">
    <p class="opis">Zadaj pytanie o dokumenty z kroku 1 – AI odpowie na ich podstawie i pokaże cytaty z nazwą pliku i stroną.</p>
    <div class="czat">${h.map(x => `<div class="czat-p">${ik("ludzie")} ${esc(x.pyt)} <small class="opis" style="margin:0">${esc(x.kto || "")} · ${esc(x.czas)}</small></div>
      <div class="czat-o">${esc(x.odp).replace(/\n/g, "<br>").replace(/\[(\d+)\]/g, "<sup>[$1]</sup>")}
      ${x.cytaty && x.cytaty.length ? `<details class="cytaty"><summary>Cytaty z dokumentów (${x.cytaty.length})</summary>${x.cytaty.map((c, i) =>
        `<div class="cytat"><b>[${i + 1}] ${esc(c.plik)}${c.strona ? ", str. " + c.strona : ""}</b><br>„${esc(c.tekst)}”</div>`).join("")}</details>` : ""}</div>`).join("")}</div>
    <div class="podpowiedzi">${(["wniosek_dot", "dotacja"].includes(p.typ) ? PYTANIA_DOT : ["zapytanie"].includes(p.typ) ? PYTANIA_ZQ : PYTANIA).map(q => `<button type="button" class="maly" onclick="$('#czat-pyt').value=this.textContent">${q}</button>`).join("")}</div>
    <div class="pasek" style="margin-top:8px"><input id="czat-pyt" placeholder="Wpisz pytanie o dokumenty…" style="flex:1;min-width:260px"
      onkeydown="if (event.key === 'Enter') zapytajCzat()">
      <button class="glowny" data-ik="czat" onclick="zapytajCzat()">Zapytaj</button>
      ${h.length ? `<button class="maly" data-ik="kosz" onclick="wyczyscCzat()">Wyczyść rozmowę</button>` : ""}</div>
  </div></div>`;
}
async function zapytajCzat() {
  const pyt = $("#czat-pyt").value.trim(); if (!pyt) return komunikat("Wpisz pytanie.", true);
  const z = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/czat`, {json: {pytanie: pyt}})); if (!z) return;
  $("#czat-pyt").value = ""; komunikat("Asystent czyta dokumenty…");
  sledz(z, odswiezProjekt);
}
async function wyczyscCzat() { if (confirm("Wyczyścić rozmowę z asystentem?")) { await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/czat/wyczysc`, {json: {}})); odswiezProjekt(); } }

// ---------- sprawdź kosztorys
let POKAZ_ZALATWIONE = false;
function panelKontroli(p) {
  const k = p.kontrola, A = (k && k.alerty) || [];
  const widoczne = A.filter(a => POKAZ_ZALATWIONE || a.status === "nowy");
  const nazwaPola = {cena: "cena jedn.", ilosc: "ilość", jm: "j.m.", opis: "opis"};
  return `<div class="kontrola"><h3>${ik("alarm")} Sprawdź kosztorys</h3>
    <p class="opis">Kontrola techniczna (brak cen, zerowe ilości, rozbieżne ceny tych samych robót) i analiza AI (nierealne ceny, ilości,
      jednostki, brakujące roboty). Nic nie zmienia się bez Twojej decyzji.</p>
    <div class="pasek"><button class="zolty" data-ik="iskra" onclick="sprawdzKosztorys()">${k ? "Sprawdź ponownie" : "Sprawdź kosztorys"}</button>
      ${k ? `<span class="opis" style="margin:0">Ostatnio: ${esc(k.data)} · ${A.filter(a => a.status === "nowy").length} do rozpatrzenia,
        ${A.filter(a => a.status === "zastosowany").length} poprawionych, ${A.filter(a => a.status === "odstepstwo").length} odstępstw</span>
        <label style="display:flex;gap:6px;align-items:center"><input type="checkbox" ${POKAZ_ZALATWIONE ? "checked" : ""} onchange="POKAZ_ZALATWIONE=this.checked; rysujProjekt()"> pokaż rozpatrzone</label>` : ""}</div>
    ${widoczne.map(a => `<div class="alert-k ${a.typ} ${a.status}">
      <div class="alert-gora"><span class="znacznik ${a.typ === "ostrzezenie" ? "z-czerwony" : "z-do-analizy"}">${a.typ === "ostrzezenie" ? "ostrzeżenie" : "optymalizacja"}</span>
        <b>${esc(a.kategoria)}</b> ${a.lp ? `· poz. ${a.lp}` : "· cały kosztorys"} <small class="opis" style="margin:0">(${esc(a.zrodlo)})</small>
        ${a.status !== "nowy" ? `<span class="znacznik ${a.status === "zastosowany" ? "z-startujemy" : "z-odpuszczamy"}">${a.status === "zastosowany" ? "poprawione" : "świadome odstępstwo"}</span>` : ""}</div>
      ${a.pozycja ? `<div class="opis" style="margin:4px 0">${esc(a.pozycja.opis).slice(0, 160)} – ${liczba(a.pozycja.ilosc, 3)} ${esc(a.pozycja.jm)} × ${zl(a.pozycja.cena)} = ${zl(a.pozycja.wartosc)}</div>` : ""}
      <div>${esc(a.opis)}</div>
      ${a.sugestia ? `<div class="sugestia">Sugestia: <b>${nazwaPola[a.sugestia.pole] || a.sugestia.pole} → ${a.sugestia.pole === "cena" ? zl(a.sugestia.wartosc) : esc(a.sugestia.wartosc)}</b></div>` : ""}
      ${a.status === "nowy" ? `<div class="pasek" style="margin:8px 0 0">
        ${a.sugestia && a.lp ? `<button class="zielony maly" data-ik="iskra" onclick="alertKontroli('${a.id}','zastosuj')">Zastosuj sugestię</button>` : ""}
        ${a.lp ? `<button class="maly" data-ik="przelacz" onclick="this.parentElement.nextElementSibling.classList.toggle('ukryj')">Popraw ręcznie</button>` : ""}
        <button class="maly" data-ik="flaga" onclick="alertKontroli('${a.id}','odstepstwo')">Świadome odstępstwo</button></div>
        ${a.lp && a.pozycja ? `<div class="ukryj siatka" style="margin-top:8px">
          <label>Ilość<input id="ak-il-${a.id}" value="${esc(a.pozycja.ilosc)}"></label><label>Cena jedn. netto<input id="ak-c-${a.id}" value="${esc(a.pozycja.cena)}"></label>
          <label>j.m.<input id="ak-jm-${a.id}" value="${esc(a.pozycja.jm)}"></label>
          <label>&nbsp;<button class="glowny maly" data-ik="zapisz" onclick="alertKontroli('${a.id}','zmien')">Zapisz poprawkę</button></label></div>` : ""}`
      : `<div class="pasek" style="margin:6px 0 0"><button class="maly" onclick="alertKontroli('${a.id}','przywroc')">Przywróć</button></div>`}
    </div>`).join("") || (k ? '<p class="zielone"><b>Brak uwag do rozpatrzenia.</b></p>' : "")}
  </div>`;
}
async function sprawdzKosztorys() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kontrola`, {json: {ai: true}})), odswiezProjekt); }
async function alertKontroli(id, akcja) {
  const d = {id, akcja};
  if (akcja === "zmien") d.zmiany = {ilosc: $(`#ak-il-${id}`).value, cena: $(`#ak-c-${id}`).value, jm: $(`#ak-jm-${id}`).value};
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kontrola/alert`, {json: d})); if (!w) return;
  if (w.oferta) komunikat(`Poprawiono pozycję. Nowa cena: ${zl(w.oferta.netto)} netto.`);
  otworzProjekt(PROJEKT_ID);
}

function krokUmowy(p) {
  const f = p.umowa_formularz || {}, u = p.umowa, o = p.oferta;
  const pole = (id, et, typ = "text", extra = "") => `<label>${et}<input id="um-${id}" type="${typ}" value="${esc(f[id] ?? "")}" ${extra}></label>`;
  const wyb = (id, et, opcje) => `<label>${et}<select id="um-${id}">${opcje.map(([v, n]) => `<option value="${v}" ${String(f[id]) === v ? "selected" : ""}>${n}</option>`).join("")}</select></label>`;
  return `<div class="krok k-czer"><div class="tytul"><span class="nr">${ik("protokol")}</span><h3>3. Umowa o roboty budowlane</h3>
    <span class="stan">${u ? "umowa gotowa" : "do zrobienia"}</span></div><div class="tresc">
    ${!o ? '<p class="pusto">Najpierw przygotuj ofertę i kosztorys (krok 2) – umowa powstaje na ich podstawie: zakres z działów kosztorysu, wynagrodzenie, VAT i gwarancja.</p>' : `
    <p class="opis">Dane z oferty i kosztorysu są już wpisane. Uzupełnij dane zamawiającego i terminy, sprawdź warunki i kliknij „Przygotuj umowę”.
      Załącznikami do umowy są kosztorys ofertowy i oferta${p.status_projektu ? "" : ""}.</p>
    <h3 style="margin:10px 0 6px">Zamawiający</h3>
    <div class="pasek"><select id="um-klient" onchange="klientDoUmowy(this.value)"><option value="">– wybierz z bazy klientów –</option></select>
      <button type="button" class="zolty" data-ik="szukaj" onclick="nipDoUmowy()">Pobierz dane po NIP</button>
      <span class="opis" style="margin:0">wpisz NIP w polu „NIP (firma) lub PESEL” i kliknij</span></div>
    <div class="siatka">${wyb("zam_typ", "Rodzaj", [["firma", "firma / wspólnota / instytucja"], ["konsument", "osoba prywatna (konsument)"]])}
      ${pole("zam_nazwa", "Nazwa lub imię i nazwisko")}${pole("zam_adres", "Adres")}
      ${pole("zam_id", "NIP (firma) lub PESEL (osoba)")}${pole("zam_reprezentant", "Reprezentowany przez (np. zarząd wspólnoty)")}
      ${pole("przedstawiciel_zam", "Przedstawiciel na budowie (opcjonalnie)")}</div>
    <h3 style="margin:10px 0 6px">Umowa i przedmiot</h3>
    <div class="siatka">${pole("numer", "Numer umowy")}${pole("data", "Data zawarcia", "date")}${pole("miejsce", "Miejsce zawarcia", "text", 'placeholder="np. Świdnica"')}
      ${pole("start", "Rozpoczęcie robót", "date")}${pole("koniec", "Zakończenie robót", "date")}</div>
    <div class="siatka">${pole("przedmiot", "Przedmiot umowy (zakres)")}${pole("obiekt", "Adres obiektu / nieruchomości")}</div>
    <h3 style="margin:10px 0 6px">Wynagrodzenie i płatności</h3>
    <div class="siatka">${wyb("wynagrodzenie", "Rodzaj wynagrodzenia", [["ryczalt", "ryczałtowe"], ["kosztorys", "kosztorysowe (wg obmiaru)"]])}
      ${pole("netto", "Wynagrodzenie netto [zł]")}${pole("vat", "Stawka VAT (np. 0.23 lub 0.08) – ustal z zamawiającym / z warunków przetargu")}
      ${wyb("platnosci", "Płatności", [["czesciowe", "częściowe po odbiorach etapów + końcowa"], ["jednorazowa", "jednorazowo po odbiorze końcowym"]])}
      ${pole("termin_platnosci", "Termin płatności [dni]", "number", 'min="1"')}${pole("zaliczka", "Zaliczka [% brutto] (0 = brak)", "number", 'min="0" step="1"')}
      ${wyb("materialy", "Materiały", [["wykonawcy", "zapewnia Wykonawca"], ["zamawiajacego", "zapewnia Zamawiający"]])}</div>
    <h3 style="margin:10px 0 6px">Gwarancja, kary i pozostałe</h3>
    <div class="siatka">${pole("gwarancja", "Gwarancja [miesiące]", "number", 'min="0"')}
      ${pole("kara_zwloka", "Kara za zwłokę [% brutto / dzień]", "number", 'step="0.01"')}${pole("kara_wady", "Kara za zwłokę w usunięciu wad [% / dzień]", "number", 'step="0.01"')}
      ${pole("kara_odstapienie", "Kara za odstąpienie [%]", "number", 'step="1"')}${pole("kara_limit", "Limit kar [% wynagrodzenia]", "number", 'step="1"')}
      ${pole("oc", "Polisa OC Wykonawcy (suma, opcjonalnie)", "text", 'placeholder="np. 500 000 zł"')}${pole("kierownik", "Kierownik budowy / robót (opcjonalnie)")}</div>
    <label class="opis" style="display:block;margin:6px 0 4px">Postanowienia dodatkowe (każde w nowej linii – trafią do osobnego paragrafu)</label>
    <textarea id="um-dodatkowe">${esc(f.dodatkowe || "")}</textarea>
    <div class="pasek" style="margin-top:10px"><button class="zielony" data-ik="protokol" onclick="generujUmowe()">${u ? "Przygotuj umowę ponownie" : "Przygotuj umowę"}</button>
      ${u ? `<span class="opis" style="margin:0">Ostatnio: ${esc(u.utworzono)} · ${zl(u.brutto)} brutto</span>` : ""}</div>
    ${u ? `<div class="pliki-wynik"><a href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(u.plik)}">${esc(u.plik)}</a></div>` : ""}
    <div class="ramka-uwaga">Umowa to wzór oparty na przepisach Kodeksu cywilnego o umowie o roboty budowlane. Przed podpisaniem przeczytaj ją w całości
      i uzupełnij żółte pola; przy dużych kontraktach lub nietypowych warunkach warto skonsultować ją z prawnikiem.</div>`}
  </div></div>`;
}
async function nipDoUmowy() {
  const d = await pobierzNip($("#um-zam_id").value); if (!d) return;
  $("#um-zam_typ").value = "firma"; $("#um-zam_nazwa").value = d.nazwa; $("#um-zam_adres").value = d.adres; $("#um-zam_id").value = d.nip;
  if (d.reprezentanci && d.reprezentanci.length && !$("#um-zam_reprezentant").value) $("#um-zam_reprezentant").value = d.reprezentanci.join(", ");
}
function klientDoUmowy(id) {
  const k = KLIENCI.find(x => x.id === id); if (!k) return;
  $("#um-zam_typ").value = "firma"; $("#um-zam_nazwa").value = k.nazwa || ""; $("#um-zam_adres").value = k.adres || "";
  $("#um-zam_id").value = k.nip || ""; if (k.reprezentant) $("#um-zam_reprezentant").value = k.reprezentant;
}
async function wypelnijListeKlientow() {
  const s = $("#um-klient"); if (!s) return;
  KLIENCI = await api("/api/klienci").catch(() => KLIENCI) || [];
  s.innerHTML = '<option value="">– wybierz z bazy klientów –</option>' + KLIENCI.map(k => `<option value="${k.id}">${esc(k.nazwa)}${k.nip ? " · " + esc(k.nip) : ""}</option>`).join("");
}
async function generujUmowe() {
  const pola = ["zam_typ", "zam_nazwa", "zam_adres", "zam_id", "zam_reprezentant", "przedstawiciel_zam", "numer", "data", "miejsce", "start", "koniec",
    "przedmiot", "obiekt", "wynagrodzenie", "netto", "vat", "platnosci", "termin_platnosci", "zaliczka", "materialy", "gwarancja",
    "kara_zwloka", "kara_wady", "kara_odstapienie", "kara_limit", "oc", "kierownik", "dodatkowe"];
  const d = {}; pola.forEach(k => { const el = $("#um-" + k); if (el) d[k] = el.value; });
  if (!d.zam_nazwa.trim()) return komunikat("Wpisz nazwę lub imię i nazwisko zamawiającego.", true);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/umowa`, {json: d})); if (!w) return;
  komunikat(`Umowa gotowa: ${zl(w.brutto)} brutto.`); location.href = w.url; otworzProjekt(PROJEKT_ID);
}
async function zmienNazwe(n) { await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/nazwa`, {json: {nazwa: n}})); ladujProjekty(); }
async function usunProjekt() {
  if (!confirm("Przenieść projekt do Archiwum? Zniknie z listy, ale w każdej chwili przywrócisz go w zakładce Archiwum.")) return;
  await bezpiecznie(() => api("/api/projekty/" + PROJEKT_ID, {method: "DELETE"}));
  PROJEKT_ID = null; $("#projekt").innerHTML = '<p class="pusto">Projekt przeniesiony do Archiwum.</p>'; ladujProjekty();
}
async function wgrajPliki(files) {
  if (!files || !files.length) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  komunikat(`Wgrywam ${files.length} plik(ów)…`);
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pliki`, {method: "POST", body: fd}));
  otworzProjekt(PROJEKT_ID);
}
const zaznaczonePliki = () => [...document.querySelectorAll(".pl:checked")].map(c => c.value);
async function przelaczPliki() { const s = zaznaczonePliki(); if (!s.length) return komunikat("Zaznacz pliki na liście.");
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pliki/przelacz`, {json: {sciezki: s}})); otworzProjekt(PROJEKT_ID); }
async function usunPliki(wszystkie) {
  const s = wszystkie ? null : zaznaczonePliki();
  if (!wszystkie && !s.length) return komunikat("Zaznacz pliki na liście.");
  if (!confirm(wszystkie ? "Usunąć WSZYSTKIE dokumenty z projektu?" : `Usunąć ${s.length} plik(ów)?`)) return;
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pliki/usun`, {json: {sciezki: s}})); otworzProjekt(PROJEKT_ID);
}
async function wgrajWynik(inp, rodzaj) {
  const fd = new FormData(); fd.append("plik", inp.files[0]); fd.append("rodzaj", rodzaj);
  await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wgraj-wynik`, {method: "POST", body: fd}));
  komunikat("Wgrano plik."); otworzProjekt(PROJEKT_ID);
}
const odswiezProjekt = () => { if (TRYBY[WIDOK] && PROJEKT_ID) otworzProjekt(PROJEKT_ID); };
async function uwzglednijWszystkie() {
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pliki/uwzglednij-wszystkie`, {json: {}}))) { komunikat("Wszystkie dokumenty są uwzględnione."); odswiezProjekt(); }
}
async function pobierzBK() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pobierz-dokumenty`, {json: {}})), odswiezProjekt); }
const OPCJE_VAT = [["auto", "z warunków przetargu (AI odczyta z dokumentów)"], ["0.23", "23%"], ["0.08", "8% – budownictwo mieszkaniowe (lokale do 150 m², domy do 300 m²)"], ["0.05", "5%"], ["0", "0% / zwolnione"]];
const selectVat = (id, wart) => `<select id="${id}">${OPCJE_VAT.map(([v, n]) => `<option value="${v}" ${String(wart) === v ? "selected" : ""}>${n}</option>`).join("")}</select>`;
async function notatkaSzacowania() {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/notatka-szacowania`, {json: {}})); if (!r) return;
  if ($("#tryb-szac")) $("#tryb-szac").innerHTML = `Wartość ${r.tryb.euro.toLocaleString("pl-PL")} € → <b>${esc(r.tryb.opis)}</b>`;
  location.href = r.url;
}
async function kosztorysPusty() {
  if (!PROJEKT.oferta && !confirm("Projekt nie ma jeszcze kosztorysu. Najpierw AI przygotuje z dokumentów pozycje i ilości (kilka minut), a potem powstanie pusty formularz / kosztorys dla wykonawców. Kontynuować?")) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kosztorys-pusty`, {json: {}})); if (!w) return;
  if (w.zadanie) { komunikat("Przygotowuję kosztorys z projektu, a potem wersję do wyceny…"); sledz(w.zadanie, odswiezProjekt); }
  else { komunikat("Gotowy pusty formularz dla wykonawców – do dołączenia do SWZ / zapytania."); location.href = w.url; odswiezProjekt(); }
}
function sekcjaOfertyKlienta(p) {
  const ok = p.oferta_klienta || {}, pl = ok.pola || {}, uf = p.umowa_formularz || {};
  const ma = !!p.oferta;
  const pole = (k, et, ph, dom) => `<label>${et}<input id="ok-${k}" value="${esc(pl[k] ?? dom ?? "")}" placeholder="${esc(ph || "")}"></label>`;
  return `<div class="etap-b" id="sek-oferta-klienta"><h4 class="etap-kroku"><span>B</span> Oferta dla klienta – na podstawie kosztorysu
      <small class="znacznik ${ok.plik ? "z-startujemy" : "z-odpuszczamy"}">${ok.plik ? "gotowa" : ma ? "do przygotowania" : "najpierw kosztorys (A)"}</small></h4>
    <p class="opis">Oferta powstaje <b>na podstawie kosztorysu z punktu A</b> – przygotowanego przez program albo wgranego własnego. Zawiera zakres robót
      (działy z wartościami), cenę netto, VAT i brutto słownie oraz warunki; kosztorys dla klienta jest załącznikiem. Po zmianie kosztorysu lub ceny
      oferta aktualizuje się sama.</p>
    ${ma ? `<div class="kwoty kafle-przetargu" style="margin-top:0"><div><span>Kosztorys netto</span><b>${zl(p.oferta.netto)}</b></div>
      <div><span>Brutto</span><b>${zl(p.oferta.brutto)}</b></div></div>
    <div class="siatka">${pole("klient_nazwa", "Klient (nazwa / imię i nazwisko)", "np. Wspólnota Mieszkaniowa Długa 5", uf.zam_nazwa)}
      ${pole("klient_adres", "Adres klienta", "", uf.zam_adres)}${pole("klient_osoba", "Osoba kontaktowa", "")}
      ${pole("termin_realizacji", "Termin realizacji", "np. do 30 dni od podpisania umowy")}${pole("gwarancja", "Gwarancja", "np. 36 miesięcy")}
      ${pole("platnosc", "Płatność", "np. przelew 14 dni po odbiorze")}${pole("waznosc", "Ważność oferty", "np. 30 dni")}
      ${pole("miejsce", "Miejscowość", "np. Świdnica")}
      <label style="grid-column: 1 / -1">Uwagi (opcjonalnie)<input id="ok-uwagi" value="${esc(pl.uwagi || "")}" placeholder="np. cena nie obejmuje kontenera na gruz"></label></div>
    <div class="pasek"><button class="zielony" data-ik="dokument" onclick="ofertaKlienta()">${ok.plik ? "Zaktualizuj ofertę" : "Przygotuj ofertę na podstawie kosztorysu"}</button>
      ${ok.utworzono ? `<span class="opis" style="margin:0">ostatnio: ${esc(ok.utworzono)}</span>` : ""}</div>
    ${ok.plik || p.kosztorys_klienta ? `<div class="pliki-ik">${plikIk(p.id, ok.plik, "Oferta dla klienta")}${plikIk(p.id, p.kosztorys_klienta, "Kosztorys dla klienta")}</div>` : ""}`
      : '<p class="pusto">Najpierw przygotuj kosztorys w programie albo wgraj własny kosztorys (punkt A).</p>'}
  </div>`;
}
function sekcjaOfertyPrzetargowej(p) {
  const o = p.oferta, gotowa = (p.pliki_oferty || []).some(x => /_formularze/.test(x)) || p.oferta_przygotowana;
  const form = (p.pliki_oferty || []).find(x => /_formularze/.test(x)), an = (p.pliki_oferty || []).find(x => /^Analiza_/.test(x));
  return `<div class="etap-b"><h4 class="etap-kroku"><span>B</span> Oferta przetargowa – na podstawie kosztorysu
      <small class="znacznik ${gotowa ? "z-startujemy" : "z-odpuszczamy"}">${gotowa ? "gotowa" : o ? "do przygotowania" : "najpierw kosztorys (A)"}</small></h4>
    <p class="opis">Formularz ofertowy z ceną z kosztorysu (netto, VAT, brutto słownie), oświadczenia i analiza przetargu. Najpierw sprawdź kosztorys
      i ewentualnie dopasuj cenę powyżej, potem przygotuj ofertę. Po zmianie kosztorysu, ceny albo VAT oferta przelicza się sama.</p>
    ${o ? `<div class="pasek"><label title="Okres gwarancji to decyzja handlowa – wpływa na punkty w kryterium i na koszt (rękojmia, serwis). Puste = propozycja z analizy przetargu.">Gwarancja w ofercie [mies.]
          <input id="of-gwar" type="number" min="1" max="240" style="width:80px" value="${esc(String(p.gwarancja_oferty || ""))}" placeholder="${esc(String((o.gwarancja_ai || "")))}"></label>
        ${o.kryteria ? `<small class="opis" style="margin:0;max-width:420px">Kryteria: ${esc(String(o.kryteria).slice(0, 220))}</small>` : ""}</div>
      <div class="pasek"><button class="zielony" data-ik="dokument" onclick="ofertaZKosztorysu()">${gotowa ? "Przygotuj ofertę ponownie" : "Przygotuj ofertę na podstawie kosztorysu"}</button>
        <span class="opis" style="margin:0">Cena oferty: <b>${zl(o.brutto)}</b> brutto (${zl(o.netto)} netto)</span></div>
      ${gotowa ? `<div class="pliki-ik">${plikIk(p.id, form, "Formularze oferty")}${plikIk(p.id, p.kosztorys_klienta, "Kosztorys dla zamawiającego")}${plikIk(p.id, an, "Analiza przetargu")}</div>` : ""}`
      : '<p class="pusto">Najpierw przygotuj kosztorys w programie albo wgraj własny kosztorys (punkt A).</p>'}
  </div>`;
}
// ---------- rozliczanie dotacji UE / KPO
let DOT = null;
const DOT_W = () => (PROJEKT && PROJEKT.typ === "wniosek_dot");
const DOT_URL = () => `/api/projekty/${PROJEKT_ID}/${DOT_W() ? "wniosek-dot" : "dotacja"}`;
async function ladujDotacje() { DOT = await api(`${DOT_URL()}`).catch(() => null); if (DOT) { rysujDotacje(); ladujPlan(); } }
function rysujDotacje() {
  const d = DOT, w = d.wymagania, dn = d.dane || {}, el = $("#dotacja"); if (!el) return;
  const sp = d.sprawdzenie, kp = d.komplet;
  const stKl = s => /^ok/.test(s) ? "z-startujemy" : /popraw|brak/.test(s) ? "z-czerwony" : /przygotowany|wgrany/.test(s) ? "z-do-analizy" : "z-odpuszczamy";
  const kat = {}; (d.lista || []).forEach(x => (kat[x.kategoria] = kat[x.kategoria] || []).push(x));
  const WN = DOT_W(), nab = d.nabor || {};
  el.innerHTML = WN ? `
  <div class="krok k-ziel"><div class="tytul"><span class="nr">${ik("iskra")}</span><h3>2. Wymagania naboru i dane projektu</h3>
    <span class="stan">${w ? (w.dokumenty || []).length + " dokumentów wniosku" : "do zrobienia"}</span></div><div class="tresc">
    ${nab.nazwa ? `<div class="karta" style="margin:0 0 12px;padding:12px 16px"><b>${esc(nab.nazwa)}</b> <span class="znacznik z-do-analizy">${esc(nab.status || "")}</span><br>
      <span class="opis" style="margin:0">${esc([nab.program, nab.instytucja, nab.poziom_dofinansowania, nab.kwota, nab.nabor_do ? "nabór do " + nab.nabor_do : ""].filter(Boolean).join(" · "))}</span>
      ${nab.link ? `<br><a href="${esc(nab.link)}" target="_blank" rel="noopener">Strona naboru ↗</a>` : ""}</div>` : ""}
    <p class="opis">Dane wnioskodawcy program bierze z <b>Profilu firmy</b> (${esc((d.wnioskodawca || {}).firma_nazwa || "uzupełnij")}). Opisz projekt – na tej podstawie program wypełni wniosek.</p>
    <div class="siatka"><label style="grid-column: 1 / -1">Opis projektu (co, gdzie, po co, efekty)<textarea id="wd-opis" style="min-height:90px">${esc(dn.opis_projektu || "")}</textarea></label>
      <label>Koszt całkowity [zł]<input id="wd-koszt" value="${esc(dn.koszt_calkowity || "")}"></label>
      <label>Wnioskowana kwota [zł]<input id="wd-kwota" value="${esc(dn.kwota_wnioskowana || "")}"></label>
      <label>Okres realizacji<input id="wd-okres" value="${esc(dn.okres_realizacji || "")}" placeholder="np. 03.2027 – 12.2027"></label>
      <label>Lokalizacja<input id="wd-lok" value="${esc(dn.lokalizacja || "")}"></label></div>
    <div class="pasek"><button class="zielony" data-ik="iskra" onclick="analizaDotacji()">${w ? "Ustal wymagania ponownie" : "Ustal wymagania wniosku (AI)"}</button>
      <span class="opis" style="margin:0">Program czyta regulamin i wzór wniosku z punktu 1: kryteria, koszty kwalifikowalne, wymagane dokumenty.</span></div>
    ${w ? `<div class="kwoty kafle-przetargu"><div><span>Program</span><b style="font-size:14px">${esc(w.program || "–")}</b></div>
      <div><span>Termin składania</span><b style="font-size:14px">${esc(w.termin_skladania || nab.nabor_do || "–")}</b></div>
      <div><span>Intensywność</span><b style="font-size:14px">${esc(w.intensywnosc || nab.poziom_dofinansowania || "–")}</b></div>
      <div><span>System</span><b style="font-size:14px">${esc(w.system || "–")}</b></div></div>
      ${(w.kryteria_dostepu || []).length ? `<h4 class="grupa-analizy">Kryteria dostępu</h4><ul class="lista">${w.kryteria_dostepu.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
      ${(w.kryteria_oceny || []).length ? `<h4 class="grupa-analizy">Kryteria oceny – gdzie zdobyć punkty</h4><div class="tabela-okno"><table class="tabela"><tr><th>Kryterium</th><th>Punkty</th><th>Jak spełnić</th></tr>
        ${w.kryteria_oceny.map(x => `<tr><td><b>${esc(x.nazwa)}</b></td><td>${esc(x.punkty || "")}</td><td>${esc(x.jak_spelnic || "")}</td></tr>`).join("")}</table></div>` : ""}
      ${(w.koszty_kwalifikowalne || []).length ? `<h4 class="grupa-analizy">Koszty kwalifikowalne</h4><ul class="lista">${w.koszty_kwalifikowalne.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
      ${(w.ryzyka || []).length ? `<div class="ramka-uwaga"><b>Najczęstsze błędy we wnioskach:</b><ul class="lista">${w.ryzyka.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}` : ""}
  </div></div><div id="plan-projektu" class="kroki-przezr"></div>` + czescDokumentow() : `
  <div class="krok k-ziel"><div class="tytul"><span class="nr">${ik("iskra")}</span><h3>2. Dokumenty potrzebne do rozliczenia</h3>
    <span class="stan">${w ? (w.dokumenty || []).length + " rodzajów dokumentów" : "do zrobienia"}</span></div><div class="tresc">
    <div class="siatka"><label>Program<select id="dt-program">${d.programy.map(x => `<option ${x === dn.program ? "selected" : ""}>${esc(x)}</option>`).join("")}</select></label>
      <label>Nr umowy<input id="dt-nr" value="${esc(dn.nr_umowy || "")}" placeholder="np. KPOD.01.03-IW.01-0123/24"></label>
      <label>Kwota dofinansowania [zł]<input id="dt-kwota" value="${esc(dn.kwota || "")}"></label>
      <label>Beneficjent<input id="dt-ben" value="${esc(dn.beneficjent || "")}"></label></div>
    <div class="pasek"><button class="zielony" data-ik="iskra" onclick="analizaDotacji()">${w ? "Przeanalizuj ponownie" : "Wskaż dokumenty potrzebne do rozliczenia (AI)"}</button>
      <span class="opis" style="margin:0">Program czyta dokumenty z punktu 1 i ustala etapy, wskaźniki, terminy i wymagane dokumenty.</span></div>
    ${w ? `<div class="kwoty kafle-przetargu"><div><span>Program</span><b style="font-size:14px">${esc(w.program || "–")}</b></div><div><span>Umowa</span><b style="font-size:14px">${esc(w.nr_umowy || "–")}</b></div>
      <div><span>Dofinansowanie</span><b>${w.kwota_dofinansowania ? zl(w.kwota_dofinansowania) : "–"}</b></div>
      <div><span>Okres kwalifikowalności</span><b style="font-size:14px">${esc(((w.okres_kwalifikowalnosci || {}).od || "?") + " – " + ((w.okres_kwalifikowalnosci || {}).do || "?"))}</b></div></div>
      ${(w.etapy || []).length ? `<h4 class="grupa-analizy">Etapy / transze</h4><div class="tabela-okno"><table class="tabela"><tr><th>Etap</th><th>Termin</th><th>Kwota</th><th>Zakres</th></tr>
        ${w.etapy.map(e => `<tr><td><b>${esc(e.nazwa)}</b></td><td>${esc(e.termin || "")}</td><td class="liczba">${e.kwota ? zl(e.kwota) : "–"}</td><td>${esc(e.zakres || "")}</td></tr>`).join("")}</table></div>` : ""}
      ${(w.wskazniki || []).length ? `<h4 class="grupa-analizy">Wskaźniki</h4><ul class="lista">${w.wskazniki.map(x => `<li><b>${esc(x.nazwa)}</b>: ${esc(x.wartosc_docelowa || "")}${x.sposob_pomiaru ? " – " + esc(x.sposob_pomiaru) : ""}</li>`).join("")}</ul>` : ""}
      ${(w.ryzyka || []).length ? `<div class="ramka-uwaga"><b>Na co uważać:</b><ul class="lista">${w.ryzyka.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}` : ""}
  </div></div><div id="plan-projektu" class="kroki-przezr"></div>` + czescDokumentow() + '<div id="dot-zamowienia" class="kroki-przezr"></div>';
  wstawIkony(el);
  kartaZamowienDotacji();
}
function czescDokumentow() {
  const d = DOT, w = d.wymagania, WN = DOT_W(), sp = d.sprawdzenie, kp = d.komplet, fold = d.folder || "rozliczenie";
  const stKl = s => /^ok/.test(s) ? "z-startujemy" : /popraw|brak/.test(s) ? "z-czerwony" : /przygotowany|wgrany/.test(s) ? "z-do-analizy" : "z-odpuszczamy";
  const kat = {}; (d.lista || []).forEach(x => (kat[x.kategoria] = kat[x.kategoria] || []).push(x));
  return `
  ${w ? `<div class="krok k-zolt"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>${WN ? 4 : 3}. ${WN ? "Dokumenty wniosku" : "Dokumenty rozliczenia"} – wgraj albo przygotuj</h3>
    <span class="stan">${esc(d.zakres_opis)}</span></div><div class="tresc">
    ${WN ? "" : `<div class="ceny-wybor"><b>Co rozliczasz?</b>
      <label><input type="radio" name="dt-zakres" value="calosc" ${d.zakres === "calosc" ? "checked" : ""} onchange="zakresDotacji(this.value)"> całą dotację (rozliczenie końcowe)</label>
      ${(w.etapy || []).map(e => `<label><input type="radio" name="dt-zakres" value="${esc(e.id)}" ${d.zakres === e.id ? "checked" : ""} onchange="zakresDotacji(this.value)"> ${esc(e.nazwa)}</label>`).join("")}</div>`}
    <p class="opis">Przy każdym dokumencie: <b>Wgraj</b> gotowy plik (np. faktury, protokoły, zdjęcia) albo <b>Przygotuj w programie</b> – dla dokumentów, które program może sporządzić na podstawie danych projektu.</p>
    ${Object.entries(kat).map(([k, L]) => `<h4 class="grupa-analizy">${esc(k)}</h4>
      <div class="tabela-okno"><table class="tabela dt-tab"><tr><th>Dokument</th><th>Stan</th><th>Pliki</th><th></th></tr>
      ${L.map(x => `<tr><td><b>${esc(x.nazwa)}</b><br><small class="opis">${esc(x.opis || "")}${x.podstawa ? " · " + esc(x.podstawa) : ""}${x.termin ? " · termin: " + esc(x.termin) : ""}</small>
          ${x.uwagi_spr ? `<br><small class="czerwone">${esc(x.uwagi_spr)}</small>` : ""}</td>
        <td><span class="znacznik ${stKl(x.stan || (x.pliki.length ? "wgrany" : ""))}">${esc(x.stan || (x.pliki.length ? "wgrany" : "brak"))}</span></td>
        <td><div class="pliki-ik">${x.pliki.map(f => plikIk(PROJEKT_ID, `${fold}/${zkl(d.zakres)}/${x.id}/${f}`, f.length > 26 ? f.slice(0, 24) + "…" : f, 1)
          + `<button class="maly" title="Usuń plik" onclick="usunPlikDotacji('${escA(x.id)}','${escA(f)}')">×</button>`).join("") || "–"}</div></td>
        <td style="white-space:nowrap"><label class="przycisk maly" data-ik="wgraj">Wgraj<input type="file" multiple hidden onchange="wgrajDotacja('${escA(x.id)}', this.files)"></label>
          ${x.mozna_przygotowac ? `<button class="maly zolty" data-ik="iskra" onclick="przygotujDotacja('${escA(x.id)}')">Przygotuj w programie</button>` : ""}</td></tr>`).join("")}</table></div>`).join("")}
  </div></div>
  <div class="krok k-nieb"><div class="tytul"><span class="nr">${ik("alarm")}</span><h3>${WN ? 5 : 4}. Sprawdzenie i komplet ${WN ? "wniosku " : ""}do złożenia</h3>
    <span class="stan">${sp ? esc(sp.ocena) : "do zrobienia"}</span></div><div class="tresc">
    <div class="pasek"><button class="zielony" data-ik="alarm" onclick="sprawdzDotacje()">Sprawdź poprawność dokumentów (AI)</button>
      <button class="glowny" data-ik="pobierz" onclick="kompletDotacji()">Przygotuj komplet do złożenia (ZIP)</button></div>
    ${sp ? `<div class="${/gotowe/.test(sp.ocena) ? "wn-gotowe" : "ramka-uwaga"}" style="margin-top:8px"><span><b>${esc(sp.ocena)}</b> (${esc(sp.data)}) – ${esc(sp.podsumowanie || "")}</span></div>
      ${(sp.uwagi || []).length ? `<ul class="lista">${sp.uwagi.map(u => `<li><b class="${u.waga === "krytyczna" || u.waga === "istotna" ? "czerwone" : ""}">[${esc(u.waga)}] ${esc(u.dokument || "")}</b>: ${esc(u.opis)}${u.propozycja ? ` <i>– ${esc(u.propozycja)}</i>` : ""}</li>`).join("")}</ul>` : ""}
      <div class="pliki-ik">${plikIk(PROJEKT_ID, `${fold}/${zkl(d.zakres)}/Raport_sprawdzenia.docx`, "Raport sprawdzenia")}</div>` : ""}
    ${kp ? `<p class="opis">Komplet (${esc(kp.data)}): ${kp.brakuje.length ? `<b class="czerwone">brakuje: ${esc(kp.brakuje.join(", "))}</b>` : '<b class="zielone">wszystkie dokumenty dołączone</b>'}</p>
      <div class="pliki-ik">${plikIk(PROJEKT_ID, kp.plik, "Komplet do złożenia (ZIP)")}</div>` : ""}
    <p class="opis" style="font-size:12px">Komplet zawiera dokumenty pogrupowane w foldery według kategorii, spis załączników i raport sprawdzenia (do użytku wewnętrznego).
      Złóż go w systemie wskazanym w ${WN ? "regulaminie naboru" : "umowie"}${w && w.system ? " (" + esc(w.system) + ")" : ""}. Dokumenty przygotowane przez program to projekty – sprawdź je z ${WN ? "regulaminem" : "umową"} i wytycznymi.</p>
  </div></div>` : ""}`;
}
const zkl = z => String(z || "calosc").replace(/[^\w\-]+/g, "_").slice(0, 60);
async function zapiszDaneDotacji() {
  const d = DOT_W() ? {opis_projektu: $("#wd-opis").value, koszt_calkowity: $("#wd-koszt").value, kwota_wnioskowana: $("#wd-kwota").value, okres_realizacji: $("#wd-okres").value, lokalizacja: $("#wd-lok").value}
    : {program: $("#dt-program").value, nr_umowy: $("#dt-nr").value, kwota: $("#dt-kwota").value, beneficjent: $("#dt-ben").value};
  return bezpiecznie(() => api(`${DOT_URL()}/dane`, {json: d}));
}
// ---------- nadchodzące nabory (harmonogramy) i alerty
let HN = null, HN_F = {region: "dolnośląskie", branza: "", wnioskodawca: "", slowa: "", trwajace: false}, ALD = null, AL_ED = null;
async function rysujNadchodzace() {
  const q = new URLSearchParams({region: HN_F.region === "cała Polska" ? "" : HN_F.region, branza: HN_F.branza, wnioskodawca: HN_F.wnioskodawca, slowa: HN_F.slowa, trwajace: HN_F.trwajace ? "1" : ""});
  [HN, ALD] = await Promise.all([api("/api/dotacje/harmonogram?" + q).catch(() => null), api("/api/dotacje/alerty").catch(() => ({alerty: []}))]);
  if (!HN) return;
  const sel = (id, op, w, pusta) => `<select id="${id}">${pusta ? `<option value="">${pusta}</option>` : ""}${op.map(o => `<option ${o === w ? "selected" : ""}>${esc(o)}</option>`).join("")}</select>`;
  const mies = {}; HN.nabory.forEach(n => { const k = (n.data_od || n.data_od_przyblizona || "").slice(0, 7) || "bez daty"; (mies[k] = mies[k] || []).push(n); });
  const MN = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"];
  const nazwaM = k => k === "bez daty" ? "Termin do ustalenia" : `${MN[+k.slice(5, 7) - 1]} ${k.slice(0, 4)}`;
  const zrOk = (HN.zrodla || []).filter(z => z.skrot).length;
  $("#dot-nadchodzace").innerHTML = `<div class="pulpit-glowka"><h2>Nadchodzące nabory</h2></div>
    <p class="opis">Nabory zapowiedziane w harmonogramach województw (programy regionalne Funduszy Europejskich) i instytucji pośredniczących.
      Harmonogramy są pobierane automatycznie co tydzień; AI czyta tylko pliki, które się zmieniły.</p>
    <div class="karta"><div class="siatka">
      <label>Region${sel("hn-region", ["cała Polska", ...HN.regiony], HN_F.region)}</label>
      <label>Branża / zakres${sel("hn-branza", HN.branze, HN_F.branza, "– dowolny –")}</label>
      <label>Wnioskodawca${sel("hn-wn", HN.wnioskodawcy, HN_F.wnioskodawca, "– dowolny –")}</label>
      <label>Słowa kluczowe<input id="hn-slowa" value="${esc(HN_F.slowa)}" placeholder="np. termomodernizacja, OZE"></label></div>
      <div class="pasek"><button class="zielony" data-ik="szukaj" onclick="filtrujNadchodzace()">Pokaż</button>
        <label class="check" style="margin:0"><input type="checkbox" id="hn-trwa" ${HN_F.trwajace ? "checked" : ""}> pokaż też nabory, które już trwają</label>
        <button data-ik="alarm" onclick="nowyAlertZFiltra()">Ustaw alert dla tych kryteriów</button>
        <button class="maly" data-ik="odswiez" onclick="odswiezHarmonogramy()">Odśwież harmonogramy${HN_F.region && HN_F.region !== "cała Polska" ? " (" + esc(HN_F.region) + ")" : ""}</button>
        <span class="opis" style="margin:0">${HN.odswiezono ? "ostatnio: " + esc(HN.odswiezono) + " · " : ""}harmonogramów: ${zrOk} · naborów w bazie: ${HN.liczba_wszystkich}</span></div></div>
    <div id="hn-alerty"></div>
    <h4 class="grupa-analizy">Nabory (${HN.nabory.length})</h4>
    ${HN.nabory.length ? Object.entries(mies).map(([k, L]) => `<div class="hn-miesiac"><b>${nazwaM(k)}</b><span class="opis" style="margin:0">${L.length}</span></div>
      <div class="dot-wyniki">${L.map(n => `<div class="dot-wynik hn">
        <div class="dw-gora"><b>${esc(n.tytul)}</b><span class="znacznik ${n.status === "trwa" ? "z-startujemy" : "z-do-analizy"}">${n.status === "trwa" ? "trwa" : "planowany"}</span></div>
        <div class="opis" style="margin:2px 0 6px">${esc([n.program, n.dzialanie].filter(Boolean).join(" · "))}</div>
        <div class="dw-kafle"><span>${ik("kalendarz")} <b>${esc(n.data_od ? dataPl(n.data_od) + (n.data_do ? " – " + dataPl(n.data_do) : "") : (n.termin_opis || "termin do ustalenia"))}</b></span>
          <span class="znacznik z-odpuszczamy">${esc(n.region)}</span>${n.kwota ? `<span>${esc(n.kwota)}</span>` : ""}</div>
        ${n.typy_projektow ? `<p>${esc(n.typy_projektow)}</p>` : ""}
        <p class="opis" style="margin:0"><b>Dla kogo:</b> ${esc(n.wnioskodawcy_opis || (n.wnioskodawcy || []).join(", ") || "–")}${n.instytucja ? ` · <b>Instytucja:</b> ${esc(n.instytucja)}` : ""}</p>
        <div class="pasek" style="margin-top:8px"><button class="maly zielony" data-ik="plus" onclick="wniosekZHarmonogramu('${escA(n.id)}')">Przygotuj się do naboru</button>
          ${n.zrodlo_url ? `<a class="przycisk maly dozw" data-ik="link" href="${esc(n.zrodlo_url)}" target="_blank" rel="noopener">Harmonogram (źródło)</a>` : ""}</div></div>`).join("")}</div>`).join("")
      : `<p class="pusto">${HN.liczba_wszystkich ? "Brak nadchodzących naborów dla wybranych kryteriów." : "Baza harmonogramów jest pusta – kliknij „Odśwież harmonogramy”."}</p>`}
    ${ADMIN() ? `<details class="karta" style="margin-top:14px"><summary><b>Źródła harmonogramów</b> (administrator)</summary>
      <p class="opis">Program sam szuka „Harmonogramu naborów” na portalach województw. Gdy go nie znajdzie albo chcesz dodać instytucję pośredniczącą (np. WFOŚiGW, PARP, NFOŚiGW), dodaj adres strony z harmonogramem albo bezpośredni link do pliku.</p>
      <div class="tabela-okno"><table class="tabela"><tr><th>Region / instytucja</th><th>Źródło</th><th>Stan</th><th>Pobrano</th></tr>
        ${(HN.zrodla || []).map(z => `<tr><td>${esc(z.region || z.klucz)}</td><td>${z.plik_url ? `<a href="${esc(z.plik_url)}" target="_blank" rel="noopener">${esc(z.plik || "plik")}</a>` : esc(z.url || "–")}</td>
          <td>${esc(z.status || "")}</td><td>${esc(z.data || "")}</td></tr>`).join("") || '<tr><td colspan="4" class="pusto">Jeszcze nie pobierano.</td></tr>'}</table></div>
      ${(HN.wlasne_zrodla || []).length ? `<h4 class="grupa-analizy">Dodane ręcznie</h4><ul class="lista">${HN.wlasne_zrodla.map(z => `<li>${esc(z.region)} – ${esc(z.nazwa || "")} <a href="${esc(z.url)}" target="_blank" rel="noopener">${esc(z.url.slice(0, 70))}</a>
        <button class="maly niebezp" onclick="zrodloHarm({usun: '${escA(z.url)}'})">×</button></li>`).join("")}</ul>` : ""}
      <div class="pasek"><select id="zh-region">${["cała Polska", ...HN.regiony].map(r => `<option>${esc(r)}</option>`).join("")}</select>
        <input id="zh-nazwa" placeholder="np. WFOŚiGW we Wrocławiu" style="max-width:220px"><input id="zh-url" placeholder="https://…/harmonogram-naborow" style="flex:1;min-width:220px">
        <button class="maly" data-ik="plus" onclick="zrodloHarm({region: $('#zh-region').value, nazwa: $('#zh-nazwa').value, url: $('#zh-url').value})">Dodaj źródło</button></div></details>` : ""}`;
  rysujAlertyDot(); wstawIkony($("#dot-nadchodzace"));
}
function filtrujNadchodzace() {
  HN_F = {region: $("#hn-region").value, branza: $("#hn-branza").value, wnioskodawca: $("#hn-wn").value, slowa: $("#hn-slowa").value, trwajace: $("#hn-trwa").checked};
  rysujNadchodzace();
}
async function odswiezHarmonogramy() {
  const reg = HN_F.region && HN_F.region !== "cała Polska" ? [HN_F.region] : [];
  sledz(await bezpiecznie(() => api("/api/dotacje/harmonogram/odswiez", {json: {regiony: reg}})), () => { if (WIDOK === "dot_nadchodzace") rysujNadchodzace(); });
}
async function zrodloHarm(d) { if (await bezpiecznie(() => api("/api/dotacje/harmonogram/zrodla", {json: d}))) { komunikat("Zapisano źródło."); rysujNadchodzace(); } }
async function wniosekZHarmonogramu(id) {
  const w = await bezpiecznie(() => api("/api/dotacje/wniosek", {json: {harmonogram: id}})); if (!w) return;
  komunikat("Utworzono wniosek z zapowiedzianego naboru – dokumenty dodasz po ogłoszeniu naboru (albo z linku na portalu).");
  TRYB = "wniosek_dot"; PROJEKT_ID = w.id; pokaz("dot_wnioski");
}
function rysujAlertyDot() {
  const el = $("#hn-alerty"); if (!el || !ALD) return;
  const L = ALD.alerty || [];
  el.innerHTML = `<div class="karta hn-alerty"><div class="polecane-gora"><b>${ik("alarm")} Moje alerty</b><button class="maly" data-ik="plus" onclick="AL_ED = {}; rysujAlertyDot()">Nowy alert</button></div>
    <p class="opis" style="margin:0 0 6px">Alert powiadamia (w programie i e-mailem, jeśli w Ustawieniach są adresy i poczta) o nowych naborach w harmonogramach dla wybranego regionu i zakresu oraz przypomina przed startem naboru.</p>
    ${L.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Alert</th><th>Regiony</th><th>Zakres</th><th>Przypomnienie</th><th>Pasujące</th><th></th></tr>
      ${L.map(a => `<tr><td><b>${esc(a.nazwa)}</b>${a.email ? ' <small class="opis">e-mail</small>' : ""}</td><td>${esc((a.regiony || []).join(", ") || "wszystkie")}</td>
        <td>${esc([...(a.branze || []), ...(a.wnioskodawcy || []), a.slowa].filter(Boolean).join(", ") || "dowolny")}</td><td>${a.dni_przed} dni przed</td>
        <td><b>${a.trafienia}</b>${a.nowe && a.nowe.length ? ` <span class="znacznik z-czerwony">${a.nowe.length} nowych</span>` : ""}</td>
        <td style="white-space:nowrap"><button class="maly" onclick="pokazAlert('${a.id}')">Pokaż</button> <button class="maly" data-ik="przelacz" onclick="AL_ED = ALD.alerty.find(x => x.id === '${a.id}'); rysujAlertyDot()">Edytuj</button>
          <button class="maly niebezp" data-ik="kosz" onclick="usunAlertDot('${a.id}')"></button></td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak alertów.</p>'}
    ${AL_ED ? `<div class="hn-edytor"><div class="siatka"><label>Nazwa alertu<input id="al-nazwa" value="${esc(AL_ED.nazwa || "")}" placeholder="np. Termomodernizacja – dolnośląskie"></label>
        <label>Przypomnij przed startem naboru [dni]<input id="al-dni" type="number" min="0" max="90" value="${AL_ED.dni_przed ?? 14}"></label>
        <label>Słowa kluczowe<input id="al-slowa" value="${esc(AL_ED.slowa || "")}"></label>
        <label class="check"><input type="checkbox" id="al-email" ${AL_ED.email !== false ? "checked" : ""}> wysyłaj e-mail</label></div>
      <b>Regiony</b><div class="wybor-h">${["cała Polska", ...HN.regiony].map(r => `<label><input type="checkbox" class="al-reg" value="${esc(r)}" ${(AL_ED.regiony || []).includes(r) ? "checked" : ""}> ${esc(r)}</label>`).join("")}</div>
      <b>Zakres (branże)</b><div class="wybor-h">${HN.branze.map(r => `<label><input type="checkbox" class="al-br" value="${esc(r)}" ${(AL_ED.branze || []).includes(r) ? "checked" : ""}> ${esc(r)}</label>`).join("")}</div>
      <b>Wnioskodawca</b><div class="wybor-h">${HN.wnioskodawcy.map(r => `<label><input type="checkbox" class="al-wn" value="${esc(r)}" ${(AL_ED.wnioskodawcy || []).includes(r) ? "checked" : ""}> ${esc(r)}</label>`).join("")}</div>
      <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszAlertDot()">Zapisz alert</button><button class="maly" onclick="AL_ED = null; rysujAlertyDot()">Anuluj</button></div></div>` : ""}</div>`;
  wstawIkony(el);
}
function nowyAlertZFiltra() {
  AL_ED = {nazwa: [HN_F.branza, HN_F.region].filter(Boolean).join(" – ") || "Mój alert", regiony: HN_F.region && HN_F.region !== "cała Polska" ? [HN_F.region] : [],
    branze: HN_F.branza ? [HN_F.branza] : [], wnioskodawcy: HN_F.wnioskodawca ? [HN_F.wnioskodawca] : [], slowa: HN_F.slowa, dni_przed: 14, email: true};
  rysujAlertyDot(); $("#hn-alerty").scrollIntoView({behavior: "smooth"});
}
async function zapiszAlertDot() {
  const v = c => [...document.querySelectorAll(c + ":checked")].map(x => x.value);
  const d = {id: AL_ED.id, nazwa: $("#al-nazwa").value, dni_przed: $("#al-dni").value, slowa: $("#al-slowa").value, email: $("#al-email").checked,
    regiony: v(".al-reg"), branze: v(".al-br"), wnioskodawcy: v(".al-wn"), bez_obecnych: !AL_ED.id};
  if (await bezpiecznie(() => api("/api/dotacje/alerty", {json: d}))) { komunikat("Zapisano alert."); AL_ED = null; rysujNadchodzace(); }
}
async function usunAlertDot(id) { if (confirm("Usunąć alert?") && await bezpiecznie(() => api("/api/dotacje/alerty", {json: {usun: id}}))) rysujNadchodzace(); }
async function pokazAlert(id) {
  const a = ALD.alerty.find(x => x.id === id); if (!a) return;
  HN_F = {region: (a.regiony || [])[0] || "cała Polska", branza: (a.branze || [])[0] || "", wnioskodawca: (a.wnioskodawcy || [])[0] || "", slowa: a.slowa || "", trwajace: false};
  await api("/api/dotacje/alerty", {json: {widziane: id}}).catch(() => {});
  rysujNadchodzace();
}

// ---------- wyszukiwanie dotacji
const WOJ = ["cała Polska", "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", "małopolskie", "mazowieckie", "opolskie", "podkarpackie", "podlaskie",
  "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie", "wielkopolskie", "zachodniopomorskie"];
async function rysujSzukajDotacji() {
  const d = await api("/api/dotacje/wyniki").catch(() => ({})), k = d.kryteria || {};
  const sel = (id, opcje, wart, pusta) => `<select id="${id}">${pusta ? `<option value="">${pusta}</option>` : ""}${opcje.map(o => `<option ${o === wart ? "selected" : ""}>${esc(o)}</option>`).join("")}</select>`;
  $("#dot-szukaj").innerHTML = `<div class="pulpit-glowka"><h2>Wyszukaj dotację</h2></div>
    <p class="opis">Program wyszukuje aktualne nabory (KPO, FEnIKS, FENG, programy regionalne, NFOŚiGW/WFOŚiGW, BGK, PARP, ARiMR…) według branży i regionu – na oficjalnych stronach programów.</p>
    <div class="karta"><div class="siatka">
      <label>Branża / obszar${sel("ds-branza", d.branze || [], k.branza, "– dowolna –")}</label>
      <label>Region${sel("ds-region", WOJ, k.region || "dolnośląskie")}</label>
      <label>Wnioskodawca${sel("ds-wn", d.wnioskodawcy || [], k.wnioskodawca, "– dowolny –")}</label>
      <label>Cel / słowa kluczowe<input id="ds-slowa" value="${esc(k.slowa || "")}" placeholder="np. pompa ciepła, fotowoltaika, zakup maszyn"></label>
      <label style="grid-column:1/-1">Co chcesz zrobić? Opisz pomysł – program znajdzie nabory, które go sfinansują
        <textarea id="ds-pomysl" placeholder="np. Chcę kupić opryskiwacz i siewnik oraz założyć fotowoltaikę 30 kW na budynku gospodarczym; albo: przeszkolić 12 pracowników z obsługi CNC">${esc(k.pomysl || "")}</textarea></label></div>
      <div class="pasek"><button class="zielony" data-ik="szukaj" onclick="szukajDotacji()">Szukaj dotacji</button>
        <label class="check" style="margin:0"><input type="checkbox" id="ds-odswiez"> szukaj ponownie w internecie (pomiń pamięć programu)</label>
        <span class="opis" style="margin:0;flex-basis:100%">Program czyta listę naborów z portalu Funduszy Europejskich wybranego województwa i programy krajowe. Nabory pobrane wcześniej bierze z pamięci programu – pobiera tylko nowe, więc kolejne wyszukiwania są szybkie i tanie.</span></div>
      <div class="pasek" style="margin-top:10px;border-top:1px dashed var(--linia);padding-top:10px"><b>Masz link do naboru?</b>
        <input id="ds-link" placeholder="np. https://funduszeuedolnoslaskie.pl/nabory/14736-…" style="flex:1;min-width:260px">
        <button data-ik="link" onclick="naborZLinku()">Dodaj nabór z linku</button></div></div>
    ${d.wyniki ? `<h4 class="grupa-analizy">Wyniki (${d.wyniki.length}) – ${esc(d.data || "")}: ${esc([k.branza, k.region, k.wnioskodawca, k.slowa].filter(Boolean).join(" · "))}</h4>
      <div class="dot-wyniki">${d.wyniki.map(x => `<div class="dot-wynik">
        <div class="dw-gora"><b>${esc(x.nazwa)}</b>${x.dopasowanie ? `<span class="ocena">${esc(x.dopasowanie)}</span>` : ""}</div>
        ${x.zrodlo ? `<small class="znacznik ${x.zrodlo === "wyszukiwanie w internecie" ? "z-odpuszczamy" : "z-startujemy"}">${esc({"portal regionalny": "z portalu regionalnego", link: "dodany z linku"}[x.zrodlo] || x.zrodlo)}</small>` : ""}
        <div class="opis" style="margin:2px 0 6px">${esc([x.program, x.instytucja].filter(Boolean).join(" · "))}</div>
        <div class="dw-kafle"><span class="znacznik ${/otwarty|ciągły/.test(x.status || "") ? "z-startujemy" : "z-do-analizy"}">${esc(x.status || "")}</span>
          ${x.poziom_dofinansowania ? `<span>${esc(x.poziom_dofinansowania)}</span>` : ""}${x.kwota ? `<span>${esc(x.kwota)}</span>` : ""}
          ${x.nabor_do ? `<span>nabór do: <b>${esc(x.nabor_do)}</b></span>` : ""}</div>
        <p>${esc(x.opis || "")}</p>${x.pobrano ? `<small class="opis">w pamięci programu od ${esc(x.pobrano.slice(0, 10))}</small>` : ""}<p class="opis" style="margin:0"><b>Dla kogo:</b> ${esc(x.dla_kogo || "–")}${x.uzasadnienie ? ` · <b>Dlaczego pasuje:</b> ${esc(x.uzasadnienie)}` : ""}</p>
        ${(x.dokumenty || []).length ? `<div class="opis" style="margin:6px 0 0">Dokumenty: ${x.dokumenty.map(u => `<a href="${esc(u.url)}" target="_blank" rel="noopener">${esc(u.nazwa || "plik")}</a>`).join(" · ")}</div>` : ""}
        <div class="pasek" style="margin-top:8px"><button class="zielony maly" data-ik="plus" onclick="uzyskajDotacje('${escA(x.id)}')">Uzyskaj dotację – przygotuj wniosek</button>
          ${x.link ? `<a class="przycisk maly dozw" data-ik="link" href="${esc(x.link)}" target="_blank" rel="noopener">Strona naboru</a>` : ""}</div></div>`).join("")}</div>
      <p class="opis" style="font-size:12px">Wyniki pochodzą z wyszukiwania w internecie – terminy i warunki sprawdź na stronie naboru.</p>` : ""}`;
  wstawIkony($("#dot-szukaj"));
}
// ================================================================ PLAN PROJEKTU DOTACYJNEGO (każdy rodzaj dotacji)
let DPL = null;
async function ladujPlan() { if (!$("#plan-projektu") || !PROJEKT_ID) return; DPL = await api(`/api/projekty/${PROJEKT_ID}/plan`).catch(() => null); if (DPL) rysujPlan(); }
const plZl = x => zl(+x || 0);
// „?” przy trudnych pojęciach (SO, de minimis, kWp, intensywność…) – dotknięcie pokazuje wyjaśnienie i jak to sprawdzić
const pomBtn = id => DPL && DPL.pomoc && DPL.pomoc[id] ? `<button type="button" class="pom-ik" data-pom="${id}" aria-label="Co to znaczy?" title="Co to znaczy?">?</button>` : "";
function pokazPomoc(btn) {
  const [tyt, opis, jak] = (DPL.pomoc || {})[btn.dataset.pom] || [];
  if (!tyt) return;
  let d = $("#pom-dymek"); if (!d) { d = document.createElement("div"); d.id = "pom-dymek"; document.body.appendChild(d); }
  if (d.style.display === "block" && d.dataset.dla === btn.dataset.pom) { d.style.display = "none"; return; }
  d.dataset.dla = btn.dataset.pom;
  d.innerHTML = `<div class="pom-gora"><b>${esc(tyt)}</b><button type="button" class="pom-x" onclick="this.parentNode.parentNode.style.display='none'">✕</button></div>
    <p>${esc(opis)}</p>${jak ? `<p class="pom-jak">${esc(jak)}</p>` : ""}`;
  d.style.display = "block";
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight, r = btn.getBoundingClientRect(), w = Math.min(380, W - 24);
  d.style.width = w + "px"; d.style.left = Math.max(12, Math.min(r.left - 20, W - w - 12)) + "px";
  const h = d.offsetHeight; d.style.top = (r.bottom + h + 12 < H ? r.bottom + 6 : Math.max(12, r.top - h - 6)) + "px";
}
document.addEventListener("click", e => {
  const b = e.target.closest && e.target.closest(".pom-ik");
  if (b) { e.preventDefault(); e.stopPropagation(); pokazPomoc(b); return; }
  const d = $("#pom-dymek"); if (d && d.style.display === "block" && !(e.target.closest && e.target.closest("#pom-dymek"))) d.style.display = "none";
}, true);
function polePlanu(pid, a, [id, et, typ, op]) {
  const v = a[id];
  if (typ === "wybor") return `<label><span class="lab-pom">${esc(et)}${pomBtn(id)}</span><select data-pole="${id}"><option value=""></option>${op.map(o => `<option ${o === v ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`;
  if (typ === "multi") return `<div style="grid-column:1/-1"><span class="opis" style="margin:0">${esc(et)}</span>${pomBtn(id)}<div class="pasek" style="margin:4px 0">${op.map(o =>
    `<label class="wiersz" style="margin:0"><input type="checkbox" data-multi="${id}" value="${esc(o)}" ${(v || []).includes(o) ? "checked" : ""}> ${esc(o)}</label>`).join("")}</div></div>`;
  return `<label><span class="lab-pom">${esc(et)}${pomBtn(id)}</span><input data-pole="${id}" ${typ === "liczba" ? 'inputmode="decimal"' : ""} value="${esc(v ?? "")}" ${op && typ === "liczba" ? `placeholder="${esc(op)}"` : ""}></label>`;
}
function rysujPlan() {
  const P = DPL, p = P.plan, K = P.katalog, reg = P.reguly || {}, b = P.budzet, WN = P.faza === "wniosek", prof = P.profil || {};
  const typW = P.typy_wnioskodawcy[prof.typ] || null;
  const dz = p.dzialania || [], kon = p.kontrola;
  const katNaz = k => (K[k] || {}).nazwa || k;
  const regKat = Object.fromEntries((reg.kategorie || []).map(x => [x.id, x]));
  const el = $("#plan-projektu");
  if (!WN && !(p.pozycje || []).length) { el.innerHTML = ""; return; }
  const kartaPoz = x => { const kt = K[x.kategoria] || {pola: []}, a = x.atrybuty || {}, rk = regKat[x.kategoria];
    return `<div class="karta pl-poz" data-id="${x.id}" data-kat="${x.kategoria}" style="margin:8px 0;padding:12px 14px">
      <div class="pasek" style="margin:0 0 6px"><span class="znacznik z-odpuszczamy">${esc(katNaz(x.kategoria))}</span>
        ${rk && rk.kwalifikowalna === false ? '<span class="znacznik z-czerwony">niekwalifikowalna w naborze</span>' : ""}
        ${x.dzialanie ? `<small class="opis" style="margin:0">${esc((dz.find(d => d.id === x.dzialanie) || {}).nazwa || "")}</small>` : ""}
        <button class="maly" style="margin-left:auto" onclick="usunPozPlanu('${x.id}')">Usuń</button></div>
      <div class="siatka"><label style="grid-column:1/-1">Nazwa pozycji<input data-pole-glowne="nazwa" value="${esc(x.nazwa || "")}"></label>
        ${kt.pola.map(f => polePlanu(x.id, a, f)).join("")}
        <label>Ilość<input data-pole-glowne="ilosc" inputmode="decimal" value="${esc(x.ilosc ?? 1)}"></label>
        <label>Cena jednostkowa netto [zł]<input data-pole-glowne="cena_netto" inputmode="decimal" value="${esc(x.cena_netto ?? "")}"></label>
        <label>VAT [%]<input data-pole-glowne="vat" inputmode="decimal" value="${esc(x.vat ?? 23)}"></label>
        <label title="Pozycje z tej samej grupy CPV (3 pierwsze cyfry) – albo, bez kodu, z tej samej kategorii – program sumuje przy wyborze trybu (zakaz dzielenia zamówienia)">Kod CPV (opcjonalnie)<input data-pole-glowne="cpv" inputmode="numeric" placeholder="np. 45321000-3" value="${esc(x.cpv || "")}"></label>
        <label>Miesiąc od – do<span class="pasek" style="margin:0;gap:4px"><input data-pole-glowne="miesiac_od" inputmode="numeric" style="width:60px" value="${esc(x.miesiac_od ?? "")}" placeholder="od">
          <input data-pole-glowne="miesiac_do" inputmode="numeric" style="width:60px" value="${esc(x.miesiac_do ?? "")}" placeholder="do"></span></label></div>
      ${x.zrodlo_ceny ? `<small class="opis">Cena: ${esc(x.zrodlo_ceny)}</small>` : ""}
      ${rk && rk.uwagi ? `<div class="sugestia" style="margin-top:6px"><b>Regulamin:</b> ${esc(rk.uwagi)}</div>` : ""}
      ${x.kategoria === "roboty" ? `<div class="pasek" style="margin:6px 0 0"><button class="maly" data-ik="kalkulator" onclick="kosztorysPozycji('${x.id}')">Wyceń w Kosztorysowaniu</button>
        <span class="opis" style="margin:0">Po przygotowaniu kosztorysu wpisz jego wartość netto jako cenę.</span></div>` : ""}</div>`; };
  const harmMax = Math.max(6, ...P.harmonogram.map(h => h.do));
  el.innerHTML = WN ? `
  <div class="krok k-ziel" id="sek-plan"><div class="tytul"><span class="nr">${ik("teczka")}</span><h3>3. Zakres projektu – na co chcesz dotację</h3>
    <span class="stan">${(p.pozycje || []).length ? odm(p.pozycje.length, "pozycja", "pozycje", "pozycji") + " · dotacja " + plZl(b.suma.dotacja) : "do zrobienia"}</span></div><div class="tresc">
    <details class="pom-slownik"><summary>Słowniczek pojęć – co znaczą trudne terminy (SO, de minimis, intensywność, koszty kwalifikowalne…)</summary>
      <dl>${Object.values(DPL.pomoc || {}).sort((a, b) => a[0].localeCompare(b[0], "pl")).map(([t, o, jk]) => `<dt>${esc(t)}</dt><dd>${esc(o)}${jk ? `<br><small class="opis">${esc(jk)}</small>` : ""}</dd>`).join("")}</dl></details>
    <p class="opis" style="margin:4px 0 0">Przy trudnych pojęciach jest znak <span class="pom-ik" style="pointer-events:none">?</span> – dotknij go, a program wyjaśni, co to znaczy i gdzie to sprawdzić.</p>
    <h4 class="grupa-analizy">Wnioskodawca</h4>
    <div class="siatka"><label>Kim jesteś?<select id="pl-typ" onchange="DPL.profil.typ=this.value; rysujPlan()"><option value=""></option>${Object.entries(P.typy_wnioskodawcy).map(([k, v]) => `<option value="${k}" ${k === prof.typ ? "selected" : ""}>${esc(v.nazwa)}</option>`).join("")}</select></label>
      ${typW ? typW.pola.map(([id, et, typ, op]) => typ === "wybor" ? `<label><span class="lab-pom">${esc(et)}${pomBtn(id)}</span><select data-prof="${id}"><option value=""></option>${op.map(o => `<option ${o === prof[id] ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`
        : `<label><span class="lab-pom">${esc(et)}${pomBtn(id)}</span><input data-prof="${id}" value="${esc(prof[id] || "")}">${id === "wielkosc_ekonomiczna"
          ? `<button type="button" class="maly" data-ik="kalkulator" style="margin-top:6px" onclick="otworzSO()">Oblicz SO</button>` : ""}</label>`).join("") : ""}</div>
    <div id="so-panel"></div>
    <h4 class="grupa-analizy">Co chcesz zrobić?</h4>
    <textarea id="pl-pomysl" placeholder="Opisz własnymi słowami, np. fotowoltaika 30 kW z magazynem 20 kWh i pompa ciepła do budynku gospodarczego; albo szkolenie 12 pracowników…">${esc(p.pomysl || "")}</textarea>
    <div class="pasek"><button class="zolty" data-ik="iskra" onclick="analizaPlanu()">${dz.length ? "Ustal ponownie, co można sfinansować (AI)" : "Ustal, co można sfinansować (AI)"}</button>
      <span class="opis" style="margin:0">AI czyta regulamin naboru: działania, kategorie kosztów, limity, intensywność, wskaźniki, kryteria punktowe${p.pomysl ? " – i proponuje pozycje dla Twojego pomysłu" : ""}.</span></div>
    ${dz.length ? `<h4 class="grupa-analizy">Co można sfinansować w tym naborze</h4><div class="pl-dzialania">${dz.map(d => `<div class="karta" style="margin:6px 0;padding:10px 14px">
      <b>${esc(d.nazwa)}</b>${d.limit_zl ? ` <span class="znacznik z-do-analizy">do ${plZl(d.limit_zl)}</span>` : ""}${d.intensywnosc_procent ? ` <span class="znacznik z-startujemy">${d.intensywnosc_procent}%</span>` : ""}
      ${d.opis ? `<div class="opis" style="margin:4px 0">${esc(d.opis)}</div>` : ""}${(d.wymagania || []).length ? `<ul class="lista" style="margin:4px 0">${d.wymagania.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
      <div class="pasek" style="margin:4px 0 0">${(d.kategorie || ["inne"]).filter(k => K[k]).map(k => `<button class="maly" data-ik="plus" onclick="dodajPozPlanu('${k}', '${d.id}', ${jsa(d.nazwa || "")})">Dodaj: ${esc(katNaz(k))}</button>`).join("")}</div></div>`).join("")}</div>
      ${(reg.wylaczenia || []).length ? `<div class="ramka-uwaga"><b>Nabór nie finansuje:</b><ul class="lista">${reg.wylaczenia.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}` : ""}
    <h4 class="grupa-analizy">Pozycje projektu</h4>
    <div id="pl-pozycje">${(p.pozycje || []).map(kartaPoz).join("") || '<p class="opis">Dodaj pozycje z listy działań powyżej albo własną pozycję.</p>'}</div>
    <div class="pasek"><select id="pl-nowa-kat">${Object.entries(K).map(([k, v]) => `<option value="${k}">${esc(v.nazwa)}</option>`).join("")}</select>
      <button class="maly" data-ik="plus" onclick="dodajPozPlanu($('#pl-nowa-kat').value, '', '')">Dodaj własną pozycję</button>
      <button class="glowny" data-ik="zapisz" onclick="zapiszPlan()">Zapisz zakres i przelicz</button>
      ${(p.pozycje || []).length ? `<button class="zolty" data-ik="iskra" onclick="wycenaPlanu()">Sprawdź ceny w internecie (AI)</button>` : ""}</div>
    ${(p.pozycje || []).length ? `
    <h4 class="grupa-analizy">Budżet i dotacja</h4>
    <div class="kwoty kafle-przetargu"><div><span>Koszty netto</span><b>${plZl(b.suma.netto)}</b></div><div><span>Koszty kwalifikowalne ${pomBtn("kwalifikowalne")}</span><b>${plZl(b.suma.kwal)}</b></div>
      <div><span>Dotacja ${pomBtn("intensywnosc_procent")}</span><b style="color:var(--bdv-morski,#1F5A99)">${plZl(b.suma.dotacja)}</b></div><div><span>Wkład własny ${pomBtn("wklad_wlasny")}</span><b>${plZl(b.suma.wklad_wlasny)}</b></div></div>
    <div class="tabela-okno"><table class="tabela"><tr><th>Pozycja</th><th>Netto</th><th>VAT</th><th>Kwalifikowalne</th><th>%</th><th>Dotacja</th></tr>
      ${b.wiersze.map(w => `<tr><td>${esc(w.nazwa || "")}<br><small class="opis">${esc(katNaz(w.kategoria))}</small></td><td class="liczba">${plZl(w.netto)}</td><td class="liczba">${plZl(w.vat)}</td>
        <td class="liczba">${plZl(w.kwalifikowalne)}</td><td class="liczba">${w.intensywnosc || "–"}</td><td class="liczba">${plZl(w.dotacja)}</td></tr>`).join("")}</table></div>
    ${b.ostrzezenia.map(x => `<div class="ramka-uwaga">⚠ ${esc(x)}</div>`).join("")}
    ${WN ? (P.wybor_ostrzezenia || []).map(x => `<div class="ramka-uwaga">⚠ ${esc(x)}</div>`).join("") : ""}
    <details><summary>Zasady naboru użyte w obliczeniach (możesz poprawić)</summary><div class="siatka">
      ${[["intensywnosc_procent", "Intensywność dofinansowania [%]"], ["limit_projektu_zl", "Limit dotacji na projekt [zł]"], ["min_koszty_zl", "Minimalne koszty kwalifikowalne [zł]"],
         ["max_koszty_zl", "Maksymalne koszty kwalifikowalne [zł]"], ["trwalosc_lat", "Okres trwałości [lata]"]].map(([k, e]) => `<label><span class="lab-pom">${e}${pomBtn(k)}</span><input data-recz="${k}" value="${esc(reg[k] ?? "")}"></label>`).join("")}
      <label class="wiersz"><input type="checkbox" data-recz="vat_kwalifikowalny" ${reg.vat_kwalifikowalny ? "checked" : ""}> VAT jest kosztem kwalifikowalnym ${pomBtn("vat_kwalifikowalny")}</label></div></details>
    <div class="pasek"><a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${P.id}/plan/xlsx">Zestawienie rzeczowo-finansowe (Excel)</a></div>
    <h4 class="grupa-analizy">Wskaźniki (wyliczone z zakresu)</h4>
    ${P.wskazniki.length ? `<ul class="lista">${P.wskazniki.map(w => `<li><b>${esc(w.nazwa)}</b>: ${w.wartosc} ${esc(w.jednostka)}${w.uwaga ? ` <small class="opis">(${esc(w.uwaga)})</small>` : ""}</li>`).join("")}</ul>` : '<p class="opis">Uzupełnij parametry pozycji (moc, liczba osób, stanowiska…).</p>'}
    ${(reg.wskazniki_obowiazkowe || []).length ? `<p class="opis"><b>Wskaźniki wymagane w naborze:</b> ${reg.wskazniki_obowiazkowe.map(w => esc(w.nazwa + (w.jednostka ? " [" + w.jednostka + "]" : ""))).join(" · ")}</p>` : ""}
    <h4 class="grupa-analizy">Harmonogram (miesiące realizacji)</h4>
    <div class="tabela-okno"><table class="tabela pl-harm"><tr><th>Pozycja</th>${Array.from({length: harmMax}, (_, i) => `<th>${i + 1}</th>`).join("")}</tr>
      ${P.harmonogram.map(h => `<tr><td>${esc(h.nazwa || "")}</td>${Array.from({length: harmMax}, (_, i) => `<td class="${i + 1 >= h.od && i + 1 <= h.do ? "pl-pasek" : ""}"></td>`).join("")}</tr>`).join("")}</table></div>
    <h4 class="grupa-analizy">Zgodność z regulaminem i punkty</h4>
    <div class="pasek"><button class="zolty" data-ik="iskra" onclick="kontrolaPlanu()">${kon ? "Sprawdź ponownie (AI)" : "Sprawdź z regulaminem i kryteriami punktowymi (AI)"}</button></div>
    ${kon ? `<div class="karta" style="margin:8px 0"><b>Ocena: ${esc(kon.ocena || "")}</b>${kon.punkty_szacowane != null ? ` · szacowane punkty: <b>${kon.punkty_szacowane}${kon.punkty_max ? " / " + kon.punkty_max : ""}</b>` : ""}
      <span class="opis"> · ${esc(kon.data || "")}</span><p style="margin:6px 0 0">${esc(kon.podsumowanie || "")}</p></div>
      ${(kon.wiecej_punktow || []).length ? `<h4 class="grupa-analizy">Jak zdobyć więcej punktów</h4><ul class="lista">${kon.wiecej_punktow.map(x => `<li><b>${esc(x.zmiana)}</b>${x.zysk_pkt ? ` – <span class="znacznik z-startujemy">+${x.zysk_pkt} pkt</span>` : ""}${x.kryterium ? ` <small class="opis">(${esc(x.kryterium)})</small>` : ""}${x.koszt_zmiany ? ` <small class="opis">koszt: ${esc(x.koszt_zmiany)}</small>` : ""}</li>`).join("")}</ul>` : ""}
      ${(kon.uwagi || []).map(u => `<div class="alert-k ${u.waga === "krytyczna" ? "ostrzezenie" : ""}"><div class="alert-gora"><span class="znacznik ${u.waga === "krytyczna" ? "z-czerwony" : u.waga === "istotna" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(u.waga || "")}</span>
        ${u.odw ? odwChip(u.odw, u.miejsce || "regulamin", {typ: "projekt", id: P.id}) : u.miejsce ? `<small class="opis">${esc(u.miejsce)}</small>` : ""}</div>
        <div>${esc(u.opis || "")}</div>${u.propozycja ? `<div class="sugestia"><b>Co zrobić:</b> ${esc(u.propozycja)}</div>` : ""}</div>`).join("")}` : ""}
    <p class="opis">Dokumenty wniosku (krok 4) program przygotuje z tego zakresu: opis projektu, zestawienie rzeczowo-finansowe, wskaźniki i harmonogram.</p>
    <div class="pasek"><button class="maly" data-ik="portfel" onclick="doRozliczeniaPlanu()">Dotacja przyznana – przejdź do rozliczenia</button></div>` : ""}
  </div></div>` : `
  <div class="krok k-ziel" id="sek-plan"><div class="tytul"><span class="nr">${ik("teczka")}</span><h3>Plan projektu – zakupy, wskaźniki, trwałość</h3>
    <span class="stan">dotacja ${plZl(b.suma.dotacja)}</span></div><div class="tresc">
    <h4 class="grupa-analizy">Zakupy i wybór wykonawców</h4>
    <p class="opis">Tryb wyboru wykonawcy program ustala po zsumowaniu zamówień tożsamych – pozycji z tej samej grupy CPV albo (bez kodu) tej samej kategorii: zasada konkurencyjności powyżej 80 000 zł netto, ustawa Pzp od 170 000 zł netto u zamawiającego publicznego.</p>
    ${(P.wybor_ostrzezenia || []).map(t => `<div class="ramka-uwaga">${esc(t)}</div>`).join("")}
    <div class="tabela-okno"><table class="tabela"><tr><th>Pozycja</th><th>Wartość netto</th><th>Jak wybrać wykonawcę</th><th></th></tr>
      ${(p.pozycje || []).map(x => { const wy = P.wybor[x.id] || {}, zq = P.zapytania[x.id];
        return `<tr><td><b>${esc(x.nazwa || "")}</b><br><small class="opis">${esc(katNaz(x.kategoria))}</small></td><td class="liczba">${plZl(((b.wiersze || []).find(w => w.id === x.id) || {}).netto || 0)}</td>
          <td><span class="znacznik ${wy.tryb === "zasada konkurencyjności" || wy.tryb === "Pzp" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(wy.tryb || "")}</span><br><small class="opis">${esc(wy.opis || "")}</small></td>
          <td>${wy.tryb === "zasada konkurencyjności" ? (zq ? `<button class="maly" onclick="ZQ_ID='${zq}'; pokaz('dot_zapytania')">Otwórz zapytanie</button>` : `<button class="maly" data-ik="plus" onclick="zapytanieZPozycji('${x.id}')">Utwórz zapytanie ofertowe</button>`)
            : wy.tryb === "Baza Usług Rozwojowych" ? `<a class="przycisk maly" href="https://uslugirozwojowe.parp.gov.pl/" target="_blank" rel="noopener">Baza Usług Rozwojowych ↗</a>` : ""}</td></tr>`; }).join("")}</table></div>
    <h4 class="grupa-analizy">Wskaźniki – plan i wykonanie</h4>
    <div class="tabela-okno"><table class="tabela"><tr><th>Wskaźnik</th><th>Plan</th><th>Osiągnięto</th></tr>
      ${P.wskazniki.map(w => `<tr><td>${esc(w.nazwa)}</td><td class="liczba">${w.wartosc} ${esc(w.jednostka)}</td><td><input data-osiag="${esc(w.nazwa)}" style="width:110px" value="${esc((p.wskazniki_osiagniete || {})[w.nazwa] || "")}"></td></tr>`).join("")}</table></div>
    <div class="siatka"><label>Data płatności końcowej (albo zakończenia projektu)<input type="date" id="pl-koniec" value="${esc(p.data_konca || "")}"></label></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszRozliczeniePlanu()">Zapisz</button></div>
    ${P.trwalosc && P.trwalosc.do ? `<h4 class="grupa-analizy">Okres trwałości: ${P.trwalosc.lata} lat (do ${esc(dataPl(P.trwalosc.do))})</h4>
      <p class="opis">Sprawozdania / przypomnienia: ${P.trwalosc.przypomnienia.map(dataPl).join(" · ")}${P.trwalosc.uwaga ? `<br>${esc(P.trwalosc.uwaga)}` : ""}</p><ul class="lista">${P.trwalosc.zakazy.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
  </div></div>`;
  wstawIkony(el);
  podpowiedziKrok2();
  setTimeout(odswiezPodmenu, 100);
}
// krok 2 („Wymagania naboru i dane projektu”): „?” przy polach i podpowiedzi wyliczone z zakresu projektu (krok 3)
function propozycjeKrok2() {
  const P = DPL, p = P.plan, poz = p.pozycje || [], b = P.budzet, K = P.katalog;
  if (!poz.length) return {};
  const nazwyKat = [...new Set(poz.map(x => (K[x.kategoria] || {}).nazwa).filter(Boolean))];
  const mies = Math.max(...P.harmonogram.map(h => h.do), 1);
  const wsk = P.wskazniki.map(w => `${w.nazwa.toLowerCase()}: ${String(w.wartosc).replace(".", ",")} ${w.jednostka}`);
  const opis = `${p.pomysl ? p.pomysl.trim().replace(/\.?$/, ".") + " " : ""}Projekt obejmuje: ${poz.map(x => x.nazwa + ((+x.ilosc || 1) > 1 ? ` (${x.ilosc} szt.)` : "")).join("; ")}.`
    + ` Zakres: ${nazwyKat.join(", ").toLowerCase()}.` + (wsk.length ? ` Planowane efekty: ${wsk.join("; ")}.` : "")
    + ` Koszt całkowity ${zl(b.suma.brutto)}, wnioskowana dotacja ${zl(b.suma.dotacja)}.`;
  const prof = P.profil || {};
  return {"wd-opis": opis, "wd-koszt": b.suma.brutto ? String(b.suma.brutto) : "", "wd-kwota": b.suma.dotacja ? String(b.suma.dotacja) : "",
          "wd-okres": `${mies} ${mies === 1 ? "miesiąc" : mies < 5 ? "miesiące" : "miesięcy"} od podpisania umowy o dofinansowanie`,
          "wd-lok": P.adres_firmy || prof.adres || ""};
}
function podpowiedziKrok2() {
  const pola = {"wd-opis": "opis_projektu", "wd-koszt": "koszt_calkowity", "wd-kwota": "kwota_wnioskowana", "wd-okres": "okres_realizacji", "wd-lok": "lokalizacja"};
  const prop = propozycjeKrok2();
  Object.entries(pola).forEach(([id, klucz]) => {
    const inp = $("#" + id); if (!inp) return;
    const lab = inp.closest("label");
    if (lab && !lab.querySelector(".pom-ik")) {
      const t = lab.firstChild; const sp = document.createElement("span"); sp.className = "lab-pom";
      sp.textContent = t && t.nodeType === 3 ? t.textContent : ""; if (t && t.nodeType === 3) lab.replaceChild(sp, t); else lab.prepend(sp);
      sp.insertAdjacentHTML("beforeend", pomBtn(klucz));
    }
    const stare = lab && lab.querySelector(".pod-krok2"); if (stare) stare.remove();
    if (lab && prop[id] && String(inp.value).trim() !== String(prop[id]).trim()) {
      lab.insertAdjacentHTML("beforeend", `<div class="pod-krok2"><span>Podpowiedź z zakresu projektu: <b>${esc(id === "wd-koszt" || id === "wd-kwota" ? zl(+prop[id]) : prop[id].length > 160 ? prop[id].slice(0, 160) + "…" : prop[id])}</b></span>
        <button type="button" class="maly" onclick="$('#${id}').value = propozycjeKrok2()['${id}']; this.parentNode.remove()">Wstaw</button></div>`);
    }
  });
  const pasek = $("#wd-opis") && $("#wd-opis").closest(".tresc");
  if (pasek && !pasek.querySelector(".pod-krok2-info")) {
    pasek.querySelector(".siatka")?.insertAdjacentHTML("beforebegin", Object.keys(prop).length
      ? `<div class="pod-krok2-info pasek"><span class="opis" style="margin:0">Program może wpisać dane z kroku 3 „Zakres projektu”.</span>
          <button type="button" class="maly zolty" onclick="Object.entries(propozycjeKrok2()).forEach(([i, v]) => { if (v && $('#' + i)) $('#' + i).value = v; }); document.querySelectorAll('.pod-krok2').forEach(e => e.remove()); komunikat('Wpisano dane z zakresu projektu – sprawdź i kliknij Zapisz / Ustal wymagania.')">Wypełnij z zakresu projektu</button></div>`
      : `<div class="pod-krok2-info opis">Nie wiesz, co wpisać? Uzupełnij najpierw krok 3 <a href="#" onclick="document.getElementById('sek-plan')?.scrollIntoView({behavior:'smooth'}); return false">„Zakres projektu”</a> – program sam podpowie opis, koszt, kwotę dotacji i okres realizacji.</div>`);
  }
}
// ---------- kalkulator SO: uprawy (ha) i zwierzęta (szt.) × współczynniki regionu FADN
let SOD = null, SO_STAN = null;
async function otworzSO() {
  if ($("#so-panel").innerHTML) { $("#so-panel").innerHTML = ""; return; }
  SOD = await bezpiecznie(() => api("/api/dotacje/so")); if (!SOD) return;
  const d = SOD.dane || {};
  SO_STAN = {woj: d.woj || "dolnośląskie", wersja: d.wersja || "SO 2017", uprawy: (d.uprawy || []).length ? d.uprawy : [{nazwa: "", ha: ""}],
             zwierzeta: (d.zwierzeta || []).length ? d.zwierzeta : [{nazwa: "", sztuk: ""}]};
  rysujSO();
}
const regionSO = woj => Object.entries(SOD.regiony).find(([, L]) => L.includes(woj))?.[0] || "";
const wspSO = () => SOD.wspolczynniki[`${regionSO(SO_STAN.woj)}|${SO_STAN.wersja}`] || null;
function zbierzSO() {
  if (!$("#so-woj")) return;
  SO_STAN.woj = $("#so-woj").value; SO_STAN.wersja = $("#so-wersja").value;
  SO_STAN.uprawy = [...document.querySelectorAll(".so-u")].map(r => ({nazwa: r.querySelector("select").value, ha: r.querySelector(".so-il").value, wsp: r.querySelector(".so-w").value}));
  SO_STAN.zwierzeta = [...document.querySelectorAll(".so-z")].map(r => ({nazwa: r.querySelector("select").value, sztuk: r.querySelector(".so-il").value, wsp: r.querySelector(".so-w").value}));
}
function liczSO() {
  const W = wspSO() || {}; let suma = 0;
  const wiersz = (x, il, tab) => { const k = +String(x.wsp || (W[tab] || {})[x.nazwa] || 0).replace(",", "."); const v = (+String(il || 0).replace(",", ".")) * k; suma += v; return {k, v}; };
  SO_STAN.uprawy.forEach(x => x._w = wiersz(x, x.ha, "uprawy")); SO_STAN.zwierzeta.forEach(x => x._w = wiersz(x, x.sztuk, "zwierzeta"));
  return suma;
}
function rysujSO() {
  const W = wspSO(), reg = regionSO(SO_STAN.woj), suma = liczSO();
  const opcje = (L, v) => `<option value=""></option>` + L.map(o => `<option ${o === v ? "selected" : ""}>${esc(o)}</option>`).join("");
  const wiersz = (x, kl, L, pole, jedn) => `<div class="${kl} so-wiersz"><select onchange="this.parentNode.querySelector('.so-w').value = ''; zbierzSO(); rysujSO()">${opcje(L, x.nazwa)}</select>
    <input class="so-il" inputmode="decimal" placeholder="${jedn}" value="${esc(x[pole] ?? "")}" onchange="zbierzSO(); rysujSO()">
    <input class="so-w" inputmode="decimal" placeholder="${(((wspSO() || {})[kl === "so-u" ? "uprawy" : "zwierzeta"] || {})[x.nazwa]) || "wsp. EUR"}" title="Współczynnik SO (EUR na ${jedn}) – puste = z tabeli regionu" value="${esc(x.wsp || "")}" onchange="zbierzSO(); rysujSO()">
    <span class="so-wyn">${x._w && x._w.k ? zl(x._w.v).replace("zł", "€") : x.nazwa ? '<small class="opis">brak wsp.</small>' : ""}</span></div>`;
  $("#so-panel").innerHTML = `<div class="karta so-karta"><div class="pasek" style="margin:0 0 6px"><b>Kalkulator wielkości ekonomicznej (SO)</b>
      <button class="maly" style="margin-left:auto" onclick="$('#so-panel').innerHTML=''">Zamknij</button></div>
    <p class="opis" style="margin:0 0 8px">Wpisz uprawy (ha) i zwierzęta (średnia liczba sztuk w roku). SO = suma (ha × współczynnik) + suma (sztuki × współczynnik). Współczynniki zależą od regionu.</p>
    <div class="siatka"><label>Województwo<select id="so-woj" onchange="zbierzSO(); rysujSO()">${WOJ.filter(w => w !== "cała Polska").map(w => `<option ${w === SO_STAN.woj ? "selected" : ""}>${w}</option>`).join("")}</select></label>
      <label>Wersja współczynników<select id="so-wersja" onchange="zbierzSO(); rysujSO()">${["SO 2017", "SO 2013", "SO 2010"].map(w => `<option ${w === SO_STAN.wersja ? "selected" : ""}>${w}</option>`).join("")}</select></label></div>
    <p class="opis" style="margin:4px 0">Region FADN: <b>${esc(reg || "–")}</b>. Wersję współczynników wskazuje regulamin naboru (dawniej w PROW: „SO 2010”).
      ${W ? `Współczynniki: ${esc(W.zrodlo || "")}${W.zrodlo_url ? ` <a href="${esc(W.zrodlo_url)}" target="_blank" rel="noopener">źródło ↗</a>` : ""} (${esc(W.data || "")}).` : ""}</p>
    <div class="pasek"><button class="${W ? "maly" : "zolty"}" data-ik="iskra" onclick="pobierzWspSO()">${W ? "Pobierz współczynniki ponownie" : "Pobierz współczynniki dla regionu (AI)"}</button>
      <span class="opis" style="margin:0">albo wpisz je ręcznie z oficjalnego arkusza.</span></div>
    <h4 class="grupa-analizy">Uprawy [ha]</h4>${SO_STAN.uprawy.map(x => wiersz(x, "so-u", SOD.uprawy, "ha", "ha")).join("")}
    <button class="maly" data-ik="plus" onclick="zbierzSO(); SO_STAN.uprawy.push({nazwa:'', ha:''}); rysujSO()">Dodaj uprawę</button>
    <h4 class="grupa-analizy">Zwierzęta [sztuki średniorocznie]</h4>${SO_STAN.zwierzeta.map(x => wiersz(x, "so-z", SOD.zwierzeta, "sztuk", "szt.")).join("")}
    <button class="maly" data-ik="plus" onclick="zbierzSO(); SO_STAN.zwierzeta.push({nazwa:'', sztuk:''}); rysujSO()">Dodaj zwierzęta</button>
    <div class="so-wynik">Wielkość ekonomiczna (SO): <b>${zl(suma).replace("zł", "EUR")}</b></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszSO()">Wpisz wynik do profilu</button>
      <a class="przycisk maly" href="https://www.gov.pl/web/arimr/kalkulator-obliczania-wielkosci-ekonomicznej-gospodarstw-so" target="_blank" rel="noopener">Arkusz ARiMR ↗</a></div>
    <p class="opis" style="font-size:12px">Wynik ma charakter poglądowy – przy wniosku obowiązuje wyliczenie według dokumentacji naboru ARiMR. Współczynniki pobrane z internetu sprawdź ze źródłem.</p></div>`;
  wstawIkony($("#so-panel"));
}
async function pobierzWspSO() {
  zbierzSO();
  sledz(await bezpiecznie(() => api("/api/dotacje/so/wspolczynniki", {json: {region: regionSO(SO_STAN.woj), wersja: SO_STAN.wersja}})),
    async () => { const d = await api("/api/dotacje/so").catch(() => null); if (d) { SOD.wspolczynniki = d.wspolczynniki; rysujSO(); } });
}
async function zapiszSO() {
  zbierzSO();
  const r = await bezpiecznie(() => api("/api/dotacje/so/oblicz", {json: {region: regionSO(SO_STAN.woj), wersja: SO_STAN.wersja, woj: SO_STAN.woj,
    uprawy: SO_STAN.uprawy.map(({nazwa, ha, wsp}) => ({nazwa, ha, wsp})), zwierzeta: SO_STAN.zwierzeta.map(({nazwa, sztuk, wsp}) => ({nazwa, sztuk, wsp})), zapisz: true}}));
  if (!r) return;
  const inp = document.querySelector('[data-prof="wielkosc_ekonomiczna"]'); if (inp) inp.value = Math.round(r.so);
  DPL.profil.wielkosc_ekonomiczna = String(Math.round(r.so));
  komunikat(`Wielkość ekonomiczna: ${Math.round(r.so).toLocaleString("pl-PL")} EUR – wpisana do profilu.` + (r.braki.length ? ` Brak współczynników dla: ${r.braki.join(", ")}.` : ""));
}
function zbierzPlan() {
  const poz = [...document.querySelectorAll("#pl-pozycje .pl-poz")].map(k => {
    const x = (DPL.plan.pozycje || []).find(q => q.id === k.dataset.id) || {id: k.dataset.id, kategoria: k.dataset.kat};
    const a = {};
    k.querySelectorAll("[data-pole]").forEach(e => { if (e.value !== "") a[e.dataset.pole] = e.value; });
    k.querySelectorAll("[data-multi]").forEach(e => { a[e.dataset.multi] = a[e.dataset.multi] || []; if (e.checked) a[e.dataset.multi].push(e.value); });
    const g = {}; k.querySelectorAll("[data-pole-glowne]").forEach(e => g[e.dataset.poleGlowne] = e.value);
    return {...x, ...g, atrybuty: a};
  });
  const profil = {typ: ($("#pl-typ") || {}).value || ""}; document.querySelectorAll("[data-prof]").forEach(e => profil[e.dataset.prof] = e.value);
  const reczne = {}; document.querySelectorAll("[data-recz]").forEach(e => reczne[e.dataset.recz] = e.type === "checkbox" ? e.checked : e.value);
  return {pozycje: poz, pomysl: ($("#pl-pomysl") || {}).value || "", profil, reczne};
}
async function zapiszPlan(cicho) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan`, {json: zbierzPlan()})); if (r) { DPL = r; rysujPlan(); if (!cicho) komunikat("Zapisano zakres – budżet, wskaźniki i harmonogram przeliczone."); }
}
async function dodajPozPlanu(kat, dz, nazwa) {
  const dane = zbierzPlan(); dane.pozycje.push({id: "", kategoria: kat, dzialanie: dz, nazwa: nazwa || (DPL.katalog[kat] || {}).nazwa || "", ilosc: 1, atrybuty: {}});
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan`, {json: dane})); if (r) { DPL = r; rysujPlan(); const k = [...document.querySelectorAll(".pl-poz")].pop(); if (k) k.scrollIntoView({behavior: "smooth", block: "center"}); }
}
async function usunPozPlanu(id) {
  if (!confirm("Usunąć pozycję?")) return;
  const dane = zbierzPlan(); dane.pozycje = dane.pozycje.filter(x => x.id !== id);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan`, {json: dane})); if (r) { DPL = r; rysujPlan(); }
}
async function analizaPlanu() { await zapiszPlan(true); sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/analiza`, {method: "POST"})), ladujPlan); }
async function wycenaPlanu() { await zapiszPlan(true); sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/wycena`, {json: {ids: []}})), ladujPlan); }
async function kontrolaPlanu() { await zapiszPlan(true); sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/kontrola`, {method: "POST"})), ladujPlan); }
async function kosztorysPozycji(id) {
  await zapiszPlan(true);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/kosztorys`, {json: {id}})); if (!r) return;
  komunikat("Utworzono kosztorys z opisem zakresu – przygotuj go w Kosztorysowaniu, a wartość netto wpisz jako cenę pozycji.");
  TRYB = "kosztorys"; PROJEKT_ID = r.id; pokaz("kosztorys");
}
async function doRozliczeniaPlanu() {
  if (!confirm("Dotacja została przyznana? Program utworzy projekt rozliczenia z tym zakresem, wskaźnikami i harmonogramem.")) return;
  await zapiszPlan(true);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/do-rozliczenia`, {method: "POST"})); if (!r) return;
  TRYB = "dotacja"; PROJEKT_ID = r.id; pokaz("dot_projekty");
}
async function zapytanieZPozycji(id) {
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan/zapytanie`, {json: {id}})); if (!r) return;
  ZQ_ID = r.id; pokaz("dot_zapytania");
}
async function zapiszRozliczeniePlanu() {
  const osi = {}; document.querySelectorAll("[data-osiag]").forEach(e => osi[e.dataset.osiag] = e.value);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/plan`, {json: {wskazniki_osiagniete: osi, data_konca: ($("#pl-koniec") || {}).value || ""}}));
  if (r) { DPL = r; rysujPlan(); komunikat("Zapisano."); }
}
async function naborZLinku() {
  const url = $("#ds-link").value.trim(); if (!url) return komunikat("Wklej link do strony naboru.", true);
  sledz(await bezpiecznie(() => api("/api/dotacje/z-linku", {json: {url}})), () => { if (WIDOK === "dot_szukaj") rysujSzukajDotacji(); });
}
async function szukajDotacji() {
  const k = {branza: $("#ds-branza").value, region: $("#ds-region").value, wnioskodawca: $("#ds-wn").value, slowa: $("#ds-slowa").value,
    pomysl: ($("#ds-pomysl") || {}).value || "", odswiez: $("#ds-odswiez").checked};
  sledz(await bezpiecznie(() => api("/api/dotacje/szukaj", {json: k})), () => { if (WIDOK === "dot_szukaj") rysujSzukajDotacji(); });
}
async function uzyskajDotacje(nabor) {
  const w = await bezpiecznie(() => api("/api/dotacje/wniosek", {json: {nabor}})); if (!w) return;
  komunikat("Utworzono wniosek – pobieram dokumenty naboru.");
  TRYB = "wniosek_dot"; PROJEKT_ID = w.id; pokaz("dot_wnioski");
  if (w.zadanie) sledz({id: w.zadanie, opis: "Pobieranie dokumentów naboru", status: "trwa", log: []}, odswiezProjekt);
}
async function dodajLinkNaboru() {
  const url = $("#wd-link").value.trim(); if (!url) return komunikat("Wklej link.", true);
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wniosek-dot/link`, {json: {url}})), odswiezProjekt);
}
// ---------- widok szybki projektu z przetargu: przetarg → kosztorys → oferta → komplet
function coDalejHtml(kroki, gotowe = "<b>Oferta gotowa</b> – komplet do złożenia.") {  // wspólny wzorzec: pasek kroków ze ✓ i „Co dalej”
  const dalej = kroki.find(k => !k[2]);
  return `<div class="kz-stepper" style="margin:6px 0 4px">${kroki.map(([id, t, ok], k) => `<button class="kz-krok ${ok ? "ok" : ""} ${dalej && dalej[0] === id ? "akt" : ""}" onclick="document.getElementById('${id}')?.scrollIntoView({behavior: 'smooth'})"><span>${ok ? "✓" : k + 1}</span>${esc(t)}</button>`).join("")}</div>
    <p class="opis" style="margin:0 0 8px">${dalej ? `<b>Co dalej:</b> ${esc(dalej[1])} – <a href="#" onclick="document.getElementById('${dalej[0]}')?.scrollIntoView({behavior: 'smooth'}); return false">przejdź</a>` : gotowe}</p>`;
}
function poWygranej(p) {
  const pr = $("#projekt"); if (!pr || pr.querySelector(".po-wygr")) return;  // raz na wyrenderowany widok
  // „Oferta” i „Po wygranej”: materiały, harmonogram dostaw i hurtownie pojawiają się po wygranej (albo na żądanie)
  const wygrany = !!p.status_projektu || /wygr/i.test(JSON.stringify(p.wynik_oferty || "")), naZadanie = localStorage.getItem("po_wygranej_" + p.id) === "1";
  const po = [...pr.querySelectorAll(":scope > .krok")].filter(k => /Zapotrzebowanie|Harmonogram i podział|Zamówienia do hurtowni/.test(k.querySelector("h3")?.textContent || ""));
  if (po.length) {
    if (!wygrany && !naZadanie) {
      po.forEach(k => k.style.display = "none");
      po[0].insertAdjacentHTML("beforebegin", `<div class="karta po-wygr" style="margin:10px 0;border-left:4px solid #1F5A99"><b>Po wygranej</b> <span class="opis">– zapotrzebowanie materiałowe, harmonogram dostaw i zamówienia do hurtowni pojawią się po oznaczeniu przetargu jako wygranego.</span>
        <button class="maly" onclick="localStorage.setItem('po_wygranej_${p.id}', '1'); odswiezProjekt()">Pokaż teraz</button></div>`);
    } else {
      po.forEach(k => k.classList.remove("zaaw"));
      if (wygrany) [...pr.querySelectorAll(":scope > .krok")].filter(k => k.id === "sek-wnioski" || /Wnioski i aneksy|Zmiany umowy/.test(k.querySelector("h3")?.textContent || ""))
        .forEach(k => k.classList.remove("zaaw"));  // projekt w realizacji: zmiany umowy widoczne także w widoku szybkim
      po[0].insertAdjacentHTML("beforebegin", `<h3 class="grupa-analizy po-wygr" style="margin:16px 0 6px">Po wygranej – materiały, dostawy, hurtownie</h3>`);
    }
  }
}
function widokSzybki(p) {
  const dost = ["dostawy", "uslugi"].includes(p.rodzaj_zamowienia);
  const szybki = dost || (localStorage.getItem("widok_przetargu") || "szybki") === "szybki", pr = $("#projekt");
  pr.classList.toggle("widok-szybki", szybki);
  [...pr.querySelectorAll(":scope > .krok")].forEach(k => { const t = k.querySelector("h3")?.textContent || "";
    if (/Zapotrzebowanie|Harmonogram i podział|Zamówienia do hurtowni|Asystent|Wnioski i aneksy|Zmiany umowy/.test(t) || k.id === "sek-wnioski") k.classList.add("zaaw"); });
  pr.querySelectorAll("#popraw-pozycje").forEach(e => e.closest(".etap-b")?.classList.add("zaaw"));
  pr.querySelectorAll("#sek-kosztorys .kontrola, #sek-przeglad").forEach(e => e.classList.add("zaaw"));
  const ile = pr.querySelectorAll(".zaaw").length;
  if (pr.querySelector(".pasek-sekcji")) paskiSekcji();
  if (dost) {  // dostawy i usługi: 1 dokumenty → 2 analiza i błędy → 3 formularz cenowy → 4 dokumenty wykonawcy → 5 złożenie oferty
    pr.insertAdjacentHTML("afterbegin", `<div class="widok-przelacznik"><span><b>${p.rodzaj_zamowienia === "uslugi" ? "Oferta usługodawcy" : "Oferta dostawcy"}:</b>
      dokumenty → analiza i błędy → formularz cenowy → dokumenty wykonawcy → złożenie oferty</span></div>`);
    const kroki = [...pr.querySelectorAll(":scope > .krok")];
    const k1 = kroki[0], k2 = kroki.find(k => /Kosztorys i oferta/.test(k.querySelector("h3")?.textContent || ""));
    const k3 = kroki.find(k => /Dokumenty wykonawcy/.test(k.querySelector("h3")?.textContent || ""));
    pr.classList.add("widok-szybki");
    kroki.forEach(k => { if (k === k1 || k === k3) return;
      if (/Zapotrzebowanie|Harmonogram i podział|Zamówienia do hurtowni/.test(k.querySelector("h3")?.textContent || "")) k.remove();  // budowlane – nie dotyczą dostawcy
      else k.classList.add("zaaw"); });
    const krok = (id, nr, tytul, kol) => `<div class="krok ${kol}" id="${id}"><div class="tytul"><span class="nr">${nr}</span><h3>${tytul}</h3><span class="stan" id="${id}-stan"></span></div>
      <div class="tresc" id="${id}-tresc"><p class="opis">Ładuję…</p></div></div>`;
    k1.insertAdjacentHTML("afterend", krok("sek-analiza-d", 2, "Analiza przetargu i błędy w dokumentach", "k-nieb") + krok("sek-formularz", 3, "Formularz cenowy – co zaoferować i za ile", "k-ziel"));
    if (k3) { const h = k3.querySelector("h3"); if (h) h.textContent = "Dokumenty wykonawcy do oferty"; const n = k3.querySelector(".nr"); if (n) n.textContent = "4"; }
    (k3 || pr.lastElementChild).insertAdjacentHTML("afterend", krok("sek-zlozenie", 5, "Złożenie oferty", "k-zolt"));
    if (pr.querySelector(".pasek-sekcji")) paskiSekcji();
    ladujFormularzCenowy(p);
    return;
  }
  poWygranej(p);
  const krW = [["sek-dokumenty", "Dokumenty przetargu", (p.pliki || []).length > 0], ["sek-weryfikacja", "Błędy i ryzyka", !!p.weryfikacja],
               ["sek-kosztorys", "Kosztorys i oferta", !!p.oferta],
               ["sek-dok-wyk", (p.komplet?.braki || []).length ? `Uzupełnij komplet – brakuje: ${p.komplet.braki.slice(0, 3).join("; ")}` : "Dokumenty do oferty i komplet",
                !!p.komplet && !(p.komplet.braki || []).length]];
  pr.insertAdjacentHTML("afterbegin", coDalejHtml(krW, "<b>Komplet gotowy</b> – podpisz dokumenty wymaganym podpisem elektronicznym i złóż ofertę na platformie przed terminem."));
  // telefon: zrobione kroki zwinięte (dotknij nagłówka, żeby rozwinąć) – strona oferty nie ciągnie się na dziesiątki ekranów
  if (window.matchMedia("(max-width: 820px)").matches) {
    krW.filter(k => k[2]).forEach(([id]) => { const k = document.getElementById(id); if (!k || k.dataset.zw) return;
      k.dataset.zw = "1"; k.classList.add("zwijany", "zwiniety");
      k.querySelector(":scope > .tytul")?.addEventListener("click", () => k.classList.toggle("zwiniety")); });
  }
  pr.insertAdjacentHTML("afterbegin", `<div class="widok-przelacznik"><span>${szybki ? `<b>Widok szybki:</b> przetarg → kosztorys → oferta → komplet (ukryto ${pr.querySelectorAll(".zaaw").length} sekcji dodatkowych)` : "<b>Widok pełny:</b> wszystkie kroki i narzędzia"}</span>
    <button class="maly" onclick="localStorage.setItem('widok_przetargu', '${szybki ? "pelny" : "szybki"}'); odswiezProjekt()">${szybki ? "Pokaż wszystkie kroki" : "Przełącz na widok szybki"}</button></div>`);
}

// ---------- kalkulator szans wygranej i wynik złożonej oferty
function parametryRynku(h) {  // rozrzut ofert w podobnych przetargach: najniższa i najwyższa względem środka przedziału
  const L = (h?.lista_podobnych || []).filter(w => w.najnizsza && w.najwyzsza && w.najwyzsza >= w.najnizsza);
  const med = x => { const s = [...x].sort((a, b) => a - b); return s.length ? (s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2) : null; };
  const a = med(L.map(w => w.najnizsza / ((w.najnizsza + w.najwyzsza) / 2))), b = med(L.map(w => w.najwyzsza / ((w.najnizsza + w.najwyzsza) / 2)));
  const ofert = h?.podobne?.srednia_ofert || h?.wszystkie?.srednia_ofert;
  return {a: a || 0.85, b: b || 1.15, n: L.length, konkurentow: Math.max(1, Math.round((ofert || 4) - 1)), z_danych: L.length >= 2};
}
const szansa = (x, M, r, k) => { const lo = r.a * M, hi = r.b * M; const F = Math.min(1, Math.max(0, (x - lo) / Math.max(1, hi - lo))); return Math.pow(1 - F, k); };
const cenaDlaSzansy = (P, M, r, k) => r.a * M + (1 - Math.pow(P, 1 / k)) * (r.b - r.a) * M;
let SZ = null;
function rysujSzanse(p) {
  const el = $("#pr-szanse"); if (!el) return;
  const o = p.oferta, h = p.historia_zam, wyn = p.wynik_oferty, dostS = ["dostawy", "uslugi"].includes(p.rodzaj_zamowienia);
  let html = "";
  if (dostS) {}
  else if (o && h && (h.wszystkie || {}).liczba) {
    const r = parametryRynku(h), M = o.brutto_rynkowe || o.brutto, bud = p.kwota_zamawiajacego || null;  // kwota brutto na sfinansowanie (art. 222 ust. 4) – wpisuje wykonawca; nie szacowana wartość netto ani szacunek AI
    SZ = {M, r, k: r.konkurentow, x: o.brutto, bud, netto_do_brutto: o.netto ? o.brutto / o.netto : 1.23};
    html += `<div class="karta szanse"><div class="polecane-gora"><b>${ik("procent")} Kalkulator szans wygranej</b><span class="opis" style="margin:0">przy kryterium ceny</span></div>
      <p class="opis" style="margin:0 0 8px">Ceny konkurentów oszacowano z rozrzutu ofert w ${r.z_danych ? r.n + " podobnych przetargach u tego zamawiającego" : "typowych przetargach (za mało podobnych danych)"} wokół ceny rynkowej z Twojego kosztorysu (${zl(M)} brutto).</p>
      <div class="sz-uklad"><div class="sz-kolo" id="sz-kolo"></div>
        <div class="sz-sterowanie"><label>Twoja cena brutto: <b id="sz-cena"></b></label>
          <input type="range" id="sz-suwak" min="${Math.round(M * Math.min(r.a, 0.7))}" max="${Math.round(M * Math.max(r.b, 1.3))}" step="${Math.max(100, Math.round(M / 500))}" value="${Math.round(o.brutto)}" oninput="SZ.x = +this.value; liczSzanse()">
          <div class="siatka" style="grid-template-columns: 1fr 1fr"><label>Liczba konkurentów<input type="number" id="sz-k" min="1" max="30" value="${r.konkurentow}" onchange="SZ.k = Math.max(1, +this.value); liczSzanse()"></label>
            <label title="Kwota, jaką zamawiający przeznaczył na sfinansowanie zamówienia (brutto) – publikowana przed otwarciem ofert (art. 222 ust. 4 Pzp)">Kwota na sfinansowanie (brutto)<input id="sz-bud" value="${bud ? Math.round(bud) : ""}" placeholder="z informacji przed otwarciem" onchange="SZ.bud = parseFloat(this.value.replace(/[^\\d,]/g, '').replace(',', '.')) || null; liczSzanse()"></label></div>
          <div id="sz-wynik"></div>
          <div class="pasek"><button class="zielony" data-ik="procent" onclick="ustawCeneZKalkulatora()">Ustaw tę cenę w ofercie</button></div></div></div>
      <svg class="sz-wykres" id="sz-wykres" viewBox="0 0 600 150" preserveAspectRatio="none"></svg>
      <p class="opis" style="font-size:12px;margin:4px 0 0">Szacunek pomocniczy: zakłada, że pozostałe kryteria (np. gwarancja, termin) wypadną u wszystkich podobnie. Im więcej podobnych przetargów u zamawiającego, tym dokładniejszy wynik.</p></div>`;
  } else if (o) {
    html += `<div class="karta szanse"><b>${ik("procent")} Kalkulator szans wygranej</b><p class="opis" style="margin:4px 0 0">Kliknij powyżej <b>Konkurencja u zamawiającego</b> – na podstawie cen i liczby ofert w podobnych przetargach program policzy szansę wygranej dla Twojej ceny.</p></div>`;
  }
  if (o) {
    const w = (wyn || {}).wynik || {};
    const kol = {wygrana: "z-startujemy", przegrana: "z-czerwony", oczekuje: "z-do-analizy"}[w.status] || "z-odpuszczamy";
    html += `<div class="karta wynik-oferty"><div class="polecane-gora"><b>${ik("trofeum")} Wynik przetargu</b>${wyn ? `<span class="znacznik ${kol}">${esc(w.status === "oczekuje" ? "czeka na wynik" : w.status)}</span>` : ""}</div>
      ${!wyn ? `<p class="opis" style="margin:0 0 6px">Po złożeniu oferty zapisz ją tutaj – program sam sprawdzi wynik w BZP po terminie składania i doda go do zakładki <b>Wygrane i przegrane</b>.</p>
        <div class="pasek"><label>Cena złożonej oferty brutto <input id="wo-cena" value="${(+o.brutto || 0).toFixed(2).replace(".", ",")}" style="max-width:160px"></label>
          <button class="zielony" data-ik="flaga" onclick="ofertaZlozona()">Złożyłem ofertę</button></div>`
      : `<p style="margin:0">Twoja cena: <b>${zl(wyn.nasza_cena)}</b> brutto · złożona ${esc(dataPl(wyn.data_zlozenia))}</p>
        ${w.status && w.status !== "oczekuje" ? `<p style="margin:4px 0 0">${w.zwyciezca ? `Zwycięzca: <b>${esc(w.zwyciezca)}</b>` : ""}${w.cena_zwyciezcy ? ` · cena ${zl(w.cena_zwyciezcy)}` : ""}${w.ofert ? ` · ofert: ${w.ofert}` : ""}
          ${w.roznica_proc != null ? ` · <b class="${w.roznica_proc > 0 ? "czerwone" : ""}">Twoja oferta była ${w.roznica_proc > 0 ? "droższa" : "tańsza"} o ${Math.abs(w.roznica_proc).toString().replace(".", ",")}%</b>` : ""}
          <small class="opis"> (${esc(w.zrodlo || "")})</small></p>` : ""}
        <div class="pasek" style="margin-top:8px">${w.status === "oczekuje" ? `<button data-ik="szukaj" onclick="sprawdzWynik()">Sprawdź wynik w BZP</button>` : ""}
          <details><summary class="opis">wpisz wynik ręcznie</summary><div class="pasek"><select id="wo-st"><option value="wygrana">wygrana</option><option value="przegrana">przegrana</option><option value="unieważniony">unieważniony</option></select>
            <input id="wo-zw" placeholder="zwycięzca"><input id="wo-cz" placeholder="cena zwycięzcy brutto" style="max-width:150px"><input id="wo-of" placeholder="ofert" style="max-width:70px">
            <button class="maly" onclick="wynikReczny()">Zapisz</button></div></details>
          <button class="maly" onclick="if (confirm('Usunąć zapis złożonej oferty?')) api('/api/projekty/' + PROJEKT_ID + '/oferta-zlozona', {json: {cofnij: true}}).then(odswiezProjekt)">Cofnij</button></div>`}</div>`;
  }
  el.innerHTML = html; wstawIkony(el);
  if (SZ && $("#sz-suwak")) liczSzanse();
}
function liczSzanse() {
  const {M, r, k, x, bud} = SZ;
  const P = szansa(x, M, r, k), miejsce = 1 + k * Math.min(1, Math.max(0, (x - r.a * M) / ((r.b - r.a) * M)));
  $("#sz-cena").textContent = zl(x);
  const R = 34, OB = 2 * Math.PI * R, kol = P >= 0.6 ? "#16a34a" : P >= 0.3 ? "#1F5A99" : "#dc2626";
  $("#sz-kolo").innerHTML = `<svg viewBox="0 0 80 80"><circle cx="40" cy="40" r="${R}" fill="none" stroke="#EEF1F4" stroke-width="8"/>
    <circle cx="40" cy="40" r="${R}" fill="none" stroke="${kol}" stroke-width="8" stroke-linecap="round" stroke-dasharray="${OB}" stroke-dashoffset="${OB * (1 - P)}" transform="rotate(-90 40 40)"/></svg>
    <span><b>${Math.round(P * 100)}%</b><small>szansy</small></span>`;
  const c50 = cenaDlaSzansy(0.5, M, r, k), c70 = cenaDlaSzansy(0.7, M, r, k), c90 = cenaDlaSzansy(0.9, M, r, k);
  $("#sz-wynik").innerHTML = `<p style="margin:6px 0">Przewidywane miejsce: <b>${miejsce.toFixed(1).replace(".", ",")}</b> z ${k + 1} ofert ·
      różnica do ceny rynkowej: <b>${((x / M - 1) * 100).toFixed(1).replace(".", ",")}%</b></p>
    <p class="opis" style="margin:0">Cena dla szansy 50%: <a href="#" onclick="SZ.x=${Math.round(c50)};$('#sz-suwak').value=SZ.x;liczSzanse();return false">${zl(c50)}</a> ·
      70%: <a href="#" onclick="SZ.x=${Math.round(c70)};$('#sz-suwak').value=SZ.x;liczSzanse();return false">${zl(c70)}</a> ·
      90%: <a href="#" onclick="SZ.x=${Math.round(c90)};$('#sz-suwak').value=SZ.x;liczSzanse();return false">${zl(c90)}</a></p>
    ${bud && x > bud ? `<p class="czerwone" style="margin:4px 0 0">Cena przekracza kwotę zamawiającego (${zl(bud)}) – oferta może zostać odrzucona albo przetarg unieważniony.</p>` : ""}`;
  const lo = +$("#sz-suwak").min, hi = +$("#sz-suwak").max, X = v => (v - lo) / (hi - lo) * 600, Y = p => 140 - p * 130;
  let d = ""; for (let i = 0; i <= 60; i++) { const v = lo + (hi - lo) * i / 60; d += (i ? "L" : "M") + X(v).toFixed(1) + " " + Y(szansa(v, M, r, k)).toFixed(1); }
  $("#sz-wykres").innerHTML = `<path d="${d}" fill="none" stroke="#071F49" stroke-width="2.5"/>
    <line x1="${X(M)}" x2="${X(M)}" y1="5" y2="140" stroke="#94a3b8" stroke-dasharray="4 4"/><text x="${X(M) + 4}" y="16" font-size="11" fill="#64748b">cena rynkowa</text>
    ${bud && bud > lo && bud < hi ? `<line x1="${X(bud)}" x2="${X(bud)}" y1="5" y2="140" stroke="#dc2626" stroke-dasharray="4 4"/><text x="${X(bud) + 4}" y="30" font-size="11" fill="#dc2626">kwota zamawiającego</text>` : ""}
    <circle cx="${X(x)}" cy="${Y(P)}" r="6" fill="#1F5A99" stroke="#fff" stroke-width="2"/>`;
}
async function ustawCeneZKalkulatora() {
  if (!confirm(`Ustawić cenę oferty na ${zl(SZ.x)} brutto? Program proporcjonalnie przeliczy ceny jednostkowe kosztorysu.`)) return;
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/dostosuj`, {json: {tryb: "brutto", wartosc: Math.round(SZ.x * 100) / 100}}))) { komunikat("Ustawiono cenę oferty."); odswiezProjekt(); }
}
async function ofertaZlozona() {
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/oferta-zlozona`, {json: {cena_brutto: $("#wo-cena").value}}))) { komunikat("Zapisano złożoną ofertę – wynik sprawdzę w BZP po terminie."); odswiezProjekt(); }
}
async function sprawdzWynik() { sledz(await bezpiecznie(() => api("/api/wyniki-ofert/sprawdz", {json: {pid: PROJEKT_ID}})), odswiezProjekt); }
async function wynikReczny() {
  const d = {status: $("#wo-st").value, zwyciezca: $("#wo-zw").value, cena_zwyciezcy: $("#wo-cz").value, ofert: $("#wo-of").value};
  if (!(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wynik-oferty`, {json: d})))) return;
  komunikat("Zapisano wynik."); odswiezProjekt();
  if (d.status === "wygrana" && !(PROJEKT || {}).status_projektu && confirm("Gratulacje! Przenieść projekt do realizacji (budowa, raporty dzienne, rozliczenia)?")
      && await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/status`, {json: {status: "realizacja"}}))) doRealizacji(PROJEKT_ID, false);
}

// ---------- Wygrane i przegrane
async function rysujWyniki() {
  const d = await api("/api/wyniki-ofert").catch(() => null); if (!d) return;
  const s = d.stat, kz = v => v != null ? zl(v) : "–";
  const proc = v => v == null ? "–" : (v > 0 ? "+" : "") + String(v).replace(".", ",") + "%";
  const wnioski = [];
  if (s.srednia_roznica != null) wnioski.push(s.srednia_roznica > 0 ? `W przegranych przetargach Twoje oferty były średnio <b>o ${String(s.srednia_roznica).replace(".", ",")}% droższe</b> od zwycięskich.`
    : `W przegranych przetargach Twoje oferty były średnio tańsze od zwycięskich – przegrywasz raczej na innych kryteriach albo wymaganiach.`);
  d.grupy.filter(g => g.srednia_roznica != null && g.srednia_roznica > 3 && g.zlozone >= 2).forEach(g => wnioski.push(`<b>${esc(g.grupa)}</b>: średnio ${String(g.srednia_roznica).replace(".", ",")}% powyżej ceny zwycięzcy (${g.wygrane} z ${g.zlozone} wygranych).`));
  $("#wyniki").innerHTML = `<div class="pulpit-glowka"><h2>Wygrane i przegrane</h2><button class="maly" data-ik="szukaj" onclick="sprawdzWszystkieWyniki()">Sprawdź wyniki w BZP</button></div>
    <p class="opis">Złożone oferty zapisujesz w projekcie z przetargu („Złożyłem ofertę”). Po terminie składania program codziennie sprawdza w BZP ogłoszenia o wyniku i zapisuje zwycięzcę, jego cenę i różnicę do Twojej oferty.</p>
    <div class="kpi">${[["dokument", "Złożone oferty", s.zlozone, `czeka na wynik: ${s.oczekuje}`, "nieb"], ["trofeum", "Wygrane", s.wygrane, `z ${s.rozstrzygniete} rozstrzygniętych`, "ziel"],
      ["procent", "Skuteczność", s.skutecznosc != null ? s.skutecznosc + "%" : "–", "wygrane / rozstrzygnięte", "pom"], ["portfel", "Różnica do zwycięzcy", proc(s.srednia_roznica), "średnio w przegranych", "nieb"]].map(([i_, t, v, op, k]) =>
      `<div class="kpi-karta"><span class="kpi-ik k-${k}">${ik(i_)}</span><div><small>${t}</small><b>${v}</b><em style="color:var(--szary)">${op}</em></div></div>`).join("")}</div>
    ${!ADMIN() ? "" : `<div class="karta raport-pow"><div class="polecane-gora"><b>${ik("tabela")} Raport: kto wygrywa przetargi w powiatach (Excel)</b></div>
      <p class="opis" style="margin:0 0 8px">Program pobiera z BZP wszystkie ogłoszenia o wyniku dla wybranego województwa (zamawiający publiczni) oraz rozstrzygnięcia z Bazy Konkurencyjności (wspólnoty, spółdzielnie, firmy, organizacje realizujące projekty z funduszy UE), przypisuje zamawiających do powiatów
        i tworzy Excel: ranking zwycięzców w każdym powiecie (liczba wygranych, wartość, średnia liczba ofert, u jakich zamawiających), podsumowanie powiatów i listę wszystkich rozstrzygnięć.
        Pierwszy raport dla województwa trwa dłużej (pobieranie dzień po dniu); kolejne korzystają z pamięci programu.</p>
      <div class="pasek"><label>Województwo <select id="rp-woj">${WOJ.slice(1).map(w => `<option ${w === "dolnośląskie" ? "selected" : ""}>${w}</option>`).join("")}</select></label>
        <label>Okres <select id="rp-mies"><option value="6">6 miesięcy</option><option value="12" selected>12 miesięcy</option><option value="24">24 miesiące</option></select></label>
<span><b>Zakres:</b> <label class="check" style="display:inline-flex;margin:0 8px 0 4px"><input type="checkbox" class="rp-zakres" value="roboty" checked> roboty budowlane</label>
          <label class="check" style="display:inline-flex;margin:0 8px 0 0"><input type="checkbox" class="rp-zakres" value="uslugi" checked> usługi</label>
          <label class="check" style="display:inline-flex;margin:0"><input type="checkbox" class="rp-zakres" value="dostawy" checked> dostawy</label></span>
        <label class="check" style="margin:0"><input type="checkbox" id="rp-bk" checked> także Baza Konkurencyjności (wspólnoty, spółdzielnie, firmy, organizacje)</label>
        <label class="check" style="margin:0"><input type="checkbox" id="rp-nowa"> od podstaw – pobierz wszystkie dane ponownie, bez pamięci programu</label>
        <button class="glowny" data-ik="tabela" onclick="raportPowiatow()">Przygotuj raport Excel</button></div>
      <div id="rp-lista"></div>
      <details style="margin-top:10px"><summary class="opis"><b>Sprawdź ogłoszenie z Bazy Konkurencyjności</b> – co program odczytuje (zwycięzca, oferty)</summary>
        <div class="pasek" style="margin-top:6px"><input id="bk-link" placeholder="https://bazakonkurencyjnosci.funduszeeuropejskie.gov.pl/ogloszenia/…" style="flex:1;min-width:260px">
          <button data-ik="szukaj" onclick="sprawdzBk()">Sprawdź</button></div><div id="bk-diag"></div></details></div>`}
    ${wnioski.length ? `<div class="ramka-uwaga"><b>Wnioski:</b><ul class="lista">${wnioski.map(w => `<li>${w}</li>`).join("")}</ul></div>` : ""}
    ${d.grupy.length ? `<h4 class="grupa-analizy">Według rodzaju robót</h4><div class="tabela-okno"><table class="tabela"><tr><th>Rodzaj robót</th><th>Rozstrzygnięte</th><th>Wygrane</th><th>Śr. różnica do zwycięzcy</th></tr>
      ${d.grupy.map(g => `<tr><td>${esc(g.grupa)}</td><td class="liczba">${g.zlozone}</td><td class="liczba">${g.wygrane}</td><td class="liczba ${g.srednia_roznica > 0 ? "czerwone" : ""}">${proc(g.srednia_roznica)}</td></tr>`).join("")}</table></div>` : ""}
    <h4 class="grupa-analizy">Złożone oferty</h4>
    ${d.oferty.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Złożono</th><th>Przetarg</th><th>Twoja cena</th><th>Wynik</th><th>Zwycięzca</th><th>Cena zwycięzcy</th><th>Różnica</th><th>Ofert</th></tr>
      ${d.oferty.map(x => { const w = x.wynik || {}; return `<tr class="klik" onclick="otworzProjekt('${x.pid}')"><td>${esc(dataPl(x.data_zlozenia))}</td><td><b>${esc((x.przedmiot || "").slice(0, 80))}</b><br><small class="opis">${esc(x.zamawiajacy)}</small></td>
        <td class="liczba">${kz(x.nasza_cena)}</td><td><span class="znacznik ${{wygrana: "z-startujemy", przegrana: "z-czerwony", oczekuje: "z-do-analizy"}[w.status] || "z-odpuszczamy"}">${esc(w.status === "oczekuje" ? "czeka" : w.status)}</span></td>
        <td>${esc(w.zwyciezca || "–")}</td><td class="liczba">${kz(w.cena_zwyciezcy)}</td><td class="liczba ${w.roznica_proc > 0 ? "czerwone" : ""}">${proc(w.roznica_proc)}</td><td class="liczba">${w.ofert ?? "–"}</td></tr>`; }).join("")}</table></div>`
      : '<p class="pusto">Brak zapisanych ofert. W projekcie z przetargu kliknij „Złożyłem ofertę”.</p>'}`;
  wstawIkony($("#wyniki"));
  if (ADMIN()) listaRaportow();
}
async function raportPowiatow() {
  if (!document.querySelectorAll(".rp-zakres:checked").length) return komunikat("Zaznacz co najmniej jeden zakres zamówień.", true);
  sledz(await bezpiecznie(() => api("/api/raporty/zwyciezcy", {json: {wojewodztwo: $("#rp-woj").value, miesiecy: $("#rp-mies").value, bk: $("#rp-bk").checked,
    zakresy: [...document.querySelectorAll(".rp-zakres:checked")].map(x => x.value), od_nowa: $("#rp-nowa").checked}})),
    z => { if (z && z.status === "ok" && z.wynik && z.wynik.url) { komunikat("Raport gotowy – pobieram plik Excel."); location.href = z.wynik.url; } listaRaportow(); });
}
async function sprawdzBk() {
  const el = $("#bk-diag"); el.innerHTML = '<p class="opis">Sprawdzam…</p>';
  const w = await bezpiecznie(() => api("/api/bk/sprawdz", {json: {url: $("#bk-link").value}})); if (!w) { el.innerHTML = ""; return; }
  el.innerHTML = `<div class="karta" style="margin:8px 0 0">${w.wynik.length ? `<p class="zielone" style="margin:0"><b>Odczytano rozstrzygnięcie</b>${w.wynik[0].odczyt === "AI" ? " (przez AI)" : ""}:</p>
      <ul class="lista">${w.wynik.map(x => `<li>${x.uniewaznione ? "postępowanie unieważnione" : `<b>${esc(x.wykonawca)}</b>${x.nip ? " · NIP " + esc(x.nip) : ""}${x.siedziba ? " · " + esc(x.siedziba) : ""}${x.cena ? " · " + zl(x.cena) : ""}`}${x.ofert ? " · ofert: " + x.ofert : ""}</li>`).join("")}</ul>`
    : `<p class="czerwone" style="margin:0"><b>Nie odczytano zwycięzcy.</b> ${w.adresy.length ? "Pobierz dane ogłoszenia i prześlij plik – dopasuję odczyt." : "Baza Konkurencyjności nie zwróciła danych tego ogłoszenia."}</p>`}
    ${w.dodano ? `<p class="opis" style="margin:4px 0 0">Ogłoszenie dodano do danych raportu dla województwa <b>${esc(w.dodano)}</b> – pojawi się w następnym raporcie.</p>` : ""}
    <p class="opis" style="margin:6px 0 0;font-size:12px">Odpowiedziało adresów API: ${w.adresy.length}${w.klucze.length ? " · pola: " + esc(w.klucze.join(", ")) : ""}</p>
    ${w.surowe ? `<a class="przycisk maly dozw" data-ik="pobierz" href="${w.surowe}">Pobierz dane ogłoszenia (JSON)</a>` : ""}
    ${w.lista ? ` <a class="przycisk maly dozw" data-ik="pobierz" href="${w.lista}">Pobierz próbkę listy ogłoszeń BK (JSON)</a>` : ""}</div>`;
  wstawIkony(el);
}
async function listaRaportow() {
  const el = $("#rp-lista"); if (!el) return;
  const L = await api("/api/raporty").catch(() => []);
  el.innerHTML = L.length ? `<h4 class="grupa-analizy">Zapisane raporty (${L.length}) <button class="maly niebezp" data-ik="kosz" onclick="usunRaport(null)">Usuń wszystkie</button></h4>
    <ul class="lista">${L.map(r => `<li><a href="${r.url}">${esc(r.nazwa)}</a> <small class="opis">${esc(r.data)} · ${Math.round(r.rozmiar / 1024)} kB</small>
      <button class="maly" title="Usuń raport" onclick="usunRaport('${escA(r.nazwa)}')">×</button></li>`).join("")}</ul>` : "";
  wstawIkony(el);
}
async function usunRaport(nazwa) {
  if (!confirm(nazwa ? `Usunąć raport ${nazwa}?` : "Usunąć wszystkie zapisane raporty?")) return;
  if (await bezpiecznie(() => api("/api/raporty/usun", nazwa ? {json: {nazwa}} : {json: {wszystkie: true}}))) { komunikat("Usunięto."); listaRaportow(); }
}
async function sprawdzWszystkieWyniki() { sledz(await bezpiecznie(() => api("/api/wyniki-ofert/sprawdz", {json: {}})), () => { if (WIDOK === "wyniki") rysujWyniki(); }); }

// ---------- oferta dostawcy / usługodawcy: analiza (2), formularz cenowy (3), złożenie (5)
let FC = null;
async function ladujFormularzCenowy(p) {
  const d = await api(`/api/projekty/${PROJEKT_ID}/formularz-cenowy`).catch(() => null); if (!d) return;
  FC = {pozycje: d.pozycje || [], vat: d.vat || "0.23", pliki: p.pliki_oferty || [], oferta: d.oferta, uslugi: p.rodzaj_zamowienia === "uslugi",
        analiza: d.analiza, zal: d.zalaczniki, podpis: d.podpis, zlozenie: d.zlozenie || {}, wer: (d.weryfikacja || {}).pozycje || {}, wer_data: (d.weryfikacja || {}).data, komplet: d.komplet, link: d.link, edycja: false, p, pam: d.pamiec || [], koszty: d.koszty_pracy};
  rysujAnalizeD(); rysujFormularzCenowy(); rysujZlozenie();
  const prz = document.querySelector("#projekt > .widok-przelacznik");
  if (prz) { document.querySelector("#projekt > .kz-stepper")?.nextElementSibling?.remove(); document.querySelector("#projekt > .kz-stepper")?.remove();
    prz.insertAdjacentHTML("afterend", coDalejHtml([["sek-dokumenty", "Dokumenty przetargu", (p.pliki || []).length > 0], ["sek-analiza-d", "Analiza i błędy", !!FC.analiza],
      ["sek-formularz", "Formularz cenowy", !!FC.oferta], ["sek-dok-wyk", "Dokumenty wykonawcy", !!FC.komplet], ["sek-zlozenie", "Złożenie oferty", !!(FC.p || {}).zlozona]])); }
}
const liczbaFC = v => parseFloat(String(v ?? "").replace(/\s/g, "").replace(",", ".")) || 0;
function rysujAnalizeD() {
  const el = $("#sek-analiza-d-tresc"); if (!el) return;
  const a = FC.analiza, P = (a || {}).postepowanie || {};
  $("#sek-analiza-d-stan").textContent = a ? `przeanalizowano ${a.data || ""}` : "do zrobienia";
  const lista = L => (L || []).length ? `<ul class="lista">${L.map(x => `<li>${esc(typeof x === "string" ? x : JSON.stringify(x))}</li>`).join("")}</ul>` : '<p class="opis">–</p>';
  el.innerHTML = !a ? `<p class="opis">AI przeczyta dokumenty przetargu i ustali: <b>co trzeba zaoferować</b> (pozycje z ilościami – trafią do formularza cenowego w kroku 3), terminy,
      wadium, kryteria oceny, wymagane dokumenty i warunki udziału oraz <b>błędy, sprzeczności i niejasności w dokumentacji</b> z gotowymi pytaniami do zamawiającego.</p>
      <div class="pasek"><button class="glowny" data-ik="iskra" onclick="analizujD()">Analizuj przetarg (AI)</button></div>`
    : `<p>${esc(a.podsumowanie || "")}</p>
      <div class="tabela-okno"><table class="tabela"><tr><th>Termin składania</th><td>${esc(P.termin_skladania || "–")}</td><th>Termin wykonania</th><td>${esc(P.termin_wykonania || "–")}</td></tr>
        <tr><th>Wadium</th><td>${esc(P.wadium || "–")}</td><th>Termin związania</th><td>${esc(P.termin_zwiazania || "–")}</td></tr>
        <tr><th>Kryteria oceny</th><td>${esc((P.kryteria_oceny || []).join(", ") || "–")}</td><th>Sposób złożenia</th><td>${esc(P.sposob_zlozenia || "–")}</td></tr></table></div>
      <h4 class="grupa-analizy">Co trzeba zaoferować: ${(a.co_zaoferowac || []).length} pozycji (formularz cenowy w kroku 3)</h4>
      ${a.uciete ? '<div class="ramka-uwaga">Odpowiedź AI była dłuższa niż limit – lista pozycji może być niepełna. Porównaj liczbę pozycji z formularzem cenowym zamawiającego w kroku 3.</div>' : ""}
      <details><summary><b>Wymagane dokumenty (${(a.wymagane_dokumenty || []).length})</b></summary>${lista(a.wymagane_dokumenty)}</details>
      <details><summary><b>Warunki udziału (${(a.warunki_udzialu || []).length})</b></summary>${lista(a.warunki_udzialu)}</details>
      <h4 class="grupa-analizy">Błędy i niejasności w dokumentacji (${(a.bledy || []).length})${a.bledy_data ? ` <small class="opis">sprawdzono ${esc(a.bledy_data)}</small>` : ""}</h4>
      ${a.bledy_status === "blad" ? `<div class="ramka-uwaga" style="border-left-color:#dc2626;background:#FEF2F2"><b>Wykrywanie błędów nie powiodło się</b> – lista poniżej może być niepełna albo pusta.<br><small>${esc(a.bledy_blad || "")}</small></div>` : ""}
      ${bledyPodejrzane(a)
        ? '<div class="ramka-uwaga">Podsumowanie wskazuje na sprzeczności lub niejasności, a lista błędów jest pusta – kliknij „Wykryj błędy ponownie” albo sprawdź te miejsca ręcznie.</div>' : ""}
      ${(a.bledy || []).length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Waga</th><th>Problem</th><th>Gdzie</th><th>Pytanie do zamawiającego</th></tr>
        ${a.bledy.map(b => `<tr><td><span class="znacznik ${b.waga === "wysoka" ? "z-czerwony" : b.waga === "średnia" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(b.waga || "")}</span></td>
          <td>${esc(b.opis || "")}</td><td>${b.odw ? odwChip(b.odw, b.miejsce || b.gdzie, {typ: "projekt", id: PROJEKT_ID}) : esc(b.gdzie || "")}</td><td><small>${esc(b.pytanie_do_zamawiajacego || "")}</small></td></tr>`).join("")}</table></div>
        <div class="pasek"><button class="maly" data-ik="dokument" onclick="kopiujPytaniaD()">Kopiuj pytania do zamawiającego</button>
          <button class="maly" data-ik="pobierz" onclick="pobierzBledy()">Pobierz wykaz błędów (Word)</button></div>`
        : a.bledy_status === "blad" || bledyPodejrzane(a) ? "" : `<p class="opis">${a.bledy_status ? "Sprawdzenie nie wykazało błędów w dokumentach." : "Brak listy błędów – uruchom wykrywanie błędów."}</p>`}
      <div class="pasek"><button class="maly" data-ik="iskra" onclick="bledyD()">Wykryj błędy ponownie</button></div>
      ${(a.ryzyka || []).length ? `<details><summary><b>Ryzyka (${a.ryzyka.length})</b></summary>${lista(a.ryzyka)}</details>` : ""}
      <div class="pasek" style="margin-top:8px"><button class="maly" data-ik="odswiez" onclick="analizujD()">Analizuj ponownie</button></div>`;
  wstawIkony(el);
}
// pusta lista błędów, choć podsumowanie analizy mówi o sprzecznościach – ostrzeżenie zamiast „nie znaleziono błędów”
const bledyPodejrzane = a => !(a.bledy || []).length && a.bledy_status !== "blad" && /sprzeczn|niejasn|niezgodn|błęd|wskazując\w* (na )?(jednego |konkretnego )?producent/i.test(a.podsumowanie || "");
async function bledyD() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/analiza-dostawcy/bledy`, {json: {}})), odswiezProjekt); }
async function analizujD() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/analiza-dostawcy`, {json: {}})), odswiezProjekt); }
function kopiujPytaniaD() {
  const t = (FC.analiza.bledy || []).map((b, i) => `${i + 1}. ${b.pytanie_do_zamawiajacego || b.opis}`).join("\n");
  navigator.clipboard?.writeText("Pytania dotyczące treści SWZ:\n" + t).then(() => komunikat("Skopiowano pytania – wklej je do wniosku o wyjaśnienie treści SWZ."), () => prompt("Skopiuj pytania:", t));
}
function zbierzFC() {
  document.querySelectorAll("#fc-tab tr[data-i]").forEach(tr => { const x = FC.pozycje[+tr.dataset.i];
    ["opis", "jm", "ilosc", "cena", "uwagi"].forEach(k => { const e = tr.querySelector(".fc-" + k); if (e) x[k] = e.value; }); });
  const v = $("#fc-vat"); if (v) FC.vat = v.value;
}
function przeliczFC() {
  zbierzFC(); let netto = 0, brak = 0;
  document.querySelectorAll("#fc-tab tr[data-i]").forEach(tr => { const x = FC.pozycje[+tr.dataset.i], w = liczbaFC(x.ilosc) * liczbaFC(x.cena); netto += w; if (!liczbaFC(x.cena)) brak++;
    tr.querySelector(".fc-wart").textContent = w ? zl(w) : "–"; });
  const vat = parseFloat(FC.vat) || 0;
  const K = FC.koszty;  // usługi: minimalne koszty pracy personelu wymaganego w SWZ (umowa o pracę) – na bieżąco przy wpisywaniu cen
  const praca = K && K.minimum_netto && netto ? (netto < K.minimum_netto
      ? `<div class="ramka-uwaga" style="margin-top:8px"><b>Cena nie pokrywa minimalnych kosztów pracy.</b> SWZ wymaga ${liczba(K.osoby, 1)} os. na umowę o pracę przez ${liczba(K.miesiace, 1)} mies. – sama płaca minimalna${K.placa_minimalna ? ` (${zl(K.placa_minimalna)} brutto – średnio w okresie umowy)` : ""} ze składkami, zastępstwami i absencjami to ok. <b>${zl(K.minimum_netto)}</b> netto (${zl(K.na_etat_mies)} na etat miesięcznie). Twoja cena: ${zl(netto)} (${Math.round(netto / K.minimum_netto * 100)}%). Taka oferta zostanie wezwana do wyjaśnień i najpewniej odrzucona jako rażąco niska (art. 224 ust. 3 pkt 4, art. 226 ust. 1 pkt 8 Pzp). <a href="#" onclick="pokaz('kalk_pracy'); return false">Kalkulator kosztów pracy</a></div>`
      : netto < K.minimum_netto * 1.1 ? `<div class="ramka-uwaga" style="margin-top:8px">Cena pokrywa minimalne koszty pracy (${zl(K.minimum_netto)} netto), ale na środki, sprzęt, koszty ogólne i zysk zostaje mniej niż 10%.</div>` : "") : "";
  $("#fc-suma").innerHTML = `Razem netto: <b>${zl(netto)}</b> · VAT ${Math.round(vat * 100)}%: ${zl(netto * vat)} · <b>brutto: ${zl(netto * (1 + vat))}</b>${brak ? ` · <span class="czerwone">bez ceny: ${brak}</span>` : ""}${praca}`;
}
function rysujFormularzCenowy() {
  const el = $("#sek-formularz-tresc") || $("#fc-tresc"); if (!el) return;
  $("#sek-formularz-stan") && ($("#sek-formularz-stan").textContent = FC.oferta ? "oferta: " + zl(FC.oferta.brutto) + " brutto" : FC.pozycje.length ? "wpisz ceny" : "po analizie");
  if (!FC.pozycje.length && !FC.edycja) {
    el.innerHTML = `<p class="opis">Pozycje do zaoferowania program ustali w <b>kroku 2 (Analizuj przetarg)</b> – z formularza cenowego zamawiającego albo opisu przedmiotu zamówienia.
      Możesz też <a href="#" onclick="FC.edycja = true; FC.pozycje.push({opis: '', jm: '${FC.uslugi ? "m-c" : "szt."}', ilosc: 1, cena: ''}); rysujFormularzCenowy(); return false">dodać pozycje ręcznie</a>.</p>`;
    return;
  }
  const ocena = lp => { const w = FC.wer[String(lp)]; if (!w) return "";
    const kl = w.ocena === "rynkowa" ? "z-startujemy" : w.ocena === "za nisko" ? "z-czerwony" : "z-do-analizy";
    return `<div style="margin-top:4px"><span class="znacznik ${kl}">${esc(w.ocena || "")}</span> <small class="opis">rynek: ${w.od ? zl(w.od) : "?"} – ${w.do ? zl(w.do) : "?"}${w.komentarz ? " · " + esc(w.komentarz) : ""}</small></div>`; };
  const E = FC.edycja;
  el.innerHTML = `<p class="opis">${E ? "Edycja pozycji – zmień opis, jednostkę albo ilość." : "Pozycje i ilości ustalił program na podstawie dokumentów. <b>Wpisz tylko cenę jednostkową netto</b> – wartości, VAT i sumę program liczy sam."}</p>
    <div class="tabela-okno"><table class="tabela" id="fc-tab"><tr><th>Lp.</th><th>${FC.uslugi ? "Usługa" : "Towar"} – co trzeba zaoferować</th><th>j.m.</th><th>Ilość</th><th>Cena jedn. netto [zł]</th><th>Wartość netto</th>${E ? "<th></th>" : ""}</tr>
      ${FC.pozycje.map((x, i) => `<tr data-i="${i}"><td>${i + 1}</td>
        <td>${E ? `<textarea class="fc-opis" rows="2" style="min-width:260px">${esc(x.opis || "")}</textarea>` : `<b>${esc(x.opis || "")}</b>${x.uwagi ? `<br><small class="opis">${esc(x.uwagi)}</small>` : ""}${x.czesc ? ` <small class="znacznik z-odpuszczamy">część ${esc(x.czesc)}</small>` : ""}`}</td>
        <td>${E ? `<input class="fc-jm" value="${esc(x.jm || "")}" style="width:70px">` : esc(x.jm || "")}</td>
        <td class="liczba">${E ? `<input class="fc-ilosc" value="${esc(String(x.ilosc ?? ""))}" style="width:80px" oninput="przeliczFC()">` : esc(String(x.ilosc ?? "")).replace(".", ",")}</td>
        <td><input class="fc-cena" value="${x.cena ? String(x.cena).replace(".", ",") : ""}" style="width:120px" oninput="przeliczFC()" placeholder="wpisz cenę">${ocena(i + 1)}
          ${(FC.pam || [])[i] ? `<div><small class="kz-zr">ostatnio: ${zl(FC.pam[i].cena)} – ${esc(FC.pam[i].projekt || "")}, ${esc(FC.pam[i].data || "")}${FC.pam[i].podobienstwo < 1 ? " (podobna pozycja)" : ""}</small></div>` : ""}</td>
        <td class="liczba fc-wart">–</td>${E ? `<td><button class="maly niebezp" data-ik="kosz" onclick="zbierzFC(); FC.pozycje.splice(${i},1); rysujFormularzCenowy()"></button></td>` : ""}</tr>`).join("")}</table></div>
    <div class="pasek"><label>Stawka VAT <select id="fc-vat" onchange="przeliczFC()">${[["0.23", "23%"], ["0.08", "8%"], ["0.05", "5%"], ["0", "0% / zw."]].map(([v, t]) => `<option value="${v}" ${v === FC.vat ? "selected" : ""}>${t}</option>`).join("")}</select></label>
      ${E ? `<button class="maly" data-ik="plus" onclick="zbierzFC(); FC.pozycje.push({opis: '', jm: '${FC.uslugi ? "m-c" : "szt."}', ilosc: 1, cena: ''}); rysujFormularzCenowy()">Dodaj pozycję</button>
        <button class="maly" onclick="zbierzFC(); FC.edycja = false; rysujFormularzCenowy()">Zakończ edycję</button>` : `<button class="maly" data-ik="przelacz" onclick="zbierzFC(); FC.edycja = true; rysujFormularzCenowy()">Edytuj pozycje</button>`}</div>
    <p id="fc-suma" style="margin:8px 0"></p>
    <div class="pasek"><button data-ik="zapisz" onclick="zapiszFC(false)">Zapisz ceny</button>
      <button data-ik="szukaj" onclick="sprawdzCenyFC()">Sprawdź, czy ceny są rynkowe</button>
      ${(FC.pam || []).some(Boolean) ? `<button class="maly" data-ik="przelacz" onclick="wstawCenyPamieci()">Wstaw ostatnie ceny do pustych (${FC.pam.filter(Boolean).length})</button>` : ""}
      <button class="zielony" data-ik="dokument" onclick="zapiszFC(true)">Przygotuj formularz cenowy i ofertę</button></div>
    ${FC.wer_data ? `<p class="opis" style="font-size:12px">Ceny sprawdzono ${esc(FC.wer_data)} (ceny rynkowe z internetu – orientacyjne).</p>` : ""}
    ${FC.pliki.length ? `<h4 class="grupa-analizy">Dokumenty oferty</h4><div class="pliki-ik">${FC.pliki.map(f => plikIk(PROJEKT_ID, f, f.length > 26 ? f.slice(0, 24) + "…" : f)).join("")}</div>` : ""}`;
  wstawIkony(el); przeliczFC();
}
function wstawCenyPamieci() {
  zbierzFC(); let n = 0;
  FC.pozycje.forEach((x, i) => { const p = (FC.pam || [])[i]; if (p && !liczbaFC(x.cena)) { x.cena = p.cena; n++; } });
  rysujFormularzCenowy(); komunikat(n ? `Wstawiono ${n} cen z poprzednich ofert – sprawdź je.` : "Wszystkie pozycje mają już ceny.");
}
async function zapiszFC(przygotuj) {
  zbierzFC();
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/formularz-cenowy`, {json: {pozycje: FC.pozycje, vat: FC.vat, przygotuj}})); if (!w) return;
  if (przygotuj) { if (w.id) sledz(w, odswiezProjekt); else odswiezProjekt(); } else komunikat("Zapisano ceny.");
}
async function sprawdzCenyFC() {
  zbierzFC(); await api(`/api/projekty/${PROJEKT_ID}/formularz-cenowy`, {json: {pozycje: FC.pozycje, vat: FC.vat}}).catch(() => {});
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/formularz-cenowy/sprawdz-ceny`, {json: {}})), odswiezProjekt);
}
function rysujZlozenie() {
  const el = $("#sek-zlozenie-tresc"); if (!el) return;
  const a = FC.analiza || {}, P = a.postepowanie || {}, wym = a.wymagane_dokumenty || [];
  // dokumenty na wezwanie (podmiotowe środki dowodowe) – osobno, nie składa się ich z ofertą
  const wez = [...new Set([...(a.dokumenty_na_wezwanie || []), ...((FC.zal || {}).na_wezwanie || [])].map(String))].filter(x => !wym.includes(x));
  zlozeniePrzenies(wym);
  const zazn = FC.zlozenie || {}, poz = (lista, pref) => `<ul class="lista">${lista.map(d => `<li><label class="check" style="margin:0"><input type="checkbox" ${zazn[pref + d] ? "checked" : ""} data-zl="${esc(pref + d)}" onchange="zaznaczZl(this.dataset.zl, this.checked)"> ${esc(d)}</label></li>`).join("")}</ul>`;
  $("#sek-zlozenie-stan").textContent = FC.komplet ? ((FC.komplet.braki || []).length ? `brakuje: ${FC.komplet.braki.length}` : "komplet gotowy") : FC.oferta ? "do przygotowania" : "najpierw krok 3";
  el.innerHTML = `<div class="tabela-okno"><table class="tabela"><tr><th>Termin składania ofert</th><td><b>${esc(P.termin_skladania || (FC.p.przetarg || {}).termin_ofert || "–")}</b></td></tr>
      <tr><th>Gdzie złożyć</th><td>${esc(P.sposob_zlozenia || "–")}${FC.link ? ` · <a href="${esc(FC.link)}" target="_blank" rel="noopener">ogłoszenie / platforma</a>` : ""}</td></tr>
      <tr><th>Oferta</th><td>${FC.oferta ? `<b>${zl(FC.oferta.brutto)}</b> brutto (${zl(FC.oferta.netto)} netto)` : '<span class="czerwone">nieprzygotowana – krok 3</span>'}</td></tr></table></div>
    ${wym.length ? `<h4 class="grupa-analizy">Lista kontrolna – składane z ofertą</h4>${poz(wym, "")}` : ""}
    ${wez.length ? `<h4 class="grupa-analizy">Na wezwanie zamawiającego <small class="opis">– podmiotowe środki dowodowe (art. 126 / art. 274 Pzp); przygotuj je wcześniej, termin na złożenie jest krótki</small></h4>${poz(wez, "wezwanie:")}` : ""}
    <div class="pasek"><button class="glowny" data-ik="paczka" onclick="kompletD()">Przygotuj wszystko do złożenia (ZIP)</button>
      ${FC.komplet ? `<a class="przycisk dozw" data-ik="pobierz" href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(FC.komplet.zip)}">Pobierz komplet (${FC.komplet.plikow} plików, ${esc(FC.komplet.utworzono)})</a>` : ""}</div>
    <p class="opis" style="font-size:12px">Komplet zawiera formularz ofertowy, formularz cenowy, dokumenty wykonawcy z kroku 4 i spis dokumentów.
      <b>Podpis:</b> ${esc((FC.podpis || {}).tekst || "od progów unijnych – kwalifikowany podpis elektroniczny (art. 63 ust. 1 Pzp); poniżej progów – kwalifikowany, zaufany albo osobisty (art. 63 ust. 2 Pzp); poza Pzp – według zapytania.")}</p>
    ${FC.zal ? `<h4 class="grupa-analizy">Przygotowane do podpisu (${FC.zal.dokumenty.length})</h4><ul class="lista">${FC.zal.dokumenty.map(x => `<li>${esc(x)}</li>`).join("")}</ul>
      ${FC.zal.do_dolaczenia.length ? `<h4 class="grupa-analizy">Do dołączenia przez Ciebie (krok 4)</h4><ul class="lista">${FC.zal.do_dolaczenia.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
      ` : ""}
    <div id="pr-szanse"></div>`;
  wstawIkony(el);
  rysujSzanse(FC.p);
}
// zaznaczenia na serwerze (to samo na telefonie i komputerze, u każdego użytkownika projektu); klucz – treść pozycji
async function zaznaczZl(klucz, v) {
  FC.zlozenie = FC.zlozenie || {}; if (v) FC.zlozenie[klucz] = true; else delete FC.zlozenie[klucz];
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/zlozenie`, {json: {klucz, v}})); if (r) FC.zlozenie = r.zaznaczenia;
}
function zlozeniePrzenies(wym) {  // jednorazowo: zaznaczenia zapisane wcześniej w tej przeglądarce (numer pozycji) → serwer
  let z = null; try { z = JSON.parse(localStorage.getItem("zlozenie_" + PROJEKT_ID) || "null"); localStorage.removeItem("zlozenie_" + PROJEKT_ID); } catch (e) {}
  if (!z) return; const zaz = {}; Object.entries(z).forEach(([i, v]) => { if (v && wym[+i] != null) zaz[wym[+i]] = true; });
  if (!Object.keys(zaz).length) return; Object.assign(FC.zlozenie, zaz);
  api(`/api/projekty/${PROJEKT_ID}/zlozenie`, {json: {zaznaczenia: zaz}}).then(r => { if (r) FC.zlozenie = r.zaznaczenia; }).catch(() => {});
}
async function kompletD() {
  if (!FC.oferta) return komunikat("Najpierw przygotuj formularz cenowy i ofertę (krok 3).", true);
  let r = await api(`/api/projekty/${PROJEKT_ID}/komplet`, {json: {}}).catch(e => ({_blad: e.message}));
  if (r._blad && /Niesprawdzone/.test(r._blad)) { if (!confirm(r._blad + "\n\nPrzygotować komplet mimo to?")) return; r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/komplet`, {json: {mimo_to: true}})); }
  else if (r._blad) return komunikat(r._blad, true);
  if (r && r.url) { komunikat((r.braki || []).length ? `Komplet spakowany, ale brakuje: ${r.braki.join("; ")}.` : "Komplet do złożenia gotowy.", (r.braki || []).length > 0); location.href = r.url; odswiezProjekt(); }
}

// ---------- zamawiający: sprawdzenie złożonych ofert, punktacja i ranking
let OC_ID = null, OCD = null;
// ================================================================ DD / WYCENA NIERUCHOMOŚCI
let NR_ID = null, NRS = null;
const nrProd = () => ({dd: ["dd"], zabudowa: ["zabudowa"], wycena: ["wycena"], pakiet: ["dd", "zabudowa", "wycena"], wlasna: ["wlasna"]}[CEL] || ["dd"]);
async function ladujNier() {
  const l = await bezpiecznie(() => api("/api/nier")); if (!l) return;
  $("#lista-nier").innerHTML = l.map(p => `<li class="${p.id === NR_ID ? "akt" : ""}" onclick="otworzNier('${p.id}')">${esc(p.nazwa)}<small>${esc(p.dzialka || "")} · ${p.produkty.map(x => ({dd: "DD", zabudowa: "zabudowa", wycena: "wycena", wlasna: "wycena własna"})[x]).join(", ")}${p.ryzyka_czerwone ? ` · <b>⚠ ${p.ryzyka_czerwone} ryzyk krytycznych</b>` : ""}</small></li>`).join("") || '<li class="pusto">Brak nieruchomości.</li>';
  if (NR_ID && l.some(p => p.id === NR_ID)) otworzNier(NR_ID); else if (l.length) otworzNier(l[0].id);
  else $("#nier").innerHTML = `<div class="karta"><h2 style="margin-top:0">Dla rzeczoznawcy / Due Diligence / Wycena nieruchomości</h2><p>Jedna teczka nieruchomości – identyfikacja działki, mapy, dokumenty, stan prawny, oględziny, rynek – i trzy produkty:
    due diligence (ryzyka, pisma, raport), analiza zabudowy (co i ile zbudować, opłacalność) oraz wycena (projekt operatu do zatwierdzenia i podpisu przez rzeczoznawcę). Każdy osobno albo w pakiecie.</p>
    <button class="glowny" data-ik="plus" onclick="nowaNier()">Nowa nieruchomość</button></div>`;
  wstawIkony($("#w-nier"));
}
let NR_NOWA = {typ: "lokal"};
function nowaNier() {
  NR_ID = null; document.querySelectorAll("#lista-nier li").forEach(li => li.classList.remove("akt"));
  const R = [["lokal", "Mieszkanie", "teczka"], ["dom", "Dom (działka z budynkiem)", "kask"], ["budowlana", "Działka", "folder"], ["lokal_uzytkowy", "Lokal użytkowy", "portfel"]];
  const L = NR_NOWA.typ === "lokal" || NR_NOWA.typ === "lokal_uzytkowy";
  $("#nier").innerHTML = `<div class="karta"><h2 style="margin-top:0">Nowa nieruchomość</h2>
    <h3 class="kz-pyt">Co badasz lub wyceniasz?</h3>
    <div class="kz-kafle" style="grid-template-columns:repeat(4,minmax(0,1fr))">${R.map(([t, nz, ic]) => `<button class="kz-kafel ${NR_NOWA.typ === t ? "akt" : ""}" onclick="NR_NOWA.typ='${t}'; nowaNier()"><span class="cel-ik">${ik(ic)}</span><b>${nz}</b></button>`).join("")}</div>
    <div class="siatka" style="margin-top:12px"><label style="grid-column:1/-1">${L ? "Adres budynku (ulica, numer, miejscowość)" : NR_NOWA.typ === "dom" ? "Adres albo obręb i numer działki" : "Obręb i numer działki (np. Pszenno 123/4) albo adres"}<input id="nn-adres"></label>
      ${L ? `<label>Numer lokalu<input id="nn-lok"></label>` : ""}${NR_NOWA.typ !== "budowlana" ? `<label>Powierzchnia użytkowa [m²]<input id="nn-pow" inputmode="decimal"></label>` : ""}</div>
    <div class="pasek"><button class="glowny" data-ik="plus" onclick="utworzNier()">Utwórz teczkę i znajdź ${L ? "budynek" : "działkę"}</button></div>
    <p class="opis">${L ? "Program ustali budynek i działkę pod nim z adresu. Wycenę orientacyjną z ofert zrobisz od razu; do operatu potrzebne są transakcje z rejestru cen." : "Program pobierze granice działki z usługi GUGiK."}</p></div>`;
  wstawIkony($("#nier"));
}
async function utworzNier() {
  const adres = nrv("nn-adres").trim(); if (!adres) return komunikat("Wpisz adres albo obręb i numer działki.", true);
  const typ = NR_NOWA.typ, L = typ === "lokal" || typ === "lokal_uzytkowy";
  const lok = nrv("nn-lok");
  const p = await bezpiecznie(() => api("/api/nier/nowa", {json: {nazwa: adres + (lok ? " / " + lok : ""), adres, typ, nr_lokalu: lok, pow_uzytkowa: nrv("nn-pow"), produkty: nrProd()}})); if (!p) return;
  NR_ID = p.id; await ladujNier();
  const jakoDzialka = !L && /\d/.test(adres) && !/ul\.|ulica|al\.|\d{2}-\d{3}|,/i.test(adres);
  const r = await api(`/api/projekty/${p.id}/nier/identyfikuj`, {json: jakoDzialka ? {obreb_nr: adres} : {adres}}).catch(() => null);
  if (r && r.wybor) nrWyborDzialki(r, false);
  else if (r) { NRS = r; rysujNier(); komunikat(L ? "Ustalono budynek i działkę pod nim." : "Zidentyfikowano działkę."); nrOstrzezenieLokalizacji(); }
  else komunikat("Nie udało się automatycznie zidentyfikować – uzupełnij dane w kroku 1.", true);
}
async function otworzNier(id) {
  NR_ID = id; document.querySelectorAll("#lista-nier li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  NRS = await bezpiecznie(() => api(`/api/projekty/${id}/nier`)); if (NRS) rysujNier();
}
async function nrZapisz(json, cicho) { const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier`, {json})); if (r) { NRS = r; rysujNier(); if (!cicho) komunikat("Zapisano."); } }
async function nrPost(sciezka, json) { const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/${sciezka}`, {json: json || {}})); if (r && r.id && !r.n) sledz(r, () => otworzNier(NR_ID)); else if (r) { NRS = r; rysujNier(); } return r; }
async function nrPlik(sciezka, plik, dodatkowe) {
  const fd = new FormData(); fd.append("plik", plik); Object.entries(dodatkowe || {}).forEach(([k, v]) => fd.append(k, v));
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/${sciezka}`, {body: fd, method: "POST"})); if (!r) return;
  if (r.id && !r.n) sledz(r, () => otworzNier(NR_ID)); else { NRS = r; rysujNier(); komunikat("Wgrano."); }
}
async function nrDokumenty(files) { if (!files.length) return; const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); await bezpiecznie(() => api(`/api/projekty/${NR_ID}/pliki`, {method: "POST", body: fd})); otworzNier(NR_ID); }
async function nrZdjecia(files, punkt) { const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); fd.append("punkt", punkt || "ogolne"); const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/zdjecia`, {method: "POST", body: fd})); if (r) { NRS = r; rysujNier(); komunikat("Dodano zdjęcia."); } }
const nrv = id => ($("#" + id) || {}).value ?? "";
function rysujNier() {
  const S = NRS, n = S.n, d = n.dane || {}, i = n.identyfikacja || {}, P = n.produkty || {}, rk = S.rekomendacja, w = n.wycena || {}, z = n.zabudowa || {}, zw = z.wynik || {};
  const pl = (kat, f, t) => `<a class="przycisk maly" data-ik="pobierz" href="/pobierz/${S.id}/${kat}/${encodeURIComponent(f)}">${esc(t || f)}</a>`;
  const krok = (id, ikona, tytul, stan, tresc, kl = "") => `<div class="krok ${kl}" id="${id}"><div class="tytul"><span class="nr">${ik(ikona)}</span><h3>${tytul}</h3>${stan ? `<span class="stan">${stan}</span>` : ""}</div><div class="tresc">${tresc}</div></div>`;
  const R = n.ryzyka || [], aktR = R.filter(r => r.status !== "wykluczone");
  const pk = w.punkty || {};
  let h = `<div class="naglowek"><h2 style="margin:0;flex:1">${esc(S.nazwa)}</h2>
    <button class="maly" data-ik="teczka" onclick="nrArchiwizuj()" title="Teczka trafi do Archiwum – można ją przywrócić">Archiwizuj</button></div>
  <div class="nr-produkty">${Object.entries(S.produkty_nazwy).filter(([k]) => !(k === "zabudowa" && S.rodzaj === "lokal")).map(([k, v]) => `<button class="nr-chip ${P[k] ? "akt" : ""}" onclick="nrZapisz({produkty: {${k}: ${!P[k]}}}, true)">${P[k] ? "✓" : "+"} ${esc(v)}</button>`).join("")}
    <a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${S.id}/nier/raport/pakiet">Pełny pakiet (ZIP)</a></div>
  <div class="karta nr-rek"><b>Rekomendacja: ${esc(rk.decyzja)}</b> <span class="opis">– ${esc(rk.uzasadnienie)}</span>
    <div class="kwoty kafle-przetargu" style="margin-top:8px"><div><span>Cena wywoławcza</span><b>${d.cena ? zl(+String(d.cena).replace(/\s/g, "").replace(",", ".")) : "–"}</b></div>
      <div><span>Wartość (wycena)</span><b>${rk.wartosc ? zl(rk.wartosc) : "–"}</b></div><div><span>Koszt usunięcia ryzyk</span><b>${zl(rk.koszt_ryzyk)}</b></div>
      <div><span>Proponowana cena</span><b>${rk.cena_proponowana ? zl(rk.cena_proponowana) : "–"}</b></div></div></div>`;
  const TYLKO_WL = P.wlasna && !P.dd && !P.wycena && !P.zabudowa;  // wycena własna dla osoby prywatnej – bez kroków rzeczoznawcy
  const KR = [["nr-ident", "Nieruchomość", S.dzialki.length || !!(i.budynek || {}).adres_pelny]]
    .concat(TYLKO_WL && S.rodzaj === "lokal" ? [] : [["nr-plan", "Przeznaczenie", !!(n.plan || {}).status]])
    .concat(TYLKO_WL ? [] : [["nr-dok", "Dokumenty i stan prawny", Object.keys(n.stan_prawny || {}).length > 0], ["nr-og", "Oględziny", !!(n.ogledziny || {}).data]])
    .concat(P.dd ? [["nr-dd", "Due diligence", R.length > 0 && !R.some(r => r.status === "do_sprawdzenia")]] : [])
    .concat(P.zabudowa && S.rodzaj !== "lokal" ? [["nr-zab", "Zabudowa", !!zw.pow_calkowita_max]] : [])
    .concat(P.wlasna ? [["nr-wl", "Wycena własna", !!(n.wlasna || {}).wynik]] : [])
    .concat(P.wycena ? [["nr-wyc", "Wycena", ((w.punkty || {}).k7 || {}).status === "zatwierdzony"]] : []);
  const dalej = KR.find(k => !k[2]);
  h += `<div class="kz-stepper" style="margin:4px 0 6px">${KR.map(([id, t, ok], k) => `<button class="kz-krok ${ok ? "ok" : ""} ${dalej && dalej[0] === id ? "akt" : ""}" onclick="document.getElementById('${id}')?.scrollIntoView({behavior: 'smooth'})"><span>${ok ? "✓" : k + 1}</span>${esc(t)}</button>`).join("")}
    ${P.wycena ? `<button class="kz-krok" onclick="nrUstawienia()" title="Założenia metod: minimum transakcji, korekty, koszty odtworzenia, marża"><span>⚙</span>Ustawienia rzeczoznawcy</button>` : ""}</div>
    ${dalej ? `<p class="opis" style="margin:0 0 10px"><b>Co dalej:</b> ${esc(dalej[1])} – <a href="#" onclick="document.getElementById('${dalej[0]}')?.scrollIntoView({behavior: 'smooth'}); return false">przejdź</a></p>` : '<p class="opis" style="margin:0 0 10px"><b>Wszystkie kroki ukończone</b> – pobierz pełny pakiet.</p>'}
    <div id="nr-ust"></div>`;
  // ---- TECZKA: identyfikacja i dane
  const LOK = S.rodzaj === "lokal", bud = i.budynek || {};
  h += krok("nr-ident", "folder", LOK ? "1. Lokal – adres, budynek i dane" : "1. Nieruchomość – identyfikacja i dane", S.dzialki.length > 1 ? `${S.dzialki.length} działki · ${S.pow_suma} m²` : i.teryt ? esc(i.teryt) : bud.adres_pelny ? "budynek ustalony" : "do identyfikacji", `
    ${bud.adres_pelny ? `<div class="karta" style="margin:0 0 10px;padding:10px 14px"><b>Budynek:</b> ${esc(bud.adres_pelny)}
      ${bud.ostrzezenie ? `<div class="ramka-uwaga" style="margin:6px 0">⚠ ${esc(bud.ostrzezenie)}</div>` : ""}
      <br><small class="opis">${[bud.id_budynku ? "budynek w ewidencji: " + esc(bud.id_budynku) : "", bud.pow_zabudowy ? "pow. zabudowy z obrysu: " + esc(bud.pow_zabudowy) + " m²" : "", bud.kondygnacje_budynku ? "kondygnacje: " + esc(bud.kondygnacje_budynku) : "", bud.rok_budowy ? "rok budowy: " + esc(bud.rok_budowy) : "", bud.funkcja ? "funkcja: " + esc(bud.funkcja) : ""].filter(Boolean).join(" · ") || "brak danych o budynku – uzupełnij z dokumentów"} · ${esc(bud.zrodlo || "")}</small>
      ${i.teryt ? `<br><small class="opis">Działka pod budynkiem: ${esc(i.teryt)} (${i.pow_ewid} m²)</small>` : ""}</div>` : ""}
    <div class="siatka"><label>Identyfikator działki (TERYT)<input id="nr-teryt" value="${S.dzialki.length ? "" : esc(i.teryt || "")}" placeholder="np. 021901_1.0001.123/4"></label>
      <label>albo obręb i numer<input id="nr-obnr" placeholder="np. Pszenno 123/4"></label><label>albo adres<input id="nr-adr" value="${esc(d.adres || "")}"></label></div>
    <div class="pasek"><button class="zolty" data-ik="szukaj" onclick="nrIdent(false)">${S.dzialki.length ? "Zastąp działkę" : "Znajdź działkę (GUGiK)"}</button>
      ${S.dzialki.length && !LOK ? `<button class="glowny" data-ik="plus" onclick="nrIdent(true)">Dodaj kolejną działkę</button>` : ""}
      <span class="opis" style="margin:0">Nieruchomość z kilku działek: wpisz numer kolejnej działki i kliknij „Dodaj kolejną działkę”.</span></div>
    ${S.dzialki.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Działka</th><th>Obręb / gmina</th><th>Pow. [m²]</th><th>Księga wieczysta</th><th>Przeznaczenie</th><th></th></tr>
      ${S.dzialki.map(x => `<tr><td><b>${esc(x.numer || "")}</b><br><small class="opis">${esc(x.teryt || "")}</small></td><td>${esc(x.obreb || "")} / ${esc(x.gmina || "")}</td><td class="liczba">${x.pow_ewid ?? "–"}</td>
        <td><input style="width:150px" value="${esc(x.kw || "")}" placeholder="np. SW1S/00012345/6" onchange="nrPost('dzialka', {id: '${x.id}', kw: this.value})"></td>
        <td>${esc((x.plan_symbole || []).join(", ") || "–")}</td><td>${S.dzialki.length > 1 ? `<button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć działkę ${escA(x.numer || "")} z teczki?')) nrPost('dzialka', {id: '${x.id}', usun: true})"></button>` : ""}</td></tr>`).join("")}
      ${S.dzialki.length > 1 ? `<tr><td colspan="2"><b>Razem (${S.dzialki.length} działki)</b></td><td class="liczba"><b>${S.pow_suma}</b></td><td colspan="3"></td></tr>` : ""}</table></div>
      ${(S.geo_uwagi || []).map(u => `<div class="ramka-uwaga">${esc(u)}</div>`).join("")}` : ""}
    ${S.svg ? `<div class="nr-svg">${S.svg}</div><p class="opis">Granice działki${zw.geometria ? " i obszar, na którym wolno stawiać budynki (zielony, po odjęciu odległości od granic)" : ""}.</p>` : ""}
    <div class="siatka"><label>Nazwa<input id="nr-nazwa" value="${esc(d.nazwa || S.nazwa || "")}"></label>
      <label>Typ nieruchomości<select id="nr-typ">${Object.entries(S.typy).map(([k, v]) => `<option value="${k}" ${k === d.typ ? "selected" : ""}>${v}</option>`).join("")}</select></label>
      <label>Cel zakupu / wyceny<input id="nr-cel" value="${esc(d.cel || "")}" placeholder="np. budowa domów, inwestycja, zabezpieczenie kredytu"></label>
      <label>Cena wywoławcza [zł]<input id="nr-cena" value="${esc(d.cena || "")}"></label><label>Powierzchnia działki [m²]<input id="nr-pdz" value="${esc(d.pow_dzialki || "")}"></label>
      <label>Powierzchnia przedmiotu wyceny [m²]<input id="nr-pp" value="${esc(d.pow_przedmiotu || "")}" placeholder="działka albo powierzchnia użytkowa lokalu"></label>
      <label>Księga wieczysta<input id="nr-kw" value="${esc(d.kw || "")}"></label>
      ${S.pola_obiektu.map(([k, t]) => `<label>${esc(t)}<input class="nr-obj" data-k="${k}" value="${esc(d[k] || "")}"></label>`).join("")}</div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="nrZapiszDane()">Zapisz dane</button>
      <span class="opis" style="margin:0">Dane ${LOK ? "lokalu" : "budynku"} uzupełnia też analiza dokumentów (akt notarialny, odpis księgi, zaświadczenie, świadectwo energetyczne).</span></div>
    ${S.rodzaj !== "dzialka" ? (() => { const o = n.orientacyjna; return `<h4 class="grupa-analizy">Wycena orientacyjna z ofert (od razu, z adresu)</h4>
      <p class="opis">Szacunek z aktualnych ofert podobnych nieruchomości w okolicy, pomniejszonych o różnicę między ceną ofertową a transakcyjną. To nie jest operat – do operatu potrzebne są transakcje z rejestru cen.</p>
      <div class="pasek"><label style="margin:0">Korekta oferta → transakcja [%] <input id="nr-kor" style="width:70px" value="${o ? o.korekta_pct : 7}"></label>
        <button class="zolty" data-ik="iskra" onclick="nrPost('orientacyjna', {korekta: nrv('nr-kor')})">${o ? "Odśwież wycenę orientacyjną (AI)" : "Wycena orientacyjna z ofert (AI)"}</button></div>
      ${o ? `<div class="kwoty kafle-przetargu"><div><span>Wartość orientacyjna</span><b>${zl(o.wartosc)}</b><small>${esc(o.data)}</small></div><div><span>Przedział</span><b style="font-size:14px">${zl(o.od)} – ${zl(o.do)}</b></div>
        <div><span>Cena za m²</span><b>${zl(o.cena_m2)}</b><small>mediana ofert ${zl(o.mediana_ofert_m2)}</small></div><div><span>Ofert</span><b>${o.liczba}</b></div></div>
        <details><summary>Dane rynkowe użyte do szacunku (${(o.oferty || []).length})</summary><ul class="lista">${(o.oferty || []).map(x => `<li>${esc(x.opis || "oferta rynkowa")} – ${x.pow} m², ${zl(x.cena)} (${zl(x.cena / x.pow)}/m²)</li>`).join("")}</ul></details>` : ""}`; })() : ""}
    <h4 class="grupa-analizy">Mapy i rejestry (raport wstępny – sprawdź na mapie)</h4>
    <ul class="lista">${S.odnosniki.map(([t, u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)} ↗</a></li>`).join("")}</ul>
    <div class="pasek"><button class="maly" data-ik="iskra" onclick="nrPost('rozpoznanie')">Rozpoznanie wstępne w internecie (AI)</button>
      ${n.rozpoznanie ? `<span class="opis" style="margin:0">Plan miejscowy: ${n.rozpoznanie.plan.jest_plan === true ? "jest" + (n.rozpoznanie.plan.nazwa ? " – " + esc(n.rozpoznanie.plan.nazwa) : "") : n.rozpoznanie.plan.jest_plan === false ? "brak planu" : "nie ustalono"} (${esc(n.rozpoznanie.data)})</span>` : ""}</div>`);
  // ---- TECZKA: przeznaczenie (plan miejscowy)
  if (!(TYLKO_WL && S.rodzaj === "lokal")) h += krok("nr-plan", "folder", "2. Przeznaczenie – plan miejscowy", (n.plan || {}).status ? esc(((n.plan || {}).symbol || "") + " · " + n.plan.status) : "do ustalenia", `
${(() => { const pl = n.plan || {}, pt = S.plan_typ || {}; return `<p class="opis">Przeznaczenie decyduje o rodzaju nieruchomości (art. 154 UGN), doborze transakcji i parametrach zabudowy.</p>
      <p class="opis">Najpewniej: <b>wgraj wypis z planu</b> albo tekst uchwały i rysunek, albo <b>podaj link</b> do uchwały lub strony z planem. Automatyczne wyszukiwanie (geoportal + internet) nie zawsze trafia we właściwy plan.</p>
      <div class="siatka"><label>Symbol terenu działki (jeśli znasz)<input id="nrp-sym" placeholder="np. 2MN" value="${esc(pl.symbol || "")}"></label>
        <label style="grid-column: span 2">Link do uchwały / wypisu / strony z planem<input id="nrp-url" placeholder="https://bip.gmina.pl/…/uchwala.pdf"></label></div>
      <div class="pasek" style="flex-wrap:wrap"><label class="przycisk glowny" data-ik="wgraj">Wgraj dokument z planem<input type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.docx,.html" hidden onchange="nrPlanPlik(this.files)"></label>
        <button class="glowny" data-ik="pobierz" onclick="nrPlanLink()">Pobierz z linku</button>
        <button class="maly" data-ik="iskra" onclick="nrPost('plan')">Szukaj automatycznie (geoportal + internet)</button></div>
      ${(n.plan_tereny || {}).tereny && n.plan_tereny.tereny.length ? `<div class="pasek" style="flex-wrap:wrap"><span class="opis" style="margin:0">Tereny z planu (${n.plan_tereny.tereny.length}) – wybierz symbol działki:</span>
        <select id="nrp-wyb">${n.plan_tereny.tereny.map(t => `<option value="${esc(t.symbol)}" ${t.symbol === pl.symbol ? "selected" : ""}>${esc(t.symbol)} – ${esc((t.przeznaczenie || "").slice(0, 70))}</option>`).join("")}</select>
        <button class="maly glowny" onclick="nrPlanWybierz(nrv('nrp-wyb'))">Ustaw symbol działki</button></div>` : ""}
      <div class="pasek" style="flex-wrap:wrap"><span class="opis" style="margin:0">Albo wpisz ręcznie:</span><input id="nrp-rsym" placeholder="symbol, np. 2MN" style="width:120px"><input id="nrp-rprz" placeholder="przeznaczenie, np. zabudowa mieszkaniowa jednorodzinna" style="min-width:260px;flex:1">
        <button class="maly" onclick="nrPlanWybierz(nrv('nrp-rsym'), nrv('nrp-rprz'))">Zapisz</button></div>
      ${pl.status ? `<div class="karta" style="margin:6px 0;padding:10px 14px"><b>${esc(pl.symbol || (pl.symbole || []).join(", ") || "–")}</b> – ${esc(pl.przeznaczenie || pt.grupa || "")}
        <span class="znacznik ${pl.status === "potwierdzone" ? "z-startujemy" : "z-do-analizy"}">${{potwierdzone: "potwierdzone (wypis)", "z dokumentu": "z dokumentu planu", "wpisane ręcznie": "wpisane ręcznie"}[pl.status] || "wstępne – z wyszukiwania"}</span>
        ${pl.uzasadnienie_symbolu ? `<br><small class="opis">Symbol działki: ${esc(pl.uzasadnienie_symbolu)}</small>` : ""}
        <br><small class="opis">${esc([pl.uchwala, pl.paragraf, pl.zrodlo_opis || pl.zrodlo, pl.data].filter(Boolean).join(" · "))}</small>
        ${pl.tytul_planu || pl.obowiazuje_od ? `<br><small class="opis">Rejestr planów (geoportal): ${esc([pl.tytul_planu, pl.obowiazuje_od ? "obowiązuje od " + pl.obowiazuje_od : ""].filter(Boolean).join(" · "))}</small>` : ""}
        ${(pl.linki || []).length ? `<br><small class="opis">${pl.linki.slice(0, 4).map(u => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(/\.tif/i.test(u) ? "rysunek planu" : /\.gml/i.test(u) ? "dane planu (GML)" : "karta planu")}</a>`).join(" · ")}</small>` : ""}
        ${(pl.rozbieznosci || []).map(x => `<div class="ramka-uwaga" style="margin:6px 0">⚠ Różnica – ${esc(x.pole)}: rejestr planów: <b>${esc(x.rejestr)}</b>; wyszukiwanie w internecie: <b>${esc(x.internet)}</b>. Program zostawił dane z rejestru – potwierdź wypisem z planu albo wpisz ręcznie.</div>`).join("")}
        ${pl.plan_ogolny ? `<br><small class="opis">Plan ogólny gminy: ${esc([pl.plan_ogolny.strefa, pl.plan_ogolny.akt].filter(Boolean).join(" · "))}</small>` : ""}
        ${pl.jest_plan === false ? `<br><small>Brak planu: ${esc(pl.bez_planu || "przeznaczenie z planu ogólnego / studium, decyzji o warunkach zabudowy albo faktycznego użytkowania")}</small>` : ""}
        ${pl.udzialy && Object.keys(pl.udzialy).length > 1 ? `<br><small>Udziały przeznaczeń (wg działek): ${Object.entries(pl.udzialy).map(([k, v]) => `${esc(k)} ${v} m²`).join(" · ")} – dokładne udziały potwierdź wypisem i wyrysem.</small>` : ""}
        ${(pl.inne_ustalenia || []).length ? `<ul class="lista">${pl.inne_ustalenia.slice(0, 6).map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
        ${pt.typ && S.rodzaj === "dzialka" && pt.typ !== d.typ ? `<div class="pasek" style="margin:6px 0 0"><span class="opis" style="margin:0">Przeznaczenie wskazuje rodzaj: <b>${esc(S.typy[pt.typ])}</b> (obecnie: ${esc(S.typy[d.typ] || "–")}).</span>
          <button class="maly glowny" onclick="nrZapisz({dane: {typ: '${pt.typ}'}})">Zmień rodzaj</button></div>` : ""}</div>` : ""}`; })()}`);
  if (!TYLKO_WL) {
  // ---- TECZKA: dokumenty i stan prawny
  const sp = n.stan_prawny || {};
  h += krok("nr-dok", "dokument", "3. Dokumenty i stan prawny", `${S.dokumenty.length} dokumentów`, `
    <p class="opis">Wgraj: odpis księgi wieczystej, wypis i wyrys z ewidencji, wypis z planu, decyzje, umowy najmu, projekty, świadectwa. AI czyta księgę dział po dziale i porównuje dokumenty.</p>
    <div class="pasek"><label class="przycisk" data-ik="wgraj">Wgraj dokumenty<input type="file" multiple hidden onchange="nrDokumenty(this.files)"></label>
      <button class="zolty" data-ik="iskra" onclick="nrPost('dokumenty')">Analizuj dokumenty (AI)</button></div>
    ${S.dokumenty.length ? `<div class="pliki-wynik">${S.dokumenty.map(f => pl("dokumenty", f)).join(" ")}</div>` : ""}
    ${Object.keys(sp).length ? `<div class="tabela-okno"><table class="tabela">${[["Księga wieczysta", sp.kw], ["Właściciele", sp.wlasciciele], ["Forma władania", sp.forma], ["Działki", sp.dzialki],
      ["Powierzchnia w KW / ewidencji", `${sp.pow_kw_m2 ?? "–"} / ${sp.pow_ewid_m2 ?? "–"} m²`], ["Hipoteki", (sp.hipoteki || []).join("; ")], ["Służebności", (sp.sluzebnosci || []).join("; ")],
      ["Roszczenia, ostrzeżenia", (sp.roszczenia_ostrzezenia || []).join("; ")], ["Egzekucje", (sp.egzekucje || []).join("; ")], ["Uwagi", sp.uwagi]].map(([a, b]) => `<tr><td><b>${a}</b></td><td>${esc(b || "–")}</td></tr>`).join("")}</table></div>` : ""}
    ${(n.braki || []).length ? `<div class="ramka-uwaga"><b>Do uzyskania:</b><ul class="lista">${n.braki.map(b => `<li>${esc(b)}</li>`).join("")}</ul></div>` : ""}`);
  // ---- TECZKA: oględziny
  const og = n.ogledziny || {punkty: {}};
  h += krok("nr-og", "aparat", "4. Oględziny", og.data ? "przeprowadzone " + esc(og.data) : "do przeprowadzenia", `
    <div class="siatka"><label>Data oględzin<input type="date" id="og-data" value="${esc(og.data || "")}"></label><label>Przeprowadził(a)<input id="og-osoba" value="${esc(og.osoba || "")}"></label></div>
    <div class="tabela-okno"><table class="tabela"><tr><th>Punkt</th><th>Ocena</th><th>Uwagi</th></tr>${S.lista_ogledzin.map((p, k) => { const v = (og.punkty || {})[p] || {};
      return `<tr><td>${esc(p)}</td><td><select class="og-oc" data-p="${esc(p)}"><option></option>${["bez uwag", "uwaga", "problem"].map(o => `<option ${o === v.ocena ? "selected" : ""}>${o}</option>`).join("")}</select></td>
        <td><input class="og-uw" data-p="${esc(p)}" value="${esc(v.uwagi || "")}"></td></tr>`; }).join("")}</table></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="nrZapiszOgl()">Zapisz oględziny</button>
      <label class="przycisk maly" data-ik="aparat">Dodaj zdjęcia<input type="file" accept="image/*" multiple hidden onchange="nrZdjecia(this.files, 'ogledziny')"></label>
      <span class="opis" style="margin:0">${S.zdjecia.length} zdjęć</span></div>`);
  }
  // ---- DD
  if (P.dd) {
    const opcje = (o, v) => Object.entries(o).map(([k, t]) => `<option value="${k}" ${k === v ? "selected" : ""}>${esc(t)}</option>`).join("");
    h += krok("nr-dd", "alarm", "Due diligence – ryzyka i pisma", `${aktR.filter(r => r.waga === "czerwone").length} krytycznych · ${aktR.length} aktywnych`, `
      <div class="tabela-okno"><table class="tabela"><tr><th>Waga</th><th>Obszar</th><th>Ryzyko</th><th>Status</th><th>Koszt [zł]</th><th>Zapis do umowy</th><th></th></tr>
      ${R.map(r => `<tr data-r="${r.id}"><td><select class="r-waga">${opcje({czerwone: "czerwone", zolte: "żółte", zielone: "zielone"}, r.waga)}</select></td><td><select class="r-obszar">${opcje(S.obszary, r.obszar)}</select></td>
        <td><textarea class="r-opis" rows="2">${esc(r.opis || "")}</textarea><small class="opis">${esc([r.autor, r.dokument, r.miejsce, r.zrodlo].filter(Boolean).join(" · "))}</small></td>
        <td><select class="r-status">${opcje(S.statusy, r.status)}</select></td><td><input class="r-koszt" style="width:90px" value="${esc(r.koszt_zl ?? "")}"></td>
        <td><input class="r-umowa" value="${esc(r.zapis_umowy || "")}"></td><td><button class="maly" onclick="nrRyzyko('${r.id}')">Zapisz</button><button class="maly niebezp" data-ik="kosz" onclick="nrZapisz({ryzyko: {id: '${r.id}', usun: true}})"></button></td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="maly" data-ik="plus" onclick="nrZapisz({ryzyko: {opis: 'Nowe ryzyko', waga: 'zolte', obszar: 'prawo'}})">Dodaj ryzyko</button></div>
      <h4 class="grupa-analizy">Pisma do urzędów i gestorów</h4>
      <div class="pasek" style="flex-wrap:wrap">${Object.entries(S.pisma_katalog).map(([k, t]) => `<button class="maly" data-ik="dokument" onclick="nrPost('pismo', {rodzaj: '${k}'})">${esc(t.replace(/^(Wniosek|Zapytanie) (o |do )?/, ""))}</button>`).join("")}</div>
      ${(n.pisma || []).length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Pismo</th><th>Wysłano</th><th>Termin odpowiedzi</th><th>Odpowiedź</th><th></th></tr>
        ${n.pisma.map(p => `<tr><td>${esc(S.pisma_katalog[p.rodzaj] || p.rodzaj)}${p.zalecane && !p.plik ? ' <small class="opis">(zalecane)</small>' : ""}<br>${p.plik ? pl("nier_pisma", p.plik, "Pobierz pismo") : `<button class="maly" onclick="nrPost('pismo', {rodzaj: '${p.rodzaj}'})">Przygotuj</button>`}</td>
          <td><input type="date" value="${esc(p.wyslano || "")}" onchange="nrPost('pismo/${p.id}', {wyslano: this.value})"></td>
          <td><input type="date" value="${esc(p.termin || "")}" onchange="nrPost('pismo/${p.id}', {termin: this.value})"></td>
          <td>${p.odpowiedz ? `<b>otrzymana</b> ${esc(p.data_odpowiedzi || "")}<br><small class="opis">${esc(p.streszczenie || "")}</small>` : `<label class="przycisk maly" data-ik="wgraj">Wgraj odpowiedź<input type="file" hidden onchange="nrPlik('pismo/${p.id}/odpowiedz', this.files[0])"></label>`}</td>
          <td><button class="maly niebezp" data-ik="kosz" onclick="nrPost('pismo/${p.id}', {usun: true})"></button></td></tr>`).join("")}</table></div>` : ""}
      <div class="pasek"><a class="przycisk glowny" data-ik="pobierz" href="/api/projekty/${S.id}/nier/raport/dd">Raport due diligence (Word)</a></div>`, "k-czer");
  }
  // ---- ZABUDOWA
  if (P.zabudowa && S.rodzaj !== "lokal") {
    const p = z.parametry || {}, pp = (k, t) => `<label>${t}<input class="zb-p" data-k="${k}" value="${esc(p[k] ?? "")}"></label>`;
    h += krok("nr-zab", "kask", "Analiza zabudowy – co i ile można zbudować", zw.pow_calkowita_max ? `do ${zw.pow_calkowita_max} m² pow. całkowitej` : "", `
      <p class="opis">Parametry z planu miejscowego (AI uzupełnia je z wypisu albo odpowiedzi gminy) – źródło: <b>${esc(p.zrodlo || "–")}</b>. Bez planu wynik jest szacunkiem i wymaga decyzji o warunkach zabudowy.</p>
      <div class="siatka">${pp("przeznaczenie", "Przeznaczenie")}${pp("pow_zab_pct", "Maks. pow. zabudowy [% działki]")}${pp("intensywnosc_max", "Intensywność zabudowy maks.")}${pp("wysokosc_m", "Wysokość maks. [m]")}
        ${pp("kondygnacje", "Kondygnacje")}${pp("pbc_pct", "Pow. biologicznie czynna min. [%]")}${pp("odl_granica_m", "Odległość od granic [m]")}${pp("parking_na_lokal", "Miejsca parkingowe na lokal")}${pp("pow_lokalu_m2", "Średnia pow. mieszkania [m²]")}</div>
      <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="nrZapiszZab()">Przelicz</button></div>
      ${zw.pow_dzialki ? `<div class="kwoty kafle-przetargu"><div><span>Działka</span><b>${zw.pow_dzialki} m²</b></div><div><span>Obszar do zabudowy</span><b>${zw.obszar_zabudowy} m²</b><small>${zw.geometria ? "z granic działki" : "szacunek"}</small></div>
        <div><span>Maks. pow. zabudowy</span><b>${zw.pow_zabudowy_max} m²</b></div><div><span>Maks. pow. całkowita</span><b>${zw.pow_calkowita_max} m²</b></div>
        <div><span>Mieszkań (szac.)</span><b>${zw.lokale}</b><small>${zw.parking} miejsc parkingowych</small></div><div><span>Min. pow. biol. czynna</span><b>${zw.pbc_min} m²</b><small>${zw.pbc_ok ? "do zachowania" : "trudna do zachowania"}</small></div></div>
      <div class="tabela-okno"><table class="tabela"><tr><th>Scenariusz</th><th>Wynik</th><th>Koszt budowy [zł/m²]</th><th>Wartość [zł/m²]</th><th>Koszt</th><th>Wartość</th><th>Maks. cena działki</th></tr>
        ${(zw.scenariusze || []).map(s => `<tr><td><b>${esc(s.nazwa)}</b></td><td>${esc(s.wynik)}</td><td>${s.id === "pv" ? "–" : `<input class="zb-c" data-k="${s.id}_koszt" style="width:80px" value="${s.koszt_m2}">`}</td>
          <td>${s.id === "pv" ? "–" : `<input class="zb-c" data-k="${s.id}_wartosc" style="width:80px" value="${s.wartosc_m2}">`}</td><td class="liczba">${s.koszt ? zl(s.koszt) : "–"}</td><td class="liczba">${s.wartosc ? zl(s.wartosc) : "–"}</td>
          <td class="liczba"><b>${s.max_cena != null ? zl(s.max_cena) : esc(s.uwaga || "–")}</b></td></tr>`).join("")}</table></div>` : '<p class="pusto">Zidentyfikuj działkę albo wpisz jej powierzchnię.</p>'}
      <p class="opis">Do sprawdzenia przez projektanta: nasłonecznienie, przesłanianie, wymagania pożarowe, strefy ochronne sieci według gestorów.</p>
      <div class="pasek"><a class="przycisk glowny" data-ik="pobierz" href="/api/projekty/${S.id}/nier/raport/zabudowa">Analiza zabudowy (Word)</a></div>`, "k-ziel");
  }
  // ---- WYCENA WŁASNA (szacunek z ofert rynkowych)
  if (P.wlasna) {
    const wl = n.wlasna || {}, O = wl.oferty || [], wy = wl.wynik, CW = S.cechy_wlasne || [];
    h += krok("nr-wl", "szukaj", "Wycena własna – szacunek z ofert rynkowych", wy ? `${zl(wy.wartosc)} · pewność ${esc(wy.pewnosc)}` : `${O.filter(o => !o.wykluczona).length} ofert`, `
      <div class="ramka-uwaga">Szacunek z aktualnych danych rynkowych (oferty sprzedaży podobnych nieruchomości) metodą porównawczą. To <b>nie jest operat szacunkowy</b> – nie zastąpi wyceny rzeczoznawcy tam, gdzie jest wymagana (bank, sąd, urząd).</div>
      <p class="opis"><b>1. Nieruchomość</b> – cechy uzupełnij w kroku 1 teczki (powierzchnia, piętro, rok budowy, standard, stan, dodatki); im dokładniej, tym trafniejsze porównanie.</p>
      <p class="opis" style="margin-top:10px"><b>2. Oferty porównawcze</b></p>
      <div class="pasek" style="flex-wrap:wrap"><button class="zolty" data-ik="iskra" onclick="nrPost('wlasna/szukaj')">Szukaj podobnych ofert (AI)</button></div>
      <div class="siatka"><label style="grid-column:1/-1">Linki do ofert albo do listy ofert (np. podobne nieruchomości w Twojej miejscowości) – każdy w nowej linii<textarea id="wl-linki" placeholder="https://…"></textarea></label></div>
      <div class="pasek"><button class="maly" data-ik="pobierz" onclick="nrPost('wlasna/linki', {linki: nrv('wl-linki')})">Dodaj oferty z linków</button>
        <span class="opis" style="margin:0">Gdy strony nie da się odczytać – dodaj ofertę ręcznie:</span>
        <input id="wl-r-cena" placeholder="cena [zł]" style="width:110px"><input id="wl-r-pow" placeholder="pow. [m²]" style="width:90px"><input id="wl-r-lok" placeholder="lokalizacja" style="width:140px"><input id="wl-r-url" placeholder="link" style="width:160px">
        <button class="maly" onclick="nrWlZapisz({reczna: {cena: nrv('wl-r-cena'), pow: nrv('wl-r-pow'), lokalizacja: nrv('wl-r-lok'), url: nrv('wl-r-url')}})">Dodaj</button></div>
      ${O.length ? `<div class="tabela-okno"><table class="tabela"><tr><th></th><th>Oferta</th><th>Pow.</th><th>Cena</th><th>zł/m²</th>${CW.map(([c]) => `<th title="na tle Twojej nieruchomości: −2 wyraźnie gorsza … +2 wyraźnie lepsza">${esc(c)}</th>`).join("")}<th></th></tr>
        ${O.map(o => `<tr class="${o.wykluczona ? "nr-wykl" : ""}"><td style="text-decoration:none"><input type="checkbox" ${o.wykluczona ? "" : "checked"} title="uwzględnij w wycenie" onchange="nrWlZapisz({oferty: [{id: '${o.id}', wykluczona: !this.checked}]})"></td>
          <td>${esc(o.lokalizacja || o.tytul || "oferta rynkowa")}<br><small class="opis">${esc([o.standard, o.rok_budowy, o.pietro, o.dodatki].filter(Boolean).join(" · "))}${o.uzasadnienie ? " – " + esc(o.uzasadnienie) : ""}</small></td>
          <td class="liczba">${o.pow}</td><td class="liczba">${zl(o.cena)}</td><td class="liczba">${zl(o.cena_m2)}</td>
          ${CW.map(([c]) => `<td><select class="wl-oc" data-o="${o.id}" data-c="${esc(c)}">${[-2, -1, 0, 1, 2].map(v => `<option value="${v}" ${(+((o.oceny || {})[c] || 0)) === v ? "selected" : ""}>${v > 0 ? "+" + v : v}</option>`).join("")}</select></td>`).join("")}
          <td><button class="maly niebezp" data-ik="kosz" onclick="nrWlZapisz({oferty: [{id: '${o.id}', usun: true}]})"></button></td></tr>`).join("")}</table></div>
        <p class="opis">Oceny cech: <b>+</b> – oferta lepsza od Twojej nieruchomości (jej cena zostanie skorygowana w dół), <b>−</b> – gorsza. Możesz je poprawić.</p>` : ""}
      <p class="opis" style="margin-top:10px"><b>3. Wynik</b></p>
      <div class="pasek" style="flex-wrap:wrap">${O.length ? `<button class="zolty" data-ik="iskra" onclick="nrPost('wlasna/oceny')">Oceń cechy ofert (AI)</button>` : ""}
        <label style="margin:0">Korekta oferta → transakcja [%] <input id="wl-kor" style="width:70px" value="${esc(wl.korekta_pct ?? "")}" placeholder="auto"></label>
        <button class="glowny" data-ik="kalkulator" onclick="nrWlOblicz()">Oblicz wycenę</button></div>
      ${wy ? `<div class="kwoty kafle-przetargu"><div><span>Wartość (najbardziej prawdopodobna)</span><b>${zl(wy.wartosc)}</b><small>${zl(wy.cena_m2)}/m²</small></div>
        <div><span>Przedział</span><b style="font-size:14px">${zl(wy.od)} – ${zl(wy.do)}</b></div>
        <div><span>Pewność</span><b>${esc(wy.pewnosc)}</b><small>${wy.liczba} ofert, rozrzut ${wy.rozrzut_pct}%</small></div>
        <div><span>Korekta ofert</span><b>${wy.korekta_pct}%</b><small>${esc(wy.zrodlo_korekty)}</small></div></div>
        <div class="pasek"><a class="przycisk glowny" data-ik="pobierz" href="/api/projekty/${S.id}/nier/raport/wlasna">Raport z wyceny własnej (Word)</a>
          ${P.wycena ? "" : `<button class="maly" data-ik="przelacz" onclick="nrWlZapisz({do_rzeczoznawcy: true})">Przekaż do rzeczoznawcy (operat)</button>`}</div>` : ""}`, "k-ziel");
  }
  // ---- WYCENA
  if (P.wycena) {
    const T = w.transakcje || [], wyn = w.wynik || {}, cechy = w.cechy || [];
    h += krok("nr-wyc", "kalkulator", "Wycena – projekt operatu do zatwierdzenia przez rzeczoznawcę", (() => { const k = {porownawcze: "wynik", parami: "parami", kosztowe: "kosztowe", dochodowe: "dochodowe", pozostalosciowa: "pozostalosciowa"}[w.podejscie || "porownawcze"]; const x = (w[k] || {}).wartosc_zaokr; return x ? zl(x) : ""; })(), `
      <div class="pasek" style="flex-wrap:wrap;margin:0 0 8px"><button class="maly" data-ik="przelacz" onclick="nrNowaWycena('aktualizacja')" title="Ta sama nieruchomość i założenia, nowa data wyceny – dodaj nowe transakcje">Aktualizuj operat (nowa data wyceny)</button>
        <button class="maly" data-ik="plus" onclick="nrNowaWycena('nowa')" title="Np. inny cel albo rodzaj wartości (ubezpieczenie – wartość odtworzeniowa)">Nowa wycena w tej teczce</button>
        ${S.archiwum_wycen.length ? `<details style="flex-basis:100%"><summary>Archiwum wycen w teczce (${S.archiwum_wycen.length})</summary><ul class="lista">${S.archiwum_wycen.slice().reverse().map(a => `<li>${esc(a.data)} · ${esc(a.etykieta || "")} · ${esc(a.rodzaj_wartosci || "")} · ${esc(a.podejscie || "")} · <b>${a.wartosc ? zl(a.wartosc) : "–"}</b>
          ${a.operat ? ` · <a href="/pobierz/${S.id}/nier_wyniki/${encodeURIComponent(a.operat)}">operat</a>` : ""}</li>`).join("")}</ul></details>` : ""}</div>
      <div class="ramka-uwaga">Operat szacunkowy sporządza i podpisuje rzeczoznawca majątkowy, który osobiście przeprowadza oględziny. Program przygotowuje projekt; każda liczba jest propozycją, dopóki rzeczoznawca nie zatwierdzi punktu kontrolnego.</div>
      <div class="nr-pk">${S.punkty_def.map(([k, t]) => { const st = (pk[k] || {}).status; return `<span class="${st === "zatwierdzony" ? "ok" : st === "do_ponownego" ? "pon" : ""}" title="${esc(pk[k] ? (pk[k].kto || "") + " " + (pk[k].kiedy || "") : "")}">${st === "zatwierdzony" ? "✓" : st === "do_ponownego" ? "!" : "○"} ${esc(t)}</span>`; }).join("")}</div>
      ${S.punkty_def.some(([k]) => (pk[k] || {}).status === "do_ponownego") ? '<div class="ramka-uwaga">Dane w teczce zmieniły się po zatwierdzeniu – punkty oznaczone „!” trzeba potwierdzić ponownie.</div>' : ""}
      <h4 class="grupa-analizy">Punkt 1 – zakres i cel</h4>
      ${(() => { const celInny = w.cel && !S.cele_wyceny.some(([c]) => c === w.cel); return `<div class="siatka">
        <label>Cel wyceny<select id="nrw-cel" onchange="const p = this.options[this.selectedIndex].dataset.rw; if (p) $('#nrw-rodz').value = p; $('#nrw-cel-inny').closest('label').style.display = this.value === 'inny cel' ? '' : 'none'">
          <option value="">– wybierz cel –</option>${S.cele_wyceny.map(([c, rw]) => `<option value="${esc(c)}" data-rw="${esc(rw)}" ${c === w.cel || (celInny && c === "inny cel") ? "selected" : ""}>${esc(c)}</option>`).join("")}</select></label>
        <label style="${celInny ? "" : "display:none"}">Inny cel – wpisz<input id="nrw-cel-inny" value="${esc(celInny ? w.cel : "")}"></label>
        <label>Rodzaj wartości<select id="nrw-rodz">${S.rodzaje_wartosci.map(r => `<option ${r === (w.rodzaj_wartosci || "wartość rynkowa") ? "selected" : ""}>${esc(r)}</option>`).join("")}</select></label>
        <label>Data wyceny<input type="date" id="nrw-data" value="${esc(w.data_wyceny || "")}"></label><label>Stan nieruchomości na dzień<input type="date" id="nrw-stan" value="${esc(w.stan_na || "")}"></label>
        <label>Zamawiający wycenę<input id="nrw-zam" value="${esc(w.zamawiajacy || "")}"></label><label>Rzeczoznawca majątkowy<input id="nrw-rz" value="${esc(w.rzeczoznawca || "")}"></label>
        <label>Nr uprawnień<input id="nrw-nr" value="${esc(w.nr_uprawnien || "")}"></label></div>`; })()}
      <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="nrZapiszZakres()">Zapisz</button>${nrPk("k1")}</div>
      <h4 class="grupa-analizy">Punkty 2–3 – stan prawny i oględziny</h4><p class="opis">Z teczki (kroki 2 i 3 powyżej).</p><div class="pasek">${nrPk("k2")}${nrPk("k3")}</div>
      <h4 class="grupa-analizy">Punkt 4 – transakcje (${T.filter(t => !t.wykluczona).length} przyjętych z ${T.length}; zalecane min. ${S.min_transakcji})</h4>
      <p class="opis">Wgraj wyciąg z rejestru cen i wartości nieruchomości (Excel, CSV albo PDF) albo własną bazę. Program wstępnie odrzuca transakcje nietypowe z uzasadnieniem – możesz je przywrócić.</p>
      <div class="pasek"><label class="przycisk" data-ik="wgraj">Wgraj transakcje<input type="file" accept=".xlsx,.csv,.pdf,.txt" hidden onchange="nrPlik('transakcje', this.files[0])"></label>
        ${T.length ? `<button class="maly" data-ik="szukaj" onclick="nrPost('wycena/segment')">Dobierz podobne (rodzaj, powierzchnia ±40%)</button><button class="maly niebezp" onclick="if (confirm('Usunąć wszystkie transakcje?')) nrPlikWyczysc()">Wyczyść</button>` : ""}${nrPk("k4")}</div>
      ${Object.keys(S.wykluczenia || {}).length ? `<div class="karta" style="margin:8px 0;padding:10px 14px"><b>Wykluczone automatycznie lub ręcznie:</b>
        ${Object.entries(S.wykluczenia).map(([k, ile]) => `<span style="white-space:nowrap;margin-right:10px">${esc(S.kategorie_wykluczen[k] || k)}: <b>${ile}</b>
          <button class="maly" onclick="nrPrzywroc('${k}')">Przywróć</button></span>`).join("")}
        ${S.wykluczenia.rodzaj ? '<p class="opis" style="margin:6px 0 0">„Inny rodzaj nieruchomości” – program porównuje kolumnę rodzaju w pliku z rodzajem wycenianej nieruchomości. Jeśli plik opisuje rodzaj inaczej, przywróć tę grupę.</p>' : ""}</div>` : ""}
      ${(() => { const pod = w.podejscie || "porownawcze", min = (S.min_metody || {})[pod]; if (!min || S.aktywne_transakcje >= min) return "";
        return `<div class="karta" style="border-left:4px solid #F59E0B;margin:8px 0"><b>Za mało transakcji (${S.aktywne_transakcje} z ${min} dla wybranej metody) – co możesz zrobić</b>
        <div class="pasek" style="flex-wrap:wrap;margin-top:8px">
          <button class="maly" data-ik="dokument" onclick="nrPost('pismo', {rodzaj: 'rcn'}); komunikat('Wniosek o dane z rejestru cen – w Due diligence → Pisma.')">Wniosek do starostwa o wyciąg z rejestru cen</button>
          <button class="maly" data-ik="szukaj" onclick="nrPoszerz()">Poszerz rynek (powierzchnia ±60%)</button>
          ${pod === "porownawcze" ? `<button class="maly" onclick="nrZapisz({wycena: {podejscie: 'parami'}}, true)">Porównywanie parami (od 3 transakcji)</button>` : ""}
          ${S.podejscia.filter(([k]) => !["porownawcze", "parami"].includes(k)).map(([k, t]) => `<button class="maly" onclick="nrZapisz({wycena: {podejscie: '${k}'}}, true)">${esc(t.replace(/^./, c => c.toUpperCase()))}</button>`).join("")}
          ${S.rodzaj !== "dzialka" ? `<button class="maly" data-ik="iskra" onclick="nrPost('orientacyjna', {korekta: 7})">Wycena orientacyjna z ofert (to nie operat)</button>` : ""}</div>
        <p class="opis" style="margin:6px 0 0">Ceny ofertowe nie są podstawą operatu – służą do analizy rynku i kontroli wyniku. Poszerzenie rynku zatwierdzasz w punkcie 4, a uzasadnienie trafia do operatu.</p></div>`; })()}
      ${T.length ? `<div class="tabela-okno" style="max-height:340px"><table class="tabela"><tr><th>Data</th><th>Położenie</th><th>Pow.</th><th>Cena</th><th>zł/m²</th><th>Status</th></tr>
        ${T.map(t => `<tr class="${t.wykluczona ? "nr-wykl" : ""}"><td>${esc(t.data)}</td><td>${esc(t.lokalizacja)}<br><small class="opis">${esc(t.uwagi || "")}</small></td><td class="liczba">${t.pow}</td><td class="liczba">${zl(t.cena)}</td>
          <td class="liczba">${zl(t.cena_m2)}</td><td style="text-decoration:none">${t.wykluczona ? `<small>${esc(t.powod)}</small><br><button class="maly" onclick="nrZapisz({wycena: {transakcja: {id: '${t.id}', wykluczona: false, powod: ''}}}, true)">Przywróć</button>`
          : `<button class="maly" onclick="const p = prompt('Powód wykluczenia transakcji:'); if (p) nrZapisz({wycena: {transakcja: {id: '${t.id}', wykluczona: true, powod: p}}}, true)">Wyklucz</button>`}</td></tr>`).join("")}</table></div>` : ""}
      <h4 class="grupa-analizy">Punkt 5 – podejście i metoda</h4>
      <div class="siatka"><label>Podejście i metoda<select id="nrw-pod" onchange="nrZapisz({wycena: {podejscie: this.value}}, true)">${S.podejscia.map(([k, t]) => `<option value="${k}" ${(w.podejscie || "porownawcze") === k ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label></div>
      ${nrFormMetody(S, w, T)}
      <div class="pasek">${nrPk("k5")}</div>
      <h4 class="grupa-analizy">Punkt 6 – cechy, wagi i obliczenia</h4>
      <div class="tabela-okno"><table class="tabela"><tr><th>Cecha rynkowa</th><th>Waga [%]</th><th>Przedmiot wyceny na tle rynku</th></tr>
        ${cechy.map((c, k) => `<tr><td><input class="w-cn" value="${esc(c.nazwa)}"></td><td><input class="w-cw" style="width:70px" value="${c.waga}"></td>
          <td><select class="w-co">${[[1, "gorsza"], [2, "przeciętna"], [3, "lepsza"]].map(([v, t]) => `<option value="${v}" ${(+((w.oceny || {})[c.nazwa] || 2)) === v ? "selected" : ""}>${t}</option>`).join("")}</select></td></tr>`).join("")}</table></div>
      <div class="pasek">${(w.podejscie || "porownawcze") === "porownawcze" ? `<button class="glowny" data-ik="kalkulator" onclick="nrOblicz()">Zapisz cechy i oblicz wartość</button>` : `<button class="maly" onclick="nrZapiszCechy()">Zapisz cechy</button>`}${nrPk("k6")}</div>
      ${wyn.cena_m2 ? `<div class="kwoty kafle-przetargu"><div><span>Cśr (po trendzie)</span><b>${zl(wyn.csr)}/m²</b><small>min ${zl(wyn.cmin)} · max ${zl(wyn.cmax)}</small></div><div><span>Trend cen</span><b>${(wyn.trend_mies * 100).toFixed(2)}%</b><small>miesięcznie</small></div>
        <div><span>Σ ki</span><b>${wyn.suma_k}</b></div><div><span>Cena jednostkowa</span><b>${zl(wyn.cena_m2)}/m²</b></div><div><span>Wartość</span><b>${zl(wyn.wartosc_zaokr)}</b></div></div>
        ${wyn.ostrzezenie ? `<div class="ramka-uwaga">${esc(wyn.ostrzezenie)}</div>` : ""}
        ${(w.wrazliwosc || []).length ? `<p class="opis"><b>Wrażliwość:</b> ${w.wrazliwosc.slice(0, 5).map(x => `${esc(x.cecha)} → ${["", "gorsza", "przeciętna", "lepsza"][x.ocena]}: ${x.zmiana_pct > 0 ? "+" : ""}${x.zmiana_pct}%`).join(" · ")}</p>` : ""}` : ""}
      <h4 class="grupa-analizy">Punkt 7 – operat</h4>
      ${S.kontrola.length ? S.kontrola.map(u => `<div class="alert-k ${u.waga === "krytyczna" ? "ostrzezenie" : ""}"><span class="znacznik ${u.waga === "krytyczna" ? "z-czerwony" : u.waga === "istotna" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(u.waga)}</span> ${esc(u.opis)}</div>`).join("") : '<div class="ramka-uwaga" style="border-color:#16a34a">✓ Kontrola kompletności i spójności bez uwag.</div>'}
      <div class="pasek"><button class="zolty" data-ik="iskra" onclick="nrPost('operat', {koncowy: false})">Przygotuj projekt operatu (AI)</button>${nrPk("k7")}
        <button class="glowny" data-ik="dokument" onclick="nrPost('operat', {koncowy: true})" ${(pk.k7 || {}).status === "zatwierdzony" ? "" : "disabled"}>Wersja do podpisu</button></div>
      ${S.wyniki.filter(f => /operat/i.test(f)).length ? `<div class="pliki-wynik">${S.wyniki.filter(f => /operat/i.test(f)).map(f => pl("nier_wyniki", f)).join(" ")}</div>` : ""}`, "k-nieb");
  }
  h += `<details style="margin:12px 0"><summary><b>Dziennik zmian (${(n.dziennik || []).length})</b></summary><div class="tabela-okno" style="max-height:260px"><table class="tabela">${(n.dziennik || []).slice().reverse().map(x => `<tr><td>${esc(x.czas)}</td><td>${esc(x.kto)}</td><td>${esc(x.co)}</td></tr>`).join("")}</table></div></details>`;
  $("#nier").innerHTML = h;
  wstawIkony($("#nier"));
}
function nrPk(k) {
  const st = ((NRS.n.wycena || {}).punkty || {})[k] || {}, naz = Object.fromEntries(NRS.punkty_def)[k];
  if (st.status === "zatwierdzony") return `<span class="znacznik z-startujemy" title="${esc(st.uwaga || "")}">✓ zatwierdzone: ${esc(st.kto || "")}, ${esc(st.kiedy || "")}${st.uwaga ? " · z uwagą" : ""}</span><button class="maly" onclick="nrPost('punkt', {k: '${k}', akcja: 'cofnij'})">Cofnij</button>`;
  return `<span class="nr-zatw"><input class="nr-uw" id="nr-uw-${k}" placeholder="uwaga do dziennika (opcjonalnie)" value="${esc(st.uwaga || "")}">
    <button class="maly ${st.status === "do_ponownego" ? "zolty" : ""}" data-ik="check" onclick="nrZatwierdz('${k}')">${st.status === "do_ponownego" ? "Potwierdź ponownie" : "Zatwierdź"}: ${esc(naz)}</button></span>`;
}
async function nrPlanPlik(files) {
  if (!files.length) return; const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); fd.append("symbol", nrv("nrp-sym"));
  sledz(await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/plan/plik`, {method: "POST", body: fd})), () => otworzNier(NR_ID));
}
async function nrPlanLink() {
  const url = nrv("nrp-url").trim(); if (!url) return komunikat("Wklej link do uchwały, wypisu albo strony z planem.", true);
  sledz(await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/plan/link`, {json: {url, symbol: nrv("nrp-sym")}})), () => otworzNier(NR_ID));
}
async function nrPlanWybierz(symbol, przeznaczenie) {
  if (!symbol) return komunikat("Podaj symbol terenu, np. 2MN.", true);
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/plan/wybierz`, {json: {symbol, przeznaczenie: przeznaczenie || ""}})); if (r) { NRS = r; rysujNier(); komunikat("Ustawiono przeznaczenie: " + symbol); }
}
async function nrIdent(dodaj) {
  const json = {teryt: nrv("nr-teryt"), obreb_nr: nrv("nr-obnr"), adres: nrv("nr-teryt") || nrv("nr-obnr") ? "" : nrv("nr-adr"), dodaj};
  if (dodaj && !json.teryt && !json.obreb_nr) return komunikat("Wpisz identyfikator albo obręb i numer kolejnej działki.", true);
  if (!dodaj && NRS.dzialki.length > 1 && !confirm("Zastąpić wszystkie działki w teczce tą jedną?")) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/identyfikuj`, {json})); if (!r) return;
  if (r.wybor) return nrWyborDzialki(r, dodaj);
  NRS = r; rysujNier(); komunikat(dodaj ? "Dodano działkę – powierzchnia przeliczona." : "Zidentyfikowano działkę.");
  nrOstrzezenieLokalizacji();
}
// ta sama nazwa obrębu i numer działki w kilku gminach – wybór należy do użytkownika (program nie bierze po cichu pierwszej)
function nrWyborDzialki(r, dodaj) {
  const stare = $("#nr-wybor"); if (stare) stare.remove();
  const d = document.createElement("div"); d.id = "nr-wybor"; d.className = "karta"; d.style.borderColor = "#f59e0b";
  d.innerHTML = `<h3 style="margin-top:0">Wybierz działkę</h3><p>${esc(r.komunikat || "")}${r.liczba > r.wybor.length ? ` Pokazano ${r.wybor.length} z ${r.liczba} – doprecyzuj, wpisując identyfikator TERYT.` : ""}</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Działka</th><th>Obręb</th><th>Gmina / powiat / województwo</th><th>Pow. [m²]</th><th></th></tr>
    ${r.wybor.map(x => `<tr><td><b>${esc(x.numer || "")}</b><br><small class="opis">${esc(x.teryt || "")}</small></td><td>${esc(x.obreb || "")}</td>
      <td>${esc([x.gmina, x.powiat, x.wojewodztwo].filter(Boolean).join(" / "))}</td><td class="liczba">${x.pow_ewid ?? "–"}</td>
      <td><button class="glowny maly" onclick="nrWybierzTeryt('${escA(x.teryt)}', ${dodaj ? "true" : "false"})">Wybierz</button></td></tr>`).join("")}</table></div>
    <div class="pasek"><button class="maly" onclick="this.closest('#nr-wybor').remove()">Anuluj</button></div>`;
  const cel = $("#nier"); cel.prepend(d); d.scrollIntoView({behavior: "smooth", block: "start"});
}
async function nrWybierzTeryt(teryt, dodaj) {
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/identyfikuj`, {json: {teryt, dodaj}})); if (!r) return;
  NRS = r; rysujNier(); komunikat(dodaj ? "Dodano działkę – powierzchnia przeliczona." : "Zidentyfikowano działkę.");
}
function nrOstrzezenieLokalizacji() {
  const b = ((NRS && NRS.n && NRS.n.identyfikacja) || {}).budynek || {};
  if (b.ostrzezenie) komunikat("Lokalizacja przybliżona – " + b.ostrzezenie, true);
}
async function nrZatwierdz(k) {
  const uw = ($("#nr-uw-" + k) || {}).value || "";
  try { const r = await api(`/api/projekty/${NR_ID}/nier/punkt`, {json: {k, akcja: "zatwierdz", uwaga: uw}}); NRS = r; rysujNier(); komunikat("Zatwierdzono."); }
  catch (e) { komunikat(e.message, true); const p = $("#nr-uw-" + k); if (p && /uzasadnienie/.test(e.message)) { p.classList.add("pole-blad"); p.placeholder = "uzasadnienie – wymagane"; p.focus(); } }
}
async function nrArchiwizuj() {
  if (!confirm("Przenieść tę teczkę (DD / wycenę) do Archiwum? Możesz ją przywrócić z zakładki Archiwum.")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${NR_ID}`, {method: "DELETE"}))) { NR_ID = null; komunikat("Teczka w Archiwum."); ladujNier(); }
}
function nrFormMetody(S, w, T) {
  const pod = w.podejscie || "porownawcze", aktT = T.filter(t => !t.wykluczona), wyb = w.wybrane_parami || [], otr = w.oceny_tr || {}, cechy = w.cechy || [];
  if (pod === "kosztowe") { const kp = w.kosztowe_param || {}, kw = w.kosztowe || {}; return `<div class="siatka">
      <label>Cena gruntu [zł/m²]<input id="kp-gr" value="${esc(kp.cena_gruntu_m2 || "")}" placeholder="z transakcji działkami w okolicy"></label>
      <label>Koszt odtworzenia budynku [zł/m²]<input id="kp-odtw" value="${esc(kp.koszt_odtw_m2 || "")}" placeholder="domyślnie wg standardu: ${Object.entries(S.koszt_odtw).map(([a, b]) => a + " " + b).join(", ")}"></label>
      <label>Zużycie [%] (puste = z wieku i stanu)<input id="kp-zuz" value="${esc(kp.zuzycie_pct || "")}"></label><label>Budynki dodatkowe, zagospodarowanie [zł]<input id="kp-dod" value="${esc(kp.budynki_dodatkowe_zl || "")}"></label></div>
      <div class="pasek"><button class="glowny" data-ik="kalkulator" onclick="nrKosztowe()">Oblicz podejściem kosztowym</button></div>
      ${kw.wartosc ? `<div class="kwoty kafle-przetargu"><div><span>Grunt</span><b>${zl(kw.wartosc_gruntu)}</b></div><div><span>Budynek po zużyciu</span><b>${zl(kw.wartosc_budynku)}</b><small>zużycie ${kw.zuzycie_pct}% (wiek ${kw.wiek} / ${kw.trwalosc} lat)</small></div>
        <div><span>Dodatkowe</span><b>${zl(kw.dodatkowe)}</b></div><div><span>Wartość</span><b>${zl(kw.wartosc_zaokr)}</b></div></div>` : ""}`; }
  if (pod === "dochodowe") { const dp = w.dochodowe_param || {}, dw = w.dochodowe || {}, cz = w.czynsze_ofertowe; return `<div class="siatka">
      <label>Czynsz rynkowy [zł/m² miesięcznie]<input id="dp-cz" value="${esc(dp.czynsz_m2 || "")}"></label><label>Pustostany i niezapłacone czynsze [%]<input id="dp-pus" value="${esc(dp.pustostany_pct || "5")}"></label>
      <label>Koszty operacyjne [% dochodu] (albo kwota niżej)<input id="dp-kp" value="${esc(dp.koszty_pct || "15")}"></label><label>Koszty operacyjne [zł rocznie]<input id="dp-kz" value="${esc(dp.koszty_zl || "")}"></label>
      <label>Stopa kapitalizacji [%]<input id="dp-st" value="${esc(dp.stopa_pct || "")}" placeholder="z rynku – uzasadnij w operacie"></label></div>
      <div class="pasek"><button class="maly" data-ik="iskra" onclick="nrPost('wycena/czynsze')">Czynsze z ofert najmu (AI)</button>${cz ? `<span class="opis" style="margin:0">mediana ${zl(cz.mediana_m2)}/m² z ${cz.oferty.length} ofert (${esc(cz.data)})</span>` : ""}
        <button class="glowny" data-ik="kalkulator" onclick="nrMetoda('dochodowe')">Oblicz podejściem dochodowym</button></div>
      ${dw.wartosc ? `<div class="kwoty kafle-przetargu"><div><span>DOR (rocznie)</span><b>${zl(dw.dor)}</b><small>RDB ${zl(dw.rdb)} − koszty ${zl(dw.koszty)}</small></div><div><span>Stopa</span><b>${dw.stopa_pct}%</b></div><div><span>Wartość</span><b>${zl(dw.wartosc_zaokr)}</b></div></div>` : ""}`; }
  if (pod === "pozostalosciowa") { const zw = (NRS.n.zabudowa || {}).wynik || {}, pw = w.pozostalosciowa || {}; return `<p class="opis">Wartość gruntu inwestycyjnego z analizy zabudowy: wartość po realizacji − koszty budowy i dodatkowe − zysk inwestora. Włącz „Analiza zabudowy” i przelicz scenariusze.</p>
      <div class="pasek"><select id="po-sc">${(zw.scenariusze || []).filter(s => s.max_cena != null).map(s => `<option value="${s.id}">${esc(s.nazwa)} – ${esc(s.wynik)}</option>`).join("")}</select>
        <button class="glowny" data-ik="kalkulator" onclick="nrMetoda('pozostalosciowa')">Oblicz metodą pozostałościową</button></div>
      ${pw.wartosc ? `<div class="kwoty kafle-przetargu"><div><span>Po realizacji</span><b>${zl(pw.wartosc_po_realizacji)}</b></div><div><span>Koszty i zysk</span><b>${zl(pw.koszt_budowy + pw.koszty_dodatkowe + pw.zysk_inwestora)}</b></div><div><span>Wartość gruntu</span><b>${zl(pw.wartosc_zaokr)}</b></div></div>` : ""}`; }
  if (pod === "wskazniki") { const wp = w.wskazniki_param || {}, ww = w.wskazniki || {}, kl = (wp.klasy || []).concat(Array(Math.max(0, 5 - (wp.klasy || []).length)).fill({}));
    return `<p class="opis">Metoda dla gruntów rolnych i leśnych przy braku transakcji: Σ (powierzchnia klasy × wskaźnik [dt/ha]) × cena 1 dt (żyta albo drewna). <b>Wskaźniki i cenę wpisz z przepisów i aktualnego komunikatu</b> – program ich nie zakłada; w operacie będą wyróżnione do potwierdzenia.</p>
      <div class="siatka"><label>Cena 1 dt [zł]<input id="ws-cena" value="${esc(wp.cena_dt || "")}"></label><label>Źródło ceny<input id="ws-zr" value="${esc(wp.zrodlo_ceny || "")}" placeholder="np. komunikat GUS – średnia cena skupu żyta"></label>
        <label>Korekta [%] (opcjonalnie)<input id="ws-kor" value="${esc(wp.korekta_pct || "")}"></label></div>
      <div class="tabela-okno"><table class="tabela"><tr><th>Klasa / użytek</th><th>Powierzchnia [ha]</th><th>Wskaźnik [dt/ha]</th></tr>
        ${kl.map(k => `<tr><td><input class="ws-kl" value="${esc(k.klasa || "")}" placeholder="np. RIIIa"></td><td><input class="ws-pow" value="${esc(k.pow_ha || "")}"></td><td><input class="ws-wsk" value="${esc(k.wskaznik || "")}"></td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="glowny" data-ik="kalkulator" onclick="nrMetoda('wskazniki')">Oblicz metodą wskaźników</button></div>
      ${ww.wartosc ? `<div class="kwoty kafle-przetargu"><div><span>Suma</span><b>${zl(ww.suma)}</b></div><div><span>Korekta</span><b>${ww.korekta_pct}%</b></div><div><span>Wartość</span><b>${zl(ww.wartosc_zaokr)}</b></div></div>` : ""}`; }
  if (pod === "parami") { const pr = w.parami || {}; return `<p class="opis">Wybierz co najmniej 3 transakcje najbardziej podobne do przedmiotu wyceny i oceń ich cechy na tle przedmiotu (ocenę przedmiotu ustawiasz w punkcie 6).</p>
      ${aktT.length ? `<div class="tabela-okno"><table class="tabela"><tr><th></th><th>Transakcja</th><th>zł/m²</th>${cechy.map(c => `<th>${esc(c.nazwa)}</th>`).join("")}</tr>
        ${aktT.map(t => `<tr><td><input type="checkbox" class="pr-wyb" value="${t.id}" ${wyb.includes(t.id) ? "checked" : ""}></td><td>${esc(t.data)} ${esc(t.lokalizacja || "")}</td><td class="liczba">${zl(t.cena_m2)}</td>
          ${cechy.map(c => `<td><select class="pr-oc" data-t="${t.id}" data-c="${esc(c.nazwa)}">${[[1, "gorsza"], [2, "przeciętna"], [3, "lepsza"]].map(([v, x]) => `<option value="${v}" ${(+((otr[t.id] || {})[c.nazwa] || 2)) === v ? "selected" : ""}>${x}</option>`).join("")}</select></td>`).join("")}</tr>`).join("")}</table></div>` : '<p class="pusto">Brak przyjętych transakcji – wgraj je w punkcie 4.</p>'}
      <div class="pasek"><button class="glowny" data-ik="kalkulator" onclick="nrMetoda('parami')">Oblicz metodą porównywania parami</button></div>
      ${pr.wartosc ? `<div class="kwoty kafle-przetargu"><div><span>Transakcji</span><b>${pr.liczba}</b></div><div><span>Cena jednostkowa</span><b>${zl(pr.cena_m2)}/m²</b></div><div><span>Wartość</span><b>${zl(pr.wartosc_zaokr)}</b></div></div>` : ""}`; }
  return '<p class="opis">Metoda korygowania ceny średniej – cechy, wagi i obliczenia w punkcie 6 (zalecane co najmniej ' + ((S.min_metody || {}).porownawcze || 12) + " transakcji).</p>";
}
async function nrPrzywroc(kategoria) { const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/przywroc`, {json: {kategoria}})); if (r) { NRS = r; rysujNier(); komunikat(r.komunikat || "Gotowe."); } }
async function nrNowaWycena(tryb) {
  const pyt = tryb === "aktualizacja" ? "Zaktualizować operat? Obecna wycena trafi do archiwum teczki; nowa ma dzisiejszą datę wyceny, te same założenia i transakcje (dodaj nowe), a punkty kontrolne trzeba potwierdzić ponownie."
    : "Rozpocząć nową wycenę w tej teczce (np. inny cel albo rodzaj wartości)? Obecna wycena trafi do archiwum teczki.";
  if (!confirm(pyt)) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/nowa`, {json: {tryb}})); if (r) { NRS = r; rysujNier(); komunikat(tryb === "aktualizacja" ? "Aktualizacja operatu – uzupełnij transakcje i potwierdź punkty." : "Nowa wycena – poprzednia w archiwum teczki."); }
}
async function nrUstawienia() {
  const el = $("#nr-ust"); if (el.innerHTML) { el.innerHTML = ""; return; }
  const d = await bezpiecznie(() => api("/api/nier/ustawienia")); if (!d) return;
  el.innerHTML = `<div class="karta" style="margin:0 0 12px;border-left:4px solid #1F5A99"><b>Ustawienia rzeczoznawcy – założenia metod</b> <span class="opis">(dla Twojego konta; zmiany przelicza się przy kolejnych obliczeniach)</span>
    <div class="siatka" style="margin-top:8px">${Object.entries(d.opisy).map(([k, t]) => k === "uzasadnienie" ? `<label style="grid-column:1/-1">${esc(t)}<textarea id="nu-${k}">${esc(d.ustawienia[k] || "")}</textarea></label>`
      : `<label>${esc(t)}<input id="nu-${k}" value="${esc(String(d.ustawienia[k]))}"><small class="opis">domyślnie ${esc(String(d.domyslne[k]))}</small></label>`).join("")}</div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="nrUstawieniaZapisz()">Zapisz ustawienia</button><button class="maly" onclick="$('#nr-ust').innerHTML = ''">Zamknij</button></div></div>`;
}
async function nrUstawieniaZapisz() {
  const u = {}; document.querySelectorAll("[id^='nu-']").forEach(e => u[e.id.slice(3)] = e.value);
  if (await bezpiecznie(() => api("/api/nier/ustawienia", {json: {ustawienia: u}}))) { komunikat("Zapisano ustawienia rzeczoznawcy."); $("#nr-ust").innerHTML = ""; otworzNier(NR_ID); }
}
async function nrWlZapisz(json) { const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wlasna`, {json})); if (r) { NRS = r; rysujNier(); } return r; }
async function nrWlOblicz() {
  const oferty = {}; document.querySelectorAll(".wl-oc").forEach(e => { (oferty[e.dataset.o] = oferty[e.dataset.o] || {})[e.dataset.c] = +e.value; });
  const r = await nrWlZapisz({oferty: Object.entries(oferty).map(([id, oceny]) => ({id, oceny})), korekta_pct: nrv("wl-kor"), oblicz: true});
  if (r) komunikat("Obliczono wycenę własną.");
}
async function nrPoszerz() { const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/poszerz`, {method: "POST"})); if (r) { NRS = r; rysujNier(); komunikat(r.komunikat || "Gotowe."); } }
function nrCechyZFormularza() {
  const cechy = [...document.querySelectorAll(".w-cn")].map((e, k) => ({nazwa: e.value, waga: document.querySelectorAll(".w-cw")[k].value}));
  const oceny = {}; cechy.forEach((c, k) => oceny[c.nazwa] = +document.querySelectorAll(".w-co")[k].value);
  return {cechy, oceny};
}
async function nrZapiszCechy() { await nrZapisz({wycena: nrCechyZFormularza()}); }
async function nrMetoda(metoda) {
  if (document.querySelector(".w-cn")) await nrZapisz({wycena: nrCechyZFormularza()}, true);
  const json = {metoda};
  if (metoda === "parami") { json.wybrane = [...document.querySelectorAll(".pr-wyb:checked")].map(e => e.value); json.oceny_tr = {};
    document.querySelectorAll(".pr-oc").forEach(e => { (json.oceny_tr[e.dataset.t] = json.oceny_tr[e.dataset.t] || {})[e.dataset.c] = +e.value; }); }
  if (metoda === "dochodowe") json.param = {czynsz_m2: nrv("dp-cz"), pustostany_pct: nrv("dp-pus"), koszty_pct: nrv("dp-kp"), koszty_zl: nrv("dp-kz"), stopa_pct: nrv("dp-st")};
  if (metoda === "pozostalosciowa") json.scenariusz = nrv("po-sc");
  if (metoda === "wskazniki") json.param = {cena_dt: nrv("ws-cena"), zrodlo_ceny: nrv("ws-zr"), korekta_pct: nrv("ws-kor"),
    klasy: [...document.querySelectorAll(".ws-kl")].map((e, k) => ({klasa: e.value, pow_ha: document.querySelectorAll(".ws-pow")[k].value, wskaznik: document.querySelectorAll(".ws-wsk")[k].value})).filter(x => x.pow_ha)};
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/metoda`, {json})); if (r) { NRS = r; rysujNier(); komunikat("Obliczono."); }
}
function nrZapiszZakres() {
  const cel = nrv("nrw-cel") === "inny cel" ? (nrv("nrw-cel-inny").trim() || "inny cel") : nrv("nrw-cel");
  nrZapisz({wycena: {cel, rodzaj_wartosci: nrv("nrw-rodz"), data_wyceny: nrv("nrw-data"), stan_na: nrv("nrw-stan"), zamawiajacy: nrv("nrw-zam"), rzeczoznawca: nrv("nrw-rz"), nr_uprawnien: nrv("nrw-nr")}});
}
function nrZapiszDane() {
  const dane = {nazwa: nrv("nr-nazwa"), typ: nrv("nr-typ"), cel: nrv("nr-cel"), cena: nrv("nr-cena"), pow_dzialki: nrv("nr-pdz"), pow_przedmiotu: nrv("nr-pp"), kw: nrv("nr-kw")};
  document.querySelectorAll(".nr-obj").forEach(e => dane[e.dataset.k] = e.value);
  nrZapisz({dane});
}
async function nrKosztowe() {
  await nrZapisz({wycena: {kosztowe_param: {cena_gruntu_m2: nrv("kp-gr"), koszt_odtw_m2: nrv("kp-odtw"), zuzycie_pct: nrv("kp-zuz"), budynki_dodatkowe_zl: nrv("kp-dod")}}}, true);
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/kosztowe`, {method: "POST"})); if (r) { NRS = r; rysujNier(); komunikat("Obliczono podejściem kosztowym."); }
}
function nrZapiszOgl() {
  const punkty = {}; document.querySelectorAll(".og-oc").forEach(e => { punkty[e.dataset.p] = {ocena: e.value, uwagi: (document.querySelector(`.og-uw[data-p="${CSS.escape(e.dataset.p)}"]`) || {}).value || ""}; });
  nrZapisz({ogledziny: {data: nrv("og-data"), osoba: nrv("og-osoba"), punkty}});
}
function nrRyzyko(id) {
  const tr = document.querySelector(`tr[data-r="${id}"]`); const v = c => tr.querySelector(c).value;
  nrZapisz({ryzyko: {id, waga: v(".r-waga"), obszar: v(".r-obszar"), opis: v(".r-opis"), status: v(".r-status"), koszt_zl: v(".r-koszt"), zapis_umowy: v(".r-umowa")}});
}
function nrZapiszZab() {
  const parametry = {}, ceny = {}; document.querySelectorAll(".zb-p").forEach(e => parametry[e.dataset.k] = e.value); document.querySelectorAll(".zb-c").forEach(e => ceny[e.dataset.k] = e.value);
  nrZapisz({zabudowa: {parametry: Object.assign(parametry, {zrodlo: (NRS.n.zabudowa.parametry || {}).zrodlo || "wpisane ręcznie"}), ceny}});
}
async function nrOblicz() {
  const cechy = [...document.querySelectorAll(".w-cn")].map((e, k) => ({nazwa: e.value, waga: document.querySelectorAll(".w-cw")[k].value}));
  const oceny = {}; cechy.forEach((c, k) => oceny[c.nazwa] = +document.querySelectorAll(".w-co")[k].value);
  await nrZapisz({wycena: {cechy, oceny}}, true);
  const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/wycena/oblicz`, {method: "POST"})); if (r && r.n) { NRS = r; rysujNier(); komunikat("Obliczono wartość."); }
}
async function nrPlikWyczysc() { const fd = new FormData(); fd.append("wyczysc", "1"); const r = await bezpiecznie(() => api(`/api/projekty/${NR_ID}/nier/transakcje`, {body: fd, method: "POST"})); if (r) { NRS = r; rysujNier(); } }

// ================================================================ BENEFICJENT DOTACJI – zasada konkurencyjności
let ZQ_ID = null, ZQD = null;
async function ladujZapytania() {
  const l = await bezpiecznie(() => api("/api/zapytania")); if (!l) return;
  $("#lista-zapytan").innerHTML = l.map(p => `<li class="${p.id === ZQ_ID ? "akt" : ""}" onclick="otworzZapytanie('${p.id}')">${esc(p.nazwa)}
    <small>${p.dotacja ? esc(p.dotacja) + " · " : ""}${p.gotowe}/${p.razem} wymagań${p.wybrany ? " · wybrany: " + esc(p.wybrany) : ""}</small></li>`).join("") || '<li class="pusto">Brak zapytań.</li>';
  if (ZQ_ID && l.some(p => p.id === ZQ_ID)) otworzZapytanie(ZQ_ID); else if (l.length) otworzZapytanie(l[0].id);
  else $("#zapytanie").innerHTML = `<div class="karta"><h2 style="margin-top:0">Wybór wykonawcy zgodnie z zasadą konkurencyjności</h2>
    <p>Przy zakupach w projekcie dotacji powyżej 80 000 zł netto (od 25.03.2025 r.; wcześniej 50 000 zł) trzeba wybrać wykonawcę zgodnie z zasadą konkurencyjności, a błąd może skończyć się uznaniem
    całości lub części wydatku za niekwalifikowany. Program prowadzi przez całe postępowanie: zapytanie ofertowe, publikację w Bazie Konkurencyjności,
    ocenę ofert i protokół – a dokumenty trafiają do rozliczenia dotacji.</p>
    <button class="glowny" data-ik="plus" onclick="noweZapytanie()">Nowe zapytanie ofertowe</button></div>`;
  wstawIkony($("#w-dot_zapytania"));
}
async function noweZapytanie(dotacjaId) {
  const nazwa = prompt("Co kupujesz w projekcie? (np. Dostawa i montaż pompy ciepła, Termomodernizacja budynku):"); if (!nazwa) return;
  const p = await bezpiecznie(() => api("/api/projekty", {json: {nazwa, typ: "zapytanie", dotacja_id: dotacjaId || ""}}));
  if (p) { ZQ_ID = p.id; if (WIDOK !== "dot_zapytania") pokaz("dot_zapytania"); else ladujZapytania(); }
}
async function otworzZapytanie(id) {
  ZQ_ID = id; document.querySelectorAll("#lista-zapytan li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  ZQD = await bezpiecznie(() => api(`/api/projekty/${id}/zapytanie`)); if (ZQD) rysujZapytanie();
}
async function zapiszZapytanie(czesc) {
  const v = id => ($("#" + id) || {}).value || "";
  const ch = id => !!($("#" + id) || {}).checked;
  const json = czesc === "dane" ? {dane: {przedmiot: v("zq-przedmiot"), rodzaj: v("zq-rodzaj"), wartosc_netto: v("zq-wartosc"), data_szacowania: v("zq-data-sz"), data_wszczecia: v("zq-data-wsz"),
      termin_realizacji: v("zq-termin-real"), opis: v("zq-opis"), beneficjent: v("zq-ben"), zamawiajacy_pzp: ch("zq-pzp"), progi_unijne: ch("zq-unijne"),
      czesci_innych_zakupow: ch("zq-czesci")}, dotacja_id: v("zq-dotacja")}
    : czesc === "publikacja" ? {publikacja: {numer: v("zq-bk-nr"), data: v("zq-bk-data"), termin: v("zq-bk-termin"), zmiany: v("zq-bk-zmiany"), wynik_data: v("zq-bk-wynik")}}
    : {};
  ZQD = await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie`, {json})); if (ZQD) { rysujZapytanie(); komunikat("Zapisano."); ladujListeZapytanCicho(); }
}
async function ladujListeZapytanCicho() { const l = await api("/api/zapytania").catch(() => null); if (l) $("#lista-zapytan").innerHTML = l.map(p => `<li class="${p.id === ZQ_ID ? "akt" : ""}" onclick="otworzZapytanie('${p.id}')">${esc(p.nazwa)}<small>${p.gotowe}/${p.razem} wymagań${p.wybrany ? " · wybrany: " + esc(p.wybrany) : ""}</small></li>`).join(""); }
async function punktListyZq(id, ok) { ZQD = await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie`, {json: {lista: {[id]: ok}}})); if (ZQD) rysujZapytanie(); }
async function dokumentyZapytania() { sledz(await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie/dokumenty`, {method: "POST"})), () => otworzZapytanie(ZQ_ID)); }
async function ocenaZapytania() {
  const r = await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie/ocena`, {method: "POST"})); if (!r) return;
  OC_ID = r.id; pokaz("zam_oferty");
}
async function protokolZapytania() { ZQD = await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie/protokol`, {method: "POST"})); if (ZQD) { rysujZapytanie(); komunikat("Protokół przygotowany."); } }
async function doRozliczenia() {
  const r = await bezpiecznie(() => api(`/api/projekty/${ZQ_ID}/zapytanie/do-rozliczenia`, {method: "POST"}));
  if (r && r.ok) { komunikat(`Przekazano ${r.plikow} plików do rozliczenia dotacji (${r.folder}).`); otworzZapytanie(ZQ_ID); }
}
function rysujZapytanie() {
  const D = ZQD, Z = D.Z || {}, d = Z.dane || {}, w = D.wymagania, pub = Z.publikacja || {}, t = Z.tresc || {}, oc = D.ocena;
  const tryKol = {zk: "z-do-analizy", pzp: "z-czerwony", ponizej: "z-startujemy"}[w.tryb] || "z-odpuszczamy";
  const pl = f => `<a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${D.projekt.id}/zapytanie/plik/${encodeURIComponent(f)}">${esc(f.replace(/_/g, " ").replace(/\.docx$/, ""))}</a>`;
  const minTermin = pub.data ? new Date(new Date(pub.data).getTime() + (w.min_dni + 1) * 864e5).toISOString().slice(0, 10) : "";
  $("#zapytanie").innerHTML = `
  <div class="naglowek"><h2 style="margin:0">${esc(D.projekt.nazwa)}</h2></div>
  <div class="kwoty kafle-przetargu"><div><span>Projekt dotacji</span><b style="font-size:14px">${esc(D.dotacja.nazwa || "– wybierz w kroku 1")}</b></div>
    <div><span>Wartość netto</span><b>${d.wartosc_netto ? zl(liczbaPL(d.wartosc_netto)) : "–"}</b></div>
    <div><span>Tryb</span><b style="font-size:14px"><span class="znacznik ${tryKol}">${esc({zk: "zasada konkurencyjności", pzp: "ustawa Pzp", ponizej: "poniżej progu"}[w.tryb] || "do ustalenia")}</span></b></div>
    <div><span>Lista kontrolna</span><b>${D.lista.filter(x => x.ok).length}/${D.lista.length}</b></div></div>
  <div class="krok" id="sek-zq-dane"><div class="tytul"><span class="nr">${ik("teczka")}</span><h3>1. Zamówienie i projekt dotacji</h3></div><div class="tresc">
    <div class="siatka">
      <label style="grid-column:1/-1">Projekt dotacji, którego dotyczy zakup<select id="zq-dotacja"><option value="">– wybierz –</option>${D.dotacje.map(x => `<option value="${x.id}" ${x.id === Z.dotacja_id ? "selected" : ""}>${esc(x.nazwa)}</option>`).join("")}</select></label>
      <label style="grid-column:1/-1">Przedmiot zamówienia<input id="zq-przedmiot" value="${esc(d.przedmiot || "")}"></label>
      <label>Rodzaj<select id="zq-rodzaj">${[["roboty", "roboty budowlane"], ["dostawy", "dostawy"], ["uslugi", "usługi"]].map(([k, n]) => `<option value="${k}" ${k === (d.rodzaj || "roboty") ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      <label>Szacunkowa wartość netto [zł]<input id="zq-wartosc" value="${esc(d.wartosc_netto || "")}"></label>
      <label>Data ustalenia wartości<input type="date" id="zq-data-sz" value="${esc(d.data_szacowania || "")}"></label>
      <label>Data wszczęcia postępowania<input type="date" id="zq-data-wsz" value="${esc(d.data_wszczecia || "")}"></label>
      <label>Termin realizacji<input id="zq-termin-real" value="${esc(d.termin_realizacji || "")}" placeholder="np. do 30.06.2027"></label>
      <label style="grid-column:1/-1">Beneficjent (zamawiający)<input id="zq-ben" value="${esc(d.beneficjent || "")}"></label>
      <label style="grid-column:1/-1">Opis potrzeb (co, ile, parametry, miejsce)<textarea id="zq-opis" style="min-height:80px">${esc(d.opis || "")}</textarea></label>
      <label class="wiersz"><input type="checkbox" id="zq-pzp" ${d.zamawiajacy_pzp ? "checked" : ""}> Beneficjent jest zamawiającym publicznym (gmina, szkoła, szpital…)</label>
      <label class="wiersz"><input type="checkbox" id="zq-unijne" ${d.progi_unijne ? "checked" : ""}> Wartość od progów unijnych</label>
      <label class="wiersz" style="grid-column:1/-1"><input type="checkbox" id="zq-czesci" ${d.czesci_innych_zakupow ? "checked" : ""}> W projekcie są inne zakupy tego samego rodzaju (sprawdzenie dzielenia zamówienia)</label></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszZapytanie('dane')">Zapisz i ustal tryb</button></div>
    <div class="ramka-uwaga" style="border-color:#1F5A99"><b>${esc(w.opis)}</b>${w.tryb === "zk" ? `<br>${esc(w.min_dni_opis)}` : ""}
      ${w.ostrzezenia.map(x => `<br>⚠ ${esc(x)}`).join("")}</div></div></div>
  <div class="krok" id="sek-zq-dok"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>2. Zapytanie ofertowe i oświadczenia</h3><span class="stan">${D.pliki.length ? D.pliki.length + " dokumentów" : "do zrobienia"}</span></div><div class="tresc">
    <p class="opis">AI przygotowuje zapytanie zgodne z zasadą konkurencyjności na podstawie opisu potrzeb, dokumentów projektu dotacji i materiałów wgranych do zamówienia:
      opis przedmiotu bez wskazywania marek, proporcjonalne warunki udziału, kryteria z wagami, terminy. Do tego formularz ofertowy i oświadczenia o braku powiązań.</p>
    <div class="pasek"><button class="zolty" data-ik="iskra" onclick="dokumentyZapytania()">${D.pliki.some(f => f.startsWith("Zapytanie")) ? "Przygotuj ponownie (AI)" : "Przygotuj zapytanie ofertowe (AI)"}</button></div>
    ${D.pliki.length ? `<div class="pasek">${D.pliki.map(pl).join(" ")}</div>` : ""}
    ${(t.kryteria || []).length ? `<h4 class="grupa-analizy">Kryteria oceny</h4><ul class="lista">${t.kryteria.map(k => `<li><b>${esc(k.nazwa)}</b> – ${esc(String(k.waga || ""))}%${k.opis ? ": " + esc(k.opis) : ""}</li>`).join("")}</ul>` : ""}
    ${(t.ryzyka || []).length ? `<div class="ramka-uwaga"><b>Na co uważać przy kontroli:</b><ul class="lista">${t.ryzyka.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}</div></div>
  <div class="krok" id="sek-zq-bk"><div class="tytul"><span class="nr">${ik("szukaj")}</span><h3>3. Publikacja w Bazie Konkurencyjności</h3><span class="stan">${pub.numer ? "opublikowano" : "do zrobienia"}</span></div><div class="tresc">
    <p class="opis">Opublikuj zapytanie w <a href="https://bazakonkurencyjnosci.funduszeeuropejskie.gov.pl/" target="_blank" rel="noopener">Bazie Konkurencyjności ↗</a> i wpisz numer ogłoszenia.
      Termin składania ofert: co najmniej <b>${w.min_dni} dni</b> od dnia następującego po publikacji${minTermin ? ` – najwcześniej <b>${esc(dataPl(minTermin))}</b>` : ""}.</p>
    <div class="siatka"><label>Numer ogłoszenia w BK<input id="zq-bk-nr" value="${esc(pub.numer || "")}"></label>
      <label>Data publikacji<input type="date" id="zq-bk-data" value="${esc(pub.data || "")}"></label>
      <label>Termin składania ofert<input type="date" id="zq-bk-termin" value="${esc((pub.termin || "").slice(0, 10))}"></label>
      <label>Wynik opublikowany w BK (data)<input type="date" id="zq-bk-wynik" value="${esc(pub.wynik_data || "")}"></label>
      <label style="grid-column:1/-1">Zmiany zapytania / pytania wykonawców<textarea id="zq-bk-zmiany">${esc(pub.zmiany || "")}</textarea></label></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszZapytanie('publikacja')">Zapisz publikację</button></div>
    ${pub.termin && minTermin && pub.termin.slice(0, 10) < minTermin ? `<div class="ramka-uwaga">⚠ Termin składania ofert jest krótszy niż ${w.min_dni} dni – instytucja może uznać wydatek za niekwalifikowany. Wydłuż termin.</div>` : ""}</div></div>
  <div class="krok" id="sek-zq-oferty"><div class="tytul"><span class="nr">${ik("trofeum")}</span><h3>4. Oferty i wybór wykonawcy</h3><span class="stan">${oc ? odm(oc.ofert, "oferta", "oferty", "ofert") : "po terminie ofert"}</span></div><div class="tresc">
    <p class="opis">Program bada każdą ofertę z zapytaniem, liczy punkty według kryteriów z zapytania i wskazuje najkorzystniejszą – tak jak przy zamówieniach publicznych.</p>
    <div class="pasek"><button class="${oc ? "maly" : "zolty"}" data-ik="trofeum" onclick="ocenaZapytania()">${oc ? "Otwórz sprawdzenie ofert" : "Sprawdź złożone oferty"}</button></div>
    ${oc ? `<p>Ofert: <b>${oc.ofert}</b>${oc.najkorzystniejsza ? ` · najkorzystniejsza: <b>${esc(oc.najkorzystniejsza)}</b> (${pkt(oc.punkty)} pkt)` : ""}</p>` : ""}</div></div>
  <div class="krok" id="sek-zq-prot"><div class="tytul"><span class="nr">${ik("protokol")}</span><h3>5. Protokół i dokumenty do rozliczenia</h3><span class="stan">${Z.przekazano ? "przekazano " + esc(Z.przekazano) : ""}</span></div><div class="tresc">
    <div class="pasek"><button class="glowny" data-ik="protokol" onclick="protokolZapytania()">Przygotuj protokół z postępowania</button>
      <button class="maly" data-ik="portfel" onclick="doRozliczenia()">Przekaż komplet do rozliczenia dotacji</button></div>
    <h4 class="grupa-analizy">Lista kontrolna – to, co sprawdza instytucja</h4>
    <ul class="lista" style="list-style:none;padding-left:0">${D.lista.map(x => `<li><label class="wiersz"><input type="checkbox" ${x.ok ? "checked" : ""} onchange="punktListyZq('${x.id}', this.checked)"> ${esc(x.opis)}</label></li>`).join("")}</ul>
    <p class="opis">Reguły według Wytycznych dotyczących kwalifikowalności wydatków na lata 2021–2027 – porównaj z umową o dofinansowanie i wytycznymi Twojego programu.</p></div></div>`;
  wstawIkony($("#zapytanie"));
  setTimeout(odswiezPodmenu, 100);
}
async function kartaZamowienDotacji() {  // w projekcie dotacji: zamówienia w projekcie i ich stan
  const el = $("#dot-zamowienia"); if (!el || !PROJEKT_ID) return;
  const l = await api(`/api/zapytania?dotacja=${PROJEKT_ID}`).catch(() => []);
  el.innerHTML = `<div class="krok"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Zamówienia w projekcie – zasada konkurencyjności</h3><span class="stan">${l.length ? odm(l.length, "zamówienie", "zamówienia", "zamówień") : ""}</span></div><div class="tresc">
    <p class="opis">Zakupy powyżej 80 000 zł netto – wybór wykonawcy zgodnie z zasadą konkurencyjności. Komplet dokumentów postępowania trafia do dokumentów rozliczenia.</p>
    ${l.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Zamówienie</th><th>Wartość netto</th><th>Lista kontrolna</th><th>Wybrany wykonawca</th><th></th></tr>
      ${l.map(z => `<tr><td><b>${esc(z.nazwa)}</b></td><td class="liczba">${z.wartosc ? zl(liczbaPL(z.wartosc)) : "–"}</td><td>${z.gotowe}/${z.razem}</td><td>${esc(z.wybrany || "–")}</td>
        <td><button class="maly" onclick="ZQ_ID='${z.id}'; pokaz('dot_zapytania')">Otwórz</button></td></tr>`).join("")}</table></div>` : ""}
    <div class="pasek"><button class="glowny" data-ik="plus" onclick="noweZapytanie('${PROJEKT_ID}')">Nowe zapytanie ofertowe w tym projekcie</button></div></div></div>`;
  wstawIkony(el);
}
async function ladujOceny() {
  if (STRONA === "zamawiajacy" && MZ().ocena_wg_zapytan && WIDOK !== "pr_oferty") return ladujOcenyWsp();
  const l = await bezpiecznie(() => api("/api/ocena-ofert" + (WIDOK === "pr_oferty" ? "?strona=prawnik" : "?modul=" + MZ().klucz))); if (!l) return;
  $("#lista-ocen").innerHTML = l.map(p => `<li class="${p.id === OC_ID ? "akt" : ""}" onclick="otworzOcene('${p.id}')">${esc(p.nazwa)}
    <small>${odm(p.ofert, "oferta", "oferty", "ofert")}${p.warunkowo ? " · wybór wstrzymany" : p.najkorzystniejsza ? " · wybrana: " + esc(p.najkorzystniejsza) : ""}</small></li>`).join("") || '<li class="pusto">Brak postępowań.</li>';
  if (OC_ID && l.some(p => p.id === OC_ID)) otworzOcene(OC_ID); else if (l.length) otworzOcene(l[0].id);
}
async function ladujOcenyWsp() {  // wspólnota: każde zapytanie ma swoje sprawdzenie ofert (oferty wgrywane z Bazy Konkurencyjności, e-maila albo papieru)
  const [Z, O] = await Promise.all([api("/api/zam/zapytania").catch(() => []), api("/api/ocena-ofert?modul=wspolnota").catch(() => [])]);
  const powiazane = new Set(Z.map(x => x.ocena_id).filter(Boolean));
  $("#lista-ocen").innerHTML = Z.map(x => `<li class="${x.ocena_id && x.ocena_id === OC_ID ? "akt" : ""}" onclick="ocDlaZapytania('${x.id}')">${esc(x.nazwa)}
      <small>zapytanie · ${odm(x.oferty, "oferta", "oferty", "ofert")}${x.termin_ofert ? " · termin " + dataPl(x.termin_ofert) : ""}</small></li>`).join("")
    + O.filter(o => !powiazane.has(o.id)).map(p => `<li class="${p.id === OC_ID ? "akt" : ""}" onclick="otworzOcene('${p.id}')">${esc(p.nazwa)} <small>${odm(p.ofert, "oferta", "oferty", "ofert")}</small></li>`).join("")
    || '<li class="opis">Brak zapytań – przygotuj zamówienie, a oferty sprawdzisz tutaj.</li>';
  if (OC_ID) otworzOcene(OC_ID);
}
async function nowaOcena() {
  const nazwa = prompt("Nazwa postępowania (np. Termomodernizacja szkoły w Marcinowicach):"); if (!nazwa) return;
  const p = await bezpiecznie(() => api("/api/projekty", {json: {nazwa, typ: "ocena_ofert", prawnik: WIDOK === "pr_oferty" ? {} : undefined, prywatny: WIDOK !== "pr_oferty" && MZ().prywatny}})); if (p) { OC_ID = p.id; ladujOceny(); }
}
async function otworzOcene(id) {
  OC_ID = id; document.querySelectorAll("#lista-ocen li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  OCD = await bezpiecznie(() => api(`/api/projekty/${id}/ocena`)); if (OCD) rysujOcene();
}
const stanOc = s => ({"prawidłowa": "z-startujemy", "do wyjaśnienia": "z-do-analizy", "do uzupełnienia": "z-do-analizy", "do odrzucenia": "z-czerwony"})[s] || "z-odpuszczamy";
function rysujOcene() {
  const O = OCD.O, swz = O.swz || {}, P = O.podsum || {}, el = $("#ocena");
  const krok = (nr, t, kol, tresc, stan = "") => `<div class="krok ${kol}"><div class="tytul"><span class="nr">${nr}</span><h3>${t}</h3><span class="stan">${stan}</span></div><div class="tresc">${tresc}</div></div>`;
  const lista = (L, oid) => (L || []).length ? `<ul class="lista">${L.map(x => `<li>${esc(typeof x === "string" ? x : (x.opis || "") + (x.poprawka ? " → " + x.poprawka : ""))}${x && x.odw ? " " + odwChip(x.odw, x.miejsce, {typ: "projekt", id: OC_ID}) : ""}</li>`).join("")}</ul>` : "";
  const ranking = O.oferty.filter(o => o.miejsce).sort((a, b) => a.miejsce - b.miejsce);
  const kryt = swz.kryteria || [];
  el.innerHTML = `${OCD.projekt.zapytanie_id ? `<div class="pasek" style="margin:0 0 8px"><button class="maly" onclick="ZQ_ID='${OCD.projekt.zapytanie_id}'; pokaz('dot_zapytania')">← Wróć do zapytania ofertowego (zasada konkurencyjności)</button></div>` : ""}<div class="pulpit-glowka"><h2>${esc(OCD.projekt.nazwa)}</h2></div>
  ${krok(1, "Dokumenty postępowania (SWZ, OPZ, formularze)", "k-nieb", `<div class="pliki-ik">${OCD.swz_pliki.map(f => `<span class="znacznik z-odpuszczamy">${esc(f)}</span>`).join(" ") || '<span class="opis">Brak dokumentów.</span>'}</div>
    <div class="pasek"><label class="przycisk maly" data-ik="wgraj">Wgraj SWZ i załączniki<input type="file" multiple hidden onchange="wgrajSwz(this.files)"></label></div>`, OCD.swz_pliki.length + " plików")}
  ${krok(2, "Kryteria oceny i wymagania", "k-ziel", `${!kryt.length ? '<p class="opis">AI odczyta z SWZ kryteria oceny z wagami i sposobem liczenia punktów, wymagane dokumenty, warunki udziału i kwotę przeznaczoną na zamówienie.</p>' : ""}
    <div class="pasek"><button data-ik="iskra" onclick="swzOceny()">${kryt.length ? "Odczytaj ponownie z SWZ" : "Odczytaj kryteria z SWZ (AI)"}</button></div>
    ${kryt.length ? `<div class="tabela-okno"><table class="tabela" id="oc-kryt"><tr><th>Kryterium</th><th>Waga [pkt]</th><th>Lepsza wartość</th><th title="Tylko „wyższa”: wartość za 0 pkt i wartość, od której pełna liczba punktów (np. gwarancja 60–84 mies.). Puste – porównanie z najlepszą ofertą.">Punktowana od–do</th><th>Sposób oceny (z SWZ)</th></tr>
      ${kryt.map((k, i) => `<tr data-i="${i}"><td><input class="k-n" value="${esc(k.nazwa)}"></td><td><input class="k-w" value="${k.waga}" style="width:70px"></td>
        <td><select class="k-t">${[["min", "niższa (cena, termin)"], ["max", "wyższa (gwarancja)"], ["punktowe", "punkty wg opisu"]].map(([v, t]) => `<option value="${v}" ${v === k.typ ? "selected" : ""}>${t}</option>`).join("")}</select></td>
        <td style="white-space:nowrap"><input class="k-od" value="${k.od ?? ""}" style="width:56px" placeholder="od"> – <input class="k-do" value="${k.do ?? ""}" style="width:56px" placeholder="do"></td>
        <td><input class="k-o" value="${esc(k.opis || "")}" style="min-width:240px"></td></tr>`).join("")}</table></div>
      <div class="pasek"><label>Kwota na sfinansowanie (brutto) <input id="oc-budzet" value="${swz.kwota_budzet_brutto || ""}" style="width:140px"></label>
        <button class="maly" data-ik="plus" onclick="zbierzKryt(); OCD.O.swz.kryteria.push({nazwa: '', waga: 0, typ: 'max'}); rysujOcene()">Dodaj kryterium</button>
        <button class="zielony" data-ik="zapisz" onclick="zapiszKryt()">Zapisz kryteria</button>
        <span class="opis" style="margin:0">suma wag: ${kryt.reduce((a, k) => a + (+k.waga || 0), 0)}</span></div>
      <details><summary><b>Wymagane dokumenty (${(swz.wymagane_dokumenty || []).length}) i warunki udziału (${(swz.warunki_udzialu || []).length})</b></summary>${lista(swz.wymagane_dokumenty)}${lista(swz.warunki_udzialu)}</details>` : ""}`,
    kryt.length ? odm(kryt.length, "kryterium", "kryteria", "kryteriów") : "do odczytania")}
  ${krok(3, "Złożone oferty", "k-zolt", `<div class="pasek" style="flex-wrap:wrap"><input id="oc-nazwa" placeholder="Nazwa wykonawcy" style="min-width:240px"><input id="oc-nip" placeholder="NIP" style="width:130px">
      <input id="oc-adres" placeholder="Siedziba (do informacji z otwarcia ofert)" style="min-width:220px">
      <button class="maly" data-ik="plus" onclick="dodajOferteOc()">Dodaj ofertę</button></div>
    ${O.oferty.map(o => `<div class="ds-zam"><div class="pasek"><b>Oferta nr ${esc(o.nr)} – ${esc(o.nazwa)}</b>${o.nip ? `<small class="opis">NIP ${esc(o.nip)}</small>` : ""}
      <span class="opis" style="margin:0">${odm((o.pliki || []).length, "plik", "pliki", "plików")}</span>
      <label class="przycisk maly" data-ik="wgraj">Wgraj pliki oferty (także ZIP)<input type="file" multiple hidden onchange="wgrajOferteOc('${o.id}', this.files)"></label>
      <button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć ofertę?')) zmienOferteOc({usun: '${o.id}'})"></button></div>
      ${(o.pliki || []).length ? `<small class="opis">${o.pliki.map(esc).join(" · ")}</small>` : ""}</div>`).join("") || '<p class="pusto">Brak ofert.</p>'}
    ${O.oferty.length && !swz.prywatny ? `<div class="pasek"><button class="maly" data-ik="dokument" onclick="dokOceny('otwarcie')">Informacja z otwarcia ofert – art. 222 ust. 5 (Word)</button>
      <small class="opis">wykonawcy, siedziby i ceny – ceny uzupełnia badanie ofert (krok 4) albo wpisz je w piśmie</small></div>` : ""}`, odm(O.oferty.length, "oferta", "oferty", "ofert"))}
  ${krok(4, "Badanie ofert – czy są prawidłowe", "k-czer", `<p class="opis">AI sprawdza każdą ofertę z SWZ: kompletność dokumentów, zgodność z SWZ i OPZ, błędy rachunkowe w formularzu cenowym, wadium, termin związania,
      warunki udziału – i wskazuje braki do uzupełnienia (art. 128), kwestie do wyjaśnienia (art. 223) oraz podstawy odrzucenia (art. 226). Dokumenty SWZ są w pamięci podręcznej, więc kolejne oferty są tańsze.</p>
    <div class="pasek"><button class="glowny" data-ik="iskra" onclick="sprawdzOferty()">Sprawdź oferty (AI)</button></div>
    ${O.oferty.filter(o => o.wynik).map(o => { const w = o.wynik; return `<div class="ds-zam"><div class="pasek"><b>Oferta ${esc(o.nr)} – ${esc(o.nazwa)}</b>
        <span class="znacznik ${o.odrzucona ? "z-czerwony" : stanOc(w.status)}">${o.odrzucona ? "odrzucona (decyzja komisji)" : esc(w.status || "")}</span>
        <b>${w.cena_brutto ? zl(+w.cena_brutto) : "–"}</b>${o.razaco_niska ? '<span class="znacznik z-czerwony">rażąco niska cena? (art. 224)</span>' : ""}${o.ponad_budzet ? '<span class="znacznik z-do-analizy">ponad kwotę zamawiającego</span>' : ""}${(o.niezgodna_kryterium || []).length ? '<span class="znacznik z-czerwony">niezgodna z SWZ (art. 226 ust. 1 pkt 5)</span>' : ""}</div>
      ${(o.niezgodna_kryterium || []).map(t => `<p class="czerwone" style="margin:2px 0">${esc(t)}</p>`).join("")}
      ${w.braki?.length ? `<b>Do uzupełnienia:</b>${lista(w.braki)}` : ""}${w.niezgodnosci?.length ? `<b>Niezgodności z SWZ:</b>${lista(w.niezgodnosci)}` : ""}
      ${w.bledy_rachunkowe?.length ? `<b>Błędy rachunkowe:</b>${lista(w.bledy_rachunkowe)}` : ""}${w.do_wyjasnienia?.length ? `<b>Do wyjaśnienia:</b>${lista(w.do_wyjasnienia)}` : ""}
      ${w.podstawa_odrzucenia ? `<p class="czerwone"><b>Podstawa odrzucenia:</b> ${esc(w.podstawa_odrzucenia)}</p>` : ""}${w.uwagi ? `<p class="opis">${esc(w.uwagi)}</p>` : ""}
      ${ocWerHtml(o)}
      <div class="pasek"><button class="maly" data-ik="dokument" onclick="dokOceny('wezwanie', '${o.id}')">Wezwanie do wykonawcy (Word)</button>
        <button class="maly" onclick="${o.odrzucona ? `zmienOferteOc({id: '${o.id}', odrzucona: false})` : `ocOdrzucPanel('${o.id}')`}">${o.odrzucona ? "Przywróć ofertę" : "Odrzuć ofertę"}</button>
        ${!o.odrzucona && (w.status !== "prawidłowa" || o.razaco_niska) ? `<button class="maly zielony" onclick="zmienOferteOc({id: '${o.id}', wynik: {status: 'prawidłowa', wyjasnione: true}})">Wyjaśnione / uzupełnione – oferta prawidłowa</button>` : ""}
        <button class="maly" onclick="sprawdzOferty(['${o.id}'])">Sprawdź ponownie</button></div>
      <div id="oc-odrz-${o.id}" class="ramka-uwaga" style="display:none;margin-top:6px"><b>Odrzucenie oferty – podstawa prawna i uzasadnienie faktyczne</b> <small class="opis">(trafią do informacji o wyborze${swz.prywatny ? "" : " – art. 253 ust. 1 pkt 2 Pzp"})</small>
        ${swz.prywatny ? "" : `<label style="display:block;margin-top:4px">Podstawa prawna – art. 226 ust. 1 Pzp<select class="oc-odrz-pkt" style="width:100%"><option value="">– wybierz punkt –</option>${Object.entries(OCD.projekt.punkty_226 || {}).map(([k, t]) => `<option value="${k}">pkt ${k} – ${esc(t)}</option>`).join("")}</select></label>`}
        <label style="display:block;margin-top:4px">Uzasadnienie faktyczne (wymagane)<textarea class="oc-odrz-txt" rows="3" style="width:100%" placeholder="np. oferta nie zawiera kosztorysu ofertowego wymaganego w rozdz. … SWZ">${esc(w.podstawa_odrzucenia || "")}</textarea></label>
        <div class="pasek"><button class="maly niebezp" onclick="ocOdrzuc('${o.id}')">Odrzuć ofertę</button><button class="maly" onclick="ocOdrzucPanel('${o.id}')">Anuluj</button></div></div></div>`; }).join("")}`,
    O.oferty.filter(o => o.wynik).length + "/" + O.oferty.length + " zbadanych")}
  ${krok(5, "Ranking i wybór najkorzystniejszej oferty", "k-fiol", (P.czesci || []).length ? ocCzesciHtml(O, P) : ranking.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Miejsce</th><th>Wykonawca</th><th>Cena brutto</th>${kryt.map(k => `<th>${esc(k.nazwa)} (${k.waga})</th>`).join("")}<th>Razem pkt</th></tr>
      ${ranking.map(o => `<tr class="${o.id === P.najkorzystniejsza && !P.warunkowo ? "wybrany" : ""}"><td><b>${o.miejsce}</b>${o.id === P.najkorzystniejsza ? (P.warunkowo ? (o.id !== P.pierwsza_w_rankingu ? ' <small class="znacznik">bez zastrzeżeń</small>' : "") : " 🏆") : ""}${o.wynik?.status !== "prawidłowa" || o.razaco_niska || (o.niezgodna_kryterium || []).length ? ' <small class="znacznik z-do-analizy">warunkowo</small>' : ""}</td><td>${esc(o.nazwa)}</td>
        <td class="liczba">${o.wynik?.cena_brutto ? zl(+o.wynik.cena_brutto) : "–"}</td>${kryt.map(k => `<td class="liczba">${pkt(o.punkty_szczegoly?.[k.nazwa])}</td>`).join("")}<td class="liczba"><b>${pkt(o.punkty)}</b></td></tr>`).join("")}</table></div>
    ${P.warunkowo && !(P.remis_248 || []).length ? `<div class="ramka-uwaga">${P.pierwsza_w_rankingu !== P.najkorzystniejsza
        ? `Najwięcej punktów ma oferta <b>${esc((O.oferty.find(o => o.id === P.pierwsza_w_rankingu) || {}).nazwa || "")}</b>, ale wymaga wyjaśnień, uzupełnień albo wyjaśnienia ceny. Wybór jest wstrzymany: przyjmij wyjaśnienia (przycisk „Wyjaśnione / uzupełnione – oferta prawidłowa” w kroku 4) albo odrzuć tę ofertę. Oferta oznaczona „bez zastrzeżeń” zostanie wybrana tylko wtedy, gdy oferta z 1. miejsca zostanie odrzucona.`
        : "Najwyżej oceniona oferta ma nierozstrzygnięte kwestie (braki, wyjaśnienia albo rażąco niską cenę) – wybór jest wstrzymany do czasu ich rozstrzygnięcia."}</div>` : ""}
    ${(P.ostrzezenia || []).map(t => `<div class="ramka-uwaga" style="margin:6px 0">⚠ ${esc(t)}</div>`).join("")}${P.art248 ? `<p class="opis">${esc(P.art248)}</p>` : ""}
    ${(() => { const n = O.oferty.find(o => o.id === P.najkorzystniejsza); return n && n.ponad_budzet && !swz.prywatny ? `<div class="ramka-uwaga">Cena najkorzystniejszej oferty (${zl(+n.wynik.cena_brutto)}) przewyższa kwotę na sfinansowanie (${zl(P.budzet)}). Zamawiający zwiększa kwotę do ceny oferty albo unieważnia postępowanie (art. 255 pkt 3 Pzp) – informacja o wyborze po decyzji.
      <div class="pasek"><button class="maly" onclick="if (confirm('Zapisać decyzję o zwiększeniu kwoty na sfinansowanie do ceny najkorzystniejszej oferty?')) ocZwiekszKwote()">Zwiększam kwotę do ceny oferty</button></div></div>` : ""; })()}
    ${swz.zwiekszona_kwota && swz.zwiekszona_kwota.do ? `<p class="opis">Kwota na sfinansowanie zwiększona z ${zl(+swz.zwiekszona_kwota.z || 0)} do ${zl(+swz.zwiekszona_kwota.do)} (${esc(swz.zwiekszona_kwota.data || "")}).</p>` : ""}
    <p class="opis">Średnia cena ofert nieodrzuconych: ${P.srednia_cen ? zl(P.srednia_cen) : "–"}${P.budzet ? " · kwota zamawiającego: " + zl(P.budzet) : ""}. Oferty „do odrzucenia” i odrzucone przez komisję nie są punktowane.</p>
    <div class="pasek"><button class="zielony" data-ik="dokument" onclick="dokOceny('protokol')">Protokół z badania i oceny ofert (Word)</button>
      <button data-ik="dokument" onclick="dokOceny('informacja')"${P.warunkowo || (P.czesci || []).some(c => c.warunkowo) ? ' disabled title="Informacja o wyborze – dostępna po rozstrzygnięciu oferty najwyżej ocenionej (wyjaśnienia albo odrzucenie)"' : ""}>Informacja o wyborze najkorzystniejszej oferty (Word)</button>
      ${swz.prywatny ? "" : `<button data-ik="dokument" onclick="dokOceny('srodki')" title="Art. 126 ust. 1 (od progów UE, co najmniej 10 dni) / art. 274 ust. 1 Pzp (co najmniej 5 dni)">Wezwanie do podmiotowych środków dowodowych – oferta najwyżej oceniona (Word)</button>`}</div>` : '<p class="pusto">Ranking pojawi się po zbadaniu ofert.</p>',
    P.warunkowo || (P.czesci || []).some(c => c.warunkowo) ? "wybór wstrzymany" : P.najkorzystniejsza ? "wybrana: " + esc((O.oferty.find(o => o.id === P.najkorzystniejsza) || {}).nazwa || "") : "")}
  ${sekcjaRynkowosci(O)}${OCD.projekt.strona === "prawnik" ? sekcjaPrawnikaOferty(OCD.projekt) : ""}`;
  if (OCD.projekt.strona === "prawnik") el.insertAdjacentHTML("afterbegin", kartaPrawnikaOferty(OCD.projekt));
  wstawIkony(el);
}
async function wgrajSwz(pliki) {
  const fd = new FormData(); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/pliki`, {method: "POST", body: fd}))) { komunikat("Wgrano dokumenty."); otworzOcene(OC_ID); }
}
async function swzOceny() { sledz(await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/swz`, {json: {}})), () => otworzOcene(OC_ID)); }
function zbierzKryt() {
  document.querySelectorAll("#oc-kryt tr[data-i]").forEach(tr => { const k = OCD.O.swz.kryteria[+tr.dataset.i];
    Object.assign(k, {nazwa: tr.querySelector(".k-n").value, waga: parseFloat(tr.querySelector(".k-w").value.replace(",", ".")) || 0, typ: tr.querySelector(".k-t").value, opis: tr.querySelector(".k-o").value,
      od: tr.querySelector(".k-od").value.replace(",", ".").trim(), do: tr.querySelector(".k-do").value.replace(",", ".").trim()}); });
}
async function ocZwiekszKwote() { if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/kryteria`, {json: {zwieksz_kwote: true}}))) { komunikat("Zapisano decyzję o zwiększeniu kwoty."); otworzOcene(OC_ID); } }
async function zapiszKryt() {
  zbierzKryt();
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/kryteria`, {json: {kryteria: OCD.O.swz.kryteria, kwota_budzet_brutto: $("#oc-budzet").value}}))) { komunikat("Zapisano – ranking przeliczony."); otworzOcene(OC_ID); }
}
function ocOdrzucPanel(id) { const e = $("#oc-odrz-" + id); if (e) e.style.display = e.style.display === "none" ? "" : "none"; }
async function ocOdrzuc(id) {  // art. 253 ust. 1 pkt 2 – odrzucenie z podstawą prawną (art. 226 ust. 1) i uzasadnieniem faktycznym
  const e = $("#oc-odrz-" + id), pkt = (e.querySelector(".oc-odrz-pkt") || {}).value || "", txt = e.querySelector(".oc-odrz-txt").value.trim();
  if (!OCD.O.swz?.prywatny && !pkt && !/art\.\s*\d+/.test(txt)) return komunikat("Wybierz podstawę prawną – punkt art. 226 ust. 1 Pzp.", true);
  if (txt.length < 5) return komunikat("Wpisz uzasadnienie faktyczne odrzucenia oferty.", true);
  zmienOferteOc({id, odrzucona: true, wynik: {punkt_226: pkt, podstawa_odrzucenia: txt}});
}
async function zmienOferteOc(d) { if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/oferta`, {json: d}))) otworzOcene(OC_ID); }
async function dodajOferteOc() {
  const nazwa = $("#oc-nazwa").value.trim(); if (!nazwa) return komunikat("Podaj nazwę wykonawcy.", true);
  await zmienOferteOc({nazwa, nip: $("#oc-nip").value, adres: ($("#oc-adres") || {}).value || ""});
}
async function wgrajOferteOc(id, pliki) {
  const fd = new FormData(); fd.append("id", id); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/plik`, {method: "POST", body: fd}))) { komunikat("Wgrano pliki oferty."); otworzOcene(OC_ID); }
}
async function sprawdzOferty(ids) { sledz(await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/sprawdz`, {json: {ids}})), () => otworzOcene(OC_ID)); }
async function dokOceny(rodzaj, id) { const w = await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/dokument`, {json: {rodzaj, id}})); if (w) location.href = w.url; }

// ---------- realizacja umów dostawcy / usługodawcy
let DS_ID = null, DSD = null;
async function ladujDostawy() {
  const l = await bezpiecznie(() => api("/api/dostawy/realizacja")); if (!l) return;
  $("#lista-dostaw").innerHTML = l.map(p => `<li class="${p.id === DS_ID ? "akt" : ""}" onclick="otworzDostawy('${p.id}')">${esc(p.nazwa)}
    <small>${p.rodzaj === "uslugi" ? "usługi" : "dostawy"} · ${p.status === "zakonczony" ? "zakończona · " : ""}umowa ${zl(p.wartosc || 0)} · ${p.proc || 0}%${p.przeterminowane ? ` · <span style="color:#ffb4b4">zaległe ${zl(p.przeterminowane)}</span>` : ""}</small></li>`).join("")
    || '<li class="pusto">Brak umów w realizacji. W ofercie wygranego przetargu kliknij „Przetarg wygrany – do realizacji”.</li>';
  if (DS_ID && l.some(p => p.id === DS_ID)) otworzDostawy(DS_ID); else if (l.length) otworzDostawy(l[0].id);
}
async function otworzDostawy(id) {
  DS_ID = id;
  document.querySelectorAll("#lista-dostaw li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  DSD = await bezpiecznie(() => api(`/api/projekty/${id}/dostawy`)); if (DSD) rysujDostawy();
}
async function zapiszDostawy(czesci, przelicz) {
  const w = await bezpiecznie(() => api(`/api/projekty/${DS_ID}/dostawy`, {json: {...czesci, przelicz_okresy: !!przelicz}})); if (!w) return;
  DSD.R = w.R; DSD.S = w.S; rysujDostawy(); komunikat("Zapisano.");
}
async function dokumentDostawy(rodzaj, id) {
  const w = await bezpiecznie(() => api(`/api/projekty/${DS_ID}/dostawy/dokument`, {json: {rodzaj, id}})); if (w) { location.href = w.url; setTimeout(() => otworzDostawy(DS_ID), 800); }
}
// zapis częściowy po id: usunięcie wysyłane wprost (serwer nie usuwa elementów, których nie przysłano – H1-05)
function usunZDostaw(lista, i) {
  const x = DSD.R[lista][i]; DSD.R[lista].splice(i, 1);
  if (x && x.id) zapiszDostawy({usun: {[lista]: [x.id]}}); else rysujDostawy();
}
function zbierzUmowe() { const u = {...DSD.R.umowa}; document.querySelectorAll("#ds-umowa [data-k]").forEach(e => { u[e.dataset.k] = e.value; }); return u; }
function rysujDostawy() {
  const R = DSD.R, S = DSD.S, u = R.umowa || {}, usl = R.rodzaj === "uslugi", el = $("#dos-real"), dzis = new Date().toISOString().slice(0, 10);
  const pole = (k, et, typ = "text", szer = "") => `<label>${et}<input data-k="${k}" type="${typ}" value="${esc(String(u[k] ?? ""))}" ${szer}></label>`;
  const kafel = (t, v, op, kl = "") => `<div class="${kl}"><span>${t}</span><b>${v}</b>${op ? `<small>${op}</small>` : ""}</div>`;
  const wz = z => zl(z.wartosc || 0);
  el.innerHTML = `<div class="pulpit-glowka"><h2>${esc(DSD.projekt.nazwa)}</h2>
      <span class="znacznik ${DSD.projekt.status === "zakonczony" ? "z-odpuszczamy" : "z-startujemy"}">${DSD.projekt.status === "zakonczony" ? "umowa zakończona" : usl ? "usługi w realizacji" : "dostawy w realizacji"}</span></div>
    <div class="kwoty kafle-przetargu">
      ${kafel("Wartość umowy", zl(S.wartosc_netto), "netto · brutto " + zl(S.wartosc_brutto))}
      ${kafel("Zrealizowano", S.proc_realizacji + "%", zl(S.zrealizowano_netto) + " netto")}
      ${kafel("Zafakturowano", zl(S.zafakturowano_brutto), "zapłacono " + zl(S.zaplacono_brutto))}
      ${kafel("Należności", zl(S.naleznosci_brutto), S.przeterminowane_brutto ? `<span class="czerwone">po terminie ${zl(S.przeterminowane_brutto)}</span>` : "bez zaległości")}
      ${kafel("Do zafakturowania", zl(S.do_zafakturowania_brutto), "odebrane, bez faktury")}
      ${kafel("Ryzyko kar", zl(S.ryzyko_kar), S.opoznione.length ? `<span class="czerwone">${odm(S.opoznione.length, "dostawa", "dostawy", "dostaw")} po terminie</span>` : "brak opóźnień")}
    </div>
    ${[S.dni_do_konca != null && S.dni_do_konca <= 30 && S.dni_do_konca >= 0 ? `Umowa kończy się za ${S.dni_do_konca} dni (${esc(S.koniec_umowy)}).` : "",
       S.faktury_po_terminie ? `${odm(S.faktury_po_terminie, "faktura", "faktury", "faktur")} po terminie płatności – możesz wysłać wezwanie do zapłaty.` : "",
       S.reklamacje_po_terminie ? `${odm(S.reklamacje_po_terminie, "reklamacja", "reklamacje", "reklamacji")} po terminie rozpatrzenia.` : "",
       S.zabezpieczenie_zwrot && S.zabezpieczenie_zwrot <= dzis ? "Minął termin zwrotu zabezpieczenia należytego wykonania – upomnij się o zwrot." : "",
       ...S.opoznione.map(o => `Dostawa ${esc(o.nr || "")} opóźniona o ${o.dni} dni – możliwa kara ok. ${zl(o.kara)}.`)].filter(Boolean).map(t => `<div class="ramka-uwaga">${t}</div>`).join("")}

    <div class="krok k-nieb"><div class="tytul"><span class="nr">1</span><h3>Umowa</h3></div><div class="tresc" id="ds-umowa">
      <div class="siatka">${pole("numer", "Numer umowy")}${pole("data", "Data zawarcia", "date")}${pole("zamawiajacy", "Zamawiający")}
        ${pole("od", "Obowiązuje od", "date")}${pole("do", "do", "date")}${pole("wartosc_netto", "Wartość netto [zł]")}${pole("vat", "VAT (np. 0,23)")}
        ${pole("termin_platnosci", "Termin płatności [dni]")}${pole("kara_proc", "Kara za zwłokę [% dziennie]")}${pole("gwarancja_mies", "Gwarancja [mies.]")}
        ${pole("zabezpieczenie", "Zabezpieczenie [zł]")}${pole("zabezpieczenie_zwrot", "Zwrot zabezpieczenia", "date")}${pole("osoba", "Osoba po stronie zamawiającego")}${pole("kontakt", "Telefon / e-mail")}
        <label>Tryb<select data-k="tryb">${(usl ? ["okresowa", "jednorazowa"] : ["sukcesywna", "jednorazowa"]).map(t => `<option ${t === u.tryb ? "selected" : ""}>${t}</option>`).join("")}</select></label>
        ${pole("uwagi", "Uwagi (np. termin dostawy od zamówienia)")}</div>
      <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszDostawy({umowa: zbierzUmowe()}, ${usl})">Zapisz umowę</button>
        ${usl ? '<span class="opis" style="margin:0">okresy rozliczeniowe przeliczą się z dat obowiązywania</span>' : ""}</div></div></div>

    ${usl ? `<div class="krok k-ziel"><div class="tytul"><span class="nr">2</span><h3>Okresy usług – wykonanie i odbiory</h3><span class="stan">${R.okresy.filter(o => o.status === "odebrane").length}/${R.okresy.length} odebranych</span></div><div class="tresc">
      <div class="tabela-okno"><table class="tabela" id="ds-okresy"><tr><th>Okres</th><th>Wartość netto</th><th>Status</th><th>Data odbioru</th><th>Faktura</th><th></th></tr>
        ${R.okresy.map((o, i) => `<tr data-i="${i}"><td><b>${esc(o.okres)}</b></td><td><input class="ok-w" value="${String(o.wartosc).replace(".", ",")}" style="width:110px"></td>
          <td><select class="ok-s">${DSD.statusy_okr.map(s => `<option ${s === o.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
          <td><input type="date" class="ok-d" value="${esc(o.data_odbioru || "")}"></td><td>${esc(o.faktura || "–")}</td>
          <td style="white-space:nowrap"><button class="maly" data-ik="dokument" onclick="dokumentDostawy('protokol', '${o.id}')">Protokół</button>
            ${!o.faktura ? `<button class="maly" onclick="fakturaZ('okres', ${i})">+ Faktura</button>` : ""}</td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszOkresy()">Zapisz okresy</button></div></div></div>`
    : `<div class="krok k-ziel"><div class="tytul"><span class="nr">2</span><h3>Zamówienia i dostawy</h3><span class="stan">${R.zamowienia.length} zamówień · ${zl(S.zamowiono_netto)}</span></div><div class="tresc">
      <p class="opis">Każde zamówienie (przy dostawie jednorazowej – jedno) z ilościami z formularza cenowego; wartość liczy się z Twoich cen. Status: przyjęte → w realizacji → dostarczone → odebrane.</p>
      ${R.zamowienia.map((z, i) => `<div class="ds-zam" data-i="${i}"><div class="pasek"><b>Zamówienie</b>
          <input class="z-nr" value="${esc(z.nr || "")}" placeholder="nr" style="width:110px"><label>z dnia<input type="date" class="z-data" value="${esc(z.data || "")}"></label>
          <label>termin<input type="date" class="z-termin" value="${esc(z.termin || "")}"></label>
          <select class="z-st">${DSD.statusy_zam.map(s => `<option ${s === z.status ? "selected" : ""}>${s}</option>`).join("")}</select>
          <label>dostarczono<input type="date" class="z-dd" value="${esc(z.data_dostawy || "")}"></label><label>odebrano<input type="date" class="z-do" value="${esc(z.data_odbioru || "")}"></label>
          <b class="${z.termin && z.termin < dzis && ["przyjęte", "w realizacji"].includes(z.status) ? "czerwone" : ""}">${wz(z)}</b></div>
        <div class="tabela-okno"><table class="tabela"><tr><th>Lp.</th><th>Pozycja</th><th>j.m.</th><th>Cena</th><th>Ilość w zamówieniu</th></tr>
          ${R.pozycje.map(p => { const x = (z.pozycje || []).find(q => +q.lp === p.lp); return `<tr><td>${p.lp}</td><td>${esc(p.opis.slice(0, 90))}</td><td>${esc(p.jm)}</td><td class="liczba">${zl(p.cena)}</td>
            <td><input class="z-il" data-lp="${p.lp}" value="${x ? String(x.ilosc).replace(".", ",") : ""}" style="width:90px"></td></tr>`; }).join("")}</table></div>
        <div class="pasek"><button class="maly" data-ik="dokument" onclick="dokumentDostawy('protokol', '${z.id}')">Protokół odbioru (Word)</button>
          ${!z.faktura ? `<button class="maly" onclick="fakturaZ('zam', ${i})">+ Faktura za tę dostawę</button>` : `<small class="opis">faktura ${esc(z.faktura)}</small>`}
          <button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć zamówienie?')) { zbierzZam(); usunZDostaw('zamowienia', ${i}); }"></button></div></div>`).join("") || '<p class="pusto">Brak zamówień.</p>'}
      <div class="pasek"><button class="maly" data-ik="plus" onclick="nowaDostawa()">Nowe zamówienie / dostawa</button><button class="zielony" data-ik="zapisz" onclick="zbierzZam(); zapiszDostawy({zamowienia: DSD.R.zamowienia})">Zapisz zamówienia</button></div>
      <details style="margin-top:8px"><summary><b>Wykorzystanie pozycji umowy</b></summary><div class="tabela-okno"><table class="tabela"><tr><th>Lp.</th><th>Pozycja</th><th>W umowie</th><th>Zamówiono</th><th>Pozostało</th><th>%</th></tr>
        ${S.wykorzystanie.map(w => `<tr><td>${w.lp}</td><td>${esc(w.opis.slice(0, 80))}</td><td class="liczba">${w.umowa} ${esc(w.jm)}</td><td class="liczba">${w.zamowiono}</td>
          <td class="liczba ${w.pozostalo < 0 ? "czerwone" : ""}">${w.pozostalo}</td><td class="liczba">${w.proc ?? "–"}%</td></tr>`).join("")}</table></div></details></div></div>`}

    <div class="krok k-zolt"><div class="tytul"><span class="nr">3</span><h3>Faktury i płatności</h3><span class="stan">${R.faktury.length} faktur</span></div><div class="tresc">
      <div class="tabela-okno"><table class="tabela" id="ds-fv"><tr><th>Nr faktury</th><th>Data</th><th>Netto</th><th>Brutto</th><th>Termin płatności</th><th>Zapłacono</th><th>Data zapłaty</th><th>Dotyczy</th><th></th></tr>
        ${R.faktury.map((f, i) => `<tr data-i="${i}" class="${!f.zaplacono && f.termin && f.termin < dzis ? "czerwone" : ""}"><td><input class="f-nr" value="${esc(f.nr || "")}" style="width:110px"></td>
          <td><input type="date" class="f-data" value="${esc(f.data || "")}"></td><td><input class="f-netto" value="${String(f.netto ?? "").replace(".", ",")}" style="width:100px"></td>
          <td><input class="f-brutto" value="${String(f.brutto ?? "").replace(".", ",")}" style="width:100px"></td><td><input type="date" class="f-termin" value="${esc(f.termin || "")}"></td>
          <td><input type="checkbox" class="f-zap" ${f.zaplacono ? "checked" : ""}></td><td><input type="date" class="f-dz" value="${esc(f.data_zaplaty || "")}"></td><td><small>${esc(f.dotyczy || "")}</small></td>
          <td style="white-space:nowrap">${!f.zaplacono && f.termin && f.termin < dzis ? `<button class="maly" data-ik="mail" onclick="dokumentDostawy('wezwanie', '${f.id}')">Wezwanie do zapłaty</button>` : ""}
            <button class="maly niebezp" data-ik="kosz" onclick="zbierzFv(); usunZDostaw('faktury', ${i})"></button></td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="maly" data-ik="plus" onclick="zbierzFv(); DSD.R.faktury.push({data: new Date().toISOString().slice(0,10)}); rysujDostawy()">Dodaj fakturę</button>
        <button class="zielony" data-ik="zapisz" onclick="zbierzFv(); zapiszDostawy({faktury: DSD.R.faktury})">Zapisz faktury</button>
        <span class="opis" style="margin:0">brutto i termin płatności uzupełniają się same z umowy</span></div></div></div>

    <div class="krok k-czer"><div class="tytul"><span class="nr">4</span><h3>Reklamacje i gwarancja</h3><span class="stan">${S.gwarancja_do ? "gwarancja do " + esc(S.gwarancja_do) : "gwarancja – po odbiorze"}</span></div><div class="tresc">
      <div class="tabela-okno"><table class="tabela" id="ds-rek"><tr><th>Data zgłoszenia</th><th>Opis</th><th>Termin rozpatrzenia</th><th>Status</th><th>Rozwiązanie</th><th></th></tr>
        ${R.reklamacje.map((r, i) => `<tr data-i="${i}" class="${r.status !== "zamknięta" && r.termin && r.termin < dzis ? "czerwone" : ""}"><td><input type="date" class="r-data" value="${esc(r.data || "")}"></td>
          <td><input class="r-opis" value="${esc(r.opis || "")}" style="min-width:220px"></td><td><input type="date" class="r-termin" value="${esc(r.termin || "")}"></td>
          <td><select class="r-st">${["zgłoszona", "w trakcie", "zamknięta"].map(s => `<option ${s === r.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
          <td><input class="r-roz" value="${esc(r.rozwiazanie || "")}"></td><td><button class="maly niebezp" data-ik="kosz" onclick="zbierzRek(); usunZDostaw('reklamacje', ${i})"></button></td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="maly" data-ik="plus" onclick="zbierzRek(); const d = new Date(); DSD.R.reklamacje.push({data: d.toISOString().slice(0,10), termin: new Date(d.getTime() + 14 * 864e5).toISOString().slice(0,10), status: 'zgłoszona'}); rysujDostawy()">Zgłoszenie reklamacji</button>
        <button class="zielony" data-ik="zapisz" onclick="zbierzRek(); zapiszDostawy({reklamacje: DSD.R.reklamacje})">Zapisz reklamacje</button></div></div></div>

    <div class="krok k-fiol"><div class="tytul"><span class="nr">5</span><h3>Dokumenty i rozliczenie końcowe</h3></div><div class="tresc">
      <div class="pliki-ik">${DSD.pliki.map(f => plikIk(DS_ID, "realizacja/dostawy/" + f, f.length > 24 ? f.slice(0, 22) + "…" : f, 1)).join("") || '<span class="opis">Brak dokumentów.</span>'}</div>
      <div class="pasek"><label class="przycisk maly" data-ik="wgraj">Wgraj (podpisane protokoły, WZ, korespondencja)<input type="file" multiple hidden onchange="wgrajDostawy(this.files)"></label>
        <button data-ik="tabela" onclick="dokumentDostawy('rozliczenie')">Rozliczenie umowy (Excel)</button>
        ${DSD.projekt.status !== "zakonczony" ? `<button class="maly" onclick="if (confirm('Oznaczyć umowę jako zakończoną?')) api('/api/projekty/${DS_ID}/status', {json: {status: 'zakonczony'}}).then(() => ladujDostawy())">Zakończ umowę</button>` : ""}</div></div></div>`;
  wstawIkony(el);
}
function zbierzZam() {
  document.querySelectorAll(".ds-zam").forEach(b => { const z = DSD.R.zamowienia[+b.dataset.i]; const g = c => b.querySelector(c).value;
    Object.assign(z, {nr: g(".z-nr"), data: g(".z-data"), termin: g(".z-termin"), status: g(".z-st"), data_dostawy: g(".z-dd"), data_odbioru: g(".z-do")});
    z.pozycje = [...b.querySelectorAll(".z-il")].filter(e => e.value.trim()).map(e => ({lp: +e.dataset.lp, ilosc: parseFloat(e.value.replace(",", ".")) || 0})); });
}
function nowaDostawa() {
  zbierzZam(); const d = new Date().toISOString().slice(0, 10), jedn = DSD.R.umowa.tryb === "jednorazowa";
  DSD.R.zamowienia.push({nr: String(DSD.R.zamowienia.length + 1), data: d, termin: DSD.R.umowa.do || d, status: "przyjęte",
    pozycje: jedn ? DSD.R.pozycje.map(p => ({lp: p.lp, ilosc: p.ilosc})) : []});
  rysujDostawy();
}
function zapiszOkresy() {
  document.querySelectorAll("#ds-okresy tr[data-i]").forEach(tr => { const o = DSD.R.okresy[+tr.dataset.i];
    Object.assign(o, {wartosc: parseFloat(tr.querySelector(".ok-w").value.replace(/\s/g, "").replace(",", ".")) || 0, status: tr.querySelector(".ok-s").value, data_odbioru: tr.querySelector(".ok-d").value}); });
  zapiszDostawy({okresy: DSD.R.okresy});
}
function zbierzFv() {
  document.querySelectorAll("#ds-fv tr[data-i]").forEach(tr => { const f = DSD.R.faktury[+tr.dataset.i]; const g = c => tr.querySelector(c);
    Object.assign(f, {nr: g(".f-nr").value, data: g(".f-data").value, netto: parseFloat(g(".f-netto").value.replace(/\s/g, "").replace(",", ".")) || 0,
      brutto: parseFloat(g(".f-brutto").value.replace(/\s/g, "").replace(",", ".")) || 0, termin: g(".f-termin").value, zaplacono: g(".f-zap").checked, data_zaplaty: g(".f-dz").value}); });
}
function zbierzRek() {
  document.querySelectorAll("#ds-rek tr[data-i]").forEach(tr => { const r = DSD.R.reklamacje[+tr.dataset.i]; const g = c => tr.querySelector(c).value;
    Object.assign(r, {data: g(".r-data"), opis: g(".r-opis"), termin: g(".r-termin"), status: g(".r-st"), rozwiazanie: g(".r-roz")}); });
}
function fakturaZ(rodz, i) {  // faktura za odebraną dostawę albo okres – kwota z wartości, numer do uzupełnienia
  zbierzFv(); const nr = prompt("Numer faktury:"); if (!nr) return;
  const el = rodz === "zam" ? (zbierzZam(), DSD.R.zamowienia[i]) : DSD.R.okresy[i];
  el.faktura = nr;
  DSD.R.faktury.push({nr, data: new Date().toISOString().slice(0, 10), netto: el.wartosc || 0, dotyczy: rodz === "zam" ? "zamówienie " + (el.nr || "") : "okres " + el.okres});
  zapiszDostawy(rodz === "zam" ? {zamowienia: DSD.R.zamowienia, faktury: DSD.R.faktury} : {okresy: DSD.R.okresy, faktury: DSD.R.faktury});
}
async function wgrajDostawy(pliki) {
  const fd = new FormData(); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${DS_ID}/dostawy/plik`, {method: "POST", body: fd}))) { komunikat("Wgrano."); otworzDostawy(DS_ID); }
}

// ---------- konkurencja u zamawiającego (BZP – ogłoszenia o wyniku)
async function historiaPrzetargu(nr, wymus) {
  sledz(await bezpiecznie(() => api("/api/przetargi/historia", {json: {numer: nr, wymus: !!wymus}})), async () => {
    const h = await api("/api/przetargi/historia/" + encodeURIComponent(nr)).catch(() => null); if (h && h.data && $("#p-historia")) rysujHistorie($("#p-historia"), h, () => historiaPrzetargu(nr, true)); });
}
async function historiaProjektu(wymus) { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/historia-zamawiajacego`, {json: {wymus: !!wymus}})), odswiezProjekt); }
function rysujHistorie(el, h, odswiez) {
  if (!el) return; el._odswiez = odswiez;
  const W = h.wszystkie || {}, P = h.podobne || {}, Z = h.najczesciej_wygrywaja || [], O = h.ostatnio_wygrali || [];
  const kz = v => v ? zl(v) : "–";
  el.innerHTML = `<div class="karta hz"><div class="polecane-gora"><b>${ik("trofeum")} Konkurencja u zamawiającego</b>
      <button class="maly" data-ik="odswiez" onclick="this.closest('.historia-zam')._odswiez()">Odśwież</button></div>
    <p class="opis" style="margin:0 0 8px">${esc(h.zamawiajacy || "")} · rozstrzygnięcia z BZP${h.z_bk ? ` i Bazy Konkurencyjności (${h.z_bk})` : " i Bazy Konkurencyjności"}, ostatnie 24 miesiące · ${esc(h.data || "")}</p>
    ${!W.liczba ? '<p class="pusto">Nie znaleziono rozstrzygniętych postępowań tego zamawiającego w BZP ani w Bazie Konkurencyjności (albo zamawiający publikuje wyniki gdzie indziej).</p>' : `
    <div class="kwoty kafle-przetargu">
      <div><span>Podobne przetargi</span><b>${P.liczba || 0}</b><small>na ${W.liczba} rozstrzygnięć</small></div>
      <div><span>Cena w podobnych (mediana)</span><b>${kz(P.mediana_ceny)}</b><small>${P.min_ceny ? kz(P.min_ceny) + " – " + kz(P.max_ceny) : ""}</small></div>
      <div><span>Średnio ofert – podobne</span><b>${P.srednia_ofert ?? "–"}</b><small>wszystkie: ${W.srednia_ofert ?? "–"}</small></div>
      <div><span>Unieważnione</span><b>${W.uniewaznione || 0}</b><small>z ${W.liczba}</small></div></div>
    ${Z.length ? `<h4 class="grupa-analizy">Najczęściej wygrywają u tego zamawiającego</h4><div class="tabela-okno"><table class="tabela"><tr><th>Wykonawca</th><th>Wygrane</th><th>Łączna wartość</th><th>Ostatnio</th></tr>
      ${Z.map(z => `<tr><td><b>${esc(z.wykonawca)}</b>${z.nip ? `<br><small class="opis">NIP ${esc(z.nip)}</small>` : ""}</td><td class="liczba">${z.wygrane}</td><td class="liczba">${kz(z.wartosc)}</td><td>${esc(dataPl(z.ostatnio))}</td></tr>`).join("")}</table></div>` : ""}
    ${O.length ? `<h4 class="grupa-analizy">Ostatnio wygrali</h4><ul class="lista">${O.map(o => `<li><b>${esc(o.wykonawca)}</b>${o.zrodlo && o.zrodlo !== "BZP" ? ' <small class="znacznik z-odpuszczamy">BK</small>' : ""} – ${esc(dataPl(o.data))}: ${esc((o.przedmiot || "").slice(0, 90))}${o.cena ? " · " + kz(o.cena) : ""}${o.ofert ? " · ofert: " + o.ofert : ""}</li>`).join("")}</ul>` : ""}
    ${(h.lista_podobnych || []).length ? `<details><summary><b>Podobne przetargi (${h.lista_podobnych.length})</b></summary><div class="tabela-okno"><table class="tabela"><tr><th>Data</th><th>Przedmiot</th><th>Ofert</th><th>Cena wybrana</th><th>Najniższa – najwyższa</th><th>Zwycięzca</th></tr>
      ${h.lista_podobnych.map(w => `<tr><td>${esc(dataPl(w.data))}</td><td>${esc((w.przedmiot || "").slice(0, 110))}${w.zrodlo && w.zrodlo !== "BZP" ? ' <small class="znacznik z-odpuszczamy">BK</small>' : ""}</td><td class="liczba">${w.ofert ?? "–"}</td><td class="liczba">${kz(w.cena)}</td>
        <td class="liczba">${w.najnizsza ? kz(w.najnizsza) + " – " + kz(w.najwyzsza) : "–"}</td><td>${w.uniewaznione ? '<span class="czerwone">unieważnione</span>' : esc(w.wykonawca || "–")}</td></tr>`).join("")}</table></div></details>` : ""}`}
  </div>`;
  wstawIkony(el);
}
async function pobierzDokNaboru() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wniosek-dot/pobierz`, {json: {}})), odswiezProjekt); }
async function analizaDotacji() { if (!(await zapiszDaneDotacji())) return; sledz(await bezpiecznie(() => api(`${DOT_URL()}/analiza`, {json: {}})), ladujDotacje); }
async function zakresDotacji(z) { if (await bezpiecznie(() => api(`${DOT_URL()}/dane`, {json: {...(DOT.dane || {}), zakres: z}}))) ladujDotacje(); }
async function wgrajDotacja(dok, pliki) {
  if (!pliki.length) return; const fd = new FormData(); fd.append("dok", dok); [...pliki].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`${DOT_URL()}/plik`, {method: "POST", body: fd}))) { komunikat("Wgrano."); ladujDotacje(); }
}
async function usunPlikDotacji(dok, plik) { if (confirm(`Usunąć plik ${plik}?`) && await bezpiecznie(() => api(`${DOT_URL()}/plik/usun`, {json: {dok, plik}}))) ladujDotacje(); }
async function przygotujDotacja(dok) { sledz(await bezpiecznie(() => api(`${DOT_URL()}/przygotuj`, {json: {dok}})), ladujDotacje); }
async function sprawdzDotacje() { sledz(await bezpiecznie(() => api(`${DOT_URL()}/sprawdz`, {json: {}})), ladujDotacje); }
async function kompletDotacji() {
  const w = await bezpiecznie(() => api(`${DOT_URL()}/komplet`, {json: {}})); if (!w) return;
  komunikat(w.brakuje.length ? `Komplet gotowy – brakuje jeszcze: ${w.brakuje.length} dokumentów.` : "Komplet gotowy do złożenia."); location.href = w.url; ladujDotacje();
}
function przeniesienieKosztorysu(p) {
  const pk = (et, ik_, typ, opis) => `<button class="przen-kafel" onclick="przeniesKosztorys('${typ}')"><span>${ik(ik_)}</span><b>${et}</b><small>${opis}</small></button>`;
  return `<div class="etap-b"><h4 class="etap-kroku"><span>B</span> Zapisz kosztorys albo przenieś go do innego modułu</h4>
    <p class="opis">Kosztorys jest zapisany w zakładce <b>Kosztorysy</b> – pobierzesz go w każdej chwili. Możesz też utworzyć z niego projekt w innym module
      (kopia – kosztorys zostaje tutaj):</p>
    <div class="pliki-ik">${plikIk(p.id, p.kosztorys, "Kosztorys (Excel)")}${plikIk(p.id, p.kosztorys_klienta, "Kosztorys dla klienta")}</div>
    <div class="przen">${pk("Wykonawca", "kask", "wlasny", "projekt własny: oferta dla klienta, umowa, materiały, realizacja")}
      ${pk("Zamawiający", "teczka", "zamowienie", "projekt zamówienia: kosztorys inwestorski, SWZ, weryfikacja")}
      ${pk("Inwestor indywidualny", "folder", "dom", "budowa domu: budżet, etapy, odbiory, formalności")}</div></div>`;
}
async function przeniesKosztorys(typ) {
  const nazwy = {wlasny: "Wykonawca – projekt własny", zamowienie: "Zamawiający – projekt zamówienia", dom: "Inwestor indywidualny – budowa domu"};
  if (!confirm(`Utworzyć kopię kosztorysu w module: ${nazwy[typ]}? Kosztorys zostanie też w Kosztorysowaniu.`)) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kopiuj`, {json: {typ}})); if (!w) return;
  komunikat(`Utworzono: ${nazwy[typ]}. Przechodzę do projektu.`);
  wybierzStrone(w.strona); PROJEKT_ID = w.id; TRYB = typ;
  setTimeout(() => pokaz({wlasny: "wlasne", zamowienie: "zam_projekty", dom: "inw_projekty"}[typ]), 300);
}
async function ofertaZKosztorysu() {
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/oferta-z-kosztorysu`, {json: {gwarancja: ($("#of-gwar") || {}).value || ""}}));
  if (!w) return;
  if (w.zadanie) {  // roboty: formularz ofertowy i oświadczenia według wzorów zamawiającego (AI)
    komunikat("Kosztorys dla zamawiającego gotowy. AI wypełnia formularz ofertowy i oświadczenia według wzorów z SWZ…");
    sledz(w.zadanie, () => odswiezProjekt());
  } else komunikat(w.uwaga || "Gotowa oferta na podstawie kosztorysu: formularze ofertowe i analiza.");
  odswiezProjekt();
}
async function ofertaKlienta() {
  const d = {}; ["klient_nazwa", "klient_adres", "klient_osoba", "termin_realizacji", "gwarancja", "platnosc", "waznosc", "miejsce", "uwagi"].forEach(k => d[k] = $("#ok-" + k).value);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/oferta-klienta`, {json: d})); if (!w) return;
  komunikat("Gotowa oferta dla klienta."); location.href = w.url; odswiezProjekt();
}
async function wgrajKosztorysWlasny(f) {
  if (!f) return; const fd = new FormData(); fd.append("plik", f);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kosztorys-wlasny`, {method: "POST", body: fd})); if (!w) return;
  if (w.zadanie) { komunikat("AI przepisuje Twój kosztorys – kilka minut."); sledz(w.zadanie, odswiezProjekt); }
  else { komunikat(`Wczytano kosztorys: ${w.wczytano} pozycji.`); odswiezProjekt(); }
}
async function generujOferte() {
  const ceny = document.querySelector('input[name="ceny-zrodlo"]:checked')?.value || "rynkowe";
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/oferta`, {json: {wskazowki: $("#wsk-oferta").value, vat_wybor: $("#vat-wybor").value, ceny}})), odswiezProjekt);
}
// ---------- własny cennik
let CENNIK = null;
async function ladujCennikStan(sila) {
  const el = $("#cennik-stan"); if (!el) return;
  if (!CENNIK || sila) CENNIK = await api("/api/cennik-wlasny").catch(() => ({liczba: 0}));
  el.innerHTML = (CENNIK.liczba ? `Mój cennik: <b>${CENNIK.liczba} pozycji</b> <span class="opis" style="margin:0">(${esc(CENNIK.plik || "")}, ${esc(CENNIK.data || "")})</span>
      <a href="#" onclick="pokazCennik(); return false">pokaż</a>` : '<span class="opis" style="margin:0">Nie masz jeszcze własnego cennika.</span>')
    + ` <label class="przycisk maly" data-ik="wgraj">${CENNIK.liczba ? "Wgraj nowy cennik" : "Wgraj cennik (Excel lub CSV)"}<input type="file" accept=".xlsx,.xlsm,.csv,.txt" hidden onchange="wgrajCennik(this.files[0])"></label>
      <a class="przycisk maly dozw" data-ik="pobierz" href="/api/cennik-wlasny/wzor.xlsx">Wzór cennika</a>
      ${CENNIK.liczba ? `<button class="maly niebezp" data-ik="kosz" onclick="usunCennik()">Usuń cennik</button>` : ""}<div id="cennik-podglad"></div>`;
  wstawIkony(el);
}
async function wgrajCennik(f) {
  if (!f) return; const fd = new FormData(); fd.append("plik", f);
  const w = await bezpiecznie(() => api("/api/cennik-wlasny", {method: "POST", body: fd})); if (!w) return;
  komunikat(`Wczytano cennik: ${w.liczba} pozycji.`); const r = document.querySelector('input[name="ceny-zrodlo"][value="cennik"]'); if (r) r.checked = true;
  ladujCennikStan(true);
}
async function usunCennik() { if (confirm("Usunąć własny cennik?") && await bezpiecznie(() => api("/api/cennik-wlasny/usun", {json: {}}))) { CENNIK = null; ladujCennikStan(true); } }
function pokazCennik() {
  const el = $("#cennik-podglad"); if (el.innerHTML) { el.innerHTML = ""; return; }
  el.innerHTML = `<div class="tabela-okno" style="max-height:260px;margin-top:6px"><table class="tabela"><tr><th>Kod</th><th>Opis</th><th>j.m.</th><th>Cena netto</th></tr>
    ${CENNIK.pozycje.slice(0, 500).map(c => `<tr><td>${esc(c.kod || "")}</td><td>${esc(c.opis)}</td><td>${esc(c.jm || "")}</td><td class="liczba">${zl(c.cena)}</td></tr>`).join("")}</table></div>`;
}
// ---------- poprawianie wybranych pozycji kosztorysu
let POZ = null;
async function ladujPozycje() {
  const el = $("#popraw-pozycje"); if (!el) return;
  const d = await api(`/api/projekty/${PROJEKT_ID}/pozycje`).catch(() => null); if (!d || d.brak) { el.innerHTML = ""; return; }
  POZ = d; rysujPozycje();
}
function rysujPozycje() {
  const el = $("#popraw-pozycje"); let lp = 0;
  el.innerHTML = `<p class="opis">Przy każdej pozycji wybierz: <b>Modyfikuj</b> – zaznacz ją i wpisz własną nazwę oraz cenę jednostkową <b>albo</b> wartość pozycji,
      lub <b>Usuń</b> – cała pozycja zostanie usunięta z kosztorysu. Po zapisaniu poprawiony kosztorys staje się podstawą oferty, materiałów, harmonogramu i umowy.</p>
    <input id="poz-szukaj" placeholder="Szukaj pozycji…" oninput="filtrujPozycje(this.value)" style="max-width:320px;margin-bottom:6px">
    <div class="tabela-okno" style="max-height:480px"><table class="tabela poz-tab"><tr><th></th><th>Lp.</th><th>Opis pozycji</th><th>j.m.</th><th>Ilość</th><th>Cena jedn. netto</th><th>Wartość netto</th><th>Źródło ceny</th><th>Usuń</th></tr>
    ${POZ.dzialy.map((dz, di) => `<tr class="wn-k-dzial"><td colspan="9">${esc(dz.nazwa)}</td></tr>` + dz.pozycje.map((p, pi) => `<tr id="poz-${di}-${pi}" data-szuk="${esc((p.opis || "").toLowerCase())}">
      <td><input type="checkbox" onchange="zaznaczPoz(${di},${pi},this.checked)"></td><td>${++lp}</td>
      <td><input class="poz-opis" disabled value="${esc(p.opis)}"></td><td>${esc(p.jm)}</td><td class="liczba">${String(p.ilosc).replace(".", ",")}</td>
      <td><input class="poz-cena wn-k-in" disabled value="${String(p.cena).replace(".", ",")}" oninput="pozWartosc(${di},${pi})"></td>
      <td><input class="poz-wart wn-k-in" disabled value="${String(p.wartosc).replace(".", ",")}" oninput="pozCena(${di},${pi})"></td>
      <td><small class="opis">${esc(p.zrodlo || "")}</small></td>
      <td><button class="maly niebezp poz-usun-btn" data-ik="kosz" title="Usuń całą pozycję" onclick="usunPoz(${di},${pi})"></button></td></tr>`).join("")).join("")}</table></div>
    <div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="zapisz" onclick="zapiszPozycje()">Zapisz zmiany i przelicz kosztorys</button>
      <button class="niebezp" data-ik="kosz" onclick="usunZaznaczonePoz()">Usuń zaznaczone pozycje</button>
      <span class="opis" style="margin:0" id="poz-info">Do zmiany: 0 · do usunięcia: 0</span></div>`;
  wstawIkony(el);
}
function filtrujPozycje(q) { q = q.toLowerCase(); document.querySelectorAll(".poz-tab tr[data-szuk]").forEach(t => t.style.display = !q || t.dataset.szuk.includes(q) ? "" : "none"); }
function infoPoz() {
  $("#poz-info").textContent = `Do zmiany: ${document.querySelectorAll(".poz-tab tr.poz-zazn:not(.poz-usun)").length} · do usunięcia: ${document.querySelectorAll(".poz-tab tr.poz-usun").length}`;
}
function zaznaczPoz(di, pi, on) {
  const t = $(`#poz-${di}-${pi}`); t.classList.toggle("poz-zazn", on); if (!on) t.classList.remove("poz-usun");
  t.querySelectorAll("input:not([type=checkbox])").forEach(i => i.disabled = !on || t.classList.contains("poz-usun"));
  infoPoz();
}
function usunPoz(di, pi) {  // przełącznik: pozycja do usunięcia / przywróć
  const t = $(`#poz-${di}-${pi}`), on = !t.classList.contains("poz-usun");
  t.classList.toggle("poz-usun", on); t.classList.toggle("poz-zazn", on); t.querySelector("input[type=checkbox]").checked = on;
  t.querySelectorAll("input:not([type=checkbox])").forEach(i => i.disabled = true);
  t.querySelector(".poz-usun-btn").title = on ? "Przywróć pozycję" : "Usuń całą pozycję";
  infoPoz();
}
async function usunZaznaczonePoz() {
  const zazn = [...document.querySelectorAll(".poz-tab tr.poz-zazn")];
  if (!zazn.length) return komunikat("Zaznacz pozycje do usunięcia.", true);
  zazn.forEach(t => t.classList.add("poz-usun")); infoPoz(); zapiszPozycje();
}
function pozWartosc(di, pi) { const t = $(`#poz-${di}-${pi}`), p = POZ.dzialy[di].pozycje[pi]; t.querySelector(".poz-wart").value = (Math.round(liczbaPL(t.querySelector(".poz-cena").value) * p.ilosc * 100) / 100).toString().replace(".", ","); t.dataset.tryb = "cena"; }
function pozCena(di, pi) { const t = $(`#poz-${di}-${pi}`), p = POZ.dzialy[di].pozycje[pi]; t.querySelector(".poz-cena").value = (p.ilosc ? Math.round(liczbaPL(t.querySelector(".poz-wart").value) / p.ilosc * 100) / 100 : 0).toString().replace(".", ","); t.dataset.tryb = "wartosc"; }
async function zapiszPozycje() {
  const usun = document.querySelectorAll(".poz-tab tr.poz-usun").length;
  if (usun && !confirm(`Usunąć z kosztorysu ${odm(usun, "pozycję", "pozycje", "pozycji")}? Kosztorys i dalsze kroki przeliczą się bez nich.`)) return;
  const zmiany = [...document.querySelectorAll(".poz-tab tr.poz-zazn")].map(t => { const [, di, pi] = t.id.split("-");
    if (t.classList.contains("poz-usun")) return {d: +di, p: +pi, usun: true};
    const z = {d: +di, p: +pi, opis: t.querySelector(".poz-opis").value};
    if (t.dataset.tryb === "wartosc") z.wartosc = t.querySelector(".poz-wart").value; else z.cena = t.querySelector(".poz-cena").value; return z; });
  if (!zmiany.length) return komunikat("Zaznacz pozycje do poprawienia.", true);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pozycje`, {json: {zmiany}}));
  if (w) { komunikat(`${w.poprawiono ? "Zmieniono: " + w.poprawiono + ". " : ""}${w.usunieto ? "Usunięto: " + w.usunieto + ". " : ""}Kosztorys: ${zl(w.oferta.brutto)} brutto.`); odswiezProjekt(); }
}
async function zmienVat() {
  const v = $("#vat-zmiana").value; if (v === "auto") return komunikat("Wybierz konkretną stawkę VAT.", true);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/vat`, {json: {vat: v}}));
  if (w) { komunikat(`Przeliczono ze stawką VAT ${Math.round(w.vat * 100)}%: ${zl(w.brutto)} brutto.`); otworzProjekt(PROJEKT_ID); }
}
async function kosztorysNaProjekt(id) {
  if (!confirm("Utworzyć z tego kosztorysu projekt własny? Przeniesie się do zakładki „Własne projekty”, gdzie przygotujesz ofertę, materiały, harmonogram i zamówienia.")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${id}/typ`, {json: {typ: "wlasny"}}))) { TRYB = "wlasny"; PROJEKT_ID = id; komunikat("Przeniesiono do Własnych projektów."); pokaz("wlasne"); }
}
async function dostosujCene(reset) {
  const tryb = reset ? "reset" : document.querySelector('input[name=kt]:checked').value, wartosc = $("#kt-wartosc")?.value;
  if (!reset && !wartosc) return komunikat("Podaj wartość.", true);
  const o = PROJEKT.oferta, baza = o.netto_pierwotne ?? o.netto;
  if (!reset) {
    const w = parseFloat(String(wartosc).replace(/\s/g, "").replace(",", "."));
    const cel = tryb === "netto" ? w : tryb === "brutto" ? w / (1 + o.vat) : baza * (1 + w / 100);
    const proc = (cel / baza - 1) * 100;
    if (!confirm(`Ceny wszystkich pozycji zmienią się o ${proc > 0 ? "+" : ""}${proc.toFixed(2)}% względem wyceny pierwotnej. Kontynuować?`)) return;
  }
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/dostosuj`, {json: {tryb, wartosc}})); if (!w) return;
  komunikat(reset ? "Przywrócono cenę pierwotną." : `Nowa cena: ${zl(w.netto)} netto / ${zl(w.brutto)} brutto` +
    (w.korekta && Math.abs(w.korekta.roznica_zaokraglen) >= 0.01 ? ` (różnica z zaokrągleń ${zl(w.korekta.roznica_zaokraglen)})` : "") +
    (w.korekta && w.korekta.info ? ` ${w.korekta.info}` : ""));
  otworzProjekt(PROJEKT_ID);
}
async function generujMaterialy() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/materialy`, {json: {wskazowki: $("#wsk-mat").value}})), odswiezProjekt); }
function liczWybranych() {
  const n = document.querySelectorAll(".h-wyb:checked").length;
  if (n > +$("#h-prac").value) $("#h-prac").value = n;
}
async function generujHarmonogram() {
  const s = $("#h-start").value; if (!s) return komunikat("Podaj datę startu.", true);
  const [r, mi, d] = s.split("-");
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/harmonogram`, {json: {start: `${d}.${mi}.${r}`, etapy: +$("#h-n").value,
    dlugosc: +$("#h-dl").value, pracownicy: +$("#h-prac").value, wybrani: [...document.querySelectorAll(".h-wyb:checked")].map(c => c.value), budowa: $("#h-budowa").value, adres: $("#h-adres").value, wskazowki: $("#wsk-harm").value}})), odswiezProjekt);
}
function daneZam(sposob) {
  return {etap: +$("#z-etap").value, typ: $("#z-typ").value, termin: $("#z-termin").value, adres: $("#z-adres").value,
    dopisek: $("#z-dopisek").value, hurtownie: [...document.querySelectorAll(".zh:checked")].map(c => +c.value), sposob};
}
async function podgladZam() {
  const d = daneZam(); if (!d.hurtownie.length) return komunikat("Zaznacz hurtownie.", true);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/zamowienie/podglad`, {json: d})); if (!w) return;
  $("#z-wynik").innerHTML = w.map(x => x.pusto ? `<p class="opis">${esc(x.hurtownia)}: brak materiałów z asortymentu w tym etapie – zostanie pominięta.</p>` :
    `<div class="podglad">Do: ${esc(x.email)}\nTemat: ${esc(x.temat)}\nZałącznik: arkusz Excel (${x.n} pozycji)\n${"-".repeat(60)}\n${esc(x.tekst)}</div>`).join("");
}
async function wyslijZam(sposob) {
  const d = daneZam(sposob); if (!d.hurtownie.length) return komunikat("Zaznacz hurtownie.", true);
  const nazwy = d.hurtownie.map(i => `• ${HURTOWNIE[i].nazwa} <${HURTOWNIE[i].email}>`).join("\n");
  if (sposob === "smtp" && !confirm(`Wysłać ${d.typ === "zamowienie" ? "ZAMÓWIENIE" : "zapytanie ofertowe"} natychmiast do:\n\n${nazwy}`)) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/zamowienie/wyslij`, {json: d})); if (!w) return;
  if (sposob === "smtp") { komunikat(`Wysłano ${w.wyslane} wiadomości.`); $("#z-wynik").innerHTML = `<p>Wysłano ${w.wyslane} wiadomości. Historia w zakładce Hurtownie.</p>`; }
  else $("#z-wynik").innerHTML = `<p class="opis">Pobierz szkice i otwórz je – otworzą się w Outlooku jako nowe wiadomości z załącznikiem. Sprawdź i kliknij „Wyślij”.</p>
    <div class="pliki-wynik">${w.linki.map(l => `<a href="${esc(l.url)}">✉ ${esc(l.hurtownia)}</a>`).join("")}</div>`;
}

// ================================================================ W REALIZACJI
let REAL_ID = null, REAL = null, STRONA_REAL = "wykonawca";
const KATEGORIE = ["materiały", "podwykonawcy", "sprzęt", "transport", "wywóz odpadów", "inne"];
const KATEGORIE_ZAM = ["nadzór / inspektor", "dokumentacja / ekspertyzy", "opłaty i ogłoszenia", "ubezpieczenia", "media / eksploatacja", "inne"];
async function ladujRealizacje() {
  const l = await bezpiecznie(() => api("/api/realizacja?strona=" + STRONA_REAL + (STRONA_REAL === "zamawiajacy" ? "&modul=" + MZ().klucz : ""))); if (!l) return;
  $("#w-realizacja aside h3").textContent = STRONA_REAL === "zamawiajacy" ? MZ().realizacja_naglowek : {zamawiajacy: "Realizacja umów", inwestor: "Moje budowy"}[STRONA_REAL] || "Budowy w realizacji";
  const nowaInw = $("#w-realizacja aside #nowa-inw");
  if (STRONA_REAL === "zamawiajacy" && MZ().nowa_inwestycja) { if (!nowaInw) $("#w-realizacja aside h3").insertAdjacentHTML("afterend", '<button id="nowa-inw" class="glowny" data-ik="plus" onclick="nowaInwestycja()" style="margin:6px 0">Nowa inwestycja</button>'); wstawIkony($("#w-realizacja aside")); }
  else if (nowaInw) nowaInw.remove();
  $("#lista-realizacji").innerHTML = l.map(p => `<li class="${p.id === REAL_ID ? "akt" : ""}" onclick="otworzRealizacje('${p.id}')">
    ${esc(p.nazwa)}<small>${p.typ === "wlasny" ? "projekt własny · " : p.typ === "przetarg" ? "z przetargu · " : ""}${p.status === "zakonczony" ? "zakończona · " : ""}${p.wartosc == null ? "" : "umowa " + zl(p.wartosc)}${ADMIN() && p.wlasciciel && p.wlasciciel !== JA.login ? " · konto: " + esc(p.wlasciciel) : ""}${p.przeterminowane ? ` · <span style="color:#ffb4b4">zaległe ${zl(p.przeterminowane)}</span>` : ""}</small></li>`).join("")
    || (STRONA_REAL === "inwestor" ? '<li class="pusto">Brak budowy. W module „Mój dom – projekt i kosztorys” kliknij „Rozpocznij budowę”.</li>' : STRONA_REAL === "zamawiajacy" ? '<li class="pusto">Brak umów w realizacji. W kreatorze zamówienia (krok „Gotowe do publikacji”) kliknij „Umowa podpisana – prowadź realizację umowy”.</li>'
      : '<li class="pusto">Brak budów w realizacji. W zakładce „Projekty z przetargów” kliknij „Przetarg wygrany – do realizacji”, a we „Własnych projektach” – „Przenieś do realizacji”.</li>');
  if (REAL_ID && l.some(p => p.id === REAL_ID)) otworzRealizacje(REAL_ID);
  else if (l.length) otworzRealizacje(l[0].id);  // od razu pierwsza budowa – w menu rozwija się lista jej sekcji
}
async function otworzRealizacje(id) {
  const innaB = !REAL || REAL.projekt.id !== id;
  REAL_ID = id;
  document.querySelectorAll("#lista-realizacji li").forEach(li => li.classList.toggle("akt", li.getAttribute("onclick")?.includes(id)));
  REAL = await bezpiecznie(() => api(`/api/projekty/${id}/realizacja`)); if (!REAL) return;
  if (!PRACOWNICY.length) PRACOWNICY = ((await api("/api/pracownicy").catch(() => null)) || {}).pracownicy || [];
  rysujRealizacje();
  oznaczPrzewijane($("#realizacja"));
  if (innaB) $("#realizacja").scrollTop = 0;
  if ($("#pogoda-tresc")) ladujPogode(innaB);
  if ($("#fin-tresc")) ladujFin();
  if ($("#rozl-mat")) ladujRozlMat();
  if ($("#pw-tresc")) ladujPw();
}
const odswiezReal = () => otworzRealizacje(REAL_ID);
// tabele szersze niż ich okno (np. harmonogram z wieloma etapami): widoczny pasek przewijania i wskazówka „przewiń w bok” – nic nie jest ucięte bez śladu.
// Sprawdzane przy każdej zmianie szerokości (także gdy ukryty krok staje się widoczny).
const PRZEWIJANE_OBS = "ResizeObserver" in window ? new ResizeObserver(w => w.forEach(x => sprawdzPrzewijanie(x.target))) : null;
function sprawdzPrzewijanie(o) {
  if (!o.isConnected || !o.clientWidth) return;
  const jest = o.scrollWidth > o.clientWidth + 2, w = o.nextElementSibling, ma = !!(w && w.classList.contains("przewin-wsk"));
  o.classList.toggle("ma-przewijanie", jest);
  if (jest && !ma) o.insertAdjacentHTML("afterend", '<p class="przewin-wsk">↔ Tabela jest szersza niż okno – przewiń ją w bok, aby zobaczyć wszystkie kolumny.</p>');
  if (!jest && ma) w.remove();
}
function oznaczPrzewijane(korzen) {
  if (!korzen) return;
  korzen.querySelectorAll(".tabela-okno").forEach(o => { sprawdzPrzewijanie(o); if (PRZEWIJANE_OBS) PRZEWIJANE_OBS.observe(o); });
}
function stanFaktury(f) {
  if (f.zaplacona) return ['<span class="znacznik z-startujemy">zapłacona</span>', ""];
  return f.termin < dzis() ? ['<span class="znacznik z-czerwony">po terminie</span>', "czerwone"] : ['<span class="znacznik z-do-analizy">oczekuje</span>', ""];
}
function rysujRealizacje() {
  const R = REAL, r = R.realizacja, s = R.podsumowanie, hrf = r.hrf, vat = (r.vat === "" || r.vat == null) ? 0.23 : (+r.vat > 1 ? +r.vat / 100 : +r.vat), ZR = R.projekt.strona === "zamawiajacy",
    RZR = ZR ? (R.projekt.rodzaj_zamowienia || "roboty") : "roboty", ZU = RZR !== "roboty", ZI = R.projekt.strona === "inwestor";
  const BF = !!R.bez_finansow || poziomU("finanse") < 1;  // rola bez Finansów (np. kierownik budowy): bez kwot umowy, faktur, kosztów i stawek
  const karta = (t, v, kl = "") => `<div class="${kl}"><span>${t}</span><b>${zl(v)}</b></div>`;
  const etapySel = hrf ? hrf.etapy.map((e, i) => `<option value="${i}">Etap ${e.nr}: ${esc(e.nazwa)}${BF ? "" : ` (${zl(e.wartosc)} netto)`}</option>`).join("") : "";
  $("#realizacja").innerHTML = `
  <div class="naglowek"><h2 style="margin:0;flex:1">${esc(R.projekt.nazwa)}</h2>
    ${poziomU("projekty") >= 2 ? `<select onchange="statusBudowy(this.value)"><option value="realizacja" ${R.projekt.status_projektu === "realizacja" ? "selected" : ""}>W realizacji</option>
      <option value="zakonczony" ${R.projekt.status_projektu === "zakonczony" ? "selected" : ""}>Zakończona</option></select>`
      : `<span class="znacznik">${R.projekt.status_projektu === "zakonczony" ? "zakończona" : "w realizacji"}</span>`}
    <a class="przycisk dozw fin" data-ik="pobierz" href="/api/projekty/${REAL_ID}/rozliczenie.xlsx">Rozliczenie (Excel)</a>
    <a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${REAL_ID}/raport.docx">Raport (Word)</a>
    <button class="dozw" data-ik="folder" onclick="kartaProjektu('${REAL_ID}', '${R.projekt.typ || "przetarg"}')">Karta projektu</button></div>
  ${kartaRealizacji(R)}
  ${BF ? "" : ZI ? kwotyDomu(R) : ZR ? `<div class="kwoty">${karta("Wartość umowy netto", s.wartosc_umowy_netto)}${karta("Odebrano netto", s.odebrano_netto)}
    ${karta("Pozostało do odbioru netto", Math.max(0, s.wartosc_umowy_netto - s.odebrano_netto))}${karta("Faktury wykonawcy brutto", s.zafakturowano_brutto)}
    ${karta("Zapłacono wykonawcy brutto", s.zaplacono_brutto, "brutto")}${karta("Do zapłaty brutto", s.naleznosci_brutto)}
    ${s.przeterminowane_brutto ? karta("Po terminie", s.przeterminowane_brutto, "alarm") : ""}${karta("Inne koszty netto", s.koszty_netto)}</div>` : `<div class="kwoty">${karta("Wartość umowy netto", s.wartosc_umowy_netto)}${karta("Odebrano netto", s.odebrano_netto)}
    ${karta("Zafakturowano brutto", s.zafakturowano_brutto)}${karta("Zapłacono brutto", s.zaplacono_brutto, "brutto")}
    ${karta("Należności brutto", s.naleznosci_brutto)}${s.przeterminowane_brutto ? karta("Po terminie", s.przeterminowane_brutto, "alarm") : ""}
    ${karta("Koszty + robocizna", s.koszty_razem)}${karta("Wynik bieżący", s.wynik_biezacy, s.wynik_biezacy < 0 ? "alarm" : "")}
    <div class="${s.wynik_prognoza != null && s.wynik_prognoza < 0 ? "alarm" : ""}" title="${esc(s.prognoza_metoda || "")}"><span>Wynik prognozowany (z postępu prac)</span><b>${s.wynik_prognoza == null ? "brak danych do prognozy" : zl(s.wynik_prognoza)}</b>
      <small class="opis" style="display:block;font-weight:normal">${esc(s.prognoza_metoda || "")}</small></div></div>`}

  <div class="krok"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>${ZI ? "Dane budowy i dokumenty" : ZU ? "Umowa i dokumenty" : "Umowa i dokumenty budowy"}</h3></div><div class="tresc">
    <div class="siatka">
      <label>${ZI ? "Nr pozwolenia na budowę / zgłoszenia" : "Nr umowy"}<input id="um-nr" value="${esc(r.umowa_nr || "")}"></label>
      <label>${ZI ? "Data rozpoczęcia budowy" : "Data umowy"}<input type="date" id="um-data" value="${esc(r.data_umowy || "")}"></label>
      ${BF ? "" : `<label>${ZI ? "Budżet budowy netto [zł] (z kosztorysu)" : ZR ? "Wartość umowy netto [zł] – cena z oferty wykonawcy" : "Wartość umowy netto [zł]"}<input id="um-wart" inputmode="decimal" value="${esc(r.wartosc_netto || "")}"
        ${ZR && r.wartosc_szacunkowa ? `placeholder="szacunkowo ${zl(+r.wartosc_szacunkowa)}"` : ""}></label>
      <label>Stawka VAT${r.vat === "" || r.vat == null ? ' <b class="czerwone">– do ustalenia</b>' : ""}<select id="um-vat">
        <option value="" ${r.vat === "" || r.vat == null ? "selected" : ""}>${ZR ? "– wybierz (z oferty wykonawcy / umowy) –" : "– wybierz (ustal z zamawiającym) –"}</option>
        ${[["0.23", "23%"], ["0.08", "8%"], ["0.05", "5%"], ["0", "0% / zw."]].map(([v, n]) => `<option value="${v}" ${r.vat !== "" && r.vat != null && Math.abs(+r.vat - +v) < 1e-9 ? "selected" : ""}>${n}</option>`).join("")}</select></label>`}
      <label>${ZU ? "Termin wykonania umowy" : "Termin zakończenia"}<input type="date" id="um-termin" value="${esc(r.termin_zakonczenia || "")}"></label>
      <label>${ZU ? "Przedstawiciel wykonawcy (koordynator umowy)" : "Kierownik budowy"}<input id="um-kier" value="${esc(r.kierownik || "")}"></label>
      <label>${ZU ? "Osoba nadzorująca umowę (zamawiający)" : "Inspektor nadzoru"}<input id="um-insp" value="${esc(r.inspektor || "")}"></label>
      <label>${RZR === "dostawy" ? "Miejsce dostawy" : ZU ? "Miejsce świadczenia usług" : "Adres budowy"}<input id="um-adres" value="${esc(r.adres || (R.oferta && R.oferta.obiekt) || "")}"></label>
      ${ZR ? `<label style="grid-column: span 2">Wykonawca (nazwa)<input id="um-wyk-nazwa" value="${esc(r.wykonawca_nazwa || "")}"></label>
        <label>NIP wykonawcy<input id="um-wyk-nip" value="${esc(r.wykonawca_nip || "")}"></label>
        <label style="grid-column: span 2">Adres wykonawcy<input id="um-wyk-adres" value="${esc(r.wykonawca_adres || "")}"></label>
        <label>&nbsp;<button type="button" class="zolty" data-ik="szukaj" onclick="wykonawcaPoNip()">Dane wykonawcy po NIP</button></label>` : ""}
    </div>
    ${ZR && !BF && !+r.wartosc_netto ? `<div class="ramka-uwaga">Wpisz <b>wartość umowy netto</b> – cenę z oferty wybranego wykonawcy${r.wartosc_szacunkowa ? ` (wartość szacunkowa zamówienia: ${zl(+r.wartosc_szacunkowa)})` : ""}. Od niej liczą się harmonogram, odbiory i faktury.</div>` : ""}
    <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszUmowe()">Zapisz dane umowy</button></div>
    <div class="upusc" id="upusc-bud">${ZU ? "Dokumenty umowy (umowa, oferta wykonawcy, aneksy, gwarancje, certyfikaty, zdjęcia)" : "Dokumenty budowy (umowa, protokół przekazania placu, dziennik, atesty, zdjęcia)"} – przeciągnij tutaj albo
      <label class="przycisk" data-ik="wgraj">wybierz z dysku<input type="file" multiple hidden onchange="wgrajBudowa(this.files)"></label></div>
    ${R.pliki.map(g => `<h3 style="margin:14px 0 6px">${esc(g.tytul)}</h3><div class="pliki-wynik">${g.pliki.map(f =>
      `<a href="/pobierz/${REAL_ID}/${f.sciezka.split("/").map(encodeURIComponent).join("/")}">${esc(f.nazwa)}</a>${g.kat === "realizacja/dokumenty" ?
        `<button class="maly niebezp tylko-admin" data-ik="kosz" onclick="usunPlikBudowy('${escA(f.sciezka)}')"></button>` : ""}`).join("")}</div>`).join("")}
  </div></div>

  <div class="krok k-ziel"><div class="tytul"><span class="nr">${ik("tabela")}</span><h3>${ZI ? "Harmonogram budowy (etapy)" : RZR === "uslugi" ? "Harmonogram i okresy rozliczeniowe usług" : RZR === "dostawy" ? "Harmonogram dostaw (dostawy częściowe)" : "Harmonogram rzeczowo-finansowy"}</h3>
    <span class="stan">${hrf ? hrf.etapy.length + (RZR === "uslugi" ? " okresów" : RZR === "dostawy" ? " dostaw" : " etapów") : "do utworzenia"}</span></div><div class="tresc">
    <p class="opis">${RZR === "uslugi" ? "Podstawa odbiorów i faktur za kolejne okresy rozliczeniowe (zwykle miesiące). Każdy okres ma taką samą część wartości umowy – możesz to zmienić w tabeli."
      : RZR === "dostawy" ? "Podstawa odbiorów i faktur za dostawy częściowe. Wpisz, jaki procent każdej grupy asortymentu przychodzi w danej dostawie (suma w wierszu = 100%); jedna dostawa = 1."
      : "Podstawa odbiorów częściowych i fakturowania. Wiersze to działy kosztorysu, kolumny – etapy. Wpisz, jaki procent działu zostanie wykonany w danym etapie (suma w wierszu = 100%)."}</p>
    ${(() => { const mies = r.data_umowy && r.termin_zakonczenia ? Math.max(1, Math.min(24, Math.round((new Date(r.termin_zakonczenia) - new Date(r.data_umowy)) / 2629746000))) : 4;
      return `<div class="siatka"><label>${RZR === "uslugi" ? "Liczba okresów rozliczeniowych" : RZR === "dostawy" ? "Liczba dostaw częściowych" : "Liczba etapów"}<input type="number" id="hrf-n" min="1" max="24" value="${hrf ? hrf.etapy.length : RZR === "uslugi" ? mies : RZR === "dostawy" ? 1 : 4}"></label>
      <label>${RZR === "uslugi" ? "Początek świadczenia usług" : RZR === "dostawy" ? "Termin pierwszej dostawy" : "Start robót"}<input type="date" id="hrf-start" value="${hrf ? hrf.etapy[0].od : (r.data_umowy || dzis())}"></label>
      <label>${RZR === "uslugi" ? "Długość okresu [dni] (30 = miesiące kalendarzowe)" : RZR === "dostawy" ? "Odstęp między dostawami [dni]" : "Długość etapu [dni]"}<input type="number" id="hrf-dl" min="1" value="30"></label></div>`; })()}
    <div class="pasek"><button class="${hrf ? "" : "zielony"}" data-ik="iskra" onclick="utworzHRF()">${hrf ? "Utwórz od nowa (propozycja)" : "Utwórz harmonogram"}</button>
      ${hrf ? `<button class="zielony" data-ik="zapisz" onclick="zapiszHRF()">Zapisz zmiany</button>
      ${BF ? "" : `<a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${REAL_ID}/hrf/xlsx">Pobierz HRF (Excel)</a>`}` : ""}</div>
    ${hrf ? rysujHRF(hrf, vat, BF) : ""}
  </div></div>

  <div class="krok k-zolt"><div class="tytul"><span class="nr">${ik("protokol")}</span><h3>${RZR === "uslugi" ? "Protokoły odbioru usług (okresowe / częściowe)" : RZR === "dostawy" ? "Protokoły odbioru dostaw (ilościowo-jakościowe)" : "Protokoły odbioru"}</h3></div><div class="tresc">
    ${!hrf ? `<p class="pusto">Najpierw utwórz ${RZR === "uslugi" ? "okresy rozliczeniowe" : RZR === "dostawy" ? "harmonogram dostaw" : "harmonogram rzeczowo-finansowy"}.</p>` : `
    ${hrf.etapy.some(e => e.protokol) ? `<div class="pliki-wynik">${hrf.etapy.filter(e => e.protokol).map(e =>
      `<a href="/pobierz/${REAL_ID}/${e.protokol.split("/").map(encodeURIComponent).join("/")}">${RZR === "uslugi" ? "Okres" : RZR === "dostawy" ? "Dostawa" : "Etap"} ${e.nr} – odebrany ${dataPl(e.data_odbioru)}</a>`).join("")}</div>` : ""}
    <div class="siatka" style="margin-top:12px"><label>${RZR === "uslugi" ? "Okres rozliczeniowy" : RZR === "dostawy" ? "Dostawa" : "Etap"}<select id="pr-etap">${etapySel}</select></label>
      <label>Data odbioru<input type="date" id="pr-data" value="${dzis()}"></label>
      <label>Miejsce<input id="pr-miejsce" value="${esc(r.adres || "")}"></label></div>
    <div class="siatka">${ZI ? `<label>Wykonawca etapu<select id="pr-wykonawca"><option value="">– wybierz z listy wykonawców –</option>
        ${(r.wykonawcy || []).map(w => `<option value="${w.id}">${esc(w.nazwa)}${w.zakres ? " – " + esc(w.zakres) : ""}</option>`).join("")}</select></label>` : ""}
      <label>${ZI ? "Inwestor (odbierający)" : "Komisja – Zamawiający"}<input id="pr-zam" placeholder="imiona i nazwiska, funkcje"></label>
      ${((r.rozliczenie_mat || {}).pozycje || []).length ? `<label class="check" style="grid-column: 1 / -1"><input type="checkbox" id="pr-mat" checked> do protokołu końcowego dołącz wykaz zużytych materiałów (${r.rozliczenie_mat.pozycje.length} poz.) z listą kart materiałowych</label>` : ""}
      <label>${ZI ? "Przedstawiciel wykonawcy / kierownik budowy" : ZU ? "Przedstawiciel wykonawcy" : "Komisja – Wykonawca"}<input id="pr-wyk" value="${esc(r.kierownik || "")}"></label>
      <label>${ZU ? "Termin usunięcia nieprawidłowości" : "Termin usunięcia usterek"}<input id="pr-term" placeholder="np. 15.11.2026"></label>
      ${RZR === "dostawy" ? `<label>Zgodność ilościowa<select id="pr-zil"><option>tak</option><option>nie</option></select></label>
        <label>Zgodność jakościowa<select id="pr-zjak"><option>tak</option><option>nie</option></select></label>
        <label style="grid-column: span 2">Dokumenty dostawy<input id="pr-ddok" placeholder="np. WZ nr 12/2026, karty gwarancyjne, instrukcje, certyfikaty"></label>` : ""}
      ${RZR === "uslugi" ? `<label>Usługi wykonane należycie<select id="pr-nal"><option>tak</option><option>nie</option></select></label>
        <label style="grid-column: span 2">Potrącenia / kary za okres<input id="pr-kary" placeholder="np. kara 150 zł – spóźnione dostarczenie posiłków 12.11"></label>` : ""}</div>
    <label class="opis" style="display:block;margin-bottom:4px">${ZU ? "Nieprawidłowości / braki (każda w osobnej linii; puste = brak)" : "Usterki (każda w osobnej linii; puste = brak usterek)"}</label>
    <textarea id="pr-ust"></textarea>
    <label class="opis" style="display:block;margin:8px 0 4px">Uwagi</label><textarea id="pr-uwagi" style="min-height:50px"></textarea>
    <div class="pasek" style="margin-top:10px"><button class="zolty" data-ik="protokol" onclick="utworzProtokol()">Utwórz protokół odbioru</button>
      <button data-ik="alarm" onclick="wstawUsterki()">${ZU ? "Wstaw otwarte reklamacje z listy" : "Wstaw otwarte usterki z listy"}</button></div>
    <div id="pr-wynik"></div>`}
  </div></div>

  ${BF ? "" : `<div class="krok"><div class="tytul"><span class="nr">${ik("faktura")}</span><h3>${ZI ? "Faktury wykonawców i sklepów" : ZR ? "Faktury wykonawcy (do zapłaty)" : "Faktury wystawione"}</h3>
    <span class="stan">${r.faktury.filter(f => !f.zaplacona).length} niezapłaconych</span></div><div class="tresc">
    <div class="siatka"><label>Numer faktury<input id="fv-nr"></label><label>Data wystawienia<input type="date" id="fv-data" value="${dzis()}"></label>
      <label>Termin płatności<input type="date" id="fv-termin"></label><label>Kwota netto [zł]<input id="fv-netto"></label>
      <label>VAT faktury<input id="fv-vat" value="${r.vat === "" || r.vat == null ? "" : vat}" placeholder="np. 0.23 lub 0.08"></label>
      <label>Etap<select id="fv-etap"><option value="">–</option>${etapySel}</select></label></div>
    <div class="pasek"><input id="fv-opis" placeholder="opis (opcjonalnie)" style="flex:1;min-width:240px">
      <label style="display:flex;gap:8px;align-items:center;font-weight:600"><input type="checkbox" id="fv-zapl"> zapłacona</label>
      <button class="zielony fin-edycja" data-ik="plus" onclick="dodajFakture()">Dodaj fakturę</button>
      ${!ZI && +r.wartosc_netto ? (() => { const fz = (r.faktury || []).reduce((a, f) => a + (+f.netto || 0), 0), zo = +r.wartosc_netto - fz;
        return `<span class="opis" style="margin:0">Wartość umowy ${zl(+r.wartosc_netto)} netto · zafakturowano ${zl(fz)} · <b class="${zo <= 0.01 ? "czerwone" : "zielone"}">do zafakturowania ${zl(Math.max(0, zo))}</b></span>`; })() : ""}</div>
    ${r.faktury.length ? `<div class="tabela-okno tk"><table class="tabela"><tr class="nagl"><th>Numer</th><th>Wystawiona / termin</th><th class="liczba">Netto / brutto</th><th>Etap</th><th>Status</th><th><span class="sr-only">Akcje</span></th></tr>
      ${r.faktury.slice().sort((a, b) => b.data.localeCompare(a.data)).map(f => { const [st, kl] = stanFaktury(f); return `<tr class="${kl}">
        <td class="szer tk-nr" data-et="Numer"><b>${esc(f.numer)}</b>${f.opis ? `<br><small class="opis">${esc(f.opis)}</small>` : ""}</td>
        <td data-et="Wystawiona / termin" class="tk-data">${dataPl(f.data)}<br><small class="opis">termin ${dataPl(f.termin)}</small></td>
        <td class="liczba" data-et="Netto / brutto">${zl(f.netto)}<br><b>${zl(f.brutto)}</b></td><td data-et="Etap">${f.etap !== null && f.etap !== "" && f.etap !== undefined ? "etap " + (+f.etap + 1) : "–"}</td>
        <td data-et="Status">${st}${f.zaplacona && f.data_zaplaty ? `<br><small class="opis">${dataPl(f.data_zaplaty)}</small>` : ""}</td>
        <td class="szer akcje"><button class="maly ${f.zaplacona ? "" : "zielony"}" data-ik="portfel" title="${f.zaplacona ? "Cofnij zapłatę" : "Oznacz jako zapłaconą"}" aria-label="${f.zaplacona ? "Cofnij zapłatę faktury" : "Oznacz jako zapłaconą fakturę"} ${esc(f.numer)}" onclick="zmienPoz('faktury','${f.id}',{zaplacona:${!f.zaplacona}})">${f.zaplacona ? "Cofnij" : "Zapłacona"}</button>
          <button class="maly niebezp" data-ik="kosz" title="Usuń fakturę" aria-label="Usuń fakturę ${esc(f.numer)}" onclick="zmienPoz('faktury','${f.id}',{usun:true})"></button></td></tr>`; }).join("")}</table></div>` : '<p class="pusto">Brak faktur.</p>'}
  </div></div>

  <div class="krok k-czer"><div class="tytul"><span class="nr">${ik("portfel")}</span><h3>${ZI ? "Inne wydatki (paragony, drobne zakupy, usługi)" : ZU ? "Inne koszty zamówienia" : ZR ? "Inne koszty inwestycji" : "Koszty budowy"}</h3>
    <span class="stan">${zl(s.koszty_netto)} netto</span></div><div class="tresc">
    <div class="siatka"><label>Data<input type="date" id="ko-data" value="${dzis()}"></label>
      <label>Kategoria<select id="ko-kat">${(ZR ? KATEGORIE_ZAM : KATEGORIE).map(k => `<option>${k}</option>`).join("")}</select></label>
      <label>Kwota netto [zł]<input id="ko-netto"></label><label>Dostawca<input id="ko-dost"></label>
      <label>Nr dokumentu<input id="ko-dok"></label></div>
    <div class="pasek"><input id="ko-opis" placeholder="${ZR ? "opis kosztu, np. nadzór inwestorski – październik, ogłoszenie, ubezpieczenie" : "opis kosztu, np. styropian 15 cm – dostawa 1"}" style="flex:1;min-width:260px">
      <label style="display:flex;gap:8px;align-items:center;font-weight:600"><input type="checkbox" id="ko-zapl"> zapłacony</label>
      <button class="zielony" data-ik="plus" onclick="dodajKoszt()">Dodaj koszt</button></div>
    ${Object.keys(s.koszty_kategorie).length ? `<div class="wybor-h">${Object.entries(s.koszty_kategorie).map(([k, v]) => `<span><b>${esc(k)}:</b> ${zl(v)}</span>`).join("")}</div>` : ""}
    ${r.koszty.length ? `<div class="tabela-okno tk"><table class="tabela"><tr class="nagl"><th>Data / kategoria</th><th>Opis</th><th>Dostawca / dokument</th><th class="liczba">Netto</th><th>Status</th><th><span class="sr-only">Akcje</span></th></tr>
      ${r.koszty.slice().sort((a, b) => b.data.localeCompare(a.data)).map(k => `<tr><td data-et="Data / kategoria" class="tk-data">${dataPl(k.data)}<br><small class="opis">${esc(k.kategoria)}</small></td><td class="szer" data-et="Opis">${esc(k.opis) || "–"}</td>
        <td class="szer" data-et="Dostawca / dokument">${esc(k.dostawca || "") || "–"}${k.dokument ? `<br><small class="opis">${esc(k.dokument)}</small>` : ""}</td><td class="liczba" data-et="Netto"><b>${zl(k.netto)}</b></td>
        <td data-et="Status">${k.zaplacona ? '<span class="znacznik z-startujemy">zapłacony</span>' : '<span class="znacznik z-do-analizy">do zapłaty</span>'}</td>
        <td class="szer akcje"><button class="maly" data-ik="portfel" title="${k.zaplacona ? "Cofnij zapłatę" : "Oznacz jako zapłacony"}" aria-label="${k.zaplacona ? "Cofnij zapłatę kosztu" : "Oznacz jako zapłacony koszt"} ${esc(k.dokument || k.opis || "")}" onclick="zmienPoz('koszty','${k.id}',{zaplacona:${!k.zaplacona}})">${k.zaplacona ? "Cofnij" : "Zapłacony"}</button>
          <button class="maly niebezp" data-ik="kosz" title="Usuń koszt" aria-label="Usuń koszt ${esc(k.dokument || k.opis || "")}" onclick="zmienPoz('koszty','${k.id}',{usun:true})"></button></td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak kosztów.</p>'}
  </div></div>`}

  ${ZI ? sekcjeDomu(R) : ""}
  ${ZI ? "" : `<div class="krok k-fiol" id="sek-pw"><div class="tytul"><span class="nr">${ik("ludzie")}</span><h3>${ZR ? "Podwykonawcy wykonawcy – zgłoszenia i oświadczenia o rozliczeniu" : "Podwykonawcy – zgłoszenia, umowy i rozliczenia"}</h3>
    <span class="stan">${(r.podwykonawcy || []).length ? r.podwykonawcy.length + " podwykonawców" : "brak"}</span></div>
    <div class="tresc" id="pw-tresc"><p class="opis">Ładuję…</p></div></div>`}
  ${ZU || poziomU("finanse") < 1 ? "" : `<div class="krok k-ziel" id="sek-rozl-mat"><div class="tytul"><span class="nr">${ik("teczka")}</span><h3>Rozliczenie inwestycji – karta zużytych materiałów</h3>
    <span class="stan">${((r.rozliczenie_mat || {}).pozycje || []).length ? r.rozliczenie_mat.pozycje.length + " pozycji" : "do przygotowania"}</span></div>
    <div class="tresc" id="rozl-mat"><p class="opis">Ładuję…</p></div></div>`}
  ${!ZR && !ZI ? `<div class="krok k-nieb" id="sek-pogoda"><div class="tytul"><span class="nr">${ik("alarm")}</span><h3>Monitoring pogody i wnioski o przedłużenie terminu</h3>
      <span class="stan" id="pogoda-stan">…</span></div><div class="tresc" id="pogoda-tresc"><p class="opis">Ładuję dane pogodowe…</p></div></div>` : ""}
  ${ZR ? `<div class="krok k-fiol" id="sek-fin"><div class="tytul"><span class="nr">${ik("portfel")}</span><h3>Finansowanie inwestycji (bank, BGK, KPO, dotacje)</h3>
    <span class="stan" id="fin-stan">…</span></div><div class="tresc" id="fin-tresc"><p class="opis">Ładuję…</p></div></div>` : ""}
  ${sekcjeBudowy(R, RZR)}
  ${ZR ? `<div class="krok k-ziel" id="sek-owu"><div class="tytul"><span class="nr">${ik("protokol")}</span><h3>Ogłoszenie o wykonaniu umowy (art. 448 Pzp)</h3>
    <span class="stan" id="owu-stan">…</span></div><div class="tresc" id="owu-tresc"><p class="opis">Ładuję…</p></div></div>` : ""}

  ${ZR || ZI ? "" : `<div class="krok"><div class="tytul"><span class="nr">${ik("ludzie")}</span><h3>Koszty pracownicze</h3>
    <span class="stan">${liczba(s.robocizna_godziny, 2)} h${BF ? "" : " · " + zl(s.robocizna)}</span></div><div class="tresc">
    <p class="opis">Godziny pracowników właściciela budowy wpisane na tym projekcie (tutaj albo w zakładce Pracownicy).</p>
    ${R.robocizna.length ? `<div class="tabela-okno" style="max-height:320px"><table class="tabela"><tr><th>Data</th><th>Pracownik</th><th>Godziny</th>${BF ? "" : "<th>Stawka</th><th>Kwota</th>"}<th>Opis</th><th></th></tr>
      ${R.robocizna.slice().sort((a, b) => b.data.localeCompare(a.data)).map(w => `<tr><td>${dataPl(w.data)}</td><td>${esc(w.imie)}</td><td class="liczba">${liczba(w.godziny, 2)}</td>
        ${BF ? "" : `<td class="liczba">${zl(w.stawka)}</td><td class="liczba">${zl(w.kwota)}</td>`}<td>${esc(w.opis || "")}</td>
        <td>${w.id && (w.kto === JA.login || ADMIN()) && poziomU("realizacja") >= 2 ? `<button class="maly niebezp" data-ik="kosz" aria-label="Usuń wpis" onclick="usunGodzinyBudowy('${escA(w.id)}')"></button>` : ""}</td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak wpisów godzin dla tej budowy.</p>'}
    <div id="godz-budowy"></div>
  </div></div>`}`;
  const u = $("#upusc-bud");
  if (u) {
    ["dragenter", "dragover"].forEach(e => u.addEventListener(e, ev => { ev.preventDefault(); u.classList.add("nad"); }));
    ["dragleave", "drop"].forEach(e => u.addEventListener(e, ev => { ev.preventDefault(); u.classList.remove("nad"); }));
    u.addEventListener("drop", ev => wgrajBudowa(ev.dataTransfer.files));
  }
  if ($("#dz-data")) wczytajWpis();
  if ($("#owu-tresc")) ladujOWU();
  if ($("#godz-budowy")) ladujGodzinyBudowy();
  paskiSekcji("#realizacja");  // telefon: pasek zakładek z krokami budowy (dziennik, zdjęcia, usterki) – bez niego widać tylko pierwszy krok
}
// ---------- godziny pracy na budowie – także udostępnionej przez inne konto: pracownicy właściciela budowy, bez stawek (H1-12)
async function ladujGodzinyBudowy() {
  const el = $("#godz-budowy"); if (!el) return;
  const G = await api(`/api/projekty/${REAL_ID}/godziny`).catch(() => null); if (!G) { el.innerHTML = ""; return; }
  if (!G.moze_wpisywac) { el.innerHTML = ""; return; }
  el.innerHTML = `<h4 class="grupa-analizy">Wpisz godziny pracy na tej budowie</h4>
    ${G.udostepniony ? '<p class="opis">Budowa udostępniona przez inne konto – wpisujesz godziny pracownikom właściciela budowy (stawki widzi właściciel).</p>' : ""}
    ${G.pracownicy.length ? `<div class="siatka"><label>Pracownik<select id="gb-prac">${G.pracownicy.map(p => `<option value="${esc(p.id)}">${esc(p.imie)}${p.stanowisko ? " – " + esc(p.stanowisko) : ""}</option>`).join("")}</select></label>
      <label>Data<input type="date" id="gb-data" value="${dzis()}" max="${dzis()}"></label><label>Godziny<input id="gb-godz" inputmode="decimal" placeholder="np. 8"></label>
      <label style="grid-column: span 2">Opis prac<input id="gb-opis" placeholder="np. ocieplenie ściany północnej"></label></div>
      <div class="pasek"><button class="zielony" data-ik="zegar" onclick="dodajGodzinyBudowy()">Dodaj godziny</button></div>`
      : '<p class="pusto">Właściciel budowy nie ma jeszcze pracowników na liście (Pracownicy).</p>'}`;
  wstawIkony(el);
}
async function dodajGodzinyBudowy() {
  const d = {pracownik: $("#gb-prac").value, data: $("#gb-data").value, godziny: $("#gb-godz").value, opis: $("#gb-opis").value};
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/godziny`, {json: d})); if (!w) return;
  komunikat(`Dodano: ${w.imie}, ${liczba(w.godziny, 2)} h.` + (w.ostrzezenie ? " " + w.ostrzezenie : ""), !!w.ostrzezenie); otworzRealizacje(REAL_ID);
}
async function usunGodzinyBudowy(id) {
  if (!confirm("Usunąć ten wpis godzin?")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/godziny/usun`, {json: {id}}))) otworzRealizacje(REAL_ID);
}
// ---------- ogłoszenie o wykonaniu umowy (art. 448 Pzp): dane z inwestycji, termin 30 dni, kontrola, tekst do BZP, dowód publikacji
let OWU = null;
async function ladujOWU() { OWU = await api(`/api/projekty/${REAL_ID}/ogloszenie-wykonania`).catch(() => null); if (OWU) rysujOWU(); }
function rysujOWU() {
  const S = OWU, o = S.dane || {}, pub = S.publikacja || {};
  const st = $("#owu-stan");
  if (st) st.textContent = S.opublikowane ? `opublikowano ${pub.data}` : S.termin_publikacji ? (S.dni_do_terminu < 0 ? `po terminie (${-S.dni_do_terminu} dni)` : `termin ${dataPl(S.termin_publikacji)} – zostało ${S.dni_do_terminu} dni`) : "po wykonaniu umowy";
  const kopia = (t, i) => `<button class="maly" onclick="navigator.clipboard?.writeText(OWU.pola[${i}][1]).then(() => komunikat('Skopiowano.'))">Kopiuj</button>`;
  $("#owu-tresc").innerHTML = `
    <p class="opis">Zamawiający w ciągu <b>30 dni od wykonania umowy</b> zamieszcza ogłoszenie w Biuletynie Zamówień Publicznych – dotyczy postępowań krajowych i unijnych,
      także po odstąpieniu od umowy. Program zbiera dane z tej umowy (dane umowy, odbiory, faktury, aneksy, podwykonawcy); uzupełnij kary i ocenę wykonania.</p>
    ${!S.opublikowane && S.termin_publikacji ? `<div class="ramka-uwaga ${S.dni_do_terminu <= 7 ? "" : ""}">${S.dni_do_terminu < 0 ? "⚠ Termin minął " + (-S.dni_do_terminu) + " dni temu – opublikuj ogłoszenie jak najszybciej." : `Ostatni dzień na publikację: <b>${dataPl(S.termin_publikacji)}</b> (zostało ${S.dni_do_terminu} dni).`}</div>` : ""}
    <h4 class="grupa-analizy">1. Wykonanie umowy</h4>
    <div class="siatka"><label>Data wykonania umowy<input type="date" id="owu-data" value="${esc(o.data_wykonania || S.data_wykonania || "")}"></label>
      <label>Pierwotny termin z umowy<input type="date" id="owu-termin" value="${esc(o.termin_pierwotny || S.termin_umowny || "")}"></label>
      <label>Okres, na jaki zawarto umowę<input id="owu-okres" value="${esc(o.okres || "")}" placeholder="np. od 01.03.2026 do 30.09.2026"></label>
      <label>Numer ogłoszenia o zamówieniu w BZP<input id="owu-nrz" value="${esc(o.nr_ogloszenia || "")}" placeholder="np. 2026/BZP 00123456/01"></label></div>
    <p class="opis" style="margin:4px 0">Podpowiedź daty: ${S.propozycje_daty.odbior ? `odbiór końcowy <b>${dataPl(S.propozycje_daty.odbior)}</b>` : "brak odebranych etapów"}${S.propozycje_daty.platnosc ? ` · ostatnia płatność <b>${dataPl(S.propozycje_daty.platnosc)}</b>` : ""}.
      Według UZP obowiązek powstaje z dniem protokołu odbioru lub uznania całej umowy za wykonaną.</p>
    ${S.opoznienie_dni > 0 ? `<label>Przyczyna opóźnienia (${S.opoznienie_dni} dni)<input id="owu-przyczyna" value="${esc(o.przyczyna_opoznienia || "")}"></label>` : ""}
    <h4 class="grupa-analizy">2. Kary umowne</h4>
    <div id="owu-kary">${(o.kary || []).map((k, i) => `<div class="pasek owu-kara" style="margin:4px 0"><input class="k-t" value="${esc(k.tytul || "")}" placeholder="z tytułu (np. zwłoka 12 dni)" style="flex:2">
      <input class="k-k" inputmode="decimal" value="${esc(k.kwota || "")}" placeholder="kwota zł" style="width:120px"><label class="wiersz" style="margin:0"><input type="checkbox" class="k-p" ${k.potracona ? "checked" : ""}> potrącona</label></div>`).join("")}</div>
    <div class="pasek"><button class="maly" data-ik="plus" onclick="$('#owu-kary').insertAdjacentHTML('beforeend', '<div class=&quot;pasek owu-kara&quot; style=&quot;margin:4px 0&quot;><input class=&quot;k-t&quot; placeholder=&quot;z tytułu&quot; style=&quot;flex:2&quot;><input class=&quot;k-k&quot; placeholder=&quot;kwota zł&quot; style=&quot;width:120px&quot;><label class=&quot;wiersz&quot; style=&quot;margin:0&quot;><input type=&quot;checkbox&quot; class=&quot;k-p&quot; checked> potrącona</label></div>')">Dodaj karę</button>
      ${S.opoznienie_dni > 0 && !(o.kary || []).length ? `<input id="owu-bezkar" value="${esc(o.bez_kar_uzasadnienie || "")}" placeholder="albo: dlaczego nie naliczono kar" style="flex:1">` : ""}</div>
    <h4 class="grupa-analizy">3. Ocena wykonania</h4>
    <div class="siatka"><label>Czy umowa została wykonana należycie?<select id="owu-nal"><option value="tak" ${S.nalezycie === "tak" ? "selected" : ""}>tak</option><option value="nie" ${S.nalezycie === "nie" ? "selected" : ""}>nie</option></select></label>
      <label>Jeśli nie – na czym polegały nieprawidłowości<input id="owu-nienal" value="${esc(o.opis_nienaleznego || "")}"></label>
      <label>Wynagrodzenie wypłacone (gdy inne niż z faktur) [zł]<input id="owu-wypl" inputmode="decimal" value="${esc(o.wyplacone || "")}" placeholder="${S.wyplacone_z_faktur}"></label>
      <label>Cena ofertowa (do raportu art. 446) [zł]<input id="owu-cena" inputmode="decimal" value="${esc(o.cena_ofertowa || "")}" placeholder="${S.wartosc_umowy_brutto}"></label>
      <label>Odstąpienie od umowy / wypowiedzenie (art. 446 ust. 1 pkt 4)<select id="owu-odst">${["", "odstąpienie od umowy w całości", "odstąpienie od umowy w części", "wypowiedzenie umowy w całości", "wypowiedzenie umowy w części"].map(x => `<option value="${x}" ${(o.odstapienie || "") === x ? "selected" : ""}>${x || "nie"}</option>`).join("")}</select></label></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszOWU()">Zapisz i przelicz</button></div>
    ${S.uwagi.length ? `<h4 class="grupa-analizy">Kontrola przed publikacją</h4>${S.uwagi.map(u => `<div class="alert-k ${u.waga === "krytyczna" ? "ostrzezenie" : ""}"><span class="znacznik ${u.waga === "krytyczna" ? "z-czerwony" : u.waga === "istotna" ? "z-do-analizy" : "z-odpuszczamy"}">${esc(u.waga)}</span> ${esc(u.opis)}</div>`).join("")}` : `<div class="ramka-uwaga" style="border-color:#16a34a">✓ Dane są spójne – można przepisać je do BZP.</div>`}
    ${S.raport_446.wymagany ? `<div class="ramka-uwaga"><b>Wymagany raport z realizacji zamówienia (art. 446 Pzp):</b> ${S.raport_446.powody.map(esc).join("; ")}.
      <a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${REAL_ID}/ogloszenie-wykonania/word?raport=1">Raport z realizacji (Word)</a></div>` : ""}
    <h4 class="grupa-analizy">4. Treść do formularza BZP</h4>
    <div class="tabela-okno"><table class="tabela"><tr><th>Pole</th><th>Treść</th><th></th></tr>${S.pola.map(([a, b], i) => `<tr><td><b>${esc(a)}</b></td><td style="white-space:pre-wrap">${esc(b || "–")}</td><td>${b ? kopia(b, i) : ""}</td></tr>`).join("")}</table></div>
    <div class="pasek"><a class="przycisk maly" data-ik="pobierz" href="/api/projekty/${REAL_ID}/ogloszenie-wykonania/word">Dane do ogłoszenia (Word)</a>
      <a class="przycisk maly" href="https://ezamowienia.gov.pl/" target="_blank" rel="noopener">Platforma e-Zamówienia ↗</a></div>
    <h4 class="grupa-analizy">5. Publikacja i dowód (art. 267 Pzp)</h4>
    <div class="siatka"><label>Numer ogłoszenia o wykonaniu umowy w BZP<input id="owu-pub-nr" value="${esc(pub.numer || "")}"></label>
      <label>Data zamieszczenia<input type="date" id="owu-pub-data" value="${esc(pub.data || "")}"></label></div>
    <div class="pasek"><button class="glowny" data-ik="zapisz" onclick="zapiszOWU(true)">Zapisz publikację i zamknij inwestycję</button>
      <label class="przycisk maly" data-ik="wgraj">Wgraj dowód (PDF)<input type="file" style="display:none" onchange="dowodOWU(this.files[0])"></label>
      ${pub.dowod ? `<span class="opis" style="margin:0">Dowód: ${esc(pub.dowod)}</span>` : ""}</div>
    <p class="opis" style="font-size:12px">Zakres pól odpowiada załącznikowi nr 7 do rozporządzenia w sprawie ogłoszeń zamieszczanych w BZP (sekcje IV–V) – porównaj z aktualnym formularzem. Wynagrodzenie podaje się po potrąceniu kar umownych.</p>`;
  wstawIkony($("#owu-tresc"));
}
async function zapiszOWU(zamknij) {
  const v = id => ($("#" + id) || {}).value ?? undefined;
  const kary = [...document.querySelectorAll(".owu-kara")].map(e => ({tytul: e.querySelector(".k-t").value, kwota: e.querySelector(".k-k").value, potracona: e.querySelector(".k-p").checked})).filter(k => k.kwota);
  const json = {data_wykonania: v("owu-data"), termin_pierwotny: v("owu-termin"), okres: v("owu-okres"), nr_ogloszenia: v("owu-nrz"), przyczyna_opoznienia: v("owu-przyczyna"),
    bez_kar_uzasadnienie: v("owu-bezkar"), nalezycie: v("owu-nal"), opis_nienaleznego: v("owu-nienal"), wyplacone: v("owu-wypl"), cena_ofertowa: v("owu-cena"), odstapienie: v("owu-odst"), kary,
    publikacja: {numer: v("owu-pub-nr"), data: v("owu-pub-data")}, zamknij: !!zamknij};
  Object.keys(json).forEach(k => json[k] === undefined && delete json[k]);
  const r = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/ogloszenie-wykonania`, {json})); if (r) { OWU = r; rysujOWU(); komunikat(zamknij && r.opublikowane ? "Zapisano publikację – inwestycja zamknięta." : "Zapisano."); }
}
async function dowodOWU(f) {
  if (!f) return; const fd = new FormData(); fd.append("plik", f);
  const r = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/ogloszenie-wykonania/dowod`, {body: fd, method: "POST"})); if (r) { OWU = r; rysujOWU(); komunikat("Dowód publikacji zapisany w dokumentach inwestycji."); }
}
// ---------- budowa: dziennik, zdjęcia, usterki
const DZIS_ISO = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
function sekcjeBudowy(R, RZR = "roboty") {
  const ZU = RZR !== "roboty";  // zamawiający – usługi / dostawy: bez dziennika budowy, zdjęcia jako dokumentacja, usterki jako reklamacje
  const r = R.realizacja, Z = r.zdjecia || [], D = (r.dziennik || []).slice().reverse(), U = r.usterki || [];
  const zdj = id => Z.find(z => z.id === id);
  const src = z => `/pobierz/${REAL_ID}/realizacja/zdjecia/${encodeURIComponent(z.miniatura || z.plik)}`;
  const pelne = z => `/pobierz/${REAL_ID}/realizacja/zdjecia/${encodeURIComponent(z.plik)}`;
  const otwarte = U.filter(u => u.status === "otwarta" || u.status === "w toku");
  const poTerminie = u => (u.status === "otwarta" || u.status === "w toku") && u.termin && u.termin < DZIS_ISO();
  const osoby = [...new Set([...(PRACOWNICY || []).map(x => x.imie), ...U.map(u => u.osoba).filter(Boolean)])];
  return `${ZU ? "" : `
  <div class="krok k-zolt"><div class="tytul"><span class="nr">${ik("kalendarz")}</span><h3>Raporty dzienne (dziennik pomocniczy)</h3>
    <span class="stan">${odm(D.length, "wpis", "wpisy", "wpisów")}</span></div><div class="tresc">
    <p class="opis">Raport dzienny: kliknij „Uzupełnij automatycznie”, a program wpisze pogodę, pracowników z ewidencji godzin, dostawy z kosztów
      i zdjęcia z tego dnia. Dopisz wykonane prace i zdarzenia, zapisz. Wydruk: przycisk „Pobierz raporty dzienne (Word)”.</p>
    <p class="opis"><b>To nie jest dziennik budowy</b> w rozumieniu art. 45 Prawa budowlanego (elektroniczny dziennik budowy EDB albo dziennik papierowy wydany przez organ) –
      to pomocniczy rejestr wykonawcy. Zmienione i usunięte raporty zostają w historii – podgląd i przywracanie w zakładce Archiwum.</p>
    <div class="siatka"><label>Data<input type="date" id="dz-data" value="${DZIS_ISO()}" max="${DZIS_ISO()}" onchange="wczytajWpis()"></label>
      <label style="grid-column: span 3">Pogoda<input id="dz-pogoda"></label></div>
    <div class="siatka"><label>Pracownicy na budowie<input id="dz-pracownicy"></label><label>Sprzęt<input id="dz-sprzet"></label></div>
    <label class="opis" style="display:block;margin:4px 0">Wykonane prace</label><textarea id="dz-prace"></textarea>
    <div class="siatka" style="margin-top:8px"><label>Dostawy / materiały<input id="dz-materialy"></label><label>Zdarzenia, polecenia, uwagi<input id="dz-uwagi"></label></div>
    <div id="dz-zdj" class="galeria mala"></div>
    <div class="pasek" style="margin-top:10px"><button class="zolty" data-ik="iskra" onclick="autoWpis()">Uzupełnij automatycznie</button>
      <button class="zielony" data-ik="zapisz" onclick="zapiszWpis()">Zapisz wpis</button>
      ${D.length ? `<a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${REAL_ID}/dziennik.docx">Pobierz raporty dzienne (Word)</a>` : ""}</div>
    ${D.length ? `<div class="tabela-okno" style="max-height:300px;margin-top:10px"><table class="tabela"><tr><th>Data</th><th>Pogoda</th><th>Pracownicy</th><th>Prace</th><th>Zdjęcia</th><th></th></tr>
      ${D.map(w => `<tr class="klik" onclick="$('#dz-data').value='${w.data}'; wczytajWpis(); $('#dz-data').scrollIntoView({behavior:'smooth',block:'center'})">
        <td><b>${dataPl(w.data)}</b></td><td>${esc(w.pogoda)}</td><td>${esc(w.pracownicy)}</td><td>${esc((w.prace || "").slice(0, 140))}</td>
        <td class="liczba">${(w.zdjecia || []).length}</td><td><button class="maly niebezp" data-ik="kosz" onclick="event.stopPropagation(); usunWpis('${w.data}')"></button></td></tr>`).join("")}</table></div>` : ""}
  </div></div>`}

  <div class="krok"><div class="tytul"><span class="nr">${ik("aparat")}</span><h3>${ZU ? (RZR === "dostawy" ? "Zdjęcia i dokumentacja dostaw (np. uszkodzenia, oznakowanie)" : "Zdjęcia i dokumentacja kontroli usług") : "Zdjęcia z budowy"}</h3><span class="stan">${odm(Z.length, "zdjęcie", "zdjęcia", "zdjęć")}</span></div><div class="tresc">
    <div class="siatka"><label>Data zdjęć<input type="date" id="zd-data" value="${DZIS_ISO()}"></label><label style="grid-column: span 2">Opis (opcjonalnie)<input id="zd-opis" placeholder="${ZU ? (RZR === "dostawy" ? "np. dostawa nr 2 – uszkodzone opakowanie" : "np. kontrola sprzątania – sala 12") : "np. elewacja płn. – klejenie styropianu"}"></label>
      <label>&nbsp;<span class="przycisk zielony-p" data-ik="aparat">Dodaj zdjęcia / zrób zdjęcie<input type="file" accept="image/*" multiple hidden onchange="wgrajZdjecia(this.files)"></span></label></div>
    <p class="opis">Na telefonie przycisk otwiera aparat albo galerię. ${ZU ? "Zdjęcia dokumentują odbiory i reklamacje – możesz je dołączyć do wezwania wykonawcy." : "Zdjęcia z danego dnia trafiają automatycznie do raportu dziennego."}</p>
    <div class="galeria">${Z.slice().reverse().map(z => `<figure><a href="${pelne(z)}" target="_blank" rel="noopener"><img src="${src(z)}" loading="lazy" alt=""></a>
      <figcaption>${dataPl(z.data)} · ${esc(z.opis || "")}<br><button class="maly" data-ik="przelacz" onclick="opisZdjecia('${z.id}')"></button>
      <button class="maly niebezp" data-ik="kosz" onclick="usunZdjecie('${z.id}')"></button></figcaption></figure>`).join("") || '<p class="pusto">Brak zdjęć.</p>'}</div>
  </div></div>

  <div class="krok k-czer"><div class="tytul"><span class="nr">${ik("alarm")}</span><h3>${ZU ? "Reklamacje, nieprawidłowości i zadania" : "Usterki i zadania"}</h3>
    <span class="stan">${otwarte.length} otwart${otwarte.length === 1 ? "a" : "ych"}${U.filter(poTerminie).length ? ` · ${U.filter(poTerminie).length} po terminie` : ""}</span></div><div class="tresc">
    <div class="siatka"><label>Rodzaj<select id="us-typ"><option value="usterka">${ZU ? "reklamacja / nieprawidłowość" : "usterka"}</option><option value="zadanie">zadanie</option></select></label>
      <label style="grid-column: span 2">Czego dotyczy<input id="us-tytul" placeholder="${ZU ? (RZR === "dostawy" ? "np. brak 5 krzeseł w dostawie nr 1" : "np. posiłki dostarczone po czasie 12.11") : "np. odspojona siatka przy oknie nr 3"}"></label>
      <label>Lokalizacja<input id="us-lok" placeholder="${ZU ? "np. budynek A, sala konferencyjna" : "np. elewacja płd., 2 piętro"}"></label></div>
    <div class="siatka"><label>Odpowiedzialny<input id="us-osoba" list="us-osoby"><datalist id="us-osoby">${osoby.map(o => `<option value="${esc(o)}">`).join("")}</datalist></label>
      <label>Termin<input type="date" id="us-termin"></label>
      <label>Zdjęcie<select id="us-zdj"><option value="">– brak –</option>${Z.slice().reverse().slice(0, 40).map(z => `<option value="${z.id}">${dataPl(z.data)} ${esc((z.opis || "").slice(0, 30))}</option>`).join("")}</select></label>
      <label>Opis (opcjonalnie)<input id="us-opis"></label></div>
    <div class="pasek"><button class="zielony" data-ik="plus" onclick="dodajUsterke()">Dodaj</button>
      ${U.length ? `<a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${REAL_ID}/usterki.docx?otwarte=1">Lista otwartych (Word)</a>
      <a class="przycisk dozw" data-ik="pobierz" href="/api/projekty/${REAL_ID}/usterki.docx">Pełna lista (Word)</a>` : ""}</div>
    ${U.length ? `<div class="tabela-okno" style="margin-top:10px"><table class="tabela"><tr><th>Rodzaj</th><th>Opis</th><th>Lokalizacja</th><th>Odpowiedzialny</th><th>Termin</th><th>Status</th><th></th></tr>
      ${U.slice().sort((a, b) => (["otwarta", "w toku", "usunięta", "zamknięta"].indexOf(a.status) - ["otwarta", "w toku", "usunięta", "zamknięta"].indexOf(b.status)) || String(a.termin || "9").localeCompare(String(b.termin || "9"))).map(u => {
        const z = zdj(u.zdjecie);
        return `<tr class="${poTerminie(u) ? "czerwone" : ""}"><td>${esc(u.typ)}</td><td><b>${esc(u.tytul)}</b>${u.opis ? `<br><small class="opis">${esc(u.opis)}</small>` : ""}
          ${z ? `<br><a href="${pelne(z)}" target="_blank" rel="noopener"><img src="${src(z)}" style="width:90px;border-radius:6px;margin-top:4px"></a>` : ""}</td>
          <td>${esc(u.lokalizacja || "")}</td><td>${esc(u.osoba || "")}</td><td>${u.termin ? dataPl(u.termin) : "–"}</td>
          <td><select onchange="statusUsterki('${u.id}', this.value)">${["otwarta", "w toku", "usunięta", "zamknięta"].map(s => `<option ${s === u.status ? "selected" : ""}>${s}</option>`).join("")}</select></td>
          <td><button class="maly niebezp" data-ik="kosz" onclick="statusUsterki('${u.id}', null, true)"></button></td></tr>`; }).join("")}</table></div>` : ""}
  </div></div>`;
}
function wczytajWpis() {
  const w = (REAL.realizacja.dziennik || []).find(x => x.data === $("#dz-data").value) || {};
  ["pogoda", "pracownicy", "prace", "materialy", "sprzet", "uwagi"].forEach(k => $("#dz-" + k).value = w[k] || "");
  pokazZdjeciaWpisu(w.zdjecia || (REAL.realizacja.zdjecia || []).filter(z => z.data === $("#dz-data").value).map(z => z.id));
}
let ZDJ_WPISU = [];
function pokazZdjeciaWpisu(ids) {
  ZDJ_WPISU = ids; const Z = REAL.realizacja.zdjecia || [];
  $("#dz-zdj").innerHTML = ids.map(id => Z.find(z => z.id === id)).filter(Boolean).map(z =>
    `<figure><img src="/pobierz/${REAL_ID}/realizacja/zdjecia/${encodeURIComponent(z.miniatura || z.plik)}"><figcaption>${esc(z.opis || "")}</figcaption></figure>`).join("");
}
async function autoWpis() {
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/dziennik/auto`, {json: {data: $("#dz-data").value}})); if (!w) return;
  ["pogoda", "pracownicy", "prace", "materialy"].forEach(k => { if (w[k] && !$("#dz-" + k).value) $("#dz-" + k).value = w[k]; });
  pokazZdjeciaWpisu(w.zdjecia || []);
  komunikat(w.uwaga || "Uzupełniono dane automatycznie – sprawdź i zapisz.", !!w.uwaga);
}
async function zapiszWpis() {
  const d = {data: $("#dz-data").value, zdjecia: ZDJ_WPISU};
  ["pogoda", "pracownicy", "prace", "materialy", "sprzet", "uwagi"].forEach(k => d[k] = $("#dz-" + k).value);
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/dziennik`, {json: d}))) { komunikat("Zapisano raport dzienny."); odswiezReal(); }
}
async function usunWpis(data) { if (confirm(`Usunąć raport dzienny z ${dataPl(data)}? Zostanie w historii (Archiwum) i można go przywrócić.`) && await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/dziennik`, {json: {data, usun: true}}))) odswiezReal(); }
async function wgrajZdjecia(files) {
  if (!files || !files.length) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f)); fd.append("data", $("#zd-data").value); fd.append("opis", $("#zd-opis").value);
  komunikat(`Wysyłam ${files.length} zdjęć…`);
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/zdjecia`, {method: "POST", body: fd}))) { komunikat("Dodano zdjęcia."); odswiezReal(); }
}
async function opisZdjecia(id) { const z = REAL.realizacja.zdjecia.find(x => x.id === id); const t = prompt("Opis zdjęcia:", z.opis || ""); if (t !== null && await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/zdjecia/zmien`, {json: {id, opis: t}}))) odswiezReal(); }
async function usunZdjecie(id) { if (confirm("Usunąć zdjęcie?") && await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/zdjecia/zmien`, {json: {id, usun: true}}))) odswiezReal(); }
async function dodajUsterke() {
  const d = {typ: $("#us-typ").value, tytul: $("#us-tytul").value, lokalizacja: $("#us-lok").value, osoba: $("#us-osoba").value,
    termin: $("#us-termin").value, zdjecie: $("#us-zdj").value, opis: $("#us-opis").value};
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/usterki`, {json: d}))) { komunikat("Dodano."); odswiezReal(); }
}
async function statusUsterki(id, status, usun) {
  if (usun && !confirm("Usunąć tę pozycję?")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/usterki`, {json: usun ? {id, usun: true} : {id, status}}))) odswiezReal();
}
function wstawUsterki() {
  const U = (REAL.realizacja.usterki || []).filter(u => u.typ === "usterka" && (u.status === "otwarta" || u.status === "w toku"));
  if (!U.length) return komunikat("Brak otwartych usterek na liście.");
  $("#pr-ust").value = U.map(u => u.tytul + (u.lokalizacja ? ` (${u.lokalizacja})` : "")).join("\n");
  const t = U.map(u => u.termin).filter(Boolean).sort().pop(); if (t && !$("#pr-term").value) $("#pr-term").value = dataPl(t);
}

function rysujHRF(hrf, vat, BF) {
  const E = hrf.etapy, D = hrf.dzialy;
  let narast = 0; const razem = D.reduce((a, d) => a + d.wartosc, 0) || 1;
  return `<div class="tabela-okno" style="max-height:none"><table class="tabela hrf"><tr><th>Dział kosztorysu</th>${BF ? "" : "<th>Wartość netto</th>"}
    ${E.map((e, k) => `<th style="min-width:170px"><input class="hrf-naz" data-k="${k}" value="${esc(e.nazwa)}" style="width:100%;font-weight:700">
      <div style="display:flex;gap:4px;margin-top:4px"><input type="date" class="hrf-od" data-k="${k}" value="${esc(e.od)}" style="width:50%;font-size:13px;padding:5px">
      <input type="date" class="hrf-do" data-k="${k}" value="${esc(e.do)}" style="width:50%;font-size:13px;padding:5px"></div>
      ${e.status === "odebrany" ? `<span class="znacznik z-startujemy" style="margin-top:4px">odebrany ${dataPl(e.data_odbioru)}</span>` : '<span class="znacznik z-odpuszczamy" style="margin-top:4px">planowany</span>'}</th>`).join("")}<th>Suma %</th></tr>
    ${D.map((d, i) => { const sm = E.reduce((a, e) => a + (+e.udzialy[i] || 0), 0); return `<tr><td>${esc(d.nazwa)}</td>${BF ? "" : `<td class="liczba">${zl(d.wartosc)}</td>`}
      ${E.map((e, k) => `<td><input class="hrf-u" data-k="${k}" data-i="${i}" type="number" min="0" max="100" step="0.01" value="${+e.udzialy[i] || 0}" style="width:90px" oninput="sumaHRF(${i})"> %</td>`).join("")}
      <td class="liczba" id="hrf-s${i}" style="font-weight:800;color:${Math.abs(sm - 100) < 0.01 ? "var(--zielony)" : "var(--czerwony)"}">${liczba(sm, 2)}%</td></tr>`; }).join("")}
    ${BF ? "" : `<tr><td><b>Netto etapu</b></td><td class="liczba"><b>${zl(razem)}</b></td>${E.map(e => `<td class="liczba"><b>${zl(e.wartosc)}</b></td>`).join("")}<td></td></tr>
    <tr><td>Brutto etapu</td><td></td>${E.map(e => `<td class="liczba">${zl(e.wartosc * (1 + vat))}</td>`).join("")}<td></td></tr>
    <tr><td>Narastająco</td><td></td>${E.map(e => { narast += e.wartosc; return `<td class="liczba">${liczba(narast / razem * 100, 1)}%</td>`; }).join("")}<td></td></tr>`}
  </table></div>`;
}
function sumaHRF(i) {
  const s = [...document.querySelectorAll(`.hrf-u[data-i="${i}"]`)].reduce((a, x) => a + (+x.value || 0), 0), el = $("#hrf-s" + i);
  el.textContent = liczba(s, 2) + "%"; el.style.color = Math.abs(s - 100) < 0.01 ? "var(--zielony)" : "var(--czerwony)";
}
async function statusBudowy(st) { await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/status`, {json: {status: st}})); ladujRealizacje(); }
async function wykonawcaPoNip() {
  const d = await pobierzNip($("#um-wyk-nip").value); if (!d) return;
  $("#um-wyk-nazwa").value = d.nazwa; $("#um-wyk-adres").value = d.adres; $("#um-wyk-nip").value = d.nip;
}
async function zapiszUmowe() {
  const d = {umowa_nr: $("#um-nr").value, data_umowy: $("#um-data").value,
    termin_zakonczenia: $("#um-termin").value, kierownik: $("#um-kier").value, inspektor: $("#um-insp").value, adres: $("#um-adres").value};
  if ($("#um-wart")) Object.assign(d, {wartosc_netto: $("#um-wart").value, vat: $("#um-vat").value});  // rola bez Finansów nie ma tych pól
  if ($("#um-wyk-nazwa")) Object.assign(d, {wykonawca_nazwa: $("#um-wyk-nazwa").value, wykonawca_nip: $("#um-wyk-nip").value, wykonawca_adres: $("#um-wyk-adres").value});
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/realizacja/umowa`, {json: d}))) { komunikat("Zapisano dane umowy."); odswiezReal(); }
}
async function wgrajBudowa(files) {
  if (!files || !files.length) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/realizacja/pliki`, {method: "POST", body: fd})); odswiezReal();
}
async function usunPlikBudowy(s) { if (!confirm("Usunąć ten dokument?")) return;
  await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/realizacja/pliki/usun`, {json: {sciezka: s}})); odswiezReal(); }
async function utworzHRF() {
  if (REAL.realizacja.hrf && !confirm("Utworzyć nową propozycję harmonogramu? Obecne procenty zostaną zastąpione.")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/hrf/utworz`, {json: {etapy: $("#hrf-n").value, start: $("#hrf-start").value, dlugosc: $("#hrf-dl").value}}))) odswiezReal();
}
async function zapiszHRF() {
  const E = REAL.realizacja.hrf.etapy.map((e, k) => ({nr: e.nr, nazwa: $(`.hrf-naz[data-k="${k}"]`).value, od: $(`.hrf-od[data-k="${k}"]`).value,
    do: $(`.hrf-do[data-k="${k}"]`).value, udzialy: [...document.querySelectorAll(`.hrf-u[data-k="${k}"]`)].map(x => x.value)}));
  const zle = REAL.realizacja.hrf.dzialy.filter((d, i) => Math.abs(E.reduce((a, e) => a + (+e.udzialy[i] || 0), 0) - 100) > 0.01);
  if (zle.length && !confirm(`Suma procentów nie wynosi 100% dla: ${zle.map(d => d.nazwa).join(", ")}. Zapisać mimo to?`)) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/hrf/zapisz`, {json: {etapy: E}}))) { komunikat("Zapisano harmonogram."); odswiezReal(); }
}
async function utworzProtokol() {
  const k = +$("#pr-etap").value, e = REAL.realizacja.hrf.etapy[k];
  if (e.status === "odebrany" && !confirm(`${e.nazwa || "Etap " + e.nr} ma już protokół. Utworzyć nowy?`)) return;
  const w = await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/protokol`, {json: {etap: k, data: $("#pr-data").value, miejsce: $("#pr-miejsce").value,
    komisja_zam: $("#pr-zam").value, komisja_wyk: $("#pr-wyk").value, wykonawca_id: $("#pr-wykonawca") ? $("#pr-wykonawca").value : "", usterki: $("#pr-ust").value, termin_usterek: $("#pr-term").value, uwagi: $("#pr-uwagi").value,
    zgodnosc_ilosc: ($("#pr-zil") || {}).value || "", zgodnosc_jakosc: ($("#pr-zjak") || {}).value || "", dokumenty_dostawy: ($("#pr-ddok") || {}).value || "",
    nalezycie: ($("#pr-nal") || {}).value || "", kary_okres: ($("#pr-kary") || {}).value || "", dolacz_materialy: $("#pr-mat") ? $("#pr-mat").checked : true}}));
  if (!w) return;
  location.href = w.url;
  await otworzRealizacje(REAL_ID);
  if (w.ostrzezenie) komunikat(w.ostrzezenie, true);  // ostatni etap przy nieodebranych wcześniejszych – protokół częściowy
  $("#pr-wynik").innerHTML = `<div class="karta"><b>Protokół gotowy</b> – ${w.koncowy ? "końcowy" : "częściowy"}, ${zl(w.netto)} netto / ${zl(w.brutto)} brutto.
    <div class="pasek" style="margin-top:10px"><button class="zielony" data-ik="faktura" onclick="fakturaZEtapu(${k}, ${w.netto})">Wpisz fakturę za ten ${REAL.projekt.rodzaj_zamowienia === "uslugi" && REAL.projekt.strona === "zamawiajacy" ? "okres" : REAL.projekt.rodzaj_zamowienia === "dostawy" && REAL.projekt.strona === "zamawiajacy" ? "dostawę" : "etap"}</button></div></div>`;
}
function fakturaZEtapu(k, netto) { $("#fv-etap").value = k; $("#fv-netto").value = netto; $("#fv-nr").focus(); $("#fv-nr").scrollIntoView({behavior: "smooth", block: "center"}); }
async function dodajFakture() {
  const d = {numer: $("#fv-nr").value, data: $("#fv-data").value, termin: $("#fv-termin").value, netto: $("#fv-netto").value, vat: $("#fv-vat").value,
    etap: $("#fv-etap").value === "" ? null : +$("#fv-etap").value, opis: $("#fv-opis").value, zaplacona: $("#fv-zapl").checked};
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/faktury`, {json: d}))) { komunikat("Dodano fakturę."); odswiezReal(); }
}
async function dodajKoszt() {
  const d = {data: $("#ko-data").value, kategoria: $("#ko-kat").value, netto: $("#ko-netto").value, dostawca: $("#ko-dost").value,
    dokument: $("#ko-dok").value, opis: $("#ko-opis").value, zaplacona: $("#ko-zapl").checked};
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/koszty`, {json: d}))) { komunikat("Dodano koszt."); odswiezReal(); }
}
async function zmienPoz(rodzaj, id, zm) {
  if (zm.usun && !confirm("Usunąć tę pozycję?")) return;
  if (await bezpiecznie(() => api(`/api/projekty/${REAL_ID}/${rodzaj}/zmien`, {json: {id, ...zm}}))) odswiezReal();
}

// ================================================================ KLIENCI (dane po NIP)
let KLIENCI = [], KL_EDYCJA = null;
async function pobierzNip(nip) {
  const n = String(nip || "").replace(/\D/g, "");
  if (n.length !== 10) { komunikat("Wpisz 10-cyfrowy NIP.", true); return null; }
  komunikat("Sprawdzam NIP w wykazie podatników VAT…");
  const r = await fetch("/api/nip/" + n, {headers: {"X-Agent": "1"}}); const d = await r.json().catch(() => ({}));
  if (!r.ok) { komunikat(d.blad || "Nie udało się pobrać danych.", true); return null; }
  komunikat(`Pobrano: ${d.nazwa}${d.z_pamieci ? " (z pamięci programu)" : ""}`);
  if (d.nazwa_osoby) komunikat(d.uwaga, true);  // JDG: w wykazie VAT tylko imię i nazwisko – nazwę firmy trzeba dopisać
  return d;
}
async function ladujKlientow() {
  KLIENCI = await bezpiecznie(() => api("/api/klienci")) || [];
  const k = KL_EDYCJA || {};
  $("#klienci").innerHTML = `<div class="karta bez-podgladu" style="margin-top:0"><h3>${ik(k.id ? "przelacz" : "plus")} ${k.id ? "Edycja: " + esc(k.nazwa) : "Nowy klient"}</h3>
    <div class="pasek"><input id="kl-nip" placeholder="NIP, np. 884-000-00-00" value="${esc(k.nip || "")}" style="width:220px"
      onkeydown="if (event.key === 'Enter') wypelnijKlienta()">
      <button class="zolty" data-ik="szukaj" onclick="wypelnijKlienta()">Pobierz dane po NIP</button>
      <span class="opis" style="margin:0" id="kl-status">${k.status_vat ? "Status VAT: <b>" + esc(k.status_vat) + "</b>" : ""}</span></div>
    <div class="siatka"><label style="grid-column: span 2">Nazwa<input id="kl-nazwa" value="${esc(k.nazwa || "")}"></label>
      <label style="grid-column: span 2">Adres<input id="kl-adres" value="${esc(k.adres || "")}"></label>
      <label>REGON<input id="kl-regon" value="${esc(k.regon || "")}"></label><label>KRS<input id="kl-krs" value="${esc(k.krs || "")}"></label>
      <label>Reprezentant / zarząd<input id="kl-reprezentant" value="${esc(k.reprezentant || "")}"></label>
      <label>Osoba kontaktowa<input id="kl-osoba" value="${esc(k.osoba || "")}"></label>
      <label>Telefon<input id="kl-telefon" value="${esc(k.telefon || "")}"></label><label>E-mail<input id="kl-email" value="${esc(k.email || "")}"></label>
      <label style="grid-column: span 2">Uwagi<input id="kl-uwagi" value="${esc(k.uwagi || "")}"></label></div>
    <div class="opis" id="kl-rachunki">${(k.rachunki || []).length ? "Rachunki z wykazu VAT: " + k.rachunki.map(esc).join(", ") : ""}</div>
    <div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="zapisz" onclick="zapiszKlienta()">Zapisz klienta</button>
      ${k.id ? `<button onclick="KL_EDYCJA=null; ladujKlientow()">Nowy klient</button>` : ""}</div></div>
  <div class="pasek" style="margin-top:14px"><input id="kl-szukaj" placeholder="Szukaj klienta (nazwa, NIP, miasto)…" style="min-width:300px" oninput="rysujKlientow()">
    <span class="licznik">${KLIENCI.length} klientów</span></div>
  <div class="tabela-okno" id="kl-tabela"></div>`;
  window.__klRach = k.rachunki || []; window.__klStatus = k.status_vat || "";
  rysujKlientow();
}
function rysujKlientow() {
  const q = ($("#kl-szukaj")?.value || "").toLowerCase();
  const L = KLIENCI.filter(k => !q || JSON.stringify(k).toLowerCase().includes(q));
  $("#kl-tabela").innerHTML = L.length ? `<table class="tabela"><tr><th>Nazwa</th><th>NIP</th><th>Adres</th><th>Kontakt</th><th>Status VAT</th><th></th></tr>
    ${L.map(k => `<tr class="klik" onclick="KL_EDYCJA=KLIENCI.find(x=>x.id==='${k.id}'); ladujKlientow(); window.scrollTo({top:0,behavior:'smooth'})">
      <td><b>${esc(k.nazwa)}</b>${k.reprezentant ? `<br><small class="opis">${esc(k.reprezentant)}</small>` : ""}</td><td style="white-space:nowrap">${esc(k.nip || "–")}</td>
      <td>${esc(k.adres || "")}</td><td>${esc([k.osoba, k.telefon, k.email].filter(Boolean).join(" · "))}</td>
      <td>${k.status_vat ? `<span class="znacznik ${/czynny/.test(k.status_vat) ? "z-startujemy" : "z-do-analizy"}">${esc(k.status_vat)}</span>` : "–"}</td>
      <td style="white-space:nowrap"><button class="maly" data-ik="przelacz" onclick="event.stopPropagation(); KL_EDYCJA=KLIENCI.find(x=>x.id==='${k.id}'); ladujKlientow(); window.scrollTo({top:0,behavior:'smooth'})">Edytuj</button>
        <button class="maly niebezp" data-ik="kosz" onclick="event.stopPropagation(); usunKlienta('${k.id}')">Usuń</button></td></tr>`).join("")}</table>`
    : '<p class="pusto" style="padding:14px">Brak klientów. Wpisz NIP powyżej i kliknij „Pobierz dane po NIP”.</p>';
}
async function wypelnijKlienta() {
  const d = await pobierzNip($("#kl-nip").value); if (!d) return;
  $("#kl-nip").value = d.nip; $("#kl-nazwa").value = d.nazwa; $("#kl-adres").value = d.adres; $("#kl-regon").value = d.regon; $("#kl-krs").value = d.krs;
  if (d.reprezentanci && d.reprezentanci.length && !$("#kl-reprezentant").value) $("#kl-reprezentant").value = d.reprezentanci.join(", ");
  window.__klRach = d.rachunki; window.__klStatus = d.status_vat;
  $("#kl-status").innerHTML = "Status VAT: <b>" + esc(d.status_vat) + "</b>";
  $("#kl-rachunki").textContent = d.rachunki.length ? "Rachunki z wykazu VAT: " + d.rachunki.join(", ") : "";
}
async function zapiszKlienta() {
  const d = {id: KL_EDYCJA && KL_EDYCJA.id, rachunki: window.__klRach, status_vat: window.__klStatus};
  ["nip", "nazwa", "adres", "regon", "krs", "reprezentant", "osoba", "telefon", "email", "uwagi"].forEach(k => d[k] = $("#kl-" + k).value);
  const w = await bezpiecznie(() => api("/api/klienci", {json: d})); if (!w) return;
  komunikat("Zapisano klienta."); KL_EDYCJA = null; ladujKlientow();
}
async function usunKlienta(id) { if (confirm("Usunąć klienta? Trafi do Archiwum – możesz go przywrócić w zakładce Archiwum.") && await bezpiecznie(() => api("/api/klienci/usun", {json: {id}}))) ladujKlientow(); }

// ================================================================ HURTOWNIE
async function ladujHurtownie() {
  await bezpiecznie(async () => {
    HURTOWNIE = await api("/api/hurtownie"); rysujHurtownie();
    const h = await api("/api/historia");
    $("#hist-tabela").innerHTML = "<tr><th>Data</th><th>Budowa</th><th>Etap</th><th>Rodzaj</th><th>Hurtownia</th><th>Sposób</th><th>Pozycji</th></tr>" +
      (h.map(x => `<tr><td>${esc(x.data)}</td><td>${esc(x.budowa)}</td><td>${x.etap}</td><td>${esc(x.typ)}</td><td>${esc(x.hurt)}</td><td>${esc(x.sposob)}</td><td class="liczba">${x.n}</td></tr>`).join("")
       || '<tr><td colspan="7" class="pusto">Brak wysłanych zamówień</td></tr>');
  });
}
function rysujHurtownie() {
  const pola = [["nazwa", "Nazwa"], ["email", "E-mail"], ["osoba", "Osoba kontaktowa"], ["kategorie", "Asortyment (słowa kluczowe)"], ["uwagi", "Uwagi"]];
  $("#h-tabela").innerHTML = "<tr>" + pola.map(p => `<th>${p[1]}</th>`).join("") + "<th></th></tr>" +
    HURTOWNIE.map((h, i) => "<tr>" + pola.map(([k]) => poziomU("hurtownie") >= 2 ? `<td><input style="width:100%" value="${esc(h[k] || "")}" oninput="HURTOWNIE[${i}]['${k}']=this.value"></td>` : `<td>${esc(h[k] || "")}</td>`).join("") +
      `<td>${poziomU("hurtownie") >= 2 ? `<button class="maly niebezp" data-ik="kosz" onclick="if (confirm('Usunąć hurtownię?')) { HURTOWNIE.splice(${i},1); zapiszHurtownie(); }">Usuń</button>` : ""}</td></tr>`).join("")
    + (HURTOWNIE.length ? "" : `<tr><td colspan="6" class="pusto">Brak hurtowni – kliknij „Dodaj hurtownię”, wpisz nazwę i e-mail, potem „Zapisz”.</td></tr>`);
}
function dodajHurtownie() { HURTOWNIE.push({nazwa: "", email: "", osoba: "", kategorie: "", uwagi: ""}); rysujHurtownie(); }
async function zapiszHurtownie() {
  const przed = HURTOWNIE.length;
  const w = await bezpiecznie(() => api("/api/hurtownie", {json: {hurtownie: HURTOWNIE}})); if (!w) return;
  HURTOWNIE = w; rysujHurtownie();
  komunikat(w.length < przed ? "Zapisano. Pominięto wiersze bez nazwy lub z błędnym e-mailem." : "Zapisano hurtownie.", w.length < przed);
}

// ================================================================ PRACOWNICY
let PRAC = {pracownicy: [], wpisy: []};
const dzis = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
// ================================================================ PŁACE (umowy, ZUS, podatek)
let PL = null, PL_LISTA = null;
function podzakladka(k) {
  document.querySelectorAll(".podzakladki button").forEach(b => { b.classList.toggle("akt", b.dataset.pz === k); b.classList.toggle("ukryj", !!b.dataset.mod && poziomU(b.dataset.mod) < 1); });
  if (k !== "rg" && poziomU(k === "umowy" ? "place" : "kadry") < 1) k = "rg";
  $("#prac-rg").classList.toggle("ukryj", k !== "rg"); $("#prac-umowy").classList.toggle("ukryj", k !== "umowy"); $("#prac-kadry").classList.toggle("ukryj", k !== "kadry");
  if (k === "umowy") ladujPlace();
  if (k === "kadry") ladujKadry();
}
// ================================================================ KADRY
let KADRY = null, KADRY_PRAC = null;
function statusTerminu(d) {
  const n = dniDo(d); if (n === null) return '<span class="znacznik z-odpuszczamy">bez terminu</span>';
  return n < 0 ? `<span class="znacznik z-czerwony">wygasł ${esc(dataPl(d))}</span>` : n <= 30 ? `<span class="znacznik z-do-analizy">wygasa za ${odm(n, "dzień", "dni", "dni")}</span>`
    : `<span class="znacznik z-startujemy">ważny do ${esc(dataPl(d))}</span>`;
}
async function ladujKadry() {
  KADRY = await bezpiecznie(() => api("/api/kadry")); if (!KADRY) return;
  const P = KADRY.pracownicy; if (!KADRY_PRAC && P.length) KADRY_PRAC = P[0].id;
  const p = P.find(x => x.id === KADRY_PRAC), k = (p && p.kadry) || {};
  const ile = x => { const docs = (x.kadry || {}).dokumenty || []; const zle = docs.filter(d => dniDo(d.wazne_do) !== null && dniDo(d.wazne_do) <= 30).length
    + (x.umowa && x.umowa.do && dniDo(x.umowa.do) <= 30 ? 1 : 0); return zle ? `<span class="znacznik z-do-analizy">${zle} do uwagi</span>` : ""; };
  $("#prac-kadry").innerHTML = `<p class="opis">Kartoteka kadrowa: dane pracownika, umowa, dokumenty z terminami ważności (badania lekarskie, BHP, uprawnienia, SEP, UDT…).
      Terminy kończące się w ciągu 30 dni pojawiają się na Pulpicie i w codziennym raporcie e-mail.</p>
    <div class="uklad"><aside><h3 style="margin:6px 0 0">Pracownicy</h3><ul>${P.map(x => `<li class="${x.id === KADRY_PRAC ? "akt" : ""}" onclick="KADRY_PRAC='${x.id}'; ladujKadry()">
      ${esc(x.imie)}<small>${esc(x.stanowisko || "")} ${ile(x)}</small></li>`).join("") || '<li class="pusto">Dodaj pracowników w podzakładce Roboczogodziny.</li>'}</ul></aside>
    <div>${p ? `<div class="karta" style="margin-top:0"><h3>${ik("ludzie")} ${esc(p.imie)}</h3>
      <div class="siatka"><label>Zatrudniony od<input type="date" id="kd-od" value="${esc(k.zatrudniony_od || "")}"></label>
        <label>Data ustania stosunku pracy<input type="date" id="kd-ustanie" value="${esc(k.data_ustania || "")}"></label>
        <label class="wybor-h" style="align-self:end"><span><input type="checkbox" id="kd-ria" ${k.ria ? "checked" : ""}> złożono raport ZUS RIA (zatrudnieni 1999–2018)</span></label>
        <label>E-mail<input id="kd-email" value="${esc(k.email || "")}"></label><label>Telefon<input id="kd-tel" value="${esc(p.telefon || "")}" placeholder="np. 600 100 200"></label>
        <label style="grid-column: span 2">Adres<input id="kd-adres" value="${esc(k.adres || "")}"></label>
        <label style="grid-column: span 2">Kontakt w razie wypadku<input id="kd-awaryjny" value="${esc(k.kontakt_awaryjny || "")}"></label>
        <label style="grid-column: 1 / -1">Uwagi<input id="kd-uwagi" value="${esc(k.uwagi || "")}"></label></div>
      <p class="opis">Umowa: ${p.umowa ? `<b>${esc({uop: "umowa o pracę", zlecenie: "umowa zlecenia", dzielo: "umowa o dzieło"}[p.umowa.typ] || p.umowa.typ)}</b>
        ${p.umowa.od ? "od " + esc(dataPl(p.umowa.od)) : ""} ${p.umowa.do ? " " + statusTerminu(p.umowa.do) : " · bezterminowa"} <small>(zmienisz w Płacach)</small>` : "brak – dodasz ją w Płacach"}</p>
      <button class="zielony" data-ik="zapisz" onclick="zapiszKartoteke('${p.id}')">Zapisz dane</button></div>
    <div class="karta"><h3>${ik("teczka")} Dokumenty i terminy</h3>
      ${(k.dokumenty || []).length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Dokument</th><th>Numer</th><th>Wydano</th><th>Ważny do</th><th>Status</th><th>Plik</th><th></th></tr>
        ${k.dokumenty.map(d => `<tr><td><b>${esc(d.typ)}</b>${d.uwagi ? `<br><small class="opis">${esc(d.uwagi)}</small>` : ""}</td><td>${esc(d.numer || "")}</td>
          <td>${d.wydano ? esc(dataPl(d.wydano)) : "–"}</td><td>${d.wazne_do ? esc(dataPl(d.wazne_do)) : "–"}</td><td>${statusTerminu(d.wazne_do)}</td>
          <td>${d.plik ? `<a class="dozw" href="/api/kadry/plik/${p.id}/${encodeURIComponent(d.plik)}">pobierz</a>` : "–"}</td>
          <td style="white-space:nowrap"><button class="maly" data-ik="przelacz" onclick="edytujDokKadr('${d.id}')">Edytuj</button>
            <button class="maly niebezp" data-ik="kosz" onclick="usunDokKadr('${p.id}','${d.id}')">Usuń</button></td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak dokumentów.</p>'}
      <h4 class="grupa-analizy" id="kdd-naglowek">Dodaj dokument</h4>
      <div class="siatka"><label>Rodzaj<select id="kdd-typ" onchange="kadryBhp()">${KADRY.typy.map(t => `<option>${esc(t)}</option>`).join("")}</select></label>
        <label class="ukryj" id="kdd-bhp-et" style="grid-column: span 2">Stanowisko – szkolenie okresowe BHP<select id="kdd-bhp" onchange="kadryBhp(true)"><option value="">– wybierz, program podpowie termin –</option>
          ${Object.entries(KADRY.grupy_bhp || {}).map(([k, t]) => `<option value="${k}">${esc(t)}</option>`).join("")}</select></label>
        <label>Numer<input id="kdd-numer"></label><label><span id="kdd-wydano-et">Data wydania</span><input type="date" id="kdd-wydano" onchange="kadryBhp(true)"></label>
        <label>Ważny do<input type="date" id="kdd-wazne"></label><label style="grid-column: span 2">Uwagi<input id="kdd-uwagi" placeholder="np. zakres uprawnień, kategoria"></label>
        <label>Skan (opcjonalnie)<input type="file" id="kdd-plik"></label></div>
      <div class="pasek"><button class="zielony" id="kdd-przycisk" data-ik="plus" onclick="dodajDokKadr('${p.id}')">Dodaj dokument</button>
        <button class="ukryj" id="kdd-anuluj" onclick="KADRY_DOK_ED = null; ladujKadry()">Anuluj edycję</button></div></div>` : ""}</div></div>
    <div class="karta" id="kadry-rodo"></div>`;
  window.__kadryDocs = (k.dokumenty || []);
  ladujRodo();
}
// ---------- RODO: dokumentacja pracownicza po okresie przechowywania (art. 94 pkt 9b KP) – lista „do trwałego usunięcia” (H1-10)
let RODO = null;
async function ladujRodo() {
  const el = $("#kadry-rodo"); if (!el) return;
  RODO = await api("/api/kadry/rodo").catch(() => null); if (!RODO) { el.remove(); return; }
  const wiersz = (x, akcja) => `<tr><td><b>${esc(x.imie)}</b>${x.pracownik_w_archiwum ? ' <small class="opis">(usunięty z listy)</small>' : ""}</td><td>${esc(x.typ)}${x.numer ? " " + esc(x.numer) : ""}</td>
    <td>${esc(String(x.usunieto || "").slice(0, 10) ? dataPl(String(x.usunieto).slice(0, 10)) : "–")}</td><td>${x.termin ? esc(dataPl(x.termin)) : "–"}<br><small class="opis">${esc(x.podstawa)}</small></td>
    <td>${akcja && RODO.moze_usuwac ? `<button class="maly niebezp" data-ik="kosz" onclick="rodoPytaj('${escA(x.pracownik)}','${escA(x.id)}','${escA(x.imie + " – " + x.typ)}')">Usuń trwale</button>` : ""}</td></tr>`;
  const tab = (L, akcja) => `<div class="tabela-okno"><table class="tabela"><tr><th>Pracownik</th><th>Dokument</th><th>Usunięto</th><th>Przechowywać do</th><th></th></tr>${L.map(x => wiersz(x, akcja)).join("")}</table></div>`;
  el.innerHTML = `<h3>${ik("teczka")} Do trwałego usunięcia (RODO) ${RODO.do_usuniecia.length ? `<span class="znacznik z-do-analizy">${RODO.do_usuniecia.length}</span>` : ""}</h3>
    <p class="opis">${esc(RODO.zasada)}</p>
    <div id="rodo-pytanie"></div>
    ${RODO.do_usuniecia.length ? tab(RODO.do_usuniecia, true) + (RODO.moze_usuwac ? "" : '<p class="opis">Trwale usuwa tylko administrator.</p>') : '<p class="pusto">Brak dokumentów po okresie przechowywania.</p>'}
    ${RODO.przechowywane.length ? `<details style="margin-top:8px"><summary>Dokumenty w archiwum kadr – okres przechowywania trwa (${RODO.przechowywane.length})</summary>${tab(RODO.przechowywane, false)}</details>` : ""}`;
  wstawIkony(el);
}
function rodoPytaj(prac, id, opis) {  // potwierdzenie w programie (nie okno przeglądarki): dokumentów nie da się przywrócić
  const el = $("#rodo-pytanie"); if (!el) return;
  el.innerHTML = `<div class="ramka-uwaga" role="alert"><b>Trwale usunąć: ${esc(opis)}?</b> Okres przechowywania minął. Dokument i skan zostaną usunięte bez możliwości przywrócenia.
    <div class="pasek" style="margin-top:8px"><button class="niebezp" id="rodo-tak" onclick="rodoUsun('${escA(prac)}','${escA(id)}')">Tak, usuń trwale</button>
    <button onclick="$('#rodo-pytanie').innerHTML=''">Anuluj</button></div></div>`;
  el.scrollIntoView({behavior: "smooth", block: "center"});
}
async function rodoUsun(prac, id) {
  const w = await bezpiecznie(() => api("/api/kadry/rodo/usun", {json: {pracownik: prac, id, potwierdzam: true}}));
  if (w) { komunikat(`Trwale usunięto dokumentów: ${w.usunieto}.`); ladujRodo(); }
}
async function zapiszKartoteke(id) {
  const d = {id, zatrudniony_od: $("#kd-od").value, data_ustania: $("#kd-ustanie").value, ria: $("#kd-ria").checked, email: $("#kd-email").value, telefon: $("#kd-tel").value, adres: $("#kd-adres").value, kontakt_awaryjny: $("#kd-awaryjny").value, uwagi: $("#kd-uwagi").value};
  if (await bezpiecznie(() => api("/api/kadry/pracownik", {json: d}))) { komunikat("Zapisano."); ladujKadry(); }
}
// H3-10: podpowiedź terminu szkolenia okresowego BHP (§ 15 rozporządzenia MGiP z 27.07.2004): data szkolenia + okres dla grupy stanowisk
function kadryBhp(licz) {
  const bhp = $("#kdd-typ") && $("#kdd-typ").value === "szkolenie BHP";
  $("#kdd-bhp-et") && $("#kdd-bhp-et").classList.toggle("ukryj", !bhp);
  if ($("#kdd-wydano-et")) $("#kdd-wydano-et").textContent = bhp ? "Data szkolenia" : "Data wydania";
  const g = bhp && $("#kdd-bhp").value, w = $("#kdd-wydano").value, mies = (KADRY.miesiace_bhp || {})[g];
  if (!licz || !g || !w || !mies) return;
  const d = new Date(w + "T12:00:00"), dzien = d.getDate(); d.setDate(1); d.setMonth(d.getMonth() + mies);
  d.setDate(Math.min(dzien, new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate()));
  $("#kdd-wazne").value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  komunikat(`Podpowiedź: następne szkolenie BHP do ${dataPl($("#kdd-wazne").value)} – możesz zmienić (pracodawca może ustalić częstsze szkolenia).`);
}
let KADRY_DOK_ED = null;
function edytujDokKadr(did) {
  const d = (window.__kadryDocs || []).find(x => x.id === did); if (!d) return;
  KADRY_DOK_ED = did;
  if (![...$("#kdd-typ").options].some(o => o.value === d.typ)) $("#kdd-typ").insertAdjacentHTML("beforeend", `<option>${esc(d.typ)}</option>`);
  $("#kdd-typ").value = d.typ; $("#kdd-numer").value = d.numer || ""; $("#kdd-wydano").value = d.wydano || ""; $("#kdd-wazne").value = d.wazne_do || ""; $("#kdd-uwagi").value = d.uwagi || "";
  if ($("#kdd-bhp")) $("#kdd-bhp").value = d.grupa_bhp || ""; kadryBhp();
  $("#kdd-naglowek").textContent = `Edytuj dokument: ${d.typ}`; $("#kdd-przycisk").lastChild.textContent = "Zapisz zmiany"; $("#kdd-anuluj").classList.remove("ukryj");
  $("#kdd-naglowek").scrollIntoView({behavior: "smooth", block: "center"});
}
async function dodajDokKadr(id) {
  const fd = new FormData(); fd.append("pracownik", id); if (KADRY_DOK_ED) fd.append("id", KADRY_DOK_ED);
  [["typ", "#kdd-typ"], ["numer", "#kdd-numer"], ["wydano", "#kdd-wydano"], ["wazne_do", "#kdd-wazne"], ["uwagi", "#kdd-uwagi"], ["grupa_bhp", "#kdd-bhp"]].forEach(([k, s]) => $(s) && fd.append(k, $(s).value));
  if ($("#kdd-plik").files[0]) fd.append("plik", $("#kdd-plik").files[0]);
  const w = await bezpiecznie(() => api("/api/kadry/dokument", {method: "POST", body: fd}));
  if (w) { komunikat(w.ostrzezenie || (KADRY_DOK_ED ? "Zapisano zmiany." : "Dodano dokument."), !!w.ostrzezenie); KADRY_DOK_ED = null; ladujKadry(); }
}
async function usunDokKadr(prac, id) { if (confirm("Usunąć dokument? Trafi do Archiwum – możesz go przywrócić.") && await bezpiecznie(() => api("/api/kadry/dokument/usun", {json: {pracownik: prac, id}}))) ladujKadry(); }

// ================================================================ PROFIL FIRMY
async function ladujFirme() {
  const F = await bezpiecznie(() => api("/api/firma")); if (!F) return;
  const D = F.dane, ed = poziomU("firma") >= 2;
  // zamawiający (gmina, urząd, szkoła, wspólnota): własne opisy; bez opisu firmy, certyfikatów, referencji i polisy – to dokumenty wykonawcy
  const ZAM = STRONA === "zamawiajacy" || window.EDYCJA === "zamawiajacy";
  const pole = (k, et, span) => `<label ${span ? 'style="grid-column: span 2"' : ""}>${et}<input id="fi-${k}" value="${esc(D[k] || "")}"></label>`;
  const lista = (rodzaj, tyt, wiersz, naglowki, formularz) => `<div class="karta"><h3>${tyt}</h3>
    ${F[rodzaj === "certyfikat" ? "certyfikaty" : rodzaj === "referencja" ? "referencje" : "polisy"].length ? `<div class="tabela-okno"><table class="tabela"><tr>${naglowki.map(n => `<th>${n}</th>`).join("")}<th>Plik</th><th></th></tr>
      ${F[rodzaj === "certyfikat" ? "certyfikaty" : rodzaj === "referencja" ? "referencje" : "polisy"].map(x => `<tr>${wiersz(x)}<td>${x.plik ? `<a class="dozw" href="/api/firma/plik/${encodeURIComponent(x.plik)}">pobierz</a>` : "–"}</td>
        <td style="white-space:nowrap">${ed ? `<button class="maly" data-ik="przelacz" onclick="edytujDokFirmy('${rodzaj}','${x.id}')">Edytuj</button>
          <button class="maly niebezp" data-ik="kosz" onclick="usunDokFirmy('${rodzaj}','${x.id}')">Usuń</button>` : ""}</td></tr>`).join("")}</table></div>` : '<p class="pusto">Brak.</p>'}
    ${ed ? `<div class="siatka" style="margin-top:10px">${formularz}<label>Plik (opcjonalnie)<input type="file" id="fd-${rodzaj}-plik"></label></div>
      <div class="pasek"><button class="zielony maly" id="fd-${rodzaj}-przycisk" data-ik="plus" onclick="dodajDokFirmy('${rodzaj}')">Dodaj</button>
        <button class="maly ukryj" id="fd-${rodzaj}-anuluj" onclick="FIRMA_ED['${rodzaj}'] = null; ladujFirme()">Anuluj edycję</button></div>` : ""}</div>`;
  window.__firmaDok = F;
  setTimeout(ladujUstawieniaKonta, 0);
  $("#firma").innerHTML = `${ZAM ? `<p class="opis">Dane zamawiającego trafiają do dokumentów zamówienia (SWZ albo zapytanie ofertowe, ogłoszenie), umowy, pism do wykonawców
      i protokołów: nazwa, adres, NIP i REGON, osoba reprezentująca (kierownik zamawiającego), dane kontaktowe, rachunek do wpłaty wadium i godziny pracy.
      Logo (herb) pojawia się w nagłówku generowanych dokumentów.</p>`
    : `<p class="opis">Dane firmy Twojego konta trafiają do ofert, umów, protokołów i zamówień. Opis firmy wykorzystuje AI przy ocenie przetargów.
      Certyfikaty, referencje i polisę dodasz jednym kliknięciem do kompletu dokumentów przetargowych (krok „Dokumenty wykonawcy”).</p>`}
    <div class="dwie"><div class="karta" style="margin-top:0"><h3>${ik("wizytowka")} ${ZAM ? "Dane zamawiającego" : "Dane podstawowe"}</h3>
      <div class="siatka">${pole("firma_nazwa", ZAM ? "Nazwa zamawiającego (np. Gmina Świdnica)" : "Nazwa firmy", true)}${pole("firma_nip", "NIP")}${pole("firma_regon", "REGON")}${pole("firma_adres", ZAM ? "Adres siedziby" : "Adres", true)}
        ${pole("firma_osoba", ZAM ? "Osoba reprezentująca (np. wójt, burmistrz, dyrektor)" : "Osoba reprezentująca")}${pole("firma_tel", "Telefon")}${pole("firma_email", "E-mail")}${pole("www", ZAM ? "Strona www / BIP" : "Strona www")}
        ${ZAM ? `${pole("rachunek", "Rachunek bankowy (wadium)")}${pole("godziny", "Godziny pracy (np. pon.–pt. 7:30–15:30)")}` : ""}</div>
      ${ZAM ? "" : `<label class="opis" style="display:block;margin:6px 0 4px">Opis firmy (zakres działalności, doświadczenie, obszar działania)</label>
      ${ed ? `<textarea id="fi-profil_firmy" style="min-height:110px" placeholder="${esc(F.podpowiedz_profil || "")}">${esc(D.profil_firmy || "")}</textarea>`
        : `<div class="karta" id="fi-profil_firmy-tekst" style="white-space:pre-wrap;margin:0">${esc(D.profil_firmy || "–")}</div>`}
      ${D.profil_firmy ? "" : '<p class="opis czerwone" id="fi-profil-brak" style="margin:4px 0 0">Opis firmy jest pusty – uzupełnij go, żeby AI mogła oceniać przetargi pod kątem Twojej firmy.</p>'}`}
      ${ed ? `<div class="pasek" style="margin-top:8px"><button class="zielony" data-ik="zapisz" onclick="zapiszFirme()">Zapisz</button>
        <button class="zolty" data-ik="szukaj" onclick="firmaPoNipProfil()">Uzupełnij po NIP</button></div>` : ""}</div>
    <div class="karta" style="margin-top:0"><h3>${ik("siatka")} Logo</h3>
      ${F.logo ? `<img src="/api/firma/logo.png?t=${Date.now()}" alt="logo" style="max-width:260px;max-height:130px;border:1px solid var(--linia);border-radius:10px;padding:8px;background:#fff">` : '<p class="pusto">Brak logo.</p>'}
      <p class="opis">${ZAM ? "Logo albo herb pojawia się w nagłówku dokumentów zamówienia (SWZ, umowa, pisma, protokoły) i w górnym pasku programu."
        : "Logo pojawia się w nagłówku generowanych dokumentów Word i w górnym pasku programu."}</p>
      ${ed ? `<label class="przycisk" data-ik="wgraj">${ZAM ? "Wgraj logo lub herb (PNG, JPG)" : "Wgraj logo (PNG, JPG)"}<input type="file" accept="image/*" hidden onchange="wgrajLogo(this.files[0])"></label>` : ""}</div></div>
    ${ZAM ? "" : lista("certyfikat", ik("protokol") + " Certyfikaty i uprawnienia firmy", x => `<td><b>${esc(x.nazwa)}</b></td><td>${esc(x.numer || "")}</td><td>${statusTerminu(x.wazny_do)}</td>`,
      ["Nazwa", "Numer", "Ważność"], `<label>Nazwa<input id="fd-certyfikat-nazwa" placeholder="np. ISO 9001, koncesja"></label><label>Numer<input id="fd-certyfikat-numer"></label><label>Ważny do<input type="date" id="fd-certyfikat-wazny_do"></label>`)}
    ${ZAM ? "" : lista("referencja", ik("trofeum") + " Referencje (zrealizowane roboty)", x => `<td><b>${esc(x.nazwa)}</b></td><td>${esc(x.zamawiajacy || "")}</td><td>${esc(x.wartosc || "")}</td><td>${esc(x.rok || "")}</td>`,
      ["Zadanie", "Zamawiający", "Wartość", "Rok"], `<label style="grid-column: span 2">Zadanie<input id="fd-referencja-nazwa"></label><label>Zamawiający<input id="fd-referencja-zamawiajacy"></label>
        <label>Wartość brutto<input id="fd-referencja-wartosc"></label><label>Rok<input id="fd-referencja-rok"></label>`)}
    ${ZAM ? "" : lista("polisa", ik("portfel") + " Polisa OC", x => `<td><b>${esc(x.nazwa)}</b></td><td>${esc(x.ubezpieczyciel || "")}</td><td>${esc(x.suma || "")}</td><td>${statusTerminu(x.wazny_do)}</td>`,
      ["Numer polisy", "Ubezpieczyciel", "Suma gwarancyjna", "Ważność"], `<label>Numer polisy<input id="fd-polisa-nazwa"></label><label>Ubezpieczyciel<input id="fd-polisa-ubezpieczyciel"></label>
        <label>Suma gwarancyjna<input id="fd-polisa-suma"></label><label>Ważna do (program przypomni 30 dni wcześniej)<input type="date" id="fd-polisa-wazny_do"></label>`)}
    <div class="karta" id="konto-ust"></div>`;
  // H3-09: polisy OC – ostrzeżenie 30 dni przed końcem ważności i przy polisie bez daty ważności (przypomnienie też na Pulpicie i w raporcie e-mail)
  if (!ZAM) {
    const pol = F.polisy || [], kon = pol.filter(x => dniDo(x.wazny_do) !== null && dniDo(x.wazny_do) <= 30), bez = pol.filter(x => !x.wazny_do);
    const msg = [...kon.map(x => `Polisa OC ${x.nazwa || ""}${x.ubezpieczyciel ? " (" + x.ubezpieczyciel + ")" : ""} ${dniDo(x.wazny_do) < 0 ? "wygasła " + dataPl(x.wazny_do) : "wygasa " + dataPl(x.wazny_do) + " – za " + odm(dniDo(x.wazny_do), "dzień", "dni", "dni")}: odnów ją i wgraj nową.`),
      ...bez.map(x => `Polisa OC ${x.nazwa || ""} nie ma daty ważności – wpisz ją, żeby program przypomniał o odnowieniu.`)];
    if (msg.length) $("#firma").insertAdjacentHTML("afterbegin", `<div class="ramka-uwaga" id="fi-polisy-uwaga" style="margin-top:0">${msg.map(esc).join("<br>")}</div>`);
  }
  const ne = $("#fi-firma_nip"); if (ne) { ne.addEventListener("input", sprawdzNipProfilu); sprawdzNipProfilu(); }
}
async function ladujUstawieniaKonta() {
  const U = await bezpiecznie(() => api("/api/konto/ustawienia")); if (!U || !$("#konto-ust")) return;
  const ZAM = STRONA === "zamawiajacy" || window.EDYCJA === "zamawiajacy";
  if (ZAM) U.pola = U.pola.filter(p => /^smtp_/.test(p.klucz)).map(p => p.klucz === "smtp_nadawca" ? {...p, etykieta: "Adres nadawcy (e-mail)"} : p);  // zamawiający: bez wyceny, wyszukiwania i oceny przetargów (ustawienia wykonawcy)
  $("#konto-ust").innerHTML = `<h3>${ik("suwaki")} Ustawienia mojego konta</h3>
    ${ZAM ? `<p class="opis">Poczta wychodząca (SMTP) Twojego konta – do wysyłki wiadomości e-mail z programu. Ustawienia tylko dla Twojego konta.</p>`
    : `<p class="opis">Parametry wyceny, automatyczne wyszukiwanie, raport e-mail i poczta do wysyłki zamówień – tylko dla Twojego konta.
      Obszar wyszukiwania i słowa kluczowe ustawiasz w zakładce Przetargi.</p>`}
    <div class="siatka">${U.pola.map(p => p.typ === "bool" ? `<label class="check"><input type="checkbox" id="ku-${p.klucz}" ${U.wartosci[p.klucz] ? "checked" : ""}> ${esc(p.etykieta)}</label>`
      : `<label>${esc(p.etykieta)}<input id="ku-${p.klucz}" ${p.typ === "secret" ? 'type="password" autocomplete="new-password"' : ""} value="${esc(U.wartosci[p.klucz] ?? "")}"></label>`).join("")}</div>
    <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszUstawieniaKonta()">Zapisz ustawienia konta</button>
      ${ZAM ? "" : `<button data-ik="mail" onclick="testRaportuKonta()">Wyślij raport e-mail teraz</button>`}</div>`;
  window.__polaKonta = U.pola;
}
async function zapiszUstawieniaKonta() {
  const d = {}; window.__polaKonta.forEach(p => { const el = $("#ku-" + p.klucz); d[p.klucz] = p.typ === "bool" ? el.checked : el.value; });
  if (await bezpiecznie(() => api("/api/konto/ustawienia", {json: d}))) { komunikat("Zapisano ustawienia konta."); ladujUstawieniaKonta(); }
}
async function testRaportuKonta() { sledz(await bezpiecznie(() => api("/api/powiadomienia/test", {json: {}})), w => komunikat(w.status === "ok" ? "Raport wysłany." : "Nie udało się wysłać – szczegóły w okienku zadania.", w.status !== "ok")); }
async function zapiszFirme() {
  const d = {}; ["firma_nazwa", "firma_nip", "firma_regon", "firma_adres", "firma_osoba", "firma_tel", "firma_email", "www", "profil_firmy", "rachunek", "godziny"].forEach(k => { if ($("#fi-" + k)) d[k] = $("#fi-" + k).value; });
  const w = await bezpiecznie(() => api("/api/firma", {json: d}));
  if (w) { komunikat(w.ostrzezenie ? "Zapisano, ale: " + w.ostrzezenie : STRONA === "zamawiajacy" || window.EDYCJA === "zamawiajacy" ? "Zapisano dane zamawiającego." : "Zapisano profil firmy.", !!w.ostrzezenie);
    await ladujFirme(); if (w.ostrzezenie) sprawdzNipProfilu(); }
}
// H3-08: suma kontrolna NIP (wagi 6-5-7-2-3-4-5-6-7, jak nip.py) – podpowiedź przy polu, zapis z ostrzeżeniem z serwera
function nipPoprawny(t) { const n = String(t || "").replace(/\D/g, ""); if (n.length !== 10 || n === "0000000000") return false;
  const s = [6, 5, 7, 2, 3, 4, 5, 6, 7].reduce((a, w, i) => a + w * +n[i], 0) % 11; return s !== 10 && s === +n[9]; }
function sprawdzNipProfilu() {
  const e = $("#fi-firma_nip"); if (!e) return; const v = e.value.trim(), zly = v && !nipPoprawny(v);
  e.setAttribute("aria-invalid", zly ? "true" : "false"); e.style.borderColor = zly ? "#dc2626" : "";
  let p = $("#fi-nip-blad"); if (!p) { p = document.createElement("small"); p.id = "fi-nip-blad"; p.className = "czerwone"; e.insertAdjacentElement("afterend", p); }
  p.textContent = zly ? "Nieprawidłowy NIP – sprawdź cyfry (suma kontrolna się nie zgadza)." : "";
}
async function firmaPoNipProfil() {
  const d = await pobierzNip($("#fi-firma_nip").value); if (!d) return;
  const obecna = $("#fi-firma_nazwa").value.trim();
  // jednoosobowa działalność: nie nadpisuj pełnej nazwy firmy samym imieniem i nazwiskiem z wykazu VAT
  if (!(d.nazwa_osoby && obecna && obecna.toLowerCase().includes(d.nazwa.toLowerCase()))) $("#fi-firma_nazwa").value = d.nazwa;
  $("#fi-firma_adres").value = d.adres; $("#fi-firma_regon").value = d.regon; $("#fi-firma_nip").value = d.nip;
  const pole = $("#fi-firma_nazwa");
  pole.classList.toggle("do-uzupelnienia", !!d.nazwa_osoby);
  let pod = document.getElementById("fi-nazwa-uwaga"); if (!pod) { pod = document.createElement("small"); pod.id = "fi-nazwa-uwaga"; pole.after(pod); }
  pod.className = "czerwone"; pod.textContent = d.nazwa_osoby ? "To imię i nazwisko z wykazu VAT – dopisz pełną nazwę firmy (np. „K.A. Jakub Górski”) i kliknij Zapisz." : "";
}
async function wgrajLogo(f) { if (!f) return; const fd = new FormData(); fd.append("logo", f);
  if (await bezpiecznie(() => api("/api/firma/logo", {method: "POST", body: fd}))) { komunikat("Wgrano logo."); ladujFirme(); pokazLogo(true); } }
const FIRMA_ED = {};
function edytujDokFirmy(rodzaj, id) {
  const F = window.__firmaDok || {}, x = (F[{certyfikat: "certyfikaty", referencja: "referencje", polisa: "polisy"}[rodzaj]] || []).find(y => y.id === id); if (!x) return;
  FIRMA_ED[rodzaj] = id;
  document.querySelectorAll(`input[id^="fd-${rodzaj}-"]`).forEach(el => { const k = el.id.split("-").slice(2).join("-"); if (k !== "plik") el.value = x[k] || ""; });
  const b = $(`#fd-${rodzaj}-przycisk`); b.lastChild.textContent = "Zapisz zmiany"; $(`#fd-${rodzaj}-anuluj`).classList.remove("ukryj");
  b.scrollIntoView({behavior: "smooth", block: "center"});
}
async function dodajDokFirmy(rodzaj) {
  const fd = new FormData(); fd.append("rodzaj", rodzaj); if (FIRMA_ED[rodzaj]) fd.append("id", FIRMA_ED[rodzaj]);
  document.querySelectorAll(`input[id^="fd-${rodzaj}-"], select[id^="fd-${rodzaj}-"]`).forEach(el => { const k = el.id.split("-").slice(2).join("-"); if (k === "plik") { if (el.files[0]) fd.append("plik", el.files[0]); } else fd.append(k, el.value); });
  const w = await bezpiecznie(() => api("/api/firma/dokument", {method: "POST", body: fd}));
  if (w) { komunikat(w.ostrzezenie || (FIRMA_ED[rodzaj] ? "Zapisano zmiany." : "Dodano."), !!w.ostrzezenie); FIRMA_ED[rodzaj] = null; ladujFirme(); }
}
async function usunDokFirmy(rodzaj, id) { if (confirm("Usunąć? Trafi do Archiwum – możesz go przywrócić.") && await bezpiecznie(() => api("/api/firma/dokument/usun", {json: {rodzaj, id}}))) ladujFirme(); }
async function pokazLogo(wgrane) {
  if (poziomU("firma") < 1 || (!wgrane && JA && JA.logo === false)) return;  // brak logo – bez zapytania kończącego się 404 w konsoli
  const r = await fetch("/api/firma/logo.png?t=" + Date.now(), {headers: {"X-Agent": "1"}}).catch(() => null);
  if (r && r.ok) { const u = URL.createObjectURL(await r.blob()); const a = $("#gp-awatar"); if (a) a.innerHTML = `<img src="${u}" alt="" class="logo-firmy">`; }
}
function rysujGornyPasek() {  // górny pasek (komputer): wyszukiwanie i użytkownik
  const el = $("#gp-uzytkownik"); if (!el) return;
  const nazwa = JA.imie || JA.login || "";
  el.innerHTML = `<span class="gp-awatar" id="gp-awatar">${esc((nazwa[0] || "?").toUpperCase())}</span><span class="gp-dane"><b>${esc(nazwa)}</b><small>${esc(JA.firma || (JA.rola === "admin" ? "administrator" : ""))}${JA.tylko_odczyt ? " · tylko podgląd" : ""}</small></span>`;
  if (JA.tylko_odczyt) el.title = "Rola „Tylko podgląd”: możesz przeglądać i pobierać pliki, ale nie zmieniasz danych.";
}
// wyszukiwarka w górnym pasku: przetargi (wykonawca, dostawca) albo lista projektów bieżącego trybu – filtr „Szukaj w projektach” (pr-szukaj)
function szukajGlobalnie(q) {
  q = (q || "").trim(); if (!q) return;
  let cel = {wykonawca: "przetargi", dostawca: "przetargi", zamawiajacy: "zam_projekty", inwestor: "inw_projekty", kosztorysant: "kos_projekty", dotacje: "dot_projekty",
    prawnik: "pr_sprawy", nieruchomosci: "nier"}[STRONA] || "przetargi";
  if (cel === "przetargi" && (!wolnoWidok("przetargi") || (window.EDYCJA && window.EDYCJA !== "pelna"))) cel = "projekty";  // rola bez Przetargów – szukaj w projektach
  if (!wolnoWidok(cel)) return komunikat("Twoja rola nie ma dostępu do modułu, w którym można szukać.", true);
  pokaz(cel);
  setTimeout(() => {
    const p = $("#p-szukaj");
    if (cel === "przetargi" && p) { p.value = q; rysujPrzetargi(); return; }
    if (TRYBY[cel] && $("#pr-szukaj")) { $("#pr-szukaj").value = q; filtrujProjekty(); return; }
    const sek = document.querySelector(".widok:not(.ukryj)"), f = sek && sek.querySelector("input[placeholder^='Szukaj'], input[type=search]");
    if (f) { f.value = q; f.dispatchEvent(new Event("input")); } else komunikat("W tym module nie ma wyszukiwania – przejdź do listy projektów.", true);
  }, 600);
}
// filtr listy projektów (lewa kolumna) – nazwa, daty, kwota, właściciel; bez zapytania do serwera
function filtrujProjekty() {
  const f = $("#pr-szukaj"), q = (f && f.value || "").trim().toLowerCase(), li = [...document.querySelectorAll("#lista-projektow > li[onclick]")];
  let ile = 0;
  li.forEach(x => { const ok = !q || x.textContent.toLowerCase().includes(q); x.classList.toggle("ukryj", !ok); ile += ok; });
  let b = $("#pr-szukaj-brak");
  if (q && !ile && li.length) { if (!b) { b = document.createElement("li"); b.id = "pr-szukaj-brak"; b.className = "opis"; $("#lista-projektow").appendChild(b); } b.textContent = `Brak projektów pasujących do „${q}”.`; }
  else if (b) b.remove();
}
async function zProfiluFirmy() {
  const F = await bezpiecznie(() => api("/api/firma")); if (!F) return;
  const pliki = [...F.certyfikaty, ...F.referencje, ...F.polisy].filter(x => x.plik);
  if (!pliki.length) return komunikat("W Profilu firmy nie ma dokumentów z plikami.", true);
  $("#z-profilu").innerHTML = `<div class="karta" style="margin:10px 0"><b>Dokumenty z Profilu firmy</b>
    <div class="wybor-h">${pliki.map(x => `<label><input type="checkbox" class="zp" value="${esc(x.plik)}" checked> ${esc(x.nazwa)}${x.wazny_do ? " " + statusTerminu(x.wazny_do) : ""}</label>`).join("")}</div>
    <button class="zielony maly" data-ik="plus" onclick="kopiujZProfilu()">Dodaj zaznaczone</button></div>`;
}
async function kopiujZProfilu() {
  const pliki = [...document.querySelectorAll(".zp:checked")].map(c => c.value);
  const w = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/wykonawca/z-profilu`, {json: {pliki}}));
  if (w) { komunikat(`Dodano ${w.skopiowano} dokumentów z profilu firmy.`); otworzProjekt(PROJEKT_ID); }
}
const OPCJE_UM = {pit2: "PIT-2 (kwota zmniejszająca 300 zł)", mlody: "do 26 lat – ulga dla młodych (PIT 0)", student: "student/uczeń do 26 lat (zlecenie – bez ZUS)",
  dojezdza: "dojeżdża z innej miejscowości (KUP 300 zł)", chorobowe: "dobrowolne chorobowe (zlecenie)", ppk: "uczestniczy w PPK",
  inne_zatrudnienie: "ma inny tytuł do ZUS z min. wynagrodzeniem (zlecenie – tylko zdrowotna)", autorskie: "prawa autorskie – KUP 50% (dzieło)"};
const OPCJE_DLA = {uop: ["pit2", "mlody", "dojezdza", "ppk"], zlecenie: ["pit2", "mlody", "student", "chorobowe", "ppk", "inne_zatrudnienie"], dzielo: ["autorskie"]};
async function ladujPlace() {
  PL = await bezpiecznie(() => api("/api/place")); if (!PL) return;
  const teraz = new Date(); const mies = `${teraz.getFullYear()}-${String(teraz.getMonth() + 1).padStart(2, "0")}`;
  $("#prac-umowy").innerHTML = `
  <p class="opis">Rozliczenie z narzutami: składki ZUS pracownika i pracodawcy, składka zdrowotna, koszty uzyskania przychodu, zaliczka na PIT,
    PPK, Fundusz Pracy i FGŚP, koszt całkowity pracodawcy. Umowę zlecenia program liczy z godzin z ewidencji × stawka.
    <b>Wyliczenia są pomocnicze – przed wypłatą zweryfikuj je z biurem rachunkowym.</b></p>
  <div class="karta" style="margin-top:0"><h3>${ik("dokument")} Umowy pracowników</h3>
    <div class="tabela-okno"><table class="tabela karty-mob"><tr><th>Pracownik</th><th>Umowa</th><th>Wynagrodzenie</th><th>Okres</th><th>Ustawienia podatkowe i ZUS</th><th></th></tr>
    ${PL.pracownicy.map(p => { const u = p.umowa; return `<tr><td class="km-tytul"><b>${esc(p.imie)}</b><br><small class="opis">${esc(p.stanowisko || "")}</small></td>
      <td data-l="Umowa">${u ? esc(PL.typy[u.typ]) : '<span class="opis">brak – tylko roboczogodziny</span>'}</td>
      <td data-l="Wynagrodzenie">${u ? (u.typ === "uop" ? zl(u.kwota) + " brutto / mies." : u.typ === "zlecenie" ? zl(u.kwota) + " brutto / h" : "kwota wpisywana w miesiącu") : "–"}</td>
      <td data-l="Okres">${u && (u.od || u.do) ? `${u.od ? dataPl(u.od) : "…"} – ${u.do ? dataPl(u.do) : "bezterminowo"}` : "–"}</td>
      <td data-l="Ustawienia">${u ? Object.entries(u.opcje || {}).filter(([, v]) => v).map(([k]) => `<span class="znacznik z-odpuszczamy" style="margin:2px">${esc(OPCJE_UM[k].split(" (")[0])}</span>`).join("") : ""}</td>
      <td><button class="maly" data-ik="przelacz" onclick="edytujUmowe('${p.id}')">${u ? "Zmień" : "Dodaj umowę"}</button></td></tr>`; }).join("") || '<tr><td colspan="6" class="pusto">Dodaj najpierw pracowników w zakładce Roboczogodziny.</td></tr>'}</table></div>
    <div id="um-edycja"></div>
  </div>
  <div class="karta"><h3>${ik("kalendarz")} Lista płac</h3>
    <div class="pasek"><label style="display:flex;gap:8px;align-items:center">Miesiąc <input type="month" id="pl-mies" value="${mies}" onchange="liczListe()"></label>
      <button class="glowny" data-ik="iskra" onclick="liczListe()">Przelicz</button>
      <button class="zielony" data-ik="zapisz" onclick="liczListe(true)">Zatwierdź listę płac</button>
      <a class="przycisk dozw" data-ik="pobierz" id="pl-xlsx" href="#">Pobierz Excel</a>
      ${PL.miesiace.length ? `<span class="opis" style="margin:0">Zatwierdzone: ${PL.miesiace.slice(0, 6).join(", ")}</span>` : ""}</div>
    <div id="pl-lista"></div>
  </div>
  <details class="karta"><summary><b>${ik("suwaki")} Parametry płacowe ${esc(PL.parametry.rok || "")}</b> – stawki ZUS, progi, kwoty (kliknij, aby zmienić)</summary>
    <p class="opis">Wartości domyślne na 2026 r. Przy zmianie przepisów (np. nowa płaca minimalna) popraw je tutaj. Stawkę wypadkową firmy sprawdź w informacji z ZUS.</p>
    <div class="siatka">${Object.entries(PL.opisy).map(([k, n]) => `<label>${esc(n)}<input id="pp-${k}" value="${esc(PL.parametry[k])}" ${PL.parametry_edycja ? "" : "disabled"}></label>`).join("")}</div>
    ${PL.parametry_edycja ? `<div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszParametry()">Zapisz parametry</button>
      <button data-ik="cofnij" onclick="zapiszParametry(true)">Przywróć wartości domyślne</button></div>` : '<p class="opis">Parametry płacowe są wspólne dla firmy – zmienia je administrator.</p>'}</details>`;
  $("#pl-xlsx").onclick = e => { e.preventDefault(); location.href = "/api/place/lista.xlsx?miesiac=" + $("#pl-mies").value; };
  liczListe();
}
function edytujUmowe(id) {
  const p = PL.pracownicy.find(x => x.id === id), u = p.umowa || {typ: "uop", kwota: "", opcje: {pit2: true}};
  $("#um-edycja").innerHTML = `<div class="korekta"><h3>Umowa: ${esc(p.imie)}</h3>
    <div class="siatka"><label>Rodzaj umowy<select id="ue-typ" onchange="opcjeUmowy()">${[["uop", "Umowa o pracę"], ["zlecenie", "Umowa zlecenia"], ["dzielo", "Umowa o dzieło"], ["brak", "Brak (tylko roboczogodziny)"]]
      .map(([v, n]) => `<option value="${v}" ${u.typ === v ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      <label id="ue-kw-l">Kwota<input id="ue-kwota" value="${esc(u.kwota)}"></label>
      <label>Etat (umowa o pracę)<select id="ue-etat">${["1", "0.75", "0.5", "0.25"].map(e => `<option ${String(u.etat || "1") === e ? "selected" : ""}>${e}</option>`).join("")}</select></label>
      <label>Od<input type="date" id="ue-od" value="${esc(u.od || "")}"></label><label>Do (puste = bezterminowo)<input type="date" id="ue-do" value="${esc(u.do || "")}"></label></div>
    <div class="wybor-h" id="ue-opcje"></div>
    <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszUmowe2('${id}')">Zapisz umowę</button><button onclick="$('#um-edycja').innerHTML=''">Anuluj</button></div></div>`;
  window.__opcjeUm = u.opcje || {}; opcjeUmowy();
  $("#um-edycja").scrollIntoView({behavior: "smooth", block: "center"});
}
function opcjeUmowy() {
  const t = $("#ue-typ").value, zazn = window.__opcjeUm || {};
  $("#ue-kw-l").firstChild.textContent = t === "uop" ? "Wynagrodzenie brutto miesięcznie [zł]" : t === "zlecenie" ? "Stawka brutto za godzinę [zł]" : "Kwota domyślna (dzieło wpisujesz w miesiącu)";
  $("#ue-opcje").innerHTML = (OPCJE_DLA[t] || []).map(k => `<label><input type="checkbox" class="ue-op" value="${k}" ${zazn[k] ? "checked" : ""}> ${esc(OPCJE_UM[k])}</label>`).join("");
}
async function zapiszUmowe2(id) {
  const opcje = {}; document.querySelectorAll(".ue-op").forEach(c => opcje[c.value] = c.checked);
  const d = {id, typ: $("#ue-typ").value, kwota: $("#ue-kwota").value || 0, etat: $("#ue-etat").value, od: $("#ue-od").value, do: $("#ue-do").value, opcje};
  if (await bezpiecznie(() => api("/api/place/umowa", {json: d}))) { komunikat("Zapisano umowę."); ladujPlace(); }
}
async function liczListe(zapisz, usun) {
  const brutto = {}; document.querySelectorAll(".pl-br").forEach(i => { if (i.dataset.zm === "1") brutto[i.dataset.id] = i.value; });
  if (usun && !confirm("Usunąć zatwierdzoną listę płac za ten miesiąc?")) return;
  PL_LISTA = await bezpiecznie(() => api("/api/place/lista", {json: {miesiac: $("#pl-mies").value, brutto, zapisz: !!zapisz, usun: !!usun}})); if (!PL_LISTA) return;
  if (zapisz) komunikat("Zatwierdzono listę płac – wyliczenia narastające (limity, progi) w kolejnych miesiącach uwzględnią ten miesiąc.");
  const L = PL_LISTA.pozycje, S = k => L.reduce((a, p) => a + (p.wynik[k] || 0), 0);
  $("#pl-lista").innerHTML = !L.length ? '<p class="pusto">Żaden pracownik nie ma umowy – dodaj umowy powyżej.</p>' : `
    <p class="opis">${PL_LISTA.zapisana ? `<b class="zielone">Lista zatwierdzona ${esc(PL_LISTA.zapisano)}</b> ·
      <a href="#" onclick="liczListe(false, true); return false">usuń zatwierdzenie</a>` : "Lista robocza – po sprawdzeniu kliknij „Zatwierdź listę płac”."}
      Kwotę brutto możesz zmienić w tabeli (np. premia, nadgodziny, dzieło) i kliknąć „Przelicz”.</p>
    <div class="tabela-okno"><table class="tabela karty-mob"><tr><th>Pracownik</th><th>Umowa</th><th>Brutto</th><th>Składki społ.</th><th>Zdrowotna</th><th>Zaliczka PIT</th><th>PPK</th>
      <th>Do wypłaty</th><th>ZUS pracodawcy</th><th>Koszt pracodawcy</th></tr>
      ${L.map(p => { const w = p.wynik; return `<tr><td class="km-tytul"><b>${esc(p.imie)}</b>${w.uwagi.length ? `<br><small class="czerwone">${esc(w.uwagi.join("; "))}</small>` : ""}</td>
        <td data-l="Umowa">${esc(PL.typy[w.typ])}${w.typ === "zlecenie" ? `<br><small class="opis">${liczba(p.godziny, 2)} h × ${zl(p.stawka)}</small>` : ""}</td>
        <td data-l="Brutto"><input class="pl-br" data-id="${p.id}" value="${p.brutto}" style="width:120px" inputmode="decimal" oninput="this.dataset.zm='1'"></td>
        <td class="liczba" data-l="Składki społeczne">${zl(w.spol_p)}</td><td class="liczba" data-l="Zdrowotna">${zl(w.zdrow)}</td>
        <td class="liczba" data-l="Zaliczka PIT">${zl(w.pit)}</td><td class="liczba" data-l="PPK">${zl(w.ppk_p)}</td>
        <td class="liczba km-wazne" data-l="Do wypłaty"><b class="zielone">${zl(w.netto)}</b></td><td class="liczba" data-l="ZUS pracodawcy">${zl(w.zus_firma + w.ppk_f)}</td>
        <td class="liczba km-wazne" data-l="Koszt pracodawcy"><b>${zl(w.koszt)}</b></td></tr>`; }).join("")}
      <tr class="km-razem"><td colspan="2"><b>RAZEM</b></td><td class="liczba" data-l="Brutto"><b>${zl(S("brutto"))}</b></td><td class="liczba" data-l="Składki społeczne">${zl(S("spol_p"))}</td><td class="liczba" data-l="Zdrowotna">${zl(S("zdrow"))}</td>
        <td class="liczba" data-l="Zaliczka PIT">${zl(S("pit"))}</td><td class="liczba" data-l="PPK">${zl(S("ppk_p"))}</td><td class="liczba" data-l="Do wypłaty"><b>${zl(S("netto"))}</b></td><td class="liczba" data-l="ZUS pracodawcy">${zl(S("zus_firma") + S("ppk_f"))}</td>
        <td class="liczba" data-l="Koszt pracodawcy"><b>${zl(S("koszt"))}</b></td></tr></table></div>
    <div class="kwoty"><div><span>Wypłaty netto</span><b>${zl(S("netto"))}</b></div>
      <div><span>Do ZUS (społ. + zdrow. + FP + FGŚP)</span><b>${zl(S("spol_p") + S("zus_firma") + S("zdrow"))}</b></div>
      <div><span>Zaliczki PIT do US</span><b>${zl(S("pit"))}</b></div>
      <div class="brutto"><span>Całkowity koszt pracodawcy</span><b>${zl(S("koszt"))}</b></div></div>`;
}
async function zapiszParametry(przywroc) {
  const d = {}; if (przywroc) { if (!confirm("Przywrócić domyślne parametry płacowe?")) return; d.przywroc = true; }
  else Object.keys(PL.opisy).forEach(k => d[k] = $("#pp-" + k).value);
  if (await bezpiecznie(() => api("/api/place/parametry", {json: d}))) { komunikat("Zapisano parametry."); ladujPlace(); }
}

async function ladujPracownikow() {
  const d = await bezpiecznie(() => api("/api/pracownicy")); if (!d) return;
  PRAC = d; rysujPracownikow();
  $("#g-prac").innerHTML = PRAC.pracownicy.map(p => `<option value="${esc(p.id)}">${esc(p.imie)}</option>`).join("") || "<option value=''>– dodaj pracownika –</option>";
  if (!$("#g-data").value) $("#g-data").value = dzis();
  stawkaPrac();
  api("/api/projekty").then(l => { l.sort((a, b) => (b.status_projektu === "realizacja") - (a.status_projektu === "realizacja"));
    $("#g-proj").innerHTML = '<option value="">– bez przypisania –</option>' + l.map(p => `<option value="${esc(p.id)}">${p.status_projektu === "realizacja" ? "● " : ""}${esc(p.nazwa)}</option>`).join(""); }).catch(() => {});
  if (!$("#r-od").value) miesiac(0); else ladujGodziny();
}
// stawki godzinowe i kwoty – tylko rola z dostępem do Płac albo Finansów (H1-03; np. kierownik budowy ich nie widzi)
const STAWKI = () => !PRAC || PRAC.stawki !== false;
function pokazStawki() {
  const st = STAWKI();
  for (const s of ["#np-stawka", "#g-stawka"]) { const e = $(s); if (e && e.closest("label")) e.closest("label").classList.toggle("ukryj", !st); }
  const k = $("#g-kwota"); if (k && k.parentElement) k.parentElement.classList.toggle("ukryj", !st);
}
function rysujPracownikow() {
  pokazStawki();
  const st = STAWKI();
  $("#pr-tabela").innerHTML = `<tr><th>Imię i nazwisko</th><th>Stanowisko</th>${st ? "<th>Stawka [zł/h]</th>" : ""}<th>Telefon</th><th></th></tr>` +
    PRAC.pracownicy.map((p, i) => `<tr><td><input style="width:100%" value="${esc(p.imie)}" oninput="PRAC.pracownicy[${i}].imie=this.value"></td>
      <td><input style="width:100%" value="${esc(p.stanowisko || "")}" oninput="PRAC.pracownicy[${i}].stanowisko=this.value"></td>
      ${st ? `<td><input type="number" step="0.01" min="0" style="width:100px" value="${esc(p.stawka)}" oninput="PRAC.pracownicy[${i}].stawka=this.value"></td>` : ""}
      <td><input style="width:100%" value="${esc(p.telefon || "")}" oninput="PRAC.pracownicy[${i}].telefon=this.value"></td>
      <td>${PRAC.wszystkie_konta ? `<small class="opis">${esc(p.wlasciciel || "")}</small> ` : ""}${p.id ? `<button class="maly niebezp" data-ik="kosz" title="Usuń pracownika (trafi do Archiwum razem z historią godzin)" onclick="usunPracownika('${escA(p.id)}', '${escA(p.imie)}')">Usuń</button>`
        : `<button class="maly" onclick="PRAC.pracownicy.splice(${i},1); rysujPracownikow()">×</button>`}</td></tr>`).join("");
  const z = $("#prac-zakres");
  if (z) z.innerHTML = `<p class="opis" style="margin:0 0 8px">Widzisz tylko <b>pracowników swojego konta</b> – inni użytkownicy mają własne listy pracowników, godzin, kadr i płac.
    ${WLASC() ? `<label style="display:inline-flex;gap:6px;align-items:center;margin-left:8px"><input type="checkbox" ${PRAC.wszystkie_konta ? "checked" : ""}
      onchange="zakresPracownikow(this.checked)"> pokaż pracowników wszystkich kont (właściciel programu)</label>` : ""}</p>`;
}
async function usunPracownika(id, imie) {
  if (!confirm(`Usunąć pracownika ${imie}? Trafi do Archiwum razem z historią roboczogodzin – możesz go stamtąd przywrócić.`)) return;
  if (await bezpiecznie(() => api("/api/pracownicy/usun", {json: {id}}))) { komunikat(`Usunięto pracownika: ${imie} (w Archiwum).`); ladujPracownikow(); }
}
async function zakresPracownikow(v) {
  await bezpiecznie(() => api("/api/pracownicy/zakres", {json: {wszystkie: v}}));
  JA.prac_wszystkie = v; ladujPracownikow(); if (!$("#prac-kadry").classList.contains("ukryj")) ladujKadry();
  if (!$("#prac-umowy").classList.contains("ukryj")) ladujPlace();
}
async function dodajPracownika() {
  const imie = $("#np-imie").value.trim(), stawka = STAWKI() ? $("#np-stawka").value : 0;
  if (!imie || stawka === "") return komunikat(STAWKI() ? "Podaj imię i nazwisko oraz stawkę godzinową." : "Podaj imię i nazwisko.", true);
  PRAC.pracownicy.push({imie, stawka, stanowisko: $("#np-stan").value, telefon: $("#np-tel").value});
  const d = await bezpiecznie(() => api("/api/pracownicy", {json: {pracownicy: PRAC.pracownicy}})); if (!d) return;
  ["#np-imie", "#np-stawka", "#np-stan", "#np-tel"].forEach(s => $(s).value = "");
  komunikat(`Dodano pracownika: ${imie}.`); ladujPracownikow();
}
async function zapiszPracownikow() {
  const d = await bezpiecznie(() => api("/api/pracownicy", {json: {pracownicy: PRAC.pracownicy}})); if (!d) return;
  komunikat("Zapisano pracowników. Zmiana stawki nie zmienia wcześniejszych wpisów."); ladujPracownikow();
}
function stawkaPrac() { const p = PRAC.pracownicy.find(x => x.id === $("#g-prac").value); $("#g-stawka").value = p ? p.stawka : ""; $("#g-stawka").readOnly = !ADMIN(); kwotaGodzin(); }
function kwotaGodzin() { const g = parseFloat(String($("#g-godz").value).replace(",", ".")), s = parseFloat(String($("#g-stawka").value).replace(",", ".")); $("#g-kwota").textContent = g > 0 && s >= 0 ? zl(g * s) : "–"; }
let EDYCJA_WPISU = null, WPISY = [];
async function dodajGodziny() {
  const d = {data: $("#g-data").value, pracownik: $("#g-prac").value, godziny: $("#g-godz").value, stawka: $("#g-stawka").value,
    projekt_id: $("#g-proj").value, projekt: $("#g-proj").selectedOptions[0]?.textContent.replace(/^● /, "") || "", opis: $("#g-opis").value};
  if (EDYCJA_WPISU) {
    const w = await bezpiecznie(() => api("/api/godziny/edytuj", {json: {id: EDYCJA_WPISU, ...d, projekt: d.projekt_id ? d.projekt : ""}}));
    if (w) { komunikat(w.ostrzezenie || `Zapisano zmiany: ${w.imie}, ${dataPl(w.data)}, ${liczba(w.godziny, 2)} h` + (w.kwota != null ? ` = ${zl(w.kwota)}` : ""), !!w.ostrzezenie); anulujEdycjeGodzin(); ladujGodziny(); }
    return;
  }
  const w = await bezpiecznie(() => api("/api/godziny", {json: d}));
  if (w) { komunikat(w.ostrzezenie ? `Dodano: ${w.imie}, ${liczba(w.godziny, 2)} h. ${w.ostrzezenie}` : `Dodano: ${w.imie}, ${liczba(w.godziny, 2)} h` + (w.kwota != null ? ` = ${zl(w.kwota)}` : ""), !!w.ostrzezenie); $("#g-opis").value = ""; ladujGodziny(); }
}
function edytujGodziny(id) {
  const w = WPISY.find(x => x.id === id); if (!w) return;
  EDYCJA_WPISU = id;
  $("#g-data").value = w.data; $("#g-prac").value = w.pracownik; $("#g-godz").value = w.godziny; $("#g-stawka").value = w.stawka;
  $("#g-proj").value = w.projekt_id || ""; $("#g-opis").value = w.opis || ""; kwotaGodzin();
  $("#g-naglowek").textContent = "Edytuj roboczogodziny"; $("#g-przycisk").lastChild.textContent = "Zapisz zmiany"; $("#g-anuluj").classList.remove("ukryj");
  $("#g-naglowek").scrollIntoView({behavior: "smooth", block: "center"});
}
function anulujEdycjeGodzin() {
  EDYCJA_WPISU = null; $("#g-naglowek").textContent = "Dodaj roboczogodziny"; $("#g-przycisk").lastChild.textContent = "Dodaj roboczogodziny";
  $("#g-anuluj").classList.add("ukryj"); $("#g-opis").value = "";
}
function miesiac(przes) {
  const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + przes);
  const od = new Date(d.getFullYear(), d.getMonth(), 1), dok = new Date(d.getFullYear(), d.getMonth() + 1, 0);
  const f = x => `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(x.getDate()).padStart(2, "0")}`;
  $("#r-od").value = f(od); $("#r-do").value = f(dok); ladujGodziny();
}
async function ladujGodziny() {
  const od = $("#r-od").value, dok = $("#r-do").value; if (!od || !dok) return;
  const r = await bezpiecznie(() => api(`/api/godziny?od=${od}&do=${dok}`)); if (!r) return;
  const st = r.stawki !== false;
  $("#r-podsum").innerHTML = r.podsumowanie.length ? `<div class="tabela-okno" style="max-width:760px"><table class="tabela">
    <tr><th>Pracownik</th><th>Dni</th><th>Godziny</th>${st ? "<th>Kwota wg stawek</th>" : ""}</tr>
    ${r.podsumowanie.map(x => `<tr><td>${esc(x.imie)}</td><td class="liczba">${x.dni}</td><td class="liczba">${liczba(x.godziny, 2)}</td>${st ? `<td class="liczba"><b>${zl(x.kwota)}</b></td>` : ""}</tr>`).join("")}
    <tr><td><b>RAZEM</b></td><td></td><td class="liczba"><b>${liczba(r.razem_godziny, 2)}</b></td>${st ? `<td class="liczba"><b>${zl(r.razem_kwota)}</b></td>` : ""}</tr></table></div>
    ${st ? '<p class="opis">Kwoty wg stawek godzinowych – bez przeliczeń składek ZUS i podatku.</p>' : ""}` : '<p class="pusto">Brak wpisów w tym okresie.</p>';
  WPISY = r.wpisy;
  $("#r-wpisy").innerHTML = `<tr><th>Data</th><th>Pracownik</th><th>Projekt</th><th>Godziny</th>${st ? "<th>Stawka</th><th>Kwota</th>" : ""}<th>Opis</th><th></th></tr>` +
    r.wpisy.map(w => `<tr><td>${dataPl(w.data)}</td><td>${esc(w.imie)}</td><td>${esc(w.projekt)}</td><td class="liczba">${liczba(w.godziny, 2)}</td>
      ${st ? `<td class="liczba">${zl(w.stawka)}</td><td class="liczba">${zl(w.kwota)}</td>` : ""}<td>${esc(w.opis)}</td>
      <td style="white-space:nowrap"><button class="maly" data-ik="przelacz" onclick="edytujGodziny('${escA(w.id)}')">Edytuj</button>
        <button class="maly niebezp" data-ik="kosz" onclick="usunGodziny('${escA(w.id)}')">Usuń</button></td></tr>`).join("");
}
async function usunGodziny(id) { if (!confirm("Usunąć ten wpis?")) return; await bezpiecznie(() => api("/api/godziny/usun", {json: {ids: [id]}})); ladujGodziny(); }
function eksportGodzin() { location.href = `/api/godziny/eksport?od=${$("#r-od").value}&do=${$("#r-do").value}`; }

// ================================================================ USTAWIENIA
let USTAW = null;
function otworzZrodla() { document.body.classList.add("pokaz-zrodla"); pokaz("przetargi"); setTimeout(() => { const d = $("#wiecej-opcji"); if (d) { d.open = true; d.scrollIntoView({behavior: "smooth"}); } }, 800); }
async function ladujUstawienia() {
  ladujUzytkownikow();
  USTAW = await bezpiecznie(() => api("/api/ustawienia")); if (!USTAW) return;
  const sekcje = {api_key: "Wyszukiwanie przetargów i AI", firma_nazwa: "Dane firmy i wycena", smtp_serwer: "Poczta (wysyłka zamówień przez SMTP)", powiadomienia: "Automatyzacja, powiadomienia, AI i ceny rynkowe"};
  const w = USTAW.wartosci, wyk = USTAW.wykonawca || {};
  $("#u-form").innerHTML = (ADMIN() ? `<div class="ramka-uwaga" style="margin:0 0 12px"><b>Źródła przetargów:</b> obserwowane strony urzędów, szpitali, uczelni i spółek oraz pełna lista pobranych przetargów –
      <a href="#" onclick="otworzZrodla(); return false">otwórz</a>.</div>` : "") + (wyk.nazwa ? `<div class="ramka-uwaga" style="margin:0 0 12px;background:var(--zielony-jasny);border-left-color:var(--zielony);color:#14532d">
    <b>Wykonawca w dokumentach:</b> ${esc(wyk.nazwa)}${wyk.adres ? ", " + esc(wyk.adres) : ""}${wyk.regon ? ", REGON " + esc(wyk.regon) : ""}
    ${wyk.z_wykazu ? " – dane z wykazu podatników VAT (po NIP)" : ""}</div>` : "") + USTAW.pola.map(p => {
    const v = w[p.klucz], id = "u-" + p.klucz, et = esc(p.etykieta.replace(/^(OFERTY|ZAMÓWIENIA) – /, ""));
    let pole;
    if (p.typ === "bool") pole = `<input type="checkbox" id="${id}" ${v ? "checked" : ""}>`;
    else if (p.typ.startsWith("wybor:")) pole = `<select id="${id}">${p.typ.slice(6).split("|").map(x => { const [w, n] = x.split("=");
      return `<option value="${esc(w)}" ${String(v) === w ? "selected" : ""}>${esc(n || w)}</option>`; }).join("")}</select>`;
    else if (p.typ === "text") pole = `<textarea id="${id}">${esc(v)}</textarea>`;
    else if (p.typ === "lines") pole = `<textarea id="${id}">${esc((v || []).join("\n"))}</textarea>`;
    else if (p.typ === "places") pole = `<textarea id="${id}" style="min-height:200px">${esc((v || []).map(x => x.join("; ")).join("\n"))}</textarea>`;
    else pole = `<input id="${id}" ${p.typ === "secret" ? 'type="password" autocomplete="new-password"' : ""} value="${esc(v ?? "")}" style="width:100%">`;
    const dop = p.klucz === "api_key" && USTAW.klucz_z_serwera ? '<br><small>Klucz jest też ustawiony na serwerze (ANTHROPIC_API_KEY) – to pole możesz zostawić puste.</small>' : "";
    return (sekcje[p.klucz] ? `<div class="sekcja">${sekcje[p.klucz]}</div>` : "") + `<div class="pole"><label for="${id}">${et}${dop}</label>${pole}</div>`;
  }).join("") + `<div class="pasek" style="margin-top:16px"><button class="zielony" data-ik="zapisz">Zapisz ustawienia</button>
    <button type="button" data-ik="mail" onclick="testRaportu()">Wyślij raport e-mail teraz</button>
    <button type="button" data-ik="wizytowka" onclick="firmaPoNip()">Uzupełnij dane firmy po NIP</button>
    <button type="button" class="zolty" data-ik="iskra" onclick="testAI()">Test połączenia z AI</button>
    <button type="button" data-ik="cofnij" onclick="przywrocUkryte()">Przywróć usunięte przetargi (${USTAW.ukrytych})</button></div>`;
}
async function ladujUzytkownikow() {
  if (!ADMIN()) { $("#u-uzytkownicy").innerHTML = ""; return; }
  const l = await bezpiecznie(() => api("/api/uzytkownicy")); if (!l) return;
  const role = JA.role || {};
  const rolePrzydzial = Object.entries(role).filter(([k]) => WLASC() || k !== "admin");  // „Administrator” nadaje tylko właściciel programu (H1-01)
  $("#u-uzytkownicy").innerHTML = `<h2>Użytkownicy strony</h2>
    <p class="opis">Osoby z tej listy logują się własnym loginem i hasłem na stronie. Nie mają dostępu do GitHuba ani Rendera,
      więc nie mogą zmieniać programu. ${WLASC() ? "Ty (konto z Rendera) jesteś właścicielem programu. Rola „Administrator” nadana przez Ciebie tworzy osobną firmę: jej administrator zarządza tylko swoją firmą (użytkownicy, projekty) – nie widzi innych firm."
        : "Jesteś administratorem swojej firmy: zakładasz i zmieniasz konta osób z Twojej firmy. Rolę „Administrator” nadaje tylko właściciel programu."}</p>
    <div id="reset-wynik"></div>
    <div class="tabela-okno" style="max-width:1040px"><table class="tabela"><tr><th>Login</th><th>Rola</th><th>Dostęp do modułów</th><th>Utworzono</th><th></th></tr>
    ${l.map(u => `<tr><td><b>${esc(u.login)}</b></td><td>${esc(role[u.rola] || u.rola + " (rola usunięta – działa jak „Tylko podgląd”)")}</td>
      <td>${u.modul ? `<span class="znacznik">tylko: ${esc(MODULY_KONTA[u.modul] || u.modul)}</span>` : "wszystkie"}</td><td>${esc(u.utworzono || "")}</td>
      <td style="white-space:nowrap">${!WLASC() && u.rola === "admin" ? '<span class="opis">administrator – zmienia właściciel programu</span>' : `<button class="maly" data-ik="przelacz" onclick="edytujUzytkownika('${escA(u.login)}','${escA(u.rola)}','${escA(u.modul || "")}')">Zmień rolę / moduł / hasło</button>
      <button class="maly" data-ik="odswiez" onclick="resetHasla('${escA(u.login)}')">Resetuj hasło</button>${u.haslo_tymczasowe ? ' <small class="opis">hasło tymczasowe</small>' : ""}
      <button class="maly niebezp" data-ik="kosz" onclick="usunUzytkownika('${escA(u.login)}')">Usuń</button>`}</td></tr>`).join("") || '<tr><td colspan="5" class="pusto">Brak dodatkowych użytkowników</td></tr>'}</table></div>
    <div class="karta" style="max-width:1040px"><h3>${ik("plus")} Dodaj lub zmień użytkownika</h3>
      <div class="siatka"><label>Login<input id="nu-login" autocomplete="off"></label>
        <label>Hasło (min. 10 znaków; puste = bez zmiany)<input id="nu-haslo" type="password" autocomplete="new-password"></label>
        <label>Rola<select id="nu-rola">${rolePrzydzial.map(([k, v]) => `<option value="${k}" ${k === "uzytkownik" ? "selected" : ""}>${esc(v)}</option>`).join("")}</select></label>
        <label>Dostęp do modułów<select id="nu-modul">${Object.entries(MODULY_KONTA).filter(([k]) => EDYCJA === "pelna" || !k || k === "gmina")
          .map(([k, v]) => `<option value="${k}">${k ? "tylko: " + esc(v) : esc(v)}</option>`).join("")}</select></label></div>
      <p class="opis">„Tylko: …” – osoba widzi wyłącznie wybrany moduł (np. tylko wspólnoty): bez wyboru rodzaju działalności, bez projektów i funkcji innych modułów.
        Rola nadal określa, co w tym module może oglądać i zmieniać.</p>
      <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszUzytkownika()">Zapisz użytkownika</button>
        <button type="button" data-ik="iskra" onclick="$('#nu-haslo').type='text'; $('#nu-haslo').value=Array.from(crypto.getRandomValues(new Uint8Array(12)),b=>'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'[b%55]).join('')">Wygeneruj hasło</button></div></div>
    <div class="karta" style="max-width:1040px" id="role-panel"></div>`;
  ladujRole();
}
let ROLE_DANE = null;
async function ladujRole(edytuj) {
  ROLE_DANE = await bezpiecznie(() => api("/api/role")); if (!ROLE_DANE) return;
  const R = ROLE_DANE, M = Object.entries(R.moduly), poz = ["–", "podgląd", "edycja"];
  const e = edytuj !== undefined ? (edytuj ? R.role[edytuj] : {nazwa: "", opis: "", uprawnienia: {}, ai: false, raporty: true}) : null;
  $("#role-panel").innerHTML = `<h3>${ik("ludzie")} Role i uprawnienia</h3>
    <p class="opis">Rola określa, co użytkownik widzi (podgląd) i co może zmieniać (edycja) w każdym module, czy może uruchamiać AI
      i pobierać raporty. Administrator ma zawsze pełny dostęp; tylko on trwale usuwa dane z Archiwum.</p>
    <div class="tabela-okno"><table class="tabela role-tab"><tr><th>Rola</th>${M.map(([, n]) => `<th title="${esc(n)}">${esc(n.split(/[:,(]/)[0])}</th>`).join("")}<th>AI</th><th>Raporty</th><th>Osób</th><th></th></tr>
      ${Object.entries(R.role).map(([k, r]) => `<tr><td><b>${esc(r.nazwa)}</b><br><small class="opis">${esc(r.opis || "")}</small></td>
        ${M.map(([m]) => `<td class="poz-${r.uprawnienia[m] || 0}">${poz[r.uprawnienia[m] || 0]}</td>`).join("")}
        <td>${r.ai ? "✔" : "–"}</td><td>${r.raporty !== false ? "✔" : "–"}</td><td class="liczba">${R.uzycie[k] || 0}</td>
        <td>${k === "admin" || !R.edycja ? "" : `<button class="maly" data-ik="przelacz" onclick="ladujRole('${escA(k)}')">Zmień</button>
          ${r.wbudowana ? "" : `<button class="maly niebezp" data-ik="kosz" aria-label="Usuń rolę ${esc(r.nazwa)}" title="Usuń rolę" onclick="usunRole('${escA(k)}')"></button>`}`}</td></tr>`).join("")}</table></div>
    ${R.edycja ? `<div class="pasek" style="margin-top:10px"><button data-ik="plus" onclick="ladujRole(null)">Nowa rola</button></div>`
      : '<p class="opis">Role są wspólne dla wszystkich firm w programie – zmienia je właściciel programu.</p>'}
    ${e ? `<div class="korekta" style="display:block"><h3>${edytuj ? "Zmiana roli: " + esc(e.nazwa) : "Nowa rola"}</h3>
      <div class="siatka"><label>Nazwa roli<input id="ro-nazwa" value="${esc(e.nazwa)}" ${edytuj && R.role[edytuj].wbudowana ? "" : ""}></label>
        <label style="grid-column: span 2">Opis<input id="ro-opis" value="${esc(e.opis || "")}"></label></div>
      <p class="opis">Pracownicy, Profil firmy, Klienci, Hurtownie i Archiwum są dostępne dla wszystkich ról (każde konto ma własne dane firmy), a Ustawienia
        oraz Użytkownicy i role – tylko dla administratora. Płace i Kadry ustaw zgodnie z opisem roli: rola bez Płac i bez Finansów nie widzi stawek pracowników ani kwot robocizny.</p>
      <div class="siatka">${M.map(([m, n]) => `<label>${esc(n)}<select class="ro-m" data-m="${m}" ${["pracownicy", "firma", "klienci", "hurtownie", "archiwum", "ustawienia", "uzytkownicy"].includes(m) ? "disabled" : ""}>${[0, 1, 2].map(v => `<option value="${v}" ${(e.uprawnienia[m] || 0) === v ? "selected" : ""}>${["brak dostępu", "podgląd", "podgląd i edycja"][v]}</option>`).join("")}</select></label>`).join("")}</div>
      <div class="wybor-h"><label><input type="checkbox" id="ro-ai" ${e.ai ? "checked" : ""}> może uruchamiać AI (oferty, analizy, dokumenty)</label>
        <label><input type="checkbox" id="ro-rap" ${e.raporty !== false ? "checked" : ""}> może pobierać pliki i raporty</label></div>
      <div class="pasek"><button class="zielony" data-ik="zapisz" onclick="zapiszRole(${edytuj ? `'${escA(edytuj)}'` : "null"})">Zapisz rolę</button>
        <button onclick="ladujRole()">Anuluj</button></div></div>` : ""}`;
}
async function zapiszRole(id) {
  const upr = {}; document.querySelectorAll(".ro-m").forEach(s => upr[s.dataset.m] = +s.value);
  const d = {id, nazwa: $("#ro-nazwa").value, opis: $("#ro-opis").value, uprawnienia: upr, ai: $("#ro-ai").checked, raporty: $("#ro-rap").checked};
  if (await bezpiecznie(() => api("/api/role", {json: d}))) { komunikat("Zapisano rolę."); JA = await api("/api/ja"); ladujUzytkownikow(); }
}
async function usunRole(id) { if (confirm("Usunąć rolę?") && await bezpiecznie(() => api("/api/role", {json: {id, usun: true}}))) ladujRole(); }
const MODULY_KONTA = {"": "Wszystkie moduły", wykonawca: "Dla wykonawcy (firma budowlana)", dostawca: "Dla dostawcy i usługodawcy", prawnik: "Dla prawnika",
  gmina: "Dla zamawiającego publicznego (gmina, urząd, szkoła)", wspolnota: "Dla wspólnot, spółdzielni i deweloperów", inwestor: "Dla inwestora (budowa domu)",
  kosztorysant: "Dla kosztorysanta", dotacje: "Dotacje i dofinansowania", nieruchomosci: "Nieruchomości"};
function edytujUzytkownika(login, rola, modul) { $("#nu-login").value = login; $("#nu-rola").value = rola; $("#nu-modul").value = modul || ""; $("#nu-haslo").value = ""; $("#nu-haslo").focus(); }
async function zapiszUzytkownika() {
  const d = {login: $("#nu-login").value, haslo: $("#nu-haslo").value, rola: $("#nu-rola").value, modul: $("#nu-modul").value};
  if (await bezpiecznie(() => api("/api/uzytkownicy", {json: d}))) {
    komunikat(`Zapisano użytkownika ${d.login}.` + (d.haslo ? " Przekaż mu login i hasło." : "")); ladujUzytkownikow(); }
}
// reset hasła (H1-07): hasło tymczasowe na 72 h, zmiana wymuszona przy logowaniu; bez SMTP – pokazane tutaj, do przekazania osobiście
async function resetHasla(login) {
  const el = $("#reset-wynik"); if (!el) return;
  el.innerHTML = `<div class="ramka-uwaga" role="alert"><b>Zresetować hasło użytkownika ${esc(login)}?</b> Dotychczasowe hasło przestanie działać, a osoba zostanie wylogowana.
    <div class="pasek" style="margin-top:8px"><button class="glowny maly" onclick="resetHaslaTak('${escA(login)}')">Tak, nadaj hasło tymczasowe</button>
    <button class="maly" onclick="$('#reset-wynik').innerHTML=''">Anuluj</button></div></div>`;
  el.scrollIntoView({behavior: "smooth", block: "center"});
}
async function resetHaslaTak(login) {
  const w = await bezpiecznie(() => api("/api/uzytkownicy/reset-hasla", {json: {login, wyslij: true}})); if (!w) return;
  $("#reset-wynik").innerHTML = w.wyslano ? `<div class="ramka-uwaga" style="background:var(--zielony-jasny);border-left-color:var(--zielony)">Hasło tymczasowe wysłano e-mailem na ${esc(w.login)} (ważne do ${esc(w.wazne_do)}).</div>`
    : `<div class="ramka-uwaga" style="background:var(--zielony-jasny);border-left-color:var(--zielony)"><b>Hasło tymczasowe dla ${esc(w.login)}:</b>
      <code id="haslo-tymcz" style="font-size:17px;user-select:all;margin:0 6px">${esc(w.haslo)}</code>
      <button class="maly" onclick="navigator.clipboard && navigator.clipboard.writeText($('#haslo-tymcz').textContent).then(() => komunikat('Skopiowano.'))">Kopiuj</button>
      <br><small>Ważne do ${esc(w.wazne_do)}. Przekaż je osobiście (poczta nie jest skonfigurowana) – po zalogowaniu program poprosi o ustawienie własnego hasła.
      Hasło nie zostanie pokazane ponownie.</small></div>`;
}
async function usunUzytkownika(login) {
  if (!confirm(`Usunąć użytkownika ${login}? Zostanie od razu wylogowany.`)) return;
  if (await bezpiecznie(() => api("/api/uzytkownicy/usun", {json: {login}}))) ladujUzytkownikow();
}
async function firmaPoNip() {
  const d = await pobierzNip($("#u-firma_nip")?.value); if (!d) return;
  const ust = (k, v) => { const el = $("#u-" + k); if (el && v) el.value = v; };
  ust("firma_nazwa", d.nazwa); ust("firma_adres", d.adres); ust("firma_nip", d.nip); ust("firma_regon", d.regon);
  komunikat("Uzupełniono dane firmy – sprawdź je i kliknij „Zapisz ustawienia”.");
}
async function testAI() {
  komunikat("Sprawdzam klucze API – kilka sekund…");
  const w = await bezpiecznie(() => api("/api/ai/test", {json: {}})); if (!w) return;
  const txt = w.wyniki.map(x => `${x.zrodlo}: klucz ${x.klucz} – ${x.ok === true ? "DZIAŁA" : x.ok === false ? "NIE DZIAŁA: " + x.opis : x.opis}`).join("\n\n");
  alert("Test połączenia z AI\n\n" + txt + (w.wyniki.some(x => x.ok) ? "\n\nProgram użyje działającego klucza." : "\n\nŻaden klucz nie działa – wklej aktualny klucz z console.anthropic.com w pole „Klucz API Claude” i zapisz.") +
    (w.pamiec ? `\n\nPamięć podręczna AI: ${w.pamiec.ok ? "DZIAŁA" : "NIE DZIAŁA"} – ${w.pamiec.opis}` + (w.pamiec.proby || []).map(p => `\n  ${p.tryb}: ${p.opis}`).join("") : ""));
}
async function testRaportu() {
  komunikat("Najpierw zapisz ustawienia, jeśli zmieniłeś adresy lub pocztę.");
  sledz(await bezpiecznie(() => api("/api/powiadomienia/test", {json: {}})), w => komunikat(w.status === "ok" ? "Raport wysłany." : "Nie udało się wysłać – szczegóły w okienku zadania.", w.status !== "ok"));
}
async function zapiszUstawienia(ev) {
  ev.preventDefault();
  const d = {};
  USTAW.pola.forEach(p => { const el = $("#u-" + p.klucz); d[p.klucz] = p.typ === "bool" ? el.checked : el.value; });
  if (await bezpiecznie(() => api("/api/ustawienia", {json: d}))) { komunikat("Zapisano ustawienia."); ladujUstawienia(); }
}
async function przywrocUkryte() { if (confirm("Przywrócić usunięte przetargi przy najbliższym wyszukiwaniu?"))
  if (await bezpiecznie(() => api("/api/ustawienia", {json: {przywroc_ukryte: true}}))) { komunikat("Przywrócono."); ladujUstawienia(); } }

// ================================================================ INSTRUKCJA INTERAKTYWNA I POMOC
const ROZDZIALY = [[1, "Co potrafi program", "pulpit"], [2, "Logowanie, pulpit, menu, role", "start"], [3, "Przetargi", "przetargi"],
  [4, "Projekt z przetargu – 6 kroków", "projekty"], [5, "Kosztorysowanie, własne projekty, umowy", "wlasne"], [6, "W realizacji", "realizacja"],
  [7, "Pracownicy, hurtownie, ustawienia konta", "pracownicy"], [8, "Konfiguracja konta: firma, poczta", "firma"],
  [9, "Moduł dla Zamawiającego", "zam_projekty"], [10, "Inwestor indywidualny – budowa domu", "inw_projekty"],
  [11, "Dotacje UE/KPO", "dot_szukaj"], [12, "Archiwum, karta projektu, profil firmy, kadry, pomoc", "pulpit"], [13, "Dobre praktyki i pytania", "pulpit"]];
const ROZDZIAL_WIDOKU = {zam_zapytania: 9, instrukcja: 1, start: 2, cel: 2, pulpit: 2, archiwum: 2, przetargi: 3, projekty: 4, wyniki: 4, wlasne: 5, kosztorys: 5, kos_projekty: 5,
  klienci: 5, realizacja: 6, dos_realizacja: 7, kalk_pracy: 7, zam_nowe: 8, zam_projekty: 8, zam_kosztorys: 8, zam_weryfikacja: 8, zam_dokumentacja: 8,
  zam_realizacja: 8, zam_oferty: 8, sprawozdanie: 8, olioc: 8, plan_zam: 8, plan_spr: 8, inw_projekty: 10, inw_budowa: 10, dot_szukaj: 11, dot_nadchodzace: 11,
  dot_wnioski: 11, dot_projekty: 11, dot_zapytania: 11, nier: 12, pr_sprawy: 13, pr_sporzadz: 13, pr_oferty: 13,
  firma: 14, hurtownie: 14, pracownicy: 14, kadry: 14, place: 14, konta: 15, ustawienia: 15};
let ROZDZIAL_DO_OTWARCIA = null, WIDOK_POPRZEDNI = "pulpit";
function otworzInstrukcje(cel) {
  ROZDZIAL_DO_OTWARCIA = null;
  const r = $("#instr-ramka"), id = cel ? (String(cel).startsWith("rozdzial-") ? String(cel) : "rozdzial-" + cel) : null;
  if (!r.getAttribute("src")) {
    r.addEventListener("load", () => { budujSpisInstrukcji(); if (id) setTimeout(() => przewinInstr(id), 150); }, {once: true});
    r.setAttribute("src", "/static/instrukcja.html");
  } else {
    if (!$("#instr-spis").dataset.gotowy) budujSpisInstrukcji();
    if (id) przewinInstr(id);
  }
}
function budujSpisInstrukcji() {
  const doc = $("#instr-ramka").contentDocument; if (!doc) return;
  const sek = [...doc.querySelectorAll("section[id^='rozdzial-']")]; if (!sek.length) return;
  $("#instr-spis").innerHTML = "<b>Spis treści</b>" + sek.map(s => {
    const h1 = s.querySelector("h1"), nr = s.id.split("-")[1], tyt = (h1 ? h1.textContent : "").replace(/^\s*\d+\s*/, "").trim();
    const pkt = [...s.querySelectorAll("h2[id]")];
    return `<details class="instr-poz" data-id="${s.id}"><summary><a href="#" onclick="przewinInstr('${s.id}'); return false">${nr}. ${esc(tyt)}</a></summary>
      ${pkt.map(h => `<a class="instr-pkt" data-id="${h.id}" href="#" onclick="przewinInstr('${h.id}'); return false">${esc(h.textContent.trim())}</a>`).join("")}</details>`;
  }).join("");
  $("#instr-spis").dataset.gotowy = "1";
}
function przewinInstr(id) {
  const r = $("#instr-ramka"), doc = r.contentDocument, el = doc && doc.getElementById(id);
  if (!el) return;
  const okno = r.contentWindow;  // przewijamy tylko instrukcję (bez przesuwania całej strony)
  okno.scrollTo({top: el.getBoundingClientRect().top + okno.scrollY - 10, behavior: "smooth"});
  el.classList.add("podswietl"); setTimeout(() => el.classList.remove("podswietl"), 2500);
  const rozdz = id.split("-").slice(0, 2).join("-");
  document.querySelectorAll("#instr-spis .instr-poz").forEach(d => { d.open = d.dataset.id === rozdz; d.classList.toggle("akt", d.dataset.id === rozdz); });
  document.querySelectorAll("#instr-spis .instr-pkt").forEach(a => a.classList.toggle("akt", a.dataset.id === id));
  if (window.innerWidth <= 900) r.scrollIntoView({behavior: "smooth", block: "start"});
}
function instrukcjaDlaWidoku() { ROZDZIAL_DO_OTWARCIA = (typeof MZ === "function" && MZ().rozdzial_instrukcji && /^zam_/.test(WIDOK)) ? MZ().rozdzial_instrukcji : (ROZDZIAL_WIDOKU[WIDOK] || 1); przelaczPomoc(true); pokaz("instrukcja"); }

function przelaczPomoc(zamknij) {
  const p = $("#pomoc-panel"); p.classList.toggle("ukryj", zamknij === true ? true : !p.classList.contains("ukryj"));
  if (!p.classList.contains("ukryj")) {
    const podp = {realizacja: ["Jak dodać nową fakturę?", "Jak przygotować wniosek o przedłużenie terminu z powodu pogody?"], przetargi: ["Jak ustawić obszar wyszukiwania?", "Co daje pełna analiza z dokumentami?"],
      projekty: ["Jak przygotować ofertę?", "Jak zmienić cenę oferty?"], pracownicy: ["Jak dodać pracownika?", "Jak rozliczyć godziny w miesiącu?"]}[WIDOK]
      || ["Jak dodać nową fakturę?", "Jak dodać użytkownika?", "Jak przywrócić usunięty projekt?"];
    $("#pomoc-podp").innerHTML = podp.map(q => `<button class="maly" onclick="$('#pomoc-pyt').value=this.textContent; zapytajPomoc()">${esc(q)}</button>`).join("");
    $("#pomoc-pyt").focus();
  }
}
const POMOC_HIST = [];
async function zapytajPomoc() {
  const q = $("#pomoc-pyt").value.trim(); if (!q) return;
  $("#pomoc-pyt").value = ""; const cz = $("#pomoc-czat");
  cz.insertAdjacentHTML("beforeend", `<div class="czat-p">${esc(q)}</div><div class="czat-o" id="pomoc-czeka">…</div>`); cz.scrollTop = cz.scrollHeight;
  const el = $("#pomoc-czeka"); el.removeAttribute("id");
  let r, d;
  try { r = await fetch("/api/pomoc", {method: "POST", headers: {"X-Agent": "1", "Content-Type": "application/json"}, body: JSON.stringify({pytanie: q, widok: WIDOK, historia: POMOC_HIST})});
    d = await r.json().catch(() => ({})); }
  catch (e) { el.textContent = "Brak połączenia z serwerem – sprawdź internet i zapytaj ponownie."; return; }
  if (!r.ok) { el.textContent = d.blad || "Nie udało się uzyskać odpowiedzi."; return; }
  // „Otwórz moduł” tylko dla modułu, który ten użytkownik ma w menu (edycja programu, konto ograniczone do modułu, rola)
  const wMenu = w => [...document.querySelectorAll(`#nav button[data-w="${w}"]:not(.ukryj)`)].some(x => !x.dataset.strona || x.dataset.strona === STRONA) && wolnoWidok(w);
  if (d.przejdz && !wMenu(d.przejdz)) d.przejdz = null;
  POMOC_HIST.push(q, d.odpowiedz);
  el.innerHTML = esc(d.odpowiedz).replace(/\n/g, "<br>").replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    + (d.przejdz ? `<div class="pasek" style="margin-top:8px"><button class="maly glowny" onclick="ROZDZIAL_DO_OTWARCIA = ROZDZIAL_WIDOKU['${d.przejdz}'] || 1; przelaczPomoc(true); pokaz('instrukcja')">Pokaż w instrukcji →</button>
      <button class="maly" onclick="pokaz('${d.przejdz}'); przelaczPomoc(true)">Otwórz moduł: ${esc(d.przejdz_nazwa)}</button></div>` : "");
  cz.scrollTop = cz.scrollHeight;
}

// ---------- zakres list administratora: wszystkie konta / moje / jedno konto
function selectZakresu() {
  if (!WLASC() || JA.jako) return "";  // zakres „wszystkie konta” – tylko właściciel programu (H1-01)
  return `<label class="zakres-admin">Konta: <select onchange="ustawZakresAdmina(this.value)">
    <option value="wszystkie" ${JA.admin_zakres === "wszystkie" ? "selected" : ""}>wszystkie konta</option>
    <option value="moje" ${JA.admin_zakres === "moje" ? "selected" : ""}>tylko moje</option>
    ${(JA.konta || []).filter(k => k !== JA.login).map(k => `<option value="${esc(k)}" ${JA.admin_zakres === k ? "selected" : ""}>${esc(k)}</option>`).join("")}</select></label>`;
}
async function ustawZakresAdmina(z) {
  if (!(await bezpiecznie(() => api("/api/admin/zakres", {json: {zakres: z}})))) return;
  JA.admin_zakres = z; wstawZakresAdmina();
  if (TRYBY[WIDOK]) ladujProjekty(); else if (["realizacja", "zam_realizacja", "inw_budowa"].includes(WIDOK)) ladujRealizacje(); else if (WIDOK === "przetargi") ladujPrzetargi();
}
function wstawZakresAdmina() {
  document.querySelectorAll(".zakres-admin-miejsce").forEach(el => el.innerHTML = selectZakresu());
}

// ================================================================ KONTA I AKTYWNOŚĆ (administrator)
let KONTO_FILTR = "";
async function ladujKonta() {
  const K = await bezpiecznie(() => api("/api/konta")); if (!K) return;
  const ZU = await api("/api/zuzycie-ai").catch(() => null);
  if (ZU) K.kurs_usd = ZU.kurs_usd;
  const sumaAi = ZU ? ZU.konta.reduce((a, x) => a + x.biezacy_zl, 0) : 0, sumaPop = ZU ? ZU.konta.reduce((a, x) => a + x.poprzedni_zl, 0) : 0;
  const A = await bezpiecznie(() => api("/api/aktywnosc?limit=400" + (KONTO_FILTR ? "&konto=" + encodeURIComponent(KONTO_FILTR) : ""))) || [];
  $("#konta").innerHTML = `<p class="opis"><b>Skąd pusta aktywność?</b> Dziennik zapisuje działania od chwili wgrania tej funkcji: logowanie, otwarcie programu i projektów,
      tworzenie i zmiany (oferty, dokumenty, faktury, wpisy, płace), pobieranie plików. Samo przeglądanie list nie tworzy wpisów, ale zmienia kolumnę
      „Ostatnio w programie”. Konto bez wpisów nie korzystało z programu od tego czasu.</p>
    <p class="opis">Każde konto to osobna firma: własny profil firmy, przetargi, projekty, klienci, hurtownie, pracownicy, kadry i płace.
      Inne konta nie mają dostępu do Twoich danych. ${JA.admin_firmy ? "Jako administrator konta widzisz tylko konta swojej firmy. " : ""}${WLASC() ? `Ty możesz otworzyć każde konto (przycisk <b>Otwórz konto</b>) i zobaczyć je tak, jak widzi je użytkownik –
      u góry pojawi się pasek z przyciskiem powrotu na Twoje konto.` : "Otwierać konta innych użytkowników może tylko właściciel programu (konto z instalacji)."}</p>
    ${ZU ? `<div class="kwoty kafle-przetargu" style="margin:0 0 10px"><div><span>Koszt AI – ${esc(ZU.miesiac)}</span><b>${zl(sumaAi)}</b></div>
      <div><span>Koszt AI – ${esc(ZU.poprzedni_miesiac)}</span><b>${zl(sumaPop)}</b></div>
      <div><span>Kurs USD przyjęty do przeliczeń</span><b>${String(ZU.kurs_usd).replace(".", ",")} zł</b></div></div>
      ${WLASC() ? `<details style="margin:0 0 10px" ontoggle="if (this.open) ladujKosztyZadan()"><summary><b>Najdroższe zadania w tym miesiącu i limity kont</b></summary><div id="koszty-zadan"><p class="opis">Ładuję…</p></div></details>` : ""}
      ${ZU.zadania && Object.keys(ZU.zadania).length ? `<details style="margin:0 0 10px"><summary><b>Koszt AI według rodzaju zadania (${esc(ZU.miesiac)})</b></summary>
        <div class="tabela-okno"><table class="tabela"><tr><th>Rodzaj zadania</th><th>Koszt</th></tr>${Object.entries(ZU.zadania).sort((a, b) => b[1] - a[1]).map(([t, v]) =>
          `<tr><td>${esc(NAZWY_ZADAN[t] || t)}</td><td class="liczba">${zl(v)}</td></tr>`).join("")}</table></div></details>` : ""}
      ${WLASC() ? `<div class="pasek" style="margin:0 0 12px"><span class="opis" style="margin:0">Ogłoszenia (BZP, TED – przetargi powyżej progów UE, Baza Konkurencyjności) pobierane raz dziennie o 01:00 – ostatnio: <b>${esc(ZU.pobranie || "jeszcze nie")}</b>.</span>
        <button class="maly" data-ik="pobierz" onclick="api('/api/wspolne/pobierz', {method: 'POST'}).then(z => sledz(z))">Pobierz teraz</button></div>` : ""}` : ""}
    <div class="tabela-okno"><table class="tabela"><tr><th>Konto</th><th>Firma</th><th>Projekty</th><th>W realizacji</th><th>Przetargi</th><th>Klienci</th><th>Pracownicy</th><th>AI w tym miesiącu</th>${WLASC() ? "<th>Windykacja</th>" : ""}<th>Ostatnio w programie</th><th>Ostatnia aktywność</th><th></th></tr>
      ${K.konta.map(k => `<tr><td><b>${esc(k.login)}</b>${k.admin ? ' <span class="znacznik z-startujemy">Ty</span>' : ""}<br><small class="opis">${esc(k.admin ? "administrator" : (String((JA.role || {})[k.rola] || k.rola || "").split(" – ")[0]))}${k.utworzono ? " · od " + esc(k.utworzono) : ""}</small></td>
        <td>${esc(k.firma || "–")}</td><td class="liczba">${k.projekty}</td><td class="liczba">${k.realizacja}</td><td class="liczba">${k.przetargi}</td>
        <td class="liczba">${k.klienci}</td><td class="liczba">${k.pracownicy}</td>
        <td class="liczba">${zl((k.ai_usd || 0) * (K.kurs_usd || 3.65))}<br><small class="opis">${k.ai_zapytan || 0} zapytań</small></td>
        ${WLASC() ? `<td>${k.admin ? '<span class="opis">zawsze</span>' : `<label style="white-space:nowrap"><input type="checkbox" ${k.windykacja ? "checked" : ""} onchange="kontoWindykacja('${escA(k.login)}', this.checked)"> dostęp</label>`}</td>` : ""}
        <td>${k.ostatnio_w_programie ? esc(k.ostatnio_w_programie) : '<span class="opis">jeszcze nie odnotowano</span>'}</td>
        <td>${esc(k.ostatnia_aktywnosc || "–")}<br><small class="opis">${esc(k.ostatnia_akcja || "")}${k.wpisow ? ` · wpisów: ${k.wpisow}` : ""}</small></td>
        <td style="white-space:nowrap">${k.admin || !WLASC() ? "" : `<button class="maly glowny" data-ik="link" onclick="otworzKonto('${escA(k.login)}')">Otwórz konto</button>`}
          <button class="maly" data-ik="zegar" onclick="KONTO_FILTR='${escA(k.login)}'; ladujKonta()">Aktywność</button></td></tr>`).join("")}</table></div>
    <div class="karta"><h3>${ik("zegar")} Dziennik aktywności ${KONTO_FILTR ? "– konto " + esc(KONTO_FILTR) + ` <button class="maly" onclick="KONTO_FILTR=''; ladujKonta()">wszystkie konta</button>` : "– wszystkie konta"}</h3>
      <div class="tabela-okno" style="max-height:520px"><table class="tabela"><tr><th>Czas</th><th>Konto</th><th>Kto</th><th>Działanie</th><th>Projekt</th><th>Szczegóły</th></tr>
        ${A.map(w => `<tr><td style="white-space:nowrap">${esc(w.czas)}</td><td>${esc(w.konto)}</td><td>${esc(w.login)}${w.login !== w.konto ? ' <small class="opis">(administrator)</small>' : ""}</td>
          <td>${esc(w.akcja)}</td><td>${esc(w.projekt || "")}</td><td>${esc(w.szczegoly || "")}</td></tr>`).join("") || '<tr><td colspan="6" class="pusto">Brak wpisów.</td></tr>'}</table></div></div>`;
}
async function otworzKonto(login) {
  if (!(await bezpiecznie(() => api("/api/konta/jako", {json: {login}})))) return;
  location.href = "/";  // przeładowanie – wszystkie moduły pokażą dane tego konta
}
async function wrocNaKonto() { await bezpiecznie(() => api("/api/konta/jako", {json: {login: ""}})); location.href = "/"; }
function pokazPasekJako() {
  const p = $("#pasek-jako"); if (!p) return;
  p.classList.toggle("ukryj", !JA.jako);
  document.body.classList.toggle("tryb-jako", !!JA.jako);
  if (JA.jako) p.innerHTML = `${ik("ludzie")} Pracujesz na koncie <b>${esc(JA.jako)}</b> (podgląd administratora) – widzisz i zmieniasz dane tego konta.
    <button class="maly" onclick="wrocNaKonto()">Wróć do swojego konta</button> <button class="maly" onclick="pokaz('konta')">Konta i aktywność</button>`;
}

// ================================================================ ARCHIWUM
async function ladujArchiwum() {
  const a = await bezpiecznie(() => api("/api/archiwum")); if (!a) return;
  // przywracanie – tylko rola z edycją Archiwum (nie „Tylko podgląd”); identyfikatory jako bezpieczne argumenty JS (escA)
  const przyc = (rodzaj, id, pid) => `${a.przywracanie !== false ? `<button class="maly zielony" data-ik="cofnij" onclick="archAkcja('przywroc','${rodzaj}','${escA(id)}','${escA(pid || "")}')">Przywróć</button>` : ""}
    ${a.trwale ? `<button class="maly niebezp" data-ik="kosz" onclick="archAkcja('usun','${rodzaj}','${escA(id)}','${escA(pid || "")}')">Usuń trwale</button>` : ""}`;
  ARCH_LISTA = [...a.projekty.map(p => ["projekt", p.id, ""]), ...a.pliki.map(f => ["plik", f.id, f.pid]), ...a.klienci.map(k => ["klient", k.id, ""]), ...a.pracownicy.map(p => ["pracownik", p.id, ""])];
  const wszystkie = (rodzaj, n) => a.trwale && n && rodzaj ? ` <button class="maly niebezp" data-ik="kosz" style="float:right" onclick="archUsunWszystkie('${rodzaj}')">Usuń wszystkie (${n})</button>` : "";
  const RODZ_TAB = {"Projekty": "projekt", "Dokumenty i zdjęcia": "plik", "Klienci": "klient", "Pracownicy": "pracownik"};
  const tab = (tyt, nag, wiersze) => `<div class="karta"><h3>${tyt} (${wiersze.length})${wszystkie(RODZ_TAB[tyt], wiersze.length)}</h3>${wiersze.length ? `<div class="tabela-okno"><table class="tabela"><tr>${nag.map(n => `<th>${n}</th>`).join("")}<th></th></tr>${wiersze.join("")}</table></div>` : '<p class="pusto">Pusto.</p>'}</div>`;
  // raporty dzienne (dziennik pomocniczy) i usterki – przywraca rola z edycją Realizacji; podgląd treści tylko do odczytu, bez przycisków
  const przycR = (rodzaj, id, pid) => a.przywracanie_realizacji ? `<button class="maly zielony" data-ik="cofnij" onclick="archAkcja('przywroc','${rodzaj}','${escA(id)}','${escA(pid || "")}')">Przywróć</button>` : "";
  const POLA_R = [["pogoda", "Pogoda"], ["pracownicy", "Pracownicy"], ["prace", "Wykonane prace"], ["materialy", "Dostawy / materiały"], ["sprzet", "Sprzęt"], ["uwagi", "Zdarzenia, polecenia, uwagi"]];
  const tresc = h => `<details class="arch-podglad"><summary>pokaż treść</summary><dl>${POLA_R.filter(([k]) => h[k]).map(([k, n]) => `<dt>${n}</dt><dd>${esc(h[k])}</dd>`).join("") || "<dd>(pusty raport)</dd>"}</dl></details>`;
  const D_ = a.dziennik || [], U_ = a.usterki || [];
  $("#archiwum").innerHTML = `<p class="opis">Usunięte projekty, dokumenty, zdjęcia, klienci, pracownicy i usterki oraz poprzednie i usunięte wersje raportów dziennych trafiają tutaj – nic nie znika przypadkiem.
      ${a.trwale ? "Jako administrator możesz też usunąć element trwale." : a.przywracanie === false ? "Twoja rola pozwala tylko przeglądać archiwum – przywraca osoba z edycją modułu Archiwum, trwale usuwa administrator." : "Trwale usuwać może tylko administrator."}</p>
    ${a.trwale && ARCH_LISTA.length ? `<div class="pasek"><button class="niebezp" data-ik="kosz" onclick="archUsunWszystkie()">Opróżnij archiwum – usuń trwale wszystko (${ARCH_LISTA.length})</button></div>` : ""}
    ${tab("Projekty", ["Projekt", "Rodzaj", "Zarchiwizowano", "Przez"], a.projekty.map(p => `<tr><td><b>${esc(p.nazwa)}</b></td><td>${esc({nieruchomosc: "DD / wycena nieruchomości", przetarg: "przetarg", zamowienie: "zamówienie", dotacja: "rozliczenie dotacji", wniosek_dot: "wniosek o dotację", kosztorys: "kosztorys", dom: "budowa domu"}[p.typ] || p.typ)}</td><td>${esc(p.data || "")}</td><td>${esc(p.kto || "")}</td><td style="white-space:nowrap">${przyc("projekt", p.id)}</td></tr>`))}
    ${tab("Dokumenty i zdjęcia", ["Plik", "Projekt", "Zarchiwizowano", "Przez"], a.pliki.map(f => `<tr><td>${esc(f.oryginal)}${f.plik && !String(f.id).startsWith("zdj:") ? ` · <a class="dozw" href="/pobierz/${f.pid}/${f.plik.split("/").map(encodeURIComponent).join("/")}">pobierz</a>` : ""}</td>
      <td>${esc(f.projekt || "")}</td><td>${esc(f.data || "")}</td><td>${esc(f.kto || "")}</td><td style="white-space:nowrap">${przyc("plik", f.id, f.pid)}</td></tr>`))}
    ${tab("Raporty dzienne (dziennik pomocniczy) – poprzednie i usunięte wersje", ["Dzień", "Projekt", "Wersja", "Zastąpiono / usunięto", "Przez"], D_.map(h => `<tr><td><b>${dataPl(h.data)}</b>${tresc(h)}</td>
      <td>${esc(h.projekt || "")}</td><td>${esc(String(h.wersja || 1))} · ${esc(h.powod || "")}</td><td>${esc(h.zastapiono || "")}</td><td>${esc(h.kto || "")}</td><td style="white-space:nowrap">${przycR("dziennik", h.id, h.pid)}</td></tr>`))}
    ${tab("Usunięte usterki i zadania", ["Usterka / zadanie", "Projekt", "Status", "Usunięto", "Przez"], U_.map(u => `<tr><td><b>${esc(u.tytul || "")}</b>${u.typ ? ` <small class="opis">(${esc(u.typ)})</small>` : ""}${u.opis || u.lokalizacja ? `<br><small class="opis">${esc([u.lokalizacja, u.opis].filter(Boolean).join(" · "))}</small>` : ""}</td>
      <td>${esc(u.projekt || "")}</td><td>${esc(u.status || "")}${u.termin ? ` · termin ${dataPl(u.termin)}` : ""}</td><td>${esc(u.archiwum_data || "")}</td><td>${esc(u.archiwum_kto || "")}</td><td style="white-space:nowrap">${przycR("usterka", u.id, u.pid)}</td></tr>`))}
    ${D_.length || U_.length ? `<p class="opis">Raporty dzienne i usterki przywraca osoba z edycją modułu Realizacja – przywrócona wersja raportu staje się bieżącą, a dotychczasowa trafia do historii. Tych pozycji nie usuwa się trwale: to ślad zmian (raporty dzienne to dziennik pomocniczy wykonawcy, nie dziennik budowy w rozumieniu art. 45 Prawa budowlanego / EDB).${a.przywracanie_realizacji ? "" : " Twoja rola pozwala tylko na podgląd."}</p>` : ""}
    ${tab("Klienci", ["Klient", "NIP", "Zarchiwizowano"], a.klienci.map(k => `<tr><td><b>${esc(k.nazwa)}</b></td><td>${esc(k.nip || "")}</td><td>${esc(k.archiwum_data || "")}</td><td style="white-space:nowrap">${przyc("klient", k.id)}</td></tr>`))}
    ${tab("Pracownicy", ["Pracownik", "Stanowisko", "Zarchiwizowano"], a.pracownicy.map(p => `<tr><td><b>${esc(p.imie)}</b></td><td>${esc(p.stanowisko || "")}</td><td>${esc(p.archiwum_data || "")}</td><td style="white-space:nowrap">${przyc("pracownik", p.id)}</td></tr>`))}`;
}
let ARCH_LISTA = [];
// trwałe usunięcie wszystkich elementów archiwum (albo jednej sekcji) – po kolei, tą samą trasą co „Usuń trwale” przy elemencie
async function archUsunWszystkie(rodzaj) {
  const lista = ARCH_LISTA.filter(x => !rodzaj || x[0] === rodzaj);
  if (!lista.length) return;
  const co = {projekt: "projekty", plik: "dokumenty i zdjęcia", klient: "klientów", pracownik: "pracowników"}[rodzaj] || "elementy archiwum";
  if (!confirm(`Usunąć TRWALE wszystkie ${co} z archiwum (${lista.length})? Tej operacji nie można cofnąć.`)) return;
  if (!rodzaj && !confirm(`Na pewno? Zostanie usuniętych ${lista.length} elementów – projekty razem z ich plikami.`)) return;
  let ok = 0, zle = 0;
  for (const [r, id, pid] of lista) {
    // pliki projektu usuniętego wcześniej w tej pętli już nie istnieją – pomijamy je bez błędu
    if (r === "plik" && lista.some(x => x[0] === "projekt" && x[1] === pid)) { ok++; continue; }
    try { await api("/api/archiwum/usun", {json: {rodzaj: r, id, pid}}); ok++; } catch (e) { zle++; }
  }
  komunikat(`Usunięto trwale: ${ok}` + (zle ? ` · nie udało się: ${zle}` : "") + ".", zle > 0);
  ladujArchiwum();
}
async function archAkcja(akcja, rodzaj, id, pid) {
  if (akcja === "usun" && !confirm("Usunąć TRWALE? Tej operacji nie można cofnąć.")) return;
  if (rodzaj === "dziennik" && !confirm("Przywrócić tę wersję raportu dziennego? Obecna wersja z tego dnia (jeśli jest) trafi do historii.")) return;
  // raporty dzienne i usterki – adres modułu Realizacja (uprawnienia jak na ekranie budowy)
  const url = ["dziennik", "usterka"].includes(rodzaj) ? `/api/projekty/${encodeURIComponent(pid)}/realizacja/przywroc` : "/api/archiwum/" + akcja;
  if (await bezpiecznie(() => api(url, {json: {rodzaj, id, pid}}))) { komunikat(akcja === "usun" ? "Usunięto trwale." : "Przywrócono."); ladujArchiwum(); }
}

// ================================================================ uprawnienia ról
const MODUL_WIDOKU = {pr_oferty: "projekty", pr_sprawy: "projekty", pr_sporzadz: "projekty", nier: "projekty", dot_zapytania: "projekty", przetargi: "przetargi", projekty: "projekty", wyniki: "projekty", dos_realizacja: "finanse", zam_oferty: "projekty", wlasne: "projekty", kosztorys: "projekty", zam_kosztorys: "projekty",
  zam_weryfikacja: "projekty", zam_dokumentacja: "projekty", zam_projekty: "projekty", realizacja: "realizacja", zam_realizacja: "realizacja",
  inw_projekty: "projekty", inw_budowa: "realizacja", zam_nowe: "projekty", kos_projekty: "projekty", dot_projekty: "projekty", dot_wnioski: "projekty", dot_szukaj: "projekty", dot_nadchodzace: "projekty",
  klienci: "klienci", hurtownie: "hurtownie", pracownicy: "pracownicy", place: "place", kadry: "kadry", firma: "firma",
  archiwum: "archiwum", ustawienia: "ustawienia"};
const SEKCJA_MODULU = {przetargi: "#w-przetargi", projekty: "#w-projekty", realizacja: "#w-realizacja", klienci: "#w-klienci",
  hurtownie: "#w-hurtownie", pracownicy: "#prac-rg", place: "#prac-umowy", kadry: "#prac-kadry", firma: "#w-firma", ustawienia: "#w-ustawienia"};
const poziomU = m => JA.rola === "admin" ? 2 : +((JA.uprawnienia || {})[m] ?? 0);
const wolnoWidok = w => !MODUL_WIDOKU[w] || poziomU(MODUL_WIDOKU[w]) >= 1;
function zastosujUprawnienia() {
  document.querySelectorAll("#nav button[data-w]").forEach(b => b.classList.toggle("brak-upr", !wolnoWidok(b.dataset.w)));
  // moduły tylko do podglądu: ukryj przyciski zmieniające dane (serwer i tak zablokuje zapis)
  const css = Object.entries(SEKCJA_MODULU).filter(([m]) => poziomU(m) === 1).map(([, s]) =>
    `${s} button:not(.dozw):not([data-w]):not(.maly-k), ${s} .upusc, ${s} .korekta, ${s} textarea, ${s} .bez-podgladu { display: none !important; }`).join("\n")
    + (poziomU("finanse") < 2 ? "\n#realizacja .fin-edycja { display: none !important; }" : "")
    + (poziomU("finanse") < 1 ? "\n#realizacja .fin, #realizacja .kwoty { display: none !important; }" : "")
    + (JA.ai === false ? "\n.wymaga-ai { display: none !important; }" : "")
    // rola „Tylko podgląd”: pola formularzy firmy, klientów, hurtowni, pracowników i ustawień konta tylko do odczytu (zapis i tak blokuje serwer – 403)
    + (JA.tylko_odczyt ? "\n" + ["#w-firma", "#w-klienci", "#w-hurtownie", "#prac-rg"].map(s =>
      `${s} .karta input:not([type=search]):not(.dozw), ${s} .karta select:not(.dozw), ${s} table input, ${s} .karta textarea`).join(", ")
      + " { pointer-events: none; opacity: .85; }" : "");
  document.querySelectorAll(".start-linki a").forEach(a => { if (/ustawienia/.test(a.getAttribute("onclick"))) a.classList.toggle("ukryj", poziomU("ustawienia") < 1); });
  let st = document.getElementById("styl-uprawnien"); if (!st) { st = document.createElement("style"); st.id = "styl-uprawnien"; document.head.appendChild(st); }
  st.textContent = css;
}

// ================================================================ start
let JA = {rola: "admin"};
const ADMIN = () => JA.rola === "admin";
const WLASC = () => !!(typeof JA !== "undefined" && JA && JA.wlasciciel);  // właściciel programu – jedyny z dostępem do Odwołań, Leadów i Księgowości
(async () => {
  JA = await api("/api/ja").catch(() => JA);
  document.body.classList.add("rola-" + JA.rola);
  if (JA.tylko_odczyt) document.body.classList.add("tylko-odczyt");
  zastosujUprawnienia();
  rysujGornyPasek();
  setTimeout(pokazTrwajaceZadania, 1500);
  pokazLogo();
  pokazPasekJako();
  wstawZakresAdmina();
  sprawdzNowePrzyStarcie();
  const w = $(".wyloguj button[data-ik=wyloguj] .etykieta"); if (w) w.textContent = `Wyloguj (${JA.login})`;
  // ostatnio wybrany tryb (zapamiętany na koncie i w przeglądarce) – od razu do Pulpitu tego trybu
  let tr = JA.ostatni_tryb; try { tr = tr || localStorage.getItem("tryb"); } catch (e) {}
  history.replaceState({korzen: true}, "", location.pathname);  // przycisk Wstecz nie wychodzi z programu – patrz obsługa popstate
  if (JA.modul) return ograniczDoModulu(JA.modul);
  if (["wykonawca", "dostawca", "zamawiajacy", "inwestor", "kosztorysant", "dotacje", "prawnik"].includes(tr)) wybierzStrone(tr); else pokaz("start");
})();

// ================================================================ KONTO OGRANICZONE DO JEDNEGO MODUŁU (administrator: Użytkownicy strony → „Dostęp do modułów”)
// Zawsze ta sama ścieżka (np. wspólnoty = zamawiający prywatny), bez wyboru rodzaju działalności i przejść do innych modułów.
// Serwer i tak blokuje adresy i projekty innych modułów – tu tylko porządek w interfejsie.
const MODUL_STRONA = {gmina: ["zamawiajacy", false], wspolnota: ["zamawiajacy", true]};
function ograniczDoModulu(mod) {
  const [st, pryw] = MODUL_STRONA[mod] || [mod, false];
  document.body.classList.add("modul-konta", "modul-" + mod);
  if (st === "zamawiajacy") { ustawZamPryw(pryw); ustawZamPryw = () => { ZAM_PRYW = pryw; }; }
  try { localStorage.setItem("tryb", st); } catch (e) {}
  const _wybierzStrone = wybierzStrone;
  wybierzStrone = function (s, ...reszta) { return _wybierzStrone(st, ...reszta); };
  const _pokaz = pokaz;
  pokaz = function (w, ...reszta) { if (w === "start") return wybierzStrone(st, true); return _pokaz(w, ...reszta); };
  let czeka = false;
  const filtruj = () => {
    czeka = false;
    document.querySelectorAll("[onclick*=\"wybierzStrone(\"]").forEach(b => {
      const o = b.getAttribute("onclick") || "";
      const inna = !o.includes(`'${st}'`) || (st === "zamawiajacy" && /ustawZamPryw\((true|false)\)/.test(o) && !o.includes(`ustawZamPryw(${pryw})`));
      if (inna) b.remove();
    });
    document.querySelectorAll("[onclick*=\"pokaz('start')\"], #nav button[data-w=\"start\"]").forEach(b => b.remove());
    if (typeof odswiezGrupyMenu === "function") odswiezGrupyMenu();
  };
  filtruj();
  new MutationObserver(() => { if (!czeka) { czeka = true; requestAnimationFrame(filtruj); } }).observe(document.body, {childList: true, subtree: true});
  wybierzStrone(st);
}

// ================================================================ EDYCJA PROGRAMU (np. „zamawiajacy” – wersja dla urzędu)
// Serwer wstawia window.EDYCJA do strony; w edycji urzędu zawsze ścieżka zamawiającego, a widoki i przyciski innych
// modułów są usuwane (serwer i tak blokuje ich adresy – to tylko porządek w interfejsie).
const EDYCJA = window.EDYCJA || "pelna";
const WIDOKI_EDYCJI = {zamawiajacy: new Set(["pulpit", "cel", "zam_nowe", "zam_projekty", "zam_kosztorys", "zam_weryfikacja", "zam_dokumentacja",
  "zam_oferty", "zam_realizacja", "firma", "archiwum", "konta", "ustawienia", "instrukcja", "olioc", "sprawozdanie", "kalk_pracy", "plan_zam", "plan_spr"])};
if (EDYCJA !== "pelna" && WIDOKI_EDYCJI[EDYCJA]) {
  const DOZW = WIDOKI_EDYCJI[EDYCJA];
  document.body.classList.add("edycja-" + EDYCJA);
  try { localStorage.setItem("tryb", "zamawiajacy"); } catch (e) {}
  ustawZamPryw(false); ustawZamPryw = () => { ZAM_PRYW = false; };  // urząd = zamawiający publiczny; moduł wspólnot niedostępny
  const _wybierzStrone = wybierzStrone;
  wybierzStrone = function (s, ...reszta) { return _wybierzStrone("zamawiajacy", ...reszta); };
  const _pokaz = pokaz;
  pokaz = function (w, ...reszta) {
    if (!DOZW.has(w)) { if (!STRONA) wybierzStrone("zamawiajacy", false, true); w = "pulpit"; }
    return _pokaz(w, ...reszta);
  };
  let czeka = false;
  const filtrujEdycje = () => {
    czeka = false;
    document.querySelectorAll("#nav button[data-w]").forEach(b => { if (!DOZW.has(b.dataset.w)) b.remove(); });
    document.querySelectorAll("[onclick*=\"pokaz('\"]").forEach(b => {
      const m = (b.getAttribute("onclick") || "").match(/pokaz\('([a-z_]+)'/); if (m && !DOZW.has(m[1])) b.remove(); });
    document.querySelectorAll("[onclick*=\"wybierzStrone(\"]").forEach(b => { const o = b.getAttribute("onclick") || ""; if (!/zamawiajacy/.test(o) || /ustawZamPryw\(true\)/.test(o)) b.remove(); });
    if (typeof odswiezGrupyMenu === "function") odswiezGrupyMenu();
  };
  filtrujEdycje();
  new MutationObserver(() => { if (!czeka) { czeka = true; requestAnimationFrame(filtrujEdycje); } }).observe(document.body, {childList: true, subtree: true});
  const marka = document.querySelector("#nav .marka, .logo-tekst"); if (marka && /^Bidivia$/.test(marka.textContent.trim())) marka.textContent = "Bidivia – Zamawiający";
}


// ================================================================ DLA PRAWNIKA – ustawienia sprawy i opinia prawna
const PR_PRZEDMIOT = {dostawy: "Dostawy", uslugi: "Usługi", roboty: "Roboty budowlane na nieruchomości"};
const PR_DLA = {zamawiajacy: "Dla zamawiającego", wykonawca: "Dla wykonawcy (oferenta)", niezalezna: "Niezależna opinia"};
const PR_TRYBY = {auto: "Ustal z dokumentów", podstawowy_1: "Tryb podstawowy bez negocjacji (art. 275 pkt 1)", podstawowy_2: "Tryb podstawowy z możliwością negocjacji (art. 275 pkt 2)",
  podstawowy_3: "Tryb podstawowy z obowiązkowymi negocjacjami (art. 275 pkt 3)", przetarg_nieograniczony: "Przetarg nieograniczony", przetarg_ograniczony: "Przetarg ograniczony",
  negocjacje_z_ogloszeniem: "Negocjacje z ogłoszeniem", dialog: "Dialog konkurencyjny", partnerstwo: "Partnerstwo innowacyjne", negocjacje_bez_ogloszenia: "Negocjacje bez ogłoszenia",
  wolna_reka: "Zamówienie z wolnej ręki", sektorowe: "Zamówienie sektorowe", ponizej_progu: "Poniżej progu Pzp (regulamin / zapytanie ofertowe)",
  zasada_konkurencyjnosci: "Zasada konkurencyjności (dofinansowanie UE)"};
function prawnikUstawienia(p) {
  const u = Object.assign({przedmiot: "roboty", tryb: "auto", dla_kogo: "zamawiajacy", klient: "", pytania_klienta: ""}, p.prawnik || {});
  const sel = (id, v, o) => `<select id="${id}" onchange="prawnikZapisz()">${Object.entries(o).map(([k, t]) => `<option value="${k}" ${k === v ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
  return `<div class="krok" id="sek-prawnik"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Sprawa – ustawienia</h3>
    <span class="stan">${esc(PR_DLA[u.dla_kogo])}</span></div><div class="tresc">
    <p class="opis">Przedmiot, tryb i strona zmieniają listę kontrolną sprawdzania. Po zmianie sprawdź dokumentację ponownie.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
      <label class="ks-pole">Przedmiot zamówienia${sel("pr-przedmiot", u.przedmiot, PR_PRZEDMIOT)}</label>
      <label class="ks-pole">Tryb${sel("pr-tryb", u.tryb, PR_TRYBY)}</label>
      <label class="ks-pole">Dla kogo${sel("pr-dla", u.dla_kogo, PR_DLA)}</label>
      <label class="ks-pole">Adresat opinii (klient)<input id="pr-klient" value="${esc(u.klient)}" onchange="prawnikZapisz()" placeholder="np. Gmina X / firma Y"></label>
    </div>
    <label class="ks-pole" style="margin-top:8px">Pytania lub obawy klienta (AI na nie odpowie)<textarea id="pr-pytania" rows="2" onchange="prawnikZapisz()">${esc(u.pytania_klienta)}</textarea></label>
    <p class="opis" style="margin:6px 0 0">Dokumenty do oceny – w kroku 1: wgraj pliki (także własne wzory) albo podaj link do ogłoszenia.</p>
    ${(p.weryfikacja || {}).nieaktualna ? `<div class="ramka-uwaga">${esc(p.weryfikacja.nieaktualna)}</div>` : ""}
  </div></div>`;
}
async function prawnikZapisz() {
  const j = {przedmiot: $("#pr-przedmiot").value, tryb: $("#pr-tryb").value, dla_kogo: $("#pr-dla").value, klient: $("#pr-klient").value, pytania_klienta: $("#pr-pytania").value};
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/prawnik`, {json: j})); if (!r) return;
  komunikat("Zapisano ustawienia sprawy."); otworzProjekt(PROJEKT_ID);
}
function prawnikOpinia(p) {
  const o = p.opinia_prawna, w = p.weryfikacja;
  return `<div class="krok" id="sek-opinia"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Opinia prawna</h3>
    <span class="stan">${o ? "sporządzono " + esc(o.data) : w ? "do zrobienia" : "najpierw sprawdź dokumentację"}</span></div><div class="tresc">
    <p class="opis">Pismo w Wordzie: przedmiot opinii, stan faktyczny, analiza prawna zagadnień z podstawą prawną i rekomendacją, odpowiedzi na pytania klienta, wnioski.
      Powstaje z ustaleń ze sprawdzenia (bez uwag oznaczonych jako odrzucone); miejsca do uzupełnienia – na żółto. Raport uwag pobierzesz w sekcji powyżej.</p>
    <div class="pasek">${w ? `<button class="glowny" data-ik="iskra" onclick="prawnikOpiniaGeneruj()">${o ? "Sporządź opinię ponownie" : "Sporządź opinię prawną"}</button>` : ""}
      ${o ? `<a class="przycisk" href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(o.plik)}">Pobierz opinię (Word)</a>` : ""}</div>
  </div></div>`;
}
async function prawnikOpiniaGeneruj() { sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/opinia-prawna`, {json: {}})), () => otworzProjekt(PROJEKT_ID)); }

async function pobierzZLinku() {
  const url = ($("#dok-link").value || "").trim(); if (!/^https?:\/\//i.test(url)) return komunikat("Wklej pełny adres postępowania (https://…).", true);
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/pobierz-z-linku`, {json: {url}})), () => otworzProjekt(PROJEKT_ID));
}


// ================================================================ SPRAWA PRAWNIKA – 4 kroki
let PR_DOK = "mam";  // krok 2: "mam" (wgraj / link) albo "przygotuj"
function rysujSprawePrawnika(p) {
  const cel = p.cel_prawnika || (p.start_przygotuj ? "sporzadz" : "sprawdz"), SP = cel === "sporzadz";
  const u = Object.assign({przedmiot: "", tryb: "auto", dla_kogo: "zamawiajacy", klient: "", pytania_klienta: "", zatwierdzone: ""}, p.prawnik || {});
  const pl = p.pliki || [];
  const k1 = !!u.zatwierdzone, k2 = pl.length > 0, k3 = !!p.weryfikacja && !(p.weryfikacja || {}).nieaktualna, k4 = SP ? !!p.przygotowanie_prawnika : !!p.opinia_prawna;
  const blok = (nr, tytul, stan, tresc, otwarty) => `<div class="krok ${otwarty ? "" : "pr-zablokowany"}" id="pr-krok-${nr}"><div class="tytul"><span class="nr">${nr}</span><h3>${tytul}</h3>
    <span class="stan">${stan}</span></div><div class="tresc">${otwarty ? tresc : `<p class="opis">Najpierw zakończ krok ${nr - 1}.</p>`}</div></div>`;
  const sel = (id, v, o) => `<select id="${id}">${Object.entries(o).map(([k, t]) => `<option value="${k}" ${k === v ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
  // ---- krok 1: czego dotyczy
  const t1 = k1 && !PR_EDYCJA1 ? `<p><b>${esc(PR_PRZEDMIOT[u.przedmiot] || "")}</b> · ${esc(PR_TRYBY[u.tryb] || "")}${SP ? "" : " · " + esc(PR_DLA[u.dla_kogo] || "")}${u.klient ? " · " + (SP ? "zamawiający: " : "adresat: ") + esc(u.klient) : ""}</p>
      ${u.pytania_klienta && !SP ? `<p class="opis">Pytania klienta: ${esc(u.pytania_klienta)}</p>` : ""}<div class="pasek"><button class="maly" onclick="PR_EDYCJA1=true; rysujSprawePrawnika(PROJEKT)">Zmień</button></div>`
    : `<p class="opis">${SP ? "Czego dotyczy zamówienie – od tego zależy komplet dokumentów i lista kontrolna sprawdzenia." : "Czego dotyczy sprawa – od tego zależy lista kontrolna sprawdzenia."}</p>
      <div class="pr-przedmiot">${Object.entries(PR_PRZEDMIOT).map(([k, t]) => `<button class="${(PR_WYBOR || (k1 ? u.przedmiot : "")) === k ? "glowny" : ""}" data-k="${k}"
        onclick="PR_WYBOR='${k}'; document.querySelectorAll('.pr-przedmiot button').forEach(b=>b.classList.toggle('glowny', b.dataset.k==='${k}'))">${esc(t)}</button>`).join("")}</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px 14px;margin-top:10px">
        <label class="ks-pole">Tryb${sel("pr-tryb", u.tryb, PR_TRYBY)}</label>
        ${SP ? `<label class="ks-pole">Zamawiający (nazwa, adres, NIP)<input id="pr-klient" value="${esc(u.klient)}" placeholder="uzupełnij – nie z Profilu firmy" ${u.klient ? "" : 'style="background:var(--zolty-jasny)"'}></label>`
          : `<label class="ks-pole">Dla kogo${sel("pr-dla", u.dla_kogo, PR_DLA)}</label>
             <label class="ks-pole">Adresat opinii (klient)<input id="pr-klient" value="${esc(u.klient)}" placeholder="np. Gmina X / firma Y"></label>`}</div>
      ${SP ? "" : `<label class="ks-pole" style="margin-top:8px">Pytania lub obawy klienta (opcjonalnie)<textarea id="pr-pytania" rows="2">${esc(u.pytania_klienta)}</textarea></label>`}
      <div class="pasek" style="margin-top:10px"><button class="glowny" onclick="prawnikKrok1()">Zatwierdź i przejdź dalej →</button></div>`;
  // ---- krok 2: dokumentacja (sprawdzenie) albo „co chcesz zamówić” (sporządzenie)
  const listaPl = pl.length ? `<div class="tabela-okno" style="max-height:260px"><table class="tabela"><tr><th></th><th>Uwzględniać</th><th>Plik</th><th>Rozmiar</th></tr>
      ${pl.map(f => `<tr><td><input type="checkbox" class="pl" value="${esc(f.sciezka)}"></td><td>${f.uwzglednij ? "✔" : '<span class="czerwone">pominięty</span>'}</td>
      <td>${esc(f.sciezka)}</td><td class="liczba">${liczba(f.rozmiar / 1048576, 2)} MB</td></tr>`).join("")}</table></div>
      <div class="pasek"><button class="maly" onclick="przelaczPliki()">Uwzględniaj / pomiń zaznaczone</button><button class="maly" onclick="usunPliki(false)">Usuń zaznaczone</button></div>` : "";
  const wgraj = `<div class="upusc" id="upusc">${SP ? "Przeciągnij to, co masz: ogłoszenie, SWZ, opis przedmiotu, własne wzory (PDF, Word, Excel, ZIP)" : "Przeciągnij pliki (PDF, Word, Excel, ZIP – także własne wzory do oceny)"} albo
        <label class="przycisk" data-ik="wgraj">wybierz z dysku<input type="file" multiple hidden onchange="wgrajPliki(this.files)"></label></div>
      <div style="display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;margin:8px 0">
        <label class="ks-pole" style="flex:1;min-width:240px">albo link do ogłoszenia / postępowania (e-Zamówienia, BZP, Baza Konkurencyjności, BIP, platforma)
          <input id="dok-link" type="url" placeholder="https://…" value="${esc((p.link_postepowania || {}).url || "")}"></label>
        <button class="zielony" data-ik="pobierz" onclick="pobierzZLinku()">Pobierz dokumenty z linku</button></div>
      ${p.link_postepowania ? `<p class="opis">Z linku ${esc(p.link_postepowania.data)}: ${p.link_postepowania.pliki} plików (${esc(p.link_postepowania.sposob)})${p.link_postepowania.uwaga ? " – " + esc(p.link_postepowania.uwaga) : ""}.</p>` : ""}`;
  const t2 = SP ? `<p class="opis">Opisz, co chcesz zamówić, albo wgraj to, co już masz – program sprawdzi to z przepisami i przygotuje pozostałe dokumenty kompletu.</p>
      <label class="ks-pole">Co chcesz zamówić (przedmiot, zakres, ilości, terminy, wymagania)<textarea id="pr-opis" rows="5" placeholder="np. Dostawa 40 laptopów z oprogramowaniem dla szkół gminy, dostawa do 30 dni, gwarancja 36 miesięcy…">${esc(p.opis_zamowienia_prawnika || "")}</textarea></label>
      <div class="pasek" style="margin:6px 0 10px"><button class="glowny" onclick="prawnikOpis()">Zapisz opis</button></div>${wgraj}${listaPl}`
    : wgraj + listaPl;
  // ---- krok 3: sprawdzenie (materiału / dokumentacji)
  const t3 = `<div id="pr-krok-3">${krokZamawiajacego(p, "weryfikacja", 3)}</div>`;
  // ---- krok 4: opinia albo komplet
  const t4 = SP ? `<div id="pr-przygotuj"><p class="opis">Wczytuję komplet dokumentów dla trybu…</p></div>` : prawnikOpiniaTresc(p);
  $("#projekt").innerHTML = `
  <div class="naglowek"><input id="pr-nazwa" value="${esc(p.nazwa)}" onchange="zmienNazwe(this.value)">
    <button class="maly dozw" data-ik="pobierz" onclick="location.href='/api/projekty/${p.id}/raport.docx'">Raport</button>
    <button class="maly" data-ik="teczka" onclick="usunProjekt()" title="Sprawa trafi do Archiwum – można ją przywrócić">Archiwizuj</button></div>
  <p class="opis" style="margin:0 0 8px">${SP ? "Ścieżka: <b>sporządzenie dokumentacji</b> – czego dotyczy → co chcesz zamówić → sprawdzenie z przepisami → komplet dokumentów do postępowania."
    : "Ścieżka: <b>sprawdzenie dokumentacji</b> – czego dotyczy → dokumentacja → sprawdzenie → opinia prawna."}</p>
  ${blok(1, SP ? "Czego dotyczy zamówienie" : "Czego dotyczy sprawa", k1 ? esc(PR_PRZEDMIOT[u.przedmiot] || "") : "do zrobienia", t1, true)}
  ${blok(2, SP ? "Co chcesz zamówić – opis albo dokumenty" : "Dokumentacja do sprawdzenia", k2 ? `${pl.length} ${pl.length === 1 ? "plik" : "plików"}` : "do zrobienia", t2, k1)}
  ${k1 && k2 ? t3 : blok(3, SP ? "Sprawdzenie z przepisami" : "Sprawdzenie dokumentacji", "do zrobienia", "", false)}
  ${blok(4, SP ? "Komplet dokumentów do postępowania" : "Opinia prawna", k4 ? (SP ? "przygotowano " + esc(p.przygotowanie_prawnika.data) : "sporządzono " + esc(p.opinia_prawna.data)) : "do zrobienia", t4, k1 && k2 && !!p.weryfikacja)}`;
  const uz = $("#upusc");
  if (uz) {
    ["dragenter", "dragover"].forEach(e => uz.addEventListener(e, ev => { ev.preventDefault(); uz.classList.add("nad"); }));
    ["dragleave", "drop"].forEach(e => uz.addEventListener(e, ev => { ev.preventDefault(); uz.classList.remove("nad"); }));
    uz.addEventListener("drop", ev => wgrajPliki(ev.dataTransfer.files));
  }
  if (SP && k1 && k2 && p.weryfikacja) prawnikPrzygotujForm(p);
}
async function prawnikOpis() {
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/prawnik/opis`, {json: {opis: $("#pr-opis").value}}))) { komunikat("Zapisano opis – przejdź do sprawdzenia."); otworzProjekt(PROJEKT_ID); }
}
let PR_EDYCJA1 = false, PR_WYBOR = null;
async function prawnikKrok1() {
  const przedmiot = PR_WYBOR || ((PROJEKT.prawnik || {}).zatwierdzone ? (PROJEKT.prawnik || {}).przedmiot : "");  // nowa sprawa – wybór wymagany
  if (!przedmiot) return komunikat("Wybierz, czego dotyczy sprawa: dostawy, usługi albo roboty budowlane.", true);
  const j = {przedmiot, tryb: $("#pr-tryb").value, dla_kogo: ($("#pr-dla") || {}).value || "zamawiajacy", klient: $("#pr-klient").value,
    pytania_klienta: ($("#pr-pytania") || {}).value || "", zatwierdzone: "1"};
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/prawnik`, {json: j})); if (!r) return;
  PR_EDYCJA1 = false; PR_WYBOR = null; await otworzProjekt(PROJEKT_ID);
  document.getElementById("pr-krok-2")?.scrollIntoView({behavior: "smooth"});
}
async function prawnikPrzygotujForm(p) {
  const d = await api(`/api/projekty/${PROJEKT_ID}/prawnik/komplet`).catch(() => null); const el = $("#pr-przygotuj"); if (!d || !el) return;
  const P = Object.assign({zamawiajacy: (p.prawnik || {}).klient || ""}, (d.przygotowanie || {}).pola || {}), u = p.prawnik || {}, dost = d.dostarczone || [];
  const pole = (id, et, v, typ = "text", zolte = false) => `<label class="ks-pole">${et}<input id="prp-${id}" type="${typ}" value="${esc(v || "")}" ${zolte && !v ? 'style="background:var(--zolty-jasny)"' : ""}></label>`;
  el.innerHTML = `<p class="opis">Program przygotuje brakujące dokumenty kompletu dla trybu <b>${esc(PR_TRYBY[u.tryb] || "")}</b> (${esc(PR_PRZEDMIOT[u.przedmiot] || "")})
      na podstawie opisu i dokumentów z kroku 2. Dane, których brakuje, zostaną oznaczone [UZUPEŁNIJ] na żółto.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
      ${pole("zamawiajacy", "Zamawiający (nazwa, adres, NIP)", P.zamawiajacy, "text", true)}${pole("nazwa", "Nazwa zamówienia", P.nazwa || p.nazwa)}
      ${pole("znak", "Znak sprawy", P.znak)}${pole("wartosc", "Wartość szacunkowa netto [zł]", P.wartosc)}
      ${pole("termin_realizacji", "Termin realizacji", P.termin_realizacji)}${pole("termin_ofert", "Termin składania ofert", P.termin_ofert)}
      ${pole("kryteria", "Kryteria oceny ofert", P.kryteria)}${pole("wadium", "Wadium", P.wadium)}${pole("gwarancja", "Gwarancja", P.gwarancja)}</div>
    <label class="ks-pole" style="margin-top:8px">Uzupełnienie opisu (opcjonalnie – podstawą jest opis i dokumenty z kroku 2)<textarea id="prp-zakres" rows="2">${esc(P.zakres || "")}</textarea></label>
    <label class="ks-pole" style="margin-top:8px">Dodatkowe wymagania<textarea id="prp-uwagi" rows="2">${esc(P.uwagi || "")}</textarea></label>
    <h4 style="margin:12px 0 4px">Własne wzory (opcjonalnie)</h4>
    <p class="opis" style="margin:0 0 6px">Program zachowa ich układ, numerację i sformułowania. ${d.wzory.length ? "Wgrane: <b>" + esc(d.wzory.join(", ")) + "</b>" : "Brak wgranych wzorów."}</p>
    <label class="przycisk maly" data-ik="wgraj">Wgraj wzory<input type="file" multiple hidden onchange="prawnikWzory(this.files)"></label>
    <h4 style="margin:12px 0 4px">Dokumenty do przygotowania</h4>
    <div class="pasek" style="flex-wrap:wrap">${d.komplet.map(([k, t]) => `<label class="wiersz" style="margin:0"><input type="checkbox" class="prp-dok" value="${k}" ${dost.includes(k) ? "" : "checked"}> ${esc(t)}${dost.includes(k) ? ' <small class="opis">(dostarczony – nie piszę od nowa)</small>' : ""}</label>`).join("")}</div>
    ${(p.weryfikacja || {}).uwagi && p.weryfikacja.uwagi.length ? `<p class="opis">Przygotowane dokumenty uwzględnią wyniki sprawdzenia z kroku 3 (${p.weryfikacja.uwagi.filter(x => x.status !== "odrzucone").length} uwag – bez odrzuconych).</p>` : ""}
    <div class="pasek" style="margin-top:8px"><button class="glowny" data-ik="iskra" onclick="prawnikPrzygotuj()">Przygotuj komplet dokumentów</button>
      ${(d.przygotowanie || {}).data ? `<a class="przycisk zielony" data-ik="pobierz" href="/api/projekty/${PROJEKT_ID}/prawnik/komplet.zip">Pobierz komplet (ZIP)</a>
        <span class="opis" style="margin:0">przygotowano ${esc(d.przygotowanie.data)}: ${esc(d.przygotowanie.pliki.join(", "))}</span>` : ""}</div>`;
}
async function prawnikWzory(files) {
  if (!files || !files.length) return;
  const fd = new FormData(); [...files].forEach(f => fd.append("pliki", f));
  if (await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/kreator/wzory`, {body: fd, method: "POST"}))) { komunikat("Wgrano wzory."); prawnikPrzygotujForm(PROJEKT); }
}
async function prawnikPrzygotuj() {
  const dokumenty = [...document.querySelectorAll(".prp-dok:checked")].map(e => e.value);
  const pola = {}; ["zamawiajacy", "nazwa", "znak", "wartosc", "termin_realizacji", "termin_ofert", "kryteria", "wadium", "gwarancja", "zakres", "uwagi"].forEach(k => pola[k] = ($("#prp-" + k) || {}).value || "");
  sledz(await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/prawnik/przygotuj`, {json: {dokumenty, pola}})), () => otworzProjekt(PROJEKT_ID));
}
function prawnikOpiniaTresc(p) {
  const o = p.opinia_prawna;
  return `<p class="opis">Pismo w Wordzie: przedmiot opinii, stan faktyczny, analiza zagadnień z podstawą prawną i rekomendacją, odpowiedzi na pytania klienta, wnioski.
      Powstaje z wyników sprawdzenia (bez uwag odrzuconych); miejsca do uzupełnienia – na żółto.</p>
    ${(p.weryfikacja || {}).nieaktualna ? `<div class="ramka-uwaga">${esc(p.weryfikacja.nieaktualna)}</div>` : ""}
    <div class="pasek"><button class="glowny" data-ik="iskra" onclick="prawnikOpiniaGeneruj()">${o ? "Sporządź opinię ponownie" : "Sporządź opinię prawną"}</button>
      ${o ? `<a class="przycisk" href="/pobierz/${PROJEKT_ID}/${encodeURIComponent(o.plik)}">Pobierz opinię (Word)</a>` : ""}</div>`;
}

let PR_DOK_PID = null;
async function nowaSprawaPrzygotuj() {
  const nazwa = prompt("Nazwa sprawy (np. „Gmina X – dostawa sprzętu, dokumentacja postępowania”):"); if (!nazwa) return pokaz("pr_sprawy");
  const r = await bezpiecznie(() => api("/api/projekty", {json: {nazwa, typ: "prawnik", przygotuj: true}})); if (!r) return;
  PR_DOK_PID = null; WIDOK = "pr_sprawy"; await ladujProjekty(); otworzProjekt(r.id);
}


// ================================================================ RYNKOWOŚĆ CEN (zamawiający i prawnik) + zakończenie ścieżki prawnika „Sprawdź oferty”
const KL_KOL = {"rażąco niska – obowiązkowe wezwanie": "#dc2626", "niska – do wyjaśnienia": "#d97706", "zawyżona": "#7c3aed", "rynkowa": "#16a34a"};
function sekcjaRynkowosci(O) {
  const swz = O.swz || {}, zb = O.oferty.filter(o => (o.wynik || {}).cena_brutto);
  const wiersz = o => { const r = o.rynkowosc; if (!r) return `<tr><td>${esc(o.nazwa)}</td><td colspan="4" class="opis">nie sprawdzono</td></tr>`;
    const odst = (r.pozycje || []).filter(p => p.flaga !== "rynkowa");
    return `<tr><td><b>${esc(o.nazwa)}</b></td><td><b style="color:${KL_KOL[r.klasyfikacja] || "inherit"}">${esc(r.klasyfikacja)}</b><br><small class="opis">${esc(r.podstawa || "")}</small></td>
      <td><small>${esc((r.art224 || {}).opis || "")}${r.inzynieria_cenowa ? "<br>" + esc(r.inzynieria_cenowa) : ""}${r.koszty_pracy ? "<br>" + esc(r.koszty_pracy.opis) : ""}</small></td>
      <td><small>${r.sprawdzono_pozycji || 0} z ${r.pozycji_oferty || 0} poz. (${esc(r.zakres || "")})${odst.length ? "<br>odstające: " + odst.slice(0, 5).map(p => `poz. ${esc(p.lp)} ${p.odchylenie_proc > 0 ? "+" : ""}${p.odchylenie_proc}%`).join(", ") : ""}</small>
        ${(r.pozycje || []).length ? `<details><summary class="opis">pozycje i źródła</summary><ul class="lista">${r.pozycje.map(p => `<li>poz. ${esc(p.lp)} ${esc(String(p.opis).slice(0, 70))}: ${p.cena_jedn} zł vs rynek ${p.rynek_typowa} zł (${p.odchylenie_proc}%) ${(p.zrodla || []).map(z => `<a href="${esc(z.url)}" target="_blank" rel="noopener">${esc(z.nazwa || "źródło")}</a>`).join(" ")}</li>`).join("")}</ul></details>` : ""}</td>
      <td>${r.klasyfikacja !== "rynkowa" ? `<button class="maly" onclick="dokOceny('wezwanie224', '${o.id}')">Wezwanie art. 224 (Word)</button>` : ""}</td></tr>`; };
  return `<div class="krok k-ziel" id="sek-rynkowosc"><div class="tytul"><span class="nr">${ik("procent")}</span><h3>Rynkowość cen ofert</h3>
    <span class="stan">${zb.some(o => o.rynkowosc) ? "sprawdzono" : zb.length ? "do sprawdzenia" : "najpierw zbadaj oferty"}</span></div><div class="tresc">
    <p class="opis">Cena całkowita a próg z art. 224 ust. 2 pkt 1 Pzp (o co najmniej 30% poniżej wartości zamówienia z VAT albo średniej cen ofert – obowiązkowe wezwanie) oraz pozycje oferty a aktualne ceny rynkowe
      (roboty – także inżynieria cenowa, usługi – koszty pracy). Ceny z internetu to ceny ofertowe, nie transakcyjne – wynik jest materiałem do decyzji, nie rozstrzygnięciem.</p>
    <div style="display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap">
      <label class="ks-pole">Wartość zamówienia z VAT ustalona przed wszczęciem [zł]<input id="ry-wartosc" type="number" step="0.01" value="${swz.wartosc_zam_brutto || ""}"
        ${swz.wartosc_zam_brutto && !(OCD.projekt.z_kreatora && !swz.wartosc_zam_reczna && !swz.stawka_vat_znana) ? "" : 'style="background:var(--zolty-jasny)"'} onchange="ryWartosc(this.value)">
        ${OCD.projekt.z_kreatora && swz.wartosc_zam_brutto && !swz.wartosc_zam_reczna ? (swz.stawka_vat_znana
          ? `<small class="opis">z kreatora: wartość netto + VAT ${Math.round((+swz.stawka_vat || 0) * 100)}% (stawka z kosztorysu zamówienia) – od tej kwoty liczy się próg z art. 224.</small>`
          : '<small class="opis">z kreatora: wartość netto × 1,23 – przyjęto VAT 23% (stawka nieustalona). Sprawdź stawkę (np. 8% – budownictwo mieszkaniowe) i popraw – od tej kwoty liczy się próg z art. 224.</small>') : ""}</label>
      <label class="ks-pole">Zakres<select id="ry-zakres"><option value="80">pozycje tworzące 80% wartości (zalecane)</option><option value="wszystkie">wszystkie pozycje</option></select></label>
      ${zb.length ? `<button class="glowny" data-ik="iskra" onclick="rySprawdz()">Sprawdź rynkowość cen</button>` : ""}</div>
    ${zb.length ? `<div class="tabela-okno" style="margin-top:8px"><table class="tabela"><tr><th>Oferta</th><th>Ocena ceny</th><th>Art. 224 / uwagi</th><th>Pozycje</th><th></th></tr>${zb.map(wiersz).join("")}</table></div>` : ""}
  </div></div>`;
}
async function ryWartosc(v) { if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/wartosc`, {json: {wartosc_brutto: v}}))) otworzOcene(OC_ID); }
async function rySprawdz() {
  sledz(await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/rynkowosc`, {json: {wszystkie: $("#ry-zakres").value === "wszystkie"}})), () => otworzOcene(OC_ID));
}
function kartaPrawnikaOferty(p) {
  const u = p.prawnik || {}, sel = (id, v, o) => `<select id="${id}" onchange="prOfZapisz()">${Object.entries(o).map(([k, t]) => `<option value="${k}" ${k === v ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
  return `<div class="krok k-fiol"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Czego dotyczy i dla kogo</h3><span class="stan">${esc(PR_DLA[u.dla_kogo] || "")}</span></div><div class="tresc">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 14px">
      <label class="ks-pole">Przedmiot${sel("po-przedmiot", u.przedmiot, PR_PRZEDMIOT)}</label><label class="ks-pole">Tryb${sel("po-tryb", u.tryb, PR_TRYBY)}</label>
      <label class="ks-pole">Dla kogo${sel("po-dla", u.dla_kogo, PR_DLA)}</label>
      <label class="ks-pole">${u.dla_kogo === "wykonawca" ? "Odwołujący / klient" : "Klient (adresat opinii)"}<input id="po-klient" value="${esc(u.klient || "")}" onchange="prOfZapisz()"></label></div>
    <p class="opis" style="margin:6px 0 0">${u.dla_kogo === "wykonawca" ? "Wykonawca: sprawdzenie oferty konkurenta (podstawy odwołania) albo własnej oferty przed złożeniem – na końcu raport, opinia i projekt odwołania do KIO."
      : "Zamawiający (komisja): zgodność ofert z zamówieniem i rynkowość cen – na końcu raport i opinia prawna."}</p></div></div>`;
}
async function prOfZapisz() {
  const j = {przedmiot: $("#po-przedmiot").value, tryb: $("#po-tryb").value, dla_kogo: $("#po-dla").value, klient: $("#po-klient").value, zatwierdzone: "1"};
  if (await bezpiecznie(() => api(`/api/projekty/${OC_ID}/prawnik`, {json: j}))) otworzOcene(OC_ID);
}
function sekcjaPrawnikaOferty(p) {
  const d = p.prawnik_oferty || {}, wyk = (p.prawnik || {}).dla_kogo === "wykonawca";
  const poz = (co, t) => `<button ${co === "raport" ? "" : 'data-ik="iskra"'} onclick="prOfDok('${co}')">${d[co] ? "Ponownie: " : ""}${t}</button>${d[co] ? ` <a class="przycisk zielony maly" href="/pobierz/${OC_ID}/ocena/${encodeURIComponent(d[co].plik)}">Pobierz (${esc(d[co].data)})</a>` : ""}`;
  return `<div class="krok k-fiol" id="sek-prawnik-oferty"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>Wynik dla klienta</h3><span class="stan">${Object.keys(d).length ? "przygotowano" : "do zrobienia"}</span></div><div class="tresc">
    <p class="opis">Raport (zgodność ofert, ranking, rynkowość cen – bez AI), opinia prawna z ustaleń${wyk ? " i projekt odwołania do KIO (zarzuty, żądania, uzasadnienie, termin z art. 515)" : ""}. Miejsca do uzupełnienia – na żółto.</p>
    <div class="pasek" style="flex-wrap:wrap">${poz("raport", "Raport z badania ofert")}${poz("opinia", "Opinia prawna")}${wyk ? poz("odwolanie", "Projekt odwołania do KIO") : ""}</div></div></div>`;
}
async function prOfDok(co) { sledz(await bezpiecznie(() => api(`/api/projekty/${OC_ID}/ocena/prawnik/${co}`, {json: {}})), () => otworzOcene(OC_ID)); }

// Księgowość: przycisk w menu dla osób z uprawnieniem (administrator nadaje moduł „Księgowość” w rolach)
setInterval(() => { const bw = document.querySelector('#nav [data-w="windykacja"]'); if (bw && typeof JA !== "undefined" && JA) bw.style.display = JA.windykacja ? "" : "none"; }, 1500);
setInterval(() => { for (const m of ["ksiegowosc", "odwolania", "leady"]) { const b = document.querySelector(`#nav [data-w="${m}"]`); if (b && typeof JA !== "undefined" && JA) b.style.display = (m === "ksiegowosc" ? JA.ksiegowosc : WLASC()) ? "" : "none"; } }, 1500);


// ================================================================ ODWOŁANIA OD PRZETARGÓW
let ODPRZ = null, ODPRZ_FILTR = "mozliwe", ODPRZ_OTW = null;
const ODPRZ_KOL = {"silny": "#dc2626", "średni": "#d97706", "do sprawdzenia": "#64748b"};
async function ladujOdwolania() { ODPRZ = await bezpiecznie(() => api("/api/odw/stan")); if (ODPRZ) rysujOdwolania(); }
function rysujOdwolania() {
  const L = ODPRZ.postepowania || [], lc = ODPRZ.liczniki || {};
  const filtry = {mozliwe: ["Możliwe do podważenia", r => r.status === "możliwy do podważenia"], sprawdz: ["Do sprawdzenia", r => r.status === "do sprawdzenia"],
    czeka: ["Czekają na rozstrzygnięcie", r => ["obserwowany", "czeka na wybór oferty", "czeka na informację z otwarcia ofert"].includes(r.status)],
    wszystkie: ["Wszystkie", r => r.status !== "ukryty"]};
  const lista = L.filter(filtry[ODPRZ_FILTR][1]);
  const pln = v => v == null ? "–" : liczba(v, 0) + " zł";
  const dni = r => { const t = ((r.ocena || []).map(o => o.termin_odwolania).filter(Boolean).sort().find(x => x >= new Date().toISOString().slice(0, 10))) || ((r.ocena || [])[0] || {}).termin_odwolania;
    const d = t ? `<br><small class="opis">${esc(dataPl(t))}</small>` : "";
    return r.dni_do_terminu == null ? "–" : r.dni_do_terminu < 0 ? `<span class="opis">minął</span>${d}` :
    `<b style="color:${r.dni_do_terminu <= 1 ? "#dc2626" : r.dni_do_terminu <= 3 ? "#d97706" : "inherit"}">${r.dni_do_terminu === 0 ? "dziś" : r.dni_do_terminu + " " + (r.dni_do_terminu === 1 ? "dzień" : "dni")}</b>${d}`; };
  const otw = ODPRZ_OTW && L.find(r => r.numer === ODPRZ_OTW);
  if (otw) { $("#odwolania").innerHTML = odwWidokPrzetargu(otw); wstawIkony($("#odwolania")); return; }
  $("#odwolania").innerHTML = `
    <div class="ramka-uwaga" style="margin-top:0">Moduł wyszukuje rozstrzygnięte przetargi z co najmniej dwiema ofertami i wskazuje argumenty za podważeniem wyboru – z podstawą prawną
      i firmą, która ma interes we wniesieniu odwołania (art. 505 Pzp). Termin odwołania od wyboru (art. 515 ust. 1 Pzp): poniżej progów unijnych 5 dni od przekazania informacji o wyborze środkami komunikacji elektronicznej, 10 dni – w inny sposób; od progów unijnych 10 / 15 dni. Reżim i datę przekazania możesz ustawić ręcznie w szczegółach postępowania. Źródła: Platforma e-Zamówienia i platformy zakupowe (bez BIP, bez Bazy Konkurencyjności).
      Wyniki to wstępna ocena z dokumentów publicznych – do weryfikacji.</div>
    ${(() => { const w = ODPRZ.ustawienia.wyszukiwanie || {}, rz = ODPRZ.rodzaje || {}, woj = ODPRZ.wojewodztwa || [];
      return `<div class="karta" style="margin:8px 0">
      <h3 style="margin-top:0">Wyszukiwanie</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
        <label class="ks-pole">Region<select id="odw-region" onchange="document.getElementById('odw-woj').style.display = this.value === 'wojewodztwa' ? '' : 'none'">
          <option value="jak_przetargi" ${w.region === "jak_przetargi" ? "selected" : ""}>jak w wyszukiwarce przetargów (${esc(ODPRZ.region || "")})</option>
          <option value="wojewodztwa" ${w.region === "wojewodztwa" ? "selected" : ""}>wybrane województwa</option>
          <option value="polska" ${w.region === "polska" ? "selected" : ""}>cała Polska</option></select></label>
        <div class="ks-pole"><span>Rodzaj zamówienia</span><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:6px">
          ${Object.entries(rz).map(([k, t]) => `<label style="display:flex;gap:4px;align-items:center"><input type="checkbox" class="odw-rodz" value="${k}" ${(w.rodzaje || []).includes(k) ? "checked" : ""}>${esc(t)}</label>`).join("")}</div></div>
        <label class="ks-pole">Słowa w przedmiocie (opcjonalnie, po przecinku)<input id="odw-slowa" value="${esc(w.slowa || "")}" placeholder="np. droga, oczyszczalnia, sprzątanie"></label>
        <label class="ks-pole">Rozstrzygane do … dni po terminie ofert<input id="odw-dni" type="number" min="1" max="90" value="${w.dni || 45}"></label>
        <label class="ks-pole">Próg wartości [zł]<input id="odw-prog" type="number" value="${ODPRZ.ustawienia.prog}"></label></div>
      <div id="odw-woj" style="display:${w.region === "wojewodztwa" ? "" : "none"};margin-top:8px"><span class="opis">Województwa:</span>
        <div style="display:flex;gap:6px 14px;flex-wrap:wrap;margin-top:4px">${woj.map(x => `<label style="display:flex;gap:4px;align-items:center"><input type="checkbox" class="odw-wojx" value="${esc(x)}" ${(w.wojewodztwa || []).includes(x) ? "checked" : ""}>${esc(x)}</label>`).join("")}</div></div>
      <div class="pasek" style="flex-wrap:wrap;align-items:center;margin-top:10px">
        <button class="glowny" data-ik="szukaj" onclick="odwSzukaj()">Szukaj</button>
        <span class="opis" style="margin:0">ostatnie sprawdzenie: ${esc((ODPRZ.stan || {}).ostatnie || "jeszcze nie")} · automatycznie o 7:00 i 14:00${ODPRZ.poza_filtrem ? ` · ${ODPRZ.poza_filtrem} obserwowanych poza obecnymi filtrami (ukryte)` : ""}</span></div>
      ${w.region === "polska" ? '<p class="opis" style="margin:6px 0 0">Cała Polska: dużo postępowań – program sprawdza je rotacyjnie (do 400 na raz, najpierw sprawdzane najdawniej), więc pełny przegląd może zająć kilka sprawdzeń.</p>' : ""}
    </div>`; })()}
    ${(() => { const n = ODPRZ.ustawienia.nadawca || {}, brak = ["nazwa", "osoba", "email"].some(k => !n[k]);
      return `<details class="karta" ${brak ? "open" : ""} style="margin:6px 0"><summary><b>Twoje dane (nadawca wniosków i wiadomości)</b>${brak ? ' – <span style="background:var(--zolty-jasny)">uzupełnij</span>' : ""}</summary>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px 12px;margin-top:6px">
        ${[["nazwa", "Firma / nazwa"], ["osoba", "Imię i nazwisko"], ["adres", "Adres"], ["email", "E-mail"], ["telefon", "Telefon"]].map(([k, t]) =>
          `<label class="ks-pole">${t}<input id="odw-n-${k}" value="${esc(n[k] || "")}" ${n[k] ? "" : 'style="background:var(--zolty-jasny)"'}></label>`).join("")}</div>
      <button class="maly" style="margin-top:6px" onclick="odwNadawca()">Zapisz dane</button></details>`; })()}
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;margin:6px 0 12px">
      <label class="ks-pole" style="flex:1;min-width:260px">Dodaj postępowanie z linku (Platforma e-Zamówienia albo platforma zakupowa)<input id="odw-link" type="url" placeholder="https://…"></label>
      <button data-ik="plus" onclick="odwDodaj()">Dodaj i sprawdź</button></div>
    <div class="pasek" style="flex-wrap:wrap">${Object.entries(filtry).map(([k, [t, f]]) => `<button class="${ODPRZ_FILTR === k ? "glowny" : ""}" onclick="ODPRZ_FILTR='${k}'; rysujOdwolania()">${t} (${L.filter(f).length})</button>`).join("")}</div>
    ${lista.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Termin odwołania</th><th>Postępowanie</th><th>Wartość</th><th>Oferty</th><th>Siła</th><th>Status</th></tr>
      ${lista.map(r => { const o = (r.ocena || [])[0] || {}; return `<tr style="cursor:pointer" onclick="ODPRZ_OTW = ${jsa(r.numer)}; rysujOdwolania(); window.scrollTo(0, 0)">
        <td>${dni(r)}</td><td><b>${esc(r.przedmiot || "")}</b><br><small class="opis">${esc(r.zamawiajacy || "")} · ${esc(r.numer)}${r.rodzaj_przedmiotu ? " · " + esc((ODPRZ.rodzaje || {})[r.rodzaj_przedmiotu] || r.rodzaj_przedmiotu) : ""}${r.wojewodztwo ? " · " + esc(r.wojewodztwo) : ""}</small></td>
        <td class="liczba">${pln(o.wartosc)}</td><td class="liczba">${o.liczba_ofert ?? "–"}</td>
        <td>${r.sila ? `<b style="color:${ODPRZ_KOL[r.sila]}">${esc(r.sila)}</b>` : ""}</td><td>${esc(r.status || "")}${r.blad ? `<br><small class="czerwone">${esc(r.blad)}</small>` : ""}</td></tr>
`; }).join("")}</table></div>`
      : `<p class="opis">Brak postępowań w tej grupie. ${L.length ? "" : "Kliknij „Szukaj”, żeby dopisać przetargi z regionu po terminie składania ofert."}</p>`}`;
  wstawIkony($("#odwolania"));
}
const ODW_ETAPY = {CollectingOffers: "składanie ofert", ExaminationOffer: "badanie i ocena ofert", ExaminationOffers: "badanie i ocena ofert", CompletedContract: "umowa zawarta", CompletedInvalid: "unieważnione"};
function odwInfo(r) {
  const ez = r.ez || {}, dokAll = r.dokumenty || [], pl = (r.platformy || [])[0];
  const gdzie = r.ocds && ez.na_platformie !== false ? `<a href="https://ezamowienia.gov.pl/mp-client/search/list/${esc(r.ocds)}" target="_blank" rel="noopener">Platforma e-Zamówienia</a>`
    : pl ? `<a href="${esc(pl)}" target="_blank" rel="noopener">${esc(pl.split("/")[2] || pl)}</a>` : "brak adresu platformy w ogłoszeniu";
  return `<div class="karta" style="margin:4px 0 10px;padding:10px 12px">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:4px 16px;font-size:14px">
      <div><span class="opis">Przedmiot</span><br><b>${esc(r.przedmiot || "")}</b></div>
      <div><span class="opis">Zamawiający</span><br>${esc(r.zamawiajacy || "")}${r.miasto ? ", " + esc(r.miasto) : ""}${r.wojewodztwo ? " (" + esc(r.wojewodztwo) + ")" : ""}</div>
      <div><span class="opis">Ogłoszenie · rodzaj</span><br>${esc(r.numer)}${r.rodzaj_przedmiotu ? " · " + esc((ODPRZ.rodzaje || {})[r.rodzaj_przedmiotu] || r.rodzaj_przedmiotu) : ""}</div>
      <div><span class="opis">Termin składania ofert</span><br>${esc(dataPl(String(r.termin_ofert || "–").slice(0, 16)))}</div>
      <div><span class="opis">Etap (e-Zamówienia)</span><br>${esc(ODW_ETAPY[ez.etap] || ez.etap || "–")}${ez.na_platformie === false ? ' <small class="opis">(postępowanie prowadzone na innej platformie – etap może nie być aktualizowany)</small>' : ""}</div>
      <div><span class="opis">Prowadzone na</span><br>${gdzie}</div>
      <div><span class="opis">Kwota przeznaczona</span><br>${ez.kwota ? liczba(ez.kwota, 2) + " zł" : "jeszcze nieopublikowana"}</div>
      <div><span class="opis">Dokumenty</span><br>${dokAll.length} znalezionych${dokAll.filter(d => d.rodzaj).length ? ", w tym rozstrzygnięcia: " + [...new Set(dokAll.filter(d => d.rodzaj).map(d => ({otwarcie: "informacja z otwarcia ofert", wybor: "informacja o wyborze", kwota: "kwota przeznaczona", uniewaznienie: "unieważnienie"})[d.rodzaj] || d.rodzaj))].map(esc).join(", ") : ""}</div>
    </div>
    <p class="opis" style="margin:6px 0 0">Status: <b>${esc(r.status || "")}</b>${r.sprawdzono ? " · sprawdzono " + esc(r.sprawdzono) : " · jeszcze nie sprawdzano"}</p>
    ${r.blad_platformy ? `<p style="margin:4px 0 0;background:var(--zolty-jasny);padding:4px 8px;border-radius:4px">${esc(r.blad_platformy)}</p>` : ""}
    ${r.blad ? `<p class="czerwone" style="margin:4px 0 0">${esc(r.blad)}</p>` : ""}</div>`;
}
function odwRezim(r) {  // reżim postępowania (progi UE) – automat albo ręczny przełącznik; wpływa na termin odwołania i związania ofertą
  const z = r.rezim || {}, rc = z.reczne === true ? "tak" : z.reczne === false ? "nie" : "auto";
  return `<div class="karta" style="margin:0 0 10px;padding:8px 12px" onclick="event.stopPropagation()">
    <label class="ks-pole" style="max-width:640px">Wartość zamówienia a progi unijne (termin odwołania – art. 515 ust. 1 Pzp; związanie ofertą – art. 220 / art. 307)
      <select id="odw-rezim" onchange="odwParam(${jsa(r.numer)}, {unijne: this.value === 'auto' ? 'auto' : this.value === 'tak'})">
        <option value="auto" ${rc === "auto" ? "selected" : ""}>automatycznie – ${z.auto ? "równa lub przekracza progi UE" : "poniżej progów UE"}</option>
        <option value="nie" ${rc === "nie" ? "selected" : ""}>poniżej progów UE (ręcznie)</option>
        <option value="tak" ${rc === "tak" ? "selected" : ""} title="postępowanie o wartości równej lub przekraczającej progi UE">równa lub przekracza progi UE (ręcznie)</option></select></label>
    <small class="opis">Obecnie: ${esc(z.opis || "")}${!z.reczne && z.reczne !== false && /nieznany/.test(z.opis || "") ? ' – <b style="background:var(--zolty-jasny)">sprawdź w ogłoszeniu (Dz.U. UE / BZP) i ustaw ręcznie</b>' : ""}</small></div>`;
}
function odwTerminCzesci(r, o, ci) {  // dzień i sposób przekazania informacji o wyborze (art. 515 ust. 1 lit. a / b Pzp)
  const U = o.unijne, sp = o.sposob_przekazania || "elektronicznie";
  return `<div class="pasek" style="flex-wrap:wrap;align-items:flex-end;margin:2px 0 8px" onclick="event.stopPropagation()">
    <label class="ks-pole" style="min-width:170px">Data przekazania informacji o wyborze<input type="date" id="odw-dp-${ci}" value="${esc(o.data_przekazania || "")}" ${o.data_przekazania ? "" : 'style="background:var(--zolty-jasny)"'}></label>
    <label class="ks-pole" style="min-width:230px">Sposób przekazania<select id="odw-sp-${ci}">
      <option value="elektronicznie" ${sp === "elektronicznie" ? "selected" : ""}>środki komunikacji elektronicznej (${U ? 10 : 5} dni)</option>
      <option value="inny" ${sp === "inny" ? "selected" : ""}>inny sposób, np. pocztą (${U ? 15 : 10} dni)</option></select></label>
    <button class="maly" onclick="odwParam(${jsa(r.numer)}, {czesc: ${ci}, data_przekazania: $('#odw-dp-${ci}').value, sposob: $('#odw-sp-${ci}').value})">Przelicz termin</button>
    ${o.data_przekazania ? `<button class="maly" onclick="odwParam(${jsa(r.numer)}, {czesc: ${ci}})">Od daty z dokumentu</button>` : ""}</div>`;
}
async function odwParam(numer, zm) {
  if (await bezpiecznie(() => api("/api/odw/parametry", {json: Object.assign({numer}, zm)}))) { komunikat("Przeliczono termin odwołania."); ladujOdwolania(); }
}
function odwSzczegoly(r) {
  const czesci = r.ocena || [];
  const dok = (r.dokumenty || []).filter(d => d.rodzaj);
  return `${odwInfo(r)}${odwRezim(r)}${czesci.map((o, ci) => `<div style="margin:6px 0 14px">
      ${czesci.length > 1 ? `<h4 style="margin:0 0 6px">Część ${esc(o.czesc || "")}</h4>` : ""}
      ${o.wybrany ? `<p style="margin:0 0 6px">Wybrana oferta: <b>${esc(o.wybrany.wykonawca || "")}</b> – ${o.wybrany.cena_brutto ? liczba(o.wybrany.cena_brutto, 2) + " zł" : ""}
        ${o.termin_odwolania ? ` · termin odwołania: <b>${esc(dataPl(o.termin_odwolania))}</b> (${esc(o.opis_terminu || `${o.unijne ? "10" : "5"} dni od przekazania informacji o wyborze, art. 515 ust. 1 pkt ${o.unijne ? "1" : "2"} lit. a Pzp`)};
          ${o.data_przekazania ? "liczony od " + esc(dataPl(o.data_przekazania)) : `liczony od daty informacji o wyborze${o.data_informacji ? " z " + esc(dataPl(o.data_informacji)) : ""} – <b>sprawdź datę i sposób przekazania</b>`})` : ""}</p>
        ${odwTerminCzesci(r, o, ci)}` : `<p class="opis">${esc(o.status || "")}</p>`}
      ${(o.argumenty || []).length ? `<ul class="lista">${o.argumenty.map(a => `<li><b style="color:${ODPRZ_KOL[a.sila]}">${esc(a.sila)}</b> · <b>${esc(a.typ)}</b>${a.dwa_wyliczenia ? ' <span class="znacznik" style="background:var(--zolty-jasny)">dwa wyliczenia – podstawa odrzucenia niepewna</span>' : ""} – ${esc(a.opis)}
          <br><small class="opis">Podstawa: ${esc(a.podstawa)} · interes we wniesieniu odwołania: ${esc(a.interes || "")}</small></li>`).join("")}</ul>` : ""}
      ${(o.oferenci || []).length ? `<h4 style="margin:12px 0 4px">Oferenci (${o.oferenci.length})</h4><div class="tabela-okno"><table class="tabela">
        <tr><th>Miejsce / status</th><th>Wykonawca</th><th>NIP · KRS · REGON</th><th>Adres · VAT</th><th>Cena · punkty</th><th>Kontakt</th><th></th></tr>
        ${o.oferenci.map(f => { const k = f.rejestr || {}, fi = (o.firmy || []).find(x => x.wykonawca === f.wykonawca);
          const em = [...new Set([k.email, ...(k.emaile_strona || [])].filter(Boolean))], tel = [...new Set([k.telefon, ...(k.telefony_strona || [])].filter(Boolean))];
          return `<tr><td><b>${esc(f.status)}</b>${fi && fi.priorytet ? `<br><small class="opis">${esc(fi.priorytet)}</small>` : ""}${f.odrzucona && f.odrzucona !== true ? `<br><small class="opis">${esc(f.odrzucona)}</small>` : ""}</td>
            <td><b>${esc(f.wykonawca)}</b>${(k.reprezentanci || []).length ? `<br><small class="opis">reprezentacja: ${esc(k.reprezentanci.join(", "))}</small>` : ""}</td>
            <td>${esc(f.nip || "–")}${k.krs ? `<br><small>KRS ${esc(k.krs)}</small>` : ""}${k.regon ? `<br><small>REGON ${esc(k.regon)}</small>` : ""}</td>
            <td>${esc(k.adres || f.adres || "")}${k.status_vat ? `<br><small class="opis">${esc(k.status_vat)}</small>` : ""}</td>
            <td class="liczba">${f.cena_brutto ? liczba(f.cena_brutto, 2) + " zł" : "–"}${f.suma != null ? `<br><small>${esc(String(f.suma))} pkt</small>` : ""}</td>
            <td>${em.map(e => `<span style="user-select:all">${esc(e)}</span>`).join("<br>")}${tel.length ? (em.length ? "<br>" : "") + tel.map(t => `<a href="tel:${esc(t)}">${esc(t)}</a>`).join("<br>") : ""}
              ${k.www ? `<br><a href="${esc(k.www.startsWith("http") ? k.www : "https://" + k.www)}" target="_blank" rel="noopener">${esc(k.www)}</a>` : ""}${k.ade ? `<br><small class="opis">e-Doręczenia: ${esc(k.ade)}</small>` : ""}
              ${!em.length && !tel.length && !k.www ? `<small class="opis">${f.nip ? "brak w rejestrach – sprawdź w ofercie (po wniosku)" : "brak NIP w dokumentach"}</small>` : ""}</td>
            <td style="white-space:nowrap" onclick="event.stopPropagation()">${f.status !== "wybrana" ? `<button class="maly" title="Projekt neutralnego tekstu informacyjnego – program niczego nie wysyła" onclick="odwEmail(${jsa(r.numer)}, ${ci}, ${jsa(f.wykonawca)})">Projekt tekstu</button>
              <button class="maly" data-ik="iskra" onclick="odwOdwolanie(${jsa(r.numer)}, ${ci}, ${jsa(f.wykonawca)})">Odwołanie</button>
              ${((r.pisma || {})[`odwolanie|${ci}|${f.wykonawca}`]) ? `<a class="przycisk zielony maly" href="/api/odw/plik/${encodeURIComponent(r.katalog || "")}/${encodeURIComponent(r.pisma[`odwolanie|${ci}|${f.wykonawca}`].plik)}">Pobierz</a>` : ""}
              <button class="maly" onclick="odwBadanie(${jsa(r.numer)}, ${ci}, ${jsa(f.wykonawca)})">Badanie</button>` : ""}</td></tr>`; }).join("")}</table></div>
        <p class="opis">Dane z rejestrów: biała lista VAT, KRS (strona www, e-mail, e-Doręczenia), CEIDG – e-mail i telefon jednoosobowych działalności (gdy w Ustawieniach jest token CEIDG) – oraz kontakt ze strony www firmy. Program przygotowuje wyłącznie projekty tekstu – niczego nie wysyła (bez wysyłki masowej i automatycznej). Informacja handlowa e-mailem, SMS-em lub telefonicznie wymaga uprzedniej zgody adresata (art. 398 Prawa komunikacji elektronicznej); RODO – art. 14 i 21; radca prawny i adwokat – zasady etyki dotyczące pozyskiwania klientów.</p>
        <div id="odw-email-${ci}" onclick="event.stopPropagation()"></div>` : ""}
      ${o.wybrany ? `<div class="pasek" onclick="event.stopPropagation()" style="flex-wrap:wrap">
        <button class="maly" onclick="odwDok(${jsa(r.numer)}, ${ci}, 'wniosek')">Wniosek o udostępnienie oferty i protokołu (Word)</button>
        <button class="maly" onclick="odwDok(${jsa(r.numer)}, ${ci}, 'notatka')">Notatka o możliwości podważenia (Word)</button></div>` : ""}
    </div>`).join("") || `<p class="opis">Program sprawdza dokumenty postępowania dwa razy dziennie – gdy zamawiający opublikuje informację z otwarcia ofert i o wyborze, pojawi się tu ocena.</p>`}
    ${dok.length ? `<p class="opis" style="margin:4px 0">Dokumenty rozstrzygnięcia: ${dok.map(d => d.plik ? `<a href="/api/odw/plik/${encodeURIComponent(r.katalog || "")}/${encodeURIComponent(d.plik)}">${esc(d.nazwa)}</a>` : esc(d.nazwa)).join(" · ")}</p>` : ""}
    <div class="pasek"><button class="maly" data-ik="odswiez" onclick="event.stopPropagation(); odwSprawdz(${jsa(r.numer)})">Sprawdź ponownie</button>
      ${r.link ? `<a class="przycisk maly" href="${esc(r.link)}" target="_blank" rel="noopener">Ogłoszenie</a>` : ""}
      <button class="maly" onclick="event.stopPropagation(); odwUkryj(${jsa(r.numer)})">Ukryj</button></div>`;
}
async function odwSprawdz(numer) { sledz(await bezpiecznie(() => api("/api/odw/sprawdz", {json: numer ? {numer} : {}})), ladujOdwolania); }
async function odwDodaj() {
  const url = ($("#odw-link").value || "").trim(); if (!/^https?:\/\//i.test(url)) return komunikat("Wklej pełny adres postępowania (https://…).", true);
  sledz(await bezpiecznie(() => api("/api/odw/dodaj", {json: {url}})), () => { ODPRZ_FILTR = "wszystkie"; ladujOdwolania(); });
}
async function odwUkryj(numer) { if (await bezpiecznie(() => api("/api/odw/ukryj", {json: {numer}}))) ladujOdwolania(); }
async function odwProg(v) { if (await bezpiecznie(() => api("/api/odw/ustawienia", {json: {prog: v}}))) { komunikat("Zapisano próg wartości."); ladujOdwolania(); } }

async function odwNadawca() {
  const n = {}; for (const k of ["nazwa", "osoba", "adres", "email", "telefon"]) n[k] = $("#odw-n-" + k).value;
  if (await bezpiecznie(() => api("/api/odw/ustawienia", {json: {nadawca: n}}))) { komunikat("Zapisano Twoje dane."); ladujOdwolania(); }
}
async function odwDok(numer, czesc, rodzaj) { const w = await bezpiecznie(() => api("/api/odw/dokument", {json: {numer, czesc, rodzaj}})); if (w) location.href = w.url; }
async function odwOdwolanie(numer, czesc, firma) {
  if (!confirm(`Przygotować projekt odwołania dla: ${firma}? (AI, ok. 1–2 min)`)) return;
  sledz(await bezpiecznie(() => api("/api/odw/dokument", {json: {numer, czesc, rodzaj: "odwolanie", firma}})), ladujOdwolania);
}
async function odwBadanie(numer, czesc, firma) {
  const w = await bezpiecznie(() => api("/api/odw/badanie", {json: {numer, czesc, firma}}));
  if (w) { komunikat("Założono badanie ofert – wgraj tam ofertę wybranego wykonawcy (z wniosku o udostępnienie) i SWZ."); pokaz("pr_oferty"); setTimeout(() => otworzOcene(w.id), 600); }
}
async function odwEmail(numer, czesc, firma, email) {  // tylko PROJEKT tekstu do skopiowania – bez wysyłki z programu (art. 398 PKE, RODO, etyka zawodowa)
  const w = await bezpiecznie(() => api("/api/odw/email", {json: {numer, czesc, firma, email: email || ""}})); if (!w) return;
  const el = $(`#odw-email-${czesc}`);
  el.innerHTML = `<div class="karta" style="margin-top:8px"><b>Projekt wiadomości do: ${esc(firma)}</b>
    <div class="ramka-uwaga" role="alert" style="margin:6px 0;border-left:4px solid #dc2626"><b>Uwaga – zgoda adresata.</b> ${esc(w.ostrzezenie || "Program niczego nie wysyła.")}</div>
    <div class="pasek" style="flex-wrap:wrap;align-items:flex-end"><label class="ks-pole" style="flex:1;min-width:240px">Adres e-mail firmy (do Twojej wiadomości – sprawdź ręcznie)
      <input id="odw-em-adr" value="${esc(w.email || "")}"></label>
      <button class="maly" onclick="odwEmail(${jsa(numer)}, ${czesc}, ${jsa(firma)}, $('#odw-em-adr').value)">Zapisz adres</button></div>
    <label class="ks-pole">Temat<input id="odw-em-temat" value="${esc(w.temat)}"></label>
    <label class="ks-pole">Treść (informacyjna, bez propozycji usług)<textarea id="odw-em-tresc" rows="14">${esc(w.tresc)}</textarea></label>
    <div class="pasek"><button class="maly" onclick="navigator.clipboard.writeText($('#odw-em-temat').value + '\\n\\n' + $('#odw-em-tresc').value); komunikat('Skopiowano projekt tekstu.')">Kopiuj tekst</button>
      <button class="maly" onclick="$('#odw-email-${czesc}').innerHTML=''">Zamknij</button></div></div>`;
}

async function odwSzukaj() {
  const w = {region: $("#odw-region").value, wojewodztwa: [...document.querySelectorAll(".odw-wojx:checked")].map(x => x.value),
    rodzaje: [...document.querySelectorAll(".odw-rodz:checked")].map(x => x.value), slowa: $("#odw-slowa").value, dni: $("#odw-dni").value};
  if (!w.rodzaje.length) return komunikat("Zaznacz co najmniej jeden rodzaj zamówienia.", true);
  if (await bezpiecznie(() => api("/api/odw/ustawienia", {json: {wyszukiwanie: w, prog: $("#odw-prog").value}}))) odwSprawdz();
}

async function kontoKsiegowosc(login, dostep) {
  if (await bezpiecznie(() => api("/api/uzytkownicy/ksiegowosc", {json: {login, dostep}}))) komunikat(dostep ? `Udostępniono Księgowość: ${login}.` : `Odebrano dostęp do Księgowości: ${login} (dane konta zostają).`);
  else ladujKonta();
}

function odwWidokPrzetargu(r) {
  const dok = r.dokumenty || [], kat = encodeURIComponent(r.katalog || "");
  const link = d => d.plik ? `/api/odw/plik/${kat}/${encodeURIComponent(d.plik)}` : d.url;
  const RODZ = {otwarcie: "informacja z otwarcia ofert", wybor: "informacja o wyborze", kwota: "kwota przeznaczona", uniewaznienie: "unieważnienie"};
  return `<div class="pasek" style="flex-wrap:wrap;margin:0 0 10px">
      <button data-ik="cofnij" onclick="ODPRZ_OTW = null; rysujOdwolania()">Lista przetargów</button>
      <button class="glowny" data-ik="iskra" onclick="odwAnalizuj(${jsa(r.numer)})">Analizuj ponownie</button>
      <button data-ik="odswiez" onclick="odwSprawdz(${jsa(r.numer)})">Sprawdź nowe dokumenty</button>
      ${r.link ? `<a class="przycisk" href="${esc(r.link)}" target="_blank" rel="noopener">Ogłoszenie</a>` : ""}
      <button class="maly" onclick="odwUkryj(${jsa(r.numer)}); ODPRZ_OTW = null">Ukryj</button></div>
    <h2 style="margin:0 0 6px">${esc(r.przedmiot || "")}</h2>
    ${odwSzczegoly(r).replace(/<div class="pasek"><button class="maly" data-ik="odswiez"[\s\S]*$/, "")}
    <div class="karta" style="margin-top:10px"><h3 style="margin-top:0">Dokumenty postępowania (${dok.length})</h3>
      ${dok.length ? `<ul class="lista">${dok.map(d => `<li><a href="${esc(link(d))}" target="_blank" rel="noopener">${esc(d.nazwa || "dokument")}</a>
          ${d.rodzaj ? ` <span class="znacznik z-startujemy">${esc(RODZ[d.rodzaj] || d.rodzaj)}</span>` : ""}${d.plik ? ' <small class="opis">pobrany</small>' : ""}</li>`).join("")}</ul>`
        : `<p class="opis">Program nie znalazł jeszcze dokumentów tego postępowania${r.blad_platformy ? " – " + esc(r.blad_platformy) : ""}. Jeśli znasz adres strony postępowania na platformie, wklej go w „Dodaj postępowanie z linku” na liście.</p>`}</div>`;
}
async function odwAnalizuj(numer) {
  if (!confirm("Odczytać ponownie dokumenty rozstrzygnięcia (AI) i przeliczyć ocenę?")) return;
  sledz(await bezpiecznie(() => api("/api/odw/sprawdz", {json: {numer, od_nowa: true}})), ladujOdwolania);
}

// ================================================================ KALKULATOR KOSZTÓW PRACY (usługi pracochłonne)
let KALKP = {od: "", osoby: 1, miesiace: 12, brutto: "", godziny_mies: 168, nocne_proc: 0, wypadkowa: 1.67, ppk: false, ppk_dodatkowa: 0, zastepstwa_proc: 10, absencje_proc: 3,
  absencje_metoda: "procent", dni_choroby_rok: 10, pracownicy_50: false, zwolnienie_fp: "", osoby_zwolnione: "",
  inne_os_mies: 0, materialy_proc: 0, ogolne_proc: 10, zysk_proc: 5, vat: 23, cena_oferty_brutto: "", tytul: ""}, KALKW = null;
// H3-03: zwolnienia z FP i FGŚP (ustawa o rynku pracy i służbach zatrudnienia art. 261–263; ustawa o ochronie roszczeń pracowniczych art. 9a–9c)
const KALK_ZWOLNIENIA = [["", "brak zwolnienia"], ["wiek", "kobieta 55+ / mężczyzna 60+ (bez limitu czasu)"], ["urlop", "powrót z urlopu macierzyńskiego / rodzicielskiego / wychowawczego – 36 mies."],
  ["do30", "bezrobotny do 30 r.ż. skierowany przez urząd pracy – 12 mies."], ["bezrobotny50", "50+ zarejestrowany jako bezrobotny – 12 mies."]];
const KALK_POLA = [["osoby", "Liczba etatów (osób na pełen etat)"], ["miesiace", "Okres umowy [mies.]"], ["brutto", "Wynagrodzenie brutto na etat [zł] (puste = minimalne w okresie umowy)"],
  ["godziny_mies", "Godziny na etat w miesiącu (ponad 168 = nadgodziny)"], ["nocne_proc", "Praca w porze nocnej [% godzin]"], ["wypadkowa", "Składka wypadkowa [%]"],
  ["zastepstwa_proc", "Zastępstwa urlopowe [% kosztu]"], ["absencje_proc", "Absencje chorobowe [% kosztu]"], ["inne_os_mies", "Odzież, BHP, badania, szkolenia [zł/os./mies.]"],
  ["materialy_proc", "Materiały / środki / paliwo [% kosztów pracy]"], ["ogolne_proc", "Koszty ogólne [%]"], ["zysk_proc", "Zysk [%]"], ["vat", "VAT [%]"],
  ["cena_oferty_brutto", "Cena oferty brutto do porównania [zł] (opcjonalnie)"]];
function rysujKalkPracy() {
  const w = KALKW;  // kwoty jak w całym programie: „4 950,00 zł” (dotąd „4 950 zł” – bez groszy)
  $("#kalk-pracy").innerHTML = `<div class="ramka-uwaga" style="margin-top:0">Minimalny koszt usługi pracochłonnej przy umowie o pracę – płaca minimalna obowiązująca w okresie umowy
      (rozporządzenia Rady Ministrów; przy umowie przechodzącej na kolejny rok – średnia z miesięcy), składki pracodawcy (emerytalna 9,76%, rentowa 6,5%, wypadkowa, FP 2,45%, FGŚP 0,1%,
      PPK 1,5% opcjonalnie), dodatek nocny 20% stawki z minimalnego wynagrodzenia (art. 151⁸ KP), godziny ponad 168 h – z dodatkiem 50% (art. 151¹ KP).
      Dla wykonawcy – kalkulacja oferty i wyjaśnienia ceny; dla zamawiającego – szacowanie wartości i ocena rażąco niskiej ceny (art. 224 ust. 3 pkt 4 Pzp).</div>
    <div class="karta"><label class="ks-pole">Czego dotyczy (opcjonalnie)<input id="kp-tytul" value="${esc(KALKP.tytul || "")}" placeholder="np. Sprzątanie budynków Urzędu Gminy, 2027"></label>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px 14px;margin-top:6px">
      <label class="ks-pole">Początek umowy (puste = dziś)<input id="kp-od" type="date" value="${esc(KALKP.od || "")}"></label>
      ${KALK_POLA.map(([k, t]) => `<label class="ks-pole">${t}<input id="kp-${k}" type="number" step="0.01" value="${esc(String(KALKP[k] ?? ""))}"></label>`).join("")}
      <label class="ks-pole" style="flex-direction:row;align-items:center;gap:6px"><input id="kp-ppk" type="checkbox" ${KALKP.ppk ? "checked" : ""}> PPK – wpłata podstawowa pracodawcy 1,5%</label>
      <label class="ks-pole">PPK – wpłata dodatkowa pracodawcy [%] (0–2,5)<input id="kp-ppk_dodatkowa" type="number" step="0.1" min="0" max="2.5" value="${esc(String(KALKP.ppk_dodatkowa ?? 0))}"></label>
      <label class="ks-pole">Zwolnienie ze składek na FP i FGŚP<select id="kp-zwolnienie_fp">${KALK_ZWOLNIENIA.map(([k, t]) => `<option value="${k}" ${KALKP.zwolnienie_fp === k ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
      <label class="ks-pole">Etaty objęte zwolnieniem (puste = wszystkie)<input id="kp-osoby_zwolnione" type="number" step="0.01" value="${esc(String(KALKP.osoby_zwolnione ?? ""))}"></label>
      <label class="ks-pole">Absencje chorobowe – sposób liczenia<select id="kp-absencje_metoda"><option value="procent" ${KALKP.absencje_metoda !== "chorobowe" ? "selected" : ""}>ryczałt – % kosztu (pole wyżej)</option>
        <option value="chorobowe" ${KALKP.absencje_metoda === "chorobowe" ? "selected" : ""}>wynagrodzenie chorobowe 80% (art. 92 KP)</option></select></label>
      <label class="ks-pole">Dni choroby na etat w roku (przy wynagrodzeniu chorobowym)<input id="kp-dni_choroby_rok" type="number" step="1" value="${esc(String(KALKP.dni_choroby_rok ?? 10))}"></label>
      <label class="ks-pole" style="flex-direction:row;align-items:center;gap:6px"><input id="kp-pracownicy_50" type="checkbox" ${KALKP.pracownicy_50 ? "checked" : ""}> pracownicy po 50. roku życia (pracodawca płaci 14 dni choroby, nie 33)</label></div>
      <p class="opis" style="margin:6px 0 0">Zwolnienie z FP (2,45%) i FGŚP (0,10%) przysługuje tylko za osoby spełniające warunki ustawowe – sprawdź wiek, datę powrotu z urlopu albo skierowanie z urzędu pracy.
        Wynagrodzenie chorobowe: 80% wynagrodzenia po odliczeniu składek pracownika (13,71%) za pierwsze 33 dni choroby w roku (14 dni – pracownik po 50. roku życia), dalej zasiłek z ZUS.</p>
      <div class="pasek" style="margin-top:10px"><button class="glowny" data-ik="kalkulator" onclick="kalkLicz()">Oblicz</button>
        ${w ? `<button onclick="kalkWord()">Wyliczenie (Word)</button>` : ""}</div></div>
    ${w ? `<div class="karta"><h3 style="margin-top:0">Wynik</h3>
      <p class="opis">Okres: ${esc(w.parametry.okres || "")} · płaca minimalna ${zl(w.parametry.placa_minimalna)}${Object.keys(w.parametry.placa_minimalna_lata || {}).length > 1 ? " (średnia: " + Object.entries(w.parametry.placa_minimalna_lata).map(([r, v]) => r + " – " + zl(v)).join(", ") + ")" : ""} · minimalna stawka godzinowa ${zl(w.parametry.stawka_godzinowa_min)}</p>
      <div class="tabela-okno"><table class="tabela"><tr><th>Na etat miesięcznie</th><th class="liczba">Kwota</th></tr>
        ${[["Wynagrodzenie brutto", w.na_etat_mies.wynagrodzenie], ["Dodatek nocny", w.na_etat_mies.dodatek_nocny], ...(w.na_etat_mies.nadgodziny ? [["Godziny nadliczbowe z dodatkiem 50%", w.na_etat_mies.nadgodziny]] : []), ["Składki pracodawcy", w.na_etat_mies.skladki],
          ["Zastępstwa urlopowe", w.na_etat_mies.zastepstwa], ["Absencje chorobowe", w.na_etat_mies.absencje], ["Odzież, BHP, badania, szkolenia", w.na_etat_mies.inne]].map(([t, v]) => `<tr><td>${t}</td><td class="liczba">${zl(v)}</td></tr>`).join("")}
        <tr><td><b>Koszt etatu</b></td><td class="liczba"><b>${zl(w.na_etat_mies.razem)}</b></td></tr></table></div>
      <p>Koszty pracy (${liczba(w.osoby, 2).replace(/,00$/, "")} et. × ${liczba(w.miesiace, 2).replace(/,00$/, "")} mies.): <b>${zl(w.koszty_pracy)}</b> · materiały ${zl(w.materialy)} · koszty ogólne ${zl(w.ogolne)} · zysk ${zl(w.zysk)}</p>
      <p style="font-size:18px">Cena: <b>${zl(w.cena_netto)} netto</b> · <b>${zl(w.cena_brutto)} brutto</b> (VAT ${w.vat}%)</p>
      <p>Minimum (same koszty pracy): ${zl(w.minimum_netto)} netto / ${zl(w.minimum_brutto)} brutto</p>
      ${w.porownanie ? `<p style="padding:8px 10px;border-radius:6px;background:${w.porownanie.pokrycie_proc < 100 ? "#FEE2E2" : w.porownanie.pokrycie_proc < 110 ? "var(--zolty-jasny)" : "#DCFCE7"}">
        Cena oferty ${zl(w.porownanie.cena_oferty_brutto)} pokrywa <b>${w.porownanie.pokrycie_proc}%</b> minimalnych kosztów pracy. ${esc(w.porownanie.ocena)}</p>` : ""}
      ${w.parametry.zwolnienie_fp ? `<p class="opis">Zwolnienie z FP i FGŚP: ${esc(w.parametry.zwolnienie_fp.opis)} – ${liczba(w.parametry.zwolnienie_fp.etaty, 2).replace(/,00$/, "")} et. × ${liczba(w.parametry.zwolnienie_fp.miesiace, 2).replace(/,00$/, "")} mies., oszczędność ${zl(w.parametry.zwolnienie_fp.oszczednosc_razem)} <small>(${esc(w.parametry.zwolnienie_fp.podstawa)})</small></p>` : ""}
      ${w.parametry.chorobowe ? `<p class="opis">${esc(w.parametry.chorobowe.opis)}</p>` : ""}
      ${w.parametry.ppk_dodatkowa ? `<p class="opis">PPK: 1,5% + wpłata dodatkowa ${liczba(w.parametry.ppk_dodatkowa, 1)}%</p>` : ""}
      ${(w.uwagi || []).map(u => `<p class="czerwone">${esc(u)}</p>`).join("")}</div>` : ""}`;
  wstawIkony($("#kalk-pracy"));
}
function kalkZbierz() {
  for (const [k] of KALK_POLA) KALKP[k] = $("#kp-" + k).value; KALKP.od = $("#kp-od").value; KALKP.ppk = $("#kp-ppk").checked; KALKP.tytul = $("#kp-tytul").value;
  for (const k of ["ppk_dodatkowa", "zwolnienie_fp", "osoby_zwolnione", "absencje_metoda", "dni_choroby_rok"]) KALKP[k] = $("#kp-" + k).value;
  KALKP.pracownicy_50 = $("#kp-pracownicy_50").checked; return KALKP;
}
async function kalkLicz() { const w = await bezpiecznie(() => api("/api/kalkulator-pracy", {json: kalkZbierz()})); if (w) { KALKW = w; rysujKalkPracy(); } }
async function kalkWord() { const w = await bezpiecznie(() => api("/api/kalkulator-pracy/word", {json: kalkZbierz()})); if (w) location.href = w.url; }

// ================================================================ LEADY Z PRZETARGÓW (gwarancje, zwycięzcy)
let LEADY = {typ: "wadium", woj: "", rodzaj: "", slowa: "", min: "", dni: 14, dane: null};
async function ladujLeady() {
  const q = new URLSearchParams({typ: LEADY.typ, woj: LEADY.woj, rodzaj: LEADY.rodzaj, slowa: LEADY.slowa, min: LEADY.min, dni: LEADY.dni});
  LEADY.laduje = true; if (LEADY.dane) rysujLeady(); else $("#leady").innerHTML = '<p class="opis">Wczytywanie…</p>';
  const d = await bezpiecznie(() => api("/api/leady?" + q)); LEADY.laduje = false; if (!d) { if (LEADY.dane) rysujLeady(); return; }
  LEADY.dane = d; rysujLeady();
  if (d.uzupelnianie) setTimeout(() => { if (WIDOK === "leady" && LEADY.typ === "wadium") ladujLeady(); }, 60000);
  if (d.zbieranie) setTimeout(() => { if (WIDOK === "leady" && LEADY.typ === "zwyciezcy") ladujLeady(); }, 45000);
}
function rysujLeady() {
  const d = LEADY.dane || {lista: [], wojewodztwa: [], rodzaje: {}}, zl = v => v != null ? liczba(v, 2) + " zł" : "–", wad = LEADY.typ === "wadium";
  const q = new URLSearchParams({typ: LEADY.typ, woj: LEADY.woj, rodzaj: LEADY.rodzaj, slowa: LEADY.slowa, min: LEADY.min, dni: LEADY.dni});
  $("#leady").innerHTML = `<div class="ramka-uwaga" style="margin-top:0">Dla gwarantów i ubezpieczycieli: przetargi z wadium (firmy potrzebują gwarancji wadialnej przed terminem ofert)
      i wybrani wykonawcy przed podpisaniem umowy (zabezpieczenie należytego wykonania – do 5% ceny, art. 452 ust. 2 Pzp; gdy ogłoszenie albo SWZ podaje procent – kwota według niego). Dla podwykonawców i dostawców: kto wygrał, co i za ile – z kontaktami.
      Zwycięzcy: ogłoszenia o wyniku z BZP i o udzieleniu zamówienia z TED z całej Polski (po podpisaniu umowy – dla podwykonawców, dostawców, wynajmu, ubezpieczeń)
      oraz wcześniejszy sygnał „przed umową” z postępowań obserwowanych w module Odwołań (dla gwarantów). Kontakt z firmami: przed wysyłką ofert handlowych sprawdź podstawę prawną (zgoda – art. 398 Prawa komunikacji elektronicznej; RODO).</div>
    <div class="pasek" style="flex-wrap:wrap">${[["wadium", "Gwarancje wadialne – otwarte przetargi"], ["zwyciezcy", "Zwycięzcy – należyte wykonanie, podwykonawstwo"]].map(([k, t]) =>
      `<button class="${LEADY.typ === k ? "glowny" : ""}" onclick="LEADY.typ='${k}'; ladujLeady()">${t}</button>`).join("")}</div>
    <div class="karta" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px 12px;align-items:end">
      <label class="ks-pole">Województwo<select id="ld-woj"><option value="">wszystkie</option>${d.wojewodztwa.map(w => `<option ${w === LEADY.woj ? "selected" : ""}>${esc(w)}</option>`).join("")}</select></label>
      <label class="ks-pole">Rodzaj<select id="ld-rodz"><option value="">wszystkie</option>${Object.entries(d.rodzaje).map(([k, t]) => `<option value="${k}" ${k === LEADY.rodzaj ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
      <label class="ks-pole">Słowa w przedmiocie<input id="ld-slowa" value="${esc(LEADY.slowa)}" placeholder="np. droga, sprzątanie"></label>
      <label class="ks-pole">${wad ? "Wadium od" : "Cena od"} [zł]<input id="ld-min" type="number" value="${esc(LEADY.min)}"></label>
      ${wad ? "" : `<label class="ks-pole">Rozstrzygnięte w ostatnich … dni<input id="ld-dni" type="number" min="1" max="60" value="${esc(String(LEADY.dni))}"></label>`}
      <div class="pasek" style="margin:0"><button class="glowny" data-ik="szukaj" onclick="LEADY.woj=$('#ld-woj').value; LEADY.rodzaj=$('#ld-rodz').value; LEADY.slowa=$('#ld-slowa').value; LEADY.min=$('#ld-min').value; if ($('#ld-dni')) LEADY.dni=$('#ld-dni').value; ladujLeady()">Pokaż</button>
        <a class="przycisk" href="/api/leady.csv?${q}">CSV (Excel)</a></div></div>
    <p class="opis">${LEADY.laduje ? "<b>Wczytywanie…</b> " : ""}${d.lista.length} pozycji${d.lista.length >= 1000 ? " (pierwsze 1000 – zawęź filtry)" : ""}.${!d.lista.length && !LEADY.laduje ? (wad ? " Żaden otwarty przetarg nie spełnia filtrów." : ldDiag(d)) : ""}</p>
    ${!wad && d.zbieranie ? '<p class="uwaga" style="margin:4px 0">Zbieram rozstrzygnięcia z całej Polski z ostatnich 21 dni (BZP i TED) – pierwszy raz trwa to kilka minut; lista sama się odświeży.</p>' : ""}
    ${d.uzupelnianie ? '<p class="uwaga" style="margin:4px 0">Uzupełniam dane o wadium w ogłoszeniach zapisanych przed tą wersją (ostatnie 45 dni) – lista sama się odświeży w ciągu kilku minut.</p>' : ""}
    <div class="tabela-okno"><table class="tabela">${wad
      ? `<tr><th>Wadium</th><th>Przedmiot</th><th>Zamawiający</th><th>Województwo · rodzaj</th><th>Termin ofert</th><th>Zabezp. nal. wyk.</th></tr>
        ${d.lista.map(x => `<tr><td class="liczba"><b>${zl(x.wadium)}</b></td><td>${x.link ? `<a href="${esc(x.link)}" target="_blank" rel="noopener">${esc(x.przedmiot || "")}</a>` : esc(x.przedmiot || "")}<br><small class="opis">${esc(x.numer || "")}</small></td>
          <td>${esc(x.zamawiajacy || "")}</td><td>${esc(x.wojewodztwo || "")}${x.rodzaj ? " · " + esc(d.rodzaje[x.rodzaj] || x.rodzaj) : ""}</td><td>${esc(dataPl(x.termin_ofert || ""))}</td><td>${x.znwu ? "tak" + (x.znwu_proc ? ` – ${liczba(x.znwu_proc, x.znwu_proc % 1 ? 1 : 0)}% ceny` : "") : x.znwu === false ? "nie" : "–"}</td></tr>`).join("")}`
      : `<tr><th>Data · etap</th><th>Wykonawca</th><th>Kontakt</th><th>Przedmiot</th><th>Cena</th><th>Województwo · rodzaj · źródło</th></tr>
        ${d.lista.map((x, i) => `<tr><td style="white-space:nowrap">${esc(dataPl(x.data || "") || "–")}<br><span class="znacznik ${x.etap === "przed umową" ? "z-startujemy" : ""}">${esc(x.etap)}</span>${x.znwu_szac ? `<br><small class="opis" title="${esc(x.znwu_opis || "")}">zabezp. ${x.znwu_proc ? liczba(x.znwu_proc, x.znwu_proc % 1 ? 1 : 0) + "%" : "do 5%"}: ${x.znwu_proc ? "" : "do "}${zl(x.znwu_szac)}${x.znwu_proc ? "" : " (art. 452 ust. 2)"}</small>` : ""}</td>
          <td><b>${esc(x.wykonawca)}</b><br><small class="opis">NIP ${esc(x.nip || "–")}${x.krs ? " · KRS " + esc(x.krs) : ""}<br>${esc(x.adres || x.siedziba || "")}</small></td>
          <td id="ld-k-${i}"><small>${x.kontakt_pobrany ? ldKontakt(x) : x.nip ? `<button class="maly" onclick="ldPobierzKontakt(${i}, '${escA(x.nip)}')">Pobierz kontakt</button>` : '<span class="opis">brak NIP</span>'}</small></td>
          <td>${x.link ? `<a href="${esc(x.link)}" target="_blank" rel="noopener">${esc(x.przedmiot)}</a>` : esc(x.przedmiot)}<br><small class="opis">${esc(x.zamawiajacy)}${x.liczba_ofert ? " · ofert: " + x.liczba_ofert : ""} · ${esc(x.numer)}</small></td>
          <td class="liczba">${zl(x.cena_brutto)}</td><td>${esc(x.wojewodztwo || "")}${x.rodzaj ? " · " + esc(d.rodzaje[x.rodzaj] || x.rodzaj) : ""}<br><small class="opis">${esc(x.zrodlo || "")}</small></td></tr>`).join("")}`}</table></div>`;
  wstawIkony($("#leady"));
}

// ================================================================ MARKA RESELLERA (nazwa programu, kolor) i BIURO RACHUNKOWE (klienci w Księgowości)
setTimeout(function marka() {
  if (typeof JA === "undefined" || !JA || !JA.login) return setTimeout(marka, 700);
  const m = JA.marka || {};
  if (m.nazwa) { document.title = m.nazwa; document.querySelectorAll("h1").forEach(h => { if (h.textContent.trim() === "Bidivia") h.textContent = m.nazwa; }); }
  if (m.kolor) { document.documentElement.style.setProperty("--akcent", m.kolor); document.documentElement.style.setProperty("--niebieski", m.kolor); }
}, 500);
async function ksKlienciBiura() {
  if (!ADMIN() || $("#ksieg-klienci")) return;
  const K = await api("/api/konta").catch(() => null); if (!K) return;
  const L = (K.konta || []).filter(k => !k.admin && k.ksiegowosc); if (!L.length && !JA.jako) return;
  $("#ksieg").insertAdjacentHTML("beforebegin", `<div id="ksieg-klienci" class="pasek" style="flex-wrap:wrap;align-items:center;margin:0 0 8px">
    <span class="opis">Biuro rachunkowe – księgi klienta:</span>
    ${L.map(k => `<button class="maly ${JA.jako === k.login ? "glowny" : ""}" onclick="otworzKonto('${escA(k.login)}')">${esc(k.firma || k.login)}</button>`).join("")}
    ${JA.jako ? `<button class="maly" onclick="wrocNaKonto()">Moje księgi</button>` : ""}</div>`);
}

// ================================================================ OCHRONA LUDNOŚCI (gmina)
let OLD = null;
async function ladujOlioc() {
  if (!MZ().ochrona_ludnosci) {  // ścieżka wspólnot, spółdzielni i deweloperów – moduł dotyczy gmin (organów ochrony ludności)
    $("#olioc").innerHTML = `<div class="karta"><h3 style="margin-top:0">Moduł dla gmin</h3><p>Ochrona ludności i obrona cywilna to zadania gminy jako organu ochrony ludności – moduł nie dotyczy wspólnot, spółdzielni ani deweloperów.
      Jeżeli budynek ma schron, ukrycie albo miejsce doraźnego schronienia, obowiązki właściciela lub zarządcy (utrzymanie, udostępnienie, kierownik budowli ochronnej) wynikają z decyzji albo porozumienia z gminą.</p>
      <button onclick="pokaz('cel')">Wróć do wyboru celu</button></div>`;
    return;
  } const d = await bezpiecznie(() => api("/api/olioc")); if (d) { OLD = d; rysujOlioc(); } }
function olPole(sciezka, wartosc) {  // sciezka np. ["obiekty", 2, "nazwa"]
  let o = OLD; for (let i = 0; i < sciezka.length - 1; i++) o = o[sciezka[i]]; o[sciezka[sciezka.length - 1]] = wartosc;
}
function olWej(sc, v, typ = "text", szer = "") {
  return `<input type="${typ}" value="${esc(v ?? "")}" ${szer ? `style="width:${szer}"` : ""} onchange='olPole(${JSON.stringify(sc)}, this.value)'>`;
}
function olWyb(sc, v, opcje) {
  return `<select onchange='olPole(${JSON.stringify(sc)}, this.value)'>${opcje.map(([k, t]) => `<option value="${esc(k)}" ${k === v ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
}
function rysujOlioc() {
  const d = OLD, p = d.pokrycie || {}, K = Object.fromEntries((d.kontrola || []).map(k => [k.id, k]));
  const pasek = (proc, norma, opis) => `<div style="margin:6px 0"><div class="opis">${opis}: <b>${proc == null ? "–" : proc + "%"}</b> (norma co najmniej ${norma}%)</div>
    <div style="height:10px;background:var(--tlo,#eee);border-radius:5px;overflow:hidden"><div style="height:100%;width:${Math.min(100, (proc || 0) / norma * 100)}%;background:${(proc || 0) >= norma ? "#16a34a" : "#dc2626"}"></div></div></div>`;
  const MW = d.gmina.typ === "miejsko-wiejska";
  const STANY = [["do sprawdzenia", "do sprawdzenia"], ["sprawny", "sprawny"], ["wymaga prac", "wymaga prac"], ["nie spełnia wymagań", "nie spełnia wymagań"]];
  const STATUSY = ["planowane", "wniosek złożony", "przyznane", "w realizacji", "rozliczone"].map(x => [x, x]);
  $("#olioc").innerHTML = `<div class="ramka-uwaga" style="margin-top:0">Normy pojemności obiektów zbiorowej ochrony (art. 90 ust. 2 ustawy o ochronie ludności i obronie cywilnej): <b>w granicach miast co najmniej 50%</b> przewidywanej liczby ludności, w tym 25% w budowlach ochronnych; <b>poza miastami co najmniej 25%</b>, w tym 15%. Punkty schronienia (art. 84a) nie są obiektami zbiorowej ochrony i nie wliczają się do pokrycia. Program Ochrony Ludności i Obrony Cywilnej na lata 2025–2026 (uchwała nr 72 RM z 27.05.2025 r., zm. uchwałą nr 151 z 4.11.2025 r.) obowiązuje do 31.12.2026 r. – zadania i dotacje na kolejne lata sprawdź w nowym programie.
      Środki wydane niezgodnie z programem albo po terminie gmina zwraca – program pilnuje terminów i wykorzystania dotacji. Wnioski składa się do wojewody; program przygotowuje dane, zamówienia i raport.
      <br><small>Kwota „nie niższa niż 0,3% PKB” (art. 155 ust. 1 ustawy) dotyczy środków budżetu państwa na ochronę ludności, a nie wydatków budżetu gminy – gmina nie musi wykazywać takiego udziału.</small></div>
    <div class="karta"><h3 style="margin-top:0">Gmina</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 14px">
      <label class="ks-pole">Nazwa${olWej(["gmina", "nazwa"], d.gmina.nazwa)}</label>
      <label class="ks-pole">Typ gminy<select onchange='olPole(["gmina", "typ"], this.value); olZapisz(true)'><option value="">– wybierz –</option>${Object.entries(d.typy_gmin || {}).map(([k, t]) => `<option value="${k}" ${k === d.gmina.typ ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
      ${d.gmina.typ === "miejsko-wiejska"
        ? `<label class="ks-pole">Ludność w granicach miasta${olWej(["gmina", "mieszkancy_miasto"], d.gmina.mieszkancy_miasto, "number")}</label><label class="ks-pole">Ludność poza miastem${olWej(["gmina", "mieszkancy_poza"], d.gmina.mieszkancy_poza, "number")}</label>`
        : `<label class="ks-pole">Przewidywana liczba ludności${olWej(["gmina", "mieszkancy"], d.gmina.mieszkancy, "number")}</label>`}</div>
      <p class="opis" style="margin:4px 0">Przewidywana liczba ludności przebywającej na obszarze w sytuacji zagrożenia (art. 90 ust. 2). Po zmianie liczb kliknij „Zapisz”, żeby przeliczyć pokrycie.</p>
      ${(p.obszary || []).map(o => `<h4 style="margin:10px 0 2px">${esc(o.nazwa.charAt(0).toUpperCase() + o.nazwa.slice(1))}${o.ludnosc ? ` – ${liczba(o.ludnosc)} osób` : ""}</h4>
        ${pasek(o.wszystkie_proc, o.norma_wszystkie, `Wszystkie obiekty zbiorowej ochrony – potwierdzone: ${Math.round(o.wszystkie_miejsc || 0)} miejsc${o.brak_wszystkie ? ` – brakuje ${liczba(o.brak_wszystkie)}` : ""}`)}
        ${pasek(o.budowle_proc, o.norma_budowle, `W tym budowle ochronne (schrony, ukrycia): ${Math.round(o.budowle_miejsc || 0)} miejsc${o.brak_budowle ? ` – brakuje ${liczba(o.brak_budowle)}` : ""}`)}
        <p class="opis" style="margin:2px 0">Deklarowane (z obiektami do sprawdzenia i wymagającymi prac): wszystkie ${o.wszystkie_proc_dekl ?? "–"}%, budowle ${o.budowle_proc_dekl ?? "–"}%.</p>`).join("")}
      ${p.punkty_liczba ? `<p class="opis" style="margin:4px 0">Punkty schronienia: ${p.punkty_liczba} (${Math.round(p.punkty_miejsc || 0)} miejsc) – poza pokryciem obiektów zbiorowej ochrony.</p>` : ""}
      ${(p.ostrzezenia || []).map(t => `<div class="ramka-uwaga" style="margin:6px 0">${esc(t)}</div>`).join("")}
      <p class="opis" style="margin:4px 0 0">Obiektów do sprawdzenia: ${p.do_sprawdzenia || 0} · wymagających prac: ${p.wymaga_prac || 0} · szacunkowy koszt prac: ${liczba(p.koszt_prac || 0, 2)} zł</p></div>
    <div class="karta"><h3 style="margin-top:0">Obiekty zbiorowej ochrony (${d.obiekty.length})</h3>
      <div class="tabela-okno"><table class="tabela"><tr><th>Nazwa</th><th>Adres</th><th>Kategoria</th>${MW ? "<th>Obszar</th>" : ""}<th>Miejsc</th><th>Stan</th><th>Potrzebne prace</th><th>Koszt [zł]</th><th></th></tr>
      ${d.obiekty.map((o, i) => `<tr><td>${olWej(["obiekty", i, "nazwa"], o.nazwa, "text", "160px")}</td><td>${olWej(["obiekty", i, "adres"], o.adres, "text", "160px")}</td>
        <td>${olWyb(["obiekty", i, "kategoria"], o.kategoria, Object.entries(d.kategorie))}</td>${MW ? `<td>${olWyb(["obiekty", i, "obszar"], o.obszar || "miasto", [["miasto", "w mieście"], ["poza", "poza miastem"]])}</td>` : ""}<td>${olWej(["obiekty", i, "pojemnosc"], o.pojemnosc, "number", "80px")}</td>
        <td>${olWyb(["obiekty", i, "stan"], o.stan || "do sprawdzenia", STANY)}</td><td>${olWej(["obiekty", i, "prace"], o.prace, "text", "180px")}</td>
        <td>${olWej(["obiekty", i, "koszt"], o.koszt, "number", "100px")}</td><td><button class="maly" onclick="OLD.obiekty.splice(${i}, 1); rysujOlioc()">Usuń</button></td></tr>`).join("")}</table></div>
      <button class="maly" data-ik="plus" onclick="OLD.obiekty.push({kategoria: 'mds', stan: 'do sprawdzenia'}); rysujOlioc()">Dodaj obiekt</button></div>
    <div class="karta"><h3 style="margin-top:0">Zadania w ramach programu (${d.zadania.length})</h3>
      ${d.zadania.map((z, i) => { const k = K[z.id] || {}; return `<div style="border:1px solid var(--linia,#ddd);border-radius:8px;padding:10px;margin:0 0 10px">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px 12px">
          <label class="ks-pole">Obszar${olWyb(["zadania", i, "obszar"], z.obszar || "I", Object.entries(d.obszary).map(([o, v]) => [o, `${o}. ${v.nazwa}`]))}</label>
          <label class="ks-pole">Zadanie${olWej(["zadania", i, "nazwa"], z.nazwa)}</label>
          <label class="ks-pole">Dotacja [zł]${olWej(["zadania", i, "dotacja"], z.dotacja, "number")}</label>
          <label class="ks-pole">Wkład własny [zł]${olWej(["zadania", i, "wklad"], z.wklad, "number")}</label>
          <label class="ks-pole">Termin wykorzystania${olWej(["zadania", i, "termin"], z.termin, "date")}</label>
          <label class="ks-pole">Status${olWyb(["zadania", i, "status"], z.status || "planowane", STATUSY)}</label></div>
        <div class="opis" style="margin:6px 0">Wydatki: ${liczba(k.wydatki || 0, 2)} zł${k.wykorzystanie != null ? ` (${k.wykorzystanie}% dotacji)` : ""}${z.projekt_id ? ` · <a href="#" onclick="otworzProjekt('${escA(z.projekt_id)}'); return false">zamówienie</a>` : ""}</div>
        ${(k.alerty || []).map(([poz, t]) => `<div style="padding:4px 8px;margin:2px 0;border-radius:4px;background:${poz === "czerwony" ? "#FEE2E2" : "var(--zolty-jasny)"}">${esc(t)}</div>`).join("")}
        <details style="margin-top:6px"><summary>Wydatki (${(z.wydatki || []).length})</summary>
          ${(z.wydatki || []).map((w, j) => `<div style="display:flex;gap:6px;flex-wrap:wrap;margin:4px 0">${olWej(["zadania", i, "wydatki", j, "data"], w.data, "date")}
            ${olWej(["zadania", i, "wydatki", j, "dokument"], w.dokument, "text", "160px")}${olWej(["zadania", i, "wydatki", j, "kwota"], w.kwota, "number", "110px")}
            <button class="maly" onclick="OLD.zadania[${i}].wydatki.splice(${j}, 1); rysujOlioc()">Usuń</button></div>`).join("")}
          <button class="maly" onclick="(OLD.zadania[${i}].wydatki = OLD.zadania[${i}].wydatki || []).push({data: dzis()}); rysujOlioc()">Dodaj wydatek (faktura, protokół)</button></details>
        <div class="pasek" style="margin-top:8px">${z.projekt_id ? "" : `<button class="maly glowny" data-ik="plus" onclick="olZamowienie(${i})">Utwórz zamówienie</button>`}
          <button class="maly" onclick="OLD.zadania.splice(${i}, 1); rysujOlioc()">Usuń zadanie</button></div></div>`; }).join("")}
      <button class="maly" data-ik="plus" onclick="OLD.zadania.push({obszar: 'I', status: 'planowane', wydatki: []}); rysujOlioc()">Dodaj zadanie</button></div>
    <div class="pasek"><button class="glowny" onclick="olZapisz()">Zapisz</button><a class="przycisk" href="/api/olioc/raport">Raport (Word)</a></div>`;
  wstawIkony($("#olioc"));
}
async function olZapisz(cicho) {
  const d = await bezpiecznie(() => api("/api/olioc", {json: {gmina: OLD.gmina, obiekty: OLD.obiekty, zadania: OLD.zadania}}));
  if (d) { Object.assign(OLD, d); rysujOlioc(); if (!cicho) komunikat("Zapisano."); }
  return d;
}
async function olZamowienie(i) {
  if (!(await olZapisz(true))) return;
  const z = OLD.zadania[i], ob = OLD.obszary[z.obszar] || {};
  if (!z.nazwa) return komunikat("Najpierw wpisz nazwę zadania.", true);
  const budzet = (Number(z.dotacja) || 0) + (Number(z.wklad) || 0);
  const p = await zalozZamowienie(({json: {rodzaj: ob.rodzaj || "roboty", nazwa: z.nazwa, sciezka: "nowe", budzet: budzet ? String(budzet) : "",
    opis: `${z.nazwa} – zadanie z Programu Ochrony Ludności i Obrony Cywilnej (obszar ${z.obszar}: ${ob.nazwa || ""}). Dotacja ${z.dotacja || 0} zł, wkład własny ${z.wklad || 0} zł, termin wykorzystania środków ${z.termin || "–"}.`}}));
  if (!p || !p.id) return;
  await bezpiecznie(() => api("/api/olioc/powiaz", {json: {zadanie_id: OLD.zadania[i].id, projekt_id: p.id}}));
  komunikat("Utworzono zamówienie – otwieram kreator.");
  KZN = {rodzaj: ob.rodzaj || "roboty", sciezka: "nowe"}; PROJEKT_ID = p.id; TRYB = "zamowienie"; pokaz("zam_projekty"); otworzProjekt(p.id);
}

// ================================================================ ROCZNE SPRAWOZDANIE DO UZP
let SPD = null;
async function ladujSprawozdanie(rok) {
  const d = await bezpiecznie(() => api("/api/sprawozdanie" + (rok ? "?rok=" + rok : ""))); if (d) { SPD = d; rysujSprawozdanie(); }
}
function spPole(i, k, v) { SPD.pozycje[i][k] = v; }
function spFlag(i, grupa, k, v) { (SPD.pozycje[i][grupa] = SPD.pozycje[i][grupa] || {})[k] = v; }
function rysujSprawozdanie() {
  const d = SPD, z = d.zestawienie || {}, zl = v => liczba(v || 0, 2) + " zł";
  const wej = (i, k, typ = "text", szer = "") => `<input type="${typ}" value="${esc(d.pozycje[i][k] ?? "")}" ${szer ? `style="width:${szer}"` : ""} onchange="spPole(${i}, '${k}', this.value)">`;
  const wyb = (i, k, opcje) => `<select onchange="spPole(${i}, '${k}', this.value)"><option value=""></option>${opcje.map(([v, t]) => `<option value="${esc(v)}" ${d.pozycje[i][k] === v ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>`;
  const SEKCJA = Object.fromEntries((z.pozycje || []).map(p => [p.id, p]));
  const lata = [0, 1, 2].map(x => new Date().getFullYear() - x);
  $("#sprawozdanie").innerHTML = `${plnPowrot()}<div class="ramka-uwaga" style="margin-top:0">Art. 82 Pzp: sprawozdanie za rok ${d.rok} przekazuje się do <b>${esc(dataPl(z.termin))}</b> wyłącznie przez formularz na platformie e-Zamówienia.
      Program przypisuje zamówienia do sekcji (wartość szacunkowa, próg krajowy ${liczba(d.prog_krajowy, 0)} zł, progi unijne, usługi społeczne, wyłączenia), liczy zestawienia i pokazuje braki; arkusz Excel ma układ formularza do przepisania.
      Podstawa: rozporządzenie z 20.12.2021 r. (Dz.U. poz. 2463) i objaśnienia UZP.</div>
    <div class="pasek" style="flex-wrap:wrap"><label class="ks-pole" style="margin:0">Rok sprawozdawczy<select onchange="ladujSprawozdanie(this.value)">${lata.map(r => `<option ${r === d.rok ? "selected" : ""}>${r}</option>`).join("")}</select></label>
      <button class="glowny" data-ik="pobierz" onclick="spImport()">Pobierz zamówienia z projektów</button>
      <button onclick="SPD.pozycje.push({kategoria: 'klasyczne', kraj: 'PL', zrodlo: 'reczne'}); rysujSprawozdanie()">Dodaj zamówienie ręcznie</button>
      <button onclick="spZapisz()">Zapisz</button><a class="przycisk" href="/api/sprawozdanie/xlsx?rok=${d.rok}" onclick="spZapisz(true).then(() => location.href = this.href); return false">Arkusz Excel</a></div>
    <div class="karta"><h3 style="margin-top:0">Sekcja I – zamawiający</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px 12px">
      ${[["nazwa", "Nazwa"], ["adres", "Adres"], ["nip", "NIP"], ["regon", "REGON"], ["rodzaj", "Rodzaj zamawiającego (art. 4, 5, 6)"], ["email", "E-mail"], ["osoba", "Osoba do kontaktu"]].map(([k, t]) =>
        `<label class="ks-pole">${t}<input value="${esc(d.zamawiajacy[k] || "")}" onchange="SPD.zamawiajacy['${k}'] = this.value" ${d.zamawiajacy[k] ? "" : 'style="background:var(--zolty-jasny)"'}></label>`).join("")}</div></div>
    <div class="karta"><h3 style="margin-top:0">Zestawienie (umowy zawarte w ${d.rok} r.: ${(z.pozycje || []).length}, razem ${zl(z.razem_netto)} netto)</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:6px">
      ${[["II", "klasyczne poniżej progów UE"], ["III", "od progów UE"], ["IV", "konflikt interesów, zmowy"], ["V", "usługi społeczne"], ["VI", "aspekty społeczne"], ["VII", "środowiskowe, innowacyjne"], ["VIII", "wyłączenia z Pzp"], ["IX", "poniżej progu Pzp"]].map(([s, t]) =>
        `<div style="border:1px solid var(--linia,#ddd);border-radius:6px;padding:6px 8px"><b>Sekcja ${s}</b><br><span class="opis">${t}</span><br>${s === "II" || s === "VIII" || s === "IX" ? "wierszy" : "pozycji"}: ${(z.liczby || {})[s] || 0}</div>`).join("")}</div>
      ${(z.braki || []).length ? `<div style="margin-top:8px;padding:8px 10px;background:var(--zolty-jasny);border-radius:6px"><b>Braki do uzupełnienia (${z.braki.length}):</b><ul class="lista" style="margin:4px 0 0">${z.braki.map(b => `<li>${esc(b.nazwa || "(bez nazwy)")} – sekcja ${b.sekcja}: ${esc(b.braki.join(", "))}</li>`).join("")}</ul></div>`
        : (z.pozycje || []).length ? '<p style="color:#16a34a;margin:8px 0 0"><b>Wszystkie wymagane dane są uzupełnione.</b></p>' : ""}</div>
    ${d.pozycje.map((p, i) => { const q = SEKCJA[p.id] || {}; return `<details class="karta" ${(q.braki || []).length ? "open" : ""}><summary><b>${esc(p.nazwa || "(bez nazwy)")}</b> · sekcja ${q.sekcja || "?"} · ${zl(p.wartosc_umowy)}${(q.braki || []).length ? ` · <span style="color:#b45309">braki: ${q.braki.length}</span>` : ""}${p.zrodlo === "projekt" ? ' · <span class="opis">z projektu</span>' : ""}</summary>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px 12px;margin-top:8px">
        <label class="ks-pole">Nazwa${wej(i, "nazwa")}</label><label class="ks-pole">Data zawarcia umowy${wej(i, "data_umowy", "date")}</label>
        <label class="ks-pole">Wartość szacunkowa netto [zł]${wej(i, "wartosc_szac", "number")}</label><label class="ks-pole">Wartość umowy netto [zł]${wej(i, "wartosc_umowy", "number")}</label>
        <label class="ks-pole">Rodzaj${wyb(i, "rodzaj", Object.entries(d.rodzaje))}</label><label class="ks-pole">Kategoria${wyb(i, "kategoria", Object.entries(d.kategorie))}</label>
        <label class="ks-pole">Tryb${wyb(i, "tryb", d.tryby.map(t => [t, t]))}</label><label class="ks-pole">Główny kod CPV${wej(i, "cpv")}</label>
        <label class="ks-pole">Nr ogłoszenia (BZP/TED)${wej(i, "numer_ogloszenia")}</label><label class="ks-pole">Liczba części${wej(i, "czesci", "number")}</label>
        <label class="ks-pole">Liczba ofert${wej(i, "oferty", "number")}</label><label class="ks-pole">Odrzucone oferty${wej(i, "odrzucone", "number")}</label>
        <label class="ks-pole">Oferty MŚP${wej(i, "oferty_msp", "number")}</label><label class="ks-pole">Wybrany wykonawca to MŚP${wyb(i, "wybrany_msp", [["TAK", "TAK"], ["NIE", "NIE"]])}</label>
        <label class="ks-pole">Kraj wykonawcy (kod)${wej(i, "kraj", "text", "70px")}</label><label class="ks-pole">Podstawa wyłączenia z Pzp (art.)${wej(i, "wylaczenie")}</label>
        <label class="ks-pole">Przypadki konfliktu interesów${wej(i, "konflikt", "number")}</label><label class="ks-pole">Wykryte porozumienia (zmowy)${wej(i, "porozumienia", "number")}</label>
        <label class="ks-pole" style="flex-direction:row;align-items:center;gap:6px"><input type="checkbox" ${p.usluga_spoleczna ? "checked" : ""} onchange="spPole(${i}, 'usluga_spoleczna', this.checked)"> Usługa społeczna (art. 359)</label></div>
      <details style="margin-top:6px"><summary>Aspekty społeczne (sekcja VI)</summary>${Object.entries(d.spoleczne).map(([k, t]) => `<label style="display:block"><input type="checkbox" ${(p.spoleczne || {})[k] ? "checked" : ""} onchange="spFlag(${i}, 'spoleczne', '${k}', this.checked)"> ${esc(t)}</label>`).join("")}</details>
      <details><summary>Aspekty środowiskowe i innowacyjne (sekcja VII)</summary>${Object.entries(d.srodowiskowe).map(([k, t]) => `<label style="display:block"><input type="checkbox" ${(p.srodowiskowe || {})[k] ? "checked" : ""} onchange="spFlag(${i}, 'srodowiskowe', '${k}', this.checked)"> ${esc(t)}</label>`).join("")}</details>
      <div class="pasek" style="margin-top:6px">${p.projekt_id ? `<a href="#" onclick="otworzProjekt('${escA(p.projekt_id)}'); return false">Otwórz projekt</a>` : ""}<button class="maly" onclick="SPD.pozycje.splice(${i}, 1); rysujSprawozdanie()">Usuń z zestawienia</button></div></details>`; }).join("")}`;
  wstawIkony($("#sprawozdanie"));
}
async function spZapisz(doPobrania) {
  const r = await bezpiecznie(() => api("/api/sprawozdanie", {json: {rok: SPD.rok, pozycje: SPD.pozycje, zamawiajacy: SPD.zamawiajacy}}));
  if (r && !doPobrania) { SPD.zestawienie = r.zestawienie; rysujSprawozdanie(); komunikat("Zapisano."); }
  return !!r || !doPobrania;
}
async function spImport() {
  await spZapisz(true);
  const r = await bezpiecznie(() => api("/api/sprawozdanie/import", {json: {rok: SPD.rok}}));
  if (r) { komunikat(r.dodano ? `Dodano ${r.dodano} zamówień z projektów (umowy z ${SPD.rok} r.).` : `Brak nowych zamówień z umową zawartą w ${SPD.rok} r. w projektach.`); ladujSprawozdanie(SPD.rok); }
}

function ldKontakt(x) {
  const e = (x.email || "").split(", ").filter(Boolean).map(a => `<a href="mailto:${esc(a)}">${esc(a)}</a>`).join("<br>");
  return (e || "") + (x.telefon ? (e ? "<br>" : "") + esc(x.telefon) : "") + (x.www ? `<br><a href="${esc(x.www.startsWith("http") ? x.www : "https://" + x.www)}" target="_blank" rel="noopener">${esc(x.www)}</a>` : "")
    + (x.ade ? `<br><span class="opis">e-Doręczenia: ${esc(x.ade)}</span>` : "")
    + (!e && !x.telefon && !x.www && !x.ade ? '<span class="opis">brak w rejestrach i na stronie</span>' : "");
}
async function ldPobierzKontakt(i, nip) {
  const el = $("#ld-k-" + i); if (el) el.innerHTML = '<small class="opis">pobieram…</small>';
  const k = await bezpiecznie(() => api("/api/leady/kontakt", {json: {nip}}));
  if (!k) { if (el) el.innerHTML = '<small class="opis">nie udało się</small>'; return; }
  const x = LEADY.dane && LEADY.dane.lista[i]; if (x) Object.assign(x, k, {kontakt_pobrany: true});
  if (el) el.innerHTML = "<small>" + ldKontakt(Object.assign({}, k)) + "</small>";
}

function ldDiag(d) {
  const g = d.diag || {};
  if (!d.dni_w_pamieci) return d.zbieranie ? " Rozstrzygnięcia są właśnie zbierane." : " W pamięci nie ma jeszcze rozstrzygnięć – zbierają się co noc albo po „Pobierz teraz” w Kontach i aktywności.";
  return ` W pamięci: ${g.w_okresie || 0} rozstrzygnięć w wybranym okresie i województwie (dni z danymi: ${d.dni_w_pamieci}); po rodzaju: ${g.po_rodzaju || 0}; po słowach w przedmiocie: ${g.po_slowach || 0}; po cenie: ${g.po_cenie || 0}.`
    + (g.po_rodzaju && !g.po_slowach ? " Słowa zawężają do tytułów zawierających dokładnie to słowo – wyczyść pole „Słowa w przedmiocie”." : "");
}

// ================================================================ ROCZNY PLAN ZAMÓWIEŃ (art. 23 Pzp)
let PLN = {rok: new Date().getFullYear() + (new Date().getMonth() >= 9 ? 1 : 0), dane: null, edycja: null};
const PLN_KAT = {wylaczone: ["wyłączone z Pzp", "#6b7280"], ponizej_pzp: ["poniżej progu Pzp – poza planem", "#6b7280"], krajowe: ["Pzp – poniżej progów UE", "#1F5A99"], unijne: ["Pzp – od progów UE", "#7C3AED"]};
async function ladujPlanZam() { const d = await bezpiecznie(() => api("/api/plan?rok=" + PLN.rok)); if (d) { PLN.dane = d; rysujPlanZam(); } }
function plnZl(v) { return liczba(v || 0, 0) + " zł"; }
function plnTermin(p) { return p.termin_typ === "kwartal" ? `${p.termin} kwartał` : (PLN.dane.listy.miesiace[p.termin - 1] || ""); }
function rysujPlanZam() {
  const d = PLN.dane, pl = d.plan, s = d.podsumowanie, L = d.listy;
  const lata = [...new Set([...d.lata, String(new Date().getFullYear()), String(new Date().getFullYear() + 1), String(PLN.rok)])].sort();
  const opubl = d.wersje.length;
  $("#plan-zam").innerHTML = `${plnPowrot()}<div class="ramka-uwaga" style="margin-top:0">Plan postępowań o udzielenie zamówień (art. 23 Pzp) sporządzają zamawiający z art. 4 pkt 1 i 2 (jednostki sektora finansów publicznych, państwowe jednostki bez osobowości prawnej) i ich związki – najpóźniej 30 dni od przyjęcia budżetu albo planu finansowego; publikacja w BZP i na stronie internetowej, aktualizacje w ciągu roku. Obejmuje zamówienia, do których stosuje się Pzp (od ${plnZl(s.prog_pzp)} netto); mniejsze i wyłączone są tylko w planie wewnętrznym – do pilnowania zakazu dzielenia zamówień (art. 29–30). Progi UE ${pl.rok}: roboty ${plnZl(s.progi_ue.roboty)}, dostawy i usługi ${plnZl(s.progi_ue.dostawy)} (kurs ${String(s.kurs).replace(".", ",")} zł/€).</div>
    <div class="pasek" style="flex-wrap:wrap;align-items:center"><label class="ks-pole" style="margin:0">Rok planu<select id="pl-rok" onchange="PLN.rok=+this.value; PLN.edycja=null; ladujPlanZam()">${lata.map(r => `<option ${+r === PLN.rok ? "selected" : ""}>${r}</option>`).join("")}</select></label>
      <button class="glowny" data-ik="plus" onclick="PLN.edycja={}; rysujPlanZam(); setTimeout(()=>$('#pl-e-przedmiot').focus(),50)">Dodaj pozycję</button>
      <button data-ik="pobierz" onclick="location.href='/api/plan/plik/wzor?rok=${PLN.rok}'">Wzór importu (Excel)</button>
      <label class="przycisk" data-ik="tabela">Import z Excela<input type="file" accept=".xlsx,.xlsm" hidden onchange="plnWgraj('import', this.files[0])"></label>
      <label class="przycisk" data-ik="iskra">Propozycje z uchwały budżetowej (AI)<input type="file" accept=".pdf,.docx,.xlsx" hidden onchange="plnWgraj('budzet', this.files[0])"></label>
      ${d.lata.includes(String(PLN.rok - 1)) ? `<button onclick="plnKopiuj()">Kopiuj z roku ${PLN.rok - 1}</button>` : ""}</div>
    <div class="karta"><h3 style="margin-top:0">Dane planu</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
      <label class="ks-pole">Rodzaj zamawiającego<select id="pl-rz">${L.rodzaje_zamawiajacego.map(x => `<option ${x === pl.rodzaj_zamawiajacego ? "selected" : ""}>${esc(x)}</option>`).join("")}</select></label>
      <label class="ks-pole">Data przyjęcia budżetu / planu finansowego<input id="pl-db" type="date" value="${esc(pl.data_budzetu || "")}"></label>
      <label class="ks-pole">Numer planu w BZP (po publikacji)<input id="pl-nr" value="${esc(pl.numer_bzp || "")}" placeholder="np. 2026/BZP 00012345/01"></label>
      <label class="ks-pole" style="flex-direction:row;align-items:center;gap:6px"><input id="pl-cz" type="checkbox" ${pl.centralny ? "checked" : ""}> centralny zamawiający (niższy próg UE dla dostaw i usług)</label></div>
      <button style="margin-top:8px" onclick="plnUstawienia()">Zapisz dane planu</button></div>
    <p><b>${s.pozycji}</b> pozycji, razem <b>${plnZl(s.suma)}</b> netto · w planie postępowań (BZP): <b>${s.w_planie_postepowan}</b> (poniżej progów UE: ${s.krajowe}, od progów UE: ${s.unijne}) · tylko w planie wewnętrznym: ${s.poza_planem}</p>
    ${d.kontrole.length ? `<div class="karta" style="padding:8px 12px"><b>Kontrole</b><ul class="lista">${d.kontrole.map(k => `<li class="${k.waga === "blad" ? "czerwone" : ""}">${k.waga === "ostrzezenie" ? "⚠ " : ""}${esc(k.opis)}</li>`).join("")}</ul></div>` : ""}
    ${PLN.edycja ? plnFormularz() : ""}
    <div class="tabela-okno"><table class="tabela"><tr><th>Id</th><th>Przedmiot</th><th>Rodzaj</th><th class="liczba">Wartość netto</th><th>Kategoria</th><th>Tryb</th><th>Termin wszczęcia</th><th>Status</th><th></th></tr>
      ${pl.pozycje.map(p => { const k = PLN_KAT[d.kategorie[p.id]] || ["", ""]; return `<tr style="${p.status === "rezygnacja" ? "opacity:.5;text-decoration:line-through" : ""}">
        <td>${esc(p.id)}${p.id_bzp ? `<br><small class="opis">BZP: ${esc(p.id_bzp)}</small>` : ""}</td><td><b>${esc(p.przedmiot)}</b><br><small class="opis">${esc([p.cpv && "CPV " + p.cpv, p.komorka, p.zrodlo].filter(Boolean).join(" · "))}</small></td>
        <td>${esc(L.rodzaje[p.rodzaj])}</td><td class="liczba">${plnZl(p.wartosc)}</td><td><small style="color:${k[1]}">${esc(k[0])}</small></td><td><small>${esc(p.tryb || "–")}</small></td>
        <td>${esc(plnTermin(p))}</td><td>${esc(p.status)}${p.projekt_id ? `<br><a href="#" onclick="PROJEKT_ID='${p.projekt_id}'; TRYB='zamowienie'; pokaz('zam_projekty'); otworzProjekt('${p.projekt_id}'); return false"><small>postępowanie</small></a>` : ""}</td>
        <td style="white-space:nowrap"><button class="maly" onclick="PLN.edycja=PLN.dane.plan.pozycje.find(x=>x.id==='${p.id}'); rysujPlanZam(); window.scrollTo(0,0)">Edytuj</button>
          ${p.status === "zaplanowane" && d.kategorie[p.id] !== "wylaczone" ? `<button class="maly glowny" onclick="plnUruchom('${p.id}')">Uruchom postępowanie</button>` : ""}
          ${p.status !== "rezygnacja" ? `<button class="maly" onclick="plnUsun('${p.id}')">${opubl ? "Rezygnacja" : "Usuń"}</button>` : ""}</td></tr>`; }).join("") || '<tr><td colspan="9" class="opis">Brak pozycji – dodaj je, zaimportuj z Excela, z uchwały budżetowej albo skopiuj z poprzedniego roku.</td></tr>'}</table></div>
    <div class="karta"><h3 style="margin-top:0">Publikacja w BZP i na stronie internetowej</h3>
      <p class="opis" style="margin-top:0">Plan zamieszczasz formularzem na Platformie e-Zamówienia (program nie publikuje go sam). Zestawienie ma układ formularza: dwie tabele (poniżej i od progów UE), w nich roboty, dostawy, usługi. Na stronie internetowej – treść tożsama z BZP.</p>
      ${opubl && d.zmiany.length ? `<p><b>Zmiany od ostatniej publikacji (do aktualizacji w BZP):</b></p><ul class="lista">${d.zmiany.map(z => `<li>${esc(z.id)} – ${esc(z.typ)}: ${esc(z.przedmiot)}${z.pola ? ` <small class="opis">(${esc(z.pola.join(", "))})</small>` : ""}</li>`).join("")}</ul>` : opubl ? '<p class="opis">Plan postępowań zgodny z ostatnią opublikowaną wersją.</p>' : ""}
      <div class="pasek" style="flex-wrap:wrap"><button data-ik="tabela" onclick="location.href='/api/plan/plik/xlsx?rok=${PLN.rok}'">Zestawienie do BZP (Excel)</button>
        <button data-ik="pobierz" onclick="location.href='/api/plan/plik/docx?rok=${PLN.rok}'">Plan na stronę internetową (Word)</button>
        <button class="glowny" onclick="plnOpublikuj()">${opubl ? "Zapisz aktualizację jako opublikowaną" : "Zapisz plan jako opublikowany w BZP"}</button></div>
      ${opubl ? `<p class="opis">Wersje: ${d.wersje.map(w => `${w.nr}. ${esc(w.data)}${w.numer_bzp ? " (" + esc(w.numer_bzp) + ")" : ""}${w.zmiany && w.zmiany.length ? ` – zmian: ${w.zmiany.length}` : " – plan pierwotny"}`).join(" · ")}</p>` : ""}</div>`;
  wstawIkony($("#plan-zam"));
  if (PLN.edycja && $("#pl-e-tt")) plnTerminy();
}
function plnFormularz() {
  const p = PLN.edycja || {}, L = PLN.dane.listy, kat = p.id ? PLN.dane.kategorie[p.id] : "";
  const tryby = kat === "unijne" ? L.tryby_ue : kat === "krajowe" ? L.tryby_kraj : [...L.tryby_kraj, ...L.tryby_ue.filter(t => !L.tryby_kraj.includes(t))];
  return `<div class="karta" style="border:2px solid var(--akcent)"><h3 style="margin-top:0">${p.id ? "Pozycja " + esc(p.id) : "Nowa pozycja"}</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
      <label class="ks-pole" style="grid-column:1/-1">Przedmiot zamówienia<input id="pl-e-przedmiot" value="${esc(p.przedmiot || "")}"></label>
      <label class="ks-pole">Rodzaj<select id="pl-e-rodzaj">${Object.entries(L.rodzaje).map(([k, t]) => `<option value="${k}" ${k === p.rodzaj ? "selected" : ""}>${t}</option>`).join("")}</select></label>
      <label class="ks-pole">Kod CPV<input id="pl-e-cpv" value="${esc(p.cpv || "")}" placeholder="np. 45233140-2"></label>
      <label class="ks-pole">Orientacyjna wartość netto [zł]<input id="pl-e-wartosc" type="number" step="0.01" value="${p.wartosc ?? ""}"></label>
      <label class="ks-pole">Termin wszczęcia<select id="pl-e-tt" onchange="plnTerminy()"><option value="miesiac" ${p.termin_typ !== "kwartal" ? "selected" : ""}>miesiąc</option><option value="kwartal" ${p.termin_typ === "kwartal" ? "selected" : ""}>kwartał</option></select></label>
      <label class="ks-pole">&nbsp;<select id="pl-e-termin"></select></label>
      <label class="ks-pole">Przewidywany tryb albo procedura<select id="pl-e-tryb"><option value="">(program dobierze do wartości)</option>${tryby.map(t => `<option ${t === p.tryb ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>
      <label class="ks-pole">Komórka / dysponent<input id="pl-e-komorka" value="${esc(p.komorka || "")}"></label>
      <label class="ks-pole">Źródło finansowania<input id="pl-e-zrodlo" value="${esc(p.zrodlo || "")}" placeholder="np. dział 600, rozdz. 60016, § 6050"></label>
      <label class="ks-pole">Status<select id="pl-e-status">${L.statusy.map(x => `<option ${x === (p.status || "zaplanowane") ? "selected" : ""}>${x}</option>`).join("")}</select></label>
      <label class="ks-pole">Identyfikator pozycji w BZP<input id="pl-e-idbzp" value="${esc(p.id_bzp || "")}" placeholder="po publikacji"></label></div>
    <div style="margin-top:8px"><span class="opis">Informacje dodatkowe:</span> ${Object.entries(L.info).map(([k, t]) => `<label style="margin-right:10px"><input type="checkbox" class="pl-e-info" value="${k}" ${(p.info || {})[k] ? "checked" : ""}> ${t}</label>`).join("")}
      <input id="pl-e-infot" value="${esc(p.info_tekst || "")}" placeholder="inne informacje dodatkowe" style="width:100%;margin-top:4px"></div>
    <label style="display:block;margin-top:6px"><input id="pl-e-wyl" type="checkbox" ${p.wylaczone ? "checked" : ""}> zamówienie wyłączone ze stosowania Pzp – podstawa: <input id="pl-e-podst" value="${esc(p.podstawa_wylaczenia || "")}" placeholder="np. art. 11 ust. 5 pkt 2"></label>
    <div class="pasek" style="margin-top:8px"><button class="glowny" onclick="plnZapisz()">Zapisz pozycję</button><button onclick="PLN.edycja=null; rysujPlanZam()">Anuluj</button></div></div>`;
}
function plnTerminy() {
  const tt = $("#pl-e-tt").value, p = PLN.edycja || {}, L = PLN.dane.listy;
  $("#pl-e-termin").innerHTML = (tt === "kwartal" ? [1, 2, 3, 4].map(k => [k, k + " kwartał"]) : L.miesiace.map((m, i) => [i + 1, m]))
    .map(([v, t]) => `<option value="${v}" ${v === p.termin && tt === (p.termin_typ || "miesiac") ? "selected" : ""}>${t}</option>`).join("");
}
async function plnZapisz() {
  const poz = {...(PLN.edycja || {}), przedmiot: $("#pl-e-przedmiot").value, rodzaj: $("#pl-e-rodzaj").value, cpv: $("#pl-e-cpv").value, wartosc: $("#pl-e-wartosc").value,
    termin_typ: $("#pl-e-tt").value, termin: +$("#pl-e-termin").value, tryb: $("#pl-e-tryb").value, komorka: $("#pl-e-komorka").value, zrodlo: $("#pl-e-zrodlo").value,
    status: $("#pl-e-status").value, id_bzp: $("#pl-e-idbzp").value, info_tekst: $("#pl-e-infot").value, wylaczone: $("#pl-e-wyl").checked, podstawa_wylaczenia: $("#pl-e-podst").value,
    info: Object.fromEntries([...document.querySelectorAll(".pl-e-info")].map(c => [c.value, c.checked]))};
  const d = await bezpiecznie(() => api("/api/plan/pozycja", {json: {rok: PLN.rok, pozycja: poz}})); if (!d) return;
  PLN.dane = d; PLN.edycja = null; rysujPlanZam(); komunikat(`Zapisano pozycję ${d.zapisano}.`);
}
async function plnUsun(id) {
  if (!confirm(PLN.dane.wersje.length ? "Oznaczyć pozycję jako rezygnację? (aktualizacja planu w BZP)" : "Usunąć pozycję z planu?")) return;
  const d = await bezpiecznie(() => api("/api/plan/usun", {json: {rok: PLN.rok, id}})); if (d) { PLN.dane = d; rysujPlanZam(); }
}
async function plnUstawienia() {
  const d = await bezpiecznie(() => api("/api/plan/ustawienia", {json: {rok: PLN.rok, rodzaj_zamawiajacego: $("#pl-rz").value, data_budzetu: $("#pl-db").value, numer_bzp: $("#pl-nr").value, centralny: $("#pl-cz").checked}}));
  if (d) { PLN.dane = d; rysujPlanZam(); komunikat("Zapisano dane planu."); }
}
async function plnKopiuj() { const d = await bezpiecznie(() => api("/api/plan/kopiuj", {json: {rok: PLN.rok}})); if (d) { PLN.dane = d; rysujPlanZam(); komunikat("Skopiowano pozycje z poprzedniego roku – sprawdź wartości i terminy."); } }
async function plnWgraj(rodzaj, plik) {
  if (!plik) return; const fd = new FormData(); fd.append("rok", PLN.rok); fd.append("plik", plik);
  const d = await bezpiecznie(() => api("/api/plan/" + rodzaj, {method: "POST", body: fd})); if (!d) return;
  if (rodzaj === "budzet") return sledz(d, ladujPlanZam);
  PLN.dane = d; rysujPlanZam(); komunikat(`Dodano ${d.dodano} pozycji z arkusza.`);
}
async function plnOpublikuj() {
  const pusty = !(PLN.dane.plan.pozycje || []).some(p => ["krajowe", "unijne"].includes(PLN.dane.kategorie[p.id]) && p.status !== "rezygnacja");
  if (pusty && !confirm("Plan postępowań jest pusty – nie ma w nim pozycji od progu stosowania ustawy Pzp. Czy na pewno zapisać pusty plan jako opublikowany w BZP?")) return;
  const nr = prompt("Numer planu w BZP (z potwierdzenia publikacji na Platformie e-Zamówienia):", PLN.dane.plan.numer_bzp || ""); if (nr === null) return;
  const d = await bezpiecznie(() => api("/api/plan/opublikuj", {json: {rok: PLN.rok, numer_bzp: nr}})); if (d) { PLN.dane = d; rysujPlanZam(); komunikat(d.ostrzezenie || "Zapisano opublikowaną wersję planu.", !!d.ostrzezenie); }
}
async function plnUruchom(id) {
  const p = PLN.dane.plan.pozycje.find(x => x.id === id); if (!p) return;
  const r = await zalozZamowienie(({json: {rodzaj: p.rodzaj, nazwa: p.przedmiot, sciezka: "nowe", budzet: String(p.wartosc || ""),
    opis: `${p.przedmiot} – pozycja ${p.id} rocznego planu zamówień na rok ${PLN.rok}${PLN.dane.plan.numer_bzp ? " (plan w BZP nr " + PLN.dane.plan.numer_bzp + (p.id_bzp ? ", pozycja " + p.id_bzp : "") + ")" : ""}; orientacyjna wartość ${plnZl(p.wartosc)} netto; termin wszczęcia: ${plnTermin(p)}.`,
    plan: {rok: PLN.rok, id: p.id, id_bzp: p.id_bzp || "", numer_bzp: PLN.dane.plan.numer_bzp || ""}}}));
  if (!r || !r.id) return;
  await bezpiecznie(() => api("/api/plan/powiaz", {json: {rok: PLN.rok, id, projekt_id: r.id}}));
  komunikat("Utworzono postępowanie z pozycji planu – otwieram kreator.");
  KZN = {rodzaj: p.rodzaj, sciezka: "nowe"}; PROJEKT_ID = r.id; TRYB = "zamowienie"; pokaz("zam_projekty"); otworzProjekt(r.id);
}

// ================================================================ ROCZNY PLAN ZAMÓWIEŃ / SPRAWOZDANIA DO UZP – ekran wyboru
function plnPowrot() { return `<button class="maly" data-ik="cofnij" style="margin-bottom:8px" onclick="pokaz('plan_spr')">Roczny plan zamówień / Sprawozdania do UZP</button>`; }
async function ladujPlanSpr() {
  const dzis = new Date(), rokP = dzis.getFullYear() + (dzis.getMonth() >= 9 ? 1 : 0), rokS = dzis.getFullYear() - (dzis.getMonth() < 3 ? 1 : 0);
  $("#plan-spr").innerHTML = '<p class="opis">Wczytywanie…</p>';
  const [p, sp] = await Promise.all([api("/api/plan?rok=" + rokP).catch(() => null), api("/api/sprawozdanie?rok=" + rokS).catch(() => null)]);
  const ps = p && p.podsumowanie, termin = p && (p.kontrole || []).find(k => /Termin publikacji/.test(k.opis));
  const karta = (w, ikona, tytul, opis, stan) => `<button class="kafel" style="min-height:190px" onclick="${w}"><span class="kafel-ik">${ik(ikona)}</span><b>${tytul}</b>
      <span class="kafel-opis">${opis}</span><span class="kafel-licznik">${stan}</span></button>`;
  $("#plan-spr").innerHTML = `<div class="kafle" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
    ${karta(`PLN.rok=${rokP}; pokaz('plan_zam')`, "kalendarz", "Roczny plan zamówień",
      "Plan postępowań (art. 23 Pzp): pozycje z budżetu, kontrola dzielenia zamówień, tabele do BZP, aktualizacje; 30 dni od przyjęcia budżetu.",
      ps ? `Rok ${rokP}: ${ps.pozycji} pozycji, w planie do BZP ${ps.w_planie_postepowan}${p.wersje.length ? ` · opublikowany (wersji: ${p.wersje.length})` : termin ? " · " + esc(termin.opis.split(" – ")[0]) : " · nieopublikowany"}` : "")}
    ${karta(`pokaz('sprawozdanie'); setTimeout(()=>ladujSprawozdanie(${rokS}),50)`, "tabela", "Sprawozdania do UZP",
      "Roczne sprawozdanie o udzielonych zamówieniach (art. 82 Pzp): zamówienia z projektów i dodane ręcznie, sekcje formularza, arkusz do przepisania – do 1 marca.",
      sp ? `Za rok ${rokS}: ${(sp.pozycje || []).length} zamówień w rejestrze · termin: 1 marca ${rokS + 1}` : "")}
  </div>`;
  wstawIkony($("#plan-spr"));
}

// ================================================================ SZACOWANIE WARTOŚCI ZAMÓWIENIA (art. 28–36 Pzp) – zamawiający publiczny
function szacPanel(S) {
  const sz = S.szacowanie || {}, w = S.szac_wynik || {}, P = S.szac_podstawy || {}, R = S.rodzaj === "roboty", dk = sz.dokument || {}, k = sz.korekty || {};
  const zl2 = v => v ? liczba(v, 2) + " zł" : "–";
  const zrodlo = {szacowanie: "szacowanie wartości", dokumenty: "wartość z dokumentów (do potwierdzenia szacowaniem)", reczna: "wartość wpisana (bez udokumentowanej podstawy)", budzet: "budżet orientacyjny (bez udokumentowanej podstawy)"}[S.netto_zrodlo] || "";
  return `<div class="karta" style="border-left:4px solid var(--akcent);margin:8px 0"><h3 style="margin-top:0">Szacowanie wartości zamówienia (art. 28–36 Pzp)</h3>
    <p class="opis" style="margin-top:0">${R ? "Roboty budowlane: wartość ustala się na podstawie kosztorysu inwestorskiego albo planowanych kosztów z programu funkcjonalno-użytkowego (art. 34 Pzp, metody – rozporządzenie z 20.12.2021 r.). Dokument sporządza projektant albo kosztorysant; program go przyjmuje, odczytuje wartość i sprawdza – AI nie sporządza kosztorysu inwestorskiego."
      : "Dostawy i usługi: wartość ustala się z należytą starannością (art. 28 Pzp) – na podstawie udokumentowanych źródeł cen; przy zamówieniach powtarzających się okresowo – według art. 35."}
      Wartość ustala się nie wcześniej niż ${R ? 6 : 3} miesięcy przed wszczęciem postępowania (art. 36).</p>
    <label class="ks-pole" style="max-width:640px">Podstawa ustalenia wartości<select id="sz-podstawa" onchange="szacZapisz({podstawa: this.value})"><option value="">– wybierz –</option>
      ${Object.entries(P).map(([kk, v]) => `<option value="${kk}" ${sz.podstawa === kk ? "selected" : ""}>${esc(v[0])}</option>`).join("")}</select></label>
    ${sz.podstawa && P[sz.podstawa] ? `<p class="opis" style="margin:2px 0 8px">Podstawa prawna: ${esc(P[sz.podstawa][1])}</p>` : ""}
    ${R ? `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 14px;align-items:end">
        <label class="przycisk" data-ik="wgraj" style="margin:0">${dk.plik ? "Wymień dokument" : (sz.podstawa === "kosztorys_inwestorski" ? "Wgraj kosztorys inwestorski" : "Wgraj zestawienie kosztów (PFU)")}<input type="file" accept=".pdf,.xlsx,.xls,.docx,.ath,.csv" hidden onchange="szacPlik('dokument', this.files[0])"></label>
        <label class="ks-pole">Wartość netto z dokumentu [zł]<input id="sz-dw" inputmode="decimal" value="${dk.wartosc ?? ""}" onchange="szacZapisz({dokument: {...(KZ.szacowanie.dokument || {}), wartosc: this.value}})"></label>
        <label class="ks-pole">Data sporządzenia<input type="date" value="${esc(dk.data || "")}" onchange="szacZapisz({dokument: {...(KZ.szacowanie.dokument || {}), data: this.value}})"></label>
        <label class="ks-pole">Sporządził (projektant / kosztorysant)<input value="${esc(dk.autor || "")}" onchange="szacZapisz({dokument: {...(KZ.szacowanie.dokument || {}), autor: this.value}})"></label></div>
      ${dk.plik ? `<p class="opis" style="margin:6px 0">Dokument: <b>${esc(dk.plik)}</b>${Object.keys(dk.elementy || {}).length ? " · rozpoznane elementy: " + Object.entries(dk.elementy).map(([n, ok]) => `${ok ? "✓" : "✗"} ${esc(n)}`).join(", ") : ""}</p>` : ""}`
    : `<div class="tabela-okno"><table class="tabela" style="margin-top:6px"><tr><th>Źródło</th><th>Opis</th><th>Data</th><th class="liczba">Wartość netto (cały zakres)</th><th>Uwzględnij</th><th></th></tr>
        ${(sz.zrodla || []).map((z, i) => `<tr><td><small>${esc((S.szac_typy || {})[z.typ] || z.typ)}</small></td><td>${esc(z.opis)}${z.plik ? `<br><small class="opis">plik: ${esc(z.plik)}</small>` : ""}</td><td>${esc(z.data || "")}</td>
          <td class="liczba">${zl2(z.wartosc)}</td><td><input type="checkbox" ${z.pominiete ? "" : "checked"} onchange="szacZrodlo(${i}, {pominiete: !this.checked})"></td>
          <td>${sz.metoda === "wybrane" ? `<label><input type="radio" name="sz-wyb" ${sz.zrodlo_wybrane === z.id ? "checked" : ""} onchange="szacZapisz({zrodlo_wybrane: '${z.id}'})"> przyjmij</label> ` : ""}<button class="maly" onclick="szacUsunZrodlo(${i})">Usuń</button></td></tr>`).join("") || '<tr><td colspan="6" class="opis">Brak źródeł – dodaj co najmniej 2–3 niezależne źródła cen.</td></tr>'}</table></div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px 10px;align-items:end;margin-top:6px">
        <label class="ks-pole">Rodzaj źródła<select id="sz-n-typ">${Object.entries(S.szac_typy || {}).map(([kk, t]) => `<option value="${kk}">${esc(t)}</option>`).join("")}</select></label>
        <label class="ks-pole">Opis (wykonawca, zakres, nr umowy)<input id="sz-n-opis"></label>
        <label class="ks-pole">Data<input id="sz-n-data" type="date"></label>
        <label class="ks-pole">Wartość netto [zł]<input id="sz-n-wart" inputmode="decimal"></label>
        <label class="przycisk" data-ik="wgraj" style="margin:0">Plik (opcjonalnie)<input id="sz-n-plik" type="file" hidden onchange="this.parentElement.dataset.plik=this.files[0]?.name||''"></label>
        <button class="glowny" onclick="szacDodajZrodlo()">Dodaj źródło</button></div>
      <div class="pasek" style="flex-wrap:wrap;margin-top:6px"><button class="maly" data-ik="dokument" onclick="szacZapytanie()">Zapytanie o cenę do wykonawców (Word)</button>
        <button class="maly" data-ik="szukaj" onclick="szacCeny()">Ceny z rozstrzygniętych przetargów</button>
        ${S.rodzaj === "uslugi" ? `<button class="maly" data-ik="kalkulator" onclick="pokaz('kalk_pracy')">Kalkulator kosztów pracy</button>` : ""}
        <label class="ks-pole" style="margin:0 0 0 auto">Wyliczenie<select onchange="szacZapisz({metoda: this.value})">${Object.entries(S.szac_metody || {}).map(([kk, t]) => `<option value="${kk}" ${sz.metoda === kk ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label></div>
      <div id="sz-ceny"></div>`}
    <details style="margin-top:8px"><summary>Składniki dodatkowe: prawo opcji, zamówienia z art. 214 ust. 1 pkt 7 i 8, inne</summary>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px 10px;margin-top:6px">
        <label class="ks-pole">Prawo opcji (największy zakres) [zł]<input inputmode="decimal" value="${k.opcje || ""}" onchange="szacZapisz({korekty: {...KZ.szacowanie.korekty, opcje: this.value}})"></label>
        <label class="ks-pole">Zamówienia z art. 214 ust. 1 pkt 7 i 8 [zł]<input inputmode="decimal" value="${k.uzupelniajace || ""}" onchange="szacZapisz({korekty: {...KZ.szacowanie.korekty, uzupelniajace: this.value}})"></label>
        <label class="ks-pole">Inne składniki [zł]<input inputmode="decimal" value="${k.inne || ""}" onchange="szacZapisz({korekty: {...KZ.szacowanie.korekty, inne: this.value}})"></label>
        <label class="ks-pole" style="grid-column:1/-1">Uzasadnienie składników / uwagi<input value="${esc(k.opis || "")}" onchange="szacZapisz({korekty: {...KZ.szacowanie.korekty, opis: this.value}})"></label></div></details>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 14px;margin-top:8px">
      <label class="ks-pole">Data ustalenia wartości<input type="date" value="${esc(sz.data_ustalenia || "")}" onchange="szacZapisz({data_ustalenia: this.value})"></label>
      <label class="ks-pole">Ustalił(a)<input value="${esc(sz.osoba || "")}" onchange="szacZapisz({osoba: this.value})"></label>
      <label class="ks-pole">Planowana data wszczęcia<input type="date" value="${esc(S.K.data_wszczecia || "")}" onchange="zapiszKreator({data_wszczecia: this.value})"></label></div>
    <p style="font-size:17px;margin:10px 0 4px">Wartość zamówienia netto: <b>${zl2(w.netto)}</b>${w.szczegoly ? ` <small class="opis">(${esc(w.szczegoly)})</small>` : ""}</p>
    ${S.netto && S.netto_zrodlo !== "szacowanie" ? `<p class="opis" style="margin:0">Obecnie tryb liczony z: ${esc(zrodlo)} – ${zl2(S.netto)}. Uzupełnij szacowanie.</p>` : ""}
    ${(w.ostrzezenia || []).length ? `<ul class="lista">${w.ostrzezenia.map(o => `<li class="${o.waga === "blad" ? "czerwone" : ""}">${o.waga === "ostrzezenie" ? "⚠ " : ""}${esc(o.opis)}</li>`).join("")}</ul>` : '<p class="opis">Szacowanie kompletne.</p>'}
    <div class="pasek"><button class="${w.kompletne ? "glowny" : ""}" data-ik="dokument" onclick="notatkaSzacowania()">Notatka z szacowania (Word)</button>
      ${S.netto ? `<button class="glowny" onclick="KZ_AKT='warunki'; rysujKreator()">Dalej →</button>` : ""}</div></div>`;
}
async function szacZapisz(zmiana) {
  const sz = {...(KZ.szacowanie || {}), ...zmiana};
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/szacowanie`, {json: {szacowanie: sz}})); if (r) { KZ = r; rysujKreator(); }
}
function szacZrodlo(i, zmiana) { const L = [...(KZ.szacowanie.zrodla || [])]; L[i] = {...L[i], ...zmiana}; szacZapisz({zrodla: L}); }
function szacUsunZrodlo(i) { const L = [...(KZ.szacowanie.zrodla || [])]; L.splice(i, 1); szacZapisz({zrodla: L}); }
async function szacDodajZrodlo(dane) {
  let z = dane;
  if (!z) {
    const f = $("#sz-n-plik").files[0]; let plik = "";
    if (f) { const fd = new FormData(); fd.append("plik", f); fd.append("cel", "zrodlo"); const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/szacowanie/plik`, {method: "POST", body: fd})); plik = r ? r.plik : ""; }
    z = {typ: $("#sz-n-typ").value, opis: $("#sz-n-opis").value, data: $("#sz-n-data").value, wartosc: $("#sz-n-wart").value, plik};
  }
  if (!z.wartosc) return komunikat("Podaj wartość netto źródła (za cały zakres zamówienia).", true);
  szacZapisz({zrodla: [...(KZ.szacowanie.zrodla || []), z]});
}
async function szacPlik(cel, f) {
  if (!f) return; const fd = new FormData(); fd.append("plik", f); fd.append("cel", cel);
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/szacowanie/plik`, {method: "POST", body: fd})); if (!r) return;
  KZ = r; rysujKreator();
  const o = r.odczyt || {}; komunikat(o.wartosc ? `Odczytano z dokumentu: ${liczba(o.wartosc, 2)} zł netto${o.data ? ", data " + o.data : ""} – sprawdź i popraw w razie potrzeby.` : "Dokument zapisany – nie odczytano wartości automatycznie, wpisz ją z dokumentu.");
}
async function szacZapytanie() { const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/szacowanie/zapytanie`, {json: {}})); if (r) location.href = r.url; }
async function szacCeny() {
  const q = prompt("Słowa do wyszukania w rozstrzygniętych przetargach (przedmiot):", PROJEKT.nazwa || ""); if (!q) return;
  const r = await bezpiecznie(() => api(`/api/projekty/${PROJEKT_ID}/szacowanie/ceny?q=${encodeURIComponent(q)}`)); if (!r) return;
  SZ_CENY = r.lista;
  $("#sz-ceny").innerHTML = r.lista.length ? `<p class="opis">${esc(r.uwaga)}</p><div class="tabela-okno"><table class="tabela"><tr><th>Przedmiot</th><th>Zamawiający</th><th>Wykonawca</th><th class="liczba">Cena (brutto)</th><th>Ofert</th><th>Data</th><th></th></tr>
    ${r.lista.map((x, i) => `<tr><td><small>${esc(x.przedmiot || "")}</small></td><td><small>${esc(x.zamawiajacy || "")}</small></td><td><small>${esc(x.wykonawca || "")}</small></td><td class="liczba">${liczba(x.cena || 0, 2)} zł</td><td>${x.ofert ?? "–"}</td><td>${esc(x.data || "")}</td>
      <td><button class="maly" onclick="szacDodajCene(${i})">Dodaj (netto)</button></td></tr>`).join("")}</table></div>`
    : '<p class="opis">Brak podobnych rozstrzygnięć w pamięci programu – spróbuj innych słów albo skorzystaj z zapytań o cenę.</p>';
}

let SZ_CENY = [];
function szacDodajCene(i) {
  const x = SZ_CENY[i]; if (!x) return;
  szacDodajZrodlo({typ: "przetarg", opis: `${x.przedmiot || ""} – ${x.zamawiajacy || ""} (${x.numer || ""}); cena brutto ${liczba(x.cena || 0, 2)} zł przeliczona na netto (23%) – sprawdź zakres`.slice(0, 290),
    data: x.data || "", wartosc: Math.round((x.cena || 0) / 1.23 * 100) / 100});
}

function sekcjaSzacowania(p) {  // zamawiający publiczny: zamiast „kosztorysu inwestorskiego (AI)” – szacowanie wartości według przepisów
  const K = p.kreator || {}, sz = K.szacowanie || {}, R = (K.rodzaj || p.rodzaj_zamowienia) === "roboty";
  const n = (sz.dokument || {}).wartosc || null, zr = (sz.zrodla || []).filter(z => z.wartosc && !z.pominiete).length;
  const stan = sz.podstawa ? (R ? (n ? `wartość z dokumentu: ${liczba(n, 2)} zł netto` : "brak wartości z dokumentu") : `źródeł cen: ${zr}`) : "nie wybrano podstawy";
  return `<div class="krok k-ziel" id="sek-kosztorys"><div class="tytul"><span class="nr">${ik("dokument")}</span><h3>2. Szacowanie wartości zamówienia</h3><span class="stan">${sz.podstawa ? "w toku" : "do zrobienia"}</span></div>
    <div class="tresc"><p class="opis" style="margin-top:0">${R ? "Roboty budowlane – podstawą wartości jest kosztorys inwestorski albo planowane koszty z programu funkcjonalno-użytkowego (art. 34 Pzp), sporządzone przez projektanta albo kosztorysanta. Program nie przygotowuje kosztorysu inwestorskiego przez AI."
      : "Dostawy i usługi – wartość ustala się z należytą starannością na podstawie udokumentowanych źródeł cen (art. 28 i 35 Pzp)."} Wynik: notatka z szacowania wartości zamówienia.</p>
      <p><b>Stan:</b> ${esc(stan)}</p>
      <div class="pasek"><button class="glowny" onclick="KZ_AKT='wartosc'; rysujKreator(); document.getElementById('kreator-zam').scrollIntoView({behavior:'smooth'})">Przejdź do szacowania (kreator, krok „Wartość i tryb”)</button></div></div></div>`;
}

async function kontoWindykacja(login, dostep) {
  const r = await bezpiecznie(() => api("/api/uzytkownicy/windykacja", {json: {login, dostep}}));
  if (r) komunikat(`Windykacja: ${dostep ? "udostępniono" : "odebrano dostęp"} – ${login}.`);
}

// ================================================================ WINDYKACJA
let WN = {dane: null, zak: "pulpit", edycja: null, wynik: null};
async function ladujWind() { const d = await bezpiecznie(() => api("/api/wind")); if (d) { WN.dane = d; rysujWind(); } }
function wnZl(v) { return liczba(v || 0, 2) + " zł"; }
function wnKlucz(f) { return f.nip || (f.kontrahent || "").toLowerCase().slice(0, 60); }
function rysujWind() {
  const d = WN.dane, p = d.pulpit;
  const zak = [["pulpit", "Pulpit"], ["akcje", `Do zrobienia${d.akcje.length ? ` (${d.akcje.length})` : ""}`], ["faktury", "Faktury"], ["wplaty", `Wpłaty${d.wplaty_nieprzypisane.length ? ` (${d.wplaty_nieprzypisane.length})` : ""}`], ["kontrahenci", "Kontrahenci"], ["ustawienia", "Ustawienia"]];
  $("#windykacja").innerHTML = `<div class="ramka-uwaga" style="margin-top:0">Transakcje handlowe między firmami i z podmiotami publicznymi: odsetki ustawowe za opóźnienie (teraz ${String(p.stawka_aktualna).replace(".", ",")}% rocznie) i rekompensata 40/70/100 € należą się od dnia po terminie zapłaty – bez wezwania. Przypomnienia program przygotowuje, a Ty wysyłasz je ze swojej poczty; noty i wezwania wymagają Twojego zatwierdzenia.${p.stawka_do_sprawdzenia ? " <b>Stawka odsetek wymaga aktualizacji na nowe półrocze.</b>" : ""}</div>
    <div class="pasek" style="flex-wrap:wrap">${zak.map(([k, t]) => `<button class="${WN.zak === k ? "glowny" : ""}" onclick="WN.zak='${k}'; rysujWind()">${t}</button>`).join("")}</div>
    <div id="wn-tresc">${({pulpit: wnPulpit, akcje: wnAkcje, faktury: wnFaktury, wplaty: wnWplaty, kontrahenci: wnKontrahenci, ustawienia: wnUstawienia, esad: wnEsadPanel})[WN.zak]()}</div>`;
  wstawIkony($("#windykacja"));
}
function wnPulpit() {
  const d = WN.dane, p = d.pulpit;
  const kaf = (t, v, o) => `<div class="kafel" style="cursor:default;min-height:auto"><span class="kafel-opis">${t}</span><b style="font-size:22px">${v}</b>${o ? `<span class="kafel-opis">${o}</span>` : ""}</div>`;
  return `<div class="kafle" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr))">
      ${kaf("Należności otwarte", wnZl(p.otwarte))}${kaf("W tym po terminie", wnZl(p.przeterminowane))}${kaf("Wpływy w ciągu 30 dni", wnZl(p.wplywy_30_dni), "terminy przypadające w 30 dni")}
      ${kaf("Odsetki do żądania", wnZl(p.odsetki), "narosłe do dziś i za zapłaty po terminie")}${kaf("Rekompensaty do żądania", wnZl(p.rekompensaty), "40/70/100 € po kursie NBP")}${kaf("Odzyskane po działaniach", wnZl(p.odzyskane))}</div>
    <h3>Wiek należności po terminie</h3><div class="tabela-okno"><table class="tabela"><tr>${Object.keys(p.wiekowanie).map(k => `<th>${k} dni</th>`).join("")}</tr><tr>${Object.values(p.wiekowanie).map(v => `<td class="liczba">${wnZl(v)}</td>`).join("")}</tr></table></div>
    <h3>Najwięksi dłużnicy</h3>${p.dluznicy.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Kontrahent</th><th>NIP</th><th class="liczba">Po terminie</th><th>Faktur</th><th>Najdłużej (dni)</th></tr>
      ${p.dluznicy.map(x => `<tr><td>${esc(x.kontrahent)}</td><td>${esc(x.nip || "–")}</td><td class="liczba">${wnZl(x.kwota)}</td><td>${x.faktur}</td><td>${x.max_dni}</td></tr>`).join("")}</table></div>` : '<p class="opis">Brak należności po terminie.</p>'}
    ${!d.faktury.length ? `<div class="karta"><b>Zacznij od faktur:</b> ${d.ksef.zrodlo ? `<button class="glowny" onclick="wnKsef()">Pobierz faktury sprzedaży z KSeF</button> albo ` : `wgraj token KSeF w <a href="#" onclick="WN.zak='ustawienia'; rysujWind(); return false">Ustawieniach</a>, albo `}wgraj e-faktury (XML KSeF) lub listę (CSV/Excel) w zakładce <a href="#" onclick="WN.zak='faktury'; rysujWind(); return false">Faktury</a>.</div>` : ""}`;
}
function wnAkcje() {
  const d = WN.dane;
  return `${WN.wynik ? wnWynik() : ""}${d.akcje.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Faktura</th><th>Kontrahent</th><th class="liczba">Do zapłaty</th><th>Dni po terminie</th><th>Działanie</th><th></th></tr>
    ${d.akcje.map(a => `<tr><td>${esc(a.numer)}</td><td>${esc(a.kontrahent)}</td><td class="liczba">${wnZl(a.pozostalo)}</td><td>${a.dni < 0 ? `za ${-a.dni} dni` : a.dni}</td><td>${esc(a.opis)}${a.zgoda ? ' <span class="znacznik">wymaga zatwierdzenia</span>' : ""}</td>
      <td style="white-space:nowrap">${a.akcja === "decyzja" ? `<button class="maly glowny" onclick="wnEsad(wnKlucz(WN.dane.faktury.find(f=>f.id==='${escA(a.faktura)}')))">E-sąd – przygotuj pozew</button><button class="maly" onclick="wnAkcja('${escA(a.faktura)}','decyzja','ugoda')">Ugoda / raty</button><button class="maly" onclick="if(confirm('Odpuścić należność (status: umorzona)?')) wnAkcja('${escA(a.faktura)}','decyzja','odpuszczenie')">Odpuść</button>`
        : `<button class="maly ${a.zgoda ? "" : "glowny"}" onclick="${a.zgoda ? `if(confirm('Zatwierdzasz: ${escA(a.opis)} dla ${escA(a.kontrahent)}?')) ` : ""}wnAkcja('${escA(a.faktura)}','${a.akcja}')">${a.zgoda ? "Zatwierdź i przygotuj" : "Przygotuj wiadomość"}</button>`}</td></tr>`).join("")}</table></div>`
    : '<p class="opis">Nic do zrobienia – wszystkie działania z harmonogramu wykonane albo brak należności po terminie.</p>'}`;
}
function wnWynik() {
  const w = WN.wynik; if (!w) return "";
  if (w.temat) return `<div class="karta" style="border-left:4px solid var(--akcent)"><b>Wiadomość do wysłania:</b> ${esc(w.temat)}<pre style="white-space:pre-wrap;font-family:inherit;background:var(--tlo-2,#F4F7FB);padding:8px;border-radius:6px">${esc(w.tresc)}</pre>
    <div class="pasek"><a class="przycisk glowny" href="${esc(w.mailto)}">Otwórz w programie pocztowym</a><button onclick="navigator.clipboard.writeText(WN.wynik.tresc); komunikat('Skopiowano treść.')">Kopiuj treść</button><button onclick="WN.wynik=null; rysujWind()">Zamknij</button></div></div>`;
  if (w.url) return `<div class="karta" style="border-left:4px solid var(--akcent)"><b>Dokument gotowy:</b> ${esc(w.plik)}${w.kwoty ? ` <span class="opis">(${Object.entries(w.kwoty).map(([k, v]) => k + ": " + wnZl(v)).join(", ")})</span>` : ""}
    <div class="pasek"><a class="przycisk glowny" href="${esc(w.url)}">Pobierz (Word)</a><button onclick="WN.wynik=null; rysujWind()">Zamknij</button></div></div>`;
  if (w.decyzja) return `<div class="karta">Zapisano decyzję: <b>${esc(w.decyzja)}</b>.${w.decyzja === "esad" ? " Pozew w e-sądzie (EPU) składasz na portalu e-sad.gov.pl ze swojego konta – roszczenia wymagalne w ostatnich 3 latach; przygotowanie pliku pozwu będzie w kolejnej wersji modułu." : ""} <button class="maly" onclick="WN.wynik=null; rysujWind()">Zamknij</button></div>`;
  return "";
}
async function wnAkcja(faktura, akcja, decyzja) {
  const d = await bezpiecznie(() => api("/api/wind/akcja", {json: {faktura, akcja, decyzja}})); if (!d) return;
  WN.dane = d; WN.wynik = d.wynik; WN.zak = "akcje"; rysujWind();
}
function wnFaktury() {
  const d = WN.dane, e = WN.edycja;
  return `<div class="pasek" style="flex-wrap:wrap;align-items:end"><label class="ks-pole" style="margin:0">Z KSeF od dnia<input id="wn-ksef-od" type="date" value="${esc(d.ksef.pobrano_do || new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10))}"></label>
      <button class="${d.ksef.zrodlo ? "glowny" : ""}" data-ik="pobierz" onclick="wnKsef()" ${d.ksef.zrodlo ? "" : 'title="Najpierw wgraj token KSeF w Ustawieniach"'}>Pobierz z KSeF</button>
      <label class="przycisk" data-ik="wgraj">Wgraj e-faktury XML / listę CSV, Excel<input type="file" multiple accept=".xml,.csv,.xlsx,.txt" hidden onchange="wnImportPliki(this.files)"></label>
      <button data-ik="plus" onclick="WN.edycja={}; rysujWind()">Dodaj fakturę</button></div>
    ${e ? `<div class="karta" style="border:2px solid var(--akcent)"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px 10px">
      ${[["numer", "Numer"], ["kontrahent", "Kontrahent"], ["nip", "NIP"], ["data", "Data wystawienia", "date"], ["termin", "Termin płatności", "date"], ["brutto", "Kwota brutto"], ["transakcja", "Umowa / transakcja (opcjonalnie)"]].map(([k, t, typ]) =>
        `<label class="ks-pole">${t}<input id="wn-e-${k}" type="${typ || "text"}" value="${esc(e[k] ?? "")}"></label>`).join("")}
      <label class="ks-pole" style="flex-direction:row;gap:6px;align-items:center"><input id="wn-e-konsument" type="checkbox" ${e.konsument ? "checked" : ""}> dłużnik – konsument (bez odsetek handlowych i rekompensaty)</label></div>
      <div class="pasek" style="margin-top:6px"><button class="glowny" onclick="wnZapiszFakture()">Zapisz</button><button onclick="WN.edycja=null; rysujWind()">Anuluj</button></div></div>` : ""}
    <div class="tabela-okno"><table class="tabela"><tr><th>Faktura</th><th>Kontrahent</th><th>Termin</th><th class="liczba">Brutto</th><th class="liczba">Pozostało</th><th class="liczba">Odsetki</th><th>Rekompensata</th><th>Status</th><th></th></tr>
    ${d.faktury.map(f => { const s = f.stan, r = f.rekompensata; return `<tr class="${s.przeterminowana ? "czerwone" : ""}"><td>${esc(f.numer)}<br><small class="opis">${esc(f.data)} · ${esc(f.zrodlo)}</small></td>
      <td>${esc(f.kontrahent)}<br><small class="opis">${esc(f.nip || "")}</small></td><td>${esc(f.termin)}${f.termin_z_faktury ? "" : '<br><small class="opis">domyślny</small>'}${s.dni_po_terminie > 0 ? `<br><small class="czerwone">${s.dni_po_terminie} dni po terminie</small>` : ""}</td>
      <td class="liczba">${wnZl(f.brutto)}</td><td class="liczba">${wnZl(s.pozostalo)}</td><td class="liczba">${s.odsetki ? wnZl(s.odsetki) : "–"}</td>
      <td>${r ? (r.pierwsza ? `${r.eur} € = ${wnZl(r.zl)}${r.faktur_w_grupie > 1 ? `<br><small class="opis">za ${r.faktur_w_grupie} faktury (1 transakcja)</small>` : ""}` : '<small class="opis">w ramach tej samej transakcji</small>') : "–"}</td>
      <td><select onchange="wnStatus('${f.id}', this.value)">${d.statusy.map(x => `<option ${x === f.status ? "selected" : ""}>${x}</option>`).join("")}</select></td>
      <td style="white-space:nowrap">${s.pozostalo > 0 ? `<button class="maly" onclick="wnZaplata('${f.id}')">Zapłacono</button>` : ""}<button class="maly" onclick="WN.edycja=WN.dane.faktury.find(x=>x.id==='${f.id}'); rysujWind()">Edytuj</button>
        <button class="maly" onclick="if(confirm('Usunąć fakturę z windykacji?')) wnPost('/api/wind/faktura/usun', {id: '${f.id}'})">Usuń</button></td></tr>`; }).join("") || '<tr><td colspan="9" class="opis">Brak faktur.</td></tr>'}</table></div>`;
}
function wnWplaty() {
  const d = WN.dane, otw = d.faktury.filter(f => f.stan.pozostalo > 0);
  return `<p class="opis">Wgraj wyciąg z banku (CSV albo Excel). Program dopasuje wpłaty do faktur po numerze faktury w tytule przelewu albo po NIP i kwocie; pozostałe przypiszesz ręcznie.</p>
    <label class="przycisk glowny" data-ik="wgraj">Wgraj wyciąg bankowy<input type="file" accept=".csv,.xlsx,.txt" hidden onchange="wnWyciag(this.files[0])"></label>
    <h3>Wpłaty nieprzypisane</h3>${d.wplaty_nieprzypisane.length ? `<div class="tabela-okno"><table class="tabela"><tr><th>Data</th><th class="liczba">Kwota</th><th>Tytuł</th><th>Nadawca</th><th>Przypisz do faktury</th></tr>
      ${d.wplaty_nieprzypisane.map(w => `<tr><td>${esc(w.data)}</td><td class="liczba">${wnZl(w.kwota)}</td><td><small>${esc(w.tytul)}</small></td><td><small>${esc(w.nadawca)}</small></td>
        <td><select onchange="if(this.value) wnPost('/api/wind/wplata/przypisz', {wplata: '${w.id}', faktura: this.value})"><option value="">– wybierz –</option>${otw.map(f => `<option value="${f.id}">${esc(f.numer)} · ${esc(f.kontrahent).slice(0, 30)} · ${wnZl(f.stan.pozostalo)}</option>`).join("")}</select></td></tr>`).join("")}</table></div>`
      : '<p class="opis">Brak nieprzypisanych wpłat.</p>'}`;
}
function wnKontrahenci() {
  const d = WN.dane, K = {};
  d.faktury.forEach(f => { const k = wnKlucz(f); (K[k] = K[k] || {klucz: k, nazwa: f.kontrahent, nip: f.nip, kwota: 0}).kwota += f.stan.pozostalo; });
  return `<p class="opis">Rekompensata należy się raz od transakcji (umowy) – domyślnie program liczy jedną na kontrahenta. Zaznacz „osobne transakcje”, gdy każda faktura to osobne zlecenie albo umowa.</p>
    <div class="tabela-okno"><table class="tabela"><tr><th>Kontrahent</th><th class="liczba">Do zapłaty</th><th>E-mail do przypomnień</th><th>Osobne transakcje</th><th>Publiczny podmiot leczniczy</th><th>Wykaz VAT</th><th></th></tr>
    ${Object.values(K).map(k => { const u = d.kontrahenci[k.klucz] || {}, sp = u.sprawdzenie; return `<tr><td>${esc(k.nazwa)}<br><small class="opis">${esc(k.nip || "")}</small></td><td class="liczba">${wnZl(k.kwota)}</td>
      <td><input value="${esc(u.email || "")}" placeholder="adres e-mail" onchange="wnPost('/api/wind/kontrahent', {klucz: '${escA(k.klucz)}', email: this.value})"></td>
      <td><input type="checkbox" ${u.osobne_transakcje ? "checked" : ""} onchange="wnPost('/api/wind/kontrahent', {klucz: '${escA(k.klucz)}', osobne_transakcje: this.checked})"></td>
      <td><input type="checkbox" ${u.leczniczy ? "checked" : ""} onchange="wnPost('/api/wind/kontrahent', {klucz: '${escA(k.klucz)}', leczniczy: this.checked})"></td>
      <td>${sp ? `<small>${esc(sp.status_vat)} (${esc(sp.data)})${sp.krs ? "<br>KRS " + esc(sp.krs) : ""}</small>` : '<small class="opis">nie sprawdzono</small>'}</td>
      <td style="white-space:nowrap">${k.kwota > 0 ? `<button class="maly" onclick="wnEsad('${escA(k.klucz)}')">Pozew (e-sąd)</button>` : ""}${k.nip ? `<button class="maly" onclick="wnPost('/api/wind/kontrahent', {klucz: '${escA(k.klucz)}', sprawdz: true})">Sprawdź</button>
        <a class="maly" href="https://krz.ms.gov.pl/" target="_blank" rel="noopener" title="Krajowy Rejestr Zadłużonych – sprawdź upadłość i restrukturyzację">KRZ</a>` : ""}</td></tr>`; }).join("") || '<tr><td colspan="7" class="opis">Brak kontrahentów.</td></tr>'}</table></div>
    <p class="opis">Przed pozwem sprawdź dłużnika w Krajowym Rejestrze Zadłużonych: przy upadłości albo restrukturyzacji zamiast pozwu zgłasza się wierzytelność.</p>`;
}
function wnUstawienia() {
  const u = WN.dane.ustawienia, h = u.harmonogram || {};
  return `<div class="karta"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 14px">
      <label class="ks-pole" style="grid-column:1/-1">Nadawca (nazwa, adres, NIP – na notach i wezwaniach)<input id="wn-u-nadawca" value="${esc(u.nadawca || "")}"></label>
      <label class="ks-pole">Numer rachunku<input id="wn-u-rachunek" value="${esc(u.rachunek || "")}"></label>
      <label class="ks-pole">Telefon (w przypomnieniach)<input id="wn-u-telefon" value="${esc(u.telefon || "")}"></label>
      <label class="ks-pole">Domyślny termin płatności (dni), gdy brak na fakturze<input id="wn-u-termin" type="number" value="${esc(String(u.termin_domyslny || 14))}"></label></div>
    <h3>Harmonogram (dni względem terminu płatności)</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px 10px">
      ${Object.entries(WN.dane.akcje_opis).map(([k, t]) => `<label class="ks-pole">${esc(t)} – ${k === "przed" ? "dni przed" : "dni po"}<input class="wn-h" data-k="${k}" type="number" value="${h[k] ?? ""}"></label>`).join("")}</div>
    ${wnKsefUstawienia()}
    <button class="glowny" style="margin-top:8px" onclick="wnPost('/api/wind/ustawienia', {nadawca: $('#wn-u-nadawca').value, rachunek: $('#wn-u-rachunek').value, telefon: $('#wn-u-telefon').value, termin_domyslny: $('#wn-u-termin').value, harmonogram: Object.fromEntries([...document.querySelectorAll('.wn-h')].map(i => [i.dataset.k, i.value]))}).then(()=>komunikat('Zapisano ustawienia.'))">Zapisz ustawienia</button></div>`;
}
async function wnPost(url, json) { const d = await bezpiecznie(() => api(url, {json})); if (d) { WN.dane = d; rysujWind(); } return d; }
function wnStatus(id, status) { wnPost("/api/wind/status", {id, status}); }
function wnZaplata(id) {
  const f = WN.dane.faktury.find(x => x.id === id);
  const kw = prompt(`Kwota zapłaty (pozostało ${wnZl(f.stan.pozostalo)}):`, String(f.stan.pozostalo).replace(".", ",")); if (kw === null) return;
  const data = prompt("Data zapłaty (RRRR-MM-DD):", new Date().toISOString().slice(0, 10)); if (!data) return;
  wnPost("/api/wind/zaplata", {id, kwota: kw, data});
}
function wnZapiszFakture() {
  const f = {...(WN.edycja || {})}; ["numer", "kontrahent", "nip", "data", "termin", "brutto", "transakcja"].forEach(k => f[k] = $("#wn-e-" + k).value); f.konsument = $("#wn-e-konsument").checked;
  if (f.termin) f.termin_z_faktury = true;
  wnPost("/api/wind/faktura", {faktura: f}).then(d => { if (d) { WN.edycja = null; rysujWind(); } });
}
async function wnKsef() {
  if (!WN.dane.ksef.zrodlo) { WN.zak = "ustawienia"; rysujWind(); return komunikat("Wgraj token KSeF (Ustawienia → KSeF) albo zapisz go w Księgowości.", true); }
  const od = $("#wn-ksef-od") ? $("#wn-ksef-od").value : "";
  const z = await bezpiecznie(() => api("/api/wind/ksef/pobierz", {json: {od}})); if (!z) return;
  sledz(z, () => { WN.zak = "faktury"; ladujWind(); });
}
async function wnImportPliki(pliki) {
  if (!pliki || !pliki.length) return; const fd = new FormData(); [...pliki].forEach(p => fd.append("pliki", p));
  const d = await bezpiecznie(() => api("/api/wind/import/plik", {method: "POST", body: fd})); if (!d) return;
  WN.dane = d; rysujWind(); komunikat(`Dodano ${d.dodano} faktur${d.pominiete ? `, pominięto ${d.pominiete} (nie sprzedaż albo nieczytelne)` : ""}.${d.uwaga ? " " + d.uwaga : ""}`, !!d.uwaga);
}
async function wnWyciag(plik) {
  if (!plik) return; const fd = new FormData(); fd.append("plik", plik);
  const d = await bezpiecznie(() => api("/api/wind/wyciag", {method: "POST", body: fd})); if (!d) return;
  WN.dane = d; rysujWind(); komunikat(`Wczytano ${d.wplat} wpłat, dopasowano ${d.dopasowano}.`);
}

function wnKsefUstawienia() {
  const k = WN.dane.ksef;
  const stan = k.zrodlo === "wlasny" ? "własny token (zapisany w Windykacji)" : k.zrodlo === "ksiegowosc" ? "token z Księgowości tego konta" : "brak tokenu";
  return `<h3>KSeF – pobieranie faktur sprzedaży</h3>
    <p class="opis" style="margin-top:0">Windykacja pobiera z KSeF tylko faktury sprzedaży (oszczędza limit ok. 60 faktur na godzinę), przyrostowo – tylko nowe. Token: jeśli wgrasz własny, program użyje jego; jeśli nie – użyje tokenu zapisanego w Księgowości tego konta. Token jest przechowywany zaszyfrowany i nie wraca do przeglądarki.</p>
    <p><b>Token:</b> ${esc(stan)}${k.ostatnia ? ` · ostatnie pobranie: ${esc(k.ostatnia)}` : ""}${k.zostalo ? ` · <b>do pobrania zostało ${k.zostalo}</b> – uruchom ponownie za godzinę` : ""}</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:6px 10px;align-items:end">
      <label class="ks-pole">NIP firmy (sprzedawcy)<input id="wn-k-nip" value="${esc(k.nip || "")}"></label>
      <label class="ks-pole">Środowisko<select id="wn-k-srod">${k.srodowiska.map(x => `<option ${x === k.srodowisko ? "selected" : ""}>${x}</option>`).join("")}</select></label>
      <label class="ks-pole">Własny token KSeF${k.wlasny ? " (zapisany – wpisz nowy, aby zmienić)" : ""}<input id="wn-k-token" type="password" autocomplete="off" placeholder="wklej token z aplikacji KSeF"></label>
      <div class="pasek" style="margin:0"><button onclick="wnPost('/api/wind/ksef/token', {token: $('#wn-k-token').value, nip: $('#wn-k-nip').value, srodowisko: $('#wn-k-srod').value}).then(d => d && komunikat('Zapisano ustawienia KSeF.'))">Zapisz KSeF</button>
        ${k.wlasny ? `<button class="maly" onclick="if(confirm('Usunąć własny token? Windykacja użyje wtedy tokenu z Księgowości, jeśli jest.')) wnPost('/api/wind/ksef/token', {usun: true})">Usuń własny token</button>` : ""}</div></div>
    <p class="opis">Uwaga: tokeny KSeF wygasają 31 grudnia 2026 r. – od 2027 r. logowanie wymaga certyfikatu KSeF.</p>`;
}

// ---------------------------------------------------------------- E-SĄD – pozew w elektronicznym postępowaniu upominawczym
async function wnEsad(klucz, skap) {
  WN.esadKlucz = klucz; WN.esadSkap = skap !== false;
  const d = await bezpiecznie(() => api(`/api/wind/esad?klucz=${encodeURIComponent(klucz)}&skap=${WN.esadSkap ? 1 : 0}`)); if (!d) return;
  WN.esad = d; WN.esadWynik = null; WN.zak = "esad"; rysujWind(); window.scrollTo(0, 0);
}
function wnPolaStrony(pref, p, rodzaje, zPeselem) {
  const a = p.adres || {}, os = ["0", "1"].includes(String(p.rodzaj));
  const OPC = ["nr_mieszkania", "stanowisko", "regon", "krs", "nazwa"];  // pola opcjonalne – bez podświetlenia braku
  const pole = (k, t, v, styl) => `<label class="ks-pole"${styl ? ` style="${styl}"` : ""}>${t}<input id="${pref}-${k}" value="${esc(v ?? "")}" class="${v || OPC.includes(k) ? "" : "do-uzupelnienia"}"></label>`;
  return `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:6px 10px">
    ${rodzaje ? `<label class="ks-pole" style="grid-column:1/-1">Rodzaj<select id="${pref}-rodzaj" onchange="wnEsadZapiszStrony(true)">${Object.entries(rodzaje).map(([k, t]) => `<option value="${k}" ${String(p.rodzaj) === k ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></label>` : ""}
    ${!rodzaje || os ? pole("imie", "Imię", p.imie) + pole("nazwisko", "Nazwisko", p.nazwisko) : ""}
    ${rodzaje ? pole("nazwa", os ? "Nazwa firmy (opcjonalnie)" : "Nazwa", p.nazwa, "grid-column:span 2") : ""}
    ${zPeselem ? `<label class="ks-pole">PESEL<input id="${pref}-pesel" placeholder="${esc(p.pesel || "11 cyfr")}" class="${p.pesel ? "" : "do-uzupelnienia"}" inputmode="numeric" autocomplete="off"></label>
      ${pole("stanowisko", "Stanowisko / funkcja", p.stanowisko)}${pole("podstawa", "Podstawa umocowania", p.podstawa || "właściciel – wpis w CEIDG", "grid-column:span 2")}` : ""}
    ${rodzaje ? pole("nip", "NIP", p.nip) + (!os ? pole("krs", "KRS", p.krs) + pole("regon", "REGON", p.regon) + pole("siedziba", "Siedziba", p.siedziba) : "") : ""}
    ${pole("ulica", "Ulica", a.ulica)}${pole("nr_domu", "Nr domu", a.nr_domu)}${pole("nr_mieszkania", "Nr lokalu", a.nr_mieszkania)}${pole("kod", "Kod pocztowy", a.kod)}${pole("miejscowosc", "Miejscowość", a.miejscowosc)}</div>`;
}
function wnZbierzStrone(pref, rodzaje) {
  const v = k => ($(`#${pref}-${k}`) || {}).value || "";
  const o = {imie: v("imie"), nazwisko: v("nazwisko"), adres: {ulica: v("ulica"), nr_domu: v("nr_domu"), nr_mieszkania: v("nr_mieszkania"), kod: v("kod"), miejscowosc: v("miejscowosc")}};
  if (rodzaje) Object.assign(o, {rodzaj: v("rodzaj"), nazwa: v("nazwa"), nip: v("nip"), krs: v("krs"), regon: v("regon"), siedziba: v("siedziba")});
  else Object.assign(o, {pesel: v("pesel"), stanowisko: v("stanowisko"), podstawa: v("podstawa")});
  return o;
}
async function wnEsadZapiszStrony(odswiez) {
  const E = WN.esad;
  const r1 = await bezpiecznie(() => api("/api/wind/esad/ustawienia", {json: {skladajacy: wnZbierzStrone("es-sk"), powod: wnZbierzStrone("es-pw", E.rodzaje_strony)}}));
  const r2 = await bezpiecznie(() => api("/api/wind/esad/pozwany", {json: {klucz: WN.esadKlucz, pozwany: wnZbierzStrone("es-pz", E.rodzaje_strony), uzasadnienie: $("#es-uz") ? $("#es-uz").value : undefined}}));
  if (r1 && r2) { await wnEsad(WN.esadKlucz, WN.esadSkap); if (!odswiez) komunikat("Zapisano dane pozwu."); }
}
function wnEsadPanel() {
  const E = WN.esad; if (!E) return '<p class="opis">Wybierz kontrahenta.</p>';
  const D = E.dane, bl = E.kontrola.filter(u => u.waga === "blad");
  return `<div class="pasek"><button class="maly" data-ik="cofnij" onclick="WN.zak='kontrahenci'; rysujWind()">Kontrahenci</button></div>
    <h3 style="margin-top:4px">Pozew do e-sądu (EPU): ${esc(D.kontrahent)}</h3>
    <p class="opis" style="margin-top:0">${esc(E.sad.nazwa)}, ${esc(E.sad.wydzial)}. Program przygotowuje pozew i plik do importu zgodny z oficjalnym schematem e-sądu; w e-sądzie wczytujesz plik, podpisujesz (podpis EPU) i opłacasz – po opłacie pozew trafia do sądu automatycznie. Program nie składa pozwu za Ciebie.</p>
    ${E.zlozony ? `<div class="ramka-uwaga">Pozew złożony ${esc(E.zlozony.data)}${E.zlozony.sygnatura ? ", sygnatura " + esc(E.zlozony.sygnatura) : ""}. Średni czas oczekiwania na nakaz zapłaty w 2025 r.: 49 dni.</div>` : ""}
    <div class="karta"><b>Kontrola przed pozwem</b>${E.kontrola.length ? `<ul class="lista">${E.kontrola.map(u => `<li class="${u.waga === "blad" ? "czerwone" : ""}">${u.waga === "ostrzezenie" ? "⚠ " : ""}${esc(u.opis)}</li>`).join("")}</ul>` : '<p class="opis">✓ Wszystkie warunki spełnione.</p>'}
      <p class="opis" style="margin:4px 0 0">Przed złożeniem sprawdź dłużnika w <a href="https://krz.ms.gov.pl/" target="_blank" rel="noopener">Krajowym Rejestrze Zadłużonych</a> – przy upadłości albo restrukturyzacji zamiast pozwu zgłasza się wierzytelność.</p></div>
    <div class="karta"><h3 style="margin-top:0">Osoba składająca pozew</h3><p class="opis" style="margin-top:0">Osoba z kontem w e-sądzie (wymaga PESEL), uprawniona do reprezentacji powoda. PESEL jest przechowywany zaszyfrowany.</p>${wnPolaStrony("es-sk", E.skladajacy, null, true)}</div>
    <div class="karta"><h3 style="margin-top:0">Powód</h3>${wnPolaStrony("es-pw", E.powod, E.rodzaje_strony)}<p class="opis">Rachunek do zapłaty i zwrotu opłat: ${E.rachunek ? esc(E.rachunek) : '<b class="czerwone">brak – uzupełnij w Ustawieniach</b>'}</p></div>
    <div class="karta"><h3 style="margin-top:0">Pozwany</h3><p class="opis" style="margin-top:0">Dane wypełnione z wykazu VAT – sprawdź adres (doręczenie nakazu).</p>${wnPolaStrony("es-pz", E.pozwany, E.rodzaje_strony)}</div>
    <div class="pasek"><button class="glowny" onclick="wnEsadZapiszStrony()">Zapisz dane stron</button></div>
    <div class="karta"><h3 style="margin-top:0">Roszczenia</h3>
      <label><input type="checkbox" ${WN.esadSkap ? "checked" : ""} onchange="wnEsad(WN.esadKlucz, this.checked)"> dochodź też skapitalizowanych odsetek za faktury zapłacone po terminie</label>
      <div class="tabela-okno"><table class="tabela"><tr><th>Lp.</th><th>Roszczenie</th><th class="liczba">Kwota</th><th>Odsetki</th><th>Dowody</th></tr>
      ${D.roszczenia.map((r, i) => `<tr><td>${i + 1}</td><td>${esc(r.opis)}</td><td class="liczba">${wnZl(r.wartosc)}</td><td><small>${r.odsetki_kod === "15" ? "ustawowe w transakcjach handlowych od " + esc(r.odsetki_od) + " do dnia zapłaty" : r.odsetki_kod ? "ustawowe za opóźnienie od " + esc(r.odsetki_od) + " do dnia zapłaty" : "–"}</small></td><td>${r.dowody.join(", ")}</td></tr>`).join("") || '<tr><td colspan="5" class="opis">Brak roszczeń.</td></tr>'}</table></div>
      <h3>Dowody</h3><ul class="lista">${D.dowody.map(x => `<li>${x.numer}. ${esc(x.typ)}: ${esc(x.oznaczenie)}${x.data ? " z " + esc(x.data) : ""}</li>`).join("") || "<li>brak</li>"}</ul>
      <p class="opis">W e-sądzie dowodów nie załącza się – wskazuje się je w pozwie; przy sprzeciwie sprawa trafia do zwykłego sądu i wtedy przedstawiasz dokumenty.</p></div>
    <div class="karta"><h3 style="margin-top:0">Uzasadnienie</h3><textarea id="es-uz" rows="8" style="width:100%">${esc(E.uzasadnienie)}</textarea>
      <button class="maly" onclick="wnEsadZapiszStrony()">Zapisz uzasadnienie</button></div>
    <div class="karta" style="border-left:4px solid var(--akcent)"><h3 style="margin-top:0">Opłata</h3>
      <p>Wartość przedmiotu sporu: <b>${D.wps} zł</b> · opłata sądowa w EPU: <b>${D.oplata} zł</b></p>
      <p class="opis" style="margin:0">Opłatę wnosisz wyłącznie w systemie e-sądu, przy pozwie („Opłać pozew”). W pozwie żądasz zwrotu kosztów – opłata zostanie zasądzona od pozwanego. Przy cofnięciu pozwu przed wydaniem nakazu opłata jest zwracana.</p></div>
    <div class="pasek" style="flex-wrap:wrap"><button data-ik="dokument" onclick="wnEsadPodglad()">Podgląd pozwu (Word)</button>
      <button class="glowny" ${bl.length ? 'disabled title="Najpierw uzupełnij braki z kontroli"' : ""} onclick="if(confirm('Akceptujesz treść pozwu? Program przygotuje plik do importu w e-sądzie.')) wnEsadAkceptuj()">Akceptuję pozew</button></div>
    ${WN.esadWynik ? wnEsadKroki() : (E.plik ? `<p class="opis">Przygotowany plik: <a href="/api/wind/plik/${encodeURIComponent(E.plik)}">${esc(E.plik)}</a></p>` : "")}
    <div class="karta"><h3 style="margin-top:0">Po złożeniu w e-sądzie</h3><div class="pasek" style="flex-wrap:wrap;align-items:end">
      <label class="ks-pole" style="margin:0">Data złożenia<input id="es-zl-data" type="date" value="${new Date().toISOString().slice(0, 10)}"></label>
      <label class="ks-pole" style="margin:0">Sygnatura / numer sprawy<input id="es-zl-syg" placeholder="np. VI Nc-e 123456/26"></label>
      <button onclick="wnPost('/api/wind/esad/zlozony', {klucz: WN.esadKlucz, data: $('#es-zl-data').value, sygnatura: $('#es-zl-syg').value}).then(d => d && wnEsad(WN.esadKlucz, WN.esadSkap))">Pozew złożony</button></div></div>`;
}
function wnEsadKroki() {
  const w = WN.esadWynik;
  return `<div class="karta" style="border:2px solid var(--akcent)"><h3 style="margin-top:0">Plik pozwu gotowy – zgodny ze schematem e-sądu</h3>
    <div class="pasek"><a class="przycisk glowny" href="${esc(w.url)}">Pobierz plik do importu (XML)</a><a class="przycisk" href="${esc(w.esad)}" target="_blank" rel="noopener">Otwórz e-sąd</a></div>
    <ol class="lista"><li>Zaloguj się na e-sad.gov.pl (nie masz konta? <a href="${esc(w.rejestracja)}" target="_blank" rel="noopener">rejestracja</a> – wymaga PESEL).</li>
      <li>Wybierz import pozwu z pliku XML i wskaż pobrany plik; sprawdź podgląd pozwu w e-sądzie.</li>
      <li>W „Dokumentach do podpisania” podpisz pozew (podpis EPU albo kwalifikowany).</li>
      <li>„Opłać pozew” – ${w.oplata} zł. Po opłacie pozew trafia do sądu automatycznie.</li>
      <li>Wróć tutaj i kliknij „Pozew złożony” z sygnaturą – faktury dostaną status „w sądzie (EPU)”.</li></ol></div>`;
}
async function wnEsadPodglad() { await wnEsadZapiszStrony(true); const r = await bezpiecznie(() => api("/api/wind/esad/podglad", {json: {klucz: WN.esadKlucz, skap: WN.esadSkap}})); if (r) location.href = r.url; }
async function wnEsadAkceptuj() {
  await wnEsadZapiszStrony(true);
  const r = await bezpiecznie(() => api("/api/wind/esad/akceptuj", {json: {klucz: WN.esadKlucz, skap: WN.esadSkap}})); if (!r) return;
  WN.esadWynik = r; WN.zak = "esad"; rysujWind(); location.href = r.url;
}
