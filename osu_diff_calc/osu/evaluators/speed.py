from ...enums import HitObjectType
from ...util import Util

import math


class SpeedEvaluator:
    single_spacing_threshold = 125
    min_speed_bonus = 75
    speed_balancing_factor = 40
    
    @staticmethod
    def evaluate_difficulty_of(hit_object):
        if hit_object.base_object.type == HitObjectType.SPINNER:
            return 0

        curr_obj = hit_object
        prev_obj = curr_obj.previous(0)
        next_obj = curr_obj.next(0)

        strain_time = curr_obj.strain_time
        doubletapness = 1

        if next_obj is not None:
            curr_delta_time = max(1, curr_obj.delta_time)
            next_delta_time = max(1, next_obj.delta_time)
            delta_difference = abs(next_delta_time - curr_delta_time)
            speed_ratio = curr_delta_time / max(curr_delta_time, delta_difference)
            window_ratio = math.pow(min(1, curr_delta_time / curr_obj.hit_window_great), 2)
            doubletapness = math.pow(speed_ratio, 1 - window_ratio)

        strain_time /= Util.clamp((strain_time / curr_obj.hit_window_great) / 0.93, 0.92, 1)

        speed_bonus = 1

        if strain_time < SpeedEvaluator.min_speed_bonus:
            speed_bonus = 1 + 0.75 * math.pow((SpeedEvaluator.min_speed_bonus - strain_time) / SpeedEvaluator.speed_balancing_factor, 2)

        travel_distance = prev_obj.travel_distance if prev_obj.travel_distance else 0
        distance = min(SpeedEvaluator.single_spacing_threshold, travel_distance + curr_obj.minimum_jump_distance)

        return (speed_bonus + speed_bonus * math.pow(distance / SpeedEvaluator.single_spacing_threshold, 3.5)) * doubletapness / strain_time
