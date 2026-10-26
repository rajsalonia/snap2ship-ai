# Deploy Snap2Ship on DigitalOcean App Platform

**Status: the free static frontend is prepared and awaiting owner account verification.** Its wizard confirmed $0/month. No DigitalOcean deployment or Gradient AI integration is claimed. The complete working demo is already verified on [free Render](https://snap2ship-ai-api.onrender.com/).

## Authorized free route

Use the [free static-site deployment](https://cloud.digitalocean.com/apps/new?repo=https://github.com/rajsalonia/snap2ship-ai/tree/digitalocean-free-20261026). That branch has a static-only `.do/app.yaml` and deployment template: build `frontend` with `npm ci --ignore-scripts --no-audit --no-fund && npm run build`, publish `dist`, and set `VITE_API_URL=https://snap2ship-ai-api.onrender.com` at build time. No web-service component is selected.

The wizard requires owner payment-method/account verification even though its selected site costs $0/month. Only the owner can complete that step. After creation, add the site's exact HTTPS origin to the Render API's `ALLOWED_ORIGINS`, redeploy the API and verify the actual frontend-to-API sample/build flow before claiming DigitalOcean hosting.

The remaining Docker instructions describe the original paid option. It was not activated and is not the authorized free deployment.

## Deployment shape

One Docker-based web service serves both the compiled React dashboard and the FastAPI API under the same URL. The image includes Python and Node.js so generated projects can undergo genuine compilation after deployment. It creates no database, disk, GPU or additional paid service.

The reviewed configuration is `.do/app.yaml`: Bangalore region, one `apps-s-1vcpu-0.5gb` instance, port 10000, `/health`, and preserved path prefixes. The dashboard is built with `VITE_API_URL=/`, so `/health` and `/api/*` use the same origin. `ALLOWED_ORIGINS` is bound to `${APP_URL}`.

DigitalOcean listed this instance at $5/month on 26 October 2026, billed by usage. Confirm the actual creation-screen cost and available promotional credits first. No paid resource or prepayment is authorized solely by this file.

## Before creating the app

1. Verify the source and passing checks at https://github.com/rajsalonia/snap2ship-ai.
2. Sign in at https://cloud.digitalocean.com and inspect Billing/Credits.
3. Confirm that credits apply to App Platform and cover the selected service, or explicitly approve its cost.
4. Confirm the account and project destination. Do not add a database or choose a larger instance automatically.

## Control panel

Use [Prepare a DigitalOcean deployment](https://cloud.digitalocean.com/apps/new?repo=https://github.com/rajsalonia/snap2ship-ai/tree/main). It reads `.do/deploy.template.yaml` from the public repository and avoids granting the GitHub app access to your repositories. Build from the repository root with `Dockerfile`. The equivalent ordinary app specification is `.do/app.yaml`.

Keep one web service. The frontend is already built into this container, so a separate frontend component is unnecessary. Review the final cost before creation.

### Secrets

Configure `GEMINI_API_KEY` as an encrypted, runtime-only environment variable when a usable Google AI Studio key is available. It is deliberately absent from the committed specification. Do not enter it into build arguments, frontend variables, the repository, chat, screenshots or logs.

Without the key, the public app can still demonstrate the clearly labelled sample, genuine template compilation, preview and ZIP export. Live analysis returns an actionable unavailable response. Do not describe that as verified Gemma access.

`GEMMA_MODEL=gemma-4-26b-a4b-it` and `BUILD_VALIDATION=true` are non-secret runtime settings.

## Verify the actual deployment

Wait for DigitalOcean to report an active deployment; an accepted creation request is insufficient. Record the deployed source commit and public URL, then check:

- Public dashboard loads and has no browser console errors.
- `/health` returns HTTP 200 and `compiler_available: true`.
- The frontend's `/api/sample` request reaches this backend.
- All three sample cards render with the sample disclosure.
- Building an idea returns `production_build_passed: true` and actual compiler logs.
- The compiled React preview renders and its interactions work.
- The source ZIP contains the source, lockfile and truthful `BUILD-REPORT.json`.
- With a usable key, test genuine text and image analysis before claiming model access.

Only then replace the prepared-status wording in README, verification and submission documents with actual deployment evidence. Hosting on App Platform does not imply DigitalOcean runs the Gemma model or uses Gradient AI.

## CLI alternative

After securely authenticating doctl and confirming account credits/cost:

```sh
doctl apps spec validate .do/app.yaml
doctl apps create --spec .do/app.yaml
```

Creation can incur charges. Do not run it without the required credit/cost verification. Keep tokens out of command-line arguments and committed files.

References: [App specification](https://docs.digitalocean.com/products/app-platform/reference/app-spec/), [Dockerfile builds](https://docs.digitalocean.com/products/app-platform/reference/dockerfile/), [Environment variables](https://docs.digitalocean.com/products/app-platform/how-to/use-environment-variables/), [Pricing](https://docs.digitalocean.com/products/app-platform/details/pricing/).

The public-repository template was successfully imported into DigitalOcean's creation wizard with the expected Docker service, region, port and $5/month estimate. The wizard requires account billing activation. The owner declined paid-service activation, so no App Platform web service was created. Account-specific billing details are excluded from these submission materials.
