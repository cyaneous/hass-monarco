"""Monarco home assistant integration."""

import asyncio
import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    DOMAIN,
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_WATCHDOG_TIMEOUT,
)
from .models import MHConfig, MHConfigEntryData

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

    # if TYPE_CHECKING:
    #     assert spi_device is not None
    #     assert spi_clkfreq is not None
    #     assert watchdog_timeout is not None

    # cxt = MonarcoContext()
    # monarco_init(cxt, spi_device, spi_clkfreq, "Linux")

    # if device is None:
    #     raise ConfigEntryNotReady(f"Failed to initialize the Monarco HAT")

    #hass.data.setdefault(DOMAIN, {})

    # entry.runtime_data = MAConfigEntryData(
    #     ma_config=ma_config,
    #     thermostat=thermostat
    # )
    
    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # entry.async_create_background_task(
    #     hass, _async_run_monarco(hass, entry), entry.entry_id
    # )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: MHConfigEntry) -> bool:
    """Unload a config entry."""
    
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True

async def update_listener(hass: HomeAssistant, entry: MHConfigEntry) -> None:
    """Handle config entry update."""

    await hass.config_entries.async_reload(entry.entry_id)

async def _async_run_monarco(hass: HomeAssistant, entry: MHConfigEntry) -> None:
    """Run the monarco update loop."""

    # monarco = entry.runtime_data.monarco
    # mac_address = entry.runtime_data.ma_config.mac_address
    # scan_interval = entry.runtime_data.ma_config.scan_interval

    # while True:
    #     try:
    #         # async with thermostat:
    #         #     await thermostat.async_get_status()
    #     except MHException as ex:
    #         _LOGGER.error("Exception caught in monarco loop: %s", ex)

    #     await asyncio.sleep(1)
