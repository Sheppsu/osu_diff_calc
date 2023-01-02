from ...strain import StrainSkill
from ...util import Util

import math


class OsuStrainSkill(StrainSkill):
    DEFAULT_DIFFICULTY_MULTIPLIER = 1.06
    reduced_section_count = 10
    reduced_strain_baseline = 0.75
    difficulty_multiplier = DEFAULT_DIFFICULTY_MULTIPLIER

    def __init__(self, mods):
        super().__init__(mods)

    def difficulty_value(self):
        difficulty = 0
        weight = 1

        strains = sorted(list(filter(lambda p: p > 0, self.get_current_strain_peaks())), reverse=True)

        for i in range(min(len(strains), self.reduced_section_count)):
            scale = math.log10(Util.lerp(1, 10, Util.clamp(i / self.reduced_section_count, 0, 1)))
            strains[i] *= Util.lerp(self.reduced_strain_baseline, 1, scale)

        for strain in sorted(strains, reverse=True):
            difficulty += strain * weight
            weight *= self.decay_weight

        return difficulty * self.difficulty_multiplier
