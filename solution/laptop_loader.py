import csv
import json
import sys
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import Optional
import dataclasses
from deap import base



class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, object):
        if is_dataclass(object):
            return dataclasses.asdict(object)
        return super().default(object)


PARENT = Path(__file__).absolute().parent


class MyFitness(base.Fitness):
    weights = (1.0, )


@dataclass
class Laptop:
    name: str
    price: int
    weight: float
    display_size: float
    brand: Optional[str] = 'ANY'
    fitness: int = MyFitness(values=(-100, ))

    def __str__(self):
        return (
            f'{self.brand} {self.name} {self.display_size}" U$D{self.price} {self.weight}Kg'
        )


def parse_storage(storage_expression):
    """Parse storage in GB"""
    try:
        return int(storage_expression.split('GB')[0])
    except ValueError:
        return int(storage_expression.split('TB')[0]) * 1024


def load_laptops():
    laptops = []
    with open(PARENT / 'laptops_2019.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                laptops.append(
                    Laptop(
                        name=row['Model Name'],
                        price=int(float(row['Price (Euros)'].replace(',', '.')) * 1.16),  # Replace comma by dot
                        weight=float(row['Weight'].split('k')[0]),  # '1kg -> 2; 4kks -> 4'
                        display_size=float(row['Screen Size'].replace('"', '')),  # Remove inches symbol
                        brand=row['Manufacturer'],
                    )
                )

            except ValueError as e:
                print(repr(e))
                print(row)
                sys.exit(1)
    laptops.sort(key=lambda x: (x.brand, x.name))
    return laptops
