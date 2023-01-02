class PerformanceCalculator:
    def __init__(self, ruleset, attributes):
        if attributes is None:
            raise ValueError("Attributes must not be none.")
        self.ruleset = ruleset
        self.attributes = attributes

    def calculate(self, score):
        raise NotImplementedError()
