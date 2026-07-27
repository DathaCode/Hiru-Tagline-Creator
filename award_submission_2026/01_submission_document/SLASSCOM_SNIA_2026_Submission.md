# SLASSCOM National Ingenuity Awards 2026
## Best Tech for Good Software Innovation
### HiruNews AI Streamline

**Submitted by:** Lotus Technologies (Pvt) Ltd, under Asia Broadcasting Corporation (Pvt) Ltd
**Product Founder & Developer:** Mr. Vidath Dulanjith, DevOps Engineer, Lotus Technologies (Pvt) Ltd
**Contact:** vidath@lotustechnologies.lk

---

## Section 1 — Detailed Write-Up on the Innovative Product
<!-- [Section 1: 977 / 1000 words] -->

**AI-Powered End-to-End TV News Streamline for Hiru News**
*Developed by: Mr. Vidath Dulanjith, DevOps Engineer, Lotus Technologies (Pvt) Ltd*

### Who We Are

Lotus Technologies (Pvt) Ltd is the in-house software and IT engineering arm of Asia Broadcasting Corporation (Pvt) Ltd — the parent company of Sri Lanka's #1 television channel, Hiru TV, and the country's most-watched news broadcast, Hiru News. ABC's media network reaches approximately 90% of Sri Lanka's internet-connected population and commands 9 million or more followers across digital platforms. Hiru News has held the #1 position in Sri Lankan television news since 2012, earning over 30 national and international awards — from the SLIM Kantar People's Awards to the Golden Business Excellence Awards 2025 — throughout that period.

Lotus Technologies operates with a single mandate: engineer technology that directly serves ABC's mission of delivering timely, accurate, trustworthy news to every Sri Lankan, in every language, through every crisis. HiruNews AI Streamline is the product built from that mandate.

### The Problem: A Three-Bulletin Relay Race

Sri Lanka's traditional TV news production workflow is a human-intensive, multi-team relay. Before HiruNews AI Streamline, producing a single Hiru News bulletin required coordinating 35 or more staff members across news desk and graphics departments. The process was fully sequential and manual at every stage: reporters submitted raw press releases, audio recordings, and video packages; transcriptionists converted audio to text by hand; writers drafted taglines from those transcriptions; a senior editor reviewed and returned corrections; approved drafts were passed to a separate graphics team of 8 members who created broadcast tagline PNG overlays in graphic design software; completed PNGs were reviewed again against editorial standards; and finally, approved assets were loaded into the broadcast playout system.

Hiru News runs three live bulletins every day — at 11:55 AM, 6:55 PM, and 9:55 PM. Each bulletin contains approximately 20 news segments. On high-volume news days — elections, disasters, national emergencies — a single bulletin can require up to 80 separate tagline PNGs. Across three bulletins and 15 direct news team members per bulletin, the cumulative daily burden of the manual relay was enormous. Every handoff between teams introduced delay. Every correction cycle consumed minutes. In routine bulletins, those minutes meant missed editorial windows. In national emergencies — floods, landslides, cyclone evacuations, health crises — those same minutes could determine whether vulnerable citizens received a warning before or after the danger reached them.

### The Solution: One Unified Pipeline

HiruNews AI Streamline collapses the relay race into a single AI-assisted production pipeline with two integrated modules, designed, architected, and built entirely by Mr. Vidath Dulanjith, DevOps Engineer at Lotus Technologies (Pvt) Ltd.

**Module 1 — AI News Processing Engine** ingests raw press releases, audio recordings, and video packages. A layered AI stack — comprising Gemini Pro, OpenAI language models, and a locally hosted LLM component for handling sensitive material — performs speaker-diarized speech-to-text transcription, automatically generates Sinhala taglines and speaker subtitles, and produces pre-processed news copy ready for editorial review. Every AI-generated output is queued in an editorial approval dashboard. A senior journalist reviews, edits, and approves each item before it advances to production. No automation publishes directly to broadcast. Human editorial judgment is mandatory and structurally enforced at every stage — the AI assists, the journalist decides.

