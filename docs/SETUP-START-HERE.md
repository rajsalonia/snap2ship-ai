# START HERE — Snap2Ship AI (Hacktoberfest Delhi 2026)

## What is already implemented

- **Web UI:** image upload (PNG/JPEG/WebP), text description, 3 Gemma idea cards, GO/REVIEW/NO-GO, app selection, generated HTML preview, downloadable React/Vite code ZIP.
- **API:** `POST /api/analyze` (real Gemma 4), `POST /api/build` (deterministic template assembly), `GET /health`.
- **Safety:** 5MB max upload, image MIME check, structured Pydantic response validation, HTML escaping, no eval of model-provided code, API key on server, no file storage in app.
- **Limitations:** The model endpoint has NOT been called with your personal API key, the main React frontend production build has NOT been run in this environment, no DigitalOcean deployment, no GitHub auto-push. `POST /api/build` performs structural checks only, not npm compile.

## Google AI Studio vs Google Cloud — important

Use **Google AI Studio** at https://aistudio.google.com/api-keys, not Google Cloud Agent Studio. `Gemma 4` is **the AI model**; the **Gemini API** is a hosted service that lets backend Python call Gemma. Your Google Cloud free trial can still be pending. Verify the Gemini Developer API tier and model access independently in AI Studio. Do not make a Google Cloud prepayment just for this MVP without confirming you need it.

## Windows / VS Code: quickest start

Prerequisites: Python 3.10+, Node.js 20+ with npm, VS Code. Extract the ZIP and open the `snap2ship-ai-ready` folder.

In **PowerShell terminal #1** (backend):

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY="PASTE_YOUR_KEY_LOCALLY_ONLY"
uvicorn main:app --reload --port 8000
```

In **PowerShell terminal #2** (frontend, from project root):

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173; API health http://localhost:8000/health. **Do not share your key** in a chat, screenshot, repository or issue.

### API smoke test before opening the UI

In the backend terminal after setting the key:

```powershell
python ..\scripts\check_gemma.py
```

`OK: ...` means the live model responded. `403`, `429`, or other errors mean check key restrictions, quota, tier, and model access. The script masks error details to avoid accidental secrets.

## How the actual pipeline works

1. User uploads photo (not uploaded to a public file server) and/or types a problem.
2. Browser posts the data URL to FastAPI backend `/api/analyze`.
3. Backend calls `gemma-4-26b-a4b-it` with image + instruction via Google Gemini API; Gemma returns a proposed JSON analysis.
4. Pydantic checks data types, length, exact number of choices; browser shows rankings and GO/REVIEW/NO-GO.
5. User chooses one idea; backend `/api/build` assembles a **template-backed** React project and a simple static HTML preview.
6. User downloads ZIP, runs `npm install` / `npm run build` for real compilation, then can publish it.

Note: Idea scores are model-proposed **feasibility estimates**, not live market research. The AI does not browse the web or run third-party competitive searches.

## Test and submit

```powershell
cd backend
python -m pytest -q
```

Screenshot the dashboard, analysis, app preview; record a demo with genuine Gemma output if service is available. Public GitHub repo should contain source, `LICENSE`, and README. DO not assert DO deployment if not performed.
