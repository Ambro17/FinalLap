import functools
import random
from typing import Type, List, Tuple
from deap import base
from deap import creator
from deap import tools

from laptop_loader import load_laptops, Laptop


class Database:
    def __init__(self, laptops: List['Laptop']):
        self.laptops = laptops

    def get_random(self) -> 'Laptop':
        """Return a random laptop from the database"""
        return random.choice(self.laptops)

    def mate(self, one_laptop, other_laptop):
        """Return an existing laptop with intersection of attributes from the two laptops"""
        # Elijo una DISTINTA a estas dos, que exista.
        # Va a ser mejor o peor?


toolbox = base.Toolbox()
db = Database(laptops=load_laptops())


def mate(laptop1: Laptop, laptop2: Laptop):
    laptops_bag = [db.get_random() for _ in range(20)]
    laptops_by_similarity = [
        (
            candidate,
            similarity_score(laptop1, candidate),
            similarity_score(laptop2, candidate),
        )
        for candidate in laptops_bag
    ]

    laptops_por_similitud = sorted(laptops_by_similarity, key=lambda tupla: tupla[1][0])
    laptops_por_similitud2 = sorted(laptops_by_similarity, key=lambda tupla: tupla[2][0])
    mas_similar = next(laptop for laptop in laptops_por_similitud if laptop != laptop1 and laptop != laptop2)
    mas_similar2 = next(laptop for laptop in laptops_por_similitud2 if laptop != laptop1 and laptop != laptop2)
    return mas_similar, mas_similar2


def similarity_score(laptop1: Laptop, laptop2: Laptop):
    return evaluate_fitness(laptop1, laptop2)


def evaluate_fitness(laptop: Laptop, ideal_laptop: Laptop) -> Tuple[int]:
    """Evaluate how good of a match is a laptop against a given laptop

    It is expected to freeze the ideal_laptop argument once it's defined by the user
    That way, this function accepts a single argument representing the individual as expected by DEAP
    """
    fitness = 0
    if laptop.price > ideal_laptop.price:
        fitness -= 1
    else:
        fitness += 1

    if laptop.weight > ideal_laptop.weight:
        fitness -= 1
    else:
        fitness += 1

    if laptop.display_size < ideal_laptop.display_size:
        fitness -= 0.5
    else:
        fitness += 0.5

    if ideal_laptop.brand != 'ANY':
        if laptop.brand != ideal_laptop.brand:
            fitness -= 1
        else:
            fitness += 1

    return (fitness, )


def create_entities(ideal_laptop):
    """Create entities required for the genetic algorithm

    - Individual with fitness, and domain attributes
    - Function that creates individuals given a set of attributes (population generator)
    """

    # Create Laptop class with fitness attribute to save individual aptitude
    creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
    creator.create(
        "Laptop",
        Laptop,
        fitness=creator.FitnessMax,
    )
    # Create function that dynamically creates individuals of a population based on same criteria
    # In this case the criteria is hardcoding params
    # But it will be a method that reads a laptopt database and generates from there
    def create_individual(creator_class: Type[Laptop], **laptop_keyword_args):
        return db.get_random()  # No genera todas

    toolbox.register("laptop", create_individual, creator.Laptop)
    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.laptop
        # Notice we don't fix the last argument of
        # tools.initRepeat, that is the amount of individuals of our population
    )

    evaluate = functools.partial(evaluate_fitness, ideal_laptop=ideal_laptop)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", mate)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0)  # indpb: Independent probability of each integer of being mutated
    toolbox.register("select", tools.selTournament, tournsize=10)

    return toolbox


def evaluate_population(population):
    # Calculate fitness for each individual
    fitnesses = map(toolbox.evaluate, population)
    for individual, fitness_values in zip(population, fitnesses):
        individual.fitness.values = fitness_values


def main(my_ideal_laptop):
    create_entities(my_ideal_laptop)
    population = toolbox.population(n=1000)  # Aca. Que la generacion genere todas,en lugar de N random

    evaluate_population(population)

    mate_probability = 0.5
    iterations = 0
    max_fitness = 2.5 if my_ideal_laptop.brand == 'ANY' else 3.5
    print("Valor ideal:", max_fitness)

    fits = [ind.fitness.values[0] for ind in population]
    while max(fits) < max_fitness and iterations < 20:
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

        # Now that individuals changed, the mutation is no longer representative.
        # Let's recalculate it
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in population]
        best = sorted([x for x in population], key=lambda ind: ind.fitness.values[0])
        print('Mejores:', [(x.name, x.fitness.values[0]) for x in best[:5]])

        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    best = max([x for x in population], key=lambda p: p.fitness.values[0])
    print(best)


def thebest(my_ideal_laptop):
    for l in db.laptops:
        l.fitness.values = evaluate_fitness(l, my_ideal_laptop)

    scored = sorted(db.laptops, key=lambda lap: lap.fitness.values[0])
    print([f'{x.name} {x.fitness.values[0]}' for x in scored[:5]])


my_ideal_laptop = Laptop(name='Pavilion', price=2000, weight=5, display_size=13, brand='Chuwi')
print('Ingresada: ', my_ideal_laptop)
main(my_ideal_laptop)

