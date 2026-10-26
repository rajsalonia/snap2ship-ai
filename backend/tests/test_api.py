import base64
import io
import json
import zipfile

import pytest
from PIL import Image
from main import decode_image, provider_error


def image_data(format="PNG", mime="image/png"):
    output = io.BytesIO()
    Image.new("RGB", (16, 12), "green").save(output, format=format)
    return f"data:{mime};base64," + base64.b64encode(output.getvalue()).decode()


def test_health_is_not_live_model_verification(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model"] == "gemma-4-26b-a4b-it"
    assert response.json()["key_configured"] is False
    assert response.json()["live_model_verified"] is False


@pytest.mark.parametrize("payload,status", [({},400), ({"description":"  "},400), ({"description":"x"*2501},422), ({"description":"event","extra":"not allowed"},422)])
def test_invalid_input(client, payload, status):
    assert client.post("/api/analyze", json=payload).status_code == status


def test_missing_key_is_actionable(client):
    response = client.post("/api/analyze", json={"description":"Campus event"})
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_text_request_uses_configured_gemma(client, fake_model):
    response = client.post("/api/analyze", json={"description":"Build a campus event tracker"})
    assert response.status_code == 200
    assert len(response.json()["ideas"]) == 3
    assert fake_model[0]["model"] == "gemma-4-26b-a4b-it"
    assert "Build a campus event tracker" in fake_model[0]["contents"][-1]


@pytest.mark.parametrize("format,mime", [("PNG","image/png"),("JPEG","image/jpeg"),("WEBP","image/webp")])
def test_image_only_reaches_sdk_as_bytes(client, fake_model, format, mime):
    response = client.post("/api/analyze", json={"image_data_url":image_data(format,mime)})
    assert response.status_code == 200
    assert fake_model[0]["contents"][0].inline_data.mime_type == mime
    assert fake_model[0]["contents"][0].inline_data.data


@pytest.mark.parametrize("data", ["data:image/png;base64,YWJj", "data:image/gif;base64,YWJj", "data:image/png;base64,====", image_data("PNG","image/jpeg")])
def test_invalid_image_rejected_before_model(client, fake_model, data):
    response = client.post("/api/analyze", json={"image_data_url":data})
    assert response.status_code == 400
    assert fake_model == []


def test_oversized_image_rejected():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as error:
        decode_image("data:image/png;base64," + "A"*7_000_001)
    assert error.value.status_code == 413


def test_oversized_request_rejected(client):
    assert client.post("/api/analyze", content="{}", headers={"Content-Length":"8000001"}).status_code == 413


def test_sample_is_explicit_and_three_distinct_ideas(client):
    response = client.get("/api/sample").json()
    assert response["model_called"] is False
    assert response["provenance"] == "curated_sample"
    ideas = response["analysis"]["ideas"]
    assert len({idea["title"] for idea in ideas}) == 3
    assert {idea["template"] for idea in ideas} == {"event","checklist","info"}


def test_build_returns_source_zip_and_honest_unverified_result(client, analysis):
    response = client.post("/api/build", json={"analysis":analysis,"idea":analysis["ideas"][0]})
    assert response.status_code == 200
    payload = response.json()
    assert payload["sample"] is True
    assert payload["validation"]["production_build_passed"] is False
    assert payload["validation"]["production_build_executed"] is False
    assert payload["preview_kind"] == "static_fallback"
    archive = zipfile.ZipFile(io.BytesIO(base64.b64decode(payload["zip_base64"])))
    assert {"src/App.jsx","src/content.json","package-lock.json","BUILD-REPORT.json","LICENSE","README.md"} <= set(archive.namelist())
    assert json.loads(archive.read("BUILD-REPORT.json"))["status"] == "unverified"
    assert json.loads(archive.read("src/content.json"))["sample"] is True


def test_build_rejects_tampered_idea_even_with_same_title(client, analysis):
    tampered = {**analysis["ideas"][0], "pitch":"A changed proposal that was not selected"}
    assert client.post("/api/build", json={"analysis":analysis,"idea":tampered}).status_code == 400


@pytest.mark.parametrize("code,status,needle", [(403,502,"access denied"),(404,502,"not found"),(429,429,"quota"),(503,503,"unavailable")])
def test_provider_errors_explained_without_leaking_secrets(code, status, needle):
    error = type("ProviderFailure",(Exception,),{"code":code})("secret-upstream-message")
    mapped = provider_error(error)
    assert mapped.status_code == status
    assert needle in mapped.detail.lower()
    assert "secret-upstream-message" not in mapped.detail


def test_timeout_is_actionable():
    assert provider_error(TimeoutError("private error")).status_code == 504


def test_cors_allows_local_frontend_and_rejects_other_origin(client):
    headers = {"Origin":"http://127.0.0.1:5173","Access-Control-Request-Method":"POST","Access-Control-Request-Headers":"Content-Type"}
    assert client.options("/api/build",headers=headers).headers["access-control-allow-origin"] == headers["Origin"]
    headers["Origin"] = "https://unrelated.invalid"
    assert client.options("/api/build",headers=headers).status_code == 400


def test_validation_error_omits_submitted_private_data(client):
    response = client.post("/api/analyze",json={"description":"sensitive-source"*300})
    assert response.status_code == 422
    assert "sensitive-source" not in response.text


def test_rate_limit(client):
    for _ in range(6):
        assert client.post("/api/analyze",json={}).status_code == 400
    response = client.post("/api/analyze",json={})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "60"


def test_production_frontend_served_without_shadowing_api(client):
    from main import frontend_dist
    if not frontend_dist.is_dir():
        pytest.skip("Frontend dist is verified in the frontend/Docker build")
    response = client.get("/")
    assert response.status_code == 200
    assert "Snap2Ship AI" in response.text
    assert client.get("/health").json()["ok"] is True
    assert client.get("/api/sample").json()["model_called"] is False


def test_ai_capacity_guard_returns_actionable_retry_without_calling_provider(client, fake_model, monkeypatch):
    import main

    class BusySlots:
        def acquire(self, blocking=False):
            return False

        def release(self):
            raise AssertionError("Unacquired capacity must never be released")

    monkeypatch.setattr(main, "MODEL_SLOTS", BusySlots())
    response = client.post("/api/analyze", json={"description": "A college poster needs an event tracker"})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "10"
    assert "busy" in response.json()["detail"].lower()
    assert fake_model == []


def test_model_capacity_is_released_after_success(client, fake_model, monkeypatch):
    import main

    class TrackingSlots:
        acquired = 0
        released = 0

        def acquire(self, blocking=False):
            self.acquired += 1
            return True

        def release(self):
            self.released += 1

    slots = TrackingSlots()
    monkeypatch.setattr(main, "MODEL_SLOTS", slots)
    response = client.post("/api/analyze", json={"description": "Create an event tracker"})
    assert response.status_code == 200
    assert slots.acquired == slots.released == 1
