from osu import Client, GameModeStr
from osu_diff_calc import OsuPerformanceCalculator, OsuDifficultyAttributes, OsuScoreAttributes
import os


client = Client.from_client_credentials(int(os.getenv('osu_client_id')), os.getenv('osu_client_secret'), os.getenv('osu_redirect_uri'))

score = client.get_score_by_id(GameModeStr.STANDARD, 4230447657)
beatmap = client.get_beatmap(score.beatmap.id)
beatmap_attributes = client.get_beatmap_attributes(beatmap.id, score.mods, score.mode)


calculator = OsuPerformanceCalculator(
    GameModeStr.STANDARD,
    OsuDifficultyAttributes.from_attributes({
        'aim_strain': beatmap_attributes.mode_attributes.aim_difficulty,
        'speed_strain': beatmap_attributes.mode_attributes.speed_difficulty,
        'flashlight_rating': beatmap_attributes.mode_attributes.flashlight_difficulty,
        'slider_factor': beatmap_attributes.mode_attributes.slider_factor,
        'approach_rate': beatmap_attributes.mode_attributes.approach_rate,
        'overall_difficulty': beatmap_attributes.mode_attributes.overall_difficulty,
        'max_combo': beatmap_attributes.max_combo,
        'drain_rate': beatmap.drain,
        'hit_circle_count': beatmap.count_circles,
        'slider_count': beatmap.count_sliders,
        'spinner_count': beatmap.count_spinners,
    }), OsuScoreAttributes.from_osupy_score(score))
print(calculator.calculate())
