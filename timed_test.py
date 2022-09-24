from osu import Client
from os.path import split
from os import getenv
from beatmap_reader import SongsFolder, HitObjectType
from osu_diff_calc import BeatmapCalculator, OsuScoreAttributes, OsuPerformanceCalculator, OsuDifficultyAttributes


client_id = int(getenv('osu_client_id'))
client_secret = getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)


songs = SongsFolder.from_path("C:\\Users\\Sheep\\Desktop\\osu!\\Songs")


def get_freedom_dive_arles():
    for beatmapset in songs.beatmapsets:
        if split(beatmapset.path)[1].startswith("257607"):
            return beatmapset.beatmaps[0]


def get_ss_pp(diff, mode):
    perfect_score = OsuScoreAttributes()
    perfect_score.set_attributes({
        "mods": diff.mods,
        "accuracy": 1,
        "score_max_combo": diff.max_combo,
        "count_great": diff.hit_circle_count + diff.slider_count + diff.spinner_count,
        "count_ok": 0,
        "count_meh": 0,
        "count_miss": 0
    })
    pp_calculator = OsuPerformanceCalculator(mode, diff, perfect_score)
    return pp_calculator.calculate()


beatmap = get_freedom_dive_arles()
beatmap.load()
print(beatmap.path)
calculator = BeatmapCalculator(beatmap)


nomod_diff = client.get_beatmap_attributes(beatmap.metadata.beatmap_id)
hit_circle_count = len([obj for obj in beatmap.hit_objects if obj.type == HitObjectType.HITCIRCLE])
slider_count = len([obj for obj in beatmap.hit_objects if obj.type == HitObjectType.SLIDER])
spinner_count = len([obj for obj in beatmap.hit_objects if obj.type == HitObjectType.SPINNER])
diff = OsuDifficultyAttributes.from_attributes({
    'aim_strain': nomod_diff.mode_attributes.aim_difficulty,
    'speed_strain': nomod_diff.mode_attributes.speed_difficulty,
    'flashlight_rating': nomod_diff.mode_attributes.flashlight_difficulty,
    'slider_factor': nomod_diff.mode_attributes.slider_factor,
    'approach_rate': nomod_diff.mode_attributes.approach_rate,
    'overall_difficulty': nomod_diff.mode_attributes.overall_difficulty,
    'max_combo': nomod_diff.max_combo,
    'drain_rate': beatmap.difficulty.hp_drain_rate,
    'hit_circle_count': hit_circle_count,
    'slider_count': slider_count,
    'spinner_count': spinner_count,
})
print("Correct values", nomod_diff.star_rating, nomod_diff.mode_attributes.aim_difficulty,
      nomod_diff.mode_attributes.speed_difficulty,
      nomod_diff.mode_attributes.flashlight_difficulty,
      nomod_diff.mode_attributes.slider_factor, f"{get_ss_pp(diff, beatmap.general.mode)}pp\n")


diff = calculator.get_difficulty_attributes()
print("Calculated values", diff.star_rating, diff.aim_strain, diff.speed_strain,
      diff.flashlight_rating, diff.slider_factor, f"{get_ss_pp(diff, beatmap.general.mode)}pp\n")


timed = calculator.calculator.calculate_timed(0)
broke_at = None
for timed_diff in timed:
    if timed_diff.time >= 224557:
        broke_at = timed_diff
        break
print(broke_at.attributes.star_rating, f"{get_ss_pp(broke_at.attributes, beatmap.general.mode)}pp\n")
