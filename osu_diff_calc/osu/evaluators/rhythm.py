from ...enums import HitObjectType

import math


class RhythmEvaluator:
    history_time_max = 5000
    rhythm_multiplier = 0.75

    @staticmethod
    def evaluate_difficulty_of(hit_object):
        if hit_object.base_object.type == HitObjectType.SPINNER:
            return 0

        previous_island_size = 0

        rhythm_complexity_sum = 0
        island_size = 1
        start_ratio = 0

        first_delta_switch = False

        historical_note_count = min(hit_object.index, 32)

        rhythm_start = 0

        while rhythm_start < historical_note_count - 2 and \
                hit_object.start_time - hit_object.previous(rhythm_start).start_time < RhythmEvaluator.history_time_max:
            rhythm_start += 1

        for i in reversed(range(1, rhythm_start+1)):
            curr_obj = hit_object.previous(i - 1)
            prev_obj = hit_object.previous(i)
            last_obj = hit_object.previous(i + 1)

            curr_historical_data = (RhythmEvaluator.history_time_max - (hit_object.start_time - curr_obj.start_time)) / \
                RhythmEvaluator.history_time_max

            curr_historical_data = min((historical_note_count - i) / historical_note_count, curr_historical_data)

            curr_delta = curr_obj.strain_time
            prev_delta = prev_obj.strain_time
            last_delta = last_obj.strain_time
            curr_ratio = 1 + 6 * min(0.5, math.pow(math.sin(math.pi / (min(prev_delta, curr_delta) /
                                                                       max(prev_delta, curr_delta))), 2))

            window_penalty = min(1, max(0, abs(prev_delta - curr_delta) - curr_obj.hit_window_great * 0.3) /
                                 (curr_obj.hit_window_great * 0.3))

            window_penalty = min(1, window_penalty)

            effective_ratio = window_penalty * curr_ratio

            if first_delta_switch:
                if not (prev_delta > 1.25 * curr_delta or prev_delta * 1.25 < curr_delta):
                    if island_size < 7:
                        island_size += 1
                else:
                    if hit_object.previous(i - 1).base_object.type == HitObjectType.SLIDER:
                        effective_ratio *= 0.125
                    if hit_object.previous(i).base_object.type == HitObjectType.SLIDER:
                        effective_ratio *= 0.25
                    if previous_island_size == island_size:
                        effective_ratio *= 0.25
                    if previous_island_size % 2 == island_size % 2:
                        effective_ratio *= 0.5
                    if last_delta > prev_delta + 10 and prev_delta > curr_delta + 10:
                        effective_ratio *= 0.125

                    rhythm_complexity_sum += math.sqrt(effective_ratio * start_ratio) * curr_historical_data * \
                        math.sqrt(4 + island_size) / 2 * math.sqrt(4 + previous_island_size) / 2

                    start_ratio = effective_ratio

                    previous_island_size = island_size

                    if prev_delta * 1.25 < curr_delta:
                        first_delta_switch = False

                    island_size = 1
            elif prev_delta > 1.25 * curr_delta:
                first_delta_switch = True
                start_ratio = effective_ratio
                island_size = 1

        return math.sqrt(4 + rhythm_complexity_sum * RhythmEvaluator.rhythm_multiplier) / 2
