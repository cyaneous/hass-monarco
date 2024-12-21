"""Monarco home assistant integration."""

import asyncio
import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_NAME, CONF_SPI_DEVICE, CONF_SPI_CLKFREQ, CONF_FANS
from .models import MHConfig, MHConfigEntryData

_LOGGER = logging.getLogger(__name__)

type MHConfigEntry = ConfigEntry[MHConfigEntryData]

PLATFORMS = [
    Platform.FAN,
]


async def async_setup_entry(hass: HomeAssistant, entry: MHConfigEntry) -> bool:
    """Set up Monarco Fan from a config entry."""
    
    # mac_address: str = entry.unique_id
    # pin: str = entry.data.get("pin")

    # if TYPE_CHECKING:
    #     assert mac_address is not None
    #     assert pin is not None

    # ma_config = MHConfig(
    #     mac_address=mac_address,
    #     pin=pin
    # )
    
    hass.data.setdefault(DOMAIN, {})
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    
    spi_device = entry.data.get(CONF_SPI_DEVICE)
    spi_clkfreq = entry.data.get(CONF_SPI_CLKFREQ)

    # cxt = MonarcoContext()
    # monarco_init(cxt, spi_device, spi_clkfreq, "Linux")
    
    # entry.async_create_background_task(
    #     hass, _async_run_monarco(hass, entry), entry.entry_id
    # )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: MHConfigEntry) -> bool:
    """Unload a config entry."""
    
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True

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