**Module 2 — Broadcast Graphics Engine, HiruTaglineCreator v2.1** is a production desktop application that receives approved taglines and renders them as broadcast-ready 1920×1080 transparent PNG overlays. Its core technical achievement is a bespoke FM-font rendering pipeline: a 762-line deterministic converter that transforms Singlish phonetic input through Sinhala Unicode into FM ASCII — the legacy encoding format used across Sri Lanka's broadcast and print industries for decades. This conversion handles the full complexity of Sinhala conjuncts and diacritics: rakaransaya, yansaya, ර්‍ය combinations, word-level exceptions such as "දුම්රිය", Latin-letter Private Use Area preservation, and pixel-perfect glyph placement through PyQt5's native HarfBuzz shaping engine. No commercially available tool converts FM-font Sinhala at this fidelity. The system supports dual broadcast graphic types — MAIN TAG and SUB TAG — and manages the complete session lifecycle aligned to Hiru News's bulletin cadence. The result: a single news team member now takes raw material from intake to broadcast-ready PNG within one unified application, with no graphics team involvement, while editorial oversight remains intact throughout.

### Live in Production — Including During a Real National Disaster

HiruNews AI Streamline entered production at Hiru News in **August 2025**. It has been in continuous daily use across all three bulletins since then, with no reversion to the prior workflow.

When the Ditwa Cyclone struck Sri Lanka in late November 2025 — among the most severe cyclone events of that year — the system was fully operational. Hiru News used the AI streamline to produce and broadcast disaster alerts, government-issued evacuation orders, hospital advisories, and emergency public safety directives throughout the crisis period. The speed of the streamlined pipeline enabled Hiru News to reach Sri Lankan citizens with verified, editorially approved, properly formatted emergency information faster than competing channels, during a real national disaster, while the system operated under full production load. This is not theoretical impact. It is proven, documented, real-world social good.

### Technical Summary

- **HiruTaglineCreator v2.1:** PyQt5 desktop application, PyInstaller-packaged, 762-line FM-font converter, dual MAIN/SUB TAG broadcast templates, session-based workflow management, on-device rendering with no cloud dependency for the broadcast production step
- **AI Processing Layer:** Gemini Pro + OpenAI API integration, speech-to-text with speaker diarization, Sinhala tagline auto-generation, editorial approval queue
- **Human-in-the-loop:** Senior editor mandatory approval before any content advances to graphics output
- **Engineering depth:** 24 documented engineering challenges resolved across eight iterative development stages

The entire system was built by Mr. Vidath Dulanjith using agentic AI-assisted software engineering with Claude Code — itself a demonstration that agentic development tools can produce broadcast-grade production software for linguistically underserved markets.

---

## Section 2 — How the Innovation Solves a Problem
<!-- [Section 2: 444 / 500 words] -->

*Evidence of positive impact on community, society, and the environment.*

### Sri Lanka's Disaster Reality and the Cost of Slow News

Sri Lanka is among the most disaster-exposed countries in South Asia. Floods, landslides, tropical cyclones, and health emergencies recur seasonally and affect millions of citizens — particularly those in rural, coastal, and low-income communities who rely on television as their primary source of news and public safety information. When disasters strike, the speed and accuracy of Sinhala-language TV news broadcasts directly shape life-and-death decisions: whether families evacuate, which roads are safe, which hospitals are accepting patients, which government directives apply to their area.

Before HiruNews AI Streamline, the multi-team manual relay adding 30 or more minutes to every bulletin's tagline and graphics production created a structural vulnerability in Hiru News's ability to respond to fast-moving emergencies. In a disaster context, a 30-minute delay between editorial approval and broadcast means a warning that should reach a coastal village before a storm surge may arrive after it.

### Proven Impact: The Ditwa Cyclone, November–December 2025

