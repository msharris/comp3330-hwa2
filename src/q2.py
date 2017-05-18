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
with open('../dataset.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers
    for row in spamreader:
        examples.append(Example(row))
        # print ', '.join(row)
    #separate examples which have different targets
    for i in examples:
        if i.target == 0:
            class0.append(i)
        elif i.target == 1:
            class1.append(i)
        print(i)



def golf_fitness(population):
    pop_fitness = 0
    for i in population:
        features = i.count(1)
        #mismatches = numberOfMatches(i)
        mismatches = 0
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
        #mismatches = numberOfMatches(1)
        mismatches = 0
        accuracy = constant/(mismatches+1)
        print(accuracy)
        i.fitness = (accuracy+(cost/(accuracy+1))+cost)
        pop_fitness += i.fitness
        print(i.fitness)
    return pop_fitness/len(population)

ind = Individual()
print(ind)
regular_fitness([ind],30)

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
