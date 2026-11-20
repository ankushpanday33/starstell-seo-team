#!/usr/bin/env node
// StarsTell agent office.
//
// Starts The Roving Office (git submodule in ./roving-office, Apache-2.0) with the
// StarsTell patch (departments, coordination visits, a wider room) and the StarsTell
// layout, then feeds it a simulated SEO pipeline over the Agent Office Protocol: the
// same events a real Claude Code agent sends.
//
// Every agent sits at a desk in its own department all day. They only get up to
// coordinate with someone in another department, to fetch knowledge from the StarsTell
// bots bookshelf, or to send finished work out through the printer.
//
//   node visualizer/starstell-office.mjs              start the office and the feed
//   node visualizer/starstell-office.mjs --feed-only  feed an office that is already running
//   SPEED=2 node visualizer/starstell-office.mjs      run twice as fast

import { spawn, execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const KEYCARD = 'STAR-7EAM';
const PORT = Number(process.env.PORT) || 8090;
const SPEED = Math.max(0.25, Number(process.env.SPEED) || 1);
const FEED_ONLY = process.argv.includes('--feed-only');
const HERE = dirname(fileURLToPath(import.meta.url));
const OFFICE_DIR = join(HERE, 'roving-office');
const PATCH = join(HERE, 'patches', 'starstell-departments.patch');
const LAYOUT = JSON.parse(readFileSync(join(HERE, 'starstell-layout.json'), 'utf8'));
const ENDPOINT_FILE = join(homedir(), '.roving-office', 'endpoint.json');
const BASE = `http://127.0.0.1:${PORT}/office/${KEYCARD}`;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms / SPEED));
const jitter = (ms) => ms * (0.8 + Math.random() * 0.4);

// ---------------------------------------------------------------- the team, by department
const TEAM = {
  head:       { actor: 'SEO Head',            department: 'hq',        color: '#E0BF71' },
  keyword:    { actor: 'Keyword Research',    department: 'research',  color: '#5B6C8F' },
  competitor: { actor: 'Competitor Intel',    department: 'research',  color: '#5B6C8F' },
  intent:     { actor: 'Search Intent',       department: 'research',  color: '#5B6C8F' },
  brief:      { actor: 'Content Brief',       department: 'research',  color: '#5B6C8F' },
  vedic:      { actor: 'Vedic Research',      department: 'knowledge', color: '#7A5A9A' },
  tarot:      { actor: 'Tarot Research',      department: 'knowledge', color: '#7A5A9A' },
  numerology: { actor: 'Numerology Research', department: 'knowledge', color: '#7A5A9A' },
  writer:     { actor: 'Senior Writer',       department: 'writing',   color: '#A45B3E' },
  fact:       { actor: 'Fact Checker',        department: 'writing',   color: '#A45B3E' },
  seo:        { actor: 'SEO Optimizer',       department: 'writing',   color: '#A45B3E' },
  editor:     { actor: 'Senior Editor',       department: 'writing',   color: '#421206' },
  hi:         { actor: 'Hindi Writer',        department: 'languages', color: '#C77A3A' },
  hinglish:   { actor: 'Hinglish Writer',     department: 'languages', color: '#C77A3A' },
  mr:         { actor: 'Marathi Writer',      department: 'languages', color: '#C77A3A' },
  ta:         { actor: 'Tamil Writer',        department: 'languages', color: '#C77A3A' },
  te:         { actor: 'Telugu Writer',       department: 'languages', color: '#C77A3A' },
  bn:         { actor: 'Bengali Writer',      department: 'languages', color: '#C77A3A' },
  visual:     { actor: 'Visual Designer',     department: 'publish',   color: '#3F7F6E' },
  cms:        { actor: 'CMS Publisher',       department: 'publish',   color: '#2F6F8F' },
  analyst:    { actor: 'SEO Analyst',         department: 'publish',   color: '#4D7A3A' },
};
for (const [key, a] of Object.entries(TEAM)) a.id = `st-${key}`;
const LANG_KEYS = ['hi', 'hinglish', 'mr', 'ta', 'te', 'bn'];
const BOT = { vedic: 'StarsTell.vedic_ask', tarot: 'StarsTell.tarot_ask', numerology: 'StarsTell.numerology_ask' };

