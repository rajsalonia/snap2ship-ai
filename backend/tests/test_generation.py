import json
import zipfile
import io
from main import Analysis, Idea, generated_files, html_preview, parse_analysis

def test_generator_and_escaping():
    idea = Idea(title="Campus Tracker", pitch="Track college events", audience="Students", template="event", verdict="GO",score=95,reason="Simple",features=["Tasks"])
    analysis = Analysis(source_summary="Test event poster", problem="Missed events", facts=["Event on 15 November", '<script>alert(1)</script>'],actions=["Register"],ideas=[idea,idea,idea],confidence_note="Verify dates")
    files=generated_files(analysis, idea)
    assert "src/App.jsx" in files
    assert json.loads(files['src/content.json'])['title']=='Campus Tracker'
    preview=html_preview(analysis,idea)
    assert '&lt;script&gt;' in preview
    assert '<script>alert(1)</script>' not in preview

def test_model_schema_parse():
    idea={"title":"Campus Tracker","pitch":"Track college events","audience":"Students","template":"event","verdict":"GO","score":95,"reason":"Simple","features":["Tasks"]}
    data={"source_summary":"Event poster","problem":"Missed events","facts":[],"actions":[],"confidence_note":"Verify","ideas":[idea,idea,idea]}
    assert len(parse_analysis('```json\n'+json.dumps(data)+'\n```').ideas)==3
