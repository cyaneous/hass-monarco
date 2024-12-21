"""Config schemas for the Monarco integration."""

import voluptuous as vol

from homeassistant.helpers import config_validation as cv

from .const import (
    DEFAULT_SPI_DEVICE,
    DEFAULT_SPI_CLKFREQ,
    CONF_NAME,
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_FANS,
    CONF_OUTPUT,
)


FAN_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_OUTPUT): vol.All(vol.Coerce(int), vol.Range(min=1, max=2))
})


CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_SPI_DEVICE, default=DEFAULT_SPI_DEVICE): cv.string,
    vol.Required(CONF_SPI_CLKFREQ, default=DEFAULT_SPI_CLKFREQ): cv.positive_int,
    vol.Required(CONF_FANS): vol.All(cv.ensure_list, [FAN_SCHEMA])
}, extra=vol.ALLOW_EXTRA)


OPTIONS_SCHEMA = vol.Schema({
    vol.Required(CONF_SPI_DEVICE, default=DEFAULT_SPI_DEVICE): cv.string,
    vol.Required(CONF_SPI_CLKFREQ, default=DEFAULT_SPI_CLKFREQ): cv.positive_int,
    vol.Required(CONF_FANS): vol.All(cv.ensure_list, [FAN_SCHEMA])
})
