from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.integrations import Codex5ProClient
from modules.operator import OperatorCore


def test_codex5pro_strategy_detection():
    client = Codex5ProClient()
    strategy = client.generate_strategy("Custody timeline with financial and medical updates")
    assert "Family custody strategy" in strategy["focus_areas"]
    assert "Financial oversight" in strategy["focus_areas"]
    assert "Medical documentation review" in strategy["focus_areas"]
    assert strategy["model"] == "codex-5pro"


def test_operator_core_workflow(tmp_path):
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    (evidence_root / "note.txt").write_text("hello")

    pdf_path = tmp_path / "case.pdf"
    pdf_path.write_text("dummy")

    audio_path = tmp_path / "call.wav"
    audio_path.write_text("audio")

    operator = OperatorCore()

    plan = operator.audit_directory(evidence_root)
    assert str(evidence_root / "note.txt") in plan
    assert (evidence_root / "note.txt").exists()

    pdf_result = operator.analyze_pdf(pdf_path)
    assert "court_documents" in pdf_result

    audio_result = operator.transcribe_audio([audio_path])
    assert "call_recordings" in audio_result

    report = operator.build_system_report(
        evidence_directory=evidence_root,
        pdf_documents=[pdf_path],
        audio_evidence=[audio_path],
        context="Custody timeline",
    )
    assert report.directory_plan
    assert report.pdf_analyses[str(pdf_path)]["court_documents"].startswith("Extract")
    assert "glacier_storage" in report.fileboss_capabilities

    markdown = operator.render_report(report)
    assert markdown.startswith("# Omni Engine Operational Report")

    export_path = tmp_path / "report.md"
    operator.export_report(
        export_path,
        evidence_directory=evidence_root,
        pdf_documents=[pdf_path],
        audio_evidence=[audio_path],
        context="Custody timeline",
    )
    assert export_path.exists()
    assert export_path.read_text().startswith("# Omni Engine Operational Report")
