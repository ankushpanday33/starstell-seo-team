# Images

Every blog gets **3 to 5 generated images**. They are made once per blog and shared by all 7 language versions.

## 1. What each blog gets

| # | Image | Size | How it is made |
|---|---|---|---|
| 1 | Featured image (also the WhatsApp and social share image) | 1200 x 630 | AI image model |
| 2 to 3 | Concept illustrations inside the article | 1200 x 800 | AI image model |
| 0 to 2 | Diagrams: Sade Sati phases, kundli houses, numerology grid, tarot spread layout | 1200 x 800 | Drawn from a template (SVG), not by AI |

## 2. Rules

- **No text inside AI images.** Image models often garble words, especially in Devanagari, Tamil, Telugu and Bengali script. With no baked-in text, one image works in all 7 languages.
- **Diagrams carry the labels.** They are drawn from SVG templates, so each language gets its own labelled copy at almost no cost and with correct spelling.
- **StarsTell style:** Cosmic Heritage palette (Cosmic Dusk, Terracotta, Stellar Gold, Ivory). Warm, calm, like a brass diya at dusk. Flat or painterly, never neon "cosmic" stock art.
- **Not allowed:** frightening Shani, Rahu or Ketu imagery; AI faces presented as real StarsTell astrologers; gemstones or products shown as cures; disrespectful or inaccurate depictions of deities. Deity imagery follows traditional iconography and always gets human review.
- **Tarot cards:** only from a licensed or StarsTell-owned deck, never an AI imitation of a known deck.
- **Files:** WebP, under 150 KB, descriptive Romanised filenames (`sade-sati-three-phases.webp`). Lazy-load all but the featured image.
- **Alt text per language:** each image gets its alt text written in all 7 languages, under 125 characters, describing the image. Keyword only where natural.

## 3. Who makes them

A new **Visual Designer** agent:
1. Reads the brief and picks 3 to 5 image moments.
2. Writes prompts from the StarsTell style template.
3. Generates 2 options per image through the Content Service `image_generate` tool.
4. Builds diagrams from SVG templates.
5. Writes alt text in all 7 languages.

The images go to human approval with the article. A rejected image is regenerated, never published.

## 4. Model choice

Decision: **test 2 models in Phase 2**, for example a Google Gemini image model and an OpenAI image model. 20 StarsTell prompts each, scored on brand fit, Indian cultural accuracy, artefacts and cost. The API key for the winner goes into the secret store, never into the repo.

## 5. Open points

- Does StarsTell need to label AI-generated images, under Indian rules or its own brand policy? To confirm with legal.
- Who approves deity imagery?
