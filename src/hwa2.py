import csv

import genetic_algorithm as ga
from genetic_algorithm import Example


# Question 2

# Read in the dataset
examples = []
with open('../dataset.csv') as csv_file:
    dataset = csv.reader(csv_file)
    next(dataset)  # Skip the header row
    for row in dataset:
        e = Example(row)
        examples.append(e)

ga.ga(examples, pop_size=10, min_features=5, max_gen=100,
      crossover_op='1-point', n=1, pc=0.7,
      mutation_op='default', pm=0.01)


# Question 4

# Read in the dataset
# examples = []
# with open('../spect-train.csv') as csv_file:
#     dataset = csv.reader(csv_file)
#     next(dataset)  # Skip the header row
#     for row in dataset:
#         e = Example(row)
#         examples.append(e)
#
# ga.ga(examples, pop_size=40, min_features=22, max_gen=100,
#       crossover_op='n-point', n=11, pc=0.75,
#       mutation_op='1-flip', pm=0.075)
