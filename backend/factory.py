"""Compile only repository-owned templates, with bounded JSON content."""
from __future__ import annotations

import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import time

from models import Analysis, Idea

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "template-runtime"
TEMPLATES = ROOT / "templates"
BUILD_LOCK = threading.Lock()


def compiler_available() -> bool:
    return bool(shutil.which("npm") and (RUNTIME / "node_modules/vite/bin/vite.js").is_file())


def generated_files(analysis: Analysis, idea: Idea, *, sample: bool = False) -> dict[str, bytes]:
    spec = idea.spec
    content = {
        "id": hashlib.sha256((analysis.model_dump_json() + idea.title).encode()).hexdigest()[:16],
        "title": idea.title, "tagline": idea.pitch, "audience": idea.audience,
        "type": idea.template, "features": idea.features, "facts": analysis.facts,
        "tasks": spec.tasks or analysis.actions,
        "events": [event.model_dump() for event in spec.events],
        "sections": [section.model_dump() for section in spec.sections],
        "verification": analysis.confidence_note, "sample": sample,
    }
    if idea.template == "event" and not content["events"]:
        content["events"] = [{"title": idea.title, "when": "Date not provided", "location": "Location not provided", "detail": analysis.source_summary}]
    if idea.template == "info" and not content["sections"]:
        content["sections"] = [{"heading": "About", "body": analysis.source_summary}, {"heading": "Source details", "body": "\n".join(analysis.facts) or "Verify details against the source."}]
    files = {
        "package.json": (RUNTIME / "package.json").read_text(encoding="utf-8"),
        "index.html": '<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="theme-color" content="#254e40"><title>' + html.escape(idea.title) + '</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>',
        "src/main.jsx": "import React from 'react';import{createRoot}from'react-dom/client';import App from './App.jsx';createRoot(document.getElementById('root')).render(<App/>);",
        "src/App.jsx": (TEMPLATES / "App.jsx").read_text(encoding="utf-8"),
        "src/style.css": (TEMPLATES / "style.css").read_text(encoding="utf-8"),
        "src/content.json": json.dumps(content, ensure_ascii=False, indent=2),
        "README.md": f"# {idea.title}\n\n{idea.pitch}\n\nA React/Vite application assembled by Snap2Ship AI from a trusted template and structured content. Review all extracted facts.\n\n## Run\n\nNode.js 22+ recommended.\n\n```sh\nnpm ci\nnpm run dev\n```\n\n## Production\n\n```sh\nnpm run build\nnpm run preview\n```\n\nDeploy `dist/` to any static host. The ZIP contains `BUILD-REPORT.json` with the actual compiler result from generation. Successful compilation is not a guarantee of factual accuracy or exhaustive runtime testing.\n\n## Interactions\n\nEvents: search, save, filter saved events, action checklist. Checklist: add, complete, delete, filter tasks and progress. Information: search, expandable sections, navigation. State persists in the browser when localStorage is available. Sandboxed previews keep session-only state.\n\n## Content\n\nEdit `src/content.json`. No API key, database, or backend is needed by this generated application.\n\n## Provenance\n\n{'Fictional curated sample; no live model call was used.' if sample else 'Content supplied through Snap2Ship; check the originating analysis and source.'}\n\n## License\n\nMIT.\n",
        "LICENSE": (ROOT.parent / "LICENSE").read_text(encoding="utf-8"),
        ".gitignore": "node_modules/\ndist/\n.env*\n",
    }
    lock = RUNTIME / "package-lock.json"
    if lock.is_file():
        files["package-lock.json"] = lock.read_text(encoding="utf-8")
    return {name: value.encode("utf-8") for name, value in files.items()}


