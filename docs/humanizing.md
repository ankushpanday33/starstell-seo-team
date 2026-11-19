# Humanizing

Goal: articles that read as if a knowledgeable, caring person wrote them for one reader. Humanizing here means better writing for readers. It does not mean trying to fool AI detectors, and it never changes facts.

## 1. Tools evaluated (19/11/2026)

| Repo | What it actually is | Maintenance | License | Decision |
|---|---|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | An agent skill that rewrites text to remove 26 signs of AI writing, based on Wikipedia's "Signs of AI writing". Keeps every claim. Says plainly it does not try to beat AI detectors | v4.0.0 on 10/11/2026, 70,963 stars | MIT | **Use** as a skill for the Senior Editor and Language Writers. Pin the version |
| [AI4Bharat/IndicLLMSuite](https://github.com/AI4Bharat/IndicLLMSuite) | Datasets and pipelines for **training** Indic language models (Sangraha corpus, IndicAlign, Setu cleaning pipeline). Not a humanizer | Last commit 07/10/2024 | MIT (code) | **Do not use for humanizing.** Use one piece: the Indic toxic-word lists (in AI4Bharat/setu) as a safety filter, after checking their licence. Its Romanization Dictionary is still marked "coming soon" |

## 2. Where humanizing happens

```
Writer draft  ->  Humanize pass  ->  Claim check  ->  SEO pass  ->  Senior Editor  ->  Human approval
```

- **Humanize pass:** the Language Writer runs the humanizer skill on its own draft, with a StarsTell voice sample so the rewrite matches the brand.
- **Claim check after it:** the Fact Checking agent confirms the rewrite kept every verified claim and added none.
- **SEO pass after humanizing**, so keywords survive and placement rules from [article-spec.md](article-spec.md) still hold.

## 3. English and Hinglish

The humanizer skill's patterns are written for English and mostly apply to Hinglish. Top patterns it removes:
1. "Not X but Y": "It's not just a transit, it's a transformation."
2. One-line closers: "Let that sink in."
3. Sayings that sound deep: "At its core, what really matters is..."
4. Staged run-ups: "Here's the thing."
5. Arguing with no one: "I'm not saying X, but..."

## 4. Hindi, Marathi, Tamil, Telugu, Bengali

The humanizer skill has no rules for Indic languages, so we add a **StarsTell Indic style guide** (skill file, written with native reviewers) covering the AI and translation tells we see in these languages:

| Tell | Fix |
|---|---|
| Translationese: English sentence order carried into Hindi or Tamil | Rewrite in natural word order for that language |
| Over-formal or heavily Sanskritised words where everyday words are used | Use the words people speak and search, taken from keyword research |
| English idioms translated literally | Use a local expression or say it plainly |
| Every paragraph opening the same way ("इसके अलावा", "इसलिए") | Vary openings; cut connectors that add nothing |
| Generic examples that could be from any country | Local festivals, family situations, regional customs |

Each language's guide grows from reviewer feedback: every rejected phrase becomes a rule.

## 5. Voice

Every version follows the StarsTell voice: the trusted family aunt who listens, explains plainly and never frightens. Name the astrological mechanism, tie outcomes to effort, promise nothing guaranteed. Hinglish is welcome where the reader is Hindi-first.

## 6. Checks

- Humanize pass recorded in the article history (before and after text kept).
- Claim check must pass after humanizing.
- Native reviewer marks any phrase that "sounds like a machine"; those feed the style guide.
