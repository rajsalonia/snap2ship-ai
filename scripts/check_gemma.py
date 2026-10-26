"""Live Gemma tests. Loads keys locally and never prints them."""
import argparse
import base64
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from main import AnalyzeRequest, analyze, provider_error
from dotenv import load_dotenv
load_dotenv(ROOT / "backend/.env", override=False)
parser = argparse.ArgumentParser(description="Check genuine Gemma access without exposing keys.")
parser.add_argument("--all", action="store_true", help="Check text, structured analysis and a fictional poster image")
args = parser.parse_args()

if not os.getenv("GEMINI_API_KEY"):
    print("NOT RUN: GEMINI_API_KEY is not configured in backend/.env or the environment.")
    raise SystemExit(2)
try:
    from google import genai
    from google.genai import types
    model = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")
    with genai.Client(api_key=os.environ["GEMINI_API_KEY"], http_options=types.HttpOptions(timeout=90_000)) as client:
        response = client.models.generate_content(model=model, contents="Reply with: Snap2Ship connection works",
            config=types.GenerateContentConfig(max_output_tokens=100))
    if not (response.text or "").strip():
        raise RuntimeError("Empty provider response")
    print(f"PASS: genuine text response from {model}.")
    if args.all:
        result = analyze(AnalyzeRequest(description="Students need a preparation task list for a college design event."))
        print(f"PASS: text analysis validated exactly {len(result.ideas)} distinct ideas.")
        data = base64.b64encode((ROOT / "examples/sample-poster.png").read_bytes()).decode()
        result = analyze(AnalyzeRequest(description="Suggest student micro-apps from this fictional event poster.",
            image_data_url="data:image/png;base64," + data))
        print(f"PASS: genuine image-plus-text analysis validated {len(result.ideas)} distinct ideas.")
except Exception as error:
    from fastapi import HTTPException
    mapped = error if isinstance(error, HTTPException) else provider_error(error)
    print(f"FAIL: HTTP {mapped.status_code}: {mapped.detail}")
    raise SystemExit(1)
