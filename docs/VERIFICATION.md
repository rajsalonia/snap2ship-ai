# Verification — 26 October 2026

Current cloud validation at approximately 2:00 PM IST. No features or application logic were changed during this onboarding run. The coding cutoff remains 3:20 PM IST today.

## Source and scope

The complete uploaded `snap2ship-ai-integrations-ready.zip` was safely extracted and inspected, including `docs/INTEGRATION-STATUS.md`. Its original 10 backend tests and frontend compilation passed. The existing GitHub repository subsequently supplied newer application source at `1f531feb34b4bdd4a34809d80086a97ba7baf61b`; that source is the basis of this validation branch. Further UI/camera commits appeared on `main` during validation. They are preserved there and are **not covered by this report**. No force push, source replacement, reset, or feature rebuild was used. The imported archive remains preserved separately in the cloud workspace and a named Git stash.

## Actual outcomes

| Check | Result |
| --- | --- |
| Uploaded archive baseline | **10 passed**, no failures; one dependency deprecation warning |
| Validated repository backend | **42 passed**, no failures; one Starlette/httpx deprecation warning |
| Dashboard production build | **Passed**; Vite 5.4.21, 1,584 modules; same-origin `VITE_API_URL=/` |
| Event, checklist and information templates | **All three genuinely compiled**; current compiler reports in `template-build-results.json` |
| Browser sample flow | Actual image upload, missing-key 503, three explicitly curated proposals, real build, interactive React preview and browser-managed source ZIP download verified |
| Event interactions | Search, save, saved-only filter and removal passed |
| Checklist interactions | Add, complete, filter, progress and delete passed |
| Information interactions | Search, expand/collapse and empty state passed; embedded navigation has the defect below |
| Mobile | Preview toggle and 390px dashboard layout checked; no horizontal page overflow |
| Exported source | Browser-downloaded event ZIP passed fresh `npm ci` and `npm run build`; exported information ZIP also passed a fresh install/build |
| Local container | Built and started as non-root; dashboard, health, sample, real compilation, preview payload and valid ZIP passed with **512 MiB / 1 CPU** limits |
| Repeatability | Complete saved installation script rerun successfully; `pip check` found no broken requirements |
| Genuine Gemma text/image requests | **NOT RUN**: `GEMINI_API_KEY` is absent; `scripts/check_gemma.py --all` exits 2 |
| DigitalOcean account, balance, promotional credits/expiry | **NOT VERIFIED**: credential absent; original read-only checker exits 2 |
| DigitalOcean deployment / public workflow | **NOT RUN**: billing, credits, prepayment and overage protections remain unverified |
| MLH form / acceptance | **NOT SUBMITTED**; no verified receipt or public deployment URL |

The browser report records **14 passing checks and one confirmed application failure**; its aggregate exit status is **1**, not an all-pass result. Early rapid-click attempts were timing-sensitive; the completed run uses paced interactions. No sample result is described as live AI output. Screenshots are from the local curated-sample workflow, not DigitalOcean or Gemini.

## Confirmed application defect

In the compiled `srcdoc` preview, fragment links such as **Back to top** resolve against the hosting dashboard URL. Clicking the link navigated the iframe to the dashboard's `/#top` and left the generated preview. Search, expansion, task controls, compilation and source download still worked. Application source was left unchanged during onboarding; fixing embedded fragment navigation is a separate coding change. Do not demonstrate these links as working inside the preview.

Standalone exported event and information app fragment navigation **passed**, as recorded separately in `evidence/standalone-results.json`. This defect does not justify calling the live, deployed end-to-end workflow verified.

## Container and setup details

The managed cloud requires a session CA for package traffic. A local Dockerfile variant outside the checkout adds BuildKit CA mounts to npm/pip installation steps, preserving TLS checks; it makes no application changes and is not a modified deployment specification. The tracked Dockerfile was not rewritten. Initial non-root startup failed because local checkout files had restrictive permissions; tracked source read/traverse permissions were normalized, then the image was rebuilt and successfully exercised. No credential was baked into the image.

The standard virtual environment, frontend dependencies, template compiler and compiled dashboard are prepared. Install and startup instructions are saved in the environment configuration draft, alongside missing Gemini and DigitalOcean secret requirements. Saving a draft does not inject credentials or publish a new environment; review/save and publication remain separate user actions.

## Evidence and submission assets

- `evidence/backend-tests.xml`, `evidence/uploaded-baseline-tests.xml`: actual pytest runs.
- `evidence/browser-results.json`: successful interactions and failed embedded navigation kept distinct.
- `evidence/container-results.json`: current container health and real compiler results.
- `evidence/source-provenance.json`: archive digest and exact application commit tested.
- `screenshots/01-input-studio.png` through `07-mobile-dashboard.png`: local sample screenshots; the older `03-compiled-preview.png` is retained from the prior repository.
- `SUBMISSION.md` and `VIDEO-SCRIPT.md`: prepared text, not a submitted form or produced video.

External services remain blocked pending secure credential configuration. Verify credit expiry, App Platform applicability, price, usage and charge liability before any DigitalOcean provisioning. No paid resources or prepayment were created by this session.
