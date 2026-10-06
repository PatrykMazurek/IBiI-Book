import numpy as np
import pandas as pd


oceny = np.array([
    [4, 5, 3, 5],  # Uczeń 0
    [2, 3, 4, 3],  # Uczeń 1
    [5, 5, 5, 4]   # Uczeń 2
])

# 1. Jaka jest średnia z CAŁEJ klasy ze wszystkich przedmiotów?
srednia_ogolna = np.mean(oceny)
print(srednia_ogolna)
# 2. Jakie są średnie z poszczególnych PRZEDMIOTÓW?

srednia_przedmioty = np.mean(oceny, axis=0)
print(srednia_przedmioty)
# 3. Jakie są średnie na koniec roku poszczególnych UCZNIÓW?
srednia_uczniowie = np.mean(oceny, axis=1)
print(srednia_uczniowie)