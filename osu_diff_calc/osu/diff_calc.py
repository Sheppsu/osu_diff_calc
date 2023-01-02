from ..enums import Mods
from ..util import Util, OsuHitWindow
from ..diff_calc import DifficultyCalculator, DifficultyAttributes
from .hit_object import OsuDifficultyHitObject
from .skills.aim import Aim
from .skills.speed import Speed
from .skills.flashlight import Flashlight

from typing import Sequence, Union
import math


class OsuDifficultyAttributes(DifficultyAttributes):
    def __init__(self, mods=None, star_rating=None):
        super().__init__(mods, star_rating)

        self.aim_difficulty = None
        self.speed_difficulty = None
        self.speed_note_count = None
        self.flashlight_difficulty = None
        self.slider_factor = None
        self.approach_rate = None
        self.overall_difficulty = None
        self.drain_rate = None
        self.hit_circle_count = None
        self.slider_count = None
        self.spinner_count = None

    @classmethod
    def from_attributes(cls, attributes):
        obj = cls()
        for attr, val in attributes.items():
            setattr(obj, attr, val)
        return obj


# pp_calc imports OsuDifficultyAttributes so define that first to avoid circular import error
from .pp_calc import OsuPerformanceCalculator


class OsuDifficultyCalculator(DifficultyCalculator):
    difficulty_multiplier = 0.0675

    def __init__(self, ruleset, beatmap):
        super().__init__(ruleset, beatmap)

    def create_difficulty_attributes(self, beatmap, mods: Mods, skills: Sequence[Union[Aim, Speed, Flashlight]], clock_rate):
        if len(beatmap.hit_objects) == 0:
            return OsuDifficultyAttributes(mods)

        aim_rating = math.sqrt(skills[0].difficulty_value()) * self.difficulty_multiplier
        aim_rating_no_sliders = math.sqrt(skills[1].difficulty_value()) * self.difficulty_multiplier
        speed_rating = math.sqrt(skills[2].difficulty_value()) * self.difficulty_multiplier
        speed_notes = skills[2].relevant_note_count()
        flashlight_rating = math.sqrt(skills[3].difficulty_value()) * self.difficulty_multiplier

        slider_factor = aim_rating_no_sliders / aim_rating if aim_rating > 0 else 1

        if mods != 0 and int(Mods.TouchDevice) & mods:
            aim_rating = math.pow(aim_rating, 0.8)
            flashlight_rating = math.pow(flashlight_rating, 0.8)

        if mods != 0 and int(Mods.Relax) & mods:
            aim_rating *= 0.9
            flashlight_rating *= 0.7
            speed_rating = 0

        base_aim_performance = math.pow(5 * max(1, aim_rating / 0.0675) - 4, 3) / 100000
        base_speed_performance = math.pow(5 * max(1, speed_rating / 0.0675) - 4, 3) / 100000
        base_flashlight_performance = 0

        if mods != 0 and int(Mods.Flashlight) & mods:
            base_flashlight_performance = math.pow(flashlight_rating, 2) * 25

        base_performance = math.pow(
            math.pow(base_aim_performance, 1.1) +
            math.pow(base_speed_performance, 1.1) +
            math.pow(base_flashlight_performance, 1.1), 1.0 / 1.1
        )

        star_rating = math.pow(OsuPerformanceCalculator.PERFORMANCE_BASE_MULTIPLIER, 1/3
                               ) * 0.027 * (math.pow(100000 / math.pow(2, 1 / 1.1) * base_performance, 1/3) + 4
                                            ) if base_performance > 0.00001 else 0

        preempt = Util.difficulty_range(beatmap.difficulty.approach_rate, 1800, 1200, 450) / clock_rate
        hit_window_great = OsuHitWindow.window_for(beatmap.difficulty.overall_difficulty, OsuHitWindow.GREAT) / clock_rate

        return OsuDifficultyAttributes.from_attributes({
            "star_rating": star_rating,
            "mods": mods,
            "aim_difficulty": aim_rating,
            "speed_difficulty": speed_rating,
            "speed_note_count": speed_notes,
            "flashlight_difficulty": flashlight_rating,
            "slider_factor": slider_factor,
            "approach_rate": (1800 - preempt) / 120 if preempt > 1200 else (1200 - preempt) / 150 + 5,
            "overall_difficulty": (80 - hit_window_great) / 6,
            "drain_rate": beatmap.difficulty.hp_drain_rate,
            "max_combo": beatmap.max_combo,
            "hit_circle_count": beatmap.hit_circle_count,
            "slider_count": beatmap.slider_count,
            "spinner_count": beatmap.spinner_count,
        })

    def create_difficulty_hit_objects(self, beatmap, clock_rate):
        objects = []
        for i in range(1, len(beatmap.hit_objects)):
            last_last = beatmap.hit_objects[i - 2] if i > 1 else None
            last = beatmap.hit_objects[i - 1]
            current = beatmap.hit_objects[i]
            objects.append(OsuDifficultyHitObject(current, last, last_last, clock_rate, objects, len(objects)))
        return objects

    def create_skills(self, beatmap, mods, clock_rate):
        return [
            Aim(mods, True),
            Aim(mods, False),
            Speed(mods),
            Flashlight(mods)
        ]

    @staticmethod
    def difficulty_adjustment_mods():
        return [
            Mods.TouchDevice,
            Mods.HalfTime,
            Mods.Easy,
            Mods.HardRock,
            Mods.Flashlight,
            Mods.Flashlight | Mods.Hidden,
        ]
