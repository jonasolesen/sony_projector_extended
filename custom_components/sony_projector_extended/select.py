import logging

from pysdcp import Projector, ACTIONS, COMMANDS

from homeassistant.components.select import SelectEntity
from homeassistant.components.sony_projector_extended.const import ASPECT_RATIOS, DOMAIN, CALIBRATION_PRESETS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    projector: Projector = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[SelectEntity] = [
        AspectRatioSelect(
            projector=projector,
            name=f"{config_entry.title} - Aspect ratio",
            unique_id=f"{config_entry.unique_id}.aspect_ratio"
        ),
        CalibrationPresetSelect(
            projector=projector,
            name=f"{config_entry.title} - Calibration preset",
            unique_id=f"{config_entry.unique_id}.calibration_preset"
        ),
    ]
    hass.data[DOMAIN]["selects"] = entities
    async_add_entities(entities, True)


class AspectRatioSelect(SelectEntity):
    _attr_icon = "mdi:aspect-ratio"

    def __init__(self, projector: Projector, unique_id: str, name: str) -> None:
        """Initialize the aspect ratio select entity."""
        self._projector = projector
        self._attr_available = self._projector.get_power() or False
        self._attr_unique_id = unique_id
        self._attr_name = name or "Aspect ratio"
        self._attr_current_option = self.update()
        self._attr_options = list(ASPECT_RATIOS)
        # self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, unique_id)}, name=name)

    def update(self) -> str | None:
        if not self._attr_available:
            return

        try:
            aspect_ratio = self._projector._send_command(ACTIONS['GET'], COMMANDS['ASPECT_RATIO'])
            return next(key for key, value in ASPECT_RATIOS.items() if value == aspect_ratio) or None
        except BaseException:
            return None

    def select_option(self, option: str) -> None:
        if option not in ASPECT_RATIOS:
            raise BaseException

        self._attr_current_option = option
        try:
            self._projector._send_command(ACTIONS["SET"], COMMANDS["ASPECT_RATIO"], ASPECT_RATIOS[option])
        except BaseException:
            _LOGGER.error('Could not set aspect ratio')


class CalibrationPresetSelect(SelectEntity):
    _attr_icon = "mdi:panorama-outline"

    def __init__(self, projector: Projector, unique_id: str, name: str) -> None:
        """Initialize the calibration preset select entity."""
        self._projector = projector
        self._attr_available = self._projector.get_power() or False
        self._attr_unique_id = unique_id
        self._attr_name = name or "Calibration preset"
        self._attr_current_option = self.update()
        self._attr_options = list(CALIBRATION_PRESETS)

    def update(self) -> str | None:
        if not self._attr_available:
            return

        try:
            calibration_preset = self._projector._send_command(ACTIONS['GET'], COMMANDS['CALIBRATION_PRESET'])
            return next(key for key, value in CALIBRATION_PRESETS.items() if value == calibration_preset) or None
        except BaseException:
            return None

    def select_option(self, option: str) -> None:
        if option not in CALIBRATION_PRESETS:
            raise BaseException

        self._attr_current_option = option
        try:
            self._projector._send_command(ACTIONS["SET"], COMMANDS["CALIBRATION_PRESET"], CALIBRATION_PRESETS[option])
        except BaseException:
            _LOGGER.error('Could not set calibration preset')
