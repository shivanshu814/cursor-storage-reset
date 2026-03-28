"""Domain-specific errors (kept narrow; stdlib errors used where they fit)."""


from __future__ import annotations


class StorageResetError(RuntimeError):
    """Base class for recoverable storage refresh failures."""


class InvalidStorageFile(StorageResetError):
    """Raised when ``storage.json`` is missing, unreadable, or not a JSON object."""
