# Alarmo Sensors

A small Home Assistant custom integration that exposes sensors configured in [Alarmo](https://github.com/nielsfaber/alarmo) as Home Assistant sensor entities.

## Features

Currently provides:

### `sensor.alarmo_away_sensors`

The state contains the number of sensors configured for Alarmo's **Away** mode.

The `sensors` attribute contains the corresponding Home Assistant entity IDs.

Example:

```yaml
state: 2
attributes:
  sensors:
    - binary_sensor.office_door_contact
    - binary_sensor.terrace_door_contact
```

The entity automatically updates when the Alarmo sensor configuration changes.

## Requirements

- Home Assistant
- Alarmo

## Installation with HACS

1. Open HACS.
2. Add this repository as a custom repository.
3. Select **Integration** as the repository type.
4. Install **Alarmo Sensors**.
5. Restart Home Assistant.

Add the following to `configuration.yaml`:

```yaml
sensor:
  - platform: alarmo_sensors
```

Restart Home Assistant.

## Manual Installation

Copy:

```text
custom_components/alarmo_sensors
```

to:

```text
/config/custom_components/alarmo_sensors
```

Add the following to `configuration.yaml`:

```yaml
sensor:
  - platform: alarmo_sensors
```

Restart Home Assistant.

## License

MIT
