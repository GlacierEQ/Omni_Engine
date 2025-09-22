"""High level orchestration helpers for Omni Engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional

from modules.evidence_pipeline.main import (
    GlacierEQFileBossInterface,
    MegaPDFLegalAnalyzer,
    MemoryLayerCompiler,
    WhisperXEvidenceProcessor,
)
from modules.filesystem_mcp.main import organize_directory
from modules.integrations import Codex5ProClient
from modules.mcp_catalog.main import build_catalog


@dataclass
class SystemReport:
    """Aggregate view of the current system status."""

    directory_plan: Dict[str, str] = field(default_factory=dict)
    pdf_analyses: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    audio_analysis: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    memory_status: Mapping[str, str] = field(default_factory=dict)
    fileboss_capabilities: Mapping[str, str] = field(default_factory=dict)
    mcp_catalog: Mapping[str, Mapping[str, object]] = field(default_factory=dict)
    codex_strategy: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON serialisable representation of the report."""

        return {
            "directory_plan": dict(self.directory_plan),
            "pdf_analyses": {k: dict(v) for k, v in self.pdf_analyses.items()},
            "audio_analysis": {k: dict(v) for k, v in self.audio_analysis.items()},
            "memory_status": dict(self.memory_status),
            "fileboss_capabilities": dict(self.fileboss_capabilities),
            "mcp_catalog": {k: dict(v) for k, v in self.mcp_catalog.items()},
            "codex_strategy": dict(self.codex_strategy),
        }


