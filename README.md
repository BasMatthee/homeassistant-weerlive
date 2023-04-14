[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# homeassistant-weerlive

## Weerlive custom_component for Home-Assistant

Note: Weerlive is a Dutch weather service. Because of this, only Dutch coordinates provide accurate data. Besides that 
wind directions are written in Dutch: N(oord), O(oost), Z(uid), W(est).

## Installation

If not installed via HACS:
* Copy the files of the `weerlive` directory to your Home Assistant to `{root}/config/custom_components/weerlive/`. 
* Restart your Home Assistant and add the configuration below to your configuration.yaml file in `{root}/config/.
* Validate your YAML configurations and restart Home Assistant once more.
* The enabled sensors should now be available for use. 

## Example configuration (drop this in your configuration.yaml)

After installing the custom component, be sure to add the configuration below to your configuration.yaml.

```yaml
sensor:
  - platform: weerlive
    name: weerlive # Optional. Defaults to weerlive. Only change
    latitude: 50.123456 # Optional. Defaults to your Home Assistants' coordinates.
    longitude: 4.123456 # Optional. Defaults to your Home Assistants' coordinates.
    api_key: { your_api_key } # Read documentation below for more information
    monitored_conditions: # Choose which sensors you want to have available
      - temperature
      - temperature_feels_like
      - wind_direction
      - wind_speed
```

## Available sensors

| Sensor                                 | Description                                    | Format    |
|----------------------------------------|------------------------------------------------|-----------|
| sensor.weerlive.temperature            | The current temperature for the given location | 24.5 °C   |
| sensor.weerlive.temperature_feels_like | How the temperature feels                      | 22.8 °C   |
| sensor.weerlive.wind_direction         | Direction of the wind                          | e.g. NW   |
| sensor.weerlive.wind_speed             | The wind speed                                 | 22.1 km/h |

## Requesting a (free) API key

A free API key can be acquired via [this website](https://weerlive.nl/api/toegang/account.php).
