import functools
import random
from typing import Type, List
from deap import base
from deap import creator
from pprint import pprint

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


def mate(db: Database, laptop1: Laptop, laptop2: Laptop):
    # 10 00
    # 01 11
    # --|--
    # 10 11
    # Parecido a L1
    # Parecido a L2
    """
    Op 1.
    Agarrar 10 laptops
    Evaluar la similitud contra la L1 y la L2
    Quedarnos con las mas parecida a ambas
    """
    laptops_bag = [db.get_random() for _ in range(200)]  # TODO: Modificar si optimiza demasiado rapido
    laptops_by_similarity = [
        (
            candidate,
            similarity_score(laptop1, candidate),
            similarity_score(laptop2, candidate),
        )
        for candidate in laptops_bag
    ]

    similar_a_1 = max(laptops_by_similarity, key=lambda tupla: tupla[1])
    similar_a_2 = max(laptops_by_similarity, key=lambda tupla: tupla[2])
    return similar_a_1[0], similar_a_2[0]


def similarity_score(laptop1: Laptop, laptop2: Laptop):
    return evaluate_fitness(laptop1, laptop2)


def evaluate_fitness(laptop: Laptop, ideal_laptop: Laptop) -> int:
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

    if laptop.display_size > ideal_laptop.display_size:
        fitness -= 0.5
    else:
        fitness += 0.5

    if laptop.brand != 'ANY':
        if laptop.brand != ideal_laptop.brand:
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


def get_best_match():
    # Create your ideal laptop
    extra_args = {
        "cpu": 'i5',
        "has_dedicated_gpu": False,
        "ram": 8,
        "storage_in_gb": 512,
        "operating_system": "Windows",
    }
    my_ideal_laptop = Laptop(name='ideal', price=2500, weight=2, display_size=15, **extra_args)

    # Load laptops from csv
    laptops = load_laptops()

    # Freeze the argument of the ideal laptop in the evaluate function
    # So that it takes only one argument, as expected by deap library
    evaluate = functools.partial(evaluate_fitness, ideal_laptop=my_ideal_laptop)

    print(laptops[0].name, evaluate(laptops[0]))
    print(laptops[1].name, evaluate(laptops[1]))
    print(laptops[2].name, evaluate(laptops[2]))

    laps = laptops[:3]
    sorted_laptops = sorted(laps, key=evaluate, reverse=True)
    print('Sorted Laptops by score', list(map(str, sorted_laptops)))
    print('Best Match: ', sorted_laptops[0])


def load_laptops2():
    laptops = load_laptops()
    db = Database(laptops=laptops)
    print('Random laptop:', db.get_random())
    assert isinstance(db.get_random(), type(laptops[0]))


def main():
    # Crear poblacion
    # Cruzar
    # Mutar (prob=0)
    # Seleccionar nueva poblacion
    # Cortar cuando pasa algo. Elegi un optimo, o freno por cant iteraciones
    pass


laptops = load_laptops()
db = Database(laptops=laptops)
print(laptops[0])
print(laptops[-1])
lap1, lap2 = mate(db, laptops[0], laptops[-1])
print(lap1)
print(lap2)