from .strain import OsuStrainSkill
from ..evaluators import FlashlightEvaluator
from ...enums import Mods

import math


class Flashlight(OsuStrainSkill):
    skill_multiplier = 0.052
    strain_decay_base = 0.15

    def __init__(self, mods):
        super().__init__(mods)

        self.has_hidden_mod = int(Mods.Hidden) & mods
        self.current_strain = 0

    def strain_decay(self, ms):
        return math.pow(self.strain_decay_base, ms / 1000)

    def calculate_initial_strain(self, time, hit_object):
        return self.current_strain * self.strain_decay(time - hit_object.previous(0).start_time)

    def strain_value_at(self, hit_object):
        self.current_strain *= self.strain_decay(hit_object.delta_time)
        self.current_strain += FlashlightEvaluator.evaluate_difficulty_of(hit_object, self.has_hidden_mod) * \
            self.skill_multiplier

        return self.current_strain

    def difficulty_value(self):
        return sum(self.get_current_strain_peaks()) * \
               OsuStrainSkill.DEFAULT_DIFFICULTY_MULTIPLIER
