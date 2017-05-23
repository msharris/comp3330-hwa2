import csv

import genetic_algorithm as ga
from genetic_algorithm import Example


# Read in the dataset
examples = []
with open('../heartdata.csv') as csv_file:
    dataset = csv.reader(csv_file)
    next(dataset)  # Skip the header row
    for row in dataset:
        e = Example(row)
        examples.append(e)

# Question 2
ga.ga(examples, pop_size=50, min_features=22, max_gen=300,
      crossover_op='1-point', n=1, pc=0.075,
      mutation_op='default', pm=0.0075)
