import random


def ga():
    # Initialise the population
    population = list()
    for i in range(31):
        individual = list()
        for j in range(12):
            individual.append(random.randrange(0, 2, 1))
        population.append(individual)
    print(population)


ga()


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
