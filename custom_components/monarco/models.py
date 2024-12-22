"""Models for the monarco integration."""

from dataclasses import dataclass

from .monarco_hat import Monarco


@dataclass(slots=True)
class MHConfigEntryData:
    """Config entry for a single monarco entity."""

    monarco: Monarco
