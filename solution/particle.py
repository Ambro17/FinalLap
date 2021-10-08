import random

from deap import base
from deap import creator

class Particle:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed


def create_individual(creator_class, position, speed):
    return creator_class(position=position, speed=speed)


creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create(
    "Particle", 
    list, 
    fitness=creator.FitnessMax, 
    speed=None,
    position=None,
    __str__=lambda self: f'Particle(speed={self.speed}, position={self.position})')

def initParticle(particleclass, max_speed, min_position, max_position):
    """Creates particle from defined parameters"""
    particle = particleclass()
    particle.speed = random.randint(1, max_speed)
    particle.position = random.randint(min_position, max_position)
    return particle

toolbox = base.Toolbox()
toolbox.register("particle", initParticle, creator.Particle)


p = toolbox.particle(max_speed=2, min_position=-3, max_position=3)
print(p)