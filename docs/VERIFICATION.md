# Verification report — 26 October 2026

Story: input image/text → validated planning specification → three ideas → selected trusted template → real compilation → compiled React preview → source ZIP.

## Verified public deployment

**https://snap2ship-ai-api.onrender.com/** is live on the free Render plan. Deployed code revision: `8be73aacfe993862f45ac0392c037ce3a5f6661a`; [its Linux CI passed](https://github.com/rajsalonia/snap2ship-ai/actions/runs/40297446895).

Public checks passed: dashboard HTTP 200, health HTTP 200 with compiler available, exactly three labelled curated proposals, real event/checklist/information-site builds, compiled React previews and valid 11-file source ZIPs. Empty analysis input returned HTTP 400; analysis without a provider key returned the expected HTTP 503. This is not a successful live Gemma test. See [actual public build logs](live-verification.json).

Free hosting can sleep after inactivity; allow time for the service to wake before presenting.

## Passing local checks

| Check | Actual result |
| --- | --- |
| Original backend baseline | 9 tests passed before edits |
| Updated backend | 44 tests passed; no failures; 2 dependency deprecation warnings |
| Dashboard production build | Passed; 1,586 modules transformed; JS ~176.47 kB, CSS ~28.88 kB before gzip |
| End-to-end pipeline check | Passed (`scripts/verify_pipeline.py`); verified health, 3 ideas, real Vite builds, preview and base64 ZIPs |
| Event generated-app production build | Passed, with HTML, bundled JS and stylesheet present |
| Checklist generated-app production build | Passed, with HTML, bundled JS and stylesheet present |
| Information-site generated-app production build | Passed, with HTML, bundled JS and stylesheet present |
| ZIP API | Valid ZIP with source, lockfile, README, MIT license and actual build report |
| Image validation | PNG/JPEG/WebP decoded; corrupt data, MIME mismatch, excessive size and invalid input rejected |
| Provider boundary | Mock SDK tests cover text and image bytes; exact configured model is used |
| Failure honesty | Missing key, quota/access errors, malformed output, compiler failure, timeout and unavailable compiler remain failures/unverified |
| API security checks | Validation response omits submitted values; compiler environment excludes Gemini key; CORS and rate-limit tests pass |
| Secret audit | No recognized credentials or private environment files in publishable source |
| Browser sample flow | Three labelled sample proposals and a real compiled event app rendered |
| Browser event interactions | Saving an event and searching for Web Workshop passed |
| Browser checklist interactions | Added “Charge my laptop”, completed it, filtered Done; preview showed 1/4 complete |
| Browser information-site interaction | Search for “laptop” filtered to the “What to bring” section |
| Mobile preview control | Actual iframe width measured at 390 pixels; sandbox remains `allow-scripts` |
| Actual browser source download | Chrome saved `campus-create-companion.zip`; archive contents and build report verified |
| Downloaded app standalone build | Fresh `npm ci` from the task cache and `npm run build` passed on the exact downloaded archive |
| Linux CI | [All three jobs passed](https://github.com/rajsalonia/snap2ship-ai/actions/runs/40290796448): backend/templates, frontend and container |
| Linux backend count | 41 passed, 1 skipped, 1 dependency warning; the skipped local-dist check passes locally |
| Deployment image | Linux container builds; Node/Python imports, installed compiler and frontend assets verified in CI |
| App specification | YAML and local invariants pass; remote DigitalOcean validation requires account credentials |

Compiler details are recorded in `template-build-results.json`. The curated sample is not live AI output. Unit tests intentionally disable real compilation by default; the separate compiler checks perform genuine builds for all categories.

## Not yet verified

- Genuine Gemma text, image-plus-text and structured-output requests: **NOT RUN**, because `GEMINI_API_KEY` is absent and the owner chose to continue without live access.
- DigitalOcean public deployment and split-origin CORS: not verified. The owner approved a free static frontend with the free Render API. The $0/month static-site wizard still requires account verification. No paid service was created. Same-origin production frontend/API communication on Render is verified.
- Full dashboard phone-viewport override: browser automation timed out. The embedded 390-pixel mobile preview was verified separately.
- Hackathon form submission/acceptance: no form destination or receipt has been verified.

## Corrected failures

The first generated-app build caught an invalid stylesheet import; it was removed and all three builds passed. Browser testing caught form submission blocked inside the sandboxed preview; task creation now uses direct button/keyboard handlers and the add/complete/filter interaction passed. Initial sandbox restrictions on Node subprocesses were resolved by running the authorized compiler checks with the required execution access.

## Remaining limits

Only three template categories are supported. Compilation is not a test of every interaction or factual accuracy. No database, authentication, payments, registration, notifications, distributed rate limits, automatic generated-app publishing, or Gradient AI integration is claimed. The iframe has session-only state; standalone apps persist state locally when browser storage is available.
