# Model strategy and responsible fine-tuning plan

## Hackathon decision — 26 October 2026

**Use the hosted Google Gemma 4 model now; do not claim a custom-trained model.** Snap2Ship's multimodal vision and proposal-generation route uses the configured `gemma-4-26b-a4b-it` Gemini Developer API model. This is model integration, not model training.

Training or fine-tuning large models is a separate data-and-compute task. For today's hackathon, the reliable path is source-image reasoning, strong prompts, Pydantic validation, task-specific scoring, and test-backed templates. The model should not be described as tuned, trained on our data, or self-improving.

## Baseline evaluation before fine-tuning

Collect a small, permission-safe benchmark (e.g., 20–50 synthetic or consented examples):

| Category | Example source | What to verify |
| --- | --- | --- |
| Campus poster | Synthetic event JPEG with date, venue and contact | Does the model preserve exact dates and decline to invent missing links? |
| Revised notice | Two synthetic date-change images | Does it recognize differences without hallucinating requirements? |
| Handwritten task list | Consent-based or generated notes | Is the extracted checklist faithful and actionable? |
| Community request | Screenshot of a non-sensitive public problem statement | Is the chosen app template feasible in the supported feature set? |
| Ambiguous image | Deliberately blurry or cropped image | Does the system flag uncertainty instead of manufacturing facts? |

For each example, save input reference, expected factual fields, allowed template choices, model response, validation errors, human rating and inference latency. **Do not include secrets, personal IDs or private documents in the repository.**

Suggested metrics:
- Fact precision = supported extracted facts / all extracted facts.
- Required-field recall = correctly extracted mandatory fields / known mandatory fields.
- JSON schema pass rate and 3-idea completion rate.
- Hallucinated dates/links/fees (should be zero on synthetic tests).
- End-to-end successful app build rate (actual `npm run build`, not preview-only).
- User corrections and reviewer agreement.

## Optional future LoRA research

If baseline quality is insufficient *after* the hackathon:

1. Select a locally deployable Gemma variant that fits available GPU capacity and supports the desired image/text task. Do not assume that a hosted Gemini Developer API model can be modified by uploading arbitrary LoRA weights.
2. Build a licensed dataset with train/validation/test splits, reviewed by a human. Keep the evaluation set isolated from training.
3. Use an appropriate fine-tuning framework and, where supported, LoRA or another parameter-efficient method.
4. Evaluate against the untuned baseline on exactly the same held-out test data.
5. Release a reproducible training script, dataset provenance, cost notes and truthful model card **only if training actually succeeds**.
6. Respect Google Gemma model license and third-party dataset terms. Do not publish private images.

Official technical reference: https://gemma.ai/tuning/

## Infrastructure responsibilities

- **Gemma 4 via Gemini API:** Image/text reasoning and app specification; API key required in the backend only.
- **DigitalOcean:** Optional hosting and potentially inference for independently supported models; not needed to train Gemma 4. Verify credit balance, expiry and billing protections before creating resources.
- **GitHub:** Versioned source, reviews, tests, build artifacts and documentation.
- **Coding agents:** May edit, test and automate delivery; their own underlying models are separate from the deployed Gemma 4 inference model.

**Truthful status:** This document is a training/evaluation plan, not evidence that any fine-tune, GPU run, or live Gemma access has occurred.
