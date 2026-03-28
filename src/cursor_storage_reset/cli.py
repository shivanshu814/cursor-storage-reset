"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cursor_storage_reset import __version__
from cursor_storage_reset.exceptions import InvalidStorageFile
from cursor_storage_reset.paths import default_storage_path
from cursor_storage_reset.storage import refresh_telemetry_ids


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate Cursor globalStorage telemetry identifiers in storage.json "
            "(atomic write; other keys preserved)."
        ),
    )
    parser.add_argument(
        "storage_path",
        nargs="?",
        type=Path,
        help="Path to storage.json (default: platform-specific Cursor location)",
    )
    parser.add_argument(
        "--print-default",
        action="store_true",
        help="Print the default storage path for this platform and exit",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    default_path = default_storage_path()
    if args.print_default:
        print(default_path)
        return 0

    path = args.storage_path.expanduser() if args.storage_path else default_path

    try:
        updated = refresh_telemetry_ids(path)
    except FileNotFoundError:
        print(
            "Could not find storage.json. Ensure Cursor is installed "
            "or pass an explicit path.",
            file=sys.stderr,
        )
        return 1
    except InvalidStorageFile as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("Success: Cursor telemetry identifiers were reset.")
    print(f"Updated: {updated}")
    print("Restart Cursor for changes to take effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
