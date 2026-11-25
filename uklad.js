// Bidivia – sposób wyświetlania jak w nowej aplikacji (dev.bidivia.eu).
// Tylko prezentacja: górny pasek z logo, zwijane grupy menu, kroki projektu wyświetlane pojedynczo z panelem kroków,
// zwijana lista projektów i dolny pasek zakładek na telefonie. Nie zmienia danych, adresów ani obliczeń z app.js.
(function () {
  "use strict";
  const KOMPUTER = window.matchMedia("(min-width: 1100px)");
  const KONTENERY = ["#projekt", "#realizacja", "#dos-real", "#ocena", "#wniosek"];
  const AKTYWNE = {};          // kontener + projekt → id wyświetlanego kroku
  let LISTA_POKAZANA = false;  // użytkownik rozwinął listę projektów obok otwartego projektu
  const pamiec = {
    czytaj(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    zapisz(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* bez pamięci przeglądarki – działa bez zapamiętania */ } },
  };
  const tekst = (el) => (el ? el.textContent || "" : "").replace(/\s+/g, " ").trim();
  const bezNumeru = (t) => t.replace(/^\s*\d+\.\s*/, "");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const projektId = () => { try { return typeof PROJEKT_ID !== "undefined" && PROJEKT_ID ? PROJEKT_ID : ""; } catch (e) { return ""; } };

  // ---------------------------------------------------------------- 1. górny pasek z logo (komputer)
  function logoWPasku() {
    const gp = document.getElementById("gora-pasek"), m = document.querySelector("header .marka");
    if (!gp || !m || gp.querySelector(".gp-logo")) return;
    const k = m.cloneNode(true);
    k.classList.add("gp-logo");
    gp.prepend(k);
  }

  // ---------------------------------------------------------------- 2. zwijane grupy menu i promienie
  function grupyMenu() {
    const zw = pamiec.czytaj("bdv-menu-zwiniete", {});
    document.querySelectorAll("#nav .nav-grupa").forEach((g, i) => {
      if (i === 0) return;  // główna grupa pracy zawsze rozwinięta
      const klucz = [...g.classList].find((c) => /^g\d$/.test(c)) || "g" + i;
      let n = g.querySelector(":scope > .nav-naglowek");
      if (!n) {
        n = document.createElement("div");  // div, nie przycisk – app.js liczy widoczne przyciski grupy
        n.className = "nav-naglowek";
        n.setAttribute("role", "button");
        n.tabIndex = 0;
        n.innerHTML = `<span>${esc((g.getAttribute("title") || "Więcej").split(":")[0])}</span>
          <svg class="chev" viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        const przelacz = () => { const z = pamiec.czytaj("bdv-menu-zwiniete", {}); z[klucz] = !g.classList.contains("zwinieta"); pamiec.zapisz("bdv-menu-zwiniete", z); stanGrupy(g, z[klucz]); };
        n.addEventListener("click", przelacz);
        n.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); przelacz(); } });
        g.prepend(n);
      }
      stanGrupy(g, !!zw[klucz]);
    });
    const h = document.querySelector("header");
    if (h && !h.querySelector(".side-rays")) {
      const r = document.createElement("div");
      r.className = "side-rays";
      r.innerHTML = `<svg viewBox="0 0 256 120" aria-hidden="true" preserveAspectRatio="none"><path d="M256 6L0 52V78Z" fill="var(--ray-2,#c4d7ec)"/>
        <path d="M256 6L0 88V120H40Z" fill="var(--ray-1,#dbe7f4)"/><path d="M256 6L90 120H150Z" fill="var(--ray-2,#c4d7ec)" opacity=".7"/></svg>`;
      h.appendChild(r);
    }
  }
  function stanGrupy(g, zwinieta) {
    const aktywna = !!g.querySelector("button.akt");
    const z = zwinieta && !aktywna;  // grupa z otwartą stroną zawsze widoczna
    g.classList.toggle("zwinieta", z);
    const n = g.querySelector(":scope > .nav-naglowek");
    if (n) n.setAttribute("aria-expanded", z ? "false" : "true");
  }

  // ---------------------------------------------------------------- 3. kroki projektu pojedynczo + panel kroków
  // pojemniki „przezroczyste” (np. #dotacja, #plan-projektu) – ich kroki należą do kroków projektu (GC-01: dotacje)
  function dzieciKrokow(k) {
    const w = [];
    [...k.children].forEach((e) => { if (e.classList.contains("kroki-przezr")) w.push(...dzieciKrokow(e)); else w.push(e); });
    return w;
  }
  function sekcjeKontenera(k) {
    return dzieciKrokow(k).filter((e) => (e.classList.contains("krok") || e.matches(".karta.przeglad"))
      && (e.id || e.querySelector("h3")) && getComputedStyle(e).display !== "none");
  }
  // „do przygotowania” to nie „gotowe” – słowo „gotow…” liczy się tylko jako osobne słowo
  function zrobione(stan) { return /(^|[^\p{L}])gotow|złożon|sprawdzon|zrobion|zakończ|kompletn|wysłan|✓/iu.test(stan) && !/nie\s+(gotow|złożon|sprawdzon)/i.test(stan); }

  function krokiKontenera(k, sel) {
    if (!k.isConnected || k.offsetParent === null) return;
    if (k.querySelector(".kz-stepper, #kreator-zam")) { wylaczKroki(k); return; }  // kreator zamówienia ma własne kroki
    const S = sekcjeKontenera(k);
    if (S.length < 3) { wylaczKroki(k); return; }
    S.forEach((s, i) => { if (!s.id) s.id = "krok-" + sel.slice(1) + "-" + i; });
    const klucz = sel + ":" + projektId();
    let akt = AKTYWNE[klucz];
    if (!S.some((s) => s.id === akt)) akt = AKTYWNE[klucz] = S[0].id;
    k.classList.add("tryb-kroki");
    // elementy między krokami (np. „Po wygranej”) należą do następnego kroku; elementy przed pierwszym krokiem – zawsze widoczne
    let po = false, nastepny = null;
    const dzieci = dzieciKrokow(k);
    for (let i = dzieci.length - 1; i >= 0; i--) {
      const e = dzieci[i];
      if (e.classList.contains("kroki-panel")) continue;
      if (S.includes(e)) { nastepny = e.id; continue; }
      if (nastepny) e.dataset.krokPrzy = nastepny;
    }
    dzieci.forEach((e) => {
      if (e.classList.contains("kroki-panel")) return;
      if (S.includes(e)) { po = true; e.classList.toggle("kr-ukryty", e.id !== akt); return; }
      if (!po) { e.classList.remove("kr-ukryty"); return; }
      e.classList.toggle("kr-ukryty", (e.dataset.krokPrzy || "") !== akt);
    });
    // panel kroków (prawa kolumna, przyklejony)
    const poz = S.map((s, i) => {
      const nr = tekst(s.querySelector(".tytul .nr")), t = bezNumeru(tekst(s.querySelector("h3")) || "Krok " + (i + 1)), st = tekst(s.querySelector(".tytul .stan"));
      return { id: s.id, nr: /^\d+$/.test(nr) ? nr : String(i + 1), t, st, ok: zrobione(st), przeglad: s.matches(".karta.przeglad") };
    });
    // pasek sekcji na telefonie: zaznaczony aktywny krok
    k.querySelectorAll(":scope > .pasek-sekcji a").forEach((a) => a.classList.toggle("akt", a.getAttribute("href") === "#" + akt));
    document.querySelectorAll("#nav .podmenu a").forEach((a) => a.classList.toggle("akt", a.dataset.cel === akt));
    const sig = JSON.stringify([akt, poz]);
    let p = k.querySelector(":scope > .kroki-panel");
    if (p && p.dataset.sig === sig) return;
    if (!p) { p = document.createElement("div"); p.className = "kroki-panel"; k.prepend(p); }
    p.dataset.sig = sig;
    const ia = poz.findIndex((x) => x.id === akt);
    p.innerHTML = `<nav class="kroki karta" aria-label="Kroki">
      ${k.closest(".uklad") ? `<button type="button" class="kr-lista maly">${LISTA_POKAZANA ? "Ukryj listę projektów" : "Pokaż listę projektów"}</button>` : ""}
      <h2>Kroki</h2>
      ${poz.map((x, i) => `<a href="#${x.id}" data-krok="${x.id}" class="krok-poz${x.ok ? " done" : ""}${x.id === akt ? " active" : ""}"${x.id === akt ? ' aria-current="step"' : ""}>
        <span class="step-mark">${x.ok ? "✓" : x.przeglad ? "●" : esc(x.nr)}</span><span><b>${esc(x.t)}</b>${x.st ? `<small>${esc(x.st)}</small>` : ""}</span></a>`).join("")}
      <div class="kroki-nawig">
        <button type="button" class="maly" data-kier="-1"${ia <= 0 ? " disabled" : ""}>← Poprzedni</button>
        <button type="button" class="maly glowny" data-kier="1"${ia >= poz.length - 1 ? " disabled" : ""}>Następny krok →</button>
      </div></nav>`;
    p.querySelectorAll("a[data-krok]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); pokazKrok(k, sel, a.dataset.krok, true); }));
    p.querySelectorAll("button[data-kier]").forEach((b) => b.addEventListener("click", () => {
      const j = ia + Number(b.dataset.kier); if (poz[j]) pokazKrok(k, sel, poz[j].id, true);
    }));
    const l = p.querySelector(".kr-lista");
    if (l) l.addEventListener("click", () => { LISTA_POKAZANA = !LISTA_POKAZANA; listaProjektow(); p.dataset.sig = ""; plan(); });
  }
  function wylaczKroki(k) {
    if (!k.classList.contains("tryb-kroki")) return;
    k.classList.remove("tryb-kroki");
    dzieciKrokow(k).forEach((e) => e.classList.remove("kr-ukryty"));
    k.querySelectorAll(":scope > .kroki-panel").forEach((e) => e.remove());
  }
  function pokazKrok(k, sel, id, przewin) {
    AKTYWNE[sel + ":" + projektId()] = id;
    krokiKontenera(k, sel);
    if (przewin) {
      const y = k.getBoundingClientRect().top + window.scrollY - (KOMPUTER.matches ? 88 : 72);
      window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
    }
  }
  // przewinięcie z app.js (podmenu, przyciski „przejdź do…”) do ukrytego kroku – najpierw pokazujemy ten krok
  const przewinOryg = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function () {
    try {
      const k = this.closest(".tryb-kroki");
      if (k) {
        const sel = KONTENERY.find((s) => k.matches(s));
        let s = this; while (s && s.parentElement !== k && !(s.parentElement && s.parentElement.classList.contains("kroki-przezr") && k.contains(s.parentElement))) s = s.parentElement;
        const cel = s && (s.classList.contains("krok") || s.matches(".karta.przeglad")) ? s.id : s && s.dataset.krokPrzy;
        if (sel && cel && s.classList.contains("kr-ukryty")) { AKTYWNE[sel + ":" + projektId()] = cel; krokiKontenera(k, sel); }
      }
    } catch (e) { /* zwykłe przewinięcie */ }
    return przewinOryg.apply(this, arguments);
  };

  // ---------------------------------------------------------------- 4. lista projektów zwinięta przy otwartym projekcie (komputer)
  function listaProjektow() {
    document.querySelectorAll(".uklad").forEach((u) => {
      const otw = !!u.querySelector(":scope > .tryb-kroki, :scope > * > .tryb-kroki");
      u.classList.toggle("lista-zwinieta", otw && !LISTA_POKAZANA);
    });
  }

  // ---------------------------------------------------------------- 5. dolny pasek zakładek (telefon)
  function pasekZakladek() {
    let t = document.getElementById("tabbar");
    if (!t) {
      t = document.createElement("nav");
      t.id = "tabbar";
      t.className = "tabbar";
      t.setAttribute("aria-label", "Zakładki");
      document.body.appendChild(t);
      t.addEventListener("click", (e) => {
        const a = e.target.closest("button"); if (!a) return;
        if (a.dataset.menu) { if (typeof przelaczMenu === "function") przelaczMenu(); return; }
        const b = [...document.querySelectorAll(`#nav button[data-w="${a.dataset.w}"]`)].find((x) => getComputedStyle(x).display !== "none");
        if (b) b.click();
      });
    }
    const g1 = document.querySelector("#nav .nav-grupa.g1"); if (!g1) return;
    const wid = [...g1.querySelectorAll(":scope > button[data-w]")].filter((b) => getComputedStyle(b).display !== "none" && !b.classList.contains("nav-cel") && b.dataset.w !== "kalk_pracy").slice(0, 4);
    const sig = JSON.stringify(wid.map((b) => [b.dataset.w, b.classList.contains("akt"), tekst(b)]));
    if (t.dataset.sig === sig) return;
    t.dataset.sig = sig;
    t.innerHTML = wid.map((b) => {
      const ik = b.querySelector("svg"), et = bezNumeru(tekst(b.querySelector(".etykieta") || b));
      return `<button type="button" class="tab" data-w="${esc(b.dataset.w)}"${b.classList.contains("akt") ? ' aria-current="page"' : ""}>${ik ? ik.outerHTML : ""}<span>${esc(et.length > 14 ? et.split(" ")[0] : et)}</span></button>`;
    }).join("") + `<button type="button" class="tab" data-menu="1"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span>Menu</span></button>`;
    document.body.classList.toggle("ma-tabbar", wid.length > 0);
  }

  // ---------------------------------------------------------------- odświeżanie po zmianach w app.js
  let czeka = false;
  function plan() {
    if (czeka) return;
    czeka = true;
    requestAnimationFrame(() => {
      czeka = false;
      try {
        logoWPasku();
        grupyMenu();
        KONTENERY.forEach((s) => document.querySelectorAll(s).forEach((k) => krokiKontenera(k, s)));
        listaProjektow();
        pasekZakladek();
      } catch (e) { if (window.console) console.warn("uklad.js", e); }
    });
  }
  function start() {
    plan();
    new MutationObserver(plan).observe(document.body, { childList: true, subtree: true });
    const nav = document.getElementById("nav");
    if (nav) new MutationObserver(plan).observe(nav, { attributes: true, subtree: true, attributeFilter: ["class", "style"] });
    window.addEventListener("resize", plan);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
