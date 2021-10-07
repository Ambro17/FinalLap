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


# Are this required?
PRICE_LIMITS_PER_CATEGORY = {0: 250, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2000, 6: 10_000}
AUTONOMY_IN_HOURS = set(range(1, 24))
WEIGHT_IN_KG = {0: 1, 1: 1.5, 2: 2, 3: 10}
BRAND = {'APPLE', 'MICROSOFT', 'ACER', 'ASUS', 'MSI', 'HP'}
DISPLAY_SIZE_IN_INCHES = {0: 12, 1: 13, 2: 14, 3: 15, 4: 17, 5: 20}


@dataclass
class Laptop:
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


my_ideal_laptop = Laptop(price=2500, autonomy_in_hours=10, weight=2, display_size=15)
bad_laptop = Laptop(price=1000, autonomy_in_hours=5, weight=1.5, display_size=12.3)
good_laptop = Laptop(price=1500, autonomy_in_hours=7, weight=3, display_size=17)
cheap_laptop = Laptop(price=500, autonomy_in_hours=11, weight=1, display_size=15)
expensive_laptop = Laptop(price=2000, autonomy_in_hours=6, weight=3, display_size=15)

evaluate = functools.partial(evaluate_fitness, ideal_laptop=my_ideal_laptop)

print('Bad Laptop score:', evaluate(bad_laptop))
print('Good Laptop score:', evaluate(good_laptop))
print('Cheap Laptop score:', evaluate(cheap_laptop))
print('Expensive Laptop score:', evaluate(expensive_laptop))