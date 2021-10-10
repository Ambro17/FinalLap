# -*- coding: utf-8
"""
La idea es acotar el conjunto de bits válidos mediante enums
Y distinguir entre LaptopSpec (conjunto de requisitos de una laptop)
Y una laptop existente
Lo autogenerado de forma aleatoria van a ser las laptopspecs,
Luego, dadas esas specs puede existir una laptop o no
Si no existe, se penaliza, si existe, se trae un random de las que matchean

De esa forma tenemos generación aleatoria de individuos + penalización de inexistentes.

DUDA: Y como evaluamos el fitness de una spec? U obtenemos una laptop primero?

Por qué generamos individuos inexistentes? Por requerimiento de la cátedra, pues así es el algoritmo Genético
"""
import dataclasses
import enum
import random


class Database:
    def find_by_specs(self):
        pass


class UsageEnum(str, enum.Enum):
    Basic = 1
    Designer = 2
    Programmer = 3
    Gamer = 4


class PriceSegment(str, enum.Enum):
    UNDER_250 = 0
    UNDER_500 = 1
    UNDER_750 = 2
    UNDER_1000 = 3
    UNDER_1500 = 4
    UPPER_1500 = 5


class Brand(str, enum.Enum):
    APPLE = 1
    MICROSOFT = 2
    ACER = 3


class ScreenSize(str, enum.Enum):
    SIZE_11 = 11
    SIZE_13 = 13
    SIZE_15 = 15
    SIZE_17 = 17


class BatteryAutonomy(str, enum.Enum):
    AT_LEAST_4 = 4
    AT_LEAST_6 = 6
    AT_LEAST_8 = 8
    AT_LEAST_10 = 10
    AT_LEAST_12 = 12
    MORE_THAN_12 = 16


def num_to_binary(num):
    return f'{num:b}'


@dataclasses.dataclass
class LaptopSpec:
    brand: Brand
    price_segment: PriceSegment
    usage: UsageEnum
    screen_size: ScreenSize
    autonomy_in_hours: int

    def asbits(self):
        return [int(field.value) for name, field in self.__dict__.items()]


def generate_laptops():
    return [
        random_laptop_spec()
        for x in range(10)
    ]


def random_laptop_spec():
    return LaptopSpec(
        brand=random.choice(list(Brand)),
        price_segment=random.choice(list(PriceSegment)),
        usage=random.choice(list(UsageEnum)),
        screen_size=random.choice(list(ScreenSize)),
        autonomy_in_hours=random.choice(list(BatteryAutonomy)),
    )


laps = generate_laptops()
print([x.asbits() for x in laps])


@dataclasses.dataclass()
class Laptop:
    name: str

def recommended_laptop(spec: LaptopSpec) -> Laptop:
    """Search laptops by spec"""
    return Laptop(name='HARDCODED')

recommended_laptop(spec=random_laptop_spec())