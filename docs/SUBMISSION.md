# Snap2Ship AI submission pack

**Title:** Snap2Ship AI

**Tagline:** From Real-World Problems to Working Apps

**Event:** Hacktoberfest Hack Day Delhi × SKILLOP DTU, 26 October 2026

**GitHub:** https://github.com/rajsalonia/snap2ship-ai

**Verified live URL:** Not yet available. DigitalOcean deployment is awaiting account access and credit/cost verification.

## Ready-to-paste project description

Snap2Ship AI is an MIT-licensed prototype that turns real-world software needs into small, functional React applications. Users upload a campus poster, screenshot or handwritten note, or describe a problem. The backend integrates Google's Gemma 4 through the official Google GenAI SDK to request source observations and exactly three practical app proposals. Pydantic validates the specifications, while the dashboard explains each idea's audience, limited MVP features, complexity and feasibility score.

After a user chooses an idea, the app factory combines bounded structured content with trusted React/Vite templates for an event tracker, checklist or information site. It runs a genuine production build in a temporary workspace, exposes compiler logs and output checks, previews the compiled React app, and exports source with a lockfile and actual build report. A successful compilation is never represented as proof of factual accuracy or exhaustive testing.

Our differentiator is image-led discovery for student and community needs, narrow functional templates, explicit review of source observations and honest build evidence. The workflow was inspired by vibeDeploy; our code, interface and assets are original.

The local backend tests, frontend production build and all three generated-app builds pass. Live Gemma access has not been verified because no API key was supplied; the recorded sample path is explicitly curated and makes no model call. DigitalOcean deployment files are prepared, but hosting and Gradient AI integration are not claimed until verified.

## Inspiration

Useful software needs hide in notices, informal task lists and screenshots. Students often need a small practical tool, not a complex platform. We wanted a shorter path from something noticed in the real world to an application people can inspect, run and adapt.

## What it does

Image/text input → bounded source observations and three proposals → transparent ranking → user selection → trusted React template plus structured data → real compilation → interactive preview → source ZIP.

The event template supports searchable sessions, saved events and preparation tasks. Checklists support task creation, completion, deletion, filters and progress. Information sites support search, expandable sections and navigation.

## How we built it and architecture

React, Vite and responsive CSS form the dashboard. FastAPI validates images and requests, and Pydantic validates model specifications. The Google GenAI SDK is configured for `gemma-4-26b-a4b-it`, with the secondary Gemma identifier available only through explicit configuration. The factory compiles repository-controlled code, not arbitrary AI-generated JavaScript. A Docker image packages the dashboard, Python API and trusted Node compiler for DigitalOcean App Platform.

No database, GPU instance, paid agent framework or additional AI provider was added. API secrets stay backend-side and are withheld from compiler subprocesses.

## Gemma 4 usage and current evidence

Gemma 4 is the implemented multimodal planning integration for image/text understanding, source observations and structured app specifications. The SDK call path is tested with controlled mocks for text, PNG, JPEG and WebP. Genuine account/model access is **not yet verified**. There is no silent fallback to another model and no simulated result presented as a genuine response.

The fictional Campus Create Day sample exists to demonstrate the downstream factory transparently while live credentials are unavailable. It is not evidence of Gemma's output quality.

## DigitalOcean usage

The requested deployment target is DigitalOcean App Platform. A same-origin Docker deployment and app specification are prepared. Until the active deployment and public endpoint are verified, state: **deployment prepared, not deployed/verified**. No Gradient AI integration is implemented.

## Challenges and solutions

- Structural checks could not establish whether generated apps compiled. We added genuine Vite compilation, captured logs, checked assets and preserved failure/unavailable states.
- General AI code generation would increase execution risk. We narrowed generation to bounded specifications and repository-owned templates.
- Image extraction and scores can sound authoritative. We separated source observations from suggestions and exposed a clear feasibility rubric and uncertainty note.
- Sandboxed preview behavior differs from standalone apps. Browser testing caught and repaired task creation inside the preview; storage is optional and session-only in the iframe.
- Credentials were unavailable. We preserved explicit access errors and labelled the curated sample rather than inventing a successful provider call.

