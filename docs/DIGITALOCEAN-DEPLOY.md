# DigitalOcean + Gemma 4 — exact responsibilities

- **Google AI Studio** supplies the `GEMINI_API_KEY` for `gemma-4-26b-a4b-it` through the **Gemini Developer API**. Your Python server makes AI requests. Do not select Google Cloud Agent Studio to obtain a key for this MVP.
- **DigitalOcean App Platform** hosts the application at a shareable URL. It can host the FastAPI API as a **Web Service** and React frontend as a **Static Site**. DigitalOcean DOES NOT run Gemma in the basic plan: the deployed backend still calls Google's hosted Gemma API.
- The **GitHub** repository is the single source for both deployable components (`frontend/` and `backend/`). This is called a monorepo.

**Prerequisites:** GitHub public repo `rajsalonia/snap2ship-ai` with this code committed; Google AI Studio API key set privately; a DigitalOcean account with billing/credits verified. Creating DO services may incur charges; credits are not guaranteed, and auto-deploys can increase usage. Do not provision a GPU Droplet, database, or dedicated inference service for this MVP.

## Step 1. Push repo

Create public repo https://github.com/new as `snap2ship-ai` (avoid unnecessary extra files from GitHub UI). From extracted project root:

```powershell
git init
git add .
git commit -m "feat: initial Snap2Ship AI MVP"
git branch -M main
git remote add origin https://github.com/rajsalonia/snap2ship-ai.git
git push -u origin main
```

Your .gitignore excludes secrets, `.venv/`, `node_modules/`, and build artifacts. Verify that no API key is committed.

## Step 2. Deploy FastAPI web service on DO App Platform

Visit https://cloud.digitalocean.com/apps and choose **Create App** → GitHub → `rajsalonia/snap2ship-ai` → `main`.

Set **Source directory** = `backend` (may appear as `/backend`). Set type **Web Service**, build command `pip install -r requirements.txt`, run command `uvicorn main:app --host 0.0.0.0 --port $PORT` and HTTP port selected for your service (the platform supplies `PORT`).

Environment variables in **Web Service**:
- `GEMINI_API_KEY`: your Google AI Studio API key, value **encrypted/secret**, runtime only.
- `GEMMA_MODEL`: `gemma-4-26b-a4b-it`
- `ALLOWED_ORIGINS`: `https://YOUR-FRONTEND-DOMAIN.ondigitalocean.app` (update after frontend creation; exact origin, no trailing slash).

Review instance costs and confirm credits/billing before creation. After deploy, test `https://YOUR-BACKEND-HOST/health`. It should return `{ "ok": true, "model": "gemma-4-26b-a4b-it", "key_configured": true }`. This does NOT verify actual model access; use the UI to make a real test call.

## Step 3. Deploy React static site on DO App Platform

In the same app choose **Add component → Static Site**, GitHub source and branch as above, **Source directory** `frontend` (or `/frontend`), **Build command** `npm install && npm run build`, **Output directory** `dist`.

Frontend build-time environment variable:
- `VITE_API_URL`: exact backend public URL (e.g. `https://example.ondigitalocean.app`, without `/api` suffix and trailing slash). This value is PUBLIC and safe; do NOT put your Google API key here.

On frontend URL run upload → real Gemma analysis → select idea → build → preview → download. If CORS error, fix `ALLOWED_ORIGINS` on backend to the exact browser origin; redeploy backend. If app and API are served under a shared host with subpaths, adjust routing/`VITE_API_URL` accordingly.

## Step 4. Verify and document

- Test real image + text with Gemma 4, not just mock data.
- Download an output project and run `npm install && npm run build` locally before claiming it compiles.
- Add frontend live URL + backend health URL + screenshots + README tech explanation to Devpost / MLH submission.
- If DO App Platform is unavailable, put static frontend on Vercel and backend on Render. Still don't claim DO sponsor integration.

Docs: https://docs.digitalocean.com/products/app-platform/how-to/deploy-from-monorepo/ ; https://docs.digitalocean.com/products/app-platform/how-to/create-apps/ ; https://docs.digitalocean.com/products/app-platform/how-to/use-environment-variables/
