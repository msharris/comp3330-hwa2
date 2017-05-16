import random

from Individual import Individual


def ga():
    # Initialise the population
    population = list()
    for _ in range(31):
        i = Individual()
        population.append(i)
    population.sort(key=lambda individual: individual.fitness)
    for i in population:
        print(i)

    # Find fitness of population
    # Fitness = 12 * mismatches + features

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
