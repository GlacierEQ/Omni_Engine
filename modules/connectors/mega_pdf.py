"""MEGA-PDF analysis connector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:  # pragma: no cover - optional dependency handled at runtime
    import fitz  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - executed when PyMuPDF missing
    fitz = None

from ..memory_bridge import MemoryEntry
from . import Connector


@dataclass(slots=True)
class MegaPdfConnector(Connector):
    """Extracts text snippets from PDF documents for memory ingestion."""

    name: str
    documents_root: Path
    layer: str = "document_insights"
    source: str = "MEGA_PDF"
    max_pages: int = 3
    characters_per_page: int = 280

    def gather(self) -> Iterable[MemoryEntry]:
        entries: list[MemoryEntry] = []
        if fitz is None:
            entries.append(
                MemoryEntry(
                    layer="ingestion_alerts",
                    content="PyMuPDF is not installed; PDF analysis skipped.",
                    source=self.source,
                )
            )
            return entries
        for pdf in sorted(self.documents_root.glob("**/*.pdf")):
            try:
                with fitz.open(pdf) as doc:
                    for page_index, page in enumerate(doc):
                        if page_index >= self.max_pages:
                            break
                        text = page.get_text().strip()
                        if not text:
                            continue
                        snippet = text[: self.characters_per_page]
                        entries.append(
                            MemoryEntry(
                                layer=self.layer,
                                content=f"{pdf.name}#page{page_index + 1}: {snippet}",
                                source=self.source,
                            )
                        )
            except RuntimeError as exc:
                entries.append(
                    MemoryEntry(
                        layer="ingestion_alerts",
                        content=f"Failed to read {pdf.name}: {exc}",
                        source=self.source,
                    )
                )
        return entries


__all__ = ["MegaPdfConnector"]