HiruNews AI Streamline was in full production at Hiru News when the Ditwa Cyclone struck Sri Lanka in late November 2025. Over the duration of that disaster event, Hiru News used the streamlined pipeline to produce and broadcast disaster alerts, government-issued evacuation routes, hospital advisories, and public safety directives continuously across its three daily bulletins. The production speed enabled by the unified AI pipeline meant that verified, senior-editor-approved emergency information reached the Sri Lankan public through Hiru News before it reached audiences through competing channels. This is not a modelled projection — it is a real operational outcome from a real national emergency, while the system was live.

### Serving Sinhala-Speaking Sri Lanka Since 2012

Hiru News has functioned as a trusted public service institution since 2012. It serves the majority of Sri Lanka's Sinhala-speaking population — including rural, elderly, and lower-income viewers who do not read English and for whom television news is not supplementary but primary. Every efficiency gain the AI streamline delivers compounds across this audience: more bulletins produced on time, fewer errors in critical government directives, faster breaking news turnaround.

The humanitarian dimension of this mission was formally recognised at the Golden Business Excellence Awards 2025, where Hiru News received the **Outstanding Humanitarian Service of the Year** award for "Rata wenuwen hiru sahana yaathra" — direct validation that the platform on which HiruNews AI Streamline operates has a documented, award-recognised record of community service.

### Measurable Impact

| Metric | Before | After |
|--------|--------|-------|
| Time per bulletin (tagline production) | Baseline | ~30 minutes saved |
| Overall workflow time reduction | — | ~68% |
| Cost reduction | — | ~45% |
| Staff coordination per bulletin | 35+ staff | Single-operator production |
| Error rate in tagline text | Higher (manual transcription) | Reduced (AI + human review) |

Every AI output remains under senior editorial review. Accuracy improves while human oversight is retained — no automation publishes without human approval.

---

## Section 3 — Why the Solution Is Innovative
<!-- [Section 3: 495 / 500 words — unchanged] -->

*What sets this product apart: core goals, values, and unique design.*

### First of Its Kind for Sinhala Broadcast

To our knowledge, HiruNews AI Streamline is the first end-to-end AI-integrated television news tagline production pipeline built natively for Sinhala broadcast in Sri Lanka. No other deployed system combines AI-assisted ingestion, Sinhala tagline generation, multi-model LLM processing, senior editorial approval workflow, and FM-font broadcast PNG rendering in a single unified pipeline. The challenge this represents is not trivial: Sinhala is classified as a low-resource language for AI systems, and the FM-font encoding standard used in Sri Lankan broadcasting has no publicly available high-fidelity Unicode conversion layer. Both problems were solved from first principles.

### Built Through Agentic AI-Assisted Engineering

The system was conceived, designed, and built entirely by Mr. Vidath Dulanjith, DevOps Engineer at Lotus Technologies, using agentic AI-assisted software development with Claude Code. This is itself an innovation: the application that uses AI in its production workflow was also built through AI-assisted engineering. It demonstrates that a single engineer with agentic tools can design and deploy broadcast-grade production software that would traditionally require a full development team — for a linguistically underserved market that larger technology companies have not served.

### The FM-Font Engine: A Rare Technical Artifact

The core of HiruTaglineCreator v2.1 is a technical artifact that does not exist in the commercial market. The 762-line deterministic Singlish → Sinhala Unicode → FM ASCII converter handles rakaransaya, yansaya, ර්‍ය conjuncts, word-level disambiguation for entries like "දුම්රිය", Latin-letter Private Use Area preservation within Sinhala text, and pixel-accurate typographic rendering via PyQt5's native HarfBuzz shaping engine. Twenty-four separate engineering challenges were identified, documented, and resolved across eight iterative development stages — ranging from Pillow bitmap rendering failures to PyInstaller Qt plugin packaging on Windows — before the system reached broadcast-quality fidelity.

### Values Driving the Design

The innovation is anchored by four interlocking values that informed every design decision:

