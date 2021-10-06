"""
Tutorial: https://deap.readthedocs.io/en/master/examples/ga_onemax.html
"""
import random

from deap import base
from deap import creator
from deap import tools

# Individuals will be list of ints
# Generate population using them
# Add some functions and operators to evolve

# Create evaluation function with only one weight
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Create Individual class with a fitness attribute 
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Generate random ints either 0 or 1
toolbox.register("attr_bool", random.randint, 0, 1)

# Enable toolbox.Individual to generate an 'Individual' with a
# a list of 100 random integers either 1 or 0
"""
Equivalent to
creator.Individual(toolbox.attr_bool, 100) -> 
[0 1 1 0 0 0 1 ... n] where n=100 of random 0s or 1s
"""
NUMBERS_ARRAY_LEN = 100 
toolbox.register(
    "individual",
    tools.initRepeat, 
    creator.Individual,
    toolbox.attr_bool,
    NUMBERS_ARRAY_LEN
)
toolbox.register(
    "population", 
    tools.initRepeat, 
    list, 
    toolbox.individual
    # Notice we don't fix the last argument of 
    # tools.initRepeat, that is the amount of individuals of our population 
)

def evaluate_individual(individual):
    # As it inherits from list, sum works. 
    # Why a tuple? Because of weights=(1.0,) on our FitnessMax function
    return (sum(individual), )

toolbox.register("evaluate", evaluate_individual)
toolbox.register("mate", tools.cxTwoPoint) # Cruza
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) # indpb: Independent probability of each integer of being mutated
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    # Generate population with our partially initialized population function.
    population = toolbox.population(n=300)
    
    # Calculate fitness for each individual
    fitnesses = map(toolbox.evaluate, population)
    for individual, fitness_values in zip(population, fitnesses):
        individual.fitness.values = fitness_values

    mate_probability = 0.5
    mutation_probability = 0.2

    fits = [ind.fitness.values[0] for ind in population]    

    # Begin the evolution
    iterations = 0
    # Mientras no sean todos 1s y haya menos de mil iteraciones..
    while max(fits) < NUMBERS_ARRAY_LEN and iterations < 1000:
        iterations = iterations + 1
        print("-- Generation %i --" % iterations)

        # Generate a new population of the same length
        offspring = toolbox.select(population, len(population))

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))        

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < mate_probability:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_probability:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Now that individuals changed, the mutation is no longer representative.
        # Let's recalculate it
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in population]
        
        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        import time; time.sleep(0.5)

main()