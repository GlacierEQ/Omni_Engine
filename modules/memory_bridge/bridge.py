from __future__ import annotations

"""High-level facade orchestrating memory bridge components."""

from datetime import datetime
from typing import Iterable

from .catalog import FunctionSpec, McpCatalog
from .fusion import FusionLoop
from .layer import MemoryLayer
from .node import IntelligenceNode
from .witness import WitnessNetwork


class MemoryBridge:
    """Coordinate layers, witness network, and MCP catalog.

    The bridge exposes a lightweight facade over the low-level components so
    callers can register layers, subscribe nodes, synchronise updates, and
    export metadata for external agents.
    """

    def __init__(
        self,
        *,
        layers: dict[str, MemoryLayer] | None = None,
        witnesses: WitnessNetwork | None = None,
        catalog: McpCatalog | None = None,
    ) -> None:
        self.layers = layers or {}
        self.witnesses = witnesses or WitnessNetwork()
        self.catalog = catalog or McpCatalog()
        self._fusion = FusionLoop(self.layers, self.witnesses)

        for name in list(self.layers):
            self._register_layer_spec(name)

    def register_layer(self, name: str) -> MemoryLayer:
        """Ensure a memory layer with ``name`` exists and return it."""

        if not name.strip():
            raise ValueError("Layer name cannot be empty.")
        layer = self.layers.get(name)
        if layer is None:
            layer = MemoryLayer(name)
            self.layers[name] = layer
            self._register_layer_spec(name)
        return layer

    def get_layer(self, name: str) -> MemoryLayer:
        """Return the layer with ``name`` or raise ``KeyError`` if absent."""

        return self.layers[name]

    def register_node(self, node: IntelligenceNode) -> None:
        """Register ``node`` with the witness network."""

        self.witnesses.register(node)

    def sync(self, nodes: Iterable[IntelligenceNode]) -> None:
        """Run a synchronization cycle using the underlying fusion loop."""

        self._fusion.cycle(nodes)

    def export_layer(self, name: str, *, since: datetime | None = None) -> list[dict[str, str]]:
        """Return serialized entries from ``name`` filtered by ``since``."""

        layer = self.get_layer(name)
        return [entry.to_dict() for entry in layer.query(since=since)]

    def describe_functions(self) -> list[dict[str, object]]:
        """Return the MCP catalog entries as dictionaries."""

        return self.catalog.describe()

    def _register_layer_spec(self, name: str) -> None:
        """Create or refresh the catalog entry for ``name``."""

        spec = FunctionSpec(
            name=f"memory.fetch_{name}",
            description=(
                f"Retrieve stored entries from the '{name}' memory layer."
            ),
            inputs={
                "since": "Optional ISO-8601 timestamp used to filter results.",
            },
            outputs={
                "entries": (
                    "List of serialized memory entries with layer, source, "
                    "content, and timestamp."
                ),
            },
            tags=("memory", name),
        )
        self.catalog.register(spec, replace=True)
