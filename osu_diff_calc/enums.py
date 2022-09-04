from enum import IntEnum, IntFlag


class GameMode(IntEnum):
    STANDARD = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3


class HitObjectType(IntEnum):
    HITCIRCLE = 0
    SLIDER = 1
    SPINNER = 2
    MANIA_HOLD_KEY = 3


class Mods(IntFlag):
    NoFail = 1 << 0
    Easy = 1 << 1
    TouchDevice = 1 << 2
    Hidden = 1 << 3
    HardRock = 1 << 4
    SuddenDeath = 1 << 5
    DoubleTime = 1 << 6
    Relax = 1 << 7
    HalfTime = 1 << 8
    Nightcore = (1 << 9)
    Flashlight = 1 << 10
    SpunOut = 1 << 12
    AutoPilot = 1 << 13
    Perfect = 1 << 14
    FadeIn = 1 << 20
    Mirror = 1 << 30

    Key4 = 1 << 15
    Key5 = 1 << 16
    Key6 = 1 << 17
    Key7 = 1 << 18
    Key8 = 1 << 19
    Key9 = 1 << 24
