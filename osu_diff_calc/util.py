from .enums import Mods


class HitWindow:
    PERFECT = (22.4, 19.4, 13.9)
    GREAT = (64, 49, 34)
    GOOD = (97, 82, 67)
    OK = (127, 112, 97)
    MEH = (151, 136, 121)
    MISS = (188, 173, 158)

    @staticmethod
    def window_for(od, hit):
        return Util.difficulty_range(od, *hit)


class OsuHitWindow(HitWindow):
    GREAT = (80, 50, 20)
    OK = (140, 100, 60)
    MEH = (200, 150, 100)
    MISS = (400, 400, 400)


class Util:
    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def get_time_rate(mods: Mods):
        if not mods:
            return 1
        if int(Mods.HalfTime) & mods:
            return 0.75
        elif int(Mods.DoubleTime) & mods or int(Mods.Nightcore) & mods:
            return 1.5
        return 1

    @staticmethod
    def difficulty_range(difficulty, min, mid, max):
        if difficulty > 5:
            return mid + (max - mid) * (difficulty - 5) / 5
        if difficulty < 5:
            return mid - (mid - min) * (5 - difficulty) / 5
        return mid
