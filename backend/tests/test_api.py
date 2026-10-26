import base64
import io
import json
import sys
import types
import zipfile
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

IDEA = {"title":"Campus Event Tracker","pitch":"Track a campus festival and its registration tasks",
        "audience":"Students","template":"event","verdict":"GO","score":94,
        "reason":"Fits a supported template","features":["Dates","Checklist"]}
ANALYSIS = {"source_summary":"Fictional campus poster","problem":"Students miss deadlines",
            "facts":["Registration closes 10 November 2026"],"actions":["Bring student ID"],
            "ideas":[IDEA, IDEA, IDEA],"confidence_note":"Verify the printed date"}

def test_health():
    result = client.get('/health')
    assert result.status_code == 200
    assert result.json()['model'] == 'gemma-4-26b-a4b-it'

def test_no_input():
    response = client.post('/api/analyze',json={"description":"","image_data_url":None})
    assert response.status_code == 400

def test_no_key_fails_cleanly(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    response = client.post('/api/analyze',json={"description":"Campus event"})
    assert response.status_code == 503
    assert 'GEMINI_API_KEY' in response.json()['detail']

def test_valid_text_uses_model_and_parses(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY','fake-local-test-value')
    calls=[]
    class FakeModels:
        def generate_content(self, model, contents):
            calls.append((model,contents))
            return types.SimpleNamespace(text=json.dumps(ANALYSIS))
    class FakeClient:
        def __init__(self,api_key):
            assert api_key == 'fake-local-test-value'
            self.models=FakeModels()
    google=types.ModuleType('google')
    genai=types.ModuleType('google.genai')
    genai.Client=FakeClient
    gentypes=types.ModuleType('google.genai.types')
    genai.types=gentypes
    google.genai=genai
    monkeypatch.setitem(sys.modules,'google',google)
    monkeypatch.setitem(sys.modules,'google.genai',genai)
    monkeypatch.setitem(sys.modules,'google.genai.types',gentypes)
    response=client.post('/api/analyze',json={"description":"Make an app from a college event"})
    assert response.status_code==200
    assert len(response.json()['ideas'])==3
    assert calls[0][0]=='gemma-4-26b-a4b-it'

def test_build_returns_valid_zip():
    response=client.post('/api/build',json={"analysis":ANALYSIS,"idea":IDEA})
    assert response.status_code==200
    payload=response.json()
    assert payload['validation']['production_build_executed'] is False
    archive=zipfile.ZipFile(io.BytesIO(base64.b64decode(payload['zip_base64'])))
    names=set(archive.namelist())
    assert 'src/App.jsx' in names
    assert 'package.json' in names
    assert 'LICENSE' in names
    assert json.loads(archive.read('src/content.json'))['title']=='Campus Event Tracker'

def test_rejects_unknown_idea():
    unknown={**IDEA,"title":"Not one of the offered ideas"}
    response=client.post('/api/build',json={"analysis":ANALYSIS,"idea":unknown})
    assert response.status_code==400

def test_image_size_validation():
    # Fake huge data URL rejected before any upstream model call
    b64='A'*7_000_100
    from main import decode_image
    from fastapi import HTTPException
    try:
        decode_image('data:image/png;base64,'+b64)
        assert False,'Should reject oversize input'
    except HTTPException as error:
        assert error.status_code==413
