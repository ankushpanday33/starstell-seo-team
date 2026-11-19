# StarsTell agent office

A live 3D office where every StarsTell agent is a character. Agents walk in through the door when Paperclip gives them work, go to the prop that matches what they are doing, and clock off when they finish.

Built on [The Roving Office](https://github.com/atlassian-labs/roving-office) by Atlassian Labs (Apache-2.0), included as a git submodule pinned to commit `f3c51c8`. We do not modify it; we feed it events.

## Run it

Needs Node 18 or newer.

```bash
git submodule update --init
```

```bash
node visualizer/starstell-office.mjs
```

Then open http://127.0.0.1:8090/office/STAR-7EAM

Faster: `SPEED=2 node visualizer/starstell-office.mjs`. Stop with Ctrl+C.

Starting the office writes its local address and write token to `~/.roving-office/endpoint.json`; that is how The Roving Office works on any machine.

## Where things are in the room

| In the office | In our system |
|---|---|
| Paper plane into the **mailbox** | **Paperclip** assigns a new blog task (ST-142 and so on) |
| Character walking in through the **door** | Paperclip wakes an agent for its step |
| **Globe** turning | **OpenSEO** and the web: keywords, SERPs, competitors, Search Console |
| **Bookshelf**, book in hand | Your **StarsTell bots** (Vedic, Tarot, Numerology): knowledge StarsTell owns |
| Sitting at a **desk** | Writing, editing, checks through the Content Service |
| Status **waiting on you** | **Human approval** in Paperclip before publishing |
| **Outbox / printer** | Publishing the 7 language links to the StarsTell CMS |
| Crumpled paper in the **bin** | A draft that failed the fact check, sent back to the writer |

The desk label shows the task and step, for example `ST-142 · Fact check every claim`. Click a character to see its current tool, such as `OpenSEO.get_serp_results` or `StarsTell.vedic_ask`. Press `?` in the office for all controls.

## What it shows today, and later

- **Today:** `starstell-office.mjs` simulates the pipeline for 6 example blogs, using the same Agent Office Protocol events a real Claude Code agent sends.
- **Later:** Paperclip's agents run on Claude Code, and The Roving Office ships a Claude Code adapter (`npm run connect:claude` inside `roving-office/`). Once Phase 1 is running, the real agents appear in this office instead of the simulation.

## Step-by-step example with outputs

[walkthrough.html](walkthrough.html) walks one blog, "Sade Sati remedies", through all 17 steps and shows what each step produces: keyword table, gap note, brief, bot answer, fact check, 7 language titles, images, meta tags and the published page in 7 languages. All its data is illustrative. Open it in any browser.
