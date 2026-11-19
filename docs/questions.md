# What we need before coding

Send documentation, never keys. Do not paste API keys, tokens or passwords into chat, issues or commits. Share docs and samples with keys removed; real keys go into the secret store on the server.

Tick items as they arrive.

## API 1: Vedic Astrology bot
- [ ] Base URL (staging and production)
- [ ] API documentation (OpenAPI, Postman or PDF)
- [ ] Authentication method
- [ ] Request parameters
- [ ] Sample request, key removed
- [ ] Sample response
- [ ] Capabilities, including whether it returns panchang, muhurat or festival dates
- [ ] Rate limits and cost per call

## API 2: Tarot bot
- [ ] Base URL
- [ ] API documentation
- [ ] Authentication method
- [ ] Request parameters
- [ ] Sample request, key removed
- [ ] Sample response
- [ ] Capabilities (spreads, card combinations, yes/no)
- [ ] Rate limits

## API 3: Numerology bot
- [ ] Base URL
- [ ] API documentation
- [ ] Authentication method
- [ ] Request parameters
- [ ] Sample request, key removed
- [ ] Sample response
- [ ] Capabilities (Chaldean, Pythagorean)
- [ ] Rate limits

## Website and publishing
- [ ] StarsTell website URL
- [ ] CMS technology (the StarsTell repo can be inspected to find out)
- [ ] CMS API documentation, or how blog posts are stored
- [ ] Hosting preference: AWS, GCP or Hungama data centre

## Google access
- [ ] Search Console: who can add a service account as a user
- [ ] GA4 property and who can grant Viewer access
- [ ] Which conversion event counts as a new StarsTell customer

## Decisions
- [ ] Architecture approved
- [ ] StarsTell brand guide on file is current
- [ ] SME astrologer for festival, panchang, muhurat and remedy sign-off
- [ ] Byline and AI disclosure policy: who is the named author or reviewer on each article
- [ ] Monthly article target and monthly budget cap
- [x] Languages: English, Hindi, Hinglish, Marathi, Tamil, Telugu, Bengali (7 links per blog)
- [ ] Native-speaker reviewer for each of the 7 languages
- [ ] Full review for every language, or sample review for some once quality is proven
- [x] Image model: test 2 models in Phase 2
- [ ] Image model API account for the test (Google, OpenAI or other)
- [ ] Legal: must AI-generated images be labelled?
- [ ] Who approves deity imagery
- [ ] Licensed or StarsTell-owned tarot deck images
- [ ] 3 to 5 approved StarsTell writing samples per language for context/writing-examples.md
- [ ] Is the StarsTell CMS WordPress? (decides whether seomachine's WordPress publisher is reused)
- [ ] Budget cap for 280 pages a month (estimate $810 to $980 a month)
- [ ] Anthropic API account and DataForSEO account: existing or new
