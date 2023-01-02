from ...enums import HitObjectType
from ...util import Util

import math


class FlashlightEvaluator:
    max_opacity_bonus = 0.4
    hidden_bonus = 0.2

    min_velocity = 0.5
    slider_multiplier = 1.3

    min_angle_multiplier = 0.2

    @staticmethod
    def evaluate_difficulty_of(hit_object, hidden):
        if hit_object.base_object.type == HitObjectType.SPINNER:
            return 0

        base_object = hit_object.base_object

        scaling_factor = 52 / base_object.radius
        small_dist_nerf = 1
        cumulative_strain_time = 0

        result = 0

        last_obj = hit_object

        angle_repeat_count = 0

        for i in range(min(hit_object.index, 10)):
            curr_obj = hit_object.previous(i)
            curr_base_obj = curr_obj.base_object

            if curr_base_obj.type != HitObjectType.SPINNER:
                jump_distance = base_object.stacked_position.distance_to(curr_base_obj.stacked_end_position)

                cumulative_strain_time += last_obj.strain_time

                if i == 0:
                    small_dist_nerf = min(1, jump_distance / 75)

                stack_nerf = min(1, (curr_obj.lazy_jump_distance / scaling_factor) / 25)

                opacity_bonus = 1 + FlashlightEvaluator.max_opacity_bonus * (1 - hit_object.opacity_at(
                    curr_base_obj.time, hidden))

                result += stack_nerf * opacity_bonus * scaling_factor * jump_distance / cumulative_strain_time

                if curr_obj.angle is not None and hit_object.angle is not None:
                    if abs(curr_obj.angle - hit_object.angle) < 0.02:
                        angle_repeat_count += max(1 - 0.1 * i, 0)

            last_obj = curr_obj

        result = math.pow(small_dist_nerf * result, 2)

        if hidden:
            result *= 1 + FlashlightEvaluator.hidden_bonus

        result *= FlashlightEvaluator.min_angle_multiplier + (1 - FlashlightEvaluator.min_angle_multiplier
                                                              ) / (angle_repeat_count + 1)

        slider_bonus = 0

        if base_object.type == HitObjectType.SLIDER:
            pixel_travel_distance = base_object.lazy_travel_distance / scaling_factor

            slider_bonus = math.pow(max(0, pixel_travel_distance / hit_object.travel_time -
                                        FlashlightEvaluator.min_velocity), 0.5)
            slider_bonus *= pixel_travel_distance

            if base_object.slides - 1 > 0:
                slider_bonus /= base_object.slides

        result += slider_bonus * FlashlightEvaluator.slider_multiplier

        return result
