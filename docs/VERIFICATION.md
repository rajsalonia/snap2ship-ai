# Verification report — 26 October 2026

Story: input image/text → validated planning specification → three ideas → selected trusted template → real compilation → compiled React preview → source ZIP.

## Passing local checks

| Check | Actual result |
| --- | --- |
| Original backend baseline | 9 tests passed before edits |
| Updated backend | 42 tests passed; no failures; 2 dependency deprecation warnings |
| Dashboard production build | Passed; 1,584 modules transformed; JS ~170.62 kB, CSS ~16.50 kB before gzip |
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

Compiler details are recorded in `template-build-results.json`. The curated sample is not live AI output. Unit tests intentionally disable real compilation by default; the separate compiler checks perform genuine builds for all categories.

## Not yet verified

- Genuine Gemma text, image-plus-text and structured-output requests: **NOT RUN**, because `GEMINI_API_KEY` is absent and the owner chose to continue without live access.
- DigitalOcean public deployment, account credits and production CORS/health: awaiting account access and cost/credit verification.
- Docker image: configuration authored; local Docker engine was not running. GitHub Actions includes a container build check; its result must be inspected separately.
- Browser-managed source download: the in-app browser download observation timed out. ZIP validity and contents pass through the actual API; browser download behavior requires another browser check.
- Information-site runtime interactions and full mobile viewport behavior: production compilation passed; further browser checks are still pending.
- Hackathon form submission/acceptance: no form destination or receipt has been verified.

## Corrected failures

The first generated-app build caught an invalid stylesheet import; it was removed and all three builds passed. Browser testing caught form submission blocked inside the sandboxed preview; task creation now uses direct button/keyboard handlers and the add/complete/filter interaction passed. Initial sandbox restrictions on Node subprocesses were resolved by running the authorized compiler checks with the required execution access.

## Remaining limits

Only three template categories are supported. Compilation is not a test of every interaction or factual accuracy. No database, authentication, payments, registration, notifications, distributed rate limits, automatic generated-app publishing, or Gradient AI integration is claimed. The iframe has session-only state; standalone apps persist state locally when browser storage is available.
