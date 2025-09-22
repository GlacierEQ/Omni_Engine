"""Operator orchestration for Omni Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from .connectors import Connector, FileBossConnector, MegaPdfConnector, StaticConnector, WhisperXConnector
from .memory_bridge import MemoryBridge, MemoryEntry, WitnessNetwork


@dataclass(slots=True)
class ConnectorAudit:
    """Outcome of running a connector during an ingestion cycle."""

    name: str
    produced: int
    layer_counts: Dict[str, int]
    alerts: List[str] = field(default_factory=list)


@dataclass(slots=True)
class AuditReport:
    """Summarises a full ingestion cycle across all connectors."""

    timestamp: datetime
    connectors: List[ConnectorAudit]

    def to_dict(self) -> dict[str, object]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "connectors": [
                {
                    "name": audit.name,
                    "produced": audit.produced,
                    "layer_counts": dict(audit.layer_counts),
                    "alerts": list(audit.alerts),
                }
                for audit in self.connectors
            ],
        }


class OperatorCore:
    """Coordinates connectors, memory bridge layers, and witness network."""

    def __init__(
        self,
        *,
        bridge: MemoryBridge | None = None,
        witnesses: WitnessNetwork | None = None,
        connectors: Iterable[Connector] | None = None,
    ) -> None:
        self.bridge = bridge or MemoryBridge(witnesses=witnesses)
        self.connectors: dict[str, Connector] = {}
        if connectors:
            for connector in connectors:
                self.register_connector(connector)

    def register_connector(self, connector: Connector) -> None:
        """Register ``connector`` with the operator."""

        self.connectors[connector.name] = connector

    def run_cycle(self) -> AuditReport:
        """Run all connectors, ingest their entries, and produce a report."""

        audits: list[ConnectorAudit] = []
        for connector in self.connectors.values():
            entries = list(connector.gather())
            layer_counts: dict[str, int] = {}
            alerts: list[str] = []
            for entry in entries:
                layer = self.bridge.register_layer(entry.layer)
                layer.add(entry)
                layer_counts[entry.layer] = layer_counts.get(entry.layer, 0) + 1
                if entry.layer == "ingestion_alerts":
                    alerts.append(entry.content)
            audits.append(
                ConnectorAudit(
                    name=connector.name,
                    produced=len(entries),
                    layer_counts=layer_counts,
                    alerts=alerts,
                )
            )
        return AuditReport(timestamp=datetime.now(timezone.utc), connectors=audits)

    def layer_snapshot(self) -> dict[str, list[MemoryEntry]]:
        """Return a dictionary of layer names to their stored entries."""

        return {name: layer.all() for name, layer in self.bridge.layers.items()}

    def generate_recommendations(self, report: AuditReport) -> list[str]:
        """Produce actionable recommendations based on ``report`` outcomes."""

        recommendations: list[str] = []
        for audit in report.connectors:
            if audit.produced == 0:
                recommendations.append(
                    f"Connector '{audit.name}' produced no entries. Verify its data sources."
                )
            if audit.alerts:
                recommendations.append(
                    f"Connector '{audit.name}' emitted {len(audit.alerts)} alerts that require review."
                )
        if not recommendations:
            recommendations.append("All connectors are operating nominally. Continue monitoring throughput.")
        return recommendations


def build_default_operator(base_path: Path | None = None) -> OperatorCore:
    """Construct an operator configured with default connectors."""

    base = base_path or Path.cwd()
    connectors: list[Connector] = [
        FileBossConnector(name="FILEBOSS", root=base / "data" / "fileboss"),
        MegaPdfConnector(name="MEGA_PDF", documents_root=base / "data" / "pdfs"),
        WhisperXConnector(name="WHISPERX", transcripts_root=base / "data" / "transcripts"),
        StaticConnector(
            name="SOVEREIGN_ASCENSION_PROTOCOL",
            layer="operational_notes",
            payloads=[
                "Synchronized memory layers across legal_evidence, document_insights, audio_transcripts.",
                "Maintain 24/7 monitoring and refresh connectors hourly.",
            ],
            source="OPERATOR",
        ),
    ]
    return OperatorCore(connectors=connectors)


__all__ = [
    "AuditReport",
    "ConnectorAudit",
    "OperatorCore",
    "build_default_operator",
]
