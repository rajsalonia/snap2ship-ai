import json
import subprocess
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
import factory
from main import Analysis, generated_files, html_preview, parse_analysis, sample_analysis


def test_model_schema_parses_json_and_fences(analysis):
    assert len(parse_analysis(json.dumps(analysis)).ideas) == 3
    fence = chr(96)*3
    assert len(parse_analysis(fence+"json\n"+json.dumps(analysis)+"\n"+fence).ideas) == 3


@pytest.mark.parametrize("text", ["not JSON", "{}", "", '{"ideas": []}'])
def test_bad_model_output_is_not_returned_as_success(text):
    with pytest.raises(HTTPException) as error:
        parse_analysis(text)
    assert error.value.status_code == 502


def test_exactly_three_distinct_ideas_required(analysis):
    analysis["ideas"][1] = analysis["ideas"][0]
    with pytest.raises(ValidationError):
        Analysis.model_validate(analysis)


def test_rubric_score_is_computed_and_sorted(analysis):
    analysis["ideas"][0]["score"] = 1
    validated = Analysis.model_validate(analysis)
    assert validated.ideas[0].score == 94
    assert validated.ideas[0].verdict == "GO"


def test_source_data_never_becomes_executable_template_code(analysis):
    analysis["facts"] = ['<img src=x onerror=alert(1)>', '</ScRiPt><script>alert(1)</script>']
    validated = Analysis.model_validate(analysis)
    files = generated_files(validated, validated.ideas[0])
    assert b"onerror=alert" not in files["src/App.jsx"]
    assert json.loads(files["src/content.json"])["facts"] == analysis["facts"]
    preview = html_preview(validated,validated.ideas[0])
    assert "<script>alert(1)" not in preview
    assert "&lt;img" in preview


def test_all_template_specs_are_in_export():
    analysis = sample_analysis()
    for idea in analysis.ideas:
        files = generated_files(analysis,idea)
        content = json.loads(files["src/content.json"])
        assert content["type"] == idea.template
        if idea.template == "event":
            assert len(content["events"]) == 3
        elif idea.template == "checklist":
            assert content["tasks"]
        else:
            assert content["sections"]


def test_no_compiler_is_explicitly_unverified(monkeypatch):
    monkeypatch.setenv("BUILD_VALIDATION","true")
    monkeypatch.setattr(factory,"compiler_available",lambda:False)
    analysis = sample_analysis()
    result,preview = factory.compile_project(generated_files(analysis,analysis.ideas[0]))
    assert result["status"] == "unverified"
    assert preview is None


def test_failed_compiler_is_never_marked_passed(monkeypatch):
    monkeypatch.setenv("BUILD_VALIDATION","true")
    monkeypatch.setenv("GEMINI_API_KEY","private-test-secret")
    monkeypatch.setattr(factory,"compiler_available",lambda:True)
    def fail(*args,**kwargs):
        assert "GEMINI_API_KEY" not in kwargs["env"]
        return SimpleNamespace(stdout="Syntax failure",stderr="compiler error",returncode=1)
    monkeypatch.setattr(factory.subprocess,"run",fail)
    analysis = sample_analysis()
    result,preview = factory.compile_project(generated_files(analysis,analysis.ideas[0]))
    assert result["status"] == "failed"
    assert result["production_build_executed"] is True
    assert result["production_build_passed"] is False
    assert "compiler error" in result["logs"]
    assert preview is None


def test_missing_build_output_is_failure(monkeypatch):
    monkeypatch.setenv("BUILD_VALIDATION","true")
    monkeypatch.setattr(factory,"compiler_available",lambda:True)
    monkeypatch.setattr(factory.subprocess,"run",lambda *args,**kwargs: SimpleNamespace(stdout="done",stderr="",returncode=0))
    analysis = sample_analysis()
    result,preview = factory.compile_project(generated_files(analysis,analysis.ideas[0]))
    assert result["status"] == "failed"
    assert result["production_build_passed"] is False


def test_timeout_reports_failure(monkeypatch):
    monkeypatch.setenv("BUILD_VALIDATION","true")
    monkeypatch.setattr(factory,"compiler_available",lambda:True)
    def timeout(*args,**kwargs):
        raise subprocess.TimeoutExpired("npm",60)
    monkeypatch.setattr(factory.subprocess,"run",timeout)
    analysis = sample_analysis()
    result,preview = factory.compile_project(generated_files(analysis,analysis.ideas[0]))
    assert result["status"] == "failed"
    assert "60-second" in result["logs"][0]


def test_inline_preview_escapes_mixed_case_script_closing(tmp_path):
    (tmp_path/"index.html").write_text('<html><head><script type="module" src="./app.js"></script></head><body></body></html>')
    (tmp_path/"app.js").write_text('const source="</ScRiPt><script>alert(1)</script>";')
    preview = factory.inline_preview(tmp_path)
    assert "</ScRiPt>" not in preview
    assert "<\\/script>" in preview
    assert "connect-src 'none'" in preview
