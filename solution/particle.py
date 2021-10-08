import random

from deap import base
from deap import creator

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create(
    "Particle", 
    list, 
    fitness=creator.FitnessMax, 
    speed=None,
    position=None,
    __str__=lambda self: f'Particle(speed={self.speed:.2f}, position={self.position})')

def initParticle(particleclass, max_speed, min_position, max_position):
    """Creates particle from defined parameters"""
    part = particleclass()
    part.speed = random.uniform(1, max_speed)
    part.position = random.randint(min_position, max_position)
    return part

toolbox = base.Toolbox()
toolbox.register("particle", initParticle, creator.Particle)


p = toolbox.particle(max_speed=2, min_position=-3, max_position=3)
print(p)