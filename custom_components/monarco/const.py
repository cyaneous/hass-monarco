"""Constants for the Monarco integration."""

from enum import StrEnum


DOMAIN = "monarco"

DEFAULT_SPI_DEVICE = "0.0"
DEFAULT_SPI_CLKFREQ = 400000
DEFAULT_WATCHDOG_TIMEOUT = 0
DEFAULT_UPDATE_INTERVAL = 1.0

CONF_SPI_DEVICE = "spi_device"
CONF_SPI_CLKFREQ = "spi_clkfreq"
CONF_WATCHDOG_TIMEOUT = "watchdog_timeout"
CONF_UPDATE_INTERVAL = "update_interval"

CONF_ANALOG_OUTPUT_1 = "analog_output_1"
CONF_ANALOG_OUTPUT_2 = "analog_output_2"

CONF_NAME = "name"
CONF_DEVICE = "device"

MANUFACTURER_MONARCO = "Monarco"
MANUFACTURER_LUNOS = "Lunos"

class DeviceModel(StrEnum):
    """Enum representing a device model."""

    NONE = "None"
    LUNOS_E2 = "Lunos e2"
    LUNOS_EGO = "Lunos ego"
