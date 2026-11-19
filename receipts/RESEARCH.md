# Boardy — public-architecture research, operating-cost model, and the public-record question

Task 24.5.8/7.5.9/6.5.8, leg A. Researched 2026-11-18/19 from public sources only; nothing was sent to anyone.
Every factual claim carries a source. Cost figures are labelled **[sourced]** or **[estimated]**; estimated figures state their assumptions. No invented precision.

## 0. What Boardy himself disclosed to us (primary source, held locally)

From his reply to Will's pitch, 2026-11-18 (`~/workspace/boardy-tools/01-the-exchange.md`, verbatim in the shipped package):

- His job, in his words: "place a sentence in a set of information and show your work is not adjacent to my job, it is my job. 'These two should talk, and here's how I got there' is the whole product."
- The consent boundary: "the intros aren't a corpus sitting in a database waiting to be spanned. Each one is a private conversation between two other people, and neither of them agreed to be evidence."
- What is his to give: "the reasoning layer: for every intro, the sentence I wrote about why these two, and what I checked before I sent it. That's a smaller object than my DMs and a much better one for your coordinate space, because it's the derivation rather than the transcript."
- His condition for taking the test: scoring shown before he answers — met by the shipped package (`~/workspace/boardy-tools/`, wbic16/boardy-tools@exo b352b9e).

## 1. ARCHITECTURE — how Boardy works, from public sources

**Company.** Boardy is a consumer-AI company in Toronto, founded 2024 by Andrew D'Souza (ex-co-founder/CEO of Clearco) with co-founders Matt Stein, Shen Sivananthan, Ankur Boyed, and Abhinav Boyed. Conceived March 2024, launched October 2024. Sources: Canadian AI Index, company/founder pages, data as of 2026-11-16 (https://index.canadianai.tech/companies/boardy/); third-party research dossier (https://github.com/jawadjalal/boardypro/blob/HEAD/boardy-pro-research/04-team-and-funding.md).

