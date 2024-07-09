from enum import IntEnum, auto


class AppState(IntEnum):
    COCKPIT = auto()
    STORAGE = auto()
    REACTOR = auto()
    PAUSE = auto()
    MENU = auto()
    SETTINGS = auto()


class AnimState(IntEnum):
    WALK = auto()
    IDLE = auto()
