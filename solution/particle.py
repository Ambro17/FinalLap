import dataclasses
import random
from typing import Type
from pprint import pprint
from deap import base
from deap import creator


@dataclasses.dataclass
class Laptop:
    name: int
    price: int


def initialize_entities():
    """Create entities required for the genetic algorithm

    - Individual with fitness, and domain attributes
    - Function that creates individuals given a set of attributes (population generator)
    """
    toolbox = base.Toolbox()

    # Create Laptop class with fitness attribute to save individual aptitude
    creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
    creator.create(
        "Laptop",
        Laptop,
        fitness=creator.FitnessMax,
        __str__=lambda self: f'Laptop(name={self.name}, price={self.price})')

    # Create function that dynamically creates individuals of a population based on same criteria
    # In this case the criteria is hardcoding params
    # But it will be a method that reads a laptopt database and generates from there
    def create_individual(creator_class: Type[Laptop], name, price):
        return creator_class(name=name, price=price)

    toolbox.register("laptop", create_individual, creator.Laptop)

    return toolbox

toolbox = initialize_entities()
population = [toolbox.laptop(name=f'Laptop {x}', price=random.randint(500, 1500)) for x in range(10)]
print('Population:', end=' \n')
pprint(population)
p = population[0]
print('Individual: ', p)
p.fitness.values = (1, )
assert p.fitness.valid is True
del p.fitness.values
assert p.fitness.valid is False
p.fitness.values = (10, )
print('Fitness: ', p.fitness)