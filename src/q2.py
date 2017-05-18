from Individual import Individual
from Example import Example
import csv
examples = []
class1 = []
class0 = []
with open('../dataset.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)  # skip the headers
    for row in spamreader:
        examples.append(Example(row))
        # print ', '.join(row)
    for i in examples:
        if i.target == 0:
            class0.append(i)
        elif i.target == 1:
            class1.append(i)
        print(i)



def fitness(population):
    # fitness = 12 * mismatches + features
    print("Hello")


def ga():
    # Initialise the population
    population = []
    for _ in range(31):
        population.append(Individual())

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
#     decode and fitness calculation
#     survivor selection
#     find best
#
#   return best