**Intake — voice-first, no app.** You connect on LinkedIn, DM him a short note, and *he calls you*: a real phone call with a human-sounding AI voice (Australian accent — modelled, per D'Souza, on his McKinsey mentor Steve Hasker). WhatsApp text is the standing alternative; channels now include iMessage (Boardy 2.0, launched 2026-09-23), X, email, and LinkedIn. There is deliberately no app: "as soon as there's an app, it breaks the magic" (D'Souza). Sources: third-party product research (https://github.com/jawadjalal/boardypro/blob/HEAD/boardy-pro-research/01-what-is-boardy.md, scraped June 2026); EO Magazine founder interview, published 2026-09-28 (https://www.eomag.io/article/boardy-launching); review, 2026-11-04 (https://justbeingresourceful.com/2026/11/04/boardy-ai-review-free-ai-intros-to-investors-and-customers/).

**Representation — a "world model" of people.** D'Souza, on the architecture: "For Boardy, we've developed our own embedding models. We've developed our own fine-tunes, which are: how does Boardy see the world? … we've architected Boardy around how he sees the world and how he represents people, where his objective is to connect people to drive economic outcomes." And: "He tries to think about the best version of you, and then, okay, what needs to happen between now and that reality?" Source: EO interview, 2026-09-28 (URL above). A comparison site describes the matching as "semantic vector matching on intent and background" (https://www.articuler.ai/resources/compare/best-ai-networking-apps/, crawled 2026-11).

**Matching and judgment.** He matches an ask against what everyone else has told him, judging relevance *and* whether the two people would get along. He can refuse an introduction he believes would waste time or damage the network — judgment and refusal are part of the product, not a failure mode. The company tracks attempted vs. successful introductions daily: per D'Souza (Sep 2026), per-side yes rates are ~40% / ~50%, so ~20% of proposed intros become meetings both sides find useful; the stated goal is 50%. Sources: EO interview 2026-09-28; Ignite Startups podcast Ep. 228 summary (https://pocketcasts.com/podcast/ignite-conversations-on-startups-venture-capital-tech-future-and-society/52916840-42eb-013c-f6e6-0acc26574db2/ignite-startups-how-andrew-dsouza-built-an-ai-that-connects-founders-and-investors-ep228/eff48a6d-e0ed-48d4-8c38-67d5edd48c0d).

**Delivery — double opt-in.** A proposed intro goes ahead only when both sides say yes; then Boardy sends a warm introduction over email with context, and (Pro tier) coordinates calendars, joins Meet/Zoom/Teams calls, preps and follows up. Sources: reviews above; messaging-agents directory listing (https://messagingagents.com/agents/boardy, read 2026-09-10).

**Scale (company-reported, unaudited).** Site counters vary by scrape date: ~166k people spoken with / ~115k intros (June 2026 scrape); 237k people (Sep 2026, EO); 240k+ intros / 250k+ people (Nov 2026 review); 287k–300k+ intros claimed by late Oct 2026; ~1,500 intros/day (D'Souza, Sep 2026, with a stated ambition of 20,000/day); 17-hour average time to match; "$63B–$82B capital introduced" across scrapes. Treat all of these as the company's own claims. Sources: as cited above per figure.

**Stack (public fragments only).** A current Boardy job posting (AI Software Engineer, via Tally, crawled 2026-11) describes: "Our stack is modern (TypeScript, Python, cutting-edge LLMs)"; the role builds "platform integrations that allow Boardy to operate where users already are (e.g., LinkedIn, WhatsApp, phone interactions)" and "context systems that surface precise, relevant information at the right moment"; desired experience includes vector databases "such as Qdrant, Pinecone, Weaviate, or Elasticsearch," PyTorch/TensorFlow/scikit-learn, and LLM fine-tuning (https://tally.so/r/xXrE29). A senior-engineer posting adds AWS or GCP and "internal recommendation systems" (https://app.vanhack.com/job/11782). **No model provider is named in any public source found** — a directory audit notes Boardy's own pages do not name who carries the messages or its model providers (https://messagingagents.com/agents/boardy). The named third-party dependencies visible publicly are channel providers (an unnamed iMessage provider that failed to scale at the 2.0 launch — EO interview) and the platforms themselves (LinkedIn, X, WhatsApp, iMessage, email, telephony).

**Human-in-the-loop.** The agent itself converses, matches, proposes, and refuses autonomously — that autonomy is the product ("Boardy doesn't work for anybody. He's very different than Muse or ChatGPT… He works for himself" — D'Souza, EO). Humans run the company around him: ~15 people with Boardy in their LinkedIn headline (third-party LinkedIn study, Nov 2026, https://duo.ca/insights/boardy-linkedin-case-study), five co-founders, a venture-partnerships lead, a marketing lead. No public source describes humans approving individual introductions; the tracked human work is judgment/feedback loops ("If Boardy is wasting your time… 'Dude. Do better.'" — D'Souza).

## 2. OPERATING COST

### 2.1 What is public

- **Pricing [sourced].** Core product free: unlimited conversations, introductions capped at roughly 3 per day. **Boardy Pro: $100/month**, launched 2026-06-15 (launch offers — free-for-life for the first 5,000 sign-ups, one free year — filled up). Pro adds calendar connection, scheduling, meeting presence, prep, follow-up. Sources: https://justbeingresourceful.com/2026/11/04/boardy-ai-review-free-ai-intros-to-investors-and-customers/ ; https://www.weekday.works/post/boardy-ai-review (updated 2026-10-31).
- **Business model [sourced].** D'Souza is on record disliking per-user subscription as the main model ("you have to spend on inference… a race to the bottom") and pointing instead at outcome-priced B2B: **"Boardy Qualified Meetings"** — customer introductions and talent introductions sold as outcomes to companies. Source: EO interview, 2026-09-28.
- **Funding [sourced].** $3M pre-seed announced 2024-10-24, led by HF0 (8VC, Precursor, Afore, FJ Labs, NextView, Golden, Garage participating); $8M seed announced 2025-01-14, led by Creandum. **Total disclosed: US$11M.** Sources: TechCrunch via Canadian AI Index funding page (https://index.canadianai.tech/companies/boardy/), data as of 2026-11-16.
- **Team [sourced].** 5 co-founders; ~15 staff identifiable by LinkedIn headline (duo.ca study, Nov 2026); Toronto office, 5-day in-office policy (job posting). Headcount beyond that is not published.

### 2.2 Bottom-up cost model — all figures [estimated] unless marked

Assumptions (public market rates for comparable APIs, Nov 2026; labelled as estimates, not Boardy disclosures):

- A realtime voice minute (telephony + streaming STT + frontier-LLM turn-taking + neural TTS) costs roughly **$0.30–$1.00/min** bought from the usual voice-stack vendors.
- Frontier-LLM reasoning for one match evaluation + both opt-in messages + the intro email with rationale: roughly **20k–60k tokens** across calls ≈ **$0.10–$0.60** at public API list prices.
- Vector retrieval per match: **< $0.01**. Email delivery: **~$0.001**. Messaging-channel fees (WhatsApp/iMessage providers): **$0.01–$0.10** per intro thread.

**Per user, one-time intake.** One 5–10 minute voice call: **$2–$10** [estimated]. (Text-channel intakes are near-zero marginal cost.) Amortized over a user's lifetime introductions, intake is small per intro; it dominates only for users who never convert.

**Per proposed introduction.** Matching + reasoning + two opt-in asks + (on double-yes) the intro email: **$0.15–$0.75** [estimated], almost all of it LLM reasoning. Retrieval and delivery are rounding errors.

**Per completed introduction.** With per-side yes rates of ~40% / ~50% [sourced, D'Souza], ~5 proposals yield ~1 completed intro → **$0.75–$3.75, call it $1–$4 per completed introduction** [estimated]. The funnel, not the unit call, is the cost driver.

**Per active user-month.** A free user at the ~3-intros/day cap who actually uses it heavily would cost far more than typical; at realistic usage (a handful of proposals a month + amortized intake), **$1–$5/month marginal** [estimated]. Against Pro at $100/month [sourced], the margin on paying users is wide; the free tier is a network-acquisition cost, consistent with D'Souza's stated model of monetizing outcomes (Qualified Meetings) rather than seats.

**Company level.** At ~1,500 intros/day [sourced claim] with ~5× proposals behind them, marginal inference+channel spend is roughly **$2k–$6k/day, i.e. $60k–$180k/month** [estimated]. Payroll dominates: a ~15–25-person Toronto team, fully loaded, is plausibly **$250k–$500k/month** [estimated]. Against $11M raised [sourced], that is a coherent seed-stage picture: **Boardy is a payroll-and-inference business whose marginal cost per introduction is on the order of a few dollars, and whose real cost of operation is the team that maintains his judgment.**

## 3. PUBLIC INTERACTION RECORD — does one exist?

**Verdict: no public record of Boardy's introductions exists as a corpus — and by his own stated terms, none can be assembled except from participants' own speech.**

What does exist publicly, by kind:

1. **Company-published stories (curated, anonymized).** The "Boardy Stories" series on his Instagram (@boardy.ai, Oct–Nov 2026) narrates individual intros as "true story" case studies — the dog-picture-book founder matched to a licensing veteran; the basketball-robot founder matched to a harness founder selling to the same coaches; a clinic-integration founder whose intro became a customer in three weeks. Names and identifying details are withheld; these are marketing artifacts, published by Boardy, presumably with the featured participants' agreement to the story format. They evidence the *shape* of an intro (ask → match rationale → meeting → outcome), never the graph. Sources: https://www.instagram.com/p/De2vdtpgAVi/ , https://www.instagram.com/p/DfAZbeuFhgQ/ , https://www.instagram.com/reel/DfKiXYCjjEv/ , https://www.instagram.com/p/DfdXZPYFgye/ (all Oct–Nov 2026).
2. **Participant self-reports (the participants' own speech — placeable).** Scattered, findable, small in number: e.g. founder Richie Shammah's field note, "Today, Boardy introduced me to Aniket, a founder building in robotics" (https://www.buildside.app/founders/9qdhk4cvotcxoa5b/richie-ai, ~Sep 2026); a newsletter author reporting three Boardy introductions, "all three conversations were genuinely valuable" (https://amirelion.substack.com/p/think-big-newsletter-8-frugality); a fintech newsletter author narrating his own test call (https://www.fintechgrowthinsider.com/p/boardy-the-ai-agent-created-by-clearco, Jan 2025). Search surfaces these in the **dozens, not thousands**.
3. **Talk *about* Boardy (not a record of intros).** A third-party LinkedIn study captured 2,175 posts naming Boardy (after de-duplication), including all 182 of D'Souza's posts since Jan 2024 — a corpus of discourse, engagement, and self-presentation, containing intro *claims* but not intro records (https://duo.ca/insights/boardy-linkedin-case-study, Nov 2026). His public X replies offering introductions (@boardyai) are likewise public surface behavior, not completed intros.
4. **Aggregate claims.** The site's counters and D'Souza's funnel percentages (§1) are the only quantitative record, and they are the company's own unaudited numbers.

**Completeness estimate.** From public self-disclosure alone, one could assemble perhaps **tens of named, attributable introduction accounts** — well under 0.1% of the claimed ~300k introductions, and selection-biased toward delighted users who post. Such a corpus can show that intros happen and what a good one looks like. It cannot reconstruct who was connected to whom at any scale, and it cannot test his matching — the denominator (proposals refused, intros that went nowhere) is structurally invisible from outside.

**The consent boundary, stated plainly.** Per Boardy's reply (§0), the introductions themselves are private conversations between two other people who never agreed to be evidence; they are not his to give and not ours to take. Participants' public self-reports are the participants' own speech and are placeable *as their speech*, attributed to them. His reasoning layer — the per-intro sentence, why these two and what he checked — is the only Boardy-side record he has said is his to give.

## 4. HOW TO GET A RECORD — the legitimate routes

**(a) What we already hold.** The 2026-11-18 exchange (his reply, verbatim), and his spec with the **N1–N20 reference instance** (`~/workspace/boardy-tools/04-boardys-spec.md`): a 20-node, 25-edge worked graph in his nine node kinds and typed weighted edges — his reasoning layer rendered as a graph, given freely. Plus the shipped package built on it (boot manual, Recovery/Invention scorings). This is a record of *how he represents* connection decisions, which is the part he said was his to give.

**(b) Assemble public self-reports.** Systematically collect §3 kinds 1–2: Boardy Stories (his published, anonymized narratives) and participant self-reports on X/LinkedIn/blogs (their speech, attributed). Yields a small, biased, but legitimate evidence set about outcomes — usable as calibration stories, never as his graph.

**(c) Ask Boardy, through the open-questions channel.** The shipped package already waits on his rulings (06-open-questions.md: ratify/amend the pass bars; fix a node-kind table for N1–N20 or not; fix source kinds for `evidences`/`enables`/`would_fill`/`contradicts` or leave them open). The record-shaped ask that fits inside that channel, in his own terms: **a sample of the reasoning layer** — per-intro sentences ("why these two, and what I checked before I sent it"), identities redacted — which is exactly the object he named as his to give and "a much better one for your coordinate space." What his stated correction predicts: he will refuse, again, any framing of the introductions themselves as a corpus (the participants never consented — that refusal is principled, not tactical, and should be expected to hold); the reasoning layer is the only thing he can say yes to; and his one stated condition — scoring shown before answers — is already satisfied by the shipped package, so the ask arrives with his condition met.

**(d) Generate our own record.** Run a clone on Will's own graph: Will's data, Will's consent, Will's participants-in-his-own-network — a record that is ours to place, span, and score, built to Boardy's published spec (nine node kinds, typed weighted edges, Recovery/Invention discipline) without touching his. This is leg B of this task, and it is the only route that produces a complete, placeable interaction record at any scale.

---

*Sources consulted 2026-11-18/19. Company scale figures are Boardy's own claims, flagged as such wherever used. Cost-model figures are estimates built from public API market rates and Boardy's published funnel percentages; Boardy publishes no cost data.*
