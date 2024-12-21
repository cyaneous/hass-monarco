"""Exceptions used by the monarco_hat library."""

__all__ = [
    "MHException",
    "MHConnectionException",
    "MHTimeoutException",
    "MHStateException",
    "MHInternalException",
]


class MHException(Exception):
    """Base exception."""


class MHConnectionException(MHException):
    """Exception for connection errors."""


class MHTimeoutException(MHException):
    """Exception for timeouts."""


class MHStateException(MHException):
    """Exception for invalid states."""


class MHInternalException(MHException):
    """Exception for internal errors."""
