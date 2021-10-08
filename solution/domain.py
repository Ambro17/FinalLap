from dataclasses import dataclass
import functools
import random
from typing import Type, Optional
from pprint import pprint
from deap import base
from deap import creator


class Database:
    def exists(self, individual: 'Laptop'):
        return True

    def get(self) -> 'Laptop':
        """Return a random laptop from the database"""
        return Laptop('Name', 1000, 12, 1, 15)


@dataclass
class Laptop:
    name: str
    price: int
    autonomy_in_hours: int
    weight: float
    display_size: float
    brand: Optional[str] = 'ANY'

    def __str__(self) -> str:
        return self.name


def evaluate_fitness(laptop: Laptop, ideal_laptop: Laptop, db: Database) -> int:
    """Evaluate how good of a match is a laptop against a given laptop

    It is expected to freeze the ideal_laptop argument once it's defined by the user
    That way, this function accepts a single argument representing the individual as expected by DEAP
    """
    if not db.exists(laptop):
        return -100

    fitness = 0
    if laptop.price > ideal_laptop.price:
        fitness -= 1
    else:
        fitness += 1

    if laptop.weight > ideal_laptop.weight:
        fitness -= 1
    else:
        fitness += 1

    if laptop.display_size > ideal_laptop.display_size:
        fitness -= 0.5
    else:
        fitness += 0.5

    if laptop.autonomy_in_hours < ideal_laptop.autonomy_in_hours:
        fitness -= 1
    else:
        fitness += 1

    if laptop.brand != 'ANY' and laptop.brand != ideal_laptop.brand:
        fitness -= 1
    else:
        fitness += 1

    return fitness


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
    )
    # Create function that dynamically creates individuals of a population based on same criteria
    # In this case the criteria is hardcoding params
    # But it will be a method that reads a laptopt database and generates from there
    def create_individual(creator_class: Type[Laptop], **laptop_keyword_args):
        return creator_class(**laptop_keyword_args)

    toolbox.register("laptop", create_individual, creator.Laptop)

    return toolbox



def create_population_and_validate_fitness(toolbox):
    population = [toolbox.laptop(
        name=f'Laptop {x}', price=random.randint(500, 1500), autonomy_in_hours=10, weight=2.5, display_size=15
    ) for x in range(10)]
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


print('Creating population and validating some things ✨')
create_population_and_validate_fitness(initialize_entities())

def get_best_match():
    # Create your ideal laptop
    my_ideal_laptop = Laptop(name='ideal', price=2500, autonomy_in_hours=10, weight=2, display_size=15)

    # Freeze the argument of the ideal laptop in the evaluate function
    # So that it takes only one argument, as expected by deap library
    evaluate = functools.partial(evaluate_fitness, ideal_laptop=my_ideal_laptop, db=Database())

    bad_laptop = Laptop(name='bad Laptop', price=1000, autonomy_in_hours=5, weight=1.5, display_size=12.3)
    good_laptop = Laptop(name='good Laptop', price=1500, autonomy_in_hours=7, weight=3, display_size=17)
    cheap_laptop = Laptop(name='cheap Laptop', price=500, autonomy_in_hours=11, weight=1, display_size=15)
    expensive_laptop = Laptop(name='expensive Laptop', price=2000, autonomy_in_hours=6, weight=3, display_size=15)

    print('Bad Laptop score:', evaluate(bad_laptop))
    print('Good Laptop score:', evaluate(good_laptop))
    print('Cheap Laptop score:', evaluate(cheap_laptop))
    print('Expensive Laptop score:', evaluate(expensive_laptop))

    laptops = [bad_laptop, good_laptop, cheap_laptop, expensive_laptop]
    sorted_laptops = sorted(laptops, key=evaluate)
    print('Sorted Laptops by score', list(map(str, sorted_laptops)))
    print('Best Match: ', sorted_laptops[0])

print('Choosing best laptop 🪄')
get_best_match()