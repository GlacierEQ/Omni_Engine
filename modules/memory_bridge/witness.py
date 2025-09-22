from __future__ import annotations

"""Witness network for broadcasting memory updates."""

from .entry import MemoryEntry
from .node import IntelligenceNode


class WitnessNetwork:
    """Event bus recording and broadcasting memory updates."""

    def __init__(self) -> None:
        self.log: list[MemoryEntry] = []
        self.subscribers: list[IntelligenceNode] = []

    def register(self, node: IntelligenceNode) -> None:
        """Register ``node`` to receive broadcast updates."""
        self.subscribers.append(node)

    def broadcast(self, entry: MemoryEntry, *, origin: IntelligenceNode | None = None) -> None:
        """Record ``entry`` and send it to all subscribers except ``origin``.

        Parameters
        ----------
        entry:
            The memory update to distribute.
        origin:
            The node that produced the update. It will not receive the broadcast.
            ``None`` means broadcast to all subscribers.
        """

        self.log.append(entry)
        for node in self.subscribers:
            if origin is not None and node is origin:
                continue
            node.apply_update(entry)
