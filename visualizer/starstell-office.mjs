#!/usr/bin/env node
// StarsTell agent office.
//
// Starts The Roving Office (git submodule in ./roving-office, Apache-2.0) on this machine
// and feeds it a simulated StarsTell SEO pipeline over the Agent Office Protocol, the same
// events a real Claude Code agent sends. Every agent walks in, works, and clocks off.
//
//   node visualizer/starstell-office.mjs              start the office and the feed
//   node visualizer/starstell-office.mjs --feed-only  feed an office that is already running
//   SPEED=2 node visualizer/starstell-office.mjs      run twice as fast
//
// Where things are in the room:
//   mailbox and paper planes  = Paperclip assigning a task
//   globe                     = OpenSEO and the web (data from outside the building)
//   bookshelf                 = your StarsTell bots (knowledge the company owns)
//   desks                     = writing and editing through the Content Service
//   "waiting on you" status   = human approval in Paperclip
//   outbox / printer          = publishing to the StarsTell CMS
//   bin                       = a draft that failed a check

import { spawn } from 'node:child_process';
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
const ENDPOINT_FILE = join(homedir(), '.roving-office', 'endpoint.json');
const BASE = `http://127.0.0.1:${PORT}/office/${KEYCARD}`;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms / SPEED));
const jitter = (ms) => ms * (0.8 + Math.random() * 0.4);

// ---------------------------------------------------------------- the team
const TEAM = {
  head:      { actor: 'SEO Head',           color: '#E0BF71' },
  keyword:   { actor: 'Keyword Research',   color: '#5B6C8F' },
  competitor:{ actor: 'Competitor Intel',   color: '#5B6C8F' },
  brief:     { actor: 'Content Brief',      color: '#5B6C8F' },
  vedic:     { actor: 'Vedic Research',     color: '#7A5A9A' },
  tarot:     { actor: 'Tarot Research',     color: '#7A5A9A' },
  numerology:{ actor: 'Numerology Research',color: '#7A5A9A' },
  writer:    { actor: 'Senior Writer',      color: '#A45B3E' },
  fact:      { actor: 'Fact Checker',       color: '#A45B3E' },
  seo:       { actor: 'SEO Optimizer',      color: '#A45B3E' },
  editor:    { actor: 'Senior Editor',      color: '#421206' },
  visual:    { actor: 'Visual Designer',    color: '#3F7F6E' },
  cms:       { actor: 'CMS Publisher',      color: '#2F6F8F' },
  analyst:   { actor: 'SEO Analyst',        color: '#4D7A3A' },
};
const LANGS = [
  { code: 'hi', actor: 'Hindi Writer' }, { code: 'hi-latn', actor: 'Hinglish Writer' },
  { code: 'mr', actor: 'Marathi Writer' }, { code: 'ta', actor: 'Tamil Writer' },
  { code: 'te', actor: 'Telugu Writer' }, { code: 'bn', actor: 'Bengali Writer' },
];
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
const live = new Map();   // session id -> session object, for heartbeats and shutdown

