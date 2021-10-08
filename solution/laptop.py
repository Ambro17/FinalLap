from dataclasses import dataclass
from decimal import Decimal
import functools
from typing import Optional


class Database:
    def exists(self, individual):
        return True


@functools.lru_cache()
def get_database():
    return Database()


@dataclass
class Laptop:
    name: str
    price: Decimal
    autonomy_in_hours: int
    weight: float
    display_size: float
    brand: Optional[str] = 'ANY'


def evaluate_fitness(laptop: Laptop, ideal_laptop: Laptop) -> int:
    db = get_database()

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


def best_match():
    # Create your ideal laptop
    my_ideal_laptop = Laptop(name='ideal', price=2500, autonomy_in_hours=10, weight=2, display_size=15)

    # Freeze the argument of the ideal laptop in the evaluate function
    # So that it takes only one argument, as expected by deap
    evaluate = functools.partial(evaluate_fitness, ideal_laptop=my_ideal_laptop)

    bad_laptop = Laptop(name='bad', price=1000, autonomy_in_hours=5, weight=1.5, display_size=12.3)
    good_laptop = Laptop(name='good', price=1500, autonomy_in_hours=7, weight=3, display_size=17)
    cheap_laptop = Laptop(name='cheap', price=500, autonomy_in_hours=11, weight=1, display_size=15)
    expensive_laptop = Laptop(name='expensive', price=2000, autonomy_in_hours=6, weight=3, display_size=15)
    print('Bad Laptop score:', evaluate(bad_laptop))
    print('Good Laptop score:', evaluate(good_laptop))
    print('Cheap Laptop score:', evaluate(cheap_laptop))
    print('Expensive Laptop score:', evaluate(expensive_laptop))
    laptops = [bad_laptop, good_laptop, cheap_laptop, expensive_laptop]
    sorted_laptops = sorted(laptops, key=evaluate)
    print('Best Match: ', sorted_laptops[0])

best_match()