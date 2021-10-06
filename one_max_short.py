"""Tutorial: https://deap.readthedocs.io/en/master/examples/ga_onemax_short.html"""
import random
import numpy

from deap import algorithms, creator
from deap import base
from deap import tools


def evalOneMax(individual):
    return (sum(individual), )


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

NUMBERS_ARRAY_LEN = 100 
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
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

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)



def main():
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
                                   stats=stats, halloffame=hof, verbose=True)
    print(hof)
    print(stats)

main()
