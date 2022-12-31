"""Constants for the Sony Projector integration."""

DOMAIN = "sony_projector_extended"

DEFAULT_SOURCES = {
    "HDMI1": 0x2,
    "HDMI2": 0x3,
}

ASPECT_RATIOS = {
    "NORMAL": 0x1,
    "V_STRETCH": 0xb,
    "ZOOM_1_85": 0xc,
    "ZOOM_2_35": 0xd,
    "SQUEEZE": 0xf,
}

CALIBRATION_PRESETS = {
    "CINEMA_FILM_1": 0x0,
    "CINEMA_FILM_2": 0x1,
    "REFERENCE": 0x2,
    "TV": 0x3,
    "PHOTO": 0x4,
    "GAME": 0x5,
    "BRIGHT_CINEMA": 0x6,
    "BRIGHT_TV": 0x7,
    "USER": 0x8,
}