class OperatorCore:
    """Central coordinator that connects evidence, MCP and intelligence layers."""

    def __init__(self, codex_client: Optional[Codex5ProClient] = None) -> None:
        self.fileboss = GlacierEQFileBossInterface()
        self.pdf_analyzer = MegaPDFLegalAnalyzer()
        self.audio_processor = WhisperXEvidenceProcessor()
        self.memory_compiler = MemoryLayerCompiler()
        self.codex_client = codex_client or Codex5ProClient()

    # ------------------------------------------------------------------
    # Filesystem integration
    # ------------------------------------------------------------------
    def audit_directory(
        self,
        directory: Path,
        *,
        apply_changes: bool = False,
        copy_files: bool = False,
    ) -> Dict[str, str]:
        """Return a mapping of planned moves for ``directory``.

        When ``apply_changes`` is ``True`` the reorganised structure is written
        to disk; otherwise the function performs a dry run mirroring the
        behaviour of the CLI tool.
        """

        if not directory.exists() or not directory.is_dir():
            raise FileNotFoundError(directory)

        moves = organize_directory(
            directory,
            dry_run=not apply_changes,
            copy_files=copy_files,
        )
        return {str(src): str(dst) for src, dst in moves.items()}

    # ------------------------------------------------------------------
    # Evidence analysis layers
    # ------------------------------------------------------------------
    def analyze_pdf(self, pdf_path: Path) -> Mapping[str, str]:
        """Analyse a PDF document using the MegaPDF shim."""

        return self.pdf_analyzer.analyze_legal_pdfs(pdf_path)

    def transcribe_audio(self, audio_files: Iterable[Path]) -> Mapping[str, str]:
        """Invoke the WhisperX shim for the supplied ``audio_files``."""

        files = list(audio_files)
        return self.audio_processor.transcribe_evidence_audio(files)

    def verify_memory_layers(self) -> Mapping[str, str]:
        """Return the status of all configured memory layers."""

        return self.memory_compiler.verify_memory_connections()

    def build_mcp_catalog(self) -> Mapping[str, Mapping[str, object]]:
        """Expose the cached MCP catalog."""

        return build_catalog()

    def compile_recommendations(self, context: str) -> Mapping[str, object]:
        """Use Codex 5 Pro heuristics to build a strategic plan."""

        return self.codex_client.generate_strategy(context)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def build_system_report(
        self,
        *,
        evidence_directory: Optional[Path] = None,
        pdf_documents: Optional[Iterable[Path]] = None,
        audio_evidence: Optional[Iterable[Path]] = None,
        context: str = "",
        apply_directory_changes: bool = False,
        copy_files: bool = False,
    ) -> SystemReport:
        """Aggregate the current system state into a :class:`SystemReport`."""

        directory_plan: Dict[str, str] = {}
        if evidence_directory is not None:
            directory_plan = self.audit_directory(
                evidence_directory,
                apply_changes=apply_directory_changes,
                copy_files=copy_files,
            )

        pdf_results: Dict[str, Mapping[str, str]] = {}
        for pdf in pdf_documents or []:
            pdf_results[str(pdf)] = self.analyze_pdf(pdf)

        audio_results: Dict[str, Mapping[str, str]] = {}
        for audio in audio_evidence or []:
            audio_results[str(audio)] = self.transcribe_audio([audio])

        memory_status = self.verify_memory_layers()
        fileboss_capabilities = self.fileboss.quantum_file_processing()
        mcp_catalog = self.build_mcp_catalog()
        codex_strategy = self.compile_recommendations(context or "General system overview")

        return SystemReport(
            directory_plan=directory_plan,
            pdf_analyses=pdf_results,
            audio_analysis=audio_results,
            memory_status=memory_status,
            fileboss_capabilities=fileboss_capabilities,
            mcp_catalog=mcp_catalog,
            codex_strategy=codex_strategy,
        )

    def export_report(
        self,
        output_path: Path,
        *,
        evidence_directory: Optional[Path] = None,
        pdf_documents: Optional[Iterable[Path]] = None,
        audio_evidence: Optional[Iterable[Path]] = None,
        context: str = "",
    ) -> SystemReport:
        """Generate a markdown report and persist it to ``output_path``."""

        report = self.build_system_report(
            evidence_directory=evidence_directory,
            pdf_documents=pdf_documents,
            audio_evidence=audio_evidence,
            context=context,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.render_report(report))
        return report

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def render_report(self, report: SystemReport) -> str:
        """Public helper to render ``report`` to markdown."""

        return self._render_report_markdown(report)

    def _render_report_markdown(self, report: SystemReport) -> str:
        """Render ``report`` as markdown."""

        lines: List[str] = ["# Omni Engine Operational Report", ""]

        if report.directory_plan:
            lines.append("## Evidence Directory Plan")
            lines.append("")
            for src, dst in sorted(report.directory_plan.items()):
                lines.append(f"- `{src}` → `{dst}`")
            lines.append("")

        if report.pdf_analyses:
            lines.append("## PDF Analyses")
            lines.append("")
            for path, data in report.pdf_analyses.items():
                lines.append(f"### {path}")
                for key, value in data.items():
                    lines.append(f"- **{key}**: {value}")
                lines.append("")

        if report.audio_analysis:
            lines.append("## Audio Evidence")
            lines.append("")
            for path, data in report.audio_analysis.items():
                lines.append(f"### {path}")
                for key, value in data.items():
                    lines.append(f"- **{key}**: {value}")
                lines.append("")

        lines.append("## Memory Layer Status")
        lines.append("")
        for key, value in report.memory_status.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")

        if report.fileboss_capabilities:
            lines.append("## FILEBOSS Integration")
            lines.append("")
            for key, value in report.fileboss_capabilities.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")

        lines.append("## MCP Catalog")
        lines.append("")
        for name, data in report.mcp_catalog.items():
            lines.append(f"- **{name}**: {data['status']}")
        lines.append("")

        lines.append("## Codex 5 Pro Recommendations")
        lines.append("")
        lines.append(f"**Summary:** {report.codex_strategy.get('summary', 'N/A')}")
        focus_areas = report.codex_strategy.get("focus_areas", [])
        if focus_areas:
            lines.append("- Focus Areas:")
            for item in focus_areas:
                lines.append(f"  - {item}")
        action_items = report.codex_strategy.get("action_items", [])
        if action_items:
            lines.append("- Action Items:")
            for action in action_items:
                title = action.get("title", "Item")
                details = action.get("details", "")
                lines.append(f"  - **{title}:** {details}")
        recommendations = report.codex_strategy.get("recommendations", [])
        if recommendations:
            lines.append("- Recommendations:")
            for rec in recommendations:
                lines.append(f"  - {rec}")

        lines.append("")
        lines.append("_Report generated by OperatorCore._")
        lines.append("")
        return "\n".join(lines)
