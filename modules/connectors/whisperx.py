"""WhisperX transcription connector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import json

from ..memory_bridge import MemoryEntry
from . import Connector


@dataclass(slots=True)
class WhisperXConnector(Connector):
    """Loads pre-generated WhisperX transcripts and forwards them as memories."""

    name: str
    transcripts_root: Path
    layer: str = "audio_transcripts"
    source: str = "WHISPERX"

    def gather(self) -> Iterable[MemoryEntry]:
        entries: list[MemoryEntry] = []
        for transcript in sorted(self.transcripts_root.glob("**/*")):
            if transcript.suffix.lower() == ".json":
                entries.extend(self._from_json(transcript))
            elif transcript.suffix.lower() in {".txt", ".vtt"}:
                entries.append(
                    MemoryEntry(
                        layer=self.layer,
                        content=f"{transcript.stem}: {transcript.read_text().strip()}",
                        source=self.source,
                    )
                )
        return entries

    def _from_json(self, path: Path) -> list[MemoryEntry]:
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            return [
                MemoryEntry(
                    layer="ingestion_alerts",
                    content=f"Failed to parse {path.name}: {exc}",
                    source=self.source,
                )
            ]
        segments = payload.get("segments") or []
        entries: list[MemoryEntry] = []
        for segment in segments:
            speaker = segment.get("speaker", "unknown")
            text = segment.get("text", "").strip()
            if not text:
                continue
            start = segment.get("start", 0.0)
            end = segment.get("end", 0.0)
            entries.append(
                MemoryEntry(
                    layer=self.layer,
                    content=f"{path.stem} [{start:.2f}-{end:.2f}] {speaker}: {text}",
                    source=self.source,
                )
            )
        return entries


__all__ = ["WhisperXConnector"]
