# Operator Control Layer

The Operator control layer unifies the FILEBOSS-style filesystem organiser,
MegaPDF legal analysis shim, WhisperX audio intake and memory catalogue into a
single orchestration surface.  The module exposes a high-level API for building
status reports and exporting the results as Markdown so the findings can be
shared with counsel or loaded into the Supermemory MCP server.

## Components

- **OperatorCore** – orchestrates evidence organisation, MCP cataloguing and
  strategic planning.
- **Codex5ProClient** – deterministic emulation of the Codex 5 Pro reasoning
  engine used to generate action plans.
- **SystemReport** – dataclass returned by the operator containing a snapshot of
  directory plans, analysis data and recommendations.
- **Streamlit Dashboard** – the `gui/dashboard.py` application renders the
  operator features inside a GUI for analysts.

## Usage

```bash
streamlit run gui/dashboard.py
```

The dashboard allows you to:

1. Audit an evidence directory using FILEBOSS heuristics.
2. Upload PDF and audio evidence for MegaPDF/WhisperX analysis shims.
3. Generate Codex 5 Pro strategic plans for the current case context.
4. Download a consolidated Markdown report.

For scripted environments the operator can be used directly:

```python
from pathlib import Path
from modules.operator import OperatorCore

operator = OperatorCore()
report = operator.build_system_report(
    evidence_directory=Path("./evidence"),
    pdf_documents=[Path("./brief.pdf")],
    context="Custody and financial disputes require coordination",
)
operator.export_report(Path("docs/reports/system_recommendations.md"), context="Full case overview")
```
