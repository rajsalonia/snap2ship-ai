import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture(autouse=True)
def isolated_requests(monkeypatch):
    main.REQUESTS.clear()
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("BUILD_VALIDATION", "false")


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture
def analysis():
    return main.sample_analysis().model_dump()


@pytest.fixture
def fake_model(monkeypatch, analysis):
    from google import genai
    calls = []
    class FakeClient:
        def __init__(self, **kwargs):
            self.models = self
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def generate_content(self, **kwargs):
            calls.append(kwargs)
            return type("Response", (), {"text": json.dumps(analysis)})()
    monkeypatch.setattr(genai, "Client", FakeClient)
    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key-not-a-credential")
    return calls
