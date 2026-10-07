"""Expose Alarmo sensor configuration through Home Assistant."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.alarmo.const import DOMAIN as ALARMO_DOMAIN

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration once Alarmo's coordinator is available."""
    if hass.data.get(ALARMO_DOMAIN, {}).get("coordinator") is None:
        raise ConfigEntryNotReady("Alarmo is not ready; configure Alarmo first")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entities and their dispatcher subscriptions."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
