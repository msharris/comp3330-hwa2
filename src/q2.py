import csv
import random
from Individual import Individual
from Example import Example

def fitness(population):
    # fitness = 12 * mismatches + features
    print("Hello")

def sortPopn(population):
    population.sort(key=lambda individual: individual.fitness, reverse=False)
    for i in population:
        print(i)


examples = []
class1 = []
class0 = []
with open('../dataset.csv') as csvfile:
    dataset = csv.reader(csvfile)
    next(dataset)  # skip the headers
    for row in dataset:
        examples.append(Example(row))
    for e in examples:
        if e.target == 0:
            class0.append(e)
        elif e.target == 1:
            class1.append(e)
        print(e)


def golf_fitness(population):
    pop_fitness = 0
    for i in population:
        features = i.count(1)
        mismatches = matches(i)
        i.fitness = 12 * mismatches + features
        pop_fitness += i.fitness
    return pop_fitness/len(population)
    # fitness = 12 * mismatches + features
    print("Hello")

def regular_fitness(population,constant):
    pop_fitness = 0
    for i in population:
        cost = i.features.count(1)
        print(cost)
        mismatches = matches(1)
        accuracy = constant/(mismatches+1)
        print(accuracy)
        i.fitness = (accuracy+(cost/(accuracy+1))+cost)
        pop_fitness += i.fitness
        print(i.fitness)
    return pop_fitness/len(population)

ind = Individual()
print(ind)
regular_fitness([ind],30)

def matches(individual):
    features = [f for f, g in enumerate(individual.features) if g == 1]  # Get the features present in individual
    matches = 0
    for e1 in class1:  # For each example in class 1
        f1 = [e1.features[f] for f in features]  #
        for e0 in class0:
            f0 = [e0.features[f] for f in features]
            if f1 == f0:
                matches += 1
    return matches


def ga():
    # Initialise the population
    population = []
    for _ in range(31):
        population.append(Individual())
    sortPopn(population)
    # parent selection
    # however, we need to decide how many we want to cull from population
    # before determining how many children we can produce
    parent1Val = random.randrange(0, len(population))
    parent2Val = random.randrange(0, len(population))
    while parent2Val == parent1Val:
        parent2Val = random.randrange(0, len(population))

    # population.sort(key=lambda individual: individual.fitness)
    # for i in population:
    #     print(i)

    # Find fitness of population
    fitness(population)

def sortPopn(population):
    population.sort(key=lambda x: x.fitness, reverse=True)

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
