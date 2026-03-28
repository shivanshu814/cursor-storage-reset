"""Read/modify ``storage.json`` with atomic persistence."""

from __future__ import annotations

import json
import os
import secrets
import tempfile
import uuid
from pathlib import Path
from typing import Any, Final, Mapping, MutableMapping

from cursor_storage_reset.exceptions import InvalidStorageFile

__all__ = ["TELEMETRY_KEYS", "refresh_telemetry_ids"]

TELEMETRY_KEYS: Final[tuple[str, ...]] = (
    "telemetry.macMachineId",
    "telemetry.machineId",
    "telemetry.devDeviceId",
)

_TELEMETRY_HEX_ID_LENGTH = 64


def _random_hex_id(length_chars: int) -> str:
    if length_chars <= 0 or length_chars % 2:
        raise ValueError("length_chars must be a positive even integer")
    return secrets.token_hex(length_chars // 2)


def _load_storage(path: Path) -> MutableMapping[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InvalidStorageFile(f"cannot read storage file: {path}") from exc
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidStorageFile(f"invalid JSON in storage file: {path}") from exc
    if not isinstance(parsed, dict):
        raise InvalidStorageFile(f"storage root must be a JSON object: {path}")
    return parsed  # type: ignore[return-value]


def _atomic_write_json(path: Path, data: Mapping[str, Any]) -> None:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            tmp_path.unlink(missing_ok=True)
        except AttributeError:
            if tmp_path.exists():
                tmp_path.unlink()
        raise


def refresh_telemetry_ids(storage_path: Path) -> Path:
    """
    Regenerate telemetry identifiers in Cursor ``storage.json``.

    Returns the resolved path written. Other keys are preserved.

    Raises:
        FileNotFoundError: if ``storage_path`` does not exist.
        InvalidStorageFile: on read/parse errors.
    """
    target = storage_path.expanduser().resolve()
    if not target.is_file():
        raise FileNotFoundError(str(target))

    data = _load_storage(target)
    data[TELEMETRY_KEYS[0]] = _random_hex_id(_TELEMETRY_HEX_ID_LENGTH)
    data[TELEMETRY_KEYS[1]] = _random_hex_id(_TELEMETRY_HEX_ID_LENGTH)
    data[TELEMETRY_KEYS[2]] = str(uuid.uuid4())

    _atomic_write_json(target, data)
    return target
