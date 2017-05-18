class Example:
    def __init__(self, row):
        self.label = row[0]
        self.features = row[1:-2]
        self.target = row[-1]

    def __str__(self):
        return str(self.label) + " " + str(self.features) + " " + str(self.target)
