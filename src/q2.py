import copy
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
        matches = conflicts(i)
        i.fitness = 12 * matches + features
        pop_fitness += i.fitness
    return pop_fitness, pop_fitness / len(population)


def regular_fitness(population, constant):
    pop_fitness = 0
    cost_max = len(population[0])  # Assumes that all members of population have the same size genotype.
    for i in population:
        cost = i.features.count(1)
        accuracy = constant / (conflicts(i) + 1)
        i.fitness = (accuracy - (cost / (accuracy + 1)) + cost_max)
        pop_fitness += i.fitness
    return pop_fitness, pop_fitness / len(population)


def conflicts(individual):
    features = [f for f, g in enumerate(individual.features) if g == 1]  # Get the features present in individual
    matches = 0
    for e1 in class1:  # For each example in class 1
        f1 = [e1.features[f] for f in features]  # Obtain the feature set
        for e0 in class0:  # For each example in class 0
            f0 = [e0.features[f] for f in features]  # Obtain the feature set
            if f1 == f0:  # Count a match if both feature sets are identical
                matches += 1
    return matches


def parent_selection(population):
    # Get total population fitness and sort the population
    total_fitness, _ = fitness(population, golf=True)
    sort(population)

    # Begin parent selection
    parents = []
    for _ in range(2):
        r = random.uniform(0, total_fitness)
        p = 0
        for i in population:
            if p + i.fitness > r:
                parents.append(i)
                break
            else:
                p += i.fitness

    # Return parents
    return parents[0], parents[1]


def crossover(parent1, parent2, op='1-point', n=1, pc=0.75):
    # Create children
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    child1.fitness = None
    child2.fitness = None
    if random.random() < pc:
        if op == '1-point':
            op, n = 'n-point', 1  # Perform n-point crossover with n = 1
        if op == 'n-point':
            points = random.sample(range(1, len(parent1.features)), n)  # Generate crossover points
            points.sort()  # Sort the crossover points
            points = [0] + points + [len(parent1.features)]  # Add the beginning and end indexes to create range tuples
            tuples = list(zip(points, points[1:]))  # Generate range tuples
            swap_zones = tuples[1::2]  # Grab every second range to swap alternating ranges
            for left, right in swap_zones:
                child2.features[left:right] = parent1.features[left:right]
                child1.features[left:right] = parent2.features[left:right]
        if op == 'uniform':
            # Each feature has a 50% chance swap
            for i in range(len(child1.features)):
                if random.choice([True, False]):
                    child1.features[i], child2.features[i] = child2.features[i], child1.features[i]
    return child1, child2


# def crossover(parent1, parent2, pc=0.75):
#     # Create children
#     child1 = copy.deepcopy(parent1)
#     child2 = copy.deepcopy(parent2)
#     child1.fitness = None
#     child2.fitness = None
#     if random.random() < pc:
#         point = random.randint(1, len(parent1.features) - 1)
#         child2.features[point:] = parent1.features[point:]
#         child1.features[point:] = parent2.features[point:]
#     return child1, child2


def mutation(child, op='default', pm=0.1):
    if op == 'default':
        for i in range(len(child.features)):
            if random.random() < pm:
                child.features[i] = 1 - child.features[i]
    else:
        if random.random() < pm and op in ['1-flip', 'multi-flip']:
            flips = 1 if op == '1-flip' else random.randrange(len(child.features))
            flip_points = random.sample(range(len(parent1.features)), flips)  # Generate flipping points
            for p in flip_points:
                child.features[p] = 1 - child.features[p]


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
for _ in range(20):
    population.append(Individual())

# Find fitness of population
total_fitness, avg_fitness = fitness(population, golf=True)
sort(population)

print("Generation: 0")
print("Population size: ", len(population))
print("Average fitness: ", avg_fitness)
print("Best solution: ", population[0])
print()

# TODO Determine termination criteria
generation = 1
while population[0].fitness > 5:
    # Generate a new population
    new_pop = []
    for _ in range(int(len(population) / 2)):
        # Perform parent selection
        parent1, parent2 = parent_selection(population)

        # Perform crossover with probability pc
        child1, child2 = crossover(parent1, parent2, op='1-point', pc=0.75)

        # Perform mutation with probability pm
        mutation(child1, pm=0.05)
        mutation(child2, pm=0.05)

        # Add children to new population
        new_pop.extend([child1, child2])

    # Replace old population with new population
    population = copy.copy(new_pop)
    new_pop.clear()

    # Find fitness of population
    total_fitness, avg_fitness = fitness(population, golf=True)
    sort(population)
    print("Generation: ", generation)
    print("Population size: ", len(population))
    print("Average fitness: ", avg_fitness)
    print("Best solution: ", population[0])
    print()
    generation += 1

    # TODO Decide how many individuals to remove from the population before determining how many children we can produce


# GA()
#   initialize population
#   find fitness of population
#
#   while (termination criteria is not reached) do
#     parent selection
#     crossover with probability pc
#     mutation with probability pm
#     fitness calculation
#     survivor selection
#     find best
#
#   return best
