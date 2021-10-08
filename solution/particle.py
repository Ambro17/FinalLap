from typing import Type
from pprint import pprint
from deap import base
from deap import creator


class Particle:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

    def __repr__(self):
        return f'{self.__class__.__name__!s}(position={self.position}, speed={self.speed})'


def initialize_entities():
    """Create entities required for the genetic algorithm

    - Individual with fitness, speed and position attributes
    - Function that creates individuals given a set of attributes (population generator)
    """
    toolbox = base.Toolbox()

    # Create Particle class with fitness attribute to save individual aptitude
    creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
    creator.create(
        "Particle",
        Particle,
        fitness=creator.FitnessMax,
        __str__=lambda self: f'Particle(speed={self.speed}, position={self.position})')


    # Create function that dynamically creates individuals of a population based on same criteria
    def create_individual(creator_class: Type[Particle], position, speed):
        return creator_class(position=position, speed=speed)

    toolbox.register("particle", create_individual, creator.Particle)

    return toolbox

toolbox = initialize_entities()
population = [toolbox.particle(position=x, speed=1) for x in range(10)]
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