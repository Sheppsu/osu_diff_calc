from ...enums import HitObjectType
from ...util import Util

import math


class AimEvaluator:
    wide_angle_multiplier = 1.5
    acute_angle_multiplier = 1.95
    slider_multiplier = 1.35
    velocity_change_multiplier = 0.75
    
    @staticmethod
    def evaluate_difficulty_of(hit_object, with_sliders):
        if hit_object.base_object.type == HitObjectType.SPINNER or hit_object.index <= 1 or \
                hit_object.previous(0).base_object.type == HitObjectType.SPINNER:
            return 0

        curr_obj = hit_object
        last_obj = hit_object.previous(0)
        last_last_obj = hit_object.previous(1)

        curr_velocity = curr_obj.lazy_jump_distance / curr_obj.strain_time

        # print(f"{curr_obj.lazy_jump_distance} | {curr_obj.strain_time}")

        if with_sliders and last_obj.base_object.type == HitObjectType.SLIDER:
            travel_velocity = last_obj.travel_distance / last_obj.travel_time
            movement_velocity = curr_obj.minimum_jump_distance / curr_obj.minimum_jump_time

            curr_velocity = max(curr_velocity, movement_velocity + travel_velocity)

        prev_velocity = last_obj.lazy_jump_distance / last_obj.strain_time

        if with_sliders and last_last_obj.base_object.type == HitObjectType.SLIDER:
            travel_velocity = last_last_obj.travel_distance / last_last_obj.travel_time
            movement_velocity = last_obj.minimum_jump_distance / last_obj.minimum_jump_time

            prev_velocity = max(prev_velocity, movement_velocity + travel_velocity)

        wide_angle_bonus = 0
        acute_angle_bonus = 0
        slider_bonus = 0
        velocity_change_bonus = 0

        aim_strain = curr_velocity

        if max(curr_obj.strain_time, last_obj.strain_time) < 1.25 * min(curr_obj.strain_time, last_obj.strain_time):
            if curr_obj.angle is not None and last_obj.angle is not None and \
                    last_last_obj.angle is not None:
                curr_angle = curr_obj.angle
                last_angle = last_obj.angle
                last_last_angle = last_last_obj.angle

                angle_bonus = min(curr_velocity, prev_velocity)

                wide_angle_bonus = AimEvaluator.calc_wide_angle_bonus(curr_angle)
                acute_angle_bonus = AimEvaluator.calc_acute_angle_bonus(curr_angle)

                if curr_obj.strain_time > 100:
                    acute_angle_bonus = 0
                else:
                    acute_angle_bonus *= AimEvaluator.calc_acute_angle_bonus(last_angle) \
                        * min(angle_bonus, 125 / curr_obj.strain_time) \
                        * math.pow(math.sin(math.pi / 2 * min(1, (100 - curr_obj.strain_time) / 25)), 2) \
                        * math.pow(math.sin(math.pi / 2 * (Util.clamp(curr_obj.lazy_jump_distance, 50, 100) - 50) / 50), 2)

                wide_angle_bonus *= angle_bonus * (1 - min(wide_angle_bonus, math.pow(
                    AimEvaluator.calc_wide_angle_bonus(last_angle), 3)))
                acute_angle_bonus *= 0.5 + 0.5 * (1 - min(acute_angle_bonus, math.pow(
                    AimEvaluator.calc_acute_angle_bonus(last_last_angle), 3)))

        if max(prev_velocity, curr_velocity) != 0:
            prev_velocity = (last_obj.lazy_jump_distance + last_last_obj.travel_distance) / last_obj.strain_time
            curr_velocity = (curr_obj.lazy_jump_distance + last_obj.travel_distance) / curr_obj.strain_time

            dist_ratio = math.pow(math.sin(math.pi / 2 * abs(prev_velocity - curr_velocity) /
                                           max(prev_velocity, curr_velocity)), 2)

            overlap_velocity_buff = min(125 / min(curr_obj.strain_time, last_obj.strain_time),
                                        abs(prev_velocity - curr_velocity))

            velocity_change_bonus = overlap_velocity_buff * dist_ratio

            velocity_change_bonus *= math.pow(min(curr_obj.strain_time, last_obj.strain_time) /
                                              max(curr_obj.strain_time, last_obj.strain_time), 2)

        if last_obj.base_object.type == HitObjectType.SLIDER:
            slider_bonus = last_obj.travel_distance / last_obj.travel_time

        aim_strain += max(acute_angle_bonus * AimEvaluator.acute_angle_multiplier, wide_angle_bonus * AimEvaluator.wide_angle_multiplier +
                          velocity_change_bonus * AimEvaluator.velocity_change_multiplier)

        if with_sliders:
            aim_strain += slider_bonus * AimEvaluator.slider_multiplier

        return aim_strain

    @staticmethod
    def calc_wide_angle_bonus(angle):
        return math.pow(math.sin(3 / 4 * (min(5 / 6 * math.pi, max(math.pi / 6, angle)) - math.pi / 6)), 2)

    @staticmethod
    def calc_acute_angle_bonus(angle):
        return 1 - AimEvaluator.calc_wide_angle_bonus(angle)