## Accomplishments and learning

We continued the existing project, preserved its source history, expanded input/schema/compiler/error tests, compiled all three app categories and verified real interactions in the browser. We learned that compilation, runtime behavior, factual accuracy and external integration access require separate evidence.

## Future roadmap

Verify genuine Gemma calls with a usable account; improve extraction evaluation; add more interaction-tested templates; extend accessibility checks; add deployment publishing only after the core pipeline has broader coverage. Keep generated app scope small and reviewable.

## Difference from vibeDeploy

The shared inspiration is a discover → evaluate → build workflow. Snap2Ship focuses on visual real-world input, student/community micro-apps, a constrained template factory, explicit source-fact review and visible build evidence. It uses original source, branding and UI and is not affiliated with vibeDeploy's creators.

## Intended categories

1. Best Use of Gemma 4 — the integration is central, but genuine image/text access must pass before presenting it as verified.
2. Best Open-Source AI Project — MIT source, reproducible setup, tests, transparent template logic and contribution instructions.

Do not claim eligibility, prize approval, DigitalOcean hosting or a successful live Gemma demo solely from this document.

## Thirty-second elevator pitch

Every campus poster hides a small software opportunity. Snap2Ship AI helps turn that observation into a working starting point: upload an image, review three scoped app ideas, choose one and get a React app with real build logs, an interactive preview and downloadable source. We use trusted templates and visible verification so students can understand what was generated. Our current demo uses a clearly labelled fictional sample; live Gemma access is still awaiting a key.

## Two-minute presentation and recording script

| Time | On screen | Say |
| --- | --- | --- |
| 0:00–0:15 | Input Studio and fictional poster | “A notice contains useful information, but turning it into a tool takes work. Snap2Ship connects that observation to a small app.” |
| 0:15–0:30 | Poster preview and context | “This is an original fictional campus poster with no private information.” |
| 0:30–0:45 | Analyze control and missing-key response, or a genuine successful response if later verified | “Gemma 4 is our implemented planning engine. For today's current recording, no live key is configured, so we will use the explicitly labelled curated sample.” |
| 0:45–1:05 | Three sample cards, facts and score rubric | “Here are three scoped options. These sample proposals are curated. The score describes builder feasibility, not independent market research.” |
| 1:05–1:25 | Build selected event idea, then compiler logs | “The factory compiles trusted React templates with structured content. These are actual npm build logs.” |
| 1:25–1:45 | React preview: search a session, save an event, add/complete a task | “This is the compiled React app. Its interactions work inside the isolated preview.” |
| 1:45–2:00 | Source ZIP, GitHub and actual hosting status | “The export includes source, a lockfile and the real build report. Our source is MIT licensed. DigitalOcean hosting is shown only if its public deployment has been verified.” |

If genuine Gemma access is later verified, replace the missing-key/sample segment with the real request, keep all source-fact and score caveats, and record the actual result. Do not edit the sample disclosure out of a sample-based recording.

## Screenshot sequence

1. Input Studio with fictional poster and context.
2. Three cards with the curated-sample badge and scoring rubric.
3. Build verified status, compiled React preview and actual logs.
4. Mobile preview and a working interaction.
5. Public repository and verified live URL, if available.

Saved screenshots are in `docs/screenshots/`, including the compiled event preview and 390-pixel mobile information-site preview. No video recording has been produced; use this exact sequence and script for a truthful recording.

## Final submission checklist

- Confirm the GitHub repository contains the reviewed source and MIT license.
- Review `docs/VERIFICATION.md` and use its actual pass/fail/untested status.
- Add a public deployment link only after checking it.
- Disclose missing live Gemma access until real checks pass.
- Keep API keys and account/billing screens out of the submission.
- Submit to the event's actual form and confirm acceptance before 4:00 PM IST. No submission receipt has been obtained by this build process.
