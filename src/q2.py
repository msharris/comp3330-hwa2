import csv
import random
from Individual import Individual
from Example import Example

def fitness(population):
    # fitness = 12 * mismatches + features
    # print("Hello")
    i = 0;

def sortPopn(population):
    population.sort(key=lambda individual: individual.fitness, reverse=False)
# for i in population:
#     print(i)


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
        # print(i) #troubleshoot printing
    # Initialise the population
    population = []
    for _ in range(31):
        population.append(Individual())
    sortPopn(population)
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
            for i in range(0,len(population[parent1Val].features)/2):
                tempFeatures.append(population[parent1Val].features[i])
            #append second half of features from parent2
            print("Parent 2:")
            print(population[parent2Val])
            # tempFeatures.append(population[parent2Val].features[len(population[parent1Val].features)/2:])
            for i in range(len(population[parent1Val].features)/2, len(population[parent1Val].features)):
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
