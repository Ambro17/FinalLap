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

PARENT = Path(__file__).absolute().parent

@dataclass
class Laptop:
    name: str
    price: int
    autonomy_in_hours: int
    weight: float
    display_size: float
    brand: Optional[str] = 'ANY'


laptops = []
with open(PARENT / 'laptops_2019.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            laptops.append(
                Laptop(
                    name=row['Model Name'],
                    price=int(float(row['Price (Euros)'].replace(',', '.')) * 1.16), # Replace comma by dot
                    autonomy_in_hours=10,  # TODO: Figure out a way to infer it.
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


with open('results.json', 'w') as f:
    json.dump(laptops, f, cls=EnhancedJSONEncoder, indent=2, sort_keys=True)
