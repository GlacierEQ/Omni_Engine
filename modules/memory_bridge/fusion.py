from __future__ import annotations

"""Fusion loop coordinating synchronization across nodes."""

from typing import Iterable

from .entry import MemoryEntry
from .layer import MemoryLayer
from .node import IntelligenceNode
from .witness import WitnessNetwork


class FusionLoop:
    """Coordinates synchronization across nodes and memory layers."""

    def __init__(self, layers: dict[str, MemoryLayer], witnesses: WitnessNetwork) -> None:
        self.layers = layers
        self.witnesses = witnesses

    def cycle(self, nodes: Iterable[IntelligenceNode]) -> None:
        """Perform a single synchronization cycle."""
        for node in nodes:
            for entry in node.fetch_updates():
                layer = self.layers.setdefault(entry.layer, MemoryLayer(entry.layer))
                layer.add(entry)
                self.witnesses.broadcast(entry, origin=node)