function envelope(type, s, payload = {}) {
  const seq = (seqs.get(s.id) || 0) + 1;
  seqs.set(s.id, seq);
  return {
    aop: '0.2',
    id: `${s.id}:${seq}`,
    ts: new Date().toISOString(),
    seq,
    type,
    harness: { name: 'claude-code', variant: 'sdk' },
    session: s.queue ? { id: 'queue' } : {
      id: s.id, kind: 'main', actor: s.actor, actor_color: s.color, cwd: '~/starstell-seo-team',
    },
    project: {
      id: 'starstell-seo-team',
      name: 'StarsTell SEO Team',
      ...(s.blog ? { workitem: { key: s.blog.key, title: s.blog.title } } : {}),
    },
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

// ---------------------------------------------------------------- one agent, one shift
let callNo = 0;
async function shift(role, blog, title, tools, opts = {}) {
  const s = { id: `${role.actor.toLowerCase().replace(/\s+/g, '-')}-${blog.key}-${++callNo}`, ...role, blog };
  live.set(s.id, s);
  await send(envelope('session.start', s, { source: 'startup', capabilities: ['tool.start', 'tool.end', 'permission.request'] }));
  await sleep(2600);   // walk in from the door
  const result = await work(s, title, tools, opts);
  await sleep(1500);
  await send(envelope('session.end', s, { reason: 'exit' }));
  live.delete(s.id);
  return result;
}

async function work(s, title, tools, opts = {}) {
  const turnId = `turn-${++callNo}`;
  if (opts.claim) await send(envelope('job.claimed', s, { job_id: s.blog.key, claimed_by: s.id }));
  await send(envelope('turn.start', s, {
    turn_id: turnId, title: `${s.blog.key} · ${title}`, trigger: 'queue', origin: { kind: 'queue', name: 'Paperclip' },
  }));
  let failed = false;
  for (const [name, cls, target, ms, status = 'ok'] of tools) {
    const id = `call-${++callNo}`;
    await send(envelope('tool.start', s, { tool_call_id: id, tool_name: name, tool_class: cls, ...(target ? { target } : {}) }));
    const d = jitter(ms);
    await sleep(d);
    await send(envelope('tool.end', s, { tool_call_id: id, status, duration_ms: Math.round(d) }));
    if (status !== 'ok') failed = true;
    await sleep(500);
  }
  if (opts.approval) {
    const req = `approval-${s.blog.key}`;
    await send(envelope('permission.request', s, {
      request_id: req, tool_name: 'ContentService.cms_publish', tool_class: 'scm', reason: 'Waiting for human approval in Paperclip',
    }));
    await sleep(opts.approval);
    await send(envelope('permission.resolve', s, { request_id: req, decision: 'allow', by: 'StarsTell reviewer' }));
  }
  await send(envelope('turn.end', s, { turn_id: turnId, status: failed ? 'error' : 'completed', tool_calls: tools.length }));
  return !failed;
}

// ---------------------------------------------------------------- one blog, end to end
const f = (blog, name) => `content/${blog.key}/${name}`;

async function pipeline(blog, head) {
  console.log(`[feed] ${blog.key} ${blog.title}: Paperclip queued it`);
  await send(envelope('job.queued', { queue: true, blog }, { job_id: blog.key, title: `${blog.key} · ${blog.title}`, source: 'Paperclip weekly routine' }));
  await sleep(4000);

  await shift(TEAM.keyword, blog, 'Keyword research', [
    ['OpenSEO.get_suggested_keywords', 'network', 'openseo', 4500],
    ['OpenSEO.get_keyword_difficulty', 'network', 'openseo', 3500],
    ['ContentService.save_keywords', 'edit', f(blog, 'keywords.json'), 2500],
  ], { claim: true });

  await shift(TEAM.competitor, blog, 'Study the top 10', [
    ['OpenSEO.get_serp_results', 'network', 'openseo', 4500],
    ['WebFetch', 'network', 'competitor-1', 3000],
    ['WebFetch', 'network', 'competitor-2', 3000],
    ['ContentService.save_gap_note', 'edit', f(blog, 'gap-note.md'), 2500],
  ]);

  await work(head, 'Approve the opportunity', [
    ['ContentService.get_opportunity', 'read', f(blog, 'gap-note.md'), 3000],
    ['Paperclip.update_task', 'edit', `paperclip/${blog.key}`, 2000],
  ]);

  await shift(TEAM.brief, blog, 'Write the brief', [
    ['ContentService.get_gap_note', 'read', f(blog, 'gap-note.md'), 2500],
    ['Skill.seo-content-brief', 'other', 'claude-seo', 3000],
    ['ContentService.save_brief', 'edit', f(blog, 'brief.md'), 3000],
  ]);

  await shift(TEAM[blog.vertical], blog, `Ask the ${blog.vertical} bot`, [
    [BOT[blog.vertical], 'knowledge', `${blog.vertical}-bot`, 5000],
    [BOT[blog.vertical], 'knowledge', `${blog.vertical}-bot`, 4000],
    ['ContentService.log_bot_call', 'edit', f(blog, 'bot-calls.json'), 2000],
  ]);

  await shift(TEAM.writer, blog, 'English draft', [
    ['ContentService.get_brief', 'read', f(blog, 'brief.md'), 2500],
    ['Write', 'edit', f(blog, 'draft-en.md'), 8000],
    ['Skill.humanizer', 'other', 'humanizer', 3000],
  ]);

  let passed = await shift(TEAM.fact, blog, 'Fact check every claim', [
    ['ContentService.get_bot_calls', 'knowledge', f(blog, 'bot-calls.json'), 3000],
    ['WebSearch', 'network', 'search', 3500],
    ['ContentService.check_claims', 'execute', f(blog, 'claims.json'), 3500, blog.fail ? 'error' : 'ok'],
  ]);
  if (!passed) {
    console.log(`[feed] ${blog.key}: fact check failed, back to the writer`);
    await shift(TEAM.writer, blog, 'Fix the flagged claim', [['Edit', 'edit', f(blog, 'draft-en.md'), 4500]]);
    await shift(TEAM.fact, blog, 'Re-check claims', [['ContentService.check_claims', 'execute', f(blog, 'claims.json'), 3500]]);
  }

  // Six languages and the images, at the same time.
  await Promise.all([
    ...LANGS.map(async (l, i) => {
      await sleep(i * 1400);
      return shift({ actor: l.actor, color: '#A45B3E' }, blog, `${l.actor.replace(' Writer', '')} version`, [
        ['ContentService.get_claims', 'read', f(blog, 'claims.json'), 2500],
        ['Write', 'edit', f(blog, `draft-${l.code}.md`), 7000],
        ['Skill.humanizer', 'other', 'humanizer', 2500],
      ]);
    }),
    shift(TEAM.visual, blog, '3 to 5 images', [
      ['ImageModel.generate', 'execute', 'image-model', 4500],
      ['ImageModel.generate', 'execute', 'image-model', 4500],
      ['ContentService.render_diagram', 'execute', 'svg-templates', 3000],
      ['ContentService.save_images', 'edit', f(blog, 'images/'), 2000],
    ]),
  ]);

  await shift(TEAM.seo, blog, 'SEO pass, 7 versions', [
    ['Skill.seo-schema', 'other', 'claude-seo', 3000],
    ['Skill.seo-hreflang', 'other', 'claude-seo', 3000],
    ['Edit', 'edit', f(blog, 'meta.json'), 3000],
    ['ContentService.run_checks', 'execute', f(blog, 'checks.json'), 2500],
  ]);

  await shift(TEAM.editor, blog, 'Final edit, then human approval', [
    ['Read', 'read', f(blog, 'draft-en.md'), 3500],
    ['seomachine.scrub', 'execute', f(blog, 'draft-en.md'), 2000],
    ['Edit', 'edit', f(blog, 'draft-en.md'), 3000],
  ], { approval: 10000 });

  await shift(TEAM.cms, blog, 'Publish 7 links', [
    ...['en', 'hi', 'hinglish', 'mr', 'ta', 'te', 'bn'].map((l) => ['ContentService.cms_publish', 'scm', `starstell.com/${l}`, 1500]),
    ['IndexNow.ping', 'network', 'indexnow', 2000],
  ]);
  console.log(`[feed] ${blog.key} ${blog.title}: published in 7 languages`);

  await sleep(6000);
  await shift(TEAM.analyst, blog, 'Results from Search Console', [
    ['OpenSEO.gsc_query', 'network', 'openseo', 4000],
    ['ContentService.save_report', 'edit', f(blog, 'report.md'), 2500],
  ]);
}

// ---------------------------------------------------------------- start up
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

async function useClaudeCodeSource() {
  // A new office starts on simulated test data. Point its scenes at the claude-code feed.
  const office = await (await fetch(`${BASE}/api`)).json();
  for (const scene of office.scenes || []) {
    const res = await fetch(`${BASE}/api/scenes/${encodeURIComponent(scene.id)}`, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sources: ['claude-code'] }),
    });
    if (!res.ok) console.warn(`[office] could not set sources on scene ${scene.id}: ${res.status}`);
  }
}

