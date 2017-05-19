import csv
import random

from Example import Example
from Individual import Individual


def sort(population):
    population.sort(key=lambda individual: individual.fitness, reverse=False)


def fitness(population, golf=False, constant=1):
    if golf:
        return golf_fitness(population)
    else:
        return regular_fitness(population, constant)


def golf_fitness(population):
    pop_fitness = 0
    for i in population:
        features = i.features.count(1)
        matches = matches(i)
        i.fitness = 12 * matches + features
        pop_fitness += i.fitness
    return pop_fitness / len(population)


def regular_fitness(population, constant):
    pop_fitness = 0
    for i in population:
        cost = i.features.count(1)
        accuracy = constant / (matches(i) + 1)
        i.fitness = (accuracy + (cost / (accuracy + 1)) + cost)
        pop_fitness += i.fitness
    return pop_fitness / len(population)


def matches(individual):
    features = [f for f, g in enumerate(individual.features) if g == 1]  # Get the features present in individual
    matches = 0
    for e1 in class1:  # For each example in class 1
        f1 = [e1.features[f] for f in features]  # Obtain the feature set
        for e0 in class0:  # For each example in class 0
            f0 = [e0.features[f] for f in features]  # Obtain the feature set
            if f1 == f0:  # Count a match if both feature sets are identical
                matches += 1
    return matches


# Read in the dataset
examples = []
with open('../dataset.csv') as csv_file:
    dataset = csv.reader(csv_file)
    next(dataset)  # Skip the header row
    for row in dataset:
        examples.append(Example(row))

# Classify each example
class1 = []
class0 = []
for e in examples:
    if e.target == 1:
        class1.append(e)
    elif e.target == 0:
        class0.append(e)

# Print examples for debugging
print('Examples:')
print(*examples, sep='\n')


# BEGIN GENETIC ALGORITHM

# Initialise the population
population = []
for _ in range(31):
    population.append(Individual())

# Find fitness of population
fitness = fitness(population)

# parent selection
# however, we need to decide how many we want to cull from population
# before determining how many children we can produce
newPopn = []
for i in range(len(population)):
    parent1Val = random.randrange(0, len(population))
    parent2Val = random.randrange(0, len(population))
    while parent2Val == parent1Val:
        parent2Val = random.randrange(0, len(population))
# crossover (10% chance of crossover)
    crossover = random.randrange(0,100)
    if crossover<10:
        tempFeatures = []
        #append first half of features from parent1
        print("Parent 1:")
        print(population[parent1Val])
        # tempFeatures.append(population[parent1Val].features[0:len(population[parent1Val].features)/2])
        for i in range(0, int(len(population[parent1Val].features)/2)):
            tempFeatures.append(population[parent1Val].features[i])
        #append second half of features from parent2
        print("Parent 2:")
        print(population[parent2Val])
        # tempFeatures.append(population[parent2Val].features[len(population[parent1Val].features)/2:])
        for i in range(int(len(population[parent1Val].features)/2), len(population[parent1Val].features)):
            tempFeatures.append(population[parent2Val].features[i])
        print("Child")
        print(tempFeatures)


# GA()
#   initialize population
#   find fitness of population
#
#   while (termination criteria is reached) do
#     parent selection
#     crossover with probability pc
#     mutation with probability pm
#     fitness calculation
#     survivor selection
#     find best
#
#   return best

