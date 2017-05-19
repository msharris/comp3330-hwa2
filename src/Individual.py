import random


class Individual:
    def __init__(self):
        self.fitness = random.random()  # TODO Change this back to None once fitness calculation is in place
        self.features = []
        for _ in range(12):
            self.features.append(random.randrange(0, 2, 1))

    def __str__(self):
        return str(self.features) + " " + str(self.fitness)