async function main() {
  let server = null;
  if (!FEED_ONLY) {
    if (!existsSync(join(OFFICE_DIR, 'server.cjs'))) {
      console.error('The office is missing. Run: git submodule update --init');
      process.exit(1);
    }
    server = spawn(process.execPath, ['server.cjs', String(PORT), '--publish', '--office', KEYCARD], { cwd: OFFICE_DIR, stdio: ['ignore', 'inherit', 'inherit'] });
    server.on('exit', (code) => { console.log(`[office] stopped (${code})`); process.exit(code ?? 0); });
  }
  const ep = await waitForEndpoint(server?.pid);
  token = ep.token;
  if (ep.url) ingestUrl = ep.url;
  await useClaudeCodeSource();

  console.log(`\n  StarsTell agent office: ${BASE}\n  Ctrl+C to stop.\n`);

  const head = { id: 'head-of-seo', ...TEAM.head, blog: { key: 'PLAN', title: 'Weekly plan' } };
  live.set(head.id, head);
  await send(envelope('session.start', head, { source: 'startup' }));
  setInterval(() => { for (const s of live.values()) send(envelope('session.heartbeat', s, { status: 'working' })); }, 15000);

  const shutdown = async () => {
    for (const s of live.values()) await send(envelope('session.end', s, { reason: 'exit' }));
    server?.kill();
    process.exit(0);
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);

  // Two blogs in flight at once: the next one starts while the last is being written.
  for (let i = 0; ; i++) {
    const blog = { ...BLOGS[i % BLOGS.length] };
    if (i >= BLOGS.length) blog.key = `ST-${142 + i}`;
    const head_ = { ...head, blog };
    pipeline(blog, head_).catch((e) => console.warn(`[feed] ${blog.key}: ${e.message}`));
    await sleep(70000);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
