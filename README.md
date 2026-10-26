**QUICK START:** Read [START HERE](docs/SETUP-START-HERE.md), [DIGITALOCEAN GUIDE](docs/DIGITALOCEAN-DEPLOY.md), and [SUBMISSION CHECKLIST](docs/SUBMISSION.md).

# Snap2Ship AI · Reality to Software

An open-source hackathon MVP: upload a real-world photo or describe a challenge; **Gemma 4** suggests three ranked micro-app ideas; choose one; preview and download a template-backed React/Vite project.

> **Current limitations:** No automatic GitHub push or DigitalOcean deployment. Template assembly is not a real npm production build; generated project must be tested with `npm run build` before deployment. Image extraction is AI-generated and can be wrong. Do not use sensitive images. The hosted model requires Google AI Studio access/quota.

## Fast setup (Windows PowerShell)

1. Generate a key at https://aistudio.google.com/apikey (never commit or paste this key).
2. Open PowerShell in `backend/`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY="YOUR_API_KEY"
uvicorn main:app --reload --port 8000
```

3. Open **another** PowerShell in `frontend/`:

```powershell
npm install
npm run dev
```

Visit http://localhost:5173. The API health endpoint is at http://localhost:8000/health.

## Demo

Upload a (non-sensitive) college-event notice and describe what you want. Select an idea with status GO and click **Build selected app**. Review its static HTML preview and download the React/Vite ZIP. Extract, run `npm install && npm run build` to validate its actual production compilation.

## Architecture

```text
React dashboard -> FastAPI /api/analyze -> Gemma 4 hosted model (image + text)
  -> Pydantic validation -> 3 idea cards -> /api/build
  -> Deterministic React template + content.json -> HTML preview + ZIP
```

## Environmental configuration

- Backend: `GEMINI_API_KEY` (required); `GEMMA_MODEL` (default `gemma-4-26b-a4b-it`); `ALLOWED_ORIGINS` (comma-separated exact URLs)
- Frontend: `VITE_API_URL` (must point to your deployed backend, or defaults to localhost)
- `.env.example` files show variable names. Never commit `.env` or API tokens.

## Deployment options

- Frontend: Vercel. Import repository, root directory `frontend`, build command `npm run build`, output `dist`, set `VITE_API_URL=https://YOUR_BACKEND_HOST`.
- Backend: Render Web Service. Import the same repository, root directory `backend`, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Add `GEMINI_API_KEY` and `ALLOWED_ORIGINS=https://YOUR_FRONTEND_HOST` in service environment variables.
- DigitalOcean App Platform can be explored once credits, product availability and configuration are confirmed. Don't claim sponsor integration without working end-to-end deployment.

## Security and correctness

Image size and MIME type are checked, AI output is schema validated, preview text is HTML escaped, arbitrary model-generated code is not executed by the backend, and uploaded images aren't intentionally stored on disk. Validation in `/api/build` is **structural only**, never presented as verified compilation. API keys stay backend-side.

## License

MIT. See LICENSE. Inspired by the general discover → rank → build → validate workflow of vibeDeploy, but uses visual physical-world input, narrowed template-backed generation, and a different educational/community-user focus. Not affiliated with vibeDeploy creators.
