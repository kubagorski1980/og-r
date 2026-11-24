// Ogór – serwer gry sieciowej (Express + Socket.IO)
"use strict";
const express = require('express');
const http = require('http');
const path = require('path');
const { Server } = require('socket.io');
const AI = require('./public/ai.js');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));
const VERSION = '1.4-czat';
app.get('/health', (req, res) => res.send('ok'));
app.get('/version', (req, res) => res.json({ server: VERSION, czat: true }));
const server = http.createServer(app);
const io = new Server(server, { pingInterval: 20000, pingTimeout: 30000 });

/* ================= ZASADY ================= */
const SUITS = ['♣', '♦', '♥', '♠'];
const LIMIT = 21, HAND = 6, MAXP = 8;
const RL = { 11: 'W', 12: 'D', 13: 'K', 14: 'A' };
const is2C = c => c.r === 2 && c.s === '♣';
const cname = c => (RL[c.r] || c.r) + c.s;
const T = { bot: 800, endTrick: 1300, reveal: 2400 };   // opóźnienia (ms)

const rooms = new Map();

function makeDeck() {
  const d = [];
  for (const s of SUITS) for (let r = 2; r <= 14; r++) d.push({ r, s });
  for (let i = d.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [d[i], d[j]] = [d[j], d[i]]; }
  return d;
}
const sortHand = h => h.sort((a, b) => a.r - b.r || SUITS.indexOf(a.s) - SUITS.indexOf(b.s));
function activeFrom(R, start) { const n = R.players.length, res = []; for (let k = 0; k < n; k++) { const i = (start + k) % n; if (!R.players[i].out) res.push(i); } return res; }
function nextActive(R, i) { const n = R.players.length; for (let k = 1; k <= n; k++) { const j = (i + k) % n; if (!R.players[j].out) return j; } return i; }
function tableTop(R) { return R.trick.length ? Math.max(...R.trick.map(t => t.c.r)) : null; }
function highestPlayer(R) { const top = tableTop(R); let hi = null; for (const t of R.trick) if (t.c.r === top) hi = t.p; return hi; }

// Dozwolone: przy wyjściu dowolna; potem >= najwyższej na stole albo najniższa z ręki (2♣, jeśli ją masz)
function legal(R, hand) {
  const top = tableTop(R);
  if (top === null) return hand.slice();
  const hasC2 = hand.some(is2C);
  const minR = Math.min(...hand.map(c => c.r));
  return hand.filter(c => c.r >= top || (hasC2 ? is2C(c) : c.r === minR));
}
function log(R, m) { R.log.unshift(m); if (R.log.length > 30) R.log.pop(); }
function later(R, fn, ms) { const g = R.gen; setTimeout(() => { if (R.gen === g && rooms.get(R.code) === R) fn(); }, ms); }

function startGame(R) {
  R.gen++;
  R.players.forEach(p => { p.points = 0; p.out = false; p.hand = []; });
  R.roundNo = 0; R.log = []; R.winner = null; R.summary = null;
  // Grę zaczyna ten, kto w poprzedniej grze odpadł jako pierwszy
  let st = R.nextStarterId ? idx(R, R.nextStarterId) : -1;
  if (st > 0) log(R, `Grę zaczyna ${R.players[st].name} – odpadł jako pierwszy w poprzedniej grze.`);
  if (st < 0) st = 0;
  R.firstOutId = null;
  startRound(R, st);
}

function startRound(R, starter) {
  R.phase = 'playing'; R.summary = null; R.roundNo++;
  const d = makeDeck(), order = activeFrom(R, starter);
  R.players.forEach(p => p.hand = []);
  for (let pass = 0; pass < HAND / 2; pass++) for (const i of order) R.players[i].hand.push(d.pop(), d.pop()); // po dwie
  order.forEach(i => sortHand(R.players[i].hand));
  R.trickNo = 1; R.played = []; R.cons = {};
  log(R, `— Rozdanie ${R.roundNo}. Zaczyna ${R.players[starter].name}.`);
  startTrick(R, starter);
}

function startTrick(R, leader) {
  R.leader = leader; R.order = activeFrom(R, leader); R.pos = 0; R.trick = []; R.reveal = false;
  if (R.trickNo === HAND) {
    // Ostatnia runda: wszyscy wykładają ostatnią kartę jednocześnie
    R.turn = null; R.reveal = true;
    R.trick = R.order.map(i => ({ p: i, c: R.players[i].hand.pop() }));
    R.pos = R.order.length;
    log(R, 'Ostatnia runda – wszyscy wykładają karty.');
    broadcast(R); later(R, () => endTrick(R), T.reveal); return;
  }
  nextTurn(R);
}

