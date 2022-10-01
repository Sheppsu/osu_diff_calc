from osu import Client, GameModeStr, Beatmapset, BeatmapsetSearchFilter, GameModeInt
from typing import Sequence
from osu_diff_calc import OsuPerformanceCalculator, OsuDifficultyAttributes, OsuScoreAttributes
from requests.exceptions import HTTPError
import os


def calculate_pp(beatmap, beatmap_attributes, score):
    calculator = OsuPerformanceCalculator(
        GameModeStr.STANDARD,
        OsuDifficultyAttributes.from_attributes({
            'aim_strain': beatmap_attributes.mode_attributes.aim_difficulty,
            'speed_strain': beatmap_attributes.mode_attributes.speed_difficulty,
            'flashlight_rating': beatmap_attributes.mode_attributes.flashlight_difficulty,
            'slider_factor': beatmap_attributes.mode_attributes.slider_factor,
            'speed_note_count': beatmap_attributes.mode_attributes.speed_note_count,
            'approach_rate': beatmap_attributes.mode_attributes.approach_rate,
            'overall_difficulty': beatmap_attributes.mode_attributes.overall_difficulty,
            'max_combo': beatmap_attributes.max_combo,
            'drain_rate': beatmap.drain,
            'hit_circle_count': beatmap.count_circles,
            'slider_count': beatmap.count_sliders,
            'spinner_count': beatmap.count_spinners,
        }), OsuScoreAttributes.from_osupy_score(score))
    calculated_pp = calculator.calculate()
    rounded_calculated_pp = round(calculated_pp, len(str(score.pp).split(".")[1]))
    assert rounded_calculated_pp == score.pp, f"{rounded_calculated_pp} ({calculated_pp}) != {score.pp}"


client = Client.from_client_credentials(int(os.getenv('osu_client_id')), os.getenv('osu_client_secret'),
                                        os.getenv('osu_redirect_uri'))

search_result = client.search_beatmapsets(BeatmapsetSearchFilter().set_mode(GameModeInt.STANDARD))
beatmapsets: Sequence[Beatmapset] = search_result["beatmapsets"]
for beatmapset in beatmapsets[:10]:
    print(f"{beatmapset.artist} - {beatmapset.title}")
    beatmap = beatmapset.beatmaps[0]
    scores = client.get_beatmap_scores(beatmap.id)
    attributes = {}
    for score in scores.scores[:5]:
        print(f" - {score.user.username}")
        if score.mods not in attributes:
            while True:
                try:
                    attributes[score.mods] = client.get_beatmap_attributes(beatmap.id, score.mods, score.mode)
                except HTTPError:
                    continue
                break
        try:
            calculate_pp(beatmap, attributes[score.mods], score)
        except Exception as e:
            print(e)
