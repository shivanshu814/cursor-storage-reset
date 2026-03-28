"""
Regenerate Cursor ``storage.json`` telemetry fields with atomic persistence.

Public API is intentionally small: path resolution, the refresh operation,
and version metadata for packaging.
"""

from __future__ import annotations

from cursor_storage_reset.paths import default_storage_path, resolve_default_storage_path
from cursor_storage_reset.storage import TELEMETRY_KEYS, refresh_telemetry_ids

__all__ = [
    "TELEMETRY_KEYS",
    "default_storage_path",
    "refresh_telemetry_ids",
    "resolve_default_storage_path",
    "__version__",
]


def _package_version() -> str:
    try:
        from importlib.metadata import version

        return version("cursor-storage-reset")
    except Exception:
        return "1.0.0"


__version__ = _package_version()
