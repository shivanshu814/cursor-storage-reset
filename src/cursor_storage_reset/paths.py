"""
Platform-aware resolution of Cursor's ``storage.json`` location.

Uses the same layout Cursor documents for user data (VS Code–style paths).
``XDG_CONFIG_HOME`` is honored on Linux/BSD; ``%APPDATA%`` on Windows.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Mapping

__all__ = ["default_storage_path", "resolve_default_storage_path"]

_CURSOR_STORAGE = Path("Cursor/User/globalStorage/storage.json")


def resolve_default_storage_path(
    *,
    platform: str,
    home: Path,
    environ: Mapping[str, str],
) -> Path:
    """
    Pure path resolver for testing and nonstandard environments.

    ``platform`` follows ``sys.platform`` (``darwin``, ``win32``, ``linux``, …).
    Platforms other than ``darwin`` and ``win32`` use the XDG-style config base.
    """
    if platform == "darwin":
        return home / "Library/Application Support" / _CURSOR_STORAGE

    if platform == "win32":
        appdata = str(environ.get("APPDATA", "") or "").strip()
        root = Path(appdata) if appdata else home / "AppData" / "Roaming"
        return root / _CURSOR_STORAGE

    xdg = str(environ.get("XDG_CONFIG_HOME", "") or "").strip()
    base = Path(xdg) if xdg else home / ".config"
    return base / _CURSOR_STORAGE


def default_storage_path() -> Path:
    """Default ``storage.json`` for this process (current platform + environment)."""
    return resolve_default_storage_path(
        platform=sys.platform,
        home=Path.home(),
        environ=os.environ,
    )
