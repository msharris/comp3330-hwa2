import copy
import random


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
        return str(feature_set) + " " + str(self.fitness)


# Declare class lists globally for ease of use
class0, class1 = [], []


def ga(examples, pop_size, crossover_op='1-point', n=1, pc=0.75, mutation_op='default', pm=0.075):
    # Classify each example
    classify(examples)

    # Initialise population
    population = init_population(pop_size)
    generation = 0

    # Find fitness of population
    _, avg_fitness = fitness(population, golf=True)

    # Print the characteristics of the initial population
    print_generation(generation, population, avg_fitness)

    while not terminate(population, generation):
        # Generate a new population
        children = []
        for _ in range(int(len(population) / 2)):
            # Perform parent selection
            parent1, parent2 = parent_selection(population)

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
        _, avg_fitness = fitness(population, golf=True)
        print_generation(generation, population, avg_fitness)
        generation += 1

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


def fitness(population, golf=False):
    if golf:
        return golf_fitness(population)
    else:
        return regular_fitness(population)


def golf_fitness(population):
    pop_fitness = 0
    for i in population:
        features = i.features.count(1)
        matches = conflicts(i)
        i.fitness = 12 * matches + features
        pop_fitness += i.fitness
    return pop_fitness, pop_fitness / len(population)


def regular_fitness(population):
    constant_val = (len(class0) * len(class1))
    pop_fitness = 0
    cost_max = len(population[0].features)  # Assumes that all members of population have the same size genotype.
    for i in population:
        cost = i.features.count(1)
        accuracy = 100-((conflicts(i)/constant_val)*100)
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


def sort(population):
    population.sort(key=lambda individual: individual.fitness, reverse=False)


def print_generation(generation, population, average_fitness):
    print("Generation: ", generation)
    print("Population size: ", len(population))
    print("Average fitness: ", average_fitness)
    sort(population)
    print("Best solution: ", population[0])
    print()


# TODO Determine termination criteria
def terminate(population, generation):
    sort(population)
    #score = 100 - (6/101) + len(population[0].features)
    return population[0].fitness <=5 or generation >= 1000


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


def mutation(child, op='default', pm=0.1):
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


# TODO Decide on survivor selection technique
def survivor_selection(population, children):
    # Replace entire population with children
    return copy.deepcopy(children)