1. **Sinhala-first language dignity** — the system treats Sinhala typography as a first-class engineering problem, not an afterthought
2. **Editorial integrity preserved** — AI generates, humans approve; the structure enforces this at every stage
3. **Operational resilience in crises** — on-device rendering with no cloud dependency for the broadcast step ensures the system functions during internet outages
4. **Speed as a social good** — in the context of disaster news, the time saved is not an efficiency metric; it is the difference between a warning that reaches people in time and one that does not

### Unique Design Features

- **Dual MAIN TAG / SUB TAG template system** for different broadcast graphic contexts
- **Raw Singlish input preserved** alongside converted Unicode, allowing editors to re-edit the phonetic source without re-transcribing
- **Session-based workflow** aligned precisely to Hiru News's three-bulletin daily cadence
- **Local LLM component** prototyped for on-premise processing of sensitive source material, protecting whistleblowers and confidential sources
- **Human-in-the-loop structure** embedded as a hard architectural requirement, not a configurable option

---

## Section 4 — How This Product Differs from Similar Products
<!-- [Section 4: 397 / 500 words] -->

*Comparison with existing solutions, highlighting unique differentiators.*

### The Market Landscape

Several categories of existing products address portions of the Hiru News production challenge. None addresses the full problem.

**Generic broadcast graphics platforms** (vMix, CasparCG, Ross XPression, Vizrt): These are powerful, widely deployed systems for broadcast graphics production. They require manual text entry for every tagline. They have no awareness of Sinhala FM-font encoding. They provide no Singlish-to-FM-ASCII conversion. They have no AI ingestion layer, no automatic tagline generation, and no editorial approval workflow. A graphics operator still inputs every word by hand, making them functionally equivalent to the manual process HiruNews AI Streamline replaced. They also carry significant licensing costs and require dedicated operator training.

**Generic AI transcription and language tools** (Otter.ai, OpenAI Whisper standalone, Google Gemini standalone, AssemblyAI): These tools handle the transcription and language generation side effectively in English and major world languages. They produce text output only — they have no broadcast graphics output stage, no FM-font rendering pipeline, no understanding of Sinhala diacritics, no MAIN TAG / SUB TAG template system, no session management aligned to newsroom cadence, and no editorial approval queue structured for a live production environment. Using them requires a separate graphics workflow to convert their text output into broadcast PNGs, which reintroduces the multi-team relay HiruNews AI Streamline eliminates.

**Outsourced graphics vendors**: Before HiruTaglineCreator, the graphics team handled PNG production as an in-house outsource equivalent. External or freelance graphics vendors carry high per-job cost, slow turnaround, zero AI layer, and are entirely unsuited to real-time crisis production. During the Ditwa Cyclone, a vendor-dependent workflow could not have produced the volume and speed of emergency broadcast assets the Hiru News team required.

**International newsroom management systems** (ENPS, Octopus Newsroom, iNEWS): These enterprise platforms manage editorial workflow at a high level. They are expensive, designed for large English-language newsrooms, and carry no localisation for Sinhala FM-font workflows. They do not render broadcast typography. They do not generate taglines. They require extensive infrastructure, dedicated IT teams, and are not deployed in Sri Lankan newsrooms.

### What Makes HiruNews AI Streamline Uniquely Different

| Capability | vMix / CasparCG | Otter / Whisper | Int'l Newsroom Systems | HiruNews AI Streamline |
|---|---|---|---|---|
| AI tagline generation (Sinhala) | No | Partial / No FM | No | Yes |
| Sinhala FM-font PNG rendering | No | No | No | Yes |
| Editorial approval workflow | No | No | Partial | Yes |
| Single-operator production | No | No | No | Yes |
| On-device rendering (no cloud dep.) | Partial | No | No | Yes |
| Deployed in live broadcast | Yes | No | No | **Yes — since Aug 2025** |
| Battle-tested in real disaster | No | No | No | **Yes — Ditwa Cyclone** |

The decisive differentiator is integration: HiruNews AI Streamline is the only solution that unifies AI ingestion, Sinhala language generation, editorial approval, and FM-font broadcast PNG rendering in a single workflow — deployed in daily live production and proven under crisis conditions.

