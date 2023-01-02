from osu import (
    Client,
    BeatmapsetSearchFilter,
    GameModeInt,
    Beatmapset
)
from typing import Sequence
from os import getenv
from beatmap_reader import Beatmap
from osu_diff_calc import BeatmapCalculator, OsuScoreAttributes
import requests


def get_beatmap(beatmap_id):
    file = requests.get(f"https://osu.ppy.sh/osu/{beatmap_id}")
    with open("osu_file.osu", "wb") as f:
        for chunk in file:
            f.write(chunk)
    beatmap = Beatmap.from_path("osu_file.osu")
    beatmap.load()
    return beatmap


client_id = int(getenv('osu_client_id'))
client_secret = getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

search_result = client.search_beatmapsets(BeatmapsetSearchFilter().set_mode(GameModeInt.STANDARD))
beatmapsets: Sequence[Beatmapset] = search_result["beatmapsets"]
for beatmapset in beatmapsets[:10]:
    print(f"{beatmapset.artist} - {beatmapset.title}")
    beatmap = beatmapset.beatmaps[0]
    scores = client.get_beatmap_scores(beatmap.id)
    local_beatmap = get_beatmap(beatmap.id)
    calculator = BeatmapCalculator(local_beatmap)
    for score in scores.scores[:5]:
        print(f" - {score.user.username}")
        real_pp = score.pp
        calculated_pp = calculator.calculate_pp(OsuScoreAttributes.from_osupy_score(score), score.mods)
        error = abs(real_pp-calculated_pp)
        if error > 2:
            print(f"error: {error}")
