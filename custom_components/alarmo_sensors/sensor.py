"""Expose sensor lists for the arm modes enabled in Alarmo."""

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.alarmo import const as alarmo_const
from custom_components.alarmo.sensors import ATTR_ALWAYS_ON

from .const import SIGNAL_SENSORS_UPDATED

SIGNAL_CONFIG_UPDATED = "alarmo_config_updated"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Discover enabled modes and follow subsequent configuration changes."""
    manager = AlarmoModeSensors(hass, async_add_entities)
    for signal in (SIGNAL_CONFIG_UPDATED, SIGNAL_SENSORS_UPDATED):
        entry.async_on_unload(
            async_dispatcher_connect(hass, signal, manager.async_refresh)
        )
    manager.async_refresh()


class AlarmoModeSensors:
    """Keep one entity per mode, aggregating its enabled Alarmo areas."""

    def __init__(self, hass: HomeAssistant, add_entities: AddEntitiesCallback) -> None:
        self.hass = hass
        self._add_entities = add_entities
        self.entities: dict[str, AlarmoModeSensor] = {}

    @callback
    def async_refresh(self, *_args: Any) -> None:
        """Reconcile entities and update snapshots on the event loop."""
        coordinator = self.hass.data.get(alarmo_const.DOMAIN, {}).get("coordinator")
        areas = coordinator.store.async_get_areas() if coordinator else {}
        configs = coordinator.store.async_get_sensors() if coordinator else {}
        enabled: dict[str, set[str]] = {}
        for area_id, area in (areas or {}).items():
            for mode, settings in (area.get(alarmo_const.ATTR_MODES) or {}).items():
                if settings.get("enabled", False):
                    enabled.setdefault(mode, set()).add(area_id)

        new_entities = []
        for mode in enabled:
            if mode not in self.entities:
                entity = self.entities[mode] = AlarmoModeSensor(mode)
                new_entities.append(entity)

        for mode, entity in self.entities.items():
            area_ids = enabled.get(mode, set())
            sensor_ids = [
                entity_id
                for entity_id, config in (configs or {}).items()
                if config.get("enabled", False)
                and config.get("area") in area_ids
                and (
                    mode in (config.get(alarmo_const.ATTR_MODES) or [])
                    or config.get(ATTR_ALWAYS_ON, False)
                )
            ]
            entity.async_set_snapshot(sensor_ids, bool(area_ids), sorted(area_ids))
            if entity.entity_id is not None:
                entity.async_write_ha_state()

        if new_entities:
            self._add_entities(new_entities)


class AlarmoModeSensor(SensorEntity):
    """Count configured inputs for one enabled Alarmo arm mode."""

    _attr_should_poll = False
    _attr_icon = "mdi:shield-home"

    def __init__(self, mode: str) -> None:
        self._mode = mode
        suffix = mode.removeprefix("armed_")
        label = "Holiday" if suffix == "vacation" else suffix.replace("_", " ").title()
        self._attr_name = f"Alarmo {label} Sensors"
        self._attr_unique_id = f"alarmo_{suffix}_sensors"
        self._attr_native_value = 0
        self._attr_available = False
        self._sensor_ids: list[str] = []
        self._area_ids: list[str] = []

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the counted entity IDs, mode and participating areas."""
        return {
            "sensors": list(self._sensor_ids),
            "mode": self._mode,
            "areas": list(self._area_ids),
        }

    @callback
    def async_set_snapshot(
        self, sensor_ids: list[str], available: bool, area_ids: list[str]
    ) -> None:
        """Keep the count and attributes consistent."""
        self._sensor_ids = sensor_ids
        self._area_ids = area_ids
        self._attr_native_value = len(sensor_ids)
        self._attr_available = available
