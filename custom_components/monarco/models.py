"""Models for the monarco integration."""

from dataclasses import dataclass

#from .monarco_hat.monarco import Monarco

from .const import DEFAULT_SPI_DEVICE, DEFAULT_SPI_CLKFREQ


@dataclass(slots=True)
class MHConfig:
    """Config for a single monarco entity."""

    spi_device: str = DEFAULT_SPI_DEVICE
    spi_clkfreq: int = DEFAULT_SPI_CLKFREQ


@dataclass(slots=True)
class MHConfigEntryData:
    """Config entry for a single monarco entity."""

    mh_config: MHConfig
    #monarco: Monarco
