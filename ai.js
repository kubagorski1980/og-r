/* Ogór – sztuczna inteligencja gracza komputerowego.
   Nie podgląda cudzych kart. Zna tylko: swoją rękę, karty już zagrane w tym rozdaniu,
   liczbę kart u rywali i to, co da się wywnioskować z ich ruchów (np. kto musiał dać
   najniższą kartę, ten nie ma nic niższego i nie ma 2♣).
   Dla każdego dozwolonego ruchu losuje kilkaset możliwych rozkładów kart rywali,
   rozgrywa resztę rozdania i wybiera ruch z najmniejszą oczekiwaną stratą
   (punkty karne, ryzyko odpadnięcia, punkty dla rywali). */
(function (root) {
  "use strict";
  const SUITS = ['♣', '♦', '♥', '♠'];
  const is2C = c => c.r === 2 && c.s === '♣';
  const key = c => c.r + c.s;

  function legalOf(hand, trick) {
    if (!trick.length) return hand.slice();
    if (is2C(trick[0].c)) {                       // lewę otworzyła 2♣ -> trzeba dać najwyższą kartę
      let mx = 0; for (const c of hand) if (c.r > mx) mx = c.r;
      return hand.filter(c => c.r === mx);
    }
    let top = 0; for (const t of trick) if (t.c.r > top) top = t.c.r;
    const has = hand.some(is2C);
    let m = 99; for (const c of hand) if (c.r < m) m = c.r;
    return hand.filter(c => c.r >= top || (has ? is2C(c) : c.r === m));
  }

  function activeFrom(players, start) {
    const n = players.length, res = [];
    for (let k = 0; k < n; k++) { const i = (start + k) % n; if (!players[i].out) res.push(i); }
    return res;
  }

  // Model ruchów rywali w symulacji: zwykle zrzucają najwyższą dozwoloną kartę,
  // czasem zagrywają inaczej (żeby nie zakładać, że rywal jest przewidywalny).
  function rolloutPick(hand, trick, rnd) {
    const lg = legalOf(hand, trick);
    if (lg.length === 1) return lg[0];
    const x = rnd();
    if (x < 0.15) return lg[Math.floor(rnd() * lg.length)];
    // trzymaj 2♣ do końca, jeśli się da
    const pool = lg.length > 1 ? lg.filter(c => !is2C(c)) : lg;
    let b = pool[0]; for (const c of pool) if (c.r > b.r) b = c;
    if (x < 0.3 && trick.length) {           // czasem: najniższa karta, która jeszcze bije
      let top = 0; for (const t of trick) if (t.c.r > top) top = t.c.r;
      const beat = pool.filter(c => c.r >= top);
      if (beat.length) { b = beat[0]; for (const c of beat) if (c.r < b.r) b = c; }
    }
    return b;
  }

  function simulate(S, H, me, move, rnd) {
    let trick = S.trick.slice(), pos = S.pos, order = S.order, trickNo = S.trickNo;
    const take = (p, c) => { const h = H[p]; h.splice(h.indexOf(c), 1); trick.push({ p, c }); pos++; };
    take(me, move);
    for (let guard = 0; guard < 200; guard++) {
      if (pos >= order.length) {
        let top = 0, hi = null;
        for (const t of trick) if (t.c.r >= top) { top = t.c.r; hi = t.p; }
        const c2 = trick.find(t => is2C(t.c));
        const lead = c2 ? c2.p : hi;
        trickNo++; trick = []; pos = 0; order = activeFrom(S.players, lead);
        if (trickNo >= S.handN) {                    // ostatnia runda: wykładamy
          const fin = order.map(p => ({ p, c: H[p][0] }));
          let t2 = 0; for (const t of fin) if (t.c.r > t2) t2 = t.c.r;
          const mult = fin.some(t => is2C(t.c)) ? 2 : 1;
          const res = {}; for (const t of fin) if (t.c.r === t2) res[t.p] = t.c.r * mult;
          return res;
        }
        continue;
      }
      const p = order[pos];
      take(p, rolloutPick(H[p], trick, rnd));
    }
    return {};
  }

  function fullDeck() { const d = []; for (const s of SUITS) for (let r = 2; r <= 14; r++) d.push({ r, s }); return d; }

  function sampleHands(S, me, rnd) {
    const known = new Set(S.hand.map(key).concat(S.played.map(key)));
    const pool0 = fullDeck().filter(c => !known.has(key(c)));
    const opp = activeFrom(S.players, 0).filter(p => p !== me && S.players[p].handSize > 0);
    const ok = (p, c) => { const k = S.cons[p]; return !k || (c.r >= (k.min || 0) && c.r <= (k.max || 14) && !(k.no2C && is2C(c))); };
    // najpierw gracze z najciaśniejszymi ograniczeniami
    opp.sort((a, b) => ((S.cons[b] || {}).min || 0) - ((S.cons[a] || {}).min || 0));
    for (let attempt = 0; attempt < 6; attempt++) {
      const pool = pool0.slice();
      for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
      const H = {}; let fail = false;
      for (const p of opp) {
        const need = S.players[p].handSize, h = [];
        for (let i = 0; i < pool.length && h.length < need; i++) {
          if (attempt < 5 && !ok(p, pool[i])) continue;
          h.push(pool[i]); pool.splice(i, 1); i--;
        }
        if (h.length < need) { fail = true; break; }
        H[p] = h;
      }
      if (!fail) return H;
    }
    return null;
  }

  function choose(S, opts) {
    opts = opts || {};
    const rnd = opts.rnd || Math.random;
    const me = S.me;
    const legal = legalOf(S.hand, S.trick);
    if (legal.length === 1) return legal[0];
    // ruchy o tej samej wartości są równoważne (poza 2♣) – licz tylko po jednym
    const cand = []; const seen = new Set();
    for (const c of legal) { const k = is2C(c) ? 'c2' : String(c.r); if (!seen.has(k)) { seen.add(k); cand.push(c); } }
    if (cand.length === 1) return cand[0];
    const N = opts.samples || 400;
    const cost = new Array(cand.length).fill(0);
    const myPts = S.players[me].points;
    // im bliżej końca gry rywale, tym cenniejsze ich punkty
    const oppW = p => 0.15 + 0.35 * Math.min(1, S.players[p].points / S.limit);
    let n = 0;
    for (let s = 0; s < N; s++) {
      const base = sampleHands(S, me, rnd); if (!base) continue;
      n++;
      for (let m = 0; m < cand.length; m++) {
        const H = {}; for (const p in base) H[p] = base[p].slice();
        H[me] = S.hand.slice();
        const res = simulate(S, H, me, cand[m], rnd);
        let cst = 0;
        for (const p in res) {
          const pts = res[p];
          if (+p === me) { cst += pts; if (myPts + pts >= S.limit) cst += 40; }
          else cst -= pts * oppW(+p);
        }
        cost[m] += cst;
      }
    }
    if (!n) { let b = legal[0]; for (const c of legal) if (c.r > b.r) b = c; return b; }
    let best = 0;
    for (let m = 1; m < cand.length; m++) if (cost[m] < cost[best] - 1e-9 || (Math.abs(cost[m] - cost[best]) < 1e-9 && cand[m].r > cand[best].r)) best = m;
    return cand[best];
  }

  const api = { choose, legalOf };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.OgorAI = api;
})(typeof self !== 'undefined' ? self : this);
