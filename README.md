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

> **`pip` is enough:** Run one of the install commands below — the package is ready to use. **No clone, no build, no extra setup.** Then run `cursor-storage-reset` or `python3 -m cursor_storage_reset`; that’s all you need.

### From PyPI (recommended)

```bash
pip install cursor-storage-reset
```

PyPI project: [pypi.org/project/cursor-storage-reset](https://pypi.org/project/cursor-storage-reset/).

### Install with `pip` / `python -m pip` only (no clone)

Use this when you don’t want to download the repo — only the package. On many systems **`python3 -m pip`** is more reliable than plain `pip` (right Python + avoids “externally managed environment” surprises if you use a venv).

```bash
# Latest from PyPI
python3 -m pip install cursor-storage-reset

# Upgrade to newest release
python3 -m pip install -U cursor-storage-reset
```

### Install latest code from GitHub with `pip` (no `git clone` folder)

Installs straight from the default branch:

```bash
python3 -m pip install "git+https://github.com/shivanshu814/cursor-storage-reset.git"
```

Then run:

```bash
cursor-storage-reset --help
# or
python3 -m cursor_storage_reset --help
```

*(If your OS blocks system-wide installs, create a venv first and run the same `pip` commands inside it.)*

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

Restart Cursor after a successful run.

### Option A: installed command (if `Scripts` / `bin` is on your `PATH`)

```bash
# Default storage.json for this OS
cursor-storage-reset

# Explicit file
cursor-storage-reset /path/to/storage.json

# Print where Cursor’s default file is on this machine
cursor-storage-reset --print-default

# Version
cursor-storage-reset --version

# All flags
cursor-storage-reset --help
```

### Option B: same thing via Python (`python -m`) — useful when `PATH` is messy

After `pip install cursor-storage-reset`, run the module name **`cursor_storage_reset`** (underscores), not the PyPI hyphen name:

```bash
# Default path
python3 -m cursor_storage_reset

# Windows (try one of these, whichever works on your PC)
python -m cursor_storage_reset
py -3 -m cursor_storage_reset
```

```bash
# Custom storage.json
python3 -m cursor_storage_reset /path/to/storage.json

# Default path location only
python3 -m cursor_storage_reset --print-default

python3 -m cursor_storage_reset --version
python3 -m cursor_storage_reset --help
```

This is the same program as `cursor-storage-reset`; only the way you launch it changes.

### Option C: `pipx` (isolated app environment)

```bash
pipx install cursor-storage-reset
cursor-storage-reset --help
```

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

**Without storing a token in GitHub:** enable [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) on PyPI for project `cursor-storage-reset`, repository `shivanshu814/cursor-storage-reset`, workflow `publish-pypi.yml`. Then open **Actions → Publish Python package to PyPI → Run workflow**, or push a tag `v1.0.0` to trigger a release build.

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
