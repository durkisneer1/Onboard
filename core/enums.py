from enum import IntEnum, auto


class AppState(IntEnum):
    EMPTY = auto()
    COCKPIT = auto()
    STORAGE = auto()
    REACTOR = auto()
    PAUSE = auto()
    MENU = auto()
    SETTINGS = auto()


class AnimState(IntEnum):
    WALK = auto()
    IDLE = auto()
