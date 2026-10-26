# Setup: start here

The original downloaded project was preserved and continued. The app now compiles generated React projects rather than presenting structural checks as production builds.

Follow the repository README or run `scripts/start-local.ps1` in PowerShell. It installs the Python, frontend and trusted compiler dependencies and starts hidden local servers. Logs and process IDs are under `.local-logs/`.

- Dashboard: http://127.0.0.1:5173
- Health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

## Credential

Copy `backend/.env.example` to `backend/.env` and configure `GEMINI_API_KEY` yourself. Use Google AI Studio / Gemini Developer API, not Google Cloud Agent Studio. Do not paste the key into chat, commit it, include it in screenshots, or put it in a frontend variable.

`python scripts/check_gemma.py --all` checks a genuine text request, structured text analysis and fictional-poster image analysis. It prints safe statuses, not your key.

No key was supplied during initial verification. The owner chose to continue without live Gemma access. Keep this limitation visible in the submission until the live checks pass.

## Demo without a key

Click **Try a fictional campus poster** to load curated sample proposals, explicitly labelled as sample data. Build any category. Real compilation and the actual React preview still run. An unavailable compiler produces an explicit unverified state.

## Generated app

Extract the downloaded ZIP, then run:

```sh
npm ci
npm run build
npm run preview
```

The ZIP includes source, lockfile, README, MIT license and `BUILD-REPORT.json`. The generated app needs no API key or database. Browser state persists when storage is available; the embedded preview intentionally keeps session-only state.

Read `docs/VERIFICATION.md` and `docs/template-build-results.json` for evidence.
