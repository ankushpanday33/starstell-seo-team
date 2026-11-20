# Example: life path number 7 (ST-144)

One blog taken end to end by Claude playing every agent in the StarsTell team, to show what the finished system produces.

- **The published blog** in 7 languages, with its Google listing and WhatsApp share preview (full article body in English and Hindi; title, description, key takeaways and alt text in all 7).
- **How the team made it:** 13 steps from the Paperclip task to the approval queue, with each agent's real output: keywords, a live competitor study, brief, knowledge notes, fact check, humanize pass, language versions, 4 images with alt text in 7 languages, meta tags, JSON-LD schema, hreflang and 46 automatic checks, then the Seryvon score gate (SEO, GEO and AEO 90+), with the real runs saved in `scores/`.

Not connected yet, and stood in for: OpenSEO (live web search instead, no volumes), the StarsTell Numerology bot (Claude's own numerology knowledge, then fact checked), the image model (SVG drawings), the CMS (not published; it waits at human approval).

## Open it

```bash
python -m http.server 8766 --bind 127.0.0.1 --directory examples/life-path-number-7
```

Then visit http://127.0.0.1:8766/index.html, or open `index.html` directly in a browser.

## The as-published pages

`preview/` holds each language as a real page with its own head tags and schema, exactly what the score gate audits:

```bash
python -m http.server 8767 --bind 127.0.0.1 --directory examples/life-path-number-7/preview
```

```bash
python scoring/score_gate.py http://127.0.0.1:8767/blog/life-path-number-7/
```

## Rebuild it

`build.py` holds all the content and computes the counts and checks:

```bash
python examples/life-path-number-7/build.py examples/life-path-number-7/index.html
```