function nextTurn(R) {
  if (R.pos >= R.order.length) { R.turn = null; broadcast(R); later(R, () => endTrick(R), T.endTrick); return; }
  R.turn = R.order[R.pos];
  if (R.players[R.turn].bot) scheduleBot(R);
  broadcast(R);
}

function scheduleBot(R) {
  const i = R.turn;
  later(R, () => {
    if (R.phase !== 'playing' || R.turn !== i || !R.players[i].bot) return;
    const P = R.players[i];
    const S = { hand: P.hand, me: i, trick: R.trick, order: R.order, pos: R.pos, trickNo: R.trickNo,
      players: R.players.map(q => ({ out: q.out, points: q.points, handSize: q.hand.length })),
      played: R.played, cons: R.cons, limit: LIMIT, handN: HAND };
    let c = AI.choose(S, { samples: 400 });
    if (!c || !legal(R, P.hand).includes(c)) c = legal(R, P.hand).sort((a, b) => b.r - a.r)[0];
    play(R, i, c);
  }, T.bot);
}

function play(R, i, c) {
  const h = R.players[i].hand;
  const top = tableTop(R);
  if (top !== null && c.r < top) {   // musiał dać najniższą -> nie ma nic niższego ani 2♣ (wiedza jawna dla wszystkich)
    const k = R.cons[i] || { min: 0, no2C: false };
    R.cons[i] = { min: Math.max(k.min, c.r), no2C: k.no2C || !is2C(c) };
  }
  h.splice(h.indexOf(c), 1);
  R.trick.push({ p: i, c });
  R.played.push(c);
  R.pos++;
  nextTurn(R);
}

function endTrick(R) {
  const top = tableTop(R), hi = highestPlayer(R);
  const c2 = R.trick.find(t => is2C(t.c));
  if (R.trickNo === HAND) { endRound(R, c2); return; }
  const next = c2 ? c2.p : hi;
  log(R, c2 ? `Lewa ${R.trickNo}: ${R.players[next].name} wyrzucił 2♣ – zaczyna.`
            : `Lewa ${R.trickNo}: najwyższa ${RL[top] || top} – zaczyna ${R.players[next].name}.`);
  R.trickNo++;
  startTrick(R, next);
}

function endRound(R, c2) {
  const top = tableTop(R);
  const losers = R.trick.filter(t => t.c.r === top);      // remis = przegrywają wszyscy
  const mult = c2 ? 2 : 1;
  const sum = { round: R.roundNo, losers: [], doubled: !!c2, c2name: c2 ? R.players[c2.p].name : null, outs: [], playoff: false, next: null };
  for (const t of losers) {
    const P = R.players[t.p], pts = t.c.r * mult;
    P.points += pts;
    if (P.points >= LIMIT) { P.out = true; sum.outs.push(P.name); }
    sum.losers.push({ name: P.name, card: t.c, pts });
    log(R, `Rozdanie ${R.roundNo}: przegrywa ${P.name} (${cname(t.c)}) +${pts} pkt${c2 ? ' (x2)' : ''}.`);
  }
  let alive = R.players.filter(p => !p.out);
  if (alive.length === 0) {               // wszyscy pozostali odpadliby naraz -> dogrywka
    sum.playoff = true; sum.outs = [];
    for (const t of losers) R.players[t.p].out = false;
    alive = R.players.filter(p => !p.out);
    log(R, 'Wszyscy pozostali przekroczyli limit naraz – dogrywka!');
  }
  if (sum.outs.length && R.firstOutId == null) {   // pierwszy odpadły (przy kilku: więcej pkt, potem dalej od wychodzącego)
    let f = null;
    for (const t of losers) if (R.players[t.p].out && (f === null || R.players[t.p].points >= R.players[f].points)) f = t.p;
    R.firstOutId = R.nextStarterId = R.players[f].id;
  }
  sum.table = R.players.map((p, i) => ({ name: p.name, points: p.points, out: p.out, lost: losers.some(t => t.p === i) }));
  R.turn = null;
  if (alive.length <= 1) {
    R.phase = 'over'; R.winner = alive[0].name; R.summary = sum;
    const fo = R.players.find(p => p.id === R.firstOutId); sum.nextGame = fo ? fo.name : null;
    log(R, `🏆 Wygrywa ${R.winner}!`);
    broadcast(R); return;
  }
  // Następne rozdanie: przegrany; przy kilku – kto ma więcej pkt, przy równych – dalej od wychodzącego
  const stillIn = losers.filter(t => !R.players[t.p].out);
  let next = null;
  if (stillIn.length) { for (const t of stillIn) if (next === null || R.players[t.p].points >= R.players[next].points) next = t.p; }
  else { let pick = null; for (const t of losers) if (pick === null || R.players[t.p].points >= R.players[pick].points) pick = t.p; next = nextActive(R, pick); }
  R.pendingNext = next; sum.next = R.players[next].name;
  R.phase = 'roundEnd'; R.summary = sum;
  broadcast(R);
}

