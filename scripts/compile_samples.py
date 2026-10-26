"""Real compilation checks for all three templates; does not call Gemma."""
import base64
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from factory import compile_project, generated_files
from main import sample_analysis


def main():
    analysis = sample_analysis()
    results = []
    for idea in analysis.ideas:
        files = generated_files(analysis, idea, sample=True)
        result, preview = compile_project(files)
        results.append({"template": idea.template, **result})
        print(f"{idea.template}: {result['status']} ({result['duration_seconds']}s)")
        if result["status"] != "passed":
            print("\n".join(result["logs"]))
    report = ROOT / "docs/template-build-results.json"
    report.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if all(item["status"] == "passed" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
