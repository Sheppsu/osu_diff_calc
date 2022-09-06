from .util import Util


class PerformanceCalculator:
    def __init__(self, ruleset, attributes, score):
        if attributes is None:
            raise ValueError("Attributes must not be none.")
        self.ruleset = ruleset
        self.attributes = attributes
        self.score = score
        self.time_rate = Util.get_time_rate(score.mods)

    def calculate(self, category_difficulty=None):
        raise NotImplementedError()
