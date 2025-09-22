from __future__ import annotations

"""Data models for the memory bridge."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class MemoryEntry:
    """Represents a unit of information stored in a memory layer."""

    layer: str
    content: str
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, str]:
        """Serialize the entry into a JSON-friendly dictionary."""

        return {
            "layer": self.layer,
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
        }
