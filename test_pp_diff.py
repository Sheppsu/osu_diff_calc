from osu import Mods, Client
from beatmap_reader import SongsFolder, HitObjectType
from osu_diff_calc import BeatmapCalculator, OsuScoreAttributes, OsuPerformanceCalculator, \
    OsuDifficultyAttributes
from os import path, getenv


songs = SongsFolder.from_path("C:\\Users\\Sheep\\Desktop\\osu!\\Songs")

print(len(songs.beatmapsets))

beatmap = None
for beatmapset in songs.beatmapsets:
    if path.split(beatmapset.path)[1].startswith("1582420"):
        beatmap = beatmapset.beatmaps[2]
        break

print(beatmap.path)
if not beatmap.load():
    quit()


calculator = BeatmapCalculator(beatmap)


difficulty = []
for mod in (None, ):#Mods.HardRock, Mods.DoubleTime, Mods.Easy, Mods.HalfTime, Mods.Flashlight):
    difficulty.append(calculator.get_difficulty_attributes(mod))


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


for diff in difficulty:
    print(diff.mods, diff.star_rating, diff.aim_strain, diff.speed_strain,
          diff.flashlight_rating, diff.slider_factor, f"{get_ss_pp(diff, beatmap.general.mode)}pp")


client_id = int(getenv('osu_client_id'))
client_secret = getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)


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
