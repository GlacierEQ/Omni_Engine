from __future__ import annotations

"""Interfaces for intelligence nodes."""

from typing import Iterable, Protocol

from .entry import MemoryEntry


class IntelligenceNode(Protocol):
    """Protocol every intelligence node must implement."""

    name: str

    def fetch_updates(self) -> Iterable[MemoryEntry]:
        """Return new memory entries produced by this node."""
        ...

    def apply_update(self, entry: MemoryEntry) -> None:
        """Handle a memory update propagated from the fusion loop."""
        ...
