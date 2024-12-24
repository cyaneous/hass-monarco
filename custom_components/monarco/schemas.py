"""Config schemas for the Monarco integration."""

import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.data_entry_flow import section
from homeassistant.helpers.selector import selector

from .const import (
    DEFAULT_SPI_DEVICE,
    DEFAULT_SPI_CLKFREQ,
    DEFAULT_WATCHDOG_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_WATCHDOG_TIMEOUT,
    CONF_UPDATE_INTERVAL,
    CONF_ANALOG_OUTPUT_1,
    CONF_ANALOG_OUTPUT_2,
    CONF_NAME,
    CONF_DEVICE,
    DeviceModel,
)


AO_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_DEVICE, default=DeviceModel.NONE): vol.All(
        str,
        vol.In([DeviceModel.NONE, DeviceModel.LUNOS_E2, DeviceModel.LUNOS_EGO]
    )),
})


CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_SPI_DEVICE, default=DEFAULT_SPI_DEVICE): cv.string,
    vol.Required(CONF_SPI_CLKFREQ, default=DEFAULT_SPI_CLKFREQ): cv.positive_int,
    vol.Required(CONF_WATCHDOG_TIMEOUT, default=DEFAULT_WATCHDOG_TIMEOUT): cv.positive_int,
    vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(float), vol.Range(min=0.05, max=1.0)),
    vol.Required(CONF_ANALOG_OUTPUT_1): section(AO_SCHEMA, {"collapsed": True}),
    vol.Required(CONF_ANALOG_OUTPUT_2): section(AO_SCHEMA, {"collapsed": True}),
}, extra=vol.ALLOW_EXTRA)


OPTIONS_SCHEMA = CONFIG_SCHEMA
