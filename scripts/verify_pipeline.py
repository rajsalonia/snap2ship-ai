"""Verify full pipeline: health -> sample/analysis -> build -> preview -> zip download."""
import io
import json
import urllib.request
import zipfile

base_url = "http://127.0.0.1:8000"

def main():
    print("1. Checking /health...")
    with urllib.request.urlopen(f"{base_url}/health") as res:
        health = json.loads(res.read())
    print("Health:", health)
    assert health["ok"] is True
    assert health["compiler_available"] is True

    print("\n2. Fetching /api/sample...")
    with urllib.request.urlopen(f"{base_url}/api/sample") as res:
        sample_data = json.loads(res.read())

    analysis = sample_data["analysis"]
    ideas = analysis["ideas"]
    print(f"Retrieved {len(ideas)} ideas:")
    for i, idea in enumerate(ideas):
        print(f"  Idea {i+1}: {idea['title']} ({idea['template']}) - score: {idea['score']}")

    assert len(ideas) == 3

    print("\n3. Testing build, preview, and ZIP for each idea...")
    for idea in ideas:
        payload = json.dumps({"analysis": analysis, "idea": idea}).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/api/build",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            build_res = json.loads(res.read())

        template = idea["template"]
        validation = build_res.get("validation", {})
        build_passed = validation.get("status") == "passed" and validation.get("production_build_passed") is True
        preview_kind = build_res.get("preview_kind")
        preview_html = build_res.get("preview_html", "")
        zip_base64 = build_res.get("zip_base64", "")
        filename = build_res.get("filename", "")

        print(f"Build [{template}]: passed={build_passed}, preview_kind={preview_kind}, preview_len={len(preview_html)}, filename={filename}")
        assert build_passed is True, f"Build failed for {template}: {validation}"
        assert preview_kind == "compiled_react", f"Expected compiled_react preview for {template}"
        assert len(preview_html) > 500, f"Preview too short for {template}"
        assert zip_base64, f"Missing zip_base64 for {template}"

        # Decode base64 ZIP
        import base64
        zip_bytes = base64.b64decode(zip_base64)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            namelist = zf.namelist()
            print(f"  Valid ZIP for [{template}]: {len(zip_bytes)} bytes, {len(namelist)} files")
            assert "package.json" in namelist
            assert "BUILD-REPORT.json" in namelist
            assert "src/App.jsx" in namelist
            report = json.loads(zf.read("BUILD-REPORT.json"))
            assert report["status"] == "passed"

    print("\nSUCCESS: All three templates successfully compiled, generated interactive preview HTML, and exported valid downloadable ZIPs!")

if __name__ == "__main__":
    main()
