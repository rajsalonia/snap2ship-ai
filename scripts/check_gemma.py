"""Live Gemma 4 smoke test. Never paste API keys into the script or terminal history files."""
import os
import sys

if not os.getenv("GEMINI_API_KEY"):
    print("ERROR: Set GEMINI_API_KEY in your local environment (never commit it).")
    raise SystemExit(2)
try:
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it"),
        contents="Reply with only this phrase: Snap2Ship Gemma connection works"
    )
    print("OK: live Gemma API replied:", (response.text or "(empty)")[:250])
except Exception as exc:
    print("ERROR: Live Gemma call failed. Check account tier, model access and usage quota. Error type:", type(exc).__name__)
    sys.exit(1)
