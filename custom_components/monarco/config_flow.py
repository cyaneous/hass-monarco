"""Configuratiion flow for the Monarco integration."""

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, CONN_CLASS_LOCAL_PUSH, HANDLERS
from homeassistant.data_entry_flow import FlowHandler
from homeassistant.core import callback

from . import schemas
from .const import DOMAIN


@HANDLERS.register(DOMAIN)
class MonarcoConfigFlow(FlowHandler):
    """Handle a config flow for the Monarco integration."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""

        if user_input is not None:
            return self.async_create_entry(title="Monarco", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=schemas.CONFIG_SCHEMA
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MonarcoFanOptionsFlowHandler(config_entry)

class MonarcoFanOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an option flow for the Monarco integration."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Manage the options."""

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=schemas.OPTIONS_SCHEMA
        )
