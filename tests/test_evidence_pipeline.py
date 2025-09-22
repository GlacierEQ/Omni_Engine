from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from modules.evidence_pipeline.main import (
    GlacierEQFileBossInterface,
    MegaPDFLegalAnalyzer,
    MemoryLayerCompiler,
    WhisperXEvidenceProcessor,
)


def test_fileboss_interface():
    iface = GlacierEQFileBossInterface()
    result = iface.quantum_file_processing()
    assert result["glacier_storage"].startswith("Deep archive")


def test_mega_pdf_analyzer(tmp_path):
    pdf = tmp_path / "doc.pdf"
    pdf.write_text("dummy")
    analyzer = MegaPDFLegalAnalyzer()
    output = analyzer.analyze_legal_pdfs(pdf)
    assert "court_documents" in output


def test_whisperx_processor(tmp_path):
    audio = tmp_path / "audio.mp3"
    audio.write_text("data")
    processor = WhisperXEvidenceProcessor()
    summary = processor.transcribe_evidence_audio([audio])
    assert "call_recordings" in summary


def test_memory_layer_compiler():
    compiler = MemoryLayerCompiler()
    status = compiler.verify_memory_connections()
    assert status["status"] == "FULLY_CONNECTED"
