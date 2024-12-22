"""Fan entity for the Monarco integration."""

from typing import Optional, Any
import math
import logging

from homeassistant.core import HomeAssistant
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util.percentage import ranged_value_to_percentage, percentage_to_ranged_value
from homeassistant.util.scaling import int_states_in_range

from .monarco_hat import Monarco, aout_volts_to_u16

from . import MHConfigEntry
from .const import (
    DOMAIN,
    CONF_AO1_NAME,
    CONF_AO1_DEVICE,
    CONF_AO2_NAME,
    CONF_AO2_DEVICE,
    MANUFACTURER_LUNOS,
    DEVICE_MODEL_LUNOS_E2,
    DEVICE_MODEL_LUNOS_EGO,
)

_LOGGER = logging.getLogger(__name__)

SPEED_RANGE = (1, 8)  # off is not included

class LUNOS_FAN_V:
    AUTO = 0.0    # 0.0 - 0.4 (the controller works independently, according to internal sensors)
    STAGE_0 = 0.7 # 0.6 - 0.9 (off)
    STAGE_1 = 1.2 # 1.1 - 1.4
    STAGE_2 = 1.7 # 1.6 - 1.9
    STAGE_3 = 2.2 # 2.1 - 2.4
    STAGE_4 = 2.7 # 2.6 - 2.9
    STAGE_5 = 3.2 # 3.1 - 3.4
    STAGE_6 = 3.7 # 3.6 - 3.9
    STAGE_7 = 4.2 # 4.1 - 4.4
    STAGE_8 = 4.7 # 4.6 - 4.9
    SUMMER_OFFSET = 5.0

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MHConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up the Monarco Fan platform."""

    config = config_entry.data
    monarco = config_entry.runtime_data.monarco

    fans = []

    name = config.get(CONF_AO1_NAME)
    device = config.get(CONF_AO1_DEVICE)
    if device in (DEVICE_MODEL_LUNOS_E2, DEVICE_MODEL_LUNOS_EGO):
        fan = LunosFan(name, device, monarco, 1)
        fans.append(fan)

    name = config.get(CONF_AO2_NAME)
    device = config.get(CONF_AO2_DEVICE)
    if device in (DEVICE_MODEL_LUNOS_E2, DEVICE_MODEL_LUNOS_EGO):
        fan = LunosFan(name, device, monarco, 2)
        fans.append(fan)

    async_add_entities(fans)

class LunosFan(FanEntity):
    """Fan entity represneting a Lunos fan."""

    _attr_entity_has_name = True
    _attr_name = None
    _attr_should_poll = False

    _attr_supported_features = (
        FanEntityFeature.OSCILLATE
        | FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
    )
    _attr_percentage = 0
    _attr_oscillating = False

    def __init__(self, name: str, model: str, monarco: Monarco, output: int) -> None:
        """Initialize the fan."""

        self._monarco = monarco
        self._output = output
        self._attr_unique_id = f"lunos_fan_{output}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            name=name,
            manufacturer=MANUFACTURER_LUNOS,
            model=model,
            identifiers={(DOMAIN, f"AO{output}")},
        )
        
        self._update_output()


    async def async_turn_on(
        self,
        speed: Optional[str] = None,
        percentage: Optional[int] = None,
        preset_mode: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Turn on the fan."""

        if percentage is not None:
            await self.async_set_percentage(percentage)
        else:
            await self.async_set_percentage(100)

        #self._attr_is_on = True
        # self.async_write_ha_state()
        # self._update_output()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the fan."""

        await self.async_set_percentage(0)
        # self._attr_is_on = False
        # self.async_write_ha_state()
        # self._update_output()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""

        self._attr_percentage = percentage
        self.async_write_ha_state()
        self._update_output()

    async def async_oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""

        self._attr_oscillating = oscillating
        self.async_write_ha_state()
        self._update_output()

    def _update_output(self) -> None:
        volts = LUNOS_FAN_V.STAGE_0
        if self.is_on:
            value_in_range = math.ceil(percentage_to_ranged_value(SPEED_RANGE, self.percentage))

            _LOGGER.error("value in range: %i", value_in_range)
            match value_in_range:
                case 0: 
                    volts = LUNOS_FAN_V.AUTO
                case 1:
                    volts = LUNOS_FAN_V.STAGE_1
                case 2:
                    volts = LUNOS_FAN_V.STAGE_2
                case 3:
                    volts = LUNOS_FAN_V.STAGE_3
                case 4:
                    volts = LUNOS_FAN_V.STAGE_4
                case 5:
                    volts = LUNOS_FAN_V.STAGE_5
                case 6:
                    volts = LUNOS_FAN_V.STAGE_6
                case 7:
                    volts = LUNOS_FAN_V.STAGE_7
                case 8:
                    volts = LUNOS_FAN_V.STAGE_8

            if not self.oscillating and volts >= LUNOS_FAN_V.STAGE_1:
                volts += LUNOS_FAN_V.SUMMER_OFFSET

        self._set_voltage(volts)

    def _set_voltage(self, volts) -> None:
        _LOGGER.error("setting volts: %i", volts)

        match self._output:
            case 1:
                _LOGGER.error("output 1")
                self._monarco._tx_data.aout1 = aout_volts_to_u16(volts)
            case 2:
                _LOGGER.error("output 2")
                self._monarco._tx_data.aout2 = aout_volts_to_u16(volts)