/* ================= WIDOK DLA GRACZA ================= */
function view(R, i) {
  const p = R.players[i];
  const myTurn = R.phase === 'playing' && R.turn === i && !p.bot;
  const top = tableTop(R), hi = highestPlayer(R);
  return {
    code: R.code, me: p.id, host: R.hostId, phase: R.phase,
    players: R.players.map((q, j) => ({ id: q.id, name: q.name, bot: q.bot, connected: q.bot || q.connected, points: q.points, out: q.out, cards: q.hand.length, turn: j === R.turn })),
    hand: p.hand, myTurn,
    legal: myTurn ? legal(R, p.hand).map(c => p.hand.indexOf(c)) : [],
    trick: (R.trick || []).map(t => ({ name: R.players[t.p].name, c: t.c, top: R.reveal ? t.c.r === top : t.p === hi })),
    top, trickNo: R.trickNo, roundNo: R.roundNo, reveal: R.reveal,
    leader: R.leader != null && R.players[R.leader] ? R.players[R.leader].name : null,
    turnName: R.turn != null ? R.players[R.turn].name : null,
    log: R.log.slice(0, 12), summary: R.summary, winner: R.winner, limit: LIMIT
  };
}
function broadcast(R) {
  R.active = Date.now();
  R.players.forEach((p, i) => { if (!p.bot && p.connected && p.sid) io.to(p.sid).emit('state', view(R, i)); });
}

/* ================= POKOJE ================= */
const idx = (R, id) => R.players.findIndex(p => p.id === id);
const cleanName = n => String(n || '').trim().slice(0, 16);
function newCode() {
  const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
  let c; do { c = Array.from({ length: 4 }, () => A[Math.floor(Math.random() * A.length)]).join(''); } while (rooms.has(c));
  return c;
}
function fixHost(R) {
  const h = R.players.find(p => p.id === R.hostId);
  if (h && h.connected && !h.bot) return;
  const nh = R.players.find(p => !p.bot && p.connected);
  if (nh) R.hostId = nh.id;
}

