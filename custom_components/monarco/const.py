"""Constants for the Monarco integration."""

from enum import StrEnum


DOMAIN = "monarco"

DEFAULT_SPI_DEVICE = "0.0"
DEFAULT_SPI_CLKFREQ = 400000
DEFAULT_WATCHDOG_TIMEOUT = 0

CONF_SPI_DEVICE = "spi_device"
CONF_SPI_CLKFREQ = "spi_clkfreq"
CONF_WATCHDOG_TIMEOUT = "watchdog_timeout"

CONF_AO1_NAME = "analog_output_1_name"
CONF_AO1_DEVICE = "analog_output_1_device"
CONF_AO2_NAME = "analog_output_2_name"
CONF_AO2_DEVICE = "analog_output_2_device"

MANUFACTURER_MONARCO = "Monarco"
MANUFACTURER_LUNOS = "Lunos"

class DeviceModel(StrEnum):
    """Enum representing a device model."""

    NONE = "None"
    LUNOS_E2 = "Lunos e2"
    LUNOS_EGO = "Lunos ego"
