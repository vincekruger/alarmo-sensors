from homeassistant.components.sensor import SensorEntity
from homeassistant.components.alarm_control_panel import AlarmControlPanelState
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from custom_components.alarmo import const
from custom_components.alarmo.sensors import ATTR_ALWAYS_ON


async def async_setup_platform(
    hass,
    config,
    async_add_entities,
    discovery_info=None,
):
    async_add_entities([AlarmoAwaySensors(hass)])


class AlarmoAwaySensors(SensorEntity):
    _attr_name = "Alarmo Away Sensors"
    _attr_unique_id = "alarmo_away_sensors"

    def __init__(self, hass):
        self.hass = hass

    @property
    def _sensors(self):
        configs = (
            self.hass.data[const.DOMAIN]["coordinator"]
            .store.async_get_sensors()
            or {}
        )

        return [
            entity_id
            for entity_id, config in configs.items()
            if config["enabled"]
            and (
                AlarmControlPanelState.ARMED_AWAY in config[const.ATTR_MODES]
                or config[ATTR_ALWAYS_ON]
            )
        ]

    @property
    def native_value(self):
        return len(self._sensors)

    @property
    def extra_state_attributes(self):
        return {
            "sensors": self._sensors,
        }

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                "alarmo_sensors_updated",
                self._handle_alarmo_update,
            )
        )

    def _handle_alarmo_update(self):
        self.async_write_ha_state()