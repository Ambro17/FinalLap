import random
from typing import Type

from deap import base
from deap import creator

class Particle:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed


def create_individual(creator_class: Type[Particle], position, speed):
    return creator_class(position=position, speed=speed)


creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create(
    "Particle", 
    Particle,
    fitness=creator.FitnessMax,
    __str__=lambda self: f'Particle(speed={self.speed}, position={self.position})')


def initParticle(particleclass, max_speed, min_position, max_position):
    """Creates particle from defined parameters"""
    particle = particleclass()
    particle.speed = random.randint(1, max_speed)
    particle.position = random.randint(min_position, max_position)
    return particle

toolbox = base.Toolbox()
toolbox.register("particle", create_individual, creator.Particle)


p = toolbox.particle(position=0, speed=1)
print(p)
p.fitness.values = (1, )
assert p.fitness.valid is True
del p.fitness.values
assert p.fitness.valid is False
p.fitness.values = (10, )
print(p.fitness)