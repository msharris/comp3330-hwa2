from Individual import Individual


def fitness(population):
    # fitness = 12 * mismatches + features
    print("Hello")


def ga():
    # Initialise the population
    population = []
    for _ in range(31):
        i = Individual()
        population.append(i)

    # population.sort(key=lambda individual: individual.fitness)
    # for i in population:
    #     print(i)

    # Find fitness of population
    fitness(population)


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
