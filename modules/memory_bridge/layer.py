from __future__ import annotations

"""Memory layer implementation."""

from datetime import datetime

from .entry import MemoryEntry


class MemoryLayer:
    """Simple in-memory storage for a particular category of memories."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.entries: list[MemoryEntry] = []

    def add(self, entry: MemoryEntry) -> None:
        """Add an entry to the layer."""
        if entry.layer != self.name:
            raise ValueError("Entry layer mismatch")
        self.entries.append(entry)

    def all(self) -> list[MemoryEntry]:
        """Return all entries currently stored in the layer."""
        return list(self.entries)

    def query(self, *, since: datetime | None = None) -> list[MemoryEntry]:
        """Return entries added at or after ``since``.

        Parameters
        ----------
        since:
            Optional timezone-aware timestamp. When provided, only entries with a
            ``timestamp`` equal to or later than ``since`` are returned.

        Returns
        -------
        list[MemoryEntry]
            Matching entries in chronological order.
        """

        if since is None:
            return self.all()
        if since.tzinfo is None or since.tzinfo.utcoffset(since) is None:
            raise ValueError("'since' must be timezone-aware.")
        return [entry for entry in self.entries if entry.timestamp >= since]
