# Alarmo Sensors

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/vincekruger)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-Support-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/vince)

Expose one sensor for each arm mode enabled in Alarmo: Away, Home, Night,
Holiday, Custom Bypass, or any additional mode supplied by Alarmo.
Each state counts enabled inputs assigned to that mode, including always-on
inputs, and its `sensors` attribute lists their entity IDs.

Mode settings are read from Alarmo's areas. Each mode sensor combines inputs only
from areas where that mode is enabled. The `mode` and `areas` attributes identify
the source configuration. Counts describe configured inputs, not open contacts.

Enabling a new mode creates its entity automatically. Disabling it in every area
makes its entity unavailable and clears its list. Re-enabling it restores the
same entity. Updates do not require a restart after the integration is loaded.
The existing Away sensor keeps its unique ID and entity registration.

## Requirements

Home Assistant 2024.6 or later and an installed, configured Alarmo integration.
Validated locally against Home Assistant 2026.9.4; earlier versions are not tested.

## Installation

### 1. Install through HACS

Make sure [HACS](https://www.hacs.xyz/docs/use/download/download/) is installed
and Alarmo is already configured in Home Assistant.

Click the button below to open **Alarmo Sensors** in HACS on your Home Assistant
instance:

[![Open Alarmo Sensors in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=vincekruger&repository=alarmo-sensors&category=integration)

If prompted by My Home Assistant, enter the URL of your Home Assistant instance.
In HACS, select **Download** and confirm the installation.

To add the repository manually:

1. Open **HACS** in Home Assistant.
2. Open the **⋮** menu in the top-right corner and select **Custom repositories**.
3. Enter `https://github.com/vincekruger/alarmo-sensors` as the repository URL.
4. Select **Integration** as the type and click **Add**.
5. Search for **Alarmo Sensors**, open its repository page, and select **Download**.

### 2. Restart Home Assistant

Restart Home Assistant after downloading the integration so it can load the new
files. A browser refresh alone does not load the integration.

### 3. Add the integration in Devices & services

Installing through HACS downloads the files. Complete setup by adding the
integration to Home Assistant:

1. Open **Settings → Devices & services**.
2. On the **Integrations** tab, select **Add integration**.
3. Search for **Alarmo Sensors** and select it to complete setup.

You can also start this step with the button below after restarting:

[![Add Alarmo Sensors to Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=alarmo_sensors)

Alarmo Sensors creates an entity for each mode enabled in Alarmo. Enable at least
one mode and configure its sensor assignments in Alarmo, then use the dashboard
examples below to display the results. Later mode and assignment changes update
automatically.

Only one Alarmo Sensors integration instance is needed. Setup retries if Alarmo
is not ready yet. No YAML sensor configuration is required; remove any old
`platform: alarmo_sensors` entry from `configuration.yaml`.

### Manual installation

As an alternative to HACS, copy the entire `custom_components/alarmo_sensors`
folder from this repository into your Home Assistant configuration directory at
`/config/custom_components/alarmo_sensors`.

Then follow **Step 2: Restart Home Assistant** and **Step 3: Add the integration
in Devices & services** above.

## Dashboard examples

Open your dashboard, select **Edit dashboard → Add card → Manual**, and paste
one of the examples below.

### All enabled modes: Markdown card

This built-in card lists every available mode, its configured sensor count, and
the current state of each input. Newly enabled modes appear automatically;
disabled modes are hidden. No additional dashboard plugin is required.

```yaml
type: markdown
title: Alarmo sensors
content: |
  {% for mode in states.sensor
      if mode.attributes.mode is defined
      and mode.attributes.sensors is defined
      and mode.state not in ['unknown', 'unavailable'] %}
  ### {{ mode.name }}
  **{{ mode.state }} sensors**
  {% for entity in mode.attributes.sensors %}
  - {{ state_attr(entity, 'friendly_name') or entity }} — {{ states(entity) }}
  {% else %}
  No sensors configured.
  {% endfor %}
  {% else %}
  No Alarmo modes enabled.
  {% endfor %}
```

This example displays raw input states such as `on` and `off`.

### One mode: dynamic Entities card

Install [Auto Entities](https://github.com/thomasloven/lovelace-auto-entities)
through HACS first. This example turns the Away sensor's `sensors` attribute into
clickable entity rows with icons and current states, such as **Open** or
**Closed** for door sensors.

```yaml
type: custom:auto-entities
card:
  type: entities
  title: Away sensors
  show_header_toggle: false
filter:
  template: >
    {{ state_attr('sensor.alarmo_away_sensors', 'sensors') or [] }}
show_empty: false
sort:
  method: name
```

Rows update automatically when you change sensor assignments in Alarmo. The
card is hidden when its list is empty, including when the mode is disabled.
For another mode, replace `sensor.alarmo_away_sensors` with that mode's actual
entity ID and change the title. Check entity IDs under **Developer tools →
States**; Home Assistant may use a different ID if an entity was renamed or a
name was already taken.

For a compact icon layout, change the inner card's `type: entities` to
`type: glance` and remove `show_header_toggle`.

## License

Released under the [MIT License](LICENSE).
