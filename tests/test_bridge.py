from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from modules import (  # noqa: E402
    FusionLoop,
    FunctionSpec,
    McpCatalog,
    MemoryBridge,
    MemoryEntry,
    MemoryLayer,
    WitnessNetwork,
)


class DummyNode:
    """Minimal node storing outbound and inbound entries for testing."""

    def __init__(self, name: str, outbound: list[MemoryEntry]):
        self.name = name
        self.outbound = outbound
        self.inbound: list[MemoryEntry] = []

    def fetch_updates(self) -> list[MemoryEntry]:
        """Return pending outbound entries and clear the queue."""
        updates = list(self.outbound)
        self.outbound.clear()
        return updates

    def apply_update(self, entry: MemoryEntry) -> None:
        """Receive a broadcast ``entry`` from the fusion loop."""
        self.inbound.append(entry)


def test_fusion_loop_syncs_layers_and_nodes():
    layers: dict[str, MemoryLayer] = {}
    witness = WitnessNetwork()
    loop = FusionLoop(layers, witness)

    a_entry = MemoryEntry(layer="legal_evidence", content="doc1", source="A")
    node_a = DummyNode("A", [a_entry])
    node_b = DummyNode("B", [])
    witness.register(node_a)
    witness.register(node_b)

    loop.cycle([node_a])

    assert layers["legal_evidence"].all() == [a_entry]
    assert node_a.inbound == []
    assert node_b.inbound == [a_entry]
    assert witness.log == [a_entry]


def test_memory_layer_query_filters_by_timestamp():
    layer = MemoryLayer("legal_evidence")
    early = datetime(2024, 1, 1, tzinfo=timezone.utc)
    later = early + timedelta(days=1)
    late = later + timedelta(days=1)

    entry_early = MemoryEntry("legal_evidence", "first", "sensor", timestamp=early)
    entry_later = MemoryEntry("legal_evidence", "second", "sensor", timestamp=later)
    entry_latest = MemoryEntry("legal_evidence", "third", "sensor", timestamp=late)

    layer.add(entry_early)
    layer.add(entry_later)
    layer.add(entry_latest)

    assert layer.query(since=later) == [entry_later, entry_latest]

    with pytest.raises(ValueError):
        layer.query(since=datetime(2024, 1, 1))


def test_mcp_catalog_registration_and_description():
    catalog = McpCatalog()
    spec = FunctionSpec(
        name="memory.fetch_legal_evidence",
        description="Fetch legal evidence entries.",
        inputs={"since": "ISO-8601 timestamp"},
        outputs={"entries": "Serialized entries"},
        tags=("memory", "legal_evidence"),
    )

    catalog.register(spec)
    assert "memory.fetch_legal_evidence" in catalog
    assert catalog.get("memory.fetch_legal_evidence").description == "Fetch legal evidence entries."
    assert catalog.describe() == [spec.to_dict()]

    with pytest.raises(ValueError):
        catalog.register(spec)

    catalog.register(spec, replace=True)  # should not raise


def test_memory_bridge_exports_entries_and_catalog():
    bridge = MemoryBridge()
    bridge.register_layer("legal_evidence")
    node = DummyNode("A", [MemoryEntry("legal_evidence", "doc", "sensor")])
    bridge.register_node(node)

    bridge.sync([node])

    exported = bridge.export_layer("legal_evidence")
    assert exported[0]["content"] == "doc"

    functions = bridge.describe_functions()
    names = {f["name"] for f in functions}
    assert "memory.fetch_legal_evidence" in names
