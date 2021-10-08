"""
La función de evaluación deberá ser un array que minimize infracciones y maximice requisitos cumplidos.
Los parámetros a evaluar son
- Precio ($)
- Uso (Básico, Diseñador, Programador, Gaming) (U)
- Autonomía de la Batería (A)
- Peso (P)
- Marca (M)
- Tamaño de Pantalla (T)
- Cantidad de Requisitos Incumplidos (X)
"""
import random

from deap import base
from deap import creator
from deap import tools


def database():
    pass


def create_world():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    world = base.Toolbox()

    # Generate random ints either 0 or 1
    world.register("attr_bool", random.randint, 0, 1)
    world.register(
        "individual",
        tools.initRepeat, 
        creator.Individual,
        world.attr_bool,
        NUMBERS_ARRAY_LEN
    )
    world.register(
        "population", 
        tools.initRepeat, 
        list, 
        world.individual
        # Notice we don't fix the last argument of 
        # tools.initRepeat, that is the amount of individuals of our population 
    )
    return world

NUMBERS_ARRAY_LEN = 100 
world = create_world(NUMBERS_ARRAY_LEN)


def evaluate_individual(individual):
    # As it inherits from list, sum works. 
    # Why a tuple? Because of weights=(1.0,) on our FitnessMax function
    return (sum(individual), )

world.register("evaluate", evaluate_individual)
world.register("mate", tools.cxTwoPoint) # Cruza
world.register("mutate", tools.mutFlipBit, indpb=0.05) # indpb: Independent probability of each integer of being mutated
world.register("select", tools.selTournament, tournsize=3)


def main():
    # Generate population with our partially initialized population function.
    population = world.population(n=300)
    
    # Calculate fitness for each individual
    fitnesses = map(world.evaluate, population)
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
        offspring = world.select(population, len(population))

        # Clone the selected individuals
        offspring = list(map(world.clone, offspring))        

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < mate_probability:
                world.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_probability:
                world.mutate(mutant)
                del mutant.fitness.values

        # Once you del individual.fitness.values the fitness is marked as invalid.
        # So we need to recalculate it for those individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(world.evaluate, invalid_ind)
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