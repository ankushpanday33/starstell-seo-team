# Article spec

Every article the team produces must meet this spec. The SEO Optimization agent applies it, the Content Service checks the measurable rules automatically, and the Senior Editor checks the rest before human approval.

Domain `www.starstell.com` below is a placeholder until the site URL is confirmed.

## 1. URL (slug)

| Rule | Example |
|---|---|
| Contains the primary keyword; lowercase; hyphens | `/blog/sade-sati-remedies` |
| 3 to 5 words; drop filler words (the, a, for, of) | `/blog/tower-card-love-meaning` |
| No dates or IDs on evergreen posts | Not `/blog/2027/11/post-4821` |
| Year only on time-bound posts | `/blog/diwali-2027-lakshmi-puja` |
| Each of the 7 languages on its own path, Romanised slug ([multilingual.md](multilingual.md)) | `/hi/blog/sade-sati-ke-upay` |
| Never changed after publishing; if forced, 301 redirect | |

## 2. Meta title (`<title>`)

- 50 to 60 characters (Hindi in Devanagari: 45 to 55).
- Primary keyword in the first half.
- Ends with ` | StarsTell` when it fits.
- Unique across the site.
- Year only on time-bound posts.
- Not allowed: ALL CAPS, clickbait, "100% accurate", "guaranteed", fear words.

Example: `Sade Sati Remedies: What Actually Helps | StarsTell` (51 characters)

## 3. Meta description

- 140 to 155 characters.
- Primary keyword once, naturally.
- Says what the reader learns, plus a soft reason to click.
- Unique across the site. StarsTell voice: reassuring, no promises.

Example: `Sade Sati is a season, not a curse. Learn its three phases, which remedies help, and how to use this Saturn period for steady growth.`

## 4. Meta tags in every article

```html
<title>Sade Sati Remedies: What Actually Helps | StarsTell</title>
<meta name="description" content="...">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://www.starstell.com/blog/sade-sati-remedies">
<link rel="alternate" hreflang="en" href="https://www.starstell.com/blog/sade-sati-remedies">
<link rel="alternate" hreflang="hi" href="https://www.starstell.com/hi/blog/sade-sati-ke-upay">
<meta property="og:type" content="article">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://www.starstell.com/images/sade-sati-three-phases.webp">
<meta property="og:url" content="https://www.starstell.com/blog/sade-sati-remedies">
<meta property="article:published_time" content="YYYY-MM-DD">
<meta property="article:modified_time" content="YYYY-MM-DD">
<meta name="twitter:card" content="summary_large_image">
```

Not used: `meta keywords` (ignored by Google since 2009 and exposes our targets), hashtags in meta, `noindex` on live posts (drafts and previews only).

To confirm with the CMS: which of these the site template already outputs, and whether the sitemap updates on publish.

## 5. Page structure

| Element | Rule |
|---|---|
| H1 | Exactly one. May be warmer and longer than the meta title |
| Key takeaways | 40 to 60 words directly under the H1, answering the query (featured snippets and AI answers quote this) |
| Table of contents | Posts over 1,500 words |
| H2 | 4 to 8 sections, many phrased as real "People also ask" questions |
| H3 | Sub-points under an H2. Never skip a level |
| Paragraphs | `<p>`, 2 to 4 sentences, 40 to 80 words. First paragraph under each H2 answers it directly |
| FAQ | 4 to 6 questions at the end |
| Author box | Named reviewer astrologer and "Last updated" date |
| Call to action | Soft invitation to talk to a StarsTell astrologer, never fear-based |
| Excerpt | 1 to 2 lines for listing pages and social sharing |

## 6. Length

Set per article from the top 10 Google results (see [competitor-research.md](competitor-research.md)), not fixed. Typical ranges:

| Type | Words |
|---|---|
| Quick answer ("What is Mangal Dosha") | 800 to 1,200 |
| Tarot card meaning | 1,200 to 1,800 |
| Festival guide | 1,500 to 2,200 |
| Pillar page | 2,500 to 4,000 |

## 7. Images and alt text

Full rules in [images.md](images.md).

- 3 to 5 generated images per blog, shared by all 7 language versions: 1 featured image at 1200 x 630 (also the share image) plus 2 to 4 inline. No text inside AI images; labelled diagrams are drawn from SVG templates per language.
- StarsTell palette (Cosmic Dusk, Terracotta, Stellar Gold, Ivory). Calm and warm. No fearful Shani or Rahu imagery. No AI-made faces presented as real astrologers.
- Tarot images only from a licensed or StarsTell-owned deck. Numerology and kundli as simple diagrams.
- WebP, under 150 KB, descriptive filenames (`sade-sati-three-phases.webp`). Lazy-load all but the featured image.
- **Alt text on every image, in every language**: describes the image, under 125 characters, keyword only where natural (about one image). Decorative images get `alt=""`.
- A person approves every AI-generated image.

## 8. Hashtags

None in the article body or meta tags. Use CMS categories and tags for site structure (Vedic Astrology > Shani > Sade Sati). Hashtags only in social captions, if a social agent is added later.

## 9. Keyword use

One primary keyword per article; the Content Strategist blocks two articles targeting the same one.

| Keyword type | Where it goes |
|---|---|
| Primary ("sade sati remedies") | Slug, meta title, H1, first 100 words, one H2, meta description, one image alt |
| Secondary and long-tail ("sade sati remedies for career") | H2 and H3 headings, body |
| Questions from "People also ask" | H2 headings and FAQ |
| Related terms (Shani, dhaiya, Saturn transit, 12th house) | Body, naturally |
| Keywords in each of the 7 languages ("sade sati ke upay") | That language's own version, from its own keyword research, linked with hreflang |

No target keyword density. A sentence that reads unnaturally because of a keyword is rewritten.

## 10. Structured data

BlogPosting (author and reviewer), BreadcrumbList, FAQPage. Google shows FAQ rich results mainly for government and health sites, but the markup still helps AI answers understand the page.

## 11. Voice and safety

Every version gets a humanize pass ([humanizing.md](humanizing.md)). Every sentence passes the StarsTell copy test: name the astrological mechanism, tie outcomes to the reader's effort, promise nothing guaranteed or overnight. Never "predict", "destiny", "fate" or "fortune". No specific tithi, muhurat or festival date goes live without SME sign-off.

## 12. Automatic checks (Content Service)

| Check | Fails when |
|---|---|
| Title length | Outside 50 to 60 characters (45 to 55 Devanagari) |
| Description length | Outside 140 to 155 characters |
| H1 count | Not exactly 1 |
| Heading order | A level is skipped |
| Alt text | Any non-decorative image without alt, or alt over 125 characters |
| Primary keyword | Missing from slug, title, H1, first 100 words or description |
| Duplicate | Title, description or primary keyword already used on another page |
| Banned words | Guarantee, predict, destiny, fate, fortune, 100% accurate |
| Image weight | Over 150 KB |
