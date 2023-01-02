from .strain import OsuStrainSkill
from ..evaluators.aim import AimEvaluator

import math


class Aim(OsuStrainSkill):
    skill_multiplier = 23.55
    strain_decay_base = 0.15

    def __init__(self, mods, with_sliders):
        super().__init__(mods)
        self.with_sliders = with_sliders
        self.current_strain = 0

    def strain_decay(self, ms):
        return math.pow(self.strain_decay_base, ms / 1000)

    def calculate_initial_strain(self, time, hit_object):
        return self.current_strain * self.strain_decay(time - hit_object.previous(0).start_time)

    def strain_value_at(self, hit_object):
        self.current_strain *= self.strain_decay(hit_object.delta_time)
        self.current_strain += AimEvaluator.evaluate_difficulty_of(hit_object, self.with_sliders) * self.skill_multiplier

        return self.current_strain
