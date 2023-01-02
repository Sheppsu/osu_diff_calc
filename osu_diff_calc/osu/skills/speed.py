from .strain import OsuStrainSkill
from ..evaluators import SpeedEvaluator, RhythmEvaluator

import math


class Speed(OsuStrainSkill):
    skill_multiplier = 1375
    strain_decay_base = 0.3
    reduced_section_count = 5
    difficulty_multiplier = 1.04

    def __init__(self, mods):
        super().__init__(mods)

        self.current_strain = 0
        self.current_rhythm = 0
        self.object_strains = []

    def strain_decay(self, ms):
        return math.pow(self.strain_decay_base, ms / 1000)

    def calculate_initial_strain(self, time, hit_object):
        return (self.current_strain * self.current_rhythm) * self.strain_decay(
            time - hit_object.previous(0).start_time)

    def strain_value_at(self, hit_object):
        self.current_strain *= self.strain_decay(hit_object.strain_time)
        self.current_strain += SpeedEvaluator.evaluate_difficulty_of(hit_object) * self.skill_multiplier

        self.current_rhythm = RhythmEvaluator.evaluate_difficulty_of(hit_object)

        total_strain = self.current_strain * self.current_rhythm

        self.object_strains.append(total_strain)

        return total_strain

    def relevant_note_count(self):
        if len(self.object_strains) == 0:
            return 0

        max_strain = max(self.object_strains)

        if max_strain == 0:
            return 0

        return sum(map(lambda strain: 1 / (1 + math.exp(-(strain / max_strain * 12 - 6))), self.object_strains))