io.on('connection', socket => {
  socket.emit('hello', { version: VERSION });
  const ctx = () => { const R = rooms.get(socket.data.code); if (!R) return {}; const i = idx(R, socket.data.id); return i < 0 ? {} : { R, i, P: R.players[i] }; };
  const err = m => socket.emit('err', m);

  socket.on('create', ({ name, token } = {}) => {
    name = cleanName(name); if (!name) return err('Podaj swoje imię.');
    if (!token) return err('Brak identyfikatora gracza.');
    const code = newCode();
    const R = { code, players: [], hostId: token, phase: 'lobby', log: [], gen: 0, trick: [], chat: [], active: Date.now() };
    R.players.push({ id: token, name, bot: false, connected: true, sid: socket.id, points: 0, out: false, hand: [] });
    rooms.set(code, R);
    socket.data = { code, id: token };
    socket.emit('chatHistory', R.chat);
    broadcast(R);
  });

  socket.on('join', ({ code, name, token } = {}) => {
    const R = rooms.get(String(code || '').toUpperCase().trim());
    if (!R) return socket.emit('noroom', 'Nie ma takiego pokoju (mógł wygasnąć).');
    if (!token) return err('Brak identyfikatora gracza.');
    const i = idx(R, token);
    if (i >= 0) {                     // powrót do swojego miejsca
      const P = R.players[i];
      P.connected = true; P.sid = socket.id; P.bot = false;
      if (cleanName(name) && R.phase === 'lobby') P.name = cleanName(name);
    } else {
      name = cleanName(name); if (!name) return err('Podaj swoje imię.');
      if (R.phase !== 'lobby') return err('Gra w tym pokoju już trwa.');
      if (R.players.length >= MAXP) return err('Pokój jest pełny (max 8 graczy).');
      if (R.players.some(p => p.name.toLowerCase() === name.toLowerCase())) name = name.slice(0, 13) + ' ' + (R.players.length + 1);
      R.players.push({ id: token, name, bot: false, connected: true, sid: socket.id, points: 0, out: false, hand: [] });
    }
    socket.data = { code: R.code, id: token };
    socket.emit('chatHistory', R.chat);
    fixHost(R); broadcast(R);
  });

  socket.on('addBot', () => {
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase !== 'lobby') return;
    if (R.players.length >= MAXP) return err('Maksymalnie 8 graczy.');
    let n = 1; while (R.players.some(p => p.name === 'Komputer ' + n)) n++;
    R.players.push({ id: 'bot-' + Math.random().toString(36).slice(2), name: 'Komputer ' + n, bot: true, connected: true, points: 0, out: false, hand: [] });
    broadcast(R);
  });

  socket.on('remove', ({ id } = {}) => {
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase !== 'lobby' || id === P.id) return;
    const j = idx(R, id); if (j < 0) return;
    const [gone] = R.players.splice(j, 1);
    if (gone.sid) io.to(gone.sid).emit('kicked', 'Gospodarz usunął Cię z pokoju.');
    broadcast(R);
  });

  socket.on('start', () => {
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase !== 'lobby') return;
    if (R.players.length < 2) return err('Potrzeba co najmniej 2 graczy (możesz dodać komputer).');
    startGame(R);
  });

  socket.on('play', ({ k } = {}) => {
    const { R, i, P } = ctx(); if (!R || R.phase !== 'playing' || R.turn !== i || P.bot) return;
    const c = P.hand[k]; if (!c) return;
    if (!legal(R, P.hand).includes(c)) return err('Tej karty nie możesz teraz zagrać.');
    play(R, i, c);
  });

  socket.on('next', () => {
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase !== 'roundEnd') return;
    startRound(R, R.pendingNext);
  });

  socket.on('again', () => {
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase !== 'over') return;
    R.phase = 'lobby'; R.gen++; R.players = R.players.filter(p => p.bot || p.connected);
    R.players.forEach(p => { p.points = 0; p.out = false; p.hand = []; });
    R.trick = []; R.summary = null; R.winner = null; R.log = [];
    broadcast(R);
  });

  socket.on('toBot', ({ id } = {}) => {        // gospodarz zastępuje rozłączonego gracza komputerem
    const { R, P } = ctx(); if (!R || R.hostId !== P.id || R.phase === 'lobby') return;
    const j = idx(R, id); if (j < 0) return;
    const Q = R.players[j]; if (Q.bot || Q.connected) return;
    Q.bot = true; Q.name = Q.name.replace(/ \(komp\.\)$/, '') + ' (komp.)';
    if (R.phase === 'playing' && R.turn === j) scheduleBot(R);
    broadcast(R);
  });

  socket.on('chat', ({ text } = {}) => {
    const { R, P } = ctx(); if (!R) return;
    text = String(text || '').replace(/\s+/g, ' ').trim().slice(0, 200); if (!text) return;
    const now = Date.now(); if (P.lastChat && now - P.lastChat < 400) return; P.lastChat = now;
    const msg = { id: P.id, name: P.name, text, t: now };
    R.chat.push(msg); if (R.chat.length > 60) R.chat.shift();
    R.players.forEach(q => { if (!q.bot && q.connected && q.sid) io.to(q.sid).emit('chat', msg); });
  });

  socket.on('leave', () => { drop(socket, true); socket.data = {}; });
  socket.on('disconnect', () => drop(socket, false));

  function drop(sock, intentional) {
    const R = rooms.get(sock.data && sock.data.code); if (!R) return;
    const i = idx(R, sock.data.id); if (i < 0) return;
    const P = R.players[i]; if (P.sid !== sock.id) return;
    if (R.phase === 'lobby') R.players.splice(i, 1);
    else { P.connected = false; P.sid = null; if (intentional) { P.bot = true; P.name += ' (komp.)'; if (R.phase === 'playing' && R.turn === i) scheduleBot(R); } }
    if (!R.players.some(p => !p.bot && p.connected) && R.phase === 'lobby' && !R.players.some(p => !p.bot)) { rooms.delete(R.code); return; }
    fixHost(R); broadcast(R);
  }
});

// Sprzątanie: usuń pokoje bez nikogo połączonego od 30 min
setInterval(() => {
  const now = Date.now();
  for (const [code, R] of rooms) if (!R.players.some(p => !p.bot && p.connected) && now - R.active > 30 * 60 * 1000) rooms.delete(code);
}, 5 * 60 * 1000);

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log('Ogór działa na porcie ' + PORT));
module.exports = { server, rooms, T };