---

## Section 5 — Emerging Area of Innovation
<!-- [Section 5: 490 / 500 words] -->

*Whether this technology falls into a cutting-edge field.*

HiruNews AI Streamline sits at the convergence of several distinct emerging technology fields, applying frontier techniques to a real-world deployment context that most of those fields have not yet reached.

### Generative AI and Large Language Models

The AI processing layer integrates Gemini Pro and OpenAI large language models to perform automatic Sinhala tagline generation, subtitle drafting, and news copy pre-processing. These represent current-generation generative AI capabilities applied to a production editorial environment. The system also incorporates a locally hosted LLM component — a prototype of on-premise AI inference for handling sensitive journalistic source material without transmitting it to third-party cloud services. On-premise LLM deployment for low-resource South Asian languages is an active frontier in both AI research and enterprise application.

### Low-Resource Natural Language Processing

Sinhala is formally classified as a low-resource language in the NLP and AI research communities. Pre-trained language models perform significantly worse in Sinhala than in English, Mandarin, or other high-resource languages, due to limited training data, complex morphology, and non-Latin script. Making generative AI produce high-quality, editorially acceptable Sinhala taglines for live broadcast — where errors have immediate public visibility — is a genuine technical frontier problem. HiruNews AI Streamline operates at this frontier in a live production deployment, not a research setting.

### Speech Recognition and Speaker Diarization

The system employs speech-to-text with speaker diarization — the ability to separate and label multiple speakers in audio recordings, such as press conferences and multi-speaker interviews. Diarized transcription for Sinhala-language audio is an emerging capability that few commercial services support with acceptable accuracy. Applying it to the newsroom workflow — automatically attributing speech to speakers and generating formatted transcripts ready for editorial review — reduces one of the most labour-intensive steps in the current production chain.

### Edge AI and Desktop-Embedded Intelligence

HiruTaglineCreator v2.1's FM-font rendering engine operates entirely on-device with no cloud dependency. This follows the emerging edge AI and on-device processing paradigm: cloud AI handles the computationally intensive ingestion and language generation step; local processing handles the production output step. This hybrid architecture ensures broadcast continuity during internet outages — critical for a news operation that cannot pause during disasters.

### Human-in-the-Loop AI Systems

The field of human-in-the-loop (HITL) AI is a growing discipline across high-stakes domains including medicine, law, and journalism. HiruNews AI Streamline implements HITL not as a design preference but as a hard architectural requirement: no AI output reaches broadcast without senior editorial approval. This positions the system as a practical, deployed implementation of responsible AI in a public-trust domain.

### Agentic AI-Assisted Software Development

The application itself was built using Claude Code, an agentic AI development environment. This makes HiruNews AI Streamline a product of the agentic software engineering paradigm — one of the most rapidly evolving areas of AI application — demonstrating that agentic development tools can deliver broadcast-grade production systems for underserved technical markets.

---

## Section 6 — How This Innovation Can Be Turned into a Sustainable Product
<!-- [Section 6: 484 / 500 words] -->

*Availability, replicability, and long-term scalability.*

### Currently Available and Operationally Proven

HiruNews AI Streamline is not a prototype awaiting deployment. Module 2 — HiruTaglineCreator v2.1, the Broadcast Graphics Engine — has been in continuous daily production use at Hiru News since August 2025. It handles all three live bulletins every day. The product's sustainability is already demonstrated by its sustained adoption in the highest-pressure live broadcast environment in Sri Lanka: a news operation with zero tolerance for production failures, running 365 days per year.

### Financially Self-Sustaining Through Demonstrated ROI

The system has already delivered measurable cost reduction internally. An approximate 45% reduction in production costs, combined with 68% reduction in time spent on manual tasks, generates a positive operational ROI that funds continued development. Lotus Technologies does not require external grant funding — the efficiency gains pay for ongoing development capacity.

### Replicable Modular Architecture

