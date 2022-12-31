import logging

from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature, MediaPlayerState
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pysdcp import Projector, ACTIONS, COMMANDS

from . import DOMAIN
from .const import DEFAULT_SOURCES
from .select import CalibrationPresetSelect, AspectRatioSelect

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Connect to Sony projector using network."""

    projector: Projector = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        SonyProjectorMediaPlayer(
            projector=projector, name=config_entry.title, unique_id=config_entry.unique_id, entry=config_entry,
            selects=hass.data[DOMAIN]["selects"] or []
        ),
    ], True)


class SonyProjectorMediaPlayer(MediaPlayerEntity):
    """Representation of Sony Projector Device."""

    _attr_supported_features = (
            MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(
            self,
            projector: Projector,
            name: str,
            unique_id: str | None,
            entry: ConfigEntry,
            selects: list[CalibrationPresetSelect | AspectRatioSelect]
    ) -> None:
        self._projector = projector
        self._entry = entry
        self._attr_name = name
        self._attr_available = False
        self._attr_unique_id = unique_id
        self._attr_selects = selects
        self._attr_source_list = list(DEFAULT_SOURCES.keys())
        self._attr_aspect_ratio = None

    async def async_update(self) -> None:
        """Update state of device."""

        try:
            power_state = self._projector.get_power()
        except BaseException:
            self._attr_available = False
            return

        if not power_state:
            self._attr_state = MediaPlayerState.OFF
            self._attr_available = True
            for select in self._attr_selects:
                select._attr_available = False

            return
        _LOGGER.debug("Projector status: %s", power_state)

        for select in self._attr_selects:
            select._attr_available = True
            select._attr_current_option = select.update()

        self._attr_available = True
        self._attr_state = MediaPlayerState.ON

        try:
            source_hex = self._projector._send_command(ACTIONS["GET"], COMMANDS["INPUT"])
            self._attr_source = next(key for key, value in DEFAULT_SOURCES.items() if value == source_hex)
        except BaseException:
            _LOGGER.warning('Could not get source')
            return

    def turn_on(self) -> None:
        if self.state == MediaPlayerState.OFF:
            self._projector.set_power(True)
            self._attr_state = MediaPlayerState.ON

    def turn_off(self) -> None:
        if self.state == MediaPlayerState.ON:
            self._projector.set_power(False)
            self._attr_state = MediaPlayerState.OFF

    def select_source(self, source: str) -> None:
        """Select input source."""
        selected_source = DEFAULT_SOURCES[source]
        self._projector._send_command(ACTIONS["SET"], COMMANDS["INPUT"], selected_source)

    # @property
    # def extra_state_attributes(self) -> dict[str, str]:
    #     """Return device specific state attributes."""
    #     if self._cmode is None:
    #         return {}
    #     return {ATTR_CMODE: self._cmode}