// Example blogs. Titles only; the content is produced in the real pipeline.
const BLOGS = [
  { key: 'ST-142', title: 'Sade Sati remedies', vertical: 'vedic', fail: true },
  { key: 'ST-143', title: 'Tower card in love readings', vertical: 'tarot', fail: false },
  { key: 'ST-144', title: 'Life path number 7', vertical: 'numerology', fail: true },
  { key: 'ST-145', title: 'Mangal Dosha explained', vertical: 'vedic', fail: false },
  { key: 'ST-146', title: 'Three of Cups meaning', vertical: 'tarot', fail: false },
  { key: 'ST-147', title: 'Name numerology for business', vertical: 'numerology', fail: false },
];

// ---------------------------------------------------------------- transport
let ingestUrl = `${BASE}/aop/v0/events`;
let token = null;
const seqs = new Map();
let callNo = 0;

function envelope(type, a, payload = {}, blog = null) {
  const id = a.queue ? 'queue' : a.id;
  const seq = (seqs.get(id) || 0) + 1;
  seqs.set(id, seq);
  return {
    aop: '0.2',
    id: `${id}:${seq}:${Date.now()}`,
    ts: new Date().toISOString(),
    seq,
    type,
    harness: { name: 'claude-code', variant: 'sdk' },
    session: a.queue ? { id: 'queue' } : { id: a.id, kind: 'main', actor: a.actor, actor_color: a.color, cwd: '~/starstell-seo-team' },
    project: {
      id: 'starstell-seo-team',
      name: 'StarsTell SEO Team',
      ...(blog ? { workitem: { key: blog.key, title: blog.title } } : {}),
    },
    ...(a.department ? { ext: { department: a.department } } : {}),
    payload,
  };
}

async function send(...events) {
  try {
    const res = await fetch(ingestUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-ndjson', 'X-Roving-Office-Token': token },
      body: events.map((e) => JSON.stringify(e)).join('\n'),
    });
    if (!res.ok) console.warn(`[feed] ${res.status} ${await res.text()}`);
  } catch (err) {
    console.warn(`[feed] send failed: ${err.message}`);
  }
}

// ---------------------------------------------------------------- standby at your own desk
// Between tasks an agent keeps an open "queue" turn with one open read, so it stays
// seated at its department desk instead of wandering off for coffee.
const standbyOf = new Map();
const DESK_WORK = {
  hq: 'Reviewing the Paperclip board', research: 'Watching rankings in OpenSEO',
  knowledge: 'Reading the bot logs', writing: 'Reading the style guide',
  languages: 'Updating the language glossary', publish: 'Checking the CMS queue',
};
async function standby(a) {
  if (standbyOf.has(a.id)) return;
  const s = { turn: `standby-${++callNo}`, call: `standby-call-${callNo}` };
  standbyOf.set(a.id, s);
  const idle = { key: 'DESK', title: DESK_WORK[a.department] };
  await send(
    envelope('turn.start', a, { turn_id: s.turn, title: idle.title, trigger: 'user' }, idle),
    envelope('tool.start', a, { tool_call_id: s.call, tool_name: 'Read', tool_class: 'read', target: 'paperclip/queue' }, idle),
  );
}
async function unstandby(a) {
  const s = standbyOf.get(a.id);
  if (!s) return;
  standbyOf.delete(a.id);
  await send(
    envelope('tool.end', a, { tool_call_id: s.call, status: 'ok' }),
    envelope('turn.end', a, { turn_id: s.turn, status: 'completed' }),
  );
}

// ---------------------------------------------------------------- work at your own desk
// tools: [name, class, target, ms, status]. A ['Coordinate', otherAgent, note] entry
// walks to that colleague's desk in another department and back.
async function work(a, blog, title, tools, opts = {}) {
  await unstandby(a);
  try { return await doWork(a, blog, title, tools, opts); } finally { await standby(a); }
}

