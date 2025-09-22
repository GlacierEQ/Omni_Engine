# Omni Engine

Omni Engine consolidates memory synchronization, connector-driven ingestion,
and an operator dashboard for legal evidence analysis.

## Features

- **Memory Bridge** – typed layers and witness network for broadcasting
  intelligence updates between collaborating agents.
- **Connector Suite** – FILEBOSS, MEGA-PDF, and WhisperX adapters convert files,
  PDFs, and transcripts into structured `MemoryEntry` objects.
- **Operator Core** – orchestrates connectors, audits ingestion cycles, and
  generates actionable recommendations for administrators.
- **Interactive Dashboard** – Textual-based interface for monitoring connector
  throughput, layer fill levels, and operational recommendations in real time.

## Quick start

Install dependencies and run the test suite:

```bash
pip install -r requirements.txt
pytest -q
```

Populate the optional data directories and launch the dashboard:

```bash
mkdir -p data/fileboss data/pdfs data/transcripts
python -m app.gui
```

The dashboard can be refreshed interactively (press `r`) to observe connector
output as new evidence is ingested.

## Extending

New connectors can be added by subclassing `Connector` and registering the
implementation with `OperatorCore`. Use the provided unit tests as a template
for validating integration behaviour.
