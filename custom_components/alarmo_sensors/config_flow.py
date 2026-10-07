"""Config flow for Alarmo Sensors."""

from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class AlarmoSensorsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Allow a single Alarmo Sensors instance."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Create the entry without requiring user configuration."""
        self._async_abort_entries_match()
        return self.async_create_entry(title="Alarmo Sensors", data={})
