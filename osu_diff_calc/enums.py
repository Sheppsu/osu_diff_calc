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
    # TODO: is_compatible_with method
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

    FourKeys = 1 << 15
    FiveKeys = 1 << 16
    SixKeys = 1 << 17
    SevenKeys = 1 << 18
    EightKeys = 1 << 19
    NineKeys = 1 << 24

    @staticmethod
    def combine(mods):
        if len(mods) == 0:
            return
        if len(mods) == 1:
            return mods[0]

        combined_mods = mods[0]
        for mod in mods[1:]:
            combined_mods |= mod

        return combined_mods