async function doWork(a, blog, title, tools, opts = {}) {
  const turnId = `turn-${++callNo}`;
  if (opts.claim) await send(envelope('job.claimed', a, { job_id: blog.key, claimed_by: a.id }, blog));
  await send(envelope('turn.start', a, {
    turn_id: turnId, title: `${blog.key} · ${title}`, trigger: 'user',
  }, blog));
  let failed = false;
  for (const t of tools) {
    const id = `call-${++callNo}`;
    if (t[0] === 'Coordinate') {
      const [, other, note] = t;
      console.log(`[feed] ${a.actor} walks to ${other.actor}: ${note}`);
      await send(envelope('tool.start', a, { tool_call_id: id, tool_name: 'Coordinate', tool_class: 'other', target: other.id, summary: `${note} (with ${other.actor})` }, blog));
      await sleep(11000);
      await send(envelope('tool.end', a, { tool_call_id: id, status: 'ok' }, blog));
      await sleep(800);
      continue;
    }
    const [name, cls, target, ms, status = 'ok'] = t;
    await send(envelope('tool.start', a, { tool_call_id: id, tool_name: name, tool_class: cls, ...(target ? { target } : {}) }, blog));
    const d = jitter(ms);
    await sleep(d);
    await send(envelope('tool.end', a, { tool_call_id: id, status, duration_ms: Math.round(d) }, blog));
    if (status !== 'ok') failed = true;
    await sleep(500);
  }
  if (opts.approval) {
    const req = `approval-${blog.key}`;
    await send(envelope('permission.request', a, {
      request_id: req, tool_name: 'ContentService.cms_publish', tool_class: 'scm', reason: 'Waiting for human approval in Paperclip',
    }, blog));
    await sleep(opts.approval);
    await send(envelope('permission.resolve', a, { request_id: req, decision: 'allow', by: 'StarsTell reviewer' }, blog));
  }
  await send(envelope('turn.end', a, { turn_id: turnId, status: failed ? 'error' : 'completed', tool_calls: tools.length }, blog));
  return !failed;
}

// ---------------------------------------------------------------- one blog, end to end
const f = (blog, name) => `content/${blog.key}/${name}`;
const T = TEAM;

