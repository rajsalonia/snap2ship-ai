# Submission-day QA matrix — Snap2Ship AI

Date: 26 Oct 2026 · hard deadline 16:00 IST. **Do not delay submission for cosmetic fixes.**

## Current evidence (recorded, not re-run by this document)

- Current main GitHub Actions builds/tests passed, including backend, React, generated templates and Docker build.
- Previously recorded local verification: 44 passing backend tests, 3 generated app production builds, sample browser interactions, and ZIP export.
- Public free Render demo: https://snap2ship-ai-api.onrender.com/ — previously tested with sample data; can cold-start.
- Real Gemma 4 provider inference: **not verified** (API key missing in testing environment).
- DigitalOcean hosting: **prepared, not deployed**; credit verification / account confirmation needed.
- Free Render and mock/curated sample cannot be presented as real Gemma reasoning.

## Highest-priority actions

1. **P0 / provider:** Configure `GEMINI_API_KEY` privately and run `python scripts/check_gemma.py --all`. Verify real image+text response and structured 3-idea output. Record only pass/fail and sanitized error details.
2. **P0 / live demo:** Open the actual public Render URL in Chrome; refresh, verify HTTP health and `/api/sample`. Confirm current deployed SHA or redeploy current main before describing updated UI.
3. **P0 / generated artifacts:** For event, checklist and info, choose ideas, compile, verify actual Vite output and React iframe, interact, download ZIP, unzip and run `npm ci && npm run build`.
4. **P0 / submission:** Create truthful screenshots, 60–90 sec demo or recording, and submit to the official MLH portal. Verify confirmation and save submission receipt.
5. **P1 / responsive:** Viewport screenshots at 390 × 844, 768 × 1024, and 1440 × 900. Check horizontal overflow, legibility, color contrast, touch targets, focus and font fallback with network blocked.
6. **P1 / camera:** On HTTPS or localhost, request camera permission only after button click; capture → retake → use photo → analyze; refuse permission; close by Escape/backdrop; ensure media tracks stop. Test upload PNG/JPEG/WebP as alternate input.
7. **P1 / backend resilience:** Empty text, invalid MIME, corrupted image, >5 MB, >16 MP, rate-limits, upstream 401/403/404/429, invalid model JSON, app compile fail/timeout, concurrent AI cap, and CORS. Do not weaken secret handling.
8. **P1 / generated app UX:** Event: search/save/unsave/filter/checklist. Checklist: add/complete/delete/active/done/persistence. Info: search/accordion/anchor scroll. Keyboard-only navigation and mobile viewport.
9. **P2 / cosmetic:** Tune floating glassmorphism spacing, gradients, readable typography and fallback fonts only after demo path is stable. Avoid moving away from photo-first design.

## Engineering checks

```powershell
git status --short
git pull --ff-only origin main
python -m pytest -q backend/tests
python scripts/compile_samples.py
cd frontend
npm ci
npm run build
cd ..
python scripts/audit_secrets.py
python scripts/check_gemma.py --all
```

When using `scripts/verify_pipeline.py`, start the local backend first. Use the project's virtual environment and dependency instructions in README; do not claim a check ran if prerequisites were missing.

## Visual QA details

- Glass card text must meet usable contrast; no unreadable translucent overlays.
- Hero doesn't overlap CTA or top navigation at narrow widths.
- Uploaded/captured source photo remains fully legible and isn't excessively obscured.
- Loading state conveys actual API/build progress, not fabricated percent complete.
- Labels, keyboard focus outlines, modal focus and reduced-motion behavior are preserved.
- DM Sans/Outfit use `display=swap`; the app must still render with system fallback offline.
- Generated mini-app uses self-contained system fonts and should build/run without external font CDN.

## Provider / deployment truth table

| Capability | Current claim |
| --- | --- |
| Gemma 4 multimodal SDK wired to backend | Yes |
| Real Gemma 4 provider access verified | No |
| 3 templates compile in local/CI | Yes |
| Public curated sample via Render | Previously verified; recheck live |
| DigitalOcean App Platform live | No |
| DigitalOcean promotional credits confirmed | No |
| Custom-trained Gemma model | No |

## GitHub coordination

Work from latest main; there may be concurrent coding agents. Do not force-push, do not overwrite concurrent changes, and keep each commit independently meaningful. Never commit API keys, user photos or local credentials.

**Freeze nonessential development by 15:20 IST; prioritize submission immediately.**
