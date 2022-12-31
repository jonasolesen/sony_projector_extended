"""The Sony Projector integration."""
from __future__ import annotations

from pysdcp import Projector

from homeassistant import exceptions
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST
from homeassistant.core import HomeAssistant

from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SELECT, Platform.MEDIA_PLAYER]


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


async def validate_projector(host: str) -> Projector:
    """Validate the given projector host allows us to connect."""
    projector = Projector(host)

    try:
        projector.get_power()
        _LOGGER.debug("Validated projector '%s' OK", host)

        return projector
    except ConnectionError:
        _LOGGER.error("Failed to connect to projector '%s'", host)
        raise CannotConnect


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Sony Projector from a config entry."""

    projector = await validate_projector(host=entry.data[CONF_HOST])
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = projector

    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, [platform])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