def html_preview(analysis: Analysis, idea: Idea) -> str:
    """A labelled fallback only; successful builds preview the compiled React app."""
    facts = "".join(f"<li>{html.escape(fact)}</li>" for fact in analysis.facts)
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{font:16px system-ui;background:#f4f4eb;color:#254e40;padding:28px}}h1{{font-size:36px}}li{{margin:16px 0}}</style><body><p>STATIC FALLBACK · REACT COMPILATION NOT VERIFIED</p><h1>{html.escape(idea.title)}</h1><p>{html.escape(idea.pitch)}</p><ul>{facts}</ul><p>{html.escape(analysis.confidence_note)}</p></body></html>'


def inline_preview(dist: Path) -> str:
    document = (dist / "index.html").read_text(encoding="utf-8")
    def asset(name: str) -> str:
        path = (dist / name.removeprefix("./").lstrip("/")).resolve()
        if not path.is_relative_to(dist.resolve()) or not path.is_file():
            raise ValueError("Missing or invalid build asset")
        return path.read_text(encoding="utf-8")
    def script(match):
        # Remove the module-preload polyfill's external requests; all assets are inline.
        code = re.sub(r"</script", lambda _: "<\\/script", asset(match.group(1)), flags=re.IGNORECASE)
        return f'<script type="module">{code}</script>'
    document = re.sub(r'<script\b[^>]*\bsrc="([^"]+)"[^>]*></script>', script, document)
    document = re.sub(r'<link\b[^>]*href="([^"]+\.css)"[^>]*>', lambda match: '<style>' + asset(match.group(1)) + '</style>', document)
    # The iframe also uses sandbox=allow-scripts without allow-same-origin.
    policy = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; font-src 'none'; form-action 'none'; base-uri 'none'"
    return document.replace("<head>", f'<head><meta http-equiv="Content-Security-Policy" content="{policy}">', 1)


def compile_project(files: dict[str, bytes]) -> tuple[dict, str | None]:
    result = {"status": "unverified", "production_build_executed": False, "production_build_passed": False,
              "template_files_present": all(name in files for name in ("index.html", "src/App.jsx", "src/content.json", "package.json")),
              "specification_schema_validated": True, "logs": [], "output_files": [], "duration_seconds": 0}
    if os.getenv("BUILD_VALIDATION", "true").lower() != "true" or not compiler_available():
        result["logs"] = ["Compilation unavailable. Install Node.js and run npm ci in backend/template-runtime, then restart the API. Source generation succeeded; no successful production build is claimed."]
        return result, None
    if not BUILD_LOCK.acquire(blocking=False):
        result["logs"] = ["Compiler busy with another build. Retry to obtain compilation verification."]
        return result, None
    started = time.monotonic()
    try:
        work_root = RUNTIME / ".work"
        work_root.mkdir(exist_ok=True)
        # Ancestor node_modules are resolved by npm/Vite; dependencies were installed
        # once from the committed lockfile, never from model-supplied package data.
        with tempfile.TemporaryDirectory(prefix="build-", dir=work_root) as folder:
            workspace = Path(folder)
            for name, data in files.items():
                target = workspace / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            safe_env = {key: value for key, value in os.environ.items() if key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA"}}
            safe_env.update({"NO_COLOR": "1", "CI": "true", "npm_config_offline": "true"})
            result["production_build_executed"] = True
            process = subprocess.run([shutil.which("npm"), "run", "build"], cwd=workspace,
                                     capture_output=True, text=True, encoding="utf-8", errors="replace",
                                     timeout=60, shell=os.name == "nt", env=safe_env)
            log = (process.stdout + "\n" + process.stderr).replace(str(workspace), "<build-workspace>")
            result["logs"] = [line for line in log.splitlines() if line.strip()][-70:]
            result["exit_code"] = process.returncode
            dist = workspace / "dist"
            if process.returncode != 0:
                result["status"] = "failed"
                return result, None
            result["output_files"] = [str(path.relative_to(dist)).replace("\\", "/") for path in dist.rglob("*") if path.is_file()]
            if "index.html" not in result["output_files"] or not any(name.endswith(".js") for name in result["output_files"]):
                result["status"] = "failed"
                result["logs"].append("Required production HTML/JavaScript output missing.")
                return result, None
            preview = inline_preview(dist)
            result.update(status="passed", production_build_passed=True)
            result["logs"].append("Verified dist/index.html, bundled JavaScript and stylesheet; assembled sandboxed React preview.")
            return result, preview
    except subprocess.TimeoutExpired:
        result.update(status="failed", logs=["Production compilation exceeded the 60-second limit."])
        return result, None
    except (OSError, ValueError) as error:
        result.update(status="failed" if result["production_build_executed"] else "unverified",
                      logs=[f"Compiler could not complete ({type(error).__name__}). Check Node.js and build workspace permissions."])
        return result, None
    finally:
        result["duration_seconds"] = round(time.monotonic() - started, 2)
        BUILD_LOCK.release()
