from enum import IntEnum, auto


class AppState(IntEnum):
    COCKPIT = auto()
    PAUSE = auto()


class AnimState(IntEnum):
    WALK = auto()
    IDLE = auto()


class Axis(IntEnum):
    X = auto()
    Y = auto()
