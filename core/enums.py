from enum import IntEnum, auto


class AppState(IntEnum):
    EMPTY = auto()
    COCKPIT = auto()
    STORAGE = auto()
    REACTOR = auto()
    PAUSE = auto()
    MENU = auto()
    SETTINGS = auto()
    INTRO = auto()
    OUTRO = auto()
    SPLASH = auto()


class AnimState(IntEnum):
    WALK = auto()
    IDLE = auto()