async function pipeline(blog) {
  console.log(`[feed] ${blog.key} ${blog.title}: Paperclip routine created the task`);

  await work(T.head, blog, 'Plan and assign', [
    ['Paperclip.create_task', 'edit', `paperclip/${blog.key}`, 2500],
    ['Coordinate', T.keyword, `New task ${blog.key}: ${blog.title}`],
  ]);

  // SEO Research: everyone stays seated; OpenSEO answers on their screens.
  await work(T.keyword, blog, 'Keyword research (OpenSEO)', [
    ['OpenSEO.get_suggested_keywords', 'read', 'openseo', 4500],
    ['OpenSEO.get_keyword_difficulty', 'read', 'openseo', 3500],
    ['ContentService.save_keywords', 'edit', f(blog, 'keywords.json'), 2500],
  ]);
  await Promise.all([
    work(T.competitor, blog, 'Top 10 study (OpenSEO)', [
      ['OpenSEO.get_serp_results', 'read', 'openseo', 4500],
      ['ContentService.save_gap_note', 'edit', f(blog, 'gap-note.md'), 3500],
    ]),
    work(T.intent, blog, 'Search intent (OpenSEO)', [
      ['OpenSEO.get_serp_results', 'read', 'openseo', 4000],
      ['ContentService.save_intent', 'edit', f(blog, 'intent.md'), 3000],
    ]),
  ]);
  await work(T.brief, blog, 'Write the brief', [
    ['ContentService.get_gap_note', 'read', f(blog, 'gap-note.md'), 2500],
    ['ContentService.save_brief', 'edit', f(blog, 'brief.md'), 4000],
    ['Coordinate', T[blog.vertical], 'Brief ready, need the bot answers'],
  ]);

  // Knowledge: fetch from the StarsTell bots shelf, then hand over to Writing.
  await work(T[blog.vertical], blog, `Ask the ${blog.vertical} bot`, [
    [BOT[blog.vertical], 'knowledge', `${blog.vertical}-bot`, 5000],
    ['ContentService.log_bot_call', 'edit', f(blog, 'bot-calls.json'), 2500],
    ['Coordinate', T.writer, 'Bot answers logged for the draft'],
  ]);

  // Writing Room.
  await work(T.writer, blog, 'English draft', [
    ['ContentService.get_brief', 'read', f(blog, 'brief.md'), 2500],
    ['Write', 'edit', f(blog, 'draft-en.md'), 8000],
    ['Skill.humanizer', 'other', 'humanizer', 3000],
  ]);
  const passed = await work(T.fact, blog, 'Fact check every claim', [
    ['ContentService.get_bot_calls', 'read', f(blog, 'bot-calls.json'), 3000],
    ['ContentService.check_claims', 'execute', f(blog, 'claims.json'), 4000, blog.fail ? 'error' : 'ok'],
  ]);
  if (!passed) {
    console.log(`[feed] ${blog.key}: fact check failed, the writer checks with Knowledge`);
    await work(T.writer, blog, 'Fix the flagged claim', [
      ['Coordinate', T[blog.vertical], 'One claim is overstated, what does the bot say?'],
      ['Edit', 'edit', f(blog, 'draft-en.md'), 4500],
    ]);
    await work(T.fact, blog, 'Re-check claims', [['ContentService.check_claims', 'execute', f(blog, 'claims.json'), 3500]]);
  }
  await work(T.fact, blog, 'Hand over to Language Desk', [
    ['Coordinate', T.hi, 'Claims verified, start the 6 languages'],
  ]);

  // Language Desk and the designer, at the same time, each at their own desk.
  await Promise.all([
    ...LANG_KEYS.map(async (k, i) => {
      await sleep(i * 900);
      return work(T[k], blog, `${T[k].actor.replace(' Writer', '')} version`, [
        ['ContentService.get_claims', 'read', f(blog, 'claims.json'), 2500],
        ['Write', 'edit', f(blog, `draft-${k}.md`), 7000],
        ['Skill.humanizer', 'other', 'humanizer', 2500],
      ]);
    }),
    work(T.visual, blog, '3 to 5 images', [
      ['ImageModel.generate', 'execute', 'image-model', 5000],
      ['ContentService.render_diagram', 'execute', 'svg-templates', 3000],
      ['ContentService.save_images', 'edit', f(blog, 'images/'), 2500],
    ]),
  ]);

  await work(T.seo, blog, 'SEO pass, 7 versions', [
    ['Coordinate', T.visual, 'Need alt text in 7 languages'],
    ['Skill.seo-schema', 'other', 'claude-seo', 3000],
    ['Skill.seo-hreflang', 'other', 'claude-seo', 3000],
    ['ContentService.run_checks', 'execute', f(blog, 'checks.json'), 2500],
  ]);

  // Score gate: Seryvon scores the preview page; SEO, GEO and AEO must each be 90+.
  const gated = await work(T.seo, blog, 'Score gate (Seryvon): SEO, GEO, AEO 90+', [
    ['Seryvon.audit', 'execute', 'preview/' + blog.key, 5000, blog.fail ? 'error' : 'ok'],
  ]);
  if (!gated) {
    console.log(`[feed] ${blog.key}: score below 90, back to the writer`);
    await work(T.seo, blog, 'Scores below 90: send fixes', [
      ['Coordinate', T.writer, 'AEO below 90: needs a direct answer and a comparison table'],
    ]);
    await work(T.writer, blog, 'Fix for the score gate', [['Edit', 'edit', f(blog, 'draft-en.md'), 4500]]);
    await work(T.seo, blog, 'Score gate re-run', [['Seryvon.audit', 'execute', 'preview/' + blog.key, 5000]]);
  }

  await work(T.editor, blog, 'Final edit, then human approval', [
    ['Read', 'read', f(blog, 'draft-en.md'), 3500],
    ['seomachine.scrub', 'execute', f(blog, 'draft-en.md'), 2000],
    ['Coordinate', T.head, 'Ready for human approval'],
  ], { approval: 10000 });

  await work(T.head, blog, 'Approved, send to publishing', [
    ['Coordinate', T.cms, `${blog.key} approved, publish 7 links`],
  ]);
  await work(T.cms, blog, 'Publish 7 links', [
    ['ContentService.cms_publish', 'scm', 'starstell.com', 4000],
    ['IndexNow.ping', 'read', 'indexnow', 2000],
  ]);
  console.log(`[feed] ${blog.key} ${blog.title}: published in 7 languages`);

  await sleep(6000);
  await work(T.analyst, blog, 'Results from Search Console', [
    ['OpenSEO.gsc_query', 'read', 'openseo', 4000],
    ['Coordinate', T.head, 'First results are in'],
  ]);
}

