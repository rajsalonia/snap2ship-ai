# Deploy Snap2Ship on DigitalOcean App Platform

**Status: configuration prepared; account access, credits and public deployment remain to be verified.** This guide does not claim a live DigitalOcean or Gradient AI integration.

## Deployment shape

One Docker-based web service serves both the compiled React dashboard and the FastAPI API under the same URL. The image includes Python and Node.js so generated projects can undergo genuine compilation after deployment. It creates no database, disk, GPU or additional paid service.

The reviewed configuration is `.do/app.yaml`: Bangalore region, one `apps-s-1vcpu-0.5gb` instance, port 10000, `/health`, and preserved path prefixes. The dashboard is built with `VITE_API_URL=/`, so `/health` and `/api/*` use the same origin. `ALLOWED_ORIGINS` is bound to `${APP_URL}`.

An earlier preparation note estimated $5/month for this instance. That is **not an independently verified current quote or an account-specific projection**. Actual pricing, promotional credit amount, expiry, applicability and overage liability remain unknown in this cloud session. Confirm the final creation-screen quote, current usage, credit coverage and a reliable spending control before provisioning. Credits or billing alerts alone do not establish a hard spending cap. No paid resource or prepayment is authorized solely by this file.

## Before creating the app

1. Verify the source and passing checks at https://github.com/rajsalonia/snap2ship-ai.
2. Sign in at https://cloud.digitalocean.com and inspect Billing/Credits.
3. Confirm that credits apply to App Platform and cover the selected service, or explicitly approve its cost.
4. Confirm the account and project destination. Do not add a database or choose a larger instance automatically.

## Control panel

Open Apps → Create App and select the `rajsalonia/snap2ship-ai` GitHub repository, branch `main`. Build from the repository root with `Dockerfile`. If the UI supports importing/editing an app specification, use `.do/app.yaml`; otherwise reproduce its service, port, health check and ingress settings.

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
