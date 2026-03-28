from __future__ import annotations

import json
from pathlib import Path

import pytest

from cursor_storage_reset.exceptions import InvalidStorageFile
from cursor_storage_reset.storage import TELEMETRY_KEYS, refresh_telemetry_ids


def test_refresh_preserves_other_keys(tmp_path: Path) -> None:
    path = tmp_path / "storage.json"
    path.write_text(
        json.dumps(
            {
                "keep": "value",
                TELEMETRY_KEYS[0]: "oldmac",
                TELEMETRY_KEYS[1]: "oldmid",
                TELEMETRY_KEYS[2]: "00000000-0000-0000-0000-000000000000",
            },
        ),
        encoding="utf-8",
    )

    refresh_telemetry_ids(path)
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["keep"] == "value"
    assert data[TELEMETRY_KEYS[0]] != "oldmac"
    assert data[TELEMETRY_KEYS[1]] != "oldmid"
    assert data[TELEMETRY_KEYS[2]] != "00000000-0000-0000-0000-000000000000"
    assert len(data[TELEMETRY_KEYS[0]]) == 64
    assert len(data[TELEMETRY_KEYS[1]]) == 64


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        refresh_telemetry_ids(tmp_path / "nope.json")


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "storage.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(InvalidStorageFile):
        refresh_telemetry_ids(path)