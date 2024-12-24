"""Configuratiion flow for the Monarco integration."""

from typing import Any
from collections.abc import Mapping
import copy
import logging

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
    FlowResult,
)
from homeassistant.data_entry_flow import section

from . import schemas
from .const import (
    DOMAIN,
    CONF_SPI_DEVICE,
    CONF_SPI_CLKFREQ,
    CONF_WATCHDOG_TIMEOUT,
    CONF_UPDATE_INTERVAL,
    CONF_ANALOG_OUTPUT_1,
    CONF_ANALOG_OUTPUT_2,
    CONF_NAME,
    CONF_DEVICE,
    MANUFACTURER_LUNOS,
    DeviceModel,
)

_LOGGER = logging.getLogger(__name__)


class MonarcoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Monarco integration."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""

        if user_input is not None:
            await self.async_set_unique_id("monarco")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Monarco", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=schemas.CONFIG_SCHEMA
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""

        return MonarcoOptionsFlow()


class MonarcoOptionsFlow(OptionsFlow):
    """Handle an option flow for the Monarco integration."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the options."""

        if user_input is not None:
            # write updated config entries
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input, options=self.config_entry.options
            )

            # reload updated config entries
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            self.async_abort(reason="Configuration updated.")

            # write empty options entries
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                schemas.OPTIONS_SCHEMA, self.config_entry.data
            )
        )
