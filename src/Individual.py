import random


class Individual:
    def __init__(self):
        self.fitness = None
        self.features = []
        for _ in range(12):
            self.features.append(random.randrange(0, 2, 1))

    def __str__(self):
        feature_set = [f + 1 for f, g in enumerate(self.features) if g == 1]
        return str(feature_set) + " " + str(self.fitness)
