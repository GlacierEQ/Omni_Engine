"""Filesystem organizer leveraging Glaciereq/FILEBOSS logic.

Usage:
    python main.py <directory> [--dry-run] [--copy]

Files are categorised by extension and relocated into type-specific
subdirectories. Filenames are sanitised using FILEBOSS' ``safe_filename``
utility and duplicates are resolved using content hashing.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from .fileboss_utils import safe_filename, calculate_file_hash, get_file_extension_type

# Mapping from file type to destination folder name
FOLDER_MAP = {
    "document": "Documents",
    "image": "Images",
    "audio": "Audio",
    "video": "Videos",
    "archive": "Archives",
}


@dataclass
class Config:
    """Configuration flags for the organiser."""

    dry_run: bool = True
    copy_files: bool = False


class FileBossOrganizer:
    """Organise files using sanitisation and conflict resolution logic."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def categorize(self, file_path: Path) -> str:
        file_type = get_file_extension_type(file_path.suffix)
        return FOLDER_MAP.get(file_type, "Other")

    def _unique_target(self, target_path: Path, src: Path) -> Path | None:
        """Return a unique path for ``src`` under ``target_path``.

        If a file with identical content already exists the operation is
        skipped and ``None`` is returned.
        """
        if not target_path.exists():
            return target_path
        if calculate_file_hash(src) == calculate_file_hash(target_path):
            return None
        stem, suffix = target_path.stem, target_path.suffix
        counter = 1
        while True:
            candidate = target_path.with_name(f"{stem}_{counter}{suffix}")
            if not candidate.exists():
                return candidate
            if calculate_file_hash(src) == calculate_file_hash(candidate):
                return None
            counter += 1

    def organize_directory(self, directory: Path) -> Dict[Path, Path]:
        moves: Dict[Path, Path] = {}
        for entry in sorted(directory.iterdir()):
            if not entry.is_file():
                continue
            category = self.categorize(entry)
            target_dir = directory / category
            target_dir.mkdir(exist_ok=True)
            sanitized = safe_filename(entry.stem) + entry.suffix.lower()
            target_path = target_dir / sanitized
            unique_target = self._unique_target(target_path, entry)
            if unique_target is None:
                continue
            moves[entry] = unique_target
            if not self.config.dry_run:
                if self.config.copy_files:
                    unique_target.write_bytes(entry.read_bytes())
                else:
                    entry.replace(unique_target)
        return moves


def categorize_file(file_path: Path) -> str:
    """Return the destination category for ``file_path``."""
    return FileBossOrganizer(Config()).categorize(file_path)


def organize_directory(directory: Path, dry_run: bool = True, copy_files: bool = False) -> Dict[Path, Path]:
    """Public helper mirroring the previous API."""
    organizer = FileBossOrganizer(Config(dry_run=dry_run, copy_files=copy_files))
    return organizer.organize_directory(directory)


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files using FILEBOSS logic")
    parser.add_argument("directory", type=Path, help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them")
    args = parser.parse_args()

    if not args.directory.exists() or not args.directory.is_dir():
        raise SystemExit(f"❌ Directory not found: {args.directory}")

    moves = organize_directory(args.directory, dry_run=args.dry_run, copy_files=args.copy)
    for src, dst in moves.items():
        action = "Would copy" if args.copy and args.dry_run else (
            "Copied" if args.copy else ("Would move" if args.dry_run else "Moved")
        )
        print(f"{action} {src.name} -> {dst.relative_to(args.directory)}")
    if args.dry_run:
        print("Run without --dry-run to apply changes.")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
