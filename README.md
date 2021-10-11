# FinalLap
![Image of Final Lap](finallap.png)

Este repo implementa un algoritmo genético para recomendar una laptop a partir de las preferencias de un usuario.

Las características que serán evaluadas para encontrar la notebook recomendada son
- Precio ($)
- Uso (Básico, Diseñador, Programador, Gaming) (U)
- Autonomía de la Batería (A)
- Peso (P)
- Marca (M)
- Tamaño de Pantalla (T)

## TODO
- [x] Get collection of laptops to populate database - ✅ Done from csv
- [ ] Create mate algorithm
- [x] Create mutate algorithm (Should we allow invalid laptops? That is, those not in db?) - ✅ Not required
- [ ] Create select algoritm (Ojo a que optimice y no quede clavado)
- [ ] Condense into runnable script that executes the genetic algorithm


## Implementación

Mediante la construcción de una base de datos de computadoras,
se partirá de los parámetros deseados y mediante iteraciones con cruza y mutación, se llegará a una laptop recomendada.

## Tecnologías
- Python - Lenguaje de Programación
- Deap   - Librería para implementar el algoritmo

## Uso
Linux: 
```
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
python example.py
```
Windows: 
```
python3 -m venv .venv && \
.venv/Scripts/activate && \
pip install -r requirements.txt && \
python example.py
```
Docker:
```
docker build . -t finallap && docker run -it --rm finallap
python example.py
python solution/domain.py
python solution/main.py
```
