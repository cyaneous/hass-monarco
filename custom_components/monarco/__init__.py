"""Monarco home assistant integration."""

import asyncio
from typing import TYPE_CHECKING
import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .monarco_hat import Monarco, MHException, aout_volts_to_u16

from .const import (
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_WATCHDOG_TIMEOUT,
    CONF_UPDATE_INTERVAL,
)
from .models import MHConfigEntryData

_LOGGER = logging.getLogger(__name__)

type MHConfigEntry = ConfigEntry[MHConfigEntryData]

PLATFORMS = [
    Platform.FAN,
]


async def async_setup_entry(hass: HomeAssistant, entry: MHConfigEntry) -> bool:
    """Set up Monarco Fan from a config entry."""

    spi_device: str = entry.data.get(CONF_SPI_DEVICE)
    spi_clkfreq: int = entry.data.get(CONF_SPI_CLKFREQ)
    watchdog_timeout: int = entry.data.get(CONF_WATCHDOG_TIMEOUT)
    update_interval: int = entry.data.get(CONF_UPDATE_INTERVAL)

    if TYPE_CHECKING:
        assert spi_device is not None
        assert spi_clkfreq is not None
        assert watchdog_timeout is not None

    try:
        monarco = Monarco(spi_device, spi_clkfreq)
        # TODO: set watchdog timeout, make sure short values are disallowed
    except MHException as ex:
        raise ConfigEntryNotReady(f"Failed to initialize the Monarco HAT: {ex}") from ex

    entry.runtime_data = MHConfigEntryData(monarco=monarco)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_create_background_task(
        hass, _async_run_monarco(hass, entry, update_interval), entry.entry_id
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: MHConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def update_listener(hass: HomeAssistant, entry: MHConfigEntry) -> None:
    """Handle config entry update."""

    entry.runtime_data.monarco.close()
    await hass.config_entries.async_reload(entry.entry_id)

async def _async_run_monarco(hass: HomeAssistant, entry: MHConfigEntry, update_interval: float) -> None:
    """Run the monarco update loop."""

    monarco = entry.runtime_data.monarco

    while True:
        try:
            monarco.run()
        except MHException as ex:
            _LOGGER.error("Exception caught in monarco run loop: %s", ex)

        await asyncio.sleep(update_interval) # 100 ms is max to keep the watchdog happy if its on
