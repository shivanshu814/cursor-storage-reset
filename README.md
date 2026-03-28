# Cursor storage reset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/cursor-storage-reset.svg)](https://pypi.org/project/cursor-storage-reset/)

**Repository:** [github.com/shivanshu814/cursor-storage-reset](https://github.com/shivanshu814/cursor-storage-reset) · **Author:** [@shivanshu814](https://github.com/shivanshu814)

Small, tested, cross-platform utility. It regenerates these fields in Cursor’s `storage.json`:

- `telemetry.macMachineId`
- `telemetry.machineId`
- `telemetry.devDeviceId`

Writes use an **atomic replace** (temp file + `fsync`) so a crash mid-save is unlikely to leave truncated JSON. Keys outside the telemetry trio are preserved.

## Install

### From PyPI (recommended)

```bash
pip install cursor-storage-reset
```

PyPI project: [pypi.org/project/cursor-storage-reset](https://pypi.org/project/cursor-storage-reset/).

### From source

Clone (same name as on GitHub):

```bash
git clone https://github.com/shivanshu814/cursor-storage-reset.git
cd cursor-storage-reset
```

From the repository root (editable install for development):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Or install without dev tools:

```bash
pip install .
```

After install, the console entry point `cursor-storage-reset` is available.

## Usage

```bash
# Use the default path for the current OS
cursor-storage-reset

# Custom file
cursor-storage-reset /path/to/storage.json

# Show the resolved default for this machine
cursor-storage-reset --print-default

python -m cursor_storage_reset --version
```

Restart Cursor after a successful run.

### Default paths

| OS      | Default `storage.json` |
|--------|-------------------------|
| macOS  | `~/Library/Application Support/Cursor/User/globalStorage/storage.json` |
| Linux  | `$XDG_CONFIG_HOME/Cursor/User/globalStorage/storage.json`, or `~/.config/...` if unset |
| Windows | `%APPDATA%\Cursor\User\globalStorage\storage.json` |

## Development

```bash
pip install -e ".[dev]"
pytest
```

### Maintainer: publish to PyPI

1. Create an account on [pypi.org](https://pypi.org) and an **API token** (scope: entire account or this project).
2. Build and upload (do **not** commit the token):

```bash
pip install build twine
python -m build
twine check dist/*
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE twine upload dist/*
```

Use [TestPyPI](https://test.pypi.org/) first if you want a dry run (`twine upload --repository testpypi dist/*` after configuring `~/.pypirc`).

## API

```python
from pathlib import Path
from cursor_storage_reset import default_storage_path, refresh_telemetry_ids

refresh_telemetry_ids(Path("/explicit/storage.json"))
print(default_storage_path())
```

## Responsibility

This tool only edits **local** files you point it at. You must follow Cursor’s terms of service and applicable law. Use for legitimate purposes (e.g. privacy, troubleshooting your own setup).

## Layout

| Path | Role |
|------|------|
| `src/cursor_storage_reset/paths.py` | Pure path resolution (testable per OS) |
| `src/cursor_storage_reset/storage.py` | JSON load/save + atomic write + ID generation |
| `src/cursor_storage_reset/cli.py` | `argparse` CLI |
| `src/cursor_storage_reset/exceptions.py` | Narrow error types |
| `tests/` | Pytest coverage for paths + storage |

Legacy root-level `mac.py` / `linux.py` / `windows.py` scripts were removed in favor of one cross-platform CLI and `python -m cursor_storage_reset`.