// ---------------------------------------------------------------- start up
function applyPatch() {
  const git = (...args) => execFileSync('git', ['-C', OFFICE_DIR, ...args], { stdio: 'pipe' });
  try { git('apply', '--reverse', '--check', PATCH); return; } catch { /* not applied yet */ }
  git('apply', '--whitespace=nowarn', PATCH);
  console.log('[office] StarsTell patch applied (departments, visits, wider room)');
}

async function waitForEndpoint(pid) {
  for (let i = 0; i < 60; i++) {
    if (existsSync(ENDPOINT_FILE)) {
      try {
        const ep = JSON.parse(readFileSync(ENDPOINT_FILE, 'utf8'));
        if (ep.keycard === KEYCARD && ep.token && (!pid || ep.pid === pid)) return ep;
      } catch { /* half-written, try again */ }
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  throw new Error(`no endpoint for ${KEYCARD} in ${ENDPOINT_FILE}`);
}

async function setUpScenes() {
  const office = await (await fetch(`${BASE}/api`)).json();
  for (const scene of office.scenes || []) {
    const res = await fetch(`${BASE}/api/scenes/${encodeURIComponent(scene.id)}`, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sources: ['claude-code'], layout: LAYOUT }),
    });
    if (!res.ok) console.warn(`[office] could not set up scene ${scene.id}: ${res.status}`);
  }
}

async function main() {
  let server = null;
  if (!FEED_ONLY) {
    if (!existsSync(join(OFFICE_DIR, 'server.cjs'))) {
      console.error('The office is missing. Run: git submodule update --init');
      process.exit(1);
    }
    applyPatch();
    server = spawn(process.execPath, ['server.cjs', String(PORT), '--publish', '--office', KEYCARD], { cwd: OFFICE_DIR, stdio: ['ignore', 'inherit', 'inherit'] });
    server.on('exit', (code) => { console.log(`[office] stopped (${code})`); process.exit(code ?? 0); });
  }
  const ep = await waitForEndpoint(server?.pid);
  token = ep.token;
  if (ep.url) ingestUrl = ep.url;
  await setUpScenes();

  console.log(`\n  StarsTell agent office: ${BASE}\n  Ctrl+C to stop.\n`);

  // Everyone arrives for the day and takes a desk in their own department.
  const everyone = Object.values(TEAM);
  for (const a of everyone) {
    await send(envelope('session.start', a, { source: 'startup', capabilities: ['tool.start', 'tool.end', 'permission.request'] }));
    await sleep(1200);
  }
  await sleep(6000);
  for (const a of everyone) await standby(a);
  setInterval(() => { for (const a of everyone) send(envelope('session.heartbeat', a, { status: 'working' })); }, 15000);

  const shutdown = async () => {
    for (const a of everyone) await send(envelope('session.end', a, { reason: 'exit' }));
    server?.kill();
    process.exit(0);
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);

  await sleep(8000);
  for (let i = 0; ; i++) {
    const blog = { ...BLOGS[i % BLOGS.length] };
    if (i >= BLOGS.length) blog.key = `ST-${142 + i}`;
    // One blog at a time, so nobody is asked to be at two desks at once.
    await pipeline(blog).catch((e) => console.warn(`[feed] ${blog.key}: ${e.message}`));
    await sleep(15000);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
