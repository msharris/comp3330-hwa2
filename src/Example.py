class Example:
    def __init__(self, row):
        self.label = str(row[0])
        self.features = list(map(int, row[1:-1]))
        self.target = int(row[-1])

    def __str__(self):
        return str(self.label) + " " + str(self.features) + " " + str(self.target)
