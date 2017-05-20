import copy
import random

import matplotlib.pyplot as plt


class Example:
    def __init__(self, row):
        self.label = str(row[0])
        self.features = list(map(int, row[1:-1]))
        self.target = int(row[-1])

    def __str__(self):
        return str(self.label) + " " + str(self.features) + " " + str(self.target)


class Individual:
    def __init__(self):
        self.fitness = None
        self.features = []
        for _ in range(12):
            self.features.append(random.randrange(0, 2, 1))

    def __str__(self):
        feature_set = [f + 1 for f, g in enumerate(self.features) if g == 1]
        return str(feature_set)


# Declare class lists globally for ease of use
class0, class1 = [], []


def ga(examples, pop_size, min_features=5, max_gen=1000,
       crossover_op='1-point', n=1, pc=0.75,
       mutation_op='default', pm=0.075):
    # Classify each example
    classify(examples)

    # Initialise population
    population = init_population(pop_size)
    generation = 0

    # Determine the fitness we should converge at
    convergence_fitness = min_features  #(len(class0[0].features) * (len(class1)*len(class0)) + len(class0[0].features)) - min_features

    # Find fitness of population
    average_fitness, _ = fitness(population)

    # Declare some arrays for plotting convergence curves
    averages = [average_fitness]
    bests = [population[0].fitness]

    # Print the characteristics of the initial population
    print_generation(generation, population, average_fitness)

    while not terminate(population, generation, convergence_fitness, max_gen):
        # Generate a new population
        children = []
        mating_pool = parent_selection(population)
        for parent1, parent2 in mating_pool:
            # Perform crossover with probability pc
            child1, child2 = crossover(parent1, parent2, crossover_op, n, pc)

            # Perform mutation with probability pm
            mutation(child1, op=mutation_op, pm=pm)
            mutation(child2, op=mutation_op, pm=pm)

            # Add children to list
            children.extend([child1, child2])

        # Perform survivor selection
        population = survivor_selection(population, children)

        # Find fitness of new population
        average_fitness, _ = fitness(population)
        averages.append(average_fitness)
        bests.append(population[0].fitness)  # Guaranteed to be sorted via fitness function
        generation += 1
        print_generation(generation, population, average_fitness)

    if generation >= max_gen and population[0].fitness > convergence_fitness:
        print("The algorithm did not converge within", max_gen, "generations.")

    # Plot convergence curves
    plt.plot(averages, label="Average fitness")
    plt.plot(bests, label="Best fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc='best')
    plt.show()

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


def classify(examples):
    for e in examples:
        if e.target == 0:
            class0.append(e)
        elif e.target == 1:
            class1.append(e)
    return class0, class1


def init_population(size):
    pop = []
    for _ in range(size):
        i = Individual()
        pop.append(i)
    return pop


def fitness(population):
    total_fitness = 0
    for i in population:
        # Obtain values for fitness calculation
        present_features = i.features.count(1)
        matches = conflicts(i)
        total_features = len(i.features)

        # Obtain fitness value
        golf_fitness = total_features * matches + present_features

        # We want a higher value to be better so inverse the fitness in relation to the highest possible golf_fitness
        #worst_fitness = total_features * (len(class1) * len(class0)) + total_features
        i.fitness = golf_fitness  # worst_fitness / golf_fitness

        total_fitness += i.fitness
    sort(population)
    return total_fitness / len(population), total_fitness


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


def sort(population):
    population.sort(key=lambda individual: individual.fitness, reverse=False)


def print_generation(generation, population, average_fitness):
    print("Generation: ", generation)
    print("Population size: ", len(population))
    print("Average fitness: ", average_fitness)
    sort(population)
    print("Best solution: ", population[0], "Fitness: ", population[0].fitness)
    print()


# TODO Determine other termination criteria?
def terminate(population, generation, convergence_fitness, max_gen):
    sort(population)
    return population[0].fitness <= convergence_fitness and generation >= max_gen


def parent_selection(population):
    # Get total population fitness and sort the population
    _, total_fitness = fitness(population)
    sort(population)
    roulette_wheel = []
    total_roulette_size = 0
    for res in population:
        roulette_wheel.append((total_fitness/res.fitness))
        total_roulette_size += total_fitness/res.fitness

    print(total_roulette_size)
    i = 0
    for val in roulette_wheel:
        print(val, " ", population[i].fitness)


    # Begin parent selection
    mating_pool = []
    for _ in range(int(len(population) / 2)):
        parents = []
        while len(parents) < 2:
            r = random.uniform(0, total_roulette_size)
            p = 0
            index = 0
            for i in roulette_wheel:
                if p + i > r:
                    if population[index] not in parents:
                        parents.append(population[index])
                    break
                else:
                    p += i
                    index += 1
        mating_pool.append(parents)
    return mating_pool


def crossover(parent1, parent2, op, n, pc):
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


def mutation(child, op, pm):
    if op == 'default':
        for i in range(len(child.features)):
            if random.random() < pm:
                child.features[i] = 1 - child.features[i]
    else:
        if random.random() < pm and op in ['1-flip', 'multi-flip']:
            flips = 1 if op == '1-flip' else random.randrange(len(child.features))
            flip_points = random.sample(range(len(child.features)), flips)  # Generate flipping points
            for p in flip_points:
                child.features[p] = 1 - child.features[p]


# TODO Decide on other survivor selection technique?
def survivor_selection(population, children):
    # Replace entire population with children
    return copy.deepcopy(children)
