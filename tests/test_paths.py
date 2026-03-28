from __future__ import annotations

from pathlib import Path

from cursor_storage_reset.paths import resolve_default_storage_path


def test_darwin_path() -> None:
    home = Path("/Users/tester")
    p = resolve_default_storage_path(platform="darwin", home=home, environ={})
    assert p == home / "Library/Application Support/Cursor/User/globalStorage/storage.json"


def test_linux_respects_xdg() -> None:
    home = Path("/home/tester")
    env = {"XDG_CONFIG_HOME": "/alt/cfg"}
    p = resolve_default_storage_path(platform="linux", home=home, environ=env)
    assert p == Path("/alt/cfg/Cursor/User/globalStorage/storage.json")


def test_linux_fallback_config() -> None:
    home = Path("/home/tester")
    p = resolve_default_storage_path(platform="linux", home=home, environ={})
    assert p == home / ".config/Cursor/User/globalStorage/storage.json"


def test_windows_uses_appdata() -> None:
    home = Path("C:/Users/tester")
    env = {"APPDATA": r"C:\Users\tester\AppData\Roaming"}
    p = resolve_default_storage_path(platform="win32", home=home, environ=env)
    assert p == Path(r"C:\Users\tester\AppData\Roaming/Cursor/User/globalStorage/storage.json")


def test_windows_appdata_missing_falls_back() -> None:
    home = Path("C:/Users/tester")
    p = resolve_default_storage_path(platform="win32", home=home, environ={})
    assert p == home / "AppData/Roaming/Cursor/User/globalStorage/storage.json"
