from __future__ import annotations

import json
from pathlib import Path

try:  # pragma: no cover - optional dependency
    import fitz
except ModuleNotFoundError:  # pragma: no cover - executed when PyMuPDF missing
    fitz = None

from modules.connectors import FileBossConnector, MegaPdfConnector, WhisperXConnector
from modules.operator import OperatorCore


def _create_pdf(path: Path, text: str) -> None:
    if fitz is None:
        path.write_bytes(b"")
        return
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def test_operator_cycle_ingests_resources(tmp_path):
    file_root = tmp_path / "files"
    file_root.mkdir()
    (file_root / "evidence.txt").write_text("Evidence contents")

    pdf_root = tmp_path / "pdfs"
    pdf_root.mkdir()
    _create_pdf(pdf_root / "case.pdf", "Legal clause analysis")

    transcripts_root = tmp_path / "transcripts"
    transcripts_root.mkdir()
    (transcripts_root / "call.json").write_text(
        json.dumps(
            {
                "segments": [
                    {
                        "speaker": "Teresa",
                        "text": "We need to discuss the custody plan.",
                        "start": 0.0,
                        "end": 12.5,
                    }
                ]
            }
        )
    )

    operator = OperatorCore(
        connectors=[
            FileBossConnector(name="FILES", root=file_root),
            MegaPdfConnector(
                name="PDFS",
                documents_root=pdf_root,
                max_pages=1,
                characters_per_page=80,
            ),
            WhisperXConnector(name="AUDIO", transcripts_root=transcripts_root),
        ]
    )

    report = operator.run_cycle()
    assert {audit.name for audit in report.connectors} == {"FILES", "PDFS", "AUDIO"}
    snapshot = operator.layer_snapshot()
    assert snapshot["legal_evidence"]
    if fitz is not None:
        assert snapshot["document_insights"]
    else:
        assert any(
            "PyMuPDF" in entry.content for entry in snapshot.get("ingestion_alerts", [])
        )
    assert snapshot["audio_transcripts"]
    recommendations = operator.generate_recommendations(report)
    if fitz is None:
        assert any("PDF" in rec or "PyMuPDF" in rec for rec in recommendations)
    else:
        assert not recommendations[0].startswith("Connector")


def test_whisperx_connector_handles_invalid_json(tmp_path):
    transcripts_root = tmp_path / "transcripts"
    transcripts_root.mkdir()
    (transcripts_root / "broken.json").write_text("not json")

    connector = WhisperXConnector(name="AUDIO", transcripts_root=transcripts_root)
    entries = list(connector.gather())
    assert any(entry.layer == "ingestion_alerts" for entry in entries)
