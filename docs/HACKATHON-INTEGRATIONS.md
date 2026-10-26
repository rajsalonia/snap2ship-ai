# Hacktoberfest 2026: sponsor-fit and demo checklist

Event: **Hacktoberfest Hack Day Delhi × SKILLOP DTU**, 26 October 2026. Submission deadline: **4:00 PM IST**.

Snap2Ship AI is a **photo-first, open-source Gemma 4 micro-app factory**. This document distinguishes implemented software from sponsor integrations that still need account verification.

## Category B — Best Use of Gemma 4

- **Core AI role:** Google `gemma-4-26b-a4b-it` is used to interpret images and written descriptions, produce source observations and generate three typed, scoped app specifications.
- **Multimodal demo:** Camera photo (HTTPS or localhost) or uploaded PNG/JPEG/WebP + optional explanation → `/api/analyze` → Gemma 4 → three ideas, evidence and uncertainty.
- **Realistic builder:** Selected idea → `/api/build` → trusted React/Vite template → actual compilation when compiler is available → sandboxed preview + downloadable ZIP.
- **Important honesty:** A configured key is **not** proof of a successful model call. The example poster route is clearly labeled fictional and does not invoke Gemma.

## Category A — Best Open-Source AI Project

- MIT licensed repository containing frontend, backend, templates, build checks, tests and GitHub Actions.
- Open-weight Gemma model is the central intelligence component, not an optional chat panel.
- Traceable source facts, constrained app-template choices and real build logs make the pipeline reviewable.
- Distinctive feature: start with real-world photographed problem evidence, not a ready-made text prompt.

## DigitalOcean (MLH category sponsor)

Current evidence: the complete app is [live on free Render](https://snap2ship-ai-api.onrender.com/), with all three public template builds verified. DigitalOcean's free static frontend is prepared on `digitalocean-free-20261026`; the wizard confirms $0/month but requires owner account verification. No DigitalOcean hosting is claimed yet, and no paid resource was activated.

- `.do/app.yaml` and `Dockerfile` prepare a **single DigitalOcean App Platform deployment** for React + FastAPI on one origin. The user must attach GitHub source, provide an encrypted Gemini API key, and verify credits / cost settings.
- This does **not** mean the project has been deployed on DigitalOcean.
- Gradient Inference/ADK, GPUs, knowledge bases, managed agents and auto-generated-app deployment are **not claimed** as integrated. They are not necessary for the chosen MVP.
- Credits: check actual promotional balance, expiry and projected charges before deployment; no unapproved paid resources.

## Demo flow for judges (60–90 seconds)

1. Open Snap2Ship's floating glass studio on HTTPS or localhost.
2. Click **Take a photo**, grant camera permission, capture an example college poster, review photo and click **Use photo**. Or use **Upload image** if webcam permission fails.
3. Add a short goal such as “Students need to find event sessions and plan what to bring.”
4. Press **Analyze with Gemma**. Explain actual model status and source uncertainty.
5. Choose one GO/REVIEW idea; click **Build**.
6. Show actual compiler logs, React preview, interactive event checklist, and source ZIP.
7. Show GitHub README, MIT license and GitHub Actions.

## Do not claim

- Custom-trained Gemma model or fine-tuning (not performed).
- Live image inference unless a real Google AI Studio key succeeds.
- Full autonomous deployment of generated applications (not implemented).
- DigitalOcean hosting or Gradient AI inference until a live run is verified.
- Universal app generation: currently only event, checklist and information-site templates are supported.

## Privacy, accessibility and robustness

- Camera permission is requested only after selecting **Take a photo**; the video feed stays local and stops on close or capture.
- API receives an image only after the user explicitly submits it for analysis. Do not upload sensitive documents.
- Image validation enforces MIME/content matching, max 5 MB and max 16 MP.
- Concurrency limit allows at most two model requests at a time; per-IP rate limiting still applies.
- Phone UI has responsive layouts, keyboard-focus styles and reduced-motion support.
- Source extraction is fallible. Users should verify deadlines, names, claims and generated content.

Official references:
- Gemma API + image input: https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api
- DigitalOcean App Platform: https://docs.digitalocean.com/products/app-platform/how-to/create-apps/
- Event page: https://www.mlh.com/events/hacktoberfest-hack-day-delhi-x-skillop-dtu
