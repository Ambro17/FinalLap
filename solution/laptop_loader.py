import csv
import json
import sys
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import Optional
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, object):
        if is_dataclass(object):
            return dataclasses.asdict(object)
        return super().default(object)


@dataclass
class Laptop:
    name: str
    price: int
    autonomy_in_hours: int
    weight: float
    display_size: float
    cpu: str
    has_dedicated_gpu: bool
    ram: int
    storage_in_gb: int
    operating_system: str
    brand: Optional[str] = 'ANY'

    def __str__(self):
        return (
            f'{self.brand} {self.name} {self.cpu} {self.ram}GB '
            f'{self.storage_in_gb}GB {self.display_size}" {self.operating_system}'
        )


def parse_storage(storage_expression):
    """Parse storage in GB"""
    try:
        return int(storage_expression.split('GB')[0])
    except ValueError:
        return int(storage_expression.split('TB')[0]) * 1024


def load_laptops(filepath):
    laptops = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                laptops.append(
                    Laptop(
                        name=row['Model Name'],
                        price=int(float(row['Price (Euros)'].replace(',', '.')) * 1.16),  # Replace comma by dot
                        autonomy_in_hours=10,  # TODO: Figure out a way to infer it.
                        weight=float(row['Weight'].split('k')[0]),  # '1kg -> 2; 4kks -> 4'
                        display_size=float(row['Screen Size'].replace('"', '')),  # Remove inches symbol
                        brand=row['Manufacturer'],
                        cpu=row['CPU'],
                        has_dedicated_gpu=bool('Intel' not in row['GPU']),
                        ram=int(row['RAM'].split('GB')[0]),
                        storage_in_gb=parse_storage(row['Storage']),
                        operating_system=row['Operating System']
                    )
                )

            except ValueError as e:
                print(repr(e))
                print(row)
                sys.exit(1)
    laptops.sort(key=lambda x: (x.brand, x.name))
    return laptops

LAPTOPS_CSV = Path(__file__).absolute().parent / 'laptops_2019.csv'
#load_laptops(LAPTOPS_CSV)