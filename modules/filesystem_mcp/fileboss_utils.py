"""Utility helpers adapted from Glaciereq/FILEBOSS."""
from __future__ import annotations

from pathlib import Path
import hashlib
import re


def safe_filename(filename: str) -> str:
    """Return a filesystem-safe version of ``filename``.

    The implementation mirrors the sanitisation rules used by
    Glaciereq/FILEBOSS. Problematic characters are replaced with
    underscores, repeated separators are collapsed and the result is
    truncated to a reasonable length.
    """
    if not filename or not filename.strip():
        return "unnamed_file"
    filename = filename.strip()
    replacements = {
        '/': '_',
        '\\': '_',
        ':': '_',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_',
        '\n': '_',
        '\r': '_',
        '\t': '_',
    }
    for char, repl in replacements.items():
        filename = filename.replace(char, repl)
    filename = re.sub(r'[\s_]+', '_', filename)
    filename = re.sub(r'^[._\-]+|[._\-]+$', '', filename)
    if not filename:
        filename = "unnamed_file"
    if len(filename) > 100:
        filename = filename[:100]
        last_underscore = filename.rfind('_')
        if last_underscore > 50:
            filename = filename[:last_underscore]
    return filename


def calculate_file_hash(file_path: Path, chunk_size: int = 8192) -> str:
    """Return SHA-256 hash of ``file_path``.

    Returns an empty string if the file cannot be read.
    """
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return ""


def get_file_extension_type(extension: str) -> str:
    """Map a file extension to a high level type.

    The mapping is a subset of the one used by FILEBOSS.
    """
    extension = extension.lower().lstrip('.')
    mapping = {
        'pdf': 'document', 'doc': 'document', 'docx': 'document', 'txt': 'document',
        'rtf': 'document', 'odt': 'document',
        'mp3': 'audio', 'wav': 'audio', 'flac': 'audio', 'm4a': 'audio',
        'aac': 'audio', 'ogg': 'audio', 'wma': 'audio',
        'mp4': 'video', 'avi': 'video', 'mov': 'video', 'mkv': 'video',
        'wmv': 'video', 'flv': 'video', 'webm': 'video',
        'jpg': 'image', 'jpeg': 'image', 'png': 'image', 'gif': 'image',
        'bmp': 'image', 'svg': 'image', 'webp': 'image',
        'zip': 'archive', 'rar': 'archive', '7z': 'archive', 'tar': 'archive',
        'gz': 'archive',
    }
    return mapping.get(extension, 'unknown')
