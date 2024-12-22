"""Exceptions used by the monarco_hat library."""

__all__ = [
    "MHException",
    "MHConnectionException",
    "MHRuntimeException",
    "MHTimeoutException",
]


class MHException(Exception):
    """Base exception."""

class MHConnectionException(MHException):
    """Exception for runtime errors."""

class MHRuntimeException(MHException):
    """Exception for runtime errors."""


class MHTimeoutException(MHException):
    """Exception for timeouts."""
