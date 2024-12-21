"""Fan entity for the Monarco integration."""

from typing import Optional, Any
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.fan import FanEntity, OSCILLATE, SUPPORT_PERCENTAGE, TURN_ON, TURN_OFF
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import ranged_value_to_percentage, percentage_to_ranged_value
from homeassistant.util.scaling import int_states_in_range

#from .monarco_hat.monarco import MonarcoContext, monarco_init, monarco_main, monarco_exit
#from .monarco_hat import monarco_util

from . import MHConfigEntry
from .const import (
    CONF_NAME,
    CONF_FANS,
    CONF_OUTPUT,
    MANUFACTURER_LUNOS,
    DEVICE_MODEL_LUNOS_E2,
    DEVICE_MODEL_LUNOS_EGO,
)

_LOGGER = logging.getLogger(__name__)

SPEED_RANGE = (1, 5)  # off is not included


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MHConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up the Monarco Fan platform."""

    config = config_entry.data
    # spi_device = config.get(CONF_SPI_DEVICE)
    # spi_clkfreq = config.get(CONF_SPI_CLKFREQ)
    # platform = "Linux"

    monarco = []
    # monarco = config_entry.monarco # MonarcoContext()

    fans = []
    for fan_conf in config.get(CONF_FANS):
        name = fan_conf.get(CONF_NAME)
        output = fan_conf.get(CONF_OUTPUT)
        fans.append(LunosFan(name, monarco, output))

    async_add_entities(fans)

class LunosFan(FanEntity):
    """Fan entity represneting a Lunos fan."""

    _attr_entity_has_name = True
    _attr_name = None
    _attr_should_poll = False

    _attr_supported_features = (OSCILLATE, SUPPORT_PERCENTAGE, TURN_OFF, TURN_ON)
    _attr_is_on = False
    _attr_percentage = 0
    _attr_oscillating = False

    # FIXME: monarco: Monarco
    def __init__(self, name: str, monarco: Any, output: int) -> None:
        """Initialize the fan."""

        self._monarco = monarco
        self._attr_unique_id = f"lunos_fan_{output}"
        self._attr_device_info = DeviceInfo(
            name=f"{MANUFACTURER_LUNOS} {DEVICE_MODEL_LUNOS_E2} {output}",
            manufacturer=MANUFACTURER_LUNOS,
            model=DEVICE_MODEL_LUNOS_E2,
        )

    async def async_turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
        """Turn on the fan."""

    #     if speed is not None:
    #         self.set_percentage(speed)
    #     else:
    #         self.set_percentage(100)  # Full speed
    #     self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the fan."""

    #     self.set_percentage(0)
    #     self._attr_is_on = False

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""

        # percentage = ranged_value_to_percentage(SPEED_RANGE, 127)
        # value_in_range = math.ceil(percentage_to_ranged_value(SPEED_RANGE, 50))

        # _attr_percentage = percentage
        # voltage = (speed / 255.0) * 10.0  # Convert speed (0-255) to voltage (0-10V)
        # voltage_u16 = monarco_util.aout_volts_to_u16(voltage)
        # if self._output == 1:
        #     self._cxt.tx_data.aout1 = voltage_u16
        # elif self._output == 2:
        #     self._cxt.tx_data.aout2 = voltage_u16
        # monarco_main(self._cxt)

    async def async_oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""

        # ...

    async def async_update(self):
        """Fetch new state data for the fan."""

        # monarco_main(self._cxt)
