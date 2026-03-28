# Cursor storage reset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/cursor-storage-reset.svg)](https://pypi.org/project/cursor-storage-reset/)

**Repository:** [github.com/shivanshu814/cursor-storage-reset](https://github.com/shivanshu814/cursor-storage-reset) · **Author:** [@shivanshu814](https://github.com/shivanshu814)

Regenerates these fields in Cursor’s `storage.json`:

- `telemetry.macMachineId`
- `telemetry.machineId`
- `telemetry.devDeviceId`

Other keys are left as-is. Saves use an **atomic write** (temp file + `fsync`) so a crash mid-save is unlikely to corrupt the file.

---

## 1. Install with `pip` (normal use)

**No git clone, no build.** Pick one install line, then run the tool (see [Run](#run-after-install)).

### From PyPI

```bash
python3 -m pip install cursor-storage-reset
```

PyPI: [pypi.org/project/cursor-storage-reset](https://pypi.org/project/cursor-storage-reset/)

Upgrade:

```bash
python3 -m pip install -U cursor-storage-reset
```

### From GitHub (no clone folder)

If you prefer the latest `main` without cloning:

```bash
python3 -m pip install "git+https://github.com/shivanshu814/cursor-storage-reset.git"
```

### If `pip` complains (macOS Homebrew, “externally managed environment”)

Use a virtualenv, then the same `pip` commands **inside** it:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python3 -m pip install cursor-storage-reset
```

### Run after install

Restart Cursor after it succeeds.

```bash
# Default storage.json for this OS
cursor-storage-reset
# same thing:
python3 -m cursor_storage_reset
```

More examples:

```bash
cursor-storage-reset /path/to/storage.json
cursor-storage-reset --print-default
cursor-storage-reset --version
cursor-storage-reset --help
```

On Windows, if `python3` is missing, try `python` or `py -3` instead (same `-m cursor_storage_reset` pattern).

**`No module named cursor_storage_reset`:** install with **`python3 -m pip install …`** using the **same** `python3` you use to run `-m cursor_storage_reset`.

### Optional: `pipx` (isolated app)

```bash
pipx install cursor-storage-reset
cursor-storage-reset --help
```

### Default `storage.json` locations

| OS      | Path |
|--------|------|
| macOS  | `~/Library/Application Support/Cursor/User/globalStorage/storage.json` |
| Linux  | `$XDG_CONFIG_HOME/Cursor/User/globalStorage/storage.json`, or `~/.config/...` if unset |
| Windows | `%APPDATA%\Cursor\User\globalStorage\storage.json` |

---

## 2. Local development (from a clone)

Use this when you want to edit the code or run tests — **not** required for normal `pip` installs.

```bash
git clone https://github.com/shivanshu814/cursor-storage-reset.git
cd cursor-storage-reset

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest
```

Run the tool from the active venv:

```bash
cursor-storage-reset --help
# or
python -m cursor_storage_reset --help
```

Plain install without dev dependencies:

```bash
pip install -e .
```

### Maintainer: publish to PyPI

1. [pypi.org](https://pypi.org) account + **API token** (keep it secret).
2. Build and upload:

```bash
pip install build twine
python -m build
twine check dist/*
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE twine upload dist/*
```

Or use [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) with this repo’s workflow `.github/workflows/publish-pypi.yml` (GitHub Actions → *Publish Python package to PyPI*).

---

## Python API

```python
from pathlib import Path
from cursor_storage_reset import default_storage_path, refresh_telemetry_ids

refresh_telemetry_ids(Path("/explicit/storage.json"))
print(default_storage_path())
```

## Responsibility

This tool only edits **local** files you choose. Follow Cursor’s terms of service and applicable law.

## Project layout

| Path | Role |
|------|------|
| `src/cursor_storage_reset/paths.py` | Platform default paths |
| `src/cursor_storage_reset/storage.py` | JSON + atomic save + ID generation |
| `src/cursor_storage_reset/cli.py` | CLI |
| `src/cursor_storage_reset/exceptions.py` | Errors |
| `tests/` | Pytest |
