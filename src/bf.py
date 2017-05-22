import csv
from itertools import product
from genetic_algorithm import Example


def conflicts(feature_set):
    features = [f for f, g in enumerate(feature_set) if g == 1]  # Get only the features present
    matches = 0
    for e1 in class1:  # For each example in class 1
        f1 = [e1.features[f] for f in features]  # Obtain the feature set
        for e0 in class0:  # For each example in class 0
            f0 = [e0.features[f] for f in features]  # Obtain the feature set
            if f1 == f0:  # Count a match if both feature sets are identical
                matches += 1
    return matches


def classify(examples):
    class0, class1 = [], []
    for e in examples:
        if e.target == 0:
            class0.append(e)
        elif e.target == 1:
            class1.append(e)
    return class0, class1


# Read in the dataset
examples = []
with open('../dataset.csv') as csv_file:
    dataset = csv.reader(csv_file)
    next(dataset)  # Skip the header row
    for row in dataset:
        e = Example(row)
        examples.append(e)

# Classify the examples
class0, class1 = classify(examples)

# Generate all possible feature sets
possible_feature_sets = map(list, product([0, 1], repeat=len(examples[0].features)))

# Brute force all feature sets
feature_sets = []
for fs in possible_feature_sets:
    if conflicts(fs) == 0:
        feature_sets.append([f + 1 for f, g in enumerate(fs) if g == 1])

feature_sets.sort(key=len)
print(*feature_sets, sep='\n')
