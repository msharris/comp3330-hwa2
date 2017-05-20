import csv

import genetic_algorithm as ga
from genetic_algorithm import Example


# Read in the dataset
examples = []
with open('../dataset.csv') as csv_file:
    dataset = csv.reader(csv_file)
    next(dataset)  # Skip the header row
    for row in dataset:
        e = Example(row)
        examples.append(e)

# Question 2
ga.ga(examples, pop_size=10, crossover_op='n-point', n=2, pc=0.75, mutation_op='default', pm=0.075)