The system is designed with clean separation between its three functional layers: the AI ingestion and generation layer, the editorial approval layer, and the FM-font broadcast rendering engine. Each layer can be adapted independently. A newsroom with a different language can replace the Sinhala FM-font converter with a Tamil or English rendering module. A broadcaster with different AI service preferences can swap the LLM integration layer without affecting the editorial approval or rendering stages. This modularity makes the architecture replicable across diverse newsroom environments without requiring a full rebuild.

### Immediate Internal Pilot Base: ABC Sister Stations

Asia Broadcasting Corporation operates a group of radio and television stations beyond Hiru TV and Hiru News: Hiru FM, Gold FM, Sun FM, Sooriyan FM, and Shaa FM. These stations provide an immediate, ready pilot base for language expansion of the system. Sooriyan FM serves Tamil-speaking audiences — a direct pathway to a Tamil-language tagline generation and rendering module. Gold FM and Sun FM serve English-language audiences, enabling an English-language workflow variant. The internal pilot infrastructure exists within the ABC group without requiring external partnerships.

### Subscription Licensing for Commercial Rollout

Lotus Technologies is developing a subscription-based licensing model to offer HiruNews AI Streamline to other broadcasters. Organic industry demand already exists: other Sri Lankan broadcasting channels have expressed interest in the technology without any promotional outreach from Lotus Technologies. The subscription model makes the product accessible to smaller regional stations that need the technology but lack the development resources to build it independently, creating a sustainable revenue stream that funds continued product development.

### Long-Term Social Impact Sustainability

Television remains the primary news medium for most Sri Lankan households — particularly rural, elderly, and lower-income audiences not served by digital-only news. The speed, accuracy, and accessibility gains HiruNews AI Streamline delivers continue generating social value every day, through every bulletin, for every viewer who relies on Hiru News as their primary source of public safety information and national events.

---

## Section 7 — Further Improvements and Wider Adoption Potential
<!-- [Section 7: 493 / 500 words] -->

*Potential improvements and wider adoption possibilities.*

### Planned Technical Improvements

**Tamil and English multilingual expansion** is the highest-priority near-term development. ABC's Sooriyan FM serves Tamil-speaking Sri Lankans — one of the country's most linguistically underserved broadcast audiences. Extending the pipeline to Tamil would bring the same speed and accuracy benefits that Sinhala has already received. English integration for Gold FM and Sun FM follows naturally from the same modular architecture.

**Full on-premise local LLM deployment** is prototyped and planned for the next development phase. Moving AI inference entirely on-device eliminates cloud API dependency for sensitive source material — protecting whistleblowers, confidential sources, and editorial intelligence from external cloud exposure. This is both a privacy improvement and an operational resilience improvement, as it removes internet connectivity as a dependency for the AI processing step.

**Broadcast playout system integration** — direct injection of approved PNGs into vMix or CasparCG playout systems without manual file handling — would eliminate the remaining manual step in the production chain, where an operator currently moves approved PNG files to the broadcast workstation.

**Auto-suggestion of story angles and rundown ordering** based on historical bulletin patterns and breaking news signals would extend the AI layer from tagline generation into editorial planning support — helping producers structure bulletins faster on high-volume news days.

**Mobile editorial approval application** would allow senior editors to review and approve AI-generated taglines from any location during field assignments, travel, or off-site emergencies — ensuring the production pipeline does not pause when key editorial staff are not at the news desk.

**Real-time subtitle generation for live broadcast** would extend the accessibility benefits of the system to hearing-impaired viewers, directly addressing a disability inclusion dimension that current production workflows do not serve.

**Automated source verification** against trusted government and institutional databases would add a fact-check layer before editorial approval, further reducing the risk of error in public safety communications.

### Wider Adoption Potential

The subscription licensing model positions HiruNews AI Streamline for adoption well beyond Hiru News:

