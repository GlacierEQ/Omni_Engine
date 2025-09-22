"""Connector interfaces for ingesting external resources into the memory bridge."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, List

from ..memory_bridge import MemoryEntry


class Connector(ABC):
    """Abstract base class for connectors feeding the :class:`MemoryBridge`."""

    name: str

    @abstractmethod
    def gather(self) -> Iterable[MemoryEntry]:
        """Return new :class:`MemoryEntry` instances produced by the connector."""


@dataclass(slots=True)
class StaticConnector(Connector):
    """Simple connector producing a predefined set of entries."""

    name: str
    layer: str
    payloads: List[str]
    source: str

    def gather(self) -> Iterable[MemoryEntry]:
        timestamp = datetime.now(timezone.utc)
        return [
            MemoryEntry(layer=self.layer, content=payload, source=self.source, timestamp=timestamp)
            for payload in self.payloads
        ]


from .fileboss import FileBossConnector  # noqa: E402  (re-export)
from .mega_pdf import MegaPdfConnector  # noqa: E402
from .whisperx import WhisperXConnector  # noqa: E402

__all__ = [
    "Connector",
    "StaticConnector",
    "FileBossConnector",
    "MegaPdfConnector",
    "WhisperXConnector",
]
