from osu import Mods
from beatmap_reader import SongsFolder
from osu_diff_calc import BeatmapCalculator, OsuScoreAttributes, OsuPerformanceCalculator
import random


songs = SongsFolder.from_path("C:\\Users\\Sheep\\Desktop\\osu!\\Songs")

print(len(songs.beatmapsets))
beatmapset = random.choice(songs.beatmapsets)
beatmap = random.choice(beatmapset.beatmaps)
print(beatmap.path)
if not beatmap.load():
    quit()


calculator = BeatmapCalculator(beatmap)


difficulty = []
for mod in (None, Mods.HardRock, Mods.DoubleTime, Mods.Easy, Mods.HalfTime, Mods.Flashlight):
    difficulty.append(calculator.get_difficulty_attributes(mod))


for diff in difficulty:
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
    pp_calculator = OsuPerformanceCalculator(beatmap.general.mode, diff, perfect_score)

    print(diff.mods, diff.star_rating, diff.aim_strain, diff.speed_strain,
          diff.flashlight_rating, diff.slider_factor, f"{pp_calculator.calculate()}pp")