- **South Asian regional broadcasters** facing low-resource language constraints — Tamil, Bengali, Urdu, Sinhala, Nepali — face identical problems to those HiruNews AI Streamline solved. The architecture is directly adaptable.
- **Community and regional television stations** in Sri Lanka and the region that cannot afford large graphics teams represent an underserved market. Subscription access to a hosted version of the system would put broadcast-quality tagline production within reach of small broadcasters.
- **Disaster communication agencies and government public information units** that need to produce fast, accurately formatted multilingual alerts during emergencies represent a non-broadcast application of the same core technology.
- **Educational and public interest broadcasters** producing Sinhala or Tamil educational content would benefit from the same AI-assisted tagline and subtitle pipeline.

The broader opportunity is a platform: the same modular architecture can be configured for any language, broadcast format, or newsroom context — with each deployment reinforcing the commercial model that funds ongoing development.

---

## Section 8 — Awareness Efforts and Recognition
<!-- [Section 8: 500 / 500 words] -->

*Public and industry engagement, market reactions, awards, and media coverage.*

### On-Air National Visibility: The Most Direct Awareness Mechanism

HiruNews AI Streamline operates through a fundamentally different awareness model than conventional software products. Most software reaches users through marketing campaigns or sales engagement. This product's output appears on Sri Lanka's #1 news broadcast — live, across three bulletins daily — reaching approximately 90% of the country's internet-connected population, every day, since August 2025. Every tagline overlay seen on Hiru News since that date was produced by this system. There is no awareness mechanism more direct than having your product's output visible to an entire nation every day.

### Internal Adoption as the Strongest Product Validation

Hiru News operates under zero-failure conditions: missed bulletins and production failures have immediate, nationally visible consequences. Since August 2025, the production team has used HiruNews AI Streamline as their standard daily tool with no reversion to the prior workflow. Sustained adoption by a high-pressure live broadcast team — where any failure produces an on-air problem — is the strongest possible validation of a production tool's reliability and value.

### Platform Recognition: Hiru News's Award History

The platform on which HiruNews AI Streamline operates is the most-awarded news brand in Sri Lanka. Selected awards:

- **SLIM Kantar People's Awards** — Most Popular TV News Provider (2024, 2025, 2026)
- **Raigam Tele'es** — Most Popular TV News Channel (2024); Best Television News Broadcast (2025)
- **Asia Miracle Awards** — Most Popular News Channel & Brand (2024, 2025)
- **Sumathi Awards** — Best TV Investigative News Reporting; Best TV Current Affairs Reporting (2023)
- **Golden Business Excellence Awards 2025** — Outstanding Humanitarian Service ("Rata wenuwen hiru sahana yaathra"); Most Influential Media Platform; Media Excellence Award
- **Platinum Excellence Awards 2026** — Best News Brand; Most Popular Investigative News; Most Influential Media Platform
- **People's Excellency Awards** — Most Popular TV News Channel (2024, 2025)
- **Business World International Awards 2025** — Best TV News Provider; Most Viewed YouTube Channel

Full list: https://www.asiabroadcasting.lk/achievements.php

These awards affirm that the broadcast graphics produced by HiruNews AI Streamline meet the highest editorial quality standards recognised by the Sri Lankan media industry.

### Organic Industry Demand

Without any promotional outreach, other Sri Lankan broadcasting organisations have expressed interest in adopting the technology. This unsolicited demand demonstrates the product's industry value and has directly motivated Lotus Technologies to develop a subscription licensing model for commercial rollout.

### Formal Recognition Strategy

This SLASSCOM submission is Lotus Technologies' deliberate first step in formalising industry recognition for HiruNews AI Streamline. Planned follow-on activities include subscription licensing demonstrations to regional broadcast clients and internal rollout to ABC sister stations as a proof-of-expansion case study.

The awareness model is unique: most software must find its audience. This product's audience finds it every day, on national television, because the product IS the broadcast.

---

*Submitted by Lotus Technologies (Pvt) Ltd (under Asia Broadcasting Corporation (Pvt) Ltd)*
*Developer & Founder: Mr. Vidath Dulanjith, DevOps Engineer*
*Contact: vidath@lotustechnologies.lk*
