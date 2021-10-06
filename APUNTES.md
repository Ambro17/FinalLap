La función de evaluación deberá ser un array que minimize infracciones y maximice requisitos.
Los parámetros a evaluar son
- Precio ($)
- Uso (Básico, Diseñador, Programador, Gaming) (U)
- Autonomía de la Batería (A)
- Peso (P)
- Marca (M)
- Tamaño de Pantalla (T)
- Cantidad de Requisitos Incumplidos (X)
Minimizar requisitos no cumplidos


if laptop_no_existe:
    penalizar 1000, ...

requisitos_incumplidos = calcular_reqs_incumplidos(individual)
if requisito_incumplidos:
    penalizar len(requisitos), ...




(-1,  1,  1,  1,  1,  1,  1)

| X | $ | U | A | P | M | T |
|---|---|---|---|---|---|---|
|-1 | 1 |   |   |   | 5 |   |
|   |   | 2 |   | 4 |   | 1 |
|   |   |   | 3 |   |   | 1 |