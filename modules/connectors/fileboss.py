"""FILEBOSS integration surface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ..memory_bridge import MemoryEntry
from . import Connector


@dataclass(slots=True)
class FileBossConnector(Connector):
    """Connector that indexes files from a working directory."""

    name: str
    root: Path
    layer: str = "legal_evidence"
    source: str = "FILEBOSS"

    def gather(self) -> Iterable[MemoryEntry]:
        entries: list[MemoryEntry] = []
        for path in sorted(self.root.rglob("*")):
            if path.is_file():
                entries.append(
                    MemoryEntry(
                        layer=self.layer,
                        content=f"Indexed file: {path.relative_to(self.root)}",
                        source=self.source,
                    )
                )
        return entries


__all__ = ["FileBossConnector"]
