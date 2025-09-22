"""Streamlit dashboard for the Omni Engine operator."""
from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable

import streamlit as st

from modules.operator import OperatorCore


def _write_temp_file(uploaded_file) -> Path:
    temp = NamedTemporaryFile(delete=False)
    temp.write(uploaded_file.getbuffer())
    temp.flush()
    return Path(temp.name)


def main() -> None:
    st.set_page_config(page_title="Omni Engine Command Center", layout="wide")
    st.title("🛰️ Omni Engine Command Center")
    st.write("Coordinate MCP services, evidence pipelines and strategic planning.")

    operator = OperatorCore()

    st.sidebar.header("Evidence Operations")
    directory_input = st.sidebar.text_input(
        "Evidence directory", value=str(Path.cwd() / "evidence_workspace"),
    )
    apply_changes = st.sidebar.checkbox("Apply changes", value=False)
    copy_files = st.sidebar.checkbox("Copy instead of move", value=False)

    if st.sidebar.button("Audit Directory"):
        evidence_dir = Path(directory_input)
        try:
            plan = operator.audit_directory(
                evidence_dir,
                apply_changes=apply_changes,
                copy_files=copy_files,
            )
        except FileNotFoundError:
            st.error("Evidence directory does not exist")
        else:
            st.success(f"Found {len(plan)} file operations")
            st.json(plan)

    st.header("📄 Document Intelligence")
    uploaded_pdf = st.file_uploader("Upload legal PDF", type=["pdf"])
    if uploaded_pdf is not None:
        tmp_path = _write_temp_file(uploaded_pdf)
        try:
            analysis = operator.analyze_pdf(tmp_path)
        except Exception as exc:  # pragma: no cover - defensive UI branch
            st.error(f"PDF analysis failed: {exc}")
        else:
            st.subheader("Analysis Result")
            st.json(analysis)

    st.header("🎙️ Audio Intelligence")
    uploaded_audios = st.file_uploader(
        "Upload audio evidence", type=["wav", "mp3", "m4a"], accept_multiple_files=True
    )
    if uploaded_audios:
        temp_paths = [_write_temp_file(file) for file in uploaded_audios]
        try:
            analysis = operator.transcribe_audio(temp_paths)
        except FileNotFoundError as exc:  # pragma: no cover - defensive UI branch
            st.error(str(exc))
        else:
            st.subheader("Transcription Blueprint")
            st.json(analysis)

    st.header("🧠 Strategic Planning")
    context = st.text_area(
        "Case context",
        "Detail the latest custody developments, financial disputes, and upcoming hearings.",
    )
    if st.button("Generate Codex 5 Pro Strategy"):
        try:
            strategy = operator.compile_recommendations(context)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.json(strategy)

    st.header("📊 System Report")
    if st.button("Build Operational Report"):
        evidence_dir = Path(directory_input) if directory_input else None
        pdfs: Iterable[Path] | None = None
        if uploaded_pdf is not None:
            pdfs = [tmp_path]
        audio_paths: Iterable[Path] | None = None
        if uploaded_audios:
            audio_paths = temp_paths
        report = operator.build_system_report(
            evidence_directory=evidence_dir if evidence_dir and evidence_dir.exists() else None,
            pdf_documents=pdfs,
            audio_evidence=audio_paths,
            context=context,
        )
        st.download_button(
            "Download report",
            data=operator.render_report(report),
            file_name="omni_engine_report.md",
        )
        st.json(report.to_dict())


if __name__ == "__main__":  # pragma: no cover - manual UI entry point
    main()
