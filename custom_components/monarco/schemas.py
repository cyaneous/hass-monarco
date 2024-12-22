"""Config schemas for the Monarco integration."""

import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.data_entry_flow import section
from homeassistant.helpers.selector import selector

from .const import (
    DEFAULT_SPI_DEVICE,
    DEFAULT_SPI_CLKFREQ,
    DEFAULT_WATCHDOG_TIMEOUT,
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_WATCHDOG_TIMEOUT,
    CONF_AO1_NAME,
    CONF_AO1_DEVICE,
    CONF_AO2_NAME,
    CONF_AO2_DEVICE,
    DEVICE_MODEL_NONE,
    DEVICE_MODEL_LUNOS_E2,
    DEVICE_MODEL_LUNOS_EGO,
)


AO1_SCHEMA = vol.Schema({
    vol.Required(CONF_AO1_NAME): cv.string,
    CONF_AO1_DEVICE: selector({
        "select": {
            "options": [DEVICE_MODEL_NONE, DEVICE_MODEL_LUNOS_E2, DEVICE_MODEL_LUNOS_EGO]
        }
    })
})

AO2_SCHEMA = vol.Schema({
    vol.Required(CONF_AO2_NAME): cv.string,
    CONF_AO2_DEVICE: selector({
        "select": {
            "options": [DEVICE_MODEL_NONE, DEVICE_MODEL_LUNOS_E2, DEVICE_MODEL_LUNOS_EGO]
        }
    })
})

# TODO: add note about watchdog: The Raspberry Pi will be power-cycled by the watchdog after this many seconds of timeout. Set to zero to disable.

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_SPI_DEVICE, default=DEFAULT_SPI_DEVICE): cv.string,
    vol.Required(CONF_SPI_CLKFREQ, default=DEFAULT_SPI_CLKFREQ): cv.positive_int,
    vol.Required(CONF_WATCHDOG_TIMEOUT, default=DEFAULT_WATCHDOG_TIMEOUT): cv.positive_int,
    "analog_output_1": section(
        AO1_SCHEMA,
        {"collapsed": True},
    ),
    "analog_output_2": section(
        AO2_SCHEMA,
        {"collapsed": True},
    ),
}, extra=vol.ALLOW_EXTRA)


# OPTIONS_SCHEMA = vol.Schema({
#     vol.Required(CONF_SPI_DEVICE, default=DEFAULT_SPI_DEVICE): cv.string,
#     vol.Required(CONF_SPI_CLKFREQ, default=DEFAULT_SPI_CLKFREQ): cv.positive_int,
# })

OPTIONS_SCHEMA = CONFIG_SCHEMA
